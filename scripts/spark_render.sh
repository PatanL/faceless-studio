#!/usr/bin/env bash
# Render a Remotion composition on the Spark (CPU only) and pull the MP4 back to the Mac.
#
# usage: scripts/spark_render.sh <CompositionId> [out_name.mp4] [extra remotion render args...]
#   PROJ=studio         Remotion project dir (relative to repo root)
#   ENTRY=src/index.ts  Remotion entry point
#   CONC=4              --concurrency: default 4, hard cap 4 (~10 cores; BRIEF thread budget, F28).
#                       Use CONC=2 while another TTS/whisper job of ours runs.
#   PROPS=path.json     input props file (repo-relative, synced with the code)
#   NO_SYNC=1           skip the code sync     NO_PULL=1  leave the MP4 on the Spark
#   STUDIO_LOCAL=1      (or SPARK_HOST=local) we are on the Spark: run here, copy the MP4 into out/ (no rsync)
# Renders are serialized with ~/studio/locks/render.lock. The npm check runs inside the same lock (F27), so it never
# swaps node_modules under another render. The render runs in its own process group: if the ssh session (or the
# calling make) goes away, or the job gets HUP/INT/TERM, the whole group is killed and the lock is freed (F29).
# Output: <app>/<PROJ>/out/<name> on the Spark, copied to <repo>/out/<name>.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
COMP="${1:?usage: spark_render.sh <CompositionId> [out.mp4] [args...]}"
NAME="${2:-$COMP.mp4}"; shift $(( $# >= 2 ? 2 : 1 ))
PROJ="${PROJ:-studio}"; ENTRY="${ENTRY:-src/index.ts}"; HOST="${SPARK_HOST:-dgx-spark}"
CONC_MAX=4
CONC="${CONC:-4}"
case "$CONC" in ''|*[!0-9]*) echo "[render] CONC=$CONC is not a number, using 4" >&2; CONC=4;; esac
if [ "$CONC" -gt "$CONC_MAX" ]; then echo "[render] WARNING: CONC=$CONC clamped to $CONC_MAX (thread budget)" >&2; CONC=$CONC_MAX; fi
[ "$CONC" -ge 1 ] || CONC=1
EXTRA=("$@")
LOCAL=0; { [ "${STUDIO_LOCAL:-0}" = 1 ] || [ "$HOST" = local ]; } && LOCAL=1

[ "${NO_SYNC:-0}" = 1 ] || [ "$LOCAL" = 1 ] || SKIP_NPM=1 "$ROOT/scripts/spark_sync.sh" "$PROJ"

# ssh flattens argv into one string, so quote every arg (empty PROPS must survive).
RARGS=$(printf '%q ' "$PROJ" "$ENTRY" "$COMP" "$NAME" "$CONC" "${PROPS:-}" ${EXTRA[@]+"${EXTRA[@]}"})
REMOTE_SCRIPT=$(cat <<'REMOTE'
set -euo pipefail
PROJ=$1 ENTRY=$2 COMP=$3 NAME=$4 CONC=$5 PROPS=$6; shift 6
APP="${APP:-$HOME/studio/app}"
export CUDA_VISIBLE_DEVICES=""
source ~/.nvm/nvm.sh >/dev/null; nvm use 22 >/dev/null
export PATH="$HOME/studio/bin:$PATH"
mkdir -p ~/studio/locks
cd "$APP/$PROJ"; mkdir -p "$(dirname "out/$NAME")"
ARGS=(--concurrency="$CONC" --log=error)
[ -n "$PROPS" ] && ARGS+=(--props="$APP/$PROPS")
echo "[render] waiting for render lock..."
exec 9>~/studio/locks/render.lock; flock -w 5400 9
# npm deps, inside the render lock (F08/F27)
if [ -f package-lock.json ]; then
  H=$(cat package.json package-lock.json | sha256sum | cut -d' ' -f1)
  if [ "$(cat node_modules/.lockhash 2>/dev/null)" != "$H" ]; then
    echo "[render] npm ci (lockfile changed)"
    nice -n 10 npm ci --no-audit --no-fund --loglevel=error 9>&-
    echo "$H" > node_modules/.lockhash
  fi
fi
START=$(date +%s.%N)
# own process group; children must not inherit the lock fd (F29)
setsid nice -n 10 npx remotion render "$ENTRY" "$COMP" "out/$NAME" "${ARGS[@]}" "$@" 9>&- &
RPID=$!
PGID=$RPID
cleanup() { kill -TERM -- "-$PGID" 2>/dev/null || true; sleep 1; kill -KILL -- "-$PGID" 2>/dev/null || true; }
trap 'cleanup; exit 130' HUP INT TERM PIPE
trap 'kill -0 "$RPID" 2>/dev/null && cleanup || true' EXIT
# watchdog: if whoever started us is gone (ssh dropped, make killed), we get reparented; stop the render
PARENT=$PPID
while kill -0 "$RPID" 2>/dev/null; do
  if ! kill -0 "$PARENT" 2>/dev/null || [ "$(ps -o ppid= -p $$ | tr -d ' ')" != "$PARENT" ]; then
    echo "[render] caller went away: killing render group $PGID" >&2; cleanup; exit 129
  fi
  sleep 3
done
set +e; wait "$RPID"; RC=$?; set -e
[ "$RC" = 0 ] || { echo "[render] remotion exited $RC" >&2; exit "$RC"; }
END=$(date +%s.%N)
echo "[render] $COMP -> $APP/$PROJ/out/$NAME in $(echo "$END - $START" | bc) s (concurrency $CONC)"
REMOTE
)

if [ "$LOCAL" = 1 ]; then
  eval "set -- $RARGS"
  APP="$ROOT" bash -c "$REMOTE_SCRIPT" render "$@"
else
  ssh "$HOST" "bash -s -- $RARGS" <<<"$REMOTE_SCRIPT"
fi

if [ "${NO_PULL:-0}" != 1 ]; then
  mkdir -p "$(dirname "$ROOT/out/$NAME")"
  if [ "$LOCAL" = 1 ]; then
    cp -p "$ROOT/$PROJ/out/$NAME" "$ROOT/out/$NAME"
    echo "[render] copied -> $ROOT/out/$NAME"
  else
    rsync -a "$HOST:~/studio/app/$PROJ/out/$NAME" "$ROOT/out/$NAME"
    echo "[render] pulled -> $ROOT/out/$NAME"
  fi
fi
