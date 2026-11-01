"""Operator state (docs/OPERATOR_DESIGN.md 5.18), config overlay (5.19), journal, HUMAN.md and job chaining.

Only the operator session and pipeline/ops/* touch data/operator/state.json. Writes are atomic (.tmp + os.replace)
under an flock on state.json.lock.

CLI (run from ~/studio/app; the operator uses these instead of editing JSON by hand):

  python -m pipeline.ops.state init                         # create state.json / config.json from defaults if missing
  python -m pipeline.ops.state show [--brief]
  python -m pipeline.ops.state heartbeat [--resume]         # --resume also sets session.last_resume_at
  python -m pipeline.ops.state session-start --id UUID      # operator_tmux.sh, on a fresh session
  python -m pipeline.ops.state journal "text"
  python -m pipeline.ops.state human "text" [--key K]       # append to HUMAN.md (deduped by key)
  python -m pipeline.ops.state crons-set '[{"name":"tick","schedule":"*/20 * * * *","id":"..."}]'
  python -m pipeline.ops.state busy on|off [--what review]  # in-session LLM job running (watchdog won't rotate)
  python -m pipeline.ops.state job JOB_ID --status done|failed|skipped [--verdict PASS|FIX|REJECT] [--exit N] [--note T]
  python -m pipeline.ops.state pause "reason"               # operator may pause; only the human unpauses
  python -m pipeline.ops.state watchdog --tmux-alive 0|1    # prints none|tick|resume|rotate
"""
from __future__ import annotations

import argparse
import contextlib
import copy
import datetime as dt
import json
import os
import sys

from pipeline.common import locks, timeutil
from pipeline.ops import paths

SESSION_JOB_TYPES = {"review", "tiktok_screens", "triage"}
DETERMINISTIC_JOB_TYPES = {"make", "fix", "publish", "status", "metrics48", "metrics7d", "learning",
                           "killrule", "tiktok_inbox"}


# ---------------------------------------------------------------------------------------------- config
def _deep_merge(base: dict, over: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in (over or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def load_config() -> dict:
    with open(paths.default_config_file(), encoding="utf-8") as f:
        base = json.load(f)
    try:
        with open(paths.config_file(), encoding="utf-8") as f:
            over = json.load(f)
    except FileNotFoundError:
        over = {}
    return _deep_merge(base, over)


def approval_mode() -> str:
    """'auto' only if both $APPROVAL_MODE and data/operator/approval_mode say auto; anything else is 'drafts'."""
    env = (os.environ.get("APPROVAL_MODE") or "drafts").strip().lower()
    try:
        with open(paths.approval_file(), encoding="utf-8") as f:
            filev = f.read().strip().lower()
    except FileNotFoundError:
        filev = "drafts"
    return "auto" if env == "auto" and filev == "auto" else "drafts"


def effective_mode(config: dict, platform: str, approval: str | None = None) -> str:
    """auto needs APPROVAL_MODE=auto AND config.mode.<p>=auto AND config.disclosure_ok_auto.<p>=true. Else draft."""
    approval = approval or approval_mode()
    if approval != "auto":
        return "draft"
    if (config.get("mode") or {}).get(platform) != "auto":
        return "draft"
    if not (config.get("disclosure_ok_auto") or {}).get(platform):
        return "draft"
    return "auto"


# ---------------------------------------------------------------------------------------------- state
def default_state() -> dict:
    return {
        "v": 1,
        "session": {"id": None, "started_at": None, "last_resume_at": None, "heartbeat_at": None, "tmux": "studio-op",
                    "busy": None},
        "paused": False, "pause_reason": None,
        "crons": [],
        "jobs": {},
        "budget": {"week": None, "weighted_tokens": 0, "videos": 0, "operator_tokens_estimate": 0,
                   "operator_by_day": {}, "stop_until": None},
        "experiment": {"active": None},
        "rejected_sources": [],
        "notified": [],
        "killrule": {"last_n": 0, "verdict": None},
        "counters": {"published": {"youtube": 0, "tiktok": 0, "instagram": 0}, "drafts_created": 0,
                     "consecutive_failed_slots": 0, "slots_failed": 0, "slots_posted": 0},
    }


def load_state() -> dict:
    try:
        with open(paths.state_file(), encoding="utf-8") as f:
            st = json.load(f)
    except FileNotFoundError:
        return default_state()
    return _deep_merge(default_state(), st)


def _write_atomic(path: str, obj: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = f"{path}.tmp.{os.getpid()}"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


@contextlib.contextmanager
def updating():
    """with updating() as st: ... -> saved atomically under the state lock."""
    os.makedirs(paths.ops_dir(), exist_ok=True)
    with locks.flock(paths.state_file() + ".lock", timeout_s=120):
        st = load_state()
        yield st
        _write_atomic(paths.state_file(), st)


def init() -> list[str]:
    made = []
    os.makedirs(paths.ops_dir(), exist_ok=True)
    os.makedirs(os.path.join(paths.ops_dir(), "jobs"), exist_ok=True)
    if not os.path.exists(paths.config_file()):
        with open(paths.default_config_file(), encoding="utf-8") as f:
            cfg = json.load(f)
        _write_atomic(paths.config_file(), cfg)
        made.append(paths.config_file())
    if not os.path.exists(paths.state_file()):
        with updating():
            pass
        made.append(paths.state_file())
    for p, head in ((paths.journal_file(), "# Operator journal (UTC)\n"), (paths.human_file(), "# For the human\n\nNewest last. The operator appends; the human deletes entries once handled.\n")):
        if not os.path.exists(p):
            with open(p, "w", encoding="utf-8") as f:
                f.write(head)
            made.append(p)
    return made


# ---------------------------------------------------------------------------------------------- journal / human
def journal(text: str) -> None:
    os.makedirs(paths.ops_dir(), exist_ok=True)
    with open(paths.journal_file(), "a", encoding="utf-8") as f:
        for i, line in enumerate(text.strip().splitlines() or [""]):
            f.write(f"- {timeutil.iso()} {line}\n" if i == 0 else f"  {line}\n")


def human(text: str, key: str | None = None, st: dict | None = None) -> bool:
    """Append an entry to HUMAN.md. With a key, an entry is written once (state.notified). Returns True if written."""
    if key:
        if st is not None:
            if key in st["notified"]:
                return False
            st["notified"] = (st["notified"] + [key])[-500:]
        else:
            with updating() as s:
                if key in s["notified"]:
                    return False
                s["notified"] = (s["notified"] + [key])[-500:]
    os.makedirs(paths.ops_dir(), exist_ok=True)
    with open(paths.human_file(), "a", encoding="utf-8") as f:
        f.write(f"\n## {timeutil.iso()} {('[' + key + ']') if key else ''}\n\n{text.strip()}\n")
    return True


# ---------------------------------------------------------------------------------------------- jobs
def job_id(date: str, slot: str | None, jtype: str, suffix: str | None = None) -> str:
    jid = f"{date.replace('-', '')}-{slot or 'na'}-{jtype}"
    return f"{jid}-{suffix}" if suffix else jid


def register(st: dict, job: dict) -> bool:
    """Add a pending job if its id is new. Idempotent. Returns True if added."""
    if job["job_id"] in st["jobs"]:
        return False
    j = {"status": "pending", "attempts": 0, "created_at": timeutil.iso()}
    j.update({k: v for k, v in job.items() if k != "job_id"})
    st["jobs"][job["job_id"]] = j
    return True


def slot_info(config: dict, date: str, slot: str) -> dict:
    for s in config["slots"]:
        if s["slot"] == slot:
            tz = timeutil.ZoneInfo(config.get("tz", "America/Chicago"))
            return {"make_at": timeutil.iso(timeutil.at_local(date, s["make_at"], tz)),
                    "post_at": timeutil.iso(timeutil.at_local(date, s["post_at"], tz))}
    raise KeyError(f"no slot {slot!r} in config")


def _slot_jobs(st: dict, date: str, slot: str, jtype: str) -> list[str]:
    pre = job_id(date, slot, jtype)
    return [k for k in st["jobs"] if k == pre or k.startswith(pre + "-")]


def _pause(st: dict, reason: str, detail: str) -> None:
    st["paused"] = True
    st["pause_reason"] = reason
    human(f"Operator paused: **{reason}**.\n\n{detail}\n\nTo resume: fix the cause, then `scripts/operator_ctl.sh unpause`.",
          key=f"pause:{reason}:{timeutil.local_date()}", st=st)


def slot_failed(st: dict, config: dict, job: dict, why: str, now: dt.datetime | None = None) -> str:
    """The make/review chain of a slot failed. Reject the source; retry with the next source if the slot's post
    time is still >= make_deadline_h away and this slot has had only one source; else count the slot as failed."""
    now = now or timeutil.now_utc()
    date, slot = job.get("date"), job.get("slot")
    src = (job.get("result") or {}).get("source_id") or job.get("source_id")
    if src and src not in st["rejected_sources"]:
        st["rejected_sources"].append(src)
    makes = _slot_jobs(st, date, slot, "make")
    post_at = timeutil.parse(slot_info(config, date, slot)["post_at"])
    left_h = (post_at - now).total_seconds() / 3600
    if len(makes) < 2 and left_h >= config.get("make_deadline_h_before_post", 3) and not st["paused"]:
        register(st, {"job_id": job_id(date, slot, "make", "r2"), "type": "make", "date": date, "slot": slot,
                      "due_at": timeutil.iso(now), "expires_at": timeutil.iso(post_at - dt.timedelta(hours=config.get("make_deadline_h_before_post", 3))),
                      "reason": f"retry with next source after: {why}"})
        journal(f"slot {date}/{slot}: {why}; source {src} rejected; retrying with the next source ({left_h:.1f} h left)")
        return "retry"
    c = st["counters"]
    c["consecutive_failed_slots"] += 1
    c["slots_failed"] += 1
    journal(f"slot {date}/{slot} FAILED ({why}); consecutive failed slots: {c['consecutive_failed_slots']}")
    if c["consecutive_failed_slots"] >= 2:
        _pause(st, "two_failed_slots", f"Last failure: slot {date}/{slot}: {why}. See data/operator/journal.md and the job logs.")
    return "failed"


def finish_job(st: dict, config: dict, jid: str, status: str, exit_code: int | None = None,
               verdict: str | None = None, result: dict | None = None, note: str | None = None,
               now: dt.datetime | None = None) -> list[str]:
    """Record a job's end and register what follows it. Returns the ids of newly registered jobs."""
    now = now or timeutil.now_utc()
    j = st["jobs"].setdefault(jid, {"status": "pending", "attempts": 0})
    before = set(st["jobs"])
    j.update({"status": status, "finished_at": timeutil.iso(now), "pid": None})
    if exit_code is not None:
        j["exit_code"] = exit_code
    if verdict:
        j["verdict"] = verdict
    if result:
        j["result"] = {**(j.get("result") or {}), **result}
    if note:
        j["note"] = note
    t = j.get("type")
    date, slot = j.get("date"), j.get("slot")
    res = j.get("result") or {}
    slug = res.get("slug") or j.get("slug")

    if exit_code == 5:
        _pause(st, "dependency_unavailable", f"Job `{jid}` exited 5 (claude auth, API 401/403, tunnel or a lane not installed). Log: {j.get('log')}")
    elif exit_code == 3:
        nxt_monday = timeutil.to_local(now).date() + dt.timedelta(days=7 - timeutil.to_local(now).weekday())
        st["budget"]["stop_until"] = timeutil.iso(timeutil.at_local(nxt_monday.isoformat(), "00:00"))
        human(f"Budget cap reached by `{jid}`; makes are paused until {nxt_monday} (metrics keep running).",
              key=f"budget:{timeutil.iso_week(now)}", st=st)

    if t in ("make", "fix"):
        if status == "done":
            rnd = 1 if t == "make" else int(j.get("round", 1)) + 1
            register(st, {"job_id": job_id(date, slot, "review", None if rnd == 1 else f"r{rnd}"), "type": "review",
                          "date": date, "slot": slot, "slug": slug, "round": rnd, "due_at": timeutil.iso(now),
                          "source_id": res.get("source_id") or j.get("source_id"), "gate": res.get("gate")})
        elif status == "failed" and exit_code not in (3, 5):
            slot_failed(st, config, j, f"{t} failed (exit {exit_code})", now)
        elif status == "failed":
            st["counters"]["slots_failed"] += 1
    elif t == "review" and status == "done":
        rnd = int(j.get("round", 1))
        if verdict == "PASS" and j.get("gate") == "FAIL":  # nothing posts without gate PASS
            verdict = "FIX"
            j["verdict"] = "FIX"
            j["note"] = ((j.get("note") or "") + " review PASS overridden: gate FAIL").strip()
        if verdict == "PASS":
            register(st, {"job_id": job_id(date, slot, "publish"), "type": "publish", "date": date, "slot": slot,
                          "slug": slug, "due_at": timeutil.iso(now), "source_id": j.get("source_id")})
        elif verdict == "FIX" and rnd <= int(config["budget"].get("max_fix_rounds", 1)):
            register(st, {"job_id": job_id(date, slot, "fix", None if rnd == 1 else f"r{rnd}"), "type": "fix",
                          "date": date, "slot": slot, "slug": slug, "round": rnd, "due_at": timeutil.iso(now),
                          "source_id": j.get("source_id")})
        else:
            slot_failed(st, config, j, f"review round {rnd} verdict {verdict or 'none'}", now)
    elif t == "publish":
        if status == "done":
            st["counters"]["consecutive_failed_slots"] = 0
            st["counters"]["slots_posted"] += 1
            st["counters"]["drafts_created"] += int(res.get("drafts", 0))
        elif exit_code not in (3, 5):
            slot_failed(st, config, j, f"publish failed (exit {exit_code})", now)
    elif t == "tiktok_inbox" and status == "done" and int(res.get("screenshots", 0)) > 0:
        register(st, {"job_id": job_id(timeutil.local_date(now), None, "tiktok_screens"), "type": "tiktok_screens",
                      "due_at": timeutil.iso(now), "files": int(res["screenshots"])})
    elif t == "killrule" and status == "done":
        act_on_killrule(st, res.get("killrule") or {})
    return sorted(set(st["jobs"]) - before)


def act_on_killrule(st: dict, kr: dict) -> None:
    """docs/OPERATOR_DESIGN.md 10.6: stop -> pause + HUMAN.md; extend/continue -> note."""
    if not kr:
        return
    v = kr.get("verdict")
    st["killrule"] = {"last_n": int(kr.get("n_videos") or 0), "verdict": v, "at": kr.get("at")}
    nums = (f"n={kr.get('n_videos')} median 7-d YouTube views={kr.get('median_views_7d')} (target "
            f"{kr.get('target_views_7d')}), first10 median={kr.get('first10_median')}, last10 median="
            f"{kr.get('last10_median')}, Theil-Sen slope/video={kr.get('theil_sen_slope_per_video')}")
    if v == "stop":
        _pause(st, "kill_rule", f"Kill rule says STOP: {nums}.\n\n{kr.get('explanation', '')}\n\nSee data/learning/LEARNING.md.")
    elif v in ("extend", "continue"):
        journal(f"kill rule: {v.upper()} ({nums})")


def mark_sources_rejected(ids: list[str], reason: str, slug: str | None = None) -> None:
    """Record rejected sources in L1's data/sources.jsonl via its CLI (L1 is that ledger's only writer).
    state.rejected_sources stays the operator's own exclude list either way."""
    import importlib.util
    import subprocess
    if not ids or importlib.util.find_spec("pipeline.sources") is None:
        return
    for sid in ids:
        cmd = [sys.executable, "-m", "pipeline.sources", "mark", sid, "rejected", "--reason", reason]
        if slug:
            cmd += ["--slug", slug]
        try:
            subprocess.run(cmd, cwd=paths.ROOT, timeout=120, capture_output=True)
        except (OSError, subprocess.TimeoutExpired):
            journal(f"could not mark source {sid} rejected in data/sources.jsonl")


def heartbeat(st: dict, resume: bool = False) -> None:
    st["session"]["heartbeat_at"] = timeutil.iso()
    if resume:
        st["session"]["last_resume_at"] = st["session"]["heartbeat_at"]


# ---------------------------------------------------------------------------------------------- watchdog
def watchdog_action(config: dict, st: dict, tmux_alive: bool, due_jobs: list[dict], now: dt.datetime,
                    stopped: bool = False) -> str:
    """none | resume | rotate | tick. Pure (tested)."""
    if stopped:
        return "none"
    if not tmux_alive:
        return "resume"
    tz = timeutil.ZoneInfo(config.get("tz", "America/Chicago"))
    sess = st.get("session") or {}
    busy = sess.get("busy")
    busy_fresh = bool(busy) and (now - timeutil.parse(busy["since"])).total_seconds() < 3600
    running_session_jobs = any(j.get("status") == "running" and j.get("type") in SESSION_JOB_TYPES for j in st["jobs"].values())
    started = timeutil.parse(sess["started_at"]) if sess.get("started_at") else None
    today = timeutil.local_date(now, tz)
    rot = timeutil.at_local(today, config.get("rotate_at", "04:00"), tz)
    in_window = rot <= now < rot + dt.timedelta(hours=config.get("rotate_window_h", 2))
    if started and not busy_fresh and not running_session_jobs:
        if (in_window and started < rot) or (now - started).total_seconds() > 30 * 3600:
            return "rotate"
    hb = sess.get("heartbeat_at")
    stale = (not hb) or (now - timeutil.parse(hb)).total_seconds() > 60 * config.get("heartbeat_stale_min", 45)
    if stale and due_jobs:
        return "tick"
    return "none"


# ---------------------------------------------------------------------------------------------- CLI
def _brief(st: dict) -> str:
    jobs = st["jobs"]
    open_ = {k: v for k, v in jobs.items() if v.get("status") in ("pending", "running")}
    recent = sorted(((v.get("finished_at") or "", k, v.get("status"), v.get("verdict") or v.get("exit_code"))
                     for k, v in jobs.items() if v.get("finished_at")), reverse=True)[:6]
    lines = [f"session: {st['session']}", f"paused: {st['paused']} ({st['pause_reason']})",
             f"crons: {[c.get('name') for c in st['crons']]}", f"budget: {st['budget']}",
             f"experiment: {st['experiment']}", f"counters: {st['counters']}", "open jobs:"]
    lines += [f"  {k}: {v.get('type')} {v.get('status')} due {v.get('due_at')}" for k, v in sorted(open_.items())] or ["  (none)"]
    lines += ["recent:"] + [f"  {r[1]}: {r[2]} {r[3]} at {r[0]}" for r in recent]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.ops.state")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    p = sub.add_parser("show"); p.add_argument("--brief", action="store_true")
    p = sub.add_parser("heartbeat"); p.add_argument("--resume", action="store_true")
    p = sub.add_parser("session-start"); p.add_argument("--id", required=True); p.add_argument("--tmux", default="studio-op")
    p = sub.add_parser("journal"); p.add_argument("text")
    p = sub.add_parser("human"); p.add_argument("text"); p.add_argument("--key")
    p = sub.add_parser("crons-set"); p.add_argument("json")
    p = sub.add_parser("busy"); p.add_argument("on_off", choices=["on", "off"]); p.add_argument("--what", default="session job")
    p = sub.add_parser("job"); p.add_argument("job_id")
    p.add_argument("--status", required=True, choices=["running", "done", "failed", "skipped"])
    p.add_argument("--verdict", choices=["PASS", "FIX", "REJECT"]); p.add_argument("--exit", type=int)
    p.add_argument("--note"); p.add_argument("--result", help="JSON object merged into job.result")
    p = sub.add_parser("pause"); p.add_argument("reason")
    p = sub.add_parser("unpause", help="human only (scripts/operator_ctl.sh unpause)")
    p = sub.add_parser("watchdog"); p.add_argument("--tmux-alive", type=int, required=True)
    a = ap.parse_args(argv)
    cfg = load_config()

    if a.cmd == "init":
        for m in init():
            print(f"created {m}")
        return 0
    if a.cmd == "show":
        st = load_state()
        print(_brief(st) if a.brief else json.dumps(st, indent=1))
        return 0
    if a.cmd == "journal":
        journal(a.text); return 0
    if a.cmd == "human":
        print("written" if human(a.text, key=a.key) else "already notified"); return 0
    if a.cmd == "watchdog":
        from pipeline.ops import due as due_mod
        st = load_state()
        now = timeutil.now_utc()
        jobs = due_mod.due_from_disk(cfg, st, now)
        print(watchdog_action(cfg, st, bool(a.tmux_alive), jobs, now, stopped=os.path.exists(paths.stopped_flag())))
        return 0
    rejected: list[str] = []
    slug = None
    with updating() as st:
        if a.cmd == "heartbeat":
            heartbeat(st, resume=a.resume)
        elif a.cmd == "session-start":
            now = timeutil.iso()
            st["session"].update({"id": a.id, "started_at": now, "last_resume_at": now, "heartbeat_at": now,
                                  "tmux": a.tmux, "busy": None})
            st["crons"] = []  # session crons die with the session; the new session re-arms them
        elif a.cmd == "crons-set":
            st["crons"] = json.loads(a.json)
        elif a.cmd == "busy":
            st["session"]["busy"] = {"what": a.what, "since": timeutil.iso()} if a.on_off == "on" else None
        elif a.cmd == "job":
            if a.job_id not in st["jobs"]:
                print(f"unknown job {a.job_id}", file=sys.stderr)
                return 2
            if a.status == "running":
                st["jobs"][a.job_id].update({"status": "running", "started_at": timeutil.iso(),
                                             "attempts": st["jobs"][a.job_id].get("attempts", 0) + 1})
            else:
                res = json.loads(a.result) if a.result else None
                before = list(st["rejected_sources"])
                new = finish_job(st, cfg, a.job_id, a.status, a.exit, a.verdict, res, a.note)
                for n in new:
                    print(f"registered {n}")
                rejected = [x for x in st["rejected_sources"] if x not in before]
                slug = (st["jobs"][a.job_id].get("result") or {}).get("slug") or st["jobs"][a.job_id].get("slug")
        elif a.cmd == "pause":
            _pause(st, "operator", a.reason)
        elif a.cmd == "unpause":
            st["paused"] = False
            st["pause_reason"] = None
            st["counters"]["consecutive_failed_slots"] = 0
            st["budget"]["stop_until"] = None
    if rejected:  # outside the state lock: L1's CLI is a separate process
        mark_sources_rejected(rejected, f"{a.job_id}: {a.verdict or a.status}", slug=slug)
    return 0


if __name__ == "__main__":
    sys.exit(main())
