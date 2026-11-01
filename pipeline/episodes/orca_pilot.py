"""explainer-orca (PILOT) scene builder, fix round 2 (reviewer 5/10 -> fixes 1-10).

One narration paragraph = one scene (14 paragraphs). Every beat is anchored to narration words (Scene.at), every
scene gets an explicit camera with punch-ins (Cam), and build.py fails the episode on any visual hold > 3 s.

Visual grammar: YOU is always the hook's diver (white YOU chip). Red is the threat accent only. Orcas appear in
side, head-on (pose "head") and top-down (pose "top") views. Frame 0 is the Shorts cover and the last frame
returns to it exactly (same orca x, diver, headline, zoom 1.0) so the loop replays seamlessly.
"""
from __future__ import annotations

from . import explainer_eps as E
from .common import comp, pop, svg

H = 1920
RED, CYAN = E.RED, E.CYAN
CUT = None
FADE, WHIP, DIP = E.FADE, E.WHIP, E.DIP

PPM0 = 100                         # hook / bookend: orca and diver share pxPerM (honest you-vs-it scale)
HOOK_ORCA = ("46%", "35%")         # orca fully in frame at frame 0 (left edge ~97 px)
HOOK_DIVER = ("76%", "52.5%")
HOOK_CHIP = ("76%", "47.2%")
HOOK_SPEED = 1.1
ORCA_PERIOD = 1 / (0.6 * HOOK_SPEED)   # swim-wave period of the hook orca (marine.tsx orca freq 0.6 * speed)

# a broad swell that rises out of the waterline (y=200 of 300) and curls over toward the right
WAVE = ('<svg viewBox="0 0 900 300" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none"><path d="M0 300 L0 200 '
        'C 200 196 380 170 520 120 C 600 92 660 70 720 76 C 760 80 790 100 800 128 C 770 112 740 112 724 130 C 760 150 '
        '820 180 900 196 L 900 300 Z" fill="#9fd6e3" opacity="0.88"/><path d="M 520 120 C 600 92 660 70 720 76 C 760 80 '
        '790 100 800 128" stroke="#ffffff" stroke-width="14" fill="none" stroke-linecap="round"/>'
        '<path d="M 300 182 C 380 170 450 150 520 120" stroke="#e8f6fa" stroke-width="6" fill="none" opacity="0.8"/></svg>')
FLASH = '<svg viewBox="0 0 10 10" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none"><rect width="10" height="10" fill="#fff"/></svg>'
DASH = ('<svg viewBox="0 0 600 40" xmlns="http://www.w3.org/2000/svg"><line x1="10" y1="20" x2="590" y2="20" stroke="#f3f6f7" '
        'stroke-width="7" stroke-dasharray="26 18" stroke-linecap="round"/><path d="M 590 20 L 560 4 L 560 36 Z" fill="#f3f6f7"/></svg>')
GLOW_RED = ('<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="r"><stop offset="0" '
            'stop-color="#ff5a4a" stop-opacity="0.85"/><stop offset="1" stop-color="#ff5a4a" stop-opacity="0"/></radialGradient>'
            '</defs><circle cx="100" cy="100" r="100" fill="url(#r)"/></svg>')
BAR = lambda label: ('<svg viewBox="0 0 400 70" xmlns="http://www.w3.org/2000/svg"><line x1="8" y1="14" x2="392" y2="14" '
                     'stroke="#f3f6f7" stroke-width="6"/><line x1="8" y1="2" x2="8" y2="26" stroke="#f3f6f7" stroke-width="6"/>'
                     '<line x1="392" y1="2" x2="392" y2="26" stroke="#f3f6f7" stroke-width="6"/><text x="200" y="64" '
                     'text-anchor="middle" font-family="Montserrat, Arial Black, sans-serif" font-weight="900" font-size="40" '
                     f'fill="#f3f6f7">{label}</text></svg>')

# Iberian orca-boat interaction area (Atlantic Orca Working Group reports, 2020-2025): Strait of Gibraltar, the Gulf of
# Cadiz, the Portuguese coast and Galicia. Inner edge sits inside the land (zones draw under the coast).
IBERIA_ZONE = [(-5.2, 36.15), (-5.7, 35.6), (-6.6, 35.55), (-7.6, 36.2), (-8.4, 36.3), (-9.9, 36.4), (-10.3, 37.4),
               (-10.2, 38.1), (-10.6, 38.7), (-10.7, 39.5), (-10.4, 40.4), (-10.1, 41.3), (-10.4, 42.2), (-10.6, 42.9),
               (-10.1, 43.8), (-8.4, 44.3), (-7.6, 44.2), (-7.6, 43.5), (-8.5, 43.2), (-8.8, 42.4), (-8.6, 41.4),
               (-8.5, 40.4), (-8.9, 39.3), (-9.0, 38.3), (-8.6, 37.3), (-7.4, 37.3), (-6.3, 36.9), (-5.7, 36.3)]


def orca(x, y, w, h, **props):
    """Side/head/top orca layer. Layer kwargs (start, end, keyframes, z, depth, flipX, idle, enter, rotate...) in props."""
    lk = {k: props.pop(k) for k in list(props) if k in (*E.LAYER_KW, "flipX", "idle", "rotate", "scale")}
    return comp("explainer/Orca", x, y, w, h, props, **lk)


def T(text, at, x="50%", y="13%", size=48, w=1000, accent=CYAN, **props):
    """Tag >= 44 px (readable at 1080 wide); red accent only for threats."""
    return E.t46(text, at, x=x, y=y, size=max(44, size), w=w, accent=accent, **props)


def S(value, label, at, y="59.5%", size=120, **props):
    """White stat, red rule, label >= 44 px."""
    return E._lk(E.stat(value, label, at, y=y, size=size, color="white", labelSize=44, **props), props)


def diver(x, y, ppm, chip_dy=-5.3, at=0.0, kf=None, chip=True, **kw):
    """YOU = the hook's diver, everywhere. chip_dy: chip offset in % of height."""
    d = comp("explainer/Diver", x, y, 2.6 * ppm + 20, 0.5 * ppm + 40, {"pxPerM": ppm, "arms": "side"}, flipX=True,
             idle=[{"type": "float", "amount": 6, "speed": 0.35}], **kw)
    if at > 0:
        d["start"], d["enter"] = at, pop(at)
    if kf:
        d["keyframes"] = kf
    out = [d]
    if chip:
        cy = f"{float(y.rstrip('%')) + chip_dy:.2f}%"
        ck = None
        if kf:
            ck = [{**k, **({"y": f"{float(k['y'].rstrip('%')) + chip_dy:.2f}%"} if "y" in k else {})} for k in kf]
        out.append(E.you_chip(at, x, cy, ck))
    return out


def flash(at, peak=0.55):
    return {"type": "rect", "fill": "#ffffff", "x": "50%", "y": "50%", "width": 4000, "height": 4000, "depth": 0, "z": 40,
            "start": at, "end": at + 0.45, "keyframes":[{"t": at, "opacity": 0}, {"t": at + 0.06, "opacity": peak}, {"t": at + 0.45, "opacity": 0, "ease": "out"}]}


def cam(s, z0=1.0, z1=1.05, p=1.15, punches=(), keys=None, locked=()):
    c = E.Cam(s.dur, z0, z1, p=p, keys=keys)
    c.punch(*punches)
    c.locked += list(locked)
    return c


def hook_orca(kf, **props):
    return orca(*HOOK_ORCA, 980, 360, speed=HOOK_SPEED, pxPerM=PPM0, keyframes=kf, z=2, **props)


def surface_bg():
    return E.ocean(6, surface=0.2, rays=8, snow=60)


def build(S_):
    sc = []
    at = lambda s, w, n=0, off=0.0: s.at(w, n, off=off)

    # ------------------------------------------------------------ p00 hook: frame 0 = cover (orca, YOU, headline in place)
    s = S_[0]
    kill = at(s, "kill", off=-0.12)
    sc.append(E.bw_scene(s, surface_bg(), [
        hook_orca([{"t": 0, "x": HOOK_ORCA[0]}, {"t": s.dur, "x": "51%", "ease": "out"}]),
        *diver(*HOOK_DIVER, PPM0, chip_dy=float(HOOK_CHIP[1].rstrip('%')) - float(HOOK_DIVER[1].rstrip('%'))),
        E.headline("KILLER WHALE?", at=E.COVER, y="15%", size=84),
        S(0, "wild human kills", kill, x="40%", size=124, duration=0.25),
    ], cam(s, punches=[kill, at(s, "never")], locked=[(0.0, 0.9)])))

    # ------------------------------------------------------------ p01 scale: true-scale male, ~8 M bar, 4 cars, YOU on its back by the fin
    s = S_[1]
    PPM = 105
    four = at(s, "four", off=-0.1)
    fin = at(s, "fin", off=-0.15)
    cars = [comp("explainer/Car", 180 + i * 240, "55%", 220, 110, {"color": c}, start=four + i * 0.12,
                 enter={"type": "drop", "at": four + i * 0.12, "duration": 0.3, "distance": 220}, depth=0.9)
            for i, c in enumerate(["#d8d8d8", "#c8453a", "#3a8fd6", "#e3b04b"])]
    sc.append(E.bw_scene(s, E.ocean(30, rays=7), [
        orca("50%", "35%", 1000, 360, pxPerM=PPM, finScale=1.5, amp=0.35, idle=[{"type": "bob", "amount": 4, "speed": 0.4}]),
        E.headline("NOT BECAUSE IT CAN'T", at=0.1, y="12%", size=64, out=at(s, "eight", off=-0.2)),
        comp("explainer/ScaleBar", "50%", "46%", 8 * PPM, 140, {"label": "~8 M", "at": at(s, "eight", off=-0.1), "labelSize": 52}),
        *cars,
        T("≈ 6 TONNES", at(s, "cars,"), y="62.5%", size=48, w=600, align="center"),
        comp("explainer/You", "67%", "28.1%", 140, 220, {"pxPerM": PPM, "pose": "wave"}, start=fin, enter=pop(fin), z=3),
        T("FIN = YOUR HEIGHT", fin + 0.2, y="13%", size=48, w=900, align="center"),
    ], cam(s, punches=[at(s, "eight"), four, fin])))

    # ------------------------------------------------------------ p02 speed: bars, then 50 m chase -> 3 SECONDS
    s = S_[2]
    chase = at(s, "From", off=-0.1)
    reach = at(s, "reaches")
    three = at(s, "three", 1, off=-0.1)
    sc.append(E.bw_scene(s, E.ocean(20, rays=8), [
        comp("explainer/SpeedBars", "50%", "31%", 1000, 560, {
            "title": "Top speed", "max": 60, "at": 0.3, "stagger": 1.85, "duration": 0.6, "size": 56, "labelWidth": 330,
            "out": chase, "rows": [{"label": "Orca", "value": 56, "unit": "km/h", "color": "red"},
                                   {"label": "Olympic swimmer", "value": 8, "unit": "km/h", "color": CYAN},
                                   {"label": "You", "value": 3, "unit": "km/h", "color": "#f3f6f7"}]}, depth=0),
        orca("50%", "52%", 640, 220, speed=1.8, z=1, end=chase,
             keyframes=[{"t": 0, "x": "-40%"}, {"t": chase, "x": "135%", "ease": "linear"}]),
        *diver("80%", "42%", 70, at=chase),
        svg(DASH, "50%", "35%", 560, 40, start=chase + 0.15, enter={"type": "fade", "at": chase + 0.15, "duration": 0.2},
            end=reach + 0.3, flipX=True, z=1),
        T("50 M", chase + 0.2, x="50%", y="30%", size=48, w=260, align="center", end=reach + 0.3),
        orca("50%", "42%", 520, 180, speed=2.2, z=2, start=chase,
             keyframes=[{"t": chase, "x": "-30%"}, {"t": s.dur - 0.1, "x": "50%", "ease": "in"}]),
        S(3, "seconds to reach you", three, size=124, duration=0.01),
    ], cam(s, punches=[at(s, "Olympic"), at(s, "You,"), reach], ), trans=WHIP))

    # ------------------------------------------------------------ p03 never just one: head-on orca, then the pod
    s = S_[3]
    every = at(s, "Every", off=-0.1)
    pod = [("28%", "27%", 540, 0.0, 0.0), ("70%", "33%", 620, 0.6, 0.12), ("40%", "45%", 440, 1.1, 0.24), ("78%", "47%", 330, 0.3, 0.36),
           ("16%", "40%", 300, 0.8, 0.48)]
    sc.append(E.bw_scene(s, E.ocean(60, rays=6), [
        orca("50%", "38%", 720, 640, pose="head", end=every + 0.3, z=3,
             keyframes=[{"t": 0, "scale": 0.55, "opacity": 1}, {"t": every, "scale": 1.2, "opacity": 1, "ease": "in"},
                        {"t": every + 0.3, "scale": 1.5, "opacity": 0, "ease": "in"}]),
        *[orca(x, y, w, w * 0.36, timeOffset=to, start=every + d, enter=pop(every + d), idle=[{"type": "float", "amount": 10, "speed": 0.3}])
          for x, y, w, to, d in pod],
        E.headline("FAMILY POD", at=every, y="13%", size=70),
        T("OWN CALLS", at(s, "calls,"), x="27%", y="57%", size=46, w=480, align="center"),
        T("OWN MENU", at(s, "menu,"), x="73%", y="57%", size=46, w=480, align="center"),
        T("OWN PLAN", at(s, "plan."), x="50%", y="63%", size=46, w=480, align="center"),
    ], cam(s, punches=[at(s, "one."), at(s, "calls,")])))

    # ------------------------------------------------------------ p04 wave-washing: charge, wave, seal off; YOU on the ice, washed off too
    s = S_[4]
    ch = at(s, "charges")
    wash = at(s, "washes")
    youd = at(s, "You'd", off=-0.35)
    sc.append(E.bw_scene(s, E.ocean(4, surface=0.36, rays=9, snow=40), [
        svg(E.ICE, "72%", "36%", 420, 170, z=2),
        svg(E.SEAL, "70%", "31.5%", 200, 80, z=3,
            keyframes=[{"t": 0, "x": "70%", "y": "31.5%", "rotate": 0}, {"t": wash, "x": "70%", "y": "31.5%", "rotate": 0},
                       {"t": wash + 0.7, "x": "58%", "y": "40%", "rotate": -35, "ease": "in"},
                       {"t": wash + 1.4, "x": "52%", "y": "47%", "rotate": -60, "opacity": 0}]),
        *[orca("10%", f"{44 + i * 4}%", 460, 160, speed=1.5, timeOffset=i * 0.3, z=1,
               keyframes=[{"t": 0, "x": "-30%"}, {"t": max(0.1, ch - 0.3), "x": "-25%"}, {"t": wash + 0.2, "x": f"{48 - i * 8}%", "ease": "inOut"}])
          for i in range(3)],
        svg(WAVE, "52%", "30.4%", 960, 320, z=4, start=wash - 0.45, end=wash + 1.0,
            keyframes=[{"t": wash - 0.45, "scaleY": 0.2, "opacity": 0, "x": "36%"}, {"t": wash, "scaleY": 1, "opacity": 1, "x": "50%", "ease": "out"},
                       {"t": wash + 1.0, "scaleY": 0.3, "opacity": 0, "x": "64%"}]),
        comp("explainer/You", "80%", "29.2%", 110, 170, {"pxPerM": 90, "pose": "panic"}, z=3, start=youd, enter=pop(youd),
             keyframes=[{"t": youd, "x": "80%", "y": "29.2%", "rotate": 0}, {"t": youd + 0.45, "x": "80%", "y": "29.2%", "rotate": 0},
                        {"t": s.dur, "x": "70%", "y": "41%", "rotate": -80, "ease": "in"}]),
        E.you_chip(youd, "80%", "22.5%"),
        svg(WAVE, "58%", "30.4%", 960, 320, z=4, start=youd + 0.25, end=s.dur,
            keyframes=[{"t": youd + 0.25, "scaleY": 0.2, "opacity": 0, "x": "44%"}, {"t": youd + 0.7, "scaleY": 1, "opacity": 1, "x": "58%", "ease": "out"},
                       {"t": s.dur, "scaleY": 0.6, "opacity": 0.5, "x": "66%"}]),
        T("ANTARCTICA", 0.15, x="30%", y="12%", size=46, w=520),
    ], _with_shake(cam(s, punches=[ch, at(s, "seal")], keys=[(0, 1.0, "50%", "50%"), (s.dur, 1.08, "50%", "50%")]),
                   [(wash, 0.6, 16), (youd + 0.7, 0.4, 10)]), trans=WHIP))

    # ------------------------------------------------------------ p05 livers: South Africa pin, shark, liver highlight, two orcas flip it
    s = S_[5]
    shark = at(s, "the", off=-0.1)
    miss = at(s, "missing")
    liver = at(s, "liver.", off=-0.12)
    orcas = at(s, "Orcas", off=-0.5)
    flip = at(s, "flipped")
    took = at(s, "took")
    sc.append(E.bw_scene(s, E.ocean(120, rays=5), [
        comp("explainer/Map", "50%", "50%", 1080, 1920, {
            "views": [{"t": 0, "lon": 22, "lat": -26, "zoom": 4.5}, {"t": shark, "lon": 20, "lat": -32, "zoom": 6.5}],
            "pins": [{"lon": 19.35, "lat": -34.6, "at": 0.1, "label": "Gansbaai"}], "labelSize": 48, "pinSize": 1.4}, depth=0, z=30, end=shark),
        T("SOUTH AFRICA", 0.1, x="50%", y="13%", size=48, w=800, align="center", end=shark, z=31),
        comp("explainer/GreatWhite", "50%", "40%", 900, 320, {"speed": 0.9}, start=shark, z=2,
             keyframes=[{"t": shark, "scaleY": 1, "rotate": 0, "x": "50%"}, {"t": flip - 0.25, "scaleY": 1, "rotate": 0, "x": "50%"},
                        {"t": flip + 0.35, "scaleY": -1, "rotate": 6, "x": "50%", "ease": "inOut"}, {"t": s.dur, "scaleY": -1, "rotate": 10, "x": "47%"}]),
        T("GREAT WHITE", shark + 0.1, x="50%", y="13%", size=48, w=700, align="center", out=miss),
        svg(GLOW_RED, "56%", "43%", 300, 300, z=3, start=miss, enter=fade(miss, 0.3),
            idle=[{"type": "pulse", "amount": 0.2, "speed": 1.2}], keyframes=[{"t": miss, "opacity": 0.8}, {"t": took, "opacity": 0.8}, {"t": took + 0.4, "opacity": 0}]),
        comp("explainer/Liver", "56%", "43%", 210, 112, {}, start=liver, enter=pop(liver, 0.3), z=4,
             shadow="0 0 26px rgba(255,90,74,0.9)", idle=[{"type": "pulse", "amount": 0.08, "speed": 1.4}],
             keyframes=[{"t": liver, "x": "56%", "y": "43%"}, {"t": took, "x": "56%", "y": "43%"},
                        {"t": s.dur, "x": "8%", "y": "33%", "ease": "in"}]),
        T("LIVER: GONE", liver + 0.1, x="50%", y="62.5%", size=50, w=700, accent=RED, align="center"),
        orca("50%", "30%", 520, 190, speed=1.6, start=orcas, z=5,
             keyframes=[{"t": orcas, "x": "-30%"}, {"t": flip, "x": "26%", "ease": "out"}, {"t": s.dur, "x": "-5%", "y": "33%", "ease": "in"}]),
        orca("50%", "51%", 520, 190, speed=1.6, start=orcas, z=5, flipX=True,
             keyframes=[{"t": orcas, "x": "130%"}, {"t": flip, "x": "76%", "ease": "out"}, {"t": s.dur, "x": "70%", "y": "54%"}]),
    ], _with_shake(cam(s, punches=[shark, liver, flip]), [(flip + 0.1, 0.4, 12)]), trans=DIP))

    # ------------------------------------------------------------ p06 great whites flee; YOU alone, a shadow passes
    s = S_[6]
    fled = at(s, "fled", off=-0.1)
    if_ = at(s, "If", off=-0.1)
    sc.append(E.bw_scene(s, E.ocean(80, rays=6), [
        *[comp("explainer/GreatWhite", x, y, w, w * 0.36, {"speed": 1.6, "timeOffset": i * 0.3}, flipX=True, end=if_,
               keyframes=[{"t": 0, "x": x}, {"t": if_, "x": f"{-30 - i * 10}%", "ease": "in"}])
          for i, (x, y, w) in enumerate([("62%", "34%", 640), ("86%", "48%", 500), ("40%", "52%", 360)])],
        E.headline("GONE FOR MONTHS", at=fled, y="14%", size=72, out=if_),
        orca("50%", "40%", 1500, 540, silhouette="#0a2531", speed=0.7, start=if_, z=0, depth=0.6,
             keyframes=[{"t": if_, "x": "150%", "opacity": 0}, {"t": if_ + 0.4, "opacity": 0.85}, {"t": s.dur, "x": "60%", "opacity": 0.85}], flipX=True),
        *diver("50%", "46%", 120, at=if_ + 0.05),
    ], cam(s, punches=[fled, at(s, "you")]), trans=CUT))

    # ------------------------------------------------------------ p07 blue whale: orcas converge, whale slows and tilts, hit on "brought down"
    s = S_[7]
    PPM2 = 34
    podt = at(s, "pod", off=-1.0)
    down = at(s, "down")
    adult = at(s, "adult", off=-0.1)
    thous = at(s, "thousand", off=-0.1)
    targets = [("-22%", "26%", "31%", "34%", False), ("122%", "28%", "71%", "36%", True), ("-26%", "56%", "37%", "47%", False),
               ("126%", "58%", "63%", "49%", True), ("50%", "-10%", "52%", "32%", False)]
    sc.append(E.bw_scene(s, E.ocean(40, rays=7), [
        comp("explainer/BlueWhale", "50%", "41%", 1000, 300, {"pxPerM": PPM2, "speed": 0.7}, z=1,
             keyframes=[{"t": 0, "x": "48%", "y": "41%", "rotate": 0}, {"t": down, "x": "52%", "y": "41%", "rotate": 0},
                        {"t": down + 0.9, "x": "53%", "y": "43%", "rotate": 7, "ease": "out"}, {"t": s.dur, "x": "53.5%", "y": "46%", "rotate": 11}]),
        *[orca(x0, y0, 300, 110, pxPerM=PPM2, speed=1.6, timeOffset=i * 0.4, z=2, flipX=fx,
               keyframes=[{"t": 0, "x": x0, "y": y0}, {"t": podt, "x": x0, "y": y0},
                          {"t": down - 0.1, "x": x1, "y": y1, "ease": "out"},
                          {"t": down + 0.5, "x": f"{float(x1[:-1]) + (2 if fx else -2)}%", "y": y1},
                          {"t": s.dur, "x": f"{float(x1[:-1]) + (-1.5 if fx else 1.5)}%", "y": f"{float(y1[:-1]) + 3}%"}])
          for i, (x0, y0, x1, y1, fx) in enumerate(targets)],
        flash(down - 0.04),
        T("2019 · WESTERN AUSTRALIA", 0.15, y="13%", size=46, w=1040, align="center", out=adult),
        T("ADULT BLUE WHALE", adult, y="60%", size=52, w=800, accent=RED, align="center"),
        *diver("82%", "58%", PPM2, at=thous, chip_dy=-3.4),
        T("1,000× YOUR WEIGHT", thous + 0.1, y="13%", size=50, w=900, align="center"),
    ], _with_shake(cam(s, p=1.22, punches=[podt + 0.6, down, adult]), [(down, 0.6, 18)]), trans=WHIP))

    # ------------------------------------------------------------ p08 the question: YOU, a shadow behind, WHY NOT YOU?
    s = S_[8]
    sc.append(E.bw_scene(s, E.ocean(260, rays=3, snow=50), [
        orca("50%", "40%", 1400, 500, silhouette="#08202b", speed=0.8, z=0, depth=0.6,
             keyframes=[{"t": 0, "x": "-60%", "opacity": 0.9}, {"t": s.dur, "x": "40%", "opacity": 0.9}]),
        *diver("50%", "46%", 140),
        E.headline("WHY NOT YOU?", at=at(s, "why", off=-0.1), y="22%", size=100, color="red"),
    ], cam(s, z1=1.08, punches=[at(s, "smart"), at(s, "never")]), trans=DIP))

    # ------------------------------------------------------------ p09 options (hard cut: no ghosted title), 3. ??? until "culture"
    s = S_[9]
    items = ["You taste bad", "Too small to bother", "Culture"]
    too = at(s, "Too", off=-0.1)
    yr = at(s, "You're")
    size_ = at(s, "size", off=-0.25)
    PPM3 = 160
    sc.append(E.bw_scene(s, E.ocean(200, rays=4), [
        comp("explainer/Options", "50%", "27%", 1000, 640, {
            "title": "Why not you?", "items": items, "at": 0.0, "itemAt": [0.1, too, too], "size": 56,
            "hidden": [{"index": 2, "until": 999, "text": "???"}],
            "strikes": [{"index": 0, "at": at(s, "Nobody's")}, {"index": 1, "at": yr}]}, depth=0),
        comp("explainer/You", "30%", "53.5%", 160, 300, {"pxPerM": PPM3, "pose": "stand"}, start=size_, enter=pop(size_), z=2),
        E.you_chip(size_, "30%", "42.6%"),
        T("1.75 M", size_ + 0.1, x="30%", y="64%", size=44, w=300, align="center"),
        comp("explainer/Seal", "68%", "59%", 280, 90, {"pxPerM": PPM3}, start=size_ + 0.15, enter=pop(size_ + 0.15), z=2),
        T("HARBOUR SEAL", size_ + 0.2, x="68%", y="52.5%", size=44, w=520, align="center"),
        T("1.6 M", size_ + 0.25, x="68%", y="64%", size=44, w=300, align="center"),
    ], cam(s, punches=[at(s, "Nobody's"), too, yr]), trans=CUT))

    # ------------------------------------------------------------ p10 culture: reveal + select, then mother teaches calf; YOU not on the menu
    s = S_[10]
    cul = at(s, "culture.", off=-0.1)
    orc = at(s, "Orcas", off=-0.15)
    no = at(s, "no", off=-0.1)
    eat = at(s, "eat", 1, off=-0.1)
    sc.append(E.bw_scene(s, E.ocean(150, rays=5), [
        comp("explainer/Options", "50%", "27%", 1000, 640, {
            "title": "Why not you?", "items": items, "at": -1, "itemAt": [-1, -1, -1], "size": 56,
            "hidden": [{"index": 2, "until": cul, "text": "???"}],
            "strikes": [{"index": 0, "at": -1}, {"index": 1, "at": -1}], "select": {"index": 2, "at": cul + 0.05}}, depth=0, end=orc),
        orca("44%", "38%", 760, 270, timeOffset=0.2, start=orc, z=2,
             keyframes=[{"t": orc, "x": "36%"}, {"t": s.dur, "x": "50%"}], idle=[{"type": "float", "amount": 8, "speed": 0.3}]),
        orca("66%", "48%", 340, 120, timeOffset=0.9, start=orc + 0.25, enter=pop(orc + 0.25), z=2,
             keyframes=[{"t": orc + 0.25, "x": "60%"}, {"t": s.dur, "x": "72%"}], idle=[{"type": "float", "amount": 8, "speed": 0.35}]),
        T("MOTHER  +  CALF", orc + 0.1, y="13%", size=48, w=800, align="center", out=no),
        *diver("78%", "58%", 90, at=no + 0.1),
        T("NOT ON THE MENU", eat, y="13%", size=52, w=900, align="center"),
    ], cam(s, punches=[cul, at(s, "mothers"), no]), trans=CUT))

    # ------------------------------------------------------------ p11 twist: sailboat from below; map of the interaction zone; ram + rudder snaps
    s = S_[11]
    exc = at(s, "Except", off=-0.1)
    spain = at(s, "Spain", off=-0.1)
    ram = at(s, "ramming", off=-0.15)
    hit1 = ram + 0.45
    snap = at(s, "snapping")
    BOAT_Y = "26%"  # Ocean surface=0.3 -> waterline at H * (1.2 * 0.3 - 0.1) = 26 % (bg overscan 1.2)
    boat_props = {"hits": [hit1, snap], "snapAt": snap, "list": [{"t": 0, "v": 0}, {"t": snap, "v": 0}, {"t": s.dur, "v": 5}]}
    MZ = 15  # map zoom on Iberia: 45 px per degree, the whole peninsula + zone in frame
    ox = lambda lon: f"{(540 + (lon + 6.2) * 3 * MZ) / 1080 * 100:.1f}%"
    oy = lambda lat: f"{(960 - (lat - 39.0) * 3 * MZ) / 1920 * 100:.1f}%"
    sc.append(E.bw_scene(s, E.ocean(4, surface=0.3, rays=8, snow=40), [
        comp("explainer/Sailboat", "50%", BOAT_Y, 600, 900, boat_props, depth=0.12, z=1),
        orca("16%", "33%", 340, 120, speed=1.8, z=2, depth=0.12, start=ram - 0.3,
             keyframes=[{"t": ram - 0.3, "x": "-30%"}, {"t": hit1, "x": "14%", "ease": "in"}, {"t": hit1 + 0.3, "x": "8%", "ease": "out"},
                        {"t": snap, "x": "15%", "ease": "in"}, {"t": s.dur, "x": "4%", "y": "36%", "ease": "out"}]),
        T("RUDDER", ram, x="34%", y="40%", size=44, w=330, align="center", out=snap),
        T("SNAPPED", snap + 0.05, x="34%", y="40%", size=48, w=360, accent=RED, align="center"),
        comp("explainer/Map", "50%", "50%", 1080, 1920, {
            "views": [{"t": exc, "lon": -10, "lat": 42, "zoom": 8}, {"t": spain - 0.4, "lon": -6.2, "lat": 39.0, "zoom": MZ}],
            "zones": [{"points": [list(p) for p in IBERIA_ZONE], "at": spain, "label": "Iberian\norcas", "labelAt": [-11.0, 39.8],
                       "labelAnchor": "end"}], "labelSize": 52}, depth=0, z=30, start=exc, end=ram),
        T("SINCE 2020", at(s, "twenty", off=-0.1), y="13%", size=50, w=600, align="center", z=31, start=exc, end=ram),
        *[orca(ox(lon), oy(lat), 150, 56, pose="top", speed=1.4, timeOffset=i * 0.4, z=31, start=spain + 0.2 + i * 0.15,
               end=ram, enter=pop(spain + 0.2 + i * 0.15), rotate=r)
          for i, (lon, lat, r) in enumerate([(-6.6, 35.85, 10), (-9.9, 37.6, -80), (-10.1, 42.0, -95)])],
    ], _with_shake(cam(s, punches=[exc, spain, hit1]), [(hit1, 0.45, 18), (snap, 0.5, 14)]), trans=DIP))

    # ------------------------------------------------------------ p12 boat lists and sinks; ~7 BOATS SUNK in at the cut, held to the end
    s = S_[12]
    sc.append(E.bw_scene(s, E.ocean(4, surface=0.3, rays=8, snow=40), [
        comp("explainer/Sailboat", "50%", BOAT_Y, 600, 900, {"snapAt": -10, "bob": 0.6,
             "list": [{"t": 0, "v": 5}, {"t": s.dur, "v": 30, "ease": "in"}],
             "sink": [{"t": 0, "v": 0}, {"t": s.dur, "v": 150, "ease": "in"}]}, depth=0.12, z=1),
        orca("40%", "44%", 340, 120, speed=1.0, z=2, depth=0.12, keyframes=[{"t": 0, "x": "6%"}, {"t": s.dur, "x": "40%"}]),
        S(7, "boats sunk since 2020", 0.05, y="58.5%", size=130, prefix="~", **{"from": 4}, duration=0.7),
    ], _with_shake(cam(s, punches=[at(s, "sunk."), at(s, "Nobody")]), [(0.1, 0.4, 10)]), trans=CUT))

    # ------------------------------------------------------------ p13 bookend: the orca circles the same YOU and lands on frame 0
    s = S_[13]
    turn = 2.2
    because = at(s, "because...", off=-0.25)
    # phase-match the swim wave so the last frame's body bend equals frame 0's
    toff = (-s.dur) % ORCA_PERIOD
    sc.append(E.bw_scene(s, surface_bg(), [
        orca("50%", "56%", 640, 230, pxPerM=60, speed=1.2, flipX=True, z=0, end=turn,
             keyframes=[{"t": 0, "x": "112%"}, {"t": turn, "x": "-22%", "ease": "linear"}]),
        hook_orca([{"t": turn, "x": "-45%"}, {"t": s.dur, "x": HOOK_ORCA[0], "ease": "out"}], start=turn, timeOffset=round(toff, 3)),
        *diver(*HOOK_DIVER, PPM0, chip_dy=float(HOOK_CHIP[1].rstrip('%')) - float(HOOK_DIVER[1].rstrip('%'))),
        E.headline("KILLER WHALE?", at=because, y="15%", size=84),
    ], cam(s, keys=[(0, 1.06, "50%", "50%"), (s.dur - 1.3, 1.0, "50%", "50%"), (s.dur, 1.0, "50%", "50%")],
           punches=[at(s, "decided"), at(s, "And")], locked=[(s.dur - 1.3, s.dur)]), trans=CUT))
    return sc


def fade(at, d=0.4):
    return {"type": "fade", "at": at, "duration": d}


def _with_shake(c, shakes):
    c.shake = [{"at": round(a, 3), "duration": d, "amplitude": amp} for a, d, amp in shakes]
    return c
