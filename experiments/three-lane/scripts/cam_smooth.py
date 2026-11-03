"""Camera smoothness of a render (our own code; visual track round 3, owner: "our camera isn't as smooth as RicksClips'").

usage: python3 -I cam_smooth.py <ffmpeg> <video> <out_prefix> [--frames N] [--skip a-b,c-d] [--json out.json] [--ref other.json]

Runs research/frame-analysis/tools/camera_motion.py (sub-pixel phase correlation, similarity fit per frame) on the first
N frames, then works on the RAW per-frame motion (not its smoothed speed), at 720x1280 px:
  v(f)      = (2 tx, 2 ty, 734 s, 734 r)              translation, zoom and roll as px/f at the frame corners
  speed     = |v|;  accel = |v(f) - v(f-1)|  (px/f^2);  jerk = |a(f) - a(f-1)|  (a the vector difference)
  jumps     = frames whose accel exceeds 25 % of the local speed + 2 px/f^2 (a velocity step, not a ramp): where one
              move hands off to the next, a start or stop with no ease, a key join
  ramps     = per move (camera_motion's peaks >= 6 px/f): attack and release frames (10 % -> peak -> 10 %)
  jitter    = while holding (speed < 2 px/f): the mean |accel| and the share of frames whose direction reverses
Frames within 3 of a --skip window (cuts, dissolves) are left out. --ref prints this video against another's numbers.
"""
import json, os, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CM = os.path.join(HERE, "../../../research/frame-analysis/tools/camera_motion.py")


def analyse(npz, cam_json, n, skip):
    d = np.load(npz); c = json.load(open(cam_json))
    tx, ty, s, r, good = d["tx"][:n], d["ty"][:n], d["s"][:n], d["r"][:n], d["good"][:n].astype(bool)
    v = np.stack([2 * tx, 2 * ty, 734 * s, 734 * r], 1)
    ok = good.copy()
    for a, b in skip:
        ok[max(0, a - 3):b + 4] = False
    speed = np.linalg.norm(v, axis=1)
    acc_v = np.diff(v, axis=0); acc = np.linalg.norm(acc_v, axis=1)            # acc[i] between frames i and i+1
    ok_a = ok[1:] & ok[:-1]
    jerk = np.linalg.norm(np.diff(acc_v, axis=0), axis=1); ok_j = ok_a[1:] & ok_a[:-1]
    loc = np.maximum(speed[1:], speed[:-1])
    jumps = [int(i + 1) for i in np.where(ok_a & (acc > 0.25 * loc + 2.0))[0]]
    hold = ok_a & (loc < 2.0)
    rev = (np.sum(v[1:, :2] * v[:-1, :2], 1) < 0) & hold & (np.linalg.norm(v[1:, :2], axis=1) > 0.15)
    pct = lambda x, q: round(float(np.percentile(x, q)), 2) if len(x) else None
    moves = [m for m in c.get("moves", []) if m.get("frame", m.get("f", 0)) < n]
    att = [m.get("attack") for m in moves if m.get("attack") is not None]; rel = [m.get("release") for m in moves if m.get("release") is not None]
    return {
        "frames": int(n), "fitted": int(ok.sum()),
        "speed_p50_p95": [pct(speed[ok], 50), pct(speed[ok], 95)],
        "accel_p50_p95_p99_max": [pct(acc[ok_a], 50), pct(acc[ok_a], 95), pct(acc[ok_a], 99), pct(acc[ok_a], 100)],
        "jerk_p50_p95_p99_max": [pct(jerk[ok_j], 50), pct(jerk[ok_j], 95), pct(jerk[ok_j], 99), pct(jerk[ok_j], 100)],
        "jumps": len(jumps), "jump_frames": jumps[:60],
        "hold_frames": int(hold.sum()), "hold_jitter_accel_mean": round(float(acc[hold].mean()), 3) if hold.any() else None,
        "hold_reversal_share": round(float(rev.sum() / max(1, hold.sum())), 3),
        "moves": len(moves), "attack_med": pct(np.array(att, float), 50) if att else None, "release_med": pct(np.array(rel, float), 50) if rel else None,
    }


def main():
    ff, vid, out = sys.argv[1:4]
    n = int(sys.argv[sys.argv.index("--frames") + 1]) if "--frames" in sys.argv else 10 ** 9
    skip = []
    if "--skip" in sys.argv:
        for w in sys.argv[sys.argv.index("--skip") + 1].split(","):
            a, b = w.split("-"); skip.append((int(a), int(b)))
    if not os.path.exists(out + "_cam.npz"):
        subprocess.run([sys.executable, "-I", CM, ff, vid, out, "--threads", "4"], check=True, capture_output=True)
    res = analyse(out + "_cam.npz", out + "_cam.json", min(n, len(np.load(out + "_cam.npz")["tx"])), skip)
    print(json.dumps(res))
    if "--json" in sys.argv: json.dump(res, open(sys.argv[sys.argv.index("--json") + 1], "w"), indent=1)
    if "--ref" in sys.argv:
        ref = json.load(open(sys.argv[sys.argv.index("--ref") + 1]))
        for k in ["accel_p50_p95_p99_max", "jerk_p50_p95_p99_max", "jumps", "hold_jitter_accel_mean", "hold_reversal_share", "attack_med", "release_med"]:
            print(f"{k:28s} ref {ref.get(k)}   this {res.get(k)}")


if __name__ == "__main__":
    main()
