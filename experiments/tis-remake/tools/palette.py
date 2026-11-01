"""Dominant colours per still or region: python3 palette.py img.png [x0,y0,x1,y1] [n=12]"""
import sys
from PIL import Image
im = Image.open(sys.argv[1]).convert("RGB")
if len(sys.argv) > 2 and sys.argv[2] != "-":
    im = im.crop(tuple(int(v) for v in sys.argv[2].split(",")))
n = int(sys.argv[3]) if len(sys.argv) > 3 else 12
q = im.quantize(colors=n, method=Image.Quantize.MEDIANCUT)
pal = q.getpalette(); cnt = sorted(q.getcolors(), reverse=True); tot = sum(c for c, _ in cnt)
print(sys.argv[1].split("/")[-1], sys.argv[2] if len(sys.argv) > 2 else "", " ".join(
    f"#{pal[3*i]:02X}{pal[3*i+1]:02X}{pal[3*i+2]:02X}:{100*c/tot:.0f}%" for c, i in cnt if c / tot >= 0.015))
