#!/usr/bin/env python3
"""Generate storyboard.json for whatif-light-walking-speed from the script's shot list, caption table and
HUD state table (keep in sync with script.md). Output path is argv[1].

Rules baked in (producibility review):
- no scene `grade` and no camera `shake`: darkness, ghosting, exposure and shakes are CrossingSet props,
  so the depth-0 HUD and caption layers are never tinted or shaken;
- every scene boundary while the HUD is visible is a hard cut; the sky whip is camera keyframes;
- white flashes are full-frame rect layers under the HUD (the HUD inverts in those windows).
"""
import json
import math
import sys

OUT = sys.argv[1]

SERIF = '"Source Serif 4", "DejaVu Serif", Georgia, serif'
AMBER = '#FFB547'
INK = '#0B0D10'
C_LIGHT = 1.4
FLIP, RETURN, SLOWMO = 7.0, 62.0, 11.0
PX_PER_M, GROUND_Y = 100, 0.55
YOU_FEET = (540, 1180)
YOU_HEAD = (540, 1005)


def tau(t):
    return (t - FLIP) / SLOWMO


def bubble_r(t):
    return max(0.0, min(5.0, tau(t))) * C_LIGHT


# ------------------------------------------------------------------ captions (global seconds)
CAPTIONS = [
    (4.5, 7.0, "You're at Shibuya Crossing, waiting on red."),
    (8.0, 10.6, 'The whole city just went black.'),
    (10.8, 14.0, 'Even your own hand is dark, until...'),
    (19.5, 22.8, 'Sound now travels faster than light.'),
    (23.0, 25.0, 'So does every car.'),
    (31.0, 34.0, 'Your friend lights up, still mid-wave.'),
    (34.5, 38.0, 'Then the car appears, driving backwards.'),
    (44.0, 47.0, 'Every phone signal is stuck mid-air.'),
    (54.0, 57.5, 'But every lamp keeps pouring out light.'),
    (62.5, 65.2, 'Light is back. All five seconds of it.'),
    (65.5, 68.0, 'Everything you missed hits your eyes at once.'),
]

# ------------------------------------------------------------------ HUD state table (global seconds)
HUD = {
    'L': [
        {'from': 0, 'to': 7, 'text': 'LIGHT SLOWS IN'},
        {'from': 7, 'to': 62, 'text': 'LIGHT RETURNS IN'},
        {'from': 62, 'to': 68.5, 'text': 'LIGHT BACK'},
    ],
    'T': [
        {'from': 0, 'to': 7, 'clock': True, 'track': [{'t': 0, 'v': 7.0, 'ease': 'linear'}, {'t': 7, 'v': 0.0, 'ease': 'linear'}], 'format': 'm:ss.mmm'},
        {'from': 7, 'to': 62, 'clock': True, 'track': [{'t': 7, 'v': 5.0, 'ease': 'linear'}, {'t': 62, 'v': 0.0, 'ease': 'linear'}], 'format': 'm:ss.mmm', 'formula': 'v = 5 - (t - 7) / 11'},
        {'from': 62, 'to': 62.6, 'clock': True, 'text': '0:00.000'},
    ],
    'S': [
        {'from': 0, 'to': 7, 'text': '299,792,458 M/S'},
        {'from': 7, 'to': 9.5, 'text': '1.4 M/S = WALKING PACE'},
        {'from': 9.5, 'to': 13, 'text': 'TIME SLOWED 11×'},
        {'from': 13, 'to': 19.5, 'text': 'HAND: 0.5 S LATE'},
        {'from': 19.5, 'to': 24, 'text': 'SOUND: 245× FASTER'},
        {'from': 24, 'to': 31, 'text': 'CAR: 10× FASTER THAN LIGHT'},
        {'from': 31, 'to': 41.7, 'text': 'FRIEND: 2.14 S LATE'},
        {'from': 41.7, 'to': 44, 'text': 'FLASH: 2.86 S LATE'},
        {'from': 44, 'to': 47.5, 'text': 'GPS ETA: 167 DAYS'},
        {'from': 47.5, 'to': 49.5, 'text': 'MOONLIGHT ETA: 8.7 YEARS'},
        {'from': 49.5, 'to': 51, 'text': 'SUNLIGHT ETA: 3,386 YEARS'},
        {'from': 51, 'to': 54, 'text': 'STARLIGHT ETA: {v} YEARS', 'track': [{'t': 51, 'v': 3386}, {'t': 52.5, 'v': 909000000, 'ease': 'in'}, {'t': 54, 'v': 909000000}], 'decimals': 0, 'thousands': True, 'scale': 'log'},
        {'from': 54, 'to': 62, 'text': 'LIGHT PILED UP: {v} S', 'track': [{'t': 54, 'v': round(tau(54), 4), 'ease': 'linear'}, {'t': 62, 'v': 5.0, 'ease': 'linear'}], 'decimals': 2, 'formula': 'v = (t - 7) / 11'},
        {'from': 63, 'to': 68.5, 'text': '214,137,470× BRIGHTER'},
    ],
}
HUD_INVERT = [[41.7, 42.9], [62.0, 62.4]]

# ------------------------------------------------------------------ light model shared by every street scene
CLOCK = {'flipAt': FLIP, 'returnAt': RETURN, 'slowmo': SLOWMO, 'c': C_LIGHT}
VIEWER = {'x': YOU_FEET[0], 'y': YOU_FEET[1], 'eyeH': 1.6, 'pxPerM': PX_PER_M, 'groundScaleY': GROUND_Y}
CAST = {
    'you': {'dxM': 0.0, 'color': '#3A8FD6', 'jacketFlapAt': 26.5},
    'friend': {'dxM': -3.0, 'color': '#F07A5A', 'waveStart': 6.0, 'armRHalfAt': 7.0},
    'tourist': {'dxM': 4.0, 'color': '#E3B04B', 'phoneUpAt': 3.0, 'flashAt': 10.3, 'phoneDownAt': 43.0},
    'signal': {'distM': 15.0, 'greenAt': FLIP + 4.0 * SLOWMO, 'waitBar': True},
    'moon': {'phase': 'full', 'x': 820, 'y': 300},
    'crowd': {'count': 22, 'seed': 4, 'kerb': 'far'},
    'traffic': {'farLanes': 2, 'carsPerLane': 3, 'seed': 9},
}


def car_images():
    """Hero car: 13.9 m/s, side 1.0 m from your eyes, closest at 0:26.5. Returns screen keyframes for the two images."""
    v, d = 50 / 3.6, 1.0
    tc = tau(26.5)
    arrive = lambda u: tc + u + math.sqrt((v * u) ** 2 + d * d) / C_LIGHT
    # refine minimiser numerically
    lo, hi = -0.1, 0.1
    for _ in range(200):
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if arrive(m1) < arrive(m2):
            hi = m2
        else:
            lo = m1
    u_star = (lo + hi) / 2
    a_min = arrive(u_star)
    t_appear = FLIP + SLOWMO * a_min

    def solve(target, a, b):
        fa = arrive(a) - target
        for _ in range(100):
            m = (a + b) / 2
            fm = arrive(m) - target
            if fa * fm <= 0:
                b = m
            else:
                a, fa = m, fm
        return v * (a + b) / 2  # metres along the lane from the closest point

    rev, fwd = [], []
    for t in [t_appear, 35.0, 36.0, 38.0, 40.0, 41.7, 44.0]:
        target = tau(t)
        if t == t_appear:
            xa = xb = v * u_star
        else:
            xa = solve(target, -3.0, u_star)
            xb = solve(target, u_star, 3.0)
        rev.append({'t': round(t, 3), 'xM': round(xa, 3)})
        fwd.append({'t': round(t, 3), 'xM': round(xb, 3)})
    return round(t_appear, 3), rev, fwd


CAR_APPEAR, CAR_REV, CAR_FWD = car_images()
HERO_CAR = {'color': '#7FA7B8', 'speedMps': round(50 / 3.6, 2), 'sideM': 1.0, 'laneCentreM': 1.85, 'passAt': 26.5, 'dir': 'ltr',
            'imageAppearAt': CAR_APPEAR, 'imageReversing': CAR_REV, 'imageForward': CAR_FWD}


def crossing(t0, view='wide', light='slow', **extra):
    p = {'t0': t0, 'view': view, 'light': light, 'clock': CLOCK, 'viewer': VIEWER, 'ghost': 0.06,
         'cast': CAST, 'heroCar': HERO_CAR, 'ringTag': light == 'slow' and view == 'wide', 'palette': 'neon-night'}
    p.update(extra)
    return {'type': 'component', 'name': 'whatif/CrossingSet', 'props': p, 'depth': 1, 'overscan': 1.3}


def comp(name, props=None, **kw):
    layer = {'type': 'component', 'name': name, 'props': props or {}}
    layer.update(kw)
    return layer


def white_flash(keys):
    return {'type': 'rect', 'x': '50%', 'y': '50%', 'width': 1080, 'height': 1920, 'fill': '#FFFFFF', 'depth': 0, 'z': 75,
            'opacity': keys[0]['opacity'], 'keyframes': keys}


RIPPLE = ('<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg"><g fill="none" stroke="#DDE6EE" stroke-width="5" '
          'stroke-linecap="round"><path d="M40 40 A28 28 0 0 1 40 80"/><path d="M28 26 A46 46 0 0 1 28 94"/>'
          '<path d="M16 12 A64 64 0 0 1 16 108"/></g></svg>')


def ripple(x, y, at, flip=False, size=90):
    return {'type': 'svg', 'markup': RIPPLE, 'x': x, 'y': y, 'width': size, 'height': size, 'flipX': flip, 'opacity': 0,
            'keyframes': [{'t': max(0, at - 0.01), 'opacity': 0}, {'t': at + 0.15, 'opacity': 0.8, 'scale': 1.0},
                          {'t': at + 1.4, 'opacity': 0, 'scale': 1.4, 'ease': 'out'}]}


TITLE_ICON = ('<svg viewBox="0 0 220 120" xmlns="http://www.w3.org/2000/svg">'
              '<defs><radialGradient id="g"><stop offset="0" stop-color="#FFF4D6"/><stop offset="0.5" stop-color="#FFB547"/>'
              '<stop offset="1" stop-color="#FFB547" stop-opacity="0"/></radialGradient></defs>'
              '<circle cx="110" cy="44" r="40" fill="url(#g)"/><circle cx="110" cy="44" r="12" fill="#FFF4D6"/>'
              '<g fill="#FFB547"><ellipse cx="78" cy="100" rx="9" ry="14" transform="rotate(-14 78 100)"/>'
              '<ellipse cx="142" cy="92" rx="9" ry="14" transform="rotate(14 142 92)"/></g></svg>')


def title_layers(start, end, enter=True, exit_at=None):
    sh = '0 4px 18px rgba(0,0,0,.55)'
    ls = [
        {'type': 'svg', 'markup': TITLE_ICON, 'x': '50%', 'y': 560, 'width': 220, 'height': 120, 'depth': 0, 'z': 60},
        {'type': 'text', 'text': 'What if light', 'x': '50%', 'y': 690, 'fontSize': 92, 'font': SERIF, 'weight': 600, 'color': '#FFFFFF', 'depth': 0, 'z': 60, 'shadow': sh},
        {'type': 'text', 'text': 'walked', 'x': '50%', 'y': 805, 'fontSize': 140, 'font': SERIF, 'weight': 700, 'color': AMBER, 'depth': 0, 'z': 60, 'shadow': sh},
        {'type': 'text', 'text': 'for 5 seconds?', 'x': '50%', 'y': 920, 'fontSize': 84, 'font': SERIF, 'weight': 600, 'color': '#FFFFFF', 'depth': 0, 'z': 60, 'shadow': sh},
    ]
    for l in ls:
        l['start'] = start
        l['end'] = end
        if enter:
            l['enter'] = {'type': 'fade', 'duration': 0.4}
        if exit_at is not None:
            l['exit'] = {'type': 'fade', 'at': exit_at, 'duration': end - exit_at}
    return ls


SHOTS = []


def shot(sid, start, end, background, layers=(), camera=None, sfx=(), notes='', hud=True):
    SHOTS.append(dict(id=sid, start=start, end=end, background=background, layers=list(layers), camera=camera,
                      sfx=list(sfx), notes=notes, hud=hud))


def cam(*keys):
    return {'keyframes': [dict(k) for k in keys]}


# 1 establishing (cover)
shot('s01-establish', 0.0, 4.5, crossing(0.0, light='normal'), [*title_layers(0.0, 4.5, enter=False, exit_at=4.1)],
     camera=cam({'t': 0, 'x': 540, 'y': 960, 'zoom': 1.0}, {'t': 4.5, 'x': 540, 'y': 975, 'zoom': 1.03, 'ease': 'linear'}),
     sfx=[{'cue': 'tick', 'at': a, 'volume': 0.5} for a in (0.0, 1.0, 2.0, 3.0, 4.0)] + [{'cue': 'whoosh', 'at': 1.2, 'volume': 0.25}, {'cue': 'whoosh', 'at': 3.4, 'volume': 0.25}],
     notes='Frame 1 = cover. Busy night crossing: cars streaming in the near and far lanes, crowd walking, screens scrolling, red signal wait bar, tourist raises phone at 3.0, full Moon rising. Title clears by 4.5.')

# 2 place you
shot('s02-place-you', 4.5, 7.0, crossing(4.5, light='normal'), [],
     camera=cam({'t': 0, 'x': 540, 'y': 975, 'zoom': 1.03}, {'t': 2.5, 'x': 540, 'y': 1005, 'zoom': 1.25}),
     sfx=[{'cue': 'tick', 'at': a, 'volume': 0.6} for a in (0.5, 1.5, 2.0, 2.3)] + [{'cue': 'whoosh', 'at': 0.8, 'volume': 0.25}],
     notes='Friend turns and starts to wave at 6.0 (armR track); arm halfway at 7.0.')

# 3 flip
shot('s03-flip', 7.0, 10.8, crossing(7.0, view='close', shake=[{'at': 0.0, 'duration': 0.3, 'amplitude': 10}], headGlowMinPx=26), [
    ripple(905, 905, at=3.3, flip=True),
],
     camera=cam({'t': 0, 'x': 540, 'y': 1005, 'zoom': 2.4}, {'t': 3.8, 'x': 540, 'y': 1005, 'zoom': 2.0}),
     sfx=[{'cue': 'impact', 'at': 0.0, 'volume': 0.9}, {'cue': 'glitch', 'at': 0.0, 'volume': 0.3}, {'cue': 'click', 'at': 3.3, 'volume': 0.8}],
     notes='World to a 6% ghost; only a sphere of light around your head (R 0 -> 0.48 m). City sound carries on. Shutter click at 10.3 from the dark right (ripple glyph), nothing lit. Shake is internal to CrossingSet.')

# 4a POV hand
POV_BG = {'type': 'gradient', 'kind': 'radial', 'colors': ['#07090C', '#020304'], 'depth': 0.2, 'overscan': 1.2}
BOKEH = {'type': 'particles', 'preset': 'dust', 'count': 30, 'color': '#FF5FA2', 'size': [18, 46], 'speed': 0.05, 'seed': 12, 'opacity': 0.06, 'blur': 8, 'depth': 0.4}
POV = {'t0': 10.8, 'clock': CLOCK, 'elbowDistM': 0.3, 'handDistM': 0.7, 'feltWiggleFrom': 13.0, 'seenDelayEvent': 0.5, 'feltStyle': 'dotted', 'skin': '#E9B48F', 'sleeve': '#3A8FD6'}
shot('s04a-pov-hand', 10.8, 15.8, POV_BG, [dict(BOKEH), comp('whatif/PovHand', POV, x=560, y=1000, width=900, height=900)],
     camera=cam({'t': 0, 'zoom': 1.0}, {'t': 5.0, 'zoom': 1.03, 'ease': 'linear'}),
     sfx=[{'cue': 'whoosh', 'at': 1.7, 'volume': 0.2}],
     notes='Light edge crawls from elbow (lit 9.4) to fingertips (lit 12.5). Dotted felt hand wiggles from 13.0; the seen hand stays frozen.')

# 4b POV push-in step
shot('s04b-pov-lag', 15.8, 19.5, POV_BG, [dict(BOKEH), comp('whatif/PovHand', dict(POV, t0=15.8), x=560, y=1000, width=900, height=900)],
     camera=cam({'t': 0, 'zoom': 1.08}, {'t': 3.7, 'zoom': 1.16, 'ease': 'linear'}),
     sfx=[{'cue': 'tick', 'at': 0.0, 'volume': 0.5}],
     notes='The seen hand starts following at 18.5 (0.5 event s behind the felt one).')

# 5 rule (sound)
shot('s05-rule-sound', 19.5, 25.0, crossing(19.5), [
    ripple(150, 640, 0.3), ripple(930, 600, 1.1, flip=True), ripple(380, 520, 2.4), ripple(760, 700, 3.6, flip=True),
],
     camera=cam({'t': 0, 'x': 540, 'y': 1000, 'zoom': 1.35}, {'t': 5.5, 'x': 540, 'y': 990, 'zoom': 1.25}),
     sfx=[{'cue': 'ding', 'at': 0.3, 'volume': 0.35}, {'cue': 'ding', 'at': 0.7, 'volume': 0.3}],
     notes='Bubble R 1.59 -> 2.29 m; ground lights from 19.6; ring tag. Sound ripples from the dark (ding = crossing-chime stand-in).')

# 6 car passes unseen (textless from 25.0)
shot('s06-car-unseen', 25.0, 30.6, crossing(25.0, shake=[{'at': 1.4, 'duration': 0.6, 'amplitude': 5}], wind={'at': 1.3, 'duration': 1.2}), [
    {'type': 'svg', 'markup': RIPPLE, 'x': 200, 'y': 1060, 'width': 120, 'height': 120, 'opacity': 0,
     'keyframes': [{'t': 0.9, 'opacity': 0, 'x': 200}, {'t': 1.5, 'opacity': 0.85, 'x': 540}, {'t': 2.2, 'opacity': 0, 'x': 880, 'ease': 'linear'}]},
],
     camera=cam({'t': 0, 'x': 540, 'y': 990, 'zoom': 1.25}, {'t': 1.3, 'x': 540, 'y': 990, 'zoom': 1.25}, {'t': 5.6, 'x': 540, 'y': 985, 'zoom': 1.3}),
     sfx=[{'cue': 'whoosh_long', 'at': 1.2, 'volume': 0.9}, {'cue': 'boom', 'at': 1.45, 'volume': 0.35}, {'cue': 'stinger', 'at': 1.5, 'volume': 0.25}],
     notes='TEXTLESS. The lit road in front of you is empty; the car passes 1.0 m away at 26.5 (sound + wind only: jacket/hair whip, paper cup tumbles). Horn: synthesize car_horn on the Spark (stinger stand-in).')

# 7 friend
shot('s07-friend', 30.6, 34.3, crossing(30.6), [],
     camera=cam({'t': 0, 'x': 540, 'y': 985, 'zoom': 1.3}, {'t': 3.7, 'x': 500, 'y': 985, 'zoom': 1.25}),
     sfx=[{'cue': 'ding', 'at': 0.0, 'volume': 0.4}],
     notes='Bubble edge reaches the friend (3.0 m) at 30.57: she lights up frozen mid-wave, then waves slowly, 2.14 s late.')

# 8 car image + tourist
shot('s08-car-image', 34.3, 41.7, crossing(34.3), [],
     camera=cam({'t': 0, 'x': 500, 'y': 985, 'zoom': 1.25}, {'t': 7.4, 'x': 560, 'y': 975, 'zoom': 1.1}),
     sfx=[{'cue': 'pop', 'at': 0.02, 'volume': 0.5}, {'cue': 'riser', 'at': 4.7, 'volume': 0.4}],
     notes=f'Car image appears at {CAR_APPEAR:.2f} a metre in front of you and splits (heroCar.imageReversing / imageForward, metres from the closest point). Tourist (4.0 m) lights up at 38.43 with the phone raised.')

# 9 white-out
shot('s09-whiteout', 41.7, 44.0, crossing(41.7, castOverrides={'tourist': {'phoneDownAt': 43.0}}), [
    white_flash([{'t': 0, 'opacity': 1}, {'t': 1.0, 'opacity': 1}, {'t': 1.8, 'opacity': 0, 'ease': 'out'}]),
], camera=cam({'t': 0, 'x': 560, 'y': 975, 'zoom': 1.1}),
     sfx=[{'cue': 'stinger', 'at': 0.0, 'volume': 0.7}, {'cue': 'whoosh', 'at': 0.05, 'volume': 0.5}],
     notes='The flash fired at 10.3 reaches your eyes at 41.73: full white 1.0 s (rect, z under the HUD; HUD inverts 41.7-42.9), fades to the crossing.')

# 10 phone insert
shot('s10-phone', 44.0, 47.0, crossing(44.0, view='close-tourist'), [
    comp('whatif/PhoneScreen', {'bars': 0, 'spinner': True, 'lit': True}, x=600, y=880, width=360, height=640, rotate=-6),
], camera=cam({'t': 0, 'zoom': 1.0}, {'t': 3.0, 'zoom': 1.08, 'ease': 'linear'}),
     sfx=[{'cue': 'phone_buzz', 'at': 0.3, 'volume': 0.25}],
     notes='The tourist\'s phone (inside your bubble, so lit): no bars, spinner. No on-screen words.')

# 11 sky (tall scene, in-scene whip)
SKY_BG = {'type': 'color', 'color': '#010203', 'depth': 0, 'overscan': 1.0}
shot('s11-sky', 47.0, 54.0, SKY_BG, [
    comp('whatif/SkyBodies', {'moon': 'full', 'ghost': 0.06, 'stars': 140, 'satellites': 2, 'seed': 3}, x=540, y=900, width=1300, height=2000, depth=1),
    comp('whatif/CrossingSet', dict(crossing(47.0, view='skyline')['props']), x=540, y=2350, width=1400, height=900, depth=1),
], camera=cam({'t': 0, 'x': 540, 'y': 2350, 'zoom': 1.0}, {'t': 0.35, 'x': 540, 'y': 960, 'zoom': 1.0, 'ease': 'out'},
              {'t': 6.0, 'x': 540, 'y': 900, 'zoom': 0.95, 'ease': 'linear'}, {'t': 7.0, 'x': 540, 'y': 2350, 'zoom': 1.0, 'ease': 'in'}),
     sfx=[{'cue': 'whoosh_long', 'at': 0.0, 'volume': 0.5}, {'cue': 'whoosh_long', 'at': 6.0, 'volume': 0.4}],
     notes='Black sky, ghost full Moon over ghost towers, ghost stars, two satellite dots. HUD climbs MOON -> SUN -> STAR (log ladder). No captions.')

# 12 plant
shot('s12-plant', 54.0, 57.5, crossing(54.0), [
    comp('whatif/Inset', {'label': 'MEANWHILE', 'content': 'neon-halo', 't0': 54.0, 'clock': CLOCK, 'haloRadius': '1.4*tau'}, x=540, y=760, width=520, height=320, depth=0, z=50,
         enter={'type': 'pop', 'duration': 0.3}),
], camera=cam({'t': 0, 'x': 540, 'y': 960, 'zoom': 1.0}),
     sfx=[{'cue': 'drone', 'at': 0.0, 'volume': 0.3}],
     notes='Bubble ~6.0 m. MEANWHILE inset: a neon sign in the dark with a thick growing halo of trapped light. HUD LIGHT PILED UP live.')

# 13 full bubble
shot('s13-full-bubble', 57.5, 62.0, crossing(57.5), [],
     camera=cam({'t': 0, 'x': 540, 'y': 960, 'zoom': 1.0}, {'t': 4.5, 'x': 540, 'y': 940, 'zoom': 0.85, 'ease': 'linear'}),
     sfx=[{'cue': 'riser', 'at': 0.5, 'volume': 0.5}, {'cue': 'clock_ticking', 'at': 2.0, 'volume': 0.3}],
     notes='Bubble 6.2 -> 7.0 m, edge leaves the frame by 61; HUD clock under 0:00.100 at 61.0.')

# 14 return + afterimage
EXPOSURE = {'from': FLIP, 'to': RETURN, 'samples': 12, 'perObjectWindow': 'min(5, r/1.4) inside the bubble, 5 s outside', 'blend': 'screen'}
shot('s14-return', 62.0, 65.5, crossing(62.0, light='exposure', exposure=EXPOSURE, exposureOpacity=[{'t': 0.4, 'v': 1.0}, {'t': 3.5, 'v': 0.55}], underlay='normal'), [
    white_flash([{'t': 0, 'opacity': 1}, {'t': 0.4, 'opacity': 0, 'ease': 'out'}]),
], camera=cam({'t': 0, 'x': 540, 'y': 960, 'zoom': 1.0}),
     sfx=[{'cue': 'impact', 'at': 0.0, 'volume': 0.9}, {'cue': 'stinger', 'at': 0.0, 'volume': 0.6}, {'cue': 'drone', 'at': 0.4, 'volume': 0.25}],
     notes='Return: white flash 62.0-62.4 (rect), then the long-exposure afterimage (cars as streaks, crowd smears, signal red AND green, friend arm fan of 5, the car double) over the normal crossing.')

# 15 twist hold
shot('s15-twist', 65.5, 68.0, crossing(65.5, light='exposure', exposure=EXPOSURE, exposureOpacity=[{'t': 0, 'v': 0.55}, {'t': 2.5, 'v': 0.15}], underlay='normal'), [],
     camera=cam({'t': 0, 'x': 540, 'y': 960, 'zoom': 1.0}, {'t': 2.5, 'x': 540, 'y': 980, 'zoom': 1.08, 'ease': 'linear'}),
     sfx=[{'cue': 'heartbeat_slow', 'at': 0.0, 'volume': 0.4}],
     notes='Afterimage fades. Caption 11.')

# 16 bookend
shot('s16-bookend', 68.0, 69.5, crossing(68.0, light='normal', castOverrides={'signal': {'state': 'green'}, 'crowd': {'surge': True}}), [],
     camera=cam({'t': 0, 'x': 540, 'y': 960, 'zoom': 1.0}),
     sfx=[{'cue': 'ding', 'at': 0.2, 'volume': 0.3}],
     notes='Frame-1 framing, normal light; signal green, crowd surging, friend waving. HUD fades out 68.0-68.5. No text.')

# 17 black
shot('s17-black', 69.5, 70.5, {'type': 'color', 'color': '#000000', 'depth': 0, 'overscan': 1.0}, [], sfx=[{'cue': 'tick', 'at': 0.3, 'volume': 0.5}],
     notes='Black, music out.', hud=False)

# 18 end card
END_FACT = "HARVARD, 2001 · LENE HAU'S LAB STOPPED A PULSE OF LIGHT IN ULTRACOLD ATOMS, THEN LET IT GO."
shot('s18-endcard', 70.5, 78.0, {'type': 'color', 'color': INK, 'depth': 0, 'overscan': 1.0}, [
    *title_layers(0.0, 7.5, enter=True),
    {'type': 'text', 'text': END_FACT, 'x': '50%', 'y': 1120, 'fontSize': 34, 'font': 'display', 'weight': 700, 'color': '#D9DEE3',
     'letterSpacing': 0.08, 'lineHeight': 1.4, 'maxWidth': 860, 'start': 1.0, 'enter': {'type': 'fade', 'duration': 0.6}, 'depth': 0, 'z': 60},
], notes='End card: exact title repeat + fact (neither is read).', hud=False)

# ------------------------------------------------------------------ assemble
scenes = []
for sh in SHOTS:
    start, end = sh['start'], sh['end']
    layers = list(sh['layers'])
    if sh['hud'] and start < 68.5:
        layers.append(comp('whatif/Hud', {'t0': start, 'lines': HUD, 'invert': HUD_INVERT, 'fadeOut': [68.0, 68.5],
                                          'mono': 'JetBrains Mono', 'accent': AMBER},
                           id='hud', x=70, y=250, anchorX=0, anchorY=0, width=820, height=260, depth=0, z=80))
    for cs, ce, text in CAPTIONS:
        if ce <= start or cs >= end:
            continue
        ls, le = max(cs, start) - start, min(ce, end) - start
        cap = {'type': 'text', 'text': text, 'x': '50%', 'y': 1400, 'fontSize': 62, 'font': SERIF, 'weight': 600,
               'color': '#FFFFFF', 'maxWidth': 860, 'lineHeight': 1.15, 'shadow': '0 3px 14px rgba(0,0,0,.7)',
               'start': round(ls, 3), 'end': round(le, 3), 'depth': 0, 'z': 70}
        if cs >= start:
            cap['enter'] = {'type': 'fade', 'duration': 0.25}
        if ce <= end:
            cap['exit'] = {'type': 'fade', 'duration': 0.25}
        layers.append(cap)
    scene = {'id': sh['id'], 'duration': round(end - start, 3), 'background': sh['background'], 'layers': layers,
             'notes': sh['notes'] + f' [screen {start:.1f}-{end:.1f} s; bubble R {bubble_r(start):.2f}-{bubble_r(end):.2f} m]'}
    if sh['camera']:
        scene['camera'] = sh['camera']
    if sh['sfx']:
        scene['sfx'] = sh['sfx']
    scenes.append(scene)

storyboard = {
    'version': 1,
    'id': 'whatif-light-walking-speed',
    'title': 'What if light walked for 5 seconds?',
    'format': '9:16',
    'fps': 30,
    'theme': {'fontDisplay': 'Montserrat', 'fontBody': 'Montserrat', 'fontCondensed': 'Anton', 'accent': AMBER, 'ink': INK, 'paper': '#FFFFFF'},
    'scenes': scenes,
    'captions': {'enabled': False},
    'audio': {
        'voice': [],
        'music': [
            {'src': 'music/documentary_pulse.m4a', 'start': 0.0, 'end': 7.0, 'volume': 0.15, 'duckTo': 0.15, 'fadeIn': 0.3, 'fadeOut': 0.1},
            {'src': 'music/tension_pulse.m4a', 'start': 7.0, 'end': 62.0, 'volume': 0.2, 'duckTo': 0.1, 'fadeIn': 0.3, 'fadeOut': 0.1},
            {'src': 'sfx/drone.wav', 'start': 0.0, 'end': 69.5, 'volume': 0.18, 'duckTo': 0.18, 'fadeIn': 0.2, 'fadeOut': 0.3, 'loop': True},
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
print(f'wrote {OUT}: {len(scenes)} scenes, {total:.2f} s; car image at {CAR_APPEAR:.2f}; rev {CAR_REV[-2]} fwd {CAR_FWD[-2]}')
