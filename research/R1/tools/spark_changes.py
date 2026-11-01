"""Run on Spark (CPU). 4 fps 96x54 grayscale; mean-abs-diff between frames -> visual change events (cuts + big graphic pop-ins)."""
import os, sys, json, subprocess
os.environ["CUDA_VISIBLE_DEVICES"] = ""
import numpy as np
FF, src, out = sys.argv[1], sys.argv[2], sys.argv[3]
W, H, FPS = 96, 54, 4
p = subprocess.run([FF, "-loglevel", "error", "-threads", "2", "-i", src, "-vf", f"fps={FPS},scale={W}:{H},format=gray", "-f", "rawvideo", "-"], capture_output=True)
a = np.frombuffer(p.stdout, np.uint8).reshape(-1, H, W).astype(np.float32)
d = np.abs(np.diff(a, axis=0)).mean(axis=(1, 2))
# fraction of pixels that changed a lot (captures pop-ins on dark bg)
frac = (np.abs(np.diff(a, axis=0)) > 25).mean(axis=(1, 2))
dur = len(a) / FPS
res = {"duration": dur}
for th in (0.02, 0.05, 0.10, 0.25):
    ev = []
    for i, f in enumerate(frac):
        t = (i + 1) / FPS
        if f >= th and (not ev or t - ev[-1] > 0.75):
            ev.append(round(t, 2))
    res[f"events_frac{th}"] = len(ev)
    res[f"events_per_min_frac{th}"] = round(len(ev) / (dur / 60), 2)
    res[f"times_frac{th}"] = ev
# per 5s window: mean pixel change (motion/animation intensity)
win = int(5 * FPS)
res["motion_per_5s"] = [round(float(d[i:i + win].mean()), 2) for i in range(0, len(d), win)]
json.dump(res, open(out, "w"))
print(os.path.basename(src), {k: v for k, v in res.items() if k.startswith("events_per_min")}, "dur", dur)
