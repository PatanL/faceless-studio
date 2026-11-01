"""Pixel probes on a still.
probe.py <img> radial cx cy r0 r1 step [angles_deg comma]   -> mean colour (over angles) at each radius
probe.py <img> line x0 y0 x1 y1 n                          -> colours along a line (3x3 mean)
probe.py <img> pts x,y x,y ...                              -> 5x5 mean colour at points"""
import sys, math
import numpy as np
from PIL import Image
im = np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(np.float32)
H, W, _ = im.shape
def at(x, y, r=1):
    x, y = int(round(x)), int(round(y))
    x0, x1, y0, y1 = max(0, x - r), min(W, x + r + 1), max(0, y - r), min(H, y + r + 1)
    a = im[y0:y1, x0:x1].reshape(-1, 3)
    return a.mean(0) if len(a) else np.array([0.0, 0.0, 0.0])
def hx(c): return "#%02x%02x%02x" % tuple(int(round(v)) for v in c)
def hsv(c):
    r, g, b = [v / 255 for v in c]; mx, mn = max(r, g, b), min(r, g, b); d = mx - mn
    if d == 0: h = 0
    elif mx == r: h = 60 * (((g - b) / d) % 6)
    elif mx == g: h = 60 * ((b - r) / d + 2)
    else: h = 60 * ((r - g) / d + 4)
    return f"H{h:3.0f} S{(d / mx if mx else 0):.2f} V{mx:.2f}"
mode = sys.argv[2]
if mode == "radial":
    cx, cy, r0, r1, st = map(float, sys.argv[3:8])
    angs = [float(a) for a in sys.argv[8].split(",")] if len(sys.argv) > 8 else list(range(0, 360, 30))
    r = r0
    while r <= r1:
        cs = [at(cx + r * math.cos(math.radians(a)), cy - r * math.sin(math.radians(a)), 2) for a in angs]
        c = np.mean(cs, 0); print(f"r={r:5.0f} {hx(c)} {hsv(c)} L={0.2126*c[0]+0.7152*c[1]+0.0722*c[2]:.0f}")
        r += st
elif mode == "line":
    x0, y0, x1, y1, n = map(float, sys.argv[3:8]); n = int(n)
    for i in range(n + 1):
        u = i / n; x, y = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u; c = at(x, y)
        print(f"({x:5.0f},{y:5.0f}) {hx(c)} {hsv(c)}")
else:
    for p in sys.argv[3:]:
        x, y = map(float, p.split(",")); c = at(x, y, 2); print(f"({x:.0f},{y:.0f}) {hx(c)} {hsv(c)}")
