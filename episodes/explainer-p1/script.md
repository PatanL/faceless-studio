---
id: explainer-p1
niche: explainer
lane: kurz (house style A, flat 2D in Remotion; no Blender)
title: How Long You'd Last in Every Prehistoric Ocean
alt_titles: The Ocean's Scariest Hunter Was Once As Long As Your Arm | Sharks Kill 6 of Us a Year. We Kill 100 Million of Them.
format: 9:16
target_s: 60
template: pipeline/templates/explainer.md (Short)
voice: am_michael
music: score
ending: loop
references:
  - id: nAWpLtG-kNs, url: https://www.youtube.com/watch?v=nAWpLtG-kNs, views: 12209257, outlier_score: 113.57  # ERAS: era ladder, verdict per era
  - id: qrfhhZ-Wvmk, url: https://www.youtube.com/watch?v=qrfhhZ-Wvmk, views: 3374140, outlier_score: 6.54    # OCEANS: same premise, ocean only; safest era is now
  - id: 2cK8l5Yg5w8, url: https://www.youtube.com/watch?v=2cK8l5Yg5w8, views: 5194382, outlier_score: 3.58    # KITCHEN: Kurzgesagt list Short, fixed slots
  - lane form (not in corpus): oR3Q7RntqEw Kurzgesagt "Whales Evolved from This Animal", 5.25M, 1.9x channel Shorts median  # WHALE: picture contradicts the claim, scrubber rewind loop
sources: draft_3 (base) + draft_2 + draft_1 grafts, research/pipeline/explainer-p1/
---

# How Long You'd Last in Every Prehistoric Ocean (Short)

**Blender: no.** Flat 2D house style A, built in code with Remotion and SVG, like every kurz-lane episode. Every frame
of both Kurzgesagt reference Shorts is flat vector art, docs/HOUSE_STYLE.md keeps Kurzgesagt-type explainers on
style A, 3D/Blender is parked (docs/FEEDBACK_LOG.md 2026-11-01), and BRIEF rule 4 says every visual is code. (BRIEF
rule 2 no longer reserves the Mac for Blender: since 2026-11-02 the Mac is a second Remotion render slot.)

**Premise.** You tread water while a time scrubber jumps through the ocean's history. At each stop: how long until
something eats you? The hook shows the first big hunter lying along your own arm; the teasers promise armour, jaws
and teeth; each rung pays one teaser in order. The favourite (Megalodon) falls at ~62 %. Twist (villain swap, the
"safest era is now" pattern): today almost nothing hunts you, because the ocean's scariest hunter now is you. The
last word "you" lands on the frame-0 composition, so the loop restarts on "The ocean's scariest hunter...".

**Topic note for the orchestrator.** The fact sheet and audience brief picked the deep-sea video (mzeN0BXR4e0); the
reference brief, drafts 2-3 and this final script follow the prehistoric-ocean premise (nAWpLtG-kNs, proven again by
qrfhhZ-Wvmk). `episodes/explainer-pressure-ladder` already covers the deep-sea ladder and the 8,336 m snailfish
twist. No `picked` row was written to data/sources.jsonl (Spark-owned).

## Edit log (retention pass)

| Change | Why |
|---|---|
| Hook: "This is the ocean's scariest hunter. It's as long as your arm." → "The ocean's scariest hunter was once as long as your arm." | Judges: present tense hid the time frame and the line ran 3.6 s. Now 11 words, one sentence, ~3 s; "was once" says *past*, "your arm" puts you and the scale in line 1. |
| Cut "Drag this slider forward, though," | Meta instruction, extra thing to parse in the 3-9 s window (judge 3). The scrubber is shown, not narrated. |
| Spoken era dates ("Three hundred and sixty million years ago") → teaser words "Armour." / "Jaws." / "Teeth." | Judges 2-3: long spoken numbers slowed the pace. Dates live on the era tag and scrubber; each rung now opens by paying the hook's teaser contract in order (PLAYBOOK §2). |
| "So would it even bother with you?" → "Would it even bother with a crumb like you?" | Graft from draft 2 ("to it you're a crumb"): gives the turn a reason, not just an assertion. |
| Cut the drowning comparison (6 vs ×50,000, "all water worldwide") | Judges: arithmetic on a phone, a category switch from "eats you", and a quiet ending. |
| New twist: "we kill about a hundred million sharks a year. Today, the ocean's scariest hunter is you." | Graft of draft 1's point-of-view flip ending ("the monster is ... You."), the most-liked reaction in the comment study. Same question, flipped direction; ends on the strongest word and mirrors line 1 word for word. |
| "Same answer as the first ocean" → "You'd last until your arms give out." | No memory test: the callback is the exact verdict phrase from rung 1, and the chip flips to the same sea-green HOURS. |
| Removed `[music: score_v2]` | Not a valid bed name; the pipeline's scored soundtrack is `score` (pipeline/audio/config.py). |

## Beat alignment

| Our beat (s, est.) | Reference beat | Ref timestamp | Device borrowed |
|---|---|---|---|
| S1 Hook 0-3.2: "scariest hunter" over a picture that undercuts it; your arm is the scale | WHALE "This is a whale" over a dog-sized animal | 0:00-0:02 | picture contradicts the claim; finished cover as frame 0 |
| S2 Teasers 3.3-7.6: armour, jaws, teeth, one hard cut each, most famous last | ERAS teaser montage; OCEANS three-monster trailer | 0:07-0:31 / 0:10-0:22 | compressed teaser stack = contract paid in order |
| S2 Rules + device 7.7-12.0 | ERAS rules + empty tier list; OCEANS score per era | 0:31-0:37 / 0:22 | "just you" rules; scrubber + survival chip on screen by ~10 s |
| S3 Rung 1, Cambrian 12.1-18.2 | ERAS Cambrian: the top predator wouldn't harm you | 1:50 | harmless apex predator as rung 0 |
| S3 Rungs 2-3, Devonian + Cretaceous 18.3-34.0 | OCEANS rungs; KITCHEN fixed slots | 4:43 / 11:19; 0:10-0:44 | era tag → place → predator + comparator → verdict chip |
| S4 Turn 34.1-41.6: the favourite falls (Megalodon) | PLAYBOOK S4 "not even top three"; OCEANS "you're not the main character" | 58-66 % / 14:13 | most famous rival lowers the threat; owned unknown as its own beat (WHALE 1:46) |
| S5-S6 Answer + twist 41.7-55.0: today; villain swap | OCEANS modern-ocean twist (84 %); SPERM / ORCA villain swap | 14:41-15:04 | safest era is now, proved by one hard number each way |
| S7 Stinger + loop 55.0-57.5: "...is you." → frame 0 | WHALE scrubber rewind to frame 0; KITCHEN two-word verdict closing line 1's frame | 2:17-2:31 / 1:04 | rewind = loop; last line mirrors the hook |

Every rung fills the same four slots in the same order: **era tag** (curtain or wipe, date on screen) → **place**
(habitat establishing frame) → **predator + one comparator** (arm, car, bus, hand) → **verdict chip** snaps onto the
scrubber.

## Facts to verify

- **Anomalocaris canadensis**, Burgess Shale (~508 Ma, "half a billion years ago"): about 60 cm (NHM), roughly an arm;
  top predator of its ecosystem. Bicknell et al. 2023, *Proc R Soc B*: its appendages were probably built for soft
  prey and would likely have been damaged on hard trilobite shells, so "probably couldn't even crack a shell".
  [AMNH](https://www.amnh.org/about/press-center/anomalocaris-canadensis-trilobite-shells) · [NHM](https://wifi.nhm.ac.uk/press-office/press-releases/-weird-shrimp--from-canada-preferred-squishy-prey.html)
- **Dunkleosteus terrelli**, Late Devonian (~360 Ma): typical adults ~3.4 m (Engelman 2023, *Diversity* 15:318), "as
  long as a car". No true teeth: self-sharpening bony jaw blades; ate other armoured fish. [MDPI](https://www.mdpi.com/1424-2818/15/3/318)
- **Mosasaurus hoffmannii**, Maastrichtian (~70 Ma): ~11-13 m (NHM), "as long as a bus" (~12 m). A marine
  reptile (squamate, "sea lizard") that breathed air and had to surface. [NHM](https://www.nhm.ac.uk/discover/what-is-a-mosasaur.html)
- **Otodus megalodon**, Miocene (~15 Ma on the tag): ~15-18 m (NHM), "longer than a bus"; largest teeth ~18 cm,
  about a hand. Fed on marine mammals including whales (bite-marked whale bones). Whether it would bother with a human
  is unknown, and the script says so. [NHM](https://www.nhm.ac.uk/discover/megalodon--the-truth-about-the-largest-shark-that-ever-lived.html)
- **Sharks today:** ISAF five-year global average ~6 unprovoked fatal bites a year. [ISAF](https://www.floridamuseum.ufl.edu/shark-attacks/yearly-worldwide-summary/)
- **Sharks killed by people:** Worm et al. 2013, *Marine Policy* 40:194-204: ~100 million (2000) and ~97 million
  (2010) a year from fishing, possible range 63-273 million. Say "about a hundred million"; on-screen tag
  "≈100 MILLION / YEAR (ESTIMATE)". It is total fishing mortality, not finning alone; never say "for their fins".
  Checked live 2026-11-02. [Worm et al. 2013 (RePEc)](https://ideas.repec.org/a/eee/marpol/v40y2013icp194-204.html) · [Dalhousie](https://www.dal.ca/news/2013/03/08/unsustainable--dal-researchers-on-the-global-shark-decline.html)
- **Verdict chips** (HOURS, MINUTES, SECONDS, HOURS?, HOURS) are our ranking, not data; each carries a small
  "BEST GUESS" tag, and the Megalodon line says aloud that nobody knows.
- **Avoided on purpose:** "the first ocean" (oceans are billions of years older than Anomalocaris; the hook says
  "was once"); Cambrian oxygen claims; Cameroceras lengths (contested); Jaekelopterus (brackish/fresh water);
  Dunkleosteus "bus-sized" or bite psi; Mosasaurus "17 m"; Megalodon "20 m+"; drowning statistics (all-water, a
  category switch); any causal link between shark culling and shark-bite rates (the two numbers sit side by side,
  never joined by "because").

## Narration

Pronunciation hints for TTS: Dunkleosteus = "dunk-lee-OSS-tee-us"; Mosasaurus = "MOH-zuh-SAW-rus"; Anomalocaris is
shown (name pill), not spoken.

```narration
The ocean's scariest hunter was once as long as your arm.

Then the ocean grew armour, then jaws, then teeth the size of your hand. [sfx: whoosh]

Drop into each ocean. No boat, just you, treading water. How long until something eats you?

Half a billion years ago? Nothing can. It probably couldn't even crack a shell. You last until your arms give out. [sfx: pop]

Armour. Dunkleosteus, a fish as long as a car, with bone blades instead of teeth, built to crack other armoured fish. You're not armoured. [sfx: impact] Minutes.

Jaws. Mosasaurus, a sea lizard as long as a bus. It breathes air, so it keeps surfacing, right where you're treading water. [sfx: impact] Seconds.

Teeth. Megalodon, longer than a bus. But it hunted whales. Would it even bother with a crumb like you?

Nobody really knows. Hours, maybe.

Now jump to today. [sfx: whoosh] Sharks kill about six people a year. You'd last until your arms give out.

Meanwhile, we kill about a hundred million sharks a year.

[sfx: stinger @-0.1] Today, the ocean's scariest hunter is you.
```

169 words, 11 paragraphs (= 11 scenes). At the explainer default (Kokoro am_michael, speed 1.1, ~190 wpm on past
episodes) that is ~53 s of speech plus ~3 s of sentence and paragraph gaps: **~56-60 s**, re-time to the TTS.
Hook 11 words / ~3.2 s; "you/your" in 9 of 11 paragraphs; 7 spoken numbers or comparators; the master question
("How long until something eats you?") is asked at ~10 s and answered at 70-100 %.

## Shot notes

Times are estimates at ~190 wpm and will be re-timed to the TTS word timings. CUT = one-frame hard cut on that word;
WIPE = 0.4-0.8 s diagonal wipe; CAM = continuous camera travel. Captions: whole 1-3 word phrases, low centre at ~74 %
height. Name pills: gradient pills at ~22 % height, 0.15 s after the name. Number tags sit on pointer lines pinned to
the object. **TimeScrubber** (new component, no existing kit file touched): a horizontal timeline across the top safe
area at ~12 % height with era ticks, a handle, and a survival chip riding the handle; it is in frame 0 already, so
the loop seam matches.

| # | Time (s) | Line | Shot / what moves on the word | Setting, palette, lightness | Kit |
|---|---|---|---|---|---|
| 1 | 0.0-3.2 | "The ocean's scariest hunter was once as long as your arm." | **Frame 0 = cover** (no black frame): split waterline; You, head and shoulders above a bright aqua Cambrian sea, one arm stretched out underwater; Anomalocaris lies alongside the arm, body the same length, frontal appendages curled. Scrubber at the far left reading "508 MILLION YEARS AGO", chip "?:??". On "scariest" it flares its appendages (verb beat). On "arm" tag "~60 cm" on a pointer; name pill "ANOMALOCARIS" at ~2.4 s. | Cambrian shallows: pale sand, sponges, a few trilobites; no fish, coral or plants; bare grey rock shore in the far layer. Aqua / sea green, highest lightness | You, Ocean(surface split), TimeScrubber, Tag, NamePill, Anomalocaris (new art) |
| 2 | 3.3-7.6 | "Then the ocean grew armour, then jaws, then teeth the size of your hand." | Scrubber handle twitches right on "Then". CUT on "armour": macro of Dunkleosteus's head plate, murky green. CUT on "jaws": a mosasaur's open jaw from below, sunlit surface above. CUT on "teeth": a megalodon tooth held beside a human hand, same size; deep blue. | Three teasers, each in its own era palette, darker each time | Dunkleosteus, Mosasaur, Megalodon tooth + Hand (new art) |
| 3 | 7.7-12.0 | "Drop into each ocean. No boat, just you, treading water. How long until something eats you?" | CUT on "Drop": back to the Cambrian wide, You drop in with a flat splash ring. On "No boat", a boat icon flies in and gets a flat red slash. On "treading water", legs kick below the line. On "How long", the chip pulses "?:??" with a small clock icon. | Cambrian surface, wide, sky-cyan band | TimeScrubber, You, Tag |
| 4 | 12.1-18.2 | "Half a billion years ago? Nothing can. It probably couldn't even crack a shell. You last until your arms give out." | CAM sinks below the waterline. On "Nothing can", Anomalocaris drifts past your legs and ignores you. On "crack a shell", it grabs a trilobite and its appendages bend and bounce off (flat arc); the trilobite scuttles off. CAM back up; your strokes slow. On "give out", chip snaps **HOURS** (sea green) + "BEST GUESS". | Cambrian underwater, then surface | camera move + 4 events |
| 5 | 18.3-26.0 | "Armour. Dunkleosteus, a fish as long as a car, with bone blades instead of teeth, built to crack other armoured fish. You're not armoured. Minutes." | WIPE on "Armour" as the handle slides to the Devonian tick; curtain reveals the orange era tag "360 MILLION YEARS AGO". Place: murky inland sea, small continent-map inset. Dunkleosteus glides in, name pill; on "car" a flat car silhouette at the same scale, tag "~3.4 m". On "bone blades" a yellow highlight ring outlines the jaw plates (x-ray slot); on "crack" it snaps a smaller armoured fish, flat plate shards. CUT on "You're not armoured" to You from below, legs dangling, Dunkleosteus rising behind. On "Minutes" chip **MINUTES** (orange). | Late Devonian inland sea: blue-green, muddy floor, mid lightness, darker on the cut | wipe + curtain + 1 cut, 6 events |
| 6 | 26.1-34.0 | "Jaws. Mosasaurus, a sea lizard as long as a bus. It breathes air, so it keeps surfacing, right where you're treading water. Seconds." | WIPE on "Jaws"; era tag "70 MILLION YEARS AGO". Place: warm shallow sea at sunset, an ammonite and a sea turtle in the mid layer. Mosasaurus crosses the full frame, name pill; on "bus" a flat bus silhouette, tag "~12 m". CAM rises with it; on "breathes air" its nostrils break the surface with a flat spray ring. On "right where you're" the camera tilts and You are a few metres away. CUT on "Seconds" to violet water with only the closing jaws as a silhouette; chip **SECONDS** (red). No contact shown. | Late Cretaceous seaway: royal blue, orange-magenta sky band; then indigo | wipe + camera move + 1 cut |
| 7 | 34.1-39.4 | "Teeth. Megalodon, longer than a bus. But it hunted whales. Would it even bother with a crumb like you?" | WIPE on "Teeth"; era tag "15 MILLION YEARS AGO". Place: open ocean, no seafloor. Megalodon rises from below, name pill; on "longer than a bus" the same bus silhouette slides in and is shorter than the shark, tag "~15-18 m". On "whales" a baleen whale crosses mid-frame and the shark turns toward it (cut away before any bite). On "crumb" CAM pulls back: You are a speck beside the shark, scale bracket; the shark's eye swivels to You. | Miocene open ocean: royal blue to indigo | wipe + camera move + 4 events |
| 8 | 39.5-41.6 | "Nobody really knows. Hours, maybe." | The eye swivels away again. On "Nobody really knows" a white "?" tag and a small "NOT KNOWN" stamp. On "Hours, maybe" chip **HOURS?** (yellow): the favourite drops a tier (TURN, ~62 %). | Same, wide | honesty beat, 2 events |
| 9 | 41.7-47.6 | "Now jump to today. Sharks kill about six people a year. You'd last until your arms give out." | On "jump" the handle races right, era ticks blur past. CUT on "today": modern coast, bright cyan, beach and a lighthouse in the far layer; You treading water; era tag "TODAY". A flat shark passes and ignores You; tag "≈6 PEOPLE / YEAR". On "arms give out" the chip flips to the same sea-green **HOURS** as rung 1 and the Cambrian tick lights up. | Modern coast: sky cyan, sun yellow, back to high lightness | 1 cut, 4 events |
| 10 | 47.7-51.0 | "Meanwhile, we kill about a hundred million sharks a year." | CUT on "Meanwhile" to the shark's point of view looking up: a fishing boat's hull and a long line of hooks drop through the cyan. On "hundred million" a flat counter tag "≈100 MILLION / YEAR" with "ESTIMATE" sub-tag; small shark icons fill the frame row by row (no gore, no fins cut). | Same coast, from below; lightness drops a step | 1 cut, 2 events |
| 11 | 51.1-54.5 | "Today, the ocean's scariest hunter is you." | On "scariest hunter" the name-pill slot that held ANOMALOCARIS, DUNKLEOSTEUS... pops a pill reading "YOU". On "is" the scrubber rewinds left and the frame **rewinds through every rung in reverse** (shark, megalodon, mosasaur, Dunkleosteus, ~0.25 s each). On "you" it lands on the exact frame-0 composition: you, arm out, Anomalocaris alongside, chip back to "?:??". Cut within 0.3 s of "you" (`ending: loop`). | Every palette in reverse, ending on frame 0's aqua | rewind = loop to frame 0 |

Pacing check (estimated):
- **Hard cuts:** 9 in ~55 s (line 2 ×3, 3, 5, 6, 9, 10, plus the loop landing), all on words: ~9.8 a minute,
  inside the 6-10 target.
- **Wipes and camera travel:** 3 wipes (eras) and 4 camera moves.
- **Visual events:** about 38, so one every ~1.5 s. No shot without camera travel runs past ~4.5 s.
- **Settings:** five (Cambrian shallows, Devonian inland sea, Cretaceous sunset seaway, Miocene open ocean, modern
  coast), each with its own palette and lightness: light falls from Cambrian to Miocene and comes back for today.
- **Names and scale:** every named animal gets a name pill; every size claim gets one comparator in frame (arm,
  hand, car, bus, you as a speck).

## Checklist (PLAYBOOK §10)

- Hook 11 words, ~3.2 s, "your" at word 10, subject on screen in frame 0, first word at ~0.15 s, no black frame.
- Teasers paid in order and by name: "Armour." (~33 %), "Jaws." (~48 %), "Teeth." (~62 %).
- Ladder climbs on two axes: date forward and predator size up (arm → car → bus → longer than a bus); verdicts
  hours → minutes → seconds, then the flip.
- Turn at ~62 % (the most famous predator lowers the threat); master question answered at 75-100 %.
- One owned unknown ("Nobody really knows") plus "BEST GUESS" tags on the verdicts.
- Twist changes axis (villain swap): the hunted becomes the hunter. Stinger on the strongest word, "you", which
  mirrors line 1; last frame = frame 0; no CTA.
- No gore: every kill cuts away before contact (R5).
- Originality: `python3 scripts/originality_check.py episodes/explainer-p1/script.md research/corpus research/library/transcripts`.
