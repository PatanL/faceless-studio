#!/bin/sh
# Re-create vendor/ at the exact commits reviewed in SETUP.md (vendor/ is git-ignored).
set -eu
V="$(cd "$(dirname "$0")/.." && pwd)/vendor"
mkdir -p "$V"
fetch() { # name url commit
  [ -d "$V/$1/.git" ] || git clone --quiet "$2" "$V/$1"
  git -C "$V/$1" fetch --quiet origin && git -C "$V/$1" checkout --quiet "$3"
  echo "$1 @ $(git -C "$V/$1" rev-parse HEAD)"
}
fetch cc-blender-skill https://github.com/RobLe3/cc-blender-skill a2634b588e80265e796aa53f8ab178d75105c2af
fetch mcp-for-blender  https://github.com/ahujasid/mcp-for-blender 992233bb258975a05eec8b5691465c50c2831e34
