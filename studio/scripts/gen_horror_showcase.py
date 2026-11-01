import json, sys

FULL = {"type": "component", "depth": 0}
def ov(name, z=50, **props):
    return {"type": "component", "name": name, "depth": 0, "z": z, "props": props}

members = {
    "Mgr. Okafor": {"color": "#4f7a73", "initials": "MO"},
    "Unit 5C": {"color": "#8f4a55", "initials": "5C"},
    "Dev (4A)": {"color": "#6b7a4a", "initials": "D"},
}

scenes = []
# 1 lock screen, notifications
scenes.append({
    "id": "lock", "duration": 2.2,
    "background": {"type": "color", "color": "#0b0d12"},
    "layers": [
        {"type": "component", "name": "horror/Bedroom", "depth": 0.2, "blur": 10, "opacity": 0.7, "props": {"lamp": 0}},
        {"type": "component", "name": "horror/HandPhone", "id": "hand", "props": {
            "phoneWidth": 0.66, "cy": 0.585, "tilt": -4, "tremble": 1.5,
            "phone": {"mode": "lock", "lock": {"time": "2:09", "date": "Tuesday, March 3", "notifications": [
                {"at": 0.35, "app": "Residents", "title": "Building 7 Residents", "text": "Mgr. Okafor: Nobody from management is doing door checks tonight."},
                {"at": 1.15, "app": "Residents", "title": "Building 7 Residents", "text": "Unit 5C: someone is knocking on every door on 5"}]},
                "vibrate": [{"at": 0.35, "duration": 0.4}, {"at": 1.15, "duration": 0.4}]}}},
        ov("horror/Vignette", amount=0.75),
    ],
    "camera": {"preset": "pushIn", "amount": 0.6},
    "sfx": [{"src": "test/pop.wav", "at": 0.35, "volume": 0.5}, {"src": "test/pop.wav", "at": 1.15, "volume": 0.5}],
})
# 2 group chat
chat = {
    "title": "Building 7 Residents", "count": 48, "unread": 9, "unreadFrom": 0, "dayLabel": "Today 2:09 AM",
    "messages": [
        {"from": "Mgr. Okafor", "text": "Reminder: management is NOT doing door checks tonight.", "at": -1},
        {"from": "Unit 5C", "text": "someone just knocked on mine. said he was maintenance", "at": 0.3},
        {"from": "Unit 5C", "text": "he knew my name", "at": 1.55},
        {"me": True, "text": "what does he look like??", "at": 2.15},
        {"from": "Unit 5C", "kind": "alert", "text": "grey cardigan. he's taking the stairs up", "at": 3.2},
    ],
    "typing": [{"from": "Unit 5C", "at": 0.85, "until": 1.55}, {"from": "Unit 5C", "at": 2.5, "until": 3.2}],
}
scenes.append({
    "id": "chat", "duration": 3.8,
    "transitionIn": {"type": "fade", "duration": 0.25},
    "background": {"type": "color", "color": "#0b0d12"},
    "layers": [
        {"type": "component", "name": "horror/LivingRoom", "depth": 0.2, "blur": 10, "opacity": 0.6, "props": {"lamp": 0.3}},
        {"type": "component", "name": "horror/HandPhone", "props": {
            "phoneWidth": 0.68, "cy": 0.585, "tilt": -2, "tremble": 2.5,
            "taps": [{"at": 2.05, "x": 0.88, "y": 0.95}],
            "phone": {"members": members, "mode": "chat", "chat": chat, "vibrate": [{"at": 3.2, "duration": 0.35}]}}},
        ov("horror/Vignette", amount=0.7),
    ],
    "camera": {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": 3.0, "zoom": 1.03}, {"t": 3.3, "zoom": 1.08, "ease": "out"}],
               "shake": [{"at": 3.2, "duration": 0.35, "amplitude": 14}]},
    "sfx": [{"src": "test/pop.wav", "at": t, "volume": 0.45} for t in (0.3, 1.55, 2.15, 3.2)],
})
# 3 living room reaction
scenes.append({
    "id": "react", "duration": 1.8,
    "background": {"type": "component", "name": "horror/LivingRoom", "props": {"lamp": 0.5, "tv": "off"}},
    "layers": [
        {"type": "component", "name": "horror/Protagonist", "x": "50%", "y": "100%", "anchorY": 1, "width": 860, "height": 1307,
         "props": {"pose": "phone", "exprs": [{"t": 0, "e": "worried"}, {"t": 0.95, "e": "scared"}], "talk": [[0.15, 0.85]], "lookY": 0.6}},
        ov("horror/Darkness", x=0.5, y=0.62, radius=0.5, darkness=0.55),
        ov("horror/Vignette", amount=0.6),
    ],
    "camera": {"preset": "pushIn", "amount": 1.2},
    "grade": {"saturate": 0.85, "brightness": 0.95},
})
# 4 front door knocks
scenes.append({
    "id": "door", "duration": 2.0,
    "transitionIn": {"type": "cut"},
    "background": {"type": "component", "name": "horror/FrontDoor", "depth": 0.3, "props": {"knocks": [0.35, 0.55, 0.75], "feet": [1.0, 9], "hallLight": 0.9, "chain": "on", "handle": [{"at": 1.3, "duration": 0.6}]}},
    "layers": [
        {"type": "component", "name": "horror/Protagonist", "x": "88%", "y": "100%", "anchorY": 1, "width": 560, "height": 851, "depth": 1.3, "flipX": True,
         "props": {"exprs": [{"t": 0, "e": "scared"}, {"t": 0.36, "e": "shocked"}], "lookX": 0.9, "blink": False}},
        ov("horror/Vignette", amount=0.8),
    ],
    "camera": {"keyframes": [{"t": 0, "zoom": 1.05, "x": "50%", "y": "50%"}, {"t": 2, "zoom": 1.16, "x": "50%", "y": "46%"}],
               "shake": [{"at": a, "duration": 0.16, "amplitude": 20} for a in (0.35, 0.55, 0.75)]},
    "sfx": [{"src": "test/impact.wav", "at": a, "volume": 0.8} for a in (0.35, 0.55, 0.75)],
})
# 5 peephole
scenes.append({
    "id": "peephole", "duration": 2.0,
    "transitionIn": {"type": "dipBlack", "duration": 0.3},
    "background": {"type": "color", "color": "#050506"},
    "layers": [
        {"type": "component", "name": "horror/Peephole", "depth": 0, "props": {
            "figure": "neighbour", "exprs": [{"t": 0, "e": "smile"}, {"t": 1.05, "e": "grin"}], "lean": 0.45, "flicker": 0.35,
            "lookX": 0, "lookY": 0.1, "talk": [[0.3, 0.9]], "glitch": [{"at": 1.0, "duration": 0.18, "amount": 0.9}]}},
        ov("horror/Flicker", strength=0.35, seed="pp"),
    ],
    "camera": {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": 2.0, "zoom": 1.1}], "shake": [{"at": 1.0, "duration": 0.25, "amplitude": 16}]},
    "sfx": [{"src": "test/glitch.wav", "at": 1.0, "volume": 0.6}],
})
# 6 hallway lights go out, figure closer
scenes.append({
    "id": "hallway", "duration": 1.6,
    "transitionIn": {"type": "glitch", "duration": 0.3},
    "background": {"type": "color", "color": "#000"},
    "layers": [
        {"type": "component", "name": "horror/Hallway", "end": 0.9, "depth": 0.3, "props": {"flicker": 0.8, "figure": 1, "figureDepth": 0.82}},
        {"type": "component", "name": "horror/Hallway", "start": 0.9, "depth": 0.3, "props": {"flicker": 0.9, "figure": 1, "figureDepth": 0.5, "lights": 2}},
        ov("horror/Flicker", strength=0.4, blackouts=[{"at": 0.78, "duration": 0.22}], seed="hw"),
        ov("horror/Vignette", amount=0.8),
    ],
    "camera": {"preset": "pushIn", "amount": 1.5},
})
# 7 elevator panel counts up
scenes.append({
    "id": "elevator", "duration": 1.8,
    "transitionIn": {"type": "whip", "duration": 0.3, "direction": "up"},
    "background": {"type": "component", "name": "horror/ElevatorPanel", "depth": 1, "props": {"from": 2, "to": 7, "at": 0.05, "perFloor": 0.24, "floors": 12}},
    "layers": [
        {"type": "component", "name": "horror/RedText", "depth": 0, "z": 40, "props": {"text": "Nobody pressed 7", "style": "neon", "at": 1.0, "fontSize": 120, "strobe": 8}},
        ov("horror/Vignette", amount=0.65),
    ],
    "camera": {"keyframes": [{"t": 0, "zoom": 1.25, "y": "25%"}, {"t": 1.8, "zoom": 1.32, "y": "26%"}], "shake": [{"at": 1.0, "duration": 0.3, "amplitude": 12}]},
    "sfx": [{"src": "test/whoosh.wav", "at": 0, "volume": 0.4}, {"src": "test/impact.wav", "at": 1.0, "volume": 0.6}],
})
# 8 stairwell: neighbour climbing, heartbeat
scenes.append({
    "id": "stairs", "duration": 1.2,
    "background": {"type": "component", "name": "horror/Stairwell", "depth": 0.3, "props": {"floor": "7", "flicker": 0.6}},
    "layers": [
        {"type": "component", "name": "horror/Neighbour", "x": "62%", "y": "100%", "anchorY": 1, "width": 760, "height": 1155, "depth": 1.1,
         "keyframes": [{"t": 0, "y": "112%"}, {"t": 1.2, "y": "100%", "ease": "out"}],
         "props": {"expr": "blank", "lookX": -0.4, "lookY": -0.3, "light": "red"}},
        ov("horror/Heartbeat", bpm=110),
        ov("horror/Flicker", strength=0.3, seed="st"),
    ],
    "camera": {"preset": "pushIn", "amount": 1.0},
})
# 9 incoming call
scenes.append({
    "id": "call", "duration": 1.6,
    "transitionIn": {"type": "cut"},
    "background": {"type": "color", "color": "#0b0d12"},
    "layers": [
        {"type": "component", "name": "horror/Bedroom", "depth": 0.2, "blur": 10, "opacity": 0.6, "props": {"lamp": 0}},
        {"type": "component", "name": "horror/HandPhone", "props": {
            "phoneWidth": 0.66, "cy": 0.585, "tilt": 3, "tremble": 7, "side": "right",
            "glitch": [{"at": 1.35, "duration": 0.2, "amount": 1}],
            "phone": {"members": members, "mode": "call", "call": {"name": "Unit 5C", "sub": "Building 7 · mobile", "at": 0}, "vibrate": [{"at": 0, "duration": 1.6, "amount": 0.7}]}}},
        ov("horror/Heartbeat", bpm=120, bpmTo=160),
        ov("horror/Glitch", z=60, cues=[{"at": 1.35, "duration": 0.2, "amount": 1}], seed="call"),
    ],
    "camera": {"preset": "pushIn", "amount": 0.8},
    "sfx": [{"src": "test/glitch.wav", "at": 1.35, "volume": 0.6}],
})
# 10 bedroom: feature phone lights up
scenes.append({
    "id": "bedroom", "duration": 2.0,
    "transitionIn": {"type": "dipBlack", "duration": 0.3},
    "background": {"type": "component", "name": "horror/Bedroom", "depth": 0.25, "props": {"lamp": 0, "wardrobeOpen": 0.35, "rain": True}},
    "layers": [
        {"type": "component", "name": "horror/Protagonist", "x": "30%", "y": "100%", "anchorY": 1, "width": 640, "height": 973,
         "props": {"exprs": [{"t": 0, "e": "scared"}, {"t": 1.0, "e": "terrified"}], "pose": "cover", "lookX": 0.8, "glitch": [{"at": 1.0, "duration": 0.22}]}},
        {"type": "component", "name": "horror/FeaturePhone", "x": "74%", "y": "63%", "width": 440, "height": 950, "rotate": 8, "depth": 1.2,
         "props": {"sms": {"from": "UNKNOWN", "text": "check your wardrobe", "at": 0.15, "cps": 16}, "vibrate": [{"at": 0.0, "duration": 0.5}], "clock": "02:17", "glitch": [{"at": 1.0, "duration": 0.22}]}},
        ov("horror/Darkness", x=0.72, y=0.5, radius=0.55, darkness=0.6, color="rgba(160,190,150,0.16)"),
        ov("horror/RedText", z=55, text="Don't turn around", style="flash", at=1.05, fontSize=140, strobe=10),
        ov("horror/Glitch", z=60, cues=[{"at": 1.0, "duration": 0.25, "amount": 1}], seed="bd"),
        ov("horror/Vignette", amount=0.8),
    ],
    "camera": {"preset": "pushIn", "amount": 1.0, "shake": [{"at": 1.0, "duration": 0.4, "amplitude": 24}]},
    "sfx": [{"src": "test/impact.wav", "at": 1.0, "volume": 0.9}],
})

# narration -> word timings (burned-in captions; no TTS in the showcase)
lines = [
    (0.2, 2.0, "At 2 a.m. my building chat would not stop buzzing."),
    (2.35, 5.9, "Management swore nobody was doing door checks. Then 5C said the man knew her name."),
    (6.15, 7.7, "Grey cardigan. That's Mr. Hale from 6B."),
    (7.95, 9.7, "Except Mr. Hale moved out in June."),
    (9.95, 11.7, "And he was smiling at my peephole."),
    (11.95, 13.3, "Then the hallway lights died."),
    (13.55, 15.1, "The elevator climbed to my floor."),
    (15.3, 16.25, "Nobody had pressed it."),
    (16.5, 17.85, "Then 5C called me."),
    (18.15, 19.8, "And my old burner phone lit up."),
]
words = []
for a, b, text in lines:
    ws = text.split()
    total = sum(len(w) + 2 for w in ws)
    t = a
    for w in ws:
        d = (b - a) * (len(w) + 2) / total
        words.append({"text": w, "start": round(t, 3), "end": round(t + d * 0.92, 3)})
        t += d

sb = {
    "version": 1, "id": "horror-showcase", "title": "B4 horror kit showcase (20s, 9:16)", "format": "9:16", "fps": 30,
    "scenes": scenes,
    "captions": {"words": words, "maxWords": 3, "maxChars": 16, "style": {
        "font": "display", "fontSize": 76, "color": "#ffffff", "highlight": "#ff4b55", "highlightMode": "color",
        "strokeWidth": 12, "uppercase": False, "y": 0.15}},
    "overlays": {"grain": 0.5, "vignette": 0.0, "fadeIn": 0.2, "fadeOut": 0.35},
}
dur = sum(s["duration"] for s in scenes)
assert abs(dur - 20.0) < 1e-6, dur
json.dump(sb, open(sys.argv[1], "w"), indent=1)
print("ok", dur, len(words), "words")
