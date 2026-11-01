#!/usr/bin/env python3
"""Generate storyboard.json for explainer-short-box-jellyfish (keep in sync with script.md).

usage: python3 gen_storyboard.py <out storyboard.json> [--timeline]

Before TTS, word timings are a per-word estimate (Kokoro am_michael: speed 0.96 for the hook and
[speed: 1.06] from paragraph 2). After TTS, replace `estimate_words()` with the real word list from
episodes/explainer-short-box-jellyfish/audio/captions.json and rerun: every layer is anchored to a
word (`A(scene, word)`), so the whole board retimes itself, and the Timer rate is re-fitted so the
clock reads 1:30 / 1:20 / 1:00 on the three spoken stamps.

Deliberate deviation from the template's "one paragraph = one scene": paragraphs 8-12 (turnstile
plus the four options) are ONE scene, so the Options card never re-enters, strikes accumulate and
the Timer layer stays continuous (producibility nice-to-have).
"""
import copy
import json
import re
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else 'storyboard.json'
SHOW_TIMELINE = '--timeline' in sys.argv

# ------------------------------------------------------------------ narration (= script.md narration block)
PARAS = [
    # (scene key, speed, text)
    ('hook', 0.96, 'Something brushed your leg. Worst case, you have two minutes.'),
    ('scale', 1.06, "You missed it because it's nearly clear: a bell up to dinner-plate size, trailing up to sixty tentacles, the longest taller than your ceiling."),
    ('reveal', 1.06, "That's a box jellyfish, called the sea's most venomous animal, and it's stuck to your shin."),
    ('mech', 1.06, 'Its tentacles are lined with nematocysts, coiled harpoons on hair triggers, and your skin just pulled thousands.'),
    ('speed', 1.06, "How fast? In a cousin, five million g, fifty times a rifle bullet, so the venom's in before you feel it."),
    ('pain', 1.06, 'Ninety seconds left, and the pain alone can drop you in the shallows.'),
    ('inside', 1.06, 'And the venom punches holes in your cells, flooding your blood with potassium, straight to your heart.'),
    ('options', 1.06, "Eighty seconds. Good news, you've got options."),
    ('options', 1.06, "Rub it? Every rub pulls more triggers, so you're petting a loaded gun."),
    ('options', 1.06, 'Rinse it? Fresh water fires any still loaded on you, and pee is fresh water with extra steps.'),
    ('options', 1.06, "Tough it out? That potassium's heading for your heart, and hearts can't tough anything out."),
    ('options', 1.06, 'Vinegar, thirty seconds. The harpoons still loaded on you, switched off.'),
    ('peak', 1.06, "One minute left. Catch is, you're down in the shallows, so someone else pulls you out, calls for help, CPR if needed, then pours."),
    ('posts', 1.06, "That's why Queensland beaches keep vinegar on posts."),
    ('twist', 1.06, 'The strange part? Twenty-four eyes, none on you. It was fishing for shrimp, and you swam into the net.'),
    ('stinger', 1.0, "Every wet season it swims back to where you swim. Still invisible."),
]
PARA_GAP = 0.32
DIP_GAP = 0.55  # extra breath before the twist (dipBlack)
TAIL = 0.4      # hard cut within 1 s of the last word
CAL = 0.885     # calibrated to the shipped am_michael Shorts (pressure-ladder: 250 words = 88.9 s at 0.96)


def estimate_words():
    """Per-word estimate: Kokoro am_michael ~185 wpm in-speech at 0.96, scaled by speed."""
    words, t = [], 0.0
    para_first = []
    for i, (_, speed, text) in enumerate(PARAS):
        if i:
            t += PARA_GAP + (DIP_GAP if PARAS[i][0] == 'twist' else 0)
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
    """Absolute time of the nth occurrence of `needle` inside paragraph `para`."""
    seen = 0
    for w in WORDS:
        if w['para'] == para and clean(w['text']).startswith(needle.lower()):
            seen += 1
            if seen == nth:
                return w['end'] if end else w['start']
    raise KeyError(f'{needle!r} not in paragraph {para}')


# scenes: consecutive paragraphs with the same key
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
    """Scene-local time of a word (para_offset picks a later paragraph inside a merged scene)."""
    s = SC[key]
    return round(word_t(s['paras'][0] + para_offset, needle, nth, end) - s['start'], 3)


# ------------------------------------------------------------------ the clock
T_MIN = word_t(0, 'minutes')                      # tick SOUND starts on "minutes"
T0 = 0.0                                          # the clock itself runs from frame 0 (it started when it touched you)
STAMPS = [(word_t(5, 'ninety'), 90), (word_t(7, 'eighty'), 80), (word_t(12, 'one'), 60)]
# least-squares rate through (T0, 120): rem(t) = 120 - r (t - T0)
num = sum((t - T0) * (120 - v) for t, v in STAMPS)
den = sum((t - T0) ** 2 for t, _ in STAMPS)
RATE = round(min(1.10, max(0.95, num / den)), 4)
T_FREEZE = word_t(12, 'someone')
FREEZE_VAL = round(120 - RATE * (T_FREEZE - T0), 2)


def clock(t):
    if t <= T0:
        return 120.0
    return max(FREEZE_VAL, 120 - RATE * (t - T0))


# ------------------------------------------------------------------ palette + svg assets (9 static markups)
RED, GREEN, CYAN = '#e5483d', '#3ccf7a', '#bff3ff'
GLOW = '0 0 14px rgba(190,245,255,0.95)'

SVG_BELL = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 140" overflow="visible">'
            '<path d="M10 128 C10 40 50 6 100 6 C150 6 190 40 190 128 C150 116 50 116 10 128 Z" fill="#bff3ff" fill-opacity="0.38" stroke="#effdff" stroke-width="5"/>'
            '<path d="M40 112 C44 60 70 30 100 28 C130 30 156 60 160 112" fill="none" stroke="#effdff" stroke-opacity="0.55" stroke-width="3"/>'
            '<ellipse cx="100" cy="86" rx="34" ry="18" fill="#e6fbff" fill-opacity="0.35"/></svg>')
SVG_TENTACLES = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 600" overflow="visible" fill="none" stroke="#d8f6ff" stroke-width="2.4" stroke-linecap="round" stroke-opacity="0.85">'
                 + ''.join(f'<path d="M{x0} 0 C{x0 + dx} 150 {x0 - dx} 300 {x0 + dx // 2} 450 S{x0 - dx} 560 {x0 + dx // 3} 600"/>'
                           for x0 in (14, 22, 30, 66, 74, 82, 118, 126, 134, 170, 178, 186) for dx in (10,))
                 + '</svg>')
SVG_TOUCH = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 100" overflow="visible">'
             '<path d="M198 70 C150 20 90 90 2 34" fill="none" stroke="#f2feff" stroke-width="5" stroke-linecap="round"/></svg>')
_CAPSULE = ('<ellipse cx="150" cy="450" rx="92" ry="128" fill="#bff3ff" fill-opacity="0.18" stroke="#ffffff" stroke-width="7"/>'
            '<line x1="150" y1="322" x2="182" y2="232" stroke="#ffe14d" stroke-width="6" stroke-linecap="round"/>')
SVG_NEMA_COILED = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 600" overflow="visible">' + _CAPSULE
                   + '<path d="M150 340 C90 360 90 420 150 420 C210 420 210 480 150 480 C90 480 90 540 150 540 C200 540 200 500 160 500" fill="none" stroke="#9fe8ff" stroke-width="6"/>'
                   + '<path d="M118 330 L182 330" stroke="#ffffff" stroke-width="8"/></svg>')
SVG_NEMA_FIRED = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 600" overflow="visible">' + _CAPSULE
                  + '<path d="M150 330 L150 10" stroke="#9fe8ff" stroke-width="6"/>'
                  + ''.join(f'<path d="M150 {y} l-16 22 M150 {y} l16 22" stroke="#9fe8ff" stroke-width="4"/>' for y in (40, 90, 140, 190))
                  + '<path d="M182 330 L214 300" stroke="#ffffff" stroke-width="8"/></svg>')


def svg_capsules(fill):
    caps = ''.join(f'<ellipse cx="{30 + 60 * i}" cy="50" rx="20" ry="30" fill="{fill}" fill-opacity="0.85" stroke="#ffffff" stroke-width="3"/>' for i in range(6))
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 100">{caps}</svg>'


SVG_CAPS_LOADED = svg_capsules('#7fe3ff')
SVG_CAPS_OFF = svg_capsules('#6b7480')
SVG_PLATE = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">'
             '<circle cx="100" cy="100" r="96" fill="#f4f1ea" stroke="#c9c3b6" stroke-width="4"/>'
             '<circle cx="100" cy="100" r="62" fill="none" stroke="#d9d3c6" stroke-width="4"/></svg>')


def svg_bottle(fill, label):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 240">'
            f'<rect x="38" y="4" width="24" height="26" rx="4" fill="#ffffff"/>'
            f'<path d="M30 30 L70 30 L80 70 L80 228 Q80 236 72 236 L28 236 Q20 236 20 228 L20 70 Z" fill="{fill}" fill-opacity="0.9" stroke="#ffffff" stroke-width="4"/>'
            f'<rect x="24" y="110" width="52" height="56" fill="#ffffff" fill-opacity="0.92"/>'
            f'<text x="50" y="146" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="15" fill="#0b0f14">{label}</text></svg>')


SVG_BOTTLE_WATER = svg_bottle('#4aa8e8', 'WATER')
SVG_BOTTLE_VINEGAR = svg_bottle('#e2a63b', 'VINEGAR')
SVG_SPARK = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">'
             + ''.join(f'<path d="M100 100 L{100 + dx} {100 + dy}" stroke="#ffe14d" stroke-width="9" stroke-linecap="round"/>'
                       for dx, dy in ((80, 0), (-80, 0), (0, 80), (0, -80), (56, 56), (-56, -56), (56, -56), (-56, 56)))
             + '<circle cx="100" cy="100" r="22" fill="#ffffff"/></svg>')

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


def headline(text, at, y='26%', color='white', size=62, out=None, **kw):
    p = {'text': text, 'at': at, 'size': size, 'color': color, 'underline': True}
    if out is not None:
        p['out'] = out
    lines = text.count('\n') + 1
    return comp('explainer/Headline', '50%', y, 1000, int(size * 1.6 * lines + 40), p, depth=0, z=20, **kw)


TIMER_BOX = dict(x=740, y='16.2%', w=380, h=160)


def timer(scene_key, start=None, end=None, white=False):
    """One Timer layer per scene (no global layers): `from` = the real clock at the layer's start."""
    s = SC[scene_key]
    t0 = s['start'] + (start or 0.0)
    v0 = round(clock(t0), 3)
    ticking = (not white) and t0 >= T0 - 1e-6 and v0 > FREEZE_VAL
    p = {'from': v0, 'to': FREEZE_VAL if ticking else v0, 'rate': RATE if ticking else 0,
         'at': start or 0.0, 'style': 'box', 'format': 'mm:ss', 'size': 96,
         'warnBelow': -1 if white else 121}
    kw = {'depth': 0, 'z': 30}
    if start is not None:
        kw['start'] = start
    if end is not None:
        kw['end'] = end
    return comp('explainer/Timer', TIMER_BOX['x'], TIMER_BOX['y'], TIMER_BOX['w'], TIMER_BOX['h'], p, **kw)


def ocean(depth=2, surface=0.2, rays=7, **extra):
    p = {'depth': depth, 'rays': rays, 'seed': 3, 'snow': 40}
    if surface is not None:
        p['surface'] = surface
    p.update(extra)
    return {'type': 'component', 'name': 'explainer/Ocean', 'depth': 0.12, 'overscan': 1.2, 'props': p}


SHALLOWS = ocean(depth=2, surface=0.2, rays=7)
DARK = ocean(depth=300, surface=None, rays=0, snow=50)


def notes(key):
    return ' '.join(PARAS[i][2] for i in SC[key]['paras'])


scenes = []

# ---------------------------------------------------------------- s01 hook (frame 1 = last frame)
HOOK_LAYERS = [
    comp('explainer/You', '50%', '24%', 200, 340, {'pose': 'stand'}, id='you', idle=[{'type': 'bob', 'amount': 6, 'speed': 0.5}]),
    svg(SVG_TENTACLES, '64%', '33.4%', 200, 600, id='tentacles', anchorY=0, opacity=0.22, idle=[{'type': 'sway', 'amount': 2, 'speed': 0.3}]),
    svg(SVG_BELL, '64%', '30%', 220, 154, id='bell', opacity=0.24, shadow=GLOW, idle=[{'type': 'breathe', 'amount': 0.04, 'speed': 0.6}]),
    svg(SVG_TOUCH, '57.5%', '31.4%', 180, 90, id='touch', opacity=0.85, shadow=GLOW),
    {'type': 'particles', 'preset': 'bubbles', 'count': 14, 'x': '50%', 'y': '40%', 'width': 1080, 'height': 900, 'opacity': 0.5, 'seed': 7, 'depth': 0.6},
]
h = SC['hook']
scenes.append({
    'id': 's01_hook', 'duration': h['dur'], 'background': SHALLOWS,
    'layers': copy.deepcopy(HOOK_LAYERS) + [
        timer('hook'),
        tag('WORST CASE', TIMER_BOX['x'], '23.2%', A('hook', 'worst'), size=26, w=380, accent=RED),
    ],
    'camera': {'keyframes': [{'t': 0, 'zoom': 1.0}, {'t': h['dur'], 'zoom': 1.06, 'ease': 'inOut'}]},
    'notes': notes('hook'),
})

# ---------------------------------------------------------------- s02 scale: shot A bell + plate, shot B tentacle vs ceiling
s = SC['scale']
tB = A('scale', 'trailing')
PPM = 260  # shot B: px per metre (You 1.75 m = 455 px; tentacle 3 m = 780 px; ceiling 2.4 m)
FLOOR_Y = 1114
scenes.append({
    'id': 's02_scale', 'duration': s['dur'], 'background': SHALLOWS,
    'layers': [
        # shot A (1100 px/m: bell 30 cm = 330 px, plate 27 cm = 297 px)
        svg(SVG_BELL, '30%', '42%', 330, 231, opacity=0.24, shadow=GLOW, end=tB,
            keyframes=[{'t': 0, 'opacity': 0.24}, {'t': 0.8, 'opacity': 0.5}]),
        svg(SVG_PLATE, '70%', '42%', 297, 297, end=tB, enter={'type': 'pop', 'at': A('scale', 'dinner'), 'duration': 0.3}, start=A('scale', 'dinner')),
        tag('BELL: UP TO ~30 CM', '30%', '53%', A('scale', 'bell'), out=tB, size=30, w=480),
        tag('DINNER PLATE ~27 CM', '70%', '53%', A('scale', 'dinner'), out=tB, size=30, w=480, accent='#ffffff'),
        # shot B (true scale, 260 px/m)
        {'type': 'rect', 'x': '50%', 'y': FLOOR_Y, 'width': 900, 'height': 6, 'fill': '#ffffff', 'opacity': 0.7, 'start': tB},
        {'type': 'rect', 'x': '50%', 'y': FLOOR_Y - int(2.4 * PPM), 'width': 900, 'height': 6, 'fill': RED, 'start': tB,
         'enter': {'type': 'wipeRight', 'at': A('scale', 'ceiling'), 'duration': 0.4}},
        svg(SVG_TENTACLES, '33%', FLOOR_Y - int(3.0 * PPM), 120, int(3.0 * PPM), anchorY=0, opacity=0.6, start=tB,
            keyframes=[{'t': tB, 'scaleY': 0.15}, {'t': A('scale', 'sixty'), 'scaleY': 0.5}, {'t': A('scale', 'longest'), 'scaleY': 1.0, 'ease': 'out'}],
            idle=[{'type': 'sway', 'amount': 1.5, 'speed': 0.3}]),
        svg(SVG_BELL, '33%', FLOOR_Y - int(3.0 * PPM) - 26, 90, 63, opacity=0.6, shadow=GLOW, start=tB),
        comp('explainer/You', '60%', FLOOR_Y - int(1.75 * PPM / 2), 260, int(1.75 * PPM), {'pose': 'stand', 'pxPerM': PPM, 'align': 'bottom'}, start=tB),
        tag('UP TO 60 TENTACLES', '33%', '61%', A('scale', 'sixty'), out=A('scale', 'longest'), size=30, w=520),
        tag('LONGEST: 3 M', '33%', '61%', A('scale', 'longest'), size=30, w=520),
        tag('2.4 M CEILING', '30%', '23.6%', A('scale', 'ceiling'), size=28, w=420, accent='#ffffff'),
        timer('scale'),
    ],
    'camera': {'preset': 'panDown', 'amount': 0.3},
    'sfx': [{'cue': 'pop', 'at': A('scale', 'bell'), 'volume': 0.5}, {'cue': 'pop', 'at': A('scale', 'ceiling'), 'volume': 0.5}],
    'notes': notes('scale'),
})

# ---------------------------------------------------------------- s03 reveal (shin close-up = push-in on You's leg)
s = SC['reveal']
scenes.append({
    'id': 's03_reveal', 'duration': s['dur'], 'background': SHALLOWS,
    'layers': [
        comp('explainer/You', '50%', '44%', 520, 900, {'pose': 'stand'}, idle=[{'type': 'bob', 'amount': 4, 'speed': 0.5}]),
        svg(SVG_TOUCH, '53%', '57%', 260, 130, opacity=0.9, shadow=GLOW),
        svg(SVG_TOUCH, '51%', '59.5%', 240, 120, opacity=0.9, shadow=GLOW, rotate=-8, flipX=True),
        svg(SVG_TOUCH, '54%', '62%', 250, 125, opacity=0.9, shadow=GLOW, rotate=6),
        headline('BOX JELLYFISH', A('reveal', 'jellyfish')),
        tag("THE SEA'S MOST VENOMOUS ANIMAL", '50%', '32%', A('reveal', 'venomous'), size=30, w=900),
        tag('60+ DEATHS ON RECORD IN AUSTRALIA', '50%', '36%', A('reveal', 'venomous', end=True) + 0.3, size=24, w=820, accent='#ffffff'),
        timer('reveal'),
    ],
    'camera': {'keyframes': [{'t': 0, 'zoom': 1.0, 'y': '50%'}, {'t': A('reveal', 'stuck'), 'zoom': 1.25, 'y': '56%', 'ease': 'out'}],
               'shake': [{'at': A('reveal', 'stuck'), 'duration': 0.35, 'amplitude': 12}]},
    'sfx': [{'cue': 'stinger', 'at': A('reveal', 'stuck'), 'volume': 0.8}],
    'notes': notes('reveal'),
})

# ---------------------------------------------------------------- s04 mechanism (coiled -> fired swap)
s = SC['mech']
t_fire = A('mech', 'pulled')
scenes.append({
    'id': 's04_mechanism', 'duration': s['dur'], 'background': ocean(depth=40, surface=None, rays=3),
    'layers': [
        svg(SVG_NEMA_COILED, '50%', '42%', 360, 720, end=t_fire),
        svg(SVG_NEMA_FIRED, '50%', '42%', 360, 720, start=t_fire, enter={'type': 'pop', 'at': t_fire, 'duration': 0.12}),
        tag('NEMATOCYST', '30%', '25%', A('mech', 'nematocysts'), size=32, w=480),
        tag('HAIR TRIGGER', '74%', '33%', A('mech', 'hair'), size=28, w=380, accent='#ffe14d'),
        tag('TOUCH = FIRE', '50%', '62%', t_fire, size=34, w=520),
        tag('x THOUSANDS', '74%', '50%', A('mech', 'thousands'), size=28, w=380, accent='#ffffff'),
        timer('mech'),
    ],
    'camera': {'preset': 'pushIn', 'amount': 0.5},
    'sfx': [{'cue': 'click', 'at': t_fire, 'volume': 0.9}],
    'notes': notes('mech'),
})

# ---------------------------------------------------------------- s05 speed (honest comparison + race without numbers)
s = SC['speed']
scenes.append({
    'id': 's05_speed', 'duration': s['dur'], 'background': DARK,
    'layers': [
        headline('HOW FAST?', A('speed', 'how'), color='red'),
        comp('explainer/SpeedBars', '50%', '41%', 920, 420, {
            'title': 'ACCELERATION', 'at': A('speed', 'cousin'), 'stagger': 0.5, 'size': 30,
            'rows': [{'label': 'RIFLE BULLET', 'value': 100000, 'text': '~100,000 G'},
                     {'label': 'HARPOON*', 'value': 5400000, 'text': '5,400,000 G', 'color': RED}]}, depth=0),
        tag('*MEASURED IN HYDRA, A RELATIVE', '50%', '53%', A('speed', 'cousin') + 0.4, size=22, w=760, accent='#ffffff'),
        tag('50x A RIFLE BULLET', '50%', '33%', A('speed', 'fifty'), out=A('speed', 'venom'), size=30, w=600),
        tag('1. VENOM IN', '32%', '60%', A('speed', 'in', nth=2), size=30, w=420),
        tag('2. YOU FEEL IT', '68%', '60%', A('speed', 'feel'), size=30, w=420, accent='#ffffff'),
        timer('speed'),
    ],
    'sfx': [{'cue': 'whoosh', 'at': A('speed', 'cousin'), 'volume': 0.7}],
    'notes': notes('speed'),
})

# ---------------------------------------------------------------- s06 pain (rung 3, clock stamp 1:30)
s = SC['pain']
t_drop = A('pain', 'drop')
scenes.append({
    'id': 's06_pain', 'duration': s['dur'], 'background': SHALLOWS,
    'layers': [
        comp('explainer/You', '50%', '30%', 220, 370, {'pose': 'panic'},
             keyframes=[{'t': 0, 'y': '30%'}, {'t': t_drop, 'y': '30%'}, {'t': s['dur'], 'y': '38%', 'ease': 'in'}]),
        {'type': 'particles', 'preset': 'bubbles', 'count': 30, 'x': '50%', 'y': '38%', 'width': 500, 'height': 600, 'start': t_drop, 'seed': 4},
        tag('PAIN', '50%', '50%', A('pain', 'pain'), size=40, w=300),
        tag('CAN DROP ADULTS IN SHALLOW WATER', '50%', '56%', t_drop, size=28, w=860, accent='#ffffff'),
        timer('pain'),
    ],
    'camera': {'preset': 'drift', 'amount': 0.4, 'shake': [{'at': t_drop, 'duration': 0.4, 'amplitude': 16}]},
    'sfx': [{'cue': 'impact', 'at': t_drop, 'volume': 0.8}, {'cue': 'breath', 'at': t_drop + 0.5, 'volume': 0.5}],
    'notes': notes('pain'),
})

# ---------------------------------------------------------------- s07 inside (x-ray You, cells, K+ dots -> heart)
s = SC['inside']
t_holes, t_k, t_heart = A('inside', 'holes'), A('inside', 'potassium'), A('inside', 'heart')
HEART_XY = (540, 640)
cells = []
for i, (cx, cy) in enumerate(((230, 1000), (330, 1110), (210, 1150))):
    cells.append({'type': 'circle', 'x': cx, 'y': cy, 'width': 120, 'height': 120, 'fill': 'rgba(255,190,190,0.25)', 'stroke': '#ffd6d6', 'strokeWidth': 4,
                  'enter': {'type': 'pop', 'at': 0.2 + 0.1 * i, 'duration': 0.3}})
    cells.append({'type': 'circle', 'x': cx + 14, 'y': cy - 10, 'width': 26, 'height': 26, 'fill': '#0b0f14', 'start': t_holes + 0.1 * i,
                  'enter': {'type': 'pop', 'at': t_holes + 0.1 * i, 'duration': 0.2}})
kdots = []
for i in range(8):
    sx, sy = 240 + (i % 3) * 50, 1060 + (i // 3) * 40
    kdots.append({'type': 'circle', 'x': sx, 'y': sy, 'width': 22, 'height': 22, 'fill': '#ffe14d', 'start': t_k,
                  'keyframes': [{'t': t_k + 0.05 * i, 'x': sx, 'y': sy}, {'t': t_heart + 0.05 * i, 'x': HEART_XY[0], 'y': HEART_XY[1], 'ease': 'in'}]})
scenes.append({
    'id': 's07_inside', 'duration': s['dur'], 'background': DARK,
    'layers': [
        comp('explainer/You', '50%', '42%', 420, 720, {'pose': 'stand', 'silhouette': '#7fd3e6'}, opacity=0.55),
        comp('explainer/WhaleHeart', HEART_XY[0], HEART_XY[1], 110, 110, {'silhouette': RED}, idle=[{'type': 'pulse', 'amount': 0.08, 'speed': 2.2}]),
        *cells, *kdots,
        tag('HOLES IN YOUR CELLS', '30%', '54%', t_holes, size=26, w=480, accent='#ffffff'),
        tag('K+ FLOODS YOUR BLOOD', '70%', '54%', t_k, size=26, w=460, accent='#ffe14d'),
        headline('YOUR HEART', t_heart, color='red'),
        timer('inside'),
    ],
    'camera': {'keyframes': [{'t': 0, 'zoom': 1.0}, {'t': s['dur'], 'zoom': 1.12, 'y': '40%'}]},
    'sfx': [{'cue': 'heartbeat_fast', 'at': t_heart, 'volume': 0.8}],
    'notes': notes('inside'),
})

# ---------------------------------------------------------------- s08 turnstile + options (paragraphs 8-12 as one scene)
s = SC['options']
o_at = A('options', 'options')
t_gun = A('options', 'gun', para_offset=1)
t_rub = A('options', 'rub', para_offset=1)
t_trig = A('options', 'triggers', para_offset=1)
t_rinse = A('options', 'rinse', para_offset=2)
t_loaded = A('options', 'loaded', para_offset=2)
t_pee = A('options', 'pee', para_offset=2)
t_tough = A('options', 'tough', para_offset=3)
t_anything = A('options', 'anything', para_offset=3)
t_vin = A('options', 'vinegar', para_offset=4)
t_loaded2 = A('options', 'loaded', para_offset=4)
t_switched = A('options', 'switched', para_offset=4)
t_pot = A('options', 'potassium', para_offset=3)
k_inset = [{'type': 'circle', 'x': 300 + 30 * i, 'y': 1133, 'width': 20, 'height': 20, 'fill': '#ffe14d', 'start': t_pot, 'end': t_vin,
            'keyframes': [{'t': t_pot + 0.06 * i, 'x': 300 + 30 * i}, {'t': t_pot + 1.2 + 0.06 * i, 'x': 540, 'ease': 'in'}]} for i in range(4)]
IN_Y = '59%'
scenes.append({
    'id': 's08_options', 'duration': s['dur'], 'background': DARK,
    'layers': [
        headline('GOOD NEWS?', A('options', 'good'), out=o_at, color='white'),
        comp('explainer/Options', '50%', '37%', 1000, 640, {
            'title': 'YOUR OPTIONS', 'at': o_at, 'stagger': 0.08, 'size': 50, 'stamp': True,
            'items': ['RUB IT', 'RINSE IT', 'TOUGH IT OUT', 'VINEGAR, 30 S'],
            'hidden': [{'index': 3, 'until': t_vin, 'text': '???'}],
            'strikes': [{'index': 0, 'at': t_gun}, {'index': 1, 'at': t_loaded}, {'index': 2, 'at': t_anything}],
            'select': {'index': 3, 'at': t_vin}}, depth=0, z=10),
        # inset 1: rub -> more triggers fire
        comp('explainer/You', '38%', IN_Y, 120, 200, {'pose': 'point'}, start=t_rub, end=t_rinse),
        svg(SVG_SPARK, '56%', IN_Y, 150, 150, start=t_trig, end=t_rinse, enter={'type': 'pop', 'at': t_trig, 'duration': 0.2}),
        # inset 2: rinse -> loaded capsules fire; pee myth
        svg(SVG_BOTTLE_WATER, '36%', IN_Y, 80, 192, rotate=-40, start=t_rinse, end=t_tough),
        svg(SVG_CAPS_LOADED, '62%', IN_Y, 300, 84, start=t_rinse, end=t_loaded),
        svg(SVG_SPARK, '62%', IN_Y, 150, 150, start=t_loaded, end=t_tough, enter={'type': 'pop', 'at': t_loaded, 'duration': 0.2}),
        tag('PEE = MYTH', '72%', '54.5%', t_pee, out=t_tough, size=28, w=320, rotate=-8),
        # inset 3: tough it out -> heart + clock
        comp('explainer/WhaleHeart', '50%', IN_Y, 120, 120, {'silhouette': RED}, start=t_tough, end=t_vin, idle=[{'type': 'pulse', 'amount': 0.1, 'speed': 2.4}]),
        *k_inset,
        # inset 4: vinegar -> loaded capsules switched off
        svg(SVG_BOTTLE_VINEGAR, '36%', IN_Y, 80, 192, rotate=-40, start=t_vin),
        svg(SVG_CAPS_LOADED, '62%', IN_Y, 300, 84, start=t_vin, end=t_switched),
        svg(SVG_CAPS_OFF, '62%', IN_Y, 300, 84, start=t_switched, enter={'type': 'fade', 'at': t_switched, 'duration': 0.3}),
        tag('WORKS', '50%', '53.5%', t_vin + 0.3, size=30, w=260, accent=GREEN),
        tag('STOPS UNFIRED STINGS ONLY', '50%', '64%', t_loaded2, size=24, w=700, accent='#ffffff'),
        tag('TROPICAL AUSTRALIAN BOX JELLYFISH', '50%', '67.5%', t_vin + 0.6, size=20, w=700, accent='#ffffff'),
        timer('options'),
    ],
    'camera': {'preset': 'none'},
    'sfx': [{'cue': 'whoosh_long', 'at': o_at, 'volume': 0.7},
            {'cue': 'glitch', 'at': t_gun, 'volume': 0.6}, {'cue': 'glitch', 'at': t_loaded, 'volume': 0.6},
            {'cue': 'glitch', 'at': t_anything, 'volume': 0.6}, {'cue': 'ding', 'at': t_vin, 'volume': 0.8}],
    'notes': notes('options'),
})

# ---------------------------------------------------------------- s09 peak (rung-3 callback, someone else stops the clock)
s = SC['peak']
t_some = A('peak', 'someone')
scenes.append({
    'id': 's09_peak', 'duration': s['dur'], 'background': ocean(depth=1, surface=0.55, rays=5),
    'layers': [
        headline('THE CATCH', A('peak', 'catch'), out=t_some, color='red'),
        comp('explainer/You', '36%', '60%', 260, 140, {'pose': 'stand'}, rotate=82, opacity=0.9, start=A('peak', 'down'),
             enter={'type': 'drop', 'at': A('peak', 'down'), 'duration': 0.4}),
        {'type': 'particles', 'preset': 'bubbles', 'count': 12, 'x': '36%', 'y': '58%', 'width': 300, 'height': 300, 'start': A('peak', 'shallows'), 'seed': 9},
        comp('explainer/You', '62%', '57%', 140, 240, {'pose': 'run'}, start=t_some,
             keyframes=[{'t': t_some, 'x': '96%'}, {'t': t_some + 1.0, 'x': '58%', 'ease': 'out'}]),
        headline('SOMEONE ELSE\nSTOPS THE CLOCK', t_some, size=56),
        comp('explainer/Options', '50%', '43%', 1000, 420, {
            'title': ' ', 'at': A('peak', 'pulls'), 'size': 38,
            'items': ['OUT OF THE WATER', 'CALL 000 / EMERGENCY', 'CPR IF NOT BREATHING', 'VINEGAR, 30 S'],
            'itemAt': [A('peak', 'out'), A('peak', 'help'), A('peak', 'cpr'), A('peak', 'pours')]}, depth=0, z=10),
        svg(SVG_BOTTLE_VINEGAR, '50%', '56%', 60, 144, rotate=-50, start=A('peak', 'cpr'),
            enter={'type': 'pop', 'at': A('peak', 'cpr'), 'duration': 0.25},
            keyframes=[{'t': A('peak', 'cpr'), 'rotate': -20}, {'t': A('peak', 'pours'), 'rotate': -70, 'ease': 'out'}]),
        timer('peak', end=t_some),
        timer('peak', start=t_some, white=True),
    ],
    'camera': {'preset': 'pushIn', 'amount': 0.3},
    'sfx': [{'cue': 'riser', 'at': t_some, 'volume': 0.5}],
    'notes': notes('peak'),
})

# ---------------------------------------------------------------- s10 posts (1.4 s map pin flash, then the post)
s = SC['posts']
t_q = A('posts', 'queensland')
t_post = A('posts', 'posts')
scenes.append({
    'id': 's10_posts', 'duration': s['dur'], 'background': ocean(depth=1, surface=0.62, rays=5),
    'layers': [
        comp('explainer/Map', '50%', '42%', 900, 700, {
            'at': t_q, 'out': t_q + 1.4, 'highlight': ['australia'],
            'views': [{'t': 0, 'lon': 134, 'lat': -25, 'zoom': 7}],
            'pins': [{'lon': 145.8, 'lat': -16.9, 'label': 'CAIRNS, N. QUEENSLAND', 'at': t_q + 0.2}]}, depth=0, end=t_q + 1.8),
        {'type': 'rect', 'x': '50%', 'y': 1010, 'width': 22, 'height': 420, 'fill': '#d9d2c3', 'start': t_post - 0.3},
        {'type': 'rect', 'x': '50%', 'y': 820, 'width': 200, 'height': 150, 'fill': '#e2a63b', 'stroke': '#ffffff', 'strokeWidth': 5, 'radius': 10, 'start': t_post - 0.3},
        {'type': 'text', 'text': 'VINEGAR', 'x': '50%', 'y': 820, 'fontSize': 40, 'color': '#0b0f14', 'start': t_post - 0.3},
        tag("MOST STINGS AREN'T FATAL", '50%', '62%', t_post, size=26, w=640, accent='#ffffff'),
        timer('posts', white=True),
    ],
    'camera': {'preset': 'pushIn', 'amount': 0.2},
    'notes': notes('posts'),
})

# ---------------------------------------------------------------- s11 twist (24 eyes, shrimp, you in the net)
s = SC['twist']
t_eyes = A('twist', 'twenty-four')
eyes = []
for c, (ex, ey) in enumerate(((440, 690), (500, 640), (580, 640), (640, 690))):
    for k in range(6):
        t = round(t_eyes + 0.04 * (c * 6 + k), 3)
        eyes.append({'type': 'circle', 'x': ex + (k % 3 - 1) * 14, 'y': ey + (k // 3) * 16, 'width': 11, 'height': 11,
                     'fill': '#9ff7ff', 'shadow': '0 0 6px #9ff7ff', 'start': t, 'enter': {'type': 'pop', 'at': t, 'duration': 0.15}})
scenes.append({
    'id': 's11_twist', 'duration': s['dur'], 'background': ocean(depth=60, surface=None, rays=2),
    'transitionIn': {'type': 'dipBlack', 'duration': 0.5},
    'layers': [
        svg(SVG_TENTACLES, '50%', 760, 520, 900, anchorY=0, opacity=0.45, idle=[{'type': 'sway', 'amount': 2, 'speed': 0.3}]),
        svg(SVG_BELL, '50%', 680, 520, 364, opacity=0.45, shadow=GLOW, idle=[{'type': 'breathe', 'amount': 0.04, 'speed': 0.6}]),
        *eyes,
        comp('explainer/Stat', '50%', '19%', 600, 220, {'value': 24, 'label': 'EYES  (YOU: 2)', 'at': t_eyes, 'duration': 0.8, 'size': 96}, depth=0, z=20),
        tag('LOOKING AT YOU: 0', '50%', '29%', A('twist', 'none'), size=30, w=560, accent='#ffffff'),
        comp('explainer/Krill', '74%', '56%', 140, 70, {}, start=A('twist', 'fishing'),
             keyframes=[{'t': A('twist', 'fishing'), 'x': '92%'}, {'t': A('twist', 'shrimp') + 0.6, 'x': '66%'}]),
        tag('DINNER: SHRIMP', '72%', '62%', A('twist', 'shrimp'), size=26, w=400),
        comp('explainer/You', '26%', '57%', 70, 120, {'pose': 'shrug', 'silhouette': True}, start=A('twist', 'you', nth=1)),
        tag('YOU: IN THE NET', '28%', '62%', A('twist', 'net'), size=26, w=400, accent='#ffffff'),
    ],
    'camera': {'preset': 'drift', 'amount': 0.4},
    'sfx': [{'cue': 'sonar_ping', 'at': t_eyes, 'volume': 0.6}],
    'notes': notes('twist'),
})

# ---------------------------------------------------------------- s12 stinger: frame-1 layers verbatim, Timer back at 2:00
s = SC['stinger']
scenes.append({
    'id': 's12_stinger', 'duration': s['dur'], 'background': SHALLOWS,
    'layers': copy.deepcopy(HOOK_LAYERS) + [
        comp('explainer/Timer', TIMER_BOX['x'], TIMER_BOX['y'], TIMER_BOX['w'], TIMER_BOX['h'],
             {'from': 120, 'to': 120, 'rate': 0, 'at': 0, 'style': 'box', 'format': 'mm:ss', 'size': 96, 'warnBelow': 121}, depth=0, z=30),
        tag('STINGER SEASON ~NOV-MAY', '50%', '50%', A('stinger', 'wet'), out=A('stinger', 'still'), size=28, w=460, accent='#ffffff'),
    ],
    # ends at zoom 1.0 = frame 1 of s01, so the loop is seamless
    'camera': {'keyframes': [{'t': 0, 'zoom': 1.06}, {'t': s['dur'], 'zoom': 1.0, 'ease': 'out'}]},
    'notes': notes('stinger'),
})

# ---------------------------------------------------------------- storyboard
twist_start = SC['twist']['start']
sb = {
    'version': 1,
    'id': 'explainer-short-box-jellyfish',
    'title': 'You Have 2 Minutes After A Box Jellyfish Sting',
    'format': '9:16',
    'fps': 30,
    'scenes': scenes,
    'captions': {
        'maxWords': 3, 'maxChars': 18,
        'glue': ['box jellyfish', 'five million', 'rifle bullet', 'fresh water', 'extra steps', 'twenty-four eyes'],
        'words': [{'text': w['text'], 'start': w['start'], 'end': w['end'],
                   **({'emph': True} if clean(w['text']) in {'minutes', 'invisible', 'heart', 'vinegar', 'someone', 'shallows'} else {})}
                  for w in WORDS],
        'style': {'font': 'display', 'fontSize': 88, 'color': '#ffffff', 'highlight': '#ff5a4a', 'highlightMode': 'none',
                  'strokeWidth': 12, 'uppercase': True, 'y': 0.70},
    },
    'audio': {
        'voice': [{'src': 'episodes/explainer-short-box-jellyfish/mix.wav', 'start': 0, 'volume': 1, 'duration': round(TOTAL, 3)}],
        'music': [
            {'src': 'music/tension_pulse.m4a', 'start': 0, 'end': round(twist_start, 3), 'volume': 0.22, 'duckTo': 0.12, 'fadeIn': 0.2, 'fadeOut': 0.6},
            {'src': 'sfx/clock_ticking.wav', 'start': round(T_MIN, 3), 'end': round(T_FREEZE, 3), 'volume': 0.3, 'duckTo': 0.3, 'fadeIn': 0.05, 'fadeOut': 0.05, 'loop': True},
            {'src': 'music/deep_ocean.m4a', 'start': round(twist_start, 3), 'end': round(TOTAL, 3), 'volume': 0.24, 'duckTo': 0.14, 'fadeIn': 0.4, 'fadeOut': 0.1},
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
    print(f'clock rate {RATE}  tick sfx from {T_MIN:.2f}  freeze {FREEZE_VAL:.1f}s left at {T_FREEZE:.2f}')
    for t, v in STAMPS:
        print(f'  stamp {v}: said at {mmss(t)}, clock reads {clock(t):.1f}')
    for i, (key, sp, text) in enumerate(PARAS):
        w0 = WORDS[PARA_FIRST[i]]
        w1 = [w for w in WORDS if w['para'] == i][-1]
        print(f'P{i + 1:<2} {key:8} {mmss(w0["start"])}-{mmss(w1["end"])} ({w0["start"] / TOTAL * 100:4.1f}%) {len(text.split()):>2}w')
    for sc in SCENES:
        print(f'  scene {sc["key"]:8} {mmss(sc["start"])} dur {sc["dur"]:.2f}')
