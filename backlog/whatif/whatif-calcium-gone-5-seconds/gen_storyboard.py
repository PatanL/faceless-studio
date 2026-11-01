#!/usr/bin/env python3
"""Generate storyboard.json for whatif-calcium-gone-5-seconds from the script's shot list,
caption list and HUD state table (keep in sync with script.md). Output path is argv[1]."""
import json
import sys

OUT = sys.argv[1]

SERIF = '"Source Serif 4", "DejaVu Serif", Georgia, serif'
CYAN = '#7FE3FF'
NAVY = '#050B18'
PALE = '#D8F6FF'
WHITE = '#FFFFFF'
EVENT, RETURN, SLOWMO = 7.0, 67.0, 12.0


def tau(t):
    return (t - EVENT) / SLOWMO


def sand_m(t):
    return max(0.0, 40 - 12.08 * (tau(t) - 1.79))


# ------------------------------------------------------------------ captions (global seconds)
CAPTIONS = [
    (5.0, 7.0, "You're queuing at the Colosseum in Rome."),
    (8.0, 11.6, 'Every finger bends like a gummy worm.'),
    (13.5, 17.0, 'The whole queue starts to wobble.'),
    (20.5, 23.8, 'Marble is 40% calcium by weight.'),
    (24.0, 27.3, 'The Colosseum is made of it.'),
    (31.5, 34.8, 'Concrete loses its glue.'),
    (35.0, 38.3, 'Your house caves in on itself.'),
    (38.5, 41.5, '8.2 billion hearts stop at once.'),
    (48.5, 52.0, 'Everest is no longer the tallest mountain.'),
    (55.0, 59.0, 'Back in Rome, the sand keeps coming.'),
    (67.5, 70.3, 'Every calcium atom reappears exactly where it vanished.'),
    (70.5, 74.5, "But you're not standing there anymore."),
]

# ------------------------------------------------------------------ HUD state table (global seconds)
HUD = {
    'L': [
        {'from': 0, 'to': 7, 'text': 'CALCIUM', 'chip': 'online'},
        {'from': 7, 'to': 67, 'text': 'CALCIUM', 'chip': 'offline'},
        {'from': 67, 'to': 74.5, 'text': 'CALCIUM', 'chip': 'backOnline'},
    ],
    'T': [
        {'from': 0, 'to': 7, 'text': 'OFFLINE IN {v} S', 'track': [{'t': 0, 'v': 7.0, 'ease': 'linear'}, {'t': 7, 'v': 0, 'ease': 'linear'}], 'decimals': 3},
        {'from': 7, 'to': 67, 'text': 'ONLINE IN {v} S', 'track': [{'t': 7, 'v': 5.0, 'ease': 'linear'}, {'t': 67, 'v': 0, 'ease': 'linear'}], 'decimals': 3,
         'colorAt': [{'t': 61.0, 'color': '#FF5A5A'}]},
        {'from': 67, 'to': 74.5, 'text': 'ONLINE IN 0.000 S'},
    ],
    'S1': [
        {'from': 0, 'to': 5.8, 'text': 'IN EVERY BONE, HEARTBEAT AND LIMESTONE'},
        {'from': 5.8, 'to': 7, 'text': 'WHITE = CALCIUM', 'color': WHITE, 'glow': True},
        {'from': 7, 'to': 11, 'text': 'X-RAY TIME ×12'},
        {'from': 11, 'to': 17, 'text': 'YOU: −1.1 KG ≈ A CARTON OF MILK'},
        {'from': 17, 'to': 20.5, 'text': '1.7 TRILLION BONES: SOFT'},
        {'from': 24, 'to': 29.5, 'text': '100,000 M³ OF TRAVERTINE'},
        {'from': 29.5, 'to': 31.5, 'text': 'SAND: {v} M AWAY', 'track': [{'t': 29.5, 'v': round(sand_m(29.5), 2), 'ease': 'linear'}, {'t': 31.5, 'v': round(sand_m(31.5), 2), 'ease': 'linear'}], 'decimals': 0,
         'formula': 'v = 40 - 12.08*((t-7)/12 - 1.79)'},
        {'from': 31.5, 'to': 38.5, 'text': 'CONCRETE FAILING: {v} BILLION T', 'track': [{'t': 31.5, 'v': 0}, {'t': 38.3, 'v': 550, 'ease': 'out'}], 'decimals': 0},
        {'from': 38.5, 'to': 43.5, 'text': 'YOUR HEART: 3 BEATS MISSED'},
        {'from': 43.5, 'to': 55, 'text': 'LAND CAVING IN: {v}%', 'track': [{'t': 43.5, 'v': 0}, {'t': 54.5, 'v': 15.2, 'ease': 'out'}], 'decimals': 1},
        {'from': 55, 'to': 71, 'text': 'SAND: {v} M AWAY', 'track': [{'t': 55, 'v': round(sand_m(55), 2), 'ease': 'linear'}, {'t': 68.2, 'v': 0, 'ease': 'linear'}, {'t': 71, 'v': 0}], 'decimals': 1, 'clampMin': 0,
         'formula': 'v = max(0, 40 - 12.08*((t-7)/12 - 1.79))'},
        {'from': 71, 'to': 74.5, 'text': 'YOUR 1.1 KG: 1 M ABOVE YOU', 'color': WHITE},
    ],
    'S2': [
        {'from': 2.5, 'to': 7, 'text': 'STANDING SINCE AD 80'},
        {'from': 46, 'to': 48.5, 'text': 'DOVER CLIFFS: {v} M', 'track': [{'t': 46, 'v': 110}, {'t': 48.3, 'v': 0, 'ease': 'in'}], 'decimals': 0},
        {'from': 48.5, 'to': 50.5, 'text': 'EVEREST: {v} M', 'track': [{'t': 48.5, 'v': 8849}, {'t': 50.3, 'v': 8600, 'ease': 'out'}], 'decimals': 0, 'thousands': True},
        {'from': 50.5, 'to': 52, 'text': 'K2: 8,611 M'},
        {'from': 52, 'to': 55, 'text': 'REEF COLLAPSED: {v} KM', 'track': [{'t': 52, 'v': 0}, {'t': 54.8, 'v': 2300, 'ease': 'linear'}], 'decimals': 0, 'thousands': True},
        {'from': 55, 'to': 67, 'text': 'REACHES YOU IN {v} S', 'track': [{'t': 55, 'v': 1.1, 'ease': 'linear'}, {'t': 67, 'v': 0.1, 'ease': 'linear'}], 'decimals': 3},
        {'from': 67, 'to': 72.5, 'text': '1,946 YEARS · 5 SECONDS', 'color': WHITE},
        {'from': 72.5, 'to': 74.5, 'text': 'YOUR HEART: STILL 0 BPM'},
    ],
}
HUD_OPACITY = [{'t': 41.5, 'v': 1.0}, {'t': 41.8, 'v': 0.4}, {'t': 43.3, 'v': 0.4}, {'t': 43.6, 'v': 1.0}]

# ------------------------------------------------------------------ helpers
XRAY = {'saturate': 1.0, 'contrast': 1.05, 'vignette': 0.2}
DAY = {'saturate': 1.05, 'vignette': 0.1}
SKY = {'type': 'gradient', 'kind': 'linear', 'angle': 180, 'colors': ['#8EC9F0', '#F4E3C1'], 'depth': 0.1, 'overscan': 1.25}
XBG = {'type': 'color', 'color': NAVY, 'depth': 0.1, 'overscan': 1.25}

QUEUE_X = [150, 250, 345, 440, 540, 640, 735, 830, 930]
YOU_I = 4  # YOU is the 5th in line
QUEUE_Y = 1240


def comp(name, props=None, **kw):
    layer = {'type': 'component', 'name': name, 'props': props or {}}
    layer.update(kw)
    return layer


def colosseum(mode, **props):
    p = {'mode': mode}
    p.update(props)
    return comp('whatif/Colosseum', p, x='50%', y=760, width=1300, height=760, depth=0.4)


def kerb(mode='day', crumble=None):
    if mode == 'day':
        return {'type': 'rect', 'x': '50%', 'y': 1325, 'width': 1300, 'height': 40, 'fill': '#E6D8B8', 'stroke': '#B9A57E', 'strokeWidth': 2, 'depth': 0.8}
    p = {'mode': 'xray', 'kind': 'kerb'}
    if crumble is not None:
        p['crumble'] = crumble
    return comp('whatif/Colosseum', p, id='kerb', x='50%', y=1325, width=1300, height=60, depth=0.8)


def statue(mode, **props):
    p = {'mode': mode}
    p.update(props)
    return comp('whatif/Statue', p, x=1000, y=1120, width=150, height=330, depth=0.7)


def day_queue():
    ls = []
    cols = ['#9C8F7A', '#7E8FA3', '#A3857E', '#8A9C7E', '#FFFFFF', '#A39A7E', '#7E8A9C', '#9C7E8F', '#8F9C9A']
    for i, x in enumerate(QUEUE_X):
        ls.append(comp('explainer/You', {'pose': 'stand', 'color': cols[i]}, x=x, y=QUEUE_Y, width=110, height=230, depth=0.8))
    ls.append(comp('explainer/Tag', {'text': 'YOU', 'at': 0.6}, x=QUEUE_X[YOU_I], y=QUEUE_Y - 175, width=180, height=70, depth=0.8))
    return ls


def xray_queue(**props):
    ls = []
    for i, x in enumerate(QUEUE_X):
        p = {'view': 'body', 'timeOffset': round(0.15 * i, 2)}
        p.update(props)
        if i == YOU_I:
            p['heart'] = props.get('heart', {'bpm': 70, 'stopAt': 1.5})
            p['isYou'] = True
        ls.append(comp('whatif/XrayFigure', p, x=x, y=QUEUE_Y, width=110, height=230, depth=0.8))
    return ls


TITLE_ICON = (
    '<svg viewBox="0 0 220 80" xmlns="http://www.w3.org/2000/svg"><path d="M40 28 a14 14 0 1 1 18 -14 a14 14 0 0 1 18 14 '
    'L144 28 a14 14 0 0 1 18 -14 a14 14 0 1 1 18 14 a14 14 0 1 1 -18 14 a14 14 0 0 1 -18 14 L76 42 a14 14 0 0 1 -18 14 '
    'a14 14 0 0 1 -18 -14 a14 14 0 1 1 0 -14 Z" fill="none" stroke="#7FE3FF" stroke-width="6" stroke-linejoin="round" '
    'transform="translate(0 6)"/></svg>'
)


def title_layers(enter=True, exit_at=None, end=5.5):
    ls = [comp('whatif/TitleCard', {'pre': 'What if', 'keyword': 'calcium', 'post': 'disappeared for 5 seconds?', 'accent': CYAN,
                                   'font': SERIF, 'iconSvg': TITLE_ICON}, x='50%', y=760, width=960, height=520, depth=0, z=60)]
    for l in ls:
        l['start'] = 0
        l['end'] = end
        if enter:
            l['enter'] = {'type': 'fade', 'duration': 0.4}
        if exit_at is not None:
            l['exit'] = {'type': 'fade', 'at': exit_at, 'duration': end - exit_at}
    return ls


SHOTS = []


def shot(sid, start, end, background, layers=(), camera=None, transition=None, grade=None, sfx=(), notes='', hud=True):
    SHOTS.append(dict(id=sid, start=start, end=end, background=background, layers=list(layers), camera=camera,
                      transition=transition, grade=grade, sfx=list(sfx), notes=notes, hud=hud))


# 1 establishing + title (0.0-5.5)
shot('s01-establish', 0.0, 5.5, SKY, [
    colosseum('day'),
    kerb('day'),
    statue('day'),
    *day_queue(),
    *title_layers(enter=False, exit_at=4.6, end=5.0),
], camera={'preset': 'drift', 'amount': 0.4}, grade=DAY,
    sfx=[{'cue': 'clock_ticking', 'at': 0.0, 'volume': 0.25}, {'cue': 'tick', 'at': 5.0, 'volume': 0.5}],
    notes='Frame 1 = cover. Sunny Colosseum, queue on a travertine kerb, marble bust on a granite plinth, YOU tagged. Title clears at 5.0 before caption 1.')

# 2 X-ray scan / baseline (5.5-7.0)
shot('s02-xray-scan', 5.5, 7.0, XBG, [
    colosseum('xray', glow=1),
    kerb('xray'),
    statue('xray', glow=1),
    *xray_queue(glow=1, heart={'bpm': 70, 'stopAt': 1.5}),
    {'type': 'rect', 'x': '50%', 'y': 0, 'width': 1080, 'height': 6, 'fill': CYAN, 'shadow': '0 0 24px #7FE3FF', 'depth': 0, 'z': 50,
     'keyframes': [{'t': 0, 'y': 0, 'opacity': 1}, {'t': 0.3, 'y': 1920, 'opacity': 1, 'ease': 'linear'}, {'t': 0.31, 'opacity': 0}]},
], camera={'keyframes': [{'t': 0, 'zoom': 1.0}, {'t': 1.5, 'zoom': 1.06, 'ease': 'linear'}]}, transition={'type': 'cut', 'duration': 0},
    grade=XRAY, sfx=[{'cue': 'sonar_ping', 'at': 0.0, 'volume': 0.5}, {'cue': 'tick', 'at': 0.5, 'volume': 0.5}],
    notes='Scan line sweeps 0-0.3 s; all calcium white for 1.2 s (WHITE = CALCIUM); YOU heart pulses at 70 bpm.')

# 3 blink-out flip (7.0-8.0)
shot('s03-blinkout', 7.0, 8.0, XBG, [
    colosseum('xray', glow=[{'t': 0, 'v': 1}, {'t': 0.07, 'v': 0, 'ease': 'step'}]),
    kerb('xray'),
    statue('xray', glow=[{'t': 0, 'v': 1}, {'t': 0.07, 'v': 0, 'ease': 'step'}]),
    *xray_queue(glow=[{'t': 0, 'v': 1}, {'t': 0.07, 'v': 0, 'ease': 'step'}], heart={'bpm': 70, 'stopAt': 0.0}),
], camera={'keyframes': [], 'shake': [{'at': 0.0, 'duration': 0.3, 'amplitude': 10}]}, grade=XRAY,
    sfx=[{'cue': 'impact', 'at': 0.0, 'volume': 0.9}, {'cue': 'glitch', 'at': 0.0, 'volume': 0.4}],
    notes='Every white fill blinks to outline in 2 frames. HUD: CALCIUM OFFLINE, ONLINE IN 5.000 S, X-RAY TIME x12.')

# 4 POV hands (8.0-13.5)
shot('s04-hands', 8.0, 13.5, XBG, [
    colosseum('xray', sag=[{'t': 0, 'v': 0.0}, {'t': 5.5, 'v': 0.05}]),
    comp('whatif/XrayFigure', {'view': 'hands', 'bend': [{'t': 0.3, 'v': 0}, {'t': 3.5, 'v': 0.8, 'ease': 'out'}], 'wobbleHz': 3}, x='50%', y=1150, width=1000, height=900, depth=1.0),
], camera={'keyframes': [{'t': 0, 'zoom': 1.0}, {'t': 5.5, 'zoom': 1.05}]}, grade=XRAY,
    sfx=[{'cue': 'pop', 'at': 1.2, 'volume': 0.3}, {'cue': 'pop', 'at': 2.0, 'volume': 0.3}],
    notes='POV: your X-ray hands, finger bones outline-only, fingers droop and wobble like gummy worms.')

# 5 queue wobble (13.5-20.5)
shot('s05-queue-wobble', 13.5, 20.5, XBG, [
    colosseum('xray', sag=[{'t': 0, 'v': 0.05}, {'t': 7, 'v': 0.15}]),
    kerb('xray'),
    statue('xray'),
    *xray_queue(sway=[{'t': 0, 'v': 0.2}, {'t': 3, 'v': 1}], slump=[{'t': 0, 'v': 0}, {'t': 7, 'v': 0.15}], heart={'bpm': 70, 'stopAt': 0.0}),
], camera={'keyframes': [{'t': 0, 'x': QUEUE_X[YOU_I], 'y': 1150, 'zoom': 1.5}, {'t': 2.5, 'x': '50%', 'y': '50%', 'zoom': 1.0}]}, grade=XRAY,
    sfx=[{'cue': 'whoosh', 'at': 0.3, 'volume': 0.3}],
    notes='Pull out from YOU to the queue: arms flop, torsos sway like tube men; nobody falls yet. HUD 1.7 TRILLION BONES at 17.0.')

# 6 bust rung (20.5-24.0)
PIE = ('<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"><circle cx="100" cy="100" r="90" fill="none" stroke="#7FE3FF" stroke-width="6"/>'
       '<path d="M100 100 L100 10 A90 90 0 0 1 152.9 172.8 Z" fill="none" stroke="#7FE3FF" stroke-width="6" stroke-dasharray="10 8"/></svg>')
shot('s06-bust', 20.5, 24.0, XBG, [
    comp('whatif/Statue', {'mode': 'xray', 'melt': [{'t': 0.3, 'v': 0}, {'t': 3.5, 'v': 0.7, 'ease': 'in'}]}, x=420, y=1000, width=420, height=900, depth=0.6),
    {'type': 'svg', 'markup': PIE, 'x': 800, 'y': 700, 'width': 260, 'height': 260, 'start': 0.4, 'enter': {'type': 'pop', 'duration': 0.3}, 'depth': 0.2},
    comp('explainer/Stat', {'value': 40, 'from': 0, 'suffix': '%', 'label': 'CALCIUM', 'at': 0.4, 'duration': 1.0, 'size': 0.8, 'color': CYAN},
         x=800, y=900, width=320, height=160, depth=0.2),
], camera={'preset': 'pushIn', 'amount': 0.5}, grade=XRAY,
    sfx=[{'cue': 'click', 'at': 0.4, 'volume': 0.5}],
    notes='The bust from 0:00 sags into wax-like drips; the granite plinth stays square. Pie wedge 40%.')

# 7 implication: the Colosseum (24.0-27.5)
shot('s07-colosseum', 24.0, 27.5, XBG, [
    colosseum('xray', sag=[{'t': 0, 'v': 0.15}, {'t': 3.5, 'v': 0.25}]),
    kerb('xray'),
    statue('xray', melt=0.7),
    *xray_queue(sway=1, slump=0.15, heart={'bpm': 70, 'stopAt': 0.0}),
], camera={'keyframes': [{'t': 0, 'x': '50%', 'y': '40%', 'zoom': 1.15}, {'t': 2.0, 'x': '50%', 'y': '42%', 'zoom': 1.1},
                         {'t': 3.5, 'x': '50%', 'y': '58%', 'zoom': 1.2, 'ease': 'inOut'}]}, grade=XRAY,
    sfx=[{'cue': 'drone', 'at': 0.0, 'volume': 0.25}],
    notes='Full X-ray facade, arches start to bow; tilt down to the kerb under the queue by 3.5.')

# 8 textless break (27.5-31.5)
shot('s08-break', 27.5, 31.5, XBG, [
    colosseum('xray', sag=[{'t': 0.8, 'v': 0.25}, {'t': 2.5, 'v': 1.0, 'ease': 'in'}], pour=[{'t': 0.8, 'v': 0}, {'t': 4.0, 'v': 1}],
              grains=500, sandFront=[{'t': 1.0, 'v': 0}, {'t': 4.0, 'v': round(40 - sand_m(31.5), 2), 'ease': 'linear'}], queueAtM=40),
    kerb('xray', crumble=[{'t': 0, 'v': 0}, {'t': 0.8, 'v': 1}]),
    statue('xray', melt=0.75),
    *xray_queue(sway=1, slump=[{'t': 1.3, 'v': 0.15}, {'t': 2.7, 'v': 1.0, 'ease': 'in'}], heart={'bpm': 70, 'stopAt': 0.0}),
], camera={'preset': 'panUp', 'amount': 0.4, 'shake': [{'at': 1.5, 'duration': 2.5, 'amplitude': 6, 'decay': False}]}, grade=XRAY,
    sfx=[{'cue': 'underwater_rumble', 'at': 0.0, 'volume': 0.5}, {'cue': 'boom', 'at': 0.9, 'volume': 0.4}],
    notes='Textless: kerb crumbles (0-0.8), arcade pours (0.8-2.5), queue folds in a 0.15 s stagger (1.3-2.7), sand tongue slides out (from 1.0). HUD SAND: 39 M AWAY at 29.5.')

# 9 concrete (31.5-35.0)
shot('s09-concrete', 31.5, 35.0, XBG, [
    comp('whatif/ConcreteSection', {'slip': [{'t': 0.2, 'v': 0}, {'t': 3.3, 'v': 1, 'ease': 'in'}], 'limestoneShare': 0.3, 'grains': 160}, x='50%', y=900, width=860, height=860),
], camera={'preset': 'pushIn', 'amount': 0.7}, grade=XRAY,
    sfx=[{'cue': 'static', 'at': 0.2, 'volume': 0.2}],
    notes='Concrete cut: empty dotted binder web, grains slip and pile, some limestone aggregate crumbles.')

# 10 your house (35.0-38.5)
shot('s10-house', 35.0, 38.5, XBG, [
    comp('whatif/House', {'cave': [{'t': 0.3, 'v': 0}, {'t': 2.4, 'v': 1, 'ease': 'in'}], 'row': [{'t': 2.4, 'v': 0}, {'t': 3.5, 'v': 1}]}, x='50%', y=1000, width=1000, height=900),
    comp('explainer/Tag', {'text': 'YOUR HOUSE', 'at': 0.2}, x=540, y=560, width=360, height=80, depth=0.5),
], camera={'keyframes': [{'t': 0, 'zoom': 1.2}, {'t': 2.4, 'zoom': 1.15}, {'t': 3.5, 'zoom': 0.85}]}, grade=XRAY,
    sfx=[{'cue': 'boom', 'at': 0.6, 'volume': 0.5}],
    notes='Generic house on a concrete slab caves in (foundation, mortar, plaster); pull back to a row of them.')

# 11 your heart (38.5-41.5)
ECG = ('<svg viewBox="0 0 800 120" xmlns="http://www.w3.org/2000/svg"><path d="M0 60 L800 60" stroke="#7FE3FF" stroke-width="5" fill="none"/></svg>')
shot('s11-heart', 38.5, 41.5, XBG, [
    comp('whatif/XrayFigure', {'view': 'body', 'slump': 1, 'isYou': True, 'heart': {'bpm': 70, 'stopAt': 0.0}, 'closeUp': 'chest'}, x='50%', y=980, width=1000, height=900, depth=0.6),
    {'type': 'svg', 'markup': ECG, 'x': 470, 'y': 1300, 'width': 800, 'height': 120, 'depth': 0},
], camera={'keyframes': [{'t': 0, 'zoom': 1.0}, {'t': 3, 'zoom': 1.04}]}, grade=XRAY,
    sfx=[{'cue': 'heartbeat_slow', 'at': 0.1, 'volume': 0.5}],
    notes='Back in Rome: YOU heap, chest close-up, still heart outline, flat ECG. Caption: 8.2 billion hearts. HUD: YOUR HEART: 3 BEATS MISSED.')

# 12 white-out (41.5-43.5)
shot('s12-whiteout', 41.5, 43.5, XBG, [
    {'type': 'particles', 'preset': 'dust', 'count': 300, 'color': PALE, 'size': [6, 22], 'speed': 3, 'seed': 11, 'x': '50%', 'y': '50%', 'width': 1080, 'height': 1920},
    {'type': 'rect', 'x': '50%', 'y': '50%', 'width': 1080, 'height': 1920, 'fill': PALE, 'depth': 0, 'z': 40,
     'keyframes': [{'t': 0, 'opacity': 0}, {'t': 1.2, 'opacity': 1, 'ease': 'in'}, {'t': 2.0, 'opacity': 1}]},
], camera={'keyframes': [], 'shake': [{'at': 0.0, 'duration': 0.6, 'amplitude': 14}]}, grade=XRAY,
    sfx=[{'cue': 'whoosh_long', 'at': 0.0, 'volume': 0.6}],
    notes='Pale cyan (not pure white, which means calcium) dust of every city; HUD at 40%.')

# 13 world map (43.5-46.0)
KARST = [(110, 25), (106, 23), (115, 28), (12, 43), (16, 44), (20, 42), (-4, 37), (3, 44), (35, 33), (45, 32), (55, 25), (-81, 28), (-89, 20),
         (-87, 37), (130, -31), (125, -30), (-100, 30), (28, -25), (-5, 33), (8, 34), (37, 37), (44, 40), (60, 40), (100, 15), (120, 15), (-60, -10),
         (-45, -12), (140, -5), (30, 30), (40, 9), (-110, 50), (-75, 45), (100, 55), (80, 60), (-2, 52), (24, 52), (30, 48), (68, 32), (90, 30), (-70, 18)]
shot('s13-world', 43.5, 46.0, {'type': 'color', 'color': '#04121A', 'depth': 0, 'overscan': 1.0}, [
    comp('explainer/Map', {'view': {'lon': 20, 'lat': 15, 'zoom': 1}, 'landColor': '#0C2233', 'strokeColor': CYAN, 'oceanColor': '#061826', 'grid': True,
                           'dots': [{'lon': lo, 'lat': la, 'at': round(0.1 + 0.03 * i, 2), 'r': 7, 'color': CYAN, 'dimTo': 0.25, 'dimAt': round(1.0 + 0.03 * i, 2)} for i, (lo, la) in enumerate(KARST)]},
         x='50%', y='50%', width=1080, height=1920),
], camera={'preset': 'drift', 'amount': 0.3}, transition={'type': 'fade', 'duration': 0.5}, grade=XRAY,
    sfx=[{'cue': 'riser', 'at': 0.0, 'volume': 0.3}],
    notes='Flat world view (equirectangular, zoom 1); carbonate-region dots pulse and dim as LAND CAVING IN climbs.')

# 14 Dover (46.0-48.5)
shot('s14-dover', 46.0, 48.5, XBG, [
    comp('whatif/Strata', {'profile': 'cliff', 'heightM': 110, 'bands': [{'fromM': 0, 'toM': 110, 'label': 'CHALK', 'style': 'solid'}], 'flint': True, 'sea': True,
                           'crumble': [{'t': 0.1, 'v': 0}, {'t': 2.3, 'v': 1, 'ease': 'in'}]}, x='45%', y=1000, width=1000, height=1100),
    comp('explainer/DepthMeter', {'depth': [{'t': 0, 'v': 110}, {'t': 2.3, 'v': 0, 'ease': 'in'}], 'max': 110, 'step': 10, 'window': 120, 'side': 'right', 'suffix': ' M'},
         x=960, y=1000, width=180, height=1000),
], camera={'preset': 'panDown', 'amount': 0.5}, grade=XRAY,
    sfx=[{'cue': 'whoosh', 'at': 0.2, 'volume': 0.4}],
    notes='White Cliffs of Dover (chalk) crumble top-down into a pale plume over the Channel. HUD DOVER CLIFFS 110 -> 0 M.')

# 15 Everest (48.5-52.0)
shot('s15-everest', 48.5, 52.0, XBG, [
    comp('whatif/Strata', {'profile': 'peak', 'summitM': 8849,
                           'bands': [{'fromM': 8600, 'toM': 8849, 'label': 'SEABED LIMESTONE', 'style': 'solid', 'fossils': True},
                                     {'fromM': 8200, 'toM': 8600, 'label': 'YELLOW BAND', 'style': 'half'},
                                     {'fromM': 7000, 'toM': 8200, 'label': '', 'style': 'rock'}],
                           'crumble': [{'t': 0.3, 'v': 0}, {'t': 1.8, 'v': 1, 'ease': 'in'}], 'rival': {'label': 'K2', 'heightM': 8611, 'at': 2.0}},
         x='45%', y=1000, width=1000, height=1100),
    comp('explainer/DepthMeter', {'depth': [{'t': 0, 'v': 8849}, {'t': 1.8, 'v': 8600, 'ease': 'out'}], 'max': 8900, 'step': 50, 'window': 400, 'side': 'right', 'suffix': ' M'},
         x=960, y=1000, width=180, height=1000),
], camera={'keyframes': [{'t': 0, 'y': '55%', 'zoom': 1.0}, {'t': 1.0, 'y': '45%', 'zoom': 1.1}], 'shake': [{'at': 1.0, 'duration': 1.0, 'amplitude': 5}]}, grade=XRAY,
    sfx=[{'cue': 'impact', 'at': 1.0, 'volume': 0.4}, {'cue': 'drone', 'at': 0.0, 'volume': 0.25}],
    notes='Summit band (Qomolangma limestone, fossils) crumbles off; Yellow Band half-dotted (caveat); K2 tick pins in at 2.0, now higher.')

# 16 reef (52.0-55.0)
REEF = [(142.5 + 0.38 * k, -10.7 - 0.46 * k) for k in range(31)]
shot('s16-reef', 52.0, 55.0, {'type': 'color', 'color': '#04121A', 'depth': 0, 'overscan': 1.0}, [
    comp('explainer/Map', {'views': [{'t': 0, 'lon': 147, 'lat': -16, 'zoom': 5}, {'t': 3, 'lon': 149, 'lat': -19, 'zoom': 5.5}],
                           'landColor': '#0C2233', 'strokeColor': CYAN, 'oceanColor': '#061826', 'grid': False,
                           'dots': [{'lon': round(lo, 2), 'lat': round(la, 2), 'at': 0, 'out': round(0.2 + 0.085 * k, 2), 'r': 6, 'color': CYAN} for k, (lo, la) in enumerate(REEF)]},
         x='50%', y='50%', width=1080, height=1920),
], camera={'preset': 'drift', 'amount': 0.2}, grade=XRAY,
    sfx=[{'cue': 'bubbles', 'at': 0.0, 'volume': 0.3}],
    notes='Queensland coast; reef dots go out north to south. HUD REEF COLLAPSED 0 -> 2,300 KM.')

# 17 race wide (55.0-61.0)
HEAPS = dict(sway=1, slump=1, heart={'bpm': 70, 'stopAt': 0.0})
shot('s17-race-wide', 55.0, 61.0, XBG, [
    colosseum('xray', sag=1, pour=1, mound=True, sandFront=[{'t': 0, 'v': round(40 - sand_m(55), 2), 'ease': 'linear'}, {'t': 6, 'v': round(40 - sand_m(61), 2), 'ease': 'linear'}], queueAtM=40),
    kerb('xray', crumble=1),
    statue('xray', melt=0.75),
    *xray_queue(**HEAPS),
], camera={'preset': 'drift', 'amount': 0.2}, transition={'type': 'whip', 'duration': 0.3, 'direction': 'left'}, grade=XRAY,
    sfx=[{'cue': 'clock_ticking', 'at': 0.0, 'volume': 0.4}, {'cue': 'drone', 'at': 0.0, 'volume': 0.3}],
    notes='Rome, low wide over the 9 heaps; the sand tongue creeps in from the right (13 -> 7 m). HUD race: REACHES YOU IN vs ONLINE IN.')

# 18 race tight (61.0-67.0)
shot('s18-race-tight', 61.0, 67.0, XBG, [
    colosseum('xray', sag=1, pour=1, mound=True, sandFront=[{'t': 0, 'v': round(40 - sand_m(61), 2), 'ease': 'linear'}, {'t': 6, 'v': round(40 - sand_m(67), 2), 'ease': 'linear'}], queueAtM=40),
    kerb('xray', crumble=1),
    *xray_queue(**HEAPS),
], camera={'keyframes': [{'t': 0, 'x': QUEUE_X[YOU_I] + 120, 'y': 1220, 'zoom': 1.6}, {'t': 6, 'x': QUEUE_X[YOU_I] + 80, 'y': 1230, 'zoom': 1.9, 'ease': 'linear'}]}, grade=XRAY,
    sfx=[{'cue': 'clock_ticking', 'at': 0.0, 'volume': 0.6}, {'cue': 'heartbeat_fast', 'at': 0.0, 'volume': 0.25}],
    notes='Low tight on YOU heap; sand edge closes 7 -> 1.2 m. Main clock red from 61.0. No caption.')

# 19 return + false resolution (67.0-69.5)
shot('s19-return', 67.0, 69.5, XBG, [
    colosseum('xray', sag=1, pour=1, mound=True, sandFront=[{'t': 0, 'v': round(40 - sand_m(67), 2), 'ease': 'linear'}, {'t': 1.2, 'v': 40, 'ease': 'linear'}], queueAtM=40),
    kerb('xray', crumble=1),
    *xray_queue(**HEAPS),
    {'type': 'rect', 'x': '50%', 'y': 0, 'width': 1080, 'height': 700, 'fill': WHITE, 'opacity': 0, 'blur': 120, 'depth': 0, 'z': 30,
     'keyframes': [{'t': 0, 'opacity': 0}, {'t': 0.15, 'opacity': 0.7}, {'t': 2.5, 'opacity': 0.55}]},
    {'type': 'particles', 'preset': 'dust', 'count': 60, 'color': '#9FB8C4', 'size': [3, 9], 'speed': 1.5, 'seed': 5, 'x': 760, 'y': 1300, 'width': 500, 'height': 160, 'start': 1.2},
], camera={'keyframes': [{'t': 0, 'x': QUEUE_X[YOU_I] + 80, 'y': 1230, 'zoom': 1.9}, {'t': 2.5, 'x': QUEUE_X[YOU_I] + 80, 'y': 1225, 'zoom': 1.92}]},
    transition={'type': 'glitch', 'duration': 0.2}, grade=XRAY,
    sfx=[{'cue': 'stinger', 'at': 0.0, 'volume': 0.7}, {'cue': 'impact', 'at': 1.2, 'volume': 0.3}],
    notes='CALCIUM BACK ONLINE: pure white light floods in from above the frame (the glows are back, but up there). 1.2 s: the sand washes over the heap anyway.')

# 20 twist reveal (69.5-74.5)
shot('s20-twist', 69.5, 74.5, XBG, [
    colosseum('xray', sag=1, pour=1, mound=True, sandFront=40, queueAtM=40),
    comp('whatif/Colosseum', {'mode': 'xray', 'ghost': True, 'glow': 1, 'ghostFall': [{'t': 3.0, 'v': 0}, {'t': 5.0, 'v': 0.2, 'ease': 'in'}]},
         x='50%', y=760, width=1300, height=760, depth=0.4, z=5),
    kerb('xray', crumble=1),
    statue('xray', melt=0.75),
    comp('whatif/Statue', {'mode': 'xray', 'ghost': True, 'glow': 1, 'ghostFall': [{'t': 3.0, 'v': 0}, {'t': 5.0, 'v': 0.2, 'ease': 'in'}]},
         x=1000, y=1120, width=150, height=330, depth=0.7, z=6),
    *xray_queue(**HEAPS),
    *[comp('whatif/XrayFigure', {'view': 'body', 'ghost': True, 'glow': 1, 'slump': 0, 'offsetYM': 1.0,
                                 'ghostFall': [{'t': 3.0, 'v': 0}, {'t': 5.0, 'v': 0.2, 'ease': 'in'}]},
           x=x, y=QUEUE_Y, width=110, height=230, depth=0.8, z=7) for x in QUEUE_X],
], camera={'keyframes': [{'t': 0, 'x': QUEUE_X[YOU_I] + 80, 'y': 1225, 'zoom': 1.4}, {'t': 2.0, 'x': '50%', 'y': '50%', 'zoom': 1.0, 'ease': 'inOut'}]}, grade=XRAY,
    sfx=[{'cue': 'impact', 'at': 1.0, 'volume': 0.5}],
    notes='Camera rises: white ghost skeletons hang upright ~1 m above each heap; ghost bust over its puddle; ghost Colosseum over its sand. Ghosts start to sift down at 3.0. No gore.')

# 21 black (74.5-76.0)
shot('s21-black', 74.5, 76.0, {'type': 'color', 'color': '#000000', 'depth': 0, 'overscan': 1.0}, [], notes='Black, silence, HUD hidden.', hud=False)

# 22 end card (76.0-84.0)
END_FACT = '99% OF YOUR CALCIUM SITS IN BONES AND TEETH.\nTHE REST TRIGGERS YOUR HEARTBEAT.'
shot('s22-endcard', 76.0, 84.0, {'type': 'color', 'color': '#000000', 'depth': 0, 'overscan': 1.0}, [
    comp('whatif/TitleCard', {'pre': 'What if', 'keyword': 'calcium', 'post': 'disappeared for 5 seconds?', 'accent': CYAN, 'font': SERIF, 'iconSvg': TITLE_ICON,
                              'fact': END_FACT, 'factAt': 0.8}, x='50%', y=860, width=960, height=760, depth=0, z=60,
         start=0, end=8.0, enter={'type': 'fade', 'duration': 0.4}),
], sfx=[{'cue': 'ding', 'at': 0.8, 'volume': 0.2}], notes='Exact title repeat (not read) + small-caps fact (not read).', hud=False)

# ------------------------------------------------------------------ assemble
scenes = []
for sh in SHOTS:
    start, end = sh['start'], sh['end']
    dur = round(end - start, 3)
    layers = list(sh['layers'])
    if sh['hud']:
        layers.append(comp('whatif/Hud', {'t0': start, 'lines': HUD, 'opacity': HUD_OPACITY, 'mono': 'JetBrains Mono', 'accent': CYAN},
                           id='hud', x=70, y=250, anchorX=0, anchorY=0, width=860, height=300, depth=0, z=80))
    for cs, ce, text in CAPTIONS:
        if ce <= start or cs >= end:
            continue
        ls, le = max(cs, start) - start, min(ce, end) - start
        cap = {'type': 'text', 'text': text, 'x': '50%', 'y': 1400, 'fontSize': 62, 'font': SERIF, 'weight': 600, 'italic': True,
               'color': '#FFFFFF', 'maxWidth': 860, 'lineHeight': 1.15, 'shadow': '0 3px 14px rgba(0,0,0,.6)',
               'start': round(ls, 3), 'end': round(le, 3), 'depth': 0, 'z': 70}
        if cs >= start:
            cap['enter'] = {'type': 'fade', 'duration': 0.25}
        if ce <= end:
            cap['exit'] = {'type': 'fade', 'duration': 0.25}
        layers.append(cap)
    scene = {'id': sh['id'], 'duration': dur, 'background': sh['background'], 'layers': layers,
             'notes': sh['notes'] + f' [screen {start:.1f}-{end:.1f} s]'}
    if sh['camera']:
        scene['camera'] = sh['camera']
    if sh['transition']:
        scene['transitionIn'] = sh['transition']
    if sh['grade']:
        scene['grade'] = sh['grade']
    if sh['sfx']:
        scene['sfx'] = sh['sfx']
    scenes.append(scene)

storyboard = {
    'version': 1,
    'id': 'whatif-calcium-gone-5-seconds',
    'title': 'What if calcium disappeared for 5 seconds?',
    'format': '9:16',
    'fps': 30,
    'theme': {'fontDisplay': 'Montserrat', 'fontBody': 'Montserrat', 'fontCondensed': 'Anton', 'accent': CYAN, 'ink': NAVY, 'paper': '#FFFFFF'},
    'scenes': scenes,
    'captions': {'enabled': False},
    'audio': {
        'voice': [],
        'music': [
            {'src': 'music/documentary_pulse.m4a', 'start': 0.0, 'end': 7.0, 'volume': 0.14, 'duckTo': 0.08, 'fadeIn': 0.3, 'fadeOut': 0.1},
            {'src': 'music/tension_pulse.m4a', 'start': 7.0, 'end': 74.3, 'volume': 0.22, 'duckTo': 0.1, 'fadeIn': 0.2, 'fadeOut': 0.1},
            {'src': 'music/documentary_pulse.m4a', 'start': 76.0, 'end': 84.0, 'volume': 0.12, 'duckTo': 0.12, 'fadeIn': 0.6, 'fadeOut': 1.0},
        ],
        'sfx': [],
        'duckOn': 'none',
    },
    'overlays': {'grain': 0.03, 'vignette': 0.12, 'fadeIn': 0, 'fadeOut': 0.4},
}

with open(OUT, 'w') as f:
    json.dump(storyboard, f, indent=1, ensure_ascii=False)
    f.write('\n')
total = sum(s['duration'] for s in scenes)
print(f'wrote {OUT}: {len(scenes)} scenes, {total:.2f} s')
