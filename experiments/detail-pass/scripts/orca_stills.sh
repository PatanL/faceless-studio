#!/usr/bin/env bash
# Run ON THE SPARK: typecheck, bundle, render OrcaOpenDetail stills at the given frames + quick metrics.
#   bash scripts/orca_stills.sh <tag> [frames...]   (default: the v3 beat frames 0 60 105 150 195 240 288)
set -euo pipefail
export CUDA_VISIBLE_DEVICES=""
source ~/.nvm/nvm.sh >/dev/null; nvm use 22 >/dev/null
export PATH="$HOME/studio/bin:$PATH"
cd "$(dirname "$0")/.."
tag=$1; shift; FR=${*:-0 60 105 150 195 240 288}
[ -e node_modules ] || ln -s ../kurz-style/engine/node_modules node_modules
mkdir -p out/stills ~/studio/locks
nice -n 10 npx tsc --noEmit
exec 9>~/studio/locks/render.lock; echo "[orca-detail] waiting for render lock"; flock -w 3600 9
rm -rf build; nice -n 10 npx remotion bundle src/index.ts --out-dir build --log=error 9>&-
P=()
for f in $FR; do o="out/stills/orca_${tag}_f$(printf %03d $f).png"; nice -n 10 npx remotion still build OrcaOpenDetail "$o" --frame=$f --log=error 9>&-; P+=("$o"); done
exec 9>&-
bash scripts/still_metrics.sh "${P[@]}"
