"""pipeline/episodes/auto.py anchor resolution and write order (findings F05, F03)."""
import re
import unittest

import _util
from pipeline.episodes.auto import resolve
from pipeline.episodes.common import Scene


def scene():
    words = [{"text": "Mom", "start": 0.5, "end": 0.8}, {"text": "called", "start": 0.9, "end": 1.2}]
    return Scene(0, 0.0, 3.0, words, "Mom called")


class Resolve(unittest.TestCase):
    def test_time_key_anchor_resolves(self):
        """Regression guard (passes today)."""
        errs = []
        out = resolve({"at": "@mom"}, scene(), errs, "p")
        self.assertEqual(out["at"], 0.5)
        self.assertEqual(errs, [])

    def test_F05_chat_text_starting_with_at_is_not_an_anchor(self):
        """F05: {'text': '@Mom'} is chat text and must stay a string."""
        out = resolve({"text": "@Mom", "at": "@mom"}, scene(), [], "p")
        self.assertEqual(out["text"], "@Mom")

    def test_F05_hash_in_chat_text_does_not_crash(self):
        """F05: '@Admin who is member #41?' raised an uncaught ValueError from int()."""
        out = resolve({"text": "@Admin who is member #41?"}, scene(), [], "p")
        self.assertEqual(out["text"], "@Admin who is member #41?")


class AnchorGrammar(unittest.TestCase):
    def test_bad_occurrence_under_time_key_is_an_error_not_a_crash(self):
        errs = []
        out = resolve({"at": "@mom#2x"}, scene(), errs, "p")
        self.assertEqual(out["at"], "@mom#2x")
        self.assertTrue(errs and "bad anchor" in errs[0], errs)

    def test_time_lists_nest(self):
        errs = []
        out = resolve({"talk": [["@mom", "@called.end"]]}, scene(), errs, "p")
        self.assertEqual(out["talk"], [[0.5, 1.2]])
        self.assertEqual(errs, [])

    def test_ambiguous_from_key(self):
        """'from' is a time for Heartbeat/Flicker and text for EndCard / chat messages."""
        errs = []
        out = resolve({"a": {"from": "@called"}, "b": {"from": "June (3B)"}, "c": {"from": "@Mom", "text": "hi"}},
                      scene(), errs, "p")
        self.assertEqual(out["a"]["from"], 0.9)
        self.assertEqual(out["b"]["from"], "June (3B)")
        self.assertEqual(out["c"]["from"], "@Mom")
        self.assertEqual(errs, [])


class WriteOrder(unittest.TestCase):
    def test_F03_zod_runs_before_storyboard_is_written(self):
        """F03 (static check): build() writes a temp file, validates it, and only then os.replace()s it over
        storyboard.json, so a zod failure keeps the last good file."""
        src = _util.read("pipeline/episodes/auto.py")
        body = src[src.index("def build("):src.index("def main(")]
        self.assertNotIn('open(path, "w")', body, "storyboard.json opened for writing directly")
        tmp_write = body.find('open(tmp, "w")')
        zod = body.find("zod_validate(tmp)")
        replace = body.find("os.replace(tmp, path)")
        self.assertTrue(-1 < tmp_write < zod < replace, (tmp_write, zod, replace))

if __name__ == "__main__":
    unittest.main()
