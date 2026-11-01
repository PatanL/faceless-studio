#!/usr/bin/env bash
# Render a Remotion composition on the Spark (CPU only) and pull the MP4 back to the Mac.
#
# usage: scripts/spark_render.sh <CompositionId> [out_name.mp4] [extra remotion render args...]
#   PROJ=studio         Remotion project dir (relative to repo root)
#   ENTRY=src/index.ts  Remotion entry point
#   CONC=8              --concurrency (hard cap 12; the Spark is shared)
#   PROPS=path.json     input props file (repo-relative, synced with the code)
#   NO_SYNC=1           skip the code sync     NO_PULL=1  leave the MP4 on the Spark
# Renders are serialized with a lock on the Spark (~/studio/locks/render.lock) so two
# lanes never exceed the thread budget at once. Output: ~/studio/app/<PROJ>/out/<name>
# on the Spark, copied to <repo>/out/<name> on the Mac.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
COMP="${1:?usage: spark_render.sh <CompositionId> [out.mp4] [args...]}"
NAME="${2:-$COMP.mp4}"; shift $(( $# >= 2 ? 2 : 1 ))
PROJ="${PROJ:-studio}"; ENTRY="${ENTRY:-src/index.ts}"; HOST="${SPARK_HOST:-dgx-spark}"
CONC="${CONC:-8}"; [ "$CONC" -gt 12 ] && { echo "CONC capped at 12"; CONC=12; }
EXTRA=("$@")

[ "${NO_SYNC:-0}" = 1 ] || "$ROOT/scripts/spark_sync.sh" "$PROJ"

# ssh flattens argv into one string, so quote every arg (empty PROPS must survive).
RARGS=$(printf '%q ' "$PROJ" "$ENTRY" "$COMP" "$NAME" "$CONC" "${PROPS:-}" ${EXTRA[@]+"${EXTRA[@]}"})
ssh "$HOST" "bash -s -- $RARGS" <<'REMOTE'
set -euo pipefail
PROJ=$1 ENTRY=$2 COMP=$3 NAME=$4 CONC=$5 PROPS=$6; shift 6
export CUDA_VISIBLE_DEVICES=""
source ~/.nvm/nvm.sh >/dev/null; nvm use 22 >/dev/null
export PATH="$HOME/studio/bin:$PATH"
mkdir -p ~/studio/locks
cd ~/studio/app/"$PROJ"; mkdir -p "$(dirname "out/$NAME")"
ARGS=(--concurrency="$CONC" --log=error)
[ -n "$PROPS" ] && ARGS+=(--props="$HOME/studio/app/$PROPS")
echo "[render] waiting for render lock..."
exec 9>~/studio/locks/render.lock; flock -w 5400 9
START=$(date +%s.%N)
npx remotion render "$ENTRY" "$COMP" "out/$NAME" "${ARGS[@]}" "$@"
END=$(date +%s.%N)
echo "[render] $COMP -> ~/studio/app/$PROJ/out/$NAME in $(echo "$END - $START" | bc) s (concurrency $CONC)"
REMOTE

if [ "${NO_PULL:-0}" != 1 ]; then
  mkdir -p "$(dirname "$ROOT/out/$NAME")"
  rsync -a "$HOST:~/studio/app/$PROJ/out/$NAME" "$ROOT/out/$NAME"
  echo "[render] pulled -> $ROOT/out/$NAME"
fi
