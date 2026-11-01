"""Contact sheets from 0.25 s frames: python3 sheet.py <frames_dir> <out_dir> [per_sheet=32] [cols=8] [cell_w=180]"""
import sys, glob, os
from PIL import Image, ImageDraw
src, out = sys.argv[1], sys.argv[2]
per = int(sys.argv[3]) if len(sys.argv) > 3 else 32
cols = int(sys.argv[4]) if len(sys.argv) > 4 else 8
W = int(sys.argv[5]) if len(sys.argv) > 5 else 180
fr = sorted(glob.glob(src + "/f_*.jpg"))
os.makedirs(out, exist_ok=True)
for si in range(0, len(fr), per):
    chunk = fr[si:si + per]
    ims = [Image.open(f).convert("RGB") for f in chunk]
    h = int(ims[0].height * W / ims[0].width)
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * W, rows * h), (0, 0, 0))
    d = ImageDraw.Draw(sheet)
    for i, im in enumerate(ims):
        t = (si + i) * 0.25
        x, y = (i % cols) * W, (i // cols) * h
        sheet.paste(im.resize((W, h)), (x, y))
        d.rectangle([x, y, x + 52, y + 14], fill=(0, 0, 0))
        d.text((x + 2, y + 1), f"{t:5.2f}s", fill=(255, 255, 0))
    p = f"{out}/sheet_{si*0.25:05.1f}-{(si+len(chunk)-1)*0.25:05.1f}.jpg"
    sheet.save(p, quality=80); print(p, sheet.size)
