"""On-screen motion onsets of a video (study only): frames where the picture suddenly changes (a cut, a pop-in, a fast
move), for checking whether sound effects land on visual action rather than only on scene transitions.

Decodes 30 fps grey at 90x160, mean absolute frame difference; a spike is a local maximum (+-3 frames) above
median + 1.5 MAD of the whole video and >= 1.6x the previous 0.3 s median (an onset, not a sustained pan).

usage: python -I motion_spikes.py video out.json
"""
import json
import subprocess
import sys

import numpy as np

W, H, FPS = 90, 160, 30


def main():
    src, out = sys.argv[1], sys.argv[2]
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-vf", f"fps={FPS},scale={W}:{H},format=gray", "-f",
                          "rawvideo", "-"], capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)
    d = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))
    med = np.median(d)
    mad = np.median(np.abs(d - med)) + 1e-6
    thr = med + 1.5 * mad
    spikes = []
    for i in range(3, len(d) - 3):
        if d[i] >= thr and d[i] == d[i - 3:i + 4].max() and d[i] >= 1.6 * np.median(d[max(0, i - 9):i]) + 0.1:
            spikes.append({"t": round((i + 1) / FPS, 3), "diff": round(float(d[i]), 2)})
    json.dump({"fps": FPS, "frames": int(len(fr)), "median_diff": round(float(med), 3), "thr": round(float(thr), 3),
               "spikes": spikes}, open(out, "w"), indent=0)
    print(src, len(spikes), "spikes", f"{len(spikes) / (len(fr) / FPS / 60):.1f}/min")


if __name__ == "__main__":
    main()
