"""`tts: ming`: Ming-3.0-tts-0.5b cloning our own designed ember voice, the story-lane narrator (config.MING).

Gives synthesize() what Kokoro and qwen3 give it: per chunk, (audio float32, sample rate, [(word, start, end)]).
- Chunks are synthesize()'s own plan (paragraphs, split again at [pause] markers), so one take never runs long enough
  to drift; Ming also splits each chunk into short fragments internally. Every chunk and fragment is conditioned on the
  same reference clip, transcript, instruction and seed, so the voice stays the same across the narration.
- Runs in its own venv on the CPU through ming_worker.py; all chunks go to one worker call, so the model loads once.
- Word timings: the worker's CTC forced alignment of the script words (qwen3_worker.align, torchaudio MMS_FA).
- `melody: rules` still applies after it in synthesize() (the script's stress / unstress, hook_boost, hook_act_st).
"""
from __future__ import annotations

import json
import os
import subprocess
import tempfile

import numpy as np

from .config import MING

HERE = os.path.dirname(os.path.abspath(__file__))


def render_many(texts: list[str], cfg: dict, meta: dict | None = None, log=print):
    """-> [(audio float32, sr, [(word, start, end)])] for each chunk text, in order."""
    py = os.path.expanduser(os.environ.get("MING_TTS_PYTHON", MING["python"]))
    if not os.path.exists(py):
        raise SystemExit(f"ming: no Ming venv at {py} (pipeline/audio/README.md, 'Ming-3.0-tts backend')")
    seed = int(cfg.get("ming_seed", MING["seed"]))
    with tempfile.TemporaryDirectory() as d:
        jobs = [{"text": t, "align_text": t, "seed": seed, "out": os.path.join(d, f"c{k:03d}.wav")}
                for k, t in enumerate(texts)]
        spec = {"src": os.environ.get("MING_TTS_SRC", MING["src"]),
                "model": os.environ.get("MING_TTS_MODEL", MING["model"]),
                "ref_audio": os.path.join(HERE, MING["ref_audio"]), "ref_text": MING["ref_text"],
                "instruction": cfg.get("ming_instruction") or MING["instruction"],
                "threads": int(os.environ.get("TTS_THREADS", MING["threads"])), "jobs": jobs}
        jf = os.path.join(d, "jobs.json")
        json.dump(spec, open(jf, "w"))
        log(f"[tts] ming voice ember (clone), {len(texts)} chunks, cpu")
        env = {**os.environ, "CUDA_VISIBLE_DEVICES": "", "HF_HUB_OFFLINE": "1"}
        subprocess.run(["nice", "-n", "10", py, "-I", os.path.join(HERE, "ming_worker.py"), jf], check=True, env=env)
        import soundfile as sf
        out = []
        for job in jobs:
            a, sr = sf.read(job["out"], dtype="float32")
            words = [(w, s, e) for w, s, e in json.load(open(job["out"][:-4] + ".words.json"))]
            out.append((a.astype(np.float32), sr, words))
        return out
