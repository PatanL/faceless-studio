"""Face study (our own code): measure character heads in close-ups. Reference frames are read from local study copies
and never stored in the repo; only the numbers are.

usage: python3 -I face_study.py <out_dir> <video>... [--every 0.5] [--min 0.09]

For every sampled frame, it finds heads: white, low-saturation blobs (holes for features filled) that are round
(hull circularity >= 0.8, aspect 0.75-1.3) and at least --min of the frame height across. For each head it measures:
  aspect        width / height of the head blob
  outline_frac  thickness of the dark ring outside the head edge (median over 72 rays) / head diameter
  shade_*       luminance inside the head (features excluded): p95 (lit), p5 (darkest), the direction of the gradient
                (degrees, 0 = darker to the right, 90 = darker at the bottom) and its strength (lit - dark)
  features      dark blobs inside the head: count, and for the eyes (the two most alike, upper half), mean height and
                width / head diameter and stroke weight (2 x max of the distance transform) / head diameter
  brow_frac     stroke weight of the thickest dark blob above the eyes / head diameter
Writes <out_dir>/faces.json (per head and summary) and <out_dir>/crops/*.png for checking by eye (scratch only).
"""
import sys, os, json, subprocess
import numpy as np, cv2


def frames(vid, every):
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", vid, "-vf", f"fps={1 / every},scale=720:1280", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True)
    return np.frombuffer(p.stdout, np.uint8).reshape(-1, 1280, 720, 3)


def heads(im, minf):
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    # lit and shaded skin: the refs' heads are white spheres shaded down to light grey
    m = ((hsv[..., 2] >= 150) & (hsv[..., 1] <= 40)).astype(np.uint8)
    m[int(0.6 * 1280):int(0.8 * 1280)] = 0                                    # the caption band
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    cnts, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    out = []
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if h < minf * 1280 or not 0.75 <= w / h <= 1.3 or x == 0 or y == 0 or x + w >= 720 or y + h >= 1280:
            continue
        hull = cv2.convexHull(c); ha = cv2.contourArea(hull); hp = cv2.arcLength(hull, True)
        if 4 * np.pi * ha / hp ** 2 < 0.8:
            continue
        filled = np.zeros(m.shape, np.uint8); cv2.drawContours(filled, [hull], -1, 1, -1)
        out.append((x, y, w, h, filled))
    return out


def measure(im, x, y, w, h, filled):
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    D = (w + h) / 2; cx, cy = x + w / 2, y + h / 2
    # outline: walk 72 rays outward from the hull edge, count dark pixels (< 0.3) right after the edge
    th = []
    for k in range(72):
        a = k * np.pi / 36
        r = 0.3 * D
        while r < 0.9 * D:
            px, py = int(cx + np.cos(a) * r), int(cy + np.sin(a) * r)
            if not (0 <= px < 720 and 0 <= py < 1280) or not filled[py, px]: break
            r += 1
        n = 0
        for s in range(1, int(0.15 * D)):
            px, py = int(cx + np.cos(a) * (r + s)), int(cy + np.sin(a) * (r + s))
            if not (0 <= px < 720 and 0 <= py < 1280) or g[py, px] > 0.3: break
            n += 1
        if n: th.append(n)
    inside = filled.astype(bool)
    dark = inside & (g < 0.35)
    skin = inside & ~cv2.dilate(dark.astype(np.uint8), np.ones((7, 7), np.uint8)).astype(bool)
    ys, xs = np.nonzero(skin); L = g[ys, xs]
    A = np.c_[np.ones_like(xs), (xs - cx) / D, (ys - cy) / D]
    coef = np.linalg.lstsq(A, L, rcond=None)[0]                                  # L = a + b x + c y
    ang = float(np.degrees(np.arctan2(-coef[2], -coef[1])))                       # direction toward darker
    n, lab, st, _ = cv2.connectedComponentsWithStats(dark.astype(np.uint8), 8)
    feats = []
    for i in range(1, n):
        fx, fy, fw, fh, fa = st[i]
        if fa < 0.0004 * D * D or fh > 0.6 * D: continue
        dt = cv2.distanceTransform((lab[fy:fy + fh, fx:fx + fw] == i).astype(np.uint8), cv2.DIST_L2, 3)
        feats.append({"cx": (fx + fw / 2 - cx) / D, "cy": (fy + fh / 2 - cy) / D, "w": fw / D, "h": fh / D, "stroke": 2 * float(dt.max()) / D, "area": fa / (D * D)})
    eyes = sorted([f for f in feats if f["cy"] < 0.12 and f["area"] > 0.002], key=lambda f: -f["area"])[:2]
    brows = [f for f in feats if eyes and f["cy"] < min(e["cy"] for e in eyes) - 0.05]
    return {"D_frac": round(D / 1280, 3), "aspect": round(w / h, 3), "outline_frac": round(float(np.median(th)) / D, 4) if th else None,
            "shade_p95": round(float(np.percentile(L, 95)), 3), "shade_p5": round(float(np.percentile(L, 5)), 3),
            "shade_dir_deg": round(ang, 1), "shade_strength": round(float(np.hypot(coef[1], coef[2])), 3),
            "n_features": len(feats),
            "eye_h": round(float(np.mean([e["h"] for e in eyes])), 3) if eyes else None, "eye_w": round(float(np.mean([e["w"] for e in eyes])), 3) if eyes else None,
            "eye_stroke": round(float(np.mean([e["stroke"] for e in eyes])), 3) if eyes else None,
            "eye_gap": round(abs(eyes[0]["cx"] - eyes[1]["cx"]), 3) if len(eyes) == 2 else None,
            "eye_y": round(float(np.mean([e["cy"] for e in eyes])), 3) if eyes else None,
            "brow_stroke": round(max(b["stroke"] for b in brows), 3) if brows else None}


def main():
    out = sys.argv[1]; vids = [a for a in sys.argv[2:] if not a.startswith("--") and not a.replace(".", "").isdigit()]
    every = float(sys.argv[sys.argv.index("--every") + 1]) if "--every" in sys.argv else 0.5
    minf = float(sys.argv[sys.argv.index("--min") + 1]) if "--min" in sys.argv else 0.09
    os.makedirs(f"{out}/crops", exist_ok=True)
    rows = []
    for v in vids:
        name = os.path.basename(v).split(".")[0][-11:]
        last = -10
        for i, im in enumerate(frames(v, every)):
            for (x, y, w, h, filled) in heads(im, minf):
                if i - last < 2: continue                                        # one head per second at most
                r = measure(im, x, y, w, h, filled)
                if r["eye_h"] is None or r["outline_frac"] is None: continue
                r.update({"video": name, "t": round(i * every, 1)})
                rows.append(r); last = i
                pad = int(0.25 * h)
                cv2.imwrite(f"{out}/crops/{name}_{i * every:05.1f}.png", im[max(0, y - pad):y + h + pad, max(0, x - pad):x + w + pad])
    keys = ["aspect", "outline_frac", "shade_p95", "shade_p5", "shade_dir_deg", "shade_strength", "eye_h", "eye_w", "eye_stroke", "eye_gap", "eye_y", "brow_stroke", "D_frac"]
    summ = {k: [round(float(np.percentile([r[k] for r in rows if r.get(k) is not None], q)), 3) for q in (25, 50, 75)] for k in keys}
    json.dump({"n": len(rows), "summary_p25_50_75": summ, "heads": rows}, open(f"{out}/faces.json", "w"), indent=1)
    print(len(rows), json.dumps(summ, indent=1))


if __name__ == "__main__":
    main()
