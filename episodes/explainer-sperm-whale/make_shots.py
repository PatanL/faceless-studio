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
    lk = {k: kw.pop(k) for k in list(kw) if k in ("keyframes", "start", "end", "z", "enter", "exit", "idle", "flipX", "allowOverlap")}
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

PERSON = ("<svg viewBox='0 0 110 40' xmlns='http://www.w3.org/2000/svg'><circle cx='14' cy='20' r='12' fill='#e9f4fc'/>"
          "<rect x='26' y='9' width='52' height='22' rx='11' fill='#fc6e0e'/><rect x='70' y='12' width='38' height='16' rx='8' "
          "fill='#250192'/></svg>")
WIPE_UP = {"type": "wipe", "duration": 0.5, "direction": "up"}
WIPE_LEFT = {"type": "wipe", "duration": 0.5, "direction": "left"}
FRAME = 1 / 30

# ------------------------------------------------------------------ settings
SURFACE = {"kind": "place", "biome": "open_ocean", "place": "open ocean", "depth": 8, "waterline": 0.05, "light": "day"}
DEEP = {"kind": "place", "biome": "deep", "place": "deep sea, 1,000 m", "depth": 1000, "waterline": None, "light": "night",
        "key": "ink"}
DOMINICA = {"kind": "place", "biome": "open_ocean", "place": "off Dominica", "depth": 4, "waterline": 0.2, "light": "day",
            "coast": {"kind": "hills"}, "cue": "Dominica"}
DUSK = {"kind": "place", "biome": "open_ocean", "place": "open ocean at dusk", "depth": 8, "waterline": 0.14, "light": "dusk",
        "key": "royal"}

# cover (frame 0 = last frame): the whale's head on the right facing left (eye in frame), YOU 1 m in front of the snout
CP = 130                                   # px per metre on the cover
C_SNOUT = (500, 0.46 * H - 0.51 * CP)      # snout middle
C_WHALE = (C_SNOUT[0] + 7.98 * CP, 0.46 * H)
C_DIVER = (C_SNOUT[0] - 1.0 * CP - 1.3 * CP, C_SNOUT[1] + 6)
SWAY0 = 0.4                                # idle sway phase of the cover whale at t = 0
SWAY_SPEED = 0.2


def cover_layers(dur, at_head, swim_in=None, jolts=()):
    """the cover composition; swim_in = keyframes for the bookend whale (ends exactly at the cover position). The last
    frame is drawn at t = dur - 1/30, so every phase in the bookend is matched at that time, not at dur."""
    T = dur - FRAME if swim_in else 0.0
    w = whale(*C_WHALE, CP, flip=True, z=2, idle=[{"type": "sway", "amount": 0.5, "speed": SWAY_SPEED,
                                                      "phase": round(SWAY0 - 2 * math.pi * SWAY_SPEED * T, 4)}])
    if swim_in:
        w["keyframes"] = swim_in
        w["props"]["timeOffset"] = round((-T) % 2.5, 3)       # swim wave period 2.5 s
    dv = diver(*C_DIVER, CP, z=3, allowOverlap=True)
    if jolts:
        x0 = pct(C_DIVER[0])
        kf = [{"t": 0, "x": x0, "rotate": 0}]
        for j in jolts:
            kf += [{"t": j, "x": x0, "rotate": 0}, {"t": f"{j}+0.34", "x": pct(C_DIVER[0] - 14), "rotate": -6, "ease": "out"},
                   {"t": f"{j}+0.8", "x": x0, "rotate": 0, "ease": "inOut"}]
        dv["keyframes"] = kf
    return [
        w,
        rings(C_SNOUT[0] - 20, C_DIVER[0] + 1.3 * CP + 6, C_SNOUT[1], round(T - 1.0, 3), rate=3, dir=-1, life=0.9, arc=40,
              h=420, width=18),
        dv,
        tag("YOU", 0 if not swim_in else -1, pct(C_DIVER[0]), pct(C_DIVER[1] - 125, H), size=48, leader=[0, 75], depth=1),
        headline("236 DECIBELS", at_head, red="236", sub="ONE CLICK, ONE METRE AWAY", size=112),
    ]


def build():
    meta, S, words, total, _ = load(SLUG)
    d = [s.dur for s in S]
    sc = []

    # p00 hook: frame 0 = cover; the diver flinches as the clicks land
    sc.append({"p": 1, "beat": "hook", "setting": SURFACE,
               "layers": cover_layers(d[0], -0.6, jolts=("@click",)),
               "camera": cam((0, 1.0, "50%", "50%"), ("@click", 1.03, "46%", "49%"), ("@:end", 1.1, "38%", "47%", "inOut"))})

    # p01 scale: true-scale male, ~16 M gauge, nine people head to toe (flat figures that read on a phone), head third
    P1 = 58
    wx, wy = 540, 0.31 * H
    people = []
    for i in range(9):
        x = 540 - 4 * 1.75 * P1 + i * 1.75 * P1
        a = f"@nine+{0.07 * i:.2f}"
        people.append(svg(PERSON, pct(x), "49.5%", round(1.75 * P1), 48, start=a,
                          enter={"type": "pop", "at": a, "duration": 0.35}, z=3))
    head0 = wx + 7.98 * P1 - 5.33 * P1
    sc.append({"p": 2, "beat": "scale", "setting": {"kind": "board", "board": "cyan"}, "transitionIn": WIPE_UP,
               "layers": [
                   whale(wx, wy, P1, z=2),
                   {"type": "component", "name": "explainer/ScaleBar", "x": "50%", "y": "42.5%", "width": round(16 * P1),
                    "height": 140, "role": "label", "props": {"label": "~16 M", "at": "@sixteen-0.1", "labelSize": 56}},
                   *people,
                   tag("YOU ×9", "@toe", "40%", "55.5%", size=46, leader=[0, -70], depth=1),
                   svg(BRACKET, pct(head0 + 2.66 * P1), "22.5%", round(5.33 * P1), 50, start="@third",
                       enter={"type": "fade", "at": "@third", "duration": 0.25}, z=4, role="label"),
                   tag("1/3 HEAD", "@third+0.1", pct(head0 + 2.66 * P1), "17.6%", size=50, depth=1),
               ],
               "camera": cam((0, 1.0, "50%", "50%"), ("@sixteen", 1.02, "50%", "48%"), ("@nine", 1.05, "50%", "47%", "inOut"),
                             ("@third", 1.04, "54%", "47%"), ("@:end", 1.05, "60%", "46%", "inOut"))})

    # p02 the organ: one click on "machine", the oil level rises, ten bathtubs, then the focused beam
    P2 = 100
    sx, sy = 700, 0.34 * H
    wcx = sx - 7.98 * P2
    tubs = []
    for i in range(10):
        r, c = divmod(i, 5)
        a = f"@ten+{0.06 * i:.2f}"
        tubs.append(svg(TUB, pct(240 + c * 150), f"{48.5 + r * 5.6:.1f}%", 140, 82, start=a,
                        enter={"type": "pop", "at": a, "duration": 0.35}, end="@focus+0.3",
                        exit={"type": "fade", "at": "@focus-0.1", "duration": 0.4}, z=3))
    sc.append({"p": 3, "beat": "mechanism", "setting": {"kind": "board", "board": "violet"}, "transitionIn": WIPE_LEFT,
               "layers": [
                   whale(wcx, sy, P2, z=2, organ=[{"t": "@Nearly", "v": 0}, {"t": "@litres", "v": 1, "ease": "inOut"}],
                         click=[{"t": "@focus", "v": 0}, {"t": "@focus+0.2", "v": 1}]),
                   rings(sx + 6, 1075, sy - 0.51 * P2, "@machine", out="@machine+0.1", rate=2, dir=1, life=0.9, arc=40, h=420,
                         width=18),
                   tag("≈ 2,000 L OF OIL", "@two", pct(sx - 2.6 * P2 + 20), "15%", size=50, leader=[0, 150], depth=1, out="@focus"),
                   *tubs,
                   rings(sx + 6, 1075, sy - 0.51 * P2, "@focus", rate=6, dir=1, life=0.6, arc=16, h=260, width=22),
                   tag("BEAM", "@beam-0.2", "80%", "24%", size=52),
               ],
               "camera": cam((0, 1.0, "50%", "50%"), ("@machine", 1.03, "52%", "48%"), ("@Nearly", 1.04, "48%", "47%"),
                             ("@litres", 1.1, "45%", "42%", "inOut"), ("@ten", 1.08, "46%", "44%"),
                             ("@focus", 1.06, "52%", "46%", "inOut"), ("@:end", 1.12, "62%", "42%", "inOut"))})

    # p03 loudest: big bars against the rivals on one underwater scale (dB re 1 uPa; bars from a 150 dB floor)
    P3 = 30
    sc.append({"p": 4, "beat": "record", "setting": {"kind": "board", "board": "blue"}, "transitionIn": WIPE_UP,
               "layers": [
                   {"type": "component", "name": "explainer/SpeedBars", "x": "50%", "y": "25%", "width": 980, "height": 620,
                    "role": "label", "depth": 0, "z": 15, "props": {
                        "title": "Loudest animals", "max": 90, "at": "@clicks", "stagger": 2.6, "duration": 0.7, "size": 62,
                        "labelWidth": 420,
                        "rows": [{"label": "Sperm whale", "value": 86, "text": "236 dB", "color": "red"},
                                 {"label": "Snapping shrimp", "value": 39, "text": "189 dB", "color": CYAN},
                                 {"label": "Blue whale", "value": 38, "text": "188 dB", "color": BONE}]}},
                   whale(380, 0.49 * H, P3, z=2, keyframes=[{"t": 0, "x": "30%"}, {"t": "@:end", "x": "36%"}]),
                   rings(380 + 7.98 * P3 + 4, 1060, 0.49 * H - 0.51 * P3, "@clicks", rate=3, dir=1, life=0.8, arc=34, h=300,
                         width=16),
               ],
               "camera": cam((0, 1.0, "50%", "50%"), ("@decibels", 1.03, "50%", "48%"), ("@louder", 1.06, "50%", "46%", "inOut"),
                             ("@:end", 1.08, "50%", "45%", "inOut"))})

    # p04 the dive: surface -> twilight -> deep, depth meter on the left, the whale goes down through the whole scene
    P4 = 36
    sc.append({"p": 5, "beat": "dive", "transitionIn": WIPE_LEFT,
               "setting": [{**SURFACE, "waterline": 0.08, "place": "open ocean (surface)"},
                           {"kind": "place", "biome": "twilight", "place": "twilight zone", "depth": 500, "waterline": None,
                            "light": "night", "at": "@kilometre"},
                           {**DEEP, "at": "@where"}],
               "layers": [
                   whale(620, 0.2 * H, P4, z=2, keyframes=[
                       {"t": 0, "x": "54%", "y": "19%", "rotate": 0}, {"t": "@breath", "x": "57%", "y": "20%", "rotate": 10},
                       {"t": "@dives", "x": "60%", "y": "27%", "rotate": 55, "ease": "inOut"},
                       {"t": "@where", "x": "62%", "y": "40%", "rotate": 68}, {"t": "@:end", "x": "63%", "y": "48%", "rotate": 72}]),
                   {"type": "component", "name": "explainer/DepthMeter", "x": "27%", "y": "36%", "width": 260, "height": 900,
                    "depth": 0, "z": 15, "role": "label",
                    "props": {"depth": [{"t": 0, "v": 0}, {"t": "@dives", "v": 0}, {"t": "@where", "v": 1000, "ease": "inOut"}],
                              "max": 1000, "step": 250, "size": 54, "side": "right"}},
                   tag("NO SUNLIGHT", "@where", "56%", "13%", size=52),
               ],
               "camera": cam((0, 1.0, "50%", "50%"), ("@breath", 1.02, "52%", "48%"), ("@dives", 1.04, "54%", "50%"),
                             ("@where", 1.08, "56%", "54%", "inOut"), ("@:end", 1.12, "56%", "58%"))})

    # p05 the hunt: click, echo, close in, buzz; a small squid at mouth height disappears behind the closing jaw
    P5 = 40
    cy5 = 0.44 * H
    k5 = 0.00979 * P5
    mouth_y = cy5 + (110 - 12) * k5
    sqx0, sqx1 = 0.8 * W, 0.82 * W
    grab = sqx1 + 70 - 7.98 * P5                   # whale centre when its head covers the squid
    sn5x = lambda cx: cx + 7.98 * P5
    sc.append({"p": 6, "beat": "hunt", "setting": DEEP, "transitionIn": WIPE_UP,
               "layers": [
                   {"type": "component", "name": "explainer/ColossalSquid", "x": pct(sqx0), "y": pct(mouth_y, H), "width": 220,
                    "height": 140, "flipX": True, "props": {"pxPerM": 18}, "z": 1, "end": "@gone+0.3", "allowOverlap": True,
                    "keyframes": [{"t": 0, "x": pct(sqx0)}, {"t": "@buzz", "x": pct(sqx1)}]},
                   whale(0.26 * W, cy5, P5, z=2, allowOverlap=True,
                         jawOpen=[{"t": "@buzz", "v": 0}, {"t": "@and#2", "v": 1}, {"t": "@gone", "v": 1}, {"t": "@gone+0.3", "v": 0}],
                         keyframes=[{"t": 0, "x": "26%"}, {"t": "@closes", "x": "28%"}, {"t": "@in.end", "x": "36%", "ease": "inOut"},
                                    {"t": "@buzz", "x": "40%"}, {"t": "@gone", "x": pct(grab), "ease": "in"},
                                    {"t": "@:end", "x": pct(grab + 30), "ease": "out"}]),
                   rings(sn5x(0.26 * W) + 4, sqx0 - 70, mouth_y - 30, "@clicks", out="@squid", dir=1, life=0.6, arc=30, h=300,
                         width=16, rate=[{"t": "@clicks", "v": 2.5}, {"t": "@speed", "v": 3}, {"t": "@buzz", "v": 16}],
                         keyframes=[{"t": 0, "x": pct((sn5x(0.26 * W) + sqx0 - 66) / 2)},
                                    {"t": "@closes", "x": pct((sn5x(0.28 * W) + sqx0 - 66) / 2)},
                                    {"t": "@in.end", "x": pct((sn5x(0.36 * W) + sqx0 - 66) / 2)}]),
                   rings(sqx0 - 80, sn5x(0.28 * W) + 30, mouth_y - 20, "@echo", out="@closes", dir=-1, life=0.6, arc=28, h=240,
                         rate=2.5, color=CYAN, width=12),
                   tag("ECHO", "@echo", "60%", "33%", size=48, out="@closes"),
                   tag("BUZZ", "@buzz", "64%", "33%", size=54, accent=RED, out="@gone"),
               ],
               "camera": cam((0, 1.0, "50%", "50%"), ("@echo", 1.03, "52%", "48%"), ("@closes", 1.06, "56%", "47%", "inOut"),
                             ("@buzz", 1.12, "60%", "46%", "inOut"), ("@gone", 1.18, "64%", "46%", "inOut"),
                             ("@:end", 1.14, "62%", "47%"))})
    sc[-1]["camera"]["shake"] = [{"at": "@gone", "duration": 0.35, "amplitude": 10}]

    # p06 the turnstile: YOU big on a board, the map names Dominica, then the sea off Dominica: clicks hit the swimmer
    P6 = 85
    snx6 = 0.52 * W
    sw = (snx6 + 7.98 * P6, 0.43 * H)
    dv6 = (snx6 - 1.8 * P6 - 1.3 * P6, sw[1] - 0.51 * P6 + 6)
    jolt = lambda w: [{"t": w, "x": pct(dv6[0]), "rotate": 0}, {"t": f"{w}+0.34", "x": pct(dv6[0] - 12), "rotate": -6, "ease": "out"},
                      {"t": f"{w}+0.66", "x": pct(dv6[0]), "rotate": 0, "ease": "inOut"}]
    sc.append({"p": 7, "beat": "turnstile", "transitionIn": WIPE_LEFT,
               "setting": [{"kind": "board", "board": "navy"},
                           {"kind": "map", "place": "Dominica", "cue": "Dominica", "at": "@Swimmers"},
                           {**DOMINICA, "at": "@say"}],
               "layers": [
                   diver(0.5 * W, 0.41 * H, 220, end="@Swimmers+0.3", z=3),
                   tag("YOU?", 0.15, "50%", "29.5%", size=60, leader=[0, 90], out="@Swimmers", depth=1),
                   {"type": "component", "name": "explainer/Map", "x": "50%", "y": "50%", "width": 1080, "height": 1920,
                    "depth": 0, "z": 30, "start": "@Swimmers", "end": "@say",
                    "enter": {"type": "fade", "at": "@Swimmers", "duration": 0.25},
                    "exit": {"type": "fade", "at": "@say-0.3", "duration": 0.3},
                    "props": {"views": [{"t": "@Swimmers", "lon": -66, "lat": 15, "zoom": 3.2},
                                        {"t": "@Dominica", "lon": -61.4, "lat": 15.4, "zoom": 6}],
                              "pins": [{"lon": -61.35, "lat": 15.42, "at": "@Dominica", "label": "Dominica"}],
                              "labelSize": 52, "pinSize": 1.5, "at": -0.5}},
                   tag("CARIBBEAN SEA", "@Swimmers", "50%", "13%", size=50, z=31, out="@say-0.3"),
                   whale(sw[0] + 300, sw[1], P6, flip=True, z=2, start="@say-0.6",
                         keyframes=[{"t": "@say-0.6", "x": pct(sw[0] + 300)}, {"t": "@thump", "x": pct(sw[0] + 40), "ease": "out"},
                                    {"t": "@:end", "x": pct(sw[0])}]),
                   diver(*dv6, P6, z=3, start="@say-0.6", keyframes=jolt("@thump") + jolt("@chest")),
                   rings(snx6 + 40, dv6[0] + 1.3 * P6, dv6[1] - 6, "@say", rate=2.4, dir=-1, life=0.8, arc=36, h=320, width=18),
                   tag("THUMP", "@thump", pct(dv6[0]), "30.5%", size=54, accent=RED, leader=[0, 70], depth=1),
                   svg(DRUM, pct(dv6[0] + 30), "48%", 170, 156, start="@like#2",
                       enter={"type": "pop", "at": "@like#2", "duration": 0.35}, z=4),
               ],
               "camera": cam((0, 1.0, "50%", "50%"), ("@you", 1.06, "50%", "47%", "inOut"), ("@say", 1.0, "50%", "50%"),
                             ("@thump", 1.03, "44%", "48%", "inOut"), ("@:end", 1.1, "38%", "45%", "inOut"))})

    # p07 point blank: a polite distance (whole head + eye in frame), then the snout 1 m from YOU, full power, eardrums
    P7 = 90
    dv7 = (0.19 * W, 0.43 * H)
    dv_end = dv7[0] + 1.3 * P7
    far, near = dv_end + 3.0 * P7, dv_end + 1.0 * P7
    cy7 = dv7[1] + 0.51 * P7 - 6
    x0 = pct(dv7[0])
    sc.append({"p": 8, "beat": "peak", "setting": {"kind": "board", "board": "ink"}, "transitionIn": WIPE_UP,
               "layers": [
                   whale(far + 7.98 * P7 + 260, cy7, P7, flip=True, z=2,
                         keyframes=[{"t": 0, "x": pct(far + 7.98 * P7 + 260)}, {"t": "@distance", "x": pct(far + 7.98 * P7), "ease": "out"},
                                    {"t": "@point", "x": pct(far + 7.98 * P7)}, {"t": "@blank.end", "x": pct(near + 7.98 * P7), "ease": "inOut"},
                                    {"t": "@:end", "x": pct(near + 7.98 * P7 - 8)}]),
                   diver(*dv7, P7, z=3, allowOverlap=True,
                         keyframes=[{"t": 0, "x": x0, "rotate": 0}, {"t": "@burst", "x": x0, "rotate": 0},
                                    {"t": "@burst+0.34", "x": pct(dv7[0] - 30), "rotate": -14, "ease": "out"},
                                    {"t": "@eardrums+0.3", "x": pct(dv7[0] - 36), "rotate": -10},
                                    {"t": "@Nobody's", "x": pct(dv7[0] - 20), "rotate": -4, "ease": "inOut"}]),
                   tag("YOU", 0.1, x0, pct(dv7[1] - 115, H), size=48, leader=[0, 70], depth=1),
                   svg(DASH, pct((dv_end + far) / 2), pct(dv7[1] + 80, H), round(far - dv_end - 20), 30,
                       start="@polite", end="@point+0.2", enter={"type": "fade", "at": "@polite", "duration": 0.25},
                       exit={"type": "fade", "at": "@point-0.1", "duration": 0.3}, z=4),
                   tag("3 M", "@distance", pct((dv_end + far) / 2), pct(dv7[1] + 160, H), size=46, depth=1, out="@point"),
                   tag("1 M", "@blank.end", pct((dv_end + near) / 2), pct(dv7[1] + 160, H), size=48, depth=1),
                   rings(near - 10, dv_end + 4, dv7[1], "@full", out="@Nobody's", rate=3.5, dir=-1, life=0.5, arc=45, h=420,
                         width=20),
                   svg(HIT, pct(dv_end - 20), pct(dv7[1] - 6, H), 200, 200, start="@burst",
                       enter={"type": "pop", "at": "@burst", "duration": 0.3}, end="@Nobody's+0.4",
                       exit={"type": "fade", "at": "@Nobody's", "duration": 0.4}, z=5,
                       idle=[{"type": "pulse", "amount": 0.12, "speed": 2.2}]),
                   tag("UNTESTED", "@Nobody's", "50%", "14%", size=60, accent=RED),
               ],
               "camera": cam((0, 1.02, "50%", "50%"), ("@distance", 1.0, "52%", "50%"), ("@point", 1.0, "50%", "50%"),
                             ("@blank.end", 1.08, "40%", "46%", "inOut"), ("@burst", 1.1, "38%", "46%"),
                             ("@eardrums", 1.16, "34%", "45%", "inOut"), ("@:end", 1.06, "44%", "47%", "inOut"))})
    sc[-1]["camera"]["shake"] = [{"at": "@burst", "duration": 0.6, "amplitude": 14}]

    # p08 twist: full power is for hunting 1 km down (whale + squid); then two families trade codas near the surface
    s = 50                                         # px per metre for the families: adult females ~11 m, calves ~4.5 m
    fam = [(0.31 * W, 0.33 * H, 11, False, 0.0), (0.22 * W, 0.385 * H, 4.5, False, 0.7),
           (0.69 * W, 0.49 * H, 11, True, 0.4), (0.79 * W, 0.545 * H, 4.5, True, 1.1)]
    sc.append({"p": 9, "beat": "twist", "transitionIn": WIPE_LEFT,
               "setting": [dict(DEEP), {**DUSK, "at": "@Near"}],
               "layers": [
                   whale(0.3 * W, 0.42 * H, 40, z=2, end="@Near+0.45",
                         keyframes=[{"t": 0, "x": "28%"}, {"t": "@Near+0.45", "x": "40%"}]),
                   {"type": "component", "name": "explainer/ColossalSquid", "x": "86%", "y": pct(0.42 * H + 38, H), "width": 160,
                    "height": 110, "flipX": True, "props": {"pxPerM": 12}, "z": 1,
                    "keyframes": [{"t": 0, "x": "84%"}, {"t": "@down", "x": "88%"}, {"t": "@Near-0.05", "x": "112%", "ease": "in"}], "end": "@Near"},
                   rings(0.3 * W + 7.98 * 40 + 10, 0.86 * W - 70, 0.42 * H - 20, 0.2, out="@down", rate=6, dir=1, life=0.5,
                         arc=26, h=260, width=16, keyframes=[{"t": 0, "x": pct((0.28 * W + 319 + 0.84 * W - 60) / 2)},
                                                              {"t": "@Near", "x": pct((0.4 * W + 319 + 0.9 * W - 60) / 2)}],
                         end="@Near+0.45"),
                   tag("1,000 M DEEP", 0.3, "50%", "14%", size=50, out="@Near-0.3"),
                   *[whale(x + (-700 if not fl else 700), y, s * m / 16, flip=fl, z=2, start="@Near+0.4", timeOffset=to,
                           keyframes=[{"t": "@Near+0.4", "x": pct(x + (-700 if not fl else 700))},
                                      {"t": "@trade", "x": pct(x), "ease": "out"},
                                      {"t": "@:end", "x": pct(x + (-30 if fl else 30))}])
                     for x, y, m, fl, to in fam],
                   {"type": "component", "name": "explainer/Coda", "x": "33%", "y": "25.5%", "width": 300, "height": 60,
                    "z": 6, "role": "fx", "props": {"at": "@trade", "gaps": [0.18, 0.18, 0.18, 0.42], "r": 15, "color": YELLOW}},
                   {"type": "component", "name": "explainer/Coda", "x": "67%", "y": "41.5%", "width": 300, "height": 60,
                    "z": 6, "role": "fx", "props": {"at": "@trade+0.5", "gaps": [0.4, 0.12, 0.12, 0.12], "r": 15, "color": MAGENTA}},
                   tag("FAMILY 1", "@family", "33%", "19.5%", size=46, depth=1),
                   tag("FAMILY 2", "@family", "67%", "35.5%", size=46, depth=1),
               ],
               "camera": cam((0, 1.04, "50%", "50%"), ("@down", 1.0, "50%", "50%"), ("@Near", 1.0, "50%", "48%"),
                             ("@trade", 1.02, "50%", "46%", "inOut"), ("@codas", 1.05, "50%", "44%", "inOut"),
                             ("@family", 1.06, "50%", "42%"), ("@:end", 1.1, "50%", "42%"))})

    # p09 bookend: the whale swims up on "swims", ends on the frame-0 cover exactly (codas fade before the headline)
    k = [{"t": 0, "x": pct(C_WHALE[0] + 760)}, {"t": "@swims", "x": pct(C_WHALE[0] + 760)},
         {"t": "@relax", "x": pct(C_WHALE[0] + 20), "ease": "out"}, {"t": round(d[9] - FRAME, 3), "x": pct(C_WHALE[0])}]
    sc.append({"p": 10, "beat": "bookend", "setting": SURFACE, "transitionIn": WIPE_UP,
               "layers": [*cover_layers(d[9], "@about-0.3", swim_in=k),
                          {"type": "component", "name": "explainer/Coda", "x": pct(C_SNOUT[0] + 20), "y": pct(C_SNOUT[1] - 230, H),
                           "width": 260, "height": 56, "z": 6, "role": "fx",
                           "props": {"at": "@clicking", "out": "@about-0.6", "gaps": [0.18, 0.18, 0.18, 0.42], "r": 14,
                                     "color": YELLOW}}],
               "camera": {"keyframes": [{"t": 0, "zoom": 1.08, "x": "50%", "y": "48%"}, {"t": "@relax", "zoom": 1.06, "x": "48%", "y": "48%"},
                                        {"t": round(d[9] - FRAME, 3), "zoom": 1.0, "x": "50%", "y": "50%", "ease": "inOut"}]}})
    # the bookend rings must only start once the whale is in place (their phase still matches frame 0 at the end)
    sc[-1]["layers"][1]["props"]["at"] = round(d[9] - FRAME - 1.0, 3)

    pages = [
        "What would", "a sperm whale's click", "do to your body?",
        "A big male", "is sixteen metres long,", "nine of you", "laid head to toe,", "and a third of it", "is head.",
        "That head", "is a sound machine.", "Nearly two thousand", "litres of oil inside,", "ten bathtubs' worth,",
        "focus every click", "into a beam.",
        "And those clicks", "hit over two hundred", "and thirty decibels.", "No animal on Earth", "is louder,",
        "not even the blue whale.",
        "It needs that to hunt.", "On one breath", "it dives", "a kilometre down,", "where you couldn't", "see your own hand.",
        "There it clicks,", "listens for the echo,", "and closes in.", "The clicks speed up", "into a buzz,",
        "and the squid is gone.",
        "So what does that", "feel like to you?", "Swimmers off Dominica", "say the clicks", "thump through", "their chest",
        "like a drum.",
        "And that's from", "a polite distance.", "On paper,", "at point blank", "and full power,", "one click could",
        "burst your eardrums.", "Nobody's volunteered", "to check.",
        "Good news:", "full power", "is for hunting,", "a kilometre down.", "Near the surface,", "they mostly trade",
        "softer patterns", "called codas,", "and every family", "has its own dialect.",
        "So if one swims up", "and starts clicking", "at you, relax.", "It's probably telling", "its family about you.",
    ]
    shots = {"niche": "explainer",
             "emphasis": ["click", "third", "decibels.", "buzz,", "thump", "eardrums.", "dialect."],
             "glue": ["sperm whale's", "blue whale", "point blank", "full power", "two thousand litres"],
             "pages": pages,
             "scenes": sc}
    out = os.path.join(HERE, "shots.json")
    with open(out, "w") as f:
        json.dump(shots, f, indent=1, ensure_ascii=False)
    print(f"wrote {os.path.relpath(out, ROOT)}: {len(sc)} scenes, {sum(len(s['layers']) for s in sc)} layers")


if __name__ == "__main__":
    build()
