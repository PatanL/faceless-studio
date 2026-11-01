#!/usr/bin/env bash
# Run ON the Spark. Benchmarks a Remotion composition at several concurrencies.
# usage: spark_bench.sh <project_dir_under_~/studio/app> <entry> <comp> <label> [conc...] [-- extra args]
# Prints one CSV line per run: label,comp,conc,frames,fps,wall_s,s_per_video_s,load1_before
set -uo pipefail
PROJ=$1 ENTRY=$2 COMP=$3 LABEL=$4; shift 4
CONCS=(); while [ $# -gt 0 ] && [ "$1" != "--" ]; do CONCS+=("$1"); shift; done; [ "${1:-}" = "--" ] && shift
export CUDA_VISIBLE_DEVICES=""
source ~/.nvm/nvm.sh >/dev/null; nvm use 22 >/dev/null
export PATH="$HOME/studio/bin:$PATH"
mkdir -p ~/studio/locks; exec 9>~/studio/locks/render.lock; flock -w 5400 9
cd ~/studio/app/"$PROJ"; mkdir -p out
for C in "${CONCS[@]:-8}"; do
  L=$(cut -d' ' -f1 /proc/loadavg)
  S=$(date +%s.%N)
  npx remotion render "$ENTRY" "$COMP" "out/bench_${LABEL}_c$C.mp4" --concurrency="$C" --log=error "$@" >/tmp/bench_$$.log 2>&1 || { echo "FAIL c=$C"; tail -20 /tmp/bench_$$.log; continue; }
  E=$(date +%s.%N)
  W=$(echo "$E - $S" | bc)
  read -r FR FPS <<<"$(~/studio/bin/ffprobe -v error -select_streams v:0 -count_packets -show_entries stream=nb_read_packets,r_frame_rate -of csv=p=0 "out/bench_${LABEL}_c$C.mp4" | awk -F, '{split($1,a,"/"); print $2, a[1]/a[2]}')"
  VS=$(echo "$FR / $FPS" | bc -l)
  printf '%s,%s,%s,%s,%s,%.1f,%.3f,%s\n' "$LABEL" "$COMP" "$C" "$FR" "$FPS" "$W" "$(echo "$W / $VS" | bc -l)" "$L"
done
