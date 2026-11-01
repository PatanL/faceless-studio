#!/usr/bin/env bash
# Run ON THE SPARK (CPU, nice 10, 4 threads): burn word-highlight captions over the Blender render and mux the
# Kokoro mix.  usage: tools/composite.sh <base.mp4> <mix.wav> <captions_dir> <dur_s> <out.mp4>
set -euo pipefail
BASE=$1 MIX=$2 CAP=$3 DUR=$4 OUT=$5
Y=$(python3 -c "import json;print(json.load(open('$CAP/segments.json'))['band_y'])")
export CUDA_VISIBLE_DEVICES=""
nice -n 10 ffmpeg -y -loglevel error -threads 4 -i "$BASE" -f concat -safe 0 -i "$CAP/list.txt" -i "$MIX" \
  -filter_complex "[1:v]fps=30,format=rgba[c];[0:v][c]overlay=0:${Y}:eof_action=pass,format=yuv420p[v];[2:a]apad,atrim=0:${DUR}[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -crf 17 -preset medium -profile:v high -c:a aac -b:a 192k -ar 48000 \
  -t "$DUR" -movflags +faststart "$OUT"
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate -of compact "$OUT"
