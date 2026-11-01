"""How often does the picture change? Compares consecutive 2 s grid frames.
usage: python -I gridchange.py <grid_dir> [spf=2]
d = mean |a-b| on 96x54 grey thumbnails (0..255).
  same      d < 6     (held or nearly held picture: only ambient motion)
  evolved   6..25     (same set, camera moved / elements added)
  new       >= 25     (different composition: new set, big zoom, text card)
Prints the share of each class, the mean seconds between "new" pictures and between
"evolved or new" changes, and the longest run of "same".
"""
import sys, glob, os
import numpy as np
from PIL import Image

d = sys.argv[1]; spf = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0
fs = sorted(glob.glob(os.path.join(d, "*.jpg")))
th = [np.asarray(Image.open(f).convert("L").resize((96, 54), Image.BILINEAR), dtype=np.float32) for f in fs]
D = np.array([np.abs(a - b).mean() for a, b in zip(th, th[1:])])
same, new = D < 6, D >= 25
evo = ~same & ~new
run = best = 0
for x in same:
    run = run + 1 if x else 0; best = max(best, run)
n = len(D)
print(f"pairs {n}: same {same.mean():.2f}  evolved {evo.mean():.2f}  new {new.mean():.2f}")
print(f"seconds per NEW picture {n*spf/max(1,new.sum()):.1f}; seconds per visible change (evolved|new) {n*spf/max(1,(~same).sum()):.1f}; longest hold {best*spf:.0f} s")
print("d p25/p50/p75:", np.round(np.percentile(D, [25, 50, 75]), 1))
