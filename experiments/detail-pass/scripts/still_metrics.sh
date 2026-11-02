#!/usr/bin/env bash
# Run ON THE SPARK: quick D1-D5 + specks + calm + palette on PNG stills (iteration loop before a full render).
#   bash scripts/still_metrics.sh <png> [<png> ...]
set -euo pipefail
export CUDA_VISIBLE_DEVICES="" OMP_NUM_THREADS=2
cd "$(dirname "$0")/.."
T=../kurz-style/tools; PY="nice -n 10 $HOME/studio/venvs/r2/bin/python -I"
d=$(mktemp -d); mkdir -p "$d/g"
for p in "$@"; do $HOME/studio/bin/ffmpeg -v error -y -i "$p" -q:v 3 "$d/g/$(basename "${p%.png}").jpg"; done
$PY $T/tis/frame_metrics.py "$d/g" "$d/fm.json" >/dev/null
$PY - "$d/fm.json" <<'PY'
import json,sys
for k,v in json.load(open(sys.argv[1])).items(): print(f"{k:28s} D4 edge {v['edge_den']:.4f}  D5 outline {v['outline']:.3f}  top-cluster {v['palette'][0]['cov']}")
PY
$PY $T/tis/density.py "$d"/g/*.jpg
$PY tools/specks.py "$d/g"; $PY tools/calm.py "$d/g"
$PY $T/house/palette_check.py ../kurz-style/house/palette.json "$d"/g/*.jpg | tail -n +1 | head -12
rm -rf "$d"
