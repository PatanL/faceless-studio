"""pipeline/episodes/reformat.py camera remap (finding F16)."""
import unittest

import _util  # noqa: F401
from pipeline.episodes.reformat import Map, camera16


class Camera16(unittest.TestCase):
    def test_identity_camera_x_stays_centred(self):
        """Regression guard (passes today): x maps centre to centre."""
        c = camera16({"keyframes": [{"t": 0, "x": "50%", "y": "50%", "zoom": 1}]}, Map(0.78))
        self.assertEqual(c["keyframes"][0]["x"], "50.00%")

    @unittest.expectedFailure
    def test_F16_identity_camera_y_stays_centred(self):
        """F16: the 9:16 identity camera (y 50%) must map to the 16:9 identity camera (y 50%), not 59.97%."""
        c = camera16({"keyframes": [{"t": 0, "x": "50%", "y": "50%", "zoom": 1}]}, Map(0.78))
        self.assertAlmostEqual(float(c["keyframes"][0]["y"][:-1]), 50.0, delta=0.05)


if __name__ == "__main__":
    unittest.main()
