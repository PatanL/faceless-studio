"""Camera + ambient-motion curves from a full-frame-rate PNG sequence (640 px wide).
usage: python -I motion.py <full_dir> <fps> <out.csv>

Per consecutive frame pair:
  s        global scale factor (similarity fit, ORB + RANSAC); >1 = push-in
  rot      rotation, degrees
  tx, ty   translation in 1080p pixels
  inl      RANSAC inlier ratio
  diff     mean |frame_i - frame_{i-1}| (0..255) before compensation
  resid    fraction of pixels still differing > 10 after warping by the global fit
           (= local/ambient animation that is not camera motion)
  cut      1 when diff > 40 or inliers < 0.2 (treated as a hard cut)
Then a summary: per shot (between cuts) cumulative zoom %/s, pan px/s, and an easing
signature: velocity in the first/last 20 % of the shot vs the middle 60 %
(~1.0 = linear drift, < 0.5 = ease-in-out).
"""
import sys, glob, os, csv
import numpy as np, cv2

d, fps, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
files = sorted(glob.glob(os.path.join(d, "*.png")))
orb = cv2.ORB_create(1500)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
rows = []
prev = cv2.imread(files[0], cv2.IMREAD_GRAYSCALE)
k = 1080 / prev.shape[0]
kp0, de0 = orb.detectAndCompute(prev, None)
for i, f in enumerate(files[1:], 1):
    cur = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
    kp1, de1 = orb.detectAndCompute(cur, None)
    s, rot, tx, ty, inl = 1.0, 0.0, 0.0, 0.0, 0.0
    diff = float(np.abs(cur.astype(np.int16) - prev.astype(np.int16)).mean())
    resid = 1.0
    if de0 is not None and de1 is not None and len(kp0) > 10 and len(kp1) > 10:
        m = bf.match(de0, de1)
        if len(m) > 10:
            p0 = np.float32([kp0[x.queryIdx].pt for x in m])
            p1 = np.float32([kp1[x.trainIdx].pt for x in m])
            M, mask = cv2.estimateAffinePartial2D(p0, p1, method=cv2.RANSAC, ransacReprojThreshold=2.0)
            if M is not None:
                inl = float(mask.mean())
                s = float(np.hypot(M[0, 0], M[1, 0]))
                rot = float(np.degrees(np.arctan2(M[1, 0], M[0, 0])))
                # translation of the frame centre
                c = np.array([cur.shape[1] / 2, cur.shape[0] / 2, 1.0])
                mc = M @ c
                tx, ty = float((mc[0] - c[0]) * k), float((mc[1] - c[1]) * k)
                w = cv2.warpAffine(prev, M, (cur.shape[1], cur.shape[0]), borderMode=cv2.BORDER_REPLICATE)
                resid = float((np.abs(cur.astype(np.int16) - w.astype(np.int16)) > 10).mean())
    cut = int(diff > 40 or inl < 0.2)
    rows.append(dict(i=i, t=round(i / fps, 3), s=round(s, 5), rot=round(rot, 3), tx=round(tx, 2), ty=round(ty, 2),
                     inl=round(inl, 2), diff=round(diff, 2), resid=round(resid, 4), cut=cut))
    prev, kp0, de0 = cur, kp1, de1

with open(out, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

# shot summaries
shots, curr = [], []
for r in rows:
    if r["cut"]:
        if curr: shots.append(curr)
        curr = []
    else:
        curr.append(r)
if curr: shots.append(curr)
for sh in shots:
    if len(sh) < 8:
        continue
    n = len(sh); dur = n / fps
    logs = np.log([r["s"] for r in sh]); tx = np.array([r["tx"] for r in sh]); ty = np.array([r["ty"] for r in sh])
    zoom = (np.exp(logs.sum()) - 1) * 100
    v = np.abs(logs) * 1e3 + np.hypot(tx, ty)  # combined speed proxy
    a, b = int(n * 0.2), int(n * 0.8)
    mid = v[a:b].mean() + 1e-6
    ease = (v[:a].mean() + v[b:].mean()) / 2 / mid if a > 0 else float("nan")
    print("shot t=%.2f-%.2fs  zoom %+.2f%% (%.2f%%/s)  pan %.0f,%.0f px (%.1f px/s)  rot %.2f deg  ease %.2f  ambient resid %.3f" % (
        sh[0]["t"], sh[-1]["t"], zoom, zoom / dur, tx.sum(), ty.sum(), np.hypot(tx.sum(), ty.sum()) / dur,
        sum(r["rot"] for r in sh), ease, np.median([r["resid"] for r in sh])))
print("cuts at", [r["t"] for r in rows if r["cut"]])
