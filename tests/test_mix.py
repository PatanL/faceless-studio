"""pipeline/audio/mix.py (findings F14, F15). Needs numpy, soundfile, pyloudnorm, scipy:
skipped on the Mac, run on the Spark inside ~/studio/.venv."""
import unittest

import _util  # noqa: F401

try:
    import numpy as np
    from pipeline.audio import mix
except Exception as e:  # noqa: BLE001
    mix = None
    REASON = f"audio deps missing ({e}); run on the Spark venv"


@unittest.skipIf(mix is None, "audio deps missing; run on the Spark venv")
class Mix(unittest.TestCase):
    @unittest.expectedFailure
    def test_F14_voice_and_bed_measured_with_same_layout(self):
        """F14: the same signal measured mono (voice path) and as a dual-mono stereo pair (bed path)
        must give the same reference, else music_db is off by ~3 LU."""
        rng = np.random.default_rng(0)
        x = (rng.standard_normal(mix.SR * 5) * 0.05).astype(np.float32)
        self.assertAlmostEqual(mix.lufs(x), mix.lufs(np.stack([x, x], 1)), delta=0.5)

    @unittest.expectedFailure
    def test_F15_negative_cue_time_is_clamped(self):
        """F15: a cue at -0.1 s must not raise a broadcast ValueError in _sfx_bus."""
        orig_load, orig_find = mix.load, mix.find_asset
        try:
            mix.find_asset = lambda kind, name: "x.wav"
            mix.load = lambda p: np.ones((mix.SR // 2, 2), np.float32)  # longer than the negative offset
            bus = mix._sfx_bus([{"cue": "whoosh", "at": -0.1}], mix.SR, print)
            self.assertEqual(len(bus), mix.SR)
        finally:
            mix.load, mix.find_asset = orig_load, orig_find


if __name__ == "__main__":
    unittest.main()
