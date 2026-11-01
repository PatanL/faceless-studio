"""Explainer episode scene builders (9:16). One function per episode; scene i = narration paragraph i.

Layout (1080x1920): picture zone y 10-62 %, captions at y 0.72, nothing important below 77 %.
Only explainer-kit components and core layers are used.
"""
from __future__ import annotations

from .common import comp, fade, pop, svg, visual_events

W, H = 1080, 1920
RED = "#e5483d"

# Plain white captions (stroke + soft shadow). No active-word karaoke: red is the one danger accent, so the only red
# caption words are the explicit per-episode EMPHASIS threat words (at most one every ~8-10 s).
CAPTIONS = {"font": "display", "fontSize": 84, "color": "#ffffff", "highlight": "#ff5a4a", "highlightMode": "none",
            "strokeWidth": 12, "uppercase": True, "y": 0.72}
# 9:16 Shorts loop: no fade at either end (frame 0 is the cover, the last frame is the loop bookend). A 16:9 cut that
# wants a fade-out sets it in pipeline/episodes/reformat.py.
OVERLAYS = {"grain": 0.04, "vignette": 0.2, "fadeIn": 0, "fadeOut": 0}
EMPHASIS = {"explainer-blue-whale": ["throat", "turn"],
            # red = threat words only, about one every 8-10 s (orca review: not "alone"/"culture")
            "explainer-orca": ["kill", "seconds.", "liver.", "biggest", "ramming", "sunk."]}   # build.py marks these caption words (Word.emph)
# caption cards on phrase boundaries (pipeline/episodes/phrases.py): opt-in per episode (True = every episode), + glue
# (explainer-orca moved to the core least-cost pager + CAPTION_GLUE: the phrases.py br pages ended on dangling words)
PHRASE_PAGES: set[str] = set()
PHRASE_GLUE = {"explainer-orca": ["shark you're scared of", "except since", "orca mother", "fifty metres out", "brought down", "you're about the size",
                                  "ramming sailboats", "because they can't", "adult blue whale", "surviving great whites",
                                  "what chance", "nobody's ever proven that", "pod brought", "since twenty twenty",
                                  "have been ramming", "you taste", "haven't decided"]}
# word runs shown as one caption token (pipeline/episodes/build.py join_words): pairs the least-cost pager would split
# or strand (number | unit, verb | object, "scared | of"); (src, shown text) swaps the text
CAPTION_JOIN = {"explainer-orca": ["fifty-six kilometres", "scared of", ("twenty twenty,", "2020,"), ("twenty nineteen,", "2019,"),
                                   "it reaches", "eight metres long,", "mothers taught", "haven't decided"],
                # numerals keep the 9:16 pages to two lines ("CLOSE TO 200 TONNES.", not a 3-line "TWO HUNDRED")
                "explainer-blue-whale": ["two and a half", "even notice", ("two hundred tonnes.", "200 tonnes."),
                                         ("two hundred tonnes", "200 tonnes"), ("forty million", "40 million"),
                                         ("forty", "40"), ("thirty metres", "30 metres"), ("seven metres", "7 metres"),
                                         ("two beats", "2 beats")] + [
                    # a 9:16 page wraps to two lines between words: these runs stay together on the 2nd line (NBSP), so no
                    # line ends on a dangling word ("PARKED NOSE TO / TAIL." -> "PARKED / NOSE TO TAIL.")
                    (r, r.replace(" ", "\u00a0")) for r in (
                        "nose to tail.", "a sixteenth.", "of a golf cart,", "a jet engine,", "in the way", "in its mouth.",
                        "only opens", "back out.", "kilometres away.", "it charges", "of krill", "of that cloud?",
                        "40 of you.")]}
# extra joins for the 16:9 cut only (longer one-line pages there; pipeline/episodes/reformat.py)
CAPTION_JOIN_16X9 = {"explainer-blue-whale": ["reach you", "hundreds of kilometres"]}
# explicit caption pages (build.py mark_pages -> Word.br; the shared core pager stays untouched because horror uses it):
# whole phrases, never ending on an open word (up / close / never / size / comparatives), number + unit together.
# "|" separates pages. 9:16 pages wrap to two lines; 16:9 pages keep a whole sentence when it fits one ~34-char line.
_P = lambda s: [p.strip() for p in s.split("|")]
CAPTION_PAGES = {"explainer-blue-whale": _P(
    "You'd fit inside | a blue whale's mouth. | It still | couldn't swallow you. | This is the heaviest animal | ever measured. | "
    "Up to 30 metres long. | That's two and a half | city buses, | parked nose to tail. | Lying beside it, | you'd cover a sixteenth. | "
    "It can weigh | close to 200 tonnes. | Heavier than | the biggest dinosaurs | ever found. | "
    "The tongue alone weighs | about as much as an elephant. | That's about 40 of you. | "
    "The heart is | the size of a golf cart, | and outweighs two of you. | On a deep dive, | it can slow | to just 2 beats a minute. | "
    "Its call is | louder than a jet engine, | and it could reach you | hundreds of kilometres away. | "
    "To eat, it charges | into a cloud of krill | and takes one gulp of water | bigger than its own body. | "
    "So what happens to you, | floating right | in the middle of that cloud? | "
    "It eats | up to 40 million krill a day, | and every one is tiny. | Its throat only opens | about as wide as a beach ball. | "
    "Anything bigger | just gets pushed back out. | The real danger | isn't being eaten. | It's being in the way | "
    "when 200 tonnes | decides to turn, | and a tail | 7 metres wide | sweeps past. | Room for you in its mouth. | "
    "No room down its throat. | And it would | never even notice you.")}
CAPTION_PAGES_16X9 = {"explainer-blue-whale": _P(
    "You'd fit inside a blue whale's mouth. | It still couldn't swallow you. | This is the heaviest animal | ever measured. | "
    "Up to 30 metres long. | That's two and a half city buses, | parked nose to tail. | Lying beside it, | you'd cover a sixteenth. | "
    "It can weigh | close to 200 tonnes. | Heavier than the biggest dinosaurs | ever found. | "
    "The tongue alone | weighs about as much as an elephant. | That's about 40 of you. | "
    "The heart is the size of a golf cart, | and outweighs two of you. | On a deep dive, | it can slow to just 2 beats a minute. | "
    "Its call is louder than a jet engine, | and it could reach you | hundreds of kilometres away. | "
    "To eat, it charges | into a cloud of krill | and takes one gulp of water | bigger than its own body. | "
    "So what happens to you, | floating right | in the middle of that cloud? | "
    "It eats up to 40 million krill | a day, and every one is tiny. | Its throat only opens | about as wide as a beach ball. | "
    "Anything bigger | just gets pushed back out. | The real danger isn't being eaten. | It's being in the way | "
    "when 200 tonnes | decides to turn, | and a tail 7 metres wide | sweeps past. | Room for you in its mouth. | "
    "No room down its throat. | And it would never even notice you."),
    "explainer-orca": _P(
    "Wild killer whales | could kill you easily. | They never have. | Not because they can't. | A big male is eight metres long, | "
    "as heavy as four cars, | and its fin alone is as tall as you. | It hits fifty-six kilometres an hour. | "
    "An Olympic swimmer manages eight. | You, maybe three. | From fifty metres out, | it reaches you in three seconds. | "
    "And you'd never meet just one. | A pod hunts as a team, | and you'd be outnumbered. | In Antarctica, | "
    "a pod charges an ice floe together, | and the wave | washes the seal straight off. | You'd go too. | Off South Africa, | "
    "the shark you're scared of | started washing up missing one organ. | The liver. | Orcas flipped them and took it. | "
    "The surviving great whites | fled for months. | If they run, | what chance do you have? | In 2019, off Western Australia, | "
    "a pod brought down | the biggest animal on Earth. | An adult blue whale, | a thousand times your weight. | "
    "So why has something this fast | and this smart never come for you? | Maybe you taste bad? | Nobody's ever proven that. | "
    "Too small to bother with? | You're about | the size of the seals they eat. | The best answer is culture. | Orcas eat | "
    "what their mothers taught them. | And no orca mother | has ever taught her calf to eat you. | Comforting, right? | "
    "Except since 2020, | orcas off Spain and Portugal | have been ramming sailboats | and snapping off their rudders. | "
    "About seven boats have sunk. | Nobody knows why. | Maybe they just haven't decided | about you yet. | And that matters, because...")}
STRICT_HOLDS = {"explainer-blue-whale", "explainer-orca"}                  # build.py fails these on any visual hold > 3 s
# 9:16 caption pages: phrase-complete 2-4 word cards (the refs show "When a horse fly"); paginate() glues numbers and
# compounds and merges flashes shorter than 0.6 s
CAPTION_PAGING = {"maxWords": 4, "maxChars": 20}
CAPTION_GLUE = {"explainer-blue-whale": ["golf cart", "beach ball", "jet engine", "deep dive", "own body", "city buses",
                                         "two hundred tonnes", "forty million", "blue whale's", "half city",
                                         "biggest dinosaurs", "gets pushed", "isn't being", "metres wide", "forty million krill"],
                 # orca: PHRASE_GLUE pairs + QA 2nd pass (number+unit, "what chance", "this fast/smart", "her calf")
                 "explainer-orca": PHRASE_GLUE["explainer-orca"] + [
                     "fiftysix kilometres an hour", "as tall as", "what chance do you have", "this fast", "this smart",
                     "never come", "for you", "orcas eat", "taught her calf", "washing up", "the best answer",
                     "and you'd never meet"]}


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


COVER = -0.6  # "at" for hook text that must be fully in on frame 0 (Headline/Tag intros take ~0.6 s)
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
    """Fix round 2 builder lives in orca_pilot.py (reviewer fixes 1-10); orca_v1 below is the first pilot cut."""
    from .orca_pilot import build
    return build(S)


def orca_v1(S):
    sc = []
    s = S[0]
    PPM0 = 100  # orca and diver share pxPerM (<= 100 so the 1.2x push + punch never crops the head): the hook is already an honest "you vs. it" scale shot
    sc.append(scene(s, ocean(6, surface=0.2, rays=8, snow=60), [
        # frame 0 is the Shorts cover: orca, diver and headline are all on screen from t=0
        comp("explainer/Orca", "50%", "35%", 980, 360, {"speed": 1.1, "pxPerM": PPM0},
             keyframes=[{"t": 0, "x": "36%"}, {"t": s.dur * 0.75, "x": "52%", "ease": "out"}]),
        comp("explainer/Diver", "76%", "52.5%", 2.6 * PPM0 + 20, 90, {"pxPerM": PPM0, "arms": "side"}, flipX=True,
             idle=[{"type": "float", "amount": 6, "speed": 0.35}]),
        tag("YOU", COVER, x="76%", y="48.5%", size=28, w=200),
        headline("KILLER WHALE?", at=COVER, y="15%", size=84, color="white"),
        stat(0, "wild human kills", at=s.at("never", off=-0.1), y="61%", size=130, duration=0.3, color=RED),
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
        tag("≈ 6 TONNES", s.at("four", off=0.6), y="65%", size=36),
    ], camera=push(0.4), trans=FADE))
    s = S[2]
    sc.append(scene(s, ocean(20, rays=8), [
        comp("explainer/SpeedBars", "50%", "30%", 1000, 520, {
            "title": "Top speed", "max": 60, "at": 0.1, "stagger": 0.25, "duration": 0.7, "size": 54, "labelWidth": 310,
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
        comp("explainer/Orca", "36%", "49%", 440, 150, {"timeOffset": 1.1}, idle=[{"type": "float", "amount": 8, "speed": 0.35}]),
        headline("FAMILY POD", at=0.2, y="14%", size=70),
        tag("OWN CALLS", s.at("calls"), x="28%", y="57%", size=34, w=440),
        tag("OWN MENU", s.at("menu"), x="72%", y="57%", size=34, w=440),
        tag("OWN PLAN", s.at("plan"), x="50%", y="62.5%", size=34, w=440, accent=RED),
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
            "views": [{"t": 0, "lon": -12, "lat": 42, "zoom": 3.2}, {"t": s.at("Spain"), "lon": -12, "lat": 42, "zoom": 3.4},
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
    # cadence: word-anchored punch-ins, then Cam.fill closes any remaining visual hold > BEAT (README: no hold > 3-4 s)
    punch_words = {0: ["killer"], 2: ["Olympic", "You,"], 3: ["alone."], 5: ["organ"], 7: ["biggest"], 8: ["smart."],
                   10: ["mothers"], 12: ["decided"]}
    for i, scd in enumerate(sc):
        ts = [S[i].at(w.rstrip(",.")) for w in punch_words.get(i, [])]
        scd["camera"] = cadence_cam(scd, ts)
    return sc


def cadence_cam(scd: dict, punches=(), p=1.12) -> dict:
    """Turn a scene's preset/keyframe camera into a Cam path with punch-ins (keeps shakes); fills holds > BEAT."""
    dur, cam = scd["duration"], scd.get("camera") or {}
    if cam.get("preset") == "pushIn":
        c = Cam(dur, 1.0, 1 + 0.18 * cam.get("amount", 1), p=p)
    elif cam.get("preset") == "drift":
        c = Cam(dur, 1.04, 1.1, p=p)
    elif cam.get("keyframes"):
        ks = cam["keyframes"]
        c = Cam(dur, p=p, keys=[(k["t"], k.get("zoom", 1.0), k.get("x", "50%"), k.get("y", "50%")) for k in ks])
    else:
        c = Cam(dur, 1.0, 1.05, p=p)
    c.shake = list(cam.get("shake", []))
    c.punch(*punches)
    c.fill(visual_events({"duration": dur, "layers": scd["layers"]}) + [sh["at"] for sh in c.shake])
    return c.build()


# =========================================================================== blue whale

# --------------------------------------------------------------------------- 9:16 cadence helpers
# README: no visual hold over 4 s on Shorts; build.py fails STRICT_HOLDS episodes on > 3 s. These helpers give every
# scene an explicit camera (slow push + punch-ins on anchored words) and fill any remaining gap > BEAT with a punch.

BEAT = 2.5
WHITE = "#f3f6f7"
CYAN = "#6fd6e8"


class Cam:
    """Base camera path [(t, zoom, x, y)] plus punch-ins that toggle zoom by `p` (1.15-1.3x) on given times."""

    def __init__(self, dur, z0=1.0, z1=1.06, x="50%", y="50%", p=1.18, keys=None):
        self.dur, self.p = dur, p
        self.keys = keys or [(0.0, z0, x, y), (dur, z1, x, y)]
        self.punches: list[float] = []
        self.shake: list[dict] = []
        self.locked: list[tuple[float, float]] = []  # windows where no auto punch may land

    def punch(self, *ts):
        self.punches += [t for t in ts if t is not None]
        return self

    def base(self, t):
        ks = self.keys
        if t <= ks[0][0]:
            return ks[0][1:]
        for a, b in zip(ks, ks[1:]):
            if a[0] <= t <= b[0]:
                f = (t - a[0]) / max(1e-6, b[0] - a[0])
                return (a[1] + (b[1] - a[1]) * f, b[2], b[3])
        return ks[-1][1:]

    def fill(self, events, lo=0.0):
        ev = sorted(set([0.0, self.dur] + list(events) + self.punches + [k[0] for k in self.keys]))
        for a, b in zip(ev, ev[1:]):
            n = int((b - a) // BEAT)
            for k in range(1, n + 1):
                t = round(a + (b - a) * k / (n + 1), 3)
                if t > lo and not any(x0 <= t <= x1 for x0, x1 in self.locked):
                    self.punches.append(t)
        return self

    def build(self):
        pts = []
        for t in sorted(set(round(t, 3) for t in self.punches if 0.05 < t < self.dur - 0.25)):
            if not pts or t - pts[-1] >= 0.6:  # punches closer than 0.6 s read as jitter
                pts.append(t)
        R = 0.22

        def mult(t):  # punch-in state after all ramps that finished by t (none inside locked windows)
            if any(x0 <= t <= x1 for x0, x1 in self.locked):
                return 1.0
            n = sum(1 for p in pts if p + R <= t + 1e-6)
            return self.p if n % 2 else 1.0

        keys = {}
        for t, z, x, y in self.keys:
            keys[round(t, 3)] = {"t": round(t, 3), "zoom": round(z * mult(t), 4), "x": x, "y": y}
        for p in pts:
            if p not in keys:
                keys[p] = {"t": p, "zoom": round(self.base(p)[0] * mult(p), 4)}
            q = round(p + R, 3)
            keys[q] = {**keys.get(q, {}), "t": q, "zoom": round(self.base(q)[0] * mult(q), 4), "ease": "out"}
        cam = {"keyframes": [keys[t] for t in sorted(keys)]}
        if self.shake:
            cam["shake"] = self.shake
        return cam


def bw_scene(sc, bg, layers, cam: Cam, trans=None, fill=True, **kw):
    s = scene(sc, bg, layers, None, trans, **kw)
    if fill:
        cam.fill(visual_events({"duration": sc.dur, "layers": layers}))
    s["camera"] = cam.build()
    return s


LAYER_KW = ("start", "end", "keyframes", "depth", "z", "enter", "opacity")


def _lk(layer, props):
    """Move layer-level kwargs (start/end/...) out of component props onto the layer."""
    for k in LAYER_KW:
        if k in layer["props"]:
            layer[k] = layer["props"].pop(k)
    return layer


def t46(t, at, x="50%", y="20%", size=48, w=900, accent=CYAN, **props):
    """Phone-readable fact tag (min 46 px on 9:16), non-red accent."""
    return _lk(tag(t, at, x=x, y=y, size=max(46, size), w=w, accent=accent, **props), props)


def you_chip(at, x, y, kf=None, size=44):
    """YOU label: white chip, dark text (44 px; the orca pilot uses ~32 px with a leader line to the diver)."""
    l = {**tag("YOU", at, x=x, y=y, size=size, w=round(240 * size / 44), accent="#0b1a22", bg="#f3f6f7", color="#0b1a22",
               align="center"),
         "depth": 1, "z": 6}
    if kf:
        l["keyframes"] = kf
    return l


def wstat(value, label, at, y="58%", size=120, **props):
    """White stat value, red rule only, label >= 38 px."""
    return _lk(stat(value, label, at, y=y, size=size, color="white", labelSize=max(38, round(size * 0.32)), **props), props)


def ring(cx, cy, at, d0=0.2, d1=2.4, life=1.6, size=600, color="rgba(225,240,245,0.75)"):
    m = (f'<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"><circle cx="100" cy="100" r="92" fill="none" '
         f'stroke="{color}" stroke-width="5"/></svg>')
    return svg(m, cx, cy, size, size, start=at, end=at + life, z=3, depth=0.6,
               keyframes=[{"t": at, "scale": d0, "opacity": 0.95}, {"t": at + life, "scale": d1, "opacity": 0, "ease": "out"}])


RULER = ('<svg viewBox="0 0 160 1020" xmlns="http://www.w3.org/2000/svg">'
         '<line x1="120" y1="6" x2="120" y2="1014" stroke="#f3f6f7" stroke-width="6" stroke-linecap="round"/>'
         + "".join(f'<line x1="{96 if k % 2 else 84}" y1="{1014 - k * 168}" x2="140" y2="{1014 - k * 168}" stroke="#f3f6f7" '
                   f'stroke-width="6" stroke-linecap="round"/>' for k in range(7))
         + "".join(f'<text x="70" y="{1014 - k * 336 + 14}" text-anchor="end" font-family="Montserrat, Arial Black, sans-serif" '
                   f'font-weight="900" font-size="44" fill="#f3f6f7">{k * 10}</text>' for k in range(3))  # 30 = the "30 M" chip
         + '</svg>')
HALF_BUS = ('<svg viewBox="0 0 600 312" xmlns="http://www.w3.org/2000/svg"><rect x="0" y="20" width="620" height="250" rx="30" '
            'fill="#f2b632"/><rect x="0" y="196" width="600" height="30" fill="#d9961c"/><rect x="0" y="20" width="600" '
            'height="22" rx="11" fill="#f7c95a"/>' + "".join(f'<rect x="{30 + i * 108}" y="60" width="92" height="92" rx="10" '
                                                             f'fill="#1d2a33"/>' for i in range(5))
            + '<circle cx="230" cy="282" r="50" fill="#15191d"/><circle cx="230" cy="282" r="24" fill="#9aa3a9"/>'
            '<line x1="598" y1="24" x2="598" y2="270" stroke="#f3f6f7" stroke-width="8" stroke-dasharray="22 16"/></svg>')
DEEP = ('<svg viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="d" x1="0" y1="0" x2="0" '
        'y2="1"><stop offset="0" stop-color="#06121c"/><stop offset="1" stop-color="#0f2a3a"/></linearGradient>'
        '<radialGradient id="dg" cx="0.5" cy="0.3" r="0.6"><stop offset="0" stop-color="rgba(60,150,180,0.22)"/>'
        '<stop offset="1" stop-color="rgba(60,150,180,0)"/></radialGradient></defs>'
        '<rect width="1080" height="1920" fill="url(#d)"/><rect width="1080" height="1920" fill="url(#dg)"/></svg>')
# full-bleed mouth interior behind the WhaleThroat art: palate red at the top, tongue pink at the bottom, so the art's
# edges never show as seams when the camera pans
MOUTH_BG = ('<svg viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="m" x1="0" y1="0" '
            'x2="0" y2="1"><stop offset="0" stop-color="#4a2430"/><stop offset="0.3" stop-color="#4f2531"/><stop offset="0.6" '
            'stop-color="#5a2a36"/><stop offset="0.75" stop-color="#93525d"/><stop offset="1" stop-color="#93525d"/>'
            '</linearGradient></defs><rect width="1080" height="1920" fill="url(#m)"/></svg>')
# the same set at 2.2 x 1.6 frames (camera pans never reach its edge); stops placed for screen y 30 / 55 / 70 %
MOUTH_BG_WIDE = ('<svg viewBox="0 0 2376 3072" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="mw" x1="0" y1="0" '
                 'x2="0" y2="1"><stop offset="0" stop-color="#4a2430"/><stop offset="0.375" stop-color="#4f2531"/>'
                 '<stop offset="0.53" stop-color="#5a2a36"/><stop offset="0.625" stop-color="#93525d"/>'
                 '<stop offset="1" stop-color="#93525d"/></linearGradient></defs>'
                 '<rect width="2376" height="3072" fill="url(#mw)"/></svg>')
# a beach ball drawn as a dashed outline: the throat opening's size
BALL_RING = ('<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"><circle cx="100" cy="100" r="92" fill="none" '
             'stroke="#f3f6f7" stroke-width="7" stroke-dasharray="22 14"/></svg>')
# 7 m fluke seen from above: two swept lobes, centre notch, the tail stock pointing down to the body
FLUKE = ('<svg viewBox="0 0 480 180" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="fk" x1="0" y1="0" x2="0" '
         'y2="1"><stop offset="0" stop-color="#7397b0"/><stop offset="1" stop-color="#3a5a78"/></linearGradient></defs>'
         '<path d="M 214 180 L 220 92 L 260 92 L 266 180 Z" fill="#3f6080"/>'
         '<path d="M 240 70 C 180 40 90 16 6 30 C 30 70 110 110 196 116 L 240 98 L 284 116 C 370 110 450 70 474 30 '
         'C 390 16 300 40 240 70 Z" fill="url(#fk)" stroke="#2f4c66" stroke-width="4"/></svg>')
ARROW = ('<svg viewBox="0 0 260 180" xmlns="http://www.w3.org/2000/svg"><path d="M 236 160 C 190 120 120 70 62 44" '
         'stroke="#e5483d" stroke-width="16" fill="none" stroke-linecap="round"/><path d="M 30 26 L 96 30 L 62 84 Z" '
         'fill="#e5483d"/></svg>')
X_MARK = ('<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><path d="M 18 18 L 82 82 M 82 18 L 18 82" '
          'stroke="#0b0d10" stroke-width="26" stroke-linecap="round"/><path d="M 18 18 L 82 82 M 82 18 L 18 82" '
          'stroke="#f3f6f7" stroke-width="14" stroke-linecap="round"/></svg>')

# hook / bookend: true-scale head close-up (28 m whale = 3000 px wide => 107 px/m, a 2.6 m diver = 280 px) with the
# mouth open and YOU lying along the lower jaw INSIDE the gape. Frame 0 and the last frame share this exact state.
BW_HOOK = dict(x="162%", y="40%", w=3000, h=437)
GAPE0 = 0.85
DIVER_IN = {"x": "55.5%", "y": "43.6%", "rotate": -25}
CHIP_IN = {"x": "52%", "y": "35.5%"}
CAM0 = (0.92, "50%", "46%")
# frame-0 cover headline (two heavy lines, one red word that adds a claim) + red arrow at YOU; p10 ends on the same
COVER_HEAD = dict(text="YOU'RE TOO\nBIG TO EAT", red="EAT", y="15%", size=116)
COVER_ARROW = dict(x="68%", y="27%", w=260, h=180, rotate=-90)


def _cover_headline(at, **kw):
    h = COVER_HEAD
    return headline(h["text"], at=at, y=h["y"], size=h["size"], red=h["red"], underline=False, **kw)


def _cover_arrow(**kw):
    a = COVER_ARROW
    return svg(ARROW, a["x"], a["y"], a["w"], a["h"], rotate=a["rotate"], z=7, depth=0, **kw)


def _hook_whale(gape):
    return comp("explainer/BlueWhale", BW_HOOK["x"], BW_HOOK["y"], BW_HOOK["w"], BW_HOOK["h"], {"gape": gape, "amp": 0.5},
                flipX=True, z=1, idle=[{"type": "bob", "amount": 6, "speed": 0.2}])


def _bw_snap(S):
    """p09 -> p10 cut on p10's first word ("Room"), not LEAD before it: the last p09 caption page ("SWEEPS PAST.") ends
    exactly at the cut instead of showing over the mouth close-up (QA: 63.9-64.1 s). Both cuts call it (equal durations)."""
    s9, s10 = S[9], S[10]
    d = round(s10.words[0]["start"] - s10.start, 3)
    if d > 0:
        s9.dur, s10.start, s10.dur = round(s9.dur + d, 3), round(s10.start + d, 3), round(s10.dur - d, 3)
    return S


def blue_whale(S):
    _bw_snap(S)
    sc = []
    # ---------------------------------------------------------------- p00 hook (frame 0 = Shorts cover)
    s = S[0]
    nope = s.at("It", off=-0.1)          # 2nd sentence (~2.7 s): CAN'T SWALLOW YOU
    out = s.at("swallow", off=0.0)
    dkf = [{"t": 0, **DIVER_IN}, {"t": out, **DIVER_IN},
           {"t": out + 0.8, "x": "18%", "y": "50%", "rotate": -60, "ease": "out"}]
    ckf = [{"t": 0, **CHIP_IN}, {"t": out, **CHIP_IN}, {"t": out + 0.8, "x": "18%", "y": "43%", "ease": "out"}]
    cam = Cam(s.dur, keys=[(0.0, *CAM0), (s.dur, CAM0[0] * 1.06, "48%", "46%")]).punch(s.at("mouth"), nope)
    cam.locked.append((0.0, 1.0))
    sc.append(bw_scene(s, ocean(30, rays=8), [
        _hook_whale([{"t": 0, "v": GAPE0}, {"t": out, "v": GAPE0}, {"t": out + 0.5, "v": 0.55, "ease": "inOut"}]),
        comp("explainer/Diver", DIVER_IN["x"], DIVER_IN["y"], 280, 60, {"arms": "side"}, z=3, rotate=DIVER_IN["rotate"],
             keyframes=dkf),
        you_chip(0, CHIP_IN["x"], CHIP_IN["y"], ckf),
        _cover_headline(0, out=nope),
        _cover_arrow(end=out),
        headline("NO WAY\nDOWN", at=nope, y="15%", size=108, red="DOWN", underline=False),  # caption says "can't swallow you"
    ], cam))

    # ---------------------------------------------------------------- p01 length: nose-up whale vs 2.5 stacked buses
    s = S[1]
    PPM = 34
    L = 30 * PPM                     # 1020 px for 30 m
    yc = 750
    top, bot = yc - L // 2, yc + L // 2          # whale spans y 270-1290 (nose up, base clear of the caption band)
    yb = lambda px: f"{px / H * 100:.2f}%"
    two, half, nose = s.at("two"), s.at("half", off=-0.1), s.at("nose")
    heavy, lying = s.at("heaviest"), s.at("Lying", off=-0.1)
    bus_x = "72%"
    sc.append(bw_scene(s, ocean(60, rays=7), [
        comp("explainer/BlueWhale", "34%", yb(yc), L, 160, {"pxPerM": PPM * 30 / 28, "speed": 0.8}, rotate=-90,
             keyframes=[{"t": 0, "y": yb(yc - 160), "opacity": 0}, {"t": 0.5, "y": yb(yc), "opacity": 1, "ease": "out"}]),
        svg(RULER, "10%", yb(yc), 160, L, start=0.1, enter=fade(0.1, 0.3)),
        t46("30 M", s.at("long"), x="12%", y=yb(top - 50), size=48, w=240),
        {**comp("explainer/Bus", bus_x, yb(bot - 6 * PPM), 12 * PPM, 110, {"pxPerM": PPM}, rotate=-90, start=two,
                enter={"type": "slideUp", "at": two, "duration": 0.35})},
        {**comp("explainer/Bus", bus_x, yb(bot - 18 * PPM), 12 * PPM, 110, {"pxPerM": PPM}, rotate=-90, start=half,
                enter={"type": "slideUp", "at": half, "duration": 0.35})},
        svg(HALF_BUS, bus_x, yb(bot - 27 * PPM), 6 * PPM, 6 * PPM * 312 / 600, rotate=-90, start=nose,
            enter={"type": "slideUp", "at": nose, "duration": 0.35}),
        comp("explainer/Diver", "53%", yb(bot - 1.3 * PPM), 2.6 * PPM, 30, {"pxPerM": PPM, "arms": "side"}, rotate=-90,
             start=heavy, enter=pop(heavy)),
        you_chip(heavy, "53%", yb(bot - 2.6 * PPM - 50)),
        t46("YOU ≈ 1/16", lying, x="50%", y=yb(bot - 2.6 * PPM - 185), size=46, w=330, align="center"),
        headline("HOW BIG IS IT?", at=0, y="11%", size=66, out=two),
        {**headline("≈ 2.5 BUSES", at=s.at("parked"), y="11%", size=66), "x": "45%"},  # ends left of the bus stack
    ], Cam(s.dur, z0=1.0, z1=1.04).punch(heavy, s.at("thirty"), two, nose, lying), captionY=0.8))

    # ---------------------------------------------------------------- p02 weight: head close-up + 190 t, then balance vs dinosaur
    s = S[2]
    hv, dino = s.at("Heavier", off=-0.1), s.at("dinosaurs", off=-0.3)
    sc.append(bw_scene(s, ocean(80, rays=6), [
        comp("explainer/BlueWhale", "-28%", "33%", 2600, 380, {"speed": 0.7}, end=hv,
             idle=[{"type": "bob", "amount": 5, "speed": 0.25}],
             keyframes=[{"t": 0, "x": "-34%"}, {"t": hv, "x": "-26%"}]),
        wstat(190, "tonnes", s.at("two", off=-0.2), y="56%", size=140, prefix="~", duration=1.0, end=hv),
        comp("explainer/Balance", "50%", "45%", 1040, 640, {
            "left": {"species": "blueWhale", "w": 470, "at": hv, "pos": 0.27, "idle": True},
            "right": {"species": "sauropod", "w": 430, "at": dino, "drop": True, "pos": 0.27},
            "tilt": [{"t": hv, "v": -14}, {"t": dino + 0.35, "v": -14}, {"t": dino + 0.9, "v": -7, "ease": "out"}],
        }, start=hv, depth=0.3),
        wstat(190, "tonnes", hv, y="20%", size=80, prefix="~", duration=0.01, rule=False, box=False, start=hv),
        t46("BIGGER THAN ANY DINOSAUR", s.at("ever"), y="64%", size=46, w=1000, align="center"),
    ], Cam(s.dur, z0=1.0, z1=1.05).punch(s.at("two"), dino)))

    # ---------------------------------------------------------------- p03 tongue vs elephant on a balance (level)
    s = S[3]
    tg, el = s.at("tongue", off=-0.1), s.at("elephant", off=-0.45)
    land = el + 0.4
    forty = s.at("forty", off=-0.15)
    # "about forty of you": 40 true-to-each-other YOU figures fill in over the tongue pan (8 x 5 grid)
    # (QA 16:9: at y 10-28 % the crowd went off the top edge after the remap; now y 30-46 %, 66 px figures, left of the beam)
    crowd = [comp("explainer/You", f"{5 + (k % 8) * 4.2:.1f}%", f"{30 + (k // 8) * 4.0:.1f}%", 40, 66, {"pose": "stand"},
                  start=forty + k * 0.018, enter=pop(forty + k * 0.018, 0.2), depth=0.2, z=8) for k in range(40)]
    sc.append(bw_scene(s, ocean(50, rays=7), [
        comp("explainer/Balance", "50%", "42%", 1040, 760, {
            "left": {"species": "whaleTongue", "w": 300, "at": tg, "pos": 0.29},
            "right": {"species": "elephant", "w": 440, "at": el, "drop": True, "pos": 0.25, "idle": True},
            "tilt": [{"t": 0, "v": -13}, {"t": land, "v": -13}, {"t": land + 0.5, "v": 0, "ease": "out"}],
        }, depth=0.3),
        t46("TONGUE", tg, x="25%", y="45%", size=46, w=360, out=forty),  # clears the way for the crowd
        t46("≈ 2.7 TONNES EACH", land, y="60%", size=54, w=1000, align="center", out=forty),
        *crowd,
        t46("≈ 40 OF YOU", forty + 0.5, x="76%", y="16%", size=54, w=420, align="center"),
    ], Cam(s.dur, z0=1.0, z1=1.06).punch(tg, land, forty), captionY=0.8))

    # ---------------------------------------------------------------- p04 heart vs golf cart, then ECG slowing to 2 bpm
    s = S[4]
    size, dive, two = s.at("size", off=-0.1), s.at("deep", off=-0.1), s.at("two", nth=1, off=-0.1)
    heavy = s.at("outweighs", off=-0.1)
    HP = 210  # px per metre: heart 1.5 m = 315 px, cart 2.4 m = 504 px, diver 2.6 m = 546 px
    hb = [0.35, 1.35, 2.35, 3.35]
    beat_tr = [k for b in hb for k in ({"t": b, "v": 0}, {"t": b + 0.12, "v": 1}, {"t": b + 0.4, "v": 0})]
    # trace history (resting beats before the dive) is already drawn at the cut, then the beats space out
    ecg = [dive - 3.0 + k * 0.75 for k in range(4)] + [dive + 0.35, dive + 1.25, dive + 2.5, dive + 4.2]
    ecg = [round(b, 3) for b in ecg if b < s.dur]
    post = [b for b in ecg if b >= dive]
    sc.append(bw_scene(s, ocean(200, rays=3, snow=40), [
        comp("explainer/WhaleHeart", "25%", "37%", 1.5 * HP, 1.5 * HP, {"pxPerM": HP, "beat": beat_tr}, end=dive),
        comp("explainer/GolfCart", "65%", "38.5%", 2.4 * HP, 1.9 * HP, {"pxPerM": HP}, start=size, end=dive,
             enter=pop(size, 0.35)),
        comp("explainer/Diver", "50%", "56%", 2.6 * HP, 60, {"pxPerM": HP, "arms": "side"}, start=heavy, end=dive,
             enter=fade(heavy, 0.3)),
        {**you_chip(heavy, "50%", "50%"), "end": dive},
        t46("HEART", 0.2, x="25%", y="21%", size=46, w=320, end=dive),
        t46("GOLF CART", size + 0.3, x="65%", y="21%", size=46, w=420, end=dive),
        t46("180 KG ≈ 2+ OF YOU", heavy + 0.3, y="13%", size=50, w=1000, align="center", end=dive),
        # deep dive: navy-to-teal depth set (never flat black), marine snow, big beating heart over a full ECG
        svg(DEEP, "50%", "50%", W, H, start=dive, depth=0, z=0),
        {"type": "particles", "preset": "snow", "count": 90, "color": "rgba(200,225,235,0.55)", "size": [2, 5],
         "speed": 0.4, "z": 1, "depth": 0, "start": dive},
        t46("DEEP DIVE · ~180 M", dive, y="8.5%", size=48, w=1000, align="center", accent=CYAN),
        comp("explainer/WhaleHeart", "50%", "27%", 440, 440, {"beat": [k for b in post for k in (
            {"t": b, "v": 0}, {"t": b + 0.12, "v": 1}, {"t": b + 0.4, "v": 0})]}, start=dive, depth=0, z=5,
             enter=pop(dive, 0.3)),
        comp("explainer/ECG", "50%", "48%", 1000, 260, {"beats": ecg, "at": dive, "speed": 300, "color": CYAN,
                                                      "prefill": True}, start=dive, depth=0, z=5),
        wstat(2, "beats a minute", dive + 0.6, y="58%", size=120, **{"from": 10}, duration=max(0.6, two - dive - 0.6),
              pulse=2.0),
    ], Cam(s.dur, z0=1.0, z1=1.06).punch(s.at("heart"), size, heavy, dive, s.at("slow"), two), captionY=0.8))

    # ---------------------------------------------------------------- p05 call: louder than a jet engine
    s = S[5]
    jet, carry = s.at("jet", off=-0.1), s.at("reach", off=-0.1)
    far = s.at("you", off=-0.1)
    hx, hy = "86%", "45%"
    rings = [ring(hx, hy, 0.6 + k * 0.55, life=1.7, size=560) for k in range(int((s.dur - 0.8) / 0.55))]
    cam = Cam(s.dur, keys=[(0.0, 1.0, "50%", "50%"), (carry, 1.04, "55%", "48%"), (carry + 1.2, 0.8, "50%", "48%"),
                           (s.dur, 0.78, "50%", "48%")]).punch(s.at("louder"), jet)
    cam.locked.append((carry, s.dur))
    sc.append(bw_scene(s, ocean(40, rays=6), [
        comp("explainer/BlueWhale", "40%", "45%", 1150, 168, {"speed": 0.8}, z=2, idle=[{"type": "bob", "amount": 5, "speed": 0.3}]),
        *rings,
        wstat(188, "decibels", s.at("louder"), y="56%", size=120, suffix=" dB", duration=0.8, out=far - 0.25),
        comp("explainer/Jet", "68%", "22%", 520, 140, {}, start=jet, depth=0.2,
             enter={"type": "slideLeft", "at": jet, "duration": 0.4}),
        t46("JET ENGINE", jet + 0.35, x="50%", y="13%", size=46, w=1000, align="center", out=carry),
        t46("HEARD 100s OF KM AWAY", s.at("hundreds"), x="50%", y="13%", size=46, w=1000, align="center"),
        # "...could reach you": a tiny YOU far out on the left edge as the camera pulls out; the rings reach it
        comp("explainer/Diver", "12%", "62%", 180, 42, {"arms": "side"}, z=3, start=far, enter=pop(far, 0.3),
             idle=[{"type": "float", "amount": 6, "speed": 0.4}]),
        you_chip(far, "12%", "57.5%"),
        ring("12%", "62%", far + 0.25, d0=0.1, d1=0.7, life=0.9, size=300, color="rgba(111,214,232,0.9)"),
    ], cam, captionY=0.8))

    # ---------------------------------------------------------------- p06 gulp: head enters the krill swarm, pouch balloons
    s = S[6]
    cloud, gulp = s.at("cloud", off=-0.2), s.at("gulp", off=-0.3)
    sc.append(bw_scene(s, ocean(25, rays=9), [
        {"type": "particles", "preset": "dust", "count": 600, "color": "rgba(255,140,105,0.9)", "size": [5, 10],
         "speed": 0.5, "x": "58%", "y": "40%", "width": 1150, "height": 1000, "z": 2},
        *[comp("explainer/Krill", x, y, 70, 30, {"speed": 1 + i * 0.2}, depth=1.4, z=6,
               idle=[{"type": "float", "amount": 14, "speed": 0.4 + i * 0.1}])
          for i, (x, y) in enumerate([("70%", "28%"), ("84%", "47%"), ("62%", "56%"), ("90%", "33%")])],
        comp("explainer/BlueWhale", "-148%", "34%", 3000, 437,
             {"speed": 1.3, "gape": [{"t": s.at("takes", off=-0.2), "v": 0}, {"t": gulp + 0.6, "v": 1, "ease": "out"}]},
             z=3, keyframes=[{"t": 0, "x": "-111%"}, {"t": cloud, "x": "-96%"}, {"t": gulp + 0.3, "x": "-65.7%", "ease": "out"}]),
        t46("KRILL", s.at("krill"), x="78%", y="18%", size=48, w=320, out=s.at("bigger", off=-0.45)),
        t46("ONE GULP > ITS OWN BODY", s.at("bigger"), y="12%", size=48, w=1000, align="center"),
    ], Cam(s.dur, z0=1.0, z1=1.08, x="52%", y="44%").punch(s.at("charges", off=-0.05), cloud, gulp + 0.3), captionY=0.8))

    # ---------------------------------------------------------------- p07 turnstile: you, alone in the cloud
    s = S[7]
    sc.append(bw_scene(s, ocean(25, rays=8), [
        {"type": "particles", "preset": "dust", "count": 600, "color": "rgba(255,140,105,0.85)", "size": [4, 9], "speed": 0.5, "z": 1},
        # the whale looms below YOU: head and open mouth in frame, dimmed and softened by depth (not a black slab)
        comp("explainer/BlueWhale", "170%", "54%", 1800, 263,
             {"speed": 0.6, "gape": [{"t": 0, "v": 0}, {"t": s.dur, "v": 0.6, "ease": "inOut"}]}, flipX=True, z=0,
             opacity=0.5, blur=3, start=0.0,
             keyframes=[{"t": 0, "x": "170%"}, {"t": s.dur, "x": "118%", "ease": "out"}]),
        comp("explainer/Diver", "50%", "44%", 600, 130, {"arms": "side"}, z=3, idle=[{"type": "float", "amount": 10, "speed": 0.4}]),
        you_chip(0.0, "50%", "38%"),
        headline("AND YOU?", at=s.at("you", off=-0.1), y="16%", size=110),
    ], Cam(s.dur, z0=1.0, z1=1.12, x="50%", y="44%").punch(s.at("floating"), s.at("middle"))))

    # ---------------------------------------------------------------- p08 krill count, then the throat close-up
    s = S[8]
    cut = s.at("throat", off=-0.35)           # hard cut to the inside of the mouth
    tiny = s.at("tiny", off=-0.3)
    TP = 1300 / 3                             # throat close-up px per metre (3 m across 1300 px)
    ring_x = 540 - 650 + 230 * 1.3            # WhaleThroat ring centre (drawing 230,470) in screen px
    ring_y = 768 - 650 + 470 * 1.3
    head_off = 345 * (2.6 * TP / 690)         # diver box centre -> head tip (px)
    stop_x = ring_x + 30 + head_off           # head tip on the ring, the body (bigger than the opening) stuck outside
    RING_D = 140                              # throat opening on screen (~0.35 m at TP), = the beach ball's diameter
    px = lambda v, n: f"{v / n * 100:.2f}%"
    opens, beach, anything, pushed = s.at("opens"), s.at("beach", off=-0.2), s.at("Anything", off=-0.1), s.at("pushed", off=-0.1)
    dkf = [{"t": cut, "x": px(stop_x + 420, W)}, {"t": opens, "x": px(stop_x + 300, W)},
           {"t": beach + 0.4, "x": px(stop_x, W), "ease": "out"}, {"t": pushed, "x": px(stop_x, W), "rotate": 0},
           {"t": pushed + 0.7, "x": px(stop_x + 260, W), "rotate": 8, "ease": "out"}]
    cam = Cam(s.dur, keys=[(0.0, 1.0, "50%", "44%"), (cut, 1.0, "50%", "44%"), (cut + 0.01, 1.0, "50%", "40%"),
                           (beach, 1.08, "40%", "40%"), (anything, 1.28, "30%", px(ring_y, H)),
                           (pushed, 1.28, "30%", px(ring_y, H)), (pushed + 0.18, 1.4, "31%", px(ring_y, H)),  # punch on "pushed"
                           (pushed + 0.6, 1.15, "36%", "40%"), (s.dur, 1.12, "38%", "40%")]).punch(s.at("forty"), tiny)
    cam.locked.append((beach - 0.3, s.dur))
    sc.append(bw_scene(s, ocean(60, rays=4, snow=30), [
        comp("explainer/Krill", "50%", "46%", 640, 280, {"speed": 0.8}, end=cut,
             keyframes=[{"t": 0, "scale": 1}, {"t": tiny, "scale": 1}, {"t": tiny + 0.35, "scale": 0.22, "ease": "inOut"}]),
        t46("≈ 6 CM LONG", 0.9, y="58.5%", size=48, w=1000, align="center", end=cut),
        wstat(40000000, "krill a day", s.at("forty", off=-0.1), y="22%", size=100, duration=1.4, end=cut),
        {"type": "particles", "preset": "dust", "count": 300, "color": "rgba(255,140,105,0.85)", "size": [4, 8], "speed": 0.4,
         "z": 1, "start": tiny + 0.2, "end": cut},
        # oversized so the camera's pan to the ring (x 30 %, zoom 1.4) never shows the ocean past its edge
        svg(MOUTH_BG_WIDE, "50%", "50%", W * 2.2, H * 1.6, start=cut, depth=0, z=1),
        comp("explainer/WhaleThroat", "50%", "40%", 1300, 1300, {"glow": [{"t": beach, "v": 0}, {"t": beach + 0.4, "v": 1}]},
             start=cut, depth=0.5, z=2),
        comp("explainer/Diver", px(stop_x + 420, W), px(ring_y, H), 2.6 * TP, 200, {"pxPerM": TP, "arms": "forward"},
             flipX=True, start=cut, z=4, depth=0.5, keyframes=dkf),
        # the beach ball drops onto the throat ring at the ring's own diameter (a size match), then stays as a dashed
        # outline the diver's head bumps into
        svg(BALL, px(ring_x, W), px(ring_y - 360, H), RING_D, RING_D, start=beach, end=beach + 1.1, z=5, depth=0.5,
            keyframes=[{"t": beach, "y": px(ring_y - 360, H), "scale": 1.4, "opacity": 1},
                       {"t": beach + 0.45, "y": px(ring_y, H), "scale": 1.0, "opacity": 0.95, "ease": "out"},
                       {"t": beach + 0.8, "y": px(ring_y, H), "scale": 1.0, "opacity": 0.9},
                       {"t": beach + 1.1, "y": px(ring_y, H), "scale": 1.0, "opacity": 0}]),
        svg(BALL_RING, px(ring_x, W), px(ring_y, H), RING_D, RING_D, start=beach + 0.8, z=5, depth=0.5,
            enter=fade(beach + 0.8, 0.3)),
        t46("THROAT ≈ BEACH BALL", beach, y="13%", size=46, w=1000, align="center"),
        t46("THROAT", s.at("throat") + 0.3, x=px(ring_x + 330, W), y=px(ring_y - 190, H), size=46, w=380, start=cut,
            out=beach),
        svg(X_MARK, px(ring_x + 40, W), px(ring_y - 80, H), 130, 130, start=anything, enter=pop(anything, 0.25), z=6,
            depth=0.5),
    ], cam))

    # ---------------------------------------------------------------- p09 the turn: head, eye and flipper pass YOU, tail sweeps
    s = S[9]
    way, turn, tail, sweeps = s.at("way", off=-0.3), s.at("turn", off=-0.4), s.at("tail"), s.at("sweeps", off=-0.1)
    cam = Cam(s.dur, z0=1.0, z1=1.05, y="44%").punch(s.at("danger"), way, s.at("tonnes"), tail)
    cam.shake = [{"at": turn + 0.3, "duration": 0.8, "amplitude": 22}, {"at": sweeps, "duration": 0.7, "amplitude": 16}]
    sc.append(bw_scene(s, ocean(30, rays=8), [
        # head, eye and flipper fill the right edge from the cut; the body passes and fades into the murk before the
        # fluke close-up below comes in, so its own tail never shares the frame with the FLUKE (QA: "two tails")
        comp("explainer/BlueWhale", "140%", "47%", 1900, 277, {"speed": 1.1}, z=1, flipX=True,
             keyframes=[{"t": 0, "x": "140%"}, {"t": way, "x": "128%", "rotate": 0},
                        {"t": turn, "x": "118%", "rotate": 0, "ease": "inOut"},
                        {"t": turn + 0.8, "x": "100%", "rotate": -14, "ease": "inOut"},
                        {"t": sweeps - 0.9, "x": "26%", "rotate": -6, "opacity": 1, "ease": "inOut"},
                        # QA round 1: the body held >= 60 % until the fluke is in (no empty half-second at 62.2 s, the
                        # fluke never reads as a separate fish); its own tail stays past the right edge
                        {"t": sweeps - 0.3, "x": "18%", "rotate": -5, "opacity": 0.75},
                        {"t": sweeps + 0.3, "x": "15%", "rotate": -4, "opacity": 0.6},
                        {"t": sweeps + 0.8, "x": "12%", "rotate": -4, "opacity": 0},
                        {"t": s.dur, "x": "10%", "rotate": -4, "opacity": 0}]),
        comp("explainer/Diver", "50%", "36%", 260, 58, {"arms": "side"}, z=6,
             keyframes=[{"t": 0, "x": "50%", "y": "36%", "rotate": 0}, {"t": turn + 0.3, "x": "50%", "y": "36%", "rotate": 0},
                        {"t": turn + 1.3, "x": "30%", "y": "31%", "rotate": -230, "ease": "out"},
                        {"t": sweeps, "x": "30%", "y": "32%", "rotate": -250},
                        {"t": sweeps + 1.0, "x": "16%", "y": "35%", "rotate": -420, "ease": "out"}]),
        you_chip(0.0, "50%", "31.5%", [{"t": 0, "x": "50%", "y": "31.5%"}, {"t": turn + 0.3, "x": "50%", "y": "31.5%"},
                                        {"t": turn + 1.3, "x": "30%", "y": "26.5%", "ease": "out"},
                                        {"t": sweeps, "x": "30%", "y": "27.5%"},
                                        {"t": sweeps + 1.0, "x": "16%", "y": "30.5%", "ease": "out"}]),
        headline("NOT THE MOUTH", at=0, y="13%", size=70, out=way),
        svg(ARROW, "64%", "41%", 260, 180, start=way, end=turn + 0.3, enter=pop(way, 0.25), z=5),
        t46("WRONG PLACE, WRONG TIME", turn, y="13%", size=48, w=1000, align="center", out=sweeps - 0.55),
        t46("7 M TAIL", sweeps, y="13%", size=50, w=500, align="center"),
        # the 7 m fluke at true scale against the 2.6 m diver (260 px => 100 px/m => 700 px), seen from above, sweeping
        # up past YOU on "sweeps"
        # (QA: it crossed in < 1 s and left through the top edge) sweeps across the middle of the frame, fades on the left
        # QA round 1: in from the right edge (where the body's own tail stock leaves the frame) from 62.2 s, the path at
        # y 0.46-0.56 (clear of the 0.72 caption), passing BELOW the diver (diver/YOU drawn above it, z 6)
        svg(FLUKE, "96%", "55%", 700, 262, start=sweeps - 0.95, end=sweeps + 1.5, z=4,
            keyframes=[{"t": sweeps - 0.95, "x": "100%", "y": "56%", "rotate": 12, "opacity": 0},
                       {"t": sweeps - 0.7, "x": "90%", "y": "55%", "rotate": 10, "opacity": 1},
                       {"t": sweeps + 0.3, "x": "58%", "y": "51%", "rotate": -4, "opacity": 1, "ease": "inOut"},
                       {"t": sweeps + 0.9, "x": "36%", "y": "47%", "rotate": -10, "opacity": 1},
                       {"t": sweeps + 1.4, "x": "20%", "y": "46%", "rotate": -14, "opacity": 0}]),
    ], cam))

    # ---------------------------------------------------------------- p10 bookend: back to the frame-0 state (seamless loop)
    s = S[10]
    no, barely = s.at("No", off=-0.1), s.at("never", off=-0.2)
    settle = min(s.dur - 0.5, barely + 1.3)
    dkf = [{"t": 0, "x": "30%", "y": "47%", "rotate": -40}, {"t": no, "x": "44%", "y": "45%", "rotate": -30, "ease": "inOut"},
           {"t": barely, **DIVER_IN, "ease": "inOut"}, {"t": s.dur, **DIVER_IN}]
    ckf = [{"t": 0, "x": "30%", "y": "39%"}, {"t": no, "x": "42%", "y": "37%", "ease": "inOut"},
           {"t": barely, **CHIP_IN, "ease": "inOut"}, {"t": s.dur, **CHIP_IN}]
    cam = Cam(s.dur, keys=[(0.0, 1.22, "42%", "45%"), (barely, 1.3, "46%", "45%"), (settle, *CAM0), (s.dur, *CAM0)]).punch(no)
    cam.locked.append((barely - 0.3, s.dur))
    sc.append(bw_scene(s, ocean(30, rays=8), [
        _hook_whale([{"t": 0, "v": 0.6}, {"t": no, "v": 0.6}, {"t": barely, "v": GAPE0, "ease": "inOut"}]),
        comp("explainer/Diver", "30%", "47%", 280, 60, {"arms": "side"}, z=3, keyframes=dkf),
        you_chip(0, "30%", "39%", ckf),
        headline("NONE DOWN\nITS THROAT", at=0.1, y="15%", size=108, red="THROAT", underline=False, out=barely),
        _cover_headline(barely + 0.3),   # the last frame = frame 0 (cover headline + arrow): exact loop
        _cover_arrow(start=barely + 0.45, enter=pop(barely + 0.45, 0.3)),
    ], cam))
    return sc


def blue_whale_16x9(S):
    """Landscape-native scenes for the 16:9 cut ({scene index: scene}, 1920x1080 px); pipeline/episodes/reformat.py
    uses them instead of remapping the 9:16 scene (p01, p02, p04). p01: the nose-up ruler left both sides of 16:9 empty and put the
    30 M chip into the header, so the whale lies along a horizontal 0-30 m ruler with 2.5 buses nose to tail below."""
    W16, H16 = 1920, 1080
    _bw_snap(S)
    s = S[1]
    PPM = 52
    L = 30 * PPM                                  # 1560 px for 30 m
    X0 = (W16 - L) // 2                           # ruler 0 at x 180, 30 m at x 1740
    Y_WHALE, Y_RULER, Y_YOU, Y_BUS = 270, 432, 572, 736
    fx = lambda v: f"{v / W16 * 100:.2f}%"
    fy = lambda v: f"{v / H16 * 100:.2f}%"
    two, half, nose = s.at("two"), s.at("half", off=-0.1), s.at("nose")
    heavy, lying = s.at("heaviest"), s.at("Lying", off=-0.1)
    pad = 60
    ruler = (f'<svg viewBox="0 0 {L + 2 * pad} 112" xmlns="http://www.w3.org/2000/svg">'
             f'<line x1="{pad}" y1="10" x2="{pad + L}" y2="10" stroke="#f3f6f7" stroke-width="6" stroke-linecap="round"/>'
             + "".join(f'<line x1="{pad + m * PPM}" y1="10" x2="{pad + m * PPM}" y2="{46 if m % 10 == 0 else 34}" '
                       f'stroke="#f3f6f7" stroke-width="6" stroke-linecap="round"/>' for m in range(0, 31, 5))
             + "".join(f'<text x="{pad + m * PPM}" y="96" text-anchor="middle" font-family="Montserrat, Arial Black, '
                       f'sans-serif" font-weight="900" font-size="40" fill="#f3f6f7">{m}</text>' for m in (0, 10, 20))
             + '</svg>')                          # 30 = the "30 M" chip at the ruler's end
    bus_h, hb_w = round(110 * PPM / 34), 6 * PPM
    bus = lambda m, at: comp("explainer/Bus", fx(X0 + m * PPM), fy(Y_BUS), 12 * PPM, bus_h, {"pxPerM": PPM}, start=at,
                             enter={"type": "slideUp", "at": at, "duration": 0.35})
    diver_w = 2.6 * PPM
    layers = [
        comp("explainer/BlueWhale", fx(X0 + L / 2), fy(Y_WHALE), L, round(160 * PPM / 34), {"pxPerM": PPM * 30 / 28, "speed": 0.8},
             keyframes=[{"t": 0, "x": "-60%"}, {"t": 1.1, "x": fx(X0 + L / 2), "ease": "out"}]),
        svg(ruler, fx(X0 + L / 2), fy(Y_RULER - 10 + 56), L + 2 * pad, 112, start=heavy + 0.4, enter=fade(heavy + 0.4, 0.3)),
        t46("30 M", s.at("long"), x=fx(X0 + L), y=fy(Y_RULER + 72), size=46, w=220, align="center"),
        bus(6, two),
        bus(18, half),
        svg(HALF_BUS, fx(X0 + 27 * PPM), fy(Y_BUS), hb_w, hb_w * 312 / 600, start=nose,
            enter={"type": "slideUp", "at": nose, "duration": 0.35}),
        comp("explainer/Diver", fx(X0 + diver_w / 2), fy(Y_YOU), diver_w, round(30 * PPM / 34), {"pxPerM": PPM, "arms": "side"},
             start=heavy, enter=pop(heavy)),
        you_chip(heavy, fx(X0 + diver_w + 150), fy(Y_YOU)),
        t46("YOU ≈ 1/16", lying, x=fx(X0 + diver_w + 440), y=fy(Y_YOU), size=46, w=330, align="center"),
        headline("HOW BIG IS IT?", at=0, y=fy(88), size=64, out=two),
        headline("≈ 2.5 CITY BUSES", at=s.at("parked"), y=fy(88), size=64),
    ]
    # gentler punch-ins than 9:16 (1.07 vs 1.18): the ruler spans 81 % of the frame width
    cam = Cam(s.dur, z0=1.0, z1=1.02, p=1.07).punch(heavy, s.at("thirty"), two, nose, lying)
    out = {1: bw_scene(s, ocean(60, rays=7), layers, cam)}

    # p04 (QA 16:9: heart + golf cart a small cluster at the top, ~55 % empty; DEEP DIVE a portrait column):
    # heart and cart side by side at ~25-33 % of the width each filling y 20-70 %, the diver under them; then a
    # full-bleed deep set with the big heart on the left and the ECG + 2 BPM stat on the right
    s = S[4]
    size, dive, two = s.at("size", off=-0.1), s.at("deep", off=-0.1), s.at("two", nth=1, off=-0.1)
    heavy = s.at("outweighs", off=-0.1)
    HP = 260  # px per metre: heart 1.5 m = 390 px, cart 2.4 m = 624 px, diver 2.6 m = 676 px
    hb = [0.35, 1.35, 2.35, 3.35]
    beat_tr = [k for b in hb for k in ({"t": b, "v": 0}, {"t": b + 0.12, "v": 1}, {"t": b + 0.4, "v": 0})]
    ecg = [dive - 3.0 + k * 0.75 for k in range(4)] + [dive + 0.35, dive + 1.25, dive + 2.5, dive + 4.2]
    ecg = [round(b, 3) for b in ecg if b < s.dur]
    post = [b for b in ecg if b >= dive]
    dw = W16 * 1.05
    layers = [
        comp("explainer/WhaleHeart", "27%", "45%", 1.5 * HP, 1.5 * HP, {"pxPerM": HP, "beat": beat_tr}, end=dive),
        comp("explainer/GolfCart", "68%", "46%", 2.4 * HP, 1.9 * HP, {"pxPerM": HP}, start=size, end=dive,
             enter={"type": "slideLeft", "at": size, "duration": 0.45}),
        comp("explainer/Diver", "50%", "75%", 2.6 * HP, 70, {"pxPerM": HP, "arms": "side"}, start=heavy, end=dive,
             enter=fade(heavy, 0.3)),
        {**you_chip(heavy, "26%", "75%"), "end": dive},
        t46("HEART", 0.2, x="27%", y="19%", size=46, w=320, end=dive),
        t46("GOLF CART", size + 0.3, x="68%", y="19%", size=46, w=420, end=dive),
        t46("180 KG ≈ 2+ OF YOU", heavy + 0.3, y="8.5%", size=50, w=1000, align="center", end=dive),
        svg(DEEP, "50%", "50%", dw, dw * 1920 / 1080, start=dive, depth=0, z=0),
        {"type": "particles", "preset": "snow", "count": 120, "color": "rgba(200,225,235,0.55)", "size": [2, 5],
         "speed": 0.4, "z": 1, "depth": 0, "start": dive},
        t46("DEEP DIVE · ~180 M", dive, y="8.5%", size=48, w=1000, align="center", accent=CYAN),
        comp("explainer/WhaleHeart", "26%", "46%", 460, 460, {"beat": [k for b in post for k in (
            {"t": b, "v": 0}, {"t": b + 0.12, "v": 1}, {"t": b + 0.4, "v": 0})]}, start=dive, depth=0, z=5,
             enter=pop(dive, 0.3)),
        comp("explainer/ECG", "64%", "38%", 1060, 260, {"beats": ecg, "at": dive, "speed": 300, "color": CYAN,
                                                      "prefill": True}, start=dive, depth=0, z=5),
        wstat(2, "beats a minute", dive + 0.6, x="64%", y="64%", size=110, **{"from": 10},
              duration=max(0.6, two - dive - 0.6), pulse=2.0),
    ]
    cam = Cam(s.dur, z0=1.0, z1=1.03, p=1.07).punch(s.at("heart"), size, heavy, dive, s.at("slow"), two)
    out[4] = bw_scene(s, ocean(200, rays=3, snow=40), layers, cam)

    # p02 (QA 16:9: the balance whale ~20 % of the width, a low-contrast grey sauropod): head close-up filling the
    # left two thirds with the 190 t stat beside it, then a frame-wide balance (whale ~43 % of the width), sauropod lifted
    s = S[2]
    hv, dino = s.at("Heavier", off=-0.1), s.at("dinosaurs", off=-0.3)
    layers = [
        comp("explainer/BlueWhale", "-25%", "42%", 3400, 497, {"speed": 0.7}, end=hv,
             idle=[{"type": "bob", "amount": 5, "speed": 0.25}],
             keyframes=[{"t": 0, "x": "-28%"}, {"t": hv, "x": "-23%"}]),
        wstat(190, "tonnes", s.at("two", off=-0.2), x="82%", y="44%", size=130, prefix="~", duration=1.0, end=hv),
        comp("explainer/Balance", "50%", "47%", 1760, 680, {
            "left": {"species": "blueWhale", "w": 820, "at": hv, "pos": 0.27, "idle": True},
            "right": {"species": "sauropod", "w": 640, "at": dino, "drop": True, "pos": 0.27, "silhouette": "#a3b1b9"},
            "tilt": [{"t": hv, "v": -10}, {"t": dino + 0.35, "v": -10}, {"t": dino + 0.9, "v": -5, "ease": "out"}],
        }, start=hv, depth=0.3),
        wstat(190, "tonnes", hv, x="22%", y="11%", size=72, prefix="~", duration=0.01, rule=False, box=False, start=hv),
        t46("BIGGER THAN ANY DINOSAUR", s.at("ever"), x="66%", y="9%", size=46, w=900, align="center"),
    ]
    out[2] = bw_scene(s, ocean(80, rays=6), layers, Cam(s.dur, z0=1.0, z1=1.03, p=1.07).punch(s.at("two"), dino))
    return out



def _pct(v):
    return float(str(v).rstrip("%"))


def blue_whale_16x9_patch(sb):
    """Post-remap fixes for the 16:9 cut (1920x1080 coords; pipeline/episodes/reformat.py PATCH_16X9), QA round 1:
    p08 throat set full-bleed (WhaleThroat bleed: walls, baleen and tongue floor run to the frame edges, the diver
    inside the set); p05 / p09 YOU chip >= 20 px above a bigger diver; p09 the 7 m fluke ~950 px wide, in from the
    right edge at mid-frame (y ~50-60 %), passing below the diver and clear of the caption band (y > 80 %)."""
    sc = sb["scenes"]
    named = lambda i, name, text=None: [l for l in sc[i]["layers"] if l.get("name") == name
                                        and (text is None or l.get("props", {}).get("text") == text)]
    for l in named(8, "explainer/WhaleThroat"):
        l["props"]["bleed"] = 700
    # p05 far YOU: diver 200 px, chip clear above it
    for d in named(5, "explainer/Diver"):
        d["width"], d["height"] = 200, 47
        for c in named(5, "explainer/Tag", "YOU"):
            c["x"], c["y"] = d["x"], f"{_pct(d['y']) - 105 / 10.8:.2f}%"
    # p09 diver ~270 px, chip keyframes follow the diver 110 px above it
    for d in named(9, "explainer/Diver"):
        d["width"], d["height"] = 270, 60
        for c in named(9, "explainer/Tag", "YOU"):
            c["y"] = f"{_pct(d['y']) - 110 / 10.8:.2f}%"
            c["keyframes"] = [{"t": k["t"], "x": k["x"], "y": f"{_pct(k['y']) - 110 / 10.8:.2f}%",
                               **({"ease": k["ease"]} if "ease" in k else {})} for k in d["keyframes"]]
    for f in [l for l in sc[9]["layers"] if l["type"] == "svg" and l.get("width", 0) > 500]:
        t0 = f["keyframes"][0]["t"]               # = sweeps - 0.95
        sw = t0 + 0.95
        f["width"], f["height"] = 950, round(950 * 180 / 480, 1)
        f["x"], f["y"] = "110%", "56%"
        f["keyframes"] = [{"t": t0, "x": "112%", "y": "57%", "rotate": 12, "opacity": 0},
                          {"t": sw - 0.7, "x": "96%", "y": "56%", "rotate": 10, "opacity": 1},
                          {"t": sw + 0.3, "x": "62%", "y": "55%", "rotate": -4, "opacity": 1, "ease": "inOut"},
                          {"t": sw + 0.9, "x": "40%", "y": "53%", "rotate": -10, "opacity": 1},
                          {"t": sw + 1.4, "x": "26%", "y": "52%", "rotate": -14, "opacity": 0}]
    return sb


PATCH_16X9 = {"explainer-blue-whale": blue_whale_16x9_patch}

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
# landscape-native scenes for the 16:9 cut (pipeline/episodes/reformat.py), {slug: fn(S) -> {scene index: scene}}
EPISODES_16X9 = {"explainer-blue-whale": blue_whale_16x9}
