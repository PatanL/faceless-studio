#!/usr/bin/env bash
# usage: run_one.sh <key> <video>   (same tools/flags as run_all.sh)
set -u
export CUDA_VISIBLE_DEVICES="" OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
PY="/home/dzliu/pzliu/.venv/bin/python -I"
T=~/studio/app/research/frame-analysis/tools
FF=~/studio/bin/ffmpeg
key=$1; vid=$2
cd ~/studio/scratch/storylane
nice -n 10 $PY $T/frame_metrics.py $FF "$vid" out/$key --threads 4 > out/${key}_fm.log 2>&1
nice -n 10 $PY $T/camera_motion.py $FF "$vid" out/$key --events out/${key}_events.json --threads 4 > out/${key}_cam.log 2>&1
nice -n 10 $PY $T/look_stats.py $FF "$vid" out/$key --threads 4 > out/${key}_look.log 2>&1
(cd ~/studio/app && nice -n 10 /home/dzliu/pzliu/.venv/bin/python -m pipeline.qa.frames30 r_$key --root ~/studio/scratch/storylane/f30root --mp4 "$vid" > ~/studio/scratch/storylane/out/${key}_f30.log 2>&1)
echo "$key done"
