"""scripts/originality_check.py gate (findings F22-F24). Black-box: runs the script on temp files."""
import os
import subprocess
import sys
import tempfile
import unittest

import _util

CHECK = os.path.join(_util.ROOT, "scripts", "originality_check.py")


def filler(n, tag):
    # unique, non-overlapping tokens: never share 5-grams with any source
    return " ".join(f"{tag}{i}" for i in range(n))


def run(script_md, sources):
    with tempfile.TemporaryDirectory() as d:
        sp = os.path.join(d, "script.md")
        with open(sp, "w", encoding="utf-8") as f:
            f.write(script_md)
        src = os.path.join(d, "src")
        os.makedirs(src)
        for name, text in sources.items():
            with open(os.path.join(src, name), "w", encoding="utf-8") as f:
                f.write(text)
        r = subprocess.run([sys.executable, CHECK, sp, src], capture_output=True, text=True)
        return r.returncode, r.stdout


class Originality(unittest.TestCase):
    def test_copied_run_inside_one_line_fails(self):
        """Regression guard (passes today): a 12-word copy within one transcript line FAILs."""
        sentence = "it drains your blood of oxygen sends your body into violent seizures"
        rc, out = run(filler(300, "q") + " " + sentence + ".\n",
                      {"a.txt": "https://x 1000 3.0\n[00:05] " + sentence + " and more\n"})
        self.assertEqual(rc, 1, out)

    @unittest.expectedFailure
    def test_F22_timestamp_between_lines_hides_copied_run(self):
        """F22: '[00:09]' between transcript lines splits a 12-word copy into runs of <= 6 words -> false PASS."""
        src = ("https://x 1000 3.0\n[00:05] It drains your blood of oxygen,\n"
               "[00:09] sends your body into violent\n[00:12] seizures, and stops you cold.\n")
        script = filler(600, "q") + " It drains your blood of oxygen, sends your body into violent seizures, and stops you cold.\n"
        rc, out = run(script, {"a.txt": src})
        self.assertEqual(rc, 1, out)

    @unittest.expectedFailure
    def test_F23_curly_apostrophe_hides_copied_run(self):
        """F23: "don’t" (U+2019) vs "don't" tokenizes differently -> a 15-word copy PASSes."""
        sent = "sugar seems innocent at first and you {} know it but it can be lethal"
        script = filler(600, "q") + " " + sent.format("don’t") + ".\n"
        rc, out = run(script, {"a.txt": "[00:01] " + sent.format("don't") + "\n"})
        self.assertEqual(rc, 1, out)

    @unittest.expectedFailure
    def test_F24_producer_notes_dilute_ngram_share(self):
        """F24: only narration should count. 3 shared 5-grams in ~96 narration 5-grams (3.1%) is a FAIL,
        but 200 words of notes outside the narration block push it under 2%."""
        copied = "the ocean floor hides older scars"  # 6 words -> 2 shared 5-grams, under the 8-word run rule
        copied2 = "nobody has mapped it all yet"
        narration = filler(45, "n") + " " + copied + " " + filler(40, "m") + " " + copied2 + "\n"
        script = ("# Title\n\n**Premise** " + filler(200, "note") + "\n\n```narration\n" + narration + "```\n")
        rc, out = run(script, {"a.txt": "[00:01] " + copied + "\n\n" + copied2 + "\n"})
        self.assertEqual(rc, 1, out)


if __name__ == "__main__":
    unittest.main()
