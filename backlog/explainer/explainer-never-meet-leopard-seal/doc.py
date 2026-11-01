"""Static prose of script.md (front matter, alignment table, pacing, facts). {T:id} = line start m:ss, {D:id} = m:ss.s,
{P:id} = % of runtime, {E:id} = line end, {S:key} = computed stat (gen.py)."""

REHOOKS = ["h5", "h9", "s1", "s4", "s6", "r1a", "r1i", "r2a", "r2h", "r3a", "r3f", "r3l", "r4a", "r4d", "r5a", "r5e", "r5j", "ri1",
           "r6a", "r6g", "c1", "c4", "c7", "c9", "c12", "c15", "t1", "t4", "t8", "t9", "p4", "p8", "p12", "b1", "b5", "x1"]
JOKES = ["h3", "r1k", "r2g", "r2j", "r3k", "r4f", "ri5", "r6f", "c11", "c14", "t8", "p8", "p11", "b6"]

FRONT = """---
slug: explainer-never-meet-leopard-seal
niche: explainer
format: long
aspect: "16:9"
title: "Why You Should Never Swim With A Leopard Seal"
title_alt_series: "Why You'd Never Want To Meet A Leopard Seal"
title_formula: "Our own variant of the 'why you'd never want to meet [X]' series formula (PLAYBOOK section 7); see titles.md for the ranked A/B list"
variant: "Dossier (PLAYBOOK 1a): verdict at {P:c16}, then a restraint twist and the gift payoff"
target_runtime_s: {S:total}
target_runtime_range_s: [540, 600]
target_words_per_min: 165        # effective incl. pauses; PLAYBOOK long-form target 160-170, Depth Theory 168
voice: "Kokoro-82M am_michael; hook speed {S:hook_speed}, body speed {S:body_speed} (pipeline.audio.make reads the [speed:] markers in the narration block)"
measured:                        # every number below is computed by gen.py from per-line Kokoro durations measured on the Spark CPU
  timing_source: "{S:timing}"
  vo_words: {S:vo_words}
  vo_runtime_s: {S:vo_span}      # + 5 s end hold = {S:total} s
  effective_wpm_incl_pauses: {S:eff_wpm}
  speech_wpm: {S:speech_wpm}     # body {S:body_speech_wpm}
  hook_words: {S:hook_words}     # immersion hook, target 70-90 words / ~30 s
  hook_s: {S:hook_s}             # rule at {S:rule_s} s, turn at {S:turn_s} s, creature named at {S:name_s} s
  avg_sentence_words: {S:avg_sentence}
  you_pct_words: {S:you_pct_words}           # target >= 3%
  you_pct_sentences: {S:you_pct_sentences}   # target >= 25%
  you_per_min: {S:you_per_min}
  numbers_per_min: {S:numbers_per_min}
  promise_s: {S:promise}         # promise at {T:s4}, EXHIBIT 7 slot at {T:s6}
  first_rung_s: {S:first_rung}   # setup (L1-L3) = {S:setup_pct}% of runtime
  rehook_median_gap_s: {S:rehook_median}
  rehook_max_gap_s: {S:rehook_max}
  joke_max_gap_s: {S:joke_max}   # the only long gap is the deliberate sober stretch around the 2003 case
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
safety: "No gore: the penguin grab cuts to splash rings and a feather puff. The 1985 and 2003 cases are told plainly with cards and a map pin, never depicted. No jokes within 20 s before or after the 2003 case (last joke ends {E:r6f}, case starts {T:r6i}, a 5 s silent pivot sits between). A 3 s black card follows it, and the climax opens on 'Now, a hypothetical' and a different scenario (you slip off a floe), not snorkelling."
description_note: "Add to the YouTube description: 'Narration uses a synthetic voice. All animation is original and code-drawn.'"
post_caption_cta: "Walrus or elephant seal: who should we put you in the water with next?"
---

# Why You Should Never Swim With A Leopard Seal
"""

BODY_BEFORE_SCRIPT = """
## Beat alignment table

| Our beat | Our time | Reference id + timestamp | Device borrowed | How we adapt it |
|---|---|---|---|---|
| L1 Hook: calm scene, threat shown in frame 1 | {T:h1}-{T:h2} | fGcgWaswMns 0:00 (2P placement); PLAYBOOK s2 "name late, show early" | 2P placement in a calm, specific scene; the subject's effect on screen at once | 8-word placement line; the viewer sees a spotted silhouette slide under the keel while YOU doesn't |
| L1 Hook: misdirect checklist + rule | {T:h2}-{E:h4} | fGcgWaswMns 0:04-0:11 (checklist ending on the rule); jw6bS-WL4F4 0:03-0:08 (absurd item) | Usual dangers ticked off, an absurd item, then the safety rule | Orcas (tick), polar bears (wrong pole), "the only thing out to get you is the cold" lands at {D:h4} |
| L1 Hook: turn + sensation | {T:h5}-{E:h7} | fGcgWaswMns 0:14 | Short turn line, then an unexplained body sensation | Penguin bursts past your boot, "Not swimming. Airborne." (loop B); a trill felt through your knees (loop A) |
| L1 Hook: subject named last | {T:h8}-{E:h10} | fGcgWaswMns 0:23 | Creature named at ~90% of the hook, holding the upper hand | Smiling face at the floe edge; named at {D:h9}; "It isn't smiling." (loop C) |
| L2 Credential stack | {T:s1}-{E:s3} | fGcgWaswMns 0:45-0:58 | 3 credentials, the last a dated historical teaser | Hunts other seals; catch-and-release; "in 1916, one came out of the sea after one of Shackleton's men" (loop D, closes {T:r6b}) |
| L3 Promise + quiet qualifier + progress device | {T:s4}-{E:s6} | fGcgWaswMns 0:58 (title restated); VtrcKTkhDHU 0:21 (quiet qualifier), 0:41 (transformation promise) | Title as the video's job; one quiet line the twist will exploit; a concrete paradox teaser | "Build the case" + "why most people who do still climb out fine" (paid {T:t2}) + "four days, nobody got bitten" (loop E); CASE FILE board from {T:s1}, slot 7 grey at {T:s6} |
| R1 Body + face | {T:r1a}-{E:r1k} | fGcgWaswMns 1:02-1:50 (numbers -> body comparisons 1:12, 1:33; "you assumed wrong" 1:19; 2-word punch 1:47) | Number -> you-comparison; anatomy correction; short punch | 3.5 m = two of you; 500 kg = seven of you; the smile is a jaw line; fang vs thumb joint; "Puppy face. Crocodile job." |
| R1 silent plant | {T:r1i} | VtrcKTkhDHU 2:54 (collagen fin, paid 27:54) | Throwaway detail with no owner, paid much later | "Wide enough to close over something you'd never expect" (no name, no camera shown); paid {T:p2}-{T:p3} |
| R2 Diet | {T:r2a}-{E:r2j} | fGcgWaswMns 1:50-1:56 (RQ answered in one word), 2:34-2:36 (everyday metaphor, joke out); dated study shape from 4:26 | RQ -> one word; a dated study; everyday metaphor; joke out | "Often? Krill." (not "mostly"); a 2013 study at Taronga; baleen trick in a garage-sized animal; "Picky eater, it is not." |
| R3 Ice edge (loop B closes) | {T:r3a}-{E:r3k} | fGcgWaswMns 2:42 (where it hunts), 3:45 (explicit "remember...?" close); VtrcKTkhDHU 1:21-2:04 (myth-bust) | Hunting ground as a place; explicit callback close; myth correction | The doorway is also your only exit (plants climax option 2); boat-tube guards as a throwaway (paid {T:c6}); "That's why the penguin by your boot came out flying" at {P:r3g}; skinning myth corrected |
| R3 turnstile | {T:r3l} | jw6bS-WL4F4 0:31 | "Not the worst part" line right after the most graphic image, background change on the next word | "And that still isn't the strangest thing it does to penguins." -> hard cut to the game diagram |
| R4 The game | {T:r4a}-{E:r4h} | fGcgWaswMns 3:50-3:54 (honest "never proven" hedge); VtrcKTkhDHU 16:21 (secondary mystery) | Callback entry, a mini-mystery left honestly open | "Remember that catch-and-release?" escalates credential 2; practice / play / killing time; "nobody has pinned it down" |
| R5 Senses + song (loop A closes) | {T:r5a}-{E:r5k} | fGcgWaswMns 2:58-3:01 (RQ bridge), 3:28 (measured record number), 3:45-3:47 (callback that explains the hook sensation) | RQ bridge; measured number tied to the body; callback reveal | Whiskers and eyes; "that trill from the start" = a male singing upside down; 177 dB "loud enough to reach you through the ice" (closes at {P:r5e}) |
| Re-immersion | {T:ri1}-{E:ri5} | fGcgWaswMns 4:43-4:53 | "Picture it again" with the rungs combined | Back on the floe at {P:ri1}; "You might be interesting." |
| R6 The record (loop D closes) | {T:r6a}-{E:r6m} | fGcgWaswMns 5:00-5:08 (people? -> dated story closing the credential teaser), 5:30 ("not the only one" second case), 5:53 (sympathy seed), 5:57 (joke) | Dated told story; second real case; perspective seed; comic button, then a sober case | Orde-Lees 1916 (crew eating seals, the seal tracks his shadow under the ice, "most Shackleton ending"); Gareth Wood 1985 (bitten twice, kicked free); 5 s silent pivot; Kirsty Brown 2003, told plainly |
| Climax: your options | {T:c1}-{E:c16} | fGcgWaswMns 5:59-7:01 (each option killed by an earlier rung, senses used twice, verdict at 70%) | Numbered escapes, each struck by a callback + a metaphor; flat verdict | Hypothetical, not her scenario. Boat: speed + tubes planted {T:r3c}. Ice: doorway + Wood 1985 + Orde-Lees. Under the floe: whiskers read your wake (R5) + "hide-and-seek while ringing a bell". Play dead: the game (R4). Verdict at {P:c16} |
| Twist: restraint | {T:t1}-{E:t9} | VtrcKTkhDHU 20:19-20:32 (paradox restated, one stark number); fGcgWaswMns 7:05-7:33 (reassurance flip, scale-of-interest analogy) | "Here's what doesn't fit"; the planted qualifier paid; one clean number; humbling analogy | "Most people climb out fine" returns; one known death in decades of research diving; tourists only as context, VO and Stat both "over a hundred thousand"; a cat inspecting a box |
| Payoff: the gift (loop E closes) | {T:p1}-{E:p14} | VtrcKTkhDHU 18:14-19:33 (named, dated story with escalating repetition), 22:14 (inner verdict in short declaratives); fGcgWaswMns 9:22 (opening credential reread as a paradox) | Named story; the plant revealed; the animal's verdict voiced; an earlier fear given a new meaning | Nicklen 2006, one of the big females planted at {T:r1a}; "And his head." pays the {T:r1i} plant; live -> live -> injured -> dead; "Clumsy thing. Big eye. Can't hunt. Needs feeding." + "Fair review."; catch-and-release reread as an offer to cooperate |
| Bookend | {T:b1}-{E:b6} | fGcgWaswMns 9:29-9:44 | Rule restated + concession, then 3 callbacks and a humbling joke | "The cold is still far more likely to kill you"; trill = singer, flying penguin = escape, smile = curiosity; "lunch is on her" |
| CTA | {T:x1}-{E:x2} | fGcgWaswMns 9:47; PLAYBOOK s6 (one comment prompt naming the next creature, <=15 s) | Comment prompt naming the next creature | Two-way choice (walrus or elephant seal) to drive debate; finished CASE FILE held 5 s |

Pacing against PLAYBOOK sections 3, 8 and 10:

| Check | Target | Ours |
|---|---|---|
| Hook | 70-90 words / ~30 s, creature named late, threat on screen in frame 1 | {S:hook_words} words / {S:hook_s} s; rule at {S:rule_s} s, turn at {S:turn_s} s, named at {S:name_s} s; silhouette in frame 1 |
| Promise + progress device | by 45-55 s | CASE FILE board at {T:s1}; promise at {T:s4}; slot 7 at {T:s6} |
| First rung | <= 45 s (corpus median 46 s, range 8-78 s) | {T:r1a} ({S:first_rung} s). Setup = {S:setup_pct}% of runtime (norm 8-10%); a {S:hook_words}-word immersion hook alone is {S:hook_s} s, so this is as tight as the hook mode allows |
| Words per minute (incl. pauses) | 160-170 | {S:eff_wpm} (speech {S:speech_wpm}) |
| Verbal re-hook interval | ~30 s | {S:rehooks} (median {S:rehook_median} s, max {S:rehook_max} s) |
| Comic deflation | every 60-90 s | {S:jokes}; max gap {S:joke_max} s, which is the sober 1985 / 2003 / hypothetical-opening stretch, kept joke-free on purpose |
| Long loops | 3-4 opened in minute 1, closed ~35/50/70/98% | B airborne penguin {T:h6} -> {T:r3g} ({P:r3g}); A trill {T:h7} -> {T:r5e} ({P:r5e}); D 1916 teaser {T:s3} -> {T:r6b} ({P:r6b}); title {T:s4} -> verdict {T:c16} ({P:c16}); qualifier {T:s5} -> {T:t2} ({P:t2}); E four-day story {T:s6} -> {T:p1}-{T:p14} ({P:p14}); rule {T:h4} -> {T:b2} ({P:b2}); C smile {T:h10} -> {T:r1f} and {T:b5} ({P:b5}) |
| Plants paid later (>= 4) | 4+ | anonymous gape {T:r1i} -> {T:p3}; boat tubes {T:r3c} -> {T:c6}; doorway / your exit {T:r3b} -> {T:ri2}, {T:c8}; big females {T:r1a} -> {T:p1}; whiskers {T:r5c} -> {T:c10}; catch-and-release {T:s2}/{T:r4b} -> {T:c13}, {T:p12}; Orde-Lees under-ice tracking {T:r6d} -> {T:c8}; Wood on the ice {T:r6g} -> {T:c8}; "most climb out fine" {T:s5} -> {T:t2}; crew eating seals {T:r6b} -> the gift reversal {T:p4} |
| Second person | >= 3% of words, >= 25% of sentences | {S:you_pct_words}% of words, {S:you_pct_sentences}% of sentences ({S:you_per_min}/min) |
| Numbers | 3-5/min, each with a comparison | {S:numbers_per_min}/min (approximate count; includes number words) |
| Re-immersion | ~47% | {T:ri1} ({P:ri1}) |
| Honest hedge | once | "nobody has pinned it down" {T:r4g}; also "probably" (whiskers), "often quoted" (speed), "Nobody's certain" (song) |

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
"""

AFTER_SCRIPT = """
## Notes on the rewrite

- The setup is now hook (cold / orcas / wrong pole / rule) -> 3 credentials -> promise. The old 0:37-0:50 misdirect list that repeated the cold is gone; the polar-bear gag lives in the hook.
- The 2003 case is never a teaser. Credential 3 is the 1916 Orde-Lees chase, the counterpart of SPERM's Essex. Brown's death is told only inside R6, after a 5 s silent pivot, followed by a 3 s black card, and the climax opens on "Now, a hypothetical" with a different scenario.
- Ladder order is body -> diet -> ice edge -> the game -> senses and song -> the record. The two penguin rungs sit together, joined by the JELLY turnstile, and the senses rung now feeds climax option 3.
- The anonymous gape plant ({T:r1i}) is paid by a 3-word reveal ({T:p3}), not a retell.
"""
