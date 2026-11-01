#!/usr/bin/env python3
"""Measure every narration paragraph of script.md with the real voice (Kokoro, CPU only) -> durations.json.

Run on the Spark only (BRIEF: TTS never on the Mac), from ~/studio/app:
  CUDA_VISIBLE_DEVICES="" OMP_NUM_THREADS=4 TTS_THREADS=4 nice -n 10 \
    ~/studio/.venv/bin/python backlog/explainer/explainer-sinking-every-1000m/measure_tts.py [speed]

Reads the ```narration``` block of script.md (one paragraph = one scene, [..] markers stripped) and the
front-matter `speed` (default 0.86). Output: durations.json next to this file:
  {"speed": s, "voice": v, "paras": [{"i": n, "text": ..., "dur": speech s, "words": [[w, start, end], ...]}]}
Word times are relative to the paragraph's first word; dur = last word end + 0.08 s.
gen_storyboard.py uses these timings when the file exists (else a wpm estimate).
"""
import json
import os
import re
import sys
import time

os.environ["CUDA_VISIBLE_DEVICES"] = ""
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("STUDIO_ROOT") or os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, ROOT)
from pipeline.audio.tts import _kokoro  # noqa: E402

SCRIPT = os.environ.get("SCRIPT_MD") or os.path.join(HERE, "script.md")
OUT = os.environ.get("OUT_JSON") or os.path.join(HERE, "durations.json")
src = open(SCRIPT, encoding="utf-8").read()
fm = re.search(r"^---\n(.*?)\n---", src, re.S).group(1)
m = re.search(r"^speed:\s*([0-9.]+)", fm, re.M)
speed = float(sys.argv[1]) if len(sys.argv) > 1 else (float(m.group(1)) if m else 0.86)
block = re.search(r"```narration\n(.*?)```", src, re.S).group(1)
paras = [re.sub(r"\s+", " ", re.sub(r"\[[^\]]*\]", " ", p)).strip() for p in re.split(r"\n\s*\n", block)]
paras = [p for p in paras if p]
out = {"speed": speed, "voice": "am_michael", "paras": []}
t0 = time.time()
for i, text in enumerate(paras, 1):
    audio, sr, words = _kokoro(text, "am_michael", "a", speed)
    words = [(w, s, e) for w, s, e in words if s is not None and e is not None]
    s0 = words[0][1] if words else 0.0
    rel = [[w, round(s - s0, 3), round(e - s0, 3)] for w, s, e in words]
    dur = (rel[-1][2] + 0.08) if rel else len(audio) / sr
    out["paras"].append({"i": i, "text": text, "dur": round(dur, 3), "audio_s": round(len(audio) / sr, 3), "words": rel})
    print(f"{i:02d} {dur:6.2f}s {len(text.split()):3d}w  {text[:60]}", flush=True)
json.dump(out, open(OUT, "w"), indent=1)
tot = sum(p["dur"] for p in out["paras"])
nw = sum(len(p["text"].split()) for p in out["paras"])
print(f"done {len(paras)} paragraphs, speech {tot:.1f}s, {nw} words, {nw / tot * 60:.0f} wpm, in {time.time() - t0:.0f}s")
