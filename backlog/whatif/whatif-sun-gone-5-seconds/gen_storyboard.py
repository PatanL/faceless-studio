#!/usr/bin/env python3
"""Generate storyboard.json for whatif-sun-gone-5-seconds from the script's shot list, caption list and
HUD state table (keep in sync with script.md). Output path is argv[1].

All live numbers come from the formulas below (same ones as the script's HUD state table and fact file)."""
import json
import sys

OUT = sys.argv[1]
FPS = 30

SERIF = '"Source Serif 4", "DejaVu Serif", Georgia, serif'
AMBER = '#FFB547'
NAVY = '#0B1A3A'

# ------------------------------------------------------------------ physics / clock formulas (screen seconds t)
T_FF = 22.0                     # 30x fast-forward starts (T = 15 s)
T_E = 22.0 + 484 / 30           # 38.1333: shadow reaches Earth (T = 499 s), frame 1144
T_BLACK_END = T_E + 0.5         # 38.6333: HUD back, T = 499.1 s
T_RET = T_E + 25                # 63.1333: light back (T = 504 s), frame 1894
C_MKM = 0.299792458             # million km per light-second


def story_T(t):
    if t < 7:
        return 0.0
    if t <= T_FF:
        return t - 7
    if t <= T_E:
        return 15 + 30 * (t - T_FF)
    if t <= T_RET:
        return 499 + (t - T_E) / 5
    return 504.0


def tau(t):
    return min(5.0, max(0.0, (t - T_E) / 5))


def drift_cm(t):
    return 0.2965 * tau(t) ** 2           # = 0.5 * 0.00593 m/s^2 * tau^2, in cm


def missed_h(t):
    return 2.453 * tau(t)                 # 1.735e17 W x tau s / 7.08e16 J per hour of world energy


def shadow_mkm(t):
    return C_MKM * (499 - story_T(t))


# ------------------------------------------------------------------ captions (global seconds; VO cue + measured Kokoro length)
CAPTIONS = [
    (5.1, 7.0, "You're on Copacabana beach at noon."),
    (8.0, 9.9, 'Nothing happens. Yet.'),
    (10.5, 12.6, 'Your skin still feels warm.'),
    (16.3, 19.4, 'Its light needs 8 minutes 19 seconds.'),
    (20.6, 22.3, 'So does its gravity.'),
    (25.8, 28.6, 'Mercury loses its sunlight first.'),
    (31.5, 34.4, 'The shadow is four Moon-distances thick.'),
    (39.3, 41.6, 'The beach goes black at noon.'),
    (44.0, 46.4, "You can't see your own hand."),
    (49.0, 51.8, 'Earth stops curving and flies straight.'),
    (56.0, 58.8, "It slips a palm's width off course."),
    (63.4, 65.4, 'Light and gravity return.'),
    (65.9, 68.5, "But Earth's orbit stays shifted."),
]

# ------------------------------------------------------------------ HUD state table (global seconds)
lin = 'linear'
HUD = {
    'L': [
        {'from': 0, 'to': 7, 'text': 'SUN VANISHES IN'},
        {'from': 7, 'to': T_RET, 'text': 'SINCE THE SUN VANISHED'},
        {'from': T_RET, 'to': 71, 'text': 'SUN BACK'},
    ],
    'T': [
        {'from': 0, 'to': 7, 'text': '{v}', 'clock': True, 'track': [{'t': 0, 'v': 7}, {'t': 7, 'v': 0, 'ease': lin}], 'decimals': 3},
        {'from': 7, 'to': T_RET, 'text': 'T+{v}', 'suffix': '/ 8:24', 'clock': True, 'formula': 'story_T(t)',
         'track': [{'t': 7, 'v': 0}, {'t': T_FF, 'v': 15, 'ease': lin}, {'t': T_E, 'v': 499, 'ease': lin}, {'t': T_RET, 'v': 504, 'ease': lin}],
         'decimals': 3, 'msBlurAbove': 10},
        {'from': T_RET, 'to': 71, 'text': 'T+8:24.000', 'suffix': '/ 8:24'},
    ],
    'C': [
        {'from': 7, 'to': T_FF, 'text': '1×'},
        {'from': T_FF, 'to': T_E, 'text': '▶▶ 30×'},
        {'from': T_BLACK_END, 'to': T_RET, 'text': 'SLOW-MO 5×'},
        {'from': T_RET, 'to': 71, 'text': '1×'},
    ],
    'S1': [
        {'from': 0, 'to': 7, 'text': 'ONE YEAR: 365.256 DAYS'},
        {'from': 7, 'to': 12, 'text': 'AT THE SUN: BACK IN {v} S', 'track': [{'t': 7, 'v': 5}, {'t': 12, 'v': 0, 'ease': lin}], 'decimals': 1},
        {'from': 12, 'to': 37.97, 'text': 'SHADOW: {v} MILLION KM AWAY', 'formula': '0.299792 * (499 - story_T(t))',
         'track': [{'t': 12, 'v': round(shadow_mkm(12), 3)}, {'t': T_FF, 'v': round(shadow_mkm(T_FF), 3), 'ease': lin}, {'t': T_E, 'v': 0, 'ease': lin}], 'decimals': 1},
        {'from': 37.97, 'to': T_E, 'text': 'SHADOW: HERE'},
        {'from': T_BLACK_END, 'to': T_RET, 'text': 'SHADOW HERE · LIGHT BACK IN {v} S', 'formula': '5 - tau',
         'track': [{'t': T_BLACK_END, 'v': 4.9}, {'t': T_RET, 'v': 0, 'ease': lin}], 'decimals': 1},
        {'from': T_RET, 'to': 68.3, 'text': 'COPACABANA, 8 MIN 24 S LATER'},
        {'from': 68.3, 'to': 71, 'text': 'YOUR YEAR NOW: 365.256 DAYS + 47 µS. FOREVER.', 'accent': True},
    ],
    'S2': [
        {'from': 2, 'to': 7, 'text': 'SUNLIGHT ON YOU: 1,000 W/M²'},
        {'from': 7, 'to': 10.3, 'text': 'SUNLIGHT ON YOU: 1,000 W/M² · STILL ARRIVING'},
        {'from': 10.3, 'to': T_FF, 'text': 'THE LIGHT ON YOUR SKIN: 8 MIN OLD'},
        {'from': 27.94, 'to': 33.53, 'text': 'MERCURY: DARK AT T+3:13'},
        {'from': 33.53, 'to': T_E, 'text': 'VENUS: DARK AT T+6:01'},
        {'from': T_BLACK_END, 'to': 41, 'text': 'SUNLIGHT ON YOU: 0 W/M² · SOLAR: 0', 'accent': True},
        {'from': 41, 'to': T_RET, 'text': 'MISSED SUNLIGHT: {v} HRS OF ALL HUMAN ENERGY', 'formula': '2.453 * tau',
         'track': [{'t': 41, 'v': round(missed_h(41), 3)}, {'t': T_RET, 'v': 12.27, 'ease': lin}], 'decimals': 1},
        {'from': T_RET, 'to': 66.7, 'text': 'MISSED: 12 HOURS OF ALL HUMAN ENERGY'},
    ],
    'S3': [
        {'from': 49, 'to': T_RET, 'text': 'OFF ORBIT BY {v} CM', 'formula': '0.2965 * tau^2',
         'track': [{'t': round(x, 3), 'v': round(drift_cm(x), 3), 'ease': lin} for x in [49 + 0.5 * i for i in range(29)] + [T_RET]], 'decimals': 1},
        {'from': T_RET, 'to': 66.7, 'text': 'OFF ORBIT BY 7.4 CM'},
        {'from': 66.7, 'to': 71, 'text': 'THAT 7.4 CM BECOMES 149 KM IN 3 MONTHS', 'accent': True},
    ],
}
HUD_HIDDEN = [(T_E, T_BLACK_END), (71.0, 80.0)]


def comp(name, props=None, **kw):
    layer = {'type': 'component', 'name': name, 'props': props or {}}
    layer.update(kw)
    return layer


def you(x, y, pose, start=None, end=None, w=200, h=330, **kw):
    layer = comp('explainer/You', {'pose': pose, 'color': '#3A8FD6'}, x=x, y=y, width=w, height=h, **kw)
    if start is not None:
        layer['start'] = start
    if end is not None:
        layer['end'] = end
    return layer


def text(t, x, y, size, color='#FFFFFF', start=None, end=None, weight=700, font='display', spacing=0.08, z=55, **kw):
    layer = {'type': 'text', 'text': t, 'x': x, 'y': y, 'fontSize': size, 'font': font, 'weight': weight, 'color': color,
             'letterSpacing': spacing, 'depth': 0, 'z': z, 'shadow': '0 2px 8px rgba(0,0,0,.6)'}
    if start is not None:
        layer['start'] = start
        layer['enter'] = {'type': 'fade', 'duration': 0.3}
    if end is not None:
        layer['end'] = end
    layer.update(kw)
    return layer


def top_panel(props, **kw):
    p = {'clip': True}
    p.update(props)
    return comp('whatif/SolarMap', p, id='solarmap-top', x=540, y=384, width=1080, height=768, depth=0, z=5, **kw)


def beach_panel(props=None, **kw):
    p = {'mode': 'day', 'clip': True, 'ghostSun': {'x': 0.82, 'y': 0.12, 'r': 46}}
    p.update(props or {})
    box = {'id': 'beach-bottom', 'x': 540, 'y': 1344, 'width': 1080, 'height': 1152, 'depth': 0, 'z': 5}
    box.update(kw)
    return comp('whatif/BeachNoon', p, **box)


SEAM = {'type': 'rect', 'x': 540, 'y': 768, 'width': 1080, 'height': 4, 'fill': '#FFFFFF', 'opacity': 0.55, 'depth': 0, 'z': 50}


def title_layers(start, end, exit_at=None, enter=False):
    ls = [
        {'type': 'text', 'text': 'What if', 'x': '50%', 'y': 990, 'fontSize': 92, 'font': SERIF, 'weight': 600, 'color': '#FFFFFF'},
        {'type': 'text', 'text': 'the Sun', 'x': '50%', 'y': 1100, 'fontSize': 132, 'font': SERIF, 'weight': 700, 'color': AMBER},
        {'type': 'text', 'text': 'vanished for 5 seconds?', 'x': '50%', 'y': 1210, 'fontSize': 80, 'font': SERIF, 'weight': 600, 'color': '#FFFFFF', 'maxWidth': 900},
    ]
    for l in ls:
        l.update({'start': start, 'end': end, 'depth': 0, 'z': 60, 'shadow': '0 4px 18px rgba(0,0,0,.5)'})
        if enter:
            l['enter'] = {'type': 'fade', 'duration': 0.4}
        if exit_at is not None:
            l['exit'] = {'type': 'fade', 'at': exit_at, 'duration': end - exit_at}
    return ls


def dark_overlay(keyframes=None, z=20):
    l = {'type': 'rect', 'id': 'night', 'x': '50%', 'y': '50%', 'width': 1080, 'height': 1920, 'fill': NAVY, 'blend': 'multiply', 'depth': 0, 'z': z}
    if keyframes:
        l['keyframes'] = keyframes
    return l


def lit_city(fade_at=None):
    """Sparse lit office windows along the promenade, phone screens on the sand, headlights (honest noon-dark lights)."""
    ls = []
    for i, (x, y) in enumerate([(70, 930), (130, 905), (205, 940), (300, 915), (365, 950), (470, 925), (560, 900), (650, 945), (720, 915), (830, 935), (905, 905), (990, 940)]):
        ls.append({'type': 'rect', 'x': x, 'y': y, 'width': 22, 'height': 30, 'fill': AMBER, 'opacity': 0.95, 'z': 30, 'blur': 1})
    for i in range(30):
        x = 90 + (i * 137) % 900
        y = 1330 + (i * 89) % 420
        ls.append({'type': 'rect', 'x': x, 'y': y, 'width': 14, 'height': 24, 'fill': '#CFE3FF', 'radius': 3, 'z': 31, 'blur': 1.5,
                   'start': round(0.15 * i % 3.2, 2), 'enter': {'type': 'fade', 'duration': 0.2}})
    for i, x in enumerate([180, 420, 640, 880]):
        for dx in (-14, 14):
            ls.append({'type': 'circle', 'x': x + dx, 'y': 1065, 'width': 16, 'height': 16, 'fill': '#FFF6D8', 'z': 31, 'blur': 3})
    if fade_at is not None:
        for l in ls:
            l['exit'] = {'type': 'fade', 'at': fade_at, 'duration': 0.4}
    return ls


SHOTS = []


def shot(sid, start, end, background, layers=(), camera=None, transition=None, sfx=(), notes=''):
    SHOTS.append(dict(id=sid, start=start, end=end, background=background, layers=list(layers), camera=camera,
                      transition=transition, sfx=list(sfx), notes=notes))


BLACK = {'type': 'color', 'color': '#000000', 'depth': 0, 'overscan': 1.0}
SPACE = {'type': 'color', 'color': '#05070D', 'depth': 0.1, 'overscan': 1.2}

# 1 split hook
shot('s01-split-hook', 0.0, 7.0, BLACK, [
    top_panel({'mode': 'sunClose', 'sunScale': 1, 'stars': 18}),
    beach_panel({'zoom': [{'t': 0, 'v': 1.0}, {'t': 7, 'v': 1.03, 'ease': lin}]}),
    you(300, 1560, 'stand', shadow='6px 4px 0 rgba(0,0,0,.35)'),
    SEAM,
    text('SUN · 149.6 MILLION KM AWAY', 540, 720, 28, color='#D9DEE3', start=1.0),
    *title_layers(0.0, 5.0, exit_at=4.7),
], sfx=[{'cue': 'tick', 'at': 4.0, 'volume': 0.5}, {'cue': 'tick', 'at': 5.0, 'volume': 0.55}, {'cue': 'tick', 'at': 6.0, 'volume': 0.6}],
    notes='Frame 0 = cover. Two vantages: the Sun close up (top 40%) and Copacabana at noon (bottom 60%) with a small Sun in its sky. Title in the beach sky, clear of the seam; clears at 5.0 before caption 1.')

# 2 event
shot('s02-event', 7.0, 12.0, BLACK, [
    top_panel({'mode': 'sunClose', 'sunScale': [{'t': 0, 'v': 1}, {'t': 0.067, 'v': 0, 'ease': 'in'}], 'stars': 18, 'emptyMarker': True}),
    {'type': 'circle', 'x': 540, 'y': 384, 'width': 300, 'height': 300, 'fill': 'rgba(0,0,0,0)', 'stroke': '#FFFFFF', 'strokeWidth': 10, 'depth': 0, 'z': 8,
     'keyframes': [{'t': 0, 'scale': 0.6, 'opacity': 1}, {'t': 0.5, 'scale': 2.2, 'opacity': 0, 'ease': 'out'}]},
    beach_panel({'zoom': 1.03}),
    you(300, 1560, 'stand', end=1.0),
    you(300, 1560, 'shrug', start=1.0),
    comp('whatif/Hand', {'look': 'warm', 'over': 'sand', 'shimmer': True}, x=850, y=1640, width=300, height=300, depth=0, z=40, start=3.5,
         enter={'type': 'pop', 'duration': 0.3}, shadow='0 6px 20px rgba(0,0,0,.4)'),
    SEAM,
    text('AT THE SUN', 540, 720, 30, color='#D9DEE3'),
    text('COPACABANA · YOUR VIEW', 540, 810, 30, color='#FFFFFF'),
    text('STILL SHINING. STILL PULLING.', 760, 1000, 30, color=AMBER, start=1.5),
], sfx=[{'cue': 'impact', 'at': 0.0, 'volume': 0.9}],
    notes='Only the AT THE SUN panel changes: white ring + disc gone in 2 frames (no shake: core shake moves the whole frame). The beach is untouched; ghost Sun labelled at 8.5. POV hand inset 10.5-12.0.')

# 3 sun back, top pull-out
shot('s03-sun-back', 12.0, 22.0, BLACK, [
    top_panel({'mode': 'sunClose', 'sunScale': [{'t': 0, 'v': 0}, {'t': 0.3, 'v': 1, 'ease': 'backOut'}], 'stars': 18,
               'zoom': [{'t': 0, 'v': 1.0}, {'t': 1.0, 'v': 1.0}, {'t': 10, 'v': 0.35, 'ease': 'inOut'}],
               'orbits': ['mercury', 'venus'], 'band': {'storyT0': 5.0, 'storyT1': 15.0}}),
    beach_panel({'zoom': 1.03}),
    you(300, 1560, 'stand'),
    SEAM,
    text('AT THE SUN: BACK', 540, 720, 30, color='#D9DEE3', start=0.0),
    text('COPACABANA · YOUR VIEW', 540, 810, 30, color='#FFFFFF'),
], sfx=[{'cue': 'pop', 'at': 0.0, 'volume': 0.6}],
    notes='Sun pops back at the source (T = 5 s). The top panel pulls out (its own zoom track) to show the dark ring leaving the Sun. HUD S1 becomes SHADOW: N MILLION KM AWAY on the same frame.')

# 4 shell ladder, full frame
D4 = T_E - T_FF
shot('s04-shell-ladder', T_FF, T_E, SPACE, [
    comp('whatif/SolarMap', {
        'mode': 'inner', 'clip': True, 'wash': {'color': '#FFD58A', 'opacity': 0.22},
        'storyT': [{'t': 0, 'v': 15}, {'t': D4, 'v': 499, 'ease': lin}],
        'band': {'thicknessLs': 5, 'exaggerate': 12, 'edgeColor': '#FFFFFF', 'edgeWidth': 3},
        'planets': [{'name': 'mercury', 'greyAt': 5.94}, {'name': 'venus', 'greyAt': 11.53}, {'name': 'earth', 'pin': 'YOU'}],
        'zoom': [{'t': 0, 'v': 0.35}, {'t': 11.0, 'v': 0.12, 'ease': 'inOut'}, {'t': 14.0, 'v': 0.12}, {'t': D4, 'v': 0.5, 'ease': 'in'}],
        'focus': [{'t': 14.0, 'v': 'sun'}, {'t': D4, 'v': 'earth'}],
    }, x='50%', y='50%', width=1080, height=1920, depth=0, z=5),
    {'type': 'particles', 'preset': 'stars', 'count': 140, 'color': '#FFFFFF', 'size': [1, 3], 'speed': 0.2, 'seed': 4, 'x': '50%', 'y': '50%', 'width': 1080, 'height': 1920, 'z': 1},
    comp('explainer/ScaleBar', {'at': 0.0, 'duration': 0.6, 'label': '1.5 MILLION KM', 'color': '#FFFFFF', 'from': 'left', 'labelSize': 34},
         x=560, y=1180, width=420, height=120, start=9.5, end=14.0, depth=0, z=30),
    *[{'type': 'rect', 'x': 350 + 105 * i, 'y': 1180, 'width': 4, 'height': 26, 'fill': '#FFFFFF', 'start': 9.9, 'end': 14.0, 'depth': 0, 'z': 31,
       'enter': {'type': 'fade', 'duration': 0.2}} for i in range(1, 5)],
    text('4 MOON-DISTANCES', 560, 1230, 26, color='#D9DEE3', start=10.0, end=14.0, z=31),
    {'type': 'rect', 'x': '50%', 'y': '50%', 'width': 1080, 'height': 1920, 'fill': '#FFFFFF', 'depth': 0, 'z': 90, 'opacity': 0,
     'keyframes': [{'t': 0, 'opacity': 0}, {'t': round(D4 - 0.1, 4), 'opacity': 0}, {'t': round(D4 - 0.0667, 4), 'opacity': 0.85, 'ease': 'step'}, {'t': D4, 'opacity': 0.85}]},
], transition={'type': 'whip', 'duration': 0.3, 'direction': 'up'},
    sfx=[{'cue': 'whoosh_long', 'at': 0.0, 'volume': 0.55}, {'cue': 'ding', 'at': 5.94, 'volume': 0.35}, {'cue': 'ding', 'at': 11.53, 'volume': 0.35},
         {'cue': 'riser', 'at': 13.5, 'volume': 0.5}],
    notes='Sunlight is a pale amber wash; the 5-light-second gap is a dark band with bright edges, so it reads on black. Mercury greys at 27.94, Venus at 33.53; YOU pin on Earth. Last 2 frames: white rim flash, then cut to black.')

# 5 interrupt
shot('s05-interrupt', T_E, T_BLACK_END, BLACK, [], notes='0.5 s pure black, HUD hidden, 0.4 s hard silence.')

# 6 dark beach
shot('s06-beach-dark', T_BLACK_END, 44.0, BLACK, [
    beach_panel({'zoom': 1.0, 'fullFrame': True, 'ghostSun': None}, x='50%', y='50%', width=1080, height=1920),
    dark_overlay(),
    *lit_city(),
    you(300, 1560, 'panic', z=32, shadow='0 0 0 rgba(0,0,0,0)'),
], camera={'preset': 'drift', 'amount': 0.4},
    sfx=[{'cue': 'heartbeat_slow', 'at': 1.5, 'volume': 0.4}],
    notes='Navy multiply rect over the day art (no scene grade, so lights above it stay at full strength). Lit: sparse office windows, phone screens on the sand, headlights. No stars: eyes cannot dark-adapt in 5 s.')

# 7 hand in the dark
shot('s07-hand', 44.0, 48.0, {'type': 'color', 'color': '#04060C', 'depth': 0, 'overscan': 1.0}, [
    comp('whatif/Hand', {'look': 'dashed'}, x=540, y=1050, width=700, height=760, opacity=0.15, z=10),
    {'type': 'circle', 'x': 600, 'y': 820, 'width': 380, 'height': 300, 'fill': '#8FE3B0', 'blur': 60, 'z': 12, 'blend': 'screen',
     'keyframes': [{'t': 0, 'x': 600, 'y': 820, 'opacity': 0.75}, {'t': 4, 'x': 520, 'y': 880, 'opacity': 0.2, 'ease': 'out'}]},
    {'type': 'circle', 'x': 640, 'y': 800, 'width': 200, 'height': 160, 'fill': '#E07AD8', 'blur': 40, 'z': 13, 'blend': 'screen',
     'keyframes': [{'t': 0, 'opacity': 0.6}, {'t': 4, 'opacity': 0.1, 'ease': 'out'}]},
], camera={'preset': 'pushIn', 'amount': 0.3}, sfx=[{'cue': 'heartbeat_slow', 'at': 0.2, 'volume': 0.45}],
    notes='POV: you cannot see your hand; a faint dashed outline marks where it is, and an afterimage of the bright beach drifts and fades.')

# 8 tangent drift
shot('s08-tangent', 48.0, 56.0, SPACE, [
    {'type': 'particles', 'preset': 'stars', 'count': 220, 'color': '#FFFFFF', 'size': [1, 3], 'speed': 0.15, 'seed': 9, 'x': '50%', 'y': '50%', 'width': 1080, 'height': 1920, 'z': 1},
    comp('whatif/SolarMap', {'mode': 'earthClose', 'clip': True, 'orbitArc': {'color': AMBER, 'dashed': True}, 'tangent': {'color': '#FFFFFF', 'glow': True},
                             'moon': True, 'bandTrailingEdge': {'from': 0.0, 'to': 1.0}, 'label': 'NO PULL', 'labelAt': 1.0}, x='50%', y='50%', width=1080, height=1920, z=5),
], camera={'preset': 'pushIn', 'amount': 0.5}, sfx=[{'cue': 'whoosh', 'at': 1.0, 'volume': 0.3}],
    notes='Bright diagram after the dark beach: Earth carries straight on along its tangent while the orbit arc curves away; the band trailing edge closes in from the Sun side.')

# 9 palm vs drift
PX_PER_CM = 81.0
BAR_W = 7.41 * PX_PER_CM
t9 = [56.0 + 0.5 * i for i in range(15)] + [T_RET]
bar_kf = [{'t': round(x - 56.0, 4), 'scaleX': round(drift_cm(x) / 7.41, 4), 'ease': lin} for x in t9]
line_kf = [{'t': round(x - 56.0, 4), 'y': round(1300 - drift_cm(x) * PX_PER_CM, 1), 'ease': lin} for x in t9]
shot('s09-palm', 56.0, T_RET, {'type': 'gradient', 'kind': 'linear', 'angle': 180, 'colors': ['#0B1A3A', '#10264F'], 'depth': 0.1, 'overscan': 1.2}, [
    comp('whatif/Hand', {'look': 'bright', 'palmWidthPx': 8 * PX_PER_CM}, x=540, y=820, width=760, height=820, z=10),
    {'type': 'svg', 'markup': '<svg viewBox="0 0 1000 10" xmlns="http://www.w3.org/2000/svg"><line x1="0" y1="5" x2="1000" y2="5" stroke="#FFFFFF" stroke-width="4" stroke-dasharray="24 16"/></svg>',
     'x': 540, 'y': 1300, 'width': 1000, 'height': 10, 'z': 20},
    text('OLD ORBIT', 180, 1335, 26, color='#D9DEE3', z=21),
    {'type': 'rect', 'x': 540, 'y': 1300, 'width': 1000, 'height': 6, 'fill': '#4FB3FF', 'z': 22, 'keyframes': line_kf},
    text('EARTH', 180, 1200, 26, color='#4FB3FF', z=21, keyframes=[{'t': k['t'], 'y': k['y'] - 35, 'ease': lin} for k in line_kf]),
    {'type': 'rect', 'x': 240, 'y': 1480, 'anchorX': 0, 'width': round(BAR_W, 1), 'height': 22, 'fill': AMBER, 'radius': 4, 'z': 25, 'keyframes': bar_kf},
], camera={'preset': 'pushIn', 'amount': 0.3},
    sfx=[{'cue': 'tick', 'at': 0.50, 'volume': 0.6}, {'cue': 'tick', 'at': 2.67, 'volume': 0.6}, {'cue': 'tick', 'at': 4.63, 'volume': 0.6}, {'cue': 'tick', 'at': 6.43, 'volume': 0.7}],
    notes='Drift bar and orbit-line gap follow the HUD formula 0.2965*tau^2 (3.79 cm at 56.0 -> 7.41 cm at 63.13); ticks at 4/5/6/7 cm.')

# 10 return
D10 = round(65.9 - T_RET, 4)
shot('s10-return', T_RET, 65.9, BLACK, [
    beach_panel({'zoom': 1.0, 'fullFrame': True}, x='50%', y='50%', width=1080, height=1920),
    dark_overlay(keyframes=[{'t': 0, 'x': '50%'}, {'t': 0.3, 'x': '150%', 'ease': 'in'}]),
    *lit_city(fade_at=0.2),
    you(300, 1560, 'panic', end=0.4, z=32),
    you(300, 1560, 'wave', start=0.4, z=32),
], camera={'preset': 'pullOut', 'amount': 0.4}, sfx=[{'cue': 'whoosh', 'at': 0.0, 'volume': 0.5}],
    notes='Light sweeps back: the navy rect slides off to the right in 0.3 s. SUN BACK / COPACABANA, 8 MIN 24 S LATER. Caption 12 at 63.4.')

# 11 orbit twist
shot('s11-orbit-twist', 65.9, 71.0, SPACE, [
    {'type': 'particles', 'preset': 'stars', 'count': 160, 'color': '#FFFFFF', 'size': [1, 3], 'speed': 0.1, 'seed': 12, 'x': '50%', 'y': '50%', 'width': 1080, 'height': 1920, 'z': 1},
    comp('whatif/SolarMap', {'mode': 'fullOrbit', 'clip': True, 'oldOrbit': {'color': '#FFFFFF', 'dashed': True}, 'newOrbit': {'color': AMBER},
                             'offsetExaggerate': 3000, 'offsetLabel': 'UP TO 149 KM', 'offsetLabelAt': 0.8, 'planets': [{'name': 'earth', 'pin': 'YOU'}]},
         x='50%', y='50%', width=1080, height=1920, z=5),
    comp('explainer/Tag', {'text': '+47 µS / YEAR', 'color': AMBER}, x=760, y=1150, width=360, height=90, start=2.4, enter={'type': 'pop', 'duration': 0.3}, z=30),
], camera={'preset': 'pullOut', 'amount': 0.4}, sfx=[{'cue': 'stinger', 'at': 0.0, 'volume': 0.6}],
    notes='Twist: old orbit dashed white, new orbit amber, offset exaggerated. HUD: THAT 7.4 CM BECOMES 149 KM IN 3 MONTHS (66.7), YOUR YEAR NOW: 365.256 DAYS + 47 uS. FOREVER. (68.3).')

# 12 black
shot('s12-black', 71.0, 72.5, BLACK, [], notes='Black, music tail, HUD hidden.')

# 13 end card
END_FACT = 'IN 2017, LIGHT AND GRAVITY CROSSED 130 MILLION LIGHT-YEARS\nAND ARRIVED 1.7 S APART. SAME SPEED.'
shot('s13-endcard', 72.5, 80.0, {'type': 'color', 'color': '#0B0D10', 'depth': 0, 'overscan': 1.0}, [
    *title_layers(0.0, 7.5, enter=True),
    {'type': 'text', 'text': END_FACT, 'x': '50%', 'y': 1360, 'fontSize': 34, 'font': 'display', 'weight': 700, 'color': '#D9DEE3',
     'letterSpacing': 0.08, 'lineHeight': 1.4, 'maxWidth': 900, 'start': 1.0, 'enter': {'type': 'fade', 'duration': 0.6}, 'depth': 0, 'z': 60},
], sfx=[{'cue': 'ding', 'at': 0.0, 'volume': 0.2}], notes='Exact title repeat in the frame-0 position (loop) + GW170817 fact held 6.5 s. Silent.')

# ------------------------------------------------------------------ assemble
scenes = []
for sh in SHOTS:
    start, end = sh['start'], sh['end']
    frames = round(end * FPS) - round(start * FPS)
    dur = round(frames / FPS, 6)
    layers = list(sh['layers'])
    hidden = any(a <= start + 1e-6 and end <= b + 1e-6 for a, b in HUD_HIDDEN)
    if not hidden:
        layers.append(comp('whatif/Hud', {'t0': round(start, 4), 'lines': HUD, 'mono': 'JetBrains Mono', 'accent': AMBER, 'chipLine': 'C'},
                           id='hud', x=70, y=250, anchorX=0, anchorY=0, width=900, height=360, depth=0, z=80))
    for cs, ce, txt in CAPTIONS:
        if ce <= start or cs >= end:
            continue
        ls, le = max(cs, start) - start, min(ce, end) - start
        cap = {'type': 'text', 'text': txt, 'x': '50%', 'y': 1400, 'fontSize': 62, 'font': SERIF, 'weight': 600,
               'color': '#FFFFFF', 'maxWidth': 860, 'lineHeight': 1.15, 'shadow': '0 3px 14px rgba(0,0,0,.6)',
               'start': round(ls, 4), 'end': round(le, 4), 'depth': 0, 'z': 70}
        if cs >= start:
            cap['enter'] = {'type': 'fade', 'duration': 0.25}
        if ce <= end:
            cap['exit'] = {'type': 'fade', 'duration': 0.25}
        layers.append(cap)
    scene = {'id': sh['id'], 'duration': dur, 'background': sh['background'], 'layers': layers,
             'notes': sh['notes'] + f' [screen {start:.3f}-{end:.3f} s]'}
    if sh['camera']:
        scene['camera'] = sh['camera']
    if sh['transition']:
        scene['transitionIn'] = sh['transition']
    if sh['sfx']:
        scene['sfx'] = sh['sfx']
    scenes.append(scene)

storyboard = {
    'version': 1,
    'id': 'whatif-sun-gone-5-seconds',
    'title': 'What if the Sun vanished for 5 seconds?',
    'format': '9:16',
    'fps': FPS,
    'theme': {'fontDisplay': 'Montserrat', 'fontBody': 'Montserrat', 'fontCondensed': 'Anton', 'accent': AMBER, 'ink': '#0B0D10', 'paper': '#FFFFFF'},
    'scenes': scenes,
    'captions': {'enabled': False},
    'audio': {
        'voice': [],
        'music': [
            {'src': 'music/documentary_pulse.m4a', 'start': 0.0, 'end': round(T_E, 4), 'volume': 0.3, 'duckTo': 0.12, 'fadeIn': 0.2, 'fadeOut': 0.03},
            {'src': 'sfx/clock_ticking.wav', 'start': 13.0, 'end': 22.0, 'volume': 0.3, 'duckTo': 0.2, 'fadeIn': 0.2, 'fadeOut': 0.1, 'loop': True},
            {'src': 'sfx/drone.wav', 'start': round(T_E + 0.4, 4), 'end': round(T_RET, 4), 'volume': 0.3, 'duckTo': 0.22, 'fadeIn': 0.3, 'fadeOut': 0.1, 'loop': True},
            {'src': 'music/documentary_pulse.m4a', 'start': round(T_RET, 4), 'end': 72.5, 'volume': 0.3, 'duckTo': 0.12, 'fadeIn': 0.3, 'fadeOut': 1.5},
        ],
        'sfx': [],
        'duckOn': 'none',
    },
    'overlays': {'grain': 0.03, 'vignette': 0.1, 'fadeIn': 0, 'fadeOut': 0.4},
}

with open(OUT, 'w') as f:
    json.dump(storyboard, f, indent=1, ensure_ascii=False)
    f.write('\n')
total = sum(s['duration'] for s in scenes)
print(f'wrote {OUT}: {len(scenes)} scenes, {total:.3f} s')
for x in (13.0, 22.0, 27.94, 33.53, 36.0, T_E, T_BLACK_END, 41.0, 49.0, 56.0, T_RET):
    print(f'  t={x:7.3f} T={story_T(x):7.2f} D={shadow_mkm(x) if x <= T_E else 0:6.1f} drift={drift_cm(x):5.2f} missed={missed_h(x):5.2f}')
