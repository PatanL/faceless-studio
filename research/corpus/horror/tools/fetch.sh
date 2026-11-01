#!/bin/bash
# usage: fetch.sh <platform> <id> <url>   (runs on Spark)
set -u
P=$1; ID=$2; URL=$3
B=~/studio/refs/corpus_horror; mkdir -p $B/vid $B/aud $B/subs $B/logs
export PATH=~/studio/bin:$PATH
YT=~/.local/bin/yt-dlp
if [ "$P" = yt ]; then
  $YT --skip-download --write-auto-subs --write-subs --sub-langs 'en.*,en' --sub-format vtt -o "$B/subs/$ID.%(ext)s" "$URL" > $B/logs/$ID.subs.log 2>&1
fi
# find existing mp4 from R2
EX=$(ls ~/studio/refs/R2/*_$ID.mp4 ~/studio/refs/R2/outliers/*_$ID.mp4 2>/dev/null | head -1)
if [ -n "$EX" ]; then ln -sf "$EX" $B/vid/$ID.mp4; fi
if [ ! -s $B/vid/$ID.mp4 ]; then
  $YT -f 'b[height<=720]/bv*[height<=720]+ba/b' -S 'res:720' --merge-output-format mp4 -o "$B/vid/$ID.%(ext)s" "$URL" > $B/logs/$ID.dl.log 2>&1
fi
$YT -j --skip-download "$URL" > $B/vid/$ID.info.json 2>/dev/null
ffmpeg -nostdin -y -loglevel error -i $B/vid/$ID.mp4 -ac 1 -ar 16000 $B/aud/$ID.wav
echo done $ID
