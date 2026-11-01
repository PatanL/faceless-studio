#!/usr/bin/env bash
# Spark system cron, every 15 min (installed by scripts/install_operator_cron.sh, a human step).
# Keeps the operator alive without doing any of its work:
#   - tmux session gone              -> operator_tmux.sh resume
#   - 04:00-06:00 local, session started before today's 04:00, not busy -> operator_tmux.sh rotate
#   - heartbeat older than 45 min and a job is due -> types "operator tick" into the session
#   - after a resume/rotate it waits WATCHDOG_SURVIVE_S (120 s) and records whether the session is still up; after 3
#     launches in a row that died that fast it backs off (30 min, 1 h, 2 h ... 4 h) and writes HUMAN.md
#   - heartbeat older than 2 h -> a HUMAN.md entry (once per day), so a dead or stuck session is never silent
# Does nothing while data/operator/STOPPED exists (operator_tmux.sh stop) or before the first start (no state.json).
# Log: ~/studio/logs/operator/watchdog.log
set -uo pipefail
export TZ=America/Chicago CUDA_VISIBLE_DEVICES=""
export PATH="$HOME/.local/bin:$HOME/studio/bin:/usr/local/bin:/usr/bin:/bin"
APP="${STUDIO_APP:-$HOME/studio/app}"
DATA="${STUDIO_DATA:-$APP/data}"
SESSION="${OPERATOR_TMUX:-studio-op}"
LOGDIR="${OPERATOR_LOG_DIR:-$HOME/studio/logs/operator}"
LOCKS="${STUDIO_LOCKS:-$HOME/studio/locks}"
mkdir -p "$LOGDIR" "$LOCKS"
LOG="$LOGDIR/watchdog.log"
log() { echo "[$(date -u +%FT%TZ)] $*" >>"$LOG"; }
exec 9>"$LOCKS/operator_watchdog.lock"
flock -n 9 || exit 0
cd "$APP" || { log "no app dir $APP"; exit 1; }
[ -f "$DATA/operator/state.json" ] || exit 0
[ -f "$DATA/operator/STOPPED" ] && exit 0
alive=0; tmux has-session -t "=$SESSION" 2>/dev/null && alive=1
act="$(STUDIO_DATA="$DATA" python3 -m pipeline.ops.state watchdog --tmux-alive "$alive" 2>>"$LOG")" || { log "watchdog check failed"; exit 1; }
survived() {  # did the session we just launched stay up? (expired login / limits / no allowlist die at once)
  sleep "${WATCHDOG_SURVIVE_S:-120}"
  local up=0; tmux has-session -t "=$SESSION" 2>/dev/null && up=1
  [ "$up" = 1 ] || log "session $SESSION died within ${WATCHDOG_SURVIVE_S:-120}s of launch"
  STUDIO_DATA="$DATA" python3 -m pipeline.ops.state watchdog-launched --survived "$up" >>"$LOG" 2>&1
}
case "$act" in
  none) ;;
  backoff) log "session $SESSION down; backing off after repeated fast exits (see HUMAN.md)" ;;
  resume) log "session $SESSION gone: resume"; OPERATOR_REMOTE=0 bash "$APP/scripts/operator_tmux.sh" resume >>"$LOG" 2>&1; survived ;;
  rotate) log "daily rotate"; OPERATOR_REMOTE=0 bash "$APP/scripts/operator_tmux.sh" rotate >>"$LOG" 2>&1; survived ;;
  tick)
    log "heartbeat stale and jobs due: sending tick"
    tmux send-keys -t "=$SESSION:" -l "operator tick (from the watchdog: heartbeat stale, jobs are due)"
    tmux send-keys -t "=$SESSION:" Enter ;;
  *) log "unexpected watchdog action: $act" ;;
esac
find "$LOGDIR" -name '*.log' -mtime +30 -delete 2>/dev/null
exit 0
