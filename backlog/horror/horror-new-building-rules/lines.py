"""Single source of the spoken lines for horror-new-building-rules (2 parts).

Used by tts_measure.py (Kokoro on the Spark CPU) and build.py (timeline, script.md tables, pacing
stats, storyboard_p1.json / storyboard_p2.json).

Entry kinds (per part list P1 / P2)
  ("#", beat_key, heading)          section marker (beat tag used in script.md)
  (id, text, opts)                  a spoken line. text = what the captions show (digits allowed);
                                    opts: say  (TTS text: numbers and unit codes spelled out, no 'lol')
                                          sfx offsets: seconds from line start, 'end', or '@k' (caption word k)
                                          gap  (s of silence after the line, default GAP)
                                          emph (caption words drawn in the highlight colour)
                                          sfx  [(cue, offset_s_from_line_start | 'end', gain_db)]
                                          vox  (voice gain dB for this line; Kokoro has no whisper, so
                                                quiet lines are speed 1.0-1.1 plus vox -6)
                                          speed (override the part speed for this line)
  ("~", id, seconds, opts)          timed silence (picture holds, SFX only); opts: sfx, music_stop
"""

VOICE = "af_heart"      # June, narrator; she voices every chat line and the voice at the door
SPEED = 1.30            # same as the shipped pilot (episodes/horror-pinned-rules)
GAP = 0.16              # breath between lines
END_CARD = 2.3          # seconds of end card after the last cut

P1 = [
    ("#", "B1", "B1 HOOK: the authority asks, the note forbids"),
    ("a01", "At 5:12, the building office asked everyone to reply with their unit number.",
     {"say": "At five twelve, the building office asked everyone to reply with their unit number.",
      "emph": ["unit", "number."], "sfx": [("notify", 0.0, -4)], "gap": 0.12}),
    ("a02", "The last tenant's note, taped under my sink, said never do that.",
     {"emph": ["never"], "gap": 0.1}),
    ("a03", "Rule one. Never give anyone your unit number. Not even the building.",
     {"emph": ["Never", "Not", "even"], "sfx": [("stinger", 0.05, -10)], "gap": 0.2}),

    ("#", "B4", "B4 SECOND CHANNEL: there is no office"),
    ("a04", "My neighbor Odette, 3B: we don't have a building office.",
     {"say": "My neighbor Odette, three-B: we don't have a building office.",
      "emph": ["don't"], "sfx": [("message_pop", 0.2, -2), ("glitch", "end", -6)]}),
    ("a05", "So who's asking?", {"emph": ["who's"], "gap": 0.28}),

    ("#", "B2", "B2 THE NOTE: three more rules, the bottom torn off"),
    ("a06", "Two. No stairs after midnight.", {"emph": ["stairs"], "sfx": [("tick", 0.0, -6)], "gap": 0.1}),
    ("a07", "Three. If your hall light goes out, stay inside until sunrise.",
     {"emph": ["light", "sunrise."], "sfx": [("tick", 0.0, -6)], "gap": 0.1}),
    ("a08", "Four. If someone you know asks your unit, it isn't them.",
     {"emph": ["isn't", "them."], "sfx": [("tick", 0.0, -6)], "gap": 0.1}),
    ("a09", "The rest was torn off.", {"emph": ["torn"], "sfx": [("click", 0.0, -8)], "gap": 0.24}),

    ("#", "B5a", "CHORUS + LEAK: the joker heads for the stairs"),
    ("a10", "Dale from 8A said he'd take the stairs and find this office.",
     {"say": "Dale from eight-A said he'd take the stairs and find this office.",
      "emph": ["stairs"], "sfx": [("message_pop", 0.0, -2)]}),
    ("a11", "The office answered in four seconds.", {"emph": ["four", "seconds."], "sfx": [("typing", 0.0, -8)]}),
    ("a12", "Dale. Your lease renews in eleven days. The stairs are fine.",
     {"emph": ["eleven", "fine."], "sfx": [("message_pop", 0.0, 0), ("stinger", 0.1, -8)]}),
    ("a13", "An office we don't have knew his lease date. And wanted him on the stairs.",
     {"emph": ["knew", "stairs."], "gap": 0.2}),

    ("#", "B6p", "COUNTABLE PLANT: four lamps"),
    ("a14", "Through my peephole, four doors down the hall. Four little amber lights.",
     {"emph": ["Four", "amber"], "gap": 0.22}),

    ("#", "B8", "B8 MIDPOINT: it knows about the note"),
    ("a15", "At 5:25, the office posted again.",
     {"say": "At five twenty-five, the office posted again.", "sfx": [("notify", 0.0, -4)]}),
    ("a16", "Reminder. The note under the sink is out of date.",
     {"emph": ["note", "sink"], "sfx": [("message_pop", 0.0, -2)]}),
    ("a17", "Nobody else had a note. It meant me.",
     {"emph": ["me."], "sfx": [("stinger", "end", -6)], "gap": 0.2}),
    ("a18", "Odette: nobody answer it.", {"emph": ["nobody"], "sfx": [("message_pop", 0.0, -2)]}),

    ("#", "B5", "B5 ROLL-CALL LADDER: each reply costs a light, the knocking walks closer"),
    ("a19", "Mrs. Kowal answered anyway. 7A. Sorry. I like rules.",
     {"say": "Mrs. Kowal answered anyway. Seven-A. Sorry. I like rules.",
      "emph": ["anyway."], "sfx": [("message_pop", 0.9, -2)]}),
    ("a20", "In the hall, the light over her door went out.",
     {"emph": ["out."], "sfx": [("click", "end", 0)], "gap": 0.24}),
    ("a21", "Then 7B. 7D. 7E. Like a roll call.",
     {"say": "Then seven-B. Seven-D. Seven-E. Like a roll call.", "emph": ["7B.", "7D.", "7E."]}),
    ("a22", "Four replies. Four lights out.", {"emph": ["Four"], "gap": 0.14}),
    ("a23", "Each time, the knocking moved one door closer.",
     {"emph": ["closer."], "sfx": [("knock3_slow", "end", -10)], "gap": 0.9}),

    ("#", "B6", "B6 VOICE SWAP + CASUALTY PROOF: the dark units post calmly"),
    ("a24", "Then Mrs. Kowal posted again. Capital letters. Full stops.",
     {"emph": ["Capital"], "sfx": [("message_pop", 0.0, -2)]}),
    ("a25", "June, please reply. It's fine.", {"emph": ["please"], "vox": -2}),
    ("a26", "7B, word for word.", {"say": "Seven-B, word for word.", "emph": ["word"],
                                   "sfx": [("message_pop", 0.0, -2)], "gap": 0.22}),

    ("#", "B9", "B9 PEAK IMAGE (P1): the open door"),
    ("a27", "Mrs. Kowal's door stood open a crack. Dark inside.",
     {"emph": ["open"], "sfx": [("door_creak", 0.2, -10)], "gap": 0.1}),
    ("~", "h1", 1.3, {"sfx": [("heartbeat_slow", 0.0, -8)]}),

    ("#", "B11", "B11 TARGET BY ELIMINATION + THE INSIDE THREAT"),
    ("a28", "My phone buzzed. A private message from the office.",
     {"emph": ["private"], "sfx": [("phone_buzz", 0.0, 0)]}),
    ("a29", "Every unit on seven has replied except one.", {"emph": ["except", "one."], "gap": 0.35}),
    ("a30", "Behind me, under the locked spare room door, a light came on.",
     {"emph": ["light"], "sfx": [("click", "end", -6)], "gap": 0.3}),

    ("#", "B12", "B12 CLIFF: three knocks, cut on the third"),
    ("a31", "I put my phone face down and held the chain.", {"speed": 1.15, "vox": -4, "gap": 0.1}),
    ("~", "q1", 0.75, {"music_stop": True}),
    ("~", "k1", 0.45, {"sfx": [("knock", 0.0, 0)]}),
    ("a32", "One.", {"speed": 1.0, "vox": -6, "gap": 0.1}),
    ("~", "k2", 0.45, {"sfx": [("knock", 0.0, 0)]}),
    ("a33", "Two.", {"speed": 1.0, "vox": -6, "gap": 0.0}),
    ("~", "k3", 0.62, {"sfx": [("knock", 0.0, 2)], "cut": True}),
]

P2 = [
    ("#", "P2-1", "P2 COLD HOOK: a trusted voice asks the forbidden question"),
    ("b01", "Three knocks. Then my neighbor Odette's voice through the door.",
     {"emph": ["Odette's"], "sfx": [("knock", 0.0, 0)], "gap": 0.1}),
    ("b02", "June? Which unit is this?", {"emph": ["Which", "unit"], "speed": 1.15, "gap": 0.22}),
    ("b04", "I texted her.", {"sfx": [("message_send", "end", -2)], "gap": 0.5}),
    ("b05", "Bathtub. Floor 3. That's not me.",
     {"say": "Bathtub. Floor three. That's not me.", "emph": ["not", "me."], "sfx": [("message_pop", 0.0, 0)], "gap": 0.1}),
    ("b06", "Typing it marks you. Saying it opens.", {"emph": ["marks", "opens."], "gap": 0.2}),

    ("#", "P2-1b", "PREMISE FOR COLD VIEWERS: the mechanic and rule four"),
    ("b07", "Four neighbors gave the building office their unit tonight. All four hall lights went out.",
     {"emph": ["Four", "out."]}),
    ("b03", "And the note under my sink says, if someone you know asks for your unit, it isn't them.",
     {"emph": ["isn't", "them."], "gap": 0.2}),

    ("#", "P2-3", "FAST LADDER + PART 1 PLANT PAID: Dale and the stairs"),
    ("b08", "Then the voice changed. Dale, from 8A.", {"say": "Then the voice changed. Dale, from eight-A.",
                                                     "emph": ["Dale,"], "sfx": [("knock3", 0.0, -2)]}),
    ("b09", "June, it's Dale. The stairs don't go down anymore. Let me in.",
     {"emph": ["don't", "down"], "speed": 1.2}),
    ("b10", "Dale had posted from the stairwell. Floor six. Floor six. Floor six.",
     {"emph": ["six."], "sfx": [("message_pop", 0.0, -4)]}),
    ("b11", "Rule two. No stairs after midnight.", {"emph": ["stairs"], "sfx": [("tick", 0.0, -6)], "gap": 0.3}),

    ("#", "P2-4", "B7 LULL + PLANT: the locked spare room"),
    ("b12", "Then the hall went quiet. Behind me, the spare room light was on.", {"emph": ["light"]}),
    ("b13", "The agent said that room stays locked. Owner's storage.", {"emph": ["locked."], "gap": 0.24}),

    ("#", "P2-5", "B8 TURN: the planted unit number pays off"),
    ("b14", "I opened our chat's member list. 7C was in it twice.",
     {"say": "I opened our chat's member list. Seven-C was in it twice.", "emph": ["twice."]}),
    ("b15", "Me. And D. Rowe, the name on the note. Online.",
     {"say": "Me. And Dee Rowe, the name on the note. Online.", "emph": ["Online."]}),
    ("b16", "Someone else still lives in my apartment.",
     {"emph": ["still", "lives"], "sfx": [("stinger", 0.05, -6)], "gap": 0.3}),

    ("#", "P2-7", "B10 CLOCK + LIFELINE: sunrise, the voices, the man in the spare room"),
    ("b19", "Sunrise was 6:04. My phone said 5:55. Nine minutes.",
     {"say": "Sunrise was six oh four. My phone said five fifty-five. Nine minutes.",
      "emph": ["Nine", "minutes."], "sfx": [("clock_ticking", 0.0, -14)]}),
    ("b20", "It tried Mrs. Kowal's voice. The super's. My mother's.",
     {"emph": ["mother's."], "sfx": [("knock3", 0.0, -6), ("knock3", "@5", -4), ("knock3", "@7", -2)]}),
    ("b21", "I messaged D. Rowe. Are you in my spare room?",
     {"say": "I messaged Dee Rowe. Are you in my spare room?", "emph": ["spare", "room?"],
      "sfx": [("message_send", "end", -2)]}),
    ("b22", "He answered instantly. Don't answer it. Not even to me.",
     {"emph": ["Not", "even"], "sfx": [("message_pop", 0.0, 0)], "gap": 0.24}),
    ("#", "P2-6", "B9 PEAK IMAGE, HELD (after the lifeline, ~63%)"),
    ("b17", "I looked through the peephole. Nobody at eye level.", {"emph": ["Nobody"], "gap": 0.2}),
    ("b18", "Lower down, something was crouched against my door. Ear to the wood.",
     {"emph": ["crouched", "Ear"], "vox": -3, "gap": 0.1}),
    ("~", "h2", 2.0, {"sfx": [("heartbeat_slow", 0.0, -6)]}),

    ("#", "P2-7b", "B10 CLOCK, LAST RUNG: just the unit, as a question"),
    ("b23", "At 6:01, the voices stopped. It just said my unit. 7C? 7C?",
     {"say": "At six oh one, the voices stopped. It just said my unit. Seven-C? Seven-C?",
      "emph": ["7C?"], "gap": 0.2}),
    ("b24", "I bit my sleeve and said nothing.", {"vox": -3, "gap": 0.2}),
    ("b25", "Three minutes. Then two. Then my phone said 6:04.",
     {"say": "Three minutes. Then two. Then my phone said six oh four.", "emph": ["6:04."],
      "sfx": [("tick", 0.0, -6)]}),
    ("b26", "The knocking stopped. Mrs. Kowal's light came back on. The other three stayed dark.",
     {"emph": ["stopped.", "dark."], "gap": 0.3}),

    ("#", "P2-8", "B11 TWIST: the torn-off end of the note, at sunrise"),
    ("b27", "Then a slip of paper slid out under the spare room door. The torn-off end of the note.",
     {"emph": ["slid", "torn-off"], "sfx": [("whoosh", 0.4, -10)], "gap": 0.2}),
    ("b28", "I never left 7C. Whatever knocks, it isn't me.",
     {"say": "I never left Seven-C. Whatever knocks, it isn't me.", "emph": ["isn't", "me."],
      "speed": 1.15, "sfx": [("stinger", "end", -4)], "gap": 0.1}),
    ("~", "q2", 0.7, {"music_stop": True}),

    ("#", "P2-9", "B12 BOOKEND CLIFF: knocks from the inside"),
    ("b29", "Then, from inside the spare room. Three knocks.", {"vox": -3, "speed": 1.15, "gap": 0.1}),
    ("~", "k4", 1.35, {"sfx": [("knock", 0.0, 0), ("knock", 0.45, 1), ("knock", 0.9, 3)], "cut": True}),
]

PARTS = {"p1": P1, "p2": P2}


def spoken():
    """(part, id, text, say, speed) for every spoken line, in order."""
    for part, rows in PARTS.items():
        for e in rows:
            if e[0] in ("#", "~"):
                continue
            lid, text, opts = e
            yield part, lid, text, opts.get("say", text), opts.get("speed", SPEED)
