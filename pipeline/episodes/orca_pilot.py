"""explainer-orca (PILOT) scene builder, fix round 2 (reviewer 5/10 -> fixes 1-10) + side-by-side fix round 1.

One narration paragraph = one scene (14 paragraphs). Every beat is anchored to narration words (Scene.at), every
scene gets an explicit camera with punch-ins (Cam), and build.py fails the episode on any visual hold > 3 s.

Visual grammar: YOU is always the hook's diver (white YOU chip). Red is the threat accent only. Orcas appear in
side, head-on (pose "head") and top-down (pose "top") views. Frame 0 is the Shorts cover (camera pushed in on the
orca's head, diver under the jaw, "0 HUMAN KILLS" claim with one red word) and the last frame returns to it exactly
(same orca x, diver, headline, camera) so the loop replays seamlessly.
"""
from __future__ import annotations

from . import explainer_eps as E
from .common import comp, pop, svg

H = 1920
RED, CYAN = E.RED, E.CYAN
CUT = None
FADE, WHIP, DIP = E.FADE, E.WHIP, E.DIP

PPM0 = 100                         # hook / bookend: orca and diver share pxPerM (honest you-vs-it scale)
HOOK_ORCA = ("46%", "35%")         # orca fully in frame at zoom 1.0 (left edge ~97 px)
HOOK_DIVER = ("74%", "42.5%")      # right under the jaw (diver 260 px at zoom 1.0, ~430 px on the cover)
HOOK_SPEED = 1.1
# cover camera (frame 0 = last frame): pushed in on the head so the orca fills ~80 % of the width, pulls back to 1.0 by 1 s
COVER_CAM = (1.65, "63.9%", "39.6%")
COVER_HEAD = dict(text="0 HUMAN KILLS", red="0", sub="IN THE WILD", y="12.5%", size=110)
CHIP = 32                          # YOU chip size (70 % of the old 44 px), always under the diver with a leader line
ORCA_PERIOD = 1 / (0.6 * HOOK_SPEED)
MENACE, MENACE_RIM = "#1f4d61", "0 0 3px #3f7f95"   # threat silhouettes: a looming shape on the #06121c water, cold rim   # swim-wave period of the hook orca (marine.tsx orca freq 0.6 * speed)

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
    lk = {k: props.pop(k) for k in list(props) if k in (*E.LAYER_KW, "flipX", "idle", "rotate", "scale", "shadow")}
    return comp("explainer/Orca", x, y, w, h, props, **lk)


def T(text, at, x="50%", y="13%", size=48, w=1000, accent=CYAN, **props):
    """Tag >= 44 px (readable at 1080 wide); red accent only for threats."""
    return E.t46(text, at, x=x, y=y, size=max(44, size), w=w, accent=accent, **props)


def S(value, label, at, y="59.5%", size=120, **props):
    """White stat, red rule, label >= 44 px."""
    return E._lk(E.stat(value, label, at, y=y, size=size, color="white", labelSize=44, **props), props)


def diver(x, y, ppm, at=0.0, kf=None, chip=True, chip_dy=4.6, **kw):
    """YOU = the hook's diver, everywhere (>= 220 px of visible body at 1080 wide). The YOU chip sits under the
    diver, tied to it by a short leader line, and never dwarfs the body. chip_dy: chip offset (% of height)."""
    d = comp("explainer/Diver", x, y, 2.6 * ppm + 20, 0.5 * ppm + 40, {"pxPerM": ppm, "arms": "side"}, flipX=True,
             idle=[{"type": "float", "amount": 6, "speed": 0.35}], **kw)
    if at > 0:
        d["start"], d["enter"] = at, pop(at)
    if kf:
        d["keyframes"] = kf
    out = [d]
    if chip:
        yv = float(y.rstrip('%'))
        top = 0.13 * ppm / H * 100 + 0.4             # just under the diver's body
        bot = chip_dy - 1.7                           # chip top
        ly, lh = yv + (top + bot) / 2, max(8, (bot - top) / 100 * H)
        line = svg('<svg viewBox="0 0 10 100" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none"><line x1="5" '
                   'y1="0" x2="5" y2="100" stroke="#f3f6f7" stroke-width="5"/></svg>', x, f"{ly:.2f}%", 10, lh, depth=1, z=6,
                   idle=[{"type": "float", "amount": 6, "speed": 0.35}])
        if at > 0:
            line["start"], line["enter"] = at, {"type": "fade", "at": at, "duration": 0.3}
        shift = lambda k, dy: {**k, **({"y": f"{float(k['y'].rstrip('%')) + dy:.2f}%"} if "y" in k else {})}
        if kf:
            line["keyframes"] = [shift(k, ly - yv) for k in kf]
        cy = f"{yv + chip_dy:.2f}%"
        out += [line, E.you_chip(at, x, cy, [shift(k, chip_dy) for k in kf] if kf else None, size=CHIP)]
    return out


def _not_to_scale(layers):
    """the YOU tag says the diver is enlarged (a separate "YOU NOT TO SCALE" tag sat on an orca and the diver)"""
    for l in layers:
        if l.get("name") == "explainer/Tag":
            l["props"]["text"] = "YOU · NOT TO SCALE"
            l["width"] = 440
    return layers


def flash(at, peak=0.25):
    """impact hit: a short (~3 frame) low white flash, not a full-frame wash-out (QA: read as a render glitch at 0.55)"""
    return {"type": "rect", "fill": "#ffffff", "x": "50%", "y": "50%", "width": 4000, "height": 4000, "depth": 0, "z": 40,
            "start": at, "end": at + 0.14, "keyframes":[{"t": at, "opacity": 0}, {"t": at + 0.03, "opacity": peak}, {"t": at + 0.14, "opacity": 0, "ease": "out"}]}


def cam(s, z0=1.0, z1=1.05, p=1.15, punches=(), keys=None, locked=()):
    c = E.Cam(s.dur, z0, z1, p=p, keys=keys)
    c.punch(*punches)
    c.locked += list(locked)
    return c


def hook_orca(kf, **props):
    return orca(*HOOK_ORCA, 980, 360, speed=HOOK_SPEED, pxPerM=PPM0, keyframes=kf, z=2, **props)


def cover_headline(at):
    h = COVER_HEAD
    return E.headline(h["text"], at=at, y=h["y"], size=h["size"], red=h["red"], sub=h["sub"], subColor="#d0dde3", subOpacity=0.9)


def surface_bg():
    # surface line ~60 px from the top (no dark letterbox band on the cover)
    # key pinned: the hook (frame 0 = cover) and the bookend (last frame = cover) must share one key for the loop
    return E.ocean(6, surface=0.12, rays=8, snow=60, key="tide")


def deep_bg(depth, **kw):
    """threat / 'why not you' beats: darker navy toward #06121c at the bottom"""
    return E.ocean(depth, bottomColor="#06121c", **kw)


YUCK = ('<svg viewBox="0 0 260 110" xmlns="http://www.w3.org/2000/svg"><rect x="4" y="4" width="252" height="102" rx="51" '
        'fill="#f3f6f7" stroke="#0b1a22" stroke-width="6"/><path d="M 40 40 Q 70 56 100 40" stroke="#0b1a22" stroke-width="8" '
        'fill="none" stroke-linecap="round"/><path d="M 56 50 Q 54 92 72 92 Q 90 92 86 50 Z" fill="#e5483d"/>'
        '<text x="176" y="72" text-anchor="middle" font-family="Montserrat, Arial Black, sans-serif" font-weight="900" '
        'font-size="44" fill="#0b1a22">YUCK?</text></svg>')
VBRACKET = ('<svg viewBox="0 0 40 300" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none"><line x1="20" y1="14" '
            'x2="20" y2="286" stroke="#f3f6f7" stroke-width="6" stroke-dasharray="18 12"/><path d="M 4 26 L 20 2 L 36 26 Z" '
            'fill="#f3f6f7"/><path d="M 4 274 L 20 298 L 36 274 Z" fill="#f3f6f7"/></svg>')
RING_RED = ('<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"><circle cx="100" cy="100" r="90" fill="rgba(229,72,61,0.12)" '
            'stroke="#e5483d" stroke-width="7"/></svg>')


def build(S_):
    sc = []
    at = lambda s, w, n=0, off=0.0: s.at(w, n, off=off)

    # ------------------------------------------------------------ p00 hook: frame 0 = cover (head close-up, YOU under the jaw, claim)
    s = S_[0]
    z0, cx0, cy0 = COVER_CAM
    hook = cam(s, keys=[(0, z0, cx0, cy0), (1.0, 1.0, "50%", "50%"), (s.dur, 1.05, "50%", "50%")],
               punches=[at(s, "never")], locked=[(0.0, 1.1)])
    sc.append(E.bw_scene(s, surface_bg(), [
        hook_orca([{"t": 0, "x": HOOK_ORCA[0]}, {"t": s.dur, "x": "50%", "ease": "out"}]),
        *diver(*HOOK_DIVER, PPM0, z=3),
        cover_headline(E.COVER),
    ], hook))
    _ease_key(sc[-1], 1.0)

    # ------------------------------------------------------------ p01 scale: true-scale male, ~8 M bar, 4 cars, YOU on its back by the fin
    s = S_[1]
    PPM = 105
    four = at(s, "four", off=-0.1)
    fin = at(s, "fin", off=-0.15)
    cars = [comp("explainer/Car", 255 + i * 190, "59%", 190, 95, {"color": c}, start=four + i * 0.12,
                 enter={"type": "drop", "at": four + i * 0.12, "duration": 0.3, "distance": 60}, depth=0.9)
            for i, c in enumerate(["#d8d8d8", "#c8453a", "#3a8fd6", "#e3b04b"])]
    # house style: the colour shift lands on the scale beat ("eight metres") and this is the episode's hero wide shot
    # (opt-in depth planes: far ridge + kelp, warm mid reef, cropped ink foreground kelp)
    house_mark = {"shift": {"at": at(s, "eight", off=-0.3), "to": "warm"}, "wide": True}
    sc.append(E.bw_scene(s, E.ocean(30, rays=7), [
        orca("50%", "35%", 1000, 360, pxPerM=PPM, finScale=1.5, amp=0.35, idle=[{"type": "bob", "amount": 4, "speed": 0.4}]),
        # (no "NOT BECAUSE THEY CAN'T" headline: it repeated the caption under it - staging [dup])
        comp("explainer/ScaleBar", "50%", "46%", 8 * PPM, 140, {"label": "~8 M", "at": at(s, "eight", off=-0.1), "labelSize": 52}),
        *cars,
        T("≈ 6 TONNES", at(s, "cars,"), y="13%", size=48, w=600, align="center", out=fin - 0.3),
        # YOU stands on the orca's back by the fin: an intended contact beat (staging.py hero check waived)
        comp("explainer/You", "67%", "28.1%", 150, 230, {"pxPerM": PPM, "pose": "wave", "style": "diver"}, start=fin, enter=pop(fin), z=3,
             allowOverlap=True),
        # left of the figure (QA: the centred chip met the raised arm after the punch-in)
        T("FIN = YOU", fin + 0.2, x="31%", y="13%", size=48, w=420, align="center"),
    ], cam(s, punches=[at(s, "eight"), four, fin]), _house=house_mark))

    # ------------------------------------------------------------ p02 speed: bars over the orca, then 50 m chase (both in frame) -> 3 SECONDS
    s = S_[2]
    chase = at(s, "From", off=-0.1)
    reach = at(s, "reaches")
    three = at(s, "three", 1, off=-0.1)
    sc.append(E.bw_scene(s, E.ocean(20, rays=8), [
        comp("explainer/SpeedBars", "50%", "23%", 960, 560, {
            "title": "Top speed", "max": 60, "at": 0.3, "stagger": 1.85, "duration": 0.6, "size": 56, "labelWidth": 330,
            "out": chase, "rows": [{"label": "Orca", "value": 56, "unit": "km/h", "color": "red"},
                                   {"label": "Olympic swimmer", "value": 8, "unit": "km/h", "color": CYAN},
                                   {"label": "You", "value": 3, "unit": "km/h", "color": "#f3f6f7"}]}, depth=0),
        orca("50%", "50%", 700, 250, speed=1.8, z=2,
             keyframes=[{"t": 0, "x": "47%", "y": "50%", "scale": 1}, {"t": max(0.1, chase - 0.05), "x": "53%", "y": "50%", "scale": 1},
                        {"t": chase + 0.45, "x": "22%", "y": "44%", "scale": 0.6, "ease": "inOut"},
                        {"t": s.dur - 0.1, "x": "60%", "y": "44%", "scale": 0.6, "ease": "in"}]),
        *diver("82%", "44%", 100, at=chase, chip_dy=4.2),
        svg(DASH, "55.5%", "40.5%", 270, 26, start=chase + 0.45, enter={"type": "fade", "at": chase + 0.45, "duration": 0.2},
            end=reach + 0.3, z=1),
        T("50 M", chase + 0.5, x="55.5%", y="36%", size=48, w=260, align="center", end=reach + 0.3),
        S(3, "seconds to reach you", three, y="55.5%", size=124, duration=0.01),
    ], cam(s, punches=[at(s, "Olympic"), at(s, "You,"), reach], ), trans=WHIP))

    # ------------------------------------------------------------ p03 never just one: head-on orca, then the pod circles YOU
    s = S_[3]
    pod_t = at(s, "pod", off=-0.1)
    team = at(s, "team,", off=-0.1)
    outn = at(s, "outnumbered.", off=-0.1)
    pod = [("18%", "31%", 420, 0.0, 0.0, False), ("82%", "34%", 400, 0.6, 0.12, True), ("16%", "55%", 380, 1.1, 0.24, False),
           ("84%", "57%", 360, 0.3, 0.36, True), ("52%", "24%", 320, 0.8, 0.48, False)]
    sc.append(E.bw_scene(s, E.ocean(60, rays=6), [
        # the head-on close-up pushes through and is gone before the pod pops in around it (staging: no pod orca inside it)
        orca("50%", "38%", 720, 640, pose="head", end=pod_t + 0.2, z=3,
             keyframes=[{"t": 0, "scale": 0.55, "opacity": 1}, {"t": pod_t, "scale": 1.2, "opacity": 1, "ease": "in"},
                        {"t": pod_t + 0.2, "scale": 1.5, "opacity": 0, "ease": "in"}]),
        *[orca(x, y, w, w * 0.36, timeOffset=to, start=pod_t + 0.15 + d, enter=pop(pod_t + 0.15 + d), flipX=fx,
               idle=[{"type": "float", "amount": 10, "speed": 0.3}],
               keyframes=[{"t": pod_t + d, "x": x}, {"t": s.dur, "x": f"{float(x[:-1]) + (-4 if fx else 4)}%"}])
          for x, y, w, to, d, fx in pod],
        *diver("50%", "47%", 110, at=pod_t + 0.2),
        E.headline("HUNTS AS A TEAM", at=team, y="13%", size=72),
        T("OUTNUMBERED", outn, x="50%", y="40%", size=48, w=560, accent=RED, align="center"),
    ], cam(s, punches=[at(s, "one."), team, outn])))

    # ------------------------------------------------------------ p04 wave-washing: pod in from t=0, wave, seal off; YOU on the ice, washed off too
    s = S_[4]
    ch = at(s, "charges")
    wash = at(s, "washes")
    youd = at(s, "You'd", off=-0.35)
    pod4 = [("44%", 1.0, 1.0, "12%", "48%"), ("52.6%", 0.8, 0.85, "8%", "38%"), ("61%", 0.8, 0.85, "14%", "29%")]
    you_kf = [{"t": youd, "x": "80%", "y": "27.5%", "rotate": 0}, {"t": youd + 0.45, "x": "80%", "y": "27.5%", "rotate": 0},
              {"t": s.dur, "x": "72%", "y": "40%", "rotate": -80, "ease": "in"}]
    sc.append(E.bw_scene(s, E.ocean(4, surface=0.36, rays=9, snow=40, glow=0.3), [
        svg(E.ICE, "72%", "36%", 420, 170, z=2),
        # opacity on every key: core sample() holds the first defined value before it, so a lone final opacity 0 hid the seal
        svg(E.SEAL, "70%", "31.2%", 240, 96, z=3,
            keyframes=[{"t": 0, "x": "70%", "y": "31.2%", "rotate": 0, "opacity": 1}, {"t": wash, "x": "70%", "y": "31.2%", "rotate": 0, "opacity": 1},
                       {"t": wash + 0.7, "x": "58%", "y": "40%", "rotate": -35, "opacity": 1, "ease": "in"},
                       {"t": wash + 1.4, "x": "52%", "y": "47%", "rotate": -60, "opacity": 0}]),
        *[orca(x0, y, 460, 160, speed=1.5, timeOffset=i * 0.3, z=1 - i, opacity=op,
               keyframes=[{"t": 0, "x": x0, "scale": sc_}, {"t": max(0.1, ch - 0.3), "x": f"{float(x0[:-1]) + 6}%", "scale": sc_},
                          {"t": wash + 0.2, "x": x1, "scale": sc_, "ease": "inOut"}])
          for i, (y, sc_, op, x0, x1) in enumerate(pod4)],
        svg(WAVE, "52%", "30.4%", 960, 320, z=4, start=wash - 0.45, end=wash + 1.0,
            keyframes=[{"t": wash - 0.45, "scaleY": 0.2, "opacity": 0, "x": "36%"}, {"t": wash, "scaleY": 1, "opacity": 1, "x": "50%", "ease": "out"},
                       {"t": wash + 1.0, "scaleY": 0.3, "opacity": 0, "x": "64%"}]),
        comp("explainer/You", "80%", "27.5%", 140, 230, {"pxPerM": 120, "pose": "panic", "style": "diver"}, z=5, start=youd, enter=pop(youd),
             keyframes=you_kf),
        E.you_chip(youd, "80%", "19%", [{**k, "y": f"{float(k['y'][:-1]) - 8.5:.2f}%"} for k in you_kf], size=CHIP),
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
    sc.append(E.bw_scene(s, deep_bg(380, rays=4), [
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
        comp("explainer/Liver", "56%", "43%", 210, 112, {}, start=liver, enter=pop(liver, 0.3), z=4, allowOverlap=True,  # inside the shark
             shadow="0 0 26px rgba(255,90,74,0.9)", idle=[{"type": "pulse", "amount": 0.08, "speed": 1.4}],
             keyframes=[{"t": liver, "x": "56%", "y": "43%"}, {"t": took, "x": "56%", "y": "43%"},
                        {"t": s.dur, "x": "8%", "y": "33%", "ease": "in"}]),
        T("LIVER: GONE", liver + 0.1, x="50%", y="62.5%", size=50, w=700, accent=RED, align="center"),
        orca("50%", "30%", 520, 190, speed=1.6, start=orcas, z=5,
             keyframes=[{"t": orcas, "x": "-30%"}, {"t": flip, "x": "26%", "ease": "out"}, {"t": s.dur, "x": "-5%", "y": "33%", "ease": "in"}]),
        orca("50%", "51%", 520, 190, speed=1.6, start=orcas, z=5, flipX=True,
             keyframes=[{"t": orcas, "x": "130%"}, {"t": flip, "x": "76%", "ease": "out"}, {"t": s.dur, "x": "70%", "y": "54%"}]),
    ], _with_shake(cam(s, punches=[shark, liver, flip]), [(flip + 0.1, 0.4, 12)]), trans=DIP, qa_class="diagram_anatomy",
                        _house={"key": "danger"}))   # colour script: the kill beats re-key to coral sinking to ink

    # ------------------------------------------------------------ p06 great whites flee; YOU alone, a shadow passes
    s = S_[6]
    fled = at(s, "fled", off=-0.1)
    if_ = at(s, "If", off=-0.1)
    sc.append(E.bw_scene(s, deep_bg(420, rays=4), [
        *[comp("explainer/GreatWhite", x, y, w, w * 0.36, {"speed": 1.6, "timeOffset": i * 0.3}, flipX=True, end=if_,
               # flee into the distance (shrink + drift left) so "fled for months" shows the sharks, not a tail sliver
               keyframes=[{"t": 0, "x": x, "scale": 1}, {"t": if_, "x": f"{float(x[:-1]) - 32 - i * 4:.0f}%", "scale": 0.55, "ease": "inOut"}])
          for i, (x, y, w) in enumerate([("66%", "34%", 640), ("80%", "50%", 500), ("52%", "54%", 360)])],
        E.headline("GONE FOR MONTHS", at=fled, y="14%", size=72, out=if_),
        # menace shape: lifted off the #06121c water with a cold rim, head in frame by if_+0.3, slow push (QA: #0a2531 was invisible)
        orca("50%", "40%", 1500, 540, silhouette=MENACE, shadow=MENACE_RIM, speed=0.7, start=if_, z=0, depth=0.6,
             keyframes=[{"t": if_, "x": "110%", "opacity": 0, "scale": 1.0}, {"t": if_ + 0.3, "opacity": 0.95},
                        {"t": s.dur, "x": "60%", "opacity": 0.95, "scale": 1.06}], flipX=True),
        *diver("50%", "46%", 120, at=if_ + 0.05),
    ], cam(s, punches=[fled, at(s, "you")]), trans=CUT, _house={"key": "danger"}))

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
        T("2019 · WESTERN AUSTRALIA", 0.15, y="13%", size=46, w=1040, align="center", out=adult - 0.3),  # gone before the next chip
        # (no "ADULT BLUE WHALE" tag: it repeated the caption - staging [dup])
        # YOU below the belly, inside the frame (enlarged: true scale would be ~90 px; the label says so)
        *_not_to_scale(diver("58%", "53%", 90, at=thous, chip_dy=3.9)),
        svg(VBRACKET, "58%", "48.4%", 30, 120, start=thous + 0.1, enter={"type": "fade", "at": thous + 0.1, "duration": 0.2}, z=3),
        T("×1,000 YOUR WEIGHT", thous + 0.35, y="13%", size=50, w=900, align="center"),
    ], _with_shake(cam(s, p=1.22, punches=[podt + 0.6, down, adult]), [(down, 0.6, 18)]), trans=WHIP))

    # ------------------------------------------------------------ p08 the question: YOU, a shadow behind, WHY NOT YOU?
    s = S_[8]
    why_head = dict(y="13%", size=96)
    sc.append(E.bw_scene(s, deep_bg(500, rays=3, snow=50), [
        orca("50%", "40%", 1500, 540, silhouette=MENACE, shadow=MENACE_RIM, speed=0.8, z=0, depth=0.6,
             keyframes=[{"t": 0, "x": "-40%", "opacity": 0.95, "scale": 1.0}, {"t": s.dur, "x": "40%", "opacity": 0.95, "scale": 1.06}]),
        *diver("50%", "46%", 140),
        E.headline("WHY NOT YOU?", at=at(s, "why", off=-0.1), **why_head),
    ], cam(s, z1=1.08, punches=[at(s, "smart"), at(s, "never")]), trans=DIP))

    # ------------------------------------------------------------ p09 options (hard cut): same WHY NOT YOU? header, orca pass + YOU vs seal shown
    s = S_[9]
    items = ["You taste bad", "Too small", "Culture"]
    too = at(s, "Too", off=-0.1)
    yr = at(s, "You're")
    size_ = at(s, "size", off=-0.25)
    nob = at(s, "Nobody's")
    PPM3 = 120
    # the size rides in the YOU chip itself on "You're" (QA: a separate 1.75 M tag landed on the diver / the list)
    you9 = diver("30%", "57%", PPM3, chip_dy=4.2)
    you9[-1]["props"]["out"] = yr - 0.25   # gone before the sized chip pops in (no double text)
    you175 = E.you_chip(yr, "30%", "61.2%", size=CHIP)
    you175["props"].update(text="YOU · 1.75 M")
    you175["width"] = 360
    sc.append(E.bw_scene(s, deep_bg(450, rays=4), [
        E.headline("WHY NOT YOU?", at=-1, **why_head),
        comp("explainer/Options", "50%", "30.5%", 960, 520, {
            "title": "", "items": items, "at": 0.0, "itemAt": [0.1, too, too], "size": 68, "stamp": True,
            "hidden": [{"index": 2, "until": 999, "text": "???"}],
            "strikes": [{"index": 0, "at": nob}, {"index": 1, "at": yr}]}, depth=0),
        # passes under the list (never over "3. ???") and leaves before the YOU-vs-seal row
        orca("50%", "48.5%", 560, 200, speed=1.0, z=1, timeOffset=0.4,
             keyframes=[{"t": 0, "x": "30%"}, {"t": too, "x": "52%"}, {"t": too + 0.9, "x": "135%", "ease": "in"}]),
        svg(YUCK, "71%", "41%", 230, 98, start=0.3, enter=pop(0.3), end=too, z=4),   # inside the safe area (was cut off at 80 %)
        *you9,
        comp("explainer/Seal", "72%", "57.5%", 260, 90, {"pxPerM": PPM3}, start=too, enter=pop(too), z=2),
        # size tags ride with their figures (depth 1, like the YOU chip), so camera punches never slide them onto the diver
        T("SEAL 1.6 M", too + 0.15, x="65%", y="58%", size=44, w=400, align="center", depth=1),  # clear of the captions under the punch-ins
        you175,
    ], cam(s, punches=[nob, too, yr, size_]), trans=CUT))

    # ------------------------------------------------------------ p10 culture: reveal + select, then mother teaches calf; YOU not on the menu
    s = S_[10]
    cul = at(s, "culture.", off=-0.1)
    orc = at(s, "Orcas", off=-0.15)
    no = at(s, "no", off=-0.1)
    sc.append(E.bw_scene(s, deep_bg(450, rays=5), [
        E.headline("WHY NOT YOU?", at=-1, out=cul + 0.5, **why_head),  # out before MOTHER + CALF (no double text)
        comp("explainer/Options", "50%", "30.5%", 960, 520, {
            "title": "", "items": items, "at": -1, "itemAt": [-1, -1, -1], "size": 68, "stamp": True,
            "hidden": [{"index": 2, "until": cul, "text": "???"}],
            "strikes": [{"index": 0, "at": -1}, {"index": 1, "at": -1}], "select": {"index": 2, "at": cul + 0.05}}, depth=0, end=cul + 0.75),
        # mother + calf swim in as "culture" lands (the list alone was a text card), the list wipes off under them
        orca("44%", "40%", 760, 270, timeOffset=0.2, start=cul + 0.3, z=2,
             keyframes=[{"t": cul + 0.3, "x": "-25%"}, {"t": orc + 0.4, "x": "36%", "ease": "out"}, {"t": s.dur, "x": "50%"}],
             idle=[{"type": "float", "amount": 8, "speed": 0.3}]),
        orca("66%", "50%", 340, 120, timeOffset=0.9, start=cul + 0.45, z=2,
             keyframes=[{"t": cul + 0.45, "x": "-12%"}, {"t": orc + 0.55, "x": "60%", "ease": "out"}, {"t": s.dur, "x": "72%"}],
             idle=[{"type": "float", "amount": 8, "speed": 0.35}]),
        T("MOTHER  +  CALF", orc + 0.05, y="13%", size=48, w=800, align="center", out=no - 0.3),
        *diver("74%", "55%", 100, at=no + 0.1, chip_dy=4.2),   # tag clear of the caption band
        E.headline("NOT ON THE MENU", at=no + 0.1, y="13%", size=76, red="MENU"),
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
    MZ = 13  # map zoom on Iberia: 39 px per degree, both coastlines (Spain + Portugal) and the zone in frame
    LON0 = -5.2  # view centre: the peninsula (lon -9.5..3.3) centred, the zone label still in frame on the left
    ox = lambda lon: f"{(540 + (lon - LON0) * 3 * MZ) / 1080 * 100:.1f}%"
    oy = lambda lat: f"{(960 - (lat - 39.0) * 3 * MZ) / 1920 * 100:.1f}%"
    tops = [(-7.2, 35.0, 10), (-11.2, 43.2, -95)]  # Gulf of Cadiz/Gibraltar + Galicia, open water off the coast
    sc.append(E.bw_scene(s, E.ocean(4, surface=0.3, rays=8, snow=40, glow=0.3), [
        comp("explainer/Sailboat", "50%", BOAT_Y, 600, 900, boat_props, depth=0.12, z=1),
        orca("16%", "33%", 340, 120, speed=1.8, z=2, depth=0.12, start=ram - 0.3,
             keyframes=[{"t": ram - 0.3, "x": "-30%"}, {"t": hit1, "x": "14%", "ease": "in"}, {"t": hit1 + 0.3, "x": "8%", "ease": "out"},
                        {"t": snap, "x": "15%", "ease": "in"}, {"t": s.dur, "x": "4%", "y": "36%", "ease": "out"}]),
        T("RUDDER", ram, x="34%", y="40%", size=44, w=330, align="center", out=snap),
        T("SNAPPED", snap + 0.05, x="34%", y="40%", size=48, w=360, accent=RED, align="center"),
        comp("explainer/Map", "50%", "50%", 1080, 1920, {
            "views": [{"t": exc, "lon": -10, "lat": 42, "zoom": 8}, {"t": spain - 0.4, "lon": LON0, "lat": 39.0, "zoom": MZ}],
            "zones": [{"points": [list(p) for p in IBERIA_ZONE], "at": exc + 0.3, "label": "Iberian orcas", "labelAt": [-8.6, 46.2],
                       "labelAnchor": "middle"}], "labelSize": 46}, depth=0, z=30, start=exc, end=ram),
        T("SINCE 2020", at(s, "twenty", off=-0.1), y="13%", size=50, w=600, align="center", z=31, start=exc, end=ram),
        T("SPAIN", spain, x=ox(-3.6), y=oy(41.2), size=48, w=300, align="center", z=31, end=ram, accent="#8fa3ab"),
        T("PORTUGAL", spain + 0.1, x=ox(-8.0), y=oy(38.0), size=40, w=380, align="center", z=31, end=ram, accent="#8fa3ab"),
        *[svg(RING_RED, ox(lon), oy(lat), 150, 150, z=31, depth=0, start=spain - 0.3 + i * 0.15, end=ram, enter=pop(spain - 0.3 + i * 0.15),
              idle=[{"type": "pulse", "amount": 0.12, "speed": 1.4}]) for i, (lon, lat, r) in enumerate(tops)],
        *[orca(ox(lon), oy(lat), 180, 68, pose="top", speed=1.4, timeOffset=i * 0.4, z=32, depth=0, start=spain - 0.3 + i * 0.15,
               end=ram, enter=pop(spain - 0.3 + i * 0.15), rotate=r, shadow="0 0 5px #ffffff")
          for i, (lon, lat, r) in enumerate(tops)],
    ], _with_shake(cam(s, punches=[exc, spain, hit1]), [(hit1, 0.45, 18), (snap, 0.5, 14)]), trans=WHIP, qa_class="stock_proof"))

    # ------------------------------------------------------------ p12 boat lists and sinks; ~7 BOATS SUNK in at the cut, held to the end
    s = S_[12]
    sc.append(E.bw_scene(s, E.ocean(4, surface=0.3, rays=8, snow=40, glow=0.3), [
        comp("explainer/Sailboat", "50%", BOAT_Y, 600, 900, {"snapAt": -10, "bob": 0.6,
             "list": [{"t": 0, "v": 5}, {"t": s.dur, "v": 30, "ease": "in"}],
             "sink": [{"t": 0, "v": 0}, {"t": s.dur, "v": 150, "ease": "in"}]}, depth=0.12, z=1),
        orca("40%", "40%", 340, 120, speed=1.0, z=2, depth=0.12, keyframes=[{"t": 0, "x": "14%"}, {"t": s.dur, "x": "42%"}]),
        S(7, "boats sunk since 2020", 0.05, y="50%", size=130, prefix="~", **{"from": 4}, duration=0.7),
    ], _with_shake(cam(s, punches=[at(s, "sunk."), at(s, "Nobody")]), [(0.1, 0.4, 10)]), trans=CUT))

    # ------------------------------------------------------------ p13 bookend: the orca closes on the same YOU (pushed in) and lands on frame 0
    s = S_[13]
    because = at(s, "because...", off=-0.25)
    toff = (-s.dur) % ORCA_PERIOD  # phase-match the swim wave so the last frame's body bend equals frame 0's
    keys = [(0, 1.3, cx0, cy0), (s.dur * 0.35, 1.38, cx0, cy0), (s.dur * 0.7, 1.5, cx0, cy0), (s.dur, z0, cx0, cy0)]
    sc.append(E.bw_scene(s, surface_bg(), [
        hook_orca([{"t": 0, "x": "18%"}, {"t": s.dur, "x": HOOK_ORCA[0], "ease": "out"}], timeOffset=round(toff, 3)),
        *diver(*HOOK_DIVER, PPM0, z=3),
        cover_headline(because),
    ], cam(s, keys=keys, locked=[(0.0, s.dur)]), trans=CUT))
    return sc


def _ease_key(scene, t):
    """ease the camera key at t (the cover pull-back)"""
    for k in scene["camera"]["keyframes"]:
        if abs(k["t"] - t) < 1e-3:
            k["ease"] = "inOut"


def fade(at, d=0.4):
    return {"type": "fade", "at": at, "duration": d}


def _with_shake(c, shakes):
    c.shake = [{"at": round(a, 3), "duration": d, "amplitude": amp} for a, d, amp in shakes]
    return c
