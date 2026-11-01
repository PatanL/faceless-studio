#!/usr/bin/env bash
# audio.sh <audio_file> <outdir>
# Loudness (EBU R128) + 0.1 s RMS envelopes for full band, <150 Hz (music bed / bass),
# 150-4000 Hz (voice band) and >5 kHz (whooshes, risers, clicks). audio.py analyses them.
set -euo pipefail
export CUDA_VISIBLE_DEVICES=""
FF=${FFMPEG:-$HOME/studio/bin/ffmpeg}
a="$1"; o="$2"; mkdir -p "$o"
nice -n 10 "$FF" -hide_banner -nostats -threads 2 -i "$a" -af ebur128=peak=true -f null - 2> "$o/ebur128.log" || true
grep -A12 "Summary" "$o/ebur128.log" > "$o/loudness.txt" || true
for band in full low voice high; do
  case $band in
    full)  f="anull";;
    low)   f="lowpass=f=150,lowpass=f=150";;
    voice) f="highpass=f=150,lowpass=f=4000";;
    high)  f="highpass=f=5000,highpass=f=5000";;
  esac
  nice -n 10 "$FF" -hide_banner -nostats -loglevel error -threads 2 -i "$a" -ac 1 -ar 16000 \
    -af "$f,asetnsamples=1600,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=$o/rms_$band.raw" -f null -
  paste -d' ' <(grep -o 'pts_time:[0-9.]*' "$o/rms_$band.raw" | cut -d: -f2) <(grep -o 'RMS_level=[-0-9.inf]*' "$o/rms_$band.raw" | cut -d= -f2) > "$o/rms_$band.txt"
  rm -f "$o/rms_$band.raw"
done
cat "$o/loudness.txt"
