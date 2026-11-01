"""Shared helpers for L4 (analytics + learning).

`pipeline/common/` (L5) is the one shared library (OPERATOR_DESIGN 4.4). Until L5's first commit lands, this module
falls back to minimal local copies with the same signatures, so L4 runs and tests on its own. When
`pipeline.common` exists it is always used.

Paths: ROOT is the repo root (`~/studio/app` on the Spark). DATA is `$STUDIO_DATA_DIR` if set (tests point it at a
temp dir), else `ROOT/data`.
"""
from __future__ import annotations

import contextlib
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def data_dir() -> str:
    return os.environ.get("STUDIO_DATA_DIR") or os.path.join(ROOT, "data")


def dpath(*parts: str) -> str:
    return os.path.join(data_dir(), *parts)


def rpath(*parts: str) -> str:
    return os.path.join(ROOT, *parts)


# ---------------------------------------------------------------- jsonl / env / time / locks (pipeline.common)
try:  # pragma: no cover - exercised once L5 lands pipeline/common
    from pipeline.common import jsonl as _jsonl  # type: ignore
    from pipeline.common import env as _env  # type: ignore
    from pipeline.common import timeutil as _tu  # type: ignore
    from pipeline.common import locks as _locks  # type: ignore

    jsonl_append, jsonl_read, jsonl_latest = _jsonl.append, _jsonl.read, _jsonl.latest
    load_env, require, redact = _env.load_env, _env.require, _env.redact
    TZ, now_utc, iso, parse, local_date = _tu.TZ, _tu.now_utc, _tu.iso, _tu.parse, _tu.local_date
    flock = _locks.flock
    COMMON = "pipeline.common"
except Exception:  # local fallback, same signatures as OPERATOR_DESIGN 4.4
    import fcntl

    COMMON = "pipeline.analytics._common (fallback)"
    TZ = ZoneInfo("America/Chicago")

    def now_utc() -> datetime:
        return datetime.now(timezone.utc)

    def iso(dt: datetime) -> str:
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def parse(s: str) -> datetime:
        s = s.strip()
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        dt = datetime.fromisoformat(s)
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)

    def local_date(dt: datetime | None = None) -> str:
        return (dt or now_utc()).astimezone(TZ).strftime("%Y-%m-%d")

    def jsonl_append(path: str, row: dict) -> None:
        row = dict(row)
        row.setdefault("v", 1)
        row.setdefault("at", iso(now_utc()))
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path + ".lock", "a") as lk:
            fcntl.flock(lk, fcntl.LOCK_EX)
            with open(path, "a", encoding="utf-8") as f:
                f.write(json.dumps(row, ensure_ascii=False, sort_keys=False) + "\n")
                f.flush()
                os.fsync(f.fileno())

    def jsonl_read(path: str) -> list[dict]:
        if not os.path.exists(path):
            return []
        out = []
        with open(path, encoding="utf-8") as f:
            for n, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    print(f"warn: {path}:{n}: bad JSON line skipped", file=sys.stderr)
        return out

    def jsonl_latest(path: str, key: str) -> dict[str, dict]:
        out: dict[str, dict] = {}
        for r in jsonl_read(path):
            k = r.get(key)
            if k is not None:
                out[str(k)] = r
        return out

    _SECRETS: set[str] = set()

    def load_env(path: str = "~/studio/.env") -> dict[str, str]:
        p = os.path.expanduser(os.environ.get("STUDIO_ENV_FILE", path))
        vals: dict[str, str] = {}
        if not os.path.exists(p):
            return vals
        with open(p, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k, v = k.strip(), v.strip()
                if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
                    v = v[1:-1]
                if re.fullmatch(r"[A-Z_][A-Z0-9_]*", k):
                    vals[k] = v
                    if len(v) >= 6:
                        _SECRETS.add(v)
        return vals

    def require(names: list[str]) -> tuple[dict, list[str]]:
        env = load_env()
        vals = {n: env[n] for n in names if env.get(n)}
        return vals, [n for n in names if n not in vals]

    def redact(s: str) -> str:
        for v in sorted(_SECRETS, key=len, reverse=True):
            s = s.replace(v, "***")
        return s

    @contextlib.contextmanager
    def flock(name: str, shared: bool = False, timeout_s: int = 1800):
        base = os.path.expanduser("~/studio/locks")
        if not os.path.isdir(base):
            base = os.path.join(tempfile.gettempdir(), "studio-locks")
            os.makedirs(base, exist_ok=True)
        import time

        with open(os.path.join(base, f"{name}.lock"), "a") as fh:
            mode = fcntl.LOCK_SH if shared else fcntl.LOCK_EX
            t_end = time.time() + timeout_s
            while True:
                try:
                    fcntl.flock(fh, mode | fcntl.LOCK_NB)
                    break
                except BlockingIOError:
                    if time.time() > t_end:
                        raise TimeoutError(f"lock {name} busy for {timeout_s}s")
                    time.sleep(1)
            try:
                yield
            finally:
                fcntl.flock(fh, fcntl.LOCK_UN)


# ---------------------------------------------------------------- small shared helpers
EXIT_OK, EXIT_FAIL, EXIT_USAGE, EXIT_BUDGET, EXIT_NOTHING, EXIT_DEP, EXIT_GATE = 0, 1, 2, 3, 4, 5, 6


class DependencyError(RuntimeError):
    """API 401/403, missing token file, network down: CLIs exit 5."""


def env_or_default(env: dict, name: str, default: str) -> str:
    return env.get(name) or os.environ.get(name) or default


def write_json_atomic(path: str, obj) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, path)


def read_json(path: str, default=None):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def median(xs: list[float]) -> float | None:
    xs = sorted(x for x in xs if x is not None)
    if not xs:
        return None
    n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


def is_real(row: dict) -> bool:
    """Ledger rows that count for learning / experiments / kill rule (no dry-run or synthetic data)."""
    return not row.get("dry_run") and row.get("status") != "dry_run" and row.get("source") != "synthetic"


def config() -> dict:
    """data/operator/config.json over pipeline/ops/config.default.json (both L5-owned; read only here)."""
    base = read_json(rpath("pipeline", "ops", "config.default.json"), {}) or {}
    over = read_json(dpath("operator", "config.json"), {}) or {}
    base.update(over)
    base.setdefault("metrics_windows_h", [48, 168])
    base.setdefault("kill_rule", {"after_videos": 30, "target_views_7d": 10000})
    return base


def window_label(hours: float) -> str:
    return {24: "24h", 48: "48h", 168: "7d", 672: "28d"}.get(int(hours), f"{int(hours)}h")


def window_hours(label: str) -> float:
    m = re.fullmatch(r"(\d+)([hd])", label)
    if not m:
        raise ValueError(f"bad window {label!r} (use 48h, 7d, 28d)")
    return int(m.group(1)) * (24 if m.group(2) == "d" else 1)
