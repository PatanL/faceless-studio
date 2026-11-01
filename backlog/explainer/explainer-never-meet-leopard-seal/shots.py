"""Shot list for explainer-never-meet-leopard-seal (16:9, 1920x1080). Each shot starts just before its anchor line.

Times inside layers are strings resolved by gen.py to scene-local seconds:
  "@r1b" start of line r1b, "@r1b.end" its end, "@r1b+0.4" offset, "@end" scene end, "@start" scene start.
Components marked NEW in KIT_GAPS do not exist yet in studio/src/kits/explainer.
"""

W, H = 1920, 1080
TEAL = "#6fd6e8"
SEAL_DARK = "#23323a"


# ---------------------------------------------------------------- helpers
def C(name, x, y, w, h, props=None, **kw):
    d = {"type": "component", "name": f"explainer/{name}", "x": x, "y": y, "width": w, "height": h, "props": props or {}}
    d.update(kw)
    return d


def ocean(depth=20, surface=None, **p):
    props = {"depth": depth, **p}
    if surface is not None:
        props["surface"] = surface
    return {"type": "component", "name": "explainer/Ocean", "depth": 0.12, "overscan": 1.2, "props": props}


def flat(color="#0b1a22"):
    return {"type": "color", "color": color}


def kicker(text, at, out=None, color="white"):
    p = {"text": text, "at": at, "size": 62, "color": color, "underline": True}
    if out:
        p["out"] = out
    return C("Headline", 960, 92, 1500, 150, p, depth=0, z=20)


def punch(text, at, out=None, y=780):
    p = {"text": text, "at": at, "size": 84, "color": "red"}
    if out:
        p["out"] = out
    return C("Headline", 960, y, 1500, 150, p, depth=0, z=21)


def tag(text, x, y, at, out=None, w=640, accent=TEAL, size=40):
    p = {"text": text, "at": at, "size": size, "accent": accent, "align": "center"}
    if out:
        p["out"] = out
    return C("Tag", x, y, w, 100, p, depth=0, z=20)


def text(t, x, y, at, size=54, color="#ffffff", **kw):
    d = {"type": "text", "text": t, "x": x, "y": y, "fontSize": size, "color": color, "start": at,
         "enter": {"type": "pop", "at": at, "duration": 0.3}, "depth": 0, "z": 18}
    d.update(kw)
    return d


LAYER_KEYS = {"id", "anchorX", "anchorY", "scale", "rotate", "opacity", "flipX", "depth", "z", "start", "end", "keyframes",
              "enter", "exit", "idle", "blur", "shadow", "blend"}


def _split(kw):
    lay = {k: v for k, v in kw.items() if k in LAYER_KEYS}
    props = {k: v for k, v in kw.items() if k not in LAYER_KEYS}
    return lay, props


def seal(x, y, w, h, pose="cruise", **kw):
    lay, props = _split(kw)
    return C("LeopardSeal", x, y, w, h, {"pose": pose, **props}, **lay)


def penguin(x, y, h, pose="waddle", **kw):
    lay, props = _split(kw)
    return C("Penguin", x, y, h * 0.55, h, {"pose": pose, **props}, **lay)


def you(x, y, h, pose="stand", **kw):
    extra = kw.pop("props", {})
    lay, props = _split(kw)
    return C("You", x, y, h * 0.6, h, {"pose": pose, **props, **extra}, **lay)


def floe(x=960, y=470, w=980, h=320, **kw):
    lay, props = _split(kw)
    return C("IceFloe", x, y, w, h, {"width": w, **props}, **lay)


def plus(at, d):
    """Offset a time that may be a "@line+off" anchor string."""
    if isinstance(at, (int, float)):
        return round(at + d, 3)
    import re as _re
    m = _re.match(r"^(@[A-Za-z0-9_]+(?:\.end)?)([+-]\d+(?:\.\d+)?)?$", at)
    return f"{m.group(1)}{float(m.group(2) or 0) + d:+.2f}"


def case(n_stamped, at, slot7="grey", label=None, out=None, full=False):
    """CASE FILE insert: 2.6 s pop-in at the right third (full=True: centred, whole scene)."""
    p = {"slots": 7, "state": {"stamped": n_stamped, "stampAt": at, "slot7": slot7}}
    if label:
        p["state"]["label"] = label
    if full:
        return C("CaseFile", 960, 540, 1100, 900, p, depth=0, z=25, enter={"type": "pop", "duration": 0.35})
    return C("CaseFile", 1540, 520, 620, 820, p, depth=0, z=25, start=at, end=out or plus(at, 2.6),
             enter={"type": "slideLeft", "at": at, "duration": 0.3}, exit={"type": "fade", "duration": 0.3})


def svg(markup, x, y, w, h, **kw):
    d = {"type": "svg", "markup": markup, "x": x, "y": y, "width": w, "height": h}
    d.update(kw)
    return d


def rings(x, y, at, n=4, color="rgba(160,220,255,0.55)", r=140, period=0.9):
    out = []
    for i in range(n):
        a = at if isinstance(at, str) else at
        out.append({"type": "circle", "x": x, "y": y, "width": r, "height": r, "fill": "rgba(0,0,0,0)",
                    "stroke": color, "strokeWidth": 4, "opacity": 0, "z": 4,
                    "idle": [{"type": "pulse", "amount": 0.9, "speed": 1 / (period * n), "phase": i / n}],
                    "start": a, "keyframes": [{"t": 0, "opacity": 0.9}]})
    return out


def hook_frame(sun=True, seal_under=False, extra=None):
    """The 0:00 floe framing reused at 4:xx (re-immersion) and 9:xx (bookend)."""
    layers = [floe(960, 500, 1000, 340, keel=True),
              you(1040, 372, 170, "kneel", props={"camera": True}, z=3)]
    if seal_under:
        layers.append(seal(-200, 820, 560, 170, "cruise", silhouette=SEAL_DARK, spots=True,
                           keyframes=[{"t": 0, "x": -300}, {"t": 6, "x": 1500, "ease": "inOut"}], z=2))
    return layers + (extra or [])


BOX_SVG = ('<svg viewBox="0 0 100 60" xmlns="http://www.w3.org/2000/svg"><rect x="4" y="4" width="92" height="52" rx="6" '
           'fill="none" stroke="#e8eef0" stroke-width="3" stroke-dasharray="6 4"/></svg>')
DOOR_SVG = ('<svg viewBox="0 0 400 40" xmlns="http://www.w3.org/2000/svg"><rect x="2" y="6" width="396" height="28" fill="rgba(255,90,74,0.18)" '
            'stroke="#ff5a4a" stroke-width="3" stroke-dasharray="12 8"/></svg>')
LOOP_SVG = ('<svg viewBox="0 0 600 360" xmlns="http://www.w3.org/2000/svg" font-family="Montserrat" font-weight="900" font-size="30" fill="#fff">'
            '<g fill="none" stroke="#6fd6e8" stroke-width="6"><path d="M150 90 A170 120 0 0 1 450 90"/><path d="M450 270 A170 120 0 0 1 150 270"/></g>'
            '<polygon points="450,70 470,100 430,100" fill="#6fd6e8"/><polygon points="150,290 130,260 170,260" fill="#6fd6e8"/>'
            '<text x="40" y="190">GRAB</text><text x="430" y="190">RELEASE</text><text x="250" y="40">CHASE</text><text x="255" y="345">GRAB</text></svg>')
FANG_SVG = ('<svg viewBox="0 0 300 200" xmlns="http://www.w3.org/2000/svg"><path d="M60 20 Q80 120 95 180 Q110 120 130 20 Z" fill="#f2efe6" stroke="#9aa" stroke-width="3"/>'
            '<path d="M190 60 q40 -20 70 10 l0 110 q-30 15 -70 0 Z" fill="#e8c4a8" stroke="#a87" stroke-width="3"/></svg>')
SIEVE_SVG = ('<svg viewBox="0 0 600 200" xmlns="http://www.w3.org/2000/svg" fill="#f2efe6" stroke="#7a8a90" stroke-width="3">'
             + "".join(f'<path d="M{20 + i * 110} 180 l15 -90 l15 40 l15 -110 l15 110 l15 -40 l15 90 Z"/>' for i in range(5)) + "</svg>")
BOOK_SVG = ('<svg viewBox="0 0 500 320" xmlns="http://www.w3.org/2000/svg"><rect x="10" y="10" width="480" height="300" fill="#e9dfc6" stroke="#8a7a5a" stroke-width="4"/>'
            '<text x="250" y="120" font-family="Georgia" font-size="40" text-anchor="middle" fill="#3a3020">SKINS ITS PREY</text>'
            + "".join(f'<rect x="60" y="{150 + i * 28}" width="380" height="8" fill="#b8a888"/>' for i in range(5)) + "</svg>")
PLATE_SVG = ('<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"><circle cx="100" cy="100" r="90" fill="#cfd6d8" stroke="#7d8a8f" stroke-width="6"/>'
             '<circle cx="100" cy="100" r="60" fill="none" stroke="#9aa6aa" stroke-width="3"/></svg>')
BELL_SVG = ('<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg"><path d="M60 12 C30 12 26 50 22 78 L12 92 L108 92 L98 78 C94 50 90 12 60 12 Z" fill="#ffd34d" stroke="#8a6a00" stroke-width="4"/>'
            '<circle cx="60" cy="102" r="10" fill="#8a6a00"/></svg>')
GARAGE_SVG = ('<svg viewBox="0 0 600 300" xmlns="http://www.w3.org/2000/svg"><path d="M20 290 L20 110 L300 20 L580 110 L580 290" fill="none" stroke="#e8eef0" stroke-width="8"/></svg>')
TIMELINE_SVG = ('<svg viewBox="0 0 1400 160" xmlns="http://www.w3.org/2000/svg" font-family="Montserrat" font-weight="800" font-size="30" fill="#cfe">'
                + "".join(f'<rect x="{20 + i * 22}" y="40" width="10" height="70" fill="{"#7d8a8f" if 1960 + i == 2003 else "#6fd6e8"}"/>' for i in range(62))
                + '<text x="10" y="150">1960s</text><text x="1290" y="150">2020s</text><text x="900" y="30" fill="#aab">2003</text></svg>')
STRIP_SVG = ('<svg viewBox="0 0 1600 120" xmlns="http://www.w3.org/2000/svg" font-family="Montserrat" font-weight="900" font-size="54" fill="#fff" text-anchor="middle">'
             '<text x="200" y="80">CIRCLE</text><text x="600" y="80">STARE</text><text x="1000" y="80" fill="#ff5a4a">GAPE</text><text x="1400" y="80">LEAVE</text></svg>')


# ---------------------------------------------------------------- shots
SHOTS = [
    # ---- L1 hook
    dict(id="s01_floe", at="0", type="wide, surface split",
         desc="`Ocean` `surface: 0.46`, low gold sky; NEW `IceFloe` (keel) centre; `You` NEW `kneel` + NEW `camera` prop on the floe; "
              "NEW `LeopardSeal` `silhouette` with spots slides under the keel left to right (frame 1; YOU never looks down); `Headline` \"ANTARCTIC PENINSULA\"; "
              "at {D:h2} `Tag` \"ORCAS\" + green tick",
         cam="slow `pushIn` 1.0 -> 1.05", sfx="`door_creak` pitched down -10 dB (ice creak), NEW `seal_trill` sub-bass only (until approved: `underwater_rumble` -12 dB)",
         bg=ocean(4, 0.46, rays=5), camera={"preset": "pushIn", "amount": 0.5},
         layers=hook_frame(seal_under=True, extra=[kicker("ANTARCTIC PENINSULA", "@h1", "@h1.end+0.6"),
                                                   tag("ORCAS  ✓", 420, 220, "@h2", None, w=460, accent="#5fd38a")]),
         cues=[("door_creak", 0.2, 0.25), ("underwater_rumble", 0.0, 0.3)]),
    dict(id="s02_wrongpole", at="h3", type="map gag",
         desc="`Map` `views` whip from Antarctica (lat -70) to the Arctic (lat 75); white `Grizzly` (`silhouette: '#f3f6f7'`) as the polar bear; `Tag` \"WRONG POLE\" + red cross",
         cam="`whip` in", sfx="`whoosh`, `pop` on the cross",
         bg=flat("#0f3a4a"), trans={"type": "whip", "duration": 0.3, "direction": "up"},
         layers=[C("Map", 960, 540, 1920, 1080, {"views": [{"t": 0, "lon": -60, "lat": -70, "zoom": 1.6}, {"t": 0.7, "lon": -40, "lat": 75, "zoom": 1.6}]}),
                 C("Grizzly", 960, 470, 420, 260, {"silhouette": "#f3f6f7"}, start=0.7, enter={"type": "pop", "at": 0.7, "duration": 0.3}),
                 tag("WRONG POLE  ✗", 960, 690, 1.0, w=560, accent="#ff5a4a")],
         cues=[("whoosh", 0.0, 0.6), ("pop", 1.0, 0.6)]),
    dict(id="s03_rule", at="h4", type="wide, surface split (0:00 framing)",
         desc="0:00 framing held; `Tag` \"-2 °C WATER\" + green tick, then `Tag` \"THE ONLY THREAT?\"",
         cam="hold", sfx="`tick`",
         bg=ocean(4, 0.46, rays=5),
         layers=hook_frame(extra=[tag("-2 °C WATER  ✓", 960, 210, "@h4+0.6", "@h4.end", w=560, accent="#5fd38a"),
                                  tag("THE ONLY THREAT?", 960, 210, "@h4.end", None, w=600)]),
         cues=[("tick", "@h4+0.6", 0.5)]),
    dict(id="s04_airborne", at="h5", type="medium, fast",
         desc="NEW `Penguin` `pose: airborne` arcs out of the water past the YOU figure's boot (keyframes x/y/rotate); red `Headline` \"AIRBORNE\"",
         cam="`shake` 0.3 s on the launch", sfx="`bubbles` + `whoosh`",
         bg=ocean(4, 0.46, rays=5), camera={"preset": "none", "shake": [{"at": "@h5+1.2", "duration": 0.3, "amplitude": 12}]},
         layers=hook_frame(extra=[penguin(700, 760, 140, "airborne", start="@h5+1.1",
                                          keyframes=[{"t": "@h5+1.1", "x": 640, "y": 760, "rotate": -40}, {"t": "@h5+1.7", "x": 980, "y": 330, "rotate": 10, "ease": "out"},
                                                     {"t": "@h5+2.3", "x": 1350, "y": 380, "rotate": 30, "ease": "in"}]),
                                  punch("AIRBORNE", "@h6+0.6")]),
         cues=[("bubbles", "@h5+1.0", 0.5), ("whoosh", "@h5+1.15", 0.7)]),
    dict(id="s05_trill", at="h7", type="under/over split",
         desc="camera dips under the waterline: dark under-ice, concentric `circle` rings rise through the keel into the kneeling figure's knees",
         cam="`panUp` from under the ice", sfx="NEW `seal_trill` (stand-in `underwater_rumble`), music out",
         bg=ocean(25, 0.3, rays=2), camera={"keyframes": [{"t": 0, "y": "62%", "zoom": 1.15}, {"t": "@end", "y": "50%", "zoom": 1.0}]},
         layers=hook_frame(extra=rings(960, 900, 0.3)),
         cues=[("underwater_rumble", 0.2, 0.7)]),
    dict(id="s06_face", at="h8", type="close, surface",
         desc="NEW `LeopardSeal` `pose: surface` side-profile head over the floe edge, mouth line curved up (no front view); `Headline` \"LEOPARD SEAL\"; red \"IT ISN'T SMILING\"; `jaw` 0 -> 8°",
         cam="slow `pushIn` to the face, `dipBlack` out", sfx="`boom` low on the punch",
         bg=ocean(4, 0.46, rays=4), camera={"preset": "pushIn", "amount": 1.2},
         layers=[floe(1150, 520, 1300, 360, keel=True),
                 seal(640, 560, 900, 300, "surface", jaw=[{"t": "@h10", "v": 0}, {"t": "@h10+0.6", "v": 8}]),
                 kicker("LEOPARD SEAL", "@h9"), punch("IT ISN'T SMILING", "@h10")],
         cues=[("boom", "@h10", 0.5)]),
    # ---- L2 credentials, L3 promise
    dict(id="s07_credentials", at="s1", type="graphic (CASE FILE)",
         desc="NEW `CaseFile` full frame, title \"THE CASE AGAINST THE LEOPARD SEAL\", `slots: 7`; credentials pop in left: \"HUNTS OTHER SEALS\", "
              "\"PLAYS WITH ITS FOOD\" (tiny penguin toss loop), red \"1916: ?\" sealed envelope",
         cam="small `drift`", sfx="`whoosh` (paper), `knock` -6 dB per credential",
         bg=flat("#0d1d26"), trans={"type": "dipBlack", "duration": 0.4},
         layers=[case(0, 0.2, full=True),
                 text("HUNTS OTHER SEALS", 560, 380, "@s1+0.4", 52), text("PLAYS WITH ITS FOOD", 560, 520, "@s2", 52),
                 text("1916: ?", 560, 660, "@s3+1.0", 64, "#ff5a4a")],
         cues=[("whoosh", 0.1, 0.5), ("knock", "@s1+0.4", 0.5), ("knock", "@s2", 0.5), ("knock", "@s3+1.0", 0.6)]),
    dict(id="s08_promise", at="s4", type="wide, deep",
         desc="`Ocean` `depth: 30`; small kneeling YOU on a floe at the top, big `LeopardSeal` `pose: cruise` below; `Headline` \"WHY YOU'D NEVER WANT TO MEET ONE\"; "
              "small grey `Tag` \"MOST CLIMB OUT FINE?\" (the quiet qualifier); `CaseFile` insert slot 7 \"EXHIBIT 7: ???\" grey + `Tag` \"4 DAYS · 0 BITES\"",
         cam="slow `panUp`", sfx="music bed returns",
         bg=ocean(30, 0.12, rays=6), camera={"preset": "panUp", "amount": 0.6},
         layers=[floe(960, 150, 520, 160), you(990, 95, 70, "kneel", props={"camera": True}),
                 seal(900, 700, 900, 280, "cruise"),
                 kicker("WHY YOU'D NEVER WANT TO MEET ONE", "@s4"),
                 tag("MOST CLIMB OUT FINE?", 480, 960, "@s5+1.0", "@s6", w=560, accent="#8a9aa0", size=32),
                 case(0, "@s6", slot7="grey", out="@end"), tag("4 DAYS · 0 BITES", 1540, 980, "@s6+2.4", w=520)]),
    # ---- R1
    dict(id="s09_size", at="r1a", type="side profile, true scale",
         desc="`LeopardSeal` `pxPerM: 400` (3.5 m = 1400 px) with two `You` NEW `lying` pose end to end below at the same `pxPerM`; `ScaleBar` \"~3.5 M\"; `Tag` \"BIGGEST = FEMALES\"",
         cam="`pushIn`", sfx="`tick` on the bar",
         bg=ocean(15),
         layers=[seal(960, 420, 1400, 420, "cruise", pxPerM=400),
                 you(610, 760, 700, "lying", pxPerM=400, start="@r1b+2.0", enter={"type": "drop", "at": "@r1b+2.0", "duration": 0.3}),
                 you(1310, 760, 700, "lying", pxPerM=400, start="@r1b+2.4", enter={"type": "drop", "at": "@r1b+2.4", "duration": 0.3}),
                 C("ScaleBar", 960, 640, 1400, 90, {"label": "~3.5 M", "at": "@r1b+0.6"}),
                 tag("BIGGEST = FEMALES", 960, 200, "@r1a+1.0", "@r1b", w=620), tag("2 x YOU", 960, 900, "@r1b+2.6", w=360)],
         cues=[("tick", "@r1b+0.6", 0.5)]),
    dict(id="s10_weight", at="r1c", type="graphic",
         desc="`Stat` \"~500 KG\" count-up; row of 7 `You` figures dropping in",
         cam="hold", sfx="`tick` roll",
         bg=ocean(15),
         layers=[C("Stat", 960, 330, 900, 260, {"value": 500, "from": 0, "prefix": "~", "suffix": " KG", "at": "@r1c+0.8", "duration": 1.2, "size": 150})]
         + [you(420 + i * 180, 720, 230, "stand", start=f"@r1c+{2.0 + i * 0.18:.2f}", enter={"type": "drop", "at": f"@r1c+{2.0 + i * 0.18:.2f}", "duration": 0.25}) for i in range(7)],
         cues=[("tick", "@r1c+0.8", 0.4)]),
    dict(id="s11_skull", at="r1d", type="split",
         desc="left: existing `Seal` (round-headed harbour seal) `Tag` \"MOST SEALS\"; right: `LeopardSeal` head with an `svg` skull-outline highlight, `Tag` \"LEOPARD SEAL\"",
         cam="`whip` left -> right", sfx="`whoosh`",
         bg=ocean(18), trans={"type": "whip", "duration": 0.3},
         layers=[C("Seal", 480, 540, 600, 260, {}), tag("MOST SEALS", 480, 760, "@r1d+0.3", w=420),
                 seal(1440, 540, 820, 300, "cruise", highlight="skull", start="@r1e", enter={"type": "slideLeft", "at": "@r1e", "duration": 0.3}),
                 tag("LEOPARD SEAL", 1440, 780, "@r1e+0.3", w=460)],
         cues=[("whoosh", "@r1e", 0.5)]),
    dict(id="s12_smile", at="r1f", type="close, head",
         desc="`LeopardSeal` head close, `highlight: 'mouth'` traces the upturned mouth line; red \"THE SMILE\"; `Tag` \"NOT A SMILE: A JAW LINE\"",
         cam="`pushIn` to the mouth", sfx="",
         bg=ocean(18), camera={"preset": "pushIn", "amount": 1.0},
         layers=[seal(860, 560, 1500, 520, "surface", highlight="mouth"), punch("THE SMILE", "@r1f+0.3", "@r1g"),
                 tag("NOT A SMILE: A JAW LINE", 960, 200, "@r1h", w=760)]),
    dict(id="s13_gape", at="r1i", type="close",
         desc="`LeopardSeal` `jaw` 0 -> 75° (cap; no fold-through) around a grey \"?\" card (the plant: nothing named, no camera shown)",
         cam="`shake` small on the open", sfx="`door_creak` (jaw)",
         bg=ocean(18), camera={"shake": [{"at": "@r1i+1.2", "duration": 0.35, "amplitude": 8}]},
         layers=[seal(900, 560, 1500, 520, "surface", jaw=[{"t": "@r1i+0.6", "v": 0}, {"t": "@r1i+1.6", "v": 75, "ease": "out"}]),
                 text("?", 1180, 520, "@r1i+1.8", 160, "#8a9aa0")],
         cues=[("door_creak", "@r1i+0.6", 0.5)]),
    dict(id="s14_fang", at="r1j", type="macro graphic",
         desc="`svg` fang beside a thumb silhouette, `ScaleBar` \"2.5 CM\"; split card \"FACE: PUPPY / JOB: CROCODILE\"; `CaseFile` insert, slot 1 \"THE FACE\" stamped",
         cam="`pullOut`", sfx="`knock` -6 dB (stamp)",
         bg=ocean(18), camera={"preset": "pullOut", "amount": 0.5},
         layers=[svg(FANG_SVG, 760, 480, 720, 480), C("ScaleBar", 700, 790, 300, 80, {"label": "2.5 CM", "at": "@r1j+1.2"}),
                 text("FACE: PUPPY", 600, 300, "@r1k", 70, "#ffffff"), text("JOB: CROCODILE", 600, 400, "@r1k+0.6", 70, "#ff5a4a"),
                 case(1, "@r1k+1.2", label="THE FACE")],
         cues=[("knock", "@r1k+1.3", 0.5)]),
    # ---- R2
    dict(id="s15_krill", at="r2a", type="macro",
         desc="`Headline` \"ON THE MENU\" -> red \"KRILL.\"; existing `explainer/Krill` swarm (several layers with `timeOffset`); `Tag` \"~6 CM ≈ YOUR LITTLE FINGER\"; "
              "then `svg` tooth row: three-cusp teeth interlock into a grid, `Tag` \"A SIEVE\"",
         cam="`pushIn` on the teeth", sfx="`pop`",
         bg=ocean(25, snow=120),
         layers=[kicker("ON THE MENU", "@r2a", "@r2c"), punch("KRILL.", "@r2b+0.5", "@r2c.end")]
         + [C("Krill", 300 + i * 260, 420 + (i % 2) * 120, 220, 110, {"timeOffset": i * 0.3}, start="@r2b+0.5", end="@r2d") for i in range(6)]
         + [tag("~6 CM ≈ YOUR LITTLE FINGER", 960, 640, "@r2c", "@r2d", w=820),
            svg(SIEVE_SVG, 960, 500, 1100, 360, start="@r2d", enter={"type": "fade", "at": "@r2d", "duration": 0.3}),
            tag("A SIEVE", 960, 760, "@r2e+0.8", w=360)],
         cues=[("pop", "@r2b+0.5", 0.5)]),
    dict(id="s16_taronga", at="r2f", type="map + diagram",
         desc="`Map` `views` zoom to `sydney`, pin \"TARONGA ZOO, SYDNEY · 2013 STUDY\"; then 3-step text diagram SUCK / SQUIRT / KEEP",
         cam="log-zoom", sfx="`whoosh_long`",
         bg=flat("#0f3a4a"),
         layers=[C("Map", 960, 540, 1920, 1080, {"views": [{"t": 0, "lon": 140, "lat": -40, "zoom": 1.2}, {"t": 1.6, "place": "sydney", "zoom": 5}],
                                                 "pins": [{"place": "sydney", "label": "TARONGA ZOO · 2013 STUDY", "at": 1.6}]}, end="@r2f+4.2"),
                 text("SUCK", 480, 540, "@r2f+4.2", 80), text("SQUIRT", 960, 540, "@r2f+4.8", 80), text("KEEP", 1440, 540, "@r2f+5.4", 80, "#6fd6e8")],
         cues=[("whoosh_long", 0.1, 0.5)]),
    dict(id="s17_garage", at="r2g", type="scale gag",
         desc="`BlueWhale` silhouette fills the top; the seal inside a garage outline (`svg`) below; `Tag` \"SAME TRICK\"",
         cam="`pullOut`", sfx="",
         bg=ocean(10), camera={"preset": "pullOut", "amount": 0.6},
         layers=[C("BlueWhale", 960, 230, 1800, 360, {"silhouette": "#2a4a58"}), svg(GARAGE_SVG, 960, 760, 760, 380),
                 seal(960, 820, 560, 180, "cruise"), tag("SAME TRICK", 960, 470, "@r2g+1.5", w=420)]),
    dict(id="s18_ladder", at="r2h", type="ladder",
         desc="icon `text` row FISH / SQUID; 6 `Penguin` silhouettes; then a prey ladder of existing `Seal` silhouettes growing left to right (crabeater pup, Weddell, fur seal pup, "
              "young elephant seal via `pxPerM`); `Orca` drifts in above, `Tag` \"ONLY PREDATOR\"; `CaseFile` insert, slot 2 \"EATS EVERYTHING\" stamped",
         cam="`drift` right", sfx="`pop` per icon, `knock` (stamp)",
         bg=ocean(20), camera={"preset": "drift", "amount": 1.0},
         layers=[text("FISH", 260, 260, "@r2h+1.5", 56), text("SQUID", 520, 260, "@r2h+1.9", 56)]
         + [penguin(760 + i * 110, 270, 120, "waddle", silhouette=True, start=f"@r2h+{2.2 + i * 0.1:.1f}") for i in range(6)]
         + [C("Seal", 300 + i * 420, 640, 220 + i * 120, 90 + i * 50, {"silhouette": "#9fb3bb"}, start=f"@r2h+{3.4 + i * 0.5:.1f}",
              enter={"type": "pop", "at": f"@r2h+{3.4 + i * 0.5:.1f}", "duration": 0.3}) for i in range(4)]
         + [C("Orca", 960, 160, 900, 260, {"silhouette": "#121c22"}, start="@r2i", keyframes=[{"t": "@r2i", "x": -400}, {"t": "@r2i+2.5", "x": 960}]),
            tag("ONLY PREDATOR", 960, 330, "@r2i+2.0", w=520), case(2, "@r2j+0.2", label="EATS EVERYTHING")],
         cues=[("pop", "@r2h+1.5", 0.4), ("pop", "@r2h+3.4", 0.4), ("knock", "@r2j+0.3", 0.5)]),
    # ---- R3
    dict(id="s19_doorway", at="r3a", type="cross-section",
         desc="NEW `IceFloe` with a penguin colony on top, `edgeStrip` dashed band \"THE DOORWAY\"; penguins diving in and scrambling out; YOU at the edge, `Tag` \"YOUR WAY OUT TOO\"; "
              "NEW `RIB` at the edge, `bites` marks appear on the black tube and a guard panel slides on, `Tag` \"TUBE GUARDS\" (throwaway plant)",
         cam="slow `pushIn` to the edge", sfx="`bubbles` (dives)",
         bg=ocean(6, 0.42, rays=4), camera={"preset": "pushIn", "amount": 0.6},
         layers=[floe(900, 470, 1300, 320, keel=True, colony=12, edgeStrip={"at": "@r3a+3.5"}),
                 tag("THE DOORWAY", 1540, 300, "@r3a+3.5", w=440, accent="#ff5a4a"),
                 you(1450, 360, 140, "stand", start="@r3b"), tag("YOUR WAY OUT TOO", 1450, 220, "@r3b+0.8", "@r3c", w=560),
                 C("RIB", 1680, 470, 420, 150, {"bites": [{"t": "@r3c+2.5", "v": 3}], "guards": {"at": "@r3c+3.5"}}, start="@r3c",
                   enter={"type": "slideLeft", "at": "@r3c", "duration": 0.4}),
                 tag("TUBE GUARDS", 1680, 610, "@r3c+3.6", w=420)],
         cues=[("bubbles", "@r3a+2.0", 0.4)]),
    dict(id="s20_patrol", at="r3d", type="under-surface",
         desc="`LeopardSeal` `pose: cruise`, `idle: false`, slight `rotate`, patrols under the edge with only the nostrils above the waterline",
         cam="`drift`", sfx="`heartbeat_slow` -12 dB",
         bg=ocean(6, 0.3, rays=3), camera={"preset": "drift", "amount": 0.6},
         layers=[floe(760, 300, 1100, 300, keel=True, colony=8),
                 seal(1500, 380, 900, 280, "cruise", rotate=-4, keyframes=[{"t": 0, "x": 1700}, {"t": "@end", "x": 1300}])],
         cues=[("heartbeat_slow", 0.2, 0.25)]),
    dict(id="s21_launch", at="r3f", type="medium",
         desc="three `Penguin` `pose: airborne` rocket out onto the floe; ghosted replay of the 0:12 penguin past the boot (`opacity` 0.5), `Tag` \"IT WAS ESCAPING\"",
         cam="hold", sfx="`whoosh` x3",
         bg=ocean(4, 0.46, rays=4),
         layers=hook_frame(extra=[penguin(500 + i * 160, 700, 120, "airborne", start=f"@r3f+{1.0 + i * 0.4:.1f}",
                                          keyframes=[{"t": f"@r3f+{1.0 + i * 0.4:.1f}", "y": 760}, {"t": f"@r3f+{1.6 + i * 0.4:.1f}", "y": 330, "ease": "out"}]) for i in range(3)]
                                 + [penguin(980, 330, 140, "airborne", opacity=0.5, start="@r3g"), tag("IT WAS ESCAPING", 960, 200, "@r3g+1.0", w=560)]),
         cues=[("whoosh", "@r3f+1.0", 0.4), ("whoosh", "@r3f+1.4", 0.4), ("whoosh", "@r3f+1.8", 0.4)]),
    dict(id="s22_grab", at="r3h", type="action, stylised",
         desc="`LeopardSeal` `pose: lunge` up at a swimming `Penguin`; red \"GRAB\"; hard cut on contact to splash `circle` rings + white feather-puff `particles` (`dust`); "
              "then motion streaks only (no penguin in the mouth, no gore)",
         cam="`shake` 0.4 s", sfx="`impact`, `bubbles`",
         bg=ocean(8), camera={"shake": [{"at": "@r3h+1.0", "duration": 0.4}]},
         layers=[penguin(1100, 360, 130, "swim", end="@r3h+1.0"),
                 seal(700, 640, 900, 300, "lunge", end="@r3h+1.0", keyframes=[{"t": 0, "x": 500, "y": 760}, {"t": "@r3h+1.0", "x": 900, "y": 460, "ease": "in"}]),
                 punch("GRAB", "@r3h+1.0", "@r3i")]
         + rings(1100, 380, "@r3h+1.0", 3, "rgba(255,255,255,0.7)", 220, 0.6)
         + [{"type": "particles", "preset": "dust", "count": 40, "color": "#ffffff", "x": 1100, "y": 380, "width": 600, "height": 400, "start": "@r3h+1.0", "speed": 2.0}],
         cues=[("impact", "@r3h+1.0", 0.6), ("bubbles", "@r3h+1.1", 0.4)]),
    dict(id="s23_myth", at="r3j", type="graphic",
         desc="`svg` old book page \"SKINS ITS PREY\" with a red \"WRONG\" stamp; `Tag` \"CAN'T CHEW\"; `CaseFile` insert, slot 3 \"OWNS THE ICE EDGE\" stamped; "
              "on {D:r3l} (turnstile) the frame darkens to near black",
         cam="`whip` in", sfx="`knock` (stamp)",
         bg=flat("#1a1712"), trans={"type": "whip", "duration": 0.3},
         layers=[svg(BOOK_SVG, 800, 520, 900, 580), text("WRONG", 820, 520, "@r3j+1.6", 120, "#ff5a4a", rotate=-12, strokeColor="#ff5a4a"),
                 tag("CAN'T CHEW", 800, 880, "@r3j+3.0", w=420), case(3, "@r3k+0.4", label="OWNS THE ICE EDGE"),
                 {"type": "rect", "x": 960, "y": 540, "width": 1920, "height": 1080, "fill": "#000000", "opacity": 0, "z": 40, "depth": 0,
                  "keyframes": [{"t": "@r3l", "opacity": 0}, {"t": "@r3l+0.6", "opacity": 0.85}]}],
         cues=[("knock", "@r3j+1.6", 0.5), ("knock", "@r3k+0.5", 0.5)]),
    # ---- R4 game
    dict(id="s24_game", at="r4a", type="diagram (new background on the turnstile's next word)",
         desc="new deep-blue background; `Headline` \"IT DOESN'T ALWAYS EAT\"; NEW `LoopDiagram` (or `svg`) GRAB -> RELEASE -> CHASE -> GRAB with `Penguin` + seal icons, counter x1, x2, x3; "
              "then `Options` \"PRACTICE? / PLAY? / KILLING TIME?\" (`itemAt` per question) and a red \"UNSOLVED\" stamp; `CaseFile` insert, slot 4 \"PLAYS WITH PREY\" stamped",
         cam="hold, loop animates", sfx="`click` per loop, `knock` (stamp)",
         bg=flat("#0b2540"),
         layers=[kicker("IT DOESN'T ALWAYS EAT", "@r4a"),
                 svg(LOOP_SVG, 960, 560, 900, 540, end="@r4d", idle=[{"type": "spin", "speed": 0.0}]),
                 text("x1", 1500, 380, "@r4b+2.5", 64, TEAL, end="@r4d"), text("x2", 1500, 480, "@r4b+4.0", 64, TEAL, end="@r4d"),
                 text("x3", 1500, 580, "@r4c", 64, "#ff5a4a", end="@r4d"),
                 C("Options", 960, 560, 1100, 520, {"title": "WHY?", "items": ["PRACTICE?", "PLAY?", "KILLING TIME?"], "at": "@r4d",
                                                    "itemAt": ["@r4d", "@r4e", "@r4f"]}, start="@r4d"),
                 text("UNSOLVED", 960, 560, "@r4g+0.3", 150, "#ff5a4a", rotate=-10, opacity=0.9, z=22),
                 case(4, "@r4h+0.5", label="PLAYS WITH PREY")],
         cues=[("click", "@r4b+2.5", 0.4), ("click", "@r4b+4.0", 0.4), ("click", "@r4c", 0.4), ("knock", "@r4g+0.3", 0.6), ("knock", "@r4h+0.6", 0.5)]),
    # ---- R5 senses + song
    dict(id="s25_whiskers", at="r5a", type="close, murk",
         desc="`Ocean` `depth: 60`, `snow` heavy; seal head with `highlight: 'whiskers'` fan; a swimming `Penguin` leaves a wavy `svg` wake the whiskers trace; `Tag` \"PROBABLY\"",
         cam="`pushIn`", sfx="`whoosh_long` soft",
         bg=ocean(60, snow=200),
         layers=[kicker("HOW DOES IT FIND YOU?", "@r5a", "@r5c"), seal(700, 560, 1100, 380, "cruise", highlight="whiskers"),
                 penguin(1500, 420, 120, "swim", keyframes=[{"t": "@r5c", "x": 1700}, {"t": "@end", "x": 1300}]),
                 tag("PROBABLY", 1200, 760, "@r5c+1.5", w=380)],
         cues=[("whoosh_long", "@r5c", 0.3)]),
    dict(id="s26_flashback", at="r5e", type="flashback",
         desc="`grade` warm-sepia tint; the 0:18 under-ice shot with rings rising into the floe; red \"IT SINGS\"",
         cam="`dipBlack` in", sfx="NEW `seal_trill` returns, clearer",
         bg=ocean(25, 0.3, rays=2), trans={"type": "dipBlack", "duration": 0.4},
         grade={"tint": "#c8a060", "tintOpacity": 0.3, "saturate": 0.7},
         layers=hook_frame(extra=rings(960, 900, 0.2) + [punch("IT SINGS", "@r5f+1.6")]),
         cues=[("underwater_rumble", 0.1, 0.6)]),
    dict(id="s27_singer", at="r5g", type="medium",
         desc="`LeopardSeal` upside down (layer `rotate: 180` + `flipX`), `idle` `sway` for the rock; `circle` rings from the chest; `Stat` \"177 dB (UNDERWATER)\"; "
              "five waveform chips 1-5; rings climb into a tiny floe; `Tag` \"WHY? UNCONFIRMED\"",
         cam="slow `drift`", sfx="trill layered",
         bg=ocean(35),
         layers=[seal(760, 560, 1000, 340, "cruise", rotate=180, flipX=True, idle=[{"type": "sway", "amount": 6, "speed": 0.4}])]
         + rings(760, 600, 0.5, 4, "rgba(160,220,255,0.6)", 260)
         + [C("Stat", 1450, 420, 700, 200, {"value": 177, "from": 120, "suffix": " dB", "label": "UNDERWATER", "at": "@r5h", "duration": 1.0, "size": 110})]
         + [text(str(i + 1), 1200 + i * 110, 640, f"@r5h+{2.5 + i * 0.3:.1f}", 48, TEAL, background="rgba(0,0,0,0.35)", padding=14, radius=10) for i in range(5)]
         + [tag("WHY? UNCONFIRMED", 1450, 800, "@r5i", w=560)],
         cues=[("underwater_rumble", 0.3, 0.5)]),
    dict(id="s28_below", at="r5j", type="wide",
         desc="rings expand to fill the frame and pass under a tiny floe with a tiny kneeling YOU; red \"SOMEWHERE BELOW YOU\"; `CaseFile` insert, slot 5 \"HEARS AND SINGS\" stamped",
         cam="`pullOut` wide", sfx="`knock` (stamp)",
         bg=ocean(10, 0.3, rays=3), camera={"preset": "pullOut", "amount": 0.8},
         layers=[floe(960, 300, 360, 120, keel=True), you(975, 262, 50, "kneel", props={"camera": True})]
         + rings(960, 820, 0.1, 5, "rgba(160,220,255,0.5)", 700, 1.4)
         + [punch("SOMEWHERE BELOW YOU", "@r5k"), case(5, "@r5k+1.2", label="HEARS AND SINGS")],
         cues=[("knock", "@r5k+1.3", 0.5)]),
    # ---- re-immersion
    dict(id="s29_again", at="ri1", type="wide, surface split (0:00 framing)",
         desc="exact 0:00 framing; `IceFloe` `edgeStrip` doorway band appears under the kneeling YOU; three exhibit icons (text chips) EATS SEALS / PLAYS / SINGS orbit the rising face; red \"INTERESTING\"",
         cam="slow `pushIn`", sfx="`door_creak` low, trill",
         bg=ocean(4, 0.46, rays=5), camera={"preset": "pushIn", "amount": 0.6},
         layers=[floe(960, 500, 1000, 340, keel=True, edgeStrip={"at": "@ri2+0.8"}), you(1040, 372, 170, "kneel", props={"camera": True}, z=3),
                 seal(1580, 560, 600, 220, "surface", start="@ri3", enter={"type": "slideUp", "at": "@ri3", "duration": 0.6})]
         + [text(w, 1250 + i * 220, 230 + (i % 2) * 90, f"@ri3+{1.0 + i * 1.0:.1f}", 40, TEAL, background="rgba(0,0,0,0.4)", padding=12, radius=10)
            for i, w in enumerate(["EATS SEALS", "PLAYS", "SINGS"])]
         + [punch("INTERESTING", "@ri5+0.4")],
         cues=[("door_creak", 0.3, 0.2), ("underwater_rumble", "@ri3", 0.3)]),
    # ---- R6 record
    dict(id="s30_1916", at="r6a", type="sepia story",
         desc="`Headline` \"AND PEOPLE?\"; `grade` sepia; document card \"ENDURANCE EXPEDITION · 1916\" (`text` on a paper `rect`); tents on a floe; "
              "`You` `pose: run` on skis as Orde-Lees; `LeopardSeal` head and foreparts only, over a floe ridge (no body on the snow); dotted chase path; "
              "the seal drops out of frame and reappears ahead; `Tag` \"FRANK WILD\"; freeze; tin plate `svg`, `Tag` \"DINNER\"",
         cam="`drift` along the chase, freeze", sfx="`footsteps`, `impact` (single off-screen crack, no gun shown), `stinger` on DINNER",
         bg=flat("#d8ccb0"), grade={"tint": "#a07840", "tintOpacity": 0.35, "saturate": 0.5},
         layers=[kicker("AND PEOPLE?", "@r6a", "@r6b", color="red"),
                 {"type": "rect", "x": 960, "y": 300, "width": 900, "height": 140, "fill": "#efe6cf", "stroke": "#6a5a3a", "strokeWidth": 4, "start": "@r6b", "end": "@r6c", "depth": 0},
                 text("ENDURANCE EXPEDITION · 1916", 960, 300, "@r6b", 48, "#3a3020", end="@r6c"),
                 floe(960, 760, 1900, 300),
                 you(1300, 600, 160, "run", start="@r6c", keyframes=[{"t": "@r6d", "x": 1300}, {"t": "@r6e", "x": 1650}]),
                 seal(700, 680, 520, 200, "surface", start="@r6c+2.0", end="@r6d+1.2"),
                 seal(1820, 680, 520, 200, "surface", flipX=True, start="@r6d+2.6", end="@r6e+1.5"),
                 tag("FRANK WILD", 960, 220, "@r6e+0.8", "@r6f", w=420),
                 svg(PLATE_SVG, 960, 520, 300, 300, start="@r6f+0.5", enter={"type": "pop", "at": "@r6f+0.5", "duration": 0.3}),
                 tag("DINNER", 960, 720, "@r6f+0.8", w=320)],
         cues=[("footsteps", "@r6d", 0.4), ("impact", "@r6e+0.9", 0.5), ("stinger", "@r6f+0.8", 0.4)]),
    dict(id="s31_1985", at="r6g", type="plain story card",
         desc="neutral grade; card \"1985 · GARETH WOOD\"; a standing figure at an ice crack, seal head rising through it; `Tag` \"BITTEN TWICE · KICKED FREE\" (no jokes from here to the 2003 card)",
         cam="slow `pushIn`", sfx="none",
         bg=ocean(6, 0.5, rays=2),
         layers=[kicker("1985 · GARETH WOOD", "@r6g"), floe(960, 520, 1700, 300), you(1000, 390, 170, "stand"),
                 seal(880, 470, 420, 160, "surface", start="@r6g+3.0", enter={"type": "slideUp", "at": "@r6g+3.0", "duration": 0.4}),
                 tag("BITTEN TWICE · KICKED FREE", 960, 760, "@r6h+0.5", w=760)]),
    dict(id="s32_pivot", at="pause1", type="tonal pivot (silence)",
         desc="5 s of still, empty grey sea under an overcast sky; no text, no figure; music down to a single pad",
         cam="locked off", sfx="none",
         bg=ocean(2, 0.5, rays=0, skyTop="#7d8790", skyBottom="#a9b2b8"), trans={"type": "fade", "duration": 1.0}),
    dict(id="s33_rothera", at="r6i", type="sober, still",
         desc="`Map` `views` zoom to NEW place `rothera`, pin \"ROTHERA RESEARCH STATION\"; calm text card \"KIRSTY BROWN · MARINE BIOLOGIST · JULY 2003\"; "
              "`Tag` \"1 KNOWN HUMAN DEATH\"; `CaseFile` insert, slot 6 \"HAS KILLED\", grey stamp; then 3 s black card (silence)",
         cam="very slow `pushIn`, no shake", sfx="none (pad only)",
         bg=flat("#0f3a4a"), camera={"preset": "pushIn", "amount": 0.25},
         layers=[C("Map", 960, 540, 1920, 1080, {"views": [{"t": 0, "lon": -64, "lat": -66, "zoom": 2.5}, {"t": 2.5, "lon": -68.13, "lat": -67.57, "zoom": 6}],
                                                 "pins": [{"lon": -68.13, "lat": -67.57, "label": "ROTHERA RESEARCH STATION", "at": 2.5}]}),
                 {"type": "rect", "x": 960, "y": 860, "width": 1300, "height": 120, "fill": "rgba(0,0,0,0.55)", "radius": 12, "depth": 0, "start": "@r6i+3.0", "z": 15},
                 text("KIRSTY BROWN · MARINE BIOLOGIST · JULY 2003", 960, 860, "@r6i+3.0", 44, "#ffffff", z=16, enter={"type": "fade", "at": "@r6i+3.0", "duration": 0.8}),
                 tag("1 KNOWN HUMAN DEATH", 960, 200, "@r6m+0.5", w=560, accent="#9aa6aa"),
                 case(6, "@r6m.end+0.2", slot7="grey", label="HAS KILLED", out="@pause2"),
                 {"type": "rect", "x": 960, "y": 540, "width": 1920, "height": 1080, "fill": "#000000", "depth": 0, "z": 50, "start": "@pause2",
                  "enter": {"type": "fade", "at": "@pause2", "duration": 0.6}}]),
    # ---- climax
    dict(id="s34_hypo", at="c1", type="surface-split side view",
         desc="`Tag` \"HYPOTHETICAL\"; side view: YOU (`pose: panic`) in the water at the floe edge, a long seal silhouette rising below (no top-down shot); `Options` appears (4 items)",
         cam="slow `pushIn`", sfx="`heartbeat_slow` (tension pulse)",
         bg=ocean(6, 0.42, rays=3), trans={"type": "fade", "duration": 0.6}, camera={"preset": "pushIn", "amount": 0.5},
         layers=[tag("HYPOTHETICAL", 960, 120, "@c1", "@c3", w=520, accent="#8a9aa0"),
                 floe(560, 440, 900, 280, keel=True), you(1100, 480, 160, "panic", start="@c2"),
                 seal(1100, 960, 700, 220, "cruise", silhouette=SEAL_DARK, start="@c2+2.5", keyframes=[{"t": "@c2+2.5", "y": 1100}, {"t": "@end", "y": 860}]),
                 C("Options", 1480, 560, 760, 560, {"title": "YOUR OPTIONS", "items": ["SWIM FOR THE BOAT", "CLIMB BACK ONTO THE ICE", "HIDE UNDER THE FLOE", "PLAY DEAD"],
                                                    "at": "@c3", "stagger": 0.25}, start="@c3", depth=0, z=20)],
         cues=[("heartbeat_slow", 0.5, 0.4)]),
    dict(id="s35_boat", at="c4", type="graphic",
         desc="`SpeedBars` SEAL ~40 KM/H vs YOU ~3 KM/H; the bitten `RIB` tube from {D:r3c} (callback); `Options` `strikes` index 0",
         cam="hold", sfx="`click` (strike)",
         bg=ocean(10),
         layers=[C("SpeedBars", 760, 460, 1200, 420, {"title": "BURST SPEED", "rows": [{"label": "SEAL", "value": 40, "unit": "KM/H", "color": "#ff5a4a", "text": "~40 KM/H (OFTEN QUOTED)"},
                                                                                     {"label": "YOU", "value": 3, "unit": "KM/H", "color": "#6fd6e8", "text": "~3 KM/H"}], "max": 45, "at": "@c5"}),
                 C("RIB", 760, 820, 520, 180, {"bites": 3}, start="@c6", enter={"type": "pop", "at": "@c6", "duration": 0.3}),
                 C("Options", 1560, 540, 640, 520, {"title": "YOUR OPTIONS", "items": ["SWIM FOR THE BOAT", "CLIMB BACK ONTO THE ICE", "HIDE UNDER THE FLOE", "PLAY DEAD"],
                                                    "strikes": [{"index": 0, "at": "@c6.end"}], "select": {"index": 0, "at": 0}, "size": 0.8}, depth=0, z=20)],
         cues=[("click", "@c6.end", 0.6)]),
    dict(id="s36_ice", at="c7", type="cross-section",
         desc="the doorway strip + the 1985 card + the 1916 chase path overlay; `strikes` index 1",
         cam="`whip` in", sfx="`click`",
         bg=ocean(6, 0.42, rays=3), trans={"type": "whip", "duration": 0.3},
         layers=[floe(760, 470, 1300, 320, keel=True, edgeStrip={"at": 0.2}), tag("THE DOORWAY", 1300, 300, "@c8", w=420, accent="#ff5a4a"),
                 text("1985", 500, 260, "@c8+2.0", 54, "#ffffff", background="rgba(0,0,0,0.4)", padding=12),
                 text("1916", 800, 260, "@c8+4.5", 54, "#e8d8b0", background="rgba(0,0,0,0.4)", padding=12),
                 C("Options", 1560, 540, 640, 520, {"title": "YOUR OPTIONS", "items": ["SWIM FOR THE BOAT", "CLIMB BACK ONTO THE ICE", "HIDE UNDER THE FLOE", "PLAY DEAD"],
                                                    "strikes": [{"index": 0, "at": 0}, {"index": 1, "at": "@c8.end"}], "select": {"index": 1, "at": 0}, "size": 0.8}, depth=0, z=20)],
         cues=[("whoosh", 0.0, 0.4), ("click", "@c8.end", 0.6)]),
    dict(id="s37_hide", at="c9", type="under-ice gag",
         desc="under the floe: YOU kicking, wavy `svg` wake lines trail toward the seal's whisker fan; a cartoon bell (`svg`) over YOU wobbles on every kick; `strikes` index 2",
         cam="`panUp` under the ice", sfx="`ding` per kick (the bell), `stinger` on the joke, `click`",
         bg=ocean(20, 0.12, rays=1),
         layers=[floe(960, 120, 1900, 260, keel=True), you(1000, 420, 150, "panic", idle=[{"type": "jitter", "amount": 4, "speed": 2}]),
                 svg(BELL_SVG, 1000, 300, 90, 90, start="@c11", idle=[{"type": "sway", "amount": 18, "speed": 2}], enter={"type": "pop", "at": "@c11", "duration": 0.25}),
                 seal(380, 600, 700, 240, "cruise", highlight="whiskers", start="@c10"),
                 C("Options", 1560, 540, 640, 520, {"title": "YOUR OPTIONS", "items": ["SWIM FOR THE BOAT", "CLIMB BACK ONTO THE ICE", "HIDE UNDER THE FLOE", "PLAY DEAD"],
                                                    "strikes": [{"index": 0, "at": 0}, {"index": 1, "at": 0}, {"index": 2, "at": "@c11.end"}], "select": {"index": 2, "at": 0}, "size": 0.8}, depth=0, z=20)],
         cues=[("ding", "@c11", 0.4), ("ding", "@c11+0.6", 0.4), ("stinger", "@c11.end", 0.35), ("click", "@c11.end+0.2", 0.6)]),
    dict(id="s38_limp", at="c12", type="diagram",
         desc="the R4 GRAB -> RELEASE loop with `You` `pose: panic` in the penguin's slot; `strikes` index 3",
         cam="hold", sfx="`click`",
         bg=flat("#0b2540"),
         layers=[svg(LOOP_SVG, 760, 560, 900, 540), you(760, 560, 160, "panic", start="@c13"),
                 C("Options", 1560, 540, 640, 520, {"title": "YOUR OPTIONS", "items": ["SWIM FOR THE BOAT", "CLIMB BACK ONTO THE ICE", "HIDE UNDER THE FLOE", "PLAY DEAD"],
                                                    "strikes": [{"index": 0, "at": 0}, {"index": 1, "at": 0}, {"index": 2, "at": 0}, {"index": 3, "at": "@c14.end"}], "select": {"index": 3, "at": 0}, "size": 0.8}, depth=0, z=20)],
         cues=[("click", "@c14.end", 0.6)]),
    dict(id="s39_verdict", at="c15", type="black card",
         desc="`Headline` white \"THE WATER IS ITS HOME. THE ICE IS ITS TRAP.\" then red \"OUT OF MOVES.\"",
         cam="hold, `dipBlack` out", sfx="single `boom`, then silence",
         bg=flat("#000000"),
         layers=[C("Headline", 960, 440, 1600, 260, {"text": "THE WATER IS ITS HOME.\nTHE ICE IS ITS TRAP.", "at": "@c16+1.0", "size": 72, "color": "white"}, depth=0),
                 C("Headline", 960, 700, 1400, 150, {"text": "OUT OF MOVES.", "at": "@c16.end-0.8", "size": 90, "color": "red"}, depth=0)],
         cues=[("boom", "@c16.end-0.8", 0.6)]),
    # ---- twist
    dict(id="s40_but", at="t1", type="map",
         desc="`Headline` \"BUT...\"; the grey qualifier `Tag` from {D:s5} returns white: \"MOST CLIMB OUT FINE\"; `Map` Antarctic Peninsula with research-diver and kayak dots multiplying; "
              "`Stat` \"100,000+\" label \"VISITORS A SEASON\" (VO says the same figure)",
         cam="slow `pullOut`", sfx="music bed returns",
         bg=flat("#0f3a4a"), trans={"type": "dipBlack", "duration": 0.5},
         layers=[C("Map", 960, 540, 1920, 1080, {"views": [{"t": 0, "lon": -62, "lat": -65, "zoom": 3}]}),
                 kicker("BUT...", "@t1"), tag("MOST CLIMB OUT FINE", 960, 220, "@t2", "@t3", w=640),
                 C("Stat", 1400, 820, 760, 200, {"value": 100000, "from": 0, "suffix": "+", "label": "VISITORS A SEASON", "at": "@t3+3.0", "duration": 1.4, "size": 96}, depth=0, z=20)]),
    dict(id="s41_strip", at="t4", type="strip",
         desc="four panels CIRCLE / STARE / GAPE / LEAVE (`svg` labels) over a seal and a `Diver`",
         cam="`drift` right", sfx="",
         bg=ocean(12), camera={"preset": "drift", "amount": 0.6},
         layers=[C("Diver", 1250, 480, 420, 200, {"arms": "side"}), seal(560, 520, 700, 240, "cruise", start="@t5",
                                                                        keyframes=[{"t": "@t5", "x": 560}, {"t": "@t5.end", "x": -300}]),
                 svg(STRIP_SVG, 960, 860, 1600, 120, start="@t5", enter={"type": "wipeRight", "at": "@t5", "duration": 3.5})]),
    dict(id="s42_restraint", at="t6", type="timeline",
         desc="row of field-season ticks 1960s -> 2020s (`svg`), one grey tick at 2003 (no per-icon death ratio); `Tag` \"1 KNOWN DEATH · DECADES OF DIVING\"; red \"RESTRAINT\"",
         cam="`pushIn` on the grey tick", sfx="`heartbeat_slow` once",
         bg=flat("#0b1a22"), camera={"preset": "pushIn", "amount": 0.4},
         layers=[svg(TIMELINE_SVG, 960, 460, 1500, 170, enter={"type": "wipeRight", "duration": 1.5}),
                 tag("1 KNOWN DEATH · DECADES OF DIVING", 960, 650, "@t6+1.5", w=900, accent="#9aa6aa"),
                 punch("RESTRAINT", "@t7+1.6", y=820)],
         cues=[("heartbeat_slow", "@t6+1.6", 0.3)]),
    dict(id="s43_cat", at="t8", type="gag",
         desc="a boxy dashed outline around a `You` figure; the seal peers at it from the left, the top, then the right, cat-style (three quick cuts via keyframes); `CaseFile` insert, \"EXHIBIT 7: ???\" pulses",
         cam="hold", sfx="`pop` per peek",
         bg=ocean(10),
         layers=[svg(BOX_SVG, 960, 560, 420, 260), you(960, 560, 200, "stand"),
                 seal(560, 560, 500, 180, "surface", start="@t8+2.6", end="@t8+3.6"),
                 seal(960, 300, 500, 180, "surface", rotate=90, start="@t8+3.6", end="@t8+4.6"),
                 seal(1360, 560, 500, 180, "surface", flipX=True, start="@t8+4.6", end="@t9"),
                 case(6, "@t9+0.4", slot7="pulse", out="@end")],
         cues=[("pop", "@t8+2.6", 0.3), ("pop", "@t8+3.6", 0.3), ("pop", "@t8+4.6", 0.3)]),
    # ---- payoff
    dict(id="s44_nicklen", at="p1", type="medium",
         desc="`Map` pin \"ANTARCTIC PENINSULA · 2006\" (2 s), then `Diver` with NEW `camera` prop beside `LeopardSeal` and `ScaleBar` \"~3.5 M\"; the {D:r1i} gape shot again, "
              "now with the diver's camera inside the 75° gape; red \"AND HIS HEAD\"",
         cam="`pushIn`", sfx="`door_creak` (jaw), `boom` low on the punch",
         bg=ocean(10), camera={"preset": "pushIn", "amount": 0.7},
         layers=[C("Map", 960, 540, 1920, 1080, {"views": [{"t": 0, "lon": -62, "lat": -65, "zoom": 4}], "pins": [{"lon": -63, "lat": -64.8, "label": "ANTARCTIC PENINSULA · 2006", "at": 0.3}]}, end="@p1+2.6"),
                 C("Diver", 1300, 520, 520, 240, {"camera": True, "arms": "forward"}, start="@p1+2.6", flipX=True),
                 seal(620, 560, 1000, 330, "cruise", start="@p1+2.6", jaw=[{"t": "@p2+1.5", "v": 0}, {"t": "@p2+2.5", "v": 75, "ease": "out"}],
                      keyframes=[{"t": "@p2", "x": 620}, {"t": "@p2+2.0", "x": 900}]),
                 C("ScaleBar", 620, 780, 1000, 80, {"label": "~3.5 M", "at": "@p1+4.0"}, end="@p2"),
                 punch("AND HIS HEAD", "@p3")],
         cues=[("door_creak", "@p2+1.5", 0.5), ("boom", "@p3", 0.4)]),
    dict(id="s45_gifts", at="p4", type="sequence",
         desc="seal backs off and returns with a `Penguin` (NEW `carry` prop on the seal, so the penguin follows the jaw); counter cards GIFT 1 LIVE / GIFT 2 LIVE / GIFT 3 SLOWER / "
              "GIFT 4 READY TO EAT (`Headline` swaps; limp cartoon penguin, nothing drawn); 1 s held beat after \"Then dead.\"",
         cam="cut on each gift", sfx="`pop` per card",
         bg=ocean(10),
         layers=[C("Diver", 1350, 520, 520, 240, {"camera": True, "arms": "forward"}, flipX=True),
                 seal(560, 560, 900, 300, "cruise", carry=[{"t": "@p4+1.5", "v": "penguin"}],
                      keyframes=[{"t": 0, "x": 560}, {"t": "@p4+0.8", "x": 200}, {"t": "@p4+1.6", "x": 560}]),
                 punch("A PENGUIN", "@p4+1.8", "@p5")]
         + [C("Headline", 960, 150, 1100, 120, {"text": t_, "at": a_, "out": o_, "size": 64, "color": c_}, depth=0, z=20)
            for t_, a_, o_, c_ in [("GIFT 1: LIVE", "@p5", "@p6", "white"), ("GIFT 2: LIVE", "@p6", "@p7", "white"),
                                   ("GIFT 3: SLOWER", "@p7", "@p8", "white"), ("GIFT 4: READY TO EAT", "@p8", None, "yellow")]],
         cues=[("pop", "@p5", 0.4), ("pop", "@p6", 0.4), ("pop", "@p7", 0.4), ("pop", "@p8", 0.4)]),
    dict(id="s46_days", at="p9", type="medium",
         desc="`Stat` `prefix: 'DAY '` from 1 to 4 (no `Timer`); bubble `particles` over the camera; her verdict typed as four short `text` lines over the diver; "
              "`Tag` \"USELESS HUNTER (HER VIEW)\"; small stamp \"FAIR\"",
         cam="`drift`", sfx="`bubbles`, `typing` for the verdict, `knock` light on FAIR",
         bg=ocean(10),
         layers=[C("Diver", 1250, 560, 560, 260, {"camera": True, "arms": "forward"}, flipX=True),
                 {"type": "particles", "preset": "bubbles", "count": 80, "x": 1150, "y": 480, "width": 500, "height": 500, "start": "@p9+2.5", "end": "@p10"},
                 C("Stat", 520, 300, 600, 200, {"value": 4, "from": 1, "prefix": "DAY ", "decimals": 0, "at": "@p9+4.0", "duration": 2.0, "size": 110}, depth=0)]
         + [text(t_, 520, 520 + i * 80, f"@p10+{2.0 + i * 0.7:.1f}", 50, "#ffffff", typewriter={"at": f"@p10+{2.0 + i * 0.7:.1f}", "cps": 30}, align="left")
            for i, t_ in enumerate(["CLUMSY THING.", "BIG EYE.", "CAN'T HUNT.", "NEEDS FEEDING."])]
         + [tag("USELESS HUNTER (HER VIEW)", 1250, 820, "@p10+4.8", w=700),
            text("FAIR", 1550, 300, "@p11+0.8", 90, "#ffd34d", rotate=-12)],
         cues=[("bubbles", "@p9+2.5", 0.4), ("typing", "@p10+2.0", 0.3), ("knock", "@p11+0.8", 0.3)]),
    dict(id="s47_offer", at="p12", type="diagram + map",
         desc="the R4 loop `svg` returns with the arrow now running seal -> diver; `Map` pin NEW place `southGeorgia` \"SOUTH GEORGIA\"; two seals share one penguin; "
              "`Tag` \"AN OFFER TO COOPERATE?\"; `CaseFile` insert, slot 7 \"FED A HUMAN\", yellow stamp",
         cam="`whip`", sfx="`ding`, `knock` (light stamp)",
         bg=flat("#0b2540"), trans={"type": "whip", "duration": 0.3},
         layers=[svg(LOOP_SVG, 960, 560, 900, 540, end="@p13"),
                 C("Map", 960, 540, 1920, 1080, {"views": [{"t": 0, "lon": -36.5, "lat": -54.3, "zoom": 6}], "pins": [{"lon": -36.5, "lat": -54.3, "label": "SOUTH GEORGIA", "at": 0.3}]},
                   start="@p13", end="@p13+3.5"),
                 seal(700, 600, 700, 240, "cruise", start="@p13+3.5"), seal(1220, 600, 700, 240, "cruise", flipX=True, start="@p13+3.5"),
                 penguin(960, 640, 90, "limp", start="@p13+3.5"),
                 tag("AN OFFER TO COOPERATE?", 960, 820, "@p13+4.0", w=760),
                 case(7, "@p14+2.0", slot7="yellow", label="FED A HUMAN", out="@end")],
         cues=[("ding", "@p13+4.0", 0.4), ("knock", "@p14+2.1", 0.3)]),
    # ---- bookend
    dict(id="s48_bookend", at="b1", type="wide, surface split (0:00 framing)",
         desc="exact 0:00 framing; `Tag` \"-2 °C WATER\" + green tick returns; rings under the floe (the singer); the airborne penguin replay ghosted; "
              "the seal face at the edge; red \"CURIOUS\"; a `Penguin` `pose: limp` slides onto the floe at YOU's knees; `You` `pose: shrug`",
         cam="slow `pullOut`", sfx="trill, `door_creak` low, `bubbles` + `stinger` (comic) on the penguin",
         bg=ocean(4, 0.46, rays=5), camera={"preset": "pullOut", "amount": 0.5},
         layers=[floe(960, 500, 1000, 340, keel=True), you(1040, 372, 170, "kneel", props={"camera": True}, end="@b6"),
                 you(1040, 372, 170, "shrug", start="@b6"),
                 tag("-2 °C WATER  ✓", 960, 210, "@b2+1.0", "@b3", w=560, accent="#5fd38a")]
         + rings(960, 900, "@b3", 4)
         + [penguin(980, 330, 140, "airborne", opacity=0.45, start="@b4", end="@b5"),
            seal(1500, 560, 600, 220, "surface", start="@b5"), punch("CURIOUS", "@b5+2.6"),
            penguin(1300, 430, 110, "limp", start="@b6+0.5", keyframes=[{"t": "@b6+0.5", "x": 1400}, {"t": "@b6+1.2", "x": 1120, "ease": "out"}])],
         cues=[("underwater_rumble", "@b3", 0.4), ("bubbles", "@b6+0.5", 0.4), ("stinger", "@b6+1.3", 0.3)]),
    # ---- CTA
    dict(id="s49_end", at="x1", type="end card",
         desc="finished `CaseFile` board (7 stamps) full frame held 5 s; `Headline` \"WALRUS OR ELEPHANT SEAL?\"; end-screen slot right",
         cam="hold 5 s", sfx="music out",
         bg=flat("#0d1d26"), trans={"type": "fade", "duration": 0.5},
         layers=[case(7, 0.0, slot7="yellow", full=True), C("Headline", 960, 980, 1400, 120, {"text": "WALRUS OR ELEPHANT SEAL?", "at": 0.2, "size": 56, "color": "white"}, depth=0, z=30)]),
]

KIT_GAPS = {
    "explainer/LeopardSeal": "NEW. One right-facing side-profile body (long flat reptilian skull, spotted grey back, pale throat, upturned mouth line). "
                             "Props: `pose` cruise|surface (head + neck over a waterline)|lunge (body arched, foreflippers back); `jaw` 0..75 deg (hard cap: the "
                             "SpermWhale-style lower-jaw rotation folds through the body past ~80), or a BlueWhale-style `gape` 0..1; `highlight` skull|mouth|whiskers (outline glow); "
                             "`carry` null|'penguin' (track; the penguin is drawn at the jaw tip so it follows the jaw, since core has no parenting); `spots`; `silhouette`; `pxPerM` (3.5 m adult female). "
                             "Upside-down singer = layer `rotate: 180` + `flipX`. Lounging = `cruise` with `idle: false` + small `rotate`. Tooth sieve and fang are `svg` diagrams, not rig states.",
    "explainer/Penguin": "NEW. One species (gentoo), `pose` waddle|swim|airborne|limp, `silhouette`.",
    "explainer/IceFloe": "NEW. Side-view slab with a visible underwater keel (`keel`), `width`, `colony` (N tiny penguin silhouettes on top), "
                         "`edgeStrip` {at} (red dashed doorway band along the water at the right edge).",
    "explainer/RIB": "NEW. Side-view inflatable with black tubes; `bites` (count or track of bite marks), `guards` {at} (panel slides over the tube).",
    "explainer/CaseFile": "NEW. Dossier board, `slots: 7` (slot 7 grey from the promise). Per-scene `state` {stamped: n, stampAt: t (scene-local, the stamp animates then), "
                          "slot7: grey|pulse|yellow, label}. Shown as a 2.6 s insert in the right third whenever a slot is stamped, never docked, so true-scale compositions keep the full frame.",
    "explainer/You (kneel, lying, camera)": "Existing `You` needs NEW `kneel` and `lying` poses and a `camera` prop (camera body held to the face). `shrug`, `panic` and `run` already exist.",
    "explainer/Diver (camera)": "Existing `Diver` needs a NEW `camera` prop (housing + dome port). Used only for the Nicklen scenes.",
    "_intro": (
        "Kit vocabulary: core layers (`rect`, `circle`, `text`, `svg`, `particles`, `component`), camera (`pushIn`, `pullOut`, `panUp`, `drift`, keyframes, `shake`), "
        "transitions (`cut`, `fade`, `dipBlack`, `whip`), `grade`, core `captions`; explainer kit `Ocean`, `Diver`, `You`, `Seal` (existing harbour seal, used as the "
        "round-headed contrast seal and for the prey ladder via `pxPerM`), `Krill`, `Orca`, `BlueWhale`, `Grizzly` (white `silhouette` = polar bear), `ScaleBar`, `Stat`, "
        "`Map` (`views`, `pins`), `Options` (`itemAt`, `strikes`, `select`), `SpeedBars`, `Headline`, `Tag`. `storyboard.json` next to this file is generated from this "
        "table by `gen.py` and validates against `studio/src/core/schema.ts`.\n\n"
        "**Asset scope (build before scheduling).** 5 NEW components (`LeopardSeal`, `Penguin`, `IceFloe`, `RIB`, `CaseFile`) plus 3 NEW figure options on existing "
        "components (`You` kneel/lying/camera, `Diver` camera). The GRAB -> RELEASE loop (R4, climax option 4, payoff) is one reusable inline `svg` in `shots.py`, as are "
        "the fang, tooth sieve, old book page, tin plate, bell, garage outline, season timeline and CIRCLE/STARE/GAPE/LEAVE strip (9 small `svg` props, already drawn). "
        "`LeopardSeal` carries about 30 of the 49 shots, so it is built first. Not needed any more: GenericSeal (existing `Seal`), globe (Map pan), polar-bear art (white "
        "`Grizzly`), tents and a separate Orde-Lees figure (`You` `run`), top-down ocean (side views only), `Timer` day counter (`Stat` with `prefix: 'DAY '`).\n\n"
        "**Map data (kit gap, shared file not edited here).** `mapdata.ts` needs PLACES `antarcticPeninsula: [-63, -65]`, `rothera: [-68.13, -67.57]`, "
        "`southGeorgia: [-36.5, -54.3]`, and two outlines: a ~20-point Antarctic Peninsula (Natural Earth 1:50m subset between lon -76..-55, lat -75..-63; Adelaide Island "
        "as its own polygon so the Rothera pin lands on land) and a ~12-point South Georgia polygon (lon -38.1..-35.7, lat -54.9..-53.9). Until then the storyboard pins "
        "by lon/lat, and Rothera sits just off the crude coast, which is where Adelaide Island is.\n\n"
        "**SFX mapping (no missing cues).** Every cue in the table is an existing file in `studio/public/sfx`: ice creak = `door_creak` pitched down at -10 dB; jaw = "
        "`door_creak`; stamp = `knock` at -6 dB; strike = `click`; comic sting = `stinger`; chime = `ding`; counter = `tick`; tension = `heartbeat_slow`; crack = `impact`; "
        "low hit = `boom`; paper/card slides = `whoosh`. Cut: colony chatter, rubber squeak, wind bed. One NEW cue, `seal_trill`, drives the hook and loop A, so it must "
        "be synthesised on the Spark (descending FM trill, 200 -> 80 Hz, with a sub-bass layer, 3-4 s) and approved before the hook is built; the storyboard uses "
        "`underwater_rumble` as its stand-in.\n\n"
        "**Build order and the 10-second gate.** LeopardSeal (profile + jaw cap + surface pose) -> IceFloe -> You kneel + camera -> Penguin -> CaseFile -> RIB. Then render "
        "shots 1-6 (0:00-0:31) as the gate test: they use 4 of the 5 new components and the trill cue. Look-dev frame for shot 9 (two `lying` YOU at `pxPerM: 400`) "
        "with `scripts/spark_stills.sh` before the full render.\n\n"
        "**Cut rate.** 49 shots in {S:total} s is about 5 per minute, inside Depth Theory's 3.1-5.4 hard cuts per minute (R1 videos.json); adjacent same-setup shots "
        "from the previous draft were merged (hook tags, krill + sieve, ladder + orca, myth + stamp, game + options, gifts + days).\n"),
}
