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
from .common import ROOT, load, norm, storyboard, visual_events

MAX_HOLD = 3.0  # s: longest stretch with no visual event (cut, layer in/out, keyframe, camera key, shake)


def check_holds(slug: str, scenes: list[dict], limit: float = MAX_HOLD) -> list[str]:
    bad, t0 = [], 0.0
    for s in scenes:
        ev = visual_events(s)
        for a, b in zip(ev, ev[1:]):
            if b - a > limit:
                bad.append(f"{s['id']} {t0 + a:.1f}-{t0 + b:.1f}s ({b - a:.1f}s)")
        t0 += s["duration"]
    return bad


def mark_emphasis(words: list[dict], tokens: list) -> None:
    """tokens: ["swallow", ("never", 1), ...] -> words[i]["emph"] = True (nth match, default first)."""
    for tok in tokens:
        tok, nth = (tok, 0) if isinstance(tok, str) else tok
        hits = [w for w in words if norm(w["text"]) == norm(tok)]
        if len(hits) <= nth:
            raise SystemExit(f"emphasis word {tok!r} #{nth} not in narration")
        hits[nth]["emph"] = True

BUILDERS = {**{k: (v, explainer_eps) for k, v in explainer_eps.EPISODES.items()},
            **{k: (v, horror_eps) for k, v in horror_eps.EPISODES.items()}}


def build(slug: str) -> str:
    fn, mod = BUILDERS[slug]
    meta, scenes, words, total, source = load(slug)
    built = fn(scenes)
    if len(built) != len(scenes):
        raise SystemExit(f"{slug}: builder made {len(built)} scenes for {len(scenes)} paragraphs")
    mark_emphasis(words, getattr(mod, "EMPHASIS", {}).get(slug, []))
    holds = check_holds(slug, built)
    if holds:
        msg = f"{slug}: visual holds over {MAX_HOLD:.0f}s: " + "; ".join(holds)
        if slug in getattr(mod, "STRICT_HOLDS", ()):
            raise SystemExit(msg)
        print("WARN " + msg)
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
