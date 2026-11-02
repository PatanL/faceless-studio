#!/usr/bin/env bash
# Run ON THE SPARK after stills.sh (uses its bundle): D4 / specks with one system off at a time, frame 60.
set -euo pipefail
export CUDA_VISIBLE_DEVICES=""; source ~/.nvm/nvm.sh >/dev/null; nvm use 22 >/dev/null; export PATH="$HOME/studio/bin:$PATH"
cd "$(dirname "$0")/.."; mkdir -p out/ablate
exec 9>~/studio/locks/render.lock; flock -w 3600 9
for k in ${KEYS:-none micro schools midreef front kelp far turtle seabed singles farfish fore}; do
  nice -n 10 npx remotion still build DetailShowcase "out/ablate/off_$k.png" --frame=60 --props="{\"off\":[\"$k\"]}" --log=error 9>&-
done
exec 9>&-
bash scripts/still_metrics.sh out/ablate/off_*.png 2>&1 | grep -E "D4|median|per_frame" 
