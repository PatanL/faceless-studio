"""Scene-change list + shot-length stats from scores.sh output ("t score" per frame).
usage: python -I cuts.py <scores.txt> [fps=60] [win_thr=0.2]

TIS rarely hard-cuts: most scene changes are 0.2-0.4 s whip/zoom/slide transitions with
motion blur, which spread a moderate ffmpeg scene score over 10-25 frames. So:
  hard cut   = one frame with score >= 0.25 that is >= 4x its +-5-frame median
  transition = local maximum of the 0.33 s windowed score sum >= win_thr (default 0.2; checked by eye
               against the contact sheets: 0.35 missed slide transitions at O4y 0:22 and 1:03)
Events closer than 0.6 s are merged. Shots = intervals between events.
Also reports the per-frame "always moving" share (score > 0.001 = something changed).
"""
import sys, json
import numpy as np

rows = [l.split() for l in open(sys.argv[1]) if l.strip()]
fps = float(sys.argv[2]) if len(sys.argv) > 2 else 60.0
t = np.array([float(r[0]) for r in rows]); s = np.array([float(r[1]) for r in rows])
n = len(s); w = max(3, int(round(fps / 3)))
thr = float(sys.argv[3]) if len(sys.argv) > 3 else 0.2
hard = []
for i in range(n):
    if s[i] >= 0.25:
        nb = np.concatenate([s[max(0, i - 5):i], s[i + 1:i + 6]])
        if s[i] >= 4 * max(np.median(nb), 0.01):
            hard.append(i)
win = np.convolve(s, np.ones(w), mode="same")
trans = []
for i in range(1, n - 1):
    if win[i] >= thr and win[i] >= win[i - 1] and win[i] > win[i + 1]:
        trans.append(i)
ev = sorted([(t[i], "cut") for i in hard] + [(t[i], "trans") for i in trans])
merged = []
for tt, k in ev:
    if merged and tt - merged[-1][0] < 0.6:
        if k == "cut":
            merged[-1] = (merged[-1][0], "cut")
        continue
    merged.append((float(tt), k))
# runs of >= 3 events spaced < 0.9 s are sustained fast motion (spinning vortex, particle
# storms), not scene changes: keep only the run's first event and log the run.
groups, busy = [], []
for m in merged:
    if groups and m[0] - groups[-1][-1][0] < 0.9:
        groups[-1].append(m)
    else:
        groups.append([m])
kept = []
for g in groups:
    if len(g) >= 3:
        busy.append((round(g[0][0], 2), round(g[-1][0], 2)))
        kept.append(g[0])
    else:
        kept.extend(g)
merged = kept
dur = float(t[-1])
edges = [0.0] + [m[0] for m in merged] + [dur]
L = np.diff(edges)
pc = lambda p: round(float(np.percentile(L, p)), 2)
out = {
    "duration_s": round(dur, 1), "events": len(merged),
    "hard_cuts": sum(1 for m in merged if m[1] == "cut"), "animated_transitions": sum(1 for m in merged if m[1] == "trans"),
    "events_per_min": round(len(merged) / dur * 60, 1),
    "shot_len_s": {"mean": round(float(L.mean()), 2), "p10": pc(10), "p25": pc(25), "median": pc(50), "p75": pc(75), "p90": pc(90)},
    "shots_under_1.5s": int((L < 1.5).sum()), "shots_over_10s": int((L > 10).sum()),
    "frames_changing(score>0.001)": round(float((s > 0.001).mean()), 3),
    "frames_static(score<=0.0005)": round(float((s <= 0.0005).mean()), 3),
    "sustained_fast_motion_runs": len(busy),
    "score_p50_p90_p99": [round(float(np.percentile(s, p)), 4) for p in (50, 90, 99)],
}
print(json.dumps(out, indent=1))
json.dump({"stats": out, "events": merged, "busy": busy}, open(sys.argv[1].replace(".txt", "_events.json"), "w"))
