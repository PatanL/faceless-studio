#!/usr/bin/env bash
# Sync the repo (code only) from the Mac to dgx-spark:~/studio/app and make sure
# npm deps are installed for the Remotion project there.
#
# usage: scripts/spark_sync.sh [project_dir]      (default: studio)
#   SYNC_DELETE=1  also delete files on the Spark that no longer exist on the Mac
#                  (Spark-owned paths in scripts/spark_owned.txt are always protected, F25)
#   SKIP_NPM=1     only rsync, skip the npm step
#   STUDIO_LOCAL=1 (or SPARK_HOST=local): we are on the Spark itself; nothing to sync, exits 0
#
# What is never pushed:
#   - every path in scripts/spark_owned.txt (operator data, op-* episodes, research ledgers, mixes,
#     episodes/*/audio/, out/): the Spark writes them, scripts/pull_ops.sh / pull_research.sh bring them back (F25, F26)
#   - in the main pass, the files make.py's claude steps edit on the Spark (episodes/*/{script.md,shots.json,
#     titles.md,description.md,thumbs.json,package.json}). They go in a second pass with --update, so a stale
#     Mac copy never overwrites a newer Spark edit, while a script you just edited on the Mac still goes up (F07).
# The remote rsync runs under an exclusive ~/studio/locks/code.lock (an operator make holds it shared for one
# step at a time), and npm runs under ~/studio/locks/render.lock so it never swaps node_modules under a
# running render (F08, F27). npm ci runs only when package.json/package-lock.json changed (node_modules/.lockhash).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PROJ="${1:-studio}"
HOST="${SPARK_HOST:-dgx-spark}"
if [ "${STUDIO_LOCAL:-0}" = 1 ] || [ "$HOST" = local ]; then
  echo "[sync] local mode: nothing to sync"
  exit 0
fi
DEL=(); [ "${SYNC_DELETE:-0}" = 1 ] && DEL=(--delete)

OWNED=()
while IFS= read -r p; do
  p="${p%%#*}"; p="${p%"${p##*[![:space:]]}"}"
  [ -n "$p" ] || continue
  OWNED+=("--filter=P $p" "--exclude=$p")
done < "$ROOT/scripts/spark_owned.txt"
EDITED=(script.md shots.json titles.md description.md thumbs.json package.json)
EDIT_EX=(); for f in "${EDITED[@]}"; do EDIT_EX+=("--exclude=/episodes/*/$f"); done
LOCKED_RSYNC='mkdir -p $HOME/studio/locks && flock -w 1800 $HOME/studio/locks/code.lock rsync'

rsync -a ${DEL[@]+"${DEL[@]}"} --rsync-path="$LOCKED_RSYNC" \
  "${OWNED[@]}" "${EDIT_EX[@]}" \
  --exclude node_modules --exclude out --exclude .git \
  --exclude '*.mp4' --exclude '.DS_Store' --exclude __pycache__ --exclude '*.prev' --exclude '*.tmp' \
  "$ROOT/" "$HOST:~/studio/app/"
# second pass: claude-edited episode files, only where the Mac copy is newer (F07)
INC=(--include='/episodes/' --include='/episodes/*/')
for f in "${EDITED[@]}"; do INC+=("--include=/episodes/*/$f"); done
rsync -a --update --rsync-path="$LOCKED_RSYNC" --exclude='/episodes/op-*/' "${INC[@]}" --exclude='*' \
  "$ROOT/" "$HOST:~/studio/app/"
echo "[sync] code -> $HOST:~/studio/app"

[ "${SKIP_NPM:-0}" = 1 ] && exit 0
[ -f "$ROOT/$PROJ/package.json" ] || { echo "[sync] no $PROJ/package.json, skipping npm"; exit 0; }

ssh "$HOST" bash -s -- "$PROJ" <<'REMOTE'
set -euo pipefail
export CUDA_VISIBLE_DEVICES=""
source ~/.nvm/nvm.sh >/dev/null; nvm use 22 >/dev/null
export PATH="$HOME/studio/bin:$PATH"
cd ~/studio/app/"$1"
mkdir -p ~/studio/locks
exec 9>~/studio/locks/render.lock; flock -w 5400 9   # npm never runs under a render (F08)
if [ -f package-lock.json ]; then
  H=$(cat package.json package-lock.json | sha256sum | cut -d' ' -f1)
  if [ "$(cat node_modules/.lockhash 2>/dev/null)" != "$H" ]; then
    echo "[sync] npm ci in $1 (lockfile changed)"
    nice -n 10 npm ci --no-audit --no-fund --loglevel=error
    [ -d node_modules/.bin ] || { echo "[sync] npm ci produced no node_modules/.bin (package.json has no deps?)"; exit 1; }
    echo "$H" > node_modules/.lockhash
  else
    echo "[sync] node_modules up to date"
  fi
else
  echo "[sync] no package-lock.json: npm install (commit the generated lock back from the Spark)"
  nice -n 10 npm install --no-audit --no-fund --loglevel=error
fi
REMOTE
