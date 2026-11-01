"""L4 analytics + learning tests (OPERATOR_DESIGN 9.8). No network, no Spark: API answers are recorded fixtures,
ledgers live in a temp STUDIO_DATA_DIR, curves are synthetic."""
import io
import json
import os
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone
from unittest import mock

from _util import ROOT  # puts the repo on sys.path

from pipeline.analytics import (_common, align, beatmap, collect, experiments as X, heatmap, instagram, killrule,
                                learning, synthetic, tiktok_import, youtube)

ORCA = os.path.join(ROOT, "episodes", "explainer-orca")


class TempData(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="l4test-")
        self._env = mock.patch.dict(os.environ, {"STUDIO_DATA_DIR": self.tmp,
                                                 "STUDIO_ENV_FILE": os.path.join(self.tmp, "no.env")})
        self._env.start()

    def tearDown(self):
        self._env.stop()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def append(self, name, row):
        _common.jsonl_append(_common.dpath(name), row)


# ---------------------------------------------------------------- align
@unittest.skipUnless(os.path.exists(os.path.join(ORCA, "storyboard.json")), "orca storyboard not present")
class AlignOrca(unittest.TestCase):
    def test_beatmap_derived_from_storyboard(self):
        bm = beatmap.load("explainer-orca")
        self.assertTrue(bm["derived"])
        self.assertEqual(len(bm["scenes"]), 14)
        self.assertEqual(bm["scenes"][0]["beat"], "HOOK")
        self.assertEqual(bm["scenes"][9]["beat"], "OPTIONS")
        # F20 cumulative rounding: scene starts are whole frames, contiguous
        for a, b in zip(bm["scenes"], bm["scenes"][1:]):
            self.assertEqual(a["t1"], b["t0"])
            self.assertAlmostEqual(b["t0"] * 30, round(b["t0"] * 30), places=6)

    def test_synthetic_drops_land_on_the_right_scene_and_line(self):
        bm = beatmap.load("explainer-orca")
        D = bm["duration_s"]
        planted = {"p02": (12.3, "Olympic"), "p09": (49.6, "taste"), "p11": (62.0, "Comforting")}
        ret = synthetic.retention_curve(D, [(t, 0.07) for t, _ in planted.values()], seed=7, noise=0.003)
        ts, ys, rel = align.curve_from_retention(ret, D)
        res = align.align(bm, ts, ys, rel, "retention", D)
        got = {d["scene_id"]: d for d in res["top_drops"]}
        self.assertEqual(set(got), set(planted))
        for sid, (t, word) in planted.items():
            self.assertLess(abs(got[sid]["t"] - t), 1.0)
            self.assertIn(word, got[sid]["line"])
            self.assertIn(word, got[sid]["caption"])
        # the three planted scenes have the highest z after the hook
        zs = sorted((s["z"] for s in res["scenes"] if s["scene_id"] != "p00" and s["z"] is not None), reverse=True)[:3]
        top = {s["scene_id"] for s in res["scenes"] if s["z"] in zs}
        self.assertEqual(top, set(planted))
        self.assertGreater(res["tail"]["end_spike"], 0)

    def test_cli_with_curve_file_does_not_write_synthetic(self):
        tmp = tempfile.mkdtemp()
        try:
            p = os.path.join(tmp, "c.json")
            with open(p, "w") as f:
                json.dump({"duration_s": 75.13, "synthetic": True,
                           "retention": synthetic.retention_curve(75.13, [(30.0, 0.08)])}, f)
            with mock.patch.dict(os.environ, {"STUDIO_DATA_DIR": tmp}):
                buf = io.StringIO()
                with redirect_stdout(buf):
                    rc = align.main(["explainer-orca", "--curve", p])
            self.assertEqual(rc, 0)
            self.assertRegex(buf.getvalue(), r"DROP 1: t=(29|30)\.\d+s scene p05")
            self.assertFalse(os.path.exists(os.path.join(tmp, "alignments.jsonl")))
        finally:
            shutil.rmtree(tmp)


class AlignSource(unittest.TestCase):
    @unittest.skipUnless(os.path.exists(os.path.join(ROOT, "research/library/videos/fGcgWaswMns.json")), "no library")
    def test_heatmap_against_source_beats(self):
        hm = synthetic.heatmap(599, [(330, 0.55), (455, 0.4)], seed=3)
        bm = beatmap.source_beatmap("fGcgWaswMns", 599)
        ts, ys = align.curve_from_heatmap(hm["points"])
        res = align.align(bm, ts, ys, None, "heatmap", 599)
        self.assertEqual(res["top_peaks"][0]["scene_id"], "b09")  # 300-362 s story beat
        self.assertTrue(res["top_peaks"][0]["line"])
        self.assertIn("STORY", res["summary"]["best_beat"])


# ---------------------------------------------------------------- collectors (recorded fixtures)
YT_VIDEOS = {"items": [{"id": "abc123def45", "snippet": {"channelId": "UCours", "publishedAt": "2026-11-02T16:30:00Z"},
                        "statistics": {"viewCount": "15234", "likeCount": "812", "commentCount": "40"},
                        "contentDetails": {"duration": "PT1M14S"}}]}
YT_TOTALS = {"kind": "youtubeAnalytics#resultTable",
             "columnHeaders": [{"name": n, "columnType": "METRIC", "dataType": "INTEGER"} for n in youtube.TOTAL_METRICS],
             "rows": [[14900, 9100, 13000, 52, 70.3, 800, 39, 120, 31]]}
YT_RET = {"kind": "youtubeAnalytics#resultTable",
          "columnHeaders": [{"name": "elapsedVideoTimeRatio", "columnType": "DIMENSION", "dataType": "FLOAT"},
                            {"name": "audienceWatchRatio", "columnType": "METRIC", "dataType": "FLOAT"},
                            {"name": "relativeRetentionPerformance", "columnType": "METRIC", "dataType": "FLOAT"}],
          "rows": [[round(0.01 * k, 2), round(1.0 - 0.006 * k, 4), 0.55] for k in range(100, 0, -1)]}


class YouTubeFixtures(TempData):
    def test_duration_and_tables(self):
        self.assertEqual(youtube.iso8601_duration("PT1M14S"), 74.0)
        self.assertEqual(youtube.iso8601_duration("PT59.5S"), 59.5)
        r = youtube.retention_from_table(YT_RET)
        self.assertEqual(len(r["x"]), 100)
        self.assertEqual(r["x"][0], 0.01)  # sorted ascending
        self.assertIsNone(youtube.retention_from_table({"columnHeaders": [], "rows": []}))

    def test_fetch_with_recorded_answers(self):
        secrets_dir = os.path.join(self.tmp, "secrets")
        os.makedirs(secrets_dir)
        cs, tok = os.path.join(secrets_dir, "cs.json"), os.path.join(secrets_dir, "tok.json")
        for path, obj in ((cs, {"installed": {"client_id": "cid", "client_secret": "x"}}),
                          (tok, {"refresh_token": "r", "access_token": "a", "expires_at": 9e12})):
            with open(path, "w") as f:
                json.dump(obj, f)
        env = {"YT_CLIENT_SECRETS_FILE": cs, "YT_TOKEN_FILE": tok, "YT_CHANNEL_ID": "UCours"}

        def fake(method, url, params=None, **kw):
            if url.endswith("/videos"):
                return YT_VIDEOS
            return YT_RET if params.get("dimensions") == "elapsedVideoTimeRatio" else YT_TOTALS

        with mock.patch.object(youtube.http, "request", side_effect=fake):
            part = youtube.fetch("abc123def45", "2026-11-02T16:30:00Z", env)
        self.assertEqual(part["views"], 15234)
        self.assertEqual(part["engaged_views"], 9100)
        self.assertEqual(part["avg_view_pct"], 70.3)
        self.assertEqual(part["duration_s"], 74.0)
        self.assertIsNone(part["pending"])
        post = {"post_key": "op-20261102-a-x:youtube", "slug": "op-20261102-a-x", "platform": "youtube",
                "published_at": "2026-11-02T16:30:00Z", "external_id": "abc123def45"}
        row = collect.build_row(post, "48h", part, False, now=datetime(2026, 11, 4, 17, tzinfo=timezone.utc))
        self.assertEqual(row["age_h"], 48.5)
        self.assertAlmostEqual(row["derived"]["hold_50pct"], 0.7, places=3)
        self.assertNotIn("dry_run", row)

    def test_engaged_views_rejected_falls_back(self):
        calls = []

        class C(youtube.Client):
            def __init__(self):
                pass

            def report(self, vid, s, e, metrics, dimensions=None):
                calls.append(list(metrics))
                if "engagedViews" in metrics:
                    raise youtube.http.ApiError(400, "Unknown identifier (engagedViews)")
                return {"columnHeaders": [{"name": m} for m in metrics], "rows": [[1] * len(metrics)]}

        tot, notes = C().totals("v", "2026-11-01", "2026-11-03")
        self.assertNotIn("engagedViews", tot)
        self.assertEqual(len(calls), 2)
        self.assertTrue(notes)


class InstagramFixtures(unittest.TestCase):
    def test_values_and_match(self):
        self.assertEqual(instagram.insight_value({"data": [{"name": "views", "values": [{"value": 321}]}]}, "views"), 321)
        self.assertEqual(instagram.insight_value({"data": [{"name": "reach", "total_value": {"value": 99}}]}, "reach"), 99)
        media = [{"id": "1", "permalink": "https://www.instagram.com/reel/AAA/", "timestamp": "2026-11-02T16:31:10+0000",
                  "caption": "Orcas could kill you", "media_product_type": "REELS"},
                 {"id": "2", "permalink": "https://www.instagram.com/reel/BBB/", "timestamp": "2026-11-02T23:30:00+0000",
                  "caption": "Other", "media_product_type": "REELS"}]
        self.assertEqual(instagram.match_media(media, {"external_url": "https://www.instagram.com/reel/BBB"})["id"], "2")
        self.assertEqual(instagram.match_media(media, {"published_at": "2026-11-02T16:30:00Z",
                                                       "caption": "Orcas could kill you #ocean"})["id"], "1")
        row = instagram.to_row({"views": 500, "ig_reels_avg_watch_time": 12500, "reels_skip_rate": 40.0, "saved": 3})
        self.assertEqual(row["avg_view_s"], 12.5)
        self.assertEqual(row["viewed_vs_swiped_pct"], 60.0)
        self.assertEqual(row["saves"], 3)


class Collect(TempData):
    def _post(self, slug, plat, hours_ago, status="published", **kw):
        pub = datetime.now(timezone.utc) - timedelta(hours=hours_ago)
        self.append("posts.jsonl", {"post_key": f"{slug}:{plat}", "slug": slug, "platform": plat, "status": status,
                                    "published_at": _common.iso(pub), "external_id": "vid" + slug[-3:], "duration_s": 74.0, **kw})

    def test_due_windows_and_pending_retry(self):
        self._post("op-20261101-a-aaa", "youtube", 50)
        self._post("op-20261101-a-aaa", "tiktok", 50)
        self._post("op-20261025-b-bbb", "youtube", 200)
        self._post("op-20261101-b-ccc", "youtube", 10)
        self._post("op-20261101-b-ddd", "instagram", 60, status="dry_run")
        d = {(x["post_key"], x["window"]) for x in collect.due(windows_h=[48, 168])}
        self.assertEqual(d, {("op-20261101-a-aaa:youtube", "48h"), ("op-20261101-a-aaa:tiktok", "48h"),
                             ("op-20261025-b-bbb:youtube", "48h"), ("op-20261025-b-bbb:youtube", "7d")})
        # a pending 48h row (Analytics still empty) is retried after 12 h only
        self.append("metrics.jsonl", {"post_key": "op-20261101-a-aaa:youtube", "window": "48h", "pending": ["analytics"]})
        d = {(x["post_key"], x["window"]) for x in collect.due(windows_h=[48])}
        self.assertNotIn(("op-20261101-a-aaa:youtube", "48h"), d)
        later = datetime.now(timezone.utc) + timedelta(hours=13)
        d = {(x["post_key"], x["window"]) for x in collect.due(now=later, windows_h=[48])}
        self.assertIn(("op-20261101-a-aaa:youtube", "48h"), d)
        # synthetic rows never satisfy a window
        self.append("metrics.jsonl", {"post_key": "op-20261025-b-bbb:youtube", "window": "7d", "dry_run": True})
        self.assertIn(("op-20261025-b-bbb:youtube", "7d"), {(x["post_key"], x["window"]) for x in collect.due(windows_h=[168])})

    def test_cli_dry_run_without_env(self):
        self._post("op-20261101-a-aaa", "youtube", 50)
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.assertEqual(collect.main(["--due"]), 0)
        out = buf.getvalue()
        self.assertIn("DRY-RUN: missing", out)
        self.assertIn("IG_ACCESS_TOKEN", out)
        self.assertIn("op-20261101-a-aaa:youtube 48h", out)
        self.assertEqual(_common.jsonl_read(_common.dpath("metrics.jsonl")), [])
        with redirect_stdout(io.StringIO()):
            self.assertEqual(collect.main(["--post-key", "op-20261101-a-aaa:youtube", "--window", "48h"]), 0)
        rows = _common.jsonl_read(_common.dpath("metrics.jsonl"))
        self.assertEqual(len(rows), 1)
        self.assertTrue(rows[0]["dry_run"])
        self.assertEqual(rows[0]["source"], "synthetic")
        self.assertEqual(len(rows[0]["retention"]["x"]), 100)
        self.assertEqual(len(rows[0]["requests"]), 3)
        self.assertIn("hold_3s", rows[0]["derived"])


class TikTok(TempData):
    def test_csv_import(self):
        self.append("posts.jsonl", {"post_key": "op-20261102-a-x:tiktok", "slug": "op-20261102-a-x", "platform": "tiktok",
                                    "status": "published", "published_at": "2026-11-02T16:30:00Z",
                                    "external_url": "https://www.tiktok.com/@us/video/7432100000000000001", "duration_s": 74.0})
        p = os.path.join(self.tmp, "t.csv")
        with open(p, "w") as f:
            f.write(",".join(tiktok_import.COLUMNS) + "\n")
            f.write("https://www.tiktok.com/@us/video/7432100000000000001,2026-11-09T18:00:00Z,12.3K,840,21,57,130,31.4,"
                    "18.2%,44,0:100;3:71;37:30;74:15\n")
        rows = tiktok_import.import_csv(p)
        self.assertEqual(rows[0]["views"], 12300)
        self.assertEqual(rows[0]["window"], "7d")
        self.assertEqual(rows[0]["derived"]["hold_3s"], 0.71)
        self.assertEqual(rows[0]["external_id"], "7432100000000000001")


class Heatmap(unittest.TestCase):
    def test_parse_states(self):
        info = {"duration": 213, "title": "t", "heatmap": [{"start_time": 0.0, "end_time": 2.1, "value": 1.0},
                                                           {"start_time": 2.1, "end_time": 4.2, "value": 0.4}]}
        self.assertEqual(heatmap.parse_info("x", 0, json.dumps(info), "")["status"], "ok")
        self.assertEqual(heatmap.parse_info("x", 0, json.dumps({**info, "heatmap": None}), "")["status"], "none")
        partial = json.dumps({"duration": None, "heatmap": None, "view_count": 5})
        err = "WARNING: [youtube] x: Sign in to confirm you're not a bot. Use --cookies"
        self.assertEqual(heatmap.parse_info("x", 0, partial, err)["status"], "blocked")
        self.assertEqual(heatmap.parse_info("x", 1, "", "ERROR: HTTP Error 429: Too Many Requests")["status"], "blocked")
        self.assertEqual(heatmap.video_id_of("https://www.youtube.com/shorts/fGcgWaswMns"), "fGcgWaswMns")


# ---------------------------------------------------------------- experiments
class Rule(unittest.TestCase):
    def test_adopt_reject_inconclusive_extend(self):
        c = [0.60, 0.62, 0.58, 0.61, 0.59, 0.63]
        t = [0.70, 0.72, 0.69, 0.66, 0.71, 0.60]
        pairs = list(zip(c, t))
        sec_ok = {"avg": ([70] * 6, [68] * 6)}
        self.assertEqual(X.rule(c, t, pairs, sec_ok, 6, 10)["decision"], "adopt")
        self.assertEqual(X.rule(t, c, [(b, a) for a, b in pairs], sec_ok, 6, 10)["decision"], "reject")
        # secondary 20 % worse blocks adoption
        self.assertEqual(X.rule(c, t, pairs, {"avg": ([70] * 6, [55] * 6)}, 6, 10)["decision"], "extend")
        flat = [0.61, 0.60, 0.62, 0.59, 0.60, 0.61]
        self.assertEqual(X.rule(c, flat, list(zip(c, flat)), {}, 6, 10)["decision"], "extend")
        c10, f10 = c + c[:4], flat + flat[:4]
        self.assertEqual(X.rule(c10, f10, list(zip(c10, f10)), {}, 6, 10)["decision"], "inconclusive")
        self.assertEqual(X.rule(c[:3], t[:3], pairs[:3], {}, 6, 10)["decision"], "pending")

    def test_arms_alternate_by_slot_and_day(self):
        a1, b1 = X.arm_for("2026-11-02", "a"), X.arm_for("2026-11-02", "b")
        a2 = X.arm_for("2026-11-03", "a")
        self.assertNotEqual(a1, b1)
        self.assertNotEqual(a1, a2)
        self.assertEqual(X.arm_for("2026-11-30", "a"), X.arm_for("2026-12-02", "a"))
        self.assertNotEqual(X.arm_for("2026-10-31", "a"), X.arm_for("2026-11-01", "a"))  # month boundary


class ExperimentFlow(TempData):
    def test_open_assign_decide_adopt_updates_rules(self):
        spec = X.propose("hook")
        self.assertEqual(spec["variable"], "hook.max_words")
        exp = X.open_experiment(spec, 3, 5)
        self.assertEqual(exp["experiment_id"], "EXP-001")
        with self.assertRaises(RuntimeError):
            X.open_experiment(X.propose("visual"))
        for dim in X.CANDIDATES:  # every backlog candidate has a valid control and treatment
            for var, val, _, _ in X.CANDIDATES[dim]:
                X.validate(var, val)
                X.validate(var, X.baseline(var))
        days = ["2026-11-02", "2026-11-03", "2026-11-04"]
        for d in days:
            for slot in "ab":
                slug = f"op-{d.replace('-', '')}-{slot}-t{slot}"
                asg = X.assign(d, slot, slug)
                self.assertEqual(X.assign(d, slot, slug), asg)  # idempotent
                good = asg["arm"] == "treatment"
                self.append("metrics.jsonl", {"post_key": f"{slug}:youtube", "platform": "youtube", "window": "7d",
                                              "views": 5000, "avg_view_pct": 80.0,
                                              "derived": {"hold_3s": 0.75 if good else 0.62}})
        self.assertEqual(sum(1 for r in X.rows() if r.get("type") == "assignment"), 6)
        res = X.evaluate(X.running())
        self.assertEqual(res["decision"], "adopt")
        self.assertEqual(res["paired_wins"], "3/3")
        X.apply_decision(X.running(), res)
        self.assertIsNone(X.running())
        rules = X.load_rules()
        self.assertEqual(rules["defaults"]["hook.max_words"], 8)
        self.assertEqual(rules["history"][-1]["old"], 12)
        promos = [r for r in X.rows() if r.get("type") == "promotion"]
        self.assertEqual(promos[0]["status"], "overlay_applied")
        if len(promos) > 1:
            patch = promos[1]["proposal"]
            with open(patch if os.path.isabs(patch) else os.path.join(ROOT, patch)) as f:
                text = f.read()
            self.assertIn("+- ", text)
            self.assertIn("hook.max_words", text)
        self.assertEqual(X.assign("2026-11-05", "a"), {})  # nothing running now

    def test_bad_values_rejected(self):
        with self.assertRaises(ValueError):
            X.validate("hook.type", "H99")
        with self.assertRaises(ValueError):
            X.validate("visual.max_hold_s", 5)
        self.assertEqual(X.validate("pace.wpm", "190"), 190)


# ---------------------------------------------------------------- kill rule
class KillRule(unittest.TestCase):
    def test_verdicts(self):
        self.assertEqual(killrule.evaluate([20000] * 12)["verdict"], "insufficient")
        self.assertEqual(killrule.evaluate([12000 + i for i in range(30)])["verdict"], "continue")
        rising = [1000 + 250 * i for i in range(30)]  # median ~4.6k, last-10 ~7.1k, slope +250
        r = killrule.evaluate(rising)
        self.assertEqual(r["verdict"], "extend")
        self.assertTrue(r["extended_once"])
        self.assertEqual(r["n_at_extend"], 30)
        self.assertEqual(killrule.evaluate(rising + [8000] * 5, r)["verdict"], "extend")  # waiting for 15 more
        self.assertEqual(killrule.evaluate(rising + [3000] * 15, r)["verdict"], "stop")  # re-check fails
        self.assertEqual(killrule.evaluate([3000 - 20 * i for i in range(30)])["verdict"], "stop")
        self.assertAlmostEqual(killrule.theil_sen([1, 3, 5, 7]), 2.0)


# ---------------------------------------------------------------- learning
@unittest.skipUnless(os.path.exists(os.path.join(ORCA, "storyboard.json")), "orca storyboard not present")
class Learning(TempData):
    def test_learning_md_from_simulated_week(self):
        bm = beatmap.load("explainer-orca")
        D = bm["duration_s"]
        for i, d in enumerate(["2026-11-09", "2026-11-10"]):
            for slot in "ab":
                slug = f"op-{d.replace('-', '')}-{slot}-orca{i}"
                for plat in ("youtube", "tiktok", "instagram"):
                    self.append("posts.jsonl", {"post_key": f"{slug}:{plat}", "slug": slug, "platform": plat,
                                                "status": "published", "published_at": f"{d}T17:30:00Z",
                                                "source_id": "VtrcKTkhDHU", "duration_s": D})
                ret = synthetic.retention_curve(D, [(12.3, 0.07), (49.6, 0.05)], seed=i)
                self.append("metrics.jsonl", {"post_key": f"{slug}:youtube", "platform": "youtube", "window": "7d",
                                              "views": 4000 + 1000 * i, "avg_view_pct": 75.0, "retention": ret,
                                              "derived": collect.derive(ret, D)})
                ts, ys, rel = align.curve_from_retention(ret, D)
                self.append("alignments.jsonl", {"kind": "own", "post_key": f"{slug}:youtube", "slug": slug,
                                                 "window": "7d", **align.align(bm, ts, ys, rel, "retention", D)})
        text = learning.build("2026-W46")
        for h in ("## 1. Scoreboard", "## 2. Where viewers leave", "## 3. Source vs ours", "## 4. Experiments",
                  "## 5. Kill rule", "## 6. Candidate next experiments", "## 7. Operator notes"):
            self.assertIn(h, text)
        self.assertIn("op-20261109-a-orca0 **(this week)**", text)
        self.assertIn("| SPEED |", text)
        self.assertIn("insufficient", text)
        self.assertIn("--dimension", text)
        with redirect_stdout(io.StringIO()):
            learning.main(["--week", "2026-W46"])
        self.assertTrue(os.path.exists(os.path.join(self.tmp, "learning", "LEARNING.md")))


if __name__ == "__main__":
    unittest.main()
