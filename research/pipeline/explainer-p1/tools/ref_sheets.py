"""Contact sheets for one reference video at its native frame grid, any aspect ratio (portrait Shorts included).

usage: python -I ref_sheets.py <ffmpeg> <video> <events.json> <out_prefix>
           [--t0 S] [--t1 S] [--step 0.5 | --every N] [--cols 10] [--rows 6] [--tw 150] [--threads 4]

  --step S   one tile every S seconds (snapped to the native frame grid), marker bar on the tile after each event
  --every N  one tile every N native frames (N=1: every frame, for hook / transition read-throughs)
Markers (left bar): red = hard cut since the previous tile, yellow = gradual transition ended, cyan = composition event.
events.json is frame_metrics.py output (fps, cuts, transitions[{start,end}], comp_events[{t}]).
Labels: m:ss.ss and the native frame index. Sheets are <= cols*(tw+2) px wide.
"""
import argparse
import json
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def font(sz):
    try:
        return ImageFont.load_default(size=sz)
    except TypeError:
        return ImageFont.load_default()


def mmss(t):
    return f"{int(t // 60)}:{t % 60:05.2f}"


ap = argparse.ArgumentParser()
ap.add_argument("ffmpeg"); ap.add_argument("video"); ap.add_argument("events"); ap.add_argument("out")
ap.add_argument("--t0", type=float, default=0.0); ap.add_argument("--t1", type=float, default=0.0)
ap.add_argument("--step", type=float, default=0.5); ap.add_argument("--every", type=int, default=0)
ap.add_argument("--cols", type=int, default=10); ap.add_argument("--rows", type=int, default=6)
ap.add_argument("--tw", type=int, default=150); ap.add_argument("--threads", type=int, default=4)
a = ap.parse_args()

ev = json.load(open(a.events)); fps = float(ev["fps"]); n_all = int(ev["n_frames"])
t1 = a.t1 or ev["duration"]
i0, i1 = int(round(a.t0 * fps)), min(n_all, int(round(t1 * fps)))
stride = a.every if a.every > 0 else max(1, int(round(a.step * fps)))
want = list(range(i0, i1, stride))
probe = subprocess.run([a.ffmpeg.replace("ffmpeg", "ffprobe"), "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "stream=width,height", "-of", "csv=p=0", a.video],
                       capture_output=True, text=True).stdout.strip().split(",")
W0, H0 = int(probe[0]), int(probe[1])
tw = a.tw; th = int(round(tw * H0 / W0 / 2) * 2)
cmd = [a.ffmpeg, "-v", "error", "-threads", str(a.threads), "-ss", f"{i0 / fps:.4f}", "-i", a.video,
       "-t", f"{(i1 - i0) / fps + 0.1:.4f}", "-fps_mode", "passthrough", "-vf", f"scale={tw}:{th}:flags=area",
       "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
fsz = tw * th * 3
frames = {}
wset = set(want); k = i0
while True:
    buf = p.stdout.read(fsz)
    if len(buf) < fsz:
        break
    if k in wset:
        frames[k] = np.frombuffer(buf, np.uint8).reshape(th, tw, 3).copy()
    k += 1
    if k >= i1:
        break
p.stdout.close(); p.wait()

cuts = ev["cuts"]; trs = [x["end"] for x in ev["transitions"]]; comps = [x["t"] for x in ev["comp_events"]]
tiles = []
prev = None
for i in want:
    if i not in frames:
        continue
    t = i / fps; lo = (prev / fps) if prev is not None else t - stride / fps
    bar = (230, 40, 40) if any(lo < c <= t + 1e-6 for c in cuts) else \
          (240, 200, 30) if any(lo < c <= t + 1e-6 for c in trs) else \
          (40, 210, 230) if any(lo < c <= t + 1e-6 for c in comps) else None
    im = Image.fromarray(frames[i]); out = Image.new("RGB", (tw, th + 14), (18, 18, 18)); out.paste(im, (0, 0))
    dr = ImageDraw.Draw(out); dr.text((3, th + 1), f"{mmss(t)} f{i}", fill=(235, 235, 235), font=font(11))
    if bar:
        dr.rectangle([0, 0, 4, th], fill=bar)
    tiles.append(out); prev = i

per = a.cols * a.rows
for s in range(0, len(tiles), per):
    chunk = tiles[s:s + per]; w, h = chunk[0].size
    sheet = Image.new("RGB", (a.cols * (w + 2), ((len(chunk) - 1) // a.cols + 1) * (h + 2)), (0, 0, 0))
    for n, im in enumerate(chunk):
        sheet.paste(im, ((n % a.cols) * (w + 2), (n // a.cols) * (h + 2)))
    t_first = want[s] / fps
    path = f"{a.out}_{s // per:02d}_{mmss(t_first).replace(':', 'm')}.jpg"
    sheet.save(path, quality=80); print(path)
