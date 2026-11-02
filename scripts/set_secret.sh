#!/usr/bin/env bash
# Store credentials in ~/studio/.env on the DGX Spark (mode 600) without them appearing on screen, in shell history,
# in a command line (ps) or in any file on the Mac.
#
# usage (on the Mac, in your own terminal):
#   scripts/set_secret.sh                 # Buffer setup: API key, then lists your channel ids and asks for them
#   scripts/set_secret.sh NAME [NAME...]  # set specific variables, e.g. scripts/set_secret.sh IG_ACCESS_TOKEN
#   scripts/set_secret.sh --clipboard NAME  # set NAME from the Mac clipboard without showing it
#
# Values are sent over ssh on stdin to a small Python writer on the Spark that replaces or appends NAME=value.
set -euo pipefail
HOST=${STUDIO_HOST:-dgx-spark}

write_var() {  # $1 = name, $2 = value (both via stdin to the remote side, never as arguments)
  printf '%s\n%s\n' "$1" "$2" | ssh "$HOST" 'python3 -c "
import os, re, sys
name = sys.stdin.readline().rstrip(\"\n\")
value = sys.stdin.readline().rstrip(\"\n\").strip()
if not re.fullmatch(r\"[A-Z][A-Z0-9_]*\", name) or \"\n\" in value:
    sys.exit(\"bad name or value\")
p = os.path.expanduser(\"~/studio/.env\")
os.makedirs(os.path.dirname(p), exist_ok=True)
lines = open(p).read().splitlines() if os.path.exists(p) else []
q = chr(39)
line = name + \"=\" + (q + value + q if (\" \" in value or \"#\" in value) and q not in value else value)
out, done = [], False
for l in lines:
    k = l.split(\"=\", 1)[0].strip().removeprefix(\"export \").strip()
    if k == name and not done:
        out.append(line); done = True
    elif k != name:
        out.append(l)
if not done:
    out.append(line)
fd = os.open(p + \".tmp\", os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
with os.fdopen(fd, \"w\") as f:
    f.write(\"\n\".join(out) + \"\n\")
os.replace(p + \".tmp\", p)
os.chmod(p, 0o600)
print(\"saved \" + name + \" (\" + str(len(value)) + \" characters)\")
"'
}

ask() {  # $1 = name, $2 = hidden (1) or shown (0)
  local v
  if [ "$2" = 1 ]; then
    IFS= read -r -s -p "$1 (hidden, paste then Enter; empty to skip): " v; echo
  else
    IFS= read -r -p "$1 (empty to skip): " v
  fi
  case "$1" in BUFFER_ORG_ID|BUFFER_CHANNEL_*)
    if [ -n "$v" ] && ! [[ "$v" =~ ^[0-9a-f]{24}$ ]]; then
      local yn
      read -r -p "That doesn't look like a Buffer id (usually 24 characters, 0-9 and a-f). Save it anyway? [y/N] " yn
      [ "$yn" = y ] || { echo "not saved"; return; }
    fi ;;
  esac
  [ -n "$v" ] && write_var "$1" "$v" || echo "skipped $1"
}

hidden_for() { case "$1" in *KEY*|*TOKEN*|*SECRET*|*PASSWORD*) echo 1 ;; *) echo 0 ;; esac; }

if [ "${1:-}" = "--clipboard" ] && [ -n "${2:-}" ]; then  # value = what's on the Mac clipboard (never shown)
  v=$(pbpaste)
  [ -n "$v" ] || { echo "clipboard is empty"; exit 1; }
  write_var "$2" "$v"
  exit 0
fi

if [ $# -gt 0 ]; then
  for n in "$@"; do ask "$n" "$(hidden_for "$n")"; done
  exit 0
fi

echo "Buffer setup. Get the key at Buffer > Settings > API (as the organization owner)."
ask BUFFER_API_KEY 1
if ! ssh "$HOST" 'grep -q "^BUFFER_API_KEY=." ~/studio/.env 2>/dev/null'; then
  echo "BUFFER_API_KEY is not saved (the hidden paste may not have registered). Run this script again and paste the key"
  echo "at the first, hidden prompt, then press Enter. Don't paste it at any of the later, visible prompts."
  exit 1
fi
echo
echo "Your Buffer organization and channels (from the Spark):"
if ! ssh "$HOST" 'cd ~/studio/app && source scripts/spark_env.sh >/dev/null 2>&1; ~/studio/.venv/bin/python -m pipeline.publish.buffer channels'; then
  echo "Couldn't list channels (is BUFFER_API_KEY set and valid?). Stopping before asking for ids."
  exit 1
fi
echo
echo "Copy the ids from the list above (they aren't secret, so they're shown as you type)."
ask BUFFER_ORG_ID 0
ask BUFFER_CHANNEL_YOUTUBE 0
ask BUFFER_CHANNEL_INSTAGRAM 0
ask BUFFER_CHANNEL_TIKTOK 0
write_var APPROVAL_MODE drafts
echo
echo "Done. Posting stays in drafts mode (APPROVAL_MODE=drafts): nothing goes out without your approval."
