#!/usr/bin/env python3
"""Write shots.json (word-anchored scene specs for pipeline/episodes/auto.py) for explainer-short-cookiecutter-shark.

One scene per narration paragraph (13). Every time is a spoken-word anchor ("@word", "@word#2", "@word.end+0.2")
resolved by auto.py against the measured Kokoro captions (speed 1.15). Shot numbers match the script.md shot list.
All art is inline svg (no new component names); overlays share the hero's viewBox and layer box so they line up.

usage: python3 gen_storyboard.py <out/shots.json>
then (Spark): python3 -m pipeline.episodes.auto explainer-short-cookiecutter-shark   -> storyboard.json (+ zod)
"""
import json
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "shots.json"
Y = "#ffe14d"      # yellow highlight
RED = "#e5483d"

# ------------------------------------------------------------------ svg assets (unique gradient ids, no id="g")
X = 'xmlns="http://www.w3.org/2000/svg"'
_BODY = ('M392 58 Q386 34 340 31 L120 37 Q62 41 30 52 L8 38 L15 58 L8 78 L30 64 Q62 76 120 80 L340 86 Q386 82 392 58 Z')
CC_SIDE = (f'<svg viewBox="0 0 400 110" {X}><path d="{_BODY}" fill="#3b2c25"/>'
           '<path d="M150 37 L168 21 L186 36 Z M96 41 L110 29 L122 40 Z" fill="#2c201b"/>'
           '<path d="M298 33 L322 32 L322 86 L298 85 Z" fill="#160e0b"/>'
           '<path d="M60 70 Q200 84 296 82" stroke="#7dffb0" stroke-width="3" stroke-dasharray="2 7" fill="none" opacity="0.8"/>'
           '<circle cx="362" cy="50" r="7" fill="#b9f3e4"/><circle cx="363" cy="50" r="3" fill="#0b1a22"/>'
           '<ellipse cx="386" cy="64" rx="8" ry="11" fill="#6b4a3f"/></svg>')
CC_GLOW = (f'<svg viewBox="0 0 400 110" {X}><defs><radialGradient id="ccg" cx="0.5" cy="0.5" r="0.5">'
           '<stop offset="0" stop-color="#9dffc4" stop-opacity="0.9"/><stop offset="1" stop-color="#3dff9a" stop-opacity="0"/>'
           '</radialGradient></defs><ellipse cx="190" cy="82" rx="185" ry="26" fill="url(#ccg)"/></svg>')
CC_LIPS = (f'<svg viewBox="0 0 400 110" {X}><ellipse cx="386" cy="64" rx="10" ry="13" fill="{Y}" fill-opacity="0.45" '
           f'stroke="{Y}" stroke-width="4"/></svg>')
CC_TOP_TEETH = (f'<svg viewBox="0 0 400 110" {X}><path d="M378 55 L381 61 L384 55 Z M384 55 L387 61 L390 55 Z" '
                f'fill="{Y}" stroke="{Y}" stroke-width="1.5"/></svg>')
CC_LOW_TEETH = (f'<svg viewBox="0 0 400 110" {X}><path d="M366 74 L370 64 L374 74 L378 64 L382 74 L386 64 L390 74 Z" '
                f'fill="{Y}" stroke="#b89a00" stroke-width="1"/></svg>')
CC_COLLAR = (f'<svg viewBox="0 0 400 110" {X}><path d="M298 33 L322 32 L322 86 L298 85 Z" fill="none" stroke="{Y}" '
             'stroke-width="4"/></svg>')
RING = f'<svg viewBox="0 0 200 200" {X}><circle cx="100" cy="100" r="88" fill="none" stroke="{Y}" stroke-width="12"/></svg>'
HOLE = (f'<svg viewBox="0 0 200 200" {X}><defs><radialGradient id="hlg"><stop offset="0.6" stop-color="#140707"/>'
        '<stop offset="1" stop-color="#5a2b28"/></radialGradient></defs><circle cx="100" cy="100" r="96" fill="url(#hlg)"/></svg>')
SKIN_WALL = (f'<svg viewBox="0 0 1200 700" {X}><defs><linearGradient id="skg" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="#a99d95"/><stop offset="1" stop-color="#6f655f"/></linearGradient></defs>'
             '<rect width="1200" height="700" fill="url(#skg)"/><path d="M0 4 Q600 -10 1200 4" stroke="#c9beb6" stroke-width="8" fill="none"/>'
             '<g fill="#8a7f78"><ellipse cx="140" cy="120" rx="9" ry="4"/><ellipse cx="420" cy="220" rx="8" ry="4"/>'
             '<ellipse cx="760" cy="150" rx="9" ry="4"/><ellipse cx="1010" cy="300" rx="8" ry="4"/><ellipse cx="300" cy="420" rx="9" ry="4"/>'
             '<ellipse cx="880" cy="520" rx="9" ry="4"/></g></svg>')
SKIN_WALL_GREY = SKIN_WALL.replace("#a99d95", "#8f979d").replace("#6f655f", "#596169").replace("#c9beb6", "#aeb6bb") \
    .replace("#8a7f78", "#737b81").replace('id="skg"', 'id="skw"').replace("url(#skg)", "url(#skw)")
SKIN_WALL_HUMAN = SKIN_WALL.replace("#a99d95", "#e0b294").replace("#6f655f", "#b98262").replace("#c9beb6", "#f1cdb4") \
    .replace("#8a7f78", "#c99a7c").replace('id="skg"', 'id="skh"').replace("url(#skg)", "url(#skh)")
XSEC_WHALE = (f'<svg viewBox="0 0 1200 900" {X}><rect width="1200" height="60" fill="#596169"/>'
              '<rect y="60" width="1200" height="440" fill="#efe0c4"/><rect y="500" width="1200" height="400" fill="#c9707a"/>'
              '<path d="M0 280 Q300 300 600 280 T1200 280" stroke="#e2cfac" stroke-width="6" fill="none"/></svg>')
XSEC_HUMAN = (f'<svg viewBox="0 0 1200 900" {X}><rect width="1200" height="40" fill="#e0b294"/>'
              '<rect y="40" width="1200" height="220" fill="#f2d27a"/><rect y="260" width="1200" height="640" fill="#b23a48"/>'
              '<path d="M0 520 Q300 540 600 520 T1200 520" stroke="#9a2f3c" stroke-width="6" fill="none"/></svg>')
PLUG = (f'<svg viewBox="0 0 140 200" {X}><rect x="0" y="0" width="140" height="24" rx="10" fill="#596169"/>'
        '<rect x="0" y="22" width="140" height="120" fill="#efe0c4"/><rect x="0" y="140" width="140" height="60" rx="10" fill="#c9707a"/></svg>')
PLUG_HUMAN = PLUG.replace("#596169", "#e0b294").replace("#efe0c4", "#f2d27a").replace("#c9707a", "#b23a48")
HOLE_SAW = (f'<svg viewBox="0 0 200 200" {X}><circle cx="100" cy="100" r="86" fill="#9aa4ab" stroke="#5d666c" stroke-width="8"/>'
            '<circle cx="100" cy="100" r="16" fill="#3a4045"/><g fill="#d5dade">'
            + "".join(f'<path d="M100 4 L108 18 L92 18 Z" transform="rotate({a} 100 100)"/>' for a in range(0, 360, 24))
            + '</g></svg>')
SUCTION_CUP = (f'<svg viewBox="0 0 160 120" {X}><path d="M10 110 Q80 0 150 110 Z" fill="{RED}"/>'
               '<rect x="70" y="0" width="20" height="50" rx="6" fill="#8a1f1a"/></svg>')
ANCHOR = (f'<svg viewBox="0 0 120 140" {X}><g fill="none" stroke="#f3f6f7" stroke-width="12" stroke-linecap="round">'
          '<circle cx="60" cy="18" r="11"/><path d="M60 30 L60 128 M20 92 Q24 128 60 128 Q96 128 100 92 M36 54 L84 54"/></g></svg>')
GOLF_BALL = (f'<svg viewBox="0 0 120 120" {X}><circle cx="60" cy="60" r="56" fill="#f6f7f2"/><g fill="#d4d6cf">'
             + "".join(f'<circle cx="{x}" cy="{y}" r="5"/>' for x, y in ((40, 36), (64, 30), (84, 46), (34, 62), (60, 56),
                                                                          (86, 70), (46, 86), (70, 84)))
             + '</g></svg>')
POOL_FLOAT = (f'<svg viewBox="0 0 560 300" {X}><path d="M30 190 Q120 90 330 100 Q470 104 530 170 Q470 240 300 240 Q130 240 30 190 Z" '
              'fill="#7cc6f0" stroke="#2f7fb0" stroke-width="8"/><path d="M60 200 Q250 250 500 180" fill="#f3f6f7"/>'
              '<path d="M250 104 L300 10 L340 104 Z" fill="#7cc6f0" stroke="#2f7fb0" stroke-width="8"/>'
              '<circle cx="440" cy="150" r="22" fill="#fff"/><circle cx="446" cy="150" r="11" fill="#0b1a22"/>'
              '<path d="M470 196 Q500 205 520 186" stroke="#0b1a22" stroke-width="6" fill="none"/>'
              '<path d="M30 190 L0 150 L4 230 Z" fill="#7cc6f0" stroke="#2f7fb0" stroke-width="8"/></svg>')
FOREARM = (f'<svg viewBox="0 0 620 120" {X}><path d="M0 40 L470 46 Q520 30 580 40 Q620 60 580 84 Q520 92 470 76 L0 82 Z" '
           'fill="#f3f6f7" stroke="#0b1a22" stroke-width="6"/></svg>')
BURJ = (f'<svg viewBox="0 0 100 828" {X}><path d="M50 0 L53 120 L60 260 L66 420 L74 600 L84 828 L16 828 L26 600 L34 420 L40 260 '
        'L47 120 Z" fill="#20323b" stroke="#5f7a86" stroke-width="2"/></svg>')
DOLPHIN = (f'<svg viewBox="0 0 700 280" {X}><path d="M40 150 Q140 82 360 84 Q500 86 580 112 Q610 124 618 136 L692 144 '
           'L692 152 L612 158 Q520 196 320 198 Q140 196 40 150 Z" fill="#8c9aa4"/><path d="M180 176 Q300 196 560 170 Q470 190 320 192 '
           'Q220 190 180 176 Z" fill="#c9d3d9"/><path d="M300 88 Q330 44 376 18 Q360 58 384 88 Z" fill="#7a8892"/>'
           '<path d="M44 150 L2 104 L16 150 L2 198 Z" fill="#7a8892"/><circle cx="586" cy="132" r="7" fill="#0b1a22"/></svg>')
SUB = (f'<svg viewBox="0 0 900 300" {X}><path d="M60 150 Q60 100 160 100 L760 100 Q880 100 880 150 Q880 200 760 200 L160 200 '
       'Q60 200 60 150 Z" fill="#3c464d"/><path d="M760 100 Q880 100 880 150 Q880 200 760 200 Z" fill="#5a4c40"/>'
       '<rect x="360" y="50" width="160" height="56" rx="12" fill="#3c464d"/><path d="M60 150 L10 110 L10 190 Z" fill="#30393f"/></svg>')
THUMB_SIL = (f'<svg viewBox="0 0 140 338" {X}><rect x="10" y="0" width="120" height="338" rx="58" fill="#e0b294" '
             'stroke="#0b1a22" stroke-width="6"/><rect x="34" y="250" width="72" height="70" rx="26" fill="#f3d9c8"/></svg>')
SCAR = f'<svg viewBox="0 0 100 100" {X}><circle cx="50" cy="50" r="40" fill="none" stroke="#e8e2d6" stroke-width="10"/></svg>'
PENCIL = f'<svg viewBox="0 0 100 20" {X}><rect x="0" y="4" width="84" height="12" fill="#f2c230"/><path d="M84 4 L100 10 L84 16 Z" fill="#3a2c25"/></svg>'
FISH = (f'<svg viewBox="0 0 220 90" {X}><path d="M20 45 Q70 5 150 30 Q190 40 205 45 Q190 52 150 60 Q70 85 20 45 Z" fill="#e9d6df" '
        'opacity="0.85"/><path d="M20 45 L0 25 L6 45 L0 65 Z" fill="#e9d6df" opacity="0.7"/><circle cx="178" cy="42" r="4" fill="#222"/></svg>')
TUNA = FISH.replace("#e9d6df", "#9fb7c9")
BAIT_FISH = FISH.replace("#e9d6df", "#160e0b").replace('opacity="0.85"', 'opacity="1" stroke="#ffe14d" stroke-width="5"')
GLOW = (f'<svg viewBox="0 0 200 200" {X}><defs><radialGradient id="bg1"><stop offset="0" stop-color="#fff6d8"/>'
        '<stop offset="0.25" stop-color="#ffd27a" stop-opacity="0.9"/><stop offset="1" stop-color="#ffd27a" stop-opacity="0"/>'
        '</radialGradient></defs><circle cx="100" cy="100" r="100" fill="url(#bg1)"/></svg>')
GREEN_GLOW = GLOW.replace("#fff6d8", "#d8fff0").replace("#ffd27a", "#3dff9a").replace('id="bg1"', 'id="gg1"').replace("url(#bg1)", "url(#gg1)")
NIGHT_SEA = (f'<svg viewBox="0 0 1080 1920" {X}><defs><linearGradient id="nsg" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="#02060c"/><stop offset="0.4" stop-color="#0b1e2b"/><stop offset="0.401" stop-color="#06202c"/>'
             '<stop offset="1" stop-color="#010507"/></linearGradient></defs><rect width="1080" height="1920" fill="url(#nsg)"/></svg>')


# ------------------------------------------------------------------ helpers
def svg(markup, x, y, w, h, **kw):
    return {"type": "svg", "markup": markup, "x": x, "y": y, "width": w, "height": h, **kw}


def comp(name, x, y, w, h, props=None, **kw):
    return {"type": "component", "name": f"explainer/{name}", "x": x, "y": y, "width": w, "height": h, "props": props or {}, **kw}


def tag(text, x, y, at, size=44, **kw):
    props = {"text": text, "at": at, "size": size, "align": "center"}
    for k in ("accent", "color", "bg", "out"):
        if k in kw:
            props[k] = kw.pop(k)
    w = round(0.62 * size * len(text) + 80)
    return comp("Tag", x, y, w, round(size * 2.4), props, z=kw.pop("z", 30), depth=0, **kw)


def head(text, at, red=None, y=300, size=112, out=None, **kw):
    props = {"text": text, "at": at, "size": size, "color": "white", "underline": False}
    if red:
        props["red"] = red
    if out is not None:
        props["out"] = out
    lines = text.count("\n") + 1
    return comp("Headline", 540, y, 1000, round(size * 1.25 * lines + 60), props, z=40, depth=0, **kw)


def ring(x, y, w, h, at, **kw):
    """Yellow ring: never draws on; enters with scale 0.6 -> 1 and opacity 0 -> 1 (producibility fix)."""
    return svg(RING, x, y, w, h, start=at, z=kw.pop("z", 12), keyframes=[
        {"t": at, "scale": 0.6, "opacity": 0}, {"t": f"{at}+0.35", "scale": 1, "opacity": 1, "ease": "out"}], **kw)


def flash(markup, x, y, w, h, at, dur, **kw):
    """Literal-analogy flash (FLY SHOW device): visible for dur seconds from at."""
    return svg(markup, x, y, w, h, start=at, end=f"{at}+{dur}", z=kw.pop("z", 20), enter={"type": "pop", "duration": 0.2}, **kw)


def glow_on(markup, x, y, w, h, at, **kw):
    """Part overlay on the hero's viewBox: opacity 0 -> 1 on its spoken word."""
    return svg(markup, x, y, w, h, start=at, z=kw.pop("z", 9), keyframes=[
        {"t": at, "opacity": 0}, {"t": f"{at}+0.2", "opacity": 1, "ease": "out"}], **kw)


def strike(x, y, w, at, **kw):
    return {"type": "rect", "x": x, "y": y, "width": w, "height": 16, "fill": RED, "radius": 8, "z": 35, "depth": 0,
            "start": f"{at}-0.35", "keyframes": [{"t": f"{at}-0.35", "scaleX": 0}, {"t": at, "scaleX": 1, "ease": "out"}], **kw}


def ocean(depth=30, **props):
    p = {"depth": depth, "rays": 7, "snow": 60}
    p.update(props)
    return {"type": "component", "name": "explainer/Ocean", "depth": 0.12, "overscan": 1.2, "props": p}


NIGHT = {"surface": 0.2, "skyTop": "#02060c", "skyBottom": "#0b1e2b", "rays": 0, "snow": 40}
P01_BG = {"depth": 30, "rays": 7, "snow": 60}


def latched_geom(mx, my, length, theta):
    """Centre of a CC_SIDE layer rotated theta deg (CSS, clockwise) whose mouth (viewBox x 392 of 400) sits at (mx, my)."""
    import math
    off = (392 - 200) / 400 * length
    return round(mx - off * math.cos(math.radians(theta))), round(my - off * math.sin(math.radians(theta)))


def hero_latched(start=None, end=None, skin=None, glow=True, mouth=(600, 1000), length=880, theta=55):
    """Frame-1 composition: a skin wall fills the lower part; the shark, big and diagonal, is latched mouth-first into it."""
    skin = skin or SKIN_WALL_HUMAN
    h = round(length * 110 / 400)
    cx, cy = latched_geom(mouth[0], mouth[1], length, theta)
    kw = {}
    if start is not None:
        kw["start"] = start
    if end is not None:
        kw["end"] = end
    L = [svg(skin, 540, 1340, 1200, 700, z=2, **kw)]
    if glow:
        L.append(svg(CC_GLOW, cx, cy, length, h, rotate=theta, z=4, idle=[{"type": "pulse", "amount": 0.15, "speed": 0.8}], **kw))
    L.append(svg(CC_SIDE, cx, cy, length, h, rotate=theta, z=5, idle=[{"type": "sway", "amount": 1.5, "speed": 0.6}], **kw))
    return L


def macro_parts():
    """Tool close-ups: mouth straight down into the wall at (540, 1000); body runs off the top, so the head is huge."""
    ln = 1500
    cx, cy = latched_geom(540, 1000, ln, 90)
    return cx, cy, ln, round(ln * 110 / 400)


# frame-1 hero geometry (shots 1, 3, 40): mouth on the wall top, body up-left, a finished hole to the right
F1 = dict(mouth=(600, 1000), length=880, theta=55)
MOUTH1 = (600, 1000)
HOLE1 = (880, 1110)

scenes = []

# ---------------------------------------------------------------- p01 HOOK (shots 1-3)
s = {"p": 1, "beat": "hook", "background": ocean(**P01_BG), "camera": {"preset": "pushIn", "amount": 0.4}, "layers": []}
L = s["layers"]
L += hero_latched(end="@perfect", **F1)
L += [svg(HOLE, *HOLE1, 230, 92, z=3, end="@perfect"), svg(RING, *HOLE1, 270, 112, z=6, end="@perfect"),
      svg(RING, *MOUTH1, 200, 80, z=6, end="@perfect")]
# shot 2: reverse-scale shock (BlueWhale pxPerM 34, shark 0.5 m = 17 px)
L += [comp("BlueWhale", 540, 720, 1000, 320, {"pxPerM": 34, "idle": False}, start="@perfect", end="@out", z=3),
      svg(CC_SIDE, 735, 712, 17, 5, start="@perfect", end="@out", z=6),
      ring(735, 712, 90, 90, "@perfect", end="@out")]
# shot 3: back on the hero, the shark twists and a second ring closes on "you"
L += hero_latched(start="@out", **F1)
L += [svg(HOLE, *HOLE1, 230, 92, z=3, start="@out"), svg(RING, *HOLE1, 270, 112, z=6, start="@out"),
      ring(*MOUTH1, 200, 80, "@you")]
L.append(head("PERFECT\nCIRCLES", -0.6, red="CIRCLES", y=290, size=120))
scenes.append(s)

# ---------------------------------------------------------------- p02 MISDIRECT (shots 4-6)
s = {"p": 2, "beat": "misdirect", "background": ocean(60), "transitionIn": {"type": "whip", "duration": 0.3},
     "camera": {"preset": "drift", "amount": 0.6}, "layers": []}
L = s["layers"]
L += [comp("GreatWhite", 540, 700, 760, 300, {"pxPerM": 120, "idle": False}, end="@tiger", z=3),
      tag("GREAT WHITE", 540, 960, "@forget", end="@tiger"), strike(540, 960, 520, "@tiger", end="@tiger+0.1")]
L += [comp("GreatWhite", 540, 700, 760, 300, {"pxPerM": 120, "idle": False, "silhouette": "#52606b"}, flipX=True,
           start="@tiger", end="@pool", z=3),
      tag("TIGER SHARK", 540, 960, "@tiger", start="@tiger", end="@pool"), strike(540, 960, 520, "@pool", end="@pool+0.1")]
L += [svg(POOL_FLOAT, 620, 740, 560, 300, start="@pool", z=4, idle=[{"type": "bob", "amount": 10, "speed": 0.7}]),
      comp("You", 240, 780, 170, 320, {"pose": "panic", "pxPerM": 120}, start="@pool", z=5),
      tag("POOL FLOAT", 540, 960, "@pool", start="@pool"), strike(540, 960, 480, "@kid")]
scenes.append(s)

# ---------------------------------------------------------------- p03 PIVOT + REVEAL + COUNT (shots 7-9)
s = {"p": 3, "beat": "pivot-reveal-count", "background": ocean(400), "transitionIn": {"type": "cut", "duration": 0},
     "camera": {"preset": "pushIn", "amount": 0.5}, "layers": []}
L = s["layers"]
L += [comp("You", 540, 760, 200, 360, {"pose": "stand"}, end="@is", z=5),
      svg(GREEN_GLOW, 540, 1250, 420, 420, end="@is", z=3, keyframes=[
          {"t": 0, "y": 1300, "opacity": 0.2}, {"t": "@included.end", "y": 1040, "opacity": 0.9, "ease": "out"}]),
      head("YOU\nINCLUDED", "@you", red="INCLUDED", y=320, out="@is")]
L += [svg(CC_GLOW, 540, 600, 520, 143, start="@is", end="@with", z=4, idle=[{"type": "pulse", "amount": 0.12, "speed": 0.8}]),
      svg(CC_SIDE, 540, 600, 520, 143, start="@is", end="@with", z=5, idle=[{"type": "bob", "amount": 6, "speed": 0.4}]),
      svg(FOREARM, 540, 800, 645, 126, start="@shorter", end="@with", z=5, enter={"type": "slideLeft", "duration": 0.3}),
      tag("COOKIECUTTER SHARK", 540, 420, "@cookiecutter", size=40, start="@is", end="@with"),
      comp("ScaleBar", 540, 930, 520, 120, {"label": "~50 CM / 1.6 FT", "at": "@shorter", "from": "left", "labelSize": 36},
           start="@shorter", end="@with", z=8)]
L += [svg(CC_SIDE, 540, 330, 360, 99, start="@with", z=5),
      comp("Options", 540, 760, 900, 520, {"title": "3 TOOLS", "items": ["SUCTION LIPS", "HOOK TEETH", "BLADE TEETH"],
                                           "at": "@three", "stagger": 0.15, "size": 50}, start="@with", z=20, depth=0)]
scenes.append(s)

# ---------------------------------------------------------------- p04 DEPTH + BAIT (shots 10-13)
s = {"p": 4, "beat": "depth-bait", "transitionIn": {"type": "fade", "duration": 0.3},
     "background": ocean([{"t": 0, "v": 1000}, {"t": "@feet.end", "v": 60, "ease": "out"}]),
     "camera": {"preset": "panUp", "amount": 0.5}, "layers": []}
L = s["layers"]
L += [comp("DepthMeter", 140, 700, 200, 1000, {"depth": [{"t": 0, "v": 1000}, {"t": "@feet.end", "v": 0, "ease": "inOut"}],
                                               "max": 1100, "window": 1100, "step": 100, "suffix": " M"},
           end="@glowing", z=10, depth=0),
      svg(BURJ, 330, 824, 92, 753, end="@glowing", z=3, opacity=0.9),
      comp("You", 720, 250, 50, 90, {"pose": "stand"}, end="@glowing", z=6),
      svg(CC_GLOW, 720, 1150, 300, 83, rotate=-20, end="@glowing", z=4,
          keyframes=[{"t": 0, "y": 1150}, {"t": "@feet.end", "y": 520, "ease": "inOut"}]),
      svg(CC_SIDE, 720, 1150, 300, 83, rotate=-20, end="@glowing", z=5,
          keyframes=[{"t": 0, "y": 1150}, {"t": "@feet.end", "y": 520, "ease": "inOut"}]),
      tag("1 KM / 3,300 FT", 720, 1000, "@kilometer", size=40, end="@glowing")]
HX, HY, HW, HH = 540, 650, 800, 220
L += [svg(CC_GLOW, HX, HY, HW, HH, start="@glowing", z=4, idle=[{"type": "pulse", "amount": 0.25, "speed": 1.0}]),
      svg(CC_SIDE, HX, HY, HW, HH, start="@glowing", z=5, idle=[{"type": "bob", "amount": 5, "speed": 0.4}]),
      glow_on(CC_COLLAR, HX, HY, HW, HH, "@collar", end="@scientists+0.3", exit={"type": "fade", "duration": 0.3}),
      tag("DARK COLLAR", 540, 900, "@collar", start="@collar", end="@scientists"),
      svg(BAIT_FISH, 765, 665, 170, 70, start="@scientists", z=8, enter={"type": "fade", "duration": 0.3}),
      head("BAIT?", "@think", y=300, size=120),
      tag("BEST GUESS", 540, 900, "@think", size=34, start="@think")]
scenes.append(s)

# ---------------------------------------------------------------- p05 THE MECHANISM, ONE SENTENCE (shots 14-22)
s = {"p": 5, "beat": "mechanism-chain", "background": ocean(200), "transitionIn": {"type": "whip", "duration": 0.3},
     "camera": {"preset": "pushIn", "amount": 0.3}, "layers": []}
L = s["layers"]
# 14 lure: tuna darts at the collar "fish"
L += [svg(CC_SIDE, 300, 650, 500, 138, end="@even", z=5), svg(BAIT_FISH, 470, 655, 80, 33, end="@even", z=6),
      svg(TUNA, 1150, 640, 260, 106, flipX=True, end="@even", z=7,
          keyframes=[{"t": 0, "x": 1150}, {"t": "@reaches.end", "x": 640, "ease": "out"}])]
# 15 whale-scale gag (visual only: pencil on a bus)
L += [comp("BlueWhale", 540, 740, 1000, 320, {"pxPerM": 34, "idle": False}, start="@even", end="@lips", z=3),
      svg(CC_SIDE, 735, 732, 17, 5, start="@even", end="@lips", z=6), ring(735, 732, 90, 90, "@even", end="@lips"),
      {"type": "rect", "x": 820, "y": 1010, "width": 400, "height": 230, "fill": "#0b1a22", "radius": 18, "opacity": 0.9,
       "start": "@whale", "end": "@same", "z": 14, "depth": 0},
      comp("Bus", 820, 990, 340, 150, {"text": ""}, start="@whale", end="@same", z=15, depth=0),
      svg(PENCIL, 780, 1030, 14, 3, start="@whale", end="@same", z=16, depth=0),
      ring(780, 1030, 44, 44, "@whale", end="@same", depth=0),
      tag("PENCIL ON A BUS", 820, 1160, "@whale", size=28, start="@whale", end="@same")]
# 16 re-count; you, honest scale next to the whale (pxPerM 34 -> 1.75 m = 60 px)
L += [comp("You", 960, 700, 40, 70, {"pose": "stand", "pxPerM": 34}, start="@same", end="@lips", z=6),
      tag("YOU", 960, 630, "@you", size=28, start="@same", end="@lips"),
      comp("Options", 540, 300, 900, 300, {"title": "3 TOOLS", "items": ["SUCTION LIPS", "HOOK TEETH", "BLADE TEETH"],
                                           "at": "@same", "stagger": 0.12, "size": 38,
                                           "select": [{"index": 0, "at": "@lips"}, {"index": 1, "at": "@anchors"},
                                                      {"index": 2, "at": "@blade"}]},
           start="@same", end="@so", z=30, depth=0)]
# 17-19 macro on whale skin: lips, top teeth, bottom row (skin -> cross-section wipe)
cx, cy, ln, h = macro_parts()
L += [svg(SKIN_WALL_GREY, 540, 1340, 1200, 700, start="@lips", end="@so", z=2),
      svg(CC_SIDE, cx, cy, ln, h, rotate=90, start="@lips", end="@so", z=5),
      glow_on(CC_LIPS, cx, cy, ln, h, "@lips", rotate=90, end="@so"),
      flash(SUCTION_CUP, 540, 1040, 180, 135, "@suction", 0.8),
      glow_on(CC_TOP_TEETH, cx, cy, ln, h, "@top", rotate=90, end="@so"),
      flash(ANCHOR, 680, 1020, 110, 128, "@anchors", 0.6),
      svg(XSEC_WHALE, 540, 1440, 1200, 900, start="@and", end="@so", z=3, enter={"type": "wipeDown", "duration": 0.5}),
      glow_on(CC_LOW_TEETH, cx, cy, ln, h, "@bottom", rotate=90, end="@so")]
# 20-21 the twist: top-down, body turns ~300 deg about the mouth (anchor at the mouth), ring closes
L += [svg(SKIN_WALL_GREY, 540, 960, 1300, 2100, start="@so", end="@hole", z=2),
      svg(CC_SIDE, 600, 720, 560, 154, anchorX=0.98, anchorY=0.53, start="@so", end="@hole", z=5,
          keyframes=[{"t": "@twists", "rotate": 0}, {"t": "@hole", "rotate": 300, "ease": "inOut"}]),
      ring(600, 720, 260, 260, "@twists", end="@hole"),
      svg(HOLE_SAW, 540, 720, 380, 380, start="@hole", end="@and#2", z=8, idle=[{"type": "spin", "speed": 1.2}],
          enter={"type": "pop", "duration": 0.2}),
      tag("HOLE SAW", 540, 990, "@hole", start="@hole", end="@and#2")]
# 22 the plug (L1 closes): 5 cm = 140 px, golf ball 4.27 cm = 120 px
L += [svg(XSEC_WHALE, 540, 1000, 1200, 900, start="@and#2", z=2),
      {"type": "rect", "x": 460, "y": 660, "width": 140, "height": 200, "fill": "#140707", "start": "@and#2", "z": 3},
      svg(PLUG, 460, 660, 140, 200, start="@and#2", z=5,
          keyframes=[{"t": "@lifts", "y": 660}, {"t": "@plug.end", "y": 540, "ease": "out"}]),
      svg(GOLF_BALL, 700, 480, 120, 120, start="@golf", z=5, enter={"type": "pop", "duration": 0.25}),
      comp("Stat", 540, 280, 600, 220, {"value": 5, "suffix": " CM", "at": "@plug", "duration": 0.6, "size": 110},
           start="@and#2", z=20, depth=0),
      tag("2 IN", 700, 600, "@golf", size=34, start="@golf")]
s["camera"] = {"preset": "pushIn", "amount": 0.3,
               "shake": [{"at": "@twists", "duration": 0.5, "amplitude": 10}]}
scenes.append(s)

# ---------------------------------------------------------------- p06 TURNSTILE (shots 23-24)
s = {"p": 6, "beat": "turnstile", "background": ocean(40), "transitionIn": {"type": "fade", "duration": 0.3},
     "camera": {"preset": "drift", "amount": 0.6}, "layers": []}
L = s["layers"]
L += [comp("BlueWhale", 540, 700, 1000, 320, {"pxPerM": 34, "idle": False}, end="@you", z=3)]
L += [svg(SCAR, x, y, 26, 26, end="@you", z=4) for x, y in ((700, 690), (742, 712), (790, 694), (660, 716))]
L += [svg(CC_SIDE, 830, 730, 40, 11, end="@you", z=5, keyframes=[{"t": 0, "x": 830}, {"t": "@spare", "x": 1040}]),
      tag("TONS TO SPARE", 540, 960, "@tons", end="@you"),
      {"type": "rect", "x": 540, "y": 960, "width": 1300, "height": 2300, "fill": "#03060a", "start": "@you", "z": 20},
      comp("You", 540, 760, 200, 360, {"pose": "stand"}, start="@you", z=22),
      head("YOU\nDON'T", "@you", red="DON'T", y=320)]
scenes.append(s)

# ---------------------------------------------------------------- p07 RE-IMMERSION ON YOU (shots 25-26)
s = {"p": 7, "beat": "re-immersion", "background": ocean(5, **NIGHT), "transitionIn": {"type": "whip", "duration": 0.3},
     "camera": {"preset": "panLeft", "amount": 0.4}, "layers": []}
L = s["layers"]
L += [{"type": "circle", "x": 840, "y": 190, "width": 110, "height": 110, "fill": "#e9eef2", "z": 2, "depth": 0.2},
      comp("You", 540, 400, 120, 220, {"pose": "run"}, rotate=-90, end="@when", z=5),
      tag("FAR FROM LAND", 540, 640, "@far", end="@when"),
      comp("You", 540, 430, 120, 220, {"pose": "run", "color": "#14242e"}, rotate=-90, start="@when", z=5),
      svg(GREEN_GLOW, 540, 1500, 360, 360, start="@when", z=4,
          keyframes=[{"t": "@when", "y": 1500, "opacity": 0.3}, {"t": "@leg", "y": 560, "opacity": 1, "ease": "inOut"}]),
      svg(CC_SIDE, 540, 1500, 220, 60, rotate=-80, start="@when", z=5,
          keyframes=[{"t": "@when", "y": 1500}, {"t": "@leg", "y": 590, "ease": "inOut"}])]
scenes.append(s)

# ---------------------------------------------------------------- p08 PEAK ON YOU (shots 27-29)
s = {"p": 8, "beat": "peak", "background": ocean(30), "transitionIn": {"type": "cut", "duration": 0},
     "camera": {"preset": "pushIn", "amount": 0.5,
                "shake": [{"at": "@twist", "duration": 0.4, "amplitude": 14}, {"at": "@swallow", "duration": 0.5, "amplitude": 18}]},
     "layers": []}
L = s["layers"]
cx, cy, ln, h = macro_parts()
L += [svg(SKIN_WALL_HUMAN, 540, 1340, 1200, 700, end="@it", z=2),
      svg(CC_SIDE, cx, cy, ln, h, rotate=90, end="@it", z=5),
      glow_on(CC_LIPS, cx, cy, ln, h, "@seal", rotate=90, end="@it"),
      glow_on(CC_TOP_TEETH, cx, cy, ln, h, "@hook", rotate=90, end="@it"),
      ring(540, 1000, 220, 90, "@twist", end="@it")]
# 28 new fact: 7 cm deep (52 px/cm: hole 5 cm = 260 px wide, 7 cm = 364 px deep, thumb 6.5 cm = 338 px)
L += [svg(XSEC_HUMAN, 540, 1000, 1200, 900, start="@it", end="@then", z=2),
      {"type": "rect", "x": 420, "y": 550, "width": 260, "height": 364, "anchorY": 0, "fill": "#140707", "start": "@it",
       "end": "@then", "z": 3, "keyframes": [{"t": "@cut", "scaleY": 0.2}, {"t": "@deep.end", "scaleY": 1, "ease": "out"}]},
      {"type": "rect", "x": 600, "y": 550, "width": 12, "height": 364, "anchorY": 0, "fill": Y, "start": "@deep", "end": "@then",
       "z": 6, "keyframes": [{"t": "@deep", "scaleY": 0}, {"t": "@deep+0.4", "scaleY": 1, "ease": "out"}]},
      svg(THUMB_SIL, 760, 719, 140, 338, start="@thumb", end="@then", z=6, enter={"type": "slideDown", "duration": 0.3}),
      tag("UP TO 7 CM / 2.75 IN", 540, 330, "@deep", size=40, start="@deep", end="@then")]
# 29 purpose reveal: the skin plug shrinks into the mouth; a clean dark disc remains (no gore)
L += [svg(SKIN_WALL_HUMAN, 540, 960, 1300, 2100, start="@then", z=2),
      svg(HOLE, 540, 760, 300, 300, start="@then", z=3),
      svg(PLUG_HUMAN.replace('viewBox="0 0 140 200"', 'viewBox="0 0 140 140"'), 540, 760, 260, 260, start="@then", z=4,
          keyframes=[{"t": "@swallow", "x": 540, "y": 760, "scale": 1}, {"t": "@circle", "x": 760, "y": 520, "scale": 0.05,
                                                                          "ease": "in"}]),
      svg(CC_SIDE, 900, 470, 480, 132, rotate=-35, anchorX=0.98, anchorY=0.53, start="@then", z=5),
      ring(540, 760, 340, 340, "@circle")]
scenes.append(s)

# ---------------------------------------------------------------- p09 REALITY FLIP (shots 30-32)
s = {"p": 9, "beat": "reality-flip", "background": {"type": "color", "color": "#05080c"},
     "transitionIn": {"type": "dipBlack", "duration": 0.4}, "camera": {"preset": "pushIn", "amount": 0.4}, "layers": []}
L = s["layers"]
L += [head("NOT A\nWHAT-IF", "@not", red="WHAT-IF", y=640, size=140, out="@in")]
L += [comp("Map", 540, 720, 1000, 900, {"views": [{"t": 0, "lon": -155, "lat": 18, "zoom": 1.6}],
                                         "pins": [{"place": "hawaii", "label": "HAWAII", "at": "@two"}],
                                         "rings": [{"place": "hawaii", "r": 5, "at": "@nine"}]},
           start="@in", end="@became", z=3, depth=0),
      tag("2009", 540, 300, "@nine", size=64, start="@in", end="@became")]
L += [svg(NIGHT_SEA, 540, 960, 1080, 1920, start="@became", z=2, depth=0),
      comp("You", 470, 790, 120, 220, {"pose": "run"}, rotate=-90, start="@became", z=5),
      svg(GLOW, 820, 740, 280, 280, start="@became", z=4, idle=[{"type": "pulse", "amount": 0.15, "speed": 0.7}]),
      {"type": "rect", "x": 820, "y": 790, "width": 200, "height": 46, "fill": "#1b2630", "radius": 10, "start": "@became", "z": 5},
      tag("FIRST KNOWN SURVIVOR", 540, 330, "@first", size=40, start="@first")]
scenes.append(s)

# ---------------------------------------------------------------- p10 RELIEF WITH A STING (shot 33)
s = {"p": 10, "beat": "relief-sting", "background": ocean(30), "transitionIn": {"type": "fade", "duration": 0.3},
     "camera": {"preset": "pushIn", "amount": 0.5}, "layers": []}
s["layers"] = [comp("You", 520, 780, 220, 400, {"pose": "stand"}, z=5),
               ring(780, 680, 170, 170, "@lived"),
               tag("SURVIVED", 540, 330, "@lived"),
               tag("NEVER GROWS BACK", 540, 460, "@grow", accent="red", start="@grow")]
scenes.append(s)

# ---------------------------------------------------------------- p11 SECOND AXIS: DISGUST (shot 34)
s = {"p": 11, "beat": "disgust", "background": {"type": "color", "color": "#120a08"},
     "transitionIn": {"type": "whip", "duration": 0.3}, "camera": {"preset": "drift", "amount": 0.5}, "layers": []}
HX, HY, HW, HH = 460, 700, 1000, 275
s["layers"] = [svg(CC_SIDE, HX, HY, HW, HH, z=5),
               svg(CC_LOW_TEETH, HX, HY, HW, HH, z=7, keyframes=[
                   {"t": "@swallows", "x": HX, "y": HY, "opacity": 1, "rotate": 0},
                   {"t": "@row.end", "x": HX - 260, "y": HY + 20, "opacity": 0, "rotate": -8, "ease": "in"}]),
               svg(CC_LOW_TEETH, HX, HY, HW, HH, start="@grows", z=7, enter={"type": "fade", "duration": 0.5}),
               tag("SWALLOWS ITS OLD TEETH", 540, 380, "@swallows", size=40)]
scenes.append(s)

# ---------------------------------------------------------------- p12 "CAN EVEN" LIST + CALLBACK (shots 35-38)
s = {"p": 12, "beat": "can-even-list", "background": ocean(120), "transitionIn": {"type": "cut", "duration": 0},
     "camera": {"preset": "pullOut", "amount": 0.4}, "layers": []}
L = s["layers"]
L += [svg(DOLPHIN, 540, 700, 700, 280, end="@tuna", z=3), svg(SCAR, 640, 680, 34, 34, end="@tuna", z=4),
      svg(SCAR, 700, 712, 30, 30, end="@tuna", z=4), tag("DOLPHINS", 540, 960, "@dolphins", end="@tuna")]
L += [svg(TUNA, 540, 700, 600, 245, start="@tuna", end="@the", z=3), svg(SCAR, 620, 700, 34, 34, start="@tuna", end="@the", z=4),
      tag("TUNA", 540, 960, "@tuna", start="@tuna", end="@the")]
L += [comp("GreatWhite", 540, 700, 760, 300, {"pxPerM": 120, "idle": False}, start="@the", end="@even", z=3),
      svg(SCAR, 700, 700, 34, 34, start="@the", end="@even", z=4),
      tag("GREAT WHITES", 540, 960, "@the", start="@the", end="@even"),
      {"type": "rect", "x": 540, "y": 960, "width": 540, "height": 16, "fill": RED, "radius": 8, "z": 35, "depth": 0,
       "start": "@the", "end": "@even", "keyframes": [{"t": "@just", "scaleX": 1}, {"t": "@forgot.end", "scaleX": 0, "ease": "in"}]}]
L += [svg(SUB, 540, 700, 900, 300, start="@even", z=3)]
L += [svg(SCAR, x, y, 28, 28, start=f"@domes+{d}", z=4, enter={"type": "pop", "duration": 0.15})
      for (x, y), d in zip(((905, 660), (930, 700), (950, 735), (915, 745), (945, 675)), (0, 0.12, 0.24, 0.36, 0.48))]
L += [tag("EVEN SUBMARINES", 540, 380, "@even", start="@even")]
scenes.append(s)

# ---------------------------------------------------------------- p13 RECURRENCE STINGER + LOOP (shots 39-40)
s = {"p": 13, "beat": "stinger-loop", "background": ocean(10, **NIGHT), "transitionIn": {"type": "fade", "duration": 0.3},
     "camera": {"preset": "pushIn", "amount": 0.4}, "layers": []}
L = s["layers"]
L += [{"type": "circle", "x": 840, "y": 190, "width": 110, "height": 110, "fill": "#e9eef2", "z": 2, "end": "@to"},
      comp("You", 540, 400, 120, 220, {"pose": "run", "color": "#14242e"}, rotate=-90, end="@to", z=5,
           idle=[{"type": "bob", "amount": 5, "speed": 0.5}]),
      svg(GREEN_GLOW, 540, 1600, 320, 320, end="@to", z=4,
          keyframes=[{"t": "@dark", "y": 1600, "opacity": 0.2}, {"t": "@rising", "y": 1200, "opacity": 0.7},
                     {"t": "@to", "y": 760, "opacity": 1, "ease": "inOut"}])]
# 40 loop frame = frame-1 composition (P01 ocean drawn as a layer so it matches frame 0)
L += [comp("Ocean", 540, 960, 1300, 2300, P01_BG, start="@to", z=1, depth=0)]
L += hero_latched(start="@to", **F1)
L += [svg(HOLE, *HOLE1, 230, 92, z=3, start="@to"), svg(RING, *HOLE1, 270, 112, z=6, start="@to"),
      ring(*MOUTH1, 200, 80, "@circle"),
      head("PERFECT\nCIRCLES", "@circle", red="CIRCLES", y=290, size=120)]
scenes.append(s)

shots = {
    "niche": "explainer",
    "emphasis": ["circles", "cookiecutter:", "bait.", "golf", "thumb", "what-if.", "submarines.", ["circle.", 3]],
    "glue": ["great whites", "tiger sharks", "pool float", "suction cup", "hole saw", "golf ball", "sonar domes",
             "navy submarines", "one more circle"],
    "scenes": scenes,
}
with open(OUT, "w") as f:
    json.dump(shots, f, indent=1, ensure_ascii=False)
print(f"{OUT}: {len(scenes)} scenes, {sum(len(x['layers']) for x in scenes)} layers")
