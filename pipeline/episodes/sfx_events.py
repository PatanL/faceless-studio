"""Action SFX from a built storyboard (FEEDBACK A2 "sound effects land on the action", rubric 2.9 / STYLE_BIBLE §12).

The polish-2d cue set (experiments/polish-2d/audio/cues.json) was hand-written for 10 s; this derives the same vocabulary
from the storyboard data for a whole episode, so every house build gets it:

  pull-back     whoosh_long under a pre-rolled opening camera move (frame 0 is the cover)
  drops         knock on every dropSquash landing (the camera kick frame), pitch-varied so four cars never sound stamped
  pops          pop on every popSpring / pop entrance (figures, bubbles, map pins), pitch-varied
  labels        tick when a lantern tag lands, a fast whoosh (zip) when a title plate wipes in, zip + click for a gauge
  impacts       impact on a white hit flash or a hard camera shake (amplitude >= 10)
  punches       a short airy whoosh on big punch-ins (zoom +0.12 or more), at most one per 2.5 s
  light event   sonar_ping when the colour key shifts (the warm proof light / a re-key), the house light event
  list beats    tick on each strike in an Options list, ding on the select

Scene cuts already get a whoosh/bubbles from pipeline.audio.make.cut_cues (one per paragraph), so transitions are not
repeated here. Cues closer than MIN_GAP keep the higher-priority one. Times are global seconds.

usage: python3 -m pipeline.episodes.sfx_events episodes/<slug>/storyboard.json [-o episodes/<slug>/audio/sfx_events.json]
then:  python -m pipeline.audio.make episodes/<slug>/script.md --reuse-tts --extra-cues episodes/<slug>/audio/sfx_events.json
"""
from __future__ import annotations

import argparse
import json
import os
import random

MIN_GAP = 0.1
FIGURE_PREFIX = "explainer/"
LABEL_TICK = {"explainer/Tag"}
PRIORITY = {"impact": 0, "knock": 1, "sonar_ping": 2, "pop": 3, "ding": 3, "click": 4, "whoosh_long": 4, "whoosh": 5, "tick": 6}


def _rate(rng: random.Random, lo: float, hi: float) -> float:
    return round(lo + (hi - lo) * rng.random(), 3)


def scene_cues(sc: dict, t0: float, rng: random.Random, first: bool) -> list[dict]:
    out: list[dict] = []
    add = lambda cue, at, why, db=0.0, rate=1.0: out.append(
        {"cue": cue, "at": round(t0 + at, 3), "db": db, "rate": rate, "why": f"{sc['id']} {why}"})
    dur = sc["duration"]
    cam = sc.get("camera") or {}
    if first and cam.get("preroll"):
        add("whoosh_long", 0.0, "pre-rolled pull-back from the cover", db=-4, rate=0.85)
    for l in sc.get("layers", []):
        if l.get("role") == "dressing":
            continue
        name = l.get("name") or l.get("type")
        p = l.get("props") or {}
        en = l.get("enter") or {}
        at = en.get("at", l.get("start"))
        if en.get("type") == "dropSquash" and isinstance(at, (int, float)):
            land = at + min(0.22, en.get("duration", 0.5) * 0.4)
            add("knock", land, f"{name} lands", db=-1, rate=_rate(rng, 0.7, 0.86))
        elif en.get("type") in ("popSpring", "pop") and isinstance(at, (int, float)) and at > 0.05:
            add("pop", at, f"{name} pops in", db=-2, rate=_rate(rng, 0.62, 1.05))
        if name in LABEL_TICK and isinstance(p.get("at"), (int, float)) and p["at"] > 0.05:
            add("tick", p["at"], f"tag {p.get('text', '')!r} lands", db=2, rate=_rate(rng, 0.9, 1.15))
        if name == "explainer/Headline" and isinstance(p.get("at"), (int, float)) and p["at"] > 0.05:
            add("whoosh", p["at"], f"title plate {p.get('text', '')!r} wipes in", db=-4, rate=1.5)
        if name == "explainer/ScaleBar" and isinstance(p.get("at"), (int, float)):
            add("whoosh", p["at"], "gauge draws out (zip)", db=-6, rate=1.4)
            add("click", p["at"] + p.get("duration", 0.6), "gauge end rings land", db=1)
        if name == "explainer/Stat" and isinstance(p.get("at"), (int, float)) and p["at"] > 0.05:
            add("click", p["at"], "stat lands", db=1)
        if name == "explainer/Options":
            for s in p.get("strikes") or []:
                if isinstance(s.get("at"), (int, float)) and s["at"] > 0.05:
                    add("tick", s["at"], "option struck", db=4, rate=0.8)
            sel = p.get("select") or {}
            if isinstance(sel.get("at"), (int, float)) and sel["at"] > 0.05:
                add("ding", sel["at"], "answer selected", db=-2)
        if name == "explainer/Map":
            for pin in p.get("pins") or []:
                if isinstance(pin.get("at"), (int, float)) and pin["at"] > 0.05:
                    add("pop", pin["at"], "map pin", db=-2, rate=1.1)
        if l.get("type") == "rect" and str(l.get("fill", "")).lower() in ("#fff", "#ffffff") and isinstance(l.get("start"), (int, float)):
            add("impact", l["start"], "hit flash", db=-1, rate=0.85)
    for s in cam.get("shake", []):
        if s.get("decay", True) and s.get("amplitude", 0) >= 10:
            add("impact", s["at"], "hard camera shake", db=-2, rate=_rate(rng, 0.75, 0.9))
    kfs = sorted(cam.get("keyframes") or [], key=lambda k: k["t"])
    last = -9.0
    for a, b in zip(kfs, kfs[1:]):
        za, zb = a.get("zoom"), b.get("zoom")
        if isinstance(za, (int, float)) and isinstance(zb, (int, float)) and zb - za >= 0.12 and b["t"] - last >= 2.5:
            add("whoosh", max(0.0, a["t"] - 0.05), "punch-in", db=-8, rate=_rate(rng, 1.3, 1.7))
            last = b["t"]
    bg = (sc.get("background") or {}).get("props") or {}
    if isinstance(bg.get("shiftAt"), (int, float)):
        add("sonar_ping", bg["shiftAt"], f"light event: key shifts to {bg.get('shiftTo')}", db=-3, rate=0.9)
    return [c for c in out if 0 <= c["at"] - t0 <= dur]


def thin(cues: list[dict]) -> list[dict]:
    """keep the higher-priority cue when two land within MIN_GAP"""
    kept: list[dict] = []
    for c in sorted(cues, key=lambda c: (PRIORITY.get(c["cue"], 9), c["at"])):
        if all(abs(c["at"] - k["at"]) >= MIN_GAP for k in kept):
            kept.append(c)
    return sorted(kept, key=lambda c: c["at"])


def events(sb: dict, seed: str | None = None) -> list[dict]:
    rng = random.Random(seed or sb.get("id", "sfx"))
    out, t0 = [], 0.0
    for i, sc in enumerate(sb["scenes"]):
        out += scene_cues(sc, t0, rng, i == 0)
        t0 += sc["duration"]
    return thin(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("storyboard")
    ap.add_argument("-o", "--out")
    a = ap.parse_args(argv)
    sb = json.load(open(a.storyboard))
    ev = events(sb)
    out = a.out or os.path.join(os.path.dirname(a.storyboard), "audio", "sfx_events.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(ev, open(out, "w"), indent=1, ensure_ascii=False)
    kinds = {}
    for c in ev:
        kinds[c["cue"]] = kinds.get(c["cue"], 0) + 1
    print(f"{a.storyboard}: {len(ev)} action cues -> {out} {kinds}")


if __name__ == "__main__":
    main()
