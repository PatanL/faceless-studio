"""Single source of the spoken lines for horror-delivery-photo-inside.

Used by tts_measure.py (Kokoro on the Spark CPU), build.py (timeline, stats, storyboard.json) and,
through build.py's printed tables, script.md.

Entry kinds
  ("#", beat_key, heading)                         section marker
  (id, spk, text, opts)                            a spoken line; opts: say (TTS text), gap (s after),
                                                   cap (caption text overrides {tts_word: shown}), sfx
                                                   [(cue, offset_s, gain_db)], screen (on-screen text)
  ("~", id, seconds, opts)                         timed silence (picture holds, SFX only)
"""

# speaker -> Kokoro voice, speed. Narrator = af_heart. Every other voice is a different Kokoro voice
# so the listener can tell narration from the driver, support, the sister and the restaurant.
# am_puck (the critique's suggestion) is not cached on the Spark; am_michael is, and reads as a calm,
# friendly US male, which is what the driver needs. Swap in am_puck later if it is downloaded.
VOICES = {
    "N": ("af_heart", 1.30),   # narrator, Nora
    "R": ("am_michael", 1.15),  # Teo, the driver (also the voice of the final review)
    "S": ("af_sky", 1.25),     # Bites Support
    "M": ("af_nicole", 1.25),  # Mia, the sister (viewer-proxy voice)
    "C": ("bm_george", 1.20),  # the restaurant on the phone
}
SPEAKER_NAME = {"N": "Narrator (Nora)", "R": "Teo (driver)", "S": "Bites Support", "M": "Mia (sister)", "C": "Lucky Noodle (restaurant)"}

GAP = 0.22        # breath between lines
TURN_GAP = 0.32   # speaker change

V = [
    ("#", "S1", "S1 HOOK"),
    ("n1", "N", "My delivery photo was taken from inside my apartment.",
     {"sfx": [("notify", 0.0, -6)], "gap": 0.18,
      "screen": "Order card: green \"✓ Left at door · 9:41 PM\"; proof photo of my front door from INSIDE, chain on; red ring on the chain; burned label \"taken from INSIDE →\""}),
    ("n2", "N", "I live alone.",
     {"sfx": [("stinger", 0.05, -8)],
      "screen": "Photo insert full-frame (white proof border, \"9:41 PM\")"}),

    ("#", "S2", "S2 TRUSTED SOURCE ANSWERS"),
    ("s1", "S", "Driver verified! Location: inside unit. Anything else today?",
     {"sfx": [("message_pop", 0.0, 0), ("glitch", 1.15, -4)],
      "screen": "Support chat. Me: \"who took this photo?? I live alone\". Support: \"Driver verified ✓ Location: INSIDE UNIT. Anything else today? 🙂\""}),

    ("#", "S3", "S3 PLANT + TELL (the chain sets the timeline)"),
    ("n3", "N", "In the photo my chain is on, and I put it on at nine. The photo says nine forty-one.",
     {"cap": {"nine.": "9:00.", "nine": "9:41.", "forty-one.": ""},
      "screen": "Macro on the chain in the photo; timestamp \"9:41 PM\" pulses; cut to the real door down the hall, chain on"}),
    ("n4", "N", "So he was already inside.",
     {"sfx": [("impact", 0.0, -10)], "screen": "RedText scrawl \"ALREADY INSIDE\" (0.8 s)"}),

    ("#", "S4", "S4 RULES"),
    ("r1", "R", "Hi! Your order's by the door. Rate me five stars and I'll head out.",
     {"sfx": [("message_pop", 0.0, 0)],
      "screen": "Driver chat header \"Teo · ★5.0 · 1,206 deliveries · 1,200 ratings\"; bubble \"Hi! Your order's by the door 🙂 Rate me ★★★★★ and I'll head out\"; app system line (on-screen only, UI chime): \"Drivers can't leave until the order is rated.\""}),

    ("#", "B3", "B3 NEAR-COMPLIANCE + S5 PROXIMITY RUNG 1"),
    ("n5", "N", "My thumb was on the fourth star when my fridge door thumped shut.",
     {"gap": 0.0, "sfx": [("impact", "end", -3)],
      "screen": "Rating sheet ★★★★☆, thumb over star 4"}),
    ("~", "q1", 0.6, {"screen": "Silence: Nora frozen, lookX toward the kitchen"}),
    ("n6", "N", "The map showed my apartment, and his icon was in the kitchen.",
     {"sfx": [("sonar_ping", 0.9, -6)],
      "screen": "Map tab: the street map zooms into a floor plan (Kitchen / Hall / Bedroom / Bath); scooter icon in Kitchen; \"Teo · 30 ft away\""}),

    ("#", "B6", "B6 CHANNEL REMOVAL + VIEWER-PROXY VOICE"),
    ("n7", "N", "I texted my sister.", {"sfx": [("message_send", 0.2, -2)],
     "screen": "Chat \"Mia\". Me: \"someone took a photo INSIDE my place\""}),
    ("m1", "M", "It's a glitch. Just rate him.", {"sfx": [("message_pop", 0.0, 0)],
     "screen": "Mia: \"it's a glitch lol. just rate him\""}),
    ("n8", "N", "I typed, he's inside. Not delivered.",
     {"cap": {}, "sfx": [("glitch", 1.0, -6)],
      "screen": "Me: \"HE'S INSIDE\" + red \"! Not delivered\""}),
    ("n9", "N", "I called nine one one, and it bounced me back to the stars. The app had taken my phone.",
     {"cap": {"nine": "911,", "one": "", "one,": ""}, "sfx": [("glitch", 1.25, -2)],
      "screen": "Call screen \"911 · Calling…\" glitches to the rating sheet \"Rate your driver ☆☆☆☆☆\""}),

    ("#", "S7", "S7 VOLUME LADDER"),
    ("r2", "R", "Just one tap.", {"gap": 0.12, "sfx": [("message_pop", 0.0, 0)], "screen": "Teo: \"just one tap :)\""}),
    ("r3", "R", "I've been very patient.", {"gap": 0.12, "sfx": [("message_pop", 0.0, 0)], "screen": "Teo: \"I've been very patient.\""}),
    ("r4", "R", "Rate me!", {"cap": {"Rate": "RATE", "me!": "ME."}, "sfx": [("phone_buzz", 0.0, 0)],
     "screen": "Teo: \"RATE ME\" (red alert bubble, phone vibrates, shake)"}),
    ("n10", "N", "His icon slid into the hallway. Ten feet.",
     {"cap": {"Ten": "10", "feet.": "FEET."}, "sfx": [("footsteps", 0.3, -12)],
      "screen": "Floor plan: icon slides Kitchen -> Hall, \"Teo · 10 ft away\""}),
    ("n11", "N", "I locked my bedroom door and sat on the bed, facing it.",
     {"sfx": [("click", 0.9, 0), ("door_creak", 1.0, -20)],
      "screen": "Bedroom: Nora on the bed facing her locked door; wardrobe ajar behind her (a faint hinge creak under the lock click)"}),

    ("#", "B8", "B8 TURN: the protective act is the trap"),
    ("s2", "S", "Sorry for the wait! Six customers never rated Teo. He's still delivering to them.",
     {"sfx": [("message_pop", 0.0, 0), ("drone", 2.0, -6)],
      "screen": "Support: \"Sorry for the wait! 6 customers never rated Teo. He's still delivering to them 🙂\"; header stat flashes 1,206 deliveries / 1,200 ratings"}),
    ("~", "q2", 1.3, {"sfx": [("message_send", 0.1, -4), ("message_send", 0.7, -2)],
     "screen": "Silence beat: Me: \"hello?\" ... \"HELLO??\" (no reply, no typing dots)"}),

    ("#", "B9", "B9 SCARIEST IMAGE, held"),
    ("n12", "N", "Then a new proof photo. Me, on my bed, staring at my locked door. Taken from behind me.",
     {"sfx": [("notify", 0.0, -2), ("stinger", "w:Taken", 0)],
      "screen": "Banner \"Proof of delivery updated\"; photo 2: Nora from behind on the bed, facing her locked door, phone glow; timestamp \"9:52 PM\""}),
    ("~", "q3", 4.0, {"sfx": [("heartbeat_slow", 0.0, -2)], "screen": "Photo 2 held still 4.0 s, heartbeat only"}),
    ("n13", "N", "The map still said hallway.",
     {"screen": "Cut to the floor plan: icon pulsing in \"Hall · 10 ft\""}),
    ("r5", "R", "I'm closer than the map says.",
     {"cap": {"I'm": "i'm"}, "sfx": [("message_pop", 0.0, -4)],
      "screen": "Teo, calm lowercase: \"i'm closer than the map says.\""}),

    ("#", "B10", "B10 LIFELINE UNDER A CLOCK (15 s, real time)"),
    ("n14", "N", "Then a timer: rate in fifteen seconds, or your driver hands you the order in person.",
     {"cap": {"fifteen": "15"}, "sfx": [("clock_ticking", 0.0, -8)],
      "screen": "Rating sheet slides up: \"Rate within 0:15 or your driver will hand you the order in person.\" Timer counts down in real time, one tick per second"}),
    ("c1", "C", "Hi, it's Lucky Noodle. Your food's still on our counter. We don't have a driver named Teo.",
     {"sfx": [("phone_buzz", -0.35, -4)],
      "screen": "Incoming in-app call \"Lucky Noodle\" over the sheet; timer keeps running under it; \"Call ended\""}),
    ("~", "q4", 2.6, {"sfx": [("tick", 0.0, -2), ("tick", 1.0, -2), ("tick", 2.0, -2)], "screen": "Silent ticks under the clock; timer runs down in real time"}),
    ("n15", "N", "I didn't turn around. I gave him five stars.",
     {"sfx": [("ding", "end", -2)], "screen": "Thumb taps star 5 at 0:02; stars fill gold"}),

    ("#", "T11", "FAKE WIN (PLAYBOOK T11)"),
    ("n16", "N", "His icon vanished, and the app said delivery complete.",
     {"screen": "Floor plan empty; green card \"Delivery complete. Thank you!\"; heartbeat fades"}),
    ("~", "q5", 0.9, {"screen": "Quiet: the bed drops 6 dB"}),

    ("#", "B11", "B11 RETRO-REVEAL + VOICE SWAP"),
    ("n17", "N", "His profile had twelve hundred and one reviews. Every photo was a front door, from the inside.",
     {"cap": {"twelve": "1,201", "hundred": "", "and": "", "one": ""}, "sfx": [("whoosh", "w:Every", -4)],
      "screen": "Profile \"Teo · ★5.0 · 1,201 reviews\"; grid of 6 door photos, all from inside, chains on"}),
    ("n18", "N", "The newest came from my account.", {"screen": "Top review: my avatar \"Nora R. · just now · ★★★★★\""}),
    ("r6", "R", "She thinks I left.",
     {"sfx": [("stinger", 0.0, -2)], "screen": "Review text types out in my account, in his voice: \"She thinks I left.\""}),

    ("#", "B12", "B12 BOOKEND + CUT"),
    ("n19", "N", "Down the hall, the chain was still on.",
     {"gap": 0.0, "sfx": [("notify", "end+0.35", -2)],
      "screen": "The photo-1 framing of the front door, chain on; ping: it gains the white proof border, \"✓ Delivered to customer · 9:58 PM\", and Nora's silhouette in the foreground: it is his photo, taken from behind her"}),
    ("~", "q6", 1.6, {"screen": "Hold on the new proof photo; hard cut to black"}),
]


def spoken():
    return [e for e in V if e[0] not in ("#", "~")]
