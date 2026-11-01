#!/usr/bin/env python3
"""Generate storyboard.json for whatif-you-100x-taller from the script's shot list, caption table and
HUD state table (keep in sync with script.md). Output path is argv[1]. All times in the tables below are
GLOBAL seconds; the builder converts them to scene-local times."""
import json
import math
import sys

OUT = sys.argv[1]

SERIF = '"Source Serif 4", "DejaVu Serif", Georgia, serif'
YELLOW = '#FFE14D'
PXM = 3.0          # px per metre in every wide shot (tower 990 px, you 510 px)
GROUND = 1250      # lawn line, px
HIP = (400, GROUND)  # hip pivot in the wide

# ------------------------------------------------------------------ captions (global seconds)
CAPTIONS = [
    (7.3, 10.8, 'You wake up on your back in Paris.'),
    (11.2, 14.3, 'A tourist could stand on your thumbnail.'),
    (14.8, 18.0, 'You groan. Car alarms wail for blocks.'),
    (18.5, 22.0, 'You weigh as much as seven Eiffel Towers.'),
    (22.5, 26.2, 'But your bones only got 10,000 times stronger.'),
    (26.6, 28.9, "That's 100 times the strain."),
    (32.8, 35.9, 'By lunch, your own heat cooks you.'),
    (36.5, 39.7, 'Each breath lifts 100 times too much.'),
    (40.2, 43.2, 'The café across the avenue stays open.'),
    (45.0, 47.3, 'You try to get up.'),
    (48.0, 50.7, 'Your heart outweighs a blue whale.'),
    (60.2, 62.1, 'Fainting saves your legs.'),
    (62.4, 64.8, 'Your head falls 50 metres.'),
]
# VO script (TTS spellings): title at 0.2, then each caption at its start time.
VO_LINES = [(0.2, 'What if you woke up a hundred times taller?')] + [
    (s, t.replace('10,000', 'ten thousand').replace('100', 'a hundred').replace('50 metres', 'fifty metres'))
    for s, _, t in CAPTIONS
]


# ------------------------------------------------------------------ motion formulas
def theta_rise(t):
    """Torso angle (deg) during the push, 54.0-60.0 (matches the 22 deg / 34 deg keyframes)."""
    if t <= 54.0:
        return 0.0
    if t <= 57.0:
        u = (t - 54.0) / 3.0
        return 22.0 * u * u
    if t <= 60.0:
        u = (t - 57.0) / 3.0
        return 22.0 + 12.0 * (1 - (1 - u) ** 2)
    return 34.0


def head_fall(t):
    """Head height (m) during the fall: free fall from 50 m, shown at SLOW-MO x2 from 60.0."""
    tau = max(0.0, (t - 60.0) / 2.0)
    return max(0.0, 50.0 - 4.905 * tau * tau)


def theta_fall(t):
    return math.degrees(math.asin(min(1.0, head_fall(t) / 90.0)))


# ------------------------------------------------------------------ HUD state table (global seconds)
HUD = {
    'L': [
        {'from': 0, 'to': 7, 'text': 'YOU WAKE UP IN'},
        {'from': 7, 'to': 66.4, 'text': 'YOU HAVE LASTED'},
        {'from': 66.4, 'to': 76, 'text': 'YOU LASTED'},
    ],
    'N': [
        {'from': 0, 'to': 7, 'text': '{v} S', 'track': [{'t': 0, 'v': 6.9}, {'t': 6.9, 'v': 0, 'ease': 'linear'}], 'decimals': 1, 'clampMin': 0},
        {'from': 7, 'to': 43.5, 'text': '{clock}', 'clock': {'at': 7, 'start': 0, 'rate': 10}, 'format': 'M MIN SS S'},
        {'from': 43.5, 'to': 60, 'text': '{clock}', 'clock': {'at': 43.5, 'start': 365, 'rate': 1}, 'format': 'M MIN SS S'},
        {'from': 60, 'to': 66.4, 'text': '{clock}', 'clock': {'at': 60, 'start': 381.5, 'rate': 0.5}, 'format': 'M MIN SS S'},
        {'from': 66.4, 'to': 76, 'text': '6 MIN 25 S'},
    ],
    'S1': [
        {'from': 0, 'to': 7, 'text': '170 M TALL'},
        {'from': 7, 'to': 43.5, 'text': 'TIME ×10'},
        {'from': 43.5, 'to': 60, 'text': 'TIME: REAL SPEED'},
        {'from': 60, 'to': 66.4, 'text': 'SLOW-MO ×2'},
    ],
    'S2': [
        {'from': 0, 'to': 7, 'text': 'BUILT FROM THE SAME STUFF'},
        {'from': 7, 'to': 66.4, 'text': 'BEST CASE: ~4 H', 'pulseAt': [32.8]},
        {'from': 66.4, 'to': 76, 'text': 'BEST CASE WAS ~4 H'},
    ],
    'S3': [
        {'from': 7.3, 'to': 11.2, 'text': 'HALF AN EIFFEL TOWER'},
        {'from': 11.2, 'to': 14.8, 'text': 'YOUR THUMBNAIL: 1.5 M WIDE'},
        {'from': 14.8, 'to': 18.5, 'text': 'YOUR VOICE: ~1 HZ · A RUMBLE YOU FEEL'},
        {'from': 18.5, 'to': 22.5, 'text': 'YOUR WEIGHT: 70,000 T (×1,000,000)'},
        {'from': 22.5, 'to': 26.6, 'text': 'BONE STRENGTH: ×10,000'},
        {'from': 29.0, 'to': 32.8, 'text': 'IF YOU STAND: ×100 · BREAKS AT ~×25'},
        {'from': 32.8, 'to': 36.5, 'text': 'CORE TEMP {v} °C · +1.2 °C AN HOUR', 'track': [{'t': 32.8, 'v': 37.0}, {'t': 36.5, 'v': 37.0}], 'decimals': 1},
        {'from': 36.5, 'to': 40.2, 'text': 'BREATHS PER MINUTE: 14 → ~0.5'},
        {'from': 40.2, 'to': 43.5, 'text': 'POLICE EVACUATING THE 7TH'},
        {'from': 51.0, 'to': 54.0, 'text': 'YOUR HEART: ~300 T · PRESSURE STILL 120 MMHG'},
        {'from': 54.0, 'to': 60.0, 'text': 'HEAD HEIGHT: {v} M', 'formula': 'h = 90*sin(theta_rise(t))',
         'track': [{'t': round(t, 2), 'v': round(90 * math.sin(math.radians(theta_rise(t))), 1), 'ease': 'linear'} for t in [54 + i * 0.5 for i in range(13)]], 'decimals': 0},
        {'from': 60.0, 'to': 66.4, 'text': 'HEAD HEIGHT: {v} M', 'formula': 'h = 50 - 4.905*((t-60)/2)^2',
         'track': [{'t': round(t, 2), 'v': round(head_fall(t), 1), 'ease': 'linear'} for t in [60 + i * 0.4 for i in range(16)] + [66.4]], 'decimals': 0},
        {'from': 74.0, 'to': 76.0, 'text': 'THE CAFÉ IS STILL OPEN'},
    ],
    'S4': [
        {'from': 64.8, 'to': 66.4, 'text': 'IMPACT ~110 KM/H · AT NORMAL SIZE: 11 KM/H'},
    ],
    'C2': [
        {'from': 54.0, 'to': 60.0, 'text': 'BLACKOUT IN {v} S', 'sub': 'BLOOD REACHES ~1.5 M UP',
         'track': [{'t': 54.0, 'v': 6.0}, {'t': 60.0, 'v': 0.0, 'ease': 'linear'}], 'decimals': 1, 'warnBelow': 3},
        {'from': 60.0, 'to': 66.4, 'text': 'BLACKOUT', 'color': '#FF4D4D'},
    ],
    'BAR': [
        {'from': 44.0, 'to': 60.0, 'label': 'LEG BONE STRESS', 'redLine': 25, 'max': 30, 'prefix': '×',
         'note': [{'from': 44.0, 'to': 45.0, 'text': 'ON YOUR BACK'}],
         'track': [{'t': 44.0, 'v': 0}, {'t': 45.0, 'v': 0}, {'t': 54.0, 'v': 6, 'ease': 'inOut'}, {'t': 60.0, 'v': 24, 'ease': 'in'}]},
        {'from': 60.0, 'to': 66.4, 'label': 'LEG BONE STRESS', 'redLine': 25, 'max': 30, 'prefix': '×',
         'track': [{'t': 60.0, 'v': 24}, {'t': 60.3, 'v': 0, 'ease': 'out'}], 'tag': {'text': 'LEGS: INTACT', 'color': '#4CD07D'}},
    ],
    'ST': [
        {'from': 69.5, 'to': 76.0, 'text': 'CHAMP DE MARS, 6 MINUTES LATER'},
    ],
}

# ------------------------------------------------------------------ helpers
SHOTS = []


def shot(sid, start, end, background, layers=(), camera=None, transition=None, grade=None, sfx=(), notes=''):
    SHOTS.append(dict(id=sid, start=start, end=end, background=background, layers=list(layers), camera=camera,
                      transition=transition, grade=grade, sfx=list(sfx), notes=notes))


def comp(name, props=None, **kw):
    layer = {'type': 'component', 'name': name, 'props': props or {}}
    layer.update(kw)
    return layer


def paris(palette, **props):
    p = {'palette': palette, 'pxPerM': PXM, 'ground': GROUND, 'tower': {'x': 860}}
    p.update(props)
    return {'type': 'component', 'name': 'whatif/ParisSkyline', 'props': p, 'depth': 0.15, 'overscan': 1.25}


def card_bg():
    return {'type': 'gradient', 'kind': 'linear', 'angle': 180, 'colors': ['#0E2A33', '#123C47'], 'depth': 0.1, 'overscan': 1.2}


def giant(**props):
    p = {'pxPerM': PXM, 'hip': list(HIP), 'headTo': 'left', 'pose': 'back', 'eyes': 'open', 'color': '#3A8FD6'}
    p.update(props)
    return comp('whatif/GiantYou', p, id='you', x=0, y=0, anchorX=0, anchorY=0, width=1080, height=1920)


def track(points, t0):
    return [{'t': round(t - t0, 3), 'v': round(v, 2)} for t, v in points]


def white_flash(at, dur=0.4):
    return {'type': 'rect', 'x': '50%', 'y': '50%', 'width': 1080, 'height': 1920, 'fill': '#FFFFFF', 'depth': 0, 'z': 90,
            'keyframes': [{'t': at, 'opacity': 1}, {'t': at + dur, 'opacity': 0, 'ease': 'out'}]}


# Iris: a huge black square with a soft round hole in the middle. The layer is 14,700 px square so the black
# still covers the frame at scale 0.15 (hole 75 px) and the hole clears the frame at scale 3.0 (hole 1,500 px).
IRIS_SVG = ('<svg viewBox="0 0 1470 1470" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="iris">'
            '<stop offset="0.71" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="1"/>'
            '</radialGradient></defs><path fill="#000" fill-rule="evenodd" d="M0 0H1470V1470H0Z M735 665a70 70 0 1 0 0.01 0Z"/>'
            '<circle cx="735" cy="735" r="70" fill="url(#iris)"/></svg>')


def iris(kfs):
    return {'type': 'svg', 'markup': IRIS_SVG, 'x': '50%', 'y': '50%', 'width': 14700, 'height': 14700, 'depth': 0, 'z': 85,
            'keyframes': kfs}


def shimmer(i):
    path = 'M10 190 C 30 160, -10 130, 10 100 S 30 40, 10 10'
    svg = f'<svg viewBox="0 0 20 200" xmlns="http://www.w3.org/2000/svg"><path d="{path}" fill="none" stroke="#FFD9A0" stroke-width="2" stroke-linecap="round"/></svg>'
    x = 300 + i * 140
    return {'type': 'svg', 'markup': svg, 'x': x, 'y': 1000, 'width': 40, 'height': 400, 'opacity': 0, 'z': 20,
            'keyframes': [{'t': 0.2 * i, 'y': 1050, 'opacity': 0}, {'t': 0.2 * i + 1.2, 'y': 900, 'opacity': 0.5},
                          {'t': 0.2 * i + 3.0, 'y': 760, 'opacity': 0, 'ease': 'in'}]}


def blink(x, y, color, period, phase=0.0, dur=3.7, r=10):
    kfs, t = [], phase
    while t < dur:
        kfs += [{'t': round(t, 2), 'opacity': 1, 'ease': 'step'}, {'t': round(t + period / 2, 2), 'opacity': 0.15, 'ease': 'step'}]
        t += period
    return {'type': 'circle', 'x': x, 'y': y, 'width': r * 2, 'height': r * 2, 'fill': color, 'z': 12, 'keyframes': kfs}


def text(t, x, y, size, color='#FFFFFF', weight=600, **kw):
    layer = {'type': 'text', 'text': t, 'x': x, 'y': y, 'fontSize': size, 'font': SERIF, 'weight': weight, 'color': color,
             'depth': 0, 'z': 60, 'shadow': '0 4px 18px rgba(0,0,0,.45)'}
    layer.update(kw)
    return layer


def title_layers(start, end, fade=True):
    ls = [text('What if you woke up', '50%', 720, 88), text('100 times taller?', '50%', 840, 112, YELLOW, 700)]
    for l in ls:
        l['start'], l['end'] = start, end
        if fade:
            l['enter'] = {'type': 'fade', 'duration': 0.4}
            l['exit'] = {'type': 'fade', 'duration': 0.4}
    return ls


def ring(at, delay, color='#D8C3A0'):
    return {'type': 'circle', 'x': HIP[0] - 200, 'y': GROUND, 'width': 300, 'height': 300, 'fill': 'rgba(0,0,0,0)',
            'stroke': color, 'strokeWidth': 10, 'z': 15, 'opacity': 0,
            'keyframes': [{'t': at + delay, 'scaleX': 0.2, 'scaleY': 0.05, 'opacity': 0.9},
                          {'t': at + delay + 2.4, 'scaleX': 3.2, 'scaleY': 0.7, 'opacity': 0, 'ease': 'out'}]}


# ------------------------------------------------------------------ shots
PREDAWN = {'brightness': 0.82, 'saturate': 0.8, 'hue': -10, 'vignette': 0.15}
SUNRISE = {'saturate': 1.05, 'vignette': 0.1}

# 1 hook (frame 1 = cover)
shot('s01-hook', 0.0, 7.0, paris('predawn'), [
    giant(eyes='closed', breathe={'rate': 0.15, 'amount': 0.02}),
    *title_layers(0.2, 6.6),
], camera={'keyframes': [{'t': 0, 'zoom': 1.0}, {'t': 7.0, 'zoom': 1.03, 'ease': 'linear'}]}, grade=PREDAWN,
    sfx=[{'cue': 'drone', 'at': 0.0, 'volume': 0.35}, {'cue': 'riser', 'at': 4.0, 'volume': 0.5}],
    notes='Frame 1: the full 170 m sleeping giant already on the Champ de Mars, tower past the feet. VO reads the title at 0.2. HUD pre-event clock YOU WAKE UP IN 6.9 S.')

# 2 wake + flip
shot('s02-wake', 7.0, 11.2, paris('sunrise', sunAt=0.0), [
    giant(eyes={'closedUntil': 0.0, 'blinkAt': [1.6]}),
], camera={'keyframes': [{'t': 0, 'zoom': 1.03}], 'shake': [{'at': 0.0, 'duration': 0.3, 'amplitude': 10}]}, grade=SUNRISE,
    sfx=[{'cue': 'impact', 'at': 0.0, 'volume': 0.8}, {'cue': 'tick', 'at': 0.1, 'volume': 0.25}],
    notes='Eyes snap open on the hit; light flips from blue pre-dawn to gold sunrise; HUD flips to YOU HAVE LASTED (TIME x10, BEST CASE ~4 H).')

# 3 POV thumb
POV_PXM = 240
shot('s03-thumb', 11.2, 14.8, {'type': 'gradient', 'kind': 'linear', 'angle': 180, 'colors': ['#F2B880', '#F7D9A8'], 'depth': 0.1, 'overscan': 1.2}, [
    comp('whatif/EiffelTower', {'color': '#B79E8A'}, x=860, y=1500, width=200, height=600, anchorY=1, blur=2, depth=0.3),
    {'type': 'rect', 'x': 620, 'y': 1700, 'width': 2.0 * POV_PXM, 'height': 1500, 'radius': 220, 'fill': '#F4F1EC', 'stroke': '#CFC8BE', 'strokeWidth': 6, 'z': 5,
     'keyframes': [{'t': 0, 'y': 2300}, {'t': 0.6, 'y': 1700, 'ease': 'out'}]},
    {'type': 'circle', 'x': 620, 'y': 1090, 'width': 1.5 * POV_PXM, 'height': 300, 'fill': '#E3DED6', 'stroke': '#CFC8BE', 'strokeWidth': 4, 'z': 6,
     'keyframes': [{'t': 0, 'y': 1690}, {'t': 0.6, 'y': 1090, 'ease': 'out'}]},
    comp('explainer/You', {'pose': 'wave', 'color': '#3A8FD6', 'pxPerM': POV_PXM}, x=620, y=1010, width=260, height=1.75 * POV_PXM, anchorY=1, z=7,
         start=0.6, enter={'type': 'pop', 'duration': 0.3}),
    comp('explainer/ScaleBar', {'label': '1.5 M', 'at': 1.2, 'duration': 0.5, 'from': 'center'}, x=620, y=1190, width=1.5 * POV_PXM, height=60, z=8),
], camera={'preset': 'pushIn', 'amount': 0.6}, grade=SUNRISE,
    sfx=[{'cue': 'whoosh', 'at': 0.0, 'volume': 0.5}, {'cue': 'pop', 'at': 1.5, 'volume': 0.6}],
    notes='POV: white rounded-rect thumb + nail ellipse (core layers) against the sunrise; a 1.75 m tourist waves on the 1.5 m nail at the same pxPerM.')

# 4 car alarms
cars4 = [(260, '#C8453A'), (560, '#E3B04B'), (860, '#5A7D9A')]
shot('s04-alarms', 14.8, 18.5, {'type': 'component', 'name': 'whatif/StreetFacade', 'props': {'palette': 'morning', 'windowJitter': 0.3}, 'depth': 0.15, 'overscan': 1.25}, [
    *[comp('explainer/Car', {'color': c}, x=x, y=1330, width=230, height=110, z=10) for x, c in cars4],
    *[blink(x + dx, 1320, '#FFB13B', 0.5, phase=0.13 * i) for i, (x, _) in enumerate(cars4) for dx in (-95, 95)],
    *[comp('explainer/You', {'pose': 'shrug', 'color': col}, x=x, y=1260, width=110, height=200, anchorY=1, z=11, flipX=(i % 2 == 1),
           idle=[{'type': 'sway', 'amount': 4, 'speed': 0.6, 'phase': 0.2 * i}])
      for i, (x, col) in enumerate([(160, '#6B6B6B'), (420, '#8E7CC3'), (700, '#3F6B3A'), (950, '#B5523B')])],
], camera={'shake': [{'at': 0.0, 'duration': 3.7, 'amplitude': 6, 'frequency': 3, 'rotate': 0.2, 'decay': False}]}, grade=SUNRISE,
    sfx=[{'cue': 'underwater_rumble', 'at': 0.0, 'volume': 0.6}, {'cue': 'notify', 'at': 0.8, 'volume': 0.35},
         {'cue': 'notify', 'at': 1.4, 'volume': 0.3}, {'cue': 'notify', 'at': 2.1, 'volume': 0.3}],
    notes='City reacts: car hazard lights blink out of sync (car_alarm.wav to generate; notify stand-in); pedestrians look around confused (pose shrug, no ear-covering).')

# 5 balance
shot('s05-balance', 18.5, 22.5, card_bg(), [
    comp('explainer/Balance', {
        'left': {'species': 'you', 'silhouette': '#3A8FD6', 'w': 200, 'at': 0.0},
        'right': {'species': 'eiffelTower', 'w': 70, 'count': 7, 'stagger': 0.3, 'at': 0.2, 'drop': True},
        'tilt': [{'t': 0, 'v': -14}, {'t': 2.3, 'v': 0, 'ease': 'out'}],
    }, x='50%', y=1000, width=900, height=700),
    comp('explainer/Stat', {'value': 70000, 'from': 0, 'suffix': ' T', 'label': 'YOUR WEIGHT', 'at': 0.2, 'duration': 2.0, 'size': 96}, x='50%', y=1280, width=800, height=200),
], camera={'preset': 'drift', 'amount': 0.4},
    sfx=[*[{'cue': 'click', 'at': round(0.4 + 0.3 * i, 2), 'volume': 0.5} for i in range(7)], {'cue': 'ding', 'at': 2.5, 'volume': 0.4}],
    notes='Seven Eiffel Towers drop onto the right pan until the beam is level (Balance needs a count prop).')

# 6 rule split
shot('s06-rule', 22.5, 26.6, card_bg(), [
    comp('explainer/Stat', {'value': 1000000, 'prefix': '×', 'label': 'WEIGHT', 'at': 0.1, 'duration': 0.8, 'size': 80, 'box': True}, x=290, y=900, width=460, height=260),
    comp('explainer/Stat', {'value': 10000, 'prefix': '×', 'label': 'BONE STRENGTH', 'at': 1.4, 'duration': 0.8, 'size': 80, 'box': True}, x=790, y=900, width=460, height=260),
    comp('explainer/Tag', {'text': 'SQUARE-CUBE LAW', 'at': 2.2, 'size': 44, 'accent': YELLOW}, x='50%', y=1120, width=700, height=90),
], camera={'preset': 'pushIn', 'amount': 0.3},
    sfx=[{'cue': 'tick', 'at': 0.1, 'volume': 0.5}, {'cue': 'tick', 'at': 1.4, 'volume': 0.5}],
    notes='"But" turn over the two numbers; the law name only in the Tag.')

# 7 femur (textless from 29.0 = local 2.4)
shot('s07-bone', 26.6, 32.8, card_bg(), [
    comp('whatif/Bone', {'bone': 'femur', 'color': '#F4F1EC', 'ghost': True,
                         'crack': [{'t': 0, 'v': 0}, {'t': 2.4, 'v': 0}, {'t': 4.4, 'v': 1, 'ease': 'out'}, {'t': 5.8, 'v': 0, 'ease': 'inOut'}],
                         'tag': {'text': 'IF YOU STAND', 'at': 2.4}}, x='50%', y=1000, width=420, height=1100, rotate=-8),
], camera={'preset': 'pushIn', 'amount': 0.8},
    sfx=[{'cue': 'stinger', 'at': 2.4, 'volume': 0.6}, {'cue': 'drone', 'at': 2.4, 'volume': 0.45}],
    notes='Caption 6 at 26.6, then 3.6 s textless (29.0-32.6): dashed ghost cracks grow along the shaft and retract; nothing breaks yet.')

# 8 heat
shot('s08-heat', 32.8, 36.5, paris('day'), [
    giant(eyes='open', breathe={'rate': 0.08, 'amount': 0.02}),
    *[shimmer(i) for i in range(4)],
], camera={'keyframes': [{'t': 0, 'x': 330, 'y': 1180, 'zoom': 2.2}, {'t': 3.7, 'x': 330, 'y': 1180, 'zoom': 2.35}]},
    grade={'tint': '#FF8A3D', 'tintOpacity': 0.2, 'saturate': 1.05, 'vignette': 0.12},
    sfx=[{'cue': 'drone', 'at': 0.0, 'volume': 0.5}],
    notes='Chest/head crop, four rising sine-stroke shimmer lines (svg layers), warm tint. HUD CORE TEMP; BEST CASE ~4 H pulses once.')

# 9 breath
shot('s09-breath', 36.5, 40.2, paris('day'), [
    giant(eyes='open', breathe={'rate': 0.05, 'amount': 0.05}),
], camera={'keyframes': [{'t': 0, 'x': 420, 'y': 1150, 'zoom': 1.7}, {'t': 3.7, 'x': 440, 'y': 1150, 'zoom': 1.72, 'ease': 'linear'}]}, grade=SUNRISE,
    sfx=[{'cue': 'breath', 'at': 0.2, 'volume': 0.35}, {'cue': 'heartbeat_slow', 'at': 0.0, 'volume': 0.4}],
    notes='Chest rises very slowly. HUD BREATHS PER MINUTE 14 -> ~0.5.')

# 10 cafe plant
POLICE = [{'t': 0, 'x': -200}, {'t': 1.4, 'x': 1300, 'ease': 'linear'}]
shot('s10-cafe', 40.2, 43.5, {'type': 'component', 'name': 'whatif/StreetFacade', 'props': {'palette': 'morning', 'cafe': True}, 'depth': 0.15, 'overscan': 1.25}, [
    comp('explainer/You', {'pose': 'stand', 'color': '#FFFFFF'}, x=640, y=1300, width=120, height=220, anchorY=1, z=11,
         idle=[{'type': 'sway', 'amount': 3, 'speed': 1.2}]),
    {'type': 'rect', 'x': 580, 'y': 1240, 'width': 140, 'height': 12, 'fill': '#8B5A3C', 'z': 10},
    *[comp('explainer/Car', {'color': '#2E4A8C'}, x=-200, y=1420, width=230, height=110, z=12, start=0.4 + 1.1 * i,
           keyframes=[{'t': 0.4 + 1.1 * i + k['t'], 'x': k['x'], **({'ease': k['ease']} if 'ease' in k else {})} for k in POLICE]) for i in range(2)],
], grade=SUNRISE,
    sfx=[{'cue': 'notify', 'at': 0.3, 'volume': 0.4}, {'cue': 'riser', 'at': 0.5, 'volume': 0.15}],
    notes='Deadpan: the waiter keeps wiping; police cars zip past at 10x (siren.wav to generate; riser stand-in). HUD POLICE EVACUATING THE 7TH.')

# 11 white flash
shot('s11-flash', 43.5, 45.0, paris('day'), [
    giant(eyes='open', pose='back', roll=[{'t': 0.4, 'v': 0}, {'t': 1.5, 'v': 0.15}]),
    white_flash(0.0),
], camera={'shake': [{'at': 0.0, 'duration': 0.4, 'amplitude': 18}]}, grade=SUNRISE,
    sfx=[{'cue': 'whoosh_long', 'at': 0.0, 'volume': 0.6}, {'cue': 'boom', 'at': 0.05, 'volume': 0.7}],
    notes='Midpoint (53%): white flash; HUD switches to TIME: REAL SPEED and shows the LEG BONE STRESS bar at x0 (ON YOUR BACK).')

# 12 roll
shot('s12-roll', 45.0, 48.0, paris('day'), [
    giant(eyes='open', pose='side', roll=[{'t': 0, 'v': 0.15}, {'t': 2.0, 'v': 1.0}], knee=[{'t': 1.0, 'v': 0}, {'t': 3.0, 'v': 60}],
          hipLift=[{'t': 1.5, 'v': 0}, {'t': 3.0, 'v': 0.2}]),
    *[comp('explainer/Car', {'color': '#2E4A8C'}, x=x, y=1265, width=24, height=12, z=8,
           keyframes=[{'t': 0, 'x': x}, {'t': 3.0, 'x': x + dx, 'ease': 'out'}]) for x, dx in [(700, 160), (520, -260), (300, -240)]],
], grade=SUNRISE,
    sfx=[{'cue': 'footsteps', 'at': 0.4, 'volume': 0.4}, {'cue': 'heartbeat', 'at': 0.0, 'volume': 0.5}],
    notes='You roll onto your side and draw one knee under you; police cars scatter. Bar x0 -> x2.')

# 13 heart vs whale
shot('s13-heart', 48.0, 51.0, card_bg(), [
    comp('explainer/Balance', {
        'left': {'species': 'whaleHeart', 'w': 260, 'at': 0.0, 'label': 'YOUR HEART ~300 T'},
        'right': {'species': 'blueWhale', 'w': 380, 'at': 0.3, 'drop': True, 'label': 'BLUE WHALE ~150-190 T'},
        'tilt': [{'t': 0.3, 'v': 0}, {'t': 1.4, 'v': -12, 'ease': 'backOut'}],
    }, x='50%', y=1000, width=960, height=700),
], sfx=[{'cue': 'click', 'at': 0.3, 'volume': 0.5}, {'cue': 'ding', 'at': 1.4, 'volume': 0.4}],
    notes='Scale inversion 3.0 s after caption 10: the heart pan goes down. Existing explainer figures (whaleHeart relabelled as your heart).')

# 14 leg planted
shot('s14-plant', 51.0, 54.0, paris('day'), [
    giant(eyes='open', pose='side', roll=1.0, knee=60, hipLift=[{'t': 0, 'v': 0.2}, {'t': 3.0, 'v': 0.35}], hand=True),
], camera={'preset': 'pushIn', 'amount': 0.3}, grade=SUNRISE,
    sfx=[{'cue': 'heartbeat', 'at': 0.0, 'volume': 0.5}],
    notes='HUD line YOUR HEART ~300 T · PRESSURE STILL 120 MMHG (after caption 11 has gone). Bar x4 -> x6.')

# 15 rise, wide
shot('s15-rise', 54.0, 57.0, paris('day'), [
    giant(eyes='open', pose='push', roll=1.0, knee=60, hipLift=0.35, hand=True,
          torsoDeg=track([(t, theta_rise(t)) for t in [54 + i * 0.5 for i in range(7)]], 54.0)),
], camera={'keyframes': [{'t': 0, 'x': 420, 'y': 1150, 'zoom': 1.3}, {'t': 3.0, 'x': 400, 'y': 1060, 'zoom': 1.3, 'ease': 'inOut'}]}, grade=SUNRISE,
    sfx=[{'cue': 'heartbeat_fast', 'at': 0.0, 'volume': 0.6}, {'cue': 'clock_ticking', 'at': 0.0, 'volume': 0.4}],
    notes='Race, textless: torso pivots at the hip 0 -> 22 deg; HEAD HEIGHT climbs; BLACKOUT IN 6.0 counts in real time; bar x6 -> x14.')

# 16 POV race
shot('s16-pov', 57.0, 60.0, paris('day', view='pov', horizon=[{'t': 0, 'v': 1150}, {'t': 3.0, 'v': 1450}]), [
    iris([{'t': 0, 'scale': 3.0}, {'t': 3.0, 'scale': 1.2, 'ease': 'in'}]),
], camera={'keyframes': [{'t': 0, 'zoom': 1.0, 'rotate': 0}, {'t': 3.0, 'zoom': 1.08, 'rotate': 3}]}, grade=SUNRISE,
    sfx=[{'cue': 'heartbeat_fast', 'at': 0.0, 'volume': 0.5}, {'cue': 'heartbeat_slow', 'at': 2.0, 'volume': 0.5}],
    notes='POV from your eyes as you rise (horizon lowers); iris closes; dizzy 3 deg roll. Bar x14 -> x24, BLACKOUT -> 0.')

# 17 faint (false resolution)
shot('s17-faint', 60.0, 62.2, paris('day', view='pov', horizon=1450), [
    iris([{'t': 0, 'scale': 1.2}, {'t': 1.2, 'scale': 0.15, 'ease': 'in'}, {'t': 1.4, 'scale': 0.0}]),
    {'type': 'rect', 'x': '50%', 'y': '50%', 'width': 1080, 'height': 1920, 'fill': '#000000', 'z': 86, 'start': 1.4},
], camera={'keyframes': [{'t': 0, 'y': '50%', 'rotate': 3}, {'t': 2.2, 'y': '56%', 'rotate': 5}]},
    sfx=[{'cue': 'tick', 'at': 0.0, 'volume': 0.4}],
    notes='Blackout. Bar drops to x0, LEGS: INTACT (green); BLACKOUT red; SLOW-MO x2. Caption 12 at 60.2. Audio cuts to one tick then silence.')

# 18 fall (twist)
FALL_T = [62.2 + i * 0.3 for i in range(15)] + [66.4]
shot('s18-fall', 62.2, 66.4, paris('day'), [
    giant(eyes='closed', pose='push', roll=1.0, knee=[{'t': 0, 'v': 60}, {'t': 4.2, 'v': 10}], hipLift=[{'t': 0, 'v': 0.35}, {'t': 4.2, 'v': 0}],
          torsoDeg=track([(t, theta_fall(t)) for t in FALL_T], 62.2), ghosts={'count': 2, 'opacity': 0.3, 'lag': 0.08}),
], camera={'keyframes': [{'t': 0, 'x': 260, 'y': 1000, 'zoom': 1.5}] +
           [{'t': round(t - 62.2, 2), 'x': 260, 'y': round(GROUND - PXM * head_fall(t) * 0.8), 'zoom': 1.5, 'ease': 'linear'} for t in FALL_T[1:]]},
    grade=SUNRISE,
    sfx=[{'cue': 'whoosh_long', 'at': 0.3, 'volume': 0.6}],
    notes='Twist: the faint drops your head 50 m (free fall at SLOW-MO x2, 3.2 s story = 6.4 s screen from 60.0). Caption 13 at 62.4; impact line at 64.8; impact 66.4.')

# 19 silent payoff (frame-1 framing)
shot('s19-impact', 66.4, 74.0, paris('day', roofShake=[{'t': 0, 'v': 1}, {'t': 2.5, 'v': 0}]), [
    giant(eyes='closed', pose='back'),
    ring(0.0, 0.0), ring(0.0, 0.15), ring(0.0, 0.3),
    {'type': 'particles', 'preset': 'dust', 'count': 80, 'color': '#D8C3A0', 'size': [4, 12], 'speed': 2.0, 'seed': 7,
     'x': 220, 'y': 1230, 'width': 500, 'height': 160, 'z': 16, 'keyframes': [{'t': 0, 'opacity': 1}, {'t': 4.0, 'opacity': 0, 'ease': 'in'}]},
    *[blink(x, 1262, '#FFB13B', 0.6, phase=0.2 * i, dur=7.6, r=4) for i, x in enumerate([620, 700, 760])],
], camera={'keyframes': [{'t': 0, 'zoom': 1.03}], 'shake': [{'at': 0.0, 'duration': 1.2, 'amplitude': 28, 'decay': True}]}, grade=SUNRISE,
    sfx=[{'cue': 'boom', 'at': 0.0, 'volume': 0.9}, {'cue': 'impact', 'at': 0.02, 'volume': 0.8}, {'cue': 'underwater_rumble', 'at': 0.1, 'volume': 0.5}],
    notes='7.6 s with no caption or VO, framed exactly like frame 1. HUD YOU LASTED 6 MIN 25 S / BEST CASE WAS ~4 H; stamp at 69.5.')

# 20 cafe button
shot('s20-cafe', 74.0, 76.0, {'type': 'component', 'name': 'whatif/StreetFacade', 'props': {'palette': 'morning', 'cafe': True}, 'depth': 0.15, 'overscan': 1.25}, [
    comp('explainer/You', {'pose': 'stand', 'color': '#FFFFFF'}, x=640, y=1300, width=120, height=220, anchorY=1, z=11,
         idle=[{'type': 'sway', 'amount': 3, 'speed': 1.2}]),
    {'type': 'rect', 'x': 580, 'y': 1240, 'width': 140, 'height': 12, 'fill': '#8B5A3C', 'z': 10},
    {'type': 'rect', 'x': 470, 'y': 1222, 'width': 26, 'height': 24, 'radius': 4, 'fill': '#FFFFFF', 'z': 12,
     'idle': [{'type': 'jitter', 'amount': 2, 'speed': 8}]},
], grade=SUNRISE, sfx=[{'cue': 'click', 'at': 0.5, 'volume': 0.4}, {'cue': 'click', 'at': 1.1, 'volume': 0.3}],
    notes='Bathos: the waiter is still wiping; one cup rattles. HUD THE CAFÉ IS STILL OPEN.')

# 21 black
shot('s21-black', 76.0, 77.0, {'type': 'color', 'color': '#000000', 'depth': 0, 'overscan': 1.0}, [], notes='Black, silence, HUD hidden.')

# 22 end card
END_FACT = 'GALILEO WORKED THIS OUT IN 1638.\nYOU WEIGHED ABOUT 1,000 OF THE BIGGEST DINOSAURS.'
shot('s22-endcard', 77.0, 82.0, {'type': 'color', 'color': '#0B0D10', 'depth': 0, 'overscan': 1.0}, [
    *[dict(l, enter={'type': 'fade', 'duration': 0.4}) for l in title_layers(0.0, 5.0, fade=False)],
    {'type': 'text', 'text': END_FACT, 'x': '50%', 'y': 1080, 'fontSize': 34, 'font': 'display', 'weight': 700, 'color': '#D9DEE3',
     'letterSpacing': 0.08, 'lineHeight': 1.4, 'maxWidth': 860, 'start': 1.0, 'enter': {'type': 'fade', 'duration': 0.6}, 'depth': 0, 'z': 60},
], sfx=[{'cue': 'ding', 'at': 1.0, 'volume': 0.25}], notes='Exact title repeat (not read) + two-line fact (not read). Held so the loop restarts on the matching title.')

# ------------------------------------------------------------------ assemble
scenes = []
for sh in SHOTS:
    start, end = sh['start'], sh['end']
    dur = round(end - start, 3)
    layers = list(sh['layers'])
    if start < 76.0:
        layers.append(comp('whatif/Hud', {'t0': start, 'lines': HUD, 'mono': 'JetBrains Mono', 'accent': YELLOW},
                           id='hud', x=70, y=250, anchorX=0, anchorY=0, width=640, height=420, depth=0, z=80))
    for cs, ce, txt in CAPTIONS:
        if ce <= start or cs >= end:
            continue
        ls, le = max(cs, start) - start, min(ce, end) - start
        cap = {'type': 'text', 'text': txt, 'x': '50%', 'y': 1400, 'fontSize': 62, 'font': SERIF, 'weight': 600,
               'color': '#FFFFFF', 'maxWidth': 860, 'lineHeight': 1.15, 'shadow': '0 3px 14px rgba(0,0,0,.6)',
               'start': round(ls, 3), 'end': round(le, 3), 'depth': 0, 'z': 70}
        if cs >= start:
            cap['enter'] = {'type': 'fade', 'duration': 0.25}
        if ce <= end:
            cap['exit'] = {'type': 'fade', 'duration': 0.25}
        layers.append(cap)
    scene = {'id': sh['id'], 'duration': dur, 'background': sh['background'], 'layers': layers,
             'notes': sh['notes'] + f' [screen {start:.1f}-{end:.1f} s]'}
    for key, field in (('camera', 'camera'), ('transition', 'transitionIn'), ('grade', 'grade'), ('sfx', 'sfx')):
        if sh[key]:
            scene[field] = sh[key]
    scenes.append(scene)

storyboard = {
    'version': 1,
    'id': 'whatif-you-100x-taller',
    'title': 'What if you woke up 100 times taller?',
    'format': '9:16',
    'fps': 30,
    'theme': {'fontDisplay': 'Montserrat', 'fontBody': 'Montserrat', 'fontCondensed': 'Anton', 'accent': YELLOW, 'ink': '#0B0D10', 'paper': '#FFFFFF'},
    'scenes': scenes,
    'captions': {'enabled': False},
    'audio': {
        'voice': [],
        'music': [
            {'src': 'music/documentary_pulse.m4a', 'start': 7.0, 'end': 43.5, 'volume': 0.22, 'duckTo': 0.1, 'fadeIn': 0.4, 'fadeOut': 0.2},
            {'src': 'music/tension_pulse.m4a', 'start': 43.5, 'end': 60.0, 'volume': 0.24, 'duckTo': 0.12, 'fadeIn': 0.1, 'fadeOut': 0.1},
            {'src': 'sfx/drone.wav', 'start': 0.0, 'end': 60.0, 'volume': 0.2, 'duckTo': 0.2, 'fadeIn': 0.5, 'fadeOut': 0.1, 'loop': True},
            {'src': 'music/documentary_pulse.m4a', 'start': 77.0, 'end': 82.0, 'volume': 0.15, 'duckTo': 0.15, 'fadeIn': 0.8, 'fadeOut': 0.6},
        ],
        'sfx': [],
        'duckOn': 'none',
    },
    'overlays': {'grain': 0.03, 'vignette': 0.1, 'fadeIn': 0, 'fadeOut': 0.4},
}

with open(OUT, 'w') as f:
    json.dump(storyboard, f, indent=1, ensure_ascii=False)
    f.write('\n')
with open(OUT.replace('storyboard.json', 'vo_lines.json'), 'w') as f:
    json.dump([{'start': s, 'text': t} for s, t in VO_LINES], f, indent=1, ensure_ascii=False)
    f.write('\n')
total = sum(s['duration'] for s in scenes)
print(f'wrote {OUT}: {len(scenes)} scenes, {total:.2f} s')
