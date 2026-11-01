"""Track an object's size over time by colour mask inside an ROI (60 fps).
usage: pop_curve.py <ffmpeg> <video> <start> <dur> x0,y0,x1,y1 hex1,hex2,.. tol
prints per-frame bbox width/height and mask area (1920x1080 coords)."""
import sys, subprocess
import numpy as np
ff, vid, ss, du, roi, cols, tol = sys.argv[1:8]
x0, y0, x1, y1 = map(int, roi.split(",")); tol = float(tol)
C = np.array([[int(h[i:i + 2], 16) for i in (1, 3, 5)] for h in cols.split(",")], np.float32)
W, H = 1920, 1080
p = subprocess.Popen([ff, "-v", "error", "-ss", ss, "-i", vid, "-t", du, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
i = 0
while True:
    b = p.stdout.read(W * H * 3)
    if len(b) < W * H * 3: break
    a = np.frombuffer(b, np.uint8).reshape(H, W, 3)[y0:y1, x0:x1].astype(np.float32)
    dmin = np.min(np.sqrt(((a[:, :, None, :] - C[None, None]) ** 2).sum(-1)), -1)
    m = dmin < tol
    if m.sum() > 20:
        ys, xs = np.nonzero(m)
        bw = np.percentile(xs, 99) - np.percentile(xs, 1); bh = np.percentile(ys, 99) - np.percentile(ys, 1)
        print(f"{float(ss) + i / 60:.3f} area={int(m.sum())} w={bw:.0f} h={bh:.0f} cx={x0 + xs.mean():.0f} cy={y0 + ys.mean():.0f}")
    else:
        print(f"{float(ss) + i / 60:.3f} area=0")
    i += 1
