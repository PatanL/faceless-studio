#!/usr/bin/env python3
"""horror-babysitter-parent-rules: timeline, pacing stats and storyboard.json from lines.py + tts_durations.json.

Inputs (this folder):
  lines.py             every spoken line (speaker, text, on-screen text, gap) and timed silences
  tts_durations.json   Kokoro-82M per-line durations + word stamps, measured on the Spark CPU (tts_measure.py)

usage: python3 gen_storyboard.py            writes storyboard.json + timing.json, prints the timed table and stats
       python3 gen_storyboard.py --stats    prints only

Every shot starts LEAD s before its anchor word; every prop cue (knock, readout swap, key press, arm, mouth, chain)
is anchored to the word that names it, in SCENE-LOCAL seconds. The horror kit is locked (BRIEF 11:27), so the kit
gaps (fridge note, cream cards, monitor feed with Theo, under-bed arm, receiver, chain insert, lock-screen preview)
are inline SVG layers here; only registered kit components are used, with props that exist today.
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
SLUG = "horror-babysitter-parent-rules"
TITLE = "The Parents Called. They Didn't Know Their Own Password."
KNOCK_HITS = (0.0, 0.32, 0.64)  # knock3.wav hit offsets (measured)


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
    toks = [{"w": w["w"], "s": t + max(0.0, w["s"]), "e": t + max(0.0, w["e"])} for w in m["words"]]
    LINES[lid] = {"id": lid, "spk": spk, "text": text, "opts": opts, "start": t, "end": t + m["dur"], "toks": toks}
    ORDER.append(lid)
    t += m["dur"]
    nxt = next((x for x in entries[i + 1:] if x[0] != "#"), None)
    if "gap" in opts:
        t += opts["gap"]
    elif nxt is None or nxt[0] == "~":
        t += L.GAP
    else:
        t += L.GAP if nxt[1] == spk else L.TURN_GAP
TOTAL = round(t + 0.05, 2)


def at(lid: str, word: str | int = 0, nth: int = 0) -> float:
    toks = [k for k in LINES[lid]["toks"] if norm(k["w"])]
    if isinstance(word, int):
        return toks[word]["s"]
    hits = [k for k in toks if norm(k["w"]) == norm(word)]
    assert len(hits) > nth, f"{lid}: no '{word}' in {[k['w'] for k in toks]}"
    return hits[nth]["s"]


def wend(lid: str, word: str, nth: int = 0) -> float:
    toks = [k for k in LINES[lid]["toks"] if norm(k["w"]) == norm(word)]
    return toks[nth]["e"]


def end(lid: str) -> float:
    return LINES[lid]["end"]


def r(x: float) -> float:
    return round(x, 3)


# ------------------------------------------------------------------ captions
CAP = {
    ("n1", "thirty-fourth"): "34th", ("n1", "five"): "5",
    ("n3", "seven"): "7:40", ("n3", "forty"): "",
    ("n6", "nine"): "9",
    ("n7", "seven"): "7:12", ("n7", "twelve"): "",
    ("n9", "one"): "1", ("n9", "eight"): "8", ("n10", "two"): "2", ("n11", "three"): "3", ("n12", "four"): "4",
    ("n13", "Twelve"): "12", ("n13", "Twenty"): "20", ("n13", "Thirty-one"): "31", ("n14", "thirty-four"): "34",
    ("n16", "five"): "5", ("d2", "five"): "5",
    ("d3", "One"): "1", ("d3b", "Two"): "2", ("d3c", "Three"): "3", ("d4", "Four"): "4", ("d4b", "Five"): "5",
    ("n18", "four"): "4", ("n19", "Nine"): "9:40", ("n19", "forty"): "",
    ("n25", "four"): "4", ("n27", "four"): "4", ("n30", "two"): "2", ("n31", "five"): "5",
}
EMPH = {("n1", "password"), ("c1", "What"), ("c1", "password"), ("w1", "Marmalade"), ("k1", "Marmalade"), ("n6", "9"),
        ("n7", "7:12"), ("n8", "let"), ("n11", "buzz"), ("n12", "you"), ("n14", "Nobody"), ("d1", "Marmalade"),
        ("n16", "had"), ("n17", "never"), ("d4b", "5"), ("n19", "dinner"), ("n20", "Not"), ("t1", "won't"),
        ("n23", "Something"), ("t2", "Ivy"), ("n27", "three"), ("n28", "pencil"), ("n29", "out"), ("n30", "2"),
        ("n32", "my"), ("e1", "Marmalade")}
QUOTED = {"c1", "w1", "k1", "c2", "d1", "d2", "d3", "d3b", "d3c", "d4", "d4b", "t1", "t2", "e1"}  # other voices: caption in quotes


def caption_words() -> list[dict]:
    out = []
    for lid in ORDER:
        lw = []
        for k in LINES[lid]["toks"]:
            raw = k["w"]
            if not norm(raw):
                if lw:
                    lw[-1]["text"] += raw
                continue
            txt = CAP.get((lid, raw), raw)
            if txt == "" and lw:
                lw[-1]["end"] = r(k["e"])
                continue
            lw.append({"text": txt, "start": r(k["s"]), "end": r(k["e"])})
        for w in lw:
            if (lid, w["text"]) in EMPH or (lid, w["text"].rstrip(".,?!:")) in EMPH:
                w["emph"] = True
        if lw:
            lw[0]["br"] = True
            if lid in QUOTED:
                lw[0]["text"] = "“" + lw[0]["text"]
                lw[-1]["text"] = lw[-1]["text"] + "”"
        out += lw
    n = 0
    for i, w in enumerate(out):
        if w.get("br"):
            n = 0
        elif n >= 3 or (i and out[i - 1]["text"].rstrip("”")[-1:] in ".?!,:"):
            w["br"] = True
            n = 0
        n += 1
    return out


# ------------------------------------------------------------------ kit helpers
DOYLE = "Mrs. Doyle"
MEMBERS = {DOYLE: {"color": "#8f5a4a", "initials": "D"}, "Ivy": {"color": "#5b4a7a", "initials": "I"}}
ACCENT = "#4a5f8f"
IVY_COLORS = {"hair": "#7a3b22", "top": "#5b4a7a", "topShade": "#463a5e"}   # recoloured: not the Nora of horror-mom-two-chats
RED = "#ff4b55"
CUES: list[dict] = []


def comp(name, props=None, **kw):
    d = {"type": "component", "name": name, "props": props or {}}
    d.update(kw)
    return d


def svg_layer(markup, **kw):
    d = {"type": "svg", "markup": markup, "x": "50%", "y": "50%", "width": 1080, "height": 1920}
    d.update(kw)
    return d


def text(txt, x="50%", y="50%", size=48, color="#ffffff", **kw):
    d = {"type": "text", "text": txt, "x": x, "y": y, "fontSize": size, "color": color, "strokeColor": "#000000", "strokeWidth": 8}
    d.update(kw)
    return d


def vignette(amount=0.45, **p):
    return comp("horror/Vignette", {"amount": amount, **p}, depth=0, z=50)


def living_bg(lamp=0.35, blur=10, opacity=0.6):
    return comp("horror/LivingRoom", {"lamp": lamp}, depth=0.2, blur=blur, opacity=opacity)


def hand_phone(phone, tremble=1.5, cy=0.585, **extra):
    p = {"phoneWidth": 0.68, "cx": 0.5, "cy": cy, "tilt": -2, "tremble": tremble, "side": "right", "phone": phone}
    p.update(extra)
    return comp("horror/HandPhone", p)


def doyle_thread(messages, clock, **kw):
    c = {"title": DOYLE, "messages": messages, "clock": clock, "battery": 31, "theme": "dark", "scale": 1.25, "accent": ACCENT,
         "dm": DOYLE, "subtitle": "mobile"}
    c.update(kw)
    return {"members": MEMBERS, "mode": "chat", "chat": c}


OLD_THREAD = [
    {"kind": "system", "text": "Today 7:41 PM", "at": -100},
    {"from": DOYLE, "text": "Thank you Ivy!! Have a quiet night x", "at": -99},
    {"kind": "system", "text": "9:40 PM", "at": -90},
    {"from": DOYLE, "text": "Still at dinner! Back by 11:30 x", "at": -89},
]


def handset(sms_from, sms_text, clock="9:41", header="HOME", at=-1.0, vibrate=None, backlight=1.0, **kw):
    """The cordless house phone (FeaturePhone). Static readouts: cps 400 so the line shows at once."""
    p = {"header": header, "clock": clock, "sms": {"from": sms_from, "text": sms_text, "at": at, "cps": 400}, "backlight": backlight}
    if vibrate:
        p["vibrate"] = vibrate
    d = comp("horror/FeaturePhone", p, x="50%", y="52%", width=630, height=1365)
    d.update(kw)
    return d


def push(d, z0=1.0, z1=1.05, x="50%", y="50%"):
    return {"keyframes": [{"t": 0, "zoom": z0, "x": x, "y": y, "ease": "linear"}, {"t": r(d), "zoom": z1, "x": x, "y": y, "ease": "linear"}]}


def ivy(expr="worried", pose="phone", light="phone", **kw):
    p = {"expr": expr, "pose": pose, "light": light, "colors": IVY_COLORS}
    p.update(kw)
    return comp("horror/Protagonist", p, x="50%", y="100%", anchorY=1, width=900, height=1368)


# ------------------------------------------------------------------ inline SVG (kit gaps)
PENCIL = "#6b6b74"
MARKER = "#1f2d6b"
REDMK = "#c8102e"
F = "Montserrat, sans-serif"

# (number, hand, [lines], first-line y)
RULES = [
    ("1.", "pencil", ["Asleep by 8. Don't wake him,", "whatever you hear."], 560),
    ("2.", "marker", ["Chain on till we text", "from the lobby."], 700),
    ("3.", "marker", ["We have keys.", "We never knock."], 850),
    ("4.", "pencil", ["If Theo talks in his sleep, don't", "answer him. He isn't talking to you."], 1000),
    ("5.", "red", ["Nobody comes in without", "the password. If we call,", "ask for it. Wrong answer?", "Hang up."], 1150),
]
RULE_Y = {i + 1: y for i, (_, _, _, y) in enumerate(RULES)}


def _rule_text(num, hand, lines, y0):
    out = [f'<text x="190" y="{y0}" font-family="{F}" font-style="italic" font-weight="500" font-size="40" fill="{PENCIL}" '
           f'transform="skewX(-10) translate({y0 * 0.176:.0f} 0)">{num}</text>']
    for j, ln in enumerate(lines):
        y = y0 + j * (50 if hand == "pencil" else 58)
        ln = ln.replace("'", "&#8217;")
        if hand == "pencil":
            out.append(f'<text x="270" y="{y}" font-family="{F}" font-style="italic" font-weight="500" font-size="35" '
                       f'fill="{PENCIL}" letter-spacing="-0.5" transform="skewX(-12) translate({y * 0.21:.0f} 0)">{ln}</text>')
        else:
            col = REDMK if hand == "red" else MARKER
            out.append(f'<text x="260" y="{y}" font-family="{F}" font-weight="800" font-size="46" fill="{col}">{ln}</text>')
    if hand == "red":
        yl = y0 + 3 * 58 + 16
        out.append(f'<path d="M 255 {yl} Q 520 {yl + 8} 820 {yl - 2}" stroke="{REDMK}" stroke-width="7" fill="none" stroke-linecap="round"/>')
        out.append(f'<path d="M 262 {yl + 18} Q 520 {yl + 26} 800 {yl + 14}" stroke="{REDMK}" stroke-width="6" fill="none" stroke-linecap="round"/>')
    return "".join(out)


def fridge_note(counter=True):
    """Steel fridge door, magnet, cream note with 5 rules in two hands (pencil: the numbers + rules 1 and 4; marker: 2, 3, 5)."""
    lines = "".join(f'<line x1="150" x2="930" y1="{y}" y2="{y}" stroke="#b9c6d8" stroke-width="2" opacity="0.6"/>' for y in range(470, 1400, 58))
    rules = "".join(_rule_text(*rr) for rr in RULES)
    ctr = ('<rect x="0" y="1500" width="1080" height="420" fill="#3a2a20"/>'
           '<rect x="0" y="1500" width="1080" height="26" fill="#5a4232"/>'
           '<rect x="0" y="1526" width="1080" height="10" fill="#1d140f" opacity="0.6"/>') if counter else ""
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920">'
        '<defs><linearGradient id="st" x1="0" x2="1"><stop offset="0" stop-color="#7f8890"/><stop offset="0.45" stop-color="#c7ced4"/>'
        '<stop offset="0.6" stop-color="#aeb6bd"/><stop offset="1" stop-color="#7a8289"/></linearGradient></defs>'
        '<rect width="1080" height="1920" fill="url(#st)"/>'
        '<rect x="985" y="0" width="34" height="1500" rx="12" fill="#5d656c" stroke="#3b4046" stroke-width="4"/>'
        '<rect x="0" y="0" width="1080" height="1920" fill="#000" opacity="0.18"/>'
        '<g transform="rotate(-1.5 540 860)">'
        '<rect x="128" y="318" width="830" height="1110" fill="#000" opacity="0.25" transform="translate(10 14)"/>'
        '<rect x="128" y="318" width="830" height="1110" fill="#f3ead2"/>'
        + lines
        + f'<line x1="240" x2="240" y1="330" y2="1420" stroke="#e5a1a1" stroke-width="3" opacity="0.7"/>'
        f'<text x="260" y="450" font-family="{F}" font-weight="800" font-size="52" fill="{MARKER}">Ivy, thank you!! x</text>'
        + rules
        + "</g>"
        '<circle cx="548" cy="330" r="42" fill="#b3232c" stroke="#5a0f14" stroke-width="5"/><circle cx="536" cy="318" r="12" fill="#ff8f8f" opacity="0.6"/>'
        + ctr + "</svg>"
    )


def highlight(rule: int, color="#ffe14d", opacity=0.45, rows=None):
    y0 = RULE_Y[rule]
    hand = RULES[rule - 1][1]
    n = rows or len(RULES[rule - 1][2])
    step = 50 if hand == "pencil" else 58
    h = (n - 1) * step + 62
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920"><g transform="rotate(-1.5 540 860)">'
            f'<rect x="180" y="{y0 - 46}" width="740" height="{h}" rx="10" fill="{color}" opacity="{opacity}"/></g></svg>')


def pencil_rings():
    rings = ""
    for rule in (1, 4):
        y0 = RULE_Y[rule]
        h = len(RULES[rule - 1][2]) * 50 + 40
        rings += f'<ellipse cx="560" cy="{y0 + h / 2 - 50}" rx="420" ry="{h / 2 + 10}" fill="none" stroke="{RED}" stroke-width="9"/>'
    for y in RULE_Y.values():
        rings += f'<circle cx="208" cy="{y - 14}" r="34" fill="none" stroke="{RED}" stroke-width="6"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920"><g transform="rotate(-1.5 540 860)">{rings}</g></svg>'


def lock_preview(time="9:41", title=f"{DOYLE} · 9:40 PM", body="Still at dinner! Back by 11:30 x"):
    """Ivy's phone face-up on the counter: lock screen with ONE big notification (legible in the cover)."""
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 860">'
        '<rect x="6" y="6" width="448" height="848" rx="60" fill="#0d0f14" stroke="#2b2f37" stroke-width="10"/>'
        '<rect x="24" y="24" width="412" height="812" rx="46" fill="#1b2340"/>'
        f'<text x="230" y="190" text-anchor="middle" font-family="{F}" font-weight="800" font-size="110" fill="#e8ecf5">{time}</text>'
        '<rect x="40" y="250" width="380" height="190" rx="28" fill="#f2f2f5" opacity="0.94"/>'
        '<rect x="62" y="272" width="44" height="44" rx="10" fill="#34c759"/>'
        f'<text x="120" y="304" font-family="{F}" font-weight="800" font-size="28" fill="#111">{title}</text>'
        f'<text x="62" y="362" font-family="{F}" font-weight="700" font-size="30" fill="#111">{body.split("! ")[0]}!</text>'
        f'<text x="62" y="404" font-family="{F}" font-weight="700" font-size="30" fill="#111">{body.split("! ", 1)[1]}</text>'
        "</svg>"
    )


def cream_card(word="marmalade", child=False):
    if child:
        cols = ["#2f7a3a", "#c0392b", "#2f5aa8", "#d68910", "#7d3c98"]
        letters = "".join(
            f'<text x="{150 + i * 88}" y="{1000 + (18 if i % 2 else -14)}" font-family="{F}" font-weight="900" font-size="{120 + (i * 37) % 40}" '
            f'fill="{cols[i % 5]}" transform="rotate({(-14, 9, -6, 12, -10, 7, -12, 10, -5)[i % 9]} {150 + i * 88} 980)">{ch}</text>'
            for i, ch in enumerate(word))
    else:
        letters = f'<text x="540" y="1010" text-anchor="middle" font-family="{F}" font-weight="800" font-size="130" fill="{MARKER}" transform="rotate(-3 540 980)">{word}</text>'
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920">'
        '<rect width="1080" height="1920" fill="#0c0b0e"/>'
        '<rect x="80" y="700" width="920" height="560" fill="#000" opacity="0.4" transform="translate(12 16)"/>'
        '<rect x="80" y="700" width="920" height="560" fill="#f3ead2" transform="rotate(-1 540 980)"/>'
        + letters + "</svg>"
    )


def chain_plate():
    """Insert: the door's edge and the chain track on the frame (static part)."""
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920">'
        '<rect width="1080" height="1920" fill="#2a211c"/>'
        '<rect x="0" y="0" width="640" height="1920" fill="#5a3f2e"/><rect x="600" y="0" width="40" height="1920" fill="#3d2a1f"/>'
        '<rect x="640" y="0" width="440" height="1920" fill="#d9cfc0"/><rect x="640" y="0" width="22" height="1920" fill="#a99f91"/>'
        '<rect x="700" y="880" width="300" height="70" rx="14" fill="#b8b2a6" stroke="#0b0b0e" stroke-width="7"/>'
        '<rect x="730" y="905" width="250" height="20" rx="10" fill="#3a3632"/>'
        '<rect x="430" y="930" width="120" height="90" rx="12" fill="#b8b2a6" stroke="#0b0b0e" stroke-width="7"/>'
        '<circle cx="490" cy="975" r="14" fill="#3a3632"/>'
        "</svg>"
    )


def chain_and_hand():
    """Moving part: the knob in the slot, the hanging chain, Ivy's fingers on the knob (local box 1080x1920, same origin)."""
    links = "".join(f'<ellipse cx="{490 + i * 30}" cy="{975 + 26 * (1 - ((i - 4.5) / 4.5) ** 2) * 2.2:.0f}" rx="18" ry="10" fill="none" '
                    f'stroke="#cfc8bb" stroke-width="7" transform="rotate({(-25 + i * 5)} {490 + i * 30} 975)"/>' for i in range(10))
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920">'
        + links
        + '<circle cx="790" cy="915" r="26" fill="#d8d2c6" stroke="#0b0b0e" stroke-width="7"/>'
        '<path d="M 760 905 Q 790 850 840 860 Q 905 870 960 940 L 1080 1010 L 1080 1120 Q 960 1080 880 1010 Q 820 960 790 940 Z" '
        'fill="#e9b996" stroke="#0b0b0e" stroke-width="8"/>'
        '<path d="M 790 905 Q 800 880 826 884 M 812 925 Q 826 900 852 906" stroke="#0b0b0e" stroke-width="6" fill="none"/>'
        '<path d="M 980 1010 Q 1020 1060 1080 1080 L 1080 1200 Q 1010 1180 960 1110 Z" fill="#5b4a7a" stroke="#0b0b0e" stroke-width="8"/>'
        "</svg>"
    )


def flashback_frame():
    """Two dark door-frame edges + a warm spill: 'seen from the hall, outside Theo's door'."""
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920">'
            '<rect x="0" y="0" width="170" height="1920" fill="#120d0b"/><rect x="910" y="0" width="170" height="1920" fill="#120d0b"/>'
            '<rect x="0" y="0" width="1080" height="150" fill="#120d0b"/>'
            '<rect x="170" y="150" width="12" height="1770" fill="#3a2a20"/><rect x="898" y="150" width="12" height="1770" fill="#3a2a20"/>'
            '</svg>')


# --- the monitor feed (night vision): Theo's room drawn here, so the bed fills the frame and his head reads at ~200 px
def monitor_room(pose="profile"):
    bed = (
        '<rect width="1080" height="1920" fill="#2b302d"/>'
        '<rect x="0" y="1330" width="1080" height="590" fill="#1c201e"/>'
        '<rect x="60" y="760" width="70" height="560" rx="10" fill="#3c4440" stroke="#0b0b0e" stroke-width="8"/>'   # headboard post
        '<rect x="60" y="760" width="250" height="300" rx="20" fill="#3c4440" stroke="#0b0b0e" stroke-width="8"/>'  # headboard
        '<rect x="90" y="1120" width="940" height="70" rx="16" fill="#8d9690" stroke="#0b0b0e" stroke-width="8"/>'  # mattress
        '<rect x="90" y="1190" width="940" height="40" fill="#46504a" stroke="#0b0b0e" stroke-width="8"/>'         # frame rail
        '<rect x="110" y="1230" width="900" height="120" fill="#030404"/>'                                            # THE GAP under the bed
        '<rect x="96" y="1230" width="30" height="120" fill="#3c4440" stroke="#0b0b0e" stroke-width="6"/>'
        '<rect x="990" y="1230" width="30" height="120" fill="#3c4440" stroke="#0b0b0e" stroke-width="6"/>'
        '<rect x="150" y="1040" width="300" height="100" rx="46" fill="#c7cec9" stroke="#0b0b0e" stroke-width="8"/>'  # pillow
        '<path d="M 400 1125 Q 430 1010 600 1030 Q 760 1000 880 1050 Q 990 1080 1010 1125 Z" fill="#6f7b74" stroke="#0b0b0e" stroke-width="8"/>'  # blanket lump
        '<path d="M 470 1060 Q 600 1050 700 1070" stroke="#56615a" stroke-width="8" fill="none"/>'
    )
    if pose == "wall":  # facing the wall: back of the head only, blanket up to the neck
        head = ('<ellipse cx="330" cy="1010" rx="92" ry="86" fill="#3a3330" stroke="#0b0b0e" stroke-width="8"/>'
                '<path d="M 250 990 Q 300 930 380 950" stroke="#26201e" stroke-width="10" fill="none"/>'
                '<path d="M 300 1095 Q 380 1050 460 1080 L 460 1125 L 300 1125 Z" fill="#6f7b74" stroke="#0b0b0e" stroke-width="8"/>')
    else:  # profile on the pillow, face up, eyes shut (the mouth is a separate layer)
        head = ('<ellipse cx="330" cy="1020" rx="92" ry="84" fill="#d9c2ae" stroke="#0b0b0e" stroke-width="8"/>'
                '<path d="M 240 1000 Q 250 925 340 932 Q 400 936 410 975 Q 350 960 300 985 Z" fill="#3a3330" stroke="#0b0b0e" stroke-width="6"/>'
                '<path d="M 412 1012 Q 432 1022 416 1036" stroke="#0b0b0e" stroke-width="6" fill="#d9c2ae"/>'   # nose
                '<path d="M 362 1000 Q 378 1010 394 1000" stroke="#0b0b0e" stroke-width="6" fill="none"/>'      # closed eye
                '<path d="M 300 1098 Q 380 1060 460 1086 L 460 1125 L 300 1125 Z" fill="#6f7b74" stroke="#0b0b0e" stroke-width="8"/>')
    stand = ('<rect x="0" y="1110" width="50" height="230" fill="#3c4440" stroke="#0b0b0e" stroke-width="6"/>')
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920">' + bed + head + stand + "</svg>"


MOUTH_OPEN = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920">'
              '<ellipse cx="400" cy="1056" rx="13" ry="10" fill="#2a1414" stroke="#0b0b0e" stroke-width="4"/></svg>')
MOUTH_SHUT = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920">'
              '<path d="M 388 1056 L 410 1054" stroke="#0b0b0e" stroke-width="5"/></svg>')
RECEIVER = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920">'
            '<g transform="rotate(-62 330 1040)"><rect x="170" y="1005" width="330" height="76" rx="34" fill="#e6ebe8" stroke="#0b0b0e" stroke-width="8"/>'
            '<rect x="210" y="1022" width="40" height="40" rx="8" fill="#9aa5a0"/><rect x="420" y="1022" width="40" height="40" rx="8" fill="#9aa5a0"/></g></svg>')
# the arm: a long grey forearm out of the under-bed gap, up the mattress edge, fingers around the receiver
ARM = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920">'
       '<path d="M 230 1360 Q 205 1260 214 1180 Q 222 1120 262 1088 Q 290 1066 318 1060 L 330 1082 Q 300 1094 282 1116 '
       'Q 252 1160 254 1240 Q 258 1300 280 1360 Z" fill="#3b403d" stroke="#0b0b0e" stroke-width="7"/>'
       '<path d="M 300 1062 Q 300 1010 318 975 M 318 1066 Q 330 1010 352 990 M 330 1078 Q 360 1040 388 1032 M 296 1080 Q 268 1056 262 1022" '
       'stroke="#3b403d" stroke-width="15" fill="none" stroke-linecap="round"/>'
       '<path d="M 300 1062 Q 300 1010 318 975 M 318 1066 Q 330 1010 352 990 M 330 1078 Q 360 1040 388 1032 M 296 1080 Q 268 1056 262 1022" '
       'stroke="#0b0b0e" stroke-width="3" fill="none" opacity="0.7"/></svg>')

NV_GRADE = {"saturate": 0.0, "tint": "#3cff8c", "tintOpacity": 0.38, "contrast": 1.25, "brightness": 0.95}


def monitor_ui(clock="9:43 PM", status="No movement since 7:12 PM", talk=None):
    L_ = [text("● LIVE · Nursery cam", x=80, y=300, size=44, color="#ff3b30", align="left", anchorX=0, depth=0, z=30),
          text(clock, x=1000, y=300, size=40, color="#e8ffe8", align="right", anchorX=1, depth=0, z=30),
          text(status, x="50%", y=1440, size=46, color="#e8ffe8", depth=0, z=30),
          comp("horror/Glitch", {"amount": 0.12}, depth=0, z=40)]
    mic = {"type": "circle", "x": "50%", "y": 1330, "width": 120, "height": 120, "fill": "#2d3330", "stroke": "#e8ffe8",
           "strokeWidth": 5, "depth": 0, "z": 31}
    L_.append(mic)
    if talk is not None:
        L_.append({"type": "circle", "x": "50%", "y": 1330, "width": 120, "height": 120, "fill": "#ff3b30", "depth": 0, "z": 32,
                   "start": r(talk), "enter": {"type": "pop", "duration": 0.2}, "idle": [{"type": "pulse", "amount": 0.08, "speed": 1.5}]})
        L_.append(text("TALK", x="50%", y=1335, size=30, color="#ffffff", depth=0, z=33, start=r(talk)))
    return L_


# ------------------------------------------------------------------ shots
def shots():
    S = []

    def add(sid, t0, beat, fn):
        S.append((sid, round(t0, 3), beat, fn))

    def note_scene(d, cam, extra=(), counter=True, ring_at=None, glitch=None):
        lay = [svg_layer(fridge_note(counter))] + list(extra) + [vignette(0.35)]
        sc = {"background": {"type": "color", "color": "#0b0d12"}, "layers": lay, "camera": cam}
        return sc

    # B1 cover: the note + ringing handset + lock preview (threat in frame 0) ---------------------------
    def cover(s0, d):
        hs = comp("horror/FeaturePhone", {"header": "HOME", "clock": "9:41", "sms": {"from": "INCOMING", "text": "DOYLE", "at": -1, "cps": 400},
                                          "vibrate": [{"at": 0.1, "duration": 1.2}, {"at": 2.4, "duration": 1.2}]},
                  x=270, y=1690, width=280, height=606, rotate=-5, z=10)
        lk = svg_layer(lock_preview(), x=790, y=1745, width=380, height=710, rotate=7, z=11)
        cam = {"keyframes": [{"t": 0, "zoom": 1.0, "x": "50%", "y": "50%"}, {"t": r(d), "zoom": 1.04, "x": "50%", "y": "52%", "ease": "linear"}]}
        sc = note_scene(d, cam, extra=[svg_layer(highlight(5, color=RED, opacity=0.12), start=0), hs, lk])
        sc["sfx"] = [{"cue": "phone_buzz_long", "at": 0.1, "volume": 0.55}]
        sc["captionY"] = 0.12
        return sc

    add("s01_cover", 0.0, "B1 hook (cover: note + ringing handset + 'Still at dinner!')", cover)

    def rule5_punch(s0, d):
        cam = {"keyframes": [{"t": 0, "zoom": 1.04, "x": "50%", "y": "52%"}, {"t": 0.35, "zoom": 1.42, "x": "50%", "y": "64%", "ease": "out"},
                             {"t": r(d), "zoom": 1.45, "x": "50%", "y": "64%"}]}
        sc = note_scene(d, cam, extra=[svg_layer(highlight(5, opacity=0.5, rows=3), start=r(at("n1", "call") - s0), enter={"type": "wipeRight", "duration": 0.4})])
        sc["captionY"] = 0.13
        sc["sfx"] = [{"cue": "phone_buzz_long", "at": 0.3, "volume": 0.4}]
        return sc

    add("s02_rule5", at("n1", "Rule") - LEAD, "B1 hook (rule five, read)", rule5_punch)

    def call(s0, d):
        return {"layers": [living_bg(0.35), handset("DOYLE", "00:04", clock="9:41"), vignette(0.5)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": 0.15, "zoom": 1.1, "ease": "out"}, {"t": r(d), "zoom": 1.12}]},
                "sfx": [{"cue": "click", "at": 0.05, "volume": 0.6}]}

    add("s03_call", at("n2") - LEAD, "B1 the call", call)

    def what_pw(s0, d):
        pw = at("c1", "password") - s0
        return {"layers": [living_bg(0.4, blur=0, opacity=1), ivy("neutral", pose="ear", light="none",
                                                                     exprs=[{"t": 0, "e": "neutral"}, {"t": r(pw), "e": "suspicious"}]),
                           comp("horror/Glitch", {"cues": [{"at": r(pw), "duration": 0.22, "amount": 0.3}]}, depth=0, z=60), vignette(0.45)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": r(pw), "zoom": 1.02}, {"t": r(pw + 0.15), "zoom": 1.12, "ease": "out"}, {"t": r(d), "zoom": 1.13}]},
                "sfx": [{"cue": "glitch", "at": r(pw), "volume": 0.3}]}

    add("s04_whatpw", at("c1") - LEAD, "B4 trusted voice fails the check", what_pw)

    # PLANT: the whisper outside Theo's door -----------------------------------------------------------
    def flashback(s0, d):
        return {"background": {"type": "component", "name": "horror/Bedroom", "props": {"lamp": 0.55, "rain": False}},
                "layers": [svg_layer(flashback_frame(), depth=0.6, z=5),
                           comp("horror/Darkness", {"x": 0.5, "y": 0.68, "radius": 0.55, "darkness": 0.35}, depth=0, z=20),
                           vignette(0.6, color="255,200,150"), comp("horror/Flicker", {"strength": 0.04}, depth=0, z=51)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.08, "x": "46%", "y": "55%"}, {"t": r(d), "zoom": 1.16, "x": "52%", "y": "62%", "ease": "linear"}]},
                "transitionIn": {"type": "dipBlack", "duration": 0.3}, "grade": {"saturate": 0.7, "tint": "#ffb36b", "tintOpacity": 0.25},
                "sfx": [{"cue": "whoosh", "at": 0.0, "volume": 0.35}]}

    add("s05_flashback", at("n3") - LEAD, "PLANT whispered outside Theo's door at 7:40", flashback)

    def card_w(s0, d):
        return {"layers": [svg_layer(cream_card()), vignette(0.6, color="255,200,150")], "camera": push(d, 1.0, 1.05),
                "grade": {"tint": "#ffb36b", "tintOpacity": 0.15}}

    add("s06_card_mum", at("w1") - LEAD, "PLANT rung 1: the parent's mouth", card_w)

    def click(s0, d):
        c = at("n4", "clicked") - s0
        return {"layers": [living_bg(0.3), handset("DOYLE", "00:12", end=r(c)),
                           handset("EXT 2", "THEO'S ROOM · ON LINE", start=r(c), glitch=[{"at": 0.0, "duration": 0.2, "amount": 0.4}]),
                           vignette(0.5)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": r(c), "zoom": 1.06}, {"t": r(c + 0.2), "zoom": 1.22, "y": "40%", "ease": "out"}, {"t": r(d), "zoom": 1.24, "y": "40%"}]},
                "sfx": [{"cue": "click", "at": r(c), "volume": 0.9}]}

    add("s07_click", at("n4") - LEAD, "B3 the hang-up interrupted (extension on the line)", click)

    def ext_room(s0, d):
        return {"background": {"type": "component", "name": "horror/Bedroom", "props": {"lamp": 0.0, "phoneGlow": True, "rain": True}},
                "layers": [svg_layer(flashback_frame(), depth=0.6, z=5),
                           comp("horror/Darkness", {"x": 0.7, "y": 0.6, "radius": 0.25, "darkness": 0.9}, depth=0, z=20), vignette(0.6)],
                "camera": push(d, 1.0, 1.08), "sfx": [{"cue": "static", "at": 0.1, "volume": 0.2}]}

    add("s08_extension", at("n5") - LEAD, "B3 Theo's extension picked up", ext_room)

    def card_k(s0, d):
        return {"layers": [svg_layer(cream_card(child=True)), vignette(0.7)], "camera": push(d, 1.0, 1.06),
                "sfx": [{"cue": "stinger", "at": 0.08, "volume": 0.55}]}

    add("s09_card_child", at("k1") - LEAD, "B3 rung 2: the child's mouth", card_k)

    def boy(s0, d):
        return {"layers": [living_bg(0.45, blur=0, opacity=1), ivy("relieved", pose="ear", light="none"), vignette(0.4)],
                "camera": push(d, 1.0, 1.04)}

    add("s10_myboy", at("c2") - LEAD, "B3 the caller closes happily (false relief)", boy)

    def nine(s0, d):
        n = at("n6", "nine") - s0
        glow = {"type": "circle", "x": 315 + 417, "y": int(0.52 * 1920 - 682 + 958), "width": 120, "height": 90, "fill": "#ffe9a8", "opacity": 0.7,
                "start": r(n), "end": r(n + 0.35), "blend": "screen", "depth": 1, "z": 20}
        return {"layers": [living_bg(0.3), handset("DOYLE", "00:21", end=r(n + 0.25)),
                           handset("LOBBY DOOR", "RELEASED", start=r(n + 0.25)), glow, vignette(0.5)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": r(n), "zoom": 1.04}, {"t": r(n + 0.2), "zoom": 1.15, "y": "45%", "ease": "out"}, {"t": r(d), "zoom": 1.16, "y": "45%"}]},
                "sfx": [{"cue": "click", "at": r(n), "volume": 0.9}, {"cue": "phone_buzz", "at": r(n + 0.25), "volume": 0.35}]}

    add("s11_nine", at("n6") - LEAD, "B3 compliance: she buzzes them up", nine)

    # B4 proof on the monitor ---------------------------------------------------------------------------
    def monitor_wall(s0, d):
        return {"background": {"type": "color", "color": "#000000"},
                "layers": [svg_layer(monitor_room("wall"))] + monitor_ui(clock="9:42 PM"),
                "camera": {"keyframes": [{"t": 0, "zoom": 1.3, "x": "42%", "y": "57%"}, {"t": r(d), "zoom": 1.4, "x": "38%", "y": "56%", "ease": "linear"}]},
                "grade": NV_GRADE, "transitionIn": {"type": "glitch", "duration": 0.25},
                "sfx": [{"cue": "static", "at": 0.0, "volume": 0.35}]}

    add("s12_monitor", at("n7") - LEAD, "B4 proof: asleep, no movement since 7:12", monitor_wall)

    def guilt(s0, d):
        lt = at("n8", "let") - s0
        return {"layers": [living_bg(0.25, blur=0, opacity=1), ivy("worried", pose="phone", light="phone", exprs=[{"t": 0, "e": "worried"}, {"t": r(lt), "e": "scared"}]), vignette(0.5)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": r(lt), "zoom": 1.03}, {"t": r(lt + 0.15), "zoom": 1.13, "ease": "out"}, {"t": r(d), "zoom": 1.14}]},
                "sfx": [{"cue": "breath", "at": r(lt), "volume": 0.4}]}

    add("s13_guilt", at("n8") - LEAD, "B4 verdict: and I'd let them in", guilt)

    # B2 rules as cards: the same note, zoomed to each rule (the note reads as one object) ---------------
    def rule_card(rule, lid, zoom=1.42, extra_fn=None):
        def fn(s0, d):
            y = RULE_Y[rule]
            yy = f"{(y + 40) / 1920 * 100:.1f}%"
            cam = {"keyframes": [{"t": 0, "zoom": zoom - 0.06, "x": "50%", "y": yy}, {"t": r(d), "zoom": zoom, "x": "50%", "y": yy, "ease": "linear"}]}
            ex = [svg_layer(highlight(rule, opacity=0.4), start=0.05, enter={"type": "wipeRight", "duration": 0.35})]
            sc = note_scene(d, cam, extra=ex, counter=False)
            sc["sfx"] = [{"cue": "tick", "at": 0.02, "volume": 0.5}]
            sc["captionY"] = 0.1
            if extra_fn:
                extra_fn(sc, s0, d)
            return sc
        return fn

    add("s14_rule1", at("n9") - LEAD, "B2 rule 1 (pencil)", rule_card(1, "n9"))

    def r2_extra(sc, s0, d):
        sc["layers"].insert(-1, comp("horror/FrontDoor", {"chain": "on", "hallLight": 0.3}, opacity=0.15, depth=0, z=1))

    add("s15_rule2", at("n10") - LEAD, "B2 rule 2 (marker): no lobby text", rule_card(2, "n10", extra_fn=r2_extra))

    def r3_extra(sc, s0, d):
        b = at("n11", "So") - s0
        sc["camera"]["keyframes"] = [sc["camera"]["keyframes"][0], {"t": r(b), "zoom": 1.4, "x": "50%", "y": sc["camera"]["keyframes"][0]["y"]},
                                     {"t": r(b + 0.2), "zoom": 2.0, "x": "40%", "y": sc["camera"]["keyframes"][0]["y"], "ease": "out"},
                                     {"t": r(d), "zoom": 2.02, "x": "40%", "y": sc["camera"]["keyframes"][0]["y"]}]
        sc["sfx"].append({"cue": "glitch", "at": r(b), "volume": 0.25})

    add("s16_rule3", at("n11") - LEAD, "B2 rule 3 (marker): the keys tell", rule_card(3, "n11", extra_fn=r3_extra))

    def r4_extra(sc, s0, d):
        g = at("n12", "He") - s0
        sc["layers"].append(comp("horror/Glitch", {"cues": [{"at": r(g), "duration": 0.3, "amount": 0.55}]}, depth=0, z=60))
        sc["sfx"].append({"cue": "glitch", "at": r(g), "volume": 0.45})
        sc["sfx"].append({"cue": "heartbeat_slow", "at": r(g + 0.2), "volume": 0.4})

    add("s17_rule4", at("n12") - LEAD, "B2 rule 4 (pencil): he isn't talking to you", rule_card(4, "n12", zoom=1.4, extra_fn=r4_extra))

    # B5 proximity: the elevator she called -------------------------------------------------------------
    def elev(s0, d):
        a12, a31 = at("n13", "Twelve") - s0, at("n13", "Thirty-one") - s0
        pf = (a31 - a12) / 19.0
        panel = comp("horror/ElevatorPanel", {"from": 11, "to": 31, "at": r(a12 - pf), "perFloor": round(pf, 4), "target": 34, "floors": 12, "flicker": 0.1},
                     x="50%", y="50%", width=1080, height=1920, anchorY=0.2, scale=2.0)
        return {"background": {"type": "color", "color": "#000000"},
                "layers": [panel, vignette(0.95, inner=0.35), comp("horror/Flicker", {"strength": 0.06}, depth=0, z=51)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.0, "x": "50%", "y": "50%"}, {"t": r(d), "zoom": 1.05, "x": "51%", "y": "50%"}]},
                "transitionIn": {"type": "whip", "duration": 0.25, "direction": "left"},
                "sfx": [{"cue": "tick", "at": r(x), "volume": 0.5} for x in (a12, at("n13", "Twenty") - s0, a31)]}

    add("s18_elevator", at("n13") - LEAD, "B5 the elevator climbs (12, 20, 31)", elev)

    def elev34(s0, d):
        a34 = at("n14", "thirty-four") - s0
        nb = at("n14", "Nobody") - s0
        panel = comp("horror/ElevatorPanel", {"from": 31, "to": 34, "at": 0.0, "perFloor": round(max(0.05, a34 / 3.0), 3), "target": 34, "floors": 12},
                     x="50%", y="50%", width=1080, height=1920, anchorY=0.2, scale=2.0, end=r(nb))
        hall = comp("horror/Peephole", {"figure": "none", "radius": 0.42, "flicker": 0.1}, x="50%", y="50%", width=1080, height=1920, start=r(nb), z=5)
        return {"background": {"type": "color", "color": "#000000"},
                "layers": [panel, hall, vignette(0.95, inner=0.35)],
                "camera": push(d, 1.0, 1.04), "sfx": [{"cue": "ding", "at": r(a34 + 0.25), "volume": 0.6}]}

    add("s19_floor34", at("n14") - LEAD, "B5 34; nobody got out (held through the 0.7 s silence)", elev34)

    # B8 turn at the door ---------------------------------------------------------------------------
    k0 = end("n15") + 0.15  # knock3 plays in the clear, after the line

    def knocks(s0, d):
        ks = [r(k0 - s0 + h) for h in KNOCK_HITS]
        return {"background": {"type": "component", "name": "horror/FrontDoor", "props": {"knocks": ks, "chain": "on", "hallLight": 0.6, "feet": False}},
                "layers": [vignette(0.5)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": r(d), "zoom": 1.06}], "shake": [{"at": k, "duration": 0.15, "amplitude": 10} for k in ks]},
                "sfx": [{"cue": "knock3", "at": r(k0 - s0), "volume": 1.0, "hush": 1.6}]}

    add("s20_knocks", at("n15") - LEAD, "B8 three knocks (rule 3 broken)", knocks)

    def door_voice(s0, d):
        mm = at("d1", "Marmalade") - s0
        return {"background": {"type": "component", "name": "horror/FrontDoor", "props": {"chain": "on", "hallLight": 0.6, "peepholeGlow": True, "feet": False,
                                                                                           "handle": [{"at": r(mm), "duration": 0.5}]}},
                "layers": [vignette(0.55)], "camera": push(d, 1.1, 1.25, y="42%"),
                "sfx": [{"cue": "drone", "at": 0.0, "volume": 0.4}]}

    add("s21_doorvoice", at("d1") - LEAD, "B8 rung 3: the door has the password", door_voice)

    def r5door(s0, d):
        y = RULE_Y[5]
        yy = f"{(y + 30) / 1920 * 100:.1f}%"
        cam = {"keyframes": [{"t": 0, "zoom": 1.4, "x": "50%", "y": yy}, {"t": r(d), "zoom": 1.46, "x": "50%", "y": yy}]}
        sc = note_scene(d, cam, extra=[svg_layer(highlight(5, opacity=0.45, rows=2), start=0.05, enter={"type": "wipeRight", "duration": 0.4})], counter=False)
        h = at("n16", "had") - s0
        sc["layers"].append(comp("horror/Glitch", {"cues": [{"at": r(h), "duration": 0.2, "amount": 0.3}]}, depth=0, z=60))
        sc["captionY"] = 0.1
        sc["sfx"] = [{"cue": "tick", "at": 0.02, "volume": 0.5}]
        return sc

    add("s22_rule5door", at("n16") - LEAD, "B8 rule 5 says let him in", r5door)

    def chain(s0, d):
        sl, nk, lg = at("n17", "slid") - s0, at("n17", "never") - s0, at("n17", "let") - s0
        mover = svg_layer(chain_and_hand(), keyframes=[{"t": 0, "x": "50%"}, {"t": r(sl), "x": "50%"}, {"t": r(sl + 0.35), "x": 512, "ease": "out"},
                                                       {"t": r(nk), "x": 512}, {"t": r(lg), "x": 512, "y": "50%"},
                                                       {"t": r(lg + 0.4), "x": 640, "y": 1080, "ease": "inOut"}])
        return {"background": {"type": "color", "color": "#000000"},
                "layers": [svg_layer(chain_plate()), mover, comp("horror/Darkness", {"x": 0.68, "y": 0.5, "radius": 0.45, "darkness": 0.75}, depth=0, z=20), vignette(0.5)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.3, "x": "62%", "y": "49%"}, {"t": r(sl), "zoom": 1.32, "x": "62%", "y": "49%"},
                                         {"t": r(sl + 0.3), "zoom": 1.45, "x": "64%", "y": "49%", "ease": "out"}, {"t": r(d), "zoom": 1.46, "x": "64%", "y": "49%"}]},
                "sfx": [{"cue": "click", "at": r(sl), "volume": 0.7}, {"cue": "chain_slide", "at": r(sl), "volume": 0.8, "_new": True},
                        {"cue": "breath", "at": r(lg), "volume": 0.4}]}

    add("s23_chain", at("n17") - LEAD, "B8 near-miss: the chain slides an inch; rule 3 stops her", chain)

    # B10 lifeline under the door's count ------------------------------------------------------------
    def door_count(lid, handle=True, quiet=False):
        def fn(s0, d):
            h = [{"at": 0.05, "duration": 0.35}] if handle else []
            return {"background": {"type": "component", "name": "horror/FrontDoor", "props": {"chain": "on", "hallLight": 0.5 if not quiet else 0.2,
                                                                                               "feet": False, "handle": h}},
                    "layers": [vignette(0.6)],
                    "camera": {"keyframes": [{"t": 0, "zoom": 1.15, "y": "45%"}, {"t": r(d), "zoom": 1.2, "y": "45%"}]}}
        return fn

    add("s24_count", at("d2") - LEAD, "B10 the door sets a count (the clock)", door_count("d2", handle=False))

    def texting(s0, d):
        a1, a2 = at("n18", "Are") - s0, at("n18", "What") - s0
        msgs = OLD_THREAD + [{"me": True, "from": "Ivy", "text": "Are you outside?", "at": r(a1)},
                             {"me": True, "from": "Ivy", "text": "What does rule 4 mean?", "at": r(a2)}]
        return {"layers": [living_bg(0.2), hand_phone(doyle_thread(msgs, "9:44"), tremble=3), vignette(0.5)],
                "camera": push(d, 1.0, 1.05), "sfx": [{"cue": "typing", "at": 0.1, "volume": 0.5}, {"cue": "message_send", "at": r(a1), "volume": 0.7},
                                                          {"cue": "message_send", "at": r(a2), "volume": 0.7}]}

    add("s25_texting", at("n18") - LEAD, "B10 lifeline: texts the real mother", texting)

    for lid in ("d3", "d3b", "d3c"):
        add(f"s26_{lid}", at(lid) - LEAD, f"B10 count ({LINES[lid]['text']})", door_count(lid))

    def missed(s0, d):
        msgs = OLD_THREAD + [{"me": True, "from": "Ivy", "text": "Are you outside?", "at": -3},
                             {"me": True, "from": "Ivy", "text": "What does rule 4 mean?", "at": -2}]
        nf = at("n19", "Nine") - s0
        return {"layers": [living_bg(0.2), hand_phone(doyle_thread(msgs, "9:44"), tremble=3), vignette(0.5)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.0, "y": "50%"}, {"t": r(nf - 0.3), "zoom": 1.05, "y": "50%"},
                                         {"t": r(nf), "zoom": 1.32, "y": "47%", "ease": "out"}, {"t": r(d), "zoom": 1.34, "y": "47%"}]}}

    add("s27_missed", at("n19") - LEAD, "B10 the missed 9:40 text (pays frame 0)", missed)

    def delivered(s0, d):
        msgs = OLD_THREAD + [{"me": True, "from": "Ivy", "text": "Are you outside?", "at": -3},
                             {"me": True, "from": "Ivy", "text": "What does rule 4 mean?", "at": -2},
                             {"kind": "system", "text": "Delivered · not read", "at": r(at("n20") - s0)}]
        return {"layers": [living_bg(0.2), hand_phone(doyle_thread(msgs, "9:44"), tremble=4), vignette(0.5)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.2, "y": "60%"}, {"t": r(d), "zoom": 1.26, "y": "62%"}]}}

    add("s28_delivered", at("n20") - LEAD, "B10 delivered, not read", delivered)

    add("s29_d4", at("d4") - LEAD, "B10 count (Four.)", door_count("d4"))
    add("s30_d4b", at("d4b") - LEAD, "B10 count (Five.)", door_count("d4b"))

    def quiet(s0, d):
        cr = at("n21", "monitor") - s0
        notes = [{"at": r(cr), "app": "Nursery cam", "title": "Sound detected", "text": "Theo's room · now"}]
        phone = {"members": MEMBERS, "mode": "lock", "lock": {"time": "9:44", "date": "Saturday, October 31", "notifications": notes, "battery": 31},
                 "vibrate": [{"at": r(cr), "duration": 0.4}]}
        return {"layers": [comp("horror/FrontDoor", {"chain": "on", "hallLight": 0.15}, depth=0.2, blur=8, opacity=0.6), hand_phone(phone, tremble=3), vignette(0.5)],
                "camera": push(d, 1.0, 1.05), "sfx": [{"cue": "static", "at": r(cr), "volume": 0.45}]}

    add("s31_quiet", at("n21") - LEAD, "B10 the door goes quiet; the monitor crackles (channel switch)", quiet)

    # B9 peak on the monitor -------------------------------------------------------------------------
    def talk_keys(a, b, step=0.12):
        ks, x, on = [{"t": 0, "opacity": 0}], a, True
        while x < b:
            ks.append({"t": r(x), "opacity": 1 if on else 0, "ease": "linear"})
            on, x = not on, x + step
        ks.append({"t": r(b), "opacity": 0})
        return ks

    def peak_build(s0, d):
        mv = at("n22", "moving") - s0
        t1a, t1b = LINES["t1"]["start"] - s0, end("t1") - s0
        lay = [svg_layer(monitor_room("profile")), svg_layer(MOUTH_SHUT),
               svg_layer(MOUTH_OPEN, opacity=0, keyframes=talk_keys(mv, mv + 0.8) + talk_keys(t1a, t1b)[1:]),
               svg_layer(RECEIVER, opacity=0.25)] + monitor_ui(clock="9:44 PM", status="Sound detected")
        return {"background": {"type": "color", "color": "#000000"}, "layers": lay, "grade": NV_GRADE,
                "camera": {"keyframes": [{"t": 0, "zoom": 1.25, "x": "34%", "y": "55%"}, {"t": r(d), "zoom": 1.4, "x": "33%", "y": "55%", "ease": "linear"}]},
                "transitionIn": {"type": "glitch", "duration": 0.25}, "sfx": [{"cue": "static", "at": 0.0, "volume": 0.3}]}

    add("s32_lips", at("n22") - LEAD, "B9 his lips move; 'She won't open it.'", peak_build)

    def peak_image(s0, d):
        ph, sm = at("n23", "phone") - s0, at("n23", "Something") - s0
        arm = svg_layer(ARM, keyframes=[{"t": 0, "y": 1180, "opacity": 0}, {"t": r(sm - 0.05), "y": 1180, "opacity": 0},
                                        {"t": r(sm + 0.1), "y": 1140, "opacity": 1, "ease": "out"}, {"t": r(sm + 1.1), "y": 960, "opacity": 1, "ease": "inOut"}])
        rec = svg_layer(RECEIVER, keyframes=[{"t": 0, "opacity": 0.25}, {"t": r(ph), "opacity": 0.25}, {"t": r(ph + 0.25), "opacity": 1}])
        lay = [svg_layer(monitor_room("profile")), svg_layer(MOUTH_SHUT), rec, arm] + monitor_ui(clock="9:44 PM", status="Sound detected")
        return {"background": {"type": "color", "color": "#000000"}, "layers": lay, "grade": NV_GRADE,
                "camera": {"keyframes": [{"t": 0, "zoom": 1.4, "x": "33%", "y": "55%"}, {"t": r(sm), "zoom": 1.42, "x": "33%", "y": "56%"},
                                         {"t": r(sm + 1.2), "zoom": 1.3, "x": "34%", "y": "60%", "ease": "inOut"}, {"t": r(d), "zoom": 1.3, "x": "34%", "y": "60%"}]},
                "sfx": [{"cue": "heartbeat_slow", "at": r(sm + 1.0), "volume": 0.7, "hush": 3.0}], "captionY": 0.12}

    add("s33_arm", at("n23") - LEAD, "B9 peak image: the arm under the bed holds the phone (held 3.0 s)", peak_image)

    def talk(s0, d):
        tl = at("n24", "talk") - s0
        t2a, t2b = LINES["t2"]["start"] - s0, end("t2") - s0
        lay = [svg_layer(monitor_room("profile")), svg_layer(MOUTH_SHUT), svg_layer(MOUTH_OPEN, opacity=0, keyframes=talk_keys(t2a, t2b)),
               svg_layer(RECEIVER), svg_layer(ARM, y=960)] + monitor_ui(clock="9:45 PM", status="Talk", talk=tl)
        return {"background": {"type": "color", "color": "#000000"}, "layers": lay, "grade": NV_GRADE,
                "camera": {"keyframes": [{"t": 0, "zoom": 1.0, "x": "50%", "y": "55%"}, {"t": r(d), "zoom": 1.05, "x": "50%", "y": "60%"}]},
                "sfx": [{"cue": "click", "at": r(tl), "volume": 0.6}, {"cue": "static", "at": r(t2a), "volume": 0.4}]}

    add("s34_talk", at("n24") - LEAD, "B9b the monitor's talk light: 'Ivy?'", talk)

    def sleeve(s0, d):
        return {"background": {"type": "color", "color": "#0b0d12"},
                "layers": [living_bg(0.1, blur=0, opacity=1), ivy("terrified", pose="cover", light="phone", blink=False),
                           comp("horror/Darkness", {"x": 0.5, "y": 0.42, "radius": 0.3, "darkness": 0.85}, depth=0, z=20), vignette(0.55)],
                "camera": push(d, 1.05, 1.12, y="40%"), "sfx": [{"cue": "breath", "at": 0.3, "volume": 0.4}]}

    add("s35_sleeve", at("n25") - LEAD, "B9b rule four, kept as an action", sleeve)

    # B11 twist -------------------------------------------------------------------------------------
    PRIOR = OLD_THREAD + [{"me": True, "from": "Ivy", "text": "Are you outside?", "at": -30},
                          {"me": True, "from": "Ivy", "text": "What does rule 4 mean?", "at": -29}]

    def twist(s0, d):
        a1, a2 = at("n27", "What") - s0, at("n27", "I") - s0
        msgs = PRIOR + [{"from": DOYLE, "text": "What rule 4?", "at": r(a1)}, {"from": DOYLE, "text": "I wrote three rules. Chain, keys, password.", "at": r(a2)}]
        ph = doyle_thread(msgs, "9:45", typing=[{"from": DOYLE, "at": 0.15, "until": r(a1)}])
        ph["vibrate"] = [{"at": 0.1, "duration": 0.4}]
        return {"layers": [living_bg(0.15), hand_phone(ph, tremble=3), vignette(0.5)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": r(a2), "zoom": 1.04}, {"t": r(a2 + 0.2), "zoom": 1.2, "y": "60%", "ease": "out"}, {"t": r(d), "zoom": 1.22, "y": "60%"}]},
                "sfx": [{"cue": "phone_buzz", "at": 0.1, "volume": 0.8}, {"cue": "message_pop", "at": r(a1), "volume": 0.8}, {"cue": "message_pop", "at": r(a2), "volume": 0.8}]}

    add("s36_twist", at("n26") - LEAD, "B11 the real mother: 'I wrote three rules.'", twist)

    def pencil(s0, d):
        p = at("n28", "pencil") - s0
        cam = {"keyframes": [{"t": 0, "zoom": 1.05, "x": "50%", "y": "45%"}, {"t": r(p), "zoom": 1.07, "x": "50%", "y": "45%"},
                             {"t": r(d), "zoom": 1.12, "x": "50%", "y": "45%"}]}
        sc = note_scene(d, cam, extra=[svg_layer(pencil_rings(), start=r(p), enter={"type": "fade", "duration": 0.25})], counter=False)
        sc["layers"].append(comp("horror/Glitch", {"cues": [{"at": r(p), "duration": 0.25, "amount": 0.4}]}, depth=0, z=60))
        sc["sfx"] = [{"cue": "stinger", "at": r(p), "volume": 0.7}]
        sc["transitionIn"] = {"type": "glitch", "duration": 0.25}
        return sc

    add("s37_pencil", at("n28") - LEAD, "B11 the plant paid: rules 1 and 4 (and the numbers) are pencil", pencil)

    def getout(s0, d):
        a = at("n29") - s0
        msgs = PRIOR + [{"from": DOYLE, "text": "What rule 4?", "at": -2}, {"from": DOYLE, "text": "I wrote three rules. Chain, keys, password.", "at": -1.5},
                        {"from": DOYLE, "kind": "alert", "text": "Get Theo. Get out.", "at": r(a)}]
        return {"layers": [living_bg(0.15), hand_phone(doyle_thread(msgs, "9:45"), tremble=5), vignette(0.5)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.15, "y": "62%"}, {"t": r(d), "zoom": 1.2, "y": "64%"}]},
                "sfx": [{"cue": "message_pop", "at": r(a), "volume": 0.9}]}

    add("s38_getout", at("n29") - LEAD, "B11 new imperative from the real authority", getout)

    # B12 voice swap + bookend ----------------------------------------------------------------------
    def ring(s0, d):
        ex = at("n30", "Extension") - s0
        return {"layers": [living_bg(0.15), handset("INCOMING", "EXT 2 · THEO'S ROOM", clock="9:45", vibrate=[{"at": 0.05, "duration": 1.6}]), vignette(0.5)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": r(ex), "zoom": 1.04}, {"t": r(ex + 0.2), "zoom": 1.2, "y": "42%", "ease": "out"}, {"t": r(d), "zoom": 1.22, "y": "42%"}],
                           "shake": [{"at": 0.05, "duration": 0.2, "amplitude": 6}]},
                "sfx": [{"cue": "landline_ring", "at": 0.05, "volume": 0.8, "_new": True}]}

    add("s39_ring", at("n30") - LEAD, "B12 the house phone rings from Extension 2", ring)

    def ask(s0, d):
        return {"background": {"type": "color", "color": "#0b0d12"},
                "layers": [living_bg(0.1, blur=0, opacity=1), ivy("terrified", pose="ear", light="none", blink=False),
                           comp("horror/Heartbeat", {"bpm": 80, "bpmTo": 120, "intensity": 0.6}, depth=0, z=45), vignette(0.6)],
                "camera": push(d, 1.0, 1.12, y="40%"),
                "sfx": [{"cue": "breath", "at": r(SIL["q3"][0] - s0 + 0.1), "volume": 0.35, "hush": 1.2}]}

    add("s40_ask", at("n31") - LEAD, "B12 her rule five: she asks (1.2 s breath on the line)", ask)

    def black(s0, d):
        m = LINES["e1"]["start"] - s0
        return {"background": {"type": "color", "color": "#000000"},
                "layers": [comp("horror/RedText", {"text": "marmalade", "at": r(m), "duration": r(d - m), "style": "scrawl", "fontSize": 150, "shake": 3}, depth=0, z=60)],
                "sfx": []}

    add("s41_voice", at("n32") - LEAD, "B12 voice swap: it answers in my voice", black)

    def endcard(s0, d):
        hs = comp("horror/FeaturePhone", {"header": "HOME", "clock": "9:46", "sms": {"from": "EXT 2", "text": "CALLING · DOYLE MOBILE", "at": -1, "cps": 400}},
                  x=420, y=1690, width=330, height=715, rotate=78, z=10)
        cam = {"keyframes": [{"t": 0, "zoom": 1.0, "x": "50%", "y": "52%"}, {"t": r(d), "zoom": 1.03, "x": "50%", "y": "52%", "ease": "linear"}]}
        sc = note_scene(d, cam, extra=[svg_layer(highlight(5, color=RED, opacity=0.12)), hs])
        sc["sfx"] = [{"cue": "drone", "at": 0.0, "volume": 0.3}]
        return sc

    add("s42_end", SIL["q4"][0], "End card: the note (bookend); the handset dialling her mother", endcard)
    return S


# ------------------------------------------------------------------ stats
NUM_RE = r"\b(thirty-fourth|five|seven forty|seven twelve|nine|eight|one|two|three|four|twelve|twenty|thirty-one|thirty-four|nine forty)\b"


def stats():
    words = sum(len(LINES[k]["text"].split()) for k in ORDER)
    sents = []
    for k in ORDER:
        sents += [s for s in re.split(r"(?<=[.?!])\s+", LINES[k]["text"]) if s.strip()]
    lens = [len(s.split()) for s in sents]
    alltext = " ".join(LINES[k]["text"].lower() for k in ORDER)
    nums = re.findall(NUM_RE, alltext)
    speech = sum(LINES[k]["end"] - LINES[k]["start"] for k in ORDER)
    hook = ["n1", "n2", "c1"]
    return {"total_s": TOTAL, "words": words, "wpm_overall": round(words / TOTAL * 60, 1), "wpm_speech": round(words / speech * 60, 1),
            "speech_s": round(speech, 2), "sentences": len(sents), "sentence_median": statistics.median(lens),
            "punch_share": round(sum(1 for x in lens if x <= 4) / len(lens), 2),
            "spoken_numbers": len(nums), "numbers_per_min": round(len(nums) / TOTAL * 60, 1),
            "hook_words_to_contradiction": sum(len(LINES[k]["text"].split()) for k in hook[:2]) + 2,
            "contradiction_at_s": round(at("c1", "password"), 2), "contradiction_end_s": round(wend("c1", "password"), 2),
            "silences_s": round(sum(b - a for a, b in SIL.values()), 2),
            "words_first_10s": sum(1 for k in ORDER for w in LINES[k]["toks"] if norm(w["w"]) and w["s"] < 10.0)}


def mmss(x):
    return f"{int(x // 60)}:{x % 60:04.1f}"


def main():
    CUES.clear()
    S = shots()
    S.sort(key=lambda s: s[1])
    scenes = []
    new_sfx = set()
    for i, (sid, t0, beat, fn) in enumerate(S):
        t1 = S[i + 1][1] if i + 1 < len(S) else TOTAL
        d = round(t1 - t0, 3)
        body = fn(t0, d)
        sc = {"id": sid, "duration": d, "background": body.pop("background", {"type": "color", "color": "#0b0d12"})}
        sc.update(body)
        spoken = [LINES[k]["text"] for k in ORDER if t0 - 0.05 <= LINES[k]["start"] < t1 - 0.05]
        sc["notes"] = f"[{beat}] " + " ".join(spoken)
        for c in sc.pop("sfx", []):  # horror episodes bake SFX into mix.wav: cues stay global, for the mixer
            cue = {"cue": c["cue"], "at": r(t0 + c["at"]), "volume": c.get("volume", 0.8)}
            if c.get("hush"):
                cue["hush"] = c["hush"]
            if c.get("_new"):
                new_sfx.add(c["cue"])
            CUES.append(cue)
        scenes.append(sc)
    words = caption_words()
    sb = {
        "version": 1, "id": SLUG, "title": TITLE, "format": "9:16", "fps": 30,
        "scenes": scenes,
        "captions": {"words": words, "maxWords": 3, "maxChars": 18, "gapBreak": 0.3,
                     "style": {"font": "display", "fontSize": 64, "color": "#ffffff", "highlight": RED, "highlightMode": "none",
                               "strokeWidth": 10, "uppercase": False, "y": 0.13, "backing": 0.85}},
        "audio": {"voice": [{"src": f"episodes/{SLUG}/mix.wav", "start": 0, "volume": 1, "duration": TOTAL}], "music": [], "sfx": [], "duckOn": "none"},
        "overlays": {"grain": 0.5, "vignette": 0.35, "fadeIn": 0, "fadeOut": 0},
        "_built": {"by": f"backlog/horror/{SLUG}/gen_storyboard.py", "timing": "kokoro-82M cpu per-line stamps (tts_durations.json, Spark)",
                   "audio": f"studio/public/episodes/{SLUG}/mix.wav (NOT BUILT YET: Spark; voices per lines.VOICES with lines.FX, dread bed with the hush cues, SFX from _sfx_cues)"},
        "_voices": {k: {"name": L.SPEAKER_NAME[k], "kokoro": v[0], "speed": v[1], "fx": L.FX.get(k, "none (dry narrator)")} for k, v in L.VOICES.items()},
        "_sfx_cues": sorted(CUES, key=lambda c: c["at"]),
        "_sfx_new": {
            "landline_ring": "synthesize on the Spark: ffmpeg aevalsrc '0.25*(sin(2*PI*440*t)+sin(2*PI*480*t))' 2 s on / 4 s off, 2 cycles -> studio/public/sfx/landline_ring.wav (phone_buzz_long is a mobile vibrate and reads wrong for a house phone)",
            "chain_slide": "synthesize: 0.35 s of band-passed noise bursts (2-6 kHz, 12 grains, decaying) + a 1.8 kHz metallic ping at the end -> studio/public/sfx/chain_slide.wav",
        },
    }
    assert new_sfx <= set(sb["_sfx_new"]), new_sfx
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
