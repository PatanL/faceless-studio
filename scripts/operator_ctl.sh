#!/usr/bin/env bash
# HUMAN switch for the operator (the operator session itself is blocked from running this).
#   scripts/operator_ctl.sh status
#   scripts/operator_ctl.sh pause ["reason"]            # config.paused=true: no new makes or posts; metrics continue
#   scripts/operator_ctl.sh unpause                     # clears config.paused AND the operator's own auto-pause
#                                                       # (two failed slots, exit 5, budget stop, kill rule)
#   scripts/operator_ctl.sh mode <youtube|tiktok|instagram|all> draft|auto
#   scripts/operator_ctl.sh disclosure <platform|all> yes|no   # you checked that platform's AI-content label works
#                                                              # without a manual toggle (needed for auto)
# A platform posts automatically only when ALL of: APPROVAL_MODE=auto (env or ~/studio/.env, read at session start),
# mode.<p>=auto and disclosure_ok_auto.<p>=true. Otherwise every post is a Buffer draft for you to approve.
# Runs on the Spark (from the Mac it re-runs itself over ssh).
set -euo pipefail
HOST="${SPARK_HOST:-dgx-spark}"
if [ "${OPERATOR_REMOTE:-auto}" = 1 ] || { [ "${OPERATOR_REMOTE:-auto}" = auto ] && [ "$(uname -s)" != Linux ]; }; then
  args=""; for a in "$@"; do args="$args $(printf '%q' "$a")"; done
  exec ssh "$HOST" "bash ~/studio/app/scripts/operator_ctl.sh$args"
fi
APP="${STUDIO_APP:-$HOME/studio/app}"
cd "$APP"
export STUDIO_DATA="${STUDIO_DATA:-$APP/data}"
python3 -m pipeline.ops.state init >/dev/null
CMD="${1:-status}"; shift || true
case "$CMD" in
  status|pause|unpause|mode|disclosure) ;;
  *) sed -n '2,13p' "$0"; exit 2 ;;
esac
python3 - "$CMD" "$@" <<'PY'
import json, os, sys
from pipeline.common import locks, timeutil
from pipeline.ops import paths, state as S
cmd, args = sys.argv[1], sys.argv[2:]
cfgp = paths.config_file()
PLAT = ["youtube", "tiktok", "instagram"]
def plats(p):
    if p == "all": return PLAT
    if p not in PLAT: sys.exit(f"platform must be one of {PLAT} or all")
    return [p]
with locks.flock(cfgp + ".lock", timeout_s=30):
    with open(cfgp, encoding="utf-8") as f:
        cfg = json.load(f)
    changed = True
    if cmd == "pause":
        cfg["paused"] = True; cfg["paused_reason"] = " ".join(args) or "human"; cfg["paused_at"] = timeutil.iso()
    elif cmd == "unpause":
        cfg["paused"] = False; cfg.pop("paused_reason", None)
        with S.updating() as st:
            st["paused"] = False; st["pause_reason"] = None
            st["counters"]["consecutive_failed_slots"] = 0; st["budget"]["stop_until"] = None
    elif cmd == "mode":
        if len(args) != 2 or args[1] not in ("draft", "auto"): sys.exit("usage: mode <platform|all> draft|auto")
        for p in plats(args[0]): cfg.setdefault("mode", {})[p] = args[1]
    elif cmd == "disclosure":
        if len(args) != 2 or args[1] not in ("yes", "no"): sys.exit("usage: disclosure <platform|all> yes|no")
        for p in plats(args[0]): cfg.setdefault("disclosure_ok_auto", {})[p] = args[1] == "yes"
    else:
        changed = False
    if changed:
        tmp = cfgp + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2); f.write("\n")
        os.replace(tmp, cfgp)
        S.journal(f"human: operator_ctl {cmd} {' '.join(args)}".strip())
full = S.load_config()
st = S.load_state()
appr = S.approval_mode()
print(f"paused: config={full.get('paused')} operator={st.get('paused')} ({st.get('pause_reason')})")
print(f"approval mode of the running session: {appr} (data/operator/approval_mode; set APPROVAL_MODE in ~/studio/.env, then operator_tmux.sh rotate)")
for p in full.get("platforms", PLAT):
    print(f"  {p:<10} mode={full['mode'].get(p)} disclosure_ok_auto={full['disclosure_ok_auto'].get(p)} -> posts as {S.effective_mode(full, p, appr)}")
PY
