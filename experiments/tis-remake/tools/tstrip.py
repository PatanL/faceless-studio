"""Per-frame strips around transitions: python3 tstrip.py <f30_dir> <out_dir> t0:t1 [t0:t1 ...] (30 fps, frames f_0001 = t 0.000)"""
import sys, os
from PIL import Image, ImageDraw
src, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
for win in sys.argv[3:]:
    t0, t1 = map(float, win.split(":"))
    idx = list(range(int(round(t0 * 30)), int(round(t1 * 30)) + 1))
    ims = [Image.open(f"{src}/f_{i+1:04d}.jpg").convert("RGB") for i in idx]
    W, H = ims[0].size; cols = min(8, len(ims)); rows = (len(ims) + cols - 1) // cols
    s = Image.new("RGB", (cols * W, rows * H)); d = ImageDraw.Draw(s)
    for k, (i, im) in enumerate(zip(idx, ims)):
        x, y = (k % cols) * W, (k // cols) * H; s.paste(im, (x, y))
        d.rectangle([x, y, x + 50, y + 13], fill=(0, 0, 0)); d.text((x + 2, y + 1), f"{i/30:6.3f}", fill=(255, 255, 0))
    p = f"{out}/trans_{t0:05.2f}.jpg"; s.save(p, quality=80); print(p, s.size)
