#!/usr/bin/env python3
"""Generate storyboard.json for explainer-short-mantis-shrimp-punch from the narration and shot
list in script.md (keep the two in sync). Stdlib only, safe on the Mac.

usage: python3 gen_storyboard.py <out.json> [--table]
  --table also prints the estimated timing table used in script.md.

Timing is an ESTIMATE: Kokoro am_michael at speed 0.96 measured ~182 wpm on pilot 3
(commit 21b4598). Each word gets a share of its paragraph's time weighted by length, with
0.1 s joins between paragraphs (Shorts never stop for breath), one 0.3 s tone-break gap before the
twist (dipBlack), and a 0.35 s tail after the last word. The builder re-times every scene from
the real Kokoro word timings (pipeline/episodes/build.py); shot anchors are word indices, so the
re-time is mechanical.
"""
import json
import re
import sys

EP = 'explainer-short-mantis-shrimp-punch'
WPM = 182.0
JOIN = 0.10
TONE_BREAK = 0.30  # before P9 only
TAIL = 0.35

# ------------------------------------------------------------------ narration (one paragraph = one beat)
P = [
    "At your size, this shrimp would hit you twice.",
    "The real one is the size of your finger, yet its club can hit at double a pro boxer's punch speed, underwater, so",
    "stretch it seventeen times to your height, keep the timing, and ignore the screaming physicists.",
    "Now that club crosses to your face at about four hundred meters a second, handgun bullet speed, before your eyelids even start to close.",
    "And no muscle is that fast. A latch holds the club while a saddle-shaped spring loads, like a crossbow, until it lets go.",
    "Then it hits you again. The swing tears the water into a bubble, and when it caves in, it slams you a second time, with a flash of light and heat.",
    "And that's usually the weaker hit.",
    "Its real punch lands with up to two and a half thousand times its body weight. Scale that to you with the same lazy math, and it's about two hundred tons, a blue whale swung at your chin. You'd get hit twice and remember neither. No referee would bother counting you out.",
    "Okay, relax, giant shrimp are made up. The small ones aren't, and they hide in live rock and ride into home fish tanks, so you might only find yours by the snaps at night. One in an English aquarium, no bigger than your finger, reportedly cracked its own glass.",
    "Staff moved him to a tougher tank and named him Tyson.",
]


def word_weight(w: str) -> float:
    core = re.sub(r"[^A-Za-z']", '', w)
    return 0.55 + 0.11 * len(core) + (0.12 if re.search(r'[,.;:]$', w) else 0.0)


def timings():
    """Return [(para, idx, word, start, end)] and the total length."""
    out, t = [], 0.0
    for pi, para in enumerate(P):
        if pi == 8:
            t += TONE_BREAK
        elif pi > 0:
            t += JOIN
        words = para.split()
        dur = len(words) / WPM * 60.0
        ws = [word_weight(w) for w in words]
        k = dur / sum(ws)
        for wi, (w, wt) in enumerate(zip(words, ws)):
            out.append((pi, wi, w, round(t, 3), round(t + wt * k, 3)))
            t += wt * k
    return out, round(t + TAIL, 2)


WORDS, TOTAL = timings()


def at(pi, wi=0):
    for p, i, _w, s, _e in WORDS:
        if p == pi and i == wi:
            return s
    raise KeyError((pi, wi))


def word_index(pi, needle):
    words = P[pi].split()
    n = needle.split()
    for i in range(len(words) - len(n) + 1):
        if [re.sub(r'[^\w\']', '', x).lower() for x in words[i:i + len(n)]] == [x.lower() for x in n]:
            return i
    raise KeyError((pi, needle))


def A(pi, needle=None):
    return at(pi, 0 if needle is None else word_index(pi, needle))


# ------------------------------------------------------------------ layer helpers
RED = '#e5483d'
WHITE = '#f3f6f7'
INK = '#0b1a22'
PX_HUMAN = 400  # px per metre for the human-scale two-shots (You = 700 px tall)


def comp(name, x, y, w, h, props=None, **kw):
    d = {'type': 'component', 'name': name, 'x': x, 'y': y, 'width': w, 'height': h, 'props': props or {}}
    d.update(kw)
    return d


def headline(text, t, out=None, y='15%', color='white', red=None, size=112, **kw):
    p = {'text': text, 'at': t, 'size': size, 'color': color, 'underline': False}
    if red:
        p['red'] = red
    if out is not None:
        p['out'] = out
    return comp('explainer/Headline', '50%', y, 1000, 360, p, depth=0, z=20, **kw)


def tag(text, x, y, t, out=None, accent=RED, size=44, w=520, **kw):
    p = {'text': text, 'at': t, 'size': size, 'accent': accent}
    if out is not None:
        p['out'] = out
    return comp('explainer/Tag', x, y, w, 110, p, depth=0, z=18, **kw)


def stat(value, suffix, t, label=None, x='50%', y='30%', color=RED, decimals=0, size=150, prefix=None):
    p = {'value': value, 'suffix': suffix, 'at': t, 'duration': 0.6, 'size': size, 'color': color, 'decimals': decimals}
    if label:
        p['label'] = label
    if prefix:
        p['prefix'] = prefix
    return comp('explainer/Stat', x, y, 900, 320, p, depth=0, z=19)


def you(x, y, pose='stand', px=PX_HUMAN, **kw):
    kw.setdefault('z', 4)
    return comp('explainer/You', x, y, 360, int(1.75 * px) + 40, {'pose': pose, 'pxPerM': px, 'align': 'bottom'}, **kw)


def shrimp(x, y, length_m, px, club, pose='side', w=None, h=None, **kw):
    """explainer/MantisShrimp: NEW kit figure (marine.tsx), see script.md 'Kit work'."""
    w = w or int(length_m * px * 1.15) + 40
    h = h or int(length_m * px * 0.75) + 40
    kw.setdefault('z', 5)
    return comp('explainer/MantisShrimp', x, y, w, h,
                {'lengthM': length_m, 'pxPerM': px, 'align': 'bottom', 'pose': pose, 'club': club}, **kw)


def svg(markup, x, y, w, h, **kw):
    d = {'type': 'svg', 'markup': markup, 'x': x, 'y': y, 'width': w, 'height': h}
    d.update(kw)
    return d


def circle(x, y, d, fill, keyframes, **kw):
    c = {'type': 'circle', 'x': x, 'y': y, 'width': d, 'height': d, 'fill': fill, 'keyframes': keyframes}
    c.update(kw)
    return c


def rect(x, y, w, h, fill, **kw):
    r = {'type': 'rect', 'x': x, 'y': y, 'width': w, 'height': h, 'fill': fill}
    r.update(kw)
    return r


OCEAN = lambda depth=8, **p: {'type': 'component', 'name': 'explainer/Ocean', 'depth': 0.12, 'overscan': 1.2,
                              'props': {'depth': depth, 'rays': 7, 'snow': 70, **p}}
BLACK = {'type': 'color', 'color': '#05090c'}
ROOM = {'type': 'gradient', 'kind': 'linear', 'angle': 180, 'colors': ['#2a2f36', '#15181d']}
NIGHT = {'type': 'gradient', 'kind': 'linear', 'angle': 180, 'colors': ['#0a0f1a', '#04060a']}

SAND = rect('50%', '87%', 1400, 520, '#1d3a40', depth=1, z=1)  # seabed band for human-scale two-shots

# inline art (static markup; motion comes from layer keyframes)
SVG_FINGER = ('<svg viewBox="0 0 300 700" xmlns="http://www.w3.org/2000/svg"><path d="M60 700 L60 170 Q60 40 150 40 '
              'Q240 40 240 170 L240 700 Z" fill="#e8b48f"/><path d="M95 120 Q150 70 205 120 L205 200 Q150 225 95 200 Z" '
              'fill="#f6d5bd"/><path d="M80 330 Q150 350 220 330 M80 470 Q150 490 220 470" stroke="#c48d6a" stroke-width="8" fill="none"/></svg>')
SVG_SPRING = ('<svg viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg"><path d="M10 60 Q75 0 150 60 Q225 120 290 60" '
              'stroke="#ffe14d" stroke-width="22" fill="none" stroke-linecap="round"/></svg>')
SVG_LATCH = ('<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg"><path d="M10 110 L10 30 L70 30 L110 70 L70 70 '
             'L70 110 Z" fill="#f3f6f7"/></svg>')
SVG_BULLET = ('<svg viewBox="0 0 400 120" xmlns="http://www.w3.org/2000/svg"><path d="M0 20 L250 20 Q390 20 400 60 Q390 100 '
              '250 100 L0 100 Z" fill="#c9a24a"/><rect x="0" y="20" width="60" height="80" fill="#8c6d2c"/>'
              '<path d="M-400 60 L-10 60" stroke="#f3f6f7" stroke-width="6" stroke-dasharray="30 18" opacity=".6"/></svg>')
SVG_CRACK = ('<svg viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg"><g stroke="#e9f6ff" stroke-width="6" fill="none" '
             'stroke-linecap="round"><path d="M300 300 L210 170 L170 40"/><path d="M300 300 L420 220 L560 190"/>'
             '<path d="M300 300 L330 450 L300 590"/><path d="M300 300 L160 360 L30 420"/><path d="M300 300 L440 400 L520 540"/>'
             '<circle cx="300" cy="300" r="26"/><circle cx="300" cy="300" r="60" stroke-width="3"/></g></svg>')
SVG_ROCK = ('<svg viewBox="0 0 700 360" xmlns="http://www.w3.org/2000/svg"><path d="M20 360 Q0 230 90 180 Q120 60 250 80 '
            'Q330 10 430 70 Q560 40 610 160 Q700 220 680 360 Z" fill="#6f5a4c"/><g fill="#4b3a30"><circle cx="190" cy="230" r="34"/>'
            '<circle cx="330" cy="160" r="22"/><circle cx="480" cy="250" r="40"/><circle cx="560" cy="170" r="18"/></g>'
            '<ellipse cx="480" cy="250" rx="30" ry="22" fill="#05090c"/></svg>')
SVG_BLACKOUT = ('<svg viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="v" cx="50%" cy="45%" r="70%">'
                '<stop offset="35%" stop-color="#000" stop-opacity="0"/><stop offset="100%" stop-color="#000" stop-opacity="1"/>'
                '</radialGradient></defs><rect width="1080" height="1920" fill="url(#v)"/></svg>')


def kf(*pairs, **const):
    return [{'t': t, **const, **v} for t, v in pairs]


# ------------------------------------------------------------------ shots
# (id, start_time, background, layers, camera, transition, sfx[(cue, scene-local t, vol)], notes)
SHOTS = []


def shot(sid, t0, bg, layers, camera=None, trans='cut', sfx=(), notes='', grade=None):
    SHOTS.append(dict(id=sid, t0=round(t0, 3), bg=bg, layers=layers, camera=camera, trans=trans, sfx=sfx, notes=notes,
                      grade=grade))


# P1 HOOK: frame 1 = human-size shrimp squared up to YOU, club cocked
t_twice = A(0, 'twice')
shot('s01_hook', 0.0, OCEAN(6),
     [SAND, shrimp('64%', '62%', 1.75, PX_HUMAN, -40, pose='display', flipX=True),
      you('24%', '60%', 'panic'), tag('YOU', '24%', '36%', 0, accent=INK, size=40, w=220),
      headline('AT YOUR\nSIZE', 0, color='white', red='SIZE')],
     camera={'preset': 'pushIn', 'amount': 0.6}, sfx=[('whoosh', 0.0, 0.7)],
     notes='Frame 1 is the thumbnail: meral-spread threat pose (real display behaviour), club cocked, YOU tagged.')
shot('s02_hit_twice', t_twice - 0.25, OCEAN(6),
     [SAND, shrimp('64%', '62%', 1.75, PX_HUMAN, [{'t': 0, 'v': -40}, {'t': 0.25, 'v': 60, 'ease': 'in'}], pose='display', flipX=True),
      you('24%', '60%', 'panic', keyframes=kf((0, {'x': '24%'}), (0.3, {'x': '17%', 'rotate': -12, 'ease': 'out'}),
                                                (0.75, {'x': '11%', 'rotate': -24, 'ease': 'out'}))),
      circle('36%', '50%', 120, '#ffffff', kf((0.25, {'scale': 0.2, 'opacity': 1}), (0.45, {'scale': 3, 'opacity': 0, 'ease': 'out'})), z=8),
      circle('30%', '50%', 120, '#fff6c8', kf((0.65, {'scale': 0.2, 'opacity': 1}), (0.85, {'scale': 2.4, 'opacity': 0, 'ease': 'out'})), z=8),
      headline('HITS YOU\nTWICE', 0.25, color='white', red='TWICE')],
     camera={'shake': [{'at': 0.25, 'duration': 0.3, 'amplitude': 16}, {'at': 0.65, 'duration': 0.3, 'amplitude': 10}]},
     sfx=[('impact', 0.25, 0.9), ('pop', 0.65, 0.8)],
     notes='Two hits 0.4 s apart: the hook plants "twice"; the second ring is warm-tinted (the bubble flash) for the 0:33 payoff.')

# P2 REVEAL + STAKES
shot('s03_reveal', A(1), OCEAN(4),
     [svg(SVG_FINGER, '72%', '58%', 300, 700, z=3, rotate=-8),
      shrimp('40%', '52%', 0.10, 3600, -30, w=480, h=330),
      comp('explainer/ScaleBar', '40%', '64%', 360, 80, {'label': '~10 CM', 'at': 0.2, 'from': 'left'}, depth=0, z=10),
      tag('REAL SIZE', '40%', '30%', 0.1, accent=INK, w=360)],
     camera={'preset': 'pushIn', 'amount': 0.5}, sfx=[('pop', 0.2, 0.6)],
     notes='Hard cut to macro: real shrimp beside a fingertip. "finger" is planted here and paid at 1:12.')
shot('s04_boxer', A(1, 'yet its club'), OCEAN(4),
     [comp('explainer/SpeedBars', '50%', '36%', 960, 520,
           {'title': 'PUNCH SPEED', 'rows': [{'label': 'PRO BOXER', 'value': 9, 'unit': 'm/s', 'color': '#8a9aa3'},
                                              {'label': 'MANTIS SHRIMP (10 CM)', 'value': 23, 'unit': 'm/s', 'color': RED}],
            'max': 25, 'at': 0.1, 'duration': 0.7, 'stagger': 0.5}, depth=0, z=10),
      tag('2x', '84%', '22%', A(1, 'double') - A(1, 'yet its club'), accent=RED, size=72, w=200),
      tag('UP TO 80 KM/H · 50 MPH · UNDERWATER', '50%', '58%', A(1, 'underwater') - A(1, 'yet its club'), w=900, size=38)],
     sfx=[('tick', 0.1, 0.6), ('tick', 0.6, 0.6), ('whoosh', A(1, 'underwater') - A(1, 'yet its club'), 0.5)],
     notes='The felt number is the boxer; the raw speed is a silent tag.')

# P3 SCALE-UP + hedge
shot('s05_scale_up', A(2), OCEAN(6),
     [SAND, you('28%', '60%', 'stand'),
      shrimp('62%', '62%', 0.10, PX_HUMAN, -30, flipX=True,
             w=int(1.75 * PX_HUMAN * 1.15) + 40, h=int(1.75 * PX_HUMAN * 0.75) + 40,
             keyframes=kf((0, {'scale': 1 / 17.5}), (1.4, {'scale': 1.0, 'ease': 'out'}))),
      stat(17, '', 0.3, prefix='x', y='22%', size=170)],
     camera={'preset': 'pullOut', 'amount': 0.5}, sfx=[('whoosh_long', 0.0, 0.7)],
     notes='Same pxPerM for both; the shrimp layer scales 1/17.5 -> 1 so the sizes stay honest.')
shot('s06_physicists', A(2, 'and ignore'), OCEAN(6),
     [SAND, you('28%', '60%', 'stand'), shrimp('62%', '62%', 1.75, PX_HUMAN, -30, flipX=True),
      comp('explainer/You', '86%', '70%', 160, 240, {'pose': 'panic', 'color': '#ffe14d', 'pxPerM': 120, 'align': 'bottom'},
           z=7, idle=[{'type': 'jitter', 'amount': 6, 'speed': 8}]),
      tag('PHYSICIST', '86%', '58%', 0, accent='#ffe14d', size=34, w=280),
      tag('LAZY MATH: SAME TIMING, 17x SIZE', '50%', '24%', 0.1, accent='#ffe14d', w=900, size=38)],
     sfx=[('tick', 0.1, 0.6)],
     notes='The hedge sits on the scaling itself (fmZfphacPPQ "somehow" analogue).')

# P4 RUNG 1: speed at you
shot('s07_bullet_speed', A(3), OCEAN(6),
     [SAND, you('22%', '60%', 'panic'),
      shrimp('62%', '62%', 1.75, PX_HUMAN, [{'t': 0, 'v': -40}, {'t': 0.9, 'v': -40}, {'t': 1.0, 'v': 55, 'ease': 'in'}], flipX=True),
      stat(400, ' M/S', 0.4, label='≈ 900 MPH', y='22%'),
      tag('AT YOUR FACE', '30%', '36%', A(3, 'a second') - A(3), accent=RED, w=420, size=40)],
     camera={'preset': 'pushIn', 'amount': 0.4}, sfx=[('whoosh', 0.9, 0.8)],
     notes='Count-up lands on "four hundred".')
shot('s08_handgun', A(3, 'handgun'), OCEAN(6),
     [svg(SVG_BULLET, '50%', '36%', 520, 156, z=6, keyframes=kf((0, {'x': '110%'}), (0.9, {'x': '-10%', 'ease': 'linear'}))),
      tag('HANDGUN BULLET ~370 M/S', '50%', '26%', 0.05, w=700),
      tag('SCALED CLUB ~400 M/S', '50%', '48%', 0.3, w=700)],
     camera={'preset': 'panLeft', 'amount': 0.6}, sfx=[('whoosh', 0.05, 0.8)])
shot('s09_blink', A(3, 'before your eyelids'), OCEAN(6),
     [comp('explainer/SpeedBars', '50%', '36%', 960, 520,
           {'title': 'HOW LONG IT TAKES', 'rows': [{'label': 'YOUR BLINK', 'value': 150, 'unit': 'ms', 'color': '#8a9aa3'},
                                                    {'label': 'THE STRIKE', 'value': 3, 'unit': 'ms', 'color': RED}],
            'max': 160, 'at': 0.1, 'duration': 0.6, 'stagger': 0.4}, depth=0, z=10)],
     sfx=[('tick', 0.1, 0.5), ('tick', 0.5, 0.5)],
     notes='Felt timing without a spoken number (the old "fifty times" line is cut).')

# P5 MECH aside (re-hook "no muscle is that fast")
t_latch = A(4, 'A latch')
shot('s10_mechanism', A(4), BLACK,
     [shrimp('46%', '44%', 0.10, 7000, -45, w=820, h=560),
      svg(SVG_SPRING, '40%', '40%', 300, 120, z=7, start=t_latch - A(4) + 0.6,
          keyframes=kf((0, {'scaleX': 1.0}), (1.2, {'scaleX': 0.72, 'ease': 'inOut'}))),
      svg(SVG_LATCH, '52%', '47%', 90, 90, z=7, start=t_latch - A(4)),
      tag('LATCH', '64%', '54%', t_latch - A(4) + 0.1, accent=WHITE, size=38, w=240),
      tag('SADDLE SPRING', '30%', '32%', t_latch - A(4) + 0.7, accent='#ffe14d', size=38, w=380),
      headline('NOT\nMUSCLE', 0, out=t_latch - A(4), color='white', red='MUSCLE'),
      headline('LIKE A\nCROSSBOW', A(4, 'like a crossbow') - A(4), color='white', red='CROSSBOW')],
     camera={'preset': 'pushIn', 'amount': 0.7}, sfx=[('click', t_latch - A(4) + 0.15, 0.8)],
     notes='Physical order: latch holds the club, muscles load the spring, latch releases (Patek et al. 2004).')
shot('s11_release', A(4, 'until it lets go'), BLACK,
     [shrimp('46%', '44%', 0.10, 7000, [{'t': 0, 'v': -45}, {'t': 0.25, 'v': 60, 'ease': 'in'}], w=820, h=560),
      stat(10000, ' G', 0.35, label='YOU BLACK OUT AT ~5 G', y='20%', size=130)],
     camera={'shake': [{'at': 0.25, 'duration': 0.25, 'amplitude': 10}]}, sfx=[('impact', 0.25, 0.8)],
     notes='Silent landmark (fmZfphacPPQ grammar): the g-force pair is shown, not said, to keep the spoken number count in band.')

# P6 RUNG 3: the second hit
shot('s12_hits_again', A(5), OCEAN(6),
     [SAND, you('26%', '60%', 'panic', rotate=-10),
      shrimp('60%', '62%', 1.75, PX_HUMAN, 60, flipX=True),
      headline('HIT #2', 0, color='red')],
     camera={'preset': 'pushIn', 'amount': 0.8}, sfx=[('riser', 0.0, 0.4)],
     notes='Micro re-hook states the strange outcome first.')
t_bub = A(5, 'The swing')
t_cave = A(5, 'and when it caves')
T_SLAM = A(5, 'slams') - t_cave
T_FLASH = A(5, 'with a flash') - t_cave
shot('s13_bubble', t_bub, OCEAN(6),
     [SAND, you('26%', '60%', 'panic', rotate=-10),
      shrimp('60%', '62%', 1.75, PX_HUMAN, 60, flipX=True),
      circle('40%', '50%', 220, 'rgba(220,240,255,0.35)', kf((0.2, {'scale': 0.05}), (1.4, {'scale': 1.0, 'ease': 'out'})),
             z=8, stroke='#e9f6ff', strokeWidth=6),
      tag('CAVITATION BUBBLE', '40%', '36%', 0.6, accent='#7fe3ff', w=520)],
     camera={'preset': 'pushIn', 'amount': 0.5}, sfx=[('bubbles', 0.2, 0.6)])
shot('s14_collapse', t_cave, OCEAN(6),
     [SAND, you('26%', '60%', 'panic', keyframes=kf((0, {'x': '26%', 'rotate': -10}), (T_SLAM - 0.1, {'x': '26%', 'rotate': -10}),
                                                       (T_SLAM + 0.2, {'x': '18%', 'rotate': -28, 'ease': 'out'}))),
      shrimp('60%', '62%', 1.75, PX_HUMAN, 60, flipX=True),
      circle('40%', '50%', 220, 'rgba(220,240,255,0.35)', kf((0, {'scale': 1.0}), (T_SLAM - 0.1, {'scale': 1.0}), (T_SLAM, {'scale': 0.02, 'ease': 'in'})),
             z=8, stroke='#e9f6ff', strokeWidth=6, end=T_SLAM),
      circle('40%', '50%', 160, '#fff3b0', kf((T_FLASH, {'scale': 0.3, 'opacity': 1}), (T_FLASH + 0.5, {'scale': 3.2, 'opacity': 0, 'ease': 'out'})),
             z=9, start=T_FLASH, blend='screen'),
      headline('HIT #2', T_SLAM, color='red'),
      tag('FLASH OF LIGHT + HEAT', '50%', '28%', T_FLASH, accent='#ffe14d', w=640)],
     camera={'shake': [{'at': T_SLAM, 'duration': 0.3, 'amplitude': 12}]}, sfx=[('pop', T_SLAM, 0.9), ('impact', T_FLASH, 0.5)])

# P7 TURNSTILE (~50%): background change on the next word
shot('s15_turnstile', A(6), BLACK,
     [comp('explainer/SpeedBars', '50%', '40%', 960, 520,
           {'title': 'FORCE', 'rows': [{'label': 'HIT #2  BUBBLE', 'value': 50, 'unit': '%', 'color': '#8a9aa3'},
                                        {'label': 'HIT #1  CLUB', 'value': 100, 'unit': '%', 'color': RED, 'text': '???'}],
            'max': 100, 'at': 0.05, 'duration': 0.5, 'stagger': 0.6}, depth=0, z=10),
      tag('USUALLY', '50%', '64%', A(6, 'usually') - A(6), accent='#ffe14d', w=320, size=40)],
     camera={'preset': 'pullOut', 'amount': 0.6}, sfx=[('riser', 0.0, 0.7)],
     notes='False reassurance; "usually" keeps it true (cavitation peaks average ~50% of impact, Patek & Caldwell 2005).')

# P8 PEAK: force on you
shot('s16_real_force', A(7), BLACK,
     [shrimp('50%', '56%', 0.10, 4200, [{'t': 0, 'v': -40}, {'t': 0.8, 'v': -40}, {'t': 0.9, 'v': 60, 'ease': 'in'}], w=560, h=380),
      tag('MEASURED: UP TO 1,500 N', '50%', '72%', 0.9, accent=WHITE, w=640, size=38),
      stat(2500, 'x', A(7, 'two and a half') - A(7), label='ITS BODY WEIGHT', y='26%')],
     camera={'shake': [{'at': 0.9, 'duration': 0.2, 'amplitude': 6}]},
     sfx=[('impact', 0.9, 0.6), ('tick', A(7, 'two and a half') - A(7), 0.6)])
shot('s17_scaled_force', A(7, 'Scale that to you'), OCEAN(8),
     [SAND, you('26%', '60%', 'panic'), shrimp('62%', '62%', 1.75, PX_HUMAN, -40, flipX=True, pose='display'),
      tag('YOU', '26%', '36%', 0.0, accent=INK, size=40, w=220),
      tag('SAME LAZY MATH', '50%', '36%', A(7, 'same lazy math') - A(7, 'Scale that to you'), accent='#ffe14d', w=480, size=38),
      stat(200, ' TONS', A(7, "it's about") - A(7, 'Scale that to you'), label='≈ 190 TONNES', y='22%')],
     sfx=[('underwater_rumble', 0.2, 0.6)])
t_whale = A(7, 'a blue whale')
shot('s18_blue_whale', t_whale, OCEAN(10),
     [comp('explainer/BlueWhale', '50%', '48%', 1000, 220, {'pxPerM': 33, 'align': 'center'}, z=3,
           keyframes=kf((0, {'x': '130%'}), (0.7, {'x': '50%', 'ease': 'out'}),
                        (1.5, {'x': '50%', 'scale': 1}), (1.9, {'x': '72%', 'scale': 0.08, 'ease': 'in'}))),
      comp('explainer/You', '24%', '52%', 60, 80, {'pose': 'panic', 'pxPerM': 33, 'align': 'bottom'}, z=4),
      tag('YOU', '24%', '45%', 0, accent=INK, size=30, w=140),
      headline('ONE PUNCH', 0.1, y='16%', color='white', red='PUNCH')],
     camera={'preset': 'pushIn', 'amount': 0.4}, sfx=[('whoosh_long', 0.0, 0.6), ('impact', 1.9, 0.9)],
     notes='The whale never appears before "blue whale" is spoken; it shrinks into the club at "your chin".')
shot('s19_remember_neither', A(7, "You'd get hit"), OCEAN(8),
     [SAND, you('40%', '74%', 'stand', rotate=-90),
      tag('1', '30%', '50%', 0.2, accent=RED, size=60, w=120), tag('2', '50%', '50%', 0.55, accent='#ffe14d', size=60, w=120),
      tag('?', '40%', '40%', 1.0, accent=WHITE, size=60, w=120)],
     sfx=[('ding', 0.2, 0.4), ('ding', 0.55, 0.4)],
     notes='Gallows joke 1 (euphemism: knocked out, never said).')
shot('s20_referee', A(7, 'No referee'), OCEAN(8),
     [SAND, you('40%', '74%', 'stand', rotate=-90),
      comp('explainer/You', '76%', '62%', 300, 560, {'pose': 'shrug', 'color': '#ffe14d', 'pxPerM': 300, 'align': 'bottom'}, z=6,
           keyframes=kf((0, {'x': '76%'}), (1.0, {'x': '76%'}), (1.6, {'x': '115%', 'ease': 'in'}))),
      tag('REFEREE', '76%', '42%', 0, accent='#ffe14d', size=34, w=260, out=1.0)],
     sfx=[('footsteps', 1.0, 0.5)],
     notes='Gallows joke 2 pays the boxing frame planted at 0:05 ("pro boxer") ahead of "Tyson".')

# P9 TWIST: reality flip with a tone break
t_small = A(8, "The small ones")
shot('s21_tone_break', A(8), ROOM,
     [shrimp('50%', '52%', 1.75, 300, -30, pose='display', silhouette=True,
             keyframes=kf((0, {'scale': 1}), (0.6, {'scale': 1}), (0.8, {'scale': 0.02, 'ease': 'backIn'}))),
      tag('MADE UP', '50%', '30%', 0.2, accent=RED, size=56, w=420, rotate=-8)],
     trans='dipBlack', sfx=[('pop', 0.8, 0.7)],
     notes='Self-correcting tone break (PUFFER 0:43 analogue, no profanity).')
shot('s22_live_rock', t_small, ROOM,
     [rect('50%', '46%', 900, 620, 'rgba(90,170,200,0.28)', stroke='#cfe6ee', strokeWidth=10, radius=8, z=2),
      svg(SVG_ROCK, '50%', '58%', 700, 360, z=3),
      shrimp('69%', '60%', 0.10, 900, -30, w=140, h=100, z=4, keyframes=kf((0, {'opacity': 0}), (1.0, {'opacity': 1}))),
      tag('HITCHHIKES IN LIVE ROCK', '50%', '26%', 0.4, accent='#7fe3ff', w=720, out=A(8, 'ride into') - t_small),
      tag('INTO HOME FISH TANKS', '50%', '26%', A(8, 'ride into') - t_small, accent='#7fe3ff', w=720)],
     camera={'preset': 'pushIn', 'amount': 0.6}, sfx=[('bubbles', 0.0, 0.4)])
t_night = A(8, 'so you might')
shot('s23_snaps', t_night, NIGHT,
     [rect('50%', '46%', 900, 620, 'rgba(40,80,110,0.25)', stroke='#5d7a88', strokeWidth=10, radius=8, z=2),
      svg(SVG_ROCK, '50%', '58%', 700, 360, z=3, opacity=0.6),
      comp('explainer/You', '18%', '70%', 200, 380, {'pose': 'panic', 'pxPerM': 200, 'align': 'bottom'}, z=5),
      tag('SNAP', '66%', '50%', 0.5, accent=WHITE, size=48, w=200, out=0.9),
      tag('SNAP', '58%', '42%', 1.3, accent=WHITE, size=48, w=200, out=1.7)],
     grade={'brightness': 0.8, 'vignette': 0.5}, sfx=[('click', 0.5, 0.9), ('click', 1.3, 0.9)])
t_eng = A(8, 'One in an English')
T_CRACK = A(8, 'cracked') - t_eng
shot('s24_cracked_glass', t_eng, ROOM,
     [rect('50%', '46%', 900, 620, 'rgba(90,170,200,0.28)', stroke='#cfe6ee', strokeWidth=10, radius=8, z=2),
      shrimp('46%', '56%', 0.10, 1400, [{'t': 0, 'v': -40}, {'t': T_CRACK - 0.1, 'v': -40}, {'t': T_CRACK, 'v': 60, 'ease': 'in'}], w=200, h=140, z=4),
      tag('NO BIGGER THAN YOUR FINGER', '50%', '72%', A(8, 'no bigger') - t_eng, accent=RED, w=760, size=38),
      svg(SVG_CRACK, '56%', '50%', 420, 420, z=6, start=T_CRACK, enter={'type': 'zoomIn', 'duration': 0.15}),
      tag('GREAT YARMOUTH, ENGLAND · 1998 (REPORTED)', '50%', '22%', 0.2, accent=WHITE, w=940, size=34)],
     camera={'shake': [{'at': T_CRACK, 'duration': 0.2, 'amplitude': 6}]}, sfx=[('impact', T_CRACK, 0.8)])

# P10 STINGER: ends on "Tyson", last frame contrasts frame 1 (tiny shrimp, cracked glass, giant YOU)
t_tyson = A(9, 'Tyson')
shot('s25_tyson', A(9), ROOM,
     [rect('50%', '46%', 900, 620, 'rgba(90,170,200,0.28)', stroke='#cfe6ee', strokeWidth=10, radius=8, z=2),
      shrimp('46%', '56%', 0.10, 1400, -30, w=200, h=140, z=4),
      svg(SVG_CRACK, '56%', '50%', 420, 420, z=6),
      comp('explainer/You', '84%', '64%', 360, 900, {'pose': 'point', 'pxPerM': 480, 'align': 'bottom'}, z=7, opacity=0.95),
      tag('MOVED TO A TOUGHER TANK', '50%', '74%', A(9, 'tougher') - A(9), accent=WHITE, w=720, size=36, out=t_tyson - A(9)),
      headline('TYSON', t_tyson - A(9), y='18%', color='red', size=150)],
     sfx=[('stinger', t_tyson - A(9), 0.9)],
     notes='Hard cut 0.35 s after "Tyson". The loop restarts on the human-size shrimp of frame 1.')


# ------------------------------------------------------------------ assemble
def build():
    scenes = []
    for i, s in enumerate(SHOTS):
        end = SHOTS[i + 1]['t0'] if i + 1 < len(SHOTS) else TOTAL
        sc = {'id': s['id'], 'duration': round(end - s['t0'], 3), 'background': s['bg'], 'layers': s['layers'],
              'transitionIn': {'type': s['trans'], 'duration': 0.3 if s['trans'] != 'cut' else 0.0},
              'sfx': [{'cue': c, 'at': round(t, 3), 'volume': v} for c, t, v in s['sfx']],
              'notes': s['notes'] or ''}
        if s['camera']:
            sc['camera'] = s['camera']
        if s['grade']:
            sc['grade'] = s['grade']
        scenes.append(sc)
    words = []
    for p, i, w, st, en in WORDS:
        d = {'text': w, 'start': st, 'end': en}
        if i == 0:
            d['br'] = True
        words.append(d)
    return {
        'version': 1, 'id': EP, 'title': 'How A Mantis Shrimp Would Hit You Twice', 'format': '9:16', 'fps': 30,
        'scenes': scenes,
        'captions': {'enabled': True, 'words': words, 'maxWords': 3, 'maxChars': 18,
                     'glue': ['pro boxer', 'blue whale', 'live rock', 'fish tanks', 'four hundred', 'two hundred tons',
                              'saddle-shaped spring', 'handgun bullet'],
                     'style': {'font': 'display', 'fontSize': 84, 'color': '#ffffff', 'highlight': '#ff5a4a',
                               'highlightMode': 'none', 'strokeWidth': 12, 'uppercase': True, 'y': 0.70}},
        'audio': {'voice': [], 'music': [{'src': 'music/deep_ocean.m4a', 'start': 0, 'volume': 0.3, 'duckTo': 0.1,
                                          'fadeIn': 0.2, 'fadeOut': 0.2}],
                  'sfx': [], 'sfxDir': 'sfx', 'duckOn': 'captions'},
        'overlays': {'grain': 0, 'vignette': 0.15, 'fadeIn': 0, 'fadeOut': 0},
    }


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else 'storyboard.json'
    sb = build()
    with open(out, 'w') as f:
        json.dump(sb, f, indent=1, ensure_ascii=False)
    print(f'wrote {out}: {len(sb["scenes"])} scenes, {TOTAL:.2f} s, {len(WORDS)} words')
    if '--table' in sys.argv:
        for pi in range(len(P)):
            ws = [w for w in WORDS if w[0] == pi]
            print(f'P{pi + 1}: {ws[0][3]:6.2f}-{ws[-1][4]:6.2f}  ({len(ws)} w)')
        for i, s in enumerate(SHOTS):
            end = SHOTS[i + 1]['t0'] if i + 1 < len(SHOTS) else TOTAL
            print(f'{s["id"]:22s} {s["t0"]:6.2f} {end:6.2f}')


if __name__ == '__main__':
    main()
