"""Path B, step 1: read the generated orca (gen/a_orca_side_v2.png) as a REFERENCE and turn it into structured,
named geometry for the hand-built component (orca-b/OrcaB.tsx).

What is measured from the image: the outer silhouette, the bone patches (eye patch, throat/belly, flank lobe),
the saddle, and the position / length / angle of every light surface mark (scars, nicks, pores). What is decided
by hand (the cut lines below): where the dorsal fin, fluke, pectoral fins and lower jaw separate from the body,
and the hidden overlap each detachable part keeps so it can rotate without opening a gap.

Shading is NOT taken from the image: the component re-shades every part from one light vector (bible §4.3).

usage: .venv/bin/python scripts/extract_orca.py   ->  orca-b/orca_geom.json (+ orca-b/extract_debug.jpg)
"""
import json, os
import cv2, numpy as np

G = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(G, 'gen', 'a_orca_side_v2.png')
OUT = os.path.join(G, 'orca-b')
os.makedirs(OUT, exist_ok=True)

im = cv2.imread(SRC)
H, W = im.shape[:2]
hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
V = hsv[..., 2].astype(np.int16)

# ---------- silhouette ----------
bg = np.median(np.concatenate([im[:40].reshape(-1, 3), im[-40:].reshape(-1, 3)]), 0)
d = np.linalg.norm(im.astype(float) - bg, axis=2)
m = ((d > 28) * 255).astype(np.uint8)
m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
n, lab, st, _ = cv2.connectedComponentsWithStats(m)
sil = (lab == 1 + np.argmax(st[1:, 4])).astype(np.uint8) * 255
cs, _ = cv2.findContours(sil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
sil = np.zeros_like(sil)
cv2.drawContours(sil, cs, -1, 255, -1)
S = sil > 0


def poly_mask(pts):
    mm = np.zeros((H, W), np.uint8)
    cv2.fillPoly(mm, [np.array(pts, np.int32)], 255)
    return mm > 0


def clean(mask, k=5):
    mm = (mask * 255).astype(np.uint8) if mask.dtype == bool else mask
    mm = cv2.morphologyEx(mm, cv2.MORPH_OPEN, np.ones((k, k), np.uint8))
    mm = cv2.morphologyEx(mm, cv2.MORPH_CLOSE, np.ones((k, k), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(mm)
    if n <= 1:
        return mm > 0
    return lab == 1 + np.argmax(st[1:, 4])


def to_path(mask, eps=1.2, smooth=0.5):
    """largest contour -> closed Catmull-Rom cubic path string"""
    mm = (mask.astype(np.uint8)) * 255
    cs, _ = cv2.findContours(mm, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    c = max(cs, key=cv2.contourArea)
    p = cv2.approxPolyDP(c, eps, True)[:, 0, :].astype(float)
    n = len(p)
    out = [f'M {p[0][0]:.1f} {p[0][1]:.1f}']
    for i in range(n):
        p0, p1, p2, p3 = p[(i - 1) % n], p[i], p[(i + 1) % n], p[(i + 2) % n]
        c1 = p1 + (p2 - p0) * smooth / 3
        c2 = p2 - (p3 - p1) * smooth / 3
        out.append(f'C {c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}')
    return ' '.join(out) + ' Z', len(p)


# ---------- hand-placed cut lines (image px) ----------
DORSAL_CUT = [(660, 352), (1010, 326)]          # back line under the dorsal fin
FLUKE_CUT_X = 250                               # peduncle notch
HINGE = (1300, 528)                              # jaw hinge
# near pectoral: generous outside the body, tight at the root inside the body
PEC_NEAR_POLY = [(1088, 556), (1140, 556), (1186, 590), (1186, 650), (1160, 720), (1110, 820), (1050, 900), (960, 905),
                 (915, 880), (915, 800), (945, 700), (990, 640), (1040, 590)]
PEC_FAR_BOX = [(1140, 640), (1275, 640), (1275, 820), (1140, 820)]
JAW_POLY = [(1290, 520), (1330, 516), (1420, 517), (1515, 512), (1540, 512), (1540, 700), (1290, 700)]


def line_y(x, a, b):
    return a[1] + (b[1] - a[1]) * (x - a[0]) / (b[0] - a[0])


yy, xx = np.mgrid[0:H, 0:W]

# dorsal = silhouette above the back line
dor = S & (yy < line_y(xx, *DORSAL_CUT)) & (xx > DORSAL_CUT[0][0]) & (xx < DORSAL_CUT[1][0])
dor = clean(dor)
# hidden overlap below the cut (drawn behind the body)
dor_ext = dor | (poly_mask([(700, 330), (990, 318), (990, 372), (700, 382)]) & ~dor)

# fluke = silhouette left of the peduncle notch, with a hidden stub into the stock
fl = clean(S & (xx < FLUKE_CUT_X))
stock = S & (xx >= FLUKE_CUT_X) & (xx < FLUKE_CUT_X + 60)
fl_ext = fl | cv2.erode(stock.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)

# near pectoral
bone = (hsv[..., 2] > 170) & (hsv[..., 1] < 90) & S
pn_region = poly_mask(PEC_NEAR_POLY)
pn = clean(S & pn_region & ~(bone & (yy < 700)), 7)
# rounded flipper root (the 'elbow' the reference shows), so the fin can rotate without a notch
root = np.zeros((H, W), np.uint8)
cv2.ellipse(root, (1128, 618), (52, 64), -30, 0, 360, 255, -1)
pn = clean(pn | ((root > 0) & S), 7)
# far pectoral = dark pixels in its box that are not the near fin / belly
pf = clean(S & poly_mask(PEC_FAR_BOX) & ~bone & ~pn_region & (yy > 640), 5)
pf_ext = pf | (poly_mask([(1150, 610), (1250, 610), (1250, 670), (1150, 670)]))

# body: silhouette minus the detachable parts; under the near fin the lower outline is interpolated
body = S & ~dor & ~fl & ~pf
cols = {}
for x in range(860, 1300):
    ys = np.where(S[:, x] & ~pn_region[:, x] & ~pf[:, x])[0]
    if len(ys):
        cols[x] = ys.max()
xa, xb = 900, 1188  # body bottom edge just outside the fin
ya = max(np.where(S[:, xa] & ~pn_region[:, xa])[0])
yb = max(np.where(S[:, xb] & ~pn_region[:, xb] & ~pf[:, xb] & (np.arange(H) < 700))[0])
for x in range(xa, xb + 1):
    t = (x - xa) / (xb - xa)
    ycut = ya + (yb - ya) * t - 14 * np.sin(np.pi * t)  # slight belly sag kept smooth
    body[int(ycut) + 1:, x] = False
body = clean(body | (S & ~pn & ~dor & ~fl & ~pf & (yy < 640) & (xx > 900) & (xx < 1300)), 3)
# add the hidden belly under the fin (between the cut curve and the near fin)
under = np.zeros_like(body)
for x in range(xa, xb + 1):
    t = (x - xa) / (xb - xa)
    ycut = ya + (yb - ya) * t - 14 * np.sin(np.pi * t)
    top = np.where(body[:, x])[0]
    if len(top):
        under[top.min():int(ycut) + 1, x] = True
body = clean(body | under, 3)

jaw = clean(body & poly_mask(JAW_POLY), 3)
upper = clean(body & ~poly_mask(JAW_POLY), 3)

# bone patches (eye patch, throat/belly, flank lobe) inside the body (clipped decals)
bn = cv2.morphologyEx((bone * 255).astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
n, lab, st, cen = cv2.connectedComponentsWithStats(bn)
patches = []
for i in range(1, n):
    if st[i, 4] < 1500:
        continue
    mk = lab == i
    cx, cy = cen[i]
    name = 'eyePatch' if cy < 520 and cx > 1100 else ('throat' if cx > 1100 else 'flank')
    # throat/belly continues under the near fin; extend it toward the flank so the fin never reveals a hole
    pth, npts = to_path(mk, eps=1.5)
    patches.append(dict(name=name, d=pth, cx=float(cx), cy=float(cy), area=int(st[i, 4])))

# saddle
sad = (hsv[..., 2] > 80) & (hsv[..., 2] < 175) & (hsv[..., 1] < 120) & S
sad = clean(cv2.morphologyEx((sad * 255).astype(np.uint8), cv2.MORPH_OPEN, np.ones((9, 9), np.uint8)) > 0, 9)

# eye
eye = dict(cx=1352.0, cy=490.0, r=9.0)

# ---------- surface marks (light strokes / dots on dark skin) ----------
skin = S & ~bone & ~sad
inner = cv2.erode(S.astype(np.uint8), np.ones((19, 19), np.uint8)).astype(bool)
bgV = cv2.medianBlur(hsv[..., 2], 21).astype(np.int16)
mk = ((V - bgV) > 22) & skin & inner
mk = cv2.morphologyEx((mk * 255).astype(np.uint8), cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
n, lab, st, cen = cv2.connectedComponentsWithStats(mk)
marks = []
part_of = lambda x, y: ('dorsal' if dor[y, x] else 'fluke' if fl[y, x] else 'pecNear' if pn[y, x] else
                        'pecFar' if pf[y, x] else 'jaw' if jaw[y, x] else 'body')
for i in range(1, n):
    a = st[i, 4]
    if a < 4 or a > 900:
        continue
    ys, xs = np.where(lab == i)
    pts = np.stack([xs, ys], 1).astype(float)
    mu = pts.mean(0)
    cov = np.cov((pts - mu).T) if len(pts) > 2 else np.eye(2)
    ev, evec = np.linalg.eigh(cov)
    major = evec[:, 1]
    proj = (pts - mu) @ major
    L = proj.max() - proj.min() + 1
    w = max(1.0, a / L)
    col = im[ys, xs].mean(0)  # BGR
    lum = float(V[ys, xs].mean())
    kind = 'scar' if L > 3.2 * w and L > 8 else 'dot'
    rec = dict(kind=kind, part=part_of(int(mu[0]), int(mu[1])), x=round(float(mu[0]), 1), y=round(float(mu[1]), 1),
               lum=round(lum))
    if kind == 'scar':
        ang = float(np.degrees(np.arctan2(major[1], major[0])))
        rec.update(len=round(float(L), 1), w=round(float(min(w, 4.0)), 2), ang=round(ang, 1))
    else:
        rec.update(r=round(float(np.sqrt(a / np.pi)), 2))
    marks.append(rec)

# fin-edge nicks (trailing edge of the dorsal): concavities of the dorsal contour
c = max(cv2.findContours((dor * 255).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0], key=cv2.contourArea)
hull = cv2.convexHull(c, returnPoints=False)
defects = cv2.convexityDefects(c, hull)
nicks = []
if defects is not None:
    for s, e, f, depth in defects.reshape(-1, 4):
        if 4 * 256 < depth < 40 * 256:
            p = c[f][0]
            if p[1] < 300:
                nicks.append(dict(x=int(p[0]), y=int(p[1]), depth=round(depth / 256, 1)))

geom = dict(
    src='gen/a_orca_side_v2.png', W=W, H=H,
    parts=dict(
        body=to_path(body, 1.2)[0], upper=to_path(upper, 1.2)[0], jaw=to_path(jaw, 1.0)[0],
        dorsal=to_path(dor_ext, 1.0)[0], fluke=to_path(fl_ext, 1.0)[0],
        pecNear=to_path(pn, 1.2)[0], pecFar=to_path(pf_ext, 1.2)[0], saddle=to_path(sad, 1.5)[0],
    ),
    pivots=dict(dorsal=[845, 345], fluke=[FLUKE_CUT_X + 20, 560], pecNear=[1140, 600], pecFar=[1200, 650],
                jaw=list(HINGE), bodyHead=[1505, 515], bodyTail=[23, 578]),
    patches=patches, eye=eye, marks=marks, nicks=nicks,
)
json.dump(geom, open(os.path.join(OUT, 'orca_geom.json'), 'w'))
from collections import Counter
print('marks', len(marks), Counter((m['part'], m['kind']) for m in marks))
print('patches', [(p['name'], p['area']) for p in patches], 'nicks', len(nicks))

# debug overlay
dbg = (im * 0.35).astype(np.uint8)
for mask, colr in [(body, (90, 60, 30)), (dor, (0, 140, 255)), (fl, (255, 0, 255)), (pn, (0, 255, 0)), (pf, (0, 255, 255)),
                   (jaw, (255, 255, 0)), (sad, (200, 200, 200))]:
    dbg[mask] = (dbg[mask] * 0.4 + np.array(colr) * 0.6).astype(np.uint8)
for m_ in marks:
    cv2.circle(dbg, (int(m_['x']), int(m_['y'])), 3, (0, 0, 255), -1)
cv2.imwrite(os.path.join(OUT, 'extract_debug.jpg'), dbg)
