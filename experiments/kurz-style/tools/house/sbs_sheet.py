"""Side-by-side judging sheet: one row per pair, OURS on the left (red frame), REFERENCE on the right.
usage: python3 -I sbs_sheet.py <out.jpg> "<label>|<ours.jpg>|<ref.jpg>[|<ref2.jpg>]" ...
Each cell is 960x540; a 9:16 frame is pillarboxed on ink-0 so both sides share one scale.
Labels go in a strip above each row (frame role, our timestamp, reference id).
"""
import sys
from PIL import Image, ImageDraw, ImageFont

CW, CH, STRIP, PAD = 960, 540, 34, 8
INK, RED, BONE = (1, 18, 26), (221, 37, 52), (244, 238, 225)
FONT = None
for f in ("DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
          "/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/Library/Fonts/Arial Bold.ttf"):
    try:
        FONT = ImageFont.truetype(f, 22); break
    except OSError:
        pass
FONT = FONT or ImageFont.load_default()

def cell(path):
    im = Image.open(path).convert("RGB"); w, h = im.size; s = min(CW / w, CH / h)
    im = im.resize((max(1, round(w * s)), max(1, round(h * s))), Image.LANCZOS)
    c = Image.new("RGB", (CW, CH), INK); c.paste(im, ((CW - im.width) // 2, (CH - im.height) // 2)); return c

out, rows = sys.argv[1], [r.split("|") for r in sys.argv[2:]]
ncol = max(len(r) - 1 for r in rows)
W = ncol * CW + (ncol + 1) * PAD; H = len(rows) * (CH + STRIP + PAD) + PAD
sheet = Image.new("RGB", (W, H), INK); dr = ImageDraw.Draw(sheet)
for i, r in enumerate(rows):
    y = PAD + i * (CH + STRIP + PAD)
    dr.text((PAD, y + 5), r[0], fill=BONE, font=FONT)
    for j, p in enumerate(r[1:]):
        x = PAD + j * (CW + PAD)
        sheet.paste(cell(p), (x, y + STRIP))
        tag = "OURS" if j == 0 else "REF " + p.rsplit("/", 1)[-1].rsplit(".", 1)[0]
        dr.text((x + CW - 12 - dr.textlength(tag, font=FONT), y + 5), tag, fill=RED if j == 0 else BONE, font=FONT)
        if j == 0:
            dr.rectangle((x - 3, y + STRIP - 3, x + CW + 2, y + STRIP + CH + 2), outline=RED, width=3)
sheet.save(out, quality=88)
print(out, sheet.size)
