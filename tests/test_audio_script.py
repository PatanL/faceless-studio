"""pipeline/audio/script.py marker and front-matter parsing (findings F09-F13)."""
import unittest

import _util  # noqa: F401
from pipeline.audio.script import parse


class AudioScriptParse(unittest.TestCase):
    def test_basic_markers_still_parse(self):
        """Regression guard (passes today): well-formed markers parse."""
        sc = parse("[music: dread]\nHello there. [pause: 0.5] Bye. [sfx: knock3 @+0.3 vol=-2]\n")
        self.assertEqual(sc.music, "dread")
        kinds = [m.kind for m in sc.segments[0].markers]
        self.assertEqual(kinds, ["pause", "sfx"])

    @unittest.expectedFailure
    def test_F09_music_stop_does_not_become_bed_name(self):
        """F09: a mid-script [music: stop] / [music: duck -6] must not replace the episode bed."""
        sc = parse("[music: dread] One.\n\nTwo. [music: duck -6]\n\nThree. [music: stop]\n")
        self.assertEqual(sc.music, "dread")

    @unittest.expectedFailure
    def test_F10_vox_mid_paragraph_applies_from_that_point(self):
        """F10: [vox:] inside a paragraph must only affect the words after it."""
        sc = parse("[vox: 0] Through the door. [vox: -3] Junie why are you whispering? [vox: 0] Then my call dropped.\n")
        segs = sc.segments
        # whichever representation the fix picks, the whispered words must end up at -3 dB
        gains = {w: s.gain_db for s in segs for w in s.words}
        self.assertEqual(gains.get("Junie"), -3.0)
        self.assertEqual(gains.get("Through"), 0.0)

    @unittest.expectedFailure
    def test_F10_speed_mid_paragraph_applies_from_that_point(self):
        sc = parse("[speed: 1.3] Then my mother. [speed: 1.15] Junie honey. [speed: 1.3] Only she calls me that.\n")
        speeds = {w: s.speed for s in sc.segments for w in s.words}
        self.assertEqual(speeds.get("honey."), 1.15)

    @unittest.expectedFailure
    def test_F11_unknown_bracket_directive_not_spoken(self):
        """F11: [cut], [voice: x] etc. must not reach TTS / captions (drop or raise)."""
        try:
            sc = parse("Last line. [pause: 1.20] [cut]\n\n[voice: af_heart] Hello.\n")
        except ValueError:
            return  # raising a clear error is also an acceptable fix
        words = [w for s in sc.segments for w in s.words]
        self.assertFalse(any("[" in w or "]" in w for w in words), words)

    @unittest.expectedFailure
    def test_F12_malformed_sfx_offset_gives_clear_error(self):
        """F12: [sfx: stinger @"Taken"] must raise an error that names the marker, not a bare float() ValueError."""
        with self.assertRaises(ValueError) as cm:
            parse('It was [sfx: stinger @"Taken"] taken.\n')
        self.assertIn("sfx", str(cm.exception).lower())

    @unittest.expectedFailure
    def test_F12_vox_word_argument_gives_clear_error(self):
        with self.assertRaises(ValueError):
            parse("[vox: quiet] Hello.\n")  # today: IndexError

    @unittest.expectedFailure
    def test_F13_front_matter_inline_comment_stripped(self):
        """F13: 'speed: 1.0  # pinned' must give a value float() accepts (make.py:96)."""
        sc = parse("---\nspeed: 1.0  # pinned to the pilot\nparagraph_pause: 0.2  # tighter\n---\nHello.\n")
        self.assertEqual(float(sc.meta["speed"]), 1.0)
        self.assertEqual(float(sc.meta["paragraph_pause"]), 0.2)

    @unittest.expectedFailure
    def test_F13_prose_music_value_not_used_as_asset(self):
        """F13: 'music: deep_ocean (0:00-4:28) - ...' must not become the asset name."""
        sc = parse("---\nmusic: deep_ocean (0:00-4:28) · swells at the reveal\n---\nHello.\n")
        self.assertIn(sc.music, ("deep_ocean", None))


if __name__ == "__main__":
    unittest.main()
