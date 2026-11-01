#!/usr/bin/env bash
# Render thumbnails on the Spark (CPU only) and pull the PNGs back to the Mac.
#
# usage: scripts/thumbs_render.sh <spec.json>... [-- extra render.mjs args]
#   spec paths are repo-relative (e.g. studio/src/kits/thumbs/samples/samples.json)
#   OUT=thumbs/<name>   output subdir (Spark: ~/studio/app/studio/out/<OUT>, Mac: out/<OUT>)
#   NO_SYNC=1           skip the code sync
# Defaults: both formats (1280x720 + 1080x1920) and a contact sheet per format.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HOST="${SPARK_HOST:-dgx-spark}"
OUT="${OUT:-thumbs/latest}"
SPECS=(); while [ $# -gt 0 ] && [ "$1" != "--" ]; do SPECS+=("$1"); shift; done; [ "${1:-}" = "--" ] && shift
[ ${#SPECS[@]} -gt 0 ] || { echo "usage: thumbs_render.sh <spec.json>... [-- args]"; exit 2; }
[ "${NO_SYNC:-0}" = 1 ] || "$ROOT/scripts/spark_sync.sh" studio

RARGS=$(printf '%q ' "$OUT" "${SPECS[@]}" -- "$@")
ssh "$HOST" "bash -s -- $RARGS" <<'REMOTE'
set -euo pipefail
OUT=$1; shift
SPECS=(); while [ "$1" != "--" ]; do SPECS+=("$HOME/studio/app/$1"); shift; done; shift
export CUDA_VISIBLE_DEVICES=""
source ~/.nvm/nvm.sh >/dev/null; nvm use 22 >/dev/null
export PATH="$HOME/studio/bin:$PATH"
cd ~/studio/app/studio
# stills are one Chrome tab: light enough to skip the MP4 render lock; niced for the shared box
nice -n 10 node src/kits/thumbs/render.mjs "${SPECS[@]}" --out "out/$OUT" --sheet "$@"
REMOTE
mkdir -p "$ROOT/out/$OUT"
rsync -a "$HOST:~/studio/app/studio/out/$OUT/" "$ROOT/out/$OUT/"
echo "[thumbs] pulled -> $ROOT/out/$OUT"
