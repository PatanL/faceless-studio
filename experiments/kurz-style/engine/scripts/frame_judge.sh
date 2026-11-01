#!/usr/bin/env bash
# Run ON THE SPARK from experiments/kurz-style/engine: the frame half of tools/house/judge_metrics.sh on a short
# clip, sampled every 0.5 s instead of 2 s (a 4 s clip only has 2 frames on the 2 s grid). Prints medians of
# P1-P8 (palette_check), D1/D2 (density), D3 (small specks, judge_summary's cv2 port), D4/D5 (frame_metrics).
#   bash scripts/frame_judge.sh <clip.mp4> <outdir> <label>
set -euo pipefail
export CUDA_VISIBLE_DEVICES="" OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
FF=$HOME/studio/bin/ffmpeg
PY="nice -n 10 $HOME/studio/venvs/r2/bin/python -I"
v="$1"; out="$2"; label="$3"
T="$(cd "$(dirname "$0")/../.." && pwd)/tools"
H="$(cd "$(dirname "$0")/../.." && pwd)/house"
mkdir -p "$out/grid"; rm -f "$out"/grid/*.jpg
nice -n 10 "$FF" -v error -nostdin -y -threads 2 -i "$v" -an -vf fps=2 -q:v 3 "$out/grid/g_%05d.jpg"
$PY "$T/house/palette_check.py" "$H/palette.json" "$out"/grid/*.jpg --json "$out/palette.json" > "$out/palette.txt"
$PY "$T/tis/frame_metrics.py" "$out/grid" "$out/fm.json" > /dev/null
$PY "$T/tis/density.py" "$out"/grid/*.jpg > "$out/density.txt"
$PY - "$out" "$label" <<'PYEOF'
import sys, os, json, glob
import numpy as np, cv2
d, label = sys.argv[1], sys.argv[2]
med = lambda xs: float(np.median(xs))
pc = json.load(open(os.path.join(d, "palette.json")))
fm = json.load(open(os.path.join(d, "fm.json"))).values()
rows = [l.split() for l in open(os.path.join(d, "density.txt")) if l.strip() and not l.startswith("frame")]
sp = []
for f in sorted(glob.glob(os.path.join(d, "grid", "*.jpg"))):
    a = cv2.imread(f).astype(np.float32); L = a @ np.array([.0722, .7152, .2126], np.float32)
    L = cv2.resize(L, (1920, 1080), interpolation=cv2.INTER_AREA) if L.shape[1] != 1920 else L
    small = cv2.resize(L, (L.shape[1] // 4, L.shape[0] // 4), interpolation=cv2.INTER_AREA)
    bg = cv2.resize(cv2.medianBlur(np.clip(small, 0, 255).astype(np.uint8), 15).astype(np.float32), (L.shape[1], L.shape[0]))
    n, lab, st, _ = cv2.connectedComponentsWithStats(((L - bg) > 12).astype(np.uint8), connectivity=8)
    a_ = st[1:, cv2.CC_STAT_AREA]; sp.append(int(((a_ >= 6) & (a_ <= 400)).sum()))
m = {"label": label, "frames": len(sp)}
for k, idn in (("conform", "P1"), ("vm_share", "P2"), ("sat_chroma", "P3"), ("grey", "P4"), ("hue_fam", "P5"), ("near_white", "P6"), ("pure_white", "P7"), ("black", "P8")):
    m[f"{idn}_{k}"] = round(med([r[k] for r in pc]), 4)
m["D1_shapes"] = med([int(r[1]) for r in rows]); m["D2_micro"] = med([int(r[2]) for r in rows])
m["D3_specks"] = med(sp)
m["D4_edge_den"] = round(med([r["edge_den"] for r in fm]), 4); m["D5_outline"] = round(med([r["outline"] for r in fm]), 4)
json.dump(m, open(os.path.join(d, "FRAME_METRICS.json"), "w"), indent=1)
print(json.dumps(m))
PYEOF
