#!/usr/bin/env bash
# Run ON THE SPARK from experiments/kurz-style/engine. Renders the 4 s engine Showcase and, for comparison,
# the first 4 s (frames 0-119) of the current kit's orca pilot (studio/ Storyboard + episodes/explainer-orca),
# both 1080x1920 30 fps, --concurrency=4, muted, nice 10, CPU only (swangle), from pre-built bundles, alternating
# E B E B so load drift hits both. Then the texture pass (ffmpeg deband + dither) on the showcase.
# Output: out/bench.tsv, out/showcase.mp4, out/showcase_tex.mp4, out/baseline_orca_4s.mp4
set -euo pipefail
export CUDA_VISIBLE_DEVICES=""
source ~/.nvm/nvm.sh >/dev/null; nvm use 22 >/dev/null
export PATH="$HOME/studio/bin:$PATH"
ENG="$(cd "$(dirname "$0")/.." && pwd)"
APP="$HOME/studio/app"
TMP="$HOME/studio/tmp/kurz-engine-bench"
mkdir -p "$ENG/out" "$TMP" ~/studio/locks
exec 9>~/studio/locks/render.lock
echo "[bench] waiting for render lock"; flock -w 5400 9
cd "$ENG"
nice -n 10 npx remotion bundle src/index.ts --out-dir build --log=error 9>&-
( cd "$APP/studio" && nice -n 10 npx remotion bundle src/index.ts --out-dir "$TMP/studio-build" --log=error 9>&- )
[ -f out/bench.tsv ] || printf 'what\tseconds\tvideo_s\ts_per_video_s\tload1_start\tload1_end\n' > out/bench.tsv
run() { # name video_seconds cmd...
  local name=$1 vs=$2; shift 2
  local L0; L0=$(cut -d' ' -f1 /proc/loadavg)
  local S; S=$(date +%s.%N)
  "$@" 9>&- >"out/$name.log" 2>&1
  local E; E=$(date +%s.%N)
  local D; D=$(echo "$E - $S" | bc)
  printf '%s\t%.1f\t%s\t%.2f\t%s\t%s\n' "$name" "$D" "$vs" "$(echo "$D / $vs" | bc -l)" "$L0" "$(cut -d' ' -f1 /proc/loadavg)" | tee -a out/bench.tsv
}
ENGINE=(nice -n 10 npx remotion render build Showcase out/showcase.mp4 --concurrency=4 --muted --log=error)
BASE=(bash -c "cd '$APP/studio' && nice -n 10 npx remotion render '$TMP/studio-build' Storyboard '$ENG/out/baseline_orca_4s.mp4' --props='$APP/episodes/explainer-orca/storyboard.json' --frames=0-119 --concurrency=4 --muted --log=error")
for i in 1 2; do
  run "engine_showcase_r$i" 4 "${ENGINE[@]}"
  run "baseline_kit_orca_r$i" 4 "${BASE[@]}"
done
# 2 s runs: (t_120f - t_60f) / 2 s = marginal render seconds per video second, without the ~2 s browser start
for i in 1 2; do
  run "engine_showcase_60f_r$i" 2 nice -n 10 npx remotion render build Showcase "$TMP/e60.mp4" --frames=0-59 --concurrency=4 --muted --log=error
  run "baseline_kit_orca_60f_r$i" 2 bash -c "cd '$APP/studio' && nice -n 10 npx remotion render '$TMP/studio-build' Storyboard '$TMP/b60.mp4' --props='$APP/episodes/explainer-orca/storyboard.json' --frames=0-59 --concurrency=4 --muted --log=error"
done
# texture pass: deband (smooth JPEG/x264 steps) then a light temporal luma dither (bible §7.3), re-encode CRF 18
S=$(date +%s.%N)
nice -n 10 ffmpeg -v error -nostdin -y -threads 4 -i out/showcase.mp4 \
  -vf "deband=1thr=0.012:2thr=0.012:3thr=0.012:range=16:blur=1,noise=c0s=4:c0f=t+u" \
  -c:v libx264 -preset medium -crf 18 -x264-params aq-mode=3 -pix_fmt yuv420p -threads 4 out/showcase_tex.mp4 9>&-
E=$(date +%s.%N)
printf 'texture_pass_ffmpeg\t%.1f\t4\t%.2f\t-\t%s\n' "$(echo "$E - $S" | bc)" "$(echo "($E - $S) / 4" | bc -l)" "$(cut -d' ' -f1 /proc/loadavg)" | tee -a out/bench.tsv
ls -la out/*.mp4
