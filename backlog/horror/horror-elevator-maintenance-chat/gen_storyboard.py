#!/usr/bin/env python3
"""horror-elevator-maintenance-chat: timeline, pacing stats and storyboard.json from lines.py + tts_durations.json.

Inputs (this folder):
  lines.py             every spoken line (speaker, text, on-screen text, gap) and timed silences
  tts_durations.json   Kokoro-82M per-line durations + word stamps, measured on the Spark CPU (tts_measure.py)

usage: python3 gen_storyboard.py            writes storyboard.json + timing.json + script_timed.md, prints stats
       python3 gen_storyboard.py --stats    prints only

Every shot starts LEAD s before its anchor word; every bubble, press, tap and expression swap is anchored to the word
that names it (no hand-typed episode seconds). The horror kit is locked (BRIEF 11:27), so the car interior, the
landing wall, the dome camera, the intercom grille, the inspection card, the counter dashes and the contact cards
are inline SVG layers drawn here; kit components are used only with props that exist today.
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
SLUG = "horror-elevator-maintenance-chat"
TITLE = "The Elevator Stopped and Maintenance Texted First (Part 1)"


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
    toks = [{"w": w["w"], "s": t + max(0.0, w["s"]), "e": t + min(m["dur"], max(0.0, w["e"]))} for w in m["words"]]
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
CAP = {  # (line, token, nth) -> caption text
    ("n1", "one", 0): "1",
    ("m4", "two", 0): "2,", ("m4", "eleven", 0): "11,", ("m4", "five", 0): "5.",
    ("n8", "two", 0): "2.", ("n9", "eleven", 0): "11.", ("n10", "five", 0): "5.",
    ("me1", "two", 0): "2.", ("o2", "two's", 0): "2's",
    ("me2", "Two", 0): "2,", ("me2", "eleven", 0): "11,", ("me2", "five", 0): "5",
    ("o5", "two", 0): "2.", ("v1", "two", 0): "2?", ("v2", "two", 0): "2.", ("nv1", "Omar", 0): "Omar,",
    ("n21", "Omar", 1): "OMAR.", ("v3", "are", 0): "are—",
}
EMPH = {("n2", "texted"), ("m1", "mirror"), ("n3", "Maintenance"), ("n5", "off"), ("m6", "alarm"), ("m7", "number"),
        ("n6", "nine"), ("n10", "Once"), ("o2", "dead"), ("o3", "talking"), ("o5", "code"), ("n13", "key"),
        ("n15", "delivered"), ("n16", "gone"), ("n17", "through"), ("v3", "Lights"), ("n20", "face"), ("m11", "look"), ("n23", "pressed"),
        ("v3", "Nobody's"), ("v3", "inside"), ("m12", "that"), ("n25", "dashes"), ("n27", "number"), ("n28", "Twice"),
        ("x1", "Nora"), ("n30", "name")}
PAGE = 4  # words per caption page at most (maxChars 18 usually breaks earlier)


def caption_words() -> list[dict]:
    out = []
    for lid in ORDER:
        line_words, seen = [], {}
        for k in LINES[lid]["toks"]:
            raw = k["w"]
            if not norm(raw):  # punctuation token: glue to previous word
                if line_words and line_words[-1]["text"][-1:] not in ".,?!—":
                    line_words[-1]["text"] += raw
                continue
            nth = seen.get(raw, 0)
            seen[raw] = nth + 1
            txt = CAP.get((lid, raw, nth), raw)
            w = {"text": txt, "start": round(k["s"], 3), "end": round(max(k["e"], k["s"] + 0.08), 3)}
            if (lid, raw) in EMPH:
                w["emph"] = True
            line_words.append(w)
        if line_words:
            line_words[0]["br"] = True
        out += line_words
    n = 0
    for i, w in enumerate(out):
        if w.get("br"):
            n = 0
        elif n >= PAGE or (i and out[i - 1]["text"][-1:] in ".?!,—"):
            w["br"] = True
            n = 0
        n += 1
    return out


# ------------------------------------------------------------------ kit helpers
MAINT = "Maintenance"
OMAR = "+1 555 0142"
MEMBERS = {MAINT: {"color": "#5b6470", "initials": "M"}, OMAR: {"color": "#7a6a4a", "initials": "#"}}
ACCENT = "#3d5a80"
DARK_SKIN = {"skin": "#6b5d52", "nail": "#7a6c60"}


def comp(name, props=None, **kw):
    d = {"type": "component", "name": name, "props": props or {}}
    d.update(kw)
    return d


def svg_layer(markup, **kw):
    d = {"type": "svg", "markup": markup, "x": "50%", "y": "50%", "width": 1080, "height": 1920}
    d.update(kw)
    return d


def rect(x, y, w, h, fill, **kw):
    d = {"type": "rect", "x": x, "y": y, "width": w, "height": h, "fill": fill}
    d.update(kw)
    return d


def vignette(amount=0.45, **kw):
    return comp("horror/Vignette", {"amount": amount, **kw}, depth=0, z=50)


def darkness(dark, x=0.5, y=0.6, radius=0.6, **kw):
    kw.setdefault("z", 40)
    return comp("horror/Darkness", {"x": x, "y": y, "radius": radius, "darkness": dark}, depth=0, **kw)


def push(d, z0=1.0, z1=1.05, x="50%", y="50%"):
    return {"keyframes": [{"t": 0, "zoom": z0, "x": x, "y": y, "ease": "linear"}, {"t": round(d, 3), "zoom": z1, "x": x, "y": y, "ease": "linear"}]}


def protagonist(expr="worried", pose="phone", light="phone", w=900, x="50%", y="100%", **kw):
    p = {"expr": expr, "pose": pose, "light": light}
    o = {k: kw.pop(k) for k in ("opacity", "blur", "z", "depth", "start", "enter", "flipX") if k in kw}
    p.update(kw)
    return comp("horror/Protagonist", p, x=x, y=y, anchorY=1, width=w, height=round(w * 760 / 500), **o)


# ------------------------------------------------------------------ inline SVG sets (kit gaps, drawn here)
def car_a(mirror_face_glint=False):
    """Backdrop A, facing Nora: mirror back wall (glare only, never a reflection), brushed-steel side walls,
    ceiling light panel, handrail across the mirror, floor."""
    glint = ('<ellipse cx="1000" cy="640" rx="38" ry="52" fill="#e9eef2" opacity="0.32"/>'
             '<ellipse cx="1000" cy="640" rx="70" ry="95" fill="#e9eef2" opacity="0.10"/>') if mirror_face_glint else ""
    lines_ = "".join(f'<line x1="{x}" y1="260" x2="{x}" y2="1520" stroke="#ffffff" stroke-opacity="0.05" stroke-width="2"/>' for x in range(14, 190, 22))
    lines_r = "".join(f'<line x1="{x}" y1="260" x2="{x}" y2="1520" stroke="#ffffff" stroke-opacity="0.05" stroke-width="2"/>' for x in range(900, 1080, 22))
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920">'
        '<defs><linearGradient id="caS" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3b4047"/><stop offset="0.5" stop-color="#626a73"/><stop offset="1" stop-color="#3b4047"/></linearGradient>'
        '<linearGradient id="caM" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9aa3ab"/><stop offset="0.55" stop-color="#7c858e"/><stop offset="1" stop-color="#5f6770"/></linearGradient></defs>'
        '<rect width="1080" height="1920" fill="#23272d"/>'
        '<rect x="0" y="260" width="190" height="1260" fill="url(#caS)"/>' + lines_ +
        '<rect x="890" y="260" width="190" height="1260" fill="url(#caS)"/>' + lines_r +
        '<rect x="190" y="260" width="700" height="1260" fill="#454b52" stroke="#0e1013" stroke-width="8"/>'
        '<rect x="226" y="296" width="628" height="1188" fill="url(#caM)"/>'
        '<polygon points="300,296 470,296 226,800 226,560" fill="#ffffff" opacity="0.16"/>'
        '<polygon points="560,296 610,296 300,1484 250,1484" fill="#ffffff" opacity="0.07"/>'
        '<rect x="0" y="0" width="1080" height="260" fill="#1b1e22"/>'
        '<rect x="290" y="80" width="500" height="110" rx="10" fill="#f1ede2" opacity="0.85"/>'
        '<rect x="290" y="80" width="500" height="110" rx="10" fill="none" stroke="#0e1013" stroke-width="6"/>'
        '<rect x="0" y="1150" width="1080" height="36" rx="18" fill="#8a929c" stroke="#0e1013" stroke-width="6"/>'
        '<rect x="0" y="1520" width="1080" height="400" fill="#2b2723"/>'
        '<rect x="0" y="1520" width="1080" height="14" fill="#15130f"/>' + glint +
        "</svg>"
    )


def mirror_strip():
    """Cover-frame plant: the edge of the mirror at the right of frame 0, with a pale face-height highlight that
    faces the camera (pays off at the B9 image)."""
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920">'
        '<defs><linearGradient id="msG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8a939c" stop-opacity="0"/><stop offset="0.35" stop-color="#8a939c" stop-opacity="0.55"/><stop offset="1" stop-color="#b6bec6" stop-opacity="0.7"/></linearGradient></defs>'
        '<rect x="930" y="0" width="150" height="1920" fill="url(#msG)"/>'
        '<ellipse cx="1012" cy="760" rx="40" ry="56" fill="#eef2f5" opacity="0.38"/>'
        '<ellipse cx="999" cy="745" rx="6" ry="4" fill="#20242a" opacity="0.5"/><ellipse cx="1025" cy="745" rx="6" ry="4" fill="#20242a" opacity="0.5"/>'
        "</svg>"
    )


def door_panel(side: str):
    """Backdrop B pieces: one steel door leaf (left or right half), brushed, in a 1080x1920 frame."""
    x0 = 150 if side == "L" else 540
    lines_ = "".join(f'<line x1="{x}" y1="130" x2="{x}" y2="1790" stroke="#ffffff" stroke-opacity="0.05" stroke-width="2"/>' for x in range(x0 + 12, x0 + 390, 18))
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920">'
        f'<defs><linearGradient id="dp{side}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5a616a"/><stop offset="0.5" stop-color="#737b84"/><stop offset="1" stop-color="#4c5259"/></linearGradient></defs>'
        f'<rect x="{x0}" y="130" width="390" height="1660" fill="url(#dp{side})" stroke="#0e1013" stroke-width="6"/>' + lines_ +
        "</svg>"
    )


DOOR_FRAME = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920">'
    '<rect x="0" y="0" width="1080" height="130" fill="#2a2e34"/><rect x="0" y="1790" width="1080" height="130" fill="#26231f"/>'
    '<rect x="0" y="0" width="150" height="1920" fill="#30343a"/><rect x="930" y="0" width="150" height="1920" fill="#30343a"/>'
    '<rect x="150" y="130" width="780" height="1660" fill="none" stroke="#0e1013" stroke-width="10"/>'
    '<rect x="150" y="1770" width="780" height="20" fill="#8a8f96"/>'
    "</svg>"
)


def landing(number: bool, warm: bool):
    """Flat landing wall facing the open doors: my floor's painted red nine (warm, plant) or bare (cold, payoff)."""
    wall, base, carpet = ("#b9a58a", "#6e5d4a", "#5a3b33") if warm else ("#59626b", "#353b42", "#2b2e33")
    num = ('<text x="540" y="1240" text-anchor="middle" font-family="Anton, Impact, sans-serif" font-size="760" fill="#b3262b" opacity="0.92">9</text>'
           if number else "")
    light = "#fff3d6" if warm else "#cfe3ff"
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920">'
        f'<rect width="1080" height="1920" fill="{wall}"/>'
        f'<rect x="0" y="0" width="1080" height="180" fill="{base}"/>'
        f'<rect x="340" y="40" width="400" height="60" rx="8" fill="{light}" opacity="{0.9 if warm else 0.55}"/>'
        f'<rect x="0" y="1500" width="1080" height="40" fill="{base}"/>'
        f'<rect x="0" y="1540" width="1080" height="380" fill="{carpet}"/>' + num +
        "</svg>"
    )


CEILING_CAM = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920">'
    '<rect width="1080" height="1920" fill="#1b1e22"/>'
    + "".join(f'<rect x="{x}" y="{y}" width="300" height="300" fill="none" stroke="#2c3036" stroke-width="6"/>' for x in (-60, 260, 580, 900) for y in (100, 420, 740, 1060, 1380))
    + '<rect x="120" y="1320" width="840" height="200" rx="12" fill="#e9e4d8" opacity="0.55"/>'
    '<circle cx="640" cy="760" r="210" fill="#8a929c" stroke="#0b0b0e" stroke-width="10"/>'
    '<circle cx="640" cy="760" r="170" fill="#15171a" stroke="#0b0b0e" stroke-width="8"/>'
    '<ellipse cx="585" cy="700" rx="70" ry="40" fill="#ffffff" opacity="0.12" transform="rotate(-30 585 700)"/>'
    '<circle cx="640" cy="790" r="44" fill="#050608"/><circle cx="628" cy="778" r="10" fill="#ffffff" opacity="0.25"/>'
    '<circle cx="760" cy="640" r="16" fill="#3a0d10" stroke="#0b0b0e" stroke-width="4"/>'
    "</svg>"
)

INTERCOM = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920">'
    '<defs><linearGradient id="icG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7a828c"/><stop offset="1" stop-color="#4a5058"/></linearGradient></defs>'
    '<rect width="1080" height="1920" fill="#2a2e34"/>'
    '<rect x="140" y="420" width="800" height="1080" rx="22" fill="url(#icG)" stroke="#0b0b0e" stroke-width="8"/>'
    + "".join(f'<rect x="250" y="{y}" width="580" height="22" rx="11" fill="#14161a"/>' for y in range(560, 1180, 56))
    + '<text x="540" y="1300" text-anchor="middle" font-family="Montserrat, sans-serif" font-weight="900" font-size="54" fill="#1d2025" letter-spacing="6">EMERGENCY PHONE</text>'
    '<circle cx="540" cy="1400" r="16" fill="#3dd17a"/>'
    "</svg>"
)

BELL = (  # alarm / phone glyph over the panel's '!' button (720, 1560), plus its label
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920">'
    '<g transform="translate(720 1556)"><path d="M -22 14 Q -22 -24 0 -26 Q 22 -24 22 14 L 28 20 L -28 20 Z" fill="#3c4148"/>'
    '<circle cx="0" cy="26" r="7" fill="#3c4148"/></g>'
    '<text x="720" y="1650" text-anchor="middle" font-family="Montserrat, sans-serif" font-weight="900" font-size="26" fill="#1d2025">ALARM / PHONE</text>'
    "</svg>"
)

CARD = (  # inspection card under the floor buttons (plant for the after-hours number)
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920">'
    '<rect x="330" y="1372" width="420" height="120" rx="8" fill="#ece6d4" stroke="#0b0b0e" stroke-width="5"/>'
    '<text x="540" y="1404" text-anchor="middle" font-family="Montserrat, sans-serif" font-weight="900" font-size="20" fill="#1b1d22" letter-spacing="2">CERTIFICATE OF INSPECTION · CAR 2</text>'
    '<text x="540" y="1440" text-anchor="middle" font-family="Montserrat, sans-serif" font-weight="800" font-size="19" fill="#4a4d55">AFTER-HOURS SERVICE</text>'
    '<text x="540" y="1474" text-anchor="middle" font-family="Montserrat, sans-serif" font-weight="900" font-size="28" fill="#a3242a">+1 555 0142</text>'
    "</svg>"
)


def dashes(arrow_mask=True):
    """Counter fix (kit gap): an opaque plate over the panel's red digits with two red dashes (between floors).
    arrow_mask False leaves the kit's arrow visible (it blinks while the car moves)."""
    x0 = 300 if arrow_mask else 500
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920">'
        f'<rect x="{x0 + 4}" y="264" width="{776 - x0 - 4}" height="242" rx="10" fill="#0b0909"/>'
        '<text x="575" y="455" text-anchor="middle" font-family="Anton, Impact, sans-serif" font-size="210" fill="#1e0709">8</text>'
        '<text x="700" y="455" text-anchor="middle" font-family="Anton, Impact, sans-serif" font-size="210" fill="#1e0709">8</text>'
        '<rect x="535" y="362" width="80" height="26" rx="4" fill="#ff3b30" style="filter: drop-shadow(0 0 12px rgba(255,50,40,0.85))"/>'
        '<rect x="660" y="362" width="80" height="26" rx="4" fill="#ff3b30" style="filter: drop-shadow(0 0 12px rgba(255,50,40,0.85))"/>'
        + ('<path d="M 390 310 L 445 400 L 335 400 Z" fill="#3a0d10"/>' if arrow_mask else "")
        + "</svg>"
    )


def split_cards():
    """The verdict split: two contact cards (readable at phone size, no tiny bubbles)."""
    def card(x, title, sub, line, accent, hi):
        return (f'<g transform="translate({x} 560)"><rect width="480" height="800" rx="40" fill="#161a20" stroke="#2c323c" stroke-width="6"/>'
                f'<circle cx="240" cy="170" r="92" fill="{accent}"/><text x="240" y="200" text-anchor="middle" font-family="Montserrat, sans-serif" font-weight="900" font-size="80" fill="#eef0f3">{title[0]}</text>'
                f'<text x="240" y="340" text-anchor="middle" font-family="Montserrat, sans-serif" font-weight="900" font-size="44" fill="#eef0f3">{title}</text>'
                f'<text x="240" y="390" text-anchor="middle" font-family="Montserrat, sans-serif" font-weight="700" font-size="26" fill="#8a93a2">{sub}</text>'
                f'<rect x="36" y="460" width="408" height="250" rx="28" fill="#262c36"/>'
                f'<text x="66" y="540" font-family="Montserrat, sans-serif" font-weight="700" font-size="34" fill="#e7e9ee">{line[0]}</text>'
                f'<text x="66" y="600" font-family="Montserrat, sans-serif" font-weight="900" font-size="46" fill="#ff4b55">{hi}</text>'
                f'<text x="66" y="660" font-family="Montserrat, sans-serif" font-weight="700" font-size="34" fill="#e7e9ee">{line[1]}</text></g>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920"><rect width="1080" height="1920" fill="#0b0d12"/>'
            + card(40, "Maintenance", "mobile", ("Stay calm,", "Don't look."), "#5b6470", "Nora.")
            + card(560, "+1 555 0142", "Not in your contacts", ("Coming up with", "Five minutes."), "#7a6a4a", "the door key.")
            + '<rect x="538" y="520" width="4" height="880" fill="#ff4b55" opacity="0.6"/></svg>')


# ------------------------------------------------------------------ composed stacks
def panel(pressed=(), frm=6, to=6, at0=999.0, per=0.45, flicker=0.12, arrow_mask=True, blur=None, opacity=1.0, card=True, bell=False):
    kw = {}
    if blur:
        kw["blur"] = blur
    if opacity < 1:
        kw["opacity"] = opacity
    out = [comp("horror/ElevatorPanel", {"from": frm, "to": to, "at": at0, "perFloor": per, "floors": 12, "target": 0, "flicker": flicker,
                                         "pressed": [{"at": round(a, 3), "floor": f} for a, f in pressed]}, **kw),
           svg_layer(dashes(arrow_mask), **kw)]
    if card:
        out.append(svg_layer(CARD, **kw))
    if bell:
        out.append(svg_layer(BELL, **kw))
    return out


def car_bg(dark=0.35, blur=None, glint=False, opacity=1.0):
    kw = {"blur": blur} if blur else {}
    if opacity < 1:
        kw["opacity"] = opacity
    return [svg_layer(car_a(glint), **kw)] + ([darkness(dark, y=0.45, radius=0.7)] if dark else [])


def hand_phone(phone, tremble=1.5, cy=0.585, dark=False, **extra):
    p = {"phoneWidth": 0.68, "cx": 0.5, "cy": cy, "tilt": -2, "tremble": tremble, "side": "right", "phone": phone}
    if dark:
        p.update(DARK_SKIN)
    p.update(extra)
    return comp("horror/HandPhone", p)


def phone_scene(phone, dark=0.35, tremble=1.5, blackout=False, **hp):
    if blackout:  # after the lights die: no car behind the phone, only the phone's own spill
        bg = [rect("50%", "50%", 1080, 1920, "#040405"), darkness(0.95, y=0.62, radius=0.42, z=0)]
    else:
        bg = [svg_layer(car_a(), blur=10, opacity=0.75), darkness(dark, y=0.45, radius=0.7, z=0)]  # z 0: the light falls on the car, not on the phone
    return bg + [hand_phone(phone, tremble=tremble, dark=blackout, **hp), vignette(0.5 if not blackout else 0.65)]


def chat(title, messages, clock, **kw):
    c = {"title": title, "dm": title, "messages": messages, "clock": clock, "battery": 31, "theme": "dark", "scale": 1.25, "accent": ACCENT}
    c.update(kw)
    return c


def m_thread(messages, clock, **kw):
    return chat(MAINT, messages, clock, subtitle="mobile", **kw)


def o_thread(messages, clock, **kw):
    return chat(OMAR, messages, clock, subtitle="Not in your contacts", **kw)


def punch(d, hits, z0=1.0, step=0.06, y_last="58%"):
    """Camera punch-ins on the newest bubble: a small zoom step at each hit (scene seconds)."""
    kf = [{"t": 0, "zoom": z0, "x": "50%", "y": "50%"}]
    z = z0
    for h in sorted(hits):
        if h <= 0.05 or h >= d - 0.05:
            continue
        kf.append({"t": round(h, 3), "zoom": round(z, 3), "x": "50%", "y": "50%" if z < 1.1 else y_last})
        z += step
        kf.append({"t": round(min(d, h + 0.18), 3), "zoom": round(z, 3), "x": "50%", "y": "50%" if z < 1.1 else y_last, "ease": "out"})
    kf.append({"t": round(d, 3), "zoom": round(z + 0.01, 3), "x": kf[-1]["x"], "y": kf[-1]["y"], "ease": "linear"})
    return {"keyframes": kf}


# message history (scene-relative times are filled per scene; negatives = already on screen)
def hist(items, base=-30.0):
    return [dict(m, at=base + 0.1 * i) for i, m in enumerate(items)]


M_EARLY = [{"from": MAINT, "text": "Stay calm, Nora. Don't look at the mirror."}, {"from": MAINT, "text": "Car 2 is jammed. I can get you moving."},
           {"me": True, "text": "how do you know my name?"}, {"from": MAINT, "text": "I'm watching you on the camera. You're doing fine."}]
M_RULES = [{"from": MAINT, "text": "One. Press 2, then 11, then 5."}, {"from": MAINT, "text": "Two. Hold Close until the lights dim."},
           {"from": MAINT, "text": "Three. Never press the alarm. It resets the car."}, {"from": MAINT, "text": "Four. Don't step out until you see your number."},
           {"from": MAINT, "text": "Don't look. Hold Close."}]
O_1 = [{"me": True, "text": "stuck in car 2. maintenance is watching me on the camera"}, {"from": OMAR, "text": "This is Omar. I'm the only maintenance on call tonight."},
       {"from": OMAR, "text": "What did they tell you to press?"}, {"me": True, "text": "2 11 5"}]
O_2 = [{"from": OMAR, "text": "That's the reset code for car 2. Only my office has it."}, {"from": OMAR, "text": "And car 2's camera has been dead since Tuesday."},
       {"from": OMAR, "text": "Who are you talking to?"}]
O_KEY = {"from": OMAR, "text": "Don't press anything. I'm coming up with the door key. Five minutes."}
O_DELETED = {"kind": "system", "text": "This message was deleted"}
ND = {"kind": "system", "text": "(!) Not delivered"}
CUES: list[dict] = []


def shots():
    """(scene id, global start, beat tag, builder(scene_start, duration) -> scene dict fields)."""
    S = []

    def add(sid, t0, beat, fn):
        S.append((sid, round(t0, 3), beat, fn))

    # B1 cover + hook ----------------------------------------------------------------------
    def cover(s0, d):
        notes = [{"at": -1, "app": "Messages", "title": MAINT, "text": "Stay calm, Nora. Don't look at the mirror."}]
        phone = {"members": MEMBERS, "mode": "lock", "lock": {"time": "1:04", "date": "Saturday, November 14", "notifications": notes, "battery": 31}}
        return {"background": {"type": "color", "color": "#0b0d12"},
                "layers": panel(blur=10, opacity=0.7, card=False) + [svg_layer(mirror_strip()), darkness(0.3, y=0.4, radius=0.8),
                          hand_phone(phone, tremble=1.0), vignette(0.5)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.0, "x": "50%", "y": "48%"}, {"t": round(at("n1", "stopped") - s0, 2), "zoom": 1.01, "x": "50%", "y": "48%"},
                                         {"t": round(at("n1", "stopped") - s0 + 0.15, 2), "zoom": 1.05, "x": "50%", "y": "48%", "ease": "out"},
                                         {"t": round(at("n2", "texted") - s0, 2), "zoom": 1.06, "x": "50%", "y": "48%"},
                                         {"t": round(at("n2", "texted") - s0 + 0.15, 2), "zoom": 1.1, "x": "50%", "y": "46%", "ease": "out"},
                                         {"t": round(d, 3), "zoom": 1.11, "x": "50%", "y": "46%"}]}, "captionY": 0.12,
                "sfx": [{"cue": "relay_click", "at": 0.12, "volume": 0.9}, {"cue": "impact", "at": round(at("n1", "stopped") - s0, 2), "volume": 0.5},
                        {"cue": "notify", "at": round(at("n2", "texted") - s0, 2), "volume": 0.7}]}

    add("s01_cover", 0.0, "B1 hook (cover, lock screen 1:04)", cover)

    def banner(s0, d):
        sc = cover(s0, d)
        sc["camera"] = {"keyframes": [{"t": 0, "zoom": 1.05, "x": "50%", "y": "48%"}, {"t": 0.25, "zoom": 1.32, "x": "50%", "y": "40%", "ease": "out"},
                                      {"t": round(d, 3), "zoom": 1.36, "x": "50%", "y": "40%", "ease": "linear"}]}
        sc["sfx"] = [{"cue": "phone_buzz", "at": 0.05, "volume": 0.5}]
        return sc

    add("s02_banner", at("m1") - LEAD, "B1 the rule arrives before anyone asked", banner)

    def nora_doubt(s0, d):
        mt = at("n3", "Maintenance") - s0
        return {"layers": car_bg(0.3) + [protagonist("worried", lookX=0.1, lookY=0.4, exprs=[{"t": 0, "e": "worried"}, {"t": round(mt, 2), "e": "suspicious"}]), vignette(0.45)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.0, "y": "50%"}, {"t": round(mt, 2), "zoom": 1.03, "y": "50%"}, {"t": round(mt + 0.15, 2), "zoom": 1.14, "y": "44%", "ease": "out"},
                                         {"t": round(d, 3), "zoom": 1.15, "y": "44%"}]}}

    add("s03_doubt", at("n3") - LEAD, "B1 contradiction: I never saved that contact (master question)", nora_doubt)

    # B2 decoy + viewer proxy ------------------------------------------------------------
    def thread1(s0, d):
        a2, a_me, a3 = at("m2") - s0, at("n4", "name") - s0, at("m3") - s0
        msgs = [dict(M_EARLY[0], at=-5), dict(M_EARLY[1], at=round(a2, 3)), dict(M_EARLY[2], at=round(a_me, 3)), dict(M_EARLY[3], at=round(a3, 3))]
        ty = at("n4", "typed") - s0
        phone = {"members": MEMBERS, "mode": "chat", "chat": m_thread(msgs, "1:04", draft="Message",
                                                                       typing=[{"from": MAINT, "at": round(a_me + 0.25, 2), "until": round(a3, 2)}])}
        taps = [{"at": round(ty + 0.12 * i, 2), "x": 0.25 + 0.09 * (i % 6), "y": 0.9} for i in range(7)]
        return {"layers": phone_scene(phone, 0.35, tremble=2, taps=taps), "camera": punch(d, [a2, a_me, a3]),
                "sfx": [{"cue": "message_pop", "at": round(a2, 2), "volume": 0.7}, {"cue": "typing", "at": round(ty, 2), "volume": 0.5},
                        {"cue": "message_send", "at": round(a_me, 2), "volume": 0.6}, {"cue": "message_pop", "at": round(a3, 2), "volume": 0.7}]}

    add("s04_thread", at("m2") - 0.3, "B2 decoy + viewer proxy (how do you know my name?)", thread1)

    def camera_off(s0, d):
        off = at("n5", "off") - s0
        return {"background": {"type": "color", "color": "#1b1e22"},
                "layers": [svg_layer(CEILING_CAM), darkness(0.45, x=0.6, y=0.4, radius=0.5), vignette(0.5)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.0, "x": "56%", "y": "40%"}, {"t": round(off, 2), "zoom": 1.25, "x": "64%", "y": "36%", "ease": "inOut"},
                                         {"t": round(d, 3), "zoom": 1.6, "x": "70%", "y": "33.5%", "ease": "out"}]},
                "sfx": [{"cue": "click", "at": round(off, 2), "volume": 0.3}]}

    add("s05_camera", at("n5") - LEAD, "B2 proxy answered with a lie: the camera light is off", camera_off)

    # B2 rules + plants ------------------------------------------------------------------
    def rules(s0, d):
        one, two, three, four = (at("m4", "One") - s0, at("m5", "Two") - s0, at("m6", "Three") - s0, at("m7", "Four") - s0)
        cards = [("2 → 11 → 5", one, two - one), ("HOLD CLOSE", two, three - two), ("NEVER: ALARM", three, four - three), ("WAIT FOR YOUR NUMBER", four, d - four)]
        texts = [comp("horror/RedText", {"text": tx, "at": round(a, 2), "duration": round(du - 0.1, 2), "style": "neon", "fontSize": 124 if len(tx) < 14 else 84},
                      depth=0, z=60, x="50%", y="34%", width=1080, height=320) for tx, a, du in cards]
        glint = at("m6", "alarm") - s0
        kf = [{"t": 0, "zoom": 1.35, "x": 540, "y": 900}, {"t": round(two, 2), "zoom": 1.35, "x": 540, "y": 1000},
              {"t": round(two + 0.35, 2), "zoom": 2.2, "x": 540, "y": 1480, "ease": "inOut"}, {"t": round(three, 2), "zoom": 2.2, "x": 560, "y": 1480},
              {"t": round(three + 0.35, 2), "zoom": 2.4, "x": 700, "y": 1500, "ease": "inOut"}, {"t": round(four, 2), "zoom": 2.4, "x": 700, "y": 1500},
              {"t": round(four + 0.35, 2), "zoom": 2.0, "x": 560, "y": 400, "ease": "inOut"}, {"t": round(d, 3), "zoom": 2.05, "x": 560, "y": 400}]
        glow = {"type": "circle", "x": 720, "y": 1560, "width": 110, "height": 110, "fill": "#fff1b0", "opacity": 0.0,
                "keyframes": [{"t": round(glint, 2), "opacity": 0}, {"t": round(glint + 0.12, 2), "opacity": 0.7}, {"t": round(glint + 0.5, 2), "opacity": 0}]}
        return {"background": {"type": "color", "color": "#2a2e34"},
                "layers": panel(bell=True) + [glow, vignette(0.4)] + texts, "camera": {"keyframes": kf}, "captionY": 0.12,
                "sfx": [{"cue": "message_pop", "at": round(a, 2), "volume": 0.6} for _, a, _ in cards] + [{"cue": "tick", "at": round(glint, 2), "volume": 0.5}]}

    add("s06_rules", at("m4") - LEAD, "B2 four numbered rules (cards) + the inspection card in view", rules)

    def nine(s0, d):
        return {"layers": [svg_layer(landing(True, True)), vignette(0.35)], "camera": push(d, 1.0, 1.08, y="55%"),
                "transitionIn": {"type": "dipBlack", "duration": 0.2}, "sfx": [{"cue": "ding", "at": 0.3, "volume": 0.3}]}

    add("s07_nine", at("n6") - LEAD, "B2 plant: my landing, the red nine (warm memory)", nine)

    def mirror_wall(s0, d):
        return {"layers": car_bg(0.35, blur=3) + [protagonist("worried", lookY=0.35, lookX=0.0), vignette(0.45)],
                "camera": {"preset": "drift", "amount": 0.6}}

    add("s08_mirror", at("n7") - LEAD, "B2 plant: the mirror (glare only) behind me, eyes on the doors", mirror_wall)

    # B5 ladder ----------------------------------------------------------------------------
    def press2(s0, d):
        p, drop = at("n8", "two") - s0, at("n8", "dropped") - s0
        return {"background": {"type": "color", "color": "#2a2e34"},
                "layers": panel(pressed=[(p, 2)]) + [comp("horror/Flicker", {"strength": 0.1, "blackouts": [{"at": round(drop, 2), "duration": 0.15}]}, depth=0, z=45), vignette(0.4)],
                "camera": {"keyframes": [{"t": 0, "zoom": 2.0, "x": 420, "y": 1250}, {"t": round(d, 3), "zoom": 2.1, "x": 420, "y": 1250}],
                           "shake": [{"at": round(drop, 2), "duration": 0.5, "amplitude": 26}]},
                "sfx": [{"cue": "click", "at": round(p, 2), "volume": 0.8}, {"cue": "impact", "at": round(drop, 2), "volume": 0.9}]}

    add("s09_press2", at("n8") - LEAD, "B5 rung 1: press 2, the car drops a foot", press2)

    def press11(s0, d):
        p = at("n9", "eleven") - s0
        return {"background": {"type": "color", "color": "#2a2e34"},
                "layers": panel(pressed=[(-5, 2), (p, 11)]) + [vignette(0.4)],
                "camera": {"keyframes": [{"t": 0, "zoom": 2.0, "x": 420, "y": 760}, {"t": round(d, 3), "zoom": 2.1, "x": 420, "y": 760}]},
                "sfx": [{"cue": "click", "at": round(p, 2), "volume": 0.8}]}

    add("s10a_press11", at("n9") - LEAD, "B5 rung 2a: press 11", press11)

    def roof(s0, d):
        sh = at("n9", "shifted") - s0
        bulge = rect(200, 135, 520, 170, "#000000", opacity=0.0, blur=24,
                     keyframes=[{"t": 0, "x": 160, "opacity": 0}, {"t": round(sh, 2), "x": 260, "opacity": 0.8}, {"t": round(d, 3), "x": 860, "opacity": 0.85, "ease": "inOut"}])
        return {"layers": car_bg(0.4) + [bulge, protagonist("worried", lookY=-0.85, exprs=[{"t": 0, "e": "worried"}, {"t": round(sh, 2), "e": "scared"}], w=820), vignette(0.5)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.0, "y": "50%"}, {"t": round(sh, 2), "zoom": 1.0, "y": "48%"}, {"t": round(d, 3), "zoom": 1.06, "y": "40%", "ease": "inOut"}],
                           "shake": [{"at": round(sh, 2), "duration": 0.6, "amplitude": 6}]},
                "sfx": [{"cue": "underwater_rumble", "at": round(sh - 0.1, 2), "volume": 0.6}]}

    add("s10b_roof", at("n9", "Something") - LEAD, "B5 rung 2b: something settles on the roof", roof)

    def press5(s0, d):
        p = at("n10", "five") - s0
        return {"background": {"type": "color", "color": "#2a2e34"},
                "layers": panel(pressed=[(-5, 2), (-5, 11), (p, 5)]) + [vignette(0.4)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.7, "x": 540, "y": 1000}, {"t": round(d, 3), "zoom": 1.8, "x": 540, "y": 1000}]},
                "sfx": [{"cue": "click", "at": round(p, 2), "volume": 0.8}]}

    add("s11a_press5", at("n10") - LEAD, "B5 rung 3a: press 5 (all three lit)", press5)

    def tap1(s0, d):
        tp = at("n10", "tapped") - s0
        return {"layers": car_bg(0.45) + [protagonist("scared", lookX=-1, lookY=0.1, blink=False, exprs=[{"t": 0, "e": "scared"}, {"t": round(tp, 2), "e": "terrified"}]), vignette(0.5)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.1, "y": "46%"}, {"t": round(d, 3), "zoom": 1.22, "y": "42%", "ease": "linear"}],
                           "shake": [{"at": round(tp, 2), "duration": 0.12, "amplitude": 8}]},
                "sfx": [{"cue": "knock", "at": round(tp, 2), "volume": 0.5}, {"cue": "message_pop", "at": round(at("m8") - s0, 2), "volume": 0.5}]}

    add("s11b_tap", at("n10", "Behind") - LEAD, "B5 rung 3b: one tap on the mirror; 'Don't look. Hold Close.'", tap1)

    def hold_close(s0, d):
        dm = at("n11", "dimmed") - s0
        steps = [rect("50%", "50%", 1080, 1920, "#000000", opacity=0.22, depth=0, z=44, start=round(dm + 0.3 * i, 2)) for i in range(3)]
        glow = {"type": "circle", "x": 540, "y": 1560, "width": 92, "height": 92, "fill": "#ffb35c", "opacity": 0.95, "shadow": "0 0 18px rgba(255,150,40,0.9)"}
        return {"background": {"type": "color", "color": "#2a2e34"},
                "layers": panel(pressed=[(-5, 2), (-5, 11), (-5, 5)]) + [glow, vignette(0.45)] + steps,
                "camera": {"keyframes": [{"t": 0, "zoom": 2.4, "x": 540, "y": 1500}, {"t": round(d, 3), "zoom": 2.6, "x": 540, "y": 1520}]},
                "sfx": [{"cue": "relay_click", "at": round(dm + 0.3 * i, 2), "volume": 0.4} for i in range(3)]}

    add("s12_close", at("n11") - LEAD, "B5: I hold Close; the light steps down three times (rule two kept)", hold_close)

    # B8 midpoint: Nora texts the real authority -----------------------------------------
    def card_insert(s0, d):
        tx = at("n12", "texted") - s0
        steps = [rect("50%", "50%", 1080, 1920, "#000000", opacity=0.45, depth=0, z=44)]
        return {"background": {"type": "color", "color": "#2a2e34"},
                "layers": panel(pressed=[(-5, 2), (-5, 11), (-5, 5)]) + steps + [darkness(0.5, x=0.5, y=0.72, radius=0.3), vignette(0.5)],
                "camera": {"keyframes": [{"t": 0, "zoom": 2.6, "x": 540, "y": 1440}, {"t": round(tx, 2), "zoom": 3.1, "x": 540, "y": 1440, "ease": "inOut"},
                                         {"t": round(d, 3), "zoom": 3.15, "x": 540, "y": 1440}]},
                "sfx": [{"cue": "typing", "at": round(tx, 2), "volume": 0.5}]}

    add("s13_card", at("n12") - LEAD, "B8 hero acts: the inspection card's after-hours number", card_insert)

    def omar1(s0, d):
        a = [at(k) - s0 for k in ("me1", "o1", "o4", "me2")]
        msgs = [dict(m, at=round(x, 3)) for m, x in zip(O_1, a)]
        phone = {"members": MEMBERS, "mode": "chat", "chat": o_thread(msgs, "1:06", typing=[{"from": OMAR, "at": round(a[0] + 0.5, 2), "until": round(a[1], 2)}])}
        return {"layers": phone_scene(phone, 0.55, tremble=2, taps=[{"at": round(a[3] - 0.3, 2), "x": 0.5, "y": 0.9}]), "camera": punch(d, a),
                "sfx": [{"cue": "message_send", "at": round(a[0], 2), "volume": 0.6}, {"cue": "message_pop", "at": round(a[1], 2), "volume": 0.7},
                        {"cue": "message_pop", "at": round(a[2], 2), "volume": 0.7}, {"cue": "message_send", "at": round(a[3], 2), "volume": 0.6}]}

    add("s14_omar", at("me1") - LEAD, "B8 hero reaches the real authority; he asks what it made her press", omar1)

    def omar_react(s0, d):
        on = at("o1", "only") - s0
        return {"layers": car_bg(0.55) + [protagonist("relieved", lookY=0.5, exprs=[{"t": 0, "e": "relieved"}, {"t": round(on, 2), "e": "suspicious"}]), vignette(0.5)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.08, "y": "46%"}, {"t": round(on, 2), "zoom": 1.1, "y": "46%"}, {"t": round(on + 0.15, 2), "zoom": 1.18, "y": "44%", "ease": "out"},
                                         {"t": round(d, 3), "zoom": 1.19, "y": "44%"}]},
                "sfx": [{"cue": "message_pop", "at": 0.1, "volume": 0.6}]}

    add("s14b_react", at("o1") - LEAD, "B8 reaction: a real person answers (then: the ONLY one on call)", omar_react)

    def omar2(s0, d):
        a = [at(k) - s0 for k in ("o4", "me2")]
        msgs = hist(O_1[:2], -6) + [dict(m, at=round(x, 3)) for m, x in zip(O_1[2:], a)]
        phone = {"members": MEMBERS, "mode": "chat", "chat": o_thread(msgs, "1:06")}
        return {"layers": phone_scene(phone, 0.55, tremble=2, taps=[{"at": round(a[1] - 0.3, 2), "x": 0.5, "y": 0.9}]), "camera": punch(d, a, z0=1.04),
                "sfx": [{"cue": "message_pop", "at": round(a[0], 2), "volume": 0.7}, {"cue": "message_send", "at": round(a[1], 2), "volume": 0.6}]}

    add("s14c_press", at("o4") - LEAD, "B8 'What did they tell you to press?' / '2 11 5'", omar2)

    def code(s0, d):
        a = at("o5") - s0
        msgs = hist(O_1, -8) + [dict(O_2[0], at=round(a, 3))]
        phone = {"members": MEMBERS, "mode": "chat", "chat": o_thread(msgs, "1:06")}
        return {"layers": phone_scene(phone, 0.55, tremble=2), "camera": punch(d, [a], step=0.12),
                "sfx": [{"cue": "message_pop", "at": round(a, 2), "volume": 0.8}]}

    add("s15_code", at("o5") - LEAD, "B4/T2 count payoff: 2-11-5 is the controller's reset code", code)

    def code_react(s0, d):
        return {"layers": car_bg(0.55) + [protagonist("shocked", lookY=0.5, blink=False), vignette(0.5)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.05}, {"t": 0.15, "zoom": 1.18, "y": "44%", "ease": "out"}, {"t": round(d, 3), "zoom": 1.2, "y": "44%"}]},
                "sfx": [{"cue": "heartbeat_slow", "at": 0.05, "volume": 0.5}]}

    add("s16_react", at("o5", "Only") - LEAD, "B4 reaction: only his office has the code", code_react)

    def turn(s0, d):
        c, a = at("o2") - s0, at("o3") - s0
        msgs = hist(O_1 + O_2[:1], -6) + [dict(O_2[1], at=round(c, 3)), dict(O_2[2], at=round(a, 3))]
        phone = {"members": MEMBERS, "mode": "chat", "chat": o_thread(msgs, "1:06"), "vibrate": [{"at": round(a, 2), "duration": 0.4}]}
        return {"layers": phone_scene(phone, 0.55, tremble=4) + [
            comp("horror/Vignette", {"amount": 0.95, "color": "190,20,30"}, depth=0, z=61, start=round(a, 2), end=round(a + 0.45, 2)),
            comp("horror/Glitch", {"cues": [{"at": round(a, 2), "duration": 0.25, "amount": 0.8}]}, depth=0, z=62)],
            "camera": {"keyframes": [{"t": 0, "zoom": 1.0, "y": "50%"}, {"t": round(c, 2), "zoom": 1.0, "y": "50%"}, {"t": round(c + 0.18, 2), "zoom": 1.06, "y": "50%", "ease": "out"},
                                     {"t": round(a, 2), "zoom": 1.07, "y": "50%"}, {"t": round(a + 0.15, 2), "zoom": 1.3, "y": "58%", "ease": "out"},
                                     {"t": round(d, 3), "zoom": 1.34, "y": "58%"}], "shake": [{"at": round(a, 2), "duration": 0.3, "amplitude": 14}]},
            "sfx": [{"cue": "message_pop", "at": round(c, 2), "volume": 0.7}, {"cue": "stinger", "at": round(a, 2), "volume": 0.8}]}

    add("s17_turn", at("o2") - LEAD, "B8 TURN: dead camera, 'Who are you talking to?' (only red flash) + 1.0 s fan-only hold", turn)

    def rival(s0, d):
        b, k = at("m9") - s0, at("o6") - s0
        msgs = hist(O_1 + O_2, -10) + [dict(O_KEY, at=round(k, 3))]
        phone = {"members": MEMBERS, "mode": "chat", "chat": o_thread(msgs, "1:07"),
                 "banners": [{"at": round(b, 2), "duration": round(k - b - 0.1, 2), "app": "Messages", "title": MAINT, "text": "Don't answer him. He isn't in the building."}]}
        return {"layers": phone_scene(phone, 0.55, tremble=3), "camera": punch(d, [k]),
                "sfx": [{"cue": "notify", "at": round(b, 2), "volume": 0.8}, {"cue": "message_pop", "at": round(k, 2), "volume": 0.7}]}

    add("s18_rival", at("m9") - LEAD, "Rival claims: Maintenance banners over Omar's thread; door key, five minutes", rival)

    def verdict(s0, d):
        return {"layers": [svg_layer(split_cards()), comp("horror/Glitch", {"amount": 0.08}, depth=0, z=40), vignette(0.45)],
                "camera": push(d, 1.0, 1.04), "transitionIn": {"type": "glitch", "duration": 0.25}, "captionY": 0.12,
                "sfx": [{"cue": "drone", "at": 0.0, "volume": 0.35}]}

    add("s19_verdict", at("n13") - LEAD, "Verdict line: one knew my name, the other had a key", verdict)

    # B6 isolation ------------------------------------------------------------------------
    def lights_out(s0, d):
        o = at("n14", "out") - s0
        return {"layers": car_bg(0.55) + [protagonist("scared", lookY=0.4),
                                          rect("50%", "50%", 1080, 1920, "#020203", depth=0, z=70, start=round(o, 2)),
                                          darkness(0.97, y=0.82, radius=0.16, start=round(o, 2), z=71)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.1}, {"t": round(d, 3), "zoom": 1.12}]},
                "sfx": [{"cue": "relay_click", "at": round(o, 2), "volume": 1.0}, {"cue": "breath", "at": round(o + 0.2, 2), "volume": 0.6}]}

    add("s20_out", at("n14") - LEAD, "B6 lights out (fan spins down)", lights_out)

    def undelivered(s0, d):
        w, nd, nb = at("n15", "where") - s0, at("n15", "Not") - s0, at("n15", "No") - s0
        msgs = hist(O_1 + O_2 + [O_KEY], -12) + [{"me": True, "text": "where are you?", "at": round(w, 3)}, dict(ND, at=round(nd, 3)),
                                                {"kind": "system", "text": "No service", "at": round(nb, 3)}]
        phone = {"members": MEMBERS, "mode": "chat", "chat": o_thread(msgs, "1:09", battery=24)}
        return {"layers": phone_scene(phone, blackout=True, tremble=3, taps=[{"at": round(w - 0.2, 2), "x": 0.9, "y": 0.93}]), "camera": punch(d, [w, nd]),
                "sfx": [{"cue": "message_send", "at": round(w, 2), "volume": 0.6}, {"cue": "tick", "at": round(nd, 2), "volume": 0.6}]}

    add("s21_nodeliver", at("n15") - LEAD, "B6 isolation: my texts fail, no service", undelivered)

    def deleted(s0, d):
        g, b = at("n16", "gone") - s0, at("m10") - s0
        msgs = hist(O_1 + O_2 + [O_DELETED, {"me": True, "text": "where are you?"}, ND, {"kind": "system", "text": "No service"}], -12)
        phone = {"members": MEMBERS, "mode": "chat", "chat": o_thread(msgs, "1:09", battery=24),
                 "banners": [{"at": round(b, 2), "duration": round(d - b, 2), "app": "Messages", "title": MAINT, "text": "He isn't coming. Keep your eyes on the doors."}]}
        return {"layers": phone_scene(phone, blackout=True, tremble=3, glitch=[{"at": 0.0, "duration": 0.3, "amount": 0.5}]),
                "camera": {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": round(g, 2), "zoom": 1.0}, {"t": round(g + 0.2, 2), "zoom": 1.04, "ease": "out"},
                                         {"t": round(b, 2), "zoom": 1.04}, {"t": round(b + 0.2, 2), "zoom": 1.07, "ease": "out"},
                                         {"t": round(at("n17") - s0, 2), "zoom": 1.07}, {"t": round(at("n17") - s0 + 0.2, 2), "zoom": 1.1, "ease": "out"}, {"t": round(d, 3), "zoom": 1.11}]},
                "sfx": [{"cue": "glitch", "at": 0.0, "volume": 0.4}, {"cue": "notify", "at": round(b, 2), "volume": 0.8}]}

    add("s22_deleted", at("n16") - LEAD, "B6 the fake authority acts on the channel: his text deleted; its banner still lands", deleted)

    # B9 peak contact ----------------------------------------------------------------------
    def doors_pov(s0, d):
        return {"background": {"type": "color", "color": "#0b0c0e"},
                "layers": [svg_layer(DOOR_FRAME), svg_layer(door_panel("L")), svg_layer(door_panel("R")),
                           rect(540, 760, 500, 860, "#aab3bc", opacity=0.14, blur=8),
                           protagonist("scared", w=980, x="42%", opacity=0.3, blur=5, lookX=0, lookY=0),
                           darkness(0.9, y=0.62, radius=0.36), vignette(0.6)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.0, "x": "50%", "y": "52%"}, {"t": round(at("n18", "mirror") - s0, 2), "zoom": 1.06, "x": "52%", "y": "48%", "ease": "linear"},
                                         {"t": round(at("n19") - s0, 2), "zoom": 1.08, "x": "53%", "y": "47%"}, {"t": round(d, 3), "zoom": 1.16, "x": "55%", "y": "44%", "ease": "linear"}]},
                "sfx": [{"cue": "breath", "at": 0.1, "volume": 0.5}, {"cue": "drone", "at": 0.3, "volume": 0.3}]}

    add("s23_doors", at("n18") - LEAD, "B9 the steel doors in phone light; the mirror behind me, reflected", doors_pov)

    def the_image(s0, d):
        return {"background": {"type": "color", "color": "#0b0c0e"},
                "layers": [svg_layer(DOOR_FRAME), svg_layer(door_panel("L")), svg_layer(door_panel("R")),
                           rect(690, 900, 560, 940, "#b9c2ca", opacity=0.3, blur=4),
                           protagonist("stare", w=520, x=720, y=1360, light="phone", blink=False, opacity=0.95),
                           protagonist("terrified", w=1000, x="30%", opacity=0.42, blur=2, blink=False, lookX=0, lookY=0),
                           darkness(0.8, x=0.58, y=0.48, radius=0.5),
                           comp("horror/Heartbeat", {"bpm": 60, "intensity": 0.5}, depth=0, z=46), vignette(0.55)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.08, "x": "56%", "y": "46%"}, {"t": round(d, 3), "zoom": 1.08, "x": "56%", "y": "46%"}]},
                "sfx": [{"cue": "heartbeat", "at": round(end("n20") - s0, 2), "volume": 0.8}]}

    add("s24_image", at("n20") - LEAD, "B9 THE image, held: my face where the back of my head should be (3.0 s silence)", the_image)

    def told(s0, d):
        a = at("m11") - s0
        msgs = hist(M_EARLY + M_RULES, -20) + [{"from": MAINT, "text": "I told you not to look.", "at": round(a, 3)}]
        phone = {"members": MEMBERS, "mode": "chat", "chat": m_thread(msgs, "1:09", battery=22)}
        return {"layers": phone_scene(phone, blackout=True, tremble=4, glitch=[{"at": round(a + 0.5, 2), "duration": 0.3, "amount": 0.4}]),
                "camera": punch(d, [a], z0=1.1),
                "sfx": [{"cue": "message_pop", "at": round(a, 2), "volume": 0.8}, {"cue": "glitch", "at": round(a + 0.5, 2), "volume": 0.3}]}

    add("s25_told", at("m11") - LEAD, "B9 punished: 'I told you not to look.'", told)

    def names(s0, d):
        o1, o2 = at("n21", "Omar") - s0, at("n21", "Omar", 1) - s0
        msgs = hist(O_1 + O_2 + [O_DELETED, {"me": True, "text": "where are you?"}, ND], -14) + [
            {"me": True, "text": "Omar?", "at": round(o1, 3)}, dict(ND, at=round(o1 + 0.3, 3)),
            {"me": True, "text": "OMAR??", "at": round(o2, 3)}, dict(ND, at=round(o2 + 0.3, 3))]
        phone = {"members": MEMBERS, "mode": "chat", "chat": o_thread(msgs, "1:10", battery=21)}
        return {"layers": phone_scene(phone, blackout=True, tremble=5), "camera": punch(d, [o1, o2], z0=1.08),
                "sfx": [{"cue": "message_send", "at": round(o1, 2), "volume": 0.6}, {"cue": "message_send", "at": round(o2, 2), "volume": 0.7}]}

    add("s26_names", at("n21") - LEAD, "S8 two unanswered name checks (caps), not delivered", names)

    # B10 lifeline ---------------------------------------------------------------------------
    def one_bar(s0, d):
        a = at("o7") - s0
        notes = [{"at": -1, "app": "Messages", "title": MAINT, "text": "I told you not to look."},
                 {"at": round(a, 3), "app": "Messages · 1 bar", "title": OMAR, "text": "Your texts stopped. Press the alarm. The intercom opens for ten seconds."}]
        phone = {"members": MEMBERS, "mode": "lock", "lock": {"time": "1:10", "date": "Saturday, November 14", "notifications": notes, "battery": 21},
                 "vibrate": [{"at": round(a, 2), "duration": 0.5}]}
        return {"layers": [rect("50%", "50%", 1080, 1920, "#040405"), darkness(0.95, y=0.62, radius=0.42, z=0), hand_phone(phone, tremble=4, dark=True), vignette(0.6)],
                "camera": punch(d, [a, at("o7", "alarm") - s0, at("o7", "ten") - s0], z0=1.02, step=0.06, y_last="44%"),
                "sfx": [{"cue": "phone_buzz", "at": round(a, 2), "volume": 0.8}]}

    add("s27_onebar", at("n22") - LEAD, "B10 one bar, one text: the alarm is the only route left", one_bar)

    def alarm_wait(s0, d):
        return {"background": {"type": "color", "color": "#08090b"},
                "layers": panel(pressed=[(-5, 2), (-5, 11), (-5, 5)], flicker=0.0, bell=True) + [
                          rect("50%", "50%", 1080, 1920, "#000000", opacity=0.3, depth=0, z=44), darkness(0.88, x=0.5, y=0.5, radius=0.3), vignette(0.6)],
                "camera": {"keyframes": [{"t": 0, "zoom": 2.2, "x": 690, "y": 1520}, {"t": round(at("o7", "intercom") - s0, 2), "zoom": 2.35, "x": 695, "y": 1530, "ease": "linear"},
                                         {"t": round(at("o7", "intercom") - s0 + 0.2, 2), "zoom": 2.5, "x": 700, "y": 1540, "ease": "out"}, {"t": round(d, 3), "zoom": 2.6, "x": 700, "y": 1540, "ease": "linear"}]},
                "sfx": [{"cue": "heartbeat_slow", "at": 0.1, "volume": 0.6}]}

    add("s27b_alarmwait", at("o7", "Press") - LEAD, "B10 the alarm button in phone light (the one rule I was told never to break)", alarm_wait)

    def alarm(s0, d):
        pr = at("n23", "pressed") - s0
        glow = {"type": "circle", "x": 720, "y": 1560, "width": 96, "height": 96, "fill": "#ffd36b", "opacity": 0.0, "shadow": "0 0 22px rgba(255,190,60,0.9)",
                "keyframes": [{"t": round(pr, 2), "opacity": 0}, {"t": round(pr + 0.08, 2), "opacity": 0.95}]}
        return {"background": {"type": "color", "color": "#08090b"},
                "layers": panel(pressed=[(-5, 2), (-5, 11), (-5, 5)], flicker=0.0, bell=True) + [glow,
                          rect("50%", "50%", 1080, 1920, "#000000", opacity=0.3, depth=0, z=44), darkness(0.85, x=0.5, y=0.5, radius=0.32), vignette(0.6)],
                "camera": {"keyframes": [{"t": 0, "zoom": 2.6, "x": 700, "y": 1540}, {"t": round(d, 3), "zoom": 2.75, "x": 710, "y": 1550}],
                           "shake": [{"at": round(pr, 2), "duration": 0.18, "amplitude": 10}]},
                "sfx": [{"cue": "click", "at": round(pr, 2), "volume": 0.9}, {"cue": "desk_bell_ring", "at": round(SIL["q3"][0] - s0, 2), "volume": 0.9},
                        {"cue": "static", "at": round(SIL["q3"][0] - s0 + 0.35, 2), "volume": 0.5}]}

    add("s28_alarm", at("n23") - LEAD, "B10 rule three broken on purpose: I press the alarm (bell, crackle)", alarm)

    def intercom(s0, d):
        t_open = at("n23", "pressed") - s0  # negative: the clock started on the press, one scene earlier
        cut = end("v3") - s0
        span = cut - t_open  # ten seconds promised; it reaches 0:00 on the cut
        nb = at("v3", "Nobodys") - s0
        timer = comp("explainer/Timer", {"from": 10, "to": 0, "at": round(t_open, 2), "rate": round(10 / span, 4), "label": "intercom", "warnBelow": 4, "size": 120},
                     depth=0, z=60, x="50%", y="30%", width=520, height=260)
        return {"background": {"type": "color", "color": "#08090b"},
                "layers": [svg_layer(INTERCOM), darkness(0.75, y=0.55, radius=0.45),
                           comp("horror/Glitch", {"cues": [{"at": round(nb, 2), "duration": 0.35, "amount": 0.5}, {"at": round(cut - 0.1, 2), "duration": 0.5, "amount": 0.9}]}, depth=0, z=45),
                           timer, vignette(0.55)],
                "camera": punch(d, [at("v1") - s0, at("nv1") - s0, at("v2", "nine") - s0, at("v3", "Nobodys") - s0], z0=1.0, step=0.04, y_last="50%"), "captionY": 0.12,
                "sfx": [{"cue": "static", "at": round(cut, 2), "volume": 0.7}]}

    add("s29_intercom", SIL["q3"][0] + 0.3, "B10/B11 ten seconds on the intercom; twist: car 2 is on nine, empty", intercom)

    # B11 punishment, climb -------------------------------------------------------------------
    def dead(s0, d):
        return {"layers": [rect("50%", "50%", 1080, 1920, "#040405"), protagonist("terrified", lookY=0.2, blink=False, w=980), darkness(0.86, y=0.5, radius=0.38), vignette(0.6)],
                "camera": push(d, 1.12, 1.16, y="44%")}

    add("s30_dead", at("n24") - LEAD, "B11 the line is dead", dead)

    def shouldnt(s0, d):
        a = at("m12") - s0
        msgs = hist(M_EARLY + M_RULES + [{"from": MAINT, "text": "I told you not to look."}], -20) + [{"from": MAINT, "text": "You shouldn't have done that.", "at": round(a, 3)}]
        phone = {"members": MEMBERS, "mode": "chat", "chat": m_thread(msgs, "1:10", battery=20)}
        return {"layers": phone_scene(phone, blackout=True, tremble=4), "camera": punch(d, [a], z0=1.1),
                "sfx": [{"cue": "message_pop", "at": round(a, 2), "volume": 0.9}]}

    add("s31_shouldnt", at("m12") - LEAD, "B11 the entity acts: 'You shouldn't have done that.'", shouldnt)

    def climb(s0, d):
        c = at("n25", "climb") - s0
        return {"background": {"type": "color", "color": "#08090b"},
                "layers": panel(pressed=[], frm=9, to=12, at0=round(c, 2), per=4.0, flicker=0.3, arrow_mask=False, card=False) +
                          [rect("50%", "50%", 1080, 1920, "#000000", opacity=0.5, depth=0, z=44), darkness(0.7, x=0.5, y=0.2, radius=0.4), vignette(0.55)],
                "camera": {"keyframes": [{"t": 0, "zoom": 2.0, "x": 540, "y": 390}, {"t": round(d, 3), "zoom": 2.2, "x": 540, "y": 390}],
                           "shake": [{"at": round(c, 2), "duration": 0.5, "amplitude": 20}, {"at": round(c + 0.5, 2), "duration": round(max(0.5, d - c - 0.5), 2), "amplitude": 3, "decay": False}]},
                "sfx": [{"cue": "impact", "at": round(c, 2), "volume": 0.8}, {"cue": "underwater_rumble", "at": round(c + 0.2, 2), "volume": 0.7}]}

    add("s32_climb", at("n25") - LEAD, "B11 the car climbs; the dashes never change", climb)

    # B12 cliff ------------------------------------------------------------------------------
    def doors_open(s0, d):
        sl = at("n26", "slid") - s0
        o = [{"t": round(sl, 2), "x": 540}, {"t": round(sl + 1.0, 2), "x": 540 - 420, "ease": "inOut"}]
        r = [{"t": round(sl, 2), "x": 540}, {"t": round(sl + 1.0, 2), "x": 540 + 420, "ease": "inOut"}]
        return {"background": {"type": "color", "color": "#0b0c0e"},
                "layers": [svg_layer(landing(False, False)), svg_layer(door_panel("L"), keyframes=o), svg_layer(door_panel("R"), keyframes=r),
                           svg_layer(DOOR_FRAME), darkness(0.6, y=0.5, radius=0.6), vignette(0.55)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": round(d, 3), "zoom": 1.04}]},
                "sfx": [{"cue": "relay_click", "at": 0.1, "volume": 0.8}, {"cue": "door_creak", "at": round(sl, 2), "volume": 0.5}]}

    add("s33_open", at("n26") - LEAD, "B12 the doors open", doors_open)

    def blank(s0, d):
        return {"layers": [svg_layer(landing(False, False)), comp("horror/Flicker", {"strength": 0.25, "rate": 3}, depth=0, z=40), vignette(0.4)],
                "camera": push(d, 1.0, 1.1, y="55%")}

    add("s34_blank", at("n27") - LEAD, "B12 plant paid: the blank wall, no number; 3.0 s dead air", blank)

    def taps(s0, d):
        tp = at("n28", "tapped") - s0
        tw = at("n28", "Twice") - s0
        return {"layers": [rect("50%", "50%", 1080, 1920, "#08090b"), protagonist("terrified", light="none", lookX=-1, blink=False, w=980),
                           darkness(0.75, x=0.5, y=0.4, radius=0.42), vignette(0.6)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.15, "y": "42%"}, {"t": round(d, 3), "zoom": 1.25, "y": "40%"}],
                           "shake": [{"at": round(tw, 2), "duration": 0.12, "amplitude": 8}, {"at": round(tw + 0.4, 2), "duration": 0.12, "amplitude": 8}]},
                "sfx": [{"cue": "knock", "at": round(tw, 2), "volume": 0.6}, {"cue": "knock", "at": round(tw + 0.4, 2), "volume": 0.6}]}

    add("s35_taps", at("n28") - LEAD, "B12 two taps on the mirror behind me", taps)

    def bookend(s0, d):
        a = at("x1") - s0
        notes = [{"at": -1, "app": "Messages", "title": MAINT, "text": "You shouldn't have done that."},
                 {"at": round(a, 3), "app": "Messages", "title": OMAR, "text": "Don't turn around, Nora. Step out."}]
        phone = {"members": MEMBERS, "mode": "lock", "lock": {"time": "1:11", "date": "Saturday, November 14", "notifications": notes, "battery": 19},
                 "vibrate": [{"at": round(a, 2), "duration": 0.5}]}
        nm = at("n30", "name") - s0
        return {"background": {"type": "color", "color": "#0b0d12"},
                "layers": [svg_layer(landing(False, False), blur=10, opacity=0.7), darkness(0.5, y=0.4, radius=0.8),
                           hand_phone(phone, tremble=3, glitch=[{"at": round(nm, 2), "duration": 0.3, "amount": 0.4}]), vignette(0.5),
                           {"type": "text", "text": "PART 2", "x": "50%", "y": "88%", "fontSize": 64, "color": "#ff4b55", "strokeColor": "#000000", "strokeWidth": 8,
                            "start": round(end("n30") - s0 + 0.15, 2), "enter": {"type": "fade", "duration": 0.15}, "depth": 0, "z": 80}],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.0, "y": "46%"}, {"t": round(a, 2), "zoom": 1.03, "y": "46%"}, {"t": round(a + 0.2, 2), "zoom": 1.12, "y": "40%", "ease": "out"},
                                         {"t": round(nm, 2), "zoom": 1.13, "y": "40%"}, {"t": round(nm + 0.15, 2), "zoom": 1.2, "y": "40%", "ease": "out"}, {"t": round(d, 3), "zoom": 1.21, "y": "40%"}]},
                "captionY": 0.12,
                "sfx": [{"cue": "notify", "at": round(a, 2), "volume": 0.8}, {"cue": "stinger", "at": round(end("n30") - s0 + 0.05, 2), "volume": 0.8}]}

    add("s36_bookend", at("n29") - LEAD, "B12 cliff: the voice swap from Omar's number, lock-screen bookend, hard cut", bookend)
    return S


# ------------------------------------------------------------------ stats
PHONE_SCENES = {"s01_cover", "s02_banner", "s04_thread", "s14_omar", "s15_code", "s17_turn", "s18_rival", "s21_nodeliver", "s22_deleted",
                "s25_told", "s26_names", "s27_onebar", "s31_shouldnt", "s36_bookend"}
NUM_RX = r"\b(1 a\.m\.|six|seven|2|11|5|nine|ten|five minutes|tuesday|car 2|one bar|ten seconds|thirty)\b"


def stats(scenes=None):
    words = sum(len(LINES[k]["text"].split()) for k in ORDER)
    sents = []
    for k in ORDER:
        sents += [s for s in re.split(r"(?<=[.?!])\s+", LINES[k]["text"]) if s.strip()]
    lens = [len(s.split()) for s in sents]
    joined = " ".join(LINES[k]["text"].lower() for k in ORDER)
    nums = re.findall(NUM_RX, joined)
    speech = sum(LINES[k]["end"] - LINES[k]["start"] for k in ORDER)
    qs = sum(LINES[k]["text"].count("?") for k in ORDER)
    you = sum(1 for s in sents if re.search(r"\byou(r|'re)?\b", s.lower()))
    out = {"total_s": TOTAL, "words": words, "wpm_overall": round(words / TOTAL * 60, 1), "wpm_speech": round(words / speech * 60, 1),
           "sentences": len(sents), "sentence_median": statistics.median(lens), "punch_share": round(sum(1 for x in lens if x <= 4) / len(lens), 2),
           "spoken_numbers": len(nums), "numbers_per_min": round(len(nums) / TOTAL * 60, 1), "questions": qs, "questions_per_min": round(qs / TOTAL * 60, 1),
           "you_sentence_share": round(you / len(sents), 2),
           "hook_words": len((LINES["n1"]["text"] + " " + LINES["n2"]["text"]).split()), "hook_end_s": round(end("n2"), 2),
           "silences_s": {k: round(b - a, 2) for k, (a, b) in SIL.items()}}
    if scenes:
        ph = sum(s["duration"] for s in scenes if s["id"] in PHONE_SCENES)
        out["phone_share"] = round(ph / TOTAL, 2)
        out["scenes"] = len(scenes)
        out["max_scene_s"] = max(s["duration"] for s in scenes)
    return out


def mmss(x):
    return f"{int(x // 60)}:{x % 60:04.1f}"


SPK_LABEL = {"N": "NARR", "M": "MAINT (text)", "O": "OMAR (text)", "V": "OMAR-V (intercom)", "X": "OMAR's number (text, voice swap)"}


def script_md(S, scenes):
    """Timed script + shot list, generated from the measured timeline (pasted into script.md)."""
    out = ["## Script (timed from the Kokoro measurement)", ""]
    sec = {k: (n, x) for k, n, x in SECTION_AT}
    idx = 0
    entries = L.V
    for e in entries:
        if e[0] == "#":
            out += ["", f"#### {e[2]} ({mmss(sec[e[1]][1])}, {100 * sec[e[1]][1] / TOTAL:.0f}%)"]
            continue
        if e[0] == "~":
            a, b = SIL[e[1]]
            out.append(f"- `[silence {b - a:.1f} s, {mmss(a)}-{mmss(b)}]` {e[3].get('screen', '')}")
            continue
        lid, spk, text, opts = e
        lab = SPK_LABEL[spk]
        if lid.startswith("me"):
            lab = "ME (text, read by NARR)"
        if lid == "nv1":
            lab = "NORA (live, intercom)"
        out.append(f"- `{mmss(LINES[lid]['start'])}` {lab}: {text}")
        if opts.get("screen"):
            out.append(f"  - On screen: {opts['screen']}")
    out += ["", "## Shot list (generated; every boundary sits LEAD 0.10 s before its anchor word)", "",
            "| # | scene | start | dur | beat | spoken in shot |", "|---|---|---|---|---|---|"]
    for i, sc in enumerate(scenes):
        spoken = " / ".join(LINES[k]["text"] for k in ORDER if S[i][1] - 0.05 <= LINES[k]["start"] < S[i][1] + sc["duration"] - 0.05)
        out.append(f"| {i + 1} | `{sc['id']}` | {mmss(S[i][1])} | {sc['duration']:.2f} | {S[i][2]} | {spoken} |")
    return "\n".join(out) + "\n"


def main():
    CUES.clear()
    S = shots()
    S.sort(key=lambda s: s[1])
    scenes = []
    for i, (sid, t0, beat, fn) in enumerate(S):
        t1 = S[i + 1][1] if i + 1 < len(S) else TOTAL
        d = round(t1 - t0, 3)
        assert d > 0.3, (sid, d)
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
        "version": 1, "id": SLUG, "title": TITLE, "format": "9:16", "fps": 30,
        "scenes": scenes,
        "captions": {"words": words, "maxWords": 5, "maxChars": 18, "gapBreak": 0.3,
                     "style": {"font": "display", "fontSize": 64, "color": "#ffffff", "highlight": "#ff4b55", "highlightMode": "none",
                               "strokeWidth": 10, "uppercase": False, "y": 0.12, "backing": 0.85}},
        "audio": {"voice": [{"src": f"episodes/{SLUG}/mix.wav", "start": 0, "volume": 1, "duration": TOTAL}], "music": [], "sfx": [], "duckOn": "none"},
        "overlays": {"grain": 0.5, "vignette": 0.35, "fadeIn": 0, "fadeOut": 0},
        "_built": {"by": f"backlog/horror/{SLUG}/gen_storyboard.py", "timing": "kokoro-82M cpu per-line stamps (tts_durations.json)",
                   "audio": f"studio/public/episodes/{SLUG}/mix.wav (Spark; per-line wavs in ~/studio/tts/hemc_lines, voice per lines.VOICES with lines.FX, SFX from _sfx_cues baked in)"},
        "_voices": {k: {"name": L.SPEAKER_NAME[k], "kokoro": v[0], "speed": v[1], "fx": L.FX.get(k, "none")} for k, v in L.VOICES.items()},
        "_sfx_cues": sorted(CUES, key=lambda c: c["at"]),
        "_bed": [{"what": "fan + fluorescent buzz bed", "from": 0.0, "to": round(SIL["q1"][0], 2)},
                 {"what": "fan only", "from": round(SIL["q1"][0], 2), "to": round(at("n14", "out"), 2)},
                 {"what": "silence, breath only; low drone from the doors shot", "from": round(at("n14", "out"), 2), "to": round(at("n25", "climb"), 2)},
                 {"what": "motor whine + sub drone (the climb)", "from": round(at("n25", "climb"), 2), "to": round(at("n26", "stopped"), 2)},
                 {"what": "hallway tube buzz only (dead air)", "from": round(at("n26", "stopped"), 2), "to": TOTAL}],
        "_sfx_new": {"glass_tap": "one hard knuckle tap on glass (synth: short 2.8 kHz + 5.1 kHz sine burst, 25 ms decay, small room); use for both mirror moments instead of 'knock'",
                     "cable_groan": "replace underwater_rumble at the 2/11 rungs: sweep_sine 60->35 Hz + shaped_noise, 1.2 s",
                     "alarm_bell": "replace desk_bell_ring: elevator alarm bell, 0.7 s, _bell at 950 Hz with 30 Hz tremolo",
                     "fan_hum / fluorescent_buzz": "bed segments per _bed (120 Hz buzz + pink-noise fan), built as placed SFX segments; mono"},
    }
    st = stats(scenes)
    timing = {"total_s": TOTAL, "stats": st,
              "lines": [{"id": k, "spk": LINES[k]["spk"], "voice": TTS[k]["voice"], "speed": TTS[k]["speed"], "start": round(LINES[k]["start"], 2),
                         "end": round(LINES[k]["end"], 2), "text": LINES[k]["text"]} for k in ORDER],
              "silences": {k: [round(a, 2), round(b, 2)] for k, (a, b) in SIL.items()},
              "sections": [(k, n, round(x, 2), round(100 * x / TOTAL, 1)) for k, n, x in SECTION_AT],
              "scenes": [{"id": s["id"], "start": round(S[i][1], 2), "dur": s["duration"], "beat": S[i][2]} for i, s in enumerate(scenes)]}
    if "--stats" not in sys.argv:
        json.dump(sb, open(os.path.join(HERE, "storyboard.json"), "w"), indent=1, ensure_ascii=False)
        json.dump(timing, open(os.path.join(HERE, "timing.json"), "w"), indent=1, ensure_ascii=False)
        open(os.path.join(HERE, "script_timed.md"), "w").write(script_md(S, scenes))  # pasted into script.md, then deleted
    print(json.dumps(st, indent=1))
    for k, n, x in SECTION_AT:
        print(f"  {mmss(x):>7} {100 * x / TOTAL:5.1f}%  {n}")
    for i, s in enumerate(scenes):
        print(f"  {s['id']:16} {S[i][1]:6.2f} +{s['duration']:5.2f}  {S[i][2]}")
    for k in ORDER:
        print(f"  {k:4} {LINES[k]['start']:6.2f}-{LINES[k]['end']:6.2f} {LINES[k]['spk']} {LINES[k]['text']}")
    print("silences", {k: (round(a, 2), round(b, 2)) for k, (a, b) in SIL.items()})


if __name__ == "__main__":
    main()
