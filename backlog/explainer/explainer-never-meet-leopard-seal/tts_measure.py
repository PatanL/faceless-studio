#!/usr/bin/env python3
"""Measure every VO line of explainer-never-meet-leopard-seal with Kokoro on the Spark CPU.

usage (Spark only):
  CUDA_VISIBLE_DEVICES="" OMP_NUM_THREADS=4 nice -n 10 ~/studio/.venv/bin/python tts_measure.py lines.json tts_durations.json
lines.json: [{"id", "text", "speed"}]  ->  {"voice", "lines": {id: {"dur", "speed", "words": [{"w", "s", "e"}]}}}
Line audio is not kept (durations and word timings only); the real mix is built later by pipeline.audio.make.
"""
import json
import os
import sys
import time

os.environ["CUDA_VISIBLE_DEVICES"] = ""
import numpy as np  # noqa: E402
import torch  # noqa: E402

torch.set_num_threads(4)
from kokoro import KPipeline  # noqa: E402

VOICE = os.environ.get("VOICE", "am_michael")
src, dst = sys.argv[1], sys.argv[2]
lines = json.load(open(src))
pipe = KPipeline(lang_code="a", device="cpu")
out = {"voice": VOICE, "engine": "kokoro-82M cpu", "lines": {}}
t0 = time.time()
for ln in lines:
    chunks, words, off = [], [], 0.0
    for r in pipe(ln["text"], voice=VOICE, speed=ln["speed"], split_pattern=None):
        a = r.audio.numpy() if hasattr(r.audio, "numpy") else np.asarray(r.audio)
        for tok in (r.tokens or []):
            if tok.start_ts is not None and tok.end_ts is not None and tok.text.strip():
                words.append({"w": tok.text, "s": round(off + tok.start_ts, 3), "e": round(off + tok.end_ts, 3)})
        chunks.append(a)
        off += len(a) / 24000
    wav = np.concatenate(chunks)
    # trim trailing/leading near-silence so gaps are controlled by the timeline, not the model
    amp = np.abs(wav)
    nz = np.where(amp > 0.01)[0]
    lead = nz[0] / 24000 if len(nz) else 0.0
    tail = (len(wav) - nz[-1]) / 24000 if len(nz) else 0.0
    dur = len(wav) / 24000 - lead - tail
    out["lines"][ln["id"]] = {"dur": round(dur, 3), "speed": ln["speed"], "lead": round(lead, 3),
                              "words": [{**w, "s": round(w["s"] - lead, 3), "e": round(w["e"] - lead, 3)} for w in words]}
    print(ln["id"], round(dur, 2), flush=True)
out["synth_s"] = round(time.time() - t0, 1)
json.dump(out, open(dst, "w"), indent=1)
