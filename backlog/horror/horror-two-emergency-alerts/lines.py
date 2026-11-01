"""Single source of the spoken lines for horror-two-emergency-alerts (final rewrite, 2026-11-01).

Used by tts_measure.py (Kokoro on the Spark CPU, per-line, multi-voice), build.py (timeline, stats,
storyboard.json) and, through build.py's printed tables, script.md.

Entry kinds
  ("#", beat_key, heading)              section marker
  (id, spk, text, opts)                 a spoken line. opts: say (TTS text if it differs), gap (s after),
                                        cap ({tts_word: shown}), sfx [(cue, offset, gain_db)] where offset is
                                        seconds from line start, "end[+s]" or "w:<word>"; fx ("door" | "phone" |
                                        "whisper"): post-processing of the clip on the Spark (vo_fx.sh); screen
  ("~", id, seconds, opts)              timed silence (picture holds, SFX only)
"""

# speaker -> Kokoro voice, speed
VOICES = {
    "N": ("af_heart", 1.36),   # narrator, Tess Avila, first person past tense
    "T": ("af_heart", 1.12),   # Tess's own spoken words on the call (whisper fx: lowpass + -6 dB)
    "A": ("bf_emma", 1.12),    # the alert text, read flat (an in-world text-to-speech read of the banner)
    "D": ("am_michael", 1.08),  # the man: the voice at the door AND the "dispatcher" (same voice on purpose)
}
SPEAKER_NAME = {"N": "Narrator (Tess)", "T": "Tess (spoken, whisper)", "A": "Alert voice",
                "D": "The man (door voice / 'dispatcher')"}

GAP = 0.10        # breath between lines, same speaker
TURN_GAP = 0.22   # speaker change

V = [
    ("#", "B1", "B1 HOOK: every phone screams + the official order"),
    ("n1", "N", "Every phone on my floor screamed at once.",
     {"sfx": [("alert_tone", -0.12, -6)], "gap": 0.1,
      "screen": "COVER FRAME. Lock screen 2:47, alert 1 card: EMERGENCY ALERT · Lindhurst County Emergency Management · "
                "SHELTER IN PLACE. Do not open your door for anyone, including emergency services. Further instructions by alert only."}),
    ("a1", "A", "Open your door for no one. Not even emergency services.",
     {"cap": {"Not": "NOT", "even": "EVEN", "emergency": "EMERGENCY", "services.": "SERVICES."},
      "screen": "Push in on the alert 1 body; caption card NOT EVEN EMERGENCY SERVICES"}),

    ("#", "B2", "B2/B4 FALSE SAFETY + CONTRADICTION (same channel)"),
    ("n2", "N", "Nine minutes later, a second one.",
     {"sfx": [("alert_tone", 0.0, -9)], "gap": 0.1, "screen": "Lock clock 2:56; alert 2 drops on top of alert 1"}),
    ("a2", "A", "Previous alert sent in error. County staff are visiting every unit. Please let them in.",
     {"screen": "Alert 2: sender 'Lindhurst Countv Emergency Management'. A 0.3 s hairline glint runs over the v (no VO)"}),

    ("#", "B3", "B3 INTRUSION: a phone screams down the hall, then a knock"),
    ("n3", "N", "At the far end of my hall, one phone went off. Alone.",
     {"sfx": [("alert_tone_wall", "w:off.", -15)], "screen": "Hallway, far end door lit; a faint red pulse under it"}),
    ("n4", "N", "Then a knock.", {"sfx": [("knock", "end", -12)], "gap": 0.35, "screen": "Same hallway, tiny figure at the far door"}),

    ("#", "B5a", "B5 CHORUS: the floor chat (viewer proxy ignored)"),
    ("n5", "N", "The floor chat lit up.", {"sfx": [("message_pop", 0.0, -2)],
     "screen": "Chat 'Ashby Tower · Floor 11', 12 members"}),
    ("n6", "N", "Raf, end of the hall: County jackets. Super polite. They asked how many live here.",
     {"sfx": [("message_pop", "w:County", -2)], "screen": "Raf: 'county jackets. super polite. they asked how many live here'"}),
    ("n7", "N", "Ines, next door: So which one is real?",
     {"sfx": [("message_pop", "w:So", -2)], "screen": "Ines: 'so which one is real??'"}),
    ("n8", "N", "Lorna: The second, obviously. The first was a glitch.",
     {"sfx": [("message_pop", "w:The", -2)], "screen": "Lorna: 'the second obviously. first was a glitch'"}),
    ("n9", "N", "I typed: Then why did the first one say not even emergency services?",
     {"sfx": [("message_send", "end", -3)], "screen": "Me: 'then why did the first one say not even emergency services?'"}),
    ("n10", "N", "Nobody answered.", {"gap": 0.3, "screen": "Typing dots start under Lorna, then stop"}),

    ("#", "B4b", "B4 COUNTABLE PROOF: the sender line"),
    ("n11", "N", "So I checked who sent the second one.", {"sfx": [("click", 0.1, -8)], "screen": "Alert 2 details"}),
    ("n12", "N", "Not County. C, O, U, N, T, V.",
     {"say": "Not County. C. O. U. N. T. V.",
      "sfx": [("tick", "w:C.", -6), ("tick", "w:O.", -6), ("tick", "w:U.", -6), ("tick", "w:N.", -6), ("tick", "w:T.", -6),
              ("tick", "w:V.", -2)],
      "cap": {"C.": "C,", "O.": "O,", "U.": "U,", "N.": "N,", "T.": "T,", "V.": "V."},
      "screen": "Full-frame header card: 'Lindhurst Countv'; letters light C·O·U·N·T·V on each tick; the v gets a red ring"}),
    ("n13", "N", "The open-up alert was fake.", {"sfx": [("stinger", 0.0, -10)], "gap": 0.2, "screen": "Card: 'PLEASE LET THEM IN' stamped FAKE"}),

    ("#", "B5b", "B5 LADDER: each door's phone screams first, then the knock, then the same post"),
    ("n14", "N", "Then another phone went off, closer. Knock.",
     {"sfx": [("alert_tone_wall", "w:off,", -11), ("knock", "w:Knock.", -9)], "screen": "Hallway, figure nearer; pulse under door 2"}),
    ("n15", "N", "Raf posted again. All done. Painless. Open up when they knock.",
     {"sfx": [("message_pop", "w:All", -2)], "screen": "Raf: 'All done. Painless. Open up when they knock.'"}),
    ("n16", "N", "Lorna's phone was next, three doors down. Knock.",
     {"sfx": [("alert_tone_wall", 0.0, -8), ("knock", "w:Knock.", -7)], "screen": "Hallway, figure at door 3"}),
    ("n17", "N", "Then Lorna. All done. Painless. Open up when they knock.",
     {"sfx": [("message_pop", "w:All", -2)], "screen": "Lorna: identical bubble, stacked under Raf's"}),
    ("n18", "N", "Word for word. Even the full stop.",
     {"sfx": [("stinger", "end", -10)], "gap": 0.2, "screen": "ECU: the two bubbles aligned, both full stops ringed red"}),

    ("#", "B6", "B6 ISOLATION: only the enemy's channels still work"),
    ("n19", "N", "I called my sister, Josie. Call failed. My texts sat on sending.",
     {"sfx": [("click", 0.0, -8), ("glitch", "w:failed.", -14)],
      "screen": "Outgoing call 'Josie' -> 'Call Failed'; SMS 'pick up pls' with grey 'Sending...'"}),
    ("n20", "N", "Only two things still worked. The floor chat, and the alerts.",
     {"screen": "Home screen: everything greyed except the chat icon and the red alert icon"}),

    ("#", "B5c", "B5 LONE ALLY SILENCED (closest rung)"),
    ("n21", "N", "Then Ines posted: Don't open. They're not",
     {"gap": 0.05, "sfx": [("message_pop", "w:Don't", -2)], "screen": "Ines: 'don't open. they're not'  (bubble ends mid-line)"}),
    ("n22", "N", "That was the whole message.", {"gap": 0.25, "screen": "Hold on the cut-off bubble"}),
    ("n23", "N", "Then her phone screamed, right through my wall.",
     {"sfx": [("alert_tone_wall", "w:screamed,", -3), ("knock", "end+0.15", -2), ("impact", "end+0.15", -10)],
      "screen": "Living-room wall; the framed print rattles on the knock next door"}),
    ("n24", "N", "A minute later, Ines posted. All done. Painless. Open up when they knock.",
     {"sfx": [("message_pop", "w:All", -2)], "screen": "Third identical bubble, from Ines"}),

    ("#", "B7", "B7 LULL + TIMED SILENCE"),
    ("n25", "N", "Then the knocking stopped.", {"gap": 0.0}),
    ("~", "q1", 3.0, {"sfx": [("breath", 0.4, -16), ("door_creak", 1.7, -20)], "mute_music": True,
                      "screen": "Silence 3 s: Tess on the floor, back to the door, phone glow; music hard-muted"}),

    ("#", "B8", "B8 MIDPOINT TURN: the alerts were choosing doors"),
    ("n26", "N", "Every door they knocked, the phone behind it screamed first.",
     {"screen": "Floor plan diagram: doors light red in order 1, 2, 3, then the knock icon follows each"}),
    ("n27", "N", "They weren't warning the building. They were picking doors.", {}),
    ("n28", "N", "And mine hadn't screamed yet.",
     {"sfx": [("stinger", "w:yet.", -4), ("glitch", "w:yet.", -10)], "gap": 0.3,
      "screen": "THE ONLY FULL-FRAME COLOUR FLASH: amber on 'yet', then her door lights red on the plan"}),
    ("n29", "N", "I held the power button. It wouldn't turn off.",
     {"sfx": [("click", 0.3, -8), ("glitch", "w:turn", -12)], "screen": "Power-off slider glitches back to the lock screen"}),

    ("#", "B9", "B9 PEAK CONTACT: my phone screams, then my door"),
    ("n30", "N", "Then mine screamed.", {"sfx": [("alert_tone", 0.0, -1)], "gap": 0.1,
     "screen": "Lock screen, alert 3 lands, phone shakes"}),
    ("n31", "N", "Alert three. Spelled right.", {"gap": 0.1, "screen": "Sender line 'Lindhurst County' gets a green underline under the y"}),
    ("a3", "A", "Previous alerts sent in error. Admit county staff.",
     {"screen": "Alert 3 body + footer 'Questions? Call 555-0148'"}),
    ("n32", "N", "Three slow knocks. My door.", {"sfx": [("knock3_slow", 0.0, -1)], "screen": "FrontDoor, three knocks, feet shadow"}),
    ("n33", "N", "Now the real sender was telling me to open.", {}),
    ("d1", "D", "Ms. Avila? County. Your sister Josie called us. She's worried sick.",
     {"fx": "door", "say": "Miss Avila? County. Your sister Josie called us. She's worried sick.",
      "screen": "FrontDoor, handle still; warm voice through the wood"}),
    ("n34", "N", "My hand was already sliding the chain off.",
     {"sfx": [("chain_strain", 0.2, -10)], "screen": "ECU: her hand slides the chain halfway along the track"}),
    ("n35", "N", "Then I remembered. My call to Josie never went through.",
     {"sfx": [("stinger", "w:never", -8)], "screen": "Insert: the 'Call Failed' screen again (1 s)"}),
    ("n36", "N", "I looked through the peephole.", {"gap": 0.1}),
    ("n37", "N", "He was pressing a phone flat to the glass. On it was my lock screen.",
     {"gap": 0.0, "screen": "Peephole POV: a man in a cap, backlit; a phone pressed to the lens"}),
    ("~", "q2", 4.0, {"sfx": [("heartbeat", 0.8, -6)], "mute_music": True,
                      "screen": "SCARIEST IMAGE, held 4 s, no VO: her own lock screen inside the lens. Same wallpaper, the three red alerts, 3:09 ticking with hers"}),
    ("n38", "N", "My wallpaper. My three alerts. Behind him, every door on my floor stood open. Dark.",
     {"screen": "Pull back inside the lens: behind him the hall, every door open, black inside"}),
    ("n39", "N", "I put the chain back on.", {"sfx": [("click", "end", -4)]}),

    ("#", "B10", "B10 LIFELINE UNDER A CLOCK: the only call that rings"),
    ("n40", "N", "Alert three had a number at the bottom. I called it.",
     {"sfx": [("click", "end", -8)], "screen": "Footer '555-0148' tapped; outgoing call screen"}),
    ("n41", "N", "All night, nothing had connected. This one rang.", {"sfx": [("phone_buzz", "w:rang.", -14)]}),
    ("n42", "N", "Then a key turned in my lock. The door swung in, four inches, and hit the chain.",
     {"sfx": [("click", "w:turned", -4), ("door_creak", "w:swung", -8), ("chain_strain", "w:hit", -2), ("impact", "w:hit", -8)],
      "screen": "FrontDoor from inside: door open to the chain, a strip of hall light; the chain shudders"}),
    ("d2", "D", "Lindhurst County. Is your door shut?", {"fx": "phone", "sfx": [("click", -0.15, -10)],
     "screen": "Call screen 'Lindhurst County EM · 00:01' running"}),
    ("t1", "T", "Did you send the alert with the v?", {"fx": "whisper", "screen": "Tess MCU, pose ear, whisper"}),
    ("d3", "D", "No, ma'am. That one's fake. Good catch.", {"fx": "phone", "sfx": [("chain_strain", "end", -8)]}),
    ("t2", "T", "And the one telling me to let them in?", {"fx": "whisper"}),
    ("d4", "D", "That one's ours. Our staff are outside your door.", {"fx": "phone"}),
    ("n43", "N", "The chain jumped. The screws were coming out of the frame.",
     {"sfx": [("chain_strain", 0.0, -1), ("impact", 0.05, -6)], "screen": "ECU: chain plate, screws backing out"}),
    ("d5", "D", "Quickly now. Your name, your unit, and is anyone with you?", {"fx": "phone"}),
    ("t3", "T", "Tess Avila. Eleven F. Just me.", {"fx": "whisper", "say": "Tess Avila. Eleven F. Just me.",
     "cap": {"Eleven": "11F.", "F.": ""}}),

    ("#", "B11", "B11 TRUTH TWIST: the dispatcher and the door are one voice"),
    ("d6", "D", "Thank you, Tess.", {"fx": "phone+door", "gap": 0.2,
     "screen": "Split: the call screen and the four-inch gap; the same words arrive in both"}),
    ("n44", "N", "In my ear, and through the gap in my door. The same voice.", {"sfx": [("stinger", "end", -6)]}),
    ("n45", "N", "The v was never a mistake.", {"gap": 0.2}),

    ("#", "B12", "B12 CLIFFHANGER + BOOKEND"),
    ("n46", "N", "My phone lit up in my hand.", {"sfx": [("alert_tone", "end", -1)], "gap": 0.35,
     "screen": "BOOKEND of the cover frame: same lock screen framing"}),
    ("a4", "A", "Tess Avila, eleven F. One occupant. Open the door.",
     {"cap": {"eleven": "11F.", "F.": ""}, "gap": 0.0,
      "screen": "Alert 4 card: TESS AVILA · 11F · ONE OCCUPANT. Open the door. Sender spelled right"}),
    ("~", "q3", 0.9, {"mute_music": True, "screen": "Hold on alert 4, then hard cut to black (no card, no tail)"}),
]


def spoken():
    return [e for e in V if e[0] not in ("#", "~")]
