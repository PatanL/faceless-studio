import sys, subprocess, numpy as np
from PIL import Image
# usage: offset_check.py video frames_dir idx(1-based) ; compares f2 frame with exact frames at 2*(idx-1)+d
v, d, idx = sys.argv[1], sys.argv[2], int(sys.argv[3])
ref = np.asarray(Image.open(f"{d}/t{idx:04d}.jpg").convert("L").resize((160, 90)), np.float32)
base = 2 * (idx - 1)
for dt in np.arange(-0.5, 3.01, 0.25):
    t = base + dt
    raw = subprocess.run([sys.argv[4], "-nostdin", "-loglevel", "error", "-ss", str(t), "-i", v, "-frames:v", "1", "-vf", "scale=160:90,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(90, 160).astype(np.float32)
    print(f"{dt:+.2f} {np.abs(a - ref).mean():.2f}")
