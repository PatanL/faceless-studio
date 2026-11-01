"""Per-frame palette / tonal / texture stats for a folder of frames.
usage: frame_stats.py <out.json> <frame_dir> <step_s> [offset_s] [glob]
For each frame (downsampled to 480x270):
  - kmeans (k=10) palette with coverage
  - n_bins95: number of 4-bit/channel colour bins needed to cover 95% of pixels (flatness)
  - n_hue_families: hue clusters (30 deg bins) with >=3% coverage among pixels with S>0.25,V>0.2
  - sat/val percentiles (HSV), dark-bg fraction
  - border colour (median of 8px frame border)
  - grain: median abs residual vs 3x3 box blur in flat regions (full res crop)
"""
import sys, glob, os, json
import numpy as np
from PIL import Image, ImageFilter

def rgb2hsv(a):
    a = a.astype(np.float32) / 255.0
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx = a.max(-1); mn = a.min(-1); d = mx - mn
    h = np.zeros_like(mx)
    m = d > 1e-6
    rr = (mx == r) & m; gg = (mx == g) & m & ~rr; bb = m & ~rr & ~gg
    h[rr] = ((g - b)[rr] / d[rr]) % 6
    h[gg] = ((b - r)[gg] / d[gg]) + 2
    h[bb] = ((r - g)[bb] / d[bb]) + 4
    h = h * 60.0
    s = np.where(mx > 0, d / np.maximum(mx, 1e-6), 0)
    return h, s, mx

def kmeans(x, k=10, it=12, seed=0):
    rng = np.random.default_rng(seed)
    c = x[rng.choice(len(x), k, replace=False)].astype(np.float32)
    for _ in range(it):
        dd = ((x[:, None, :] - c[None]) ** 2).sum(-1)
        lab = dd.argmin(1)
        for j in range(k):
            sel = x[lab == j]
            if len(sel): c[j] = sel.mean(0)
    dd = ((x[:, None, :] - c[None]) ** 2).sum(-1); lab = dd.argmin(1)
    cov = np.bincount(lab, minlength=k) / len(x)
    o = np.argsort(-cov)
    return c[o], cov[o]

def hx(c): return "#%02x%02x%02x" % tuple(int(round(v)) for v in c)

out, d, step = sys.argv[1], sys.argv[2], float(sys.argv[3])
off = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
pat = sys.argv[5] if len(sys.argv) > 5 else "*.jpg"
res = []
for f in sorted(glob.glob(os.path.join(d, pat))):
    n = int(os.path.basename(f).split(".")[0]); t = off + (n - 1) * step
    im = Image.open(f).convert("RGB")
    full = np.asarray(im)
    sm = np.asarray(im.resize((480, 270), Image.BILINEAR))
    px = sm.reshape(-1, 3)
    sub = px[:: 7]
    c, cov = kmeans(sub.astype(np.float32), 10)
    q = (px >> 4).astype(np.int32); key = q[:, 0] * 256 + q[:, 1] * 16 + q[:, 2]
    cnt = np.sort(np.bincount(key, minlength=4096))[::-1]
    cum = np.cumsum(cnt) / cnt.sum()
    n95 = int(np.searchsorted(cum, 0.95) + 1); n80 = int(np.searchsorted(cum, 0.80) + 1)
    h, s, v = rgb2hsv(sm)
    chroma = (s > 0.25) & (v > 0.2)
    hb = np.bincount((h[chroma] // 30).astype(int) % 12, minlength=12) / max(1, chroma.sum())
    fam = int((hb >= 0.03).sum())
    border = np.concatenate([sm[:8].reshape(-1, 3), sm[-8:].reshape(-1, 3), sm[:, :8].reshape(-1, 3), sm[:, -8:].reshape(-1, 3)])
    # grain: residual in flat areas of full-res luminance
    L = np.asarray(im.convert("L"), dtype=np.float32)
    Lb = np.asarray(im.convert("L").filter(ImageFilter.BoxBlur(1)), dtype=np.float32)
    Lb2 = np.asarray(im.convert("L").filter(ImageFilter.BoxBlur(4)), dtype=np.float32)
    flat = np.abs(Lb2 - Lb) < 1.0
    resid = np.abs(L - Lb)[flat]
    res.append(dict(t=round(t, 2), file=os.path.basename(f),
        palette=[[hx(cc), round(float(p), 3)] for cc, p in zip(c, cov)],
        n_bins95=n95, n_bins80=n80, hue_families=fam,
        hue_hist=[round(float(x), 3) for x in hb],
        sat_p=[round(float(x), 3) for x in np.percentile(s, [10, 50, 90])],
        val_p=[round(float(x), 3) for x in np.percentile(v, [10, 50, 90])],
        sat_chroma_med=round(float(np.median(s[chroma])) if chroma.any() else 0, 3),
        dark_frac=round(float((v < 0.2).mean()), 3),
        near_white_frac=round(float(((v > 0.92) & (s < 0.15)).mean()), 4),
        border=hx(np.median(border, 0)),
        grain=round(float(np.median(resid)) if resid.size else -1, 3),
        grain_p90=round(float(np.percentile(resid, 90)) if resid.size else -1, 3),
        flat_frac=round(float(flat.mean()), 3)))
json.dump(res, open(out, "w"), indent=0)
print(out, len(res))
