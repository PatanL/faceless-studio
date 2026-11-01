#!/usr/bin/env bash
# Install (idempotently) the daily research pull as a user crontab entry on the Spark, 06:00 local
# (America/Chicago). Keeps every other crontab line. Run from the Mac: scripts/install_research_cron.sh
# Remove: scripts/install_research_cron.sh --remove
set -euo pipefail
HOST="${SPARK_HOST:-dgx-spark}"
TAG="# faceless-studio research_daily"
LINE="0 6 * * * \$HOME/studio/app/scripts/research_daily.sh >/dev/null 2>&1 $TAG (metadata only, no LLM; see STUDIO.md)"
if [ "${1:-}" = --remove ]; then
  ssh "$HOST" "crontab -l 2>/dev/null | grep -vF '$TAG' | crontab -"
else
  ssh "$HOST" "chmod +x ~/studio/app/scripts/research_daily.sh; (crontab -l 2>/dev/null | grep -vF '$TAG'; echo '$LINE') | crontab -"
fi
ssh "$HOST" 'crontab -l'
