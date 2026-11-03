"""Qwen3-TTS render worker. Runs inside its own venv (~/faceless-work/venvs/qwen3tts), never the pipeline env, and
never on a CUDA GPU: MPS on the Mac, else CPU.

Reads a JSON job file and writes one 24 kHz mono WAV per job:
  {"model_dir": ".../Qwen3-TTS-12Hz-1.7B-VoiceDesign", "dtype": "bf16",
   "jobs": [{"text": "...", "instruct": "...", "seed": 7, "out": "/path/a.wav", "language": "English",
             "ref_audio": null, "ref_text": null, "temperature": 0.9, "top_p": 1.0, "align_text": null}]}
With "align_text" (the plain script words of the job), it also writes <out>.words.json: [[word, start, end], ...]
from a CTC forced alignment (torchaudio MMS_FA), so the pipeline gets word timings without whisper.
A job with "ref_audio" uses the Base model's clone path (model_dir must then be a Base checkpoint). It is only ever
pointed at one of OUR OWN designed reference clips (voice design, then reuse), never at a real narrator's audio.

usage: <qwen3tts venv>/bin/python -I pipeline/audio/qwen3_worker.py jobs.json
Model code: github.com/QwenLM/Qwen3-TTS @022e286 (Apache-2.0), weights from the official Qwen HF repos only.
"""
import json
import os
import sys
import time

os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")


_ONES = ("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen "
         "seventeen eighteen nineteen").split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def _num(n):
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + ("" if n % 10 == 0 else " " + _ONES[n % 10])
    if n < 1000:
        return _ONES[n // 100] + " hundred" + ("" if n % 100 == 0 else " " + _num(n % 100))
    if n < 1000000:
        return _num(n // 1000) + " thousand" + ("" if n % 1000 == 0 else " " + _num(n % 1000))
    return " ".join(_ONES[int(c)] for c in str(n))


def _letters(word):
    import re
    w = word.lower().replace("\u2019", "'")
    if re.search(r"\d", w):
        w = re.sub(r"\d+", lambda m: " " + _num(int(m.group())) + " ", w.replace(",", ""))
    toks = [re.sub(r"[^a-z']", "", t).strip("'") for t in re.split(r"[\s\-\u2013\u2014]+", w)]
    return [t for t in toks if t]


_FA = None


def align(audio, sr, text):
    """[[word, start, end]] for the whitespace words of `text` (words with no letters get a zero-length slot)."""
    global _FA
    import numpy as np
    import torch
    import torchaudio
    if _FA is None:
        b = torchaudio.pipelines.MMS_FA
        _FA = (b, b.get_model(with_star=False).eval(), b.get_tokenizer(), b.get_aligner())
    b, model, tok, aligner = _FA
    wav = torch.from_numpy(audio.astype(np.float32))[None]
    if sr != b.sample_rate:
        wav = torchaudio.functional.resample(wav, sr, b.sample_rate)
    with torch.inference_mode():
        em, _ = model(wav)
    ratio = wav.shape[1] / em.shape[1] / b.sample_rate
    words = text.split()
    pieces, owner = [], []
    for i, w in enumerate(words):
        for t in _letters(w):
            pieces.append(t)
            owner.append(i)
    got = {}
    if pieces:
        for k, sp in enumerate(aligner(em[0], tok(pieces))):
            s, e = sp[0].start * ratio, sp[-1].end * ratio
            i = owner[k]
            got[i] = (min(s, got[i][0]), max(e, got[i][1])) if i in got else (s, e)
    out, last = [], 0.0
    for i, w in enumerate(words):
        s, e = got.get(i, (last, last))
        out.append([w, round(float(s), 3), round(float(e), 3)])
        last = e
    return out


def main(path):
    import numpy as np
    import soundfile as sf
    import torch
    from qwen_tts import Qwen3TTSModel

    spec = json.load(open(path))
    dev = os.environ.get("QWEN3_TTS_DEVICE") or ("mps" if torch.backends.mps.is_available() else "cpu")
    if dev.startswith("cuda"):
        raise SystemExit("qwen3_worker: CUDA is not allowed (Mac MPS or CPU only)")
    torch.set_num_threads(int(os.environ.get("TTS_THREADS", "6")))
    dtype = {"bf16": torch.bfloat16, "fp16": torch.float16, "fp32": torch.float32}[spec.get("dtype", "bf16")]
    t0 = time.time()
    model = Qwen3TTSModel.from_pretrained(os.path.expanduser(spec["model_dir"]), device_map=dev, dtype=dtype,
                                          attn_implementation="sdpa")
    print(f"[qwen3] loaded {os.path.basename(spec['model_dir'].rstrip('/'))} on {dev} {spec.get('dtype', 'bf16')} "
          f"in {time.time() - t0:.1f}s", flush=True)
    prompts = {}
    stats = []
    for job in spec["jobs"]:
        if os.path.exists(job["out"]) and not job.get("force"):
            continue
        torch.manual_seed(int(job.get("seed", 0)))
        np.random.seed(int(job.get("seed", 0)))
        kw = {k: job[k] for k in ("temperature", "top_p", "top_k", "repetition_penalty", "max_new_tokens") if k in job}
        t1 = time.time()
        if job.get("ref_audio"):
            key = (job["ref_audio"], job.get("ref_text"))
            if key not in prompts:
                prompts[key] = model.create_voice_clone_prompt(ref_audio=job["ref_audio"], ref_text=job.get("ref_text"))
            wavs, sr = model.generate_voice_clone(text=job["text"], language=job.get("language", "English"),
                                                  voice_clone_prompt=prompts[key], **kw)
        else:
            wavs, sr = model.generate_voice_design(text=job["text"], language=job.get("language", "English"),
                                                   instruct=job.get("instruct", ""), **kw)
        el = time.time() - t1
        a = np.asarray(wavs[0], dtype=np.float32)
        os.makedirs(os.path.dirname(job["out"]) or ".", exist_ok=True)
        sf.write(job["out"], a, sr)
        if job.get("align_text"):
            json.dump(align(a, sr, job["align_text"]), open(job["out"][:-4] + ".words.json", "w"))
        stats.append({"out": job["out"], "audio_s": round(len(a) / sr, 2), "gen_s": round(el, 1), "sr": sr})
        print(f"[qwen3] {os.path.basename(job['out'])}: {len(a) / sr:.2f}s audio in {el:.1f}s "
              f"(rtf {el / max(1e-3, len(a) / sr):.2f})", flush=True)
    if spec.get("stats_out"):
        json.dump(stats, open(spec["stats_out"], "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
