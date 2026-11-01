#!/bin/bash
# sheets.sh <id> : 1 fps frames -> contact sheets of 12 tiles (6x2), 270px wide; sheet k covers seconds 12*(k-1)..12*k-1
B=~/studio/refs/corpus_horror; ID=$1; export PATH=~/studio/bin:$PATH
rm -rf $B/frames/$ID $B/sheets/$ID; mkdir -p $B/frames/$ID $B/sheets/$ID
nice ffmpeg -threads 2 -nostdin -y -loglevel error -i $B/vid/$ID.mp4 -vf "fps=1,scale=270:-2" -q:v 4 $B/frames/$ID/f_%04d.jpg
nice ffmpeg -threads 2 -nostdin -y -loglevel error -framerate 1 -i $B/frames/$ID/f_%04d.jpg -vf "tile=6x2:padding=2" -q:v 5 $B/sheets/$ID/s_%03d.jpg
echo $ID $(ls $B/frames/$ID | wc -l) frames $(ls $B/sheets/$ID | wc -l) sheets
