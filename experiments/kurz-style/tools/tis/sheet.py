"""Contact sheets with mm:ss labels.
usage: python -I sheet.py <grid_dir> <out_prefix> [step=1] [per_sheet=100] [sec_per_frame=2]
"""
import sys, glob, os
from PIL import Image, ImageDraw

d, pre = sys.argv[1], sys.argv[2]
step = int(sys.argv[3]) if len(sys.argv) > 3 else 1
per = int(sys.argv[4]) if len(sys.argv) > 4 else 100
spf = float(sys.argv[5]) if len(sys.argv) > 5 else 2.0
files = sorted(glob.glob(os.path.join(d, "*.jpg")))
idx = list(range(0, len(files), step))
cols, W = 10, 192
H = 108
for s in range(0, len(idx), per):
    chunk = idx[s:s + per]
    rows = (len(chunk) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * W, rows * H), (0, 0, 0))
    dr = ImageDraw.Draw(sheet)
    for k, i in enumerate(chunk):
        im = Image.open(files[i]).convert("RGB").resize((W, H))
        x, y = (k % cols) * W, (k // cols) * H
        sheet.paste(im, (x, y))
        t = i * spf
        lab = "%d:%02d" % (t // 60, t % 60) if t < 3600 else "%d:%02d:%02d" % (t // 3600, (t % 3600) // 60, t % 60)
        dr.rectangle([x, y, x + 8 + 7 * len(lab), y + 13], fill=(0, 0, 0))
        dr.text((x + 3, y + 1), lab, fill=(255, 255, 0))
    out = "%s_%02d.jpg" % (pre, s // per)
    sheet.save(out, quality=82)
    print(out, sheet.size)
