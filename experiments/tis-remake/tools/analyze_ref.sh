#!/usr/bin/env bash
# Reference analysis for the TIS AK-12 benchmark (INTERNAL, never published).
# Runs on the Spark (CPU only). Reproduces everything in ~/studio/refs/tis-ak12/ and pulls
# the small outputs into experiments/tis-remake/ref/ (git-ignored: reference media).
#   bash experiments/tis-remake/tools/analyze_ref.sh
set -euo pipefail
URL="https://www.youtube.com/shorts/syVYb73Yj38"
R='~/studio/refs/tis-ak12'
HERE="$(cd "$(dirname "$0")" && pwd)"
LOCAL_REF="$HERE/../ref"
rsync -a "$HERE/" dgx-spark:$R/tools/
ssh dgx-spark "set -e; mkdir -p $R && cd $R
F=~/studio/bin/ffmpeg
# 1. download 1080x1920 (vp9 616) + opus; merge ourselves (yt-dlp can't see ffmpeg on PATH). Auto-subs hit HTTP 429, so whisper below.
[ -f ref.mp4 ] || { nice -n 10 ~/.local/bin/yt-dlp --js-runtimes node -f 'bv*[height>=1920]+ba/bv*+ba/b' -o 'ref.%(ext)s' --write-info-json '$URL' || true
  nice -n 10 \$F -v error -y -i ref.f616.mp4 -i ref.f251-18.webm -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k ref.mp4; }
\$F -v error -y -i ref.mp4 -vn audio.wav; \$F -v error -y -i ref.mp4 -vn -ac 1 -ar 16000 audio16k.wav
# 2. frames every 0.25 s (540x960) and every frame (270x480) for transitions
mkdir -p f025 f30; nice -n 10 \$F -v error -threads 2 -i ref.mp4 -vf fps=4,scale=540:960 -q:v 3 f025/f_%04d.jpg
nice -n 10 \$F -v error -threads 2 -i ref.mp4 -vf scale=270:480 -q:v 4 f30/f_%04d.jpg
# 3. scene detection (hard cuts are rare; most changes are matte wipes or camera moves, so use a low threshold)
nice -n 10 \$F -threads 2 -i ref.mp4 -vf 'select=gt(scene\,0.04),metadata=print:file=scenes04.txt' -an -f null - 2>/dev/null
# 4. transcript (faster-whisper small.en, CPU int8, 4 threads; audio loaded via numpy because the venv's PyAV is too new)
CUDA_VISIBLE_DEVICES='' OMP_NUM_THREADS=4 nice -n 10 ~/studio/.venv/bin/python - <<'PY'
import wave, json, numpy as np
from faster_whisper import WhisperModel
w = wave.open('audio16k.wav'); a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
m = WhisperModel('small.en', device='cpu', compute_type='int8', cpu_threads=4)
segs, _ = m.transcribe(a, word_timestamps=True, beam_size=5)
out = []; fw = open('words.tsv', 'w')
for s in segs:
    out.append(dict(start=s.start, end=s.end, text=s.text.strip()))
    for x in s.words: fw.write(f'{x.start:.2f}\t{x.end:.2f}\t{x.word.strip()}\n')
json.dump(out, open('transcript.json', 'w'), indent=1)
PY
# 5. contact sheets, transition strips, key stills
python3 tools/sheet.py f025 sheets 32 8 180
python3 tools/tstrip.py f30 trans 0.0:0.5 2.8:3.3 4.4:5.4 7.9:8.9 11.2:11.7 13.85:14.35 18.1:18.6 21.8:22.3 25.85:26.35 32.3:32.8 34.6:35.4 38.35:38.95 44.3:44.8 49.55:50.15
mkdir -p stills_full stills
for t in 0.0 0.5 0.75 1.25 2.5 2.95 3.0 3.1 3.5 4.75 5.0 5.5 6.5 7.0 7.5 8.0 8.5 9.0 9.75 10.75 11.5 12.0 13.5 14.0 14.1 14.5 16.25 17.0 18.25 18.5 19.75 21.0 21.9 22.0 22.5 24.0 25.75 26.0 26.1 27.0 28.0 28.75 30.0 31.0 32.5 33.0 34.75 35.0 35.5 37.0 38.6 39.5 40.75 42.5 44.5 45.0 47.0 49.0 49.8 50.0 51.0 53.0 54.75 55.9; do
  n=\$(printf '%05.2f' \$t); \$F -v error -threads 2 -ss \$t -i ref.mp4 -frames:v 1 -y stills_full/s_\$n.png
  \$F -v error -i stills_full/s_\$n.png -vf scale=720:1280 -q:v 4 -y stills/s_\$n.jpg; done
"
mkdir -p "$LOCAL_REF"
rsync -a dgx-spark:$R/sheets/ "$LOCAL_REF/sheets/"
rsync -a dgx-spark:$R/trans/ "$LOCAL_REF/transitions/"
rsync -a dgx-spark:$R/stills/ "$LOCAL_REF/stills/"
rsync -a dgx-spark:$R/{transcript.json,words.tsv,scenes04.txt} "$LOCAL_REF/"
# colour sampling example: ssh dgx-spark "cd $R/stills_full && python3 ../tools/palette.py s_06.50.png 75,1280,1005,1720 3"
