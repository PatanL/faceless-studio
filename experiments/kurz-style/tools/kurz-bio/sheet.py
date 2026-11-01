import sys, glob, os
from PIL import Image, ImageDraw
# usage: sheet.py framesdir outprefix step_seconds offset_seconds cols width per_sheet
d, outp, step, off = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
cols, W, per = int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7])
fr = sorted(glob.glob(d + "/*.jpg"))
for s in range(0, len(fr), per):
    chunk = fr[s:s+per]
    ims = [Image.open(f).convert("RGB") for f in chunk]
    h = int(ims[0].height * W / ims[0].width)
    rows = (len(ims) + cols - 1) // cols
    sh = Image.new("RGB", (cols * W, rows * (h + 2)), (0, 0, 0)); dr = ImageDraw.Draw(sh)
    for i, im in enumerate(ims):
        k = s + i
        t = off + k * step
        x, y = (i % cols) * W, (i // cols) * (h + 2)
        sh.paste(im.resize((W, h)), (x, y))
        lab = "%d:%05.2f" % (t // 60, t % 60)
        dr.rectangle([x, y, x + 58, y + 13], fill=(0, 0, 0)); dr.text((x + 2, y + 1), lab, fill=(255, 255, 0))
    out = "%s_%02d.jpg" % (outp, s // per)
    sh.save(out, quality=82); print(out, sh.size)
