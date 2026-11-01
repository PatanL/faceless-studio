#!/usr/bin/env bash
# Render a few frames of the remake as half-size JPEGs + one contact sheet. Runs on the Spark.
#   bash stills.sh <tag> <frame> [frame...]   -> out/dbg/<tag>.jpg
set -euo pipefail
TAG="$1"; shift
APP=~/studio/app/experiments/tis-remake
cd $APP/remotion
source ~/.nvm/nvm.sh >/dev/null; nvm use 22 >/dev/null
export PATH=$HOME/studio/bin:$PATH CUDA_VISIBLE_DEVICES=""
D=$APP/out/dbg/$TAG; rm -rf "$D"; mkdir -p "$D"
nice -n 10 node tools/stills.mjs "$D" "$@" >/dev/null
python3 - "$D" "$APP/out/dbg/$TAG.jpg" "$@" <<'PY'
import sys, glob
from PIL import Image, ImageDraw
d, out, *fr = sys.argv[1:]
fs = sorted(glob.glob(d + '/s_*.jpeg'))
ims = [Image.open(f) for f in fs]
w, h = ims[0].size
cols = min(len(ims), 5); rows = (len(ims) + cols - 1) // cols
s = Image.new('RGB', (cols * w, rows * h), (20, 20, 20))
for i, (im, f) in enumerate(zip(ims, fr)):
    dr = ImageDraw.Draw(im); dr.rectangle((0, 0, 120, 30), fill=(0, 0, 0)); dr.text((6, 8), f'{f} {int(f)/30:.2f}s', fill=(255, 255, 255))
    s.paste(im, ((i % cols) * w, (i // cols) * h))
s.save(out, quality=85)
PY
echo $APP/out/dbg/$TAG.jpg
