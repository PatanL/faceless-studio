"""pipeline/qa/script_judge.py: sentence split, beat heuristics, scoring, and calibration on the 24 references."""
import json
import os
import statistics as st
import tempfile
import unittest

import _util  # noqa: F401  (puts the repo on sys.path)
from pipeline.qa import script_judge as sj

GOOD = """---
id: t
---
```narration
[sfx: tick] A smith kept laying his shield face-down in the dirt while an army camped outside the walls.

The guards think the siege has cracked him.

It's a city on the coast, and the enemy has it surrounded for months.

Then one week the attacks stop, and the camp goes quiet.

That's when the smith starts walking the inside of the wall and kneeling to listen.

"Lost something?" a guard laughs.

For days, nothing.

Then, by the tower, the shield rings, and the dust on it shivers.

You see, the enemy had stopped attacking the wall because they were digging under it.

Over solid ground the bronze thuds, but over a hollow tunnel every pick below makes it hum.

So wherever it rang, the defenders dug down and broke into the tunnel.

An army dug for months in silence, and a shield in the dirt heard every swing.
```
"""


class TestScriptJudge(unittest.TestCase):
    def test_split_keeps_quotes(self):
        s = sj.split_sentences('He says, "Only God knows." Nobody is punished. "Lost something?" a guard laughs.')
        self.assertEqual(s, ['He says, "Only God knows."', "Nobody is punished.", '"Lost something?" a guard laughs.'])

    def test_numbers(self):
        self.assertEqual(sj.numbers("Thirty men, 1628, seventy-two guns and a dog"), ["Thirty", "1628", "seventy-two"])

    def test_good_script_beats(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "script.md")
            open(p, "w").write(GOOD)
            paras, _ = sj.read_narration(sj.pathlib.Path(p))
        sents = [s for x in paras for s in sj.split_sentences(x)]
        r = sj.run_one("t", sents, None, None, None, None)
        self.assertEqual(r["beats"]["pivot"], 9)  # the "You see" sentence
        self.assertGreaterEqual(len(r["beats"]["esc"]), 2)
        self.assertGreater(r["score"], 70)  # short toy script: loses only the length checks

    def test_question_hook_and_question_ending_lose_points(self):
        sents = ["Have you ever wondered why ships sink?", "They just do.", "Would you sail one?"]
        r = sj.run_one("t", sents, None, None, None, None)
        checks = {c["check"]: c for c in r["checks"]}
        self.assertLess(checks["hook_form"]["score"], 1)
        self.assertLess(checks["last_line"]["score"], 1)

    def test_beats_override(self):
        sents = [f"Sentence number {i} has a few words in it." for i in range(1, 13)]
        r = sj.run_one("t", sents, None, None, "E=3-4,5-6,7;P=8;M=8-10;L=12", None)
        self.assertEqual(r["beats"]["esc"], [[3, 4], [5, 6], [7]])
        self.assertEqual(r["beats"]["pivot"], 8)
        self.assertEqual(r["beats"]["mech"], [8, 9, 10])

    def test_timings_measure_pace_and_gaps(self):
        sents = ["One two three four.", "Five six seven eight."]
        words = [dict(text=w, start=i * 0.3, end=i * 0.3 + 0.25) for i, w in enumerate("One two three four. Five six seven eight.".split())]
        for w in words[4:]:  # a 0.55 s gap before "Five"
            w["start"] += 0.5
            w["end"] += 0.5
        r = sj.run_one("t", sents, words, None, None, None)
        p = r["metrics"]["pauses"]
        self.assertEqual(r["metrics"]["timing"], "measured")
        self.assertEqual(p["n_ge_400ms"], 1)

    @unittest.skipUnless(sj.REFS.is_file(), "ricks24_beats.json not present")
    def test_calibration_top_beats_rest(self):
        refs = json.loads(sj.REFS.read_text())["videos"]
        by = {"top": [], "rest": []}
        for vid, d in refs.items():
            _, sents, timed = sj.ref_input(vid)
            r = sj.run_one(vid, sents, timed, d["duration_s"], None, None)
            by["top" if d["tier"] == "top" else "rest"].append(r["score"])
        self.assertGreater(st.median(by["top"]), st.median(by["rest"]) + 10)


if __name__ == "__main__":
    unittest.main()
