"""L5 operator: pipeline.common, pipeline.ops (state, due, run, budget, guard) and the operator shell scripts.

No network, no tmux, no claude: run.py is driven with a fake command runner, the shell scripts with stub binaries.
"""
import copy
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from _util import ROOT  # noqa: F401  (puts the repo on sys.path)

from pipeline.common import env, jsonl, locks, timeutil
from pipeline.ops import budget, due as D, guard, run as R, state as S

UTC = dt.timezone.utc


class Tmp(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="l5test")
        self.old = {k: os.environ.get(k) for k in ("STUDIO_DATA", "STUDIO_EPISODES", "OPERATOR_LOG_DIR", "STUDIO_LOCKS",
                                                    "APPROVAL_MODE", "STUDIO_ENV_FILE")}
        os.environ.update(STUDIO_DATA=os.path.join(self.tmp, "data"), STUDIO_EPISODES=os.path.join(self.tmp, "episodes"),
                          OPERATOR_LOG_DIR=os.path.join(self.tmp, "logs"), STUDIO_LOCKS=os.path.join(self.tmp, "locks"),
                          STUDIO_ENV_FILE=os.path.join(self.tmp, "env"))
        os.environ.pop("APPROVAL_MODE", None)
        S.init()
        self.cfg = S.load_config()

    def tearDown(self):
        for k, v in self.old.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        shutil.rmtree(self.tmp, ignore_errors=True)


class TestCommon(Tmp):
    def test_jsonl_latest_and_bad_line(self):
        p = os.path.join(self.tmp, "x.jsonl")
        jsonl.append(p, {"k": "a", "n": 1})
        with open(p, "a") as f:
            f.write("{broken\n")
        jsonl.append(p, {"k": "a", "n": 2})
        rows = jsonl.read(p)
        self.assertEqual([r["n"] for r in rows], [1, 2])
        self.assertTrue(all(r["v"] == 1 and r["at"].endswith("Z") for r in rows))
        self.assertEqual(jsonl.latest(p, "k")["a"]["n"], 2)
        self.assertEqual(jsonl.read(os.path.join(self.tmp, "missing.jsonl")), [])

    def test_env_require_and_redact(self):
        with open(os.environ["STUDIO_ENV_FILE"], "w") as f:
            f.write("# comment\nBUFFER_API_KEY='abc123secret'\nEMPTY=\nX=1 # note\n$(rm -rf /)=no\n")
        vals, missing = env.require(["BUFFER_API_KEY", "EMPTY", "X", "YT_CHANNEL_ID"])
        self.assertEqual(vals, {"BUFFER_API_KEY": "abc123secret", "X": "1"})
        self.assertEqual(missing, ["EMPTY", "YT_CHANNEL_ID"])
        self.assertEqual(env.redact("Bearer abc123secret!"), "Bearer ***!")
        self.assertIn("DRY-RUN: missing EMPTY,YT_CHANNEL_ID", env.dry_run_notice(missing))

    def test_time_dst(self):
        # 2026-11-01 is the DST change in America/Chicago: 06:30 CST = 12:30 UTC; a week earlier CDT = 11:30 UTC
        self.assertEqual(timeutil.iso(timeutil.at_local("2026-11-02", "06:30")), "2026-11-02T12:30:00Z")
        self.assertEqual(timeutil.iso(timeutil.at_local("2026-10-26", "06:30")), "2026-10-26T11:30:00Z")
        self.assertEqual(timeutil.local_date(timeutil.parse("2026-11-03T04:00:00Z")), "2026-11-02")
        self.assertEqual(timeutil.iso_week(timeutil.parse("2026-11-02T18:00:00Z")), "2026-W45")

    def test_lock_excludes(self):
        with locks.flock("t1"):
            with self.assertRaises(locks.LockTimeout):
                with locks.flock("t1", timeout_s=0):
                    pass
        with locks.flock("t2", shared=True):
            with locks.flock("t2", shared=True, timeout_s=0):
                pass


# ---------------------------------------------------------------------------------------------- simulated calendar
class TestDueCalendar(Tmp):
    """10 simulated days at 10-minute ticks with a fake world: makes finish, reviews pass, posts publish at the slot,
    metrics get collected when due. Checks timing, counts and idempotency (restart = reload state from JSON)."""

    def test_ten_days(self):
        cfg = self.cfg
        st = S.default_state()
        posts, metrics = {}, []
        start = timeutil.at_local("2026-11-02", "04:00")  # a Monday
        now = start
        seen = []          # (job_id, type, time it became due)
        published = {}     # post_key -> published_at
        while now < start + dt.timedelta(days=10):
            for _ in range(6):  # one tick: keep handling until the chain (make -> review -> publish) settles
                r = D.due_jobs(cfg, st, posts, metrics, now, {"budget": "ok", "tiktok_inbox": 0})
                if not r["due"]:
                    break
                for j in r["new"]:
                    self.assertTrue(S.register(st, j))
                self._handle(cfg, st, r["due"], posts, metrics, published, seen, now)
            # restart: the state survives as JSON and a second due() at the same instant adds nothing
            st = json.loads(json.dumps(st))
            again = D.due_jobs(cfg, st, posts, metrics, now, {"budget": "ok"})
            self.assertEqual(again["new"], [], f"duplicates after restart at {now}")
            self.assertEqual([j["job_id"] for j in again["due"]], [], f"jobs due twice at {now}")
            now += dt.timedelta(minutes=10)
        self._check(seen, published)

    def _handle(self, cfg, st, due, posts, metrics, published, seen, now):
            for j in due:
                jid, t = j["job_id"], j["type"]
                seen.append((jid, t, now))
                if t == "make":
                    slug = f"op-{j['date'].replace('-', '')}-{j['slot']}-topic"
                    S.finish_job(st, cfg, jid, "done", 0, result={"slug": slug, "gate": "PASS", "source_id": "src" + jid}, now=now)
                elif t == "review":
                    S.finish_job(st, cfg, jid, "done", verdict="PASS", now=now)
                elif t == "publish":
                    S.finish_job(st, cfg, jid, "done", 0, result={"drafts": 0}, now=now)
                    post_at = timeutil.parse(S.slot_info(cfg, j["date"], j["slot"])["post_at"])
                    for p in ("youtube", "tiktok", "instagram"):
                        key = f"{j['slug']}:{p}"
                        posts[key] = {"post_key": key, "slug": j["slug"], "platform": p, "status": "scheduled",
                                      "scheduled_at": timeutil.iso(post_at), "source_id": "s"}
                elif t == "status":
                    for key, p in posts.items():
                        if p["status"] == "scheduled" and timeutil.parse(p["scheduled_at"]) <= now:
                            p.update(status="published", published_at=p["scheduled_at"])
                            published[key] = timeutil.parse(p["scheduled_at"])
                    S.finish_job(st, cfg, jid, "done", 0, now=now)
                elif t in ("metrics48", "metrics7d"):
                    metrics.append({"post_key": j["post_key"], "window": j["window"], "platform": j["platform"]})
                    S.finish_job(st, cfg, jid, "done", 0, now=now)
                else:
                    S.finish_job(st, cfg, jid, "done", 0, now=now)

    def _check(self, seen, published):
        ids = [s[0] for s in seen]
        self.assertEqual(len(ids), len(set(ids)), "a job ran twice")
        makes = [s for s in seen if s[1] == "make"]
        self.assertEqual(len(makes), 20)  # 2 per day
        for jid, _, t in makes:
            loc = timeutil.to_local(t)
            self.assertIn(f"{loc:%H:%M}", ("06:30", "08:50"), jid)  # 08:45 falls between 10-min ticks
        self.assertEqual(len([s for s in seen if s[1] == "publish"]), 20)
        learn = [s for s in seen if s[1] == "learning"]
        self.assertEqual([timeutil.local_date(s[2]) for s in learn], ["2026-11-02", "2026-11-09"])
        self.assertEqual(len([s for s in seen if s[1] == "killrule"]), 2)
        # metrics: only youtube + instagram, at published + 48 h / 7 d (within one tick + one status bucket)
        m48 = [s for s in seen if s[1] == "metrics48"]
        m7 = [s for s in seen if s[1] == "metrics7d"]
        self.assertTrue(m48 and m7)
        self.assertFalse([s for s in m48 + m7 if ":tiktok" in s[0]])
        for jid, t, when in m48 + m7:
            key = jid.split("-", 3)[3]
            want = published[key] + dt.timedelta(hours=48 if t == "metrics48" else 168)
            self.assertTrue(dt.timedelta(0) <= when - want < dt.timedelta(minutes=10), (jid, when, want))
        # posts published on days 1-8 reach 7 d inside the window: (8 days * 2 slots) * 2 platforms at most
        self.assertGreaterEqual(len(m7), 2 * 2 * 2)

    def test_paused_and_budget(self):
        now = timeutil.at_local("2026-11-02", "07:40")
        st = S.default_state()
        r = D.due_jobs(self.cfg, st, {}, [], now, {"budget": "ok"})
        self.assertIn("20261102-a-make", [j["job_id"] for j in r["due"]])
        st["paused"] = True
        r = D.due_jobs(self.cfg, st, {}, [], now, {"budget": "ok"})
        self.assertNotIn("make", [j["type"] for j in r["due"]])
        self.assertIn("learning", [j["type"] for j in r["due"]])  # learning still runs while paused
        st["paused"] = False
        later = timeutil.at_local("2026-11-02", "08:50")
        r = D.due_jobs(self.cfg, st, {}, [], later, {"budget": "ok"})
        self.assertEqual([j["slot"] for j in r["due"] if j["type"] == "make"], ["b"])
        r = D.due_jobs(self.cfg, st, {}, [], later, {"budget": "soft"})
        self.assertEqual([j["slot"] for j in r["due"] if j["type"] == "make"], [])  # soft: one video per day (slot a only)
        r = D.due_jobs(self.cfg, st, {}, [], later, {"budget": "hard"})
        self.assertFalse([j for j in r["due"] if j["type"] == "make"])

    def test_make_expires_when_too_late(self):
        st = S.default_state()
        now = timeutil.at_local("2026-11-02", "09:00")  # slot a posts 11:30, deadline 08:30
        r = D.due_jobs(self.cfg, st, {}, [], now, {"budget": "ok"})
        self.assertIn("20261102-a-make", [j["job_id"] for j in r["expired"]])
        self.assertIn("20261102-b-make", [j["job_id"] for j in r["due"]])

    def test_learning_catch_up_window(self):
        st = S.default_state()
        wed = timeutil.at_local("2026-11-04", "09:00")
        self.assertIn("20261102-na-learning", [j["job_id"] for j in D.due_jobs(self.cfg, st, {}, [], wed, {})["due"]])
        sun = timeutil.at_local("2026-11-08", "09:00")
        self.assertNotIn("20261102-na-learning", [j["job_id"] for j in D.due_jobs(self.cfg, st, {}, [], sun, {})["due"]])

    def test_killrule_every_fifth_row(self):
        st = S.default_state()
        now = timeutil.at_local("2026-11-04", "12:00")
        rows = [{"post_key": f"p{i}:youtube", "platform": "youtube", "window": "7d"} for i in range(30)]
        ids = [j["job_id"] for j in D.due_jobs(self.cfg, st, {}, rows, now, {})["due"]]
        self.assertIn("20261104-na-killrule-n30", ids)
        st["killrule"]["last_n"] = 30
        rows += [{"post_key": f"q{i}:youtube", "platform": "youtube", "window": "7d"} for i in range(4)]
        ids = [j["job_id"] for j in D.due_jobs(self.cfg, st, {}, rows, now, {})["due"]]
        self.assertFalse([i for i in ids if "killrule-n" in i])


class TestChain(Tmp):
    def _make_job(self, st, date="2026-11-02", slot="a", suffix=None):
        jid = S.job_id(date, slot, "make", suffix)
        S.register(st, {"job_id": jid, "type": "make", "date": date, "slot": slot, "due_at": "2026-11-02T12:30:00Z"})
        return jid

    def test_fix_round_then_fail_then_retry_then_pause(self):
        cfg, st = self.cfg, S.default_state()
        t = timeutil.at_local("2026-11-02", "07:30")
        jid = self._make_job(st)
        new = S.finish_job(st, cfg, jid, "done", 0, result={"slug": "op-20261102-a-x", "gate": "FAIL", "source_id": "AAA"}, now=t)
        self.assertEqual(new, ["20261102-a-review"])
        self.assertEqual(S.finish_job(st, cfg, "20261102-a-review", "done", verdict="FIX", now=t), ["20261102-a-fix"])
        self.assertEqual(S.finish_job(st, cfg, "20261102-a-fix", "done", 0, result={"gate": "PASS"}, now=t), ["20261102-a-review-r2"])
        # round 2 FIX is final (max_fix_rounds 1): source rejected, retry with the next source (4 h left)
        self.assertEqual(S.finish_job(st, cfg, "20261102-a-review-r2", "done", verdict="FIX", now=t), ["20261102-a-make-r2"])
        self.assertEqual(st["rejected_sources"], ["AAA"])
        # the retry fails too: the slot counts as failed
        S.finish_job(st, cfg, "20261102-a-make-r2", "failed", 1, now=t)
        self.assertEqual(st["counters"]["consecutive_failed_slots"], 1)
        self.assertFalse(st["paused"])
        # slot b fails with no time left -> second failed slot in a row -> pause + HUMAN.md
        jb = self._make_job(st, slot="b")
        S.finish_job(st, cfg, jb, "failed", 1, now=timeutil.at_local("2026-11-02", "16:00"))
        self.assertTrue(st["paused"])
        self.assertEqual(st["pause_reason"], "two_failed_slots")
        with open(os.path.join(os.environ["STUDIO_DATA"], "operator", "HUMAN.md")) as f:
            self.assertIn("two_failed_slots", f.read())

    def test_review_pass_with_gate_fail_becomes_fix(self):
        cfg, st = self.cfg, S.default_state()
        jid = self._make_job(st)
        S.finish_job(st, cfg, jid, "done", 0, result={"slug": "op-20261102-a-x", "gate": "FAIL", "source_id": "A"},
                     now=timeutil.at_local("2026-11-02", "07:30"))
        new = S.finish_job(st, cfg, "20261102-a-review", "done", verdict="PASS", now=timeutil.at_local("2026-11-02", "07:40"))
        self.assertEqual(new, ["20261102-a-fix"])

    def test_exit5_pauses_and_killrule_stop_pauses(self):
        cfg, st = self.cfg, S.default_state()
        jid = self._make_job(st)
        S.finish_job(st, cfg, jid, "failed", 5, note="claude auth")
        self.assertEqual(st["pause_reason"], "dependency_unavailable")
        st2 = S.default_state()
        S.register(st2, {"job_id": "20261109-na-killrule", "type": "killrule", "due_at": "x"})
        S.finish_job(st2, cfg, "20261109-na-killrule", "done", 0,
                     result={"killrule": {"verdict": "stop", "n_videos": 30, "median_views_7d": 900}})
        self.assertTrue(st2["paused"])
        self.assertEqual(st2["pause_reason"], "kill_rule")
        st3 = S.default_state()
        S.act_on_killrule(st3, {"verdict": "extend", "n_videos": 30})
        self.assertFalse(st3["paused"])
        self.assertEqual(st3["killrule"]["last_n"], 30)


class TestApprovalAndWatchdog(Tmp):
    def test_effective_mode_needs_all_three(self):
        cfg = copy.deepcopy(self.cfg)
        cfg["mode"]["youtube"] = "auto"
        cfg["disclosure_ok_auto"]["youtube"] = True
        self.assertEqual(S.effective_mode(cfg, "youtube", "drafts"), "draft")
        self.assertEqual(S.effective_mode(cfg, "youtube", "auto"), "auto")
        self.assertEqual(S.effective_mode(cfg, "tiktok", "auto"), "draft")
        cfg["mode"]["tiktok"] = "auto"
        self.assertEqual(S.effective_mode(cfg, "tiktok", "auto"), "draft")  # disclosure not confirmed
        # approval_mode: env AND file must both say auto
        os.environ["APPROVAL_MODE"] = "auto"
        self.assertEqual(S.approval_mode(), "drafts")
        with open(os.path.join(os.environ["STUDIO_DATA"], "operator", "approval_mode"), "w") as f:
            f.write("auto\n")
        self.assertEqual(S.approval_mode(), "auto")
        os.environ["APPROVAL_MODE"] = "drafts"
        self.assertEqual(S.approval_mode(), "drafts")

    def test_watchdog(self):
        cfg, st = self.cfg, S.default_state()
        now = timeutil.at_local("2026-11-02", "04:20")
        st["session"].update(started_at=timeutil.iso(now - dt.timedelta(hours=20)), heartbeat_at=timeutil.iso(now))
        self.assertEqual(S.watchdog_action(cfg, st, False, [], now), "resume")
        self.assertEqual(S.watchdog_action(cfg, st, False, [], now, stopped=True), "none")
        self.assertEqual(S.watchdog_action(cfg, st, True, [], now), "rotate")
        st["session"]["busy"] = {"what": "review", "since": timeutil.iso(now - dt.timedelta(minutes=5))}
        self.assertEqual(S.watchdog_action(cfg, st, True, [], now), "none")
        st["session"]["busy"] = None
        st["session"]["started_at"] = timeutil.iso(now - dt.timedelta(minutes=10))  # already rotated today
        self.assertEqual(S.watchdog_action(cfg, st, True, [], now), "none")
        st["session"]["heartbeat_at"] = timeutil.iso(now - dt.timedelta(minutes=50))
        self.assertEqual(S.watchdog_action(cfg, st, True, [{"job_id": "x"}], now), "tick")
        self.assertEqual(S.watchdog_action(cfg, st, True, [], now), "none")


class TestGuard(unittest.TestCase):
    APP = "/home/u/studio/app"

    def bash(self, c, appr="drafts"):
        return guard.decide({"tool_name": "Bash", "tool_input": {"command": c}}, appr, self.APP)

    def test_drafts_blocks_auto_posting(self):
        self.assertIsNotNone(self.bash("python -m pipeline.publish.post op-1 --slot-at T --mode auto"))
        self.assertIsNotNone(self.bash("python -m pipeline.publish.post op-1 --slot-at T"))
        self.assertIsNotNone(self.bash("APPROVAL_MODE=auto python -m pipeline.ops.run start 20261102-a-publish"))
        self.assertIsNone(self.bash("python -m pipeline.publish.post op-1 --slot-at T --mode draft"))
        self.assertIsNone(self.bash("python -m pipeline.ops.run start 20261102-a-publish"))
        self.assertIsNone(self.bash("python -m pipeline.publish.post op-1 --slot-at T --mode auto", "auto"))

    def test_always_blocked(self):
        for c in ["scripts/operator_ctl.sh mode youtube auto", "cat ~/studio/.env", "crontab -l", "git push",
                  "python -m pipeline.ops.state unpause", "curl https://api.buffer.com/graphql",
                  "echo '{}' > data/posts.jsonl", "rm data/metrics.jsonl", "sed -i s/draft/auto/ data/operator/config.json",
                  "scripts/operator_tmux.sh rotate", "claude --dangerously-skip-permissions"]:
            self.assertIsNotNone(self.bash(c, "auto"), c)
        for c in ["tail -3 data/posts.jsonl", "cat data/operator/config.json", "source ~/studio/.venv/bin/activate",
                  "python -m pipeline.ops.due", "scripts/operator_tmux.sh status"]:
            self.assertIsNone(self.bash(c), c)

    def test_writes_limited_to_operator_outputs(self):
        w = lambda p: guard.decide({"tool_name": "Write", "tool_input": {"file_path": p}}, "drafts", self.APP)
        self.assertIsNone(w(self.APP + "/out/op-20261102-a-x/qa/review.json"))
        self.assertIsNone(w(self.APP + "/episodes/op-20261102-a-x/review_notes.md"))
        self.assertIsNone(w("/tmp/scratch.txt"))
        for p in ["/data/operator/config.json", "/pipeline/make.py", "/research/corpus/explainer/PLAYBOOK.md",
                  "/data/posts.jsonl", "/episodes/explainer-orca/script.md", "/pipeline/ops/guard.py"]:
            self.assertIsNotNone(w(self.APP + p), p)
        self.assertIsNotNone(guard.decide({"tool_name": "Read", "tool_input": {"file_path": "/home/u/studio/.env"}}, "auto", self.APP))

    def test_settings_and_hook_cli(self):
        s = guard.build_settings("drafts", self.APP, {"_comment": "x", "permissions": {"allow": ["Read"], "defaultMode": "bypassPermissions"}})
        self.assertNotIn("_comment", s)
        self.assertNotIn("defaultMode", s["permissions"])
        self.assertEqual(s["env"]["APPROVAL_MODE"], "drafts")
        cmd = s["hooks"]["PreToolUse"][-1]["hooks"][0]["command"]
        self.assertIn("guard.py hook --approval drafts", cmd)
        me = os.path.join(ROOT, "pipeline", "ops", "guard.py")
        ev = json.dumps({"tool_name": "Bash", "tool_input": {"command": "python -m pipeline.publish.post x --mode auto"}})
        p = subprocess.run([sys.executable, "-I", me, "hook", "--approval", "drafts"], input=ev, text=True, capture_output=True)
        self.assertEqual(p.returncode, 2)
        self.assertIn("BLOCKED", p.stderr)
        ev = json.dumps({"tool_name": "Bash", "tool_input": {"command": "python -m pipeline.ops.due"}})
        p = subprocess.run([sys.executable, "-I", me, "hook", "--approval", "drafts"], input=ev, text=True, capture_output=True)
        self.assertEqual(p.returncode, 0)


class TestRunHandlers(Tmp):
    def fake(self, calls):
        eps = os.environ["STUDIO_EPISODES"]

        def f(key, argv):
            calls.append(argv)
            if key == "pipeline.analytics.experiments":
                return 0, json.dumps({"experiment_id": "EXP-001", "arm": "treatment", "variables": {"hook.type": "H6"}})
            if key == "pipeline.sources":
                return 0, json.dumps({"source_id": "fGcgWaswMns"})
            if key == "studio-make":
                d = argv[argv.index("--date") + 1].replace("-", "")
                slot = argv[argv.index("--slot") + 1]
                ep = os.path.join(eps, f"op-{d}-{slot}-sperm-whale")
                os.makedirs(ep, exist_ok=True)
                with open(os.path.join(ep, "make_status.json"), "w") as fh:
                    json.dump({"slug": os.path.basename(ep), "status": "done", "started_at": timeutil.iso(),
                               "usage_total": {"weighted_tokens": 1200000}}, fh)
                return 0, ""
            if key == "pipeline.qa.gate":
                return 6, ""
            return 0, ""
        return f

    def test_make_chain_commands(self):
        date = timeutil.local_date()
        with S.updating() as st:
            st["rejected_sources"] = ["OLD1"]
            S.register(st, {"job_id": S.job_id(date, "a", "make"), "type": "make", "date": date, "slot": "a", "due_at": timeutil.iso()})
        calls = []
        code = R.execute(S.job_id(date, "a", "make"), fake=self.fake(calls))
        self.assertEqual(code, 0)
        flat = [" ".join(c) for c in calls]
        self.assertIn("experiments assign --date " + date + " --slot a", flat[0])
        self.assertIn("pipeline.sources pick --niche explainer --json --exclude OLD1", flat[1])
        self.assertTrue(flat[2].startswith("./studio-make --source fGcgWaswMns --niche explainer --slot a --date " + date))
        self.assertIn("--experiment EXP-001:treatment", flat[2])
        self.assertIn("--budget-tokens 2500000", flat[2])
        self.assertIn("pipeline.qa.gate op-", flat[3])
        st = S.load_state()
        j = st["jobs"][S.job_id(date, "a", "make")]
        self.assertEqual((j["status"], j["result"]["gate"], j["result"]["source_id"]), ("done", "FAIL", "fGcgWaswMns"))
        self.assertIn(S.job_id(date, "a", "review"), st["jobs"])
        self.assertEqual(budget.check(self.cfg, st)["make"], 1200000)

    def _publish(self, approval_file=None, env_mode=None, cfg_auto=False):
        tomorrow = (timeutil.to_local().date() + dt.timedelta(days=1)).isoformat()
        if cfg_auto:
            cp = os.path.join(os.environ["STUDIO_DATA"], "operator", "config.json")
            with open(cp) as f:
                cfg = json.load(f)
            cfg["mode"]["youtube"] = "auto"; cfg["disclosure_ok_auto"]["youtube"] = True
            cfg["mode"]["tiktok"] = "auto"  # disclosure not confirmed -> stays draft
            with open(cp, "w") as f:
                json.dump(cfg, f)
        if approval_file:
            with open(os.path.join(os.environ["STUDIO_DATA"], "operator", "approval_mode"), "w") as f:
                f.write(approval_file)
        if env_mode:
            os.environ["APPROVAL_MODE"] = env_mode
        jid = S.job_id(tomorrow, "b", "publish")
        with S.updating() as st:
            S.register(st, {"job_id": jid, "type": "publish", "date": tomorrow, "slot": "b", "slug": "op-x", "due_at": timeutil.iso()})
        calls = []
        self.assertEqual(R.execute(jid, fake=lambda k, a: (calls.append(a), (0, ""))[1]), 0)
        return [" ".join(c) for c in calls]

    def test_publish_drafts_by_default(self):
        flat = self._publish(cfg_auto=True)  # config says auto, but APPROVAL_MODE is unset (drafts)
        self.assertEqual(len(flat), 1)
        self.assertIn("--platforms youtube,tiktok,instagram --mode draft", flat[0])
        with open(os.path.join(os.environ["STUDIO_DATA"], "operator", "HUMAN.md")) as f:
            self.assertIn("Approve the Buffer drafts for `op-x`", f.read())

    def test_publish_auto_only_where_all_switches_agree(self):
        flat = self._publish(approval_file="auto", env_mode="auto", cfg_auto=True)
        self.assertIn("--platforms tiktok,instagram --mode draft", flat[0])
        self.assertIn("--platforms youtube --mode auto", flat[1])

    def test_dry_run_and_missing_lane(self):
        date = timeutil.local_date()
        jid = S.job_id(date, "a", "make")
        with S.updating() as st:
            S.register(st, {"job_id": jid, "type": "make", "date": date, "slot": "a", "due_at": timeutil.iso()})
        with open(os.path.join(self.tmp, "plan.log"), "w+") as log:
            self.assertEqual(R.execute(jid, dry=True, log=log), 0)
            log.seek(0)
            txt = log.read()
        self.assertIn("./studio-make --source DRYRUN_SOURCE", txt)
        self.assertEqual(S.load_state()["jobs"][jid]["status"], "pending")  # dry-run changes no state
        # real run without the L1 lane installed -> exit 5 -> loop paused
        if not R._have("pipeline.sources"):
            self.assertEqual(R.execute(jid), 5)
            self.assertEqual(S.load_state()["pause_reason"], "dependency_unavailable")


class TestShell(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="l5sh")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def env(self, **kw):
        e = dict(os.environ, OPERATOR_REMOTE="0", STUDIO_APP=ROOT, STUDIO_DATA=os.path.join(self.tmp, "data"),
                 OPERATOR_SETTINGS=os.path.join(ROOT, "scripts", "operator_settings.example.json"),
                 HOME=self.tmp, CLAUDE_BIN="/bin/echo")
        e.pop("APPROVAL_MODE", None)
        e.update(kw)
        return e

    def sh(self, *args, **kw):
        return subprocess.run(["bash", os.path.join(ROOT, "scripts", "operator_tmux.sh"), *args], env=self.env(**kw),
                              capture_output=True, text=True, timeout=60)

    def test_print_cmd_drafts(self):
        p = self.sh("print-cmd")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("APPROVAL_MODE=drafts", p.stdout)
        self.assertIn("--permission-mode dontAsk", p.stdout)
        self.assertIn("guard.py hook --approval drafts", p.stdout)
        self.assertIn("STUDIO_LOCAL=1 TZ=America/Chicago", p.stdout)
        self.assertNotIn("bypassPermissions", p.stdout.split("--- settings")[0])

    def test_refuses_bypass_in_drafts_and_missing_allowlist(self):
        p = self.sh("print-cmd", OPERATOR_PERMISSION_MODE="bypassPermissions")
        self.assertEqual(p.returncode, 2)
        self.assertIn("refusing", p.stdout)
        p = self.sh("print-cmd", OPERATOR_SETTINGS=os.path.join(self.tmp, "nope.json"))
        self.assertEqual(p.returncode, 5)
        os.makedirs(os.path.join(self.tmp, "studio"))
        with open(os.path.join(self.tmp, "studio", ".env"), "w") as f:
            f.write("BUFFER_API_KEY=x\nAPPROVAL_MODE=auto\n")
        p = self.sh("print-cmd", OPERATOR_PERMISSION_MODE="bypassPermissions")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("APPROVAL_MODE=auto", p.stdout)

    def test_cron_installer_print(self):
        p = subprocess.run(["bash", os.path.join(ROOT, "scripts", "install_operator_cron.sh"), "--print"],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0)
        self.assertIn("*/15 * * * * $HOME/studio/app/scripts/operator_watchdog.sh", p.stdout)


if __name__ == "__main__":
    unittest.main()
