import sys, glob, os
from PIL import Image, ImageDraw
fs = sorted(glob.glob(sys.argv[1] + "/*.jpg")); cols = 5; W = 384; h = 216
sh = Image.new("RGB", (cols * W, ((len(fs) + cols - 1) // cols) * (h + 2)), (0, 0, 0)); d = ImageDraw.Draw(sh)
for i, f in enumerate(fs):
    x, y = (i % cols) * W, (i // cols) * (h + 2)
    sh.paste(Image.open(f).convert("RGB").resize((W, h)), (x, y))
    n = os.path.basename(f)[:-4]; d.rectangle([x, y, x + 7 * len(n) + 4, y + 13], fill=(0, 0, 0)); d.text((x + 2, y + 1), n, fill=(255, 255, 0))
sh.save(sys.argv[2], quality=80); print(sh.size)
