#!/usr/bin/env bash
# Rerun the reference frame analysis on any video (ours or a reference). Runs on the Spark, CPU only.
#
#   ssh dgx-spark
#   cd ~/studio/refs/frame-analysis            # tools/ and .venv/ live here (uv venv with numpy + pillow)
#   tools/run_spark.sh /path/to/video.mp4 KEY [settings.csv] [t0] [t1]
#
# Step 1 (always): every-frame metrics -> out/KEY.npz + out/KEY_events.json
#                  review frames every 0.5 s + both sides of each cut/transition -> out/KEY_f/
#                  0.5 s contact sheets with cut/transition/composition markers -> sheets/KEY_half_*.jpg
# Step 2 (after you have written the settings catalogue KEY_settings.csv by watching the sheets):
#                  settings-vs-shot stats -> out/KEY_settings_stats.json
#                  colour script -> sheets/colour_KEY.jpg + out/KEY_colour.json
set -euo pipefail
VID=$1; KEY=$2; CSV=${3:-}; T0=${4:-0}; T1=${5:-0}
FF=~/studio/bin/ffmpeg
PY=".venv/bin/python -I"
export CUDA_VISIBLE_DEVICES=""
mkdir -p out sheets
nice -n 10 $PY tools/frame_metrics.py $FF "$VID" out/$KEY --threads 6
nice -n 10 $PY tools/grab_frames.py $FF "$VID" out/${KEY}_events.json out/${KEY}_f --threads 6
nice -n 10 $PY tools/sheets.py grid out/${KEY}_f out/${KEY}_events.json sheets/${KEY}_half
if [ -n "$CSV" ]; then
  $PY tools/settings_stats.py "$CSV" out/${KEY}_events.json --t0 $T0 --t1 $T1 --json out/${KEY}_settings_stats.json
  $PY tools/colour_script.py out/$KEY.npz "$CSV" sheets/colour_$KEY.jpg --title "$KEY" --t0 $T0 --t1 $T1 --json out/${KEY}_colour.json
fi
