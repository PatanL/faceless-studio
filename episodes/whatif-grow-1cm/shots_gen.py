#!/usr/bin/env python3
"""Writes episodes/whatif-grow-1cm/shots.json (the hand-written shot plan for lane C).

The world and its clock plate share one clock track per scene, so they are written from one place here. Times are
@word anchors resolved by pipeline/episodes/auto.py. Run: python3 episodes/whatif-grow-1cm/shots_gen.py
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
L = math.log10
DAY, YEAR = 86400, 365.25 * 86400


def world(clock, items, ground="street", lin=False, seed="w", **view):
    props = {"clock": clock, "items": items, "ground": ground, "seed": seed, **view}
    if lin:
        props["clockScale"] = "lin"
    return {"type": "component", "name": "explainer/GrowWorld", "depth": 0.12, "overscan": 1.06, "props": props}


def hud(clock, lin=False, **extra):
    p = {"clock": clock, **extra}
    if lin:
        p["clockScale"] = "lin"
    return {"type": "component", "name": "explainer/GrowHud", "role": "fx", "x": "50%", "y": "50%", "width": 1080,
            "height": 1920, "depth": 0, "z": 50, "props": p}


def tag(text, x, y, at, leader=None, accent="amber", size=34, out=None):
    p = {"text": text, "accent": accent, "size": size, "at": at}
    if leader:
        p["leader"] = leader
    if out is not None:
        p["out"] = out
    w = round(0.62 * size * len(text) + 90)
    return {"type": "component", "name": "explainer/Tag", "x": x, "y": y, "width": w, "height": 80, "z": 40,
            "cue": None, "props": p}


def k(t, v, ease=None):
    d = {"t": t, "v": v}
    if ease:
        d["ease"] = ease
    return d


def setting(kind, biome=None, place=None, light="day", cue=None):
    s = {"kind": kind, "light": light}
    if biome:
        s.update({"biome": biome, "depth": 0, "waterline": None})
    if place:
        s["place"] = place
    if cue:
        s["cue"] = cue
    return s


def shake(at, amp=12, dur=0.45):
    return {"at": at, "duration": dur, "amplitude": amp, "frequency": 9, "rotate": 0.2, "decay": True}


def street(x0, x1, seed):
    """houses, trees, lamps and a few cars along a street from x0 to x1 (m), skipping YOU's feet"""
    out, x, i = [], x0, 0
    palette = ["coral-2", "amber-2", "tide-2", "magenta-2", "kelp-2", "violet-3"]
    while x < x1:
        kind = ["house", "tree", "house", "lamp", "house", "tree"][i % 6]
        if kind == "house":
            out.append({"kind": "house", "x": x, "w": 9, "h": 5.5, "color": palette[i % len(palette)],
                        "roof": "violet-1" if i % 2 else "dusk-1"})
            x += 13
        elif kind == "tree":
            out.append({"kind": "tree", "x": x, "h": 8 + (i % 3)})
            x += 7
        else:
            out.append({"kind": "lamp", "x": x})
            x += 5
        i += 1
    return out


ROOM = [{"kind": "room", "ceiling": 2.4}]
FIG_W = 152 / 344          # kit YOU: box width / height


def scenes():
    S = []

    # P1 hook: the bedroom, YOU sprouting toward the ceiling (frame 0 = the cover)
    room1 = [{"kind": "room", "ceiling": 2.4, "at": "@hits"}]
    clk = [k(0, 0), k("@hits", 65, "linear")]
    S.append({"p": 1, "beat": "hook", "setting": setting("place", "home", "your bedroom"),
              "background": world(clk, room1, lin=True, seed="room",
                                  lppm=[k(0, 2.49), k("@hits", 2.57, "out")], gy=0.64, cx=0.52,
                                  face=[{"at": 0, "face": "calm"}, {"at": "@minute", "face": "worried"},
                                        {"at": "@hits", "face": "strain"}],
                                  pose=[{"at": 0, "pose": "stand"}, {"at": "@hits+0.15", "pose": "shrug"}]),
              "layers": [hud(clk, lin=True, title="+1 CM EVERY SECOND", titleUntil="@and")],
              "camera": {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": "@hits", "zoom": 1.03, "ease": "inOut"}],
                         "shake": [shake("@hits", 16)]}})

    # P2 street: grow past houses and a ten-storey block, then push down to a car beside the shoe
    items = street(-120, -12, "s2a") + street(48, 160, "s2b") + [
        {"kind": "skyline", "x0": -900, "x1": 900, "seed": "sk2"},
        {"kind": "sun", "sx": 0.82, "sy": 0.22, "r": 0.06},
        {"kind": "block", "x": 26, "w": 16, "floors": 10, "color": "magenta-1", "seed": "b2"},
        {"kind": "car", "x": 9.6, "color": "coral-2"},
        {"kind": "car", "x": -48, "color": "amber-2"},
    ]
    # skyline is far: draw it first (items draw in order)
    items = [items[-4]] + [i for i in items if i["kind"] not in ("skyline", "sun")]
    clk = [k(0, 65), k("@metres", 3600, "inOut"), k("@:end", 3750)]
    S.append({"p": 2, "beat": "rung1", "setting": setting("place", "town", "your street"),
              "background": world(clk, items, seed="st",
                                  lppm=[k(0, 2.35), k("@metres", 1.1, "inOut"), k("@building.end", 1.12),
                                        k("@car", 1.62, "inOut")],
                                  gy=[k(0, 0.62), k("@car", 0.6, "inOut")],
                                  cx=[k(0, 0.5), k("@metres", 0.36), k("@building.end", 0.36), k("@car", 0.22, "inOut")],
                                  face=[{"at": 0, "face": "strain"}, {"at": "@added", "face": "wow"},
                                        {"at": "@car", "face": "smile"}],
                                  pose=[{"at": 0, "pose": "stand"}, {"at": "@car", "pose": "point"}]),
              "layers": [hud(clk)]})

    # P3 board: the square-cube law
    S.append({"p": 3, "beat": "science", "setting": {"kind": "board", "board": "navy"},
              "layers": [{"type": "component", "name": "explainer/CubeLaw", "role": "label", "x": "50%", "y": "37%",
                          "width": 900, "height": 1000, "depth": 0.6, "z": 10,
                          "props": {"k": 20, "itemAt": ["@twenty", "@eight", "@four"], "top": 0.02, "rowH": 0.28}}],
              "camera": {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": "@:end", "zoom": 1.025, "ease": "inOut"}]}})

    # P4 street again: a step cracks the road, the knees dip and hold, the clock runs on toward Paris
    foot = 3.0  # right foot centre ~ x = (140-100)/152 * width
    clk = [k(0, 3750), k("@keep", 4200), k("@:end", 12000, "in")]
    items4 = street(-160, -14, "s4a") + street(30, 200, "s4b") + [
        {"kind": "skyline", "x0": -1500, "x1": 1500, "seed": "sk4"},
        {"kind": "sun", "sx": 0.18, "sy": 0.2, "r": 0.06},
        {"kind": "block", "x": 44, "w": 16, "floors": 10, "color": "violet-2", "seed": "b4"},
        {"kind": "car", "x": 14, "color": "tide-2"},
        {"kind": "crack", "x": 4.2, "w": 14, "at": "@cracks"},
    ]
    items4 = [items4[-4]] + [i for i in items4 if i["kind"] not in ("skyline", "sun")]
    S.append({"p": 4, "beat": "turn", "setting": setting("place", "town", "your street"),
              "background": world(clk, items4, seed="st4",
                                  lppm=[k(0, 1.5), k("@knees", 1.5), k("@fold", 1.18, "inOut"), k("@keep", 1.15),
                                        k("@:end", 0.55, "in")],
                                  gy=[k(0, 0.58), k("@fold", 0.64, "inOut")],
                                  focusXH=None, cx=[k(0, 0.3), k("@fold", 0.45, "inOut")],
                                  sy=[k(0, 1), k("@fold", 1), k("@here", 0.9, "out"), k("@don't", 0.9),
                                      k("@don't+0.35", 1.0, "backOut")],
                                  face=[{"at": 0, "face": "calm"}, {"at": "@fold", "face": "strain"},
                                        {"at": "@don't", "face": "smile"}],
                                  pose=[{"at": 0, "pose": "stand"}, {"at": "@don't", "pose": "wave"}]),
              "layers": [hud(clk)],
              "camera": {"shake": [shake("@cracks", 18, 0.5)]}})
    S[-1]["background"]["props"].pop("focusXH")

    # P5 Paris: eye to eye with the top of the Eiffel Tower
    h9 = 1.75 + 0.01 * 9 * 3600
    clk = [k(0, 9 * 3600), k("@:end", 9.4 * 3600)]
    items5 = [{"kind": "skyline", "x0": -4000, "x1": 4000, "seed": "pa"},
              {"kind": "sun", "sx": 0.84, "sy": 0.19, "r": 0.055},
              {"kind": "paris", "x0": -2500, "x1": -80, "seed": "pr1"},
              {"kind": "paris", "x0": 80, "x1": 2500, "seed": "pr2"},
              {"kind": "eiffel", "x": 158}]
    S.append({"p": 5, "beat": "landmark", "setting": setting("place", "city", "Paris"),
              "background": world(clk, items5, ground="street", seed="pa",
                                  lppm=[k(0, 0.42), k("@eye", 0.42), k("@top", 0.62, "inOut")],
                                  gy=[k(0, 0.64), k("@eye", 0.64), k("@top", 0.64 + 0.4 * 0 + 0.0, "inOut")],
                                  focusXH=None,
                                  cx=[k(0, 0.42), k("@eye", 0.42), k("@top", 0.24, "inOut")],
                                  face=[{"at": 0, "face": "calm"}, {"at": "@eye", "face": "wow"}]),
              "layers": [hud(clk)]})
    bg = S[-1]["background"]["props"]
    bg.pop("focusXH")
    # push to the face: keep eye level (~0.86 of YOU) at screen y 0.36
    bg.pop("gy")
    bg["focusAlt"] = [k(0, 0.0), k("@eye", 0.0), k("@top", 0.86, "inOut")]
    bg["focusY"] = [k(0, 0.64), k("@eye", 0.64), k("@top", 0.38, "inOut")]

    # P6 the clouds at your shoulders on day two
    clk = [k(0, 1.05 * DAY), k("@:end", 1.6 * DAY)]
    clouds = []
    deck = [(-1500, 1300, 700, False), (1400, 1400, 650, False), (-1300, 900, 620, True), (-650, 860, 560, True),
            (0, 980, 520, True), (650, 880, 600, True), (1300, 930, 640, True), (-950, 760, 640, True),
            (350, 740, 700, True), (1050, 780, 660, True), (-1500, 720, 620, True)]
    for i, (x, alt, w, front) in enumerate(deck):
        clouds.append({"kind": "cloud", "x": x, "alt": alt, "w": w, "seed": f"c6{i}", "front": front,
                       "drift": 70 if i % 2 else -70})
    S.append({"p": 6, "beat": "rung", "setting": setting("place", "sky", "above the clouds"),
              "background": world(clk, [{"kind": "sun", "sx": 0.2, "sy": 0.2, "r": 0.06},
                                        {"kind": "hills", "x0": -4000, "x1": 4000, "h": 160, "seed": "h6"}] + clouds, ground="land",
                                  seed="cl", lppm=[k(0, L(0.85)), k("@clouds", L(0.6), "inOut")],
                                  focusAlt=[k(0, 0.55), k("@clouds", 0.62, "inOut")], focusY=0.44, cx=0.5,
                                  face=[{"at": 0, "face": "wow"}, {"at": "@clouds", "face": "smile"}]),
              "layers": [hud(clk)]})

    # P7 Everest: pass the summit, then the thin air at your face
    clk = [k(0, 8.2e5), k("@Everest", 8.9e5, "inOut"), k("@:end", 9.05e5)]
    mts = [{"kind": "mountain", "x": -5200, "h": 7000, "w": 13000, "far": True, "seed": "m1"},
           {"kind": "mountain", "x": 13500, "h": 7400, "w": 13000, "far": True, "seed": "m2"},
           {"kind": "mountain", "x": 6600, "h": 8849, "w": 13000, "seed": "ev"},
           {"kind": "cloud", "x": -2500, "alt": 1600, "w": 2600, "seed": "c71", "front": True, "drift": 80},
           {"kind": "cloud", "x": 3000, "alt": 1400, "w": 2400, "seed": "c72", "front": True, "drift": -80}]
    S.append({"p": 7, "beat": "body", "setting": setting("place", "mountains", "Himalayas"),
              "background": world(clk, [{"kind": "sun", "sx": 0.15, "sy": 0.22, "r": 0.055}] + mts, ground="land",
                                  seed="ev", lppm=[k(0, L(0.075)), k("@air", L(0.08)), k("@face", L(0.2), "inOut")],
                                  focusAlt=[k(0, 0.0), k("@air", 0.0), k("@face", 0.86, "inOut")],
                                  focusY=[k(0, 0.69), k("@air", 0.69), k("@face", 0.4, "inOut")],
                                  cx=[k(0, 0.26), k("@air", 0.26), k("@face", 0.5, "inOut")],
                                  face=[{"at": 0, "face": "calm"}, {"at": "@Everest", "face": "wow"},
                                        {"at": "@thin", "face": "gasp"}],
                                  puffs=[{"at": "@thin"}, {"at": "@breathe"}, {"at": "@breathe+0.6"}]),
              "layers": [hud(clk)]})

    # P8 airliners cross under your chin
    clk = [k(0, 14 * DAY), k("@:end", 14.4 * DAY)]
    yh = 1.75 + 0.01 * 14 * DAY
    chin = yh * (1 - (92 + 4 - 12) / 344)
    planes = [{"kind": "plane", "x": -1150, "alt": chin - 120, "v": 900, "at": "@airliners", "dir": 1, "scale": 5,
               "trail": 2500, "front": True},
              {"kind": "plane", "x": 1150, "alt": chin - 380, "v": 850, "at": "@cruise", "dir": -1, "scale": 5,
               "trail": 2200, "front": True}]
    S.append({"p": 8, "beat": "rung", "setting": setting("place", "sky", "cruising altitude"),
              "background": world(clk, [{"kind": "sun", "sx": 0.82, "sy": 0.2, "r": 0.05},
                                        {"kind": "cloud", "x": -3000, "alt": 7000, "w": 3000, "seed": "c81"},
                                        {"kind": "cloud", "x": 4200, "alt": 6400, "w": 2600, "seed": "c82"}] + planes,
                                  ground="land", seed="pl", lppm=[k(0, L(0.36)), k("@:end", L(0.4))],
                                  focusAlt=0.8, focusY=0.46, cx=0.5,
                                  face=[{"at": 0, "face": "calm"}, {"at": "@airliners", "face": "shock"}]),
              "layers": [hud(clk)]})

    # P9 the edge of space, then one dive down to the feet still on your street
    clk = [k(0, 9.0e6), k("@space", 1.02e7, "inOut"), k("@while", 1.04e7)]
    yh = 1.75 + 0.01 * 1.04e7
    toe = (164 - 100) / 344 * yh            # toe tip x (m)
    st = [dict(i, x=i["x"] + toe) for i in street(60, 900, "s9")]
    items9 = [{"kind": "karman"}] + st + [{"kind": "block", "x": toe + 300, "w": 16, "floors": 10, "color": "magenta-1",
                                           "seed": "b9"}]
    S.append({"p": 9, "beat": "threshold", "setting": setting("place", "space", "edge of space", light="night"),
              "background": world(clk, items9, ground="street", seed="sp",
                                  lppm=[k(0, L(0.0098)), k("@while", L(0.0098)), k("@street", L(0.06), "inOut")],
                                  gy=0.66, focusXH=[k(0, 0.0), k("@while", 0.0), k("@street", 0.14, "inOut")],
                                  focusSX=0.5,
                                  face=[{"at": 0, "face": "calm"}, {"at": "@space", "face": "wow"},
                                        {"at": "@no", "face": "gasp"}]),
              "layers": [hud(clk),
                         tag("EDGE OF SPACE", "28%", "21%", "@edge", out="@while"),
                         tag("YOUR HOUSE", "80%", "41%", "@street", leader=[0, 470])]})

    # P10 the Moon beside you, Earth a ball under your feet
    clk = [k(0, 3.2e8), k("@wide", 3.47e8, "inOut"), k("@:end", 3.48e8)]
    yh = 1.75 + 0.01 * 3.47e8
    mx = 0.22 * yh + 1737400 + 300000
    S.append({"p": 10, "beat": "top", "setting": setting("place", "space", "Earth orbit", light="night"),
              "background": world(clk, [{"kind": "moon", "x": mx, "alt": 1737400, "from": "@Moon"}], ground="land",
                                  seed="mo", lppm=[k(0, L(1.55e-4)), k("@Earth", L(1.55e-4)), k("@ball", L(7.2e-5), "inOut")],
                                  gy=[k(0, 0.62), k("@Earth", 0.62), k("@ball", 0.36, "inOut")],
                                  cx=[k(0, 0.32), k("@Earth", 0.32), k("@ball", 0.42, "inOut")],
                                  face=[{"at": 0, "face": "calm"}, {"at": "@Moon", "face": "wow"}]),
              "layers": [hud(clk), tag("3,475 KM ACROSS", "70%", "24%", "@Moon+0.2", out="@Earth")]})

    # P11 the reframe: the clock turns on the viewer; the bedroom again (loop to frame 0)
    room11 = [{"kind": "room", "ceiling": 2.4, "at": "@ceiling"}]
    clk = [k(0, 0), k("@ceiling", 65, "inOut")]
    S.append({"p": 11, "beat": "loop", "setting": setting("place", "home", "your bedroom"),
              "background": world(clk, room11, lin=True, seed="room",
                                  lppm=[k(0, 2.49), k("@ceiling", 2.57, "out")], gy=0.64, cx=0.52,
                                  face=[{"at": 0, "face": "calm"}, {"at": "@taller", "face": "worried"},
                                        {"at": "@ceiling", "face": "strain"}],
                                  pose=[{"at": 0, "pose": "stand"}, {"at": "@ceiling+0.15", "pose": "shrug"}]),
              "layers": [hud(clk, lin=True, title="SINCE YOU PRESSED PLAY", titleUntil="@already")],
              "camera": {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": "@ceiling", "zoom": 1.03, "ease": "inOut"}],
                         "shake": [shake("@ceiling", 12)]}})

    # remove helper Nones (tag cue)
    for s in S:
        for l in s.get("layers", []):
            if l.get("cue", 1) is None:
                l.pop("cue")
        s["_house"] = {"set": False}
    return S


def main():
    shots = {"niche": "explainer", "emphasis": ["ceiling.", "thousand", "Everest,", "space,", "Moon"],
             "glue": ["Eiffel Tower", "Mount Everest", "ten-storey building"], "scenes": scenes()}
    with open(os.path.join(HERE, "shots.json"), "w") as f:
        json.dump(shots, f, indent=1)
    print("shots.json:", len(shots["scenes"]), "scenes")


if __name__ == "__main__":
    main()
