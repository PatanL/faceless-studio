"""Set detail density and character size, measured on frames30 sheets (our own code).

usage: python3 -I look_density.py <out.json> <name>=<f30 sheet dir> [<name>=<dir> ...] [--step 2] [--tiles DIR]

Both the references and ours are read from pipeline/qa/frames30 sheets (10 columns, 162x288 frame tiles under an
18 px label), so they pass through the same downscale and JPEG. Render ours at 240x426 first (the references' copies)
and run frames30 on that, so the sharpness matches.

Per tile, with the caption band (0.60-0.82 of the height) masked:
  edge_density   share of pixels on a Canny edge (50/120 on a 3x3-blurred gray)
  texture        mean |Laplacian| of gray (0-255): fine painted texture, grain, gaps
  flat_share     share of 6x6 blocks with gray std < 3: empty flat colour (sky, water, bare walls)
  head_h         height of the biggest round light head / frame height (0 when none is found): light, low
                 saturation (V >= 165, S <= 70, so night-tinted heads count), eyes and mouth filled (external
                 contour), solid (area / hull >= 0.85) and round (hull circularity >= 0.78), >= 14 px, and from 60 px up it must hold a face: 2-7 dark
                 holes covering 2-35 % of it (a lamp or plate has none, a clock dial too many); a head
                 clipped by up to two frame edges counts at its larger side. Our stick figures and theirs are both
                 round-head characters about 3 heads tall, so figure height ~ 3 x head_h.
Per source: median and quartiles of each, the share of tiles with a head, and the median head_h over tiles that
have one. --tiles writes an annotated sample of tiles for checking the head finder by eye.
"""
import sys, json, glob, os
import numpy as np
import cv2

CW, CH, LAB, PAD = 162, 288, 18, 2


def tiles(d, step=1):
    k = 0
    for p in sorted(glob.glob(os.path.join(d, "*.jpg"))):
        im = cv2.imread(p)
        H, W = im.shape[:2]
        rows = (H - PAD) // (CH + LAB + PAD)
        for r in range(rows):
            for c in range(10):
                y = PAD + r * (CH + LAB + PAD) + LAB
                x = PAD + c * (CW + PAD)
                t = im[y:y + CH, x:x + CW]
                if t.shape[:2] != (CH, CW) or t.std() < 2:
                    continue
                k += 1
                if k % step == 0:
                    yield t


def heads(t):
    """biggest round, light, low-saturation blob (holes for eyes and mouth filled): a character's head"""
    hsv = cv2.cvtColor(t, cv2.COLOR_BGR2HSV)
    m = ((hsv[..., 2] >= 165) & (hsv[..., 1] <= 70)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    cnts, hier = cv2.findContours(m, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    best = 0.0, None
    if hier is None:
        return best
    hier = hier[0]
    for i, c in enumerate(cnts):
        if hier[i][3] != -1:
            continue                                          # a hole, not an outer contour
        a = cv2.contourArea(c)
        if a < 14:
            continue
        # a face: 2-7 dark holes (eyes, mouth, brows) that cover 2-35 % of the blob; a plain disc (a lamp, a plate)
        # has none, a clock dial has more
        holes, k = [], hier[i][2]
        while k != -1:
            holes.append(cv2.contourArea(cnts[k])); k = hier[k][0]
        big = [h for h in holes if h >= 1]
        if a >= 60 and not (2 <= len(big) <= 7 and 0.02 <= sum(big) / a <= 0.35):
            continue
        x, y, w, h = cv2.boundingRect(c)
        hull = cv2.convexHull(c); ha = cv2.contourArea(hull); hp = cv2.arcLength(hull, True)
        if ha <= 0 or a / ha < 0.85 or 4 * np.pi * ha / max(hp, 1) ** 2 < 0.78:
            continue
        edges = (x == 0) + (y == 0) + (x + w >= CW) + (y + h >= CH)
        if edges > 2 or (edges == 0 and not 0.6 <= w / max(h, 1) <= 1.6):
            continue
        # a clipped head: its diameter is the larger side of the box
        d = max(w, h) if edges else h
        if d / CH > best[0]:
            best = d / CH, (x, y, w, h)
    return best


def metrics(t):
    g = cv2.cvtColor(t, cv2.COLOR_BGR2GRAY)
    keep = np.ones(g.shape, bool)
    keep[int(0.60 * CH):int(0.82 * CH)] = False
    e = cv2.Canny(cv2.GaussianBlur(g, (3, 3), 0), 50, 120) > 0
    lap = np.abs(cv2.Laplacian(g.astype(np.float32), cv2.CV_32F))
    blocks = [g[y:y + 6, x:x + 6].std() for y in range(0, CH - 6, 6) for x in range(0, CW - 6, 6) if keep[y, x] and keep[y + 5, x]]
    hh, box = heads(t)
    return {"edge": float(e[keep].mean()), "tex": float(lap[keep].mean()), "flat": float(np.mean(np.array(blocks) < 3)), "head": hh}, box


def summ(v):
    v = np.array(v, float)
    return [round(float(np.percentile(v, q)), 4) for q in (25, 50, 75)]


def main():
    out = sys.argv[1]
    step = int(sys.argv[sys.argv.index("--step") + 1]) if "--step" in sys.argv else 1
    tdir = sys.argv[sys.argv.index("--tiles") + 1] if "--tiles" in sys.argv else None
    res = {}
    for arg in sys.argv[2:]:
        if "=" not in arg:
            continue
        name, d = arg.split("=", 1)
        rows, sample = [], []
        for i, t in enumerate(tiles(d, step)):
            m, box = metrics(t)
            rows.append(m)
            if tdir and i % 40 == 0 and len(sample) < 20:
                s = t.copy()
                if box:
                    x, y, w, h = box
                    cv2.rectangle(s, (x, y), (x + w, y + h), (0, 0, 255), 1)
                sample.append(s)
        if not rows:
            print(name, "no tiles in", d); continue
        hh = [r["head"] for r in rows if r["head"] > 0]
        res[name] = {"tiles": len(rows), "edge": summ([r["edge"] for r in rows]), "tex": summ([r["tex"] for r in rows]),
                     "flat": summ([r["flat"] for r in rows]), "head_share": round(len(hh) / max(1, len(rows)), 3),
                     "head_h": summ(hh) if hh else [0, 0, 0]}
        if tdir and sample:
            os.makedirs(tdir, exist_ok=True)
            cv2.imwrite(os.path.join(tdir, f"{name}.jpg"), np.hstack(sample))
        print(name, json.dumps(res[name]))
    json.dump(res, open(out, "w"), indent=1)


if __name__ == "__main__":
    main()
