"""Colour script for one video: movie barcode + setting-kind band + luminance curve, and per-setting colour stats.

usage: python3 -I colour_script.py <metrics.npz> <settings.csv> <out.jpg> --title "..." [--t0 S --t1 S] [--json out.json]

barcode: each column is the mean of the per-frame 9-band vertical colour profile over its time slice.
band:    the kind of each catalogued segment (world / board / analogy / stock / intro).
curve:   mean luma per column (0-255).
json:    per backdrop-hold mean colour (sRGB, CIELAB L*, chroma C*, hue h) and the CIEDE76 jump at each
         setting change versus inside a setting (frame 1 s before vs 1 s after random non-boundary points).
"""
import csv, json, argparse
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument("npz"); ap.add_argument("csv"); ap.add_argument("out")
ap.add_argument("--title", default=""); ap.add_argument("--t0", type=float, default=0.0)
ap.add_argument("--t1", type=float, default=0.0); ap.add_argument("--json", default="")
a = ap.parse_args()
z = np.load(a.npz); fps = float(z["fps"]); st = float(z["start"])
rows_prof = z["rows"].astype(np.float32); lum = z["lum"]; rgb = z["rgb"]
n = len(lum); T = st + np.arange(n) / fps
t1 = a.t1 or T[-1]
segs = [dict(r, start=float(r["start"]), end=float(r["end"])) for r in csv.DictReader(open(a.csv))]

def lab(c):
    c = np.asarray(c, np.float64) / 255.0
    c = np.where(c > 0.04045, ((c + 0.055) / 1.055) ** 2.4, c / 12.92)
    M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    xyz = c @ M.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    L = 116 * f[..., 1] - 16; A = 500 * (f[..., 0] - f[..., 1]); B = 200 * (f[..., 1] - f[..., 2])
    return np.stack([L, A, B], -1)

# ---- image
SURF = (26, 26, 25); TXT = (240, 239, 236); TXT2 = (195, 194, 183); GRID = (60, 60, 58)
KIND = {"world": (57, 135, 229), "board": (217, 89, 38), "analogy": (25, 158, 112), "stock": (201, 133, 0), "intro": (90, 90, 88)}
W, L0 = 1600, 64; PW = W - L0 - 16
H_BAR, H_BAND, H_CURVE = 110, 14, 90
y_bar = 34; y_band = y_bar + H_BAR + 4; y_curve = y_band + H_BAND + 14; y_axis = y_curve + H_CURVE + 4
img = Image.new("RGB", (W, y_axis + 44), SURF); d = ImageDraw.Draw(img)
def font(s):
    try: return ImageFont.load_default(size=s)
    except TypeError: return ImageFont.load_default()
d.text((L0, 8), a.title, fill=TXT, font=font(15))
x_of = lambda t: L0 + (t - a.t0) / (t1 - a.t0) * PW
colsL = []
for x in range(PW):
    ta = a.t0 + x / PW * (t1 - a.t0); tb = a.t0 + (x + 1) / PW * (t1 - a.t0)
    m = (T >= ta) & (T < tb)
    if not m.any(): m = np.abs(T - ta) == np.abs(T - ta).min()
    prof = rows_prof[m].mean(0)                      # (9, 3)
    col = np.repeat(prof, int(np.ceil(H_BAR / prof.shape[0])), 0)[:H_BAR]
    img.paste(Image.fromarray(np.clip(col, 0, 255).astype(np.uint8)[:, None, :].repeat(1, 1)), (L0 + x, y_bar))
    colsL.append(float(lum[m].mean()))
for s in segs:
    if s["end"] <= a.t0 or s["start"] >= t1: continue
    xa, xb = x_of(max(s["start"], a.t0)), x_of(min(s["end"], t1))
    d.rectangle([xa + 1, y_band, max(xa + 1, xb - 1), y_band + H_BAND], fill=KIND.get(s["kind"], (120, 120, 120)))
for v in (64, 128, 192):
    y = y_curve + H_CURVE - v / 255 * H_CURVE
    d.line([(L0, y), (L0 + PW, y)], fill=GRID, width=1); d.text((8, y - 6), str(v), fill=TXT2, font=font(10))
pts = [(L0 + x, y_curve + H_CURVE - v / 255 * H_CURVE) for x, v in enumerate(colsL)]
d.line(pts, fill=TXT2, width=2)
d.text((8, y_curve - 14), "mean luma (0-255)", fill=TXT2, font=font(10))
step = 60 if t1 - a.t0 > 180 else 30
t = np.ceil(a.t0 / step) * step
while t <= t1:
    x = x_of(t); d.line([(x, y_axis), (x, y_axis + 5)], fill=TXT2, width=1)
    d.text((x - 12, y_axis + 7), f"{int(t // 60)}:{int(t % 60):02d}", fill=TXT2, font=font(11)); t += step
lx = L0
for k in ("world", "board", "analogy", "stock"):
    if not any(s["kind"] == k for s in segs): continue
    d.rectangle([lx, y_axis + 26, lx + 12, y_axis + 36], fill=KIND[k]); d.text((lx + 16, y_axis + 24), k, fill=TXT, font=font(11))
    lx += 90
d.text((lx + 20, y_axis + 24), "band = setting kind per catalogue; barcode = 9-band vertical colour profile", fill=TXT2, font=font(11))
img.save(a.out, quality=88)

# ---- per-setting colour stats
def seg_rgb(s0, s1):
    m = (T >= s0) & (T < s1)
    return rgb[m].mean(0) if m.any() else None
merged = []
for s in segs:
    if s["kind"] == "intro" or s["end"] <= a.t0 or s["start"] >= t1: continue
    if merged and merged[-1]["setting"] == s["setting"]: merged[-1]["end"] = s["end"]
    else: merged.append(dict(s))
out = []
for s in merged:
    c = seg_rgb(s["start"], s["end"]); Lb = lab(c)
    out.append(dict(start=s["start"], end=s["end"], setting=s["setting"], kind=s["kind"], rgb=[int(v) for v in c],
                    L=round(float(Lb[0]), 1), C=round(float(np.hypot(Lb[1], Lb[2])), 1),
                    h=round(float(np.degrees(np.arctan2(Lb[2], Lb[1])) % 360), 0)))
jumps = []
for s in merged[1:]:
    b = s["start"]; p = seg_rgb(b - 1.0, b - 0.2); q = seg_rgb(b + 0.2, b + 1.0)
    if p is not None and q is not None: jumps.append(float(np.linalg.norm(lab(p) - lab(q))))
rng = np.random.default_rng(0); inside = []
for s in merged:
    for _ in range(3):
        if s["end"] - s["start"] < 3: continue
        b = rng.uniform(s["start"] + 1.2, s["end"] - 1.2)
        p = seg_rgb(b - 1.0, b - 0.2); q = seg_rgb(b + 0.2, b + 1.0)
        if p is not None and q is not None: inside.append(float(np.linalg.norm(lab(p) - lab(q))))
res = dict(dE_at_setting_change=dict(median=round(float(np.median(jumps)), 1), p25=round(float(np.percentile(jumps, 25)), 1)),
           dE_inside_setting=dict(median=round(float(np.median(inside)), 1), p75=round(float(np.percentile(inside, 75)), 1)),
           L_by_kind={k: round(float(np.median([o["L"] for o in out if o["kind"] == k])), 1) for k in {o["kind"] for o in out}},
           C_by_kind={k: round(float(np.median([o["C"] for o in out if o["kind"] == k])), 1) for k in {o["kind"] for o in out}},
           segments=out)
print(json.dumps({k: v for k, v in res.items() if k != "segments"}))
if a.json: json.dump(res, open(a.json, "w"), indent=1)
