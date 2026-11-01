#!/usr/bin/env bash
# Render a few storyboard stills on the Spark (CPU only, niced, no render lock) and pull back
# one contact sheet. For look-dev between MP4 renders.
#
# usage: scripts/spark_stills.sh <storyboard.json> <t1,t2,...> [sheet.jpg]
#   storyboard path is repo-relative; times are seconds. FORMAT=16:9 overrides the format.
#   Sheet default: out/stills/<storyboard-basename>.jpg (tiles of 360 px wide cells, 6 per row).
#   NO_SYNC=1 skips the code sync.
#   STUDIO_LOCAL=1 (or SPARK_HOST=local): we are on the Spark; run here and copy the sheet (no ssh/rsync).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HOST="${SPARK_HOST:-dgx-spark}"
SB="${1:?usage: spark_stills.sh <storyboard.json> <t1,t2> [sheet.jpg]}"; AT="${2:?times}"
NAME="$(basename "$(dirname "$SB")")_$(basename "${SB%.json}")"
SHEET="${3:-out/stills/$NAME.jpg}"
LOCAL=0; { [ "${STUDIO_LOCAL:-0}" = 1 ] || [ "$HOST" = local ]; } && LOCAL=1
[ "${NO_SYNC:-0}" = 1 ] || [ "$LOCAL" = 1 ] || SKIP_NPM=1 "$ROOT/scripts/spark_sync.sh" studio >/dev/null
RARGS=$(printf '%q ' "$SB" "$AT" "$NAME" "${FORMAT:-}")
REMOTE_SCRIPT=$(cat <<'REMOTE'
set -euo pipefail
SB=$1 AT=$2 NAME=$3 FMT=$4
APP="${APP:-$HOME/studio/app}"
export CUDA_VISIBLE_DEVICES=""
source ~/.nvm/nvm.sh >/dev/null; nvm use 22 >/dev/null
export PATH="$HOME/studio/bin:$PATH"
cd "$APP/studio"
OUT="out/stills/$NAME"; rm -rf "$OUT"; mkdir -p "$OUT"
EXTRA=(); [ -n "$FMT" ] && EXTRA=(--format "$FMT")
nice -n 10 node src/cli/stills.mjs "$APP/$SB" --at "$AT" --out "$OUT" "${EXTRA[@]+"${EXTRA[@]}"}" | tail -n +1
N=$(ls "$OUT"/*.jpg | wc -l); COLS=$(( N < 6 ? N : 6 )); ROWS=$(( (N + COLS - 1) / COLS ))
nice -n 10 ffmpeg -v error -y -threads 2 -pattern_type glob -i "$OUT/*.jpg" -vf "scale=360:-2,tile=${COLS}x${ROWS}:padding=4:color=black" -frames:v 1 -q:v 3 "$OUT.jpg"
REMOTE
)
mkdir -p "$(dirname "$ROOT/$SHEET")"
if [ "$LOCAL" = 1 ]; then
  eval "set -- $RARGS"
  APP="$ROOT" bash -c "$REMOTE_SCRIPT" stills "$@"
  cp -p "$ROOT/studio/out/stills/$NAME.jpg" "$ROOT/$SHEET"
else
  ssh "$HOST" "bash -s -- $RARGS" <<<"$REMOTE_SCRIPT"
  rsync -a "$HOST:~/studio/app/studio/out/stills/$NAME.jpg" "$ROOT/$SHEET"
fi
echo "[stills] sheet -> $ROOT/$SHEET"
