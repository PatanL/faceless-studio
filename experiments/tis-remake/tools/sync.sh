#!/usr/bin/env bash
# Push the remake code (not ref/ or out/) to the Spark and link the studio's node_modules.
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
ssh dgx-spark 'mkdir -p ~/studio/app/experiments/tis-remake'
rsync -a --exclude node_modules --exclude out --exclude ref "$HERE/" dgx-spark:~/studio/app/experiments/tis-remake/
ssh dgx-spark 'cd ~/studio/app/experiments/tis-remake/remotion && [ -e node_modules ] || ln -s ~/studio/app/studio/node_modules node_modules'
