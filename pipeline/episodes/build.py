#!/usr/bin/env python3
"""Build episodes/<slug>/storyboard.json from episodes/<slug>/script.md (+ audio/captions.json timings).

usage: python3 -m pipeline.episodes.build [slug ...]      (no args = every episode with a builder)

Timing comes from episodes/<slug>/audio/captions.json (pipeline.audio.make --meta-out episodes/<slug>/audio).
Without it, a words-per-minute estimate is used and the storyboard says so in "_built.timing".
"""
from __future__ import annotations

import json
import os
import sys

from . import explainer_eps, horror_eps
from .common import ROOT, load, storyboard

BUILDERS = {**{k: (v, explainer_eps) for k, v in explainer_eps.EPISODES.items()},
            **{k: (v, horror_eps) for k, v in horror_eps.EPISODES.items()}}


def build(slug: str) -> str:
    fn, mod = BUILDERS[slug]
    meta, scenes, words, total, source = load(slug)
    built = fn(scenes)
    if len(built) != len(scenes):
        raise SystemExit(f"{slug}: builder made {len(built)} scenes for {len(scenes)} paragraphs")
    sb = storyboard(slug, meta, built, words, total, mod.CAPTIONS, mod.OVERLAYS, source)
    out = os.path.join(ROOT, "episodes", slug, "storyboard.json")
    with open(out, "w") as f:
        json.dump(sb, f, indent=1, ensure_ascii=False)
    dur = sum(s["duration"] for s in built)
    print(f"{slug}: {len(built)} scenes, {dur:.1f}s, {len(words)} words, timing={source.split()[0]} -> {os.path.relpath(out, ROOT)}")
    return out


if __name__ == "__main__":
    for s in sys.argv[1:] or sorted(BUILDERS):
        build(s)
