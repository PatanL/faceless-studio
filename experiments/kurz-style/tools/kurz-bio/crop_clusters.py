import sys, glob, os, colorsys, numpy as np
from PIL import Image
def km(x, k, it=20, seed=1):
    rng = np.random.default_rng(seed); c = [x[rng.integers(len(x))]]
    for _ in range(k - 1):
        d = np.min(((x[:, None] - np.array(c)[None]) ** 2).sum(-1), 1); c.append(x[rng.choice(len(x), p=d / d.sum())])
    c = np.array(c, np.float32)
    for _ in range(it):
        l = ((x[:, None] - c[None]) ** 2).sum(-1).argmin(1)
        for j in range(k):
            if (l == j).any(): c[j] = x[l == j].mean(0)
    l = ((x[:, None] - c[None]) ** 2).sum(-1).argmin(1); cov = np.bincount(l, minlength=k) / len(x); o = np.argsort(-cov); return c[o], cov[o]
for f in sys.argv[2:]:
    im = Image.open(f).convert("RGB"); im.thumbnail((240, 240))
    x = np.asarray(im).reshape(-1, 3).astype(np.float32)
    c, cov = km(x, int(sys.argv[1]))
    print("==", os.path.basename(f))
    for ci, p in zip(c, cov):
        h, s, v = colorsys.rgb_to_hsv(*(ci / 255))
        print("  #%02x%02x%02x %5.1f%%  H%3d S%.2f V%.2f" % (*[int(round(t)) for t in ci], p * 100, h * 360, s, v))
