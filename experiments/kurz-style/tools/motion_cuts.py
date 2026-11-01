"""Cut detection + ambient-motion stats. usage: motion_cuts.py <ffmpeg> <video> <out.json> [fps]
Decodes at fps (default 30) to 192x108 RGB. Per frame: mean abs diff vs previous (0-255).
Cut = diff > max(18, 4*median of +-15 neighbours) and colour-hist distance high.
Static frame = diff < 0.15 (nothing moves at all)."""
import sys, subprocess, json
import numpy as np
ff, vid, out = sys.argv[1], sys.argv[2], sys.argv[3]
fps = float(sys.argv[4]) if len(sys.argv) > 4 else 30.0
W, H = 192, 108
p = subprocess.Popen([ff, "-v", "error", "-threads", "2", "-i", vid, "-vf", f"fps={fps},scale={W}:{H}:flags=area", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
prev = None; prevh = None; diffs = []; hd = []
while True:
    b = p.stdout.read(W * H * 3)
    if len(b) < W * H * 3: break
    a = np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.int16)
    h = np.histogramdd(a.reshape(-1, 3) // 32, bins=(8, 8, 8), range=((0, 8),) * 3)[0].ravel() / (W * H)
    if prev is not None:
        diffs.append(float(np.abs(a - prev).mean())); hd.append(float(0.5 * np.abs(h - prevh).sum()))
    prev, prevh = a, h
d = np.array(diffs); hdd = np.array(hd)
cuts = []
for i in range(len(d)):
    lo, hi = max(0, i - 15), min(len(d), i + 16)
    nb = np.concatenate([d[lo:i], d[i + 1:hi]])
    med = np.median(nb) if len(nb) else 0
    if d[i] > max(14.0, 4 * med) and hdd[i] > 0.25:
        t = (i + 1) / fps
        if not cuts or t - cuts[-1] > 0.3: cuts.append(round(t, 3))
dur = (len(d) + 1) / fps
bounds = [0.0] + cuts + [dur]
shots = np.diff(bounds)
res = dict(fps=fps, duration=round(dur, 2), n_cuts=len(cuts), cuts=cuts,
    shot_len=dict(mean=round(float(shots.mean()), 2), median=round(float(np.median(shots)), 2),
                  p10=round(float(np.percentile(shots, 10)), 2), p90=round(float(np.percentile(shots, 90)), 2)),
    static_frac=round(float((d < 0.15).mean()), 4), lowmotion_frac=round(float((d < 0.5).mean()), 4),
    diff_pct=[round(float(x), 3) for x in np.percentile(d, [5, 25, 50, 75, 95])],
    diff_series=[round(x, 2) for x in d.tolist()], hist_series=[round(x, 3) for x in hdd.tolist()])
# longest static run
run = best = 0
for x in d:
    run = run + 1 if x < 0.15 else 0; best = max(best, run)
res["longest_static_s"] = round(best / fps, 2)
json.dump(res, open(out, "w"))
print(out, res["n_cuts"], res["shot_len"], res["static_frac"], res["lowmotion_frac"], res["diff_pct"], res["longest_static_s"])
