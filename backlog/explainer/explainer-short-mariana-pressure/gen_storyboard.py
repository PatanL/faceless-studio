#!/usr/bin/env python3
"""Generate storyboard.json for explainer-short-mariana-pressure (keep PARAS in sync with script.md).

usage: python3 gen_storyboard.py <out storyboard.json> [--timeline]

Before TTS, word timings are a per-word estimate (Kokoro am_michael, [speed: 1.02] for the hook, rung 1 and
the stakes line, [speed: 1.06] from paragraph 4, [speed: 1.0] for the stinger), calibrated like the box-jellyfish board (CAL 0.885 from the
shipped pressure-ladder voice). After TTS, replace `estimate_words()` with the word list from
episodes/explainer-short-mariana-pressure/audio/captions.json and rerun: every layer is anchored to a word
(`A(scene, word)`), so the whole board retimes itself (producibility must-fix: no fixed-second cuts).

Kit notes
- The depth meter is drawn from core layers on a LOG scale (y ~ log10(1 + d)), so 10 / 30 / 100 / 250 / 1,000 /
  10,935 m are evenly spaced. explainer/DepthMeter is linear (10 m and 100 m would sit 2 px and 17 px below 0 m on
  a 10,935 m ruler); the kit extension `scale: 'log'` + `pins` is logged as a kit gap, and this fallback renders
  today without touching shared kit files.
- The x-ray is two flat svg cards (head, chest) plus separate lung / blood / crack layers animated with layer
  keyframes, not a new component. Heart rate is explainer/ECG with widening beat spacing.
- `whip` is only ever a scene transitionIn (core/schema.ts Transition), never a camera move.
"""
import copy
import json
import math
import re
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else 'storyboard.json'
SHOW_TIMELINE = '--timeline' in sys.argv

# ------------------------------------------------------------------ narration (= script.md narration block)
PARAS = [
    # (scene key, speed, text)
    ('hook', 1.02, 'Hold your breath. Just ten metres down, your ears ache,'),
    ('r10', 1.02, "because the pressure's doubled and squeezed your one breath to half,"),
    ('stakes', 1.02, 'and the floor of the Mariana Trench is still almost eleven kilometres below you.'),
    ('r30', 1.06, "By thirty metres it's a quarter, your heart's slowing, and you're not floating anymore, you're falling,"),
    ('r100', 1.06, 'and at a hundred, your whole breath fits in a water bottle, so blood rushes into your chest to fill the space,'),
    ('r100', 1.06, 'and even trained freedivers can come up from here coughing blood,'),
    ('r250', 1.06, "and by two hundred and fifty metres, you're about as deep as anyone has ever gone on a single breath,"),
    ('r250', 1.06, 'so from here on, pretend you somehow still have air.'),
    ('turn', 1.06, 'Relax. That was the easy part.'),
    ('r1k', 1.06, "One kilometre down, your breath is squeezed into a shot glass, and your ribs can't fold that small,"),
    ('r1k', 1.06, "so something gives, and you still haven't imploded."),
    ('whale', 1.06, 'Sperm whales hunt down here with ribs built to fold.'),
    ('peak', 1.06, "Yours aren't, so by the time you reach the bottom, your whole breath is one teaspoon,"),
    ('everest', 1.06, 'drop Everest in beside you and its peak is still underwater,'),
    ('dead', 1.06, "and you've been extremely not alive since roughly the shot glass,"),
    ('twist', 1.06, 'and yet you never imploded.'),
    ('can', 1.06, 'That only happens to hollow things full of air, like a sealed can,'),
    ('flesh', 1.06, "and you're basically a water balloon, and water barely squeezes, so your flesh is only about four percent smaller."),
    ('sting_q', 1.0, 'And the biggest squeeze on your air?'),
    ('sting_a', 1.0, 'The first ten metres.'),
]
PARA_GAP = 0.32
DIP_GAP = 0.45   # extra breath before the turnstile's dipBlack and the twist
TAIL = 0.35      # hard cut within 1 s of the last word
CAL = 0.885      # calibrated to the shipped am_michael Shorts (pressure-ladder: 250 words = 88.9 s at 0.96)


def estimate_words():
    words, t = [], 0.12
    para_first = []
    for i, (key, speed, text) in enumerate(PARAS):
        if i:
            t += PARA_GAP + (DIP_GAP if key in ('r1k', 'twist') and PARAS[i - 1][0] != key else 0)
        para_first.append(len(words))
        k = 0.96 / speed
        for tok in text.split():
            letters = len(re.sub(r"[^A-Za-z0-9]", '', tok))
            d = (0.13 + 0.043 * letters) * k * CAL
            words.append({'text': tok, 'start': round(t, 3), 'end': round(t + d, 3), 'para': i})
            t += d
            if tok[-1] in ',':
                t += 0.12 * k * CAL
            elif tok[-1] in '.?!:;':
                t += 0.28 * k * CAL
    return words, para_first


WORDS, PARA_FIRST = estimate_words()


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
for i, (key, _, _) in enumerate(PARAS):
    if not SCENES or SCENES[-1]['key'] != key:
        SCENES.append({'key': key, 'paras': [i]})
    else:
        SCENES[-1]['paras'].append(i)
for j, s in enumerate(SCENES):
    s['start'] = 0.0 if j == 0 else WORDS[PARA_FIRST[s['paras'][0]]]['start'] - 0.12
for j, s in enumerate(SCENES):
    s['end'] = SCENES[j + 1]['start'] if j + 1 < len(SCENES) else WORDS[-1]['end'] + TAIL
    s['dur'] = round(s['end'] - s['start'], 3)
SC = {s['key']: s for s in SCENES}
TOTAL = SCENES[-1]['end']


def A(key, needle, nth=1, para_offset=0, end=False):
    s = SC[key]
    return round(word_t(s['paras'][0] + para_offset, needle, nth, end) - s['start'], 3)


def notes(key):
    return ' '.join(PARAS[i][2] for i in SC[key]['paras'])


# ------------------------------------------------------------------ palette + svg assets (all inline, code-drawn)
RED, GREEN, WHITE, CYAN, GREY = '#e5483d', '#3ccf7a', '#ffffff', '#bff3ff', '#8a96a0'
XRAY = '#7fd3e6'

SVG_HEAD = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">'
            '<rect x="6" y="6" width="388" height="388" rx="28" fill="#06202b" stroke="#7fd3e6" stroke-width="4"/>'
            '<circle cx="190" cy="180" r="120" fill="none" stroke="#7fd3e6" stroke-width="10"/>'
            '<path d="M300 200 L360 200" stroke="#7fd3e6" stroke-width="18" stroke-linecap="round"/>'
            '<path d="M296 186 C 330 186 330 214 296 214" fill="none" stroke="#7fd3e6" stroke-width="6"/>'
            '<text x="200" y="370" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="30" fill="#7fd3e6">X-RAY: EAR</text></svg>')
SVG_EARDRUM = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 120">'
               '<path d="M30 4 C 4 40 4 80 30 116" fill="none" stroke="#ffffff" stroke-width="8" stroke-linecap="round"/></svg>')
SVG_CHEST = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 560">'
             '<rect x="6" y="6" width="488" height="548" rx="30" fill="#06202b" stroke="#7fd3e6" stroke-width="4"/>'
             '<path d="M250 40 L250 470" stroke="#7fd3e6" stroke-width="16" stroke-linecap="round"/>'
             + ''.join(f'<path d="M250 {y} C {250 - w} {y - 6} {250 - w - 30} {y + 40} {250 - w + 10} {y + 70}" fill="none" stroke="#7fd3e6" stroke-width="9" stroke-linecap="round"/>'
                       f'<path d="M250 {y} C {250 + w} {y - 6} {250 + w + 30} {y + 40} {250 + w - 10} {y + 70}" fill="none" stroke="#7fd3e6" stroke-width="9" stroke-linecap="round"/>'
                       for y, w in ((90, 120), (140, 150), (190, 165), (240, 170), (290, 165), (340, 150)))
             + '<text x="250" y="530" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="30" fill="#7fd3e6">X-RAY: CHEST</text></svg>')
SVG_LUNG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 220">'
            '<path d="M60 10 C 10 30 4 120 10 200 C 40 214 100 214 110 190 C 116 110 100 30 60 10 Z" fill="#bff3ff" fill-opacity="0.55" stroke="#ffffff" stroke-width="5"/></svg>')
SVG_BLOOD = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 560">'
             '<path d="M250 120 C 140 140 120 300 160 420 M250 120 C 360 140 380 300 340 420 M250 160 L250 440" fill="none" stroke="#e5483d" stroke-width="22" stroke-linecap="round" stroke-opacity="0.85"/>'
             '<ellipse cx="250" cy="290" rx="150" ry="150" fill="#e5483d" fill-opacity="0.28"/></svg>')
SVG_CRACK = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 80">'
             '<path d="M6 40 L36 22 L52 52 L76 18 L92 46 L114 30" fill="none" stroke="#ffffff" stroke-width="7" stroke-linejoin="round"/></svg>')
SVG_BOTTLE = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 240">'
              '<rect x="38" y="4" width="24" height="26" rx="4" fill="#ffffff"/>'
              '<path d="M30 30 L70 30 L80 70 L80 228 Q80 236 72 236 L28 236 Q20 236 20 228 L20 70 Z" fill="#4aa8e8" fill-opacity="0.85" stroke="#ffffff" stroke-width="4"/></svg>')
SVG_SHOT = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 120">'
            '<path d="M10 8 L90 8 L80 112 L20 112 Z" fill="#bff3ff" fill-opacity="0.35" stroke="#ffffff" stroke-width="6" stroke-linejoin="round"/>'
            '<path d="M14 40 L86 40" stroke="#ffffff" stroke-opacity="0.5" stroke-width="3"/></svg>')
SVG_SPOON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 100">'
             '<ellipse cx="70" cy="50" rx="62" ry="38" fill="#d9e2e8" stroke="#ffffff" stroke-width="5"/>'
             '<ellipse cx="70" cy="50" rx="40" ry="20" fill="#bff3ff" fill-opacity="0.8"/>'
             '<path d="M130 50 L292 44" stroke="#d9e2e8" stroke-width="16" stroke-linecap="round"/></svg>')
SVG_CAN = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 260">'
           '<rect x="20" y="20" width="120" height="220" rx="18" fill="#c8d2da" stroke="#ffffff" stroke-width="6"/>'
           '<rect x="20" y="90" width="120" height="70" fill="#e5483d"/>'
           '<text x="80" y="136" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="26" fill="#ffffff">AIR</text></svg>')
SVG_CAN_CRUSHED = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 260">'
                   '<path d="M14 200 L40 176 L60 196 L84 170 L104 194 L126 172 L146 200 L140 240 L20 240 Z" fill="#c8d2da" stroke="#ffffff" stroke-width="6" stroke-linejoin="round"/>'
                   '<path d="M24 214 L136 214" stroke="#e5483d" stroke-width="16"/></svg>')
SVG_TISSUE = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300" overflow="visible">'
              '<rect x="-4" y="-4" width="308" height="308" fill="none" stroke="#ffffff" stroke-width="5" stroke-dasharray="18 12"/>'
              '<rect x="6" y="6" width="288" height="288" rx="10" fill="#f2a7a0" stroke="#ffffff" stroke-width="5"/></svg>')
SVG_BALLOON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 260">'
               '<path d="M100 10 C 30 10 10 90 30 150 C 50 210 90 224 100 226 C 110 224 150 210 170 150 C 190 90 170 10 100 10 Z" fill="#4aa8e8" fill-opacity="0.75" stroke="#ffffff" stroke-width="6"/>'
               '<path d="M92 226 L108 226 L100 244 Z" fill="#ffffff"/></svg>')
# landmarks (visual only, never spoken): ~96 m clock tower at 100 m, 3 stacked 330 m lattice towers at 1 km
SVG_TOWER = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 400">'
             '<path d="M20 400 L20 110 L60 110 L60 400 Z" fill="#0b1a22" stroke="#cfe8ee" stroke-width="4"/>'
             '<circle cx="40" cy="135" r="15" fill="#cfe8ee"/><path d="M14 110 L40 30 L66 110 Z" fill="#0b1a22" stroke="#cfe8ee" stroke-width="4"/></svg>')
SVG_LATTICE = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 360">'
               '<path d="M60 4 L74 120 L112 356 L84 356 L60 230 L36 356 L8 356 L46 120 Z" fill="#0b1a22" stroke="#cfe8ee" stroke-width="4" stroke-linejoin="round"/>'
               '<path d="M38 170 L82 170" stroke="#cfe8ee" stroke-width="4"/></svg>')
# trench cross-section, one svg (V trench, waterline); Everest is a separate layer so it can drop in
TR_W, TR_H = 760, 1040
SVG_TRENCH = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {TR_W} {TR_H}">'
              f'<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2b8197"/><stop offset="0.25" stop-color="#10465a"/><stop offset="1" stop-color="#02080c"/></linearGradient></defs>'
              f'<rect x="0" y="0" width="{TR_W}" height="{TR_H}" fill="url(#w)"/>'
              f'<path d="M0 220 L230 240 L330 {TR_H} L430 {TR_H} L530 240 L{TR_W} 220 L{TR_W} {TR_H} L0 {TR_H} Z" fill="#1a1410" stroke="#5c4a3a" stroke-width="4"/>'
              f'<path d="M0 3 L{TR_W} 3" stroke="#e8f6f8" stroke-width="6"/></svg>')
EVEREST_FRAC = 8849 / 10935  # honest height: 81% of the water column
SVG_EVEREST = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 800" preserveAspectRatio="none">'
               '<path d="M0 800 L200 0 L400 800 Z" fill="#6b6f76" stroke="#ffffff" stroke-width="5"/>'
               '<path d="M150 200 L200 0 L250 200 L224 180 L200 210 L176 180 Z" fill="#ffffff"/></svg>')

# ------------------------------------------------------------------ layer helpers


def comp(name, x, y, w, h, props, **kw):
    l = {'type': 'component', 'name': name, 'x': x, 'y': y, 'width': w, 'height': h, 'props': props}
    l.update(kw)
    return l


def svg(markup, x, y, w, h, **kw):
    l = {'type': 'svg', 'markup': markup, 'x': x, 'y': y, 'width': w, 'height': h}
    l.update(kw)
    return l


def tag(text, x, y, at, out=None, accent=RED, size=32, w=780, **kw):
    p = {'text': text, 'at': at, 'size': size, 'accent': accent, 'align': 'center'}
    if out is not None:
        p['out'] = out
    return comp('explainer/Tag', x, y, w, int(size * 2.6), p, depth=0, z=20, **kw)


def headline(text, at, y='24%', color='white', size=66, out=None, red=None, **kw):
    p = {'text': text, 'at': at, 'size': size, 'color': color, 'underline': True}
    if out is not None:
        p['out'] = out
    if red:
        p['red'] = red
    lines = text.count('\n') + 1
    return comp('explainer/Headline', '55%', y, 900, int(size * 1.6 * lines + 40), p, depth=0, z=20, **kw)


def stat(value, label, at, x='58%', y='30%', size=96, **extra):
    p = {'value': value, 'label': label, 'at': at, 'duration': 0.8, 'size': size}
    p.update(extra)
    return comp('explainer/Stat', x, y, 720, 240, p, depth=0, z=20)


def ocean(depth=0, surface=None, rays=0, snow=60, **extra):
    p = {'depth': depth, 'rays': rays, 'seed': 5, 'snow': snow}
    if surface is not None:
        p['surface'] = surface
    p.update(extra)
    return {'type': 'component', 'name': 'explainer/Ocean', 'depth': 0.12, 'overscan': 1.2, 'props': p}


# ------------------------------------------------------------------ log-scale depth meter (core layers, left edge)
M_X, M_TOP, M_BOT = 112, 300, 1180
LOG_MAX = math.log10(1 + 10935)
PINS = [(10, '10 M', 'x2'), (30, '30 M', 'x4'), (100, '100 M', 'x11'), (250, '250 M', 'x26'),
        (1000, '1 KM', 'x101'), (10935, '10,935 M', 'x1,072')]


def m_y(d):
    return round(M_TOP + (M_BOT - M_TOP) * math.log10(1 + d) / LOG_MAX, 1)


def meter(stamped, arrive=None, from_d=None, to_d=None, t_from=0.0):
    """stamped: depths already stamped red; arrive=(depth, t) stamps a new pin at scene time t.
    The marker moves from from_d (at t_from) to to_d (at the arrive time)."""
    L = [{'type': 'rect', 'x': M_X, 'y': (M_TOP + M_BOT) / 2, 'width': 5, 'height': M_BOT - M_TOP, 'fill': 'rgba(230,245,250,0.5)', 'depth': 0, 'z': 15},
         {'type': 'text', 'text': '0 M', 'x': M_X + 26, 'y': M_TOP, 'anchorX': 0, 'fontSize': 24, 'color': 'rgba(230,245,250,0.7)', 'depth': 0, 'z': 15}]
    for d, label, mult in PINS:
        y = m_y(d)
        done = d in stamped
        new = arrive is not None and arrive[0] == d
        L.append({'type': 'circle', 'x': M_X, 'y': y, 'width': 24, 'height': 24, 'fill': RED if done else '#56646d', 'stroke': WHITE, 'strokeWidth': 3, 'depth': 0, 'z': 16})
        L.append({'type': 'text', 'text': label, 'x': M_X + 26, 'y': y, 'anchorX': 0, 'fontSize': 26, 'color': WHITE if done else 'rgba(230,245,250,0.6)', 'depth': 0, 'z': 16})
        if done:
            L.append({'type': 'text', 'text': mult, 'x': M_X + 26, 'y': y + 30, 'anchorX': 0, 'fontSize': 24, 'color': RED, 'depth': 0, 'z': 16})
        if new:
            t = arrive[1]
            L.append({'type': 'circle', 'x': M_X, 'y': y, 'width': 24, 'height': 24, 'fill': RED, 'stroke': WHITE, 'strokeWidth': 3, 'depth': 0, 'z': 17,
                      'start': t, 'enter': {'type': 'pop', 'at': t, 'duration': 0.25}})
            L.append({'type': 'text', 'text': mult, 'x': M_X + 26, 'y': y + 30, 'anchorX': 0, 'fontSize': 30, 'color': RED, 'depth': 0, 'z': 17,
                      'start': t, 'enter': {'type': 'pop', 'at': t, 'duration': 0.25}})
    if from_d is not None:
        kf = [{'t': t_from, 'y': m_y(from_d)}]
        if arrive is not None and to_d is not None:
            kf.append({'t': arrive[1], 'y': m_y(to_d), 'ease': 'out'})
        L.append({'type': 'circle', 'x': M_X, 'y': m_y(from_d), 'width': 40, 'height': 40, 'fill': 'rgba(0,0,0,0)', 'stroke': RED, 'strokeWidth': 6,
                  'depth': 0, 'z': 18, 'keyframes': kf})
    return L


def bubble(pct, x='60%', y='44%', base=300, at=None, from_pct=None, label=True, ly='55%', **kw):
    """Breath bubble: area ~ air volume, so diameter ~ sqrt(pct). Optional shrink from from_pct at `at`."""
    d1 = max(18, base * math.sqrt(pct / 100))
    out = []
    if from_pct is not None and at is not None:
        d0 = max(18, base * math.sqrt(from_pct / 100))
        s0 = d0 / d1
        out.append({'type': 'circle', 'x': x, 'y': y, 'width': round(d1), 'height': round(d1), 'fill': 'rgba(191,243,255,0.28)', 'stroke': WHITE, 'strokeWidth': 5,
                    'depth': 0, 'z': 12, 'keyframes': [{'t': 0, 'scale': s0}, {'t': at, 'scale': s0}, {'t': at + 0.5, 'scale': 1, 'ease': 'out'}], **kw})
    else:
        out.append({'type': 'circle', 'x': x, 'y': y, 'width': round(d1), 'height': round(d1), 'fill': 'rgba(191,243,255,0.28)', 'stroke': WHITE, 'strokeWidth': 5,
                    'depth': 0, 'z': 12, **kw})
    return out


scenes = []
DONE = []  # stamped pins so far

# ---------------------------------------------------------------- s01 hook (frame 0 = the stinger's last frame)
SURFACE = ocean(depth=0, surface=0.22, rays=7, snow=30)


def hook_static_layers():
    """Frame-0 layout, reused verbatim (no motion) as the stinger's last frame so the loop is seamless."""
    return [
        comp('explainer/You', '60%', 450, 170, 290, {'pose': 'stand'}, id='you', idle=[{'type': 'bob', 'amount': 5, 'speed': 0.5}]),
        {'type': 'circle', 'id': 'breath', 'x': '80%', 'y': 380, 'width': 150, 'height': 150, 'fill': 'rgba(191,243,255,0.28)', 'stroke': WHITE, 'strokeWidth': 5, 'depth': 0, 'z': 12},
        {'type': 'text', 'id': 'breathlabel', 'text': 'YOUR AIR\n100%', 'x': '80%', 'y': 380, 'fontSize': 30, 'color': WHITE, 'depth': 0, 'z': 13},
        tag('THOUGHT EXPERIMENT: 1 BREATH, NO GEAR', '58%', 300, 0, size=26, w=760, accent='#ffffff'),
        {'type': 'particles', 'preset': 'bubbles', 'count': 12, 'x': '60%', 'y': '45%', 'width': 700, 'height': 700, 'opacity': 0.5, 'seed': 7, 'depth': 0.6},
    ] + meter([], from_d=0)


h = SC['hook']
t_ten = A('hook', 'ten')
t_ears = A('hook', 'ears')
hook_layers = hook_static_layers()
for l in hook_layers:
    if l.get('id') == 'you':
        # tips head-down after "breath", sinks to the 10 m line
        l['keyframes'] = [{'t': 0, 'y': 450, 'rotate': 0}, {'t': A('hook', 'breath', end=True), 'y': 450, 'rotate': 0}, {'t': A('hook', 'just'), 'y': 470, 'rotate': 180, 'ease': 'inOut'},
                          {'t': h['dur'], 'y': 900, 'rotate': 180, 'ease': 'in'}]
hook_layers = [l for l in hook_layers if l.get('type') != 'circle' or l.get('stroke') != RED]  # replace static marker
hook_layers += [
    {'type': 'circle', 'x': M_X, 'y': m_y(0), 'width': 40, 'height': 40, 'fill': 'rgba(0,0,0,0)', 'stroke': RED, 'strokeWidth': 6, 'depth': 0, 'z': 18,
     'keyframes': [{'t': 0, 'y': m_y(0)}, {'t': A('hook', 'just'), 'y': m_y(0)}, {'t': t_ten + 0.4, 'y': m_y(10), 'ease': 'out'}]},
    {'type': 'rect', 'x': M_X + 50, 'y': (m_y(0) + m_y(10)) / 2, 'width': 6, 'height': m_y(10) - m_y(0), 'fill': RED, 'depth': 0, 'z': 15,
     'start': t_ten, 'enter': {'type': 'wipeDown', 'at': t_ten, 'duration': 0.35}},
    tag('JUST 10 M', '34%', m_y(10) - 120, t_ten, size=30, w=300),
    svg(SVG_HEAD, '66%', 1060, 330, 330, start=t_ears, enter={'type': 'pop', 'at': t_ears, 'duration': 0.25}, depth=0, z=14),
    svg(SVG_EARDRUM, '76.5%', 1068, 30, 90, start=t_ears, depth=0, z=15,
        keyframes=[{'t': t_ears, 'scaleX': 0.4}, {'t': h['dur'], 'scaleX': 1.4, 'ease': 'out'}]),
    tag('EARS ACHE', '66%', 1260, t_ears + 0.15, size=28, w=320),
]
scenes.append({
    'id': 's01_hook', 'duration': h['dur'], 'background': SURFACE,
    'layers': hook_layers,
    'camera': {'keyframes': [{'t': 0, 'zoom': 1.0}, {'t': h['dur'], 'zoom': 1.04, 'ease': 'inOut'}]},
    'sfx': [{'cue': 'breath', 'at': 0.05, 'volume': 0.6}, {'cue': 'bubbles', 'at': A('hook', 'just'), 'volume': 0.5}],
    'notes': notes('hook'),
})

# ---------------------------------------------------------------- s02 rung 1: 10 m, x2, breath halves (no sky comparison: that is pressure-ladder's hook)
s = SC['r10']
t_dbl, t_half = A('r10', 'doubled'), A('r10', 'half')
DONE_10 = [10]
scenes.append({
    'id': 's02_r10', 'duration': s['dur'], 'background': ocean(depth=10, rays=6, snow=40),
    'layers': meter([], arrive=(10, t_dbl), from_d=10) + [
        comp('explainer/You', '40%', 640, 150, 255, {'pose': 'stand'}, rotate=180, idle=[{'type': 'bob', 'amount': 4, 'speed': 0.5}]),
        *bubble(50, x='66%', y=600, base=360, at=t_half - 0.2, from_pct=100),
        {'type': 'text', 'text': 'YOUR AIR', 'x': '66%', 'y': 800, 'fontSize': 30, 'color': WHITE, 'depth': 0, 'z': 13},
        headline('HALF', t_half, y='62%', color='red', size=96),
        stat(2, 'THE PRESSURE', t_dbl, x='58%', y=340, size=84, prefix='x'),
            ],
    'camera': {'preset': 'pushIn', 'amount': 0.3},
    'sfx': [{'cue': 'click', 'at': t_dbl, 'volume': 0.8}, {'cue': 'pop', 'at': t_half - 0.2, 'volume': 0.6}],
    'notes': notes('r10'),
})

# ---------------------------------------------------------------- s03 stakes: the whole column, endpoint + implode contract
s = SC['stakes']
t_el, t_mar = A('stakes', 'eleven'), A('stakes', 'mariana')
TR_X, TR_Y = 600, 760   # centre of the trench svg
TR_TOP = TR_Y - TR_H / 2
scenes.append({
    'id': 's03_stakes', 'duration': s['dur'], 'background': {'type': 'color', 'color': '#02080c'},
    'transitionIn': {'type': 'whip', 'duration': 0.3, 'direction': 'up'},
    'layers': meter(DONE_10, from_d=10) + [
        svg(SVG_TRENCH, TR_X, TR_Y, TR_W, TR_H, depth=0, z=5),
        {'type': 'circle', 'x': TR_X, 'y': TR_TOP + 12, 'width': 18, 'height': 18, 'fill': WHITE, 'depth': 0, 'z': 8, 'idle': [{'type': 'pulse', 'amount': 0.3, 'speed': 1.5}]},
        tag('YOU (10 M)', TR_X + 170, TR_TOP + 40, 0.1, size=24, w=260, accent='#ffffff'),
        headline('MARIANA TRENCH', t_mar, y='14%', size=60),
        stat(10935, 'METRES TO THE FLOOR', t_el, x=TR_X, y=TR_TOP + 560, size=96, suffix=' M'),
        tag("EVERYONE SAYS YOU'D IMPLODE...", TR_X, TR_TOP + 780, A('stakes', 'below'), size=30, w=700),
    ],
    'camera': {'keyframes': [{'t': 0, 'zoom': 1.15, 'y': '30%'}, {'t': s['dur'], 'zoom': 1.0, 'y': '50%', 'ease': 'out'}]},
    'sfx': [{'cue': 'whoosh_long', 'at': 0.05, 'volume': 0.6}, {'cue': 'tick', 'at': t_el, 'volume': 0.5}],
    'notes': notes('stakes'),
})

# ---------------------------------------------------------------- s04 rung 2: 30 m, x4, a quarter, heart slows, freefall
s = SC['r30']
t_30, t_q, t_heart, t_fall = A('r30', 'thirty'), A('r30', 'quarter'), A('r30', "heart's"), A('r30', 'falling')
d = s['dur']
beats = [round(0.2 + sum(0.55 + 0.09 * k for k in range(i)), 2) for i in range(12)]
beats = [b for b in beats if b < d]
scenes.append({
    'id': 's04_r30', 'duration': d, 'background': ocean(depth=30, rays=4, snow=50),
    'layers': meter(DONE_10, arrive=(30, t_30), from_d=10, to_d=30) + [
        comp('explainer/You', '42%', 560, 150, 255, {'pose': 'stand'}, rotate=180,
             keyframes=[{'t': 0, 'y': 540}, {'t': t_fall, 'y': 600}, {'t': d, 'y': 860, 'ease': 'in'}]),
        *bubble(25, x='70%', y=560, base=360, at=t_q - 0.1, from_pct=50),
        {'type': 'text', 'text': '25%', 'x': '70%', 'y': 560, 'fontSize': 40, 'color': WHITE, 'depth': 0, 'z': 13, 'start': t_q},
        tag('A QUARTER', '70%', 700, t_q, size=30, w=320),
        comp('explainer/ECG', '58%', 1000, 760, 180, {'beats': beats, 'at': t_heart - 0.4, 'prefill': True, 'color': RED}, depth=0, z=10, start=t_heart - 0.4),
        tag('HEART SLOWING (DIVE REFLEX)', '58%', 1130, t_heart, size=26, w=620, accent='#ffffff'),
        tag('NOT FLOATING. FALLING.', '58%', 360, t_fall, size=32, w=560),
        {'type': 'particles', 'preset': 'bubbles', 'count': 18, 'x': '42%', 'y': '28%', 'width': 300, 'height': 400, 'start': t_fall, 'seed': 3, 'speed': 1.6},
    ],
    'camera': {'preset': 'panDown', 'amount': 0.4},
    'sfx': [{'cue': 'click', 'at': t_30, 'volume': 0.7}, {'cue': 'heartbeat_slow', 'at': t_heart, 'volume': 0.7}, {'cue': 'whoosh', 'at': t_fall, 'volume': 0.5}],
    'notes': notes('r30'),
})

# ---------------------------------------------------------------- s05 rung 3: 100 m, x11, a water bottle, blood shift, lung squeeze
s = SC['r100']
DONE_30 = [10, 30]
t_100, t_bottle, t_blood, t_chest = A('r100', 'hundred'), A('r100', 'bottle'), A('r100', 'blood'), A('r100', 'chest')
t_free, t_cough = A('r100', 'trained', para_offset=1), A('r100', 'coughing', para_offset=1)
CH_X, CH_Y = 640, 860
scenes.append({
    'id': 's05_r100', 'duration': s['dur'], 'background': ocean(depth=100, rays=2, snow=70),
    'layers': meter(DONE_30, arrive=(100, t_100), from_d=30, to_d=100) + [
        # visual-only landmark: a ~96 m clock tower next to YOU, gone when the x-ray opens
        svg(SVG_TOWER, '40%', 880, 110, 550, end=t_blood, opacity=0.9),
        tag('~96 M CLOCK TOWER', '44%', 1200, 0.3, out=t_blood, size=22, w=320, accent='#ffffff'),
        comp('explainer/You', '52%', 1080, 50, 85, {'pose': 'stand'}, rotate=180, end=t_blood),
        *bubble(9, x='62%', y=520, base=360, at=t_bottle - 0.3, from_pct=25, end=t_blood),
        svg(SVG_BOTTLE, '80%', 520, 80, 192, start=t_bottle - 0.3, end=t_blood, enter={'type': 'pop', 'at': t_bottle - 0.3, 'duration': 0.25}),
        tag('YOUR BREATH ~0.5 L', '70%', 680, t_bottle, out=t_blood, size=28, w=420),
        # chest card
        svg(SVG_CHEST, CH_X, CH_Y, 500, 560, start=t_blood, enter={'type': 'zoomIn', 'at': t_blood, 'duration': 0.3}, depth=0, z=10),
        svg(SVG_LUNG, CH_X - 70, CH_Y - 10, 120, 220, start=t_blood, depth=0, z=11,
            keyframes=[{'t': t_blood, 'scale': 0.55}, {'t': t_chest + 0.6, 'scale': 0.32, 'ease': 'out'}]),
        svg(SVG_LUNG, CH_X + 70, CH_Y - 10, 120, 220, flipX=True, start=t_blood, depth=0, z=11,
            keyframes=[{'t': t_blood, 'scale': 0.55}, {'t': t_chest + 0.6, 'scale': 0.32, 'ease': 'out'}]),
        svg(SVG_BLOOD, CH_X, CH_Y, 500, 560, start=t_blood, depth=0, z=12,
            keyframes=[{'t': t_blood, 'opacity': 0}, {'t': t_chest + 0.8, 'opacity': 0.9}]),
        tag('BLOOD SHIFT', CH_X, CH_Y - 330, t_chest, size=32, w=360),
        tag('TRAINED FREEDIVERS', CH_X, 1220, t_free, size=28, w=480, accent='#ffffff'),
        tag('LUNG SQUEEZE', CH_X, 1290, t_cough, size=30, w=360),
    ],
    'camera': {'keyframes': [{'t': 0, 'zoom': 1.0}, {'t': t_blood, 'zoom': 1.05}, {'t': s['dur'], 'zoom': 1.12, 'ease': 'out'}],
               'shake': [{'at': t_cough, 'duration': 0.3, 'amplitude': 8}]},
    'sfx': [{'cue': 'click', 'at': t_100, 'volume': 0.7}, {'cue': 'sonar_ping', 'at': t_100 + 0.2, 'volume': 0.4}, {'cue': 'pop', 'at': t_bottle, 'volume': 0.5},
            {'cue': 'heartbeat_slow', 'at': t_blood, 'volume': 0.7}],
    'notes': notes('r100'),
})

# ---------------------------------------------------------------- s06 rung 4: 250 m, the one-breath record + the "somehow" hedge
s = SC['r250']
DONE_100 = [10, 30, 100]
t_250, t_record, t_pretend = A('r250', 'two'), A('r250', 'deep'), A('r250', 'pretend', para_offset=1)
scenes.append({
    'id': 's06_r250', 'duration': s['dur'], 'background': ocean(depth=250, rays=0, snow=90),
    'layers': meter(DONE_100, arrive=(250, t_250 + 0.4), from_d=100, to_d=250) + [
        comp('explainer/You', '58%', 640, 150, 255, {'pose': 'stand'}, rotate=180),
        *bubble(4, x='76%', y=520, base=360),
        {'type': 'text', 'text': '4%', 'x': '76%', 'y': 470, 'fontSize': 30, 'color': WHITE, 'depth': 0, 'z': 13},
        {'type': 'rect', 'x': '58%', 'y': 900, 'width': 760, 'height': 6, 'fill': GREEN, 'depth': 0, 'z': 9, 'start': t_record,
         'enter': {'type': 'wipeRight', 'at': t_record, 'duration': 0.4}},
        tag('DEEPEST BREATH-HOLD DIVE: ~253 M (2012)', '58%', 960, t_record, size=26, w=760, accent=GREEN),
        tag('HUMANS STOP HERE', '58%', 840, A('r250', 'single'), size=28, w=420, accent='#ffffff'),
        headline('PRETEND YOU\nSTILL HAVE AIR', t_pretend, y='22%', size=58),
        comp('explainer/You', '58%', 640, 150, 255, {'pose': 'shrug'}, start=t_pretend),
    ],
    'camera': {'preset': 'drift', 'amount': 0.4},
    'sfx': [{'cue': 'click', 'at': t_250 + 0.4, 'volume': 0.7}, {'cue': 'ding', 'at': t_record + 0.3, 'volume': 0.5}],
    'notes': notes('r250'),
})
# the shrug layer replaces the standing one from "pretend"
scenes[-1]['layers'][len(meter(DONE_100, arrive=(250, 0), from_d=100, to_d=250))]['end'] = t_pretend

# ---------------------------------------------------------------- s07 turnstile (~48%): ironic reassurance, black on the next word
s = SC['turn']
DONE_250 = [10, 30, 100, 250]
scenes.append({
    'id': 's07_turnstile', 'duration': s['dur'], 'background': ocean(depth=250, rays=0, snow=90),
    'layers': meter(DONE_250, from_d=250) + [
        comp('explainer/You', '58%', 860, 170, 290, {'pose': 'shrug'}),
        headline('THAT WAS\nTHE EASY PART', A('turn', 'that'), y='26%', size=70),
    ],
    'camera': {'preset': 'pushIn', 'amount': 0.4},
    'sfx': [{'cue': 'stinger', 'at': A('turn', 'easy'), 'volume': 0.7}],
    'notes': notes('turn'),
})

# ---------------------------------------------------------------- s08 rung 5: 1 km, x101, shot glass, ribs, "something gives", implode planted
s = SC['r1k']
t_1k, t_shot, t_ribs = A('r1k', 'one'), A('r1k', 'shot'), A('r1k', 'ribs')
t_gives, t_impl = A('r1k', 'gives', para_offset=1), A('r1k', 'imploded', para_offset=1)
CH2_X, CH2_Y = 620, 900
scenes.append({
    'id': 's08_r1k', 'duration': s['dur'], 'background': ocean(depth=1000, rays=0, snow=120),
    'transitionIn': {'type': 'dipBlack', 'duration': 0.4},
    'layers': meter(DONE_250, arrive=(1000, t_1k + 0.3), from_d=250, to_d=1000) + [
        # visual-only landmark: three stacked ~330 m lattice towers = ~1 km, before the x-ray
        svg(SVG_LATTICE, '40%', 1180, 90, 270, end=t_ribs, opacity=0.85),
        svg(SVG_LATTICE, '40%', 910, 90, 270, end=t_ribs, opacity=0.85),
        svg(SVG_LATTICE, '40%', 640, 90, 270, end=t_ribs, opacity=0.85),
        tag('~3 EIFFEL TOWERS', '42%', 470, 0.3, out=t_ribs, size=22, w=320, accent='#ffffff'),
        *bubble(1, x='70%', y=640, base=360, at=t_shot - 0.3, from_pct=4, end=t_ribs),
        svg(SVG_SHOT, '70%', 820, 100, 120, start=t_shot - 0.2, end=t_ribs, enter={'type': 'pop', 'at': t_shot - 0.2, 'duration': 0.25}),
        tag('YOUR BREATH ~60 ML', '70%', 940, t_shot, out=t_ribs, size=26, w=380),
        # chest card again: lungs a sliver, ribs, crack on "gives"
        svg(SVG_CHEST, CH2_X, CH2_Y, 500, 560, start=t_ribs, enter={'type': 'zoomIn', 'at': t_ribs, 'duration': 0.3}, depth=0, z=10),
        svg(SVG_LUNG, CH2_X - 70, CH2_Y - 10, 120, 220, start=t_ribs, depth=0, z=11, keyframes=[{'t': t_ribs, 'scale': 0.3}, {'t': t_gives, 'scale': 0.1, 'ease': 'out'}]),
        svg(SVG_LUNG, CH2_X + 70, CH2_Y - 10, 120, 220, flipX=True, start=t_ribs, depth=0, z=11, keyframes=[{'t': t_ribs, 'scale': 0.3}, {'t': t_gives, 'scale': 0.1, 'ease': 'out'}]),
        svg(SVG_BLOOD, CH2_X, CH2_Y, 500, 560, start=t_ribs, opacity=0.9, depth=0, z=12),
        svg(SVG_CRACK, CH2_X + 120, CH2_Y - 60, 120, 80, start=t_gives, enter={'type': 'pop', 'at': t_gives, 'duration': 0.12}, depth=0, z=13),
        tag('SOMETHING GIVES', CH2_X, CH2_Y - 330, t_gives, size=34, w=440),
        tag("STILL NOT IMPLODED", CH2_X, CH2_Y + 330, t_impl, size=30, w=440, accent='#ffffff'),
    ],
    'camera': {'preset': 'pushIn', 'amount': 0.3, 'shake': [{'at': t_gives, 'duration': 0.35, 'amplitude': 14}]},
    'sfx': [{'cue': 'boom', 'at': t_1k + 0.3, 'volume': 0.7}, {'cue': 'pop', 'at': t_shot, 'volume': 0.5}, {'cue': 'impact', 'at': t_gives, 'volume': 0.8}],
    'notes': notes('r1k'),
})

# ---------------------------------------------------------------- s09 sperm whale: you-vs-it, ribs built to fold
s = SC['whale']
DONE_1K = [10, 30, 100, 250, 1000]
t_fold = A('whale', 'fold')
scenes.append({
    'id': 's09_whale', 'duration': s['dur'], 'background': ocean(depth=1000, rays=0, snow=120),
    'layers': meter(DONE_1K, from_d=1000) + [
        comp('explainer/SpermWhale', '60%', 640, 900, 300, {}, keyframes=[{'t': 0, 'x': '95%'}, {'t': s['dur'], 'x': '50%', 'ease': 'linear'}]),
        comp('explainer/You', '62%', 980, 70, 120, {'pose': 'stand'}, rotate=180),
        tag('RIBS BUILT TO FOLD  ✓', '60%', 820, t_fold, size=30, w=520, accent=GREEN),
    ],
    'camera': {'preset': 'drift', 'amount': 0.5},
    'sfx': [{'cue': 'sonar_ping', 'at': 0.2, 'volume': 0.6}, {'cue': 'sonar_ping', 'at': 0.9, 'volume': 0.5}],
    'notes': notes('whale'),
})

# ---------------------------------------------------------------- s10 peak: the bottom, x1,072, a teaspoon (tonne/cm2 on screen only)
s = SC['peak']
t_yours, t_bottom, t_spoon = A('peak', 'yours'), A('peak', 'bottom'), A('peak', 'teaspoon')
scenes.append({
    'id': 's10_peak', 'duration': s['dur'], 'background': ocean(depth=10935, rays=0, snow=40),
    'transitionIn': {'type': 'whip', 'duration': 0.3, 'direction': 'down'},
    'layers': meter(DONE_1K, arrive=(10935, t_bottom + 0.2), from_d=1000, to_d=10935) + [
        headline("YOURS AREN'T", t_yours, y='16%', color='red', size=70, out=t_bottom),
        {'type': 'rect', 'x': '58%', 'y': 1240, 'width': 900, 'height': 120, 'fill': '#1a1410', 'depth': 0, 'z': 4},
        comp('explainer/You', '58%', 1090, 110, 190, {'pose': 'stand'}, rotate=180,
             keyframes=[{'t': 0, 'y': 400}, {'t': t_bottom + 0.2, 'y': 1090, 'ease': 'in'}]),
        stat(1.1, 'TONNES ON EVERY CM²', t_bottom + 0.3, x='58%', y='22%', size=84, prefix='~', decimals=1),
        tag('x1,072 THE SURFACE PRESSURE', '58%', 610, t_bottom + 0.5, size=26, w=600, accent='#ffffff'),
        svg(SVG_SPOON, '58%', 800, 300, 100, start=t_spoon - 0.2, enter={'type': 'pop', 'at': t_spoon - 0.2, 'duration': 0.25}),
        tag('YOUR WHOLE BREATH: ~5 ML', '58%', 900, t_spoon, size=30, w=560),
    ],
    'camera': {'keyframes': [{'t': 0, 'zoom': 1.0}, {'t': t_bottom + 0.2, 'zoom': 1.0}, {'t': s['dur'], 'zoom': 1.08, 'ease': 'out'}],
               'shake': [{'at': t_bottom + 0.2, 'duration': 0.4, 'amplitude': 16}]},
    'sfx': [{'cue': 'glitch', 'at': t_yours, 'volume': 0.4}, {'cue': 'boom', 'at': t_bottom + 0.2, 'volume': 0.9}, {'cue': 'pop', 'at': t_spoon, 'volume': 0.5}],
    'notes': notes('peak'),
})

# ---------------------------------------------------------------- s11 Everest dropped into the trench beside you (the biggest landmark, spent here)
s = SC['everest']
DONE_ALL = [10, 30, 100, 250, 1000, 10935]
t_ev = A('everest', 'everest')
EV_H = round((TR_H - 6) * EVEREST_FRAC)
EV_Y = TR_TOP + TR_H - EV_H / 2
scenes.append({
    'id': 's11_everest', 'duration': s['dur'], 'background': {'type': 'color', 'color': '#02080c'},
    'layers': meter(DONE_ALL, from_d=10935) + [
        svg(SVG_TRENCH, TR_X, TR_Y, TR_W, TR_H, depth=0, z=5),
        svg(SVG_EVEREST, TR_X - 30, EV_Y, 200, EV_H, depth=0, z=6, start=t_ev,
            keyframes=[{'t': t_ev, 'y': EV_Y - EV_H}, {'t': t_ev + 0.45, 'y': EV_Y, 'ease': 'in'}]),
        {'type': 'circle', 'x': TR_X + 70, 'y': TR_TOP + TR_H - 14, 'width': 16, 'height': 16, 'fill': WHITE, 'depth': 0, 'z': 8},
        tag('YOU', TR_X + 140, TR_TOP + TR_H - 40, 0.1, size=22, w=120, accent='#ffffff'),
        tag('EVEREST 8,849 M', TR_X + 140, EV_Y, t_ev + 0.45, size=24, w=320, accent='#ffffff'),
        {'type': 'rect', 'x': TR_X - 30, 'y': TR_TOP + (TR_H - EV_H) / 2, 'width': 6, 'height': TR_H - EV_H - 12, 'fill': RED, 'depth': 0, 'z': 7,
         'start': t_ev + 0.6, 'enter': {'type': 'wipeDown', 'at': t_ev + 0.6, 'duration': 0.3}},
        tag('~2 KM OF WATER ABOVE THE PEAK', TR_X + 60, TR_TOP + (TR_H - EV_H) / 2, t_ev + 0.6, size=24, w=520),
    ],
    'camera': {'preset': 'none', 'shake': [{'at': t_ev + 0.45, 'duration': 0.35, 'amplitude': 12}]},
    'sfx': [{'cue': 'whoosh', 'at': t_ev, 'volume': 0.6}, {'cue': 'impact', 'at': t_ev + 0.45, 'volume': 0.8}],
    'notes': notes('everest'),
})

# ---------------------------------------------------------------- s12 the death beat as a deflation (at the peak, about you)
s = SC['dead']
t_ext, t_shotglass = A('dead', 'extremely'), A('dead', 'shot')
scenes.append({
    'id': 's12_dead', 'duration': s['dur'], 'background': ocean(depth=10935, rays=0, snow=40),
    'layers': meter(DONE_ALL, from_d=10935) + [
        {'type': 'rect', 'x': '58%', 'y': 1240, 'width': 900, 'height': 120, 'fill': '#1a1410', 'depth': 0, 'z': 4},
        comp('explainer/You', '58%', 1130, 110, 190, {'pose': 'stand', 'silhouette': GREY, 'idle': False},
             keyframes=[{'t': 0, 'rotate': 180, 'y': 1090}, {'t': t_ext, 'rotate': 270, 'y': 1150, 'ease': 'out'}]),
        tag('STATUS: EXTREMELY NOT ALIVE', '58%', 820, t_ext, size=32, w=640),
        tag('(SINCE ~1 KM)', '58%', 900, t_shotglass, size=26, w=320, accent='#ffffff'),
    ],
    'camera': {'preset': 'pushIn', 'amount': 0.3},
    'sfx': [{'cue': 'ding', 'at': t_shotglass, 'volume': 0.5}],
    'notes': notes('dead'),
})

# ---------------------------------------------------------------- s13 twist title: the implode myth busted (pays off 0:0x tag + the 1 km plant)
s = SC['twist']
t_never, t_imp = A('twist', 'never'), A('twist', 'imploded')
scenes.append({
    'id': 's13_twist', 'duration': s['dur'], 'background': {'type': 'color', 'color': '#04121a'},
    'transitionIn': {'type': 'whip', 'duration': 0.3, 'direction': 'left'},
    'layers': [
        {'type': 'text', 'text': 'YOU NEVER IMPLODED', 'x': '50%', 'y': '36%', 'fontSize': 84, 'color': WHITE, 'depth': 0, 'z': 20, 'maxWidth': 820,
         'enter': {'type': 'pop', 'at': 0.05, 'duration': 0.25}},
        tag("'YOU'D IMPLODE'", '50%', '24%', 0.05, size=34, w=480, accent='#ffffff'),
        {'type': 'rect', 'x': '50%', 'y': '24%', 'width': 440, 'height': 8, 'fill': RED, 'depth': 0, 'z': 21, 'start': t_never,
         'enter': {'type': 'wipeRight', 'at': t_never, 'duration': 0.3}},
        tag('MYTH', '50%', '48%', t_imp, size=40, w=240),
    ],
    'camera': {'preset': 'pushIn', 'amount': 0.4},
    'sfx': [{'cue': 'riser', 'at': 0.0, 'volume': 0.4}, {'cue': 'glitch', 'at': t_never, 'volume': 0.5}],
    'notes': notes('twist'),
})

# ---------------------------------------------------------------- s14 sealed can (2 pre-drawn paths, swap on "can")
s = SC['can']
t_hollow, t_can = A('can', 'hollow'), A('can', 'can')
scenes.append({
    'id': 's14_can', 'duration': s['dur'], 'background': ocean(depth=10935, rays=0, snow=40),
    'layers': [
        svg(SVG_CAN, '50%', 820, 240, 390, end=t_can + 0.15),
        svg(SVG_CAN_CRUSHED, '50%', 820, 240, 390, start=t_can + 0.15),
        tag('HOLLOW + AIR', '50%', 560, t_hollow, size=34, w=420),
        tag('= IMPLODES', '50%', 1080, t_can + 0.2, size=34, w=360),
    ],
    'camera': {'preset': 'none', 'shake': [{'at': t_can + 0.15, 'duration': 0.3, 'amplitude': 14}]},
    'sfx': [{'cue': 'impact', 'at': t_can + 0.15, 'volume': 0.9}],
    'notes': notes('can'),
})

# ---------------------------------------------------------------- s15 water balloon + tissue block (-4% is flesh, not the whole YOU)
s = SC['flesh']
t_ball, t_water, t_flesh, t_four = A('flesh', 'balloon'), A('flesh', 'water', nth=2), A('flesh', 'flesh'), A('flesh', 'four')
scenes.append({
    'id': 's15_flesh', 'duration': s['dur'], 'background': ocean(depth=10935, rays=0, snow=40),
    'layers': [
        comp('explainer/You', '36%', 760, 170, 290, {'pose': 'stand', 'silhouette': GREY, 'idle': False}, end=t_flesh),
        svg(SVG_BALLOON, '66%', 760, 200, 260, start=t_ball, end=t_flesh, enter={'type': 'pop', 'at': t_ball, 'duration': 0.25}),
        tag('= WATER BALLOON', '58%', 1000, t_ball, out=t_flesh, size=30, w=460),
        tag('WATER BARELY SQUEEZES', '50%', 420, t_water, size=30, w=560, accent='#ffffff'),
        svg(SVG_TISSUE, '50%', 800, 300, 300, start=t_flesh, enter={'type': 'zoomIn', 'at': t_flesh, 'duration': 0.3},
            keyframes=[{'t': t_flesh, 'scale': 1.0}, {'t': t_four + 0.5, 'scale': 0.987, 'ease': 'out'}]),
        tag('YOUR FLESH', '50%', 610, t_flesh, size=28, w=320, accent='#ffffff'),
        stat(-4, 'SMALLER', t_four, x='50%', y=1080, size=96, suffix='%'),
    ],
    'camera': {'preset': 'pushIn', 'amount': 0.3},
    'sfx': [{'cue': 'pop', 'at': t_ball, 'volume': 0.5}, {'cue': 'tick', 'at': t_four, 'volume': 0.5}],
    'notes': notes('flesh'),
})

# ---------------------------------------------------------------- s16 stinger question: where the air went (it is about air volume)
s = SC['sting_q']
t_air = A('sting_q', 'air')
BAR_Y = 900
scenes.append({
    'id': 's16_sting_q', 'duration': s['dur'], 'background': {'type': 'color', 'color': '#04121a'},
    'transitionIn': {'type': 'whip', 'duration': 0.3, 'direction': 'up'},
    'layers': [
        headline('YOUR AIR', 0.05, y='20%', size=70),
        {'type': 'rect', 'x': 300 + 240, 'y': BAR_Y, 'width': 480, 'height': 70, 'fill': RED, 'anchorX': 0.5, 'depth': 0, 'z': 10,
         'enter': {'type': 'wipeRight', 'at': 0.1, 'duration': 0.35}},
        {'type': 'text', 'text': 'LOST IN THE FIRST 10 M: 50%', 'x': '50%', 'y': BAR_Y - 80, 'fontSize': 34, 'color': WHITE, 'depth': 0, 'z': 11, 'start': 0.1},
        {'type': 'rect', 'x': 540, 'y': BAR_Y + 200, 'width': 480, 'height': 70, 'fill': '#56646d', 'depth': 0, 'z': 10, 'start': t_air,
         'enter': {'type': 'wipeRight', 'at': t_air, 'duration': 0.35}},
        {'type': 'text', 'text': 'LOST IN THE NEXT 10,925 M: ~50%', 'x': '50%', 'y': BAR_Y + 120, 'fontSize': 34, 'color': WHITE, 'depth': 0, 'z': 11, 'start': t_air},
        tag('LEFT AT THE BOTTOM: ~0.09%', '50%', BAR_Y + 320, t_air + 0.2, size=26, w=560, accent='#ffffff'),
    ],
    'camera': {'preset': 'none'},
    'sfx': [{'cue': 'whoosh_long', 'at': 0.0, 'volume': 0.6}],
    'notes': notes('sting_q'),
})

# ---------------------------------------------------------------- s17 stinger answer: frame-0 layout verbatim (no motion), cut on "metres"
s = SC['sting_a']
t_first = A('sting_a', 'first')
sting_layers = hook_static_layers()
sting_layers += [
    {'type': 'rect', 'x': M_X + 50, 'y': (m_y(0) + m_y(10)) / 2, 'width': 6, 'height': m_y(10) - m_y(0), 'fill': RED, 'depth': 0, 'z': 15,
     'start': t_first, 'enter': {'type': 'wipeDown', 'at': t_first, 'duration': 0.3}},
    tag('HALF YOUR AIR GOES HERE', '44%', m_y(10) + 70, t_first, size=28, w=480),
]
scenes.append({
    'id': 's17_sting_a', 'duration': s['dur'], 'background': copy.deepcopy(SURFACE),
    'transitionIn': {'type': 'whip', 'duration': 0.25, 'direction': 'down'},
    'layers': sting_layers,
    # ends at zoom 1.0 = frame 0 of s01, so the loop restarts on the same picture
    'camera': {'keyframes': [{'t': 0, 'zoom': 1.03}, {'t': s['dur'], 'zoom': 1.0, 'ease': 'out'}]},
    'sfx': [{'cue': 'bubbles', 'at': 0.0, 'volume': 0.5}],
    'notes': notes('sting_a'),
})

# ---------------------------------------------------------------- storyboard
t_turn = SC['turn']['start']
t_r1k = SC['r1k']['start']
t_twist = SC['twist']['start']
EMPH = {'ache', 'half', 'imploded', 'falling', 'bottle', 'blood', 'pretend', 'easy', 'shot', 'gives', 'teaspoon', 'underwater', 'alive', 'never',
        'can', 'balloon', 'four', 'first'}
sb = {
    'version': 1,
    'id': 'explainer-short-mariana-pressure',
    'title': "You Wouldn't Implode In The Mariana Trench",
    'format': '9:16',
    'fps': 30,
    'scenes': scenes,
    'captions': {
        'maxWords': 3, 'maxChars': 18,
        'glue': ['ten metres', 'water bottle', 'shot glass', 'sperm whales', 'water balloon', 'four percent', 'Mariana Trench', 'not alive'],
        'words': [{'text': w['text'], 'start': w['start'], 'end': w['end'],
                   **({'emph': True} if clean(w['text']).strip(",.?'") in EMPH else {})} for w in WORDS],
        'style': {'font': 'display', 'fontSize': 86, 'color': '#ffffff', 'highlight': '#ff5a4a', 'highlightMode': 'none',
                  'strokeWidth': 12, 'uppercase': True, 'y': 0.71},
    },
    'audio': {
        'voice': [{'src': 'episodes/explainer-short-mariana-pressure/mix.wav', 'start': 0, 'volume': 1, 'duration': round(TOTAL, 3)}],
        'music': [
            # bed 1 under the shallow rungs, cut dead on the turnstile so the black frame lands in silence
            {'src': 'music/deep_ocean.m4a', 'start': 0, 'end': round(t_turn + 0.2, 3), 'volume': 0.24, 'duckTo': 0.14, 'fadeIn': 0.2, 'fadeOut': 0.15},
            {'src': 'sfx/underwater_rumble.wav', 'start': round(t_r1k, 3), 'end': round(t_twist, 3), 'volume': 0.3, 'duckTo': 0.2, 'fadeIn': 0.3, 'fadeOut': 0.2, 'loop': True},
            {'src': 'music/dread.m4a', 'start': round(t_r1k, 3), 'end': round(t_twist, 3), 'volume': 0.2, 'duckTo': 0.12, 'fadeIn': 0.4, 'fadeOut': 0.2},
            {'src': 'music/deep_ocean.m4a', 'start': round(t_twist, 3), 'end': round(TOTAL, 3), 'volume': 0.22, 'duckTo': 0.13, 'fadeIn': 0.3, 'fadeOut': 0.05},
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
    print(f'words {nwords}  total {TOTAL:.1f}s  wpm(all) {nwords / TOTAL * 60:.0f}')
    for i, (key, sp, text) in enumerate(PARAS):
        w0 = WORDS[PARA_FIRST[i]]
        w1 = [w for w in WORDS if w['para'] == i][-1]
        print(f'P{i + 1:<2} {key:8} {mmss(w0["start"])}-{mmss(w1["end"])} ({w0["start"] / TOTAL * 100:4.1f}%) {len(text.split()):>2}w  {text[:50]}')
    for sc in SCENES:
        print(f'  scene {sc["key"]:8} {mmss(sc["start"])} dur {sc["dur"]:.2f}')
    for needle, para in (('ten', 0), ('doubled', 1), ('thirty', 3), ('hundred', 4), ('two', 6), ('one', 9), ('bottom', 12), ('ache', 0), ('easy', 8), ('never', 15), ('metres', 19)):
        print(f'  "{needle}" at {word_t(para, needle):.2f}')
