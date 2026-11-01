#!/usr/bin/env bash
# HUMAN STEP. Install (idempotently) the operator watchdog as a user crontab entry on the Spark, every 15 min.
# Keeps every other crontab line (research_daily, other users' jobs). Agents never run this.
#   scripts/install_operator_cron.sh            # install (from the Mac via ssh, or on the Spark)
#   scripts/install_operator_cron.sh --remove
#   scripts/install_operator_cron.sh --print    # show the line only
# The watchdog does nothing until the operator was started once (data/operator/state.json) and while
# data/operator/STOPPED exists.
set -euo pipefail
HOST="${SPARK_HOST:-dgx-spark}"
TAG="# faceless-studio operator_watchdog"
LINE="*/15 * * * * \$HOME/studio/app/scripts/operator_watchdog.sh >/dev/null 2>&1 $TAG (keeps tmux studio-op alive; see OPERATOR.md)"
run() {
  if [ "$(uname -s)" = Linux ] && [ "${OPERATOR_REMOTE:-auto}" != 1 ]; then bash -c "$1"; else ssh "$HOST" "$1"; fi
}
case "${1:-}" in
  --print) echo "$LINE"; exit 0 ;;
  --remove) run "crontab -l 2>/dev/null | grep -vF '$TAG' | crontab -" ;;
  "") run "chmod +x ~/studio/app/scripts/operator_watchdog.sh; (crontab -l 2>/dev/null | grep -vF '$TAG'; echo '$LINE') | crontab -" ;;
  *) sed -n '2,9p' "$0"; exit 2 ;;
esac
run 'crontab -l'
