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

    @unittest.expectedFailure
    def test_F05_chat_text_starting_with_at_is_not_an_anchor(self):
        """F05: {'text': '@Mom'} is chat text and must stay a string."""
        out = resolve({"text": "@Mom", "at": "@mom"}, scene(), [], "p")
        self.assertEqual(out["text"], "@Mom")

    @unittest.expectedFailure
    def test_F05_hash_in_chat_text_does_not_crash(self):
        """F05: '@Admin who is member #41?' raised an uncaught ValueError from int()."""
        out = resolve({"text": "@Admin who is member #41?"}, scene(), [], "p")
        self.assertEqual(out["text"], "@Admin who is member #41?")


class WriteOrder(unittest.TestCase):
    @unittest.expectedFailure
    def test_F03_zod_runs_before_storyboard_is_written(self):
        """F03 (static check): build() must validate before replacing storyboard.json
        (validate a temp file, then os.replace), so a zod failure keeps the last good file."""
        src = _util.read("pipeline/episodes/auto.py")
        body = src[src.index("def build("):src.index("def main(")]
        writes = [m.start() for m in re.finditer(r'open\(path, "w"\)', body)]
        zod = body.find("zod_validate(")
        self.assertTrue(writes and zod != -1)
        self.assertTrue("os.replace" in body or zod < writes[0], "storyboard.json is written before zod_validate")


if __name__ == "__main__":
    unittest.main()
