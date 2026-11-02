"""Look statistics for one video: tone, black level, shadow/highlight colour, ink on edges, soft (lens-blurred) edges.

usage: python -I look_stats.py <ffmpeg> <video> <out_prefix> [--step 3] [--threads 4] [--split T (s)]

Every `step`-th frame is decoded at 720x1280 (portrait; ours are scaled down to the reference size) and the caption
band (60-80 % of the height) is removed from every statistic. Per frame:
  Y'      Rec.709 luma of sRGB values, 0-1: p1, p5, p50, p95, mean
  ink     black top-hat (9x9 grey closing - Y' > 0.12) and Y' < 0.30: thin dark lines
  blk     "pure black area": Y' < 0.06 and not ink (dilated 2 px), share of the frame
  np5     non-ink p5 (the black level of areas, not lines)
  sat     HSV S mean over V > 0.15;  colf = Hasler-Suesstrunk colourfulness
  shadow  mean CIELAB a*, b* of non-ink pixels with Y' < 0.30 (and their hue angle);  hi = same for Y' > 0.70
  edges   Canny (60/140 on a 1-px blurred Y') strong-edge pixels with local contrast (9x9 max-min) >= 0.15:
          ink_edge  share of strong edges with an ink pixel within 2 px  (outlined edges)
          soft_edge share of strong edges whose |grad| / contrast < 0.18 (a step blurred by sigma >~ 2 px at 720 wide;
                    crisp anti-aliased edges score ~0.4-0.5)
--split T: also report every statistic before and after T seconds (e.g. the "You see" pivot).
Writes <out_prefix>_look.json and <out_prefix>_look.csv.
"""
import argparse
import csv
import json
import subprocess

import numpy as np
import cv2

W, H = 720, 1280
C0, C1 = int(0.60 * H), int(0.80 * H)


def lab_ab(rgb):
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    return lab[..., 1] - 128.0, lab[..., 2] - 128.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ffmpeg"); ap.add_argument("video"); ap.add_argument("out")
    ap.add_argument("--step", type=int, default=3); ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--split", type=float, default=None)
    a = ap.parse_args()
    cv2.setNumThreads(2)
    probe = subprocess.run([a.ffmpeg.replace("ffmpeg", "ffprobe"), "-v", "error", "-select_streams", "v:0",
                            "-show_entries", "stream=avg_frame_rate", "-of", "csv=p=0", a.video],
                           capture_output=True, text=True).stdout.strip().split("\n")[0]
    num, _, den = probe.partition("/")
    fps = float(num) / float(den or 1)
    vf = (f"select=not(mod(n\\,{a.step})),scale={W}:{H}:flags=area:in_color_matrix=bt709:in_range=tv:out_range=pc")
    cmd = [a.ffmpeg, "-v", "error", "-threads", str(a.threads), "-i", a.video, "-map", "0:v:0", "-fps_mode",
           "passthrough", "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    keep = np.ones(H, bool); keep[C0:C1] = False
    k9 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    k5 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    rows = []
    i = 0
    while True:
        buf = p.stdout.read(W * H * 3)
        if len(buf) < W * H * 3:
            break
        rgb = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        f = rgb.astype(np.float32) / 255.0
        Y = f @ np.array([0.2126, 0.7152, 0.0722], np.float32)
        th = cv2.morphologyEx(Y, cv2.MORPH_CLOSE, k9) - Y
        ink = (th > 0.12) & (Y < 0.30)
        inkd = cv2.dilate(ink.astype(np.uint8), k5) > 0
        K = keep[:, None] & np.ones((1, W), bool)
        Yk = Y[K]
        nonink = K & ~inkd
        mx, mn = f.max(-1), f.min(-1)
        S = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
        vmask = K & (mx > 0.15)
        rg = f[..., 0] - f[..., 1]; yb = 0.5 * (f[..., 0] + f[..., 1]) - f[..., 2]
        colf = float(np.hypot(rg[K].std(), yb[K].std()) + 0.3 * np.hypot(rg[K].mean(), yb[K].mean()))
        A, B = lab_ab(rgb)
        sh = nonink & (Y < 0.30); hi = nonink & (Y > 0.70)
        g8 = (cv2.GaussianBlur(Y, (0, 0), 1.0) * 255).astype(np.uint8)
        E = cv2.Canny(g8, 60, 140) > 0
        cont = cv2.dilate(Y, k9) - cv2.erode(Y, k9)
        gx = cv2.Sobel(Y, cv2.CV_32F, 1, 0, ksize=3) / 8.0; gy = cv2.Sobel(Y, cv2.CV_32F, 0, 1, ksize=3) / 8.0
        gm = np.hypot(gx, gy)
        SE = E & K & (cont >= 0.15)
        ne = int(SE.sum())
        inkn = cv2.dilate(ink.astype(np.uint8), k5) > 0
        acu = gm[SE] / np.maximum(cont[SE], 1e-3)
        np5 = float(np.percentile(Y[nonink], 5)) if nonink.any() else float("nan")
        rows.append(dict(
            frame=i * a.step, t=round(i * a.step / fps, 3),
            p1=round(float(np.percentile(Yk, 1)), 4), p5=round(float(np.percentile(Yk, 5)), 4),
            p50=round(float(np.median(Yk)), 4), p95=round(float(np.percentile(Yk, 95)), 4),
            mean=round(float(Yk.mean()), 4), np5=round(np5, 4),
            blk=round(float((nonink & (Y < 0.06)).sum() / K.sum()), 5), ink=round(float((ink & K).sum() / K.sum()), 4),
            sat=round(float(S[vmask].mean()), 4) if vmask.any() else 0.0, colf=round(colf * 100, 2),
            sh_n=int(sh.sum()), sh_a=round(float(A[sh].mean()), 2) if sh.sum() > 200 else None,
            sh_b=round(float(B[sh].mean()), 2) if sh.sum() > 200 else None,
            hi_a=round(float(A[hi].mean()), 2) if hi.sum() > 200 else None,
            hi_b=round(float(B[hi].mean()), 2) if hi.sum() > 200 else None,
            all_b=round(float(B[K].mean()), 2),
            edges=ne, ink_edge=round(float(inkn[SE].mean()), 4) if ne > 200 else None,
            soft_edge=round(float((acu < 0.18).mean()), 4) if ne > 200 else None,
            acu_med=round(float(np.median(acu)), 3) if ne > 200 else None))
        i += 1
    p.wait()

    def summ(rs):
        def col(k):
            return np.array([r[k] for r in rs if r[k] is not None], float)
        pct = lambda x, qs: [round(float(v), 3) for v in np.percentile(x, qs)] if len(x) else []
        sa, sb = col("sh_a"), col("sh_b")
        ha, hb = col("hi_a"), col("hi_b")
        shue = np.degrees(np.arctan2(sb, sa)) % 360 if len(sa) else np.array([])
        return dict(
            n=len(rs),
            luma_p50_med=pct(col("p50"), [50]), luma_mean_pct_10_50_90=pct(col("mean"), [10, 50, 90]),
            luma_p1_med=pct(col("p1"), [50]), luma_p95_med=pct(col("p95"), [50]),
            nonink_p5_pct_10_50_90=pct(col("np5"), [10, 50, 90]),
            black_area_share_med=pct(col("blk"), [50]), frames_black_area_over_1pct=round(float((col("blk") > 0.01).mean()), 3),
            ink_px_share_med=pct(col("ink"), [50]),
            sat_pct_10_50_90=pct(col("sat"), [10, 50, 90]), colourfulness_med=pct(col("colf"), [50]),
            shadow_a_b_med=[pct(sa, [50]), pct(sb, [50])],
            shadow_b_negative_share=round(float((sb < 0).mean()), 3) if len(sb) else None,
            shadow_hue_deg_pct_25_50_75=pct(shue, [25, 50, 75]),
            highlight_a_b_med=[pct(ha, [50]), pct(hb, [50])],
            highlight_b_positive_share=round(float((hb > 0).mean()), 3) if len(hb) else None,
            frame_b_med=pct(col("all_b"), [50]),
            ink_edge_pct_25_50_75=pct(col("ink_edge"), [25, 50, 75]),
            soft_edge_pct_25_50_75=pct(col("soft_edge"), [25, 50, 75]),
            frames_soft_edge_over_40pct=round(float((col("soft_edge") > 0.4).mean()), 3),
            acutance_med=pct(col("acu_med"), [50]))
    res = dict(video=a.video, fps=fps, step=a.step, caption_band=[0.60, 0.80], all=summ(rows))
    if a.split is not None:
        res["split_t"] = a.split
        res["before"] = summ([r for r in rows if r["t"] < a.split])
        res["after"] = summ([r for r in rows if r["t"] >= a.split])
    json.dump(res, open(a.out + "_look.json", "w"), indent=1)
    with open(a.out + "_look.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print(json.dumps(res["all"]))


if __name__ == "__main__":
    main()
