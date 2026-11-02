"""Calm-field share of rendered frames: fraction of 40x40 px tiles (native resolution) with no Canny edge
(60/140, same thresholds as tis/frame_metrics.py) after removing specks (components <= 400 px). Calm = flat
field or a smooth gradient; KB median top-cluster share 33-41 %, bible §8 target 30-50 %.
usage: python -I calm.py <grid_dir>  -> JSON"""
import sys, os, glob, json
import numpy as np, cv2
cv2.setNumThreads(2)
res = {}
for f in sorted(glob.glob(os.path.join(sys.argv[1], "*.jpg"))):
    g = cv2.cvtColor(cv2.imread(f), cv2.COLOR_BGR2GRAY)
    e = cv2.Canny(cv2.GaussianBlur(g, (0, 0), 1.0), 60, 140)
    n, lab, st, _ = cv2.connectedComponentsWithStats((e > 0).astype(np.uint8), connectivity=8)
    small = np.isin(lab, np.where(st[:, cv2.CC_STAT_AREA] <= 60)[0]) & (lab > 0)
    e2 = (e > 0) & ~small
    h, w = g.shape; T = 40; calm = tot = 0
    for y in range(0, h - T + 1, T):
        for x in range(0, w - T + 1, T):
            tot += 1; calm += int(e2[y:y + T, x:x + T].sum() == 0)
    res[os.path.basename(f)] = round(calm / tot, 3)
v = list(res.values())
print(json.dumps({"per_frame": res, "median": float(np.median(v)) if v else 0}))
