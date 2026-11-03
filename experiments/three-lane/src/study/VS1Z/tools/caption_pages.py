# Internal study tool: find the frames where the burnt-in caption page changes in a 720x1280 reference
# (white text in the band y 0.64-0.78). Prints page start frames. Usage: python3 -I caption_pages.py ref.webm [nFrames]
import subprocess, sys
import numpy as np
src = sys.argv[1]; n = int(sys.argv[2]) if len(sys.argv) > 2 else 620
W, H = 360, 640
y0, y1 = int(0.64 * H), int(0.78 * H)
p = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-frames:v", str(n), "-vf", f"scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
fr = np.frombuffer(p.stdout, np.uint8).reshape(-1, H, W, 3)[:, y0:y1].astype(np.int16)
# caption mask: near-white pixels (all channels > 235) with a dark stroke nearby
mask = (fr.min(axis=3) > 232)
prev = None; starts = [0]
for i, m in enumerate(mask):
    if prev is not None:
        d = np.logical_xor(m, prev).sum() / max(1, (m | prev).sum())
        if d > 0.45 and (i - starts[-1]) >= 2: starts.append(i)
    prev = m
print(" ".join(map(str, starts)))
