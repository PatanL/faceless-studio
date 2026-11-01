#!/usr/bin/env bash
# Render thumbnails on the Spark (CPU only) and pull the PNGs back to the Mac.
#
# usage: scripts/thumbs_render.sh <spec.json>... [-- extra render.mjs args]
#   spec paths are repo-relative (e.g. studio/src/kits/thumbs/samples/samples.json)
#   OUT=thumbs/<name>   output subdir (Spark: <app>/studio/out/<OUT>, Mac: out/<OUT>)
#   NO_SYNC=1           skip the code sync
#   STUDIO_LOCAL=1      (or SPARK_HOST=local) we are on the Spark: run here, copy into out/<OUT> (no rsync)
# Defaults: both formats (1280x720 + 1080x1920) and a contact sheet per format.
# The sync never runs npm; the npm check runs briefly under ~/studio/locks/render.lock (F27).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HOST="${SPARK_HOST:-dgx-spark}"
OUT="${OUT:-thumbs/latest}"
SPECS=(); while [ $# -gt 0 ] && [ "$1" != "--" ]; do SPECS+=("$1"); shift; done; [ "${1:-}" = "--" ] && shift
[ ${#SPECS[@]} -gt 0 ] || { echo "usage: thumbs_render.sh <spec.json>... [-- args]"; exit 2; }
LOCAL=0; { [ "${STUDIO_LOCAL:-0}" = 1 ] || [ "$HOST" = local ]; } && LOCAL=1
[ "${NO_SYNC:-0}" = 1 ] || [ "$LOCAL" = 1 ] || SKIP_NPM=1 "$ROOT/scripts/spark_sync.sh" studio

RARGS=$(printf '%q ' "$OUT" "${SPECS[@]}" -- "$@")
REMOTE_SCRIPT=$(cat <<'REMOTE'
set -euo pipefail
APP="${APP:-$HOME/studio/app}"
OUT=$1; shift
SPECS=(); while [ "$1" != "--" ]; do SPECS+=("$APP/$1"); shift; done; shift
export CUDA_VISIBLE_DEVICES=""
source ~/.nvm/nvm.sh >/dev/null; nvm use 22 >/dev/null
export PATH="$HOME/studio/bin:$PATH"
cd "$APP/studio"
mkdir -p ~/studio/locks
# npm deps under the render lock (F27); the lock is released before the stills render
( exec 9>~/studio/locks/render.lock; flock -w 5400 9
  if [ -f package-lock.json ]; then
    H=$(cat package.json package-lock.json | sha256sum | cut -d' ' -f1)
    if [ "$(cat node_modules/.lockhash 2>/dev/null)" != "$H" ]; then
      echo "[thumbs] npm ci (lockfile changed)"; nice -n 10 npm ci --no-audit --no-fund --loglevel=error 9>&-
      echo "$H" > node_modules/.lockhash
    fi
  fi )
# stills are one Chrome tab: light enough to skip the MP4 render lock; niced for the shared box
nice -n 10 node src/kits/thumbs/render.mjs "${SPECS[@]}" --out "out/$OUT" --sheet "$@"
REMOTE
)
mkdir -p "$ROOT/out/$OUT"
if [ "$LOCAL" = 1 ]; then
  eval "set -- $RARGS"
  APP="$ROOT" bash -c "$REMOTE_SCRIPT" thumbs "$@"
  cp -pR "$ROOT/studio/out/$OUT/." "$ROOT/out/$OUT/"
  echo "[thumbs] copied -> $ROOT/out/$OUT"
else
  ssh "$HOST" "bash -s -- $RARGS" <<<"$REMOTE_SCRIPT"
  rsync -a "$HOST:~/studio/app/studio/out/$OUT/" "$ROOT/out/$OUT/"
  echo "[thumbs] pulled -> $ROOT/out/$OUT"
fi
