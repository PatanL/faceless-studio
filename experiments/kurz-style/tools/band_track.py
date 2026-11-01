"""Per-band (optional 7th arg: frame step) horizontal/vertical motion via phase correlation at native fps.
usage: band_track.py <ffmpeg> <video> <start> <dur> <out.json> <bands as y0:y1,y0:y1 fractions>"""
import sys, subprocess, json
import numpy as np
ff, vid, ss, du, out, bands = sys.argv[1:7]
STEP = int(sys.argv[7]) if len(sys.argv) > 7 else 1
W, H = 960, 540
p = subprocess.Popen([ff, "-v", "error", "-ss", ss, "-i", vid, "-t", du, "-vf", f"scale={W}:{H}:flags=area,format=gray", "-f", "rawvideo", "-pix_fmt", "gray", "-"], stdout=subprocess.PIPE)
fr = []
while True:
    b = p.stdout.read(W * H)
    if len(b) < W * H: break
    fr.append(np.frombuffer(b, np.uint8).reshape(H, W).astype(np.float32))
bl = [tuple(float(v) for v in s.split(":")) for s in bands.split(",")]
win = np.hanning(W)[None, :]
def shift(a, b):
    a = (a - a.mean()) * win; b = (b - b.mean()) * win
    hA = np.hanning(a.shape[0])[:, None]; a = a * hA; b = b * hA
    F = np.fft.fft2(a) * np.conj(np.fft.fft2(b)); F /= np.abs(F) + 1e-9
    c = np.fft.ifft2(F).real; y, x = np.unravel_index(c.argmax(), c.shape)
    if y > c.shape[0] // 2: y -= c.shape[0]
    if x > c.shape[1] // 2: x -= c.shape[1]
    return float(x), float(y), float(c.max())
res = {"fps": 60, "step": STEP, "start": float(ss), "W": W, "bands": bands, "dx": [], "dy": [], "peak": []}
for (y0, y1) in bl:
    r0, r1 = int(y0 * H), int(y1 * H); dxs, dys, pk = [], [], []
    for i in range(STEP, len(fr), STEP):
        x, y, c = shift(fr[i][r0:r1], fr[i - STEP][r0:r1]); dxs.append(x); dys.append(y); pk.append(round(c, 3))
    res["dx"].append(dxs); res["dy"].append(dys); res["peak"].append(pk)
json.dump(res, open(out, "w"))
for j, b in enumerate(bl):
    dx = np.array(res["dx"][j]); print(b, "total dx(px@960)=", dx.sum(), "mean/frame", round(dx.mean(), 3))
