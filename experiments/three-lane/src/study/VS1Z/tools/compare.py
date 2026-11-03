# REPLICATION STUDY: theirs vs ours, frame by frame. Writes side-by-side sheets (60 frames = 2 s per sheet, each cell
# theirs | ours at the same frame number) and per-shot numbers: structural match (blockwise SSIM on blurred luma, the
# caption band masked), colour distance (mean Lab dE of 8x8-block averages), motion-energy correlation and the lag
# (frames) that best aligns our motion curve with theirs.
# usage: python3 -I compare.py ref.webm ours.mp4 outdir tag [nFrames]
import subprocess, sys, os, json
import numpy as np
from PIL import Image, ImageDraw
ref, ours, outdir, tag = sys.argv[1:5]; N = int(sys.argv[5]) if len(sys.argv) > 5 else 600
W, H = 180, 320
def load(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-frames:v", str(N), "-vf", f"scale={W}:{H}:flags=area", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
A, B = load(ref), load(ours)
n = min(len(A), len(B), N)
SHOTS = [("1 hook take", 0, 92), ("2 warning, travel, laugh", 92, 224), ("3 jar orbit to frog", 224, 404), ("4 balcony crane", 404, 535), ("5 weeks later", 535, 600)]
# ---- sheets
os.makedirs(outdir, exist_ok=True)
cw, ch = 120, 213
for s in range((n + 59) // 60):
    sheet = Image.new("RGB", (6 * (2 * cw + 6), 10 * (ch + 14)), (18, 14, 28)); d = ImageDraw.Draw(sheet)
    for k in range(60):
        f = s * 60 + k
        if f >= n: break
        x, y = (k % 6) * (2 * cw + 6), (k // 6) * (ch + 14)
        sheet.paste(Image.fromarray(A[f]).resize((cw, ch)), (x, y + 14)); sheet.paste(Image.fromarray(B[f]).resize((cw, ch)), (x + cw, y + 14))
        d.text((x + 2, y + 1), f"F{f}  theirs | ours", fill=(230, 230, 230))
    sheet.save(os.path.join(outdir, f"{tag}_{s:02d}_F{s*60:04d}-F{s*60+59:04d}.jpg"), quality=85)
# ---- numbers
def blur(x):
    k = np.array([1, 4, 6, 4, 1], float); k /= k.sum()
    x = np.apply_along_axis(lambda r: np.convolve(r, k, "same"), 1, x)
    return np.apply_along_axis(lambda c: np.convolve(c, k, "same"), 0, x)
def luma(f): return (0.299 * f[..., 0] + 0.587 * f[..., 1] + 0.114 * f[..., 2]) / 255.0
mask = np.ones((H, W), bool); mask[int(0.64 * H):int(0.78 * H)] = False
def ssim(a, b, bs=10):
    vals = []
    for y in range(0, H - bs + 1, bs):
        for x in range(0, W - bs + 1, bs):
            if not mask[y:y + bs, x:x + bs].all(): continue
            p, q = a[y:y + bs, x:x + bs], b[y:y + bs, x:x + bs]
            mp, mq = p.mean(), q.mean(); vp, vq = p.var(), q.var(); cv = ((p - mp) * (q - mq)).mean()
            c1, c2 = 0.01 ** 2, 0.03 ** 2
            vals.append(((2 * mp * mq + c1) * (2 * cv + c2)) / ((mp * mp + mq * mq + c1) * (vp + vq + c2)))
    return float(np.mean(vals))
def lab(f):
    c = f[:H // 8 * 8, :W // 8 * 8].reshape(H // 8, 8, W // 8, 8, 3).mean(axis=(1, 3)) / 255.0
    c = np.where(c > 0.04045, ((c + 0.055) / 1.055) ** 2.4, c / 12.92)
    X = c @ np.array([[0.4124, 0.2126, 0.0193], [0.3576, 0.7152, 0.1192], [0.1805, 0.0722, 0.9505]])
    X = X / np.array([0.9505, 1.0, 1.089])
    fx = np.where(X > 0.008856, np.cbrt(X), 7.787 * X + 16 / 116)
    return np.stack([116 * fx[..., 1] - 16, 500 * (fx[..., 0] - fx[..., 1]), 200 * (fx[..., 1] - fx[..., 2])], -1)
per = []
LA = [blur(luma(A[f])) for f in range(n)]; LB = [blur(luma(B[f])) for f in range(n)]
for f in range(n):
    per.append({"f": f, "ssim": round(ssim(LA[f], LB[f]), 3), "dE": round(float(np.linalg.norm(lab(A[f]) - lab(B[f]), axis=-1).mean()), 1)})
mA = np.array([0.0] + [np.abs(LA[f] - LA[f - 1])[mask].mean() for f in range(1, n)])
mB = np.array([0.0] + [np.abs(LB[f] - LB[f - 1])[mask].mean() for f in range(1, n)])
out = []
for name, a, b in SHOTS:
    b = min(b, n)
    s = [p["ssim"] for p in per[a:b]]; e = [p["dE"] for p in per[a:b]]
    best, lag = -2, 0
    for L in range(-8, 9):
        x, y = mA[a + 1 + 8:b - 8], mB[a + 1 + 8 + L:b - 8 + L]
        if len(x) > 5 and x.std() > 0 and y.std() > 0:
            c = float(np.corrcoef(x, y)[0, 1])
            if c > best: best, lag = c, L
    out.append({"shot": name, "frames": [a, b - 1], "ssim": round(float(np.mean(s)), 3), "dE": round(float(np.mean(e)), 1),
                "motion_corr": round(best, 2), "motion_lag_f": lag, "motion_energy_ratio": round(float(mB[a + 1:b].mean() / max(1e-6, mA[a + 1:b].mean())), 2)})
json.dump({"tag": tag, "shots": out, "per_frame": per}, open(os.path.join(outdir, f"{tag}_numbers.json"), "w"), indent=1)
for o in out: print(o)
