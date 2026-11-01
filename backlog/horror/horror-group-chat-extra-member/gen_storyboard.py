"""Build storyboard.json for backlog/horror/horror-group-chat-extra-member from the final Kokoro stamps.

All prop / keyframe / layer times are converted to scene-local seconds (kit rule).
Usage: python3 gen_sb.py <episode_dir>
"""
import json
import sys

EP = sys.argv[1]
ID = 'horror-group-chat-extra-member'
cap = json.load(open(f'{EP}/audio/captions.json'))['words']
aud = json.load(open(f'{EP}/audio/audio.storyboard.json'))
TOTAL = round(aud['duration_s'], 3)

# ------------------------------------------------------------------ cast / constants
MEMBERS = {
    'Night Security': {'color': '#4b5563', 'initials': '🛡️'},
    'Leo · 7C': {'color': '#4a628f', 'initials': 'L'},
    'Ama · 3D': {'color': '#7a5c8f', 'initials': 'A'},
    'Dana · 9D': {'color': '#4f7a73', 'initials': 'D'},
    'Mrs. Petrov · 1A · admin': {'color': '#8f6a4a', 'initials': 'P'},
    'Mr. Okafor': {'color': '#3e5872', 'initials': 'O'},
}
OKAFOR = {'hair': '#1b1716', 'skin': '#7a4e33', 'top': '#3e5872', 'topShade': '#2c3f52', 'shirt': '#d9d2c3'}
HAND = {'phoneWidth': 0.68, 'cx': 0.53, 'cy': 0.61, 'tilt': -3, 'tremble': 1.5, 'side': 'right', 'thumbY': 0.94, 'thumbReach': 0.1}
PUNCH = {'zoom': 1.22, 'x': '55.60%', 'y': '77.80%'}  # newest-bubble punch-in (pilot framing)

NS = 'Night Security'
# group chat, global times
GROUP = [
    {'from': 'Dana · 9D', 'text': "anyone else's radiator banging", 'at': -40.0},
    {'from': 'Leo · 7C', 'text': 'every night lol', 'at': -39.0},
    {'from': 'Ama · 3D', 'text': "someone's in the hall??", 'at': -6.0},
    {'from': NS, 'text': 'Nobody. Go back to bed, 3D.', 'at': -5.0},
    {'from': 'Leo · 7C', 'text': "who's in the hallway?", 'at': 3.3},
    {'from': NS, 'text': 'One. Delivery for 7A. Leaving now.', 'at': 4.21},
    {'me': True, 'text': "who's in the hallway?", 'at': 14.0},
    {'from': NS, 'text': 'One. Mr. Okafor, next door. Taking out recycling.', 'at': 15.59},
    {'me': True, 'text': 'who actually runs night security??', 'at': 25.9},
    {'from': 'Dana · 9D', 'text': 'leave it alone it found my cat 🐈', 'at': 27.09},
    {'from': 'Mrs. Petrov · 1A · admin', 'text': 'Landlord says that account joined 2 days before this chat existed. Removing it.', 'at': 29.25},
    {'kind': 'system', 'text': 'Night Security removed Mrs. Petrov (1A)', 'at': 34.33},
    {'from': NS, 'text': "Who's in the hallway? One. Floor 8, by the stairs. Me.", 'at': 41.64},
    {'from': NS, 'text': 'Floor 7.', 'at': 44.44},
    {'from': NS, 'text': 'Floor 6.', 'at': 45.77},
    {'from': NS, 'text': 'Floor 5.', 'at': 48.34},
    {'from': NS, 'text': 'Door check. 5B. 20 seconds.', 'kind': 'alert', 'at': 61.28},
    {'from': 'Dana · 9D', 'text': 'just open it 5B its never wrong', 'at': 63.31},
    {'from': 'Leo · 7C', 'text': 'open it', 'at': 65.41},
    {'from': 'Ama · 3D', 'text': 'open it 5B', 'at': 65.95},
    {'me': True, 'text': "who's in 5B?", 'at': 77.28},
    {'from': NS, 'text': 'Two.', 'at': 78.42},
]
GROUP_TYPING = [{'from': 'Mrs. Petrov · 1A · admin', 'at': 28.5, 'until': 29.25}]
DM_NS = [
    {'from': NS, 'text': 'You looked, 5B.', 'at': 24.04},
    {'from': NS, 'text': 'So did 2C.', 'at': 24.84},
    {'from': NS, 'text': 'Step back from the peephole, 5B.', 'at': 58.24},
]
DM_OK = [
    {'from': 'Mr. Okafor', 'text': 'parcel for you at the front desk 📦', 'at': -300.0},
    {'me': True, 'text': 'got it thank you!!', 'at': -299.0},
    {'kind': 'system', 'text': 'Night Security is in this chat', 'at': 67.75},
    {'me': True, 'text': 'was that you at my door??', 'at': 69.32},
    {'from': 'Mr. Okafor', 'text': 'ive been asleep since 9. what night security?? nobodys posted in our chat since friday', 'at': 71.89},
]
SEARCH = [
    {'from': NS, 'text': 'Nobody. The boiler.', 'at': -9}, {'from': NS, 'text': 'One. 8A, locked out.', 'at': -8},
    {'from': NS, 'text': 'Two. Delivery, 6B and 6C.', 'at': -7}, {'from': NS, 'text': 'Nobody. Wind in the stairwell.', 'at': -6},
    {'from': NS, 'text': "One. 4D's dog walker.", 'at': -5}, {'from': NS, 'text': "Three. 1A's grandchildren.", 'at': -4},
    {'from': NS, 'text': 'Nobody.', 'at': -3}, {'from': NS, 'text': 'One. 7A, night shift.', 'at': 0.4},
    {'from': NS, 'text': 'One. Outside 2C.', 'at': 1.6},
]


def local(msgs, t0, keep=9):
    out = [dict(m, at=round(m['at'] - t0, 3)) for m in msgs]
    past = [m for m in out if m['at'] <= 0]
    fut = [m for m in out if m['at'] > 0]
    return past[-keep:] + fut


def clock(t):
    return '1:12' if t < 18 else '1:13' if t < 40 else '1:14' if t < 60 else '1:15'


def chat_group(t0, dur, **kw):
    c = {'title': 'Larkspur Court Residents', 'subtitle': '38 members', 'dayLabel': 'Today 1:02 AM', 'accent': '#3d5a80',
         'clock': clock(t0), 'battery': 23, 'theme': 'dark', 'scale': 1.25,
         'messages': [m for m in local(GROUP, t0) if m['at'] <= dur + 0.01]}
    ty = [dict(y, at=round(y['at'] - t0, 3), until=round(y['until'] - t0, 3)) for y in GROUP_TYPING if y['until'] > t0 and y['at'] < t0 + dur]
    if ty:
        c['typing'] = ty
    c.update(kw)
    return c


def chat_dm(name, msgs, t0, dur, **kw):
    c = {'dm': name, 'title': name, 'subtitle': 'private chat', 'accent': '#3d5a80', 'clock': clock(t0), 'battery': 23,
         'theme': 'dark', 'scale': 1.25, 'messages': [m for m in local(msgs, t0) if m['at'] <= dur + 0.01]}
    c.update(kw)
    return c


def hand(chat=None, phone_extra=None, **kw):
    phone = {'members': MEMBERS, 'mode': 'chat'}
    if chat is not None:
        phone['chat'] = chat
    if phone_extra:
        phone.update(phone_extra)
    p = dict(HAND)
    p.update(kw)
    p['phone'] = phone
    return {'type': 'component', 'name': 'horror/HandPhone', 'props': p}


def comp(name, props=None, **kw):
    d = {'type': 'component', 'name': name, 'props': props or {}}
    d.update(kw)
    return d


def full(name, props=None, **kw):
    return comp(name, props, **kw)


def door_layer(blur=8, opacity=0.75, **props):
    p = {'hallLight': 0.9, 'chain': 'on', 'feet': False}
    p.update(props)
    return comp('horror/FrontDoor', p, depth=0.2, blur=blur, opacity=opacity)


def living_layer():
    return comp('horror/LivingRoom', {'lamp': 0.2, 'tv': 'off'}, depth=0.2, blur=8, opacity=0.8)


VIGNETTE = comp('horror/Vignette', {'amount': 0.4}, depth=0, z=50)


def push(dur, a=1.0, b=1.04, x='50%', y='50%'):
    return {'keyframes': [{'t': 0, 'zoom': a, 'x': x, 'y': y, 'ease': 'linear'}, {'t': round(dur, 3), 'zoom': b, 'x': x, 'y': y, 'ease': 'linear'}]}


def pt1():
    return {'type': 'text', 'text': 'PT 1', 'fontSize': 34, 'font': 'display', 'weight': 900, 'color': '#ffffff',
            'background': '#c0202b', 'padding': 10, 'radius': 8, 'x': 135, 'y': 1440, 'depth': 0, 'z': 95}


CHIP_T0 = 62.48  # "seconds." -> the 20 s door check starts


def chip_layers(t0, dur):
    """Countdown chip as one text layer per second (scene-local start/end)."""
    out = []
    for k in range(0, 21):
        a, b = CHIP_T0 + k, CHIP_T0 + k + 1
        if b <= t0 or a >= t0 + dur:
            continue
        out.append({'type': 'text', 'text': f'DOOR CHECK 0:{20 - k:02d}', 'fontSize': 40, 'font': 'display', 'weight': 900,
                    'color': '#ffffff', 'background': '#c0202b', 'padding': 12, 'radius': 12, 'x': '50%', 'y': 372,
                    'depth': 0, 'z': 92, 'start': round(max(0, a - t0), 3), 'end': round(min(dur, b - t0), 3)})
    return out


scenes = []


def scene(sid, t0, t1, layers, camera=None, transition=None, callouts=None, notes=None, bg='#0b0d12'):
    dur = round(t1 - t0, 3)
    s = {'id': sid, 'duration': dur, 'background': {'type': 'color', 'color': bg}, 'layers': layers + chip_layers(t0, dur) + [pt1()]}
    if camera:
        s['camera'] = camera
    if transition:
        s['transitionIn'] = transition
    if callouts:
        s['callouts'] = callouts
    if notes:
        s['notes'] = notes
    scenes.append(s)
    return dur


# ------------------------------------------------------------------ scenes (global times from audio/captions.json)
t0, t1 = 0.0, 6.15
cam = push(5.45, 1.0, 1.03)
cam['keyframes'] += [{'t': 5.49, **PUNCH, 'ease': 'step'}, {'t': 6.15, 'zoom': 1.25, 'x': PUNCH['x'], 'y': PUNCH['y'], 'ease': 'linear'}]
scene('s01_cover_hook', t0, t1, [
    door_layer(),
    hand(chat_group(t0, t1 - t0)),
    VIGNETTE,
    comp('horror/RedText', {'text': 'we have no\nnight security', 'style': 'scrawl', 'at': -0.3, 'duration': 6.6, 'fontSize': 80, 'shake': 0, 'y': 0.205}, depth=0, z=70),
], camera=cam, notes='Frame 0 = cover: phone over her own front door (hall light under it), newest bubble "Nobody. Go back to bed, 3D.", red scrawl.')

t0, t1 = 6.15, 8.35
scene('s02_profile_bio', t0, t1, [
    door_layer(),
    hand(chat_group(t0, t1 - t0, title='Night Security', subtitle='Unit: — · Joined Mar 1',
                    pinned={'label': 'BIO', 'text': 'Ask me.\nNever use your peephole.', 'lines': 2, 'at': 0.3})),
    VIGNETTE,
], camera=push(t1 - t0, 1.0, 1.03))

t0, t1 = 8.35, 10.87
scene('s03_empty_2c', t0, t1, [
    full('horror/Hallway', {'lights': 1, 'figure': 0, 'runner': True, 'endDoor': True, 'flicker': 0.1}),
    {'type': 'rect', 'x': '22%', 'y': '44%', 'width': 120, 'height': 64, 'fill': '#c9b98f', 'stroke': '#2a2410', 'strokeWidth': 4, 'radius': 6},
    {'type': 'text', 'text': '2C', 'x': '22%', 'y': '44%', 'fontSize': 44, 'color': '#2a2410', 'weight': 900},
    comp('horror/Flicker', {'strength': 0.1}, depth=0, z=60),
    VIGNETTE,
], camera=push(t1 - t0, 1.0, 1.06), transition={'type': 'dipBlack', 'duration': 0.25})

t0, t1 = 10.87, 13.85
scene('s04_barrier', t0, t1, [
    full('horror/FrontDoor', {'chain': 'on', 'hallLight': 1.0, 'feet': [round(12.2 - t0, 3), round(t1 - t0 + 1, 3)]}),
    comp('horror/Darkness', {'x': 0.5, 'y': 0.7, 'radius': 0.55, 'darkness': 0.6}, depth=0, z=45),
    VIGNETTE,
], camera=push(t1 - t0, 1.0, 1.06), callouts=[{'style': 'label', 'text': '5B', 'at': round(13.43 - t0, 3), 'x': '50%', 'y': '30%'}])

t0, t1 = 13.85, 18.4
scene('s05_ritual', t0, t1, [
    door_layer(feet=True),
    hand(chat_group(t0, t1 - t0), taps=[{'at': round(13.95 - t0, 3), 'x': 0.82, 'y': 0.9}]),
    VIGNETTE,
], camera=push(t1 - t0, 1.0, 1.05))

t0, t1 = 18.4, 19.12
scene('s06_nora_rule', t0, t1, [
    comp('horror/FrontDoor', {'chain': 'on', 'hallLight': 1.0, 'feet': True}, blur=4),
    comp('horror/Protagonist', {'pose': 'idle', 'expr': 'suspicious', 'lookX': 0.5, 'light': 'none'}, x='40%', y='100%', anchorY=1, width=1450, height=2204),
    VIGNETTE,
], camera=push(t1 - t0, 1.0, 1.08))

t0, t1 = 19.12, 22.0
scene('s07_peephole_okafor', t0, t1, [
    full('horror/Peephole', {'figure': 'neighbour', 'expr': 'blank', 'blink': False, 'colors': OKAFOR, 'lookX': 0, 'lookY': 0,
                             'lean': 0.45, 'flicker': 0.1, 'radius': 0.52, 'exposure': 1.2, 'surround': '#050506'}),
], camera=push(t1 - t0, 1.0, 1.04), transition={'type': 'dipBlack', 'duration': 0.2})

t0, t1 = 22.0, 22.82
scene('s08_peephole_empty', t0, t1, [
    full('horror/Peephole', {'figure': 'none', 'flicker': 0.2, 'radius': 0.52, 'exposure': 1.2, 'surround': '#050506'}),
])

t0, t1 = 22.82, 25.8
scene('s09_dm_you_looked', t0, t1, [
    door_layer(feet=False),
    hand(chat_dm(NS, DM_NS, t0, t1 - t0, subtitle='private chat'),
         phone_extra={'screens': [{'t': 0, 'mode': 'lock'}, {'t': 0.9, 'mode': 'chat'}],
                      'lock': {'time': '1:13', 'date': 'Sunday, November 1', 'notifications': [{'at': 0.45, 'app': 'Residents', 'title': NS, 'text': 'private message'}]},
                      'vibrate': [{'at': 0.45, 'duration': 0.4}]},
         glitch=[{'at': round(25.3 - t0, 3), 'duration': 0.2, 'amount': 0.8}]),
    VIGNETTE,
], camera={'keyframes': push(t1 - t0, 1.0, 1.05)['keyframes'], 'shake': [{'at': round(25.3 - t0, 3), 'duration': 0.2, 'amplitude': 12}]})

t0, t1 = 25.8, 33.63
scene('s10_chorus_admin', t0, t1, [
    living_layer(),
    hand(chat_group(t0, t1 - t0)),
    VIGNETTE,
], camera={'keyframes': [{'t': 0, 'zoom': 1.0, 'x': '50%', 'y': '50%', 'ease': 'linear'}, {'t': round(29.25 - t0, 3), 'zoom': 1.0, 'x': '50%', 'y': '50%', 'ease': 'linear'},
                         {'t': round(t1 - t0, 3), 'zoom': 1.08, 'x': PUNCH['x'], 'y': '70%', 'ease': 'inOut'}]})

t0, t1 = 33.63, 36.7
scene('s11_admin_removed', t0, t1, [
    living_layer(),
    hand(chat_group(t0, t1 - t0), tremble=0, glitch=[{'at': round(34.33 - t0, 3), 'duration': 0.2, 'amount': 0.9}]),
    VIGNETTE,
], camera=push(t1 - t0, 1.0, 1.02))

t0, t1 = 36.7, 39.84
scene('s12_search_214', t0, t1, [
    living_layer(),
    hand({'title': 'Search: Night Security', 'subtitle': '214 results', 'dayLabel': 'Mar 3', 'accent': '#3d5a80', 'clock': '1:13',
          'battery': 23, 'theme': 'dark', 'scale': 1.25, 'messages': SEARCH}),
    VIGNETTE,
], camera=push(t1 - t0, 1.02, 1.06), transition={'type': 'fade', 'duration': 0.25})

t0, t1 = 39.84, 44.44
scene('s13_turn_me', t0, t1, [
    living_layer(),
    hand(chat_group(t0, t1 - t0, unread=0, unreadFrom=0.1)),
    VIGNETTE,
    comp('horror/Glitch', {'cues': [{'at': round(43.88 - t0, 3), 'duration': 0.25, 'amount': 0.9}], 'seed': 'turn'}, depth=0, z=60),
], camera={'keyframes': push(t1 - t0, 1.0, 1.05)['keyframes'], 'shake': [{'at': round(43.88 - t0, 3), 'duration': 0.25, 'amplitude': 16}]})

for sid, a, b, fl in (('s14_floor7', 44.44, 45.77, '7'), ('s15_floor6', 45.77, 46.66, '6')):
    scene(sid, a, b, [
        full('horror/Stairwell', {'floor': fl, 'exit': True, 'flicker': 0.3}),
        comp('horror/Darkness', {'x': 0.5, 'y': 0.45, 'radius': 0.4, 'darkness': 0.6}, depth=0, z=45),
        VIGNETTE,
    ], camera=push(b - a, 1.0, 1.08))

t0, t1 = 46.66, 48.34
scene('s16_seen_by_36', t0, t1, [
    living_layer(),
    hand(chat_group(t0, t1 - t0, subtitle='Seen by 36'), tremble=0),
    VIGNETTE,
])

t0, t1 = 48.34, 49.25
scene('s17_floor5', t0, t1, [
    full('horror/Stairwell', {'floor': '5', 'exit': True, 'flicker': 0.4}),
    comp('horror/Darkness', {'x': 0.5, 'y': 0.45, 'radius': 0.4, 'darkness': 0.65}, depth=0, z=45),
    VIGNETTE,
], callouts=[{'style': 'banner', 'text': 'Night Security: Floor 5.', 'at': 0.0, 'y': '74%'}])

t0, t1 = 49.25, 50.61
scene('s18_footsteps_stop', t0, t1, [
    full('horror/FrontDoor', {'chain': 'on', 'hallLight': 1.0, 'flicker': 0.3, 'feet': [0.1, round(t1 - t0 + 1, 3)]}),
    comp('horror/Darkness', {'x': 0.5, 'y': 0.7, 'radius': 0.5, 'darkness': 0.65}, depth=0, z=45),
    VIGNETTE,
], camera=push(t1 - t0, 1.0, 1.05))

t0, t1 = 50.61, 53.34
scene('s19_no_signal', t0, t1, [
    door_layer(feet=True),
    hand(chat_group(t0, t1 - t0, draft='someone is at my door'),
         phone_extra={'screens': [{'t': 0, 'mode': 'call'}, {'t': 1.55, 'mode': 'chat'}],
                      'call': {'name': '911', 'sub': 'No signal', 'label': 'Call failed', 'at': 0}}),
    VIGNETTE,
], camera={'keyframes': [], 'shake': [{'at': 0.0, 'duration': 0.3, 'amplitude': 10}]})

t0, t1 = 53.34, 53.93
scene('s20_nora_looks', t0, t1, [
    comp('horror/FrontDoor', {'chain': 'on', 'hallLight': 1.0, 'feet': True}, blur=4),
    comp('horror/Protagonist', {'pose': 'idle', 'expr': 'terrified', 'lookX': 0.6, 'light': 'none'}, x='40%', y='100%', anchorY=1, width=1450, height=2204),
    VIGNETTE,
], camera=push(t1 - t0, 1.0, 1.1))

t0, t1 = 53.93, 58.24
blink = 56.05 - t0
glint = 56.15 - t0
scene('s21_covered_peephole', t0, t1, [
    full('horror/Peephole', {'figure': 'none', 'exposure': 0.03, 'flicker': 0, 'radius': 0.52, 'surround': '#26272d'}),
    full('horror/Peephole', {'figure': 'none', 'exposure': 0.6, 'flicker': 0, 'radius': 0.52, 'surround': '#26272d'}, opacity=0,
         keyframes=[{'t': round(blink, 3), 'opacity': 0}, {'t': round(blink + 0.2, 3), 'opacity': 0.85}, {'t': round(blink + 0.4, 3), 'opacity': 0}]),
    {'type': 'circle', 'x': '77.6%', 'y': '31.5%', 'width': 18, 'height': 18, 'fill': '#e8f4ff', 'opacity': 0, 'depth': 0, 'z': 52,
     'keyframes': [{'t': round(glint, 3), 'opacity': 0}, {'t': round(glint + 0.1, 3), 'opacity': 0.9}, {'t': round(glint + 0.35, 3), 'opacity': 0}]},
    comp('horror/Vignette', {'amount': 0.6}, depth=0, z=50),
    comp('horror/Heartbeat', {'bpm': 70, 'bpmTo': 90, 'from': round(54.99 - t0, 3), 'intensity': 0.7}, depth=0, z=55),
], transition={'type': 'cut'}, notes='The only fully still shot: no camera move. Black lens (rim drawn), blinks at 56.05-56.45 with a wet glint.')

t0, t1 = 58.24, 60.17
scene('s22_dm_step_back', t0, t1, [
    door_layer(feet=True),
    hand(chat_dm(NS, DM_NS, t0, t1 - t0), tremble=4, phone_extra={'vibrate': [{'at': 0.0, 'duration': 0.4}]}),
    VIGNETTE,
])

t0, t1 = 60.17, 63.31
scene('s23_door_check', t0, t1, [
    door_layer(feet=True),
    hand(chat_group(t0, t1 - t0), phone_extra={'banners': [{'at': 0.55, 'duration': 1.4, 'app': 'Residents', 'title': NS, 'text': 'Door check. 5B. 20 seconds.'}]}),
    VIGNETTE,
], camera=push(t1 - t0, 1.0, 1.05))

t0, t1 = 63.31, 66.47
scene('s24_open_it', t0, t1, [
    door_layer(feet=True),
    hand(chat_group(t0, t1 - t0), tremble=3),
    VIGNETTE,
])

t0, t1 = 66.47, 71.89
scene('s25_dm_okafor', t0, t1, [
    door_layer(feet=True),
    hand(chat_dm('Mr. Okafor', DM_OK, t0, t1 - t0, subtitle='5A · last seen 9:02 PM',
                 typing=[{'from': 'Mr. Okafor', 'at': round(70.36 - t0, 3), 'until': round(71.89 - t0, 3)}]),
         glitch=[{'at': round(67.75 - t0, 3), 'duration': 0.15, 'amount': 0.5}]),
    VIGNETTE,
], camera=push(t1 - t0, 1.0, 1.05))

t0, t1 = 71.89, 75.78
scene('s26_twist', t0, t1, [
    door_layer(feet=True),
    hand(chat_dm('Mr. Okafor', DM_OK, t0, t1 - t0, subtitle='5A · online')),
    VIGNETTE,
    comp('horror/Glitch', {'cues': [{'at': round(73.18 - t0, 3), 'duration': 0.2, 'amount': 0.6}], 'seed': 'twist'}, depth=0, z=60),
], camera={'keyframes': [{'t': 0, 'zoom': 1.0, 'x': '50%', 'y': '50%', 'ease': 'linear'}, {'t': round(t1 - t0, 3), 'zoom': 1.12, 'x': PUNCH['x'], 'y': '72%', 'ease': 'inOut'}]})

t0, t1 = 75.78, 79.6
off = 78.6 - t0
scene('s27_bookend_two', t0, t1, [
    door_layer(feet=True),
    comp('horror/FrontDoor', {'hallLight': 0.0, 'chain': 'on', 'feet': False}, depth=0.2, blur=8, opacity=0,
         keyframes=[{'t': round(off, 3), 'opacity': 0}, {'t': round(off + 0.3, 3), 'opacity': 0.75}]),
    hand(chat_group(t0, t1 - t0), tremble=1.5),
    VIGNETTE,
], camera=push(t1 - t0, 1.0, 1.04), transition={'type': 'whip', 'duration': 0.3, 'direction': 'left'},
   notes='Bookend: framed exactly like s01. The light line under the door goes out after "Two."')

t0, t1 = 79.6, TOTAL
dur = round(t1 - t0, 3)
scenes.append({'id': 's28_part2_card', 'duration': dur, 'background': {'type': 'color', 'color': '#000000'},
               'layers': [comp('horror/EndCard', {'rule': "Who's in 5B?", 'from': NS, 'sub': 'is typing…', 'label': 'PART 2', 'at': 0.2, 'stampAt': 0.5}, depth=0, z=80)]})

# ------------------------------------------------------------------ captions
EMPH = {'no', 'never', 'wrong.', 'peephole.', 'empty', 'alone,', 'blinking.', 'two', 'removed', 'me.', 'covered.', 'blinked.',
        'nine.', 'friday.', 'two.', 'signal.'}
words = []
for w in cap:
    d = {'text': w['text'], 'start': round(w['start'], 3), 'end': round(w['end'], 3)}
    if w['text'].lower() in EMPH:
        d['emph'] = True
    words.append(d)

sb = {
    'version': 1, 'id': ID, 'title': 'We Have No Night Security. Our Building Chat Does. (Part 1)', 'format': '9:16', 'fps': 30,
    'scenes': scenes,
    'captions': {'words': words, 'maxWords': 6, 'maxChars': 20, 'gapBreak': 0.25,
                 'glue': ['Night Security', 'five B', 'two C', 'nine D', 'Mr. Okafor', 'seven C', 'three D'],
                 'style': {'font': 'display', 'fontSize': 58, 'color': '#ffffff', 'highlight': '#ff4b55', 'highlightMode': 'none',
                           'strokeWidth': 10, 'uppercase': False, 'y': 0.12, 'backing': 0.85}},
    'audio': aud['audio'],
    'overlays': {'grain': 0.5, 'vignette': 0.35, 'fadeIn': 0, 'fadeOut': 0},
}
tot = sum(s['duration'] for s in scenes)
assert abs(tot - TOTAL) < 0.05, (tot, TOTAL)
json.dump(sb, open(f'{EP}/storyboard.json', 'w'), ensure_ascii=False, indent=1)
print('scenes', len(scenes), 'total', round(tot, 3), 'audio', TOTAL)
