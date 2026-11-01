"""House-style palette check on frames (STYLE_BIBLE.md section 1, JUDGE_RUBRIC.md P-checks).
usage: python3 -I palette_check.py <palette.json> <img> [<img> ...] [--json out.json] [--tol 0.04]

Per frame it reports:
  conform   share of pixels whose OKLab colour lies within --tol of an ALLOWED colour:
            a token, a straight mix between adjacent steps of one ramp (gradients), a mix of any
            token toward any ink/dusk token (shadow, haze, fade to dark), or a mix of any token
            toward a light token amber-4/5, bone-2, tide-5 (highlight, key light, rim, glow core).
  vm_share  share of chromatic px (S>0.25, V>0.2) with HSV hue 240-330 (violet/magenta band)
  sat_chroma median HSV saturation of chromatic px
  near_white share of px with V>0.92 and S<0.15;  pure_white share with all channels >= 250
  black     share of px with V<0.05
  grey      share of px with S<0.20 and 0.20<V<=0.92 (desaturated mid-tones: the TIS look)
  hue_fam   30-degree hue bins holding >= 3 % of chromatic px (same as ../frame_stats.py)
"""
import sys, os, json
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from oklab import rgb_to_oklab, hex_to_rgb01

args = sys.argv[1:]
out_json, tol = None, 0.04
if "--json" in args:
    i = args.index("--json"); out_json = args[i + 1]; del args[i:i + 2]
if "--tol" in args:
    i = args.index("--tol"); tol = float(args[i + 1]); del args[i:i + 2]
pal = json.load(open(args[0]))["ramps"]
imgs = args[1:]

tok = {t["token"]: rgb_to_oklab(hex_to_rgb01(t["hex"])) for r in pal.values() for t in r}
segs = set()
for name, r in pal.items():
    for a, b in zip(r[:-1], r[1:]):
        segs.add((a["token"], b["token"]))
darks = [t["token"] for t in pal["ink"] + pal["dusk"]]
lights = ["amber-4", "amber-5", "bone-2", "tide-5"]
for t in tok:
    for d in darks + lights:
        if d != t:
            segs.add(tuple(sorted((t, d))))
A = np.array([tok[a] for a, b in segs]); B = np.array([tok[b] for a, b in segs])
D = B - A; DD = (D * D).sum(1) + 1e-12

def seg_dist(P):
    best = np.full(len(P), np.inf)
    for k in range(0, len(A), 64):
        a, d, dd = A[k:k + 64], D[k:k + 64], DD[k:k + 64]
        t = np.clip(((P[:, None, :] - a[None]) * d[None]).sum(2) / dd[None], 0, 1)
        q = a[None] + t[..., None] * d[None]
        best = np.minimum(best, np.sqrt(((P[:, None, :] - q) ** 2).sum(2)).min(1))
    return best

rows = []
for f in imgs:
    im = Image.open(f).convert("RGB")
    w, h = im.size; s = 320 / max(w, h)
    sm = np.asarray(im.resize((max(1, int(w * s)), max(1, int(h * s))), Image.BILINEAR)).reshape(-1, 3)
    rgb = sm.astype(np.float64) / 255
    dist = seg_dist(rgb_to_oklab(rgb))
    mx, mn = rgb.max(1), rgb.min(1); S = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-9), 0); V = mx
    r, g, b = rgb.T; d = np.maximum(mx - mn, 1e-9)
    H = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    ch = (S > 0.25) & (V > 0.2)
    hb = np.bincount((H[ch] // 30).astype(int) % 12, minlength=12) / max(1, ch.sum())
    row = dict(file=os.path.basename(f), conform=round(float((dist <= tol).mean()), 3),
               vm_share=round(float(hb[8:11].sum()), 3),
               sat_chroma=round(float(np.median(S[ch])) if ch.any() else 0, 2),
               near_white=round(float(((V > 0.92) & (S < 0.15)).mean()), 4),
               pure_white=round(float((sm.min(1) >= 250).mean()), 4),
               black=round(float((V < 0.05).mean()), 4),
               grey=round(float(((S < 0.20) & (V > 0.20) & (V <= 0.92)).mean()), 3),
               hue_fam=int((hb >= 0.03).sum()))
    rows.append(row)
    print("%-40s conform %.2f  vm %.2f  satC %.2f  grey %.3f  nearW %.3f  pureW %.4f  black %.3f  fam %d" % (
        row["file"][:40], row["conform"], row["vm_share"], row["sat_chroma"], row["grey"], row["near_white"],
        row["pure_white"], row["black"], row["hue_fam"]))
if rows:
    k = lambda key: float(np.median([r[key] for r in rows]))
    print("MEDIAN conform %.2f  vm %.2f  satC %.2f  grey %.3f  nearW %.3f  pureW %.4f  black %.3f  fam %.1f  (n=%d, tol %.3f)" % (
        k("conform"), k("vm_share"), k("sat_chroma"), k("grey"), k("near_white"), k("pure_white"), k("black"),
        k("hue_fam"), len(rows), tol))
if out_json:
    json.dump(rows, open(out_json, "w"), indent=0)
