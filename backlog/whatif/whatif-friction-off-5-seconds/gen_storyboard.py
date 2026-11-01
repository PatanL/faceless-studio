#!/usr/bin/env python3
"""Generate storyboard.json for whatif-friction-off-5-seconds from the script's shot list,
caption table and HUD state table (keep in sync with script.md). Output path is argv[1]."""
import json
import sys

OUT = sys.argv[1]

SERIF = '"Source Serif 4", "DejaVu Serif", Georgia, serif'
AMBER = '#FFB547'
WARM_SKY = ['#F2B880', '#F7D9A8']

# ------------------------------------------------------------------ captions (global seconds)
CAPTIONS = [
    (4.5, 7.0, "You're on Lombard Street, San Francisco."),
    (8.0, 11.6, 'Your shoelaces untie themselves.'),
    (11.0, 13.6, 'You glide downhill without taking a step.'),
    (17.0, 20.6, 'Nails hold wood only by friction.'),
    (21.0, 22.6, 'So does every screw.'),
    (26.0, 29.3, 'Cotton thread is 1-inch fibers, twisted tight.'),
    (29.5, 32.8, 'Your shirt unravels into fluff.'),
    (33.0, 36.8, 'No car can brake or steer.'),
    (37.0, 40.0, 'Cable cars grip their cable by friction.'),
    (44.0, 48.0, 'The San Andreas Fault is locked by friction.'),
    (49.0, 51.0, 'In 1906, it slipped about 20 feet.'),
    (62.5, 65.5, 'Everything grips again, just like before.'),
    (66.5, 69.5, 'But nothing that came apart goes back.'),
]

# ------------------------------------------------------------------ HUD state table (global seconds)
# Each line: list of segments {from, to, text} where text may hold one {v} filled from a track.
HUD = {
    'L': [
        {'from': 0, 'to': 7, 'text': 'FRICTION', 'chip': 'on'},
        {'from': 7, 'to': 62, 'text': 'FRICTION', 'chip': 'off'},
        {'from': 62, 'to': 69.5, 'text': 'FRICTION', 'chip': 'on'},
    ],
    'T': [
        {'from': 0, 'to': 7, 'text': 'OFF IN {v} S', 'track': [{'t': 0, 'v': 6.9}, {'t': 6.9, 'v': 0}], 'decimals': 3, 'clampMin': 0},
        {'from': 7, 'to': 62, 'text': 'BACK ON IN {v} S', 'track': [{'t': 7, 'v': 5}, {'t': 62, 'v': 0}], 'decimals': 3},
        {'from': 62, 'to': 69.5, 'text': 'GRIP RESTORED'},
    ],
    'S1': [
        {'from': 0, 'to': 7, 'text': 'EVERY STEP YOU TAKE NEEDS IT'},
        {'from': 7, 'to': 23, 'text': 'SLOW-MO ×11'},
        {'from': 23, 'to': 33, 'text': 'NAILS + SCREWS: BACKING OUT'},
        {'from': 33, 'to': 37, 'text': 'CARS: NO BRAKES · NO STEERING'},
        {'from': 37, 'to': 44, 'text': 'HYDE ST CABLE CAR · 30 RIDERS · SLIDING'},
        {'from': 44, 'to': 51, 'text': 'SAN ANDREAS: SLIPPED {v} FT (EST.)', 'track': [{'t': 44, 'v': 12.5}, {'t': 51, 'v': 14.9}], 'decimals': 0},
        {'from': 51, 'to': 62, 'text': 'PILE-UP AHEAD: {v} FT · IMPACT IN {w} S', 'formula': 'pile_ft = 120 - 4.2*((t-7)/11)^2; impact_s = 5.349 - (t-7)/11', 'wDecimals': 2},
        {'from': 62, 'to': 63, 'text': 'PILE-UP AHEAD: 15 FT'},
        {'from': 63, 'to': 64.2, 'text': 'T+5 S · LOMBARD ST'},
        {'from': 64.2, 'to': 66.2, 'text': 'STOPPING DISTANCE: 66 FT · PILE: 15 FT'},
        {'from': 66.2, 'to': 69.5, 'text': 'IMPACT 25 MPH ≈ A 21-FT FALL'},
    ],
    'S2': [
        {'from': 2, 'to': 7, 'text': 'HILL GRADE 27%'},
        {'from': 7, 'to': 11, 'text': 'AIR DRAG OFF TOO'},
        {'from': 11, 'to': 62, 'text': 'YOU: {v} MPH', 'track': [{'t': 11, 'v': 2.1, 'ease': 'linear'}, {'t': 62, 'v': 28.6, 'ease': 'linear'}], 'decimals': 1},
        {'from': 62, 'to': 66.2, 'text': 'YOU: {v} MPH', 'track': [{'t': 62, 'v': 28.6, 'ease': 'linear'}, {'t': 66.2, 'v': 25.1, 'ease': 'linear'}], 'decimals': 0},
        {'from': 66.2, 'to': 69.5, 'text': 'YOU: 0 MPH'},
    ],
    'S3': [
        {'from': 30, 'to': 62, 'text': 'SHIRTS UNRAVELLED IN SF: {v}', 'track': [{'t': 30, 'v': 0}, {'t': 50, 'v': 808000, 'ease': 'out'}, {'t': 62, 'v': 808000}], 'decimals': 0, 'thousands': True},
        {'from': 67, 'to': 69.5, 'text': 'YOUR SHIRT: IN THE PILE'},
    ],
}

# ------------------------------------------------------------------ shots
FRICTIONLESS = {'hue': -18, 'saturate': 0.75, 'brightness': 1.05, 'contrast': 1.02, 'vignette': 0.15}
WARM = {'saturate': 1.05, 'vignette': 0.12}


def you(x, y, pose, shirt=0.0, w=220, h=360, **kw):
    layer = {
        'type': 'component', 'name': 'explainer/You', 'x': x, 'y': y, 'width': w, 'height': h,
        'props': {'pose': pose, 'color': '#3A8FD6', 'shirt': {'color': '#3A8FD6', 'unravel': shirt}},
    }
    layer.update(kw)
    return layer


def comp(name, props=None, **kw):
    layer = {'type': 'component', 'name': name, 'props': props or {}}
    layer.update(kw)
    return layer


def overlay_cyan():
    return [
        {'type': 'rect', 'x': '50%', 'y': '50%', 'width': 1080, 'height': 1920, 'fill': '#9FE8FF', 'opacity': 0.18, 'blend': 'screen', 'depth': 0, 'z': 40},
        comp('whatif/Streaks', {'opacity': 0.22, 'angle': -28}, x='50%', y='50%', width=1080, height=1920, depth=0, z=41),
    ]


def map_bg(view, palette='golden', **props):
    p = {'view': view, 'palette': palette}
    p.update(props)
    return {'type': 'component', 'name': 'whatif/LombardMap', 'props': p, 'depth': 0.15, 'overscan': 1.25}


def strip_bg(palette='golden', **props):
    p = {'palette': palette, 'slopeDeg': 15.1}
    p.update(props)
    return {'type': 'component', 'name': 'whatif/SlopeStrip', 'props': p, 'depth': 0.3, 'overscan': 1.25}


def card_bg():
    return {'type': 'gradient', 'kind': 'linear', 'angle': 180, 'colors': ['#0E2A33', '#123C47'], 'depth': 0.1, 'overscan': 1.2}


SHOTS = []


def shot(sid, start, end, background, layers=(), camera=None, transition=None, grade=None, sfx=(), notes='', frictionless=False):
    SHOTS.append(dict(id=sid, start=start, end=end, background=background, layers=list(layers), camera=camera,
                      transition=transition, grade=grade, sfx=list(sfx), notes=notes, frictionless=frictionless))


TITLE_ICON = (
    '<svg viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg"><g fill="none" stroke="#FFB547" stroke-width="9" '
    'stroke-linecap="round"><path d="M100 60 C70 10 20 20 30 55 C40 85 80 70 100 60 Z"/>'
    '<path d="M100 60 C130 10 180 20 170 55 C160 85 120 70 100 60 Z"/>'
    '<path d="M100 60 C90 85 70 100 55 112"/><path d="M100 60 C112 85 135 100 150 112"/></g>'
    '<circle cx="100" cy="60" r="10" fill="#FFB547"/></svg>'
)


def title_layers(start, end, enter=True, exit_at=None):
    ls = [
        {'type': 'svg', 'markup': TITLE_ICON, 'x': '50%', 'y': 560, 'width': 200, 'height': 120, 'depth': 0, 'z': 60},
        {'type': 'text', 'text': 'What if', 'x': '50%', 'y': 690, 'fontSize': 92, 'font': SERIF, 'weight': 600, 'color': '#FFFFFF', 'depth': 0, 'z': 60, 'shadow': '0 4px 18px rgba(0,0,0,.45)'},
        {'type': 'text', 'text': 'friction', 'x': '50%', 'y': 800, 'fontSize': 132, 'font': SERIF, 'weight': 700, 'color': AMBER, 'depth': 0, 'z': 60, 'shadow': '0 4px 18px rgba(0,0,0,.45)'},
        {'type': 'text', 'text': 'switched off for 5 seconds?', 'x': '50%', 'y': 910, 'fontSize': 76, 'font': SERIF, 'weight': 600, 'color': '#FFFFFF', 'maxWidth': 900, 'depth': 0, 'z': 60, 'shadow': '0 4px 18px rgba(0,0,0,.45)'},
    ]
    for l in ls:
        l['start'] = start
        l['end'] = end
        if enter:
            l['enter'] = {'type': 'fade', 'duration': 0.4}
        if exit_at is not None:
            l['exit'] = {'type': 'fade', 'at': exit_at, 'duration': end - exit_at}
    return ls


# 1 establishing
shot('s01-establish', 0.0, 4.5, map_bg('low'), [
    comp('explainer/Car', {'color': '#C8453A'}, x=380, y=1120, width=200, height=100, keyframes=[{'t': 0, 'x': 380, 'y': 1120}, {'t': 4.5, 'x': 430, 'y': 1150, 'ease': 'linear'}]),
    comp('explainer/Car', {'color': '#E3B04B'}, x=700, y=880, width=170, height=85, flipX=True, keyframes=[{'t': 0, 'x': 700, 'y': 880}, {'t': 4.5, 'x': 660, 'y': 905, 'ease': 'linear'}]),
    comp('whatif/CableCar', {'riders': 30, 'palette': 'golden'}, x=540, y=330, width=360, height=150, keyframes=[{'t': 0, 'x': 470}, {'t': 4.5, 'x': 610, 'ease': 'linear'}]),
    *title_layers(0.0, 4.5, enter=False, exit_at=4.1),
], camera={'keyframes': [{'t': 0, 'x': '50%', 'y': '50%', 'zoom': 1.0}, {'t': 4.5, 'x': '50%', 'y': '48%', 'zoom': 1.04, 'ease': 'linear'}]},
    grade=WARM, sfx=[{'cue': 'clock_ticking', 'at': 0.0, 'volume': 0.4}],
    notes='Frame 1 = cover. Golden-hour Lombard from below hairpin 6; title clears by 4.5 before caption 1.')

# 2 place you
shot('s02-place-you', 4.5, 7.0, strip_bg(), [
    comp('explainer/Car', {'color': '#7FA7B8'}, id='hatchback', x=300, y=1060, width=300, height=150, rotate=-15.1),
    you(620, 1150, 'stand', rotate=-0.0),
], camera={'preset': 'pushIn', 'amount': 0.5}, grade=WARM,
    sfx=[{'cue': 'tick', 'at': 1.5, 'volume': 0.6}, {'cue': 'tick', 'at': 2.0, 'volume': 0.6}, {'cue': 'tick', 'at': 2.3, 'volume': 0.7}],
    notes='You stand on the brick roadway just below hairpin 5; hatchback parked uphill (the tell).')

# 3 flip
shot('s03-flip', 7.0, 8.0, strip_bg('frictionless'), [
    comp('explainer/Car', {'color': '#7FA7B8', 'wheelsSpin': False}, id='hatchback', x=300, y=1060, width=300, height=150, rotate=-15.1,
         keyframes=[{'t': 0, 'x': 300, 'y': 1060}, {'t': 1.0, 'x': 318, 'y': 1065, 'ease': 'in'}]),
    you(620, 1150, 'stand'),
    *overlay_cyan(),
], camera={'keyframes': [], 'shake': [{'at': 0.0, 'duration': 0.35, 'amplitude': 14}]}, grade=FRICTIONLESS,
    sfx=[{'cue': 'impact', 'at': 0.0, 'volume': 0.9}, {'cue': 'glitch', 'at': 0.0, 'volume': 0.4}],
    notes='Hard cut to the frictionless look; HUD flips to BACK ON IN 5.000 S / SLOW-MO x11 / AIR DRAG OFF TOO.', frictionless=True)

# 4 shoelaces POV
shot('s04-laces', 8.0, 11.0, {'type': 'color', 'color': '#8A4A3A', 'depth': 0.2, 'overscan': 1.3}, [
    comp('whatif/BrickTexture', {'scroll': [{'t': 0, 'v': 0}, {'t': 3, 'v': 45}]}, x='50%', y='50%', width=1350, height=2400, depth=1),
    comp('whatif/ShoePair', {'state': [{'t': 0.3, 'v': 0}, {'t': 2.2, 'v': 1}], 'laceSway': 0.6}, x='50%', y=1000, width=760, height=620),
    *overlay_cyan(),
], camera={'keyframes': [{'t': 0, 'x': '50%', 'y': '46%', 'zoom': 1.0}, {'t': 1.2, 'x': '50%', 'y': '52%', 'zoom': 1.05}, {'t': 3, 'x': '51%', 'y': '53%', 'zoom': 1.07, 'ease': 'linear'}]},
    grade=FRICTIONLESS, sfx=[{'cue': 'whoosh', 'at': 0.3, 'volume': 0.3}],
    notes='POV down at your own shoes: the bows slide open by themselves.', frictionless=True)

# 5 glide
shot('s05-glide', 11.0, 17.0, strip_bg('frictionless', scroll=[{'t': 0, 'v': 0}, {'t': 6, 'v': 170}]), [
    you(520, 1140, 'slide', keyframes=[{'t': 0, 'rotate': 0}, {'t': 6, 'rotate': -9}]),
    comp('explainer/Car', {'color': '#7FA7B8', 'wheelsSpin': False}, x=250, y=1050, width=300, height=150, rotate=-15.1),
    *overlay_cyan(),
], camera={'keyframes': [{'t': 0, 'zoom': 1.0}, {'t': 6, 'zoom': 1.08, 'ease': 'linear'}]}, grade=FRICTIONLESS,
    sfx=[{'cue': 'whoosh_long', 'at': 0.2, 'volume': 0.35}],
    notes='Wonder: gliding at walking pace (2.1 -> 5.2 mph); 13.6-17 textless breather. Everything glides together (same acceleration).', frictionless=True)

# 6 nail / screw diagram
shot('s06-nail-screw', 17.0, 22.0, card_bg(), [
    comp('whatif/DiagramCard', {'kind': 'nail', 'at': 0.0, 'swapTo': 'screw', 'swapAt': 4.0, 'labels': [{'text': 'FRICTION', 'at': 0.3, 'fadeTo0At': 1.2}]},
         x='50%', y=880, width=900, height=900),
    *overlay_cyan(),
], camera={'preset': 'pushIn', 'amount': 0.6}, grade=FRICTIONLESS,
    sfx=[{'cue': 'click', 'at': 1.5, 'volume': 0.5}, {'cue': 'tick', 'at': 4.0, 'volume': 0.6}],
    notes='Caption 4 over the nail sliding out of wood; caption 5 at 21.0 over the screw spinning back out.', frictionless=True)

# 7 row house break (textless from 22.6)
shot('s07-rowhouse', 22.0, 26.0, strip_bg('frictionless'), [
    comp('whatif/RowHouse', {'breakAt': 0.4, 'boards': 9, 'steps': 4, 'bayWindow': True, 'slopeDeg': 15.1}, x=560, y=820, width=900, height=1100),
    *overlay_cyan(),
], camera={'preset': 'panLeft', 'amount': 0.5}, grade=FRICTIONLESS,
    sfx=[{'cue': 'riser', 'at': 0.0, 'volume': 0.35}, {'cue': 'pop', 'at': 1.0, 'volume': 0.3}, {'cue': 'pop', 'at': 1.7, 'volume': 0.3}, {'cue': 'pop', 'at': 2.5, 'volume': 0.3}],
    notes='Textless break: siding boards, porch steps and the bay window slide apart and downhill.', frictionless=True)

# 8 thread diagram
shot('s08-thread', 26.0, 29.5, card_bg(), [
    comp('whatif/DiagramCard', {'kind': 'thread', 'at': 0.0, 'bracket': '1 IN'}, x='50%', y=880, width=900, height=900),
    *overlay_cyan(),
], camera={'preset': 'pullOut', 'amount': 0.6}, grade=FRICTIONLESS, sfx=[{'cue': 'tick', 'at': 0.0, 'volume': 0.6}],
    notes='One thread magnified into short twisted fibres sliding apart.', frictionless=True)

# 9 your shirt
shot('s09-shirt', 29.5, 33.0, strip_bg('frictionless'), [
    {'type': 'component', 'name': 'explainer/You', 'x': 560, 'y': 1180, 'width': 380, 'height': 200,
     'props': {'pose': 'sprawl', 'color': '#3A8FD6', 'shirt': {'color': '#3A8FD6', 'unravel': [{'t': 0.2, 'v': 0}, {'t': 3.0, 'v': 1}]}}},
    comp('whatif/FluffWisps', {'source': 'you', 'at': 0.2, 'count': 40}, x=560, y=1150, width=600, height=300),
    *[{'type': 'component', 'name': 'explainer/You', 'x': x, 'y': y, 'width': 160, 'height': 260, 'scale': 0.8,
       'props': {'pose': 'slide', 'color': c, 'shirt': {'color': c, 'unravel': [{'t': 0.5, 'v': 0}, {'t': 3.2, 'v': 1}]}}}
      for x, y, c in ((220, 980, '#C8453A'), (840, 1260, '#E3B04B'), (380, 1060, '#5DAA6B'))],
    *overlay_cyan(),
], camera={'preset': 'panDown', 'amount': 0.5}, grade=FRICTIONLESS, sfx=[{'cue': 'whoosh', 'at': 0.2, 'volume': 0.3}],
    notes='Personal dip: YOUR shirt unravels (shirt.unravel 0 -> 1); SHIRTS UNRAVELLED IN SF meter starts at 30.0.', frictionless=True)

# 10 cars top-down
shot('s10-cars', 33.0, 37.0, map_bg('high', 'frictionless'), [
    *[comp('whatif/TopDownCar', {'color': c, 'brakeLights': True, 'tyreGlow': (i == 0), 'tyreGlowAt': 0.4, 'tyreFadeAt': 2.4}, x=x0, y=y0, width=110, height=200, rotate=r,
           keyframes=[{'t': 0, 'x': x0, 'y': y0}, {'t': 4, 'x': x0 + 40, 'y': y0 + 520, 'ease': 'in'}])
      for i, (x0, y0, c, r) in enumerate(((420, 600, '#C8453A', 8), (700, 380, '#E3B04B', -22), (300, 260, '#7FA7B8', 30)))],
    *[{'type': 'circle', 'x': x, 'y': y, 'width': 22, 'height': 22, 'fill': '#FF3B30', 'opacity': 0.9, 'blur': 4,
       'keyframes': [{'t': 0, 'x': x, 'y': y}, {'t': 4, 'x': x + 40, 'y': y + 520, 'ease': 'in'}]}
      for x, y in ((392, 696), (448, 696))],
    {'type': 'text', 'text': 'EACH ≈ A POSTCARD', 'x': 640, 'y': 560, 'fontSize': 34, 'font': 'display', 'weight': 800, 'color': AMBER,
     'background': 'rgba(11,13,16,.75)', 'padding': 12, 'radius': 8, 'start': 0.5, 'end': 2.6, 'enter': {'type': 'pop', 'duration': 0.3}, 'exit': {'type': 'fade', 'duration': 0.3}, 'z': 30},
    *overlay_cyan(),
], camera={'keyframes': [{'t': 0, 'x': '50%', 'y': '45%', 'zoom': 1.0, 'rotate': 0}, {'t': 4, 'x': '50%', 'y': '55%', 'zoom': 1.05, 'rotate': 2}]},
    grade=FRICTIONLESS, sfx=[{'cue': 'whoosh_long', 'at': 0.4, 'volume': 0.45}, {'cue': 'impact', 'at': 2.5, 'volume': 0.4}],
    notes='Top-down cars slide straight across the hairpins through a hydrangea bed; brake lights on, no effect; 4 tyre patches glow then go grey.', frictionless=True)

# 11 cable car
shot('s11-cablecar', 37.0, 40.0, strip_bg('frictionless', variant='hyde'), [
    comp('whatif/CableCar', {'riders': 30, 'bell': True}, x=600, y=980, width=760, height=330, rotate=-15.1,
         keyframes=[{'t': 0, 'x': 600, 'y': 980}, {'t': 3, 'x': 520, 'y': 1000, 'ease': 'in'}]),
    comp('whatif/DiagramCard', {'kind': 'cable-grip', 'at': 0.4, 'label': 'CABLE 9.5 MPH', 'inset': True}, x=800, y=560, width=420, height=320,
         enter={'type': 'pop', 'at': 0.4, 'duration': 0.3}),
    *overlay_cyan(),
], camera={'keyframes': [{'t': 0, 'y': '50%', 'zoom': 1.0}, {'t': 3, 'y': '42%', 'zoom': 1.12}]}, grade=FRICTIONLESS,
    sfx=[{'cue': 'ding', 'at': 0.3, 'volume': 0.6}, {'cue': 'ding', 'at': 1.5, 'volume': 0.3}],
    notes='Hyde St cable car with 30 riders slides downhill; inset shows the grip letting go of the 9.5 mph cable.', frictionless=True)

# 12 interrupt
shot('s12-interrupt', 40.0, 43.0, {'type': 'color', 'color': '#0E2A33', 'depth': 0.1, 'overscan': 1.2}, [
    comp('whatif/DebrisField', {'count': 100, 'seed': 7, 'glyphs': ['button', 'nail', 'bolt', 'threadCurl'], 'direction': 'up', 'stretch': 2.2}, x='50%', y='50%', width=1200, height=2100, blur=4),
    {'type': 'rect', 'x': '50%', 'y': '50%', 'width': 1080, 'height': 1920, 'fill': '#FFFFFF', 'depth': 0, 'z': 90,
     'opacity': 0, 'keyframes': [{'t': 0, 'opacity': 0}, {'t': 2.0, 'opacity': 0}, {'t': 2.4, 'opacity': 1, 'ease': 'in'}, {'t': 3.0, 'opacity': 1}]},
    *overlay_cyan(),
], camera={'keyframes': [], 'shake': [{'at': 0.0, 'duration': 1.0, 'amplitude': 10}]}, transition={'type': 'whip', 'duration': 0.3, 'direction': 'down'},
    grade=FRICTIONLESS, sfx=[{'cue': 'whoosh_long', 'at': 0.0, 'volume': 0.6}, {'cue': 'stinger', 'at': 2.0, 'volume': 0.6}],
    notes='Full-frame interrupt: loose buttons, nails and bolts stream past; white flash 42.0-42.4 (rect opacity, not grade).', frictionless=True)

# 13a aerial
shot('s13a-aerial-fault', 43.0, 48.0, map_bg('aerial', 'frictionless', zoom=[{'t': 0, 'v': 1.0}, {'t': 3.2, 'v': 0.35, 'ease': 'inOut'}, {'t': 5, 'v': 0.33}], showFault=True, faultAt=1.2, hillsEmptying=True), [
    *overlay_cyan(),
], camera={'preset': 'drift', 'amount': 0.3}, transition={'type': 'fade', 'duration': 0.4}, grade=FRICTIONLESS,
    notes='Pull out over the city to the San Andreas (red dashed line off the stylised west coast). Map is not to scale.', frictionless=True)

# 13b fault card
shot('s13b-fault-card', 48.0, 51.0, card_bg(), [
    comp('whatif/DiagramCard', {'kind': 'fault', 'at': 0.0, 'brackets': [{'text': '1906: ~20 FT', 'at': 1.0}, {'text': 'NOW: {v} FT (EST.)', 'track': [{'t': 0, 'v': 13.9}, {'t': 3, 'v': 14.9}]}]},
         x='50%', y=880, width=900, height=900),
    *overlay_cyan(),
], camera={'preset': 'pushIn', 'amount': 0.4}, grade=FRICTIONLESS, sfx=[{'cue': 'boom', 'at': 0.2, 'volume': 0.35}],
    notes='Fault cross-section; 1906 offset next to our estimate (speculative, flagged EST.).', frictionless=True)

# 14 chase
CHASE_YOU = {'type': 'component', 'name': 'explainer/You', 'x': 500, 'y': 1250, 'width': 300, 'height': 170, 'rotate': 62,
             'props': {'pose': 'sprawl', 'color': '#3A8FD6', 'shirt': {'color': '#3A8FD6', 'unravel': 1}}}
shot('s14-chase', 51.0, 56.0, map_bg('chase', 'frictionless', follow=[{'t': 0, 'v': 0.0}, {'t': 5, 'v': 0.45}], pile=True, pileAt='lastBend'), [
    dict(CHASE_YOU),
    comp('whatif/FluffPile', {'grow': [{'t': 0, 'v': 0.5}, {'t': 5, 'v': 0.7}]}, x=760, y=360, width=360, height=220, depth=0.6),
    *overlay_cyan(),
], camera={'keyframes': [{'t': 0, 'zoom': 1.0}, {'t': 5, 'zoom': 1.25}]}, grade=FRICTIONLESS,
    sfx=[{'cue': 'heartbeat', 'at': 0.0, 'volume': 0.35}],
    notes='Behind-and-above chase straight down the fall line over hedges and planter beds; pile-up at the garden wall of the last bend. HUD race: IMPACT IN vs BACK ON IN.', frictionless=True)

# 15 tight race
shot('s15-race', 56.0, 62.0, map_bg('chase', 'frictionless', follow=[{'t': 0, 'v': 0.45}, {'t': 6, 'v': 1.0}], pile=True, pileAt='lastBend'), [
    dict(CHASE_YOU),
    comp('whatif/FluffPile', {'grow': [{'t': 0, 'v': 0.7}, {'t': 6, 'v': 1.0}]}, x=700, y=480, width=520, height=320, depth=0.6,
         keyframes=[{'t': 0, 'scale': 1.0}, {'t': 6, 'scale': 1.6}]),
    *overlay_cyan(),
], camera={'preset': 'pushIn', 'amount': 1.0}, grade=FRICTIONLESS,
    sfx=[{'cue': 'heartbeat_fast', 'at': 0.0, 'volume': 0.45}, {'cue': 'clock_ticking', 'at': 3.0, 'volume': 0.4}],
    notes='Wordless race: only the HUD numbers move.', frictionless=True)

# 16a skid start
SKID_YOU = {'type': 'component', 'name': 'explainer/You', 'x': 420, 'y': 1180, 'width': 380, 'height': 200,
            'props': {'pose': 'sprawl', 'color': '#3A8FD6', 'shirt': {'color': '#3A8FD6', 'unravel': 1}}}
shot('s16a-skid', 62.0, 63.0, strip_bg('golden'), [
    dict(SKID_YOU, keyframes=[{'t': 0, 'x': 380}, {'t': 1, 'x': 470, 'ease': 'linear'}]),
    {'type': 'particles', 'preset': 'dust', 'count': 60, 'color': '#C9876F', 'size': [3, 9], 'speed': 2.5, 'seed': 3, 'x': 420, 'y': 1260, 'width': 600, 'height': 160},
], camera={'keyframes': [], 'shake': [{'at': 0.0, 'duration': 0.5, 'amplitude': 16}]}, grade=WARM,
    sfx=[{'cue': 'impact', 'at': 0.0, 'volume': 0.9}],
    notes='GRIP RESTORED. Hard cut to warm; you hit the bricks and skid. Caption 12 (false resolution) at 62.5.')

# 16b bookend
shot('s16b-bookend', 63.0, 64.2, map_bg('low', 'aftermath', carsInBeds=True, sidingDown=True, cableCarGone=True, fluff=True), [
    comp('explainer/Car', {'color': '#C8453A'}, x=300, y=1240, width=200, height=100, rotate=24),
    comp('explainer/Car', {'color': '#E3B04B'}, x=820, y=1010, width=170, height=85, rotate=-31, flipX=True),
], grade=WARM, sfx=[{'cue': 'whoosh', 'at': 0.0, 'volume': 0.25}],
    notes='Re-frame of shot 1, same camera: aftermath. HUD stamp T+5 S · LOMBARD ST.')

# 16c skid toward pile
shot('s16c-skid-pile', 64.2, 66.2, strip_bg('golden', wallAt='right'), [
    dict(SKID_YOU, keyframes=[{'t': 0, 'x': 380}, {'t': 2.0, 'x': 700, 'ease': 'out'}]),
    comp('whatif/FluffPile', {'grow': 1.0}, x=930, y=1120, width=420, height=300),
    {'type': 'particles', 'preset': 'dust', 'count': 40, 'color': '#C9876F', 'size': [3, 8], 'speed': 1.8, 'seed': 5, 'x': 520, 'y': 1260, 'width': 600, 'height': 140},
], camera={'keyframes': [{'t': 0, 'x': '50%'}, {'t': 2.0, 'x': '56%', 'ease': 'out'}]}, grade=WARM,
    sfx=[{'cue': 'heartbeat', 'at': 0.0, 'volume': 0.3}],
    notes='HUD: STOPPING DISTANCE 66 FT · PILE 15 FT; YOU 27 -> 25 MPH.')

# 17 landing
shot('s17-landing', 66.2, 69.5, strip_bg('golden', wallAt='right', damage=True), [
    comp('whatif/FluffPile', {'grow': 1.0, 'burstAt': 0.0}, x=760, y=1110, width=560, height=380),
    {'type': 'component', 'name': 'explainer/You', 'x': 700, 'y': 1080, 'width': 220, 'height': 320,
     'props': {'pose': 'sitUp', 'fallbackPose': 'shrug', 'color': '#3A8FD6', 'shirt': None}, 'start': 0.8, 'enter': {'type': 'pop', 'at': 0.8, 'duration': 0.3}},
    {'type': 'circle', 'x': 520, 'y': 1290, 'width': 28, 'height': 28, 'fill': '#3A8FD6', 'stroke': '#1F4E7A', 'strokeWidth': 3, 'start': 0.6,
     'keyframes': [{'t': 0.6, 'x': 380, 'rotate': 0}, {'t': 2.2, 'x': 520, 'rotate': 540, 'ease': 'out'}]},
], camera={'keyframes': [{'t': 0, 'zoom': 1.15}, {'t': 1.3, 'zoom': 1.15}, {'t': 3.3, 'zoom': 0.95}]}, grade=WARM,
    sfx=[{'cue': 'pop', 'at': 0.0, 'volume': 0.7}, {'cue': 'whoosh', 'at': 0.2, 'volume': 0.3}],
    notes='You plough into the fluff heap (slapstick), sit up shirtless, one button rolls to a stop; pull back on the damaged hill. Caption 13 at 66.5.')

# 18 black
shot('s18-black', 69.5, 71.0, {'type': 'color', 'color': '#000000', 'depth': 0, 'overscan': 1.0}, [], notes='Black, silence, HUD hidden.')

# 19 end card
END_FACT = "ABOUT 20% OF THE WORLD'S ENERGY IS SPENT FIGHTING FRICTION.\nEVERY KNOT YOU'VE EVER TIED DEPENDS ON IT."
shot('s19-endcard', 71.0, 78.0, {'type': 'color', 'color': '#0B0D10', 'depth': 0, 'overscan': 1.0}, [
    *title_layers(0.0, 7.0, enter=True),
    {'type': 'text', 'text': END_FACT, 'x': '50%', 'y': 1120, 'fontSize': 34, 'font': 'display', 'weight': 700, 'color': '#D9DEE3',
     'letterSpacing': 0.08, 'lineHeight': 1.4, 'maxWidth': 860, 'start': 1.0, 'enter': {'type': 'fade', 'duration': 0.6}, 'depth': 0, 'z': 60},
], sfx=[{'cue': 'ding', 'at': 0.0, 'volume': 0.25}], notes='End card: exact title repeat (not read) + fact (not read).')

# ------------------------------------------------------------------ assemble
scenes = []
for sh in SHOTS:
    start, end = sh['start'], sh['end']
    dur = round(end - start, 3)
    layers = list(sh['layers'])
    # HUD on every shot until black
    if start < 69.5:
        layers.append(comp('whatif/Hud', {'t0': start, 'lines': HUD, 'mono': 'JetBrains Mono', 'accent': AMBER},
                           id='hud', x=70, y=250, anchorX=0, anchorY=0, width=820, height=330, depth=0, z=80))
    # captions overlapping this shot
    for cs, ce, text in CAPTIONS:
        if ce <= start or cs >= end:
            continue
        ls, le = max(cs, start) - start, min(ce, end) - start
        cap = {'type': 'text', 'text': text, 'x': '50%', 'y': 1400, 'fontSize': 62, 'font': SERIF, 'weight': 600,
               'color': '#FFFFFF', 'maxWidth': 860, 'lineHeight': 1.15, 'shadow': '0 3px 14px rgba(0,0,0,.6)',
               'start': round(ls, 3), 'end': round(le, 3), 'depth': 0, 'z': 70}
        if cs >= start:
            cap['enter'] = {'type': 'fade', 'duration': 0.25}
        if ce <= end and ce < 69.5:
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
    'id': 'whatif-friction-off-5-seconds',
    'title': 'What if friction switched off for 5 seconds?',
    'format': '9:16',
    'fps': 30,
    'theme': {'fontDisplay': 'Montserrat', 'fontBody': 'Montserrat', 'fontCondensed': 'Anton', 'accent': AMBER, 'ink': '#0B0D10', 'paper': '#FFFFFF'},
    'scenes': scenes,
    'captions': {'enabled': False},
    'audio': {
        'voice': [],
        'music': [
            {'src': 'music/tension_pulse.m4a', 'start': 7.0, 'end': 62.0, 'volume': 0.22, 'duckTo': 0.1, 'fadeIn': 0.3, 'fadeOut': 0.1},
            {'src': 'sfx/drone.wav', 'start': 7.0, 'end': 62.0, 'volume': 0.25, 'duckTo': 0.25, 'fadeIn': 0.2, 'fadeOut': 0.1, 'loop': True},
            {'src': 'sfx/underwater_rumble.wav', 'start': 43.0, 'end': 62.0, 'volume': 0.3, 'duckTo': 0.3, 'fadeIn': 0.5, 'fadeOut': 0.1, 'loop': True},
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
