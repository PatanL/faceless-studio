"""pipeline/audio/emphasis.py: rule-based stress marks (research/music/VOICE_CADENCE.md section 3)."""
import unittest

import _util  # noqa: F401
from pipeline.audio import emphasis as E


def marked(text, **kw):
    return {m.word.strip(".,!?\"'").lower(): m.reason for m in E.mark(text, **kw)}


class EmphasisRules(unittest.TestCase):
    def test_hook_act_verb_object_and_end(self):
        m = marked("He sawed gaps into a railroad every few feet.")
        self.assertEqual(m.get("sawed"), "act verb")
        self.assertIn("gaps", m)
        self.assertNotIn("he", m)

    def test_numbers_contrast_and_turn(self):
        t = "He opened the box. Inside were twelve keys, but only one fit. You see, the lock was new."
        m = marked(t)
        self.assertIn("twelve", m)
        self.assertTrue("only" in m or "but" in m)
        self.assertEqual(m.get("see"), "turn")

    def test_never_function_words_and_density(self):
        t = ("The king sent a letter to the admiral and the admiral sent a letter back to the king, "
             "and the two of them kept writing letters for a year.")
        ms = E.mark(t)
        self.assertTrue(all(E._norm(x.word) not in E.FUNCTION for x in ms))
        self.assertLessEqual(len(ms), round(0.25 * len(t.split())) + 1)

    def test_force_and_veto(self):
        t = "He hid the coin in a loaf of bread."
        self.assertIn("loaf", marked(t, force=["loaf"]))
        self.assertNotIn("hid", marked(t, veto=["hid"]))

    def test_markup_keeps_words_and_punctuation(self):
        t = "He hid one coin, and nobody found it."
        out = E.markup(t, E.mark(t))
        self.assertEqual(out.lower(), t.lower())
        self.assertNotEqual(out, t)

    def test_instruct_names_the_words(self):
        ms = E.mark("They buried a man alive with a bell.")
        ins = E.instruct_for(ms, "Warm young storyteller")
        self.assertTrue(ins.startswith("Warm young storyteller. "))
        self.assertIn("buried", ins)


if __name__ == "__main__":
    unittest.main()
