"""Ghost check for scene joins (our own code). Does a join ever show two places semi-transparently over each other?

usage: python -I ghost_check.py <ffmpeg> <video> <windows.json> <out.json> [--k 1] [--control]

windows.json: {"windows": [{"group", "kind", "from", "to", "t0f"}]} (absolute frames; plan_kitlab.ts writes it).
For every frame j inside a window, with A = the last frame before the window and B = the first frame after it, each
pixel (gray, 135x240) where A and B differ by > 0.12 gets alpha = (F_j - B) / (A - B). A pixel is "mixed" (a ghost
pixel) when 0.25 < alpha < 0.75 and F_j is within 0.06 of the blend alpha*A + (1-alpha)*B. Per frame:
mixed_share = mixed pixels / differing pixels. A cross-dissolve's middle frames read ~0.6-0.9; a hard-edged reveal
reads only its feathered rim. The camera keeps moving through a join, so A and B are not exact; 135x240 keeps the
motion under ~1 px and the estimate is an upper bound.
Also runs the global blend detector (frame j ~ a*F(j-5) + (1-a)*F(j+5), the dissolve test from
research/references/STORY_LANE_TUTORIAL_CHECK.md) over the whole video and lists the blend frames.
--control: also builds a synthetic 7-frame cross-dissolve between each window's A and B and reports its score, so
the numbers have a ruler.
"""
import sys, json, subprocess
import numpy as np

W, H = 135, 240


def frames(ff, vid):
    p = subprocess.run([ff, "-v", "error", "-i", vid, "-vf", f"scale={W}:{H}:flags=area,format=gray", "-f", "rawvideo", "-"],
                       capture_output=True, check=True)
    a = np.frombuffer(p.stdout, np.uint8).reshape(-1, H, W).astype(np.float32) / 255.0
    # the caption band (0.62-0.80 of the height) is masked: captions swap on words, not on joins
    a[:, int(0.62 * H):int(0.80 * H), :] = np.nan
    return a


def mixed_share(Fj, A, B):
    d = A - B
    m = np.isfinite(d) & (np.abs(d) > 0.12)
    if m.sum() < 50:
        return 0.0, int(m.sum())
    al = (Fj[m] - B[m]) / d[m]
    fit = np.abs(Fj[m] - (al * A[m] + (1 - al) * B[m])) < 0.06
    mix = (al > 0.25) & (al < 0.75) & fit
    return float(mix.mean()), int(m.sum())


def blend_frames(F, k=5):
    out = []
    for j in range(k, len(F) - k):
        a, b, c = F[j - k], F[j + k], F[j]
        m = np.isfinite(a)
        x, y, z = a[m], b[m], c[m]
        dab = np.abs(x - y).mean()
        if dab < 0.06:
            continue
        den = ((x - y) ** 2).sum()
        al = float(((z - y) * (x - y)).sum() / max(den, 1e-6))
        if not 0.2 < al < 0.8:
            continue
        res = np.abs(z - (al * x + (1 - al) * y)).mean()
        if res < 0.5 * min(np.abs(z - x).mean(), np.abs(z - y).mean()):
            out.append(j)
    return out


def main():
    ff, vid, wpath, opath = sys.argv[1:5]
    control = "--control" in sys.argv
    F = frames(ff, vid)
    wins = json.load(open(wpath))["windows"]
    rows = []
    for w in wins:
        a, b = max(0, w["from"] - 1), min(len(F) - 1, w["to"])
        A, B = F[a], F[b]
        sh = [mixed_share(F[j], A, B)[0] for j in range(a + 1, b)]
        row = {"group": w["group"], "kind": w["kind"], "frames": [a + 1, b - 1], "n": len(sh),
               "mixed_max": round(max(sh), 3) if sh else 0, "mixed_mean": round(float(np.mean(sh)), 3) if sh else 0,
               "per_frame": [round(x, 3) for x in sh]}
        if control:
            n = 7
            ctl = [mixed_share((1 - (i + 1) / (n + 1)) * A + ((i + 1) / (n + 1)) * B, A, B)[0] for i in range(n)]
            row["control_dissolve_max"] = round(max(ctl), 3)
        rows.append(row)
    bl = blend_frames(F)
    out = {"video": vid, "frames": len(F), "windows": rows, "global_blend_frames": bl, "n_global_blend": len(bl)}
    json.dump(out, open(opath, "w"), indent=1)
    for r in rows:
        print(f"{r['group']:12s} {r['kind']:6s} frames {r['frames']} mixed max {r['mixed_max']:.3f} mean {r['mixed_mean']:.3f}"
              + (f"  (control dissolve max {r['control_dissolve_max']:.3f})" if control else ""))
    print("global blend frames:", len(bl), bl[:40])


if __name__ == "__main__":
    main()
