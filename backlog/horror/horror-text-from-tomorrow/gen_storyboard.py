#!/usr/bin/env python3
"""horror-text-from-tomorrow: timeline, pacing stats and storyboard.json from lines.py + tts_durations.json.

Inputs (this folder):
  lines.py             every spoken line (speaker, text, on-screen text, gap) and timed silences
  tts_durations.json   Kokoro-82M per-line durations + word stamps, measured on the Spark CPU (tts_measure.py)

usage: python3 gen_storyboard.py            writes storyboard.json + timing.json, prints the timed table and stats
       python3 gen_storyboard.py --stats    prints only

Every shot starts LEAD s before its anchor word; every bubble, knock and expression swap is anchored to the word
that names it. Kit components are used only with props that exist today; the two kit gaps (SockFeet, Padlock) are
inline SVG layers here, so nothing falls back. Re-snap after the real mix by re-measuring (same ids).
"""
from __future__ import annotations

import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lines as L  # noqa: E402

TTS = json.load(open(os.path.join(HERE, "tts_durations.json")))["lines"]
START = 0.25   # first word (frame 0 is the silent cover)
LEAD = 0.10    # a cut lands this long before its anchor word
SLUG = "horror-text-from-tomorrow"


def norm(w: str) -> str:
    return re.sub(r"[^a-z0-9]", "", w.lower())


# ------------------------------------------------------------------ timeline
LINES: dict[str, dict] = {}
ORDER: list[str] = []
SIL: dict[str, tuple[float, float]] = {}
SECTION_AT: list[tuple[str, str, float]] = []
t = START
entries = L.V
for i, e in enumerate(entries):
    if e[0] == "#":
        SECTION_AT.append((e[1], e[2], t))
        continue
    if e[0] == "~":
        SIL[e[1]] = (t, t + e[2])
        t += e[2]
        continue
    lid, spk, text, opts = e
    m = TTS[lid]
    toks = []
    for w in m["words"]:
        toks.append({"w": w["w"], "s": t + max(0.0, w["s"]), "e": t + max(0.0, w["e"])})
    LINES[lid] = {"id": lid, "spk": spk, "text": text, "opts": opts, "start": t, "end": t + m["dur"], "toks": toks}
    ORDER.append(lid)
    t += m["dur"]
    nxt = next((x for x in entries[i + 1:] if x[0] not in ("#",)), None)
    if "gap" in opts:
        t += opts["gap"]
    elif nxt is None or nxt[0] == "~":
        t += L.GAP
    else:
        t += L.GAP if nxt[1] == spk else L.TURN_GAP
TOTAL = round(t + 0.05, 2)


def at(lid: str, word: str | int = 0, nth: int = 0) -> float:
    """Global start time of a word in a line (by index among alnum tokens, or by text)."""
    toks = [k for k in LINES[lid]["toks"] if norm(k["w"])]
    if isinstance(word, int):
        return toks[word]["s"]
    hits = [k for k in toks if norm(k["w"]) == norm(word)]
    assert len(hits) > nth, f"{lid}: no '{word}' in {[k['w'] for k in toks]}"
    return hits[nth]["s"]


def end(lid: str) -> float:
    return LINES[lid]["end"]


# ------------------------------------------------------------------ captions
CAP = {  # (line, token) -> caption text ("" merges the token into the previous word)
    ("n1", "two"): "2:31.", ("n1", "thirty-one"): "",
    ("n2", "one"): "1:52.", ("n2", "fifty-two"): "",
    ("m1", "two"): "2:14", ("m1", "fourteen"): "",
    ("n9", "Two"): "2:14.", ("n9", "fourteen"): "",
    ("n10", "Thirty-seven"): "37",
    ("n12", "thirty-eight"): "38",
    ("o4", "two"): "2:30.", ("o4", "thirty"): "",
    ("d2", "it's"): "its",
    ("n18", "two"): "2:31,", ("n18", "thirty-one"): "",
}
EMPH = {("n1", "own"), ("m1", "beg"), ("m2", "sock"), ("n4", "hole"), ("o2", "roof"), ("l1", "out"),
        ("n10", "me"), ("n12", "38"), ("n15", "above"), ("n17", "roof"), ("n18", "2:31,"), ("m4", "went"),
        ("n19", "Me."), ("n21", "hole"), ("m5", "begging")}


def caption_words() -> list[dict]:
    out = []
    for lid in ORDER:
        line_words = []
        for k in LINES[lid]["toks"]:
            raw = k["w"]
            if not norm(raw):  # punctuation token: glue to previous word
                if line_words:
                    line_words[-1]["text"] += raw
                continue
            key = (lid, raw)
            txt = CAP.get(key, raw)
            if txt == "" and line_words:
                line_words[-1]["end"] = round(k["e"], 3)
                continue
            line_words.append({"text": txt, "start": round(k["s"], 3), "end": round(k["e"], 3)})
        for w in line_words:
            if (lid, w["text"]) in EMPH or (lid, w["text"].rstrip(".,?!")) in EMPH:
                w["emph"] = True
        if line_words:
            line_words[0]["br"] = True
        out += line_words
    # phrase pages: break inside a line on sentence ends and every <= 3 words
    n = 0
    for i, w in enumerate(out):
        if w.get("br"):
            n = 0
        elif n >= 3 or (i and out[i - 1]["text"][-1:] in ".?!,"):
            w["br"] = True
            n = 0
        n += 1
    return out


# ------------------------------------------------------------------ kit helpers
OFFICE = "Ostrel House Office"
MEMBERS = {
    OFFICE: {"color": "#4f7f86", "initials": "OH"},
    "Me": {"color": "#55704f", "initials": "T"},
    "Dee (3A)": {"color": "#8f6a4a", "initials": "D"},
    "Mrs. Lind (4C)": {"color": "#6a5a8f", "initials": "L"},
    "Jonah (1B)": {"color": "#4a628f", "initials": "J"},
    "Marta (5A)": {"color": "#8f4a63", "initials": "M"},
}
ACCENT = "#3d5a80"


def comp(name, props=None, **kw):
    d = {"type": "component", "name": name, "props": props or {}}
    d.update(kw)
    return d


def bedroom_bg(lamp=0.25, blur=10, opacity=0.6):
    return comp("horror/Bedroom", {"lamp": lamp, "rain": True}, depth=0.2, blur=blur, opacity=opacity)


def vignette(amount=0.45):
    return comp("horror/Vignette", {"amount": amount}, depth=0, z=50)


def hand_phone(phone, tremble=1.5, cy=0.585, **extra):
    p = {"phoneWidth": 0.68, "cx": 0.5, "cy": cy, "tilt": -2, "tremble": tremble, "side": "right", "phone": phone}
    p.update(extra)
    return comp("horror/HandPhone", p)


def chat(title, messages, clock, **kw):
    c = {"title": title, "messages": messages, "clock": clock, "battery": 18, "theme": "dark", "scale": 1.25, "accent": ACCENT}
    c.update(kw)
    return c


def me_thread(messages, clock, **kw):
    return chat("Me", messages, clock, dm="Me", subtitle="mobile · your number", **kw)


def residents(messages, clock, **kw):
    kw.setdefault("count", 39)
    kw.setdefault("pinned", {"from": OFFICE, "text": "Roof closed. Padlocked. Only the office has the key.", "at": -30})
    return chat("Ostrel House Residents", messages, clock, **kw)


def phone_scene(phone, cy=0.585, tremble=1.5, lamp=0.25, **hp):
    return [bedroom_bg(lamp), hand_phone(phone, tremble=tremble, cy=cy, **hp), vignette()]


def push(d, z0=1.0, z1=1.05, x="50%", y="50%"):
    return {"keyframes": [{"t": 0, "zoom": z0, "x": x, "y": y, "ease": "linear"}, {"t": round(d, 3), "zoom": z1, "x": x, "y": y, "ease": "linear"}]}


def protagonist(expr="worried", pose="phone", light="phone", **kw):
    p = {"expr": expr, "pose": pose, "light": light}
    p.update(kw)
    return comp("horror/Protagonist", p, x="50%", y="100%", anchorY=1, width=900, height=1368)


def svg_layer(markup, **kw):
    d = {"type": "svg", "markup": markup, "x": "50%", "y": "50%", "width": 1080, "height": 1920}
    d.update(kw)
    return d


# Kit gap 1 (required, no fallback): SockFeet, front-low view of two socked feet, hole at the LEFT big toe
# (viewer's right when the feet face us, so `mirror` flips it for the door-gap shot where they face us too).
def sock_feet(floor="#1d1a1c", glow=0.0, door=False, toe_light=1.0):
    door_edge = (
        '<rect x="0" y="0" width="1080" height="1180" fill="#2b2320"/>'
        '<rect x="0" y="1150" width="1080" height="34" fill="#1a1512" stroke="#0b0b0e" stroke-width="6"/>'
        if door else ""
    )
    spill = (f'<rect x="0" y="1184" width="1080" height="120" fill="#e7b46a" opacity="{0.25 * glow:.2f}"/>' if glow else "")
    fy = 1325 if door else 1230  # under a door, only the toes and the hole show below the door's bottom edge
    foot = lambda cx, hole: (  # noqa: E731
        f'<g transform="translate({cx} {fy}) scale(1.55)">'
        '<path d="M -150 140 Q -170 -10 -110 -60 Q -40 -95 40 -80 Q 130 -60 150 40 L 160 140 Z" fill="#8a90a0" stroke="#0b0b0e" stroke-width="10"/>'
        '<path d="M -130 60 Q 0 30 140 60" stroke="#6c7282" stroke-width="10" fill="none"/>'
        + "".join(f'<ellipse cx="{x}" cy="-58" rx="{r}" ry="{r * 0.8:.0f}" fill="#9aa1b2" stroke="#0b0b0e" stroke-width="7"/>'
                  for x, r in ((-95, 34), (-35, 30), (20, 27), (70, 24), (112, 20)))
        + (f'<ellipse cx="-95" cy="-64" rx="22" ry="17" fill="#f2cfa8" opacity="{toe_light:.2f}" stroke="#0b0b0e" stroke-width="5"/>'
           '<path d="M -118 -70 L -108 -52 M -74 -72 L -82 -52" stroke="#0b0b0e" stroke-width="4"/>' if hole else "")
        + "</g>"
    )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920">'
        f'<rect width="1080" height="1920" fill="{floor}"/>'
        + "".join(f'<line x1="0" x2="1080" y1="{y}" y2="{y}" stroke="#141214" stroke-width="5"/>' for y in (1320, 1420, 1540, 1690))
        + spill
        # left foot is on the viewer's right (feet face the camera); the hole is on the left foot's big toe (inner side)
        + foot(300, False).replace('scale(1.55)', 'scale(-1.55 1.55)')
        + foot(780, True).replace('scale(1.55)', 'scale(-1.55 1.55)')
        + door_edge
        + "</svg>"
    )


# Kit gap 2 (required): a padlock on the roof door's hasp, drawn over horror/Stairwell's fire door.
PADLOCK = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 260">'
    '<path d="M 50 110 L 50 70 Q 50 20 100 20 Q 150 20 150 70 L 150 110" fill="none" stroke="#9aa0a8" stroke-width="22"/>'
    '<rect x="25" y="105" width="150" height="130" rx="18" fill="#c9a24a" stroke="#0b0b0e" stroke-width="10"/>'
    '<circle cx="100" cy="160" r="16" fill="#2b2320"/><rect x="93" y="165" width="14" height="40" fill="#2b2320"/>'
    "</svg>"
)
ROOF_SIGN = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 110">'
    '<rect x="5" y="5" width="310" height="100" rx="10" fill="#7a1e1e" stroke="#0b0b0e" stroke-width="8"/>'
    '<text x="160" y="72" font-family="Montserrat, sans-serif" font-weight="900" font-size="54" fill="#f3e9e1" text-anchor="middle">ROOF</text>'
    "</svg>"
)

# ------------------------------------------------------------------ messages (word-anchored, global times)
CUES: list[dict] = []  # global SFX cues collected from the shot builders
WARN = "At 2:14 the office will call a gas leak and send everyone up to the roof. Don't go. Not even if they beg."
WARN_PARTS = ["At 2:14 the office will call a gas leak and send everyone up to the roof.", "Don't go.", "Not even if they beg."]


def warn_msgs(at0=-5.0):
    return [{"from": "Me", "text": x, "at": at0 + 0.1 * i} for i, x in enumerate(WARN_PARTS)]
PRED = ["First, the hall goes dark, door by door.", "The dog downstairs stops mid-bark.", "The office types for a full minute."]
OLD_RES = [
    {"from": "Jonah (1B)", "text": "anyone got a parcel for 1B?", "at": -60},
    {"from": "Marta (5A)", "text": "dryer 2 is broken again", "at": -50},
    {"from": OFFICE, "text": "Gas check done. All clear. Sleep well", "at": -40},
]


def shots():
    """(scene id, global start, builder(scene_start, duration) -> scene dict fields, beat tag)."""
    S = []

    def add(sid, t0, beat, fn):
        S.append((sid, round(t0, 3), beat, fn))

    # S1 cover + hook ------------------------------------------------------------------
    def lock_cover(s0, d):
        notes = [
            {"at": -1, "app": "Ostrel House Residents", "title": OFFICE, "text": "Gas check done. All clear. Sleep well · 1:49 AM"},
            {"at": -1, "app": "Messages · sent 2:31 AM", "title": "Me · 2:31 AM", "text": "At 2:14 the office will call a gas leak and send everyone up to the roof. Don't go…"},
        ]
        phone = {"members": MEMBERS, "mode": "lock", "lock": {"time": "1:52", "date": "Wednesday, November 11", "notifications": notes, "battery": 18},
                 "vibrate": [{"at": 0.15, "duration": 0.4}]}
        return {"layers": phone_scene(phone, lamp=0.2) + [
            {"type": "text", "text": "SENT 2:31 AM", "x": "50%", "y": "13%", "fontSize": 92, "color": "#ff4b55", "strokeColor": "#000000",
             "strokeWidth": 10, "start": 0, "end": 0.3, "exit": {"type": "fade", "duration": 0.15}}],
            "camera": push(d, 1.0, 1.04), "sfx": [{"cue": "notify", "at": 0.15, "volume": 0.8}], "captionY": 0.12}

    add("s01_cover", 0.0, "S1 hook (cover)", lock_cover)

    def lock_punch(s0, d):
        sc = lock_cover(s0, d)
        sc["layers"] = sc["layers"][:-1]
        sc["layers"][1]["props"]["phone"]["vibrate"] = []
        sc["layers"][1]["props"]["glitch"] = [{"at": 0.25, "duration": 0.35, "amount": 0.4}]
        sc["camera"] = {"keyframes": [{"t": 0, "zoom": 1.04, "x": "50%", "y": "50%"}, {"t": 0.35, "zoom": 1.3, "x": "50%", "y": "44%", "ease": "out"},
                                      {"t": round(d, 3), "zoom": 1.34, "x": "50%", "y": "44%", "ease": "linear"}]}
        sc["sfx"] = [{"cue": "glitch", "at": 0.25, "volume": 0.4}]
        return sc

    add("s02_punch", at("n2") - LEAD, "S1 hook (1:52 vs 2:31)", lock_punch)

    # S2 warning ------------------------------------------------------------------------
    def warning(s0, d):
        ts = [at("m1") - s0, at("m1", "Dont") - s0, at("m1", "Not") - s0]
        msgs = [{"from": "Me", "text": x, "at": round(a, 3)} for x, a in zip(WARN_PARTS, ts)]
        phone = {"members": MEMBERS, "mode": "chat", "chat": me_thread(msgs, "1:52", dayLabel="Today 2:31 AM")}
        beg = at("m1", "beg") - s0
        gas = at("m1", "gas") - s0
        cam = {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": round(gas, 2), "zoom": 1.01}, {"t": round(gas + 0.2, 2), "zoom": 1.05, "ease": "out"}, {"t": round(ts[1], 2), "zoom": 1.06}, {"t": round(ts[1] + 0.15, 2), "zoom": 1.1, "ease": "out"},
                             {"t": round(beg, 2), "zoom": 1.12}, {"t": round(beg + 0.15, 2), "zoom": 1.2, "y": "56%", "ease": "out"}, {"t": round(d, 3), "zoom": 1.21, "y": "56%"}]}
        return {"layers": phone_scene(phone, tremble=2), "camera": cam, "sfx": [{"cue": "message_pop", "at": round(a, 3), "volume": 0.7} for a in ts]}

    add("s03_warning", at("m1") - 0.35, "S2 warning (contradicts the all-clear)", warning)

    # S3 proof --------------------------------------------------------------------------
    def proof(s0, d):
        msgs = warn_msgs() + [
                {"from": "Me", "text": "You.", "at": round(at("m2", "You") - s0, 3)},
                {"from": "Me", "text": "Check your left sock.", "at": round(at("m2", "Check") - s0, 3)}]
        ty = at("n3", "who") - s0
        phone = {"members": MEMBERS, "mode": "chat", "chat": me_thread(msgs, "1:53", dayLabel="Today 2:31 AM", draft="who is this?")}
        taps = [{"at": round(ty + i * 0.18, 2), "x": 0.3 + 0.08 * (i % 5), "y": 0.9} for i in range(6)]
        return {"layers": phone_scene(phone, tremble=3, taps=taps), "camera": push(d, 1.02, 1.08),
                "sfx": [{"cue": "typing", "at": round(ty, 2), "volume": 0.6}, {"cue": "message_pop", "at": round(at("m2", "You") - s0, 3), "volume": 0.8},
                        {"cue": "message_pop", "at": round(at("m2", "Check") - s0, 3), "volume": 0.8}]}

    add("s04_proof", at("n3") - LEAD, "S3 impossible proof (answered before send)", proof)

    def sock_plant(s0, d):
        return {"background": {"type": "color", "color": "#0c0b0d"},
                "layers": [svg_layer(sock_feet(floor="#2a2324", glow=0.0, door=False, toe_light=1.0)),
                           comp("horror/Darkness", {"x": 0.55, "y": 0.64, "radius": 0.5, "darkness": 0.6}, depth=0, z=40), vignette(0.5)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.0, "x": "50%", "y": "58%"}, {"t": round(d, 3), "zoom": 1.12, "x": "62%", "y": "62%", "ease": "inOut"}]},
                "sfx": [{"cue": "heartbeat_slow", "at": 0.2, "volume": 0.7}], "captionY": 0.15}

    add("s05_sock", at("n4") - LEAD, "S3 plant paid (the sock hole)", sock_plant)

    # S4 predictions --------------------------------------------------------------------
    def predictions(s0, d):
        starts = [at("m3", "First"), at("m3", "The", 1), at("m3", "The", 2)]
        msgs = [{"from": "Me", "text": txt, "at": round(a - s0, 3)} for txt, a in zip(PRED, starts)]
        phone = {"members": MEMBERS, "mode": "chat", "chat": me_thread(msgs, "1:54", dayLabel="Today 2:31 AM")}
        return {"layers": phone_scene(phone, tremble=2), "camera": push(d, 1.0, 1.06),
                "sfx": [{"cue": "message_pop", "at": round(a - s0, 3), "volume": 0.7} for a in starts]}

    add("s06_predictions", at("m3") - 0.3, "S4 three predictions", predictions)

    # S2b authority + pinned rule -----------------------------------------------------
    def pinned(s0, d):
        c = residents(OLD_RES, "1:56")
        c["pinned"] = {"from": OFFICE, "text": "Roof closed. Padlocked. Only the office has the key.", "at": round(at("o1") - s0, 3)}
        phone = {"members": MEMBERS, "mode": "chat", "chat": c}
        pk = at("o1", "Padlocked") - s0
        cam = {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": round(pk, 2), "zoom": 1.03}, {"t": round(pk + 0.2, 2), "zoom": 1.22, "y": "34%", "ease": "out"}, {"t": round(d, 3), "zoom": 1.24, "y": "34%"}]}
        return {"layers": phone_scene(phone), "camera": cam, "transitionIn": {"type": "whip", "duration": 0.3, "direction": "left"},
                "sfx": [{"cue": "whoosh", "at": 0.0, "volume": 0.5}]}

    add("s07_pinned", at("o1") - 0.25, "S2 authority + pinned rule", pinned)

    def stair(s0, d):
        return {"background": {"type": "component", "name": "horror/Stairwell", "props": {"floor": "6", "flicker": 0.2, "exit": True}},
                "layers": [svg_layer(ROOF_SIGN, x=255, y=700, width=200, height=69),
                           svg_layer(PADLOCK, x=330, y=930, width=90, height=117, idle=[{"type": "sway", "amount": 2, "speed": 0.6}]),
                           vignette(0.5)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.05, "x": "50%", "y": "58%"}, {"t": round(d, 3), "zoom": 1.18, "x": "34%", "y": "50%", "ease": "inOut"}]},
                "sfx": [{"cue": "drone", "at": 0.0, "volume": 0.35}]}

    add("s08_roofdoor", at("n5") - LEAD, "S2 plant: last door before the roof stairs", stair)

    # S5 predictions land -------------------------------------------------------------
    def lights(s0, d):
        c1, c2, c3 = at("n6", "dark") - s0, at("n6", "light") - s0, at("n6", "mine") - s0
        track = [{"t": 0, "v": 0.85}, {"t": round(c1, 2), "v": 0.85}, {"t": round(c1 + 0.05, 2), "v": 0.55},
                 {"t": round(c2, 2), "v": 0.55}, {"t": round(c2 + 0.05, 2), "v": 0.25}, {"t": round(c3, 2), "v": 0.25}, {"t": round(c3 + 0.05, 2), "v": 0.0}]
        return {"background": {"type": "component", "name": "horror/FrontDoor", "props": {"hallLight": track, "chain": "on", "dark": 0.2}},
                "layers": [vignette(0.5)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": round(d, 3), "zoom": 1.06, "ease": "linear"}],
                           "shake": [{"at": round(c, 2), "duration": 0.15, "amplitude": 4} for c in (c1, c2, c3)]},
                "sfx": [{"cue": "click", "at": round(c, 2), "volume": v} for c, v in ((c1, 0.35), (c2, 0.6), (c3, 0.95))]}

    add("s09_lights", at("n6") - LEAD, "S5 prediction 1 (darkness travels TOWARD my door)", lights)

    def dog(s0, d):
        st = at("n7", "stopped") - s0
        return {"background": {"type": "color", "color": "#0b0d12"},
                "layers": [comp("horror/Bedroom", {"lamp": 0.1, "rain": True}, depth=0.2),
                           protagonist("worried", lookX=0.6, lookY=0.3, exprs=[{"t": 0, "e": "worried"}, {"t": round(st, 2), "e": "scared"}], blink=False),
                           vignette(0.55)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": round(st, 2), "zoom": 1.02}, {"t": round(st + 0.12, 2), "zoom": 1.12, "ease": "out"},
                                         {"t": round(d, 3), "zoom": 1.13}]}}

    add("s10_dog", at("n7") - LEAD, "S5 prediction 2 (the bark cut off)", dog)

    def typing(s0, d):
        c = residents(OLD_RES, "2:13", typing=[{"from": OFFICE, "at": round(at("n8", "typing") - s0, 2), "until": round(d + 0.5, 2)}])
        phone = {"members": MEMBERS, "mode": "chat", "chat": c}
        return {"layers": phone_scene(phone, tremble=2), "camera": push(d, 1.0, 1.1, y="40%"),
                "sfx": [{"cue": "clock_ticking", "at": 0.1, "volume": 0.4}]}

    add("s11_typing", at("n8") - LEAD, "S5 prediction 3 (the office types for a minute)", typing)

    # S6 turn -----------------------------------------------------------------------
    def turn(s0, d):
        a = at("o2") - s0
        c = residents(OLD_RES + [{"from": OFFICE, "kind": "alert", "text": "Gas leak. Everyone up to the roof. The door is open.", "at": round(a, 3)}], "2:14")
        phone = {"members": MEMBERS, "mode": "chat", "chat": c, "vibrate": [{"at": round(a, 2), "duration": 0.5, "amount": 1}]}
        door = at("o2", "door") - s0
        return {"layers": phone_scene(phone, tremble=4) + [
            comp("horror/RedText", {"text": "2:14", "at": 0.02, "duration": 0.6, "style": "flash"}, depth=0, z=60),
            comp("horror/Glitch", {"cues": [{"at": 0.02, "duration": 0.3, "amount": 0.6}]}, depth=0, z=61)],
            "camera": {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": 0.12, "zoom": 1.15, "ease": "out"}, {"t": round(door, 2), "zoom": 1.15, "y": "50%"},
                                     {"t": round(door + 0.35, 2), "zoom": 1.32, "y": "40%", "ease": "out"}, {"t": round(d, 3), "zoom": 1.34, "y": "40%"}],
                       "shake": [{"at": 0.02, "duration": 0.3, "amplitude": 16}]},
            "sfx": [{"cue": "stinger", "at": 0.02, "volume": 0.7}, {"cue": "phone_buzz", "at": round(a, 2), "volume": 0.8}]}

    add("s12_turn", at("n9") - LEAD, "S6 the 2:14 order (rule inverted)", turn)

    # S7 chorus, proxy, count chip ------------------------------------------------------
    def chorus(s0, d):
        prev = OLD_RES + [{"from": OFFICE, "kind": "alert", "text": "Gas leak. Everyone up to the roof. The door is open.", "at": -3}]
        new = [{"from": "Dee (3A)", "text": "EVERYONE UP", "at": round(at("d1") - s0, 3)},
               {"from": "Mrs. Lind (4C)", "text": "why UP?? you go OUT in a gas leak", "at": round(at("l1") - s0, 3)},
               {"from": OFFICE, "text": "Stairwell is full of gas. GO NOW.", "at": round(at("o3") - s0, 3)},
               {"kind": "system", "text": "37 replied: On my way", "at": round(at("n10") - s0, 3)}]
        typ = [{"from": "Mrs. Lind (4C)", "at": round(at("d1") - s0 + 0.4, 2), "until": round(at("l1") - s0, 2)}]
        c = residents(prev + new, "2:15", typing=typ, unread=5, unreadFrom=0)
        phone = {"members": MEMBERS, "mode": "chat", "chat": c}
        return {"layers": phone_scene(phone, tremble=4), "camera": push(d, 1.0, 1.06),
                "sfx": [{"cue": "notify", "at": round(m["at"], 2), "volume": 0.6} for m in new]}

    add("s13_chorus", at("d1") - 0.2, "S7 chorus (caps) + proxy objection shut down", chorus)

    def feet_pass(s0, d):
        pulses = [{"t": 0, "v": 0.0}]
        for w in ("feet", "past", "stairs", "ran"):
            a = at("n11", w) - s0
            pulses += [{"t": round(a, 2), "v": 0.0}, {"t": round(a + 0.2, 2), "v": 0.5}, {"t": round(a + 0.45, 2), "v": 0.0}]
        return {"background": {"type": "component", "name": "horror/FrontDoor", "props": {"hallLight": pulses, "chain": "on", "dark": 0.35}},
                "layers": [vignette(0.55)], "camera": push(d, 1.0, 1.08, y="70%"),
                "sfx": [{"cue": "footsteps", "at": round(at("n11", "feet") - s0, 2), "volume": 0.7}]}

    add("s14_feet_pass", at("n11") - LEAD, "S7 proximity: feet past my door, torches under the gap", feet_pass)

    def knock(s0, d):
        return {"background": {"type": "component", "name": "horror/FrontDoor", "props": {"hallLight": 0.0, "dark": 0.35, "knocks": [0.08], "chain": "on",
                                                                                     "handle": [{"at": 0.3, "duration": 0.4}]}},
                "layers": [vignette(0.55)], "camera": {"shake": [{"at": 0.08, "duration": 0.3, "amplitude": 10}]},
                "sfx": [{"cue": "knock3_slow", "at": 0.05, "volume": 0.9}]}

    add("s15_knock", end("n11") + 0.02, "S7 knock", knock)

    def peephole(s0, d):
        return {"background": {"type": "component", "name": "horror/Peephole",
                               "props": {"figure": "neighbour", "expr": "blank", "talk": [[0.0, round(end("a1") - s0, 2)]], "lean": 0.2, "flicker": 0.3, "exposure": 0.7}},
                "layers": [vignette(0.4)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": round(at("a1", "Everyone") - s0, 2), "zoom": 1.02}, {"t": round(d, 3), "zoom": 1.1, "ease": "in"}]}}

    add("s16_peephole", at("a1", "Its") - LEAD, "S7 the too-polite neighbour", peephole)

    def count(s0, d):
        c38 = at("n12", "thirty-eight") - s0
        return {"background": {"type": "color", "color": "#0b0d12"},
                "layers": [comp("horror/Bedroom", {"lamp": 0.1}, depth=0.2), protagonist("terrified", blink=False, lookY=0.2),
                           comp("horror/Heartbeat", {"bpm": 80, "bpmTo": 110, "from": round(c38, 2)}, depth=0, z=45), vignette(0.55)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": round(c38, 2), "zoom": 1.03}, {"t": round(c38 + 0.12, 2), "zoom": 1.16, "ease": "out"}, {"t": round(d, 3), "zoom": 1.17}]},
                "sfx": [{"cue": "heartbeat_fast", "at": round(c38, 2), "volume": 0.7}]}

    add("s17_count", at("n12") - LEAD, "S7 count deduction: 37 replied, 38 sets of feet", count)

    def tagged(s0, d):
        prev = OLD_RES + [{"from": OFFICE, "kind": "alert", "text": "Gas leak. Everyone up to the roof. The door is open.", "at": -8},
                          {"from": "Dee (3A)", "text": "EVERYONE UP", "at": -7}, {"from": "Mrs. Lind (4C)", "text": "why UP?? you go OUT in a gas leak", "at": -6},
                          {"from": OFFICE, "text": "Stairwell is full of gas. GO NOW.", "at": -5}, {"kind": "system", "text": "37 replied: On my way", "at": -4}]
        a = at("o4") - s0
        c = residents(prev + [{"from": OFFICE, "text": "@6A Last one. The roof locks at 2:30.", "at": round(a, 3)}], "2:22")
        phone = {"members": MEMBERS, "mode": "chat", "chat": c, "vibrate": [{"at": round(a, 2), "duration": 0.3}]}
        return {"layers": phone_scene(phone, tremble=3), "camera": push(d, 1.0, 1.08), "sfx": [{"cue": "notify", "at": round(a, 2), "volume": 0.8}]}

    add("s18_tagged", at("n13") - LEAD, "S7 tagged by unit + the 2:30 clock", tagged)

    # S8 lowercase, name checks, contact above -------------------------------------------
    def quiet(s0, d):
        prev = [{"from": OFFICE, "text": "@6A Last one. The roof locks at 2:30.", "at": -3}]
        new = [{"from": "Dee (3A)", "text": "its so quiet up here", "at": round(at("d2") - s0, 3)},
               {"me": True, "text": "Dee?", "at": round(at("n14", "Dee") - s0, 3)},
               {"me": True, "text": "Mrs Lind?", "at": round(at("n14", "Mrs") - s0, 3)},
               {"kind": "system", "text": "Seen", "at": round(at("n14", "Seen") - s0, 3)}]
        c = residents(prev + new, "2:26")
        phone = {"members": MEMBERS, "mode": "chat", "chat": c}
        return {"layers": phone_scene(phone, tremble=2, lamp=0.12), "camera": push(d, 1.0, 1.08),
                "sfx": [{"cue": "message_pop", "at": round(new[0]["at"], 2), "volume": 0.5}, {"cue": "message_send", "at": round(new[1]["at"], 2), "volume": 0.6},
                        {"cue": "message_send", "at": round(new[2]["at"], 2), "volume": 0.6}]}

    add("s19_quiet", at("d2") - 0.25, "S8 broken lowercase + two unanswered name checks", quiet)

    def above(s0, d):
        fs = at("n15", "footstep") - s0
        return {"background": {"type": "color", "color": "#07080b"},
                "layers": [comp("horror/Bedroom", {"lamp": 0.08}, depth=0.2),
                           comp("horror/Darkness", {"x": 0.5, "y": 0.05, "radius": 0.5, "darkness": 0.9}, depth=0, z=5),
                           {"type": "particles", "preset": "dust", "count": 70, "color": "#cfc6b8", "size": [2, 5], "speed": 0.6, "start": round(fs + 0.1, 2), "depth": 0, "z": 30,
                            "enter": {"type": "fade", "duration": 0.6}},
                           protagonist("terrified", lookY=-1, blink=False, scale=1.15), vignette(0.6)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.0, "y": "50%"}, {"t": round(fs, 2), "zoom": 1.04, "y": "48%"}], "shake": [{"at": round(fs, 2), "duration": 0.25, "amplitude": 6}]},
                "sfx": [{"cue": "impact", "at": round(fs, 2), "volume": 0.5}, {"cue": "drone", "at": 0.0, "volume": 0.3}]}

    add("s20_above", at("n15") - LEAD, "S8/B9 scariest image: one footstep above my bed, held", above)

    # S9 lifeline --------------------------------------------------------------------
    def gasline(s0, d):
        a = at("g1") - s0
        return {"background": {"type": "color", "color": "#0b0d12"},
                "layers": [comp("horror/Bedroom", {"lamp": 0.1}, depth=0.2), protagonist("worried", pose="ear", light="phone", lookX=-0.3, exprs=[{"t": 0, "e": "worried"}, {"t": round(a, 2), "e": "scared"}]), vignette(0.5)],
                "callouts": [{"style": "lowerThird", "text": "Gas Emergency Line", "sub": "calling…", "at": 0.15, "duration": round(a - 0.15, 2)},
                             {"style": "lowerThird", "text": "Gas Emergency Line", "sub": "No leak reported at that address", "at": round(a, 2)}],
                "camera": push(d, 1.0, 1.05), "sfx": [{"cue": "phone_buzz", "at": 0.1, "volume": 0.3}]}

    add("s21_gasline", at("n16") - LEAD, "S9 lifeline: the real authority says no leak", gasline)

    def calling(s0, d):
        msgs = [{"from": "Me", "text": "I went. Now you have to.", "at": 99}][:0] + [
            {"from": "Me", "text": PRED[2], "at": -6}, {"kind": "system", "text": "Calling Me…", "at": round(at("n17", "called") - s0, 3)}]
        phone = {"members": MEMBERS, "mode": "chat", "chat": me_thread(msgs, "2:29", dayLabel="Today 2:31 AM")}
        return {"layers": phone_scene(phone, tremble=3, lamp=0.1), "camera": push(d, 1.0, 1.06)}

    add("s22_calling", at("n17") - LEAD, "S9 I call my own number", calling)

    def ringtone(s0, d):
        return {"background": {"type": "color", "color": "#07080b"},
                "layers": [comp("horror/Bedroom", {"lamp": 0.08}, depth=0.2), comp("horror/Darkness", {"x": 0.5, "y": 0.05, "radius": 0.5, "darkness": 0.85}, depth=0, z=5),
                           protagonist("shocked", pose="ear", lookY=-1, blink=False), comp("horror/Heartbeat", {"bpm": 95, "bpmTo": 125}, depth=0, z=45), vignette(0.6)],
                "camera": push(d, 1.05, 1.15, y="45%"),
                "sfx": [{"cue": "ringtone_muffled", "at": 0.05, "volume": 0.35}]}

    add("s23_ringtone", at("n17", "Up") - LEAD, "S9 the ringtone is on the roof", ringtone)

    def ended(s0, d):
        msgs = [{"from": "Me", "text": PRED[2], "at": -6}, {"kind": "system", "text": "Calling Me…", "at": -2}, {"kind": "system", "text": "Call ended", "at": 0.05}]
        phone = {"members": MEMBERS, "mode": "chat", "chat": me_thread(msgs, "2:30", dayLabel="Today 2:31 AM")}
        return {"layers": phone_scene(phone, tremble=1, lamp=0.1), "sfx": [{"cue": "tick", "at": 0.05, "volume": 0.8}]}

    add("s24_230", SIL["q3"][0], "S9 clock runs out (2:30), ringtone stops", ended)

    # S10 twist --------------------------------------------------------------------
    def twist(s0, d):
        msgs = warn_msgs() + [
                {"kind": "system", "text": "Today 2:31 AM", "at": round(at("n18", "new") - s0, 3)},
                {"from": "Me", "text": "I went. Now you have to.", "at": round(at("m4") - s0, 3)}]
        phone = {"members": MEMBERS, "mode": "chat", "chat": me_thread(msgs, "2:31", dayLabel="Today 2:31 AM")}
        g = at("m4") - s0
        return {"layers": phone_scene(phone, tremble=3, lamp=0.1, glitch=[{"at": round(g + 0.9, 2), "duration": 0.3, "amount": 0.3}]),
                "camera": {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": round(g, 2), "zoom": 1.05}, {"t": round(g + 0.15, 2), "zoom": 1.22, "y": "58%", "ease": "out"}, {"t": round(d, 3), "zoom": 1.24, "y": "58%"}]},
                "sfx": [{"cue": "message_pop", "at": round(g, 2), "volume": 0.9}, {"cue": "glitch", "at": round(g + 0.9, 2), "volume": 0.4}]}

    add("s25_twist", at("n18") - LEAD, "S10 twist: same minute, same sender", twist)

    def rename(s0, d):
        prev = [{"from": OFFICE, "text": "@6A Last one. The roof locks at 2:30.", "at": -9}, {"from": "Dee (3A)", "text": "its so quiet up here", "at": -8},
                {"me": True, "text": "Dee?", "at": -7}, {"me": True, "text": "Mrs Lind?", "at": -6}, {"kind": "system", "text": "Seen", "at": -5}]
        a = at("n19", "name") - s0
        c = residents(prev + [{"kind": "system", "text": "Ostrel House Office changed their name to Me", "at": round(a, 3)}], "2:31")
        c["pinned"] = {"from": "Me", "text": "Roof closed. Padlocked. Only the office has the key.", "at": -30, "edited": True}
        phone = {"members": MEMBERS, "mode": "chat", "chat": c}
        return {"layers": phone_scene(phone, tremble=2, lamp=0.1, glitch=[{"at": round(a, 2), "duration": 0.25, "amount": 0.35}]),
                "camera": {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": round(a, 2), "zoom": 1.04}, {"t": round(a + 0.2, 2), "zoom": 1.25, "y": "62%", "ease": "out"}, {"t": round(d, 3), "zoom": 1.26, "y": "62%"}]},
                "sfx": [{"cue": "glitch", "at": round(a, 2), "volume": 0.35}]}

    add("s26_rename", at("n19") - LEAD, "S10 the office was me (closes the padlock/authority loop)", rename)

    def door_stop(s0, d):
        st = at("n20", "stopped") - s0
        return {"background": {"type": "component", "name": "horror/FrontDoor", "props": {"hallLight": 0.4, "dark": 0.3, "chain": "on", "feet": [round(st, 2), 99]}},
                "layers": [vignette(0.55)], "camera": push(d, 1.0, 1.12, y="78%"),
                "sfx": [{"cue": "footsteps", "at": 0.05, "volume": 0.6}]}

    add("s27_door", at("n20") - LEAD, "S10 one set of feet stops at my door", door_stop)

    def gap(s0, d):
        so = at("n21", "under") - s0
        return {"background": {"type": "color", "color": "#050507"},
                "layers": [svg_layer(sock_feet(floor="#1d1a1c", glow=1.0, door=True, toe_light=1.0), start=round(so, 2), enter={"type": "fade", "duration": 0.35}),
                           {"type": "rect", "x": "50%", "y": 1190, "width": 1080, "height": 10, "fill": "#e7b46a", "opacity": 0.55},
                           vignette(0.55)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.25, "x": "50%", "y": "61%"}, {"t": round(so, 2), "zoom": 1.25, "x": "50%", "y": "61%"},
                                         {"t": round(at("n21", "hole") - s0, 2), "zoom": 1.3, "x": "55%", "y": "61%"},
                                         {"t": round(d, 3), "zoom": 1.45, "x": "64%", "y": "62%", "ease": "inOut"}]},
                "sfx": [{"cue": "heartbeat_fast", "at": 0.0, "volume": 0.6}]}

    add("s28_gap", at("n21") - LEAD, "S9 proof held: the holed sock under the door", gap)

    def cliff(s0, d):
        a = at("m5") - s0
        notes = [{"at": -1, "app": "Messages", "title": "Me · 2:31 AM", "text": WARN},
                 {"at": round(a, 3), "app": "Messages · now", "title": "Me", "text": "Please. I'm begging you. Open up. It's just me."}]
        phone = {"members": MEMBERS, "mode": "lock", "lock": {"time": "2:33", "date": "Wednesday, November 11", "notifications": notes, "battery": 9},
                 "vibrate": [{"at": round(a, 2), "duration": 0.5}]}
        return {"layers": phone_scene(phone, tremble=5, lamp=0.05, glitch=[{"at": round(d - 0.35, 2), "duration": 0.3, "amount": 0.4}]),
                "camera": push(d, 1.04, 1.1), "captionY": 0.12,
                "sfx": [{"cue": "notify", "at": round(a, 2), "volume": 0.8}, {"cue": "stinger", "at": round(end("m5") - s0 + 0.05, 2), "volume": 0.8}]}

    add("s29_cliff", at("n22") - LEAD, "S10 cliff: the beg, bookend lock screen", cliff)
    return S


# ------------------------------------------------------------------ stats
def stats():
    words = sum(len(LINES[k]["text"].split()) for k in ORDER)
    sents = []
    for k in ORDER:
        sents += [s for s in re.split(r"(?<=[.?!])\s+", LINES[k]["text"]) if s.strip()]
    lens = [len(s.split()) for s in sents]
    nums = re.findall(r"\b(one fifty-two|two thirty-one|two fourteen|two thirty|thirty-seven|thirty-eight)\b", " ".join(LINES[k]["text"].lower() for k in ORDER))
    speech = sum(LINES[k]["end"] - LINES[k]["start"] for k in ORDER)
    return {"total_s": TOTAL, "words": words, "wpm_overall": round(words / TOTAL * 60, 1), "wpm_speech": round(words / speech * 60, 1),
            "sentences": len(sents), "sentence_median": statistics.median(lens), "punch_share": round(sum(1 for x in lens if x <= 4) / len(lens), 2),
            "spoken_numbers": len(nums), "numbers_per_min": round(len(nums) / TOTAL * 60, 1),
            "hook_words": len((LINES["n1"]["text"] + " " + LINES["n2"]["text"]).split()), "hook_end_s": round(end("n2"), 2),
            "silences_s": round(sum(b - a for a, b in SIL.values()), 2)}


def mmss(x):
    return f"{int(x // 60)}:{x % 60:04.1f}"


def main():
    CUES.clear()
    S = shots()
    S.sort(key=lambda s: s[1])
    scenes = []
    for i, (sid, t0, beat, fn) in enumerate(S):
        t1 = S[i + 1][1] if i + 1 < len(S) else TOTAL
        d = round(t1 - t0, 3)
        body = fn(t0, d)
        sc = {"id": sid, "duration": d, "background": body.pop("background", {"type": "color", "color": "#0b0d12"})}
        sc.update(body)
        spoken = [LINES[k]["text"] for k in ORDER if t0 - 0.05 <= LINES[k]["start"] < t1 - 0.05]
        sc["notes"] = f"[{beat}] " + " ".join(spoken)
        for c in sc.pop("sfx", []):  # horror episodes bake SFX into mix.wav: keep cues global, for the mixer
            CUES.append({"cue": c["cue"], "at": round(t0 + c["at"], 3), "volume": c.get("volume", 0.8)})
        scenes.append(sc)
    words = caption_words()
    sb = {
        "version": 1, "id": SLUG, "title": "My Own Number Texted Me 39 Minutes Early", "format": "9:16", "fps": 30,
        "scenes": scenes,
        "captions": {"words": words, "maxWords": 3, "maxChars": 18, "gapBreak": 0.3,
                     "style": {"font": "display", "fontSize": 64, "color": "#ffffff", "highlight": "#ff4b55", "highlightMode": "none",
                               "strokeWidth": 10, "uppercase": False, "y": 0.12, "backing": 0.85}},
        "audio": {"voice": [{"src": f"episodes/{SLUG}/mix.wav", "start": 0, "volume": 1, "duration": TOTAL}], "music": [], "sfx": [], "duckOn": "none"},
        "overlays": {"grain": 0.5, "vignette": 0.35, "fadeIn": 0, "fadeOut": 0},
        "_built": {"by": f"backlog/horror/{SLUG}/gen_storyboard.py", "timing": "kokoro-82M cpu per-line stamps (tts_durations.json)",
                   "audio": f"studio/public/episodes/{SLUG}/mix.wav (Spark; voice per lines.VOICES with lines.FX, SFX from _sfx_cues baked in)"},
        "_voices": {k: {"name": L.SPEAKER_NAME[k], "kokoro": v[0], "speed": v[1], "fx": L.FX.get(k, "none")} for k, v in L.VOICES.items()},
        "_sfx_cues": sorted(CUES, key=lambda c: c["at"]),
        "_sfx_new": {"ringtone_muffled": "synthesize on the Spark: ffmpeg aevalsrc 3-note marimba-like loop (660/880/990 Hz, 0.18 s notes), "
                                         "lowpass 600 Hz, volume 0.3, 3.5 s; never reuse phone_buzz_long (a vibration)"},
    }
    st = stats()
    timing = {"total_s": TOTAL, "stats": st,
              "lines": [{"id": k, "spk": LINES[k]["spk"], "voice": TTS[k]["voice"], "speed": TTS[k]["speed"], "start": round(LINES[k]["start"], 2),
                         "end": round(LINES[k]["end"], 2), "text": LINES[k]["text"]} for k in ORDER],
              "silences": {k: [round(a, 2), round(b, 2)] for k, (a, b) in SIL.items()},
              "sections": [(k, n, round(x, 2), round(100 * x / TOTAL, 1)) for k, n, x in SECTION_AT],
              "scenes": [{"id": s["id"], "start": round(S[i][1], 2), "dur": s["duration"], "beat": S[i][2]} for i, s in enumerate(scenes)]}
    if "--stats" not in sys.argv:
        json.dump(sb, open(os.path.join(HERE, "storyboard.json"), "w"), indent=1, ensure_ascii=False)
        json.dump(timing, open(os.path.join(HERE, "timing.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps(st, indent=1))
    for k, n, x in SECTION_AT:
        print(f"  {mmss(x):>7} {100 * x / TOTAL:5.1f}%  {n}")
    for i, s in enumerate(scenes):
        print(f"  {s['id']:18} {S[i][1]:6.2f} +{s['duration']:5.2f}  {S[i][2]}")
    for k in ORDER:
        print(f"  {k:4} {LINES[k]['start']:6.2f}-{LINES[k]['end']:6.2f} {LINES[k]['spk']} {LINES[k]['text']}")
    print("silences", {k: (round(a, 2), round(b, 2)) for k, (a, b) in SIL.items()})


if __name__ == "__main__":
    main()
