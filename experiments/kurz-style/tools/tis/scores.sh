#!/usr/bin/env bash
# scores.sh <video> <out.txt> [ss] [t]
# Per-frame ffmpeg scene score (0..1) on a 160 px proxy: "pts_time score" per line.
# cuts.py turns these into a cut list / shot-length stats.
set -euo pipefail
export CUDA_VISIBLE_DEVICES=""
FF=${FFMPEG:-$HOME/studio/bin/ffmpeg}
v="$1"; out="$2"; rng=()
[ $# -ge 4 ] && rng=(-ss "$3" -t "$4")
nice -n 10 "$FF" -hide_banner -loglevel error -threads 3 "${rng[@]}" -i "$v" -an \
  -vf "scale=160:-2,select='gte(scene,0)',metadata=print:key=lavfi.scene_score:file=$out.raw" -f null -
paste -d' ' <(grep -o 'pts_time:[0-9.]*' "$out.raw" | cut -d: -f2) <(grep -o 'scene_score=[0-9.]*' "$out.raw" | cut -d= -f2) > "$out"
rm -f "$out.raw"; wc -l "$out"
