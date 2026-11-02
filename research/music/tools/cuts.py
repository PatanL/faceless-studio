"""Visual change timeline of a (vertical) video, a stand-in for the hand-made setting catalogue on the Shorts.

Decodes 10 fps at 72x128, colour histograms (8x8x8) per frame; a "change" is a peak of the histogram distance between
the 0.4 s before and the 0.4 s after a frame (catches cuts and 0.3 s iris transitions alike), at least 1.0 s apart.
Writes the analyze.py --settings-json shape: [{"t0", "t1", "label": "visual", ...}].

usage: python research/music/tools/cuts.py video.mp4 out.json [--thr 0.35]
"""
import json
import subprocess
import sys

import numpy as np

W, H, FPS = 72, 128, 10


def main():
    src, out = sys.argv[1], sys.argv[2]
    thr = float(sys.argv[sys.argv.index("--thr") + 1]) if "--thr" in sys.argv else 0.35
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-vf", f"fps={FPS},scale={W}:{H}", "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    q = (fr // 32).astype(np.int32)
    idx = q[..., 0] * 64 + q[..., 1] * 8 + q[..., 2]
    hist = np.stack([np.bincount(i.ravel(), minlength=512) for i in idx]).astype(float)
    hist /= hist.sum(1, keepdims=True)
    k = 4
    d = np.zeros(len(hist))
    for i in range(k, len(hist) - k):
        a, b = hist[i - k:i].mean(0), hist[i:i + k].mean(0)
        d[i] = 0.5 * np.abs(a - b).sum()
    peaks = [i for i in range(1, len(d) - 1) if d[i] >= thr and d[i] == d[max(0, i - FPS):i + FPS + 1].max()]
    times = [round(i / FPS, 2) for i in peaks]
    T = len(hist) / FPS
    edges = [0.0] + times + [T]
    runs = [{"t0": a, "t1": b, "label": "visual", "place": "", "kind": "visual", "why": f"d={d[int(a * FPS)]:.2f}"}
            for a, b in zip(edges[:-1], edges[1:]) if b - a > 0.05]
    json.dump(runs, open(out, "w"), indent=0)
    print(f"{src}: {len(times)} changes in {T:.1f}s ({len(times) / T * 60:.1f}/min)")


if __name__ == "__main__":
    main()
