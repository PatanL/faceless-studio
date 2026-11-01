#!/usr/bin/env bash
# Run ON THE SPARK after render.sh: A/B side-by-side (left = live pipeline, right = polish, polish audio),
# a still sheet at matched times, and per-frame strips of the car drops (frames 206-225).
set -euo pipefail
export PATH="$HOME/studio/bin:$PATH"
cd "$(dirname "$0")/out"
ffmpeg -nostdin -v error -y -i baseline10.mp4 -i polish10.mp4 \
  -filter_complex "[0:v]scale=540:960[a];[1:v]scale=540:960[b];[a][b]hstack" \
  -map 1:a -c:v libx264 -crf 20 -preset veryfast -threads 4 -c:a aac ab_side_by_side.mp4
rm -f ab_t*.jpg
i=0
for t in 0.0 1.5 2.6 5.6 7.1 7.6 8.4; do
  ffmpeg -nostdin -v error -y -ss "$t" -i ab_side_by_side.mp4 -frames:v 1 -vf scale=540:480 "ab_t$i.jpg"; i=$((i+1))
done
ffmpeg -nostdin -v error -y -i ab_t%d.jpg -vf tile=1x7 -frames:v 1 ab_sheet.jpg
for v in baseline10 polish10; do
  ffmpeg -nostdin -v error -y -i "$v.mp4" -vf "select='between(n,206,225)',crop=1080:420:0:960,scale=360:140,tile=4x5" -frames:v 1 "strip_$v.jpg"
done
ls -la ab_side_by_side.mp4 ab_sheet.jpg strip_*.jpg
