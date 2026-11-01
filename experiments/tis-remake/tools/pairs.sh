#!/usr/bin/env bash
# Paired ref|remake frames at arbitrary times -> one labelled sheet. Runs on the Spark.
#   bash pairs.sh <version> <out.jpg> <cols> t1 t2 ...
# INTERNAL BENCHMARK ONLY: outputs stay in experiments/tis-remake/out/ (git-ignored).
set -euo pipefail
V="$1"; OUT="$2"; COLS="$3"; shift 3
R=~/studio/refs/tis-ak12/ref.mp4
APP=~/studio/app/experiments/tis-remake
M=$APP/remotion/out/remake_$V.mp4
F=~/studio/bin/ffmpeg
FONT=$APP/remotion/public/fonts/K2D-Medium.ttf
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
export CUDA_VISIBLE_DEVICES=""
i=0
for T in "$@"; do
  n=$(printf '%02d' $i)
  nice -n 10 $F -v error -y -ss $T -i "$R" -frames:v 1 -vf scale=360:640 "$TMP/r_$n.png"
  nice -n 10 $F -v error -y -ss $T -i "$M" -frames:v 1 -vf scale=360:640 "$TMP/m_$n.png"
  i=$((i+1))
done
python3 - "$TMP" "$OUT" "$FONT" "$V" "$COLS" "$@" <<'PY'
import sys
from PIL import Image, ImageDraw, ImageFont
d, out, font, v, cols, *times = sys.argv[1:]
cols = int(cols); rows = (len(times) + cols - 1) // cols
f = ImageFont.truetype(font, 24)
W, H, G = 360, 640, 10
sheet = Image.new('RGB', (cols * (2 * W + G) + G, rows * (H + G) + G), (24, 24, 24))
for i, t in enumerate(times):
    x0 = G + (i % cols) * (2 * W + G); y0 = G + (i // cols) * (H + G)
    for k, (pre, lab) in enumerate((('r', f'ref {t}s'), ('m', f'{v} {t}s'))):
        im = Image.open(f'{d}/{pre}_{i:02d}.png').convert('RGB')
        dr = ImageDraw.Draw(im); bb = dr.textbbox((10, 8), lab, font=f)
        dr.rectangle((bb[0] - 6, bb[1] - 4, bb[2] + 6, bb[3] + 4), fill=(0, 0, 0)); dr.text((10, 8), lab, font=f, fill=(255, 255, 255))
        sheet.paste(im, (x0 + k * W, y0))
sheet.save(out, quality=86)
print(out)
PY
