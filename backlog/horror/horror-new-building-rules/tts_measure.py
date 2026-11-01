"""Measure every spoken line of horror-new-building-rules with Kokoro-82M on the Spark CPU.

usage (Spark only, from this folder):
  CUDA_VISIBLE_DEVICES="" OMP_NUM_THREADS=4 nice -n 10 ~/studio/.venv/bin/python tts_measure.py tts_durations.json [wav_dir]
Reads lines.py. Writes {"lines": {id: {"part","text","say","voice","speed","dur","lead","phonemes","words":[{w,s,e}]}}}.
Trimmed line wavs are written to wav_dir (Spark only) when it is given; build.py --voice joins them into
one voice track per part, laid out on the measured timeline.
"""
import json
import os
import sys
import time

os.environ["CUDA_VISIBLE_DEVICES"] = ""
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402
import torch  # noqa: E402

torch.set_num_threads(4)
from kokoro import KPipeline  # noqa: E402

import lines as L  # noqa: E402

SR = 24000
dst = sys.argv[1]
wav_dir = sys.argv[2] if len(sys.argv) > 2 else None
pipe = KPipeline(lang_code=L.VOICE[0], device="cpu")
out = {"engine": "kokoro-82M cpu", "voice": L.VOICE, "lines": {}}
t0 = time.time()
for part, lid, text, say, speed in L.spoken():
    chunks, words, phon, off = [], [], [], 0.0
    for r in pipe(say, voice=L.VOICE, speed=speed, split_pattern=None):
        a = r.audio.numpy() if hasattr(r.audio, "numpy") else np.asarray(r.audio)
        for tok in (r.tokens or []):
            if tok.text.strip():
                phon.append([tok.text, tok.phonemes])
            if tok.start_ts is not None and tok.end_ts is not None and tok.text.strip():
                words.append({"w": tok.text, "s": round(off + tok.start_ts, 3), "e": round(off + tok.end_ts, 3)})
        chunks.append(a)
        off += len(a) / SR
    wav = np.concatenate(chunks)
    amp = np.abs(wav)
    nz = np.where(amp > 0.01)[0]
    lead = nz[0] / SR if len(nz) else 0.0
    tail = (len(wav) - nz[-1]) / SR if len(nz) else 0.0
    dur = len(wav) / SR - lead - tail
    if wav_dir:
        import wave
        os.makedirs(wav_dir, exist_ok=True)
        seg = wav[int(lead * SR): len(wav) - int(tail * SR)]
        with wave.open(os.path.join(wav_dir, f"{lid}.wav"), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((np.clip(seg, -1, 1) * 32767).astype("<i2").tobytes())
    out["lines"][lid] = {"part": part, "text": text, "say": say, "voice": L.VOICE, "speed": speed,
                         "dur": round(dur, 3), "lead": round(lead, 3), "phonemes": phon,
                         "words": [{**w, "s": round(w["s"] - lead, 3), "e": round(w["e"] - lead, 3)} for w in words]}
    print(part, lid, speed, round(dur, 2), flush=True)
out["synth_s"] = round(time.time() - t0, 1)
json.dump(out, open(dst, "w"), indent=1)
