"""Estimate uniform scale + translation between frame pairs (slow camera push / drift).
usage: zoom_est.py <video_ffmpeg> <video> <t0> <dt> [<t0> <dt> ...]  -> scale per second, px/s drift"""
import sys, subprocess
import numpy as np
from PIL import Image
ff, vid = sys.argv[1], sys.argv[2]
args = sys.argv[3:]
W, H = 640, 360
def grab(t):
    b = subprocess.run([ff, "-v", "error", "-ss", str(t), "-i", vid, "-frames:v", "1", "-vf", f"scale={W}:{H}:flags=area,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    return Image.frombytes("L", (W, H), b)
def ncc(a, b):
    a = a - a.mean(); b = b - b.mean(); return float((a * b).sum() / (np.sqrt((a * a).sum() * (b * b).sum()) + 1e-9))
def best(a, b):
    A = np.asarray(a, np.float32); res = []
    for s in np.arange(0.90, 1.12, 0.0025):
        w, h = int(W * s), int(H * s)
        bs = np.asarray(b.resize((w, h), Image.BILINEAR), np.float32)
        x0, y0 = (w - W) // 2, (h - H) // 2
        if s >= 1:
            B = bs[y0:y0 + H, x0:x0 + W]; Ac = A
        else:
            B = bs; Ac = A[-y0:-y0 + h, -x0:-x0 + w]
        m = 40  # search translation coarse
        bestl = (-2, 0, 0)
        for dy in range(-8, 9, 2):
            for dx in range(-16, 17, 2):
                a1 = Ac[m + dy:Ac.shape[0] - m + dy, m + dx:Ac.shape[1] - m + dx]; b1 = B[m:B.shape[0] - m, m:B.shape[1] - m]
                if a1.shape != b1.shape: continue
                c = ncc(a1, b1)
                if c > bestl[0]: bestl = (c, dx, dy)
        res.append((bestl[0], s, bestl[1], bestl[2]))
    return max(res)
for i in range(0, len(args), 2):
    t0, dt = float(args[i]), float(args[i + 1])
    c, s, dx, dy = best(grab(t0), grab(t0 + dt))
    print(f"t={t0:.2f}+{dt}s ncc={c:.3f} scale(b->a)={s:.4f}  => zoom {((1/s)**(1/dt)-1)*100:+.2f}%/s  shift({dx},{dy})px@640 => {dx*3/dt:.1f},{dy*3/dt:.1f} px/s@1920")
