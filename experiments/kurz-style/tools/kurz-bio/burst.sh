#!/bin/bash
# usage: burst.sh video start label   -> 20 frames at 4 fps over 5 s
v=$1; s=$2; lab=$3
mkdir -p burst/$lab
nice -n 10 ~/studio/bin/ffmpeg -nostdin -loglevel error -threads 3 -ss $s -i $v.mp4 -t 5 -vf fps=4 -q:v 2 burst/$lab/b%03d.jpg
