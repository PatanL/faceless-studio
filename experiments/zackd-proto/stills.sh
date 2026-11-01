#!/usr/bin/env bash
# On the Spark: bundle once, then render the given frames as PNG stills (CPU, niced).
# usage: bash stills.sh 0 60 120 ...
set -euo pipefail
cd "$(dirname "$0")"
export CUDA_VISIBLE_DEVICES=""
source ~/.nvm/nvm.sh >/dev/null; nvm use 22 >/dev/null
export PATH="$HOME/studio/bin:$PATH"
mkdir -p out/stills
nice -n 10 npx remotion bundle src/index.ts --out-dir=out/bundle --log=error >/dev/null
for f in "$@"; do
  s=$(date +%s.%N)
  nice -n 10 npx remotion still out/bundle ZackdProto "out/stills/f$(printf %03d "$f").png" --frame="$f" --gl=swangle --log=error >/dev/null
  echo "frame $f $(echo "$(date +%s.%N) - $s" | bc) s"
done
