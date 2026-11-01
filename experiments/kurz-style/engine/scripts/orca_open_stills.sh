#!/usr/bin/env bash
# Run ON THE SPARK from experiments/kurz-style/engine: bundle and render OrcaOpen proof stills (CPU, niced, render lock).
# usage: bash scripts/orca_open_stills.sh <tag> [frames...]
set -euo pipefail
export CUDA_VISIBLE_DEVICES=""
source ~/.nvm/nvm.sh >/dev/null; nvm use 22 >/dev/null
export PATH="$HOME/studio/bin:$PATH"
cd "$(dirname "$0")/.."
TAG=${1:-v1}; shift || true
FRAMES=${*:-0 45 75 110 125 165 200 240 270 285}
mkdir -p out/oo_stills/$TAG ~/studio/locks
exec 9>~/studio/locks/render.lock
flock -w 3600 9
nice -n 10 npx remotion bundle src/index.ts --out-dir build --log=error 9>&-
for f in $FRAMES; do
  nice -n 10 npx remotion still build OrcaOpen "out/oo_stills/$TAG/f$(printf %03d "$f").png" --frame="$f" --log=error 9>&- &
  while [ "$(jobs -r | wc -l)" -ge 3 ]; do wait -n; done
done
wait
ls out/oo_stills/$TAG
