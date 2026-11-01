#!/usr/bin/env bash
# The operator: one Claude Code session in tmux session `studio-op` on the Spark, in ~/studio/app.
# See OPERATOR.md (what the session does) and docs/OPERATOR_DESIGN.md section 10.
#
#   scripts/operator_tmux.sh start      # fresh session (refuses if one is running); clears data/operator/STOPPED
#   scripts/operator_tmux.sh resume     # session gone: --resume <last id> if its transcript is < 24 h old, else fresh
#   scripts/operator_tmux.sh rotate     # graceful /exit, then a fresh session (watchdog does this at 04:00 local)
#   scripts/operator_tmux.sh stop       # graceful /exit; writes data/operator/STOPPED so the watchdog leaves it down
#   scripts/operator_tmux.sh attach     # watch / talk to it (detach: Ctrl-b d)
#   scripts/operator_tmux.sh status
#   scripts/operator_tmux.sh print-cmd  # show the launcher that start would run; changes nothing
#
# From the Mac every command re-runs itself on the Spark over `ssh -t dgx-spark` (OPERATOR_REMOTE=0 to disable).
#
# Approval: APPROVAL_MODE (environment, else the APPROVAL_MODE= line of ~/studio/.env, else `drafts`). While it is
# not `auto`, nothing auto-publishes: run.py posts every platform as a Buffer draft, the PreToolUse guard
# (pipeline/ops/guard.py) blocks --mode auto, and bypassPermissions is refused. The session runs with
# --permission-mode dontAsk (OPERATOR_PERMISSION_MODE) and the human's allowlist ~/studio/operator_settings.json
# (copy of scripts/operator_settings.example.json), merged with the guard into data/operator/claude_settings.json.
#
# Env: OPERATOR_TMUX (studio-op) STUDIO_APP (~/studio/app) STUDIO_DATA (<app>/data) CLAUDE_BIN (claude)
#      OPERATOR_MODEL (unset = claude default) OPERATOR_PERMISSION_MODE (dontAsk) OPERATOR_SETTINGS
#      (~/studio/operator_settings.json) OPERATOR_RESUME_MAX_H (24) SPARK_HOST (dgx-spark)
set -euo pipefail

HOST="${SPARK_HOST:-dgx-spark}"
REMOTE="${OPERATOR_REMOTE:-auto}"
if [ "$REMOTE" = 1 ] || { [ "$REMOTE" = auto ] && [ "$(uname -s)" != Linux ]; }; then
  args=""; for a in "$@"; do args="$args $(printf '%q' "$a")"; done
  exec ssh -t "$HOST" "bash ~/studio/app/scripts/operator_tmux.sh$args"
fi

CMD="${1:-status}"; shift || true
SESSION="${OPERATOR_TMUX:-studio-op}"
APP="$(cd "${STUDIO_APP:-$HOME/studio/app}" && pwd -P)"
DATA="${STUDIO_DATA:-$APP/data}"
OPS="$DATA/operator"
CLAUDE_BIN="${CLAUDE_BIN:-claude}"
PERM="${OPERATOR_PERMISSION_MODE:-dontAsk}"
ALLOW="${OPERATOR_SETTINGS:-$HOME/studio/operator_settings.json}"
MAX_H="${OPERATOR_RESUME_MAX_H:-24}"
PROMPT_FRESH="Read OPERATOR.md and run the resume protocol."
PROMPT_RESUME="Operator resumed after a restart. Read OPERATOR.md and run the resume protocol."
export PATH="$HOME/.local/bin:$HOME/studio/bin:$PATH"
cd "$APP"
mkdir -p "$OPS"

say() { echo "[operator_tmux] $*"; }
alive() { tmux has-session -t "=$SESSION" 2>/dev/null; }
pyops() { STUDIO_DATA="$DATA" python3 -m "$@"; }

approval_mode() {
  local v="${APPROVAL_MODE:-}"
  if [ -z "$v" ] && [ -r "$HOME/studio/.env" ]; then
    # read only this one key; never source the file (it holds secrets)
    v="$(grep -E '^[[:space:]]*APPROVAL_MODE=' "$HOME/studio/.env" | tail -1 | cut -d= -f2- | tr -d "\"' \r" || true)"
  fi
  [ "$v" = auto ] && echo auto || echo drafts
}

new_uuid() {
  cat /proc/sys/kernel/random/uuid 2>/dev/null || python3 -c 'import uuid; print(uuid.uuid4())'
}

transcript_age_h() {  # hours since the session transcript was written, or 9999
  local id="$1" proj f
  proj="$(printf '%s' "$APP" | sed 's#[^A-Za-z0-9]#-#g')"
  f="$HOME/.claude/projects/$proj/$id.jsonl"
  [ -f "$f" ] || { echo 9999; return; }
  echo $(( ( $(date +%s) - $(stat -c %Y "$f" 2>/dev/null || stat -f %m "$f") ) / 3600 ))
}

check_modes() {
  local appr="$1"
  case "$PERM" in acceptEdits|auto|manual|dontAsk|plan) ;; bypassPermissions)
    if [ "$appr" != auto ]; then
      say "refusing --permission-mode bypassPermissions while APPROVAL_MODE=$appr (would auto-approve publishing)"; exit 2
    fi ;;
  *) say "unknown OPERATOR_PERMISSION_MODE=$PERM"; exit 2 ;; esac
  if [ "$PERM" = dontAsk ] && [ ! -f "$ALLOW" ] && [ "${OPERATOR_ALLOW_NO_ALLOWLIST:-0}" != 1 ]; then
    say "no allowlist at $ALLOW: with dontAsk every tool call would be refused."
    say "Human step: review scripts/operator_settings.example.json, then cp it to $ALLOW (or set OPERATOR_SETTINGS)."
    exit 5
  fi
}

write_launcher() {  # $1 = fresh|resume, $2 = session id, $3 = settings path, $4 = launcher path
  local how="$1" id="$2" settings="$3" out="$4" appr; appr="$(approval_mode)"
  local sess_flag model_flag="" prompt
  if [ "$how" = fresh ]; then sess_flag="--session-id $id"; prompt="$PROMPT_FRESH"
  else sess_flag="--resume $id"; prompt="$PROMPT_RESUME"; fi
  [ -n "${OPERATOR_MODEL:-}" ] && model_flag="--model $(printf '%q' "$OPERATOR_MODEL")"
  cat >"$out" <<EOF
#!/usr/bin/env bash
# written by scripts/operator_tmux.sh $how at $(date -u +%FT%TZ); runs inside tmux session $SESSION
cd $(printf '%q' "$APP")
export STUDIO_LOCAL=1 TZ=America/Chicago CUDA_VISIBLE_DEVICES="" APPROVAL_MODE=$appr OPERATOR=1 OPERATOR_TMUX=$(printf '%q' "$SESSION")
$( [ -n "${STUDIO_DATA:-}" ] && echo "export STUDIO_DATA=$(printf '%q' "$STUDIO_DATA")" )
export PATH="\$HOME/.local/bin:\$HOME/studio/bin:\$PATH"
[ -f scripts/spark_env.sh ] && source scripts/spark_env.sh >/dev/null 2>&1
exec $(printf '%q' "$CLAUDE_BIN") --name $(printf '%q' "$SESSION") --permission-mode $PERM --settings $(printf '%q' "$settings") $sess_flag $model_flag $(printf '%q' "$prompt")
EOF
  chmod +x "$out"
}

launch() {  # $1 = fresh|resume
  local how="$1" appr id settings launcher
  if alive; then say "tmux session $SESSION is already running (attach: $0 attach)"; return 0; fi
  appr="$(approval_mode)"
  check_modes "$appr"
  pyops pipeline.ops.state init >/dev/null
  printf '%s\n' "$appr" >"$OPS/approval_mode"
  settings="$OPS/claude_settings.json"
  python3 -I "$APP/pipeline/ops/guard.py" settings --approval "$appr" --app "$APP" --base "$ALLOW" --out "$settings" >/dev/null
  id="$(cat "$OPS/session_id" 2>/dev/null || true)"
  if [ "$how" = resume ] && [ -n "$id" ] && [ "$(transcript_age_h "$id")" -lt "$MAX_H" ]; then
    pyops pipeline.ops.state heartbeat --resume
  else
    how=fresh; id="$(new_uuid)"; printf '%s\n' "$id" >"$OPS/session_id"
    pyops pipeline.ops.state session-start --id "$id" --tmux "$SESSION"
  fi
  launcher="$OPS/launch.sh"
  write_launcher "$how" "$id" "$settings" "$launcher"
  rm -f "$OPS/STOPPED"
  tmux new-session -d -s "$SESSION" -x 220 -y 50 -c "$APP" "bash $(printf '%q' "$launcher")"
  tmux set-option -t "=$SESSION:" history-limit 20000 >/dev/null 2>&1 || true
  pyops pipeline.ops.state journal "session $how (id $id, APPROVAL_MODE=$appr, permission-mode $PERM)"
  say "$how: tmux $SESSION, claude session $id, APPROVAL_MODE=$appr, permission-mode $PERM"
}

graceful_exit() {
  alive || return 0
  tmux send-keys -t "=$SESSION:" Escape
  sleep 1
  tmux send-keys -t "=$SESSION:" -l "/exit"
  tmux send-keys -t "=$SESSION:" Enter
  for _ in $(seq 1 30); do alive || return 0; sleep 1; done
  tmux send-keys -t "=$SESSION:" C-c; sleep 1; tmux send-keys -t "=$SESSION:" C-c
  for _ in $(seq 1 10); do alive || return 0; sleep 1; done
  tmux kill-session -t "=$SESSION" 2>/dev/null || true
}

case "$CMD" in
  start)
    if alive; then say "already running"; exit 0; fi
    rm -f "$OPS/STOPPED"; launch fresh ;;
  resume) launch resume ;;
  rotate)
    graceful_exit
    pyops pipeline.ops.state journal "session rotated" || true
    launch fresh ;;
  stop)
    graceful_exit
    date -u +%FT%TZ >"$OPS/STOPPED"
    pyops pipeline.ops.state journal "session stopped by operator_tmux.sh stop (watchdog will not restart it)" || true
    say "stopped; data/operator/STOPPED written (start clears it)" ;;
  attach) exec tmux attach -t "=$SESSION" ;;
  status)
    if alive; then say "tmux $SESSION: running"; else say "tmux $SESSION: not running"; fi
    [ -f "$OPS/STOPPED" ] && say "STOPPED flag set at $(cat "$OPS/STOPPED")"
    say "approval mode: $(approval_mode); permission mode: $PERM; allowlist: $([ -f "$ALLOW" ] && echo "$ALLOW" || echo "MISSING ($ALLOW)")"
    id="$(cat "$OPS/session_id" 2>/dev/null || true)"; [ -n "$id" ] && say "claude session $id (transcript age $(transcript_age_h "$id") h)"
    crontab -l 2>/dev/null | grep -q 'faceless-studio operator_watchdog' && say "watchdog cron: installed" || say "watchdog cron: not installed"
    [ -f "$OPS/state.json" ] && pyops pipeline.ops.state show --brief || say "no state.json yet" ;;
  print-cmd)
    appr="$(approval_mode)"; check_modes "$appr"
    tmp="$(mktemp -d)"
    python3 -I "$APP/pipeline/ops/guard.py" settings --approval "$appr" --app "$APP" --base "$ALLOW" --out "$tmp/claude_settings.json" >/dev/null
    write_launcher fresh "00000000-0000-4000-8000-000000000000" "$OPS/claude_settings.json" "$tmp/launch.sh"
    cat "$tmp/launch.sh"; echo "--- settings ($OPS/claude_settings.json)"; cat "$tmp/claude_settings.json"; rm -rf "$tmp" ;;
  *) sed -n '2,24p' "$0"; exit 2 ;;
esac
