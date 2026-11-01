"""Contact sheet: sheet.py <frame_dir> <out_prefix> <step_seconds> [cols] [per_sheet] [thumb_w]
Frames named %04d.jpg starting at 1, frame n is at (n-1)*step seconds (ffmpeg fps filter)."""
import sys, glob, os
from PIL import Image, ImageDraw, ImageFont
d, outp, step = sys.argv[1], sys.argv[2], float(sys.argv[3])
cols = int(sys.argv[4]) if len(sys.argv) > 4 else 8
per = int(sys.argv[5]) if len(sys.argv) > 5 else 64
W = int(sys.argv[6]) if len(sys.argv) > 6 else 240
off = float(sys.argv[7]) if len(sys.argv) > 7 else 0.0
fr = sorted(glob.glob(os.path.join(d, "*.jpg")))
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
for s in range(0, len(fr), per):
    chunk = fr[s:s+per]
    im0 = Image.open(chunk[0]); h = int(im0.height * W / im0.width)
    rows = (len(chunk) + cols - 1) // cols
    sheet = Image.new("RGB", (cols*W, rows*h), (0, 0, 0)); dr = ImageDraw.Draw(sheet)
    for i, f in enumerate(chunk):
        n = int(os.path.basename(f)[:-4]); t = off + (n-1)*step
        x, y = (i % cols)*W, (i//cols)*h
        sheet.paste(Image.open(f).convert("RGB").resize((W, h), Image.LANCZOS), (x, y))
        lab = f"{int(t//60)}:{t%60:05.2f}"
        dr.rectangle([x, y, x+70, y+17], fill=(0, 0, 0)); dr.text((x+3, y+1), lab, fill=(255, 230, 0), font=font)
    sheet.save(f"{outp}_{s//per+1:02d}.jpg", quality=82)
    print(f"{outp}_{s//per+1:02d}.jpg", sheet.size)
