"""Per-image palette/tone/texture stats. usage: still_stats.py out.json img1 img2 ..."""
import sys, json, os
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

def rgb2hsv(a):
    a = a.astype(np.float32) / 255.0
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx = a.max(-1); mn = a.min(-1); d = mx - mn
    h = np.zeros_like(mx); m = d > 1e-6
    rr = (mx == r) & m; gg = (mx == g) & m & ~rr; bb = m & ~rr & ~gg
    h[rr] = ((g - b)[rr] / d[rr]) % 6; h[gg] = ((b - r)[gg] / d[gg]) + 2; h[bb] = ((r - g)[bb] / d[bb]) + 4
    return h * 60.0, np.where(mx > 0, d / np.maximum(mx, 1e-6), 0), mx

def kmeans(x, k=10, it=15, seed=0):
    rng = np.random.default_rng(seed)
    # kmeans++ init
    c = [x[rng.integers(len(x))]]
    for _ in range(k - 1):
        d = np.min(((x[:, None, :] - np.array(c)[None]) ** 2).sum(-1), 1)
        c.append(x[rng.choice(len(x), p=d / d.sum())])
    c = np.array(c, np.float32)
    for _ in range(it):
        lab = ((x[:, None, :] - c[None]) ** 2).sum(-1).argmin(1)
        for j in range(k):
            s = x[lab == j]
            if len(s): c[j] = s.mean(0)
    lab = ((x[:, None, :] - c[None]) ** 2).sum(-1).argmin(1)
    cov = np.bincount(lab, minlength=k) / len(x); o = np.argsort(-cov)
    return c[o], cov[o]

hx = lambda c: "#%02x%02x%02x" % tuple(int(round(float(v))) for v in c)

def stats(path, k=10):
    im = np.asarray(Image.open(path).convert("RGB"))
    H, W, _ = im.shape
    sm = np.asarray(Image.fromarray(im).resize((320, 180), Image.BILINEAR)).reshape(-1, 3).astype(np.float32)
    c, cov = kmeans(sm, k)
    # distinct colours: 4-bit/channel bins covering 90/95%
    q = (im >> 4).astype(np.int32); key = (q[..., 0] << 8) | (q[..., 1] << 4) | q[..., 2]
    cnt = np.sort(np.bincount(key.ravel(), minlength=4096))[::-1]; cs = np.cumsum(cnt) / cnt.sum()
    h, s, v = rgb2hsv(im)
    chrom = (s > 0.25) & (v > 0.2)
    hb = np.bincount((h[chrom] // 30).astype(int) % 12, minlength=12) / max(chrom.sum(), 1)
    lum = im.astype(np.float32) @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    gx = ndi.sobel(lum, 1); gy = ndi.sobel(lum, 0); g = np.hypot(gx, gy) / 8.0
    flat = (g < 0.75).mean(); soft = ((g >= 0.75) & (g < 4)).mean(); edge = (g >= 4).mean()
    resid = lum - ndi.uniform_filter(lum, 5)
    fm = g < 1.5
    grain = float(np.std(resid[fm])) if fm.sum() > 1000 else None
    # large-scale background gradient: luminance of heavily blurred image, range across frame
    bl = ndi.zoom(ndi.uniform_filter(lum, 31), 0.1)
    b = int(0.1 * min(H, W))
    border = np.concatenate([lum[:b].ravel(), lum[-b:].ravel(), lum[:, :b].ravel(), lum[:, -b:].ravel()])
    center = lum[H // 4:3 * H // 4, W // 4:3 * W // 4]
    return dict(file=os.path.basename(path),
        palette=[dict(hex=hx(ci), pct=round(float(p) * 100, 1)) for ci, p in zip(c, cov)],
        bins90=int(np.searchsorted(cs, 0.90) + 1), bins95=int(np.searchsorted(cs, 0.95) + 1),
        hue_families_3pct=int((hb >= 0.03).sum()), hue_hist_30deg=[round(float(x) * 100, 1) for x in hb],
        sat_p10_50_90=[round(float(x), 2) for x in np.percentile(s, [10, 50, 90])],
        val_p10_50_90=[round(float(x), 2) for x in np.percentile(v, [10, 50, 90])],
        pct_sat_gt_060=round(float((s > 0.6).mean()) * 100, 1),
        pct_pure_black_lt_005=round(float((v < 0.05).mean()) * 100, 2),
        pct_near_white=round(float(((s < 0.12) & (v > 0.92)).mean()) * 100, 2),
        flat_pct=round(flat * 100, 1), soft_gradient_pct=round(soft * 100, 1), edge_pct=round(edge * 100, 1),
        grain_std=round(grain, 2) if grain is not None else None,
        border_minus_center_lum=round(float(border.mean() - center.mean()), 1),
        bg_lowfreq_lum_range=round(float(np.percentile(bl, 95) - np.percentile(bl, 5)), 1))

out = [stats(p) for p in sys.argv[2:]]
json.dump(out, open(sys.argv[1], "w"), indent=1)
print(len(out))
