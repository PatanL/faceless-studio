"""Secrets from ~/studio/.env (docs/OPERATOR_DESIGN.md 4.5).

KEY=VALUE lines, `#` comments, optional surrounding quotes, no `export`, no shell evaluation. A missing file gives
{}. Callers that lack a variable switch to --dry-run and print `DRY-RUN: missing <NAMES> in ~/studio/.env`.
Never print a value; pass anything you log through redact().
"""
from __future__ import annotations

import os

DEFAULT_PATH = "~/studio/.env"
_loaded: dict[str, str] = {}


def _path(path: str | None) -> str:
    return os.path.expanduser(path or os.environ.get("STUDIO_ENV_FILE") or DEFAULT_PATH)


def load_env(path: str | None = None) -> dict[str, str]:
    p = _path(path)
    out: dict[str, str] = {}
    try:
        with open(p, encoding="utf-8") as f:
            lines = f.read().splitlines()
    except (FileNotFoundError, PermissionError, IsADirectoryError):
        return {}
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        if k.startswith("export "):  # tolerated but not required
            k = k[len("export "):].strip()
        if not k.replace("_", "").isalnum():
            continue
        v = v.strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
            v = v[1:-1]
        elif " #" in v:  # trailing comment on an unquoted value
            v = v.split(" #", 1)[0].rstrip()
        out[k] = v
    _loaded.update({k: v for k, v in out.items() if v})
    return out


def require(names: list[str], path: str | None = None) -> tuple[dict[str, str], list[str]]:
    """(values for the names that are set and non-empty, missing names)."""
    env = load_env(path)
    vals = {n: env[n] for n in names if env.get(n)}
    return vals, [n for n in names if n not in vals]


def dry_run_notice(missing: list[str]) -> str:
    return f"DRY-RUN: missing {','.join(missing)} in {DEFAULT_PATH}"


def redact(s: str) -> str:
    """Replace every loaded secret value (length >= 4) in s with ***."""
    if not s:
        return s
    for v in sorted(set(_loaded.values()), key=len, reverse=True):
        if len(v) >= 4:
            s = s.replace(v, "***")
    return s
