#!/usr/bin/env python3
"""explainer-sperm-whale, plates twin: storyboard.json -> storyboard_plates.json.

The same Short with Codex background plates instead of our flat code sets, for the owner's plates-vs-flat comparison
(lane B, 2026-11-02). Plates: experiments/asset-gen/gen/sw_plate_*_A.png (prompts/sw_plate_*_A.txt + style_A_common,
style board A attached), resized to studio/public/plates/explainer-sperm-whale/*.jpg.

Every place setting (scene background or an in-scene rig layer) draws its plate instead of the Ocean rig; the biome
set dressing the house pass added is dropped (the plate is the set) except the far specks, which keep a parallax plane
between the plate (depth 0.12) and the figures (1.0); a sparse foreground bubble plane (depth 1.45) is added so camera
moves and drift show three planes moving at different rates. Boards and map cards stay code (abstract beats).
"""
import copy
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "plates/explainer-sperm-whale/{}.jpg"


def plate_of(seg: dict) -> str | None:
    if not seg or seg.get("kind") != "place":
        return None
    if seg.get("biome") == "deep":
        return "deep"
    if seg.get("biome") == "twilight":
        return "twilight"
    if "Dominica" in str(seg.get("place", "")):
        return "dominica"
    if seg.get("light") == "dusk":
        return "dusk"
    return "surface"


def segs(sc):
    st = sc.get("setting")
    return st if isinstance(st, list) else [st] if st else []


def main():
    sb = json.load(open(os.path.join(HERE, "storyboard.json")))
    out = copy.deepcopy(sb)
    out["id"] = sb["id"] + "-plates"
    for sc in out["scenes"]:
        ss = segs(sc)
        first = next((s for s in ss if s.get("kind") != "map"), None)
        has_place = any(plate_of(s) for s in ss)
        layers = []
        if plate_of(first):
            # the plate is a layer (not the background) so it can drift: a slow push across the scene on top of the
            # camera's own moves (Ken Burns), on the background plane
            sc["background"] = {"type": "color", "color": "#14045c", "depth": 0.12, "overscan": 1.2}
            dur = sc["duration"]
            layers.append({"type": "image", "src": SRC.format(plate_of(first)), "fit": "cover", "role": "dressing",
                           "x": "50%", "y": "50%", "width": 1296, "height": 2304, "depth": 0.12, "z": -80,
                           "keyframes": [{"t": 0, "scale": 1.0, "y": "50%"}, {"t": dur, "scale": 1.045, "y": "49%", "ease": "linear"}]})
        later = [s for s in ss if s is not first and s.get("kind") == "place"]
        for l in sc["layers"]:
            if l.get("setting_rig"):
                # the rig of an in-scene place change: match it to its segment by start time
                seg = min(later, key=lambda s: abs(float(s.get("at", 0)) - float(l.get("start", 0)))) if later else None
                pl = plate_of(seg)
                if pl:
                    img = {k: l[k] for k in ("x", "y", "width", "height", "depth", "z", "start", "end", "enter") if k in l}
                    layers.append({"type": "image", "src": SRC.format(pl), "fit": "cover", "role": "dressing", **img})
                    continue
            if l.get("role") == "dressing" and str(l.get("name", "")).startswith("explainer/") and l.get("name") != "explainer/Specks":
                continue                       # kelp, fish schools, coast...: the plate is the set
            if l.get("type") == "rect" and l.get("role") == "fx" and has_place:
                continue                       # the midnight veil: the deep plate is already dark
            layers.append(l)
        if has_place:
            layers.append({"type": "particles", "preset": "bubbles", "count": 14, "seed": 7, "x": "50%", "y": "50%",
                           "width": 1300, "height": 2200, "depth": 1.45, "z": 25, "opacity": 0.45, "role": "dressing",
                           "color": "#e9f4fc", "size": [6, 16], "speed": 0.6})
        sc["layers"] = layers
    path = os.path.join(HERE, "storyboard_plates.json")
    json.dump(out, open(path, "w"), indent=1, ensure_ascii=False)
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
