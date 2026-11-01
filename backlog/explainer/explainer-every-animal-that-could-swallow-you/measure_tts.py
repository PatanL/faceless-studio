#!/usr/bin/env python3
"""Measure every VO line with the real TTS voice (Kokoro, CPU only) -> durations.json.

Run on the Spark only (BRIEF: TTS never on the Mac), from ~/studio/app:
  CUDA_VISIBLE_DEVICES="" OMP_NUM_THREADS=4 TTS_THREADS=4 nice -n 10 \
    ~/studio/.venv/bin/python backlog/explainer/explainer-every-animal-that-could-swallow-you/measure_tts.py

Output: durations.json next to this file: {id: {"dur": speech seconds, "words": [[text, start, end], ...]}}
(word times relative to the first word of the line; dur = last word end + 0.08 s).
"""
import json
import os
import sys
import time

os.environ["CUDA_VISIBLE_DEVICES"] = ""
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, ROOT)
from pipeline.audio.tts import _kokoro  # noqa: E402

spec = json.load(open(os.path.join(HERE, "vo_lines.json")))
v = spec["voice"]
out = {}
t0 = time.time()
for ln in spec["lines"]:
    audio, sr, words = _kokoro(ln["text"], v["voice"], v["lang"], v["speed"])
    words = [(w, s, e) for w, s, e in words if s is not None and e is not None]
    s0 = words[0][1] if words else 0.0
    rel = [[w, round(s - s0, 3), round(e - s0, 3)] for w, s, e in words]
    dur = (rel[-1][2] + 0.08) if rel else len(audio) / sr
    out[ln["id"]] = {"dur": round(dur, 3), "audio_s": round(len(audio) / sr, 3), "words": rel}
    print(f"{ln['id']:4} {dur:6.2f}s  {ln['text'][:60]}", flush=True)
json.dump(out, open(os.path.join(HERE, "durations.json"), "w"), indent=1)
print(f"done {len(out)} lines in {time.time() - t0:.0f}s")
