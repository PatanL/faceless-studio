#!/usr/bin/env python3
"""Single source for whatif-breathe-underwater (final rewrite, 2026-11-01).

Holds the VO (caption/display spelling), the TTS spelling rules, the HUD state tables, the
shot list and the storyboard specs as data. It computes every timestamp from the TTS word count
of each line at a per-section rate, measures pacing with the PLAYBOOK §9 regexes, and writes:
  script.md        (from script.template.md: metrics, VO with timestamps, HUD table, shot list)
  storyboard.json  (studio/src/core/schema.ts, 16:9 30 fps)
  vo_lines.json    (id, display text, TTS text, start, duration) for the Kokoro pass
  timing.json      (lines, shots, metrics)
Run: python3 gen_storyboard.py   (pure Python, no deps; tiny, fine on the Mac)
"""
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
FPS = 30
GAP = 0.15           # pipeline paragraph_pause (pipeline/audio/config.py)
KEEP_PAD = 0.17      # silence the pipeline keeps per chunk: head 0.05 + tail 0.12 (pipeline/audio/tts.py)
RAW_PAD = 0.512      # measured Kokoro lead+tail silence per line at speed 1.25 (fit intercept, tts_timing.json)
SENT_PAUSE = 0.028   # measured extra pause per internal sentence break at speed 1.25
TTS_SPEED = "1.25"   # chosen Kokoro speed (measured 207 spoken wpm inside lines)
FLOOR_EXTRA_GAP = 0.35  # slower cadence on the trench floor (extra silence after each L10b line)
MEASURED = json.loads((HERE / "tts_timing.json").read_text())["lines"] if (HERE / "tts_timing.json").exists() else {}
SECTION_GAP = 0.3
TITLE_MIN = 2.2      # title card length (VO is spoken over it, so it is not a dead hold)
RAMP_HOLD = 2.0      # descent ramp after "You go down." at the line
END_HOLD = 3.5       # end-card hold after the last VO line
SLOW_FACTOR = 1.10   # "what if Kokoro reads 10% slower" runtime check

# ------------------------------------------------------------------ VO data
# (section label, TTS rate in spoken words per minute, [(line id, display text, [(offset s, on-screen)])])
# Display text keeps digits (caption form, like the corpus auto-subs). tts() expands them for timing.
SECTIONS = [
 ("L1 COLD OPEN", 207, [
  ("c1", "You fall off a ferry in the Pacific and gasp in seawater.",
   [(0.0, "HUD from frame 1: DEPTH 0 M · BODY 37.0°C; TAG `WESTERN PACIFIC`")]),
  ("c2", "And you're fine.", [(0.0, "bubbles stop; YOU floats upright")]),
  ("c3", "No coughing. No burning. Your chest just keeps going, like you've done this forever.",
   [(0.0, "BODY TEMP readout starts ticking down from 37.0 (no comment yet)")]),
  ("c4", "Something bumps your back and holds on. A remora. It thinks you're a shark.",
   [(1.6, "HUD REMORA chip: ATTACHED")]),
  ("c5", "Everyone up there breathes air. Everyone but you.", []),
  ("c6", "And here's the catch: air doesn't work for you anymore. You can't climb back on.",
   [(0.6, "TAG `AIR: DOESN'T WORK FOR YOU`; red strike across the surface")]),
  ("c7", "Under you, the floor is 4 kilometres down. The deepest floor on Earth is a trench, a few hundred kilometres south-west of you.",
   [(0.4, "STAT `4,000 M TO THE FLOOR`"), (3.0, "MAP inset: YOU pin -> dashed 300 KM line -> CHALLENGER DEEP pin")]),
  ("c8", "And a line on your way down is a wall.",
   [(0.0, "ROUTE ticks light: 200 · 1,000 · 2,000 · 4,000 · 8,200 (red, `THE WALL?`) · 10,935 M")]),
  ("c9", "So you go down.",
   [(0.3, "DepthMeter starts moving: the tracker runs from here to the end")]),
 ]),
 ("L2 TITLE + RULES", 207, [
  ("t0", "What if you could breathe underwater?", [(0.0, "TITLE CARD (VO over it): WHAT IF YOU COULD BREATHE UNDERWATER? (UNDERWATER red)")]),
  ("r1", "One change: your body can pull oxygen out of water.",
   [(1.2, "RULE 1 `ONE CHANGE: OXYGEN FROM WATER`")]),
  ("r2", "One promise: every time the ocean tries to kill you, you get the fix a real animal already uses.",
   [(0.4, "RULE 2 `EVERY THREAT -> A REAL ANIMAL'S FIX`")]),
  ("r3", "Until there isn't one.", [(0.0, "RULE 3 `UNTIL THERE ISN'T ONE` (red)")]),
  ("r4", "Everything else stays human: daylight eyes, and blood at 37 degrees.",
   [(0.0, "card STAYS HUMAN: SKIN · EYES · 37°C BLOOD (37°C red)")]),
  ("r5", "Keep an eye on that number. It's already moving.",
   [(0.0, "pointer ring on the HUD BODY readout (36.8 and falling)")]),
 ]),
 ("L3 GROUNDING WHILE SINKING (0 -> 200 M)", 207, [
  ("g1", "First, the bad news: seawater holds about 30 times less oxygen than air.",
   [(0.8, "SPEEDBARS `OXYGEN PER LITRE` AIR vs SEAWATER (~1/30)")]),
  ("g2", "So about 60 litres of sea has to pour through you every minute.",
   [(0.6, "SPEEDBARS `THROUGH YOU EVERY MINUTE` AIR 6 L vs WATER 60 L")]),
  ("g3", "A bathtub every two and a half minutes.", [(0.3, "TIMER ring 2:30 + TAG `1 BATHTUB`")]),
  ("g4", "Lungs can't. Water is heavy, and lungs push it in and out the same pipe.",
   [(1.6, "lung diagram: one pipe, arrows in and out, red ✗")]),
  ("g5", "In 1966, a lab mouse breathed oxygen-rich liquid and lived. Breathing out was the hard part.",
   [(0.3, "DATE CHIP 1966 · jar + mouse silhouette")]),
  ("g6", "You try to shout for help. Nothing comes out. No air, no voice.",
   [(1.4, "empty speech bubble `...`")]),
  ("g7", "The remora looks relieved.", [(0.0, "REMORA chip: RELIEVED")]),
  ("g8", "So here's your first fix, borrowed from every fish alive: gills.",
   [(2.4, "slits draw on behind the jaw; HUD BORROWED 1: GILLS (FISH)")]),
  ("g9", "Water goes in your mouth and out behind your jaw, with your blood flowing against it.",
   [(0.0, "GILL DIAGRAM: one-way arrows; counter-current strip WATER -> / <- BLOOD")]),
  ("g10", "That grabs up to 80 percent of the oxygen. Your lungs managed a quarter.",
   [(0.6, "SPEEDBARS GILLS 80% vs LUNGS 25%")]),
  ("g11", "Easy. Except breathing water does one more thing to you, and you won't feel it yet.",
   [(0.0, "TAG `EASY.`"), (0.7, "TAG `EXCEPT...` (red); BODY readout blinks once")]),
 ]),
 ("L4 HONEYMOON + PROBLEM LADDER (200 M)", 207, [
  ("h1", "200 metres. For a while, this is the best swim of your life.",
   [(0.0, "STAMP `200 M · THE LAST LIGHT`")]),
  ("h2", "Every 10 metres adds an atmosphere of pressure, crushing the air inside divers.",
   [(0.5, "PRESSURE x21; inset DIVER air bubble shrinks")]),
  ("h3", "But you have no air left to crush. Water floods your sinuses and ears, and water barely squeezes.",
   [(1.6, "TAG `EARS + SINUSES: FLOODED`; YOU's water glyph stays the same size")]),
  ("h4", "The deepest anyone has dived on a single breath is 253 metres. You pass it without noticing.",
   [(0.5, "DepthMeter mark `253 M · DEEPEST BREATH-HOLD` slides past")]),
  ("h5", "Then a blue whale slides under you, longer than two buses.",
   [(2.0, "SCALEBAR ~28 M vs YOU 1.75 M; two BUS silhouettes")]),
  ("h6", "It doesn't even look at you. Good.",
   [(0.0, "REMORA chip: UNBOTHERED")]),
  ("h7", "Problem one: salt. The sea you keep swallowing is about 3 times saltier than your blood.",
   [(0.0, "TAG `PROBLEM 1: SALT`"), (3.4, "SPEEDBARS SALT: SEAWATER vs YOUR BLOOD (~x3)")]),
  ("h8", "Fish have the fix: gill cells that pump salt back out. Now so do you.",
   [(1.0, "GILL DIAGRAM salt mode; HUD BORROWED 2: SALT PUMPS (FISH)")]),
  ("h9", "Problem two: light. About 1 percent of the sunlight gets this deep, and your eyes were made for beaches. No fix for that.",
   [(0.0, "TAG `PROBLEM 2: LIGHT`; STAT `LIGHT 1%`")]),
  ("h11", "Your fingertips have gone white. You decide it's just the light.",
   [(0.0, "TAG `FINGERTIPS: WHITE`; BODY readout 34.6, already under the 35 line")]),
 ]),
 ("L5 1,000 M · MIDNIGHT -> RUG PULL", 207, [
  ("m1", "1,000 metres. The light isn't dim anymore. It's gone.",
   [(0.0, "STAMP `1,000 M · MIDNIGHT`; STAT `LIGHT 0%`; PRESSURE x101")]),
  ("m2", "Then the dark starts to sparkle: around 3 in 4 animals here make their own light.",
   [(1.2, "bioluminescent dots; STAT `~3 IN 4 GLOW`")]),
  ("m3", "Problem three: something glowing drifts up to your face. An anglerfish, small enough for your palm.",
   [(0.0, "TAG `PROBLEM 3: THE NEIGHBOURS`"), (4.0, "SCALEBAR ~0.2 M")]),
  ("m5", "But here's the thing. None of that was ever the real problem.",
   [(1.2, "grade to near-black")]),
  ("m6", "The real problem has been killing you since the ferry, and it's on screen right now.",
   [(2.6, "BODY readout flies from the HUD to centre: 33.9°C, red")]),
  ("m7", "Your blood. 37 degrees, remember? The water here is 4.",
   [(0.0, "STAT 37°C (red) vs STAT WATER 4°C (blue)")]),
  ("m8", "Gills swap heat too. Your blood leaves them as cold as the sea.",
   [(0.0, "GILL DIAGRAM heat mode: red heat dots leave with the water")]),
  ("m9", "At the surface, you were losing heat about 30 times faster than you make it.",
   [(0.8, "STAT `SURFACE: x30`")]),
  ("m10", "Here, it's a hundred. Your gills are a radiator, and the ocean is the room.",
   [(0.2, "STAT `HERE: x100` (~10 KW vs ~100 W)"), (2.4, "radiator icon replaces the slits; heat lines into the ocean")]),
  ("m11", "Hypothermia starts at 35 degrees. You passed it a while ago.",
   [(0.0, "BODY readout with the 35° HYPOTHERMIA line; TAG `PASSED AT ~200 M`")]),
  ("m12", "Down here, you've got minutes.",
   [(2.8, "frost tint, small tremble")]),
 ]),
 ("L6 REAL ANALOGUE -> FIX 3", 207, [
  ("f1", "Except a few fish cheat the cold, and their cheat is real.",
   [(0.0, "TAG `REAL ANIMAL: BLUEFIN TUNA`")]),
  ("f2", "In a bluefin tuna, warm blood heading out hands its heat to cold blood coming in, through a tangle of tiny vessels.",
   [(0.0, "TUNA cutaway: vessel tangle in the swimming muscle, warm red <-> cold blue")]),
  ("f3", "It's your gill trick run backwards, saving heat instead of grabbing oxygen.",
   [(0.6, "the gill counter-current strip slides in beside it with labels flipped")]),
  ("f4", "So your third fix: a tuna's heat exchanger, between your gills and the rest of you.",
   [(1.0, "coil between the gill slits and the torso; HUD BORROWED 3: HEAT EXCHANGER (TUNA); BODY readout climbs")]),
  ("f5", "The readout stops falling. But tuna stay warm by never stopping, and now neither can you.",
   [(2.0, "TAG `STOP SWIMMING = FREEZE`")]),
 ]),
 ("L7 2,000 M · THE HUNTING GROUND (MIDPOINT)", 207, [
  ("n1", "2,000 metres. A click hits you so hard you feel it in your teeth.",
   [(0.0, "STAMP `2,000 M · THE HUNTING GROUND`; PRESSURE x201")]),
  ("n2", "Then faster and faster, until the clicks blur into a buzz.",
   [(0.0, "click rings tighten into a buzz")]),
  ("n3", "That's a sperm whale. When its clicks become a buzz, it's closing in on something.",
   [(0.6, "SPERM WHALE glides in; SCALEBAR ~16 M"), (4.4, "TAG `CLICKS -> BUZZ = CLOSING IN`")]),
  ("n4", "You're warm, you're moving, and you're about the size of what it eats.", []),
  ("n6", "The buzz hits you in the chest. Then the whale turns away.", []),
  ("n7", "It wanted a giant squid, with eyes as wide as dinner plates. You don't make the cut.",
   [(0.0, "GIANT SQUID at shared scale; STAT `GIANT SQUID · EYE ~27 CM`")]),
  ("n8", "Here's the problem nobody warned you about: every fix makes you better at the deep, and worse at everything else.",
   [(0.0, "three fix icons orbit YOU; TAG `BETTER DEEP · WORSE EVERYWHERE ELSE`")]),
  ("n9", "Many deep fish brought up to the surface don't survive the trip. You're turning into one.",
   [(0.0, "a deep fish rises on a line and comes apart"), (3.2, "HUD line `WAY BACK: ?`")]),
 ]),
 ("L8 4,000 M · THE ABYSS (PRESSURE)", 207, [
  ("a1", "4,000 metres. You land on the floor of the Pacific: mud, cold, and 400 atmospheres.",
   [(0.0, "STAMP `4,000 M · THE ABYSS`; PRESSURE x401; DAYS chip `DAY 1`")]),
  ("a2", "Your gills are fine. Your molecules are not.", []),
  ("a3", "Pressure this strong squeezes your proteins out of shape. Your hands shake. Your thoughts slow.",
   [(0.0, "protein ribbon squashes; nerve sparks")]),
  ("a4", "In 1992, a diver in a French chamber survived the pressure of 701 metres, a human record.",
   [(0.3, "DATE CHIP 1992; DepthMeter mark 701 M")]),
  ("a5", "You're almost 6 times deeper. But deep fish carry a molecule called TMAO that props proteins back into shape.",
   [(0.0, "SPEEDBARS 701 M vs 4,000 M"), (2.4, "TAG `TMAO (FROM DEEP FISH)`")]),
  ("a6", "Your fourth fix: you pack your cells with it. The shaking stops.",
   [(0.3, "HUD BORROWED 4: TMAO (DEEP FISH)")]),
  ("a7", "But there's a ceiling: the deeper you go, the more you need, and around 8,200 metres your cells get as concentrated as the sea.",
   [(0.0, "TMAO-vs-depth line climbs to the dashed `AS CONCENTRATED AS SEAWATER` line at 8,200 M")]),
  ("a8", "In 2014, scientists predicted that's where fish run out. It's the wall on your route.",
   [(0.0, "DATE CHIP 2014"), (2.4, "HUD red 8,200 mark pulses: `THE WALL`")]),
 ]),
 ("L9 THE ABYSS PLAIN · LOW POINT -> TURN", 207, [
  ("w1", "The trench is still days away. So you walk.",
   [(0.0, "STAMP `DAY 4 · THE ABYSS PLAIN`; map inset: dashed line two-thirds done")]),
  ("w2", "Then a brand-new problem: you're starving.", []),
  ("w3", "Staying warm burns food, and about 1 percent of what grows in sunlight ever reaches this mud.",
   [(2.4, "STAT `~1% OF SUNLIT FOOD REACHES THE FLOOR`")]),
  ("w4", "The remora has gone quiet.", [(0.0, "REMORA chip: QUIET")]),
  ("w5", "So, honestly, where could you live?", [(0.0, "OPTIONS `WHERE COULD YOU LIVE?` OPEN OCEAN · ABYSS · VENT · REEF")]),
  ("w6", "The open ocean? Nothing to eat. The abyss? You're in it.", [(0.8, "strike OPEN OCEAN"), (2.4, "strike ABYSS")]),
  ("w7", "Unless you find a vent, a hot spring on the seafloor crowded with life.",
   [(0.6, "VENT tile (hypothetical); chip ALVIN · 1977")]),
  ("w8", "But your best home is a coral reef, 30 metres down, still in the sunshine.",
   [(0.6, "REEF tile; select REEF")]),
  ("w9", "Except you can't go back up. Not in a body tuned for the abyss.",
   [(0.0, "red ✗ over the REEF tile: `CAN'T GO BACK UP`")]),
  ("w10", "And then, ahead of you, the floor just ends.", [(1.8, "the mud edge drops into black")]),
 ]),
 ("L10 CLIMAX · THE LINE -> CHALLENGER DEEP", 207, [
  ("x1", "8,200 metres. The trench walls close in.",
   [(0.0, "STAMP `8,200 M · THE LINE`; DAYS 5")]),
  ("x2", "Right at the line, a pale fish drifts past like a wet tissue. A snailfish.", []),
  ("x3", "One trench north, in 2022, a camera filmed its cousin at 8,336 metres. No fish has ever been seen deeper.",
   [(0.5, "MAP pin IZU-OGASAWARA TRENCH; DATE CHIP 2022; DepthMeter mark 8,336 M beside the red 8,200")]),
  ("x4", "This is the wall. There's no animal left to borrow from.",
   [(0.5, "HUD BORROWED flips to `NO FIX LEFT` (red)")]),
  ("x5", "The remora lets go and drifts back up toward the light.",
   [(0.0, "REMORA chip: LEAVING -> GONE")]),
  ("x6", "From here on, this is our guess, not known science.", [(0.0, "TAG `BEYOND KNOWN BIOLOGY`")]),
  ("x7", "You can stay at the line, where your body still makes sense. Or pay for the last 2,700 metres with the only thing you have left: the way back.",
   [(0.0, "two tiles: STAY AT THE LINE / GO DOWN 2,700 M · COST: THE WAY BACK")]),
  ("x8", "You keep packing your cells past the limit. They swell with sea. They hold.", [(0.0, "cells swell")]),
  ("x9", "And they'll never work in the shallows again.", [(0.0, "HUD line `WAY BACK: GONE`")]),
  ("x10", "You go down.", [(0.8, "HOLD: descent ramp, DepthMeter races 8,200 -> 10,900")]),
 ]),
 ("L10b THE FLOOR", 207, [
  ("x11", "10,935 metres. Challenger Deep.", [(0.0, "STAMP `10,935 M · CHALLENGER DEEP`; DAYS 6")]),
  ("x12", "No light. No sound. Just a puff of grey mud where you land.", []),
  ("x13", "Over 1,000 atmospheres: a small car parked on each of your thumbnails.",
   [(0.0, "PRESSURE x1,000+"), (1.8, "CAR on a thumbnail; STAT `~1.1 T / CM²`")]),
  ("x14", "And finally, food. Amphipods, little shrimp-like scavengers, swarm over anything that sinks.",
   [(2.0, "amphipods converge")]),
  ("x15", "Down here, you're the thing that sank.", []),
  ("x16", "You eat them. They nibble you back. Fair.", []),
  ("x17", "In 2019, scientists opened up amphipods from this trench. Every single one had man-made fibres in its gut.",
   [(0.3, "DATE CHIP 2019"), (3.6, "magnifier on one amphipod: coloured fibres; STAT `100% HAD MAN-MADE FIBRES`")]),
  ("x18", "Your first meal in 6 days, and your world got to it first.", [(0.0, "one coloured fibre drifts past your face")]),
 ]),
 ("L11 BOOKEND + VERDICT + RECAP", 207, [
  ("b1", "You look up. 11 kilometres above you, the ferry is still crossing. The remora is up there somewhere.",
   [(0.0, "camera rides up the whole column to the tiny ferry; REMORA chip: UP THERE SOMEWHERE")]),
  ("b2", "So, could you breathe underwater? Yes. That part's easy.", [(1.4, "HEADLINE `YES.`")]),
  ("b3", "You'd need gills, salt pumps, a tuna's heat exchanger and a deep fish's chemistry. And you'd pay with the way home.",
   [(0.0, "RECAP STRIP: 4 borrowed fixes + a red `WAY BACK ✗`")]),
  ("b4", "Getting in was never the hard part. Getting out is.", [(0.0, "HEADLINE on the trench floor")]),
 ]),
 ("L12 CTA + SERIES LOOP", 207, [
  ("e1", "So, back at that ferry rail: would you jump? And where would you stop: the reef, the vent, or the line?",
   [(0.0, "END CARD from the ferry rail: REEF · VENT · THE LINE")]),
  ("e2", "Want to see what happens when you try to swim back up? Tell me.",
   [(0.0, "TAG `NEXT: SWIM BACK UP?`")]),
 ]),
]

# ------------------------------------------------------------------ TTS spelling

ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def say_int(n):
    if n < 20:
        return ONES[n]
    if n < 100:
        return TENS[n // 10] + ("" if n % 10 == 0 else "-" + ONES[n % 10])
    if n < 1000:
        r = n % 100
        return ONES[n // 100] + " hundred" + ("" if r == 0 else " and " + say_int(r))
    th, r = divmod(n, 1000)
    s = say_int(th) + " thousand"
    if r == 0:
        return s
    if r < 100:
        return s + " and " + say_int(r)
    return s + " " + say_int(r)


def say_year(y):
    a, b = divmod(y, 100)
    if b == 0:
        return say_int(a) + " hundred"
    return say_int(a) + " " + (say_int(b) if b >= 10 else "oh " + say_int(b))


def tts(text):
    t = text.replace("TMAO", "T-M-A-O").replace("percent", "percent")
    t = re.sub(r"\b(19\d\d|20\d\d)\b", lambda m: say_year(int(m.group(1))), t)
    t = re.sub(r"\b\d{1,3}(?:,\d{3})+\b|\b\d+\b", lambda m: say_int(int(m.group(0).replace(",", ""))), t)
    return t


def spoken_words(text):
    return len(re.findall(r"[A-Za-z']+", tts(text).replace("-", " ")))


def wc(s):
    return len(s.split())

# ------------------------------------------------------------------ timing


LINES = {}
order = []
t = 0.0
for label, rate, lines in SECTIONS:
    for lid, text, os_ in lines:
        sw = spoken_words(text)
        n_sent = max(1, len(re.findall(r"[.?!:](?:\s|$)", text)))
        meas = MEASURED.get(lid)
        if meas and meas["tts"] == tts(text):
            dur = meas["raw_" + TTS_SPEED] - RAW_PAD + KEEP_PAD
            src = "measured"
        else:
            dur = sw * 60.0 / rate + SENT_PAUSE * (n_sent - 1) + KEEP_PAD
            src = "model"
        LINES[lid] = dict(id=lid, text=text, tts=tts(text), os=os_, start=round(t, 2), dur=round(dur, 2),
                          end=round(t + dur, 2), section=label, rate=rate, spoken=sw, src=src)
        order.append(lid)
        t += dur + GAP + (FLOOR_EXTRA_GAP if label.startswith("L10b") else 0.0)
        if lid == "t0":
            # title card: VO over the card, card held at least TITLE_MIN
            t = max(t, LINES["t0"]["start"] + TITLE_MIN)
        if lid == "x10":
            t += RAMP_HOLD
    t += SECTION_GAP
NARRATION_END = LINES["e2"]["end"]
RUNTIME = round(NARRATION_END + END_HOLD, 1)
TITLE_START = LINES["t0"]["start"]
TITLE_END = round(TITLE_START + max(TITLE_MIN, LINES["t0"]["dur"] + 0.3), 2)
RAMP_START = round(LINES["x10"]["end"] + 0.1, 2)
RAMP_END = round(RAMP_START + RAMP_HOLD, 2)


def mmss(x):
    x = max(0.0, x)
    return f"{int(x // 60)}:{int(x % 60):02d}"


def mmss1(x):
    x = max(0.0, x)
    return f"{int(x // 60)}:{x % 60:04.1f}"


def T(ref):
    """'lid' or 'lid+off' -> global seconds."""
    lid, _, off = ref.partition("+")
    return LINES[lid]["start"] + float(off or 0)

# ------------------------------------------------------------------ metrics (PLAYBOOK §9 regexes)


ALL_TEXT = [LINES[i]["text"] for i in order]
SENTS = []
for s in ALL_TEXT:
    SENTS += [p.strip() for p in re.split(r"(?<=[.?!])\s+", s) if p.strip()]
YOU = re.compile(r"\b(you|your|you're|yourself|yours|you've|you'd|you'll)\b", re.I)
PIV = re.compile(r"\b(but|except|until|unless|here's|problem|catch|though|instead|turns out)\b", re.I)
NUMW = re.compile(r"\b(\d[\d,.]*|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|billion|half|quarter|percent)\b", re.I)
total_words = sum(wc(s) for s in ALL_TEXT)
narr_min = NARRATION_END / 60
run_min = RUNTIME / 60
piv_hits = [(lid, m.group(0)) for lid in order for m in PIV.finditer(LINES[lid]["text"])]
num_hits = [(lid, m.group(0)) for lid in order for m in NUMW.finditer(LINES[lid]["text"])]
M = dict(
    words=total_words,
    spoken_words=sum(LINES[i]["spoken"] for i in order),
    sentences=len(SENTS),
    mean_sentence=round(total_words / len(SENTS), 1),
    punch_pct=round(100 * sum(1 for s in SENTS if wc(s) <= 3) / len(SENTS), 1),
    second_person_pct=round(100 * sum(1 for s in SENTS if YOU.search(s)) / len(SENTS), 1),
    second_person_sentences=sum(1 for s in SENTS if YOU.search(s)),
    you_words=sum(len(YOU.findall(s)) for s in ALL_TEXT),
    pivots=len(piv_hits),
    pivots_per_min=round(len(piv_hits) / run_min, 2),
    questions=sum(s.count("?") for s in ALL_TEXT),
    numbers=len(num_hits),
    numbers_per_min=round(len(num_hits) / run_min, 1),
    wpm_overall=round(total_words / run_min, 1),
    wpm_narration=round(total_words / narr_min, 1),
    narration_end=round(NARRATION_END, 1),
    runtime=RUNTIME,
    runtime_if_10pct_slower=round(RUNTIME + (sum(LINES[i]["dur"] for i in order)) * (SLOW_FACTOR - 1), 1),
    lines_measured=sum(1 for i in order if LINES[i]["src"] == "measured"),
    lines_total=len(order),
)
if MEASURED and all(i in MEASURED and "raw_1.2" in MEASURED[i] for i in order):
    # same layout, Kokoro speed 1.2 (fit intercept 0.524 s)
    M["runtime_at_speed_1.2"] = round(RUNTIME + sum((MEASURED[i]["raw_1.2"] - 0.524) - (MEASURED[i]["raw_1.25"] - RAW_PAD) for i in order), 1)
M["you_per_100"] = round(100 * M["you_words"] / total_words, 1)
hook_ids = [lid for lid, _, _ in SECTIONS[0][2]]
M["hook_words"] = sum(wc(LINES[i]["text"]) for i in hook_ids)
M["hook_end"] = LINES["c9"]["end"]
M["first_sentence_words"] = wc(LINES["c1"]["text"])
M["fine_at"] = LINES["c2"]["start"]
M["you_first_30s"] = sum(len(YOU.findall(LINES[i]["text"])) for i in order if LINES[i]["start"] < 30)
spoken_time = sum(LINES[i]["dur"] for i in order)
M["tts_wpm_assumed"] = round(M["spoken_words"] / (spoken_time / 60), 1)

# ------------------------------------------------------------------ HUD state tables (global time)
# Generator rule: every scene except the title, verdict/recap and end cards carries one whatif/Hud layer;
# its props are the state at the scene start plus tracks/changes inside the scene, in scene-local seconds.

DEPTH_KEYS = [("c1", 0), ("c9+0.3", 0), ("g1", 8), ("h1", 200), ("h4+0.5", 238), ("h4+3.5", 262), ("m1", 1000),
              ("n1", 2000), ("a1", 4000), ("w10+1.8", 4000), ("w10+3.4", 6000), ("x1", 8200), ("x10+0.8", 8200),
              ("x11", 10935)]
TEMP_KEYS = [("c1", 37.0), ("c3", 37.0), ("r5", 36.8), ("h1", 35.1), ("h4+0.5", 34.9), ("h11", 34.6), ("m1", 34.3), ("m6+2.6", 33.9),
             ("f4+1.0", 33.7), ("f5", 35.0), ("n1", 36.2)]
BORROWED = [("c1", 0, ""), ("g8+2.4", 1, "GILLS"), ("h8+1.0", 2, "SALT PUMPS"), ("f4+1.0", 3, "HEAT EXCHANGER"),
            ("a6+0.3", 4, "TMAO"), ("x4+0.5", -1, "NO FIX LEFT")]
DAYS = [("c1", None), ("a1", 1), ("w1", 4), ("x1", 5), ("x11", 6)]
REMORA = [("c1", ""), ("c4+1.6", "ATTACHED"), ("g7", "RELIEVED"), ("h6", "UNBOTHERED"), ("m3+4.5", "HIDING"),
          ("n4+1.0", "RELOCATING"), ("w4", "QUIET"), ("x5", "LEAVING"), ("x5+3.0", "GONE"), ("b1+4.0", "UP THERE SOMEWHERE")]
WAYBACK = [("c1", ""), ("n9+3.2", "?"), ("w9", "SHRINKING"), ("x9", "GONE")]
MARKS = [  # DepthMeter marks (kit edit: DepthMeter `marks` prop)
    dict(d=200, label="200", at="c8"), dict(d=1000, label="1,000", at="c8+0.4"), dict(d=2000, label="2,000", at="c8+0.8"),
    dict(d=4000, label="4,000", at="c8+1.2"), dict(d=8200, label="8,200 · THE WALL", color="red", at="c8+1.6"),
    dict(d=10935, label="10,935", at="c8+2.0"), dict(d=253, label="253 · BREATH-HOLD RECORD", color="yellow", at="h4+0.5"),
    dict(d=701, label="701 · HUMAN PRESSURE RECORD", color="yellow", at="a4+0.3"),
    dict(d=8336, label="8,336 · DEEPEST FISH", color="yellow", at="x3+0.5"),
]


def interp(keys, g):
    pts = [(T(k), v) for k, v in keys]
    if g <= pts[0][0]:
        return pts[0][1]
    for (t0, v0), (t1, v1) in zip(pts, pts[1:]):
        if t0 <= g <= t1:
            return v0 if t1 == t0 else v0 + (v1 - v0) * (g - t0) / (t1 - t0)
    return pts[-1][1]


def track(keys, s0, s1, dec=0):
    """Scene-local track: value at start, every key inside, value at end."""
    pts = [(0.0, interp(keys, s0))]
    for k, v in keys:
        g = T(k)
        if s0 < g < s1:
            pts.append((round(g - s0, 2), v))
    pts.append((round(s1 - s0, 2), interp(keys, s1)))
    out = []
    for tt, v in pts:
        out.append({"t": tt, "v": round(v, dec) if dec else int(round(v)), "ease": "linear"})
    return out


def step_state(table, g):
    cur = table[0][1:] if len(table[0]) > 2 else table[0][1]
    for row in table:
        if T(row[0]) <= g + 1e-6:
            cur = row[1:] if len(row) > 2 else row[1]
    return cur


def changes(table, s0, s1):
    out = []
    for row in table:
        g = T(row[0])
        if s0 < g < s1:
            out.append((round(g - s0, 2), row[1:] if len(row) > 2 else row[1]))
    return out


def hud_props(s0, s1, focus=None):
    n, lab = step_state(BORROWED, s0)
    p = {
        "depth": track(DEPTH_KEYS, s0, s1),
        "pressure": "auto",   # x(1 + depth/10), rounded; '1,000+' above 9,990 m
        "bodyTemp": track(TEMP_KEYS, s0, s1, dec=1),
        "tempWarnBelow": 35.0,
        "borrowed": {"n": n, "label": lab},
        "days": step_state(DAYS, s0),
        "remora": step_state(REMORA, s0),
        "wayBack": step_state(WAYBACK, s0),
        "marks": [dict({k: v for k, v in m.items() if k != "at"}, at=max(0.0, round(T(m["at"]) - s0, 2)))
                  for m in MARKS if T(m["at"]) < s1],
        "changes": [],
    }
    for at, (nn, ll) in changes(BORROWED, s0, s1):
        p["changes"].append({"at": at, "borrowed": {"n": nn, "label": ll}})
    for key, table in (("days", DAYS), ("remora", REMORA), ("wayBack", WAYBACK)):
        for at, v in changes(table, s0, s1):
            p["changes"].append({"at": at, key: v})
    p["changes"].sort(key=lambda c: c["at"])
    if focus:
        p["focus"] = focus
    return p

# ------------------------------------------------------------------ storyboard helpers


RED = "#E5484D"; BLUE = "#5BB8E8"; WHITE = "#F3F6F7"; YELLOW = "#FFD84D"; MUD = "#3A3128"; PALE = "#E9EEF0"
BOARD_PANEL = {"type": "rect", "fill": "rgba(4,16,24,0.72)", "radius": 28, "x": "55%", "y": "47%", "width": 1440, "height": 760, "depth": 0, "z": 5}


def comp(name, props=None, **kw):
    d = {"type": "component", "name": name, "props": props or {}}
    d.update(kw)
    return d


def ocean(**props):
    return {"type": "component", "name": "explainer/Ocean", "props": props}


def you(pose="stand", x="55%", y="55%", pxPerM=120, **kw):
    lk = {k: kw.pop(k) for k in list(kw) if k in ("start", "end", "keyframes", "rotate", "flipX", "idle", "z", "opacity", "enter", "exit", "depth")}
    p = {"pose": pose, "pxPerM": pxPerM, "color": WHITE}
    p.update(kw)
    box = max(500, int(pxPerM * 2.1))  # YOU is 1.75 m tall; keep the true-scale figure inside its box
    return comp("explainer/You", p, x=x, y=y, width=box, height=box, **lk)


def creature(name, pxPerM, x, y, w, h, **kw):
    lk = {k: kw.pop(k) for k in list(kw) if k in ("start", "end", "keyframes", "rotate", "flipX", "idle", "z", "opacity", "enter", "exit", "depth", "scale")}
    p = {"pxPerM": pxPerM}
    p.update(kw)
    return comp(f"explainer/{name}", p, x=x, y=y, width=w, height=h, **lk)


def fish(species, x, y, w=420, h=200, **kw):
    """NEW whatif/Fish: one parametrised figure (remora | tuna | snailfish | deepfish), optional cutaway."""
    lk = {k: kw.pop(k) for k in list(kw) if k in ("start", "end", "keyframes", "rotate", "flipX", "idle", "z", "opacity", "enter", "exit", "depth", "scale")}
    p = {"species": species}
    p.update(kw)
    return comp("whatif/Fish", p, x=x, y=y, width=w, height=h, **lk)


def tag(text, at=0.3, x="55%", y="20%", accent=None, out=None, size=None):
    p = {"text": text, "at": at, "align": "center"}
    if accent:
        p["accent"] = accent
    if out is not None:
        p["out"] = out
    if size:
        p["size"] = size
    return comp("explainer/Tag", p, x=x, y=y, width=1200, height=100, depth=0, z=70)


def stat(value, label, at=0.3, x="55%", y="44%", sub=None, color=None, w=1000):
    p = {"value": value, "label": label, "at": at}
    if sub:
        p["sub"] = sub
    if color:
        p["color"] = color
    return comp("explainer/Stat", p, x=x, y=y, width=w, height=320, depth=0, z=60)


def bars(rows, title=None, at=0.3, y="50%", mx=None):
    p = {"rows": rows, "at": at, "stagger": 0.6}
    if mx is not None:
        p["max"] = mx
    if title:
        p["title"] = title
    return comp("explainer/SpeedBars", p, x="55%", y=y, width=1300, height=420, depth=0, z=50)


def stamp(num, sub, at=0.0):
    """Chapter stamp: Headline with the number in red + grey sub line, held ~2.1 s."""
    if num.startswith("DAY"):
        text, red = num, [num.split()[1]]
    else:
        text, red = f"{num} M", [num]
    return comp("explainer/Headline", {"text": text, "red": red, "sub": sub, "size": 132, "at": at, "out": at + 2.1},
                x="55%", y="45%", width=1500, height=360, depth=0, z=95)


def svg(markup, x="55%", y="50%", w=800, h=500, **kw):
    d = {"type": "svg", "markup": markup, "x": x, "y": y, "width": w, "height": h}
    d.update(kw)
    return d


def ring(at, x="55%", y="50%", size=1800, dur=0.9, color="rgba(220,240,255,0.7)"):
    """A sperm-whale click: a stroked circle that expands and fades (core circle layer)."""
    return {"type": "circle", "fill": "rgba(0,0,0,0)", "stroke": color, "strokeWidth": 6, "x": x, "y": y,
            "width": size, "height": size, "start": at, "end": at + dur, "depth": 0.6,
            "keyframes": [{"t": at, "scale": 0.05, "opacity": 1}, {"t": at + dur, "scale": 1.0, "opacity": 0, "ease": "out"}]}


def mapview(views, pins=None, at=0, x="74%", y="62%", w=760, h=430):
    return comp("explainer/Map", {"views": views, "pins": pins or [], "at": at}, x=x, y=y, width=w, height=h, depth=0, z=40)


def cam(preset=None, amount=1.0, keys=None, shake=None):
    c = {"preset": preset or "none", "amount": amount}
    if keys:
        c["keyframes"] = keys
    if shake:
        c["shake"] = shake
    return c


# small inline SVGs (flat, original, code-drawn)
SEAFLOOR = ('<svg viewBox="0 0 1920 300" xmlns="http://www.w3.org/2000/svg"><path d="M0 120 Q240 80 480 110 T960 100 T1440 115 T1920 95 V300 H0Z" fill="#2E2A24"/>'
            '<path d="M0 150 Q300 120 640 145 T1300 140 T1920 135 V300 H0Z" fill="#3A3128"/></svg>')
SEAFLOOR_EDGE = ('<svg viewBox="0 0 1920 400" xmlns="http://www.w3.org/2000/svg"><path d="M0 160 Q300 130 620 150 T1100 145 L1180 170 L1240 400 H0Z" fill="#3A3128"/>'
                 '<path d="M1180 170 L1240 400 H1920 V400Z" fill="#05080B"/></svg>')
TRENCH_L = '<svg viewBox="0 0 600 1080" xmlns="http://www.w3.org/2000/svg"><path d="M0 0 H420 L380 200 L450 420 L360 650 L430 860 L380 1080 H0Z" fill="#141A1E"/></svg>'
TRENCH_R = '<svg viewBox="0 0 600 1080" xmlns="http://www.w3.org/2000/svg"><path d="M600 0 H180 L230 230 L150 430 L240 640 L170 870 L220 1080 H600Z" fill="#141A1E"/></svg>'
PROTEIN = ('<svg viewBox="0 0 600 240" xmlns="http://www.w3.org/2000/svg"><path d="M20 120 C80 20 140 220 200 120 S320 20 380 120 S500 220 580 120" '
           'fill="none" stroke="#F2A541" stroke-width="22" stroke-linecap="round"/></svg>')
TMAO_DOTS = ('<svg viewBox="0 0 600 240" xmlns="http://www.w3.org/2000/svg">' + "".join(
    f'<circle cx="{40 + i * 58}" cy="{60 if i % 2 else 180}" r="14" fill="#7FE0C2"/>' for i in range(10)) + '</svg>')
TMAO_CHART = ('<svg viewBox="0 0 900 520" xmlns="http://www.w3.org/2000/svg"><g stroke="#9FB3BF" stroke-width="3" fill="none">'
              '<path d="M80 40 V460 H860"/></g><path d="M80 420 L300 360 L520 280 L700 200 L780 170" stroke="#7FE0C2" stroke-width="8" fill="none"/>'
              '<path d="M80 160 H860" stroke="#E5484D" stroke-width="4" stroke-dasharray="18 12"/>'
              '<text x="470" y="140" fill="#E5484D" font-family="Montserrat" font-weight="800" font-size="30" text-anchor="middle">AS CONCENTRATED AS SEAWATER · ~8,200 M</text>'
              '<text x="470" y="505" fill="#C9D6DD" font-family="Montserrat" font-weight="700" font-size="26" text-anchor="middle">DEPTH →</text>'
              '<text x="30" y="250" fill="#C9D6DD" font-family="Montserrat" font-weight="700" font-size="26" transform="rotate(-90 30 250)" text-anchor="middle">TMAO IN YOUR CELLS</text></svg>')
VENT_TILE = ('<svg viewBox="0 0 520 360" xmlns="http://www.w3.org/2000/svg"><rect width="520" height="360" rx="20" fill="#0B1418"/>'
             '<path d="M230 360 L245 170 L275 170 L290 360Z" fill="#3B332C"/><path d="M260 170 C230 120 290 90 255 30" stroke="#8C949A" stroke-width="26" fill="none" opacity=".5"/>'
             + "".join(f'<path d="M{150 + i * 35} 360 V{250 - (i % 3) * 25}" stroke="#E9EEF0" stroke-width="7"/><circle cx="{150 + i * 35}" cy="{246 - (i % 3) * 25}" r="10" fill="#E5484D"/>' for i in range(7)) + '</svg>')
REEF_TILE = ('<svg viewBox="0 0 520 360" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4FC3D9"/><stop offset="1" stop-color="#1B6F86"/></linearGradient></defs>'
             '<rect width="520" height="360" rx="20" fill="url(#g)"/><path d="M0 360 V300 Q60 230 110 300 Q150 210 210 300 Q260 240 320 300 Q380 220 430 300 Q480 250 520 290 V360Z" fill="#F28C6B"/>'
             + "".join(f'<ellipse cx="{70 + i * 60}" cy="{120 + (i % 3) * 40}" rx="16" ry="8" fill="#FFD84D"/>' for i in range(7)) + '</svg>')
JAR_MOUSE = ('<svg viewBox="0 0 420 460" xmlns="http://www.w3.org/2000/svg"><rect x="70" y="60" width="280" height="370" rx="40" fill="rgba(140,200,230,.25)" stroke="#CFE8F2" stroke-width="8"/>'
             '<rect x="60" y="40" width="300" height="34" rx="10" fill="#9FB3BF"/><ellipse cx="210" cy="260" rx="70" ry="38" fill="#C9D0D4"/><circle cx="270" cy="240" r="26" fill="#C9D0D4"/>'
             '<path d="M140 270 Q100 300 90 250" stroke="#C9D0D4" stroke-width="8" fill="none"/></svg>')
LUNG_PIPE = ('<svg viewBox="0 0 600 420" xmlns="http://www.w3.org/2000/svg"><path d="M300 20 V160" stroke="#E9EEF0" stroke-width="26"/>'
             '<path d="M300 160 C200 160 150 240 160 380 C240 400 290 330 300 170Z M300 160 C400 160 450 240 440 380 C360 400 310 330 300 170Z" fill="#E58A8A"/>'
             '<path d="M250 40 V130 M230 110 L250 135 L270 110" stroke="#5BB8E8" stroke-width="10" fill="none"/><path d="M350 130 V40 M330 60 L350 35 L370 60" stroke="#5BB8E8" stroke-width="10" fill="none"/></svg>')
BUBBLE = '<svg viewBox="0 0 360 220" xmlns="http://www.w3.org/2000/svg"><path d="M30 20 H330 Q350 20 350 40 V140 Q350 160 330 160 H120 L70 210 L80 160 H30 Q10 160 10 140 V40 Q10 20 30 20Z" fill="#F3F6F7"/><text x="180" y="115" font-family="Montserrat" font-weight="900" font-size="64" text-anchor="middle" fill="#13202A">...</text></svg>'
RADIATOR = ('<svg viewBox="0 0 360 260" xmlns="http://www.w3.org/2000/svg">' + "".join(f'<rect x="{30 + i * 50}" y="40" width="34" height="180" rx="14" fill="#E5484D"/>' for i in range(6))
            + "".join(f'<path d="M{47 + i * 50} 30 q12 -14 0 -28" stroke="#F2A541" stroke-width="6" fill="none"/>' for i in range(6)) + '</svg>')
COIL = '<svg viewBox="0 0 300 160" xmlns="http://www.w3.org/2000/svg"><path d="M10 80 C40 10 70 150 100 80 S160 10 190 80 S250 150 290 80" stroke="#E5484D" stroke-width="14" fill="none"/><path d="M10 95 C40 25 70 165 100 95 S160 25 190 95 S250 165 290 95" stroke="#5BB8E8" stroke-width="14" fill="none"/></svg>'
CELLS = '<svg viewBox="0 0 600 300" xmlns="http://www.w3.org/2000/svg">' + "".join(f'<circle cx="{70 + (i % 5) * 115}" cy="{80 + (i // 5) * 140}" r="48" fill="rgba(127,224,194,.35)" stroke="#7FE0C2" stroke-width="6"/>' for i in range(10)) + '</svg>'
FIBRES = ('<svg viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg"><circle cx="150" cy="150" r="140" fill="rgba(240,230,210,.15)" stroke="#F3F6F7" stroke-width="8"/>'
          '<path d="M70 160 C110 120 150 200 210 140" stroke="#E5484D" stroke-width="6" fill="none"/><path d="M90 190 C140 170 170 210 230 180" stroke="#5BB8E8" stroke-width="6" fill="none"/>'
          '<path d="M100 120 C140 100 180 130 220 110" stroke="#FFD84D" stroke-width="6" fill="none"/></svg>')
WATER_ARROWS = ('<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg"><path d="M20 120 H170 M140 95 L172 120 L140 145" stroke="#5BB8E8" stroke-width="12" fill="none"/>'
                '<path d="M230 180 H380 M350 155 L382 180 L350 205" stroke="#5BB8E8" stroke-width="12" fill="none"/></svg>')
STRIKE = {"type": "rect", "fill": RED, "x": "50%", "y": "6%", "width": 1920, "height": 10, "depth": 0.5, "z": 30,
          "keyframes": [{"t": 0.0, "scaleX": 0.0}, {"t": 0.5, "scaleX": 1.0, "ease": "out"}]}


def local(ref, s0):
    return round(T(ref) - s0, 2)

# ------------------------------------------------------------------ shot list
# Each shot: anchor (line id + offset), type, description (kit vocabulary), camera, sfx, storyboard layers.
# Times inside layers use 'lid+off' strings and are converted to scene-local seconds.

PX = 120  # px per metre for the human-scale shots (YOU = 210 px tall)

SHOTS = [
 # ---------------- L1 cold open
 dict(id="s01-fall", at="c1", type="STORY wide, split waterline",
      desc="`explainer/Ocean` `surface: 0.35`, dusk `skyTop` violet / `skyBottom` orange; NEW `whatif/Ferry` slides right->left along the waterline with a lit deck rail; `You` `pose: panic` just under the surface in a `particles` bubbles burst; HUD from frame 1 (DEPTH 0 M, BODY 37.0); `Tag` WESTERN PACIFIC",
      cam=cam(shake=[{"at": 0.0, "duration": 0.4, "amplitude": 14}]), cam_txt="`shake` 0.4 s on the fall, then hold", sfx=[("impact", 0.0, 0.9), ("bubbles", 0.2, 0.7)], sfx_txt="`impact` splash; `bubbles` until the fine beat",
      bg=ocean(depth=2, surface=0.35, skyTop="#4B3C78", skyBottom="#F2A15C", rays=3, snow=20),
      layers=lambda s: [comp("whatif/Ferry", {"lights": True}, x="60%", y="31%", width=900, height=260, depth=0.3, keyframes=[{"t": 0, "x": "70%"}, {"t": s["dur"], "x": "52%", "ease": "linear"}]),
                        you("panic", x="48%", y="52%"), {"type": "particles", "preset": "bubbles", "count": 140, "x": "48%", "y": "55%", "width": 600, "height": 700, "end": local("c2", s["start"]), "speed": 1.6},
                        tag("WESTERN PACIFIC", at=0.4, x="22%", y="88%", size=34)]),
 dict(id="s02-fine", at="c2", type="STORY medium underwater",
      desc="Bubbles gone; `You` relaxes to `pose: stand`, floating upright (`idle` float); a slow chest-rise `svg` arc pulses (`idle` breathe); light from above flickers",
      cam=cam("pushIn", 0.4), cam_txt="slow `pushIn`", sfx=[("heartbeat_slow", 1.0, 0.5)], sfx_txt="bubbles cut dead; `heartbeat_slow`",
      bg=ocean(depth=4, surface=0.12, rays=6, snow=30),
      layers=lambda s: [you("stand", x="50%", y="58%", idle=[{"type": "float", "amount": 10, "speed": 0.3}])]),
 dict(id="s03-remora", at="c4", type="STORY medium, companion intro",
      desc="NEW `whatif/Fish` `species: remora` (~0.6 m, shared `pxPerM`) swims in from the left and latches on between `You`'s shoulders; HUD REMORA chip `ATTACHED` pops",
      cam=cam("pushIn", 0.3), cam_txt="`pushIn` on the latch", sfx=[("pop", 1.6, 0.6)], sfx_txt="`pop` on the latch",
      bg=ocean(depth=6, surface=0.1, rays=6, snow=30),
      layers=lambda s: [you("stand", x="50%", y="58%"), fish("remora", "44%", "50%", 220, 90, pxPerM=PX, keyframes=[{"t": 0, "x": "-10%"}, {"t": 1.6, "x": "45%", "ease": "out"}])]),
 dict(id="s04-ferry-leaves", at="c5", type="STORY wide, split waterline (POV stand-in)",
      desc="The 0:00 split frame again: the `whatif/Ferry` shrinks by keyframes (scale 1 -> 0.35) while tiny deck-rail `circle` heads stay lit; `You` small below the waterline with the remora",
      cam=cam("panUp", 0.3), cam_txt="small `panUp`", sfx=[("underwater_rumble", 0.0, 0.5)], sfx_txt="`underwater_rumble` (engine) fading",
      bg=ocean(depth=3, surface=0.35, skyTop="#3B2F66", skyBottom="#E58F55", rays=3, snow=20),
      layers=lambda s: [comp("whatif/Ferry", {"lights": True}, x="58%", y="31%", width=900, height=260, depth=0.3, keyframes=[{"t": 0, "scale": 1}, {"t": s["dur"], "scale": 0.35}]),
                        you("stand", x="45%", y="66%", pxPerM=80), fish("remora", "44.3%", "62%", 150, 60, pxPerM=80)]),
 dict(id="s05-air-rule", at="c6", type="STORY medium, rule beat",
      desc="`You` reaches up toward the bright surface line; a red `rect` strike draws across the surface (the one-way rule); `Tag` AIR: DOESN'T WORK FOR YOU",
      cam=cam(), cam_txt="static", sfx=[("tick", 0.6, 0.6)], sfx_txt="`tick` on the strike",
      bg=ocean(depth=8, surface=0.08, rays=6, snow=30),
      layers=lambda s: [you("point", x="50%", y="62%"), dict(STRIKE, start=0.6, keyframes=[{"t": 0.6, "scaleX": 0.0}, {"t": 1.1, "scaleX": 1.0, "ease": "out"}]),
                        tag("AIR: DOESN'T WORK FOR YOU", at=0.6, y="24%", accent="red")]),
 dict(id="s06-route-map", at="c7", type="GRAPHIC map + stat",
      desc="`Stat` 4,000 M TO THE FLOOR; then `explainer/Map` inset (western Pacific, zoom 3): pin YOU, dashed 300 KM line, pin CHALLENGER DEEP",
      cam=cam("pullOut", 0.3), cam_txt="`pullOut`", sfx=[("tick", 0.4, 0.5), ("ding", 3.0, 0.5)], sfx_txt="`tick`, `ding` on the pin",
      bg=ocean(depth=60, rays=4, snow=40),
      layers=lambda s: [stat(4000, "M TO THE FLOOR", at=0.4, x="40%", y="40%"),
                        mapview([{"t": 0, "lon": 143.5, "lat": 12.5, "zoom": 3}], pins=[{"lon": 144.6, "lat": 13.9, "label": "YOU", "at": 3.0}, {"lon": 142.2, "lat": 11.35, "label": "CHALLENGER DEEP · ~300 KM", "at": 3.6}], at=2.8)]),
 dict(id="s07-route-ruler", at="c8", type="GRAPHIC full-height ruler (route)",
      desc="HUD `focus: route`: the DepthMeter grows to full frame height, `max: 11000`; route marks light one by one 200 · 1,000 · 2,000 · 4,000 · **8,200 (red, THE WALL?)** · 10,935 (kit edit: DepthMeter `marks`)",
      cam=cam("pullOut", 0.2), cam_txt="`pullOut`", sfx=[("tick", 0.0, 0.5), ("tick", 0.4, 0.5), ("tick", 0.8, 0.5), ("tick", 1.2, 0.5), ("stinger", 1.6, 0.5), ("tick", 2.0, 0.5)], sfx_txt="`tick` x5, soft `stinger` on the red line",
      bg=ocean(depth=300, rays=0, snow=40), hud_focus="route", layers=lambda s: []),
 dict(id="s08-go-down", at="c9", type="STORY vertical descent",
      desc="`You` rotated head-down (`rotate: 160`, `pose: run` as a kick) with the remora on its back; Ocean `depth` track starts (HUD meter leaves 0 for good)",
      cam=cam("panDown", 0.6), cam_txt="`panDown`", sfx=[("whoosh", 0.3, 0.6), ("riser", 0.6, 0.5)], sfx_txt="`whoosh`; `riser` into the title",
      bg="auto", layers=lambda s: [you("run", x="50%", y="50%", rotate=160), fish("remora", "50%", "47%", 220, 90, pxPerM=PX, rotate=160)]),
 # ---------------- L2
 dict(id="s09-title", at="t0", type="TITLE card (VO over it, no dead hold)",
      desc="`explainer/Headline` WHAT IF YOU COULD / BREATHE UNDERWATER? (`red: [UNDERWATER?]`, underline) over Ocean `depth: 25`, `snow: 60`; HUD hidden for the card",
      cam=cam(), cam_txt="static", sfx=[("stinger", 0.0, 0.6)], sfx_txt="`stinger`; music hit", hud=False,
      bg=ocean(depth=25, rays=5, snow=60),
      layers=lambda s: [comp("explainer/Headline", {"text": "WHAT IF YOU COULD\nBREATHE UNDERWATER?", "red": ["UNDERWATER?"], "underline": True, "size": 104, "at": 0.0}, x="50%", y="46%", width=1600, height=420, depth=0, z=90)]),
 dict(id="s10-rule-change", at="r1", type="RULE card",
      desc="`You` floating with water `svg` arrows in through the mouth and out at the neck; `Tag` ONE CHANGE: OXYGEN FROM WATER",
      cam=cam("drift"), cam_txt="`drift`", sfx=[("whoosh", 1.2, 0.4)], sfx_txt="soft `whoosh`",
      bg="auto", layers=lambda s: [you("stand", x="40%", y="58%"), svg(WATER_ARROWS, x="47%", y="44%", w=300, h=220, start=1.2), tag("ONE CHANGE: OXYGEN FROM WATER", at=1.2, x="62%", y="22%")]),
 dict(id="s11-rule-promise", at="r2", type="RULE card",
      desc="`explainer/Options` title THE RULES, items EVERY THREAT -> A REAL ANIMAL'S FIX · UNTIL THERE ISN'T ONE (`itemAt` synced, second item drawn with a red `Tag` overlay)",
      cam=cam(), cam_txt="static", sfx=[("pop", 0.4, 0.5), ("pop", "r3", 0.6)], sfx_txt="`pop` per rule",
      bg="auto", layers=lambda s: [BOARD_PANEL, comp("explainer/Options", {"title": "THE RULES", "items": ["EVERY THREAT -> A REAL ANIMAL'S FIX", "UNTIL THERE ISN'T ONE"], "itemAt": [0.4, "r3"], "size": 54}, x="55%", y="47%", width=1300, height=520, depth=0, z=60),
                                   tag("UNTIL THERE ISN'T ONE", at="r3", x="55%", y="62%", accent="red")]),
 dict(id="s12-stays-human", at="r4", type="RULE card + plant",
      desc="`Options` STAYS HUMAN: SKIN · EYES · 37°C BLOOD (`stagger 0.8`); at r5 a pointer `circle` ring lands on the HUD BODY readout (36.8 and falling)",
      cam=cam("pushIn", 0.2), cam_txt="static, small `pushIn`", sfx=[("pop", 0.0, 0.4), ("pop", 0.8, 0.4), ("pop", 1.6, 0.4), ("ding", "r5", 0.6)], sfx_txt="`pop` x3; `ding` on the plant",
      bg="auto", layers=lambda s: [BOARD_PANEL, comp("explainer/Options", {"title": "STAYS HUMAN", "items": ["SOFT SKIN", "DAYLIGHT EYES", "37°C BLOOD"], "stagger": 0.8, "size": 56}, x="55%", y="47%", width=1200, height=520, depth=0, z=60),
                                   {"type": "circle", "fill": "rgba(0,0,0,0)", "stroke": YELLOW, "strokeWidth": 6, "x": 250, "y": 300, "width": 230, "height": 230, "depth": 0, "z": 99, "start": local("r5", s["start"]), "idle": [{"type": "pulse", "amount": 0.08, "speed": 1.2}]}]),
 # ---------------- L3 grounding (meter 0 -> 200 m)
 dict(id="s13-oxygen", at="g1", type="BOARD diagram (register switch)",
      desc="Dark panel `rect` over the descending Ocean (meter keeps moving); `SpeedBars` OXYGEN PER LITRE: AIR 100 vs SEAWATER 3 (`text` ~1/30)",
      cam=cam(), cam_txt="`cut` in; static", sfx=[("tick", 0.8, 0.5)], sfx_txt="`tick` on the bars",
      bg="auto", layers=lambda s: [BOARD_PANEL, bars([{"label": "AIR", "value": 100, "text": "1"}, {"label": "SEAWATER", "value": 3, "text": "~1/30", "color": "red"}], "OXYGEN PER LITRE", at=0.8)]),
 dict(id="s14-flow", at="g2", type="BOARD diagram",
      desc="`SpeedBars` THROUGH YOU EVERY MINUTE: AIR 6 L vs WATER 60 L; at g3 a `Timer` ring 2:30 spins next to `Tag` 1 BATHTUB",
      cam=cam("pushIn", 0.2), cam_txt="slow `pushIn`", sfx=[("bubbles", 0.6, 0.4), ("tick", "g3+0.3", 0.5)], sfx_txt="`bubbles` (filling)",
      bg="auto", layers=lambda s: [BOARD_PANEL, bars([{"label": "AIR (LUNGS)", "value": 6, "unit": "L"}, {"label": "WATER (YOU NOW)", "value": 60, "unit": "L", "color": "red"}], "THROUGH YOU EVERY MINUTE", at=0.6, y="40%", mx=60),
                                   comp("explainer/Timer", {"from": 0, "to": 150, "at": "g3+0.3", "rate": 40, "style": "ring", "format": "mm:ss", "label": "1 BATHTUB"}, x="55%", y="72%", width=260, height=260, depth=0, z=60)]),
 dict(id="s15-lungs", at="g4", type="BOARD diagram",
      desc="Inline `svg` lung with one pipe and arrows in AND out; a red ✗ `Tag` SAME PIPE IN AND OUT",
      cam=cam(), cam_txt="static", sfx=[("impact", 1.6, 0.4)], sfx_txt="light `impact` on the ✗",
      bg="auto", layers=lambda s: [BOARD_PANEL, svg(LUNG_PIPE, x="55%", y="50%", w=560, h=400, start=0.3, enter={"type": "pop"}), tag("✗ SAME PIPE IN AND OUT", at=1.6, y="80%", accent="red")]),
 dict(id="s16-mouse", at="g5", type="HISTORY vignette",
      desc="Inline `svg` jar + mouse silhouette in liquid on the dark panel; date `Tag` 1966; the mouse's chest `idle` breathe",
      cam=cam("pushIn", 0.3), cam_txt="`pushIn`", sfx=[("ding", 0.3, 0.6), ("bubbles", 1.0, 0.3)], sfx_txt="`ding` on the date; quiet `bubbles`",
      bg="auto", layers=lambda s: [BOARD_PANEL, svg(JAR_MOUSE, x="50%", y="52%", w=380, h=420, idle=[{"type": "breathe", "amount": 0.02, "speed": 0.6}]), tag("1966", at=0.3, x="70%", y="30%", accent="yellow", size=60)]),
 dict(id="s17-no-voice", at="g6", type="STORY gag beat",
      desc="`You` close, mouth-open pose (`panic`); an empty speech-bubble `svg` with `...` pops; at g7 the remora chip reads RELIEVED and the `whatif/Fish` remora does a little `idle` sway",
      cam=cam("pushIn", 0.4), cam_txt="`pushIn`", sfx=[("pop", 1.4, 0.5)], sfx_txt="silence beat, `pop` on the bubble",
      bg="auto", layers=lambda s: [you("panic", x="45%", y="60%", pxPerM=180), svg(BUBBLE, x="62%", y="34%", w=360, h=220, start=1.4, enter={"type": "pop"}),
                                   fish("remora", "41%", "52%", 300, 120, pxPerM=180, idle=[{"type": "sway", "amount": 6, "speed": 1.4}], start=0.0)]),
 dict(id="s18-gills", at="g8", type="DIAGRAM (gills)",
      desc="NEW `whatif/GillDiagram` `mode: oxygen`: head profile (circle head at close scale) with three slit strokes drawing on behind the jaw at g8+2.4; then one-way arrows mouth -> gills (conveyor texture) and the two-lane counter-current strip WATER -> / <- BLOOD with dots crossing; HUD BORROWED 1",
      cam=cam("drift"), cam_txt="`drift`, then `pushIn` on the strip", sfx=[("pop", 2.4, 0.6), ("ding", 2.6, 0.5), ("whoosh", "g9", 0.4)], sfx_txt="`pop` + `ding` on the fix; `whoosh` on the arrows",
      bg="auto", layers=lambda s: [BOARD_PANEL, comp("whatif/GillDiagram", {"mode": "oxygen", "slitsAt": 2.4, "flowAt": local("g9", s["start"])}, x="55%", y="48%", width=1300, height=640, depth=0, z=50)]),
 dict(id="s19-extraction", at="g10", type="BOARD diagram",
      desc="`SpeedBars` OXYGEN TAKEN: GILLS 80% vs LUNGS 25%",
      cam=cam(), cam_txt="static", sfx=[("pop", 0.6, 0.5)], sfx_txt="`pop` on the bars",
      bg="auto", layers=lambda s: [BOARD_PANEL, bars([{"label": "YOUR GILLS", "value": 80, "unit": "%", "color": "green"}, {"label": "YOUR OLD LUNGS", "value": 25, "unit": "%"}], "OXYGEN TAKEN FROM EACH BREATH", at=0.6, mx=100)]),
 dict(id="s20-easy-except", at="g11", type="STORY wide (false resolution)",
      desc="`You` swimming down easily; `Tag` EASY. then a red `Tag` EXCEPT... replaces it; the HUD BODY readout blinks once (HUD `blink: temp` change)",
      cam=cam("panDown", 0.3), cam_txt="slow `panDown`", sfx=[("tick", 0.7, 0.6)], sfx_txt="one `tick` on EXCEPT",
      bg="auto", layers=lambda s: [you("run", x="50%", y="55%", rotate=150), fish("remora", "50%", "52%", 220, 90, pxPerM=PX, rotate=150),
                                   tag("EASY.", at=0.0, out=0.7, y="22%"), tag("EXCEPT...", at=0.7, y="22%", accent="red")], hud_blink=0.7),
 # ---------------- L4 honeymoon 200 m
 dict(id="s21-200m", at="h1", type="STAMP + wide sunlit zone",
      desc="Stamp 200 M · THE LAST LIGHT; Ocean (auto depth) `rays: 7`, `snow: 40`; `You` swimming down (rotated 75°) with the remora",
      cam=cam("panDown", 0.3), cam_txt="`panDown` slow", sfx=[("whoosh", 0.0, 0.6)], sfx_txt="`whoosh` on the stamp",
      bg="auto", layers=lambda s: [stamp("200", "THE LAST LIGHT"), you("run", x="45%", y="62%", rotate=75), fish("remora", "44%", "59%", 220, 90, pxPerM=PX, rotate=75)]),
 dict(id="s22-pressure", at="h2", type="STORY inset comparison",
      desc="Inset left: `Diver` with an air-bubble `circle` that shrinks by keyframes (scale 1 -> 0.3) as PRESSURE ticks x1 -> x21; inset right: `You` with a water glyph that stays the same size",
      cam=cam(), cam_txt="static", sfx=[("tick", 0.5, 0.3), ("tick", 1.5, 0.3), ("tick", 2.5, 0.3)], sfx_txt="light `tick` per atmosphere",
      bg="auto", layers=lambda s: [creature("Diver", 70, "35%", "56%", 400, 400, bubbles=False), {"type": "circle", "fill": "rgba(230,245,255,0.5)", "x": "35%", "y": "45%", "width": 120, "height": 120, "depth": 0.8, "keyframes": [{"t": 0.5, "scale": 1}, {"t": s["dur"], "scale": 0.3}]},
                                   you("stand", x="72%", y="56%"), {"type": "circle", "fill": "rgba(91,184,232,0.5)", "x": "72%", "y": "47%", "width": 120, "height": 120, "depth": 0.8}]),
 dict(id="s23-ears", at="h3", type="STORY close-up",
      desc="`You` head close (`pxPerM` 300); short water `svg` arrows into the ear and nose; `Tag` EARS + SINUSES: FLOODED",
      cam=cam("pushIn", 0.3), cam_txt="`pushIn`", sfx=[("bubbles", 1.6, 0.3)], sfx_txt="soft `bubbles`",
      bg="auto", layers=lambda s: [you("stand", x="50%", y="78%", pxPerM=300), svg(WATER_ARROWS, x="58%", y="30%", w=260, h=190, start=1.6), tag("EARS + SINUSES: FLOODED", at=1.6, y="18%")]),
 dict(id="s24-record", at="h4", type="HUD close-up",
      desc="HUD `focus: meter` with DepthMeter `window: 400`; the yellow mark 253 M · BREATH-HOLD RECORD appears and the YOU marker slides past it",
      cam=cam("pushIn", 0.3), cam_txt="`pushIn` on the ruler", sfx=[("tick", 0.5, 0.6), ("whoosh", 3.0, 0.5)], sfx_txt="`tick`; `whoosh` as it passes",
      bg="auto", hud_focus="meter", layers=lambda s: []),
 dict(id="s25-bluewhale", at="h5", type="STORY wide, scale",
      desc="`BlueWhale` passes beneath, left -> right, same `pxPerM` (14) as `You`; two `Bus` silhouettes end to end in a lower inset; `ScaleBar` ~28 M",
      cam=cam("panRight", 0.5), cam_txt="`panRight` tracking the whale", sfx=[("underwater_rumble", 0.0, 0.6)], sfx_txt="`underwater_rumble` swell",
      bg="auto", layers=lambda s: [creature("BlueWhale", 14, "50%", "70%", 520, 160, keyframes=[{"t": 0, "x": "20%"}, {"t": s["dur"], "x": "75%", "ease": "linear"}]),
                                   you("stand", x="58%", y="38%", pxPerM=14), creature("Bus", 14, "40%", "90%", 180, 60), creature("Bus", 14, "50%", "90%", 180, 60),
                                   comp("explainer/ScaleBar", {"label": "~28 M", "at": 2.0}, x="50%", y="82%", width=392, height=40, depth=0, z=60)]),
 dict(id="s26-salt", at="h7", type="BOARD diagram (problem 1)",
      desc="`Tag` PROBLEM 1: SALT; `SpeedBars` SALT: SEAWATER ~35 G/L vs YOUR BLOOD ~9 G/L",
      cam=cam(), cam_txt="`cut`; static", sfx=[("tick", 0.0, 0.5), ("tick", 3.4, 0.5)], sfx_txt="`tick` on the problem",
      bg="auto", layers=lambda s: [BOARD_PANEL, tag("PROBLEM 1: SALT", at=0.0, y="18%", accent="red"), bars([{"label": "SEAWATER", "value": 35, "unit": " G/L", "color": "red"}, {"label": "YOUR BLOOD", "value": 9, "unit": " G/L"}], "SALT", at=3.4)]),
 dict(id="s27-salt-fix", at="h8", type="DIAGRAM (gills, salt mode)",
      desc="`whatif/GillDiagram` `mode: salt`: white salt dots leave through cells on the gill strip; HUD BORROWED 2",
      cam=cam("pushIn", 0.2), cam_txt="`pushIn`", sfx=[("pop", 1.0, 0.5), ("ding", 1.2, 0.5)], sfx_txt="`pop` + `ding`",
      bg="auto", layers=lambda s: [BOARD_PANEL, comp("whatif/GillDiagram", {"mode": "salt", "slitsAt": 0}, x="55%", y="48%", width=1300, height=640, depth=0, z=50)]),
 dict(id="s28-light", at="h9", type="STORY wide (problem 2)",
      desc="`Tag` PROBLEM 2: LIGHT; `Stat` LIGHT 1%; the auto-depth Ocean fades the rays as the meter passes ~300 m",
      cam=cam("panDown", 0.3), cam_txt="slow `panDown`", sfx=[("tick", 0.0, 0.5)], sfx_txt="`tick`",
      bg="auto", layers=lambda s: [tag("PROBLEM 2: LIGHT", at=0.0, y="18%", accent="red"), stat("1%", "OF THE SUNLIGHT REACHES HERE", at=0.4, y="42%"),
                                   you("stand", x="58%", y="70%", pxPerM=80)]),
 dict(id="s29-fingertips", at="h11", type="STORY insert (the crack)",
      desc="Two `You` layers crossfade (`color` #F3F6F7 -> pale blue #CFE3F2) with opacity keyframes; `Tag` FINGERTIPS: WHITE; the HUD BODY readout reads 34.6, already below the 35 line (nobody says so yet)",
      cam=cam("pushIn", 0.4), cam_txt="`pushIn`", sfx=[("heartbeat_slow", 0.2, 0.5)], sfx_txt="`heartbeat_slow`",
      bg="auto", layers=lambda s: [you("shrug", x="50%", y="64%", pxPerM=200), you("shrug", x="50%", y="64%", pxPerM=200, color="#CFE3F2", keyframes=[{"t": 0, "opacity": 0}, {"t": 1.6, "opacity": 1}]),
                                   tag("FINGERTIPS: WHITE", at=0.0, y="20%")]),
 # ---------------- L5 1,000 m + rug pull
 dict(id="s30-1000m", at="m1", type="STAMP + wide black water", trans={"type": "dipBlack", "duration": 0.5},
      desc="`dipBlack` into the stamp 1,000 M · MIDNIGHT; Ocean depth ~1,000 (black), `snow: 30`; `Stat` LIGHT 0%",
      cam=cam("drift"), cam_txt="`drift`", sfx=[("whoosh", 0.0, 0.5)], sfx_txt="music drops to `drone`",
      bg="auto", layers=lambda s: [stamp("1,000", "MIDNIGHT"), stat("0%", "SUNLIGHT", at=2.2, y="70%"), you("stand", x="60%", y="62%", pxPerM=80)]),
 dict(id="s31-glow", at="m2", type="STORY wide (wonder)",
      desc="`particles` `stars` preset in cyan/blue blinking around `You` (bioluminescence); `Stat` ~3 IN 4 GLOW",
      cam=cam("drift"), cam_txt="`drift`", sfx=[("ding", 1.2, 0.2), ("ding", 2.4, 0.2)], sfx_txt="soft `ding` blips with the glows",
      bg="auto", layers=lambda s: [{"type": "particles", "preset": "stars", "count": 160, "color": "#6FE3FF", "speed": 0.4, "start": 1.0, "depth": 0.8},
                                   you("stand", x="55%", y="60%", pxPerM=80), stat("~3 IN 4", "ANIMALS HERE MAKE LIGHT", at=1.2, y="24%")]),
 dict(id="s32-angler", at="m3", type="STORY close, scale (problem 3)",
      desc="`Tag` PROBLEM 3: THE NEIGHBOURS; `Anglerfish` (lure glow) rises to `You`'s face at the same `pxPerM` (300); `ScaleBar` ~0.2 M beside the open hand; at m4 the remora slides behind the head (keyframes)",
      cam=cam("pushIn", 0.4), cam_txt="slow `pushIn`", sfx=[("pop", 2.0, 0.5)], sfx_txt="`pop` on the lure",
      bg="auto", layers=lambda s: [tag("PROBLEM 3: THE NEIGHBOURS", at=0.0, y="16%", accent="red"), you("stand", x="42%", y="80%", pxPerM=300),
                                   creature("Anglerfish", 300, "62%", "52%", 300, 200, keyframes=[{"t": 0, "y": "90%"}, {"t": 3.0, "y": "52%", "ease": "out"}]),
                                   fish("remora", "48%", "46%", 260, 110, pxPerM=300, keyframes=[{"t": 0, "x": "48%"}, {"t": 4.5, "x": "48%"}, {"t": 5.5, "x": "36%"}]),
                                   comp("explainer/ScaleBar", {"label": "~0.2 M", "at": 4.0}, x="62%", y="66%", width=60, height=40, depth=0, z=60)]),
 dict(id="s33-rugpull", at="m5", type="RUG PULL (grade + HUD fly-in)",
      desc="Frame grades to near-black (`grade` vignette 0.6, brightness 0.6); at m6+2.6 HUD `focus: temp` flies the BODY readout to centre, big, red (33.9°C)",
      cam=cam("pushIn", 0.8), cam_txt="hard `pushIn` on the readout", sfx=[("stinger", 1.2, 0.8), ("heartbeat", 2.0, 0.6)], sfx_txt="`stinger` + `heartbeat`",
      bg="auto", grade={"brightness": 0.6, "vignette": 0.6}, hud_focus_at=("temp", "m6+2.6"), layers=lambda s: [you("stand", x="55%", y="64%", pxPerM=80, opacity=0.6)]),
 dict(id="s34-blood-vs-water", at="m7", type="BOARD numbers",
      desc="`Stat` 37°C (red) left vs `Stat` WATER 4°C (blue) right",
      cam=cam(), cam_txt="static", sfx=[("pop", 0.0, 0.5), ("pop", 2.4, 0.5)], sfx_txt="`pop` x2",
      bg="auto", layers=lambda s: [BOARD_PANEL, stat("37°C", "YOUR BLOOD", at=0.0, x="38%", color="red", w=560), stat("4°C", "THE WATER", at=2.4, x="72%", color=BLUE, w=560)]),
 dict(id="s35-heat", at="m8", type="DIAGRAM (gills, heat mode)",
      desc="`whatif/GillDiagram` `mode: heat`: red heat dots leave with the water stream; at m9 `Stat` SURFACE: x30 small, at m10 `Stat` HERE: x100 (sub ~10 KW vs ~100 W)",
      cam=cam("pullOut", 0.3), cam_txt="`pullOut`", sfx=[("whoosh_long", 0.0, 0.5)], sfx_txt="`whoosh_long`",
      bg="auto", layers=lambda s: [BOARD_PANEL, comp("whatif/GillDiagram", {"mode": "heat", "slitsAt": 0}, x="55%", y="44%", width=1200, height=560, depth=0, z=50),
                                   stat("x30", "SURFACE: HEAT LOST vs MADE", at="m9+0.8", x="40%", y="80%", w=560), stat("x100", "DOWN HERE", at="m10+0.2", x="72%", y="80%", sub="~10 KW vs ~100 W", color="red", w=560)]),
 dict(id="s36-radiator", at="m10+2.4", type="DIAGRAM metaphor",
      desc="Radiator `svg` icon replaces the gill slits on `You`'s neck; wavy heat lines drift out into a wide black ocean",
      cam=cam("pullOut", 0.6), cam_txt="`pullOut` (the room is the ocean)", sfx=[("whoosh_long", 0.0, 0.4)], sfx_txt="`whoosh_long`",
      bg="auto", layers=lambda s: [you("stand", x="50%", y="64%", pxPerM=160), svg(RADIATOR, x="55%", y="40%", w=240, h=180, enter={"type": "pop"})]),
 dict(id="s37-hypothermia", at="m11", type="HUD close + body",
      desc="HUD `focus: temp` with the 35° HYPOTHERMIA line on the readout scale (readout 33.8, blinking); `Tag` PASSED AT ~200 M; at m12+2.8 frost-blue tint `rect` fades in and `You` gets an `idle` jitter",
      cam=cam(shake=[{"at": 4.0, "duration": 1.0, "amplitude": 4}]), cam_txt="static, small `shake` on 'minutes'", sfx=[("heartbeat_slow", 0.0, 0.6)], sfx_txt="`heartbeat_slow` slowing",
      bg="auto", hud_focus="temp", layers=lambda s: [tag("PASSED AT ~200 M", at=0.6, x="60%", y="80%", accent="red"),
                                                    {"type": "rect", "fill": "#9CC9F0", "x": "50%", "y": "50%", "width": 1920, "height": 1080, "depth": 0, "z": 80, "blend": "multiply", "keyframes": [{"t": 0, "opacity": 0}, {"t": local("m12+2.8", s["start"]), "opacity": 0}, {"t": local("m12+3.6", s["start"]), "opacity": 0.35}]}]),
 # ---------------- L6 tuna
 dict(id="s38-tuna", at="f1", type="REAL-ANIMAL vignette", trans={"type": "whip", "duration": 0.35, "direction": "left"},
      desc="`whip` in; NEW `whatif/Fish` `species: tuna` (~2.5 m) crosses at mid-depth; `Tag` REAL ANIMAL: BLUEFIN TUNA",
      cam=cam("panLeft", 0.4), cam_txt="`panLeft` with the fish", sfx=[("whoosh", 0.0, 0.6)], sfx_txt="`whoosh`",
      bg=ocean(depth=400, rays=2, snow=40), layers=lambda s: [fish("tuna", "50%", "55%", 700, 260, pxPerM=110, keyframes=[{"t": 0, "x": "85%"}, {"t": s["dur"], "x": "35%", "ease": "linear"}]), tag("REAL ANIMAL: BLUEFIN TUNA", at=0.0, y="18%")]),
 dict(id="s39-retia", at="f2", type="DIAGRAM cutaway",
      desc="`whatif/Fish` tuna `cutaway: true`: the vessel tangle in the red swimming muscle, counter-flow arrows warm red <-> cold blue; at f3+0.6 the gill counter-current strip (GillDiagram `mode: strip`, `flip: true`) slides in beside it with its labels flipped (callback)",
      cam=cam("drift"), cam_txt="`drift`", sfx=[("tick", "f3+0.6", 0.5)], sfx_txt="`tick` on the flip",
      bg="auto", layers=lambda s: [BOARD_PANEL, fish("tuna", "40%", "45%", 760, 300, cutaway=True), comp("whatif/GillDiagram", {"mode": "strip", "flip": True}, x="72%", y="70%", width=560, height=220, depth=0, z=55, start=local("f3+0.6", s["start"]), enter={"type": "slideLeft"})]),
 dict(id="s40-exchanger", at="f4", type="STORY close (fix 3)",
      desc="`You` torso close with a coil `svg` (red/blue lanes) between the neck slits and the chest; tint `rect` warms back; HUD BORROWED 3; BODY readout climbs",
      cam=cam("pushIn", 0.4), cam_txt="`pushIn`", sfx=[("pop", 1.0, 0.6), ("ding", 1.2, 0.6)], sfx_txt="`pop`; `ding`",
      bg="auto", layers=lambda s: [you("stand", x="50%", y="72%", pxPerM=260), svg(COIL, x="51%", y="36%", w=280, h=150, start=1.0, enter={"type": "wipeRight"})]),
 dict(id="s41-keep-swimming", at="f5", type="STORY wide",
      desc="`You` kicking hard downward (`pose: run`, rotated), remora on board; `Tag` STOP SWIMMING = FREEZE",
      cam=cam("panDown", 0.5), cam_txt="`panDown`", sfx=[("whoosh", 2.0, 0.4)], sfx_txt="`whoosh`",
      bg="auto", layers=lambda s: [you("run", x="50%", y="55%", rotate=160), fish("remora", "50%", "52%", 220, 90, pxPerM=PX, rotate=160), tag("STOP SWIMMING = FREEZE", at=2.0, y="20%", accent="red")]),
 # ---------------- L7 2,000 m
 dict(id="s42-2000m-click", at="n1", type="STAMP + clicks",
      desc="Stamp 2,000 M · THE HUNTING GROUND; full-frame expanding `circle` stroke rings (one per click), `shake` 0.15 s on each; at n2 the rings come faster until they blur",
      cam=cam(shake=[{"at": 1.8, "duration": 0.2, "amplitude": 10}, {"at": 3.6, "duration": 0.2, "amplitude": 10}]), cam_txt="`shake` on each click", sfx=[("click", 1.8, 1.0), ("click", 3.6, 1.0), ("click", "n2+0.8", 0.9), ("click", "n2+1.5", 0.9), ("click", "n2+2.0", 0.9), ("click", "n2+2.4", 0.9), ("sonar_ping", "n2+2.8", 0.5)], sfx_txt="`click` (loud) accelerating; `sonar_ping` tail",
      bg="auto", layers=lambda s: [stamp("2,000", "THE HUNTING GROUND"), ring(1.8), ring(3.6)] + [ring(local(f"n2+{o}", s["start"])) for o in (0.8, 1.5, 2.0, 2.4, 2.7, 2.9, 3.1)] + [you("stand", x="55%", y="60%", pxPerM=80)]),
 dict(id="s43-spermwhale", at="n3", type="STORY wide, scale (threat)",
      desc="`SpermWhale` (`jaw: 4`) glides toward `You` at shared `pxPerM` (60); `ScaleBar` ~16 M; `Tag` CLICKS -> BUZZ = CLOSING IN",
      cam=cam("panLeft", 0.4), cam_txt="`panLeft` tracking", sfx=[("click", 0.4, 0.8), ("click", 1.6, 0.8), ("click", 2.6, 0.8)], sfx_txt="`click` x3",
      bg="auto", layers=lambda s: [creature("SpermWhale", 60, "60%", "52%", 1000, 260, jaw=4, flipX=True, keyframes=[{"t": 0, "x": "95%"}, {"t": s["dur"], "x": "62%", "ease": "linear"}]),
                                   you("stand", x="22%", y="56%", pxPerM=60), comp("explainer/ScaleBar", {"label": "~16 M", "at": 0.6}, x="62%", y="78%", width=960, height=40, depth=0, z=60),
                                   tag("CLICKS -> BUZZ = CLOSING IN", at=4.4, y="16%", accent="red")]),
 dict(id="s44-in-the-beam", at="n4", type="STORY medium (threat)",
      desc="`You` small in the whale's path; ring layers converge on `You` (buzz); at n5 the remora slides around to the far side (keyframes)",
      cam=cam("pushIn", 0.5), cam_txt="`pushIn`", sfx=[("click", 0.0, 0.7), ("click", 0.3, 0.7), ("click", 0.5, 0.7), ("click", 0.7, 0.7), ("click", 0.9, 0.7)], sfx_txt="buzz (rapid `click`)",
      bg="auto", layers=lambda s: [ring(0.0, x="40%"), ring(0.3, x="40%"), ring(0.6, x="40%"), ring(0.9, x="40%"), ring(1.2, x="40%"),
                                   you("stand", x="40%", y="58%", pxPerM=140), fish("remora", "40%", "52%", 200, 80, pxPerM=140, keyframes=[{"t": 0, "x": "37%"}, {"t": 1.0, "x": "37%"}, {"t": 2.0, "x": "44%"}]),
                                   creature("SpermWhale", 60, "88%", "50%", 1000, 260, jaw=6, flipX=True)]),
 dict(id="s45-turns-away", at="n6", type="STORY wide",
      desc="One last ring hits `You` full-frame; the whale banks away (rotate + x keyframes) into the dark",
      cam=cam(shake=[{"at": 0.2, "duration": 0.4, "amplitude": 14}]), cam_txt="`shake` on the buzz hit", sfx=[("boom", 0.2, 0.6)], sfx_txt="`boom` (low) on the hit",
      bg="auto", layers=lambda s: [ring(0.1, x="40%", size=2400), you("stand", x="40%", y="58%", pxPerM=60),
                                   creature("SpermWhale", 60, "70%", "50%", 1000, 260, flipX=True, keyframes=[{"t": 1.5, "x": "70%", "rotate": 0}, {"t": s["dur"], "x": "110%", "rotate": -14}])]),
 dict(id="s46-giant-squid", at="n7", type="STORY wide, scale",
      desc="Giant squid stand-in: kit `ColossalSquid` figure with `hooks: false`, `scale` 1.1 to read as ~10 m at the shared `pxPerM` (60); eye-ring highlight + a dinner-plate `circle` icon; `Stat` GIANT SQUID · EYE ~27 CM",
      cam=cam("pushIn", 0.3), cam_txt="slow `pushIn` on the eye", sfx=[("underwater_rumble", 0.0, 0.5)], sfx_txt="`underwater_rumble`",
      bg="auto", layers=lambda s: [creature("ColossalSquid", 60, "55%", "50%", 600, 180, hooks=False, scale=1.1), {"type": "circle", "fill": "rgba(0,0,0,0)", "stroke": YELLOW, "strokeWidth": 5, "x": "47%", "y": "47%", "width": 70, "height": 70, "depth": 1, "start": 1.0},
                                   stat("~27 CM", "GIANT SQUID EYE · A DINNER PLATE", at=1.2, y="78%"), you("stand", x="85%", y="60%", pxPerM=60)]),
 dict(id="s47-midpoint", at="n8", type="GRAPHIC (midpoint re-hook)",
      desc="`You` centre with three small fix icons (slits, salt dots, coil) orbiting (`idle` spin on a group `svg`); `Tag` BETTER DEEP · WORSE EVERYWHERE ELSE",
      cam=cam("pushIn", 0.3), cam_txt="`pushIn`", sfx=[("stinger", 0.0, 0.5)], sfx_txt="soft `stinger`",
      bg="auto", layers=lambda s: [you("stand", x="55%", y="60%", pxPerM=160), svg(COIL, x="40%", y="40%", w=160, h=90, start=0.4), svg(RADIATOR, x="70%", y="40%", w=150, h=110, start=0.8, opacity=0.6),
                                   tag("BETTER DEEP · WORSE EVERYWHERE ELSE", at=3.0, y="16%", accent="red")]),
 dict(id="s48-way-back", at="n9", type="STORY vertical (stranding plant)",
      desc="A `whatif/Fish` `species: deepfish` rises on a thin line toward a bright surface band; it loses shape (scaleY keyframes 1 -> 0.4, opacity down); HUD WAY BACK: ? appears",
      cam=cam("panUp", 0.4), cam_txt="`panUp` with the fish", sfx=[("riser", 0.0, 0.4), ("tick", 3.2, 0.6)], sfx_txt="`riser`; `tick` on WAY BACK",
      bg="auto", layers=lambda s: [{"type": "rect", "fill": "#C9D6DD", "x": "50%", "y": "30%", "width": 3, "height": 700, "depth": 1},
                                   fish("deepfish", "50%", "70%", 300, 140, keyframes=[{"t": 0, "y": "75%", "scaleY": 1, "opacity": 1}, {"t": 3.0, "y": "25%", "scaleY": 0.4, "opacity": 0.4}]),
                                   tag("HOLD ON TO THAT", at=local("n9+3.6", s["start"]), y="85%")]),
 # ---------------- L8 4,000 m
 dict(id="s49-4000m", at="a1", type="STAMP + wide seafloor",
      desc="Stamp 4,000 M · THE ABYSS; seafloor `svg` (mud mounds) along the bottom; `You` lands (`align: bottom`) with a `dust` particles puff; PRESSURE x401; DAYS chip DAY 1 appears",
      cam=cam("pushIn", 0.3), cam_txt="`pushIn`", sfx=[("impact", 1.0, 0.4), ("underwater_rumble", 0.0, 0.5)], sfx_txt="soft `impact` on landing",
      bg="auto", layers=lambda s: [stamp("4,000", "THE ABYSS"), svg(SEAFLOOR, x="50%", y="86%", w=1920, h=300, depth=0.9), you("stand", x="56%", y="70%", pxPerM=80, align="bottom"),
                                   {"type": "particles", "preset": "dust", "count": 50, "color": "#8C7F70", "x": "56%", "y": "78%", "width": 300, "height": 120, "start": 1.0, "end": 3.5, "speed": 0.6}]),
 dict(id="s50-proteins", at="a3", type="DIAGRAM inset",
      desc="Protein ribbon `svg` with `scaleY` keyframes 1 -> 0.45 (squashed); small `embers` particles as nerve sparks; `You` gets an `idle` jitter",
      cam=cam(), cam_txt="static", sfx=[("glitch", 0.6, 0.3)], sfx_txt="faint `glitch` sparks",
      bg="auto", layers=lambda s: [BOARD_PANEL, svg(PROTEIN, x="55%", y="40%", w=700, h=280, keyframes=[{"t": 0, "scaleY": 1}, {"t": 2.0, "scaleY": 0.45}]),
                                   {"type": "particles", "preset": "embers", "count": 30, "color": YELLOW, "x": "55%", "y": "40%", "width": 700, "height": 300, "start": 1.0},
                                   you("stand", x="55%", y="76%", pxPerM=90, idle=[{"type": "jitter", "amount": 3, "speed": 8}])]),
 dict(id="s51-chamber", at="a4", type="HISTORY vignette",
      desc="`Diver` (stand-in for the chamber diver, no fins/bubbles) inside a rounded `rect` chamber with a porthole `circle`; date `Tag` 1992; HUD mark 701 M; at a5 `SpeedBars` 701 M vs 4,000 M",
      cam=cam("pushIn", 0.3), cam_txt="`cut`; `pushIn` on the porthole", sfx=[("ding", 0.3, 0.6)], sfx_txt="`ding` on the date",
      bg="auto", layers=lambda s: [BOARD_PANEL, {"type": "rect", "fill": "#26323A", "stroke": "#9FB3BF", "strokeWidth": 8, "radius": 160, "x": "42%", "y": "48%", "width": 520, "height": 640, "depth": 0, "z": 20},
                                   creature("Diver", 80, "42%", "50%", 380, 380, bubbles=False, fins=False, z=25), tag("1992", at=0.3, x="68%", y="28%", accent="yellow", size=60)]),
 dict(id="s52-deeper", at="a5", type="BOARD + TMAO",
      desc="`SpeedBars` HUMAN RECORD 701 M vs YOU 4,000 M; at a5+2.4 the protein ribbon returns with TMAO dot `svg` pushing it back (scaleY 0.45 -> 1); `Tag` TMAO (FROM DEEP FISH); HUD BORROWED 4 at a6",
      cam=cam("drift"), cam_txt="`drift`", sfx=[("pop", 2.4, 0.5), ("ding", "a6+0.3", 0.6)], sfx_txt="`pop`; `ding` on the fix",
      bg="auto", layers=lambda s: [BOARD_PANEL, bars([{"label": "HUMAN RECORD", "value": 701, "unit": " M"}, {"label": "YOU", "value": 4000, "unit": " M", "color": "red"}], None, at=0.0, y="30%", mx=4000),
                                   svg(PROTEIN, x="55%", y="64%", w=600, h=240, start=2.4, keyframes=[{"t": 2.4, "scaleY": 0.45}, {"t": 4.4, "scaleY": 1}]), svg(TMAO_DOTS, x="55%", y="64%", w=600, h=240, start=2.6),
                                   tag("TMAO (FROM DEEP FISH)", at=2.4, y="84%")]),
 dict(id="s53-limit", at="a7", type="BOARD chart (tracker advance)",
      desc="TMAO-vs-depth line chart `svg` revealed with `wipeRight`, climbing to the dashed red AS CONCENTRATED AS SEAWATER · ~8,200 M line; at a8 date `Tag` 2014 and the HUD red 8,200 mark pulses THE WALL",
      cam=cam("pullOut", 0.2), cam_txt="`pullOut`", sfx=[("riser", 0.0, 0.4), ("ding", "a8", 0.5), ("stinger", "a8+2.4", 0.5)], sfx_txt="short `riser`; `ding`; soft `stinger`",
      bg="auto", layers=lambda s: [BOARD_PANEL, svg(TMAO_CHART, x="55%", y="48%", w=1100, h=640, enter={"type": "wipeRight", "duration": 3.0}), tag("2014", at="a8", x="80%", y="22%", accent="yellow", size=56)], hud_pulse=("8200", "a8+2.4")),
 # ---------------- L9 the plain
 dict(id="s54-walk", at="w1", type="STAMP + wide plain",
      desc="Stamp DAY 4 · THE ABYSS PLAIN; `You` walking (`pose: run`, small) across the mud `svg`; `Map` inset with the dashed line two-thirds drawn",
      cam=cam("panRight", 0.4), cam_txt="`panRight`", sfx=[("footsteps", 1.0, 0.2)], sfx_txt="muffled `footsteps`",
      bg="auto", layers=lambda s: [stamp("DAY 4", "THE ABYSS PLAIN"), svg(SEAFLOOR, x="50%", y="86%", w=1920, h=300, depth=0.9), you("run", x="40%", y="72%", pxPerM=60),
                                   mapview([{"t": 0, "lon": 143.5, "lat": 12.5, "zoom": 3}], pins=[{"lon": 144.6, "lat": 13.9, "label": "FERRY"}, {"lon": 142.2, "lat": 11.35, "label": "CHALLENGER DEEP"}, {"lon": 142.9, "lat": 12.2, "label": "YOU"}], at=2.2, x="80%", y="30%", w=560, h=320)]),
 dict(id="s55-starving", at="w2", type="STORY wide (low point)",
      desc="`You` very small on the mud; marine snow thins (two `particles` `snow` layers crossfade, 90 -> 15); `Stat` ~1% OF SUNLIT FOOD REACHES THE FLOOR; at w4 the remora hangs limp (`idle` off)",
      cam=cam("pullOut", 0.5), cam_txt="slow `pullOut` (isolation)", sfx=[("drone", 0.0, 0.5)], sfx_txt="`drone` only",
      bg="auto", layers=lambda s: [svg(SEAFLOOR, x="50%", y="86%", w=1920, h=300, depth=0.9), you("shrug", x="50%", y="74%", pxPerM=40),
                                   {"type": "particles", "preset": "snow", "count": 90, "speed": 0.3, "keyframes": [{"t": 0, "opacity": 1}, {"t": 3.0, "opacity": 0}]},
                                   {"type": "particles", "preset": "snow", "count": 15, "speed": 0.3, "seed": 4},
                                   stat("~1%", "OF SUNLIT FOOD REACHES THE FLOOR", at="w3+2.4", y="30%")]),
 dict(id="s56-options", at="w5", type="OPTION board (hypothetical, no trip)",
      desc="`Options` WHERE COULD YOU LIVE? OPEN OCEAN · ABYSS · VENT · REEF; `strikes` OPEN OCEAN at w6+0.8, ABYSS at w6+2.4",
      cam=cam(), cam_txt="static", sfx=[("pop", 0.3, 0.4), ("tick", "w6+0.8", 0.5), ("tick", "w6+2.4", 0.5)], sfx_txt="`pop`; `tick` per strike",
      bg="auto", layers=lambda s: [BOARD_PANEL, comp("explainer/Options", {"title": "WHERE COULD YOU LIVE?", "items": ["OPEN OCEAN", "ABYSS", "VENT", "REEF"], "at": 0.3, "stagger": 0.3, "strikes": [{"index": 0, "at": "w6+0.8"}, {"index": 1, "at": "w6+2.4"}], "size": 58}, x="55%", y="48%", width=1200, height=620, depth=0, z=60)]),
 dict(id="s57-vent", at="w7", type="OPTION tile (vent)",
      desc="The board slides left; a VENT tile (inline `svg`: chimney, shimmering plume, red-plumed tube worms) in a rounded frame; small chip ALVIN · 1977 (on screen only)",
      cam=cam("pushIn", 0.2), cam_txt="`pushIn` on the tile", sfx=[("bubbles", 0.6, 0.3), ("ding", 0.8, 0.5)], sfx_txt="`bubbles`; `ding` on the chip",
      bg="auto", layers=lambda s: [BOARD_PANEL, svg(VENT_TILE, x="50%", y="50%", w=780, h=540, start=0.6, enter={"type": "pop"}), tag("ALVIN · 1977", at=0.8, x="76%", y="24%", accent="yellow", size=44)]),
 dict(id="s58-reef", at="w8", type="OPTION tile (reef)",
      desc="REEF tile (inline `svg`: bright water gradient, coral silhouettes, yellow fish ovals) beside the dimmed vent tile; `Tag` REEF · 30 M · STILL IN THE SUNSHINE",
      cam=cam(), cam_txt="static", sfx=[("pop", 0.6, 0.5)], sfx_txt="`pop`; brief music lift",
      bg="auto", layers=lambda s: [BOARD_PANEL, svg(VENT_TILE, x="34%", y="50%", w=520, h=360, opacity=0.4), svg(REEF_TILE, x="70%", y="50%", w=640, h=440, start=0.6, enter={"type": "pop"}), tag("REEF · 30 M · STILL IN THE SUNSHINE", at=0.6, y="84%")]),
 dict(id="s59-cant-go-back", at="w9", type="OPTION tile + body",
      desc="A red ✗ stamps over the REEF tile with `Tag` CAN'T GO BACK UP; HUD WAY BACK: SHRINKING",
      cam=cam(shake=[{"at": 0.2, "duration": 0.3, "amplitude": 8}]), cam_txt="small `shake` on the ✗", sfx=[("impact", 0.2, 0.5)], sfx_txt="`impact`",
      bg="auto", layers=lambda s: [BOARD_PANEL, svg(REEF_TILE, x="55%", y="48%", w=700, h=480), {"type": "text", "text": "✗", "fontSize": 420, "color": RED, "x": "55%", "y": "48%", "depth": 0, "z": 70, "start": 0.2, "enter": {"type": "pop"}},
                                   tag("CAN'T GO BACK UP", at=0.4, y="84%", accent="red")]),
 dict(id="s60-edge", at="w10", type="STORY wide (turn)",
      desc="Back on the plain; the mud edge `svg` drops away into black (trench lip) in front of `You`",
      cam=cam("panRight", 0.4), cam_txt="`panRight` to the edge", sfx=[("riser", 1.0, 0.4)], sfx_txt="`riser`",
      bg="auto", layers=lambda s: [svg(SEAFLOOR_EDGE, x="50%", y="78%", w=1920, h=400, depth=0.9), you("stand", x="56%", y="62%", pxPerM=60)]),
 # ---------------- L10 climax
 dict(id="s61-8200m", at="x1", type="STAMP + trench",
      desc="Stamp 8,200 M · THE LINE; two trench-wall polygon `svg` layers close in (x keyframes); at x2 NEW `whatif/Fish` `species: snailfish` (pale, translucent) drifts across",
      cam=cam("pushIn", 0.3), cam_txt="slow `pushIn`", sfx=[("underwater_rumble", 0.0, 0.5), ("drone", 2.0, 0.4)], sfx_txt="`underwater_rumble`; `drone`",
      bg="auto", layers=lambda s: [stamp("8,200", "THE LINE"), svg(TRENCH_L, x="12%", y="50%", w=600, h=1080, keyframes=[{"t": 0, "x": "4%"}, {"t": s["dur"], "x": "14%"}]),
                                   svg(TRENCH_R, x="98%", y="50%", w=600, h=1080, keyframes=[{"t": 0, "x": "106%"}, {"t": s["dur"], "x": "96%"}]),
                                   fish("snailfish", "50%", "48%", 300, 120, pxPerM=200, translucent=True, start=local("x2", s["start"]), keyframes=[{"t": local("x2", s["start"]), "x": "75%"}, {"t": s["dur"], "x": "40%", "ease": "linear"}]),
                                   you("stand", x="45%", y="66%", pxPerM=100)]),
 dict(id="s62-cousin", at="x3", type="MAP + HUD",
      desc="`Map` (Japan to the Marianas) with pin IZU-OGASAWARA TRENCH; date `Tag` 2022; HUD mark 8,336 M lands right beside the red 8,200",
      cam=cam("pushIn", 0.2), cam_txt="`cut`; slow map zoom", sfx=[("ding", 0.5, 0.5), ("tick", 2.4, 0.5)], sfx_txt="`ding`; `tick`",
      bg="auto", layers=lambda s: [mapview([{"t": 0, "lon": 142, "lat": 22, "zoom": 2.4}, {"t": 4, "lon": 142, "lat": 28, "zoom": 3.2}], pins=[{"lon": 142.6, "lat": 30.0, "label": "IZU-OGASAWARA TRENCH · 8,336 M", "at": 0.5}, {"lon": 142.2, "lat": 11.35, "label": "YOU"}], x="55%", y="50%", w=1300, h=760),
                                   tag("2022", at=0.5, x="82%", y="20%", accent="yellow", size=56)]),
 dict(id="s63-wall", at="x4", type="HUD close (planted rule pays)",
      desc="HUD `focus: borrowed`: the BORROWED counter flips to NO FIX LEFT in red; `Tag` THE WALL",
      cam=cam("pushIn", 0.3), cam_txt="`pushIn`", sfx=[("stinger", 0.5, 0.6)], sfx_txt="`stinger`",
      bg="auto", hud_focus="borrowed", layers=lambda s: [tag("THE WALL", at=0.5, y="80%", accent="red")]),
 dict(id="s64-remora-leaves", at="x5", type="STORY (tender beat)",
      desc="The remora lets go of `You`'s back and drifts up and away toward a faint glow (y + opacity keyframes); REMORA chip LEAVING -> GONE",
      cam=cam("panUp", 0.2), cam_txt="small `panUp` with the remora", sfx=[], sfx_txt="music thins to one soft line",
      bg="auto", layers=lambda s: [svg(TRENCH_L, x="14%", y="50%", w=600, h=1080), svg(TRENCH_R, x="96%", y="50%", w=600, h=1080), you("stand", x="50%", y="66%", pxPerM=120),
                                   fish("remora", "50%", "58%", 220, 90, pxPerM=120, keyframes=[{"t": 0.6, "y": "58%", "opacity": 1}, {"t": s["dur"], "y": "8%", "opacity": 0.1}])]),
 dict(id="s65-guess", at="x6", type="GRAPHIC (honesty flag)", trans={"type": "glitch", "duration": 0.3},
      desc="`glitch` in; `Tag` BEYOND KNOWN BIOLOGY; `grade` desaturates",
      cam=cam(), cam_txt="static", sfx=[("glitch", 0.0, 0.5)], sfx_txt="`glitch`",
      bg="auto", grade={"saturate": 0.3}, layers=lambda s: [tag("BEYOND KNOWN BIOLOGY", at=0.1, y="45%", accent="red", size=64)]),
 dict(id="s66-decision", at="x7", type="DECISION board (climax choice)",
      desc="Two tiles: left STAY AT THE LINE · YOU CAN STILL LIVE HERE; right GO DOWN 2,700 M · COST: THE WAY BACK (red); the right tile lights at x7 end",
      cam=cam("pushIn", 0.2), cam_txt="slow `pushIn`", sfx=[("tick", 0.4, 0.4), ("tick", 4.0, 0.4), ("heartbeat_slow", 6.0, 0.5)], sfx_txt="`tick` per tile; `heartbeat_slow`",
      bg="auto", grade={"saturate": 0.5}, layers=lambda s: [comp("explainer/Options", {"title": "THE LINE", "items": ["STAY: YOUR BODY STILL MAKES SENSE", "GO DOWN 2,700 M: COSTS THE WAY BACK"], "itemAt": [0.4, 4.0], "select": {"index": 1, "at": s["dur"] - 0.6}, "size": 50}, x="55%", y="48%", width=1400, height=520, depth=0, z=60)]),
 dict(id="s67-cells", at="x8", type="DIAGRAM (speculative)",
      desc="Cells `svg` (ten teal circles) swell (scale keyframes 1 -> 1.25) and hold; at x9 HUD WAY BACK: GONE",
      cam=cam("pushIn", 0.3), cam_txt="`pushIn`", sfx=[("bubbles", 0.0, 0.3), ("stinger", "x9", 0.4)], sfx_txt="`bubbles`; soft `stinger`",
      bg="auto", grade={"saturate": 0.5}, layers=lambda s: [svg(CELLS, x="55%", y="48%", w=900, h=450, keyframes=[{"t": 0, "scale": 1}, {"t": 2.6, "scale": 1.25, "ease": "out"}])]),
 dict(id="s68-ramp", at="x10", type="DESCENT ramp (hold)",
      desc="'You go down.' then a 2 s hold: HUD meter races 8,200 -> 10,935; upward speed lines (`particles` `rain`, negative `speed`); Ocean near-black",
      cam=cam("panDown", 1.2), cam_txt="fast `panDown`", sfx=[("whoosh_long", 0.6, 0.7), ("drone", 0.8, 0.6)], sfx_txt="`whoosh_long`; music drops to one low `drone`",
      bg="auto", layers=lambda s: [{"type": "particles", "preset": "rain", "count": 120, "color": "rgba(200,220,230,0.5)", "speed": -2.5}, you("run", x="50%", y="50%", rotate=170, pxPerM=100)]),
 dict(id="s69-floor", at="x11", type="STAMP + trench floor (sensory mirror)",
      desc="Stamp 10,935 M · CHALLENGER DEEP; pale sediment floor `svg`; `You` lands, a grey `dust` puff; silence; inset `Map` pin MARIANA TRENCH",
      cam=cam("pushIn", 0.2), cam_txt="slow `pushIn`", sfx=[("impact", 2.4, 0.3)], sfx_txt="near silence; soft `impact` on the landing",
      bg="auto", layers=lambda s: [stamp("10,935", "CHALLENGER DEEP"), svg(SEAFLOOR.replace("#2E2A24", "#5A5650").replace("#3A3128", "#6E6A63"), x="50%", y="86%", w=1920, h=300, depth=0.9),
                                   you("stand", x="54%", y="70%", pxPerM=80, align="bottom"), {"type": "particles", "preset": "dust", "count": 60, "color": "#A8A39A", "x": "54%", "y": "78%", "width": 320, "height": 120, "start": 2.4, "end": 6.0, "speed": 0.5}]),
 dict(id="s70-thumbnail-car", at="x13", type="ICON comparison",
      desc="PRESSURE x1,000+; at x13+1.8 a `Car` figure sits on a big rounded `circle` 'thumbnail'; `Stat` ~1.1 T / CM²",
      cam=cam("pushIn", 0.2), cam_txt="`pushIn`", sfx=[("pop", 1.8, 0.6)], sfx_txt="`pop` on the icon",
      bg="auto", layers=lambda s: [BOARD_PANEL, {"type": "circle", "fill": "#E9D8C8", "stroke": "#C9B6A4", "strokeWidth": 8, "x": "45%", "y": "58%", "width": 360, "height": 300, "depth": 0, "z": 40, "start": 1.8},
                                   creature("Car", 70, "45%", "44%", 360, 140, z=45, start=1.8, enter={"type": "drop"}), stat("~1.1 T", "ON EVERY SQUARE CENTIMETRE", at=1.8, x="72%", y="50%", w=600)]),
 dict(id="s71-amphipods", at="x14", type="STORY medium, swarm",
      desc="12 `Krill` layers (amphipod stand-ins, 3-6 cm, shared `pxPerM` 600 near the camera) converge on `You` by keyframes; distant ones = `dust` particles",
      cam=cam("pushIn", 0.3), cam_txt="slow `pushIn`", sfx=[("bubbles", 2.0, 0.2)], sfx_txt="faint `bubbles`",
      bg="auto", layers=lambda s: [you("stand", x="50%", y="70%", pxPerM=200), {"type": "particles", "preset": "dust", "count": 120, "color": "#D8CFC0", "speed": 0.4, "start": 2.0}]
      + [creature("Krill", 600, f"{(i * 37) % 100}%", f"{20 + (i * 23) % 70}%", 120, 60, start=2.0, flipX=bool(i % 2), keyframes=[{"t": 2.0, "x": f"{(i * 37) % 100}%", "y": f"{20 + (i * 23) % 70}%"}, {"t": s["dur"], "x": f"{46 + (i % 5) * 2}%", "y": f"{55 + (i % 4) * 5}%"}]) for i in range(12)]),
 dict(id="s72-eat", at="x15", type="STORY close (hunger payoff)",
      desc="Close on `You` among the swarm; `Tag` YOU ARE THE THING THAT SANK, then at x16 `Tag` FIRST MEAL IN 6 DAYS",
      cam=cam("pushIn", 0.3), cam_txt="`pushIn`", sfx=[("pop", 0.4, 0.3)], sfx_txt="small `pop`",
      bg="auto", layers=lambda s: [you("shrug", x="50%", y="76%", pxPerM=300)] + [creature("Krill", 600, f"{38 + i * 5}%", f"{48 + (i % 3) * 8}%", 120, 60, flipX=bool(i % 2)) for i in range(6)]
      + [tag("YOU ARE THE THING THAT SANK", at=0.2, y="16%", out=local("x16", s["start"])), tag("FIRST MEAL IN 6 DAYS", at=local("x16", s["start"]), y="16%")]),
 dict(id="s73-fibres", at="x17", type="INSET (bathos)",
      desc="Date `Tag` 2019; magnifier `svg` circle on one amphipod with red/blue/yellow fibre threads in its gut; `Stat` 100% HAD MAN-MADE FIBRES",
      cam=cam("pushIn", 0.3), cam_txt="`pushIn` on the inset", sfx=[("ding", 0.3, 0.5), ("ding", 3.6, 0.6)], sfx_txt="`ding` on the date and on 100%",
      bg="auto", layers=lambda s: [BOARD_PANEL, creature("Krill", 6000, "42%", "50%", 520, 240), svg(FIBRES, x="42%", y="50%", w=420, h=420, start=1.0, enter={"type": "zoomIn"}),
                                   tag("2019", at=0.3, x="76%", y="24%", accent="yellow", size=56), stat("100%", "HAD MAN-MADE FIBRES IN THE GUT", at=3.6, x="72%", y="58%", color="red", w=640)]),
 dict(id="s74-fibre-face", at="x18", type="STORY close",
      desc="Close on `You`'s face; one coloured fibre `rect` (thin, red) drifts past by keyframes",
      cam=cam("pushIn", 0.15), cam_txt="very slow `pushIn`", sfx=[("stinger", 2.8, 0.3)], sfx_txt="silence, then soft `stinger`",
      bg="auto", layers=lambda s: [you("stand", x="50%", y="86%", pxPerM=420), {"type": "rect", "fill": RED, "x": "70%", "y": "40%", "width": 90, "height": 4, "depth": 1, "keyframes": [{"t": 0, "x": "80%", "y": "30%", "rotate": 10}, {"t": s["dur"], "x": "30%", "y": "45%", "rotate": -20}]}]),
 # ---------------- L11 bookend
 dict(id="s75-look-up", at="b1", type="VERTICAL callback (bookend)",
      desc="`You` looks up; camera rides up the whole column (background Ocean `depth` track 10,935 -> 0) to the tiny `whatif/Ferry` at the surface, the 0:00 framing, with a tiny remora dot near the hull; the HUD keeps reading 10,935 M (you stay down)",
      cam=cam("panUp", 1.0), cam_txt="`panUp` fast, easing out", sfx=[("whoosh_long", 0.3, 0.6)], sfx_txt="`whoosh_long`",
      bg=lambda s: ocean(depth=[{"t": 0, "v": 10935}, {"t": 3.8, "v": 0, "ease": "inOut"}], surface=0.3, skyTop="#3B2F66", skyBottom="#E58F55", rays=3, snow=30),
      layers=lambda s: [comp("whatif/Ferry", {"lights": True}, x="56%", y="28%", width=240, height=70, depth=0.3, start=3.4), {"type": "circle", "fill": "#C9D6DD", "x": "58%", "y": "33%", "width": 12, "height": 6, "depth": 0.3, "start": 4.0}]),
 dict(id="s76-verdict", at="b2", type="VERDICT board",
      desc="`Headline` COULD YOU BREATHE UNDERWATER? then YES. (red) below",
      cam=cam(), cam_txt="static", sfx=[("ding", 1.4, 0.5)], sfx_txt="`ding` on YES",
      bg=ocean(depth=1500, rays=0, snow=40), hud=False,
      layers=lambda s: [comp("explainer/Headline", {"text": "COULD YOU BREATHE UNDERWATER?", "size": 80, "at": 0.0}, x="50%", y="38%", width=1600, height=200, depth=0, z=60),
                        comp("explainer/Headline", {"text": "YES.", "red": ["YES."], "size": 150, "at": 1.4}, x="50%", y="60%", width=800, height=240, depth=0, z=60)]),
 dict(id="s77-recap", at="b3", type="RECAP strip",
      desc="Four fix icons pop left -> right (gill slits, salt dots, coil, protein ribbon) with labels FISH · FISH · TUNA · DEEP FISH, then a red fifth tile WAY BACK ✗",
      cam=cam(), cam_txt="static", sfx=[("pop", 0.2, 0.4), ("pop", 1.0, 0.4), ("pop", 1.8, 0.4), ("pop", 2.8, 0.4), ("impact", 5.4, 0.4)], sfx_txt="`pop` x4; `impact` on the last tile",
      bg=ocean(depth=1500, rays=0, snow=40), hud=False,
      layers=lambda s: [comp("explainer/Options", {"title": "WHAT IT TOOK", "items": ["GILLS · FISH", "SALT PUMPS · FISH", "HEAT EXCHANGER · TUNA", "TMAO · DEEP FISH", "THE WAY BACK"], "itemAt": [0.2, 1.0, 1.8, 2.8, 5.4], "strikes": [{"index": 4, "at": 5.6}], "size": 50}, x="50%", y="50%", width=1300, height=720, depth=0, z=60)]),
 dict(id="s78-thesis", at="b4", type="THESIS",
      desc="Back on the trench floor; `You` standing small; `Headline` GETTING IN WAS NEVER THE HARD PART. / GETTING OUT IS. (OUT red)",
      cam=cam("pullOut", 0.3), cam_txt="slow `pullOut`", sfx=[], sfx_txt="music swells gently",
      bg=ocean(depth=10935, rays=0, snow=15), hud=False,
      layers=lambda s: [svg(SEAFLOOR.replace("#2E2A24", "#5A5650").replace("#3A3128", "#6E6A63"), x="50%", y="86%", w=1920, h=300, depth=0.9), you("stand", x="50%", y="74%", pxPerM=60, align="bottom"),
                        comp("explainer/Headline", {"text": "GETTING IN WAS NEVER THE HARD PART.\nGETTING OUT IS.", "red": ["OUT"], "size": 70, "at": 0.2}, x="50%", y="34%", width=1600, height=300, depth=0, z=60)]),
 # ---------------- L12 CTA
 dict(id="s79-endcard", at="e1", type="END CARD (callback to the ferry rail)",
      desc="Top third: the lit `whatif/Ferry` rail at dusk (0:00 palette); `Headline` WOULD YOU JUMP?; three tiles rebuilt as layers (REEF tile `svg`, VENT tile `svg`, THE LINE = trench-wall `svg` pair + snailfish) with labels",
      cam=cam(), cam_txt="static", sfx=[("pop", 3.0, 0.4), ("pop", 3.6, 0.4), ("pop", 4.2, 0.4)], sfx_txt="`pop` per tile",
      bg=ocean(depth=2, surface=0.3, skyTop="#3B2F66", skyBottom="#E58F55", rays=3, snow=20), hud=False,
      layers=lambda s: [comp("whatif/Ferry", {"lights": True}, x="50%", y="24%", width=700, height=200, depth=0.3),
                        comp("explainer/Headline", {"text": "WOULD YOU JUMP?", "red": ["JUMP?"], "size": 84, "at": 0.0}, x="50%", y="44%", width=1400, height=160, depth=0, z=60),
                        svg(REEF_TILE, x="25%", y="74%", w=440, h=300, start=3.0, enter={"type": "pop"}), svg(VENT_TILE, x="50%", y="74%", w=440, h=300, start=3.6, enter={"type": "pop"}),
                        {"type": "rect", "fill": "#05080B", "radius": 20, "x": "75%", "y": "74%", "width": 440, "height": 300, "depth": 0, "start": 4.2, "enter": {"type": "pop"}},
                        fish("snailfish", "75%", "74%", 200, 80, translucent=True, start=4.2),
                        tag("REEF", at=3.0, x="25%", y="92%", size=36), tag("VENT", at=3.6, x="50%", y="92%", size=36), tag("THE LINE", at=4.2, x="75%", y="92%", size=36, accent="red")]),
 dict(id="s80-series", at="e2", type="END CARD + series loop",
      desc="Same end card; `Tag` NEXT: SWIM BACK UP? slides in above the tiles; holds 3.5 s after the VO, music out",
      cam=cam(), cam_txt="static", sfx=[("ding", 0.2, 0.4)], sfx_txt="`ding`; music out by the end",
      bg=ocean(depth=2, surface=0.3, skyTop="#3B2F66", skyBottom="#E58F55", rays=3, snow=20), hud=False,
      layers=lambda s: [comp("whatif/Ferry", {"lights": True}, x="50%", y="24%", width=700, height=200, depth=0.3),
                        svg(REEF_TILE, x="25%", y="74%", w=440, h=300), svg(VENT_TILE, x="50%", y="74%", w=440, h=300),
                        {"type": "rect", "fill": "#05080B", "radius": 20, "x": "75%", "y": "74%", "width": 440, "height": 300, "depth": 0},
                        fish("snailfish", "75%", "74%", 200, 80, translucent=True), tag("NEXT: SWIM BACK UP?", at=0.2, y="46%", accent="red", size=60)]),
]

# ------------------------------------------------------------------ resolve shot times

for s in SHOTS:
    s["start"] = round(T(s["at"]), 2)
SHOTS.sort(key=lambda s: s["start"])
SHOTS[0]["start"] = 0.0
for i, s in enumerate(SHOTS):
    s["end"] = SHOTS[i + 1]["start"] if i + 1 < len(SHOTS) else RUNTIME
    s["dur"] = round(s["end"] - s["start"], 2)

problems = []
for s in SHOTS:
    if s["dur"] < 1.5:
        problems.append(f"{s['id']} only {s['dur']} s")
    if s["dur"] > 15.0:
        problems.append(f"{s['id']} {s['dur']} s > 15 s")
LONGEST = max(SHOTS, key=lambda s: s["dur"])


def scene_rel(val, s):
    if isinstance(val, str) and re.match(r"^[a-z]+\d+(\+[\d.]+)?$", val) and val.split("+")[0] in LINES:
        return round(T(val) - s["start"], 2)
    return val


def fix_times(obj, s):
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if k in ("t", "at", "start", "end", "out") and not isinstance(v, (dict, list)):
                out[k] = scene_rel(v, s)
            elif k == "itemAt":
                out[k] = [scene_rel(x, s) for x in v]
            else:
                out[k] = fix_times(v, s)
        return out
    if isinstance(obj, list):
        return [fix_times(x, s) for x in obj]
    return obj


def clamp_times(obj, dur):
    """Keep every scene-local time inside [0, dur]."""
    if isinstance(obj, dict):
        for k, v in list(obj.items()):
            if k in ("t", "at", "start", "end") and isinstance(v, (int, float)):
                obj[k] = round(max(0.0, min(float(v), dur)), 2)
            else:
                clamp_times(v, dur)
    elif isinstance(obj, list):
        for x in obj:
            clamp_times(x, dur)
    return obj

# ------------------------------------------------------------------ storyboard


def hud_layer(s):
    p = hud_props(s["start"], s["end"], s.get("hud_focus"))
    if s.get("hud_focus_at"):
        f, ref = s["hud_focus_at"]
        p["changes"].append({"at": round(T(ref) - s["start"], 2), "focus": f})
    if s.get("hud_blink") is not None:
        p["changes"].append({"at": s["hud_blink"], "blink": "temp"})
    if s.get("hud_pulse"):
        mark, ref = s["hud_pulse"]
        p["changes"].append({"at": round(T(ref) - s["start"], 2), "pulseMark": int(mark)})
    p["changes"].sort(key=lambda c: c["at"])
    return comp("whatif/Hud", p, x=60, y=60, anchorX=0, anchorY=0, width=420, height=960, depth=0, z=92)


def build_storyboard():
    scenes = []
    for s in SHOTS:
        layers = s["layers"](s)
        if s.get("hud", True):
            layers.append(hud_layer(s))
        bg = s["bg"]
        if bg == "auto":
            bg = ocean(depth=track(DEPTH_KEYS, s["start"], s["end"]), rays=7, snow=50)
        elif callable(bg):
            bg = bg(s)
        scene = {
            "id": s["id"],
            "duration": round(s["dur"], 2),
            "background": bg,
            "layers": layers,
            "camera": s["cam"],
            "transitionIn": s.get("trans", {"type": "cut"}),
            "sfx": [{"cue": c, "at": a, "volume": v} for c, a, v in s["sfx"]],
            "notes": s["type"] + ": " + s["desc"],
        }
        if s.get("grade"):
            scene["grade"] = s["grade"]
        scene = clamp_times(fix_times(scene, s), round(s["dur"], 2))
        for cue in scene["sfx"]:
            cue["at"] = max(0.0, min(cue["at"], s["dur"] - 0.05))
        scenes.append(scene)
    words = []
    for lid in order:
        L = LINES[lid]
        toks = L["text"].split()
        weights = [max(1, spoken_words(w)) * 6 + len(w) for w in toks]
        tot = sum(weights)
        t0 = L["start"]
        for w, wt in zip(toks, weights):
            d = L["dur"] * wt / tot
            words.append({"text": w, "start": round(t0, 3), "end": round(t0 + d * 0.92, 3)})
            t0 += d
    G = lambda ref: round(T(ref), 2)
    music = [
        {"src": "music/tension_pulse.m4a", "start": 0, "end": G("t0"), "volume": 0.22, "duckTo": 0.08, "fadeOut": 0.3},
        {"src": "music/deep_ocean.m4a", "start": G("t0"), "end": G("m5"), "volume": 0.3, "duckTo": 0.1},
        {"src": "music/tension_pulse.m4a", "start": G("m5"), "end": G("f1"), "volume": 0.3, "duckTo": 0.12},
        {"src": "music/deep_ocean.m4a", "start": G("f1"), "end": G("w1"), "volume": 0.3, "duckTo": 0.1},
        {"src": "music/dread.m4a", "start": G("w1"), "end": round(RAMP_START, 2), "volume": 0.22, "duckTo": 0.08},
        {"src": "music/deep_ocean.m4a", "start": G("x11+3.0"), "end": G("b1"), "volume": 0.18, "duckTo": 0.07, "fadeIn": 2.0},
        {"src": "music/documentary_pulse.m4a", "start": G("b1"), "end": RUNTIME, "volume": 0.2, "duckTo": 0.08, "fadeIn": 1.5, "fadeOut": 2.0},
    ]
    return {
        "version": 1,
        "id": "whatif-breathe-underwater",
        "title": "What If You Could Breathe Underwater, But Never Come Back Up?",
        "format": "16:9",
        "fps": FPS,
        "theme": {"fontDisplay": "Montserrat", "fontBody": "Montserrat", "fontCondensed": "Anton", "accent": RED, "ink": "#071219", "paper": WHITE},
        "scenes": scenes,
        "captions": {
            "enabled": True, "words": words, "maxWords": 4, "maxChars": 26, "gapBreak": 0.3,
            "style": {"font": "display", "weight": 900, "fontSize": 62, "color": "#FFFFFF", "highlight": RED, "highlightMode": "content", "strokeWidth": 10, "uppercase": True, "y": 0.88, "backing": 0.0},
        },
        "audio": {"voice": [], "music": music, "sfx": [], "sfxDir": "sfx", "duckOn": "captions"},
        "overlays": {"grain": 0.03, "vignette": 0.18, "fadeIn": 0.2, "fadeOut": 1.0},
    }

# ------------------------------------------------------------------ markdown


def vo_markdown():
    out = []
    for label, rate, lines in SECTIONS:
        s0 = LINES[lines[0][0]]["start"]
        e1 = LINES[lines[-1][0]]["end"]
        out.append(f"\n#### [{label}] {mmss1(s0)}–{mmss1(e1)} (TTS {rate} wpm)")
        for lid, text, os_ in lines:
            L = LINES[lid]
            out.append(f"- {mmss1(L['start'])} VO: {text}")
            for off, txt in os_:
                out.append(f"  - {mmss1(L['start'] + off)} ON-SCREEN: {txt}")
            if lid == "x10":
                out.append(f"- {mmss1(RAMP_START)}–{mmss1(RAMP_END)} HOLD ({RAMP_HOLD:.1f} s): descent ramp, the meter races 8,200 -> 10,935; music drops to one low drone")
    out.append(f"- {mmss1(NARRATION_END)}–{mmss1(RUNTIME)} HOLD ({END_HOLD:.1f} s): end card, music out")
    return "\n".join(out)


def shot_markdown():
    rows = ["| # | t_start | t_end | shot type | visual description (kit vocabulary) | camera move | SFX |", "|---|---|---|---|---|---|---|"]
    for i, s in enumerate(SHOTS, 1):
        rows.append(f"| {i} | {mmss1(s['start'])} | {mmss1(s['end'])} | {s['type']} | {s['desc']} | {s['cam_txt']} | {s['sfx_txt']} |")
    return "\n".join(rows)


def hud_table():
    rows = ["| scene | t | depth (m) | pressure | body °C | borrowed | days | remora | way back | HUD focus |", "|---|---|---|---|---|---|---|---|---|---|"]
    for s in SHOTS:
        if not s.get("hud", True):
            rows.append(f"| {s['id']} | {mmss1(s['start'])} | — | — | — | — | — | — | — | hidden |")
            continue
        d0, d1 = interp(DEPTH_KEYS, s["start"]), interp(DEPTH_KEYS, s["end"])
        t0, t1 = interp(TEMP_KEYS, s["start"]), interp(TEMP_KEYS, s["end"])
        n, lab = step_state(BORROWED, s["start"])
        bor = "NO FIX LEFT" if n == -1 else (f"{n} {lab}".strip() if n else "0")
        ch = changes(BORROWED, s["start"], s["end"])
        if ch:
            nn, ll = ch[-1][1]
            bor += " -> " + ("NO FIX LEFT" if nn == -1 else f"{nn} {ll}")
        def stepcell(table):
            v0 = step_state(table, s["start"])
            c = changes(table, s["start"], s["end"])
            txt = "—" if v0 in (None, "") else str(v0)
            for _, v in c:
                txt += f" -> {v}"
            return txt
        dep = f"{int(d0):,}" if abs(d1 - d0) < 1 else f"{int(d0):,} -> {int(d1):,}"
        pf = lambda d: "x1,000+" if d > 9990 else f"x{int(round(1 + d / 10)):,}"
        pr = pf(d0) if pf(d0) == pf(d1) else f"{pf(d0)} -> {pf(d1)}"
        tmp = f"{t0:.1f}" if abs(t1 - t0) < 0.05 else f"{t0:.1f} -> {t1:.1f}"
        foc = s.get("hud_focus") or (s.get("hud_focus_at") or ("",))[0] or "—"
        rows.append(f"| {s['id']} | {mmss1(s['start'])} | {dep} | {pr} | {tmp} | {bor} | {stepcell(DAYS)} | {stepcell(REMORA)} | {stepcell(WAYBACK)} | {foc} |")
    return "\n".join(rows)


def stamps():
    st = [("200 M", "h1"), ("1,000 M", "m1"), ("2,000 M", "n1"), ("4,000 M", "a1"), ("DAY 4", "w1"), ("8,200 M", "x1"), ("10,935 M", "x11")]
    ts = [T(l) for _, l in st]
    gaps = [round(b - a) for a, b in zip(ts, ts[1:])]
    return ", ".join(f"{n} {mmss(T(l))}" for n, l in st), gaps


def rehooks():
    """Verbal re-hooks: pivots, questions, plants/teases, deadpan buttons (marked ids)."""
    extra = {"c2", "c4", "c8", "r3", "r5", "g7", "h6", "h11", "m6", "m11", "n4", "n9", "w4", "w10", "x5", "x9", "x15", "x18", "b4"}
    ts = sorted({LINES[l]["start"] for l, _ in piv_hits} | {LINES[l]["start"] for l in order if "?" in LINES[l]["text"] or l in extra})
    gaps = [b - a for a, b in zip(ts, ts[1:])]
    return ts, round(max(gaps), 1), round(sorted(gaps)[len(gaps) // 2], 1)


if __name__ == "__main__":
    sb = build_storyboard()
    (HERE / "storyboard.json").write_text(json.dumps(sb, indent=1, ensure_ascii=False) + "\n")
    (HERE / "vo_lines.json").write_text(json.dumps([{"id": l, "text": LINES[l]["text"], "tts": LINES[l]["tts"], "start": LINES[l]["start"], "dur": LINES[l]["dur"]} for l in order], indent=1, ensure_ascii=False) + "\n")
    timing = {"lines": [dict(LINES[i], os=None) for i in order], "shots": [{k: s[k] for k in ("id", "start", "end", "dur")} for s in SHOTS], "metrics": M}
    (HERE / "timing.json").write_text(json.dumps(timing, indent=1) + "\n")
    st, st_gaps = stamps()
    rh, rh_max, rh_med = rehooks()
    pct = lambda ref: round(100 * T(ref) / RUNTIME)
    repl = {
        "{{VO}}": vo_markdown(), "{{SHOTS}}": shot_markdown(), "{{HUD}}": hud_table(),
        "{{RUNTIME}}": str(RUNTIME), "{{RUNTIME_MMSS}}": mmss1(RUNTIME), "{{NARR_END}}": mmss1(NARRATION_END),
        "{{STAMPS}}": st, "{{STAMP_GAPS}}": ", ".join(f"{g} s" for g in st_gaps), "{{STAMP_MIN}}": str(min(st_gaps)), "{{STAMP_MAX}}": str(max(st_gaps)),
        "{{REHOOK_N}}": str(len(rh)), "{{REHOOK_MAX}}": str(rh_max), "{{REHOOK_MED}}": str(rh_med),
        "{{SHOTCOUNT}}": str(len(SHOTS)), "{{LONGEST_SHOT}}": f"{LONGEST['id']} {LONGEST['dur']} s",
        "{{TITLE_T}}": mmss1(TITLE_START), "{{TITLE_END}}": mmss1(TITLE_END), "{{RAMP}}": f"{mmss1(RAMP_START)}–{mmss1(RAMP_END)}",
        "{{ENDING_SHARE}}": str(round(100 * (RUNTIME - T("b1")) / RUNTIME, 1)),
        "{{PIVOT_LIST}}": ", ".join(f"{w.lower()} {mmss(LINES[l]['start'])}" for l, w in piv_hits),
    }
    for k, v in M.items():
        repl["{{M:" + k + "}}"] = str(v)
    for lid in order:
        repl["{{T:" + lid + "}}"] = mmss(LINES[lid]["start"])
        repl["{{T1:" + lid + "}}"] = mmss1(LINES[lid]["start"])
        repl["{{P:" + lid + "}}"] = str(pct(lid))
    for s in SHOTS:
        repl["{{S:" + s["id"] + "}}"] = mmss(s["start"])
    tmpl = (HERE / "script.template.md").read_text()
    text = tmpl
    for k, v in repl.items():
        text = text.replace(k, v)
    left = re.findall(r"\{\{[^}]+\}\}", text)
    (HERE / "script.md").write_text(text)
    print(json.dumps(M, indent=1))
    print("shots", len(SHOTS), "runtime", RUNTIME, "title", TITLE_START, "stamps", st, st_gaps)
    print("rehooks max gap", rh_max, "median", rh_med)
    print("pivots:", repl["{{PIVOT_LIST}}"])
    print("longest shot", LONGEST["id"], LONGEST["dur"])
    print("problems:", problems or "none")
    print("unresolved placeholders:", left or "none")
