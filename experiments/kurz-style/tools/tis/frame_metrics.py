"""Per-frame style metrics for a folder of stills (style study, CPU only).

usage: python -I frame_metrics.py <grid_dir> <out.json> [step]

For every frame (optionally every `step`-th) it measures, on a 640x360 proxy:
  palette      k-means (k=10, Lab) cluster hexes + coverage, sorted by coverage
  n_colours    clusters covering >= 2 % of the frame (the "dominant colours" count)
  n_flat       distinct 4-bit/channel colours covering >= 0.5 % (flat-fill count)
  sat/val      HSV S and V percentiles p10/p50/p90 (0..1)
  dark_frac    fraction of pixels with V < 0.12 (blacks/outline ink)
  outline      thin dark-line response: fraction of Canny edge pixels that sit on a
               <= 3 px line at least 45 L* darker than its 7 px neighbourhood (blackhat)
  edge_den     Canny edge pixels / all pixels (detail density proxy)
  grad_frac    fraction of low-edge pixels that sit on a smooth ramp (0 < |grad| < 4 L/px):
               high = gradient fills, low = flat fills
  grain        std of the high-pass residual (img - gauss3) inside flat regions, in 8-bit units
  vignette     mean L of the four corner tiles / mean L of the centre tile
  blur_frac    fraction of textured 40 px tiles whose Laplacian variance is < 15 % of the
               frame's 90th percentile (soft / defocused planes)
"""
import sys, json, glob, os
import numpy as np, cv2


def hexs(rgb):
    return "#%02x%02x%02x" % tuple(int(c) for c in rgb)


def metrics(path):
    im = cv2.imread(path)
    if im is None:
        return None
    im = cv2.resize(im, (640, 360), interpolation=cv2.INTER_AREA)
    lab = cv2.cvtColor(im, cv2.COLOR_BGR2LAB)
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV).astype(np.float32)
    S, V = hsv[..., 1] / 255.0, hsv[..., 2] / 255.0
    L = lab[..., 0].astype(np.float32) * 100 / 255.0

    # palette
    sm = cv2.resize(lab, (160, 90), interpolation=cv2.INTER_AREA).reshape(-1, 3).astype(np.float32)
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.5)
    _, lbl, cent = cv2.kmeans(sm, 10, None, crit, 3, cv2.KMEANS_PP_CENTERS)
    cov = np.bincount(lbl.ravel(), minlength=10) / lbl.size
    cent_rgb = cv2.cvtColor(cent.reshape(1, -1, 3).astype(np.uint8), cv2.COLOR_LAB2RGB)[0]
    order = np.argsort(-cov)
    pal = [{"hex": hexs(cent_rgb[i]), "cov": round(float(cov[i]), 3)} for i in order]
    n_col = int((cov >= 0.02).sum())

    q = (im >> 4).reshape(-1, 3)
    keys = q[:, 0].astype(np.int32) * 256 + q[:, 1].astype(np.int32) * 16 + q[:, 2]
    cnt = np.bincount(keys, minlength=4096) / keys.size
    n_flat = int((cnt >= 0.005).sum())

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 60, 140) > 0
    edge_den = float(edges.mean())
    bh = cv2.morphologyEx(L, cv2.MORPH_BLACKHAT, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
    line = bh > 45
    outline = float((line & cv2.dilate(edges.astype(np.uint8), None) .astype(bool)).sum() / max(1, edges.sum()))

    gx = cv2.Sobel(L, cv2.CV_32F, 1, 0, ksize=3) / 8
    gy = cv2.Sobel(L, cv2.CV_32F, 0, 1, ksize=3) / 8
    g = np.hypot(gx, gy)
    near_edge = cv2.dilate(edges.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    flat = ~near_edge
    ramp = flat & (g > 0.15) & (g < 4)
    grad_frac = float(ramp.sum() / max(1, flat.sum()))
    hp = gray.astype(np.float32) - cv2.GaussianBlur(gray, (0, 0), 1.0).astype(np.float32)
    grain = float(hp[flat].std()) if flat.any() else 0.0

    h, w = L.shape
    t = 60
    corners = np.concatenate([L[:t, :t].ravel(), L[:t, -t:].ravel(), L[-t:, :t].ravel(), L[-t:, -t:].ravel()])
    centre = L[h // 2 - t:h // 2 + t, w // 2 - t:w // 2 + t]
    vign = float(corners.mean() / max(1.0, centre.mean()))

    lap = cv2.Laplacian(gray, cv2.CV_32F)
    tiles = []
    for y in range(0, h - 40 + 1, 40):
        for x in range(0, w - 40 + 1, 40):
            tl = gray[y:y + 40, x:x + 40]
            if tl.std() > 8:  # textured tile
                tiles.append(float(lap[y:y + 40, x:x + 40].var()))
    blur_frac = 0.0
    if len(tiles) > 5:
        tiles = np.array(tiles)
        blur_frac = float((tiles < 0.15 * np.percentile(tiles, 90)).mean())

    pct = lambda a: [round(float(np.percentile(a, p)), 3) for p in (10, 50, 90)]
    return {
        "palette": pal, "n_colours": n_col, "n_flat": n_flat,
        "sat": pct(S), "val": pct(V), "dark_frac": round(float((V < 0.12).mean()), 3),
        "outline": round(outline, 3), "edge_den": round(edge_den, 4), "grad_frac": round(grad_frac, 3),
        "grain": round(grain, 2), "vignette": round(vign, 3), "blur_frac": round(blur_frac, 3),
        "meanL": round(float(L.mean()), 1),
    }


if __name__ == "__main__":
    cv2.setNumThreads(2)
    d, out = sys.argv[1], sys.argv[2]
    step = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    files = sorted(glob.glob(os.path.join(d, "*.jpg")))[::step]
    res = {}
    for f in files:
        m = metrics(f)
        if m:
            res[os.path.basename(f)] = m
    json.dump(res, open(out, "w"))
    print(len(res), "frames ->", out)
