#!/bin/bash
# usage: scene.sh video.mp4 out.log
nice -n 10 ~/studio/bin/ffmpeg -nostdin -threads 3 -i "$1" -an -vf 'fps=30,scale=320:-2,select=gt(scene\,0.20),showinfo' -f null - 2> "$2"
grep -o 'pts_time:[0-9.]*' "$2" | cut -d: -f2 > "${2%.log}.txt"
