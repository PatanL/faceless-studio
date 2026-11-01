"""scripts/plot_similarity.py plot gate. Black-box: runs the script on temp scripts against the real
horror-cn corpus annotations (research/corpus/horror-cn/BV*.md). python3 only, no network.

The fixtures below are test inputs, not stories for publication. TOO_CLOSE is a deliberately lazy
"transposition" of BV1fR7szYEDq (names and setting swapped, the specific event chain kept) so the gate
has something to catch. TRANSPOSED reuses the same source's GENERIC mechanics (night knock with a
familiar name, an authority alone at the door, a third party phoning to contradict him, a logistics
impossibility, a phone ringing behind a wall, group-chat disbelief, a volunteer's livestream) with new
specifics, and must PASS.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

import _util

CHECK = os.path.join(_util.ROOT, "scripts", "plot_similarity.py")
CORPUS = os.path.join(_util.ROOT, "research", "corpus", "horror-cn")
DINO = os.path.join(CORPUS, "BV1fR7szYEDq.md")
SIEGE = os.path.join(CORPUS, "BV1nEoYBBEXE.md")


def script_md(paragraphs):
    body = "\n\n".join(paragraphs)
    return ("---\nid: test\nniche: horror\n---\n\n# Test\n\n## Narration\n\n```narration\n"
            + body + "\n```\n")


def run(paragraphs, *sources, as_json=True):
    with tempfile.TemporaryDirectory() as d:
        sp = os.path.join(d, "script.md")
        with open(sp, "w", encoding="utf-8") as f:
            f.write(script_md(paragraphs))
        cmd = [sys.executable, "-I", CHECK, sp, *sources] + (["--json"] if as_json else [])
        r = subprocess.run(cmd, capture_output=True, text=True)
        return r.returncode, (json.loads(r.stdout) if as_json and r.stdout.strip().startswith("{") else r.stdout)


# Lazy rename of BV1fR7szYEDq: new names, US vocabulary, same specific combination and order.
TOO_CLOSE = [
    "The zoo where I work bred a baby dinosaur, and the director got rich selling tickets to see it.",
    "Six months later it knocked on my apartment door at night. Dad, open up, I'm hungry, it said.",
    "My coworker Mike called. It escaped. He admitted the director spliced my DNA into it so it would be smart enough to perform.",
    "My neighbor came out to complain about the noise and it pinned her. She begged me to help. I locked my door.",
    "Through the peephole I watched it press her hand to her fingerprint lock and drag her inside.",
    "It ate her on the balcony where I could see, and when it finished it grew half a meter taller.",
    "The director arrived with a tranquilizer gun and a net. I told him to bring a rifle. He said treat it like a child.",
    "Then he knocked alone and asked to come in for a glass of water.",
    "Mike texted me. He only brought two keepers. Two keepers can't carry a four hundred kilo animal down eight floors.",
    "I called one of the keepers. His ringtone came from the apartment next door.",
    "You could just run downstairs, I told him. It's standing behind you.",
    "The police shot it. Mike called. Did they suspect you? No. The zoo is ours now.",
]

# Original suburban story built on the same source's GENERIC mechanics only.
TRANSPOSED = [
    "At two a.m. the Larkspur Court neighborhood app pinged. Storm drain flooding, stay indoors, the board is handling it.",
    "Then someone knocked, soft and patient. A voice through the wood said, Bug, it's Grandpa, I forgot my key. Grandpa has been gone nine years. Only he called me Bug.",
    "I texted my sister. She replied in seconds. Don't you dare. Nobody alive calls you that.",
    "The knocking stopped. Through the doorbell camera I saw Mr. Pruitt, the board president, in his yellow rain slicker, alone on my porch.",
    "He said he was checking every water shutoff on the street and needed two minutes in my laundry room.",
    "My sister texted again. Pruitt is at his lake cabin all week. He posted pictures of the dock an hour ago.",
    "He said he had walked over from the clubhouse in the downpour. On the camera, his slicker and his shoes were bone dry.",
    "I called the number on his board flyer. Somewhere inside my own garage, a phone started to ring.",
    "I posted in the street chat. Mr. Pruitt is on my porch and his phone is in my garage. Somebody laughed and asked if I was sleepwalking again.",
    "Dana from number nine said she'd walk over and film it so I'd calm down. Her video showed my porch light, the rain, and nobody there.",
    "Then Dana turned the camera toward her own front window. Mr. Pruitt was standing in her living room, waving.",
    "My doorbell chimed. The little screen said Visitor recognized: Grandpa. I never saved his face.",
]


class PlotSimilarity(unittest.TestCase):
    def test_too_close_lazy_rename_fails(self):
        rc, out = run(TOO_CLOSE, DINO)
        self.assertEqual(rc, 1, out)
        res = out["results"][0]
        self.assertEqual(res["verdict"], "FAIL")
        self.assertGreaterEqual(len(res["chain"]), 3, res)
        joined = " ".join(" ".join(c["shared"]) for c in res["chain"])
        self.assertTrue(any(w in joined for w in ("dinosaur", "keeper", "balcony", "director")), joined)

    def test_too_close_even_with_new_monster(self):
        """Swapping the creature is not enough: the authority-at-the-door chain is still the source's."""
        mid = [
            "The wildlife park kept a grizzly in the night enclosure, and the owner loved the money it made.",
            "Tonight it got loose. The owner came with a tranquilizer and a net. I told him to bring a rifle.",
            "Later he knocked on my door alone and asked to come in for some water.",
            "My coworker texted me. He only brought two keepers. Two men can't carry a four hundred kilo bear down eight floors.",
            "I called one of the keepers. His ringtone came from the unit next door.",
            "You could just run downstairs, I said. It's behind you.",
        ]
        rc, out = run(mid, DINO)
        self.assertEqual(rc, 1, out)
        self.assertGreaterEqual(len(out["results"][0]["chain"]), 3, out)

    def test_transposed_generic_mechanics_pass(self):
        rc, out = run(TRANSPOSED, DINO)
        self.assertEqual(rc, 0, out)
        res = out["results"][0]
        self.assertEqual(res["verdict"], "PASS")
        self.assertLess(len(res["chain"]), 3, res)
        # It really does share the source's generic mechanics, and that is allowed.
        self.assertGreaterEqual(len(res["generic_mechanics_shared"]), 3, res)

    def test_transposed_passes_whole_corpus(self):
        rc, out = run(TRANSPOSED, CORPUS)
        self.assertEqual(rc, 0, out)
        self.assertEqual(len(out["results"]), 10, [r["source"] for r in out["results"]])

    def test_generic_mechanics_alone_pass(self):
        """Knock, fake authority, count clue, group chat, ringtone, cut signal: all mechanics, no specifics."""
        generic = [
            "Our group chat said the danger was over and the police were going door to door.",
            "Someone knocked three times. A calm voice said it was the police and asked me to open the door.",
            "I counted the messages in the chat. Too many neighbours had replied too fast.",
            "My phone had no signal. The chat still worked, and everyone kept telling me to open the door.",
            "I called the number from the warning. A phone rang right outside my door.",
            "The voice knew my name. Then it knew my mother's name. I did not open the door.",
        ]
        rc, out = run(generic, CORPUS)
        self.assertEqual(rc, 0, out)

    def test_names_plus_clue_fails(self):
        """A short script that keeps a source name and a signature clue fails even without a chain."""
        rc, out = run([
            "Li Ping texted me at midnight from the flat below.",
            "She said there were bloody footprints in the lift and I must not answer.",
            "I went back to bed.",
        ], SIEGE)
        self.assertEqual(rc, 1, out)
        res = out["results"][0]
        self.assertIn("li ping", res["names"])
        self.assertTrue(res["clues"], res)

    def test_text_report_lists_overlaps(self):
        rc, out = run(TOO_CLOSE, DINO, as_json=False)
        self.assertEqual(rc, 1, out)
        self.assertIn("FAIL", out)
        self.assertIn("event chain", out)
        self.assertTrue(out.rstrip().endswith("FAIL"), out)

    def test_pilot_scripts_pass(self):
        """Our published horror originals must not trip the gate (false-positive guard)."""
        eps = os.path.join(_util.ROOT, "episodes")
        if not os.path.isdir(eps):
            self.skipTest("no episodes/")
        checked = 0
        for name in sorted(os.listdir(eps)):
            sp = os.path.join(eps, name, "script.md")
            if name.startswith("horror-") and os.path.isfile(sp):
                r = subprocess.run([sys.executable, "-I", CHECK, sp, CORPUS], capture_output=True, text=True)
                self.assertEqual(r.returncode, 0, name + "\n" + r.stdout)
                checked += 1
        if not checked:
            self.skipTest("no horror episodes")


if __name__ == "__main__":
    unittest.main()
