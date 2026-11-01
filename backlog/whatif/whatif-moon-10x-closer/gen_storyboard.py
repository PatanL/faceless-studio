#!/usr/bin/env python3
"""Generate storyboard.json for whatif-moon-10x-closer from the script's tide model, caption list,
HUD state table and shot list (keep in sync with script.md). Output path is argv[1].

One tide model drives every number: the HUD SEA LEVEL meter, the Cliffs seaLevel track, the Moon's
az/alt/phase and the sky clock. Story hours t = screen seconds - 8, time-lapse 1 hour per second."""
import json
import math
import sys

OUT = sys.argv[1]

SERIF = '"Source Serif 4", "DejaVu Serif", Georgia, serif'
MONO = 'JetBrains Mono'
SILVER = '#CFE3FF'   # keyword / HUD accent (moon-silver)
INK = '#0B0D10'

# ------------------------------------------------------------------ tide model (see script.md "Tide model")
LAT = math.radians(51.15)
K = 0.357 * 1000 * 0.69          # m: today's equilibrium lunar tide x 1/d^3 x (1 + k2 - h2)
RATE = 360 / 20.7 - 360 / 23.934  # deg per story hour (hour angle decreases: west -> east)


def _h_of_H(hdeg):
    c = math.cos(LAT) * math.cos(math.radians(hdeg))
    return K * (3 * c * c - 1) / 2


def _solve_h0():
    lo, hi = 0.0, 90.0
    for _ in range(60):
        m = (lo + hi) / 2
        if _h_of_H(m) > 0:
            lo = m
        else:
            hi = m
    return lo


H0 = _solve_h0()                         # ~23.0 deg: sea starts exactly at today's level
T_RETURN = (180 - 2 * H0) / RATE         # ~57.0 h -> clock 57:00:00 at 1 h/s, zero at 1:05.0
T_HIGH = (180 - H0) / RATE               # ~66.8 h, +22 m


def story_t(s):
    return max(0.0, s - 8.0)


def sea_level(s):
    return _h_of_H(H0 + RATE * story_t(s))


def moon_altaz(s):
    H = math.radians(-(H0 + RATE * story_t(s)))
    alt = math.asin(math.cos(LAT) * math.cos(H))
    az = math.atan2(-math.sin(H), -math.sin(LAT) * math.cos(H))
    return math.degrees(alt), math.degrees(az) % 360


def elongation(s):
    return (145 + 17.4 * story_t(s)) % 360


def clock_hour(s):
    return (19.0 + story_t(s)) % 24


def moon_size_deg(s):
    """Apparent size follows 1/d with ease-out on 1/d during the hook; 5.78 deg after arrival."""
    if s >= 8:
        return 5.78
    p = 1 - (1 - s / 8) ** 3
    inv = 1 / 384400 + (1 / 38440 - 1 / 384400) * p
    return 0.523 * (384400 * inv)


def sampled(fn, s0, s1, step=0.5, nd=2):
    out, s = [], s0
    while s < s1 - 1e-9:
        out.append({'t': round(s - s0, 3), 'v': round(fn(s), nd), 'ease': 'linear'})
        s += step
    out.append({'t': round(s1 - s0, 3), 'v': round(fn(s1), nd), 'ease': 'linear'})
    return out


# ------------------------------------------------------------------ captions (global seconds)
CAPTIONS = [
    (5.0, 8.0, "You're under the White Cliffs of Dover."),
    (10.0, 13.5, 'You can read a book by moonlight.'),
    (15.0, 18.5, 'But its tides are 1,000 times stronger.'),
    (19.0, 20.8, 'So the sea keeps leaving.'),
    (24.5, 27.5, 'Ferries sit on the bare seabed.'),
    (28.0, 31.0, 'The North Sea floor is dry land.'),
    (31.5, 34.5, 'You could walk to France from here.'),
    (39.5, 43.0, 'TV satellites are flung from orbit.'),
    (44.0, 47.5, 'GPS satellites get yanked off course.'),
    (48.5, 52.0, 'Solid ground heaves like a tide.'),
    (65.3, 68.0, 'The tide is back at the old shoreline.'),
    (68.3, 70.8, 'Then it climbs over where you stood.'),
    (71.0, 73.5, 'And the Moon is falling toward us.'),
]

# ------------------------------------------------------------------ HUD state table (global seconds)
HUD = {
    'L': [
        {'from': 0, 'to': 8, 'text': 'THE MOON'},
        {'from': 8, 'to': 65, 'text': 'SEA BACK IN'},
        {'from': 65, 'to': 73.5, 'text': 'SEA BACK'},
    ],
    'N': [
        {'from': 0, 'to': 8, 'text': '{v} KM', 'formula': 'd = 1/(1/384400 + (1/38440 - 1/384400)*easeOutCubic(t/8))',
         'decimals': 0, 'thousands': True},
        {'from': 8, 'to': 65, 'text': '{hms}', 'formula': f'hours_left = {T_RETURN:.4f} - (t-8)  # 1 hour per second', 'clampMin': 0},
        {'from': 65, 'to': 68.3, 'text': '00:00:00'},
    ],
    'S1': [
        {'from': 0, 'to': 8, 'text': 'DRIFTS 3.8 CM AWAY EACH YEAR'},
        {'from': 8, 'to': 65, 'text': '1 HOUR PER SECOND'},
        {'from': 65, 'to': 68.3, 'text': 'DOVER, 57 HOURS LATER'},
        {'from': 68.3, 'to': 73.5, 'text': 'DOVER, 67 HOURS LATER'},
    ],
    'S2': [
        {'from': 8.5, 'to': 68.3, 'text': 'SEA LEVEL {v} M (EST.)', 'track': [dict(k, t=round(k['t'] + 8.5, 3)) for k in sampled(sea_level, 8.5, 68.3, 0.5, 1)], 'decimals': 0, 'sign': True},
        {'from': 68.3, 'to': 73.5, 'text': 'SEA LEVEL +22 M OR MORE (EST.)'},
    ],
    'S3': [
        {'from': 8.5, 'to': 14.5, 'text': '120× BRIGHTER'},
        {'from': 28.0, 'to': 31.5, 'text': 'LAST THIS LOW: 20,000 YEARS AGO'},
        {'from': 48.5, 'to': 55.0, 'text': 'GROUND TIDE ~130 M (EST.)'},
        {'from': 55.0, 'to': 73.5, 'text': 'MOON {v} KM',
         'formula': 'km = 38440 - 0.00137083*story_hours; story_hours = t-8 (to 65), then 66.8 from 68.3', 'decimals': 3, 'thousands': True},
    ],
    'S4': [
        {'from': 69.3, 'to': 71.0, 'text': 'LONDON FLOODS TWICE A WEEK'},
        {'from': 71.5, 'to': 73.5, 'text': 'TORN APART IN ~500 YEARS (EST.)'},
    ],
}

# ------------------------------------------------------------------ helpers
SILVER_GRADE = {'hue': 8, 'saturate': 0.85, 'brightness': 1.08, 'contrast': 1.03, 'vignette': 0.2}
BLUEHOUR = {'saturate': 1.0, 'vignette': 0.15}


def comp(name, props=None, **kw):
    layer = {'type': 'component', 'name': name, 'props': props or {}}
    layer.update(kw)
    return layer


def cliffs_bg(s0, s1, bearing=144, fov=30, horizon=0.8, **props):
    p = {'bearing': bearing, 'fovH': fov, 'horizonY': horizon,
         'clockHour': sampled(clock_hour, s0, s1, 0.5, 3) if s0 >= 8 else 19.0,
         'seaLevel': sampled(sea_level, s0, s1, 0.5, 1), 'wrackLine': True}
    p.update(props)
    return {'type': 'component', 'name': 'whatif/Cliffs', 'props': p, 'depth': 0.1, 'overscan': 1.15}


def moon(s0, s1, bearing=144, fov=30, horizon=0.8, **props):
    p = {'bearing': bearing, 'fovH': fov, 'horizonY': horizon,
         'az': sampled(lambda s: moon_altaz(s)[1], s0, s1, 0.5, 2),
         'alt': sampled(lambda s: moon_altaz(s)[0], s0, s1, 0.5, 2),
         'sizeDeg': sampled(moon_size_deg, s0, s1, 0.25 if s0 < 8 else 1.0, 3),
         'elongation': sampled(elongation, s0, s1, 0.5, 1),
         'earthshine': 0.35, 'glow': 0.6, 'maria': 'default'}
    p.update(props)
    return comp('whatif/Moon', p, id='moon', x='50%', y='50%', width=1080, height=1920, depth=0, z=5)


def orbit_bg(**props):
    p = {'earthR_px': 68, 'moonRing_km': 38440, 'geo_km': 42164, 'gps_km': 26560, 'fitKm': 45000,
         'terminator': True, 'continents': False}
    p.update(props)
    return {'type': 'component', 'name': 'whatif/OrbitView', 'props': p, 'depth': 0.1, 'overscan': 1.2}


def tag(text, x, y, at, **kw):
    return comp('explainer/Tag', {'text': text, 'at': at, 'color': SILVER}, x=x, y=y, **kw)


SHOTS = []


def shot(sid, start, end, background, layers=(), camera=None, transition=None, grade=None, sfx=(), notes='', hud=True):
    SHOTS.append(dict(id=sid, start=start, end=end, background=background, layers=list(layers), camera=camera,
                      transition=transition, grade=grade, sfx=list(sfx), notes=notes, hud=hud))


def title_layers(start, end, enter=True, exit_at=None):
    ls = [
        {'type': 'text', 'text': 'What if the Moon was', 'x': '50%', 'y': 760, 'fontSize': 84, 'font': SERIF, 'weight': 600,
         'color': '#FFFFFF', 'maxWidth': 920, 'depth': 0, 'z': 60, 'shadow': '0 4px 18px rgba(0,0,0,.5)'},
        {'type': 'text', 'text': '10 times closer?', 'x': '50%', 'y': 880, 'fontSize': 120, 'font': SERIF, 'weight': 700,
         'color': SILVER, 'maxWidth': 960, 'depth': 0, 'z': 60, 'shadow': '0 4px 18px rgba(0,0,0,.5)'},
    ]
    for l in ls:
        l['start'] = start
        l['end'] = end
        if enter:
            l['enter'] = {'type': 'fade', 'duration': 0.4}
        if exit_at is not None:
            l['exit'] = {'type': 'fade', 'at': exit_at, 'duration': end - exit_at}
    return ls


BOOK_SVG = (
    '<svg viewBox="0 0 900 520" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M450 70 C330 30 170 30 60 70 L60 470 C170 430 330 430 450 470 Z" fill="#E9EEF5"/>'
    '<path d="M450 70 C570 30 730 30 840 70 L840 470 C730 430 570 430 450 470 Z" fill="#F4F7FB"/>'
    '<g stroke="#9AA6B8" stroke-width="7" stroke-linecap="round">'
    '<path d="M110 130 H400"/><path d="M110 175 H390"/><path d="M110 220 H405"/><path d="M110 265 H380"/>'
    '<path d="M500 130 H790"/><path d="M500 175 H780"/><path d="M500 220 H795"/><path d="M500 265 H760"/></g>'
    '<path d="M560 300 C600 270 680 280 720 330 L700 470 L590 470 Z" fill="#1B2433" opacity="0.55"/>'
    '<path d="M0 520 C40 380 120 330 170 360 L240 520 Z" fill="#C9A88E"/>'
    '<path d="M900 520 C860 380 780 330 730 360 L660 520 Z" fill="#C9A88E"/>'
    '</svg>'
)

ARROW_SVG = ('<svg viewBox="0 0 120 400" xmlns="http://www.w3.org/2000/svg"><path d="M60 10 V340" stroke="#CFE3FF" '
             'stroke-width="10" stroke-dasharray="22 14"/><path d="M20 320 L60 390 L100 320 Z" fill="#CFE3FF"/></svg>')

# ------------------------------------------------------------------ shots
# 1 hook
shot('s01-hook', 0.0, 8.0, cliffs_bg(0.0, 8.0, sky='blueHour'), [
    moon(0.0, 8.0),
    *title_layers(0.0, 4.5, enter=False, exit_at=4.1),
], camera={'preset': 'none'}, grade=BLUEHOUR,
    sfx=[*[{'cue': 'tick', 'at': round(i * 0.25, 2), 'volume': 0.35} for i in range(32)], {'cue': 'riser', 'at': 5.0, 'volume': 0.5}],
    notes='Frame 1 = cover. St Margaret\'s Bay, bearing 144, fovH 30, horizon y 80%. Moon size from the 1/d ease-out '
          '(19 px + halo at 0:00, 75 px at 0:01, 208 px at 0:08); HUD distance derived from the same curve. Static camera.')

# 2 flip
shot('s02-flip', 8.0, 9.5, cliffs_bg(8.0, 9.5, sky='night', glitter=1.0), [moon(8.0, 9.5)],
     camera={'keyframes': [], 'shake': [{'at': 0.0, 'duration': 0.35, 'amplitude': 10}]}, grade=SILVER_GRADE,
     sfx=[{'cue': 'boom', 'at': 0.0, 'volume': 0.9}],
     notes='Moon locks at 5.78 deg; grade snaps to silver; HUD flips to SEA BACK IN 57:00:00 / 1 HOUR PER SECOND; SEA LEVEL meter at 0:08.5.')

# 3 POV book
shot('s03-pov-book', 9.5, 15.0, {'type': 'gradient', 'kind': 'linear', 'angle': 180, 'colors': ['#1F3B66', '#6E8DB8'], 'depth': 0.05, 'overscan': 1.2}, [
    moon(9.5, 15.0, bearing=140, fov=40, horizon=1.15),
    {'type': 'svg', 'markup': BOOK_SVG, 'x': '50%', 'y': 1560, 'width': 1000, 'height': 580, 'depth': 0, 'z': 20,
     'idle': [{'type': 'sway', 'amount': 1.5, 'speed': 0.25}]},
], camera={'preset': 'pushIn', 'amount': 0.3}, grade=SILVER_GRADE, sfx=[{'cue': 'whoosh', 'at': 0.0, 'volume': 0.25}],
    notes='POV looking up SSE: your hands hold an open book lit by the full giant Moon (full at 0:10), thumb shadow on the page. HUD 120x BRIGHTER.')

# 4 rule
shot('s04-rule', 15.0, 19.0, cliffs_bg(15.0, 19.0, sky='clock'), [
    moon(15.0, 19.0),
    {'type': 'svg', 'markup': ARROW_SVG, 'x': 700, 'y': 900, 'width': 120, 'height': 400, 'start': 0.3, 'enter': {'type': 'fade', 'duration': 0.4}, 'z': 15},
    tag('×1,000', 820, 980, 0.4, z=16),
], camera={'preset': 'drift', 'amount': 0.4}, grade=SILVER_GRADE, sfx=[{'cue': 'stinger', 'at': 0.0, 'volume': 0.4}],
    notes='Night 02:00-06:00, last-quarter Moon; the waterline far out on the chalk platform (-37 -> -60 m).')

# 5 dawn drain (textless from 20.8)
shot('s05-dawn-drain', 19.0, 24.5, cliffs_bg(19.0, 24.5, bearing=125, sky='clock', seabedBands=True), [
    moon(19.0, 24.5, bearing=125),
], camera={'preset': 'none'}, grade={'saturate': 1.0, 'vignette': 0.12}, sfx=[{'cue': 'whoosh_long', 'at': 0.5, 'volume': 0.4}],
    notes='Sunrise at 0:19; the sea drains to the horizon (-60 -> -91 m); dark new Moon with earthshine low in the ESE beside the Sun. Textless 20.8-24.5.')

# 6 ferry
shot('s06-ferry', 24.5, 28.0, cliffs_bg(24.5, 28.0, bearing=125, sky='clock', seabedBands=True), [
    moon(24.5, 28.0, bearing=125),
    comp('whatif/Ferry', {'tilt': 7, 'livery': 'white-blue'}, x=560, y=1330, width=520, height=170, z=12),
], camera={'preset': 'pushIn', 'amount': 0.4}, grade={'saturate': 1.0, 'vignette': 0.12},
    sfx=[{'cue': 'door_creak', 'at': 0.5, 'volume': 0.25}],
    notes='A cross-Channel ferry aground ~2 km offshore on dry chalk seabed; crescent Moon pale in the day sky.')

# 7 North Sea map
NS_ZONES = [
    {'points': [[1.2, 51.3], [1.9, 51.2], [1.9, 50.8], [1.2, 50.85]], 'at': 0.0, 'color': '#D8C08E', 'style': 'solid'},
    {'points': [[1.5, 51.6], [4.2, 51.6], [6.5, 53.3], [4.5, 55.5], [1.5, 55.2], [0.5, 53.5]], 'at': 0.3, 'color': '#D8C08E', 'style': 'solid'},
    {'points': [[-1.5, 57.0], [8.0, 57.0], [8.6, 55.0], [8.0, 53.6], [4.0, 51.4], [-0.5, 53.0], [-2.0, 55.5]], 'at': 0.8, 'color': '#CDB27C', 'style': 'solid'},
]
shot('s07-northsea', 28.0, 31.5, {'type': 'color', 'color': '#123047', 'depth': 0, 'overscan': 1.0}, [
    comp('explainer/Map', {'views': [{'t': 0, 'lon': 3.5, 'lat': 54.0, 'zoom': 30}, {'t': 3.5, 'lon': 3.5, 'lat': 54.0, 'zoom': 26}],
                           'detailRegion': 'channel', 'detailZoom': 4, 'zones': NS_ZONES, 'grid': False,
                           'trench': {'points': [[4.5, 58.5], [6.0, 57.6], [8.5, 57.8], [10.5, 59.0]], 'color': '#1E5A8A'}},
         x='50%', y='50%', width=1080, height=1920),
    tag('DOGGERLAND', 470, 820, 0.9, z=20),
], transition={'type': 'whip', 'duration': 0.3, 'direction': 'up'}, sfx=[{'cue': 'whoosh', 'at': 0.0, 'volume': 0.5}],
    notes='Map zoom 30 -> 26 (base 3 px/deg): southern North Sea shelf in sand colour, Norwegian Trench blue; DOGGERLAND tag. HUD LAST THIS LOW: 20,000 YEARS AGO.')

# 8 strait map
shot('s08-strait', 31.5, 34.5, {'type': 'color', 'color': '#123047', 'depth': 0, 'overscan': 1.0}, [
    comp('explainer/Map', {'views': [{'t': 0, 'lon': 3.5, 'lat': 54.0, 'zoom': 30}, {'t': 0.6, 'lon': 1.48, 'lat': 51.01, 'zoom': 500, 'ease': 'inOut'}, {'t': 3.0, 'lon': 1.48, 'lat': 51.01, 'zoom': 500}],
                           'detailRegion': 'channel', 'detailZoom': 4, 'grid': False,
                           'zones': [{'points': [[1.25, 51.25], [1.75, 51.2], [1.8, 50.8], [1.3, 50.82]], 'at': 0.0, 'color': '#D8C08E', 'style': 'solid'},
                                     {'points': [[1.47, 51.02], [1.5, 51.03], [1.52, 51.0], [1.48, 50.99]], 'at': 0.0, 'color': '#2C6E9E', 'style': 'solid'},
                                     {'points': [[1.55, 50.96], [1.58, 50.97], [1.59, 50.94], [1.56, 50.93]], 'at': 0.0, 'color': '#2C6E9E', 'style': 'solid'}],
                           'pins': [{'lon': 1.38, 'lat': 51.15, 'label': 'YOU', 'at': 0.7}, {'lon': 1.58, 'lat': 50.87, 'label': 'CAP GRIS-NEZ', 'at': 0.9}],
                           'paths': [{'points': [[1.38, 51.15], [1.58, 50.87]], 'at': 1.0, 'duration': 1.5, 'dash': [18, 12], 'label': '33 KM', 'color': SILVER}]},
         x='50%', y='50%', width=1080, height=1920),
], sfx=[{'cue': 'pop', 'at': 0.7, 'volume': 0.5}, {'cue': 'pop', 'at': 0.9, 'volume': 0.5}, {'cue': 'click', 'at': 2.5, 'volume': 0.5}],
    notes='Zoom to the strait (frame ~50 km wide at zoom 500); dotted 33 km walking line YOU -> CAP GRIS-NEZ; Fosses Dangeard as two small pools.')

# 9 moonset at low water (textless)
shot('s09-moonset', 34.5, 38.5, cliffs_bg(34.5, 38.5, bearing=90, fov=40, horizon=0.62, sky='clock', seabedBands=True, dryToHorizon=True), [
    moon(34.5, 38.5, bearing=90, fov=40, horizon=0.62),
], camera={'preset': 'none'}, grade=SILVER_GRADE,
    notes='Looking east: lower limb touches at 0:34.6, centre on the horizon at 0:36.5 = lowest water (-123 m), gone at 0:38.4; light drains with it.')

# 10 black
shot('s10-black', 38.5, 39.5, {'type': 'color', 'color': '#000000', 'depth': 0, 'overscan': 1.0}, [
    {'type': 'particles', 'preset': 'stars', 'count': 140, 'color': '#FFFFFF', 'size': [1, 3], 'speed': 0.2, 'seed': 11,
     'x': '50%', 'y': '50%', 'width': 1080, 'height': 1920},
], notes='Black with stars, music out; HUD only.')

# 11 TV satellites
shot('s11-geo', 39.5, 44.0, orbit_bg(moonAngle=[{'t': 0, 'v': 200}, {'t': 4.5, 'v': 278}],
                                     geoScatter=[{'t': 0, 'v': 0}, {'t': 1.0, 'v': 0}, {'t': 4.5, 'v': 1}], showGps=False), [
    tag('3,700 KM', 820, 520, 1.2, z=20),
], transition={'type': 'fade', 'duration': 0.4}, camera={'preset': 'drift', 'amount': 0.3},
    sfx=[{'cue': 'stinger', 'at': 0.0, 'volume': 0.5}],
    notes='Moon ring 820 px, GEO dot ring 900 px; the Moon passes the GEO dots and they scatter off the ring. Leader-line tag on the 3,700 km gap.')

# 12 GPS
shot('s12-gps', 44.0, 48.5, orbit_bg(moonAngle=[{'t': 0, 'v': 278}, {'t': 4.5, 'v': 356}], geoScatter=1, showGps=True,
                                     gpsWobble=[{'t': 0, 'v': 0}, {'t': 4.5, 'v': 1}], fitKm=30000), [
    tag('GPS 20,200 KM UP', 300, 1250, 0.5, z=20),
], camera={'preset': 'pushIn', 'amount': 0.4}, sfx=[{'cue': 'glitch', 'at': 1.0, 'volume': 0.25}],
    notes='Zoomed to the GPS ring (26,560 km); its dots wobble and drift off their dotted ring.')

# 13 ground tide diagram
shot('s13-ground', 48.5, 52.0, {'type': 'gradient', 'kind': 'linear', 'angle': 180, 'colors': ['#16263A', '#22384F'], 'depth': 0.1, 'overscan': 1.2}, [
    comp('whatif/DiagramCard', {'kind': 'groundTide', 'at': 0.0, 'bars': [{'text': '110 M', 'of': 'cliff'}, {'text': '130 M', 'of': 'groundTide', 'at': 0.8}],
                                'heave': [{'t': 0, 'v': 0}, {'t': 1.75, 'v': 1, 'ease': 'inOut'}, {'t': 3.5, 'v': 0, 'ease': 'inOut'}]},
         x='50%', y=900, width=920, height=920),
], sfx=[{'cue': 'boom', 'at': 0.3, 'volume': 0.3}],
    notes='Cliff cross-section: dashed today ground line; the ground block rises and sinks; 110 M cliff bar vs 130 M ground-tide arrow.')

# 14 sea floods back (race, textless)
shot('s14-flood-back', 52.0, 58.0, cliffs_bg(52.0, 58.0, bearing=125, sky='clock', seabedBands=True), [
    comp('whatif/Ferry', {'tilt': 7, 'livery': 'white-blue'}, x=560, y=1330, width=520, height=170, z=12),
], camera={'preset': 'none'},
    notes='Sunset at 0:55 mid-shot (sky from clockHour); the sea floods back across the seabed (-72 -> -37 m); ferry still aground. Moon below horizon.')

# 15 foam line races the wrack line
shot('s15-wrack-race', 58.0, 65.0, cliffs_bg(58.0, 65.0, bearing=144, fov=50, horizon=0.55, sky='clock', closeShingle=True), [],
     camera={'preset': 'pushIn', 'amount': 0.3},
     sfx=[*[{'cue': 'tick', 'at': round(4.0 + i * 0.125, 3), 'volume': 0.4} for i in range(24)], {'cue': 'riser', 'at': 3.0, 'volume': 0.5}],
     notes='Low close on the shingle at night: the foam line races up toward the seaweed tideline from 0:00 and reaches it at 1:05.0 (-37 -> 0 m).')

# 16 callback
shot('s16-callback', 65.0, 68.3, cliffs_bg(65.0, 68.3, sky='clock'), [], transition={'type': 'glitch', 'duration': 0.2},
     camera={'preset': 'none'}, sfx=[{'cue': 'impact', 'at': 0.0, 'volume': 0.8}],
     notes='Exact 0:00 framing (bearing 144, fovH 30). Night 04:00, empty sky where the Moon hung (below the horizon, far side), sea at the wrack line.')

# 17 drowned cutaway
shot('s17-drowned', 68.3, 71.0, {'type': 'component', 'name': 'explainer/Ocean',
                                  'props': {'surface': 0.22, 'skyTop': '#5FA8E8', 'skyBottom': '#BFE0F7', 'depth': 20, 'rays': 0.6, 'snow': 0.2},
                                  'depth': 0.1, 'overscan': 1.15}, [
    comp('whatif/Cliffs', {'variant': 'drownedSilhouette', 'bearing': 144, 'fovH': 30, 'horizonY': 0.8, 'seaLevel': 22, 'wrackLine': True},
         x='50%', y='50%', width=1080, height=1920, z=2, opacity=0.85),
    {'type': 'component', 'name': 'explainer/You', 'x': 540, 'y': 1500, 'width': 200, 'height': 330,
     'props': {'pose': 'stand', 'ghost': True, 'outline': '#FFFFFF', 'dash': [10, 8]}, 'opacity': 0.8, 'z': 10},
    comp('explainer/ScaleBar', {'at': 0.3, 'from': 'center', 'barY': 422, 'length': 1080, 'label': '18 M', 'vertical': True, 'color': '#FFFFFF'},
         x=760, y=960, width=200, height=1100, z=12),
], camera={'preset': 'pushIn', 'amount': 0.3}, sfx=[{'cue': 'boom', 'at': 0.0, 'volume': 0.4}, {'cue': 'bubbles', 'at': 0.2, 'volume': 0.3}],
    notes='Same bearing, 14:00: surface at y 22%; underwater the drowned shingle, wrack line and cliff foot; ghost YOU at the old spot; 18 M bar. HUD LONDON FLOODS TWICE A WEEK at 1:09.3.')

# 18 falling Moon
shot('s18-falling', 71.0, 73.5, orbit_bg(moonAngle=[{'t': 0, 'v': 10}, {'t': 2.5, 'v': 60}], geoScatter=1, showGps=False,
                                         spiral={'turns': 1.2, 'shrink': 0.12, 'label': None}, roche={'km': 18000, 'label': '18,000 KM', 'dash': [14, 10]}), [],
     camera={'preset': 'pushIn', 'amount': 0.5}, sfx=[{'cue': 'riser', 'at': 0.0, 'volume': 0.4}],
     notes='The Moon ring tightens on a visible spiral (an exaggerated animation of the trend); dashed Roche ring; MOON meter ticking. HUD TORN APART IN ~500 YEARS (EST.).')

# 19 black
shot('s19-black', 73.5, 74.3, {'type': 'color', 'color': '#000000', 'depth': 0, 'overscan': 1.0}, [], notes='Black, HUD hidden.', hud=False)

# 20 end card
END_FACT = 'REAL MOON: 3.8 CM FARTHER EACH YEAR\nLASER-TIMED OFF APOLLO 11 MIRRORS'
shot('s20-endcard', 74.3, 80.0, {'type': 'color', 'color': INK, 'depth': 0, 'overscan': 1.0}, [
    *title_layers(0.0, 5.7, enter=True),
    {'type': 'text', 'text': END_FACT, 'x': '50%', 'y': 1080, 'fontSize': 36, 'font': 'display', 'weight': 700, 'color': '#D9DEE3',
     'letterSpacing': 0.08, 'lineHeight': 1.4, 'maxWidth': 900, 'start': 0.5, 'enter': {'type': 'fade', 'duration': 0.6}, 'depth': 0, 'z': 60},
], sfx=[{'cue': 'ding', 'at': 0.5, 'volume': 0.25}], notes='Exact title repeat + 12-word fact held 5.2 s (neither is read).', hud=False)

# ------------------------------------------------------------------ assemble
scenes = []
for sh in SHOTS:
    start, end = sh['start'], sh['end']
    dur = round(end - start, 3)
    layers = list(sh['layers'])
    if sh['hud'] and start < 73.5:
        layers.append(comp('whatif/Hud', {'t0': start, 'lines': HUD, 'mono': MONO, 'accent': SILVER, 'maxChars': 32},
                           id='hud', x=70, y=250, anchorX=0, anchorY=0, width=640, height=380, depth=0, z=80))
    for cs, ce, text in CAPTIONS:
        if ce <= start or cs >= end:
            continue
        ls, le = max(cs, start) - start, min(ce, end) - start
        cap = {'type': 'text', 'text': text, 'x': '50%', 'y': 1400, 'fontSize': 60, 'font': SERIF, 'weight': 600, 'italic': True,
               'color': '#FFFFFF', 'maxWidth': 860, 'lineHeight': 1.15, 'shadow': '0 3px 14px rgba(0,0,0,.65)',
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
    'id': 'whatif-moon-10x-closer',
    'title': 'What if the Moon was 10 times closer?',
    'format': '9:16',
    'fps': 30,
    'theme': {'fontDisplay': 'Montserrat', 'fontBody': 'Montserrat', 'fontCondensed': 'Anton', 'accent': SILVER, 'ink': INK, 'paper': '#FFFFFF'},
    'scenes': scenes,
    'captions': {'enabled': False},
    'audio': {
        'voice': [],
        'music': [
            {'src': 'music/documentary_pulse.m4a', 'start': 0.0, 'end': 38.5, 'volume': 0.22, 'duckTo': 0.22, 'fadeIn': 0.5, 'fadeOut': 2.0},
            {'src': 'sfx/underwater_rumble.wav', 'start': 8.0, 'end': 38.5, 'volume': 0.25, 'duckTo': 0.25, 'fadeIn': 0.5, 'fadeOut': 2.0, 'loop': True},
            {'src': 'music/tension_pulse.m4a', 'start': 39.5, 'end': 73.5, 'volume': 0.22, 'duckTo': 0.22, 'fadeIn': 0.3, 'fadeOut': 0.8},
            {'src': 'sfx/clock_ticking.wav', 'start': 52.0, 'end': 65.0, 'volume': 0.35, 'duckTo': 0.35, 'fadeIn': 0.2, 'fadeOut': 0.1, 'loop': True},
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
print(f'wrote {OUT}: {len(scenes)} scenes, {total:.2f} s; T_RETURN={T_RETURN:.3f} h, T_HIGH={T_HIGH:.3f} h, '
      f'low={sea_level(8 + (90 - H0) / RATE):.1f} m, high={_h_of_H(180):.1f} m')
