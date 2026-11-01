#!/usr/bin/env python3
"""Render-readiness check for storyboards (no rendering, stdlib only, safe on the Mac or the Spark).

For each storyboard JSON it reports:
  components  every component name is registered by a kit in studio/src/kits (else it renders a
              magenta "missing: name" box)
  audio       every voice/music/sfx `src` exists under studio/public (mix.wav lives on the Spark only,
              so run this on the Spark for the audio column to mean anything)
  holds       longest stretch with no visual event, vs the 3.0 s pilot rule (pipeline/episodes/build.py)
Schema validation itself is `npm run validate` in studio/ (zod); this script complements it.

usage: python3 scripts/check_storyboards.py [storyboard.json ...]   (default: episodes/*/storyboard*.json)
exit 1 if any storyboard has missing components or missing audio.
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KITS = os.path.join(ROOT, "studio", "src", "kits")
PUBLIC = os.path.join(ROOT, "studio", "public")


def registered() -> set[str]:
    names: set[str] = set()
    for f in glob.glob(os.path.join(KITS, "**", "*.ts*"), recursive=True):
        src = open(f, encoding="utf-8").read()
        names |= set(re.findall(r"registerComponent\(\s*['\"]([^'\"]+)['\"]", src))
        # explainer/index.tsx registers a FIXED {Name: species} map with a template literal
        for prefix, var in re.findall(r"registerComponent\(\s*`([\w-]+)/\$\{(\w+)\}`", src):
            m = re.search(r"const\s+FIXED[^=]*=\s*\{(.*?)\};", src, re.S)
            if m:
                names |= {f"{prefix}/{k}" for k in re.findall(r"^\s*(\w+)\s*:", m.group(1), re.M)}
    return names


def components(sb: dict) -> set[str]:
    out = set()
    for s in sb.get("scenes", []):
        bg = s.get("background") or {}
        if bg.get("type") == "component":
            out.add(bg["name"])
        for layer in s.get("layers", []):
            if layer.get("type") == "component":
                out.add(layer["name"])
    return out


def audio_srcs(sb: dict) -> list[str]:
    a = sb.get("audio") or {}
    srcs = [c.get("src") for k in ("voice", "music", "sfx") for c in a.get(k, []) if c.get("src")]
    for s in sb.get("scenes", []):
        srcs += [c.get("src") for c in s.get("sfx", []) or [] if c.get("src")]
    return [x for x in srcs if not str(x).startswith("http")]


def max_hold(sb: dict) -> float:
    sys.path.insert(0, ROOT)
    try:
        from pipeline.episodes.common import visual_events
    except Exception:
        return float("nan")
    worst = 0.0
    for s in sb.get("scenes", []):
        ev = visual_events(s)
        for a, b in zip(ev, ev[1:]):
            worst = max(worst, b - a)
    return worst


def main(argv: list[str]) -> int:
    files = argv or sorted(glob.glob(os.path.join(ROOT, "episodes", "*", "storyboard*.json")))
    reg = registered()
    bad = 0
    print(f"{len(reg)} registered components")
    print(f"{'storyboard':58} {'fmt':5} {'secs':>6} {'hold':>5}  status")
    for f in files:
        sb = json.load(open(f))
        miss = sorted(components(sb) - reg)
        noaudio = [s for s in audio_srcs(sb) if not os.path.exists(os.path.join(PUBLIC, s))]
        secs = sum(s.get("duration", 0) for s in sb.get("scenes", []))
        hold = max_hold(sb)
        status = []
        if miss:
            status.append(f"MISSING {len(miss)} components: {', '.join(miss[:6])}{' ...' if len(miss) > 6 else ''}")
        if noaudio:
            status.append(f"NO AUDIO {', '.join(noaudio[:3])}")
        if hold > 3.0:
            status.append(f"holds>3s (max {hold:.1f}s)")
        bad += bool(miss or noaudio)
        print(f"{os.path.relpath(f, ROOT):58} {sb.get('format', '?'):5} {secs:6.1f} {hold:5.1f}  {'; '.join(status) or 'ready'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
