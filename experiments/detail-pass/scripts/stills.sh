#!/usr/bin/env bash
# Run ON THE SPARK: typecheck, bundle, render proof stills (Sheet, Hero, showcase frames) + quick metrics.
#   bash scripts/stills.sh <tag> [frames...]   (default frames: 0 60 105)
set -euo pipefail
export CUDA_VISIBLE_DEVICES=""
source ~/.nvm/nvm.sh >/dev/null; nvm use 22 >/dev/null
export PATH="$HOME/studio/bin:$PATH"
cd "$(dirname "$0")/.."
tag=$1; shift; FR=${*:-0 60 105}
[ -e node_modules ] || ln -s ../kurz-style/engine/node_modules node_modules
mkdir -p out/stills ~/studio/locks
nice -n 10 npx tsc --noEmit
exec 9>~/studio/locks/render.lock; flock -w 3600 9
rm -rf build; nice -n 10 npx remotion bundle src/index.ts --out-dir build --log=error 9>&-
for s in Sheet Hero; do nice -n 10 npx remotion still build $s "out/stills/${s,,}_$tag.png" --log=error 9>&-; done
P=()
for f in $FR; do o="out/stills/show_${tag}_f$(printf %03d $f).png"; nice -n 10 npx remotion still build DetailShowcase "$o" --frame=$f --log=error 9>&-; P+=("$o"); done
exec 9>&-
bash scripts/still_metrics.sh "${P[@]}"
