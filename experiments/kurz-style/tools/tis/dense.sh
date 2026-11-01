#!/usr/bin/env bash
# dense.sh <video> <outdir> <label> <start_s> [dur_s=5]
# Writes <outdir>/dense_<label>/d_XX.jpg (every 0.25 s, full res) and
#        <outdir>/dense_<label>/full/f_XXX.png (every source frame, 640 px) for motion curves.
set -euo pipefail
export CUDA_VISIBLE_DEVICES=""
FF=${FFMPEG:-$HOME/studio/bin/ffmpeg}
v="$1"; out="$2/dense_$3"; ss="$4"; dur="${5:-5}"; mkdir -p "$out/full"
nice -n 10 "$FF" -hide_banner -loglevel error -threads 2 -ss "$ss" -t "$dur" -i "$v" -vf fps=4 -q:v 2 "$out/d_%02d.jpg"
nice -n 10 "$FF" -hide_banner -loglevel error -threads 2 -ss "$ss" -t "$dur" -i "$v" -vf scale=640:-2 "$out/full/f_%03d.png"
echo "$3 @ ${ss}s: $(ls "$out" | grep -c d_) dense, $(ls "$out/full" | wc -l) full-rate"
