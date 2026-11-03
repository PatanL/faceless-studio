#!/usr/bin/env bash
# usage: gen_one.sh <prompt.txt> <out-name>  -- generate one image with the Codex CLI image tool and copy it into gen/
set -euo pipefail
G="$(cd "$(dirname "$0")" && pwd)"
C=${CODEX:-/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex}
mkdir -p "$G/logs" "$G/gen"
cd "${TMPDIR:-/tmp}"
STAMP=$(mktemp); trap 'rm -f "$STAMP"' EXIT        # marks the start: only images newer than this count
"$C" exec --skip-git-repo-check -s read-only ${REF:+-i "$REF"} - < "$1" > "$G/logs/$2.log" 2>&1
# Codex now saves to ~/.codex/generated_images/<session>/<file>.png and may not print the path: take the newest image
# written there since this run started (fall back to a path printed in the log)
P=$(find "$HOME/.codex/generated_images" -type f -name '*.png' -newer "$STAMP" -print0 2>/dev/null | xargs -0 ls -t 2>/dev/null | head -1)
[ -n "$P" ] || P=$(grep -o '/Users/[^ ]*generated_images/[^ ]*\.png' "$G/logs/$2.log" | tail -1)
[ -n "$P" ] || { echo "no generated image found (see $G/logs/$2.log)" >&2; exit 1; }
cp "$P" "$G/gen/$2.png" && echo "$G/gen/$2.png"
