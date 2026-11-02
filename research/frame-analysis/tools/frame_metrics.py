"""Every-frame metrics for one video, at its native frame rate.

usage: python -I frame_metrics.py <ffmpeg> <video> <out_prefix> [--threads 6] [--start S] [--end S]

Decodes every frame (no fps filter, -fps_mode passthrough) at 192x108 and records per frame:
  rgb mean, luma mean, mean saturation, chroma-weighted circular hue mean + concentration,
  d1  = mean |luma(i) - luma(i-1)|              (frame-difference energy, 0-255)
  h1  = 0.5 * L1 distance of 8x8x8 RGB histograms (0-1)
  grid = 16x9 block-mean RGB signature (layout fingerprint)
Derived (written to <out_prefix>_events.json):
  hard cuts       one-frame layout jump: g1 >= CUT_G, >= 3x both neighbours, h1 >= 0.12 or g1 >= 2*CUT_G
  flashes         a jump that returns to the pre-jump layout within 0.4 s (not counted as cuts)
  transitions     gradual full-frame replacement: grid distance over 0.6 s >= TR_G with no hard cut
                  in the window and no single frame carrying more than half of the change
                  (dissolves, wipes, fast push/zoom-through)
  comp events     composition changes without a cut: 1.0 s grid distance >= COMP_G, peak-picked,
                  >= 1 s apart, not within 0.5 s of a hard cut (big camera move, layout swap,
                  large element entering)
  shots           segments between hard cuts and transitions
Per-frame arrays go to <out_prefix>.npz so the colour-script and sheet tools can reuse them.
Run on the Spark with CUDA_VISIBLE_DEVICES="" nice -n 10 (CPU only).
"""
import sys, subprocess, json, argparse
import numpy as np

CUT_G = 14.0     # one-frame grid change (0-255 scale) for a hard cut
TR_G = 38.0      # 0.6 s grid change for a gradual full-frame transition
COMP_G = 22.0    # 1.0 s grid change for a composition-change event
W, H = 192, 108
GX, GY = 16, 9

ap = argparse.ArgumentParser()
ap.add_argument("ffmpeg"); ap.add_argument("video"); ap.add_argument("out")
ap.add_argument("--threads", type=int, default=6)
ap.add_argument("--start", type=float, default=0.0)
ap.add_argument("--end", type=float, default=0.0, help="stop at this time (0 = end of file)")
a = ap.parse_args()

probe = subprocess.run([a.ffmpeg.replace("ffmpeg", "ffprobe"), "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "stream=r_frame_rate,avg_frame_rate", "-of", "csv=p=0", a.video],
                       capture_output=True, text=True).stdout.strip().split("\n")[0].split(",")
num, den = probe[0].split("/"); fps = float(num) / float(den)

cmd = [a.ffmpeg, "-v", "error", "-threads", str(a.threads)]
if a.start: cmd += ["-ss", str(a.start)]
cmd += ["-i", a.video]
if a.end: cmd += ["-t", str(a.end - a.start)]
cmd += ["-map", "0:v:0", "-fps_mode", "passthrough", "-vf", f"scale={W}:{H}:flags=area",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
p = subprocess.Popen(cmd, stdout=subprocess.PIPE)

rgbm, lum, sat, hue, hconc, d1, h1, grids = [], [], [], [], [], [], [], []
prevY = prevH = None
FB = W * H * 3
while True:
    b = p.stdout.read(FB)
    if len(b) < FB: break
    f = np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.float32)
    Y = 0.2126 * f[..., 0] + 0.7152 * f[..., 1] + 0.0722 * f[..., 2]
    mx = f.max(-1); mn = f.min(-1); c = mx - mn
    s = np.where(mx > 0, c / np.maximum(mx, 1e-6), 0)
    r, g, bl = f[..., 0], f[..., 1], f[..., 2]
    # hue in degrees
    hh = np.zeros_like(mx)
    m = c > 1e-6
    rr = (mx == r) & m; gg = (mx == g) & m & ~rr; bb = m & ~rr & ~gg
    hh[rr] = ((g - bl)[rr] / c[rr]) % 6
    hh[gg] = ((bl - r)[gg] / c[gg]) + 2
    hh[bb] = ((r - g)[bb] / c[bb]) + 4
    hh *= 60.0
    wgt = c / 255.0
    ang = np.deg2rad(hh)
    sx, sy = (wgt * np.cos(ang)).sum(), (wgt * np.sin(ang)).sum()
    tw = wgt.sum() + 1e-6
    hue.append(float(np.rad2deg(np.arctan2(sy, sx)) % 360)); hconc.append(float(np.hypot(sx, sy) / tw))
    rgbm.append(f.reshape(-1, 3).mean(0)); lum.append(float(Y.mean())); sat.append(float(s.mean()))
    hist = np.histogramdd((f.reshape(-1, 3) // 32), bins=(8, 8, 8), range=((0, 8),) * 3)[0].ravel() / (W * H)
    grids.append(f.reshape(GY, H // GY, GX, W // GX, 3).mean((1, 3)).astype(np.float16))
    if prevY is None:
        d1.append(0.0); h1.append(0.0)
    else:
        d1.append(float(np.abs(Y - prevY).mean())); h1.append(float(0.5 * np.abs(hist - prevH).sum()))
    prevY, prevH = Y, hist
p.wait()

n = len(lum)
G = np.stack(grids).astype(np.float32).reshape(n, -1)
d1 = np.array(d1); h1 = np.array(h1); lum = np.array(lum)
g1 = np.zeros(n); g1[1:] = np.abs(G[1:] - G[:-1]).mean(1)

def gdist(i, j):
    return float(np.abs(G[i] - G[j]).mean())

# ---- hard cuts and flashes
cand = []
for i in range(1, n):
    nb = max(g1[i - 1] if i > 1 else 0, g1[i + 1] if i + 1 < n else 0)
    if g1[i] >= CUT_G and g1[i] >= 3 * nb and (h1[i] >= 0.12 or g1[i] >= 2 * CUT_G):
        cand.append(i)
cuts, flashes = [], []
skip = set()
for k, i in enumerate(cand):
    if i in skip: continue
    # flash: layout returns to pre-jump state within 0.4 s
    ret = [j for j in cand[k + 1:] if j - i <= int(0.4 * fps)]
    if ret and gdist(i - 1, ret[-1]) < 0.35 * g1[i]:
        flashes.append(i); skip.update(ret); continue
    if cuts and i - cuts[-1] <= 2: continue
    cuts.append(i)
cutset = np.zeros(n, bool); cutset[cuts] = True

# ---- gradual transitions (full-frame replacement without a hard cut)
w6 = max(2, int(round(0.6 * fps)))
gw6 = np.zeros(n); gw6[w6:] = np.abs(G[w6:] - G[:-w6]).mean(1)
cum_cut = np.concatenate([[0], np.cumsum(cutset)])
trans = []
i = w6
while i < n:
    if gw6[i] >= TR_G and cum_cut[i + 1] - cum_cut[i - w6 + 1] == 0 and g1[i - w6 + 1:i + 1].max() < 0.5 * gw6[i]:
        j = i
        while j + 1 < n and gw6[j + 1] >= gw6[j]: j += 1   # climb to the local peak
        lo = j - w6
        if not trans or lo > trans[-1][1]:
            # 10-90 % duration of the change, measured from a frame 1.2 s before the peak
            A = max(0, j - int(1.2 * fps)); B = min(n - 1, j + int(0.2 * fps))
            tot = gdist(A, B) + 1e-6
            dk = [gdist(A, k) / tot for k in range(A, B + 1)]
            k10 = next(k for k, v in enumerate(dk) if v >= 0.1); k90 = next(k for k, v in enumerate(dk) if v >= 0.9)
            s0, s1 = A + k10, (A + k90 if k90 > k10 else j)
            if trans and s0 <= trans[-1][1] + 1:      # overlapping detections of one change: merge
                p0, p1, pg = trans.pop(); s0, s1 = min(p0, s0), max(p1, s1); g = max(pg, float(gw6[j]))
            else:
                g = float(gw6[j])
            trans.append((s0, s1, round(g, 1)))
        i = j + w6
    else:
        i += 1

# ---- composition-change events (1 s window), excluding cuts and transitions
w10 = max(2, int(round(1.0 * fps)))
gw10 = np.zeros(n); gw10[w10:] = np.abs(G[w10:] - G[:-w10]).mean(1)
block = np.zeros(n, bool)
for c in cuts: block[max(0, c - int(0.5 * fps)):c + w10 + int(0.5 * fps)] = True
for lo, hi, _ in trans: block[max(0, lo - int(0.3 * fps)):hi + w10] = True
comp = []
order = np.argsort(-gw10)
taken = np.zeros(n, bool)
for i in order:
    if gw10[i] < COMP_G: break
    if block[i] or taken[i]: continue
    comp.append(int(i)); taken[max(0, i - w10):i + w10] = True
comp.sort()

# ---- shots
bounds = sorted([0] + cuts + [hi for lo, hi, _ in trans] + [n])
shots = []
for s0, s1 in zip(bounds[:-1], bounds[1:]):
    if s1 - s0 < 2: continue
    seg = slice(s0, s1)
    rm = np.stack(rgbm[s0:s1]).mean(0)
    shots.append(dict(start=round(s0 / fps + a.start, 3), end=round(s1 / fps + a.start, 3),
                      dur=round((s1 - s0) / fps, 3), rgb=[int(x) for x in rm],
                      lum=round(float(lum[seg].mean()), 1), n_comp=int(sum(1 for c in comp if s0 <= c < s1))))
sl = np.array([s["dur"] for s in shots])
dur = n / fps
T = lambda i: round(i / fps + a.start, 3)
pct = lambda x, q: [round(float(v), 2) for v in np.percentile(x, q)] if len(x) else []
res = dict(video=a.video, fps=fps, start=a.start, n_frames=n, duration=round(dur, 2),
           thresholds=dict(CUT_G=CUT_G, TR_G=TR_G, COMP_G=COMP_G),
           n_cuts=len(cuts), n_flashes=len(flashes), n_transitions=len(trans), n_comp=len(comp),
           cuts_per_min=round(len(cuts) / dur * 60, 2), shots_per_min=round(len(shots) / dur * 60, 2),
           comp_per_min=round(len(comp) / dur * 60, 2),
           trans_dur_pct_10_25_50_75_90=pct([(hi - lo) / fps for lo, hi, _ in trans], [10, 25, 50, 75, 90]),
           n_trans_fast=int(sum(1 for lo, hi, _ in trans if (hi - lo) / fps <= 0.3)),
           shot_len=dict(n=len(sl), mean=round(float(sl.mean()), 2), median=round(float(np.median(sl)), 2),
                         p10_25_75_90=pct(sl, [10, 25, 75, 90]), max=round(float(sl.max()), 2)),
           # interval between any visual event (cut, transition, comp event)
           d1_pct_5_25_50_75_95=pct(d1[1:], [5, 25, 50, 75, 95]),
           static_frac=round(float((d1[1:] < 0.15).mean()), 4), low_motion_frac=round(float((d1[1:] < 0.5).mean()), 4),
           cuts=[T(i) for i in cuts], flashes=[T(i) for i in flashes],
           transitions=[dict(start=T(lo), end=T(hi), dur=round((hi - lo) / fps, 3), g=g) for lo, hi, g in trans],
           comp_events=[dict(t=T(i), g=round(float(gw10[i]), 1)) for i in comp],
           shots=shots)
ev = sorted([T(i) for i in cuts] + [T(hi) for _, hi, _ in trans] + [T(i) for i in comp])
gaps = np.diff([a.start] + ev) if ev else np.array([])
res["visual_event_gap"] = dict(n=len(ev), median=pct(gaps, [50])[0] if len(gaps) else None,
                               p10_25_75_90=pct(gaps, [10, 25, 75, 90]))
json.dump(res, open(a.out + "_events.json", "w"), indent=1)
np.savez_compressed(a.out + ".npz", fps=fps, start=a.start, rgb=np.stack(rgbm).astype(np.float32), lum=lum,
                    sat=np.array(sat), hue=np.array(hue), hconc=np.array(hconc), d1=d1, h1=h1, g1=g1,
                    gw6=gw6, gw10=gw10, rows=G.reshape(n, GY, GX, 3).mean(2).astype(np.float16))
print(json.dumps({k: res[k] for k in ("fps", "n_frames", "duration", "n_cuts", "n_flashes", "n_transitions",
                                      "n_comp", "cuts_per_min", "shots_per_min", "comp_per_min", "shot_len",
                                      "visual_event_gap", "static_frac")}))
