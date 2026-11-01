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
target_runtime: "9:00-10:00 (this version: {rt:} including a 1.6 s end hold)"
target_words_per_min: "160-170 while speaking (this version: {s:words} words, {s:wpm_speech} wpm while speaking, {s:wpm} wpm over the whole runtime)"
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

**Master question (spoken at {t:r02}, {p:r02}, on a black frame; re-armed at {w:g06@Which}, "a strange exception"):** why has an animal built for killing never picked you? **Progress device:** a six-tab THREAT FILE chip, on screen from {t:r03} for the whole ladder; one tab lights per rung and gets a verdict stamp at its seam; the bookend recaps all six on the finished board.

## 1. Beat alignment

Our timestamps are measured Kokoro times (see front matter). Reference timestamps were re-checked against the annotated corpus files in `research/corpus/explainer/`.

| Our beat | Our timestamp | Reference id + timestamp | Device borrowed | How we adapt it |
|---|---|---|---|---|
| L1 Hook: calm 2P scene, checklist, rule, felt clue, creature named last | 0:00-{t:r01} | fGcgWaswMns 0:00-0:29 (checklist 0:04-0:07, rule 0:09, sensation 0:14, named 0:23) | H1 calm scene + broken rule + unexplained sensation, subject named at ~80% of the hook | Kayak, not a dive. Checklist is sea + life jacket (no "sharks are rare" frame). The clue is a sound through the hull that stops. Named at {t:h06} (85% of the hook). Ends on "deciding something about you", a new frame. Hook = {s:hook_words} words |
| L1 paradox + quiet qualifier | {t:h03} | VtrcKTkhDHU 0:21 ("in the wild" qualifier) | H6 paradox with a planted loophole | "With killer in its name ... in the wild" plants both the name myth-bust ({t:b06}) and the villain swap ({t:v01}) |
| L2 Rival conceded in one line | {t:r01} | fGcgWaswMns 0:29-0:43 (rival concession -> pivot) | Concession then pivot | Sharks' bite tally vs the orca's zero, one line (was three) |
| L2 Master question on black | {t:r02} ({p:r02}); re-armed {w:g06@Which} | VtrcKTkhDHU 0:32 (why-question on a black frame), 9:05 (absolute line re-arms it) | Spoken paradox question by ~0:40, held on black | "So why has an animal built for killing never picked you?" Re-armed after the blue whale with "your seventy-odd kilos ... a strange exception" |
| L2 Three credentials as table of contents, paid in order | {t:r03} | VtrcKTkhDHU 0:09 (power list paid 7:11 / 8:18 / 23:44); fGcgWaswMns 0:45-0:53 (credential stack, last a teaser) | Hook list doubles as the TOC; each item paid in order | 1 beach raids -> paid {t:pl09} ({p:pl09}); 2 great whites without livers -> {t:k02} ({p:k02}); 3 largest animal ever -> {t:g02} ({p:g02}) |
| L3 Promise + progress device | {t:p01}; chip on screen from {t:r03} | fGcgWaswMns 0:58 (promise); JkAcCdqYJN0 0:14-0:20 (scoring rule, first entry) | Promise line; visible progress device before rung 1 | Big THREAT FILE folder shrinks into the corner chip; tab one opens at {w:b01@one} |
| Per-tab verdict stamps + finished board | each tab seam; recap {t:e04} | JkAcCdqYJN0 7:01 (per-entry "time inside" stamp), 8:37 (one-breath recap of every verdict) | Each entry ends on a stamp; the end recaps them all | BODY: YOU LOSE, SPEED: NO CONTEST, PLAN: IT THINKS AHEAD, WAVE: NOWHERE IS SAFE, SHARKS: EVEN THEY LEAVE, GIANTS: NO UPPER LIMIT; all six land again on their words in the bookend |
| L4 Tab 1 Body | {t:b01}-{t:s01} | fGcgWaswMns 1:02-1:50 (numbers -> everyday objects 1:12, body comparison 1:33, punch 1:47); VtrcKTkhDHU 2:04 ("not even whales") | Every number gets a comparison; short punch; small "you assumed wrong" | Our own anchors: two family cars long / four cars heavy, fin as tall as you, tooth longer than your credit card. Punch is HOLD / TEAR / SWALLOW on screen inside a longer sentence. Name myth-bust with the false/pygmy killer whale joke |
| L5 Tab 2 Speed | {t:s01}-{t:pl01} | fGcgWaswMns 1:50-1:56 (RQ -> one-word answer), 2:49 (its number vs yours) | RQ micro loop; you-vs-it number | "Could you outswim one? No." 56 km/h = the speed you drive through town; 130 kg on a big day > you; "never ordered one" (paid at {t:t11}) |
| L5 Tab 3 Plan: ecotypes, silence, teaching | {t:pl01}-{t:w01} | VtrcKTkhDHU 9:14 (muscle -> mind pivot), 10:00-10:41 (beaching taught); fGcgWaswMns 3:45 (hook clue closed by callback) | Shift from muscle to mind; close the felt clue by callback | Fish eaters click freely (plant for the ship-noise threat), mammal hunters hunt by listening (plant for climax move 3); clue closed at {t:pl07} ({p:pl07}); beaching told through the Crozet observations (mothers push calves, calves rehearse on empty beaches) |
| L5 Tab 4 Wave + re-immersion | {t:w01}-{t:k01} | VtrcKTkhDHU 9:34-9:46 (ice-floe wave); fGcgWaswMns 4:43 ("picture it again") | Tactic as an action sequence; re-immersion | "They take a look first" (plant for the twist answer at {t:t08}); Weddell preference (plant for {t:t10}); kayak = floe at {t:w07} ({p:w07}) |
| L5 Tab 5 Sharks (credential 2 paid) | {t:k01}-{t:g01} | VtrcKTkhDHU 7:16-7:30 (whodunit, 14 s); fGcgWaswMns 3:54 (one honest "never proven" hedge) | Mystery from the hook list closed as a dated story; one honesty hedge | Three great whites in one week (May 2017), Port and Starboard, fuel-tank joke, tonic immobility flagged unconfirmed, Starboard's 2023 solo kill of a young white vs your toothbrushing, cage-dive "you" line, "moving house" |
| L5 Tab 6 Giants (credential 3 paid) | {t:g01}-{t:pr01} | VtrcKTkhDHU 8:18 (blue whale top rung), 8:48 (turn-taking tactic), 9:05 (absolute line) | Top rung with dated proof, a 3-step tactic and an absolute line | Bremer Bay 2019 adult ~20 m; "eleven of you head to toe"; bite / ram / push under; 2019 adult, 2019 calf, 2021 young; "nothing in the sea hunts it back" (paid {t:v07}) |
| L5 Proof: could vs has | {t:pr01}-{t:c01} | fGcgWaswMns 5:00 (RQ "against people?"); JkAcCdqYJN0 7:06-7:30 (legend fake-out closed on could vs has) | Midpoint question, near-miss story, could-vs-has verdict | Honest "a handful of bites and bumps, no deaths" (no false "once"); Ponting 1911 told as the closest call; "his ice vs your hull" you-line; "Could it? Clearly. Has it? ... zero." |
| L6 Climax: four moves, each killed by an earlier tab | {t:c01}-{t:t01}; verdict {w:c06@Once} | fGcgWaswMns 5:59-7:01 (options killed by callbacks 6:10-6:49; verdict 7:01 = 70%) | Numbered options, each struck by an earlier rung, then an absolute verdict | 1 swim -> tab 2; 2 climb -> tab 4; 3 dive -> tab 3 ("they hunt by listening"); 4 play dead -> tab 5 (hedged "if the theory is right"). Verdict frame is our own ("the outcome is not up to you") at {p:c06} |
| L7 Twist: no wild pod has made that pick | {t:t01}-{t:t06} | fGcgWaswMns 7:13 (they almost never come after people); VtrcKTkhDHU 20:42-21:07 (you face to face, anticlimax) | Reversal right after the darkest verdict; 2P face-to-face beat | Iberian rudder pods leave the crews unhurt (plant for the closing sting); "You're slow, soft, and floating in their kitchen, and still they swim past" |
| L7 Twist answer | {t:t06}-{t:v01} | VtrcKTkhDHU 21:23-22:14 (dismiss a misconception -> named mechanism that pays an early plant -> the animal's verdict voiced) | Misconception, mechanism, verdict | Sharks bite people by mistake (a person on a board looks like a seal from below); orcas check first (pays {t:w02}); culture decides the menu (pays {t:w03} Weddell and {t:s05} "never ordered"); silence re-read as "silent while they look, chatty once they've decided" (ties tab 3's "quiet is an orca at work"); verdict "They checked, and you weren't food." |
| L7 Villain swap | {t:v01}-{t:e01} | VtrcKTkhDHU 25:36 (captivity pays "in the wild"), 31:00-31:44 (present threats); fGcgWaswMns 8:00 (before/after number), 8:22 (three modern threats); JkAcCdqYJN0 7:37 + 8:23 (comedy retired, unjoked beat) | Loophole payoff; harm runs the other way; before/after number; three threats; no jokes | Four captive deaths as one sober stat (no names, no retelling); Puget Sound captures; Southern Residents ~98 (1995) -> ~75 today = one school bus; salmon / ship noise (pays the "clicks" plant) / PCBs; "Nothing in the sea hunts the orca. The closest thing it has to a predator is us." |
| L8 Bookend | {t:e01}-{t:x01} | fGcgWaswMns 9:29-9:44 (opening rule restated, callbacks); JkAcCdqYJN0 8:37 (one-breath recap) | Return to the opening image; restate the rule; recap; end on an image | Same kayak frame; the squeaking returns (they decided); "The rule you paddled out with still holds. In the wild, zero."; six-tab recap in one breath; title line, then the sting: safe because of a habit, in an animal that keeps picking up new ones (callback to the Iberian rudder habit); last image a single fin rising |
| L9 CTA | {t:x01} | fGcgWaswMns 9:47-9:52 (comment prompt naming the next creature); PLAYBOOK §6 | One comment prompt under 15 s | Two-way choice that names the next files: "leopard seal or box jellyfish?" (both are in the backlog) |

### Open loops and plants

| Loop / plant | Opens | Closes | Target (PLAYBOOK) |
|---|---|---|---|
| Master question: why hasn't it come for you? | {t:r02} ({p:r02}) | re-armed {w:g06@Which}; answered {t:t06}-{t:t13} ({p:t13}) | spoken early, answered late (VtrcKTkhDHU) |
| Sound through the hull, then silence | {t:h04} | callback {t:pl07} ({p:pl07}); re-read {t:t12}; bookend {t:e02} | ~35% |
| "Deciding something about you" | {t:h06} | {t:t13} "They checked, and you weren't food." ({p:t13}); {t:e06} "They decided not to." | late |
| Credential 1: beach raids | {t:r03} | {t:pl09} ({p:pl09}) | first teaser by ~35% |
| Credential 2: great whites without livers | {t:r03} | {t:k02} ({p:k02}) | ~40-50% |
| Credential 3: largest animal ever | {t:r03} | {t:g02} ({p:g02}) | ~50-60% |
| Title: could hunt you | {t:p01} | climax verdict {w:c06@Once} ({p:c06}); title line {t:e06} | ~70% |
| "In the wild" | {t:h03} | {t:v01} ({p:v01}) | late |
| "Killer" in its name | {t:h03} | name myth-bust {t:b06} | plant-payoff |
| "Nothing in the sea hunts it back" | {t:g06} | {t:v07} ({p:v07}) | plant-payoff |
| P "never ordered one" | {t:s05} | {t:t11} menu card | plant-payoff |
| P "they take a look first" | {t:w02} | {t:t08} "Remember, they check first" | plant-payoff |
| P Weddell preference | {t:w03} | {t:t10} | plant-payoff |
| P mammal hunters "hunt by listening" | {t:pl04} | climax move 3 {t:c04} | plant-payoff (a true callback) |
| P fish eaters "click all day" | {t:pl04} | ship noise drowns the clicks {t:v06} | plant-payoff |
| P tonic immobility (unconfirmed) | {t:k07} | move 4 {t:c05}, still hedged | plant-payoff |
| P Iberian pods: a new habit since 2020 | {t:t03} | closing sting {t:e07} | plant-payoff |

## 2. Pacing self-check (PLAYBOOK §8 targets; measured, not modelled)

| Metric | Target | This version | Pass? |
|---|---|---|---|
| Runtime | 8-10 min | {rt:} | yes |
| Words / wpm while speaking | ~1,500-1,650 / 160-170 | {s:words} / {s:wpm_speech} | yes |
| Hook | 70-90 word immersion hook, creature named at ~80% | {s:hook_words} words / 0:00-{t:r01}; "orcas" at {t:h06} (85% of the hook) | yes |
| Progress device / first rung | by 45 s (corpus median 46 s, range 8-78 s) | chip on screen {t:r03}; first tab {w:b01@one} | device yes; first rung 14 s late (accepted: the spoken master question and the three-item TOC sit before it, as fGcgWaswMns does to 1:02) |
| Setup share (L1-L3) | 8-10% | {p:b01} | yes |
| "You" in sentences / words | >=25% / >=3% | {s:you_sent}% / {s:you_words}% | yes |
| Average sentence | 10-13 words with 1-3 word punches | {s:avg} words; kept punches: "No." "Smart." "It plans." "It's served." "Look familiar?" "Clearly." | yes |
| Numbers per minute | 3-5, each with a comparison | ~{s:nums_min} by the crude counter (it also counts "one"/"four" in "four moves", "Tab one"); every hard number has a comparison | borderline |
| Re-hook | reset ~20 s, verbal re-hook ~30 s, new rung 40-70 s | a shot change every 4.6 s on average ({n:} shots); verbal re-hooks at {t:r02}, {t:p01}, {t:s01}, {t:pl01}, {t:pl07}, {t:w01}, {t:w07}, {t:k01}, {t:g01}, {w:g06@Which}, {t:pr01}, {t:c01}, {t:t01}, {t:t06}, {t:v01}, {t:e01}; rungs run 31-64 s | yes |
| Comic deflation | every 60-90 s until the villain swap | pygmy killer whale {t:b06}, never ordered {t:s05}, served {t:w06}, fuel tank {t:k06}, moving house {t:k11}, eleven of you {t:g03}, delivery {t:c02}, ask its liver {t:c05}, menu {t:t11}; none after {t:v01} | yes (one 97 s gap, {t:k11}-{t:c02}) |
| Climax verdict | dossier 60-75% | {p:c06} | yes |
| Re-immersion ("picture it again") | ~47% | {p:w07} | early; kept because it lands right after the floe it rhymes with |

## 3. Script (voiceover = burned-in captions)

Hook first line: **"You're in a sea kayak on cold, glassy water."** (9 words; the checklist starts at {t:h02})
Hook first visual: **the yellow kayak with the seated stick-figure YOU at the left third of a dusk waterline, three black dorsal fins 130 px tall (12% of the frame) mid-distance right from frame 1; the nearest fin sinks at ~2.3 s.**
<!--SCRIPT-->

## 4. Shot list ({n:} shots)

Generated from `gen_storyboard.py` (one function per shot; the same code writes `storyboard.json`). Kit vocabulary from `studio/src/kits/explainer/README.md`. NEW S = an inline-SVG prop written into the storyboard (no kit change). The THREAT FILE chip is an inline-SVG layer the generator adds to every scene from {t:r03} to the end of the climax; a tab-light is a second chip layer that pops on the tab's word. {filled:} long scenes also get camera re-frame keyframes every <= 2.6 s so no hold exceeds 3 s; those should get a real state change in the first render review.

<!--SHOTS-->

### Kit gaps, by cost tier

S = inline SVG markup in the storyboard (no code change). M = a new registered Figure. L = a new component. **M + L items: 0.** Everything below is S, or reuses an existing kit component.

| Prop | Tier | Used in | How |
|---|---|---|---|
| THREAT FILE corner chip (6 tabs, lit count) | S | {t:r03}-{t:t01} | `chip_svg(lit)` injected per scene by the generator; tab-light = a second layer with `pop` on the word |
| THREAT FILE folder (promise, finished board, CTA) | S | {t:p01}, {t:e04}, {t:x01} | `folder_svg()`; verdict stamps are kit `Tag` layers (bg red, rotated) landing on their words |
| Kayak side view + seated YOU, top view, flipped | S | hook, {t:pl07}, {t:w07}, twist, bookend, climax | three markups; the side view's waterline is at 77% of its box (`kayak_at`) |
| Dorsal fins (hook, sinking fin, last-image fin) | S | hook, {t:w07}, {t:t01}, bookend | one fin path, >= 8% of frame height |
| Hull sound rings | S | hook, {t:pl07}, {t:t12}, {t:e02}, {t:c04}, {t:v06} | core `circle` layers with scale/opacity keyframes (`ring_layers`) |
| Orca fin at true scale vs YOU | S | {t:b03} | fin path drawn 1.8 m x 300 px/m beside kit `You` 1.75 m at `pxPerM` 300, one baseline (fixes the 1.2 m kit fin problem) |
| Tooth vs credit card, interlocking tooth rows | S | {t:b04}, {t:b05} | true scale 4500 px/m; rows slide together on y keyframes |
| Order slip, family-menu chalkboard, strike bar | S | {t:s05}, {t:t09}, {t:t11}, {t:e07} | text in SVG |
| Beach strip with foam | S | {t:r03}, {t:pl09}, {t:pl10} | one markup |
| Ice floe, wave crest | S (reused) | {t:w01}-{t:w07}, {t:pr04}, {t:c03} | `ICE` copied from the pilot (explainer_eps.py), wave crest from orca_pilot.py's shape |
| Bent-fin overlays (Port / Starboard), mugshot frames | S | {t:k04} | two fin paths over kit Orca silhouettes with `finScale` 0.4 |
| Jerrycan, cardboard box | S | {t:k06}, {t:k11} | keyframed in lockstep with the creature (no parenting) |
| Toothbrush, shark cage | S | {t:k08}, {t:k09} | simple shapes |
| Diary page, sepia Ponting figure with tripod camera, ice slabs | S | {t:pr02}-{t:pr05} | warm gradient background instead of a sepia filter; a distinct figure, not the YOU icon; dogs as a Tag only |
| Person-on-board and seal silhouettes from below | S | {t:t07} | two dark shapes |
| Life raft | S | {t:t04} | with two kit `You` |
| Tank cross-section | S (core rects) | {t:v02} | side view, one Orca with `scaleX` flips at the walls (no top-down art needed) |
| 75 / 98 dot grid, ship, blubber cross-section, arrow, ear, speed-limit sign, rudder | S | villain swap, R2, R3, bookend | simple shapes |
| Map places | data only | {t:pl09}, {t:pl10}, {t:k02}, {t:g02}, {t:t03}, {t:v04} | lon/lat pins in the storyboard (Valdés -64.0,-42.5; Crozet 51.0,-46.4; Gansbaai 19.35,-34.58; Bremer Bay 119.4,-34.4; Gibraltar -5.6,36.0; Puget Sound -122.5,47.6). Zoom capped at 3-3.5 except Iberia (5, which has detail coastlines) |
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
