"""Shared helpers for pipeline/qa (paths, episode files, ffmpeg, JSON/JSONL, script text).

Stdlib only. numpy is needed only by frames.py and sheet.py.
"""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone

REPO = pathlib.Path(__file__).resolve().parents[2]

# --------------------------------------------------------------------------- root and paths


def root(arg: str | None = None) -> pathlib.Path:
    """Working root: --root, else $STUDIO_ROOT, else the repo this file lives in."""
    return pathlib.Path(arg or os.environ.get("STUDIO_ROOT") or REPO).expanduser().resolve()


def qa_dir(r: pathlib.Path, slug: str) -> pathlib.Path:
    return r / "out" / slug / "qa"


def first(*paths) -> pathlib.Path | None:
    for p in paths:
        if p and pathlib.Path(p).is_file():
            return pathlib.Path(p)
    return None


def find_mp4(r: pathlib.Path, slug: str) -> pathlib.Path | None:
    """The 9:16 master: make_status outputs.mp4, out/<slug>/, then out/pilots/<slug>/."""
    ms = read_json(r / "episodes" / slug / "make_status.json") or {}
    mp4 = (ms.get("outputs") or {}).get("mp4")
    return first(r / mp4 if mp4 else None,
                 r / "out" / slug / f"{slug}_9x16.mp4",
                 r / "out" / "pilots" / slug / f"{slug}_9x16.mp4",
                 r / "out" / slug / f"{slug}.mp4")


def package_dirs(r: pathlib.Path, slug: str) -> list[pathlib.Path]:
    """Where titles.md / description.md / thumbs/ may live (operator episodes, then pilots)."""
    return [r / "episodes" / slug, r / "out" / slug, r / "out" / "pilots" / slug]


def episode_file(r: pathlib.Path, slug: str, name: str) -> pathlib.Path | None:
    return first(*[d / name for d in package_dirs(r, slug)])


def rel(r: pathlib.Path, p) -> str | None:
    if p is None:
        return None
    p = pathlib.Path(p)
    try:
        return str(p.resolve().relative_to(pathlib.Path(r).resolve()))
    except ValueError:
        return str(p)


def refs_dir() -> pathlib.Path:
    return pathlib.Path(os.environ.get("STUDIO_REFS", "~/studio/refs")).expanduser()


# --------------------------------------------------------------------------- json / jsonl


def read_json(p) -> dict | list | None:
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def write_json(p, obj) -> None:
    """Atomic write (.tmp + os.replace)."""
    p = pathlib.Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, p)


def read_jsonl(p) -> list[dict]:
    """pipeline.common.jsonl.read when L5's library is present, else the same contract here."""
    try:
        from pipeline.common import jsonl  # type: ignore
        return jsonl.read(str(p))
    except Exception:
        pass
    rows = []
    try:
        with open(p, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except ValueError:
                    print(f"qa: skipped a bad line in {p}", file=sys.stderr)
    except OSError:
        return []
    return rows


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# --------------------------------------------------------------------------- operator config / rules

RULE_DEFAULTS = {"hook.max_words": 12, "visual.max_hold_s": 3.0, "pace.rehook_s": 9}


def rules(r: pathlib.Path) -> dict:
    """data/learned/rules.json defaults (L4) over the design defaults."""
    out = dict(RULE_DEFAULTS)
    d = read_json(r / "data" / "learned" / "rules.json") or {}
    out.update({k: v for k, v in (d.get("defaults") or {}).items() if v is not None})
    return out


def last_n_default(r: pathlib.Path) -> int:
    cfg = read_json(r / "data" / "operator" / "config.json") or {}
    try:
        return int((cfg.get("sameness") or {}).get("last_n", 10))
    except (TypeError, ValueError):
        return 10


# --------------------------------------------------------------------------- process helpers


def be_nice() -> None:
    """BRIEF: batch work on the Spark runs at nice 10, CPU only."""
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    try:
        if os.getpriority(os.PRIO_PROCESS, 0) < 10:
            os.setpriority(os.PRIO_PROCESS, 0, 10)
    except (AttributeError, OSError):
        pass


def tool(name: str) -> str:
    """ffmpeg / ffprobe: $FFMPEG-style env override, ~/studio/bin (Spark static build), then PATH."""
    env = os.environ.get(name.upper())
    if env:
        return env
    local = pathlib.Path("~/studio/bin").expanduser() / name
    if local.is_file():
        return str(local)
    found = shutil.which(name)
    if not found:
        raise RuntimeError(f"{name} not found (set ${name.upper()} or install it in ~/studio/bin)")
    return found


def run(cmd: list[str], *, binary=False, timeout=900) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=not binary, timeout=timeout)


def probe_duration(mp4) -> float:
    p = run([tool("ffprobe"), "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp4)])
    try:
        return float(p.stdout.strip())
    except ValueError:
        raise RuntimeError(f"ffprobe could not read {mp4}: {p.stderr.strip()[:200]}")


def probe_size(path) -> tuple[int, int]:
    p = run([tool("ffprobe"), "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
             "-of", "csv=p=0", str(path)])
    w, h = (int(x) for x in p.stdout.strip().split(",")[:2])
    return w, h


# --------------------------------------------------------------------------- script text

FRONT = re.compile(r"\A---\n(.*?)\n---\n", re.S)
REF_LINE = re.compile(r"^\s*-\s*id:\s*([^,\s]+)", re.M)


def front_matter(text: str) -> dict:
    m = FRONT.match(text)
    out = {}
    if not m:
        return out
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t", "-")):
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    out["_references"] = REF_LINE.findall(m.group(1))
    return out


def narration_paragraphs(script_path) -> list[str]:
    """Spoken paragraphs as TTS will read them (pipeline.audio.script.parse)."""
    if str(REPO) not in sys.path:
        sys.path.insert(0, str(REPO))
    from pipeline.audio.script import parse
    return [s.text for s in parse(pathlib.Path(script_path).read_text(encoding="utf-8")).segments if s.text.strip()]


def first_sentence(text: str) -> str:
    m = re.match(r"(.+?[.!?])(\s|$)", text.strip())
    return (m.group(1) if m else text).strip()


def hook_text(paragraphs: list[str]) -> str:
    return first_sentence(paragraphs[0]) if paragraphs else ""


def originality_module():
    """scripts/originality_check.py as a module (same normalisation and thresholds as the gate CLI)."""
    import importlib.util
    path = REPO / "scripts" / "originality_check.py"
    spec = importlib.util.spec_from_file_location("originality_check", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


def slug_topic(slug: str) -> str:
    """op-YYYYMMDD-a-pistol-shrimp -> 'pistol shrimp'; explainer-blue-whale -> 'blue whale'."""
    m = re.match(r"^op-\d{8}-[ab]-(.+)$", slug)
    t = m.group(1) if m else re.sub(r"^(explainer|horror|whatif)-(short-)?", "", slug)
    return t.replace("-", " ").strip()
