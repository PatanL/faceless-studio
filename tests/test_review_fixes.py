"""Regression tests for the L1-L4 review findings (2026-11-01): template-aware title sameness, topic aliases and
fallbacks, gated same-day siblings in the sameness history, the source-title / music / disclosure gate checks, AUTH_RX,
the per-video budget marker, transient vs auth errors, Instagram shortcodes, kill-rule views, per-platform dry runs
and the status link refresh. No network, no Spark."""
import io
import json
import os
import pathlib
import shutil
import tempfile
import time
import unittest
import urllib.error
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timedelta, timezone
from unittest import mock

import _util  # noqa: F401  (puts the repo on sys.path)

from pipeline import make as mk
from pipeline import sources
from pipeline.analytics import _common, collect, http, instagram, killrule
from pipeline.publish import buffer as B
from pipeline.publish import captions as C
from pipeline.publish import status
from pipeline.qa import gate as G
from pipeline.qa import sameness, textsim


class Titles(unittest.TestCase):
    def test_template_on_another_subject_is_warn_not_fail(self):
        for a, b in [("Why Sperm Whales Are Terrifying", "Why Orcas Are Terrifying"),
                     ("What Happens If You Fall Into The Mariana Trench", "What Happens If You Fall Into A Volcano")]:
            c = textsim.title_compare(a, b)
            self.assertGreaterEqual(c["full"], 0.6)
            self.assertEqual(c["level"], "WARN", (a, b, c))
        self.assertEqual(textsim.title_compare("How Electrical Outlets Work", "How Car Engines Work")["level"], "PASS")
        self.assertEqual(textsim.title_compare("Why Orcas Are Terrifying", "Why Orcas Are Terrifying")["level"], "FAIL")

    def test_sameness_template_hit_is_warn(self):
        fp = {"slug": "a", "title": "Why Sperm Whales Are Terrifying", "hook": "one", "topic": "sperm whale"}
        old = {"slug": "b", "title": "Why Orcas Are Terrifying", "hook": "two", "topic": "orca"}
        res = sameness.check(fp, [old])
        self.assertEqual(res["status"], "WARN", res["detail"])
        self.assertIn("title_template", res["detail"])
        # yt_title (title) and the picked title (title_alt) are both checked
        fp2 = dict(fp, title="Sperm Whales Explained", title_alt=["Why Orcas Are Terrifying"])
        self.assertEqual(sameness.check(fp2, [old])["status"], "FAIL")

    def test_topic_alias_values_are_not_stripped(self):
        self.assertTrue(textsim.same_topic("octopus", "giant pacific octopus"))
        self.assertEqual(textsim.topic_key("walrus"), "walrus")
        self.assertEqual(textsim.topic_key("orcas"), "orca")

    def test_sources_topic_fallback_keeps_the_subject(self):
        a = sources.fallback_topic({"title": "What Happens If You Fall Into A Volcano"})
        b = sources.fallback_topic({"title": "What Happens If You Fall Into The Mariana Trench"})
        self.assertNotEqual(a, b)
        self.assertLess(sources._jaccard("What Happens If You Fall Into A Volcano",
                                         "What Happens If You Fall Into The Mariana Trench"), 0.5)


class Root(unittest.TestCase):
    def setUp(self):
        self.r = pathlib.Path(tempfile.mkdtemp(prefix="fixes-"))

    def tearDown(self):
        shutil.rmtree(self.r, ignore_errors=True)

    def gated(self, slug, verdict="PASS", review=None, age_h=1.0, title="T"):
        q = self.r / "out" / slug / "qa"
        q.mkdir(parents=True, exist_ok=True)
        (q / "gate.json").write_text(json.dumps({"verdict": verdict}))
        (q / "fingerprint.json").write_text(json.dumps({"slug": slug, "title": title, "hook": "h", "topic": slug}))
        if review:
            (q / "review.json").write_text(json.dumps({"verdict": review}))
        t = time.time() - age_h * 3600
        os.utime(q / "gate.json", (t, t))


class History(Root):
    def test_same_day_gated_sibling_is_in_history(self):
        self.gated("op-20261102-a-orca")
        self.gated("op-20261102-a-old", age_h=60)
        self.gated("op-20261102-a-bad", verdict="FAIL")
        self.gated("op-20261102-a-rej", review="REJECT")
        h = sameness.history_slugs(self.r, "op-20261102-b-killer-whale", 10)
        self.assertEqual(h, ["op-20261102-a-orca"])
        res = sameness.run(self.r, "op-20261102-b-killer-whale", {"slug": "x", "title": "Q", "hook": "z", "topic": "y"})
        self.assertEqual((res["history_mode"], res["history"]), ("default", ["op-20261102-a-orca"]))
        self.assertEqual(sameness.run(self.r, "x", {"title": "Q"}, against=[""])["history_mode"], "against")


class GateChecks(Root):
    def test_source_title(self):
        src = {"source_id": "S", "title": "What Happens If You Fall Into A Volcano"}
        self.assertEqual(G.check_source_title(src, ["What Happens If You Fall Into A Volcano"], "x")["status"], "FAIL")
        self.assertEqual(G.check_source_title(src, ["What Happens If You Fall Into The Mariana Trench"],
                                              "x")["status"], "WARN")
        self.assertEqual(G.check_source_title(src, ["The Deepest Place You Could Ever Sink"], "x")["status"], "PASS")
        hook = "Fall into a volcano and you would not sink at all"
        self.assertEqual(G.check_source_title({"title": "You Would Not Sink At All In Lava"}, ["Lava Is Thick"],
                                              hook)["status"], "FAIL")  # 5-word run "you would not sink at"
        self.assertEqual(G.check_source_title({}, ["x"], "y")["status"], "PASS")

    def test_music_allowlist(self):
        ep = self.r / "episodes" / "s" / "audio"
        ep.mkdir(parents=True)
        for music, want in (("deep_ocean", "PASS"), ("none", "PASS"), ("/home/u/Downloads/hit_song.mp3", "FAIL"),
                            ("ext/some_track", "FAIL")):
            (ep / "report.json").write_text(json.dumps({"mix": {"music": music}}))  # pipeline.audio.make's shape
            self.assertEqual(G.check_music(self.r, "s")["status"], want, music)
        self.assertEqual(G.DUR_FAIL, 180.0)

    def test_disclosure_checks_every_built_caption(self):
        ep = self.r / "episodes" / "s"
        ep.mkdir(parents=True)
        (ep / "package.json").write_text(json.dumps({
            "titles": ["T"], "title_pick": 0, "short_caption": "Caption.", "hashtags": ["#a"],
            "yt_description": "Body.\nNarration: synthetic AI voice", "disclosure_line": "Animation: original 2D vector art."}))
        g = G.check_disclosure(self.r, "s")
        self.assertEqual(g["status"], "PASS", g)  # the non-AI line is replaced by C.DISCLOSURE everywhere
        cap = C.build("s", dict(json.loads((ep / "package.json").read_text()), yt_title="T"))
        for t in (cap["tiktok"]["text"], cap["instagram"]["text"], cap["youtube"]["description"]):
            self.assertTrue(C.AI_VOICE_RX.search(t))
        self.assertFalse(C.AI_VOICE_RX.search("Thai voice #tts"))

    def test_missing_source_transcript_fails_for_a_source_episode(self):
        ep = self.r / "episodes" / "s"
        ep.mkdir(parents=True)
        script = ep / "script.md"
        script.write_text("---\nid: s\n---\n\n```narration\n" + " ".join(f"word{i}" for i in range(80)) + "\n```\n")
        (self.r / "research" / "corpus").mkdir(parents=True)
        res = G.check_originality(self.r, "s", script, {"source_id": "NOPE"}, {}, "explainer")
        self.assertEqual(res["status"], "FAIL", res)
        res = G.check_originality(self.r, "s", script, {}, {}, "explainer")
        self.assertEqual(res["status"], "WARN", res)


class MakeAuth(unittest.TestCase):
    def test_ordinary_failure_mentioning_author_or_403_is_exit_1(self):
        from test_l1_make import fake
        with tempfile.TemporaryDirectory() as tmp:
            m = fake(tmp)
            out = json.dumps({"type": "result", "is_error": True, "session_id": "4013-a403-0401",
                              "result": "The author section is missing; 403 words is too short", "total_cost_usd": 0.4013})

            def spark(cmd, check=True, **k):
                if "claude -p" in cmd:
                    raise mk.Fail("x", out=out, rc=1)
                return ""
            m.spark = spark
            with self.assertRaises(mk.Fail) as cm:
                m.claude("p", "script")
            self.assertEqual(cm.exception.exit_code, 1)

    def test_budget_stop_is_marked_per_video(self):
        from test_l1_make import fake
        with tempfile.TemporaryDirectory() as tmp:
            m = fake(tmp, budget_tokens=1_000_000)
            m.status["usage_total"]["weighted_tokens"] = 900_000
            with self.assertRaises(mk.Fail) as cm:
                m.claude("p", "shots")
            self.assertEqual((cm.exception.exit_code, m.status["budget_cap"]), (3, "video"))


class Transient(unittest.TestCase):
    def test_buffer_5xx_and_unreachable_are_exit_1(self):
        c = B.BufferClient("k" * 20, sleep=lambda s: None, out=io.StringIO())
        err = urllib.error.HTTPError("https://api.buffer.com", 503, "x", {}, io.BytesIO(b"{}"))
        with mock.patch("urllib.request.urlopen", side_effect=err):
            with self.assertRaises(B.Unavailable) as cm:
                c.organizations()
        self.assertEqual(cm.exception.exit_code, 1)
        with mock.patch("urllib.request.urlopen", side_effect=urllib.error.URLError(OSError("dns"))):
            with self.assertRaises(B.Unavailable):
                c.organizations()

    def test_analytics_network_error_is_transient(self):
        with mock.patch("urllib.request.urlopen", side_effect=urllib.error.URLError("down")), \
                mock.patch("time.sleep"):
            with self.assertRaises(_common.TransientError):
                http.request("GET", "https://example.invalid/x")


class L4(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="fixes-l4-")
        self._env = mock.patch.dict(os.environ, {"STUDIO_DATA_DIR": self.tmp,
                                                 "STUDIO_ENV_FILE": os.path.join(self.tmp, "no.env")})
        self._env.start()

    def tearDown(self):
        self._env.stop()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_instagram_shortcode_is_resolved_to_a_media_id(self):
        post = {"post_key": "s:instagram", "platform": "instagram", "external_id": "C1a2B3c4D5e",
                "external_url": "https://www.instagram.com/reel/C1a2B3c4D5e/", "published_at": "2026-11-02T17:30:00Z"}
        asked = []

        def get(self_, path, params):
            asked.append(path)
            if path.endswith("/media"):
                return {"data": [{"id": "17890000000000001", "shortcode": "C1a2B3c4D5e",
                                  "permalink": "https://www.instagram.com/reel/C1a2B3c4D5e/"}]}
            return {"data": [{"name": params["metric"], "values": [{"value": 42}]}]}
        with mock.patch.object(instagram.Client, "get", get):
            row = instagram.fetch(post, {"IG_USER_ID": "u1", "IG_ACCESS_TOKEN": "t"})
        self.assertEqual((row["external_id"], row["external_shortcode"], row["views"]),
                         ("17890000000000001", "C1a2B3c4D5e", 42))
        self.assertTrue(all("C1a2B3c4D5e" not in p for p in asked))
        self.assertTrue(instagram.is_media_id("17890000000000001"))

    def test_killrule_uses_first_7d_row_and_drops_late_rows(self):
        def m(k, views, age):
            _common.jsonl_append(_common.dpath("metrics.jsonl"), {"post_key": k, "platform": "youtube", "window": "7d",
                                                                  "views": views, "age_h": age, "source": "yt_data"})
        m("a:youtube", 9000, 168.2)
        m("a:youtube", 12000, 204.0)   # pending retry 36 h later: must not win
        m("b:youtube", 50000, 300.0)   # collected after downtime: excluded
        late = []
        rows = killrule.series(excluded=late)
        self.assertEqual([(r["post_key"], r["views"]) for r in rows], [("a:youtube", 9000)])
        self.assertEqual([r["post_key"] for r in late], ["b:youtube"])

    def test_collect_due_is_dry_per_platform(self):
        pub = datetime.now(timezone.utc) - timedelta(hours=50)
        for plat in ("youtube", "instagram"):
            _common.jsonl_append(_common.dpath("posts.jsonl"), {
                "post_key": f"s:{plat}", "slug": "s", "platform": plat, "status": "published",
                "published_at": _common.iso(pub), "external_id": "17890000000000001", "duration_s": 70})
        envf = os.path.join(self.tmp, "ig.env")
        open(envf, "w").write("IG_USER_ID=u1\nIG_ACCESS_TOKEN=t\n")
        with mock.patch.dict(os.environ, {"STUDIO_ENV_FILE": envf}), \
                mock.patch.object(instagram, "fetch", return_value={"source": "ig_graph", "views": 7}) as f:
            buf = io.StringIO()
            with redirect_stdout(buf), redirect_stderr(buf):
                self.assertEqual(collect.main(["--due"]), 0)
        self.assertEqual(f.call_count, 1)  # instagram fetched although YouTube creds are missing
        rows = _common.jsonl_read(_common.dpath("metrics.jsonl"))
        self.assertEqual([(r["platform"], r["views"]) for r in rows], [("instagram", 7)])


class StatusLinks(unittest.TestCase):
    def test_published_row_without_link_stays_open_for_48h(self):
        now = datetime(2026, 11, 3, 18, 0, tzinfo=timezone.utc)
        row = {"status": "published", "published_at": "2026-11-02T17:30:00Z", "external_url": None}
        self.assertTrue(status.needs_link(row, now))
        self.assertFalse(status.needs_link(dict(row, external_url="u", external_id="i"), now))
        self.assertFalse(status.needs_link(row, now + timedelta(days=2)))


if __name__ == "__main__":
    unittest.main()
