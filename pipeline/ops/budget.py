"""Token budget (docs/OPERATOR_DESIGN.md 10.4). Unit: weighted tokens = input + output + cache_creation + 0.1 * cache_read.

Week total = sum of `usage_total.weighted_tokens` in episodes/op-*/make_status.json whose started_at falls in the
local ISO week, plus the operator's own estimates (`add-operator`). check() levels:

  ok    < soft_pct (80 %) of the weekly cap
  soft  >= 80 %: one video per day (slot B skipped), no optional review rounds or optional analysis
  hard  >= 100 %: no makes until Monday; metrics, status and learning keep running

The per-video cap is enforced by studio-make itself (`--budget-tokens`, exit 3).

  python -m pipeline.ops.budget show
  python -m pipeline.ops.budget check            # exit 0 ok, 3 hard (prints the level)
  python -m pipeline.ops.budget add-operator N [--what review]
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys

from pipeline.common import timeutil
from pipeline.ops import paths, state as S


def weighted(u: dict) -> float:
    return (u.get("input_tokens", 0) + u.get("output_tokens", 0) + u.get("cache_creation_tokens", 0)
            + 0.1 * u.get("cache_read_tokens", 0))


def make_usage(week: str) -> dict:
    total, per = 0.0, {}
    for f in glob.glob(os.path.join(paths.episodes_dir(), "op-*", "make_status.json")):
        try:
            with open(f, encoding="utf-8") as fh:
                ms = json.load(fh)
        except (OSError, json.JSONDecodeError):
            continue
        started = ms.get("started_at")
        if not started or timeutil.iso_week(timeutil.parse(started)) != week:
            continue
        ut = ms.get("usage_total") or {}
        w = ut.get("weighted_tokens")
        if w is None:
            w = sum(weighted(u) for u in (ms.get("usage") or {}).values() if isinstance(u, dict))
        per[ms.get("slug") or os.path.basename(os.path.dirname(f))] = float(w)
        total += float(w)
    return {"total": total, "per_video": per}


def operator_usage(st: dict, week: str) -> float:
    by_day = (st.get("budget") or {}).get("operator_by_day") or {}
    return float(sum(v for d, v in by_day.items() if timeutil.iso_week(timeutil.at_local(d, "12:00")) == week))


def check(config: dict, st: dict, now=None) -> dict:
    week = timeutil.iso_week(now)
    b = config["budget"]
    mk = make_usage(week)
    op = operator_usage(st, week)
    used = mk["total"] + op
    cap = float(b["weighted_tokens_per_week"])
    pct = 100.0 * used / cap if cap else 0.0
    level = "hard" if pct >= 100 else ("soft" if pct >= b.get("soft_pct", 80) else "ok")
    today = timeutil.local_date(now)
    op_today = float(((st.get("budget") or {}).get("operator_by_day") or {}).get(today, 0))
    return {"week": week, "level": level, "pct": round(pct, 1), "used": int(used), "cap": int(cap),
            "make": int(mk["total"]), "operator": int(op), "operator_today": int(op_today),
            "operator_day_cap": int(b.get("operator_tokens_per_day_estimate", 0)),
            "per_video_cap": int(b["weighted_tokens_per_video"]), "per_video": mk["per_video"]}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.ops.budget")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("show"); sub.add_parser("check")
    p = sub.add_parser("add-operator"); p.add_argument("tokens", type=int); p.add_argument("--what", default="")
    a = ap.parse_args(argv)
    cfg = S.load_config()
    if a.cmd == "add-operator":
        with S.updating() as st:
            d = timeutil.local_date()
            by = st["budget"].setdefault("operator_by_day", {})
            by[d] = int(by.get(d, 0)) + a.tokens
            st["budget"]["operator_tokens_estimate"] = int(st["budget"].get("operator_tokens_estimate", 0)) + a.tokens
            st["budget"]["week"] = timeutil.iso_week()
            # keep 21 days
            for k in sorted(by)[:-21]:
                by.pop(k, None)
        print(f"operator estimate +{a.tokens} {a.what}".strip())
        return 0
    r = check(cfg, S.load_state())
    if a.cmd == "show":
        print(json.dumps(r, indent=1))
        return 0
    print(f"{r['level']} {r['pct']}% of {r['cap']} (make {r['make']}, operator {r['operator']}; today operator {r['operator_today']}/{r['operator_day_cap']})")
    return 3 if r["level"] == "hard" else 0


if __name__ == "__main__":
    sys.exit(main())
