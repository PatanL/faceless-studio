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
    return {"at": at, "duration": dur, "amplitude": amp, "frequency": 9, "rotate": 0, "decay": True}


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
    SUN = {"kind": "sun", "sx": 0.18, "sy": 0.2, "r": 0.055}     # one sun, upper left: the light every shadow agrees with

    # P1 hook: the bedroom, YOU sprouting toward the ceiling (frame 0 = the cover); the plate counts from 0
    room1 = [{"kind": "room", "ceiling": 2.35, "at": "@hits"}]
    clk = [k(0, 0), k("@hits", 60, "linear")]
    S.append({"p": 1, "beat": "hook", "setting": setting("place", "home", "your bedroom"),
              "background": world(clk, room1, lin=True, seed="room",
                                  lppm=[k(0, 2.6), k("@hits", 2.8, "inOut")],
                                  focusAlt=[k(0, 0.62), k("@hits", 0.88, "inOut")],
                                  focusY=[k(0, 0.5), k("@hits", 0.42, "inOut")], cx=0.52,
                                  face=[{"at": 0, "face": "calm"}, {"at": "@minute", "face": "worried"},
                                        {"at": "@hits", "face": "strain"}],
                                  sy=[k(0, 1), k("@hits", 1), k("@hits+0.12", 0.95, "out"), k("@hits+0.5", 0.97)]),
              "layers": [hud(clk, lin=True, ff=True)]})
    S[-1]["background"]["props"]["shake"] = [shake("@hits", 16)]

    # P2 street: in front of your house, outgrow the rooflines and a ten-storey block, then down to a car by the shoe
    items = [SUN, {"kind": "house", "x": -1.5, "w": 11, "h": 6.2, "color": "coral-2", "roof": "dusk-1"}] + \
        street(-130, -12, "s2a") + street(14, 170, "s2b") + [
        {"kind": "block", "x": 30, "w": 16, "floors": 10, "color": "magenta-1", "seed": "b2"},
        {"kind": "level", "alt": 33, "text": "10 FLOORS", "at": "@taller", "until": "@and", "color": "amber-4"},
        {"kind": "car", "x": 9.6, "color": "coral-2"},
        {"kind": "car", "x": -48, "color": "amber-2"},
        {"kind": "marker", "x": 9.6, "alt": 1.5, "dx": 150, "dy": -330, "text": "CAR 4.5 M", "at": "@car", "front": True},
    ]
    clk = [k(0, 60), k("@metres", 3600, "inOut"), k("@:end", 3900)]
    S.append({"p": 2, "beat": "rung1", "setting": setting("place", "town", "your street"),
              "background": world(clk, items, seed="st",
                                  lppm=[k(0, 2.2), k("@metres", 1.1, "inOut"), k("@you're", 1.1), k("@building", 1.22),
                                        k("@building.end", 1.2), k("@smaller", 1.75, "inOut")],
                                  gy=[k(0, 0.64), k("@building.end", 0.64), k("@smaller", 0.6, "inOut")],
                                  cx=[k(0, 0.5), k("@metres", 0.34), k("@building.end", 0.34), k("@smaller", 0.2, "inOut")],
                                  face=[{"at": 0, "face": "strain"}, {"at": "@added", "face": "wow"},
                                        {"at": "@car", "face": "smile"}]),
              "layers": [hud(clk, ff=True, ffUntil="@you're")]})

    # P3 the square-cube law on YOU in the street: x20 bracket, x8,000 weight arrows, x400 glowing bones
    clk = [k(0, 3900), k("@:end", 4100)]
    S.append({"p": 3, "beat": "science", "setting": setting("place", "town", "your street (x-ray)"),
              "background": world(clk, [SUN, {"kind": "block", "x": 24, "w": 16, "floors": 10, "color": "magenta-1",
                                              "seed": "b2"},
                                        {"kind": "marker", "x": -10.3, "alt": 1.0, "dx": -150, "dy": -230,
                                         "text": "1.75 M YOU", "at": "@twenty+0.3", "front": True, "size": 40}] + street(-150, -14, "s3a") + street(48, 200, "s3b"),
                                  seed="x3", lppm=1.27, gy=0.69, cx=0.5,
                                  face=[{"at": 0, "face": "calm"}, {"at": "@heavier", "face": "strain"},
                                        {"at": "@bones", "face": "worried"}],
                                  sy=[k(0, 1), k("@heavier", 1), k("@heavier+0.3", 0.97, "out")],
                                  xray={"times": ["@twenty", "@eight", "@bones"]}),
              "layers": [hud(clk)]})
    S[-1]["background"]["props"]["shake"] = [shake("@heavier", 8, 0.35)]

    # P4 street: close on the leg, the step cracks the road, the knees dip and hold, then pull back as you grow
    clk = [k(0, 4100), k("@keep", 4400), k("@:end", 14000, "in")]
    items4 = [SUN] + street(-160, -14, "s4a") + street(30, 200, "s4b") + [
        {"kind": "block", "x": 44, "w": 16, "floors": 10, "color": "magenta-1", "seed": "b2"},
        {"kind": "car", "x": 14, "color": "tide-2"},
        {"kind": "crack", "x": 4.2, "w": 16, "at": "@cracks"},
    ]
    S.append({"p": 4, "beat": "turn", "setting": setting("place", "town", "your street"),
              "background": world(clk, items4, seed="st4",
                                  lppm=[k(0, 1.72), k("@and", 1.72), k("@knees", 1.68, "inOut"), k("@keep", 1.68),
                                        k("@:end", 0.5, "in")],
                                  gy=[k(0, 0.62), k("@and", 0.62), k("@knees", 0.66, "inOut"), k("@keep", 0.66)],
                                  cx=[k(0, 0.36), k("@and", 0.36), k("@knees", 0.5, "inOut"), k("@keep", 0.5),
                                      k("@:end", 0.45, "inOut")],
                                  fold=[k(0, 0), k("@fold", 0), k("@here", 1, "out"), k("@don't", 1),
                                        k("@don't+0.35", 0, "backOut")],
                                  sy=[k(0, 1), k("@fold", 1), k("@here", 0.88, "out"), k("@don't", 0.88),
                                      k("@don't+0.35", 1.0, "backOut")],
                                  face=[{"at": 0, "face": "calm"}, {"at": "@fold", "face": "strain"},
                                        {"at": "@don't", "face": "smile"}]),
              "layers": [hud(clk)]})
    S[-1]["background"]["props"]["shake"] = [shake("@cracks", 18, 0.5), shake("@don't", 6, 0.3)]

    # P5 Paris: eye to eye with the top of the Eiffel Tower
    clk = [k(0, 30700), k("@top", 31100, "inOut"), k("@:end", 31150)]
    items5 = [SUN, {"kind": "skyline", "x0": -4000, "x1": 4000, "seed": "pa"},
              {"kind": "paris", "x0": -2500, "x1": -80, "seed": "pr1"},
              {"kind": "paris", "x0": 80, "x1": 2500, "seed": "pr2"},
              {"kind": "eiffel", "x": 158},
              {"kind": "level", "alt": 276, "at": "@eye#2", "text": "TOP DECK 276 M", "hits": ["@top"], "labelX": 0.92}]
    S.append({"p": 5, "beat": "landmark", "setting": setting("place", "city", "Paris"),
              "background": world(clk, items5, ground="street", seed="pa",
                                  lppm=[k(0, 0.42), k("@hours", 0.42), k("@top", 0.6, "inOut")],
                                  focusAlt=[k(0, 0.0), k("@hours", 0.0), k("@top", 0.86, "inOut")],
                                  focusY=[k(0, 0.66), k("@hours", 0.66), k("@top", 0.4, "inOut")],
                                  cx=[k(0, 0.4), k("@hours", 0.4), k("@top", 0.24, "inOut")],
                                  face=[{"at": 0, "face": "calm"}, {"at": "@eye", "face": "wow"}]),
              "layers": [hud(clk)]})

    # P6 the clouds at your head on day two
    clk = [k(0, 1.05 * DAY), k("@:end", 1.6 * DAY)]
    clouds = []
    deck = [(-1500, 1300, 700, False), (1400, 1400, 650, False), (-1300, 900, 620, True), (-650, 860, 560, True),
            (0, 980, 520, True), (650, 880, 600, True), (1300, 930, 640, True), (-950, 760, 640, True),
            (350, 740, 700, True), (1050, 780, 660, True), (-1500, 720, 620, True)]
    for i, (x, alt, w, front) in enumerate(deck):
        clouds.append({"kind": "cloud", "x": x, "alt": alt, "w": w, "seed": f"c6{i}", "front": front,
                       "drift": 70 if i % 2 else -70})
    S.append({"p": 6, "beat": "rung", "setting": setting("place", "sky", "above the clouds"),
              "background": world(clk, [SUN, {"kind": "hills", "x0": -4000, "x1": 4000, "h": 160, "seed": "h6"}] + clouds,
                                  ground="land", seed="cl", lppm=[k(0, L(0.85)), k("@clouds", L(0.6), "inOut")],
                                  focusAlt=[k(0, 0.55), k("@clouds", 0.62, "inOut")], focusY=0.44, cx=0.5,
                                  face=[{"at": 0, "face": "wow"}, {"at": "@clouds", "face": "smile"}]),
              "layers": [hud(clk)]})

    # P7 Everest: the head passes the summit line on "top", then the thin air at your face
    clk = [k(0, 8.3e5), k("@pass", 8.62e5), k("@top", 9.06e5, "inOut"), k("@:end", 9.07e5)]
    mts = [{"kind": "mountain", "x": -5200, "h": 7000, "w": 13000, "far": True, "seed": "m1"},
           {"kind": "mountain", "x": 13500, "h": 7400, "w": 13000, "far": True, "seed": "m2"},
           {"kind": "mountain", "x": 3700, "h": 8849, "w": 13000, "seed": "ev"},
           {"kind": "level", "alt": 8849, "text": "EVEREST 8,849 M", "labelX": 0.97, "hits": ["@top"], "until": "@air"},
           {"kind": "hills", "x0": -9000, "x1": 16000, "h": 900, "seed": "fh", "color": "violet-1",
            "color2": "violet-0", "front": True},
           {"kind": "cloud", "x": -2500, "alt": 1600, "w": 2600, "seed": "c71", "front": True, "drift": 80},
           {"kind": "cloud", "x": 3000, "alt": 1400, "w": 2400, "seed": "c72", "front": True, "drift": -80}]
    S.append({"p": 7, "beat": "body", "setting": setting("place", "mountains", "Himalayas"),
              "background": world(clk, [SUN] + mts, ground="rock", seed="ev",
                                  lppm=[k(0, L(0.08)), k("@days", L(0.08)), k("@top", L(0.2), "inOut"), k("@and", L(0.2)),
                                        k("@face", L(0.32), "inOut")],
                                  focusAlt=[k(0, 0.0), k("@days", 0.0), k("@top", 0.93, "inOut"), k("@and", 0.93),
                                            k("@face", 0.86, "inOut")],
                                  focusY=[k(0, 0.74), k("@days", 0.74), k("@top", 0.4, "inOut"), k("@and", 0.4),
                                          k("@face", 0.42, "inOut")],
                                  cx=[k(0, 0.22), k("@days", 0.22), k("@top", 0.2, "inOut"), k("@and", 0.2),
                                      k("@face", 0.5, "inOut")],
                                  face=[{"at": 0, "face": "calm"}, {"at": "@pass", "face": "wow"},
                                        {"at": "@thin", "face": "gasp"}],
                                  pose=[{"at": 0, "pose": "stand"}],
                                  puffs=[{"at": "@thin"}, {"at": "@thin+0.3"}, {"at": "@breathe"},
                                         {"at": "@breathe+0.3"}]),
              "layers": [hud(clk)]})

    # P8 airliners cross under your chin (planes drawn 5x so they read)
    clk = [k(0, 14 * DAY), k("@:end", 14.4 * DAY)]
    yh = 1.75 + 0.01 * 14 * DAY
    chin = yh * (1 - (92 + 4 - 12) / 344)
    planes = [{"kind": "plane", "x": -1300, "alt": chin - 70, "v": 1500, "at": "@airliners", "dir": 1, "scale": 5,
               "trail": 3000, "front": True},
              {"kind": "plane", "x": 1400, "alt": chin - 260, "v": 1400, "at": "@cruise", "dir": -1, "scale": 5,
               "trail": 2600, "front": True}]
    S.append({"p": 8, "beat": "rung", "setting": setting("place", "sky", "cruising altitude"),
              "background": world(clk, [SUN, {"kind": "cloud", "x": -3000, "alt": 7000, "w": 3000, "seed": "c81"},
                                        {"kind": "cloud", "x": 4200, "alt": 6400, "w": 2600, "seed": "c82"}] + planes,
                                  ground="land", seed="pl", lppm=[k(0, L(0.25)), k("@:end", L(0.28))],
                                  focusAlt=0.8, focusY=0.5, cx=0.5,
                                  face=[{"at": 0, "face": "gasp"}, {"at": "@airliners", "face": "shock"}]),
              "layers": [hud(clk)]})

    # P9 the edge of space: mountains and clouds at your feet, the 100 km line, then one dive to the street
    clk = [k(0, 9.5e6), k("@space.end", 1.03e7, "linear"), k("@while", 1.04e7)]
    yh = 1.75 + 0.01 * 1.04e7
    toe = (164 - 100) / 344 * yh            # toe tip x (m)
    items9 = [{"kind": "level", "alt": 100000, "text": "SPACE: 100 KM", "labelX": 0.97, "hits": ["@space"]},
              {"kind": "mountain", "x": -16000, "h": 7500, "w": 14000, "far": True, "seed": "m91"},
              {"kind": "mountain", "x": 26000, "h": 8000, "w": 15000, "far": True, "seed": "m92"},
              {"kind": "cloud", "x": -14000, "alt": 2500, "w": 9000, "seed": "c91", "front": True},
              {"kind": "cloud", "x": 33000, "alt": 2200, "w": 8000, "seed": "c92", "front": True},
              {"kind": "town", "x0": toe + 120, "n": 9, "px": 16},
              {"kind": "marker", "x": toe + 700, "alt": 0, "dx": -170, "dy": -420, "text": "YOUR STREET", "at": "@in",
               "front": True}]
    S.append({"p": 9, "beat": "threshold", "setting": setting("place", "space", "edge of space", light="night"),
              "background": world(clk, items9, ground="land", seed="sp",
                                  lppm=[k(0, L(0.0082)), k("@there's", L(0.0095)), k("@all", L(0.02), "inOut"),
                                        k("@while", L(0.02)), k("@street", L(0.06), "inOut")],
                                  focusAlt=[k(0, 0.5), k("@there's", 0.5), k("@all", 0.88, "inOut"), k("@while", 0.88),
                                            k("@street", 0.0, "inOut")],
                                  focusY=[k(0, 0.43), k("@there's", 0.43), k("@all", 0.4, "inOut"), k("@while", 0.4),
                                          k("@street", 0.66, "inOut")],
                                  focusXH=[k(0, 0.0), k("@while", 0.0), k("@street", 0.14, "inOut")], focusSX=0.5,
                                  face=[{"at": 0, "face": "calm"}, {"at": "@space", "face": "wow"},
                                        {"at": "@no", "face": "strain"}, {"at": "@feet", "face": "calm"}]),
              "layers": [hud(clk)]})

    # P10 the Moon beside you, then pull back: Earth a ball under your feet
    clk = [k(0, 3.36e8), k("@wide", 3.47e8, "inOut"), k("@:end", 3.48e8)]
    yh = 1.75 + 0.01 * 3.47e8
    mx = 0.22 * yh + 1737400 + 300000
    S.append({"p": 10, "beat": "top", "setting": setting("place", "space", "Earth orbit", light="night"),
              "background": world(clk, [{"kind": "moon", "x": mx, "alt": 1737400, "from": "@Moon"},
                                        {"kind": "marker", "x": mx, "alt": 3474800 + 150000, "dx": 0, "dy": -170,
                                         "text": "3,475 KM WIDE", "at": "@wide", "until": "@Earth", "front": True,
                                         "size": 44},
                                        {"kind": "marker", "x": 0, "alt": -6371000, "dx": 0, "dy": 0,
                                         "text": "EARTH 12,742 KM", "at": "@ball+0.2", "front": True, "size": 46}],
                                  ground="land", seed="mo",
                                  lppm=[k(0, L(1.55e-4)), k("@wide.end", L(1.55e-4)), k("@ball.end", L(7.4e-5), "inOut")],
                                  gy=[k(0, 0.62), k("@wide.end", 0.62), k("@ball.end", 0.34, "inOut")],
                                  cx=[k(0, 0.32), k("@wide.end", 0.32), k("@ball.end", 0.5, "inOut")],
                                  face=[{"at": 0, "face": "calm"}, {"at": "@Moon", "face": "wow"}]),
              "layers": [hud(clk)]})

    # P11 the reframe: the clock turns on the viewer; the bedroom again (loop to frame 0)
    room11 = [{"kind": "room", "ceiling": 2.35, "at": "@ceiling"}]
    clk = [k(0, 0), k("@sixty", 58), k("@ceiling", 60, "out")]
    S.append({"p": 11, "beat": "loop", "setting": setting("place", "home", "your bedroom"),
              "background": world(clk, room11, lin=True, seed="room",
                                  lppm=[k(0, 2.6), k("@ceiling", 2.8, "inOut")],
                                  focusAlt=[k(0, 0.62), k("@ceiling", 0.88, "inOut")],
                                  focusY=[k(0, 0.5), k("@ceiling", 0.42, "inOut")], cx=0.52,
                                  face=[{"at": 0, "face": "calm"}, {"at": "@taller", "face": "worried"},
                                        {"at": "@ceiling", "face": "strain"}],
                                  sy=[k(0, 1), k("@ceiling", 1), k("@ceiling+0.12", 0.95, "out"), k("@ceiling+0.5", 0.97)]),
              "layers": [hud(clk, lin=True, ff=True)]})
    S[-1]["background"]["props"]["shake"] = [shake("@ceiling", 12)]

    for s in S:
        for l in s.get("layers", []):
            if l.get("cue", 1) is None:
                l.pop("cue")
        s["_house"] = {"set": False}
        if s["p"] > 1:
            s["transitionIn"] = {"type": "cut"}      # Zack-style hard cuts (house "cuts": false keeps them)
    return S


def main():
    shots = {"niche": "explainer", "house": {"cuts": False},
             "emphasis": ["ceiling.", "thousand", "Everest,", "space,", "Moon"],
             "glue": ["one minute later", "Eiffel Tower", "Mount Everest", "ten-storey building", "eye to eye",
                      "the second day", "ten days in", "two weeks in", "four months", "eleven years in",
                      "pressed play", "sixty centimetres", "four hundred", "eight thousand"],
             "scenes": scenes()}
    with open(os.path.join(HERE, "shots.json"), "w") as f:
        json.dump(shots, f, indent=1)
    print("shots.json:", len(shots["scenes"]), "scenes")


if __name__ == "__main__":
    main()
