#!/usr/bin/env python3
"""storyboard.json for horror-roommate-texts-from-room, built from the measured multi-voice timings
(audio/lines.json, audio/captions.json, audio/cues.json from gen_audio.py) and the shot list in script.md.

usage: python3 backlog/horror/horror-roommate-texts-from-room/gen_storyboard.py [--table]
  --table   also print the shot list as markdown rows (pasted into script.md, so the two never drift)

Every time is anchored to a spoken line, word or SFX cue, so a re-voice only needs new audio/*.json.
Kit gaps are drawn here as inline SVG layers instead of kit edits (studio/src/kits/horror is locked):
an interior bedroom door with no peephole/chain/deadbolt, a lever that turns slowly (layer rotate keyframes),
hands on the lever, three plates, a napkin, and the one photo.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = 'horror-roommate-texts-from-room'
LINES = {r['id']: r for r in json.load(open(os.path.join(HERE, 'audio', 'lines.json')))}
WORDS = json.load(open(os.path.join(HERE, 'audio', 'captions.json')))['words']
CUES = json.load(open(os.path.join(HERE, 'audio', 'cues.json')))
REPORT = json.load(open(os.path.join(HERE, 'audio', 'report.json')))
END = round(LINES['L42']['end'] + 0.55, 3)   # hard cut 0.55 s after "Come out."
RED = '#ff4b55'
INK = '#0b0c10'


def S(lid):
    return LINES[lid]['start']


def E(lid):
    return LINES[lid]['end']


def W(lid, i):
    return LINES[lid]['words'][i]['start']


def CUE(name, line, nth=0):
    hits = [c['at'] for c in CUES if c['name'] == name and c['line'] == line]
    return hits[nth]


# ------------------------------------------------------------------ inline SVG art (original, drawn here)
def door_svg(light=0.85, hue='#6a5442', hue2='#3e3128', wall='#232a36'):
    """Maya's bedroom door from inside: no peephole, no chain, no deadbolt (it does not lock). Lever drawn separately."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920">
<defs><linearGradient id="w" x1="0" x2="1"><stop offset="0" stop-color="{wall}"/><stop offset=".55" stop-color="#1d222d"/><stop offset="1" stop-color="#14171f"/></linearGradient>
<linearGradient id="d" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{hue}"/><stop offset="1" stop-color="{hue2}"/></linearGradient>
<radialGradient id="g" cx=".5" cy="0" r=".8"><stop offset="0" stop-color="#f4c47c" stop-opacity="{0.6 * light:.2f}"/><stop offset="1" stop-color="#f4c47c" stop-opacity="0"/></radialGradient></defs>
<rect width="1080" height="1920" fill="url(#w)"/>
<rect x="120" y="980" width="70" height="110" rx="10" fill="#cfc9bb" stroke="{INK}" stroke-width="4" opacity=".55"/>
<rect x="0" y="1700" width="1080" height="220" fill="#16141a"/>
<line x1="0" x2="1080" y1="1760" y2="1760" stroke="#100f13" stroke-width="4"/><line x1="0" x2="1080" y1="1840" y2="1840" stroke="#100f13" stroke-width="4"/>
<ellipse cx="540" cy="1702" rx="470" ry="150" fill="url(#g)"/>
<rect x="250" y="300" width="580" height="1404" fill="#2e3441" stroke="{INK}" stroke-width="8"/>
<rect x="290" y="340" width="500" height="1346" fill="url(#d)" stroke="{INK}" stroke-width="7"/>
<rect x="340" y="400" width="400" height="520" rx="6" fill="none" stroke="#2a211b" stroke-width="10" opacity=".7"/>
<rect x="340" y="990" width="400" height="630" rx="6" fill="none" stroke="#2a211b" stroke-width="10" opacity=".7"/>
<rect x="292" y="1686" width="496" height="13" fill="#ffd38e" opacity="{light:.2f}"/>
<circle cx="735" cy="1010" r="26" fill="#a9a59c" stroke="{INK}" stroke-width="5"/>
</svg>'''


LEVER = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 150 48"><rect x="4" y="12" width="128" height="24" rx="11" fill="#c2beb4" stroke="{INK}" stroke-width="5"/><circle cx="126" cy="24" r="14" fill="#a9a59c" stroke="{INK}" stroke-width="5"/></svg>'''


def feet_svg(pairs=1, spread=0):
    """Shadows of feet breaking the light strip under the door, with their long shadows on my floor."""
    xs = [430, 590] if pairs == 1 else [345, 455, 625, 735]
    shapes = ''.join(
        f'<rect x="{x - 32}" y="1684" width="64" height="17" rx="4" fill="#07070a"/>'
        f'<path d="M {x - 30} 1700 L {x + 30} 1700 L {x + 60 + spread} 1900 L {x - 60 - spread} 1900 Z" fill="#07070a" opacity=".55"/>'
        for x in xs)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920">{shapes}</svg>'


def lever_close_svg():
    """Extreme close-up of the door surface around the lever (the lever + hands are a separate rotating layer)."""
    grain = ''.join(f'<path d="M 0 {y} C 300 {y + 18} 700 {y - 22} 1080 {y + 6}" stroke="#4d3b2f" stroke-width="5" fill="none" opacity=".45"/>'
                    for y in range(140, 1900, 120))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920"><defs><linearGradient id="d" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6a5442"/><stop offset="1" stop-color="#352a22"/></linearGradient></defs>
<rect width="1080" height="1920" fill="url(#d)"/>{grain}
<rect x="990" y="0" width="90" height="1920" fill="#2e3441" stroke="{INK}" stroke-width="8"/>
<rect x="770" y="700" width="150" height="420" rx="40" fill="#9f9b92" stroke="{INK}" stroke-width="8"/>
<circle cx="845" cy="1060" r="22" fill="#2a2a2e"/></svg>'''


def lever_arm_svg(hands=0):
    """Big lever arm (pivot at 660,150 in this 760x520 box) with 0, 1 or 2 cartoon hands gripping it from below."""
    skin, sh = '#e8b897', '#c9906d'

    def hand(x):
        return (f'<path d="M {x - 70} 520 L {x - 64} 230 Q {x - 60} 160 {x} 160 Q {x + 60} 160 {x + 64} 230 L {x + 70} 520 Z" fill="{skin}" stroke="{INK}" stroke-width="7"/>'
                f'<path d="M {x - 82} 132 Q {x - 82} 100 {x - 46} 100 L {x + 50} 100 Q {x + 84} 100 {x + 84} 134 L {x + 84} 196 Q {x + 84} 228 {x + 50} 228 L {x - 46} 228 Q {x - 82} 228 {x - 82} 196 Z" fill="{skin}" stroke="{INK}" stroke-width="7"/>'
                + ''.join(f'<line x1="{x + d}" x2="{x + d}" y1="104" y2="150" stroke="{sh}" stroke-width="6"/>' for d in (-40, -4, 32)))
    hs = ''.join(hand(x) for x in ([300] if hands == 1 else [180, 430] if hands == 2 else []))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 520">
<rect x="10" y="110" width="680" height="84" rx="40" fill="#c8c4ba" stroke="{INK}" stroke-width="9"/>
<rect x="30" y="122" width="600" height="18" rx="9" fill="#e6e2d8" opacity=".7"/>
{hs}
<circle cx="660" cy="150" r="70" fill="#aaa69d" stroke="{INK}" stroke-width="9"/></svg>'''


def plates_svg():
    plate = lambda x, y: (f'<ellipse cx="{x}" cy="{y + 14}" rx="150" ry="62" fill="#000" opacity=".35"/>'
                          f'<ellipse cx="{x}" cy="{y}" rx="150" ry="62" fill="#efece4" stroke="{INK}" stroke-width="7"/>'
                          f'<ellipse cx="{x}" cy="{y}" rx="98" ry="38" fill="none" stroke="#cfc9bb" stroke-width="6"/>'
                          f'<rect x="{x + 170}" y="{y - 52}" width="14" height="110" rx="6" fill="#b9b5ab" stroke="{INK}" stroke-width="4"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920"><defs>
<radialGradient id="l" cx=".5" cy=".42" r=".7"><stop offset="0" stop-color="#e3a65c" stop-opacity=".55"/><stop offset="1" stop-color="#e3a65c" stop-opacity="0"/></radialGradient>
<linearGradient id="t" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a3c28"/><stop offset="1" stop-color="#2d1f16"/></linearGradient></defs>
<rect width="1080" height="1920" fill="#120f12"/><rect y="560" width="1080" height="1360" fill="url(#t)"/>
{''.join(f'<line x1="0" x2="1080" y1="{y}" y2="{y + 30}" stroke="#3a281c" stroke-width="5" opacity=".6"/>' for y in range(640, 1900, 150))}
{plate(330, 900)}{plate(740, 1060)}{plate(380, 1300)}
<rect width="1080" height="1920" fill="url(#l)"/></svg>'''


def gap_svg():
    """Low close-up of the gap under my door: the door's bottom edge, the warm strip, my floor."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920"><defs>
<radialGradient id="g" cx=".5" cy="0" r=".9"><stop offset="0" stop-color="#f4c47c" stop-opacity=".55"/><stop offset="1" stop-color="#f4c47c" stop-opacity="0"/></radialGradient>
<linearGradient id="d" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5e4a3a"/><stop offset="1" stop-color="#3a2d24"/></linearGradient></defs>
<rect width="1080" height="1920" fill="#0f0e12"/><rect width="1080" height="1060" fill="url(#d)"/>
<rect x="0" y="980" width="1080" height="80" fill="#2a2119"/>
<rect x="0" y="1060" width="1080" height="34" fill="#ffd38e"/>
<rect x="250" y="1060" width="150" height="34" fill="#07070a"/><rect x="640" y="1060" width="150" height="34" fill="#07070a"/>
<rect y="1094" width="1080" height="826" fill="#17151a"/><ellipse cx="540" cy="1100" rx="700" ry="420" fill="url(#g)"/>
<path d="M 250 1094 L 400 1094 L 330 1920 L 60 1920 Z" fill="#07070a" opacity=".5"/><path d="M 640 1094 L 790 1094 L 1020 1920 L 760 1920 Z" fill="#07070a" opacity=".5"/></svg>'''


NAPKIN = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 300"><path d="M 12 30 L 400 8 L 412 270 L 20 292 Z" fill="#f4f1ea" stroke="{INK}" stroke-width="6"/>
<path d="M 16 160 L 406 140" stroke="#d8d3c8" stroke-width="5"/><path d="M 210 20 L 216 282" stroke="#e3dfd6" stroke-width="4"/></svg>'''

NAPKIN_CLOSE = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920"><rect width="1080" height="1920" fill="#17151a"/>
<ellipse cx="540" cy="900" rx="700" ry="600" fill="#f4c47c" opacity=".16"/>
<path d="M 90 520 L 1000 470 L 1020 1420 L 110 1470 Z" fill="#f4f1ea" stroke="{INK}" stroke-width="10"/>
<path d="M 100 990 L 1010 950" stroke="#d6d0c4" stroke-width="8"/><path d="M 555 490 L 566 1445" stroke="#e3dfd6" stroke-width="6"/>
<circle cx="840" cy="1290" r="70" fill="#e8b46a" opacity=".22"/></svg>'''


def photo_svg():
    """The only image: shot from inside Dani's dark room, through her open doorway, across the flat to MY door.
    Greyscale. Someone is standing at my door, backlit by the strip under it. Faceless."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 1200"><defs>
<linearGradient id="h" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2b2b2b"/><stop offset="1" stop-color="#121212"/></linearGradient>
<radialGradient id="s" cx=".5" cy="1" r=".6"><stop offset="0" stop-color="#d9d9d9" stop-opacity=".7"/><stop offset="1" stop-color="#d9d9d9" stop-opacity="0"/></radialGradient></defs>
<rect width="900" height="1200" fill="#f2f2f0"/>
<g transform="translate(28 28)"><rect width="844" height="1100" fill="url(#h)"/>
<path d="M 0 1100 L 300 690 L 544 690 L 844 1100 Z" fill="#1d1d1d"/>
<rect x="300" y="200" width="244" height="490" fill="#262626"/>
<rect x="330" y="236" width="184" height="452" fill="#3d3d3d" stroke="#0a0a0a" stroke-width="5"/>
<rect x="332" y="682" width="180" height="8" fill="#e6e6e6"/>
<ellipse cx="422" cy="700" rx="230" ry="60" fill="url(#s)"/>
<path d="M 380 690 L 382 470 Q 384 420 422 412 Q 462 420 464 470 L 466 690 Z" fill="#050505"/>
<circle cx="422" cy="380" r="40" fill="#050505"/>
<path d="M 380 690 L 340 1100 L 360 1100 L 400 690 Z M 446 690 L 500 1100 L 520 1100 L 466 690 Z" fill="#050505" opacity=".6"/>
<rect x="0" y="0" width="120" height="1100" fill="#070707"/><rect x="724" y="0" width="120" height="1100" fill="#070707"/>
<path d="M 724 0 L 640 60 L 640 1040 L 724 1100 Z" fill="#141414"/>
<rect x="0" y="0" width="844" height="70" fill="#070707"/>
<text x="820" y="1080" text-anchor="end" font-family="Montserrat, sans-serif" font-size="30" font-weight="700" fill="#9a9a9a">11:51 PM</text></g></svg>'''


# ------------------------------------------------------------------ layer helpers
def comp(name, props, **kw):
    d = {'type': 'component', 'name': name, 'props': props}
    d.update(kw)
    return d


def svg(markup, x='50%', y='50%', w=1080, h=1920, **kw):
    d = {'type': 'svg', 'markup': markup, 'x': x, 'y': y, 'width': w, 'height': h}
    d.update(kw)
    return d


def vignette(amount=0.45, **p):
    return comp('horror/Vignette', {'amount': amount, **p}, depth=0, z=60)


def darkness(dark=0.6, x=0.5, y=0.55, radius=0.55):
    return comp('horror/Darkness', {'x': x, 'y': y, 'radius': radius, 'darkness': dark}, depth=0, z=55)


def maya(props, **kw):
    d = comp('horror/Protagonist', props, x='50%', y='100%', anchorY=1, width=1150, height=1748)
    d.update(kw)
    return d


def lever_layer(keys, hands=0, close=True):
    """Rotating lever. close=True: the big arm (+hands) in the close-up frame; else the small lever on door_svg."""
    if close:
        return svg(lever_arm_svg(hands), x=845, y=905, w=760, h=520, anchorX=660 / 760, anchorY=150 / 520, keyframes=keys, z=5)
    return svg(LEVER, x=735, y=1010, w=150, h=48, anchorX=126 / 150, anchorY=0.5, keyframes=keys, z=5)


def rot(t0, a0, t1, a1, ease='out'):
    return [{'t': round(max(0, t0), 3), 'rotate': a0}, {'t': round(max(0, t1), 3), 'rotate': a1, 'ease': ease}]


def jolt(at, depth=-9):
    """The handle forced down against a grip, then sprung back."""
    return [{'t': round(at, 3), 'rotate': 0}, {'t': round(at + 0.09, 3), 'rotate': depth, 'ease': 'out'}, {'t': round(at + 0.3, 3), 'rotate': 0, 'ease': 'backOut'}]


MEMBERS = {'Dani': {'color': '#8f4a5a', 'initials': 'D'}, "Dani's Mom": {'color': '#5a6f8f', 'initials': 'M'}, 'Maya': {'color': '#3d5a80', 'initials': 'M'}}


def handphone(chat=None, mode='chat', t0=0.0, lock=None, call=None, tremble=1.5, vibrate=None, banners=None, layer=None, **kw):
    phone = {'members': MEMBERS, 'mode': mode}
    if chat:
        phone['chat'] = chat
    if lock:
        phone['lock'] = lock
    if call:
        phone['call'] = call
    if vibrate:
        phone['vibrate'] = vibrate
    if banners:
        phone['banners'] = banners
    p = {'phoneWidth': 0.68, 'cx': 0.53, 'cy': 0.61, 'tilt': -3, 'tremble': tremble, 'side': 'right', 'thumbY': 0.94, 'thumbReach': 0.1, 'phone': phone}
    p.update(kw)
    return comp('horror/HandPhone', p, z=10, **(layer or {}))


# Dani thread, global times (bubbles pop when they are read; silent ones at their cue)
DANI_MSGS = [
    ('Dani', "don't come out of your room", S('L01')),
    ('Dani', "that one isn't me", S('L05')),
    ('Dani', "i've been in bed since nine. she has my face", S('L06')),
    ('Dani', "she's lying to you", CUE('message_pop', 'L11')),
    ('Dani', "rule one. don't answer her.", S('L14')),
    ('Dani', "rule two. if she tries your handle, hold it up. she can't open a door you're holding.", S('L16')),
    ('me', "how do I know you're the real one?", S('L17')),
    ('Dani', "because she wants you out there. i want you alive.", S('L18')),
    ('Dani', "don't. she's outside your door.", S('L21')),
    ('Dani', 'HOLD IT UP', S('L25')),
    ('Dani', 'MAYA HOLD IT', S('L25') + 0.55),
    ('me', 'where are you', S('B02')),
    ('me', 'WHO ARE YOU', S('B03')),
    ('Dani', '[Photo]', S('L37')),
]
DANI_TYPING = [(S('L05') - 0.55, S('L05')), (CUE('message_pop', 'L11') - 1.0, CUE('message_pop', 'L11')), (S('L14') - 0.5, S('L14')),
               (S('L18') - 0.45, S('L18')), (S('L21') - 0.9, S('L21')), (S('B04'), S('L37'))]
MOM_MSGS = [("Dani's Mom", 'thank you for the birthday flowers maya!! xx', -900.0),
            ('me', 'is Dani with you?', S('L33')),
            ("Dani's Mom", "Maya? Dani's been home with us since Sunday.", S('L34')),
            ("Dani's Mom", "She's asleep down the hall. I just checked.", S('L35'))]
MOM_TYPING = [(E('L33') + 0.1, S('L34')), (E('L34') + 0.05, S('L35'))]


def chat(title, msgs, typing, t0, clock='11:4' + '3', **kw):
    m = []
    for frm, text, at in msgs:
        d = {'text': text, 'at': round(at - t0, 3)}
        if frm == 'me':
            d['me'] = True
        else:
            d['from'] = frm
        m.append(d)
    ty = [{'from': title, 'at': round(a - t0, 3), 'until': round(b - t0, 3)} for a, b in typing]
    c = {'title': title, 'dm': title, 'messages': m, 'typing': ty, 'theme': 'dark', 'scale': 1.25, 'clock': clock, 'battery': 64,
         'accent': '#3d5a80', 'dayLabel': 'Today 11:40 PM', 'subtitle': 'iMessage'}
    c.update(kw)
    return c


# ------------------------------------------------------------------ shots
SHOTS = []   # (id, start, end, shot type, description, scene dict without duration)


def shot(sid, start, end, kind, desc, layers, camera=None, transition=None, sfx_note='', grade=None, captionY=None, notes=''):
    SHOTS.append(dict(id=sid, start=round(start, 3), end=round(end, 3), kind=kind, desc=desc, layers=layers, camera=camera,
                      transition=transition, sfx=sfx_note, grade=grade, captionY=captionY, notes=notes))


def build():
    c = [0.0]
    cut = lambda t: round(t, 3)
    # --- S1 hook: frame 0 = cover = the threat (the banner is already on the lock screen)
    a, b = 0.0, cut(S('L03') - 0.05)
    shot('s01', a, b, 'Phone POV, lock screen (cover)',
         'HandPhone lock 11:40, banner "Dani: don\'t come out of your room" already on screen at frame 0; behind it, my bedroom door blurred with the warm strip under it',
         [svg(door_svg(0.9), blur=9, opacity=0.8, depth=0.3),
          handphone(mode='lock', lock={'time': '11:40', 'date': 'Thursday', 'notifications': [{'at': -0.6, 'app': 'Messages', 'title': 'Dani', 'text': "don't come out of your room"}]}, tremble=1.0,
                    vibrate=[{'at': 0.05, 'duration': 0.4}]),
          vignette(0.5)],
         camera={'preset': 'pushIn', 'amount': 0.4}, sfx_note='notify at 0.0 (banner already present); muffled sizzle fades in under L02')
    # --- S1 contradiction: her voice from the kitchen
    a, b = b, cut(S('L05') - 0.06)
    shot('s02', a, b, 'Medium, Maya in bed', 'Bedroom lamp 0.15; Maya pose phone, light phone, looks toward the door (frame right); neutral -> scared on "Dani\'s voice"',
         [comp('horror/Bedroom', {'lamp': 0.15, 'phoneGlow': 0.8}, depth=0.2),
          maya({'pose': 'phone', 'light': 'phone', 'lookX': 0.8, 'exprs': [{'t': 0, 'e': 'worried'}, {'t': round(S('L04') - a, 3), 'e': 'scared'}]}),
          vignette(0.45)],
         camera={'preset': 'drift', 'amount': 0.6}, sfx_note='KITCHEN voice through the wall (1.8 kHz low-pass), sizzle under')
    # --- S2 named threat
    a, b = b, cut(S('L07') - 0.06)
    shot('s03', a, b, 'Phone POV, DM "Dani"', 'chat dm "Dani": the warning, then "that one isn\'t me" and "i\'ve been in bed since nine. she has my face"; typing dots first',
         [svg(door_svg(0.9), blur=10, opacity=0.6, depth=0.3), handphone(chat(f'Dani', DANI_MSGS, DANI_TYPING, a), tremble=2), vignette(0.45)],
         camera={'keyframes': [{'t': 0, 'zoom': 1.0}, {'t': round(b - a, 3), 'zoom': 1.06, 'ease': 'linear'}]}, sfx_note='message_pop x2')
    # --- S3 setup: away all week, six steps
    a, b = b, cut(W('L08', 5) - 0.05)
    t_home = W('L07', 12) - a
    t_six = W('L08', 1) - a
    shot('s04', a, b, 'Wide, the flat\'s corridor', 'Hallway (lights 1, endDoor) as the flat\'s corridor; label "HOME 10 PM" on "home", then "6 STEPS" between the two bedroom doors',
         [comp('horror/Hallway', {'lights': 1, 'endDoor': True, 'runner': True}, depth=0.4), vignette(0.5)],
         camera={'preset': 'pushIn', 'amount': 0.6},
         notes='callouts', sfx_note='sizzle (muffled) under')
    SHOTS[-1]['callouts'] = [{'style': 'label', 'text': 'AWAY ALL WEEK', 'at': 0.15, 'duration': round(t_home - 0.15, 3), 'y': '30%'},
                             {'style': 'label', 'text': 'HOME 10 PM', 'at': round(t_home, 3), 'duration': round(t_six - t_home, 3), 'y': '30%'},
                             {'style': 'banner', 'text': '6 STEPS', 'at': round(t_six, 3), 'y': '62%', 'color': '#ffffff', 'accent': RED}]
    # --- plant 1: the door that clicks twice
    a, b = b, cut(S('L10') - 0.08)
    l2 = CUE('latch2', 'L08') - a
    shot('s05', a, b, 'Close, Dani\'s door', 'her door (cooler colours), its lever dips twice exactly on the two latch clicks; "CLICK" "CLICK" labels; then still and dark on "hadn\'t clicked once"',
         [svg(door_svg(0.35, hue='#4f5a6e', hue2='#2c3342', wall='#1f2430'), depth=1),
          lever_layer(jolt(l2, -14) + jolt(l2 + 0.38, -14)[1:], close=False),
          darkness(0.55, 0.62, 0.52, 0.5), vignette(0.5)],
         camera={'keyframes': [{'t': 0, 'zoom': 1.15, 'x': 640, 'y': 1000}, {'t': round(b - a, 3), 'zoom': 1.35, 'x': 700, 'y': 1010, 'ease': 'linear'}]},
         sfx_note='latch2 (the signature sample) after "opens"')
    SHOTS[-1]['callouts'] = [{'style': 'label', 'text': 'CLICK', 'at': round(l2, 3), 'duration': 0.35, 'x': '74%', 'y': '44%', 'rotate': -6},
                             {'style': 'label', 'text': 'CLICK', 'at': round(l2 + 0.38, 3), 'duration': 0.4, 'x': '78%', 'y': '50%', 'rotate': 5}]
    # --- skeptic beat
    a, b = b, cut(S('L11') - 0.04)
    shot('s06', a, b, 'Close, Maya', 'Bedroom lamp 0.15; Maya suspicious, half a smirk: "I figured it was a prank."',
         [comp('horror/Bedroom', {'lamp': 0.15, 'phoneGlow': 0.8}, depth=0.2, blur=3),
          maya({'pose': 'phone', 'light': 'phone', 'lookX': 0.3, 'expr': 'suspicious'}, width=1350, height=2052), vignette(0.45)],
         camera={'preset': 'pushIn', 'amount': 0.3})
    a, b = b, cut(S('L13') - 0.06)
    shot('s07', a, b, 'Phone POV, DM "Dani"', 'Dani typing dots run WHILE the kitchen voice is mid-sentence; "she\'s lying to you" pops on "Hurry"',
         [svg(door_svg(0.9), blur=10, opacity=0.6, depth=0.3), handphone(chat('Dani', DANI_MSGS, DANI_TYPING, a), tremble=2), vignette(0.45)],
         camera={'keyframes': [{'t': 0, 'zoom': 1.0}, {'t': round(CUE('message_pop', 'L11') - a, 3), 'zoom': 1.04, 'ease': 'linear'},
                               {'t': round(CUE('message_pop', 'L11') - a + 0.03, 3), 'zoom': 1.2, 'x': '55%', 'y': '66%', 'ease': 'step'},
                               {'t': round(b - a, 3), 'zoom': 1.24, 'x': '55%', 'y': '66%', 'ease': 'linear'}],
                 'shake': [{'at': round(CUE('message_pop', 'L11') - a, 3), 'duration': 0.25, 'amplitude': 8}]},
         sfx_note='message_pop under the kitchen voice')
    # --- countable plant
    a, b = b, cut(S('L14') - 0.1)
    t2 = W('L13', 2) - a
    shot('s08', a, b, 'Top-down insert, the table', 'three plates set out under warm kitchen light; "3 PLATES" then "2 OF US" in red',
         [svg(plates_svg(), depth=1), vignette(0.5)], camera={'preset': 'pushIn', 'amount': 0.5})
    SHOTS[-1]['callouts'] = [{'style': 'banner', 'text': '3 PLATES', 'at': 0.05, 'duration': round(t2 - 0.05, 3), 'y': '30%'},
                             {'style': 'banner', 'text': '2 OF US', 'at': round(t2, 3), 'y': '30%', 'background': RED}]
    # --- rule one
    a, b = b, cut(S('L15') - 0.06)
    shot('s09', a, b, 'Phone POV, rule one', 'bubble "rule one. don\'t answer her." + neon card "RULE 1"',
         [svg(door_svg(0.9), blur=10, opacity=0.6, depth=0.3), handphone(chat('Dani', DANI_MSGS, DANI_TYPING, a), tremble=2),
          comp('horror/RedText', {'text': 'RULE 1', 'at': 0.05, 'duration': round(b - a - 0.05, 3), 'style': 'neon', 'fontSize': 96}, x='76%', y='22%', width=420, height=200, depth=0, z=40),
          vignette(0.45)])
    a, b = b, cut(S('L16') - 0.08)
    shot('s10', a, b, 'Medium, my door', 'my bedroom door from inside: a plain lever, no lock of any kind; label "NO LOCK"',
         [svg(door_svg(0.85), depth=1), lever_layer([{'t': 0, 'rotate': 0}], close=False), vignette(0.45)],
         camera={'keyframes': [{'t': 0, 'zoom': 1.25, 'x': 640, 'y': 1000}, {'t': round(b - a, 3), 'zoom': 1.32, 'x': 660, 'y': 1000, 'ease': 'linear'}]})
    SHOTS[-1]['callouts'] = [{'style': 'banner', 'text': 'NO LOCK', 'at': 0.1, 'y': '32%', 'background': RED}]
    # --- rule two + viewer proxy
    a, b = b, cut(S('L19') - 0.1)
    ins0, ins1 = W('L16', 7) - a - 0.1, W('L16', 7) - a + 0.75
    shot('s11', a, b, 'Phone POV, rule two + my question', 'bubble rule two + "RULE 2" card; 0.85 s insert of my lever with a white UP arrow on "hold it up"; my blue bubble "how do I know you\'re the real one?"; Dani: "because she wants you out there. i want you alive."',
         [svg(door_svg(0.9), blur=10, opacity=0.6, depth=0.3), handphone(chat('Dani', DANI_MSGS, DANI_TYPING, a), tremble=2),
          comp('horror/RedText', {'text': 'RULE 2', 'at': 0.05, 'duration': round(ins0 - 0.05, 3), 'style': 'neon', 'fontSize': 96}, x='76%', y='22%', width=420, height=200, depth=0, z=40),
          svg(lever_close_svg(), depth=0, z=45, start=round(ins0, 3), end=round(ins1, 3)),
          svg(lever_arm_svg(0), x=845, y=905, w=760, h=520, anchorX=660 / 760, anchorY=150 / 520, depth=0, z=46, start=round(ins0, 3), end=round(ins1, 3),
              keyframes=[{'t': round(ins0, 3), 'rotate': 0}, {'t': round(ins0 + 0.3, 3), 'rotate': 6, 'ease': 'out'}]),
          svg(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 300"><path d="M 100 10 L 180 120 L 130 120 L 130 290 L 70 290 L 70 120 L 20 120 Z" fill="#fff" stroke="{INK}" stroke-width="10"/></svg>',
              x='40%', y='38%', w=200, h=300, depth=0, z=47, start=round(ins0 + 0.1, 3), end=round(ins1, 3), enter={'type': 'pop', 'duration': 0.2}),
          vignette(0.45)],
         camera={'keyframes': [{'t': 0, 'zoom': 1.0}, {'t': round(S('L17') - a, 3), 'zoom': 1.03, 'ease': 'linear'},
                               {'t': round(S('L17') - a + 0.03, 3), 'zoom': 1.2, 'x': '55%', 'y': '70%', 'ease': 'step'},
                               {'t': round(b - a, 3), 'zoom': 1.24, 'x': '55%', 'y': '70%', 'ease': 'linear'}]},
         sfx_note='message_pop, message_send')
    # --- proximity rung 2: the sizzle stops
    a, b = b, cut(S('L20') - 0.06)
    shot('s12', a, b, 'Medium, my door', 'my door from inside, the warm strip under it; the kitchen sound cuts dead; a small "clink" label on the plate sound',
         [svg(door_svg(0.85), depth=1), lever_layer([{'t': 0, 'rotate': 0}], close=False), darkness(0.45, 0.5, 0.75, 0.6), vignette(0.5)],
         camera={'preset': 'pushIn', 'amount': 0.5}, sfx_note='sizzle stops dead on "stopped"; plate clink in the hall')
    SHOTS[-1]['callouts'] = [{'style': 'label', 'text': 'clink', 'at': round(CUE('plate', 'L19') - a, 3), 'duration': 0.6, 'x': '30%', 'y': '80%', 'rotate': -4}]
    # --- exit closed: 911, and the texter's tell
    a, b = b, cut(S('L21') - 0.06)
    shot('s13', a, b, 'Close, Maya dialing', 'Maya, phone lit under her face, thumb on the keypad; big red "911" label (no call screen: the kit only draws an incoming call)',
         [comp('horror/Bedroom', {'lamp': 0.1, 'phoneGlow': 1.0}, depth=0.2, blur=4),
          maya({'pose': 'phone', 'light': 'phone', 'lookX': 0.0, 'lookY': 0.4, 'expr': 'scared'}, width=1350, height=2052), vignette(0.5)],
         camera={'preset': 'pushIn', 'amount': 0.5})
    SHOTS[-1]['callouts'] = [{'style': 'banner', 'text': '9 1 1', 'at': round(W('L20', 3) - a, 3), 'x': '72%', 'y': '58%', 'background': RED}]
    a, b = b, cut(CUE('floor_creak', 'L21') - 0.08)
    shot('s14', a, b, 'Phone POV, DM "Dani"', 'Dani was already typing as I dialed; "don\'t. she\'s outside your door." lands BEFORE any sound from the hall',
         [svg(door_svg(0.85), blur=10, opacity=0.6, depth=0.3), handphone(chat('Dani', DANI_MSGS, DANI_TYPING, a), tremble=3), vignette(0.5)],
         camera={'keyframes': [{'t': 0, 'zoom': 1.2, 'x': '55%', 'y': '70%'}, {'t': round(b - a, 3), 'zoom': 1.26, 'x': '55%', 'y': '70%', 'ease': 'linear'}]})
    a, b = b, cut(S('L23') - 0.08)
    shot('s15', a, b, 'Medium, my door', 'the floor creaks; two foot shadows step into the strip under my door and stop',
         [svg(door_svg(0.85), depth=1), lever_layer([{'t': 0, 'rotate': 0}], close=False),
          svg(feet_svg(1), depth=1, z=3, keyframes=[{'t': 0.0, 'opacity': 0}, {'t': 0.25, 'opacity': 1, 'ease': 'out'}]),
          darkness(0.55, 0.5, 0.8, 0.55), vignette(0.55)],
         camera={'preset': 'pushIn', 'amount': 0.6}, sfx_note='floor_creak')
    # --- S6 turn
    a, b = b, cut(S('L24') - 0.08)
    t = S('L23') - a
    shot('s16', a, b, 'Close, my door (the turn)', '"Is she texting you, Maya?" right behind the door: the only full-frame red flash (Glitch + red Vignette 0.4 s), shake on the impact',
         [svg(door_svg(0.85), depth=1), lever_layer([{'t': 0, 'rotate': 0}], close=False), svg(feet_svg(1), depth=1, z=3),
          comp('horror/Glitch', {'cues': [{'at': round(t, 3), 'duration': 0.25, 'amount': 0.8}]}, depth=0, z=70),
          comp('horror/Vignette', {'amount': 0.95, 'color': '190,20,30'}, depth=0, z=65, start=round(t, 3), end=round(t + 0.4, 3)),
          darkness(0.6, 0.5, 0.7, 0.5), vignette(0.55)],
         camera={'keyframes': [{'t': 0, 'zoom': 1.15, 'x': 540, 'y': 1150}, {'t': round(b - a, 3), 'zoom': 1.35, 'x': 540, 'y': 1150, 'ease': 'linear'}],
                 'shake': [{'at': round(t, 3), 'duration': 0.3, 'amplitude': 16}]}, sfx_note='impact; DOOR voice dry and close')
    # --- S7 panic ladder
    a, b = b, cut(S('L25') - 0.06)
    tj = CUE('jolt_a', 'L24') - a
    shot('s17', a, b, 'Extreme close, my lever', 'my lever tips down on its own (the handle test)',
         [svg(lever_close_svg(), depth=1), lever_layer(rot(tj, 0, tj + 0.35, -16), hands=0), vignette(0.55)],
         camera={'preset': 'pushIn', 'amount': 0.4, 'shake': [{'at': round(tj, 3), 'duration': 0.25, 'amplitude': 10}]}, sfx_note='jolt')
    a, b = b, cut(S('L26') - 0.06)
    shot('s18', a, b, 'Phone POV, CAPS', 'CAPS bubbles "HOLD IT UP", "MAYA HOLD IT"; phone vibrates and trembles; heartbeat edges start',
         [handphone(chat('Dani', DANI_MSGS, DANI_TYPING, a), tremble=8, vibrate=[{'at': 0.0, 'duration': 0.9, 'amount': 1}]),
          comp('horror/Heartbeat', {'bpm': 96, 'bpmTo': 120, 'intensity': 0.6}, depth=0, z=58), vignette(0.5)],
         camera={'preset': 'none', 'shake': [{'at': 0.02, 'duration': 0.2, 'amplitude': 8}, {'at': 0.57, 'duration': 0.2, 'amplitude': 8}]},
         sfx_note='phone_buzz')
    a, b = b, cut(S('L27') - 0.08)
    j1, j2 = CUE('jolt_b', 'L26') - a, CUE('jolt_c', 'L26') - a
    shot('s19', a, b, 'Extreme close, both hands on the lever', 'both my hands hold the lever up; it is forced down against them on "Once." and "Twice."',
         [svg(lever_close_svg(), depth=1), lever_layer([{'t': 0, 'rotate': -16}, {'t': 0.3, 'rotate': 0, 'ease': 'out'}] + jolt(j1, -10) + jolt(j2, -12), hands=2),
          comp('horror/Heartbeat', {'bpm': 110, 'bpmTo': 130, 'intensity': 0.6}, depth=0, z=58), vignette(0.55)],
         camera={'preset': 'pushIn', 'amount': 0.3, 'shake': [{'at': round(j1, 3), 'duration': 0.22, 'amplitude': 12}, {'at': round(j2, 3), 'duration': 0.22, 'amplitude': 14}]},
         sfx_note='jolt x2 on the words')
    # --- B8 rival claim + rule inversion
    a, b = b, cut(S('L28') - 0.08)
    shot('s20', a, b, 'Low medium, my door', 'the door, feet in the strip; her voice pleads: "It\'s me. The one in my room is the copy."',
         [svg(door_svg(0.85), depth=1), lever_layer([{'t': 0, 'rotate': 0}], close=False), svg(feet_svg(1), depth=1, z=3),
          comp('horror/Heartbeat', {'bpm': 120, 'intensity': 0.5}, depth=0, z=58), darkness(0.55, 0.5, 0.75, 0.55), vignette(0.55)],
         camera={'keyframes': [{'t': 0, 'zoom': 1.1, 'x': 540, 'y': 1300}, {'t': round(b - a, 3), 'zoom': 1.22, 'x': 540, 'y': 1350, 'ease': 'linear'}]})
    a, b = b, cut(S('L29') - 0.08)
    shot('s21', a, b, 'Close, Maya against the door', 'Maya (pose idle, holding on, frame-edge hands implied) terrified -> suspicious on "so you can\'t leave" (the rule inverted)',
         [svg(door_svg(0.85), blur=6, depth=0.3),
          maya({'pose': 'idle', 'lookX': -0.5, 'exprs': [{'t': 0, 'e': 'terrified'}, {'t': round(W('L28', 6) - a, 3), 'e': 'suspicious'}]}, width=1350, height=2052),
          darkness(0.5, 0.5, 0.45, 0.5), comp('horror/Heartbeat', {'bpm': 124, 'intensity': 0.5}, depth=0, z=58), vignette(0.55)],
         camera={'preset': 'pushIn', 'amount': 0.4})
    # --- barrier rung: the napkin
    a, b = b, cut(S('L30') - 0.08)
    tw = CUE('whoosh', 'L29') - a
    shot('s22', a, b, 'Low close, the gap under my door', 'a white napkin slides out from under the door between her two foot shadows',
         [svg(gap_svg(), depth=1),
          svg(NAPKIN, x='50%', y=1080, w=420, h=300, z=4, keyframes=[{'t': 0, 'y': 1060, 'scale': 0.6, 'opacity': 0}, {'t': round(tw, 3), 'y': 1070, 'scale': 0.6, 'opacity': 1, 'ease': 'step'},
                                                                   {'t': round(tw + 0.6, 3), 'y': 1300, 'scale': 1.25, 'opacity': 1, 'ease': 'out'}]),
          vignette(0.55)],
         camera={'preset': 'pushIn', 'amount': 0.3}, sfx_note='whoosh at -8 dB (paper slide)')
    a, b = b, cut(S('L31') - 0.08)
    shot('s23', a, b, 'Insert, the napkin', 'the napkin up close; her handwriting appears: "still sorry about your cactus"',
         [svg(NAPKIN_CLOSE, depth=1),
          comp('horror/RedText', {'text': 'still sorry about your cactus', 'at': 0.05, 'style': 'scrawl', 'fontSize': 84, 'color': '#2b2b3a', 'shake': 0, 'cps': 26, 'maxWidth': 0.8},
               x='52%', y='50%', width=1000, height=800, depth=1, z=5, rotate=-3),
          vignette(0.45)],
         camera={'preset': 'pushIn', 'amount': 0.3})
    # --- B10 lifeline under a physical clock (the handle)
    a, b = b, cut(S('L33') - 0.06)
    tj = CUE('jolt_a', 'L32') - a
    shot('s24', a, b, 'Phone POV, "Dani\'s Mom" thread', 'the thread with Dani\'s mom (one old, harmless message from her); a 0.7 s insert of my lever dipping the instant I let go, then my left hand shoving it back up',
         [svg(door_svg(0.85), blur=10, opacity=0.6, depth=0.3), handphone(chat("Dani's Mom", MOM_MSGS, MOM_TYPING, a), tremble=3, side='right'),
          svg(lever_close_svg(), depth=0, z=45, start=round(tj - 0.1, 3), end=round(tj + 0.75, 3)),
          svg(lever_arm_svg(1), x=845, y=905, w=760, h=520, anchorX=660 / 760, anchorY=150 / 520, depth=0, z=46, start=round(tj - 0.1, 3), end=round(tj + 0.75, 3),
              keyframes=[{'t': round(tj - 0.1, 3), 'rotate': 0}, {'t': round(tj + 0.1, 3), 'rotate': -18, 'ease': 'out'}, {'t': round(tj + 0.55, 3), 'rotate': 0, 'ease': 'backOut'}]),
          vignette(0.45)],
         camera={'keyframes': [{'t': 0, 'zoom': 1.0}, {'t': round(b - a, 3), 'zoom': 1.05, 'ease': 'linear'}], 'shake': [{'at': round(tj, 3), 'duration': 0.25, 'amplitude': 12}]},
         sfx_note='jolt on "dipped"')
    a, b = b, cut(S('L36') - 0.1)
    tg = CUE('stinger', 'L35') - a
    shot('s25', a, b, 'Phone POV, the outside check', 'my bubble "is Dani with you?" sends; typing; Mom: "Maya? Dani\'s been home with us since Sunday." / "She\'s asleep down the hall. I just checked."; glitch on the last bubble',
         [svg(door_svg(0.85), blur=10, opacity=0.6, depth=0.3), handphone(chat("Dani's Mom", MOM_MSGS, MOM_TYPING, a), tremble=3),
          comp('horror/Glitch', {'cues': [{'at': round(tg, 3), 'duration': 0.3, 'amount': 0.6}]}, depth=0, z=70), vignette(0.5)],
         camera={'keyframes': [{'t': 0, 'zoom': 1.2, 'x': '55%', 'y': '70%'}, {'t': round(S('L34') - a, 3), 'zoom': 1.22, 'x': '55%', 'y': '70%', 'ease': 'linear'},
                               {'t': round(S('L34') - a + 0.03, 3), 'zoom': 1.3, 'x': '55%', 'y': '70%', 'ease': 'step'}, {'t': round(b - a, 3), 'zoom': 1.36, 'x': '55%', 'y': '70%', 'ease': 'linear'}]},
         sfx_note='message_send, typing, message_pop x2, stinger -3 dB')
    # --- S8 silence beat
    a, b = b, cut(S('B01') - 0.04)
    shot('s26', a, b, 'Close, Maya', 'Maya pose cover, terrified, no blinking; "The handle went slack. Outside, nothing."',
         [comp('horror/Bedroom', {'lamp': 0.05}, depth=0.2, blur=4), maya({'pose': 'cover', 'expr': 'terrified', 'blink': False}, width=1350, height=2052),
          darkness(0.9, 0.5, 0.45, 0.35), vignette(0.6)],
         camera={'preset': 'none'}, sfx_note='music hushes to near silence')
    a, b = b, cut(S('L37') - 0.03)
    shot('s27', a, b, 'Phone POV, DM "Dani" (silence)', '3.3 s with no voice: my bubbles "where are you", then "WHO ARE YOU", then Dani\'s typing dots',
         [handphone(chat('Dani', DANI_MSGS, DANI_TYPING, a), tremble=1), darkness(0.5, 0.53, 0.55, 0.6), vignette(0.6)],
         camera={'keyframes': [{'t': 0, 'zoom': 1.2, 'x': '55%', 'y': '70%'}, {'t': round(b - a, 3), 'zoom': 1.28, 'x': '55%', 'y': '70%', 'ease': 'linear'}]},
         sfx_note='message_send x2 at -4 dB, nothing else')
    # --- S9 proof: the only image
    a, b = b, cut(S('B05') - 0.02)
    shot('s28', a, b, 'Photo insert (the only image), held still', 'greyscale photo card (white border, 2 deg tilt) over the blurred thread: taken from inside Dani\'s dark room, through her doorway, across the flat to MY door; someone stands at it, backlit by the strip',
         [handphone(chat('Dani', DANI_MSGS, DANI_TYPING, a), tremble=0, layer={'opacity': 0.5, 'blur': 8}),
          svg(photo_svg(), x='50%', y='47%', w=900, h=1200, rotate=2, depth=0, z=30, enter={'type': 'pop', 'duration': 0.25}, shadow='0 30px 60px rgba(0,0,0,.6)'),
          vignette(0.55)],
         camera={'preset': 'none'}, sfx_note='message_pop; held still 3.9 s')
    # --- S10 plant payoff
    a, b = b, cut(S('B06') - 0.04)
    shot('s29', a, b, 'Close, Maya', 'no narration: the two latch clicks (the plant\'s exact sample) into silence; Maya\'s eyes snap toward the sound',
         [comp('horror/Bedroom', {'lamp': 0.05}, depth=0.2, blur=4),
          maya({'pose': 'cover', 'exprs': [{'t': 0, 'e': 'terrified'}, {'t': 0.05, 'e': 'shocked'}], 'lookX': -0.9, 'blink': False}, width=1350, height=2052),
          darkness(0.9, 0.5, 0.45, 0.35), vignette(0.6)],
         camera={'keyframes': [{'t': 0, 'zoom': 1.0}, {'t': 0.06, 'zoom': 1.12, 'ease': 'step'}, {'t': round(b - a, 3), 'zoom': 1.15, 'ease': 'linear'}]},
         sfx_note='latch2 (same file as s05)')
    a, b = b, cut(S('L40') - 0.1)
    st = [round(0.05 + k * 2.1 / 5, 3) for k in range(6)]
    shot('s30', a, b, 'Medium, my door (six steps)', 'six footsteps cross the flat; a second pair of foot shadows joins the first in the strip on the last step; "Six steps."',
         [svg(door_svg(0.85), depth=1), lever_layer([{'t': 0, 'rotate': 0}], close=False),
          svg(feet_svg(1), depth=1, z=3, keyframes=[{'t': 0, 'opacity': 1}, {'t': st[-1], 'opacity': 1}, {'t': st[-1] + 0.2, 'opacity': 0, 'ease': 'out'}]),
          svg(feet_svg(2), depth=1, z=3, keyframes=[{'t': 0, 'opacity': 0}, {'t': st[-1], 'opacity': 0}, {'t': st[-1] + 0.2, 'opacity': 1, 'ease': 'out'}]),
          darkness(0.6, 0.5, 0.75, 0.5), vignette(0.6)],
         camera={'keyframes': [{'t': 0, 'zoom': 1.0, 'x': 540, 'y': 1250}] + [{'t': s, 'zoom': round(1.0 + 0.04 * (k + 1), 3), 'x': 540, 'y': 1250, 'ease': 'out'} for k, s in enumerate(st)]},
         sfx_note='steps6 (getting closer)')
    SHOTS[-1]['callouts'] = [{'style': 'label', 'text': f'{k + 1}', 'at': s, 'duration': 0.32, 'x': f'{20 + k * 12}%', 'y': '22%'} for k, s in enumerate(st)]
    a, b = b, cut(S('L41') - 0.08)
    th = CUE('handle_turn', 'L40') - a
    shot('s31', a, b, 'Extreme close, my hand on the lever', 'my one hand holding it up; the lever turns slowly down under it anyway, then stops dead halfway',
         [svg(lever_close_svg(), depth=1), lever_layer([{'t': 0, 'rotate': 0}, {'t': round(th, 3), 'rotate': 0}, {'t': round(th + 1.25, 3), 'rotate': -24, 'ease': 'inOut'}], hands=1),
          vignette(0.6)],
         camera={'preset': 'pushIn', 'amount': 0.5}, sfx_note='handle_turn (slow squeak + ratchet), cut dead')
    # --- bookend: lock screen, calm sentence case
    a, b = b, END
    shot('s32', a, b, 'Phone POV, lock screen (bookend of s01)', 'lock screen again, 11:52; calm banners "Rule three, Maya." / "Dinner is for three. Come out."; behind the phone my door, now with FOUR foot shadows in the strip; hard cut to black',
         [svg(door_svg(0.9), blur=9, opacity=0.85, depth=0.3), svg(feet_svg(2), blur=9, opacity=0.85, depth=0.3),
          handphone(mode='lock', lock={'time': '11:52', 'date': 'Thursday', 'notifications': [
              {'at': round(S('L41') - a, 3), 'app': 'Messages', 'title': 'Dani', 'text': 'Rule three, Maya.'},
              {'at': round(S('L42') - a, 3), 'app': 'Messages', 'title': 'Dani', 'text': 'Dinner is for three. Come out.'}]}, tremble=0.5),
          vignette(0.55)],
         camera={'preset': 'pushIn', 'amount': 0.5}, sfx_note='notify x2 at -4 dB; audio and picture cut together')


def caption_words():
    EMPH = {'kitchen.', 'nine.', 'away', 'six', 'twice', 'once', 'prank.', 'three', 'plates!', 'plates.', 'two', "doesn't", 'lock.', 'stopped.', '911',
            'creaked.', 'texting', 'Once.', 'Twice.', 'copy.', "can't", 'leave.', 'cactus.', 'Dani', 'dipped.', 'slack.', 'nothing.', 'photo.', 'Someone',
            'Six', 'turn.'}
    out = []
    for w in WORDS:
        d = {'text': w['text'], 'start': w['start'], 'end': w['end']}
        if w['text'] in EMPH:
            d['emph'] = True
        out.append(d)
    return out


def storyboard():
    build()
    scenes = []
    for sh in SHOTS:
        sc = {'id': sh['id'], 'duration': round(sh['end'] - sh['start'], 3), 'background': {'type': 'color', 'color': '#0b0d12'},
              'layers': sh['layers'], 'notes': f"{sh['kind']}: {sh['desc']}"}
        if sh.get('camera'):
            sc['camera'] = sh['camera']
        if sh.get('callouts'):
            sc['callouts'] = sh['callouts']
        scenes.append(sc)
    total = sum(s['duration'] for s in scenes)
    assert abs(total - END) < 0.02, (total, END)
    return {
        'version': 1, 'id': SLUG, 'title': "My Roommate Texted Me: Don't Come Out", 'format': '9:16', 'fps': 30,
        'scenes': scenes,
        'captions': {'words': caption_words(), 'maxWords': 4, 'maxChars': 18, 'gapBreak': 0.3,
                     'glue': ['three plates', 'two of us', 'six steps', 'both hands'],
                     'style': {'font': 'display', 'fontSize': 62, 'color': '#ffffff', 'highlight': RED, 'highlightMode': 'none', 'strokeWidth': 10,
                               'uppercase': False, 'y': 0.12, 'backing': 0.85}},
        'audio': {'voice': [{'src': f'episodes/{SLUG}/mix.wav', 'start': 0, 'volume': 1, 'duration': REPORT['duration_s']}],
                  'music': [], 'sfx': [], 'duckOn': 'none'},
        'overlays': {'grain': 0.5, 'vignette': 0.3, 'fadeIn': 0, 'fadeOut': 0},
        '_built': {'by': f'backlog/horror/{SLUG}/gen_storyboard.py', 'timing': 'audio/lines.json (gen_audio.py, Kokoro on the Spark CPU)',
                   'audio': f'studio/public/episodes/{SLUG}/mix.wav (Spark only; rebuild with gen_audio.py)'},
    }


def fmt(t):
    return f"{int(t // 60)}:{t % 60:04.1f}"


if __name__ == '__main__':
    sb = storyboard()
    json.dump(sb, open(os.path.join(HERE, 'storyboard.json'), 'w'), indent=1)
    print(f"storyboard.json: {len(sb['scenes'])} scenes, {sum(s['duration'] for s in sb['scenes']):.2f} s, {len(sb['captions']['words'])} caption words")
    if '--table' in sys.argv:
        for i, sh in enumerate(SHOTS, 1):
            print(f"| {i} | {fmt(sh['start'])} | {fmt(sh['end'])} | {sh['kind']} | {sh['desc']} | {sh['sfx'] or '-'} |")
