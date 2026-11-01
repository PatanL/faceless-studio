#!/usr/bin/env bash
# Spark cron entry (06:00 America/Chicago): daily metadata pull for research/automation/channels.json.
# yt-dlp --flat-playlist metadata only, no downloads, no LLM, no GPU, one process, niced.
# Appends to ~/studio/app/research/library.jsonl, report in ~/studio/app/research/daily/latest.md.
# Log: ~/studio/logs/research_daily/<date>.log (kept 30 days).
set -uo pipefail
export CUDA_VISIBLE_DEVICES=""
export OMP_NUM_THREADS=1 PYTHONUNBUFFERED=1
export PATH="$HOME/.local/bin:$HOME/studio/bin:/usr/local/bin:/usr/bin:/bin"
APP="${STUDIO_APP:-$HOME/studio/app}"
LOGDIR="$HOME/studio/logs/research_daily"; mkdir -p "$LOGDIR" "$HOME/studio/locks"
LOG="$LOGDIR/$(date -u +%F).log"
exec 9>"$HOME/studio/locks/research_daily.lock"
flock -n 9 || { echo "[research_daily] already running" >>"$LOG"; exit 0; }
echo "[research_daily] start $(date -u +%FT%TZ)" >>"$LOG"
nice -n 10 /usr/bin/python3 -I "$APP/research/automation/daily_pull.py" "$@" >>"$LOG" 2>&1
rc=$?
echo "[research_daily] end $(date -u +%FT%TZ) rc=$rc" >>"$LOG"
find "$LOGDIR" -name '*.log' -mtime +30 -delete 2>/dev/null
exit $rc
