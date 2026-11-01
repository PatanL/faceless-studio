"""Explainer episode scene builders (9:16). One function per episode; scene i = narration paragraph i.

Layout (1080x1920): picture zone y 10-62 %, captions at y 0.72, nothing important below 77 %.
Only explainer-kit components and core layers are used.
"""
from __future__ import annotations

from .common import comp, fade, pop, svg

W, H = 1080, 1920
RED = "#e5483d"

CAPTIONS = {"font": "display", "fontSize": 84, "color": "#ffffff", "highlight": "#ff5a4a", "highlightMode": "color",
            "strokeWidth": 12, "uppercase": True, "y": 0.72}
OVERLAYS = {"grain": 0.04, "vignette": 0.2, "fadeIn": 0, "fadeOut": 0.5}  # frame 0 is the Shorts cover: never black


def ocean(depth, **props):
    if "surface" in props:  # keep the sky dark navy (kit default is a pale sky)
        props = {"skyTop": "#071620", "skyBottom": "#1b3b4a", **props}
    return {"type": "component", "name": "explainer/Ocean", "depth": 0.12, "overscan": 1.2, "props": {"depth": depth, **props}}


def headline(t, at=0.15, y="15%", size=72, color="white", underline=True, **props):
    return comp("explainer/Headline", "50%", y, 1000, size * 3.2, {"text": t, "at": at, "size": size, "color": color,
                                                                 "underline": underline, **props}, depth=0, z=20)


def tag(t, at, x="50%", y="60%", size=40, accent=None, w=900, **props):
    p = {"text": t, "at": at, "size": size, **props}
    if accent:
        p["accent"] = accent
    return comp("explainer/Tag", x, y, w, size * 2.4, p, depth=0, z=20)


def stat(value, label, at, x="50%", y="58%", size=110, **props):
    return comp("explainer/Stat", x, y, 900, size * 2.6, {"value": value, "label": label, "at": at, "size": size, **props},
                depth=0, z=20)


def you(x, y, h=260, pose="stand", **kw):
    return comp("explainer/You", x, y, h * 0.6, h, {"pose": pose}, **kw)


def scene(sc, bg, layers, camera=None, trans=None, **kw):
    s = {"id": f"p{sc.i:02d}", "duration": sc.dur, "background": bg, "layers": layers, "notes": sc.text}
    if camera:
        s["camera"] = camera
    if trans:
        s["transitionIn"] = trans
    s.update(kw)
    return s


def push(a=0.6):
    return {"preset": "pushIn", "amount": a}


FADE = {"type": "fade", "duration": 0.3}
WHIP = {"type": "whip", "duration": 0.3, "direction": "left"}
DIP = {"type": "dipBlack", "duration": 0.35}

ICE = ('<svg viewBox="0 0 400 160" xmlns="http://www.w3.org/2000/svg"><path d="M10 70 L60 30 L170 22 L260 34 L390 60 '
       'L360 92 L40 96 Z" fill="#e8f3f6"/><path d="M40 96 L360 92 L330 150 L70 150 Z" fill="#9fc6d1" opacity="0.55"/></svg>')
SEAL = ('<svg viewBox="0 0 200 80" xmlns="http://www.w3.org/2000/svg"><path d="M10 60 Q40 20 110 26 Q160 30 186 44 '
        'Q196 52 184 58 Q150 70 90 66 Q40 70 10 60 Z" fill="#6f7f86"/><circle cx="170" cy="44" r="4" fill="#111"/>'
        '<path d="M60 64 L40 78 L70 70 Z" fill="#5c6b71"/></svg>')
HEART = ('<svg viewBox="0 0 200 180" xmlns="http://www.w3.org/2000/svg"><path d="M100 170 C20 110 0 70 20 35 C40 0 85 5 '
         '100 40 C115 5 160 0 180 35 C200 70 180 110 100 170 Z" fill="#c8453a"/><path d="M60 40 C70 30 85 32 92 44" '
         'stroke="#f08a7e" stroke-width="8" fill="none" stroke-linecap="round"/></svg>')
EYES = ('<svg viewBox="0 0 240 60" xmlns="http://www.w3.org/2000/svg"><ellipse cx="60" cy="38" rx="44" ry="16" fill="#3d4a2e"/>'
        '<ellipse cx="180" cy="38" rx="44" ry="16" fill="#3d4a2e"/><ellipse cx="60" cy="32" rx="16" ry="10" fill="#d9c25a"/>'
        '<ellipse cx="180" cy="32" rx="16" ry="10" fill="#d9c25a"/><rect x="57" y="23" width="6" height="18" fill="#111"/>'
        '<rect x="177" y="23" width="6" height="18" fill="#111"/></svg>')
GLOW = ('<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="g"><stop offset="0" '
        'stop-color="#d8fff6"/><stop offset="0.25" stop-color="#6ff0d8" stop-opacity="0.9"/><stop offset="1" '
        'stop-color="#6ff0d8" stop-opacity="0"/></radialGradient></defs><circle cx="100" cy="100" r="100" fill="url(#g)"/></svg>')
THUMB = ('<svg viewBox="0 0 300 420" xmlns="http://www.w3.org/2000/svg"><path d="M60 420 L60 140 Q60 30 150 30 Q240 30 240 140 '
         'L240 420 Z" fill="#e3b99a"/><path d="M85 150 Q85 70 150 70 Q215 70 215 150 L215 200 Q150 215 85 200 Z" '
         'fill="#f3d8c8" stroke="#c99a80" stroke-width="5"/></svg>')
FISH = ('<svg viewBox="0 0 220 90" xmlns="http://www.w3.org/2000/svg"><path d="M20 45 Q70 5 150 30 Q190 40 205 45 Q190 52 150 60 '
        'Q70 85 20 45 Z" fill="#e9d6df" opacity="0.85"/><path d="M20 45 L0 25 L6 45 L0 65 Z" fill="#e9d6df" opacity="0.7"/>'
        '<circle cx="178" cy="42" r="4" fill="#222"/></svg>')
BALL = ('<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"><circle cx="100" cy="100" r="96" fill="#f3f6f7"/>'
        '<path d="M100 4 A96 96 0 0 1 196 100 L100 100 Z" fill="#e5483d"/><path d="M100 196 A96 96 0 0 1 4 100 L100 100 Z" '
        'fill="#3a8fd6"/><circle cx="100" cy="100" r="14" fill="#fff"/></svg>')


# =========================================================================== orca (PILOT)

def orca(S):
    sc = []
    s = S[0]
    sc.append(scene(s, ocean(6, surface=0.2, rays=8, snow=60), [
        comp("explainer/Orca", "50%", "44%", 980, 340, {"speed": 1.1},
             keyframes=[{"t": 0, "x": "-40%"}, {"t": s.dur * 0.7, "x": "50%", "ease": "out"}]),
        headline("KILLER WHALE?", at=0.25, y="17%", size=84, color="white"),
        stat(0, "wild human kills", at=s.at("never", off=-0.1), y="60%", size=130, duration=0.3, color=RED),
    ], camera=push(0.5)))
    s = S[1]
    PPM = 105
    cars = [comp("explainer/Car", 180 + i * 240, "60%", 220, 110, {"color": c}, start=s.at("four", off=i * 0.15),
                 enter={"type": "drop", "at": s.at("four", off=i * 0.15), "duration": 0.35, "distance": 200}, depth=0.9)
            for i, c in enumerate(["#d8d8d8", "#c8453a", "#3a8fd6", "#e3b04b"])]
    sc.append(scene(s, ocean(30, rays=7), [
        comp("explainer/Orca", "50%", "35%", 1000, 360, {"pxPerM": PPM}, idle=[{"type": "bob", "amount": 6, "speed": 0.4}]),
        comp("explainer/ScaleBar", "50%", "46%", 8 * PPM, 140, {"label": "~8 M", "at": s.at("eight", off=-0.1), "labelSize": 48}),
        *cars,
        tag("≈ 6 TONNES", s.at("four", off=0.6), y="69%", size=36),
    ], camera=push(0.4), trans=FADE))
    s = S[2]
    sc.append(scene(s, ocean(20, rays=8), [
        comp("explainer/SpeedBars", "50%", "30%", 1000, 520, {
            "title": "Top speed", "max": 60, "at": 0.1, "stagger": 0.25, "duration": 0.7, "size": 44,
            "rows": [{"label": "Orca", "value": 56, "unit": "km/h", "color": "red"},
                     {"label": "Olympic swimmer", "value": 8, "unit": "km/h", "color": "#6fd6e8"},
                     {"label": "You", "value": 3, "unit": "km/h", "color": "#f3f6f7"}]}, depth=0),
        comp("explainer/Orca", "50%", "56%", 700, 240, {"speed": 1.8},
             keyframes=[{"t": 0, "x": "-40%"}, {"t": s.dur, "x": "140%", "ease": "linear"}]),
    ], trans=WHIP))
    s = S[3]
    sc.append(scene(s, ocean(60, rays=6), [
        comp("explainer/Orca", "30%", "30%", 520, 180, {"timeOffset": 0.0}, idle=[{"type": "float", "amount": 10, "speed": 0.3}]),
        comp("explainer/Orca", "68%", "41%", 600, 210, {"timeOffset": 0.6}, idle=[{"type": "float", "amount": 12, "speed": 0.25}]),
        comp("explainer/Orca", "38%", "52%", 440, 150, {"timeOffset": 1.1}, idle=[{"type": "float", "amount": 8, "speed": 0.35}]),
        headline("FAMILY POD", at=0.2, y="14%", size=70),
        tag("OWN CALLS", s.at("calls"), x="28%", y="63%", size=34, w=440),
        tag("OWN MENU", s.at("menu"), x="72%", y="63%", size=34, w=440),
        tag("OWN PLAN", s.at("plan"), x="50%", y="68%", size=34, w=440, accent=RED),
    ], camera={"preset": "drift"}, trans=FADE))
    s = S[4]
    ch = s.at("charges")
    wash = s.at("washes")
    sc.append(scene(s, ocean(4, surface=0.36, rays=9, snow=40), [
        svg(ICE, "72%", "36%", 420, 170, z=2),
        svg(SEAL, "74%", "31.5%", 200, 80, z=3,
            keyframes=[{"t": 0, "x": "74%", "y": "31.5%", "rotate": 0}, {"t": wash, "x": "74%", "y": "31.5%", "rotate": 0},
                       {"t": wash + 0.8, "x": "62%", "y": "40%", "rotate": -35, "ease": "in"}]),
        *[comp("explainer/Orca", "10%", f"{44 + i * 4}%", 460, 160, {"speed": 1.5, "timeOffset": i * 0.3}, z=1,
               keyframes=[{"t": 0, "x": "-30%"}, {"t": max(0.1, ch - 0.3), "x": "-25%"}, {"t": wash + 0.2, "x": f"{48 - i * 8}%", "ease": "inOut"}])
          for i in range(3)],
        tag("ANTARCTICA", 0.2, x="30%", y="12%", size=34, w=500),
    ], camera={"keyframes": [{"t": 0, "zoom": 1.0}, {"t": s.dur, "zoom": 1.08}],
               "shake": [{"at": wash, "duration": 0.6, "amplitude": 16}]}, trans=WHIP))
    s = S[5]
    sc.append(scene(s, ocean(120, rays=5), [
        comp("explainer/GreatWhite", "50%", "40%", 900, 320, {}, idle=[{"type": "float", "amount": 8, "speed": 0.3}]),
        tag("SOUTH AFRICA", 0.2, x="32%", y="12%", size=34, w=520),
        tag("LIVER: MISSING", s.at("liver", off=-0.1), y="58%", size=46, accent=RED),
    ], camera=push(0.6), trans=DIP))
    s = S[6]
    sc.append(scene(s, ocean(80, rays=6), [
        comp("explainer/GreatWhite", "60%", "36%", 640, 230, {"speed": 1.4}, flipX=True,
             keyframes=[{"t": 0, "x": "60%"}, {"t": s.dur, "x": "-40%", "ease": "in"}]),
        comp("explainer/GreatWhite", "85%", "50%", 520, 190, {"speed": 1.5, "timeOffset": 0.4}, flipX=True,
             keyframes=[{"t": 0, "x": "85%"}, {"t": s.dur, "x": "-30%", "ease": "in"}]),
        headline("GONE FOR MONTHS", at=s.at("fled*", off=-0.1), y="16%", size=70, color="red"),
    ], trans=FADE))
    s = S[7]
    PPM2 = 34
    sc.append(scene(s, ocean(40, rays=7), [
        comp("explainer/BlueWhale", "50%", "42%", 1000, 300, {"pxPerM": PPM2}, idle=[{"type": "bob", "amount": 5, "speed": 0.2}]),
        *[comp("explainer/Orca", "50%", "50%", 300, 110, {"pxPerM": PPM2, "speed": 1.4, "timeOffset": i * 0.5}, z=2,
               keyframes=[{"t": 0, "x": f"{-20 - i * 15}%", "y": f"{30 + i * 8}%"},
                          {"t": s.dur, "x": f"{70 - i * 18}%", "y": f"{34 + i * 9}%", "ease": "out"}])
          for i in range(3)],
        tag("2019 · WESTERN AUSTRALIA", s.at("Western", off=-0.1), y="13%", size=34),
        tag("ADULT BLUE WHALE", s.at("blue", off=-0.1), y="60%", size=40, accent=RED),
    ], camera=push(0.5), trans=WHIP))
    s = S[8]
    sc.append(scene(s, ocean(260, rays=3, snow=50), [
        you("50%", "46%", 280, "shrug", idle=[{"type": "float", "amount": 8, "speed": 0.3}]),
        headline("WHY NOT US?", at=s.at("Why", off=-0.1), y="22%", size=96, color="red"),
    ], camera=push(0.8), trans=DIP))
    s = S[9]
    items = ["We taste bad", "Too small to bother", "Culture"]
    sc.append(scene(s, ocean(200, rays=4), [
        comp("explainer/Options", "50%", "38%", 1000, 700, {"title": "Why not us?", "items": items, "at": 0.0, "stagger": 0.12,
                                                             "size": 56, "strikes": [{"index": 0, "at": s.at("Nobody's")},
                                                                                     {"index": 1, "at": s.at("They", off=0.2)}]}, depth=0),
    ], trans=FADE))
    s = S[10]
    sc.append(scene(s, ocean(150, rays=5), [
        comp("explainer/Options", "50%", "27%", 1000, 640, {"title": "Why not us?", "items": items, "at": -1, "stagger": 0,
                                                             "size": 56, "strikes": [{"index": 0, "at": -1}, {"index": 1, "at": -1}],
                                                             "select": {"index": 2, "at": s.at("culture", off=-0.1)}}, depth=0),
        comp("explainer/Orca", "44%", "54%", 560, 200, {"timeOffset": 0.2}, idle=[{"type": "float", "amount": 8, "speed": 0.3}]),
        comp("explainer/Orca", "66%", "58%", 280, 100, {"timeOffset": 0.9}, idle=[{"type": "float", "amount": 8, "speed": 0.3}],
             start=s.at("calf", off=-0.3), enter=pop(s.at("calf", off=-0.3))),
    ]))
    s = S[11]
    gib = {"lon": -6.0, "lat": 36.6}
    sc.append(scene(s, {"type": "color", "color": "#04121a"}, [
        comp("explainer/Map", "50%", "50%", 1080, 1920, {
            "views": [{"t": 0, "lon": -20, "lat": 40, "zoom": 1.6}, {"t": s.at("Spain"), "lon": -20, "lat": 40, "zoom": 1.6},
                      {"t": s.at("Spain", off=1.4), **gib, "zoom": 9}],
            "rings": [{**gib, "r": 1.2, "at": s.at("Spain", off=1.2), "label": "Iberian orcas"}]}, depth=0),
        tag("SINCE 2020", s.at("twenty*", off=0.2), x="50%", y="13%", size=40),
        stat(7, "boats sunk (and counting)", s.at("sunk", off=-0.2), y="62%", size=110, prefix="~", color=RED),
    ], trans=DIP, camera={"shake": [{"at": s.at("sunk"), "duration": 0.5, "amplitude": 14}]}))
    s = S[12]
    sc.append(scene(s, ocean(4, surface=0.3, rays=8, snow=50), [
        you("50%", "31%", 200, "wave", z=3),
        comp("explainer/Orca", "50%", "50%", 620, 210, {"speed": 0.8}, z=1,
             keyframes=[{"t": 0, "x": "120%", "y": "52%"}, {"t": s.dur * 0.5, "x": "50%", "y": "46%"},
                        {"t": s.dur, "x": "-20%", "y": "52%"}], flipX=True),
        tag("WHAT ARE THEY LEARNING?", s.at("What", off=-0.1), y="13%", size=40, accent=RED),
    ], camera=push(0.5), trans=FADE))
    return sc


# =========================================================================== blue whale

def blue_whale(S):
    sc = []
    s = S[0]
    # hook: true-scale head close-up (28 m whale = 3000 px, a 2.6 m diver = ~280 px), mouth open,
    # YOU drifts into the mouth on "inside", then gets pushed back out on "swallow".
    inside, nope = s.at("inside", off=-0.2), s.at("swallow", off=-0.1)
    diver_kf = [{"t": 0, "x": "16%", "y": "51%"}, {"t": inside + 1.4, "x": "38%", "y": "45%", "ease": "inOut"},
                {"t": nope, "x": "40%", "y": "45%"}, {"t": nope + 0.9, "x": "12%", "y": "50%", "rotate": -25, "ease": "out"}]
    sc.append(scene(s, ocean(30, rays=8), [
        comp("explainer/BlueWhale", "162%", "40%", 3000, 437,
             {"gape": [{"t": 0, "v": 0.55}, {"t": inside, "v": 0.85}, {"t": nope, "v": 0.85}, {"t": nope + 0.8, "v": 0.6}],
              "amp": 0.5}, flipX=True, z=1, idle=[{"type": "bob", "amount": 6, "speed": 0.2}]),
        comp("explainer/Diver", "8%", "50%", 280, 60, {"arms": "forward"}, z=3, keyframes=diver_kf),
        {**tag("YOU", 0.0, x="16%", y="46%", size=30, w=160, accent=RED), "depth": 1, "z": 4,
         "keyframes": [{**k, "y": f"{float(k['y'][:-1]) - 4.5}%", "rotate": 0} for k in diver_kf]},
        headline("FITS IN ITS MOUTH", at=0.0, y="14%", size=74, out=s.at("still", off=-0.1)),
        headline("CAN'T SWALLOW YOU", at=s.at("couldn't", off=-0.1), y="14%", size=74, color="red"),
    ], camera={"keyframes": [{"t": 0, "zoom": 1.12, "x": "45%", "y": "48%"}, {"t": s.dur, "zoom": 1.0, "x": "50%", "y": "50%"}]}))
    s = S[1]
    PPM = 34
    sc.append(scene(s, ocean(60, rays=7), [
        comp("explainer/BlueWhale", "50%", "34%", 30 * PPM, 300, {"pxPerM": PPM * 30 / 28},
             keyframes=[{"t": 0, "x": "130%"}, {"t": 1.6, "x": "50%", "ease": "out"}]),
        headline("HEAVIEST ANIMAL EVER", at=s.at("heaviest", off=-0.1), y="14%", size=64, out=s.at("two", off=-0.2)),
        comp("explainer/ScaleBar", "50%", "44%", 30 * PPM, 140, {"label": "~30 M", "at": s.at("thirty", off=-0.1)}),
        comp("explainer/Bus", "28%", "56%", 12 * PPM, 140, {"pxPerM": PPM}, start=s.at("two"),
             enter={"type": "slideRight", "at": s.at("two"), "duration": 0.4}),
        comp("explainer/Bus", "66%", "56%", 12 * PPM, 140, {"pxPerM": PPM}, start=s.at("half", off=-0.1),
             enter={"type": "slideRight", "at": s.at("half", off=-0.1), "duration": 0.4}),
        comp("explainer/Bus", "91%", "56%", 6 * PPM, 140, {"pxPerM": PPM}, start=s.at("nose"),
             enter={"type": "slideRight", "at": s.at("nose"), "duration": 0.4}, opacity=0.8),
        headline("2.5 CITY BUSES", at=s.at("two", off=0.3), y="14%", size=66),
    ], camera=push(0.3), trans=FADE))
    s = S[2]
    sc.append(scene(s, ocean(80, rays=6), [
        comp("explainer/BlueWhale", "50%", "36%", 1300, 400, {}, idle=[{"type": "bob", "amount": 5, "speed": 0.25}]),
        stat(190, "tonnes", s.at("two", off=-0.2), y="58%", size=130, prefix="~", duration=1.2, color=RED),
        tag("HEAVIER THAN ANY DINOSAUR WE'VE FOUND", s.at("Heavier"), y="14%", size=32),
    ], camera=push(0.7), trans=WHIP))
    s = S[3]
    sc.append(scene(s, ocean(50, rays=7), [
        comp("explainer/Elephant", "50%", "40%", 620, 560, {}, start=s.at("elephant", off=-0.5),
             enter={"type": "drop", "at": s.at("elephant", off=-0.5), "duration": 0.4, "distance": 300}),
        headline("THE TONGUE ALONE", at=0.2, y="14%", size=70, color="red"),
        tag("≈ 2.7 TONNES", s.at("elephant"), y="62%", size=40),
    ], trans=FADE))
    s = S[4]
    beats = [0.4 + k * 1.6 for k in range(int(s.dur / 1.6))]
    slow = s.at("two", off=0)
    sc.append(scene(s, ocean(400, rays=2, snow=40), [
        svg(HEART, "50%", "36%", 460, 420, idle=[{"type": "pulse", "amount": 0.05, "speed": 0.8}],
            keyframes=[{"t": 0, "scale": 0.6, "opacity": 0}, {"t": 0.4, "scale": 1, "opacity": 1, "ease": "backOut"}]),
        tag("≈ GOLF-CART SIZED", s.at("golf", off=-0.1), y="13%", size=38),
        stat(2, "beats a minute on a dive", slow, y="60%", size=130, color=RED, duration=0.3),
    ], camera={"preset": "pushIn", "amount": 0.6,
               "shake": [{"at": b, "duration": 0.18, "amplitude": 6} for b in beats if b < slow]}, trans=DIP))
    s = S[5]
    gulp = s.at("gulp", off=-0.2)
    sc.append(scene(s, ocean(25, rays=9), [
        {"type": "particles", "preset": "dust", "count": 240, "color": "rgba(255,150,140,0.75)", "size": [3, 7], "speed": 0.5,
         "x": "60%", "y": "40%", "width": 1100, "height": 900, "z": 2},
        comp("explainer/BlueWhale", "25%", "34%", 1500, 220, {"speed": 1.3, "gape": [{"t": gulp, "v": 0}, {"t": gulp + 0.7, "v": 1, "ease": "out"}]},
             z=1, keyframes=[{"t": 0, "x": "-80%"}, {"t": gulp + 0.4, "x": "25%", "ease": "out"}]),
        tag("KRILL", s.at("krill", off=-0.1), x="75%", y="14%", size=38, w=320),
        headline("ONE GULP > ITS OWN BODY", at=gulp, y="58%", size=54, color="red", underline=False),
    ], trans=WHIP))
    s = S[6]
    sc.append(scene(s, ocean(25, rays=8), [
        {"type": "particles", "preset": "dust", "count": 260, "color": "rgba(255,150,140,0.7)", "size": [3, 6], "speed": 0.6, "z": 1},
        comp("explainer/BlueWhale", "25%", "30%", 1500, 220,
             {"speed": 0.8, "gape": [{"t": 0, "v": 1}, {"t": s.at("squeezes", off=-0.1), "v": 1},
                                     {"t": s.at("food", end=True), "v": 0.25, "ease": "inOut"}]}, z=2),
        tag("BALEEN = SIEVE", s.at("baleen", off=-0.1), x="62%", y="14%", size=38, w=560),
        stat(40000000, "krill in a single day", s.at("Up", off=-0.1), y="58%", size=104, duration=1.6),
    ], trans=FADE))
    s = S[7]
    sc.append(scene(s, ocean(25, rays=8), [
        {"type": "particles", "preset": "dust", "count": 260, "color": "rgba(255,150,140,0.7)", "size": [3, 6], "speed": 0.5, "z": 1},
        comp("explainer/Diver", "50%", "44%", 640, 140, {"arms": "forward"}, z=3, idle=[{"type": "float", "amount": 10, "speed": 0.4}]),
        headline("AND YOU?", at=s.at("you", off=-0.1), y="18%", size=100, color="red"),
    ], camera=push(1.0), trans=DIP))
    s = S[8]
    sc.append(scene(s, ocean(40, rays=7), [
        svg(BALL, "34%", "40%", 330, 330, start=s.at("beach", off=-0.2), enter=pop(s.at("beach", off=-0.2))),
        you("70%", "40%", 420, "stand"),
        tag("THROAT ≈ BEACH BALL", s.at("throat"), y="14%", size=40),
        headline("✕", at=s.at("Anything"), y="40%", size=220, color="red", underline=False),
    ], trans=FADE))
    s = S[9]
    turn = s.at("turn", off=-0.4)
    sc.append(scene(s, ocean(30, rays=8), [
        comp("explainer/Diver", "50%", "36%", 420, 92, {"arms": "forward"}, z=3,
             keyframes=[{"t": turn, "x": "50%", "y": "36%", "rotate": 0}, {"t": turn + 1.2, "x": "14%", "y": "26%", "rotate": -200, "ease": "out"}]),
        comp("explainer/BlueWhale", "50%", "44%", 2400, 350, {"speed": 1.2}, z=1, flipX=True,
             keyframes=[{"t": 0, "x": "160%"}, {"t": turn + 0.6, "x": "50%", "ease": "inOut"}, {"t": s.dur, "x": "-60%"}]),
        headline("BEING IN THE WAY", at=s.at("being", off=-0.1), y="14%", size=66, color="red"),
    ], camera={"shake": [{"at": turn + 0.4, "duration": 0.8, "amplitude": 22}]}, trans=WHIP))
    s = S[10]
    # bookend: the hook framing again (same true-scale head close-up, mouth open, YOU outside it)
    end_kf = [{"t": 0, "x": "16%", "y": "51%"}, {"t": s.dur, "x": "20%", "y": "50%"}]
    sc.append(scene(s, ocean(30, rays=8), [
        comp("explainer/BlueWhale", "162%", "40%", 3000, 437, {"gape": [{"t": 0, "v": 0.3}, {"t": 2.5, "v": 0.7}], "amp": 0.5},
             flipX=True, z=1, idle=[{"type": "bob", "amount": 6, "speed": 0.2}]),
        comp("explainer/Diver", "16%", "51%", 280, 60, {"arms": "forward"}, z=3, keyframes=end_kf),
        {**tag("YOU", 0.0, x="16%", y="46.5%", size=30, w=160, accent=RED), "depth": 1, "z": 4,
         "keyframes": [{**k, "y": f"{float(k['y'][:-1]) - 4.5}%"} for k in end_kf]},
        headline("NEVER DOWN ITS THROAT", at=s.at("never", off=-0.1), y="14%", size=64, out=s.at("Which", off=-0.2)),
        tag("WHO SHOULD I PUT YOU NEXT TO?", s.at("Which", off=-0.1), y="13%", size=36, accent=RED),
    ], camera=push(0.4), trans=FADE))
    return sc


# =========================================================================== pressure ladder

def _depth_scene(s, d_from, d_to, layers, label_at=None, trans=FADE, rays=6, zones=None, camera=None):
    track = [{"t": 0, "v": d_from}, {"t": min(s.dur, 2.2), "v": d_to, "ease": "out"}]
    meter = comp("explainer/DepthMeter", "88%", "40%", 260, 1100,
                 {"depth": track, "window": max(40, d_to * 0.6), "step": _nice_step(d_to), "size": 40,
                  **({"zones": zones} if zones else {})}, depth=0, z=10)
    return scene(s, ocean(track, rays=rays, snow=70), layers + [meter], camera=camera or push(0.4), trans=trans)


def _nice_step(d):
    for st in (5, 10, 50, 100, 500, 1000, 2000):
        if d * 0.6 / st <= 6:
            return st
    return 5000


def pressure(S):
    sc = []
    s = S[0]
    sc.append(scene(s, ocean(2, surface=0.3, rays=9), [
        you("45%", "31%", 200, "wave", idle=[{"type": "bob", "amount": 6, "speed": 0.5}],
            keyframes=[{"t": 0, "y": "31%"}, {"t": s.at("Let's"), "y": "31%"}, {"t": s.dur, "y": "44%", "ease": "in"}]),
        headline("HOW DEEP CAN YOU GO?", at=0.25, y="14%", size=66),
        tag("+1 SKY OF PRESSURE / 10 M", s.at("sky's", off=-0.2), y="60%", size=38, accent=RED),
    ], camera=push(0.4)))
    s = S[1]
    sc.append(_depth_scene(s, 0, 10, [
        comp("explainer/Diver", "42%", "36%", 700, 140, {"bubbles": True}),
        {"type": "circle", "x": "30%", "y": "52%", "width": 150, "height": 150, "fill": "#f08a7e", "opacity": 0.8,
         "keyframes": [{"t": 0, "scale": 1}, {"t": s.at("half", off=0.1), "scale": 1}, {"t": s.at("half", off=0.8), "scale": 0.7}]},
        {"type": "circle", "x": "52%", "y": "52%", "width": 150, "height": 150, "fill": "#f08a7e", "opacity": 0.8,
         "keyframes": [{"t": 0, "scale": 1}, {"t": s.at("half", off=0.1), "scale": 1}, {"t": s.at("half", off=0.8), "scale": 0.7}]},
        tag("LUNGS: 1/2", s.at("half"), x="41%", y="62%", size=36, w=500),
        stat(2, "x surface pressure", s.at("doubled", off=-0.2), x="42%", y="18%", size=100, suffix="x", duration=0.3),
    ], trans=None))
    s = S[2]
    sc.append(_depth_scene(s, 10, 30, [
        you("42%", "38%", 300, "shrug", idle=[{"type": "sway", "amount": 10, "speed": 0.6}]),
        tag("RAPTURE OF THE DEEP", s.at("rapture", off=-0.1), x="42%", y="58%", size=38, w=720, accent=RED),
    ], camera={"preset": "drift", "amount": 1.5}))
    s = S[3]
    sc.append(_depth_scene(s, 30, 100, [
        comp("explainer/Diver", "42%", "36%", 640, 130, {"arms": "side"}),
        stat(11, "x surface pressure", s.at("Eleven", off=-0.2), x="42%", y="54%", size=120, suffix="x", duration=0.6),
        tag("FREE DIVERS: ONE BREATH", s.at("Free"), x="42%", y="14%", size=34, w=720),
    ]))
    s = S[4]
    sc.append(_depth_scene(s, 100, 332, [
        comp("explainer/Diver", "42%", "34%", 640, 130, {"torch": True, "beam": 300}),
        tag("SCUBA RECORD · 332 M", 0.3, x="42%", y="14%", size=36, w=720),
        stat(12, "minutes down", s.at("Minutes", off=-0.2), x="30%", y="54%", size=96, prefix="~", duration=0.6),
        stat(15, "hours back up", s.at("fifteen", off=-0.2), x="30%", y="64%", size=96, prefix="~", duration=0.6, color=RED),
    ], rays=4))
    s = S[5]
    sc.append(_depth_scene(s, 332, 1000, [
        svg(GLOW, "30%", "44%", 140, 140, start=s.at("light", off=-0.2), enter=fade(s.at("light", off=-0.2), 0.8),
            idle=[{"type": "pulse", "amount": 0.2, "speed": 0.7}]),
        comp("explainer/Anglerfish", "36%", "46%", 360, 230, {}, start=s.at("animals", off=-0.2),
             enter=fade(s.at("animals", off=-0.2), 1.0), idle=[{"type": "bob", "amount": 8, "speed": 0.5}]),
        headline("NO MORE SUNLIGHT", at=s.at("sunlight", off=-0.1), y="16%", size=66, color="red"),
    ], trans=DIP, rays=2))
    s = S[6]
    sc.append(_depth_scene(s, 1000, 2000, [
        comp("explainer/SpermWhale", "40%", "38%", 1200, 360, {"speed": 0.8},
             keyframes=[{"t": 0, "x": "130%"}, {"t": s.dur, "x": "-10%", "ease": "linear"}], flipX=True),
        tag("WHALE: 60+ MIN", s.at("hour", off=-0.5), x="30%", y="56%", size=36, w=520),
        tag("YOU: ~2 MIN", s.at("two"), x="30%", y="63%", size=36, w=520, accent=RED),
    ], rays=1))
    s = S[7]
    sc.append(_depth_scene(s, 2000, 3800, [
        headline("TITANIC DEPTH", at=s.at("Titanic", off=-0.1), y="15%", size=70),
        stat(390, "kg on every cm² of you", s.at("grand", off=-0.3), x="42%", y="44%", size=120, prefix="~", duration=1.0, color=RED),
        tag("≈ A GRAND PIANO", s.at("piano", off=-0.1), x="42%", y="60%", size=38, w=640),
    ], rays=0))
    s = S[8]
    sc.append(scene(s, {"type": "color", "color": "#04121a"}, [
        comp("explainer/Map", "50%", "50%", 1080, 1920, {
            "views": [{"t": 0, "lon": 150, "lat": 15, "zoom": 1.4}, {"t": min(s.dur - 0.5, 2.0), "place": "marianaTrench", "zoom": 10}],
            "rings": [{"place": "marianaTrench", "r": 0.8, "at": 1.6, "label": "Challenger Deep"}]}, depth=0),
        stat(10900, "metres down", 0.3, y="14%", size=90, duration=1.4),
        stat(1086, "bar of pressure", s.at("thousand", off=-0.2), y="62%", size=110, duration=0.8, color=RED),
    ], trans=DIP))
    s = S[9]
    car_at = s.at("car", off=-0.3)
    sc.append(scene(s, ocean(10900, rays=0, snow=50), [
        svg(THUMB, "50%", "52%", 360, 504),
        comp("explainer/Car", "50%", "36%", 420, 200, {"color": "#c8453a"}, start=car_at,
             enter={"type": "drop", "at": car_at, "duration": 0.35, "distance": 600}),
        tag("≈ 1.1 TONNES / CM²", s.at("thumbnail"), y="14%", size=40, accent=RED),
    ], camera={"shake": [{"at": car_at + 0.35, "duration": 0.5, "amplitude": 20}]}, trans=FADE))
    s = S[10]
    sc.append(scene(s, ocean(8300, rays=0, snow=90, drift=0.4), [
        svg(FISH, "50%", "42%", 360, 150, keyframes=[{"t": 0, "x": "30%"}, {"t": s.dur, "x": "65%", "ease": "linear"}],
            idle=[{"type": "bob", "amount": 10, "speed": 0.3}]),
        tag("8,336 M · FISH FILMED", s.at("filmed", off=-0.2), y="14%", size=38),
    ], camera=push(0.6), trans=DIP))
    s = S[11]
    sc.append(scene(s, ocean(2, surface=0.3, rays=9), [
        you("50%", "31%", 220, "wave", idle=[{"type": "bob", "amount": 6, "speed": 0.5}]),
        stat(27, "people at the very bottom", 0.2, x="50%", y="47%", size=96, prefix="~", duration=0.6, color=RED),
        stat(600, "people in space", s.at("space", off=-0.3), x="50%", y="60%", size=96, suffix="+", duration=0.6),
        tag("WHERE WOULD YOU TURN AROUND?", s.at("Comment", off=-0.1), y="13%", size=36),
    ], camera=push(0.4), trans=FADE))
    return sc


# =========================================================================== saltwater crocodile

def croc(S):
    sc = []
    s = S[0]
    sc.append(scene(s, ocean(2, surface=0.42, rays=8), [
        you("30%", "41%", 180, "wave", idle=[{"type": "bob", "amount": 6, "speed": 0.5}]),
        svg(EYES, "72%", "41.5%", 180, 45, start=s.at("worry", off=-0.6), enter=fade(s.at("worry", off=-0.6), 0.8)),
        headline("THE WATER LOOKS EMPTY", at=0.3, y="15%", size=60),
    ], camera={"keyframes": [{"t": 0, "zoom": 1.0}, {"t": s.dur, "zoom": 1.12, "x": "60%"}]}))
    s = S[1]
    PPM = 150
    sc.append(scene(s, ocean(10, rays=7), [
        comp("explainer/Crocodile", "50%", "36%", 1000, 300, {"pxPerM": PPM}),
        comp("explainer/ScaleBar", "50%", "45%", 6 * PPM, 140, {"label": "6 M+", "at": s.at("six", off=-0.1)}),
        you("85%", "54%", 1.75 * PPM, "stand"),
        stat(1, "tonne", s.at("tonne", off=-0.4), x="35%", y="58%", size=110, duration=0.3, color=RED),
    ], camera=push(0.4), trans=FADE))
    s = S[2]
    sc.append(scene(s, {"type": "color", "color": "#04121a"}, [
        comp("explainer/Map", "50%", "50%", 1080, 1920, {
            "views": [{"t": 0, "lon": 140, "lat": -12, "zoom": 3.0}, {"t": s.dur, "lon": 145, "lat": -10, "zoom": 3.6}],
            "pins": [{"lon": 131, "lat": -12.4, "label": "N. Australia", "at": 0.3},
                     {"lon": 160, "lat": -9.4, "label": "Solomon Is.", "at": s.at("islands", off=-0.6)}],
            "highlight": ["australia"]}, depth=0),
        tag("590 KM IN 25 DAYS (ONE TAGGED CROC)", s.at("hundreds", off=-0.1), y="13%", size=32, accent=RED),
    ], trans=WHIP))
    s = S[3]
    sc.append(scene(s, ocean(8, surface=0.25, rays=7), [
        comp("explainer/Crocodile", "50%", "46%", 900, 260, {}, idle=[{"type": "float", "amount": 6, "speed": 0.2}]),
        stat(60, "minutes underwater", s.at("hour", off=-0.4), y="15%", size=110, suffix="+", duration=0.8, color=RED),
        svg(EYES, "62%", "25%", 160, 40, start=s.at("eyes", off=-0.2), enter=fade(s.at("eyes", off=-0.2))),
    ], camera=push(0.5), trans=FADE))
    s = S[4]
    snap = s.at("closes", off=0.1)
    sc.append(scene(s, ocean(20, rays=6), [
        comp("explainer/Crocodile", "50%", "38%", 1200, 380, {"jaw": 32, "idle": False}, end=snap),
        comp("explainer/Crocodile", "50%", "38%", 1200, 380, {"jaw": 0}, start=snap),
        stat(16400, "newtons: strongest bite measured", s.at("strongest", off=-0.2), y="58%", size=104, duration=0.9, color=RED),
        tag("CRACKS TURTLE SHELLS", s.at("turtle*", off=-0.2), y="13%", size=38),
    ], camera={"preset": "pushIn", "amount": 0.6, "shake": [{"at": snap + 0.12, "duration": 0.4, "amplitude": 24}]}, trans=WHIP))
    s = S[5]
    sc.append(scene(s, ocean(60, rays=3), [
        comp("explainer/Crocodile", "50%", "40%", 900, 270, {}, idle=[{"type": "spin", "speed": 0.5}]),
        you("50%", "60%", 160, "panic", idle=[{"type": "spin", "speed": 0.5}]),
        headline("WHICH WAY IS UP?", at=s.at("which", off=-0.1), y="15%", size=62, color="red"),
    ], camera=push(0.8), trans=DIP))
    opts = ["Swim for the shore", "Run zigzag", "Play dead", "Stay off the water's edge"]

    def opt_scene(s, strikes, select=None, title_at=0.0, trans=FADE):
        p = {"title": "Your options", "items": opts, "at": title_at, "stagger": 0.12 if title_at >= 0 else 0, "size": 46,
             "strikes": strikes}
        if select:
            p["select"] = select
        return scene(s, ocean(30, rays=6), [comp("explainer/Options", "50%", "36%", 1000, 760, p, depth=0)], trans=trans)

    s = S[6]
    sc.append(opt_scene(s, [{"index": 0, "at": s.at("faster", off=0.1)}]))
    s = S[7]
    sc.append(opt_scene(s, [{"index": 0, "at": -1}, {"index": 1, "at": s.at("myth")}], title_at=-1, trans=None))
    s = S[8]
    sc.append(opt_scene(s, [{"index": 0, "at": -1}, {"index": 1, "at": -1}, {"index": 2, "at": s.at("drag", off=-0.3)}],
                        title_at=-1, trans=None))
    s = S[9]
    sc.append(opt_scene(s, [{"index": i, "at": -1} for i in range(3)], select={"index": 3, "at": s.at("Stay", off=-0.1)},
                        title_at=-1, trans=None))
    s = S[10]
    sc.append(scene(s, ocean(3, surface=0.4, rays=7), [
        you("70%", "36%", 200, "stand"),
        comp("explainer/Crocodile", "30%", "47%", 640, 190, {"silhouette": True}, opacity=0.85,
             idle=[{"type": "float", "amount": 4, "speed": 0.15}]),
        tag("IT LEARNS YOUR ROUTINE", s.at("learned", off=-0.1), y="14%", size=40, accent=RED),
    ], camera={"keyframes": [{"t": 0, "zoom": 1.0, "x": "50%"}, {"t": s.dur, "zoom": 1.15, "x": "40%"}]}, trans=DIP))
    s = S[11]
    sc.append(scene(s, ocean(2, surface=0.42, rays=8), [
        svg(EYES, "60%", "41.5%", 180, 45, idle=[{"type": "pulse", "amount": 0.05, "speed": 0.2}]),
        headline("EMPTY = IT'S WORKING", at=s.at("Empty", off=-0.1), y="15%", size=60, color="red"),
        tag("SEEN CROC SIGNS? WHERE?", s.at("Ever", off=-0.1), y="60%", size=36),
    ], camera=push(0.5), trans=FADE))
    return sc


# =========================================================================== anglerfish

def anglerfish(S):
    sc = []
    s = S[0]
    sc.append(scene(s, ocean(1000, rays=0, snow=60), [
        comp("explainer/Diver", "42%", "44%", 480, 95, {"arms": "forward"}, idle=[{"type": "float", "amount": 8, "speed": 0.3}]),
        svg(GLOW, "74%", "36%", 120, 120, idle=[{"type": "pulse", "amount": 0.25, "speed": 0.6}]),
        headline("DON'T.", at=s.at("don't", off=-0.1), y="16%", size=120, color="red"),
    ], camera={"keyframes": [{"t": 0, "zoom": 1.0, "x": "45%"}, {"t": s.dur, "zoom": 1.1, "x": "58%"}]}))
    s = S[1]
    sc.append(scene(s, ocean(1000, rays=0, snow=110, drift=0.5), [
        svg(GLOW, "50%", "36%", 160, 160, idle=[{"type": "pulse", "amount": 0.25, "speed": 0.6}]),
        comp("explainer/DepthMeter", "88%", "40%", 260, 1000, {"depth": 1000, "window": 600, "step": 100, "size": 40}, depth=0),
        tag("NO SUNLIGHT", 0.3, y="14%", size=40),
    ], camera=push(0.5), trans=FADE))
    s = S[2]
    sc.append(scene(s, ocean(1100, rays=0, snow=60), [
        comp("explainer/Anglerfish", "50%", "40%", 800, 520, {}, start=s.at("anglerfish*", off=-0.4),
             enter=fade(s.at("anglerfish*", off=-0.4), 0.9), idle=[{"type": "bob", "amount": 8, "speed": 0.4}]),
        headline("IT'S BAIT", at=s.at("bait", off=-0.1), y="15%", size=90, color="red"),
        tag("ROD = FIN SPINE", s.at("spine", off=-0.3), y="62%", size=40),
    ], camera=push(0.5), trans=FADE))
    s = S[3]
    sc.append(scene(s, ocean(1100, rays=0, snow=40), [
        comp("explainer/Anglerfish", "30%", "60%", 1200, 780, {}),
        {"type": "particles", "preset": "dust", "count": 90, "color": "rgba(120,255,220,0.9)", "size": [3, 6], "speed": 0.4,
         "x": "84%", "y": "40%", "width": 300, "height": 300, "z": 4},
        tag("BACTERIA", s.at("bacteria", off=-0.1), x="60%", y="18%", size=44, w=420, accent=RED),
    ], camera={"keyframes": [{"t": 0, "zoom": 1.0}, {"t": s.dur, "zoom": 1.2, "x": "62%", "y": "44%"}]}, trans=WHIP))
    s = S[4]
    up = s.at("scale", off=0)
    sc.append(scene(s, ocean(1100, rays=0, snow=50), [
        you("72%", "44%", 360, "stand"),
        comp("explainer/Anglerfish", "36%", "44%", 600, 400, {}, keyframes=[{"t": 0, "scale": 0.18}, {"t": up, "scale": 0.18},
                                                                            {"t": up + 1.4, "scale": 1.0, "ease": "backOut"}]),
        tag("REAL SIZE: SMALLER THAN YOUR HAND", 0.3, y="14%", size=32),
    ], camera={"shake": [{"at": up + 1.3, "duration": 0.4, "amplitude": 14}]}, trans=DIP))
    s = S[5]
    sc.append(scene(s, ocean(1100, rays=0, snow=40), [
        comp("explainer/Anglerfish", "50%", "42%", 1100, 720, {}),
        headline("ONE-WAY DOOR", at=s.at("one-way", off=-0.1), y="14%", size=76, color="red"),
    ], camera=push(0.9), trans=FADE))
    s = S[6]
    sc.append(scene(s, ocean(1100, rays=0, snow=40), [
        comp("explainer/Anglerfish", "50%", "40%", 900, 600, {}, idle=[{"type": "breathe", "amount": 0.06, "speed": 0.5}]),
        stat(2, "x its own length", s.at("twice", off=-0.2), y="60%", size=130, suffix="x", duration=0.3, color=RED),
    ], trans=FADE))
    s = S[7]
    car_at = s.at("car", off=-0.3)
    sc.append(scene(s, ocean(1100, rays=0, snow=40), [
        comp("explainer/Anglerfish", "44%", "38%", 900, 600, {}),
        comp("explainer/Car", "60%", "58%", 520, 240, {"color": "#3a8fd6"}, start=car_at,
             enter={"type": "drop", "at": car_at, "duration": 0.35, "distance": 400}),
        tag("AT YOUR SIZE", 0.2, y="14%", size=40),
    ], camera={"shake": [{"at": s.at("bite", off=0.1), "duration": 0.4, "amplitude": 20}]}, trans=WHIP))
    s = S[8]
    sc.append(scene(s, ocean(1500, rays=0, snow=50), [
        headline("NOT EVEN THE STRANGEST PART", at=0.1, y="36%", size=70, color="red"),
    ], camera=push(1.0), trans=DIP))
    s = S[9]
    bite = s.at("bites", off=0)
    sc.append(scene(s, ocean(1500, rays=0, snow=50), [
        comp("explainer/Anglerfish", "40%", "40%", 800, 520, {}),
        comp("explainer/Anglerfish", "90%", "46%", 110, 72, {"speed": 1.6}, z=3,
             keyframes=[{"t": 0, "x": "110%", "y": "30%"}, {"t": bite, "x": "62%", "y": "46%", "ease": "out"}]),
        tag("MALE", s.at("males", off=-0.1), x="78%", y="58%", size=34, w=260),
        tag("NEVER LETS GO", s.at("never", off=-0.1), y="14%", size=40, accent=RED),
    ], camera={"shake": [{"at": bite, "duration": 0.3, "amplitude": 10}]}, trans=FADE))
    s = S[10]
    sc.append(scene(s, ocean(1500, rays=0, snow=50), [
        comp("explainer/Anglerfish", "40%", "40%", 800, 520, {}),
        comp("explainer/Anglerfish", "62%", "46%", 110, 72, {"silhouette": "#2b3036"}, z=3,
             keyframes=[{"t": 0, "opacity": 1}, {"t": s.dur, "opacity": 0.25}]),
        tag("SHARED BLOOD", s.at("blood", off=-0.2), y="14%", size=40, accent=RED),
        tag("EYES · ORGANS: GONE", s.at("eyes", off=-0.1), y="60%", size=36),
    ], camera=push(0.7), trans=FADE))
    s = S[11]
    males = [comp("explainer/Anglerfish", f"{30 + (i % 4) * 14}%", f"{50 + (i // 4) * 6}%", 90, 60, {"silhouette": "#2b3036", "timeOffset": i * 0.3},
                  start=s.at("eight", off=-0.4 + i * 0.08), enter=pop(s.at("eight", off=-0.4 + i * 0.08)), z=3) for i in range(8)]
    sc.append(scene(s, ocean(1500, rays=0, snow=50), [
        comp("explainer/Anglerfish", "50%", "34%", 760, 500, {}),
        *males,
        stat(8, "males on one female", s.at("eight", off=-0.2), y="64%", size=110, duration=0.4, color=RED),
    ], trans=WHIP))
    s = S[12]
    sc.append(scene(s, ocean(1000, rays=0, snow=60), [
        svg(GLOW, "50%", "38%", 160, 160, idle=[{"type": "pulse", "amount": 0.25, "speed": 0.6}]),
        tag("WHO SHOULD I SCALE UP NEXT?", s.at("Which", off=-0.1), y="60%", size=36, accent=RED),
        headline("DON'T SWIM TOWARD IT", at=0.2, y="15%", size=62),
    ], camera=push(0.6), trans=DIP))
    return sc


EPISODES = {
    "explainer-orca": orca,
    "explainer-blue-whale": blue_whale,
    "explainer-pressure-ladder": pressure,
    "explainer-saltwater-croc": croc,
    "explainer-anglerfish": anglerfish,
}
