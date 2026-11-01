#!/usr/bin/env bash
# Pull the Spark-owned daily research outputs back to the Mac (small text files only):
#   research/library.jsonl, research/library.state.json, research/daily/*.md
# These paths are excluded from scripts/spark_sync.sh so a Mac->Spark sync never overwrites them.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HOST="${SPARK_HOST:-dgx-spark}"
rsync -a "$HOST:~/studio/app/research/library.jsonl" "$HOST:~/studio/app/research/library.state.json" "$ROOT/research/"
rsync -a "$HOST:~/studio/app/research/daily/" "$ROOT/research/daily/"
wc -l "$ROOT/research/library.jsonl"; echo "report: $ROOT/research/daily/latest.md"
