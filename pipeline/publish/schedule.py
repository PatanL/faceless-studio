"""Slot datetimes from data/operator/config.json (OPERATOR_DESIGN 8.1; used by L5 to pass --slot-at).

    python -m pipeline.publish.schedule next --date YYYY-MM-DD [--slot a|b]

Prints JSON: [{"slot": "a", "date": ..., "post_at_local": "11:30", "post_at": "<UTC ISO Z>"}, ...] using
America/Chicago (config.tz), DST-aware.
"""
from __future__ import annotations

import argparse
import json
import sys
from zoneinfo import ZoneInfo

from pipeline.common import timeutil

from . import paths


def slots(date: str, cfg: dict | None = None, slot: str | None = None) -> list[dict]:
    cfg = cfg or paths.load_config()
    tz = ZoneInfo(cfg.get("tz") or "America/Chicago")
    out = []
    for s in cfg.get("slots") or []:
        if slot and s["slot"] != slot:
            continue
        out.append({"slot": s["slot"], "date": date, "post_at_local": s["post_at"],
                    "post_at": timeutil.iso(timeutil.at_local(date, s["post_at"], tz))})
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.publish.schedule")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("next")
    p.add_argument("--date", default=None, help="local date, default today (America/Chicago)")
    p.add_argument("--slot", choices=["a", "b"])
    a = ap.parse_args(argv)
    date = a.date or timeutil.local_date()
    res = slots(date, slot=a.slot)
    if not res:
        print("no slots configured", file=sys.stderr)
        return 4
    print(json.dumps(res, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
