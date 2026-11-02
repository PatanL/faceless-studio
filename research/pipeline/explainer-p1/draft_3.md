---
id: explainer-p1
draft: 3 (writer 3: concrete number / scale hook)
niche: explainer
lane: kurz (house style A, flat 2D in Remotion; no Blender)
title: How Long You'd Last in Every Prehistoric Ocean
alt_titles: The Ocean's Scariest Hunter Was As Long As Your Arm | Drag the Slider, Meet the Teeth
format: 9:16
target_s: 60 (measured estimate 58-61 s; 176 words at ~185 wpm plus beat pauses)
voice: am_michael (Kokoro, sentence-by-sentence, pipeline default)
music: score v2 (kurz Shorts study); brightens on the Cambrian and today rungs, darkens with each predator rung
references:
  - id: qrfhhZ-Wvmk, url: https://www.youtube.com/watch?v=qrfhhZ-Wvmk, views: 3374140, outlier_score: 6.54   # OCEANS: same premise, ocean-only cast
  - id: nAWpLtG-kNs, url: https://www.youtube.com/watch?v=nAWpLtG-kNs, views: 12209257, outlier_score: 113.57  # ERAS: ladder, verdict per era
  - id: 2cK8l5Yg5w8, url: https://www.youtube.com/watch?v=2cK8l5Yg5w8, views: 5194382, outlier_score: 3.58    # KITCHEN: Kurzgesagt 60-90 s list Short, fixed slots
  - lane form (not in corpus): oR3Q7RntqEw Kurzgesagt "Whales Evolved from This Animal", 5.25M, 1.9x channel Shorts median  # WHALE: contradiction hook, scrubber rewind loop
---

# explainer-p1, draft 3: the arm-length hunter

**Blender: no.** Flat 2D house style A in Remotion, like every kurz episode. Both Kurzgesagt references are flat
vector, 3D/Blender is parked (FEEDBACK_LOG 2026-11-01), and BRIEF rule 4 says every visual is code. (BRIEF rule 2
no longer reserves the Mac for Blender since 2026-11-02; it is now a Remotion render slot, so that reason no longer
applies, but the other three still hold.)

**Topic note for the orchestrator.** The inputs disagree on the topic. The reference brief picks the prehistoric
ocean (nAWpLtG-kNs, proven again by qrfhhZ-Wvmk). The fact sheet and the audience brief pick the deep-sea video
mzeN0BXR4e0. This draft follows the reference brief, for three reasons:
- The task says to follow the reference brief's structure (era rungs, time scrubber, today's ocean as the twist,
  rewind loop), and that structure only works with the era premise.
- `episodes/explainer-pressure-ladder` already covers the deep-sea ladder, including Challenger Deep and the
  8,336 m snailfish twist that the fact sheet proposes, so a deep-sea p1 would repeat it.
- Each era is a new setting, which meets the owner's "switch scenery more" note (FEEDBACK_LOG 2026-11-01, P3).

The fact sheet covers deep-sea facts only, so I checked every prehistoric number in this draft myself (see the
Facts section). None of the fact sheet's numbers is used.

**Hook type (writer 3).** A scale number that you can see at once. Frame 0 shows the Cambrian apex predator lying
along your own outstretched arm, so the claim "scariest hunter" is undercut by the picture, as in WHALE. The arm
then becomes the unit for the whole video: hand-sized teeth in the teaser, and the last word, "arms", loops back
to the first line.

**Premise.** You tread water and drag a time slider. At each stop, how long until something eats you? Five stops:
Cambrian, Devonian, Cretaceous, Miocene, today. The verdict curve goes HOURS, MINUTES, SECONDS, HOURS?, then back
to the first ocean's answer.

## Beat alignment

| Our beat (s) | Reference beat | Ref timestamp | Device borrowed |
|---|---|---|---|
| Hook 0-3.6: "scariest hunter" over a picture that undercuts it, with your arm as the scale | WHALE "This is a whale" over a dog-sized animal | 0:00-0:02 | picture contradicts the claim; cover frame 0 |
| Teasers 3.7-8.6: armour, jaws, teeth, three hard cuts, most famous last | ERAS teaser montage; OCEANS three-monster trailer | 0:07-0:31 / 0:10-0:22 | compressed teaser stack, one cut per noun |
| Rules + device 8.7-12.8 | ERAS rules + empty tier list; OCEANS score per era | 0:31-0:37 / 0:22 | "just you" rules; scrubber + survival chip |
| Rung 1 Cambrian 12.9-19.6 | ERAS Cambrian: the predator "wouldn't harm you" | 1:50 | harmless apex predator as rung 0 |
| Rungs 2-3 Devonian, Cretaceous 19.8-38.4 | OCEANS ESC-4 / ESC-8; KITCHEN fixed slots | 4:43 / 11:19; 0:10-0:44 | era tag, place, predator + comparator, verdict chip |
| Turn 38.6-46.8: the favourite falls (Megalodon) | PLAYBOOK L5b flip; OCEANS rung 9 "you're not the main character" | 58-66 % / 14:13 | most famous rival lowers the threat |
| Owned unknown 42.9-46.8 | WHALE "we don't know exactly" beat | 1:46 | honesty beat |
| Answer + twist 47.0-53.0: today's ocean, 6 vs 300,000 | OCEANS modern-ocean twist (one hard number) | 14:41-15:04 (84 %) | safest era is now, with one hard number |
| Loop 53.1-58.4: scrubber rewinds to frame 0, last word "arms" | WHALE scrubber rewind to the opening frame | 2:17-2:31 | rewind = loop; last word matches the hook |

Every rung uses the same four slots in the same order (brief, KITCHEN): **era tag** (curtain or wipe) → **place**
(habitat establishing frame) → **predator + one comparator** (arm, car, bus, hand, whale) → **verdict chip** snaps
onto the scrubber.

## Facts (checked live 2026-11-02; spot-check again before lock)

- **Anomalocaris canadensis**, Burgess Shale (~508 Ma, "half a billion years ago"). About 60 cm long ("about two
  feet", NHM), roughly a human arm. Apex predator of its time. Bicknell et al. 2023, *Proc R Soc B*: its grasping
  appendages were probably built for soft, fast prey, and modelling suggests they would have been damaged on
  hard-shelled trilobites. Say "probably couldn't even crack a shell"; the paper itself treats this as a tested
  hypothesis, not a certainty. [AMNH](https://www.amnh.org/about/press-center/anomalocaris-canadensis-trilobite-shells) · [NHM](https://wifi.nhm.ac.uk/press-office/press-releases/-weird-shrimp--from-canada-preferred-squishy-prey.html) · [Sci.News](https://www.sci.news/paleontology/anomalocaris-canadensis-appendages-12065.html)
- **Dunkleosteus terrelli**, Late Devonian (Cleveland Shale, ~360 Ma). Engelman 2023 (*Diversity* 15:318): typical
  adults about 3.4 m, the largest about 4.1 m. Say "as long as a car" (a small car is 3.5-4 m). It had no true
  teeth, only bony jaw plates with sharp blades, and probably ate other large armoured fish. Don't use "bus-sized"
  or a psi bite figure. [MDPI](https://www.mdpi.com/1424-2818/15/3/318) · [Sci.News](https://www.sci.news/paleontology/dunkleosteus-terrelli-11735.html)
- **Mosasaurus**, Late Cretaceous (Maastrichtian, ~70-66 Ma). Estimates for *M. hoffmannii* run about 11-13 m, and
  some go up to 17 m (NHM; Cleary et al. 2018 calls the high end probably overestimated). Say "as long as a bus" (a
  bus is about 12 m). Mosasaurs were reptiles and breathed air, so they came to the surface. Their jaws were
  jointed partway along and flexible, like a snake's (Britannica). That last fact is not spoken; it is shown as an
  optional x-ray. [NHM](https://www.nhm.ac.uk/discover/what-is-a-mosasaur.html) · [Britannica](https://www.britannica.com/animal/mosasaur)
- **Megalodon (Otodus megalodon)**, Miocene (~15 Ma; extinct ~3.6 Ma). Estimates are about 15-18 m (NHM), from
  teeth. Say "longer than a bus". Teeth are about the size of a human hand (Geological Society). It fed on marine
  mammals including whales; fossil whale bones carry its bite marks. Whether it would bother with a human is
  unknown, and the script says so. [NHM](https://www.nhm.ac.uk/discover/megalodon--the-truth-about-the-largest-shark-that-ever-lived.html)
- **Sharks today:** ISAF's five-year global average is about **6 unprovoked fatal bites a year** (4 in 2024, 9 in
  2025). [ISAF 2025 report](https://www.floridamuseum.ufl.edu/shark-attacks/yearly-worldwide-summary/)
- **Drowning:** WHO, *Global status report on drowning prevention 2024*: **about 300,000 deaths in 2021**.
  300,000 ÷ 6 = 50,000, so "fifty thousand times that" is exact. Caveat: this covers drowning in all water (rivers,
  lakes, pools, sea), not only the ocean. The on-screen tag says "ALL WATER, WORLDWIDE" so the comparison stays
  honest. [WHO](https://www.who.int/publications/i/item/9789240103962) · [RLSS summary](https://www.royallifesaving.com.au/about/news-and-updates/news/2024/dec/who-report-reveals-staggering-global-drowning-toll-30-lives-lost-every-hour)
- **Verdict chips** (HOURS, MINUTES, SECONDS, HOURS?) are our ranking, not data. Each chip carries a small
  "BEST GUESS" tag, and line 11 says aloud that nobody knows.
- **Avoided on purpose:** the Cambrian low-oxygen "Everest" line (overstated, per the OCEANS fact note); Cameroceras
  lengths (contested); Jaekelopterus (Devonian and probably brackish or fresh water, so not an open-ocean rung);
  Dunkleosteus "bus-sized" and bite psi; Mosasaurus "17 m" as fact; megalodon "20 m+"; "OCEANS' second row of
  teeth" (their device, not ours).

## Narration

Pronunciation hints for TTS: Dunkleosteus = "dunk-lee-OSS-tee-us"; Mosasaurus = "MOH-zuh-SAW-rus"; Anomalocaris
is shown, not spoken.

```narration
[music: score_v2] This is the ocean's scariest hunter. It's as long as your arm.

Drag this slider forward, though, and the ocean grows armour, then jaws, then hand-sized teeth. [sfx: whoosh]

Rules: just you, treading water, no boat. How long until something eats you?

Half a billion years ago? Nothing can. It probably couldn't even crack a shell. You last until your arms give out. [sfx: pop]

Three hundred and sixty million years ago: Dunkleosteus. An armoured fish as long as a car.

No teeth, just bone blades, made for cracking other armoured fish. You're not armoured. Minutes. [sfx: impact]

Seventy million years ago: Mosasaurus, a sea lizard as long as a bus.

It breathes air, so it keeps surfacing, right where you are. Seconds. [sfx: impact]

Fifteen million years ago: Megalodon. Longer than a bus, and it ate whales.

So would it even bother with you? Nobody really knows. Hours, maybe.

Now drag it to today. [sfx: whoosh]

Sharks kill about six people a year. Drowning kills fifty thousand times that.

Same answer as the first ocean: almost nothing hunts you. The water just outlasts your arms.
```

Word count 176. Sentences average about 8 words, with 1-2 word verdict punches. "You/your" appears in 9 of 14
lines, or 64 % (target ≥ 60 %). There are 13 spoken numbers or scale units in about 60 s, at the top of the ranking
range; each is either a single comparator or a date tag. Master question: "How long until something eats you?" Its
answer, at 80-100 %, is that today's ocean barely hunts you at all.

## Shot list: every line on screen

Times are estimates at ~185 wpm and will be re-timed to the TTS. CUT means a one-frame hard cut on that word; WIPE
means a 0.4-0.8 s diagonal wipe; CAM means continuous camera travel. Captions are whole phrases, low centre at
~74 % height. Name pills are gradient pills at ~22 % height, shown 0.15 s after the name. Number tags sit on pointer
lines pinned to the object. **TimeScrubber** is a new component: a horizontal timeline bar across the top-safe
area at ~12 % height, with era ticks, a draggable handle, and a survival chip that rides the handle.

| # | Time (s) | Line (spoken) | Shot / what moves on the word | Setting, palette, lightness | Change |
|---|---|---|---|---|---|
| 1 | 0.0-3.6 | "This is the ocean's scariest hunter. It's as long as your arm." | **Frame 0 = cover**: You, head and shoulders above a bright aqua Cambrian sea, half-underwater view (split waterline). Anomalocaris, mid-frame below the line, swims toward camera. On "scariest" it flares its frontal appendages (verb beat). On "arm" You stretch an arm out underwater and Anomalocaris slides up alongside it; its body matches the arm's length; tag "~60 cm" on a pointer. Name pill "ANOMALOCARIS" pops at ~2.4 s. | Cambrian shallows: pale sand floor, sponges, a few trilobites, no fish, no coral, no plants; bare grey rock shore in the far layer. Aqua / sea green, high lightness | opening shot 3.6 s, alive through 3 motion beats |
| 2 | 3.7-8.6 | "Drag this slider forward, though, and the ocean grows armour, then jaws, then hand-sized teeth." | On "slider", the TimeScrubber drops in at the top; a hand-cursor grabs the handle and drags right. CUT on "armour": macro of Dunkleosteus's armoured head plate, dark green water. CUT on "jaws": a mosasaur's open jaw from below, sunlit surface above. CUT on "teeth": megalodon tooth held beside a human hand, same size (comparator); deep blue. | Three teasers, each in its own era palette (green → blue-gold → royal blue), darker each time | 3 hard cuts, ~1.1 s apart |
| 3 | 8.7-12.8 | "Rules: just you, treading water, no boat. How long until something eats you?" | CUT back to the Cambrian wide: You tread water at the surface. On "no boat", a little boat icon flies in and is crossed out (flat red slash). On "How long", the survival chip appears on the scrubber handle reading "?:??". The scrubber reads "508 MILLION YEARS AGO". | Cambrian surface, wide, sunny aqua sky band | device on screen by ~10 s; hard cut + 2 events |
| 4 | 12.9-19.6 | "Half a billion years ago? Nothing can. It probably couldn't even crack a shell. You last until your arms give out." | CAM: the camera sinks below the waterline. On "Nothing can", Anomalocaris drifts past your legs and ignores you. On "crack a shell", it grabs a trilobite and its appendages bend and bounce off (flat "boing" arc); the trilobite scuttles away. CAM back up: You tread water and your arms slow down. On "arms give out", the chip snaps in: **HOURS** (sea green) with a small "BEST GUESS" tag. | Cambrian underwater, then surface | camera move + 4 events; no shot over 6 s without travel |
| 5 | 19.8-25.0 | "Three hundred and sixty million years ago: Dunkleosteus. An armoured fish as long as a car." | WIPE (diagonal) as the scrubber handle slides to the Devonian tick. A flat curtain opens on a big orange **era tag "360 MILLION YEARS AGO · DEVONIAN"**. The place: an inland sea seen from above, with a small map inset of the continents (Laurussia shoreline). Dunkleosteus glides in; name pill. On "as long as a car", a flat car silhouette fades in beside it at the same scale, with tag "~3.4 m". | Late Devonian inland sea: murky blue-green, muddy floor, a few small placoderms. Mid lightness | wipe + curtain + 3 events |
| 6 | 25.1-30.0 | "No teeth, just bone blades, made for cracking other armoured fish. You're not armoured. Minutes." | Close-up: the jaw opens and a yellow highlight ring outlines the blade plates (x-ray mechanism slot). On "cracking", it snaps a smaller armoured fish; flat plate shards fly. CUT on "You're not armoured" to You at the surface from below, legs dangling, Dunkleosteus rising in the background. On "Minutes", the chip snaps: **MINUTES** (orange). | Same Devonian sea, darker | 1 hard cut, 4 events |
| 7 | 30.2-34.4 | "Seventy million years ago: Mosasaurus, a sea lizard as long as a bus." | WIPE: the scrubber slides to the Cretaceous tick, and the era tag "70 MILLION YEARS AGO · CRETACEOUS" is revealed on a curtain. The place: a warm shallow sea at sunset, with an ammonite and a sea turtle in the mid layer. Mosasaurus passes the full width of the frame; name pill. On "bus", a flat bus silhouette appears beside it, with tag "~12 m". | Late Cretaceous seaway: royal blue water, orange-magenta sunset sky band | wipe + 3 events |
| 8 | 34.5-38.4 | "It breathes air, so it keeps surfacing, right where you are. Seconds." | CAM: the camera rises with the mosasaur. On "breathes air", its nostrils break the surface and a flat spray ring appears. On "right where you are", the camera tilts and You are a few metres away, treading water (same You). CUT on "Seconds" to black-violet water with only the closing jaws as a silhouette; the chip snaps **SECONDS** (red). No gore: the cut happens before contact. | Surface, then indigo | peak of the ladder; camera move + 1 hard cut |
| 9 | 38.6-42.8 | "Fifteen million years ago: Megalodon. Longer than a bus, and it ate whales." | WIPE: the scrubber slides to the Miocene tick; era tag "15 MILLION YEARS AGO · MIOCENE". The place: open ocean, deep royal blue. A baleen whale crosses mid-frame; Megalodon comes up from below, and its name pill pops. On "longer than a bus", the same bus silhouette from line 7 slides in and is shorter than the shark (the comparator is reused on purpose for honesty); tag "~15-18 m". On "ate whales", the camera follows the shark toward the whale; the frame cuts away before the bite. | Miocene open ocean: royal blue to indigo, no seafloor | wipe + 3 events; TURN begins (~66 %) |
| 10 | 42.9-46.8 | "So would it even bother with you? Nobody really knows. Hours, maybe." | CAM pulls back: You are a speck next to the shark; a scale bracket labels the gap. On "bother", the shark's eye swivels to You and away again (verb beat). On "Nobody really knows", a "?" tag in white on a pointer, plus a small "NOT KNOWN" honesty stamp. On "Hours, maybe", the chip snaps **HOURS?** (yellow), the favourite knocked down a tier. | Same, wide | camera move + 3 events |
| 11 | 47.0-48.6 | "Now drag it to today." | The handle drags fast to the far right; era ticks blur past. CUT on "today" to a modern sea: bright cyan, a beach with sand and a lighthouse in the far layer, a swimmer (You) in calm water. Era tag "TODAY". | Modern coast: sky cyan, sun yellow, the highest lightness in the video | 1 hard cut |
| 12 | 48.7-53.0 | "Sharks kill about six people a year. Drowning kills fifty thousand times that." | A flat shark swims past You; tag "≈6 / YEAR" with a small shark icon. CUT on "Drowning": the camera pulls out to a flat bar chart floating over the water. The shark's 6 is a one-pixel sliver; the drowning bar rises off the top of the frame. Tags "≈300,000 / YEAR" and "ALL WATER, WORLDWIDE". | Modern coast, chart overlay | 1 hard cut, 3 events |
| 13 | 53.1-58.4 | "Same answer as the first ocean: almost nothing hunts you. The water just outlasts your arms." | On "first ocean", the chip flips to the same sea green **HOURS** as the Cambrian rung, and the Cambrian tick lights up. On "almost nothing hunts you", the shark turns away. On "outlasts", the scrubber rewinds left, and the frame **rewinds through every rung in reverse** (megalodon, mosasaur, Dunkleosteus, ~0.25 s each). It lands on "arms" in the exact frame-0 composition: You with an outstretched arm and Anomalocaris sliding alongside. Cut within 0.3 s of "arms". | Every palette in reverse, ending on the aqua of frame 0 | rewind = loop to frame 0 |

Pacing check (estimated):
- **Hard cuts:** 9 in ~58 s (lines 2 ×3, 3, 6, 8, 11, 12, plus the rewind landing), all on words. That is 9.3 a
  minute, inside the 6-10 target.
- **Wipes and camera travel:** 4 wipes (eras) and 4 camera moves.
- **Visual events:** about 40, so one every ~1.5 s.
- **Shots:** the longest single shot without travel is line 1 (3.6 s), and no shot without camera travel goes past
  6 s.
- **Settings:** five distinct ones (Cambrian shallows, Devonian inland sea, Cretaceous sunset seaway, Miocene open
  ocean, modern coast), each with its own palette and lightness. Lightness falls from Cambrian to Cretaceous, then
  comes back with the bright modern coast.
- **Names and scale:** every named animal gets a name pill. Every size claim gets one comparator in frame (arm,
  hand, car, bus, You as a speck).

## Checklist (PLAYBOOK §10)

- Hook ≤ 12 words (12), with "you" (as "your") inside the first 12 words, the subject on screen in frame 1, and
  the first word at 0.0 s.
- Teasers are paid in order: armour (Devonian, 33 %), jaws (Cretaceous, 52 %), teeth (Megalodon, 66 %).
- The ladder climbs on two axes: date forward, and predator size up (arm → car → bus → longer than a bus). The
  verdicts go hours → minutes → seconds, then the flip.
- Turn at 66 %: the most famous predator lowers the threat. The master question is answered at 80-100 %.
- One owned unknown ("Nobody really knows"), and "BEST GUESS" tags on the verdicts.
- Stinger: the strongest word, "arms", closes line 1's frame. The last frame matches frame 0. No CTA.
- No gore: every kill cuts away before contact (R5).
- Originality: `python3 scripts/originality_check.py research/pipeline/explainer-p1/draft_3.md research/corpus research/library/transcripts` printed **PASS** (2026-11-02).
