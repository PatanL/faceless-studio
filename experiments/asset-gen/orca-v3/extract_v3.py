"""OrcaV3 step 1: measure the flat v3 reference orcas and write named, rig-ready geometry (orca-v3/geom_v3.json).

Same approach as scripts/extract_orca.py (path B): the image is a REFERENCE, read for silhouette, flat colour
patches and the flat shadow shapes; the cut lines, pivots and hidden overlaps are placed by hand. The v3 images are
flat (a handful of colours), so every pixel is classified to the nearest palette colour first, and each named part
gets its base path plus one flat shadow path. No marks are extracted (the v3 look has almost none).

  side   gen/a_orca_side_v3.png       (the owner's chosen look)
  front  orca-v3/refs/orca_v3_front_v1.png   (Codex, head-on; orca-v3/prompts/orca_v3_front.txt)
  below  orca-v3/refs/orca_v3_below_v1.png   (Codex, from below; orca-v3/prompts/orca_v3_below.txt)

Front and below are mirrored from their left half so the rig stays symmetric.

usage: python3 orca-v3/extract_v3.py   ->  orca-v3/geom_v3.json + orca-v3/out/extract_{side,front,below}.jpg
"""
import json, os
import cv2, numpy as np

G = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(G, 'orca-v3')
os.makedirs(os.path.join(OUT, 'out'), exist_ok=True)

# palette sampled from a_orca_side_v3.png (k-means centres); classes in this order
PAL = dict(bg='17187c', lit='19134d', dark='120d3c', white='f3f1ee', wsh='e2e1e0', saddle='9998b0', eye='05040f')
NAMES = list(PAL)
BG, LIT, DARK, WHITE, WSH, SADDLE, EYE = range(len(NAMES))
MAX_SEG = 12


def classify(im, pal=PAL):
    cols = np.array([[int(h[4:6], 16), int(h[2:4], 16), int(h[0:2], 16)] for h in pal.values()], np.float32)
    d = ((im.astype(np.float32)[:, :, None, :] - cols[None, None]) ** 2).sum(-1)
    lab = d.argmin(-1)
    # a 3x3 mode filter removes the anti-aliasing fringe (a 1 px band of 'in-between' classes on every edge)
    out = lab.copy()
    for k in range(len(cols)):
        m = (lab == k).astype(np.uint8)
        cnt = cv2.blur(m.astype(np.float32), (5, 5))
        out[(cnt > 0.6) & (lab != k)] = k
    return out


def poly_mask(shape, pts):
    mm = np.zeros(shape, np.uint8)
    cv2.fillPoly(mm, [np.array(pts, np.int32)], 255)
    return mm > 0


def clean(mask, k=5, keep='largest', min_area=400):
    mm = (mask * 255).astype(np.uint8) if mask.dtype == bool else mask
    if k > 1:
        mm = cv2.morphologyEx(mm, cv2.MORPH_OPEN, np.ones((k, k), np.uint8))
        mm = cv2.morphologyEx(mm, cv2.MORPH_CLOSE, np.ones((k, k), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(mm)
    if n <= 1:
        return mm > 0
    if keep == 'largest':
        return lab == 1 + np.argmax(st[1:, 4])
    return np.isin(lab, [i for i in range(1, n) if st[i, 4] >= min_area])


def fill_holes(mask):
    mm = (mask * 255).astype(np.uint8)
    cs, _ = cv2.findContours(mm, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    out = np.zeros_like(mm)
    cv2.drawContours(out, cs, -1, 255, -1)
    return out > 0


def to_paths(mask, eps=1.4, smooth=0.5, min_area=300, holes=False):
    """contours (area >= min_area) -> closed Catmull-Rom cubic paths in one 'd' string. holes=True also emits the
    inner contours (draw with fill-rule evenodd), e.g. a shadow shape grown around its part"""
    mm = (mask.astype(np.uint8)) * 255
    cs, _ = cv2.findContours(mm, cv2.RETR_CCOMP if holes else cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    out = []
    for c in sorted(cs, key=cv2.contourArea, reverse=True):
        if cv2.contourArea(c) < min_area:
            continue
        p = cv2.approxPolyDP(c, eps, True)[:, 0, :].astype(float)
        if len(p) < 3:
            continue
        # densify: no segment longer than MAX_SEG px, so the rig's non-rigid point warps (jaw, flipper, dorsal) move
        # every outline the same way and decal edges stay glued to the part outline
        q = []
        for i in range(len(p)):
            a, b = p[i], p[(i + 1) % len(p)]
            k = max(1, int(np.ceil(np.hypot(*(b - a)) / MAX_SEG)))
            q += [a + (b - a) * j / k for j in range(k)]
        p = np.array(q)
        n = len(p)
        s = [f'M {p[0][0]:.1f} {p[0][1]:.1f}']
        for i in range(n):
            p0, p1, p2, p3 = p[(i - 1) % n], p[i], p[(i + 1) % n], p[(i + 2) % n]
            c1 = p1 + (p2 - p0) * smooth / 3
            c2 = p2 - (p3 - p1) * smooth / 3
            s.append(f'C {c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}')
        out.append(' '.join(s) + ' Z')
    return ' '.join(out)


def grow_out(shadow, part, r=70):
    """extend a flat shadow shape OUTSIDE its part (never inside), so the shape can slide with the light and stay
    clipped to the part without exposing its own back edge"""
    dil = cv2.dilate(shadow.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))) > 0
    return shadow | (dil & ~part)


def debug(name, im, layers):
    dbg = (im * 0.3).astype(np.uint8)
    for mask, colr in layers:
        dbg[mask] = (dbg[mask] * 0.35 + np.array(colr) * 0.65).astype(np.uint8)
    cv2.imwrite(os.path.join(OUT, 'out', f'extract_{name}.jpg'), dbg, [cv2.IMWRITE_JPEG_QUALITY, 80])


# ============================================================================================ side
def side():
    im = cv2.imread(os.path.join(G, 'gen', 'a_orca_side_v3.png'))
    H, W = im.shape[:2]
    lab = classify(im)
    S = fill_holes(clean(lab != BG, 3))
    yy, xx = np.mgrid[0:H, 0:W]
    pm = lambda pts: poly_mask((H, W), pts)

    # ---- hand-placed cuts (image px)
    FLUKE_X = 272                                    # peduncle notch: fluke = silhouette left of this
    LOBE_Y = 547                                     # split between the upper and lower fluke lobe
    DORSAL_CUT = [(690, 393), (760, 379), (877, 358), (980, 360)]   # just under the fin's dark base line
    HINGE = (1288, 528)                              # jaw hinge (behind the gape)
    PEC_POLY = [(1000, 590), (1160, 590), (1165, 660), (1140, 760), (1060, 860), (940, 860), (930, 760), (970, 650)]

    cut_y = np.interp(xx, [p[0] for p in DORSAL_CUT], [p[1] for p in DORSAL_CUT])
    dorsal_zone = (yy < cut_y) & (xx > DORSAL_CUT[0][0]) & (xx < DORSAL_CUT[-1][0])

    # ---- near flipper: lit pixels in its zone + its dark trailing strip, as one convex leaf
    zone = pm(PEC_POLY)
    pl = clean(zone & (lab == LIT) & (yy > 585), 5)
    strip = zone & (lab == DARK) & (yy > 676)
    pts = np.argwhere(pl | clean(strip, 3, keep='all', min_area=50))[:, ::-1].astype(np.int32)
    hull = cv2.convexHull(pts)
    pec = np.zeros((H, W), np.uint8)
    cv2.fillPoly(pec, [hull], 255)
    pec = (pec > 0) & S
    pec_dark = pec & (lab == DARK) & (yy > 640)
    pec_dark = clean(pec_dark, 3)

    # ---- body labels hidden under the flipper: interpolate each horizontal boundary across the flipper
    lab2 = lab.copy()
    cover = cv2.dilate(pec.astype(np.uint8), np.ones((7, 7), np.uint8)) > 0
    x0, x1 = int(np.argwhere(pec)[:, 1].min()) - 4, int(np.argwhere(pec)[:, 1].max()) + 4
    xs_fit = [x for x in list(range(x0 - 70, x0)) + list(range(x1, x1 + 70))]
    def boundary(x, fn):
        col = lab[:, x]
        return fn(col)
    b_white = lambda col: next((y for y in range(560, 760) if col[y] in (WHITE, WSH)), None)      # dark -> white
    b_wsh = lambda col: next((y for y in range(600, 780) if col[y] == WSH), None)                 # white -> its shadow
    b_bot = lambda col: max([y for y in range(560, 800) if col[y] != BG] or [None])               # bottom outline
    fits = {}
    for nm, fn in [('w', b_white), ('s', b_wsh), ('b', b_bot)]:
        X, Y = [], []
        for x in xs_fit:
            y = boundary(x, fn)
            if y is not None and not cover[max(0, y - 3):y + 4, x].any():
                X.append(x)
                Y.append(y)
        fits[nm] = np.polyfit(X, Y, 3)
    for x in range(x0, x1 + 1):
        yw, ys, yb = (np.polyval(fits[k], x) for k in 'wsb')
        for y in np.where(cover[:, x])[0]:
            if y < 560:
                continue
            lab2[y, x] = DARK if y < yw else WHITE if y < ys else WSH if y < yb else BG
    # body silhouette with the flipper removed (hidden belly reconstructed)
    Sb = fill_holes(clean(lab2 != BG, 3))

    # ---- parts
    fluke = Sb & (xx < FLUKE_X + 4)
    stub = clean(cv2.erode((Sb & (xx >= FLUKE_X) & (xx < FLUKE_X + 70)).astype(np.uint8), np.ones((9, 9), np.uint8)) > 0, 1)
    # the lobes are separated by background left of the notch tip; right of it they overlap by a few px
    notch_x = max(x for x in range(90, FLUKE_X) if (lab2[LOBE_Y - 3:LOBE_Y + 4, x] == BG).any())
    lobeU = clean(fluke & (yy < LOBE_Y), 7) | (stub & (yy < 552))
    # the lower lobe reaches 22 px up under the upper lobe (hidden at rest), so the lobes can scissor apart
    # without opening a gap between them
    lobeL = clean(fluke & ((yy >= LOBE_Y) | ((yy >= LOBE_Y - 22) & (xx > notch_x + 10))), 3) | (stub & (yy >= 528))
    dorsal = clean(Sb & dorsal_zone, 3)
    # hidden stub: a 40 px band under the cut line, kept 6 px inside the body outline so it never shows
    inner = cv2.erode(Sb.astype(np.uint8), np.ones((13, 13), np.uint8)) > 0
    dorsal_stub = inner & (yy >= cut_y - 2) & (yy < cut_y + 40) & (xx > DORSAL_CUT[0][0] + 20) & (xx < DORSAL_CUT[-1][0] - 10)
    # the body ends in a taper along the lobe split (not a vertical cut): its dark lower half then tapers to a point
    # over the lit lower lobe, as in the reference, and the end never shows as an edge
    taper = pm([(FLUKE_X + 2, 512), (FLUKE_X + 2, 588), (238, LOBE_Y + 1)])
    body = clean(Sb & ~dorsal & (~(xx < FLUKE_X) | taper), 3)

    def shade(part, cls, k=3, r=70):
        m = clean(part & np.isin(lab2, cls), k, keep='all', min_area=120)
        return m, grow_out(m, part, r)

    lobeU_d, lobeU_dx = shade(lobeU, [DARK], 5)
    lobeL_d, lobeL_dx = shade(lobeL, [DARK], 7)
    dor_d, dor_dx = shade(dorsal | dorsal_stub, [DARK])   # never grow into the stub: the body edge would pick it up
    body_d, body_dx = shade(body, [DARK], 3, 40)
    pec_dx = grow_out(pec_dark, pec, 60)

    # white patches: eye patch (above the eye), belly+chin (one region incl. its shadow strip), flank lobe
    wl = clean(body & np.isin(lab2, [WHITE, WSH]), 3, keep='all', min_area=500)
    n, cc, st, cen = cv2.connectedComponentsWithStats(wl.astype(np.uint8))
    patches = {}
    for i in range(1, n):
        cx, cy = cen[i]
        nm = 'eyePatch' if cy < 520 else 'belly'
        patches[nm] = patches.get(nm, np.zeros_like(wl)) | (cc == i)
    wsh = clean(body & (lab2 == WSH), 3, keep='all', min_area=200)
    saddle = clean(body & (lab2 == SADDLE), 5)

    # jaw: body below the mouth line (= top edge of the chin white) in front of the hinge, + an overlap behind it
    mouth = []
    for x in range(HINGE[0], 1458, 6):
        ys = np.where(np.isin(lab2[:, x], [WHITE, WSH]) & (np.arange(H) > 516) & (np.arange(H) < 600))[0]
        if len(ys):
            mouth.append((x, int(ys.min())))
    my = np.array([m[1] for m in mouth], float)
    my = np.array([np.median(my[max(0, i - 2):i + 3]) for i in range(len(my))])   # drop the eye-glint spikes
    mouth = [(m[0], float(y)) for m, y in zip(mouth, my)]
    tip = (1460, 532)
    mouth.append(tip)
    jaw_poly = mouth + [(1470, 560), (1470, 720), (HINGE[0] - 60, 720), (HINGE[0] - 60, mouth[0][1] + 6)]
    jaw = clean(body & pm(jaw_poly), 3)
    eye = dict(cx=1315.0, cy=508.5, r=7.5)
    ey = np.argwhere(lab2[490:530, 1300:1330] == EYE)
    if len(ey):
        eye = dict(cx=float(1300 + ey[:, 1].mean()), cy=float(490 + ey[:, 0].mean()), r=7.5)

    debug('side', im, [(body, (120, 70, 40)), (body_d, (90, 30, 30)), (dorsal, (0, 140, 255)), (lobeU, (255, 0, 255)),
                       (lobeL, (180, 0, 120)), (pec, (0, 255, 0)), (pec_dark, (0, 120, 0)), (jaw, (255, 255, 0)),
                       (patches.get('belly', body & False), (230, 230, 230)), (wsh, (160, 200, 160)), (saddle, (200, 120, 255))])
    P = lambda m, e=1.4: to_paths(m, e)
    PH = lambda m, e=1.4: to_paths(m, e, holes=True)
    return dict(
        src='gen/a_orca_side_v3.png', W=W, H=H,
        parts=dict(
            body=P(body, 1.2), bodyDark=PH(body_dx, 1.6), jaw=P(jaw, 1.2),
            dorsal=P(dorsal | dorsal_stub, 1.2), dorsalDark=PH(dor_dx),
            lobeU=P(lobeU, 1.0), lobeUDark=PH(lobeU_dx, 1.2), lobeL=P(lobeL, 1.0), lobeLDark=PH(lobeL_dx, 1.2),
            pecNear=P(pec, 1.0), pecNearDark=PH(pec_dx, 1.2),
            eyePatch=P(patches['eyePatch'], 1.2), belly=P(patches['belly'], 1.2), bellyShadow=PH(grow_out(wsh, body, 30), 1.4),
            saddle=P(saddle, 1.4),
        ),
        mouth=mouth,
        pivots=dict(dorsalBase=[830, 368], flukeRoot=[FLUKE_X + 6, 548], pecNear=[1100, 625], jaw=list(HINGE),
                    head=[1460, 532], tail=[75, 548]),
        cutY=DORSAL_CUT, eye=eye,
        box=[int(np.argwhere(S)[:, 1].min()), int(np.argwhere(S)[:, 0].min()),
             int(np.argwhere(S)[:, 1].max() - np.argwhere(S)[:, 1].min()), int(np.argwhere(S)[:, 0].max() - np.argwhere(S)[:, 0].min())],
    )


# ============================================================================================ symmetric views
def mirror_sym(mask, cx):
    """keep the left half (x < cx) and mirror it about x = cx, so the view is exactly symmetric"""
    H, W = mask.shape
    left = mask.copy()
    left[:, int(np.floor(cx)) + 1:] = False
    xs = np.arange(W)
    src = np.clip(np.round(2 * cx - xs).astype(int), 0, W - 1)
    right = left[:, src] & (xs[None, :] >= cx)
    return left | right


def front():
    """head-on view (approaching): head disc, dorsal behind it, two flippers in front, saddle, mask band, eye
    patches, chin + its flat shadow, two eyes. Mirrored from the left half."""
    im = cv2.imread(os.path.join(OUT, 'refs', 'orca_v3_front_v1.png'))
    H, W = im.shape[:2]
    CX = 767.0
    lab = classify(im)
    yy, xx = np.mgrid[0:H, 0:W]
    sym = lambda m: mirror_sym(m, CX)
    S = sym(fill_holes(clean(lab != BG, 3)))
    # flipper (left) = silhouette left of the head below y 630 that is lit/dark navy and outside a circle fitted to
    # the visible head outline; the head outline hidden under the flipper root comes from that circle
    head_rows = [(y, np.nonzero(S[y])[0]) for y in range(330, 630, 4)]
    pts = [(xs.min(), y) for y, xs in head_rows if len(xs)] + [(xs.max(), y) for y, xs in head_rows if len(xs)]
    pts += [(x, max(np.nonzero(S[:, x])[0])) for x in range(560, 975, 6)]
    pts = np.array(pts, np.float32)
    # algebraic circle fit with the centre on the symmetry axis: (x-CX)^2 + (y-b)^2 = r^2
    A = np.c_[2 * pts[:, 1], np.ones(len(pts))]
    rhs = (pts[:, 0] - CX) ** 2 + pts[:, 1] ** 2
    (bcy, c0), *_ = np.linalg.lstsq(A, rhs, rcond=None)
    rr = np.sqrt(c0 + bcy ** 2)
    disc = (xx - CX) ** 2 + (yy - bcy) ** 2 <= rr ** 2
    flipL = clean(S & (xx < CX) & (yy > 600) & ~disc, 27)   # big opening: no thin sliver along the head outline
    disc_big = (xx - CX) ** 2 + (yy - bcy) ** 2 <= (rr + 3) ** 2
    # upper half = the fitted circle itself (clean crown, the fin sits behind it); lower half = the measured outline
    head = sym(clean((S & ~flipL & disc_big & (yy > bcy)) | (disc & (yy <= bcy)) | (disc & (yy > 560)), 21))
    flipL_d = clean(flipL & (lab == DARK), 5, keep='all', min_area=200)
    dorsal = clean(S & ~disc & (yy < bcy) & (np.abs(xx - CX) < 140), 9)
    # hidden stub: overlaps the crown (the fin is drawn behind the head), so the fin root never shows a seam
    dstub = disc & (yy < bcy - rr + 70) & (np.abs(xx - CX) < 62)
    dorsal = sym(dorsal | dstub)
    dorsal_d = dorsal & (xx < CX - 4)                     # flat split: the fin's left half is in shade
    body = head
    sad = sym(clean(head & (lab == SADDLE), 3, keep='all', min_area=200))
    band = sym(clean(head & (lab == DARK) & (yy > 420), 5, keep='all', min_area=300))
    eyeP = sym(clean(head & (lab == WHITE) & (yy < 590), 5, keep='all', min_area=300))
    chin = sym(clean(head & np.isin(lab, [WHITE, WSH]) & (yy >= 580), 5, keep='all', min_area=300))
    chin_s = sym(clean(head & (lab == WSH), 5, keep='all', min_area=300))
    # smile line = top edge of the chin, sampled across the face (left half, mirrored)
    smile = []
    for x in range(int(CX - 250), int(CX) + 1, 10):
        ys = np.nonzero(chin[:, x])[0]
        if len(ys):
            smile.append((float(x), float(ys.min())))
    sm = np.array(smile)
    sm[:, 1] = np.convolve(np.pad(sm[:, 1], 2, mode='edge'), np.ones(5) / 5, mode='valid')   # soften the AI wiggles
    smile = [tuple(p) for p in sm] + [(2 * CX - x, y) for x, y in sm[::-1][1:]]
    smx = np.array([p[0] for p in smile])
    smy = np.array([p[1] for p in smile])
    jaw = body & (yy > np.interp(xx, smx, smy) - 1)          # head below the smile (lower jaw), corners included
    ey = np.argwhere((lab == EYE) & (xx < CX))
    ecx_, ecy_ = (float(ey[:, 1].mean()), float(ey[:, 0].mean())) if len(ey) else (567.0, 565.0)
    xs = np.arange(W)
    src = np.clip(np.round(2 * CX - xs).astype(int), 0, W - 1)
    flipR = flipL[:, src]
    flipR_d = flipL_d[:, src]
    debug('front', im, [(body, (120, 70, 40)), (dorsal, (0, 140, 255)), (flipL, (0, 255, 0)), (flipR, (0, 200, 0)),
                        (band, (90, 30, 30)), (chin, (230, 230, 230)), (chin_s, (160, 200, 160)), (sad, (200, 120, 255)), (eyeP, (255, 255, 0))])
    P = lambda m, e=1.4: to_paths(m, e)
    PH = lambda m, part, r=50, e=1.4: to_paths(grow_out(m, part, r), e, holes=True)
    return dict(
        src='orca-v3/refs/orca_v3_front_v1.png', W=W, H=H, cx=CX,
        parts=dict(head=P(body, 1.0), dorsal=P(dorsal, 1.2), dorsalDark=PH(dorsal_d, dorsal, 40),
                   flipL=P(flipL, 1.2), flipLDark=PH(flipL_d, flipL), flipR=P(flipR, 1.2), flipRDark=PH(flipR_d, flipR),
                   saddle=P(sad), band=PH(band, body, 30), jaw=P(jaw, 1.0), eyePatch=P(eyeP), chin=P(chin, 1.2), chinShadow=PH(chin_s, chin, 30)),
        smile=smile, eyes=[[ecx_, ecy_], [2 * CX - ecx_, ecy_]],
        pivots=dict(flipL=[505, 690], flipR=[2 * CX - 505, 690], dorsalBase=[CX, 330]),
        box=[int(np.argwhere(S)[:, 1].min()), int(np.argwhere(S)[:, 0].min()),
             int(np.ptp(np.argwhere(S)[:, 1])), int(np.ptp(np.argwhere(S)[:, 0]))],
    )


def below():
    """from underneath, rising (head up): body with dark sides, white throat/belly/flank patches, two flippers behind
    the body, flukes with pale undersides. Mirrored from the left half."""
    im = cv2.imread(os.path.join(OUT, 'refs', 'orca_v3_below_v1.png'))
    H, W = im.shape[:2]
    CX = 767.5
    lab = classify(im)
    yy, xx = np.mgrid[0:H, 0:W]
    sym = lambda m: mirror_sym(m, CX)
    S = sym(fill_holes(clean(lab != BG, 3)))
    # body outline under the flippers: the visible side edge just above / below the flipper, joined by a spline
    def edge(y):
        xs = np.nonzero(S[y, :int(CX)])[0]
        return xs.min() if len(xs) else None
    ya, yb = 288, 505
    xa, xb = edge(ya), edge(yb)
    yk = np.arange(ya, yb + 1)
    xk = xa + (xb - xa) * (yk - ya) / (yb - ya) - 6 * np.sin(np.pi * (yk - ya) / (yb - ya))
    side = np.zeros((H, W), bool)
    for y, x in zip(yk, xk):
        side[y, :int(round(x))] = True
    flipL = clean(S & side & (xx < CX), 5)
    body = sym(clean(S & ~flipL, 3))
    # hidden flipper root under the body edge
    flipL = clean(flipL | (cv2.dilate(flipL.astype(np.uint8), np.ones((1, 41), np.uint8)).astype(bool) & body & (xx < CX - 60)), 3)
    flipL_d = clean(flipL & (lab == DARK) & (yy > 380), 5, keep='all', min_area=200)
    # flukes: below the peduncle, behind the body, + a stub up the peduncle
    FL_Y = 842
    fl = clean(S & (yy > FL_Y), 3, keep='all', min_area=500)
    fl = sym(fl | (body & (yy > FL_Y - 40) & (np.abs(xx - CX) < 14)))
    fl_pale = sym(clean(fl & (lab == WSH), 5, keep='all', min_area=200))
    body = sym(clean(body & ~((yy > FL_Y + 6) & fl), 3))
    white = sym(clean(body & np.isin(lab, [WHITE]) & (yy <= FL_Y + 8), 5, keep='all', min_area=400))
    rim = sym(clean(body & (lab == LIT) & (yy < 300), 7, keep='all', min_area=300))  # lit head rim (upper jaw edge)
    HINGE_Y = 205
    jaw = sym(clean(white & (yy < HINGE_Y + 40) & (np.abs(xx - CX) < 96), 15))   # throat only, not the side crescents
    ey = np.argwhere((lab == EYE) & (xx < CX) & (yy < 220))
    eye = (float(ey[:, 1].mean()), float(ey[:, 0].mean())) if len(ey) else (672.0, 160.0)
    # jaw rim: outline of the lower jaw from the left hinge over the tip to the right hinge (upper tooth row sits here)
    rimL = []
    for y in range(HINGE_Y, 0, -8):
        xs_ = np.nonzero(jaw[y, :int(CX)])[0]
        if len(xs_):
            rimL.append((float(xs_.min()), float(y)))
    tipY = float(np.nonzero(jaw[:, int(CX)])[0].min())
    jawRim = rimL + [(CX, tipY)] + [(2 * CX - x, y) for x, y in rimL[::-1]]
    src = np.clip(np.round(2 * CX - np.arange(W)).astype(int), 0, W - 1)
    flipR, flipR_d = flipL[:, src], flipL_d[:, src]
    debug('below', im, [(body, (120, 70, 40)), (white, (230, 230, 230)), (rim, (255, 180, 120)), (flipL, (0, 255, 0)),
                        (flipR, (0, 200, 0)), (fl, (255, 0, 255)), (fl_pale, (160, 200, 160)), (jaw, (255, 255, 0))])
    P = lambda m, e=1.4: to_paths(m, e)
    PH = lambda m, part, r=50, e=1.4: to_paths(grow_out(m, part, r), e, holes=True)
    return dict(
        src='orca-v3/refs/orca_v3_below_v1.png', W=W, H=H, cx=CX,
        parts=dict(body=P(body, 1.0), white=P(white, 1.2), rim=PH(rim, body, 30), jaw=P(jaw, 1.0),
                   flipL=P(flipL, 1.2), flipLDark=PH(flipL_d, flipL), flipR=P(flipR, 1.2), flipRDark=PH(flipR_d, flipR),
                   fluke=P(fl, 1.0), flukePale=PH(fl_pale, fl, 30)),
        eyes=[[eye[0], eye[1]], [2 * CX - eye[0], eye[1]]], jawRim=jawRim,
        pivots=dict(flipL=[640, 330], flipR=[2 * CX - 640, 330], flukeRoot=[CX, FL_Y - 20], hingeY=HINGE_Y,
                    head=[CX, 36], tail=[CX, 940]),
        box=[int(np.argwhere(S)[:, 1].min()), int(np.argwhere(S)[:, 0].min()),
             int(np.ptp(np.argwhere(S)[:, 1])), int(np.ptp(np.argwhere(S)[:, 0]))],
    )


if __name__ == '__main__':
    geom = dict(side=side(), front=front(), below=below())
    import sys
    if os.path.exists(os.path.join(OUT, 'geom_v3.json')):
        old = json.load(open(os.path.join(OUT, 'geom_v3.json')))
        old.update(geom)
        geom = old
    json.dump(geom, open(os.path.join(OUT, 'geom_v3.json'), 'w'))
    for v in ('side', 'front', 'below'):
        print(v, 'box', geom[v]['box'], {k: len(d) for k, d in geom[v]['parts'].items()})
