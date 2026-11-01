"""pipeline/make.py step logic with ssh/rsync/claude stubbed out (findings F01, F02, F04, F06)."""
import argparse
import os
import tempfile
import unittest

import _util  # noqa: F401
from pipeline import make as mk


def fake_make(tmp, **args):
    m = mk.Make.__new__(mk.Make)
    m.slug, m.niche = "t-ep", "explainer"
    m.ep = os.path.join(tmp, "ep")
    m.out = os.path.join(tmp, "out")
    os.makedirs(m.ep), os.makedirs(m.out)
    a = dict(script=None, rewrite=False, reshot=False, topic="x", review_rounds=1)
    a.update(args)
    m.a = argparse.Namespace(**a)
    m.logs = []
    m.log = m.logs.append
    m.sync = lambda *x, **k: None
    m.pull = lambda *x, **k: None
    m.fill = lambda *x, **k: "prompt"
    m.has_claude = lambda: True
    return m


def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


class Make(unittest.TestCase):
    @unittest.expectedFailure
    def test_F01_failed_claude_rewrite_is_not_success(self):
        """F01: claude exits 1 (auth/rate limit); the old script.md is still there. step_script must fail."""
        with tempfile.TemporaryDirectory() as tmp:
            m = fake_make(tmp, rewrite=True)
            write(os.path.join(m.ep, "script.md"), "Old script.\n")
            m.run = lambda *x, **k: ""

            def spark(cmd, check=True, **k):
                if "claude -p" in cmd:
                    if check:
                        raise mk.Fail("claude exited 1")
                    return "Error: authentication expired\n"
                return "PASS\n"
            m.spark = spark
            with self.assertRaises(mk.Fail):
                m.step_script()

    @unittest.expectedFailure
    def test_F02_new_script_invalidates_shots(self):
        """F02: after --rewrite / --script, an existing shots.json (old paragraphs/anchors) must be replanned."""
        with tempfile.TemporaryDirectory() as tmp:
            m = fake_make(tmp, rewrite=True, reshot=False)
            write(os.path.join(m.ep, "script.md"), "New para one.\n\nNew para two.\n")
            write(os.path.join(m.ep, "shots.json"), '{"scenes": []}')
            calls = []
            m.claude = lambda *x, **k: calls.append(x) or ""
            m.step_shots()
            self.assertTrue(calls, "shots: used the stale shots.json")

    @unittest.expectedFailure
    def test_F04_failed_review_round_keeps_last_good_shots(self):
        """F04: a review round that breaks shots.json must roll back to the last good one."""
        with tempfile.TemporaryDirectory() as tmp:
            m = fake_make(tmp)
            shots = os.path.join(m.ep, "shots.json")
            write(shots, "GOOD")
            m.stills_times = lambda: [0.0]
            m.run = lambda *x, **k: ""
            m.claude = lambda *x, **k: ""
            m.pull = lambda *x, **k: write(shots, "BROKEN")

            def bad_storyboard():
                raise mk.Fail("storyboard: auto build failed")
            m.step_storyboard = bad_storyboard
            try:
                m.step_review()
            except mk.Fail:
                pass
            self.assertEqual(open(shots).read(), "GOOD")

    @unittest.expectedFailure
    def test_F06_pull_failures_are_not_silent(self):
        """F06: pull() must not use check=False (or must verify the pulled file)."""
        with tempfile.TemporaryDirectory() as tmp:
            m = fake_make(tmp)
            seen = []
            m.run = lambda cmd, **k: seen.append(k.get("check", True))
            root = mk.ROOT
            mk.ROOT = tmp  # pull() makedirs under ROOT: keep it out of the repo
            try:
                mk.Make.pull(m, "episodes/t-ep/shots.json")
            finally:
                mk.ROOT = root
            self.assertNotIn(False, seen)


if __name__ == "__main__":
    unittest.main()
