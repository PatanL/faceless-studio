"""Append-only JSONL ledgers (docs/OPERATOR_DESIGN.md 4.3).

Every row gets "v": 1 and "at" (UTC ISO) if missing. Appends hold an flock on `<file>.lock`, write one line and
fsync. Readers take the latest row per key. Nobody rewrites a ledger in place.
"""
from __future__ import annotations

import json
import os
import sys

from . import locks, timeutil


def append(path: str, row: dict) -> None:
    row = dict(row)
    row.setdefault("v", 1)
    row.setdefault("at", timeutil.iso())
    line = json.dumps(row, ensure_ascii=False, separators=(",", ":"), sort_keys=False)
    if "\n" in line:  # json.dumps never emits raw newlines, but keep the invariant explicit
        raise ValueError("row serialises to more than one line")
    d = os.path.dirname(os.path.abspath(path))
    os.makedirs(d, exist_ok=True)
    with locks.flock(os.path.abspath(path) + ".lock", timeout_s=60):
        with open(path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
            f.flush()
            os.fsync(f.fileno())


def read(path: str) -> list[dict]:
    """All rows; [] if the file is missing. A bad line is skipped and reported on stderr."""
    if not os.path.exists(path):
        return []
    rows = []
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"[jsonl] {path}:{n}: skipped bad line ({e})", file=sys.stderr)
                continue
            if isinstance(obj, dict):
                rows.append(obj)
            else:
                print(f"[jsonl] {path}:{n}: skipped non-object line", file=sys.stderr)
    return rows


def latest(path: str, key: str) -> dict[str, dict]:
    """Last row per row[key] (rows without the key are ignored). Insertion order = first appearance."""
    out: dict[str, dict] = {}
    for row in read(path):
        k = row.get(key)
        if k is None:
            continue
        out[str(k)] = row
    return out
