---
slug: explainer-never-meet-leopard-seal
niche: explainer
format: long
aspect: "16:9"
title: "Why You Should Never Swim With A Leopard Seal"
title_alt_series: "Why You'd Never Want To Meet A Leopard Seal"
title_formula: "Our own variant of the 'why you'd never want to meet [X]' series formula (PLAYBOOK section 7); see titles.md for the ranked A/B list"
variant: "Dossier (PLAYBOOK 1a): verdict at 74%, then a restraint twist and the gift payoff"
target_runtime_s: 571.29
target_runtime_range_s: [540, 600]
target_words_per_min: 165        # effective incl. pauses; PLAYBOOK long-form target 160-170, Depth Theory 168
voice: "Kokoro-82M am_michael; hook speed 0.82, body speed 0.94 (pipeline.audio.make reads the [speed:] markers in the narration block)"
measured:                        # every number below is computed by gen.py from per-line Kokoro durations measured on the Spark CPU
  timing_source: "Kokoro-82M am_michael on the Spark CPU, measured per line"
  vo_words: 1576
  vo_runtime_s: 566.3      # + 5 s end hold = 571.29 s
  effective_wpm_incl_pauses: 167.0
  speech_wpm: 181.5     # body 182.0
  hook_words: 77     # immersion hook, target 70-90 words / ~30 s
  hook_s: 29.6             # rule at 7.8 s, turn at 11.6 s, creature named at 26.7 s
  avg_sentence_words: 9.9
  you_pct_words: 3.05           # target >= 3%
  you_pct_sentences: 27.0   # target >= 25%
  you_per_min: 5.1
  numbers_per_min: 4.9
  promise_s: 41.6         # promise at 0:41, EXHIBIT 7 slot at 0:48
  first_rung_s: 55.3   # setup (L1-L3) = 9.7% of runtime
  rehook_median_gap_s: 13.3
  rehook_max_gap_s: 46.1
  joke_max_gap_s: 92.0   # the only long gap is the deliberate sober stretch around the 2003 case
references:
  - id: fGcgWaswMns
    short: SPERM
    url: https://www.youtube.com/watch?v=fGcgWaswMns
    views: 2307237
    outlier_score: 14.65
    why_chosen: "Same series formula, format (8-10 min dossier) and 2D kit style. We borrow its skeleton: a calm second-person hook that ticks off the usual dangers and states a safety rule, a turn line and a felt sensation, the creature named last; a 3-credential stack ending on a dated historical teaser; a capability ladder closed by 1-3 word answers; a 'picture it again' re-immersion near the midpoint; a dated story, a second case ('not the only one') and a sympathy seed in the proof-of-harm rung; an options climax where earlier rungs (including the senses) kill each escape; a reassurance flip with a scale-of-interest analogy; and a bookend that restates the rule, concedes it, and ends on three callbacks."
  - id: VtrcKTkhDHU
    short: ORCA
    url: https://www.youtube.com/watch?v=VtrcKTkhDHU
    views: 8289332
    outlier_score: 318.82
    why_chosen: "Closest premise: a top predator that could harm people but almost never does. We borrow the quiet qualifier planted early and exploited later (0:21 'in the wild'), the paradox restated with one stark number (20:19-20:32), the silent throwaway plant paid much later (2:54 -> 27:54), the myth-bust on a famous belief (1:21-2:04), a named, dated individual story with escalating repetition (18:14-19:33), and the animal's inner verdict voiced in short declaratives (22:14)."
  - id: jw6bS-WL4F4
    short: JELLY
    url: https://www.youtube.com/watch?v=jw6bS-WL4F4
    views: 6716278
    outlier_score: 1.43
    why_chosen: "Same 'looks harmless, is worse than you think' contrast. We borrow the comic misdirect list of famous regional threats with an absurd item (0:03-0:08; ours: polar bears at the wrong pole) and the 'not the worst part' turnstile placed right after the most graphic image, with a background change on the next word (0:31)."
fact_file: "section 'Fact sheet' below; every number and mechanism has a source; hedged claims are worded as hedges in the VO"
safety: "No gore: the penguin grab cuts to splash rings and a feather puff. The 1985 and 2003 cases are told plainly with cards and a map pin, never depicted. No jokes within 20 s before or after the 2003 case (last joke ends 5:17, case starts 5:38, a 5 s silent pivot sits between). A 3 s black card follows it, and the climax opens on 'Now, a hypothetical' and a different scenario (you slip off a floe), not snorkelling."
description_note: "Add to the YouTube description: 'Narration uses a synthetic voice. All animation is original and code-drawn.'"
post_caption_cta: "Walrus or elephant seal: who should we put you in the water with next?"
---

# Why You Should Never Swim With A Leopard Seal


## Beat alignment table

| Our beat | Our time | Reference id + timestamp | Device borrowed | How we adapt it |
|---|---|---|---|---|
| L1 Hook: calm scene, threat shown in frame 1 | 0:00-0:03 | fGcgWaswMns 0:00 (2P placement); PLAYBOOK s2 "name late, show early" | 2P placement in a calm, specific scene; the subject's effect on screen at once | 8-word placement line; the viewer sees a spotted silhouette slide under the keel while YOU doesn't |
| L1 Hook: misdirect checklist + rule | 0:03-0:11 | fGcgWaswMns 0:04-0:11 (checklist ending on the rule); jw6bS-WL4F4 0:03-0:08 (absurd item) | Usual dangers ticked off, an absurd item, then the safety rule | Orcas (tick), polar bears (wrong pole), "the only thing out to get you is the cold" lands at 0:07.8 |
| L1 Hook: turn + sensation | 0:11-0:21 | fGcgWaswMns 0:14 | Short turn line, then an unexplained body sensation | Penguin bursts past your boot, "Not swimming. Airborne." (loop B); a trill felt through your knees (loop A) |
| L1 Hook: subject named last | 0:22-0:29 | fGcgWaswMns 0:23 | Creature named at ~90% of the hook, holding the upper hand | Smiling face at the floe edge; named at 0:26.7; "It isn't smiling." (loop C) |
| L2 Credential stack | 0:30-0:41 | fGcgWaswMns 0:45-0:58 | 3 credentials, the last a dated historical teaser | Hunts other seals; catch-and-release; "in 1916, one came out of the sea after one of Shackleton's men" (loop D, closes 4:52) |
| L3 Promise + quiet qualifier + progress device | 0:41-0:55 | fGcgWaswMns 0:58 (title restated); VtrcKTkhDHU 0:21 (quiet qualifier), 0:41 (transformation promise) | Title as the video's job; one quiet line the twist will exploit; a concrete paradox teaser | "Build the case" + "why most people who do still climb out fine" (paid 7:11) + "four days, nobody got bitten" (loop E); CASE FILE board from 0:30, slot 7 grey at 0:48 |
| R1 Body + face | 0:55-1:39 | fGcgWaswMns 1:02-1:50 (numbers -> body comparisons 1:12, 1:33; "you assumed wrong" 1:19; 2-word punch 1:47) | Number -> you-comparison; anatomy correction; short punch | 3.5 m = two of you; 500 kg = seven of you; the smile is a jaw line; fang vs thumb joint; "Puppy face. Crocodile job." |
| R1 silent plant | 1:26 | VtrcKTkhDHU 2:54 (collagen fin, paid 27:54) | Throwaway detail with no owner, paid much later | "Wide enough to close over something you'd never expect" (no name, no camera shown); paid 8:02-8:08 |
| R2 Diet | 1:39-2:20 | fGcgWaswMns 1:50-1:56 (RQ answered in one word), 2:34-2:36 (everyday metaphor, joke out); dated study shape from 4:26 | RQ -> one word; a dated study; everyday metaphor; joke out | "Often? Krill." (not "mostly"); a 2013 study at Taronga; baleen trick in a garage-sized animal; "Picky eater, it is not." |
| R3 Ice edge (loop B closes) | 2:20-3:15 | fGcgWaswMns 2:42 (where it hunts), 3:45 (explicit "remember...?" close); VtrcKTkhDHU 1:21-2:04 (myth-bust) | Hunting ground as a place; explicit callback close; myth correction | The doorway is also your only exit (plants climax option 2); boat-tube guards as a throwaway (paid 6:23); "That's why the penguin by your boot came out flying" at 30%; skinning myth corrected |
| R3 turnstile | 3:15 | jw6bS-WL4F4 0:31 | "Not the worst part" line right after the most graphic image, background change on the next word | "And that still isn't the strangest thing it does to penguins." -> hard cut to the game diagram |
| R4 The game | 3:19-3:45 | fGcgWaswMns 3:50-3:54 (honest "never proven" hedge); VtrcKTkhDHU 16:21 (secondary mystery) | Callback entry, a mini-mystery left honestly open | "Remember that catch-and-release?" escalates credential 2; practice / play / killing time; "nobody has pinned it down" |
| R5 Senses + song (loop A closes) | 3:46-4:36 | fGcgWaswMns 2:58-3:01 (RQ bridge), 3:28 (measured record number), 3:45-3:47 (callback that explains the hook sensation) | RQ bridge; measured number tied to the body; callback reveal | Whiskers and eyes; "that trill from the start" = a male singing upside down; 177 dB "loud enough to reach you through the ice" (closes at 43%) |
| Re-immersion | 4:36-4:50 | fGcgWaswMns 4:43-4:53 | "Picture it again" with the rungs combined | Back on the floe at 48%; "You might be interesting." |
| R6 The record (loop D closes) | 4:50-6:00 | fGcgWaswMns 5:00-5:08 (people? -> dated story closing the credential teaser), 5:30 ("not the only one" second case), 5:53 (sympathy seed), 5:57 (joke) | Dated told story; second real case; perspective seed; comic button, then a sober case | Orde-Lees 1916 (crew eating seals, the seal tracks his shadow under the ice, "most Shackleton ending"); Gareth Wood 1985 (bitten twice, kicked free); 5 s silent pivot; Kirsty Brown 2003, told plainly |
| Climax: your options | 6:04-7:08 | fGcgWaswMns 5:59-7:01 (each option killed by an earlier rung, senses used twice, verdict at 70%) | Numbered escapes, each struck by a callback + a metaphor; flat verdict | Hypothetical, not her scenario. Boat: speed + tubes planted 2:32. Ice: doorway + Wood 1985 + Orde-Lees. Under the floe: whiskers read your wake (R5) + "hide-and-seek while ringing a bell". Play dead: the game (R4). Verdict at 74% |
| Twist: restraint | 7:09-7:50 | VtrcKTkhDHU 20:19-20:32 (paradox restated, one stark number); fGcgWaswMns 7:05-7:33 (reassurance flip, scale-of-interest analogy) | "Here's what doesn't fit"; the planted qualifier paid; one clean number; humbling analogy | "Most people climb out fine" returns; one known death in decades of research diving; tourists only as context, VO and Stat both "over a hundred thousand"; a cat inspecting a box |
| Payoff: the gift (loop E closes) | 7:50-8:55 | VtrcKTkhDHU 18:14-19:33 (named, dated story with escalating repetition), 22:14 (inner verdict in short declaratives); fGcgWaswMns 9:22 (opening credential reread as a paradox) | Named story; the plant revealed; the animal's verdict voiced; an earlier fear given a new meaning | Nicklen 2006, one of the big females planted at 0:55; "And his head." pays the 1:26 plant; live -> live -> injured -> dead; "Clumsy thing. Big eye. Can't hunt. Needs feeding." + "Fair review."; catch-and-release reread as an offer to cooperate |
| Bookend | 8:55-9:19 | fGcgWaswMns 9:29-9:44 | Rule restated + concession, then 3 callbacks and a humbling joke | "The cold is still far more likely to kill you"; trill = singer, flying penguin = escape, smile = curiosity; "lunch is on her" |
| CTA | 9:20-9:26 | fGcgWaswMns 9:47; PLAYBOOK s6 (one comment prompt naming the next creature, <=15 s) | Comment prompt naming the next creature | Two-way choice (walrus or elephant seal) to drive debate; finished CASE FILE held 5 s |

Pacing against PLAYBOOK sections 3, 8 and 10:

| Check | Target | Ours |
|---|---|---|
| Hook | 70-90 words / ~30 s, creature named late, threat on screen in frame 1 | 77 words / 29.6 s; rule at 7.8 s, turn at 11.6 s, named at 26.7 s; silhouette in frame 1 |
| Promise + progress device | by 45-55 s | CASE FILE board at 0:30; promise at 0:41; slot 7 at 0:48 |
| First rung | <= 45 s (corpus median 46 s, range 8-78 s) | 0:55 (55.3 s). Setup = 9.7% of runtime (norm 8-10%); a 77-word immersion hook alone is 29.6 s, so this is as tight as the hook mode allows |
| Words per minute (incl. pauses) | 160-170 | 167.0 (speech 181.5) |
| Verbal re-hook interval | ~30 s | 0:11, 0:26, 0:30, 0:41, 0:48, 0:55, 1:26, 1:39, 2:07, 2:20, 2:48, 3:15, 3:19, 3:33, 3:46, 4:02, 4:29, 4:36, 4:50, 5:17, 6:04, 6:12, 6:25, 6:37, 6:47, 6:59, 7:09, 7:23, 7:40, 7:47, 8:09, 8:20, 8:38, 8:55, 9:13, 9:20 (median 13.3 s, max 46.1 s) |
| Comic deflation | every 60-90 s | 0:05, 1:37, 2:02, 2:19, 3:12, 3:35, 4:48, 5:14, 6:45, 6:55, 7:40, 8:20, 8:36, 9:17; max gap 92.0 s, which is the sober 1985 / 2003 / hypothetical-opening stretch, kept joke-free on purpose |
| Long loops | 3-4 opened in minute 1, closed ~35/50/70/98% | B airborne penguin 0:15 -> 2:54 (30%); A trill 0:17 -> 4:02 (43%); D 1916 teaser 0:36 -> 4:52 (51%); title 0:41 -> verdict 7:01 (74%); qualifier 0:45 -> 7:11 (76%); E four-day story 0:48 -> 7:50-8:48 (93%); rule 0:07 -> 8:57 (94%); C smile 0:28 -> 1:17 and 9:13 (97%) |
| Plants paid later (>= 4) | 4+ | anonymous gape 1:26 -> 8:08; boat tubes 2:32 -> 6:23; doorway / your exit 2:29 -> 4:38, 6:28; big females 0:55 -> 7:50; whiskers 3:52 -> 6:39; catch-and-release 0:33/3:21 -> 6:49, 8:38; Orde-Lees under-ice tracking 5:06 -> 6:28; Wood on the ice 5:17 -> 6:28; "most climb out fine" 0:45 -> 7:11; crew eating seals 4:52 -> the gift reversal 8:09 |
| Second person | >= 3% of words, >= 25% of sentences | 3.05% of words, 27.0% of sentences (5.1/min) |
| Numbers | 3-5/min, each with a comparison | 4.9/min (approximate count; includes number words) |
| Re-immersion | ~47% | 4:36 (48%) |
| Honest hedge | once | "nobody has pinned it down" 3:38; also "probably" (whiskers), "often quoted" (speed), "Nobody's certain" (song) |

## Fact sheet

| # | Claim in VO | Value used | Source / note |
|---|---|---|---|
| F1 | Biggest leopard seals are females; ~3.5 m, ~500 kg | 3.5 m, ~500 kg | Wikipedia "Leopard seal": adults 2.4-3.5 m, 200-600 kg; females up to 50% larger than males |
| F2 | Two of you end to end | 2 x 1.75 m YOU = 3.5 m | kit `You` is 1.75 m |
| F3 | Seven of you | 7 x ~70 kg = 490 kg | arithmetic |
| F4 | Front fangs up to 2.5 cm, about your thumb's top joint | 2.5 cm vs ~2.5-3 cm | Wikipedia "Leopard seal" |
| F5 | Krill are "often" the food; shrimp-like, about as long as your little finger | up to ~6 cm | Share varies by place and season: Cape Shirreff spring diet krill 31.7-38%, fish 31.6-36.5%, penguins 24-27% (BMC Ecology 2020); Wikipedia: krill "a major part of older seals' diets" in winter. Antarctic krill reach ~6 cm. VO avoids "mostly" |
| F6 | Back teeth sieve krill; a 2013 study at Taronga Zoo | 2013 (publication year) | Hocking, Evans & Fitzgerald 2013, Polar Biology 36:211-222 (captive seals at Taronga Zoo, Sydney); Monash University release. VO says "a 2013 study" |
| F7 | Prey: fish, squid, six penguin species, other seals up to young elephant seals | 6 species | Wikipedia "Leopard seal" (emperor, king, rockhopper, Adelie, gentoo, chinstrap; crabeater, Weddell, Ross, fur seal pups, elephant seal young) |
| F8 | Only seal in Antarctica that hunts other seals | | Narrowed from "only seal that routinely hunts other seals" (sea lions also take seals). No other Antarctic seal (Weddell, crabeater, Ross, southern elephant, Antarctic fur) preys on seals |
| F9 | Only natural predator: the orca | | Wikipedia "Leopard seal" |
| F10 | The doorway: ambush at the ice edge; penguins launch themselves out onto the ice | | Wikipedia "Leopard seal" (waits near the ice edge; grabs by the feet, beats on the surface, tears by thrashing; old "skinning" reports considered wrong). Penguins porpoising and leaping onto ice at colony edges is widely filmed and is described as predator avoidance in Adelie penguin literature (Ainley 2002, The Adelie Penguin); in the hook it is a hypothetical scene |
| F11 | Station crews fit guards because seals bite inflatable tubes | | Wikipedia "Leopard seal": "a predilection for attacking the black, torpedo-shaped pontoons of rigid inflatable boats"; researchers fitted protective guards |
| F12 | Catch-and-release of penguins, purpose unresolved | hedged | Widely filmed by divers and documentary crews; no peer-reviewed rate found, so VO says "have watched" and "nobody has pinned it down". The unsourced "young seals do it more" line was cut |
| F13 | Whiskers "probably" tuned to wakes; big eyes suit dim water | hedged | Hydrodynamic trail-following shown in harbour seals; not measured in leopard seals, so VO says "Like other seals ... probably" |
| F14 | Males sing in the southern summer, upside down, rocking, for hours a day; up to ~177 dB underwater; five call types; purpose not settled | 153-177 dB re 1 uPa at 1 m, 5 types | Wikipedia "Leopard seal" (vocalisation; Rogers et al.); confirm the dB range against Rogers et al. before posting. Never compared with air dB on screen. "Loud enough to reach you through the ice" and the felt trill in the hook are a hypothetical-scene claim (seal calls are commonly heard through sea ice); "claim space or call in females" is hedged with "Probably ... Nobody's certain"; the VO no longer says hearing one puts you inside a territory |
| F15 | 1916: Orde-Lees, on skis, chased; the seal tracked his shadow under the ice and surfaced ahead; Frank Wild shot it; the crew ate it; the crew were eating whatever seals they could catch | 1916 | Shackleton, South (1919); Wikipedia "Leopard seal" ("chased Orde-Lees on the ice ... saved only when ... Frank Wild shot it"). Exact date not confirmed, so VO says only "1916" |
| F16 | 1985: Gareth Wood, standing on sea ice, grabbed by the leg, bitten twice; companions kicked it in the head with spiked boots (crampons) until it let go | 1985 | Wikipedia "Leopard seal" ("bitten twice on the leg when a leopard seal tried to drag him off the ice and into the sea"; companions kicked it with crampons); Swissinfo and PBS NOVA accounts of the In the Footsteps of Scott expedition. Sources disagree on nationality and exact place, so VO gives neither |
| F17 | Kirsty Brown, BAS marine biologist, snorkelling with a colleague near Rothera, July 2003; held under ~6 min, to ~70 m; age 28; only known human death | 22 July 2003, 6 min, 70 m, 28 | National Geographic News, Aug 2003; BAS statement ("the first person we know of to have been killed by a leopard seal"); Wikipedia "Leopard seal". Inquest by the coroner for British Antarctic Territory (Stanley, Falkland Islands, late 2003). VO says "only known", not "only ever" |
| F18 | Decades of research diving near leopard seals; one known death | decades | Muir, Barnes & Reid 2006, Antarctic Science 18:61-74 ("Interactions between humans and leopard seals", BAS records); BAS has run diving programmes at Signy and Rothera since the 1960s-70s. VO and screen say "decades", not a count |
| F19 | Over a hundred thousand visitors a season | 2023-24: ~122,000 | IAATO season statistics. Context only: most visitors never enter the water, so the restraint claim rests on F18, not on tourist numbers. VO "over a hundred thousand" = Stat "100,000+" |
| F20 | Burst speed "often quoted" ~40 km/h | hedged | Popular figure, not well measured; worded "often quoted" on both VO and SpeedBars |
| F21 | You, soaked and freezing, ~3 km/h | EST | Recreational finning ~0.8 m/s; a clothed swimmer in ice water is slower, so 3 is generous |
| F22 | Nicklen, 2006, Antarctic Peninsula; a big female, ~3.5 m by his estimate; mouth over his camera and head; live, then injured, then dead penguins over four days; pushed them at his lens; blew bubbles | 2006, 4 days | National Geographic "How a Leopard Seal Fed Me Penguins" (2014); Nicklen TED 2011; NPR Fresh Air 2017. His estimate is 12 ft (3.66 m); VO rounds to "around three and a half metres", matching F1 and the ScaleBar |
| F23 | His read of her verdict: a useless hunter who needed feeding | | NPR Fresh Air 2017, paraphrased; voiced as four short lines and framed as his read ("He came away sure of her verdict") |
| F24 | Seals filmed sharing a carcass at South Georgia; gifts to divers might be an offer to cooperate | | Krause, Rogers et al. 2019, Polar Biology (drone footage, St Andrews Bay, Oct 2016); the authors' own framing is possible cooperation / tolerance |

## The script

Layers: KICKER = ALL-CAPS white title top-centre; PUNCH = red caption for the beat's punch word only; TAG = small white label pinned to an object; CASE FILE = dossier board (NEW `explainer/CaseFile`, 7 slots) shown as a 2-3 s insert each time a slot is stamped. Burned-in word captions follow the VO (core `captions`). Timestamps are line starts on the measured Kokoro timeline (hook speed 0.82, body 0.94); `(SILENCE n s)` lines hold the picture with no VO.

Hook first line: "You're kneeling on Antarctic sea ice, camera up."
Hook first visual: wide surface split, low sun; YOU kneels on a white floe with a camera to the eye; under the waterline a long spotted silhouette slides beneath the ice keel, left to right. The viewer sees it; YOU does not. Sound: ice creak + the sub-bass trill.


### [0:00] L1 HOOK (immersion, slower read)

[0:00.0] You're kneeling on Antarctic sea ice, camera up.
ON SCREEN: FRAME 1: a long spotted silhouette slides under the ice keel, left to right. YOU, kneeling on the floe with the camera to your eye, never looks down. KICKER "ANTARCTIC PENINSULA"
[0:03.3] Orcas leave people alone.
ON SCREEN: TAG "ORCAS" + green tick
[0:05.4] Polar bears? Wrong pole.
ON SCREEN: map whips north; white bear silhouette, TAG "WRONG POLE" + red cross
[0:07.8] Down here, the only thing out to get you is the cold.
ON SCREEN: TAG "-2 °C WATER" + green tick, then "THE ONLY THREAT?"
[0:11.6] Then a penguin shoots out of the water past your boot.
[0:15.0] Not swimming. Airborne.
ON SCREEN: PUNCH "AIRBORNE"
[0:17.3] Under the ice, a low trill starts, and you feel it through your knees.
ON SCREEN: rings rise through the floe into your knees
[0:22.0] A long face rises at the edge of the floe, smiling up at you.
ON SCREEN: side-profile head over the floe edge, mouth line curved up
[0:26.7] That's a leopard seal.
ON SCREEN: KICKER "LEOPARD SEAL"
[0:28.4] It isn't smiling.
ON SCREEN: PUNCH "IT ISN'T SMILING"

### [0:30] L2 CREDENTIALS + L3 PROMISE

[0:30.1] It's the only seal in Antarctica that hunts other seals.
ON SCREEN: CASE FILE board pops in: "THE CASE AGAINST THE LEOPARD SEAL", 7 slots; credential 1 "HUNTS OTHER SEALS"
[0:33.8] It plays catch-and-release with live penguins.
ON SCREEN: credential 2 "PLAYS WITH ITS FOOD"
[0:36.6] And in 1916, one came out of the sea after one of Shackleton's men.
ON SCREEN: credential 3 in red "1916: ?" (sealed envelope)
[0:41.6] So let's build the case against ever sharing water with one.
ON SCREEN: KICKER "WHY YOU'D NEVER WANT TO MEET ONE"
[0:45.6] And work out why most people who do still climb out fine.
ON SCREEN: TAG "MOST CLIMB OUT FINE?" (small, grey)
[0:48.8] Then, the strangest leopard seal story on record. It lasted four days, and nobody got bitten.
ON SCREEN: slot 7 "EXHIBIT 7: ???" in grey; TAG "4 DAYS · 0 BITES"

### [0:55] R1 BODY AND FACE (exhibit 1)

[0:55.3] Start with size. The biggest leopard seals are the females.
ON SCREEN: TAG "BIGGEST = FEMALES"
[0:59.4] A big one can reach about three and a half metres: two of you, lying end to end.
ON SCREEN: ScaleBar "~3.5 M"; two YOU figures lying end to end under the seal, TAG "2 x YOU"
[1:04.5] She can weigh around five hundred kilos, about seven of you packed into one torpedo.
ON SCREEN: Stat "~500 KG" counting up; icon row of 7 YOU figures
[1:10.2] Most seals look like sleepy dogs.
ON SCREEN: TAG "MOST SEALS" over the round-headed harbour seal
[1:12.5] This one looks like a reptile: long flat skull, head too big for its body.
ON SCREEN: TAG "LEOPARD SEAL"; skull outline highlights
[1:17.5] And the smile is a trick.
ON SCREEN: PUNCH "THE SMILE"
[1:19.2] The corners of its mouth curve up, so at rest it looks pleased to see you.
ON SCREEN: mouth-line highlight
[1:23.7] It's really a jaw that opens very, very wide.
ON SCREEN: TAG "NOT A SMILE: A JAW LINE"
[1:26.9] How wide? Wide enough to close over something you'd never expect. We'll get to that.
ON SCREEN: jaw opens to 75°; a grey "?" card inside the gape (no camera shown)
[1:32.2] Its front fangs grow up to two and a half centimetres, about the top joint of your thumb.
ON SCREEN: fang next to a thumb silhouette, ScaleBar "2.5 CM"
[1:37.4] Puppy face. Crocodile job.
ON SCREEN: split card "FACE: PUPPY / JOB: CROCODILE"; slot 1 "THE FACE" stamped

### [1:39] R2 DIET (exhibit 2)

[1:39.8] So what fills a mouth like that?
ON SCREEN: KICKER "ON THE MENU"
[1:41.7] Often? Krill.
ON SCREEN: PUNCH "KRILL."
[1:43.1] Shrimp-like animals about as long as your little finger.
ON SCREEN: krill swarm; TAG "~6 CM ≈ YOUR LITTLE FINGER"
[1:46.8] Behind the fangs sit back teeth shaped like little three-pronged forks.
[1:51.1] Clamp them together and they make a sieve.
ON SCREEN: tooth row, three-cusp teeth interlock into a grid, TAG "A SIEVE"
[1:53.5] In a 2013 study at Sydney's Taronga Zoo, captive seals sucked in water, squirted it out through the gaps and kept the krill.
ON SCREEN: map pin "TARONGA ZOO, SYDNEY · 2013 STUDY"; then 3-step diagram SUCK / SQUIRT / KEEP
[2:02.3] That's how a baleen whale feeds, done by an animal that would fit in your garage.
ON SCREEN: blue whale silhouette vs the seal inside a garage outline, TAG "SAME TRICK"
[2:07.3] Then it eats everything else: fish, squid, six kinds of penguin, and other seals, up to young elephant seals.
ON SCREEN: icon row FISH / SQUID / 6 penguins, then a prey ladder of seal silhouettes, each bigger
[2:15.1] The only thing in the sea that hunts a leopard seal is an orca.
ON SCREEN: orca silhouette drifts over, TAG "ONLY PREDATOR"
[2:19.1] Picky eater, it is not.
ON SCREEN: slot 2 "EATS EVERYTHING" stamped

### [2:20] R3 THE ICE EDGE (exhibit 3, closes the airborne penguin)

[2:21.0] Every penguin colony has a doorway: the strip of water at the ice edge where birds dive in to feed and scramble out to get home.
ON SCREEN: cross-section of a colony on the floe; dashed strip at the edge labelled "THE DOORWAY"
[2:29.6] It's also the only way out of the water for you.
ON SCREEN: YOU at the edge, TAG "YOUR WAY OUT TOO"
[2:32.5] Station crews even fit guards to their rubber boats, because the seals keep biting the tubes.
ON SCREEN: small inflatable at the edge; bite marks on the black tube, guard panel slides on (throwaway, paid in the climax)
[2:38.6] Leopard seals know exactly where the doorways are, including yours.
[2:43.2] One cruises just under the surface along the edge, almost hidden, and waits.
ON SCREEN: seal patrols under the edge, nostrils at the surface
[2:48.3] So penguins don't just climb out here. They launch themselves out of the water and onto the ice.
ON SCREEN: penguins rocket out onto the floe
[2:54.1] That's why the penguin by your boot came out flying.
ON SCREEN: ghost replay of the 0:11.6 penguin; TAG "IT WAS ESCAPING"
[2:56.9] The ones that don't make it get grabbed, often by the feet, and beaten against the surface.
ON SCREEN: PUNCH "GRAB"; lunge, hard cut to splash rings + feather puff (no gore)
[3:02.5] Then the seal whips them side to side to tear off pieces it can swallow.
ON SCREEN: motion streaks only
[3:06.9] Older books said it skinned them on purpose. Researchers now think it simply can't chew.
ON SCREEN: old book page "SKINS ITS PREY", red stamp "WRONG"; TAG "CAN'T CHEW"
[3:12.3] Which, if you're the penguin, is not much of an improvement.
ON SCREEN: slot 3 "OWNS THE ICE EDGE" stamped
[3:15.9] And that still isn't the strangest thing it does to penguins.
ON SCREEN: turnstile: hard cut to a new background on the next word

### [3:19] R4 THE GAME (exhibit 4)

[3:19.6] Remember that catch-and-release?
ON SCREEN: KICKER "IT DOESN'T ALWAYS EAT"
[3:21.6] Divers and film crews have watched leopard seals grab a penguin, let it go, wait for it to race for the ice, and grab it again.
ON SCREEN: loop diagram GRAB -> RELEASE -> CHASE -> GRAB, counter x1, x2, x3
[3:30.2] Sometimes over and over, without ever eating it.
[3:33.3] Is it practice?
ON SCREEN: list item 1 "PRACTICE?"
[3:34.5] Is it play?
ON SCREEN: list item 2 "PLAY?"
[3:35.6] Or is it just a seal that's already full, killing time?
ON SCREEN: list item 3 "KILLING TIME?" with a tiny clock
[3:38.8] Honestly, nobody has pinned it down.
ON SCREEN: red stamp "UNSOLVED" across all three
[3:41.1] Which is not a comforting thing to wonder while you're the new thing in its water.
ON SCREEN: slot 4 "PLAYS WITH PREY" stamped

### [3:46] R5 SENSES AND SONG (exhibit 5, closes the trill)

[3:46.1] So how does a lone hunter find a penguin, or you, in all that ice and murk?
ON SCREEN: KICKER "HOW DOES IT FIND YOU?"
[3:51.3] Partly with its face.
[3:52.8] Like other seals, its whiskers are probably tuned to the faint wakes of swimming animals, and its big eyes suit dim water.
ON SCREEN: whisker fan; a swimming penguin leaves a wavy wake the whiskers trace; TAG "PROBABLY"
[4:01.1] And partly, it listens.
[4:02.8] Which brings us back to that trill from the start.
ON SCREEN: flashback tint: the raft from 0:17.3, rings under the ice
[4:05.4] In the southern summer, male leopard seals sing.
ON SCREEN: PUNCH "IT SINGS"
[4:08.5] A male hangs upside down, rocking from side to side with his chest pulsing, and calls for hours every day.
ON SCREEN: seal upside down (layer rotate 180 + flip), slow rock; rings pulse from the chest
[4:16.1] Those calls reach about 177 decibels underwater, in five distinct types, loud enough to reach you through the ice.
ON SCREEN: Stat "177 dB (UNDERWATER)"; five waveform chips 1-5; rings climb into the floe
[4:25.2] Probably to claim space or call in females. Nobody's certain.
ON SCREEN: TAG "WHY? UNCONFIRMED"
[4:29.7] Either way, if you can hear one through the ice, there's a big male somewhere below you.
[4:35.0] And you can't see him.
ON SCREEN: PUNCH "SOMEWHERE BELOW YOU"; slot 5 "HEARS AND SINGS" stamped

### [4:36] RE-IMMERSION (picture it again)

[4:36.6] So go back to your floe.
ON SCREEN: same framing as 0:00
[4:38.2] You're kneeling on the exact strip where it waits.
ON SCREEN: the dashed "DOORWAY" strip appears under your floe
[4:40.9] Something that eats seals, plays with what it catches, and sings under your feet is looking up at you.
ON SCREEN: three exhibit icons fly in around the face: EATS SEALS / PLAYS / SINGS
[4:47.3] You might be worse than prey.
[4:49.0] You might be interesting.
ON SCREEN: PUNCH "INTERESTING"

### [4:50] R6 THE RECORD (exhibit 6, closes the 1916 teaser)

[4:50.8] Which brings the case file to people.
ON SCREEN: KICKER "AND PEOPLE?"
[4:52.9] In 1916, Shackleton's crew were stranded on drifting sea ice, eating whatever seals they could catch.
ON SCREEN: sepia document card "ENDURANCE EXPEDITION · 1916"; tents on a floe
[5:00.6] Thomas Orde-Lees was skiing back to camp when a leopard seal lunged out of the water at him.
ON SCREEN: seal head and foreparts over a floe ridge; stick figure on skis
[5:06.5] He ran. It dived, tracked his shadow from under the ice, and burst up ahead of him.
ON SCREEN: dotted chase path; the seal vanishes and reappears ahead
[5:11.9] Frank Wild, the second in command, shot it.
ON SCREEN: TAG "FRANK WILD"; single off-screen crack, freeze frame (no gun shown)
[5:14.6] Then the crew ate it, the most Shackleton ending possible.
ON SCREEN: tin plate icon, TAG "DINNER"
[5:18.0] In 1985, explorer Gareth Wood was standing on sea ice when a leopard seal burst through, grabbed his leg and tried to drag him in.
ON SCREEN: plain card "1985 · GARETH WOOD"; YOU-figure at an ice crack, seal head rising
[5:27.6] It bit him twice. His companions kicked it in the head with their spiked boots until it let go.
ON SCREEN: TAG "BITTEN TWICE · KICKED FREE"
[5:33.4] (SILENCE 5.0 s)
ON SCREEN: tonal pivot: music fades to a single pad; still, empty grey sea; no text
[5:38.4] In July 2003, near Britain's Rothera research station, marine biologist Kirsty Brown was snorkelling with a colleague when a leopard seal pulled her under.
ON SCREEN: map pin "ROTHERA RESEARCH STATION"; calm text card "KIRSTY BROWN · MARINE BIOLOGIST · JULY 2003" (no depiction of the event)
[5:49.6] It held her under for around six minutes, as deep as seventy metres.
[5:54.1] Her team could not save her.
[5:55.8] She was twenty-eight.
[5:57.2] It is still the only known human death caused by a leopard seal.
ON SCREEN: TAG "1 KNOWN HUMAN DEATH"; slot 6 "HAS KILLED" closes quietly (grey stamp)
[6:01.0] (SILENCE 3.0 s)
ON SCREEN: black card, silence

### [6:04] CLIMAX: YOUR OPTIONS (a hypothetical; verdict at 74%)

[6:04.0] Now, a hypothetical, and only that.
ON SCREEN: TAG "HYPOTHETICAL"
[6:06.1] Your floe tips, and you slide into the water. A long grey shape turns toward you.
ON SCREEN: surface-split side view: YOU in the water at the floe edge; seal silhouette rising below
[6:11.4] What can you actually do?
ON SCREEN: Options "YOUR OPTIONS: 1 SWIM FOR THE BOAT / 2 CLIMB BACK ONTO THE ICE / 3 HIDE UNDER THE FLOE / 4 PLAY DEAD"
[6:12.9] Option one: swim for the boat.
[6:15.0] Leopard seal bursts are often quoted at around forty kilometres an hour. You, soaked and freezing, might manage three.
ON SCREEN: SpeedBars SEAL ~40 KM/H vs YOU ~3 KM/H
[6:23.1] And remember what it likes to bite on boats.
ON SCREEN: bitten tube from 2:32.5; option 1 struck
[6:25.6] Option two: climb back onto the ice.
[6:28.1] That edge is its ambush strip. Gareth Wood was standing on ice when one grabbed him, and Orde-Lees learned it can follow you from underneath.
ON SCREEN: "THE DOORWAY" strip + 1985 card + the 1916 chase path; option 2 struck
[6:37.0] Option three: dive under the floe and hide.
[6:39.8] Every kick of your legs leaves a wake, and those whiskers are probably tuned to read it.
ON SCREEN: under-ice view; wavy wake lines trail behind YOU toward the whiskers
[6:45.2] That's hide-and-seek while ringing a bell.
ON SCREEN: a cartoon bell over YOU rings with every kick; option 3 struck
[6:47.5] Option four: go limp and play dead.
[6:49.9] This is the animal that catches things, lets them go, and catches them again.
ON SCREEN: the GRAB -> RELEASE loop from R4 with YOU in the penguin's slot
[6:55.2] Holding still doesn't end the game. It just makes you a quieter toy.
ON SCREEN: option 4 struck
[6:59.6] Which closes the case.
[7:01.2] If a leopard seal decides you're worth its time, the water is its home, the ice is its trap, and you're out of moves.
ON SCREEN: black card, white "THE WATER IS ITS HOME. THE ICE IS ITS TRAP." then red "OUT OF MOVES."

### [7:09] TWIST: RESTRAINT

[7:09.4] And yet, here's what doesn't fit the case.
ON SCREEN: KICKER "BUT..."
[7:11.7] Remember: most people who share its water climb out fine.
ON SCREEN: the grey 0:45.6 TAG "MOST CLIMB OUT FINE?" returns, now white
[7:15.2] Scientists have dived near leopard seals for decades, and over a hundred thousand visitors a season now come to Antarctica.
ON SCREEN: Stat "100,000+ VISITORS A SEASON"; research divers and kayak dots on the Peninsula map
[7:23.7] Almost every meeting in the water ends the same way.
[7:27.0] The seal circles, stares, opens that huge mouth in what looks like a warning, and leaves.
ON SCREEN: four-step strip CIRCLE / STARE / GAPE / LEAVE
[7:32.9] One known death, in decades of people working in its water.
ON SCREEN: a row of field-season ticks 1960s -> 2020s, one grey tick at 2003; TAG "1 KNOWN DEATH · DECADES OF DIVING"
[7:36.9] For an animal this well armed, that's a lot of restraint.
ON SCREEN: PUNCH "RESTRAINT"
[7:40.7] Most of the time, you're not lunch. You're the odd new thing it checks out, like a cat inspecting a box.
ON SCREEN: the seal peers at a boxy YOU from every side, cat-style
[7:47.3] Which brings us to the strangest leopard seal story of all.
ON SCREEN: CASE FILE "EXHIBIT 7: ???" pulses

### [7:50] PAYOFF: THE GIFT (exhibit 7)

[7:50.8] In 2006, photographer Paul Nicklen slipped into the water off the Antarctic Peninsula beside one of those big females, around three and a half metres by his estimate.
ON SCREEN: map pin "ANTARCTIC PENINSULA · 2006"; diver with camera beside the seal, ScaleBar "~3.5 M"
[8:02.8] First she swam straight at him and opened that enormous mouth over his camera.
ON SCREEN: the 1:26.9 gape shot, now with the diver's camera inside
[8:08.0] And his head.
ON SCREEN: PUNCH "AND HIS HEAD"
[8:09.4] Then she backed off, and came back with a penguin.
ON SCREEN: PUNCH "A PENGUIN"
[8:12.4] A live one. She let it go right in front of him.
ON SCREEN: card "GIFT 1: LIVE"
[8:15.3] When he didn't take it, she tried again.
ON SCREEN: card "GIFT 2: LIVE"
[8:17.5] Then she brought them injured, easier to catch.
ON SCREEN: card "GIFT 3: SLOWER"
[8:20.4] Then dead.
ON SCREEN: card "GIFT 4: READY TO EAT" (limp cartoon penguin, nothing drawn)
[8:22.2] By his own account, she pushed penguins against his lens, blew bubbles in his face when he didn't eat, and kept it up for four days.
ON SCREEN: Stat "DAY 1" -> "DAY 4"; bubble stream over the camera
[8:30.9] He came away sure of her verdict. Clumsy thing. Big eye. Can't hunt. Needs feeding.
ON SCREEN: her verdict typed as four short lines over the diver; TAG "USELESS HUNTER (HER VIEW)"
[8:36.2] Honestly? Fair review.
ON SCREEN: small stamp "FAIR"
[8:38.2] Remember the game with the penguins?
ON SCREEN: the R4 loop diagram returns, the arrow now points from seal to diver
[8:40.3] Researchers who filmed leopard seals sharing a carcass at South Georgia suggest offerings like this might be an offer to cooperate.
ON SCREEN: map pin "SOUTH GEORGIA"; two seals share one penguin; TAG "AN OFFER TO COOPERATE?"
[8:49.0] Either way, the habit that makes this seal frightening is the same one that made it try to look after a person.
ON SCREEN: slot 7 fills "FED A HUMAN", stamped in yellow, not red

### [8:55] BOOKEND

[8:55.6] So, back on your floe.
ON SCREEN: exact framing of 0:00
[8:57.0] The rule said only the cold was out to get you. Fair enough: the cold is still far more likely to kill you.
ON SCREEN: TAG "-2 °C WATER" returns with its green tick
[9:04.0] But that trill under your knees is a male, singing upside down somewhere below.
ON SCREEN: rings under the floe
[9:09.2] The penguin that flew past your boot was getting away from something.
ON SCREEN: airborne penguin replay, ghosted
[9:13.3] And the face at the edge of the floe isn't friendly. It's curious.
ON SCREEN: PUNCH "CURIOUS"
[9:17.5] If you're very lucky, lunch is on her.
ON SCREEN: a penguin slides onto the floe at your knees; YOU shrugs

### [9:20] CTA

[9:20.4] Walrus or elephant seal: who should we put you in the water with next?
ON SCREEN: Headline "WALRUS OR ELEPHANT SEAL?"
[9:25.0] Tell us in the comments.
ON SCREEN: finished CASE FILE board (7 stamps) held 5 s with end-screen slot; no subscribe plea


## Notes on the rewrite

- The setup is now hook (cold / orcas / wrong pole / rule) -> 3 credentials -> promise. The old 0:37-0:50 misdirect list that repeated the cold is gone; the polar-bear gag lives in the hook.
- The 2003 case is never a teaser. Credential 3 is the 1916 Orde-Lees chase, the counterpart of SPERM's Essex. Brown's death is told only inside R6, after a 5 s silent pivot, followed by a 3 s black card, and the climax opens on "Now, a hypothetical" with a different scenario.
- Ladder order is body -> diet -> ice edge -> the game -> senses and song -> the record. The two penguin rungs sit together, joined by the JELLY turnstile, and the senses rung now feeds climax option 3.
- The anonymous gape plant (1:26) is paid by a 3-word reveal (8:08), not a retell.


## Shot list

Kit vocabulary: core layers (`rect`, `circle`, `text`, `svg`, `particles`, `component`), camera (`pushIn`, `pullOut`, `panUp`, `drift`, keyframes, `shake`), transitions (`cut`, `fade`, `dipBlack`, `whip`), `grade`, core `captions`; explainer kit `Ocean`, `Diver`, `You`, `Seal` (existing harbour seal, used as the round-headed contrast seal and for the prey ladder via `pxPerM`), `Krill`, `Orca`, `BlueWhale`, `Grizzly` (white `silhouette` = polar bear), `ScaleBar`, `Stat`, `Map` (`views`, `pins`), `Options` (`itemAt`, `strikes`, `select`), `SpeedBars`, `Headline`, `Tag`. `storyboard.json` next to this file is generated from this table by `gen.py` and validates against `studio/src/core/schema.ts`.

**Asset scope (build before scheduling).** 5 NEW components (`LeopardSeal`, `Penguin`, `IceFloe`, `RIB`, `CaseFile`) plus 3 NEW figure options on existing components (`You` kneel/lying/camera, `Diver` camera). The GRAB -> RELEASE loop (R4, climax option 4, payoff) is one reusable inline `svg` in `shots.py`, as are the fang, tooth sieve, old book page, tin plate, bell, garage outline, season timeline and CIRCLE/STARE/GAPE/LEAVE strip (9 small `svg` props, already drawn). `LeopardSeal` carries about 30 of the 49 shots, so it is built first. Not needed any more: GenericSeal (existing `Seal`), globe (Map pan), polar-bear art (white `Grizzly`), tents and a separate Orde-Lees figure (`You` `run`), top-down ocean (side views only), `Timer` day counter (`Stat` with `prefix: 'DAY '`).

**Map data (kit gap, shared file not edited here).** `mapdata.ts` needs PLACES `antarcticPeninsula: [-63, -65]`, `rothera: [-68.13, -67.57]`, `southGeorgia: [-36.5, -54.3]`, and two outlines: a ~20-point Antarctic Peninsula (Natural Earth 1:50m subset between lon -76..-55, lat -75..-63; Adelaide Island as its own polygon so the Rothera pin lands on land) and a ~12-point South Georgia polygon (lon -38.1..-35.7, lat -54.9..-53.9). Until then the storyboard pins by lon/lat, and Rothera sits just off the crude coast, which is where Adelaide Island is.

**SFX mapping (no missing cues).** Every cue in the table is an existing file in `studio/public/sfx`: ice creak = `door_creak` pitched down at -10 dB; jaw = `door_creak`; stamp = `knock` at -6 dB; strike = `click`; comic sting = `stinger`; chime = `ding`; counter = `tick`; tension = `heartbeat_slow`; crack = `impact`; low hit = `boom`; paper/card slides = `whoosh`. Cut: colony chatter, rubber squeak, wind bed. One NEW cue, `seal_trill`, drives the hook and loop A, so it must be synthesised on the Spark (descending FM trill, 200 -> 80 Hz, with a sub-bass layer, 3-4 s) and approved before the hook is built; the storyboard uses `underwater_rumble` as its stand-in.

**Build order and the 10-second gate.** LeopardSeal (profile + jaw cap + surface pose) -> IceFloe -> You kneel + camera -> Penguin -> CaseFile -> RIB. Then render shots 1-6 (0:00-0:31) as the gate test: they use 4 of the 5 new components and the trill cue. Look-dev frame for shot 9 (two `lying` YOU at `pxPerM: 400`) with `scripts/spark_stills.sh` before the full render.

**Cut rate.** 49 shots in 571.29 s is about 5 per minute, inside Depth Theory's 3.1-5.4 hard cuts per minute (R1 videos.json); adjacent same-setup shots from the previous draft were merged (hook tags, krill + sieve, ladder + orca, myth + stamp, game + options, gifts + days).


| # | t_start | t_end | shot type | visual description (kit vocabulary) | camera move | SFX (existing `studio/public/sfx` names) |
|---|---|---|---|---|---|---|
| 1 | 0:00.0 | 0:05.2 | wide, surface split | `Ocean` `surface: 0.46`, low gold sky; NEW `IceFloe` (keel) centre; `You` NEW `kneel` + NEW `camera` prop on the floe; NEW `LeopardSeal` `silhouette` with spots slides under the keel left to right (frame 1; YOU never looks down); `Headline` "ANTARCTIC PENINSULA"; at 0:03.3 `Tag` "ORCAS" + green tick | slow `pushIn` 1.0 -> 1.05 | `door_creak` pitched down -10 dB (ice creak), NEW `seal_trill` sub-bass only (until approved: `underwater_rumble` -12 dB) |
| 2 | 0:05.2 | 0:07.6 | map gag | `Map` `views` whip from Antarctica (lat -70) to the Arctic (lat 75); white `Grizzly` (`silhouette: '#f3f6f7'`) as the polar bear; `Tag` "WRONG POLE" + red cross | `whip` in | `whoosh`, `pop` on the cross |
| 3 | 0:07.6 | 0:11.5 | wide, surface split (0:00 framing) | 0:00 framing held; `Tag` "-2 °C WATER" + green tick, then `Tag` "THE ONLY THREAT?" | hold | `tick` |
| 4 | 0:11.5 | 0:17.2 | medium, fast | NEW `Penguin` `pose: airborne` arcs out of the water past the YOU figure's boot (keyframes x/y/rotate); red `Headline` "AIRBORNE" | `shake` 0.3 s on the launch | `bubbles` + `whoosh` |
| 5 | 0:17.2 | 0:21.9 | under/over split | camera dips under the waterline: dark under-ice, concentric `circle` rings rise through the keel into the kneeling figure's knees | `panUp` from under the ice | NEW `seal_trill` (stand-in `underwater_rumble`), music out |
| 6 | 0:21.9 | 0:30.0 | close, surface | NEW `LeopardSeal` `pose: surface` side-profile head over the floe edge, mouth line curved up (no front view); `Headline` "LEOPARD SEAL"; red "IT ISN'T SMILING"; `jaw` 0 -> 8° | slow `pushIn` to the face, `dipBlack` out | `boom` low on the punch |
| 7 | 0:30.0 | 0:41.4 | graphic (CASE FILE) | NEW `CaseFile` full frame, title "THE CASE AGAINST THE LEOPARD SEAL", `slots: 7`; credentials pop in left: "HUNTS OTHER SEALS", "PLAYS WITH ITS FOOD" (tiny penguin toss loop), red "1916: ?" sealed envelope | small `drift` | `whoosh` (paper), `knock` -6 dB per credential |
| 8 | 0:41.4 | 0:55.1 | wide, deep | `Ocean` `depth: 30`; small kneeling YOU on a floe at the top, big `LeopardSeal` `pose: cruise` below; `Headline` "WHY YOU'D NEVER WANT TO MEET ONE"; small grey `Tag` "MOST CLIMB OUT FINE?" (the quiet qualifier); `CaseFile` insert slot 7 "EXHIBIT 7: ???" grey + `Tag` "4 DAYS · 0 BITES" | slow `panUp` | music bed returns |
| 9 | 0:55.1 | 1:04.3 | side profile, true scale | `LeopardSeal` `pxPerM: 400` (3.5 m = 1400 px) with two `You` NEW `lying` pose end to end below at the same `pxPerM`; `ScaleBar` "~3.5 M"; `Tag` "BIGGEST = FEMALES" | `pushIn` | `tick` on the bar |
| 10 | 1:04.3 | 1:10.0 | graphic | `Stat` "~500 KG" count-up; row of 7 `You` figures dropping in | hold | `tick` roll |
| 11 | 1:10.0 | 1:17.4 | split | left: existing `Seal` (round-headed harbour seal) `Tag` "MOST SEALS"; right: `LeopardSeal` head with an `svg` skull-outline highlight, `Tag` "LEOPARD SEAL" | `whip` left -> right | `whoosh` |
| 12 | 1:17.4 | 1:26.7 | close, head | `LeopardSeal` head close, `highlight: 'mouth'` traces the upturned mouth line; red "THE SMILE"; `Tag` "NOT A SMILE: A JAW LINE" | `pushIn` to the mouth |  |
| 13 | 1:26.7 | 1:32.0 | close | `LeopardSeal` `jaw` 0 -> 75° (cap; no fold-through) around a grey "?" card (the plant: nothing named, no camera shown) | `shake` small on the open | `door_creak` (jaw) |
| 14 | 1:32.0 | 1:39.7 | macro graphic | `svg` fang beside a thumb silhouette, `ScaleBar` "2.5 CM"; split card "FACE: PUPPY / JOB: CROCODILE"; `CaseFile` insert, slot 1 "THE FACE" stamped | `pullOut` | `knock` -6 dB (stamp) |
| 15 | 1:39.7 | 1:53.3 | macro | `Headline` "ON THE MENU" -> red "KRILL."; existing `explainer/Krill` swarm (several layers with `timeOffset`); `Tag` "~6 CM ≈ YOUR LITTLE FINGER"; then `svg` tooth row: three-cusp teeth interlock into a grid, `Tag` "A SIEVE" | `pushIn` on the teeth | `pop` |
| 16 | 1:53.3 | 2:02.1 | map + diagram | `Map` `views` zoom to `sydney`, pin "TARONGA ZOO, SYDNEY · 2013 STUDY"; then 3-step text diagram SUCK / SQUIRT / KEEP | log-zoom | `whoosh_long` |
| 17 | 2:02.1 | 2:07.2 | scale gag | `BlueWhale` silhouette fills the top; the seal inside a garage outline (`svg`) below; `Tag` "SAME TRICK" | `pullOut` |  |
| 18 | 2:07.2 | 2:20.8 | ladder | icon `text` row FISH / SQUID; 6 `Penguin` silhouettes; then a prey ladder of existing `Seal` silhouettes growing left to right (crabeater pup, Weddell, fur seal pup, young elephant seal via `pxPerM`); `Orca` drifts in above, `Tag` "ONLY PREDATOR"; `CaseFile` insert, slot 2 "EATS EVERYTHING" stamped | `drift` right | `pop` per icon, `knock` (stamp) |
| 19 | 2:20.8 | 2:38.5 | cross-section | NEW `IceFloe` with a penguin colony on top, `edgeStrip` dashed band "THE DOORWAY"; penguins diving in and scrambling out; YOU at the edge, `Tag` "YOUR WAY OUT TOO"; NEW `RIB` at the edge, `bites` marks appear on the black tube and a guard panel slides on, `Tag` "TUBE GUARDS" (throwaway plant) | slow `pushIn` to the edge | `bubbles` (dives) |
| 20 | 2:38.5 | 2:48.1 | under-surface | `LeopardSeal` `pose: cruise`, `idle: false`, slight `rotate`, patrols under the edge with only the nostrils above the waterline | `drift` | `heartbeat_slow` -12 dB |
| 21 | 2:48.1 | 2:56.8 | medium | three `Penguin` `pose: airborne` rocket out onto the floe; ghosted replay of the 0:12 penguin past the boot (`opacity` 0.5), `Tag` "IT WAS ESCAPING" | hold | `whoosh` x3 |
| 22 | 2:56.8 | 3:06.8 | action, stylised | `LeopardSeal` `pose: lunge` up at a swimming `Penguin`; red "GRAB"; hard cut on contact to splash `circle` rings + white feather-puff `particles` (`dust`); then motion streaks only (no penguin in the mouth, no gore) | `shake` 0.4 s | `impact`, `bubbles` |
| 23 | 3:06.8 | 3:19.5 | graphic | `svg` old book page "SKINS ITS PREY" with a red "WRONG" stamp; `Tag` "CAN'T CHEW"; `CaseFile` insert, slot 3 "OWNS THE ICE EDGE" stamped; on 3:15.9 (turnstile) the frame darkens to near black | `whip` in | `knock` (stamp) |
| 24 | 3:19.5 | 3:45.9 | diagram (new background on the turnstile's next word) | new deep-blue background; `Headline` "IT DOESN'T ALWAYS EAT"; NEW `LoopDiagram` (or `svg`) GRAB -> RELEASE -> CHASE -> GRAB with `Penguin` + seal icons, counter x1, x2, x3; then `Options` "PRACTICE? / PLAY? / KILLING TIME?" (`itemAt` per question) and a red "UNSOLVED" stamp; `CaseFile` insert, slot 4 "PLAYS WITH PREY" stamped | hold, loop animates | `click` per loop, `knock` (stamp) |
| 25 | 3:45.9 | 4:02.7 | close, murk | `Ocean` `depth: 60`, `snow` heavy; seal head with `highlight: 'whiskers'` fan; a swimming `Penguin` leaves a wavy `svg` wake the whiskers trace; `Tag` "PROBABLY" | `pushIn` | `whoosh_long` soft |
| 26 | 4:02.7 | 4:08.4 | flashback | `grade` warm-sepia tint; the 0:18 under-ice shot with rings rising into the floe; red "IT SINGS" | `dipBlack` in | NEW `seal_trill` returns, clearer |
| 27 | 4:08.4 | 4:29.5 | medium | `LeopardSeal` upside down (layer `rotate: 180` + `flipX`), `idle` `sway` for the rock; `circle` rings from the chest; `Stat` "177 dB (UNDERWATER)"; five waveform chips 1-5; rings climb into a tiny floe; `Tag` "WHY? UNCONFIRMED" | slow `drift` | trill layered |
| 28 | 4:29.5 | 4:36.5 | wide | rings expand to fill the frame and pass under a tiny floe with a tiny kneeling YOU; red "SOMEWHERE BELOW YOU"; `CaseFile` insert, slot 5 "HEARS AND SINGS" stamped | `pullOut` wide | `knock` (stamp) |
| 29 | 4:36.5 | 4:50.6 | wide, surface split (0:00 framing) | exact 0:00 framing; `IceFloe` `edgeStrip` doorway band appears under the kneeling YOU; three exhibit icons (text chips) EATS SEALS / PLAYS / SINGS orbit the rising face; red "INTERESTING" | slow `pushIn` | `door_creak` low, trill |
| 30 | 4:50.6 | 5:17.8 | sepia story | `Headline` "AND PEOPLE?"; `grade` sepia; document card "ENDURANCE EXPEDITION · 1916" (`text` on a paper `rect`); tents on a floe; `You` `pose: run` on skis as Orde-Lees; `LeopardSeal` head and foreparts only, over a floe ridge (no body on the snow); dotted chase path; the seal drops out of frame and reappears ahead; `Tag` "FRANK WILD"; freeze; tin plate `svg`, `Tag` "DINNER" | `drift` along the chase, freeze | `footsteps`, `impact` (single off-screen crack, no gun shown), `stinger` on DINNER |
| 31 | 5:17.8 | 5:33.4 | plain story card | neutral grade; card "1985 · GARETH WOOD"; a standing figure at an ice crack, seal head rising through it; `Tag` "BITTEN TWICE · KICKED FREE" (no jokes from here to the 2003 card) | slow `pushIn` | none |
| 32 | 5:33.4 | 5:38.2 | tonal pivot (silence) | 5 s of still, empty grey sea under an overcast sky; no text, no figure; music down to a single pad | locked off | none |
| 33 | 5:38.2 | 6:03.9 | sober, still | `Map` `views` zoom to NEW place `rothera`, pin "ROTHERA RESEARCH STATION"; calm text card "KIRSTY BROWN · MARINE BIOLOGIST · JULY 2003"; `Tag` "1 KNOWN HUMAN DEATH"; `CaseFile` insert, slot 6 "HAS KILLED", grey stamp; then 3 s black card (silence) | very slow `pushIn`, no shake | none (pad only) |
| 34 | 6:03.9 | 6:12.8 | surface-split side view | `Tag` "HYPOTHETICAL"; side view: YOU (`pose: panic`) in the water at the floe edge, a long seal silhouette rising below (no top-down shot); `Options` appears (4 items) | slow `pushIn` | `heartbeat_slow` (tension pulse) |
| 35 | 6:12.8 | 6:25.4 | graphic | `SpeedBars` SEAL ~40 KM/H vs YOU ~3 KM/H; the bitten `RIB` tube from 2:32.5 (callback); `Options` `strikes` index 0 | hold | `click` (strike) |
| 36 | 6:25.4 | 6:36.9 | cross-section | the doorway strip + the 1985 card + the 1916 chase path overlay; `strikes` index 1 | `whip` in | `click` |
| 37 | 6:36.9 | 6:47.4 | under-ice gag | under the floe: YOU kicking, wavy `svg` wake lines trail toward the seal's whisker fan; a cartoon bell (`svg`) over YOU wobbles on every kick; `strikes` index 2 | `panUp` under the ice | `ding` per kick (the bell), `stinger` on the joke, `click` |
| 38 | 6:47.4 | 6:59.5 | diagram | the R4 GRAB -> RELEASE loop with `You` `pose: panic` in the penguin's slot; `strikes` index 3 | hold | `click` |
| 39 | 6:59.5 | 7:09.2 | black card | `Headline` white "THE WATER IS ITS HOME. THE ICE IS ITS TRAP." then red "OUT OF MOVES." | hold, `dipBlack` out | single `boom`, then silence |
| 40 | 7:09.2 | 7:23.6 | map | `Headline` "BUT..."; the grey qualifier `Tag` from 0:45.6 returns white: "MOST CLIMB OUT FINE"; `Map` Antarctic Peninsula with research-diver and kayak dots multiplying; `Stat` "100,000+" label "VISITORS A SEASON" (VO says the same figure) | slow `pullOut` | music bed returns |
| 41 | 7:23.6 | 7:32.7 | strip | four panels CIRCLE / STARE / GAPE / LEAVE (`svg` labels) over a seal and a `Diver` | `drift` right |  |
| 42 | 7:32.7 | 7:40.6 | timeline | row of field-season ticks 1960s -> 2020s (`svg`), one grey tick at 2003 (no per-icon death ratio); `Tag` "1 KNOWN DEATH · DECADES OF DIVING"; red "RESTRAINT" | `pushIn` on the grey tick | `heartbeat_slow` once |
| 43 | 7:40.6 | 7:50.6 | gag | a boxy dashed outline around a `You` figure; the seal peers at it from the left, the top, then the right, cat-style (three quick cuts via keyframes); `CaseFile` insert, "EXHIBIT 7: ???" pulses | hold | `pop` per peek |
| 44 | 7:50.6 | 8:09.2 | medium | `Map` pin "ANTARCTIC PENINSULA · 2006" (2 s), then `Diver` with NEW `camera` prop beside `LeopardSeal` and `ScaleBar` "~3.5 M"; the 1:26.9 gape shot again, now with the diver's camera inside the 75° gape; red "AND HIS HEAD" | `pushIn` | `door_creak` (jaw), `boom` low on the punch |
| 45 | 8:09.2 | 8:22.0 | sequence | seal backs off and returns with a `Penguin` (NEW `carry` prop on the seal, so the penguin follows the jaw); counter cards GIFT 1 LIVE / GIFT 2 LIVE / GIFT 3 SLOWER / GIFT 4 READY TO EAT (`Headline` swaps; limp cartoon penguin, nothing drawn); 1 s held beat after "Then dead." | cut on each gift | `pop` per card |
| 46 | 8:22.0 | 8:38.0 | medium | `Stat` `prefix: 'DAY '` from 1 to 4 (no `Timer`); bubble `particles` over the camera; her verdict typed as four short `text` lines over the diver; `Tag` "USELESS HUNTER (HER VIEW)"; small stamp "FAIR" | `drift` | `bubbles`, `typing` for the verdict, `knock` light on FAIR |
| 47 | 8:38.0 | 8:55.4 | diagram + map | the R4 loop `svg` returns with the arrow now running seal -> diver; `Map` pin NEW place `southGeorgia` "SOUTH GEORGIA"; two seals share one penguin; `Tag` "AN OFFER TO COOPERATE?"; `CaseFile` insert, slot 7 "FED A HUMAN", yellow stamp | `whip` | `ding`, `knock` (light stamp) |
| 48 | 8:55.4 | 9:20.3 | wide, surface split (0:00 framing) | exact 0:00 framing; `Tag` "-2 °C WATER" + green tick returns; rings under the floe (the singer); the airborne penguin replay ghosted; the seal face at the edge; red "CURIOUS"; a `Penguin` `pose: limp` slides onto the floe at YOU's knees; `You` `pose: shrug` | slow `pullOut` | trill, `door_creak` low, `bubbles` + `stinger` (comic) on the penguin |
| 49 | 9:20.3 | 9:31.3 | end card | finished `CaseFile` board (7 stamps) full frame held 5 s; `Headline` "WALRUS OR ELEPHANT SEAL?"; end-screen slot right | hold 5 s | music out |

## Narration (TTS source)

Read by `pipeline.audio.make` (Kokoro am_michael). One paragraph per shot so scene cuts land just before each paragraph's first word.

```narration
[speed: 0.82]
You're kneeling on Antarctic sea ice, camera up. Orcas leave people alone.

Polar bears? Wrong pole.

Down here, the only thing out to get you is the cold.

Then a penguin shoots out of the water past your boot. Not swimming. Airborne.

Under the ice, a low trill starts, and you feel it through your knees.

A long face rises at the edge of the floe, smiling up at you. That's a leopard seal. It isn't smiling.

[speed: 0.94] It's the only seal in Antarctica that hunts other seals. It plays catch-and-release with live penguins. And in 1916, one came out of the sea after one of Shackleton's men.

So let's build the case against ever sharing water with one. And work out why most people who do still climb out fine. Then, the strangest leopard seal story on record. It lasted four days, and nobody got bitten.

Start with size. The biggest leopard seals are the females. A big one can reach about three and a half metres: two of you, lying end to end.

She can weigh around five hundred kilos, about seven of you packed into one torpedo.

Most seals look like sleepy dogs. This one looks like a reptile: long flat skull, head too big for its body.

And the smile is a trick. The corners of its mouth curve up, so at rest it looks pleased to see you. It's really a jaw that opens very, very wide.

How wide? Wide enough to close over something you'd never expect. We'll get to that.

Its front fangs grow up to two and a half centimetres, about the top joint of your thumb. Puppy face. Crocodile job.

So what fills a mouth like that? Often? Krill. Shrimp-like animals about as long as your little finger. Behind the fangs sit back teeth shaped like little three-pronged forks. Clamp them together and they make a sieve.

In a 2013 study at Sydney's Taronga Zoo, captive seals sucked in water, squirted it out through the gaps and kept the krill.

That's how a baleen whale feeds, done by an animal that would fit in your garage.

Then it eats everything else: fish, squid, six kinds of penguin, and other seals, up to young elephant seals. The only thing in the sea that hunts a leopard seal is an orca. Picky eater, it is not.

Every penguin colony has a doorway: the strip of water at the ice edge where birds dive in to feed and scramble out to get home. It's also the only way out of the water for you. Station crews even fit guards to their rubber boats, because the seals keep biting the tubes.

Leopard seals know exactly where the doorways are, including yours. One cruises just under the surface along the edge, almost hidden, and waits.

So penguins don't just climb out here. They launch themselves out of the water and onto the ice. That's why the penguin by your boot came out flying.

The ones that don't make it get grabbed, often by the feet, and beaten against the surface. Then the seal whips them side to side to tear off pieces it can swallow.

Older books said it skinned them on purpose. Researchers now think it simply can't chew. Which, if you're the penguin, is not much of an improvement. And that still isn't the strangest thing it does to penguins.

Remember that catch-and-release? Divers and film crews have watched leopard seals grab a penguin, let it go, wait for it to race for the ice, and grab it again. Sometimes over and over, without ever eating it. Is it practice? Is it play? Or is it just a seal that's already full, killing time? Honestly, nobody has pinned it down. Which is not a comforting thing to wonder while you're the new thing in its water.

So how does a lone hunter find a penguin, or you, in all that ice and murk? Partly with its face. Like other seals, its whiskers are probably tuned to the faint wakes of swimming animals, and its big eyes suit dim water. And partly, it listens.

Which brings us back to that trill from the start. In the southern summer, male leopard seals sing.

A male hangs upside down, rocking from side to side with his chest pulsing, and calls for hours every day. Those calls reach about 177 decibels underwater, in five distinct types, loud enough to reach you through the ice. Probably to claim space or call in females. Nobody's certain.

Either way, if you can hear one through the ice, there's a big male somewhere below you. And you can't see him.

So go back to your floe. You're kneeling on the exact strip where it waits. Something that eats seals, plays with what it catches, and sings under your feet is looking up at you. You might be worse than prey. You might be interesting.

Which brings the case file to people. In 1916, Shackleton's crew were stranded on drifting sea ice, eating whatever seals they could catch. Thomas Orde-Lees was skiing back to camp when a leopard seal lunged out of the water at him. He ran. It dived, tracked his shadow from under the ice, and burst up ahead of him. Frank Wild, the second in command, shot it. Then the crew ate it, the most Shackleton ending possible.

In 1985, explorer Gareth Wood was standing on sea ice when a leopard seal burst through, grabbed his leg and tried to drag him in. It bit him twice. His companions kicked it in the head with their spiked boots until it let go.

[pause: 5.0]

In July 2003, near Britain's Rothera research station, marine biologist Kirsty Brown was snorkelling with a colleague when a leopard seal pulled her under. It held her under for around six minutes, as deep as seventy metres. Her team could not save her. She was twenty-eight. It is still the only known human death caused by a leopard seal. [pause: 3.0]

Now, a hypothetical, and only that. Your floe tips, and you slide into the water. A long grey shape turns toward you. What can you actually do?

Option one: swim for the boat. Leopard seal bursts are often quoted at around forty kilometres an hour. You, soaked and freezing, might manage three. And remember what it likes to bite on boats.

Option two: climb back onto the ice. That edge is its ambush strip. Gareth Wood was standing on ice when one grabbed him, and Orde-Lees learned it can follow you from underneath.

Option three: dive under the floe and hide. Every kick of your legs leaves a wake, and those whiskers are probably tuned to read it. That's hide-and-seek while ringing a bell.

Option four: go limp and play dead. This is the animal that catches things, lets them go, and catches them again. Holding still doesn't end the game. It just makes you a quieter toy.

Which closes the case. If a leopard seal decides you're worth its time, the water is its home, the ice is its trap, and you're out of moves.

And yet, here's what doesn't fit the case. Remember: most people who share its water climb out fine. Scientists have dived near leopard seals for decades, and over a hundred thousand visitors a season now come to Antarctica.

Almost every meeting in the water ends the same way. The seal circles, stares, opens that huge mouth in what looks like a warning, and leaves.

One known death, in decades of people working in its water. For an animal this well armed, that's a lot of restraint.

Most of the time, you're not lunch. You're the odd new thing it checks out, like a cat inspecting a box. Which brings us to the strangest leopard seal story of all.

In 2006, photographer Paul Nicklen slipped into the water off the Antarctic Peninsula beside one of those big females, around three and a half metres by his estimate. First she swam straight at him and opened that enormous mouth over his camera. And his head.

Then she backed off, and came back with a penguin. A live one. She let it go right in front of him. When he didn't take it, she tried again. Then she brought them injured, easier to catch. Then dead.

By his own account, she pushed penguins against his lens, blew bubbles in his face when he didn't eat, and kept it up for four days. He came away sure of her verdict. Clumsy thing. Big eye. Can't hunt. Needs feeding. Honestly? Fair review.

Remember the game with the penguins? Researchers who filmed leopard seals sharing a carcass at South Georgia suggest offerings like this might be an offer to cooperate. Either way, the habit that makes this seal frightening is the same one that made it try to look after a person.

So, back on your floe. The rule said only the cold was out to get you. Fair enough: the cold is still far more likely to kill you. But that trill under your knees is a male, singing upside down somewhere below. The penguin that flew past your boot was getting away from something. And the face at the edge of the floe isn't friendly. It's curious. If you're very lucky, lunch is on her.

Walrus or elephant seal: who should we put you in the water with next? Tell us in the comments.
```
