"""Detail density on stills: how many distinct shapes and micro-details per frame.
usage: python -I density.py <img> [<img> ...]
On a 960x540 proxy, colours are quantised to 16 k-means clusters (Lab); each connected
region of one cluster is a "shape".
  shapes      regions >= 150 px (>= 0.03 % of frame; ~600 px at 1080p)
  micro       regions 4..149 px (stars, sparkles, dust, rivets, window glints, text strokes)
  big         regions >= 2 % of frame (backdrops, big masses)
Text-heavy frames inflate "micro" (each glyph counts); read alongside the frame.
"""
import sys, os
import numpy as np, cv2

cv2.setNumThreads(2)
print("%-22s %7s %7s %5s" % ("frame", "shapes", "micro", "big"))
for p in sys.argv[1:]:
    im = cv2.resize(cv2.imread(p), (960, 540), interpolation=cv2.INTER_AREA)
    im = cv2.bilateralFilter(im, 5, 20, 5)  # suppress JPEG/grain noise, keep edges
    lab = cv2.cvtColor(im, cv2.COLOR_BGR2LAB).reshape(-1, 3).astype(np.float32)
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    _, lbl, _ = cv2.kmeans(lab, 16, None, crit, 2, cv2.KMEANS_PP_CENTERS)
    lbl = lbl.reshape(540, 960)
    shapes = micro = big = 0
    for k in range(16):
        n, cc, stats, _ = cv2.connectedComponentsWithStats((lbl == k).astype(np.uint8), connectivity=8)
        a = stats[1:, cv2.CC_STAT_AREA]
        shapes += int((a >= 150).sum()); micro += int(((a >= 4) & (a < 150)).sum()); big += int((a >= 0.02 * 960 * 540).sum())
    print("%-22s %7d %7d %5d" % (os.path.basename(p), shapes, micro, big))
