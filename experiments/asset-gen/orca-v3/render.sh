#!/usr/bin/env bash
# Render OrcaV3 stills (react-dom/server + rsvg-convert + ffmpeg; light, fine on the Mac): orca-v3/out/*.png
set -euo pipefail
cd "$(dirname "$0")/.."
node_modules/.bin/esbuild orca-v3/render.tsx --bundle --platform=node --format=cjs --outfile=build/render_v3.cjs --log-level=warning
node build/render_v3.cjs
