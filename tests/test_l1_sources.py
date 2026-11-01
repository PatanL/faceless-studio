"""Lane L1: pipeline/sources.py (pick, skeleton, variant, originality vs the source) and auto.py beatmap.
Reads the real corpus/library files; writes only to temp dirs. No network, no claude."""
import json
import os
import tempfile
import unittest

import _util  # noqa: F401
from pipeline import sources as S


class Pick(unittest.TestCase):
    def test_rank_is_deterministic_and_scored(self):
        a, _ = S.rank("explainer")
        b, _ = S.rank("explainer")
        self.assertTrue(a, "no explainer candidates found in research/library + corpus")
        self.assertEqual([c["source_id"] for c in a[:10]], [c["source_id"] for c in b[:10]])
        self.assertEqual(a, sorted(a, key=lambda c: (-c["score"], c["source_id"])))

    def test_kit_fit_and_avoid(self):
        self.assertEqual(S.kit_fit("Why You'd Never Want To Meet A Sperm Whale")["component"], "explainer/SpermWhale")
        self.assertGreater(S.kit_fit("What It's Like To Fight The Deadliest Spiders")["penalty"], 0)

    def test_used_source_is_dropped_and_stale_pick_is_reusable(self):
        self.assertFalse(S.is_unused({"status": "used", "at": "2026-11-01T00:00:00Z"}))
        self.assertTrue(S.is_unused({"status": "picked", "at": "2020-01-01T00:00:00Z"}))
        self.assertFalse(S.is_unused({"status": "picked", "at": S.now_iso()}))

    def test_slug_and_ids(self):
        self.assertEqual(S.make_slug("20261102", "a", "pistol shrimp"), "op-20261102-a-pistol-shrimp")
        self.assertEqual(S.video_id("https://www.youtube.com/shorts/XFFjxTllpoA"), "XFFjxTllpoA")
        self.assertEqual(S.video_id("https://www.youtube.com/watch?v=fGcgWaswMns&t=3"), "fGcgWaswMns")


class Skeleton(unittest.TestCase):
    def check(self, src):
        sk = src["skeleton"]
        codes = [e["playbook"] for e in sk]
        self.assertEqual(codes[0], "S1")
        self.assertEqual(codes[-1], "S7")
        for c in ("S2", "S3", "S4", "S5"):
            self.assertIn(c, codes)
        self.assertEqual(codes, sorted(codes, key=S.PLAYBOOK_ORDER.index), "skeleton out of PLAYBOOK order")
        self.assertEqual(sk[0]["target_pct0"], 0)
        self.assertEqual(sk[-1]["target_pct1"], 100)
        for x, y in zip(sk, sk[1:]):
            self.assertAlmostEqual(x["target_pct1"], y["target_pct0"], delta=0.11)
        self.assertLessEqual(sk[0]["target_pct1"], 6.0)
        self.assertNotIn("CTA", [b["label"] for b in src["beats"] if b["playbook"]])

    def test_long_source_compresses_to_shorts_skeleton(self):
        src = S.skeleton("fGcgWaswMns")
        self.assertEqual(src["format"], "long")
        self.assertEqual(src["hook"]["code"], "H1")
        self.assertLessEqual(sum(1 for e in src["skeleton"] if e["playbook"] == "S3"), 4)
        self.check(src)

    def test_short_source_keeps_its_proportions(self):
        src = S.skeleton("XFFjxTllpoA")
        self.assertEqual(src["format"], "short")
        self.check(src)
        turn = next(e for e in src["skeleton"] if e["playbook"] == "S4")
        self.assertTrue(45 <= turn["target_pct0"] <= 65, turn)

    def test_parse_beat(self):
        b = S.parse_beat("ESC-2 prey it beats (1:50-2:42, 8.7%)", 599)
        self.assertEqual((b["label"], b["t0"], b["t1"]), ("ESC-2", 110, 162))
        self.assertEqual(S.category("CTA", 99), None)
        self.assertEqual(S.category("TURNSTILE", 46), "S4")


class Variant(unittest.TestCase):
    def test_overrides_are_validated(self):
        v = S.build_variant(None, ["hook.max_words=9", "visual.cover=eye"])
        self.assertEqual(v["values"]["hook.max_words"], 9)
        self.assertTrue(any("at most 9 words" in d for d in v["directives_by_step"]["script"]))
        with self.assertRaises(S.SourceError):
            S.build_variant(None, ["hook.max_words=40"])
        with self.assertRaises(S.SourceError):
            S.build_variant(None, ["no.such=1"])


class VsSource(unittest.TestCase):
    def test_copied_line_fails_and_original_passes(self):
        tr = S.transcript_file("XFFjxTllpoA")
        lines = S.read_transcript(tr)
        copied = lines[2][1]  # one verbatim source sentence
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "script.md")
            body = ("The reef looks calm at noon, and the water is warm enough to doze in. " * 3).strip()
            open(p, "w").write("---\nid: t\n---\n```narration\n" + body + "\n\n" + copied + "\n```\n")
            v = S.vs_source(p, tr)
            self.assertFalse(v["pass"], v)
            self.assertGreaterEqual(v["max_run"], 6)
            open(p, "w").write("---\nid: t\n---\n```narration\n" + body + "\n```\n")
            self.assertTrue(S.vs_source(p, tr)["pass"])


class Beatmap(unittest.TestCase):
    def test_beatmap_rows_follow_the_beat_plan_and_frames(self):
        from pipeline.episodes.auto import beatmap
        sb = {"fps": 30, "scenes": [{"id": "p01", "duration": 1.017, "layers": [{"type": "component", "name": "explainer/Orca"}],
                                     "notes": "a"}] * 4,
              "captions": {"words": [{"text": "a", "start": 0.1, "end": 0.3, "br": True}, {"text": "b", "start": 1.2, "end": 1.4, "br": True}]}}
        src = {"source_id": "x", "skeleton": [{"i": 0, "label": "HOOK", "playbook": "S1", "from_beats": [0], "target_pct0": 0, "target_pct1": 50},
                                              {"i": 1, "label": "STINGER", "playbook": "S7", "from_beats": [3], "target_pct0": 50, "target_pct1": 100}]}
        bm = beatmap("t", sb, [{}] * 4, {"beat_plan": "0 0 1 1"}, src)
        self.assertEqual(bm["beats_from"], "beat_plan")
        self.assertEqual([r["beat"] for r in bm["scenes"]], ["HOOK", "HOOK", "STINGER", "STINGER"])
        self.assertEqual(bm["scenes"][3]["t0"], round(round(3 * 1.017 * 30) / 30, 3))  # cumulative rounding (F20)
        self.assertEqual(bm["scenes"][1]["caption_pages"][0]["text"], "b")
        bm2 = beatmap("t", sb, [{}] * 4, {}, src)
        self.assertEqual(bm2["beats_from"], "timing")


if __name__ == "__main__":
    unittest.main()
