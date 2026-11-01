"""Measure every spoken line of horror-elevator-maintenance-chat with Kokoro on the Spark CPU (multi-voice).

usage (Spark only, from this folder):
  CUDA_VISIBLE_DEVICES="" OMP_NUM_THREADS=4 nice -n 10 ~/studio/.venv/bin/python tts_measure.py tts_durations.json [wav_dir]
Reads lines.py (VOICES + V). Writes {"lines": {id: {"voice","speed","dur","lead","words":[{w,s,e}]}}}.
Line wavs (trimmed) are kept on the Spark only when wav_dir is given.
"""
import json
import os
import sys
import time

os.environ["CUDA_VISIBLE_DEVICES"] = ""
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402
import torch  # noqa: E402

torch.set_num_threads(3)
from kokoro import KPipeline  # noqa: E402

import lines as L  # noqa: E402

dst = sys.argv[1]
wav_dir = sys.argv[2] if len(sys.argv) > 2 else None
pipes = {}
out = {"engine": "kokoro-82M cpu", "voices": L.VOICES, "lines": {}}
t0 = time.time()
for e in L.spoken():
    lid, spk, text, opts = e
    voice, speed = L.VOICES[spk]
    speed = opts.get("speed", speed)
    lang = voice[0]
    if lang not in pipes:
        pipes[lang] = KPipeline(lang_code=lang, device="cpu")
    say = opts.get("say", text)
    chunks, words, off = [], [], 0.0
    for r in pipes[lang](say, voice=voice, speed=speed, split_pattern=None):
        a = r.audio.numpy() if hasattr(r.audio, "numpy") else np.asarray(r.audio)
        for tok in (r.tokens or []):
            if tok.start_ts is not None and tok.end_ts is not None and tok.text.strip():
                words.append({"w": tok.text, "s": round(off + tok.start_ts, 3), "e": round(off + tok.end_ts, 3)})
        chunks.append(a)
        off += len(a) / 24000
    wav = np.concatenate(chunks)
    amp = np.abs(wav)
    nz = np.where(amp > 0.01)[0]
    lead = nz[0] / 24000 if len(nz) else 0.0
    tail = (len(wav) - nz[-1]) / 24000 if len(nz) else 0.0
    dur = len(wav) / 24000 - lead - tail
    if wav_dir:
        import wave
        os.makedirs(wav_dir, exist_ok=True)
        seg = wav[int(lead * 24000): len(wav) - int(tail * 24000)]
        with wave.open(os.path.join(wav_dir, f"{lid}.wav"), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(24000)
            w.writeframes((np.clip(seg, -1, 1) * 32767).astype("<i2").tobytes())
    out["lines"][lid] = {"voice": voice, "speed": speed, "dur": round(dur, 3), "lead": round(lead, 3),
                         "words": [{**w, "s": round(w["s"] - lead, 3), "e": round(w["e"] - lead, 3)} for w in words]}
    print(lid, voice, speed, round(dur, 2), flush=True)
out["synth_s"] = round(time.time() - t0, 1)
json.dump(out, open(dst, "w"), indent=1)
