#!/usr/bin/env python3
"""Generate storyboard.json for explainer-short-moray-second-jaw (keep PARAS in sync with script.md).

usage: python3 gen_storyboard.py <out storyboard.json> [--timeline]

Before TTS, word timings are a per-word estimate for Kokoro am_michael at speed 0.96 (config.py default), calibrated on
the shipped am_michael Shorts (pressure-ladder 250 words = 88.9 s at 0.96; blue-whale-scale 193 words at
1.05 = 190 wpm over the speech span, measured). After TTS, replace `estimate_words()` with the word list
from episodes/explainer-short-moray-second-jaw/audio/captions.json and rerun: every layer is anchored to a
word with A(scene, word), so the board retimes itself.

Assets: the kit has no moray, coral wall, hand or jaw cutaway, so they are inline static SVG layers. Every
motion below is a transform/opacity keyframe or an idle (no internal SVG animation, no masks):
  - occlusion by stacking: hole-dark < moray head < coral wall with an evenodd hole < hand
  - the cutaway is 5 stacked layers: cavity < fish < throat jaw < head shell (evenodd window) < oral jaws
  - tick / cross are SVG primitives (Montserrat/Anton have no U+2713/U+2717)
Kit gap (recommended, not blocking): an `explainer/Moray` species with `jaw` and swimWarp undulation would
replace MORAY_BODY / MORAY_HEAD_* and let shot s03 slide out with a real body wave.
"""
import copy
import json
import re
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else 'storyboard.json'
SHOW_TIMELINE = '--timeline' in sys.argv
SLUG = 'explainer-short-moray-second-jaw'

# ------------------------------------------------------------------ narration (= script.md narration block, cues stripped)
SPEED = 0.96
PARAS = [
    ('hook', 'Your fingers just brushed a hole with two mouths.'),
    ('misdirect', "You checked for sharks, jellyfish and one suspicious crab, never the crack you're touching."),
    ('reveal', "It's a moray eel's home, and the biggest reach three metres, longer than you're tall."),
    ('rung1', 'Mouth one is right by your hand, its teeth curved backwards like fish hooks.'),
    ('rung2', 'It can barely see you, so a hand in its home gets bitten first, questions later.'),
    ('rq', "And the worst thing you can do next is the first thing you'll do."),
    ('pull', 'Pull. Those hooks point inward, so yanking back drags your hand across every one.'),
    ('handshake', "It's the one handshake on the reef you don't get to end."),
    ('turnstile', "Relax, it's not trying to eat you."),
    ('fish', "If you were a fish, you'd meet mouth two."),
    ('suction', "Its throat can't suck you in, so a second jaw does it."),
    ('launch', 'The front teeth catch you, then that jaw launches out of its throat like a monster-movie mouth.'),
    ('ratchet', "It grabs you, and the jaws swap grips, hand over hand, until you're gone."),
    ('twist', 'But plenty of bites come from the friendly ones, the morays people feed by hand.'),
    ('taught', "If you've ever fed one by hand, you taught it that fingers smell like fish."),
    ('cantsee', "And it can barely see, so it can't tell which part is the fish."),
    ('stinger', 'This time, it really is trying to eat your fingers.'),
]
PARA_GAP = 0.27          # config.py: paragraph_pause 0.15 + tail trimmed to <= 0.12 s
EXTRA_GAP = {'turnstile': 0.2, 'twist': 0.2}   # script [pause: 0.2] before "Relax." and before the twist
LEAD_IN = 0.12
TAIL = 0.4               # hard cut 0.4 s after the last word (loop seam)
CAL = 0.885              # see docstring


def estimate_words():
    words, t = [], LEAD_IN
    para_first = []
    k = 0.96 / SPEED
    for i, (key, text) in enumerate(PARAS):
        if i:
            t += PARA_GAP + EXTRA_GAP.get(key, 0.0)
        para_first.append(len(words))
        for tok in text.split():
            letters = len(re.sub(r"[^A-Za-z0-9]", '', tok))
            d = (0.13 + 0.043 * letters) * k * CAL
            words.append({'text': tok, 'start': round(t, 3), 'end': round(t + d, 3), 'para': i})
            t += d
            if tok[-1] == ',':
                t += 0.12 * k * CAL
            elif tok[-1] in '.?!:;':
                t += 0.28 * k * CAL
    return words, para_first


def measured_words():
    """Real Kokoro word timings from the Spark pilot (audio/captions.json), split into paragraphs by word count."""
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    cap, rep = os.path.join(here, 'audio', 'captions.json'), os.path.join(here, 'audio', 'report.json')
    if not os.path.exists(cap):
        return None
    raw = json.load(open(cap))['words']
    counts = [len(t.split()) for _, t in PARAS]
    if sum(counts) != len(raw):
        print(f'captions.json has {len(raw)} words, PARAS {sum(counts)}: falling back to the estimate', file=sys.stderr)
        return None
    words, para_first, i = [], [], 0
    for p, n in enumerate(counts):
        para_first.append(i)
        for w in raw[i:i + n]:
            words.append({'text': w['text'], 'start': w['start'], 'end': w['end'], 'para': p})
        i += n
    mix_s = json.load(open(rep))['mix']['duration_s'] if os.path.exists(rep) else None
    return words, para_first, mix_s


_m = None if '--estimate' in sys.argv else measured_words()
if _m:
    WORDS, PARA_FIRST, MIX_S = _m
    TIMING = 'measured (audio/captions.json, Kokoro am_michael 0.96, Spark CPU)'
else:
    WORDS, PARA_FIRST = estimate_words()
    MIX_S = None
    TIMING = 'estimate'


def clean(w):
    return re.sub(r"[^a-z0-9'-]", '', w.lower())


def word_t(para, needle, nth=1, end=False):
    seen = 0
    for w in WORDS:
        if w['para'] == para and clean(w['text']).startswith(needle.lower()):
            seen += 1
            if seen == nth:
                return w['end'] if end else w['start']
    raise KeyError(f'{needle!r} not in paragraph {para}')


SCENES = []
for i, (key, _) in enumerate(PARAS):
    SCENES.append({'key': key, 'paras': [i]})
for j, s in enumerate(SCENES):
    s['start'] = 0.0 if j == 0 else WORDS[PARA_FIRST[s['paras'][0]]]['start'] - 0.1
for j, s in enumerate(SCENES):
    s['end'] = SCENES[j + 1]['start'] if j + 1 < len(SCENES) else (MIX_S or WORDS[-1]['end'] + TAIL)
    s['dur'] = round(s['end'] - s['start'], 3)
SC = {s['key']: s for s in SCENES}
TOTAL = SCENES[-1]['end']


def A(key, needle, nth=1, end=False):
    s = SC[key]
    return round(word_t(s['paras'][0], needle, nth, end) - s['start'], 3)


def G(key, needle, nth=1, end=False):
    """Global time of a word."""
    return round(word_t(SC[key]['paras'][0], needle, nth, end), 3)


# ------------------------------------------------------------------ palette
RED, GREEN, YELLOW, WHITE = '#e5483d', '#3ccf7a', '#ffe14d', '#ffffff'
MORAY, MORAY_DARK, SPECK = '#6f7d2e', '#4a5520', '#d9c64a'
CORAL_A, CORAL_B = '#c9727a', '#c89a52'
SKIN, SLEEVE = '#e9b48f', '#1f5fae'
X = 'xmlns="http://www.w3.org/2000/svg"'

# ------------------------------------------------------------------ svg assets (static markup)
# 1. coral wall, 1080x1300, one oval hole cut with evenodd at (540, 650) rx 150 ry 95
_lumps = ''.join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}" opacity="0.9"/>'
                 for cx, cy, r, c in ((110, 470, 70, CORAL_B), (330, 450, 55, CORAL_A), (820, 455, 75, CORAL_A),
                                      (1010, 480, 60, CORAL_B), (600, 452, 40, CORAL_B), (180, 980, 140, CORAL_B),
                                      (520, 1150, 130, CORAL_A), (900, 1010, 150, CORAL_B), (980, 760, 80, CORAL_A),
                                      (300, 560, 50, '#d98c6a'), (760, 540, 45, '#d98c6a'), (330, 850, 70, '#b9665f')))
_polyps = ''.join(f'<circle cx="{cx}" cy="{cy}" r="7" fill="#f2d3c4" opacity="0.7"/>'
                  for cx, cy in ((140, 520), (230, 600), (650, 500), (880, 600), (420, 930), (700, 900), (950, 540),
                                 (110, 760), (560, 420), (800, 1180), (300, 1100), (1020, 1100)))
SVG_WALL = (f'<svg {X} viewBox="0 0 1080 1300">'
            f'<g>{_lumps}</g>'
            f'<path fill-rule="evenodd" fill="{CORAL_A}" d="M0 470 Q270 430 540 460 T1080 470 V1300 H0 Z '
            f'M390 650 A150 95 0 1 0 690 650 A150 95 0 1 0 390 650 Z"/>'
            f'<path fill-rule="evenodd" fill="{CORAL_B}" opacity="0.55" d="M0 520 Q300 470 540 520 T1080 500 V1300 H0 Z '
            f'M390 650 A150 95 0 1 0 690 650 A150 95 0 1 0 390 650 Z"/>'
            f'<ellipse cx="540" cy="650" rx="154" ry="99" fill="none" stroke="#7a3d3a" stroke-width="10"/>'
            f'{_polyps}</svg>')
SVG_HOLE = f'<svg {X} viewBox="0 0 300 190"><ellipse cx="150" cy="95" rx="150" ry="95" fill="#05080a"/></svg>'
SVG_EYES = (f'<svg {X} viewBox="0 0 160 70">'
            '<circle cx="40" cy="30" r="11" fill="#e8f0d8"/><circle cx="42" cy="31" r="5" fill="#0b0f14"/>'
            '<circle cx="112" cy="27" r="11" fill="#e8f0d8"/><circle cx="114" cy="28" r="5" fill="#0b0f14"/>'
            f'<path d="M58 58 Q78 46 96 58" fill="none" stroke="{MORAY}" stroke-width="8" stroke-linecap="round" opacity="0.8"/></svg>')
SVG_DIM = f'<svg {X} viewBox="0 0 160 70"><rect x="0" y="0" width="160" height="70" rx="30" fill="#8a949c" opacity="0.75"/></svg>'

# 2. hand (blue wetsuit sleeve on the right, bare hand reaching left), 600x260
SVG_HAND = (f'<svg {X} viewBox="0 0 600 260">'
            f'<path d="M330 70 L600 50 L600 230 L330 210 Z" fill="{SLEEVE}"/>'
            f'<rect x="318" y="66" width="26" height="148" rx="8" fill="#163f73"/>'
            f'<path d="M330 80 C280 70 220 82 190 96 L70 92 C40 92 40 122 70 124 L180 128 L60 140 C30 142 30 172 60 172 L185 166 '
            f'L80 188 C52 194 58 222 86 218 L200 196 C230 214 290 214 330 200 Z" fill="{SKIN}" stroke="#b9805e" stroke-width="5"/>'
            f'<path d="M210 96 C190 70 150 52 120 50 C96 50 98 76 120 80 L200 104" fill="{SKIN}" stroke="#b9805e" stroke-width="5"/></svg>')

# 3. moray: side profile head facing left (closed / open with recurved teeth), 700x360; full body 1000x220
_speck = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{SPECK}" opacity="0.8"/>'
                 for x, y, r in ((300, 120, 7), (360, 170, 6), (430, 110, 8), (480, 200, 6), (540, 140, 7), (600, 210, 6),
                                 (640, 120, 7), (250, 190, 5), (520, 250, 6), (660, 260, 5)))
_teeth_up = ''.join(f'<path d="M{x} 190 q8 22 22 20 q-10 -6 -10 -20 Z" fill="#f5f2e8"/>' for x in range(70, 250, 30))
_teeth_lo = ''.join(f'<path d="M{x} 236 q8 -22 22 -20 q-10 6 -10 20 Z" fill="#f5f2e8"/>' for x in range(80, 240, 30))
_HEAD_TOP = (f'<path d="M700 90 C560 60 380 70 230 110 C150 130 80 150 30 180 L250 200 C400 205 560 230 700 250 Z" fill="{MORAY}"/>'
             f'{_speck}<circle cx="190" cy="140" r="16" fill="#e8f0d8"/><circle cx="186" cy="141" r="8" fill="#0b0f14"/>'
             f'<path d="M48 168 l-18 -26 l14 -4 l14 22 Z" fill="{MORAY_DARK}"/>')
SVG_HEAD_CLOSED = (f'<svg {X} viewBox="0 0 700 360">{_HEAD_TOP}'
                   f'<path d="M30 182 C120 200 260 210 420 215 L700 250 L700 300 C540 290 380 270 240 250 C150 238 80 214 30 182 Z" fill="{MORAY_DARK}"/>'
                   f'<path d="M34 182 L330 214" stroke="#2c3312" stroke-width="5"/></svg>')
SVG_HEAD_OPEN = (f'<svg {X} viewBox="0 0 700 360">{_HEAD_TOP}'
                 f'<path d="M40 186 L330 205 L330 236 L60 300 Z" fill="#7a2b33"/>'
                 f'{_teeth_up}'
                 f'<path d="M60 300 C140 290 250 262 330 236 L700 250 L700 320 C520 330 300 330 160 318 C110 314 80 308 60 300 Z" fill="{MORAY_DARK}"/>'
                 f'<g transform="rotate(-14 330 236)">{_teeth_lo}</g></svg>')
SVG_TOOTH_GLOW = (f'<svg {X} viewBox="0 0 700 360"><path d="M60 186 L330 205" stroke="{YELLOW}" stroke-width="34" stroke-linecap="round" opacity="0.55"/>'
                  f'<path d="M70 296 L320 240" stroke="{YELLOW}" stroke-width="30" stroke-linecap="round" opacity="0.45"/></svg>')
SVG_HOOKS = (f'<svg {X} viewBox="0 0 700 360" fill="none" stroke="#cfd6dc" stroke-width="7" stroke-linecap="round">'
             + ''.join(f'<path d="M{x} 182 L{x} 206 Q{x} 222 {x + 14} 220 Q{x + 24} 214 {x + 18} 202"/><path d="M{x + 18} 202 l-9 4"/>' for x in range(72, 250, 34))
             + '</svg>')
SVG_MORAY_BODY = (f'<svg {X} viewBox="0 0 1000 220">'
                  f'<path d="M20 110 C60 70 130 60 200 80 C320 115 420 40 560 70 C700 100 780 170 900 140 C950 128 980 110 1000 104 '
                  f'C980 124 950 150 900 166 C770 200 690 130 560 108 C430 86 330 160 200 128 C140 114 70 130 20 110 Z" fill="{MORAY}"/>'
                  + ''.join(f'<circle cx="{x}" cy="{y}" r="5" fill="{SPECK}"/>' for x, y in ((150, 92), (260, 104), (380, 86), (470, 80), (600, 92), (700, 128), (820, 150), (900, 148)))
                  + f'<circle cx="60" cy="92" r="7" fill="#e8f0d8"/><circle cx="58" cy="92" r="3.5" fill="#0b0f14"/>'
                  f'<path d="M22 110 L110 116" stroke="#2c3312" stroke-width="3"/></svg>')

# 4. jaw cutaway, 1000x500 (head faces left; throat runs right). Stacked: cavity < fish < throat jaw < shell < oral jaws
SVG_CAVITY = (f'<svg {X} viewBox="0 0 1000 500"><path d="M120 250 C260 200 420 210 560 228 L1000 236 L1000 268 L560 276 C420 292 260 300 120 250 Z" '
              f'fill="#a8454f"/><path d="M560 228 L1000 236 L1000 268 L560 276 Z" fill="#7a2b33"/></svg>')
SVG_SHELL = (f'<svg {X} viewBox="0 0 1000 500">'
             f'<path fill-rule="evenodd" fill="{MORAY}" d="M1000 120 C800 100 520 110 330 150 C230 170 150 200 90 240 C150 290 230 330 330 350 '
             f'C520 390 800 400 1000 380 Z M130 250 C260 196 430 204 640 222 L640 282 C430 300 260 304 130 250 Z"/>'
             f'<path d="M640 222 L640 282" stroke="#f5f2e8" stroke-width="4" stroke-dasharray="10 8" opacity="0.6"/>'
             f'<circle cx="240" cy="190" r="18" fill="#e8f0d8"/><circle cx="236" cy="191" r="9" fill="#0b0f14"/></svg>')
SVG_ORAL_UP = (f'<svg {X} viewBox="0 0 1000 500"><path d="M90 240 C160 214 260 200 360 206 L360 222 C260 220 170 232 110 250 Z" fill="{MORAY_DARK}"/>'
               + ''.join(f'<path d="M{x} 222 q8 20 20 18 q-9 -5 -9 -18 Z" fill="#f5f2e8"/>' for x in range(120, 350, 34)) + '</svg>')
SVG_ORAL_LO = (f'<svg {X} viewBox="0 0 1000 500"><path d="M110 254 C170 276 260 290 360 292 L360 278 C260 276 170 268 120 250 Z" fill="{MORAY_DARK}"/>'
               + ''.join(f'<path d="M{x} 278 q8 -20 20 -18 q-9 5 -9 18 Z" fill="#f5f2e8"/>' for x in range(130, 350, 34)) + '</svg>')
SVG_PHARY = (f'<svg {X} viewBox="0 0 220 120">'
             f'<path d="M10 20 C70 6 150 6 210 18 L210 40 C150 34 70 36 10 46 Z" fill="{YELLOW}"/>'
             f'<path d="M10 100 C70 114 150 114 210 102 L210 80 C150 86 70 84 10 74 Z" fill="{YELLOW}"/>'
             + ''.join(f'<path d="M{x} 44 l10 18 l6 -20 Z" fill="#ffffff"/><path d="M{x} 76 l10 -18 l6 20 Z" fill="#ffffff"/>' for x in (24, 64, 104, 144))
             + '</svg>')
SVG_FLOW = (f'<svg {X} viewBox="0 0 400 200" fill="none" stroke="#bfefff" stroke-width="6" stroke-linecap="round" stroke-dasharray="18 14">'
            '<path d="M0 60 C120 60 220 90 400 100"/><path d="M0 100 C140 100 260 100 400 100"/><path d="M0 140 C120 140 220 110 400 100"/></svg>')

# 5. fish (grey reef fish facing left), 260x140
SVG_FISH = (f'<svg {X} viewBox="0 0 260 140">'
            '<path d="M20 70 C60 20 160 18 200 60 L250 22 L240 70 L250 118 L200 80 C160 122 60 120 20 70 Z" fill="#9aa7b0" stroke="#5f6b73" stroke-width="5"/>'
            '<circle cx="62" cy="62" r="9" fill="#0b0f14"/><path d="M110 40 L120 100" stroke="#5f6b73" stroke-width="4"/></svg>')
SVG_FISH_GHOST = SVG_FISH.replace('#9aa7b0', 'none').replace('#5f6b73', '#bfefff')

# 6-7. primitives: tick, cross, red arrow, smell lines, ring
SVG_TICK = f'<svg {X} viewBox="0 0 100 100"><path d="M14 54 L40 78 L88 22" fill="none" stroke="{GREEN}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/></svg>'
SVG_CROSS = f'<svg {X} viewBox="0 0 100 100"><path d="M18 18 L82 82 M82 18 L18 82" fill="none" stroke="{RED}" stroke-width="16" stroke-linecap="round"/></svg>'
SVG_ARROW = (f'<svg {X} viewBox="0 0 400 120"><path d="M10 60 L330 60" stroke="{RED}" stroke-width="22" stroke-linecap="round"/>'
             f'<path d="M300 14 L392 60 L300 106 Z" fill="{RED}"/></svg>')
SVG_SMELL = (f'<svg {X} viewBox="0 0 500 160" fill="none" stroke="{YELLOW}" stroke-width="7" stroke-linecap="round" opacity="0.9">'
             '<path d="M500 40 C440 10 400 70 340 40 S240 10 180 40 S80 70 0 40"/>'
             '<path d="M500 90 C440 60 400 120 340 90 S240 60 180 90 S80 120 0 90"/>'
             '<path d="M500 135 C440 105 400 160 340 135 S240 105 180 135"/></svg>')
SVG_RING = f'<svg {X} viewBox="0 0 400 260"><ellipse cx="200" cy="130" rx="190" ry="120" fill="none" stroke="{RED}" stroke-width="12"/></svg>'

# ------------------------------------------------------------------ layer helpers


def comp(name, x, y, w, h, props, **kw):
    l = {'type': 'component', 'name': name, 'x': x, 'y': y, 'width': w, 'height': h, 'props': props}
    l.update(kw)
    return l


def svg(markup, x, y, w, h, **kw):
    l = {'type': 'svg', 'markup': markup, 'x': x, 'y': y, 'width': w, 'height': h}
    l.update(kw)
    return l


def tag(text, x, y, at, out=None, accent=RED, size=34, w=860, **kw):
    p = {'text': text, 'at': at, 'size': size, 'accent': accent, 'align': 'center'}
    if out is not None:
        p['out'] = out
    return comp('explainer/Tag', x, y, w, int(size * 2.6), p, depth=0, z=20, **kw)


def headline(text, at, y='19%', color='white', size=64, out=None, **kw):
    p = {'text': text, 'at': at, 'size': size, 'color': color, 'underline': True}
    if out is not None:
        p['out'] = out
    lines = text.count('\n') + 1
    return comp('explainer/Headline', '50%', y, 1000, int(size * 1.6 * lines + 40), p, depth=0, z=20, **kw)


def chip(lit1=None, lit2=None, flash2=None):
    """Two-slot counter, top-left. lit = scene-local time the slot lights (None = stays dark; 0 = lit all scene)."""
    out = []
    for i, (label, lit, col) in enumerate((('MOUTH 1', lit1, YELLOW), ('MOUTH 2', lit2, RED))):
        cx = 170 + i * 250
        out.append({'type': 'rect', 'x': cx, 'y': '12.5%', 'width': 230, 'height': 70, 'radius': 35,
                    'fill': 'rgba(10,16,20,0.75)', 'stroke': '#5b6770', 'strokeWidth': 4, 'depth': 0, 'z': 30})
        out.append({'type': 'text', 'text': label, 'x': cx, 'y': '12.5%', 'fontSize': 34, 'color': '#6f7a82', 'depth': 0, 'z': 31})
        if lit is not None:
            lay = {'type': 'rect', 'x': cx, 'y': '12.5%', 'width': 230, 'height': 70, 'radius': 35, 'fill': col,
                   'depth': 0, 'z': 32, 'start': lit}
            if lit > 0:
                lay['enter'] = {'type': 'pop', 'at': lit, 'duration': 0.25}
            out.append(lay)
            out.append({'type': 'text', 'text': label, 'x': cx, 'y': '12.5%', 'fontSize': 34, 'color': '#0b0f14',
                        'depth': 0, 'z': 33, 'start': lit})
    if flash2 is not None:
        out.append({'type': 'rect', 'x': 420, 'y': '12.5%', 'width': 230, 'height': 70, 'radius': 35, 'fill': RED, 'depth': 0, 'z': 32,
                    'start': flash2, 'end': flash2 + 0.5})
    return out


def ocean(depth=12, rays=5, snow=50, **extra):
    p = {'depth': depth, 'rays': rays, 'seed': 5, 'snow': snow}
    p.update(extra)
    return {'type': 'component', 'name': 'explainer/Ocean', 'depth': 0.12, 'overscan': 1.2, 'props': p}


REEF = ocean(depth=12, rays=5, snow=50)
TEAL = ocean(depth=60, rays=2, snow=40)
DARK = ocean(depth=300, rays=0, snow=40)

GAP = (540, 730)           # hole centre on screen (wall layer at y 730, hole at wall-local (540, 650) -> (540, 730))
WALL_Y = 730 + (650 - 650) + 0  # wall box centre y (1300 tall box, hole at local y 650 = box centre)


def wall_layers(eyes=True, blink_at=None, dim_at=None):
    lay = [svg(SVG_HOLE, GAP[0], GAP[1], 300, 190, z=1, id='hole')]
    if eyes:
        kf = []
        if blink_at is not None:
            kf = [{'t': blink_at, 'scaleY': 1}, {'t': blink_at + 0.08, 'scaleY': 0.1}, {'t': blink_at + 0.18, 'scaleY': 1}]
        lay.append(svg(SVG_EYES, GAP[0], GAP[1] - 10, 160, 70, z=2, id='eyes', keyframes=kf,
                       idle=[{'type': 'bob', 'amount': 3, 'speed': 0.4}]))
        if dim_at is not None:
            lay.append(svg(SVG_DIM, GAP[0], GAP[1] - 10, 170, 76, z=3, start=dim_at, enter={'type': 'fade', 'at': dim_at, 'duration': 0.3}))
    lay.append(svg(SVG_WALL, '50%', WALL_Y, 1080, 1300, z=4, id='wall'))
    return lay


def hand(x=990, y=760, z=8, **kw):
    return svg(SVG_HAND, x, y, 520, 225, z=z, id=kw.pop('id', 'hand'), **kw)


def notes(key):
    return ' '.join(PARAS[i][1] for i in SC[key]['paras'])


scenes = []


def add(key, background, layers, camera=None, sfx=None, **kw):
    s = {'id': f's{len(scenes) + 1:02d}_{key}', 'duration': SC[key]['dur'], 'background': background, 'layers': layers}
    if camera:
        s['camera'] = camera
    if sfx:
        s['sfx'] = sfx
    s.update(kw)
    s['notes'] = notes(key)
    scenes.append(s)


# ---------------------------------------------------------------- s01 hook (frame 0 = cover = loop frame)
HOOK_LAYERS = wall_layers(eyes=True, blink_at=1.4) + [hand(idle=[{'type': 'bob', 'amount': 4, 'speed': 0.5}],
                                                        keyframes=[{'t': 0, 'x': 990}, {'t': 1.8, 'x': 975}, {'t': 2.6, 'x': 990}])]
d = SC['hook']['dur']
add('hook', REEF, copy.deepcopy(HOOK_LAYERS) + chip() + [
    headline('2 MOUTHS', 0.0, color='red', size=96),
    # x-ray glimpse (frames 0-~0.6 s): the throat jaw glows inside the gap, shown not named (retention nice-to-have)
    svg(SVG_PHARY, GAP[0] + 30, GAP[1] + 22, 150, 82, z=1.5, end=0.75, opacity=0.9, shadow='0 0 14px #ffe14d',
        exit={'type': 'fade', 'duration': 0.25}),
], camera={'keyframes': [{'t': 0, 'zoom': 1.0}, {'t': d, 'zoom': 1.05, 'ease': 'inOut'}]},
    sfx=[{'cue': 'underwater_rumble', 'at': 0.0, 'volume': 0.13}, {'cue': 'bubbles', 'at': 0.6, 'volume': 0.3}])

# ---------------------------------------------------------------- s02 misdirect: wide checklist, then whip back to the crack
k = 'misdirect'
t_never = A(k, 'never')
items_at = [A(k, 'sharks'), A(k, 'jellyfish'), A(k, 'crab')]
add(k, ocean(depth=8, rays=6, snow=40), [
    comp('explainer/GreatWhite', '78%', '30%', 300, 120, {'silhouette': '#5c7d8c'}, end=t_never, opacity=0.7,
         keyframes=[{'t': 0, 'x': '86%'}, {'t': t_never, 'x': '70%'}]),
    comp('explainer/Diver', '24%', '52%', 420, 200, {'arms': 'side', 'kick': True, 'bubbles': True}, end=t_never, flipX=True),
    comp('explainer/Options', '50%', '33%', 900, 520, {'title': 'CHECKED FOR', 'items': ['SHARKS', 'JELLYFISH', 'SUSPICIOUS CRAB'],
                                                       'at': items_at[0] - 0.3, 'itemAt': items_at, 'size': 52}, depth=0, z=10, end=t_never),
    *[svg(SVG_TICK, 900, 578 + 108 * i, 70, 70, z=12, depth=0, start=t, end=t_never, enter={'type': 'pop', 'at': t, 'duration': 0.2})
      for i, t in enumerate(items_at)],
    # whip back to the gap at "never"
    *[dict(l, start=t_never) for l in wall_layers(eyes=True, blink_at=t_never + 0.6)],
    hand(start=t_never),
    svg(SVG_RING, GAP[0], GAP[1], 420, 270, z=9, start=A(k, 'crack'), enter={'type': 'pop', 'at': A(k, 'crack'), 'duration': 0.25}),
    tag('NOT ON THE LIST', '50%', '52%', A(k, 'crack'), size=40, w=640),
    *[dict(l, start=t_never) for l in chip()],
], camera={'keyframes': [{'t': 0, 'zoom': 1.0}, {'t': t_never - 0.05, 'zoom': 0.94}, {'t': t_never, 'zoom': 1.0},
                         {'t': SC[k]['dur'], 'zoom': 1.04}]},
    sfx=[{'cue': 'pop', 'at': t, 'volume': 0.5} for t in items_at] + [{'cue': 'whoosh', 'at': t_never - 0.15, 'volume': 0.7},
                                                                     {'cue': 'sonar_ping', 'at': A(k, 'touching'), 'volume': 0.4}])

# ---------------------------------------------------------------- s03 reveal + honest scale (300 px/m)
k = 'reveal'
t_big = A(k, 'biggest')
PPM = 300
FLOOR = 1050
add(k, REEF, [
    *[dict(l, end=t_big) for l in wall_layers(eyes=False)],
    svg(SVG_HEAD_CLOSED, GAP[0] + 150, GAP[1] + 20, 420, 216, z=2, end=t_big,
        keyframes=[{'t': 0, 'x': GAP[0] + 260, 'scale': 0.7}, {'t': A(k, 'moray'), 'x': GAP[0] + 90, 'scale': 0.9, 'ease': 'out'}]),
    hand(end=t_big, keyframes=[{'t': 0, 'x': 990}, {'t': A(k, 'moray'), 'x': 1040, 'ease': 'out'}]),
    headline('MORAY EEL', A(k, 'moray'), out=t_big),
    # scale card: same px per metre on both
    {'type': 'rect', 'x': '50%', 'y': FLOOR, 'width': 1000, 'height': 6, 'fill': WHITE, 'opacity': 0.6, 'start': t_big},
    svg(SVG_MORAY_BODY, 50 + 450, FLOOR - 120, 3.0 * PPM, 3.0 * PPM * 0.22, start=t_big,
        enter={'type': 'slideRight', 'at': t_big, 'duration': 0.4}, idle=[{'type': 'sway', 'amount': 1.2, 'speed': 0.4}]),
    comp('explainer/ScaleBar', 50 + 450, FLOOR + 40, 3.0 * PPM, 60, {'label': 'GIANT MORAY: UP TO ~3 M', 'at': A(k, 'three'), 'from': 'left', 'color': RED}, start=t_big, depth=0),
    comp('explainer/You', 880, FLOOR - int(1.75 * PPM / 2), 220, int(1.75 * PPM), {'pose': 'stand', 'pxPerM': PPM, 'align': 'bottom'},
         start=A(k, 'longer'), enter={'type': 'pop', 'at': A(k, 'longer'), 'duration': 0.25}),
    tag('YOU: 1.75 M', 880, '37%', A(k, 'longer'), size=30, w=320, accent=WHITE),
    *chip(),
], camera={'preset': 'drift', 'amount': 0.3},
    sfx=[{'cue': 'whoosh_long', 'at': A(k, 'moray') - 0.2, 'volume': 0.6}, {'cue': 'ding', 'at': A(k, 'longer'), 'volume': 0.6}])

# ---------------------------------------------------------------- s04 rung 1: mouth one, hooked teeth (plant shape only)
k = 'rung1'
t_hooks = A(k, 'hooks')
add(k, TEAL, [
    svg(SVG_HEAD_OPEN, '52%', '38%', 920, 473, z=2, idle=[{'type': 'breathe', 'amount': 0.01, 'speed': 0.4}]),
    svg(SVG_TOOTH_GLOW, '52%', '38%', 920, 473, z=3, start=A(k, 'teeth'), enter={'type': 'fade', 'at': A(k, 'teeth'), 'duration': 0.3},
        idle=[{'type': 'pulse', 'amount': 0.05, 'speed': 1.2}]),
    svg(SVG_HOOKS, '52%', '38%', 920, 473, z=4, start=t_hooks, end=t_hooks + 1.1,
        enter={'type': 'fade', 'at': t_hooks, 'duration': 0.15}, exit={'type': 'fade', 'duration': 0.2}),
    hand(x=1000, y='47%', z=5, opacity=0.9),
    tag('TEETH CURVE BACKWARD', '50%', '54%', A(k, 'curved'), size=36, w=700, accent=YELLOW),
    *chip(lit1=A(k, 'one')),
], camera={'keyframes': [{'t': 0, 'zoom': 1.0}, {'t': SC[k]['dur'], 'zoom': 1.08}]},
    sfx=[{'cue': 'click', 'at': A(k, 'one'), 'volume': 0.6}, {'cue': 'tick', 'at': t_hooks, 'volume': 0.6}])

# ---------------------------------------------------------------- s05 rung 2: defensive bite (head lunges out in front of the wall)
k = 'rung2'
t_hand, t_bit = A(k, 'hand'), A(k, 'bitten')
add(k, REEF, [
    *wall_layers(eyes=True, dim_at=A(k, 'barely')),
    tag('EYESIGHT: POOR', '50%', '27%', A(k, 'barely'), out=t_bit, size=34, w=520, accent=WHITE),
    hand(keyframes=[{'t': 0, 'x': 990}, {'t': t_hand, 'x': 990}, {'t': t_hand + 0.5, 'x': 900, 'ease': 'out'}]),
    svg(SVG_HEAD_OPEN, GAP[0] - 60, GAP[1] + 10, 560, 288, z=6, start=t_bit,
        keyframes=[{'t': t_bit, 'scale': 0.35, 'x': GAP[0] + 40}, {'t': t_bit + 0.18, 'scale': 1.0, 'x': GAP[0] + 130, 'ease': 'out'}]),
    headline('DEFENDING ITS HOME', t_bit, color='red', size=58),
    tag('QUESTIONS: LATER', '50%', '55%', A(k, 'questions'), size=30, w=460, accent=WHITE),
    *chip(lit1=0),
], camera={'keyframes': [{'t': 0, 'zoom': 1.0}, {'t': t_bit, 'zoom': 1.06}, {'t': t_bit + 0.15, 'zoom': 1.12, 'ease': 'out'}],
           'shake': [{'at': t_bit, 'duration': 0.35, 'amplitude': 16}]},
    sfx=[{'cue': 'impact', 'at': t_bit, 'volume': 0.8}, {'cue': 'stinger', 'at': t_bit, 'volume': 0.5}])

# ---------------------------------------------------------------- s06 rhetorical question (freeze on the locked bite)
k = 'rq'
BITE_LAYERS = wall_layers(eyes=False) + [hand(x=900), svg(SVG_HEAD_OPEN, GAP[0] + 130, GAP[1] + 10, 560, 288, z=6)]
add(k, REEF, copy.deepcopy(BITE_LAYERS) + [
    headline('WORST MOVE?', A(k, 'worst'), color='red'),
    tag('= FIRST INSTINCT', '50%', '55%', A(k, 'first'), size=34, w=560, accent=WHITE),
    *chip(lit1=0),
], camera={'keyframes': [{'t': 0, 'zoom': 1.12}, {'t': SC[k]['dur'], 'zoom': 1.17, 'ease': 'inOut'}]},
    grade={'saturate': 0.8, 'vignette': 0.3}, sfx=[{'cue': 'heartbeat_slow', 'at': A(k, 'first'), 'volume': 0.5}])

# ---------------------------------------------------------------- s07 pull: hooks point inward (callback to the plant), no wound
k = 'pull'
t_yank = A(k, 'yanking')
add(k, TEAL, [
    headline('PULL', 0.05, color='red', size=110, out=A(k, 'those')),
    svg(SVG_CROSS, 790, '19%', 120, 120, z=21, depth=0, start=0.25, end=A(k, 'those'), enter={'type': 'pop', 'at': 0.25, 'duration': 0.2}),
    svg(SVG_HEAD_OPEN, '48%', '38%', 920, 473, z=2),
    svg(SVG_HOOKS, '48%', '38%', 920, 473, z=4, start=A(k, 'hooks'), end=A(k, 'hooks') + 0.9, enter={'type': 'fade', 'at': A(k, 'hooks'), 'duration': 0.15}),
    svg(SVG_TOOTH_GLOW.replace(YELLOW, RED), '48%', '38%', 920, 473, z=3, start=t_yank, enter={'type': 'fade', 'at': t_yank, 'duration': 0.2}),
    hand(x=820, y='41%', z=5, keyframes=[{'t': 0, 'x': 820}, {'t': t_yank, 'x': 820}, {'t': t_yank + 0.25, 'x': 860, 'ease': 'out'},
                                         {'t': t_yank + 0.45, 'x': 835}]),
    svg(SVG_ARROW, 840, '50%', 300, 90, z=6, start=t_yank, enter={'type': 'wipeRight', 'at': t_yank, 'duration': 0.3}),
    tag('POINT INWARD', '50%', '27%', A(k, 'inward'), size=34, w=520, accent=YELLOW),
    tag("DON'T PULL", '50%', '55%', t_yank, size=44, w=520),
    *chip(lit1=0),
], camera={'preset': 'pushIn', 'amount': 0.4, 'shake': [{'at': t_yank + 0.2, 'duration': 0.3, 'amplitude': 10}]},
    sfx=[{'cue': 'impact', 'at': 0.05, 'volume': 0.6}, {'cue': 'click', 'at': A(k, 'hooks'), 'volume': 0.6}, {'cue': 'glitch', 'at': t_yank, 'volume': 0.5}])

# ---------------------------------------------------------------- s08 handshake joke
k = 'handshake'
add(k, REEF, copy.deepcopy(BITE_LAYERS) + [
    tag('THE HANDSHAKE', '50%', '24%', A(k, 'handshake'), size=40, w=560, accent=WHITE),
    tag('YOU LET GO SECOND', '50%', '55%', A(k, 'end'), size=36, w=600),
    *chip(lit1=0),
], camera={'keyframes': [{'t': 0, 'zoom': 1.1}, {'t': SC[k]['dur'], 'zoom': 1.04}],
           'shake': [{'at': A(k, 'handshake'), 'duration': 0.6, 'amplitude': 6, 'frequency': 6}]},
    sfx=[{'cue': 'pop', 'at': A(k, 'end'), 'volume': 0.5}])

# ---------------------------------------------------------------- s09 turnstile (music out, plain card)
k = 'turnstile'
add(k, DARK, [
    headline("IT'S NOT TRYING\nTO EAT YOU", A(k, 'not'), y='34%', size=74),
    svg(SVG_TICK, '50%', '50%', 150, 150, depth=0, z=21, start=A(k, 'eat'), enter={'type': 'pop', 'at': A(k, 'eat'), 'duration': 0.25}),
    *chip(lit1=0),
], sfx=[{'cue': 'ding', 'at': A(k, 'eat'), 'volume': 0.5}])

# ---------------------------------------------------------------- s10 you, as a fish (spine payoff, slot 2)
k = 'fish'
t_f = A(k, 'fish')
add(k, TEAL, [
    comp('explainer/You', '50%', '38%', 240, 420, {'pose': 'shrug'}, end=t_f + 0.3, exit={'type': 'fade', 'duration': 0.3}),
    svg(SVG_FISH, '50%', '38%', 420, 226, start=t_f, enter={'type': 'pop', 'at': t_f, 'duration': 0.3},
        idle=[{'type': 'bob', 'amount': 8, 'speed': 0.6}]),
    tag('YOU (AS A FISH)', '50%', '50%', t_f + 0.2, size=34, w=520, accent=WHITE),
    headline('MOUTH 2', A(k, 'mouth'), color='red', size=90),
    *chip(lit1=0, lit2=A(k, 'two')),
], camera={'preset': 'pushIn', 'amount': 0.3},
    sfx=[{'cue': 'pop', 'at': t_f, 'volume': 0.5}, {'cue': 'riser', 'at': A(k, 'meet'), 'volume': 0.5}])

# ---------------------------------------------------------------- s11-s13 the cutaway (5 stacked layers, one coordinate frame)
CX, CY, CW, CH = 540, 760, 1080, 540    # cutaway box (1000x500 viewBox scaled to 1080x540, 1.08 px per unit)
U = 1.08


def cut_layers(fish_kf, phary_kf, low_kf, fish_end=None):
    fish = svg(SVG_FISH, CX, CY, 230, 124, z=2, keyframes=fish_kf)
    if fish_end is not None:
        fish['end'] = fish_end
    return [
        svg(SVG_CAVITY, CX, CY, CW, CH, z=1),
        fish,
        svg(SVG_PHARY, CX + int((690 - 500) * U), CY, 200, 110, z=3, keyframes=phary_kf),
        svg(SVG_SHELL, CX, CY, CW, CH, z=4),
        svg(SVG_ORAL_UP, CX, CY, CW, CH, z=5),
        svg(SVG_ORAL_LO, CX, CY, CW, CH, z=5, anchorX=0.36, anchorY=0.5, keyframes=low_kf),
    ]


PH_HOME = CX + int((690 - 500) * U)     # throat jaw parked behind the dashed throat line (hidden by the shell)
PH_OUT = CX + int((470 - 500) * U)      # launched into the mouth window
MOUTH_X = CX + int((250 - 500) * U)
k = 'suction'
t_suck = A(k, 'suck')
add(k, DARK, cut_layers(
    fish_kf=[{'t': 0, 'x': CX - 560}, {'t': t_suck, 'x': CX - 470}, {'t': t_suck + 1.0, 'x': CX - 455}],
    phary_kf=[{'t': 0, 'x': PH_HOME}],
    low_kf=[{'t': 0, 'rotate': 14}]) + [
    svg(SVG_FLOW, CX - 330, CY, 320, 160, z=3, start=t_suck, end=A(k, 'second'), opacity=0.8,
        keyframes=[{'t': t_suck, 'x': CX - 380, 'opacity': 0.9}, {'t': t_suck + 0.9, 'x': CX - 350, 'opacity': 0.25}]),
    svg(SVG_CROSS, CX - 330, CY - 150, 110, 110, z=8, start=A(k, "can't"), end=A(k, 'second'),
        enter={'type': 'pop', 'at': A(k, "can't"), 'duration': 0.2}),
    tag('WEAK SUCTION', '50%', '27%', A(k, 'suck'), out=A(k, 'second'), size=34, w=480, accent=WHITE),
    svg(SVG_PHARY, PH_HOME, CY, 230, 126, z=6, opacity=0.6, start=A(k, 'second'), enter={'type': 'fade', 'at': A(k, 'second'), 'duration': 0.3},
        idle=[{'type': 'pulse', 'amount': 0.08, 'speed': 1.5}]),
    tag('PHARYNGEAL JAW', '72%', '48%', A(k, 'jaw'), size=30, w=460, accent=YELLOW),
    *chip(lit1=0, lit2=0),
], camera={'preset': 'pushIn', 'amount': 0.3}, sfx=[{'cue': 'bubbles', 'at': t_suck, 'volume': 0.4}])

k = 'launch'
t_catch, t_launch, t_grab = A(k, 'catch'), A(k, 'launches'), A(k, 'mouth', end=True)
add(k, DARK, cut_layers(
    fish_kf=[{'t': 0, 'x': CX - 455}, {'t': t_catch, 'x': MOUTH_X}, {'t': t_grab, 'x': MOUTH_X}, {'t': t_grab + 0.3, 'x': MOUTH_X + 70}],
    phary_kf=[{'t': 0, 'x': PH_HOME}, {'t': t_launch, 'x': PH_HOME}, {'t': t_launch + 0.35, 'x': PH_OUT, 'ease': 'out'},
              {'t': t_grab + 0.3, 'x': PH_OUT + 70}],
    low_kf=[{'t': 0, 'rotate': 14}, {'t': t_catch, 'rotate': 14}, {'t': t_catch + 0.15, 'rotate': 0, 'ease': 'in'}]) + [
    tag('MOUTH 2: THROAT JAW', '50%', '27%', t_launch, size=38, w=640),
    tag('A MOUTH INSIDE A MOUTH', '50%', '56%', A(k, 'monster'), size=34, w=640, accent=WHITE),
    *chip(lit1=0, lit2=0, flash2=t_launch),
], camera={'keyframes': [{'t': 0, 'zoom': 1.0}, {'t': t_launch, 'zoom': 1.05}, {'t': t_launch + 0.3, 'zoom': 1.15, 'x': '56%', 'ease': 'out'}],
           'shake': []},
    sfx=[{'cue': 'click', 'at': t_catch, 'volume': 0.7}, {'cue': 'whoosh', 'at': t_launch - 0.1, 'volume': 0.8},
         {'cue': 'riser', 'at': t_grab - 0.6, 'volume': 0.4}])

k = 'ratchet'
t0r, t_gone = A(k, 'and'), A(k, 'gone')
steps = [t0r + i * (t_gone - t0r) / 4 for i in range(5)]
fish_kf, ph_kf, lo_kf = [{'t': 0, 'x': MOUTH_X + 70}], [{'t': 0, 'x': PH_OUT + 70}], [{'t': 0, 'rotate': 0}]
fx = MOUTH_X + 70
for i, t in enumerate(steps[:4]):
    # front jaw lets go, throat jaw hauls the fish one step back, front jaw re-bites
    lo_kf += [{'t': t, 'rotate': 0}, {'t': t + 0.12, 'rotate': 10}, {'t': t + 0.45, 'rotate': 0}]
    fx += 120
    fish_kf += [{'t': t + 0.12, 'x': fx - 120}, {'t': t + 0.4, 'x': fx, 'ease': 'out'}]
    ph_kf += [{'t': t + 0.12, 'x': PH_OUT + 70 + 120 * i}, {'t': t + 0.4, 'x': PH_OUT + 70 + 120 * (i + 1), 'ease': 'out'}]
ph_kf += [{'t': t_gone + 0.3, 'x': PH_HOME}]
add(k, DARK, cut_layers(fish_kf, ph_kf, lo_kf, fish_end=t_gone + 0.35) + [
    tag('HAND OVER HAND', '50%', '27%', A(k, 'hand'), size=38, w=560, accent=YELLOW),
    *[tag(lbl, '50%', '56%', t + 0.1, out=t + 0.45, size=40, w=200, accent=c)
      for t, lbl, c in zip(steps[:4], ['1', '2', '1', '2'], [YELLOW, RED, YELLOW, RED])],
    *chip(lit1=0, lit2=0),
], camera={'keyframes': [{'t': 0, 'zoom': 1.15, 'x': '56%'}, {'t': SC[k]['dur'], 'zoom': 1.05, 'x': '54%'}],
           'shake': [{'at': A(k, 'grabs'), 'duration': 0.3, 'amplitude': 12}]},
    sfx=[{'cue': 'impact', 'at': A(k, 'grabs'), 'volume': 0.6}] + [{'cue': 'click', 'at': t + 0.12, 'volume': 0.55} for t in steps[:4]] + [{'cue': 'whoosh_long', 'at': t_gone - 0.2, 'volume': 0.5}])

# ---------------------------------------------------------------- s14 twist: the friendly one at a feeding site
k = 'twist'
t_friend = A(k, 'friendly')
add(k, ocean(depth=6, rays=7, snow=30), [
    svg(SVG_WALL, '18%', 900, 900, 1083, z=1, opacity=1.0),
    svg(SVG_MORAY_BODY, 494, 900, 600, 132, z=2, flipX=True, start=t_friend - 0.2,
        keyframes=[{'t': t_friend - 0.2, 'x': 300, 'opacity': 0}, {'t': t_friend + 0.6, 'x': 494, 'opacity': 1, 'ease': 'out'}],
        idle=[{'type': 'sway', 'amount': 1.5, 'speed': 0.5}]),
    comp('explainer/Diver', '80%', '46%', 460, 220, {'arms': 'forward', 'bubbles': True}, flipX=True,
         idle=[{'type': 'bob', 'amount': 6, 'speed': 0.4}]),
    svg(SVG_FISH, 730, 880, 110, 60, z=6, start=A(k, 'feed'), enter={'type': 'pop', 'at': A(k, 'feed'), 'duration': 0.2}),
    headline('THE FRIENDLY ONES', t_friend, color='red', size=62),
    tag('FEEDING SITES', '50%', '27%', A(k, 'feed'), size=34, w=460, accent=WHITE),
    *chip(lit1=0, lit2=0),
], camera={'preset': 'pullOut', 'amount': 0.4}, transitionIn={'type': 'dipBlack', 'duration': 0.3},
    sfx=[{'cue': 'whoosh_long', 'at': 0.0, 'volume': 0.5}, {'cue': 'sonar_ping', 'at': t_friend, 'volume': 0.4}])

# ---------------------------------------------------------------- s15 you taught it: smell lines from the fish-holding hand
k = 'taught'
FEED_LAYERS = [
    svg(SVG_HEAD_CLOSED, 300, '38%', 640, 330, z=2, flipX=True, idle=[{'type': 'breathe', 'amount': 0.015, 'speed': 0.5}]),
    hand(x=830, y='39%', z=5),
]
add(k, REEF, copy.deepcopy(FEED_LAYERS) + [
    svg(SVG_FISH, 600, '38%', 190, 102, z=6, id='fed_fish'),
    svg(SVG_SMELL, 470, '33%', 420, 134, z=7, start=A(k, 'smell'), opacity=0.9,
        keyframes=[{'t': A(k, 'smell'), 'x': 640, 'opacity': 0}, {'t': A(k, 'smell') + 0.8, 'x': 470, 'opacity': 0.9}]),
    tag('YOU TAUGHT IT', '50%', '24%', A(k, 'taught'), size=36, w=520, accent=WHITE),
    tag('FINGERS = FISH SMELL', '50%', '52%', A(k, 'smell'), size=36, w=640, accent=YELLOW),
    *chip(lit1=0, lit2=0),
], camera={'preset': 'drift', 'amount': 0.3}, sfx=[{'cue': 'bubbles', 'at': A(k, 'fed'), 'volume': 0.3}])

# ---------------------------------------------------------------- s16 can't see: fish is gone, only the glowing hand is left
k = 'cantsee'
t_which = A(k, 'which')
add(k, REEF, copy.deepcopy(FEED_LAYERS) + [
    svg(SVG_FISH, 600, '38%', 190, 102, z=6, end=t_which, exit={'type': 'fade', 'duration': 0.25}),
    svg(SVG_FISH_GHOST, 640, '38%', 220, 118, z=6, start=t_which, enter={'type': 'fade', 'at': t_which, 'duration': 0.25},
        idle=[{'type': 'pulse', 'amount': 0.06, 'speed': 1.5}]),
    svg(SVG_DIM, 446, 693, 60, 30, z=3, start=A(k, 'barely'), enter={'type': 'fade', 'at': A(k, 'barely'), 'duration': 0.3}),
    tag('EYESIGHT: POOR', '50%', '24%', A(k, 'barely'), out=t_which, size=34, w=480, accent=WHITE),
    tag('WHICH PART IS THE FISH?', '50%', '52%', t_which, size=36, w=720),
    *chip(lit1=0, lit2=0),
], camera={'keyframes': [{'t': 0, 'zoom': 1.0}, {'t': SC[k]['dur'], 'zoom': 1.1, 'x': '58%'}]},
    sfx=[{'cue': 'tick', 'at': t_which, 'volume': 0.5}])

# ---------------------------------------------------------------- s17 stinger: frame-1 layers verbatim, hard stop
k = 'stinger'
t_fing = A(k, 'fingers')
add(k, REEF, copy.deepcopy(HOOK_LAYERS) + chip() + [
    headline('2 MOUTHS', 0.0, color='red', size=96),
    svg(SVG_RING, 770, 760, 220, 143, z=9, start=t_fing, enter={'type': 'pop', 'at': t_fing, 'duration': 0.2}),
], camera={'keyframes': [{'t': 0, 'zoom': 1.05}, {'t': SC[k]['dur'], 'zoom': 1.0, 'ease': 'out'}]},
    sfx=[{'cue': 'heartbeat_slow', 'at': t_fing, 'volume': 0.6}])

# ---------------------------------------------------------------- storyboard
t_relax = SC['turnstile']['start']
t_back = SC['fish']['start']
sb = {
    'version': 1,
    'id': SLUG,
    'title': 'How A Moray Eel Bites You',
    'format': '9:16',
    'fps': 30,
    'scenes': scenes,
    'captions': {
        'maxWords': 3, 'maxChars': 18,
        'glue': ['moray eel', 'fish hooks', 'mouth one', 'mouth two', 'three metres', 'second jaw', 'hand over hand', 'questions later'],
        'words': [{'text': w['text'], 'start': w['start'], 'end': w['end'],
                   **({'emph': True} if clean(w['text']) in {'two', 'mouths', 'hooks', 'pull', 'bitten', 'second', 'friendly', 'fingers', 'gone'} else {})}
                  for w in WORDS],
        'style': {'font': 'display', 'fontSize': 88, 'color': '#ffffff', 'highlight': '#ff5a4a', 'highlightMode': 'none',
                  'strokeWidth': 12, 'uppercase': True, 'y': 0.70},
    },
    'audio': {
        'voice': [{'src': f'episodes/{SLUG}/mix.wav', 'start': 0, 'volume': 1, 'duration': round(TOTAL, 3)}],
        # two bed entries = the turnstile music drop (no mute cue in the schema)
        'music': [
            {'src': 'music/deep_ocean.m4a', 'start': 0, 'end': round(t_relax, 3), 'volume': 0.24, 'duckTo': 0.14, 'fadeIn': 0.2, 'fadeOut': 0.25},
            {'src': 'music/deep_ocean.m4a', 'start': round(t_back, 3), 'end': round(TOTAL, 3), 'volume': 0.24, 'duckTo': 0.14, 'fadeIn': 0.3, 'fadeOut': 0.05},
        ],
        'sfx': [],
        'duckOn': 'captions',
    },
    'overlays': {'grain': 0.04, 'vignette': 0.2, 'fadeIn': 0, 'fadeOut': 0},
}

with open(OUT, 'w') as f:
    json.dump(sb, f, indent=1)

if SHOW_TIMELINE:
    def mmss(t):
        return f'{int(t // 60)}:{t % 60:04.1f}'
    nwords = len(WORDS)
    speech = WORDS[-1]['end'] - WORDS[0]['start']
    print(TIMING)
    print(f'words {nwords}  total {TOTAL:.1f}s  speech {speech:.1f}s  wpm(speech) {nwords / speech * 60:.0f}  wpm(all) {nwords / TOTAL * 60:.0f}')
    for i, (key, text) in enumerate(PARAS):
        w0 = WORDS[PARA_FIRST[i]]
        w1 = [w for w in WORDS if w['para'] == i][-1]
        print(f'P{i + 1:<2} {key:10} {mmss(w0["start"])}-{mmss(w1["end"])} ({w0["start"] / TOTAL * 100:4.1f}%) {len(text.split()):>2}w {w1["end"] - w0["start"]:.1f}s')
    for name, key, needle in (('crack', 'misdirect', 'crack'), ('moray named', 'reveal', 'moray'), ('three', 'reveal', 'three'),
                              ('mouth one', 'rung1', 'one'), ('bitten', 'rung2', 'bitten'), ('Pull', 'pull', 'pull'),
                              ('yanking', 'pull', 'yanking'), ('mouth two', 'fish', 'two'), ('launches', 'launch', 'launches'),
                              ('gone', 'ratchet', 'gone'), ('friendly', 'twist', 'friendly'), ('fingers', 'stinger', 'fingers')):
        t = G(key, needle)
        print(f'  {name:12} {mmss(t)} ({t / TOTAL * 100:4.1f}%)')
