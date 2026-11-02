#!/usr/bin/env python3
"""explainer-sperm-whale: write shots.json (the studio-make shots step, by hand; built by pipeline/episodes/auto.py).

usage: python3 episodes/explainer-sperm-whale/make_shots.py      (then: python3 -m pipeline.episodes.auto explainer-sperm-whale --check)

Geometry: the style-A sperm whale (studio/src/kits/explainer/house/spermWhaleA.tsx) is 16 m snout to fluke; with
pxPerM p its snout sits 7.98 p px from the layer centre, the snout's middle 0.51 p px above it. Frame 0 (the cover)
and the last frame are the same picture (loop): the whale's head on the right facing the diver YOU, 1 m apart at true
scale, its clicks travelling into the diver.
"""
from __future__ import annotations

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
from pipeline.episodes.common import load  # noqa: E402

SLUG = "explainer-sperm-whale"
W, H = 1080, 1920
BONE, RED, CYAN, YELLOW, MAGENTA = "#e9f4fc", "red", "#0de9e0", "#fddf35", "#fb17b8"
pct = lambda px, n=W: f"{px / n * 100:.2f}%"


def whale(cx, cy, ppm, flip=False, **kw):
    """sperm whale layer centred at (cx, cy) px; kw: layer keys (keyframes, start, end, z, depth, idle...) or props"""
    layer_keys = {"keyframes", "start", "end", "z", "depth", "idle", "enter", "exit", "opacity", "allowOverlap", "role", "rotate"}
    lk = {k: kw.pop(k) for k in list(kw) if k in layer_keys}
    return {"type": "component", "name": "explainer/SpermWhale", "x": pct(cx), "y": pct(cy, H),
            "width": round(16.6 * ppm), "height": round(4.3 * ppm), "flipX": flip, "role": "hero",
            "props": {"pxPerM": ppm, **kw}, **lk}


def snout(cx, cy, ppm, flip=False):
    return (cx - 7.98 * ppm if flip else cx + 7.98 * ppm, cy - 0.51 * ppm)


def diver(cx, cy, ppm, **kw):
    lk = {k: kw.pop(k) for k in list(kw) if k in ("keyframes", "start", "end", "z", "enter", "idle", "flipX", "allowOverlap")}
    return {"type": "component", "name": "explainer/Diver", "x": pct(cx), "y": pct(cy, H), "width": round(2.6 * ppm + 20),
            "height": round(0.5 * ppm + 40), "props": {"pxPerM": ppm, "arms": "side", **kw}, **lk}


def tag(text, at, x, y, size=48, accent=None, leader=None, w=None, **kw):
    w = w or round(0.62 * size * len(text) + 90)
    p = {"text": text, "at": at, "size": size, "align": "center"}
    if accent:
        p["accent"] = accent
    if leader:
        p["leader"] = leader
    for k in ("out",):
        if k in kw:
            p[k] = kw.pop(k)
    return {"type": "component", "name": "explainer/Tag", "x": x, "y": y, "width": w, "height": round(size * 2.4),
            "depth": 0, "z": 20, "role": "label", "props": p, **kw}


def headline(text, at, y="13%", size=110, red=None, sub=None, **kw):
    p = {"text": text, "at": at, "size": size, "color": "white"}
    if red:
        p["red"] = red
    if sub:
        p.update(sub=sub, subColor="#d0dde3", subOpacity=0.9)
    for k in ("out",):
        if k in kw:
            p[k] = kw.pop(k)
    return {"type": "component", "name": "explainer/Headline", "x": "50%", "y": y, "width": 960,
            "height": round(size * 2.8), "depth": 0, "z": 20, "role": "label", "props": p, **kw}


def rings(x0, x1, cy, at, out=None, rate=3, dir=1, life=0.8, arc=38, h=360, color=BONE, width=12, opacity=1.0, **kw):
    """click rings from x0 (emitter) to x1, centred at cy (px)"""
    lo, hi = min(x0, x1), max(x0, x1)
    p = {"at": at, "rate": rate, "dir": dir, "life": life, "arc": arc, "color": color, "width": width, "opacity": opacity}
    if out is not None:
        p["out"] = out
    return {"type": "component", "name": "explainer/ClickRings", "x": pct((lo + hi) / 2), "y": pct(cy, H),
            "width": round(hi - lo), "height": h, "role": "fx", "z": 4, "props": p, **kw}


def svg(markup, x, y, w, h, **kw):
    return {"type": "svg", "x": x, "y": y, "width": w, "height": h, "markup": markup, "role": "prop", **kw}


def cam(*keys, drift=True):
    """keys: (t, zoom, x, y[, ease])"""
    out = []
    for k in keys:
        d = {"t": k[0], "zoom": k[1], "x": k[2], "y": k[3]}
        if len(k) > 4:
            d["ease"] = k[4]
        out.append(d)
    return {"keyframes": out}


TUB = ("<svg viewBox='0 0 120 70' xmlns='http://www.w3.org/2000/svg'><rect x='4' y='14' width='112' height='40' rx='18' "
       "fill='#e9f4fc'/><rect x='4' y='34' width='112' height='20' rx='10' fill='#bfd3ee'/><rect x='14' y='8' width='92' "
       "height='14' rx='7' fill='#fddf35'/><rect x='18' y='52' width='10' height='14' rx='4' fill='#bfd3ee'/>"
       "<rect x='92' y='52' width='10' height='14' rx='4' fill='#bfd3ee'/></svg>")
BRACKET = ("<svg viewBox='0 0 400 60' xmlns='http://www.w3.org/2000/svg' preserveAspectRatio='none'><path d='M 6 54 L 6 14 "
           "L 394 14 L 394 54' stroke='#e9f4fc' stroke-width='9' fill='none' stroke-linecap='round' stroke-linejoin='round'/></svg>")
DASH = ("<svg viewBox='0 0 600 40' xmlns='http://www.w3.org/2000/svg' preserveAspectRatio='none'><line x1='10' y1='20' "
        "x2='590' y2='20' stroke='#e9f4fc' stroke-width='7' stroke-dasharray='24 18' stroke-linecap='round'/></svg>")
HIT = ("<svg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'><circle cx='100' cy='100' r='92' fill='#fa302a' "
       "opacity='0.25'/><circle cx='100' cy='100' r='60' fill='none' stroke='#fa302a' stroke-width='10'/></svg>")
DRUM = ("<svg viewBox='0 0 120 110' xmlns='http://www.w3.org/2000/svg'><rect x='14' y='30' width='92' height='64' rx='10' "
        "fill='#fa302a'/><rect x='14' y='30' width='92' height='18' rx='9' fill='#fc6e0e'/><ellipse cx='60' cy='30' rx='46' "
        "ry='14' fill='#e9f4fc'/><path d='M 20 52 L 40 92 L 60 52 L 80 92 L 100 52' stroke='#fddf35' stroke-width='6' "
        "fill='none'/><rect x='70' y='0' width='8' height='34' rx='4' fill='#fddf35' transform='rotate(30 74 17)'/></svg>")

# ------------------------------------------------------------------ settings
SURFACE = {"kind": "place", "biome": "open_ocean", "place": "open ocean", "depth": 8, "waterline": 0.05, "light": "day"}
DEEP = {"kind": "place", "biome": "deep", "place": "deep sea, 1,000 m", "depth": 1000, "waterline": None, "light": "night"}
DOMINICA = {"kind": "place", "biome": "open_ocean", "place": "off Dominica", "depth": 4, "waterline": 0.2, "light": "day",
            "coast": {"kind": "hills"}, "cue": "Dominica"}
DUSK = {"kind": "place", "biome": "open_ocean", "place": "open ocean at dusk", "depth": 8, "waterline": 0.14, "light": "dusk"}

# cover (frame 0 = last frame): the whale's head on the right facing left, YOU 1 m in front of the snout
CP = 150                                   # px per metre on the cover
C_SNOUT = (560, 0.46 * H - 0.51 * CP)      # snout middle
C_WHALE = (C_SNOUT[0] + 7.98 * CP, 0.46 * H)
C_DIVER = (C_SNOUT[0] - 1.0 * CP - 1.3 * CP, C_SNOUT[1])
SWAY0 = 0.4                                # idle sway phase of the cover whale at t = 0
SWAY_SPEED = 0.2


def cover_layers(dur, at_head, end_state_only=False, swim_in=None):
    """the cover composition; swim_in = keyframes for the bookend whale (ends exactly at the cover position)"""
    w = whale(*C_WHALE, CP, flip=True, z=2, idle=[{"type": "sway", "amount": 0.5, "speed": SWAY_SPEED,
                                                      "phase": round(SWAY0 if not swim_in else
                                                                     SWAY0 - 2 * math.pi * SWAY_SPEED * dur, 4)}])
    if swim_in:
        w["keyframes"] = swim_in
        w["props"]["timeOffset"] = round((-dur) % 2.5, 3)    # swim wave period 2.5 s: last frame = frame 0
    rings_at = -1.0 if not swim_in else round(dur - 1.0, 3)
    return [
        w,
        rings(C_SNOUT[0] - 30, C_DIVER[0] + 1.3 * CP + 10, C_SNOUT[1], rings_at, rate=3, dir=-1, life=0.8, arc=40, h=380),
        diver(*C_DIVER, CP, z=3, allowOverlap=True),
        tag("YOU", 0 if not swim_in else -1, pct(C_DIVER[0]), pct(C_DIVER[1] - 120, H), size=46, leader=[0, 70]),
        headline("236 DECIBELS", at_head, red="236", sub="ONE CLICK, ONE METRE AWAY", size=112),
    ]


def build():
    meta, S, words, total, _ = load(SLUG)
    d = [s.dur for s in S]
    sc = []

    # p00 hook: frame 0 = cover
    sc.append({"p": 1, "beat": "hook", "setting": SURFACE,
               "layers": cover_layers(d[0], -0.6),
               "camera": cam((0, 1.0, "50%", "50%"), ("@click", 1.03, "48%", "48%"), ("@:end", 1.08, "44%", "46%", "inOut"))})

    # p01 scale: true-scale male, ~16 M gauge, nine YOU lying nose to tail, the head third bracketed
    P1 = 60
    wx, wy = 540, 0.30 * H
    yous = []
    for i in range(9):
        x = 540 - 4 * 105 + i * 105
        yous.append({"type": "component", "name": "explainer/You", "x": pct(x), "y": "50.5%", "width": 120, "height": 110,
                     "rotate": -90, "props": {"pxPerM": P1, "pose": "stand", "style": "diver"}, "start": f"@nine+{0.08 * i:.2f}",
                     "enter": {"type": "pop", "at": f"@nine+{0.08 * i:.2f}", "duration": 0.4}, "role": "prop", "z": 3})
    head0 = wx + 7.98 * P1 - 5.33 * P1
    sc.append({"p": 2, "beat": "scale", "setting": {"kind": "board", "board": "cyan"},
               "layers": [
                   whale(wx, wy, P1, z=2, keyframes=[{"t": 0, "x": "46%"}, {"t": "@:end", "x": "50%"}]),
                   {"type": "component", "name": "explainer/ScaleBar", "x": "50%", "y": "41.5%", "width": 16 * P1, "height": 140,
                    "role": "label", "props": {"label": "~16 M", "at": "@sixteen-0.1", "labelSize": 52}},
                   *yous,
                   svg(BRACKET, pct(head0 + 2.66 * P1), "21.6%", round(5.33 * P1), 50, start="@third",
                       enter={"type": "fade", "at": "@third", "duration": 0.25}, z=4, role="label"),
                   tag("1/3 HEAD", "@third+0.1", pct(head0 + 2.66 * P1), "15.5%", size=48),
               ],
               "camera": cam((0, 1.0, "50%", "50%"), ("@sixteen", 1.02, "50%", "48%"), ("@sixteen+0.3", 1.08, "50%", "45%", "out"),
                             ("@nine", 1.09, "50%", "46%"), ("@nine+0.4", 1.04, "50%", "48%", "out"),
                             ("@third", 1.05, "52%", "46%"), ("@third+0.35", 1.16, "66%", "38%", "out"),
                             ("@:end", 1.19, "67%", "37%"))})

    # p02 the organ: head cutaway fills amber, ten bathtubs, then the beam leaves the nose
    P2 = 100
    sx, sy = 700, 0.34 * H
    wcx = sx - 7.98 * P2
    tubs = []
    for i in range(10):
        r, c = divmod(i, 5)
        tubs.append(svg(TUB, pct(270 + c * 135), f"{49 + r * 5.4:.1f}%", 120, 70, start=f"@ten+{0.06 * i:.2f}",
                        enter={"type": "pop", "at": f"@ten+{0.06 * i:.2f}", "duration": 0.35}, end="@focus+0.3",
                        exit={"type": "fade", "at": "@focus-0.1", "duration": 0.4}, z=3))
    sc.append({"p": 3, "beat": "mechanism", "setting": {"kind": "board", "board": "violet"},
               "layers": [
                   whale(wcx, sy, P2, z=2, organ=[{"t": "@Nearly", "v": 0}, {"t": "@Nearly+0.7", "v": 1}],
                         click=[{"t": "@focus", "v": 0}, {"t": "@focus+0.2", "v": 1}]),
                   tag("≈ 2,000 L OF OIL", "@two", pct(sx - 2.6 * P2 + 20), "15%", size=48, leader=[0, 150]),
                   *tubs,
                   rings(sx + 6, 1075, sy - 0.51 * P2, "@focus", rate=4, dir=1, life=0.7, arc=20, h=300),
                   tag("BEAM", "@beam", "84%", "23%", size=48),
               ],
               "camera": cam((0, 1.0, "50%", "50%"), ("@Nearly", 1.03, "48%", "47%"), ("@Nearly+0.3", 1.12, "44%", "40%", "out"),
                             ("@ten", 1.12, "45%", "42%"), ("@ten+0.3", 1.02, "50%", "48%", "out"),
                             ("@focus", 1.03, "52%", "47%"), ("@focus+0.3", 1.1, "62%", "42%", "out"), ("@:end", 1.12, "63%", "41%"))})

    # p03 loudest: bars against the rivals on one underwater scale (dB re 1 uPa; bars from a 150 dB floor)
    P3 = 30
    sc.append({"p": 4, "beat": "record", "setting": {"kind": "board", "board": "blue"},
               "layers": [
                   {"type": "component", "name": "explainer/SpeedBars", "x": "50%", "y": "24%", "width": 940, "height": 560,
                    "role": "label", "depth": 0, "z": 15, "props": {
                        "title": "Loudest animals", "max": 90, "at": "@hit", "stagger": 2.3, "duration": 0.7, "size": 52,
                        "labelWidth": 360,
                        "rows": [{"label": "Sperm whale", "value": 86, "text": "236 dB", "color": "red"},
                                 {"label": "Snapping shrimp", "value": 39, "text": "189 dB", "color": CYAN},
                                 {"label": "Blue whale", "value": 38, "text": "188 dB", "color": BONE}]}},
                   whale(380, 0.52 * H, P3, z=2, keyframes=[{"t": 0, "x": "30%"}, {"t": "@:end", "x": "36%"}]),
                   rings(380 + 7.98 * P3 + 4, 1060, 0.52 * H - 0.51 * P3, "@hit", rate=3, dir=1, life=0.8, arc=34, h=320),
               ],
               "camera": cam((0, 1.0, "50%", "50%"), ("@decibels", 1.02, "50%", "48%"), ("@decibels+0.3", 1.08, "50%", "40%", "out"),
                             ("@louder", 1.09, "50%", "41%"), ("@louder+0.3", 1.03, "50%", "46%", "out"),
                             ("@blue", 1.04, "50%", "46%"), ("@blue+0.3", 1.1, "50%", "38%", "out"), ("@:end", 1.11, "50%", "38%"))})

    # p04 the dive: surface -> twilight -> deep, depth meter 0 -> 1,000 m, the whale goes head-down past the light
    P4 = 36
    sc.append({"p": 5, "beat": "dive",
               "setting": [{**SURFACE, "waterline": 0.08, "place": "open ocean (surface)"},
                           {"kind": "place", "biome": "twilight", "place": "twilight zone", "depth": 500, "waterline": None,
                            "light": "night", "at": "@kilometre"},
                           {**DEEP, "at": "@where"}],
               "layers": [
                   whale(470, 0.2 * H, P4, z=2, keyframes=[
                       {"t": 0, "x": "40%", "y": "20%", "rotate": 0}, {"t": "@breath", "x": "44%", "y": "21%", "rotate": 8},
                       {"t": "@dives", "x": "46%", "y": "28%", "rotate": 55, "ease": "inOut"},
                       {"t": "@where", "x": "46%", "y": "42%", "rotate": 70}, {"t": "@:end", "x": "46%", "y": "50%", "rotate": 72}]),
                   {"type": "component", "name": "explainer/DepthMeter", "x": "86%", "y": "38%", "width": 220, "height": 900,
                    "depth": 0, "z": 15, "role": "label",
                    "props": {"depth": [{"t": 0, "v": 0}, {"t": "@dives", "v": 0}, {"t": "@where", "v": 1000, "ease": "inOut"}],
                              "max": 1000, "step": 250, "size": 44, "side": "left"}},
                   tag("NO SUNLIGHT", "@where", "40%", "13%", size=50),
               ],
               "camera": cam((0, 1.0, "50%", "50%"), ("@breath", 1.02, "50%", "48%"), ("@dives", 1.04, "50%", "50%"),
                             ("@down", 1.1, "48%", "54%", "inOut"), ("@:end", 1.14, "48%", "58%"))})

    # p05 the hunt: click, echo, close in, buzz, squid gone
    P5 = 40
    wx5 = 0.28 * W
    sn5 = snout(wx5, 0.44 * H, P5)
    sq = (0.84 * W, 0.44 * H)
    sc.append({"p": 6, "beat": "hunt", "setting": DEEP,
               "layers": [
                   {"type": "component", "name": "explainer/ColossalSquid", "x": pct(sq[0]), "y": pct(sq[1], H), "width": 440,
                    "height": 280, "flipX": True, "props": {"pxPerM": 40}, "z": 1, "end": "@gone+0.1", "allowOverlap": True,
                    "keyframes": [{"t": 0, "x": pct(sq[0])}, {"t": "@buzz", "x": pct(sq[0] - 30)}, {"t": "@gone", "x": pct(sq[0] - 40)}]},
                   whale(wx5, 0.44 * H, P5, z=2, allowOverlap=True,
                         jawOpen=[{"t": "@buzz", "v": 0}, {"t": "@and#2", "v": 1}, {"t": "@gone", "v": 1}, {"t": "@gone+0.35", "v": 0}],
                         keyframes=[{"t": 0, "x": "26%"}, {"t": "@closes", "x": "28%"}, {"t": "@in.end", "x": "36%", "ease": "inOut"},
                                    {"t": "@buzz", "x": "40%"}, {"t": "@gone", "x": "58%", "ease": "in"},
                                    {"t": "@:end", "x": "62%", "ease": "out"}]),
                   rings(sn5[0] + 4, sq[0] - 120, sn5[1], "@clicks", out="@squid", dir=1, life=0.6, arc=30, h=300,
                         rate=[{"t": "@clicks", "v": 2.5}, {"t": "@speed", "v": 3}, {"t": "@buzz", "v": 16}],
                         keyframes=[{"t": 0, "x": pct((sn5[0] + sq[0] - 116) / 2)}, {"t": "@closes", "x": pct((sn5[0] + sq[0] - 116) / 2)},
                                    {"t": "@in.end", "x": pct((sn5[0] + 86 + sq[0] - 116) / 2)}]),
                   rings(sq[0] - 140, sn5[0] + 30, sq[1] - 20, "@echo", out="@closes", dir=-1, life=0.6, arc=28, h=260,
                         rate=2.5, color=CYAN, width=9, opacity=0.85),
                   tag("ECHO", "@echo", "62%", "31%", size=46, out="@closes"),
                   tag("BUZZ", "@buzz", "66%", "30%", size=52, accent=RED, out="@gone+0.2"),
               ],
               "camera": cam((0, 1.0, "50%", "50%"), ("@echo", 1.02, "52%", "48%"), ("@echo+0.3", 1.08, "56%", "44%", "out"),
                             ("@buzz", 1.09, "58%", "44%"), ("@buzz+0.25", 1.16, "62%", "42%", "out"),
                             ("@gone", 1.17, "62%", "42%"), ("@:end", 1.1, "60%", "44%"))})
    sc[-1]["camera"]["shake"] = [{"at": "@gone", "duration": 0.35, "amplitude": 10}]

    # p06 the turnstile: YOU on a board, the map names Dominica, then swimmers at the surface feel the clicks
    P6 = 70
    sw = (0.5 * W + 7.98 * P6, 0.42 * H)   # whale off Dominica, facing left (snout at 50 %)
    sn6 = snout(*sw, P6, flip=True)
    dv6 = (sn6[0] - 2.4 * P6 - 1.3 * P6, sn6[1])
    sc.append({"p": 7, "beat": "turnstile",
               "setting": [{"kind": "board", "board": "navy"},
                           {"kind": "map", "place": "Dominica", "cue": "Dominica", "at": "@Swimmers"},
                           {**DOMINICA, "at": "@say"}],
               "layers": [
                   diver(0.5 * W, 0.36 * H, 150, end="@Swimmers+0.3", z=3),
                   tag("YOU?", 0.2, "50%", "27%", size=56, leader=[0, 80], out="@Swimmers"),
                   {"type": "component", "name": "explainer/Map", "x": "50%", "y": "50%", "width": 1080, "height": 1920,
                    "depth": 0, "z": 30, "start": "@Swimmers", "end": "@say",
                    "props": {"views": [{"t": "@Swimmers", "lon": -66, "lat": 16, "zoom": 3.2},
                                        {"t": "@Dominica", "lon": -61.4, "lat": 15.4, "zoom": 6}],
                              "pins": [{"lon": -61.35, "lat": 15.42, "at": "@Dominica", "label": "Dominica"}],
                              "labelSize": 48, "pinSize": 1.4, "at": -0.5}},
                   tag("CARIBBEAN", "@Swimmers", "50%", "13%", size=48, z=31, out="@say"),
                   whale(sw[0] + 260, sw[1], P6, flip=True, z=2, start="@say-0.7",
                         keyframes=[{"t": "@say-0.7", "x": pct(sw[0] + 260)}, {"t": "@:end", "x": pct(sw[0])}]),
                   diver(*dv6, P6, z=3, start="@say-0.7", keyframes=[
                       {"t": "@thump", "x": pct(dv6[0])}, {"t": "@thump+0.08", "x": pct(dv6[0] - 6)},
                       {"t": "@thump+0.2", "x": pct(dv6[0])}, {"t": "@drum", "x": pct(dv6[0])},
                       {"t": "@drum+0.08", "x": pct(dv6[0] - 6)}, {"t": "@drum+0.2", "x": pct(dv6[0])}]),
                   rings(sn6[0] + 260 - 60, dv6[0] + 40, sn6[1], "@say", rate=2.2, dir=-1, life=0.9, arc=36, h=280,
                         keyframes=[{"t": "@say", "x": pct((sn6[0] + 200 + dv6[0] + 40) / 2)},
                                    {"t": "@:end", "x": pct((sn6[0] - 60 + dv6[0] + 40) / 2)}]),
                   tag("THUMP", "@thump", pct(dv6[0]), "29%", size=50, accent=RED),
                   svg(DRUM, pct(dv6[0] - 120), "44%", 100, 92, start="@drum", enter={"type": "pop", "at": "@drum", "duration": 0.35}, z=4),
               ],
               "camera": cam((0, 1.0, "50%", "50%"), ("@you", 1.06, "50%", "44%", "inOut"), ("@say", 1.0, "50%", "50%"),
                             ("@thump", 1.02, "46%", "48%"), ("@thump+0.3", 1.12, "38%", "42%", "out"), ("@:end", 1.14, "37%", "42%"))})

    # p07 point blank: a polite distance, then the snout 1 m from YOU, full power, eardrums, UNTESTED
    P7 = 120
    dv7 = (0.21 * W, 0.42 * H)
    near = dv7[0] + 1.3 * P7 + 1.0 * P7                  # snout 1 m in front of the diver
    far = 0.9 * W
    cy7 = dv7[1] + 0.51 * P7
    sc.append({"p": 8, "beat": "peak", "setting": {"kind": "board", "board": "ink"},
               "layers": [
                   whale(far + 7.98 * P7, cy7, P7, flip=True, z=2,
                         keyframes=[{"t": 0, "x": pct(far + 7.98 * P7 + 60)}, {"t": "@distance", "x": pct(far + 7.98 * P7)},
                                    {"t": "@point", "x": pct(far + 7.98 * P7)}, {"t": "@blank.end", "x": pct(near + 7.98 * P7), "ease": "inOut"},
                                    {"t": "@:end", "x": pct(near + 7.98 * P7 - 10)}]),
                   diver(*dv7, P7, z=3, allowOverlap=True),
                   tag("YOU", 0.1, pct(dv7[0]), pct(dv7[1] - 120, H), size=46, leader=[0, 70]),
                   svg(DASH, pct((dv7[0] + 1.3 * P7 + far) / 2), pct(dv7[1] + 90, H), round(far - dv7[0] - 1.3 * P7 - 30), 30,
                       start="@polite", end="@point", enter={"type": "fade", "at": "@polite", "duration": 0.25}, z=4),
                   tag("1 M", "@blank.end", pct(near - 0.5 * P7), pct(dv7[1] + 200, H), size=46, depth=1),
                   rings(near - 10, dv7[0] + 1.3 * P7 + 10, dv7[1], "@full", out="@Nobody's", rate=3.5, dir=-1, life=0.5,
                         arc=45, h=420, width=16),
                   svg(HIT, pct(dv7[0] + 1.0 * P7), pct(dv7[1] - 4, H), 190, 190, start="@burst",
                       enter={"type": "pop", "at": "@burst", "duration": 0.3}, end="@Nobody's+0.3", z=5,
                       idle=[{"type": "pulse", "amount": 0.12, "speed": 2.2}]),
                   tag("UNTESTED", "@Nobody's", "50%", "14%", size=56, accent=RED),
               ],
               "camera": cam((0, 1.04, "50%", "50%"), ("@distance", 1.0, "52%", "50%"), ("@point", 1.0, "50%", "50%"),
                             ("@blank.end", 1.1, "36%", "42%", "inOut"), ("@burst", 1.12, "34%", "42%"),
                             ("@burst+0.25", 1.22, "30%", "40%", "out"), ("@Nobody's", 1.18, "36%", "42%"),
                             ("@Nobody's+0.4", 1.04, "48%", "46%", "out"), ("@:end", 1.03, "48%", "46%"))})
    sc[-1]["camera"]["shake"] = [{"at": "@burst", "duration": 0.6, "amplitude": 14}]

    # p08 twist: full power is for the deep; near the surface two families trade codas, each with its own rhythm
    PF = 22                                         # females ~11 m: 16 m figure at 11/16 scale
    sc.append({"p": 9, "beat": "twist",
               "setting": [dict(DEEP), {**DUSK, "at": "@Near"}],
               "layers": [
                   whale(0.4 * W, 0.42 * H, 40, z=2, end="@Near+0.1",
                         keyframes=[{"t": 0, "x": "34%"}, {"t": "@Near+0.1", "x": "46%"}]),
                   rings(snout(0.4 * W, 0.42 * H, 40)[0] + 10, 1075, 0.42 * H - 20, 0.2, out="@down", rate=6, dir=1,
                         life=0.5, arc=26, h=260, keyframes=[{"t": 0, "x": "78%"}, {"t": "@Near", "x": "86%"}], end="@Near"),
                   tag("1,000 M", 0.3, "50%", "14%", size=48, out="@Near-0.3"),
                   # family 1 (left) and family 2 (right), adults + a calf each, cruising at the surface
                   *[whale(x, y, ppm, flip=fl, z=2, start="@Near", timeOffset=to,
                           keyframes=[{"t": "@Near", "x": pct(x + (90 if fl else -90))}, {"t": "@:end", "x": pct(x + (-30 if fl else 30))}])
                     for x, y, ppm, fl, to in [(0.27 * W, 0.30 * H, PF, False, 0.0), (0.22 * W, 0.37 * H, 9, False, 0.7),
                                               (0.74 * W, 0.47 * H, PF, True, 0.4), (0.79 * W, 0.54 * H, 9, True, 1.1)]],
                   {"type": "component", "name": "explainer/Coda", "x": "27%", "y": "23%", "width": 300, "height": 60,
                    "z": 6, "role": "fx", "props": {"at": "@codas", "gaps": [0.18, 0.18, 0.18, 0.42], "r": 15, "color": YELLOW}},
                   {"type": "component", "name": "explainer/Coda", "x": "73%", "y": "40%", "width": 300, "height": 60,
                    "z": 6, "role": "fx", "props": {"at": "@codas+0.5", "gaps": [0.4, 0.12, 0.12, 0.12], "r": 15, "color": MAGENTA}},
                   tag("FAMILY 1", "@family", "27%", "16.5%", size=44),
                   tag("FAMILY 2", "@family+0.25", "73%", "33.5%", size=44),
               ],
               "camera": cam((0, 1.06, "50%", "50%"), ("@down", 1.0, "50%", "50%"), ("@Near", 1.0, "50%", "48%"),
                             ("@trade", 1.02, "50%", "46%"), ("@codas", 1.05, "50%", "44%", "inOut"), ("@family", 1.06, "50%", "42%"), ("@:end", 1.1, "50%", "42%"))})

    # p09 bookend: the whale swims up to the same YOU and lands on the frame-0 cover exactly
    k = [{"t": 0, "x": pct(C_WHALE[0] + 420)}, {"t": "@up", "x": pct(C_WHALE[0] + 160), "ease": "out"},
         {"t": "@:end", "x": pct(C_WHALE[0]), "ease": "out"}]
    sc.append({"p": 10, "beat": "bookend", "setting": SURFACE,
               "layers": [*cover_layers(d[9], "@about-0.3", swim_in=k),
                          {"type": "component", "name": "explainer/Coda", "x": pct(C_SNOUT[0] + 30), "y": pct(C_SNOUT[1] - 210, H),
                           "width": 260, "height": 56, "z": 6, "role": "fx", "props": {"at": "@clicking", "out": "@about-0.4",
                                                                                       "gaps": [0.18, 0.18, 0.18, 0.42],
                                                                                       "r": 14, "color": YELLOW}}],
               "camera": {"keyframes": [{"t": 0, "zoom": 1.1, "x": "46%", "y": "46%"}, {"t": "@relax", "zoom": 1.08, "x": "47%", "y": "47%"},
                                        {"t": "@:end", "zoom": 1.0, "x": "50%", "y": "50%", "ease": "inOut"}]}})
    # the bookend rings start before the scene: leave the leading ones out until the whale is in place
    sc[-1]["layers"][1]["props"]["at"] = round(d[9] - 1.0, 3)

    shots = {"niche": "explainer",
             "emphasis": ["click", "third", "decibels.", "buzz,", "thump", "eardrums.", "dialect."],
             "glue": ["sperm whale's", "blue whale", "point blank", "full power", "two thousand litres"],
             "scenes": sc}
    out = os.path.join(HERE, "shots.json")
    with open(out, "w") as f:
        json.dump(shots, f, indent=1, ensure_ascii=False)
    print(f"wrote {os.path.relpath(out, ROOT)}: {len(sc)} scenes, {sum(len(s['layers']) for s in sc)} layers")


if __name__ == "__main__":
    build()
