#!/bin/zsh
# REPLICATION STUDY: bundle the study, render key stills, and tile theirs (top) over ours (bottom) at the same frames.
# usage: src/study/VS1Z/tools/keys.sh <tag> frame...   (run from experiments/three-lane)
set -e
TAG=$1; shift
OUT=../../out/study/VS1Z/keys/$TAG; REF=../../out/study/VS1Z/ref/ricks720_VS1Z_Q-Klt8.webm
mkdir -p $OUT
nice npx remotion bundle src/study/index.ts --out-dir /tmp/vs1z_bundle >/dev/null 2>&1
echo '{}' > /tmp/vs1z_props.json
nice node scripts/stills.mjs /tmp/vs1z_bundle /tmp/vs1z_props.json $OUT/ours VS1Z angle "$@" >/dev/null
python3 -I src/study/VS1Z/tools/tile_keys.py $REF $OUT "$@"
