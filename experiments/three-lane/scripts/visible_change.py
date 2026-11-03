"""Visible-change check on a render (our own code; the post-render twin of the `still` gate in src/kit/gates.ts).

usage: python3 -I scripts/visible_change.py <ffmpeg> <video> [--max 2.0] [--json out.json]

Every frame is compared with the one before at 270x480 (gray), with the caption band (0.60-0.82 of the height) masked,
giving the mean absolute difference d (0-255). A --max-second window (default 2 s = 60 frames) is STILL when the
median d inside it is below 1.5. Calibrated on the 8 RicksClips refs at 720p: their 2 s windows have a median d of
1.75 / 4.1-6.5 / 8.1-10 (p5 / p25 / p50 over each video), and none falls under 1.5 (GM9U is the closest, at 2.6 % of
windows under 1.0). Barca v14 had p25 2.66, so a lot of its time sat in near-still windows. Also reported:
quiet_share, the share of windows with median d < 2.5. Exit 1 when any window is still.
"""
import sys, json, subprocess
import numpy as np

W, H = 270, 480


def main():
    ff, vid = sys.argv[1:3]
    mx = float(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 2.0
    p = subprocess.run([ff, "-v", "error", "-i", vid, "-vf", f"scale={W}:{H}:flags=area,format=gray", "-f", "rawvideo", "-"], capture_output=True, check=True)
    F = np.frombuffer(p.stdout, np.uint8).reshape(-1, H, W).astype(np.float32)
    keep = np.ones((H, W), bool); keep[int(0.60 * H):int(0.82 * H)] = False
    d = np.array([np.abs(F[i] - F[i - 1])[keep].mean() for i in range(1, len(F))])
    n = int(round(mx * 30))
    wins = np.array([np.median(d[i:i + n]) for i in range(0, max(1, len(d) - n + 1))])
    runs, s = [], None
    for i, still in enumerate(list(wins < 1.5) + [False]):
        if still and s is None: s = i
        if not still and s is not None:
            runs.append([round(s / 30, 2), round((i + n) / 30, 2)]); s = None
    out = {"frames": len(F), "window_median_d_p5_25_50": [round(float(np.percentile(wins, q)), 2) for q in (5, 25, 50)],
           "quiet_share": round(float((wins < 2.5).mean()), 3), "still_windows": runs}
    print(json.dumps(out))
    if "--json" in sys.argv: json.dump(out, open(sys.argv[sys.argv.index("--json") + 1], "w"), indent=1)
    sys.exit(1 if runs else 0)


if __name__ == "__main__":
    main()
