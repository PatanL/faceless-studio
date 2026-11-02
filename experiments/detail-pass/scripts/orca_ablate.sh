#!/usr/bin/env bash
# Run ON THE SPARK after orca_stills.sh (uses its bundle): D4 / D5 / specks with one system off at a time.
#   FRAME=60 KEYS="none micro ..." bash scripts/orca_ablate.sh
set -euo pipefail
export CUDA_VISIBLE_DEVICES=""; source ~/.nvm/nvm.sh >/dev/null; nvm use 22 >/dev/null; export PATH="$HOME/studio/bin:$PATH"
cd "$(dirname "$0")/.."; rm -rf out/oablate; mkdir -p out/oablate
F=${FRAME:-60}
exec 9>~/studio/locks/render.lock; flock -w 3600 9
for k in ${KEYS:-none micro schools midreef front farkelp backkelp far seabed singles farfish fore orca light}; do
  nice -n 10 npx remotion still build OrcaOpenDetail "out/oablate/off_$k.png" --frame=$F --props="{\"off\":[\"$k\"]}" --log=error 9>&-
done
exec 9>&-
bash scripts/still_metrics.sh out/oablate/off_*.png 2>&1 | grep -E "D4|per_frame"
