"""Single source of the spoken lines for horror-elevator-maintenance-chat (final).

Used by tts_measure.py (Kokoro-82M on the Spark CPU) and gen_storyboard.py (timeline, stats, storyboard.json).
script.md's timed script is generated from the same timings (gen_storyboard.py --md).

Entry kinds
  ("#", beat_key, heading)              section marker
  (id, spk, text, opts)                 a spoken line. opts: say (TTS text if different), speed (override),
                                        gap (s of silence after, default GAP/TURN_GAP), screen (on-screen text / picture)
  ("~", id, seconds, opts)              timed silence (picture holds, SFX only)
"""

# speaker -> (Kokoro voice, speed). Every voice here is cached on the Spark (no downloads).
VOICES = {
    "N": ("af_heart", 1.35),     # Nora, first-person narrator; also reads her own ME bubbles and her intercom line
    "M": ("bm_george", 1.15),    # "Maintenance": calm, flat, never raises its voice (sentence case on screen, always)
    "O": ("am_michael", 1.25),   # Omar, the real on-call maintenance man (texts)
    "V": ("am_michael", 1.2),    # Omar live over the car intercom (same voice, intercom chain in the mix)
    "X": ("am_michael", 1.0),    # the last text from Omar's number: his voice, Maintenance's calm register (voice swap)
}
SPEAKER_NAME = {"N": "Nora (narrator, ME bubbles, her intercom line)", "M": "Maintenance (texts)", "O": "Omar (texts)",
                "V": "Omar (intercom)", "X": "Omar's number, last text (the entity)"}
FX = {"V": "intercom: band-pass 300-3400 Hz, light crackle, mono",
      "X": "pitch -1 st, dry (no room), slower: Omar's voice speaking in Maintenance's register",
      "M": "dry, close, -2 dB high shelf above 8 kHz (flat, intimate)"}

GAP = 0.12        # breath between lines, same speaker
TURN_GAP = 0.20   # speaker change

V = [
    ("#", "B1", "B1 HOOK: stalled car, and help arrives before anyone asked"),
    ("n1", "N", "At 1 a.m., my elevator stopped between six and seven.",
     {"say": "At one a.m., my elevator stopped between six and seven.",
      "screen": "Lock screen 1:04, banner 'Maintenance: Stay calm, Nora. Don't look at the mirror.' already up; blurred panel, counter on two red dashes; a pale face-height highlight in the mirror strip at the right edge"}),
    ("n2", "N", "Before I touched a thing, Maintenance texted me.", {"screen": "Banner pulses once"}),
    ("m1", "M", "Stay calm, Nora. Don't look at the mirror.", {"screen": "Banner text, 'mirror' red in the caption"}),
    ("n3", "N", "I never saved that contact. Who is Maintenance?",
     {"screen": "Banner opens into the 'Maintenance' thread; header 'Maintenance'"}),

    ("#", "B2", "B2 DECOY + VIEWER PROXY (the 0:03 question asked by 0:13)"),
    ("m2", "M", "Car 2 is jammed. I can get you moving.", {"screen": "MAINT bubble"}),
    ("n4", "N", "I typed: how do you know my name?", {"screen": "keyboard ticks; ME bubble 'how do you know my name?' pops on 'name'"}),
    ("m3", "M", "I'm watching you on the camera. You're doing fine.", {"screen": "MAINT bubble"}),
    ("n5", "N", "The camera in the corner had its red light off.", {"screen": "Dome camera, LED unlit"}),

    ("#", "B2r", "B2 RULES (numbered, from the wrong authority) + PLANTS"),
    ("m4", "M", "One. Press 2, then 11, then 5.",
     {"say": "One. Press two, then eleven, then five.", "screen": "Panel close-up; neon card '2 → 11 → 5'; inspection card under the buttons: 'CAR 2 · AFTER HOURS +1 555 0142'"}),
    ("m5", "M", "Two. Hold Close until the lights dim.", {"screen": "card 'HOLD CLOSE'"}),
    ("m6", "M", "Three. Never press the alarm. It resets the car.", {"screen": "card 'NEVER: ALARM'; the alarm button glints"}),
    ("m7", "M", "Four. Don't step out until you see your number.", {"screen": "card 'WAIT FOR YOUR NUMBER'"}),
    ("n6", "N", "Mine's a red nine, painted across from the doors.", {"screen": "Warm insert: my landing, a huge red 9 on the wall facing the doors"}),
    ("n7", "N", "The back wall is a mirror. I kept my eyes on the steel doors.", {"screen": "Nora facing camera, mirror behind her empty (glare only, out of focus)"}),

    ("#", "B5", "B5 PRESSURE LADDER: one rung per button"),
    ("n8", "N", "I pressed 2. The car dropped a foot and caught.", {"say": "I pressed two. The car dropped a foot and caught."}),
    ("n9", "N", "I pressed 11. Something on the roof shifted, settling in.", {"say": "I pressed eleven. Something on the roof shifted, settling in."}),
    ("n10", "N", "I pressed 5. Behind me, something tapped the mirror. Once.", {"say": "I pressed five. Behind me, something tapped the mirror. Once."}),
    ("m8", "M", "Don't look. Hold Close.", {}),
    ("n11", "N", "I held it down until the lights dimmed.", {"screen": "Thumb on Close; the car light drops in three steps"}),

    ("#", "B8", "B8 MIDPOINT: Nora texts the real authority; the count pays off (reset code); TURN"),
    ("n12", "N", "The inspection card had an after-hours number. I texted it.",
     {"screen": "Inspection card insert: '+1 555 0142'"}),
    ("me1", "N", "stuck in car 2. maintenance is watching me on the camera", {"say": "Stuck in car two. Maintenance is watching me on the camera.",
                                                                            "screen": "ME bubble, lowercase, new thread '+1 555 0142'"}),
    ("o1", "O", "This is Omar. I'm the only maintenance on call tonight.", {}),
    ("o4", "O", "What did they tell you to press?", {}),
    ("me2", "N", "2, 11, 5", {"say": "Two, eleven, five.", "screen": "ME bubble '2 11 5'"}),
    ("o5", "O", "That's the reset code for car 2. Only my office has it.", {"say": "That's the reset code for car two. Only my office has it."}),
    ("o2", "O", "And car 2's camera has been dead since Tuesday.", {"say": "And car two's camera has been dead since Tuesday."}),
    ("o3", "O", "Who are you talking to?", {"gap": 0.0, "screen": "the video's only full-frame red flash"}),
    ("~", "q1", 1.0, {"screen": "Hold on the bubble; the fluorescent buzz cuts out, fan only"}),

    ("#", "B5b", "RIVAL CLAIMS: the fake authority answers inside the real one's thread"),
    ("m9", "M", "Don't answer him. He isn't in the building.", {"screen": "Maintenance banner over Omar's thread"}),
    ("o6", "O", "Don't press anything. I'm coming up with the door key. Five minutes.", {}),
    ("n13", "N", "One of them knew my name. The other had a key.", {"screen": "Split: Maintenance header + 'Nora' bubble / Omar's number + 'door key' bubble"}),

    ("#", "B6", "B6 ISOLATION: lights out, my texts stop, the enemy's keep coming; the fake authority deletes the real one"),
    ("n14", "N", "Then the lights went out.", {"speed": 1.15, "screen": "Black; phone glow only"}),
    ("n15", "N", "I typed, where are you? Not delivered. No bars.", {"screen": "ME bubble 'where are you?', system lines '(!) Not delivered' and 'No service' (the kit's status bar can't drop bars)"}),
    ("n16", "N", "And his last text was gone.", {"screen": "Omar's 'door key' bubble becomes 'This message was deleted'"}),
    ("m10", "M", "He isn't coming. Keep your eyes on the doors.", {"screen": "Maintenance banner arrives anyway"}),
    ("n17", "N", "So why did its texts still come through?", {}),

    ("#", "B9", "B9 PEAK CONTACT: the mirror, seen in the doors (held)"),
    ("n18", "N", "My phone lit the steel doors. In them, I saw the mirror behind me.", {"screen": "Steel doors in phone light; my reflection close, the mirror rectangle behind it"}),
    ("n19", "N", "I should have seen the back of my head.", {"speed": 1.1}),
    ("n20", "N", "I saw my face. Calm. Looking right at me.", {"speed": 1.15, "gap": 0.0, "screen": "THE image: my terrified reflection close; in the mirror behind, my face, calm, staring"}),
    ("~", "q2", 3.0, {"screen": "Image held still; heartbeat only"}),
    ("m11", "M", "I told you not to look.", {}),

    ("#", "S8", "S8 NAME CHECKS: unanswered"),
    ("n21", "N", "I typed, Omar? Then, OMAR. Nothing went through.", {"say": "I typed, Omar? Then, Omar! Nothing went through.",
                                                                   "screen": "ME 'Omar?' / 'OMAR??', each followed by '(!) Not delivered'"}),

    ("#", "B10", "B10 LIFELINE UNDER A CLOCK: one bar, one text, the alarm is the only route"),
    ("n22", "N", "One bar flickered back. One text got through.", {"screen": "Lock screen 1:10, dark hand"}),
    ("o7", "O", "Your texts stopped. Press the alarm. The intercom opens for ten seconds.", {"screen": "Lock-screen banner from +1 555 0142"}),
    ("n23", "N", "Never press the alarm. I pressed it.", {"gap": 0.0, "screen": "Thumb on the alarm button"}),
    ("~", "q3", 0.7, {"screen": "Bell rings once; intercom crackle opens; 0:10 clock starts"}),
    ("v1", "V", "Car 2? I can hear you. Talk to me.", {"say": "Car two? I can hear you. Talk to me.", "screen": "Intercom grille, 0:10 counting down"}),
    ("nv1", "N", "Omar, who's been texting me?", {}),
    ("v2", "V", "I don't know. Listen. I'm on nine, right in front of car 2.", {"say": "I don't know. Listen. I'm on nine, right in front of car two."}),
    ("v3", "V", "Doors open. Lights on. Nobody's inside. So where are", {"say": "Doors open. Lights on. Nobody's inside. So where are", "gap": 0.0,
                                                          "screen": "glitch on 'Nobody's inside'; the clock hits 0:00 as the line cuts mid-sentence"}),
    ("~", "q4", 0.5, {"screen": "Crackle dies; 0:00"}),

    ("#", "B11", "B11 TRUTH TWIST LANDS + PUNISHMENT FROM MAINTENANCE'S SIDE"),
    ("n24", "N", "The line went dead.", {}),
    ("m12", "M", "You shouldn't have done that.", {"screen": "Maintenance bubble, then the car jolts"}),
    ("n25", "N", "And the car began to climb. The display stayed on two dashes.", {"screen": "Counter crop: dashes, arrow blinking up"}),

    ("#", "B12", "B12 CLIFF: no number, two taps, the voice swap"),
    ("n26", "N", "It stopped. The doors slid open.", {}),
    ("n27", "N", "The wall across from me was blank. No number.", {"speed": 1.2, "gap": 0.0, "screen": "Same framing as the red-nine insert, the wall bare and cold"}),
    ("~", "q5", 3.0, {"screen": "Dead air: hallway tube buzz only"}),
    ("n28", "N", "Behind me, something tapped the mirror. Twice.", {}),
    ("n29", "N", "My phone lit up. Omar's number.", {"screen": "Lock-screen bookend of frame 0"}),
    ("x1", "X", "Don't turn around, Nora. Step out.", {"screen": "Banner from +1 555 0142: 'Don't turn around, Nora. Step out.'"}),
    ("n30", "N", "I never told Omar my name.", {"speed": 1.15, "gap": 0.0}),
    ("~", "q6", 0.6, {"screen": "Hold, 'PART 2' card, hard cut to black"}),
]


def spoken():
    return [e for e in V if e[0] not in ("#", "~")]
