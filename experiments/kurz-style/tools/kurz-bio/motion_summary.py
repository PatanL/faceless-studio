"""usage: motion_summary.py motion.npz label -> cuts, shot lengths, static %, camera drift, ease profiles"""
import sys, json, numpy as np
z = np.load(sys.argv[1]); fps = float(z["fps"]); mad = z["mad"]; chg = z["chg"]; dx = z["dx"]; dy = z["dy"]; pk = z["pk"]; hist = z["hist"].astype(np.float32)
n = len(mad); t = np.arange(n) / fps
h = hist / hist.sum(1, keepdims=True)
hd = np.r_[0, 0.5 * np.abs(h[1:] - h[:-1]).sum(1)]  # histogram L1/2 distance 0..1
# cut: single-frame spike in mad AND histogram change, relative to local context
cuts = []
for i in range(2, n - 2):
    loc = np.r_[mad[max(1, i - 8):i - 1], mad[i + 2:i + 9]]
    base = np.median(loc) if len(loc) else 0
    if mad[i] > 10 and mad[i] > 4 * base + 3 and hd[i] > 0.12:
        if not cuts or i - cuts[-1] > fps * 0.3: cuts.append(i)
ct = t[cuts]
shots = np.diff(np.r_[0, ct, t[-1]])
# visual-change events: big frame change from cuts OR fast transitions (sum of mad over 0.5s window > thr)
static = mad < 0.25
runs = []; cur = 0
for s in static:
    cur = cur + 1 if s else (runs.append(cur) or 0)
runs.append(cur); runs = np.array(runs) / fps
spd = np.hypot(dx, dy) * fps * (1920 / 256)  # px/s in 1080p space
good = pk > 0.08
pan = good & (spd > 3) & (chg > 0.02)
# camera-move segments: contiguous frames with consistent dir
segs = []; i = 0
while i < n:
    if pan[i]:
        j = i
        while j < n and pan[j]: j += 1
        if (j - i) / fps >= 0.8: segs.append((i, j))
        i = j
    else: i += 1
prof = []
for a, b in segs:
    v = spd[a:b]; L = len(v)
    if L < 8: continue
    vm = v.max(); k10 = np.argmax(v >= 0.1 * vm); k90 = np.argmax(v >= 0.9 * vm)
    r90 = L - 1 - np.argmax(v[::-1] >= 0.9 * vm); r10 = L - 1 - np.argmax(v[::-1] >= 0.1 * vm)
    prof.append(dict(t0=round(a / fps, 2), dur=round(L / fps, 2), peak_px_s=round(float(vm), 1), mean_px_s=round(float(v.mean()), 1),
                     ease_in_s=round((k90 - k10) / fps, 2), ease_out_s=round((r10 - r90) / fps, 2),
                     dir_deg=round(float(np.degrees(np.arctan2(np.median(dy[a:b]), np.median(dx[a:b])))), 0)))
res = dict(label=sys.argv[2], n_frames=n, fps=fps, duration=round(n / fps, 1), n_cuts=len(cuts), cut_times=[round(float(x), 2) for x in ct],
    shot_len_s_p10_50_90=[round(float(x), 2) for x in np.percentile(shots, [10, 50, 90])], shot_len_mean=round(float(shots.mean()), 2),
    pct_static_frames=round(float(static.mean() * 100), 2), longest_static_s=round(float(runs.max()), 2), static_runs_over_1s=int((runs > 1).sum()),
    mad_p10_50_90=[round(float(x), 2) for x in np.percentile(mad[1:], [10, 50, 90])],
    pct_frames_changed_pixels_gt1pct=round(float((chg > 0.01).mean() * 100), 1),
    pct_frames_global_pan=round(float(pan.mean() * 100), 1), pan_speed_px_s_p50_90=[round(float(x), 1) for x in np.percentile(spd[pan], [50, 90])] if pan.any() else None,
    n_pan_segments=len(segs), pan_profiles=prof[:400])
# visual change events per 10 s (big change: hd>0.08 sustained over 0.5s window)
w = int(fps * 0.5); cs = np.convolve(hd, np.ones(w), "same")
ev = []
for i in range(n):
    if cs[i] > 0.25 and (not ev or i - ev[-1] > fps * 1.0): ev.append(i)
res["n_big_visual_changes"] = len(ev); res["big_change_interval_s_median"] = round(float(np.median(np.diff(np.array(ev) / fps))), 2) if len(ev) > 2 else None
res["big_change_times"] = [round(float(x / fps), 1) for x in ev]
json.dump(res, open(sys.argv[1].replace(".npz", "_summary.json"), "w"), indent=1)
for k, v in res.items():
    if k not in ("pan_profiles", "cut_times", "big_change_times"): print(k, v)
print("cut_times", res["cut_times"][:80])
print("big_change_times", res["big_change_times"][:120])
pp = sorted(prof, key=lambda d: -d["dur"])[:15]
for p in pp: print(p)
ei = [p["ease_in_s"] for p in prof if p["dur"] > 1.5]; eo = [p["ease_out_s"] for p in prof if p["dur"] > 1.5]
if ei: print("ease_in median", np.median(ei), "ease_out median", np.median(eo), "n", len(ei))
