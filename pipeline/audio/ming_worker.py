"""Ming-3.0-tts render worker. Runs inside its own venv (~/faceless-work/venvs/ming), never the pipeline env, on the
CPU only (MPS crashes inside the model, CUDA is never used).

Reads a JSON job file and writes one WAV per job (the model's own rate):
  {"src": "~/faceless-work/src/Ming-3.0-tts", "model": "~/faceless-work/models/Ming-3.0-tts-0.5b",
   "ref_audio": ".../voices/ember_ref_ming.flac", "ref_text": "...", "instruction": "...",
   "jobs": [{"text": "...", "seed": 11, "out": "/path/c000.wav", "align_text": "..."}]}
Every job clones the same reference clip (TTS task, speaker embedding on) with the same instruction, so the voice
is the same in every chunk. With "align_text", it also writes <out>.words.json from qwen3_worker.align (MMS_FA).
The reference is only ever one of OUR OWN designed clips, never a real person's audio.

usage: <ming venv>/bin/python -I pipeline/audio/ming_worker.py jobs.json
"""
import json
import os
import sys
import time

os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["HF_HUB_OFFLINE"] = "1"
HERE = os.path.dirname(os.path.abspath(__file__))


def main(path):
    spec = json.load(open(path))
    src = os.path.expanduser(spec["src"])
    sys.path.insert(0, src)
    sys.path.append(HERE)  # after the model code: only qwen3_worker (the aligner) is taken from here
    os.chdir(src)
    import numpy as np
    import soundfile as sf
    import torch
    from ming_tts import MingTTS
    from qwen3_worker import align

    torch.set_num_threads(int(spec.get("threads", 6)))
    t0 = time.time()
    m = MingTTS(os.path.expanduser(spec["model"]), device="cpu", text_normalization=False)
    spk = m.spkemb_extractor

    class _NoCast:  # the ONNX speaker encoder needs float32 features: run it outside autocast
        def __getattr__(self, k):
            return getattr(spk, k)

        def __call__(self, *a, **k):
            with torch.autocast(device_type="cpu", enabled=False):
                return spk(*[x.float() if torch.is_tensor(x) else x for x in a], **k)

    m.spkemb_extractor = _NoCast()
    print(f"[ming] loaded {os.path.basename(spec['model'].rstrip('/'))} on cpu in {time.time() - t0:.1f}s", flush=True)
    for job in spec["jobs"]:
        if os.path.exists(job["out"]) and not job.get("force"):
            continue
        torch.manual_seed(int(job.get("seed", 11)))
        np.random.seed(int(job.get("seed", 11)))
        t1 = time.time()
        with torch.autocast(device_type="cpu", dtype=torch.bfloat16):  # the model code assumes CUDA autocast
            wav = m.synthesize(task="TTS", text=job["text"], language_id="English", prompt_wav_path=spec["ref_audio"],
                               prompt_text=spec["ref_text"], use_spk_emb=True, instruction=spec.get("instruction"))
        a = wav.detach().float().cpu().numpy().reshape(-1).astype(np.float32)
        sr = m.sample_rate
        os.makedirs(os.path.dirname(job["out"]) or ".", exist_ok=True)
        sf.write(job["out"], a, sr)
        if job.get("align_text"):
            json.dump(align(a, sr, job["align_text"]), open(job["out"][:-4] + ".words.json", "w"))
        el = time.time() - t1
        print(f"[ming] {os.path.basename(job['out'])}: {len(a) / sr:.2f}s audio in {el:.1f}s "
              f"(rtf {el / max(1e-3, len(a) / sr):.2f})", flush=True)


if __name__ == "__main__":
    main(sys.argv[1])
