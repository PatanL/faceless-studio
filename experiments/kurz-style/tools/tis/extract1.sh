#!/usr/bin/env bash
# extract1.sh <video> <outdir>  -- single-decode variant for long videos:
# full-res frame every 2 s + per-frame scene scores (160 px) in one pass.
set -euo pipefail
export CUDA_VISIBLE_DEVICES=""
FF=${FFMPEG:-$HOME/studio/bin/ffmpeg}
v="$1"; out="$2"; mkdir -p "$out/grid"
nice -n 10 "$FF" -hide_banner -loglevel error -threads 4 -i "$v" -an -filter_complex \
  "[0:v]split=2[a][b];[a]fps=0.5[a1];[b]scale=160:-2,select='gte(scene,0)',metadata=print:key=lavfi.scene_score:file=$out/scores.raw[b1]" \
  -map "[a1]" -q:v 3 "$out/grid/g_%05d.jpg" -map "[b1]" -f null -
paste -d' ' <(grep -o 'pts_time:[0-9.]*' "$out/scores.raw" | cut -d: -f2) <(grep -o 'scene_score=[0-9.]*' "$out/scores.raw" | cut -d= -f2) > "$out/scores.txt"
rm -f "$out/scores.raw"; echo "grid frames: $(ls "$out/grid" | wc -l)  score lines: $(wc -l < "$out/scores.txt")"
