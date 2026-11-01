#!/usr/bin/env python3
"""Generate storyboard.json for explainer-short-blue-whale-scale from the measured Kokoro word timings
(audio/captions.json, speed 1.05) and the shot list in script.md. Keep in sync with script.md.

usage: python3 backlog/explainer/explainer-short-blue-whale-scale/gen_storyboard.py [out.json]
Every time below is anchored to a spoken word (W('word', nth)), so a re-voice only needs a new captions.json.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'storyboard.json')
SLUG = 'explainer-short-blue-whale-scale'
WORDS = json.load(open(os.path.join(HERE, 'audio', 'captions.json')))['words']
W_, H_ = 1080, 1920
RED, GREEN, CYAN, WHITE, ORANGE = '#e5483d', '#3ddc84', '#7fe3ff', '#ffffff', '#f08a24'
LEAD = 0.15
TOTAL = 61.5          # speech ends 60.93; 0.57 s loop hold
LOOP_AT = 60.95


def norm(w):
    return re.sub(r"[^a-z0-9']", '', w.lower())


def W(token, nth=0, end=False, after=None):
    """Global time of the nth spoken word matching token (optionally the first one starting at/after `after`)."""
    hits = [w for w in WORDS if norm(w['text']) == norm(token)]
    if after is not None:
        hits = [w for w in hits if w['start'] >= after - 1e-6]
        nth = 0
    w = hits[nth]
    return round(w['end'] if end else w['start'], 3)


# ------------------------------------------------------------------ layer helpers
def comp(name, x, y, w, h, props, **kw):
    d = {'type': 'component', 'name': name, 'x': x, 'y': y, 'width': w, 'height': h, 'props': props}
    d.update(kw)
    return d


def svg(markup, x, y, w, h, **kw):
    d = {'type': 'svg', 'markup': markup, 'x': x, 'y': y, 'width': w, 'height': h}
    d.update(kw)
    return d


def headline(text, at=0.0, y='22%', size=110, color='white', out=None, **p):
    props = {'text': text, 'at': at, 'size': size, 'color': color, 'underline': True, **p}
    if out is not None:
        props['out'] = out
    return comp('explainer/Headline', '50%', y, 1000, size * 3.0, props, depth=0, z=30)


def tag(text, at, x='50%', y='60%', size=40, accent=None, w=900, out=None, **p):
    props = {'text': text, 'at': at, 'size': size, 'align': 'center', **p}
    if accent:
        props['accent'] = accent
    if out is not None:
        props['out'] = out
    return comp('explainer/Tag', x, y, w, size * 2.4, props, depth=0, z=25)


def stat(value, at, x='50%', y='30%', size=120, **p):
    return comp('explainer/Stat', x, y, 900, size * 2.4, {'value': value, 'at': at, 'size': size, **p}, depth=0, z=25)


def you(x, y, px, pose='stand', **kw):
    h = 1.75 * px
    return comp('explainer/You', x, y, h * 0.62, h, {'pose': pose, 'pxPerM': px}, **kw)


def ocean(depth, **p):
    return {'type': 'component', 'name': 'explainer/Ocean', 'depth': 0.12, 'overscan': 1.2, 'props': {'depth': depth, **p}}


def kf(t, **v):
    return {'t': round(max(0.0, t), 3), **v}


# ------------------------------------------------------------------ scoreboard (one source of truth)
SCORE_EVENTS = [(0.0, '0 : 0'), (W('point', 0), '1 : 0'), (W('point', 1), '2 : 0'), (W('point', 2), '3 : 0'),
                (W('point', 3), '4 : 0'), (W('point', 4), '4 : 1')]


def score_layers(s0, s1):
    """Scoreboard Tag layers for the scene [s0, s1) (global seconds), one layer per state."""
    out = []
    for i, (t, txt) in enumerate(SCORE_EVENTS):
        t_end = SCORE_EVENTS[i + 1][0] if i + 1 < len(SCORE_EVENTS) else 1e9
        if t_end <= s0 or t >= s1:
            continue
        start = max(0.0, t - s0)
        fresh = t >= s0 and t > 0          # an update inside this scene pops in; otherwise fully in at frame 0
        accent = GREEN if txt == '4 : 1' else RED
        layer = tag(f'WHALE {txt} YOU', at=start if fresh else -0.6, y=270, size=44, accent=accent, w=640,
                    bg='#0b1a22', color=WHITE)
        layer['start'] = round(start, 3)
        if t_end < s1:
            layer['end'] = round(t_end - s0, 3)
        out.append(layer)
    return out


# ------------------------------------------------------------------ inline art
def court_svg():
    # 28.65 m x 15.24 m NBA court, foreshortened (viewed at a low angle): 1031 px wide at 36 px/m
    return ('<svg viewBox="0 0 1031 140" xmlns="http://www.w3.org/2000/svg">'
            '<polygon points="60,0 971,0 1031,140 0,140" fill="#c98a4b" stroke="#ffffff" stroke-width="5"/>'
            '<line x1="515" y1="0" x2="515" y2="140" stroke="#ffffff" stroke-width="5"/>'
            '<ellipse cx="515" cy="70" rx="64" ry="26" fill="none" stroke="#ffffff" stroke-width="5"/>'
            '<path d="M 40 30 Q 230 70 30 112" fill="none" stroke="#ffffff" stroke-width="5"/>'
            '<path d="M 991 30 Q 801 70 1001 112" fill="none" stroke="#ffffff" stroke-width="5"/></svg>')


def flipper_svg():
    # 3 m pectoral flipper, root on the left, 900 x 260 px at 300 px/m
    return ('<svg viewBox="0 0 900 260" xmlns="http://www.w3.org/2000/svg">'
            '<path d="M 0 70 C 220 20 520 30 760 90 C 860 115 900 140 890 160 C 860 185 700 190 520 185 '
            'C 320 182 140 200 0 200 Z" fill="#4f6f86"/>'
            '<path d="M 0 200 C 140 200 320 182 520 185 C 700 190 860 185 890 160" fill="none" stroke="#e8f1f5" stroke-width="10"/></svg>')


def bones_svg():
    # x-ray arm bones inside the flipper: humerus, radius + ulna, wrist, five finger rays
    g = ['<svg viewBox="0 0 900 260" xmlns="http://www.w3.org/2000/svg"><g fill="#dff6ff" opacity="0.92">',
         '<rect x="30" y="105" width="190" height="34" rx="17"/>',
         '<rect x="225" y="92" width="170" height="20" rx="10"/><rect x="225" y="128" width="170" height="20" rx="10"/>',
         '<circle cx="420" cy="118" r="20"/><circle cx="445" cy="140" r="16"/>']
    for i, (y, ln) in enumerate([(88, 300), (108, 360), (128, 380), (148, 330), (168, 240)]):
        x = 470
        for k in range(4):
            seg = ln / 4 - 8
            g.append(f'<rect x="{x:.0f}" y="{y}" width="{seg:.0f}" height="12" rx="6"/>')
            x += seg + 8
    g.append('</g></svg>')
    return ''.join(g)


def back_svg():
    # whale back at the waterline, blowhole at x 540 of a 1600 px wide arc
    return ('<svg viewBox="0 0 1600 220" xmlns="http://www.w3.org/2000/svg">'
            '<path d="M 0 220 C 300 40 1100 0 1600 160 L 1600 220 Z" fill="#3e5a70"/>'
            '<ellipse cx="540" cy="58" rx="34" ry="10" fill="#132430"/></svg>')


def spout_svg():
    return ('<svg viewBox="0 0 300 1080" xmlns="http://www.w3.org/2000/svg"><defs>'
            '<linearGradient id="sp" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#ffffff" stop-opacity="0.95"/>'
            '<stop offset="1" stop-color="#ffffff" stop-opacity="0.15"/></linearGradient></defs>'
            '<path d="M 135 1080 C 120 700 40 300 20 60 C 80 0 220 0 280 60 C 260 300 180 700 165 1080 Z" fill="url(#sp)"/></svg>')


def icon_row(n, cell_w, cell_h, color=WHITE):
    """One row of n stick icons (the reusable CountGrid, drawn as svg rows)."""
    parts = [f'<svg viewBox="0 0 {n * cell_w} {cell_h}" xmlns="http://www.w3.org/2000/svg"><g stroke="{color}" '
             f'stroke-width="{max(2, cell_w // 10)}" stroke-linecap="round" fill="none">']
    for i in range(n):
        cx = i * cell_w + cell_w / 2
        r = cell_w * 0.18
        parts.append(f'<circle cx="{cx:.1f}" cy="{r + 2:.1f}" r="{r:.1f}" fill="{color}"/>'
                     f'<path d="M {cx:.1f} {2 * r + 4:.1f} L {cx:.1f} {cell_h * 0.68:.1f} '
                     f'M {cx - cell_w * 0.3:.1f} {cell_h * 0.42:.1f} L {cx + cell_w * 0.3:.1f} {cell_h * 0.42:.1f} '
                     f'M {cx:.1f} {cell_h * 0.68:.1f} L {cx - cell_w * 0.22:.1f} {cell_h - 3:.1f} '
                     f'M {cx:.1f} {cell_h * 0.68:.1f} L {cx + cell_w * 0.22:.1f} {cell_h - 3:.1f}"/>')
    parts.append('</g></svg>')
    return ''.join(parts)


def count_grid(n, cols, cell_w, cell_h, x0, y0, t0, t1, z=12, end=None):
    """CountGrid: n icons, `cols` per row, rows revealed between scene-local t0 and t1 (pop)."""
    rows = (n + cols - 1) // cols
    out = []
    for r in range(rows):
        k = min(cols, n - r * cols)
        at = t0 + (t1 - t0) * (r / max(1, rows - 1))
        lay = svg(icon_row(k, cell_w, cell_h), x0 + k * cell_w / 2, y0 + r * cell_h + cell_h / 2, k * cell_w, cell_h,
                  depth=0, z=z, start=round(at, 3), enter={'type': 'pop', 'duration': 0.18})
        if end is not None:
            lay['end'] = round(end, 3)
            lay['exit'] = {'type': 'fade', 'duration': 0.25}
        out.append(lay)
    return out


def tunnel_svg():
    return ('<svg viewBox="0 0 800 800" xmlns="http://www.w3.org/2000/svg"><defs>'
            '<radialGradient id="tn"><stop offset="0" stop-color="#050000"/><stop offset="0.55" stop-color="#3a0609"/>'
            '<stop offset="1" stop-color="#8f1d24" stop-opacity="0"/></radialGradient></defs>'
            '<ellipse cx="400" cy="400" rx="380" ry="330" fill="url(#tn)"/></svg>')


def basketball_svg():
    return ('<svg viewBox="0 0 480 480" xmlns="http://www.w3.org/2000/svg">'
            '<circle cx="240" cy="240" r="234" fill="#e0782a" stroke="#2b1306" stroke-width="10"/>'
            '<g fill="none" stroke="#2b1306" stroke-width="9"><line x1="6" y1="240" x2="474" y2="240"/>'
            '<line x1="240" y1="6" x2="240" y2="474"/><path d="M 70 70 C 170 170 170 310 70 410"/>'
            '<path d="M 410 70 C 310 170 310 310 410 410"/></g></svg>')


def bust_svg():
    # face-on head and shoulders at 2000 px/m: head 16 cm wide (320 px), shoulders 45 cm (900 px). Box 960 x 900.
    return ('<svg viewBox="0 0 960 900" xmlns="http://www.w3.org/2000/svg">'
            '<rect x="420" y="380" width="120" height="120" fill="#8fa3ae"/>'
            '<path d="M 30 900 C 30 600 120 500 480 490 C 840 500 930 600 930 900 Z" fill="#8fa3ae" stroke="#ffffff" stroke-width="6"/>'
            '<ellipse cx="480" cy="210" rx="160" ry="200" fill="#8fa3ae" stroke="#ffffff" stroke-width="6"/>'
            '<circle cx="425" cy="200" r="16" fill="#0b1a22"/><circle cx="535" cy="200" r="16" fill="#0b1a22"/>'
            '<path d="M 430 300 Q 480 330 530 300" stroke="#0b1a22" stroke-width="10" fill="none"/></svg>')


def round_icons_svg():
    # flipper, spout, calf, krill pile, aorta ring (green: the win)
    return ('<svg viewBox="0 0 1000 200" xmlns="http://www.w3.org/2000/svg"><g stroke-width="10" fill="none">'
            '<path d="M 20 110 C 80 70 150 80 180 110 C 140 130 70 135 20 130 Z" fill="#4f6f86" stroke="#ffffff"/>'
            '<path d="M 300 180 C 295 120 260 60 250 20 C 280 0 320 0 350 20 C 340 60 305 120 300 180" fill="#ffffff" stroke="#ffffff"/>'
            '<path d="M 420 120 C 470 80 560 80 590 110 L 600 95 L 600 135 L 590 120 C 560 150 470 150 420 120 Z" fill="#7d9bb0" stroke="#ffffff"/>'
            '<path d="M 650 170 Q 730 40 810 170 Z" fill="#ff8fa3" stroke="#ffffff"/>'
            '<circle cx="910" cy="110" r="62" stroke="#3ddc84" stroke-width="18"/></g></svg>')


# ------------------------------------------------------------------ scenes (global start, end)
def cut(word, after):
    return round(W(word, after=after) - LEAD, 3)


B = [0.0, cut('it', 3.0), round(W('bigger') + 0.92, 3), cut('and', 16.0), cut('so', 24.5), cut('newborn', 27.0),
     cut('round', 35.0), cut('and', 45.0), cut('you', 49.0), round(W('you', end=True, after=56.0) + 0.04, 3), LOOP_AT, TOTAL]
# B[2] = ROUND 1 card time (7.95), just before 'Round one' (8.27)
assert all(b < c for b, c in zip(B, B[1:])), B
names = ['hook', 'anchor', 'r1_flipper', 'r2_spout', 'r3_baby', 'r3_newborn', 'r4_lunch', 'r5_myth', 'r5_ring',
         'stinger', 'loop']


def L(t, s0):
    return round(t - s0, 3)


def hook_layers(s0=0.0, frozen=False):
    """Frame-0 composition (also reused verbatim as the loop shot)."""
    return [
        comp('explainer/BlueWhale', '50%', '36%', 1080, 320, {'pxPerM': 36, 'amp': 0.5, 'idle': not frozen}, z=2,
             idle=[{'type': 'bob', 'amount': 5, 'speed': 0.2}]),
        you('90%', '41%', 36, pose='shrug', z=3),
        svg('<svg viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg"><line x1="290" y1="10" x2="20" y2="290" '
            'stroke="#ffffff" stroke-width="4" stroke-dasharray="12 10"/></svg>', '82%', '49%', 150, 150, z=4, depth=0),
        {'type': 'circle', 'x': '70%', 'y': '58%', 'width': 360, 'height': 360, 'fill': 'rgba(8,30,40,0.85)',
         'stroke': WHITE, 'strokeWidth': 6, 'z': 5, 'depth': 0},
        you('70%', '58.5%', 171, pose='point', z=6, depth=0, flipX=True),
    ]


def scenes():
    S = []

    def add(i, bg, layers, camera=None, trans=None, sfx=None, notes='', **kw):
        s0, s1 = B[i], B[i + 1]
        sc = {'id': f'{i:02d}_{names[i]}', 'duration': round(s1 - s0, 3), 'background': bg,
              'layers': layers + (score_layers(s0, s1) if names[i] not in ('stinger',) else []),
              'notes': notes}
        if camera:
            sc['camera'] = camera
        if trans:
            sc['transitionIn'] = trans
        if sfx:
            sc['sfx'] = [{'cue': c, 'at': round(max(0.0, t - s0), 3), 'volume': v} for c, t, v in sfx]
        sc.update(kw)
        S.append(sc)

    # 00 hook (cover)
    add(0, ocean(25, rays=8, snow=60), hook_layers(), camera={'preset': 'pushIn', 'amount': 0.4},
        sfx=[('underwater_rumble', 0.0, 0.5), ('ding', W('five'), 0.6)],
        notes='Frame 0 = cover: whole whale in colour, true-scale YOU at its eye + 300 px magnifier inset. 2 text elements (score + caption).')

    # 01 anchor + rule
    s0 = B[1]
    add(1, ocean(25, rays=8, snow=60), [
        comp('explainer/BlueWhale', '50%', '36%', 1080, 320, {'pxPerM': 36, 'amp': 0.5}, z=2),
        svg(court_svg(), '50%', '46%', 1031, 140, z=1),
        comp('explainer/ScaleBar', '50%', '28%', 1008, 120, {'label': '~28 M', 'at': L(W('basketball'), s0), 'from': 'left'}, z=10, depth=0),
        headline('BIGGER WINS', at=L(W('bigger'), s0), y='62%', size=100, underline=False),
    ], camera={'preset': 'drift', 'amount': 0.6},
        sfx=[('whoosh', W('it'), 0.5), ('impact', W('bigger'), 0.7)],
        notes='Whale (kit 28 m) at the same pxPerM as a 28.65 m court: "as long as" matches the picture.')

    # 02 round 1 flipper (pxPerM 300)
    s0 = B[2]
    t_tip, t_arm, t_small, t_pt = L(W('tip'), s0), L(W('basically'), s0), L(W('too'), s0), L(W('point', 0), s0)
    add(2, ocean(40, rays=6, snow=50), [
        headline('ROUND 1', at=0.0, out=1.1),
        svg(flipper_svg(), '50%', '42%', 900, 260, z=3, start=0.9, enter={'type': 'slideLeft', 'duration': 0.4}),
        you('31%', '55%', 300, pose='stand', z=4, rotate=-90, start=L(W('lie'), s0), enter={'type': 'pop', 'duration': 0.3}),
        svg('<svg viewBox="0 0 20 400" xmlns="http://www.w3.org/2000/svg"><line x1="10" y1="0" x2="10" y2="400" stroke="#ffffff" '
            'stroke-width="6" stroke-dasharray="18 12"/></svg>', '91%', '48%', 20, 400, z=5, depth=0, start=t_tip),
        comp('explainer/ScaleBar', '50%', '33%', 900, 110, {'label': '~3 M', 'at': t_tip, 'from': 'left'}, z=10, depth=0),
        svg(bones_svg(), '50%', '42%', 900, 260, z=6, start=t_arm, enter={'type': 'fade', 'duration': 0.35}),
        tag('ARM BONES', t_arm, y='60%', accent=CYAN, w=520),
        tag('TOO SMALL', t_small, y='66%', size=48, accent=RED, w=560),
    ], camera={'keyframes': [kf(0, zoom=1.1), kf(0.5, zoom=1.0, ease='out'), kf(B[3] - s0, zoom=1.05)]},
        sfx=[('ding', B[2], 0.7), ('pop', W('tip'), 0.6), ('pop', W('basically'), 0.6), ('click', W('too'), 0.7), ('ding', W('point', 0), 0.6)],
        notes='Flipper 3 m and YOU 1.75 m share pxPerM 300 (900 px vs 525 px). Bones = x-ray overlay on "basically its arm".')

    # 03 round 2 spout (pxPerM 120, waterline y 1306)
    s0 = B[3]
    t_stand, t_shoot, t_five, t_snot = L(W('stand'), s0), L(W('shoots'), s0), L(W('five', 1), s0), L(W('snot'), s0)
    stack = [you('24%', round(1306 - 96.25 - 192.5 * k, 1), 110, pose='stand' if k else 'wave', z=6,
                 start=t_stand if k == 0 else round(t_five + 0.12 * (k - 1), 3), enter={'type': 'pop', 'duration': 0.2})
             for k in range(5)]
    add(3, ocean(5, surface=0.68, rays=7, snow=30, skyTop='#071620', skyBottom='#1b3b4a'), [
        headline('ROUND 2', at=0.0, out=1.1),
        svg(back_svg(), '60%', 1306 - 60, 1600, 220, z=3),
        {**svg(spout_svg(), '50%', 1266, 280, 990, z=4, anchorY=1.0, start=t_shoot),
         'keyframes': [kf(t_shoot, scaleY=0.05, opacity=0.6), kf(t_shoot + 0.7, scaleY=1.0, opacity=1, ease='out')]},
        *stack,
        stat(9, t_five, x='72%', y='30%', size=120, suffix=' M', duration=0.6),
        {'type': 'particles', 'preset': 'rain', 'count': 120, 'color': '#c9f2b0', 'size': [3, 7], 'speed': 0.6, 'seed': 3,
         'x': '55%', 'y': '35%', 'width': 700, 'height': 700, 'z': 7, 'depth': 0, 'start': t_snot},
        tag('PARTLY SNOT', t_snot, x='70%', y='42%', accent='#9be36b', w=560),
    ], camera={'keyframes': [kf(0, zoom=1.0, y='55%'), kf(t_shoot, zoom=1.0, y='55%'), kf(t_five + 0.6, zoom=1.0, y='45%', ease='inOut'),
                             kf(B[4] - s0, zoom=1.03, y='45%')]},
        sfx=[('ding', B[3], 0.7), ('whoosh_long', W('shoots'), 0.6)] + [('tick', W('five', 1) + 0.12 * k, 0.5) for k in range(4)]
            + [('bubbles', W('snot'), 0.5), ('ding', W('point', 1), 0.6)],
        captionY=0.76,
        notes='Spout 9 m = 990 px, YOU 1.75 m = 192.5 px, 5 stacked = 962 px (shared pxPerM 110). Raw "9 M" shown, not said.')

    # 04 round 3 turnstile line
    s0 = B[4]
    add(4, ocean(20, rays=8, snow=40), [
        headline('ROUND 3', at=0.0, out=1.1),
        comp('explainer/BlueWhale', '50%', '45%', 520, 160, {'amp': 0.6}, z=3, idle=[{'type': 'bob', 'amount': 8, 'speed': 0.5}]),
        tag('BABY', L(W('baby'), s0), y='56%', size=56, accent=CYAN, w=360),
    ], camera={'preset': 'drift', 'amount': 0.4}, sfx=[('ding', B[4], 0.7)],
        notes='Turnstile: "should be easy, it\'s a baby" (41-44%), cute and calm, broken on the next word.')

    # 05 round 3 newborn (background change)
    s0 = B[5]
    t35, tmilk, tgain = L(W('thirtyfive'), s0), L(W('milk'), s0), L(W('gains'), s0)
    add(5, ocean(8, rays=9, snow=20, topColor='#5fd0d8', midColor='#1e8fa6', bottomColor='#0d4f66'), [
        comp('explainer/BlueWhale', '42%', '24%', 900, 260, {'pxPerM': 30, 'amp': 0.6}, z=3),
        you('88%', '25%', 120, pose='shrug', z=4),
        stat(2.5, t35, x='50%', y='37%', size=110, prefix='~', suffix=' T', decimals=1, duration=0.5),
        *count_grid(35, 7, 96, 88, 540 - 7 * 96 / 2, 820, t35, t35 + 0.4, end=tgain),
        {'type': 'particles', 'preset': 'bubbles', 'count': 80, 'color': '#ffffff', 'size': [4, 9], 'speed': 0.5, 'seed': 7,
         'x': '40%', 'y': '34%', 'width': 900, 'height': 500, 'z': 5, 'start': tmilk},
        comp('explainer/SpeedBars', '50%', '62%', 960, 260, {'rows': [
            {'label': 'CALF GAINS / DAY', 'value': 90, 'unit': ' KG', 'color': CYAN},
            {'label': 'ONE YOU', 'value': 70, 'unit': ' KG', 'color': WHITE}], 'max': 100, 'at': tgain, 'size': 34}, z=20, depth=0,
             start=tgain),
    ], camera={'preset': 'panRight', 'amount': 0.4}, trans={'type': 'cut', 'duration': 0.0},
        captionY=0.76,
        sfx=[('whoosh', W('newborn'), 0.6), ('tick', W('thirtyfive'), 0.6), ('pop', W('gains'), 0.6), ('ding', W('point', 2), 0.6)],
        notes='Calf: BlueWhale pxPerM 30 (draws 7 m at the scene scale of 120 px/m = 840 px); YOU pxPerM 120 (210 px). 35-icon CountGrid.')

    # 06 round 4 lunch (hard cut, no slam)
    s0 = B[6]
    t_scale, t_200, t_side, t_tom = L(W('scale'), s0), L(W('two', 1), s0), L(W('side'), s0), L(W('tomorrow'), s0)
    add(6, ocean(15, rays=5, snow=20), [
        tag('ROUND 4', 0.0, y=380, size=40, accent=RED, w=380, out=t_scale - 0.3),
        {'type': 'particles', 'preset': 'dust', 'count': 300, 'color': '#ff8fa3', 'size': [3, 8], 'speed': 0.4, 'seed': 11,
         'x': '50%', 'y': '50%', 'width': 1080, 'height': 1920, 'z': 1},
        *count_grid(230, 23, 40, 48, 540 - 23 * 40 / 2, 520, t_200, t_side),
        comp('explainer/Balance', '50%', 1150, 1000, 460, {
            'left': {'species': 'krill', 'w': 340, 'at': 0.2, 'pos': 0.3},
            'right': {'species': 'you', 'w': 90, 'at': t_200, 'pos': 0.3, 'drop': True},
            'tilt': [{'t': 0, 'v': -14}, {'t': t_200, 'v': -14}, {'t': t_side, 'v': 0, 'ease': 'out'},
                     {'t': t_tom, 'v': 0}, {'t': t_tom + 0.4, 'v': -14, 'ease': 'backOut'}]}, z=10),
        stat(16, t_scale, x='50%', y=400, size=80, prefix='~', suffix=' T / DAY', duration=0.6),
        tag('SAVOCA ET AL. 2021', t_scale + 0.3, y=486, size=22, w=420, accent=CYAN),
        tag('DAY 2', t_tom, x='76%', y=940, size=48, accent=RED, w=300),
    ], camera={'keyframes': [kf(0, zoom=1.0, y='45%'), kf(t_200, zoom=1.0, y='45%'), kf(t_side, zoom=1.0, y='52%', ease='inOut'),
                             kf(B[7] - s0, zoom=1.04, y='52%')]},
        captionY=0.76,
        sfx=[('boom', B[6], 0.6), ('tick', W('scale'), 0.5)] + [('tick', W('two', 1) + 0.18 * k, 0.4) for k in range(10)]
            + [('impact', W('side'), 0.7), ('pop', W('tomorrow'), 0.6), ('ding', W('point', 3), 0.6)],
        notes='Peak. 230-icon CountGrid (23x10, 44x62 px icons) fills the top row by row; Balance levels on "side", re-tips on "tomorrow".')

    # 07 round 5 myth set-up (inside the vessel)
    s0 = B[7]
    red_bg = {'type': 'gradient', 'kind': 'radial', 'colors': ['#6a1018', '#2a0508', '#120203'], 'depth': 0.1, 'overscan': 1.2}
    add(7, red_bg, [
        headline('ROUND 5', at=0.0, out=1.1, color='green'),
        {'type': 'particles', 'preset': 'bubbles', 'count': 180, 'color': '#c0303a', 'size': [8, 18], 'speed': 0.5, 'seed': 5,
         'x': '50%', 'y': '50%', 'width': 1080, 'height': 1920, 'z': 1},
        svg(tunnel_svg(), '50%', '42%', 800, 800, z=2),
        {**comp('explainer/Diver', '50%', '62%', 420, 120, {'kick': 1.2, 'arms': 'forward'}, z=4, rotate=-80),
         'keyframes': [kf(0, y='70%', scale=1.0), kf(B[8] - s0, y='46%', scale=0.45, ease='in')]},
        tag('MYTH?', L(W('heard'), s0), y='60%', size=52, accent=RED, w=360),
    ], camera={'preset': 'pushIn', 'amount': 0.8},
        sfx=[('ding', B[7], 0.7), ('underwater_rumble', B[7] + 0.2, 0.5)],
        notes='Background change: inside the blood vessel. Diver swims for the tunnel.')

    # 08 round 5 ring (pxPerM 2000)
    s0 = B[8]
    t_cant, t_ball, t_head, t_in, t_sh, t_big, t_pt = (L(W('can\'t'), s0), L(W('basketball', 1), s0), L(W('head'), s0),
                                                      L(W('in'), s0), L(W('shoulders'), s0), L(W('bigger', 1), s0), L(W('point', 4), s0))
    ring_y, head_y, stop_y, bust_y = 640, 960, 1180, 1200   # bust box 960x900 centred at bust_y: head centre at bust_y - 240
    add(8, red_bg, [
        tag('MYTH', 0.0, x='24%', y=380, size=56, accent=RED, w=320),
        {'type': 'rect', 'x': '24%', 'y': 380, 'width': 280, 'height': 12, 'fill': RED, 'z': 26, 'depth': 0,
         'start': t_cant, 'enter': {'type': 'wipeRight', 'duration': 0.3}},
        stat(23, t_ball, x='80%', y=380, size=72, prefix='~', suffix=' CM', duration=0.5),
        {'type': 'circle', 'x': '50%', 'y': ring_y, 'width': 460, 'height': 460, 'fill': 'rgba(0,0,0,0)', 'stroke': RED,
         'strokeWidth': 18, 'z': 8, 'start': 0.6, 'enter': {'type': 'pop', 'duration': 0.3},
         'keyframes': [kf(0, y=ring_y), kf(t_head, y=ring_y), kf(t_in, y=head_y, ease='inOut'), kf(t_sh, y=head_y),
                       kf(t_sh + 0.25, y=stop_y, ease='out')]},
        {**svg(basketball_svg(), '50%', ring_y, 480, 480, z=9, start=t_ball, end=t_head),
         'keyframes': [kf(t_ball, y=-300), kf(t_ball + 0.45, y=ring_y, ease='bounce')]},
        {**svg(bust_svg(), '50%', bust_y, 960, 900, z=7, start=t_ball + 0.3),
         'keyframes': [kf(t_ball + 0.3, y=2300), kf(t_head, y=bust_y, ease='out')]},
        tag('BIGGER WINS: YOU', t_big, y=520, size=48, accent=GREEN, w=700),
    ], camera={'keyframes': [kf(0, zoom=1.0), kf(B[9] - s0, zoom=1.03)],
               'shake': [{'at': t_sh + 0.2, 'duration': 0.35, 'amplitude': 16}]},
        grade={'brightness': 1.05}, captionY=0.76,
        sfx=[('glitch', W('can\'t'), 0.7), ('pop', W('basketball', 1), 0.6), ('impact', W('shoulders') + 0.2, 0.8),
             ('ding', W('point', 4), 0.8), ('pop', W('point', 4) + 0.1, 0.6)],
        notes='True scale at 2000 px/m: aorta ring 23 cm = 460 px, basketball 24 cm = 480 px, bust head 16 cm = 320 px wide, '
              'shoulders 45 cm = 900 px. The ring slides over the head (fits) and stops on the shoulders (shake).')

    # 09 stinger
    s0 = B[9]
    add(9, ocean(30, rays=6, snow=40), [
        headline('WHALE 4 : 1 YOU', at=0.0, y='40%', size=92, underline=False),
        svg(round_icons_svg(), '50%', '54%', 1000, 200, z=10, start=0.4, enter={'type': 'slideUp', 'duration': 0.35}),
        # the one win: the ring icon (svg x 910 -> 40 + 910 = 950 px) lights up on "you one" and again on "won"
        {'type': 'circle', 'x': 950, 'y': 1047, 'width': 190, 'height': 190, 'fill': 'rgba(61,220,132,0.18)', 'stroke': GREEN,
         'strokeWidth': 8, 'z': 11, 'depth': 0, 'start': L(W('you', after=58.0), s0), 'enter': {'type': 'pop', 'duration': 0.25},
         'keyframes': [kf(L(W('won'), s0), scale=1.0), kf(L(W('won'), s0) + 0.2, scale=1.25, ease='out'),
                       kf(L(W('won'), s0) + 0.45, scale=1.0)]},
    ], camera={'keyframes': [kf(0, zoom=1.0), kf(L(W('too', 1), s0), zoom=1.05), kf(L(W('too', 1), s0) + 0.2, zoom=1.16, ease='out'),
                             kf(B[10] - s0, zoom=1.17)]},
        sfx=[('riser', B[9] + 0.05, 0.4), ('boom', W('too', 1), 0.8)],
        notes='Final score held centre; punch on "too big". Hard stop on "big".')

    # 10 loop shot = frame 0
    add(10, ocean(25, rays=8, snow=60), hook_layers(), camera={'preset': 'pushIn', 'amount': 0.4 * (B[11] - B[10]) / B[1]},
        notes='Loop: exact frame-0 recomposition, score reset to 0 : 0 (score_layers gives the 0 : 0 state only at t=0, so set it here).')
    S[-1]['layers'] = [l for l in S[-1]['layers'] if not (l.get('name') == 'explainer/Tag' and 'WHALE' in l['props'].get('text', ''))]
    S[-1]['layers'].append(tag('WHALE 0 : 0 YOU', -0.6, y=270, size=44, accent=RED, w=640, bg='#0b1a22', color=WHITE))
    return S


def captions():
    emph = {('small.', 0), ('big.', 0)}
    seen = {}
    words = []
    for w in WORDS:
        k = w['text']
        n = seen.get(k, 0)
        seen[k] = n + 1
        d = {'text': w['text'], 'start': w['start'], 'end': w['end']}
        if (k, n) in emph:
            d['emph'] = True
        words.append(d)
    return {'enabled': True, 'words': words, 'maxWords': 4, 'maxChars': 20, 'linger': 0.1,
            'glue': ['basketball court', 'five of you', 'thirty-five of you', 'whole you', 'two hundred and thirty',
                     'Point, whale.', 'Point, you.', 'too big.'],
            'style': {'font': 'display', 'fontSize': 84, 'color': '#ffffff', 'highlight': '#ff5a4a', 'highlightMode': 'none',
                      'strokeWidth': 12, 'uppercase': True, 'y': 0.72}}


sb = {
    'version': 1,
    'id': SLUG,
    'title': '5 Rounds Against A Blue Whale (You Win One)',
    'format': '9:16',
    'fps': 30,
    'scenes': scenes(),
    'captions': captions(),
    'audio': {'voice': [{'src': f'episodes/{SLUG}/mix.wav', 'start': 0, 'volume': 1, 'duration': 61.93}],
              'music': [], 'sfx': [], 'duckOn': 'none'},
    'overlays': {'grain': 0.04, 'vignette': 0.2, 'fadeIn': 0, 'fadeOut': 0},
}
total = sum(s['duration'] for s in sb['scenes'])
assert abs(total - TOTAL) < 0.02, total
json.dump(sb, open(OUT, 'w'), indent=1)
print(f'wrote {OUT}: {len(sb["scenes"])} scenes, {total:.2f}s, cuts at ' + ', '.join(f'{b:.2f}' for b in B))
