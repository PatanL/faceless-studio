"""Side-by-side sheet for the orca opening A/B. Row 1 = approved v3 (engine, judged 59/100), row 2 = detail pass,
both at the same beat timestamps; row 3 = Kurzgesagt reference stills (study only) matched to the beats.
Run with python3 -I.
usage: orca_sbs.py <out.jpg> <v3.mp4> <detail.mp4> <t1,t2,...> <ref1> [<ref2> ...]
"""
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

out, v3, det, ts, refs = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4].split(","), sys.argv[5:]
N = len(ts)
CW, CH, PAD, STRIP = 432, 768, 12, 46
INK, RED, BONE, TIDE = (1, 18, 26), (221, 37, 52), (244, 238, 225), (127, 228, 231)
FONT = SMALL = None
for f in ("/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/Library/Fonts/Arial Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
    try:
        FONT, SMALL = ImageFont.truetype(f, 26), ImageFont.truetype(f, 20)
        break
    except OSError:
        pass
FONT = FONT or ImageFont.load_default()
SMALL = SMALL or FONT
tmp = tempfile.mkdtemp()


def grab(video, t, tag):
    p = os.path.join(tmp, f"{tag}_{t}.png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", t, "-i", video, "-frames:v", "1", p], check=True)
    return Image.open(p).convert("RGB").resize((CW, CH), Image.LANCZOS)


W = N * CW + (N + 1) * PAD
RW = (W - (len(refs) + 1) * PAD) // len(refs)
RH = RW * 9 // 16
H = 3 * STRIP + 2 * CH + RH + 4 * PAD
sheet = Image.new("RGB", (W, H), INK)
dr = ImageDraw.Draw(sheet)
y = PAD
for label, video, col, tag in (
    ("v3: APPROVED OPENING (kurz-style engine, judged 59/100)", v3, BONE, "v3"),
    ("DETAIL PASS: same beats, same mix (procedural set + asset-gen path-B orca)", det, RED, "dp"),
):
    dr.text((PAD, y + 10), label, fill=col, font=FONT)
    y += STRIP
    for i, t in enumerate(ts):
        x = PAD + i * (CW + PAD)
        sheet.paste(grab(video, t, tag), (x, y))
        dr.text((x + 10, y + 10), f"{float(t):.1f} s", fill=TIDE, font=FONT)
        if tag == "dp":
            dr.rectangle((x - 3, y - 3, x + CW + 2, y + CH + 2), outline=RED, width=3)
    y += CH + PAD
dr.text((PAD, y + 10), "REFERENCE TIER: Kurzgesagt stills at matching beats (study only, never copied)", fill=BONE, font=FONT)
y += STRIP
for i, r in enumerate(refs):
    im = Image.open(r).convert("RGB")
    im = im.resize((RW, RW * im.height // im.width), Image.LANCZOS)
    x = PAD + i * (RW + PAD)
    cell = Image.new("RGB", (RW, RH), INK)
    cell.paste(im, (0, (RH - im.height) // 2))
    sheet.paste(cell, (x, y))
    dr.text((x + 10, y + RH - 30), os.path.basename(r).rsplit(".", 1)[0], fill=BONE, font=SMALL)
sheet.save(out, quality=90)
print(out, sheet.size)
