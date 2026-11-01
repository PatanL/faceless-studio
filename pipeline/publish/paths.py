"""Where L3 reads and writes (docs/OPERATOR_DESIGN.md 4.2, 5.5-5.10).

ROOT is the repo root (Mac) or ~/studio/app (Spark). DATA is ROOT/data unless STUDIO_DATA_DIR is set (tests and
off-ledger proofs use that so they never touch the real ledger).
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

ROOT = Path(os.environ.get("STUDIO_ROOT") or Path(__file__).resolve().parents[2])


def data_dir() -> Path:
    return Path(os.environ.get("STUDIO_DATA_DIR") or os.environ.get("STUDIO_DATA") or ROOT / "data")


def posts_ledger() -> Path:
    return data_dir() / "posts.jsonl"


def schema_file() -> Path:
    return data_dir() / "buffer_schema.json"


def config_file() -> Path:
    return data_dir() / "operator" / "config.json"


def load_config() -> dict:
    """data/operator/config.json over pipeline/ops/config.default.json (shallow merge per top-level key)."""
    cfg: dict = {}
    default = ROOT / "pipeline" / "ops" / "config.default.json"
    for p in (default, config_file()):
        if p.exists():
            with open(p, encoding="utf-8") as f:
                cfg.update(json.load(f))
    return cfg


def episode_dir(slug: str) -> Path:
    return ROOT / "episodes" / slug


def out_dir(slug: str) -> Path:
    return ROOT / "out" / slug


def pilot_dir(slug: str) -> Path:
    return ROOT / "out" / "pilots" / slug


def qa_dir(slug: str) -> Path:
    return out_dir(slug) / "qa"


def publish_dir(slug: str) -> Path:
    return out_dir(slug) / "publish"


def first_existing(*paths: Path) -> Path | None:
    for p in paths:
        if p and p.exists():
            return p
    return None


def read_json(p: Path | None) -> dict | None:
    if not p or not p.exists():
        return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def find_mp4(slug: str) -> Path | None:
    """make_status.outputs.mp4, then out/<slug>/<slug>_9x16.mp4, then the pilot location."""
    st = read_json(episode_dir(slug) / "make_status.json") or {}
    rel = (st.get("outputs") or {}).get("mp4")
    cands = [ROOT / rel] if rel else []
    cands += [out_dir(slug) / f"{slug}_9x16.mp4", pilot_dir(slug) / f"{slug}_9x16.mp4"]
    return first_existing(*cands)


def sha256_file(p: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()
