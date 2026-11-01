#!/usr/bin/env bash
# Sync the repo (code only) from the Mac to dgx-spark:~/studio/app and make sure
# npm deps are installed for the Remotion project there.
#
# usage: scripts/spark_sync.sh [project_dir]      (default: studio)
#   SYNC_DELETE=1  also delete files on the Spark that no longer exist on the Mac
#   SKIP_NPM=1     only rsync, skip the npm step
# research/library.jsonl, library.state.json and research/daily/ are written on the Spark by the
# daily cron (scripts/research_daily.sh) and never synced from the Mac; pull them with scripts/pull_research.sh.
# npm ci runs only when package.json/package-lock.json changed (hash stamp in node_modules/.lockhash).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PROJ="${1:-studio}"
HOST="${SPARK_HOST:-dgx-spark}"
DEL=(); [ "${SYNC_DELETE:-0}" = 1 ] && DEL=(--delete)

rsync -a ${DEL[@]+"${DEL[@]}"} --exclude node_modules --exclude out --exclude .git \
  --exclude '*.mp4' --exclude '.DS_Store' \
  --exclude /research/library.jsonl --exclude /research/library.state.json --exclude /research/daily/ \
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
if [ -f package-lock.json ]; then
  H=$(cat package.json package-lock.json | sha256sum | cut -d' ' -f1)
  if [ "$(cat node_modules/.lockhash 2>/dev/null)" != "$H" ]; then
    echo "[sync] npm ci in $1 (lockfile changed)"
    npm ci --no-audit --no-fund --loglevel=error
    [ -d node_modules/.bin ] || { echo "[sync] npm ci produced no node_modules/.bin (package.json has no deps?)"; exit 1; }
    echo "$H" > node_modules/.lockhash
  else
    echo "[sync] node_modules up to date"
  fi
else
  echo "[sync] no package-lock.json: npm install (commit the generated lock back from the Spark)"
  npm install --no-audit --no-fund --loglevel=error
fi
REMOTE
