"""Camera motion from every frame: sub-pixel phase correlation on 9 tiles, fitted as a similarity (pan, zoom, roll).

usage: python -I camera_motion.py <ffmpeg> <video> <out_prefix> [--events frame_metrics_events.json] [--threads 4]
                                  [--mask-transitions]

Why: a whole-frame difference cannot tell a slow push-in from a still frame, and integer phase correlation misses
moves below a few px/frame. This fits each frame against the previous one so 0.1 px/f drifts are visible.

Method
  frames decoded at 360x640 (portrait) grey, every frame, -fps_mode passthrough
  tiles: 3 columns x 3 bands at 3-29 %, 29-56 % and 80-97 % of the height (the 56-80 % caption band is skipped)
  per tile: cv2.phaseCorrelate with a Hann window (sub-pixel); tiles with response < 0.08 or flat texture dropped
  fit: dx = tx + s*x - r*y, dy = ty + s*y + r*x (x, y from the frame centre); the worst tile is dropped while its
       residual > 2.0 px (720-scale 4 px: a 3D dolly gives parallax, so a pure similarity never fits exactly) and
       >= 4 tiles remain
  speed (px/f at 720x1280) = 2*|t| + (|s| + |r|) * 734   (734 = corner radius at 720x1280; same definition as the
       tutorial repo's motion report); Gaussian sigma 1.2 f over fitted frames
  fallback: frames the similarity cannot fit but where >= 3 tiles correlate get "tile speed" = 2 * median tile shift
  masked: frames within 2 f of a hard cut or flash (from frame_metrics.py events; its gradual "transitions" are
          masked only with --mask-transitions, because most of them are fast camera travel)
Classes (fitted frames): hold < 0.3 px/f, drift 0.3-2, move >= 2.  "moving" = drift + move.
  moving_any: over every unmasked frame with >= 3 tiles, max(fit speed, tile speed) >= 0.3
Moves: peaks of the speed smoothed with sigma 2 f, >= 6 px/f, >= 10 f apart, all frames around them fitted;
  fwhm = contiguous frames >= half the peak; len_eq = fwhm / 0.54 = the length of a smootherstep move with that
  FWHM (validated: a synthetic 23 f smootherstep of 100 px reads peak 8.5 px/f, fwhm 12-13 f, len_eq ~23 f);
  attack/release = frames from 10 % of the peak up to it / down from it.
  A move that runs into a cut, an unfit frame or another move is still counted (its fwhm is a lower bound).
Push-ins: zoom rate s in fitted frames whose translation is < 2 px/f (synthetic 0.20 %/f reads ~0.15-0.2).
Writes <out_prefix>_cam.json (summary) and <out_prefix>_cam.npz (per-frame tx, ty, s, r, speed, good, tile).
"""
import argparse
import json
import subprocess

import numpy as np
import cv2

W, H = 360, 640
BANDS = [(0.03, 0.29), (0.29, 0.56), (0.80, 0.97)]
COLS = [(0.02, 0.34), (0.34, 0.66), (0.66, 0.98)]
R720 = float(np.hypot(360, 640))  # corner radius at 720x1280
RES_MAX = 2.0


def tiles():
    out = []
    for b0, b1 in BANDS:
        for c0, c1 in COLS:
            y0, y1, x0, x1 = int(b0 * H), int(b1 * H), int(c0 * W), int(c1 * W)
            out.append((y0, y1, x0, x1, (x0 + x1) / 2 - W / 2, (y0 + y1) / 2 - H / 2))
    return out


def fit(pts):
    """pts: list of (x, y, dx, dy). Returns tx, ty, s, r, n or None."""
    pts = list(pts)
    while len(pts) >= 4:
        A, b = [], []
        for x, y, dx, dy, in pts:
            A.append([1, 0, x, -y]); b.append(dx)
            A.append([0, 1, y, x]); b.append(dy)
        A = np.array(A, float); b = np.array(b, float)
        p, *_ = np.linalg.lstsq(A, b, rcond=None)
        res = (A @ p - b).reshape(-1, 2)
        e = np.hypot(res[:, 0], res[:, 1])
        k = int(e.argmax())
        if e[k] > RES_MAX and len(pts) > 4:
            pts.pop(k)
            continue
        if e[k] > RES_MAX:
            return None
        return float(p[0]), float(p[1]), float(p[2]), float(p[3]), len(pts)
    return None


def gsmooth(x, good, sigma):
    r = int(3 * sigma) + 1
    k = np.arange(-r, r + 1); gk = np.exp(-0.5 * (k / sigma) ** 2)
    num = np.convolve(np.where(good, x, 0), gk, "same"); den = np.convolve(good.astype(float), gk, "same")
    return np.where(den > 0.3, num / np.maximum(den, 1e-6), 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ffmpeg"); ap.add_argument("video"); ap.add_argument("out")
    ap.add_argument("--events", default=None)
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--mask-transitions", action="store_true")
    a = ap.parse_args()
    cv2.setNumThreads(2)
    probe = subprocess.run([a.ffmpeg.replace("ffmpeg", "ffprobe"), "-v", "error", "-select_streams", "v:0",
                            "-show_entries", "stream=avg_frame_rate", "-of", "csv=p=0", a.video],
                           capture_output=True, text=True).stdout.strip().split("\n")[0]
    num, _, den = probe.partition("/")
    fps = float(num) / float(den or 1)
    cmd = [a.ffmpeg, "-v", "error", "-threads", str(a.threads), "-i", a.video, "-map", "0:v:0", "-fps_mode",
           "passthrough", "-vf", f"scale={W}:{H}:flags=area", "-f", "rawvideo", "-pix_fmt", "gray", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    T = tiles()
    wins = {(y1 - y0, x1 - x0): cv2.createHanningWindow((x1 - x0, y1 - y0), cv2.CV_32F) for y0, y1, x0, x1, _, _ in T}
    rows, tsp, ntl = [], [], []
    prev = None
    while True:
        buf = p.stdout.read(W * H)
        if len(buf) < W * H:
            break
        g = np.frombuffer(buf, np.uint8).reshape(H, W).astype(np.float32)
        if prev is None:
            rows.append((0, 0, 0, 0, 0)); tsp.append(0.0); ntl.append(0); prev = g; continue
        pts = []
        for y0, y1, x0, x1, cx, cy in T:
            A0, A1 = prev[y0:y1, x0:x1], g[y0:y1, x0:x1]
            if A0.std() < 2.0 or A1.std() < 2.0:
                continue
            (dx, dy), resp = cv2.phaseCorrelate(A0, A1, wins[(y1 - y0, x1 - x0)])
            if resp < 0.08 or abs(dx) > 40 or abs(dy) > 40:
                continue
            pts.append((cx, cy, dx, dy))
        ntl.append(len(pts))
        tsp.append(2 * float(np.median([np.hypot(q[2], q[3]) for q in pts])) if len(pts) >= 3 else np.nan)
        f = fit(pts)
        rows.append((1, *f[:4]) if f else (0, 0, 0, 0, 0))
        prev = g
    p.wait()
    R = np.array(rows, float)
    tsp = np.array(tsp, float)
    n = len(R)
    valid = R[:, 0] > 0
    tx, ty, s, r = R[:, 1], R[:, 2], R[:, 3], R[:, 4]
    raw = 2 * np.hypot(tx, ty) + (np.abs(s) + np.abs(r)) * R720
    mask = np.zeros(n, bool); mask[0] = True
    if a.events:
        ev = json.load(open(a.events))
        for t in ev.get("cuts", []) + ev.get("flashes", []):
            k = int(round(t * fps)); mask[max(0, k - 2):k + 3] = True
        if a.mask_transitions:
            for tr in ev.get("transitions", []):
                mask[int(tr["start"] * fps):int(tr["end"] * fps) + 1] = True
    good = valid & ~mask
    sp = gsmooth(raw, good, 1.2)
    S = sp[good]
    hold = float((S < 0.3).mean()); drift = float(((S >= 0.3) & (S < 2)).mean()); move = float((S >= 2).mean())
    anyok = ~mask & (valid | ~np.isnan(tsp))
    anysp = np.where(valid, sp, np.nan_to_num(tsp))
    moving_any = float((anysp[anyok] >= 0.3).mean())
    move_any = float((anysp[anyok] >= 2).mean())
    # moves on a smoother speed
    sp2 = gsmooth(raw, good, 2.0)
    moves, last = [], -99
    for i in range(1, n - 1):
        if not good[i] or sp2[i] < 6 or sp2[i] < sp2[i - 1] or sp2[i] < sp2[i + 1] or i - last < 10:
            continue
        pk = sp2[i]
        lo = i
        while lo > 0 and good[lo - 1] and sp2[lo - 1] >= 0.5 * pk:
            lo -= 1
        hi = i
        while hi < n - 1 and good[hi + 1] and sp2[hi + 1] >= 0.5 * pk:
            hi += 1
        fw = hi - lo + 1
        lo10 = i
        while lo10 > 0 and good[lo10 - 1] and sp2[lo10 - 1] >= 0.1 * pk and sp2[lo10 - 1] <= sp2[lo10] + 0.5:
            lo10 -= 1
        hi10 = i
        while hi10 < n - 1 and good[hi10 + 1] and sp2[hi10 + 1] >= 0.1 * pk and sp2[hi10 + 1] <= sp2[hi10] + 0.5:
            hi10 += 1
        moves.append(dict(f=i, t=round(i / fps, 2), peak=round(float(pk), 1), fwhm=fw, len_eq=round(fw / 0.54, 1),
                          attack=i - lo10, release=hi10 - i))
        last = i
    q = good & (2 * np.hypot(tx, ty) < 2)
    zr = s[q] * 100  # %/frame
    pct = lambda x, qs: [round(float(v), 2) for v in np.percentile(x, qs)] if len(x) else []
    col = lambda k: np.array([m[k] for m in moves], float)
    dur = n / fps
    res = dict(video=a.video, fps=fps, frames=n, fitted_frames=int(good.sum()), masked_frames=int(mask.sum()),
               unfit_frames=int((~valid & ~mask).sum()), tile_only_frames=int((anyok & ~valid).sum()),
               hold=round(hold, 3), drift=round(drift, 3), move=round(move, 3), moving=round(drift + move, 3),
               moving_any=round(moving_any, 3), move_any=round(move_any, 3),
               speed_pct_25_50_75_90=pct(S, [25, 50, 75, 90]),
               n_moves=len(moves), moves_per_10s=round(len(moves) / dur * 10, 2),
               move_peak_pct_25_50_75_90=pct(col("peak"), [25, 50, 75, 90]),
               move_fwhm_pct_25_50_75=pct(col("fwhm"), [25, 50, 75]),
               move_len_eq_pct_25_50_75=pct(col("len_eq"), [25, 50, 75]),
               move_attack_med=pct(col("attack"), [50]), move_release_med=pct(col("release"), [50]),
               snaps_attack_le3_peak_ge25=int(((col("attack") <= 3) & (col("peak") >= 25)).sum()) if moves else 0,
               quiet_frames=int(q.sum()),
               quiet_zoom_active=round(float((np.abs(zr) >= 0.05).mean()), 3) if len(zr) else None,
               quiet_pushin_share=round(float((zr >= 0.05).mean()), 3) if len(zr) else None,
               quiet_zoom_rate_pct_med=pct(np.abs(zr[np.abs(zr) >= 0.05]), [50]),
               moves=moves)
    json.dump(res, open(a.out + "_cam.json", "w"), indent=1)
    np.savez_compressed(a.out + "_cam.npz", fps=fps, tx=tx, ty=ty, s=s, r=r, speed=sp, good=good, tile=tsp,
                        ntiles=np.array(ntl))
    print(json.dumps({k: v for k, v in res.items() if k != "moves"}))


if __name__ == "__main__":
    main()
