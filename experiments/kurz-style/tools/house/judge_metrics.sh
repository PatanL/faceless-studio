#!/usr/bin/env bash
# judge_metrics.sh: the automatic half of JUDGE_RUBRIC.md, run on one rendered MP4 (Spark, CPU only).
#   bash tools/house/judge_metrics.sh <video.mp4> <outdir> [label]
# Run from experiments/kurz-style/ (synced to the Spark). Writes into <outdir>:
#   grid/            frame every 2 s (also the frames for the side-by-side sheet)
#   palette.json     tools/house/palette_check.py per frame
#   fm.json          tools/tis/frame_metrics.py per frame (edge density, outline, blur, gradients)
#   density.txt      tools/tis/density.py (shapes / micro-details per frame)
#   gridchange.txt   tools/tis/gridchange.py (new composition cadence)
#   scores.txt, scores_events.json, cuts.txt   tools/tis/scores.sh + cuts.py (hard cuts, transitions)
#   motion.npz, motion_summary.json            tools/kurz-bio/motion.py + motion_summary.py
#   loud.txt, silence.txt                      ffmpeg ebur128 + silencedetect (-45 dB, 0.4 s)
#   JUDGE_METRICS.json + printed table         tools/house/judge_summary.py (targets from STYLE_BIBLE.md §13)
set -euo pipefail
export CUDA_VISIBLE_DEVICES="" OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
FF=${FFMPEG:-$HOME/studio/bin/ffmpeg}; FP=${FFPROBE:-$HOME/studio/bin/ffprobe}
PY="nice -n 10 ${PYTHON:-$HOME/studio/venvs/r2/bin/python} -I"
v="$1"; out="$2"; label="${3:-$(basename "$v" .mp4)}"; mkdir -p "$out"
here="$(cd "$(dirname "$0")/../.." && pwd)"   # experiments/kurz-style
T="$here/tools"
fps=$("$FP" -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$v" | awk -F/ '{printf "%.3f", $1/($2?$2:1)}')
echo "[$label] fps $fps"
FFMPEG="$FF" bash "$T/tis/extract.sh" "$v" "$out"
$PY "$T/house/palette_check.py" "$here/house/palette.json" "$out"/grid/*.jpg --json "$out/palette.json" > "$out/palette.txt"
$PY "$T/tis/frame_metrics.py" "$out/grid" "$out/fm.json" > /dev/null
$PY "$T/tis/density.py" "$out"/grid/*.jpg > "$out/density.txt"
$PY "$T/tis/gridchange.py" "$out/grid" > "$out/gridchange.txt"
FFMPEG="$FF" bash "$T/tis/scores.sh" "$v" "$out/scores.txt" > /dev/null
$PY "$T/tis/cuts.py" "$out/scores.txt" "$fps" > "$out/cuts.txt"
$PY "$T/kurz-bio/motion.py" "$FF" "$v" 30 "$out/motion.npz" > /dev/null
$PY "$T/kurz-bio/motion_summary.py" "$out/motion.npz" "$label" > "$out/motion.txt"
nice -n 10 "$FF" -hide_banner -nostats -threads 2 -i "$v" -vn -af ebur128 -f null - 2> "$out/loud.txt" || true
nice -n 10 "$FF" -hide_banner -nostats -threads 2 -i "$v" -vn -af silencedetect=n=-45dB:d=0.4 -f null - 2> "$out/silence.txt" || true
$PY "$T/house/judge_summary.py" "$out" "$label"
