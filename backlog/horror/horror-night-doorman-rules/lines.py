"""Single source of the spoken lines for horror-night-doorman-rules (2 parts).

Used by tts_measure.py (Kokoro on the Spark CPU), build.py (timelines, stats, storyboards) and, through
build.py's printed tables, script.md.

Entry kinds (same as backlog/horror/horror-delivery-photo-inside/lines.py)
  ("#", beat_key, heading)                section marker
  (id, spk, text, opts)                   a spoken line; opts: say (TTS text), gap (s after), cap (caption
                                          overrides {tts_word: shown}, "" glues to the previous word),
                                          sfx [(cue, offset_s | "end" | "end+0.3" | "w:word", gain_db)],
                                          screen (what is on screen)
  ("~", id, seconds, opts)                timed silence (picture holds, SFX only)

Cast (renamed for this episode so the channel does not reuse names): Lena (narrator, first night on the
desk), Gus Brandt (night concierge for 31 years, exists only as a chat), "Mr. Pell" (a contact saved as the
owner), Marcus (day shift). The building is the Calloway.

Who is who (one model, the props agree):
  - The chat "Gus" is the real Gus. He is up in 1903 (his cell rings there, P2) and he protects Lena: every
    order he gives is "don't go up / let it ring / put it back". "I'm home in bed" is a protective lie, and he
    says so at the end ("I lied so you wouldn't come.").
  - The VOICE (bm_george: the desk line in P2, then the man in the blazer) is the lure. It wears Gus's voice
    and calls her "kid". The chat Gus never says "kid".
  - "Mr. Pell" texts from a number that is not the owner's (the staff sheet has the real one). Rule 5 is a real
    rule (obey the owner); the contact was swapped, so neither rule was wrong: the number was.
"""

# speaker -> Kokoro voice, speed. Lena reads her narration AND every chat bubble ("Gus: ..."), so the chat
# Gus has no voice of his own; only the lure gets a voice (bm_george, slower, older).
VOICES = {
    "N": ("af_heart", 1.35),    # Lena, narrator; reads Gus's and Pell's texts aloud
    "V": ("bm_george", 1.05),   # the voice on the 1903 line / the man in the blazer
}
SPEAKER_NAME = {"N": "Narrator (Lena)", "V": "The voice (Gus's voice)"}

GAP = 0.16        # breath between lines
TURN_GAP = 0.30   # speaker change

# rule bubbles, shared by both parts (narration contract: Part 2's closing bubbles repeat these exactly,
# except rule 3)
RULES = {
    1: "1. Never open the glass doors after 1.",
    2: "2. If the elevator comes down empty, don't get in.",
    3: "3. If 1903 calls, send nobody up. 1903 is empty.",
    4: "4. At 3, count the keys. 95. If there's a 96th, don't touch it.",
    5: "5. If Mr. Pell, the owner, texts you, do what he says.",
    6: "6. Never leave the desk before 7.",
}
RULE3_NEW = "3. If 1903 calls, send nobody up. Even if it sounds like me."

C1903 = {"nineteen-oh-three": "1903", "nineteen-oh-three.": "1903.", "nineteen-oh-three,": "1903,",
         "nineteen-oh-three?": "1903?"}

P1 = [
    ("#", "B1", "B1 HOOK: rule 3 + confession + who ordered it"),
    ("n1", "N", "Rule three of my night desk. If nineteen-oh-three calls, send nobody up. Nineteen-oh-three is empty.",
     {"cap": C1903, "sfx": [("drone", 0.0, -10)],
      "screen": "FRAME 0 = COVER: desk-phone close-up, the 1903 button under yellow tape glowing bright red through it; "
                "the propped work phone shows the Desk Handover chat with the rule-3 bubble enlarged (\"1903\" in an alert bubble)"}),
    ("n2", "N", "Tonight I broke rule three. A text from the owner ordered me to.",
     {"sfx": [("phone_buzz", "w:text", -4), ("stinger", "end", -8)],
      "screen": "Lock-screen banner flash: \"Mr. Pell (Owner) · Go up now.\" (snap zoom, glitch)"}),

    ("#", "B2", "B2 SETUP + AUTHORITY"),
    ("n3", "N", "The concierge before me, Gus, had that desk for thirty-one years. Last night was his last shift.",
     {"cap": {"thirty-one": "31"},
      "screen": "Lobby wide: glass doors, marble desk, elevator behind; Lena small at the desk. Chat header \"Desk Handover · 2 members\", "
                "system line \"Gus Brandt · Night Desk · 31 yrs\""}),
    ("n4", "N", "We never met, but he added me to a chat called Desk Handover, with six rules.",
     {"sfx": [("notify", 0.0, -6)],
      "screen": "Banner \"Gus added you to Desk Handover\"; Gus: \"6 rules. Read them twice.\" then the six rule bubbles stack in fast"}),

    ("#", "B3", "B3 INTRUSION: a minor rule broken before it is read (HEARSE-P1 0:31)"),
    ("n5", "N", "I only read rule three. So at one, when the lobby got stuffy, I propped the glass door open.",
     {"cap": {"one,": "1 AM,"}, "sfx": [("door_creak", "w:propped", -8)],
      "screen": "Desk clock 1:04; the glass door swings open onto the dark street, wastebasket as a wedge"}),
    ("n6", "N", "Behind me, the elevator started coming down by itself, from nineteen.",
     {"cap": {"nineteen.": "19."}, "sfx": [("ding", "end", -14)],
      "screen": "Elevator floor display counting down 19 > 18 > 17 (nobody pressed it)"}),
    ("g1", "N", "Gus texted: Shut the door. Rule one, never open the glass doors after one.",
     {"cap": {"one.": "1."}, "sfx": [("message_pop", 0.0, 0)],
      "screen": "Gus: \"Shut the door. Rule 1, never open the glass doors after 1.\" (rule-1 pinned bar highlighted)"}),
    ("n7", "N", "How did he know? He wasn't even in the building.",
     {"screen": "Lena CU, suspicious, looking up at the ceiling"}),

    ("#", "B4", "B4 FIRST PROOF: the rules are real"),
    ("n8", "N", "I kicked the door shut, but the elevator kept coming, and it opened on the lobby with nobody inside.",
     {"sfx": [("click", "w:shut.", 0), ("ding", "w:opened", -2)],
      "screen": "Door bolt flash; elevator doors slide open on an empty lit car"}),
    ("g2", "N", "Gus: Rule two. If the elevator comes down empty, don't get in.",
     {"sfx": [("message_pop", 0.0, 0)], "screen": "Rule-2 bubble pops: \"2. If the elevator comes down empty, don't get in.\""}),
    ("n9", "N", "So I stayed in my chair. Inside the car, the button for nineteen was already lit.",
     {"cap": {"nineteen": "19"}, "screen": "Car panel insert: button 19 glowing orange, nobody inside"}),
    ("n10", "N", "And the doors stayed open, waiting, until I looked away. Then it climbed straight back to nineteen.",
     {"cap": {"nineteen.": "19."}, "sfx": [("whoosh", "w:climbed", -10)],
      "screen": "Doors hold open (no timer runs out); the moment the camera cuts to Lena looking down, the doors close; display climbs to 19"}),
    ("n11", "N", "One small rule broken, and the building answered in seconds. After that, I read every rule twice.",
     {"sfx": [("pop", 0.0, -10)], "screen": "Chat pulls out to show all six rule bubbles; ticks appear beside 1 and 2"}),

    ("#", "B7", "B7 LULL + PLANTS (keys, tape)"),
    ("n12", "N", "Rule four was about the key board behind me. At three, count the keys: ninety-five, and if there's a ninety-sixth, don't touch it.",
     {"cap": {"three,": "3 AM,", "ninety-five,": "95,", "ninety-sixth,": "96th,"}, "sfx": [("tick", "w:ninety-five,", -8)],
      "screen": "Key board: 96 numbered hooks, 95 keys, one empty hook; rule-4 bubble \"4. At 3, count the keys. 95. If there's a 96th, don't touch it.\""}),
    ("n13", "N", "And on the desk phone, the button for nineteen-oh-three had a strip of yellow tape over it. Old tape, curling at one corner.",
     {"cap": C1903, "screen": "Desk-phone close-up: rows of unit buttons \"1901 1902 [tape] 1904\"; the tape's curled corner"}),

    ("#", "B8", "B8 MIDPOINT: the owner orders the break (rival authorities)"),
    ("n14", "N", "At two forty-one, the work phone buzzed. A text from a contact already saved as Mr. Pell, owner.",
     {"say": "At two forty-one, the work phone buzzed. A text from a contact already saved as Mister Pell, owner.",
      "cap": {"two": "2:41,", "forty-one,": ""}, "sfx": [("phone_buzz", "w:buzzed.", 0)],
      "screen": "Desk clock 2:41; new thread \"Mr. Pell (Owner)\" with a saved-contact card"}),
    ("p1", "N", "Nineteen-oh-three needs help. Go up now.",
     {"cap": C1903, "sfx": [("message_pop", 0.0, 0)], "screen": "Pell: \"1903 needs help. Go up now.\""}),
    ("n15", "N", "Rule five. If Mr. Pell, the owner, texts you, do what he says.",
     {"say": "Rule five. If Mister Pell, the owner, texts you, do what he says.",
      "screen": "Rule-5 bubble highlighted: \"5. If Mr. Pell, the owner, texts you, do what he says.\""}),
    ("n16", "N", "So rule five said go up, and rule three said nobody goes up. The same man wrote both. One of them had to be wrong.",
     {"sfx": [("whoosh", 0.0, -12)], "screen": "Whip between the rule-5 and rule-3 bubbles, both highlighted"}),
    ("n17", "N", "I asked Gus which rule wins. He started typing. Stopped. Started again.",
     {"sfx": [("message_send", 0.0, -2), ("typing", "end", -6)],
      "screen": "Me: \"The owner says go up. Which rule wins?\"; header \"Gus is typing…\" on, off, on"}),
    ("~", "s1", 1.1, {"sfx": [("typing", 0.0, -8)], "screen": "Typing dots, no VO"}),
    ("g3", "N", "Gus: What number texted you?", {"gap": 0.12, "sfx": [("message_pop", 0.0, 0)], "screen": "Gus: \"What number texted you?\""}),
    ("n18", "N", "I sent him a screenshot.", {"gap": 0.12, "sfx": [("message_send", 0.0, -2)],
     "screen": "My screenshot bubble: the Pell contact card, number visible (it will not match the staff sheet in Part 2)"}),
    ("g4", "N", "That number was never his.", {"sfx": [("glitch", 0.2, -6)], "screen": "Gus: \"That number was never his.\" (glitch, shake)"}),
    ("n19", "N", "So neither rule was wrong. The number was.", {"screen": "Lena CU, shocked"}),
    ("g5", "N", "Gus: Don't go up. Don't send anyone.", {"sfx": [("message_pop", 0.0, 0)], "screen": "Gus: \"Don't go up. Don't send anyone.\""}),
    ("n20", "N", "I typed, and if nineteen-oh-three calls? And he didn't answer.",
     {"cap": C1903, "sfx": [("message_send", "w:typed,", -2)], "screen": "Me: \"and if 1903 calls?\" (delivered, no reply)"}),

    ("#", "B9", "B9 PEAK: the camera monitor (the scariest image, held ~4 s with one change)"),
    ("n21", "N", "I checked the camera monitor. On nineteen, the door to nineteen-oh-three was open a crack, and a man in a concierge blazer stood beside it, facing the wall.",
     {"cap": {**C1903, "nineteen,": "19,"}, "sfx": [("static", 0.0, -14), ("drone", "w:blazer", -4)],
      "screen": "Monitor: 2x3 CCTV grid, zoom into \"CAM 19-E\"; grey hallway, 1903's door ajar, a back-view man in a navy blazer facing the wall beside it"}),
    ("~", "h1", 3.8, {"sfx": [("heartbeat_slow", 0.0, -4)],
                      "screen": "HELD 3.8 s, music out: the dark gap of 1903's door widens slowly while the man does not move"}),
    ("p2", "N", "Then Pell again. Gus doesn't work here anymore. Ask him why he left at two forty-one last night.",
     {"cap": {"two": "2:41", "forty-one": ""}, "sfx": [("phone_buzz", 0.0, -2)],
      "screen": "Pell: \"Gus doesn't work here anymore. Ask him why he left at 2:41 last night.\""}),
    ("n22", "N", "Two forty-one, the exact same minute, twenty-four hours ago.",
     {"cap": {"Two": "2:41,", "forty-one,": "", "twenty-four": "24"}, "sfx": [("heartbeat_slow", 0.0, -6)],
      "screen": "Desk clock 2:41 in red, then \"-24 h\""}),

    ("#", "B10", "B10 LIFELINE + B6 ISOLATION"),
    ("n23", "N", "I called building security and got a recording. Next patrol, six a.m.",
     {"say": "I called building security and got a recording. Next patrol, six A M.",
      "cap": {"six": "6", "a.m.": "AM."}, "sfx": [("phone_buzz", 0.0, -14)],
      "screen": "Call screen \"Calloway Security · recording\"; \"Next patrol 6:00 AM\""}),
    ("n24", "N", "I typed to Gus, why did you leave? And his little green dot went grey.",
     {"sfx": [("message_send", 0.0, -2)], "screen": "Me: \"why did you leave?\"; Gus's header goes from \"online\" to \"last seen 2:38\""}),

    ("#", "B12", "B12 CLIFF: sound before visual, new imperative, bookend"),
    ("n25", "N", "Then the desk phone made a sound I'd never heard it make. Under the yellow tape, a light was glowing red.",
     {"sfx": [("desk_ring", "w:sound", -12)], "screen": "Lobby wide, lights dip; then the desk-phone ECU, red light through the tape"}),
    ("~", "h2", 1.4, {"sfx": [("desk_ring", 0.0, -6)], "screen": "Ring; LCD \"LINE 1903\"; no VO"}),
    ("n26", "N", "It was line nineteen-oh-three, and Gus's dot flicked back to green.",
     {"cap": C1903, "sfx": [("desk_ring", "end", -4)], "screen": "Gus's header: \"online\"; typing dots"}),
    ("g6", "N", "Let it ring.",
     {"gap": 0.0, "sfx": [("message_pop", 0.0, 0), ("stinger", 0.15, -2)],
      "screen": "Gus: \"Let it ring.\" Push past it to the rule-3 bubble over the red-lit button (frame-0 framing); card \"PART 1/2\""}),
    ("~", "e1", 1.3, {"sfx": [("desk_ring", 0.1, -8)], "screen": "Hold the bookend; hard cut to black"}),
]

P2 = [
    ("#", "B1", "B1 COLD HOOK: the rule, the call, a defied order, the voice"),
    ("q1", "N", "Our front desk phone was ringing from nineteen-oh-three. My handover rules swore nineteen-oh-three was empty.",
     {"cap": C1903, "sfx": [("desk_ring", 0.0, -6)],
      "screen": "FRAME 0 = COVER: desk-phone ECU, red light through the yellow tape, LCD \"LINE 1903 · CALLING\"; behind it the work phone with the rule-3 bubble"}),
    ("q2", "N", "Gus said let it ring, and I picked up.",
     {"sfx": [("click", "w:picked", -2)], "screen": "Gus's bubble \"Let it ring.\" on the propped phone; Lena lifts the receiver"}),
    ("v1", "V", "Kid, it's Gus. Whatever's in that chat, it isn't me.",
     {"sfx": [("static", 0.0, -16)], "screen": "Lena CU, receiver to her ear; LCD \"1903 · 00:04\" (line hiss)"}),
    ("q3", "N", "Then a click, and the line went dead.", {"sfx": [("click", "w:click,", 0)], "screen": "LCD \"LINE DROPPED\"; the red light snaps off"}),

    ("#", "B5", "B5 RIVAL AUTHORITIES (read-out rhythm)"),
    ("q4", "N", "Then the handover chat buzzed. Gus: That wasn't me on the phone. I'm home in bed. Don't pick up again.",
     {"sfx": [("phone_buzz", 0.0, -2), ("message_pop", "w:Gus:", 0)],
      "screen": "Gus: \"That wasn't me on the phone. I'm home in bed. Don't pick up again.\""}),
    ("q5", "N", "Then the owner, Pell: Gus never came home last night. Go up.",
     {"sfx": [("message_pop", "w:Pell:", 0)], "screen": "Thread \"Mr. Pell (Owner)\": \"Gus never came home last night. Go up.\""}),
    ("q6", "N", "Two Guses and one owner. So which Gus was in my chat? Somebody was lying to me.",
     {"screen": "Lena CU, eyes left / right"}),

    ("#", "B4", "B4 OUTSIDE CHECK on paper (HEARSE-P2 1:36-1:47)"),
    ("q7", "N", "Under the desk there's a laminated staff sheet. It's paper, and nobody can edit paper.",
     {"sfx": [("whoosh", 0.0, -16)], "screen": "Tilt down under the desk: a laminated sheet \"CALLOWAY STAFF · EMERGENCY CONTACTS\" in phone-torch light"}),
    ("q8", "N", "Mr. Pell's real number was on it. It wasn't the number that had been texting me.",
     {"say": "Mister Pell's real number was on it. It wasn't the number that had been texting me.",
      "screen": "Sheet row \"R. Pell (Owner)\" with a number; side by side with the Pell contact card: the numbers differ (red strike on the contact)"}),
    ("q9", "N", "Gus's cell was on it too, so I dialed it.",
     {"sfx": [("tick", "end", -6)], "screen": "Row \"G. Brandt (Night) · cell\" highlighted; call screen \"Gus Brandt · calling…\""}),
    ("q10", "N", "It rang, and at the exact same second, under the yellow tape, line nineteen-oh-three lit up.",
     {"cap": C1903, "sfx": [("desk_ring", "w:lit", -4)],
      "screen": "Split screen: work phone \"calling…\" / desk-phone 1903 light, pulsing together"}),
    ("q11", "N", "His phone was up there, so the Gus in my chat lied too. He wasn't home in bed.",
     {"sfx": [("glitch", "w:lied", -8)], "screen": "Gus's bubble \"I'm home in bed.\" edited to red: \"I'm home in bed. ✕\""}),

    ("#", "B5b", "B5 COUNT LADDER + PART-1 PLANTS PAID"),
    ("q12", "N", "At three a.m., rule four: count the keys. Ninety-five, and if there's a ninety-sixth, don't touch it.",
     {"say": "At three A M, rule four: count the keys. Ninety-five, and if there's a ninety-sixth, don't touch it.",
      "cap": {"three": "3", "a.m.,": "AM,", "Ninety-five,": "95,", "ninety-sixth,": "96th,"},
      "sfx": [("clock_ticking", 0.0, -12)],
      "screen": "Desk clock 3:00; rule-4 bubble \"4. At 3, count the keys. 95. If there's a 96th, don't touch it.\"; key board"}),
    ("q13", "N", "Ninety-three. Ninety-four. Ninety-five.",
     {"gap": 0.0, "cap": {"Ninety-three.": "93.", "Ninety-four.": "94.", "Ninety-five.": "95."},
      "sfx": [("tick", "w:Ninety-three.", -4), ("tick", "w:Ninety-four.", -4), ("tick", "w:Ninety-five.", -4)],
      "screen": "Count overlay 93 · 94 · 95, one hook lighting per count"}),
    ("~", "ps1", 0.6, {"screen": "Near-black beat, one brass glint"}),
    ("q14", "N", "Ninety-six.", {"cap": {"Ninety-six.": "96."}, "sfx": [("stinger", 0.0, -6)], "screen": "\"96\" in red; the extra key swings on hook 96"}),
    ("q15", "N", "The extra key had a brass tag that said nineteen-oh-three.", {"cap": C1903, "screen": "Brass tag \"1903\" ECU"}),
    ("q16", "N", "Behind me, the elevator chimed. It had come down from nineteen, empty, and it held its doors open for me.",
     {"cap": {"nineteen,": "19,"}, "sfx": [("ding", "w:chimed.", -2)],
      "screen": "Lena turns; the elevator doors open on an empty lit car; button 19 lit inside"}),
    ("q17", "N", "The key, the elevator, the owner. Everything in this building was pointing up.",
     {"sfx": [("pop", "w:key,", -8), ("pop", "w:elevator,", -8), ("pop", "w:owner.", -8)],
      "screen": "Triptych: brass tag / open car / Pell bubble, each pops on its word; arrows up"}),

    ("#", "B7", "B7 LULL + PAPER PLANT (the log)"),
    ("q18", "N", "I opened the visitor log so my hands had something to do. Gus's last entry was from last night.",
     {"sfx": [("whoosh", 0.0, -18)], "screen": "Visitor log, pages turning back to yesterday"}),
    ("q19", "N", "Two forty-one, nineteen-oh-three called, going up myself, back in five.",
     {"cap": {"Two": "2:41,", "forty-one,": "", **C1903},
      "screen": "Handwriting writes on: \"2:41 – 1903 called. Going up myself. Back in five. –G\""}),
    ("q20", "N", "He never signed back in.", {"screen": "The empty TIME IN cell"}),

    ("#", "B8", "B8 MIDPOINT REFRAME: rule 3 inverted"),
    ("q21", "N", "That's when I got it. Rule three says send nobody up, so Gus didn't send anybody. He went himself.",
     {"screen": "Lena CU, shocked to angry; rule-3 bubble over her"}),
    ("q22", "N", "And rule three is why nobody ever went up after him.",
     {"sfx": [("glitch", "w:nobody", -10)], "screen": "Rule-3 bubble: \"send nobody up\" glows red"}),
    ("q23", "N", "Pell lied about everything else, but he was right about one thing. Somebody had to go up.",
     {"screen": "Pell's \"Go up now.\" bubble; Lena stands"}),

    ("#", "B5c", "B5 RULE-BREAK LADDER (each rule named as it breaks)"),
    ("q24", "N", "I took the ninety-sixth key, rule four. I got into the empty elevator, rule two.",
     {"sfx": [("click", "w:key,", -4), ("impact", "w:four.", -10), ("impact", "w:two.", -10)],
      "screen": "Hook 96 empties; stamp \"4 ✕ the 96th key\"; elevator doors; stamp \"2 ✕ rode it empty\""}),
    ("q25", "N", "I left the desk before seven, rule six. And I sent somebody up. Me. Rule three.",
     {"cap": {"seven,": "7,"}, "sfx": [("impact", "w:six.", -10), ("boom", "w:three.", -6)],
      "screen": "Empty desk, chair turning; stamp \"6 ✕ left the desk\"; then the big red stamp \"3 ✕ sent somebody up: me\""}),
    ("q26", "N", "The chat lit up. Gus: Put the key back, please. Nobody means you too.",
     {"sfx": [("phone_buzz", 0.0, -2)], "screen": "Gus: \"Put the key back, please. Nobody means you too.\""}),
    ("q27", "N", "Five, nine, and at thirteen the lights dipped. At sixteen my signal died, but the chat kept working. How?",
     {"cap": {"Five,": "5,", "nine,": "9,", "thirteen": "13", "sixteen": "16"}, "sfx": [("static", "w:sixteen", -6)],
      "screen": "Floor display 5 > 9 > 13 (light dip) > 16 (status bar \"No Service\"); the chat still delivers"}),
    ("q28", "N", "Gus: If I'm standing up there, it isn't me.",
     {"sfx": [("message_pop", 0.0, 0)], "screen": "Gus: \"If I'm standing up there, it isn't me.\""}),

    ("#", "B9", "B9 PEAK: the man in the blazer (held 4 s)"),
    ("q29", "N", "At nineteen, the doors opened on a hallway with one light on.",
     {"cap": {"nineteen,": "19,"}, "sfx": [("ding", 0.0, -2)], "screen": "Display 19; doors part on the hallway"}),
    ("q30", "N", "At the far end, outside nineteen-oh-three, a man in a concierge blazer stood with his face to the wall.",
     {"cap": C1903, "sfx": [("heartbeat_slow", "w:blazer", -4)],
      "screen": "Hallway, one light; door plate 1903 ajar; the back-view blazer man beside it, facing the wall"}),
    ("~", "ph1", 4.0, {"sfx": [("breath", 1.6, -14)], "screen": "HELD 4.0 s, music out, heartbeat only; slow push 1.00 > 1.04"}),

    ("#", "B10", "B10 LIFELINE (removed)"),
    ("q31", "N", "Four percent battery and no signal. I dialed nine-one-one anyway, and the call failed.",
     {"cap": {"Four": "4%", "percent": "", "nine-one-one": "911"}, "sfx": [("glitch", "w:failed.", -8)],
      "screen": "Battery 4% red; call \"911 · Call failed\""}),

    ("#", "B11", "B11 TWIST: the voice was the lure, the chat was protecting her"),
    ("q32", "N", "He didn't turn around. He just said, softly, in Gus's voice:", {"screen": "Hallway, very slow push; no lip flap"}),
    ("v2", "V", "Thanks, kid. Your shift now.", {"sfx": [("breath", 0.0, -12)], "screen": "Caption only; the man stays facing the wall"}),
    ("q33", "N", "Then the hallway light went out.", {"sfx": [("boom", "end", -6)], "screen": "Black; phone glow from below on Lena"}),
    ("q34", "N", "The chat buzzed one last time. Gus: I'm sorry. I lied so you wouldn't come.",
     {"sfx": [("phone_buzz", 0.0, -4)], "screen": "Gus: \"I'm sorry. I lied so you wouldn't come.\""}),

    ("#", "B12", "B12 CLIFF + BOOKEND: a new rule from a new authority"),
    ("q35", "N", "Then the handover chat added a new member, Marcus from the day shift. And a message started sending, from me.",
     {"sfx": [("notify", 0.0, -4), ("message_send", "w:sending,", -2)],
      "screen": "Banner \"Marcus (Day Desk) joined Desk Handover\"; header \"3 members\"; my outgoing bubble with a sending spinner"}),
    ("q36", "N", "The same six rules, word for word, except rule three. If nineteen-oh-three calls, send nobody up. Even if it sounds like me.",
     {"cap": C1903, "sfx": [("message_pop", 0.0, -6), ("stinger", "end", -2)],
      "screen": "Rules 1, 2, 4, 5, 6 stack in exactly as in Part 1, sent by Lena; last bubble: \"3. If 1903 calls, send nobody up. Even if it sounds like me.\"; card \"END · PART 2/2\""}),
    ("~", "pe1", 1.2, {"sfx": [("desk_ring", 0.1, -16)], "screen": "Faint ring of line 1903 under the bookend; hard cut"}),
]

PARTS = {"p1": P1, "p2": P2}


def spoken():
    return [e for part in (P1, P2) for e in part if e[0] not in ("#", "~")]
