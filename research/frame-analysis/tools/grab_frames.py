"""Save the frames a human needs to review, in one sequential decode.

usage: python -I grab_frames.py <ffmpeg> <video> <events.json> <out_dir> [--step 0.5] [--size 320x180] [--threads 6]
         [--times t1,t2,...]   extra timestamps (s) to save at --size
Saves f_<frameindex>.jpg for: every --step seconds; the frame before and after every hard cut;
the first and last frame of every gradual transition; the frames 1 s apart around each composition event.
Frame index = round(t * fps) on the source's native frame grid.
"""
import sys, subprocess, json, argparse, os
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("ffmpeg"); ap.add_argument("video"); ap.add_argument("events"); ap.add_argument("out")
ap.add_argument("--step", type=float, default=0.5); ap.add_argument("--size", default="320x180")
ap.add_argument("--threads", type=int, default=6); ap.add_argument("--times", default="")
a = ap.parse_args()
ev = json.load(open(a.events)); fps = ev["fps"]; n = ev["n_frames"]; st = ev.get("start", 0.0)
W, H = map(int, a.size.split("x"))
idx = lambda t: int(round((t - st) * fps))
want = set(range(0, n, max(1, int(round(a.step * fps)))))
for t in ev["cuts"]:
    i = idx(t); want.update([i - 1, i])
for tr in ev["transitions"]:
    want.update([idx(tr["start"]), idx(tr["end"])])
for c in ev["comp_events"]:
    i = idx(c["t"]); want.update([i - int(round(fps)), i])
for t in [float(x) for x in a.times.split(",") if x]:
    want.add(idx(t))
want = {i for i in want if 0 <= i < n}
os.makedirs(a.out, exist_ok=True)
cmd = [a.ffmpeg, "-v", "error", "-threads", str(a.threads)]
if st: cmd += ["-ss", str(st)]
cmd += ["-i", a.video, "-map", "0:v:0", "-fps_mode", "passthrough", "-vf", f"scale={W}:{H}:flags=area",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
FB = W * H * 3; i = 0; saved = 0; last = max(want)
while i <= last:
    b = p.stdout.read(FB)
    if len(b) < FB: break
    if i in want:
        Image.frombuffer("RGB", (W, H), b).save(f"{a.out}/f_{i:06d}.jpg", quality=88); saved += 1
    i += 1
p.kill()
print(a.out, "saved", saved)
