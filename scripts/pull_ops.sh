#!/usr/bin/env bash
# Mac: bring the operator's Spark-owned files back into this repo for review and commits (no media).
#   scripts/pull_ops.sh               # operator paths: data/, episodes/op-*/, research/corpus/*/auto/, out/op-*/
#   scripts/pull_ops.sh --all         # every path in scripts/spark_owned.txt (research ledgers, audio timings, mixes' json)
#   scripts/pull_ops.sh --proposals   # then list data/proposals/*.patch waiting for a Mac session to apply
#   scripts/pull_ops.sh --dry-run     # show what would be copied
# Media is never pulled (*.mp4 *.wav *.mov *.webm *.m4a *.npy); keep the Mac's out/ under 2 GB (BRIEF).
# Never deletes anything on either side; --update keeps a newer Mac file. Commit what you want afterwards.
# The list comes from scripts/spark_owned.txt (owned by L1); the built-in copy below is used until that exists.
set -euo pipefail
HOST="${SPARK_HOST:-dgx-spark}"
REMOTE_APP="${REMOTE_APP:-studio/app}"
cd "$(dirname "$0")/.."
DRY=""; PROPOSALS=0; ALL=0
for a in "$@"; do case "$a" in --dry-run|-n) DRY="-n";; --proposals) PROPOSALS=1;; --all) ALL=1;; *) sed -n '2,10p' "$0"; exit 2;; esac; done
if [ "$ALL" = 0 ]; then
  PATTERNS='/data/
/episodes/op-*/
/research/corpus/*/auto/
/out/op-*/'
elif [ -f scripts/spark_owned.txt ]; then
  PATTERNS="$(grep -vE '^\s*(#|$)' scripts/spark_owned.txt)"
else
  PATTERNS='/data/
/episodes/op-*/
/research/corpus/*/auto/
/research/library.jsonl
/research/library.state.json
/research/daily/
/studio/public/episodes/
/studio/public/music/*.wav
/episodes/*/audio/
/out/'
fi
# expand the anchored globs on the Spark into the paths that exist
LIST="$(mktemp)"; trap 'rm -f "$LIST"' EXIT
GLOBS="$(printf '%s\n' "$PATTERNS" | sed -e 's#^/##' -e 's#/$##' | tr '\n' ' ')"
ssh "$HOST" "cd ~/$REMOTE_APP && for g in $GLOBS; do for p in \$g; do [ -e \"\$p\" ] && echo \"\$p\"; done; done; true" >"$LIST"
if [ ! -s "$LIST" ]; then echo "[pull_ops] nothing to pull"; exit 0; fi
echo "[pull_ops] $(wc -l <"$LIST" | tr -d ' ') path(s) from $HOST:~/$REMOTE_APP"
rsync -a -r --update --relative $DRY --files-from="$LIST" \
  --exclude '*.mp4' --exclude '*.wav' --exclude '*.mov' --exclude '*.webm' --exclude '*.m4a' --exclude '*.npy' \
  --exclude '*.lock' --exclude '*.tmp.*' --exclude 'logs/' --exclude 'claude_settings.json' --exclude 'launch.sh' \
  --itemize-changes "$HOST:$REMOTE_APP/" ./ | grep -v '^\.' || true
if [ "$PROPOSALS" = 1 ]; then
  echo "[pull_ops] proposals (apply on the Mac after review, commit, sync, then mark repo_applied):"
  ls -1 data/proposals/*.patch 2>/dev/null || echo "  (none)"
fi
du -sh out 2>/dev/null | sed 's/^/[pull_ops] out\/ is now /'
