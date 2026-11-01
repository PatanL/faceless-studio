#!/usr/bin/env bash
# Run ON THE SPARK from experiments/kurz-style/engine: bundle once and render proof stills (CPU, niced, lock).
# usage: bash scripts/stills.sh [frames for Showcase, default "0 60 119"]
set -euo pipefail
export CUDA_VISIBLE_DEVICES=""
source ~/.nvm/nvm.sh >/dev/null; nvm use 22 >/dev/null
export PATH="$HOME/studio/bin:$PATH"
cd "$(dirname "$0")/.."
mkdir -p out/stills ~/studio/locks
FRAMES=${*:-0 60 119}
exec 9>~/studio/locks/render.lock
flock -w 3600 9
nice -n 10 npx remotion bundle src/index.ts --out-dir build --log=error 9>&-
nice -n 10 npx remotion still build ShadingLadder out/stills/ladder.png --log=error 9>&-
nice -n 10 npx remotion still build Assets out/stills/assets.png --log=error 9>&-
for f in $FRAMES; do
  nice -n 10 npx remotion still build Showcase "out/stills/show_f$(printf %03d "$f").png" --frame="$f" --log=error 9>&-
done
ls -la out/stills
