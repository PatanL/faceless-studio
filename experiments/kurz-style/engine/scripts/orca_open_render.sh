#!/usr/bin/env bash
# Run ON THE SPARK from experiments/kurz-style/engine. Renders the OrcaOpen rebuild (orca pilot 0-9.73 s),
# 1080x1920 30 fps, CPU only, --concurrency=4, nice 10, under the shared render lock; then the texture pass
# (deband + dither, bible §7.3) and the episode's own narration mix muxed in (first 9.733 s, 60 ms fade-out).
# usage: bash scripts/orca_open_render.sh <tag>      -> out/orca_open_<tag>.mp4 (+ _raw), timing in out/orca_open_bench.tsv
set -euo pipefail
export CUDA_VISIBLE_DEVICES=""
source ~/.nvm/nvm.sh >/dev/null; nvm use 22 >/dev/null
export PATH="$HOME/studio/bin:$PATH"
cd "$(dirname "$0")/.."
TAG=${1:-v1}
MIX="$HOME/studio/app/studio/public/episodes/explainer-orca/mix.wav"
DUR=9.733
mkdir -p out ~/studio/locks
exec 9>~/studio/locks/render.lock
echo "[orca_open] waiting for render lock"; flock -w 5400 9
nice -n 10 npx remotion bundle src/index.ts --out-dir build --log=error 9>&-
L0=$(cut -d' ' -f1 /proc/loadavg); S=$(date +%s.%N)
nice -n 10 npx remotion render build OrcaOpen "out/orca_open_${TAG}_raw.mp4" --concurrency=4 --muted --log=error 9>&-
M=$(date +%s.%N)
nice -n 10 ffmpeg -v error -nostdin -y -threads 4 -i "out/orca_open_${TAG}_raw.mp4" -t $DUR -i "$MIX" \
  -filter_complex "[0:v]deband=1thr=0.012:2thr=0.012:3thr=0.012:range=16:blur=1,noise=c0s=4:c0f=t+u[v];[1:a]atrim=0:$DUR,afade=t=out:st=$(echo "$DUR - 0.06" | bc):d=0.06[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 18 -x264-params aq-mode=3 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart \
  "out/orca_open_${TAG}.mp4" 9>&-
E=$(date +%s.%N)
[ -f out/orca_open_bench.tsv ] || printf 'tag\trender_s\ttexture_mux_s\ttotal_s\tvideo_s\trender_s_per_video_s\tload1_start\tload1_end\n' > out/orca_open_bench.tsv
printf '%s\t%.1f\t%.1f\t%.1f\t%s\t%.2f\t%s\t%s\n' "$TAG" "$(echo "$M - $S" | bc)" "$(echo "$E - $M" | bc)" "$(echo "$E - $S" | bc)" $DUR "$(echo "($M - $S) / $DUR" | bc -l)" "$L0" "$(cut -d' ' -f1 /proc/loadavg)" | tee -a out/orca_open_bench.tsv
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height -of compact "out/orca_open_${TAG}.mp4"
