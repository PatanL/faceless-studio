"""Single source of the spoken lines for horror-babysitter-parent-rules (final).

Used by tts_measure.py (Kokoro-82M on the Spark CPU) and gen_storyboard.py (timeline, stats, storyboard.json).
script.md's timed table and narration block are generated from the same timings.

Entry kinds
  ("#", beat_key, heading)              section marker
  (id, spk, text, opts)                 a spoken line. opts: say (TTS text if different), speed (override),
                                        gap (s of silence after, default GAP/TURN_GAP), screen (on-screen text, word for word)
  ("~", id, seconds, opts)              timed silence (picture holds, SFX only)
"""

# speaker -> (Kokoro voice, speed). Every voice here is cached on the Spark.
# The four "marmalade"s are four different voices / filters, so the ladder is audible:
#   W (the real Mrs. Doyle, whispering at 7:40)  ->  K (the "child" on the extension)  ->  D (the door)  ->  E (Ivy's own voice, from the handset).
# The caller C uses the SAME Kokoro voice as W, through a phone filter: on the line she sounds exactly like Mrs. Doyle.
# E is Ivy's narrator voice (af_heart) but slower, band-passed like a phone line and doubled with a 45 ms slap and -0.4 st,
# so it is plainly her voice coming OUT OF THE HANDSET, not the narrator saying the word.
VOICES = {
    "N": ("af_heart", 1.25),     # Ivy, narrator, the babysitter
    "C": ("af_sky", 1.15),       # the caller "Mrs. Doyle" on the house phone
    "W": ("af_sky", 0.95),       # the real Mrs. Doyle, whispering the password at 7:40 (flashback)
    "K": ("af_nicole", 0.9),     # the "child" on the extension in Theo's room
    "D": ("am_michael", 1.05),   # the door: "Mr. Doyle"
    "T": ("af_nicole", 0.85),    # Theo (or what has his voice) on the baby-monitor speaker
    "E": ("af_heart", 1.0),      # Ivy's own voice, out of the handset (the swap)
}
SPEAKER_NAME = {"N": "Narrator (Ivy, babysitter)", "C": "Caller as Mrs. Doyle (house phone)", "W": "Mrs. Doyle, 7:40 whisper",
                "K": "Extension 2 (child's voice)", "D": "The door (Mr. Doyle's voice)", "T": "Baby monitor (Theo's voice)",
                "E": "Extension 2 (Ivy's own voice)"}
FX = {"C": "phone band-pass 300-3400 Hz, light line hiss",
      "W": "dry, close, -4 dB, warm low-shelf (a remembered whisper)",
      "K": "pitch +3 st, phone band-pass 300-3400 Hz, hiss",
      "D": "through-door muffle: lowpass 2.2 kHz, small-room reverb",
      "T": "pitch +3 st, monitor-speaker band-pass 500-3000 Hz, crackle bed",
      "E": "pitch -0.4 st, phone band-pass 300-3400 Hz, 45 ms slap doubled at -9 dB, no room"}

GAP = 0.18        # breath between lines, same speaker
TURN_GAP = 0.26   # speaker change

RULE5 = "Nobody comes in without the password. If we call, ask for it. Wrong answer? Hang up."

V = [
    ("#", "B1", "B1 HOOK: babysitting, rule five in red, the call; the trusted voice fails by ~6 s"),
    ("n1", "N", "I was babysitting on the thirty-fourth floor. Rule five, in red: if we call, ask for the password.",
     {"screen": "Frame 0 / cover: the fridge note (5 rules; the numbers and rules 1 and 4 in grey pencil, rules 2, 3 and 5 in navy marker; "
                "rule 5 in red marker, double-underlined: \"5. " + RULE5 + "\"). On the counter: the cordless handset ringing "
                "\"INCOMING · DOYLE\" and Ivy's phone face-up, lock-screen preview \"Mrs. Doyle · 9:40 PM: Still at dinner! Back by 11:30 x\""}),
    ("n2", "N", "They called. I asked.", {"gap": 0.15, "screen": "Handset \"DOYLE · 00:04\", clock 9:41"}),
    ("c1", "C", "What password, Ivy? We're downstairs.", {"screen": "Handset \"DOYLE · 00:07\""}),

    ("#", "P1", "PLANT: the whisper outside Theo's door (rung 1: the parent's mouth)"),
    ("n3", "N", "She'd whispered it at seven forty, outside Theo's door.", {"screen": "Flashback, warm grade: the hall, Theo's door ajar, a dark gap under his bed"}),
    ("w1", "W", "Marmalade.", {"gap": 0.3, "screen": "Cream card: \"marmalade\" in Mrs. Doyle's marker"}),

    ("#", "B3", "B3 THE HANG-UP INTERRUPTED; the password works; Ivy complies (rung 2: the child's mouth)"),
    ("n4", "N", "Wrong answer meant hang up. Then the line clicked.", {"screen": "Handset readout swaps to \"EXT 2 · THEO'S ROOM · ON LINE\""}),
    ("n5", "N", "Theo's extension had picked up.", {"screen": "Bedroom from the doorway, dark; the extension's glow on the nightstand"}),
    ("k1", "K", "Marmalade.", {"gap": 0.25, "screen": "Cream card: \"marmalade\" in wobbly child letters"}),
    ("c2", "C", "There's my boy! Buzz us up, honey.", {"screen": "Handset \"DOYLE · 00:19\""}),
    ("n6", "N", "Theo knew it. So I pressed nine.", {"screen": "Handset keypad: 9 pressed; readout \"LOBBY DOOR · RELEASED\""}),

    ("#", "B4", "B4 PROOF on a second channel (the monitor app)"),
    ("n7", "N", "The baby monitor showed Theo asleep, facing the wall. No movement since seven twelve.",
     {"screen": "Monitor app full frame, night-vision green: \"● LIVE · Nursery cam\" / \"No movement since 7:12 PM\""}),
    ("n8", "N", "He hadn't moved to pick up. And I'd let them in.", {"screen": "Ivy, phone light on her face"}),

    ("#", "B2", "B2 RULES reread as cards; the keys tell"),
    ("n9", "N", "Rule one. Asleep by eight. Don't wake him, whatever you hear.",
     {"screen": "Card (pencil hand): \"1. Asleep by 8. Don't wake him, whatever you hear.\""}),
    ("n10", "N", "Rule two. Chain on till we text from the lobby. No text.",
     {"screen": "Card (marker): \"2. Chain on till we text from the lobby.\" Then Ivy's thread: nothing since 7:41"}),
    ("n11", "N", "Rule three. We have keys. We never knock. So why buzz?",
     {"screen": "Card (marker): \"3. We have keys. We never knock.\""}),
    ("n12", "N", "Rule four. If Theo talks in his sleep, don't answer him. He isn't talking to you.",
     {"screen": "Card (pencil hand): \"4. If Theo talks in his sleep, don't answer him. He isn't talking to you.\" Glitch on the last sentence"}),

    ("#", "B5", "B5 PROXIMITY: the elevator Ivy called up"),
    ("n13", "N", "In the peephole, the elevator was climbing. Twelve. Twenty. Thirty-one.",
     {"screen": "Peephole ring over the elevator's floor display: 12, 20, 31 on the words"}),
    ("n14", "N", "It stopped on thirty-four. Nobody got out.", {"screen": "Display 34; the hall through the peephole, elevator open and empty"}),
    ("~", "q1", 0.7, {"screen": "Empty hall held, room tone"}),

    ("#", "B8", "B8 TURN: the password at the door; rule five collides with rule three (rung 3: the door)"),
    ("n15", "N", "Then three knocks.", {"gap": 1.25, "screen": "FrontDoor, chain on, three rattles"}),
    ("d1", "D", "Ivy? It's Mr. Doyle. Marmalade.", {"screen": "Close on the door; no shadow under it"}),
    ("n16", "N", "Rule five. Nobody comes in without the password. He had it.", {"screen": "Rule 5 card, the first sentence underlined"}),
    ("n17", "N", "The chain slid an inch. But they never knock. I let go.", {"screen": "Insert: Ivy's hand on the chain, it slides 1 cm, stops"}),

    ("#", "B10", "B10 LIFELINE under a count (the door counts to five)"),
    ("d2", "D", "I'll count to five, Ivy.", {"screen": "Door, still"}),
    ("n18", "N", "I texted Mrs. Doyle. Are you outside? What does rule four mean?",
     {"screen": "Sent bubbles: \"Are you outside?\" / \"What does rule 4 mean?\""}),
    ("d3", "D", "One.", {"gap": 0.4, "screen": "Count chip 1 at the top of the thread"}),
    ("d3b", "D", "Two.", {"gap": 0.4, "screen": "Count chip 2"}),
    ("d3c", "D", "Three.", {"gap": 0.25, "screen": "Count chip 3"}),
    ("n19", "N", "Above it, a text I'd missed. Nine forty. Still at dinner.",
     {"screen": "Above Ivy's bubbles: Mrs. Doyle · 9:40 PM \"Still at dinner! Back by 11:30 x\""}),
    ("n20", "N", "Delivered. Not read.", {"screen": "System line under Ivy's bubbles: \"Delivered · not read\""}),
    ("d4", "D", "Four.", {"gap": 0.42, "screen": "Count chip 4"}),
    ("d4b", "D", "Five.", {"gap": 0.4, "screen": "Count chip 5"}),
    ("n21", "N", "The door went quiet. Then the monitor crackled.", {"screen": "Lock-screen banner: \"Nursery cam · Sound detected\""}),

    ("#", "B9", "B9 PEAK on the monitor, held (rung: Theo's bed)"),
    ("n22", "N", "Theo's lips were moving. He whispered,", {"gap": 0.15, "screen": "Monitor feed: Theo in profile, eyes shut, mouth moving"}),
    ("t1", "T", "She won't open it.", {"screen": "Same feed; caption in quotes"}),
    ("n23", "N", "The phone was at his ear. Something under the bed was holding it.",
     {"gap": 0.0, "screen": "The receiver at his ear; a long grey arm from the dark under the bed holds it; then everything holds"}),
    ("~", "q2", 3.0, {"screen": "Held still: the arm, the receiver, the closed eyes. Monitor hiss and heartbeat only"}),

    ("#", "B9b", "Rule four as an action (the temptation)"),
    ("n24", "N", "The monitor's talk light came on.", {"screen": "Monitor app: the push-to-talk icon lights red"}),
    ("t2", "T", "Ivy?", {"gap": 0.4, "screen": "\"Ivy?\" through the monitor speaker"}),
    ("n25", "N", "Rule four. Don't answer him.", {"screen": "Ivy, sleeve pressed over her mouth"}),

    ("#", "B11", "B11 TWIST: the real mother wrote three rules"),
    ("n26", "N", "My phone buzzed.", {"gap": 0.15, "screen": "Thread: Mrs. Doyle typing, then the reply"}),
    ("n27", "N", "What rule four? I wrote three rules. Chain, keys, password.",
     {"screen": "Mrs. Doyle: \"What rule 4?\" / \"I wrote three rules. Chain, keys, password.\""}),
    ("n28", "N", "The other two were in pencil. Both about Theo.", {"screen": "Fridge note: rules 1 and 4 (and every number) in pencil, ringed"}),
    ("n29", "N", "Get Theo. Get out.", {"gap": 0.3, "screen": "Mrs. Doyle: \"Get Theo. Get out.\""}),

    ("#", "B12", "B12 VOICE SWAP onto Ivy + bookend (rung 4: Ivy's own mouth)"),
    ("n30", "N", "The house phone rang in my hand. Extension two.", {"screen": "Handset \"INCOMING · EXT 2 · THEO'S ROOM\""}),
    ("n31", "N", "Her rule five. I asked for the password.", {"gap": 0.0, "screen": "Ivy, handset at her ear"}),
    ("~", "q3", 1.2, {"screen": "Ivy's face, a slow breath on the line"}),
    ("n32", "N", "It answered in my voice.", {"gap": 0.25, "screen": "Black"}),
    ("e1", "E", "Marmalade.", {"gap": 0.0, "screen": "RedText scrawl \"marmalade\" (the one RedText); hard cut on the last syllable"}),
    ("~", "q4", 1.6, {"screen": "End card: the fridge note (frame 0 bookend); the handset on the floor: \"EXT 2 · CALLING · DOYLE MOBILE\""}),
]


def spoken():
    return [e for e in V if e[0] not in ("#", "~")]
