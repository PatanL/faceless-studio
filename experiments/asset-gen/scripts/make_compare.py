"""Build compare.jpg: source PNG vs Path A (vtracer) vs Path B (structured redraw) vs the current kit orca,
plus the reef through Path A, with per-panel metrics from the house tools.

usage: .venv/bin/python scripts/make_compare.py
"""
import importlib.util, json, os, sys
import cv2, numpy as np
from scipy import ndimage as ndi

G = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(G, '..', 'kurz-style', 'tools')
spec = importlib.util.spec_from_file_location('fm', os.path.join(TOOLS, 'tis', 'frame_metrics.py'))
fm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fm)
P = lambda *a: os.path.join(G, *a)
TMP = P('build', 'panels')
os.makedirs(TMP, exist_ok=True)


def specks(img):
    """KB particles.py, inlined: small bright specks 6-400 px brighter than the local background"""
    a = img[..., ::-1].astype(np.float32)
    L = a @ np.array([.2126, .7152, .0722], np.float32)
    bg = ndi.median_filter(L[::4, ::4], 15)
    bg = np.kron(bg, np.ones((4, 4)))[:L.shape[0], :L.shape[1]]
    m = (L - bg) > 12
    lab, n = ndi.label(m)
    sz = ndi.sum(m, lab, range(1, n + 1)) if n else np.array([])
    return int(((sz >= 6) & (sz <= 400)).sum())


def measure(name, img):
    f = os.path.join(TMP, name + '.png')
    cv2.imwrite(f, img)
    r = fm.metrics(f)
    return dict(edge_den=round(r['edge_den'], 4), outline=round(r['outline'], 3), specks=specks(img))


def fit(img, w, h, bg=(40, 40, 40)):
    s = min(w / img.shape[1], h / img.shape[0])
    im = cv2.resize(img, (int(img.shape[1] * s), int(img.shape[0] * s)), interpolation=cv2.INTER_AREA)
    out = np.full((h, w, 3), bg, np.uint8)
    y, x = (h - im.shape[0]) // 2, (w - im.shape[1]) // 2
    out[y:y + im.shape[0], x:x + im.shape[1]] = im
    return out


def label(img, lines, top=True):
    img = img.copy()
    y0 = 6 if top else img.shape[0] - 18 * len(lines) - 8
    cv2.rectangle(img, (0, y0 - 6), (img.shape[1], y0 + 18 * len(lines) + 2), (20, 18, 14), -1)
    for i, t in enumerate(lines):
        cv2.putText(img, t, (8, y0 + 13 + 18 * i), cv2.FONT_HERSHEY_SIMPLEX, 0.46, (225, 238, 244), 1, cv2.LINE_AA)
    return img


stats = json.load(open(P('vec', 'orca_stats.json')))
rstats = json.load(open(P('vec', 'reef_stats.json')))
geom = json.load(open(P('orca-b', 'orca_geom.json')))

kit_frame = cv2.imread(P('kit', 'kit_orca_v3_t2.2.png'))
kit_orca = kit_frame[650:1070, 90:960]
orca = {
    'source (Codex PNG)': cv2.imread(P('gen', 'a_orca_side_v2.png')),
    'A: vtracer medium': cv2.imread(P('vec', 'orca_medium.png')),
    'A: vtracer fine': cv2.imread(P('vec', 'orca_fine.png')),
    'B: structured redraw': cv2.imread(P('orca-b', 'out', 'hero.png')),
    'kit orca (orca_open_v3)': kit_orca,
}
notes = {
    'source (Codex PNG)': ['raster, 1536x1024', 'not animatable'],
    'A: vtracer medium': [f"{stats['medium']['paths']} paths, {stats['medium']['kb']} KB", f"PSNR {stats['medium']['psnr']} dB; flat colour blobs"],
    'A: vtracer fine': [f"{stats['fine']['paths']} paths, {stats['fine']['kb']} KB", f"PSNR {stats['fine']['psnr']} dB; no named parts"],
    'B: structured redraw': ['8 named parts + eye, 1 light vector', f"{len(geom['marks'])} surface marks (from ref)"],
    'kit orca (orca_open_v3)': ['engine Orca.tsx, frame t=2.2 s', '~40 marks, scene crop'],
}
PW, PH = 640, 427
row1, row2, metrics = [], [], {}
for k, im in orca.items():
    m = measure('orca_' + k.split(':')[0].split(' ')[0], fit(im, 1536, 1024, (86, 66, 4)))
    metrics[k] = m
    row1.append(label(label(fit(im, PW, PH), [k] + notes[k]), [f"edge {m['edge_den']}  outline {m['outline']}  specks {m['specks']}"], top=False))
    # 1:1-ish detail crop: head + flipper of each, at matching relative position
    h, w = im.shape[:2]
    crop = im[int(h * 0.36):int(h * 0.80), int(w * 0.58):int(w * 0.99)] if 'kit' not in k else im[int(h * 0.30):int(h * 0.95), int(w * 0.62):int(w * 0.99)]
    row2.append(fit(crop, PW, PH))
sep = lambda n, wd: np.full((n, wd, 3), 245, np.uint8)
r1 = np.hstack([np.hstack([p, np.full((PH, 6, 3), 245, np.uint8)]) for p in row1])
r2 = np.hstack([np.hstack([p, np.full((PH, 6, 3), 245, np.uint8)]) for p in row2])

# reef row: source, A medium, A fine, kit reef band (same 9:16 crop region)
reef_src = cv2.imread(P('gen', 'c_reef_9x16_v2.png'))
reef = {
    'reef source (Codex PNG)': (reef_src, ['raster 941x1672']),
    'reef A: vtracer coarse': (cv2.imread(P('vec', 'reef_coarse.png')), [f"{rstats['coarse']['paths']} paths, PSNR {rstats['coarse']['psnr']}"]),
    'reef A: vtracer medium': (cv2.imread(P('vec', 'reef_medium.png')), [f"{rstats['medium']['paths']} paths, {rstats['medium']['kb']} KB, PSNR {rstats['medium']['psnr']}"]),
    'reef A: vtracer fine': (cv2.imread(P('vec', 'reef_fine.png')), [f"{rstats['fine']['paths']} paths, {rstats['fine']['kb']} KB, PSNR {rstats['fine']['psnr']}"]),
    'kit reef (orca_open_v3 t=2.2)': (cv2.resize(kit_frame, (941, 1672)), ['engine Reef.tsx in scene']),
}
RH = 2 * PH + 6
RW = int(RH * 941 / 1672)
row3 = []
for k, (im, nt) in reef.items():
    m = measure('reef_' + k.split(':')[0].replace(' ', '_')[-12:] + str(len(row3)), cv2.resize(im, (1080, 1920)))
    metrics[k] = m
    row3.append(label(label(fit(im, RW, RH), [k] + nt), [f"edge {m['edge_den']} outl {m['outline']}", f"specks {m['specks']}"], top=False))
# B pose sheet next to the reefs, to show animation
poses = cv2.imread(P('orca-b', 'out', 'poses.png'))
light = cv2.imread(P('orca-b', 'out', 'light.png'))
side_w = r1.shape[1] - sum(p.shape[1] + 6 for p in row3)
pose_p = fit(poses, side_w, int(RH * 0.62))
light_p = fit(light, side_w, RH - pose_p.shape[0] - 6)
side = np.vstack([label(pose_p, ['B is rigged: same component, props only (swim, jaw, flipper, blink)']), sep(6, side_w),
                  label(light_p, ['B relights: move the key vector, every part re-shades'])])
r3 = np.hstack([np.hstack([p, np.full((RH, 6, 3), 245, np.uint8)]) for p in row3] + [side])
W = max(r1.shape[1], r3.shape[1])
padw = lambda r: np.hstack([r, np.full((r.shape[0], W - r.shape[1], 3), 245, np.uint8)]) if r.shape[1] < W else r
title = np.full((44, W, 3), 245, np.uint8)
cv2.putText(title, 'asset-gen: Codex image -> (A) vtracer auto-vectorize  vs  (B) structured layered redraw  vs  current kit   |   row 2 = detail crops',
            (12, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (30, 30, 30), 2, cv2.LINE_AA)
sheet = np.vstack([title, padw(r1), sep(6, W), padw(r2), sep(6, W), padw(r3)])
cv2.imwrite(P('compare.jpg'), sheet, [cv2.IMWRITE_JPEG_QUALITY, 88])
json.dump(metrics, open(P('compare_metrics.json'), 'w'), indent=1)
print(json.dumps(metrics, indent=1))
print('compare.jpg', sheet.shape)
