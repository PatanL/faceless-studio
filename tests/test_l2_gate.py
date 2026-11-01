"""L2 gate checks (pipeline/qa/gate.py) on synthetic fixtures (design 7.5).

The originality and storyboard checks are pure python. The media tests build tiny clips with ffmpeg's lavfi sources
(108x192, 10 fps: well under a second of CPU each) and are skipped when ffmpeg or numpy is missing:
a 1 s black gap FAILs black_frames, a 55 s cut FAILs duration, a magenta "missing" box FAILs missing_kit, and a
clean 62 s clip passes those three.
"""
import json
import pathlib
import shutil
import subprocess
import tempfile
import unittest

import _util  # noqa: F401

from pipeline.qa import gate as G

ROOT = pathlib.Path(_util.ROOT)
SOURCE_LINE = "the pressure down there would fold a submarine like a soda can"
SOURCE_TXT = ("https://example.invalid/v SRC1 1000000 views\n[00:01] nobody has ever been this deep and come back\n"
              f"[00:04] {SOURCE_LINE}\n[00:09] and still something lives there\n")
ORIGINAL = ("You are standing on the floor of the deepest trench. Every square centimetre of you "
            "carries the weight of a small car. Your lungs would shrink to the size of two lemons. And yet, a pale "
            "fish drifts past your mask as if nothing were wrong. It has no swim bladder to crush. Its cells are "
            "packed with a molecule that keeps proteins in shape. Down here, being soft is the armour.")


def have_media():
    try:
        import numpy  # noqa: F401
    except ImportError:
        return False
    try:
        from pipeline.qa.util import tool
        tool("ffmpeg")
        tool("ffprobe")
        return True
    except RuntimeError:
        return False


def make_episode(r: pathlib.Path, slug: str, narration: str) -> None:
    ep = r / "episodes" / slug
    (ep / "audio").mkdir(parents=True)
    (ep / "script.md").write_text(
        f"---\nid: {slug}\nniche: explainer\ntitle: Test {slug}\nreferences:\n"
        "  - id: SRC1, url: https://example.invalid/v, views: 1000000, outlier_score: 5\n---\n\n"
        f"# Test\n\n## Narration\n\n```narration\n{narration}\n```\n", encoding="utf-8")
    (ep / "storyboard.json").write_text(json.dumps({"fps": 30, "format": "9:16", "scenes": []}))
    (ep / "audio" / "captions.json").write_text(json.dumps({"words": [{"text": "You", "start": 0.1, "end": 0.3}]}))
    (ep / "description.md").write_text("Narration: synthetic AI voice (Kokoro TTS). Animation: original 2D vector art.\n")
    tr = r / "research" / "library" / "transcripts"
    tr.mkdir(parents=True, exist_ok=True)
    (tr / "SRC1.txt").write_text(SOURCE_TXT)
    (r / "research" / "corpus" / "explainer").mkdir(parents=True, exist_ok=True)


def make_clip(path: pathlib.Path, dur: float, vf: str = "null") -> None:
    """Grey moving test pattern (testsrc2's colour bars include magenta, which is the kit's 'missing' colour)."""
    from pipeline.qa.util import tool
    path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [tool("ffmpeg"), "-nostdin", "-hide_banner", "-loglevel", "error", "-y", "-threads", "2",
           "-f", "lavfi", "-i", f"testsrc2=s=108x192:r=10:d={dur}", "-f", "lavfi", "-i", f"sine=f=330:d={dur}",
           "-vf", f"format=gray,format=yuv420p,{vf}", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(path)]
    subprocess.run(cmd, check=True, capture_output=True)


class Originality(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.r = pathlib.Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def run_check(self, narration):
        make_episode(self.r, "t", narration)
        script = self.r / "episodes" / "t" / "script.md"
        from pipeline.qa.util import front_matter
        return G.check_originality(self.r, "t", script, {}, front_matter(script.read_text()), "explainer")

    def test_original_passes(self):
        c = self.run_check(ORIGINAL)
        self.assertEqual(c["status"], "PASS", c)
        self.assertEqual(c["value"]["source_id"], "SRC1")
        self.assertEqual(c["value"]["source_transcript"], "research/library/transcripts/SRC1.txt")

    def test_copied_nine_word_source_line_fails(self):
        nine = " ".join(SOURCE_LINE.split()[:9])  # "the pressure down there would fold a submarine like"
        c = self.run_check(ORIGINAL + f" Honestly, {nine} nothing.")
        self.assertEqual(c["status"], "FAIL", c)
        self.assertGreaterEqual(c["value"]["vs_source_run"], 9)
        self.assertIn("vs source SRC1", c["detail"])

    def test_six_word_run_vs_source_fails_even_under_corpus_limit(self):
        six = " ".join(SOURCE_LINE.split()[4:10])  # "would fold a submarine like a"
        c = self.run_check(ORIGINAL + f" It {six} paper cup.")
        self.assertEqual(c["status"], "FAIL", c)
        self.assertLess(c["value"]["max_run"], 8)  # the corpus rule alone would have passed it

    def test_longest_run(self):
        a = "x the cat sat on the mat y".split()
        b = "a dog and the cat sat on the mat today".split()
        self.assertEqual(G._longest_run(a, b, 3), 6)
        self.assertEqual(G._longest_run(a, b, 7), 0)


class Storyboard(unittest.TestCase):
    def test_pilots_have_no_safe_area_fail(self):
        for s in ("explainer-orca", "explainer-blue-whale", "horror-pinned-rules"):
            sb = json.loads((ROOT / "episodes" / s / "storyboard.json").read_text())
            self.assertNotEqual(G.check_safe_area(sb)["status"], "FAIL", s)

    def test_caption_clamp_matches_renderer(self):
        sb = {"format": "9:16", "fps": 30, "captions": {"words": [{"text": "a", "start": 0, "end": 1}],
                                                        "style": {"fontSize": 84, "y": 0.95}},
              "scenes": [{"id": "p00", "duration": 2, "layers": []}]}
        y = G.caption_ys(sb["scenes"][0], sb["captions"]["style"], sb)[0]
        self.assertAlmostEqual(y * 1920, 1920 - 440 - 0.6 * 84, places=3)  # captions.tsx yMax

    def test_screen_fixed_text_low_fails(self):
        sb = {"format": "9:16", "fps": 30, "captions": {},
              "scenes": [{"id": "p00", "duration": 2, "layers": [
                  {"type": "component", "name": "explainer/Headline", "x": "50%", "y": "88%", "width": 900, "height": 120,
                   "depth": 0}]}]}
        self.assertEqual(G.check_safe_area(sb)["status"], "FAIL")

    def test_stopword_emphasis_warns(self):
        sb = {"captions": {"words": [{"text": "the", "start": 0, "end": 0.2, "emph": True}]}, "scenes": []}
        self.assertEqual(G.check_captions(sb, None)["status"], "WARN")

    def test_scene_times_are_frame_accurate(self):
        sb = {"fps": 30, "scenes": [{"duration": 1.017}] * 4}
        starts = [round(t0 * 30) for t0, _, _ in G.scene_times(sb)]
        self.assertEqual(starts, [0, 31, 61, 92])  # round(cum * fps), no drift (F20)


@unittest.skipUnless(have_media(), "needs ffmpeg/ffprobe and numpy")
class Media(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.r = pathlib.Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def gate(self, slug, dur, vf="null"):
        make_episode(self.r, slug, ORIGINAL)
        make_clip(self.r / "out" / slug / f"{slug}_9x16.mp4", dur, vf)
        return G.gate(slug, self.r, against=[], sheets=False, log=lambda *_: None)

    def test_clean_clip(self):
        g = self.gate("clean", 62)
        for k in ("duration", "black_frames", "missing_kit", "frozen", "originality", "disclosure", "hook", "sameness"):
            self.assertEqual(g["checks"][k]["status"], "PASS", (k, g["checks"][k]))
        self.assertEqual(len(g["mp4_sha256"]), 64)

    def test_black_gap_fails(self):
        g = self.gate("black", 62, "drawbox=enable='between(t,20,21)':color=black:t=fill")
        self.assertEqual(g["checks"]["black_frames"]["status"], "FAIL")
        run = g["checks"]["black_frames"]["value"][0]
        self.assertAlmostEqual(run["t0"], 20.0, delta=0.2)
        self.assertGreaterEqual(run["d"], 0.9)
        self.assertEqual(g["checks"]["duration"]["status"], "PASS")
        self.assertEqual(g["verdict"], "FAIL")

    def test_short_cut_fails(self):
        g = self.gate("short", 55)
        self.assertEqual(g["checks"]["duration"]["status"], "FAIL")
        self.assertEqual(g["fail"], ["duration"] + [k for k in g["fail"] if k != "duration"])

    def test_magenta_box_fails(self):
        g = self.gate("magenta", 62, "drawbox=x=20:y=50:w=50:h=50:color=0xFF00FF:t=fill")
        self.assertEqual(g["checks"]["missing_kit"]["status"], "FAIL", g["checks"]["missing_kit"])
        self.assertGreater(g["checks"]["missing_kit"]["value"], 0.05)


if __name__ == "__main__":
    unittest.main()
