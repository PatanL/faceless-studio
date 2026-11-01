"""Pixel probes for shading-recipe measurement on a 1920x1080 still.
usage:
  probe.py <img> pt  x,y [x,y ...]                  hex + HSV at points (3x3 median)
  probe.py <img> line x0,y0 x1,y1 [n=24]            hex + L* profile along a line (glow falloff, gradients, rims)
  probe.py <img> box x0,y0,x1,y1                    mean/std hex, distinct-colour count (4-bit) inside a box
"""
import sys, colorsys
import numpy as np
from PIL import Image

im = np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(np.float32)


def at(x, y):
    x, y = int(round(x)), int(round(y))
    p = im[max(0, y - 1):y + 2, max(0, x - 1):x + 2].reshape(-1, 3)
    return np.median(p, axis=0)


def L(rgb):
    c = rgb / 255.0
    c = np.where(c > 0.04045, ((c + 0.055) / 1.055) ** 2.4, c / 12.92)
    Y = 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    return 116 * (Y ** (1 / 3) if Y > 0.008856 else 7.787 * Y + 16 / 116) - 16


def fmt(rgb):
    h, s, v = colorsys.rgb_to_hsv(*(rgb / 255.0))
    return "#%02x%02x%02x  H%3d S%.2f V%.2f L*%5.1f" % (*[int(c) for c in rgb], h * 360, s, v, L(rgb))


mode = sys.argv[2]
if mode == "pt":
    for a in sys.argv[3:]:
        x, y = map(float, a.split(","))
        print(a, fmt(at(x, y)))
elif mode == "line":
    x0, y0 = map(float, sys.argv[3].split(",")); x1, y1 = map(float, sys.argv[4].split(","))
    n = int(sys.argv[5]) if len(sys.argv) > 5 else 24
    for i in range(n + 1):
        f = i / n
        x, y = x0 + (x1 - x0) * f, y0 + (y1 - y0) * f
        print("%5.0f,%5.0f  %s" % (x, y, fmt(at(x, y))))
elif mode == "box":
    x0, y0, x1, y1 = map(int, sys.argv[3].split(","))
    p = im[y0:y1, x0:x1].reshape(-1, 3)
    q = (p.astype(np.uint8) >> 4).astype(np.int32)
    k = q[:, 0] * 256 + q[:, 1] * 16 + q[:, 2]
    cnt = np.bincount(k, minlength=4096) / len(k)
    print("mean", fmt(p.mean(0)), " std", np.round(p.std(0), 1), " colours>=1%:", int((cnt >= 0.01).sum()))
