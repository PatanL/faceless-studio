"""House-style QA gate checks (pipeline/qa/house_style.py): thresholds calibrated on the new (Lantern & Ink) and the
old-kit orca, the storyboard 'built in the house style' check, and the staging checker wiring. python3 only."""
import json
import pathlib
import subprocess
import unittest

import _util  # noqa: F401

from pipeline.qa import house_style as H

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "experiments" / "kurz-style" / "data" / "house"


class Thresholds(unittest.TestCase):
    def test_new_orca_passes_every_fail_line(self):
        st, rows, fails, _ = H.evaluate(json.loads((DATA / "judge_lantern_orca_full_v2.json").read_text()))
        self.assertEqual(fails, [])
        self.assertNotEqual(st, "FAIL")

    def test_old_kit_orca_fails_on_house_metrics(self):
        st, rows, fails, _ = H.evaluate(json.loads((DATA / "judge_orca.json").read_text()))
        self.assertEqual(st, "FAIL")
        self.assertEqual({f.split()[0] for f in fails}, {"P5", "D3", "D4", "D5", "M5"})

    def test_old_kit_9x16_numbers_fail(self):
        # old_orca_9x16 as measured on the Spark (house_metrics.py == judge_metrics.sh)
        m = {"pal_sat_chroma": 0.685, "pal_grey": 0.0275, "pal_hue_fam": 1.0, "pal_pure_white": 0.0044,
             "density_shapes": 103, "density_micro": 714, "specks_small": 63.5, "fm_edge_den": 0.0294, "fm_outline": 0.13,
             "alive_pct": 98.58, "longest_quiet_s": 0.93, "sec_per_new": 10.6, "sec_per_change": 2.0,
             "hard_cuts_per_min": 7.99}
        st, _, fails, _ = H.evaluate(m)
        self.assertEqual({f.split()[0] for f in fails}, {"P5", "D3", "D4", "D5", "M5"})

    def test_missing_metric_warns(self):
        st, rows, fails, warns = H.evaluate({})
        self.assertEqual(st, "WARN")
        self.assertEqual(len(warns), len(H.THRESHOLDS))


class Storyboard(unittest.TestCase):
    def test_live_orca_storyboard_passes_staging(self):
        sb = json.loads((ROOT / "episodes" / "explainer-orca" / "storyboard.json").read_text())
        self.assertEqual(H.check_staging(sb, "explainer")["status"], "PASS")

    def test_old_kit_storyboard_fails(self):
        try:
            old = subprocess.run(["git", "-C", str(ROOT), "show", "0413c5c:episodes/explainer-orca/storyboard.json"],
                                 capture_output=True, text=True, check=True).stdout
        except (OSError, subprocess.CalledProcessError):
            self.skipTest("no git history")
        c = H.check_staging(json.loads(old), "explainer")
        self.assertEqual(c["status"], "FAIL")
        self.assertIn("no scene light", c["value"]["fail"][0])

    def test_horror_is_out_of_scope(self):
        sb = json.loads((ROOT / "episodes" / "horror-pinned-rules" / "storyboard.json").read_text())
        self.assertEqual(H.check_staging(sb, "horror")["status"], "PASS")
        self.assertEqual(H.check_house_style(ROOT, None, ROOT, "horror", sb)["status"], "PASS")

    def test_off_spark_metrics_warn_without_running(self):
        import os
        if H.on_spark(ROOT) or os.environ.get("STUDIO_HOUSE_PY"):
            self.skipTest("on the Spark the metrics really run")
        c = H.check_house_style(ROOT, "/nonexistent.mp4", ROOT / "out" / "_t", "explainer", None)
        self.assertEqual(c["status"], "WARN")


if __name__ == "__main__":
    unittest.main()
