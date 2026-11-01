---
id: explainer-never-meet-orca
niche: explainer
format: long-form 16:9 (1920x1080)
title: "Orcas Could Hunt You. They Decided Not To."
alt_titles:
  - Why Orcas Have Never Hunted You
  - The Sea Animal Called "Killer" That Has Never Killed You
  - Why You'd Never Want To Meet An Orca
title_note: "Distinct from the 9:16 pilot episodes/explainer-orca ('Why You'd Never Want To Meet An Orca'), so the channel never carries two uploads with the same title. If both go out, the Short is described as a cut-down of this video. See titles.md."
series_formula: "THREAT FILE series (6-tab dossier on one animal); title leads with the could-vs-did paradox (VtrcKTkhDHU title pattern) instead of copying Depth Theory's 'Why you'd never want to meet X'"
target_runtime: "9:00-10:00 (this version: 9:58.8 including a 1.6 s end hold)"
target_words_per_min: "160-170 while speaking (this version: 1526 words, 163.1 wpm while speaking, 152.9 wpm over the whole runtime)"
timing_source: "Every timestamp below comes from Kokoro-82M am_michael line renders measured on the Spark CPU (tts_durations.json): speed 0.96 for the body, 0.84 for the hook, 0.88 for the bookend and CTA. Shots start 0.12 s before the word they illustrate. Re-snap after the final mix by rerunning gen_storyboard.py on the mix's captions.json."
voice: Kokoro am_michael on the Spark CPU, calm-dry narrator; hook at speed 0.84 (~160 wpm), bookend + CTA at 0.88 (~147 wpm), body 0.96
music: deep_ocean bed ducked under the VO; drop to silence after "Then it all goes quiet", under the master question, and at the climax verdict; jokes and comic SFX retired from the villain swap on
references:
  - id: fGcgWaswMns
    url: https://www.youtube.com/watch?v=fGcgWaswMns
    title: Why You'd Never Want To Meet A Sperm Whale (Depth Theory)
    views: 2307237
    outlier_score: 14.65
    why_chosen: Same flat-2D kit style and the dossier template we follow for structure (immersion hook with a felt clue closed by callback, rival concession, capability ladder, re-immersion, numbered options killed by callbacks, twist, villain swap, bookend, comment CTA). We borrow its structure and devices only; every sentence frame flagged in review was rewritten.
  - id: VtrcKTkhDHU
    url: https://www.youtube.com/watch?v=VtrcKTkhDHU
    title: Why The Ocean's Deadliest Predator Refuses To Kill Us (OctoLab)
    views: 8289332
    outlier_score: 318.82
    why_chosen: Same subject and master paradox (apex killer, zero wild human deaths). We borrow the why-question on a black frame, the hook list paid in order as a table of contents, the quiet "in the wild" qualifier paid by the captivity reversal, the you-face-to-face beat and the answer device (dismiss a misconception, then a named mechanism that pays an early plant). We do NOT borrow its stories or wording (no Pliny, no Tilikum narrative, no 1972 surfer story, no Tahlequah; beaching rewritten around the Crozet observations).
  - id: JkAcCdqYJN0
    url: https://www.youtube.com/watch?v=JkAcCdqYJN0
    title: Every Animal That Could Swallow You (Only One Actually Can) (Occam)
    views: 332151
    outlier_score: 15.82
    why_chosen: Our premise is a could-vs-has question. We borrow its per-entry verdict stamp (here one stamp per THREAT FILE tab), the could-vs-has close of a legend fake-out (Ponting 1911), the one-breath recap of every verdict on a finished board, and retiring the comedy when the answer turns sober.
demand_evidence: WILD VERSUS "This Is Why Orcas Are Called Killer Whales" 56M (83x); OctoLab VtrcKTkhDHU 8.2M (315-319x); BeyondTheBlue orca video 2.7M (9x). See backlog/explainer/TOPICS.md row 1.
originality: python3 scripts/originality_check.py backlog/explainer/explainer-never-meet-orca/script.md research/corpus research/library/transcripts -> PASS (result recorded in review.json)
sources_for_description: Towner et al. 2022 and 2024 (African Journal of Marine Science); Totterdell et al. 2022 (Marine Mammal Science); Pitman & Durban 2012; Visser et al. 2008; Deecke, Ford & Slater 2005; Guinet & Bouvier 1995; Lopez & Lopez 1985; Florida Museum ISAF; NOAA Fisheries; Center for Whale Research; Atlantic Orca Working Group (GTOA)
status: final script. Every fact in section 5 has a source; "confirmed in the critique round" = re-checked by the originality/retention reviewers; "source listed" = from the cited source, not re-read this round; CHECK = confirm before the voice is mixed.
generated_by: gen_storyboard.py renders this file from script.tmpl.md + lines.py + tts_durations.json (edit those, not this file)
---

# Orcas Could Hunt You. They Decided Not To. (long-form explainer)

**Premise.** The one sea animal with "killer" in its name has no recorded human kill in the wild. We open its six-tab THREAT FILE (body, speed, planning, wave-washing, great whites emptied for their livers, blue whales), use those facts to kill every escape move, then turn it: the pod under your kayak checked you and decided you are not food. The hook's quiet "in the wild" is paid by the only human deaths, all in marine parks, and the villain swap (we are its only predator). The last line keeps the threat alive: you are safe because of a family habit, in an animal that picks up new habits.

**Master question (spoken at 0:38.9, 6%, on a black frame; re-armed at 5:25.5, "a strange exception"):** why has an animal built for killing never picked you? **Progress device:** a six-tab THREAT FILE chip, on screen from 0:43.4 for the whole ladder; one tab lights per rung and gets a verdict stamp at its seam; the bookend recaps all six on the finished board.

## 1. Beat alignment

Our timestamps are measured Kokoro times (see front matter). Reference timestamps were re-checked against the annotated corpus files in `research/corpus/explainer/`.

| Our beat | Our timestamp | Reference id + timestamp | Device borrowed | How we adapt it |
|---|---|---|---|---|
| L1 Hook: calm 2P scene, checklist, rule, felt clue, creature named last | 0:00-0:30.9 | fGcgWaswMns 0:00-0:29 (checklist 0:04-0:07, rule 0:09, sensation 0:14, named 0:23) | H1 calm scene + broken rule + unexplained sensation, subject named at ~80% of the hook | Kayak, not a dive. Checklist is sea + life jacket (no "sharks are rare" frame). The clue is a sound through the hull that stops. Named at 0:25.8 (85% of the hook). Ends on "deciding something about you", a new frame. Hook = 73 words |
| L1 paradox + quiet qualifier | 0:07.5 | VtrcKTkhDHU 0:21 ("in the wild" qualifier) | H6 paradox with a planted loophole | "With killer in its name ... in the wild" plants both the name myth-bust (1:31.5) and the villain swap (8:16.7) |
| L2 Rival conceded in one line | 0:30.9 | fGcgWaswMns 0:29-0:43 (rival concession -> pivot) | Concession then pivot | Sharks' bite tally vs the orca's zero, one line (was three) |
| L2 Master question on black | 0:38.9 (6%); re-armed 5:25.5 | VtrcKTkhDHU 0:32 (why-question on a black frame), 9:05 (absolute line re-arms it) | Spoken paradox question by ~0:40, held on black | "So why has an animal built for killing never picked you?" Re-armed after the blue whale with "your seventy-odd kilos ... a strange exception" |
| L2 Three credentials as table of contents, paid in order | 0:43.4 | VtrcKTkhDHU 0:09 (power list paid 7:11 / 8:18 / 23:44); fGcgWaswMns 0:45-0:53 (credential stack, last a teaser) | Hook list doubles as the TOC; each item paid in order | 1 beach raids -> paid 2:49.3 (28%); 2 great whites without livers -> 3:50.4 (38%); 3 largest animal ever -> 4:54.3 (49%) |
| L3 Promise + progress device | 0:55.4; chip on screen from 0:43.4 | fGcgWaswMns 0:58 (promise); JkAcCdqYJN0 0:14-0:20 (scoring rule, first entry) | Promise line; visible progress device before rung 1 | Big THREAT FILE folder shrinks into the corner chip; tab one opens at 0:59.7 |
| Per-tab verdict stamps + finished board | each tab seam; recap 9:26.0 | JkAcCdqYJN0 7:01 (per-entry "time inside" stamp), 8:37 (one-breath recap of every verdict) | Each entry ends on a stamp; the end recaps them all | BODY: YOU LOSE, SPEED: NO CONTEST, PLAN: IT THINKS AHEAD, WAVE: NOWHERE IS SAFE, SHARKS: EVEN THEY LEAVE, GIANTS: NO UPPER LIMIT; all six land again on their words in the bookend |
| L4 Tab 1 Body | 0:59.4-1:40.8 | fGcgWaswMns 1:02-1:50 (numbers -> everyday objects 1:12, body comparison 1:33, punch 1:47); VtrcKTkhDHU 2:04 ("not even whales") | Every number gets a comparison; short punch; small "you assumed wrong" | Our own anchors: two family cars long / four cars heavy, fin as tall as you, tooth longer than your credit card. Punch is HOLD / TEAR / SWALLOW on screen inside a longer sentence. Name myth-bust with the false/pygmy killer whale joke |
| L5 Tab 2 Speed | 1:40.8-2:10.0 | fGcgWaswMns 1:50-1:56 (RQ -> one-word answer), 2:49 (its number vs yours) | RQ micro loop; you-vs-it number | "Could you outswim one? No." 56 km/h = the speed you drive through town; 130 kg on a big day > you; "never ordered one" (paid at 8:02.2) |
| L5 Tab 3 Plan: ecotypes, silence, teaching | 2:10.0-3:06.7 | VtrcKTkhDHU 9:14 (muscle -> mind pivot), 10:00-10:41 (beaching taught); fGcgWaswMns 3:45 (hook clue closed by callback) | Shift from muscle to mind; close the felt clue by callback | Fish eaters click freely (plant for the ship-noise threat), mammal hunters hunt by listening (plant for climax move 3); clue closed at 2:40.8 (27%); beaching told through the Crozet observations (mothers push calves, calves rehearse on empty beaches) |
| L5 Tab 4 Wave + re-immersion | 3:06.7-3:48.0 | VtrcKTkhDHU 9:34-9:46 (ice-floe wave); fGcgWaswMns 4:43 ("picture it again") | Tactic as an action sequence; re-immersion | "They take a look first" (plant for the twist answer at 7:36.5); Weddell preference (plant for 7:51.7); kayak = floe at 3:40.4 (37%) |
| L5 Tab 5 Sharks (credential 2 paid) | 3:48.0-4:52.1 | VtrcKTkhDHU 7:16-7:30 (whodunit, 14 s); fGcgWaswMns 3:54 (one honest "never proven" hedge) | Mystery from the hook list closed as a dated story; one honesty hedge | Three great whites in one week (May 2017), Port and Starboard, fuel-tank joke, tonic immobility flagged unconfirmed, Starboard's 2023 solo kill of a young white vs your toothbrushing, cage-dive "you" line, "moving house" |
| L5 Tab 6 Giants (credential 3 paid) | 4:52.1-5:29.5 | VtrcKTkhDHU 8:18 (blue whale top rung), 8:48 (turn-taking tactic), 9:05 (absolute line) | Top rung with dated proof, a 3-step tactic and an absolute line | Bremer Bay 2019 adult ~20 m; "eleven of you head to toe"; bite / ram / push under; 2019 adult, 2019 calf, 2021 young; "nothing in the sea hunts it back" (paid 9:03.8) |
| L5 Proof: could vs has | 5:29.5-6:17.8 | fGcgWaswMns 5:00 (RQ "against people?"); JkAcCdqYJN0 7:06-7:30 (legend fake-out closed on could vs has) | Midpoint question, near-miss story, could-vs-has verdict | Honest "a handful of bites and bumps, no deaths" (no false "once"); Ponting 1911 told as the closest call; "his ice vs your hull" you-line; "Could it? Clearly. Has it? ... zero." |
| L6 Climax: four moves, each killed by an earlier tab | 6:17.8-7:01.5; verdict 6:57.5 | fGcgWaswMns 5:59-7:01 (options killed by callbacks 6:10-6:49; verdict 7:01 = 70%) | Numbered options, each struck by an earlier rung, then an absolute verdict | 1 swim -> tab 2; 2 climb -> tab 4; 3 dive -> tab 3 ("they hunt by listening"); 4 play dead -> tab 5 (hedged "if the theory is right"). Verdict frame is our own ("the outcome is not up to you") at 69% |
| L7 Twist: no wild pod has made that pick | 7:01.5-7:25.1 | fGcgWaswMns 7:13 (they almost never come after people); VtrcKTkhDHU 20:42-21:07 (you face to face, anticlimax) | Reversal right after the darkest verdict; 2P face-to-face beat | Iberian rudder pods leave the crews unhurt (plant for the closing sting); "You're slow, soft, and floating in their kitchen, and still they swim past" |
| L7 Twist answer | 7:25.1-8:16.7 | VtrcKTkhDHU 21:23-22:14 (dismiss a misconception -> named mechanism that pays an early plant -> the animal's verdict voiced) | Misconception, mechanism, verdict | Sharks bite people by mistake (a person on a board looks like a seal from below); orcas check first (pays 3:12.8); culture decides the menu (pays 3:18.4 Weddell and 2:05.0 "never ordered"); silence re-read as "silent while they look, chatty once they've decided" (ties tab 3's "quiet is an orca at work"); verdict "They checked, and you weren't food." |
| L7 Villain swap | 8:16.7-9:09.8 | VtrcKTkhDHU 25:36 (captivity pays "in the wild"), 31:00-31:44 (present threats); fGcgWaswMns 8:00 (before/after number), 8:22 (three modern threats); JkAcCdqYJN0 7:37 + 8:23 (comedy retired, unjoked beat) | Loophole payoff; harm runs the other way; before/after number; three threats; no jokes | Four captive deaths as one sober stat (no names, no retelling); Puget Sound captures; Southern Residents ~98 (1995) -> ~75 today = one school bus; salmon / ship noise (pays the "clicks" plant) / PCBs; "Nothing in the sea hunts the orca. The closest thing it has to a predator is us." |
| L8 Bookend | 9:09.8-9:52.2 | fGcgWaswMns 9:29-9:44 (opening rule restated, callbacks); JkAcCdqYJN0 8:37 (one-breath recap) | Return to the opening image; restate the rule; recap; end on an image | Same kayak frame; the squeaking returns (they decided); "The rule you paddled out with still holds. In the wild, zero."; six-tab recap in one breath; title line, then the sting: safe because of a habit, in an animal that keeps picking up new ones (callback to the Iberian rudder habit); last image a single fin rising |
| L9 CTA | 9:52.2 | fGcgWaswMns 9:47-9:52 (comment prompt naming the next creature); PLAYBOOK §6 | One comment prompt under 15 s | Two-way choice that names the next files: "leopard seal or box jellyfish?" (both are in the backlog) |

### Open loops and plants

| Loop / plant | Opens | Closes | Target (PLAYBOOK) |
|---|---|---|---|
| Master question: why hasn't it come for you? | 0:38.9 (6%) | re-armed 5:25.5; answered 7:25.1-8:14.2 (83%) | spoken early, answered late (VtrcKTkhDHU) |
| Sound through the hull, then silence | 0:14.5 | callback 2:40.8 (27%); re-read 8:07.7; bookend 9:14.3 | ~35% |
| "Deciding something about you" | 0:25.8 | 8:14.2 "They checked, and you weren't food." (83%); 9:40.7 "They decided not to." | late |
| Credential 1: beach raids | 0:43.4 | 2:49.3 (28%) | first teaser by ~35% |
| Credential 2: great whites without livers | 0:43.4 | 3:50.4 (38%) | ~40-50% |
| Credential 3: largest animal ever | 0:43.4 | 4:54.3 (49%) | ~50-60% |
| Title: could hunt you | 0:55.4 | climax verdict 6:57.5 (69%); title line 9:40.7 | ~70% |
| "In the wild" | 0:07.5 | 8:16.7 (83%) | late |
| "Killer" in its name | 0:07.5 | name myth-bust 1:31.5 | plant-payoff |
| "Nothing in the sea hunts it back" | 5:21.3 | 9:03.8 (91%) | plant-payoff |
| P "never ordered one" | 2:05.0 | 8:02.2 menu card | plant-payoff |
| P "they take a look first" | 3:12.8 | 7:36.5 "Remember, they check first" | plant-payoff |
| P Weddell preference | 3:18.4 | 7:51.7 | plant-payoff |
| P mammal hunters "hunt by listening" | 2:23.4 | climax move 3 6:38.5 | plant-payoff (a true callback) |
| P fish eaters "click all day" | 2:23.4 | ship noise drowns the clicks 8:53.5 | plant-payoff |
| P tonic immobility (unconfirmed) | 4:20.9 | move 4 6:47.3, still hedged | plant-payoff |
| P Iberian pods: a new habit since 2020 | 7:05.0 | closing sting 9:44.2 | plant-payoff |

## 2. Pacing self-check (PLAYBOOK §8 targets; measured, not modelled)

| Metric | Target | This version | Pass? |
|---|---|---|---|
| Runtime | 8-10 min | 9:58.8 | yes |
| Words / wpm while speaking | ~1,500-1,650 / 160-170 | 1526 / 163.1 | yes |
| Hook | 70-90 word immersion hook, creature named at ~80% | 73 words / 0:00-0:30.9; "orcas" at 0:25.8 (85% of the hook) | yes |
| Progress device / first rung | by 45 s (corpus median 46 s, range 8-78 s) | chip on screen 0:43.4; first tab 0:59.7 | device yes; first rung 14 s late (accepted: the spoken master question and the three-item TOC sit before it, as fGcgWaswMns does to 1:02) |
| Setup share (L1-L3) | 8-10% | 10% | yes |
| "You" in sentences / words | >=25% / >=3% | 30.1% / 3.1% | yes |
| Average sentence | 10-13 words with 1-3 word punches | 11.5 words; kept punches: "No." "Smart." "It plans." "It's served." "Look familiar?" "Clearly." | yes |
| Numbers per minute | 3-5, each with a comparison | ~5.4 by the crude counter (it also counts "one"/"four" in "four moves", "Tab one"); every hard number has a comparison | borderline |
| Re-hook | reset ~20 s, verbal re-hook ~30 s, new rung 40-70 s | a shot change every 4.6 s on average (130 shots); verbal re-hooks at 0:38.9, 0:55.4, 1:40.8, 2:10.0, 2:40.8, 3:06.7, 3:40.4, 3:48.0, 4:52.1, 5:25.5, 5:29.5, 6:17.8, 7:01.5, 7:25.1, 8:16.7, 9:09.8; rungs run 31-64 s | yes |
| Comic deflation | every 60-90 s until the villain swap | pygmy killer whale 1:31.5, never ordered 2:05.0, served 3:34.5, fuel tank 4:15.4, moving house 4:46.1, eleven of you 5:04.9, delivery 6:22.9, ask its liver 6:47.3, menu 8:02.2; none after 8:16.7 | yes (one 97 s gap, 4:46.1-6:22.9) |
| Climax verdict | dossier 60-75% | 69% | yes |
| Re-immersion ("picture it again") | ~47% | 37% | early; kept because it lands right after the floe it rhymes with |

## 3. Script (voiceover = burned-in captions)

Hook first line: **"You're in a sea kayak on cold, glassy water."** (9 words; the checklist starts at 0:04.0)
Hook first visual: **the yellow kayak with the seated stick-figure YOU at the left third of a dusk waterline, three black dorsal fins 130 px tall (12% of the frame) mid-distance right from frame 1; the nearest fin sinks at ~2.3 s.**

### L1 HOOK  (0:00.3-0:30.3, 0-5%)

**[0:00.3]** You're in a sea kayak on cold, glassy water.  

**[0:04.0]** The sea is flat and your life jacket is zipped.  
  *On screen:* `SEA: FLAT ✓ · LIFE JACKET: ON ✓`

**[0:07.5]** And the one animal out here with killer in its name has never killed anyone in the wild.  
  *On screen:* `WILD HUMAN KILLS: 0`

**[0:14.5]** Then, through the thin plastic under your legs, you hear squeaks and creaks, like a rusty gate trying to sing.  

**[0:22.9]** Then it all goes quiet.  

**[0:25.8]** That quiet is a pod of orcas, deciding something about you.  
  *On screen:* `THEY'RE DECIDING SOMETHING`


### L2 REFRAME + MASTER QUESTION + CREDENTIALS  (0:30.9-0:55.0, 5-9%)

**[0:30.9]** Sharks bite around sixty to seventy people a year, unprovoked. The orca, the one called killer, sits on zero.  
  *On screen:* `SHARKS: ~60-70 BITES / YR · ORCA: 0`

**[0:38.9]** So why has an animal built for killing never picked you?  
  *On screen:* `WHY HAS IT NEVER PICKED YOU?`

**[0:43.4]** It's not that it can't. It surfs onto beaches for sea lions, leaves great whites washed up without their livers, and has taken down the largest animal that ever lived.  
  *On screen:* `1 BEACH RAIDS · 2 GREAT WHITES, NO LIVERS · 3 THE LARGEST ANIMAL EVER`


### L3 PROMISE  (0:55.4-0:59.0, 9-10%)

**[0:55.4]** So let's open its threat file, one tab at a time.  
  *On screen:* `THREAT FILE: ORCA [1 BODY] [2 SPEED] [3 PLAN] [4 WAVE] [5 SHARKS] [6 GIANTS]`


### L4 TAB 1 BODY  (0:59.4-1:40.5, 10-17%)

**[0:59.4]** Tab one, the body. A big male runs about eight metres long and weighs around six tonnes.  
  *On screen:* `~8 M · ~6 TONNES`

**[1:05.9]** That's nearly two family cars nose to tail, as heavy as four of them.  
  *On screen:* `≈ 2 CARS LONG · ≈ 4 CARS HEAVY`

**[1:11.2]** His dorsal fin alone can stand about as tall as you.  
  *On screen:* `FIN: ~1.8 M · YOU: ~1.75 M`

**[1:15.2]** Inside the mouth sit up to fifty-six cone-shaped teeth, the biggest around ten centimetres, longer than your credit card.  
  *On screen:* `40-56 TEETH · UP TO ~10 CM`

**[1:24.0]** They interlock when the jaw closes and aren't made for chewing, so you'd be held, torn and swallowed in chunks.  
  *On screen:* `HOLD · TEAR · SWALLOW`

**[1:31.5]** It isn't even a whale. It's the biggest dolphin there is, and there's also a false killer whale and a pygmy one, so somebody was nervous.  
  *On screen:* `NOT A WHALE. A DOLPHIN. · ALSO REAL: FALSE KILLER WHALE · PYGMY KILLER WHALE`


### L5 TAB 2 SPEED  (1:40.8-2:09.5, 17-22%)

**[1:40.8]** So could you outswim one? No.  
  *On screen:* `COULD YOU OUTSWIM IT?  NO.`

**[1:43.3]** In a sprint an orca hits about fifty-six kilometres an hour, the speed you'd drive through town.  
  *On screen:* `ORCA: ~56 KM/H = YOUR CAR IN TOWN`

**[1:50.0]** The fastest human swimmers manage about eight. You, in a borrowed wetsuit, maybe three.  
  *On screen:* `OLYMPIC SWIMMER: ~8 · YOU: ~3`

**[1:56.2]** All that speed burns fuel, and a big adult can eat up to about a hundred and thirty kilos on a big day, more than you weigh.  
  *On screen:* `UP TO ~130 KG / DAY > YOU`

**[2:05.0]** So you'd be a perfectly sized meal. It's just never ordered one.  
  *On screen:* `ORDERS PLACED: 0`


### L5 TAB 3 PLAN  (2:10.0-3:06.2, 22-31%)

**[2:10.0]** But speed isn't what makes it dangerous. It plans.  
  *On screen:* `IT PLANS.`

**[2:13.8]** Orcas live in family pods led by older females, and in the North Pacific some eat only fish while others eat only mammals.  
  *On screen:* `PODS · LED BY GRANDMOTHERS`

**[2:23.4]** The fish eaters chatter all day, since salmon barely hear them. Mammal hunters can't, because seals hear orca calls well, so these pods hunt in near silence, by listening.  
  *On screen:* `FISH EATERS: NOISY · MAMMAL HUNTERS: SILENT, HUNT BY EAR`

**[2:35.6]** Underwater microphones show most of their calling starts after the kill.  
  *On screen:* `CALLS: AFTER THE KILL`

**[2:40.8]** Remember the squeaking through your kayak, and then the silence?  

**[2:44.9]** Noisy is an orca off duty. Quiet is an orca at work.  
  *On screen:* `QUIET = WORKING`

**[2:49.3]** And the planning gets taught. In Argentina, orcas surf up the beach to grab young sea lions, then slide back on the next wave.  
  *On screen:* `ARGENTINA · BEACH RAIDS`

**[2:58.6]** On the Crozet Islands, mothers have been seen pushing calves up the sand, and calves rehearse on empty beaches.  
  *On screen:* `CROZET ISLANDS · BEACH SCHOOL`


### L5 TAB 4 WAVE  (3:06.7-3:47.5, 31-38%)

**[3:06.7]** In Antarctica, a seal can escape all that by hauling out onto floating ice. Smart.  
  *On screen:* `ANTARCTICA · SAFE ON ICE?`

**[3:12.8]** Except a pod swims up, lifts their heads out of the water, and takes a look first.  
  *On screen:* `THEY CHECK FIRST`

**[3:18.4]** Scientists noticed they kept choosing Weddell seals, even where others were easier to find.  
  *On screen:* `PREFERRED: WEDDELL SEAL`

**[3:24.5]** Then the pod backs off, lines up, and charges together. At the last second they dive, and their wave rolls over the floe and tips the seal in.  
  *On screen:* `WAVE-WASHING`

**[3:34.5]** If it fails, they go again. A seal on an ice floe isn't safe. It's served.  
  *On screen:* `ATTEMPT 2... 3...  NOT SAFE. SERVED.`

**[3:40.4]** Now picture your kayak again: a small flat thing on the water, with something warm on top. Look familiar?  
  *On screen:* `LOOK FAMILIAR?`


### L5 TAB 5 SHARKS  (3:48.0-4:51.6, 38-49%)

**[3:48.0]** Which brings us back to those sharks.  

**[3:50.4]** In one week in May 2017, three great whites washed up near Gansbaai, South Africa.  
  *On screen:* `GANSBAAI · MAY 2017 · 3 IN ONE WEEK`

**[3:57.2]** Each had wounds near the front fins and no liver, and at least one had lost its heart too.  
  *On screen:* `LIVER: GONE · HEART: GONE (AT LEAST 1)`

**[4:03.3]** The suspects were two local males, Port and Starboard, named for their floppy dorsal fins.  
  *On screen:* `SUSPECTS: PORT & STARBOARD`

**[4:09.8]** Why the liver? In a great white it can be a quarter of the body, and it's full of oil.  
  *On screen:* `LIVER ≈ 1/4 OF THE BODY · OIL`

**[4:15.4]** Think of it as the shark's fuel tank. The orcas take the tank and leave the car.  
  *On screen:* `TAKE THE TANK. LEAVE THE CAR.`

**[4:20.9]** Scientists suspect they flip sharks into a trance called tonic immobility, though that is still unconfirmed.  
  *On screen:* `TONIC IMMOBILITY? (UNCONFIRMED)`

**[4:28.0]** What is on film is Starboard, in 2023, killing a young great white alone in under two minutes, less time than you spend brushing your teeth.  
  *On screen:* `2023 · ONE ORCA · < 2 MIN`

**[4:38.3]** And the sharks? They left, for months at a time, so a cage dive there could mean you staring at empty water all day.  
  *On screen:* `GREAT WHITES: GONE`

**[4:46.1]** Imagine being the most feared fish in the ocean and moving house because of a dolphin.  
  *On screen:* `MOVING HOUSE`


### L5 TAB 6 GIANTS  (4:52.1-5:29.0, 49-55%)

**[4:52.1]** Think being huge would save you?  

**[4:54.3]** In March 2019, off Bremer Bay in Western Australia, more than a dozen orcas brought down an adult blue whale around twenty metres long.  
  *On screen:* `BREMER BAY · MARCH 2019 · ~20 M`

**[5:04.9]** Line up eleven of you head to toe and you'd only just match it.  
  *On screen:* `≈ 11 OF YOU`

**[5:09.2]** They took turns biting its fins and flanks and pushing it under until it gave out.  
  *On screen:* `BITE · RAM · PUSH UNDER`

**[5:14.8]** It was the first ever documented, and it has happened twice more since, both to young whales.  
  *On screen:* `2019 · 2019 · 2021`

**[5:21.3]** So size doesn't stop it, and nothing in the sea hunts it back. Which makes your seventy-odd kilos a strange exception.  
  *On screen:* `NO UPPER LIMIT · NO NATURAL PREDATOR → SO WHY NOT YOU?`


### L5 PROOF: COULD VS HAS  (5:29.5-6:17.3, 55-63%)

**[5:29.5]** So has an orca ever turned any of this on a person?  
  *On screen:* `HAS IT EVER TRIED IT ON A HUMAN?`

**[5:33.6]** A handful of bites and bumps are on record, and no deaths. The closest call is in an explorer's diary.  
  *On screen:* `BITES & BUMPS: A HANDFUL · DEATHS: 0`

**[5:41.4]** In January 1911, on Scott's Antarctic expedition, photographer Herbert Ponting walked onto the sea ice to photograph a pod.  
  *On screen:* `ANTARCTICA · JANUARY 1911`

**[5:51.5]** Seconds later the ice under him heaved and split, broken from below, the same idea as the floe trick.  
  *On screen:* `THE ICE CRACKS`

**[5:59.0]** Ponting leapt slab to slab and made it back, off ice thick enough to hold sled dogs. You'd have a few millimetres of plastic.  
  *On screen:* `HE MADE IT · HIS ICE vs YOUR HULL`

**[6:07.8]** Were they after him, his dogs, or a dark shape on the ice? Nobody knows.  
  *On screen:* `HIM? THE DOGS? A SHAPE?`

**[6:13.2]** Could it? Clearly. Has it? Wild orcas, human deaths: zero.  
  *On screen:* `COULD: YES · HAS: 0`


### L6 CLIMAX: FOUR MOVES  (6:17.8-7:00.6, 63-70%)

**[6:17.8]** Still, run the thought experiment. A pod has picked you, and you get four moves.  
  *On screen:* `YOUR FOUR MOVES: 1 SWIM · 2 CLIMB · 3 DIVE · 4 PLAY DEAD`

**[6:22.9]** One, swim for it: fifty-six against your three. That's not a race, it's a delivery.  

**[6:28.8]** Two, climb onto something, a rock, a buoy, your flipped kayak. You've seen what they do to things on top of the water. Up there, you're the seal.  

**[6:38.5]** Three, dive and hide. Remember, they hunt by listening, and you kicking down on burning lungs are exactly the noise they want.  
  *On screen:* `THEY HUNT BY EAR`

**[6:47.3]** Four, play dead. If the theory is right, that's roughly what a flipped great white does. Ask its liver how that went.  
  *On screen:* `ASK THE LIVER`

**[6:55.3]** Four moves, four losses. Once a pod picks you, the outcome is not up to you.  
  *On screen:* `ONCE IT PICKS YOU, IT'S NOT YOUR CALL.`


### L7 TWIST: THEY CHECKED  (7:01.5-8:16.1, 70-83%)

**[7:01.5]** And yet no wild pod has ever made that pick.  
  *On screen:* `AND YET: 0`

**[7:05.0]** Off Spain and Portugal since 2020, some pods have rammed sailboats and snapped off their rudders, and a few boats sank.  
  *On screen:* `IBERIA · SINCE 2020 · RUDDERS`

**[7:13.6]** Even then they swim off once the rudder's gone, and nobody aboard has been seriously hurt.  
  *On screen:* `BOATS SUNK: A FEW · PEOPLE HURT: 0`

**[7:20.0]** You're slow, soft, and floating in their kitchen, and still they swim past.  

**[7:25.1]** So why? Nobody knows for certain, but two things help.  
  *On screen:* `WHY? (NOBODY KNOWS FOR SURE)`

**[7:28.7]** Shark bites on people are often thought to be mistakes, because from below, you on a board look a lot like a seal.  
  *On screen:* `SHARKS: MISTAKEN IDENTITY?`

**[7:36.5]** Orcas don't work that way. Remember, they check first, looking and listening, so that mistake is much harder to make.  
  *On screen:* `THEY CHECK FIRST`

**[7:44.4]** And what they check has to be on the family menu, because an orca eats what its grandmother taught its mother to eat.  
  *On screen:* `CULTURE`

**[7:51.7]** Fish-eating pods off Canada swim past seals without a second look, and mammal hunters learn which mammals count, like those Weddell-choosing pods.  
  *On screen:* `FISH EATERS IGNORE SEALS`

**[8:02.2]** In all those generations of handed-down menus, you have never made the list.  
  *On screen:* `MENU: SALMON · HERRING · SEAL · SHARK LIVER · YOU (never)`

**[8:07.7]** So the quiet under your kayak was a check, silent while they look and chatty once they've decided.  
  *On screen:* `QUIET WHILE CHECKING · NOISY ONCE DONE`

**[8:14.2]** They checked, and you weren't food.  
  *On screen:* `THEY CHECKED. YOU WEREN'T FOOD.`


### L7 VILLAIN SWAP  (8:16.7-9:09.1, 83-92%)

**[8:16.7]** Which leaves three words from the start: in the wild.  
  *On screen:* `"IN THE WILD"`

**[8:20.3]** Every human death ever linked to an orca happened in a marine park, with animals taken from the sea or born in tanks. There have been four.  
  *On screen:* `HUMAN DEATHS: 4 · ALL IN CAPTIVITY`

**[8:30.2]** Out in the open, the harm mostly flows from people like you and me to them.  
  *On screen:* `US → THEM`

**[8:35.3]** In the 1960s and 70s, dozens of orcas were caught or killed around Puget Sound for aquarium shows.  
  *On screen:* `1960s-70s · DOZENS TAKEN`

**[8:43.4]** The Southern Residents who live there today number about seventy-five, down from ninety-eight in 1995, roughly one school bus full.  
  *On screen:* `1995: ~98 → TODAY: ~75 ≈ 1 SCHOOL BUS`

**[8:53.5]** Their salmon is vanishing, ship noise drowns out the clicks they hunt it with, and their blubber holds some of the highest chemical loads of any marine mammal.  
  *On screen:* `SALMON ↓ · SHIP NOISE · CHEMICALS`

**[9:03.8]** Nothing in the sea hunts the orca. The closest thing it has to a predator is us.  
  *On screen:* `NO NATURAL PREDATOR. EXCEPT US.`


### L8 BOOKEND  (9:09.8-9:51.4, 92-99%)

**[9:09.8]** Back to your kayak. The water's glassy, the inlet's cold.  

**[9:14.3]** The squeaking starts up again, louder, and the pod slides by close enough to hear them breathe.  

**[9:21.1]** The rule you paddled out with still holds. In the wild, zero.  
  *On screen:* `WILD HUMAN KILLS: 0`

**[9:26.0]** But the animal passing you outsizes you, outruns you, plans ahead, washes seals off ice, empties great whites and brings down blue whales.  
  *On screen:* `FILE: 6 TABS STAMPED`

**[9:37.2]** And it just looked you over, then kept swimming.  

**[9:40.7]** Orcas could hunt you. They decided not to.  
  *On screen:* `THEY DECIDED NOT TO.`

**[9:44.2]** And the only thing keeping you off that menu is a habit, in an animal that keeps picking up new ones.  
  *On screen:* `YOU'RE SAFE BECAUSE OF A HABIT.`


### L9 CTA  (9:52.2-9:57.2, 99-100%)

**[9:52.2]** Next file: leopard seal or box jellyfish? Pick one in the comments.  
  *On screen:* `NEXT FILE: LEOPARD SEAL or BOX JELLYFISH?`


## 4. Shot list (130 shots)

Generated from `gen_storyboard.py` (one function per shot; the same code writes `storyboard.json`). Kit vocabulary from `studio/src/kits/explainer/README.md`. NEW S = an inline-SVG prop written into the storyboard (no kit change). The THREAT FILE chip is an inline-SVG layer the generator adds to every scene from 0:43.4 to the end of the climax; a tab-light is a second chip layer that pops on the tab's word. 47 long scenes also get camera re-frame keyframes every <= 2.6 s so no hold exceeds 3 s; those should get a real state change in the first render review.

| # | t_start | t_end | dur | shot type | visual (kit vocabulary; NEW S = inline SVG in the storyboard) | camera | SFX |
|---|---|---|---|---|---|---|---|
| 1 | 0:00.0 | 0:03.9 | 3.9 | WIDE | Dusk surface (Ocean surface 0.5). NEW S Kayak + seated YOU at left third, big enough to read; three black dorsal fins mid-distance right, 130 px tall (12% of frame) from frame 1; the nearest fin sinks at ~2.3 s | drift | underwater_rumble bed |
| 2 | 0:03.9 | 0:07.4 | 3.5 | MED | Same kayak, closer; green-tick Tags SEA: FLAT then LIFE JACKET: ON land on their words; two fins hold far right | pushIn | tick x2 |
| 3 | 0:07.4 | 0:14.4 | 7.0 | MED | Fins glide closer from the right; Stat 0 WILD HUMAN KILLS pops on 'never'; small Tag IN THE WILD under it on 'wild' | static | pop on the 0 |
| 4 | 0:14.4 | 0:18.0 | 3.6 | CU | Split waterline: YOU in the kayak above; below, the hull from underneath | pushIn |  |
| 5 | 0:18.0 | 0:22.8 | 4.8 | CU | White sound rings ripple up into the hull on 'squeaks'; Tag SQUEAK · CREAK | static | sonar_ping pitched up x3 |
| 6 | 0:22.8 | 0:25.7 | 2.9 | CU | Rings stop; the fins are gone from the surface; Ocean rays dim | static | all audio ducks to silence 1.0 s |
| 7 | 0:25.7 | 0:30.7 | 5.1 | REVEAL | Cut below: three Orca glide beneath the kayak's shadow (first full reveal); red Headline THEY'RE DECIDING SOMETHING on 'deciding' | pullOut | whoosh_long + stinger |
| 8 | 0:30.7 | 0:35.1 | 4.3 | INFO | GreatWhite enters left beside a small YOU; Tag ~60-70 BITES / YEAR (ISAF) on 'sixty' | panRight | whoosh |
| 9 | 0:35.1 | 0:38.8 | 3.7 | INFO | Orca slides in, Tag KILLER WHALE stamps across it, Stat 0 pops on 'zero' | pushIn | impact light |
| 10 | 0:38.8 | 0:43.3 | 4.5 | PUNCH | Master question on a hard black frame, white with red YOU, held through the 1 s pause | static | music drops out |
| 11 | 0:43.3 | 0:45.2 | 1.9 | CARD | 'It's not that it can't.' over the dark card; THREAT FILE corner chip slides in top-right and stays for the whole ladder | static | click |
| 12 | 0:45.2 | 0:48.0 | 2.8 | CARD | Credential 1: beige beach strip, Orca sliding up the sand toward a Seal; Tag 1 BEACH RAIDS | static | pop |
| 13 | 0:48.0 | 0:51.2 | 3.2 | CARD | Credential 2: grey GreatWhite on its back on the sand, red Liver glow then empty; Tag 2 GREAT WHITES, NO LIVERS | pushIn | pop |
| 14 | 0:51.2 | 0:55.3 | 4.1 | CARD | Credential 3: BlueWhale silhouette fills the frame, a cluster of tiny Orca icons at its flank; Tag 3 THE BIGGEST ANIMAL EVER | pullOut | pop |
| 15 | 0:55.3 | 0:59.3 | 4.0 | CARD | Progress device: big THREAT FILE folder, six empty tabs 1 BODY .. 6 GIANTS; shrinks into the corner chip at the end | static | whoosh + click |
| 16 | 0:59.3 | 1:05.8 | 6.5 | SCALE | Tab 1 lights on the chip; Orca at true scale (pxPerM 120); ScaleBar ~8 M grows on 'eight'; Tag ~6 TONNES on 'six' | panRight | whoosh |
| 17 | 1:05.8 | 1:09.0 | 3.2 | SCALE | Same pxPerM: two Car figures nose to tail under the Orca (2 x 4.5 m vs 8 m) | static | pop x2 |
| 18 | 1:09.0 | 1:11.1 | 2.1 | SCALE | Balance: Orca on the left, a Car drops on the right, Tag x4 CARS ≈ 6 T; beam settles level | static | ding |
| 19 | 1:11.1 | 1:15.1 | 3.9 | SCALE | Honest true scale (300 px/m): NEW S dorsal-fin cut-out 1.8 m beside YOU 1.75 m on one baseline; Tags with heights | pushIn | ding |
| 20 | 1:15.1 | 1:19.2 | 4.1 | INFO | Orca head-on (pose head); Stat counts up to 56 TEETH (MAX) on 'fifty-six' | pushIn | tick on count end |
| 21 | 1:19.2 | 1:23.9 | 4.7 | CU | True scale (4500 px/m): NEW S cone tooth 10 cm beside a credit card 8.6 cm; Tags | static | click |
| 22 | 1:23.9 | 1:28.0 | 4.1 | CU | Two NEW S tooth rows slide together and lock on 'interlock'; Tag INTERLOCKING | static | click sharp |
| 23 | 1:28.0 | 1:31.4 | 3.4 | PUNCH | Black flash, three red words punch in on their words: HOLD · TEAR · SWALLOW | shake small x3 | impact x3 |
| 24 | 1:31.4 | 1:35.4 | 4.0 | INFO | Orca with a red tag WHALE? struck through on 'whale', then DOLPHIN (THE BIGGEST) on 'dolphin' | static | whoosh |
| 25 | 1:35.4 | 1:40.7 | 5.3 | JOKE | Two smaller grey dolphins shuffle in with name tags FALSE KILLER WHALE / PYGMY KILLER WHALE; YOU shrugs on 'nervous'; seam stamp BODY: YOU LOSE | static | pop; stamp tick |
| 26 | 1:40.7 | 1:43.2 | 2.5 | CARD | Tab 2 lights; Headline COULD YOU OUTSWIM IT?; red NO. fills the frame on 'No' (held >= 0.8 s) | static | tick; impact |
| 27 | 1:43.2 | 1:49.8 | 6.6 | INFO | SpeedBars row ORCA ~56 km/h fills red; then a Car and an Orca cruise side by side past a 50 sign on 'speed' | static | whoosh |
| 28 | 1:49.8 | 1:56.1 | 6.3 | INFO | SpeedBars: ORCA 56, OLYMPIC SWIMMER 8 on 'eight', YOU 3 on 'three'; YOU pose=panic beside the last bar | static | pop x2 |
| 29 | 1:56.1 | 2:03.2 | 7.1 | INFO | Stat counts 0 -> 130 KG on 'hundred' (label FOOD ON A BIG DAY) | pushIn | tick on count end |
| 30 | 2:03.2 | 2:04.9 | 1.7 | INFO | Two bars: FOOD / BIG DAY ~130 KG vs YOU ~75 KG | static | ding |
| 31 | 2:04.9 | 2:09.9 | 5.0 | JOKE | NEW S diner order slip: SALMON/HERRING/SEAL/SHARK ticked, HUMAN empty; red stamp NEVER ORDERED on 'never'; seam stamp SPEED: NO CONTEST | static | stinger light |
| 32 | 2:09.9 | 2:12.2 | 2.3 | MED | Tab 3 lights; camera keyframes push from 1x to 2.6x onto the Orca's eye | push to eye (keyframes) | riser short |
| 33 | 2:12.2 | 2:13.7 | 1.5 | PUNCH | Red IT PLANS. on black (>= 0.8 s) | static | impact |
| 34 | 2:13.7 | 2:17.7 | 3.9 | WIDE | Pod of five Orca cruising, one large female in front, calves small; dotted family-tree lines link them; Tag PODS · LED BY GRANDMOTHERS on 'older' | panRight | underwater_rumble |
| 35 | 2:17.7 | 2:23.3 | 5.6 | SPLIT | Split screen with a wall: left pod + FISH icons, right pod + seal icons; Tag FISH EATERS | MAMMAL HUNTERS (North Pacific) | static | click x2 |
| 36 | 2:23.3 | 2:27.6 | 4.3 | ACTION | Fish eaters: two Orca with busy sound rings, FISH icons drift on unbothered; Tag FISH EATERS: NOISY | static | sonar_ping chirps |
| 37 | 2:27.6 | 2:35.5 | 7.9 | ACTION | Stalking pod: their sound rings go dark; a Seal on the right; Tag MAMMAL HUNTERS: SILENT on 'silence', then HUNT BY EAR + ear icon on 'listening' | panLeft | sonar_ping fades out |
| 38 | 2:35.5 | 2:40.7 | 5.2 | INFO | ECG trace as a hydrophone strip: flat, red KILL marker, then busy calls; Tag CALLS: AFTER THE KILL | static | static burst at the marker |
| 39 | 2:40.7 | 2:44.8 | 4.1 | CALLBACK | Return to the hook hull frame: rings ripple, then stop dead on 'silence' | pushIn | sonar_ping x1 then silence |
| 40 | 2:44.8 | 2:49.2 | 4.4 | PUNCH | Two-line card: NOISY = OFF DUTY (green), then QUIET = AT WORK (red) on 'Quiet' | static | heartbeat_slow x2 |
| 41 | 2:49.2 | 2:52.3 | 3.1 | MAP | Map world -> South America (zoom 3), pin Peninsula Valdes (-64.0,-42.5); Tag ARGENTINA | static (map zoom) | click |
| 42 | 2:52.3 | 2:58.5 | 6.2 | ACTION | Side view: beige beach strip with foam; Orca surges up the sand to a Seal (sea lion stand-in), then slides back out on 'slide'; credential 1 tick | panRight | whoosh_long |
| 43 | 2:58.5 | 3:00.3 | 1.8 | MAP | Map pin Crozet Islands (51.0,-46.4) at zoom 3; Tag CROZET ISLANDS | static | click |
| 44 | 3:00.3 | 3:03.6 | 3.3 | MED | A big Orca nudges a small Orca up the same beach; dotted practice arrow | static | pop |
| 45 | 3:03.6 | 3:06.6 | 3.0 | MED | The calf alone rehearsing on an empty beach (no prey); Tag BEACH SCHOOL; seam stamp PLAN: IT THINKS AHEAD | static | stamp tick |
| 46 | 3:06.6 | 3:12.7 | 6.1 | WIDE | Tab 4 lights; icy palette; ice floe (reused pilot ICE markup) on the waterline, a Seal hauls up onto it; Tag ANTARCTICA | pullOut | underwater_rumble |
| 47 | 3:12.7 | 3:18.2 | 5.5 | MED | Two Orca spy-hop (rotated vertical, heads above the waterline) beside the floe; Tag THEY CHECK FIRST on 'look' | pushIn | bubbles |
| 48 | 3:18.2 | 3:24.4 | 6.2 | INFO | Three seal cards (one Seal figure tinted three greys) WEDDELL / CRABEATER / LEOPARD; red ring stays on WEDDELL | static | click |
| 49 | 3:24.4 | 3:28.4 | 4.0 | ACTION | Side view: four Orca abreast (same scale) back off left, then charge the floe left to right on 'charges' | panRight | whoosh_long |
| 50 | 3:28.4 | 3:34.4 | 6.0 | ACTION | Orcas dip below; NEW S wave crest band sweeps over the floe; the Seal slides off into the water; Tag WAVE-WASHING | shake medium x1 | impact + bubbles |
| 51 | 3:34.4 | 3:36.4 | 2.0 | ACTION | Pod resets; corner Tags ATTEMPT 2 -> ATTEMPT 3 on 'again' | static | tick x2 |
| 52 | 3:36.4 | 3:40.3 | 3.9 | PUNCH | Empty floe, red stamp NOT SAFE. SERVED. on 'served' | static | stinger light |
| 53 | 3:40.3 | 3:46.1 | 5.9 | CALLBACK | Re-immersion (~36%): the hook kayak on the same icy-to-dusk waterline; four fins line up in the distance | pushIn | heartbeat x3 |
| 54 | 3:46.1 | 3:47.9 | 1.8 | PUNCH | Hard cut: floe+seal (left) and kayak+YOU (right) with the same dashed outline; Headline LOOK FAMILIAR?; seam stamp WAVE: NOWHERE IS SAFE | static | impact |
| 55 | 3:47.9 | 3:50.3 | 2.4 | CARD | Tab 5 lights; GreatWhite crosses the frame | panRight | whoosh |
| 56 | 3:50.3 | 3:57.1 | 6.8 | MAP | Map South Africa (zoom 3.5), pin Gansbaai (19.35,-34.58); Tags MAY 2017 and 3 GREAT WHITES IN ONE WEEK on 'three' | pushIn (map zoom) | drone |
| 57 | 3:57.1 | 4:03.1 | 6.1 | INFO | Grey GreatWhite belly-up; NEW S liver overlay (kit Liver) flashes red then empties on 'liver'; small HEART icon fades on 'heart' (at least one) | static | click x2 |
| 58 | 4:03.1 | 4:09.6 | 6.5 | INFO | Mugshot frames: two Orca silhouettes with NEW S bent-fin overlays (left / right) and height lines; name tags on their words | static | pop x2 |
| 59 | 4:09.6 | 4:15.3 | 5.6 | INFO | GreatWhite cutaway; kit Liver scaled to ~25% of the body in yellow-red; oil-drop on 'oil'; Tag LIVER ≈ 1/4 OF THE BODY | pushIn | ding |
| 60 | 4:15.3 | 4:20.8 | 5.5 | JOKE | Kit Car with its fuel cap open; an Orca swims off with a NEW S yellow jerrycan in lockstep; Tag TAKE THE TANK. LEAVE THE CAR. | static | whoosh |
| 61 | 4:20.8 | 4:27.9 | 7.1 | INFO | GreatWhite rolls 180 degrees (rotate keyframe); Tag TONIC IMMOBILITY? on 'tonic', yellow UNCONFIRMED on 'unconfirmed' (honesty hedge) | static | underwater_rumble |
| 62 | 4:27.9 | 4:35.1 | 7.2 | INFO | Timer ring 0:00 -> 1:59 runs fast beside an Orca and a smaller young GreatWhite (~2.5 m); Tag 2023 · ONE ORCA · < 2 MIN | static | clock_ticking then stinger |
| 63 | 4:35.1 | 4:38.2 | 3.0 | INFO | YOU with a NEW S toothbrush; the same Timer ring reads 2:00; Tag LESS THAN YOUR TOOTHBRUSHING | static | ding |
| 64 | 4:38.2 | 4:41.3 | 3.1 | MAP | Map pin Gansbaai; three shark icons fade out one by one; Tag GREAT WHITES: GONE on 'left' | pullOut | whoosh reverse |
| 65 | 4:41.3 | 4:45.9 | 4.7 | MED | NEW S shark cage with a Diver (YOU) inside, empty blue water; Tag SIGHTINGS: 0 | static | bubbles |
| 66 | 4:45.9 | 4:52.0 | 6.0 | JOKE | GreatWhite with a NEW S cardboard box strapped on (lockstep keyframes) swims off left; Tag MOVING HOUSE; seam stamp SHARKS: EVEN THEY LEAVE | panLeft | pop; stamp tick |
| 67 | 4:52.0 | 4:54.2 | 2.2 | CARD | Tab 6 lights; Headline THINK BEING HUGE WOULD SAVE YOU? | static | riser short |
| 68 | 4:54.2 | 4:59.0 | 4.8 | MAP | Map Australia (zoom 3), pin Bremer Bay (119.4,-34.4); Tag MARCH 2019 | static (map zoom) | click |
| 69 | 4:59.0 | 5:04.8 | 5.8 | SCALE | BlueWhale drawn at 20 m (its pxPerM = 80 x 20/28) with 12 small Orca at 80 px/m swarming; ScaleBar ~20 M on 'twenty' | panRight | underwater_rumble + impact |
| 70 | 5:04.8 | 5:09.1 | 4.3 | SCALE | Same whale scale; eleven YOU figures lying head to toe beneath it pop in left to right; Tag ≈ 11 OF YOU | static | pop x11 (soft) |
| 71 | 5:09.1 | 5:14.6 | 5.6 | ACTION | Three-step tactic on the whale: Tags BITE (fins) on 'biting', FLANKS on 'flanks', PUSH UNDER on 'pushing' as the whale is pressed down | static | impact x3 |
| 72 | 5:14.6 | 5:21.2 | 6.6 | INFO | Three tally cards stamp in: 2019 ADULT on 'first', 2019 CALF on 'twice', 2021 YOUNG on 'young' | static | click x3 |
| 73 | 5:21.2 | 5:25.4 | 4.2 | INFO | Orca centred; GreatWhite, BlueWhale and SpermWhale icons ring it with grey crosses; Headline NO UPPER LIMIT, Tag NO NATURAL PREDATOR on 'nothing' | static | click x3 |
| 74 | 5:25.4 | 5:29.4 | 4.0 | PUNCH | A small YOU with Tag ~75 KG; red Headline SO WHY NOT YOU? (master question re-armed); seam stamp GIANTS: NO UPPER LIMIT | pushIn | stinger soft |
| 75 | 5:29.4 | 5:33.5 | 4.1 | CARD | Red Headline HAS IT EVER TRIED IT ON A HUMAN? over a dark frame; chip shows all six tabs lit | pushIn | drone |
| 76 | 5:33.5 | 5:37.8 | 4.4 | INFO | Tag BITES & BUMPS: A HANDFUL; Stat 0 DEATHS on 'deaths' | static | pop |
| 77 | 5:37.8 | 5:41.3 | 3.4 | STORY | NEW S sepia diary page dated Jan. 1911 opens; warm paper background | pushIn | breath |
| 78 | 5:41.3 | 5:51.4 | 10.1 | STORY | Sepia: a distinct sepia figure with a box camera on tripod (NOT the YOU icon) on a white ice sheet; dark fins beyond; Tag 2 SLED DOGS NEARBY; Tag ANTARCTICA · JANUARY 1911 | drift | breath |
| 79 | 5:51.4 | 5:56.1 | 4.7 | ACTION | The ice sheet splits into three slabs on 'split'; dark Orca backs rise under the cracks; heavy shake | shake heavy x2 | impact + boom |
| 80 | 5:56.1 | 5:58.9 | 2.8 | CALLBACK | Small callback inset: the floe + wave crest from R4 (reused markup); Tag REMEMBER THE FLOE | static | whoosh |
| 81 | 5:58.9 | 6:01.9 | 3.0 | ACTION | The sepia figure hops across three slabs toward safety; Tag HE MADE IT | panLeft | whoosh x3 |
| 82 | 6:01.9 | 6:07.7 | 5.8 | SCALE | Split comparison: a thick sea-ice slab vs a thin yellow kayak hull line; Tags HIS ICE / YOUR HULL on 'You'd' | static | ding |
| 83 | 6:07.7 | 6:13.1 | 5.4 | INFO | Options list HIM? / HIS DOGS? / A DARK SHAPE?, no selection; ? stamp NOBODY KNOWS on 'Nobody' | static | click |
| 84 | 6:13.1 | 6:17.7 | 4.5 | PUNCH | Could-vs-has card: COULD IT? YES on 'Clearly', HAS IT? on 'Has', then a huge white 0 on 'zero' | static | stinger |
| 85 | 6:17.7 | 6:20.9 | 3.2 | WIDE | Top-down: NEW S top-view kayak centred in a spotlight circle; four Orca (pose top) circle it slowly | pushIn | heartbeat loop |
| 86 | 6:20.9 | 6:22.8 | 1.9 | CARD | Options YOUR FOUR MOVES, four items stagger in | static | click x4 |
| 87 | 6:22.8 | 6:28.7 | 5.9 | INFO | Option 1 selected (list left); right: SpeedBars recall ORCA 56 / YOU 3; Tag DELIVERY on 'delivery'; strike on 1 at the end | static | whoosh then strike click |
| 88 | 6:28.7 | 6:33.1 | 4.4 | INFO | Option 2 selected; right: NEW S flipped kayak on the waterline with YOU perched on top | static | click |
| 89 | 6:33.1 | 6:38.4 | 5.3 | INFO | Right: the R4 floe-and-wave replays (reused ICE + WAVE markup); on 'seal' the Seal swaps for a YOU icon; strike on 2 | static | impact; click |
| 90 | 6:38.4 | 6:40.4 | 2.0 | INFO | Option 3 selected; right: Diver sinks into darkening water (keyframes) | panDown | bubbles |
| 91 | 6:40.4 | 6:47.2 | 6.7 | INFO | Right: sound rings spread from the kicking Diver toward an Orca outline with the ear icon (R3 callback); Tag THEY HUNT BY EAR; strike on 3 | static | sonar_ping x2; click |
| 92 | 6:47.2 | 6:55.2 | 8.1 | JOKE | Option 4 selected; right: upside-down GreatWhite with the emptied Liver outline; Tag ASK THE LIVER on 'Ask'; strike on 4 | static | pop + click |
| 93 | 6:55.2 | 6:57.4 | 2.2 | CARD | All four moves struck through and held | pushIn | riser |
| 94 | 6:57.4 | 7:01.4 | 4.0 | PUNCH | Climax verdict (~69%): black card, white text, red NOT YOUR CALL | static | boom then silence |
| 95 | 7:01.4 | 7:04.9 | 3.5 | MED | Kayak again in a daylight palette; fins pass by at a distance; Stat 0 AND YET | drift | underwater_rumble bed back in |
| 96 | 7:04.9 | 7:07.7 | 2.8 | MAP | Map Iberia at detail zoom 5 (mapdetail.ts has Iberia), pin Strait of Gibraltar (-5.6, 36.0); Tag SINCE 2020 | static (map zoom) | click |
| 97 | 7:07.7 | 7:13.5 | 5.8 | ACTION | Kit Sailboat: an Orca rams it (hits), the rudder snaps off on 'snapped', the boat lists and sinks on 'sank' | static | impact (wood crack) |
| 98 | 7:13.5 | 7:19.9 | 6.4 | INFO | Orca swims away from the listing boat; NEW S life raft with two YOU icons, green tick; Tag PEOPLE SERIOUSLY HURT: 0 on 'nobody' | static | bubbles; ding |
| 99 | 7:19.9 | 7:25.0 | 5.1 | CU | Face to face: YOU in the kayak, three Tags pop SLOW / SOFT / IN THEIR KITCHEN, then three Orca glide past below on 'still' | static | pop x3; whoosh |
| 100 | 7:25.0 | 7:28.6 | 3.6 | CARD | Headline WHY? with a yellow tag NOBODY KNOWS FOR SURE; Tag 2 CLUES on 'two' | static | tick |
| 101 | 7:28.6 | 7:36.4 | 7.8 | INFO | Looking up from below: NEW S silhouettes of a person on a board and a seal side by side, a GreatWhite rising below; Tag MISTAKEN IDENTITY? | static | underwater_rumble |
| 102 | 7:36.4 | 7:44.3 | 7.9 | CALLBACK | Callback to R4: an Orca spy-hops beside your kayak, head out of the water; the same Tag THEY CHECK FIRST | pushIn | bubbles |
| 103 | 7:44.3 | 7:51.6 | 7.3 | INFO | The R3 pod family tree returns with menu cards hanging under each branch; Headline CULTURE on 'family' | pushIn | ding |
| 104 | 7:51.6 | 7:56.2 | 4.6 | ACTION | A fish-eating pod glides past a Seal with no reaction; the seal does a double take (rotate keyframes); Tag FISH EATERS IGNORE SEALS | panRight | whoosh |
| 105 | 7:56.2 | 8:02.1 | 5.9 | INFO | Recall the R4 WEDDELL select card (same layout, red ring) | static | click |
| 106 | 8:02.1 | 8:07.6 | 5.5 | JOKE | NEW S chalkboard FAMILY MENU; the YOU line gets a red strike on 'never' | static | click |
| 107 | 8:07.6 | 8:14.1 | 6.5 | CALLBACK | Hook hull frame, silent: Tag LOOKING; on 'chatty' the rings return softly with Tag DECIDED | pushIn | silence -> sonar_ping soft |
| 108 | 8:14.1 | 8:16.6 | 2.5 | PUNCH | Green stamp THEY CHECKED. YOU WEREN'T FOOD. over the YOU icon (calls back THEY CHECK FIRST) | static | ding |
| 109 | 8:16.6 | 8:20.2 | 3.6 | CARD | The hook's WILD HUMAN KILLS: 0 card returns; IN THE WILD underlines in red on 'wild' | pushIn | riser |
| 110 | 8:20.2 | 8:28.3 | 8.1 | INFO | Side-view tank cross-section (grey walls, flat water); one Orca swims back and forth, scaleX flips at each wall | static | drone |
| 111 | 8:28.3 | 8:30.1 | 1.8 | INFO | Stat 4 in red, label HUMAN DEATHS · ALL IN CAPTIVITY (one sober line, no names) | static | none |
| 112 | 8:30.1 | 8:35.1 | 5.1 | INFO | Red arrow from a YOU icon to an Orca icon; Tag US → THEM | static | whoosh |
| 113 | 8:35.1 | 8:43.2 | 8.1 | MAP | Map Pacific Northwest (zoom 3.5), pin Puget Sound (-122.5,47.6); five orca dots lifted out one by one; Tag 1960s-70s · DOZENS TAKEN | pushIn (map zoom) | click steady |
| 114 | 8:43.2 | 8:50.8 | 7.5 | INFO | Dot grid: 75 white dots (Stat 75 on 'seventy'), then 23 grey outlines appear on 'ninety-eight' (1995 peak) | static | tick |
| 115 | 8:50.8 | 8:53.4 | 2.6 | SCALE | Kit Bus labelled ONE SCHOOL BUS FULL beside the 75-dot grid shrunk to a block | static | ding |
| 116 | 8:53.4 | 8:55.3 | 2.0 | INFO | Triptych 1: salmon icons fade out one by one; Tag SALMON ↓ | static | underwater_rumble |
| 117 | 8:55.3 | 8:58.8 | 3.4 | INFO | Triptych 2: NEW S ship silhouette on the surface with noise rings scrambling an Orca's click arcs; Tag SHIP NOISE | static | static low |
| 118 | 8:58.8 | 9:03.6 | 4.9 | INFO | Triptych 3: NEW S blubber cross-section with dark specks; Tag CHEMICALS | pushIn | drone |
| 119 | 9:03.6 | 9:09.7 | 6.0 | PUNCH | Card NO NATURAL PREDATOR. then red EXCEPT US. on 'us' (pays off R6's 'nothing hunts it back') | static | stinger soft |
| 120 | 9:09.7 | 9:14.1 | 4.5 | WIDE | Exact hook frame: kayak at dusk, same composition as 0:00 | drift | underwater_rumble |
| 121 | 9:14.1 | 9:17.1 | 3.0 | CU | Hull rings return, louder (bigger, faster) | static | sonar_ping chirps |
| 122 | 9:17.1 | 9:21.0 | 3.8 | MED | Three Orca surface beside the kayak; blow puffs (white circles) on 'breathe' | panRight | breath x3 |
| 123 | 9:21.0 | 9:25.9 | 4.9 | INFO | Hook Stat WILD HUMAN KILLS: 0 returns over the kayak; Tag THE RULE HOLDS | static | tick |
| 124 | 9:25.9 | 9:37.1 | 11.2 | CARD | Finished board: the THREAT FILE folder with each tab's verdict stamp landing on its word (outsizes BODY ... blue whales GIANTS) | static | tick x6 |
| 125 | 9:37.1 | 9:38.5 | 1.4 | CU | Orca eye level with YOU, camera pushes 1x -> 1.6x and holds | pushIn | heartbeat_slow |
| 126 | 9:38.5 | 9:40.6 | 2.1 | WIDE | Fins move off toward the horizon | pullOut | whoosh_long soft |
| 127 | 9:40.6 | 9:44.1 | 3.5 | END IMAGE | Kayak alone on glassy water; lower-third Headline ORCAS COULD HUNT YOU., second line THEY DECIDED NOT TO. lands on 'They'; the last fin drops below the horizon mid-shot | static | music swell |
| 128 | 9:44.1 | 9:48.2 | 4.2 | END IMAGE | The FAMILY MENU card slides up over the water, YOU still struck; Tag A HABIT on 'habit' | static | none |
| 129 | 9:48.2 | 9:52.1 | 3.8 | END IMAGE | Sting: a snapped rudder icon (the Iberian new habit) floats by; a single fin rises behind the kayak on the last word; card YOU'RE SAFE BECAUSE OF A HABIT. | static | music cut on the last word |
| 130 | 9:52.1 | 9:58.8 | 6.7 | CARD | Threat-file folder closes; two new folders LEOPARD SEAL? and BOX JELLYFISH? slide in; end-screen slot right | static | click |

### Kit gaps, by cost tier

S = inline SVG markup in the storyboard (no code change). M = a new registered Figure. L = a new component. **M + L items: 0.** Everything below is S, or reuses an existing kit component.

| Prop | Tier | Used in | How |
|---|---|---|---|
| THREAT FILE corner chip (6 tabs, lit count) | S | 0:43.4-7:01.5 | `chip_svg(lit)` injected per scene by the generator; tab-light = a second layer with `pop` on the word |
| THREAT FILE folder (promise, finished board, CTA) | S | 0:55.4, 9:26.0, 9:52.2 | `folder_svg()`; verdict stamps are kit `Tag` layers (bg red, rotated) landing on their words |
| Kayak side view + seated YOU, top view, flipped | S | hook, 2:40.8, 3:40.4, twist, bookend, climax | three markups; the side view's waterline is at 77% of its box (`kayak_at`) |
| Dorsal fins (hook, sinking fin, last-image fin) | S | hook, 3:40.4, 7:01.5, bookend | one fin path, >= 8% of frame height |
| Hull sound rings | S | hook, 2:40.8, 8:07.7, 9:14.3, 6:38.5, 8:53.5 | core `circle` layers with scale/opacity keyframes (`ring_layers`) |
| Orca fin at true scale vs YOU | S | 1:11.2 | fin path drawn 1.8 m x 300 px/m beside kit `You` 1.75 m at `pxPerM` 300, one baseline (fixes the 1.2 m kit fin problem) |
| Tooth vs credit card, interlocking tooth rows | S | 1:15.2, 1:24.0 | true scale 4500 px/m; rows slide together on y keyframes |
| Order slip, family-menu chalkboard, strike bar | S | 2:05.0, 7:44.4, 8:02.2, 9:44.2 | text in SVG |
| Beach strip with foam | S | 0:43.4, 2:49.3, 2:58.6 | one markup |
| Ice floe, wave crest | S (reused) | 3:06.7-3:40.4, 5:51.5, 6:28.8 | `ICE` copied from the pilot (explainer_eps.py), wave crest from orca_pilot.py's shape |
| Bent-fin overlays (Port / Starboard), mugshot frames | S | 4:03.3 | two fin paths over kit Orca silhouettes with `finScale` 0.4 |
| Jerrycan, cardboard box | S | 4:15.4, 4:46.1 | keyframed in lockstep with the creature (no parenting) |
| Toothbrush, shark cage | S | 4:28.0, 4:38.3 | simple shapes |
| Diary page, sepia Ponting figure with tripod camera, ice slabs | S | 5:33.6-5:59.0 | warm gradient background instead of a sepia filter; a distinct figure, not the YOU icon; dogs as a Tag only |
| Person-on-board and seal silhouettes from below | S | 7:28.7 | two dark shapes |
| Life raft | S | 7:13.6 | with two kit `You` |
| Tank cross-section | S (core rects) | 8:20.3 | side view, one Orca with `scaleX` flips at the walls (no top-down art needed) |
| 75 / 98 dot grid, ship, blubber cross-section, arrow, ear, speed-limit sign, rudder | S | villain swap, R2, R3, bookend | simple shapes |
| Map places | data only | 2:49.3, 2:58.6, 3:50.4, 4:54.3, 7:05.0, 8:35.3 | lon/lat pins in the storyboard (Valdés -64.0,-42.5; Crozet 51.0,-46.4; Gansbaai 19.35,-34.58; Bremer Bay 119.4,-34.4; Gibraltar -5.6,36.0; Puget Sound -122.5,47.6). Zoom capped at 3-3.5 except Iberia (5, which has detail coastlines) |
| Existing kit pieces used | kit | throughout | Ocean, Orca (side, `pose` head/top, `finScale`, `silhouette`), GreatWhite, BlueWhale (drawn at 20 m with `pxPerM` x 20/28), SpermWhale, Seal, Liver, Car, Bus, You, Diver, Balance, ECG (hydrophone strip), Sailboat (`snapAt`, `sink`), Map, ScaleBar, Stat, Timer, Options (`strikes`, `select`, `stamp`), SpeedBars, Headline, Tag |

Producibility notes: (1) render a 10-second gate on the Spark CPU from shots 1-6 (kayak, fins, hull rings, silence, reveal) before any full TTS mix, per the PLAN's one-shot-must-pass rule; it exercises the three cheapest new props. (2) Shots that start mid-line (for example "It plans.", "No.", "HOLD / TEAR / SWALLOW") are anchored to Kokoro word times, so after the real mix, rerun the generator on the mix's captions.json. (3) Punch cards are all >= 0.8 s.

## 5. Facts (every number and mechanism, with its source)

| # | Claim in script | Source | Status |
|---|---|---|---|
| 1 | No confirmed fatal attack on a human by a wild orca; a handful of non-fatal bites and bumps (1972 Point Sur surfer bite, 2005 Ketchikan bump) | NOAA Fisheries killer whale profile; Whale and Dolphin Conservation; press records of the 1972 and 2005 incidents | confirmed in the critique round (wording avoids "once") |
| 2 | Around sixty to seventy unprovoked shark bites a year | Florida Museum International Shark Attack File (10-year mean ~70; 5-year mean ~64; 2024 = 47) | confirmed in the critique round; "around sixty to seventy" covers the range |
| 3 | Big male ~8 m, ~6 t (records near 9.8 m) | NOAA; Ford 2009 Encyclopedia of Marine Mammals | source listed. Comparisons: 2 x 4.5 m family car = 9 m ("nearly"); 6 t ~ four 1.5 t cars |
| 4 | Male dorsal fin up to ~1.8 m | NOAA; Ford 2009 | source listed; "about as tall as you" (~1.75 m) |
| 5 | 40-56 conical interlocking teeth, up to ~10 cm long | Ford 2009; Smithsonian Ocean | source listed; credit card is 8.56 cm (ISO/IEC 7810 ID-1) |
| 6 | Largest member of the dolphin family; false killer whale and pygmy killer whale are separate species | NOAA species pages (Pseudorca crassidens, Feresa attenuata) | source listed |
| 7 | Burst speed ~56 km/h; elite swimmers ~8 km/h (50 m free WR ~20.9 s = 8.6 km/h); casual ~3 km/h | NOAA; World Aquatics records | source listed; 50 km/h is the common urban limit, so "the speed you'd drive through town" |
| 8 | Up to about 130 kg of food on a big day | NOAA: 100-300 lb (45-136 kg) a day | confirmed in the critique round (was "well over a hundred kilos a day") |
| 9 | Pods led by older females; in the North Pacific, fish-eating residents and mammal-eating Bigg's orcas do not swap diets | Ford et al. 1998 Can. J. Zool.; Ford & Ellis 2006 | source listed; qualified "in the North Pacific" (some populations are generalists) |
| 10 | Fish eaters call and echolocate freely; Chinook salmon hear poorly at those frequencies | Barrett-Lennard, Ford & Heise 1996 Animal Behaviour; Au et al. 2004 JASA | source listed |
| 11 | Mammal hunters hunt mostly silently, by passive listening, because seals and porpoises hear orca calls; calling rises after a kill | Barrett-Lennard et al. 1996; Deecke, Ford & Slater 2005 Animal Behaviour | source listed (this replaces the old "bouncing clicks" option, which contradicted it) |
| 12 | Intentional stranding: Valdés takes sea lion pups; at Crozet, mothers push calves up the beach and calves practise on beaches without prey | Lopez & Lopez 1985 J. Mammalogy; Guinet & Bouvier 1995 Can. J. Zool. | source listed |
| 13 | Antarctic wave-washing; pods spy-hop to inspect the floe; strong preference for Weddell seals even where crabeaters are commoner | Visser et al. 2008 Marine Mammal Science; Pitman & Durban 2012 Marine Mammal Science | source listed |
| 14 | 3-7 May 2017: three white shark carcasses near Gansbaai, livers removed, at least one heart taken | Towner et al. 2022 African Journal of Marine Science; Dyer Island Conservation Trust releases | CHECK the heart detail against Towner 2022 before the mix (sources disagree on which shark) |
| 15 | Port and Starboard named for their collapsed dorsal fins | Towner et al. 2022 | source listed |
| 16 | White shark liver up to ~a quarter of body mass, oil-rich | Pethybridge et al. 2014; Towner et al. 2022 | source listed |
| 17 | Tonic immobility: inverted sharks go still; use by orcas suspected, not confirmed in the wild | Pyle et al. 1999 Marine Mammal Science (Farallon 1997 observation) | kept "unconfirmed" in R5 and "if the theory is right" in the climax |
| 18 | 18 June 2023, Mossel Bay: Starboard alone killed a ~2.5 m young white shark in under 2 minutes | Towner et al. 2024, African Journal of Marine Science 46(1), "Further insights into killer whales preying on white sharks in South Africa" | confirmed in the critique round (was "2022" and "a great white", which implied an adult; the 2022 footage is a different, multi-orca event). Comparison: dentists recommend 2 min of brushing |
| 19 | Gansbaai's white sharks largely left for months at a time; cage-dive boats went long stretches without sightings | Towner et al. 2022 ("Fear at the top"); operator sighting logs reported by Dyer Island Conservation Trust | source listed |
| 20 | March 2019 Bremer Bay: first documented orca kill of an adult blue whale (~18-22 m), >12 orcas; then a calf in 2019 and a juvenile in 2021 | Totterdell et al. 2022 Marine Mammal Science; Flinders University release | confirmed in the critique round (tally now 2019 adult, 2019 calf, 2021 young). Comparison: 20 m / 1.75 m = 11.4 of you |
| 21 | They took turns biting fins and flanks and pushing it under | Totterdell et al. 2022 (attack descriptions) | CHECK the exact tactics list against the paper's narrative before the mix |
| 22 | January 1911, Terra Nova expedition: orcas broke the sea ice under Herbert Ponting; two dogs tethered nearby; he escaped across the floes | Scott's journal, 5 January 1911 (*Scott's Last Expedition*); Ponting, *The Great White South* (1921) | source listed |
| 23 | Iberian orcas damaging rudders since 2020; a few yachts sunk; no crew seriously hurt | Atlantic Orca Working Group (GTOA); Spanish and Portuguese maritime authority reports 2020-2024 | source listed |
| 24 | Many shark bites on people are thought to be mistaken identity (a person on a board looks like a seal from below) | Ryan et al. 2021 J. R. Soc. Interface (white shark vision study) | source listed; hedged "often thought to be" |
| 25 | Four human deaths linked to captive orcas (1991, 1999, 2009, 2010), none in the wild | OSHA v. SeaWorld record (2010); Loro Parque 2009 news record; NOAA | source listed |
| 26 | Dozens of Southern Residents captured or killed 1965-1975 for aquariums | NOAA Southern Resident recovery plan (2008) | source listed |
| 27 | Southern Residents peaked at ~98 in 1995; ~73-76 now | Center for Whale Research annual census (74 on 1 July 2025) | confirmed in the critique round; "about seventy-five". Comparison: a US school bus seats ~72-90 |
| 28 | Threats: Chinook decline, vessel noise masking echolocation, PCB loads among the highest in marine mammals | NOAA recovery plan; Ross et al. 2000 Marine Pollution Bulletin | source listed |

## 6. Safety and policy notes

| Item | Handling |
|---|---|
| Captive deaths | One sober line with a number; no names, no retelling, no gore (R5 ad safety); avoids copying VtrcKTkhDHU's Tilikum segment |
| Animal deaths | Cartoon cut-aways (empty liver outline, seal tips into water, whale pressed down); no blood colour beyond the kit's red accent |
| Advice framing | The four moves are a thought experiment. Nothing encourages approaching wildlife (the old "close enough to touch" line is gone); the twist makes clear wild orcas are not a threat to kayakers |
| Closing sting | "Safe because of a habit, in an animal that keeps picking up new ones" is framed as unease, not a prediction of attacks; the Iberian example it calls back is explicitly harmless to people |
| Synthetic voice | Kokoro TTS over obvious flat-2D animation; not presented as a human presenter. The description carries the source list from the front matter |
| Channel duplication | Distinct title and angle from the 9:16 pilot (see title_note) |
