#!/usr/bin/env python3
"""Write storyboards/explainer-showcase.json: a 20 s 16:9 tour of the explainer kit.

usage: python3 studio/scripts/gen_explainer_showcase.py
"""
import json
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "storyboards", "explainer-showcase.json")


def comp(name, x, y, w, h, props=None, **kw):
    layer = {"type": "component", "name": name, "x": x, "y": y, "width": w, "height": h, "props": props or {}}
    layer.update(kw)
    return layer


def ocean(depth, **props):
    return {"type": "component", "name": "explainer/Ocean", "depth": 0.12, "overscan": 1.2, "props": {"depth": depth, **props}}


def headline(text, at=0.2, y="12%", size=64, **props):
    return comp("explainer/Headline", "50%", y, 1600, size * 3, {"text": text, "at": at, "size": size, **props}, depth=0)


scenes = []

# 1 -- the dive: diver sinking past the surface light, depth meter ticking
d1 = [{"t": 0, "v": 15}, {"t": 2.6, "v": 140, "ease": "linear"}]
scenes.append({
    "id": "dive", "duration": 2.6,
    "background": ocean(d1, rays=9, snow=90),
    "camera": {"preset": "drift", "amount": 1},
    "layers": [
        comp("explainer/Diver", "40%", "60%", 900, 170, {"bubbles": True},
             keyframes=[{"t": 0, "x": "30%", "y": "56%"}, {"t": 2.6, "x": "52%", "y": "62%", "ease": "linear"}]),
        comp("explainer/DepthMeter", "90%", "50%", 300, 900, {"depth": d1, "max": 500, "step": 100, "size": 44}, depth=0),
        headline("You vs. the deep", at=0.3, y="20%", size=88, underline=True, color="white", sub="explainer kit"),
    ],
})

# 2 -- scale: sperm whale vs a city bus at true scale
PPM = 70
scenes.append({
    "id": "scale", "duration": 2.8,
    "transitionIn": {"type": "fade", "duration": 0.35},
    "background": ocean(260, rays=7, snow=70),
    "camera": {"preset": "pushIn", "amount": 0.6},
    "layers": [
        comp("explainer/SpermWhale", "50%", "42%", 1400, 400, {"pxPerM": PPM}, idle=[{"type": "bob", "amount": 6, "speed": 0.4}],
             enter={"type": "fade", "duration": 0.4}),
        comp("explainer/ScaleBar", "50%", "62%", 16 * PPM, 140, {"label": "~16 M", "at": 0.3, "labelSize": 44}),
        comp("explainer/Bus", "50%", "84%", 1000, 300, {"pxPerM": PPM}, start=1.1,
             keyframes=[{"t": 1.1, "y": "120%"}, {"t": 1.55, "y": "84%", "ease": "backOut"}]),
        headline("Longer than a city bus", at=1.5, y="11%", size=56, underline=True, color="red"),
    ],
})

# 3 -- the roster: all ten creatures, idle-animated
roster = ["spermWhale", "blueWhale", "orca", "greatWhite", "colossalSquid",
          "anglerfish", "octopus", "crocodile", "hippo", "grizzly"]
names = ["SPERM WHALE", "BLUE WHALE", "ORCA", "GREAT WHITE", "COLOSSAL SQUID",
         "ANGLERFISH", "GIANT OCTOPUS", "SALTWATER CROC", "HIPPO", "GRIZZLY"]
layers = [headline("The lineup", at=0.0, y="10%", size=58, underline=True)]
for i, (sp, nm) in enumerate(zip(roster, names)):
    cx = 270 + (i % 5) * 345
    cy = 400 if i < 5 else 770
    at = 0.15 + i * 0.07
    pop = {"type": "pop", "at": at, "duration": 0.35}
    layers.append({"type": "rect", "x": cx, "y": cy, "width": 320, "height": 330, "radius": 18,
                   "fill": "rgba(4,16,23,0.62)", "stroke": "rgba(190,230,240,0.18)", "strokeWidth": 2,
                   "start": at, "enter": pop, "depth": 0.9})
    h = 230 if sp in ("octopus", "grizzly", "hippo", "anglerfish") else 190
    layers.append(comp("explainer/Creature", cx, cy - 30, 270, h, {"species": sp, "timeOffset": i * 0.37},
                       start=at, enter=pop, depth=0.9))
    layers.append({"type": "text", "text": nm, "x": cx, "y": cy + 128, "fontSize": 25, "weight": 900,
                   "letterSpacing": 0.06, "color": "#f3f6f7", "start": at, "enter": pop, "depth": 0.9})
scenes.append({
    "id": "roster", "duration": 2.8,
    "transitionIn": {"type": "whip", "duration": 0.35, "direction": "left"},
    "background": ocean(420, rays=5, snow=60),
    "camera": {"preset": "pushIn", "amount": 0.4},
    "layers": layers,
})

# 4 -- height chart wall
scenes.append({
    "id": "heights", "duration": 2.6,
    "transitionIn": {"type": "fade", "duration": 0.3},
    "background": ocean(500, rays=3, snow=40),
    "layers": [
        headline("How tall is trouble?", at=0.0, y="9%", size=54, underline=True),
        comp("explainer/HeightChart", "50%", "57%", 1760, 860, {
            "maxM": 3.5, "stepM": 0.5, "at": 0.0, "size": 28, "gap": 50,
            "entries": [
                {"kind": "you", "label": "You", "at": 0.3},
                {"kind": "grizzly", "pose": "standing", "label": "Grizzly", "at": 0.6},
                {"kind": "hippo", "label": "Hippo", "heightM": 1.6, "at": 0.9},
                {"kind": "elephant", "label": "Elephant", "at": 1.2},
            ]}),
    ],
})

# 5 -- map zoom + stat callout
scenes.append({
    "id": "map", "duration": 2.6,
    "transitionIn": {"type": "dipBlack", "duration": 0.35},
    "background": {"type": "color", "color": "#04121a"},
    "layers": [
        comp("explainer/Map", "50%", "50%", 1920, 1080, {
            "views": [{"t": 0, "lon": -45, "lat": 20, "zoom": 1.15},
                      {"t": 0.4, "lon": -45, "lat": 20, "zoom": 1.15},
                      {"t": 1.7, "place": "dominica", "zoom": 30}],
            "rings": [{"place": "dominica", "r": 0.45, "at": 1.6, "label": "Dominica"}],
        }, depth=0),
        comp("explainer/Tag", "16%", "12%", 600, 90, {"text": "Caribbean Sea", "at": 0.2, "size": 28}, depth=0),
        comp("explainer/Stat", "18%", "82%", 560, 240, {"value": 6500, "prefix": "~", "label": "Codas analysed",
                                                        "at": 1.1, "duration": 1.2, "size": 78}, depth=0),
    ],
})

# 6 -- options list + countdown
scenes.append({
    "id": "options", "duration": 2.6,
    "transitionIn": {"type": "fade", "duration": 0.3},
    "background": ocean(180, rays=6, snow=60),
    "layers": [
        comp("explainer/Options", "34%", "50%", 1000, 800, {
            "items": ["Swim away", "Dive down and hide", "Stay perfectly still", "Scare it off"],
            "at": 0.0, "stagger": 0.1, "size": 46,
            "strikes": [{"index": 0, "at": 0.8}, {"index": 1, "at": 1.25}],
            "select": {"index": 2, "at": 1.75}}),
        comp("explainer/Timer", "77%", "42%", 460, 460, {"from": 7, "to": 0, "at": 0.1, "style": "ring", "format": "s",
                                                         "label": "seconds of air", "warnBelow": 5.4, "size": 150}, depth=0),
        comp("explainer/Diver", "77%", "84%", 520, 110, {"torch": True, "beam": 520, "speed": 1.3}),
    ],
})

# 7 -- speed bars with an orca crossing
scenes.append({
    "id": "speed", "duration": 2.0,
    "transitionIn": {"type": "whip", "duration": 0.3, "direction": "up"},
    "background": ocean(90, rays=8, snow=70),
    "layers": [
        comp("explainer/SpeedBars", "50%", "34%", 1500, 460, {
            "title": "Top speed", "max": 60, "at": 0.0, "stagger": 0.15, "duration": 0.8, "size": 40,
            "rows": [{"label": "You", "value": 3, "color": "#f3f6f7"},
                     {"label": "Sperm whale", "value": 30, "color": "#9aa3a9"},
                     {"label": "Great white", "value": 40, "color": "#6fd6e8"},
                     {"label": "Orca", "value": 55, "color": "red"}]}, depth=0),
        comp("explainer/Orca", "50%", "78%", 760, 250, {"speed": 1.6},
             keyframes=[{"t": 0, "x": "-22%"}, {"t": 2.0, "x": "92%", "ease": "linear"}]),
    ],
})

# 8 -- the abyss: anglerfish + colossal squid, scrolling depth meter
d8 = [{"t": 0, "v": 950}, {"t": 2.0, "v": 2000, "ease": "out"}]
scenes.append({
    "id": "abyss", "duration": 2.0,
    "transitionIn": {"type": "dipBlack", "duration": 0.3},
    "background": ocean(d8, rays=4, snow=80, drift=0.6),
    "camera": {"preset": "pushIn", "amount": 0.5},
    "layers": [
        comp("explainer/ColossalSquid", "58%", "52%", 980, 320, {"speed": 0.8}, idle=[{"type": "float", "amount": 10, "speed": 0.3}]),
        comp("explainer/Anglerfish", "22%", "66%", 360, 230, {}, idle=[{"type": "bob", "amount": 8, "speed": 0.5}]),
        comp("explainer/DepthMeter", "90%", "50%", 300, 900, {"depth": d8, "window": 900, "step": 200, "size": 44,
                                                             "zones": [{"from": 1000, "to": 2400, "color": "#e5483d"}]}, depth=0),
        headline("No sunlight. No way out.", at=0.3, y="12%", size=56, underline=True, color="red"),
    ],
})

sb = {
    "version": 1,
    "id": "explainer-showcase",
    "title": "Explainer kit showcase",
    "format": "16:9",
    "fps": 30,
    "scenes": scenes,
    # explicit, so Remotion's defaultProps (test storyboard captions/music) never merge in
    "captions": {"enabled": False, "words": []},
    "audio": {"voice": [], "music": [], "sfx": []},
    "overlays": {"grain": 0.03, "vignette": 0.15, "fadeIn": 0.2, "fadeOut": 0.4},
}
assert abs(sum(s["duration"] for s in scenes) - 20) < 1e-6, sum(s["duration"] for s in scenes)
with open(OUT, "w") as f:
    json.dump(sb, f, indent=1)
print("wrote", os.path.normpath(OUT), len(scenes), "scenes")

# ---- 6 s vertical (9:16) sample: same components laid out for Shorts ----
PPMV = 52
vert = [
    {"id": "v-scale", "duration": 2.0,
     "background": ocean(260, rays=6, snow=60),
     "layers": [
         comp("explainer/SpermWhale", "50%", "36%", 1000, 300, {"pxPerM": PPMV}),
         comp("explainer/ScaleBar", "50%", "47%", 16 * PPMV, 140, {"label": "~16 M", "at": 0.2}),
         comp("explainer/Bus", "50%", "58%", 800, 200, {"pxPerM": PPMV}, start=0.6,
              keyframes=[{"t": 0.6, "y": "110%"}, {"t": 1.0, "y": "58%", "ease": "backOut"}]),
         comp("explainer/Headline", "50%", "20%", 1000, 200, {"text": "Bigger than\na city bus", "size": 72, "underline": True, "color": "red"}, depth=0),
     ]},
    {"id": "v-options", "duration": 2.0, "transitionIn": {"type": "fade", "duration": 0.3},
     "background": ocean(150, rays=6, snow=60),
     "layers": [
         comp("explainer/Timer", "50%", "24%", 440, 440, {"from": 7, "style": "ring", "format": "s", "label": "seconds of air", "size": 150}, depth=0),
         comp("explainer/Options", "50%", "52%", 1000, 700, {"items": ["Swim away", "Hide", "Stay still", "Scare it off"], "size": 54,
                                                              "strikes": [{"index": 0, "at": 0.6}, {"index": 1, "at": 0.9}], "select": {"index": 2, "at": 1.3}}, depth=0),
     ]},
    {"id": "v-heights", "duration": 2.0, "transitionIn": {"type": "whip", "duration": 0.3},
     "background": ocean(400, rays=3, snow=40),
     "layers": [
         comp("explainer/HeightChart", "50%", "45%", 1000, 900, {"maxM": 3, "size": 30, "gap": 40, "entries": [
             {"kind": "you", "label": "You"}, {"kind": "grizzly", "pose": "standing", "label": "Grizzly"}]}),
         comp("explainer/Stat", "50%", "72%", 700, 260, {"value": 2.7, "decimals": 1, "suffix": " m", "label": "standing grizzly", "at": 0.8, "size": 96}, depth=0),
     ]},
]
sbv = {"version": 1, "id": "explainer-9x16", "format": "9:16", "fps": 30, "scenes": vert,
       "captions": {"enabled": False, "words": []}, "audio": {"voice": [], "music": [], "sfx": []},
       "overlays": {"vignette": 0.15}}
OUTV = os.path.join(os.path.dirname(__file__), "..", "storyboards", "explainer-9x16.json")
with open(OUTV, "w") as f:
    json.dump(sbv, f, indent=1)
print("wrote", os.path.normpath(OUTV))
