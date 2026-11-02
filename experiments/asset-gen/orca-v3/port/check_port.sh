#!/usr/bin/env bash
# Port dry run (does NOT touch studio/): copies studio/src to a temp dir, drops OrcaV3.tsx + geom_v3.json +
# orcaV3Kit.tsx into kits/explainer/house/, bundles a small entry that draws the kit Figure (side, jaw/pec, front,
# below, far plane with cold light + haze, silhouette) through the real kit light/tint/blink code, and renders
# orca-v3/out/port_check.png. 'remotion' is stubbed (only motion.ts's imports are touched at load time).
set -euo pipefail
AG="$(cd "$(dirname "$0")/../.." && pwd)"
ROOT="$(cd "$AG/../.." && pwd)"
T="$(mktemp -d)"
trap 'rm -rf "$T"' EXIT
cp -R "$ROOT/studio/src" "$T/src"
H="$T/src/kits/explainer/house"
cp "$AG/orca-v3/OrcaV3.tsx" "$AG/orca-v3/geom_v3.json" "$AG/orca-v3/port/orcaV3Kit.tsx" "$H/"
cp "$AG/orca-v3/port/check/entry.tsx" "$AG/orca-v3/port/check/remotion_stub.js" "$T/"
cd "$T"
NODE_PATH="$AG/node_modules" "$AG/node_modules/.bin/esbuild" entry.tsx --bundle --platform=node --format=cjs --outfile=entry.cjs \
	--log-level=warning --alias:remotion=./remotion_stub.js --jsx=automatic
node entry.cjs "$T/port.svg"
rsvg-convert -w 1150 "$T/port.svg" -o "$AG/orca-v3/out/port_check.png"
echo "$AG/orca-v3/out/port_check.png"
