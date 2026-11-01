#!/usr/bin/env python3
"""explainer-never-meet-orca: one generator for the timeline, script.md (timed script + shot list) and storyboard.json.

Inputs (same folder):
  lines.py             narration lines (text, on-screen text, pause after)
  tts_durations.json   Kokoro-82M am_michael per-line timings measured on the Spark CPU
                       (speed 0.96 body, 0.84 hook, 0.88 bookend/CTA) with word timestamps
  script.tmpl.md       script.md template: <!--SCRIPT-->, <!--SHOTS-->, <!--GAPS--> blocks and {t:id} / {p:id} tokens

usage: python3 gen_storyboard.py            writes script.md and storyboard.json next to this file
       python3 gen_storyboard.py --stats    prints the pacing numbers only

Shots start 0.12 s before their anchor word. Scene-local times ("at") come from the same word timestamps, so every
graphic lands on the word that names it. Re-snap after the real mix: rerun with the mix's captions.json timings.
Only registered kit components plus core rect/circle/text/svg layers are used (kit gaps are inline SVG, tier S).
"""
from __future__ import annotations

import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lines import LINES, SECTIONS  # noqa: E402

W, H = 1920, 1080
RED, WHITE, CYAN, YEL, GREEN, GREY, INK = "#e5483d", "#f3f6f7", "#6fd6e8", "#f2c94c", "#5ccf7a", "#8a9aa3", "#0b0f14"
START = 0.30   # first word
GAP = 0.06     # added after every line's own pause
LEAD = 0.12    # cut this long before the anchor word
END_HOLD = 1.6

TTS = json.load(open(os.path.join(HERE, "tts_durations.json")))
SEC_NAME = {k: n for k, n, _ in SECTIONS}


def norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


# ============================================================== timeline
class Line:
    pass


TL = {}
ORDER = []
_t = START
for _id, _sec, _text, _os, _pause in LINES:
    m = TTS[_id]
    assert m["text"] == _text, f"tts_durations.json is stale for {_id}: rerun the Spark TTS check"
    L = Line()
    L.id, L.sec, L.text, L.os, L.pause = _id, _sec, _text, _os, _pause
    L.start = _t
    lead = m["lead"]
    ws = []
    for w, s, e in m["words"]:
        ws.append([w, None if s is None else _t + s - lead, None if e is None else _t + e - lead])
    for i, w in enumerate(ws):  # fill any untimed word by neighbours
        if w[1] is None:
            w[1] = ws[i - 1][2] if i else _t
        if w[2] is None:
            w[2] = w[1] + 0.25
    L.words = ws
    L.dur = m["dur"]
    L.end = _t + m["dur"]
    TL[_id] = L
    ORDER.append(L)
    _t = L.end + _pause + GAP
SPEECH_END = ORDER[-1].end
TOTAL = round(SPEECH_END + END_HOLD, 2)


def word_time(line_id, anchor, nth=1):
    L = TL[line_id]
    if anchor in (0, None, ""):
        return L.words[0][1]
    if isinstance(anchor, int):
        return L.words[anchor][1]
    a = norm(anchor)
    k = 0
    for w in L.words:
        if norm(w[0]).startswith(a):
            k += 1
            if k == nth:
                return w[1]
    raise KeyError(f"{line_id}: no word {anchor!r}")


def fmt(t):
    m, s = divmod(t, 60)
    return f"{int(m)}:{s:04.1f}"


# ============================================================== layer helpers
def comp(name, x, y, w, h, props=None, **kw):
    d = {"type": "component", "name": name, "x": x, "y": y, "width": w, "height": h, "props": props or {}}
    d.update(kw)
    return d


def SV(markup, x, y, w, h, **kw):
    d = {"type": "svg", "markup": markup, "x": x, "y": y, "width": w, "height": h}
    d.update(kw)
    return d


def HL(text, at=0.1, y="15%", size=70, color="white", underline=True, w=1500, **p):
    return comp("explainer/Headline", "50%", y, w, size * 3.2, {"text": text, "at": at, "size": size, "color": color,
                                                               "underline": underline, **p}, depth=0, z=20)


def TAG(text, at, x="50%", y="72%", size=40, accent=CYAN, w=900, **p):
    return comp("explainer/Tag", x, y, w, size * 2.4, {"text": text, "at": at, "size": size, "accent": accent, **p},
                depth=0, z=21)


def STAMP(text, at, x="72%", y="66%", color=RED, size=46, rot=-7):
    return comp("explainer/Tag", x, y, 760, size * 2.6, {"text": text, "at": at, "size": size, "accent": color,
                                                         "bg": color, "color": WHITE, "align": "center"},
                depth=0, z=40, rotate=rot, enter={"type": "pop", "at": at, "duration": 0.3})


def STAT(value, label, at, x="50%", y="58%", size=120, **p):
    return comp("explainer/Stat", x, y, 1000, size * 2.6, {"value": value, "label": label, "at": at, "size": size, **p},
                depth=0, z=20)


def CR(name, x, y, w, h, kf=None, **props):
    extra = {}
    for k in ("start", "end", "enter", "exit", "flipX", "rotate", "z", "opacity", "idle", "scale", "depth"):
        if k in props and not (k == "idle" and isinstance(props[k], bool)):
            extra[k] = props.pop(k)
    d = comp(f"explainer/{name}", x, y, w, h, props, **extra)
    if kf:
        d["keyframes"] = kf
    return d


def pop(at, d=0.3):
    return {"type": "pop", "at": max(0.0, at), "duration": d}


def fade(at, d=0.4):
    return {"type": "fade", "at": max(0.0, at), "duration": d}


def ocean(depth=20, **p):
    return {"type": "component", "name": "explainer/Ocean", "depth": 0.12, "overscan": 1.2, "props": {"depth": depth, **p}}


DUSK = {"skyTop": "#1a2433", "skyBottom": "#5d6f7d"}
DAY = {"skyTop": "#6f9fb8", "skyBottom": "#c9dde6"}
ICY = {"skyTop": "#9fc3d4", "skyBottom": "#e3f1f6", "topColor": "#4f93ad", "midColor": "#1f5368"}


def surface(y=0.5, pal=DUSK, depth=4, **p):
    return ocean(depth, **{"surface": y, "rays": 6, "snow": 30, **pal, **p})


def black():
    return {"type": "color", "color": "#05080b"}


def card():
    return {"type": "gradient", "kind": "radial", "colors": ["#123341", "#071820"]}


def sepia():
    return {"type": "gradient", "colors": ["#e8dcc0", "#cbb68c"]}


def cam(preset="pushIn", amount=0.6):
    return {"preset": preset, "amount": amount}


def cam_to(x, y, zoom, a, b, z0=1.0):
    return {"keyframes": [{"t": 0, "x": 960, "y": 540, "zoom": z0}, {"t": a, "x": 960, "y": 540, "zoom": z0},
                          {"t": b, "x": x, "y": y, "zoom": zoom, "ease": "inOut"}]}


def shake(at, amp=16, dur=0.4):
    return {"at": max(0.0, at), "duration": dur, "amplitude": amp}


def sfx(cue, at=0.0, vol=0.7):
    return {"cue": cue, "at": max(0.0, at), "volume": vol}


# ============================================================== inline SVG props (kit gaps, tier S)
def _svg(vb, body):
    return f'<svg viewBox="{vb}" xmlns="http://www.w3.org/2000/svg">{body}</svg>'


KAYAK = _svg("0 0 600 220",
             '<path d="M300 150 L300 92" stroke="#f3f6f7" stroke-width="12" stroke-linecap="round"/>'
             '<rect x="284" y="98" width="32" height="40" rx="8" fill="#ff7a2f"/>'
             '<circle cx="300" cy="66" r="24" fill="#f3f6f7"/>'
             '<path d="M190 70 L430 150" stroke="#3a4650" stroke-width="9" stroke-linecap="round"/>'
             '<ellipse cx="186" cy="68" rx="26" ry="10" fill="#3a4650" transform="rotate(18 186 68)"/>'
             '<ellipse cx="434" cy="151" rx="26" ry="10" fill="#3a4650" transform="rotate(18 434 151)"/>'
             '<path d="M300 112 L250 100 M300 112 L352 128" stroke="#f3f6f7" stroke-width="9" stroke-linecap="round"/>'
             '<path d="M18 148 Q300 132 582 148 Q560 178 300 186 Q40 178 18 148 Z" fill="#f2c230"/>'
             '<path d="M40 152 Q300 140 560 152" stroke="#c99a1e" stroke-width="5" fill="none"/>')
KAYAK_WL = 0.77   # waterline as a fraction of the kayak box height
KAYAK_TOP = _svg("0 0 600 160",
                 '<ellipse cx="300" cy="80" rx="290" ry="62" fill="#f2c230"/><ellipse cx="300" cy="80" rx="70" ry="34" fill="#c99a1e"/>'
                 '<circle cx="300" cy="80" r="26" fill="#f3f6f7"/><rect x="286" y="48" width="28" height="64" rx="8" fill="#ff7a2f" opacity="0.85"/>'
                 '<path d="M300 -10 L300 170" stroke="#3a4650" stroke-width="10"/>')
KAYAK_FLIP = _svg("0 0 600 260",
                  '<path d="M18 200 Q300 70 582 200 Z" fill="#f2c230"/><path d="M300 120 L300 40" stroke="#f3f6f7" stroke-width="12" stroke-linecap="round"/>'
                  '<circle cx="300" cy="20" r="20" fill="#f3f6f7"/><path d="M300 70 L262 96 M300 70 L338 96" stroke="#f3f6f7" stroke-width="9" stroke-linecap="round"/>')
FIN = _svg("0 0 100 140", '<path d="M6 140 C28 112 44 62 50 0 C62 52 78 104 96 140 Z" fill="#0d1216"/>'
                          '<path d="M0 138 Q50 128 100 138" stroke="#cfe3ea" stroke-width="4" fill="none" opacity="0.7"/>')
FIN_PORT = _svg("0 0 140 120", '<path d="M40 120 C40 80 30 40 0 20 C40 26 70 70 90 120 Z" fill="#0d1216"/>')
FIN_STAR = _svg("0 0 140 120", '<path d="M50 120 C70 70 100 26 140 20 C110 40 100 80 100 120 Z" fill="#0d1216"/>')
TOOTH = _svg("0 0 60 200", '<path d="M8 200 C8 120 18 40 30 0 C42 40 52 120 52 200 Z" fill="#f3f1e6"/>'
                           '<path d="M8 200 L52 200 L46 150 L14 150 Z" fill="#d9cfb4"/>')
CARD = _svg("0 0 856 540", '<rect x="4" y="4" width="848" height="532" rx="44" fill="#3a8fd6"/><rect x="90" y="190" width="130" height="100" rx="14" fill="#f2c94c"/>'
                           '<rect x="90" y="400" width="560" height="34" rx="10" fill="#cfe3f5" opacity="0.7"/>')


def tooth_row(up):
    n = 12
    step = 800 / n
    if up:
        pts = "0,100 " + " ".join(f"{i * step + step / 2:.0f},8 {(i + 1) * step:.0f},100" for i in range(n))
    else:
        pts = "0,0 " + " ".join(f"{i * step + step / 2:.0f},92 {(i + 1) * step:.0f},0" for i in range(n))
    return _svg("0 0 800 100", f'<polygon points="{pts}" fill="#f3f1e6"/>')


def chip_svg(lit):
    labels = ["BODY", "SPEED", "PLAN", "WAVE", "SHARKS", "GIANTS"]
    tabs = ""
    for i, lab in enumerate(labels):
        on = i < lit
        x = 10 + i * 70
        tabs += (f'<rect x="{x}" y="34" width="64" height="40" rx="6" fill="{RED if on else "#2b3b45"}" stroke="#8fb3c0" stroke-width="2"/>'
                 f'<text x="{x + 32}" y="52" font-family="Montserrat" font-weight="900" font-size="15" fill="{WHITE if on else "#7e95a0"}" text-anchor="middle">{i + 1}</text>'
                 f'<text x="{x + 32}" y="68" font-family="Montserrat" font-weight="800" font-size="10" fill="{WHITE if on else "#7e95a0"}" text-anchor="middle">{lab}</text>')
    return _svg("0 0 440 84", '<rect x="2" y="2" width="436" height="80" rx="10" fill="#0f1d24" fill-opacity="0.88" stroke="#8fb3c0" stroke-width="2"/>'
                              f'<text x="14" y="25" font-family="Montserrat" font-weight="900" font-size="17" fill="{WHITE}">THREAT FILE: ORCA</text>{tabs}')


FOLDER_LABELS = ["BODY", "SPEED", "PLAN", "WAVE", "SHARKS", "GIANTS"]
VERDICTS = ["YOU LOSE", "NO CONTEST", "THINKS AHEAD", "NOWHERE SAFE", "EVEN THEY LEAVE", "NO UPPER LIMIT"]


def folder_svg(lit=0, title="THREAT FILE: ORCA"):
    cols = ""
    for i, lab in enumerate(FOLDER_LABELS):
        x = 60 + i * 215
        on = i < lit
        cols += (f'<rect x="{x}" y="40" width="190" height="70" rx="12" fill="{RED if on else "#2b3b45"}" stroke="#8fb3c0" stroke-width="3"/>'
                 f'<text x="{x + 95}" y="86" font-family="Montserrat" font-weight="900" font-size="30" fill="{WHITE}" text-anchor="middle">{i + 1} {lab}</text>'
                 f'<rect x="{x}" y="150" width="190" height="380" rx="10" fill="#14262f" stroke="#3d5966" stroke-width="2"/>')
    return _svg("0 0 1400 600", f'<rect x="20" y="100" width="1360" height="470" rx="22" fill="#0f1d24" stroke="#8fb3c0" stroke-width="4"/>{cols}'
                                f'<text x="700" y="590" font-family="Montserrat" font-weight="900" font-size="0" fill="#fff">.</text>')


SLIP = _svg("0 0 420 560", '<path d="M10 10 L410 10 L410 530 L380 550 L350 530 L320 550 L290 530 L260 550 L230 530 L200 550 L170 530 L140 550 L110 530 L80 550 L50 530 L10 550 Z" fill="#f5efe0"/>'
                           '<text x="210" y="70" font-family="Montserrat" font-weight="900" font-size="34" fill="#222" text-anchor="middle">ORDER SLIP</text>'
                           + "".join(f'<text x="50" y="{150 + i * 80}" font-family="Montserrat" font-weight="800" font-size="34" fill="#333">{t}</text>'
                                     f'<rect x="330" y="{120 + i * 80}" width="40" height="40" fill="none" stroke="#333" stroke-width="4"/>'
                                     + (f'<path d="M336 {140 + i * 80} L348 {154 + i * 80} L368 {124 + i * 80}" stroke="#2e9e55" stroke-width="7" fill="none"/>' if t != "HUMAN" else "")
                                     for i, t in enumerate(["SALMON", "HERRING", "SEAL", "SHARK", "HUMAN"])))
MENU = _svg("0 0 700 560", '<rect x="10" y="10" width="680" height="540" rx="18" fill="#1f2a24" stroke="#8a6a3a" stroke-width="18"/>'
                           '<text x="350" y="90" font-family="Montserrat" font-weight="900" font-size="46" fill="#f3f1e6" text-anchor="middle">FAMILY MENU</text>'
                           + "".join(f'<text x="120" y="{170 + i * 76}" font-family="Montserrat" font-weight="700" font-size="40" fill="#e9e4d4">{t}</text>'
                                     for i, t in enumerate(["SALMON", "HERRING", "SEAL", "SHARK LIVER", "YOU"])))
STRIKE = _svg("0 0 400 20", '<rect x="0" y="6" width="400" height="9" rx="4" fill="#e5483d"/>')
BEACH = _svg("0 0 1920 320", '<path d="M0 320 L0 210 Q600 140 1920 40 L1920 320 Z" fill="#d8c08a"/>'
                             '<path d="M0 214 Q300 186 600 176 Q900 150 1200 128" stroke="#f3f6f7" stroke-width="10" fill="none" stroke-dasharray="40 18" opacity="0.85"/>')
ICE = ('<svg viewBox="0 0 400 160" xmlns="http://www.w3.org/2000/svg"><path d="M10 70 L60 30 L170 22 L260 34 L390 60 '
       'L360 92 L40 96 Z" fill="#e8f3f6"/><path d="M40 96 L360 92 L330 150 L70 150 Z" fill="#9fc6d1" opacity="0.55"/></svg>')
WAVE = _svg("0 0 900 300", '<path d="M0 300 L0 200 Q200 40 420 60 Q600 80 700 150 Q760 190 900 200 L900 300 Z" fill="#e8f6fa" opacity="0.9"/>'
                           '<path d="M60 190 Q240 90 420 100" stroke="#ffffff" stroke-width="14" fill="none" opacity="0.8"/>')
FISH = ('<svg viewBox="0 0 220 90" xmlns="http://www.w3.org/2000/svg"><path d="M20 45 Q70 5 150 30 Q190 40 205 45 Q190 52 150 60 '
        'Q70 85 20 45 Z" fill="#e9d6df" opacity="0.85"/><path d="M20 45 L0 25 L6 45 L0 65 Z" fill="#e9d6df" opacity="0.7"/>'
        '<circle cx="178" cy="42" r="4" fill="#222"/></svg>')
HEART = ('<svg viewBox="0 0 200 180" xmlns="http://www.w3.org/2000/svg"><path d="M100 170 C20 110 0 70 20 35 C40 0 85 5 '
         '100 40 C115 5 160 0 180 35 C200 70 180 110 100 170 Z" fill="#c8453a"/></svg>')
JERRY = _svg("0 0 120 150", '<rect x="10" y="30" width="100" height="115" rx="12" fill="#f2c230"/><rect x="60" y="8" width="34" height="28" rx="6" fill="#c99a1e"/>'
                            '<path d="M24 60 L96 130 M96 60 L24 130" stroke="#c99a1e" stroke-width="8"/>')
BOX = _svg("0 0 200 150", '<rect x="5" y="20" width="190" height="125" fill="#b8874f"/><rect x="5" y="5" width="190" height="30" fill="#a07440"/>'
                          '<rect x="90" y="5" width="20" height="140" fill="#e2c38c"/><text x="100" y="105" font-family="Montserrat" font-weight="900" font-size="22" fill="#5b3e1c" text-anchor="middle">FRAGILE</text>')
BRUSH = _svg("0 0 300 60", '<rect x="0" y="22" width="230" height="16" rx="8" fill="#6fd6e8"/><rect x="226" y="10" width="64" height="26" rx="6" fill="#f3f6f7"/>')
CAGE = _svg("0 0 400 400", '<rect x="10" y="10" width="380" height="380" fill="none" stroke="#c7d2d6" stroke-width="12"/>'
                           + "".join(f'<line x1="{10 + i * 63}" y1="10" x2="{10 + i * 63}" y2="390" stroke="#c7d2d6" stroke-width="7"/>' for i in range(1, 6)))
DIARY = _svg("0 0 700 480", '<rect x="10" y="10" width="680" height="460" rx="8" fill="#efe2c2" stroke="#9a7b4a" stroke-width="6"/><line x1="350" y1="10" x2="350" y2="470" stroke="#9a7b4a" stroke-width="4"/>'
                            + "".join(f'<line x1="{40 if i < 8 else 380}" y1="{80 + (i % 8) * 46}" x2="{320 if i < 8 else 660}" y2="{80 + (i % 8) * 46}" stroke="#6b5636" stroke-width="5" opacity="0.6"/>' for i in range(16))
                            + '<text x="180" y="62" font-family="Georgia" font-style="italic" font-size="34" fill="#4a3a22" text-anchor="middle">Jan. 1911</text>')
PONTING = _svg("0 0 220 300", '<circle cx="80" cy="40" r="26" fill="#4a3a2a"/><path d="M80 66 L80 180 M80 90 L140 110 M80 180 L50 290 M80 180 L110 290" stroke="#4a3a2a" stroke-width="14" stroke-linecap="round"/>'
                              '<rect x="140" y="92" width="56" height="44" rx="4" fill="#2f2418"/><path d="M168 136 L140 296 M168 136 L196 296 M168 136 L168 296" stroke="#2f2418" stroke-width="6"/>')
DOTS98 = _svg("0 0 1400 560", "".join(f'<circle cx="{70 + (i % 14) * 97}" cy="{60 + (i // 14) * 72}" r="26" fill="{WHITE}"/>' for i in range(75)))
DOTS23 = _svg("0 0 1400 560", "".join(f'<circle cx="{70 + (i % 14) * 97}" cy="{60 + (i // 14) * 72}" r="26" fill="none" stroke="#5c6b71" stroke-width="5"/>' for i in range(75, 98)))
SHIP = _svg("0 0 700 260", '<path d="M20 150 L680 150 L620 230 L80 230 Z" fill="#4d5a62"/><rect x="380" y="70" width="180" height="80" fill="#6b7880"/><rect x="420" y="20" width="40" height="50" fill="#e5483d"/>')
BLUBBER = _svg("0 0 900 360", '<rect x="0" y="0" width="900" height="70" fill="#1d2228"/><rect x="0" y="70" width="900" height="200" fill="#f1e3c6"/><rect x="0" y="270" width="900" height="90" fill="#b5524a"/>'
                              + "".join(f'<circle cx="{40 + (i * 137) % 860}" cy="{90 + (i * 53) % 170}" r="{6 + i % 5}" fill="#2a2a2a" opacity="0.8"/>' for i in range(46)))
RAFT = _svg("0 0 420 160", '<ellipse cx="210" cy="110" rx="200" ry="44" fill="#ff7a2f"/><ellipse cx="210" cy="104" rx="150" ry="24" fill="#c95a1f"/>')
BOARDER = _svg("0 0 520 200", '<ellipse cx="260" cy="100" rx="250" ry="34" fill="#0d1216"/><path d="M160 100 L60 150 M200 100 L120 170 M330 100 L420 150 M300 100 L380 170" stroke="#0d1216" stroke-width="18" stroke-linecap="round"/>')
SEALSIL = _svg("0 0 520 200", '<path d="M20 120 Q120 40 300 60 Q440 70 500 100 Q470 140 300 150 Q120 170 20 120 Z" fill="#0d1216"/><path d="M180 140 L130 190 L220 150 Z M360 140 L420 190 L330 150 Z" fill="#0d1216"/>')
ARROW = _svg("0 0 600 120", '<path d="M10 60 L500 60" stroke="#e5483d" stroke-width="22" stroke-linecap="round"/><path d="M480 10 L590 60 L480 110 Z" fill="#e5483d"/>')
PODTREE = _svg("0 0 1200 420", '<path d="M600 40 L250 200 M600 40 L600 200 M600 40 L950 200 M250 200 L150 360 M250 200 L350 360 M950 200 L1050 360" stroke="#8fb3c0" stroke-width="6" fill="none" stroke-dasharray="18 12"/>')
SPOT = _svg("0 0 800 800", '<defs><radialGradient id="s"><stop offset="0" stop-color="#ffffff" stop-opacity="0.32"/><stop offset="0.7" stop-color="#ffffff" stop-opacity="0.08"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient></defs><circle cx="400" cy="400" r="400" fill="url(#s)"/>')
LIMIT = _svg("0 0 200 200", '<circle cx="100" cy="100" r="90" fill="#fff" stroke="#e5483d" stroke-width="20"/><text x="100" y="128" font-family="Montserrat" font-weight="900" font-size="80" fill="#111" text-anchor="middle">50</text>')
RUDDER = _svg("0 0 120 220", '<path d="M50 0 L70 0 L70 60 L110 70 L100 210 L40 200 L50 60 Z" fill="#c9b48a" stroke="#6b5a3a" stroke-width="6"/>')
SLAB_THICK = _svg("0 0 300 420", '<rect x="0" y="0" width="300" height="420" fill="#e8f3f6"/><rect x="0" y="0" width="300" height="40" fill="#ffffff"/>')
SLAB_THIN = _svg("0 0 300 420", '<rect x="0" y="0" width="300" height="10" fill="#f2c230"/>')
OUTLINE = _svg("0 0 600 220", '<path d="M18 148 Q300 132 582 148 Q560 178 300 186 Q40 178 18 148 Z" fill="none" stroke="#f2c94c" stroke-width="6" stroke-dasharray="20 12"/>')
EAR = _svg("0 0 120 160", '<path d="M90 30 C40 0 0 40 20 90 C30 120 60 110 60 140 C60 160 90 160 96 140" stroke="#f3f6f7" stroke-width="12" fill="none" stroke-linecap="round"/>')


def ring_layers(cx, cy, a, b, period=0.9, n=3, size=320, color=WHITE):
    """Sound rings rippling between scene-local a and b (n staggered circles)."""
    out = []
    if b - a < 0.3:
        return out
    for k in range(n):
        kf, t0 = [], a + k * period / n
        while t0 + 0.1 < b:
            kf += [{"t": round(t0, 3), "scale": 0.25, "opacity": 0.0}, {"t": round(t0 + 0.08, 3), "opacity": 0.85},
                   {"t": round(min(t0 + period, b), 3), "scale": 1.5, "opacity": 0.0, "ease": "out"}]
            t0 += period
        if kf:
            out.append({"type": "circle", "x": cx, "y": cy, "width": size, "height": size, "fill": "rgba(0,0,0,0)",
                        "stroke": color, "strokeWidth": 5, "opacity": 0, "keyframes": kf, "z": 4})
    return out


def kayak_at(x, wl_y, w=520, **kw):
    """Side-view kayak whose hull waterline sits on screen y wl_y (px)."""
    h = w * 220 / 600
    y = wl_y - (KAYAK_WL - 0.5) * h
    return SV(KAYAK, x, y, w, h, z=5, **kw)


def fins(xs, wl_y, h=130, sink=None, kf_x=None):
    """Dorsal fins above a waterline; h >= 8% of frame height so they read on a phone."""
    out = []
    for i, x in enumerate(xs):
        lay = SV(FIN, x, wl_y - h / 2 + 6, h * 100 / 140, h, z=3)
        kf = []
        if kf_x:
            kf = [{"t": t, "x": xx[i] if isinstance(xx, list) else xx} for t, xx in kf_x]
        if sink and i in sink:
            ts = sink[i]
            kf = (kf or [{"t": 0, "x": x}]) + [{"t": ts, "y": wl_y - h / 2 + 6, "opacity": 1}, {"t": ts + 0.5, "y": wl_y + h * 0.4, "opacity": 0, "ease": "in"}]
        if kf:
            lay["keyframes"] = sorted(kf, key=lambda k: k["t"])
        out.append(lay)
    return out


def orca(x, y, w, h, kf=None, **p):
    return CR("Orca", x, y, w, h, kf, **p)


# ============================================================== shots
SHOTS = []


def shot(line, anchor=0, kind="", vis="", camd="static", sfxd="", nth=1):
    def deco(fn):
        SHOTS.append({"line": line, "anchor": anchor, "nth": nth, "kind": kind, "vis": vis, "cam": camd, "sfx": sfxd, "fn": fn})
        return fn
    return deco


class Ctx:
    def __init__(self, t0, d, line):
        self.t0, self.d, self.line = t0, d, line

    def w(self, anchor, line=None, nth=1):
        return round(max(0.0, word_time(line or self.line, anchor, nth) - self.t0), 3)

    def ls(self, line=None):
        return round(max(0.0, TL[line or self.line].start - self.t0), 3)

    def le(self, line=None):
        return round(TL[line or self.line].end - self.t0, 3)


WL = 540  # default waterline px for half-frame surface shots (surface=0.5)

# ---------------------------------------------------------------- L1 hook
@shot("h01", 0, "WIDE", "Dusk surface (Ocean surface 0.5). NEW S Kayak + seated YOU at left third, big enough to read; three black dorsal fins mid-distance right, 130 px tall (12% of frame) from frame 1; the nearest fin sinks at ~2.3 s", "drift", "underwater_rumble bed")
def _(c):
    L = [kayak_at("34%", WL, 560)] + fins([1240, 1420, 1580], WL, 130, sink={0: 2.2})
    return dict(bg=surface(0.5), layers=L, camera=cam("drift", 0.5), sfx=[sfx("underwater_rumble", 0, 0.5)])


@shot("h02", 0, "MED", "Same kayak, closer; green-tick Tags SEA: FLAT then LIFE JACKET: ON land on their words; two fins hold far right", "pushIn", "tick x2")
def _(c):
    L = [kayak_at("40%", WL + 40, 700)] + fins([1420, 1600], WL + 40, 120)
    L += [TAG("SEA: FLAT ✓", c.w("flat"), "20%", "16%", accent=GREEN, w=520), TAG("LIFE JACKET: ON ✓", c.w("jacket"), "24%", "26%", accent=GREEN, w=640)]
    return dict(bg=surface(0.5), layers=L, camera=cam("pushIn", 0.4), sfx=[sfx("tick", c.w("flat")), sfx("tick", c.w("jacket"))])


@shot("h03", 0, "MED", "Fins glide closer from the right; Stat 0 WILD HUMAN KILLS pops on 'never'; small Tag IN THE WILD under it on 'wild'", "static", "pop on the 0")
def _(c):
    L = [kayak_at("30%", WL + 40, 620)] + fins([1500, 1660], WL + 40, 130, kf_x=[(0, [1500, 1660]), (c.d, [1180, 1340])])
    L += [STAT(0, "WILD HUMAN KILLS", c.w("never"), "68%", "26%", 130), TAG("IN THE WILD", c.w("wild"), "68%", "44%", 34, w=420)]
    return dict(bg=surface(0.5), layers=L, sfx=[sfx("pop", c.w("never"))])


@shot("h04", 0, "CU", "Split waterline: YOU in the kayak above; below, the hull from underneath", "pushIn", "")
def _(c):
    return dict(bg=surface(0.38, depth=10), layers=[kayak_at("50%", 0.38 * H, 900)], camera=cam("pushIn", 0.5))


@shot("h04", "squeaks", "CU", "White sound rings ripple up into the hull on 'squeaks'; Tag SQUEAK · CREAK", "static", "sonar_ping pitched up x3")
def _(c):
    L = [kayak_at("50%", 0.38 * H, 900)] + ring_layers(960, 640, 0.1, c.d, 0.8, 3, 360)
    L += [TAG("SQUEAK · CREAK", 0.2, "50%", "78%", accent=CYAN, w=520)]
    return dict(bg=surface(0.38, depth=10), layers=L, sfx=[sfx("sonar_ping", 0.1, 0.5), sfx("sonar_ping", 1.0, 0.5), sfx("sonar_ping", 1.9, 0.5)])


@shot("h05", 0, "CU", "Rings stop; the fins are gone from the surface; Ocean rays dim", "static", "all audio ducks to silence 1.0 s")
def _(c):
    return dict(bg=surface(0.38, depth=40, rays=2), layers=[kayak_at("50%", 0.38 * H, 900)], camera={"keyframes": [{"t": 0, "zoom": 1.0}, {"t": c.d, "zoom": 1.06}]})


@shot("h06", 0, "REVEAL", "Cut below: three Orca glide beneath the kayak's shadow (first full reveal); red Headline THEY'RE DECIDING SOMETHING on 'deciding'", "pullOut", "whoosh_long + stinger")
def _(c):
    L = [SV(KAYAK, "50%", "6%", 380, 140, opacity=0.55, z=2)]
    for i, (x0, y, s) in enumerate([(-300, 520, 1.0), (-700, 640, 0.8), (-200, 760, 0.65)]):
        L.append(orca(x0, y, 900 * s, 330 * s, [{"t": 0, "x": x0}, {"t": c.d, "x": x0 + 1500, "ease": "linear"}], timeOffset=i * 0.4))
    L.append(HL("THEY'RE DECIDING SOMETHING", c.w("deciding"), "84%", 64, "red"))
    return dict(bg=ocean(25), layers=L, camera=cam("pullOut", 0.5), sfx=[sfx("whoosh_long", 0.1), sfx("stinger", c.w("deciding"), 0.6)])


# ---------------------------------------------------------------- L2 reframe
@shot("r01", 0, "INFO", "GreatWhite enters left beside a small YOU; Tag ~60-70 BITES / YEAR (ISAF) on 'sixty'", "panRight", "whoosh")
def _(c):
    L = [CR("GreatWhite", "30%", "48%", 760, 300, [{"t": 0, "x": "18%"}, {"t": c.d, "x": "32%"}], pxPerM=110),
         CR("You", "64%", "52%", 140, 230, pose="stand"), TAG("~60-70 BITES / YEAR", c.w("sixty"), "50%", "18%", 46, accent=RED, w=760)]
    return dict(bg=ocean(15), layers=L, camera=cam("panRight", 0.5), sfx=[sfx("whoosh", 0)])


@shot("r01", "The", "INFO", "Orca slides in, Tag KILLER WHALE stamps across it, Stat 0 pops on 'zero'", "pushIn", "impact light")
def _(c):
    L = [orca("50%", "50%", 900, 340, pxPerM=105), TAG("\"KILLER\" WHALE", c.w("killer"), "50%", "20%", 48, accent=RED, w=600),
         STAT(0, "WILD HUMAN KILLS", c.w("zero"), "50%", "80%", 110)]
    return dict(bg=ocean(15), layers=L, camera=cam("pushIn", 0.4), sfx=[sfx("impact", c.w("zero"), 0.5)])


@shot("r02", 0, "PUNCH", "Master question on a hard black frame, white with red YOU, held through the 1 s pause", "static", "music drops out")
def _(c):
    return dict(bg=black(), layers=[HL("WHY HAS IT\nNEVER PICKED YOU?", 0.15, "46%", 96, "white", False)],
                camera={"keyframes": [{"t": 0, "zoom": 1.0}, {"t": c.d, "zoom": 1.05}]}, trans={"type": "dipBlack", "duration": 0.3})


@shot("r03", 0, "CARD", "'It's not that it can't.' over the dark card; THREAT FILE corner chip slides in top-right and stays for the whole ladder", "static", "click")
def _(c):
    return dict(bg=card(), layers=[HL("IT'S NOT THAT IT CAN'T.", 0.05, "46%", 76)], sfx=[sfx("click", 0.3)])


@shot("r03", "surfs", "CARD", "Credential 1: beige beach strip, Orca sliding up the sand toward a Seal; Tag 1 BEACH RAIDS", "static", "pop")
def _(c):
    L = [SV(BEACH, "50%", "80%", 1920, 320, z=1), orca("50%", "62%", 640, 240, [{"t": 0, "x": "30%", "y": "70%"}, {"t": c.d, "x": "48%", "y": "60%"}], rotate=-8),
         CR("Seal", "72%", "54%", 260, 110), TAG("1  BEACH RAIDS", 0.1, "50%", "18%", 48, accent=RED, w=640)]
    return dict(bg=surface(0.45, DAY), layers=L, sfx=[sfx("pop", 0.1)])


@shot("r03", "leaves", "CARD", "Credential 2: grey GreatWhite on its back on the sand, red Liver glow then empty; Tag 2 GREAT WHITES, NO LIVERS", "pushIn", "pop")
def _(c):
    L = [SV(BEACH, "50%", "80%", 1920, 320, z=1), comp("explainer/GreatWhite", "52%", "64%", 700, 260, {"silhouette": "#9aa7ad", "idle": False}, keyframes=[{"t": 0, "scaleY": -1}]),
         CR("Liver", "47%", "66%", 150, 110, kf=[{"t": 0, "opacity": 0}, {"t": 0.3, "opacity": 1}, {"t": max(0.6, c.d - 0.4), "opacity": 0}], shadow="0 0 18px #e5483d"),
         TAG("2  GREAT WHITES, NO LIVERS", 0.1, "50%", "18%", 48, accent=RED, w=820)]
    return dict(bg=surface(0.45, DAY), layers=L, camera=cam("pushIn", 0.4), sfx=[sfx("pop", 0.1)])


@shot("r03", "and", "CARD", "Credential 3: BlueWhale silhouette fills the frame, a cluster of tiny Orca icons at its flank; Tag 3 THE BIGGEST ANIMAL EVER", "pullOut", "pop")
def _(c):
    L = [CR("BlueWhale", "50%", "52%", 1700, 420, silhouette="#4b6b7a")]
    L += [orca(f"{60 + i * 4}%", f"{40 + (i % 2) * 18}%", 160, 60, timeOffset=i * 0.3) for i in range(5)]
    L += [TAG("3  THE LARGEST ANIMAL EVER", 0.1, "50%", "15%", 48, accent=RED, w=820)]
    return dict(bg=ocean(30), layers=L, camera=cam("pullOut", 0.4), sfx=[sfx("pop", 0.1)])


# ---------------------------------------------------------------- L3 promise
@shot("p01", 0, "CARD", "Progress device: big THREAT FILE folder, six empty tabs 1 BODY .. 6 GIANTS; shrinks into the corner chip at the end", "static", "whoosh + click")
def _(c):
    f = SV(folder_svg(0), "50%", "52%", 1400, 600, z=10, enter=pop(0.05, 0.35),
           keyframes=[{"t": 0, "scale": 1, "x": "50%", "y": "52%", "opacity": 1}, {"t": max(0.5, c.d - 0.55), "scale": 1, "x": "50%", "y": "52%"},
                      {"t": c.d, "scale": 0.3, "x": "86%", "y": "6%", "opacity": 0.2, "ease": "in"}])
    return dict(bg=card(), layers=[f, HL("THREAT FILE: ORCA", 0.1, "12%", 64)], sfx=[sfx("whoosh", 0), sfx("click", c.d - 0.4)], nochip=True)


# ---------------------------------------------------------------- R1 body
@shot("b01", 0, "SCALE", "Tab 1 lights on the chip; Orca at true scale (pxPerM 120); ScaleBar ~8 M grows on 'eight'; Tag ~6 TONNES on 'six'", "panRight", "whoosh")
def _(c):
    L = [orca("50%", "48%", 1100, 420, pxPerM=120, finScale=1.5),
         comp("explainer/ScaleBar", "50%", "74%", 960, 110, {"label": "~8 M", "at": c.w("eight"), "labelSize": 44}),
         TAG("~6 TONNES", c.w("six"), "50%", "18%", 48, w=520)]
    return dict(bg=ocean(12), layers=L, camera=cam("panRight", 0.4), sfx=[sfx("whoosh", 0)])


@shot("b02", 0, "SCALE", "Same pxPerM: two Car figures nose to tail under the Orca (2 x 4.5 m vs 8 m)", "static", "pop x2")
def _(c):
    L = [orca("50%", "34%", 1100, 420, pxPerM=120, finScale=1.5),
         CR("Car", "36%", "74%", 560, 220, pxPerM=120, start=c.w("two"), enter=pop(c.w("two"))),
         CR("Car", "64%", "74%", 560, 220, pxPerM=120, color="#c8453a", start=c.w("two") + 0.25, enter=pop(c.w("two") + 0.25)),
         TAG("≈ 2 CARS LONG", c.w("two"), "50%", "92%", 40, w=520)]
    return dict(bg=ocean(12), layers=L, sfx=[sfx("pop", c.w("two")), sfx("pop", c.w("two") + 0.25)])


@shot("b02", "as", "SCALE", "Balance: Orca on the left, a Car drops on the right, Tag x4 CARS ≈ 6 T; beam settles level", "static", "ding")
def _(c):
    L = [comp("explainer/Balance", "50%", "56%", 1500, 700, {"left": {"species": "orca", "w": 640, "at": 0}, "right": {"species": "car", "w": 360, "at": 0.3, "drop": True},
                                                          "tilt": [{"t": 0, "v": -12}, {"t": 0.8, "v": -12}, {"t": 1.6, "v": 0, "ease": "out"}]}),
         TAG("× 4 CARS ≈ 6 TONNES", 0.5, "72%", "20%", 44, w=640)]
    return dict(bg=ocean(12), layers=L, sfx=[sfx("ding", 1.6)])


@shot("b03", 0, "SCALE", "Honest true scale (300 px/m): NEW S dorsal-fin cut-out 1.8 m beside YOU 1.75 m on one baseline; Tags with heights", "pushIn", "ding")
def _(c):
    ppm, base = 300, 980
    L = [SV(FIN, "38%", base - 1.8 * ppm / 2, 1.8 * ppm * 100 / 140, 1.8 * ppm, z=3),
         CR("You", "62%", base - 1.75 * ppm / 2, 1.75 * ppm * 0.6, 1.75 * ppm, pxPerM=ppm, align="bottom", pose="shrug", start=c.w("as"), enter=pop(c.w("as"))),
         TAG("FIN ~1.8 M", 0.2, "38%", "8%", 40, w=420), TAG("YOU ~1.75 M", c.w("you"), "62%", "8%", 40, w=420)]
    return dict(bg=ocean(10), layers=L, camera=cam("pushIn", 0.3), sfx=[sfx("ding", c.w("you"))])


@shot("b04", 0, "INFO", "Orca head-on (pose head); Stat counts up to 56 TEETH (MAX) on 'fifty-six'", "pushIn", "tick on count end")
def _(c):
    L = [orca("30%", "50%", 520, 520, pose="head"), STAT(56, "TEETH (UP TO)", c.w("fifty"), "68%", "48%", 150, **{"from": 0, "duration": 0.8})]
    return dict(bg=ocean(14), layers=L, camera=cam("pushIn", 0.3), sfx=[sfx("tick", c.w("fifty") + 0.8)])


@shot("b04", "biggest", "CU", "True scale (4500 px/m): NEW S cone tooth 10 cm beside a credit card 8.6 cm; Tags", "static", "click")
def _(c):
    ppm = 4500
    L = [SV(TOOTH, "36%", "52%", 0.1 * ppm * 0.3, 0.1 * ppm, z=3), SV(CARD, "64%", "56%", 0.0856 * ppm, 0.054 * ppm, start=c.w("longer"), enter=pop(c.w("longer"))),
         TAG("TOOTH ~10 CM", 0.2, "36%", "12%", 40, w=440), TAG("YOUR CARD 8.6 CM", c.w("credit"), "64%", "28%", 40, w=520)]
    return dict(bg=card(), layers=L, sfx=[sfx("click", c.w("longer"))])


@shot("b05", 0, "CU", "Two NEW S tooth rows slide together and lock on 'interlock'; Tag INTERLOCKING", "static", "click sharp")
def _(c):
    a = c.w("interlock")
    L = [SV(tooth_row(False), "50%", "40%", 900, 112, keyframes=[{"t": 0, "y": "30%"}, {"t": a, "y": "30%"}, {"t": a + 0.4, "y": "44.6%", "ease": "in"}]),
         SV(tooth_row(True), "50%", "60%", 900, 112, keyframes=[{"t": 0, "y": "70%"}, {"t": a, "y": "70%"}, {"t": a + 0.4, "y": "55.4%", "ease": "in"}]),
         TAG("INTERLOCKING", a + 0.4, "50%", "84%", 44, w=520)]
    return dict(bg=card(), layers=L, sfx=[sfx("click", a + 0.4)])


@shot("b05", "held", "PUNCH", "Black flash, three red words punch in on their words: HOLD · TEAR · SWALLOW", "shake small x3", "impact x3")
def _(c):
    L = [comp("explainer/Headline", f"{28 + i * 22}%", "48%", 520, 260, {"text": t, "at": c.w(wd), "size": 96, "color": "red", "underline": False}, depth=0, z=20)
         for i, (t, wd) in enumerate([("HOLD", "held"), ("TEAR", "torn"), ("SWALLOW", "swallowed")])]
    return dict(bg=black(), layers=L, camera={"shake": [shake(c.w(w), 10, 0.25) for w in ("held", "torn", "swallowed")]},
                sfx=[sfx("impact", c.w(w), 0.5) for w in ("held", "torn", "swallowed")])


@shot("b06", 0, "INFO", "Orca with a red tag WHALE? struck through on 'whale', then DOLPHIN (THE BIGGEST) on 'dolphin'", "static", "whoosh")
def _(c):
    L = [orca("50%", "54%", 900, 340), TAG("WHALE?", 0.1, "38%", "18%", 52, accent=RED, w=360),
         SV(STRIKE, "38%", "18%", 300, 18, start=c.w("whale"), enter={"type": "wipeRight", "at": c.w("whale"), "duration": 0.25}, z=30),
         TAG("DOLPHIN (THE BIGGEST)", c.w("dolphin"), "64%", "18%", 48, accent=GREEN, w=660)]
    return dict(bg=ocean(14), layers=L, sfx=[sfx("whoosh", c.w("dolphin"))])


@shot("b06", "there's", "JOKE", "Two smaller grey dolphins shuffle in with name tags FALSE KILLER WHALE / PYGMY KILLER WHALE; YOU shrugs on 'nervous'; seam stamp BODY: YOU LOSE", "static", "pop; stamp tick")
def _(c):
    L = [orca("30%", "46%", 560, 210, silhouette="#7d8b92", start=c.w("false"), enter=pop(c.w("false"))),
         orca("62%", "56%", 340, 130, silhouette="#7d8b92", start=c.w("pygmy"), enter=pop(c.w("pygmy"))),
         TAG("FALSE KILLER WHALE", c.w("false"), "30%", "26%", 36, w=520), TAG("PYGMY KILLER WHALE", c.w("pygmy"), "62%", "40%", 36, w=520),
         CR("You", "84%", "62%", 150, 250, pose="shrug", start=c.w("nervous"), enter=pop(c.w("nervous"))),
         STAMP("BODY: YOU LOSE", c.le() + 0.15, "50%", "84%")]
    return dict(bg=ocean(14), layers=L, sfx=[sfx("pop", c.w("false")), sfx("pop", c.w("pygmy")), sfx("tick", c.le() + 0.15)])


# ---------------------------------------------------------------- R2 speed
@shot("s01", 0, "CARD", "Tab 2 lights; Headline COULD YOU OUTSWIM IT?; red NO. fills the frame on 'No' (held >= 0.8 s)", "static", "tick; impact")
def _(c):
    L = [HL("COULD YOU OUTSWIM IT?", 0.1, "30%", 72, out=c.w("No")), HL("NO.", c.w("No"), "50%", 200, "red", False)]
    return dict(bg=card(), layers=L, sfx=[sfx("impact", c.w("No"), 0.6)])


@shot("s02", 0, "INFO", "SpeedBars row ORCA ~56 km/h fills red; then a Car and an Orca cruise side by side past a 50 sign on 'speed'", "static", "whoosh")
def _(c):
    a = c.w("speed")
    L = [comp("explainer/SpeedBars", "50%", "32%", 1300, 300, {"title": "TOP SPEED", "max": 60, "at": 0.1, "duration": 0.7, "size": 44, "labelWidth": 380,
                                                            "rows": [{"label": "ORCA", "value": 56, "unit": "km/h", "color": "red"}]}),
         CR("Car", "20%", "76%", 380, 150, start=a, enter=pop(a), kf=[{"t": a, "x": "20%"}, {"t": c.d, "x": "70%", "ease": "linear"}]),
         orca("20%", "64%", 520, 190, start=a, enter=pop(a), kf=[{"t": a, "x": "18%"}, {"t": c.d, "x": "68%", "ease": "linear"}], speed=1.8),
         SV(LIMIT, "86%", "70%", 150, 150, start=a, enter=pop(a)), TAG("= YOUR CAR IN TOWN", a, "70%", "52%", 40, w=520)]
    return dict(bg=ocean(10), layers=L, sfx=[sfx("whoosh", a)])


@shot("s03", 0, "INFO", "SpeedBars: ORCA 56, OLYMPIC SWIMMER 8 on 'eight', YOU 3 on 'three'; YOU pose=panic beside the last bar", "static", "pop x2")
def _(c):
    rows = [{"label": "ORCA", "value": 56, "unit": "km/h", "color": "red"}, {"label": "OLYMPIC SWIMMER", "value": 8, "unit": "km/h", "color": CYAN},
            {"label": "YOU", "value": 3, "unit": "km/h", "color": WHITE}]
    L = [comp("explainer/SpeedBars", "50%", "46%", 1400, 560, {"title": "TOP SPEED", "max": 60, "duration": 0.5, "size": 44, "labelWidth": 420,
                                                            "stagger": max(0.4, c.w("three") - c.w("eight")), "at": max(0.0, 2 * c.w("eight") - c.w("three")), "rows": rows}),
         CR("You", "86%", "70%", 140, 230, pose="panic", start=c.w("three"), enter=pop(c.w("three")))]
    return dict(bg=ocean(10), layers=L, sfx=[sfx("pop", c.w("eight")), sfx("pop", c.w("three"))])


@shot("s04", 0, "INFO", "Stat counts 0 -> 130 KG on 'hundred' (label FOOD ON A BIG DAY)", "pushIn", "tick on count end")
def _(c):
    a = c.w("hundred")
    return dict(bg=ocean(10), layers=[STAT(130, "KG OF FOOD ON A BIG DAY", a, "50%", "46%", 170, **{"from": 0, "duration": 0.9, "suffix": " KG"}),
                                      orca("50%", "80%", 520, 190, idle=[{"type": "bob", "amount": 4, "speed": 0.4}])],
                camera=cam("pushIn", 0.3), sfx=[sfx("tick", a + 0.9)])


@shot("s04", "more", "INFO", "Two bars: FOOD / BIG DAY ~130 KG vs YOU ~75 KG", "static", "ding")
def _(c):
    rows = [{"label": "FOOD / BIG DAY", "value": 130, "unit": "kg", "color": "red"}, {"label": "YOU", "value": 75, "unit": "kg", "color": WHITE}]
    return dict(bg=ocean(10), layers=[comp("explainer/SpeedBars", "50%", "50%", 1400, 420, {"title": "WEIGHT", "max": 140, "at": 0.05, "duration": 0.5, "stagger": 0.35, "size": 46, "labelWidth": 440, "rows": rows})],
                sfx=[sfx("ding", 0.6)])


@shot("s05", 0, "JOKE", "NEW S diner order slip: SALMON/HERRING/SEAL/SHARK ticked, HUMAN empty; red stamp NEVER ORDERED on 'never'; seam stamp SPEED: NO CONTEST", "static", "stinger light")
def _(c):
    L = [SV(SLIP, "40%", "50%", 420, 560, enter=pop(0.05)), STAMP("NEVER ORDERED", c.w("never"), "42%", "72%"),
         STAMP("SPEED: NO CONTEST", c.le() + 0.15, "74%", "40%")]
    return dict(bg=card(), layers=L, sfx=[sfx("stinger", c.w("never"), 0.4), sfx("tick", c.le() + 0.15)])


# ---------------------------------------------------------------- R3 plan
@shot("pl01", 0, "MED", "Tab 3 lights; camera keyframes push from 1x to 2.6x onto the Orca's eye", "push to eye (keyframes)", "riser short")
def _(c):
    return dict(bg=ocean(16), layers=[orca("50%", "50%", 1100, 420, idle=False)], camera=cam_to(1290, 520, 2.6, 0.2, c.d), sfx=[sfx("riser", 0.1, 0.5)])


@shot("pl01", "It", "PUNCH", "Red IT PLANS. on black (>= 0.8 s)", "static", "impact", nth=2)
def _(c):
    return dict(bg=black(), layers=[HL("IT PLANS.", 0.0, "48%", 150, "red", False)], sfx=[sfx("impact", 0.05, 0.6)])


@shot("pl02", 0, "WIDE", "Pod of five Orca cruising, one large female in front, calves small; dotted family-tree lines link them; Tag PODS · LED BY GRANDMOTHERS on 'older'", "panRight", "underwater_rumble")
def _(c):
    L = [SV(PODTREE, "50%", "34%", 1200, 420, z=1, start=0.3, enter=fade(0.3))]
    for i, (x, y, s) in enumerate([(50, 26, 0.5), (26, 52, 0.38), (50, 52, 0.38), (74, 52, 0.38), (16, 74, 0.25), (34, 74, 0.25)]):
        L.append(orca(f"{x}%", f"{y}%", 900 * s, 330 * s, timeOffset=i * 0.37))
    L.append(TAG("PODS · LED BY GRANDMOTHERS", c.w("older"), "50%", "92%", 40, w=800))
    return dict(bg=ocean(14), layers=L, camera=cam("panRight", 0.3), sfx=[sfx("underwater_rumble", 0, 0.4)])


@shot("pl02", "and", "SPLIT", "Split screen with a wall: left pod + FISH icons, right pod + seal icons; Tag FISH EATERS | MAMMAL HUNTERS (North Pacific)", "static", "click x2")
def _(c):
    L = [{"type": "rect", "x": "50%", "y": "50%", "width": 10, "height": 760, "fill": "#8fb3c0", "z": 2},
         orca("25%", "48%", 520, 190), orca("75%", "48%", 520, 190, flipX=True),
         SV(FISH, "18%", "70%", 160, 66, start=c.w("fish"), enter=pop(c.w("fish"))), SV(FISH, "32%", "74%", 140, 58, start=c.w("fish") + 0.2, enter=pop(c.w("fish") + 0.2)),
         CR("Seal", "70%", "72%", 240, 100, start=c.w("mammals"), enter=pop(c.w("mammals"))),
         TAG("FISH EATERS", c.w("fish"), "25%", "20%", 44, accent=CYAN, w=480), TAG("MAMMAL HUNTERS", c.w("mammals"), "75%", "20%", 44, accent=RED, w=520),
         TAG("NORTH PACIFIC", 0.1, "50%", "90%", 32, w=360)]
    return dict(bg=ocean(14), layers=L, sfx=[sfx("click", c.w("fish")), sfx("click", c.w("mammals"))])


@shot("pl04", 0, "ACTION", "Fish eaters: two Orca with busy sound rings, FISH icons drift on unbothered; Tag FISH EATERS: NOISY", "static", "sonar_ping chirps")
def _(c):
    L = [orca("34%", "46%", 640, 240), orca("58%", "60%", 520, 190, timeOffset=0.5)] + ring_layers(560, 470, 0.1, c.d, 0.7, 3, 300)
    L += [SV(FISH, f"{70 + i * 7}%", f"{36 + i * 10}%", 150, 62, keyframes=[{"t": 0, "x": f"{70 + i * 7}%"}, {"t": c.d, "x": f"{64 + i * 7}%"}]) for i in range(3)]
    L += [TAG("FISH EATERS: NOISY", 0.1, "50%", "14%", 44, accent=CYAN, w=600)]
    return dict(bg=ocean(14), layers=L, sfx=[sfx("sonar_ping", 0.2, 0.4), sfx("sonar_ping", 1.2, 0.4)])


@shot("pl04", "Mammal", "ACTION", "Stalking pod: their sound rings go dark; a Seal on the right; Tag MAMMAL HUNTERS: SILENT on 'silence', then HUNT BY EAR + ear icon on 'listening'", "panLeft", "sonar_ping fades out")
def _(c):
    L = [orca("30%", "52%", 640, 240, speed=0.6), orca("16%", "66%", 520, 190, speed=0.6, timeOffset=0.4), CR("Seal", "80%", "40%", 280, 120)]
    L += ring_layers(600, 520, 0.0, min(1.2, c.d), 0.6, 2, 260)
    L += [TAG("MAMMAL HUNTERS: SILENT", c.w("silence"), "50%", "14%", 44, accent=RED, w=720),
          SV(EAR, "52%", "34%", 90, 120, start=c.w("listening"), enter=pop(c.w("listening"))), TAG("HUNT BY EAR", c.w("listening"), "50%", "86%", 44, accent=RED, w=480)]
    return dict(bg=ocean(18), layers=L, camera=cam("panLeft", 0.3), sfx=[sfx("sonar_ping", 0.1, 0.3)])


@shot("pl06", 0, "INFO", "ECG trace as a hydrophone strip: flat, red KILL marker, then busy calls; Tag CALLS: AFTER THE KILL", "static", "static burst at the marker")
def _(c):
    k = c.w("after")
    beats = [round(k + 0.25 * i, 2) for i in range(1, 30) if k + 0.25 * i < c.d]
    L = [comp("explainer/ECG", "50%", "50%", 1600, 300, {"beats": beats, "speed": 380, "color": CYAN, "at": 0.0, "prefill": True}),
         {"type": "rect", "x": "50%", "y": "50%", "width": 8, "height": 340, "fill": RED, "start": k, "enter": pop(k), "z": 5},
         TAG("KILL", k, "50%", "26%", 40, accent=RED, w=240), TAG("CALLS: AFTER THE KILL", k + 0.3, "50%", "80%", 44, w=640)]
    return dict(bg=card(), layers=L, sfx=[sfx("static", k, 0.3)])


@shot("pl07", 0, "CALLBACK", "Return to the hook hull frame: rings ripple, then stop dead on 'silence'", "pushIn", "sonar_ping x1 then silence")
def _(c):
    s = c.w("silence")
    return dict(bg=surface(0.38, depth=10), layers=[kayak_at("50%", 0.38 * H, 900)] + ring_layers(960, 640, 0.1, s, 0.8, 3, 360),
                camera=cam("pushIn", 0.4), sfx=[sfx("sonar_ping", 0.1, 0.5)])


@shot("pl08", 0, "PUNCH", "Two-line card: NOISY = OFF DUTY (green), then QUIET = AT WORK (red) on 'Quiet'", "static", "heartbeat_slow x2")
def _(c):
    q = c.w("Quiet")
    return dict(bg=black(), layers=[HL("NOISY = OFF DUTY", 0.05, "38%", 84, "green", False), HL("QUIET = AT WORK", q, "60%", 96, "red", False)],
                sfx=[sfx("heartbeat_slow", q, 0.6)])


@shot("pl09", 0, "MAP", "Map world -> South America (zoom 3), pin Peninsula Valdes (-64.0,-42.5); Tag ARGENTINA", "static (map zoom)", "click")
def _(c):
    return dict(bg=ocean(40), layers=[comp("explainer/Map", "50%", "50%", W, H, {"views": [{"t": 0, "lon": -40, "lat": -20, "zoom": 1.4}, {"t": 1.2, "lon": -62, "lat": -40, "zoom": 3}],
                                                                                 "pins": [{"lon": -64.0, "lat": -42.5, "at": 0.8, "label": "Valdés"}], "labelSize": 40, "pinSize": 1.4}, depth=0),
                                      TAG("ARGENTINA", 0.4, "50%", "10%", 44, w=420)], sfx=[sfx("click", 0.8)])


@shot("pl09", "orcas", "ACTION", "Side view: beige beach strip with foam; Orca surges up the sand to a Seal (sea lion stand-in), then slides back out on 'slide'; credential 1 tick", "panRight", "whoosh_long")
def _(c):
    s = c.w("slide")
    L = [SV(BEACH, "50%", "80%", 1920, 320, z=1), CR("Seal", "62%", "62%", 240, 100, end=s + 0.3),
         orca("30%", "70%", 640, 240, [{"t": 0, "x": "20%", "y": "72%", "rotate": 0}, {"t": max(0.5, s - 0.6), "x": "54%", "y": "62%", "rotate": -8},
                                       {"t": c.d, "x": "24%", "y": "74%", "rotate": -4}]),
         TAG("1  BEACH RAIDS ✓", 0.2, "50%", "14%", 44, accent=RED, w=560)]
    return dict(bg=surface(0.45, DAY), layers=L, camera=cam("panRight", 0.3), sfx=[sfx("whoosh_long", 0.1)])


@shot("pl10", 0, "MAP", "Map pin Crozet Islands (51.0,-46.4) at zoom 3; Tag CROZET ISLANDS", "static", "click")
def _(c):
    return dict(bg=ocean(40), layers=[comp("explainer/Map", "50%", "50%", W, H, {"views": [{"t": 0, "lon": 30, "lat": -40, "zoom": 2}, {"t": 1.0, "lon": 51, "lat": -46, "zoom": 3}],
                                                                                 "pins": [{"lon": 51.0, "lat": -46.4, "at": 0.6, "label": "Crozet"}], "labelSize": 40, "pinSize": 1.4}, depth=0),
                                      TAG("CROZET ISLANDS", 0.3, "50%", "10%", 44, w=520)], sfx=[sfx("click", 0.6)])


@shot("pl10", "mothers", "MED", "A big Orca nudges a small Orca up the same beach; dotted practice arrow", "static", "pop")
def _(c):
    L = [SV(BEACH, "50%", "80%", 1920, 320, z=1), orca("36%", "70%", 640, 240, [{"t": 0, "x": "28%"}, {"t": c.d, "x": "36%"}]),
         orca("54%", "64%", 320, 120, [{"t": 0, "x": "44%", "y": "68%"}, {"t": c.d, "x": "56%", "y": "62%"}]),
         SV(ARROW, "62%", "48%", 300, 60, start=0.4, enter=fade(0.4), rotate=-10), TAG("MOTHER + CALF", 0.3, "50%", "14%", 44, w=480)]
    return dict(bg=surface(0.45, DAY), layers=L, sfx=[sfx("pop", 0.4)])


@shot("pl10", "calves", "MED", "The calf alone rehearsing on an empty beach (no prey); Tag BEACH SCHOOL; seam stamp PLAN: IT THINKS AHEAD", "static", "stamp tick", nth=2)
def _(c):
    L = [SV(BEACH, "50%", "80%", 1920, 320, z=1), orca("50%", "64%", 320, 120, [{"t": 0, "x": "40%", "y": "68%"}, {"t": c.d * 0.6, "x": "56%", "y": "62%"}, {"t": c.d, "x": "46%", "y": "68%"}]),
         TAG("BEACH SCHOOL", 0.1, "50%", "14%", 52, accent=YEL, w=520), STAMP("PLAN: IT THINKS AHEAD", c.le() + 0.15, "70%", "36%")]
    return dict(bg=surface(0.45, DAY), layers=L, sfx=[sfx("tick", c.le() + 0.15)])


# ---------------------------------------------------------------- R4 wave
@shot("w01", 0, "WIDE", "Tab 4 lights; icy palette; ice floe (reused pilot ICE markup) on the waterline, a Seal hauls up onto it; Tag ANTARCTICA", "pullOut", "underwater_rumble")
def _(c):
    L = [SV(ICE, "56%", "47%", 560, 224, z=2), CR("Seal", "56%", "42%", 260, 110, kf=[{"t": 0, "y": "56%", "rotate": -20}, {"t": min(2.0, c.d * 0.6), "y": "40%", "rotate": 0}]),
         TAG("ANTARCTICA", 0.1, "50%", "12%", 44, w=420), TAG("SAFE ON ICE? ✓", c.w("Smart"), "50%", "84%", 44, accent=GREEN, w=520)]
    return dict(bg=surface(0.5, ICY, depth=6), layers=L, camera=cam("pullOut", 0.3), sfx=[sfx("underwater_rumble", 0, 0.4)])


@shot("w02", 0, "MED", "Two Orca spy-hop (rotated vertical, heads above the waterline) beside the floe; Tag THEY CHECK FIRST on 'look'", "pushIn", "bubbles")
def _(c):
    L = [SV(ICE, "64%", "47%", 560, 224, z=2), CR("Seal", "64%", "42%", 260, 110),
         orca("28%", "52%", 520, 190, [{"t": 0, "y": "70%"}, {"t": c.w("lifts"), "y": "70%"}, {"t": c.w("lifts") + 0.6, "y": "50%", "ease": "out"}], rotate=-80),
         orca("40%", "56%", 460, 170, [{"t": 0, "y": "74%"}, {"t": c.w("lifts") + 0.3, "y": "74%"}, {"t": c.w("lifts") + 0.9, "y": "54%", "ease": "out"}], rotate=-78, timeOffset=0.4),
         TAG("THEY CHECK FIRST", c.w("look"), "50%", "12%", 52, accent=RED, w=600)]
    return dict(bg=surface(0.5, ICY, depth=6), layers=L, camera=cam("pushIn", 0.3), sfx=[sfx("bubbles", c.w("lifts"), 0.5)])


@shot("w03", 0, "INFO", "Three seal cards (one Seal figure tinted three greys) WEDDELL / CRABEATER / LEOPARD; red ring stays on WEDDELL", "static", "click")
def _(c):
    L = []
    for i, (lab, col) in enumerate([("WEDDELL", "#8a98a0"), ("CRABEATER", "#c7cdd0"), ("LEOPARD", "#5c666b")]):
        x = f"{25 + i * 25}%"
        L += [{"type": "rect", "x": x, "y": "52%", "width": 420, "height": 440, "fill": "#14262f", "stroke": "#3d5966", "strokeWidth": 3, "radius": 16},
              CR("Seal", x, "50%", 320, 140, silhouette=col), TAG(lab, 0.1 + i * 0.2, x, "72%", 36, w=380)]
    L.append({"type": "circle", "x": "25%", "y": "52%", "width": 470, "height": 470, "fill": "rgba(0,0,0,0)", "stroke": RED, "strokeWidth": 10, "start": c.w("Weddell"), "enter": pop(c.w("Weddell")), "z": 6})
    L.append(TAG("EASIER TO FIND", c.w("easier"), "50%", "88%", 34, accent=GREY, w=440))
    return dict(bg=card(), layers=L, sfx=[sfx("click", c.w("Weddell"))])


@shot("w04", 0, "ACTION", "Side view: four Orca abreast (same scale) back off left, then charge the floe left to right on 'charges'", "panRight", "whoosh_long")
def _(c):
    ch = c.w("charges")
    L = [SV(ICE, "78%", "47%", 520, 208, z=2), CR("Seal", "78%", "42%", 240, 100)]
    for i in range(4):
        y = 56 + i * 7
        L.append(orca("40%", f"{y}%", 420, 150, [{"t": 0, "x": "40%"}, {"t": ch, "x": "16%"}, {"t": c.d, "x": "54%", "ease": "in"}], timeOffset=i * 0.1, speed=1.6))
    return dict(bg=surface(0.5, ICY, depth=6), layers=L, camera=cam("panRight", 0.3), sfx=[sfx("whoosh_long", ch)])


@shot("w04", "At", "ACTION", "Orcas dip below; NEW S wave crest band sweeps over the floe; the Seal slides off into the water; Tag WAVE-WASHING", "shake medium x1", "impact + bubbles")
def _(c):
    r = c.w("rolls")
    L = [SV(ICE, "70%", "47%", 520, 208, z=2),
         CR("Seal", "70%", "42%", 240, 100, kf=[{"t": 0, "x": "70%", "y": "42%", "rotate": 0}, {"t": r + 0.3, "x": "70%", "y": "42%"}, {"t": c.w("tips") + 0.4, "x": "82%", "y": "60%", "rotate": 40, "ease": "in"}]),
         SV(WAVE, "20%", "44%", 900, 300, z=3, keyframes=[{"t": 0, "x": "-20%", "opacity": 0}, {"t": r, "x": "30%", "opacity": 1}, {"t": r + 1.0, "x": "80%", "opacity": 0.9}, {"t": c.d, "x": "120%", "opacity": 0}])]
    for i in range(4):
        L.append(orca("50%", f"{58 + i * 7}%", 420, 150, [{"t": 0, "x": "40%", "y": f"{58 + i * 7}%"}, {"t": 0.8, "x": "52%", "y": f"{68 + i * 7}%", "opacity": 0.6}], timeOffset=i * 0.1))
    L.append(TAG("WAVE-WASHING", r, "50%", "12%", 52, accent=RED, w=560))
    return dict(bg=surface(0.5, ICY, depth=6), layers=L, camera={"shake": [shake(r + 0.3, 14)]}, sfx=[sfx("impact", r + 0.3, 0.6), sfx("bubbles", c.w("tips"))])


@shot("w06", 0, "ACTION", "Pod resets; corner Tags ATTEMPT 2 -> ATTEMPT 3 on 'again'", "static", "tick x2")
def _(c):
    L = [SV(ICE, "76%", "47%", 520, 208, z=2), CR("Seal", "76%", "42%", 240, 100)]
    L += [orca("30%", f"{58 + i * 8}%", 420, 150, [{"t": 0, "x": "50%"}, {"t": c.d, "x": "22%"}], flipX=True, timeOffset=i * 0.2) for i in range(3)]
    L += [TAG("ATTEMPT 2", 0.1, "14%", "12%", 40, w=320, end=c.w("again")), TAG("ATTEMPT 3", c.w("again"), "14%", "12%", 40, accent=RED, w=320)]
    return dict(bg=surface(0.5, ICY, depth=6), layers=L, sfx=[sfx("tick", 0.1), sfx("tick", c.w("again"))])


@shot("w06", "seal", "PUNCH", "Empty floe, red stamp NOT SAFE. SERVED. on 'served'", "static", "stinger light")
def _(c):
    return dict(bg=surface(0.5, ICY, depth=6), layers=[SV(ICE, "50%", "47%", 640, 256, z=2), HL("NOT SAFE.", 0.05, "18%", 80, "white", False),
                                                     STAMP("SERVED.", c.w("served"), "50%", "66%", size=72, rot=-6)], sfx=[sfx("stinger", c.w("served"), 0.4)])


@shot("w07", 0, "CALLBACK", "Re-immersion (~36%): the hook kayak on the same icy-to-dusk waterline; four fins line up in the distance", "pushIn", "heartbeat x3")
def _(c):
    L = [kayak_at("44%", WL, 620)] + fins([1360, 1480, 1600, 1720], WL, 110, kf_x=[(0, [1500, 1600, 1700, 1800]), (c.d, [1300, 1420, 1540, 1660])])
    return dict(bg=surface(0.5, DUSK), layers=L, camera=cam("pushIn", 0.5), sfx=[sfx("heartbeat", 0.4, 0.5)])


@shot("w07", "Look", "PUNCH", "Hard cut: floe+seal (left) and kayak+YOU (right) with the same dashed outline; Headline LOOK FAMILIAR?; seam stamp WAVE: NOWHERE IS SAFE", "static", "impact")
def _(c):
    L = [SV(ICE, "28%", "50%", 560, 224, z=2), CR("Seal", "28%", "45%", 240, 100), SV(OUTLINE, "28%", "52%", 600, 220, z=6),
         kayak_at("72%", 0.52 * H, 600), SV(OUTLINE, "72%", 0.52 * H - (KAYAK_WL - 0.5) * 220, 600, 220, z=6),
         HL("LOOK FAMILIAR?", 0.05, "16%", 80), STAMP("WAVE: NOWHERE IS SAFE", c.le() + 0.15, "50%", "84%")]
    return dict(bg=surface(0.5, DUSK), layers=L, sfx=[sfx("impact", 0.05, 0.5), sfx("tick", c.le() + 0.15)])


# ---------------------------------------------------------------- R5 sharks
@shot("k01", 0, "CARD", "Tab 5 lights; GreatWhite crosses the frame", "panRight", "whoosh")
def _(c):
    return dict(bg=ocean(16), layers=[CR("GreatWhite", "50%", "52%", 760, 300, [{"t": 0, "x": "20%"}, {"t": c.d, "x": "70%", "ease": "linear"}])], sfx=[sfx("whoosh", 0)])


@shot("k02", 0, "MAP", "Map South Africa (zoom 3.5), pin Gansbaai (19.35,-34.58); Tags MAY 2017 and 3 GREAT WHITES IN ONE WEEK on 'three'", "pushIn (map zoom)", "drone")
def _(c):
    return dict(bg=ocean(40), layers=[comp("explainer/Map", "50%", "50%", W, H, {"views": [{"t": 0, "lon": 22, "lat": -28, "zoom": 2.5}, {"t": 1.4, "lon": 20, "lat": -33, "zoom": 3.5}],
                                                                                 "pins": [{"lon": 19.35, "lat": -34.58, "at": c.w("Gansbaai"), "label": "Gansbaai"}], "labelSize": 40, "pinSize": 1.4}, depth=0),
                                      TAG("MAY 2017", c.w("May"), "22%", "12%", 44, w=360), TAG("3 GREAT WHITES IN ONE WEEK", c.w("three"), "60%", "12%", 44, accent=RED, w=760)],
                sfx=[sfx("drone", 0, 0.4)])


@shot("k03", 0, "INFO", "Grey GreatWhite belly-up; NEW S liver overlay (kit Liver) flashes red then empties on 'liver'; small HEART icon fades on 'heart' (at least one)", "static", "click x2")
def _(c):
    li, he = c.w("liver"), c.w("heart")
    L = [comp("explainer/GreatWhite", "50%", "50%", 1100, 420, {"silhouette": "#9aa7ad", "idle": False}, keyframes=[{"t": 0, "scaleY": -1}]),
         CR("Liver", "44%", "54%", 220, 160, kf=[{"t": 0, "opacity": 0}, {"t": li, "opacity": 1}, {"t": li + 0.9, "opacity": 1}, {"t": li + 1.4, "opacity": 0.15}], shadow="0 0 22px #e5483d"),
         SV(HEART, "36%", "50%", 90, 80, keyframes=[{"t": 0, "opacity": 0}, {"t": he, "opacity": 1}, {"t": he + 0.8, "opacity": 0.15}]),
         TAG("LIVER: GONE", li, "30%", "16%", 44, accent=RED, w=440), TAG("HEART: GONE (AT LEAST 1)", he, "68%", "16%", 40, accent=RED, w=660)]
    return dict(bg=ocean(18), layers=L, sfx=[sfx("click", li), sfx("click", he)])


@shot("k04", 0, "INFO", "Mugshot frames: two Orca silhouettes with NEW S bent-fin overlays (left / right) and height lines; name tags on their words", "static", "pop x2")
def _(c):
    L = []
    for x, fin, nm in (("30%", FIN_PORT, "Port"), ("70%", FIN_STAR, "Starboard")):
        L += [{"type": "rect", "x": x, "y": "52%", "width": 640, "height": 560, "fill": "#14262f", "stroke": "#8fb3c0", "strokeWidth": 4, "radius": 10},
              SV(_svg("0 0 640 560", "".join(f'<line x1="0" y1="{40 + i * 80}" x2="640" y2="{40 + i * 80}" stroke="#3d5966" stroke-width="3"/>' for i in range(7))), x, "52%", 640, 560, z=1),
              orca(x, "60%", 560, 210, silhouette="#1b2328", finScale=0.4), SV(fin, f"{float(x[:-1]) - 1.5}%", "45%", 120, 104, z=3),
              TAG(nm.upper(), c.w(nm), x, "84%", 44, accent=RED, w=440)]
    return dict(bg=card(), layers=L, sfx=[sfx("pop", c.w("Port")), sfx("pop", c.w("Starboard"))])


@shot("k05", 0, "INFO", "GreatWhite cutaway; kit Liver scaled to ~25% of the body in yellow-red; oil-drop on 'oil'; Tag LIVER ≈ 1/4 OF THE BODY", "pushIn", "ding")
def _(c):
    q = c.w("quarter")
    L = [CR("GreatWhite", "50%", "50%", 1200, 460, silhouette="#7f9099", idle=False),
         CR("Liver", "46%", "54%", 360, 220, kf=[{"t": 0, "scale": 0.3, "opacity": 0}, {"t": q, "scale": 0.3, "opacity": 1}, {"t": q + 0.6, "scale": 1.0, "opacity": 1, "ease": "backOut"}]),
         TAG("LIVER ≈ 1/4 OF THE BODY", q, "50%", "14%", 46, w=700), TAG("OIL", c.w("oil"), "62%", "80%", 44, accent=YEL, w=240)]
    return dict(bg=ocean(16), layers=L, camera=cam("pushIn", 0.3), sfx=[sfx("ding", q + 0.4)])


@shot("k06", 0, "JOKE", "Kit Car with its fuel cap open; an Orca swims off with a NEW S yellow jerrycan in lockstep; Tag TAKE THE TANK. LEAVE THE CAR.", "static", "whoosh")
def _(c):
    a = c.w("orcas")
    kf_o = [{"t": 0, "x": "56%"}, {"t": a, "x": "56%"}, {"t": c.d, "x": "96%", "ease": "in"}]
    kf_j = [{"t": 0, "x": "61%"}, {"t": a, "x": "61%"}, {"t": c.d, "x": "101%", "ease": "in"}]
    L = [CR("Car", "26%", "64%", 560, 230, color="#d8d8d8"), orca("56%", "40%", 640, 240, kf_o), SV(JERRY, "61%", "52%", 110, 140, keyframes=kf_j, z=4),
         TAG("TAKE THE TANK. LEAVE THE CAR.", a, "50%", "86%", 46, accent=YEL, w=900)]
    return dict(bg=ocean(10), layers=L, sfx=[sfx("whoosh", a)])


@shot("k07", 0, "INFO", "GreatWhite rolls 180 degrees (rotate keyframe); Tag TONIC IMMOBILITY? on 'tonic', yellow UNCONFIRMED on 'unconfirmed' (honesty hedge)", "static", "underwater_rumble")
def _(c):
    t = c.w("flip")
    L = [CR("GreatWhite", "50%", "50%", 1000, 380, [{"t": 0, "rotate": 0}, {"t": t, "rotate": 0}, {"t": t + 1.2, "rotate": 180, "ease": "inOut"}], idle=False),
         TAG("TONIC IMMOBILITY?", c.w("tonic"), "50%", "14%", 48, w=620), TAG("UNCONFIRMED", c.w("unconfirmed"), "50%", "84%", 48, accent=YEL, bg=YEL, color=INK, w=480)]
    return dict(bg=ocean(20), layers=L, sfx=[sfx("underwater_rumble", 0, 0.4)])


@shot("k08", 0, "INFO", "Timer ring 0:00 -> 1:59 runs fast beside an Orca and a smaller young GreatWhite (~2.5 m); Tag 2023 · ONE ORCA · < 2 MIN", "static", "clock_ticking then stinger")
def _(c):
    L = [orca("30%", "46%", 640, 240, pxPerM=70), CR("GreatWhite", "34%", "70%", 260, 100, pxPerM=70, flipX=True),
         comp("explainer/Timer", "74%", "50%", 420, 420, {"from": 0, "to": 119, "at": c.w("killing"), "rate": 40, "style": "ring", "format": "mm:ss", "label": "SOLO KILL"}),
         TAG("2023 · ONE ORCA · < 2 MIN", c.w("2023"), "50%", "12%", 44, accent=RED, w=760)]
    return dict(bg=ocean(16), layers=L, sfx=[sfx("clock_ticking", c.w("killing"), 0.5)])


@shot("k08", "less", "INFO", "YOU with a NEW S toothbrush; the same Timer ring reads 2:00; Tag LESS THAN YOUR TOOTHBRUSHING", "static", "ding")
def _(c):
    L = [CR("You", "36%", "56%", 220, 380, pose="stand"), SV(BRUSH, "40%", "40%", 200, 40, idle=[{"type": "jitter", "amount": 6, "speed": 4}]),
         comp("explainer/Timer", "70%", "50%", 420, 420, {"from": 120, "to": 120, "at": 0, "rate": 0, "style": "ring", "format": "mm:ss", "label": "BRUSHING"}),
         TAG("LESS THAN YOUR TOOTHBRUSHING", 0.2, "50%", "12%", 44, w=820)]
    return dict(bg=card(), layers=L, sfx=[sfx("ding", 0.3)])


@shot("k09", 0, "MAP", "Map pin Gansbaai; three shark icons fade out one by one; Tag GREAT WHITES: GONE on 'left'", "pullOut", "whoosh reverse")
def _(c):
    lft = c.w("left")
    L = [comp("explainer/Map", "50%", "50%", W, H, {"views": [{"t": 0, "lon": 20, "lat": -33, "zoom": 3.5}], "pins": [{"lon": 19.35, "lat": -34.58, "at": 0, "label": "Gansbaai"}], "labelSize": 40}, depth=0)]
    L += [CR("GreatWhite", f"{60 + i * 8}%", f"{62 + i * 6}%", 200, 80, silhouette="#c7d2d6", kf=[{"t": 0, "opacity": 1}, {"t": lft + i * 0.35, "opacity": 1}, {"t": lft + i * 0.35 + 0.3, "opacity": 0}], depth=0, z=31) for i in range(3)]
    L += [TAG("GREAT WHITES: GONE", lft, "50%", "10%", 46, accent=RED, w=600)]
    return dict(bg=ocean(40), layers=L, camera=cam("pullOut", 0.2), sfx=[sfx("whoosh", lft)])


@shot("k09", "so", "MED", "NEW S shark cage with a Diver (YOU) inside, empty blue water; Tag SIGHTINGS: 0", "static", "bubbles")
def _(c):
    L = [SV(CAGE, "50%", "52%", 440, 440, z=2), CR("Diver", "50%", "52%", 360, 140, arms="side", idle=[{"type": "float", "amount": 6, "speed": 0.3}]),
         TAG("SIGHTINGS: 0", c.w("empty"), "50%", "12%", 48, w=440)]
    return dict(bg=ocean(12), layers=L, sfx=[sfx("bubbles", 0.3, 0.4)])


@shot("k11", 0, "JOKE", "GreatWhite with a NEW S cardboard box strapped on (lockstep keyframes) swims off left; Tag MOVING HOUSE; seam stamp SHARKS: EVEN THEY LEAVE", "panLeft", "pop; stamp tick")
def _(c):
    kf = [{"t": 0, "x": "70%"}, {"t": c.d, "x": "6%", "ease": "linear"}]
    kfb = [{"t": 0, "x": "71%"}, {"t": c.d, "x": "7%", "ease": "linear"}]
    L = [CR("GreatWhite", "70%", "52%", 760, 300, kf, flipX=True), SV(BOX, "71%", "38%", 180, 135, keyframes=kfb, z=4),
         TAG("MOVING HOUSE", c.w("moving"), "50%", "14%", 50, accent=YEL, w=520), STAMP("SHARKS: EVEN THEY LEAVE", c.le() + 0.15, "66%", "82%")]
    return dict(bg=ocean(12), layers=L, sfx=[sfx("pop", c.w("moving")), sfx("tick", c.le() + 0.15)])


# ---------------------------------------------------------------- R6 giants
@shot("g01", 0, "CARD", "Tab 6 lights; Headline THINK BEING HUGE WOULD SAVE YOU?", "static", "riser short")
def _(c):
    return dict(bg=card(), layers=[HL("THINK BEING HUGE\nWOULD SAVE YOU?", 0.05, "46%", 84)], sfx=[sfx("riser", 0, 0.4)])


@shot("g02", 0, "MAP", "Map Australia (zoom 3), pin Bremer Bay (119.4,-34.4); Tag MARCH 2019", "static (map zoom)", "click")
def _(c):
    return dict(bg=ocean(40), layers=[comp("explainer/Map", "50%", "50%", W, H, {"views": [{"t": 0, "lon": 130, "lat": -25, "zoom": 2}, {"t": 1.2, "lon": 120, "lat": -33, "zoom": 3}],
                                                                                 "pins": [{"lon": 119.4, "lat": -34.4, "at": c.w("Bremer"), "label": "Bremer Bay"}], "labelSize": 40, "pinSize": 1.4}, depth=0),
                                      TAG("MARCH 2019", c.w("March"), "50%", "10%", 44, w=420)], sfx=[sfx("click", c.w("Bremer"))])


BW_PPM = 80
BW_FIG = 28.0  # kit BlueWhale is drawn as a 28 m animal: scale its pxPerM by 20/28 so it reads as the ~20 m adult


@shot("g02", "more", "SCALE", "BlueWhale drawn at 20 m (its pxPerM = 80 x 20/28) with 12 small Orca at 80 px/m swarming; ScaleBar ~20 M on 'twenty'", "panRight", "underwater_rumble + impact")
def _(c):
    L = [CR("BlueWhale", "50%", "46%", 1800, 400, pxPerM=BW_PPM * 20 / BW_FIG)]
    L += [orca(f"{18 + (i % 6) * 13}%", f"{30 + (i // 6) * 34}%", 8 * BW_PPM + 40, 260, pxPerM=BW_PPM * 0.5, timeOffset=i * 0.23) for i in range(12)]
    L += [comp("explainer/ScaleBar", "50%", "82%", 20 * BW_PPM, 110, {"label": "~20 M", "at": c.w("twenty"), "labelSize": 44})]
    return dict(bg=ocean(30), layers=L, camera=cam("panRight", 0.2), sfx=[sfx("underwater_rumble", 0, 0.4), sfx("impact", c.w("brought"), 0.4)])


@shot("g03", 0, "SCALE", "Same whale scale; eleven YOU figures lying head to toe beneath it pop in left to right; Tag ≈ 11 OF YOU", "static", "pop x11 (soft)")
def _(c):
    L = [CR("BlueWhale", "50%", "40%", 1800, 400, pxPerM=BW_PPM * 20 / BW_FIG)]
    span = c.w("match") - c.w("Line")
    for i in range(11):
        at = c.w("Line") + span * i / 11
        L.append(CR("You", f"{50 - 5 * 1.75 * BW_PPM / W * 100 + i * 1.75 * BW_PPM / W * 100:.2f}%", "76%", 60, 1.75 * BW_PPM, pxPerM=BW_PPM, rotate=90, start=at, enter=pop(at, 0.2)))
    L.append(TAG("≈ 11 OF YOU", c.w("match"), "50%", "92%", 44, w=420))
    return dict(bg=ocean(30), layers=L, sfx=[sfx("pop", c.w("Line"), 0.4), sfx("ding", c.w("match"))])


@shot("g04", 0, "ACTION", "Three-step tactic on the whale: Tags BITE (fins) on 'biting', FLANKS on 'flanks', PUSH UNDER on 'pushing' as the whale is pressed down", "static", "impact x3")
def _(c):
    p = c.w("pushing")
    L = [CR("BlueWhale", "50%", "44%", 1800, 400, [{"t": 0, "y": "44%"}, {"t": p, "y": "44%"}, {"t": c.d, "y": "56%", "ease": "inOut"}], pxPerM=BW_PPM * 20 / BW_FIG)]
    L += [orca(f"{30 + i * 14}%", f"{30 + (i % 2) * 30}%", 340, 130, timeOffset=i * 0.3) for i in range(4)]
    L += [TAG("BITE THE FINS", c.w("biting"), "22%", "12%", 40, accent=RED, w=420), TAG("RAM THE FLANKS", c.w("flanks"), "50%", "12%", 40, accent=RED, w=440),
          TAG("PUSH IT UNDER", p, "78%", "12%", 40, accent=RED, w=440)]
    return dict(bg=ocean(30), layers=L, sfx=[sfx("impact", c.w(w), 0.4) for w in ("biting", "flanks", "pushing")])


@shot("g05", 0, "INFO", "Three tally cards stamp in: 2019 ADULT on 'first', 2019 CALF on 'twice', 2021 YOUNG on 'young'", "static", "click x3")
def _(c):
    L = [STAMP("2019 · ADULT", c.w("first"), "24%", "50%", color=RED, rot=-4), STAMP("2019 · CALF", c.w("twice"), "50%", "50%", color="#a33a31", rot=3),
         STAMP("2021 · YOUNG", c.w("young"), "76%", "50%", color="#a33a31", rot=-3), TAG("FIRST EVER DOCUMENTED", c.w("documented"), "50%", "20%", 44, w=680)]
    return dict(bg=card(), layers=L, sfx=[sfx("click", c.w(w)) for w in ("first", "twice", "young")])


@shot("g06", 0, "INFO", "Orca centred; GreatWhite, BlueWhale and SpermWhale icons ring it with grey crosses; Headline NO UPPER LIMIT, Tag NO NATURAL PREDATOR on 'nothing'", "static", "click x3")
def _(c):
    n = c.w("nothing")
    L = [orca("50%", "54%", 640, 240), HL("NO UPPER LIMIT", 0.05, "14%", 72)]
    for i, (nm, x, y) in enumerate([("GreatWhite", "18%", "40%"), ("SpermWhale", "82%", "40%"), ("GreatWhite", "50%", "86%")]):
        L += [CR(nm, x, y, 340, 130, silhouette="#5c6b71", start=n + i * 0.2, enter=pop(n + i * 0.2)),
              TAG("✕", n + i * 0.2 + 0.2, x, y, 60, accent=GREY, w=120)]
    L.append(TAG("NOTHING HUNTS IT", n, "50%", "28%", 44, accent=RED, w=560))
    return dict(bg=ocean(16), layers=L, sfx=[sfx("click", n + i * 0.2) for i in range(3)])


@shot("g06", "Which", "PUNCH", "A small YOU with Tag ~75 KG; red Headline SO WHY NOT YOU? (master question re-armed); seam stamp GIANTS: NO UPPER LIMIT", "pushIn", "stinger soft")
def _(c):
    L = [CR("You", "50%", "58%", 200, 330, pose="shrug"), TAG("~75 KG", c.w("seventy"), "64%", "46%", 40, w=260), HL("SO WHY NOT YOU?", c.w("exception"), "16%", 84, "red", False),
         STAMP("GIANTS: NO UPPER LIMIT", c.le() + 0.15, "50%", "86%")]
    return dict(bg=card(), layers=L, camera=cam("pushIn", 0.3), sfx=[sfx("stinger", c.w("exception"), 0.3), sfx("tick", c.le() + 0.15)])


# ---------------------------------------------------------------- proof
@shot("pr01", 0, "CARD", "Red Headline HAS IT EVER TRIED IT ON A HUMAN? over a dark frame; chip shows all six tabs lit", "pushIn", "drone")
def _(c):
    return dict(bg=black(), layers=[HL("HAS IT EVER TRIED IT\nON A HUMAN?", 0.05, "46%", 84)], camera=cam("pushIn", 0.3), sfx=[sfx("drone", 0, 0.4)])


@shot("pr02", 0, "INFO", "Tag BITES & BUMPS: A HANDFUL; Stat 0 DEATHS on 'deaths'", "static", "pop")
def _(c):
    return dict(bg=card(), layers=[TAG("BITES & BUMPS ON RECORD: A HANDFUL", 0.1, "50%", "28%", 46, w=980), STAT(0, "DEATHS", c.w("deaths"), "50%", "60%", 150)],
                sfx=[sfx("pop", c.w("deaths"))])


@shot("pr02", "The", "STORY", "NEW S sepia diary page dated Jan. 1911 opens; warm paper background", "pushIn", "breath", nth=1)
def _(c):
    return dict(bg=sepia(), layers=[SV(DIARY, "50%", "52%", 1050, 720, enter=pop(0.05, 0.4)), TAG("THE CLOSEST CALL", 0.2, "50%", "10%", 44, accent="#7a5a2a", w=560)],
                camera=cam("pushIn", 0.3), sfx=[sfx("breath", 0.2, 0.4)])


@shot("pr03", 0, "STORY", "Sepia: a distinct sepia figure with a box camera on tripod (NOT the YOU icon) on a white ice sheet; dark fins beyond; Tag 2 SLED DOGS NEARBY; Tag ANTARCTICA · JANUARY 1911", "drift", "breath")
def _(c):
    L = [{"type": "rect", "x": "50%", "y": "74%", "width": W * 1.2, "height": 420, "fill": "#f4f1e8", "z": 1},
         SV(PONTING, "40%", "56%", 220, 300, z=3), TAG("ANTARCTICA · JANUARY 1911", 0.1, "50%", "10%", 44, accent="#7a5a2a", w=760),
         TAG("2 SLED DOGS NEARBY", c.w("Ponting"), "20%", "88%", 34, accent="#7a5a2a", w=480)]
    L += [SV(FIN, f"{70 + i * 8}%", "46%", 70, 98, z=2, opacity=0.8) for i in range(3)]
    return dict(bg=sepia(), layers=L, camera=cam("drift", 0.3), sfx=[sfx("breath", 0.4, 0.4)])


@shot("pr04", 0, "ACTION", "The ice sheet splits into three slabs on 'split'; dark Orca backs rise under the cracks; heavy shake", "shake heavy x2", "impact + boom")
def _(c):
    s = c.w("split")
    L = []
    for i, (x, dx, rot) in enumerate([(26, -4, -6), (50, 0, 3), (74, 4, 7)]):
        L.append(SV(_svg("0 0 640 420", '<path d="M0 30 L640 0 L640 420 L0 420 Z" fill="#f4f1e8"/>'), f"{x}%", "76%", 650, 420, z=1,
                    keyframes=[{"t": 0, "x": f"{x}%", "rotate": 0}, {"t": s, "x": f"{x}%", "rotate": 0}, {"t": s + 0.5, "x": f"{x + dx}%", "rotate": rot, "ease": "out"}]))
    L += [orca(f"{38 + i * 24}%", "64%", 420, 150, [{"t": 0, "y": "80%", "opacity": 0}, {"t": s, "y": "80%", "opacity": 0}, {"t": s + 0.6, "y": "62%", "opacity": 1, "ease": "out"}], silhouette="#1b1510", z=2) for i in range(2)]
    L += [SV(PONTING, "40%", "54%", 200, 270, z=3, keyframes=[{"t": 0, "rotate": 0}, {"t": s, "rotate": 0}, {"t": s + 0.4, "rotate": -10}]), TAG("THE ICE CRACKS", s, "50%", "10%", 48, accent=RED, w=520)]
    return dict(bg=sepia(), layers=L, camera={"shake": [shake(s, 26, 0.5), shake(s + 0.7, 18, 0.4)]}, sfx=[sfx("impact", s, 0.6), sfx("boom", s + 0.1, 0.5)])


@shot("pr04", "the", "CALLBACK", "Small callback inset: the floe + wave crest from R4 (reused markup); Tag REMEMBER THE FLOE", "static", "whoosh", nth=2)
def _(c):
    return dict(bg=surface(0.5, ICY, depth=6), layers=[SV(ICE, "50%", "47%", 560, 224, z=2), SV(WAVE, "30%", "44%", 700, 240, z=3, keyframes=[{"t": 0, "x": "20%"}, {"t": c.d, "x": "60%"}]),
                                                     TAG("REMEMBER THE FLOE", 0.1, "50%", "12%", 46, w=600)], sfx=[sfx("whoosh", 0.1)])


@shot("pr05", 0, "ACTION", "The sepia figure hops across three slabs toward safety; Tag HE MADE IT", "panLeft", "whoosh x3")
def _(c):
    L = [SV(_svg("0 0 640 420", '<path d="M0 30 L640 0 L640 420 L0 420 Z" fill="#f4f1e8"/>'), f"{x}%", "78%", 600, 380, z=1, rotate=r) for x, r in ((22, -6), (50, 3), (78, 7))]
    kf = [{"t": 0, "x": "78%", "y": "56%"}]
    for i, x in enumerate((64, 50, 36, 22)):
        kf += [{"t": 0.35 + i * 0.4, "x": f"{x}%", "y": "48%"}, {"t": 0.55 + i * 0.4, "x": f"{x}%", "y": "56%"}]
    L += [SV(PONTING, "78%", "56%", 200, 270, z=3, keyframes=kf), TAG("HE MADE IT", c.w("made"), "50%", "10%", 48, accent=GREEN, w=440)]
    return dict(bg=sepia(), layers=L, sfx=[sfx("whoosh", 0.35 + i * 0.4, 0.4) for i in range(3)])


@shot("pr05", "off", "SCALE", "Split comparison: a thick sea-ice slab vs a thin yellow kayak hull line; Tags HIS ICE / YOUR HULL on 'You'd'", "static", "ding")
def _(c):
    L = [SV(SLAB_THICK, "32%", "56%", 300, 420), SV(SLAB_THIN, "68%", "56%", 300, 420), TAG("HIS ICE", 0.1, "32%", "16%", 44, w=320),
         TAG("YOUR HULL: A FEW MM", c.w("You'd"), "68%", "16%", 44, accent=RED, w=560), kayak_at("68%", 0.56 * H - 205, 300)]
    return dict(bg=card(), layers=L, sfx=[sfx("ding", c.w("You'd"))])


@shot("pr07", 0, "INFO", "Options list HIM? / HIS DOGS? / A DARK SHAPE?, no selection; ? stamp NOBODY KNOWS on 'Nobody'", "static", "click")
def _(c):
    return dict(bg=sepia(), layers=[comp("explainer/Options", "50%", "50%", 1200, 700, {"title": "WHAT WERE THEY AFTER?", "items": ["HIM?", "HIS DOGS?", "A DARK SHAPE ON THE ICE?"],
                                                                                         "itemAt": [c.w("him"), c.w("dogs"), c.w("dark")], "size": 50}),
                                    STAMP("NOBODY KNOWS", c.w("Nobody"), "70%", "80%", color="#7a5a2a")], sfx=[sfx("click", c.w("Nobody"))])


@shot("pr08", 0, "PUNCH", "Could-vs-has card: COULD IT? YES on 'Clearly', HAS IT? on 'Has', then a huge white 0 on 'zero'", "static", "stinger")
def _(c):
    return dict(bg=black(), layers=[HL("COULD IT?  YES.", c.w("Clearly"), "24%", 76, "white", False), HL("HAS IT?", c.w("Has"), "44%", 76, "white", False),
                                    STAT(0, "WILD ORCAS · HUMAN DEATHS", c.w("zero"), "50%", "70%", 170)], sfx=[sfx("stinger", c.w("zero"), 0.5)])


# ---------------------------------------------------------------- climax
OPTS = ["SWIM FOR IT", "CLIMB ON SOMETHING", "DIVE AND HIDE", "PLAY DEAD"]


def opts_layer(c, select=None, strikes=(), itemAt=None, x="27%"):
    p = {"title": "YOUR FOUR MOVES", "items": [f"{i + 1}  {t}" for i, t in enumerate(OPTS)], "size": 40, "stamp": True,
         "strikes": [{"index": i, "at": a} for i, a in strikes]}
    if itemAt:
        p["itemAt"] = itemAt
    if select is not None:
        p["select"] = {"index": select[0], "at": select[1]}
    return comp("explainer/Options", x, "52%", 900, 760, p, depth=0, z=20)


@shot("c01", 0, "WIDE", "Top-down: NEW S top-view kayak centred in a spotlight circle; four Orca (pose top) circle it slowly", "pushIn", "heartbeat loop")
def _(c):
    L = [SV(SPOT, "50%", "50%", 860, 860, z=1), SV(KAYAK_TOP, "50%", "50%", 420, 112, z=5)]
    for k in range(4):
        kf = []
        for j in range(9):
            a = 2 * math.pi * (k / 4 + j / 8 * min(1.0, c.d / 6))
            t = c.d * j / 8
            kf.append({"t": round(t, 2), "x": 960 + 380 * math.cos(a), "y": 540 + 300 * math.sin(a), "rotate": math.degrees(a) + 90, "ease": "linear"})
        L.append(orca(kf[0]["x"], kf[0]["y"], 360, 140, kf, pose="top"))
    return dict(bg=ocean(8), layers=L, camera=cam("pushIn", 0.3), sfx=[sfx("heartbeat", 0.2, 0.5)])


@shot("c01", "and", "CARD", "Options YOUR FOUR MOVES, four items stagger in", "static", "click x4", nth=1)
def _(c):
    return dict(bg=card(), layers=[opts_layer(c, x="50%", itemAt=[0.1 + i * 0.25 for i in range(4)])], sfx=[sfx("click", 0.1 + i * 0.25, 0.5) for i in range(4)])


@shot("c02", 0, "INFO", "Option 1 selected (list left); right: SpeedBars recall ORCA 56 / YOU 3; Tag DELIVERY on 'delivery'; strike on 1 at the end", "static", "whoosh then strike click")
def _(c):
    rows = [{"label": "ORCA", "value": 56, "unit": "km/h", "color": "red"}, {"label": "YOU", "value": 3, "unit": "km/h", "color": WHITE}]
    L = [opts_layer(c, (0, 0.05), [(0, c.le() + 0.05)]), comp("explainer/SpeedBars", "72%", "44%", 880, 320, {"title": "REMEMBER?", "max": 60, "at": c.w("fifty"), "stagger": 0.3, "size": 38, "labelWidth": 200, "rows": rows}),
         TAG("NOT A RACE. A DELIVERY.", c.w("delivery"), "72%", "76%", 40, accent=RED, w=640)]
    return dict(bg=card(), layers=L, sfx=[sfx("whoosh", c.w("fifty")), sfx("click", c.le() + 0.05)])


@shot("c03", 0, "INFO", "Option 2 selected; right: NEW S flipped kayak on the waterline with YOU perched on top", "static", "click")
def _(c):
    L = [opts_layer(c, (1, 0.05), [(0, 0)]), SV(KAYAK_FLIP, "72%", "50%", 600, 260, z=5), {"type": "rect", "x": "72%", "y": "74%", "width": 900, "height": 300, "fill": "#1f5368", "opacity": 0.8, "z": 4}]
    return dict(bg=card(), layers=L, sfx=[sfx("click", 0.05)])


@shot("c03", "You've", "INFO", "Right: the R4 floe-and-wave replays (reused ICE + WAVE markup); on 'seal' the Seal swaps for a YOU icon; strike on 2", "static", "impact; click")
def _(c):
    s = c.w("seal")
    L = [opts_layer(c, (1, 0), [(0, 0), (1, c.le() + 0.05)]), SV(ICE, "72%", "50%", 520, 208, z=2), CR("Seal", "72%", "45%", 220, 96, end=s),
         CR("You", "72%", "40%", 80, 140, pose="panic", start=s, enter=pop(s)),
         SV(WAVE, "60%", "46%", 600, 200, z=3, keyframes=[{"t": 0, "x": "52%", "opacity": 0}, {"t": 0.6, "x": "62%", "opacity": 0.9}, {"t": c.d, "x": "92%", "opacity": 0}])]
    return dict(bg=card(), layers=L, sfx=[sfx("impact", 0.6, 0.4), sfx("click", c.le() + 0.05)])


@shot("c04", 0, "INFO", "Option 3 selected; right: Diver sinks into darkening water (keyframes)", "panDown", "bubbles")
def _(c):
    L = [opts_layer(c, (2, 0.05), [(0, 0), (1, 0)]), CR("Diver", "72%", "40%", 420, 160, kf=[{"t": 0, "y": "30%"}, {"t": c.d, "y": "62%"}], kick=True, arms="forward", rotate=60)]
    return dict(bg=ocean(40), layers=L, sfx=[sfx("bubbles", 0.2, 0.5)])


@shot("c04", "Remember", "INFO", "Right: sound rings spread from the kicking Diver toward an Orca outline with the ear icon (R3 callback); Tag THEY HUNT BY EAR; strike on 3", "static", "sonar_ping x2; click")
def _(c):
    L = [opts_layer(c, (2, 0), [(0, 0), (1, 0), (2, c.le() + 0.05)]), CR("Diver", "64%", "60%", 380, 150, kick=True, arms="forward", rotate=60)]
    L += ring_layers(1230, 650, 0.2, c.d, 0.7, 3, 360)
    L += [orca("86%", "34%", 420, 160, silhouette="#0d1216", flipX=True), SV(EAR, "86%", "20%", 70, 94), TAG("THEY HUNT BY EAR", c.w("listening"), "72%", "84%", 40, accent=RED, w=560)]
    return dict(bg=ocean(60), layers=L, sfx=[sfx("sonar_ping", 0.3, 0.4), sfx("click", c.le() + 0.05)])


@shot("c05", 0, "JOKE", "Option 4 selected; right: upside-down GreatWhite with the emptied Liver outline; Tag ASK THE LIVER on 'Ask'; strike on 4", "static", "pop + click")
def _(c):
    L = [opts_layer(c, (3, 0.05), [(0, 0), (1, 0), (2, 0), (3, c.le() + 0.05)]),
         comp("explainer/GreatWhite", "72%", "48%", 760, 300, {"silhouette": "#9aa7ad", "idle": False}, keyframes=[{"t": 0, "scaleY": -1}]),
         CR("Liver", "70%", "50%", 150, 110, opacity=0.25), TAG("IF THE THEORY IS RIGHT", c.w("theory"), "72%", "20%", 34, accent=YEL, w=520),
         TAG("ASK THE LIVER", c.w("Ask"), "72%", "76%", 46, accent=RED, w=480)]
    return dict(bg=card(), layers=L, sfx=[sfx("pop", c.w("Ask")), sfx("click", c.le() + 0.05)])


@shot("c06", 0, "CARD", "All four moves struck through and held", "pushIn", "riser")
def _(c):
    return dict(bg=card(), layers=[opts_layer(c, None, [(0, 0), (1, 0), (2, 0), (3, 0)], x="50%")], camera=cam("pushIn", 0.4), sfx=[sfx("riser", 0, 0.4)])


@shot("c06", "Once", "PUNCH", "Climax verdict (~69%): black card, white text, red NOT YOUR CALL", "static", "boom then silence")
def _(c):
    return dict(bg=black(), layers=[HL("ONCE IT PICKS YOU,", 0.0, "38%", 84, "white", False), HL("IT'S NOT YOUR CALL.", c.w("outcome"), "58%", 96, "red", False)],
                sfx=[sfx("boom", c.w("outcome"), 0.5)], trans={"type": "dipBlack", "duration": 0.3})


# ---------------------------------------------------------------- twist
@shot("t01", 0, "MED", "Kayak again in a daylight palette; fins pass by at a distance; Stat 0 AND YET", "drift", "underwater_rumble bed back in")
def _(c):
    L = [kayak_at("40%", WL, 620)] + fins([1500, 1640], WL, 110, kf_x=[(0, [1500, 1640]), (c.d, [1700, 1840])]) + [STAT(0, "AND YET", 0.3, "70%", "24%", 120)]
    return dict(bg=surface(0.5, DAY), layers=L, camera=cam("drift", 0.3), sfx=[sfx("underwater_rumble", 0, 0.4)])


@shot("t03", 0, "MAP", "Map Iberia at detail zoom 5 (mapdetail.ts has Iberia), pin Strait of Gibraltar (-5.6, 36.0); Tag SINCE 2020", "static (map zoom)", "click")
def _(c):
    return dict(bg=ocean(40), layers=[comp("explainer/Map", "50%", "50%", W, H, {"views": [{"t": 0, "lon": -6, "lat": 39, "zoom": 3}, {"t": 1.0, "lon": -6.5, "lat": 37.5, "zoom": 5}],
                                                                                 "pins": [{"lon": -5.6, "lat": 36.0, "at": 0.8, "label": "Gibraltar"}], "labelSize": 40, "pinSize": 1.4}, depth=0),
                                      TAG("SPAIN & PORTUGAL · SINCE 2020", c.w("2020"), "50%", "10%", 44, w=780)], sfx=[sfx("click", 0.8)])


@shot("t03", "some", "ACTION", "Kit Sailboat: an Orca rams it (hits), the rudder snaps off on 'snapped', the boat lists and sinks on 'sank'", "static", "impact (wood crack)")
def _(c):
    sn, sk = c.w("snapped"), c.w("sank")
    L = [comp("explainer/Sailboat", "50%", "46%", 900, 700, {"snapAt": sn, "hits": [c.w("rammed"), sn], "list": [{"t": 0, "v": 0}, {"t": sk, "v": 8}, {"t": c.d, "v": 18}],
                                                          "sink": [{"t": 0, "v": 0}, {"t": sk, "v": 0}, {"t": c.d + 1.5, "v": 260}], "bob": True}),
         orca("30%", "70%", 520, 190, [{"t": 0, "x": "10%"}, {"t": c.w("rammed"), "x": "40%"}, {"t": c.d, "x": "34%"}]), TAG("RUDDERS", sn, "76%", "14%", 44, accent=RED, w=360)]
    return dict(bg=surface(0.5, DAY, depth=6), layers=L, sfx=[sfx("impact", sn, 0.6)])


@shot("t04", 0, "INFO", "Orca swims away from the listing boat; NEW S life raft with two YOU icons, green tick; Tag PEOPLE SERIOUSLY HURT: 0 on 'nobody'", "static", "bubbles; ding")
def _(c):
    n = c.w("nobody")
    L = [orca("40%", "72%", 520, 190, [{"t": 0, "x": "40%"}, {"t": c.d, "x": "-10%"}], flipX=True), SV(RAFT, "66%", "52%", 420, 160, z=4),
         CR("You", "62%", "44%", 70, 120, pose="wave", z=5), CR("You", "70%", "44%", 70, 120, pose="stand", z=5), TAG("PEOPLE SERIOUSLY HURT: 0 ✓", n, "50%", "14%", 46, accent=GREEN, w=760)]
    return dict(bg=surface(0.5, DAY, depth=6), layers=L, sfx=[sfx("bubbles", 0.2, 0.4), sfx("ding", n)])


@shot("t05", 0, "CU", "Face to face: YOU in the kayak, three Tags pop SLOW / SOFT / IN THEIR KITCHEN, then three Orca glide past below on 'still'", "static", "pop x3; whoosh")
def _(c):
    st = c.w("still")
    L = [kayak_at("50%", 0.42 * H, 760), TAG("SLOW", c.w("slow"), "20%", "14%", 44, w=240), TAG("SOFT", c.w("soft"), "50%", "14%", 44, w=240),
         TAG("IN THEIR KITCHEN", c.w("kitchen"), "80%", "14%", 44, w=480)]
    L += [orca(f"{-20 + i * 10}%", f"{66 + i * 10}%", 560, 210, [{"t": 0, "x": "-30%"}, {"t": st, "x": "-30%"}, {"t": c.d + 1.5, "x": "120%", "ease": "linear"}], timeOffset=i * 0.3) for i in range(3)]
    return dict(bg=surface(0.42, DAY, depth=10), layers=L, sfx=[sfx("pop", c.w(w), 0.5) for w in ("slow", "soft", "kitchen")] + [sfx("whoosh", st)])


@shot("t06", 0, "CARD", "Headline WHY? with a yellow tag NOBODY KNOWS FOR SURE; Tag 2 CLUES on 'two'", "static", "tick")
def _(c):
    return dict(bg=card(), layers=[HL("WHY?", 0.05, "36%", 130), TAG("NOBODY KNOWS FOR SURE", c.w("Nobody"), "50%", "60%", 44, accent=YEL, bg=YEL, color=INK, w=640),
                                   TAG("2 CLUES", c.w("two"), "50%", "78%", 44, w=300)], sfx=[sfx("tick", c.w("two"))])


@shot("t07", 0, "INFO", "Looking up from below: NEW S silhouettes of a person on a board and a seal side by side, a GreatWhite rising below; Tag MISTAKEN IDENTITY?", "static", "underwater_rumble")
def _(c):
    L = [SV(BOARDER, "34%", "16%", 520, 200), SV(SEALSIL, "70%", "16%", 520, 200, start=c.w("seal"), enter=pop(c.w("seal"))),
         CR("GreatWhite", "50%", "70%", 700, 270, kf=[{"t": 0, "y": "86%"}, {"t": c.d, "y": "66%"}], rotate=-14), TAG("MISTAKEN IDENTITY?", c.w("mistakes"), "50%", "44%", 46, accent=YEL, w=600)]
    return dict(bg=ocean(10), layers=L, sfx=[sfx("underwater_rumble", 0, 0.3)])


@shot("t08", 0, "CALLBACK", "Callback to R4: an Orca spy-hops beside your kayak, head out of the water; the same Tag THEY CHECK FIRST", "pushIn", "bubbles")
def _(c):
    L = [kayak_at("62%", WL, 560), orca("34%", "50%", 520, 190, [{"t": 0, "y": "70%"}, {"t": 1.0, "y": "48%", "ease": "out"}], rotate=-80),
         TAG("THEY CHECK FIRST", c.w("check"), "50%", "12%", 52, accent=RED, w=600), TAG("LOOK + LISTEN", c.w("looking"), "50%", "86%", 44, w=420)]
    return dict(bg=surface(0.5, DAY), layers=L, camera=cam("pushIn", 0.3), sfx=[sfx("bubbles", 0.2, 0.4)])


@shot("t09", 0, "INFO", "The R3 pod family tree returns with menu cards hanging under each branch; Headline CULTURE on 'family'", "pushIn", "ding")
def _(c):
    L = [SV(PODTREE, "50%", "40%", 1200, 420, z=1)]
    for i, (x, y, s) in enumerate([(50, 22, 0.42), (21, 50, 0.3), (50, 50, 0.3), (79, 50, 0.3)]):
        L.append(orca(f"{x}%", f"{y}%", 900 * s, 330 * s, timeOffset=i * 0.37))
    L += [SV(MENU, f"{21 + i * 29}%", "80%", 220, 176, start=c.w("menu") + i * 0.2, enter=pop(c.w("menu") + i * 0.2)) for i in range(3)]
    L.append(HL("CULTURE", c.w("family"), "10%", 70, "white", True))
    return dict(bg=ocean(14), layers=L, camera=cam("pushIn", 0.3), sfx=[sfx("ding", c.w("family"))])


@shot("t10", 0, "ACTION", "A fish-eating pod glides past a Seal with no reaction; the seal does a double take (rotate keyframes); Tag FISH EATERS IGNORE SEALS", "panRight", "whoosh")
def _(c):
    L = [orca("50%", "60%", 560, 210, [{"t": 0, "x": "0%"}, {"t": c.d, "x": "100%", "ease": "linear"}]), orca("50%", "72%", 460, 170, [{"t": 0, "x": "-12%"}, {"t": c.d, "x": "88%", "ease": "linear"}], timeOffset=0.4),
         CR("Seal", "60%", "36%", 260, 110, kf=[{"t": 0, "rotate": 0}, {"t": c.d * 0.5, "rotate": 0}, {"t": c.d * 0.5 + 0.25, "rotate": -18}, {"t": c.d * 0.5 + 0.5, "rotate": 0}, {"t": c.d * 0.5 + 0.75, "rotate": -18}]),
         TAG("FISH EATERS IGNORE SEALS", 0.2, "50%", "12%", 46, w=760)]
    return dict(bg=ocean(12), layers=L, camera=cam("panRight", 0.2), sfx=[sfx("whoosh", 0.3)])


@shot("t10", "and", "INFO", "Recall the R4 WEDDELL select card (same layout, red ring)", "static", "click", nth=1)
def _(c):
    L = [{"type": "rect", "x": "50%", "y": "52%", "width": 520, "height": 520, "fill": "#14262f", "stroke": "#3d5966", "strokeWidth": 3, "radius": 16},
         CR("Seal", "50%", "50%", 380, 160, silhouette="#8a98a0"), TAG("WEDDELL", 0.1, "50%", "74%", 40, w=380),
         {"type": "circle", "x": "50%", "y": "52%", "width": 580, "height": 580, "fill": "rgba(0,0,0,0)", "stroke": RED, "strokeWidth": 10, "start": 0.3, "enter": pop(0.3), "z": 6},
         TAG("MAMMAL HUNTERS LEARN WHICH COUNT", 0.2, "50%", "12%", 42, w=900)]
    return dict(bg=card(), layers=L, sfx=[sfx("click", 0.3)])


@shot("t11", 0, "JOKE", "NEW S chalkboard FAMILY MENU; the YOU line gets a red strike on 'never'", "static", "click")
def _(c):
    n = c.w("never")
    return dict(bg=card(), layers=[SV(MENU, "50%", "50%", 820, 656, enter=pop(0.05)), SV(STRIKE, "45%", "73.5%", 260, 22, start=n, enter={"type": "wipeRight", "at": n, "duration": 0.3}, z=5),
                                   TAG("NEVER ON IT", n, "76%", "76%", 40, accent=RED, w=360)], sfx=[sfx("click", n)])


@shot("t12", 0, "CALLBACK", "Hook hull frame, silent: Tag LOOKING; on 'chatty' the rings return softly with Tag DECIDED", "pushIn", "silence -> sonar_ping soft")
def _(c):
    ch = c.w("chatty")
    L = [kayak_at("50%", 0.38 * H, 900), TAG("SILENT = LOOKING", 0.2, "26%", "78%", 40, accent=RED, w=480, end=ch),
         TAG("CHATTY = DECIDED", ch, "74%", "78%", 40, accent=GREEN, w=480)] + ring_layers(960, 640, ch, c.d, 1.0, 3, 340)
    return dict(bg=surface(0.38, depth=10), layers=L, camera=cam("pushIn", 0.3), sfx=[sfx("sonar_ping", ch, 0.3)])


@shot("t13", 0, "PUNCH", "Green stamp THEY CHECKED. YOU WEREN'T FOOD. over the YOU icon (calls back THEY CHECK FIRST)", "static", "ding")
def _(c):
    return dict(bg=card(), layers=[CR("You", "50%", "50%", 200, 330, pose="wave"), STAMP("THEY CHECKED.", 0.05, "50%", "20%", color=GREEN, size=56, rot=-3),
                                   STAMP("YOU WEREN'T FOOD.", c.w("weren't"), "50%", "82%", color=GREEN, size=56, rot=3)], sfx=[sfx("ding", c.w("weren't"))])


# ---------------------------------------------------------------- villain swap (no jokes from here)
@shot("v01", 0, "CARD", "The hook's WILD HUMAN KILLS: 0 card returns; IN THE WILD underlines in red on 'wild'", "pushIn", "riser")
def _(c):
    return dict(bg=surface(0.5, DUSK), layers=[STAT(0, "WILD HUMAN KILLS", 0, "50%", "38%", 140), TAG("\"IN THE WILD\"", c.w("wild"), "50%", "66%", 60, accent=RED, w=600)],
                camera=cam("pushIn", 0.3), sfx=[sfx("riser", 0, 0.4)], nochip=True)


@shot("v02", 0, "INFO", "Side-view tank cross-section (grey walls, flat water); one Orca swims back and forth, scaleX flips at each wall", "static", "drone")
def _(c):
    kf, t, x = [], 0.0, 30
    while t < c.d:
        kf += [{"t": round(t, 2), "x": f"{x}%", "scaleX": 1 if x == 30 else -1}, {"t": round(min(c.d, t + 1.6), 2), "x": f"{100 - x}%", "scaleX": 1 if x == 30 else -1, "ease": "inOut"}]
        t += 1.65
        x = 100 - x
    L = [{"type": "rect", "x": "50%", "y": "58%", "width": 1400, "height": 560, "fill": "#2a3a44", "stroke": "#8a9aa3", "strokeWidth": 18, "z": 1},
         {"type": "rect", "x": "50%", "y": "62%", "width": 1364, "height": 480, "fill": "#3f7f96", "opacity": 0.7, "z": 1}, orca("30%", "62%", 420, 150, kf, z=3)]
    return dict(bg={"type": "color", "color": "#1a2026"}, layers=L, sfx=[sfx("drone", 0, 0.3)], nochip=True)


@shot("v02", "There", "INFO", "Stat 4 in red, label HUMAN DEATHS · ALL IN CAPTIVITY (one sober line, no names)", "static", "none")
def _(c):
    return dict(bg={"type": "color", "color": "#1a2026"}, layers=[STAT(4, "HUMAN DEATHS · ALL IN CAPTIVITY", 0.05, "50%", "50%", 170, color="red")], nochip=True)


@shot("v03", 0, "INFO", "Red arrow from a YOU icon to an Orca icon; Tag US → THEM", "static", "whoosh")
def _(c):
    return dict(bg=card(), layers=[CR("You", "20%", "52%", 180, 300), SV(ARROW, "50%", "52%", 600, 120, enter={"type": "wipeRight", "at": 0.2, "duration": 0.4}), orca("80%", "52%", 520, 190),
                                   TAG("US → THEM", c.w("people"), "50%", "80%", 48, accent=RED, w=420)], sfx=[sfx("whoosh", 0.2)], nochip=True)


@shot("v04", 0, "MAP", "Map Pacific Northwest (zoom 3.5), pin Puget Sound (-122.5,47.6); five orca dots lifted out one by one; Tag 1960s-70s · DOZENS TAKEN", "pushIn (map zoom)", "click steady")
def _(c):
    L = [comp("explainer/Map", "50%", "50%", W, H, {"views": [{"t": 0, "lon": -125, "lat": 46, "zoom": 2.5}, {"t": 1.2, "lon": -123, "lat": 48, "zoom": 3.5}],
                                                    "pins": [{"lon": -122.5, "lat": 47.6, "at": 0.6, "label": "Puget Sound"}], "labelSize": 40, "pinSize": 1.4}, depth=0)]
    L += [{"type": "circle", "x": f"{46 + i * 2.4}%", "y": "58%", "width": 30, "height": 30, "fill": WHITE, "depth": 0, "z": 32,
           "keyframes": [{"t": 0, "opacity": 1, "y": "58%"}, {"t": 1.4 + i * 0.5, "opacity": 1, "y": "58%"}, {"t": 1.8 + i * 0.5, "opacity": 0, "y": "40%"}]} for i in range(5)]
    L += [TAG("1960s-70s · DOZENS TAKEN", c.w("dozens"), "50%", "10%", 44, accent=RED, w=700)]
    return dict(bg=ocean(40), layers=L, sfx=[sfx("click", 1.4 + i * 0.5, 0.4) for i in range(5)], nochip=True)


@shot("v05", 0, "INFO", "Dot grid: 75 white dots (Stat 75 on 'seventy'), then 23 grey outlines appear on 'ninety-eight' (1995 peak)", "static", "tick")
def _(c):
    L = [SV(DOTS98, "50%", "56%", 1400, 560), SV(DOTS23, "50%", "56%", 1400, 560, start=c.w("ninety"), enter=fade(c.w("ninety"))),
         TAG("TODAY: ~75", c.w("seventy"), "30%", "10%", 46, w=400), TAG("1995: ~98", c.w("ninety"), "70%", "10%", 46, accent=GREY, w=400)]
    return dict(bg=card(), layers=L, sfx=[sfx("tick", c.w("seventy")), sfx("tick", c.w("ninety"))], nochip=True)


@shot("v05", "roughly", "SCALE", "Kit Bus labelled ONE SCHOOL BUS FULL beside the 75-dot grid shrunk to a block", "static", "ding")
def _(c):
    return dict(bg=card(), layers=[CR("Bus", "36%", "56%", 900, 380, text="ONE BUS"), SV(DOTS98, "78%", "56%", 560, 224), TAG("≈ ONE SCHOOL BUS FULL", 0.1, "50%", "12%", 46, w=700)],
                sfx=[sfx("ding", 0.2)], nochip=True)


@shot("v06", 0, "INFO", "Triptych 1: salmon icons fade out one by one; Tag SALMON ↓", "static", "underwater_rumble")
def _(c):
    L = [SV(FISH, f"{20 + (i % 4) * 20}%", f"{40 + (i // 4) * 20}%", 220, 90, keyframes=[{"t": 0, "opacity": 1}, {"t": 0.3 + i * 0.25, "opacity": 1}, {"t": 0.6 + i * 0.25, "opacity": 0.12}]) for i in range(8)]
    return dict(bg=ocean(14), layers=L + [TAG("SALMON ↓", 0.1, "50%", "12%", 48, accent=RED, w=360)], sfx=[sfx("underwater_rumble", 0, 0.3)], nochip=True)


@shot("v06", "ship", "INFO", "Triptych 2: NEW S ship silhouette on the surface with noise rings scrambling an Orca's click arcs; Tag SHIP NOISE", "static", "static low")
def _(c):
    L = [SV(SHIP, "50%", "20%", 700, 260), orca("50%", "70%", 560, 210)] + ring_layers(960, 230, 0.0, c.d, 0.5, 4, 600, "#e5483d")
    return dict(bg=surface(0.3, DUSK, depth=12), layers=L + [TAG("SHIP NOISE", 0.1, "80%", "50%", 46, accent=RED, w=400)], sfx=[sfx("static", 0.1, 0.25)], nochip=True)


@shot("v06", "blubber", "INFO", "Triptych 3: NEW S blubber cross-section with dark specks; Tag CHEMICALS", "pushIn", "drone")
def _(c):
    return dict(bg=card(), layers=[SV(BLUBBER, "50%", "54%", 1100, 440), TAG("CHEMICALS (PCBs)", 0.2, "50%", "12%", 46, accent=RED, w=560)], camera=cam("pushIn", 0.3),
                sfx=[sfx("drone", 0, 0.3)], nochip=True)


@shot("v07", 0, "PUNCH", "Card NO NATURAL PREDATOR. then red EXCEPT US. on 'us' (pays off R6's 'nothing hunts it back')", "static", "stinger soft")
def _(c):
    return dict(bg=black(), layers=[HL("NOTHING HUNTS THE ORCA.", 0.05, "38%", 80, "white", False), HL("EXCEPT US.", c.w("us"), "58%", 110, "red", False)],
                sfx=[sfx("stinger", c.w("us"), 0.3)], nochip=True)


# ---------------------------------------------------------------- bookend
@shot("e01", 0, "WIDE", "Exact hook frame: kayak at dusk, same composition as 0:00", "drift", "underwater_rumble")
def _(c):
    return dict(bg=surface(0.5), layers=[kayak_at("34%", WL, 560)] + fins([1420, 1580], WL, 120), camera=cam("drift", 0.4), sfx=[sfx("underwater_rumble", 0, 0.4)], nochip=True)


@shot("e02", 0, "CU", "Hull rings return, louder (bigger, faster)", "static", "sonar_ping chirps")
def _(c):
    return dict(bg=surface(0.38, depth=10), layers=[kayak_at("50%", 0.38 * H, 900)] + ring_layers(960, 640, 0.0, c.d, 0.6, 4, 460),
                sfx=[sfx("sonar_ping", 0.1, 0.5), sfx("sonar_ping", 0.9, 0.5)], nochip=True)


@shot("e02", "and", "MED", "Three Orca surface beside the kayak; blow puffs (white circles) on 'breathe'", "panRight", "breath x3")
def _(c):
    b = c.w("breathe")
    L = [kayak_at("36%", WL, 560)]
    L += [orca(f"{58 + i * 13}%", f"{55 + i * 2}%", 520, 190, [{"t": 0, "x": f"{70 + i * 13}%"}, {"t": c.d + 1, "x": f"{52 + i * 13}%"}], timeOffset=i * 0.4) for i in range(3)]
    L += [{"type": "circle", "x": f"{64 + i * 13}%", "y": "40%", "width": 120, "height": 120, "fill": "#f3f6f7", "opacity": 0,
           "keyframes": [{"t": max(0, b - 0.2 + i * 0.3), "opacity": 0, "scale": 0.3}, {"t": b + i * 0.3, "opacity": 0.8}, {"t": b + 0.8 + i * 0.3, "opacity": 0, "scale": 1.4}]} for i in range(3)]
    return dict(bg=surface(0.5), layers=L, camera=cam("panRight", 0.2), sfx=[sfx("breath", b + i * 0.3, 0.5) for i in range(3)], nochip=True)


@shot("e03", 0, "INFO", "Hook Stat WILD HUMAN KILLS: 0 returns over the kayak; Tag THE RULE HOLDS", "static", "tick")
def _(c):
    return dict(bg=surface(0.5), layers=[kayak_at("30%", WL, 560), STAT(0, "WILD HUMAN KILLS", c.w("wild"), "68%", "28%", 130), TAG("THE RULE HOLDS", 0.2, "68%", "48%", 40, accent=GREEN, w=440)],
                sfx=[sfx("tick", c.w("wild"))], nochip=True)


@shot("e04", 0, "CARD", "Finished board: the THREAT FILE folder with each tab's verdict stamp landing on its word (outsizes BODY ... blue whales GIANTS)", "static", "tick x6")
def _(c):
    ws = ["outsizes", "outruns", "plans", "washes", "empties", "brings"]
    L = [SV(folder_svg(6), "50%", "54%", 1400, 600, z=5)]
    for i, w in enumerate(ws):
        xpct = f"{(960 - 700 + (60 + i * 215 + 95)) / W * 100:.2f}%"
        L.append(comp("explainer/Tag", xpct, "62%", 200, 240, {"text": VERDICTS[i].replace(" ", "\n", 1), "at": c.w(w), "size": 26, "accent": RED, "bg": RED, "color": WHITE, "align": "center"},
                      depth=0, z=30, rotate=-8 + (i % 2) * 6, enter=pop(c.w(w), 0.25)))
    return dict(bg=card(), layers=L + [HL("THREAT FILE: ORCA", 0.05, "10%", 56)], sfx=[sfx("tick", c.w(w), 0.6) for w in ws], nochip=True)


@shot("e05", 0, "CU", "Orca eye level with YOU, camera pushes 1x -> 1.6x and holds", "pushIn", "heartbeat_slow")
def _(c):
    return dict(bg=surface(0.3, depth=12), layers=[kayak_at("70%", 0.3 * H, 520), orca("36%", "60%", 1000, 380)],
                camera={"keyframes": [{"t": 0, "zoom": 1.0}, {"t": c.d, "x": 900, "y": 560, "zoom": 1.5}]}, sfx=[sfx("heartbeat_slow", 0.2, 0.5)], nochip=True)


@shot("e05", "then", "WIDE", "Fins move off toward the horizon", "pullOut", "whoosh_long soft")
def _(c):
    return dict(bg=surface(0.5), layers=[kayak_at("34%", WL, 560)] + fins([1100, 1240, 1380], WL, 120, kf_x=[(0, [1100, 1240, 1380]), (c.d + 1.5, [1600, 1740, 1880])]),
                camera=cam("pullOut", 0.3), sfx=[sfx("whoosh_long", 0.1, 0.3)], nochip=True)


@shot("e06", 0, "END IMAGE", "Kayak alone on glassy water; lower-third Headline ORCAS COULD HUNT YOU., second line THEY DECIDED NOT TO. lands on 'They'; the last fin drops below the horizon mid-shot", "static", "music swell")
def _(c):
    L = [kayak_at("34%", WL, 560)] + fins([1700], WL, 100, sink={0: c.w("They")})
    L += [HL("ORCAS COULD HUNT YOU.", 0.05, "74%", 64, "white", False), HL("THEY DECIDED NOT TO.", c.w("They"), "86%", 64, "red", False)]
    return dict(bg=surface(0.5), layers=L, sfx=[], nochip=True)


@shot("e07", 0, "END IMAGE", "The FAMILY MENU card slides up over the water, YOU still struck; Tag A HABIT on 'habit'", "static", "none")
def _(c):
    return dict(bg=surface(0.5), layers=[kayak_at("24%", WL, 460), SV(MENU, "64%", "46%", 600, 480, enter={"type": "slideUp", "at": 0.05, "duration": 0.4}),
                                         SV(STRIKE, "61%", "63%", 200, 18, z=6), TAG("A HABIT", c.w("habit"), "64%", "86%", 48, accent=YEL, w=320)], nochip=True)


@shot("e07", "in", "END IMAGE", "Sting: a snapped rudder icon (the Iberian new habit) floats by; a single fin rises behind the kayak on the last word; card YOU'RE SAFE BECAUSE OF A HABIT.", "static", "music cut on the last word", nth=1)
def _(c):
    last = c.le()
    L = [kayak_at("40%", WL, 620), SV(RUDDER, "78%", "52%", 80, 150, keyframes=[{"t": 0, "x": "90%", "rotate": 10}, {"t": c.d, "x": "70%", "rotate": -6}]),
         SV(FIN, "60%", WL - 70, 100, 140, keyframes=[{"t": 0, "y": WL + 60, "opacity": 0}, {"t": max(0.1, last - 0.6), "y": WL + 60, "opacity": 0}, {"t": last, "y": WL - 64, "opacity": 1, "ease": "out"}], z=3),
         TAG("NEW HABIT · SINCE 2020", 0.2, "78%", "36%", 34, accent=GREY, w=460), HL("YOU'RE SAFE BECAUSE OF A HABIT.", max(0.1, last - 0.4), "84%", 56, "white", False)]
    return dict(bg=surface(0.5), layers=L, sfx=[sfx("stinger", last, 0.3)], nochip=True)


@shot("x01", 0, "CARD", "Threat-file folder closes; two new folders LEOPARD SEAL? and BOX JELLYFISH? slide in; end-screen slot right", "static", "click")
def _(c):
    L = [SV(folder_svg(0, ""), "30%", "54%", 700, 300, enter={"type": "slideRight", "at": 0.1, "duration": 0.4}), TAG("LEOPARD SEAL?", c.w("leopard"), "30%", "30%", 44, w=420),
         SV(folder_svg(0, ""), "30%", "84%", 700, 300, start=c.w("box"), enter={"type": "slideRight", "at": c.w("box"), "duration": 0.4}), TAG("BOX JELLYFISH?", c.w("box"), "30%", "66%", 44, w=420),
         {"type": "rect", "x": "76%", "y": "50%", "width": 700, "height": 394, "fill": "#0f1d24", "stroke": "#8fb3c0", "strokeWidth": 4, "radius": 12},
         HL("NEXT FILE?", 0.05, "10%", 60)]
    return dict(bg=card(), layers=L, sfx=[sfx("click", 0.1), sfx("click", c.w("box"))], nochip=True)


# ============================================================== assembly
TAB_LIGHTS = [("b01", "one"), ("s01", 0), ("pl01", 0), ("w01", 0), ("k01", 0), ("g01", 0)]
TAB_T = [word_time(l, a) for l, a in TAB_LIGHTS]
CHIP_FROM = word_time("r03", 0)
CHIP_TO = TL["c06"].end + TL["c06"].pause


def shot_times():
    out = []
    for s in SHOTS:
        t = word_time(s["line"], s["anchor"], s["nth"]) - LEAD
        out.append(max(0.0, t))
    out[0] = 0.0
    for a, b in zip(out, out[1:]):
        assert b > a + 0.5, f"shots too close or out of order at {fmt(a)} / {fmt(b)}"
    return out


def chip_layers(t0, d):
    lit = sum(1 for t in TAB_T if t <= t0 + 0.05)
    L = []
    inside = [t for t in TAB_T if t0 + 0.05 < t < t0 + d]
    first_end = (inside[0] - t0) if inside else None
    base = SV(chip_svg(lit), 1650, 62, 440, 84, depth=0, z=60)
    if t0 < CHIP_FROM:  # chip slides in inside this scene
        a = CHIP_FROM - t0
        base["start"] = a
        base["enter"] = {"type": "slideLeft", "at": a, "duration": 0.4}
    if first_end is not None:
        base["end"] = first_end
    L.append(base)
    for t in inside:
        lit2 = sum(1 for x in TAB_T if x <= t + 0.01)
        a = t - t0
        lay = SV(chip_svg(lit2), 1650, 62, 440, 84, depth=0, z=61, start=a, enter={"type": "pop", "at": a, "duration": 0.3})
        nxt = [x for x in inside if x > t]
        if nxt:
            lay["end"] = nxt[0] - t0
        L.append(lay)
    return L


def visual_events(scene):
    ev = [0.0, scene["duration"]]
    for l in scene.get("layers", []):
        for k in ("start", "end"):
            if isinstance(l.get(k), (int, float)):
                ev.append(l[k])
        for k in ("enter", "exit"):
            if isinstance(l.get(k), dict) and isinstance(l[k].get("at"), (int, float)):
                ev.append(l[k]["at"])
        ev += [k["t"] for k in l.get("keyframes", [])]
        p = l.get("props") or {}
        for k in ("at", "out"):
            if isinstance(p.get(k), (int, float)) and p[k] > 0:
                ev.append(p[k])
        for v in p.values():
            if isinstance(v, list):
                ev += [k["t"] for k in v if isinstance(k, dict) and isinstance(k.get("t"), (int, float))]
                ev += [k for k in v if isinstance(k, (int, float)) and k > 0] if p.get("beats") is v else []
            if isinstance(v, dict) and isinstance(v.get("at"), (int, float)):
                ev.append(v["at"])
        for k in ("itemAt",):
            if isinstance(p.get(k), list):
                ev += [x for x in p[k] if isinstance(x, (int, float))]
    cam_ = scene.get("camera") or {}
    ev += [k["t"] for k in cam_.get("keyframes", [])]
    ev += [s["at"] for s in cam_.get("shake", [])]
    return sorted(t for t in ev if 0 <= t <= scene["duration"])


sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..")))
from pipeline.episodes.common import visual_events as pipe_events  # noqa: E402  (same rule check_storyboards.py uses)


def preset_kfs(cam_, d):
    a = cam_.get("amount", 1)
    cx, cy, pan = W / 2, H / 2, min(W, H) * 0.12 * a
    p = cam_.get("preset", "none")
    table = {"pushIn": ((cx, cy, 1), (cx, cy, 1 + 0.18 * a)), "pullOut": ((cx, cy, 1 + 0.18 * a), (cx, cy, 1)),
             "panLeft": ((cx + pan, cy, 1.08), (cx - pan, cy, 1.08)), "panRight": ((cx - pan, cy, 1.08), (cx + pan, cy, 1.08)),
             "panUp": ((cx, cy + pan, 1.08), (cx, cy - pan, 1.08)), "panDown": ((cx, cy - pan, 1.08), (cx, cy + pan, 1.08)),
             "drift": ((cx - pan * 0.3, cy + pan * 0.15, 1.04), (cx + pan * 0.3, cy - pan * 0.15, 1.1))}
    s0, s1 = table.get(p, ((cx, cy, 1), (cx, cy, 1)))
    return [{"t": 0, "x": s0[0], "y": s0[1], "zoom": s0[2], "ease": "linear"}, {"t": d, "x": s1[0], "y": s1[1], "zoom": s1[2], "ease": "linear"}]


def _interp(kfs, t, key, dflt):
    pts = [(k["t"], k[key]) for k in kfs if key in k and isinstance(k[key], (int, float))]
    if not pts:
        return dflt
    pts.sort()
    if t <= pts[0][0]:
        return pts[0][1]
    for (t0, v0), (t1, v1) in zip(pts, pts[1:]):
        if t0 <= t <= t1:
            return v0 + (v1 - v0) * (t - t0) / max(1e-6, t1 - t0)
    return pts[-1][1]


def fill_holds(scene, limit=2.9):
    """Gaps between visual events longer than `limit` get camera re-frame keyframes (a small zoom nudge on the existing
    camera path). Returns the number of keyframes added."""
    ev = pipe_events(scene)
    gaps = [(a, b) for a, b in zip(ev, ev[1:]) if b - a > limit]
    if not gaps:
        return 0
    d = scene["duration"]
    cam_ = scene.get("camera") or {}
    kfs = list(cam_.get("keyframes") or preset_kfs(cam_, d))
    if not kfs:
        kfs = [{"t": 0, "x": W / 2, "y": H / 2, "zoom": 1.0}, {"t": d, "x": W / 2, "y": H / 2, "zoom": 1.0}]
    added = 0
    for a, b in gaps:
        n = int(math.ceil((b - a) / limit))
        for i in range(1, n):
            t = round(a + (b - a) * i / n, 3)
            kfs.append({"t": t, "x": round(_interp(kfs, t, "x", W / 2), 1), "y": round(_interp(kfs, t, "y", H / 2), 1),
                        "zoom": round(_interp(kfs, t, "zoom", 1.0) + (0.015 if added % 2 == 0 else -0.01), 3), "ease": "inOut"})
            added += 1
    scene["camera"] = {k: v for k, v in cam_.items() if k not in ("preset", "amount")}
    scene["camera"]["keyframes"] = sorted(kfs, key=lambda k: k["t"])
    return added


def build():
    starts = shot_times()
    ends = starts[1:] + [TOTAL]
    scenes, rows, filled = [], [], 0
    for i, (s, a, b) in enumerate(zip(SHOTS, starts, ends)):
        d = round(b - a, 3)
        c = Ctx(a, d, s["line"])
        r = s["fn"](c)
        layers = list(r.get("layers", []))
        if not r.get("nochip") and a + d > CHIP_FROM and a < CHIP_TO:
            layers += chip_layers(a, d)
        voiced = [L for L in ORDER if L.start < b and L.end > a]
        sc = {"id": f"s{i + 1:03d}", "duration": d, "background": r.get("bg", ocean(15)), "layers": layers,
              "sfx": [x for x in r.get("sfx", []) if x["at"] < d], "notes": f"{s['kind']}: {s['vis']} | VO: " + " / ".join(L.text for L in voiced)}
        if r.get("camera"):
            sc["camera"] = r["camera"]
        if r.get("trans"):
            sc["transitionIn"] = r["trans"]
        filled += 1 if fill_holds(sc) else 0
        scenes.append(sc)
        rows.append((i + 1, a, b, s))
    words = []
    for L in ORDER:
        for w, st, en in L.words:
            words.append({"text": w, "start": round(st, 3), "end": round(min(en, st + 1.2), 3)})
    sb = {
        "version": 1, "id": "explainer-never-meet-orca", "title": "Orcas Could Hunt You. They Decided Not To.", "format": "16:9", "fps": 30,
        "scenes": scenes,
        "captions": {"enabled": True, "words": words, "maxWords": 4, "maxChars": 22,
                     "style": {"font": "display", "fontSize": 67, "color": "#ffffff", "highlight": "#ff5a4a", "highlightMode": "none", "strokeWidth": 12,
                               "uppercase": True, "y": 0.9}},
        "audio": {"voice": [], "music": [{"src": "music/deep_ocean.m4a", "start": 0, "volume": 0.32, "duckTo": 0.12}], "sfx": [], "duckOn": "captions"},
        "overlays": {"grain": 0.04, "vignette": 0.2, "fadeIn": 0, "fadeOut": 0.8},
        "_built": {"by": "backlog/explainer/explainer-never-meet-orca/gen_storyboard.py",
                   "timing": "Kokoro-82M am_michael per-line durations + word timestamps measured on the Spark CPU (tts_durations.json); voice track not mixed yet",
                   "todo": "make the mix with pipeline.audio.make on the Spark, then rerun this generator with the mix's captions.json word times and set audio.voice"},
    }
    return sb, rows, filled


# ============================================================== script.md rendering
def pct(t):
    return 100 * t / TOTAL


def stats():
    sents, words, youw = [], 0, 0
    for L in ORDER:
        w = re.findall(r"[A-Za-z0-9'-]+", L.text)
        words += len(w)
        youw += sum(1 for x in w if x.lower() in ("you", "your", "you're", "you'd", "you've", "yours", "you'll"))
        sents += [s for s in re.split(r"(?<=[.?!])\s+", L.text) if s.strip()]
    ys = sum(1 for s in sents if re.search(r"\byou(r|'re|'d|'ve|rs|'ll)?\b", s, re.I))
    speech = sum(L.dur for L in ORDER)
    hook = [L for L in ORDER if L.sec == "L1"]
    hw = sum(len(re.findall(r"[A-Za-z0-9'-]+", L.text)) for L in hook)
    numw = set("one two three four five six seven eight nine ten eleven twelve twenty thirty forty fifty sixty seventy eighty ninety hundred thousand thousands hundreds dozen dozens".split())
    nums = sum(1 for L in ORDER for x in re.findall(r"[a-z0-9-]+", L.text.lower()) if re.match(r"^\d", x) or any(n in x.split("-") for n in numw))
    return dict(words=words, sentences=len(sents), avg=words / len(sents), you_sent=100 * ys / len(sents), you_words=100 * youw / words,
                you_min=youw / (TOTAL / 60), runtime=TOTAL, speech=speech, wpm_speech=words / speech * 60, wpm=words / TOTAL * 60,
                hook_words=hw, hook_s=hook[-1].end, nums_min=nums / (TOTAL / 60))


def render_script(rows):
    out = []
    for key, name, _ in SECTIONS:
        ls = [L for L in ORDER if L.sec == key]
        if not ls:
            continue
        out.append(f"\n### {name}  ({fmt(ls[0].start)}-{fmt(ls[-1].end)}, {pct(ls[0].start):.0f}-{pct(ls[-1].end):.0f}%)\n")
        for L in ls:
            out.append(f"**[{fmt(L.start)}]** {L.text}  ")
            if L.os:
                out.append(f"  *On screen:* `{L.os}`")
            out.append("")
    shots = ["| # | t_start | t_end | dur | shot type | visual (kit vocabulary; NEW S = inline SVG in the storyboard) | camera | SFX |", "|---|---|---|---|---|---|---|---|"]
    for n, a, b, s in rows:
        shots.append(f"| {n} | {fmt(a)} | {fmt(b)} | {b - a:.1f} | {s['kind']} | {s['vis']} | {s['cam']} | {s['sfx']} |")
    return "\n".join(out), "\n".join(shots)


def main():
    sb, rows, filled = build()
    st = stats()
    if "--stats" in sys.argv:
        print(json.dumps({k: round(v, 2) for k, v in st.items()}, indent=1), "filled", filled, "scenes", len(rows))
        return
    script, shots = render_script(rows)
    tmpl = open(os.path.join(HERE, "script.tmpl.md")).read()

    def tok(m):
        kind, ref = m.group(1), m.group(2)
        if kind == "t":
            return fmt(TL[ref].start)
        if kind == "p":
            return f"{pct(TL[ref].start):.0f}%"
        if kind == "w":  # word time: id@word
            lid, w = ref.split("@")
            return fmt(word_time(lid, w))
        if kind == "s":
            v = st[ref]
            return f"{v:.1f}" if isinstance(v, float) else str(v)
        if kind == "rt":
            return fmt(TOTAL)
        if kind == "n":
            return str(len(rows))
        if kind == "filled":
            return str(filled)
        raise KeyError(kind)
    text = re.sub(r"\{(t|p|w|s|rt|n|filled):?([^}]*)\}", tok, tmpl)
    text = text.replace("<!--SCRIPT-->", script).replace("<!--SHOTS-->", shots)
    open(os.path.join(HERE, "script.md"), "w").write(text)
    json.dump(sb, open(os.path.join(HERE, "storyboard.json"), "w"), ensure_ascii=False, separators=(",", ":"))
    print(f"script.md + storyboard.json: {len(rows)} scenes, {fmt(TOTAL)}, holds filled by camera keys in {filled} scenes")


if __name__ == "__main__":
    main()
