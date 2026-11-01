#!/usr/bin/env python3
"""Generate storyboard.json for explainer-sinking-every-1000m from script.md (narration block) and
durations.json (real Kokoro word timings, measured on the Spark with measure_tts.py). Stdlib only, safe on the Mac.

usage: python3 gen_storyboard.py [--md]
  writes storyboard.json next to this file;
  --md also rewrites the generated sections of script.md (between the <!-- gen:... --> markers):
  the timed scene list, the shot table and the measured pacing block.

Timing model (matches pipeline/audio/make.py with this script's front matter):
- voice speed = front-matter `speed` (1.0), paragraph gap GAP = 0.32 s (paragraph_pause 0.2 + Kokoro tail),
  lead-in 0.1 s, plus every [pause: s] marker in the narration block.
- word times inside a paragraph come from durations.json (Kokoro word timestamps). If the file is missing or
  a paragraph's text changed, that paragraph falls back to a 166 wpm length-weighted estimate.
- every shot starts on a word anchor (paragraph, phrase); every layer event is a word anchor too, so the builder
  can re-time from the final mix by re-running this script with the final durations.

One global depth track (DEPTH anchors on spoken words, linear in between) drives the DepthMeter, the Ocean
darkness and the HUD in every scene, so the numbers never jump at a cut (producibility must-fix).
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EP = 'explainer-sinking-every-1000m'
GAP = 0.32
LEAD = 0.1
TAIL_HOLD = 6.0      # finished board held after the last word (PLAYBOOK: 5+ s, no spoken CTA)
EST_WPM = 166.0

# ------------------------------------------------------------------ narration + timings
SRC = open(os.path.join(HERE, 'script.md'), encoding='utf-8').read()
BLOCK = re.search(r"```narration\n(.*?)```", SRC, re.S).group(1)
RAW = [p.strip() for p in re.split(r"\n\s*\n", BLOCK) if p.strip()]
PAUSE_BEFORE = []
P = []
for raw in RAW:
    pz = sum(float(x) for x in re.findall(r"\[pause:\s*([0-9.]+)\]", raw))
    PAUSE_BEFORE.append(pz)
    P.append(re.sub(r"\s+", " ", re.sub(r"\[[^\]]*\]", " ", raw)).strip())

DUR = {}
dpath = os.path.join(HERE, 'durations.json')
if os.path.exists(dpath):
    for d in json.load(open(dpath))['paras']:
        DUR[d['text']] = d


def word_weight(w):
    core = re.sub(r"[^A-Za-z']", '', w)
    return 0.55 + 0.11 * len(core) + (0.25 if re.search(r'[,.;:?!]$', w) else 0.0)


WORDS = []   # (para 1-based, idx, word, start, end) absolute
PSTART, PEND = {}, {}
MEASURED = 0
t = LEAD
for pi, para in enumerate(P, 1):
    if pi > 1:
        t += GAP
    t += PAUSE_BEFORE[pi - 1]
    ws = para.split()
    PSTART[pi] = t
    d = DUR.get(para)
    if d and len(d['words']) == len(ws):
        MEASURED += 1
        for wi, (w, s, e) in enumerate(d['words']):
            WORDS.append((pi, wi, ws[wi], t + s, t + e))
        t += d['dur']
    else:
        dur = len(ws) / EST_WPM * 60.0
        wt = [word_weight(w) for w in ws]
        k = dur / sum(wt)
        c = t
        for wi, (w, x) in enumerate(zip(ws, wt)):
            WORDS.append((pi, wi, w, c, c + x * k * 0.9))
            c += x * k
        t += dur
    PEND[pi] = t
SPEECH_END = t
TOTAL = round(SPEECH_END + TAIL_HOLD, 2)


def norm(w):
    return re.sub(r"[^\w']", '', w).lower().replace('’', "'")


def A(pi, needle=None, end=False):
    """Absolute time of the first word of `needle` in paragraph pi (or of the paragraph); end=True -> its end."""
    ws = P[pi - 1].split()
    if needle is None:
        i = 0
    else:
        n = [norm(x) for x in needle.split()]
        for i in range(len(ws) - len(n) + 1):
            if [norm(x) for x in ws[i:i + len(n)]] == n:
                break
        else:
            raise KeyError((pi, needle))
        if end:
            i += len(n) - 1
    for p, wi, _w, s, e in WORDS:
        if p == pi and wi == i:
            return e if end else s
    raise KeyError((pi, needle))


def fmt(s):
    d = int(round(s * 10))
    return f"{d // 600}:{(d % 600) / 10:04.1f}"


# ------------------------------------------------------------------ the dive model (one global track each)
DEPTH_ANCHORS = [
    (0.0, 0), ((1, 'drops'), 0), ((4, 'Ten metres'), 10), ((7, 'red first'), 60), ((7, 'everything is blue'), 200),
    ((8, 'seven hundred'), 700), ((9, None), 740), ((10, None), 860), ((11, 'One kilometre'), 1000),
    ((13, None), 1040), ((15, None), 1250), ((15, 'twice the record'), 1400), ((16, 'past two kilometres'), 2000),
    ((17, None), 2120), ((18, 'Near three kilometres'), 2900), ((19, None), 3000), ((21, None), 3040),
    ((23, 'Nearly four kilometres'), 3700), ((25, 'Four kilometres'), 4000), ((28, None), 4300),
    ((29, None), 4500), ((30, 'Five kilometres'), 5000), ((33, 'Six kilometres'), 6000), ((36, None), 6150),
    ((38, 'Seven kilometres'), 7000), ((40, 'Eight kilometres'), 8000), ((42, 'just past that line'), 8250),
    ((43, 'through its ceiling'), 8340), ((45, 'Mount Everest'), 8849), ((47, 'Nine kilometres'), 9000),
    ((49, 'Ten kilometres'), 10000), ((50, 'thumps'), 10935), (10_000.0, 10935),
]


def _at(a):
    return a if isinstance(a, (int, float)) else A(*a)


DEPTH = sorted((_at(a), d) for a, d in DEPTH_ANCHORS)


def depth(tt):
    for (t0, d0), (t1, d1) in zip(DEPTH, DEPTH[1:]):
        if t0 <= tt <= t1:
            return d0 if t1 == t0 else d0 + (d1 - d0) * (tt - t0) / (t1 - t0)
    return DEPTH[-1][1]


# ALIVE meter state (step track) and cheats left (3 -> 0)
ALIVE = [
    (0.0, 'YES'), ((15, 'Then your hands'), 'MOSTLY'), ((16, 'It says this'), '?'), ((18, 'Near three kilometres'), 'BARELY'),
    ((19, 'No.'), 'NO'), ((20, 'a heated suit'), 'YES'), ((32, 'Mostly.'), 'MOSTLY'), ((36, 'No.'), 'NO'),
    ((37, 'the mud lets'), 'YES'), ((39, 'Barely.'), 'BARELY'), ((43, 'No.'), 'NO'), ((44, 'you borrow'), 'YES'),
    ((51, 'The needle slides'), 'BARELY'), ((51, 'Alive? Yes.'), 'YES'),
]
ALIVE = sorted((_at(a), s) for a, s in ALIVE)
CHEAT_EVENTS = sorted([(A(20, 'a heated suit'), 2), (A(37, 'the mud lets'), 1), (A(44, 'you borrow'), 0)])
STATE_COLOR = {'YES': '#3ecf6e', 'MOSTLY': '#a6d94a', '?': '#ffe14d', 'BARELY': '#ff9a2a', 'NO': '#e5483d'}


def cheats_at(tt):
    c = 3
    for te, v in CHEAT_EVENTS:
        if tt >= te:
            c = v
    return c


# ------------------------------------------------------------------ layer helpers (16:9, 1920x1080)
RED, WHITE, INK, YEL, GRN, ORG = '#e5483d', '#f3f6f7', '#0b1a22', '#ffe14d', '#3ecf6e', '#ff9a2a'
PX = 200  # px per metre for You two-shots (You ~350 px tall)


def comp(name, x, y, w, h, props=None, **kw):
    d = {'type': 'component', 'name': name, 'x': x, 'y': y, 'width': w, 'height': h, 'props': props or {}}
    d.update(kw)
    return d


def headline(text, at, out=None, y=150, color='white', size=84, w=1400, **kw):
    p = {'text': text, 'at': at, 'size': size, 'color': color, 'underline': True}
    if out is not None:
        p['out'] = out
    return comp('explainer/Headline', '50%', y, w, 240, p, depth=0, z=40, **kw)


def tag(text, x, y, at, out=None, accent=RED, size=34, w=640, **kw):
    p = {'text': text, 'at': at, 'size': size, 'accent': accent}
    if out is not None:
        p['out'] = out
    return comp('explainer/Tag', x, y, w, 90, p, depth=0, z=38, **kw)


def stat(value, at, suffix='', label=None, x='50%', y=300, color=RED, size=110, prefix=None, frm=None, dur=0.8, out=None, w=760):
    p = {'value': value, 'suffix': suffix, 'at': at, 'duration': dur, 'size': size, 'color': color}
    if label:
        p['label'] = label
    if prefix:
        p['prefix'] = prefix
    if frm is not None:
        p['from'] = frm
    if out is not None:
        p['out'] = out
    return comp('explainer/Stat', x, y, w, 300, p, depth=0, z=39)


def you(x, y, pose='stand', px=PX, color=None, **kw):
    p = {'pose': pose, 'pxPerM': px, 'align': 'bottom'}
    if color:
        p['color'] = color
    kw.setdefault('z', 12)
    return comp('explainer/You', x, y, int(0.9 * px) + 60, int(1.75 * px) + 30, p, **kw)


def svg(markup, x, y, w, h, **kw):
    d = {'type': 'svg', 'markup': markup, 'x': x, 'y': y, 'width': w, 'height': h}
    d.update(kw)
    return d


def circle(x, y, dia, fill, **kw):
    d = {'type': 'circle', 'x': x, 'y': y, 'width': dia, 'height': dia, 'fill': fill}
    d.update(kw)
    return d


def rect(x, y, w, h, fill, **kw):
    d = {'type': 'rect', 'x': x, 'y': y, 'width': w, 'height': h, 'fill': fill}
    d.update(kw)
    return d


def text(s, x, y, at=0, size=48, color=WHITE, **kw):
    d = {'type': 'text', 'text': s, 'x': x, 'y': y, 'fontSize': size, 'color': color, 'start': at}
    d.update(kw)
    return d


def parts(preset, x, y, w, h, count, color=None, size=None, speed=1.0, **kw):
    d = {'type': 'particles', 'preset': preset, 'x': x, 'y': y, 'width': w, 'height': h, 'count': count, 'speed': speed}
    if color:
        d['color'] = color
    if size:
        d['size'] = size
    d.update(kw)
    return d


def kf(*pairs):
    return [dict(t=round(tt, 3), **v) for tt, v in pairs]


def fig(name, x, y, w, h, px, **kw):
    """Kit figure at true scale (pxPerM shared with You = honest comparison)."""
    props = {'pxPerM': px, 'align': kw.pop('align', 'center')}
    props.update(kw.pop('props', {}))
    kw.setdefault('z', 10)
    return comp(f'explainer/{name}', x, y, w, h, props, **kw)


# ------------------------------------------------------------------ static inline art (rigid; motion = layer keyframes)
SLED = ('<svg viewBox="0 0 300 90" xmlns="http://www.w3.org/2000/svg"><rect x="10" y="10" width="280" height="22" rx="6" fill="#f2c230"/>'
        '<rect x="30" y="32" width="18" height="40" fill="#c99a1c"/><rect x="252" y="32" width="18" height="40" fill="#c99a1c"/>'
        '<rect x="20" y="66" width="260" height="20" rx="4" fill="#4d5560"/><rect x="60" y="70" width="40" height="12" fill="#2f353d"/>'
        '<rect x="130" y="70" width="40" height="12" fill="#2f353d"/><rect x="200" y="70" width="40" height="12" fill="#2f353d"/></svg>')
BOAT = ('<svg viewBox="0 0 900 360" xmlns="http://www.w3.org/2000/svg"><path d="M40 250 L860 250 L790 340 L110 340 Z" fill="#e9eef2"/>'
        '<rect x="300" y="170" width="260" height="80" fill="#d23c32"/><rect x="330" y="190" width="40" height="30" fill="#9fd3ff"/>'
        '<rect x="390" y="190" width="40" height="30" fill="#9fd3ff"/><path d="M640 250 L660 40 L840 40" stroke="#f2c230" stroke-width="16" fill="none"/>'
        '<path d="M840 40 L840 100" stroke="#2f353d" stroke-width="4"/></svg>')
FINGERTIP = ('<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg"><rect x="20" y="20" width="360" height="360" rx="24" fill="#e8b48f"/>'
             '<path d="M70 120 Q200 60 330 120 M60 200 Q200 140 340 200 M70 280 Q200 220 330 280" stroke="#c48d6a" stroke-width="8" fill="none"/>'
             '<rect x="20" y="20" width="360" height="360" rx="24" fill="none" stroke="#f3f6f7" stroke-width="6" stroke-dasharray="18 12"/></svg>')
PIANO = ('<svg viewBox="0 0 420 260" xmlns="http://www.w3.org/2000/svg"><path d="M10 60 L300 60 Q410 60 410 150 L410 190 L10 190 Z" fill="#14161a"/>'
         '<rect x="10" y="190" width="160" height="26" fill="#f3f6f7"/><g fill="#14161a"><rect x="24" y="190" width="10" height="16"/><rect x="50" y="190" width="10" height="16"/>'
         '<rect x="90" y="190" width="10" height="16"/><rect x="116" y="190" width="10" height="16"/><rect x="142" y="190" width="10" height="16"/></g>'
         '<rect x="30" y="216" width="14" height="44" fill="#14161a"/><rect x="380" y="190" width="14" height="70" fill="#14161a"/>'
         '<path d="M40 60 L230 0" stroke="#14161a" stroke-width="10"/></svg>')
COW = ('<svg viewBox="0 0 440 300" xmlns="http://www.w3.org/2000/svg"><rect x="60" y="70" width="290" height="140" rx="50" fill="#f3f6f7"/>'
       '<path d="M120 90 Q160 70 190 110 Q170 160 120 140 Z M250 150 Q300 120 320 170 Q280 200 250 190 Z" fill="#14161a"/>'
       '<rect x="340" y="40" width="90" height="80" rx="30" fill="#f3f6f7"/><rect x="380" y="90" width="56" height="40" rx="18" fill="#f2a7a0"/>'
       '<circle cx="372" cy="70" r="7" fill="#14161a"/><path d="M350 40 L340 14 M410 40 L424 14" stroke="#c9b48a" stroke-width="10"/>'
       '<g fill="#f3f6f7"><rect x="90" y="200" width="26" height="90"/><rect x="140" y="200" width="26" height="90"/><rect x="270" y="200" width="26" height="90"/>'
       '<rect x="310" y="200" width="26" height="90"/></g><path d="M60 110 Q20 140 30 200" stroke="#f3f6f7" stroke-width="10" fill="none"/></svg>')
CHAMBER = ('<svg viewBox="0 0 520 360" xmlns="http://www.w3.org/2000/svg"><rect x="20" y="40" width="480" height="280" rx="140" fill="#8a97a1"/>'
           '<rect x="40" y="60" width="440" height="240" rx="120" fill="#5f6b74"/><circle cx="420" cy="180" r="70" fill="#2b3239" stroke="#c7d0d6" stroke-width="16"/>'
           '<circle cx="420" cy="180" r="44" fill="#9fd3ff" opacity=".35"/><rect x="200" y="320" width="120" height="30" fill="#4d5560"/>'
           '<text x="150" y="200" font-family="Montserrat,Arial" font-weight="900" font-size="40" fill="#e9eef2">HYDRA</text></svg>')
SUB = ('<svg viewBox="0 0 300 160" xmlns="http://www.w3.org/2000/svg"><rect x="20" y="40" width="240" height="90" rx="45" fill="#f2c230"/>'
       '<rect x="110" y="16" width="70" height="34" rx="10" fill="#f2c230"/><circle cx="90" cy="85" r="22" fill="#9fd3ff" stroke="#2f353d" stroke-width="6"/>'
       '<circle cx="160" cy="85" r="22" fill="#9fd3ff" stroke="#2f353d" stroke-width="6"/><path d="M260 70 L290 50 L290 120 L260 100 Z" fill="#c99a1c"/></svg>')
STRIKE = '<svg viewBox="0 0 400 40" xmlns="http://www.w3.org/2000/svg"><rect x="0" y="10" width="400" height="20" rx="10" fill="#e5483d"/></svg>'
FROST = ('<svg viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="f" cx="50%" cy="50%" r="70%">'
         '<stop offset="55%" stop-color="#dff4ff" stop-opacity="0"/><stop offset="100%" stop-color="#dff4ff" stop-opacity=".75"/></radialGradient></defs>'
         '<rect width="1920" height="1080" fill="url(#f)"/></svg>')
VIGNETTE = ('<svg viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="v" cx="50%" cy="50%" r="65%">'
            '<stop offset="40%" stop-color="#000" stop-opacity="0"/><stop offset="100%" stop-color="#000" stop-opacity=".95"/></radialGradient></defs>'
            '<rect width="1920" height="1080" fill="url(#v)"/></svg>')
SECTION = ('<svg viewBox="0 0 1600 900" xmlns="http://www.w3.org/2000/svg"><rect width="1600" height="900" fill="#0b2a3a"/>'
           '<path d="M0 330 L560 330 L700 860 L840 880 L980 330 L1600 330 L1600 900 L0 900 Z" fill="#3b2f28"/>'
           '<path d="M0 330 L560 330" stroke="#c9b48a" stroke-width="6" stroke-dasharray="20 14"/><path d="M980 330 L1600 330" stroke="#c9b48a" stroke-width="6" stroke-dasharray="20 14"/>'
           '<rect x="0" y="0" width="1600" height="12" fill="#9fd3ff"/></svg>')
WALL = ('<svg viewBox="0 0 700 2400" xmlns="http://www.w3.org/2000/svg"><path d="M0 0 L380 0 Q430 200 400 380 Q470 600 430 820 Q520 1040 470 1260 '
        'Q560 1480 500 1700 Q590 1920 540 2140 Q600 2300 580 2400 L0 2400 Z" fill="#3a2e26" stroke="#5a4a3e" stroke-width="10"/>'
        '<g fill="#3b2f28"><ellipse cx="300" cy="260" rx="60" ry="22"/><ellipse cx="340" cy="700" rx="80" ry="26"/><ellipse cx="380" cy="1150" rx="70" ry="24"/>'
        '<ellipse cx="420" cy="1600" rx="90" ry="28"/><ellipse cx="460" cy="2050" rx="70" ry="22"/></g></svg>')
SHELL = ('<svg viewBox="0 0 120 100" xmlns="http://www.w3.org/2000/svg"><path d="M10 90 Q60 -20 110 90 Z" fill="#f2e3c6"/>'
         '<path d="M60 90 L60 20 M35 90 L45 35 M85 90 L75 35" stroke="#c9b48a" stroke-width="5"/></svg>')
CAMFRAME = ('<svg viewBox="0 0 1500 840" xmlns="http://www.w3.org/2000/svg"><rect x="8" y="8" width="1484" height="824" fill="none" stroke="#f3f6f7" stroke-width="6"/>'
            '<path d="M8 90 L8 8 L90 8 M1410 8 L1492 8 L1492 90 M8 750 L8 832 L90 832 M1410 832 L1492 832 L1492 750" stroke="#f3f6f7" stroke-width="16" fill="none"/>'
            '<circle cx="70" cy="70" r="14" fill="#e5483d"/><text x="100" y="84" font-family="Montserrat,Arial" font-weight="800" font-size="40" fill="#f3f6f7">BAIT CAM</text></svg>')
MUDFLOOR = ('<svg viewBox="0 0 1920 300" xmlns="http://www.w3.org/2000/svg"><path d="M0 80 Q480 40 960 70 Q1440 100 1920 60 L1920 300 L0 300 Z" fill="#3b2f28"/>'
            '<path d="M0 80 Q480 40 960 70 Q1440 100 1920 60" stroke="#5a4a3e" stroke-width="10" fill="none"/></svg>')
BONES = ('<svg viewBox="0 0 500 160" xmlns="http://www.w3.org/2000/svg"><g stroke="#e9eef2" stroke-width="10" stroke-linecap="round" fill="none">'
         '<path d="M40 80 L420 80"/><path d="M110 80 L80 30 M110 80 L80 130 M170 80 L145 25 M170 80 L145 135 M230 80 L210 25 M230 80 L210 135 M290 80 L275 30 M290 80 L275 130 M350 80 L340 40 M350 80 L340 120"/>'
         '<path d="M420 80 L480 40 M420 80 L480 120"/></g><circle cx="40" cy="80" r="34" fill="none" stroke="#e9eef2" stroke-width="10"/></svg>')
COL_TOP = 80


def COLY(d):
    return COL_TOP + 960 * d / 10935


COLUMN = ('<svg viewBox="0 0 900 1000" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">'
          '<stop offset="0" stop-color="#1f6f8b"/><stop offset=".15" stop-color="#0b2a3a"/><stop offset="1" stop-color="#03080b"/></linearGradient></defs>'
          '<rect x="0" y="40" width="900" height="960" fill="url(#g)"/><rect x="0" y="0" width="900" height="40" fill="#9fd3ff"/>'
          '<path d="M0 40 L900 40" stroke="#f3f6f7" stroke-width="4"/><path d="M0 1000 L900 1000" stroke="#e5483d" stroke-width="8"/></svg>')
EVEREST = ('<svg viewBox="0 0 800 800" xmlns="http://www.w3.org/2000/svg"><path d="M0 800 L330 75 L400 0 L470 88 L800 800 Z" fill="#6b7a86"/>'
           '<path d="M330 75 L400 0 L470 88 L440 150 L405 112 L370 162 Z" fill="#f3f6f7"/></svg>')  # square viewBox: SvgMarkup scales with "meet"
BAG = ('<svg viewBox="0 0 300 340" xmlns="http://www.w3.org/2000/svg"><path d="M60 110 Q40 80 70 40 Q90 20 100 70 L200 70 Q210 20 230 40 Q260 80 240 110 '
       'L270 300 Q150 340 30 300 Z" fill="#f3f6f7" opacity=".9"/><path d="M80 140 Q150 170 220 140 M70 220 Q160 250 240 210" stroke="#c7d0d6" stroke-width="6" fill="none"/></svg>')
BLOB = ('<svg viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg"><path d="M60 140 Q50 60 140 70 Q230 40 250 130 Q280 220 180 250 Q80 280 60 200 Z" '
        'fill="none" stroke="#8a97a1" stroke-width="8" stroke-dasharray="14 10"/></svg>')
BRANCH = ('<svg viewBox="0 0 700 200" xmlns="http://www.w3.org/2000/svg"><path d="M10 120 L690 90" stroke="#6b4a2e" stroke-width="36" stroke-linecap="round"/>'
          '<path d="M260 110 L330 40 M460 100 L520 30" stroke="#6b4a2e" stroke-width="18" stroke-linecap="round"/></svg>')
XRAY_GUT = ('<svg viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg"><ellipse cx="200" cy="100" rx="180" ry="80" fill="none" stroke="#7fe3ff" stroke-width="6" stroke-dasharray="10 8"/>'
            '<g fill="#8a6a3e"><rect x="120" y="80" width="40" height="14" rx="4"/><rect x="190" y="110" width="50" height="12" rx="4"/><rect x="250" y="70" width="30" height="12" rx="4"/></g>'
            '<circle cx="170" cy="125" r="7" fill="#8a97a1"/></svg>')
FIBRES = ('<svg viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg"><g stroke="#e5483d" stroke-width="5" fill="none" stroke-linecap="round">'
          '<path d="M120 120 Q150 90 180 130 Q210 160 240 120"/><path d="M150 70 Q190 100 230 70"/><path d="M200 140 Q240 110 280 140"/>'
          '<path d="M110 90 Q130 60 160 80"/></g></svg>')
XENO = ('<svg viewBox="0 0 800 220" xmlns="http://www.w3.org/2000/svg"><g fill="#c9b48a" stroke="#8a7550" stroke-width="5">'
        '<path d="M60 200 Q40 120 110 100 Q170 70 200 140 Q230 200 150 210 Z"/><path d="M380 210 Q350 110 450 90 Q540 90 530 170 Q520 220 430 215 Z"/>'
        '<path d="M650 205 Q640 150 690 140 Q740 140 745 190 Q740 215 690 212 Z"/></g>'
        '<g fill="#8a7550"><circle cx="120" cy="150" r="6"/><circle cx="450" cy="150" r="7"/><circle cx="480" cy="180" r="5"/><circle cx="690" cy="180" r="5"/></g></svg>')
PROTEIN = ('<svg viewBox="0 0 600 300" xmlns="http://www.w3.org/2000/svg"><path d="M30 150 Q80 40 130 150 T230 150 T330 150 T430 150 T530 150 Q560 200 580 150" '
           'stroke="#ffe14d" stroke-width="20" fill="none" stroke-linecap="round"/></svg>')
MEMBRANE = ('<svg viewBox="0 0 900 140" xmlns="http://www.w3.org/2000/svg"><g fill="#7fe3ff">' +
            ''.join(f'<circle cx="{30 + i * 42}" cy="30" r="14"/><circle cx="{30 + i * 42}" cy="110" r="14"/>' for i in range(21)) +
            '</g><g stroke="#7fe3ff" stroke-width="5">' + ''.join(f'<path d="M{30 + i * 42} 44 L{30 + i * 42} 96"/>' for i in range(21)) + '</g></svg>')
PLATES = ('<svg viewBox="0 0 1500 600" xmlns="http://www.w3.org/2000/svg"><rect width="1500" height="200" fill="#0b2a3a"/>'
          '<path d="M0 200 L820 200 L840 240 L0 240 Z" fill="#6b5a4c"/><path d="M840 240 L1500 200 L1500 260 L860 300 Z" fill="#8a6a50"/>'
          '<text x="160" y="320" font-family="Montserrat,Arial" font-weight="800" font-size="40" fill="#f3f6f7">PHILIPPINE SEA PLATE</text>'
          '<text x="980" y="380" font-family="Montserrat,Arial" font-weight="800" font-size="40" fill="#f3f6f7">PACIFIC PLATE</text>'
          '<path d="M1300 330 L1000 420" stroke="#e5483d" stroke-width="14" marker-end="url(#a)"/><defs><marker id="a" viewBox="0 0 10 10" refX="5" refY="5" '
          'markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0 L10 5 L0 10 Z" fill="#e5483d"/></marker></defs></svg>')
THUMB = ('<svg viewBox="0 0 260 500" xmlns="http://www.w3.org/2000/svg"><path d="M40 500 L40 140 Q40 30 130 30 Q220 30 220 140 L220 500 Z" fill="#e8b48f"/>'
         '<path d="M70 90 Q130 50 190 90 L190 170 Q130 190 70 170 Z" fill="#f6d5bd"/><path d="M50 250 Q130 270 210 250" stroke="#c48d6a" stroke-width="8" fill="none"/></svg>')
ROV_LIGHT = ('<svg viewBox="0 0 1000 800" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="l" cx="50%" cy="55%" r="50%">'
             '<stop offset="0" stop-color="#fff6d8" stop-opacity=".55"/><stop offset="1" stop-color="#fff6d8" stop-opacity="0"/></radialGradient></defs>'
             '<ellipse cx="500" cy="440" rx="480" ry="340" fill="url(#l)"/></svg>')
MUDCLOUD = ('<svg viewBox="0 0 1920 1400" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="m" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#4a3a2e" stop-opacity="0"/><stop offset=".35" stop-color="#4a3a2e" stop-opacity=".95"/>'
            '<stop offset="1" stop-color="#2a221d" stop-opacity="1"/></linearGradient></defs><rect width="1920" height="1400" fill="url(#m)"/></svg>')

OCEAN_DEFAULT = {'rays': 7, 'snow': 70, 'falloff': 260}


def ocean_bg(d0, d1, dur, **extra):
    props = dict(OCEAN_DEFAULT)
    props['depth'] = [{'t': 0, 'v': round(d0)}, {'t': round(dur, 3), 'v': round(d1)}]
    props.update(extra)
    return {'type': 'component', 'name': 'explainer/Ocean', 'depth': 0.12, 'overscan': 1.2, 'props': props}


BLACK = {'type': 'color', 'color': '#04080b'}
DARK = {'type': 'gradient', 'kind': 'linear', 'angle': 180, 'colors': ['#071722', '#02060a']}

ZONES = [{'from': 200, 'to': 1000, 'label': 'TWILIGHT', 'color': '#2f7fa3'},
         {'from': 1000, 'to': 4000, 'label': 'MIDNIGHT', 'color': '#1d4a66'},
         {'from': 4000, 'to': 6000, 'label': 'ABYSS', 'color': '#3a3f6b'},
         {'from': 6000, 'to': 11000, 'label': 'HADAL', 'color': '#7a2a2a'}]
MARKERS = [{'depth': 701, 'label': 'HUMAN RECORD 701 M', 'color': RED}, {'depth': 2992, 'label': 'BEAKED WHALE 2,992 M', 'color': WHITE},
           {'depth': 3700, 'label': 'AVERAGE SEAFLOOR', 'color': '#c9b48a'}, {'depth': 6957, 'label': 'DEEPEST OCTOPUS', 'color': WHITE},
           {'depth': 8200, 'label': 'FISH LIMIT ~8,200 M', 'color': RED}, {'depth': 8849, 'label': 'ONE EVEREST', 'color': WHITE},
           {'depth': 10935, 'label': 'CHALLENGER DEEP', 'color': RED}]

# ------------------------------------------------------------------ shots
SHOTS = []


def shot(sid, anchor, kind, desc, bg='ocean', layers=None, camera='drift', amount=0.5, trans='cut', sfx=(), hud=True,
         wall=False, sled=True, you_pose='stand', you_color=None, notes='', grade=None, you_kf=None, you_idle=True, you_at=(720, 640, PX)):
    """bg: 'ocean' (depth-matched), 'black', 'dark', or a background dict. layers: fn(T, L) -> list, where
    T(pi, needle) -> scene-local time of a word and L is the scene length. sled: draw You on the sled (centre-left)."""
    SHOTS.append(dict(id=sid, t0=_at(anchor), kind=kind, desc=desc, bg=bg, layers=layers, camera=camera, amount=amount,
                      trans=trans, sfx=list(sfx), hud=hud, wall=wall, sled=sled, you_pose=you_pose, you_color=you_color,
                      notes=notes, grade=grade, you_kf=you_kf, you_idle=you_idle, you_at=you_at))


SUIT = '#ff8a2a'   # heated suit colour from cheat 1 on


def suit_on(t0):
    return t0 >= A(20, 'a heated suit')


# ---- P01-P03 hook, teasers, master question
shot('s01_surface', 0.0, 'wide, cross-section', 'Bright Pacific surface; tiny boat crane holds YOU strapped to the yellow sled; 5 s Timer ring hits 0 on "drops"; Tag MARIANA TRENCH',
     bg={'type': 'component', 'name': 'explainer/Ocean', 'depth': 0.12, 'overscan': 1.2, 'props': {'depth': 0, 'surface': 0.55, 'rays': 7, 'snow': 30}},
     layers=lambda T, L: [svg(BOAT, 1110, 440, 900, 360, z=6),
                          comp('explainer/Timer', 1720, 190, 280, 280, {'from': 5, 'to': 0, 'at': 0.0, 'rate': 5 / max(0.5, T(1, 'drops')), 'style': 'ring', 'format': 's', 'label': 'DROP', 'warnBelow': 3}, depth=0, z=40),
                          tag('MARIANA TRENCH, PACIFIC', 330, 120, 0.2, accent=WHITE, w=560)],
     camera='drift', amount=0.3, hud=False, sled=True, sfx=[('underwater_rumble', 0.0, 0.35), ('tick', 1.0, 0.3), ('tick', 2.0, 0.3), ('tick', 3.0, 0.3), ('tick', 4.0, 0.3)],
     you_at=(1500, 590, 110), notes='Frame 1 = thumbnail A composition. The sled hangs from the crane at the waterline; You pose stand. The ring empties exactly on "drops" (rate set from the word time).')
shot('s02_drop', (1, 'drops'), 'tilt-down reveal', 'Latch opens; sled + YOU plunge through the waterline in bubbles; the column darkens; DepthMeter slides in; red Headline 11 KM on "eleven"',
     bg={'type': 'component', 'name': 'explainer/Ocean', 'depth': 0.12, 'overscan': 1.2, 'props': {'depth': [{'t': 0, 'v': 0}, {'t': 4, 'v': 30}], 'surface': [{'t': 0, 'v': 0.55}, {'t': 1.2, 'v': -0.2}], 'rays': 7, 'snow': 60}},
     layers=lambda T, L: [parts('bubbles', '40%', '55%', 700, 700, 80, speed=1.6, start=0.0, end=2.5),
                          headline('11 KM DOWN', T(2, 'eleven'), color='red', size=110)],
     camera='panDown', amount=0.8, sfx=[('bubbles', 0.05, 0.7), ('whoosh_long', 0.1, 0.6), ('riser', 1.2, 0.35)],
     notes='The release is on the word "drops" (hook contract kept: the drop happens at 0:05). From here the HUD DepthMeter is on screen.',
     you_at=(1500, 590, 110), you_kf=[{'t': 0, 'x': 1500, 'feet': 590}, {'t': 1.4, 'x': 1150, 'feet': 1300, 'ease': 'in'}])
shot('t1_eye', (2, 'a squid'), 'teaser card 1', 'Squid silhouette, one huge eye glints; Tag AN EYE WIDER THAN YOUR FACE', bg='black',
     layers=lambda T, L: [fig('ColossalSquid', '52%', '52%', 1300, 520, 120, props={'silhouette': '#1b2a33', 'hooks': False, 'variant': 'giant'}),
                          circle('36%', '50%', 120, '#e9f6ff', opacity=0.9, keyframes=kf((0.2, {'scale': 0.2}), (0.6, {'scale': 1.0, 'ease': 'backOut'})), z=11),
                          tag('AN EYE WIDER THAN YOUR FACE', '50%', 820, 0.15, accent=WHITE, w=860)],
     camera='pushIn', amount=0.6, hud=False, sled=False, sfx=[('whoosh', 0.0, 0.5)])
shot('t2_whale', (2, 'a whale'), 'teaser card 2', 'Beaked-whale silhouette; Tag ONE BREATH LONGER THAN YOUR WHOLE TRIP', bg='black',
     layers=lambda T, L: [fig('BeakedWhale', '50%', '50%', 1300, 420, 190, props={'silhouette': '#1b2a33'},
                              keyframes=kf((0, {'x': '58%'}), (L, {'x': '44%', 'ease': 'linear'}))),
                          tag('ONE BREATH > YOUR WHOLE TRIP', '50%', 820, 0.15, accent=WHITE, w=860)],
     camera='pushIn', amount=0.5, hud=False, sled=False, sfx=[('whoosh', 0.0, 0.5)])
shot('t3_fish', (2, 'the last fish'), 'teaser card 3', 'Pale pink snailfish alone on black; Tag THE LAST FISH', bg='black',
     layers=lambda T, L: [fig('Snailfish', '50%', '50%', 900, 360, 2600),
                          tag('THE LAST FISH ON THE PLANET', '50%', 820, 0.15, accent=WHITE, w=860)],
     camera='pushIn', amount=0.5, hud=False, sled=False, sfx=[('whoosh', 0.0, 0.5)])
shot('t4_unknown', (2, 'and, almost'), 'teaser card 4', 'Black frame, a dashed grey outline that reads as nothing; red Headline ?', bg='black',
     layers=lambda T, L: [svg(BLOB, '50%', '52%', 360, 360, opacity=0.8), headline('?', 0.3, y='50%', color='red', size=220)],
     camera='pushIn', amount=0.4, hud=False, sled=False, sfx=[('stinger', 0.3, 0.6)],
     notes='Keep the outline unreadable (retention nice-to-have): a lumpy dashed loop, no handles, no bag shape.')
shot('s03_question', (3, None), 'title card', 'YOU sinking small in blue; Headline HOW MANY TIMES DOES THE OCEAN KILL YOU?; Tag LET\'S COUNT; DEATHS counter 0 appears',
     layers=lambda T, L: [headline('HOW MANY TIMES DOES\nTHE OCEAN KILL YOU?', 0.1, size=76),
                          stat(0, T(3, 'count'), label='DEATHS', x=1250, y=560, color=RED, size=90, w=360)],
     camera='pushIn', amount=0.4, sfx=[('riser', 0.0, 0.35), ('ding', (3, 'count'), 0.4)],
     notes='Master question asked aloud (reference nice-to-have); it is the title and the thing the final board answers.')

# ---- P04-P06 rung 1 entry + rules + format reveal
RULES = ['YOU CAN BREATHE', 'DIE = USE A CHEAT', 'NO SUBMARINE']


def rules_layer(visible_from):
    return comp('explainer/Options', 1190, 500, 660, 400, {'title': 'THE RULES', 'items': RULES, 'at': -1, 'itemAt': visible_from, 'size': 36},
                depth=0, z=30)


shot('s04_ears', (4, None), 'medium, you vs water', 'Ocean 10 m, rays; YOU panic then pop; Tag PRESSURE x2 (first felt rung at 0:28)',
     layers=lambda T, L: [tag('10 M: PRESSURE x2', 1100, 300, 0.2, w=520), tag('PINCH · BLOW · POP', 1100, 400, T(4, 'Pinch'), accent=WHITE, w=460),
                          circle(760, 420, 60, '#e9f6ff', start=T(4, 'pop.'), keyframes=kf((T(4, 'pop.'), {'scale': 0.2, 'opacity': 1}), (T(4, 'pop.') + 0.4, {'scale': 2.2, 'opacity': 0, 'ease': 'out'})), z=20)],
     you_pose='panic', camera='pushIn', amount=0.6, sfx=[('pop', 'pop.', 0.8)],
     notes='You pose panic until "pop", then stand (pose switch at the next shot). Rays bright, colours still full.')
shot('s05_rule1', (4, 'And yes'), 'rules card', 'Options THE RULES, item 1 YOU CAN BREATHE lands; YOU shrug',
     layers=lambda T, L: [rules_layer([0.2, 999, 999])], you_pose='shrug', sfx=[('click', 0.2, 0.6)])
shot('s06_rule2', (5, None), 'rules card + HUD build', 'Item 2 lands; ALIVE meter slides in left; CHEATS LEFT 3 top-left on "three"',
     layers=lambda T, L: [rules_layer([-1, 0.2, 999]), tag('YOU GET 3', 1190, 740, T(5, 'only get three,'), accent=WHITE, w=300),
                          tag('ALL GONE = TRIP OVER', 1190, 830, T(5, "when they're gone,"), accent=RED, w=440)], you_pose='stand', sfx=[('click', 0.2, 0.6), ('ding', 'three,', 0.4)],
     notes='HUD: AliveMeter enters with this shot (0:40) and CHEATS LEFT 3 appears on "three".')
shot('s07_meter', (5, "That's what this meter"), 'HUD close-up', 'AliveMeter big centre-screen, needle settles on YES with a green stamp; Headline ARE YOU STILL ALIVE?',
     bg='dark', layers=lambda T, L: [comp('explainer/AliveMeter', '50%', '56%', 520, 620, {'state': 'YES', 'stamp': [{'at': T(5, 'yes.'), 'text': 'YES', 'color': GRN}], 'size': 1.6}, depth=0, z=30),
                                     headline('ARE YOU STILL ALIVE?', 0.1, size=72)],
     sled=False, camera='pushIn', amount=0.4, sfx=[('ding', 'yes.', 0.6)])
shot('s08_rule3', (6, None), 'rules card', 'Item 3 NO SUBMARINE lands; yellow sub slides in and is struck red; small kit Bus with Tag FEWER VISITORS THAN BUS SEATS',
     layers=lambda T, L: [rules_layer([-1, -1, 0.2]),
                          svg(SUB, 460, 520, 220, 117, keyframes=kf((0, {'x': -300}), (0.6, {'x': 460, 'ease': 'out'})), z=20),
                          svg(STRIKE, 460, 520, 260, 30, rotate=-12, start=0.9, enter={'type': 'wipeRight', 'duration': 0.3}, z=21),
                          fig('Bus', 1190, 760, 360, 140, 28, align='bottom', start=T(6, 'Fewer people')),
                          tag('EVER BEEN TO THE BOTTOM: FEWER THAN A BUSLOAD', '50%', 840, T(6, 'Fewer people'), accent=WHITE, w=1100, size=30, out=T(6, 'all of them')),
                          tag('ALL OF THEM INSIDE A SUB', '50%', 840, T(6, 'all of them'), accent=WHITE, w=600, size=30, out=T(6, 'so you\'ll be')),
                          headline('YOU: THE FIRST WITHOUT ONE', T(6, 'first thing'), color='#ffe14d', size=60, y=830)],
     sled=False, sfx=[('click', 0.2, 0.6), ('pop', 0.9, 0.6)])
shot('s09_rate', (6, 'At this slow walking pace'), 'stat callouts', 'YOU on sled sinking; Stat 1 M/S SINK RATE; Stat ~3 HOURS TO THE BOTTOM',
     layers=lambda T, L: [stat(1, 0.2, suffix=' M/S', label='SINK RATE (SLOW WALK)', x=1150, y=330, size=90, w=620),
                          stat(3, T(6, 'three hours.'), prefix='~', suffix=' HOURS', label='TO THE BOTTOM', x=1150, y=650, size=90, w=620)],
     sfx=[('tick', 0.2, 0.5), ('tick', 'three hours.', 0.5)])

# ---- P07-P12 rung 1 (0-1 km)
shot('s10_colours', (7, None), 'wide, falling', 'Ocean depth 10->200; Options COLOURS LEFT [RED ORANGE YELLOW GREEN BLUE], strikes on each spoken colour; zone TWILIGHT lights; silent landmark Tag 330 M = 1 EIFFEL TOWER',
     layers=lambda T, L: [comp('explainer/Options', 1150, 520, 640, 520, {'title': 'COLOURS LEFT', 'items': ['RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE'], 'at': -1, 'itemAt': [-1] * 5, 'size': 40,
                                                                       'strikes': [{'index': 0, 'at': T(7, 'red')}, {'index': 1, 'at': T(7, 'orange,')}, {'index': 2, 'at': T(7, 'yellow,')}, {'index': 3, 'at': T(7, 'blue.')}]}, depth=0, z=30),
                          tag('TWILIGHT ZONE', 1150, 150, T(7, 'twilight'), accent='#2f7fa3', w=480)],
     camera='panDown', amount=0.5, sfx=[('whoosh_long', 0.0, 0.4), ('tick', 'red', 0.4), ('tick', 'orange,', 0.4), ('tick', 'yellow,', 0.4)])
shot('s11_record', (8, None), 'record card', 'Pressure chamber (HYDRA) with a figure inside; Stat 701 M DEEPEST PRESSURE A HUMAN HAS FELT (1992, CHAMBER); silent Tag 330 M = 1 EIFFEL TOWER passes',
     layers=lambda T, L: [svg(CHAMBER, 1120, 520, 620, 430, z=20, enter={'type': 'slideLeft', 'duration': 0.4}),
                          you(1080, 600, 'stand', px=90, z=21), tag('TEST CHAMBER, FRANCE', 1120, 800, T(8, 'French test chamber'), accent=WHITE, w=420, size=28),
                          stat(701, T(8, 'record.'), suffix=' M', label='DEEPEST PRESSURE A HUMAN HAS FELT (1992)', x=1120, y=200, size=80, w=900),
                          tag('330 M: ONE EIFFEL TOWER DOWN', 300, 980, 0.2, accent=WHITE, size=26, w=480, out=2.5)],
     sfx=[('tick', 'record.', 0.6)])
shot('s12_limit', (8, 'and no human'), 'threshold', 'Red dashed HUMAN LIMIT line scrolls up past YOU; DepthMeter flag at 701 m; Headline NO HUMAN HAS FELT MORE',
     layers=lambda T, L: [rect('50%', 0, 1920, 8, RED, keyframes=kf((0, {'y': 900}), (L, {'y': 300, 'ease': 'linear'})), z=8),
                          text('HUMAN LIMIT', 1300, 0, 0, size=34, color=RED, keyframes=kf((0, {'y': 870}), (L, {'y': 270, 'ease': 'linear'})), z=8),
                          headline('NO HUMAN HAS FELT MORE', 0.1, size=70)],
     camera='pushIn', amount=0.4, sfx=[('drone', 0.0, 0.35)])
shot('s13_clicks', (9, None), 'sound reveal', 'Near-black; sonar rings pulse across the frame; YOU jitters with each click; Tag CLICK CLICK CLICK',
     layers=lambda T, L: [circle('70%', '45%', 200, 'rgba(0,0,0,0)', stroke='#7fe3ff', strokeWidth=6, start=i * 0.8,
                                 keyframes=kf((i * 0.8, {'scale': 0.2, 'opacity': 0.9}), (i * 0.8 + 1.6, {'scale': 6, 'opacity': 0, 'ease': 'out'})), z=5) for i in range(5)]
                         + [tag('CLICK  CLICK  CLICK', 1150, 300, 0.3, accent='#7fe3ff', w=520)],
     you_idle=False, sfx=[('click', 0.0, 0.7), ('click', 0.8, 0.7), ('click', 1.6, 0.7), ('click', 2.4, 0.7), ('sonar_ping', 3.2, 0.5)],
     notes='You layer gets a jitter idle in this shot (vibrating with the clicks).')
shot('s14_whale', (9, 'A sperm whale'), 'creature pass', 'SpermWhale at shared pxPerM (16 m vs 1.75 m) glides L->R behind YOU; Tag LOUDEST ANIMAL ON EARTH; silent Tag 828 M = 1 BURJ KHALIFA DOWN',
     layers=lambda T, L: [fig('SpermWhale', '50%', '40%', 1100, 300, 60, keyframes=kf((0, {'x': -400}), (L, {'x': 1500, 'ease': 'linear'})), z=6),
                          tag('SPERM WHALE', 1200, 160, 0.3, accent=WHITE, w=420),
                          tag('LOUDEST ANIMAL ON EARTH', 1200, 250, T(9, 'loudest'), w=560),
                          tag('828 M: ONE BURJ KHALIFA DOWN', 300, 980, 0.4, accent=WHITE, size=26, w=480, out=3.0)],
     camera='panRight', amount=0.4, you_at=(720, 700, 60), sfx=[('underwater_rumble', 0.0, 0.5)])
shot('s15_plant', (10, None), 'two-shot', 'Whale tilts down and dives out of frame; a round thought bubble with a small squid silhouette; Tag MENU: SQUID',
     layers=lambda T, L: [fig('SpermWhale', '60%', '38%', 1100, 300, 60, keyframes=kf((0, {'y': 380, 'rotate': 0}), (L, {'y': 1300, 'rotate': 35, 'ease': 'in'})), z=6),
                          circle(1250, 250, 240, 'rgba(243,246,247,0.12)', stroke=WHITE, strokeWidth=4, start=0.4, z=20),
                          fig('ColossalSquid', 1250, 250, 200, 90, 18, props={'silhouette': WHITE, 'hooks': False}, start=0.4, z=21),
                          tag('MENU: SQUID', 1250, 420, 0.6, w=360),
                          tag('NEXT: ITS DINNER', '50%', 820, T(10, 'its dinner.'), accent=YEL, w=520)],
     camera='panDown', amount=0.4, you_at=(720, 700, 60), sfx=[('whoosh', 0.2, 0.5)])
shot('s16_midnight', (11, None), 'threshold card', 'DepthMeter ticks 1,000 with a flash; zone MIDNIGHT; Headline SUNLIGHT: 0%; rays gone; blue bioluminescent flashes (particles stars) on "alive"',
     layers=lambda T, L: [headline('SUNLIGHT: 0%', 0.1, size=84), tag('MIDNIGHT ZONE', 1150, 300, T(11, 'midnight'), accent='#1d4a66', w=480),
                          parts('stars', '50%', '50%', 1900, 1000, 70, color='#5fd3ff', size=[4, 10], speed=0.6, start=T(11, 'only light')),
                          tag('~3 IN 4 ANIMALS HERE MAKE LIGHT', '50%', 820, T(11, 'alive.'), accent='#5fd3ff', w=760, size=30)],
     camera='pushIn', amount=0.5, sfx=[('boom', 0.0, 0.3), ('sonar_ping', 'alive.', 0.3)],
     notes='Ocean prop rays fall to 0 by 1,000 m (depth falloff). The 3-in-4 figure is on screen only (Martini & Haddock 2017).')
shot('s17_boxer', (12, None), 'scale gag (motif 1/4)', 'Stat 100x; fingertip tile with a tiny YOU as the heavyweight boxer standing on it; Tag ~100 KG ON EVERY CM2',
     layers=lambda T, L: [stat(100, 0.2, suffix='x', label='SURFACE PRESSURE', x=1250, y=260, size=96, w=600),
                          svg(FINGERTIP, 760, 640, 400, 400, z=20), you(760, 600, 'stand', px=120, color='#e5483d', z=21, start=T(12, 'heavyweight')),
                          tag('BOXER ~100 KG', 760, 380, T(12, 'heavyweight'), w=380),
                          tag('~100 KG ON EVERY CM² OF YOU', 1250, 560, T(12, 'every fingertip'), w=620)],
     sled=False, sfx=[('impact', 'heavyweight', 0.5)])
shot('s18_v1', (12, 'Alive?'), 'verdict stamp', 'AliveMeter big: YES stamp; YOU shrugs alone in black; Tag 1 KM: YES',
     bg='black', layers=lambda T, L: [comp('explainer/AliveMeter', 1250, '55%', 420, 520, {'state': 'YES', 'stamp': [{'at': 0.3, 'text': 'YES', 'color': GRN}], 'size': 1.3}, depth=0, z=30),
                                      tag('1 KM: ALIVE', 1250, 200, 0.3, accent=GRN, w=360)],
     you_pose='shrug', camera='pushIn', amount=0.4, sfx=[('ding', 0.3, 0.6)])

# ---- P13-P16 rung 2 (1-2 km): giant squid, HPNS '?'
shot('s19_eye_opens', (13, None), 'withheld reveal', 'Below YOU a huge pale eye opens in the black (two circles, scaleY 0->1) on "something huge"',
     bg='black', layers=lambda T, L: [circle(1100, 780, 300, '#e9f6ff', keyframes=kf((T(13, 'something huge'), {'scaleY': 0.05}), (T(13, 'something huge') + 0.6, {'scaleY': 1, 'ease': 'out'})), z=5),
                                      circle(1100, 780, 140, '#0b1a22', keyframes=kf((T(13, 'something huge'), {'scaleY': 0.05}), (T(13, 'something huge') + 0.6, {'scaleY': 1, 'ease': 'out'})), z=6)],
     camera='panDown', amount=0.4, sfx=[('heartbeat_slow', 0.2, 0.6)])
shot('s20_squid', (13, 'a giant squid'), 'creature reveal', 'ColossalSquid drawing as giant squid (hooks off, variant giant) at shared pxPerM with YOU; kit Bus ghosted behind for length; Tag GIANT SQUID; ScaleBar UP TO ~12 M',
     layers=lambda T, L: [fig('Bus', '52%', '62%', 900, 260, 70, align='bottom', props={'silhouette': '#1d3a4a'}, start=T(13, 'length of a bus'), opacity=0.5, z=5),
                          fig('ColossalSquid', '52%', '46%', 1100, 420, 92, props={'hooks': False, 'variant': 'giant'}, z=8),
                          tag('GIANT SQUID', 1250, 160, 0.2, accent=WHITE, w=420),
                          comp('explainer/ScaleBar', '52%', 760, 1100, 70, {'label': 'UP TO ~12 M', 'at': T(13, 'length of a bus'), 'from': 'left'}, depth=0, z=30)],
     camera='pullOut', amount=0.5, sled=True, you_at=(300, 700, 70), sfx=[('whoosh_long', 0.0, 0.5)],
     notes='You at the same pxPerM (92) stays tiny at left. Giant squid live mostly 300-1,000 m: this is the deep edge of its range.')
shot('s21_eye_face', (13, 'with an eye'), 'scale comparison', 'Close: the 27 cm eye beside YOU\'s head at the same scale; Tag EYE ~27 CM vs YOUR FACE ~14 CM (teaser 1 paid, 21%)',
     bg='black', layers=lambda T, L: [circle(1150, 520, 405, '#e9f6ff', z=5), circle(1150, 520, 190, '#0b1a22', z=6),
                                      you(700, 1650, 'stand', px=1500, z=7),
                                      tag('ITS EYE ~27 CM', 1150, 200, 0.2, w=420), tag('YOUR FACE ~14 CM', 700, 200, 0.5, accent=WHITE, w=420)],
     sled=False, camera='pushIn', amount=0.3, sfx=[('pop', 0.2, 0.5)],
     notes='You drawn at pxPerM 1500-ish so only the head is in frame; the eye circle is 0.27 m at the same scale.')
shot('s22_suckers', (14, None), 'detail insert', 'Close on a squid arm: sucker discs with toothed rim rings (circle layers); Tag TOOTHED SUCKER RINGS',
     bg='black', layers=lambda T, L: [fig('ColossalSquid', '40%', '50%', 2400, 900, 260, props={'hooks': False, 'variant': 'giant'}, z=4)]
     + [circle(700 + i * 150, 560 + (i % 2) * 40, 70, 'rgba(0,0,0,0)', stroke=WHITE, strokeWidth=8, start=0.2 + i * 0.12, z=6) for i in range(6)]
     + [tag('TOOTHED SUCKER RINGS', 1250, 220, 0.4, w=520)],
     sled=False, camera='pushIn', amount=0.6, sfx=[('click', 0.3, 0.5)])
shot('s23_scars', (14, 'and dead sperm whales'), 'callback insert', 'SpermWhale head close-up printed with rows of ring scars (stroke circles) like bottle caps; Headline DINNER FIGHTS BACK',
     bg='dark', layers=lambda T, L: [fig('SpermWhale', '62%', '50%', 2600, 700, 160, z=4)]
     + [circle(900 + (i % 4) * 90, 420 + (i // 4) * 90, 60, 'rgba(0,0,0,0)', stroke='#f3d6cf', strokeWidth=7, start=0.3 + i * 0.06, z=6) for i in range(8)]
     + [tag('SUCKER-RING SCARS', 600, 220, 0.4, accent=WHITE, w=480), tag('≈ ROWS OF BOTTLE CAPS', 600, 320, T(14, 'like rows'), accent=WHITE, w=480, size=28), headline('DINNER FIGHTS BACK', T(14, 'Dinner'), color='red', y=830)],
     sled=False, camera='panLeft', amount=0.4, sfx=[('impact', 'Dinner', 0.4)])
shot('s24_shake', (15, None), 'symptom beats', 'YOU on sled with a jitter idle; wobble rotate keyframes on "rooms spin"; "Zz" text on "nod off"; Tag HIGH PRESSURE NERVOUS SYNDROME',
     layers=lambda T, L: [tag('HIGH PRESSURE NERVOUS SYNDROME', 1200, 220, 0.4, accent=YEL, w=760),
                          text('TREMBLE', 1200, 420, T(15, 'fingers tremble,'), size=44, color=YEL, z=20, end=T(15, 'rooms spin,')),
                          text('SPIN', 1200, 420, T(15, 'rooms spin,'), size=44, color=YEL, z=20, end=T(15, 'nod off')),
                          text('Zz', 940, 380, T(15, 'nod off'), size=80, color=YEL, z=20)],
     you_idle=False, camera='drift', amount=0.5, sfx=[('glitch', 'rooms spin', 0.3)],
     notes='You layer: jitter idle (amount 6, speed 9) + rotate keyframes -8/8 around "rooms spin". No face drawing needed.')
shot('s25_unknown', (15, 'And at twice'), 'admission card', 'DepthMeter flags 701 and 1,400 (2x RECORD); Headline NOBODY KNOWS red',
     layers=lambda T, L: [tag('2x THE HUMAN RECORD', 1200, 330, 0.2, w=520), headline('NOBODY KNOWS', T(15, 'Nobody knows.'), color='red', size=110)],
     you_idle=False, camera='pushIn', amount=0.5, sfx=[('drone', 0.0, 0.4)])
shot('s26_q', (16, None), 'meter beat', 'AliveMeter big: needle spins and lands on ? (yellow) on "It says this"',
     bg='dark', layers=lambda T, L: [comp('explainer/AliveMeter', '50%', '55%', 520, 620, {'state': [{'t': 0, 'v': 'MOSTLY'}, {'t': T(16, 'It says this'), 'v': '?'}],
                                                                                          'spin': [{'at': 0.5, 'duration': T(16, 'It says this') - 0.5}],
                                                                                          'stamp': [{'at': T(16, 'It says this'), 'text': '?', 'color': YEL}], 'size': 1.6}, depth=0, z=30)],
     sled=False, camera='pushIn', amount=0.4, sfx=[('glitch', 'It says this', 0.5)])
shot('s27_nocheat', (16, 'And a maybe'), 'rule beat', 'CHEATS LEFT 3 pulses; Tag A MAYBE DOESN\'T EARN A CHEAT; YOU keeps sinking, shaking, DepthMeter passes 2,000',
     layers=lambda T, L: [tag("A MAYBE DOESN'T EARN A CHEAT", 1150, 300, 0.2, accent=YEL, w=720), tag('2 KM: ?', 1150, 420, T(16, 'past two kilometres.'), accent=YEL, w=300)],
     you_idle=False, sfx=[('tick', 0.2, 0.4)])

# ---- P17-P22 rung 3 (2-3 km): cold, death 1, cheat 1, beaked whale
shot('s28_cold', (17, None), 're-hook card', 'Headline THE COLD; frost vignette creeps in from the edges; YOU tinted pale blue, pose panic',
     layers=lambda T, L: [headline('THE COLD', T(17, 'the cold.'), size=120, color='#dff4ff'),
                          svg(FROST, '50%', '50%', 1920, 1080, depth=0, z=25, keyframes=kf((0, {'opacity': 0}), (L, {'opacity': 1, 'ease': 'out'})))],
     you_pose='panic', you_color='#bfe3ff', camera='pushIn', amount=0.5, sfx=[('drone', 0.0, 0.4)])
shot('s29_temp', (17, 'The surface was'), 'temperature drop', 'Stat counts 28 -> 2 °C WATER TEMPERATURE across the sentence; Tags SURFACE: HEATED-POOL WARM / HERE: BARELY ABOVE FREEZING',
     layers=lambda T, L: [stat(2, 0.1, suffix=' °C', label='WATER TEMPERATURE', frm=28, dur=max(0.5, T(17, 'freezing.') - 0.1), x=1200, y=300, color='#7fe3ff', size=100, w=640),
                          tag('SURFACE: HEATED-POOL WARM (~28 °C)', 1200, 560, 0.2, accent=ORG, w=640, size=28),
                          tag('HERE: BARELY ABOVE FREEZING', 1200, 650, T(17, 'barely'), accent='#7fe3ff', w=640, size=28),
                          svg(FROST, '50%', '50%', 1920, 1080, depth=0, z=25, opacity=1)],
     you_pose='panic', you_color='#bfe3ff', sfx=[('tick', 0.1, 0.4)])
shot('s30_blackout', (18, None), 'you-scenario', 'Tag MOST PEOPLE BLACK OUT IN < 1 H; Stat 33 MIN YOU, IN WATER THIS COLD; frost thickens',
     layers=lambda T, L: [tag('0-4 °C WATER: MOST BLACK OUT WITHIN AN HOUR', 1150, 260, 0.2, accent='#7fe3ff', w=860, size=28),
                          stat(33, T(18, 'over half an hour'), suffix=' MIN', label='YOU, IN WATER THIS COLD', x=1150, y=520, color='#7fe3ff', size=96, w=600),
                          svg(FROST, '50%', '50%', 1920, 1080, depth=0, z=25, opacity=1)],
     you_pose='panic', you_color='#bfe3ff', sfx=[('heartbeat_slow', 0.5, 0.5)])
shot('s31_limp', (18, 'Near three kilometres'), 'you close-up', 'Shiver stops: YOU goes grey and tips over (rotate -75) and drifts; ALIVE needle slides to BARELY; host Tag I\'D HAVE QUIT HERE',
     layers=lambda T, L: [tag("HOST: I'D HAVE QUIT HERE", 1200, 260, T(18, "I'll be honest"), accent=WHITE, w=560, size=28),
                          svg(FROST, '50%', '50%', 1920, 1080, depth=0, z=25, opacity=1)],
     you_pose='stand', you_color='#8a97a1', you_kf=[{'t': 0, 'rotate': 0}, {'t': 2.0, 'rotate': -75, 'ease': 'inOut'}],
     camera='pushIn', amount=0.6, sfx=[('heartbeat_slow', 0.0, 0.6)])
shot('s32_death1', (19, None), 'verdict stamp (DEATH 1)', 'Music out. AliveMeter big slams NO, red stamp DEATH 1; Tag 3,000 M · 50 MIN IN; grade dark; DEATHS 0->1',
     bg='black', layers=lambda T, L: [comp('explainer/AliveMeter', '50%', '55%', 520, 620, {'state': [{'t': 0, 'v': 'BARELY'}, {'t': T(19, 'No.'), 'v': 'NO'}],
                                                                                          'stamp': [{'at': T(19, 'No.'), 'text': 'DEATH 1', 'color': RED}], 'size': 1.6}, depth=0, z=30),
                                      tag('3,000 M · 50 MIN IN', 1450, 560, T(19, 'fifty'), w=440),
                                      stat(1, T(19, 'No.'), frm=0, label='DEATHS', x=1500, y=300, size=80, w=300, dur=0.3)],
     sled=False, camera='pushIn', amount=0.3, sfx=[('stinger', 'No.', 0.8)], grade={'brightness': 0.8, 'vignette': 0.6})
shot('s33_cheat1', (20, None), 'revive', 'YOU re-coloured orange (heated suit, glow shadow), rotates upright; CHEATS LEFT 3->2; ALIVE YES; a long shadow slides behind on "not alone"',
     layers=lambda T, L: [tag('CHEAT 1: HEATED SUIT', 1150, 260, T(20, 'a heated suit'), accent=ORG, w=520),
                          fig('BeakedWhale', '50%', '45%', 1300, 300, 120, props={'silhouette': '#08141b'}, start=T(20, "you're not alone."),
                              keyframes=kf((T(20, "you're not alone."), {'x': 2400}), (L + 0.5, {'x': 1100, 'ease': 'linear'})), z=4)],
     you_kf=[{'t': 0, 'rotate': -75}, {'t': 0.8, 'rotate': 0, 'ease': 'backOut'}], camera='drift', sfx=[('riser', 0.0, 0.4), ('ding', 'a heated suit', 0.5)])
shot('s34_beaked', (21, None), 'creature pass', 'BeakedWhale (6 m, grey, scarred) glides past YOU at shared pxPerM; Tags CUVIER\'S BEAKED WHALE / DEEPEST-DIVING MAMMAL',
     layers=lambda T, L: [fig('BeakedWhale', '50%', '42%', 1300, 300, 120, keyframes=kf((0, {'x': 1700}), (L, {'x': 300, 'ease': 'linear'})), z=6),
                          tag("CUVIER'S BEAKED WHALE", 1200, 160, T(21, "Cuvier's"), accent=WHITE, w=520),
                          tag('DEEPEST-DIVING MAMMAL', 1200, 250, T(21, 'deepest-diving'), w=520)],
     camera='panLeft', amount=0.3, you_at=(720, 680, 120), sfx=[('underwater_rumble', 0.0, 0.5)])
shot('s35_beaked_record', (21, 'and one was followed'), 'record card', 'DepthMeter marker 2,992 m sits right at YOU; Stat 2,992 M TRACKED DIVE; Tag = YOUR DEPTH',
     layers=lambda T, L: [stat(2992, 0.2, suffix=' M', label='DEEPEST TRACKED DIVE', x=1150, y=300, size=96, w=680),
                          tag('= YOUR DEPTH, RIGHT NOW', 1150, 520, T(21, 'your depth.'), accent=WHITE, w=520)],
     sfx=[('tick', 0.2, 0.4)])
shot('s36_breath', (22, None), 'comparison bars', 'SpeedBars ONE BREATH vs YOUR TRIP [YOUR WHOLE FALL 182 MIN, ITS RECORD BREATH 222 MIN red]; whale gets its own CHEATS 0 tag (teaser 2 paid, 36%)',
     layers=lambda T, L: [fig('BeakedWhale', '50%', 200, 1300, 300, 120, props={'silhouette': '#0b2230'}, keyframes=kf((0, {'x': 900}), (L, {'x': 200, 'ease': 'linear'})), z=4),
                          tag('IT BREATHES AIR, LIKE YOU', 1120, 230, 0.2, accent=WHITE, w=560, out=T(22, 'longest breath')),
                          comp('explainer/SpeedBars', 1120, 460, 1100, 360, {'title': 'ONE BREATH vs YOUR TRIP', 'rows': [
                              {'label': 'YOUR WHOLE FALL', 'value': 182, 'unit': 'min', 'color': '#8a97a1'},
                              {'label': 'ITS LONGEST BREATH', 'value': 222, 'unit': 'min', 'color': RED}], 'max': 230, 'at': T(22, 'longest breath'), 'duration': 0.8, 'stagger': 0.5}, depth=0, z=30),
                          tag('ITS CHEATS: 0', 1120, 760, T(22, 'no cheats'), accent=RED, w=360)],
     you_pose='shrug', sfx=[('tick', 'longest breath', 0.4), ('pop', 'no cheats', 0.5)])

# ---- P23-P24 rung 4 (3-4 km): average depth, onto the trench wall
shot('s37_average', (23, None), 'cross-section', 'Wide cutaway: typical seafloor line at 3.7 km with the trench slot dropping away under YOU (dot); Tag AVERAGE OCEAN DEPTH ~3,700 M',
     bg='black', layers=lambda T, L: [svg(SECTION, '50%', '50%', 1600, 900, z=2), circle(800, 300, 24, ORG, z=10),
                                      tag('YOU', 860, 260, 0.3, accent=ORG, w=160, size=26),
                                      tag('AVERAGE OCEAN DEPTH ~3,700 M', 400, 420, T(23, 'average depth'), accent='#c9b48a', w=620, size=28)],
     sled=False, camera='pullOut', amount=0.6, sfx=[('whoosh_long', 0.0, 0.5)])
shot('s38_nudge', (24, None), 'cross-section beat', 'Same cutaway: the YOU dot drifts to the trench\'s west wall (keyframes), Tag CURRENT, then cuts in',
     bg='black', layers=lambda T, L: [svg(SECTION, '50%', '50%', 1600, 900, z=2),
                                      circle(800, 300, 24, ORG, keyframes=kf((0, {'x': 800, 'y': 330}), (T(24, 'against its wall'), {'x': 690, 'y': 420, 'ease': 'inOut'}),
                                                                             (L, {'x': 720, 'y': 560, 'ease': 'in'})), z=10),
                                      tag('CURRENT  →  THE WALL', 700, 220, 0.4, accent=WHITE, w=480, size=28)],
     sled=False, camera='pushIn', amount=0.4, sfx=[('whoosh', 0.3, 0.4)])
shot('s39_wall', (24, 'and you slide'), 'wall view (from here to the floor)', 'Trench WALL (rock slope) enters left, scrolling up as the sled scrapes down it; Headline 7 KM TO GO red',
     wall=True, layers=lambda T, L: [headline('7 KM TO GO', T(24, 'seven kilometres'), color='red', size=110)],
     camera='drift', amount=0.4, sfx=[('underwater_rumble', 0.0, 0.4)],
     notes='Geometry fix: from 3.7 km on, every seafloor encounter happens on this wall; the wall layer runs in every later descent shot.')

# ---- P25-P29 rung 5 (4-5 km): abyss, shells, scavengers, picture it again
shot('s40_abyss', (25, None), 'process insert', 'Zone ABYSS lights; seashells drift onto the wall ledge and fade to nothing; Tag SHELLS DISSOLVE BELOW ~4,500 M',
     wall=True, layers=lambda T, L: [tag('ABYSS', 1150, 180, 0.1, accent='#3a3f6b', w=320)]
     + [svg(SHELL, 760 + i * 110, 300, 90, 75, z=9, start=0.4 + i * 0.4, keyframes=kf((0.4 + i * 0.4, {'y': 250, 'opacity': 1}), (2.4 + i * 0.4, {'y': 620}),
                                                                                         (min(L, 4.4 + i * 0.4), {'y': 640, 'opacity': 0}))) for i in range(4)]
     + [tag('SEASHELLS DISSOLVE THIS DEEP', 1200, 820, T(25, 'seashells'), accent='#c9b48a', w=640, size=28)],
     sfx=[('bubbles', 0.4, 0.3)])
shot('s41_news', (26, None), 'punch card', 'Headline GOOD NEWS (green) then BAD NEWS: YOU\'RE FOOD (red); YOU point then panic (turnstile 1, 42%)',
     wall=True, layers=lambda T, L: [headline('GOOD NEWS', 0.05, out=T(26, 'Bad news:'), color='green', size=100),
                                     headline("BAD NEWS: YOU'RE FOOD", T(26, 'Bad news:'), color='red', size=100)],
     you_pose='point', sfx=[('pop', 0.05, 0.5), ('stinger', 'Bad news:', 0.35)])
shot('s42_baitcam', (27, None), 'bait-cam frame', 'Bait-cam frame on the slope: dead fish (DeepFish dead) on the mud; Tag +30 MIN; grenadiers (DeepFish x2) nose in on "grenadiers"',
     bg='dark', layers=lambda T, L: [svg(MUDFLOOR, '50%', 900, 1920, 300, z=2), svg(CAMFRAME, '50%', '50%', 1500, 840, depth=0, z=30),
                                     fig('DeepFish', 900, 770, 500, 160, 600, props={'dead': True, 'idle': False}, z=6),
                                     fig('DeepFish', 1300, 650, 600, 200, 600, start=T(27, 'grenadiers'), flipX=True,
                                         keyframes=kf((T(27, 'grenadiers'), {'x': 2100}), (T(27, 'grenadiers') + 1.6, {'x': 1250, 'ease': 'out'})), z=7),
                                     fig('DeepFish', 500, 620, 600, 200, 600, start=T(27, 'grenadiers') + 0.4,
                                         keyframes=kf((T(27, 'grenadiers') + 0.4, {'x': -300}), (T(27, 'grenadiers') + 2.0, {'x': 560, 'ease': 'out'})), z=7),
                                     tag('+30 MIN', 1500, 160, T(27, 'within half an hour'), accent=WHITE, w=260),
                                     tag('GRENADIERS', 1300, 520, T(27, 'grenadiers'), accent=WHITE, w=360, size=28)],
     sled=False, hud=False, camera='pushIn', amount=0.4, sfx=[('static', 0.0, 0.25), ('tick', 'within half an hour', 0.4)])
shot('s43_bones', (27, 'tiny scavengers'), 'time-lapse', 'Pale speck swarm (particles dust) covers the bait, then a skeleton replaces the fish; Tag 1 DAY: BONES (gross-out peak, 43-45%)',
     bg='dark', layers=lambda T, L: [svg(MUDFLOOR, '50%', 900, 1920, 300, z=2), svg(CAMFRAME, '50%', '50%', 1500, 840, depth=0, z=30),
                                     fig('DeepFish', 900, 770, 500, 160, 600, props={'dead': True, 'idle': False}, end=T(27, 'bones.'), z=6),
                                     parts('dust', 900, 760, 560, 200, 220, color='#e9e2d6', size=[3, 7], speed=2.2, end=T(27, 'bones.') + 0.3, z=8),
                                     svg(BONES, 900, 770, 500, 160, start=T(27, 'bones.'), z=6),
                                     tag('+1 DAY: BONES', 1500, 160, T(27, 'within a day'), accent=WHITE, w=320)],
     sled=False, hud=False, camera='drift', amount=0.3, sfx=[('static', 0.0, 0.3), ('pop', 'bones.', 0.6)])
shot('s44_circling', (28, None), 'threat on you', 'Back on the wall: three grenadiers circle YOU (looping keyframes); Options STRATEGY [KEEP MOVING]; Tag NAP = EVENT OF THE YEAR',
     wall=True, layers=lambda T, L: [fig('DeepFish', 700 + i * 300, 380 + (i % 2) * 260, 220, 90, PX, flipX=bool(i % 2),
                                         keyframes=kf((0, {'x': 1700 - i * 500}), (L, {'x': 500 + i * 450, 'ease': 'linear'})), z=7 + i) for i in range(3)]
     + [comp('explainer/Options', 1300, 760, 620, 200, {'title': 'STRATEGY', 'items': ['KEEP MOVING'], 'at': T(28, 'Strategy:'), 'size': 40}, depth=0, z=30),
        tag('NAP = EVENT OF THE YEAR', 1300, 220, T(28, 'event of the year'), accent=YEL, w=560)],
     you_pose='run', sfx=[('whoosh', 0.3, 0.3)])
shot('s45_watched', (28, 'Alive? Yes.'), 'gag + verdict', 'Pairs of eyes glint in the black around YOU; ALIVE YES stamp; Tag BEING WATCHED: YES',
     wall=True, layers=lambda T, L: [circle(400 + (i * 263) % 1200, 200 + (i * 151) % 650, 16, '#e9f6ff', start=0.2 + i * 0.15, z=5) for i in range(10)]
     + [tag('BEING WATCHED: YES', 1250, 260, T(28, 'Being watched?'), accent=YEL, w=480)],
     you_pose='shrug', camera='pullOut', amount=0.3, sfx=[('ding', 0.05, 0.5)])
shot('s46_picture', (29, None), 'column cutaway ("picture it again", 47%)', 'Full 0-11 km column: boat at the top, YOU dot at 4.5 km on the wall; Tag BOAT: 75 MIN STRAIGHT UP on "Look up"; Tag MORE WATER BELOW THAN ABOVE on "Look down"',
     bg='black', layers=lambda T, L: [svg(COLUMN, '50%', '50%', 900, 1000, z=2), svg(BOAT, 960, COL_TOP - 30, 220, 88, z=3),
                                      circle(960, COLY(4500), 26, ORG, z=10),
                                      rect(1000, COLY(2250), 8, COLY(4500) - COL_TOP, WHITE, start=T(29, 'Look up:'), z=9),
                                      tag('BOAT: 75 MIN STRAIGHT UP', 1450, 220, T(29, 'Look up:'), accent=WHITE, w=520, size=28),
                                      rect(1000, COLY(4500 + 6435 / 2), 8, COLY(6435) - COL_TOP, RED, start=T(29, 'Look down:'), z=9),
                                      tag('6.4 KM BELOW  >  4.5 KM ABOVE', 1450, 720, T(29, 'Look down:'), accent=RED, w=560, size=28)],
     sled=False, camera='pullOut', amount=0.6, sfx=[('whoosh_long', 0.0, 0.4)])

# ---- P30-P32 rung 6 (5-6 km)
shot('s47_piano', (30, None), 'scale gag (motif 2/4)', 'Fingertip tile, now a grand piano on it; Stat 500x; Tag ~500 KG ON EVERY CM2',
     layers=lambda T, L: [stat(500, 0.2, suffix='x', label='SURFACE PRESSURE', x=1250, y=260, size=96, w=600),
                          svg(FINGERTIP, 760, 640, 400, 400, z=20), svg(PIANO, 760, 540, 330, 205, z=21, start=T(30, 'grand piano.'), enter={'type': 'drop', 'duration': 0.35}),
                          tag('~500 KG ON EVERY CM² OF YOU', 1250, 560, T(30, 'grand piano.'), w=620)],
     sled=False, sfx=[('impact', 'grand piano.', 0.6)])
shot('s48_dumbo', (31, None), 'creature reveal', 'DumboOctopus flaps in beside YOU (ear-fin flap idle); Tag DUMBO OCTOPUS; ScaleBar ~30 CM next to YOU\'s forearm',
     wall=True, layers=lambda T, L: [fig('DumboOctopus', 860, 470, 120, 120, PX, keyframes=kf((0, {'y': 900, 'opacity': 0}), (1.2, {'y': 470, 'opacity': 1, 'ease': 'out'})), z=13),
                                     tag('DUMBO OCTOPUS', 1150, 200, 0.4, accent=WHITE, w=420), tag('FINS ≈ ELEPHANT EARS', 1150, 300, T(31, 'waving two fins'), accent=WHITE, w=440, size=28),
                                     comp('explainer/ScaleBar', 860, 560, 60, 50, {'label': '~30 CM ≈ YOUR FOREARM', 'at': T(31, 'about as long'), 'from': 'left'}, depth=0, z=30)],
     sfx=[('bubbles', 0.2, 0.4)])
shot('s49_dumbo_record', (31, 'and it lives deeper'), 'record card', 'DepthMeter marker 6,957 m far below YOU; Stat 6,957 M DEEPEST OCTOPUS (2020)',
     wall=True, layers=lambda T, L: [fig('DumboOctopus', 860, 470, 120, 120, PX, z=13),
                                     stat(6957, 0.2, suffix=' M', label='DEEPEST OCTOPUS EVER FILMED', x=1300, y=820, size=80, w=640)],
     sfx=[('tick', 0.2, 0.4)])
shot('s50_mostly', (32, None), 'verdict + turnstile 2', 'ALIVE MOSTLY stamp; camera pans up the wall to a hairline crack; Headline THE WALL red on "about to become the problem" (52%)',
     wall=True, layers=lambda T, L: [tag('5 KM: MOSTLY', 1250, 300, 0.1, accent='#a6d94a', w=360),
                                     svg('<svg viewBox="0 0 60 400" xmlns="http://www.w3.org/2000/svg"><path d="M30 0 L20 90 L40 160 L18 250 L36 330 L28 400" stroke="#e5483d" stroke-width="6" fill="none"/></svg>',
                                         420, 300, 60, 400, start=T(32, 'But that wall'), z=9),
                                     headline('THE WALL', T(32, 'the problem.'), color='red', size=110)],
     camera='panUp', amount=0.4, sfx=[('ding', 0.1, 0.4), ('underwater_rumble', 'But that wall', 0.5)])

# ---- P33-P37 rung 7 (6-7 km): hadal, plates, Japan 2011, death 2
shot('s51_hadal', (33, None), 'threshold card', 'Zone HADAL lights red; trench walls rise on both sides; Tags HADAL ZONE / A SLIVER OF THE SEAFLOOR / ~45% OF THE OCEAN\'S DEPTH RANGE',
     wall=True, layers=lambda T, L: [svg(WALL, 1700, 540, 700, 2400, flipX=True, keyframes=kf((0, {'y': 1100}), (L, {'y': 700, 'ease': 'linear'})), z=3),
                                     tag('HADAL ZONE', 1100, 180, 0.1, accent='#7a2a2a', w=360),
                                     tag('A SLIVER OF THE SEAFLOOR', 1100, 300, T(33, 'a sliver'), accent=WHITE, w=520, size=28),
                                     tag('~45% OF THE OCEAN\'S DEPTH RANGE', 1100, 390, T(33, 'almost half'), w=620, size=28)],
     camera='panDown', amount=0.4, sfx=[('boom', 0.0, 0.4)])
shot('s52_plates', (34, None), 'diagram', 'Two-plate cross-section (Pacific plate dives under the Philippine Sea plate, red arrow); camera shake on "shake"; Tag AVALANCHES',
     bg='black', layers=lambda T, L: [svg(PLATES, '50%', '50%', 1500, 600, z=2),
                                      tag('ONE PLATE DIVES UNDER ANOTHER', '50%', 160, 0.3, accent=WHITE, w=720),
                                      tag('→ QUAKES → AVALANCHES OF MUD', '50%', 820, T(34, 'avalanches'), w=720)],
     sled=False, camera='pushIn', amount=0.4, sfx=[('underwater_rumble', 'shake,', 0.6)],
     notes='camera shake at "shake," (generator adds it).')
shot('s53_japan', (35, None), 'map aside', 'Map: Japan Trench, ring at the 2011 Tohoku epicentre; pin YOU at the Mariana Trench; Tag 2011: MUD REACHED THE TRENCH FLOOR',
     bg='black', layers=lambda T, L: [comp('explainer/Map', '50%', '50%', 1920, 1080, {'views': [{'t': 0, 'lon': 142, 'lat': 26, 'zoom': 2.2}, {'t': 2.5, 'lon': 142.5, 'lat': 36, 'zoom': 3.0}],
                                                                                    'rings': [{'lon': 142.4, 'lat': 38.3, 'r': 1.2, 'at': 1.0, 'label': 'TOHOKU 2011'}],
                                                                                    'pins': [{'place': 'marianaTrench', 'label': 'YOU', 'at': 0.2, 'color': ORG}, {'lon': 143.8, 'lat': 38.0, 'label': 'JAPAN TRENCH', 'at': 1.4}]}, depth=0, z=2),
                                      tag('MUD SLID ALL THE WAY TO THE TRENCH FLOOR', '50%', 820, T(35, 'all the way'), w=900, size=30)],
     sled=False, hud=False, camera='none', sfx=[('boom', 1.0, 0.4)],
     notes='Map shows Japan at zoom <= 3 (coarse coastline is fine).')
shot('s54_punished', (35, 'And your strategy'), 'callback strike', 'Back on the wall: STRATEGY [KEEP MOVING] returns and gets struck red on "exactly where avalanches run"; Tag AVALANCHE PATH arrow down the wall',
     wall=True, layers=lambda T, L: [comp('explainer/Options', 1300, 600, 620, 200, {'title': 'STRATEGY', 'items': ['KEEP MOVING'], 'at': -1, 'itemAt': [-1], 'size': 40,
                                                                                  'strikes': [{'index': 0, 'at': T(35, 'exactly where')}]}, depth=0, z=30),
                                     tag('↓ AVALANCHE PATH ↓', 420, 300, T(35, 'avalanches run.'), w=420)],
     you_pose='run', sfx=[('pop', 'exactly where', 0.6)],
     notes='nAWpLtG-kNs 5:33 -> 5:49 device: the viewer\'s own strategy is exactly where the next threat lives.')
shot('s55_death2', (36, None), 'avalanche + verdict (DEATH 2)', 'Wall shudders (camera shake), mud cloud (gradient + brown particles) rolls down over YOU; AliveMeter NO, red stamp DEATH 2; DEATHS 1->2',
     wall=True, layers=lambda T, L: [svg(MUDCLOUD, '50%', 0, 1920, 1400, depth=0, z=24, keyframes=kf((0.6, {'y': -900}), (T(36, 'Alive?'), {'y': 540, 'ease': 'in'}))),
                                     parts('dust', '50%', '50%', 1920, 1080, 260, color='#6b5a4c', size=[6, 18], speed=2.5, start=0.8, z=25),
                                     comp('explainer/AliveMeter', '50%', '55%', 520, 620, {'state': [{'t': 0, 'v': 'MOSTLY'}, {'t': T(36, 'No.'), 'v': 'NO'}],
                                                                                          'stamp': [{'at': T(36, 'No.'), 'text': 'DEATH 2', 'color': RED}], 'size': 1.6}, depth=0, z=40, start=T(36, 'Alive?')),
                                     stat(2, T(36, 'No.'), frm=1, label='DEATHS', x=1500, y=300, size=80, w=300, dur=0.3)],
     camera='drift', amount=0.3, sfx=[('boom', 0.3, 0.7), ('underwater_rumble', 0.3, 0.7), ('stinger', 'No.', 0.8)])
shot('s56_cheat2', (37, None), 'revive', 'Mud thins (opacity out); YOU in the orange suit shakes off (jitter), CHEATS LEFT 2->1; ALIVE YES; host Tag TOLD YOU: THE WALL',
     wall=True, layers=lambda T, L: [svg(MUDCLOUD, '50%', 540, 1920, 1400, depth=0, z=24, keyframes=kf((0, {'opacity': 1}), (1.4, {'opacity': 0, 'ease': 'out'}))),
                                     tag('CHEAT 2: THE MUD LETS GO', 1200, 260, T(37, 'the mud lets'), accent=ORG, w=560),
                                     tag('1 CHEAT LEFT', 1200, 360, T(37, 'a single cheat'), accent=RED, w=320),
                                     tag('HOST: I DID WARN YOU', 1200, 820, T(37, 'I did warn'), accent=WHITE, w=460, size=28)],
     you_pose='wave', sfx=[('riser', 0.0, 0.4), ('ding', 'the mud lets', 0.5)])

# ---- P38-P39 rung 8 (7-8 km)
shot('s57_cow', (38, None), 'scale gag (motif 3/4)', 'Fingertip tile, now a dairy cow on it; Stat 700x; Tag ~700 KG ON EVERY CM2',
     layers=lambda T, L: [stat(700, T(38, 'seven hundred'), suffix='x', label='SURFACE PRESSURE', x=1250, y=260, size=96, w=600),
                          svg(FINGERTIP, 760, 640, 400, 400, z=20, start=T(38, 'every fingertip')), svg(COW, 760, 520, 360, 245, z=21, start=T(38, 'dairy cow'), enter={'type': 'drop', 'duration': 0.35}),
                          tag('~700 KG ON EVERY CM² OF YOU', 1250, 560, T(38, 'dairy cow'), w=620)],
     sled=False, sfx=[('impact', 'dairy cow', 0.7)])
shot('s58_protein', (39, None), 'microscope insert', 'Circular microscope frame (dipBlack in): a folded protein ribbon is squashed flat (scaleY 1->0.35) on "squashed"; Tag PROTEINS: OUT OF SHAPE',
     bg='black', layers=lambda T, L: [circle('50%', '50%', 760, '#0b2a3a', stroke=WHITE, strokeWidth=10, z=2),
                                      svg(PROTEIN, '50%', '50%', 600, 300, z=4, keyframes=kf((0, {'scaleY': 1}), (T(39, 'squashed'), {'scaleY': 1}), (T(39, 'squashed') + 0.6, {'scaleY': 0.35, 'ease': 'in'}))),
                                      tag("PROTEINS = YOUR CELLS' MACHINES", '50%', 150, T(39, 'Proteins,'), accent=YEL, w=640, out=T(39, 'squashed')),
                                      tag('PROTEINS: OUT OF SHAPE', '50%', 150, T(39, 'squashed'), w=560)],
     sled=False, trans='dipBlack', camera='pushIn', amount=0.4, sfx=[('glitch', 'squashed', 0.5)])
shot('s59_membrane', (39, 'your cell membranes'), 'mechanism + verdict', 'Membrane bilayer row compresses (scaleY); ALIVE BARELY orange stamp on "Barely"; YOU sags (rotate 15)',
     bg='black', layers=lambda T, L: [circle('50%', '50%', 760, '#0b2a3a', stroke=WHITE, strokeWidth=10, z=2),
                                      svg(MEMBRANE, '50%', '50%', 640, 100, z=4, keyframes=kf((0, {'scaleY': 1}), (0.8, {'scaleY': 0.6, 'ease': 'in'}))),
                                      tag('CELL MEMBRANES: STIFF', '50%', 150, 0.2, w=560),
                                      comp('explainer/AliveMeter', 1500, '55%', 360, 440, {'state': [{'t': 0, 'v': 'MOSTLY'}, {'t': T(39, 'Barely.'), 'v': 'BARELY'}],
                                                                                         'stamp': [{'at': T(39, 'Barely.'), 'text': 'BARELY', 'color': ORG}], 'size': 1.1}, depth=0, z=40, start=T(39, 'Alive?'))],
     sled=False, camera='drift', sfx=[('heartbeat_slow', 'Alive?', 0.6)])

# ---- P40-P44 rung 9a (8 km): snailfish, the ceiling, death 3, last cheat
shot('s60_snailfish', (40, None), 'creature reveal', 'A pale shape flickers at frame edge, then the Snailfish swims up to YOU\'s face; Tags SNAILFISH / LIKE WET TISSUE PAPER',
     wall=True, layers=lambda T, L: [fig('Snailfish', 820, 330, 110, 50, PX, keyframes=kf((0, {'x': 1700, 'opacity': 0.3}), (T(40, 'A snailfish,'), {'x': 1200, 'opacity': 0.6}), (T(40, 'swims right up'), {'x': 790, 'opacity': 1, 'ease': 'out'})), flipX=True, z=13),
                                     tag('SNAILFISH', 1200, 200, T(40, 'A snailfish,'), accent=WHITE, w=360),
                                     tag('LIKE WET TISSUE PAPER WITH EYES', 1200, 820, T(40, 'like wet tissue'), accent='#f2a7c2', w=680, size=28)],
     sfx=[('sonar_ping', 0.2, 0.3), ('bubbles', 'swims right up', 0.4)])
shot('s61_tmao', (41, None), 'x-ray cutaway', 'Snailfish x-ray (prop xray): small TMAO spheres prop up a protein ribbon; Tag TMAO HOLDS PROTEINS IN SHAPE',
     bg='black', layers=lambda T, L: [fig('Snailfish', '50%', '45%', 1000, 420, 3200, props={'xray': True}, z=4),
                                      svg(PROTEIN, '50%', 760, 420, 210, z=6)] +
     [circle(780 + i * 90, 700 + (i % 2) * 50, 34, '#7fe3ff', start=0.5 + i * 0.15, z=7) for i in range(5)] +
     [tag('TMAO: HOLDS PROTEINS IN SHAPE', '50%', 150, T(41, 'TMAO'), accent='#7fe3ff', w=720)],
     sled=False, camera='pushIn', amount=0.4, sfx=[('pop', 'TMAO', 0.5)])
shot('s62_ceiling', (41, 'But the deeper'), 'graph', 'SpeedBars TMAO A FISH NEEDS by depth (2 / 4 / 6 / 8 KM, last row red text LIMIT ~8.2 KM); Tag BEYOND THIS: WATER FLOODS IN',
     bg='black', layers=lambda T, L: [comp('explainer/SpeedBars', '50%', '50%', 1200, 560, {'title': 'TMAO A FISH NEEDS', 'rows': [
                                          {'label': '2 KM', 'value': 25, 'color': '#7fe3ff'}, {'label': '4 KM', 'value': 45, 'color': '#7fe3ff'},
                                          {'label': '6 KM', 'value': 65, 'color': '#7fe3ff'}, {'label': '8 KM', 'value': 85, 'color': '#7fe3ff'},
                                          {'label': '~8.2 KM', 'value': 100, 'color': RED, 'text': 'LIMIT'}], 'max': 100, 'at': 0.2, 'duration': 0.6, 'stagger': 0.45}, depth=0, z=30),
                                      tag('DEEPER = MORE TMAO', '50%', 840, T(41, 'the more it needs,'), accent='#7fe3ff', w=520, size=30, out=T(41, 'a little past')),
                          tag('A LITTLE PAST 8 KM...', '50%', 840, T(41, 'a little past'), accent=WHITE, w=520, size=30, out=T(41, 'flood')),
                          tag('PAST THIS: WATER WOULD FLOOD ITS BODY', '50%', 840, T(41, 'flood'), w=860, size=30)],
     sled=False, camera='drift', sfx=[('tick', 0.2, 0.3), ('tick', 0.65, 0.3), ('tick', 1.1, 0.3), ('tick', 1.55, 0.3), ('stinger', 'flood', 0.3)],
     notes='Bars only grow (SpeedBars), so the ceiling is the last row in red, not a moving line. Values are illustrative ordering, not measured TMAO.')
shot('s63_lastfish', (42, None), 'record card (teaser 3 paid, 70%)', 'DepthMeter marker FISH LIMIT; small juvenile Snailfish at a red flag; Stat 8,336 M DEEPEST FISH EVER FILMED (2022); Headline THE LAST FISH',
     wall=True, layers=lambda T, L: [fig('Snailfish', 1000, 500, 80, 40, PX, props={'juvenile': True}, z=13),
                                     stat(8336, 0.2, suffix=' M', label='DEEPEST FISH EVER FILMED (2022)', x=1250, y=260, size=90, w=720),
                                     tag('A YOUNG SNAILFISH', 1000, 420, 0.6, accent=WHITE, w=380, size=28)],
     sfx=[('ding', 0.2, 0.4)])
shot('s63b_nofish', (42, 'No fish has ever'), 'isolation', 'Red FISH LIMIT line under YOU; Tag NO FISH SEEN DEEPER; Headline THE LAST FISH ON THE PLANET on "You just met"',
     wall=True, layers=lambda T, L: [fig('Snailfish', 1000, 500, 80, 40, PX, props={'juvenile': True}, z=13),
                                     rect('50%', 760, 1920, 8, RED, z=9), text('FISH LIMIT ~8,200 M', 1250, 730, 0, size=34, color=RED, z=9),
                                     tag('NO FISH EVER SEEN DEEPER', 1250, 260, 0.2, accent=RED, w=520),
                                     tag('CHEMISTRY SAYS: NONE CAN GO MUCH FURTHER', 1250, 350, T(42, 'the chemistry'), accent=WHITE, w=760, size=28),
                                     headline('THE LAST FISH ON THE PLANET', T(42, 'You just met'), size=76, y=830)],
     sfx=[('drone', 'You just met', 0.3)])
shot('s64_death3', (43, None), 'isolation + verdict (DEATH 3)', 'The snailfish turns back up and fades; red dashed FISH CEILING line scrolls up past YOU; AliveMeter NO, stamp DEATH 3; DEATHS 2->3',
     wall=True, layers=lambda T, L: [fig('Snailfish', 1000, 500, 80, 40, PX, props={'juvenile': True}, keyframes=kf((0, {'y': 520, 'opacity': 1, 'scaleX': -1}), (2.0, {'y': -50, 'opacity': 0, 'scaleX': -1})), z=8),
                                     rect('50%', 0, 1920, 8, RED, keyframes=kf((0, {'y': 900}), (T(43, 'through its ceiling') + 0.5, {'y': 380, 'ease': 'linear'}), (L, {'y': 200})), z=9),
                                     text('FISH CEILING', 1200, 0, 0, size=34, color=RED, keyframes=kf((0, {'y': 870}), (T(43, 'through its ceiling') + 0.5, {'y': 350, 'ease': 'linear'}), (L, {'y': 170})), z=9),
                                     comp('explainer/AliveMeter', '50%', '55%', 520, 620, {'state': [{'t': 0, 'v': 'BARELY'}, {'t': T(43, 'No.'), 'v': 'NO'}],
                                                                                          'stamp': [{'at': T(43, 'No.'), 'text': 'DEATH 3', 'color': RED}], 'size': 1.6}, depth=0, z=40, start=T(43, 'Alive?')),
                                     stat(3, T(43, 'No.'), frm=2, label='DEATHS', x=1500, y=300, size=80, w=300, dur=0.3)],
     you_kf=[{'t': 0, 'rotate': 15}, {'t': A(43, 'Alive?') - A(43), 'rotate': -70}], you_color='#8a97a1',
     sfx=[('stinger', 'No.', 0.8)], notes='"The facts become the weapon": the fish limit you just learned is what kills you (PLAYBOOK §4).')
shot('s65_cheat3', (44, None), 'revive (last cheat)', 'Tiny amber Amphipods crawl on the wall beside YOU; CHEATS LEFT 1->0 (red); ALIVE YES; Headline 0 CHEATS LEFT; Tag NEXT DEATH = TRIP OVER',
     wall=True, layers=lambda T, L: [circle(470, 600, 300, 'rgba(11,42,58,0.85)', stroke=WHITE, strokeWidth=6, z=7), text('x40', 470, 780, 0, size=30, z=8)]
     + [fig('Amphipod', 410 + i * 60, 580 + (i % 2) * 50, 110, 64, 2400, props={'color': '#d9a35a'}, z=8) for i in range(3)]
     + [tag('CHEAT 3 (LAST): THE CRUSTACEANS\' TRICK', 1200, 260, T(44, 'you borrow'), accent=ORG, w=760, size=28),
        headline('0 CHEATS LEFT', T(44, "You're out of cheats"), color='red', size=96, y=820),
        tag('NEXT DEATH = TRIP OVER', 1200, 360, T(44, 'the trip is over.'), accent=RED, w=480)],
     you_kf=[{'t': 0, 'rotate': -70}, {'t': 0.8, 'rotate': 0, 'ease': 'backOut'}], sfx=[('riser', 0.0, 0.4), ('ding', 'you borrow', 0.5), ('stinger', "You're out of cheats", 0.3)])

# ---- P45-P48 rung 9b (8.8-9 km): Everest, no rescue, Hirondellea plant
shot('s66_everest', (45, None), 'signature scale image (75%)', 'Wide column: Everest hung upside down from the surface line, its summit exactly at YOU (8,849 m); 2 km of water still below; Tags ONE EVEREST DOWN / +2 KM TO GO',
     bg='black', layers=lambda T, L: [svg(COLUMN, '50%', '50%', 900, 1000, z=2),
                                      svg(EVEREST, 960, (COL_TOP + COLY(8849)) / 2, COLY(8849) - COL_TOP, COLY(8849) - COL_TOP, rotate=180, z=4, start=0.2, enter={'type': 'slideDown', 'duration': 0.8, 'distance': 300}),
                                      circle(960, COLY(8849), 26, ORG, z=10),
                                      tag('8,849 M: ONE EVEREST DOWN', 1500, COLY(8849) - 60, T(45, 'Mount Everest'), accent=WHITE, w=520, size=28),
                                      tag('+2 KM TO GO', 1450, 900, T(45, 'two kilometres'), w=320)],
     sled=False, camera='pullOut', amount=0.6, sfx=[('whoosh_long', 0.1, 0.5), ('boom', 'Mount Everest', 0.4)],
     notes='Geometry fix: you have sunk one Everest-height; the summit (inverted, hanging from the surface) touches YOU. Not "standing on the floor".')
shot('s67_rescue', (46, None), 'record card', 'Same column: small yellow sub icon at 480 m near the top, sperm-whale icon at ~800 m, YOU far below; Tag DEEPEST RESCUE EVER: 480 M (1973); Headline NOBODY IS COMING',
     bg='black', layers=lambda T, L: [svg(COLUMN, '50%', '50%', 900, 1000, z=2),
                                      svg(SUB, 960, COLY(480), 120, 64, z=6, start=T(46, 'the deepest rescue')),
                                      tag('DEEPEST RESCUE EVER: 480 M (1973)', 1450, COLY(480), T(46, 'the deepest rescue'), accent=YEL, w=640, size=26),
                                      fig('SpermWhale', 960, COLY(800) + 30, 180, 50, 10, z=6, start=T(46, 'sperm whale.')),
                                      circle(960, COLY(8900), 26, ORG, z=10),
                                      headline('NOBODY IS COMING', T(46, 'Nobody is coming.'), size=90, y=830)],
     sled=False, camera='pushIn', amount=0.3, sfx=[('tick', 'the deepest rescue', 0.4), ('drone', 'Nobody is coming.', 0.4)])
shot('s68_hirondellea', (47, None), 'creature + scale', 'Amber Amphipod (Hirondellea, ~3 cm) chewing a sunken branch on the wall; thumb tile beside it; ScaleBar ~3 CM ≈ TOP JOINT OF YOUR THUMB',
     bg='dark', layers=lambda T, L: [svg(BRANCH, '50%', 640, 1300, 370, z=3), fig('Amphipod', 900, 560, 420, 240, 12000, props={'color': '#d9a35a'}, z=6),
                                     svg(THUMB, 1500, 760, 260, 500, z=5, start=T(47, 'top joint')),
                                     comp('explainer/ScaleBar', 900, 760, 360, 60, {'label': '~3 CM', 'at': T(47, 'about as long'), 'from': 'left'}, depth=0, z=30),
                                     tag('HIRONDELLEA GIGAS', 900, 200, 0.3, accent=WHITE, w=440)],
     sled=False, camera='pushIn', amount=0.4, sfx=[('click', 0.4, 0.4), ('click', 1.0, 0.4)])
shot('s69_plant', (47, 'Its gut turns'), 'x-ray plant', 'X-ray gut overlay: wood bits, and one faint grey speck among them (unlabelled plant); Tag DEAD WOOD -> SUGAR; speck pulses once on "Remember that"',
     bg='dark', layers=lambda T, L: [fig('Amphipod', '50%', 560, 840, 480, 24000, props={'color': '#d9a35a', 'xray': True}, z=4),
                                     svg(XRAY_GUT, '50%', 560, 600, 300, z=6),
                                     circle(910, 590, 24, 'rgba(0,0,0,0)', stroke='#c7d0d6', strokeWidth=4, start=T(47, 'Remember that.'),
                                            keyframes=kf((T(47, 'Remember that.'), {'scale': 0.6, 'opacity': 1}), (T(47, 'Remember that.') + 0.8, {'scale': 2.0, 'opacity': 0})), z=7),
                                     tag('DEAD WOOD → SUGAR', '50%', 160, 0.3, accent='#d9a35a', w=480, out=T(47, 'whatever sinks')),
                                     tag('WHATEVER SINKS ENDS UP IN HERE', '50%', 160, T(47, 'whatever sinks'), accent=WHITE, w=700)],
     sled=False, camera='pushIn', amount=0.5, sfx=[('sonar_ping', 'Remember that.', 0.3)])
shot('s70_lonely', (48, None), 'verdict stamp', 'AliveMeter YES; CHEATS LEFT 0 in red; YOU tiny in a wide black frame on the wall; Tag LONELY: EXTREMELY',
     wall=True, layers=lambda T, L: [tag('9 KM: ALIVE · 0 CHEATS', 1250, 260, 0.1, accent=GRN, w=520), tag('LONELY: EXTREMELY', 1250, 360, T(48, 'Lonely?'), accent=WHITE, w=420)],
     camera='pullOut', amount=0.6, sfx=[('ding', 0.1, 0.4)])

# ---- P49-P52 rung 10-11: xenophyophores, landing, final squeeze, final board
shot('s71_xeno', (49, None), 'creature', 'Fist-sized xenophyophore lumps on the wall ledge beside YOU (pose point); Tags ONE CELL EACH / YOU: ~30 TRILLION CELLS',
     wall=True, layers=lambda T, L: [svg(XENO, 560, 610, 240, 66, z=6, start=T(49, 'Lumps')),
                                     tag('XENOPHYOPHORE: ONE CELL EACH', 1250, 260, T(49, 'single giant cell'), accent='#c9b48a', w=640, size=28),
                                     tag('YOU: ~30 TRILLION CELLS', 1250, 360, T(49, 'trillions.'), accent=WHITE, w=520, size=28)],
     you_pose='point', sfx=[('bubbles', 0.3, 0.3)])
shot('s72_landing', (50, None), 'landing', 'Sled thumps into the mud (squash keyframe), silt puff; DepthMeter locks 10,935 with a red frame; Tag CHALLENGER DEEP; Tag 3 H 02 MIN on "three hours"',
     layers=lambda T, L: [svg(MUDFLOOR, '50%', 960, 1920, 300, z=3),
                          parts('dust', 760, 820, 700, 200, 120, color='#8a7550', size=[6, 16], speed=1.2, start=T(50, 'thumps'), z=14),
                          tag('CHALLENGER DEEP', 1250, 220, T(50, 'Challenger Deep,'), accent=RED, w=440),
                          tag('ELAPSED: 3 H 02 MIN', 1250, 320, T(50, 'three hours'), accent=WHITE, w=440, size=28)],
     you_kf=[{'t': 0, 'feet': 380}, {'t': A(50, 'thumps') - A(50), 'feet': 800, 'ease': 'in'}, {'t': A(50, 'thumps') - A(50) + 0.12, 'scaleY': 0.9}, {'t': A(50, 'thumps') - A(50) + 0.3, 'scaleY': 1.0}],
     you_at=(720, 800, PX),
     camera='pushIn', amount=0.4, sfx=[('impact', 'thumps', 0.9), ('boom', 'thumps', 0.5)])
shot('s73_car', (51, None), 'scale gag (motif 4/4)', 'Fingertip tile, now the kit Car on it; Tag ~1.1 T ON EVERY CM2',
     layers=lambda T, L: [svg(FINGERTIP, 760, 640, 400, 400, z=20), fig('Car', 760, 560, 380, 150, 80, align='bottom', start=T(51, 'small car'), enter={'type': 'drop', 'duration': 0.35}, z=21),
                          tag('~1.1 TONNES ON EVERY CM² OF YOU', 1250, 400, T(51, 'more than a tonne'), w=680)],
     sled=False, sfx=[('impact', 'small car', 0.8)])
shot('s74_last_test', (51, 'and you have no cheats'), 'final near-death', 'AliveMeter big, 0 cheats: needle slides toward NO, stops at BARELY, then YES stamp on "Alive? Yes."; heartbeat',
     bg='black', layers=lambda T, L: [comp('explainer/AliveMeter', '50%', '55%', 520, 620, {'state': [{'t': 0, 'v': 'YES'}, {'t': T(51, 'The needle slides'), 'v': 'BARELY'}, {'t': T(51, 'Yes.'), 'v': 'YES'}],
                                                                                          'stamp': [{'at': T(51, 'Yes.'), 'text': 'YES', 'color': GRN}], 'size': 1.6}, depth=0, z=30),
                                      tag('CHEATS LEFT: 0', '50%', 150, 0.1, accent=RED, w=360)],
     sled=False, camera='pushIn', amount=0.5, sfx=[('heartbeat_slow', 0.1, 0.7), ('ding', 'Yes.', 0.6)],
     notes='The arrival is a real test with zero cheats (retention nice-to-have: last near-death beat before the twist).')
BOARD_ROWS = ['0-1 KM   YES', '1-2 KM   ?', '2-3 KM   DEATH 1', '3-4 KM   YES', '4-5 KM   YES', '5-6 KM   MOSTLY',
              '6-7 KM   DEATH 2', '7-8 KM   BARELY', '8-9 KM   DEATH 3', '9-10 KM  YES', '10 KM-BOTTOM  YES (0 CHEATS)']


def board(at_items, strikes_at=None, x=760, size=30):
    p = {'title': 'FINAL READING', 'items': BOARD_ROWS, 'at': -1, 'itemAt': at_items, 'size': size}
    return comp('explainer/Options', x, 540, 760, 900, p, depth=0, z=30)


shot('s75_board', (52, None), 'finished board (peak declared, 86%)', 'Board FINAL READING, 11 km bands written out (0-1 YES / 1-2 ? / 2-3 DEATH 1 / 3-4 YES / 4-5 YES / 5-6 MOSTLY / 6-7 DEATH 2 / 7-8 BARELY / 8-9 DEATH 3 / 9-10 YES / 10-bottom YES, 0 cheats); Stat DEATHS 3, CHEATS LEFT 0; Headline YOU BEAT THE OCEAN (green)',
     bg='dark', layers=lambda T, L: [board([0.1 + i * 0.12 for i in range(11)]),
                                     stat(3, T(52, 'Deaths:'), label='DEATHS', x=1450, y=330, size=110, w=420, frm=3),
                                     stat(0, T(52, 'Cheats left:'), label='CHEATS LEFT', x=1450, y=620, size=110, w=420, frm=0),
                                     headline('YOU BEAT THE OCEAN', T(52, 'You beat'), color='green', size=80, y=990)],
     sled=False, hud=False, camera='pullOut', amount=0.3, sfx=[('ding', 'Deaths:', 0.5), ('riser', 'You beat', 0.4)])

# ---- P53-P57 twist
shot('s76_turn', (53, None), 'turn', 'dipBlack; slow push toward a grey shape half-buried in the mud beside YOU; Headline NOT THE FIRST (red)',
     layers=lambda T, L: [svg(MUDFLOOR, '50%', 960, 1920, 300, z=3), svg(BLOB, 1250, 860, 220, 220, z=4, opacity=0.7),
                          headline('NOT THE FIRST', T(53, 'first thing'), color='red', size=100)],
     trans='dipBlack', hud=False, camera='pushIn', amount=0.9, you_at=(720, 820, PX), sfx=[('stinger', 0.1, 0.6)],
     notes='Music out (mix). The shape is the same unreadable outline as teaser 4.')
shot('s77_bag', (54, None), 'reveal (teaser 4 paid, 89%)', 'ROV light pool on the mud: a white single-use plastic bag; Stat 10,898 M FILMED 1998; Tag SINGLE-USE PLASTIC BAG; on "No cheats" Tag RULE 3: BROKEN',
     bg='black', layers=lambda T, L: [svg(MUDFLOOR, '50%', 960, 1920, 300, z=2), svg(ROV_LIGHT, '50%', 600, 1200, 900, z=3),
                                      svg(BAG, 960, 700, 300, 340, z=5, start=T(54, 'a plastic shopping bag,'), enter={'type': 'fade', 'duration': 0.8}),
                                      stat(10898, T(54, 'floor of this trench'), suffix=' M', label='FILMED BY A ROBOT SUB, 1998', x=1450, y=240, size=80, w=640),
                                      tag('SINGLE-USE PLASTIC BAG', 960, 860, T(54, 'single-use'), accent=WHITE, w=520),
                                      tag('RULE 3: BROKEN · NO CHEATS · NO HELP', 500, 240, T(54, 'No cheats,'), accent=RED, w=640, size=28)],
     sled=False, hud=False, camera='pushIn', amount=0.4, sfx=[('drone', 0.0, 0.4)])
shot('s78_fibres', (55, None), 'callback x-ray', 'The 9 km x-ray gut again: the grey speck turns red and multiplies into fibres (stagger); Tag MAN-MADE FIBRES: IN EVERY ONE CHECKED',
     bg='dark', layers=lambda T, L: [fig('Amphipod', '50%', 560, 840, 480, 24000, props={'color': '#d9a35a', 'xray': True}, z=4),
                                     svg(XRAY_GUT, '50%', 560, 600, 300, z=6),
                                     svg(FIBRES, '50%', 560, 600, 300, z=7, start=T(55, 'man-made'), enter={'type': 'fade', 'duration': 0.6}),
                                     tag('SAMPLES FROM THE DEEPEST PART OF THIS TRENCH', '50%', 160, T(55, 'Researchers checked'), accent=WHITE, w=900, size=28, out=T(55, 'every one they')),
                                     tag('MAN-MADE FIBRES: IN EVERY ONE CHECKED', '50%', 160, T(55, 'every one they'), w=860, size=30)],
     sled=False, hud=False, camera='pushIn', amount=0.5, sfx=[('sonar_ping', 0.2, 0.3)])
shot('s79_pcb', (56, None), 'comparison bars', 'SpeedBars PCB LEVELS [PADDY-FIELD CRABS, POLLUTED RIVER 1x grey; TRENCH AMPHIPODS ~50x red]; Tag BANNED DECADES AGO',
     bg='black', layers=lambda T, L: [comp('explainer/SpeedBars', '50%', '48%', 1200, 380, {'title': 'PCB LEVELS', 'rows': [
                                          {'label': "CRABS, CHINA'S LIAO RIVER PADDIES", 'value': 1, 'unit': 'x', 'color': '#8a97a1'},
                                          {'label': 'AMPHIPODS, THIS TRENCH', 'value': 50, 'unit': 'x', 'color': RED}], 'max': 50, 'at': T(56, 'fifty'), 'duration': 0.9, 'stagger': 0.5}, depth=0, z=30),
                                      headline('PCBs', 0.1, size=90, y=150, out=T(56, 'fifty')),
                                      tag('PCBs: BANNED DECADES AGO', '50%', 820, T(56, 'banned'), accent=WHITE, w=560, out=T(56, 'paddy fields')),
                                      tag("CRABS FROM PADDY FIELDS FED BY CHINA'S LIAO RIVER", '50%', 820, T(56, 'paddy fields'), accent='#8a97a1', w=980, size=28)],
     sled=False, hud=False, sfx=[('tick', 'fifty', 0.4)])
shot('s80_swap', (57, None), 'callback strike-list + tilt up', 'Options [THE SQUID, THE COLD, THE MUD, THE CRUSHING WEIGHT] struck in turn on each word; Headline THE NEWEST ARRIVAL IS OURS (red); camera tilts up the column',
     bg='black', layers=lambda T, L: [comp('explainer/Options', '50%', 520, 900, 520, {'title': 'EVERYTHING YOU MET', 'items': ['THE SQUID', 'THE COLD', 'THE MUD', 'THE CRUSHING WEIGHT'], 'at': 0.1,
                                                                                    'strikes': [{'index': 0, 'at': T(57, 'squid,')}, {'index': 1, 'at': T(57, 'cold,')}, {'index': 2, 'at': T(57, 'mud')},
                                                                                                {'index': 3, 'at': T(57, 'crushing weight,')}], 'size': 44}, depth=0, z=30),
                                      headline('THE NEWEST ARRIVAL IS OURS', T(57, 'the newest arrival'), color='red', size=76, y=830)],
     sled=False, hud=False, camera='panUp', amount=0.4, sfx=[('whoosh', 'squid,', 0.3), ('whoosh', 'cold,', 0.3), ('whoosh', 'mud', 0.3), ('whoosh', 'crushing weight,', 0.3)])

# ---- P58 bookend + finished board hold
shot('s81_bookend', (58, None), 'bookend (mirror of s01)', 'Same framing as frame 1: bright surface, boat, empty crane, no sled',
     bg={'type': 'component', 'name': 'explainer/Ocean', 'depth': 0.12, 'overscan': 1.2, 'props': {'depth': 0, 'surface': 0.55, 'rays': 7, 'snow': 30}},
     layers=lambda T, L: [svg(BOAT, 1110, 440, 900, 360, z=6), tag('YOUR SLED: 3 HOURS', 330, 120, T(58, 'Your sled'), accent=WHITE, w=480)],
     sled=False, hud=False, camera='drift', amount=0.3, trans='fade', sfx=[('underwater_rumble', 0.0, 0.3)])
shot('s82_drift', (58, 'Whatever slips'), 'drift-down', 'A single plastic bag slips under the surface and starts down the darkening column; Tags YOU: 3 H / IT: ? on "nobody knows how long"',
     bg={'type': 'component', 'name': 'explainer/Ocean', 'depth': 0.12, 'overscan': 1.2, 'props': {'depth': [{'t': 0, 'v': 0}, {'t': 8, 'v': 400}], 'surface': [{'t': 0, 'v': 0.55}, {'t': 2.5, 'v': -0.2}], 'rays': 7, 'snow': 50}},
     layers=lambda T, L: [svg(BAG, 1000, 300, 200, 226, z=6, keyframes=kf((0, {'y': 300, 'rotate': -10}), (L, {'y': 760, 'rotate': 25, 'ease': 'linear'})), idle=[{'type': 'sway', 'amount': 8, 'speed': 0.4}]),
                          tag('YOU: 3 H', 1450, 300, T(58, 'nobody knows'), accent=ORG, w=280), tag('IT: ?', 1450, 400, T(58, 'how long'), accent=RED, w=200)],
     sled=False, hud=False, camera='panDown', amount=0.5, sfx=[('bubbles', 0.3, 0.4)])
shot('s83_hold', SPEECH_END + 0.3, 'finished board hold (6 s, no spoken CTA)', 'Finished board held; Tag WHERE WOULD YOU HAVE QUIT?; cut to black at the end',
     bg='dark', layers=lambda T, L: [board([-1] * 11), stat(3, -1, label='DEATHS', x=1450, y=330, size=110, w=420, frm=3),
                                     tag('WHERE WOULD YOU HAVE QUIT?', 1450, 640, 0.3, accent=YEL, w=600, size=34)],
     sled=False, hud=False, camera='none', sfx=[('ding', 0.3, 0.4)],
     notes='PLAYBOOK §6: the three biggest outliers end on a held board with no spoken CTA.')

HUD_OFF = {'s21_eye_face', 's22_suckers', 's23_scars', 's37_average', 's38_nudge', 's46_picture', 's52_plates', 's58_protein', 's59_membrane',
           's61_tmao', 's62_ceiling', 's66_everest', 's67_rescue', 's68_hirondellea', 's69_plant'}
for _s in SHOTS:
    if _s['id'] in HUD_OFF:
        _s['hud'] = False
SHOTS.sort(key=lambda s: s['t0'])

# ------------------------------------------------------------------ HUD and per-scene assembly


def depth_track(t0, t1):
    pts = [t0] + [tt for tt, _ in DEPTH if t0 < tt < t1] + [t1]
    return [{'t': round(p - t0, 3), 'v': round(depth(p))} for p in pts]


def alive_track(t0, t1):
    cur = 'YES'
    for tt, s in ALIVE:
        if tt <= t0:
            cur = s
    tr = [{'t': 0, 'v': cur}] + [{'t': round(tt - t0, 3), 'v': s} for tt, s in ALIVE if t0 < tt < t1]
    return tr


def hud_layers(t0, t1, L):
    out = [comp('explainer/DepthMeter', 1730, 560, 190, 880, {'depth': depth_track(t0, t1), 'max': 11000, 'window': 1400, 'step': 200,
                                                             'zones': ZONES, 'markers': MARKERS, 'side': 'right', 'size': 40}, depth=0, z=50,
                **({'enter': {'type': 'slideLeft', 'duration': 0.5}} if t0 < 6.5 else {}))]
    if t0 >= A(5) - 0.05:
        out.append(comp('explainer/AliveMeter', 190, 600, 220, 420, {'state': alive_track(t0, t1), 'size': 0.8, 'label': 'ALIVE?'}, depth=0, z=50,
                        **({'enter': {'type': 'slideRight', 'duration': 0.5}} if abs(t0 - A(5)) < 0.1 else {})))
    if t1 > A(5, 'three,'):
        c0 = cheats_at(t0)
        ev = [(te, v) for te, v in CHEAT_EVENTS if t0 < te < t1]
        first_at = max(-1.0, A(5, 'three,') - t0) if t0 < A(5, 'three,') else -1
        if not ev:
            out.append(stat(c0, first_at, label='CHEATS LEFT', x=190, y=170, size=56, w=260, color=RED if c0 == 0 else WHITE, frm=c0, dur=0.2))
        else:
            te, v = ev[0]
            out.append(stat(c0, -1, label='CHEATS LEFT', x=190, y=170, size=56, w=260, frm=c0, dur=0.2, out=te - t0))
            out.append(stat(v, te - t0, label='CHEATS LEFT', x=190, y=170, size=56, w=260, color=RED if v == 0 else ORG, frm=c0, dur=0.4))
    return out


def you_small(x, feet, px=PX, pose='stand', color=None, kfs=None, idle=True, sled=True, z=12):
    """YOU standing on the sled at true scale px (pxPerM). feet = screen y of YOU's feet (= top of the sled).
    kfs: [{t, x?, feet?, rotate?, scaleY?, ease?}] applied to the pair (rotate/scaleY on YOU only)."""
    h = int(1.75 * px) + 30
    w = int(0.9 * px) + 60
    sw, sh = 1.5 * px, 0.45 * px
    you_kw, sled_kw = {'z': z}, {'z': z - 1}
    if kfs:
        yk, sk = [], []
        for f in kfs:
            a = {'t': f['t']}
            if 'ease' in f:
                a['ease'] = f['ease']
            b = dict(a)
            if 'x' in f:
                a['x'] = f['x']
                b['x'] = f['x']
            if 'feet' in f:
                a['y'] = round(f['feet'] - h / 2, 1)
                b['y'] = round(f['feet'] + sh / 2, 1)
            for k in ('rotate', 'scaleY'):
                if k in f:
                    a[k] = f[k]
            yk.append(a)
            if len(b) > 1 + ('ease' in b):
                sk.append(b)
        you_kw['keyframes'] = yk
        if sk:
            sled_kw['keyframes'] = sk
    idle_you = [{'type': 'float', 'amount': 6, 'speed': 0.3}] if idle else [{'type': 'jitter', 'amount': 5, 'speed': 9}]
    p = {'pose': pose, 'pxPerM': px, 'align': 'bottom'}
    if color:
        p['color'] = color
    if color == SUIT:
        you_kw['shadow'] = '0 0 18px rgba(255,138,42,.8)'
    out = []
    if sled:
        out.append(svg(SLED, x, feet + sh / 2, sw, sh, idle=[{'type': 'float', 'amount': 6, 'speed': 0.3}] if idle else [], **sled_kw))
    out.append(comp('explainer/You', x, feet - h / 2, w, h, p, idle=idle_you, **you_kw))
    return out


def you_sled(s, t0, L):
    col = s['you_color']
    if col is None and suit_on(t0):
        col = SUIT
    x, feet, px = s['you_at']
    return you_small(x, feet, px, s['you_pose'], col, s['you_kf'], s['you_idle'])


def wall_layer(L):
    return svg(WALL, 230, 540, 700, 2400, keyframes=kf((0, {'y': 900}), (L, {'y': 900 - 40 * L, 'ease': 'linear'})), z=3)


def sfx_list(s, T, L):
    out = []
    for cue, at, vol in s['sfx']:
        if isinstance(at, (int, float)):
            tt = at
        elif isinstance(at, tuple):
            tt = T(*at)
        else:
            tt = T(s['_pi'], at)
        if 0 <= tt < L + 0.01:
            out.append({'cue': cue, 'at': round(max(0.0, tt), 3), 'volume': vol})
    return out


def build():
    scenes = []
    for k, s in enumerate(SHOTS):
        t0 = s['t0']
        t1 = SHOTS[k + 1]['t0'] if k + 1 < len(SHOTS) else TOTAL
        L = round(t1 - t0, 3)
        s['t1'] = t1
        # paragraph that owns this shot (for word anchors without an explicit paragraph)
        pi = max([p for p in PSTART if PSTART[p] <= t0 + 1e-6] or [1])
        s['_pi'] = pi

        def T(p, needle=None, end=False, _t0=t0):
            if needle is None and isinstance(p, str):
                p, needle = s['_pi'], p
            return round(A(p, needle, end) - _t0, 3)

        def Tsfx(p, needle):
            return T(p, needle)
        s['_T'] = T
        layers = []
        if s['bg'] == 'ocean':
            bg = ocean_bg(depth(t0), depth(t1), L)
        elif s['bg'] == 'black':
            bg = BLACK
        elif s['bg'] == 'dark':
            bg = DARK
        else:
            bg = s['bg']
        if s['wall']:
            layers.append(wall_layer(L))
        if s['sled']:
            layers += you_sled(s, t0, L)
        if s['layers']:
            layers += s['layers'](T, L)
        if s['hud']:
            has_meter = any(l.get('name') == 'explainer/AliveMeter' for l in layers)
            layers += [l for l in hud_layers(t0, t1, L) if not (has_meter and l.get('name') == 'explainer/AliveMeter')]
        cam = {'preset': s['camera'], 'amount': s['amount']}
        if s['id'] == 's52_plates':
            cam['shake'] = [{'at': T(34, 'shake,'), 'duration': 0.6, 'amplitude': 14}]
        if s['id'] == 's55_death2':
            cam['shake'] = [{'at': 0.3, 'duration': 1.4, 'amplitude': 22}]
        if s['id'] == 's72_landing':
            cam['shake'] = [{'at': T(50, 'thumps'), 'duration': 0.35, 'amplitude': 16}]
        trans = {'type': s['trans'], 'duration': 0.5 if s['trans'] != 'cut' else 0.4}
        sc = {'id': s['id'], 'duration': L, 'background': bg, 'layers': layers, 'camera': cam, 'transitionIn': trans,
              'sfx': sfx_list(s, T, L), 'notes': f"[{fmt(t0)}-{fmt(t1)}] {s['kind']}: {s['desc']}" + (f" NOTE: {s['notes']}" if s['notes'] else '')}
        if s['grade']:
            sc['grade'] = s['grade']
        scenes.append(sc)
    words = [{'text': w, 'start': round(st, 3), 'end': round(en, 3)} for _p, _i, w, st, en in WORDS]
    # music bed: drops out for the three death stamps and the twist turn (script front matter)
    gaps = [(A(19) - 0.2, A(20)), (A(36, 'Alive?') - 0.2, A(37)), (A(43, 'Alive?') - 0.2, A(44)), (A(53) - 0.6, A(54) + 1.0)]
    music, c = [], 0.0
    for g0, g1 in gaps:
        music.append({'src': 'music/deep_ocean.m4a', 'start': round(c, 2), 'end': round(g0, 2), 'volume': 0.3, 'duckTo': 0.1, 'fadeIn': 0.6 if c else 1.0, 'fadeOut': 0.4})
        c = g1
    music.append({'src': 'music/deep_ocean.m4a', 'start': round(c, 2), 'end': TOTAL, 'volume': 0.24, 'duckTo': 0.08, 'fadeIn': 1.5, 'fadeOut': 1.5})
    sb = {
        'version': 1, 'id': EP, 'title': 'How Many Times Would The Ocean Kill You On The Way To The Bottom?', 'format': '16:9', 'fps': 30,
        'theme': {'fontDisplay': 'Montserrat', 'fontBody': 'Montserrat', 'fontCondensed': 'Anton', 'accent': '#ffe14d', 'ink': INK, 'paper': WHITE},
        'scenes': scenes,
        'captions': {'enabled': True, 'words': words, 'maxWords': 4, 'maxChars': 26, 'gapBreak': 0.3,
                     'glue': ['giant squid', 'sperm whale', 'beaked whale', 'dumbo octopus', 'Mount Everest', 'Challenger Deep', 'twilight zone', 'midnight zone', 'hadal zone'],
                     'style': {'fontSize': 56, 'y': 0.9, 'highlightMode': 'content', 'highlight': '#ffe14d', 'strokeWidth': 10, 'backing': 0.0}},
        'audio': {'voice': [], 'music': music, 'sfx': [], 'sfxDir': 'sfx', 'duckOn': 'captions'},
        'overlays': {'grain': 0.03, 'vignette': 0.18, 'fadeIn': 0.0, 'fadeOut': 0.6},
    }
    return sb


# ------------------------------------------------------------------ script.md generated sections
PARA = {  # beat label, on-screen summary (generator keeps it next to the shots)
    1: ('HOOK (drop on "drops")', 'Timer ring 5 -> 0 hits zero on "drops"; Tag MARIANA TRENCH, PACIFIC'),
    2: ('HOOK / teasers x4', 'Headline 11 KM DOWN; teaser cards: AN EYE WIDER THAN YOUR FACE / ONE BREATH > YOUR WHOLE TRIP / THE LAST FISH ON THE PLANET / ? (red)'),
    3: ('MASTER QUESTION (= title)', 'Headline HOW MANY TIMES DOES THE OCEAN KILL YOU?; DEATHS 0'),
    4: ('RUNG 1 (0-1 km) entry + rule 1', 'Tag 10 M: PRESSURE x2; Options THE RULES item 1'),
    5: ('Rule 2 + FORMAT REVEAL (ALIVE meter, CHEATS LEFT 3)', 'Options item 2; AliveMeter enters; CHEATS LEFT 3; big meter YES'),
    6: ('Rule 3 (planted for the twist) + sink rate', 'Options item 3 + struck sub; Bus: FEWER THAN A BUSLOAD; Stat 1 M/S, ~3 HOURS'),
    7: ('RUNG 1 colour loss, TWILIGHT named', 'Options COLOURS LEFT struck one by one; Tag TWILIGHT ZONE'),
    8: ('RUNG 1 record (701 m)', 'Chamber; Stat 701 M; HUMAN LIMIT line; silent 330 M = 1 EIFFEL TOWER'),
    9: ('RUNG 1 creature: sperm whale', 'Sonar rings; SpermWhale; Tag LOUDEST ANIMAL ON EARTH; silent 828 M = 1 BURJ KHALIFA'),
    10: ('RUNG 1 plant ("its dinner")', 'Tag MENU: SQUID / NEXT: ITS DINNER'),
    11: ('RUNG 1 threshold 1 km, MIDNIGHT named', 'Headline SUNLIGHT: 0%; bioluminescent flashes; Tag ~3 IN 4 ANIMALS HERE MAKE LIGHT'),
    12: ('RUNG 1 number + verdict YES', 'Stat 100x; boxer on the fingertip tile; AliveMeter YES'),
    13: ('RUNG 2 (1-2 km) creature: giant squid (teaser 1 paid)', 'Eye opens; giant squid vs Bus; ScaleBar UP TO ~12 M; EYE ~27 CM vs YOUR FACE ~14 CM'),
    14: ('RUNG 2 weapon + callback (dinner fights back)', 'Tag TOOTHED SUCKER RINGS; whale scars; Headline DINNER FIGHTS BACK'),
    15: ('RUNG 2 threat: nerves + honest unknown', 'Tag HIGH PRESSURE NERVOUS SYNDROME; Headline NOBODY KNOWS'),
    16: ('RUNG 2 verdict "?" (no cheat for a maybe)', "AliveMeter spins to ?; Tag A MAYBE DOESN'T EARN A CHEAT"),
    17: ('RUNG 3 (2-3 km) threat: the cold', 'Headline THE COLD; Stat 28 -> 2 °C; frost'),
    18: ('RUNG 3 you-scenario + host ruling', 'Stat 33 MIN; YOU tips over; Tag HOST: I\'D HAVE QUIT HERE'),
    19: ('DEATH 1 (32%)', 'AliveMeter NO, stamp DEATH 1; DEATHS 1; music out'),
    20: ('Cheat 1', 'Orange heated suit; CHEATS LEFT 2'),
    21: ('RUNG 3 creature: beaked whale (at your depth)', "Tags CUVIER'S BEAKED WHALE / DEEPEST-DIVING MAMMAL; Stat 2,992 M = YOUR DEPTH"),
    22: ('RUNG 3 comparison (teaser 2 paid)', 'SpeedBars YOUR WHOLE FALL 182 MIN vs ITS LONGEST BREATH 222 MIN; ITS CHEATS: 0'),
    23: ('RUNG 4 (3-4 km) expectation reversal', 'Cross-section: AVERAGE OCEAN DEPTH ~3,700 M'),
    24: ('RUNG 4 geometry: onto the trench wall', 'Dot drifts to the wall; wall view from here on; Headline 7 KM TO GO'),
    25: ('RUNG 5 (4-5 km) ABYSS named, shells dissolve', 'Tag ABYSS; shells fade; Tag SEASHELLS DISSOLVE THIS DEEP'),
    26: ('Turnstile 1 (good news / bad news)', "Headline GOOD NEWS -> BAD NEWS: YOU'RE FOOD"),
    27: ('RUNG 5 gross-out: bait cam', 'BAIT CAM frame; +30 MIN; grenadiers; swarm; +1 DAY: BONES'),
    28: ('RUNG 5 threat on you + strategy + verdict', 'Grenadiers circle YOU; STRATEGY: KEEP MOVING; BEING WATCHED: YES'),
    29: ('"Picture it again" re-immersion (47%)', 'Column: BOAT 75 MIN STRAIGHT UP; 6.4 KM BELOW > 4.5 KM ABOVE'),
    30: ('RUNG 6 (5-6 km) number', 'Stat 500x; piano on the fingertip tile'),
    31: ('RUNG 6 creature: dumbo octopus', 'ScaleBar ~30 CM ≈ YOUR FOREARM; Stat 6,957 M DEEPEST OCTOPUS'),
    32: ('Verdict MOSTLY + turnstile 2 (52%)', 'Crack in the wall; Headline THE WALL'),
    33: ('RUNG 7 (6-7 km) HADAL named', 'Tags HADAL ZONE / A SLIVER OF THE SEAFLOOR / ~45% OF THE DEPTH RANGE'),
    34: ('RUNG 7 mechanism', 'Plate diagram; Tag QUAKES -> AVALANCHES OF MUD'),
    35: ('RUNG 7 dated aside + strategy punished', 'Map: TOHOKU 2011 / JAPAN TRENCH; STRATEGY KEEP MOVING struck'),
    36: ('DEATH 2 (58%, sawtooth crash)', 'Mud cloud; AliveMeter NO, stamp DEATH 2; DEATHS 2'),
    37: ('Cheat 2 + host ruling', 'CHEATS LEFT 1; Tag HOST: I DID WARN YOU'),
    38: ('RUNG 8 (7-8 km) number', 'Stat 700x; cow on the fingertip tile'),
    39: ('RUNG 8 threat: molecules, verdict BARELY', 'Protein squashed; membranes stiff; AliveMeter BARELY'),
    40: ('RUNG 9 (8-9 km) creature: snailfish ("and yet" reversal)', 'Tags SNAILFISH / LIKE WET TISSUE PAPER WITH EYES'),
    41: ('RUNG 9 mechanism + its ceiling', 'TMAO x-ray; SpeedBars TMAO A FISH NEEDS (last row LIMIT ~8.2 KM)'),
    42: ('Teaser 3 paid: the last fish', 'Stat 8,336 M DEEPEST FISH EVER FILMED; Headline THE LAST FISH ON THE PLANET'),
    43: ('DEATH 3 (72%): the fish ceiling becomes the weapon', 'FISH CEILING line passes; AliveMeter NO, stamp DEATH 3; DEATHS 3'),
    44: ('Cheat 3 (last) + stakes reset', 'CHEATS LEFT 0; Headline 0 CHEATS LEFT; NEXT DEATH = TRIP OVER'),
    45: ('Biggest landmark: one Everest down (75%)', 'Inverted Everest hung from the surface, summit at YOU; +2 KM TO GO'),
    46: ('No rescue (callback to the whale)', 'Sub icon at 480 M; whale at ~800 M; Headline NOBODY IS COMING'),
    47: ('RUNG 10 (9-10 km) creature + plant', 'HIRONDELLEA GIGAS ~3 CM vs thumb; x-ray gut with an unlabelled grey speck'),
    48: ('Verdict YES, 0 cheats', 'Tags 9 KM: ALIVE · 0 CHEATS / LONELY: EXTREMELY'),
    49: ('RUNG 11 (10-10.9 km) creature', 'Tags XENOPHYOPHORE: ONE CELL EACH / YOU: ~30 TRILLION CELLS'),
    50: ('Arrival: Challenger Deep, three hours', 'Sled lands; DepthMeter locks 10,935; CHALLENGER DEEP; ELAPSED 3 H 02 MIN'),
    51: ('Final number + final near-death with 0 cheats', 'Car on the fingertip tile; ~1.1 TONNES ON EVERY CM²; needle slides, stops, YES'),
    52: ('Finished board + peak declared (86%)', 'Board FINAL READING (11 rows); DEATHS 3; YOU BEAT THE OCEAN'),
    53: ('TWIST (88%): rule 3 turned around', 'dipBlack; half-buried grey shape; Headline NOT THE FIRST'),
    54: ('Teaser 4 paid: the bag (89%)', 'Stat 10,898 M FILMED 1998; SINGLE-USE PLASTIC BAG; RULE 3: BROKEN'),
    55: ('Callback to the plant: fibres', 'x-ray speck turns red, multiplies; MAN-MADE FIBRES: IN EVERY ONE CHECKED'),
    56: ('Escalation: PCBs', 'SpeedBars PCB LEVELS 1x vs ~50x; PCBs: BANNED DECADES AGO'),
    57: ('Villain swap', 'EVERYTHING YOU MET struck in turn; Headline THE NEWEST ARRIVAL IS OURS'),
    58: ('BOOKEND (mirror of frame 1) + left-open ending', 'Surface, boat, empty crane; bag drifts down; YOU: 3 H / IT: ?; board held 6 s with WHERE WOULD YOU HAVE QUIT?'),
}


def md_scenes():
    out = []
    for pi, para in enumerate(P, 1):
        beat, ons = PARA.get(pi, ('', ''))
        out.append(f"### {pi:02d}. [{fmt(PSTART[pi])}-{fmt(PEND[pi])}] {beat}\n\nVO: {para}\n\nOn screen: {ons}\n")
    return '\n'.join(out)


def md_shots():
    rows = ['| # | t_start | t_end | shot | visual (kit vocabulary) | camera | SFX |', '|---|---|---|---|---|---|---|']
    for k, s in enumerate(SHOTS, 1):
        sfx = ', '.join(sorted({c for c, _a, _v in s['sfx']})) or '-'
        cam = s['camera'] + (' + shake' if s['id'] in ('s52_plates', 's55_death2', 's72_landing') else '')
        extra = []
        if s['wall']:
            extra.append('WALL')
        if s['sled']:
            extra.append('YOU+sled')
        if s['hud']:
            extra.append('HUD')
        rows.append(f"| {k} `{s['id']}` | {fmt(s['t0'])} | {fmt(s['t1'])} | {s['kind']} | {s['desc']}" + (f" [{' · '.join(extra)}]" if extra else '') + f" | {cam} | {sfx} |")
    return '\n'.join(rows)


def md_pacing(sb):
    words = sum(len(p.split()) for p in P)
    holds = [sc['duration'] for sc in sb['scenes']]
    long = [(sc['id'], sc['duration']) for sc in sb['scenes'] if sc['duration'] > 9.0]
    return (f"- Source: {'Kokoro am_michael speed 1.0 word timings for ' + str(MEASURED) + '/' + str(len(P)) + ' paragraphs (durations.json)' if MEASURED else 'wpm estimate'}; "
            f"gaps {GAP} s; lead-in {LEAD} s; board hold {TAIL_HOLD} s.\n"
            f"- Runtime {fmt(TOTAL)} ({TOTAL:.1f} s); speech ends {fmt(SPEECH_END)}; {words} words = {words / (SPEECH_END / 60):.0f} wpm over the speech span.\n"
            f"- {len(sb['scenes'])} scenes; median scene {sorted(holds)[len(holds) // 2]:.1f} s; scenes over 9 s: "
            + (', '.join(f"{i} {d:.1f} s" for i, d in long) or 'none') + ' (each has 3+ timed internal beats).\n')


def write_md(sb):
    src = open(os.path.join(HERE, 'script.md'), encoding='utf-8').read()
    for key, body in (('scenes', md_scenes()), ('shots', md_shots()), ('pacing', md_pacing(sb))):
        pat = re.compile(rf"(<!-- gen:{key} -->\n)(?:.*?\n)?(<!-- /gen:{key} -->)", re.S)
        if not pat.search(src):
            raise SystemExit(f'marker gen:{key} missing in script.md')
        src = pat.sub(lambda m: m.group(1) + body.rstrip('\n') + '\n' + m.group(2), src)
    open(os.path.join(HERE, 'script.md'), 'w', encoding='utf-8').write(src)


if __name__ == '__main__':
    sb = build()
    json.dump(sb, open(os.path.join(HERE, 'storyboard.json'), 'w'), indent=1, ensure_ascii=False)
    print(f"storyboard.json: {len(sb['scenes'])} scenes, {TOTAL:.2f} s, measured paragraphs {MEASURED}/{len(P)}, captions {len(sb['captions']['words'])} words")
    if '--md' in sys.argv:
        write_md(sb)
        print('script.md generated sections updated')
