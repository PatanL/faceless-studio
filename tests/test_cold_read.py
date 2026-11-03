"""pipeline/qa/cold_read.py: prompt building and scoring against an answer key."""
import json
import os
import tempfile
import unittest

import _util  # noqa: F401
from pipeline.qa import cold_read as cr

KEY = {"slug": "t", "items": [
    {"id": "who-a", "part": "who", "text": "a smith", "all": [["smith"]]},
    {"id": "what-ring", "part": "what", "text": "the shield rings", "all": [["ring"]]},
    {"id": "why-tunnel", "part": "why", "text": "digging under", "all": [["dig", "tunnel"], ["under"]]},
    {"id": "twist", "part": "twist", "text": "the shield heard it", "all": [["shield"], ["heard", "detect"]]}]}


class TestColdRead(unittest.TestCase):
    def test_prompt_has_narration_and_no_title(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "s.md")
            open(p, "w").write("---\ntitle: Secret Title\n---\n```narration\n[sfx: tick] A smith listened.\n\nIt rang.\n```\n")
            out = cr.build_prompt(p)
        self.assertIn("A smith listened.", out)
        self.assertNotIn("Secret Title", out)
        self.assertNotIn("[sfx", out)

    def test_full_retell_passes(self):
        r = {"who": {"smith": "a smith"}, "what_happened": ["the shield rings"], "why": "they were digging under the wall",
             "twist": "the shield heard them", "reread_lines": [{"line": "x", "level": "slowed"}], "logic_jumps": []}
        s = cr.score(r, KEY, {})
        self.assertEqual(s["coverage"], {"who": 1.0, "what": 1.0, "why": 1.0, "twist": 1.0})
        self.assertTrue(s["passed"])
        self.assertEqual(s["friction"], 98.0)

    def test_lost_line_or_blocking_jump_fails(self):
        r = {"who": "smith", "what_happened": "ring", "why": "dig under", "twist": "shield detect",
             "reread_lines": [{"line": "x", "level": "lost"}]}
        self.assertFalse(cr.score(r, KEY, {})["passed"])
        r = {"who": "smith", "what_happened": "ring", "why": "dig under", "twist": "shield detect",
             "logic_jumps": [{"between": "a -> b", "blocks_understanding": True}]}
        self.assertFalse(cr.score(r, KEY, {})["passed"])

    def test_missed_beat_and_manual_grade(self):
        r = {"who": "smith", "what_happened": "ring", "why": "magic", "twist": "shield detect"}
        s = cr.score(r, KEY, {})
        self.assertEqual(s["coverage"]["why"], 0.0)
        self.assertEqual(cr.score(r, KEY, {"why-tunnel": 1})["coverage"]["why"], 1.0)


if __name__ == "__main__":
    unittest.main()
