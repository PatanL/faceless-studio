#!/usr/bin/env bash
# Side-by-side (reference left, remake right, reference audio) + a 12-pair frame sheet. Runs on the Spark.
#   ssh dgx-spark 'bash ~/studio/app/experiments/tis-remake/tools/compare.sh v1'
# INTERNAL BENCHMARK ONLY: outputs stay in experiments/tis-remake/out/ (git-ignored).
set -euo pipefail
V="${1:-v1}"
R=~/studio/refs/tis-ak12/ref.mp4
APP=~/studio/app/experiments/tis-remake
M=$APP/remotion/out/remake_$V.mp4
O=$APP/out; mkdir -p "$O/pairs_$V"
F=~/studio/bin/ffmpeg
FONT=$APP/remotion/public/fonts/K2D-Medium.ttf
export CUDA_VISIBLE_DEVICES=""
nice -n 10 $F -v error -y -threads 4 -i "$R" -i "$M" -filter_complex \
  "[0:v]scale=540:960,setsar=1[a];[1:v]scale=540:960,setsar=1[b];[a][b]hstack=inputs=2[v]" -map "[v]" -map 0:a -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -c:a aac -b:a 160k -shortest "$O/side_by_side_$V.mp4"
# 12 paired frames (ref | remake), labelled with Pillow (the static ffmpeg has no drawtext)
TIMES="1.25 3.5 6.5 12.0 14.5 20.5 23.0 27.0 33.0 37.0 45.0 54.75"
i=0
for T in $TIMES; do
  n=$(printf '%02d' $i)
  $F -v error -y -ss $T -i "$R" -frames:v 1 -vf scale=360:640 "$O/pairs_$V/r_$n.png"
  $F -v error -y -ss $T -i "$M" -frames:v 1 -vf scale=360:640 "$O/pairs_$V/m_$n.png"
  i=$((i+1))
done
python3 - "$O/pairs_$V" "$O/pairs_${V}_sheet.jpg" "$FONT" "$V" $TIMES <<'PY'
import sys
from PIL import Image, ImageDraw, ImageFont
d, out, font, v, *times = sys.argv[1:]
f = ImageFont.truetype(font, 24)
W, H, G = 360, 640, 10
sheet = Image.new('RGB', (4 * (2 * W + G) + G, 3 * (H + G) + G), (24, 24, 24))
for i, t in enumerate(times):
    x0 = G + (i % 4) * (2 * W + G); y0 = G + (i // 4) * (H + G)
    for k, (pre, lab) in enumerate((('r', f'ref {t}s'), ('m', f'remake {v} {t}s'))):
        im = Image.open(f'{d}/{pre}_{i:02d}.png').convert('RGB')
        dr = ImageDraw.Draw(im); bb = dr.textbbox((10, 8), lab, font=f)
        dr.rectangle((bb[0] - 6, bb[1] - 4, bb[2] + 6, bb[3] + 4), fill=(0, 0, 0)); dr.text((10, 8), lab, font=f, fill=(255, 255, 255))
        sheet.paste(im, (x0 + k * W, y0))
sheet.save(out, quality=88)
PY
ls -la "$O"
