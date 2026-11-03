# REPLICATION STUDY: tile reference frames (top row) over our stills (bottom row) at the same frame numbers, 10% grid.
import subprocess, sys, os
import numpy as np
from PIL import Image, ImageDraw
ref, out, frames = sys.argv[1], sys.argv[2], [int(f) for f in sys.argv[3:]]
W, H = 216, 384
def grid(im):
    d = ImageDraw.Draw(im)
    for k in range(1, 10):
        d.line([(k * W / 10, 0), (k * W / 10, H)], fill=(255, 255, 0), width=1)
        d.line([(0, k * H / 10), (W, k * H / 10)], fill=(255, 255, 0), width=1)
    return im
n = max(frames) + 1
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", ref, "-frames:v", str(n), "-vf", f"scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
R = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
cols = 8
rows = (len(frames) + cols - 1) // cols
sheet = Image.new("RGB", (cols * W, rows * (2 * H + 16)), (20, 16, 30))
for i, f in enumerate(frames):
    x, y = (i % cols) * W, (i // cols) * (2 * H + 16)
    a = grid(Image.fromarray(R[f]).copy()); sheet.paste(a, (x, y + 16))
    p = os.path.join(out, "ours", f"f{f:05d}.png")
    if os.path.exists(p): sheet.paste(grid(Image.open(p).convert("RGB").resize((W, H))), (x, y + 16 + H))
    ImageDraw.Draw(sheet).text((x + 4, y + 2), f"F{f}", fill=(255, 255, 255))
sheet.save(os.path.join(out, "keys.jpg"), quality=88)
print(os.path.join(out, "keys.jpg"))
