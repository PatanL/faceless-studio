"""Which operator jobs are due now (docs/OPERATOR_DESIGN.md 10.1).

`due_jobs(config, state, posts, metrics, now, facts)` is a pure function: it returns new time-based jobs (make per
slot, Buffer status refresh, metrics at published + 48 h / 7 d, TikTok inbox, Monday learning, kill rule) plus the
pending chained jobs already in state (review, fix, publish, retries) whose due_at has passed. Ids are
deterministic (`<YYYYMMDD>-<slot|na>-<type>[-<suffix>]`), so calling it twice or after a restart adds nothing new.

  python -m pipeline.ops.due [--now ISO] [--register] [--json]

--register writes new jobs to state.json as pending and marks expired ones skipped. Order of the output:
publish, review, fix, make, status, metrics, tiktok, learning, killrule (then due_at).

Publish jobs expire at post_at + publish_late_h (skipped, never failed: a missed slot does not reject the source),
also while the loop is paused. A metrics job whose latest row for (post_key, window) is still incomplete (dry run or
synthetic, `pending`, an error, or no views) gets a `-retry<k>` job 12 h after the previous attempt finished, until
window + 48 h. In-session jobs (review, tiktok_screens) wait while the operator session is at its daily token cap.
"""
from __future__ import annotations

import argparse
import datetime as dt
import glob
import json
import os
import sys

from pipeline.common import jsonl, timeutil
from pipeline.ops import paths, state as S

PRIORITY = {"publish": 0, "review": 1, "fix": 2, "make": 3, "status": 4, "metrics48": 5, "metrics7d": 5,
            "tiktok_inbox": 6, "tiktok_screens": 6, "learning": 7, "killrule": 8, "triage": 9}
OPEN_POST = {"draft", "scheduled", "sending"}
METRICS_RETRY_H = 12      # collect.RETRY_PENDING_H
METRICS_GRACE_H = 48      # collect.PENDING_GRACE_H


def metric_incomplete(m: dict | None) -> bool:
    """A metrics row that should be fetched again: missing, dry-run/synthetic, pending, an error, or no views."""
    if not m:
        return True
    return bool(m.get("dry_run") or m.get("status") == "dry_run" or m.get("source") == "synthetic"
                or m.get("error") or m.get("pending") or m.get("views") is None)


def needs_link(p: dict, now: dt.datetime) -> bool:
    """A published Buffer post whose platform link is not known yet (status.py keeps polling it for 48 h)."""
    if p.get("status") != "published" or p.get("dry_run") or not p.get("buffer_post_id"):
        return False
    if p.get("external_url") and p.get("external_id"):
        return False
    sent = p.get("published_at")
    return not sent or (now - timeutil.parse(sent)).total_seconds() < 48 * 3600
WEEKDAYS = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]


def window_label(h: int) -> str:
    return "7d" if h == 168 else ("28d" if h == 672 else f"{h}h")


def _tz(config):
    return timeutil.ZoneInfo(config.get("tz", "America/Chicago"))


def _makes_allowed(config: dict, st: dict, facts: dict, now: dt.datetime) -> tuple[bool, str]:
    if config.get("paused"):
        return False, "config.paused"
    if st.get("paused"):
        return False, f"state.paused ({st.get('pause_reason')})"
    stop = (st.get("budget") or {}).get("stop_until")
    if stop and now < timeutil.parse(stop):
        return False, "budget stop"
    if facts.get("budget") == "hard":
        return False, "budget hard cap"
    return True, ""


def time_based_jobs(config: dict, st: dict, posts: dict, metrics: list, now: dt.datetime, facts: dict) -> list[dict]:
    tz = _tz(config)
    today = timeutil.local_date(now, tz)
    d8 = today.replace("-", "")
    jobs: list[dict] = []
    ok_make, _ = _makes_allowed(config, st, facts, now)

    # make per slot (today only: yesterday's slot is gone once its post time passed)
    for i, s in enumerate(config["slots"]):
        if not ok_make:
            break
        if facts.get("budget") == "soft" and i > 0:  # >= 80 % of the weekly budget: one video per day
            continue
        info = S.slot_info(config, today, s["slot"])
        expires = timeutil.parse(info["post_at"]) - dt.timedelta(hours=config.get("make_deadline_h_before_post", 3))
        jobs.append({"job_id": S.job_id(today, s["slot"], "make"), "type": "make", "date": today, "slot": s["slot"],
                     "due_at": info["make_at"], "expires_at": timeutil.iso(expires), "post_at": info["post_at"]})

    # Buffer status refresh: current half-hour bucket, only while some post is open
    if any(((p.get("status") in OPEN_POST) and not p.get("dry_run")) or needs_link(p, now) for p in posts.values()):
        every = int(config.get("status_every_min", 30))
        loc = timeutil.to_local(now, tz)
        mins = (loc.hour * 60 + loc.minute) // every * every
        bucket = loc.replace(hour=mins // 60, minute=mins % 60, second=0, microsecond=0)
        jobs.append({"job_id": S.job_id(today, None, "status", f"{bucket:%H%M}"), "type": "status",
                     "due_at": timeutil.iso(bucket), "expires_at": timeutil.iso(bucket + dt.timedelta(minutes=every))})

    # metrics at published + 48 h / 7 d (API platforms only; TikTok comes through the inbox)
    have = {(m.get("post_key"), m.get("window")) for m in metrics if not m.get("error") and not m.get("dry_run")}
    last_row: dict = {}
    for m in metrics:
        last_row[(m.get("post_key"), m.get("window"))] = m
    existing = st.get("jobs", {})
    for key, p in posts.items():
        if p.get("status") != "published" or not p.get("published_at"):
            continue
        if p.get("platform") not in config.get("metrics_platforms", ["youtube", "instagram"]):
            continue
        pub = timeutil.parse(p["published_at"])
        pd = timeutil.local_date(pub, tz)
        for h in config.get("metrics_windows_h", [48, 168]):
            w = window_label(int(h))
            jt = "metrics48" if w == "48h" else ("metrics7d" if w == "7d" else f"metrics{w}")
            base = {"type": jt if jt in PRIORITY else "metrics48", "post_key": key, "slug": p.get("slug"),
                    "platform": p.get("platform"), "window": w, "source_id": p.get("source_id")}
            base_id = S.job_id(pd, None, jt, key)
            if base_id in existing:
                retry = _metrics_retry(existing, base_id, last_row.get((key, w)), pub, int(h), now)
                if retry:
                    jobs.append({**base, **retry})
                continue
            if (key, w) in have:
                continue
            jobs.append({"job_id": base_id, **base, "due_at": timeutil.iso(pub + dt.timedelta(hours=int(h)))})

    # TikTok inbox (daily, only when files are waiting)
    if facts.get("tiktok_inbox", 0) > 0:
        jobs.append({"job_id": S.job_id(today, None, "tiktok_inbox"), "type": "tiktok_inbox",
                     "due_at": timeutil.iso(timeutil.at_local(today, config.get("tiktok_inbox_at", "21:00"), tz))})

    # weekly learning + kill rule on the configured weekday; caught up later in the same week after downtime
    lw = config.get("learning", {})
    wd = WEEKDAYS.index(lw.get("weekday", "MON"))
    loc_date = timeutil.to_local(now, tz).date()
    anchor = loc_date - dt.timedelta(days=(loc_date.weekday() - wd) % 7)
    a_iso = anchor.isoformat()
    learn_dt = timeutil.at_local(a_iso, lw.get("at", "07:30"), tz)
    learn_at = timeutil.iso(learn_dt)
    late_by = learn_dt + dt.timedelta(days=int(lw.get("catch_up_days", 3)))  # after downtime, catch up for 3 days only
    jobs.append({"job_id": S.job_id(a_iso, None, "learning"), "type": "learning", "week": timeutil.iso_week(learn_dt, tz),
                 "due_at": learn_at, "expires_at": timeutil.iso(late_by)})
    jobs.append({"job_id": S.job_id(a_iso, None, "killrule"), "type": "killrule", "due_at": learn_at,
                 "expires_at": timeutil.iso(late_by)})

    # kill rule every Nth new 7-day YouTube row once n >= after_videos
    kr = config.get("kill_rule", {})
    n7 = len({m.get("post_key") for m in metrics if m.get("platform") == "youtube" and m.get("window") == "7d"
              and not m.get("error") and not m.get("dry_run")})
    last_n = int((st.get("killrule") or {}).get("last_n") or 0)
    if n7 >= kr.get("after_videos", 30) and n7 - last_n >= kr.get("recheck_every", 5):
        jobs.append({"job_id": S.job_id(today, None, "killrule", f"n{n7}"), "type": "killrule", "due_at": timeutil.iso(now)})
    return jobs


def _metrics_retry(existing: dict, base_id: str, last: dict | None, pub: dt.datetime, h: int,
                   now: dt.datetime) -> dict | None:
    """The next `<base>-retry<k>` job (id + due_at) when the base job and earlier retries have finished and the
    latest row is still incomplete, 12 h after the last attempt, within window + 48 h; else None."""
    if not metric_incomplete(last):
        return None
    if now > pub + dt.timedelta(hours=h + METRICS_GRACE_H):
        return None
    tries = [base_id] + sorted((k for k in existing if k.startswith(base_id + "-retry")),
                               key=lambda k: int(k.rsplit("retry", 1)[1] or 0))
    prev = existing[tries[-1]]
    if prev.get("status") in ("pending", "running"):
        return None
    since = prev.get("finished_at") or prev.get("due_at")
    due = timeutil.parse(since) + dt.timedelta(hours=METRICS_RETRY_H) if since else now
    return {"job_id": f"{base_id}-retry{len(tries)}", "due_at": timeutil.iso(max(due, pub + dt.timedelta(hours=h))),
            "retry": len(tries)}


def due_jobs(config: dict, st: dict, posts: dict, metrics: list, now: dt.datetime, facts: dict | None = None) -> dict:
    """{"due": [...], "expired": [...], "new": [...]} - pure; `new` = due or future-dated jobs not yet in state."""
    facts = facts or {}
    existing = st.get("jobs", {})
    due, expired, new = [], [], []
    ok_make, why = _makes_allowed(config, st, facts, now)
    for j in time_based_jobs(config, st, posts, metrics, now, facts):
        if j["job_id"] in existing:
            continue
        exp = j.get("expires_at")
        if exp and now >= timeutil.parse(exp):
            if j["type"] == "make":
                expired.append({**j, "reason": "too late for the slot"})
            continue
        if timeutil.parse(j["due_at"]) <= now:
            new.append(j)
            due.append(j)
    for jid, j in existing.items():
        if j.get("status") != "pending":
            continue
        exp = j.get("expires_at")
        if not exp and j.get("type") == "publish" and j.get("date") and j.get("slot"):
            try:  # publish jobs registered before they carried expires_at
                post_at = timeutil.parse(S.slot_info(config, j["date"], j["slot"])["post_at"])
                exp = timeutil.iso(post_at + dt.timedelta(hours=config.get("publish_late_h", 2)))
            except KeyError:
                exp = None
        if exp and now >= timeutil.parse(exp):  # checked before the pause: a paused publish still expires
            why = "slot post time passed while pending" if j.get("type") == "publish" else "expired while pending"
            expired.append({"job_id": jid, **j, "reason": why})
            continue
        if j.get("type") == "make" and not ok_make:
            continue
        if j.get("type") == "publish" and (config.get("paused") or st.get("paused")):
            continue
        if j.get("type") in S.SESSION_JOB_TYPES and facts.get("operator_cap"):
            continue
        if timeutil.parse(j.get("due_at") or timeutil.iso(now)) <= now:
            due.append({"job_id": jid, **j})
    due.sort(key=lambda j: (PRIORITY.get(j.get("type"), 99), j.get("due_at") or ""))
    return {"due": due, "expired": expired, "new": new, "makes_blocked": None if ok_make else why,
            "session_blocked": "operator daily token cap" if facts.get("operator_cap") else None}


# ---------------------------------------------------------------------------------------------- disk loaders
def load_facts(config: dict, st: dict) -> dict:
    from pipeline.ops import budget
    b = budget.check(config, st)
    facts = {"budget": b["level"], "operator_cap": b.get("operator_cap", False),
             "operator_measured_today": b.get("operator_measured_today")}
    inbox = os.path.join(paths.data_dir(), "inbox", "tiktok")
    facts["tiktok_inbox"] = len([f for f in glob.glob(os.path.join(inbox, "*")) if os.path.isfile(f)])
    return facts


def due_from_disk(config: dict, st: dict, now: dt.datetime) -> list[dict]:
    posts = jsonl.latest(paths.ledger("posts.jsonl"), "post_key")
    metrics = jsonl.read(paths.ledger("metrics.jsonl"))
    return due_jobs(config, st, posts, metrics, now, load_facts(config, st))["due"]


def register_due(now: dt.datetime | None = None) -> dict:
    now = now or timeutil.now_utc()
    config = S.load_config()
    with S.updating() as st:
        posts = jsonl.latest(paths.ledger("posts.jsonl"), "post_key")
        metrics = jsonl.read(paths.ledger("metrics.jsonl"))
        facts = load_facts(config, st)
        r = due_jobs(config, st, posts, metrics, now, facts)
        if facts.get("operator_measured_today") is not None:
            md = st["budget"].setdefault("operator_measured_by_day", {})
            md[timeutil.local_date(now)] = int(facts["operator_measured_today"])
            for k in sorted(md)[:-21]:
                md.pop(k, None)
        if facts.get("operator_cap"):
            S.human("The operator session reached its daily token cap (budget.operator_tokens_per_day_estimate, "
                    "measured from its transcripts): in-session jobs (review, tiktok_screens) wait until tomorrow. "
                    "Deterministic jobs keep running.", key=f"opcap:{timeutil.local_date(now)}", st=st)
        for j in r["new"]:
            S.register(st, j)
        for j in r["expired"]:
            jid = j["job_id"]
            if jid not in st["jobs"]:
                S.register(st, {k: v for k, v in j.items() if k != "reason"})
            if st["jobs"][jid].get("status") == "pending":
                if j.get("type") == "publish":
                    S.finish_job(st, config, jid, "skipped", note=j["reason"], now=now)
                    S.journal(f"{jid}: skipped ({j['reason']})")
                    continue
                st["jobs"][jid].update({"status": "skipped", "note": j["reason"], "finished_at": timeutil.iso(now)})
                if j.get("type") == "make" and j.get("slot"):
                    S.journal(f"{jid}: skipped ({j['reason']})")
    return r


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.ops.due")
    ap.add_argument("--now", help="ISO time (testing)")
    ap.add_argument("--register", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    now = timeutil.parse(a.now) if a.now else timeutil.now_utc()
    if a.register:
        r = register_due(now)
    else:
        cfg = S.load_config()
        st = S.load_state()
        posts = jsonl.latest(paths.ledger("posts.jsonl"), "post_key")
        r = due_jobs(cfg, st, posts, jsonl.read(paths.ledger("metrics.jsonl")), now, load_facts(cfg, st))
    if a.json:
        print(json.dumps(r, indent=1))
    else:
        for j in r["due"]:
            mode = "session" if j.get("type") in S.SESSION_JOB_TYPES else "run.py"
            print(f"DUE  {j['job_id']:<60} {j.get('type'):<13} {mode:<8} due {j.get('due_at')}")
        for j in r["expired"]:
            print(f"SKIP {j['job_id']:<60} {j.get('reason')}")
        if r.get("makes_blocked"):
            print(f"makes blocked: {r['makes_blocked']}")
        if not r["due"]:
            print("nothing due")
    return 0 if r["due"] else 4


if __name__ == "__main__":
    sys.exit(main())
