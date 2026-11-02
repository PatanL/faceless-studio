"""Every-frame metrics for one video (CPU only): cuts, transitions, motion energy, colour script, composition and
setting-change events.

usage: python -I every_frame.py <video> <out_prefix> [--threads 6] [--boundaries storyboard.json]

Decodes EVERY frame at the native rate with OpenCV (no resampling) and writes
  <out_prefix>_frames.csv   one row per frame (columns below)
  <out_prefix>_events.json  hard cuts, gradual transitions, composition-change events, shots, setting segments,
                            summary stats (shot lengths, cut rate, colour-script hue families)
Run the frame sampler (sample_frames.py) on the same video for the stills the setting catalogue is judged from.

Per-frame columns
  diff       mean |RGB(t) - RGB(t-1)| on a 108x192 (portrait) / 192x108 (landscape) area-downscaled proxy, 0-255.
             Same proxy size and maths as kurz-tools/motion_cuts.py (the reference-study cut detector), so numbers
             compare with the reference analyses.
  hist       0.5 * L1 distance of 8x8x8 RGB histograms, frame vs previous (0-1). Same as motion_cuts.py.
  hist15     the same histogram distance between t-7 and t+8 (a 0.5 s window at 30 fps): gradual change
  L,a,b      mean CIELAB (L 0-100, a/b signed)
  hue,sat,val  saturation-weighted circular mean hue (deg 0-360), mean HSV S and V (0-1)
  warm       fraction of pixels in the warm family (hue 0-50 deg or > 330 deg, S > 0.35, V > 0.25)
  bot_warm   `warm` measured in the bottom 22 % of the frame only (where the house reef strip sits)
  grid       composition: 0.5 * L1 distance between the 6x4 (portrait) luminance+edge layout of t and t-15 (0.5 s)
  bg_sim     backdrop similarity: correlation of the frame's backdrop signature (edge-orientation + Lab grid of the
             bottom 30 % and the outer 12 % side strips, the regions the set dressing occupies) with the median
             signature of the first scene. 1 = same backdrop as the cover.

Events
  cuts         motion_cuts.py rule: diff > max(14, 4 * median(+-15 neighbours)) and hist > 0.25, >= 0.3 s apart
  transitions  hist15 local maxima > 0.18 that are not within 0.3 s of a hard cut, merged into [start, end] spans
               where hist15 stays > 0.5 * peak (wipes, whips, fades, irises, full-frame cards)
  comp_events  grid local maxima > 0.12 (layout changes: figure/label/card enters, camera punch), >= 0.4 s apart
  setting      backdrop segments: bg signature clustered greedily (a new segment when the 0.5 s-median signature's
               correlation with the running segment mean drops below 0.80 for >= 0.4 s)
"""
import argparse
import csv
import json
import math
import os

import numpy as np
import cv2


def hist8(a):
    q = (a // 32).reshape(-1, 3).astype(np.int32)
    k = q[:, 0] * 64 + q[:, 1] * 8 + q[:, 2]
    return np.bincount(k, minlength=512).astype(np.float32) / k.size


def warm_mask(hsv):
    h = hsv[..., 0].astype(np.float32) * 2.0
    s = hsv[..., 1] / 255.0
    v = hsv[..., 2] / 255.0
    return ((h <= 50) | (h >= 330)) & (s > 0.35) & (v > 0.25)


def grid_sig(gray, gx, gy):
    """6x4 (portrait) layout: mean luminance and edge energy per cell, each normalised"""
    e = cv2.Canny(gray, 60, 140).astype(np.float32) / 255.0
    lum = cv2.resize(gray.astype(np.float32) / 255.0, (gx, gy), interpolation=cv2.INTER_AREA)
    edg = cv2.resize(e, (gx, gy), interpolation=cv2.INTER_AREA)
    v = np.concatenate([lum.ravel(), 3.0 * edg.ravel()])
    return v / max(1e-6, v.sum())


def bg_sig(im_small):
    """backdrop signature: bottom 30 % band + outer side strips; Lab 8x3 grid + 8-bin edge-orientation histogram"""
    h, w = im_small.shape[:2]
    bot = im_small[int(h * 0.70):, :]
    sides = np.concatenate([im_small[int(h * 0.3):int(h * 0.7), :int(w * 0.12)],
                            im_small[int(h * 0.3):int(h * 0.7), w - int(w * 0.12):]], axis=1)
    feats = []
    for reg, gw, gh in ((bot, 8, 3), (sides, 2, 4)):
        lab = cv2.cvtColor(reg, cv2.COLOR_BGR2LAB).astype(np.float32)
        g = cv2.resize(lab, (gw, gh), interpolation=cv2.INTER_AREA)
        feats.append((g / 255.0).ravel())
        gray = cv2.cvtColor(reg, cv2.COLOR_BGR2GRAY).astype(np.float32)
        sx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
        sy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
        mag = np.hypot(sx, sy)
        ang = (np.arctan2(sy, sx) % np.pi) / np.pi * 8
        oh = np.bincount(np.minimum(7, ang.astype(np.int32)).ravel(), weights=mag.ravel(), minlength=8)
        feats.append(oh / max(1e-6, oh.sum()) * 2.0)
        feats.append(np.array([float(mag.mean()) / 40.0]))
    return np.concatenate(feats).astype(np.float32)


def corr(a, b):
    a = a - a.mean()
    b = b - b.mean()
    return float((a * b).sum() / max(1e-9, math.sqrt((a * a).sum() * (b * b).sum())))


def local_max(x, i, r):
    lo, hi = max(0, i - r), min(len(x), i + r + 1)
    return x[i] >= x[lo:hi].max()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("out_prefix")
    ap.add_argument("--threads", type=int, default=6)
    ap.add_argument("--boundaries", default=None, help="storyboard.json: scene start times are added to events.json")
    a = ap.parse_args()
    cv2.setNumThreads(a.threads)

    cap = cv2.VideoCapture(a.video)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    W0 = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    H0 = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    portrait = H0 > W0
    PW, PH = (108, 192) if portrait else (192, 108)
    GX, GY = (4, 6) if portrait else (6, 4)
    SW, SH = (270, 480) if portrait else (480, 270)

    rows, hists, grids, bgs = [], [], [], []
    prev = None
    i = 0
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        px = cv2.resize(fr, (PW, PH), interpolation=cv2.INTER_AREA)
        rgb = px[..., ::-1].astype(np.int16)
        hs = hist8(px[..., ::-1])
        sm = cv2.resize(fr, (SW, SH), interpolation=cv2.INTER_AREA)
        hsv = cv2.cvtColor(sm, cv2.COLOR_BGR2HSV)
        lab = cv2.cvtColor(sm, cv2.COLOR_BGR2LAB).astype(np.float32)
        S = hsv[..., 1] / 255.0
        Hr = hsv[..., 0].astype(np.float32) * 2.0 * np.pi / 180.0
        wsum = max(1e-6, float(S.sum()))
        hue = (math.degrees(math.atan2(float((np.sin(Hr) * S).sum()) / wsum, float((np.cos(Hr) * S).sum()) / wsum)) + 360) % 360
        wm = warm_mask(hsv)
        nb = int(SH * 0.78)
        gray = cv2.cvtColor(sm, cv2.COLOR_BGR2GRAY)
        rows.append({
            "frame": i, "t": round(i / fps, 4),
            "diff": round(float(np.abs(rgb - prev).mean()), 3) if prev is not None else 0.0,
            "L": round(float(lab[..., 0].mean() * 100 / 255), 2),
            "a": round(float(lab[..., 1].mean() - 128), 2), "b": round(float(lab[..., 2].mean() - 128), 2),
            "hue": round(hue, 1), "sat": round(float(S.mean()), 4), "val": round(float(hsv[..., 2].mean() / 255.0), 4),
            "warm": round(float(wm.mean()), 4), "bot_warm": round(float(wm[nb:].mean()), 4),
        })
        hists.append(hs)
        grids.append(grid_sig(gray, GX, GY))
        bgs.append(bg_sig(sm))
        prev = rgb
        i += 1
    n = len(rows)
    hists = np.array(hists)
    grids = np.array(grids)
    bgs = np.array(bgs)
    d = np.array([r["diff"] for r in rows])
    hd = np.zeros(n)
    hd[1:] = 0.5 * np.abs(hists[1:] - hists[:-1]).sum(1)
    h15 = np.zeros(n)
    for k in range(n):
        lo, hi = max(0, k - 7), min(n - 1, k + 8)
        h15[k] = 0.5 * np.abs(hists[hi] - hists[lo]).sum()
    gr = np.zeros(n)
    for k in range(15, n):
        gr[k] = 0.5 * np.abs(grids[k] - grids[k - 15]).sum()
    ref = np.median(bgs[: max(1, int(fps * 1.0))], axis=0)
    bsim = np.array([corr(ref, b) for b in bgs])
    for k, r in enumerate(rows):
        r["hist"] = round(float(hd[k]), 4)
        r["hist15"] = round(float(h15[k]), 4)
        r["grid"] = round(float(gr[k]), 4)
        r["bg_sim"] = round(float(bsim[k]), 4)

    # hard cuts: motion_cuts.py rule (diff[i] is frame i vs i-1, so the cut lands at t = i / fps)
    cuts = []
    for k in range(1, n):
        lo, hi = max(1, k - 15), min(n, k + 16)
        nbh = np.concatenate([d[lo:k], d[k + 1:hi]])
        med = float(np.median(nbh)) if len(nbh) else 0.0
        if d[k] > max(14.0, 4 * med) and hd[k] > 0.25:
            t = k / fps
            if not cuts or t - cuts[-1] > 0.3:
                cuts.append(round(t, 3))
    # gradual transitions
    trans = []
    for k in range(n):
        if h15[k] > 0.18 and local_max(h15, k, 8) and all(abs(k / fps - c) > 0.3 for c in cuts):
            lo = k
            while lo > 0 and h15[lo - 1] > 0.5 * h15[k]:
                lo -= 1
            hi = k
            while hi < n - 1 and h15[hi + 1] > 0.5 * h15[k]:
                hi += 1
            span = [round(max(0, lo - 7) / fps, 3), round(min(n - 1, hi + 8) / fps, 3)]
            if trans and span[0] <= trans[-1]["end"]:
                if h15[k] > trans[-1]["peak"]:
                    trans[-1].update(peak=round(float(h15[k]), 3), t=round(k / fps, 3))
                trans[-1]["end"] = max(trans[-1]["end"], span[1])
                continue
            trans.append({"t": round(k / fps, 3), "start": span[0], "end": span[1], "peak": round(float(h15[k]), 3),
                          "max_frame_diff": round(float(d[max(0, k - 8):k + 9].max()), 2)})
    comp = []
    for k in range(15, n):
        if gr[k] > 0.12 and local_max(gr, k, 6):
            t = k / fps
            if not comp or t - comp[-1]["t"] >= 0.4:
                comp.append({"t": round(t - 0.25, 3), "grid": round(float(gr[k]), 3)})
    # setting segments from the backdrop signature (0.5 s medians)
    win = max(1, int(round(fps * 0.5)))
    meds = [np.median(bgs[s:s + win], axis=0) for s in range(0, n, win)]
    segs = []
    cur = {"start": 0.0, "sum": meds[0].copy(), "k": 1}
    low = 0
    for j in range(1, len(meds)):
        c = corr(cur["sum"] / cur["k"], meds[j])
        if c < 0.80:
            low += 1
            if low >= 1:
                segs.append({"start": cur["start"], "end": round(j * win / fps, 3)})
                cur = {"start": round(j * win / fps, 3), "sum": meds[j].copy(), "k": 1}
                low = 0
                continue
        else:
            low = 0
        cur["sum"] += meds[j]
        cur["k"] += 1
    segs.append({"start": cur["start"], "end": round(n / fps, 3)})

    dur = n / fps
    bounds = [0.0] + cuts + [dur]
    shots = np.diff(bounds)
    # colour script: hue family per 0.5 s
    fam = lambda h: "warm" if (h < 50 or h >= 330) else "green" if h < 150 else "teal" if h < 200 else "blue" if h < 260 else "violet"
    hues = np.array([r["hue"] for r in rows])
    fams = [fam(float(np.median(hues[s:s + win]))) for s in range(0, n, win)]
    res = {
        "video": os.path.basename(a.video), "fps": fps, "frames": n, "duration": round(dur, 3), "size": [W0, H0],
        "detector": "cuts = kurz-tools/motion_cuts.py rule on a %dx%d proxy; see every_frame.py docstring" % (PW, PH),
        "cuts": cuts, "n_cuts": len(cuts), "cuts_per_min": round(len(cuts) / dur * 60, 2),
        "shot_len": {"n": int(len(shots)), "mean": round(float(shots.mean()), 2), "median": round(float(np.median(shots)), 2),
                     "min": round(float(shots.min()), 2), "max": round(float(shots.max()), 2)},
        "transitions": trans, "n_transitions": len(trans), "comp_events": comp, "n_comp_events": len(comp),
        "comp_events_per_min": round(len(comp) / dur * 60, 1),
        "bg_segments": segs,
        "diff_pct": [round(float(x), 3) for x in np.percentile(d[1:], [5, 25, 50, 75, 95])],
        "static_frac": round(float((d[1:] < 0.15).mean()), 4), "lowmotion_frac": round(float((d[1:] < 0.5).mean()), 4),
        "hue_family_per_0.5s": fams,
        "hue_family_share": {f: round(fams.count(f) / len(fams), 3) for f in sorted(set(fams))},
        "bg_sim_pct": [round(float(x), 3) for x in np.percentile(bsim, [5, 25, 50, 75, 95])],
    }
    if a.boundaries:
        sb = json.load(open(a.boundaries))
        t = 0.0
        sc = []
        for s in sb["scenes"]:
            k0, k1 = int(round(t * fps)), min(n, int(round((t + s["duration"]) * fps)))
            seg = slice(k0, max(k0 + 1, k1))
            sc.append({"id": s["id"], "start": round(t, 3), "end": round(t + s["duration"], 3),
                       "transitionIn": (s.get("transitionIn") or {}).get("type", "cut" if t > 0 else None),
                       "mean_diff": round(float(d[seg].mean()), 3), "mean_hue": round(float(np.median(hues[seg])), 1),
                       "mean_L": round(float(np.mean([r["L"] for r in rows[seg]])), 1),
                       "bot_warm": round(float(np.mean([r["bot_warm"] for r in rows[seg]])), 4),
                       "bg_sim_med": round(float(np.median(bsim[seg])), 3)})
            t += s["duration"]
        res["scenes"] = sc
    with open(a.out_prefix + "_frames.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    json.dump(res, open(a.out_prefix + "_events.json", "w"), indent=1)
    print(n, "frames", res["n_cuts"], "cuts", res["n_transitions"], "transitions", res["n_comp_events"], "comp events",
          len(segs), "bg segments", res["shot_len"])


if __name__ == "__main__":
    main()
