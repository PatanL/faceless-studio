#!/usr/bin/env bash
# Run ON THE SPARK from experiments/kurz-style/engine: cost breakdown of the Showcase. Renders frames 0-59
# with one system switched off at a time (src/lib/flags.ts), concurrency 4, nice 10, from one bundle.
set -euo pipefail
export CUDA_VISIBLE_DEVICES=""
source ~/.nvm/nvm.sh >/dev/null; nvm use 22 >/dev/null
export PATH="$HOME/studio/bin:$PATH"
cd "$(dirname "$0")/.."
mkdir -p out/prof ~/studio/locks
exec 9>~/studio/locks/render.lock; flock -w 5400 9
nice -n 10 npx remotion bundle src/index.ts --out-dir build --log=error 9>&-
printf 'variant\tseconds_60f\tload1\n' > out/profile.tsv
for v in ${VARIANTS:-none gap blur stipple shade caustics screen none}; do
  P=$(python3 -c "import json,sys; v=sys.argv[1]; print(json.dumps({'off': [] if v=='none' else v.split(',')}))" "$v")
  S=$(date +%s.%N)
  nice -n 10 npx remotion render build Showcase "out/prof/$v.mp4" --frames=0-59 --concurrency=4 --muted --props="$P" --log=error 9>&-
  E=$(date +%s.%N)
  printf '%s\t%.1f\t%s\n' "$v" "$(echo "$E - $S" | bc)" "$(cut -d' ' -f1 /proc/loadavg)" | tee -a out/profile.tsv
done
