---
slug: sinking-to-the-bottom
niche: explainer
format: long-form 16:9 (1920x1080)
title: "How Many Times Would The Ocean Kill You On The Way To The Bottom?"
title_options: titles.md (10 ranked options mapped to viral title patterns)
variant: "Ladder/countdown, ERAS sawtooth sub-form (PLAYBOOK 1a): spoken flip at 65%, end game on 0 cheats from 75% with a 3-option plan-killer loop (77-80%), climax inside the final item (landing test, 84-88%), peak declared at 88%, twist from 89%, bookend at 97%, no spoken CTA"
promoted_from: backlog/explainer/explainer-sinking-every-1000m (reviewed 2026-11-01 04:25 UTC, self-assessed 8/8/8/7). Revision 2 (2026-11-01 ~13:10 UTC) applies three long-form reviews (scores 7/7/6, see review.json): zero-cheat test at the landing, a 3-option plan-killer loop, spoken 65% flip, DEATH 3 paid by the planted squeeze, fact fixes, a split twist zone. Line numbers below are the NEW numbering (62 lines).
selection: "Picked over explainer-never-meet-orca, explainer-every-animal-that-could-swallow-you and explainer-never-meet-leopard-seal; reasons in the 'Why this one' section below."
target_runtime_s: 599.6          # 9:59.6 ESTIMATED = 9:54.6 of speech + gaps, then a 5 s held board. Brief range 8-10 min. If the re-measure lands over 600 s, cut the hold to 4.5 s first, then the "Please don't try to play it" tag (line 30)
target_words: "1,500-1,700"
words: 1571                      # narration only, counted by whitespace split of the pipeline block (timing.json in this folder still describes revision 1; regenerate it at the build gate, assets.md §5)
target_wpm: "~170 (PLAYBOOK long-form 160-170; R1: Depth Theory sperm whale ~170 wpm, 10 min ~ 1,680 words)"
wpm_measured: 166                # Kokoro am_michael speed 1.0, CPU, Spark: speech only. 160 over the full runtime
timing_source: "MEASURED (Kokoro am_michael 1.0 word timestamps from the parent's durations.json, text unchanged): lines 1-5, 7-12, 14-17, 19-29, 32-39, 41, 46, 51, 54-55, 62. ESTIMATED (0.362 s/word, the measured mean, + 0.25 s tail), each tagged (estimated: re-measure): lines 6, 13, 18, 30-31, 40, 42-45, 47-50, 52-53, 56-61 (22 lines). Every time from 0:53.4 onward is provisional until the build gate re-runs Kokoro on the estimated lines and regenerates timing.json (assets.md §5). WRITING ONLY lane: no TTS was run."
voice: "Kokoro-82M am_michael, speed 1.0 (pinned; 0.86 -> 148 wpm and 0.96 -> 162 wpm were measured and rejected)"
music: "deep_ocean bed (studio/public/music/deep_ocean.m4a), ducked under VO; drops out for the three death stamps and from the twist turn [pause: 0.5] to the bag reveal"
hook_words: 17                   # 0:00.1-0:05.7; drop lands on "drops" at 0:04.7
first_rung_s: 28.5               # "Ten metres down" (PLAYBOOK <= 45 s)
format_reveal_s: 40.5            # DepthMeter from 0:05; ALIVE? meter + CHEATS LEFT 3 from 0:40
references:
  - id: nAWpLtG-kNs
    short: ERAS
    url: https://www.youtube.com/watch?v=nAWpLtG-kNs
    title: "How Long You'd Last in Every Prehistoric Era (Fossil)"
    views: 12209257
    outlier_score: 113.57
    why_chosen: "The engine: a 'how long would YOU last' ladder with rules that make verdicts comparable, a 4-teaser contract paid in order, a visible board, a sawtooth verdict curve, host rulings, a viewer strategy that gets punished, and a twist that turns an opening rule around."
  - id: mzeN0BXR4e0
    short: DEEP
    url: https://www.youtube.com/watch?v=mzeN0BXR4e0
    title: "Why Deep Sea Creatures Get Creepier the Deeper You Go (Mr. Science)"
    views: 17219766
    outlier_score: 12.86
    why_chosen: "Same premise family (a descent where each zone is more hostile and its life stranger). We borrow the zone-entry ritual, first-rung-longest pacing, a dated human aside, the gross-out near 44%, the 'and yet' reversal, an Everest scale image near 72-75% and the left-open ending. We break its hadal fact order on purpose (see Originality notes)."
  - id: fGcgWaswMns
    short: SPERM
    url: https://www.youtube.com/watch?v=fGcgWaswMns
    title: "Why You'd Never Want To Meet A Sperm Whale (Depth Theory)"
    views: 2307237
    outlier_score: 14.65
    why_chosen: "The house voice, art style and length we copy (R1: 2.29M at 16.3x, a 10-min long-form at ~170 wpm). Devices only: an everyday comparison for every number, 'picture it again' at the midpoint, options killed by callbacks, a villain swap, and a bookend back to the opening image."
  - id: qrfhhZ-Wvmk
    short: OCEANS
    url: https://www.youtube.com/watch?v=qrfhhZ-Wvmk
    title: "How Long Would You Survive In Every Ocean Era? (BeyondTheBlue)"
    views: 3370000
    outlier_score: 6.54
    why_chosen: "PLAYBOOK §11 names it the closest premise to ours (ocean 'how long would you last' long-form). Borrowed: the plan-killer loop, where a sensible viewer plan is voiced as a question and killed by a fact the video already gave (3:26-4:19 shore strategy -> 'completely useless'; 5:56-6:05 steel shark cage -> 'you're still going to die. Here's why.'), and the 'stakes completely shift' reset (13:22)."
device_only_source:
  - id: fmZfphacPPQ   # Zack D. Films "Could You Survive Extreme Ocean Pressure?" 14.71M, 1.84x. Cited for two devices only (mild first symptom; planted mechanism that returns as the cause of death)
originality: "python3 scripts/originality_check.py backlog/longform/sinking-to-the-bottom/script.md research/corpus research/library/transcripts -> see 'Originality gate' at the end of this file"
disclosure: description.md (R5: YouTube Attributes > AI use = Yes; synthetic-voice caption line)
---

# How Many Times Would The Ocean Kill You On The Way To The Bottom? (long-form, 16:9)

## Why this one (selection)

| Candidate | Demand evidence (TOPICS.md, R1, corpus) | Format fit (PLAYBOOK) | Production fit | Verdict |
|---|---|---|---|---|
| **explainer-sinking-every-1000m** | Highest ceiling in the niche: mzeN0BXR4e0 17.22M (12.86x), Insider Tech depth animation 83.6M; the ERAS engine nAWpLtG-kNs 12.21M (113.57x) and its ocean clone qrfhhZ-Wvmk 3.37M (6.54x) | Ladder: 8 of 12 long outliers use a ladder (PLAYBOOK 1a). Countable master question answered by a board (PLAYBOOK §9.5 progress device) | DepthMeter, Ocean depth darkening and Options already exist; one global depth track drives every shot | **PICK** |
| explainer-never-meet-orca | WILD VERSUS 56M, OctoLab 8.29M (318.82x) | Dossier, strong paradox | Same subject as pilot `explainer-orca` (9:16, already rendered): a second orca upload so soon risks R5's "templated sameness" and splits the audience | hold until the pilot's numbers are in |
| explainer-every-animal-that-could-swallow-you | Occam JkAcCdqYJN0 0.33M (15.82x); "swallowed by a whale" 16-20M | Ladder, close to Occam's own premise | Needs the most new drawings (six throats + gauge) | second |
| explainer-never-meet-leopard-seal | Animalogic 3.2M, Nat Geo face-off 12.3M; no long-form outlier in the corpus | Dossier on the Depth Theory template | Needs a new seal/penguin set | third |

R1 says the Depth Theory hit is a 10-min long-form at about 170 wpm and that the subject matters more than the template (the hit and the flop share a title). The depth descent is the biggest proven category in the corpus, it puts YOU at risk in every rung (PLAYBOOK §9.1), and it has the cheapest visual system of the four.

## Premise

You ride a sled from the surface above the Mariana Trench to the floor of Challenger Deep at about 1 m/s (about three hours). The master question, asked aloud at 0:23 and printed in the title, is how many times the ocean kills you before you reach the bottom. Three rules make every verdict comparable. One: you can breathe. Two: every death costs one cheat; you get three, and when they run out the trip is over. Three: no submarine, so you will be the first thing of ours to reach the bottom without one. A depth meter and an ALIVE? meter track you the whole way. The ocean kills you three times (cold at 3 km, an avalanche at ~6.15 km, and at ~8.3 km the pressure that has been squashing your proteins since 7 km wins at the depth where even the snailfish's TMAO runs out), so the last 2.6 km run on zero cheats. Cheat 3 is named: you borrow the hadal crustaceans' pressure-proof proteins. A three-option plan loop (float up / wait for rescue / hold your breath) is killed by callbacks. The landing is the hardest test: the squeeze is a third stronger than the one that killed you, the needle slides toward NO and the borrowed trick stops it. The twist turns rule three around: a plastic bag got there first, and the trench amphipods carry swallowed fibres (plastic among those tested) and PCBs.

**Geometry.** Open water above the trench to 3.7 km; at the average-depth beat the current pushes the sled onto the trench's west wall and it slides down that wall to the floor (a WALL layer in every later descent shot), so every seafloor encounter happens on the wall.

**Verdict curve (the final board, one row per 1 km band).**

| band (km) | 0-1 | 1-2 | 2-3 | 3-4 | 4-5 | 5-6 | 6-7 | 7-8 | 8-9 | 9-10 | 10-bottom |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ALIVE? | YES | ? | DEATH 1 (cold) | YES | YES | MOSTLY | DEATH 2 (avalanche) | BARELY | DEATH 3 (the squeeze, past the fish ceiling) | YES | YES, 0 cheats (needle stopped short of NO) |
| cheats left | 3 | 3 (a maybe earns none) | 2 | 2 | 2 | 2 | 1 | 1 | 0 | 0 | 0 |

## Beat alignment to the PLAYBOOK long-form skeleton (L1-L9)

Our times: revision-2 line starts (measured lines 1-5 fixed; everything from 0:53.4 provisional, see `timing_source`). Percentages use the 599.6 s estimated runtime. Reference timestamps were checked against `research/corpus/explainer/<id>.md`.

| PLAYBOOK beat (target %) | Our beat (line) | Our time (%) | Reference id + timestamp | Device borrowed | How we adapt it |
|---|---|---|---|---|---|
| L1 cold open hook (0-4%) | Strapped to the sled; the ring empties on "drops" (1) | 0:00-0:05.7 (0-1%) | nAWpLtG-kNs 0:00; fmZfphacPPQ 0:00-0:03 | 2P premise in one sentence, experiment already starting (17 words) | A 5 s Timer ring hits zero exactly on "drops". |
| L1 teaser contract | Four teasers, most mysterious last (2) | 0:06-0:23 (1-4%) | nAWpLtG-kNs 0:10-0:19 | Teasers as a contract, paid in order | Paid at 21%, 36%, 70% and 90%. |
| L2 stakes / rules (4-9%) | Master question aloud, then three rules (3-6) | 0:23-1:09 (4-12%) | nAWpLtG-kNs 0:22-0:24 | Stakes question before rules; one rule planted for the end | Rule 3 is reworded to stay true ("fewer than have been to space"). |
| L3 promise + format reveal (by 45 s) | DepthMeter with the drop; ALIVE? + CHEATS LEFT 3 on rule two (2, 5) | 0:05 / 0:40 | nAWpLtG-kNs 0:31-0:35; mzeN0BXR4e0 1:34 | Visible progress device before rung 1 | Two meters; the board appears only when full (88%). |
| L4 rung 1, format-teaching (10-25%, longest) | 0-1 km (4-12) | 0:28-2:04 (5-21%) | mzeN0BXR4e0 1:18-6:06; fmZfphacPPQ 0:03-0:07 | First unit longest; mild relatable first symptom | 96 s. |
| L4 zone-entry ritual | Twilight 1:10, midnight 1:45, abyss 4:03, hadal 5:17 | 12/18/41/53% | mzeN0BXR4e0 1:39, 6:08, 9:12, 12:28 | Each chapter names its zone | Named at the HUD boundary. |
| L5 escalation, plant + thumbnail payoff | "its dinner" -> giant squid whose eye "has turned toward you" -> scars (10, 13, 14) | 1:39 -> 2:05-2:28 (17-25%) | mzeN0BXR4e0 5:59; fGcgWaswMns 2:23 | Soft cliffhanger bridge; prey fights back | Line 13 now pays the thumbnail promise IT SEES YOU at 21%. |
| L5 honest unknown (once) | Nerves misfire; "nobody knows" -> "?" (15, 16) | 2:28-2:51 (25-29%) | mzeN0BXR4e0 2:46 | Admitted unknown, reprised at the end | Reprised by the bookend. |
| L5 sawtooth drop 1 | DEATH 1: the cold (19) | 3:15 (33%) | nAWpLtG-kNs 8:34 | First hard drop | "Within half an hour" now matches the cold-water tables. |
| L5 close a long loop (~35%) | Teaser 2 paid: the beaked whale's breath (22) | 3:36 (36%) | fGcgWaswMns 2:42-2:58 | You-vs-it on time | 222 min vs your ~182 min fall. |
| L5 reversal re-hook | Average depth... but you're over a trench (23, 24) | 3:46-4:03 (38-41%) | mzeN0BXR4e0 9:12 | Reverse "this is where the ocean ends" | Geometry beat (onto the wall). |
| L5 turnstile + gross-out (40-45%) | Good news / bad news -> bait cam -> grenadiers circle YOU (26-28) | 4:12-4:40 (42-47%) | nAWpLtG-kNs 1:23-1:46; mzeN0BXR4e0 7:49 | Contrast pair; most shareable fact at ~44% | No gore. |
| L5 viewer strategy | STRATEGY: KEEP MOVING (28) | 4:33 (46%) | nAWpLtG-kNs 5:33; qrfhhZ-Wvmk 3:26-4:19 | The viewer's plan is where the next threat lives | Punished at 5:45 (58%) and again by option 1 at 7:40. |
| L5 re-immersion (~47%) | "Picture where you are" (29) | 4:40 (47%) | fGcgWaswMns 4:43-4:46 | Put the viewer back in the scene | More water below than above. |
| L5 dated human aside | Japan Trench mud, 2011 (35) | 5:36 (56%) | mzeN0BXR4e0 5:21-5:39 | Dated event breaks the parade | One sentence + map. |
| L5 sawtooth crash | DEATH 2: the wall avalanche (36) | 5:50 (58%) | nAWpLtG-kNs 8:38-9:57 | Sawtooth crash | Strategy punished. |
| **L5b the 60-65% flip (58-66%)** | **Spoken flip: "the question changes: not what kills you, but what can live where you can't" (40)** + HUD state change (ALIVE? panel turns from red-alert to a teal LIVES HERE? panel for the snailfish beat, water line on the DepthMeter turns teal) | 6:29 (65%) | nAWpLtG-kNs 8:38-9:57; mzeN0BXR4e0 6:25, 13:21 ("and yet") | Change the question the video is asking, with a visible change | One 17-word spoken line, then the creature entrance. |
| L6 facts become the weapon | Line 39 plants "the chemistry of being alive starts to jam"; line 41 sets the fish's TMAO ceiling; line 43: "the squeeze that was jamming your proteins keeps climbing, and right where even the fish's TMAO runs out, it wins" -> DEATH 3; teaser 3 paid (42) | 6:14 -> 7:06 (62-71%) | fmZfphacPPQ 0:12 -> 0:25 (planted mechanism returns as the cause); nAWpLtG-kNs 12:25 | Planted mechanism is the cause of death | The kill pays line 39, not chemistry YOU never had. |
| L6 stakes reset | Cheat 3 named ("proteins built to hold their shape under the squeeze") + "slightly shrimpier" + "Die again, and the trip is over" (44, 45) | 7:17-7:32 (73-75%) | nAWpLtG-kNs 14:53-14:57; qrfhhZ-Wvmk 13:22 ("the stakes completely shift") | Tell the viewer the end game has started | The trick is paid in the same line; it returns as the reason you survive the landing. |
| L6 signature scale image (72-75%) | One Everest down, 2 km still below (46) | 7:33 (76%) | mzeN0BXR4e0 12:52-13:07 | Everest-in-the-trench image | Everest hung from the surface, summit at YOU. |
| **L6 options killed by callbacks (§3 device 11, §4 "facts become the weapon")** | "Can you save yourself?" 1 float up -> three hours back along the wall that buried you (DEATH 2); 2 wait for rescue -> deepest rescue shallower than the sperm whale (line 9); 3 hold your breath like the beaked whale -> "Great plan, if you were a whale. Breath was never the problem. The squeeze is." (lines 22, 39, 43) (47-49) | 7:40-8:04 (77-80%) | fGcgWaswMns 5:59-7:05; qrfhhZ-Wvmk 3:26-4:19 (shore strategy killed) and 5:56-6:05 (shark cage: verdict first, then "here's why") | Each sensible plan voiced as a question, killed by an earlier rung | Options board with 3 strikes on screen (s67b_options). |
| L6 plant for the twist | Amphipod gut: "whatever sinks ends up inside it. Remember that." (50) | 8:05 (81%) | fmZfphacPPQ 0:12 | Throwaway detail paid in the twist | Unlabelled grey speck in the x-ray. |
| L6 climax inside the final item (85-95%) | Landing on 0 cheats: the squeeze that killed you is a third stronger (~1,100 vs ~830 bar); the needle slides toward NO and stops because the crustacean trick holds (52, 53) | 8:22-8:46 (84-88%) | nAWpLtG-kNs 14:53-15:47 | The final item is the hardest test | The needle's movement now has a cause (the squeeze) and a cause for stopping (cheat 3). |
| L6/L8 finished board + peak declared | FINAL READING (54) | 8:46 (88%) | nAWpLtG-kNs 14:45-14:49, 16:01 | Announce the peak, then show the board | Rows = verdict curve above. |
| L7 twist | Rule three turned around (55) | 8:54 (89%) | nAWpLtG-kNs 15:41-15:47 | Opening rule used against the viewer's win | 2P. |
| L7 teaser 4 paid + punch | The 1998 single-use plastic bag (56) -> "It beat you here. No cheats. No help." (57) | 8:59-9:10 (90-92%) | nAWpLtG-kNs 14:53-14:55; PLAYBOOK §3 device 10 (re-hooks densest near the end) | Reveal, then a 1-4 word punch | Was one 40-word line; now reveal + three-beat punch. |
| L7 human harm reaches the deep | Fibres (58) -> "That grey speck in its gut? Ours." (59) -> PCBs, "eleven kilometres from the nearest factory" (60) | 9:11-9:30 (92-95%) | mzeN0BXR4e0 14:07-14:19 | Human-relevance turn | Paddy-field-crab comparison moved to on-screen text (PLAYBOOK §9.3). |
| L7 villain swap | "The cold, the mud, the fish's ceiling: not one of the things that killed you got there first." (61) | 9:30 (95%) | fGcgWaswMns 7:52 | The real danger ran the other way | Strike-list callback. |
| L8 payoff + bookend | Frame 1 mirrored, empty crane, a bag starts the trip (62) | 9:41-9:55 (97-99%) | fGcgWaswMns 9:29-9:44; mzeN0BXR4e0 16:16-17:40 | Return to frame 1, one question open | Reprises "nobody knows". |
| L9 close (97-100%) | No spoken CTA; board held 5 s, WHERE WOULD YOU HAVE QUIT? | 9:54.6-9:59.6 | nAWpLtG-kNs 16:01-16:10 | Finished board as comment bait | PLAYBOOK §6. |

**Loops.** Master loop: opens 0:23, closed by the board at 8:46. Teasers: squid eye (2:05, now turned on YOU), whale breath (3:36), last fish (6:57-7:05), the unknown "?" (8:59). Plants and payoffs (10 pairs): "its dinner" -> squid -> scars; "nobody knows" -> bookend; STRATEGY: KEEP MOVING -> avalanche -> option 1; "chemistry of being alive starts to jam" (39) -> DEATH 3 (43) -> option 3 -> landing (53); cheat 3's borrowed proteins (44) -> the needle stops (53); the sperm whale's depth (9) -> option 2; the beaked whale's breath (22) -> option 3; rule 3 -> the bag; amphipod "remember that" -> "that grey speck? Ours."; fingertip boxer -> piano -> cow -> car.

**Originality notes.** We do not follow mzeN0BXR4e0's hadal order (no Hades etymology; Everest before the amphipods with the opposite geometry; the snailfish's molecule marks the depth where YOUR death happens instead of being a wonder; the twist leads with the 1998 bag). The options loop borrows only OCEANS' structure (plan as a question, killed by an earlier fact); our three plans and kills are our own rungs. The squid-scar line is reworded around stranded whales. The bioluminescence share is on screen only.

## Pacing (this package, revision 2)

| Metric | Ours | PLAYBOOK target |
|---|---|---|
| Runtime | 9:59.6 (599.6 s, estimated) | 8-10 min |
| Words / wpm | 1,571 / ~166 speech-only (157 over runtime) | 1,500-1,700 / 160-170 |
| Hook | 17 words, 5.6 s; drop at 0:04.7 | <= 25 words / 10 s |
| First rung / format reveal | 0:28.5 / 0:40.5 | <= 45 s |
| "You" | every rung from 6:29 to 8:46 is a test on YOU (flip, death, cheat, options, landing); twist lines 57, 59 and 61 address YOU | >= 25% / >= 3% |
| Numbers | ~4.8 spoken number phrases/min; secondary stats on screen only | 3-5/min |
| Verbal re-hooks | median ~9 s; twist zone 8:54-9:41 has a re-hook every ~3-10 s (reveal, punch, reveal, punch) | ~30 s, denser at the end |
| New rung | every 20-96 s | 40-70 s |
| Jokes (punch lines only) | 0:38 "don't ask how", 1:43 "it's after squid, not you", 2:26 "Dinner fights back", 2:49 "a maybe doesn't earn a cheat", 3:12 "this is where I'd have quit", 4:37 "the event of the year / Being watched? Also yes", 4:56 "Please don't try to play it", 5:11 "Alive? Mostly.", 6:03 "I did warn you about the wall", 6:36 "wet tissue paper with eyes", 7:26 "slightly shrimpier", 7:59 "Great plan, if you were a whale", 8:19 "Lonely? Extremely". Longest gap 4:56 -> 5:11 -> 6:03 (52 s) | every 60-90 s; our internal target <= 55 s |
| Long-loop closes | 21%, 36%, 70%, 88%, 90% | ~35/50/70/98% |

(Descriptions such as "cartoon elephant ears" and the removed "made of trillions" are no longer counted as jokes.)

## Facts (every number has a source; check the CHECK rows before the voice is mixed)

| Claim (paraphrased) | Source |
|---|---|
| ~1 atm per ~10 m of seawater; pressure doubles at 10 m | NOAA Ocean Service, "How does pressure change with ocean depth?" |
| Red light absorbed first, blue deepest; twilight 200-1,000 m; midnight 1,000-4,000 m; abyss 4,000-6,000 m; hadal 6,000-11,000 m | NOAA Ocean Exploration "Light in the ocean"; NOAA ocean zones; Jamieson 2015, The Hadal Zone |
| ~3 in 4 midwater animals are bioluminescent (on screen) | Martini & Haddock 2017, Scientific Reports 7:45750 |
| 100 / 500 / 700 / ~1,086 bar ~ 102 / 510 / 714 / ~1,107 kgf per cm² (boxer, grand piano, dairy cow, small car) | Unit conversion (1 bar = 1.02 kgf/cm²) |
| Deepest pressure a human has experienced: 701 m equivalent, Comex HYDRA X chamber, 1992 | Comex records; Undersea & Hyperbaric Medicine literature |
| HPNS: tremor, dizziness, nausea, microsleep; no human data near 1,400 m | Bennett & Rostain, in Bennett and Elliott's Physiology and Medicine of Diving |
| Sperm whale clicks are the loudest known animal sound; hunt ~400-1,200 m | Møhl et al. 2003, JASA 114:1143; NOAA Fisheries |
| Giant squid up to ~12-13 m; eyes up to ~27 cm; serrated sucker rings | Nilsson et al. 2012, Current Biology 22:683; Smithsonian Ocean |
| Sperm whales carry circular sucker scars | Clarke 1980; Smithsonian Ocean |
| Deep water ~1.5-4 °C; surface ~28-29 °C | World Ocean Atlas; NOAA |
| 0-4 °C water: exhaustion or unconsciousness in < 15-30 min, expected survival ~15-90 min ("most people black out within half an hour") | National Center for Cold Water Safety, survival estimates (coldwatersafety.org/survival-estimates); NY State Parks, Cold Water Immersion; Golden & Tipton, Essentials of Sea Survival |
| Cuvier's beaked whale: deepest dive 2,992 m; longest 222 min | Schorr et al. 2014, PLOS ONE 9:e92633; Quick et al. 2020, J. Exp. Biol. 223:jeb222109 |
| Average ocean depth ~3,682 m | Charette & Smith 2010, Oceanography 23:112 |
| Carbonate shells start dissolving at the Pacific lysocline (shallower than the ~4,200-4,500 m CCD); on-screen tag at 4 km reads SHELLS START DISSOLVING HERE | Open University, Ocean Chemistry; NOAA |
| Grenadiers at baited landers within ~30 min; bait to bones within ~1 day | Jamieson et al. baited-lander studies; Priede & Bagley 2000 |
| Trenches: a sliver of seafloor, ~45% of the ocean's depth range | Jamieson 2015; Jamieson et al. 2010, TREE 25:190 |
| Trenches form at subduction zones (Pacific plate under the Philippine Sea plate) | USGS |
| 2011 Tohoku earthquake sent sediment flows to the Japan Trench floor | McHugh et al. 2016, Geology 44:391; Ikehara et al. 2016, EPSL 445:48 |
| Dumbo octopus (Grimpoteuthis) filmed at 6,957 m (Java Trench, filmed 2019, Five Deeps Expedition; paper 2020); ~35 cm total length (mantle 110 mm), the 5,760 m one ~43 cm ("as long as your forearm and hand") | Jamieson & Vecchione 2020, Marine Biology 167:82; Guinness World Records "deepest octopus" |
| Pressure distorts proteins and stiffens membranes | Somero 1992, Annual Review of Physiology 54:557 |
| TMAO rises with depth; fish iso-osmotic at ~8,200 m (a prediction, hedged) | Yancey et al. 2014, PNAS 111:4461 |
| Deepest fish filmed: juvenile snailfish at 8,336 m, Izu-Ogasawara Trench, 2022 | Minderoo-UWA Deep Sea Research Centre, April 2023 |
| Everest 8,848.86 m; Challenger Deep ~10,935 m | Nepal/China 2020 survey; Greenaway et al. 2021 |
| Deepest rescue: Pisces III, 480 m, off Cork, 1973 (option 2) | Guinness World Records |
| Hirondellea gigas ~3-5 cm at Challenger Deep; gut enzymes turn plant debris into sugar | Kobayashi et al. 2012, PLOS ONE 7:e42727; Live Science 2019; National Geographic 2012 |
| Cheat 3: hadal animals carry pressure-adapted proteins that keep their shape under the squeeze (the "crustacean trick"; framed as a borrowed cheat, not a claim that it would work in a human) | Somero 1992, Annu. Rev. Physiol. 54:557; Jamieson 2015, The Hadal Zone ch. on adaptations |
| Pressure at Challenger Deep ~1,086 bar vs ~830 bar at 8.3 km: "a third stronger" (+31%) | NOAA ~1 atm / 10 m; unit arithmetic |
| Xenophyophores: single cells up to ~10-20 cm, found to ~10,641 m (Sirena Deep; on screen only in revision 2) | 2011 Scripps / National Geographic dropcam survey of the Sirena Deep (Levin; identification by Gooday): scripps.ucsd.edu/news/scientists-id-giant-amoebas-extreme-deep |
| Challenger Deep visitors: 27 people by July 2022; Fendouzhe had carried 29 people below 10,000 m by 2023 and 32 by 2024, so ~55-60+ now, all in submersibles. The old "fewer than fit on a bus" is no longer safely true, so line 6 now says "fewer people have ever reached the bottom than have been to space" (600+ and rising faster) | RESOLVED: Cornell "Challenging the Deep" deep-dives tally; CAS 2024-03-05; Wuxi gov 2024-03-05 |
| A single-use plastic bag at 10,898 m, Mariana Trench, 1998 (ROV Kaiko); no source says it was a checkout or shopping bag, so the script does not | Chiba et al. 2018, Marine Policy 96:204 (JAMSTEC Deep-sea Debris Database); WHOI; Guinness World Records |
| Every Mariana amphipod examined held microparticles (mean 3.3 per animal, highest of six trenches); the FTIR-tested subsample included synthetic and semi-synthetic fibres (plastic) and natural ramie ("every one they opened had swallowed tiny fibres, and the ones they tested included plastic") | Jamieson et al. 2019, Royal Society Open Science 6:180667 |
| POPs (PCBs) in every sample of every Mariana amphipod species tested; the worst at ~50x crabs from Liaohe-fed paddy fields (on screen only: WORST: 50x PADDY-FIELD CRABS, LIAO RIVER). Nearest factory is at least ~11 km away (the trench floor is ~10.9 km below the surface) | Jamieson et al. 2017, Nature Ecology & Evolution 1:0051 |

## Chapters (YouTube; also in description.md)

Curiosity labels, no death spoilers; no chapter under 30 s. Times are provisional (see `timing_source`) and must be re-checked against the final captions before upload.

| Time | Chapter |
|---|---|
| 0:00 | The drop |
| 0:28 | Your ears go first |
| 1:45 | Where the light is alive |
| 2:51 | The problem nobody mentions |
| 3:46 | Where the ocean should end |
| 5:17 | The walls that move |
| 6:29 | What lives where you can't |
| 7:29 | No cheats left |
| 8:22 | The bottom |
| 8:54 | What got there first |

## Narration with timestamps

**First line:** "You're strapped to a sled above the deepest trench on Earth, and in five seconds it drops."
**First visual:** bright Pacific surface, a tiny boat's crane holding YOU on a yellow sled at the waterline, a 5 s Timer ring that empties on "drops"; then the sled plunges and the DepthMeter slides in.

Each paragraph is one narration chunk (one TTS line). Gaps between paragraphs are 0.32 s; a 0.5 s pause precedes line 53.

**[0:00.1-0:05.7] 01. HOOK (drop on "drops")**  
You're strapped to a sled above the deepest trench on Earth, and in five seconds it drops.

**[0:06.0-0:22.8] 02. HOOK / teasers x4**  
It won't stop for eleven kilometres, and on the way down you'll meet a squid with an eye wider than your face, a whale that holds one breath longer than your whole trip, the last fish on the planet, and, almost at the bottom, something that should never have made it there.

**[0:23.1-0:28.1] 03. MASTER QUESTION (= title)**  
So how many times does the ocean kill you before you reach the bottom? Let's count.

**[0:28.5-0:40.2] 04. RUNG 1 (0-1 km) entry + rule 1**  
Ten metres down, your ears already hurt, because the pressure on you has doubled. Pinch your nose, blow, pop. And yes, you can breathe down here. That's rule one, so don't ask how.

**[0:40.5-0:53.1] 05. Rule 2 + FORMAT REVEAL (ALIVE meter, CHEATS LEFT 3)**  
Rule two: every time the ocean kills you, you get a cheat that brings you back, but you only get three, and when they're gone, so are you. That's what this meter is for. Are you still alive? Right now, yes.

**[0:53.4-1:09.6] 06. Rule 3 (planted for the twist) + sink rate** (estimated: re-measure)  
Rule three: no submarine. Fewer people have ever reached the bottom than have been to space, all of them inside one, so you'll be the first thing of ours to get there without. At this slow walking pace, the trip takes about three hours.

**[1:09.9-1:17.4] 07. RUNG 1 colour loss, TWILIGHT named**  
Then the colours go, red first, then orange, then yellow, until everything is blue. Welcome to the twilight zone.

**[1:17.7-1:28.3] 08. RUNG 1 record (701 m)**  
At seven hundred metres, you pass a quiet record. A diver in a French test chamber was once squeezed to exactly this pressure, and no human has felt more.

**[1:28.7-1:38.7] 09. RUNG 1 creature: sperm whale**  
Then you feel a clicking so loud it buzzes in your chest. A sperm whale is hunting somewhere in the dark, and its clicks are the loudest sound any animal makes.

**[1:39.0-1:44.7] 10. RUNG 1 plant ("its dinner")**  
Relax, it's after squid, not you. Keep that in mind, because you're about to meet its dinner.

**[1:45.0-1:53.3] 11. RUNG 1 threshold 1 km, MIDNIGHT named**  
One kilometre, and you've reached the midnight zone, where the sunlight is gone for good, and from here down, the only light is alive.

**[1:53.6-2:04.6] 12. RUNG 1 number + verdict YES**  
The pressure is now a hundred times what you're used to, like a heavyweight boxer standing on every fingertip of your skin. Alive? Yes. You just can't see a thing.

**[2:04.9-2:17.1] 13. RUNG 2 (1-2 km) creature: giant squid (teaser 1 paid)** (estimated: re-measure)  
Just below the line, something huge drifts up beside you: a giant squid, up to the length of a bus, with an eye wider than your face, and it has turned toward you.

**[2:17.5-2:28.0] 14. RUNG 2 weapon + callback (dinner fights back)**  
Its suckers are ringed with tiny teeth, and dead sperm whales wash up with those rings printed on their skin, like rows of bottle caps. Dinner fights back.

**[2:28.3-2:41.8] 15. RUNG 2 threat: nerves + honest unknown**  
Then your hands start to shake, because at pressures like this nerves misfire: fingers tremble, rooms spin, people nod off mid-sentence. And at twice the record? Nobody knows. Nobody has been there.

**[2:42.1-2:50.8] 16. RUNG 2 verdict "?" (no cheat for a maybe)**  
So your meter can't say yes or no. It says this. And a maybe doesn't earn a cheat, so you keep sinking, shaking, past two kilometres.

**[2:51.1-3:00.8] 17. RUNG 3 (2-3 km) threat: the cold**  
And here's the problem nobody warned you about: the cold. The surface was as warm as a heated pool, and down here it's barely above freezing.

**[3:01.1-3:14.8] 18. RUNG 3 you-scenario + host ruling** (estimated: re-measure)  
In water that cold, most people black out within half an hour, and you've been in it for over half an hour. Near three kilometres, you stop shivering. I'll be honest, this is where I'd have quit.

**[3:15.2-3:18.3] 19. DEATH 1 (33%)**  
Alive? No. First death, fifty minutes in.

**[3:18.6-3:24.1] 20. Cheat 1**  
Cheat number one: a heated suit. You wake up warm, still sinking, and you're not alone.

**[3:24.4-3:36.0] 21. RUNG 3 creature: beaked whale (at your depth)**  
A slim grey whale with a short beak glides past you: a Cuvier's beaked whale, the deepest-diving mammal ever tracked, and one was followed almost exactly to your depth.

**[3:36.3-3:45.4] 22. RUNG 3 comparison (teaser 2 paid)**  
It breathes air, just like you, and with no cheats at all, its longest breath on record lasted longer than your entire fall to the bottom.

**[3:45.7-3:53.3] 23. RUNG 4 (3-4 km) expectation reversal**  
Nearly four kilometres down, you pass the average depth of the ocean, where most of the planet's seafloor would be.

**[3:53.7-4:03.1] 24. RUNG 4 geometry: onto the trench wall**  
But you're over a trench, so the current nudges your sled against its wall, and you slide down it the rest of the way, with seven kilometres to go.

**[4:03.4-4:11.6] 25. RUNG 5 (4-5 km) ABYSS named, shells dissolve**  
Four kilometres: the abyss. The water here is so cold and squeezed that seashells landing this deep slowly dissolve.

**[4:11.9-4:16.0] 26. Turnstile 1 (good news / bad news)**  
Good news: you're not a seashell. Bad news: down here, you're food.

**[4:16.3-4:28.6] 27. RUNG 5 gross-out: bait cam**  
When scientists drop a dead fish on slopes like this, long-tailed fish called grenadiers find it within half an hour, tiny scavengers swarm in, and within a day it can be bones.

**[4:28.9-4:40.0] 28. RUNG 5 threat on you + strategy + verdict**  
And now the grenadiers are circling you. Strategy: keep moving, because if you nap down here, you become the event of the year. Alive? Yes. Being watched? Also yes.

**[4:40.4-4:50.1] 29. "Picture it again" re-immersion (47%)**  
Picture where you are. Look up: the boat and the sunshine are over an hour of climbing above you. Look down: there's more water below you than above you.

**[4:50.4-4:57.9] 30. RUNG 6 (5-6 km) number** (estimated: re-measure)  
Five kilometres. Every fingertip of your skin is now holding up a grand piano. Please don't try to play it.

**[4:58.2-5:10.8] 31. RUNG 6 creature: dumbo octopus** (estimated: re-measure)  
Out of the dark flaps a dumbo octopus, waving two fins like cartoon elephant ears. It's about as long as your forearm and hand, and it lives deeper than any other octopus we know.

**[5:11.1-5:16.6] 32. Verdict MOSTLY + turnstile 2 (52%)**  
Alive? Mostly. But that wall you're sliding along is about to become the problem.

**[5:16.9-5:26.7] 33. RUNG 7 (6-7 km) HADAL named**  
Six kilometres. You've crossed into the hadal zone, the trenches, which cover a sliver of the seafloor but span almost half of the ocean's full depth.

**[5:27.1-5:35.7] 34. RUNG 7 mechanism**  
Trenches form where one plate of Earth's crust dives under another, so they shake, and their walls collapse in avalanches of mud.

**[5:36.0-5:49.6] 35. RUNG 7 dated aside + strategy punished**  
After the great Japan earthquake of twenty eleven, mud slid down the Japan Trench all the way to its floor. And your strategy was to keep moving along the wall, which is exactly where avalanches run.

**[5:49.9-5:56.4] 36. DEATH 2 (58%, sawtooth crash)**  
The slope above you shudders, and a cloud of mud rolls over your sled. Alive? No. Second death.

**[5:56.7-6:05.3] 37. Cheat 2 + host ruling**  
Cheat number two: the mud lets you go. You shake yourself off, still sinking, with a single cheat left. I did warn you about the wall.

**[6:05.6-6:14.2] 38. RUNG 8 (7-8 km) number**  
Seven kilometres, and seven hundred times surface pressure, so every fingertip of your skin now has a dairy cow standing on it.

**[6:14.6-6:28.9] 39. RUNG 8 threat: molecules, verdict BARELY**  
Now the pressure goes after your molecules. Proteins, the tiny machines your cells run on, get squashed out of shape, your cell membranes stiffen, and the chemistry of being alive starts to jam. Alive? Barely.

**[6:29.2-6:41.8] 40. RUNG 9 (8-9 km) SPOKEN FLIP (65%) + creature: snailfish** (estimated: re-measure)  
Eight kilometres, and the question changes: not what kills you, but what can live where you can't. A snailfish, pink and see-through, like wet tissue paper with eyes, swims right up to your face.

**[6:42.1-6:57.2] 41. RUNG 9 mechanism + its ceiling**  
Its body is packed with a molecule called TMAO that holds its proteins in shape. But the deeper a fish lives, the more it needs, and a little past eight kilometres, it would need so much that water would flood its body.

**[6:57.5-7:05.7] 42. Teaser 3 paid: the last fish** (estimated: re-measure)  
The deepest fish ever filmed was a young snailfish just past that line. You just met the last fish on the planet.

**[7:06.0-7:16.8] 43. DEATH 3: the planted squeeze wins where the fish's TMAO runs out** (estimated: re-measure)  
It turns back. You don't. The squeeze that was jamming your proteins keeps climbing, and right where even the fish's TMAO runs out, it wins. Alive? No. Third death.

**[7:17.2-7:29.4] 44. Cheat 3 (last), trick named + joke** (estimated: re-measure)  
Cheat number three, your last: you borrow the trick of the tiny crustaceans down here, proteins built to hold their shape under the squeeze. You wake up slightly shrimpier, with no cheats left.

**[7:29.7-7:32.5] 45. STAKES RESET (end game starts)** (estimated: re-measure)  
Die again, and the trip is over.

**[7:32.8-7:39.6] 46. Biggest landmark: one Everest down**  
By now, you've sunk the full height of Mount Everest, and there are still two kilometres of water underneath you.

**[7:39.9-7:48.1] 47. OPTIONS 1/3: float up (killed by DEATH 2's wall)** (estimated: re-measure)  
Can you save yourself? Drop the weights and float up? That's three more hours back along the wall that buried you once.

**[7:48.4-7:55.9] 48. OPTIONS 2/3: wait for rescue (killed by the sperm whale's depth)** (estimated: re-measure)  
Wait for rescue? The deepest rescue in history happened shallower than where you heard that sperm whale. Nobody is coming.

**[7:56.3-8:04.5] 49. OPTIONS 3/3: hold your breath (killed by the squeeze) + joke** (estimated: re-measure)  
Hold your breath like the beaked whale? Great plan, if you were a whale. Breath was never the problem. The squeeze is.

**[8:04.8-8:17.7] 50. RUNG 10 (9-10 km) creature + plant** (estimated: re-measure)  
Nine kilometres. A tiny amphipod, about as long as the top joint of your thumb, chews on a sunken branch. Its gut turns wood into sugar, so whatever sinks ends up inside it. Remember that.

**[8:18.0-8:21.5] 51. Verdict YES, 0 cheats**  
Alive? Yes. Cheats left? None. Lonely? Extremely.

**[8:21.8-8:32.6] 52. RUNG 11 (10-10.9 km) + arrival: Challenger Deep, three hours** (estimated: re-measure)  
Ten kilometres, and then the sled thumps into soft mud. This is the bottom, Challenger Deep, the lowest point in the ocean, three hours after you left the boat.

**[8:32.9-8:45.8] 53. ZERO-CHEAT TEST: the squeeze peaks; the borrowed trick holds** (estimated: re-measure)  
Every fingertip now carries more than a tonne, about a small car, and the squeeze that killed you is a third stronger. The needle slides toward no, and stops: the crustacean trick holds. Alive? Yes.

**[8:46.2-8:53.8] 54. Finished board + peak declared (88%)**  
Final reading. Deaths: three. Cheats left: none. You beat the ocean, and honestly, it doesn't get any better than this.

**[8:54.1-8:58.6] 55. TWIST (89%): rule 3 turned around**  
[pause: 0.5] Except you weren't the first thing of ours to get here without a submarine.

**[8:58.9-9:07.1] 56. Teaser 4 paid: the bag (reveal)** (estimated: re-measure)  
In nineteen ninety-eight, a robot sub filmed it on the floor of this trench, almost at the bottom: a single-use plastic bag.

**[9:07.4-9:10.5] 57. Punch: rule 3 broken** (estimated: re-measure)  
It beat you here. No cheats. No help.

**[9:10.8-9:20.5] 58. Callback to the plant: fibres (reveal)** (estimated: re-measure)  
And the amphipod you met, the one that eats whatever sinks? Every one they opened had swallowed tiny fibres, and the ones they tested included plastic.

**[9:20.9-9:23.7] 59. Punch: the speck pays** (estimated: re-measure)  
That grey speck in its gut? Ours.

**[9:24.0-9:29.7] 60. Escalation: PCBs (comparison on screen only)** (estimated: re-measure)  
They also carried PCBs, industrial poisons banned decades ago, eleven kilometres from the nearest factory.

**[9:30.0-9:40.8] 61. Villain swap** (estimated: re-measure)  
The cold, the mud, the fish's ceiling: not one of the things that killed you got there first. The newest arrival at the bottom of the world is ours.

**[9:41.1-9:54.6] 62. BOOKEND (mirror of frame 1) + left-open ending**  
Picture the start again: calm water, sunshine, the boat. Your sled took three hours. Whatever slips into that water today starts the same trip, and nobody knows how long it takes. It just keeps arriving.

## Narration (pipeline block)

Same text as above, in the `pipeline.audio.make` block format (music and pause markers).

```narration
[music: deep_ocean] You're strapped to a sled above the deepest trench on Earth, and in five seconds it drops.

It won't stop for eleven kilometres, and on the way down you'll meet a squid with an eye wider than your face, a whale that holds one breath longer than your whole trip, the last fish on the planet, and, almost at the bottom, something that should never have made it there.

So how many times does the ocean kill you before you reach the bottom? Let's count.

Ten metres down, your ears already hurt, because the pressure on you has doubled. Pinch your nose, blow, pop. And yes, you can breathe down here. That's rule one, so don't ask how.

Rule two: every time the ocean kills you, you get a cheat that brings you back, but you only get three, and when they're gone, so are you. That's what this meter is for. Are you still alive? Right now, yes.

Rule three: no submarine. Fewer people have ever reached the bottom than have been to space, all of them inside one, so you'll be the first thing of ours to get there without. At this slow walking pace, the trip takes about three hours.

Then the colours go, red first, then orange, then yellow, until everything is blue. Welcome to the twilight zone.

At seven hundred metres, you pass a quiet record. A diver in a French test chamber was once squeezed to exactly this pressure, and no human has felt more.

Then you feel a clicking so loud it buzzes in your chest. A sperm whale is hunting somewhere in the dark, and its clicks are the loudest sound any animal makes.

Relax, it's after squid, not you. Keep that in mind, because you're about to meet its dinner.

One kilometre, and you've reached the midnight zone, where the sunlight is gone for good, and from here down, the only light is alive.

The pressure is now a hundred times what you're used to, like a heavyweight boxer standing on every fingertip of your skin. Alive? Yes. You just can't see a thing.

Just below the line, something huge drifts up beside you: a giant squid, up to the length of a bus, with an eye wider than your face, and it has turned toward you.

Its suckers are ringed with tiny teeth, and dead sperm whales wash up with those rings printed on their skin, like rows of bottle caps. Dinner fights back.

Then your hands start to shake, because at pressures like this nerves misfire: fingers tremble, rooms spin, people nod off mid-sentence. And at twice the record? Nobody knows. Nobody has been there.

So your meter can't say yes or no. It says this. And a maybe doesn't earn a cheat, so you keep sinking, shaking, past two kilometres.

And here's the problem nobody warned you about: the cold. The surface was as warm as a heated pool, and down here it's barely above freezing.

In water that cold, most people black out within half an hour, and you've been in it for over half an hour. Near three kilometres, you stop shivering. I'll be honest, this is where I'd have quit.

Alive? No. First death, fifty minutes in.

Cheat number one: a heated suit. You wake up warm, still sinking, and you're not alone.

A slim grey whale with a short beak glides past you: a Cuvier's beaked whale, the deepest-diving mammal ever tracked, and one was followed almost exactly to your depth.

It breathes air, just like you, and with no cheats at all, its longest breath on record lasted longer than your entire fall to the bottom.

Nearly four kilometres down, you pass the average depth of the ocean, where most of the planet's seafloor would be.

But you're over a trench, so the current nudges your sled against its wall, and you slide down it the rest of the way, with seven kilometres to go.

Four kilometres: the abyss. The water here is so cold and squeezed that seashells landing this deep slowly dissolve.

Good news: you're not a seashell. Bad news: down here, you're food.

When scientists drop a dead fish on slopes like this, long-tailed fish called grenadiers find it within half an hour, tiny scavengers swarm in, and within a day it can be bones.

And now the grenadiers are circling you. Strategy: keep moving, because if you nap down here, you become the event of the year. Alive? Yes. Being watched? Also yes.

Picture where you are. Look up: the boat and the sunshine are over an hour of climbing above you. Look down: there's more water below you than above you.

Five kilometres. Every fingertip of your skin is now holding up a grand piano. Please don't try to play it.

Out of the dark flaps a dumbo octopus, waving two fins like cartoon elephant ears. It's about as long as your forearm and hand, and it lives deeper than any other octopus we know.

Alive? Mostly. But that wall you're sliding along is about to become the problem.

Six kilometres. You've crossed into the hadal zone, the trenches, which cover a sliver of the seafloor but span almost half of the ocean's full depth.

Trenches form where one plate of Earth's crust dives under another, so they shake, and their walls collapse in avalanches of mud.

After the great Japan earthquake of twenty eleven, mud slid down the Japan Trench all the way to its floor. And your strategy was to keep moving along the wall, which is exactly where avalanches run.

The slope above you shudders, and a cloud of mud rolls over your sled. Alive? No. Second death.

Cheat number two: the mud lets you go. You shake yourself off, still sinking, with a single cheat left. I did warn you about the wall.

Seven kilometres, and seven hundred times surface pressure, so every fingertip of your skin now has a dairy cow standing on it.

Now the pressure goes after your molecules. Proteins, the tiny machines your cells run on, get squashed out of shape, your cell membranes stiffen, and the chemistry of being alive starts to jam. Alive? Barely.

Eight kilometres, and the question changes: not what kills you, but what can live where you can't. A snailfish, pink and see-through, like wet tissue paper with eyes, swims right up to your face.

Its body is packed with a molecule called TMAO that holds its proteins in shape. But the deeper a fish lives, the more it needs, and a little past eight kilometres, it would need so much that water would flood its body.

The deepest fish ever filmed was a young snailfish just past that line. You just met the last fish on the planet.

It turns back. You don't. The squeeze that was jamming your proteins keeps climbing, and right where even the fish's TMAO runs out, it wins. Alive? No. Third death.

Cheat number three, your last: you borrow the trick of the tiny crustaceans down here, proteins built to hold their shape under the squeeze. You wake up slightly shrimpier, with no cheats left.

Die again, and the trip is over.

By now, you've sunk the full height of Mount Everest, and there are still two kilometres of water underneath you.

Can you save yourself? Drop the weights and float up? That's three more hours back along the wall that buried you once.

Wait for rescue? The deepest rescue in history happened shallower than where you heard that sperm whale. Nobody is coming.

Hold your breath like the beaked whale? Great plan, if you were a whale. Breath was never the problem. The squeeze is.

Nine kilometres. A tiny amphipod, about as long as the top joint of your thumb, chews on a sunken branch. Its gut turns wood into sugar, so whatever sinks ends up inside it. Remember that.

Alive? Yes. Cheats left? None. Lonely? Extremely.

Ten kilometres, and then the sled thumps into soft mud. This is the bottom, Challenger Deep, the lowest point in the ocean, three hours after you left the boat.

Every fingertip now carries more than a tonne, about a small car, and the squeeze that killed you is a third stronger. The needle slides toward no, and stops: the crustacean trick holds. Alive? Yes.

Final reading. Deaths: three. Cheats left: none. You beat the ocean, and honestly, it doesn't get any better than this.

[pause: 0.5] Except you weren't the first thing of ours to get here without a submarine.

In nineteen ninety-eight, a robot sub filmed it on the floor of this trench, almost at the bottom: a single-use plastic bag.

It beat you here. No cheats. No help.

And the amphipod you met, the one that eats whatever sinks? Every one they opened had swallowed tiny fibres, and the ones they tested included plastic.

That grey speck in its gut? Ours.

They also carried PCBs, industrial poisons banned decades ago, eleven kilometres from the nearest factory.

The cold, the mud, the fish's ceiling: not one of the things that killed you got there first. The newest arrival at the bottom of the world is ours.

Picture the start again: calm water, sunshine, the boat. Your sled took three hours. Whatever slips into that water today starts the same trip, and nobody knows how long it takes. It just keeps arriving.
```

## Originality gate

`python3 scripts/originality_check.py backlog/longform/sinking-to-the-bottom/script.md research/corpus research/library/transcripts` -> **PASS** (exit 0), run 2026-11-01 13:08 UTC on revision 2 (all review rewrites in). Rerun after any wording change made at the build gate.
