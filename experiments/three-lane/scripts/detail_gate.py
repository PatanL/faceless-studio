"""Detail density by region (our own code; visual track round 3, owner: "theirs has far more detail, on the objects viewers
look at and in the background").

usage: python3 -I detail_gate.py <ffmpeg> <video> [--frames a-b] [--every N] [--ref ref.json] [--json out.json]
       [--boxes boxes.json]   per-frame hero boxes {"frame": [x0, y0, x1, y1]} (fractions); default: a centre box

Regions per frame (360x640 grey; the caption band 0.64-0.78 is masked out of every region):
  hero        the box the viewer looks at (default x 0.22-0.78, y 0.18-0.70)
  background  outside the hero box, above y 0.42 (walls, windows, sky, skyline)
  midground   everything else outside the hero box (floor, props, side figures)
Measures per region:
  edge        share of Canny edge pixels (60 / 140), the ink and the drawn detail
  texture     mean |Laplacian| (fine surface detail: engraving, scales, weave, brickwork)
  busy        share of 8 px blocks whose std > 12 (how much of the region carries any detail at all)
--ref compares with a reference run of the same tool: a region fails when its median edge or texture is under 80 % of
the reference's median (the gate; VS1Z ranges in out/study/VS1Z/detail_ref.json). Exit 1 on a failure.
"""
import json, subprocess, sys
import numpy as np, cv2

W, H = 360, 640


def frames(ff, vid, a, b, every):
    p = subprocess.run([ff, "-v", "error", "-i", vid, "-vf", f"select='between(n\\,{a}\\,{b})*not(mod(n-{a}\\,{every}))',scale={W}:{H}:flags=area,format=gray", "-vsync", "0", "-f", "rawvideo", "-"], capture_output=True)
    return np.frombuffer(p.stdout, np.uint8).reshape(-1, H, W), list(range(a, b + 1, every))


def masks(box):
    x0, y0, x1, y1 = box
    hero = np.zeros((H, W), bool); hero[int(y0 * H):int(y1 * H), int(x0 * W):int(x1 * W)] = True
    cap = np.zeros((H, W), bool); cap[int(0.64 * H):int(0.78 * H)] = True
    top = np.zeros((H, W), bool); top[:int(0.42 * H)] = True
    return {"hero": hero & ~cap, "background": top & ~hero & ~cap, "midground": ~top & ~hero & ~cap}


def measure(g, m):
    e = cv2.Canny(g, 60, 140) > 0
    lap = np.abs(cv2.Laplacian(g.astype(np.float32), cv2.CV_32F))
    bs = 8; blk = g[:H - H % bs, :W - W % bs].reshape(H // bs, bs, W // bs, bs).std(axis=(1, 3)) > 12
    mb = m[:H - H % bs, :W - W % bs].reshape(H // bs, bs, W // bs, bs).mean(axis=(1, 3)) > 0.5
    return {"edge": float(e[m].mean()), "texture": float(lap[m].mean()), "busy": float(blk[mb].mean()) if mb.any() else 0.0}


def main():
    ff, vid = sys.argv[1:3]
    a, b = (map(int, sys.argv[sys.argv.index("--frames") + 1].split("-")) if "--frames" in sys.argv else (0, 599))
    every = int(sys.argv[sys.argv.index("--every") + 1]) if "--every" in sys.argv else 10
    boxes = json.load(open(sys.argv[sys.argv.index("--boxes") + 1])) if "--boxes" in sys.argv else {}
    F, idx = frames(ff, vid, a, b, every)
    rows = []
    for g, f in zip(F, idx):
        box = boxes.get(str(f), [0.22, 0.18, 0.78, 0.70])
        rows.append({"frame": f, **{f"{rg}_{k}": v for rg, msk in masks(box).items() for k, v in measure(g, msk).items()}})
    keys = [k for k in rows[0] if k != "frame"]
    summ = {k: [round(float(np.percentile([r[k] for r in rows], q)), 4) for q in (25, 50, 75)] for k in keys}
    out = {"video": vid, "frames": len(rows), "p25_50_75": summ, "rows": rows}
    fails = []
    if "--ref" in sys.argv:
        ref = json.load(open(sys.argv[sys.argv.index("--ref") + 1]))["p25_50_75"]
        for k in keys:
            if k.endswith(("_edge", "_texture")) and summ[k][1] < 0.8 * ref[k][1]:
                fails.append(f"detail: {k} median {summ[k][1]} < 80 % of the reference median {ref[k][1]}")
        out["vs_ref"] = {k: {"ref_p25_50_75": ref[k], "this_p25_50_75": summ[k]} for k in keys}
    out["failures"] = fails
    print(json.dumps({"p25_50_75": summ, "failures": fails}, indent=1))
    if "--json" in sys.argv: json.dump(out, open(sys.argv[sys.argv.index("--json") + 1], "w"), indent=1)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
