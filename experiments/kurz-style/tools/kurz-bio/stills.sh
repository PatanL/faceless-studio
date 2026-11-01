#!/bin/bash
# extracts full-res stills; list lines: VIDEO PREFIX SECONDS NAME
mkdir -p stills
while read v p s n; do
  [ -z "$v" ] && continue
  mm=$(printf "%02d%02d" $((s/60)) $((s%60)))
  nice -n 10 ~/studio/bin/ffmpeg -nostdin -loglevel error -threads 2 -ss $s -i $v.mp4 -frames:v 1 -q:v 2 -y stills/${p}_${mm}_${n}.jpg
done < stills.list
ls stills | wc -l
