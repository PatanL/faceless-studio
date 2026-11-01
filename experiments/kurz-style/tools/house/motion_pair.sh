#!/usr/bin/env bash
# motion_pair.sh: side-by-side motion evidence for JUDGE_RUBRIC.md (Spark, CPU only).
#   bash tools/house/motion_pair.sh <ours.mp4> <ours_start_s> <ref.mp4> <ref_start_s> <out_prefix> [dur=5]
# Writes:
#   <out_prefix>.mp4        ours (left) | reference (right), 960x540 each, 30 fps, no audio
#   <out_prefix>_strip.jpg  0.25 s strip: 2 rows of ours, then 2 rows of the reference (10 frames per row)
# A 9:16 source is pillarboxed on ink-0 (#01121a) so both sides share one scale.
set -euo pipefail
export CUDA_VISIBLE_DEVICES=""
FF=${FFMPEG:-$HOME/studio/bin/ffmpeg}
o="$1"; os="$2"; r="$3"; rs="$4"; out="$5"; dur="${6:-5}"
fit="fps=30,scale=960:540:force_original_aspect_ratio=decrease,pad=960:540:(ow-iw)/2:(oh-ih)/2:color=0x01121a,setsar=1"
nice -n 10 "$FF" -hide_banner -loglevel error -y -threads 3 -ss "$os" -t "$dur" -i "$o" -ss "$rs" -t "$dur" -i "$r" \
  -filter_complex "[0:v]$fit[a];[1:v]$fit[b];[a][b]hstack=inputs=2" -an -c:v libx264 -crf 20 -pix_fmt yuv420p "$out.mp4"
st="fps=4,scale=384:216:force_original_aspect_ratio=decrease,pad=384:216:(ow-iw)/2:(oh-ih)/2:color=0x01121a,setsar=1,tile=10x2:padding=4:color=0x01121a"
nice -n 10 "$FF" -hide_banner -loglevel error -y -threads 3 -ss "$os" -t "$dur" -i "$o" -ss "$rs" -t "$dur" -i "$r" \
  -filter_complex "[0:v]$st[a];[1:v]$st[b];[a][b]vstack=inputs=2" -frames:v 1 -q:v 3 "${out}_strip.jpg"
echo "$out.mp4 ${out}_strip.jpg"
