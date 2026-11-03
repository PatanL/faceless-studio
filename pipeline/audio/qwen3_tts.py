"""TTS engines that run outside the pipeline env: `qwen3` (local Qwen3-TTS) and `qwen_api` (hosted, not wired yet).

Both give synthesize() what Kokoro gives it: per chunk, (audio float32, sample rate, [(word, start, end)]), so the
word timings, captions, SFX markers and mix work unchanged.

qwen3 (research/music/VOICE_CADENCE.md, out/rnd-voice/):
- Our ORIGINAL narrator voices: each was designed once from a text description (Qwen3-TTS VoiceDesign), and that
  designed clip is reused as the Base model's voice prompt, so a voice stays the same across chunks and episodes
  (QWEN3_VOICES in config.py; the clips are in pipeline/audio/voices/). No real person's audio is ever a prompt.
- `emphasis: on` (default off) marks the stressed words from rules (pipeline/audio/emphasis.py) and sends them in
  capitals; the captions keep the script's own words. Capitals raise the marked words (+3.4 to +3.9 st against +1.0 to
  +1.6 plain on the Myeongnyang hook) but sometimes make the model spell or bend a word (WROTE as letters, LAUGHING
  heard as "lacking", JAPAN'S, YI, VASA), so it stays off until a safer control exists.
- Runs in its own venv (QWEN3["python"], default ~/faceless-work/venvs/qwen3tts) through qwen3_worker.py, MPS on the
  Mac or CPU. CUDA is refused. All chunks of a script go to one worker call, so the model loads once.
- Word timings come from the worker's CTC forced alignment of the script words (torchaudio MMS_FA), coverage ~1.0.
"""
from __future__ import annotations

import json
import os
import subprocess
import tempfile

import numpy as np

from . import emphasis as E
from .config import QWEN3, QWEN3_VOICES

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINES = ("qwen3", "qwen_api")


def _list(v):
    if not v:
        return []
    if isinstance(v, (list, tuple)):
        return list(v)
    return [x.strip() for x in str(v).split(",") if x.strip()]


def _on(v, default=False):
    if v is None or v == "":
        return default
    return str(v).strip().lower() in ("1", "on", "true", "yes", "y")


def plan_texts(texts: list[str], cfg: dict, meta: dict | None = None) -> list[str]:
    """The texts the TTS reads, one per chunk: the script text, with stressed words in capitals when emphasis is on.
    Marks are made on the whole narration at once (the hook rules belong to its first sentence and the payoff to its
    last word, not to every paragraph), then split back into the chunks."""
    meta = meta or {}
    if not _on(cfg.get("emphasis"), False):
        return list(texts)
    full = " ".join(texts)
    marks = E.mark(full, force=_list(meta.get("stress")), veto=_list(meta.get("unstress")))
    out, base = [], 0
    for t in texts:
        n = len(t.split())
        local = [E.Mark(m.index - base, m.word, m.reason) for m in marks if base <= m.index < base + n]
        out.append(E.markup(t, local))
        base += n
    return out


def render_many(texts: list[str], cfg: dict, meta: dict | None = None, log=print):
    """-> [(audio float32, sr, [(word, start, end)])] for each chunk text, in order."""
    engine = cfg["engine"]
    if engine == "qwen_api":
        return _qwen_api(texts, cfg, meta, log)
    name = cfg.get("qwen3_voice") or (cfg.get("voice") if cfg.get("voice") in QWEN3_VOICES else QWEN3["default_voice"])
    if name not in QWEN3_VOICES:
        raise SystemExit(f"qwen3: unknown voice {name!r}; voices: {sorted(QWEN3_VOICES)}")
    v = QWEN3_VOICES[name]
    py = os.path.expanduser(os.environ.get("QWEN3_TTS_PYTHON", QWEN3["python"]))
    models = os.path.expanduser(os.environ.get("QWEN3_TTS_MODELS", QWEN3["models"]))
    if not os.path.exists(py):
        raise SystemExit(f"qwen3: no Qwen3-TTS venv at {py} (pipeline/audio/README.md, 'Qwen3-TTS backend')")
    seed = int(cfg.get("qwen3_seed", v.get("seed", 11)))
    with tempfile.TemporaryDirectory() as d:
        jobs = []
        for k, (t, said) in enumerate(zip(texts, plan_texts(texts, cfg, meta))):
            job = {"text": said, "seed": seed + k, "out": os.path.join(d, f"c{k:03d}.wav"),
                   "language": "English", "align_text": t,
                   # 12 codec frames/s; cap at ~2 words/s + 4 s so a runaway take cannot run for minutes
                   "max_new_tokens": int(12 * (len(t.split()) / 2.0 + 4))}
            job.update({"ref_audio": os.path.join(HERE, v["ref_audio"]), "ref_text": v["ref_text"]})
            jobs.append(job)
        spec = {"model_dir": os.path.join(models, QWEN3["base_model"]), "dtype": QWEN3.get("dtype", "bf16"),
                "jobs": jobs}
        jf = os.path.join(d, "jobs.json")
        json.dump(spec, open(jf, "w"))
        env = {**os.environ, "CUDA_VISIBLE_DEVICES": "", "HF_HUB_OFFLINE": "1"}
        log(f"[tts] qwen3 voice {name}, emphasis {'on' if _on(cfg.get('emphasis'), False) else 'off'}, "
            f"{len(texts)} chunks")
        subprocess.run([py, "-I", os.path.join(HERE, "qwen3_worker.py"), jf], check=True, env=env)
        import soundfile as sf
        out = []
        for job in jobs:
            a, sr = sf.read(job["out"], dtype="float32")
            words = [(w, s, e) for w, s, e in json.load(open(job["out"][:-4] + ".words.json"))]
            out.append((a.astype(np.float32), sr, words))
        return out


def _qwen_api(texts, cfg, meta, log):
    """Hosted Qwen TTS on Alibaba Cloud Model Studio (DashScope). Not wired: there is no key yet, and spending money
    is the owner's call. What it needs is in pipeline/audio/README.md ('Hosted engine: qwen_api'). When a key exists
    this function posts each chunk (plan_texts + an instruction from emphasis.instruct_for), downloads the audio, and
    gets word timings by forced alignment, the same as qwen3 (qwen3_worker.align)."""
    key = os.environ.get("DASHSCOPE_API_KEY")
    if not key:
        env_file = os.path.expanduser("~/studio/.env")
        if os.path.exists(env_file):
            for line in open(env_file):
                if line.startswith("DASHSCOPE_API_KEY="):
                    key = line.split("=", 1)[1].strip().strip("'\"")
    if not key:
        raise SystemExit("qwen_api: DASHSCOPE_API_KEY is not set (env or ~/studio/.env); the hosted engine stays off "
                         "until the owner adds a key")
    raise SystemExit("qwen_api: a key is present but the client is not implemented yet "
                     "(pipeline/audio/README.md, 'Hosted engine: qwen_api')")
