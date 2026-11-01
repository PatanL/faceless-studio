#!/usr/bin/env bash
# Run ON THE SPARK from experiments/polish-bench: bundle once, then time each composition (150 frames,
# 1080x1920, concurrency 2, nice 10, swangle CPU GL) under the shared render lock.
# Each composition is 450 frames (15 s); Base is re-run every 4-5 comps to track the shared box's load.
# usage: bash bench.sh [Comp ...]   -> out/results.tsv, out/stills/*.jpg, out/sheet.jpg
set -euo pipefail
export CUDA_VISIBLE_DEVICES=""
source ~/.nvm/nvm.sh >/dev/null; nvm use 22 >/dev/null
export PATH="$HOME/studio/bin:$PATH"
cd "$(dirname "$0")"
mkdir -p out/stills ~/studio/locks
COMPS=("$@")
[ ${#COMPS[@]} -gt 0 ] || COMPS=(Base Parallax5 DofCss DofSvg Rays Base RimGlowGradient GlowSvgFilter GlowCssDropShadow ShadowGradient Base ShadowBlurFilter GrainTurbulence GrainTile GrainEffect Base Particles150 Bokeh40Gradient Bokeh40CssBlur CausticsTurbulence Base CausticsTile LightLeakEffect GradeCssFilter VignetteGradient Base KurzStack MotionBlurPlainChild GlowEffectHtmlInCanvas Base)
[ -f public/noise.png ] || ffmpeg -v error -y -f lavfi -i "nullsrc=s=512x512,geq=lum='128+60*(random(1)-0.5)*2':cb=128:cr=128" -frames:v 1 public/noise.png
exec 9>~/studio/locks/render.lock
echo "[bench] waiting for render lock"; flock -w 3600 9
nice -n 10 npx remotion bundle src/index.ts --out-dir build --log=error 9>&-
[ -f public/caustic.png ] || { nice -n 10 npx remotion still build CausticSource public/caustic.png --log=error 9>&-; nice -n 10 npx remotion bundle src/index.ts --out-dir build --log=error 9>&-; }
[ -f out/results.tsv ] || printf 'comp\tseconds\tload1_start\tload1_end\tstatus\n' > out/results.tsv
for c in "${COMPS[@]}"; do
  L=$(cut -d' ' -f1 /proc/loadavg)
  S=$(date +%s.%N)
  if nice -n 10 npx remotion render build "$c" "out/$c.mp4" --concurrency=2 --log=error 9>&- >"out/$c.log" 2>&1; then ST=ok; else ST=FAIL; fi
  E=$(date +%s.%N)
  printf '%s\t%.1f\t%s\t%s\t%s\n' "$c" "$(echo "$E - $S" | bc)" "$L" "$(cut -d' ' -f1 /proc/loadavg)" "$ST" | tee -a out/results.tsv
  [ "$ST" = ok ] && ffmpeg -v error -nostdin -y -ss 7.5 -i "out/$c.mp4" -frames:v 1 -vf scale=270:480 "out/stills/$c.jpg" || true
done
ls out/stills/*.jpg >/dev/null 2>&1 && ffmpeg -v error -nostdin -y -pattern_type glob -i 'out/stills/*.jpg' -vf tile=7x4 out/sheet.jpg || true
