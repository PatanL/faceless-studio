#!/usr/bin/env bash
# Style-study frame extraction (runs on the Spark, CPU only).
#   extract.sh <video> <outdir>
# Writes:
#   <outdir>/grid/g_00001.jpg ...   full-res frame every 2 s (g_N is t = 2*(N-1) s)
#   <outdir>/scenes.txt             hard-cut times (scdet score >= 10 on a 320 px proxy)
#   <outdir>/freeze.txt             freezedetect: stretches with no visible change >= 1 s
# Two separate ffmpeg passes (a split graph with a starved null output stalls).
# Dense 0.25 s stretches are cut separately with dense.sh once stretches are picked.
set -euo pipefail
export CUDA_VISIBLE_DEVICES=""
FF=${FFMPEG:-$HOME/studio/bin/ffmpeg}
v="$1"; out="$2"; mkdir -p "$out/grid"
nice -n 10 "$FF" -hide_banner -loglevel error -threads 3 -i "$v" -an -vf fps=0.5 -q:v 3 "$out/grid/g_%05d.jpg" &
nice -n 10 "$FF" -hide_banner -loglevel info -threads 3 -i "$v" -an \
  -vf "scale=320:-2,scdet=threshold=10,freezedetect=n=0.003:d=1" -f null - 2> "$out/ffmpeg.log" &
wait
tr '\r' '\n' < "$out/ffmpeg.log" | grep -o 'lavfi.scd.time: [0-9.]*' | awk '{print $2}' > "$out/scenes.txt" || true
tr '\r' '\n' < "$out/ffmpeg.log" | grep -oE 'freeze_(start|duration|end): [0-9.]+' > "$out/freeze.txt" || true
echo "grid frames: $(ls "$out/grid" | wc -l)  cuts: $(wc -l < "$out/scenes.txt")  freezes: $(grep -c duration "$out/freeze.txt")"
