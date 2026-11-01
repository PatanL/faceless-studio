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
  python -m pipeline.ops.state watchdog --tmux-alive 0|1    # prints none|tick|resume|rotate|backoff; writes HUMAN.md
                                                            # when the heartbeat is > 2 h stale or launches die fast
  python -m pipeline.ops.state watchdog-launched --survived 0|1
"""
from __future__ import annotations

import argparse
import contextlib
import copy
import datetime as dt
import json
import os
import re
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
        "sessions": [],
        "dep_strikes": {},
        "watchdog": {"launches": [], "fast_exits": 0, "next_launch_after": None},
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


def chain_of(j: dict, jid: str = "") -> int:
    """Which source attempt of its slot a job belongs to: 1 for the first make's chain, 2 for make-r2's, ..."""
    if j.get("chain"):
        return int(j["chain"])
    m = re.search(r"-make-r(\d+)$", jid or "")
    return int(m.group(1)) if m else 1


def chain_suffix(chain: int, rnd: int | None = None) -> str | None:
    """Id suffix of a chained job: review/fix/publish of make-r2 are ...-review-s2, ...-fix-s2, ...-publish-s2
    (review round 2 of it: ...-review-s2-r2), so they never collide with the first make's chain."""
    parts = [f"s{chain}"] if chain and chain > 1 else []
    if rnd and rnd > 1:
        parts.append(f"r{rnd}")
    return "-".join(parts) or None


DEP_OF = {"make": "claude", "fix": "claude", "review": "claude", "publish": "buffer", "status": "buffer",
          "metrics48": "analytics", "metrics7d": "analytics", "learning": "analytics", "killrule": "analytics",
          "tiktok_inbox": "analytics"}


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
                      "chain": 2,
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

    dep = DEP_OF.get(t, t or "job")
    if exit_code == 5:
        _dependency_strike(st, config, dep, jid, j, now)
    elif exit_code == 0 and status == "done":
        st.setdefault("dep_strikes", {}).pop(dep, None)
        st["dep_strikes"].pop(f"{dep}:fail1", None)
    elif exit_code == 1 and status == "failed" and t not in ("make", "fix"):
        _light_failure(st, config, dep, jid, j, now)
    budget_hard = False
    if exit_code == 3:
        budget_hard = _budget_stop(st, config, jid, res, now)

    chain = chain_of(j, jid)
    if t in ("make", "fix"):
        if status == "done":
            rnd = 1 if t == "make" else int(j.get("round", 1)) + 1
            register(st, {"job_id": job_id(date, slot, "review", chain_suffix(chain, rnd)), "type": "review",
                          "date": date, "slot": slot, "slug": slug, "round": rnd, "chain": chain,
                          "due_at": timeutil.iso(now),
                          "source_id": res.get("source_id") or j.get("source_id"), "gate": res.get("gate")})
        elif status == "failed" and exit_code == 5:
            st["counters"]["slots_failed"] += 1  # not the source's fault: no reject, the loop is paused/striking
        elif status == "failed" and exit_code == 3 and budget_hard:
            st["counters"]["slots_failed"] += 1  # weekly cap: makes stop until Monday
        elif status == "failed":
            why = (f"{t} hit the per-video token cap (exit 3)" if exit_code == 3 else f"{t} failed (exit {exit_code})")
            slot_failed(st, config, j, why, now)
    elif t == "review" and status == "done":
        rnd = int(j.get("round", 1))
        if verdict == "PASS" and j.get("gate") == "FAIL":  # nothing posts without gate PASS
            verdict = "FIX"
            j["verdict"] = "FIX"
            j["note"] = ((j.get("note") or "") + " review PASS overridden: gate FAIL").strip()
        if verdict == "PASS":
            post_at = timeutil.parse(slot_info(config, date, slot)["post_at"])
            register(st, {"job_id": job_id(date, slot, "publish", chain_suffix(chain)), "type": "publish",
                          "date": date, "slot": slot, "chain": chain, "slug": slug, "due_at": timeutil.iso(now),
                          "source_id": j.get("source_id"),
                          "expires_at": timeutil.iso(post_at + dt.timedelta(hours=config.get("publish_late_h", 2)))})
        elif verdict == "FIX" and rnd <= int(config["budget"].get("max_fix_rounds", 1)):
            register(st, {"job_id": job_id(date, slot, "fix", chain_suffix(chain, rnd)), "type": "fix",
                          "date": date, "slot": slot, "slug": slug, "round": rnd, "chain": chain,
                          "due_at": timeutil.iso(now), "source_id": j.get("source_id")})
        else:
            slot_failed(st, config, j, f"review round {rnd} verdict {verdict or 'none'}", now)
    elif t == "publish":
        _finish_publish(st, config, jid, j, status, exit_code, res, slug, now)
    elif t == "tiktok_inbox" and status == "done" and int(res.get("screenshots", 0)) > 0:
        register(st, {"job_id": job_id(timeutil.local_date(now), None, "tiktok_screens"), "type": "tiktok_screens",
                      "due_at": timeutil.iso(now), "files": int(res["screenshots"])})
    elif t == "killrule" and status == "done":
        act_on_killrule(st, res.get("killrule") or {})
    return sorted(set(st["jobs"]) - before)


def _dependency_strike(st: dict, config: dict, dep: str, jid: str, j: dict, now: dt.datetime) -> None:
    """Exit 5 = a real auth/config failure (401/403, expired login, missing binary): pause after
    dependency_pause_after[dep] such exits in a row for the same dependency within dependency_window_h.
    Short outages are exit 1 and never pause (the next bucket retries)."""
    strikes = st.setdefault("dep_strikes", {})
    win = dt.timedelta(hours=float(config.get("dependency_window_h", 6)))
    lst = [x for x in strikes.get(dep, []) if now - timeutil.parse(x) < win] + [timeutil.iso(now)]
    strikes[dep] = lst[-20:]
    after = config.get("dependency_pause_after") or {}
    need = int(after.get(dep, after.get("default", 2)) if isinstance(after, dict) else after)
    if len(lst) >= max(1, need):
        _pause(st, "dependency_unavailable",
               f"Job `{jid}` exited 5 ({dep}: auth rejected, login expired, or a tool/lane not installed); "
               f"{len(lst)} such failure(s) in {win.total_seconds() / 3600:.0f} h. Log: {j.get('log')}")
    else:
        journal(f"{jid}: dependency {dep} exit 5 ({len(lst)}/{need} before pausing)")


def _light_failure(st: dict, config: dict, dep: str, jid: str, j: dict, now: dt.datetime) -> None:
    """Exit 1 on a light job (network blip, 5xx): count; tell the human after N in a row, never pause."""
    fails = st.setdefault("dep_strikes", {})
    key = f"{dep}:fail1"
    lst = (fails.get(key) or []) + [timeutil.iso(now)]
    fails[key] = lst[-50:]
    n = int(config.get("light_failures_notify", 6))
    if len(lst) >= n:
        human(f"`{dep}` jobs have failed {len(lst)} times in a row (exit 1, e.g. network or 5xx). Last: `{jid}`, "
              f"log {j.get('log')}. The loop keeps retrying; check the dependency if this goes on.",
              key=f"light:{dep}:{timeutil.local_date(now)}", st=st)


def _budget_stop(st: dict, config: dict, jid: str, res: dict, now: dt.datetime) -> bool:
    """Exit 3: the weekly cap (makes stop until Monday) only when budget.check() says hard; studio-make's own
    per-video cap (make_status budget_cap=video) just fails that slot. Returns True for the weekly stop."""
    level = res.get("budget_level")
    if level is None:
        try:
            from pipeline.ops import budget
            level = budget.check(config, st, now)["level"]
        except Exception:  # noqa: BLE001 - unknown -> treat as the per-video cap (never a silent week-long stop)
            level = "unknown"
    if level != "hard":
        journal(f"{jid}: per-video token cap reached (weekly budget {level}); only this slot fails")
        return False
    nxt_monday = timeutil.to_local(now).date() + dt.timedelta(days=7 - timeutil.to_local(now).weekday())
    st["budget"]["stop_until"] = timeutil.iso(timeutil.at_local(nxt_monday.isoformat(), "00:00"))
    human(f"Weekly token budget reached (`{jid}`); makes are paused until {nxt_monday} (metrics keep running).",
          key=f"budget:{timeutil.iso_week(now)}", st=st)
    return True


def live_posts(slug: str | None) -> list[dict]:
    """Latest non-dry-run posts.jsonl rows of a slug that exist in Buffer (or were posted by hand)."""
    if not slug:
        return []
    from pipeline.common import jsonl
    live = {"draft", "scheduled", "sending", "published", "missed", "manual"}
    return [r for r in jsonl.latest(paths.ledger("posts.jsonl"), "post_key").values()
            if r.get("slug") == slug and not r.get("dry_run") and r.get("status") in live]


def _finish_publish(st, config, jid, j, status, exit_code, res, slug, now) -> None:
    c = st["counters"]
    created = res.get("created") or [r.get("platform") for r in live_posts(slug)]
    if status == "done" and res.get("dry_run"):
        journal(f"{jid}: publish was a dry run (Buffer credentials missing); nothing reached Buffer")
        human(f"Publish of `{slug}` ran as a **dry run**: BUFFER_API_KEY / BUFFER_CHANNEL_* are missing in "
              f"~/studio/.env, so nothing was posted. Payloads are in data/posts.jsonl (dry_run rows).",
              key=f"publish-dry:{timeutil.local_date(now)}", st=st)
    elif status == "done":
        c["consecutive_failed_slots"] = 0
        c["slots_posted"] += 1
        c["drafts_created"] += int(res.get("drafts", 0))
    elif status == "skipped":
        journal(f"{jid}: publish skipped ({j.get('note') or 'slot passed'}); source not rejected")
        human(f"`{slug}` passed review but missed its slot ({j.get('note') or 'post time passed'}). It was not "
              f"posted and its source was not rejected; post it by hand or leave it.", key=f"missed-slot:{jid}", st=st)
    elif created:
        # posts exist in Buffer: never reject the source or re-make the slot over a failure after creation
        c["consecutive_failed_slots"] = 0
        c["slots_posted"] += 1
        journal(f"{jid}: publish exited {exit_code} after Buffer posts were created for {created}; not a failed slot")
        human(f"Publish job `{jid}` for `{slug}` exited {exit_code} after creating Buffer posts for "
              f"{', '.join(created)}. Check them in Buffer (and the job log {j.get('log')}).",
              key=f"publish-partial:{jid}", st=st)
    elif exit_code != 5 and not (exit_code == 3):
        slot_failed(st, config, j, f"publish failed (exit {exit_code})", now)


def reset_stale_session_jobs(st: dict, now: dt.datetime, max_min: float = 90, max_attempts: int = 2) -> list[str]:
    """In-session jobs (review, tiktok_screens) left `running` by a session that died: back to pending (attempt
    counted) after max_min, failed after max_attempts. Returns the ids changed."""
    out = []
    for jid, j in list(st["jobs"].items()):  # slot_failed may register a retry make
        if j.get("type") not in SESSION_JOB_TYPES or j.get("status") != "running":
            continue
        since = j.get("started_at")
        if since and (now - timeutil.parse(since)).total_seconds() < max_min * 60:
            continue
        if int(j.get("attempts", 0)) >= max_attempts:
            j.update({"status": "failed", "finished_at": timeutil.iso(now),
                      "note": f"session job running > {max_min:.0f} min {j.get('attempts')} times (session died?)"})
            journal(f"{jid}: stale session job failed after {j.get('attempts')} attempts")
            if j.get("type") == "review" and j.get("slot"):
                config = load_config()
                slot_failed(st, config, j, "review never finished (stale session job)", now)
        else:
            j.update({"status": "pending", "due_at": timeutil.iso(now),
                      "note": f"reset: running > {max_min:.0f} min without an end (attempt {j.get('attempts', 0)})"})
            journal(f"{jid}: stale session job reset to pending")
        out.append(jid)
    return out


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
        nxt = (st.get("watchdog") or {}).get("next_launch_after")
        if nxt and now < timeutil.parse(nxt):
            return "backoff"
        return "resume"
    tz = timeutil.ZoneInfo(config.get("tz", "America/Chicago"))
    sess = st.get("session") or {}
    busy = sess.get("busy")
    busy_fresh = bool(busy) and (now - timeutil.parse(busy["since"])).total_seconds() < 3600
    running_session_jobs = any(
        j.get("status") == "running" and j.get("type") in SESSION_JOB_TYPES and j.get("started_at")
        and (now - timeutil.parse(j["started_at"])).total_seconds() < 90 * 60 for j in st["jobs"].values())
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


WATCHDOG_FAST_EXIT_N = 3
WATCHDOG_STALE_H = 2.0


def watchdog_launched(st: dict, survived: bool, now: dt.datetime) -> int:
    """Record a resume/rotate launch the watchdog made and whether the session was still alive ~2 min later.
    After WATCHDOG_FAST_EXIT_N fast exits in a row, back off: 30 min, 1 h, 2 h, ... up to 4 h. Returns the streak."""
    wd = st.setdefault("watchdog", {"launches": [], "fast_exits": 0, "next_launch_after": None})
    wd["launches"] = (wd.get("launches") or [])[-19:] + [timeutil.iso(now)]
    if survived:
        wd["fast_exits"] = 0
        wd["next_launch_after"] = None
        return 0
    wd["fast_exits"] = int(wd.get("fast_exits", 0)) + 1
    n = wd["fast_exits"]
    if n >= WATCHDOG_FAST_EXIT_N:
        wait_min = min(240, 30 * 2 ** (n - WATCHDOG_FAST_EXIT_N))
        wd["next_launch_after"] = timeutil.iso(now + dt.timedelta(minutes=wait_min))
    return n


def watchdog_notes(config: dict, st: dict, now: dt.datetime, stopped: bool = False) -> list[tuple[str, str]]:
    """(key, text) HUMAN.md entries the watchdog should write (deduped by key). Pure."""
    if stopped:
        return []
    out = []
    day = timeutil.local_date(now)
    wd = st.get("watchdog") or {}
    n = int(wd.get("fast_exits", 0))
    if n >= WATCHDOG_FAST_EXIT_N:
        out.append((f"watchdog:fast-exit:{day}",
                    f"The operator session died within 2 minutes of launch {n} times in a row (expired claude login, "
                    f"usage/rate limit, or a missing allowlist: `scripts/operator_tmux.sh status`, and "
                    f"~/studio/logs/operator/watchdog.log). The watchdog now waits until "
                    f"{wd.get('next_launch_after')} between launches. Makes and slots are being skipped."))
    hb = (st.get("session") or {}).get("heartbeat_at")
    if hb and (now - timeutil.parse(hb)).total_seconds() > WATCHDOG_STALE_H * 3600:
        age = (now - timeutil.parse(hb)).total_seconds() / 3600
        out.append((f"watchdog:stale:{day}",
                    f"The operator heartbeat is {age:.1f} h old (session down or stuck). Due jobs are not being "
                    f"handled; makes expire and slots are skipped. `scripts/operator_tmux.sh status` / `attach`."))
    return out


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
    p = sub.add_parser("watchdog-launched", help="watchdog: a launch it made was (not) alive ~2 min later")
    p.add_argument("--survived", type=int, required=True)
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
        stopped = os.path.exists(paths.stopped_flag())
        jobs = due_mod.due_from_disk(cfg, st, now)
        notes = watchdog_notes(cfg, st, now, stopped)
        if notes:
            with updating() as s2:
                for key, text in notes:
                    human(text, key=key, st=s2)
        print(watchdog_action(cfg, st, bool(a.tmux_alive), jobs, now, stopped=stopped))
        return 0
    if a.cmd == "watchdog-launched":
        with updating() as s2:
            n = watchdog_launched(s2, bool(a.survived), timeutil.now_utc())
            for key, text in watchdog_notes(cfg, s2, timeutil.now_utc()):
                human(text, key=key, st=s2)
        print(f"fast exits in a row: {n}")
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
            # every session id, so budget.py can measure real usage from the transcripts
            st["sessions"] = ([x for x in st.get("sessions", []) if x.get("id") != a.id]
                              + [{"id": a.id, "started_at": now}])[-30:]
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
