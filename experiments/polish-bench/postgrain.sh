# Spark: cost of adding grain in ffmpeg after the render instead of in Chrome
set -e
export PATH="$HOME/studio/bin:$PATH"
cd ~/studio/app/experiments/polish-bench/out
t() { local s=$(date +%s.%N); nice -n 10 "$@"; echo "$(echo "$(date +%s.%N) - $s" | bc)"; }
P=$(t ffmpeg -v error -nostdin -y -threads 4 -i Base.mp4 -c:v libx264 -crf 18 -pix_fmt yuv420p -an post_plain.mp4)
G=$(t ffmpeg -v error -nostdin -y -threads 4 -i Base.mp4 -vf "noise=c0s=7:c0f=t+u" -c:v libx264 -crf 18 -pix_fmt yuv420p -an post_grain.mp4)
printf 'ffmpeg_reencode_plain\t%.1f\t%s\nffmpeg_reencode_grain7\t%.1f\t%s\n' "$P" "$(stat -c %s post_plain.mp4)" "$G" "$(stat -c %s post_grain.mp4)" | tee postgrain.tsv
