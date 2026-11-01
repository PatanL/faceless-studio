"""Single source of the spoken lines for horror-text-from-tomorrow (final).

Used by tts_measure.py (Kokoro-82M on the Spark CPU) and gen_storyboard.py (timeline, stats, storyboard.json).
script.md's timed table and narration block are generated from the same timings.

Entry kinds
  ("#", beat_key, heading)              section marker
  (id, spk, text, opts)                 a spoken line. opts: say (TTS text if different), speed (override),
                                        gap (s of silence after, default GAP/TURN_GAP), screen (on-screen text, word for word)
  ("~", id, seconds, opts)              timed silence (picture holds, SFX only)
"""

# speaker -> (Kokoro voice, speed). The voice swap is audible: "Me" is af_heart at 1.10 (slower than the narrator's 1.30) and,
# in the mix, pitched down 1 semitone, dry (no room reverb) and low-passed at 6 kHz, so it is the
# narrator's own voice, slightly wrong. Its FIRST line (0:04) gets the same treatment as the last.
# The building office gets its own flat voice. Every voice here is cached on the Spark.
VOICES = {
    "N": ("af_heart", 1.30),     # Tess, narrator, flat 6A (last door before the roof stairs)
    "M": ("af_heart", 1.10),     # "Me": texts from Tess's own number (processed in the mix, see above)
    "O": ("bm_george", 1.15),    # Ostrel House Office (the building chat's admin account)
    "A": ("am_michael", 1.05),   # Mr. Abel, 6B, next door (too polite, unhurried)
    "D": ("af_sky", 1.30),       # Dee, 3A (chorus caps; later the broken lowercase line)
    "L": ("bf_isabella", 1.25),  # Mrs. Lind, 4C (the viewer-proxy doubter)
    "G": ("bf_alice", 1.20),     # gas emergency line operator (the real authority)
}
SPEAKER_NAME = {"N": "Narrator (Tess)", "M": "Me (Tess's own number)", "O": "Ostrel House Office",
                "A": "Mr. Abel (6B)", "D": "Dee (3A)", "L": "Mrs. Lind (4C)", "G": "Gas emergency line"}
FX = {"M": "pitch -1 st, dry, lowpass 6 kHz", "O": "phone-speaker band-pass 300-3400 Hz", "G": "phone-call band-pass",
      "A": "through-door muffle (lowpass 2.5 kHz)", "D": "phone-speaker band-pass", "L": "phone-speaker band-pass"}

GAP = 0.20        # breath between lines, same speaker
TURN_GAP = 0.30   # speaker change

V = [
    ("#", "S1", "S1 HOOK: my own number, stamped 2:31, at 1:52"),
    ("n1", "N", "My own number texted me. Sent at two thirty-one.",
     {"screen": "Lock 1:52 · Wed, Nov 11. Top notification: Me · 2:31 AM (red, large). Under it: Ostrel House Residents · Office: \"Gas check done. All clear. Sleep well\" · 1:49"}),
    ("n2", "N", "It was one fifty-two.", {"gap": 0.25, "screen": "Punch-in: lock clock 1:52 against the red 2:31 AM stamp"}),

    ("#", "S2", "S2 WARNING: contradicts the office's all-clear by 0:09"),
    ("m1", "M", "At two fourteen the office will call a gas leak and send everyone up to the roof. Don't go. Not even if they beg.",
     {"screen": "Thread \"Me\", stamp \"Today 2:31 AM\", grey bubble: \"At 2:14 the office will call a gas leak and send everyone up to the roof. Don't go. Not even if they beg.\""}),

    ("#", "S3", "S3 IMPOSSIBLE PROOF + PLANT"),
    ("n3", "N", "I typed, who is this? It answered before I hit send.",
     {"screen": "Draft \"who is this?\" stays unsent in the input box"}),
    ("m2", "M", "You. Check your left sock.", {"screen": "\"You.\" / \"Check your left sock.\" pop in while the draft is still unsent"}),
    ("n4", "N", "I looked. A hole, at the big toe.", {"screen": "none (SockFeet insert, front-low view)"}),

    ("#", "S4", "S4 PREDICTIONS: three things first"),
    ("m3", "M", "First, the hall goes dark, door by door. The dog downstairs stops mid-bark. The office types for a full minute.",
     {"screen": "3 grey bubbles: \"First, the hall goes dark, door by door.\" / \"The dog downstairs stops mid-bark.\" / \"The office types for a full minute.\""}),

    ("#", "S2b", "S2 AUTHORITY + RULE (pinned) + the layout plant"),
    ("o1", "O", "Roof closed. Padlocked. Only the office has the key.",
     {"screen": "Thread \"Ostrel House Residents · 39 members\"; PINNED · Ostrel House Office: \"Roof closed. Padlocked. Only the office has the key.\""}),
    ("n5", "N", "My door's the last one before the roof stairs.", {"screen": "Stairwell: roof door at the top of the flight, padlock on the hasp"}),

    ("#", "S5", "S5 PREDICTIONS COME TRUE (proximity rung, sound rung, chat rung)"),
    ("n6", "N", "Then the far end of the hall went dark. Then the next light. Then mine.",
     {"screen": "Status clock 2:09. Under-door strip: far glow, nearer glow, then my strip clicks off"}),
    ("n7", "N", "Downstairs, the dog stopped mid-bark.", {"screen": "Status clock 2:11"}),
    ("n8", "N", "Then the office started typing. For a full minute.",
     {"gap": 0.1, "screen": "Header: \"Ostrel House Office is typing…\" · status clock 2:13"}),
    ("~", "q1", 1.0, {"screen": "Typing dots keep going; clock ticks 2:13 -> 2:14"}),

    ("#", "S6", "S6 TURN: 2:14, the office inverts its own pinned rule"),
    ("n9", "N", "Two fourteen.", {"gap": 0.15, "screen": "RedText \"2:14\" flash (the episode's one RedText)"}),
    ("o2", "O", "Gas leak. Everyone up to the roof. The door is open.",
     {"screen": "Alert bubble, Ostrel House Office: \"Gas leak. Everyone up to the roof. The door is open.\" Pinned bar still reads \"Roof closed. Padlocked.\""}),

    ("#", "S7", "S7 CHORUS (caps), PROXY OBJECTION, PROXIMITY, KNOCK, COUNT, CLOCK"),
    ("d1", "D", "Everyone up!", {"gap": 0.15, "screen": "Dee (3A): \"EVERYONE UP\""}),
    ("l1", "L", "Why up? You go out in a gas leak.", {"gap": 0.15, "screen": "Mrs. Lind (4C): \"why UP?? you go OUT in a gas leak\""}),
    ("o3", "O", "Stairwell's full of gas. Go now.", {"screen": "Office: \"Stairwell is full of gas. GO NOW.\""}),
    ("n10", "N", "Thirty-seven neighbours replied, on my way. Everyone but me.",
     {"screen": "Under the alert: \"On my way · 37\" reply chip counting up"}),
    ("n11", "N", "Then feet went past my door, up the roof stairs. Nobody ran.",
     {"screen": "none (FrontDoor, hall dark; phone torches sweep the gap)"}),
    ("a1", "A", "Tess. It's Abel, from next door. Everyone is waiting for you.",
     {"screen": "none (Peephole: Mr. Abel lit only by his phone, blank face)"}),
    ("n12", "N", "I didn't open. I'd counted thirty-eight sets of feet.", {"screen": "none (Tess CU)"}),
    ("n13", "N", "The office tagged me.", {"gap": 0.15}),
    ("o4", "O", "Last one. The roof locks at two thirty.", {"screen": "Office: \"@6A Last one. The roof locks at 2:30.\""}),

    ("#", "S8", "S8 BROKEN LOWERCASE, TWO UNANSWERED NAME CHECKS, CONTACT ABOVE (scariest image, held)"),
    ("d2", "D", "its so quiet up here", {"say": "it's so quiet up here", "speed": 1.0, "screen": "Dee (3A): \"its so quiet up here\""}),
    ("n14", "N", "I typed, Dee? Mrs. Lind? Seen. Nobody answered.",
     {"screen": "Me: \"Dee?\" / \"Mrs Lind?\" each gets \"Seen\"; no typing dots"}),
    ("n15", "N", "Then one footstep, right above my bed.", {"gap": 0.0}),
    ("~", "q2", 2.8, {"screen": "Held still: Tess looking straight up, dust sifting down from the dark above her (single thud SFX at the start, then dead air)"}),

    ("#", "S9", "S9 LIFELINE (the real authority), THEN MY OWN NUMBER"),
    ("n16", "N", "I called the gas line.", {"gap": 0.2}),
    ("g1", "G", "No leak reported at that address.", {"screen": "Lower third: \"Gas Emergency Line · no leak reported\""}),
    ("n17", "N", "Then I called my own number. It rang. Up on the roof, faintly, my ringtone was playing.",
     {"gap": 0.1, "screen": "Thread \"Me\": system line \"Calling Me…\"; status clock 2:29"}),
    ("~", "q3", 0.7, {"screen": "Ringtone cuts out. System line \"Call ended\"; status clock flips 2:29 -> 2:30"}),

    ("#", "S10", "S10 TWIST: same minute, same sender; the office was me"),
    ("n18", "N", "At two thirty-one, the minute on the first text, a new one came in.",
     {"screen": "Thread \"Me\": the first warning's stamp \"Today 2:31 AM\" and a new bubble under the same stamp"}),
    ("m4", "M", "I went. Now you have to.", {"gap": 0.25, "screen": "Grey bubble: \"I went. Now you have to.\""}),
    ("n19", "N", "And in the building chat, the office had a new name. Me.",
     {"screen": "Residents chat system line: \"Ostrel House Office changed their name to Me\"; the gold OH avatar becomes the T avatar"}),

    ("#", "S10b", "S9/S10 PROOF AT THE DOOR (held)"),
    ("n20", "N", "One set of feet came down. They stopped at my door.", {"screen": "none (FrontDoor, EXIT glow; two feet shadows stop centred)"}),
    ("n21", "N", "I lay flat and looked under. Socks. A hole at the left big toe.", {"gap": 0.0, "screen": "none (door-gap insert: SockFeet, pale toe in the hole)"}),
    ("~", "q4", 1.6, {"screen": "Door-gap feet held still; heartbeat stops"}),

    ("#", "S11", "CLIFF: the beg pays off; bookend on the lock screen"),
    ("n22", "N", "My phone lit up beside me.", {"gap": 0.3, "screen": "Lock screen on the floor, same layout as frame 0"}),
    ("m5", "M", "Please. I'm begging you. Open up. It's just me.",
     {"gap": 0.0, "screen": "Notification: Me · now: \"Please. I'm begging you. Open up. It's just me.\""}),
    ("~", "q5", 0.5, {"screen": "Hold, then hard cut to black"}),
]


def spoken():
    return [e for e in V if e[0] not in ("#", "~")]
