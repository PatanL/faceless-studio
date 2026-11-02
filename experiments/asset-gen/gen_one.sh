#!/usr/bin/env bash
# usage: gen_one.sh <prompt.txt> <out-name>  -- generate one image with the Codex CLI image tool and copy it into gen/
set -euo pipefail
G="$(cd "$(dirname "$0")" && pwd)"
C=${CODEX:-/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex}
mkdir -p "$G/logs" "$G/gen"
cd "${TMPDIR:-/tmp}"
"$C" exec --skip-git-repo-check -s read-only - < "$1" > "$G/logs/$2.log" 2>&1
P=$(grep -o '/Users/[^ ]*generated_images/[^ ]*\.png' "$G/logs/$2.log" | tail -1)
cp "$P" "$G/gen/$2.png" && echo "$G/gen/$2.png"
