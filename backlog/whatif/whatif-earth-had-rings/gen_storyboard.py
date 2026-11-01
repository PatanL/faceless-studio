#!/usr/bin/env python3
"""Generate storyboard.json for whatif-earth-had-rings from script.md's shot list, caption list and HUD
state table. Every HUD number, band position and declination comes from rings.py (same folder).

usage: python3 gen_storyboard.py <out.json>
"""
import json
import math
import os
import sys
from datetime import timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rings as R  # noqa: E402

OUT = sys.argv[1]
SERIF = '"Fraunces", "Source Serif 4", "DejaVu Serif", Georgia, serif'
MONO = 'IBM Plex Mono'
GOLD = '#E8B04A'
W, H = 1080, 1920
BLACK_AT = 72.6

# ------------------------------------------------------------------ captions (global seconds; VO = these lines)
CAPTIONS = [
    (4.1, 7.0, "You're on Miami's Ocean Drive."),
    (8.0, 11.9, 'An arch 33 Moons wide fills the south.'),
    (12.5, 15.8, 'At midnight, the rings light your street.'),
    (18.0, 21.0, 'The rings shade a stripe of Earth.'),
    (22.0, 24.1, 'But the Sun moves.'),
    (28.0, 31.6, 'So the shadow creeps north, day by day.'),
    (33.0, 36.4, 'In Fortaleza, noon goes dark.'),
    (41.0, 43.8, 'Now it crosses into the north.'),
    (52.0, 54.9, 'Havana is next. Then you.'),
    (56.8, 59.8, 'Every weather app still says sunny.'),
    (60.0, 62.9, 'A gap in the rings. Sunlight.'),
    (63.8, 67.7, 'Miami gets less December sun than Moscow.'),
    (69.4, 72.5, 'Then it comes back. Every November.'),
]

# ------------------------------------------------------------------ calendar helpers
CONTACT_DAYS = 144  # JUN 21 -> NOV 12 (rings.py)


def date_at(t):
    return R.FLIP + timedelta(days=(t - R.FLIP_T) * R.DAYS_PER_SEC)


def decl_at(t):
    """Noon declination (rad) at screen time t, linear between days (Miami meridian)."""
    off = (t - R.FLIP_T) * R.DAYS_PER_SEC
    d0 = R.FLIP + timedelta(days=math.floor(off))
    f = off - math.floor(off)
    a = R.noon_decl(d0, R.MIAMI[1])
    b = R.noon_decl(d0 + timedelta(days=1), R.MIAMI[1])
    return a + (b - a) * f


def lat_for_radius(dec, r):
    lo, hi = 1e-6, 90 - math.degrees(abs(dec)) - 1e-6
    for _ in range(70):
        mid = (lo + hi) / 2
        if math.cos(math.radians(mid)) + math.sin(math.radians(mid)) / math.tan(abs(dec)) < r:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def km_at(t):
    if t >= 55.0:
        return 0
    return int(round(R.miami_distance_km(date_at(t)) / 10.0) * 10)


# ------------------------------------------------------------------ HUD state table (global seconds)
def seg(a, b, text, **kw):
    d = {'from': a, 'to': b, 'text': text}
    d.update(kw)
    return d


KM_TRACK_1 = [{'t': float(t), 'v': km_at(t)} for t in range(7, 39)]
KM_TRACK_2 = [{'t': float(t), 'v': km_at(t)} for t in range(41, 56)]
HUD = {
    'CH': [
        seg(7, 18, '1 · THE RINGS'), seg(18, 28, '2 · THE SHADOW'), seg(28, 38.3, '3 · THE WALK NORTH'),
        seg(38.3, 55, '4 · EQUINOX'), seg(55, 63, '5 · CONTACT'), seg(63, BLACK_AT, '6 · WINTER'),
    ],
    'L': [
        seg(0, 7, 'RINGS FORM IN'), seg(7, 55, 'RING SHADOW REACHES YOU IN'), seg(55, 69.4, 'RING SHADOW'),
        seg(69.4, BLACK_AT, 'RING SHADOW RETURNS IN'),
    ],
    'N': [
        seg(0, 7, '{v} S', track=[{'t': 0, 'v': 7.0, 'ease': 'linear'}, {'t': 7, 'v': 0.0, 'ease': 'linear'}], decimals=2),
        seg(7, 55, '{v} DAYS', track=[{'t': 7, 'v': 144.0, 'ease': 'linear'}, {'t': 55, 'v': 0.0, 'ease': 'linear'}], decimals=1),
        seg(55, 68, 'ON YOU'), seg(68, 69.4, 'GONE'),
        seg(69.4, 74.0, '{v} DAYS', track=[{'t': 69.4, 'v': 286.0, 'ease': 'linear'}, {'t': 74.0, 'v': 272.2, 'ease': 'linear'}], decimals=1,
            centreFrom=BLACK_AT),
    ],
    'K': [
        seg(7, 38.3, 'SHADOW EDGE {v} KM SOUTH', track=KM_TRACK_1, decimals=0, thousands=True),
        seg(38.8, 41, "SATURN'S DID THIS ON 11 AUG 2009"),
        seg(41, 55, 'SHADOW EDGE {v} KM SOUTH', track=KM_TRACK_2, decimals=0, thousands=True),
        seg(55, 68, 'IN SHADOW · DAY {v}', track=[{'t': 55, 'v': 0, 'ease': 'linear'}, {'t': 68, 'v': 39, 'ease': 'linear'}], decimals=0),
        seg(68, BLACK_AT, '79 DAYS IN SHADOW'),
    ],
    'S': [
        seg(0, 7, 'THEIR SHADOW IS HEADED FOR MIAMI'),
        seg(8.5, 11, '3,400-8,100 KM UP · 29°-47° HIGH'),
        seg(11, 12.4, 'SHADOW ON RIO · JOBURG · SYDNEY'),
        seg(13.5, 16, 'BRIGHTER THAN A FULL MOON (EST.)'),
        seg(16, 18, '4,700 KM WIDE · ABOUT 10 M THICK'),
        seg(18.5, 22, '21 ANCIENT CRATERS LINE AN OLD EQUATOR · WHY?'),
        seg(29, 33.5, 'THE SUN HEADS SOUTH · THE SHADOW HEADS NORTH'),
        seg(33.5, 38.3, 'FORTALEZA · SEP 8 · NOON LIGHT <1% (EST.)'),
        seg(38.3, 41.3, 'SEP 23 · SHADOW SHRINKS TO A LINE'),
        seg(41.3, 44.3, 'OCT 02 · BOGOTÁ'), seg(44.3, 45.3, 'OCT 11 · PANAMA CITY'), seg(45.3, 47, 'OCT 14 · CARACAS'),
        seg(47, 53.3, 'CLOSING ~57 KM A DAY'), seg(53.3, 55, 'NOV 07 · HAVANA'),
        seg(55, 56.8, 'NOV 12 · 25.8°N · A RING'), seg(56.8, 60, 'NOON LIGHT ~20% (EST.)'),
        seg(60, 63, 'NOV 27 · CASSINI DIVISION · ~75%'), seg(63, 64.8, 'DEC 6 · B RING · NOON LIGHT ~2% (EST.)'),
        seg(64.8, 66.6, 'DECEMBER SUN ~7% OF NORMAL (EST.)'),
        seg(66.6, 68, 'UNDER THE SHADOW: 14°N-41°N · 3+ BILLION PEOPLE (EST.)'),
        seg(68, 69.4, 'FULL SUN AGAIN'), seg(70.6, BLACK_AT, 'EVERY YEAR · NOV 12 TO JAN 30'),
    ],
    'D': [
        seg(0, 7, 'JUN 21 · DUSK'),
        seg(7, 12.5, '{date} · 3 DAYS / SEC · EACH DUSK', date={'t0': 7, 'd0': '2026-06-21', 'perSec': 3}),
        seg(12.5, 18, '{date} · 3 DAYS / SEC · EACH MIDNIGHT', date={'t0': 7, 'd0': '2026-06-21', 'perSec': 3}),
        seg(18, 68, '{date} · 3 DAYS / SEC · EACH NOON', date={'t0': 7, 'd0': '2026-06-21', 'perSec': 3}),
        seg(68, 69.4, '▸▸ JAN 30'),
        seg(69.4, BLACK_AT, '{date} · 3 DAYS / SEC · EACH MIDNIGHT', date={'t0': 69.4, 'd0': '2027-01-30', 'perSec': 3}),
    ],
}
SCRUBBER = [
    {'from': 7, 'to': 69.4, 'start': '2026-06-21', 'end': '2027-02-15', 'you': '2026-11-12', 'date': {'t0': 7, 'd0': '2026-06-21', 'perSec': 3}},
    {'from': 69.4, 'to': BLACK_AT, 'start': '2027-01-15', 'end': '2027-12-15', 'you': '2027-11-12', 'date': {'t0': 69.4, 'd0': '2027-01-30', 'perSec': 3}},
]
STAMPS = [{'at': 55.0, 'duration': 0.8, 'text': 'ON YOU', 'color': GOLD}]


# ------------------------------------------------------------------ layer helpers
def comp(name, props=None, **kw):
    layer = {'type': 'component', 'name': name, 'props': props or {}}
    layer.update(kw)
    return layer


def you(x, y, pose='stand', color='#3A8FD6', w=150, h=250, **kw):
    return comp('explainer/You', {'pose': pose, 'color': color}, x=x, y=y, width=w, height=h, **kw)


def street(time, **props):
    p = {'time': time, 'vanish': [540, 900]}
    p.update(props)
    return comp('whatif/OceanDrive', p, id='street', x='50%', y=1300, width=W, height=2600, depth=1)


def arch(lit, **props):
    p = {'lit': lit}
    p.update(props)
    return comp('whatif/RingArch', p, id='arch', x='50%', y=560, width=W, height=820, depth=1)


def overlay(fill, keys, blend=None, z=30):
    layer = {'type': 'rect', 'x': '50%', 'y': '50%', 'width': W * 1.4, 'height': H * 1.4, 'fill': fill, 'depth': 0, 'z': z,
             'opacity': keys[0][1], 'keyframes': [{'t': t, 'opacity': o, 'ease': 'inOut'} for t, o in keys]}
    if blend:
        layer['blend'] = blend
    return layer


def shade(keys):
    """Ring shade = dark overlay + blue-grey multiply tint, both keyed (light EST. -> opacity)."""
    return [overlay('#0E1620', keys, z=30), overlay('#5B6B7A', [(t, min(0.45, o * 0.6)) for t, o in keys], blend='multiply', z=31)]


def map_layer(view, pins=(), rings=()):
    return comp('explainer/Map', {'view': view, 'pins': list(pins), 'rings': list(rings), 'grid': True, 'labelSize': 34, 'pinSize': 0.8},
                id='map', x='50%', y='50%', width=W, height=H, depth=1)


def band_layers(view, t0, t1, step=0.5, deepen=None):
    """B / Cassini / A noon shadow band as rect layers in the map's equirectangular projection."""
    k = 3.0 * view['zoom']
    lat0 = view['lat']

    def y_of(lat):
        return H / 2 - (lat - lat0) * k

    zones = [('B', R.B_IN, R.B_OUT, '#0B0F14', 0.55), ('CD', R.B_OUT, R.A_IN, '#0B0F14', 0.12), ('A', R.A_IN, R.A_OUT, '#0B0F14', 0.32)]
    layers = []
    n = int(round((t1 - t0) / step))
    for name, r_in, r_out, fill, op in zones:
        keys = []
        for i in range(n + 1):
            t = t0 + i * step
            dec = decl_at(t)
            if abs(dec) < math.radians(0.05):
                la, lb = 0.0, 0.05
            else:
                la, lb = lat_for_radius(dec, r_in), lat_for_radius(dec, r_out)
            sign = -1 if dec > 0 else 1   # Sun north -> band in the south
            ya, yb = y_of(sign * la), y_of(sign * lb)
            kf = {'t': round(t - t0, 3), 'y': round((ya + yb) / 2, 1), 'scaleY': round(max(0.02, abs(ya - yb) / 100.0), 4), 'ease': 'linear'}
            if deepen and name == 'B':
                kf['opacity'] = op if t < deepen[0] else deepen[1]
            keys.append(kf)
        layers.append({'type': 'rect', 'id': f'band-{name}', 'x': '50%', 'y': keys[0]['y'], 'width': W * 1.6, 'height': 100,
                       'fill': fill, 'opacity': op, 'blur': 6, 'depth': 1, 'z': 5, 'keyframes': keys})
    return layers


def pin(lon, lat, label, at, color='#9FB4C7'):
    return {'lon': lon, 'lat': lat, 'label': label, 'at': at, 'color': color}


SHOTS = []


def shot(sid, start, end, background, layers=(), camera=None, transition=None, grade=None, sfx=(), notes=''):
    SHOTS.append(dict(id=sid, start=start, end=end, background=background, layers=list(layers), camera=camera,
                      transition=transition, grade=grade, sfx=list(sfx), notes=notes))


GLYPH = ('<svg viewBox="0 0 220 120" xmlns="http://www.w3.org/2000/svg"><ellipse cx="110" cy="62" rx="100" ry="26" fill="none" '
         'stroke="#E8B04A" stroke-width="8"/><circle cx="110" cy="58" r="38" fill="#E8B04A"/>'
         '<path d="M14 66 C40 92 180 92 206 66" fill="none" stroke="#E8B04A" stroke-width="8"/></svg>')


def title_layers(start, end, exit_at=None, enter=True):
    sh = '0 4px 18px rgba(0,0,0,.45)'
    ls = [
        {'type': 'svg', 'markup': GLYPH, 'x': '50%', 'y': 560, 'width': 220, 'height': 120, 'depth': 0, 'z': 60},
        {'type': 'text', 'text': 'What if Earth had', 'x': '50%', 'y': 690, 'fontSize': 84, 'font': SERIF, 'weight': 600, 'color': '#FFFFFF', 'depth': 0, 'z': 60, 'shadow': sh},
        {'type': 'text', 'text': 'rings like Saturn?', 'x': '50%', 'y': 810, 'fontSize': 112, 'font': SERIF, 'weight': 700, 'color': GOLD, 'depth': 0, 'z': 60, 'shadow': sh},
    ]
    for layer in ls:
        layer['start'], layer['end'] = start, end
        if enter:
            layer['enter'] = {'type': 'fade', 'duration': 0.4}
        if exit_at is not None:
            layer['exit'] = {'type': 'fade', 'at': exit_at, 'duration': round(end - exit_at, 3)}
    return ls


DUSK_SKY = {'type': 'gradient', 'kind': 'linear', 'angle': 180, 'colors': ['#7B5EA7', '#F6A96B'], 'depth': 0.1, 'overscan': 1.3}
NOON_SKY = {'type': 'gradient', 'kind': 'linear', 'angle': 180, 'colors': ['#8EC9F0', '#CDE9F7'], 'depth': 0.1, 'overscan': 1.3}
NIGHT_SKY = {'type': 'gradient', 'kind': 'linear', 'angle': 180, 'colors': ['#0B1530', '#1B2A4A'], 'depth': 0.1, 'overscan': 1.3}
CARD = {'type': 'gradient', 'kind': 'linear', 'angle': 180, 'colors': ['#0E1A26', '#14283A'], 'depth': 0.1, 'overscan': 1.2}
SEA = {'type': 'color', 'color': '#04121a', 'depth': 0.1, 'overscan': 1.2}
BLACK = {'type': 'color', 'color': '#000000', 'depth': 0, 'overscan': 1.0}
ENDBG = {'type': 'color', 'color': '#0B0D10', 'depth': 0, 'overscan': 1.0}
MIAMI_PIN = pin(-80.13, 25.79, 'YOU', 0.0, GOLD)

# 1 establishing (frame 1 = cover)
shot('s01-establish', 0.0, 4.5, DUSK_SKY, [
    street('dusk', neonOn=True),
    *title_layers(0.0, 4.5, exit_at=4.1, enter=False),
], camera={'keyframes': [{'t': 0, 'zoom': 1.0}, {'t': 4.5, 'zoom': 1.03, 'ease': 'linear'}]},
    sfx=[{'cue': 'clock_ticking', 'at': 0.0, 'volume': 0.4}],
    notes='Frame 1 = cover: dusk Ocean Drive looking due south, empty southern sky, title upper third, HUD pre-event clock + threat subline.')

# 2 place you
shot('s02-place-you', 4.5, 7.0, DUSK_SKY, [
    street('dusk', neonOn=True),
    you(430, 1330, 'stand'),
], camera={'preset': 'pushIn', 'amount': 0.4},
    sfx=[{'cue': 'tick', 'at': 1.5, 'volume': 0.6}, {'cue': 'tick', 'at': 2.0, 'volume': 0.6}, {'cue': 'tick', 'at': 2.3, 'volume': 0.7}],
    notes='You, small, back to camera on the sidewalk under a palm. Caption 1 started at 4.1 under the title fade.')

# 3 flip
shot('s03-flip', 7.0, 8.0, DUSK_SKY, [
    street('dusk', neonOn=True),
    arch(1, slideIn={'at': 0.0, 'duration': 0.35}),
    you(430, 1330, 'stand'),
    overlay('#2A1C4A', [(0.0, 0.0), (0.35, 0.15)], z=4),
], camera={'keyframes': [], 'shake': [{'at': 0.0, 'duration': 0.35, 'amplitude': 12}]},
    sfx=[{'cue': 'boom', 'at': 0.0, 'volume': 0.9}, {'cue': 'whoosh_long', 'at': 0.0, 'volume': 0.5}],
    notes='Rings land: the two halves of the arch slide in from the left and right edges and lock. HUD flips to RING SHADOW REACHES YOU IN 144.0 DAYS.')

# 4 tilt up, 33 Moons
shot('s04-arch', 8.0, 12.5, DUSK_SKY, [
    street('dusk', neonOn=True),
    arch(1, moonStack={'count': 33, 'at': 0.6, 'duration': 2.0}),
    comp('explainer/Stat', {'value': 33, 'from': 0, 'at': 0.6, 'duration': 2.0, 'label': 'MOONS', 'color': GOLD}, x=880, y=520, width=260, height=200, depth=0, z=50),
], camera={'keyframes': [{'t': 0, 'y': '50%', 'zoom': 1.0}, {'t': 1.6, 'y': 700, 'zoom': 0.94}, {'t': 4.5, 'y': 690, 'zoom': 0.94, 'ease': 'linear'}]},
    sfx=[{'cue': 'pop', 'at': 0.6 + 0.4 * i, 'volume': 0.2} for i in range(6)],
    notes='Tilt up (y -260): 33 Moon discs stack across the band height; Stat counts to 33.')

# 5 midnight ringlight
shot('s05-midnight', 12.5, 18.0, NIGHT_SKY, [
    street('night', streetlights=True, neonOn=True),
    arch(1, earthShadowNotch=True, glow=True),
    *[{'type': 'circle', 'x': x, 'y': 1440, 'width': 70, 'height': 220, 'fill': '#04070D', 'opacity': 0.45, 'blur': 14, 'rotate': r, 'depth': 1, 'z': 9}
      for x, r in ((520, 24), (600, -24))],
    you(560, 1330, 'stand', w=170, h=280, z=10),
], camera={'keyframes': [{'t': 0, 'y': 760, 'zoom': 0.95}, {'t': 1.6, 'y': 1000, 'zoom': 1.0}, {'t': 5.5, 'y': 1010, 'zoom': 1.02, 'ease': 'linear'}]},
    sfx=[{'cue': 'breath', 'at': 0.7, 'volume': 0.25}, {'cue': 'ding', 'at': 1.0, 'volume': 0.2}],
    notes='EACH MIDNIGHT. Ringlight from the arch east and west halves (Earth-shadow notch at the meridian): two soft shadows fan down-screen (north). This is the plant shot 17 reverses.')

# 6 diagram: rule + implication
shot('s06-diagram', 18.0, 24.1, CARD, [
    comp('whatif/RingGlobe', {'decl': [{'t': round(t - 18.0, 2), 'v': round(math.degrees(decl_at(t)), 2)} for t in (18.0, 21.0, 24.1)],
                              'labels': [{'text': 'EQUATOR', 'at': 0.4}, {'text': 'BULGE', 'at': 1.0}], 'band': True},
         x='50%', y=900, width=980, height=980, depth=1),
], camera={'preset': 'pullOut', 'amount': 0.5}, sfx=[{'cue': 'whoosh', 'at': 0.0, 'volume': 0.3}],
    notes='EACH NOON. Caption 4 (rule) at 18.0, caption 5 (implication) at 22.0. HUD S plant: 21 ANCIENT CRATERS LINE AN OLD EQUATOR · WHY?')

# 7 textless break
shot('s07-textless', 24.1, 28.0, CARD, [
    comp('whatif/RingGlobe', {'decl': [{'t': round(t - 24.1, 2), 'v': round(math.degrees(decl_at(t)), 2)} for t in (24.1, 25.0, 26.0, 27.0, 28.0)], 'band': True},
         x='50%', y=900, width=980, height=980, depth=1),
], camera={'preset': 'pushIn', 'amount': 0.3}, sfx=[{'cue': 'riser', 'at': 0.0, 'volume': 0.35}],
    notes='Textless 24.1-28.0: Sun slides +15.4 -> +11.6 deg, band climbs toward the equator. No HUD S line, no caption.')

# 8 map wide (Americas), shadow creeps north
V8 = {'lon': -62, 'lat': 2, 'zoom': 5.5}
shot('s08-map-south', 28.0, 33.0, SEA, [
    map_layer(V8, pins=[MIAMI_PIN, pin(-43.17, -22.91, 'RIO', 0.2), pin(-77.04, -12.05, 'LIMA', 0.4)]),
    *band_layers(V8, 28.0, 33.0),
], camera={'keyframes': [{'t': 0, 'zoom': 1.0}, {'t': 5.0, 'zoom': 1.06, 'ease': 'linear'}]},
    sfx=[{'cue': 'whoosh', 'at': 0.0, 'volume': 0.25}],
    notes='Static map view lon -62 lat 2 zoom 5.5 (16.5 px/deg). Band rects from rings.py noon band (B / Cassini / A).')

# 9 Fortaleza
V9 = V8
shot('s09-fortaleza', 33.0, 38.3, SEA, [
    map_layer(V9, pins=[MIAMI_PIN, pin(-38.52, -3.73, 'FORTALEZA', 0.2, '#C9D3DD')]),
    *band_layers(V9, 33.0, 38.3, deepen=(33.5, 0.8)),
    comp('explainer/Tag', {'text': 'NOON · <1%', 'accent': GOLD, 'size': 0.7, 'at': 0.5}, x=880, y=1010, width=300, height=90, depth=1, z=20),
], camera={'keyframes': [{'t': 0, 'x': '50%', 'y': '50%', 'zoom': 1.06}, {'t': 2.5, 'x': 760, 'y': 1050, 'zoom': 1.5}, {'t': 5.3, 'x': 770, 'y': 1050, 'zoom': 1.55, 'ease': 'linear'}]},
    sfx=[{'cue': 'sonar_ping', 'at': 0.5, 'volume': 0.3}],
    notes='Push toward NE Brazil: Fortaleza under the B band (SEP 6-13), noon light <1% (EST.).')

# 10 equinox interrupt
shot('s10-equinox', 38.3, 41.0, ENDBG, [
    comp('whatif/RingGlobe', {'decl': [{'t': 0, 'v': 0.0}], 'edgeOn': True, 'band': True, 'shadowLine': True}, x='50%', y=900, width=1040, height=1040, depth=1),
    overlay('#FFF3D6', [(0.0, 0.0), (0.12, 1.0), (0.3, 1.0), (0.6, 0.0)], z=90),
], camera={'keyframes': []}, sfx=[{'cue': 'stinger', 'at': 0.0, 'volume': 0.6}],
    notes='SEP 23: white-gold glint, then the full-frame edge-on diagram: Sun in the ring plane, shadow = a line on the equator. Music cuts.')

# 11 map north
V11 = {'lon': -72, 'lat': 10, 'zoom': 7}
shot('s11-map-north', 41.0, 47.0, SEA, [
    map_layer(V11, pins=[MIAMI_PIN,
                         pin(-74.07, 4.71, 'BOGOTÁ', 0.0, '#C9D3DD'), pin(-74.07, 4.71, '', 0.33, '#5E6670'),
                         pin(-79.52, 8.98, 'PANAMA', 0.0, '#C9D3DD'), pin(-79.52, 8.98, '', 3.33, '#5E6670'),
                         pin(-66.88, 10.49, 'CARACAS', 0.0, '#C9D3DD'), pin(-66.88, 10.49, '', 4.33, '#5E6670')]),
    *band_layers(V11, 41.0, 47.0),
], camera={'keyframes': [{'t': 0, 'y': '50%', 'zoom': 1.0}, {'t': 6.0, 'y': 900, 'zoom': 1.08, 'ease': 'linear'}]},
    sfx=[{'cue': 'sonar_ping', 'at': a, 'volume': 0.3} for a in (0.33, 3.33, 4.33)],
    notes='Pins grey (duplicate grey pin, later `at`) on the stamp dates: OCT 02 Bogota, OCT 11 Panama City, OCT 14 Caracas.')

# 12 map Caribbean
V12 = {'lon': -79, 'lat': 18, 'zoom': 9}
shot('s12-map-caribbean', 47.0, 55.0, SEA, [
    map_layer(V12, pins=[MIAMI_PIN, pin(-82.37, 23.11, 'HAVANA', 0.0, '#C9D3DD'), pin(-82.37, 23.11, '', 6.33, '#5E6670')],
              rings=[{'lon': -80.13, 'lat': 25.79, 'r': 1.2, 'at': 5.0, 'color': GOLD}]),
    *band_layers(V12, 47.0, 55.0),
], camera={'preset': 'pushIn', 'amount': 0.6},
    sfx=[{'cue': 'heartbeat_slow', 'at': 5.0, 'volume': 0.35}, {'cue': 'sonar_ping', 'at': 6.33, 'volume': 0.3}],
    notes='Caribbean-wide (27 px/deg) so the crude Cuba polygon stays acceptable. Havana greys NOV 07 (53.3); Miami ring pulses from 52.0.')

# 13 contact
shot('s13-contact', 55.0, 60.0, NOON_SKY, [
    street('day', neonOn=False, neonFlickerAt=0.8),
    arch(0.4, dayside=True),
    you(430, 1330, 'stand'),
    you(760, 1380, 'stand', color='#E07A5F', w=140, h=240),
    {'type': 'rect', 'x': 540, 'y': 900, 'width': 260, 'height': 160, 'fill': '#0E1620', 'radius': 80, 'blur': 40, 'opacity': 0.55, 'depth': 1, 'z': 29,
     'keyframes': [{'t': 0, 'scale': 0.2}, {'t': 2.0, 'scale': 14, 'ease': 'in'}]},
    *shade([(0.0, 0.0), (1.9, 0.0), (2.2, 0.55), (5.0, 0.55)]),
    {'type': 'rect', 'x': 800, 'y': 1180, 'width': 300, 'height': 86, 'fill': '#FFFFFF', 'radius': 18, 'opacity': 0.95, 'depth': 1, 'z': 40, 'start': 1.8,
     'enter': {'type': 'pop', 'duration': 0.3}},
    {'type': 'text', 'text': '☀ SUNNY · 79°F', 'x': 800, 'y': 1180, 'fontSize': 38, 'font': 'display', 'weight': 800, 'color': '#1B2A4A', 'depth': 1, 'z': 41,
     'start': 1.8, 'enter': {'type': 'pop', 'duration': 0.3}},
], camera={'keyframes': [{'t': 0, 'zoom': 1.1}, {'t': 5.0, 'zoom': 1.0}]},
    sfx=[{'cue': 'impact', 'at': 0.0, 'volume': 0.6}],
    notes='EACH NOON. NOV 12: the shade grows out from the vanishing point down the street (soft rect scale), then holds at ~20% light. Centred ON YOU stamp (HUD). Passer-by phone pill = the weather-app gag.')

# 14 Cassini relief
shot('s14-cassini', 60.0, 63.0, NOON_SKY, [
    street('day', neonOn=True),
    arch(0.4, dayside=True),
    you(430, 1330, 'stand'),
    *shade([(0.0, 0.55), (0.6, 0.15), (3.0, 0.15)]),
    {'type': 'rect', 'x': 540, 'y': 1350, 'width': 1600, 'height': 220, 'fill': '#FFE7B0', 'opacity': 0.35, 'blur': 30, 'blend': 'screen', 'depth': 1, 'z': 32,
     'keyframes': [{'t': 0, 'y': 1000}, {'t': 3.0, 'y': 1700, 'ease': 'linear'}]},
], camera={'preset': 'drift', 'amount': 0.3}, sfx=[{'cue': 'ding', 'at': 0.0, 'volume': 0.35}],
    notes='NOV 27: Cassini Division, ~75% light. Caption 11.')

# 15 B ring
shot('s15-b-ring', 63.0, 68.0, NOON_SKY, [
    street('day', neonOn=True, palmsSilhouette=True),
    arch(0.4, dayside=True),
    you(430, 1330, 'stand'),
    *shade([(0.0, 0.15), (0.4, 0.9), (5.0, 0.9)]),
    *[{'type': 'circle', 'x': x, 'y': 1180, 'width': 120, 'height': 60, 'fill': '#FFF2C8', 'opacity': 0.8, 'blur': 18, 'blend': 'screen', 'depth': 1, 'z': 40}
      for x in (500, 590)],
    {'type': 'text', 'text': '12:00', 'x': 860, 'y': 640, 'fontSize': 64, 'font': MONO, 'weight': 700, 'color': '#FF7AC6', 'shadow': '0 0 18px rgba(255,122,198,.9)',
     'depth': 1, 'z': 41},
], camera={'preset': 'pushIn', 'amount': 0.6, 'shake': [{'at': 0.0, 'duration': 0.4, 'amplitude': 6}]},
    sfx=[{'cue': 'boom', 'at': 0.0, 'volume': 0.6}, {'cue': 'heartbeat', 'at': 0.0, 'volume': 0.4}],
    notes='DEC 6 -> DEC 21: B ring, ~2% light; headlights + neon only; neon 12:00 on a hotel fin. Caption 12 at 63.8; HUD region line at 66.6.')

# 16 JAN 30 relief
shot('s16-jan30', 68.0, 69.4, NOON_SKY, [
    street('day', neonOn=False),
    arch(0.4, dayside=True),
    you(430, 1330, 'stand'),
], camera={'keyframes': []}, transition={'type': 'whip', 'duration': 0.3, 'direction': 'left'},
    sfx=[{'cue': 'whoosh', 'at': 0.0, 'volume': 0.4}, {'cue': 'tick', 'at': 0.1, 'volume': 0.5}],
    notes='Labelled jump DEC 21 -> JAN 30: full sun, HUD RING SHADOW GONE / 79 DAYS IN SHADOW (relief).')

# 17 twist: unlit side
shot('s17-unlit', 69.4, BLACK_AT, NIGHT_SKY, [
    street('night', streetlights=True, neonOn=True),
    arch(-1, stars=True),
    you(560, 1330, 'stand', w=170, h=280, z=10),
], camera={'keyframes': [{'t': 0, 'y': 1000, 'zoom': 1.0}, {'t': 3.2, 'y': 780, 'zoom': 0.96}]},
    sfx=[{'cue': 'stinger', 'at': 0.0, 'volume': 0.4}],
    notes='EACH MIDNIGHT, JAN 30+: unlit side (B black and starless, A dim translucent glow, stars through Cassini). Same spot as shot 5, no ringlight shadow. Caption 13; HUD RETURNS IN 286.0 DAYS.')

# 18 black (countdown keeps ticking, centred)
shot('s18-black', BLACK_AT, 74.0, BLACK, [], sfx=[{'cue': 'clock_ticking', 'at': 0.0, 'volume': 0.25}],
     notes='Near-black; the HUD shows only the return countdown, small and centred (centreFrom). No music.')

# 19 end card
END_FACT = '466 MILLION YEARS AGO · A RING MAY HAVE LEFT THOSE CRATERS\nAND CHILLED THE PLANET'
shot('s19-endcard', 74.0, 79.0, ENDBG, [
    *title_layers(0.0, 5.0, enter=True),
    {'type': 'text', 'text': END_FACT, 'x': '50%', 'y': 1010, 'fontSize': 34, 'font': 'display', 'weight': 700, 'color': '#D9DEE3',
     'letterSpacing': 0.08, 'lineHeight': 1.4, 'maxWidth': 880, 'start': 0.5, 'enter': {'type': 'fade', 'duration': 0.6}, 'depth': 0, 'z': 60},
], sfx=[{'cue': 'ding', 'at': 0.0, 'volume': 0.25}], notes='Exact title repeat + fact closing the 0:18.5 crater plant (not read).')

# ------------------------------------------------------------------ assemble
scenes = []
for sh in SHOTS:
    start, end = sh['start'], sh['end']
    layers = list(sh['layers'])
    if start < 74.0:
        layers.append(comp('whatif/Hud', {'t0': start, 'lines': HUD, 'scrubber': SCRUBBER, 'stamps': STAMPS, 'mono': MONO, 'serif': SERIF,
                                          'accent': GOLD, 'minimal': start >= BLACK_AT},
                           id='hud', x=70, y=250, anchorX=0, anchorY=0, width=860, height=360, depth=0, z=80))
    for cs, ce, text in CAPTIONS:
        if ce <= start or cs >= end:
            continue
        ls, le = max(cs, start) - start, min(ce, end) - start
        cap = {'type': 'text', 'text': text, 'x': '50%', 'y': 1400, 'fontSize': 62, 'font': SERIF, 'weight': 500,
               'color': '#FFFFFF', 'maxWidth': 860, 'lineHeight': 1.15, 'shadow': '0 3px 14px rgba(0,0,0,.6)',
               'start': round(ls, 3), 'end': round(le, 3), 'depth': 0, 'z': 70}
        if cs >= start:
            cap['enter'] = {'type': 'fade', 'duration': 0.25}
        if ce <= end:
            cap['exit'] = {'type': 'fade', 'duration': 0.25}
        layers.append(cap)
    scene = {'id': sh['id'], 'duration': round(end - start, 3), 'background': sh['background'], 'layers': layers,
             'notes': sh['notes'] + f' [screen {start:.1f}-{end:.1f} s]'}
    for key, field in (('camera', 'camera'), ('transition', 'transitionIn'), ('grade', 'grade'), ('sfx', 'sfx')):
        if sh[key]:
            scene[field] = sh[key]
    scenes.append(scene)

storyboard = {
    'version': 1,
    'id': 'whatif-earth-had-rings',
    'title': 'What if Earth had rings like Saturn?',
    'format': '9:16',
    'fps': 30,
    'theme': {'fontDisplay': 'Montserrat', 'fontBody': 'Montserrat', 'fontCondensed': 'Anton', 'accent': GOLD, 'ink': '#0B0D10', 'paper': '#FFFFFF'},
    'scenes': scenes,
    'captions': {'enabled': False},
    'audio': {
        'voice': [],
        'music': [
            {'src': 'music/documentary_pulse.m4a', 'start': 7.0, 'end': 38.3, 'volume': 0.22, 'duckTo': 0.1, 'fadeIn': 0.3, 'fadeOut': 0.1},
            {'src': 'music/tension_pulse.m4a', 'start': 41.0, 'end': 63.0, 'volume': 0.22, 'duckTo': 0.1, 'fadeIn': 0.4, 'fadeOut': 0.2},
            {'src': 'music/dread.m4a', 'start': 63.0, 'end': 69.4, 'volume': 0.22, 'duckTo': 0.12, 'fadeIn': 0.1, 'fadeOut': 0.6},
            {'src': 'music/documentary_pulse.m4a', 'start': 74.0, 'end': 79.0, 'volume': 0.18, 'duckTo': 0.18, 'fadeIn': 0.6, 'fadeOut': 0.8},
            {'src': 'sfx/drone.wav', 'start': 28.0, 'end': BLACK_AT, 'volume': 0.18, 'duckTo': 0.15, 'fadeIn': 0.5, 'fadeOut': 0.3, 'loop': True},
        ],
        'sfx': [],
        'duckOn': 'voice',
    },
    'overlays': {'grain': 0.03, 'vignette': 0.1, 'fadeIn': 0, 'fadeOut': 0.4},
}

with open(OUT, 'w') as f:
    json.dump(storyboard, f, indent=1, ensure_ascii=False)
    f.write('\n')
print(f'wrote {OUT}: {len(scenes)} scenes, {sum(s["duration"] for s in scenes):.2f} s')
