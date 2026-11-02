#!/usr/bin/env bash
# Run ON THE SPARK from experiments/detail-pass: bundle, proof stills, the 4 s showcase, texture pass, metrics.
#   bash scripts/render.sh [tag]        (CPU only, nice 10, concurrency 4, shared render lock)
set -euo pipefail
export CUDA_VISIBLE_DEVICES=""
source ~/.nvm/nvm.sh >/dev/null; nvm use 22 >/dev/null
export PATH="$HOME/studio/bin:$PATH"
cd "$(dirname "$0")/.."
DP="$(pwd)"; KS="$DP/../kurz-style"
tag=${1:-v1}
[ -e node_modules ] || ln -s ../kurz-style/engine/node_modules node_modules
mkdir -p out/stills ~/studio/locks
exec 9>~/studio/locks/render.lock
echo "[detail] waiting for render lock"; flock -w 5400 9
nice -n 10 npx tsc --noEmit 9>&-
nice -n 10 npx remotion bundle src/index.ts --out-dir build --log=error 9>&-
for s in Sheet Hero; do nice -n 10 npx remotion still build $s "out/stills/${s,,}_$tag.png" --log=error 9>&-; done
for f in 0 60 105; do nice -n 10 npx remotion still build DetailShowcase "out/stills/show_${tag}_f$(printf %03d $f).png" --frame=$f --log=error 9>&-; done
S=$(date +%s.%N)
nice -n 10 npx remotion render build DetailShowcase "out/detail_${tag}_raw.mp4" --concurrency=4 --muted --log=error 9>&-
E=$(date +%s.%N)
printf '%s\trender_4s\t%.1f\t%s\n' "$tag" "$(echo "$E - $S" | bc)" "$(cut -d' ' -f1 /proc/loadavg)" | tee -a out/bench.tsv
# texture pass (same as engine bench.sh): deband + light temporal luma dither
nice -n 10 ffmpeg -v error -nostdin -y -threads 4 -i "out/detail_${tag}_raw.mp4" \
  -vf "deband=1thr=0.012:2thr=0.012:3thr=0.012:range=16:blur=1,noise=c0s=4:c0f=t+u" \
  -c:v libx264 -preset medium -crf 18 -x264-params aq-mode=3 -pix_fmt yuv420p -threads 4 "out/detail_${tag}.mp4" 9>&-
exec 9>&-
# metrics: 0.5 s grid (engine frame_judge.sh) + the full judge on the 2 s grid
bash "$KS/engine/scripts/frame_judge.sh" "out/detail_${tag}.mp4" "out/judge_${tag}" "detail_${tag}" | tail -1
bash "$KS/tools/house/judge_metrics.sh" "out/detail_${tag}.mp4" "out/jm_${tag}" "detail_${tag}" > "out/jm_${tag}.txt" 2>&1 || echo "judge_metrics failed (see out/jm_${tag}.txt)"
~/studio/venvs/r2/bin/python -I tools/calm.py "out/judge_${tag}/grid" > "out/judge_${tag}/calm.json"
~/studio/venvs/r2/bin/python -I tools/specks.py "out/judge_${tag}/grid" > "out/judge_${tag}/specks.json"
node_modules/.bin/esbuild scripts/manifest.ts --bundle --platform=node --log-level=error --outfile=out/manifest.cjs && node out/manifest.cjs > "out/judge_${tag}/manifest.json"
ls -la out/*.mp4
