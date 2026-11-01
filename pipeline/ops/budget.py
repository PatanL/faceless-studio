"""Token budget (docs/OPERATOR_DESIGN.md 10.4). Unit: weighted tokens = input + output + cache_creation + 0.1 * cache_read.

Week total = sum of `usage_total.weighted_tokens` in episodes/op-*/make_status.json whose started_at falls in the
local ISO week, plus the operator's own estimates (`add-operator`). check() levels:

  ok    < soft_pct (80 %) of the weekly cap
  soft  >= 80 %: one video per day (slot B skipped), no optional review rounds or optional analysis
  hard  >= 100 %: no makes until Monday; metrics, status and learning keep running

The per-video cap is enforced by studio-make itself (`--budget-tokens`, exit 3, make_status budget_cap=video);
only `hard` here stops makes for the week.

Operator session usage is measured, not trusted: the session transcripts
(~/.claude/projects/<project>/<session_id>.jsonl, plus <session_id>/**/*.jsonl for its subagents; override the root
with CLAUDE_PROJECTS_DIR) are summed per local day from the `message.usage` of assistant entries (deduped by
message id). Per day the larger of that and the `add-operator` self-reports counts. At
budget.operator_tokens_per_day_estimate (1.5M) `operator_cap` is true: due.py holds in-session jobs (review,
tiktok_screens) until the next day and HUMAN.md says so.

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


def projects_dir() -> str:
    return os.path.expanduser(os.environ.get("CLAUDE_PROJECTS_DIR") or "~/.claude/projects")


def session_ids(st: dict) -> list[str]:
    ids = [x.get("id") for x in (st.get("sessions") or []) if x.get("id")]
    cur = (st.get("session") or {}).get("id")
    return list(dict.fromkeys(ids + ([cur] if cur else [])))


def transcript_files(ids: list[str]) -> list[str]:
    root = projects_dir()
    out = []
    for sid in ids:
        out += glob.glob(os.path.join(root, "*", f"{sid}.jsonl"))
        out += glob.glob(os.path.join(root, "*", sid, "**", "*.jsonl"), recursive=True)
    return sorted(set(out))


def measured_by_day(ids: list[str]) -> dict[str, float]:
    """Weighted tokens per local date from the transcripts of these sessions (and their subagents)."""
    seen, by = set(), {}
    for f in transcript_files(ids):
        try:
            fh = open(f, encoding="utf-8", errors="replace")
        except OSError:
            continue
        with fh:
            for line in fh:
                if '"usage"' not in line:
                    continue
                try:
                    e = json.loads(line)
                except json.JSONDecodeError:
                    continue
                msg = e.get("message") if isinstance(e, dict) else None
                u = (msg or {}).get("usage") if isinstance(msg, dict) else None
                if not isinstance(u, dict) or not e.get("timestamp"):
                    continue
                key = (msg.get("id"), e.get("requestId")) if msg.get("id") else (f, e.get("uuid"))
                if key in seen:  # streamed messages repeat the same usage on several lines
                    continue
                seen.add(key)
                try:
                    day = timeutil.local_date(timeutil.parse(e["timestamp"]))
                except (ValueError, TypeError):
                    continue
                w = (u.get("input_tokens", 0) or 0) + (u.get("output_tokens", 0) or 0) + \
                    (u.get("cache_creation_input_tokens", 0) or 0) + 0.1 * (u.get("cache_read_input_tokens", 0) or 0)
                by[day] = by.get(day, 0.0) + w
    return by


def operator_by_day(st: dict, measured: dict[str, float] | None = None) -> dict[str, float]:
    """max(self-reported, measured) per day; measured falls back to what register_due cached in state."""
    b = st.get("budget") or {}
    rep = b.get("operator_by_day") or {}
    meas = dict(b.get("operator_measured_by_day") or {})
    meas.update(measured or {})
    return {d: max(float(rep.get(d, 0)), float(meas.get(d, 0))) for d in set(rep) | set(meas)}


def operator_usage(st: dict, week: str, measured: dict[str, float] | None = None) -> float:
    return float(sum(v for d, v in operator_by_day(st, measured).items()
                     if timeutil.iso_week(timeutil.at_local(d, "12:00")) == week))


def check(config: dict, st: dict, now=None) -> dict:
    week = timeutil.iso_week(now)
    b = config["budget"]
    mk = make_usage(week)
    try:
        measured = measured_by_day(session_ids(st))
    except Exception:  # noqa: BLE001 - never let a bad transcript break the loop; self-reports still count
        measured = {}
    op = operator_usage(st, week, measured)
    used = mk["total"] + op
    cap = float(b["weighted_tokens_per_week"])
    pct = 100.0 * used / cap if cap else 0.0
    level = "hard" if pct >= 100 else ("soft" if pct >= b.get("soft_pct", 80) else "ok")
    today = timeutil.local_date(now)
    op_today = float(operator_by_day(st, measured).get(today, 0))
    day_cap = int(b.get("operator_tokens_per_day_estimate", 0))
    return {"week": week, "level": level, "pct": round(pct, 1), "used": int(used), "cap": int(cap),
            "make": int(mk["total"]), "operator": int(op), "operator_today": int(op_today),
            "operator_measured_today": int(measured.get(today, 0)),
            "operator_day_cap": day_cap, "operator_cap": bool(day_cap) and op_today >= day_cap,
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
    print(f"{r['level']} {r['pct']}% of {r['cap']} (make {r['make']}, operator {r['operator']}; today operator "
          f"{r['operator_today']}/{r['operator_day_cap']} (measured {r['operator_measured_today']})"
          f"{' CAP: in-session jobs held' if r['operator_cap'] else ''})")
    return 3 if r["level"] == "hard" else 0


if __name__ == "__main__":
    sys.exit(main())
