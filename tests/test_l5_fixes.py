"""Regression tests for the L5 operator review findings (2026-11-01): chained job ids, exit 5/3 handling, publish
outcomes (detached hold, partial, dry run, expiry), metrics retries, stale session jobs, watchdog backoff/notes,
measured operator usage and the TikTok inbox. No network, no tmux, no claude."""
import datetime as dt
import json
import os
import sys
import time
import unittest

from _util import ROOT  # noqa: F401  (puts the repo on sys.path)
from test_l5_ops import Tmp

from pipeline.common import jsonl, timeutil
from pipeline.ops import budget, due as D, run as R, state as S


def human_text():
    with open(os.path.join(os.environ["STUDIO_DATA"], "operator", "HUMAN.md")) as f:
        return f.read()


class TestChainIds(Tmp):
    def test_make_r2_chain_reaches_review_fix_and_publish(self):
        cfg, st = self.cfg, S.default_state()
        t = timeutil.at_local("2026-11-02", "07:00")
        S.register(st, {"job_id": "20261102-a-make", "type": "make", "date": "2026-11-02", "slot": "a", "due_at": "x"})
        S.finish_job(st, cfg, "20261102-a-make", "done", 0, result={"slug": "op-1", "gate": "PASS", "source_id": "A"}, now=t)
        self.assertEqual(S.finish_job(st, cfg, "20261102-a-review", "done", verdict="REJECT", now=t),
                         ["20261102-a-make-r2"])
        new = S.finish_job(st, cfg, "20261102-a-make-r2", "done", 0,
                           result={"slug": "op-2", "gate": "FAIL", "source_id": "B"}, now=t)
        self.assertEqual(new, ["20261102-a-review-s2"])  # was [] (id collision with the first make's review)
        self.assertEqual(S.finish_job(st, cfg, "20261102-a-review-s2", "done", verdict="FIX", now=t),
                         ["20261102-a-fix-s2"])
        self.assertEqual(S.finish_job(st, cfg, "20261102-a-fix-s2", "done", 0, result={"gate": "PASS"}, now=t),
                         ["20261102-a-review-s2-r2"])
        self.assertEqual(S.finish_job(st, cfg, "20261102-a-review-s2-r2", "done", verdict="PASS", now=t),
                         ["20261102-a-publish-s2"])
        pub = st["jobs"]["20261102-a-publish-s2"]
        self.assertEqual((pub["slug"], pub["chain"]), ("op-2", 2))
        self.assertTrue(pub["expires_at"])
        S.finish_job(st, cfg, "20261102-a-publish-s2", "done", 0, result={"drafts": 3}, now=t)
        self.assertEqual(st["counters"]["slots_posted"], 1)

    def test_second_source_failing_counts_the_slot(self):
        cfg, st = self.cfg, S.default_state()
        t = timeutil.at_local("2026-11-02", "07:00")
        S.register(st, {"job_id": "20261102-a-make", "type": "make", "date": "2026-11-02", "slot": "a", "due_at": "x"})
        S.finish_job(st, cfg, "20261102-a-make", "failed", 1, now=t)
        S.finish_job(st, cfg, "20261102-a-make-r2", "done", 0, result={"slug": "op-2", "gate": "PASS"}, now=t)
        S.finish_job(st, cfg, "20261102-a-review-s2", "done", verdict="REJECT", now=t)
        self.assertEqual(st["counters"]["consecutive_failed_slots"], 1)  # no third source


class TestExitCodes(Tmp):
    def _job(self, st, jid, t):
        S.register(st, {"job_id": jid, "type": t, "due_at": "x"})

    def test_one_light_exit5_does_not_pause_two_do(self):
        cfg, st = self.cfg, S.default_state()
        now = timeutil.at_local("2026-11-02", "10:00")
        for i, jid in enumerate(("20261102-na-status-1000", "20261102-na-status-1030")):
            self._job(st, jid, "status")
            S.finish_job(st, cfg, jid, "failed", 5, now=now + dt.timedelta(minutes=30 * i))
            self.assertEqual(st["paused"], i == 1, i)
        self.assertEqual(st["pause_reason"], "dependency_unavailable")

    def test_success_resets_strikes_and_exit1_never_pauses(self):
        cfg, st = self.cfg, S.default_state()
        now = timeutil.at_local("2026-11-02", "10:00")
        self._job(st, "s1", "status"); S.finish_job(st, cfg, "s1", "failed", 5, now=now)
        self._job(st, "s2", "status"); S.finish_job(st, cfg, "s2", "done", 0, now=now)
        self._job(st, "s3", "status"); S.finish_job(st, cfg, "s3", "failed", 5, now=now)
        self.assertFalse(st["paused"])
        for i in range(10):
            self._job(st, f"m{i}", "metrics48"); S.finish_job(st, cfg, f"m{i}", "failed", 1, now=now)
        self.assertFalse(st["paused"])
        self.assertIn("`analytics` jobs have failed", human_text())

    def test_per_video_cap_fails_only_the_slot(self):
        cfg, st = self.cfg, S.default_state()
        t = timeutil.at_local("2026-11-02", "07:00")
        S.register(st, {"job_id": "20261102-a-make", "type": "make", "date": "2026-11-02", "slot": "a", "due_at": "x"})
        new = S.finish_job(st, cfg, "20261102-a-make", "failed", 3,
                           result={"budget_cap": "video", "budget_level": "ok", "source_id": "A"}, now=t)
        self.assertIsNone(st["budget"]["stop_until"])
        self.assertEqual(new, ["20261102-a-make-r2"])  # the slot still gets its next-source retry
        st2 = S.default_state()
        S.register(st2, {"job_id": "20261102-a-make", "type": "make", "date": "2026-11-02", "slot": "a", "due_at": "x"})
        S.finish_job(st2, cfg, "20261102-a-make", "failed", 3, result={"budget_level": "hard"}, now=t)
        self.assertTrue(st2["budget"]["stop_until"])


class TestPublishOutcomes(Tmp):
    def _review_pass(self, st, t):
        S.register(st, {"job_id": "20261102-a-make", "type": "make", "date": "2026-11-02", "slot": "a", "due_at": "x"})
        S.finish_job(st, self.cfg, "20261102-a-make", "done", 0, result={"slug": "op-x", "gate": "PASS", "source_id": "A"}, now=t)
        S.finish_job(st, self.cfg, "20261102-a-review", "done", verdict="PASS", now=t)
        return "20261102-a-publish"

    def test_paused_publish_expires_as_skipped_without_rejecting(self):
        t = timeutil.at_local("2026-11-02", "09:00")
        with S.updating() as st:
            jid = self._review_pass(st, t)
            st["paused"] = True
        later = timeutil.at_local("2026-11-02", "14:00")  # post 11:30 + publish_late_h 2
        D.register_due(later)
        st = S.load_state()
        self.assertEqual(st["jobs"][jid]["status"], "skipped")
        self.assertEqual(st["rejected_sources"], [])
        self.assertEqual(st["counters"]["consecutive_failed_slots"], 0)
        self.assertIn("missed its slot", human_text())

    def test_late_publish_exit4_is_skipped(self):
        st = S.default_state()
        jid = self._review_pass(st, timeutil.at_local("2026-11-02", "09:00"))
        S.finish_job(st, self.cfg, jid, "skipped", 4, note="late", now=timeutil.at_local("2026-11-02", "14:00"))
        self.assertEqual((st["rejected_sources"], st["counters"]["slots_failed"]), ([], 0))
        self.assertNotIn("20261102-a-make-r2", st["jobs"])

    def test_failure_after_posts_were_created_is_not_a_failed_slot(self):
        t = timeutil.at_local("2026-11-02", "09:00")
        st = S.default_state()
        jid = self._review_pass(st, t)
        jsonl.append(os.path.join(os.environ["STUDIO_DATA"], "posts.jsonl"),
                     {"post_key": "op-x:youtube", "slug": "op-x", "platform": "youtube", "status": "draft",
                      "dry_run": False, "buffer_post_id": "p1"})
        S.finish_job(st, self.cfg, jid, "failed", 1, note="timeout", now=t)
        self.assertEqual(st["rejected_sources"], [])
        self.assertNotIn("20261102-a-make-r2", st["jobs"])
        self.assertEqual(st["counters"]["slots_posted"], 1)

    def test_dry_run_publish_is_not_counted(self):
        st = S.default_state()
        jid = self._review_pass(st, timeutil.at_local("2026-11-02", "09:00"))
        S.finish_job(st, self.cfg, jid, "done", 0, result={"dry_run": True, "drafts": 0})
        self.assertEqual((st["counters"]["slots_posted"], st["counters"]["drafts_created"]), (0, 0))
        self.assertIn("dry run", human_text())

    def test_detached_returns_at_created_and_leaves_the_hold_running(self):
        res = os.path.join(self.tmp, "res.json")
        code = ("import json,os,sys,time\n"
                f"json.dump({{'phase':'created','pid':os.getpid(),'exit':0,'created':['youtube'],'holding':True}},"
                f"open({res!r},'w'))\n"
                "time.sleep(60)\n")
        with open(os.path.join(self.tmp, "log"), "w") as log:
            r = R.Runner("j", {}, self.cfg, log)
            t0 = time.time()
            rc, out = r.detached([sys.executable, "-c", code], res, wait_s=30)
        self.assertLess(time.time() - t0, 20)
        self.assertEqual((rc, out["created"]), (0, ["youtube"]))
        pid = out["hold_pid"]
        self.assertTrue(R._alive(pid))  # not killed by the job
        os.killpg(pid, 15)

    def test_h_publish_partial_and_skipped(self):
        tomorrow = (timeutil.to_local().date() + dt.timedelta(days=1)).isoformat()
        jid = S.job_id(tomorrow, "b", "publish")
        with S.updating() as st:
            S.register(st, {"job_id": jid, "type": "publish", "date": tomorrow, "slot": "b", "slug": "op-x",
                            "due_at": timeutil.iso()})

        def fake(key, argv):
            rf = argv[argv.index("--result-file") + 1]
            with open(rf, "w") as f:
                json.dump({"phase": "done", "exit": 1, "created": ["youtube"], "failed": ["tiktok"],
                           "skipped_platforms": ["instagram"], "dry_run": False}, f)
            return 1, ""
        self.assertEqual(R.execute(jid, fake=fake), 0)
        j = S.load_state()["jobs"][jid]
        self.assertEqual((j["status"], j["result"]["partial"], j["result"]["drafts"]), ("done", True, 1))
        txt = human_text()
        self.assertIn("FAILED tiktok", txt)
        self.assertIn("BUFFER_CHANNEL_INSTAGRAM missing", txt)

    def test_h_status_reports_failed_buffer_posts(self):
        jsonl.append(os.path.join(os.environ["STUDIO_DATA"], "posts.jsonl"),
                     {"post_key": "op-x:instagram", "slug": "op-x", "platform": "instagram", "status": "failed",
                      "dry_run": False, "buffer_post_id": "p7", "error": "media fetch failed"})
        with S.updating() as st:
            S.register(st, {"job_id": "s", "type": "status", "due_at": timeutil.iso()})
        R.execute("s", fake=lambda k, a: (0, ""))
        self.assertIn("went to **failed**: media fetch failed", human_text())


class TestMetricsRetry(unittest.TestCase):
    cfg = None

    def setUp(self):
        self.cfg = json.load(open(os.path.join(ROOT, "pipeline", "ops", "config.default.json")))

    def test_pending_row_gets_retry_every_12h_until_grace(self):
        pub = timeutil.parse("2026-11-02T17:30:00Z")
        posts = {"s:youtube": {"post_key": "s:youtube", "slug": "s", "platform": "youtube", "status": "published",
                               "published_at": timeutil.iso(pub)}}
        st = S.default_state()
        base = S.job_id(timeutil.local_date(pub), None, "metrics48", "s:youtube")
        t48 = pub + dt.timedelta(hours=48, minutes=5)
        r = D.due_jobs(self.cfg, st, posts, [], t48, {})
        self.assertIn(base, [j["job_id"] for j in r["new"]])
        S.register(st, r["new"][0] if r["new"][0]["job_id"] == base else next(j for j in r["new"] if j["job_id"] == base))
        st["jobs"][base].update(status="done", finished_at=timeutil.iso(t48))
        metrics = [{"post_key": "s:youtube", "window": "48h", "platform": "youtube", "views": 10, "pending": ["retention"]}]
        self.assertFalse([j for j in D.due_jobs(self.cfg, st, posts, metrics, t48 + dt.timedelta(hours=1), {})["new"]
                          if "retry" in j["job_id"]])
        r = D.due_jobs(self.cfg, st, posts, metrics, t48 + dt.timedelta(hours=12, minutes=1), {})
        self.assertIn(base + "-retry1", [j["job_id"] for j in r["new"]])
        # complete row -> no retry; past window + 48 h -> no retry
        ok = metrics + [{"post_key": "s:youtube", "window": "48h", "platform": "youtube", "views": 12}]
        self.assertFalse([j for j in D.due_jobs(self.cfg, st, posts, ok, t48 + dt.timedelta(hours=13), {})["new"]
                          if "retry" in j["job_id"]])
        self.assertFalse([j for j in D.due_jobs(self.cfg, st, posts, metrics, pub + dt.timedelta(hours=97), {})["new"]
                          if "retry" in j["job_id"]])

    def test_dry_run_and_error_rows_are_incomplete(self):
        self.assertTrue(D.metric_incomplete({"dry_run": True, "views": 5}))
        self.assertTrue(D.metric_incomplete({"error": "no external_id yet", "views": None}))
        self.assertTrue(D.metric_incomplete({"views": None, "source": "ig_graph"}))
        self.assertFalse(D.metric_incomplete({"views": 5, "source": "yt_data"}))


class TestSessionAndWatchdog(Tmp):
    def test_stale_review_reset_then_failed(self):
        cfg, st = self.cfg, S.default_state()
        now = timeutil.at_local("2026-11-02", "08:00")
        S.register(st, {"job_id": "20261102-a-review", "type": "review", "date": "2026-11-02", "slot": "a",
                        "due_at": "x"})
        st["jobs"]["20261102-a-review"].update(status="running", attempts=1,
                                               started_at=timeutil.iso(now - dt.timedelta(hours=2)))
        st["session"]["started_at"] = timeutil.iso(now - dt.timedelta(hours=31))
        st["session"]["heartbeat_at"] = timeutil.iso(now)
        self.assertEqual(S.watchdog_action(cfg, st, True, [], now), "rotate")  # a stale running job never blocks
        self.assertEqual(S.reset_stale_session_jobs(st, now), ["20261102-a-review"])
        self.assertEqual(st["jobs"]["20261102-a-review"]["status"], "pending")
        st["jobs"]["20261102-a-review"].update(status="running", attempts=2,
                                               started_at=timeutil.iso(now - dt.timedelta(hours=2)))
        S.reset_stale_session_jobs(st, now)
        self.assertEqual(st["jobs"]["20261102-a-review"]["status"], "failed")

    def test_fast_exits_back_off_and_notify(self):
        cfg, st = self.cfg, S.default_state()
        now = timeutil.at_local("2026-11-02", "08:00")
        for _ in range(3):
            S.watchdog_launched(st, False, now)
        self.assertEqual(S.watchdog_action(cfg, st, False, [], now + dt.timedelta(minutes=15)), "backoff")
        self.assertEqual(S.watchdog_action(cfg, st, False, [], now + dt.timedelta(minutes=31)), "resume")
        notes = dict(S.watchdog_notes(cfg, st, now))
        self.assertTrue(any(k.startswith("watchdog:fast-exit") for k in notes))
        S.watchdog_launched(st, True, now)
        self.assertEqual(S.watchdog_action(cfg, st, False, [], now), "resume")
        st["session"]["heartbeat_at"] = timeutil.iso(now - dt.timedelta(hours=3))
        self.assertTrue(any(k.startswith("watchdog:stale") for k, _ in S.watchdog_notes(cfg, st, now)))
        self.assertEqual(S.watchdog_notes(cfg, st, now, stopped=True), [])


class TestOperatorBudget(Tmp):
    def test_measured_usage_from_transcripts_holds_session_jobs(self):
        proj = os.path.join(self.tmp, "claude", "projects", "-home-u-studio-app")
        os.makedirs(os.path.join(proj, "sid1", "subagents"))
        os.environ["CLAUDE_PROJECTS_DIR"] = os.path.join(self.tmp, "claude", "projects")
        self.addCleanup(os.environ.pop, "CLAUDE_PROJECTS_DIR", None)
        ts = timeutil.iso()
        line = {"type": "assistant", "timestamp": ts, "requestId": "r1",
                "message": {"id": "m1", "usage": {"input_tokens": 800_000, "output_tokens": 0,
                                                  "cache_read_input_tokens": 1_000_000}}}
        with open(os.path.join(proj, "sid1.jsonl"), "w") as f:
            f.write(json.dumps(line) + "\n" + json.dumps(line) + "\n")  # streamed duplicate counts once
        sub = dict(line, requestId="r2", message={"id": "m2", "usage": {"input_tokens": 700_000, "output_tokens": 0}})
        with open(os.path.join(proj, "sid1", "subagents", "a.jsonl"), "w") as f:
            f.write(json.dumps(sub) + "\n")
        st = S.default_state()
        st["sessions"] = [{"id": "sid1"}]
        b = budget.check(self.cfg, st)
        self.assertEqual(b["operator_measured_today"], 800_000 + 100_000 + 700_000)
        self.assertTrue(b["operator_cap"])
        S.register(st, {"job_id": "rv", "type": "review", "due_at": timeutil.iso()})
        r = D.due_jobs(self.cfg, st, {}, [], timeutil.now_utc(), {"operator_cap": True})
        self.assertNotIn("rv", [j["job_id"] for j in r["due"]])
        self.assertEqual(r["session_blocked"], "operator daily token cap")


class TestTikTokInbox(Tmp):
    def test_import_once_moves_csv_and_covered_screens_and_dedupes(self):
        data = os.environ["STUDIO_DATA"]
        inbox = os.path.join(data, "inbox", "tiktok")
        os.makedirs(inbox)
        jsonl.append(os.path.join(data, "posts.jsonl"),
                     {"post_key": "op-x:tiktok", "slug": "op-x", "platform": "tiktok", "status": "published",
                      "external_id": "7400000000000000001", "published_at": "2026-11-01T17:30:00Z", "duration_s": 70})
        img = os.path.join(inbox, "a.png")
        open(img, "wb").write(b"png")
        csvp = os.path.join(inbox, "2026-11-04-1.screenshot.csv")
        row = "7400000000000000001,2026-11-04T18:00:00Z,12.3K,840,21,57,130,31.4,18.2,44,0:100;3:71;10:48"
        open(csvp, "w").write("tiktok_url_or_id,captured_at,views,likes,comments,shares,saves,avg_watch_s,"
                              "full_watch_pct,new_followers,retention\n" + row + "\n")
        os.utime(img, (time.time() - 60, time.time() - 60))
        with S.updating() as st:
            S.register(st, {"job_id": "tt", "type": "tiktok_inbox", "due_at": timeutil.iso()})
        os.environ["STUDIO_DATA_DIR"] = data  # the analytics lane's data dir (run.py's subprocess inherits it)
        self.addCleanup(os.environ.pop, "STUDIO_DATA_DIR", None)
        from pipeline.analytics import tiktok_import
        self.assertEqual(R.execute("tt"), 0)
        j = S.load_state()["jobs"]["tt"]
        self.assertEqual((j["status"], j["result"]["screenshots"], j["result"]["screenshots_done"]), ("done", 0, 1))
        self.assertTrue(os.path.exists(os.path.join(inbox, "done", "a.png")))
        self.assertFalse(os.path.exists(csvp))
        self.assertFalse([k for k in S.load_state()["jobs"] if "tiktok_screens" in k])  # nothing left to transcribe
        rows = jsonl.read(os.path.join(data, "metrics.jsonl"))
        self.assertEqual(len(rows), 1)
        # a re-import of the same file adds nothing
        os.replace(os.path.join(inbox, "done", os.path.basename(csvp)), csvp)
        self.assertEqual(tiktok_import.import_csv(csvp, source="tiktok_screenshot"), [])
        self.assertEqual(len(jsonl.read(os.path.join(data, "metrics.jsonl"))), 1)


if __name__ == "__main__":
    unittest.main()
