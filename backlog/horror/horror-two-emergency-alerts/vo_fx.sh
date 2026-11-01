#!/usr/bin/env bash
# Post-process the per-line Kokoro clips for horror-two-emergency-alerts (Spark only).
# usage: bash vo_fx.sh <wav_dir>     (needs ffmpeg; -threads 2)
# door   : the voice through a closed door (lowpass 1.3 kHz, a little wood boom, -3 dB)
# phone  : a phone line (band-pass 300-3400 Hz, light compression)
# whisper: Tess's own words, close and quiet (lowpass 5 kHz, -5 dB)
# d6 is rendered twice: d6_phone.wav and d6_door.wav (the storyboard starts the door copy 0.06 s later).
set -euo pipefail
D="$1"; cd "$D"
FF="${FFMPEG:-ffmpeg}"
fx() { "$FF" -nostdin -loglevel error -threads 2 -y -i "$1" -af "$2" "$3"; }
DOOR="lowpass=f=1300,lowpass=f=1300,equalizer=f=160:t=q:w=1:g=4,volume=-3dB"
PHONE="highpass=f=300,highpass=f=300,lowpass=f=3400,lowpass=f=3400,acompressor=threshold=-18dB:ratio=3,volume=1dB"
WHISPER="lowpass=f=5000,volume=-5dB"
mkdir -p raw
for f in d1; do cp -n "$f.wav" raw/ 2>/dev/null || true; fx "raw/$f.wav" "$DOOR" "$f.wav"; done
for f in d2 d3 d4 d5; do cp -n "$f.wav" raw/ 2>/dev/null || true; fx "raw/$f.wav" "$PHONE" "$f.wav"; done
for f in t1 t2 t3; do cp -n "$f.wav" raw/ 2>/dev/null || true; fx "raw/$f.wav" "$WHISPER" "$f.wav"; done
cp -n d6.wav raw/ 2>/dev/null || true
fx raw/d6.wav "$PHONE" d6_phone.wav
fx raw/d6.wav "$DOOR" d6_door.wav
echo "fx ok"
