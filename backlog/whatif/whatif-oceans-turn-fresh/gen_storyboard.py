#!/usr/bin/env python3
"""Generate storyboard.json for whatif-oceans-turn-fresh from the script's caption list, HUD state table and
shot list (keep in sync with script.md). Output path is argv[1]."""
import json
import sys

OUT = sys.argv[1]

SERIF = '"Source Serif 4", "DejaVu Serif", Georgia, serif'
CYAN = '#7fe3ff'
RED = '#ff5a4f'
END_T = 71.0  # black starts; HUD and captions end here

# ------------------------------------------------------------------ captions (global seconds)
CAPTIONS = [
    (5.0, 7.8, "You're fishing in Bergen harbor, Norway."),
    (9.0, 13.6, 'The spray on your lips tastes like rain.'),
    (14.0, 19.0, 'The whole sea is drinkable now.'),
    (19.5, 23.6, 'But fish blood is saltier than this water.'),
    (24.0, 27.0, 'So the fish swell.'),
    (31.0, 34.2, 'Nearly every sea animal dies before dawn.'),
    (34.5, 37.7, "You're now saltier than the ocean."),
    (38.0, 41.0, '3.2 billion people rely on fish protein.'),
    (45.0, 50.6, 'Sinking salty water up north helps pull it.'),
    (51.0, 54.5, 'Icy fresh water floats.'),
    (62.5, 65.6, 'Sunrise. The sea looks normal.'),
    (66.0, 71.0, 'But that current kept your winters mild.'),
]

# ------------------------------------------------------------------ HUD state table (global seconds)
CLOCK = {'format': 'h:mm:ss', 'track': [{'t': 8, 'v': 21600, 'ease': 'linear'}, {'t': 62, 'v': 0, 'ease': 'linear'}]}
HUD = {
    'slots': {'C': {'y': 250, 'size': 30, 'color': CYAN}, 'L': {'y': 296, 'size': 30}, 'T': {'y': 340, 'size': 96, 'mono': True},
              'M': {'labelY': 456, 'labelSize': 28, 'valueY': 492, 'size': 54, 'unitSize': 28, 'mono': True}, 'S': {'y': 566, 'size': 28}, 'maxWidth': 860},
    'C': [
        {'from': 8, 'to': 20, 'text': 'THE WATER'},
        {'from': 20, 'to': 33, 'text': 'THE FISH'},
        {'from': 33, 'to': 43, 'text': 'THE PEOPLE'},
        {'from': 43, 'to': 62, 'text': 'THE CURRENT'},
        {'from': 66, 'to': END_T, 'text': 'FIRST WINTER'},
    ],
    'L': [
        {'from': 0, 'to': 8, 'text': 'SALT GONE IN'},
        {'from': 8, 'to': 62, 'text': 'BOATS LEAVE IN'},
        {'from': 62, 'to': 66, 'text': 'BOATS OUT'},
    ],
    'T': [
        {'from': 0, 'to': 8, 'text': '{v}', 'format': 'ss.mmm', 'prefix': '0:', 'track': [{'t': 0, 'v': 8.0, 'ease': 'linear'}, {'t': 8, 'v': 0.0, 'ease': 'linear'}]},
        dict({'from': 8, 'to': 62, 'text': '{v}'}, **CLOCK),
        {'from': 62, 'to': 66, 'text': '0:00:00'},
    ],
    'M': [
        {'from': 0, 'to': 8, 'label': 'OCEAN SALT', 'text': '{v}', 'unit': 'g/kg', 'decimals': 1, 'track': [{'t': 0, 'v': 35.0}]},
        {'from': 8, 'to': 43, 'label': 'OCEAN SALT', 'text': '{v}', 'unit': 'g/kg', 'decimals': 1,
         'track': [{'t': 8, 'v': 35.0, 'ease': 'linear'}, {'t': 9, 'v': 0.0, 'ease': 'linear'}],
         'colorTrack': [{'t': 8, 'v': CYAN}, {'t': 9, 'v': RED}]},
        {'from': 43, 'to': 47, 'label': 'SALT GONE', 'text': '~50', 'unit': 'QUADRILLION TONNES'},
        {'from': 47, 'to': 62, 'label': 'HEAT CARRIED NORTH', 'text': '60×', 'unit': 'HUMAN ENERGY USE'},
    ],
    'S': [
        {'from': 0, 'to': 8, 'text': 'GULF STREAM: OFFSHORE', 'opacity': 0.7},
        {'from': 8, 'to': 14.5, 'text': '1 HOUR = 9 SECONDS'},
        {'from': 14.5, 'to': 20, 'text': '2.2 BILLION LACK SAFE WATER'},
        {'from': 55, 'to': 62, 'text': 'NORTHERN SINKING: STOPPED', 'dot': RED},
        {'from': 62, 'to': 66, 'text': 'BERGEN, 6 HOURS LATER'},
        {'from': 67, 'to': END_T, 'text': 'SHUTDOWN MODEL: BERGEN ~15°C COLDER'},
    ],
    'inkDuring': [{'from': 41, 'to': 43, 'color': '#0b1a2e'}],
}

SHOTS = []


def shot(sid, start, end, background, layers=(), camera=None, transition=None, grade=None, sfx=(), notes=''):
    SHOTS.append(dict(id=sid, start=start, end=end, background=background, layers=list(layers), camera=camera,
                      transition=transition, grade=grade, sfx=list(sfx), notes=notes))


def comp(name, props=None, **kw):
    layer = {'type': 'component', 'name': name, 'props': props or {}}
    layer.update(kw)
    return layer


def harbor(time='night', **props):
    p = {'time': time}
    p.update(props)
    return {'type': 'component', 'name': 'whatif/BergenHarbor', 'props': p, 'depth': 0.15, 'overscan': 1.2}


def you(x, y, pose='stand', w=200, h=330, rod=True, reel=None, **kw):
    ls = [comp('explainer/You', {'pose': pose, 'color': '#3A8FD6'}, x=x, y=y, width=w, height=h, **kw)]
    if rod:
        ls.append(comp('whatif/RodLine', {'hand': 'right', 'lineTo': [x + 260, y + 260], 'reel': reel if reel is not None else 0},
                       x=x + 150, y=y - 40, width=360, height=520))
    return ls


def fresh_overlay(op_track=None):
    l = {'type': 'rect', 'x': '50%', 'y': 1460, 'width': 1080, 'height': 920, 'fill': '#bfeaff', 'opacity': 0.22, 'blend': 'screen', 'depth': 0.15, 'z': 20}
    if op_track:
        l['keyframes'] = op_track
    return l


def ribbon(width=120, opacity=0.8, **kw):
    return comp('whatif/CurrentRibbon', {'color': '#ff8a3d', 'width': width, 'opacity': opacity, 'dashSpeed': 1.0},
                x='50%', y=1380, width=1300, height=420, depth=0.15, z=15, **kw)


def card_bg(c='#10283a'):
    return {'type': 'color', 'color': c, 'depth': 0, 'overscan': 1.0}


def map_bg(views, **props):
    p = {'views': views, 'box': {'y': 420, 'height': 1000}, 'palette': {'land': '#2a3b4c', 'sea': '#0f2a40'}}
    p.update(props)
    return {'type': 'component', 'name': 'explainer/Map', 'props': p, 'depth': 0, 'overscan': 1.0}


GULF_PATH = {'points': [[-80.5, 24.5], [-79.5, 30], [-75.5, 35.2], [-60, 40.5], [-45, 45], [-25, 51], [-12, 55.5], [-3, 59], [5.32, 60.39]],
             'color': '#ff8a3d', 'width': 10, 'dash': [18, 10], 'drawAt': 0.6, 'drawDur': 2.4, 'label': 'GULF STREAM', 'labelAt': [-50, 41]}

TITLE_ICON = ('<svg viewBox="0 0 200 90" xmlns="http://www.w3.org/2000/svg"><path d="M5 55 Q30 25 55 55 T105 55 T155 55 T205 55" '
              'fill="none" stroke="#7fe3ff" stroke-width="9" stroke-linecap="round"/><g fill="#ffffff"><rect x="88" y="6" width="12" height="12" '
              'transform="rotate(20 94 12)"/><rect x="112" y="16" width="9" height="9" transform="rotate(-15 116 20)"/></g></svg>')


def title_layers(start, end, enter=True, exit_at=None):
    sh = '0 4px 18px rgba(0,0,0,.45)'
    ls = [
        {'type': 'svg', 'markup': TITLE_ICON, 'x': '50%', 'y': 640, 'width': 200, 'height': 90, 'depth': 0, 'z': 60},
        {'type': 'text', 'text': 'What if all the', 'x': '50%', 'y': 760, 'fontSize': 84, 'font': SERIF, 'weight': 600, 'color': '#FFFFFF', 'depth': 0, 'z': 60, 'shadow': sh},
        {'type': 'text', 'text': 'salt', 'x': '50%', 'y': 880, 'fontSize': 150, 'font': SERIF, 'weight': 700, 'color': CYAN, 'depth': 0, 'z': 60, 'shadow': sh},
        {'type': 'text', 'text': 'left the sea tonight?', 'x': '50%', 'y': 1000, 'fontSize': 84, 'font': SERIF, 'weight': 600, 'color': '#FFFFFF', 'maxWidth': 900, 'depth': 0, 'z': 60, 'shadow': sh},
    ]
    for l in ls:
        l['start'] = start
        l['end'] = end
        if enter:
            l['enter'] = {'type': 'fade', 'duration': 0.4}
        if exit_at is not None:
            l['exit'] = {'type': 'fade', 'at': exit_at, 'duration': end - exit_at}
    return ls


# 1 establishing (cover)
shot('s01-harbor-night', 0.0, 8.0, harbor('night', moon=True, ripples=True), [
    ribbon(),
    *you(240, 1240),
    *title_layers(0.0, 7.0, enter=False, exit_at=6.6),
], camera={'keyframes': [{'t': 0, 'x': '50%', 'y': '50%', 'zoom': 1.0}, {'t': 7.0, 'x': '50%', 'y': '50%', 'zoom': 1.05, 'ease': 'linear'},
                         {'t': 8.0, 'x': '50%', 'y': '54%', 'zoom': 1.08}]},
    sfx=[{'cue': 'clock_ticking', 'at': 0.0, 'volume': 0.35}],
    notes='Frame 1 = cover: bright moonlit Bryggen, moon reflection with ripples, orange current ribbon (plant), you with a rod. Title clears 6.6-7.0.')

# 2 flip
shot('s02-flip', 8.0, 9.0, harbor('night', moon=True, ripples=True), [
    ribbon(),
    *you(240, 1240),
    {'type': 'particles', 'preset': 'bubbles', 'count': 140, 'color': '#FFFFFF', 'size': [3, 7], 'speed': 3.0, 'seed': 11,
     'x': '50%', 'y': 1460, 'width': 1080, 'height': 900, 'end': 1.0, 'exit': {'type': 'fade', 'duration': 0.4}},
    fresh_overlay([{'t': 0, 'opacity': 0}, {'t': 1.0, 'opacity': 0.22}]),
    {'type': 'rect', 'x': '50%', 'y': '50%', 'width': 1080, 'height': 1920, 'fill': '#FFFFFF', 'depth': 0, 'z': 90,
     'opacity': 1, 'keyframes': [{'t': 0, 'opacity': 1}, {'t': 0.3, 'opacity': 0, 'ease': 'out'}]},
], camera={'keyframes': [], 'shake': [{'at': 0.0, 'duration': 0.35, 'amplitude': 12}]},
    sfx=[{'cue': 'impact', 'at': 0.0, 'volume': 0.9}, {'cue': 'whoosh', 'at': 0.0, 'volume': 0.5}],
    notes='9-frame white flash (8.0-8.3); salt glints burst off the water and wink out; HUD salt 35.0 -> 0.0 in 1 s; chapter THE WATER.')

# 3 body
shot('s03-spray', 9.0, 14.0, harbor('night', moon=True, ripples=True, crop='quay'), [
    ribbon(),
    fresh_overlay(),
    *you(420, 1150, w=300, h=495),
    {'type': 'particles', 'preset': 'rain', 'count': 20, 'color': '#dff4ff', 'size': [2, 4], 'speed': 0.6, 'seed': 4, 'x': 520, 'y': 900, 'width': 360, 'height': 260},
    comp('whatif/Glyph', {'kind': 'droplet', 'color': CYAN}, x=700, y=820, width=90, height=110, start=0.6, enter={'type': 'pop', 'duration': 0.3}),
    comp('whatif/Glyph', {'kind': 'raincloud', 'color': '#dff4ff'}, x=800, y=740, width=130, height=90, start=1.0, enter={'type': 'pop', 'duration': 0.3}),
], camera={'preset': 'pushIn', 'amount': 0.5}, sfx=[{'cue': 'bubbles', 'at': 0.2, 'volume': 0.2}],
    notes='Body first: spray on your lips tastes like rain. Glyphs only, no text.')

# 4 drinkable
shot('s04-cup', 14.0, 19.5, harbor('night', moon=True, ripples=True, crop='waterline'), [
    fresh_overlay(),
    {'type': 'svg', 'markup': '<svg viewBox="0 0 120 110" xmlns="http://www.w3.org/2000/svg"><path d="M10 10 H100 L92 100 H18 Z" fill="#c9d3dc" stroke="#5b6b73" stroke-width="5"/>'
     '<path d="M100 30 Q125 45 98 70" fill="none" stroke="#5b6b73" stroke-width="7"/><rect x="16" y="30" width="80" height="62" fill="#bfeaff" opacity=".8"/></svg>',
     'x': 560, 'y': 1180, 'width': 240, 'height': 220, 'z': 30,
     'keyframes': [{'t': 0, 'y': 980}, {'t': 1.4, 'y': 1300, 'ease': 'inOut'}, {'t': 3.0, 'y': 1020, 'ease': 'inOut'}, {'t': 5.5, 'y': 1000}]},
], camera={'keyframes': [{'t': 0, 'y': '50%', 'zoom': 1.0}, {'t': 5.5, 'y': '48%', 'zoom': 1.04}]},
    sfx=[{'cue': 'pop', 'at': 0.6, 'volume': 0.4}],
    notes='False resolution: a tin cup dips into the harbour and comes up clear; HUD 2.2 BILLION LACK SAFE WATER at 14.5.')

# 5 school
UNDER = {'type': 'component', 'name': 'explainer/Ocean', 'props': {'depth': 10, 'rays': 6, 'snow': 20, 'topColor': '#1b6f8f', 'bottomColor': '#0b3550'}, 'depth': 0.2, 'overscan': 1.2}
shot('s05-school', 19.5, 27.0, UNDER, [
    comp('whatif/Kelp', {'count': 7, 'seed': 2}, x='50%', y=1500, width=1200, height=700, depth=0.4),
    comp('whatif/FishSchool', {'species': ['herring'] * 24 + ['cod'] * 3, 'seed': 5, 'swell': [{'t': 0, 'v': 0}, {'t': 4.5, 'v': 0}, {'t': 7.5, 'v': 1}]},
         x='50%', y=900, width=1000, height=700, keyframes=[{'t': 0, 'x': 480}, {'t': 7.5, 'x': 600, 'ease': 'linear'}]),
], camera={'keyframes': [{'t': 0, 'x': '48%'}, {'t': 7.5, 'x': '52%', 'ease': 'linear'}]},
    sfx=[{'cue': 'sonar_ping', 'at': 0.5, 'volume': 0.4}],
    notes='Rule caption 4 at 19.5 (chapter THE FISH at 20.0); caption 5 at 24.0; fish start to swell at 24.0.')

# 6 textless break
shot('s06-sink', 27.0, 31.0, UNDER, [
    comp('whatif/Kelp', {'count': 7, 'seed': 2}, x='50%', y=1500, width=1200, height=700, depth=0.4),
    comp('whatif/FishSchool', {'species': ['herring'] * 24 + ['cod'] * 3, 'seed': 5, 'swell': 1, 'scatter': [{'t': 0, 'v': 0}, {'t': 4, 'v': 1}],
                                'sink': [{'t': 0, 'v': 0}, {'t': 4, 'v': 260, 'ease': 'in'}], 'tilt': 70}, x=600, y=900, width=1000, height=700),
], camera={'preset': 'pullOut', 'amount': 0.4}, sfx=[{'cue': 'drone', 'at': 0.0, 'volume': 0.35}],
    notes='Textless: the school breaks apart and sinks past the kelp.')

# 7 water column
shot('s07-column', 31.0, 34.5, UNDER, [
    comp('whatif/SeaColumn', {'surfaceBand': True, 'freshOverlay': 0.22, 'settling': [{'t': 0, 'v': 0.3}, {'t': 3.5, 'v': 1}],
                              'glyphs': ['fish', 'fish', 'crab', 'jelly', 'starfish', 'fish']}, x='50%', y='50%', width=1080, height=1920),
], camera={'keyframes': [{'t': 0, 'zoom': 1.15}, {'t': 3.5, 'zoom': 0.9}]}, sfx=[{'cue': 'whoosh_long', 'at': 0.2, 'volume': 0.3}],
    notes='Nearly every sea animal dies before dawn: whole-column cross-section, everything settling. Chapter THE PEOPLE at 33.0.')

# 8 dip
shot('s08-dip', 34.5, 38.0, harbor('night', moon=True, ripples=True, crop='quay'), [
    fresh_overlay(),
    *you(380, 1150, pose='shrug', w=300, h=495, rod=False),
    comp('whatif/SaltBars', {'you': 9, 'sea': 0, 'max': 12, 'growAt': 0.2}, x=760, y=1000, width=300, height=420),
], camera={'preset': 'pushIn', 'amount': 0.4},
    sfx=[{'cue': 'tick', 'at': 0.1, 'volume': 0.5}, {'cue': 'tick', 'at': 0.7, 'volume': 0.5}],
    notes='Return-to-you dip at 43%: two icon bars, you (tall) vs the sea (empty). No text.')

# 9 people
shot('s09-people', 38.0, 41.0, card_bg(), [
    comp('whatif/PeopleGrid', {'count': 32, 'cols': 8, 'stagger': 0.06, 'fishGlyph': True, 'greyFishAt': 2.0}, x='50%', y=900, width=900, height=700),
], camera={'preset': 'pullOut', 'amount': 0.3},
    sfx=[{'cue': 'pop', 'at': 0.1, 'volume': 0.3}, {'cue': 'pop', 'at': 0.4, 'volume': 0.3}, {'cue': 'pop', 'at': 0.7, 'volume': 0.3}, {'cue': 'pop', 'at': 1.0, 'volume': 0.3},
         {'cue': 'riser', 'at': 1.5, 'volume': 0.4}],
    notes='3.2 billion: 32 figures (1 = 100 million) with fish glyphs that grey out from 40.0.')

# 10 white-out
shot('s10-whiteout', 41.0, 43.0, card_bg('#10283a'), [
    {'type': 'particles', 'preset': 'bubbles', 'count': 300, 'color': '#FFFFFF', 'size': [6, 18], 'speed': 4.0, 'seed': 21, 'x': '50%', 'y': '50%', 'width': 1080, 'height': 1920},
    {'type': 'rect', 'x': '50%', 'y': '50%', 'width': 1080, 'height': 1920, 'fill': '#FFFFFF', 'depth': 0, 'z': 70,
     'opacity': 0, 'keyframes': [{'t': 0, 'opacity': 0}, {'t': 0.8, 'opacity': 1, 'ease': 'in'}, {'t': 2.0, 'opacity': 1}]},
], sfx=[{'cue': 'boom', 'at': 0.8, 'volume': 0.7}],
    notes='White salt crystals fill the frame, then pure white. No new text; HUD drawn in ink colour.')

# 11 map pull-out
shot('s11-map-path', 43.0, 47.0, map_bg([{'t': 0, 'place': 'bergen', 'zoom': 8}, {'t': 2.5, 'lon': -35, 'lat': 45, 'zoom': 3.2}],
                                         pins=[{'place': 'bergen', 'label': 'YOU', 'color': CYAN}], paths=[GULF_PATH]), [
    {'type': 'rect', 'x': '50%', 'y': '50%', 'width': 1080, 'height': 1920, 'fill': '#FFFFFF', 'depth': 0, 'z': 70,
     'opacity': 1, 'keyframes': [{'t': 0, 'opacity': 1}, {'t': 0.3, 'opacity': 0}]},
], sfx=[{'cue': 'whoosh', 'at': 0.0, 'volume': 0.5}],
    notes='Scale jump: Bergen pin -> North Atlantic; Gulf Stream path draws Florida Straits -> Bergen (plant named). Chapter THE CURRENT; meter SALT GONE.')

# 12 north atlantic
RINGS = [{'place': 'labradorSea', 'r': 60, 'color': '#6fc3ff'}, {'place': 'nordicSeas', 'r': 60, 'color': '#6fc3ff'}]
shot('s12-map-sinking', 47.0, 55.0, map_bg([{'t': 0, 'lon': -35, 'lat': 45, 'zoom': 3.2}, {'t': 8, 'lon': -25, 'lat': 58, 'zoom': 3.4}],
                                            pins=[{'place': 'bergen', 'label': 'YOU', 'color': CYAN}], paths=[dict(GULF_PATH, drawAt=-10)],
                                            rings=RINGS, ringsGreyAt=4.0), [],
    sfx=[{'cue': 'underwater_rumble', 'at': 0.0, 'volume': 0.25}],
    notes='Captions 9 (45.0, in previous shot) and 10 (51.0). Sinking rings pulse, then stop and grey at 51.0. HEAT CARRIED NORTH held.')

# 13 textless status
shot('s13-map-stopped', 55.0, 59.0, map_bg([{'t': 0, 'lon': -25, 'lat': 58, 'zoom': 3.4}],
                                            pins=[{'place': 'bergen', 'label': 'YOU', 'color': CYAN}],
                                            paths=[dict(GULF_PATH, drawAt=-10, widthTrack={'northOfLat': 55, 'track': [{'t': 0, 'v': 10}, {'t': 4, 'v': 4}]})],
                                            rings=[dict(RINGS[0], out=0.4), dict(RINGS[1], out=1.6)], ringsGrey=True), [],
    sfx=[{'cue': 'drone', 'at': 0.0, 'volume': 0.3}],
    notes='NORTHERN SINKING: STOPPED. Rings fade; the path keeps flowing but thins north of 55N only (wind-driven part continues).')

# 14 dive back
shot('s14-map-dive', 59.0, 62.0, map_bg([{'t': 0, 'lon': -25, 'lat': 58, 'zoom': 3.4}, {'t': 3, 'place': 'bergen', 'zoom': 9, 'ease': 'in'}],
                                         pins=[{'place': 'bergen', 'label': 'YOU', 'color': CYAN}],
                                         paths=[dict(GULF_PATH, drawAt=-10, width=6)], dawnSweep={'at': 0.5, 'dur': 2.5}), [],
    sfx=[{'cue': 'riser', 'at': 0.5, 'volume': 0.35}, {'cue': 'clock_ticking', 'at': 1.0, 'volume': 0.3}],
    notes='Dive back into the Bergen pin as a dawn glow sweeps from the east; master clock runs out.')

# 15 dawn bookend
shot('s15-harbor-dawn', 62.0, 66.0, harbor('dawn', boatsOut=[{'t': 0.3, 'v': 0}, {'t': 4, 'v': 1}]), [
    ribbon(),
    fresh_overlay([{'t': 0, 'opacity': 0.22}, {'t': 1.0, 'opacity': 0}]),
    *you(240, 1240, reel=[{'t': 1.0, 'v': 0}, {'t': 3.0, 'v': 1, 'ease': 'inOut'}]),
], camera={'keyframes': [{'t': 0, 'x': '50%', 'y': '50%', 'zoom': 1.0}]},
    sfx=[{'cue': 'ding', 'at': 0.0, 'volume': 0.4}, {'cue': 'breath', 'at': 0.2, 'volume': 0.15}, {'cue': 'click', 'at': 2.8, 'volume': 0.4}],
    notes='Bookend of shot 1 at dawn: the sea looks normal, boats head out, you reel in an empty hook (bathos, no text). BOATS OUT / BERGEN, 6 HOURS LATER.')

# 16 winter twist
shot('s16-harbor-winter', 66.0, 71.0, harbor('winter', snowOnRoofs=True), [
    ribbon(width=40, opacity=0.35),
    *you(240, 1240),
    {'type': 'particles', 'preset': 'snow', 'count': 80, 'color': '#FFFFFF', 'size': [3, 8], 'speed': 0.8, 'seed': 9, 'x': '50%', 'y': '50%', 'width': 1080, 'height': 1920},
], camera={'preset': 'pushIn', 'amount': 0.3},
    sfx=[{'cue': 'stinger', 'at': 0.0, 'volume': 0.5}, {'cue': 'whoosh_long', 'at': 0.3, 'volume': 0.3}],
    notes='Twist on the viewer: same quay in snow, FIRST WINTER; current ribbon thin and pale. One HUD line at 67.0.')

# 17 black
shot('s17-black', 71.0, 73.0, {'type': 'color', 'color': '#000000', 'depth': 0, 'overscan': 1.0}, [], notes='Black, silence, HUD hidden.')

# 18 end card
END_FACT = '12,900 YEARS AGO, MELTWATER LIKELY STALLED THIS CURRENT.\nEUROPE TURNED ICE-AGE COLD FOR 1,200 YEARS.'
shot('s18-endcard', 73.0, 80.0, {'type': 'color', 'color': '#05080c', 'depth': 0, 'overscan': 1.0}, [
    *title_layers(0.0, 7.0, enter=True),
    {'type': 'text', 'text': END_FACT, 'x': '50%', 'y': 1180, 'fontSize': 34, 'font': 'display', 'weight': 700, 'color': '#D9DEE3',
     'letterSpacing': 0.08, 'lineHeight': 1.4, 'maxWidth': 860, 'start': 1.0, 'enter': {'type': 'fade', 'duration': 0.6}, 'depth': 0, 'z': 60},
], sfx=[{'cue': 'ding', 'at': 0.0, 'volume': 0.2}], notes='Exact title repeat + Younger Dryas fact (not read).')

# ------------------------------------------------------------------ assemble
scenes = []
for sh in SHOTS:
    start, end = sh['start'], sh['end']
    layers = list(sh['layers'])
    if start < END_T:
        layers.append(comp('whatif/Hud', {'t0': start, 'state': HUD, 'mono': 'JetBrains Mono', 'accent': CYAN, 'warn': RED},
                           id='hud', x=70, y=240, anchorX=0, anchorY=0, width=860, height=340, depth=0, z=80))
    for cs, ce, text in CAPTIONS:
        if ce <= start or cs >= end:
            continue
        ls, le = max(cs, start) - start, min(ce, end) - start
        cap = {'type': 'text', 'text': text, 'x': '50%', 'y': 1330, 'fontSize': 62, 'font': SERIF, 'weight': 600,
               'color': '#FFFFFF', 'maxWidth': 860, 'lineHeight': 1.15, 'shadow': '0 3px 14px rgba(0,0,0,.6)',
               'start': round(ls, 3), 'end': round(le, 3), 'depth': 0, 'z': 75}
        if cs >= start:
            cap['enter'] = {'type': 'fade', 'duration': 0.25}
        if ce <= end and ce < END_T:
            cap['exit'] = {'type': 'fade', 'duration': 0.25}
        layers.append(cap)
    scene = {'id': sh['id'], 'duration': round(end - start, 3), 'background': sh['background'], 'layers': layers,
             'notes': sh['notes'] + f' [screen {start:.1f}-{end:.1f} s]'}
    for k_src, k_dst in (('camera', 'camera'), ('transition', 'transitionIn'), ('grade', 'grade'), ('sfx', 'sfx')):
        if sh[k_src]:
            scene[k_dst] = sh[k_src]
    scenes.append(scene)

storyboard = {
    'version': 1,
    'id': 'whatif-oceans-turn-fresh',
    'title': 'What if all the salt left the sea tonight?',
    'format': '9:16',
    'fps': 30,
    'theme': {'fontDisplay': 'Montserrat', 'fontBody': 'Montserrat', 'fontCondensed': 'Anton', 'accent': CYAN, 'ink': '#0B0D10', 'paper': '#FFFFFF'},
    'scenes': scenes,
    'captions': {'enabled': False},
    'audio': {
        'voice': [],
        'music': [
            {'src': 'music/deep_ocean.m4a', 'start': 0.0, 'end': 41.0, 'volume': 0.25, 'duckTo': 0.12, 'fadeIn': 0.5, 'fadeOut': 0.3},
            {'src': 'music/documentary_pulse.m4a', 'start': 43.0, 'end': 71.0, 'volume': 0.25, 'duckTo': 0.12, 'fadeIn': 0.3, 'fadeOut': 0.4},
            {'src': 'sfx/underwater_rumble.wav', 'start': 19.5, 'end': 34.5, 'volume': 0.3, 'duckTo': 0.3, 'fadeIn': 0.4, 'fadeOut': 0.4, 'loop': True},
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
