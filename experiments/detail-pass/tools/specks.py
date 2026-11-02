"""Per-frame D3 small-speck count, exactly the judge_summary.py / frame_judge.sh counter (kurz-bio particles.py
cv2 port): components 6-400 px that are > 12 luma above a 1/4-res median-15 background, on the frame resized to
1920x1080 like the reference measurements.  usage: python -I specks.py <grid_dir>  -> JSON {frame: count, median}"""
import sys, os, glob, json
import numpy as np, cv2
cv2.setNumThreads(2)
res = {}
for f in sorted(glob.glob(os.path.join(sys.argv[1], "*.jpg"))):
    a = cv2.imread(f).astype(np.float32); L = a @ np.array([.0722, .7152, .2126], np.float32)
    L = cv2.resize(L, (1920, 1080), interpolation=cv2.INTER_AREA) if L.shape[1] != 1920 else L
    small = cv2.resize(L, (L.shape[1] // 4, L.shape[0] // 4), interpolation=cv2.INTER_AREA)
    bg = cv2.resize(cv2.medianBlur(np.clip(small, 0, 255).astype(np.uint8), 15).astype(np.float32), (L.shape[1], L.shape[0]))
    n, lab, st, _ = cv2.connectedComponentsWithStats(((L - bg) > 12).astype(np.uint8), connectivity=8)
    ar = st[1:, cv2.CC_STAT_AREA]
    res[os.path.basename(f)] = int(((ar >= 6) & (ar <= 400)).sum())
v = list(res.values())
print(json.dumps({"per_frame": res, "median": float(np.median(v)) if v else 0, "min": min(v) if v else 0, "max": max(v) if v else 0}))
