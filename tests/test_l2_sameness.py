"""L2 sameness check (pipeline/qa/sameness.py, textsim.py, fingerprint.py). Pure python: no ffmpeg, no network.

Synthetic fingerprints test each FAIL/WARN rule on its own; the pilots' text-only fingerprints and every pair of
distinct scripts in episodes/ check that the thresholds don't fire on videos that are really different.
"""
import copy
import itertools
import json
import os
import pathlib
import tempfile
import unittest

import _util  # noqa: F401  (puts the repo root on sys.path)

from pipeline.qa import fingerprint as F
from pipeline.qa import sameness as S
from pipeline.qa import textsim as T

ROOT = pathlib.Path(_util.ROOT)
PILOTS = ["explainer-orca", "explainer-blue-whale", "horror-pinned-rules"]


def fp(**kw):
    base = {
        "slug": "op-20261102-a-pistol-shrimp", "title": "The Shrimp That Shoots Bubbles Hotter Than The Sun",
        "hook": "This shrimp can stun a fish without touching it.", "topic": "pistol shrimp",
        "beat_seq": ["HOOK", "STAKES", "RUNG", "RUNG", "TURN", "PEAK", "TWIST", "STINGER"],
        "shot_mix": {"explainer/Ocean": 12, "explainer/Shrimp": 9, "explainer/Stat": 4},
        "subject": "explainer/Shrimp", "thumb_dhash": "0f0f0f0f0f0f0f0f", "cover_dhash": "00ff00ff00ff00ff",
        "frame_dhashes": [f"{i:016x}" for i in range(1, 11)], "source_id": "AAA",
        "narration_shingles": T.shingles("snap claw cavitation bubble collapses with a flash of light and heat " * 3),
    }
    base.update(kw)
    return base


OTHER = fp(slug="op-20261101-b-mantis-shrimp", title="Why A Mantis Shrimp Could Break Your Aquarium Glass",
           hook="Its punch is faster than a bullet leaving a pistol.", topic="mantis shrimp",
           beat_seq=["HOOK", "RUNG", "RUNG", "STAKES", "PEAK", "STINGER"],
           shot_mix={"explainer/Ocean": 10, "explainer/Mantis": 8, "explainer/SpeedBars": 3},
           subject="explainer/Mantis", thumb_dhash="f0f0f0f0f0f0f0f0", cover_dhash="ff00ff00ff00ff00",
           frame_dhashes=[f"{(i * 0x1f3b5d7f9eef) & 0xffffffffffffffff:016x}" for i in range(1, 11)], source_id="BBB",
           narration_shingles=T.shingles("the club accelerates like a twenty two calibre round and boils the water " * 3))


def metrics(res, level="FAIL"):
    return sorted({h["metric"] for h in res.get("hits", []) if h["level"] == level})


class TextSim(unittest.TestCase):
    def test_trigram_cosine_bounds(self):
        self.assertAlmostEqual(T.trigram_cosine("Why Orcas Never Attack", "why orcas never attack!"), 1.0)
        self.assertLess(T.trigram_cosine("Why Orcas Never Attack", "The Deepest Hole On Earth"), 0.3)
        self.assertEqual(T.trigram_cosine("", "x"), 0.0)

    def test_topic_aliases(self):
        self.assertTrue(T.same_topic("killer whale", "orca"))
        self.assertTrue(T.same_topic("orcas", "orca"))
        self.assertTrue(T.same_topic("orca hunting", "orca"))
        self.assertTrue(T.same_topic("white shark", "great white shark"))
        self.assertFalse(T.same_topic("blue whale", "sperm whale"))
        self.assertFalse(T.same_topic("blue whale", "orca"))

    def test_containment_and_hamming(self):
        a = T.shingles("one two three four five six seven eight nine ten")
        self.assertEqual(T.containment(a, a), 1.0)
        self.assertEqual(T.containment(a, T.shingles("eleven twelve thirteen fourteen fifteen sixteen")), 0.0)
        self.assertEqual(T.hamming_hex("ff", "0f"), 4)
        self.assertIsNone(T.hamming_hex(None, "0f"))

    def test_norm_edit_distance(self):
        self.assertEqual(T.norm_edit_distance(["A", "B"], ["A", "B"]), 0.0)
        self.assertAlmostEqual(T.norm_edit_distance(["A", "B", "C", "D"], ["A", "X", "C", "D"]), 0.25)


class Rules(unittest.TestCase):
    def test_distinct_passes(self):
        res = S.check(fp(), [OTHER])
        self.assertEqual(res["status"], "PASS", res["detail"])

    def test_no_history_passes(self):
        self.assertEqual(S.check(fp(), [])["status"], "PASS")

    def test_exact_duplicate_fails_everything(self):
        dup = copy.deepcopy(fp(slug="op-20261101-a-pistol-shrimp"))
        res = S.check(fp(), [dup])
        self.assertEqual(res["status"], "FAIL")
        self.assertEqual(metrics(res), ["frames_hamming", "hook", "script", "thumb_hamming", "title", "topic"])

    def _only(self, metric, **change):
        """OTHER with one field made close to fp(): exactly that FAIL fires."""
        old = dict(OTHER, **change)
        res = S.check(fp(), [old])
        self.assertEqual(res["status"], "FAIL", res["detail"])
        self.assertEqual(metrics(res), [metric], res["detail"])

    def test_title_paraphrase(self):
        self._only("title", title="The Shrimp That Shoots Bubbles Hotter Than the Sun!")

    def test_hook_paraphrase(self):
        self._only("hook", hook="This shrimp can stun a fish without even touching it.")

    def test_topic_alias(self):
        self._only("topic", topic="pistol shrimps")

    def test_thumbnail_close(self):
        self._only("thumb_hamming", thumb_dhash="0f0f0f0f0f0f0fff")  # 4 bits off

    def test_script_revoiced(self):
        self._only("script", narration_shingles=fp()["narration_shingles"])

    def test_same_cut_reencoded(self):
        near = [f"{i ^ 0x3:016x}" for i in range(1, 11)]  # every frame hash 1-2 bits off
        self._only("frames_hamming", frame_dhashes=near)

    def test_thresholds_are_inclusive_edges(self):
        def flip(h, k):  # h with its k lowest bits flipped
            return f"{int(h, 16) ^ ((1 << k) - 1):016x}"
        base = fp()["thumb_dhash"]
        far = dict(OTHER, thumb_dhash=flip(base, 8))  # 8 bits off: FAIL (<= 8)
        self.assertIn("thumb_hamming", metrics(S.check(fp(), [far])))
        far = dict(OTHER, thumb_dhash=flip(base, 9))  # 9 bits off: no FAIL
        self.assertNotIn("thumb_hamming", metrics(S.check(fp(), [far])))

    def test_warns_do_not_fail(self):
        old = dict(OTHER, shot_mix=fp()["shot_mix"], subject=fp()["subject"], source_id="AAA",
                   cover_dhash=fp()["cover_dhash"])
        res = S.check(fp(), [old])
        self.assertEqual(res["status"], "WARN", res["detail"])
        self.assertEqual(metrics(res, "WARN"), ["cover_hamming", "shot_mix", "source", "subject"])

    def test_beat_template_needs_three(self):
        same = dict(OTHER, beat_seq=fp()["beat_seq"])
        two = [dict(same, slug=f"s{i}", topic=f"t{i}") for i in range(2)]
        three = [dict(same, slug=f"s{i}", topic=f"t{i}") for i in range(3)]
        self.assertNotIn("beats_ned", metrics(S.check(fp(), two), "WARN"))
        self.assertIn("beats_ned", metrics(S.check(fp(), three), "WARN"))

    def test_value_shape_for_gate_json(self):
        res = S.check(fp(), [OTHER])
        self.assertEqual(set(res["value"]["max"]) >= {"title", "hook", "beats", "shot_mix", "thumb_hamming"}, True)
        self.assertEqual(res["value"]["vs"], [OTHER["slug"]])


class History(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.r = pathlib.Path(self.tmp.name)
        (self.r / "data").mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def posts(self, rows):
        with open(self.r / "data" / "posts.jsonl", "w") as f:
            for row in rows:
                f.write(json.dumps({"v": 1, **row}) + "\n")

    def test_latest_row_per_post_key_and_status(self):
        self.posts([
            {"post_key": "a:youtube", "slug": "a", "status": "draft", "at": "2026-11-02T10:00:00Z"},
            {"post_key": "a:youtube", "slug": "a", "status": "published", "published_at": "2026-11-02T17:00:00Z"},
            {"post_key": "b:youtube", "slug": "b", "status": "published", "published_at": "2026-11-03T17:00:00Z"},
            {"post_key": "c:youtube", "slug": "c", "status": "draft", "at": "2026-11-04T10:00:00Z"},
            {"post_key": "c:youtube", "slug": "c", "status": "failed", "at": "2026-11-04T11:00:00Z"},
            {"post_key": "d:tiktok", "slug": "d", "status": "scheduled", "scheduled_at": "2026-11-05T00:30:00Z"},
            {"post_key": "e:youtube", "slug": "e", "status": "deleted", "at": "2026-11-05T01:00:00Z"},
            {"post_key": "me:youtube", "slug": "me", "status": "draft", "at": "2026-11-06T01:00:00Z"},
        ])
        self.assertEqual(S.history_slugs(self.r, "me", 10), ["d", "b", "a"])
        self.assertEqual(S.history_slugs(self.r, "me", 2), ["d", "b"])

    def test_missing_ledger_is_empty(self):
        self.assertEqual(S.history_slugs(self.r, "x", 10), [])

    def test_run_reads_saved_fingerprints(self):
        self.posts([{"post_key": "old:youtube", "slug": "old", "status": "published", "published_at": "2026-11-01T00:00:00Z"}])
        F.save(self.r, dict(fp(), slug="old"))
        res = S.run(self.r, "new", fp(slug="new"), last_n=10)
        self.assertEqual(res["status"], "FAIL")
        self.assertEqual(res["value"]["vs"], ["old"])
        res = S.run(self.r, "new", fp(slug="new"), against=[])
        self.assertEqual(res["status"], "PASS")


class RealScripts(unittest.TestCase):
    """The thresholds must not fire on scripts that are really different (calibration guard)."""

    def test_pilot_fingerprints(self):
        fps = {s: F.build(s, ROOT, video=False) for s in PILOTS}
        self.assertEqual(fps["explainer-orca"]["title"], "The Killer Whale Has Never Killed You. Here's Why.")
        self.assertEqual(fps["explainer-orca"]["topic"], "orca")
        self.assertEqual(fps["explainer-orca"]["beat_seq"][0], "HOOK")
        self.assertEqual(fps["explainer-orca"]["beat_seq"][-1], "STINGER")
        self.assertTrue(fps["explainer-orca"]["thumb"].endswith("explainer-orca_explainer-eye_9x16.jpg"))
        self.assertTrue(fps["horror-pinned-rules"]["thumb"].endswith("horror-pinned-rules_horror-door_9x16.jpg"))
        for a, b in itertools.combinations(PILOTS, 2):
            res = S.check(fps[a], [fps[b]])
            self.assertNotEqual(res["status"], "FAIL", f"{a} vs {b}: {res['detail']}")

    def test_distinct_episode_scripts_stay_under_fail(self):
        # hand-made episodes only: op-* are operator runtime output (and selftest fixtures) on the Spark
        eps = sorted(p.name for p in (ROOT / "episodes").iterdir()
                     if (p / "script.md").is_file() and not p.name.startswith("op-"))
        fps = {}
        for s in eps:
            try:
                fps[s] = F.build(s, ROOT, video=False)
            except Exception:  # a script the TTS parser rejects is not this test's business
                continue
        if len(fps) < 6:
            self.skipTest(f"only {len(fps)} hand-made episodes here (a partial copy of the repo)")
        for a, b in itertools.combinations(fps, 2):
            p = S.pair(fps[a], fps[b])
            self.assertLess(p["title"], S.THRESH["title"], (a, b))
            self.assertLess(p["hook"], S.THRESH["hook"], (a, b))
            self.assertLess(p["script"], S.THRESH["script"], (a, b))
            self.assertFalse(p["topic"], (a, b))


if __name__ == "__main__":
    unittest.main()
