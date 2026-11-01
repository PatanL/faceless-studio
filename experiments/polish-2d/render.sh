#!/usr/bin/env bash
# Run ON THE SPARK from ~/studio/app/experiments/polish-2d (after rsyncing this folder).
# Renders the first 10 s (frames 0-299) of explainer-orca twice, 9:16, concurrency 4, nice 10, CPU only:
#   out/baseline10.mp4  the live pipeline: studio/src/index.ts "Storyboard" + episodes/explainer-orca/storyboard.json
#   out/polish10.mp4    this experiment: src/index.ts "Polish10"
# plus cost-attribution variants. Both bundles are built first (bundle time is not in the render times).
# The baseline bundle gets a slim public dir holding only mix.wav (the real one is 1.5 GB); frames are unaffected.
# usage: [FRAMES=0-299] [TAG=] bash render.sh [Comp ...]
#   Comp = Base | Kit10 | Kit10NoGrain | Polish10 | Polish10NoLight | Polish10NoDepth | Polish10NoGrain
#   FRAMES=0-1 TAG=_startup measures the fixed per-render cost (Chrome start, metadata), to subtract from 300-frame times
set -euo pipefail
export CUDA_VISIBLE_DEVICES=""
source ~/.nvm/nvm.sh >/dev/null; nvm use 22 >/dev/null
export PATH="$HOME/studio/bin:$PATH"
HERE="$(cd "$(dirname "$0")" && pwd)"
APP="$(cd "$HERE/../.." && pwd)"
cd "$HERE"
[ -e node_modules ] || ln -s ../../studio/node_modules node_modules   # one remotion/react instance for both trees
mkdir -p public out results public-base/episodes/explainer-orca ~/studio/locks
MIX="$APP/studio/public/episodes/explainer-orca/mix.wav"
cp -f "$MIX" public-base/episodes/explainer-orca/mix.wav
[ -f public/grain512.png ] || ffmpeg -v error -y -f lavfi -i "nullsrc=s=512x512,format=gray,geq=lum='128+60*(random(1)-0.5)*2',gblur=sigma=0.7" -frames:v 1 public/grain512.png
nice -n 10 python3 -I audio/make_audio.py "$MIX" "$APP/studio/public/sfx" public > results/audio_report.json

FRAMES="${FRAMES:-0-299}"; TAG="${TAG:-}"
COMPS=("$@")
[ ${#COMPS[@]} -gt 0 ] || COMPS=(Base Polish10 Base Polish10NoLight Polish10NoDepth Base Polish10NoGrain Kit10 Base Polish10)

exec 9>~/studio/locks/render.lock
echo "[polish-2d] waiting for render lock"; flock -w 3600 9
(cd "$APP/studio" && nice -n 10 npx remotion bundle src/index.ts --public-dir "$HERE/public-base" --out-dir "$HERE/build-base" --log=error 9>&-)
nice -n 10 npx remotion bundle src/index.ts --out-dir build --log=error 9>&-

[ -f results/times.tsv ] || printf 'comp\tseconds\tload1_start\tload1_end\tstatus\twhen_utc\n' > results/times.tsv
for c in "${COMPS[@]}"; do
  L=$(cut -d' ' -f1 /proc/loadavg); S=$(date +%s.%N)
  if [ "$c" = Base ]; then
    OUTF="$HERE/out/baseline10$TAG.mp4"
    ( cd "$APP/studio" && nice -n 10 npx remotion render "$HERE/build-base" Storyboard "$OUTF" \
        --props="$APP/episodes/explainer-orca/storyboard.json" --frames="$FRAMES" --concurrency=4 --log=error 9>&- ) >"out/$c.log" 2>&1 && ST=ok || ST=FAIL
  else
    OUTF="$HERE/out/$(echo "$c" | tr 'A-Z' 'a-z')$TAG.mp4"
    nice -n 10 npx remotion render build "$c" "$OUTF" --frames="$FRAMES" --concurrency=4 --log=error 9>&- >"out/$c.log" 2>&1 && ST=ok || ST=FAIL
  fi
  E=$(date +%s.%N)
  printf '%s\t%.1f\t%s\t%s\t%s\t%s\n' "$c$TAG" "$(echo "$E - $S" | bc)" "$L" "$(cut -d' ' -f1 /proc/loadavg)" "$ST" "$(date -u +%H:%M:%S)" | tee -a results/times.tsv
done
ls -la out/*.mp4
