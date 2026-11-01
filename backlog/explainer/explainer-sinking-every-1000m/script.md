---
id: explainer-sinking-every-1000m
niche: explainer
title: How Many Times Would The Ocean Kill You On The Way To The Bottom?
alt_titles: What You'd Meet Sinking To The Bottom Of The Ocean | Every 1,000 Metres Down, The Ocean Tries Something New (full ranked list in titles.md)
format: 16:9 long-form
voice: am_michael
speed: 1.0  # pinned. Measured on the Spark (Kokoro am_michael, CPU): 0.86 -> 148 wpm, 0.96 -> 162 wpm, 1.0 -> 166 wpm (durations.json)
paragraph_pause: 0.2  # ~0.32 s between paragraphs after Kokoro tail trims
target_runtime_s: 582  # 9:42 measured = 9:36 of speech and gaps + 6 s held final board; brief range 8-10 min
words: 1542
wpm_measured: 166  # speech only (557.1 s); 159 over the full speech span incl. gaps. PLAYBOOK long-form target 160-170
hook_words: 17  # PLAYBOOK long-form short hook <=25 words / ~10 s; the drop happens on the word "drops" at 0:04.7
first_rung_s: 28.4  # "Ten metres down" (PLAYBOOK <=45 s; corpus median 46 s)
format_reveal_s: 40.4  # DepthMeter on screen from the drop (0:05), ALIVE meter + CHEATS LEFT from 0:40
reset_interval_s: ~4-10 (new depth, threat, creature, stamp or tag per shot); verbal re-hook gap max ~25 s (see Pacing)
music: deep_ocean (ducked under VO; drops out for the three death stamps and the twist turn)
template: pipeline/templates/explainer.md (long-form, ladder variant)
references:
  - id: nAWpLtG-kNs
    url: https://www.youtube.com/watch?v=nAWpLtG-kNs
    views: 12209257
    outlier_score: 113.57
    why_chosen: The engine. A 'how long would YOU last' ladder with challenge rules that make verdicts comparable, a teaser contract paid in order, a visible verdict board, a sawtooth verdict curve (first drop, crash at 55-60%, peak declared near 90%), host rulings, a viewer strategy that gets punished, and a final twist that turns on an opening rule. Our death count, cheats and ALIVE meter map onto its tier board.
  - id: mzeN0BXR4e0
    url: https://www.youtube.com/watch?v=mzeN0BXR4e0
    views: 17219766
    outlier_score: 12.86
    why_chosen: Same premise family (a descent where each zone is more hostile and its life stranger). We borrow the zone-entry ritual (each chapter names its zone and depth), first-rung-longest pacing, a dated non-animal aside, the gross-out near 44%, the 'and yet' reversal, an Everest scale image near 72% and the open-loop ending. We deliberately break its hadal fact order (see Originality notes).
  - id: fmZfphacPPQ
    url: https://www.youtube.com/watch?v=fmZfphacPPQ
    views: 14711279
    outlier_score: 1.84
    why_chosen: The depth-meter ladder in its purest form - 2P conditional open, a mild relatable first symptom (ears), a new number every rung with a silent landmark beside it, and a planted word that returns as the cause of the end. Best match for code-only visuals.
  - id: fGcgWaswMns
    url: https://www.youtube.com/watch?v=fGcgWaswMns
    views: 2307237
    outlier_score: 14.65
    why_chosen: Devices only (same voice/style family we copy). The 'picture it again' re-immersion near 47%, everyday comparisons for every number (a whale's breath vs yours), the villain swap with numbers, and the bookend back to the opening image.
evidence: Mr. Science "Why Deep Sea Creatures Get Creepier the Deeper You Go" 17.2M (12.9x); Fossil "How Long You'd Last in Every Prehistoric Era" 12.2M (113.6x); Spinosnack and BeyondTheBlue clones of both title formulas (PLAYBOOK §7)
sibling_short: explainer-short-mariana-pressure (body-only Short). Shares no lines with this script by design (R3: cut-downs flop).
---

# How Many Times Would The Ocean Kill You On The Way To The Bottom? (long-form, 16:9)

**Premise.** You ride a sled from the surface of the Mariana Trench to the bottom of Challenger Deep at a slow walking pace (1 m/s, about three hours). The master question, asked aloud at 0:23 and printed in the title, is how many times the ocean kills you before you reach the bottom. Three rules make every verdict comparable. One: you can breathe. Two: every death costs one cheat, you get three, and when they run out the trip is over. Three: no submarine, so you will be the first thing of ours to reach the bottom without one. A depth meter and an ALIVE? meter track you the whole way. The ocean kills you three times (cold at 3 km, an avalanche at 6 km, the fish chemistry ceiling at 8.3 km), so the last 2.6 km run on zero cheats and the landing is a real test. The twist turns rule three around: a plastic bag got there before you, with no cheats and no help, and the trench amphipods are full of man-made fibres and PCBs.

**Geometry (fixed).** The sled falls through open water above the trench until 3.7 km. At the average-depth beat the current pushes it against the trench's west wall, and it slides down that wall the rest of the way (a `WALL` layer in every later descent shot). From then on every encounter with the seafloor (bait cams and grenadiers, the avalanche, xenophyophores) happens on the wall, so nothing is "beside you" while you are still kilometres above the floor.

**Verdict curve (one row per 1 km band, exactly as the final board shows it).**

| band (km) | 0-1 | 1-2 | 2-3 | 3-4 | 4-5 | 5-6 | 6-7 | 7-8 | 8-9 | 9-10 | 10-bottom |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ALIVE? | YES | ? | DEATH 1 (cold, 3,000 m) | YES | YES | MOSTLY | DEATH 2 (avalanche, ~6,150 m) | BARELY | DEATH 3 (fish ceiling, ~8,340 m) | YES | YES, with 0 cheats |
| cheats left at band end | 3 | 3 (a maybe earns none) | 2 | 2 | 2 | 2 | 1 | 1 | 0 | 0 | 0 |

Rule two is honoured at every stamp: each NO is followed at once by a cheat, the "?" explicitly earns nothing, and BARELY / MOSTLY need none. The curve reads YES, ?, NO, YES, YES, MOSTLY, NO, BARELY, NO, YES, YES: a sawtooth with the crash at 58% and the peak declared at 86%.

**Variant:** ladder/countdown (PLAYBOOK 1a). Climax at the landing with zero cheats (84-87%), peak declared at 86%, twist from 88%, bookend 97%, no spoken CTA.

## Kit work this episode needs (producibility)

The 99-shot / ~55-drawing version is cut to **88 shots (median 6.7 s), 7 kit additions and 30 static one-off SVG drawings (reused across 122 layer placements)**, all written out in `gen_storyboard.py`. Inline SVG never animates internally (SvgMarkup is static), so every inline asset is a rigid object that moves as a whole layer (sled, boat, bag, tiles, chamber, shells, piano, cow, Everest, column, plates, branch, gut x-ray, fibres, lumps, protein ribbon, membrane). Anything that swims, flaps or crawls in two or more shots is a kit figure with idle motion.

| # | Kit addition | Where it lives | Props | Used in |
|---|---|---|---|---|
| 1 | `explainer/AliveMeter` (new UI component) | `ui.tsx` | `state` (string or step track of YES / MOSTLY / ? / BARELY / NO, colours green / lime / yellow / orange / red), `stamp` [{at, text, color}] (slam + 2 s hold), `spin` [{at, duration}] (needle spins before landing), `size`, `label` ("ALIVE?") | HUD in every descent shot; big centre version in s07, s18, s26, s32, s55, s59, s64, s74 |
| 2 | `DepthMeter` `markers` [{depth, label, color}] | `ocean.tsx` | flags drawn on the ruler when inside the window | HUD: 701 m human record, 2,992 m beaked whale, 3,700 m average seafloor, 6,957 m octopus, ~8,200 m fish limit, 8,849 m one Everest, 10,935 m bottom |
| 3 | `explainer/Snailfish` | `marine.tsx` | `pxPerM`, `align`, `silhouette`, `juvenile` (smaller, rounder), `xray` (dotted soft spine) | t3, s60, s61, s63, s64 |
| 4 | `explainer/Amphipod` | `marine.tsx` | `pxPerM`, `color` (pale for scavengers, amber for Hirondellea), `xray` (outline + gut window) | s65 (inset), s68, s69, s78 |
| 5 | `explainer/DumboOctopus` | `marine.tsx` | `pxPerM`, ear-fin flap idle, short webbed arms | s48, s49 |
| 6 | `explainer/BeakedWhale` | `marine.tsx` (derive from SpermWhale/Orca code) | `pxPerM`, `silhouette`, scar lines | t2, s33, s34 |
| 7 | `explainer/DeepFish` (grenadier) | `marine.tsx` | `pxPerM`, `dead` (belly-up, idle off), long tapering rat-tail | s42, s43, s44 |
| opt | `ColossalSquid` `variant: "giant"` | `marine.tsx` | longer feeding tentacles, no hooks, slimmer mantle (the giant squid); until built, `hooks:false` reads fine | t1, s15, s20, s22 |

Reused as is: Ocean, DepthMeter, You (poses stand/panic/point/shrug/run/wave, `color` for the suit and the cold, rotate/scaleY keyframes for limp and squash, jitter idle for shaking; no face directions anywhere), SpermWhale, ColossalSquid, Bus, Car, Stat (numbers only), Tag, Headline, Options (rules, colours struck, strategy struck, final board, villain list), SpeedBars (bars only grow, so the TMAO ceiling is the last row in red), ScaleBar, Timer (5 s ring, counts down), Map (Japan Trench and Mariana pins).

Other producibility fixes: Stat is only used with numeric values (non-numbers are Tags/Headlines); HeightChart is not used; the 5 s timer counts down; there is one global depth track (anchored on the spoken depths, linear in between) sliced into every scene's DepthMeter, Ocean darkness and HUD, so the numbers never jump at a cut; shots are timed to Kokoro word timestamps (`durations.json`, measured at speed 1.0), not to a wpm guess; the shortest scene is 2.0 s; every scene over 9 s has 3+ word-anchored internal beats.

## Beat alignment

All reference timestamps were re-checked against `research/corpus/explainer/<id>.md` on 2026-11-01. Our timestamps are measured (Kokoro speed 1.0).

| Our beat | Our time (%) | Reference id + timestamp | Device borrowed | How we adapt it |
|---|---|---|---|---|
| Hook: strapped to the sled, drop on "drops" | 0:00-0:05.7 (0-1%) | fmZfphacPPQ 0:00-0:03; nAWpLtG-kNs 0:00 | 2P conditional with the experiment already starting; 2P premise in one sentence | A 5 s ring empties exactly on the word "drops", so the hook's promise is kept to the second (old version dropped at 0:53). |
| Teasers x4, most mysterious last | 0:06-0:23 (1-4%) | nAWpLtG-kNs 0:10-0:19 | Teasers as a contract, paid in order, the mysterious one held | Ours are paid at 21%, 36%, 70% and 89% (ERAS pays at 37/63/77/92). The second teaser is now on the path (the whale's breath) instead of off-path vents. |
| Master question aloud | 0:23 (4%) | nAWpLtG-kNs 0:22 | Stakes question asked before the rules | "How many times does the ocean kill you" is the title and is answered by the final board (DEATHS 3). |
| Rules given during the first metres | 0:28-1:08 (5-12%) | nAWpLtG-kNs 0:24 | Challenge rules that make verdicts comparable, one rule planted for the end | The rules are spoken while you sink through the bright shallows, so the first rung (ears) starts at 0:28. Rule 3 ("first thing of ours without a sub") is the one the twist turns around. |
| Format reveal: depth meter + ALIVE meter | 0:05 / 0:40 (1% / 7%) | nAWpLtG-kNs 0:31-0:35 (empty tier list); mzeN0BXR4e0 1:34 (cross-section with depth ruler) | Visible progress device before rung 1 | The DepthMeter enters with the drop; the ALIVE meter and CHEATS LEFT 3 enter on rule two. |
| Rung 1 felt first symptom | 0:28 (5%) | fmZfphacPPQ 0:03-0:07 | A mild, relatable first symptom (ear/sinus squeeze) | "Pinch your nose, blow, pop" is the felt first rung. |
| Rung 1 is the longest unit (0-1 km) | 0:28-2:03 (5-21%) | mzeN0BXR4e0 1:18-6:06 (format-teaching chapter, ~27%) | First unit longest, teaches the per-rung formula | Our formula: depth -> threat -> number with a body comparison -> creature -> ALIVE stamp. Rung 1 runs 95 s; later rungs 20-75 s. The 701 m record now sits in rung 1 at 700 m, so the meter never rewinds. |
| Zone-entry ritual | 1:12 twilight, 1:43 midnight, 3:56 abyss, 5:07 hadal | mzeN0BXR4e0 1:39, 6:08, 9:12, 12:28 | Each chapter opens by naming the zone and its depth | All four zones are named aloud at their HUD boundaries (200 / 1,000 / 4,000 / 6,000 m). |
| Silent landmarks | 1:16 (330 m), 1:27 (828 m), 7:16 (8,849 m) | fmZfphacPPQ 0:10, 0:27 | SCALE-V: a famous landmark of matching height beside the number, never spoken | On-screen Tags only (Eiffel Tower, Burj Khalifa); Everest is the one we speak. |
| Plant: "you're about to meet its dinner" -> squid -> scars | 1:37 -> 2:03-2:23 (17-25%) | mzeN0BXR4e0 5:59 (bridge line); fGcgWaswMns 2:23 (scar evidence) | Soft cliffhanger bridge; physical proof that prey fights back | Paid 26 s later. The scar line is reworded around dead whales washing up with sucker rings printed on them, not the reference's wording. |
| Fingertip motif x4 | 1:52 boxer, 4:43 piano, 5:56 cow, 8:12 car | fGcgWaswMns 1:02-1:50 (every number given an everyday object); PLAYBOOK 1a #7 | Number + everyday comparison; one recurring graphic per rung | The same 1 cm² skin tile with a heavier load each time: 100 kg, 500 kg, 700 kg, 1.1 t. |
| Honest unknown (HPNS) -> "?" with no cheat | 2:23-2:46 (25-28%) | mzeN0BXR4e0 2:46 (admitted mystery, reprised unsolved at 16:59) | Once-per-video honest admission, left open and reprised at the end | The admission becomes a meter state. "A maybe doesn't earn a cheat" keeps rule two literal. The bookend's "nobody knows" is its reprise. |
| Host rulings (1P) | 3:03, 5:52, 8:28 | nAWpLtG-kNs 3:27 (host reaction), 7:47-8:06 (confession gag) | A host who rules on the verdicts gives the viewer someone to argue with | "This is where I'd have quit", "I did warn you about the wall", "honestly, it doesn't get any better than this". |
| First death (sawtooth drop 1) | 3:08 (32%) | nAWpLtG-kNs 8:34 (first drop down the board) | Sawtooth: the first hard drop breaks the run of good verdicts | Earlier than ERAS's ~53% because cold is the real killer; the cheat keeps the descent going. |
| Whale vs your trip | 3:17-3:38 (34-37%) | fGcgWaswMns 2:42-2:58 (its dive vs your one-minute breath-hold) | you-vs-it comparison on time | Its record breath (222 min) beats your whole fall (182 min); it was tracked "almost exactly to your depth". |
| Expectation reversal: average depth, but you're over a trench | 3:38-3:56 (38-41%) | mzeN0BXR4e0 9:12 (touch the bottom of the abyss + scale stat) | Re-hook by reversing "this is where the ocean ends" | Doubles as the geometry beat: the sled is pushed onto the trench wall. |
| Turnstile 1: good news / bad news | 4:04 (42%) | nAWpLtG-kNs 1:23-1:46 (good news, more good news, then the "but") | Contrast pair that flips relief into threat | "Bad news: down here, you're food" leads straight into the bait cam. |
| Gross-out peak | 4:09-4:33 (43-47%) | mzeN0BXR4e0 7:49 (gross-out at ~44%) | Most shareable fact at 40-45% | A dead fish turning to bones on a bait cam, then the grenadiers circling YOU (2P, no gore). |
| Strategy, then punished | 4:21 -> 5:26-5:40 (45% -> 56-58%) | nAWpLtG-kNs 5:33 (stay in fresh water) -> 5:49 (the predator lives exactly there) | The viewer's own plan is where the next threat lives | "Keep moving along the wall" is exactly where avalanches run; the STRATEGY card returns and is struck. |
| "Picture it again" re-immersion | 4:33 (47%) | fGcgWaswMns 4:43-4:46 | Put the viewer back in the scene at the midpoint | Look up: the boat is over an hour of climbing away. Look down: more water below than above. |
| Turnstile 2: "about to become the problem" | 5:01 (52%) | nAWpLtG-kNs 7:15-7:17 (says the climb is about to break) | A tease that the next part is worse | The MOSTLY stamp is followed by the warning about the wall. |
| Dated aside: Japan 2011 | 5:26-5:40 (56-58%) | mzeN0BXR4e0 5:21-5:39 (WWII sonar history aside) | Break the creature parade with a dated human event | A trench example (sediment that slid down the Japan Trench after the 2011 quake), told in one sentence with a map; it replaces the 1929 Grand Banks slope event. |
| Death 2 (the crash) | 5:40 (58%) | nAWpLtG-kNs 8:38-9:57 (crash to the bottom of the board, 54-62%) | Sawtooth crash at 55-60% | A real death with a cheat, so the middle no longer sags (the old 3:30-6:15 stretch was YES -> YES -> YES -> MOSTLY). |
| "And yet" reversal: the locals don't mind | 6:19 (65%) | mzeN0BXR4e0 6:25 (nothing could survive, and yet...), 13:21 (snailfish thrives) | Hostility peaks, then fragile life appears | Said in one clause before the snailfish arrives. |
| Facts become the weapon: the fish ceiling kills you | 6:29-7:05 (67-73%) | fmZfphacPPQ 0:12 -> 0:25-0:27 (planted "collapse" returns as the cause); PLAYBOOK §4 | A planted mechanism comes back bigger | The TMAO ceiling (~8,200 m) is explained, then you sink through it without the chemistry: DEATH 3. Old version: the cheat expired and you survived anyway. |
| Teaser 3 paid: the last fish | 6:44-6:58 (70-72%) | nAWpLtG-kNs 12:25 (third teaser paid at 77%) | Teaser paid in fame order | Hedged: "no fish has ever been seen deeper, and the chemistry says none can go much further". |
| Zero cheats left: stakes reset | 7:05 (73%) | nAWpLtG-kNs 14:53-14:57 ("finally", last-item pull) | Tell the viewer the end game has started | "Die again, and the trip is over" makes every remaining rung a real test. |
| Biggest landmark: one Everest down | 7:16 (75%) | mzeN0BXR4e0 12:52-13:07 (Everest-in-the-trench scale at ~72%) | Signature scale image near 72-75% | Geometry corrected: you have sunk one Everest-height and 2 km of water is still under you. The visual hangs Everest upside down from the surface, its summit at YOU. |
| No rescue, by callback | 7:23 (76%) | fGcgWaswMns 5:59-7:05 (options killed by callbacks to earlier rungs) | An earlier fact used against you | The deepest rescue ever was shallower than where you heard the sperm whale (480 m on screen only). |
| Plant for the twist | 7:32-7:48 (78-80%) | fmZfphacPPQ 0:12 (planted word, paid twice) | Throwaway detail, paid in the twist | "Whatever sinks from the surface ends up inside it. Remember that." The x-ray shows an unlabelled grey speck. |
| Landing + last near-death on 0 cheats | 8:02-8:23 (83-86%) | nAWpLtG-kNs 14:53-15:47 (the final item is the hardest test) | The climax lives inside the final item | The needle slides toward NO and stops. A real test, so "you beat the ocean" is a win worth undercutting. |
| Finished board + peak declared | 8:23-8:31 (86-87%) | nAWpLtG-kNs 14:45-14:49 (peak declared at 91%), 16:01 (finished board) | Announce the peak, then show the board | Board rows are written out (see Verdict curve). |
| Twist: rule three turned around | 8:31 (88%) | nAWpLtG-kNs 15:41-15:47 (the opening no-tools rule is what the twist turns on) | Opening rule used against the viewer's win | Rule 3 promised you'd be the first thing of ours down there without a sub; the bag was first. |
| Teaser 4 paid: the bag | 8:36-8:49 (89-91%) | nAWpLtG-kNs 14:53-14:55 (last teaser paid at ~92%) | Most mysterious teaser held to last | Said accurately: filmed in 1998 lying on the floor of this trench, almost at the bottom (10,898 m on screen). |
| Fibres + PCBs callback | 8:49-9:12 (91-95%) | mzeN0BXR4e0 14:07-14:19 (plastic fibres in trench amphipods as the human-relevance turn) | Human harm reaches the deepest place | The 17M reference already uses the fibres fact, so we lead with the bag (fresher) and escalate with PCBs (less known). |
| Villain swap | 9:12-9:22 (95-96%) | fGcgWaswMns 7:52 (the real danger ran the other way) | Villain swap after the peak | Three-word callback list struck on screen; "the newest arrival at the bottom of the world is ours". |
| Bookend + left-open ending | 9:22-9:36 (96-99%) | fGcgWaswMns 9:29-9:44 (return to the opening scene); mzeN0BXR4e0 16:16-17:40 (questions left open) | Return to frame 1 with everything learned; end on an image | Frame 1 mirrored with an empty crane; "nobody knows how long it takes" reprises the HPNS unknown. |
| Close: no spoken CTA, board held 6 s | 9:36-9:42 (99-100%) | nAWpLtG-kNs 16:01-16:10 (final board held, no CTA); PLAYBOOK §6 | Finished board as comment bait | On-screen WHERE WOULD YOU HAVE QUIT? only. The spoken line ends on "It just keeps arriving." |

**Loops.** Master loop: how many times does the ocean kill you (opens 0:23, closed by the board at 8:23: three). Teasers: squid eye (paid 2:03-2:12, 21-23%), the whale's breath (3:29, 36%), the last fish (6:44-6:58, 70-72%), "?" (8:36, 89%). Plants and payoffs: "its dinner" -> giant squid -> sucker scars; "nobody knows" (nerves) -> bookend "nobody knows how long it takes"; STRATEGY: KEEP MOVING -> punished by the avalanche; the TMAO ceiling -> DEATH 3; the whale's depth -> "the deepest rescue was shallower than the whale"; rule 3 ("first thing of ours without a sub") -> the bag; amphipod gut "remember that" -> fibres; fingertip boxer -> piano -> cow -> car; frame 1 -> bookend.

**Originality notes.** The old hadal stretch followed mzeN0BXR4e0 12:47-14:19 fact for fact (Hades name, Everest, snailfish protein molecules, amphipods, plastic fibres). Now: no Hades etymology; Everest moves before the amphipods and uses a different geometry (one Everest sunk, summit at you); the snailfish's molecule is the cause of a death, not a wonder; the twist leads with the 1998 bag and escalates with PCBs. The squid-scar line is reworded around dead whales washing ashore with sucker rings printed on them. The bioluminescence share (3 in 4) is on screen only.

## Pacing (measured)

<!-- gen:pacing -->
- Source: Kokoro am_michael speed 1.0 word timings for 58/58 paragraphs (durations.json); gaps 0.32 s; lead-in 0.1 s; board hold 6.0 s.
- Runtime 9:42.0 (582.0 s); speech ends 9:36.0; 1542 words = 161 wpm over the speech span.
- 88 scenes; median scene 6.7 s; scenes over 9 s: s08_rule3 10.7 s, s36_breath 9.4 s, s46_picture 10.0 s, s51_hadal 10.1 s, s60_snailfish 10.1 s, s62_ceiling 9.4 s, s65_cheat3 10.5 s, s67_rescue 9.4 s, s71_xeno 10.1 s, s72_landing 9.6 s, s77_bag 12.8 s, s78_fibres 10.9 s, s79_pcb 12.2 s, s80_swap 10.0 s (each has 3+ timed internal beats).
<!-- /gen:pacing -->

- First rung 0:28 (5%); hook 17 words; drop at 0:04.7; both meters on screen by 0:41.
- Narration stats (research/corpus/explainer/stats.py method, plus a per-phrase number count): 1,542 words, 140 sentences, average 11.0 words (target 10-13; 1-3 word punches kept for verdicts and jokes); "you/your" in 63/140 = 45% of sentences (target >=25%; old version 22%) and 5.7% of words (target >=3%; old 3.4%), 9.2 you-words/min. The lowest minutes are the arrival and twist (27-33%, third person by design); every ladder minute is 36-60%, including the old sag minutes 4-7.
- Spoken numbers: 47 number phrases = 4.9/min; stats.py token count 5.0/min (target 3-5; old version 10/min by phrase, 13/min by token). Depths are spoken once per rung, mostly as kilometres; elapsed time is spoken only at the first death ("fifty minutes in") and the arrival ("three hours"). Secondary stats (2,992 m, 222 min, 6,957 m, 8,336 m, 480 m, 10,898 m, ~45%, 30 trillion, 3 in 4) are on screen only.
- Verbal re-hooks: 0:23 master question, 0:28 new rung, 0:40 rule two, 1:08 colours, 1:16 record, 1:27 clicking, 1:37 plant, 1:43 zone, 2:03 withheld noun, 2:23 symptom + question, 2:37 "it says this", 2:46 "the problem nobody warned you about", 3:08 death, 3:11 "you're not alone", 3:38 reversal, 3:46 "but you're over a trench", 4:04 turnstile 1, 4:21 "now the grenadiers are circling you", 4:33 picture it again, 4:43 new rung, 5:01 turnstile 2, 5:07 zone, 5:26 strategy punished, 5:40 death, 5:56 new rung, 6:04 "now the pressure goes after your molecules", 6:19 reversal, 6:29 "but the deeper...", 6:58 death, 7:05 "die again and the trip is over", 7:16 Everest, 7:23 "nobody is coming", 7:32 "remember that", 7:52 new rung, 8:02 landing, 8:12 last test, 8:31 twist. Longest gap ~25 s (5:56 -> 6:19 is 23 s).
- Jokes / deflations about every 45-70 s: "don't ask how", "you just can't see a thing", "dinner fights back", "a maybe doesn't earn a cheat", "event of the year / being watched", "cartoon elephant ears", "I did warn you about the wall", "lonely? extremely", "made of trillions".

## Facts to verify (paraphrased; check before publishing)

| Claim | Source to check |
|---|---|
| ~1 atm added per ~10 m of seawater; pressure doubles at 10 m | NOAA Ocean Service, "How does pressure change with ocean depth?" |
| Red light absorbed first (~10 m), then orange, yellow, green; blue penetrates deepest; twilight zone 200-1,000 m | NOAA Ocean Exploration, "Light in the ocean"; NOAA ocean zones |
| Sunlight effectively gone by ~1,000 m; midnight zone 1,000-4,000 m; abyss 4,000-6,000 m; hadal 6,000-11,000 m | NOAA Ocean Service ocean zones; Jamieson 2015, The Hadal Zone |
| ~76% of observed midwater animals are bioluminescent (on screen "~3 IN 4"; VO says "most") | Martini & Haddock 2017, Scientific Reports 7:45750 |
| 100 bar ~ 102 kgf/cm²; 500 bar ~ 510; 700 bar ~ 714; Challenger Deep ~1,086 bar ~ 1,107 kgf/cm² (VO: boxer, grand piano ~480 kg, dairy cow ~650-700 kg, small car ~1.1 t) | Unit conversion (1 bar = 1.02 kgf/cm²) |
| Deepest pressure a human has experienced: 701 m equivalent, Théo Mavrostomos, Comex HYDRA X, Toulon, France, 1992 (chamber) | Comex records; Undersea & Hyperbaric Medicine literature |
| HPNS: tremor, dizziness, nausea, microsleep; worsens with depth and compression rate; no human data near 1,400 m | Bennett & Rostain, HPNS, in Bennett and Elliott's Physiology and Medicine of Diving |
| Sperm whale clicks are the loudest known animal sound (~230+ dB re 1 µPa); they hunt ~400-1,200 m | Møhl et al. 2003, JASA 114:1143; NOAA Fisheries |
| Giant squid (Architeuthis): up to ~12-13 m total length; eyes up to ~27 cm, among the largest of any animal; suckers with serrated chitin rings; usual depth ~300-1,000 m (VO places it "just below" 1 km, the deep edge) | Nilsson et al. 2012, Current Biology 22:683; Roper & Boss 1982, Scientific American; Smithsonian Ocean |
| Sperm whales carry circular sucker scars from squid; giant squid are a sperm-whale prey item | Clarke 1980 (sperm whale diet); Smithsonian Ocean |
| First video of a live giant squid in its deep habitat: 2012, off Chichijima, Ogasawara (Kubodera, NHK/Discovery). Not used in VO this version | NHK / National Museum of Nature and Science, Japan |
| Deep water below ~1,000 m in the western Pacific is ~1.5-4 °C; surface ~28-29 °C (VO: heated pool -> barely above freezing) | World Ocean Atlas; NOAA |
| In 0-4 °C water: exhaustion/unconsciousness within ~15-30 min, expected survival ~30-90 min (VO: most black out within an hour; at 1 m/s you are in <4 °C water ~33 min by 3,000 m) | US Coast Guard cold-water survival table |
| Cuvier's beaked whale: deepest recorded dive 2,992 m; longest 222 min (3 h 42 min) > the 182 min fall | Schorr et al. 2014, PLOS ONE 9:e92633; Quick et al. 2020, J. Exp. Biol. 223:jeb222109 |
| Average ocean depth ~3,682 m | Charette & Smith 2010, Oceanography 23:112 |
| Carbonate shells dissolve once they settle below the calcite compensation depth, ~4,200-4,500 m in the Pacific (VO: "seashells landing this deep slowly dissolve") | Open University, Ocean Chemistry; NOAA |
| Abyssal grenadiers arrive at baited landers within ~30 min; amphipod swarms follow; bait reduced to bones within ~1 day | Jamieson et al. baited-lander studies (Deep-Sea Research I); Priede & Bagley 2000 |
| Trenches: a sliver of the seafloor (estimates from ~0.2% to <2%) but ~45% of the ocean's depth range | Jamieson 2015, The Hadal Zone; Jamieson et al. 2010, TREE 25:190 |
| Trenches form where one plate subducts beneath another (Mariana: Pacific plate under the Philippine Sea plate) | USGS |
| 2011 Tohoku earthquake triggered sediment gravity flows down the Japan Trench, with fresh turbidites in the trench axis (~7-8 km) | McHugh et al. 2016, Geology 44:391; Ikehara et al. 2016, EPSL 445:48 |
| Deepest octopus: dumbo octopus (Grimpoteuthis) filmed at 6,957 m, Java Trench, 2020; typical length ~20-30 cm | Jamieson & Vecchione 2020, Marine Biology 167:82 |
| High hydrostatic pressure distorts protein folding/ligand binding and orders (stiffens) cell membranes | Somero 1992, Annual Review of Physiology 54:557 |
| Snailfish: translucent, scaleless, poorly ossified skeleton, high TMAO | Gerringer et al. 2017, Zootaxa 4358:161; Wang et al. 2019, Nat. Ecol. Evol. 3:823 |
| TMAO rises with depth; fish would become iso-osmotic with seawater at ~8,200 m, predicting no fish much deeper (a physiological prediction, hedged in VO) | Yancey et al. 2014, PNAS 111:4461 |
| Deepest fish filmed: juvenile snailfish (Pseudoliparis sp.) at 8,336 m, Izu-Ogasawara Trench, Sept 2022 | Minderoo-UWA Deep Sea Research Centre, April 2023 |
| Everest 8,848.86 m (2020 survey); Challenger Deep ~10,935 m; 10,935 - 8,849 = 2,086 m still below | Nepal/China 2020 survey; Greenaway et al. 2021 |
| Deepest rescue: Pisces III, 480 m, off Cork, Ireland, 1973 (Chapman & Mallinson, ~76 h) | Guinness World Records |
| Hirondellea gigas ~2-3 cm (Challenger Deep specimens just over 3 cm); gut cellulase digests plant debris into glucose | Kobayashi et al. 2012, PLOS ONE 7:e42727 |
| Xenophyophores: single-celled, up to ~10-20 cm, found to ~10,641 m (Sirena Deep, Mariana Trench); human body ~30 trillion cells | Gooday et al. 2017; Scripps 2011 trench expedition; Sender, Fuchs & Milo 2016, PLOS Biology |
| Challenger Deep reached first in 1960 (Trieste); visitors since, all in submersibles, number in the few dozens (VO: fewer than fit on a bus) | Five Deeps / Caladan Oceanic tallies; Fendouzhe dive reports |
| A single-use plastic bag recorded on the seafloor at 10,898 m in the Mariana Trench in 1998 (ROV Kaiko; JAMSTEC Deep-sea Debris Database) | Chiba et al. 2018, Marine Policy 96:204 |
| Man-made microfibres (mostly plastics, some semi-synthetic cellulosics) in 100% of amphipods sampled from the Mariana Trench (small sample) | Jamieson et al. 2019, Royal Society Open Science 6:180667 |
| PCBs in Mariana amphipods ~50x higher than crabs from paddy fields fed by the Liao River, one of China's most polluted rivers | Jamieson et al. 2017, Nature Ecology & Evolution 1:0051 |

## Script

Timestamps are measured: Kokoro am_michael at speed 1.0 word timestamps (`durations.json`), 0.32 s between paragraphs, 0.1 s lead-in, the [pause: 0.5] before the twist. One paragraph = one narration chunk; shots inside a paragraph start on word anchors (see Shot list).

**First line:** "You're strapped to a sled above the deepest trench on Earth, and in five seconds it drops."
**First visual:** bright Pacific surface, a tiny boat's crane holding YOU strapped to a yellow sled at the waterline, a 5-second `Timer` ring that empties exactly on "drops"; then the sled plunges and the DepthMeter slides in.

<!-- gen:scenes -->
### 01. [0:00.1-0:05.7] HOOK (drop on "drops")

VO: You're strapped to a sled above the deepest trench on Earth, and in five seconds it drops.

On screen: Timer ring 5 -> 0 hits zero on "drops"; Tag MARIANA TRENCH, PACIFIC

### 02. [0:06.0-0:22.8] HOOK / teasers x4

VO: It won't stop for eleven kilometres, and on the way down you'll meet a squid with an eye wider than your face, a whale that holds one breath longer than your whole trip, the last fish on the planet, and, almost at the bottom, something that should never have made it there.

On screen: Headline 11 KM DOWN; teaser cards: AN EYE WIDER THAN YOUR FACE / ONE BREATH > YOUR WHOLE TRIP / THE LAST FISH ON THE PLANET / ? (red)

### 03. [0:23.1-0:28.1] MASTER QUESTION (= title)

VO: So how many times does the ocean kill you before you reach the bottom? Let's count.

On screen: Headline HOW MANY TIMES DOES THE OCEAN KILL YOU?; DEATHS 0

### 04. [0:28.4-0:40.1] RUNG 1 (0-1 km) entry + rule 1

VO: Ten metres down, your ears already hurt, because the pressure on you has doubled. Pinch your nose, blow, pop. And yes, you can breathe down here. That's rule one, so don't ask how.

On screen: Tag 10 M: PRESSURE x2; Options THE RULES item 1

### 05. [0:40.4-0:53.0] Rule 2 + FORMAT REVEAL (ALIVE meter, CHEATS LEFT 3)

VO: Rule two: every time the ocean kills you, you get a cheat that brings you back, but you only get three, and when they're gone, so are you. That's what this meter is for. Are you still alive? Right now, yes.

On screen: Options item 2; AliveMeter enters; CHEATS LEFT 3; big meter YES

### 06. [0:53.3-1:08.3] Rule 3 (planted for the twist) + sink rate

VO: Rule three: no submarine. Fewer people than fit on a bus have ever reached the bottom, all of them inside one, so you'll be the first thing of ours to get there without. At this slow walking pace, the trip takes about three hours.

On screen: Options item 3 + struck sub; Bus: FEWER THAN A BUSLOAD; Stat 1 M/S, ~3 HOURS

### 07. [1:08.6-1:16.1] RUNG 1 colour loss, TWILIGHT named

VO: Then the colours go, red first, then orange, then yellow, until everything is blue. Welcome to the twilight zone.

On screen: Options COLOURS LEFT struck one by one; Tag TWILIGHT ZONE

### 08. [1:16.4-1:27.0] RUNG 1 record (701 m)

VO: At seven hundred metres, you pass a quiet record. A diver in a French test chamber was once squeezed to exactly this pressure, and no human has felt more.

On screen: Chamber; Stat 701 M; HUMAN LIMIT line; silent 330 M = 1 EIFFEL TOWER

### 09. [1:27.3-1:37.3] RUNG 1 creature: sperm whale

VO: Then you feel a clicking so loud it buzzes in your chest. A sperm whale is hunting somewhere in the dark, and its clicks are the loudest sound any animal makes.

On screen: Sonar rings; SpermWhale; Tag LOUDEST ANIMAL ON EARTH; silent 828 M = 1 BURJ KHALIFA

### 10. [1:37.6-1:43.3] RUNG 1 plant ("its dinner")

VO: Relax, it's after squid, not you. Keep that in mind, because you're about to meet its dinner.

On screen: Tag MENU: SQUID / NEXT: ITS DINNER

### 11. [1:43.6-1:51.9] RUNG 1 threshold 1 km, MIDNIGHT named

VO: One kilometre, and you've reached the midnight zone, where the sunlight is gone for good, and from here down, the only light is alive.

On screen: Headline SUNLIGHT: 0%; bioluminescent flashes; Tag ~3 IN 4 ANIMALS HERE MAKE LIGHT

### 12. [1:52.2-2:03.2] RUNG 1 number + verdict YES

VO: The pressure is now a hundred times what you're used to, like a heavyweight boxer standing on every fingertip of your skin. Alive? Yes. You just can't see a thing.

On screen: Stat 100x; boxer on the fingertip tile; AliveMeter YES

### 13. [2:03.5-2:12.2] RUNG 2 (1-2 km) creature: giant squid (teaser 1 paid)

VO: Just below the line, something huge drifts up beside you: a giant squid, up to the length of a bus, with an eye wider than your face.

On screen: Eye opens; giant squid vs Bus; ScaleBar UP TO ~12 M; EYE ~27 CM vs YOUR FACE ~14 CM

### 14. [2:12.5-2:23.0] RUNG 2 weapon + callback (dinner fights back)

VO: Its suckers are ringed with tiny teeth, and dead sperm whales wash up with those rings printed on their skin, like rows of bottle caps. Dinner fights back.

On screen: Tag TOOTHED SUCKER RINGS; whale scars; Headline DINNER FIGHTS BACK

### 15. [2:23.3-2:36.8] RUNG 2 threat: nerves + honest unknown

VO: Then your hands start to shake, because at pressures like this nerves misfire: fingers tremble, rooms spin, people nod off mid-sentence. And at twice the record? Nobody knows. Nobody has been there.

On screen: Tag HIGH PRESSURE NERVOUS SYNDROME; Headline NOBODY KNOWS

### 16. [2:37.1-2:45.8] RUNG 2 verdict "?" (no cheat for a maybe)

VO: So your meter can't say yes or no. It says this. And a maybe doesn't earn a cheat, so you keep sinking, shaking, past two kilometres.

On screen: AliveMeter spins to ?; Tag A MAYBE DOESN'T EARN A CHEAT

### 17. [2:46.1-2:55.8] RUNG 3 (2-3 km) threat: the cold

VO: And here's the problem nobody warned you about: the cold. The surface was as warm as a heated pool, and down here it's barely above freezing.

On screen: Headline THE COLD; Stat 28 -> 2 °C; frost

### 18. [2:56.1-3:07.7] RUNG 3 you-scenario + host ruling

VO: In water that cold, most people black out within an hour, and you've been in it for over half an hour. Near three kilometres, you stop shivering. I'll be honest, this is where I'd have quit.

On screen: Stat 33 MIN; YOU tips over; Tag HOST: I'D HAVE QUIT HERE

### 19. [3:08.0-3:11.1] DEATH 1 (32%)

VO: Alive? No. First death, fifty minutes in.

On screen: AliveMeter NO, stamp DEATH 1; DEATHS 1; music out

### 20. [3:11.4-3:16.9] Cheat 1

VO: Cheat number one: a heated suit. You wake up warm, still sinking, and you're not alone.

On screen: Orange heated suit; CHEATS LEFT 2

### 21. [3:17.2-3:28.8] RUNG 3 creature: beaked whale (at your depth)

VO: A slim grey whale with a short beak glides past you: a Cuvier's beaked whale, the deepest-diving mammal ever tracked, and one was followed almost exactly to your depth.

On screen: Tags CUVIER'S BEAKED WHALE / DEEPEST-DIVING MAMMAL; Stat 2,992 M = YOUR DEPTH

### 22. [3:29.1-3:38.2] RUNG 3 comparison (teaser 2 paid)

VO: It breathes air, just like you, and with no cheats at all, its longest breath on record lasted longer than your entire fall to the bottom.

On screen: SpeedBars YOUR WHOLE FALL 182 MIN vs ITS LONGEST BREATH 222 MIN; ITS CHEATS: 0

### 23. [3:38.5-3:46.1] RUNG 4 (3-4 km) expectation reversal

VO: Nearly four kilometres down, you pass the average depth of the ocean, where most of the planet's seafloor would be.

On screen: Cross-section: AVERAGE OCEAN DEPTH ~3,700 M

### 24. [3:46.4-3:55.8] RUNG 4 geometry: onto the trench wall

VO: But you're over a trench, so the current nudges your sled against its wall, and you slide down it the rest of the way, with seven kilometres to go.

On screen: Dot drifts to the wall; wall view from here on; Headline 7 KM TO GO

### 25. [3:56.1-4:04.3] RUNG 5 (4-5 km) ABYSS named, shells dissolve

VO: Four kilometres: the abyss. The water here is so cold and squeezed that seashells landing this deep slowly dissolve.

On screen: Tag ABYSS; shells fade; Tag SEASHELLS DISSOLVE THIS DEEP

### 26. [4:04.6-4:08.7] Turnstile 1 (good news / bad news)

VO: Good news: you're not a seashell. Bad news: down here, you're food.

On screen: Headline GOOD NEWS -> BAD NEWS: YOU'RE FOOD

### 27. [4:09.0-4:21.3] RUNG 5 gross-out: bait cam

VO: When scientists drop a dead fish on slopes like this, long-tailed fish called grenadiers find it within half an hour, tiny scavengers swarm in, and within a day it can be bones.

On screen: BAIT CAM frame; +30 MIN; grenadiers; swarm; +1 DAY: BONES

### 28. [4:21.6-4:32.7] RUNG 5 threat on you + strategy + verdict

VO: And now the grenadiers are circling you. Strategy: keep moving, because if you nap down here, you become the event of the year. Alive? Yes. Being watched? Also yes.

On screen: Grenadiers circle YOU; STRATEGY: KEEP MOVING; BEING WATCHED: YES

### 29. [4:33.0-4:42.7] "Picture it again" re-immersion (47%)

VO: Picture where you are. Look up: the boat and the sunshine are over an hour of climbing above you. Look down: there's more water below you than above you.

On screen: Column: BOAT 75 MIN STRAIGHT UP; 6.4 KM BELOW > 4.5 KM ABOVE

### 30. [4:43.0-4:48.5] RUNG 6 (5-6 km) number

VO: Five kilometres. Every fingertip of your skin is now holding up a grand piano.

On screen: Stat 500x; piano on the fingertip tile

### 31. [4:48.8-5:00.9] RUNG 6 creature: dumbo octopus

VO: Out of the dark flaps a dumbo octopus, waving two fins like cartoon elephant ears. It's about as long as your forearm, and it lives deeper than any other octopus we know.

On screen: ScaleBar ~30 CM ≈ YOUR FOREARM; Stat 6,957 M DEEPEST OCTOPUS

### 32. [5:01.2-5:06.7] Verdict MOSTLY + turnstile 2 (52%)

VO: Alive? Mostly. But that wall you're sliding along is about to become the problem.

On screen: Crack in the wall; Headline THE WALL

### 33. [5:07.0-5:16.8] RUNG 7 (6-7 km) HADAL named

VO: Six kilometres. You've crossed into the hadal zone, the trenches, which cover a sliver of the seafloor but span almost half of the ocean's full depth.

On screen: Tags HADAL ZONE / A SLIVER OF THE SEAFLOOR / ~45% OF THE DEPTH RANGE

### 34. [5:17.1-5:25.7] RUNG 7 mechanism

VO: Trenches form where one plate of Earth's crust dives under another, so they shake, and their walls collapse in avalanches of mud.

On screen: Plate diagram; Tag QUAKES -> AVALANCHES OF MUD

### 35. [5:26.0-5:39.6] RUNG 7 dated aside + strategy punished

VO: After the great Japan earthquake of twenty eleven, mud slid down the Japan Trench all the way to its floor. And your strategy was to keep moving along the wall, which is exactly where avalanches run.

On screen: Map: TOHOKU 2011 / JAPAN TRENCH; STRATEGY KEEP MOVING struck

### 36. [5:39.9-5:46.4] DEATH 2 (58%, sawtooth crash)

VO: The slope above you shudders, and a cloud of mud rolls over your sled. Alive? No. Second death.

On screen: Mud cloud; AliveMeter NO, stamp DEATH 2; DEATHS 2

### 37. [5:46.7-5:55.3] Cheat 2 + host ruling

VO: Cheat number two: the mud lets you go. You shake yourself off, still sinking, with a single cheat left. I did warn you about the wall.

On screen: CHEATS LEFT 1; Tag HOST: I DID WARN YOU

### 38. [5:55.6-6:04.2] RUNG 8 (7-8 km) number

VO: Seven kilometres, and seven hundred times surface pressure, so every fingertip of your skin now has a dairy cow standing on it.

On screen: Stat 700x; cow on the fingertip tile

### 39. [6:04.5-6:18.8] RUNG 8 threat: molecules, verdict BARELY

VO: Now the pressure goes after your molecules. Proteins, the tiny machines your cells run on, get squashed out of shape, your cell membranes stiffen, and the chemistry of being alive starts to jam. Alive? Barely.

On screen: Protein squashed; membranes stiff; AliveMeter BARELY

### 40. [6:19.1-6:28.9] RUNG 9 (8-9 km) creature: snailfish ("and yet" reversal)

VO: Eight kilometres, and the locals don't mind at all. A snailfish, pink and see-through, like wet tissue paper with eyes, swims right up to your face.

On screen: Tags SNAILFISH / LIKE WET TISSUE PAPER WITH EYES

### 41. [6:29.2-6:44.3] RUNG 9 mechanism + its ceiling

VO: Its body is packed with a molecule called TMAO that holds its proteins in shape. But the deeper a fish lives, the more it needs, and a little past eight kilometres, it would need so much that water would flood its body.

On screen: TMAO x-ray; SpeedBars TMAO A FISH NEEDS (last row LIMIT ~8.2 KM)

### 42. [6:44.6-6:57.8] Teaser 3 paid: the last fish

VO: The deepest fish ever filmed was a young snailfish just past that line. No fish has ever been seen deeper, and the chemistry says none can go much further. You just met the last fish on the planet.

On screen: Stat 8,336 M DEEPEST FISH EVER FILMED; Headline THE LAST FISH ON THE PLANET

### 43. [6:58.1-7:05.1] DEATH 3 (72%): the fish ceiling becomes the weapon

VO: It turns back, and you sink straight through its ceiling without any of its chemistry. Alive? No. Third death.

On screen: FISH CEILING line passes; AliveMeter NO, stamp DEATH 3; DEATHS 3

### 44. [7:05.4-7:15.6] Cheat 3 (last) + stakes reset

VO: Cheat number three, your last: you borrow the trick of the little crustaceans that live all the way down. You're out of cheats, so die again, and the trip is over.

On screen: CHEATS LEFT 0; Headline 0 CHEATS LEFT; NEXT DEATH = TRIP OVER

### 45. [7:15.9-7:22.7] Biggest landmark: one Everest down (75%)

VO: By now, you've sunk the full height of Mount Everest, and there are still two kilometres of water underneath you.

On screen: Inverted Everest hung from the surface, summit at YOU; +2 KM TO GO

### 46. [7:23.0-7:32.1] No rescue (callback to the whale)

VO: You're also far beyond help, because the deepest rescue in history happened shallower than where you heard that sperm whale. Nobody is coming.

On screen: Sub icon at 480 M; whale at ~800 M; Headline NOBODY IS COMING

### 47. [7:32.4-7:47.9] RUNG 10 (9-10 km) creature + plant

VO: Nine kilometres. A tiny amphipod, about as long as the top joint of your thumb, is chewing on a sunken branch. Its gut turns dead wood into sugar, so whatever sinks from the surface ends up inside it. Remember that.

On screen: HIRONDELLEA GIGAS ~3 CM vs thumb; x-ray gut with an unlabelled grey speck

### 48. [7:48.2-7:51.7] Verdict YES, 0 cheats

VO: Alive? Yes. Cheats left? None. Lonely? Extremely.

On screen: Tags 9 KM: ALIVE · 0 CHEATS / LONELY: EXTREMELY

### 49. [7:52.0-8:01.9] RUNG 11 (10-10.9 km) creature

VO: Ten kilometres. Lumps the size of your fist sit on the wall, and each one is a single giant cell. You, for comparison, are made of trillions.

On screen: Tags XENOPHYOPHORE: ONE CELL EACH / YOU: ~30 TRILLION CELLS

### 50. [8:02.2-8:11.4] Arrival: Challenger Deep, three hours

VO: Then the sled thumps into soft mud. This is the bottom, Challenger Deep, the lowest point in the ocean, three hours after you left the boat.

On screen: Sled lands; DepthMeter locks 10,935; CHALLENGER DEEP; ELAPSED 3 H 02 MIN

### 51. [8:11.7-8:23.1] Final number + final near-death with 0 cheats

VO: Every fingertip of your skin now carries more than a tonne, about the weight of a small car, and you have no cheats left. The needle slides toward no, and stops. Alive? Yes.

On screen: Car on the fingertip tile; ~1.1 TONNES ON EVERY CM²; needle slides, stops, YES

### 52. [8:23.4-8:31.0] Finished board + peak declared (86%)

VO: Final reading. Deaths: three. Cheats left: none. You beat the ocean, and honestly, it doesn't get any better than this.

On screen: Board FINAL READING (11 rows); DEATHS 3; YOU BEAT THE OCEAN

### 53. [8:31.8-8:36.3] TWIST (88%): rule 3 turned around

VO: Except you weren't the first thing of ours to get here without a submarine.

On screen: dipBlack; half-buried grey shape; Headline NOT THE FIRST

### 54. [8:36.6-8:49.1] Teaser 4 paid: the bag (89%)

VO: In nineteen ninety-eight, a robot sub filmed it lying on the floor of this trench, almost at the bottom: a plastic shopping bag, the single-use kind from a checkout. No cheats, and no help.

On screen: Stat 10,898 M FILMED 1998; SINGLE-USE PLASTIC BAG; RULE 3: BROKEN

### 55. [8:49.4-9:00.0] Callback to the plant: fibres

VO: And that amphipod that eats whatever sinks? Researchers checked the ones from the deepest part of this trench, and every one they opened had man-made fibres in its gut.

On screen: x-ray speck turns red, multiplies; MAN-MADE FIBRES: IN EVERY ONE CHECKED

### 56. [9:00.3-9:12.2] Escalation: PCBs

VO: Some carried PCBs, industrial chemicals banned decades ago, at about fifty times the levels in crabs from paddy fields fed by one of China's most polluted rivers.

On screen: SpeedBars PCB LEVELS 1x vs ~50x; PCBs: BANNED DECADES AGO

### 57. [9:12.5-9:22.2] Villain swap

VO: So of everything you met on the way down, the squid, the cold, the mud and the crushing weight, the newest arrival at the bottom of the world is ours.

On screen: EVERYTHING YOU MET struck in turn; Headline THE NEWEST ARRIVAL IS OURS

### 58. [9:22.5-9:36.0] BOOKEND (mirror of frame 1) + left-open ending

VO: Picture the start again: calm water, sunshine, the boat. Your sled took three hours. Whatever slips into that water today starts the same trip, and nobody knows how long it takes. It just keeps arriving.

On screen: Surface, boat, empty crane; bag drifts down; YOU: 3 H / IT: ?; board held 6 s with WHERE WOULD YOU HAVE QUIT?
<!-- /gen:scenes -->

## Shot list

Kit: `studio/src/kits/explainer`. `[YOU+sled]` = YOU standing on the static sled SVG at true scale (default 200 px/m; whale, squid and beaked-whale shots draw YOU at the creature's pxPerM). `[WALL]` = the trench-wall layer, scrolling up as you slide (every descent shot from 3:56 on). `[HUD]` = DepthMeter right (window 1,400 m, zones + markers), AliveMeter left (from 0:40), CHEATS LEFT top-left (from "three" at 0:44). Times are measured word anchors; the builder re-times by re-running `gen_storyboard.py` after the final mix.

<!-- gen:shots -->
| # | t_start | t_end | shot | visual (kit vocabulary) | camera | SFX |
|---|---|---|---|---|---|---|
| 1 `s01_surface` | 0:00.0 | 0:04.7 | wide, cross-section | Bright Pacific surface; tiny boat crane holds YOU strapped to the yellow sled; 5 s Timer ring hits 0 on "drops"; Tag MARIANA TRENCH [YOU+sled] | drift | tick, underwater_rumble |
| 2 `s02_drop` | 0:04.7 | 0:09.9 | tilt-down reveal | Latch opens; sled + YOU plunge through the waterline in bubbles; the column darkens; DepthMeter slides in; red Headline 11 KM on "eleven" [YOU+sled · HUD] | panDown | bubbles, riser, whoosh_long |
| 3 `t1_eye` | 0:09.9 | 0:12.9 | teaser card 1 | Squid silhouette, one huge eye glints; Tag AN EYE WIDER THAN YOUR FACE | pushIn | whoosh |
| 4 `t2_whale` | 0:12.9 | 0:16.5 | teaser card 2 | Beaked-whale silhouette; Tag ONE BREATH LONGER THAN YOUR WHOLE TRIP | pushIn | whoosh |
| 5 `t3_fish` | 0:16.5 | 0:18.6 | teaser card 3 | Pale pink snailfish alone on black; Tag THE LAST FISH | pushIn | whoosh |
| 6 `t4_unknown` | 0:18.6 | 0:23.1 | teaser card 4 | Black frame, a dashed grey outline that reads as nothing; red Headline ? | pushIn | stinger |
| 7 `s03_question` | 0:23.1 | 0:28.4 | title card | YOU sinking small in blue; Headline HOW MANY TIMES DOES THE OCEAN KILL YOU?; Tag LET'S COUNT; DEATHS counter 0 appears [YOU+sled · HUD] | pushIn | ding, riser |
| 8 `s04_ears` | 0:28.4 | 0:35.4 | medium, you vs water | Ocean 10 m, rays; YOU panic then pop; Tag PRESSURE x2 (first felt rung at 0:28) [YOU+sled · HUD] | pushIn | pop |
| 9 `s05_rule1` | 0:35.4 | 0:40.4 | rules card | Options THE RULES, item 1 YOU CAN BREATHE lands; YOU shrug [YOU+sled · HUD] | drift | click |
| 10 `s06_rule2` | 0:40.4 | 0:48.0 | rules card + HUD build | Item 2 lands; ALIVE meter slides in left; CHEATS LEFT 3 top-left on "three" [YOU+sled · HUD] | drift | click, ding |
| 11 `s07_meter` | 0:48.0 | 0:53.3 | HUD close-up | AliveMeter big centre-screen, needle settles on YES with a green stamp; Headline ARE YOU STILL ALIVE? [HUD] | pushIn | ding |
| 12 `s08_rule3` | 0:53.3 | 1:04.0 | rules card | Item 3 NO SUBMARINE lands; yellow sub slides in and is struck red; small kit Bus with Tag FEWER VISITORS THAN BUS SEATS [HUD] | drift | click, pop |
| 13 `s09_rate` | 1:04.0 | 1:08.6 | stat callouts | YOU on sled sinking; Stat 1 M/S SINK RATE; Stat ~3 HOURS TO THE BOTTOM [YOU+sled · HUD] | drift | tick |
| 14 `s10_colours` | 1:08.6 | 1:16.4 | wide, falling | Ocean depth 10->200; Options COLOURS LEFT [RED ORANGE YELLOW GREEN BLUE], strikes on each spoken colour; zone TWILIGHT lights; silent landmark Tag 330 M = 1 EIFFEL TOWER [YOU+sled · HUD] | panDown | tick, whoosh_long |
| 15 `s11_record` | 1:16.4 | 1:24.8 | record card | Pressure chamber (HYDRA) with a figure inside; Stat 701 M DEEPEST PRESSURE A HUMAN HAS FELT (1992, CHAMBER); silent Tag 330 M = 1 EIFFEL TOWER passes [YOU+sled · HUD] | drift | tick |
| 16 `s12_limit` | 1:24.8 | 1:27.3 | threshold | Red dashed HUMAN LIMIT line scrolls up past YOU; DepthMeter flag at 701 m; Headline NO HUMAN HAS FELT MORE [YOU+sled · HUD] | pushIn | drone |
| 17 `s13_clicks` | 1:27.3 | 1:30.7 | sound reveal | Near-black; sonar rings pulse across the frame; YOU jitters with each click; Tag CLICK CLICK CLICK [YOU+sled · HUD] | drift | click, sonar_ping |
| 18 `s14_whale` | 1:30.7 | 1:37.6 | creature pass | SpermWhale at shared pxPerM (16 m vs 1.75 m) glides L->R behind YOU; Tag LOUDEST ANIMAL ON EARTH; silent Tag 828 M = 1 BURJ KHALIFA DOWN [YOU+sled · HUD] | panRight | underwater_rumble |
| 19 `s15_plant` | 1:37.6 | 1:43.6 | two-shot | Whale tilts down and dives out of frame; a round thought bubble with a small squid silhouette; Tag MENU: SQUID [YOU+sled · HUD] | panDown | whoosh |
| 20 `s16_midnight` | 1:43.6 | 1:52.2 | threshold card | DepthMeter ticks 1,000 with a flash; zone MIDNIGHT; Headline SUNLIGHT: 0%; rays gone; blue bioluminescent flashes (particles stars) on "alive" [YOU+sled · HUD] | pushIn | boom, sonar_ping |
| 21 `s17_boxer` | 1:52.2 | 1:59.5 | scale gag (motif 1/4) | Stat 100x; fingertip tile with a tiny YOU as the heavyweight boxer standing on it; Tag ~100 KG ON EVERY CM2 [HUD] | drift | impact |
| 22 `s18_v1` | 1:59.5 | 2:03.5 | verdict stamp | AliveMeter big: YES stamp; YOU shrugs alone in black; Tag 1 KM: YES [YOU+sled · HUD] | pushIn | ding |
| 23 `s19_eye_opens` | 2:03.5 | 2:07.2 | withheld reveal | Below YOU a huge pale eye opens in the black (two circles, scaleY 0->1) on "something huge" [YOU+sled · HUD] | panDown | heartbeat_slow |
| 24 `s20_squid` | 2:07.2 | 2:09.9 | creature reveal | ColossalSquid drawing as giant squid (hooks off, variant giant) at shared pxPerM with YOU; kit Bus ghosted behind for length; Tag GIANT SQUID; ScaleBar UP TO ~12 M [YOU+sled · HUD] | pullOut | whoosh_long |
| 25 `s21_eye_face` | 2:09.9 | 2:12.5 | scale comparison | Close: the 27 cm eye beside YOU's head at the same scale; Tag EYE ~27 CM vs YOUR FACE ~14 CM (teaser 1 paid, 21%) | pushIn | pop |
| 26 `s22_suckers` | 2:12.5 | 2:15.2 | detail insert | Close on a squid arm: sucker discs with toothed rim rings (circle layers); Tag TOOTHED SUCKER RINGS | pushIn | click |
| 27 `s23_scars` | 2:15.2 | 2:23.3 | callback insert | SpermWhale head close-up printed with rows of ring scars (stroke circles) like bottle caps; Headline DINNER FIGHTS BACK | panLeft | impact |
| 28 `s24_shake` | 2:23.3 | 2:32.1 | symptom beats | YOU on sled with a jitter idle; wobble rotate keyframes on "rooms spin"; "Zz" text on "nod off"; Tag HIGH PRESSURE NERVOUS SYNDROME [YOU+sled · HUD] | drift | glitch |
| 29 `s25_unknown` | 2:32.1 | 2:37.1 | admission card | DepthMeter flags 701 and 1,400 (2x RECORD); Headline NOBODY KNOWS red [YOU+sled · HUD] | pushIn | drone |
| 30 `s26_q` | 2:37.1 | 2:40.6 | meter beat | AliveMeter big: needle spins and lands on ? (yellow) on "It says this" [HUD] | pushIn | glitch |
| 31 `s27_nocheat` | 2:40.6 | 2:46.1 | rule beat | CHEATS LEFT 3 pulses; Tag A MAYBE DOESN'T EARN A CHEAT; YOU keeps sinking, shaking, DepthMeter passes 2,000 [YOU+sled · HUD] | drift | tick |
| 32 `s28_cold` | 2:46.1 | 2:50.0 | re-hook card | Headline THE COLD; frost vignette creeps in from the edges; YOU tinted pale blue, pose panic [YOU+sled · HUD] | pushIn | drone |
| 33 `s29_temp` | 2:50.0 | 2:56.1 | temperature drop | Stat counts 28 -> 2 °C WATER TEMPERATURE across the sentence; Tags SURFACE: HEATED-POOL WARM / HERE: BARELY ABOVE FREEZING [YOU+sled · HUD] | drift | tick |
| 34 `s30_blackout` | 2:56.1 | 3:02.0 | you-scenario | Tag MOST PEOPLE BLACK OUT IN < 1 H; Stat 33 MIN YOU, IN WATER THIS COLD; frost thickens [YOU+sled · HUD] | drift | heartbeat_slow |
| 35 `s31_limp` | 3:02.0 | 3:08.0 | you close-up | Shiver stops: YOU goes grey and tips over (rotate -75) and drifts; ALIVE needle slides to BARELY; host Tag I'D HAVE QUIT HERE [YOU+sled · HUD] | pushIn | heartbeat_slow |
| 36 `s32_death1` | 3:08.0 | 3:11.4 | verdict stamp (DEATH 1) | Music out. AliveMeter big slams NO, red stamp DEATH 1; Tag 3,000 M · 50 MIN IN; grade dark; DEATHS 0->1 [HUD] | pushIn | stinger |
| 37 `s33_cheat1` | 3:11.4 | 3:17.2 | revive | YOU re-coloured orange (heated suit, glow shadow), rotates upright; CHEATS LEFT 3->2; ALIVE YES; a long shadow slides behind on "not alone" [YOU+sled · HUD] | drift | ding, riser |
| 38 `s34_beaked` | 3:17.2 | 3:25.5 | creature pass | BeakedWhale (6 m, grey, scarred) glides past YOU at shared pxPerM; Tags CUVIER'S BEAKED WHALE / DEEPEST-DIVING MAMMAL [YOU+sled · HUD] | panLeft | underwater_rumble |
| 39 `s35_beaked_record` | 3:25.5 | 3:29.1 | record card | DepthMeter marker 2,992 m sits right at YOU; Stat 2,992 M TRACKED DIVE; Tag = YOUR DEPTH [YOU+sled · HUD] | drift | tick |
| 40 `s36_breath` | 3:29.1 | 3:38.5 | comparison bars | SpeedBars ONE BREATH vs YOUR TRIP [YOUR WHOLE FALL 182 MIN, ITS RECORD BREATH 222 MIN red]; whale gets its own CHEATS 0 tag (teaser 2 paid, 36%) [YOU+sled · HUD] | drift | pop, tick |
| 41 `s37_average` | 3:38.5 | 3:46.4 | cross-section | Wide cutaway: typical seafloor line at 3.7 km with the trench slot dropping away under YOU (dot); Tag AVERAGE OCEAN DEPTH ~3,700 M | pullOut | whoosh_long |
| 42 `s38_nudge` | 3:46.4 | 3:51.3 | cross-section beat | Same cutaway: the YOU dot drifts to the trench's west wall (keyframes), Tag CURRENT, then cuts in | pushIn | whoosh |
| 43 `s39_wall` | 3:51.3 | 3:56.1 | wall view (from here to the floor) | Trench WALL (rock slope) enters left, scrolling up as the sled scrapes down it; Headline 7 KM TO GO red [WALL · YOU+sled · HUD] | drift | underwater_rumble |
| 44 `s40_abyss` | 3:56.1 | 4:04.6 | process insert | Zone ABYSS lights; seashells drift onto the wall ledge and fade to nothing; Tag SHELLS DISSOLVE BELOW ~4,500 M [WALL · YOU+sled · HUD] | drift | bubbles |
| 45 `s41_news` | 4:04.6 | 4:09.0 | punch card | Headline GOOD NEWS (green) then BAD NEWS: YOU'RE FOOD (red); YOU point then panic (turnstile 1, 42%) [WALL · YOU+sled · HUD] | drift | pop, stinger |
| 46 `s42_baitcam` | 4:09.0 | 4:16.6 | bait-cam frame | Bait-cam frame on the slope: dead fish (DeepFish dead) on the mud; Tag +30 MIN; grenadiers (DeepFish x2) nose in on "grenadiers" | pushIn | static, tick |
| 47 `s43_bones` | 4:16.6 | 4:21.6 | time-lapse | Pale speck swarm (particles dust) covers the bait, then a skeleton replaces the fish; Tag 1 DAY: BONES (gross-out peak, 43-45%) | drift | pop, static |
| 48 `s44_circling` | 4:21.6 | 4:28.9 | threat on you | Back on the wall: three grenadiers circle YOU (looping keyframes); Options STRATEGY [KEEP MOVING]; Tag NAP = EVENT OF THE YEAR [WALL · YOU+sled · HUD] | drift | whoosh |
| 49 `s45_watched` | 4:28.9 | 4:33.0 | gag + verdict | Pairs of eyes glint in the black around YOU; ALIVE YES stamp; Tag BEING WATCHED: YES [WALL · YOU+sled · HUD] | pullOut | ding |
| 50 `s46_picture` | 4:33.0 | 4:43.0 | column cutaway ("picture it again", 47%) | Full 0-11 km column: boat at the top, YOU dot at 4.5 km on the wall; Tag BOAT: 75 MIN STRAIGHT UP on "Look up"; Tag MORE WATER BELOW THAN ABOVE on "Look down" | pullOut | whoosh_long |
| 51 `s47_piano` | 4:43.0 | 4:48.8 | scale gag (motif 2/4) | Fingertip tile, now a grand piano on it; Stat 500x; Tag ~500 KG ON EVERY CM2 [HUD] | drift | impact |
| 52 `s48_dumbo` | 4:48.8 | 4:57.5 | creature reveal | DumboOctopus flaps in beside YOU (ear-fin flap idle); Tag DUMBO OCTOPUS; ScaleBar ~30 CM next to YOU's forearm [WALL · YOU+sled · HUD] | drift | bubbles |
| 53 `s49_dumbo_record` | 4:57.5 | 5:01.2 | record card | DepthMeter marker 6,957 m far below YOU; Stat 6,957 M DEEPEST OCTOPUS (2020) [WALL · YOU+sled · HUD] | drift | tick |
| 54 `s50_mostly` | 5:01.2 | 5:07.0 | verdict + turnstile 2 | ALIVE MOSTLY stamp; camera pans up the wall to a hairline crack; Headline THE WALL red on "about to become the problem" (52%) [WALL · YOU+sled · HUD] | panUp | ding, underwater_rumble |
| 55 `s51_hadal` | 5:07.0 | 5:17.1 | threshold card | Zone HADAL lights red; trench walls rise on both sides; Tags HADAL ZONE / A SLIVER OF THE SEAFLOOR / ~45% OF THE OCEAN'S DEPTH RANGE [WALL · YOU+sled · HUD] | panDown | boom |
| 56 `s52_plates` | 5:17.1 | 5:26.0 | diagram | Two-plate cross-section (Pacific plate dives under the Philippine Sea plate, red arrow); camera shake on "shake"; Tag AVALANCHES | pushIn + shake | underwater_rumble |
| 57 `s53_japan` | 5:26.0 | 5:33.4 | map aside | Map: Japan Trench, ring at the 2011 Tohoku epicentre; pin YOU at the Mariana Trench; Tag 2011: MUD REACHED THE TRENCH FLOOR | none | boom |
| 58 `s54_punished` | 5:33.4 | 5:39.9 | callback strike | Back on the wall: STRATEGY [KEEP MOVING] returns and gets struck red on "exactly where avalanches run"; Tag AVALANCHE PATH arrow down the wall [WALL · YOU+sled · HUD] | drift | pop |
| 59 `s55_death2` | 5:39.9 | 5:46.7 | avalanche + verdict (DEATH 2) | Wall shudders (camera shake), mud cloud (gradient + brown particles) rolls down over YOU; AliveMeter NO, red stamp DEATH 2; DEATHS 1->2 [WALL · YOU+sled · HUD] | drift + shake | boom, stinger, underwater_rumble |
| 60 `s56_cheat2` | 5:46.7 | 5:55.6 | revive | Mud thins (opacity out); YOU in the orange suit shakes off (jitter), CHEATS LEFT 2->1; ALIVE YES; host Tag TOLD YOU: THE WALL [WALL · YOU+sled · HUD] | drift | ding, riser |
| 61 `s57_cow` | 5:55.6 | 6:04.5 | scale gag (motif 3/4) | Fingertip tile, now a dairy cow on it; Stat 700x; Tag ~700 KG ON EVERY CM2 [HUD] | drift | impact |
| 62 `s58_protein` | 6:04.5 | 6:11.8 | microscope insert | Circular microscope frame (dipBlack in): a folded protein ribbon is squashed flat (scaleY 1->0.35) on "squashed"; Tag PROTEINS: OUT OF SHAPE | pushIn | glitch |
| 63 `s59_membrane` | 6:11.8 | 6:19.1 | mechanism + verdict | Membrane bilayer row compresses (scaleY); ALIVE BARELY orange stamp on "Barely"; YOU sags (rotate 15) | drift | heartbeat_slow |
| 64 `s60_snailfish` | 6:19.1 | 6:29.2 | creature reveal | A pale shape flickers at frame edge, then the Snailfish swims up to YOU's face; Tags SNAILFISH / LIKE WET TISSUE PAPER [WALL · YOU+sled · HUD] | drift | bubbles, sonar_ping |
| 65 `s61_tmao` | 6:29.2 | 6:35.2 | x-ray cutaway | Snailfish x-ray (prop xray): small TMAO spheres prop up a protein ribbon; Tag TMAO HOLDS PROTEINS IN SHAPE | pushIn | pop |
| 66 `s62_ceiling` | 6:35.2 | 6:44.6 | graph | SpeedBars TMAO A FISH NEEDS by depth (2 / 4 / 6 / 8 KM, last row red text LIMIT ~8.2 KM); Tag BEYOND THIS: WATER FLOODS IN | drift | stinger, tick |
| 67 `s63_lastfish` | 6:44.6 | 6:49.7 | record card (teaser 3 paid, 70%) | DepthMeter marker FISH LIMIT; small juvenile Snailfish at a red flag; Stat 8,336 M DEEPEST FISH EVER FILMED (2022); Headline THE LAST FISH [WALL · YOU+sled · HUD] | drift | ding |
| 68 `s63b_nofish` | 6:49.7 | 6:58.1 | isolation | Red FISH LIMIT line under YOU; Tag NO FISH SEEN DEEPER; Headline THE LAST FISH ON THE PLANET on "You just met" [WALL · YOU+sled · HUD] | drift | drone |
| 69 `s64_death3` | 6:58.1 | 7:05.4 | isolation + verdict (DEATH 3) | The snailfish turns back up and fades; red dashed FISH CEILING line scrolls up past YOU; AliveMeter NO, stamp DEATH 3; DEATHS 2->3 [WALL · YOU+sled · HUD] | drift | stinger |
| 70 `s65_cheat3` | 7:05.4 | 7:15.9 | revive (last cheat) | Tiny amber Amphipods crawl on the wall beside YOU; CHEATS LEFT 1->0 (red); ALIVE YES; Headline 0 CHEATS LEFT; Tag NEXT DEATH = TRIP OVER [WALL · YOU+sled · HUD] | drift | ding, riser, stinger |
| 71 `s66_everest` | 7:15.9 | 7:23.0 | signature scale image (75%) | Wide column: Everest hung upside down from the surface line, its summit exactly at YOU (8,849 m); 2 km of water still below; Tags ONE EVEREST DOWN / +2 KM TO GO | pullOut | boom, whoosh_long |
| 72 `s67_rescue` | 7:23.0 | 7:32.4 | record card | Same column: small yellow sub icon at 480 m near the top, sperm-whale icon at ~800 m, YOU far below; Tag DEEPEST RESCUE EVER: 480 M (1973); Headline NOBODY IS COMING | pushIn | drone, tick |
| 73 `s68_hirondellea` | 7:32.4 | 7:40.4 | creature + scale | Amber Amphipod (Hirondellea, ~3 cm) chewing a sunken branch on the wall; thumb tile beside it; ScaleBar ~3 CM ≈ TOP JOINT OF YOUR THUMB | pushIn | click |
| 74 `s69_plant` | 7:40.4 | 7:48.2 | x-ray plant | X-ray gut overlay: wood bits, and one faint grey speck among them (unlabelled plant); Tag DEAD WOOD -> SUGAR; speck pulses once on "Remember that" | pushIn | sonar_ping |
| 75 `s70_lonely` | 7:48.2 | 7:52.0 | verdict stamp | AliveMeter YES; CHEATS LEFT 0 in red; YOU tiny in a wide black frame on the wall; Tag LONELY: EXTREMELY [WALL · YOU+sled · HUD] | pullOut | ding |
| 76 `s71_xeno` | 7:52.0 | 8:02.2 | creature | Fist-sized xenophyophore lumps on the wall ledge beside YOU (pose point); Tags ONE CELL EACH / YOU: ~30 TRILLION CELLS [WALL · YOU+sled · HUD] | drift | bubbles |
| 77 `s72_landing` | 8:02.2 | 8:11.7 | landing | Sled thumps into the mud (squash keyframe), silt puff; DepthMeter locks 10,935 with a red frame; Tag CHALLENGER DEEP; Tag 3 H 02 MIN on "three hours" [YOU+sled · HUD] | pushIn + shake | boom, impact |
| 78 `s73_car` | 8:11.7 | 8:16.5 | scale gag (motif 4/4) | Fingertip tile, now the kit Car on it; Tag ~1.1 T ON EVERY CM2 [HUD] | drift | impact |
| 79 `s74_last_test` | 8:16.5 | 8:23.4 | final near-death | AliveMeter big, 0 cheats: needle slides toward NO, stops at BARELY, then YES stamp on "Alive? Yes."; heartbeat [HUD] | pushIn | ding, heartbeat_slow |
| 80 `s75_board` | 8:23.4 | 8:31.8 | finished board (peak declared, 86%) | Board FINAL READING, 11 km bands written out (0-1 YES / 1-2 ? / 2-3 DEATH 1 / 3-4 YES / 4-5 YES / 5-6 MOSTLY / 6-7 DEATH 2 / 7-8 BARELY / 8-9 DEATH 3 / 9-10 YES / 10-bottom YES, 0 cheats); Stat DEATHS 3, CHEATS LEFT 0; Headline YOU BEAT THE OCEAN (green) | pullOut | ding, riser |
| 81 `s76_turn` | 8:31.8 | 8:36.6 | turn | dipBlack; slow push toward a grey shape half-buried in the mud beside YOU; Headline NOT THE FIRST (red) [YOU+sled] | pushIn | stinger |
| 82 `s77_bag` | 8:36.6 | 8:49.4 | reveal (teaser 4 paid, 89%) | ROV light pool on the mud: a white single-use plastic bag; Stat 10,898 M FILMED 1998; Tag SINGLE-USE PLASTIC BAG; on "No cheats" Tag RULE 3: BROKEN | pushIn | drone |
| 83 `s78_fibres` | 8:49.4 | 9:00.3 | callback x-ray | The 9 km x-ray gut again: the grey speck turns red and multiplies into fibres (stagger); Tag MAN-MADE FIBRES: IN EVERY ONE CHECKED | pushIn | sonar_ping |
| 84 `s79_pcb` | 9:00.3 | 9:12.5 | comparison bars | SpeedBars PCB LEVELS [PADDY-FIELD CRABS, POLLUTED RIVER 1x grey; TRENCH AMPHIPODS ~50x red]; Tag BANNED DECADES AGO | drift | tick |
| 85 `s80_swap` | 9:12.5 | 9:22.5 | callback strike-list + tilt up | Options [THE SQUID, THE COLD, THE MUD, THE CRUSHING WEIGHT] struck in turn on each word; Headline THE NEWEST ARRIVAL IS OURS (red); camera tilts up the column | panUp | whoosh |
| 86 `s81_bookend` | 9:22.5 | 9:28.6 | bookend (mirror of s01) | Same framing as frame 1: bright surface, boat, empty crane, no sled | drift | underwater_rumble |
| 87 `s82_drift` | 9:28.6 | 9:36.3 | drift-down | A single plastic bag slips under the surface and starts down the darkening column; Tags YOU: 3 H / IT: ? on "nobody knows how long" | panDown | bubbles |
| 88 `s83_hold` | 9:36.3 | 9:42.0 | finished board hold (6 s, no spoken CTA) | Finished board held; Tag WHERE WOULD YOU HAVE QUIT?; cut to black at the end | none | ding |
<!-- /gen:shots -->

## Narration (pipeline block)

```narration
[music: deep_ocean] You're strapped to a sled above the deepest trench on Earth, and in five seconds it drops.

It won't stop for eleven kilometres, and on the way down you'll meet a squid with an eye wider than your face, a whale that holds one breath longer than your whole trip, the last fish on the planet, and, almost at the bottom, something that should never have made it there.

So how many times does the ocean kill you before you reach the bottom? Let's count.

Ten metres down, your ears already hurt, because the pressure on you has doubled. Pinch your nose, blow, pop. And yes, you can breathe down here. That's rule one, so don't ask how.

Rule two: every time the ocean kills you, you get a cheat that brings you back, but you only get three, and when they're gone, so are you. That's what this meter is for. Are you still alive? Right now, yes.

Rule three: no submarine. Fewer people than fit on a bus have ever reached the bottom, all of them inside one, so you'll be the first thing of ours to get there without. At this slow walking pace, the trip takes about three hours.

Then the colours go, red first, then orange, then yellow, until everything is blue. Welcome to the twilight zone.

At seven hundred metres, you pass a quiet record. A diver in a French test chamber was once squeezed to exactly this pressure, and no human has felt more.

Then you feel a clicking so loud it buzzes in your chest. A sperm whale is hunting somewhere in the dark, and its clicks are the loudest sound any animal makes.

Relax, it's after squid, not you. Keep that in mind, because you're about to meet its dinner.

One kilometre, and you've reached the midnight zone, where the sunlight is gone for good, and from here down, the only light is alive.

The pressure is now a hundred times what you're used to, like a heavyweight boxer standing on every fingertip of your skin. Alive? Yes. You just can't see a thing.

Just below the line, something huge drifts up beside you: a giant squid, up to the length of a bus, with an eye wider than your face.

Its suckers are ringed with tiny teeth, and dead sperm whales wash up with those rings printed on their skin, like rows of bottle caps. Dinner fights back.

Then your hands start to shake, because at pressures like this nerves misfire: fingers tremble, rooms spin, people nod off mid-sentence. And at twice the record? Nobody knows. Nobody has been there.

So your meter can't say yes or no. It says this. And a maybe doesn't earn a cheat, so you keep sinking, shaking, past two kilometres.

And here's the problem nobody warned you about: the cold. The surface was as warm as a heated pool, and down here it's barely above freezing.

In water that cold, most people black out within an hour, and you've been in it for over half an hour. Near three kilometres, you stop shivering. I'll be honest, this is where I'd have quit.

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

Five kilometres. Every fingertip of your skin is now holding up a grand piano.

Out of the dark flaps a dumbo octopus, waving two fins like cartoon elephant ears. It's about as long as your forearm, and it lives deeper than any other octopus we know.

Alive? Mostly. But that wall you're sliding along is about to become the problem.

Six kilometres. You've crossed into the hadal zone, the trenches, which cover a sliver of the seafloor but span almost half of the ocean's full depth.

Trenches form where one plate of Earth's crust dives under another, so they shake, and their walls collapse in avalanches of mud.

After the great Japan earthquake of twenty eleven, mud slid down the Japan Trench all the way to its floor. And your strategy was to keep moving along the wall, which is exactly where avalanches run.

The slope above you shudders, and a cloud of mud rolls over your sled. Alive? No. Second death.

Cheat number two: the mud lets you go. You shake yourself off, still sinking, with a single cheat left. I did warn you about the wall.

Seven kilometres, and seven hundred times surface pressure, so every fingertip of your skin now has a dairy cow standing on it.

Now the pressure goes after your molecules. Proteins, the tiny machines your cells run on, get squashed out of shape, your cell membranes stiffen, and the chemistry of being alive starts to jam. Alive? Barely.

Eight kilometres, and the locals don't mind at all. A snailfish, pink and see-through, like wet tissue paper with eyes, swims right up to your face.

Its body is packed with a molecule called TMAO that holds its proteins in shape. But the deeper a fish lives, the more it needs, and a little past eight kilometres, it would need so much that water would flood its body.

The deepest fish ever filmed was a young snailfish just past that line. No fish has ever been seen deeper, and the chemistry says none can go much further. You just met the last fish on the planet.

It turns back, and you sink straight through its ceiling without any of its chemistry. Alive? No. Third death.

Cheat number three, your last: you borrow the trick of the little crustaceans that live all the way down. You're out of cheats, so die again, and the trip is over.

By now, you've sunk the full height of Mount Everest, and there are still two kilometres of water underneath you.

You're also far beyond help, because the deepest rescue in history happened shallower than where you heard that sperm whale. Nobody is coming.

Nine kilometres. A tiny amphipod, about as long as the top joint of your thumb, is chewing on a sunken branch. Its gut turns dead wood into sugar, so whatever sinks from the surface ends up inside it. Remember that.

Alive? Yes. Cheats left? None. Lonely? Extremely.

Ten kilometres. Lumps the size of your fist sit on the wall, and each one is a single giant cell. You, for comparison, are made of trillions.

Then the sled thumps into soft mud. This is the bottom, Challenger Deep, the lowest point in the ocean, three hours after you left the boat.

Every fingertip of your skin now carries more than a tonne, about the weight of a small car, and you have no cheats left. The needle slides toward no, and stops. Alive? Yes.

Final reading. Deaths: three. Cheats left: none. You beat the ocean, and honestly, it doesn't get any better than this.

[pause: 0.5] Except you weren't the first thing of ours to get here without a submarine.

In nineteen ninety-eight, a robot sub filmed it lying on the floor of this trench, almost at the bottom: a plastic shopping bag, the single-use kind from a checkout. No cheats, and no help.

And that amphipod that eats whatever sinks? Researchers checked the ones from the deepest part of this trench, and every one they opened had man-made fibres in its gut.

Some carried PCBs, industrial chemicals banned decades ago, at about fifty times the levels in crabs from paddy fields fed by one of China's most polluted rivers.

So of everything you met on the way down, the squid, the cold, the mud and the crushing weight, the newest arrival at the bottom of the world is ours.

Picture the start again: calm water, sunshine, the boat. Your sled took three hours. Whatever slips into that water today starts the same trip, and nobody knows how long it takes. It just keeps arriving.
```

## Notes for the storyboard builder

- `gen_storyboard.py` is the source of the shot list, the timed scene list and the pacing block above (run `python3 gen_storyboard.py --md`). Edit shots there, not in this file.
- Re-time after the final mix: run `measure_tts.py` on the Spark (or copy the mix's caption word timings into `durations.json` in the same shape) and re-run the generator. Every shot and layer event is a word anchor, so nothing else changes.
- Numbers are spelled out in VO; digits appear only in `Stat` / `Tag` / `Headline` layers. `Stat` gets numeric values only.
- Gore: none. The deaths are a grey stick figure tipping over plus a red stamp; the avalanche is a mud cloud; the bait cam shows a dead fish, never a person.
- Mix: music bed drops out for the three death stamps and the twist turn (music entries in storyboard.json); death stingers are storyboard SFX, not narration markers, so they are not doubled.
- Description line (R5 insurance): "Narration voiced with a synthetic voice. Animation is original and code-drawn." Sources go in the description.
- Sameness (R5): this is a ladder with a death-count game mechanic and a trench-wall descent, not a "never want to meet X" dossier; it shares no VO lines with the sibling Short.
