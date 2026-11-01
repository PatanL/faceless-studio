"""Run deterministic operator jobs detached, so the operator never blocks a tool call for more than ~2 minutes.

  python -m pipeline.ops.run start JOB_ID [--dry-run]   # setsid nohup ... exec JOB_ID, returns at once
  python -m pipeline.ops.run auto [--dry-run] [--json]   # register due jobs, start every startable deterministic one
                                                         # (<= 1 heavy (make/fix) + <= 1 light at a time); prints the
                                                         # in-session jobs left for the operator
  python -m pipeline.ops.run reconcile                    # running jobs whose pid is gone -> failed (or resumed)
  python -m pipeline.ops.run plan JOB_ID                  # print the commands a job would run (dry, no state change)
  python -m pipeline.ops.run exec JOB_ID [--dry-run]      # internal: run the job in the foreground

Job handlers call only the lane CLIs of docs/OPERATOR_DESIGN.md (L1 studio-make / pipeline.sources, L2
pipeline.qa.gate, L3 pipeline.publish.*, L4 pipeline.analytics.*). A lane module that is not installed yet makes
the step exit 5 (dependency unavailable), which pauses the loop. --dry-run (or OPS_DRY_RUN=1) logs every command
without running it and finishes the job without changing state.

Publishing mode per platform is decided here, never by the operator: `auto` only when APPROVAL_MODE is auto (env
and data/operator/approval_mode), config.mode.<p> is auto and config.disclosure_ok_auto.<p> is true; else `draft`.
"""
from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import glob
import importlib.util
import json
import os
import shlex
import signal
import subprocess
import sys
import time

from pipeline.common import jsonl, locks, timeutil
from pipeline.ops import paths, state as S

PY = sys.executable or "python3"
HEAVY = {"make", "fix"}
LIGHT = {"publish", "status", "metrics48", "metrics7d", "learning", "killrule", "tiktok_inbox"}
LANE_MODULE = {  # module that must exist for a step, by argv prefix
    "pipeline.sources": "pipeline.sources", "pipeline.qa.gate": "pipeline.qa.gate",
    "pipeline.publish.post": "pipeline.publish.post", "pipeline.publish.status": "pipeline.publish.status",
    "pipeline.analytics.collect": "pipeline.analytics.collect", "pipeline.analytics.align": "pipeline.analytics.align",
    "pipeline.analytics.heatmap": "pipeline.analytics.heatmap", "pipeline.analytics.experiments": "pipeline.analytics.experiments",
    "pipeline.analytics.learning": "pipeline.analytics.learning", "pipeline.analytics.killrule": "pipeline.analytics.killrule",
    "pipeline.analytics.tiktok_import": "pipeline.analytics.tiktok_import",
}


class StepFailed(Exception):
    def __init__(self, code: int, msg: str):
        super().__init__(msg)
        self.code = code


def _have(module: str) -> bool:
    try:
        return importlib.util.find_spec(module) is not None
    except (ImportError, ValueError):
        return False


class Runner:
    """Runs (or, dry, logs) the steps of one job. `fake` maps an argv[2] module/-name to (exit, stdout) for tests."""

    def __init__(self, job_id: str, job: dict, config: dict, log, dry: bool = False, fake=None):
        self.job_id, self.job, self.config, self.log, self.dry, self.fake = job_id, job, config, log, dry, fake
        self.result: dict = {}
        self.cmds: list[list[str]] = []

    def say(self, msg: str):
        self.log.write(f"[{timeutil.iso()}] {msg}\n")
        self.log.flush()

    def sh(self, argv: list[str], timeout_s: float = 1800, ok=(0,), optional=False, capture=False) -> tuple[int, str]:
        argv = [str(x) for x in argv]
        self.cmds.append(argv)
        mod = next((LANE_MODULE[m] for m in LANE_MODULE if m in argv[:3]), None)
        self.say("$ " + " ".join(shlex.quote(x) for x in argv))
        if self.fake is not None:
            key = argv[2] if len(argv) > 2 and argv[1] == "-m" else os.path.basename(argv[0])
            code, out = self.fake(key, argv)
        elif self.dry:
            return 0, ""
        elif mod and not _have(mod):
            code, out = 5, f"lane module {mod} is not installed"
        else:
            code, out = self._exec(argv, timeout_s, capture)
        if code not in ok:
            msg = f"exit {code}: {' '.join(argv[:4])} {out[-400:] if out else ''}".strip()
            self.say(("optional step failed, continuing: " if optional else "FAILED ") + msg)
            if not optional:
                raise StepFailed(code, msg)
        return code, out

    def _exec(self, argv, timeout_s, capture) -> tuple[int, str]:
        env = dict(os.environ, CUDA_VISIBLE_DEVICES="", TZ="America/Chicago", PYTHONUNBUFFERED="1")
        p = subprocess.Popen(argv, cwd=paths.ROOT, env=env, stdout=subprocess.PIPE if capture else self.log,
                             stderr=self.log, text=True, start_new_session=True)
        try:
            out, _ = p.communicate(timeout=timeout_s)
        except subprocess.TimeoutExpired:
            self.say(f"timeout after {timeout_s:.0f}s: killing process group {p.pid}")
            try:
                os.killpg(p.pid, signal.SIGTERM)
                time.sleep(10)
                os.killpg(p.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            p.wait()
            return 1, "timeout"
        if capture and out:
            self.say(out.strip()[-2000:])
        return p.returncode, out or ""

    def detached(self, argv: list[str], result_file: str, wait_s: float = 2400) -> tuple[int, dict]:
        """Start argv in its own session and return as soon as it writes `result_file` with phase created|done, or
        exits. The process may keep running after that (post.py's tunnel hold): it is never killed by this job.
        If neither happens within wait_s, the process group is terminated (SIGTERM first, so post.py closes its
        tunnel) and (1, {}) is returned. -> (exit code, result JSON)."""
        argv = [str(x) for x in argv]
        self.cmds.append(argv)
        mod = next((LANE_MODULE[m] for m in LANE_MODULE if m in argv[:3]), None)
        self.say("$ (detached) " + " ".join(shlex.quote(x) for x in argv))
        with contextlib.suppress(OSError):
            os.unlink(result_file)
        if self.fake is not None:
            key = argv[2] if len(argv) > 2 and argv[1] == "-m" else os.path.basename(argv[0])
            code, _ = self.fake(key, argv)
            return code, _read_json(result_file)
        if self.dry:
            return 0, {}
        if mod and not _have(mod):
            return 5, {}
        env = dict(os.environ, CUDA_VISIBLE_DEVICES="", TZ="America/Chicago", PYTHONUNBUFFERED="1")
        p = subprocess.Popen(argv, cwd=paths.ROOT, env=env, stdout=self.log, stderr=self.log, stdin=subprocess.DEVNULL,
                             text=True, start_new_session=True)
        t_end = time.time() + wait_s
        while time.time() < t_end:
            rc = p.poll()
            res = _read_json(result_file)
            if rc is not None:
                return rc, res
            if res.get("phase") in ("created", "done") and res.get("pid") == p.pid:
                self.say(f"pid {p.pid} reported phase {res['phase']}: leaving it running (hold={res.get('holding')})")
                return int(res.get("exit") or 0), {**res, "hold_pid": p.pid if res.get("holding") else None}
            time.sleep(2)
        self.say(f"no result from pid {p.pid} after {wait_s:.0f}s: terminating its process group")
        with contextlib.suppress(ProcessLookupError):
            os.killpg(p.pid, signal.SIGTERM)
            for _ in range(30):
                if p.poll() is not None:
                    break
                time.sleep(1)
            if p.poll() is None:
                os.killpg(p.pid, signal.SIGKILL)
        p.wait()
        return 1, _read_json(result_file)

    def json_out(self, argv, **kw) -> dict:
        code, out = self.sh(argv, capture=True, **kw)
        if self.dry and self.fake is None:
            return {}
        try:
            return json.loads(out.strip().splitlines()[-1]) if out.strip() else {}
        except (json.JSONDecodeError, IndexError):
            try:
                return json.loads(out)
            except json.JSONDecodeError:
                raise StepFailed(1, f"expected JSON from {' '.join(argv[:4])}")


def _read_json(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


# ---------------------------------------------------------------------------------------------- handlers
def _find_slug(job: dict, since: float) -> str | None:
    if job.get("slug"):
        return job["slug"]
    d8 = job["date"].replace("-", "")
    hits = []
    for f in glob.glob(os.path.join(paths.episodes_dir(), f"op-{d8}-{job['slot']}-*", "make_status.json")):
        if os.path.getmtime(f) >= since - 5:
            hits.append((os.path.getmtime(f), os.path.basename(os.path.dirname(f))))
    return max(hits)[1] if hits else None


def _make_status(slug: str) -> dict:
    try:
        with open(os.path.join(paths.episodes_dir(), slug, "make_status.json"), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def _gate(r: Runner, slug: str) -> str:
    code, _ = r.sh([PY, "-m", "pipeline.qa.gate", slug], ok=(0, 6), timeout_s=1800)
    return "PASS" if code == 0 else "FAIL"


def h_make(r: Runner, st: dict):
    job, cfg = r.job, r.config
    niche = cfg.get("niche", "explainer")
    started = time.time()
    exp = {}
    if r.fake is not None or _have("pipeline.analytics.experiments"):
        exp = r.json_out([PY, "-m", "pipeline.analytics.experiments", "assign", "--date", job["date"], "--slot", job["slot"]])
    else:
        r.say("L4 experiments not installed: making without an experiment arm")
    excl = ",".join(st.get("rejected_sources") or [])
    pick_cmd = [PY, "-m", "pipeline.sources", "pick", "--niche", niche, "--json", "--date", job["date"],
                "--slot", job["slot"]] + (["--exclude", excl] if excl else [])
    pick = r.json_out(pick_cmd, ok=(0,))
    src = (pick.get("source_id") or (pick.get("pick") or {}).get("source_id") or pick.get("id")
           or ("DRYRUN_SOURCE" if r.dry else None))
    if not src:
        raise StepFailed(4, "no source candidate")
    r.result.update({"source_id": src, "experiment_id": exp.get("experiment_id"), "arm": exp.get("arm")})
    cap = int(cfg["budget"]["weighted_tokens_per_video"])
    cmd = ["./studio-make", "--source", src, "--niche", niche, "--slot", job["slot"], "--date", job["date"],
           "--budget-tokens", str(cap)]
    if exp.get("experiment_id") and exp.get("arm"):
        cmd += ["--experiment", f"{exp['experiment_id']}:{exp['arm']}"]
    max_s = float(cfg["budget"].get("max_make_hours", 3)) * 3600
    t0 = time.time()
    try:
        r.sh(cmd, timeout_s=max_s)
    except StepFailed as e:
        slug = _find_slug(job, started)
        ms = _make_status(slug) if slug else {}
        left = max_s - (time.time() - t0)
        if slug:
            r.result["slug"] = slug
        if e.code == 3:
            r.result["budget_cap"] = ms.get("budget_cap") or "video"  # studio-make's cap is per video
        if e.code == 1 and slug and ms.get("step") and left > 600:
            r.say(f"retrying once from step {ms['step']}")
            r.sh(["./studio-make", "--slug", slug, "--from", ms["step"], "--budget-tokens", str(cap)], timeout_s=left)
        else:
            raise
    slug = _find_slug(job, started) or ("op-DRYRUN" if r.dry else None)
    if not slug:
        raise StepFailed(1, "studio-make finished but no episodes/op-<date>-<slot>-*/make_status.json was written")
    r.result["slug"] = slug
    r.result["gate"] = _gate(r, slug)


def h_fix(r: Runner, st: dict):
    slug = r.job["slug"]
    notes = f"episodes/{slug}/review_notes.md"
    if not r.dry and r.fake is None and not os.path.exists(os.path.join(paths.ROOT, notes)):
        raise StepFailed(2, f"{notes} missing: the operator writes it before starting a fix job")
    # studio-make counts a slug's usage across invocations, so a fix round starts from the make's total: give it
    # its own allowance on top of the per-video cap instead of failing on the first claude call
    b = r.config["budget"]
    cap = int(b["weighted_tokens_per_video"]) + int(b.get("fix_round_tokens", 1_000_000))
    r.sh(["./studio-make", "--slug", slug, "--from", "review", "--review-notes", notes, "--budget-tokens", str(cap)],
         timeout_s=float(b.get("max_make_hours", 3)) * 3600)
    r.result.update({"slug": slug, "gate": _gate(r, slug)})


def h_publish(r: Runner, st: dict):
    """One pipeline.publish.post call for every platform (per-platform modes, one URL, one hold), started detached:
    the job ends as soon as the Buffer posts exist; post.py keeps the cloudflared URL up on its own afterwards."""
    job, cfg = r.job, r.config
    slug = job["slug"]
    post_at = timeutil.parse(S.slot_info(cfg, job["date"], job["slot"])["post_at"])
    late = timeutil.now_utc() - post_at
    if late > dt.timedelta(hours=cfg.get("publish_late_h", 2)):
        raise StepFailed(4, f"slot post time {timeutil.iso(post_at)} passed {late} ago; not posting late")
    slot_at = max(post_at, timeutil.now_utc() + dt.timedelta(minutes=20))
    approval = S.approval_mode()
    platforms = cfg.get("platforms", ["youtube", "tiktok", "instagram"])
    modes = {p: S.effective_mode(cfg, p, approval) for p in platforms}
    groups: dict[str, list[str]] = {}
    for p in platforms:
        groups.setdefault(modes[p], []).append(p)
    r.say(f"APPROVAL_MODE={approval}; modes {groups}")
    res_file = os.path.join(paths.ops_dir(), "publish", f"{r.job_id}.json")
    os.makedirs(os.path.dirname(res_file), exist_ok=True)
    code, res = r.detached([PY, "-m", "pipeline.publish.post", slug, "--slot-at", timeutil.iso(slot_at),
                            "--platforms", ",".join(platforms), "--modes", ",".join(f"{p}={modes[p]}" for p in platforms),
                            "--result-file", res_file, "--hold-max-h", str(cfg.get("publish_hold_max_h", 12))],
                           res_file, wait_s=float(cfg.get("publish_wait_s", 2400)))
    created = res.get("created")
    if created is None:  # fake runner / dry plan / a post.py that died before writing: assume all or nothing
        created = platforms if code == 0 else []
    skipped = res.get("skipped_platforms") or []
    failed = [p for p in res.get("failed") or [] if p not in created]
    drafts = [p for p in created if modes.get(p) == "draft"]
    r.result.update({"slug": slug, "slot_at": timeutil.iso(slot_at), "modes": groups, "created": created,
                     "failed": failed, "skipped_platforms": skipped, "dry_run": bool(res.get("dry_run")),
                     "drafts": 0 if res.get("dry_run") else len(drafts), "hold_pid": res.get("hold_pid"),
                     "result_file": res_file})
    if code != 0 and not created:
        raise StepFailed(code, f"pipeline.publish.post exited {code}; no Buffer post was created")
    if r.dry or res.get("dry_run"):
        return
    if code != 0 or failed:
        r.result["partial"] = True
        S.human(f"Publish of `{slug}`: created {', '.join(created) or 'nothing'}, FAILED {', '.join(failed) or '?'} "
                f"(exit {code}). See the job log and data/posts.jsonl; post the missing platform(s) by hand and "
                f"record them with `pipeline.publish.post --record-manual`.", key=f"publish-failed:{slug}", st=st)
    if skipped:
        S.human(f"`{slug}` was not posted to {', '.join(skipped)}: "
                f"{', '.join('BUFFER_CHANNEL_' + p.upper() for p in skipped)} missing in ~/studio/.env.",
                key=f"publish-skipped:{','.join(skipped)}:{timeutil.local_date()}", st=st)
    if drafts:
        loc = timeutil.to_local(slot_at)
        S.human(f"Approve the Buffer drafts for `{slug}` ({', '.join(drafts)}) by {loc:%a %H:%M} "
                f"America/Chicago. In Buffer, set each platform's AI-content toggle before approving. "
                f"Captions: out/{slug}/publish/captions.json. Unapproved drafts count as missed "
                f"{cfg.get('drafts_missed_h', 6)} h after the slot.", key=f"approve:{slug}", st=st)


def h_status(r: Runner, st: dict):
    code, _ = r.sh([PY, "-m", "pipeline.publish.status", "--all-open"], timeout_s=900, ok=(0, 4))
    if r.dry:
        return
    cfg = r.config
    now = timeutil.now_utc()
    for key, p in jsonl.latest(paths.ledger("posts.jsonl"), "post_key").items():
        if p.get("dry_run"):
            continue
        if p.get("mode") == "draft" and p.get("status") == "draft" and p.get("scheduled_at"):
            if now - timeutil.parse(p["scheduled_at"]) > dt.timedelta(hours=cfg.get("drafts_missed_h", 6)):
                S.human(f"Draft `{key}` was not approved within {cfg.get('drafts_missed_h', 6)} h of its slot "
                        f"({p['scheduled_at']}); it counts as missed. Delete or post it in Buffer.",
                        key=f"missed:{key}", st=st)
        if p.get("status") == "failed" and p.get("buffer_post_id"):
            S.human(f"Buffer post `{key}` ({p.get('buffer_post_id')}) went to **failed**: {p.get('error') or 'no error text'}. "
                    f"It will not go out; fix it in Buffer (media fetch? channel?) or post by hand and record it with "
                    f"`pipeline.publish.post --record-manual`.", key=f"failed:{key}", st=st)


def h_metrics(r: Runner, st: dict):
    j = r.job
    r.sh([PY, "-m", "pipeline.analytics.collect", "--post-key", j["post_key"], "--window", j["window"]], timeout_s=900)
    if j.get("slug"):
        r.sh([PY, "-m", "pipeline.analytics.align", j["slug"], "--window", j["window"]], timeout_s=600, optional=True)
    if j["window"] == "7d" and j.get("platform") == "youtube" and j.get("source_id"):
        r.sh([PY, "-m", "pipeline.analytics.heatmap", j["source_id"]], timeout_s=600, optional=True)
        r.sh([PY, "-m", "pipeline.analytics.align", "--source", j["source_id"]], timeout_s=600, optional=True)


def h_learning(r: Runner, st: dict):
    r.sh([PY, "-m", "pipeline.analytics.experiments", "decide"], timeout_s=900)
    r.sh([PY, "-m", "pipeline.analytics.learning", "--week", r.job.get("week") or timeutil.iso_week()], timeout_s=900)


def h_killrule(r: Runner, st: dict):
    r.sh([PY, "-m", "pipeline.analytics.killrule"], timeout_s=600)
    try:
        with open(paths.ledger("killrule.json"), encoding="utf-8") as f:
            r.result["killrule"] = json.load(f)
    except (OSError, json.JSONDecodeError):
        r.result["killrule"] = {}


IMAGE_EXT = (".png", ".jpg", ".jpeg", ".webp")


def h_tiktok_inbox(r: Runner, st: dict):
    """Import every CSV once (`tiktok_import --inbox` moves them to done/ and dedupes rows), then move the
    screenshots a successfully imported `*.screenshot.csv` covered (images not newer than it) to done/ from code.
    Only screenshots still waiting afterwards make a tiktok_screens session job."""
    inbox = os.path.join(paths.data_dir(), "inbox", "tiktok")
    done = os.path.join(inbox, "done")
    csvs = sorted(glob.glob(os.path.join(inbox, "*.csv")))
    screen_csvs = {os.path.basename(f): os.path.getmtime(f) for f in csvs if f.endswith(".screenshot.csv")}
    code = 0
    if csvs:
        code, _ = r.sh([PY, "-m", "pipeline.analytics.tiktok_import", "--inbox"], timeout_s=300, ok=(0, 1))
    moved = 0
    if not r.dry and r.fake is None:
        imported = [m for n, m in screen_csvs.items() if os.path.exists(os.path.join(done, n))]
        if imported:
            upto = max(imported)
            os.makedirs(done, exist_ok=True)
            for f in glob.glob(os.path.join(inbox, "*")):
                if f.lower().endswith(IMAGE_EXT) and os.path.getmtime(f) <= upto + 1:
                    os.replace(f, os.path.join(done, os.path.basename(f)))
                    moved += 1
        if code != 0:
            S.human("TikTok import: some CSVs in data/inbox/tiktok/ failed (moved to data/inbox/tiktok/failed/; see "
                    f"the job log {os.path.join(paths.log_dir(), r.job_id + '.log')}). Fix and drop them again.",
                    key=f"tiktok-import:{timeutil.local_date()}", st=st)
    shots = [f for f in glob.glob(os.path.join(inbox, "*")) if f.lower().endswith(IMAGE_EXT)]
    r.result.update({"csv": len(csvs), "screenshots": len(shots), "screenshots_done": moved, "import_exit": code})


HANDLERS = {"make": h_make, "fix": h_fix, "publish": h_publish, "status": h_status, "metrics48": h_metrics,
            "metrics7d": h_metrics, "learning": h_learning, "killrule": h_killrule, "tiktok_inbox": h_tiktok_inbox}


# ---------------------------------------------------------------------------------------------- exec / start
def execute(job_id: str, dry: bool = False, fake=None, log=None) -> int:
    cfg = S.load_config()
    st = S.load_state()
    job = st["jobs"].get(job_id)
    if not job:
        print(f"unknown job {job_id}", file=sys.stderr)
        return 2
    h = HANDLERS.get(job.get("type"))
    if not h:
        print(f"{job_id}: type {job.get('type')} is an in-session job, not run.py", file=sys.stderr)
        return 2
    own_log = log is None
    log = log or open(os.path.join(paths.log_dir(), f"{job_id}.log"), "a", encoding="utf-8")
    r = Runner(job_id, job, cfg, log, dry=dry, fake=fake)
    r.say(f"=== {job_id} ({job.get('type')}) start{' DRY-RUN' if dry else ''} pid {os.getpid()}")
    code = 0
    note = None
    try:
        if job.get("type") in HEAVY:
            with locks.flock("make", timeout_s=float(cfg["budget"].get("max_make_hours", 3)) * 3600):
                h(r, st)
        else:
            h(r, st)
    except StepFailed as e:
        code, note = e.code, str(e)
    except locks.LockTimeout as e:
        code, note = 1, str(e)
    except Exception as e:  # noqa: BLE001 - recorded, never swallowed silently
        code, note = 1, f"{type(e).__name__}: {e}"
        r.say(note)
    if code == 4 and job.get("type") == "publish":
        status = "skipped"  # the slot's post time passed: not a failure of the video or its source
    else:
        status = "done" if code in (0, 4) and not (code == 4 and job.get("type") == "make") else "failed"
    if code == 3:
        try:
            from pipeline.ops import budget
            r.result["budget_level"] = budget.check(cfg, st)["level"]
        except Exception:  # noqa: BLE001
            pass
    r.say(f"=== {job_id} end exit {code} -> {status} result {json.dumps(r.result)}")
    if not dry:
        with S.updating() as st2:
            # handler-side HUMAN.md dedupe keys were added to the stale copy `st`; carry them over
            st2["notified"] = list(dict.fromkeys(st2["notified"] + st["notified"]))[-500:]
            before = list(st2["rejected_sources"])
            new = S.finish_job(st2, cfg, job_id, status, code, result=r.result, note=note)
            S.journal(f"{job_id}: {status} (exit {code}){' -> ' + ', '.join(new) if new else ''}{' - ' + note[:200] if note else ''}")
            rejected = [x for x in st2["rejected_sources"] if x not in before]
        if fake is None:
            S.mark_sources_rejected(rejected, f"{job_id}: {note or status}"[:200], slug=r.result.get("slug"))
    if own_log:
        log.close()
    return code


def start(job_id: str, dry: bool = False) -> int:
    with S.updating() as st:
        j = st["jobs"].get(job_id)
        if not j:
            print(f"unknown job {job_id} (run `python -m pipeline.ops.due --register` first)", file=sys.stderr)
            return 2
        if j.get("type") not in HANDLERS:
            print(f"{job_id} is an in-session job ({j.get('type')})", file=sys.stderr)
            return 2
        if j.get("status") == "running" and _alive(j.get("pid")):
            print(f"{job_id} already running (pid {j.get('pid')})")
            return 0
        logf = os.path.join(paths.log_dir(), f"{job_id}.log")
        argv = [PY, "-m", "pipeline.ops.run", "exec", job_id] + (["--dry-run"] if dry else [])
        out = open(logf, "a", encoding="utf-8")
        p = subprocess.Popen(["nohup", "nice", "-n", "10"] + argv, cwd=paths.ROOT, stdout=out, stderr=out,
                             stdin=subprocess.DEVNULL, start_new_session=True,
                             env=dict(os.environ, CUDA_VISIBLE_DEVICES="", TZ="America/Chicago"))
        out.close()
        if not dry:
            j.update({"status": "running", "pid": p.pid, "started_at": timeutil.iso(), "log": logf,
                      "attempts": j.get("attempts", 0) + 1})
    print(f"started {job_id} pid {p.pid} log {logf}")
    return 0


def _alive(pid) -> bool:
    if not pid:
        return False
    try:
        os.kill(int(pid), 0)
    except (ProcessLookupError, ValueError, TypeError):
        return False
    except PermissionError:
        return True
    # a zombie child still answers kill(0); check /proc where available
    try:
        with open(f"/proc/{int(pid)}/stat") as f:
            return f.read().split()[2] != "Z"
    except OSError:
        return True


def reconcile() -> list[str]:
    cfg = S.load_config()
    out = []
    with S.updating() as st:
        out += S.reset_stale_session_jobs(st, timeutil.now_utc(), float(cfg.get("session_job_stale_min", 90)))
        for jid, j in st["jobs"].items():
            if j.get("status") != "running" or j.get("type") not in HANDLERS:
                continue
            if _alive(j.get("pid")):
                continue
            S.finish_job(st, cfg, jid, "failed", 1, note="process died without recording an exit (reconciled)")
            out.append(jid)
            S.journal(f"{jid}: reconciled as failed (pid {j.get('pid')} gone)")
    return out


def auto(dry: bool = False) -> dict:
    from pipeline.ops import due as D
    reconcile()
    r = D.register_due()
    st = S.load_state()
    running = [j for j in st["jobs"].values() if j.get("status") == "running" and _alive(j.get("pid"))]
    heavy_busy = any(j.get("type") in HEAVY for j in running)
    light_busy = any(j.get("type") in LIGHT for j in running)
    started, session, waiting = [], [], []
    for j in r["due"]:
        jid, t = j["job_id"], j.get("type")
        cur = st["jobs"].get(jid, {})
        if cur.get("status") != "pending":
            continue
        if t in S.SESSION_JOB_TYPES:
            session.append(jid)
        elif t in HEAVY and not heavy_busy:
            start(jid, dry=dry); started.append(jid); heavy_busy = True
        elif t in LIGHT and not light_busy:
            start(jid, dry=dry); started.append(jid); light_busy = True
        else:
            waiting.append(jid)
    return {"started": started, "session_jobs": session, "waiting": waiting, "expired": [j["job_id"] for j in r["expired"]],
            "makes_blocked": r.get("makes_blocked")}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.ops.run")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for c in ("start", "exec", "plan"):
        p = sub.add_parser(c); p.add_argument("job_id"); p.add_argument("--dry-run", action="store_true")
    p = sub.add_parser("auto"); p.add_argument("--dry-run", action="store_true"); p.add_argument("--json", action="store_true")
    sub.add_parser("reconcile")
    a = ap.parse_args(argv)
    dry = getattr(a, "dry_run", False) or os.environ.get("OPS_DRY_RUN") == "1"
    if a.cmd == "exec":
        return execute(a.job_id, dry=dry)
    if a.cmd == "plan":
        return execute(a.job_id, dry=True, log=sys.stdout)
    if a.cmd == "start":
        return start(a.job_id, dry=dry)
    if a.cmd == "reconcile":
        for j in reconcile():
            print(f"reconciled {j}")
        return 0
    res = auto(dry=dry)
    if a.json:
        print(json.dumps(res, indent=1))
    else:
        for k, v in res.items():
            print(f"{k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
