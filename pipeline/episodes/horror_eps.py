"""Horror episode scene builders (9:16). One function per episode; scene i = narration paragraph i.

Phone scenes use horror/HandPhone with a blurred set behind; chat threads keep their history across scenes
(earlier bubbles are placed at negative scene times so they are already on screen).
Only horror-kit components and core layers are used.
"""
from __future__ import annotations

from .common import load_cues, ov

# captions sit in the dark band above the hand-held phone (phone cy 0.61; captions clamp to y ~0.16 by the safe area);
# the backing pill keeps them legible whenever a punch-in puts UI behind them
CAPTIONS = {"font": "display", "fontSize": 76, "color": "#ffffff", "highlight": "#ff4b55", "highlightMode": "color",
            "strokeWidth": 12, "uppercase": False, "y": 0.12, "backing": 0.5}
OVERLAYS = {"grain": 0.5, "vignette": 0.0, "fadeIn": 0, "fadeOut": 0.25}  # frame 0 is the TikTok/Shorts cover: never black
VIG = 0.4      # default vignette (0.7-0.8 crushed the picture far below the references' exposure)
DARK = 0.3     # default Darkness overlay strength (was 0.55-0.65)
# Chat look shared by every horror episode: bright grey messenger with big text, like the reference series
# (a light screen glowing in a dark room reads at a glance on a phone; 1.25x text keeps 3-5 bubbles on screen).
CHAT_THEME = "light"
CHAT_SCALE = 1.25
BG = {"type": "color", "color": "#0b0d12"}

FADE = {"type": "fade", "duration": 0.25}
DIP = {"type": "dipBlack", "duration": 0.3}
GLITCH = {"type": "glitch", "duration": 0.3}
WHIP = {"type": "whip", "duration": 0.3, "direction": "up"}


class Thread:
    """A chat thread whose messages persist across scenes. Times stored globally."""

    def __init__(self, title, members, count=None, subtitle=None, accent="#3d5a80", day="Today", clock="1:02", battery=31,
                 theme=None, scale=None):
        self.title, self.members, self.count, self.subtitle = title, members, count, subtitle
        self.accent, self.day, self.clock, self.battery = accent, day, clock, battery
        self.theme, self.scale = theme or CHAT_THEME, scale or CHAT_SCALE
        self.msgs = []  # (global_t, dict)
        self.pin = None  # {"text", "at" (global), "editAt" (global), "editText", ...}

    def history(self, items, start=-60.0):
        """Old messages already on screen when the thread first appears: [(from, text) | ("system", text)]."""
        for k, (frm, txt) in enumerate(items):
            m = {"text": txt, "kind": "system"} if frm == "system" else {"text": txt, "me": True} if frm == "me" else {"text": txt, "from": frm}
            self.msgs.append((start + k, m))

    def system(self, sc, at, text):
        self.msgs.append((sc.start + at, {"text": text, "kind": "system"}))

    def pinned(self, sc, at, text, **kw):
        self.pin = {"text": text, "at": sc.start + at, **kw}

    def edit_pin(self, sc, at, text):
        self.pin.update({"editAt": sc.start + at, "editText": text})

    def add(self, sc, at, text, frm=None, me=False, kind=None):
        m = {"text": text}
        if me:
            m["me"] = True
        else:
            m["from"] = frm
        if kind:
            m["kind"] = kind
        self.msgs.append((sc.start + at, m))

    def chat(self, sc, typing=(), keep=7, dots=0.7, **over):
        """dots: show the sender's typing dots for this many seconds before every bubble that lands in this scene."""
        shown = [(t, m) for t, m in self.msgs if t < sc.start + sc.dur]
        shown = shown[-keep:]
        msgs = []
        typing = list(typing)
        for t, m in shown:
            local = round(t - sc.start, 3)
            msgs.append({**m, "at": local})
            if dots and m.get("from") and m.get("kind") != "system" and local > dots + 0.05 \
                    and not any(a <= local <= u + 0.05 for _, a, u in typing):
                typing.append((m["from"], round(local - dots, 3), local))
        c = {"title": self.title, "messages": msgs, "dayLabel": self.day, "accent": self.accent,
             "clock": self.clock, "battery": self.battery, "theme": self.theme, "scale": self.scale}
        if self.pin and self.pin["at"] < sc.start + sc.dur:
            pin = {**self.pin, "at": round(self.pin["at"] - sc.start, 3)}
            if "editAt" in pin:
                pin["editAt"] = round(pin["editAt"] - sc.start, 3)
            c["pinned"] = pin
        if self.count is not None:
            c["count"] = self.count
        if self.subtitle:
            c["subtitle"] = self.subtitle
        if typing:
            c["typing"] = [{"from": f, "at": a, "until": u} for f, a, u in typing]
        c.update(over)
        return c


def handphone(phone, tilt=-3, tremble=1.5, taps=None, side="right", **kw):
    # thumb rests over the input bar so it never covers the newest bubble
    # cy 0.61: the status bar sits below the caption band
    p = {"phoneWidth": 0.68, "cx": 0.53, "cy": 0.61, "tilt": tilt, "tremble": tremble, "side": side, "phone": phone,
         "thumbY": 0.9, "thumbReach": 0.16, **kw}
    if taps:
        p["taps"] = taps
    return {"type": "component", "name": "horror/HandPhone", "props": p}


def behind(name, **props):
    return {"type": "component", "name": f"horror/{name}", "depth": 0.2, "blur": 4, "opacity": 1.0, "props": props}


# world positions on the hand-held phone (cy 0.61, width 0.68): newest bubble ~86% down, pinned bar ~34%
BUBBLE_Y = 0.86
PIN_Y = 0.34


def _clampy(v, z):
    lo = 1 / (2 * z)
    return max(lo, min(1 - lo, v))


def shot(t, zoom=1.0, y=None, x=None, how="cut", drift=0.03):
    """One framing. how: 'cut' (hard cut, then slow drift) or 'punch' (0.25 s ease-out push from the last framing).
    y/x: world point (fraction of the frame) to aim at, clamped so the view never leaves the frame."""
    yy = _clampy(0.5 if y is None else y, zoom)
    xx = _clampy(0.5 if x is None else x, zoom)
    return {"t": round(max(0.0, t), 3), "zoom": zoom, "y": yy, "x": xx, "how": how, "drift": drift}


def shots_cam(shots, dur, shake=None):
    """Camera keyframes from a shot list (rule: no framing held longer than ~3 s)."""
    shots = sorted(shots, key=lambda s: s["t"])
    kfs, last = [], None
    for i, s in enumerate(shots):
        nxt = shots[i + 1]["t"] if i + 1 < len(shots) else dur
        pos = {"zoom": s["zoom"], "x": f"{s['x'] * 100:.2f}%", "y": f"{s['y'] * 100:.2f}%"}
        if s["how"] == "punch" and last:
            kfs.append({**last, "t": s["t"], "ease": "linear"})
            kfs.append({"t": round(min(s["t"] + 0.25, nxt - 0.02), 3), **pos, "ease": "out"})
        else:
            kfs.append({"t": s["t"], **pos, "ease": "step" if kfs else "linear"})
        z2 = round(s["zoom"] * (1 + s["drift"]), 4)
        last = {"zoom": z2, "x": f"{_clampy(s['x'], z2) * 100:.2f}%", "y": f"{_clampy(s['y'], z2) * 100:.2f}%"}
        kfs.append({"t": round(max(kfs[-1]["t"] + 0.05, nxt - 1 / 30), 3), **last, "ease": "linear"})
    cam = {"keyframes": kfs}
    if shake:
        cam["shake"] = shake
    return cam


def bubble_shots(chat, dur, punch=1.3):
    """Default phone camera: full shot, then a 0.25 s punch toward the bubble zone on every new bubble, easing back."""
    beats = sorted(m["at"] for m in (chat or {}).get("messages", []) if 0.3 <= m["at"] < dur - 0.3)
    out = [shot(0, 1.0)]
    for a in beats:
        out.append(shot(a, punch, y=BUBBLE_Y, how="punch", drift=-0.15))
    return out


def phone_scene(sc, members, chat=None, mode="chat", set_="Bedroom", set_props=None, tilt=-3, tremble=1.5, taps=None,
                vibrate=None, banners=None, extra=None, camera=None, trans=FADE, lock=None, call=None, screens=None,
                heartbeat=None, glitch=None, shots=None, vig=VIG, shake=None):
    """Camera: `camera` as given, else `shots` (see shot()), else bubble_shots (punch-in on every new bubble)."""
    phone = {"members": members, "mode": mode}
    if chat:
        phone["chat"] = chat
    if lock:
        phone["lock"] = lock
    if call:
        phone["call"] = call
    if screens:
        phone["screens"] = screens
    if vibrate:
        phone["vibrate"] = [{"at": a, "duration": 0.4} for a in vibrate]
    if banners:
        phone["banners"] = banners
    hp = handphone(phone, tilt=tilt, tremble=tremble, taps=taps)
    if glitch:
        hp["props"]["glitch"] = [{"at": a, "duration": 0.22, "amount": 0.9} for a in glitch]
    layers = [behind(set_, **(set_props or {"lamp": 0})), hp, ov("horror/Vignette", amount=vig)]
    if heartbeat:
        layers.append(ov("horror/Heartbeat", **heartbeat))
    if glitch:
        layers.append(ov("horror/Glitch", z=60, cues=[{"at": a, "duration": 0.25, "amount": 1} for a in glitch], seed=f"g{sc.i}"))
    layers += extra or []
    cam = camera or shots_cam(shots or bubble_shots(chat, sc.dur), sc.dur, shake=shake)
    if vibrate and "shake" not in cam:
        cam = {**cam, "shake": [{"at": a, "duration": 0.3, "amplitude": 10} for a in vibrate]}
    s = {"id": f"p{sc.i:02d}", "duration": sc.dur, "background": BG, "layers": layers, "camera": cam,
         "transitionIn": trans or {"type": "cut"}, "notes": sc.text}
    return s


def set_scene(sc, bg_name, bg_props, layers, camera=None, trans=FADE, grade=None, bg_depth=0.25):
    s = {"id": f"p{sc.i:02d}", "duration": sc.dur,
         "background": {"type": "component", "name": f"horror/{bg_name}", "depth": bg_depth, "props": bg_props},
         "layers": layers, "camera": camera or {"preset": "pushIn", "amount": 0.8},
         "transitionIn": trans or {"type": "cut"}, "notes": sc.text}
    if grade:
        s["grade"] = grade
    return s


def nora(expr_track, pose="idle", x="50%", w=860, look=(0, 0), talk=None, light=None, flip=False, blink=True, **kw):
    p = {"pose": pose, "exprs": [{"t": t, "e": e} for t, e in expr_track], "lookX": look[0], "lookY": look[1]}
    if not blink:
        p["blink"] = False
    if talk:
        p["talk"] = talk
    if light:
        p["light"] = light
    layer = {"type": "component", "name": "horror/Protagonist", "x": x, "y": "100%", "anchorY": 1, "width": w,
             "height": round(w * 1.52), "props": p, "flipX": flip}
    layer.update(kw)
    return layer


def knocks_cam(times, amp=20):
    return [{"at": a, "duration": 0.16, "amplitude": amp} for a in times]


def cutaway(t0, t1, bg_name, bg_props, layers=(), z=40, push=(1.0, 1.05)):
    """A reaction/insert shot inside a phone scene: a full-frame set plus layers shown from t0 to t1 (scene time),
    fixed to the screen (depth 0) so the phone scene's camera move does not touch it. Breaks up long chat runs the
    way the reference series cuts phone -> face -> phone. push: slow scale on the set over the shot."""
    t0, t1 = round(t0, 3), round(t1, 3)
    bg = {"type": "component", "name": f"horror/{bg_name}", "depth": 0, "z": z, "start": t0, "end": t1, "props": bg_props}
    if push and push[0] != push[1]:
        bg["keyframes"] = [{"t": t0, "scale": push[0]}, {"t": t1, "scale": push[1], "ease": "linear"}]
    out = [bg]
    for k, l in enumerate(layers):
        out.append({**l, "depth": 0, "z": z + 1 + k, "start": t0, "end": t1})
    return out


def nora_cu(expr_track, w=1150, look=(0, 0.4), **kw):
    """Reaction close-up: Nora lit by her phone, face in the middle third of the frame."""
    return nora(expr_track, pose="phone", light="phone", x="50%", w=w, look=look, **kw)


def phone_insert(t0, t1, phone, z=45, **hp):
    """A hand-held phone popping over a non-phone scene (e.g. a buzz at the end of a peephole shot)."""
    layer = handphone({"mode": "chat", **phone}, **hp)
    return [{"type": "rect", "fill": "#000000", "opacity": 0.55, "width": "100%", "height": "100%", "depth": 0, "z": z,
             "start": t0, "end": t1},
            {**layer, "depth": 0, "z": z + 1, "start": t0, "end": t1, "enter": {"type": "slideUp", "duration": 0.25, "distance": 500}}]


# =========================================================================== pinned rules (PILOT)

def pinned_rules(S):
    """Shot grammar (fix round 1): every phone paragraph alternates full phone -> tight insert on the newest bubble
    (hard cut, zoom 1.7-2.0) -> Nora reaction close-up, no framing held > 3 s; sets lifted to night midtones."""
    use_cues("horror-pinned-rules")
    M = {"Management": {"color": "#3a3f4a", "initials": "M"}, "Ben (5A)": {"color": "#8f6a4a", "initials": "B"},
         "Dev (6C)": {"color": "#4f7a73", "initials": "D"}, "Mrs. Ortiz (3B)": {"color": "#7a5c8f", "initials": "MO"},
         "Kay (2F)": {"color": "#4a628f", "initials": "K"}}
    RULE4 = "RULE 4: If someone knocks three times, you are not home. Do not answer. Do not move."
    th = Thread("Willow Court Residents", M, count=38, day="Today 1:02 AM", clock="1:04")
    # a lived-in chat: ordinary building noise before the rules arrive (fills the top of the screen)
    th.history([("Kay (2F)", "whoever keeps propping the lobby door open pls stop"),
                ("Mrs. Ortiz (3B)", "the dryer in the basement ate my sock again"),
                ("Dev (6C)", "anyone else's heating ticking all night?"),
                ("system", "Management pinned a message")])
    BED = {"lamp": 0.15, "rain": True}
    BED_CU = {"lamp": 0.3, "rain": True, "phoneGlow": 1}
    LIV = {"lamp": 0.45, "tv": "off"}
    DOOR = {"hallLight": 0.5, "chain": "on"}
    out = []

    # 0 hook: frame 0 = tight crop on the red pinned rule (the cover), hook caption burned in for 0-0.5 s,
    #   pull back to the full phone, then Nora's face on "Do not answer"
    s = S[0]
    th.pinned(s, -1, RULE4, **{"from": "Management"})
    th.add(s, -0.6, RULE4, "Management", kind="card")
    cu = s.at("Do", off=-0.08)
    out.append(phone_scene(s, M, th.chat(s), set_props=BED, trans=None,
                           camera={"keyframes": [{"t": 0, "zoom": 1.5, "x": "50%", "y": "66.6%"},
                                                 {"t": 0.5, "zoom": 1.5, "x": "50%", "y": "66.6%"},
                                                 {"t": 2.5, "zoom": 1.1, "x": "50%", "y": "56%", "ease": "inOut"},
                                                 {"t": cu, "zoom": 1.14, "x": "50%", "y": "56%", "ease": "linear"}],
                                   "shake": [{"at": s.at("knocks"), "duration": 0.6, "amplitude": 8}]},
                           extra=[ov("horror/RedText", z=70, text="RULE 4: DON'T ANSWER THE DOOR", style="neon", at=-0.3,
                                     duration=s.first() + 0.3, fontSize=118, shake=0, y=0.155)]
                           + cutaway(cu, s.dur, "Bedroom", BED_CU, [
                               nora_cu([(0, "scared"), (s.at("move.", off=-0.1), "terrified")], blink=False)])))
    # 1 pinned + signed + rule five: full -> punch on the post -> insert on rule 5 -> face
    s = S[1]
    b1 = s.at("Signed", off=-0.05)
    b2 = s.at("Rule", off=-0.05)
    th.add(s, b1, "New building rules (1-7) are now in effect. Thank you for your cooperation.\n- Management", "Management")
    th.add(s, b2, "RULE 5: Management will never ask to come inside.", "Management")
    f1 = s.at("Management", nth=1, off=-0.05)
    out.append(phone_scene(s, M, th.chat(s, unread=6, unreadFrom=-99), vibrate=[0.1], trans=None,
                           shots=[shot(0, 1.0), shot(b1, 1.3, y=BUBBLE_Y, how="punch", drift=0.02),
                                  shot(b2 + 0.05, 1.65, y=BUBBLE_Y, x=0.53)],
                           extra=cutaway(f1 + 0.9, s.dur, "Bedroom", BED_CU, [nora_cu([(0, "suspicious")], look=(0.1, 0.5))])))
    # 2 the company is gone (lands ~12-14 s): full -> insert on Dev's alert -> Nora reaction on "shut down"
    s = S[2]
    b = s.at("checked", off=-0.05)
    shut = s.at("shut")
    th.add(s, b, "Looked up Hartwell Property Group. DISSOLVED. Closed two years ago.", "Dev (6C)", kind="alert")
    out.append(phone_scene(s, M, th.chat(s), glitch=[shut], tremble=2.5, trans=None,
                           shots=[shot(0, 1.0), shot(b, 1.3, y=BUBBLE_Y, how="punch", drift=0.02),
                                  shot(s.at("Our", off=-0.05), 1.65, y=BUBBLE_Y, x=0.53)],
                           extra=cutaway(shut, s.dur, "LivingRoom", LIV, [
                               nora_cu([(0, "shocked"), (shut + 0.5, "scared")], blink=False)])))
    # 3 reaction: medium, then a hard cut closer on "And who pinned the rules?"
    s = S[3]
    out.append(set_scene(s, "LivingRoom", LIV, [
        nora([(0, "suspicious"), (s.at("pinned", off=-0.2), "scared")], pose="phone", light="phone", look=(0, 0.6), w=900),
        ov("horror/Darkness", x=0.5, y=0.55, radius=0.55, darkness=DARK),
        ov("horror/Vignette", amount=VIG)], grade={"saturate": 0.85}, trans=DIP,
        camera=shots_cam([shot(0, 1.0, y=0.55), shot(s.at("And", off=-0.05), 1.4, y=0.5)], s.dur)))
    # 4 the chorus laughs, Ben dares it: punches on each bubble, insert on Ben, a hallway establishing shot
    s = S[4]
    th.add(s, s.at("prank.", off=-0.4), "lol is this a prank", "Mrs. Ortiz (3B)")
    th.add(s, s.at("prank.", off=0.35), "probably the kids on 4", "Kay (2F)")
    bb1 = s.at("leave", off=0.1)
    bb2 = s.at("break", off=0.2)
    th.add(s, bb1, "leaving my hallway light ON tonight", "Ben (5A)")
    th.add(s, bb2, "breaking every rule. let's see what happens", "Ben (5A)")
    h0, h1 = s.at("light", off=0.0), bb2 - 0.05
    out.append(phone_scene(s, M, th.chat(s, clock="1:09"), trans=FADE,
                           shots=[shot(0, 1.0), shot(s.at("prank.", off=-0.4), 1.25, y=BUBBLE_Y, how="punch", drift=0.02),
                                  shot(s.at("prank.", off=0.35), 1.35, y=BUBBLE_Y, how="punch", drift=0.02),
                                  shot(bb1, 1.65, y=BUBBLE_Y, x=0.53), shot(bb2, 1.6, y=BUBBLE_Y, x=0.53),
                                  shot(s.at("just", off=-0.05), 1.0)],
                           extra=cutaway(h0, h1, "Hallway", {"flicker": 0.5, "lights": 3, "endDoor": True}, push=(1.0, 1.12))))
    # 5 2:14, Ben at his door: insert on "someone's knocking", then a two-shot of Ben's door, back for "wish me luck"
    s = S[5]
    th.clock = "2:14"
    k1 = s.at("Someone's", off=-0.1)
    k2 = s.at("I'm", off=-0.1)
    th.add(s, k1, "someone's knocking. 3 times", "Ben (5A)")
    th.add(s, k2, "i'm opening it. wish me luck", "Ben (5A)")
    d0, d1 = k1 + 0.65, s.at("Wish", off=-0.03)
    ben = {"type": "component", "name": "horror/Neighbour", "x": "50%", "y": "100%", "anchorY": 1, "width": 980, "height": 1490,
           "props": {"silhouette": True, "exprs": [{"t": 0, "e": "neutral"}], "lookX": 0.6}}
    plate = {"type": "text", "text": "5A", "x": "50%", "y": "21%", "fontSize": 64, "color": "#c9b98f", "font": "display"}
    out.append(phone_scene(s, M, th.chat(s), vibrate=[k1], trans=DIP,
                           shots=[shot(0, 1.0), shot(k1, 1.65, y=BUBBLE_Y, x=0.53), shot(d1, 1.6, y=BUBBLE_Y, x=0.53)],
                           extra=cutaway(d0, d1, "FrontDoor", {"hallLight": 0.9, "chain": "off", "knocks": [d0 + 0.05, d0 + 0.35],
                                                              "handle": [{"at": s.at("opening"), "duration": 0.6}]},
                                         [ben, plate], push=(1.0, 1.1))))
    # 6 the green dot goes grey (dark UI: the lights are going out)
    s = S[6]
    g = s.at("grey.", off=-0.05)
    th.system(s, g, "Ben (5A) · last seen 2:14 AM")
    out.append(phone_scene(s, M, th.chat(s, clock="2:21"), tremble=3, heartbeat={"bpm": 80, "bpmTo": 110}, trans=None,
                           shots=[shot(0, 1.0), shot(s.at("His", off=-0.05), 1.8, y=BUBBLE_Y, x=0.5),
                                  shot(g, 1.35, y=BUBBLE_Y, how="punch")],
                           extra=cutaway(g + 0.35, s.dur, "Bedroom", {"lamp": 0.1, "phoneGlow": 1}, [
                               nora_cu([(0, "scared")], blink=False, look=(0, 0.6))])))
    # 7 rule five is edited: insert on the pinned bar as it flashes, insert on the new alert, then her face
    s = S[7]
    e = s.at("changed.", off=-0.1)
    th.edit_pin(s, e, "RULE 5 (edited): Management may need to come inside. Please cooperate.")
    th.system(s, e, "Management edited the pinned message")
    ra = s.at("Rule", off=-0.05)
    th.add(s, ra, "RULE 5 (edited): Management may need to come inside. Please cooperate.", "Management", kind="alert")
    out.append(phone_scene(s, M, th.chat(s, clock="2:23"), glitch=[e], tremble=3, trans=GLITCH,
                           shots=[shot(0, 1.0), shot(e, 1.65, y=PIN_Y, x=0.53), shot(s.at("Management", off=-0.1), 1.6, y=BUBBLE_Y, x=0.53)],
                           extra=cutaway(s.at("Please", off=-0.1), s.dur, "Bedroom", {"lamp": 0.1, "phoneGlow": 1}, [
                               nora_cu([(0, "terrified")], blink=False, look=(0, 0.6))])))
    # 8 back against the door: wide (light switches off), then a hard cut closer on "sat", face in the middle third
    s = S[8]
    off_t = s.at("off")
    out.append(set_scene(s, "FrontDoor", DOOR, [
        nora([(0, "scared"), (s.dur * 0.6, "terrified")], x="50%", w=1000, look=(0.5, 0)),
        ov("horror/Darkness", x=0.5, y=0.5, radius=0.6, darkness=DARK),
        ov("horror/Flicker", strength=0, blackouts=[{"at": off_t, "duration": 0.12}], seed="sw"),
        ov("horror/Vignette", amount=VIG)], trans=DIP,
        camera=shots_cam([shot(0, 1.0, drift=0.02), shot(s.at("sat", off=-0.05), 1.15, y=0.47, drift=0.04)], s.dur)))
    # 9 three knocks behind my head (knock3_slow onsets 0 / 0.95 / 1.9 s): cut on every knock
    s = S[9]
    k0 = _sfx_at(s, "knock3_slow", s.at("knocked", off=0.4))
    ks = [k0, k0 + 0.95, k0 + 1.9]
    three = s.at("Three", off=-0.05)
    out.append(set_scene(s, "FrontDoor", {**DOOR, "knocks": ks, "feet": [k0 - 0.5, 99]}, [
        nora([(0, "scared")], x="50%", w=1000, look=(0.5, 0), end=k0),
        *cutaway(ks[1], ks[2], "FrontDoor", {**DOOR, "knocks": ks, "feet": [k0 - 0.5, 99]}, [
            nora([(0, "shocked")], x="50%", w=1200, look=(0.8, 0), blink=False)], push=(1.05, 1.1)),
        *cutaway(three, s.dur, "FrontDoor", {**DOOR, "knocks": ks, "feet": [k0 - 0.5, 99]}, [
            nora([(0, "terrified")], x="50%", w=1200, look=(0.8, 0.1), blink=False)], push=(1.05, 1.12)),
        ov("horror/Vignette", amount=VIG)],
        camera=shots_cam([shot(0, 1.12, y=0.47, drift=0.03), shot(k0, 1.3, x=0.66, y=0.47),
                          shot(ks[2], 1.25, y=0.87, drift=0.08)], s.dur, shake=knocks_cam(ks)), trans=None))
    # 10 the voice: peephole, hard cut closer when it says "It's Management"
    s = S[10]
    out.append({"id": f"p{s.i:02d}", "duration": s.dur, "background": {"type": "color", "color": "#050506"},
                "layers": [{"type": "component", "name": "horror/Peephole", "depth": 1, "props": {
                    "figure": "neighbour", "exprs": [{"t": 0, "e": "smile"}], "lean": 0.4, "flicker": 0.3, "radius": 0.52, "exposure": 2.0, "surround": "#4a5262",
                    "talk": [[s.at("It's"), s.last()]]}},
                    ov("horror/Flicker", strength=0.3, seed="pp")],
                "camera": shots_cam([shot(0, 1.0), shot(s.at("It's", off=-0.05), 1.3, y=0.42), shot(s.at("We", off=-0.05), 1.15, y=0.45)], s.dur),
                "transitionIn": DIP, "notes": s.text})
    # 11 Ben's DM: pre-filled thread, punch on each bubble, 0.3 s flash of the peephole between them, then her face
    s = S[11]
    dm = Thread("Ben (5A)", M, subtitle="online", day="Yesterday", clock="2:31")
    dm.history([("Ben (5A)", "u still have my drill?"), ("me", "yeah sorry, tomorrow"), ("Ben (5A)", "no rush lol"),
                ("Ben (5A)", "did u see the rules thing in the group"), ("system", "Today 2:31 AM")], start=-40)
    m1 = s.at("It's", off=-0.05)
    m2 = s.at("I'm", off=-0.05)
    dm.add(s, m1, "it's fine, open up. they only want to talk", "Ben (5A)")
    dm.add(s, m2, "i'm standing right behind them", "Ben (5A)")
    pk = s.at("They", off=0.05)
    out.append(phone_scene(s, M, dm.chat(s), vibrate=[s.at("buzzed.", off=-0.1)], tremble=4, set_="FrontDoor",
                           set_props=DOOR, trans=None,
                           shots=[shot(0, 1.0), shot(s.at("message", off=-0.05), 1.35, y=0.64), shot(m1, 1.55, y=BUBBLE_Y, how="punch", drift=0.02),
                                  shot(pk + 0.3, 1.35, y=0.64), shot(m2, 1.6, y=BUBBLE_Y, how="punch", drift=0.02)],
                           extra=[*cutaway(pk, pk + 0.3, "Peephole", {"figure": "neighbour", "exprs": [{"t": 0, "e": "smile"}], "lean": 0.5, "flicker": 0.5, "radius": 0.52, "exposure": 2.0, "surround": "#4a5262"}, push=None),
                                  *cutaway(s.at("behind", off=-0.05), s.dur, "FrontDoor", DOOR, [
                                      nora_cu([(0, "terrified")], blink=False, look=(0, 0.5))])]))
    # 12 only one person (hard cut closer on "one", grin, red under-light) -> RULE 6 bookend on the phone -> PART 2
    s = S[12]
    one = s.at("one")
    buzz = _sfx_at(s, "phone_buzz", s.at("there.", off=1.2))
    book = round(buzz - 0.15, 3)
    card = round(buzz + 0.68, 3)
    dur = round(card + 0.97, 3)          # end ~0.8 s after the PART 2 card lands
    th.clock = "2:33"
    th.add(s, buzz + 0.05, "RULE 6:", "Management", kind="card")
    rule6 = th.chat(s, typing=[("Management", buzz + 0.45, dur + 1)], dots=0)
    rule6["subtitle"] = "Management is typing…"
    rule6["scale"] = 1.5
    peep = {"radius": 0.52, "exposure": 2.0, "surround": "#4a5262", "lean": 0.55, "flicker": 0.5, "lookX": 0, "lookY": 0.1, "figure": "neighbour"}
    end_phone = handphone({"members": M, "mode": "chat", "chat": rule6, "vibrate": [{"at": buzz, "duration": 0.5}]}, tremble=5)
    out.append({"id": f"p{s.i:02d}", "duration": dur, "background": {"type": "color", "color": "#050506"},
                "layers": [{"type": "component", "name": "horror/Peephole", "depth": 1, "end": one, "props": {
                    **peep, "exprs": [{"t": 0, "e": "smile"}]}},
                    {"type": "component", "name": "horror/Peephole", "depth": 1, "start": one, "props": {
                        **peep, "exprs": [{"t": 0, "e": "grin"}], "light": "red", "flicker": 0.2,
                        "glitch": [{"at": one, "duration": 0.25, "amount": 1}]}},
                    ov("horror/RedText", z=55, text="Only one", style="flash", at=one + 0.1, duration=book - one - 0.1,
                       fontSize=120, strobe=8, y=0.8),
                    ov("horror/Glitch", z=60, cues=[{"at": one, "duration": 0.3, "amount": 1}], seed="end"),
                    ov("horror/Flicker", strength=0.4, seed="pe"),
                    *cutaway(book, dur, "Bedroom", {**BED, "lamp": 0.6}, [end_phone], z=45, push=None),
                    ov("horror/RedText", z=70, text="PART 2", style="stamp", at=card, duration=dur - card, fontSize=130, shake=0, y=0.135)],
                "camera": shots_cam([shot(0, 1.0, drift=0.06), shot(one, 1.4, y=0.36)], dur,
                                    shake=[{"at": one, "duration": 0.4, "amplitude": 18}]),
                "transitionIn": GLITCH, "notes": s.text})
    return out


def _sfx_at(sc, cue, default):
    """Scene-local start of an SFX cue placed by the audio mix (episodes/<slug>/audio/cues.json), else default,
    so knocks/buzzes on screen land on the knocks/buzzes in the mix."""
    for c in _CUES:
        if c["cue"] == cue and sc.start <= c["at"] < sc.start + sc.dur:
            return round(c["at"] - sc.start, 3)
    return default


_CUES: list = []


def use_cues(slug):
    _CUES[:] = load_cues(slug)


# =========================================================================== mom two chats

def mom_two_chats(S):
    M = {"Mom": {"color": "#8f4a55", "initials": "M"}, "Dad": {"color": "#4a628f", "initials": "D"},
         "Sam": {"color": "#6b7a4a", "initials": "S"}}
    fam = Thread("Family", M, subtitle="Mom, Dad, Sam, you", day="Today 11:02 PM", clock="11:02")
    dm = Thread("Mom", M, subtitle="mobile", day="Today 11:02 PM", clock="11:02")
    fam.add(S[0], -2, "dinner sunday?", "Sam")
    out = []
    s = S[0]
    fam.add(s, s.at("I'm", off=-0.05), "I'm outside. Unlock the door, my hands are full", "Mom")
    out.append(phone_scene(s, M, fam.chat(s), set_="LivingRoom", set_props={"lamp": 0.4, "tv": "glow"},
                           vibrate=[s.at("I'm", off=-0.05)], trans=None))
    s = S[1]
    dm.add(s, s.at("Still", off=-0.05), "Still at the hospital with Grandpa.", "Mom")
    dm.add(s, s.at("Don't", off=-0.05), "Don't open the door for anyone.", "Mom", kind="alert")
    out.append(phone_scene(s, M, dm.chat(s), set_="LivingRoom", set_props={"lamp": 0.4, "tv": "glow"},
                           mode="chat", banners=[{"at": 0.1, "duration": 1.4, "app": "Messages", "title": "Mom", "text": "Still at the hospital with Grandpa."}],
                           vibrate=[0.1]))
    s = S[2]
    out.append({"id": f"p{s.i:02d}", "duration": s.dur, "background": BG, "notes": s.text, "transitionIn": DIP,
                "layers": [
                    behind("LivingRoom", lamp=0.3),
                    {"type": "component", "name": "horror/Phone", "x": "27%", "y": "56%", "width": 470, "height": 970, "rotate": -5,
                     "props": {"members": M, "mode": "chat", "chat": fam.chat(s)}},
                    {"type": "component", "name": "horror/Phone", "x": "73%", "y": "56%", "width": 470, "height": 970, "rotate": 5,
                     "props": {"members": M, "mode": "chat", "chat": dm.chat(s)}},
                    ov("horror/RedText", z=55, text="One is lying", style="neon", at=s.at("lying", off=-0.2), fontSize=110, strobe=0),
                    ov("horror/Vignette", amount=0.7)],
                "camera": {"preset": "pushIn", "amount": 0.6}})
    s = S[3]
    fam.add(s, s.at("Mom", off=-0.1), "Mom, what was our first dog called?", me=True)
    fam.add(s, s.at("Biscuit"), "Biscuit", "Mom")
    out.append(phone_scene(s, M, fam.chat(s, clock="11:04"), set_="LivingRoom", set_props={"lamp": 0.4},
                           taps=[{"at": s.at("Mom", off=-0.3), "x": 0.88, "y": 0.95}], trans=DIP))
    s = S[4]
    dm.add(s, s.at("same", off=0), "what was our first dog called?", me=True)
    dm.add(s, s.at("Biscuit"), "Biscuit. Lock the deadbolt. Please.", "Mom")
    out.append(phone_scene(s, M, dm.chat(s, clock="11:05", typing=[("Mom", s.at("took"), s.at("Biscuit"))]),
                           set_="LivingRoom", set_props={"lamp": 0.4}, trans=FADE))
    s = S[5]
    out.append({"id": f"p{s.i:02d}", "duration": s.dur, "background": {"type": "color", "color": "#050506"}, "notes": s.text,
                "transitionIn": DIP,
                "layers": [{"type": "component", "name": "horror/Peephole", "depth": 0,
                            "props": {"figure": "silhouette", "lean": 0.2, "flicker": 0.35}},
                           ov("horror/Flicker", strength=0.3, seed="bell")],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": s.dur, "zoom": 1.1}],
                           "shake": [{"at": s.at("rang", off=-0.2), "duration": 0.3, "amplitude": 12}]}})
    s = S[6]
    fam.add(s, s.at("joined", off=-0.1), "Dad joined the conversation", "Dad", kind="alert")
    fam.add(s, s.at("It's", off=-0.05), "It's really her, sweetheart. Let her in. It's freezing out there.", "Dad")
    out.append(phone_scene(s, M, fam.chat(s, clock="11:07"), set_="LivingRoom", set_props={"lamp": 0.3},
                           vibrate=[s.at("It's", off=-0.05)], trans=DIP))
    s = S[7]
    out.append(phone_scene(s, M, mode="call", call={"name": "Dad", "sub": "mobile", "label": "calling…", "at": 0, "clock": "11:07"},
                           set_="LivingRoom", set_props={"lamp": 0.3}, tremble=3, trans=FADE))
    s = S[8]
    out.append(set_scene(s, "LivingRoom", {"lamp": 0.3, "tv": "off"}, [
        nora([(0, "worried"), (s.at("house", off=-0.2), "shocked"), (s.at("closet"), "terrified")], pose="ear",
             look=(-0.6, 0), x="62%"),
        ov("horror/Heartbeat", bpm=100, bpmTo=140),
        ov("horror/Vignette", amount=0.75)],
        camera={"preset": "pushIn", "amount": 1.0, "shake": [{"at": s.at("house", off=-0.2), "duration": 0.3, "amplitude": 14}]},
        trans=None))
    s = S[9]
    out.append(set_scene(s, "LivingRoom", {"lamp": 0.2}, [
        nora([(0, "terrified")], x="50%", w=980, look=(0, 0.2)),
        ov("horror/Darkness", x=0.5, y=0.55, radius=0.5, darkness=0.6),
        ov("horror/Heartbeat", bpm=120)], camera={"preset": "pushIn", "amount": 1.4}, trans=None))
    s = S[10]
    out.append(set_scene(s, "Hallway", {"flicker": 0.6, "lights": 1, "endDoor": True}, [
        ov("horror/Darkness", x=0.5, y=0.45, radius=0.35, darkness=0.8, flicker=0.3),
        ov("horror/RedText", z=55, text="In the closet", style="scrawl", at=s.at("closet", off=-0.1), fontSize=130),
        ov("horror/Vignette", amount=0.85)], camera={"preset": "pushIn", "amount": 1.5}, trans=GLITCH))
    s = S[11]
    out.append(phone_scene(s, M, fam.chat(s, clock="11:08", typing=[("Dad", s.at("dots", off=-0.4), s.dur + 1)]),
                           set_="LivingRoom", set_props={"lamp": 0.1}, tremble=5, glitch=[s.at("typing", off=0.4)],
                           heartbeat={"bpm": 130, "bpmTo": 170}, trans=FADE,
                           camera={"keyframes": [{"t": 0, "zoom": 1.0}, {"t": s.dur, "zoom": 1.06, "y": "48%"}]}))
    return out


# =========================================================================== member 41

def member_41(S):
    M = {"Night Desk": {"color": "#2a2d33", "initials": "ND"}, "Priya (2D)": {"color": "#8f4a55", "initials": "P"},
         "Admin · Tom (1A)": {"color": "#4f7a73", "initials": "T"}, "Leo (3C)": {"color": "#6b7a4a", "initials": "L"},
         "4D": {"color": "#7a5c8f", "initials": "4D"}}
    th = Thread("Elm House Residents", M, count=41, day="Today 12:40 AM", clock="12:41")
    th.add(S[0], -4, "anyone hear that bang on 3?", "Leo (3C)")
    th.add(S[0], -3, "A delivery cart. It has left the building.", "Night Desk")
    out = []
    s = S[0]
    out.append(phone_scene(s, M, th.chat(s), set_="Hallway", set_props={"flicker": 0.2, "lights": 2},
                           extra=[ov("horror/RedText", z=55, text="41 members", style="neon", at=s.at("forty-one", off=-0.1), fontSize=100)],
                           trans=None))
    s = S[1]
    out.append(phone_scene(s, M, th.chat(s), set_="Hallway", set_props={"flicker": 0.2, "lights": 2},
                           camera={"keyframes": [{"t": 0, "zoom": 1.0}, {"t": s.dur, "zoom": 1.14, "y": "47%"}]}, trans=None))
    s = S[2]
    out.append(phone_scene(s, M, th.chat(s), set_="Hallway", set_props={"flicker": 0.3, "lights": 2}, trans=None))
    s = S[3]
    th.add(s, s.at("asked", off=0), "who is running in the stairwell??", "Priya (2D)")
    th.add(s, s.at("Nobody"), "Nobody is in the stairwell. Stay in your unit.", "Night Desk")
    out.append(phone_scene(s, M, th.chat(s, clock="12:52"), set_="Stairwell", set_props={"floor": "2", "flicker": 0.3},
                           vibrate=[s.at("Nobody")], trans=FADE))
    s = S[4]
    out.append(set_scene(s, "Stairwell", {"floor": "2", "flicker": 0.5}, [
        ov("horror/Darkness", x=0.35, y=0.45, radius=0.45, darkness=0.5, flicker=0.3),
        ov("horror/RedText", z=55, text="Wide open", style="scrawl", at=s.at("Wide", off=-0.1), fontSize=130),
        ov("horror/Vignette", amount=0.75)], camera={"preset": "pushIn", "amount": 1.0,
                                                    "shake": [{"at": s.at("Swinging"), "duration": 0.6, "amplitude": 8, "frequency": 3}]},
        trans=WHIP))
    s = S[5]
    th.add(s, s.at("remove", off=0), "@Admin can you remove Night Desk??", "Leo (3C)")
    th.add(s, s.at("I", off=0), "I already have. 3 times. It keeps coming back.", "Admin · Tom (1A)", kind="alert")
    out.append(phone_scene(s, M, th.chat(s, clock="12:55"), set_="Bedroom", trans=DIP))
    s = S[6]
    flip = s.at("forty-two", off=-0.1)
    out.append(phone_scene(s, M, th.chat(s, clock="12:56", count=41), set_="Bedroom", glitch=[flip],
                           camera={"keyframes": [{"t": 0, "zoom": 1.0}, {"t": s.dur, "zoom": 1.18, "y": "40%"}]}, trans=None,
                           extra=[ov("horror/RedText", z=55, text="42", style="flash", at=flip, fontSize=220, strobe=6)]))
    s = S[7]
    th.add(s, s.at("Fourth", off=-0.05), "Fourth floor residents, remain behind your doors. Someone is checking each unit.", "Night Desk", kind="alert")
    th.count = 42
    out.append(phone_scene(s, M, th.chat(s, clock="12:58"), set_="Bedroom", vibrate=[s.at("Fourth", off=-0.05)], tremble=3, trans=None))
    s = S[8]
    out.append(set_scene(s, "Bedroom", {"lamp": 0.15, "phoneGlow": True}, [
        nora([(0, "scared")], pose="phone", look=(0, 0.6)),
        ov("horror/Vignette", amount=0.7)], camera={"preset": "pushIn", "amount": 1.4}, trans=DIP))
    s = S[9]
    ks = [s.at("knock", nth=i, off=-0.35) for i in range(3)]
    out.append({"id": f"p{s.i:02d}", "duration": s.dur, "background": {"type": "color", "color": "#000"}, "notes": s.text,
                "transitionIn": GLITCH,
                "layers": [
                    {"type": "component", "name": "horror/Hallway", "depth": 0.3, "end": ks[1],
                     "props": {"flicker": 0.7, "figure": 1, "figureDepth": 0.85}},
                    {"type": "component", "name": "horror/Hallway", "depth": 0.3, "start": ks[1], "end": ks[2],
                     "props": {"flicker": 0.8, "figure": 1, "figureDepth": 0.6}},
                    {"type": "component", "name": "horror/Hallway", "depth": 0.3, "start": ks[2],
                     "props": {"flicker": 0.9, "figure": 1, "figureDepth": 0.38, "lights": 1}},
                    ov("horror/Flicker", strength=0.4, blackouts=[{"at": k - 0.1, "duration": 0.15} for k in ks], seed="hw"),
                    ov("horror/Vignette", amount=0.8)],
                "camera": {"preset": "pushIn", "amount": 1.2, "shake": knocks_cam(ks, 14)}})
    s = S[10]
    out.append(set_scene(s, "FrontDoor", {"hallLight": 0.6, "chain": "on", "feet": [0.2, 99]}, [
        ov("horror/Heartbeat", bpm=130, bpmTo=160), ov("horror/Vignette", amount=0.8)],
        camera={"preset": "pushIn", "amount": 1.2}, trans=None))
    s = S[11]
    th.add(s, s.at("At", off=-0.05), "At 4D now. Please open, for your safety.", "Night Desk", kind="alert")
    out.append(phone_scene(s, M, th.chat(s, clock="1:03"), set_="Bedroom", vibrate=[s.at("lit", off=-0.2)], tremble=5,
                           heartbeat={"bpm": 150}, trans=FADE))
    s = S[12]
    out.append(phone_scene(s, M, th.chat(s, clock="1:03", typing=[("4D", s.at("typing", off=-0.6), s.dur + 1)]),
                           set_="Bedroom", tremble=6, glitch=[s.at("me", off=0)], heartbeat={"bpm": 160},
                           camera={"keyframes": [{"t": 0, "zoom": 1.0}, {"t": s.dur, "zoom": 1.2, "y": "40%"}]}, trans=None))
    return out


# =========================================================================== elevator maintenance

def elevator(S):
    M = {"Maintenance": {"color": "#3a3f4a", "initials": "M"}, "Brightline Lift Services": {"color": "#4f7a73", "initials": "BL"}}
    mt = Thread("Maintenance", M, subtitle="+1 (555) 0143", day="Today 1:07 AM", clock="1:07", battery=18)
    out = []
    s = S[0]
    out.append({"id": f"p{s.i:02d}", "duration": s.dur, "notes": s.text,
                "background": {"type": "component", "name": "horror/ElevatorPanel", "depth": 1,
                               "props": {"from": 6, "to": 6, "at": 0, "floors": 10, "flicker": 0.3}},
                "layers": [ov("horror/Flicker", strength=0.5, blackouts=[{"at": s.at("lights", off=0.2), "duration": 99}], seed="el"),
                           ov("horror/Vignette", amount=0.7)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.2, "y": "30%"}, {"t": s.dur, "zoom": 1.28, "y": "30%"}],
                           "shake": [{"at": 0.2, "duration": 0.4, "amplitude": 20}]}})
    s = S[1]
    mt.add(s, s.at("So", off=0), "Hi, I'm stuck in the elevator at 120 Grant St. Between floors. Lights are out.", me=True)
    out.append(phone_scene(s, M, mt.chat(s), set_="Stairwell", set_props={"floor": "", "flicker": 0},
                           taps=[{"at": s.at("So", off=-0.3), "x": 0.88, "y": 0.95}],
                           extra=[ov("horror/Darkness", x=0.5, y=0.5, radius=0.6, darkness=0.5)], trans=DIP))
    s = S[2]
    mt.add(s, s.at("Stay", off=-0.05), "Stay calm. Press 4, then 2, then hold CLOSE.", "Maintenance")
    mt.add(s, s.at("Whatever", off=-0.05), "Whatever you do, don't look at the mirror.", "Maintenance", kind="alert")
    out.append(phone_scene(s, M, mt.chat(s, typing=[("Maintenance", 0.1, s.at("Stay", off=-0.05))]), set_="Stairwell",
                           set_props={"floor": "", "flicker": 0}, vibrate=[s.at("Stay", off=-0.05)], trans=None))
    s = S[3]
    out.append(set_scene(s, "Hallway", {"lights": 1, "flicker": 0.2}, [
        {"type": "component", "name": "horror/Stranger", "x": "78%", "y": "100%", "anchorY": 1, "width": 620, "height": 942,
         "depth": 1.1, "opacity": 0.85, "props": {"silhouette": True, "expr": "blank"}},
        nora([(0, "scared"), (s.at("behind", off=-0.3), "terrified")], x="38%", w=820, look=(0.8, 0), blink=False),
        ov("horror/Darkness", x=0.4, y=0.5, radius=0.45, darkness=0.85),
        ov("horror/Vignette", amount=0.85)], camera={"preset": "pushIn", "amount": 1.0}, trans=DIP, grade={"saturate": 0.6}))
    s = S[4]
    p4, p2, jolt = s.at("four", off=0), s.at("two", off=0), s.at("jolted", off=0)
    out.append({"id": f"p{s.i:02d}", "duration": s.dur, "notes": s.text, "transitionIn": DIP,
                "background": {"type": "component", "name": "horror/ElevatorPanel", "depth": 1,
                               "props": {"from": 6, "to": 9, "at": jolt + 0.3, "perFloor": 1.1, "floors": 10,
                                         "pressed": [{"at": p4, "floor": 4}, {"at": p2, "floor": 2}], "flicker": 0.4}},
                "layers": [ov("horror/Vignette", amount=0.7)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.15, "y": "50%"}, {"t": jolt, "zoom": 1.15, "y": "50%"},
                                         {"t": jolt + 0.6, "zoom": 1.25, "y": "28%"}],
                           "shake": [{"at": jolt, "duration": 0.5, "amplitude": 22}]}})
    s = S[5]
    mt.add(s, s.at("Good"), "Good. Keep holding CLOSE.", "Maintenance")
    mt.add(s, s.at("You'll", off=-0.05), "You'll hear someone ask to get in. Say no.", "Maintenance")
    out.append(phone_scene(s, M, mt.chat(s, clock="1:09"), set_="Stairwell", set_props={"floor": "", "flicker": 0},
                           vibrate=[s.at("Good")], trans=FADE))
    s = S[6]
    real = Thread("Brightline Lift Services", M, subtitle="Verified business", day="Today 1:10 AM", clock="1:10", battery=17)
    real.add(s, s.at("We're", off=-0.05), "We're closed until 8 AM. Your elevator shows OUT OF SERVICE.", "Brightline Lift Services")
    real.add(s, s.at("Who", off=-0.05), "Who are you talking to?", "Brightline Lift Services", kind="alert")
    out.append(phone_scene(s, M, real.chat(s), set_="Stairwell", set_props={"floor": "", "flicker": 0},
                           banners=[{"at": 0.1, "duration": 1.6, "app": "Messages", "title": "Brightline Lift Services",
                                     "text": "Building maintenance here."}], vibrate=[0.1], glitch=[s.at("Who")], trans=GLITCH))
    s = S[7]
    mt.add(s, s.at("Don't", off=-0.05), "Don't listen to them. They're the ones who want in.", "Maintenance", kind="alert")
    out.append(phone_scene(s, M, mt.chat(s, clock="1:11"), set_="Stairwell", set_props={"floor": "", "flicker": 0},
                           vibrate=[s.at("Don't", off=-0.05)], tremble=4, heartbeat={"bpm": 100, "bpmTo": 130}, trans=FADE))
    s = S[8]
    e8 = s.at("Eight")
    out.append({"id": f"p{s.i:02d}", "duration": s.dur, "notes": s.text, "transitionIn": WHIP,
                "background": {"type": "component", "name": "horror/ElevatorPanel", "depth": 1,
                               "props": {"from": 7, "to": 11, "at": e8 - 0.6, "perFloor": 0.62, "floors": 12, "flicker": 0.4}},
                "layers": [ov("horror/RedText", z=40, text="We only have 10 floors", style="neon", at=s.at("only", off=-0.2),
                              fontSize=96, strobe=6),
                           ov("horror/Vignette", amount=0.65)],
                "camera": {"keyframes": [{"t": 0, "zoom": 1.25, "y": "25%"}, {"t": s.dur, "zoom": 1.35, "y": "26%"}],
                           "shake": [{"at": s.at("Eleven"), "duration": 0.3, "amplitude": 14}]}})
    s = S[9]
    out.append(set_scene(s, "Hallway", {"lights": 1, "flicker": 0.8, "figure": 0.7, "figureDepth": 0.9}, [
        {"type": "rect", "x": "25%", "y": "50%", "width": 540, "height": 1920, "fill": "#0d0f12", "depth": 0, "z": 5,
         "keyframes": [{"t": 0, "x": "25%"}, {"t": s.at("doors"), "x": "25%"}, {"t": s.dur, "x": "-5%", "ease": "out"}]},
        {"type": "rect", "x": "75%", "y": "50%", "width": 540, "height": 1920, "fill": "#0d0f12", "depth": 0, "z": 5,
         "keyframes": [{"t": 0, "x": "75%"}, {"t": s.at("doors"), "x": "75%"}, {"t": s.dur, "x": "105%", "ease": "out"}]},
        ov("horror/Vignette", amount=0.85)], camera={"preset": "pushIn", "amount": 0.8}, trans=None))
    s = S[10]
    out.append(phone_scene(s, M, mode="lock", lock={"time": "1:13", "date": "Sunday, November 1", "notifications": [
        {"at": s.at("Run", off=-0.05), "app": "Messages", "title": "Maintenance", "text": "Run."},
        {"at": s.at("Stay", off=-0.05), "app": "Messages", "title": "Brightline Lift Services", "text": "Stay."}]},
        set_="Hallway", set_props={"lights": 1, "flicker": 0.6}, vibrate=[s.at("Run", off=-0.05), s.at("Stay", off=-0.05)],
        tremble=5, trans=FADE))
    s = S[11]
    look = s.at("looking", off=-0.2)
    out.append(set_scene(s, "Hallway", {"lights": 1, "flicker": 0.4}, [
        nora([(0, "terrified")], x="30%", w=760, look=(-0.6, 0), pose="phone"),
        {"type": "component", "name": "horror/Protagonist", "x": "76%", "y": "100%", "anchorY": 1, "width": 700, "height": 1064,
         "depth": 1.0, "opacity": 0.9, "start": s.at("mirror", off=-0.2), "enter": {"type": "fade", "duration": 0.6},
         "props": {"exprs": [{"t": 0, "e": "neutral"}, {"t": look, "e": "suspicious"}], "light": "red", "lookX": -1, "blink": False,
                   "glitch": [{"at": look, "duration": 0.3, "amount": 1}]}},
        ov("horror/Glitch", z=60, cues=[{"at": look, "duration": 0.35, "amount": 1}], seed="mir"),
        ov("horror/Vignette", amount=0.85)],
        camera={"keyframes": [{"t": 0, "zoom": 1.0, "x": "45%"}, {"t": s.dur, "zoom": 1.15, "x": "65%"}],
                "shake": [{"at": look, "duration": 0.4, "amplitude": 18}]}, trans=DIP))
    return out


# =========================================================================== roommate two rooms

def roommate(S):
    M = {"Jess": {"color": "#8f4a55", "initials": "J"}, "Mr. Abbott (landlord)": {"color": "#4a628f", "initials": "MA"}}
    dm = Thread("Jess", M, subtitle="online", day="Today 7:48 PM", clock="7:48")
    dm.add(S[0], -3, "are you home?", "Jess")
    dm.add(S[0], -2, "yeah why", me=True)
    out = []
    s = S[0]
    dm.add(s, s.at("Don't", off=-0.05), "Don't come out.", "Jess")
    dm.add(s, s.at("There's", off=-0.05), "There's someone in the living room who looks like me.", "Jess", kind="alert")
    out.append(phone_scene(s, M, dm.chat(s), set_="Bedroom", set_props={"lamp": 0.6}, vibrate=[s.at("Don't", off=-0.05)], trans=None))
    s = S[1]
    out.append(set_scene(s, "Bedroom", {"lamp": 0.6}, [
        nora([(0, "worried"), (s.at("Jess's", off=-0.1), "scared")], pose="phone", look=(0.8, 0), x="40%"),
        ov("horror/Vignette", amount=0.6)], camera={"preset": "pushIn", "amount": 0.8}, trans=DIP))
    s = S[2]
    dm.add(s, s.at("If", off=-0.05), "If you're really in your room, knock on the wall.", me=True)
    k0 = s.at("Three", off=-0.9)
    out.append(phone_scene(s, M, dm.chat(s, clock="7:49"), set_="Bedroom", set_props={"lamp": 0.6},
                           taps=[{"at": s.at("If", off=-0.3), "x": 0.88, "y": 0.95}],
                           camera={"keyframes": [{"t": 0, "zoom": 1.0}, {"t": s.dur, "zoom": 1.05}],
                                   "shake": knocks_cam([k0, k0 + 0.45, k0 + 0.9], 16)}, trans=None))
    s = S[3]
    out.append(set_scene(s, "LivingRoom", {"lamp": 0.7, "tv": "glow"}, [
        {"type": "component", "name": "horror/Stranger", "x": "50%", "y": "100%", "anchorY": 1, "width": 760, "height": 1155,
         "depth": 1.05, "props": {"silhouette": True, "expr": "smile", "talk": [[s.at("Who"), s.last()]]}},
        ov("horror/Darkness", x=0.5, y=0.5, radius=0.6, darkness=0.4), ov("horror/Vignette", amount=0.7)],
        camera={"preset": "pushIn", "amount": 0.7}, trans=DIP))
    s = S[4]
    dm.add(s, s.at("What", off=-0.05), "What did I break last week?", me=True)
    dm.add(s, s.at("Your", off=-0.05), "your blue mug", "Jess")
    out.append(phone_scene(s, M, dm.chat(s, clock="7:51", typing=[("Jess", s.at("She", off=0), s.at("Your", off=-0.05))]),
                           set_="Bedroom", set_props={"lamp": 0.5}, trans=DIP))
    s = S[5]
    out.append(set_scene(s, "FrontDoor", {"hallLight": 0.7, "feet": [0, 99]}, [
        nora([(0, "worried"), (s.at("laughed", off=-0.1), "shocked")], pose="ear", x="80%", w=620, look=(0.9, 0), flip=True, depth=1.3),
        ov("horror/Vignette", amount=0.75)], camera={"preset": "pushIn", "amount": 0.9}, trans=FADE))
    s = S[6]
    ll = Thread("Mr. Abbott (landlord)", M, subtitle="landlord", day="Today 7:53 PM", clock="7:53")
    ll.add(s, s.at("Does", off=-0.05), "Does anyone else have a key to our flat?", me=True)
    out.append(phone_scene(s, M, ll.chat(s), set_="Bedroom", set_props={"lamp": 0.4},
                           taps=[{"at": s.at("Does", off=-0.3), "x": 0.88, "y": 0.95}], trans=DIP))
    s = S[7]
    ll.add(s, s.at("Jess", off=-0.05), "Jess moved out yesterday. She handed in her keys this morning.", "Mr. Abbott (landlord)", kind="alert")
    ll.add(s, s.at("Why", off=-0.05), "Why, is someone there?", "Mr. Abbott (landlord)")
    out.append(phone_scene(s, M, ll.chat(s), set_="Bedroom", set_props={"lamp": 0.4}, vibrate=[s.at("Jess", off=-0.05)],
                           glitch=[s.at("moved", off=0.1)], tremble=3, trans=None))
    s = S[8]
    out.append(set_scene(s, "Bedroom", {"lamp": 0.1}, [
        nora([(0, "terrified")], x="50%", w=980, look=(0, 0), blink=False),
        ov("horror/Darkness", x=0.5, y=0.55, radius=0.45, darkness=0.65),
        ov("horror/Heartbeat", bpm=110, bpmTo=140)], camera={"preset": "pushIn", "amount": 1.4}, trans=DIP))
    s = S[9]
    d1 = s.at("open", off=0)
    out.append(set_scene(s, "FrontDoor", {"hallLight": 0.8, "feet": [0, 99], "handle": [{"at": d1, "duration": 1.2}], "chain": "on"}, [
        ov("horror/Flicker", strength=0.3, seed="dr"), ov("horror/Vignette", amount=0.8)],
        camera={"preset": "pushIn", "amount": 1.2, "shake": [{"at": d1, "duration": 0.4, "amplitude": 16}]}, trans=GLITCH))
    s = S[10]
    dm.add(s, s.at("Which", off=-0.05), "Which one of us are you going to let in?", "Jess", kind="alert")
    out.append(phone_scene(s, M, dm.chat(s, clock="7:56"), set_="Bedroom", set_props={"lamp": 0.1},
                           vibrate=[s.at("buzzed", off=-0.1)], tremble=5, glitch=[s.at("in", off=0.2)],
                           heartbeat={"bpm": 150}, trans=FADE,
                           camera={"keyframes": [{"t": 0, "zoom": 1.0}, {"t": s.dur, "zoom": 1.06, "y": "48%"}]}))
    return out


STRICT_HOLDS = ("horror-pinned-rules",)  # pilot: fail the build on any >3 s visual hold

EPISODES = {
    "horror-pinned-rules": pinned_rules,
    "horror-mom-two-chats": mom_two_chats,
    "horror-member-41": member_41,
    "horror-elevator-maintenance": elevator,
    "horror-roommate-two-rooms": roommate,
}
