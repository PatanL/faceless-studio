#!/usr/bin/env python3
"""storyboard.json (16:9, 30 fps) for explainer-shoulder-test, from vo_lines.json + timeline.json.

Every shot starts on a VO line id and every in-shot beat is anchored to a spoken word (w("B9", "win")), so a new
TTS pass only needs: measure_tts.py (Spark) -> timing.py -> this script. Nothing here is hand-timed in seconds
except holds and animation lengths.

The board, the shoulder gauge (red ring + throat ring), the front-view YOU and every small prop are core layers
(rect / circle / text / inline svg), so they need no kit work. New kit figures are listed in KIT_GAPS.

usage: python3 gen_storyboard.py [out.json] [--md]      (--md prints the shot table for script.md)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TL = json.load(open(os.path.join(HERE, "timeline.json")))
LINES = {l["id"]: l for l in TL["lines"]}
ORDER = [l["id"] for l in TL["lines"]]
TOTAL = TL["total"]
SLUG = "explainer-shoulder-test"
W, H = 1920, 1080
WHITE, RED, YEL, GREEN, GREY = "#e8f1f4", "#ff5a4a", "#ffd23f", "#7ee0a1", "#8aa3ab"
SIL = "#0b2530"
CYAN = "#46d1ff"  # the throat ring (reads on the white front-view YOU)
CUT_LEAD = 0.15

KIT_GAPS = {
    "explainer/WhaleShark": "NEW figure (18 m, spotted, `jaw` 0..1, faces right; side view only, head-on shots use the open jaw + a vertical ScaleBar)",
    "explainer/BaskingShark": "NEW figure (10 m, `jaw` 0..1 with gill arches + raker comb visible, `rot` 0..1 fades the lower jaw, gill area and fins for the Zuiyo-maru diagram)",
    "explainer/Humpback": "NEW figure (15 m, long pectorals, `pleats` 0..1 throat inflation, `pose: \"lunge\"` vertical)",
    "explainer/GoliathGrouper": "NEW figure (2.5 m, `flare` 0..1 suction gape)",
}


# ------------------------------------------------------------------ timing helpers

def L(i):
    return LINES[i]


def word_t(line, word, nth=1, end=False):
    """absolute time of the nth word in a line that starts with `word` (case/punct-insensitive)."""
    key = word.lower().strip(".,:;?!'\"")
    hits = [w for w in L(line)["words"] if w[0].lower().strip(".,:;?!'\"’").startswith(key)]
    if len(hits) < nth:
        raise KeyError(f"{line}: no word {word!r} #{nth} in {L(line)['text']}")
    w = hits[nth - 1]
    return w[2] if end else w[1]


class Ctx:
    def __init__(self, start, dur):
        self.s, self.dur = start, dur

    def w(self, line, word, nth=1, end=False, off=0.0):
        return round(max(0.0, min(self.dur - 0.05, word_t(line, word, nth, end) - self.s + off)), 2)

    def ls(self, line, off=0.0):
        return round(max(0.0, L(line)["start"] - self.s + off), 2)

    def le(self, line, off=0.0):
        return round(max(0.0, min(self.dur, L(line)["end"] - self.s + off)), 2)


# ------------------------------------------------------------------ layer helpers

def ocean(depth=30, **p):
    if "surface" in p:
        p = {"skyTop": "#071620", "skyBottom": "#1b3b4a", **p}
    return {"type": "component", "name": "explainer/Ocean", "depth": 0.12, "overscan": 1.2, "props": {"depth": depth, "rays": 6, "snow": 60, **p}}


def comp(name, x, y, w, h, props=None, **kw):
    d = {"type": "component", "name": name, "x": x, "y": y, "width": w, "height": h, "props": props or {}}
    d.update(kw)
    return d


def fig(name, x, y, w, h, **p):
    kw = {k: p.pop(k) for k in list(p) if k in ("start", "end", "keyframes", "z", "flipX", "depth", "opacity", "idle", "enter", "exit")}
    return comp(f"explainer/{name}", x, y, w, h, p, **kw)


def head(text, at=0.0, out=None, y=120, size=64, color="white", red=None, **kw):
    p = {"text": text, "at": at, "size": size, "color": color, "underline": False}
    if out is not None:
        p["out"] = out
    if red:
        p["red"] = red
    return comp("explainer/Headline", 960, y, 1700, 170, p, z=20, depth=0, **kw)


def tag(text, at, x=960, y=830, accent="red", size=34, out=None, **kw):
    p = {"text": text, "at": at, "accent": accent, "size": size, "align": "center"}
    if out is not None:
        p["out"] = out
    return comp("explainer/Tag", x, y, 1400, 90, p, z=21, depth=0, **kw)


def txt(t, x, y, size=44, color=WHITE, **kw):
    d = {"type": "text", "text": t, "x": x, "y": y, "fontSize": size, "color": color, "font": "display", "weight": 900,
         "uppercase": True, "strokeColor": "#04141a", "strokeWidth": 6}
    d.update(kw)
    return d


def rect(x, y, w, h, fill, **kw):
    d = {"type": "rect", "x": x, "y": y, "width": w, "height": h, "fill": fill}
    d.update(kw)
    return d


def circ(x, y, d, stroke, sw=8, fill="rgba(0,0,0,0)", **kw):
    c = {"type": "circle", "x": x, "y": y, "width": d, "height": d, "fill": fill, "stroke": stroke, "strokeWidth": sw}
    c.update(kw)
    return c


def svg(markup, x, y, w, h, **kw):
    d = {"type": "svg", "markup": markup, "x": x, "y": y, "width": w, "height": h}
    d.update(kw)
    return d


def appear(at, d=0.35, kind="pop"):
    return {"type": kind, "at": at, "duration": d}


def kf_in(at, d=0.4, frm=0.0):
    return [{"t": max(0.0, at - 0.01), "opacity": frm, "scale": 0.85}, {"t": at + d, "opacity": 1, "scale": 1, "ease": "backOut"}]


# ------------------------------------------------------------------ props (inline SVG, flat, kit palette)

def S(vb, body):
    return f'<svg viewBox="{vb}" xmlns="http://www.w3.org/2000/svg">{body}</svg>'


# front-view YOU for every gauge beat, true scale in cm: head 16, shoulders 45 (bideltoid), hips 36, 175 tall
def you_front(shoulders=45, color=WHITE, dashed=False):
    sh = shoulders / 2
    hip = 18 * shoulders / 45
    stroke = f'stroke="{color}" stroke-width="0.8" stroke-dasharray="2 1.5" fill="none"' if dashed else f'fill="{color}"'
    return S("-30 0 60 180",
             f'<circle cx="0" cy="11" r="8" {stroke}/>'
             f'<path d="M-3 18 L3 18 L3 23 L{sh - 3} 26 Q{sh} 27 {sh} 31 L{sh} 92 L{sh - 4.5} 92 L{sh - 5} 40 '
             f'L{hip} 64 L{hip} 96 L4 175 L1 175 L0 102 L-1 175 L-4 175 L-{hip} 96 L-{hip} 64 L-{sh - 5} 40 '
             f'L-{sh - 4.5} 92 L-{sh} 92 L-{sh} 31 Q-{sh} 27 -{sh - 3} 26 L-3 23 Z" {stroke}/>')


PIZZA = S("0 0 46 8", '<rect x="0" y="1" width="46" height="7" rx="0.6" fill="#c9a26b"/><rect x="0" y="0" width="46" height="2" rx="0.6" fill="#e0bd85"/>'
          '<text x="23" y="6.6" font-size="3.4" text-anchor="middle" font-family="Montserrat" font-weight="900" fill="#7a4e22">PIZZA</text>')
BOWL = S("0 0 16 8", '<path d="M0 1 h16 q-1 7 -8 7 q-7 0 -8 -7Z" fill="#f2f2f2"/><rect x="0" y="0" width="16" height="1.4" rx="0.7" fill="#dfe8ea"/>')
MUG = S("0 0 12 11", '<rect x="0" y="0" width="9" height="11" rx="1.2" fill="#f2f2f2"/><path d="M9 3 h1.6 a2.2 2.2 0 0 1 0 4.4 H9" stroke="#f2f2f2" stroke-width="1.2" fill="none"/>')
GRAPEFRUIT = S("0 0 10 10", '<circle cx="5" cy="5" r="5" fill="#ff9f6b"/><circle cx="5" cy="5" r="3.6" fill="#ffb98f"/>')
PLATE = S("0 0 10 10", '<circle cx="5" cy="5" r="5" fill="#dfe8ea"/><circle cx="5" cy="5" r="3.4" fill="#f4f8f9"/>')
BEACHBALL = S("0 0 10 10", '<circle cx="5" cy="5" r="5" fill="#ffffff"/><path d="M5 0 A5 5 0 0 1 10 5 L5 5Z" fill="#ff5a4a"/>'
              '<path d="M5 10 A5 5 0 0 1 0 5 L5 5Z" fill="#3fa9f5"/><path d="M0 5 A5 5 0 0 1 5 0 L5 5Z" fill="#ffd23f"/>')
FIST = S("0 0 10 9", '<rect x="0" y="1" width="10" height="8" rx="3" fill="#e9c2a6"/><path d="M2.5 1 v4 M5 1 v4 M7.5 1 v4" stroke="#c99c80" stroke-width="0.6"/>')
VERTEBRA = S("0 0 100 100", ''.join(f'<circle cx="50" cy="50" r="{48 - i * 4.4}" fill="none" stroke="{"#ff5a4a" if i == 4 else "#cfd9dc"}" stroke-width="{2.6 if i == 4 else 1.4}"/>' for i in range(10))
             + '<circle cx="50" cy="50" r="5" fill="#cfd9dc"/>')
MUSHROOM = S("0 0 20 24", '<ellipse cx="10" cy="6" rx="9" ry="5.5" fill="#cfd9dc"/><rect x="7.5" y="9" width="5" height="12" fill="#cfd9dc"/><rect x="2" y="21" width="16" height="3" rx="1.5" fill="#cfd9dc"/>')
BOAT_LIGHTS = S("0 0 400 260", '<path d="M20 20 L380 20 L340 70 L60 70 Z" fill="#0a1a20"/><circle cx="200" cy="72" r="6" fill="#fff6c8"/>'
                '<path d="M200 72 L60 260 L340 260 Z" fill="#fff6c8" opacity="0.18"/>')
SIEVE = S("0 0 1920 1080", '<rect width="1920" height="1080" fill="#3a1f26"/>' + ''.join(
    f'<rect x="{180 + i * 130}" y="120" width="70" height="840" rx="30" fill="#6b3a44"/><rect x="{196 + i * 130}" y="140" width="38" height="800" rx="18" fill="#82505a" opacity="0.6"/>'
    for i in range(12)) + '<ellipse cx="960" cy="560" rx="26" ry="20" fill="#120609"/>')
POOL = S("0 0 50 25", '<rect x="1" y="1" width="48" height="23" fill="none" stroke="#cfd9dc" stroke-width="1"/>' + ''.join(f'<line x1="1" y1="{1 + i * 2.875}" x2="49" y2="{1 + i * 2.875}" stroke="#cfd9dc" stroke-width="0.3"/>' for i in range(1, 8)))
POOL_FILL = S("0 0 50 25", '<rect x="1" y="1" width="48" height="23" fill="#3fa9f5" opacity="0.55"/>')
RAKERS = S("0 0 200 120", ''.join(f'<line x1="{8 + i * 9}" y1="10" x2="{8 + i * 9}" y2="110" stroke="#d8c6b8" stroke-width="3" stroke-linecap="round"/>' for i in range(21)))
CARCASS = S("0 0 300 160", '<path d="M10 120 Q40 40 90 60 Q120 70 140 95 Q200 80 250 100 Q290 115 292 135 Q250 150 180 145 Q120 150 80 140 Q50 132 30 128 Z" fill="#b8a99a"/>'
            '<path d="M120 140 l-20 18 M160 145 l10 15 M210 143 l-8 16 M250 138 l12 14" stroke="#b8a99a" stroke-width="7" stroke-linecap="round"/>')
NEWSPAPER = S("0 0 160 110", '<rect width="160" height="110" fill="#efe9dc"/><rect x="8" y="8" width="144" height="16" fill="#2b2b2b"/>'
              + ''.join(f'<rect x="8" y="{34 + i * 9}" width="{70 if i % 2 else 64}" height="4" fill="#9a958b"/>' for i in range(8))
              + '<rect x="84" y="34" width="68" height="66" fill="#b8a99a"/>')
SANDWICH = S("0 0 60 34", '<path d="M2 16 Q30 2 58 16 Z" fill="#e3b46b"/><rect x="2" y="16" width="56" height="5" fill="#7cc576"/><rect x="2" y="21" width="56" height="4" fill="#e85d4a"/>'
             '<path d="M2 25 h56 q-28 10 -56 0Z" fill="#e3b46b"/><path d="M40 18 q14 -14 18 -4 l-4 6Z" fill="#c9c3f2"/>')
PIANO = S("0 0 60 40", '<path d="M2 14 L30 14 Q40 4 58 8 L58 30 L2 30 Z" fill="#101418"/><rect x="2" y="24" width="28" height="4" fill="#f2f2f2"/>'
          '<rect x="6" y="30" width="3" height="10" fill="#101418"/><rect x="52" y="30" width="3" height="10" fill="#101418"/>')
WRECK = S("0 0 900 300", '<path d="M0 300 L60 120 L700 90 L860 160 L900 300 Z" fill="#0d262c"/><rect x="200" y="40" width="80" height="70" fill="#0d262c"/>'
          + ''.join(f'<circle cx="{120 + i * 90}" cy="190" r="12" fill="#06161a"/>' for i in range(7)))
BUBBLE = lambda t: S("0 0 220 90", f'<rect x="2" y="2" width="216" height="64" rx="20" fill="#f4f8f9"/><path d="M40 66 l-10 22 l30 -22Z" fill="#f4f8f9"/>'
                     f'<text x="110" y="44" font-size="22" text-anchor="middle" font-family="Montserrat" font-weight="900" fill="#14262c">{t}</text>')
HOOK_X = S("0 0 60 60", '<path d="M30 4 v30 a10 10 0 1 1 -14 -8" stroke="#cfd9dc" stroke-width="4" fill="none"/><path d="M6 6 L54 54 M54 6 L6 54" stroke="#ff5a4a" stroke-width="7"/>')
CROSS = S("0 0 60 60", '<path d="M6 6 L54 54 M54 6 L6 54" stroke="#ff5a4a" stroke-width="9" stroke-linecap="round"/>')
STOMACH = S("0 0 400 260", '<ellipse cx="200" cy="130" rx="190" ry="120" fill="#2a1a20" stroke="#6b3a44" stroke-width="6"/>')
NET = S("0 0 300 180", '<ellipse cx="150" cy="90" rx="140" ry="82" fill="#5b6b5a"/>' + ''.join(
    f'<path d="M{20 + i * 26} 20 L{40 + i * 22} 170" stroke="#9fb08f" stroke-width="3"/>' for i in range(10))
    + ''.join(f'<path d="M15 {30 + i * 18} L285 {40 + i * 15}" stroke="#c7a76b" stroke-width="4"/>' for i in range(8)))


def debris(kind):
    return {
        "cup": S("0 0 10 12", '<path d="M0 0 h10 l-1.6 12 h-6.8Z" fill="#f2f2f2"/><rect x="0" y="0" width="10" height="1.4" fill="#ff5a4a"/>'),
        "bag": S("0 0 12 14", '<path d="M1 4 h10 l1 10 h-12Z" fill="#dfe8ea" opacity="0.9"/><path d="M3 4 q1 -4 3 0 M6 4 q1 -4 3 0" stroke="#dfe8ea" fill="none"/>'),
        "flipflop": S("0 0 8 16", '<ellipse cx="4" cy="8" rx="3.8" ry="7.8" fill="#3fa9f5"/><path d="M4 3 L1 8 M4 3 L7 8" stroke="#ffd23f" stroke-width="1"/>'),
        "bowling": S("0 0 10 10", '<circle cx="5" cy="5" r="5" fill="#2a3440"/><circle cx="4" cy="3" r="0.7" fill="#000"/><circle cx="6" cy="3.2" r="0.7" fill="#000"/><circle cx="5" cy="4.8" r="0.7" fill="#000"/>'),
        "scale": S("0 0 40 14", '<rect x="0" y="6" width="40" height="8" rx="2" fill="#cfd9dc"/><rect x="14" y="0" width="12" height="6" rx="1" fill="#14262c"/>'),
    }[kind]


# ------------------------------------------------------------------ the gauge (red ring = your shoulders, white ring = the throat)

PXCM = 9.0  # px per cm in gauge shots
HOOP = {"t": 0, "scaleY": 0.32}  # rings are drawn as a hoop round the shoulders (front view, slight top-down tilt)


def gauge(ctx, cx, cy, throat=None, at=0.0, est=False, extra_cap=None, label=None, you=True, ring_at=None, ring_out=None):
    """YOU front view at true scale with the red 45 cm ring around the shoulders and a throat ring.
    throat: (from_cm, to_cm, t0, t1) grows the white ring; est=True draws it dashed (estimate only)."""
    out = []
    if you:
        out.append(svg(you_front(), cx, cy + (90 - 29) * PXCM, 60 * PXCM, 180 * PXCM, z=3, depth=0.4))
    ra = at if ring_at is None else ring_at
    ring = circ(cx, cy, 45 * PXCM, RED, 9, z=5, depth=0.4, keyframes=kf_in(ra, 0.35) + [HOOP])
    if ring_out is not None:
        ring["keyframes"] = kf_in(ra, 0.35) + [HOOP, {"t": ring_out, "opacity": 1, "y": cy}, {"t": ring_out + 1.2, "opacity": 0, "y": cy + 700, "rotate": 25, "ease": "in"}]
    out.append(ring)
    out.append(txt("YOUR SHOULDERS ~45", cx + 45 * PXCM / 2 + 24, cy, 28, RED, align="left", anchorX=0, z=6, depth=0.4, start=ra))
    if throat:
        f, t, t0, t1 = throat
        c = circ(cx, cy, t * PXCM, CYAN if not est else YEL, 7, z=6, depth=0.4,
                 keyframes=[{"t": max(0, t0 - 0.01), "scale": 0.0, "opacity": 0}, {"t": t0 + 0.2, "scale": f / t, "opacity": 1},
                            {"t": t1, "scale": 1.0, "opacity": 1, "ease": "out"}, HOOP])
        out.append(c)
        if label:
            out.append(txt(label, cx - 45 * PXCM / 2 - 24, cy, 28, CYAN if not est else YEL, align="right", anchorX=1, z=6, depth=0.4, start=t1))
    return out


# ------------------------------------------------------------------ the board (columns on a cm ruler; red line = your shoulders)

BX0, BX1, BASE, TOPV, TOPY = 330, 1700, 820, 60.0, 200
PX_PER_CM_B = (BASE - TOPY) / TOPV
ENTRIES = {
    "whaleShark": {"label": "WHALE SHARK", "solid": 2.5, "cap": 15, "val": "≤15", "color": "#9fd3e0"},
    "basking": {"label": "BASKING SHARK", "solid": 10, "cap": None, "val": "~10", "color": "#9fd3e0"},
    "blue": {"label": "BLUE WHALE", "solid": 25, "cap": 35, "val": "≤35", "color": "#9fd3e0"},
    "humpback": {"label": "HUMPBACK", "solid": 10, "cap": 38, "val": "≤38 · RECORD", "color": "#9fd3e0"},
    "grouper": {"label": "GOLIATH GROUPER", "solid": 0, "cap": 40, "val": "~40*", "color": YEL, "dashed": True},
    "sperm": {"label": "SPERM WHALE", "solid": 0, "cap": 52, "val": "?", "color": GREY, "dashed": True},
    "rubbish": {"label": "OUR RUBBISH", "solid": 58, "cap": None, "val": "~100 KG · HAS", "color": RED},
}
SORT = ["basking", "whaleShark", "blue", "humpback", "grouper", "sperm", "rubbish"]


def slot_x(i, n):
    span = BX1 - BX0
    return BX0 + span * (i + 0.5) / max(n, 1)


def board(ctx, shown, new=None, at=0.0, pulse=None, title_at=0.0, hover=None, slots=7):
    """shown: keys already on the board; new: key that joins at `at` (others slide to make room).
    pulse: [(key, t)] to pulse a column (final recap). hover: (key, cm) = new column first rises to cm then falls."""
    lay = [rect(960, 505, 1760, 790, "rgba(4,20,26,0.82)", radius=26, z=1, depth=0, keyframes=[{"t": max(0, title_at - 0.01), "opacity": 0}, {"t": title_at + 0.3, "opacity": 1}]),
           txt("THE SHOULDER GAUGE", 960, 160, 50, WHITE, z=4, depth=0, start=title_at)]
    for cm, lab, col, dash in ((45, "YOUR SHOULDERS 45", RED, False), (40, "SMALLER ADULTS 40", "#ff9a8f", True),
                               (16, "YOUR HEAD 16", GREY, True), (9, "YOUR FIST 9", GREY, True)):
        y = BASE - cm * PX_PER_CM_B
        lay.append(rect((BX0 + BX1) / 2, y, BX1 - BX0, 6 if not dash else 3, col, opacity=1 if not dash else 0.6, z=3, depth=0, start=title_at))
        lay.append(txt(lab, BX0 - 30, y, 24, col, align="right", anchorX=1, z=4, depth=0, start=title_at))
    lay.append(rect((BX0 + BX1) / 2, BASE + 2, BX1 - BX0, 4, GREY, z=3, depth=0, start=title_at))
    lay.append(txt("PASS ↑", BX1 + 10, BASE - 45 * PX_PER_CM_B - 34, 26, RED, align="left", anchorX=0, z=4, depth=0, start=title_at))
    final = [k for k in SORT if k in shown or k == new]
    before = [k for k in SORT if k in shown]
    for k in final:
        e = ENTRIES[k]
        x1 = slot_x(final.index(k), len(final) if slots is None else slots)
        x0 = slot_x(before.index(k), len(before) if slots is None else slots) if k in before else x1
        is_new = k == new
        xs = [{"t": 0, "x": x0}, {"t": max(0.01, at - 0.4), "x": x0}, {"t": at, "x": x1, "ease": "inOut"}] if (x0 != x1) else []
        top = max(e["solid"], e["cap"] or 0)
        grow_t = at + 0.1 if is_new else 0
        def col_layer(h_cm, fill, dashed=False, op=1.0):
            hpx = max(2, h_cm * PX_PER_CM_B)
            base = {"type": "rect", "x": x1, "y": BASE, "width": 120, "height": hpx, "anchorY": 1.0, "fill": fill if not dashed else "rgba(0,0,0,0)",
                    "radius": 10, "z": 5, "depth": 0, "opacity": op}
            if dashed:
                base.update({"stroke": fill, "strokeWidth": 5})
            kf = []
            if is_new:
                if hover and hover[0] == k:
                    hh = hover[1] / max(h_cm, 0.1)
                    kf = [{"t": max(0, grow_t - 0.01), "scaleY": 0.0}, {"t": grow_t + 0.5, "scaleY": hh, "ease": "out"},
                          {"t": grow_t + 1.3, "scaleY": hh}, {"t": grow_t + 1.7, "scaleY": 1.0, "ease": "bounce"}]
                else:
                    kf = [{"t": max(0, grow_t - 0.01), "scaleY": 0.0}, {"t": grow_t + 0.6, "scaleY": 1.0, "ease": "backOut"}]
            elif xs:
                kf = [dict(x) for x in xs]
            if xs and is_new is False:
                pass
            if pulse:
                for pk, pt in pulse:
                    if pk == k:
                        kf += [{"t": pt, "scale": 1.0}, {"t": pt + 0.2, "scale": 1.08}, {"t": pt + 0.5, "scale": 1.0}]
            base["keyframes"] = sorted(kf, key=lambda q: q["t"])
            return base
        if e["cap"]:
            lay.append(col_layer(e["cap"], e["color"], dashed=True, op=0.85))
        if e["solid"]:
            lay.append(col_layer(e["solid"], e["color"]))
        lab_kf = [dict(x) for x in xs] if xs else []
        st = (at + 0.5) if is_new else None
        lay.append(txt(e["label"], x1, BASE + 36, 19, WHITE, maxWidth=180, z=6, depth=0, keyframes=lab_kf, **({"start": st} if st else {})))
        lay.append(txt(e["val"], x1, BASE - top * PX_PER_CM_B - 30, 30 if e["val"] != "?" else 64, e["color"] if k != "rubbish" else RED,
                       z=6, depth=0, keyframes=lab_kf, **({"start": at + (1.9 if hover and hover[0] == k else 0.8)} if is_new else {})))
    return lay


# ------------------------------------------------------------------ hook tableau (shot 1, re-immersion, bookend)

SIX = [("BlueWhale", 30, 0.30, 0.78, 0), ("WhaleShark", 18, 0.78, 0.70, 1.3), ("BaskingShark", 10, 0.18, 0.55, 2.1),
       ("Humpback", 15, 0.82, 0.40, 0.7), ("GoliathGrouper", 2.5, 0.62, 0.88, 1.7), ("SpermWhale", 16, 0.12, 0.30, 2.6)]


def tableau(ctx, greys=None, empty=False, pulse_red=None):
    lay = []
    if not empty:
        for i, (nm, m, fx, fy, ph) in enumerate(SIX):
            pxm = 26 if m > 5 else 60
            wpx = m * pxm
            g = (greys or {}).get(nm)
            kf = [{"t": 0, "x": fx * W - 120, "opacity": 1}, {"t": ctx.dur, "x": fx * W + 120}]
            if g is not None:
                kf = [{"t": 0, "x": fx * W - 120, "opacity": 1}, {"t": g, "opacity": 1}, {"t": g + 0.6, "opacity": 0.25, "x": fx * W - 40}, {"t": ctx.dur, "x": fx * W + 120, "opacity": 0.25}]
            lay.append(fig(nm, fx * W, fy * H, wpx, wpx * 0.35, pxPerM=pxm, silhouette=SIL, timeOffset=ph, speed=0.6, z=1 + i % 3,
                           depth=0.5 + 0.2 * (i % 3), keyframes=kf, flipX=bool(i % 2)))
            if g is not None:
                lay.append(svg(CROSS, fx * W + 40, fy * H, 70, 70, z=8, depth=0.6, start=g + 0.3, enter=appear(g + 0.3)))
            if pulse_red and nm in pulse_red:
                lay.append(fig(nm, fx * W + 40, fy * H, wpx, wpx * 0.35, pxPerM=pxm, silhouette="#7a2a26", timeOffset=ph, speed=0.6, z=4,
                               depth=0.5 + 0.2 * (i % 3), start=pulse_red[nm], keyframes=[{"t": pulse_red[nm], "opacity": 0}, {"t": pulse_red[nm] + 0.4, "opacity": 0.9}],
                               flipX=bool(i % 2)))
    lay.append(fig("You", 960, 330, 90, 180, pose="stand", z=6, depth=1.0, idle=[{"type": "float", "amount": 8, "speed": 0.3}]))
    return lay


# ------------------------------------------------------------------ shot list

SHOTS = []


def shot(line, kind, desc, cam="", sfx="", bg=None, transition=None, grade=None, music=None, offset=0.0):
    def deco(fn):
        SHOTS.append({"line": line, "kind": kind, "desc": desc, "cam": cam, "sfx": sfx, "bg": bg, "build": fn,
                      "transition": transition, "grade": grade, "offset": offset})
        return fn
    return deco


DROP = {"saturate": 0.4, "vignette": 0.5, "contrast": 1.05, "tint": "#2b4650", "tintOpacity": 0.2}


@shot("H1", "Hook wide", "`explainer/Ocean` surface 0.12; `You` floats under the surface; six silhouettes (BlueWhale, WhaleShark*, BaskingShark*, Humpback*, GoliathGrouper*, SpermWhale) circle on 3 parallax depths; red 45 cm ring snaps round YOU's shoulders on \"giants\"; kicker", "slow push-in 1.0→1.08", "underwater_rumble bed; click on ring snap", bg=ocean(8, surface=0.12, rays=7))
def _(c):
    lay = tableau(c)
    lay.append(circ(960, 292, 100, RED, 7, z=7, depth=1.0, keyframes=kf_in(c.w("H1", "giants"), 0.25) + [HOOP]))
    lay += [head(L("H1")["screen"], c.w("H1", "fed"), out=c.ls("H2"), red=["ONE"]),
            head(L("H2")["screen"], c.ls("H2"), red=["FIT?"])]
    return lay, {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": c.dur, "zoom": 1.08}]}, [("click", c.w("H1", "giants"))]


@shot("T1", "Teaser contract", "4 cards, one per clause, each a 1.05 push: vertebra rings + mushroom icon (BOMB-DATED) · humpback mouth + tiny YOU (PEOPLE IN ITS MOUTH) · grouper flare + shark silhouette (INHALES SHARKS) · sperm whale head with a `?` throat ring (NEVER MEASURED)", "cut per clause", "whoosh per card; stinger on \"measured\"", bg=ocean(40))
def _(c):
    t1, t2, t3, t4 = c.w("T1", "fish"), c.w("T1", "whale"), c.w("T1", "fish", 2), c.w("T1", "throat")
    end = c.dur
    lay = [svg(VERTEBRA, 760, 520, 420, 420, start=t1, end=t2, z=3), svg(MUSHROOM, 1180, 380, 110, 132, start=t1, end=t2, z=3),
           head("BOMB-DATED", t1, out=t2 - 0.1, y=830, size=58, red=["BOMB-DATED"]),
           fig("Humpback", 900, 520, 1100, 380, pxPerM=70, pleats=1, start=t2, end=t3, z=3), fig("You", 1250, 560, 40, 80, pose="panic", start=t2, end=t3, z=4),
           head("PEOPLE IN ITS MOUTH", t2, out=t3 - 0.1, y=830, size=58, red=["MOUTH"]),
           fig("GoliathGrouper", 760, 540, 700, 330, pxPerM=280, flare=[{"t": t3 + 0.4, "v": 0}, {"t": t3 + 0.7, "v": 1}], start=t3, end=t4, z=3),
           fig("GreatWhite", 1380, 540, 300, 110, pxPerM=60, silhouette="#c9d6da", start=t3, end=t4, z=3,
               keyframes=[{"t": t3, "x": 1380}, {"t": t3 + 0.5, "x": 1380}, {"t": t3 + 0.9, "x": 900, "scale": 0.3, "opacity": 0}]),
           head("INHALES SHARKS", t3, out=t4 - 0.1, y=830, size=58, red=["SHARKS"]),
           fig("SpermWhale", 760, 540, 1400, 420, pxPerM=85, start=t4, z=3), circ(1320, 610, 120, YEL, 6, start=t4 + 0.4, z=5),
           txt("?", 1320, 610, 90, YEL, start=t4 + 0.4, z=6), head("NEVER MEASURED", t4, y=830, size=58, red=["NEVER"])]
    cam = {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": t2 - 0.01, "zoom": 1.05}, {"t": t2, "zoom": 1.0}, {"t": t3 - 0.01, "zoom": 1.05},
                         {"t": t3, "zoom": 1.0}, {"t": t4 - 0.01, "zoom": 1.05}, {"t": t4, "zoom": 1.0}, {"t": end, "zoom": 1.06}]}
    return lay, cam, [("whoosh", t1), ("whoosh", t2), ("whoosh", t3), ("whoosh", t4), ("stinger", c.w("T1", "measured"))]


@shot("R1", "Strike-off", "`GreatWhite` and `Orca` side by side (`pxPerM` 40); red ✕ stamps; kicker TEETH DON'T COUNT", "slight pan L→R", "impact ×2", bg=ocean(25))
def _(c):
    t = c.w("R1", "teeth")
    return [fig("GreatWhite", 620, 560, 300 * 1.6, 110 * 1.6, pxPerM=80, z=3), fig("Orca", 1300, 560, 640, 220, pxPerM=80, z=3),
            svg(CROSS, 620, 560, 200, 200, start=t + 0.2, enter=appear(t + 0.2), z=5), svg(CROSS, 1300, 560, 200, 200, start=t + 0.5, enter=appear(t + 0.5), z=5),
            head("TEETH DON'T COUNT", t, red=["DON'T"])], {"preset": "panRight", "amount": 0.4}, [("impact", t + 0.2), ("impact", t + 0.5)]


@shot("R2", "Rules card", "`Options` title RULES, items JUST YOU / NOTHING IN YOUR HANDS / NOTHING IN YOUR POCKETS / NO GEAR (itemAt on the words); `You` pose shrug right", "static", "tick per item", bg=ocean(30))
def _(c):
    its = [c.w("R2", "just"), c.w("R2", "nothing"), c.w("R2", "pockets"), c.w("R2", "gear")]
    return [comp("explainer/Options", 760, 540, 1100, 700, {"title": "THE RULES", "items": ["JUST YOU", "NOTHING IN YOUR HANDS", "NOTHING IN YOUR POCKETS", "NO GEAR"],
                                                          "itemAt": its, "size": 50}, z=4, depth=0),
            fig("You", 1520, 600, 140, 280, pose="shrug", z=4)], {"preset": "none"}, [("tick", t) for t in its]


@shot("R3", "Gauge reveal", "Front-view YOU (inline SVG at true scale: head 16, shoulders 45, hips 36 cm); `ScaleBar` ~45 CM across the shoulders; party-size pizza box slides in under it at the same width", "push-in to shoulders", "pop; ding on \"pizza\"", bg=ocean(30))
def _(c):
    k = PXCM
    t_sh, t_pz = c.w("R3", "shoulders"), c.w("R3", "pizza")
    lay = [svg(you_front(), 960, 360 + 61 * k, 60 * k, 180 * k, z=3),
           comp("explainer/ScaleBar", 960, 250, 45 * k, 120, {"label": "~45 CM", "at": t_sh, "duration": 0.6, "color": "red", "labelSize": 40}, z=5, depth=0.9),
           svg(PIZZA, 960, 900, 46 * k, 8 * k, z=6, keyframes=[{"t": max(0, t_pz - 0.3), "x": 2400}, {"t": t_pz + 0.2, "x": 960, "ease": "out"}]),
           head(L("R3")["screen"], t_pz, red=["PIZZA"])]
    return lay, {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": c.dur, "zoom": 1.12, "y": 420}]}, [("pop", t_sh), ("ding", t_pz + 0.2)]


@shot("R4", "Smaller adult", "A dashed 40 cm YOU outline slides in beside the 45 cm one; kicker SMALLER ADULTS ~40 CM; on \"hold\" a small `40` pin tag drops into the corner and stays for the rest of the setup (the plant paid at G11)", "static", "pop; click on \"hold\"", bg=ocean(30))
def _(c):
    k = PXCM
    return [svg(you_front(), 760, 360 + 61 * k, 60 * k, 180 * k, z=3),
            svg(you_front(40, "#ff9a8f", dashed=True), 1180, 360 + 61 * k, 60 * k, 180 * k, z=3, keyframes=kf_in(c.w("R4", "smaller"))),
            txt("45", 760, 230, 60, RED, z=5), txt("40", 1180, 250, 60, "#ff9a8f", z=5, start=c.w("R4", "forty")),
            head(L("R4")["screen"], c.w("R4", "smaller")), tag("HOLD ON TO 40", c.w("R4", "hold"), x=1620, y=830, accent="yellow", size=28)], {"preset": "none"}, \
        [("pop", c.w("R4", "smaller")), ("click", c.w("R4", "hold"))]


@shot("R5", "Gauge rule + empty board", "Red ring grows round the front-view YOU (\"PASS = WIDER THAN THE RING\"), then on \"estimate\" the empty board slides in over it: a cm ruler with the red 45 line, dashed 40 / head 16 / fist 9 lines, seven empty slots", "pull-out", "riser short; whoosh_long on the board", bg=ocean(35))
def _(c):
    t_b = c.w("R5", "estimate")
    lay = gauge(c, 960, 520, at=c.w("R5", "ring"))
    for l in lay:
        l["end"] = t_b + 0.3
    lay += [head("PASS = WIDER THAN THE RING", c.w("R5", "pass"), out=t_b, red=["WIDER"])]
    lay += board(c, [], title_at=t_b)
    return lay, {"keyframes": [{"t": 0, "zoom": 1.06}, {"t": t_b, "zoom": 1.0}]}, [("riser", c.w("R5", "ring")), ("whoosh_long", t_b)]


@shot("B1", "Size", "`Tag` #6 BLUE WHALE; `BlueWhale` `pxPerM` 45 crossing frame; `ScaleBar` ~30 M", "slow pan following the whale", "underwater_rumble swell", bg=ocean(30))
def _(c):
    return [fig("BlueWhale", 960, 560, 30 * 45, 300, pxPerM=45, z=3, keyframes=[{"t": 0, "x": 1200}, {"t": c.dur, "x": 760}]),
            comp("explainer/ScaleBar", 960, 760, 30 * 45, 120, {"label": "~30 M", "at": c.w("B1", "biggest"), "color": "white"}, z=4),
            tag("#6 BLUE WHALE", c.w("B1", "number"), y=150, size=44)], {"preset": "panLeft", "amount": 0.4}, [("whoosh", c.w("B1", "number"))]


@shot("B2", "Scale compare", "2.5 × `Bus` nose to tail under the whale at the same `pxPerM`; kicker ~30 M ≈ 2.5 BUSES", "static", "pop ×3 on the buses", bg=ocean(30))
def _(c):
    t = c.w("B2", "two")
    lay = [fig("BlueWhale", 960, 420, 30 * 45, 300, pxPerM=45, z=3)]
    for i in range(3):
        lay.append(fig("Bus", 960 - 30 * 45 / 2 + 12 * 45 * (i + 0.5), 760, 12 * 45, 160, pxPerM=45, z=4, start=t + i * 0.35, enter=appear(t + i * 0.35),
                       **({"opacity": 0.5} if i == 2 else {})))
    lay.append(head(L("B2")["screen"], t, red=["BUSES"]))
    return lay, {"preset": "none"}, [("pop", t + i * 0.35) for i in range(3)]


@shot("B3", "Lunge", "`BlueWhale` `gape` 0→1 (jaw drop, pleated pouch balloons); kicker 1 GULP > ITS OWN WEIGHT; a tiny YOU dot rides the inflow", "push-in on the jaw", "whoosh_long, bubbles", bg=ocean(25))
def _(c):
    t = c.w("B3", "lunge")
    return [fig("BlueWhale", 900, 540, 30 * 55, 360, pxPerM=55, gape=[{"t": t, "v": 0}, {"t": t + 1.2, "v": 1, "ease": "out"}], z=3),
            fig("You", 1700, 520, 20, 40, pose="panic", z=4, keyframes=[{"t": 0, "x": 1760}, {"t": c.dur, "x": 1560}]),
            head(L("B3")["screen"], c.w("B3", "more"), red=["WEIGHT"])], {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": c.dur, "zoom": 1.15, "x": 1150}]}, \
        [("whoosh_long", t), ("bubbles", t + 0.6)]


@shot("B4", "2P scenario", "`You` at the surface (`surface` 0.2); a BlueWhale silhouette rises from below; on \"drops\" the jaw opens (`gape`), on \"in\" YOU slides into the mouth and the frame dips to the dark mouth interior", "camera drops with YOU; shake 0.3 s on the gulp", "underwater_rumble, bubbles, whoosh", bg=ocean(6, surface=0.2))
def _(c):
    tr, td, ti = c.w("B4", "shadow"), c.w("B4", "drops"), c.w("B4", "in")
    return [fig("You", 960, 260, 80, 160, pose="stand", z=5, keyframes=[{"t": 0, "y": 260}, {"t": ti, "y": 300}, {"t": ti + 0.8, "y": 760, "scale": 0.5, "ease": "in"}]),
            fig("BlueWhale", 960, 1300, 1700, 420, pxPerM=60, rotate=-70, silhouette=SIL, gape=[{"t": td, "v": 0}, {"t": td + 0.8, "v": 1}], z=3,
                keyframes=[{"t": 0, "y": 1500, "rotate": -70}, {"t": tr + 2.0, "y": 980, "rotate": -70, "ease": "out"}]),
            rect(960, 540, W, H, "#120609", z=9, depth=0, keyframes=[{"t": max(0, ti + 0.6), "opacity": 0}, {"t": ti + 1.1, "opacity": 0.92}])], \
        {"keyframes": [{"t": 0, "y": 540}, {"t": ti + 1.0, "y": 640}], "shake": [{"at": ti + 0.3, "duration": 0.3, "amplitude": 12}]}, \
        [("underwater_rumble", tr), ("whoosh", ti), ("bubbles", ti + 0.3)]


@shot("B5", "Micro-loop", "Dark mouth interior; kicker WHAT STOPS YOU? → on \"throat\" cut to `WhaleThroat` close-up (throat ring ~0.34 m)", "slow push", "heartbeat_slow; ding on \"throat\"", bg={"type": "color", "color": "#120609"})
def _(c):
    t = c.w("B6", "throat")
    return [head("WHAT STOPS YOU?", c.ls("B5"), out=t, red=["STOPS"]), fig("WhaleThroat", 960, 560, 1100, 700, start=t, enter=appear(t, 0.3, "zoomIn"), z=3),
            head("THE THROAT", t, red=["THROAT"])], {"preset": "pushIn", "amount": 0.6}, [("heartbeat_slow", 0.2), ("ding", t)]


@shot("B7", "Gauge #6", "Front-view YOU + red 45 ring; cyan throat ring grows grapefruit → plate (solid, 10→25 cm) then a yellow dashed cap to 35 cm as a small beach ball pops in; icons grapefruit/plate/ball beside; kicker 35 vs 45", "static, slight push on \"win\"", "tick on each icon, sonar_ping on the ring, impact soft on \"win\"", bg=ocean(30))
def _(c):
    g, p, b = c.w("B7", "grapefruit"), c.w("B7", "plate"), c.w("B8", "beach")
    lay = gauge(c, 760, 520, throat=(10, 25, g, p + 0.4), at=0.1)
    lay.append(circ(760, 520, 35 * PXCM, YEL, 6, z=6, depth=0.4, keyframes=kf_in(b, 0.4) + [HOOP]))
    lay += [svg(GRAPEFRUIT, 1350, 330, 90, 90, start=g, enter=appear(g)), svg(PLATE, 1500, 330, 225, 225, start=p, enter=appear(p)),
            svg(BEACHBALL, 1450, 640, 315, 315, start=b, enter=appear(b)),
            txt("~10", 1350, 410, 30, WHITE, start=g), txt("~25", 1500, 470, 30, WHITE, start=p), txt("~35 (WIDEST CLAIM)", 1450, 830, 30, YEL, start=b),
            head(L("B7")["screen"], g, out=b), head(L("B8")["screen"], b, out=c.ls("B9"), red=["~35"]), head("35 vs 45", c.ls("B9"), red=["45"], size=80)]
    return lay, {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": c.ls("B9"), "zoom": 1.0}, {"t": c.dur, "zoom": 1.08, "x": 860}]}, \
        [("tick", g), ("tick", p), ("sonar_ping", b), ("impact", c.w("B9", "win"))]


@shot("B10", "Baleen flush", "BlueWhale close-up, `gape` 1; baleen curtain; `Krill` particles stay while the water arrows (svg) push out; YOU tumbles out the side (pose panic → shrug), drip lines; kicker BALEEN", "slight pan; shake 0.2 s at the exit", "whoosh, bubbles; pop on \"offended\"", bg=ocean(15))
def _(c):
    out_t = c.w("B11", "out")
    return [fig("BlueWhale", 700, 540, 2600, 600, pxPerM=90, gape=1, z=3),
            {"type": "particles", "preset": "dust", "count": 90, "color": "#ffb3a0", "size": [3, 7], "x": 1300, "y": 560, "width": 520, "height": 300, "z": 4},
            fig("You", 1300, 560, 90, 180, pose="panic", z=5, keyframes=[{"t": 0, "x": 1300}, {"t": out_t, "x": 1320}, {"t": out_t + 0.8, "x": 1800, "y": 420, "rotate": 200, "ease": "out"}]),
            fig("You", 1720, 400, 90, 180, pose="shrug", z=5, start=c.w("B11", "wet")),
            head("BALEEN", c.w("B10", "baleen")), head("VERY CONFUSING KRILL", c.w("B10", "confusing"), y=830, size=50, red=["CONFUSING"], out=out_t)], \
        {"preset": "panRight", "amount": 0.3, "shake": [{"at": out_t + 0.2, "duration": 0.2, "amplitude": 10}]}, \
        [("whoosh", out_t), ("bubbles", out_t + 0.2), ("pop", c.w("B11", "offended"))]


@shot("B12", "Appetite", "`Stat` 16 suffix \" TONNES / DAY\" count-up; a row of 10 `Car`s; tiny YOU at the end labelled ROUNDING ERROR", "push-in on the tiny YOU", "ding", bg=ocean(30))
def _(c):
    t = c.w("B12", "sixteen")
    lay = [comp("explainer/Stat", 960, 330, 900, 300, {"value": 16, "suffix": " TONNES / DAY", "at": t, "duration": 1.0, "size": 110}, z=4, depth=0)]
    for i in range(10):
        lay.append(fig("Car", 300 + i * 125, 760, 120, 60, pxPerM=26, z=3, start=c.w("B12", "ten") + i * 0.08))
    lay.append(fig("You", 1620, 780, 18, 36, pose="wave", z=4))
    return lay, {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": c.dur, "zoom": 1.1, "x": 1100}]}, [("ding", c.w("B12", "ten"))]


@shot("B13", "Verdict #6", "Board: BlueWhale column grows (solid to 25 = most estimates, dashed cap to 35 = widest claim) and stops under the red 45 line; stamp BLUE WHALE · ~35 CM AT MOST", "static", "impact low; stinger tail", bg=ocean(40))
def _(c):
    t = c.w("B13", "tops")
    return board(c, [], new="blue", at=t) + [tag(L("B13")["screen"], c.w("B13", "size"), y=245, accent="red")], {"preset": "none"}, [("impact", t + 0.6)]


@shot("W1", "Withheld noun + bomb carbon", "Kicker #5 ???; vertebra cross-section with growth rings; a red spike ring sweeps through on \"Cold War\"; small flat mushroom icon top-left (non-graphic); `Stat` ~50 YEARS", "push-in to the rings", "tick per ring; ding on \"fifty\"", bg=ocean(45))
def _(c):
    t_c = c.w("W3", "carbon")
    return [head("#5 ???", c.ls("W1")), svg(VERTEBRA, 960, 540, 560, 560, z=3, start=c.ls("W2")),
            svg(MUSHROOM, 300, 260, 140, 168, z=3, start=c.w("W3", "cold"), enter=appear(c.w("W3", "cold"))),
            head(L("W3")["screen"], c.w("W3", "2020"), out=c.ls("W4"), red=["BOMB"]),
            rect(960, 540, 8, 560, RED, z=4, keyframes=[{"t": t_c, "x": 680, "opacity": 0}, {"t": t_c + 0.1, "opacity": 1}, {"t": t_c + 1.6, "x": 1240}]),
            comp("explainer/Stat", 960, 920, 700, 220, {"value": 50, "prefix": "~", "suffix": " YEARS", "at": c.w("W4", "fifty"), "size": 90}, z=5, depth=0)], \
        {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": c.dur, "zoom": 1.12}]}, [("tick", c.ls("W2") + 0.3 * i) for i in range(4)] + [("ding", c.w("W4", "fifty"))]


@shot("W5", "Size", "Kicker #5 WHALE SHARK; `WhaleShark`* jaw open, `ScaleBar` ~1.5 M (vertical) across the mouth with YOU standing beside it (1.75 m)", "pull-out from the mouth", "whoosh", bg=ocean(20))
def _(c):
    t = c.w("W5", "metre")
    return [fig("WhaleShark", 900, 560, 18 * 70, 400, pxPerM=70, jaw=1, z=3), fig("You", 1650, 620, 0.5 * 70, 1.75 * 70, pose="stand", z=4),
            comp("explainer/ScaleBar", 1560, 620, 1.5 * 70, 80, {"label": "~1.5 M", "at": t}, rotate=-90, z=4),
            head(L("W5")["screen"], c.w("W5", "whale"), red=["WHALE"])], {"keyframes": [{"t": 0, "zoom": 1.3, "x": 1400}, {"t": c.dur, "zoom": 1.0, "x": 960}]}, [("whoosh", 0.1)]


@shot("W6", "2P night scenario", "Night surface (`surface` 0.15, dark sky); boat hull + light cone (svg) at top; plankton particles gather in the cone; YOU floats in the glow (no gear); the WhaleShark* rises mouth-open into the cone; on \"dark\" the frame goes black-red (inside)", "slow creep-in; dip to dark", "bubbles; underwater_rumble on \"rises\"", bg=ocean(4, surface=0.15, skyTop="#02070a", skyBottom="#06141b", rays=0))
def _(c):
    tr, td = c.w("W6", "rises"), c.w("W6", "dark")
    return [svg(BOAT_LIGHTS, 960, 230, 800, 520, z=2, depth=0.8),
            {"type": "particles", "preset": "dust", "count": 120, "color": "#fff6c8", "size": [2, 5], "x": 960, "y": 420, "width": 500, "height": 360, "z": 3},
            fig("You", 960, 360, 70, 140, pose="stand", z=5),
            fig("WhaleShark", 960, 1250, 1400, 400, pxPerM=70, rotate=-60, jaw=1, z=4, keyframes=[{"t": 0, "y": 1400}, {"t": tr + 2.0, "y": 760, "ease": "out"}]),
            rect(960, 540, W, H, "#120609", z=9, depth=0, keyframes=[{"t": max(0, td - 0.3), "opacity": 0}, {"t": td + 0.3, "opacity": 1}])], \
        {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": c.dur, "zoom": 1.1}]}, [("bubbles", 0.3), ("underwater_rumble", tr)]


@shot("W7", "Gauge #5 from inside", "POV inside the mouth: full-frame sieve (filter pads) with the dark throat hole centre; on \"throat\" cut to the gauge: front-view YOU + red ring, cyan throat ring grows from a quarter (2.5 cm, solid) to 15 cm (dashed cap); cereal-bowl icon pops; pizza box under YOU; kicker THROAT ≤ ~15 CM ≈ A CEREAL BOWL", "push-in on the tiny ring", "pop on \"bowl\", click", bg={"type": "color", "color": "#120609"})
def _(c):
    t = c.w("W7", "throat")
    sieve = svg(SIEVE, 960, 540, W, H, z=2, depth=0, end=t + 0.3, keyframes=[{"t": 0, "scale": 1.0}, {"t": t, "scale": 1.25}])
    g = gauge(c, 760, 500, throat=(2.5, 15, c.w("W8", "quarter"), c.w("W8", "cereal")), at=t + 0.3, label="≤ ~15 CM")
    for l in g:
        l.setdefault("start", t + 0.3)
    return [sieve, rect(960, 540, W, H, "#0c2a33", z=1, depth=0, start=t + 0.3)] + g + [
        svg(BOWL, 1400, 480, 150, 75, start=c.w("W8", "cereal"), enter=appear(c.w("W8", "cereal")), z=6),
        svg(PIZZA, 1400, 700, 46 * PXCM * 0.8, 8 * PXCM * 0.8, start=c.w("W9", "pizza"), enter=appear(c.w("W9", "pizza")), z=6),
        head(L("W8")["screen"], c.w("W8", "estimates"), red=["MUG"]),
        head("NOT A CONTEST", c.w("W9", "contest"), y=830, size=50, red=["CONTEST"])], \
        {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": t + 0.3, "zoom": 1.0}, {"t": c.dur, "zoom": 1.1, "x": 760}]}, [("pop", c.w("W8", "cereal")), ("click", t + 0.3)]


@shot("W10", "Exit", "The water jets out through the gill slits (arrows); YOU drifts back out of the mouth the way it came in; the WhaleShark* cruises on, unbothered", "shake 0.15 s", "whoosh, bubbles", bg=ocean(10, surface=0.1))
def _(c):
    t = c.w("W10", "you")
    return [fig("WhaleShark", 960, 600, 1400, 400, pxPerM=70, jaw=0.6, z=3, keyframes=[{"t": 0, "x": 1000}, {"t": c.dur, "x": 700}]),
            fig("You", 1600, 560, 60, 120, pose="shrug", z=4, keyframes=[{"t": max(0, t - 0.2), "x": 1500, "opacity": 0}, {"t": t + 0.6, "x": 1700, "opacity": 1, "ease": "out"}])], \
        {"preset": "drift", "shake": [{"at": t, "duration": 0.15, "amplitude": 8}]}, [("whoosh", t), ("bubbles", 0.2)]


@shot("W11", "Verdict #5 (drop)", "Board: the blue whale column slides right; the WhaleShark column grows to 15 (solid to 2.5, dashed cap) in slot 1, below it; stamp WHALE SHARK · ≤15 CM", "static", "whoosh down, impact", bg=ocean(40))
def _(c):
    t = c.w("W11", "drops")
    return board(c, ["blue"], new="whaleShark", at=t) + [tag(L("W11")["screen"], c.w("W11", "fifteen"), y=245)], {"preset": "none"}, [("impact", t + 0.6)]


@shot("K1", "Face + filter rate", "Kicker #4 BASKING SHARK; `BaskingShark`* jaw fully open, gill arches + raker comb visible, `ScaleBar` ~1 M (vertical) on the mouth; then `Stat` 2,000,000 L / HOUR with an Olympic-pool outline filling beside it", "slow push into the mouth", "underwater_rumble; bubbles loop", bg=ocean(15))
def _(c):
    t = c.w("K3", "two")
    return [fig("BaskingShark", 760, 560, 10 * 120, 360, pxPerM=120, jaw=1, z=3),
            comp("explainer/ScaleBar", 1160, 560, 1.0 * 120, 80, {"label": "~1 M", "at": c.w("K2", "metre")}, rotate=-90, z=4),
            head("#4 BASKING SHARK", c.w("K1", "basking"), out=t, red=["BASKING"]),
            comp("explainer/Stat", 1440, 330, 760, 220, {"value": 2000000, "suffix": " L / HOUR", "at": t, "duration": 1.4, "size": 72}, z=5, depth=0),
            svg(POOL, 1440, 620, 500, 250, start=t, z=5),
            svg(POOL_FILL, 1440, 745, 500, 250, start=t, z=4, anchorY=1.0, keyframes=[{"t": t, "scaleY": 0}, {"t": t + 2.5, "scaleY": 0.8}])], \
        {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": c.dur, "zoom": 1.08, "x": 860}]}, [("underwater_rumble", 0.1), ("bubbles", t)]


@shot("K4", "Speed bump", "Kicker SO WHY NOT YOU?; YOU drifts into the open mouth, bonks into the raker comb (svg), the shark swerves; `Tag` SPEED BUMP (yellow)", "side tracking; bump shake 0.1 s", "pop (bonk), whoosh", bg=ocean(12))
def _(c):
    tb = c.w("K6", "drift")
    return [head(L("K4")["screen"], c.ls("K4"), out=c.ls("K5"), red=["NOT"]),
            fig("BaskingShark", 760, 560, 10 * 120, 360, pxPerM=120, jaw=1, z=3, keyframes=[{"t": 0, "rotate": 0}, {"t": tb + 0.6, "rotate": 0}, {"t": tb + 1.4, "rotate": -12}]),
            svg(RAKERS, 1180, 560, 200, 260, z=4, start=c.w("K5", "comb"), enter=appear(c.w("K5", "comb"))),
            fig("You", 1500, 560, 70, 140, pose="panic", z=5, keyframes=[{"t": 0, "x": 1700}, {"t": tb + 0.5, "x": 1260}, {"t": tb + 0.7, "x": 1330, "rotate": 30}]),
            tag("SPEED BUMP", c.w("K6", "speed"), accent="yellow", y=830, size=44)], \
        {"preset": "panLeft", "amount": 0.3, "shake": [{"at": tb + 0.5, "duration": 0.1, "amplitude": 10}]}, [("pop", tb + 0.5), ("whoosh", tb + 1.0)]


@shot("K8", "Sea monster (gross-out)", "Night deck kept minimal: newspaper card (svg) with a lumpy long-necked carcass silhouette; `Headline` 1977 · SEA MONSTER? stamp; non-graphic", "slow push", "drone; stinger on \"monster\"", bg=ocean(5, surface=0.25, skyTop="#02070a", skyBottom="#0a1820", rays=0))
def _(c):
    return [svg(CARCASS, 760, 520, 900, 480, z=3, start=c.w("K8", "carcass"), enter=appear(c.w("K8", "carcass"), 0.5, "fade")),
            svg(NEWSPAPER, 1450, 560, 480, 330, z=4, start=c.w("K8", "papers"), enter=appear(c.w("K8", "papers"), 0.3, "drop")),
            head(L("K8")["screen"], c.w("K8", "1977"), red=["MONSTER?"])], {"preset": "pushIn", "amount": 0.5}, \
        [("drone", 0.2), ("stinger", c.w("K8", "monster"))]


@shot("K9", "Rot diagram + gauge", "Diagram: BaskingShark* outline; `rot` 0→1 fades the lower jaw, gills and fins; the remains morph to the 1977 carcass outline (\"dinosaur\"); then the throat: a cyan ~10 cm ring with a sharp bend drawn behind it next to the red 45 ring; kicker THROAT ~10 CM + A BEND", "static, then push on the ring", "tick; stinger tail", bg=ocean(40))
def _(c):
    tr = c.w("K9", "rots")
    tg = c.w("K10", "ten")
    lay = [fig("BaskingShark", 760, 480, 1100, 330, pxPerM=110, silhouette="#9fb3b8", rot=[{"t": tr, "v": 0}, {"t": tr + 2.4, "v": 1}], z=3, end=c.ls("K10") + 0.5),
           svg(CARCASS, 760, 520, 900, 480, z=2, opacity=0.5, start=c.w("K9", "dinosaur"), end=c.ls("K10") + 0.5),
           head(L("K9")["screen"], c.w("K9", "tissue"), out=c.ls("K10"))]
    g = gauge(c, 960, 520, throat=(10, 10, tg, tg + 0.3), at=c.ls("K10") + 0.4, label="~10 CM + A BEND")
    for l in g:
        l.setdefault("start", c.ls("K10") + 0.4)
    lay += g + [svg(S("0 0 40 40", '<path d="M20 2 L20 22 L36 36" stroke="#e8f1f4" stroke-width="3" fill="none"/>'), 1010, 560, 100, 100, start=c.w("K10", "bend"), z=7),
                head(L("K10")["screen"], c.w("K10", "ten"))]
    return lay, {"preset": "none"}, [("tick", tg), ("stinger", c.w("K9", "dinosaur"))]


@shot("K11", "Verdict #4 (sawtooth drop)", "Board: the BaskingShark column first rises past the blue whale (to ~38, \"the scariest mouth\"), hovers, then falls to 10, below even the whale shark (the others slide right); stamp BASKING SHARK · ~10 CM", "static", "whoosh down, impact", bg=ocean(40))
def _(c):
    t = c.ls("K11") + 0.2
    return board(c, ["blue", "whaleShark"], new="basking", at=t, hover=("basking", 38)) + [tag(L("K11")["screen"], c.w("K11", "bottom"), y=245)], \
        {"preset": "none"}, [("riser", t), ("whoosh", t + 1.3), ("impact", t + 1.8)]


@shot("X1", "Re-immersion (escalates)", "Exact replay of the 0:00 tableau (same seed); the three strainers already ranked (BlueWhale, WhaleShark, BaskingShark) fade grey with a ✕ on \"passed\"; the three left (Humpback, GoliathGrouper, SpermWhale) darken to red-black one by one on \"people\", \"inhales\", \"teeth\"; the board flashes small top-right with its 3 columns", "slow push-in matching 0:00", "heartbeat_slow; tick ×3; heartbeat on \"teeth\"", bg=ocean(8, surface=0.12, rays=7))
def _(c):
    tp = c.w("X2", "passed")
    greys = {"BlueWhale": tp, "WhaleShark": tp + 0.3, "BaskingShark": tp + 0.6}
    reds = {"Humpback": c.w("X3", "people"), "GoliathGrouper": c.w("X3", "inhales"), "SpermWhale": c.w("X3", "teeth")}
    lay = tableau(c, greys=greys, pulse_red=reds)
    lay.append(svg(S("0 0 300 170", '<rect width="300" height="170" rx="14" fill="rgba(4,20,26,0.85)"/><rect x="20" y="40" width="260" height="3" fill="#ff5a4a"/>'
                    '<rect x="40" y="130" width="40" height="25" fill="#9fd3e0"/><rect x="110" y="130" width="40" height="25" fill="#9fd3e0"/><rect x="180" y="62" width="40" height="93" fill="#9fd3e0"/>'),
                   1700, 140, 300, 170, depth=0, z=12, start=c.ls("X1") + 0.5, end=c.ls("X2") + 1.5))
    return lay, {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": c.dur, "zoom": 1.1}]}, [("heartbeat_slow", 0.2)] + [("tick", t) for t in greys.values()] + [("heartbeat", reds["SpermWhale"])]


@shot("U1", "Gauge first (#3)", "Kicker #3 HUMPBACK; `Humpback`* silhouette top-right; front-view YOU + red ring; a fist icon, then the cyan ring grows from fist (10, solid) to 38 cm (dashed cap) — the closest yet, a yellow NEW RECORD stamp, still inside the red ring", "static; slow push on \"short\"", "sonar_ping on the ring; ding + click on \"record\"", bg=ocean(30))
def _(c):
    tf, t38 = c.w("U2", "fist"), c.w("U3", "thirty-eight")
    lay = [tag("#3 HUMPBACK", c.ls("U1"), y=150, size=44), fig("Humpback", 1500, 300, 15 * 40, 200, pxPerM=40, silhouette="#9fb3b8", z=2)]
    lay += gauge(c, 760, 540, throat=(10, 38, tf + 0.2, t38 + 0.5), at=c.w("U2", "gauge"), label="≤ ~38 CM (STRETCHED)")
    lay += [svg(FIST, 1300, 620, 90, 81, start=tf, enter=appear(tf)), head(L("U3")["screen"], t38, out=c.ls("U4"), red=["~38"]),
            tag(L("U4")["screen"], c.w("U4", "widest"), accent="yellow", y=830, size=40)]
    return lay, {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": c.ls("U4"), "zoom": 1.0}, {"t": c.dur, "zoom": 1.1, "x": 760}]}, \
        [("sonar_ping", tf + 0.2), ("ding", c.w("U4", "widest")), ("click", c.w("U4", "short"))]


@shot("U5", "Real cases (composite)", "`Map` Atlantic-wide (zoom ≤ 2): pins Cape Cod (lon -70.2, lat 41.9) \"2021\" and Strait of Magellan (lon -70.9, lat -53.2) \"2025\"; per pin a 1 s flat vignette (diver / kayak silhouette in a mouth → back in open water); kicker 2021 · CAPE COD / 2025 · CHILE", "map pans between pins", "sonar_ping per pin", bg={"type": "color", "color": "#0b2028"})
def _(c):
    t1, t2 = c.w("U6", "cape"), c.w("U6", "strait")
    mp = comp("explainer/Map", 960, 540, W, H, {"views": [{"t": 0, "lon": -60, "lat": 0, "zoom": 1.3}, {"t": t1, "lon": -70, "lat": 35, "zoom": 2.0},
                                                         {"t": t2, "lon": -70, "lat": -45, "zoom": 2.0}],
                                               "pins": [{"lon": -70.2, "lat": 41.9, "at": t1, "label": "2021"}, {"lon": -70.9, "lat": -53.2, "at": t2, "label": "2025"}]}, z=1, depth=0)
    return [mp, fig("Diver", 1500, 760, 260, 110, arms="side", z=4, start=t1, end=t2), fig("You", 1500, 760, 40, 80, pose="wave", z=4, start=t2),
            head(L("U6")["screen"], t1, red=["CAPE", "CHILE"])], {"preset": "none"}, [("sonar_ping", t1), ("sonar_ping", t2)]


@shot("U7", "Lunge + word gag", "`Humpback`* vertical lunge through a fish ball (particles) with YOU inside the ball; then `Headline` ENGULFED ≠ SWALLOWED with a sandwich + sock inset", "camera tilts up with the lunge", "whoosh_long, bubbles; pop on \"sock\"", bg=ocean(10, surface=0.2))
def _(c):
    tl = c.w("U7", "lunge")
    return [{"type": "particles", "preset": "dust", "count": 180, "color": "#cfe3ea", "size": [3, 6], "x": 960, "y": 420, "width": 600, "height": 360, "z": 3, "end": c.ls("U8") + 1.0},
            fig("You", 980, 420, 50, 100, pose="panic", z=4, end=c.ls("U8") + 1.0),
            fig("Humpback", 960, 1300, 1400, 500, pxPerM=90, pose="lunge", pleats=[{"t": tl + 1.5, "v": 0}, {"t": tl + 2.4, "v": 1}], z=5, end=c.ls("U8") + 1.0,
                keyframes=[{"t": 0, "y": 1500}, {"t": tl + 2.0, "y": 560, "ease": "out"}]),
            head(L("U8")["screen"], c.w("U8", "engulfed"), red=["≠"]),
            svg(SANDWICH, 960, 640, 520, 300, start=c.w("U8", "sandwich"), enter=appear(c.w("U8", "sandwich")), z=7)], \
        {"keyframes": [{"t": 0, "y": 700}, {"t": tl + 2.2, "y": 480}]}, [("whoosh_long", tl), ("bubbles", tl + 1.5), ("pop", c.w("U8", "sock"))]


@shot("U10", "Verdict #3 (record)", "Board: the Humpback column grows past the blue whale to 38 (solid to fist, dashed cap), RECORD label; stamp HUMPBACK · ~38 CM · RECORD; lifeguard whistle icon gag", "static", "impact, ding", bg=ocean(40))
def _(c):
    t = c.ls("U10") + 0.2
    return board(c, ["blue", "whaleShark", "basking"], new="humpback", at=t) + [tag(L("U10")["screen"], c.w("U10", "record"), y=245, accent="yellow")], \
        {"preset": "none"}, [("impact", t + 0.6), ("ding", c.w("U10", "record"))]


@shot("G1", "Size (#2)", "Kicker #2 GOLIATH GROUPER; `GoliathGrouper`* next to YOU at true scale (`pxPerM` 260); grand piano silhouette (svg) drops in on \"piano\"; kicker ~360 KG ≈ A GRAND PIANO", "static, slight push", "underwater_rumble; pop on \"piano\"", bg=ocean(20))
def _(c):
    tp = c.w("G2", "piano")
    return [fig("GoliathGrouper", 760, 560, 2.5 * 260, 300, pxPerM=260, z=3), fig("You", 1400, 600, 0.5 * 260, 1.75 * 260, pose="stand", z=3),
            head("#2 GOLIATH GROUPER", c.w("G1", "goliath"), out=c.ls("G2"), red=["GOLIATH"]), svg(PIANO, 1550, 860, 330, 220, start=tp, enter=appear(tp, 0.3, "drop"), z=4),
            head(L("G2")["screen"], c.ls("G2"), red=["PIANO"])], {"preset": "pushIn", "amount": 0.3}, [("underwater_rumble", 0.1), ("pop", tp)]


@shot("G3", "Suction", "Kicker IT INHALES; `GoliathGrouper`* `flare` 0→1 in 6 frames on each prey word; lobster, fish, turtle, shark icons (svg / GreatWhite silhouette) pulled in one after another", "quick push on each gulp", "whoosh ×4 short", bg=ocean(20))
def _(c):
    ts = [c.w("G4", "lobsters"), c.w("G4", "fish"), c.w("G4", "turtles"), c.w("G4", "sharks")]
    flare = []
    for t in ts:
        flare += [{"t": t, "v": 0}, {"t": t + 0.2, "v": 1}, {"t": t + 0.7, "v": 0}]
    lay = [head(L("G3")["screen"], c.w("G3", "inhales"), red=["INHALES"]), fig("GoliathGrouper", 700, 560, 2.5 * 300, 340, pxPerM=300, flare=flare, z=3)]
    for i, t in enumerate(ts):
        icon = fig("GreatWhite", 1400, 560, 300, 110, pxPerM=60, silhouette="#c9d6da") if i == 3 else svg(S("0 0 20 10", '<ellipse cx="10" cy="5" rx="9" ry="4" fill="#c9d6da"/>'), 1400, 560, 160, 80)
        icon.update({"z": 4, "start": max(0, t - 1.0), "keyframes": [{"t": max(0, t - 1.0), "x": 1500, "scale": 1}, {"t": t, "x": 1500, "scale": 1}, {"t": t + 0.35, "x": 1000, "scale": 0.2, "opacity": 0, "ease": "in"}]})
        lay.append(icon)
    return lay, {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": c.dur, "zoom": 1.08}], "shake": [{"at": t + 0.15, "duration": 0.15, "amplitude": 5} for t in ts]}, [("whoosh", t) for t in ts]


@shot("G5", "Proof", "`Map` Gulf of Mexico (zoom 3) pin SW Florida (lon -81.9, lat 26.3); vignette: fishing line + hooked shark (GreatWhite silhouette as blacktip stand-in) inhaled by the grouper; kicker SHARK ~1.2 M · ONE GULP", "static", "impact", bg={"type": "color", "color": "#0b2028"})
def _(c):
    tg = c.w("G5", "gulp")
    return [comp("explainer/Map", 480, 540, 960, 1080, {"views": [{"t": 0, "lon": -84, "lat": 25, "zoom": 3}], "pins": [{"lon": -81.9, "lat": 26.3, "at": 0.4, "label": "FLORIDA"}]}, z=1, depth=0),
            rect(1440, 540, 960, 1080, "#0e3440", z=1, depth=0),
            fig("GoliathGrouper", 1300, 620, 650, 300, pxPerM=260, flare=[{"t": tg - 0.3, "v": 0}, {"t": tg, "v": 1}, {"t": tg + 0.6, "v": 0}], z=3),
            fig("GreatWhite", 1720, 600, 1.2 * 260, 110, pxPerM=260 / 1.2 * 1.2 / 5, silhouette="#c9d6da", z=4, keyframes=[{"t": 0, "x": 1720}, {"t": tg - 0.1, "x": 1720}, {"t": tg + 0.3, "x": 1380, "scale": 0.2, "opacity": 0}]),
            head(L("G5")["screen"], c.w("G5", "hooked"), red=["GULP"])], {"preset": "none"}, [("impact", tg)]


@shot("G6", "2P wreck", "Wreck hull silhouette on the seabed (`Ocean` depth 25); YOU drifting over it (no gear); a sofa-sized shape slides out from under the hull", "slow creep-in", "drone; boom ×2 under \"hull\"", bg=ocean(25))
def _(c):
    ts = c.w("G6", "slides")
    return [svg(WRECK, 960, 900, 1700, 560, z=2), fig("You", 960, 360, 70, 140, pose="stand", z=4),
            fig("GoliathGrouper", 900, 880, 650, 300, pxPerM=260, silhouette=SIL, z=3, keyframes=[{"t": 0, "x": 500, "opacity": 0}, {"t": ts, "x": 500, "opacity": 0}, {"t": ts + 1.6, "x": 900, "opacity": 1}])], \
        {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": c.dur, "zoom": 1.1}]}, [("drone", 0.2), ("boom", c.w("G6", "hull")), ("boom", c.w("G6", "hull") + 0.8)]


@shot("G8", "Micro-loop + gauge #2", "Kicker HOW WIDE? → NOBODY KNOWS / NO PUBLISHED NUMBER; then the gauge: front-view YOU (45) beside the dashed 40 outline; yellow dashed throat ring ~40 (ESTIMATE); on \"stops\" YOU's shoulders hit the ring and the frame holds (idle off) with a glitch on the freeze; kicker 45: STUCK · 40: TOO CLOSE TO CALL", "push-in; freeze 0.5 s", "tick; impact + glitch on \"stops\"", bg=ocean(30))
def _(c):
    tg, tstop = c.w("G10", "forty"), c.w("G12", "stops")
    lay = [head("HOW WIDE?", c.ls("G8"), out=c.ls("G9")), head("NOBODY KNOWS", c.ls("G9"), out=c.ls("G10"), red=["NOBODY"]),
           head(L("G10")["screen"], tg, out=c.ls("G12"), color="yellow")]
    lay += gauge(c, 760, 520, throat=(40, 40, tg, tg + 0.4), at=c.ls("G10"), est=True, label="~40 (ESTIMATE)")
    lay += [svg(you_front(40, "#ff9a8f", dashed=True), 1350, 520 + 61 * PXCM, 60 * PXCM, 180 * PXCM, z=3, start=c.ls("G11")),
            txt("40", 1350, 300, 60, "#ff9a8f", start=c.ls("G11"), z=5),
            head(L("G12")["screen"], c.w("G12", "forty", 2), y=830, size=48, red=["STUCK"])]
    return lay, {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": tstop, "zoom": 1.12, "x": 760}, {"t": tstop + 0.5, "zoom": 1.12, "x": 760}, {"t": c.dur, "zoom": 1.0, "x": 960}],
                 "shake": [{"at": tstop, "duration": 0.2, "amplitude": 14}]}, [("tick", tg), ("impact", tstop), ("glitch", tstop + 0.05)]


@shot("G13", "Folklore + ban", "Dive-boat speech bubbles (\"IT ATE A DIVER!\") each stamped with a red ✕, kicker STORIES THAT HOLD UP: 0; then `Headline` 1990 · HARVEST BAN over a fishing hook with a red ✕", "static", "pop ×3, impact", bg=ocean(10, surface=0.15))
def _(c):
    tb = c.w("G14", "banned")
    lay = []
    for i, msg in enumerate(["IT ATE A DIVER!", "SWALLOWED HIM!", "TRUE STORY!"]):
        t = c.ls("G13") + 0.4 + i * 0.6
        lay.append(svg(BUBBLE(msg), 520 + i * 440, 420 + (i % 2) * 120, 400, 164, start=t, end=c.ls("G14") + 0.2, enter=appear(t), z=4))
        lay.append(svg(CROSS, 520 + i * 440, 420 + (i % 2) * 120, 90, 90, start=c.w("G13", "single") + i * 0.15, end=c.ls("G14") + 0.2, z=5))
    lay += [head(L("G13")["screen"], c.w("G13", "single"), out=c.ls("G14"), red=["0"]), svg(HOOK_X, 960, 560, 260, 260, start=tb, enter=appear(tb), z=4),
            head(L("G14")["screen"], c.w("G14", "1990"), red=["BAN"])]
    return lay, {"preset": "none"}, [("pop", c.ls("G13") + 0.4 + i * 0.6) for i in range(3)] + [("impact", tb)]


@shot("G15", "Verdict #2 (asterisk)", "Board: the Grouper column (yellow, dashed = estimate only) rises to ~40, just past the humpback, with a big asterisk; stamp GROUPER · ~40 CM*", "static", "impact; click on \"asterisk\"", bg=ocean(40))
def _(c):
    t = c.ls("G15") + 0.3
    return board(c, ["blue", "whaleShark", "basking", "humpback"], new="grouper", at=t) + [tag(L("G15")["screen"], c.w("G15", "asterisk"), y=245, accent="yellow")], \
        {"preset": "none"}, [("impact", t + 0.6), ("click", c.w("G15", "asterisk"))]


@shot("S1", "Size (#1)", "Kicker #1 SPERM WHALE; `SpermWhale` `teeth` on, `ScaleBar` ~16 M; 3 × `Bus` icons stacked as a weight comparison (`Stat` ~40 T); music thins (deep_ocean low, no jokes from here)", "slow pan along the body", "underwater_rumble", bg=ocean(40))
def _(c):
    tb = c.w("S2", "three")
    return [fig("SpermWhale", 960, 480, 16 * 90, 420, pxPerM=90, teeth=True, z=3, keyframes=[{"t": 0, "x": 1100}, {"t": c.dur, "x": 820}]),
            comp("explainer/ScaleBar", 960, 760, 16 * 90, 120, {"label": "~16 M", "at": c.w("S2", "sixteen")}, z=4),
            head("#1 SPERM WHALE", c.w("S1", "sperm"), red=["SPERM"]),
            tag("~40 T ≈ 3 BUSES", tb, y=830)] + [fig("Bus", 1500, 1000 - i * 70, 300, 70, pxPerM=25, start=tb + i * 0.25, z=4) for i in range(3)], \
        {"preset": "panLeft", "amount": 0.3}, [("underwater_rumble", 0.1)]


@shot("S3", "Prey", "`DepthMeter` 0→1,000 m quick; whale in near-dark meets a giant squid (`ColossalSquid` `hooks` false as stand-in); `Map` inset Azores pin 1955; the stomach cutaway (svg) with a near-whole squid inside; `Stat` ~180 KG (REPORTED) + two YOU figures on a scale", "track down with the whale", "sonar_ping, drone; ding on \"two\"", bg=ocean(800))
def _(c):
    ta, tw = c.w("S4", "azores"), c.w("S5", "weight")
    return [comp("explainer/DepthMeter", 120, 540, 160, 900, {"depth": [{"t": 0, "v": 0}, {"t": 4, "v": 1000, "ease": "out"}], "max": 1200, "step": 200}, z=6, depth=0, end=ta),
            fig("SpermWhale", 760, 520, 16 * 70, 340, pxPerM=70, z=3, end=ta),
            fig("ColossalSquid", 1450, 560, 10 * 60, 300, pxPerM=60, hooks=False, z=3, end=ta),
            head(L("S3")["screen"], c.w("S3", "bigger"), out=ta, red=["BIGGER"]),
            comp("explainer/Map", 1500, 300, 640, 360, {"views": [{"t": 0, "lon": -28, "lat": 38.5, "zoom": 3}], "pins": [{"lon": -28, "lat": 38.5, "at": ta + 0.2, "label": "1955"}]}, z=5, depth=0, start=ta),
            svg(STOMACH, 700, 560, 900, 585, start=ta, z=3), fig("ColossalSquid", 700, 560, 700, 260, pxPerM=70, hooks=False, silhouette="#c98a7a", start=ta + 0.4, z=4),
            head(L("S4")["screen"], ta, out=tw, red=["SQUID"]),
            comp("explainer/Stat", 1500, 760, 700, 200, {"value": 180, "prefix": "~", "suffix": " KG", "label": "REPORTED", "at": tw, "size": 80}, z=6, depth=0),
            fig("You", 1420, 960, 50, 100, pose="stand", z=6, start=c.w("S5", "two")), fig("You", 1500, 960, 50, 100, pose="stand", z=6, start=c.w("S5", "two") + 0.15),
            txt("+", 1570, 950, 50, WHITE, start=c.w("S5", "two") + 0.3, z=6)], \
        {"keyframes": [{"t": 0, "y": 400}, {"t": ta, "y": 600}, {"t": ta + 0.01, "y": 540}]}, [("sonar_ping", 0.5), ("drone", 1.0), ("ding", c.w("S5", "two"))]


@shot("S6", "Gauge #1: no number", "Front-view YOU + red ring; the throat ring flickers (no size), a big `?`; kicker NO MEASUREMENT; then ScaleBar comparison 16 M (typical big bull) vs 18 M+ (the anatomist's \"very big adult bull\") with SpermWhale silhouettes; kicker BIG BULLS ONLY · ~18 M+", "static", "tick; heartbeat_slow", bg=ocean(60))
def _(c):
    tn, t18 = c.ls("S7"), c.w("S9", "eighteen")
    g = gauge(c, 760, 520, at=0.2)
    for l in g:
        l["end"] = c.ls("S9")
    flick = circ(760, 520, 30 * PXCM, CYAN, 6, z=6, depth=0.4, end=c.ls("S9"), keyframes=[{"t": 0.6, "scale": 0.4, "opacity": 0.8}, {"t": 1.0, "scale": 1.4}, {"t": 1.3, "scale": 0.6},
                                                                                            {"t": 1.6, "scale": 1.6}, {"t": 1.9, "scale": 0.3, "opacity": 0}, HOOP])
    return g + [flick, txt("?", 760, 520, 200, YEL, start=tn, end=c.ls("S9"), z=7), head("NO MEASUREMENT", tn, out=c.ls("S9"), red=["NO"]),
                fig("SpermWhale", 900, 420, 16 * 70, 300, pxPerM=70, silhouette="#4a6670", z=3, start=c.ls("S9")),
                fig("SpermWhale", 960, 760, 18 * 70, 340, pxPerM=70, silhouette="#9fb3b8", z=3, start=t18, enter=appear(t18)),
                txt("MOST BIG BULLS ~16 M", 1600, 420, 30, GREY, start=c.ls("S9"), z=4), txt("\"VERY BIG\" ~18 M+", 1640, 760, 34, WHITE, start=t18, z=4),
                head(L("S9")["screen"], t18, red=["ONLY"])], {"preset": "none"}, [("tick", tn), ("heartbeat_slow", c.ls("S8"))]


@shot("S10", "Honest hedge", "Dark water, the whale fades into the deep as the depth grade drops; `Tag` NEVER SEEN FEEDING; small quote marks around \"SWALLOWS PREY WHOLE?\"", "slow push, no shake", "drone only", bg=ocean(900))
def _(c):
    return [fig("SpermWhale", 960, 560, 16 * 70, 340, pxPerM=70, z=3, keyframes=[{"t": 0, "opacity": 1, "y": 520}, {"t": c.dur, "opacity": 0.15, "y": 700}]),
            head(L("S10")["screen"], c.w("S10", "nobody"), red=["NEVER"]), tag("\"SWALLOWS PREY WHOLE?\" · EDUCATED GUESS", c.w("S10", "educated"), y=830, accent="yellow", size=30)], \
        {"preset": "pushIn", "amount": 0.4}, [("drone", 0.2)]


@shot("S11", "Ring retired", "The front-view YOU with the red ring; on \"down\" the ring drops off-frame and spins away (the gauge is retired)", "static", "click; low whoosh on the fall", bg=ocean(60))
def _(c):
    td = c.w("S11", "down")
    return gauge(c, 960, 520, at=0.1, ring_out=td) + [head("THE ONE THROAT THE GAUGE CAN'T MEASURE", c.w("S11", "this"), red=["CAN'T"], size=54)], {"preset": "none"}, \
        [("click", td), ("whoosh", td + 0.2)]


@shot("S12", "Verdict #1", "Board: a grey dashed SpermWhale column with a large `?` rises through the red line (\"COULD: BIG BULLS\"), then a small stamp HAS: NEVER under it; kicker COULD: BIG BULLS · HAS: NEVER", "static", "impact soft", bg=ocean(40))
def _(c):
    t = c.w("S12", "possibly")
    return board(c, ["blue", "whaleShark", "basking", "humpback", "grouper"], new="sperm", at=t) + [
        head(L("S12")["screen"], c.w("S12", "has"), y=62, size=40, red=["NEVER"]), tag(L("S13")["screen"], c.ls("S13"), y=245)], {"preset": "none"}, [("impact", t + 0.6)]


@shot("F1", "Reassurance flip", "Wide: the SpermWhale glides past a tiny YOU without turning; `Tag` YOU: NOT ON THE MENU; a squid icon floats by and the whale turns toward it instead", "slow pan", "bubbles", bg=ocean(80))
def _(c):
    return [fig("SpermWhale", 960, 600, 16 * 60, 280, pxPerM=60, z=3, keyframes=[{"t": 0, "x": 400}, {"t": c.dur, "x": 1500}]),
            fig("You", 1100, 330, 40, 80, pose="shrug", z=4), fig("ColossalSquid", 1800, 700, 200, 90, pxPerM=20, hooks=False, z=3, start=c.w("F1", "menu")),
            tag(L("F1")["screen"], c.w("F1", "menu"), y=830)], {"preset": "panRight", "amount": 0.3}, [("bubbles", 0.3)]


@shot("V1", "Twist (tone drop)", "Grade drops (saturate 0.4, vignette 0.5) and music cuts to dread through a 1.2 s fade; the board returns with one empty slot above the red line pulsing; kicker YES. on \"yes\"", "slow push", "stinger on \"yes\"", bg=ocean(40), transition={"type": "fade", "duration": 1.2}, grade=DROP)
def _(c):
    ty = c.ls("V3")
    lay = board(c, ["blue", "whaleShark", "basking", "humpback", "grouper", "sperm"])
    sx = slot_x(6, 7)
    lay.append(rect(sx, BASE - 58 * PX_PER_CM_B / 2, 130, 58 * PX_PER_CM_B, "rgba(0,0,0,0)", stroke=RED, strokeWidth=4, radius=10, z=7, depth=0,
                    keyframes=[{"t": c.w("V1", "empty"), "opacity": 0}, {"t": c.w("V1", "empty") + 0.4, "opacity": 1}, {"t": c.w("V1", "empty") + 0.9, "opacity": 0.4},
                               {"t": c.w("V1", "empty") + 1.4, "opacity": 1}]))
    lay.append(head("YES.", ty, size=140, red=["YES."], y=540))
    return lay, {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": c.dur, "zoom": 1.06}]}, [("stinger", ty)]


@shot("V4", "Evidence: Scotland", "`Map` UK + N Atlantic (zoom 3, Great Britain is coarse: ring marker, no coastline close-up) pin Isle of Harris (lon -7.0, lat 57.8) \"2019\"; stomach cutaway (svg) fills with a rope-and-net ball (svg); `Stat` ~100 KG; a YOU silhouette on a scale reads less (\"MORE THAN YOU WEIGH\")", "map then cut to the cutaway; slow push", "sonar_ping; drone", bg=ocean(40), grade=DROP)
def _(c):
    th, tk = c.w("V4", "harris"), c.w("V4", "hundred")
    return [comp("explainer/Map", 960, 540, W, H, {"views": [{"t": 0, "lon": -10, "lat": 52, "zoom": 2.5}], "rings": [{"lon": -7.0, "lat": 57.8, "r": 1.5, "at": th, "label": "2019 · HARRIS"}]},
                 z=1, depth=0, end=tk),
            svg(STOMACH, 760, 560, 900, 585, start=tk, z=3), svg(NET, 760, 560, 600, 360, start=tk + 0.2, z=4, keyframes=[{"t": tk + 0.2, "scale": 0.2}, {"t": tk + 2.0, "scale": 1.0, "ease": "out"}]),
            comp("explainer/Stat", 1450, 380, 700, 220, {"value": 100, "prefix": "~", "suffix": " KG", "at": tk, "size": 96}, z=5, depth=0),
            svg(debris("scale"), 1450, 760, 400, 140, start=c.w("V4", "weigh"), z=5), fig("You", 1450, 650, 60, 120, pose="stand", z=6, start=c.w("V4", "weigh")),
            tag("MORE THAN YOU WEIGH", c.w("V4", "weigh"), x=1450, y=880, size=30),
            tag("BUILT UP OVER TIME", c.w("V5", "built"), y=1000, accent="yellow", size=28)], \
        {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": c.dur, "zoom": 1.06}]}, [("sonar_ping", th), ("drone", tk)]


@shot("V6", "Evidence: Indonesia", "`Map` pin Wakatobi (lon 123.6, lat -5.5) \"2018\"; icon row counts in (`Debris`: 115 cups, 25 bags, 2 flip-flops) with `Stat` per icon; a bowling ball drops beside \"~6 KG\"", "map; icon row stagger", "pop per icon (fast); ding on each total", bg=ocean(40), grade=DROP)
def _(c):
    tc, tb, tf, tk = c.w("V6", "cups"), c.w("V6", "bags"), c.w("V6", "flip-flops"), c.w("V6", "bowling")
    lay = [comp("explainer/Map", 480, 330, 860, 560, {"views": [{"t": 0, "lon": 120, "lat": -3, "zoom": 3}], "rings": [{"lon": 123.6, "lat": -5.5, "r": 1.2, "at": 0.4, "label": "2018"}]}, z=1, depth=0)]
    for i, (kind, n, t) in enumerate((("cup", 115, tc), ("bag", 25, tb), ("flipflop", 2, tf))):
        x = 1100 + i * 260
        lay.append(svg(debris(kind), x, 360, 120, 150, start=t - 0.3, enter=appear(t - 0.3), z=4))
        lay.append(comp("explainer/Stat", x, 520, 260, 140, {"value": n, "at": t - 0.3, "duration": 0.8, "size": 64, "box": False}, z=5, depth=0))
    lay += [svg(debris("bowling"), 960, 820, 160, 160, start=tk, enter=appear(tk, 0.3, "drop"), z=4), tag("~6 KG ≈ A BOWLING BALL", tk, y=830),
            head(L("V6")["screen"], tc, size=48)]
    return lay, {"preset": "none"}, [("ding", tc + 0.6), ("ding", tb + 0.6), ("ding", tf + 0.6), ("impact", tk + 0.3)]


@shot("V7", "Rule callback", "Replay of the 0:16 RULES card (`Options`, same layout); on \"net\", \"rope\", \"flip-flops\" matching icons (rope coil, net, flip-flop) slide out of the card into the stomach cutaway, which now holds every piece of gear in the video; kicker ALL THE GEAR → INSIDE THE WHALE", "static", "whoosh per item; stinger tail on \"whale\"", bg=ocean(40), grade=DROP)
def _(c):
    its = [c.w("V7", "net"), c.w("V7", "rope"), c.w("V7", "flip-flops")]
    lay = [comp("explainer/Options", 620, 520, 1000, 680, {"title": "THE RULES", "items": ["JUST YOU", "NOTHING IN YOUR HANDS", "NOTHING IN YOUR POCKETS", "NO GEAR"], "at": -5, "size": 46,
                                                          "select": {"index": 3, "at": c.w("V7", "remember")}}, z=4, depth=0),
           svg(STOMACH, 1500, 560, 640, 416, z=3)]
    for i, (t, kind) in enumerate(zip(its, ("rope", "net", "flipflop"))):
        mk = debris("flipflop") if kind == "flipflop" else NET
        lay.append(svg(mk, 900, 700, 120 if kind == "flipflop" else 200, 160 if kind == "flipflop" else 120, z=6, start=t,
                       keyframes=[{"t": t, "x": 900, "y": 700}, {"t": t + 0.8, "x": 1420 + i * 70, "y": 540 + i * 30, "ease": "inOut"}]))
    lay.append(head(L("V8")["screen"], c.ls("V8"), red=["INSIDE"], size=56))
    return lay, {"preset": "none"}, [("whoosh", t) for t in its] + [("stinger", c.w("V8", "whale"))]


@shot("V9", "Villain swap", "Pull back from the gear-filled stomach to the whole whale swimming, then up to YOU floating free at the surface while a single flip-flop drifts down past the camera", "long pull-out", "drone fade; bubbles", bg=ocean(8, surface=0.1), grade=DROP)
def _(c):
    return [fig("SpermWhale", 960, 760, 16 * 60, 280, pxPerM=60, z=3, keyframes=[{"t": 0, "x": 900}, {"t": c.dur, "x": 1300}]),
            fig("You", 960, 220, 70, 140, pose="stand", z=4),
            svg(debris("flipflop"), 1300, 100, 60, 120, z=8, depth=1.4, keyframes=[{"t": 0, "y": 80, "rotate": 0}, {"t": c.dur, "y": 1100, "rotate": 160}])], \
        {"keyframes": [{"t": 0, "zoom": 1.5, "y": 760}, {"t": c.dur, "zoom": 1.0, "y": 480}]}, [("bubbles", 0.5)]


@shot("E1", "Final board", "The finished board, colour back to normal; each column pulses as its verdict is read (basking shark, whale shark, blue whale, humpback, grouper, sperm whale, our rubbish); held as comment bait", "static, hold", "tick per column", bg=ocean(40), transition={"type": "fade", "duration": 0.8})
def _(c):
    pulses = [("basking", c.w("E2", "basking")), ("whaleShark", c.w("E2", "whale")), ("blue", c.w("E2", "blue")), ("humpback", c.w("E2", "humpback")),
              ("grouper", c.w("E2", "grouper")), ("sperm", c.w("E2", "sperm")), ("rubbish", c.w("E2", "rubbish"))]
    return board(c, ["blue", "whaleShark", "basking", "humpback", "grouper", "sperm", "rubbish"], pulse=pulses) + [tag("FINAL BOARD", c.ls("E1"), y=245, accent="red", size=30)], \
        {"preset": "none"}, [("tick", t) for _, t in pulses]


@shot("E3", "Bookend", "Back to the 0:00 composition, now empty of shadows; YOU swims up out of frame toward the surface; the red ring is gone", "slow tilt up", "whoosh; deep_ocean swells (gain automation)", bg=ocean(8, surface=0.12, rays=7))
def _(c):
    lay = tableau(c, empty=True)
    lay[-1]["keyframes"] = [{"t": 0, "y": 330}, {"t": c.dur, "y": 60}]
    return lay, {"keyframes": [{"t": 0, "y": 540}, {"t": c.dur, "y": 420}]}, [("whoosh", 0.3)]


@shot("C1", "CTA", "Finished board returns small; `Headline` NEXT GIANT? ↓; on \"blue whale\" a BlueWhale silhouette glides across the bottom with `gape` open and a krill cloud, and YOU (pose panic) scoots out of frame", "static; hard cut to black at the end", "pop; stinger", bg=ocean(30))
def _(c):
    tb = c.w("C2", "blue")
    lay = board(c, ["blue", "whaleShark", "basking", "humpback", "grouper", "sperm", "rubbish"])
    for l in lay:
        l["opacity"] = 0.45
    lay += [head(L("C1")["screen"], c.w("C1", "which"), red=["NEXT"], y=540, size=96),
            fig("BlueWhale", 960, 950, 1500, 260, pxPerM=50, gape=0.7, z=8, depth=0, start=tb, keyframes=[{"t": tb, "x": -900}, {"t": c.dur, "x": 1100}]),
            fig("You", 1700, 900, 60, 120, pose="panic", z=9, depth=0, start=tb, keyframes=[{"t": tb + 1.0, "x": 1700}, {"t": tb + 2.0, "x": 2100}])]
    return lay, {"preset": "none"}, [("pop", c.w("C1", "which")), ("stinger", c.w("C2", "krill", end=True))]


# ------------------------------------------------------------------ assemble

def build():
    starts = []
    for i, s in enumerate(SHOTS):
        st = 0.0 if i == 0 else round(L(s["line"])["start"] - CUT_LEAD + s["offset"], 2)
        starts.append(st)
    ends = starts[1:] + [TOTAL]
    scenes, md = [], []
    for i, (s, st, en) in enumerate(zip(SHOTS, starts, ends)):
        ctx = Ctx(st, round(en - st, 2))
        layers, cam, cues = s["build"](ctx)
        sc = {"id": f"s{i + 1:02d}", "duration": round(en - st, 2), "background": s["bg"] or ocean(30), "layers": layers,
              "camera": cam, "sfx": [{"cue": n, "at": round(max(0.0, min(ctx.dur - 0.05, t)), 2), "volume": 0.7} for n, t in cues],
              "notes": f"{s['kind']} | starts on VO line {s['line']} | " + " ".join(L(x)["text"] for x in ORDER if st - 0.01 <= L(x)["start"] < en - 0.01)}
        if s["transition"]:
            sc["transitionIn"] = s["transition"]
        elif i:
            sc["transitionIn"] = {"type": "cut"}
        if s["grade"]:
            sc["grade"] = s["grade"]
        punch_ins(sc, st)
        scenes.append(sc)
        md.append((i + 1, s["line"], st, en, s["kind"], s["desc"], s["cam"], s["sfx"]))
    words = [{"text": w[0], "start": w[1], "end": w[2]} for l in TL["lines"] for w in l["words"]]
    sb = {
        "version": 1, "id": SLUG, "title": "Could Any Ocean Giant Actually Swallow You? (The Shoulder Test)", "format": "16:9", "fps": 30,
        "scenes": scenes,
        "captions": {"enabled": True, "words": words, "maxWords": 4, "maxChars": 22,
                     "glue": ["pizza box", "beach ball", "coffee mug", "red ring", "whale shark", "basking shark", "goliath grouper", "sperm whale", "blue whale",
                              "gill rakers", "flip-flops", "Isle of Harris", "Cape Cod", "Strait of Magellan", "forty-five centimetres"],
                     "style": {"font": "display", "fontSize": 67, "color": "#ffffff", "highlight": "#ff5a4a", "highlightMode": "none", "strokeWidth": 12, "uppercase": True, "y": 0.86}},
        "audio": {"voice": [{"src": f"episodes/{SLUG}/mix.wav", "start": 0, "volume": 1, "duration": TOTAL}],
                  "music": [
                      {"src": "music/deep_ocean.m4a", "start": 0, "end": round(L("U1")["start"], 2), "volume": 0.32, "fadeOut": 1.5},
                      {"src": "music/documentary_pulse.m4a", "start": round(L("U1")["start"] - 0.5, 2), "end": round(L("S1")["start"], 2), "volume": 0.3, "fadeIn": 1.0, "fadeOut": 1.5},
                      {"src": "music/deep_ocean.m4a", "start": round(L("S1")["start"] - 0.5, 2), "end": round(L("V1")["start"], 2), "volume": 0.22, "fadeIn": 1.5, "fadeOut": 1.0},
                      {"src": "music/dread.m4a", "start": round(L("V1")["start"] - 0.6, 2), "end": round(L("E1")["start"], 2), "volume": 0.3, "fadeIn": 1.2, "fadeOut": 1.2},
                      {"src": "music/deep_ocean.m4a", "start": round(L("E1")["start"] - 0.5, 2), "volume": 0.34, "fadeIn": 1.0, "fadeOut": 0.6}],
                  "sfx": [], "duckOn": "voice"},
        "overlays": {"grain": 0.04, "vignette": 0.2, "fadeIn": 0, "fadeOut": 0.4},
        "_built": {"by": "backlog/explainer/explainer-every-animal-that-could-swallow-you/gen_storyboard.py",
                   "timing": "Kokoro am_michael 0.96 per-line durations measured on the Spark CPU (durations.json -> timing.py)",
                   "voice": f"studio/public/episodes/{SLUG}/mix.wav (not built yet: run pipeline.audio.make on the Spark with these lines and pauses)",
                   "unbuilt_components": KIT_GAPS},
    }
    return sb, md


PRESET_KF = {  # camera presets as keyframes, so punch-ins can be added on top (keyframes override presets)
    "none": lambda d, a: [{"t": 0, "zoom": 1.0}, {"t": d, "zoom": 1.0}],
    "pushIn": lambda d, a: [{"t": 0, "zoom": 1.0}, {"t": d, "zoom": 1.0 + 0.12 * a}],
    "pullOut": lambda d, a: [{"t": 0, "zoom": 1.0 + 0.12 * a}, {"t": d, "zoom": 1.0}],
    "panLeft": lambda d, a: [{"t": 0, "x": 960 + 120 * a, "zoom": 1.06}, {"t": d, "x": 960 - 120 * a, "zoom": 1.06}],
    "panRight": lambda d, a: [{"t": 0, "x": 960 - 120 * a, "zoom": 1.06}, {"t": d, "x": 960 + 120 * a, "zoom": 1.06}],
    "drift": lambda d, a: [{"t": 0, "x": 940, "y": 530, "zoom": 1.04}, {"t": d, "x": 980, "y": 550, "zoom": 1.04}],
}


def _interp(kfs, t, key, default):
    pts = [(k["t"], k[key]) for k in kfs if key in k]
    if not pts:
        return default
    pts.sort()
    if t <= pts[0][0]:
        return pts[0][1]
    for (t0, v0), (t1, v1) in zip(pts, pts[1:]):
        if t0 <= t <= t1:
            return v0 + (v1 - v0) * ((t - t0) / max(1e-6, t1 - t0))
    return pts[-1][1]


def punch_ins(scene, st):
    """Depth Theory cadence (a visual change every 2-4 s): where nothing changes for > 3 s, add a small camera
    punch-in on the next sentence start inside that gap (or the midpoint)."""
    import importlib.util
    root = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
    sys.path.insert(0, root)
    from pipeline.episodes.common import visual_events
    cam = scene.get("camera") or {}
    if not cam.get("keyframes"):
        cam["keyframes"] = PRESET_KF.get(cam.get("preset", "none"), PRESET_KF["none"])(scene["duration"], cam.get("amount", 1.0))
        cam.pop("preset", None)
        cam.pop("amount", None)
    scene["camera"] = cam
    sent = []
    for l in TL["lines"]:
        prev = None
        for w in l["words"]:
            if prev is None or prev[0][-1:] in ".?!:":
                sent.append(round(w[1] - st, 2))
            prev = w
    flip = 1
    for _ in range(12):
        ev = visual_events(scene)
        gaps = [(a, b) for a, b in zip(ev, ev[1:]) if b - a > 3.0]
        if not gaps:
            break
        a, b = gaps[0]
        cands = [t for t in sent if a + 1.2 <= t <= b - 1.0]
        t = cands[0] if cands else round((a + b) / 2, 2)
        kfs = cam["keyframes"]
        z = _interp(kfs, t, "zoom", 1.0)
        x = _interp(kfs, t, "x", 960)
        y = _interp(kfs, t, "y", 540)
        k0 = {"t": round(max(0.0, t - 0.01), 2), "zoom": round(z, 3), "x": round(x, 1), "y": round(y, 1)}
        k1 = {"t": round(t + 0.25, 2), "zoom": round(z * (1.035 if flip > 0 else 1 / 1.035), 3), "x": round(x, 1), "y": round(y, 1), "ease": "out"}
        flip = -flip
        # every later keyframe keeps the new zoom ratio so the punch holds until the next beat
        ratio = k1["zoom"] / max(1e-6, z)
        for k in kfs:
            if k["t"] > k1["t"] and "zoom" in k:
                k["zoom"] = round(k["zoom"] * ratio, 3)
        kfs += [k0, k1]
        kfs.sort(key=lambda q: q["t"])
    return scene


def mmss(x):
    return f"{int(x // 60)}:{x % 60:04.1f}"


if __name__ == "__main__":
    sb, md = build()
    out = next((a for a in sys.argv[1:] if not a.startswith("--")), os.path.join(HERE, "storyboard.json"))
    json.dump(sb, open(out, "w"), indent=1, ensure_ascii=False)
    print(f"{out}: {len(sb['scenes'])} scenes, {sum(s['duration'] for s in sb['scenes']):.2f}s, {len(sb['captions']['words'])} caption words", file=sys.stderr)
    if "--md" in sys.argv:
        print("| # | Starts on (VO line) | t_start | t_end | Shot type | Visual (kit vocabulary; * = new figure) | Camera | SFX |")
        print("|---|---|---|---|---|---|---|---|")
        for n, line, st, en, kind, desc, cam, sfx in md:
            print(f"| {n} | {line} \"{' '.join(L(line)['text'].split()[:4])}…\" | {mmss(st)} | {mmss(en)} | {kind} | {desc} | {cam} | {sfx} |")
