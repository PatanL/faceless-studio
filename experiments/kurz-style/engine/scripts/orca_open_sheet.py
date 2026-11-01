"""Side-by-side sheet for the orca-open rebuild: band 1 = current pipeline, band 2 = engine rebuild (same
timestamps), band 3 = three reference frames (Kurzgesagt tier target). Run with python3 -I.
usage: orca_open_sheet.py <out.jpg> <current.mp4> <rebuild.mp4> <t1,t2,t3> <ref1> <ref2> <ref3>
"""
import subprocess, sys, tempfile, os
from PIL import Image, ImageDraw, ImageFont

out, cur, reb, ts, refs = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4].split(","), sys.argv[5:8]
CW, CH, PAD, STRIP = 540, 960, 12, 46
INK, RED, BONE, TIDE = (1, 18, 26), (221, 37, 52), (244, 238, 225), (127, 228, 231)
FONT = None
for f in ("/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/Library/Fonts/Arial Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
    try:
        FONT = ImageFont.truetype(f, 28); break
    except OSError:
        pass
FONT = FONT or ImageFont.load_default()
tmp = tempfile.mkdtemp()

def grab(video, t, tag):
    p = os.path.join(tmp, f"{tag}_{t}.png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", t, "-i", video, "-frames:v", "1", p], check=True)
    return Image.open(p).convert("RGB").resize((CW, CH), Image.LANCZOS)

W = 3 * CW + 4 * PAD
RH = (W - 4 * PAD) // 3 * 9 // 16  # reference cells: 16:9 at the same column width
H = 3 * STRIP + 2 * CH + RH + 4 * PAD
sheet = Image.new("RGB", (W, H), INK); dr = ImageDraw.Draw(sheet)
y = PAD
for label, video, col in (("CURRENT PIPELINE (studio kit)", cur, BONE), ("REBUILD (kurz-style engine, Lantern & Ink)", reb, RED)):
    dr.text((PAD, y + 8), label, fill=col, font=FONT); y += STRIP
    for i, t in enumerate(ts):
        x = PAD + i * (CW + PAD)
        sheet.paste(grab(video, t, label[:3]), (x, y))
        dr.text((x + 10, y + 10), f"{float(t):.1f} s", fill=TIDE, font=FONT)
        if video is reb:
            dr.rectangle((x - 3, y - 3, x + CW + 2, y + CH + 2), outline=RED, width=3)
    y += CH + PAD
dr.text((PAD, y + 8), "REFERENCE TIER (Kurzgesagt stills, study only)", fill=BONE, font=FONT); y += STRIP
for i, r in enumerate(refs):
    im = Image.open(r).convert("RGB"); im = im.resize((CW, CW * im.height // im.width), Image.LANCZOS)
    x = PAD + i * (CW + PAD)
    cell = Image.new("RGB", (CW, RH), INK); cell.paste(im, (0, (RH - im.height) // 2)); sheet.paste(cell, (x, y))
    dr.text((x + 10, y + RH - 38), os.path.basename(r).rsplit(".", 1)[0], fill=BONE, font=FONT)
sheet.save(out, quality=90)
print(out, sheet.size)
