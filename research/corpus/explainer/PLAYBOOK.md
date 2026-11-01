# Explainer PLAYBOOK: ocean/animal "you vs X"

Built 2026-11-01 ~09:30 UTC from the 12 annotated scripts in this folder (`<id>.md`, transcripts in `raw/`), `SOURCES.md`, and the controls in `research/library/` and `research/R1/` (same-channel videos that did not pop). Machine-readable index: `INDEX.json`.

Rules for using this file:
- It describes structure and devices only. All wording below is ours. Nothing here may be copied from a reference transcript; your script still has to pass `python3 scripts/originality_check.py <script.md> research/corpus research/library/transcripts`.
- Put the 2-3 closest references and a beat alignment table in your script's front matter (BRIEF, Update 09:00).
- Check every fact. Several references overstate their science (fmZfphacPPQ's pressure mechanisms, mzeN0BXR4e0's contradictory "% explored" stats). We copy the format, never the errors.

Source ids used below:

| Short id | Full id | Fmt | Channel | Views | Outlier |
|---|---|---|---|---|---|
| SPERM | fGcgWaswMns | long 9:59 | Depth Theory | 2.31M | 14.65 |
| ERAS | nAWpLtG-kNs | long 16:10 | Fossil | 12.21M | 113.57 |
| ORCA | VtrcKTkhDHU | long 33:42 | OctoLab | 8.29M | 318.82 |
| DEEP | mzeN0BXR4e0 | long 17:57 | Mr. Science | 17.22M | 12.86 |
| SWALLOW | JkAcCdqYJN0 | long 9:11 | Occam | 0.33M | 15.82 |
| PLANT | QxM2Hu70tVk | long 8:49 | Dumb Doggo | 16.18M | 2.82 |
| PUFFER | XFFjxTllpoA | short 0:59 | Casual Geographic | 7.93M | 1.69 |
| JELLY | jw6bS-WL4F4 | short 0:58 | Casual Geographic | 6.72M | 1.43 |
| EEL | Ky0XPonYDcc | short 0:40 | Casual Geographic | 8.61M | 1.83 |
| ADRIFT | 4QGQhaRv4Dw | short 0:38 | Zack D. Films | 23.76M | 2.97 |
| PRESSURE | fmZfphacPPQ | short 0:33 | Zack D. Films | 14.71M | 1.84 |
| FLY | 6mRR91AbxjQ | short 0:28 | Zack D. Films | 13.69M | 1.71 |

Controls (same channel, did not pop): SQUID 2819-mQEA9M (Depth Theory, 0.79x), GW-ERAS mg2YJ04Hl9k (Depth Theory, 1.0x), HUMPBACK 4Mmo_dlsArE (Depth Theory, too new to score), ROCKS JavhxLs3Cs8 (Dumb Doggo, 1.04x), SKY uH-hucq-dmA (ExtinctZoo, 1.16x), MEG fC4LtXFAa1M (Mr. Science, 0.96x), GOBLIN U35yA-9nVEA (Casual Geographic, 0.78x), MANTIS XffxtLGdXUQ (Zack D. Films, 1.06x).

---

## 1. The canonical viral skeleton

Every reference runs on the same engine: **one big question opened in the first seconds, a ladder of rungs that each get worse (or closer to the answer), a turn after the peak, and an ending that closes the loop and invites a replay or a comment.** There are two shapes of long-form and one shape of Short.

### 1a. Long-form (8-10 min; we make 4)

Two variants share the open and the close. Pick one by premise:
- **Dossier** (one creature profiled, "why you'd never want to meet X"): climax at 60-75%, then a twist act. SPERM, ORCA.
- **Ladder/countdown** (N items ranked, "how long you'd last at every X", "every X that could Y"): climax inside the final item at 85-95%, with the twist built into that item. ERAS, SWALLOW, PLANT, DEEP.

Seconds are given for 8 min (480 s) / 10 min (600 s).

| # | Beat | % of runtime | Seconds (8 / 10 min) | What it must do | Exemplars |
|---|---|---|---|---|---|
| L1 | **Cold open hook** | 0-4% (median 3.4%) | 0-16 / 0-20 s (corpus range 5-49 s) | Open the master question. Either put "you" in a scene (immersion hook, 70-95 words) or restate the title as an action on you (short hook, 14-25 words). Name the creature late (at ~80% of the hook) or not at all. No channel intro, no "in this video". | SPERM 4.8%, ERAS 3.2%, ORCA 2.4%, DEEP 3.3%, SWALLOW 3.6%, PLANT 1.5% |
| L2 | **Reframe / stakes / rules** | 4-9% | 16-43 / 20-54 s | Dismiss the famous rival or common belief, then raise our subject above it with a 3-item credential stack whose last item is a teaser. For ladders: state the challenge rules (just you, no gear) and plant one rule you will break at the end. | SPERM reframe, DEEP stakes, ERAS rules, SWALLOW scoring rule, ORCA myth-bust |
| L3 | **Promise + format reveal** | ~9-10% | by 45 / 55 s (corpus median 46 s to first rung) | One line restating the title as what the video delivers. Show the progress device on screen: empty scoreboard, depth meter, countdown card, stopwatch. | SPERM 0:58, DEEP 0:36, ERAS 0:35 board, SWALLOW 0:20 stopwatch |
| L4 | **Rung 1, the format-teaching unit** | 10-25% (first unit is the longest) | 48-120 / 60-150 s | Run the full per-rung formula slowly so viewers learn it. Later rungs compress it. | PLANT 31.8%, DEEP 26.7%, ERAS front-loaded (first 8 eras avg 71 s, last 7 avg 52 s) |
| L5 | **Escalation rungs 2..N-1** | 25-60% | 120-290 / 150-360 s; 40-70 s per rung | Each rung strictly worse, or closer to passing the title test. Close the first long loop at ~35% by callback. Put the most shareable / gross-out fact at 40-45%. Re-immerse "you" at ~47% ("picture the opening again, knowing all this"). | SPERM rungs 1-6, ORCA power/mind/heart, DEEP zones 2-3, ERAS first sawtooth drop at 50% |
| L6 | **Climax: you vs it / the answer** | Dossier 60-75%; ladder 85-95% | Dossier 290-360 / 360-450 s | Dossier: an interactive "what would you do" with 3-4 options, each killed by a callback to an earlier rung, then a hard verdict. Ladder: the final item answers the title in the title's own words, with the comedy dropped and the tone sober. | SPERM verdict at 70%, ORCA answer 61-75%, SWALLOW answer at 92%, DEEP biggest landmark at 72% |
| L7 | **Twist / reversal** | 70-90% | 340-430 / 420-540 s | Flip the fear: it ignores you, or humans were the real danger, or the expected winner fails, or the opening rule is used against you. Frame each step as "here's the part nobody tells you". | SPERM twist + villain swap 70-88%, ORCA captivity 75-91%, ERAS no-tools twist 92-99%, SWALLOW legend debunk 77-85% |
| L8 | **Payoff + bookend** | 88-98% | 420-470 / 530-590 s | Return to the opening scene or rule with everything learned (3 callbacks), or recap every verdict in one breath, or count down the unsolved mysteries. End on an image, not a summary. | SPERM bookend, ORCA "next time you see the sea", DEEP mystery countdown, SWALLOW recap |
| L9 | **Close / CTA** | 98-100% | last 8-15 s | Either no spoken CTA (hold the finished board or the last image) or one comment prompt that names the next creature. Never a subscribe plea up front. | ERAS none, DEEP none, ORCA end screen only, SPERM comment CTA, PLANT/SWALLOW joke-threat CTA |

Macro proportions, median across the six: setup (L1-L3) 8-10%, ladder (L4-L6) 60-75%, turn (L7) 15-25%, close (L8-L9) 3-5%.

**Per-rung formula (long-form, every rung):**
1. Entry: a rhetorical question answered in 1-3 words, or a "here's what's worse" tease, or a numbered card. (SPERM, ERAS, DEEP)
2. One or two hard numbers, each followed within one sentence by an everyday or you-vs-it comparison (bus, elephants, your hand, your one-minute breath-hold). (SPERM, ERAS, ORCA, SWALLOW)
3. A short "you" scenario in present tense, 3-5 actions, each an animation beat. (PLANT, SWALLOW, ERAS)
4. One qualified authority line (a dated study, "researchers measured"); once per video, honestly admit something is unproven. (SPERM, ORCA, SWALLOW)
5. A 1-3 word punch line and a comic deflation. (SPERM, ERAS, SWALLOW, PLANT)
6. A seam: a bonus weird fact or a verdict stamp at the very end so there is no dead air before the next rung. (SWALLOW, ERAS)
7. One recurring graphic motif per rung (scale bar, counter, meter, sonar view, map, document stamp, strike-through list). (SPERM, ERAS)

### 1b. Shorts (we make 6, 60-90 s target; corpus outliers run 28-59 s)

No outlier in the corpus is longer than 59 s. To reach 60-90 s, **add rungs, not length per rung**, add the twist beat, or run two creatures back to back. Do not slow the voice down to fill time.

Seconds are given for a 55 s Short and a 30 s Short.

| # | Beat | % of runtime | Seconds (55 / 30 s) | What it must do | Exemplars |
|---|---|---|---|---|---|
| S1 | **Hook** | 0-6% | 0-3 / 0-2 s (median 9 words, 3 s) | The title as a second-person scenario or conditional, or the absurd outcome stated first, or the accident already happening. The subject is on screen in frame 1 even if it is named later. | all six |
| S2 | **Stakes / anchor** | 6-20% | 3-11 / 2-6 s | Two numbers (a body count and a multiple of something feared), or a counted inventory ("N tools"), or a misdirect list of famous threats then a pivot. | PUFFER, FLY, JELLY, EEL, ADRIFT |
| S3 | **Ladder rungs 1-3** | 20-48% | 11-26 / 6-14 s; a new rung every 3-6 s | Each rung one notch worse; one 3-4 s mechanism aside with the real term plus a plain verb, paid off in the next line. Join rungs with "and / then / so / until" so there is no full stop to swipe on. | PUFFER, PRESSURE, FLY, JELLY |
| S4 | **Turnstile re-hook** | 45-55% | at ~25 / ~14 s, 1-2 s long | A 4-7 word false reassurance or "not the worst part" line, or a time-jump opener, with a background change on the next word. | PUFFER 46%, JELLY 53%, ADRIFT 48%, EEL 48% |
| S5 | **Peak + main loop closes** | 55-75% | 26-41 / 14-22 s | The worst outcome, said through jokes or euphemism, or the big reveal of the absurd answer. | PUFFER 70%, JELLY 53-70%, EEL 70%, ADRIFT 64-72%, FLY 57-65% |
| S6 | **Twist / second axis** | 75-90% | 41-50 / 22-27 s | Change axis after the peak: hypothetical becomes real, pain becomes disgust, outside becomes inside, or step out of the story and rank it. | PUFFER reality flip, FLY disgust axis, PRESSURE inside-to-whole-body, EEL step-out |
| S7 | **Stinger** | 90-100% | 50-55 / 27-30 s, 4-15 words | End on the strongest word (a finality word, a recurrence fact, a purpose reveal, a callback insult). Cut within 1 s. The last frame matches or contrasts the first so the loop is seamless. No CTA. | all six |

Macro proportions, median across the six: hook + stakes 20%, ladder 50-70%, peak/twist 15-25%, stinger 7-10%.

**Shorts in a 30-35 s mechanism format** (FLY, PRESSURE): drop S6, merge S5 and S7, and put the payoff in the final clause.

---

## 2. Hook formulas (abstracted; write fresh words)

| # | Formula (pattern only) | Shape | Used by (views, outlier) | Notes |
|---|---|---|---|---|
| H1 | **Calm scene, broken rule** | 2P "picture this" in a safe place -> tick off 2-3 usual dangers -> state the safe rule -> 3-4 word turn -> an unexplained body sensation -> creature named last, already ahead of you | SPERM (2.31M, 14.65) | The SQUID control (0.79x) used the same template but opened on a general claim instead of a sensation and a rule. The felt clue is closed by callback at ~35%. |
| H2 | **Title as an action on you** | Restate the title in present tense with "you" as the object, plus a scope word (every/all) and a qualifier that hints most will fail | SWALLOW (0.33M, 15.82), FLY (13.69M, 1.71) | Shortest hook in the corpus (5-14 words). Works best when the title already promises a body consequence. |
| H3 | **"Here's what happens if you [risky act]"** | Title restated as a promise -> 2 numbers by second 7 | PUFFER (7.93M, 1.69) | The creature is on screen at once but called only "this tiny [thing]" until late. |
| H4 | **Conditional with a minimised first number** | "If you [action] to just [small value]..." -> the first mild symptom | PRESSURE (14.71M, 1.84) | "Just" tells the viewer trouble starts early and promises much bigger numbers. Pair with a depth meter. |
| H5 | **Stranded in a random [set item]** | 2P "imagine" you are stuck in one item of a set -> ranking question -> 3-4 quick teaser items, the most famous held for last -> "is any survivable?" -> rules -> "let's see" | ERAS (12.21M, 113.57) | The teasers are a contract, paid off in fame order at ~35/60/75/90%. The GW-ERAS control (1.0x) used the same tournament with a shark, not you. |
| H6 | **Unnamed predator paradox** | "A creature that can [feat 1], [feat 2], [feat 3, bending toward humans]... yet has never [done the obvious thing to us]" -> why-question on a black frame -> "after this you'll see [X] differently" | ORCA (8.29M, 318.82) | The subject is never named in the hook or the title. Slip in one quiet qualifier ("in the wild") that the reversal act later exploits. |
| H7 | **Forbidden world, impossible life** | Evidence frame of the thumbnail creature, then 2 lines: a place we were not meant to see, and things there that should not exist -> N-step promise naming every stage | DEEP (17.22M, 12.86) | Visual hook first, verbal hook about 10 s, promise in by 36 s. |
| H8 | **Superlative plus odd-category consequence** | "The [most dangerous] [thing] in [place] can make you [an unexpected kind of effect]" -> misdirect list of famous threats -> pivot | JELLY (6.72M, 1.43) | Pick a consequence nobody links to the subject (time, memory, perception, paralysis while awake). Avoid self-harm wording (R5 ad risk). |
| H9 | **Absurd true outcome first** | On-screen text states the strange true result; the voice only promises to explain how it happened | EEL (8.61M, 1.83) | Only for real, checkable stories. Tell it backwards: the result, then the chain. |
| H10 | **Accident already happening** | The disaster in the first clause + one mystery adverb (nobody knows how) + one isolation clause (nobody saw) | ADRIFT (23.76M, 2.97) | Third person and past tense, but the camera puts you in his place. The mystery is never closed and drives rewatches. The MANTIS control (1.06x) also opens mid-action but on animal vs animal, with no human at stake. |
| H11 | **Shrink the viewer, joke, count down** | You are made small (or made the prey) -> title as a question -> one-line comic deflation -> "number N" card | PLANT (16.18M, 2.82) | Show every threat in the video in one tableau during the hook (the menu up front). |

Hook rules across all 11:
- **Median hook length:** long-form 48 words / 20 s (two modes: short hooks of 14-25 words in 5-10 s, immersion hooks of 70-95 words in 29-41 s); Shorts 9 words / 3 s (range 5-15 words, 1.5-6 s).
- **"You" within the first 10 words** in 8 of 12 references (by word 7 in 7 of them). The four that skip "you" (ORCA, DEEP, ADRIFT, EEL) replace it with a paradox, a forbidden place, a person in danger, or an absurd outcome.
- **Name the creature late, show it early.** SPERM names it at 0:23, ORCA at 1:23, JELLY at 0:10, PUFFER at 0:44, while each shows it (or its effect) on screen almost at once.
- **The hook carries a contract.** Every teaser or credential named in the hook is paid off later, in order, the first one by ~20-35% of runtime (ERAS, ORCA, SPERM).

---

## 3. Re-hook cadence

| Metric | Long-form median (range) | Shorts median (range) | Sources |
|---|---|---|---|
| Any attention reset (pivot, question, gag, cut, callback) | ~20 s (14-30) | ~4.5 s (3-6.5) | PLANT 14 s, DEEP 25 s, SPERM 30 s / PUFFER 3.5, JELLY 5, EEL 6.5, ADRIFT 4.5, PRESSURE 4.5, FLY 3 |
| Explicit verbal re-hook line | ~28 s (14-65) | ~10 s (6.5-23) | SPERM 30, DEEP 25, SWALLOW 42, ORCA 65 / PUFFER 15, JELLY 23, ADRIFT 10.5, PRESSURE 9 |
| Structural unit (new rung, item, chapter card) | ~70 s (50-300) | n/a (rungs every 3-8 s) | SPERM ~50, ERAS 62, SWALLOW 62, PLANT 65-100, DEEP 200, ORCA 300 |
| Punch line / joke | every 60-90 s (comedy hosts every 8-12 s) | none before midpoint, then every 4-6 s (comedy Shorts) | SPERM, SWALLOW, PUFFER |
| Visual state change | every 2-4 s | every 1-3 s; caption card every 0.5-3 s | SPERM, PRESSURE, FLY, ADRIFT |

Re-hook devices, ranked by how often they appear:
1. **Rhetorical question answered in 1-3 words** (SPERM, ERAS, PLANT, ORCA). Opens a 2-6 s micro loop.
2. **"Worse" turnstile:** a tease that the next part is worse or stranger (PUFFER, JELLY, SPERM, ORCA, DEEP).
3. **Numbered card / new item** (ERAS, SWALLOW, PLANT, DEEP chapters, ORCA chapters).
4. **Conjunction chain:** clauses joined by and/so/until/which so no sentence ends (PRESSURE, FLY, EEL, MANTIS). This is the Shorts' main tool.
5. **Time-jump opener** at ~15%, ~48% and ~72% (ADRIFT).
6. **Callback** to a hook detail ("remember the [sensation]?") (SPERM, ORCA, SWALLOW).
7. **"Picture it again"** re-immersion at about the midpoint (SPERM).
8. **Withheld noun** ("something touched him"; "a machine that..." then the next chapter names it) (ADRIFT, ORCA).
9. **The host breaks their own routine** (refuses to score, puts the stopwatch away) (SWALLOW).
10. **Re-hooks get denser near the end**, where drop-off is highest (ERAS, ORCA acts V-VI).

---

## 4. Escalation ladders

Every ladder climbs on **two axes at once** (the number grows and the threat changes kind). Pick two:

| Ladder | Rungs (abstract) | Sources |
|---|---|---|
| **Depth / magnitude x10** | small value -> x10 -> x10 -> x3 final; each value shown with a landmark of that size | PRESSURE, DEEP |
| **Clock** | minutes -> tens of minutes -> hours (or seconds -> hours -> about a day) | PUFFER, ADRIFT, JELLY ("all within minutes") |
| **Body system, outside to inside** | skin/ears -> organs -> blood chemistry -> whole body | PRESSURE, PUFFER, FLY |
| **Capability dossier** | size -> weapon -> what it beats -> where it goes that you can't -> how it senses you -> how smart it is -> proof it has harmed people | SPERM, ORCA |
| **Closeness to passing the test** | can't -> briefly -> real but partial -> possible but never recorded -> passes | SWALLOW |
| **Fame** | least famous first, most famous held to last and announced as the one you've waited for | PLANT, ERAS |
| **Sawtooth verdicts** | rising overall, a first drop at ~50%, a crash at ~55-60%, peak declared at ~90%, expected winner below peak at the end | ERAS |
| **Hostility + strangeness** | each zone has less light, more pressure, less food, and stranger adaptations; scope grows from one animal to whole ecosystems to other worlds | DEEP |
| **Hypothetical to real** | "you would..." -> it actually happened (dated) -> it still happens every year | PUFFER, SWALLOW, SPERM |
| **Tone** | slapstick -> gross-out -> narrator fear -> darkness -> sober | SWALLOW, PLANT |
| **Personal to final** | potency -> body -> visible marks -> mind -> speed -> death mechanism -> lasting cost | JELLY |
| **Isolation** | crowd -> alone -> a dot seen from above | ADRIFT |

Ladder rules:
- **The facts become the weapon.** In the climax, kill each escape option with a callback to an earlier rung (SPERM). Viewers feel smart and doomed at once.
- **The peak is not the end.** After the main loop closes, change axis so the back third doesn't sag (JELLY puts its emotional peak before the literal death; PUFFER flips to "this really happens").
- **One planted word, paid twice.** Introduce a failure word early as something avoided, then pay it off partly and then totally (PRESSURE). Long-form: plant at least four throwaway details in the first third and pay each off later (ORCA has 12 plant-payoff pairs).

---

## 5. Twist and payoff patterns

| Pattern | Shape | Sources |
|---|---|---|
| **Villain swap** | After the threat peaks: the real danger has always run the other way (human harm, with before/after numbers) | SPERM, ORCA, SQUID control |
| **Reassurance flip** | Right after the darkest verdict: it barely notices you (diet share near zero; you are the fly in this relationship) | SPERM |
| **Reality flip** | The hypothetical happens on purpose (people eat it, swim there, keep it) and one small error kills | PUFFER |
| **Opening rule turned against you** | The rule stated in the hook (no tools, stay shallow) is what the final threat exploits | ERAS, ORCA ("in the wild" qualifier) |
| **Could vs has** | A legend fake-out on the second-to-last item, debunked fast; only the last passes for real | SWALLOW |
| **Myth-bust on the famous one** | The best-known item or name is wrong in the popular telling; show the real numbers | PLANT (#1), ORCA (its name), ERAS (Ice Age) |
| **Purpose reveal in the last clause** | Everything shown was for one reason, revealed last (it is feeding on you) | FLY |
| **Relief with a sting** | You survive, but at a lasting cost | JELLY |
| **Deliberately unresolved** | The biggest questions are left open as the payoff (we still don't know), or one mystery adverb is never explained | DEEP, ADRIFT |
| **Question upgrade** | "The real mystery isn't why X, it's how Y" | ORCA |

---

## 6. Endings and CTAs

- **Shorts: 6 of 6 have no CTA.** They end on the strongest word and cut within ~1 s; the last frame mirrors (FLY, ADRIFT, EEL) or contrasts (PRESSURE) the first so the loop restarts cleanly. Stinger types: finality word (PRESSURE), recurrence fact (PUFFER), purpose reveal (FLY), callback insult (JELLY), step-out ranking (EEL), flat outcome (ADRIFT).
- **Long-form: the three biggest outliers have no spoken CTA** (ERAS 113x, ORCA 319x, DEEP 12.9x). They end on a finished scoreboard, a moral line or a 3-part emotional button.
- When a CTA is used it is **≤15 s, at 98-100%, and asks for a comment that names the next creature** (SPERM, and the same line in both Depth Theory controls, so the CTA is not what drove the outlier) or is a **joke threat** that mirrors an earlier gag (PLANT, SWALLOW).
- **Bookend.** 4 of 6 long-forms return to the opening image, rule or promise in the last 5% (SPERM, ORCA, DEEP, SWALLOW).
- **Finished board as comment bait.** A ranking held on screen for 5+ s at the end makes viewers argue placements (ERAS).

---

## 7. Series and part-2 mechanics

The explainer niche runs on **series formulas, not cliffhangers.** None of the 12 references ends on a "part 2" cliffhanger (that is a horror-niche device; see `research/corpus/horror/`).
- **Fixed title formula per series:** "Why you'd never want to meet [X]" (Depth Theory, 3 videos, one fixed script template); "What it's like to [be killed by] [X]" (Dumb Doggo, 3 outliers at 1.8-2.8x); "Nothing about [X] is normal" (Mr. Science, 2 at 2.6x); "[Deadliest X] from every single period" (ExtinctZoo, 2 at 3.7-4.7x); "How [creature] [hurts] you" (Zack D. Films). Formulas transfer across channels: the "deeper you go, the creepier" and "how long you'd last in every X" titles were cloned by Spinosnack (33x) and BeyondTheBlue (11.4x) (SOURCES runners-up).
- **Split a long list into parts** only when the list is large (Dumb Doggo spiders "Part 1", 1.85x).
- **Cross-video callbacks:** a joke that references the channel's previous creature (Depth Theory sperm whale and squid both cite a "stealing dinner" link) rewards binge viewers.
- **Next-creature prompt** in the CTA feeds the topic queue and makes each video an episode.
- **For our Shorts:** use one title formula per series (for example "How [ocean animal] [hurts] you" and "Could you survive [ocean extreme]?") and keep the beat sheet identical between episodes, as Depth Theory does in long-form.

---

## 8. Pacing stats

Computed from the transcripts by `stats.py` (word counts, "you" words, digit and number-word tokens); hook lengths, re-hooks and loops are taken from each annotation file. Shorts sentence lengths use the annotators' counts because auto-subs drop punctuation.

| Metric | Long-form median (range), n=6 | Shorts median (range), n=6 | Our target |
|---|---|---|---|
| Words per minute | 152 (117-168) | **two clusters:** narrated animation 172 (150-177: ADRIFT, PRESSURE, FLY); talking-head TikTok 288 (275-293: PUFFER, JELLY, EEL) | Long 160-170 (Depth Theory 168); Shorts 180-230 for TTS (Kokoro/Piper sounds rushed above ~250) |
| Hook length | 48 words / 20 s (14-94 words, 5-41 s) | 9 words / 3 s (5-15 words, 1.5-6 s) | Long: ≤25 words/10 s, or 70-90 words/30 s for an immersion hook. Shorts: ≤12 words, ≤3 s |
| Time to first rung / format reveal | 46 s (8-78 s) | 6-11 s | Long ≤45 s; Shorts ≤8 s |
| Average sentence length (words) | 12.4 (9.1-21.2) | 15 (13-26; PRESSURE is one 93-word chained sentence) | Long 10-13 with 1-3 word punches; Shorts 12-16 words, or chained clauses |
| Second person: % of all words that are you/your | 2.7% (0-5.4%) | 5.8% (0-8.6%) | Long ≥3%; Shorts ≥5% |
| Second person: % of sentences containing "you" | 22% (0-41%) | 66% (0-100%) | Long ≥25%; Shorts ≥60% |
| "You" words per minute | 4.2 (0-8.5) | 13.6 (0-23) | Long 4-8; Shorts 12-20 |
| Numbers per minute (digits + number words) | 3.0 (1.5-6.4) | 6.3 (1.5-7.7) | Long 3-5, each with a comparison; Shorts 5-8 |
| Open loops per minute (annotated loop tables) | 0.87 (0.45-1.36) | 6.3 (4.5-9.1) | Long: 3-4 long loops opened in the first minute + ~1 new loop/min; Shorts: 1 spine loop + a micro loop every 8-12 s |
| Max short loops open at once | ~2 | 1 spine + 1 micro | same |
| Long-loop close points | ~35%, 50%, 70%, 98% (SPERM); teasers paid at 35/60/75/90% (ERAS) | spine closes at 64-100% (median ~70%) | same |

Per-video computed values (for reference):

| id | wpm | avg sentence | you % words | you % sentences | you/min | numbers/min | loops/min |
|---|---|---|---|---|---|---|---|
| SPERM fGcgWaswMns | 168 | 12.7 | 2.4 | 21 | 4.0 | 3.3 | 0.90 |
| ERAS nAWpLtG-kNs | 166 | 9.1 | 3.5 | 29 | 5.8 | 3.5 | 0.62 |
| ORCA VtrcKTkhDHU | 117 | 21.2 | 0.3 | 4 | 0.3 | 1.9 | 0.45 |
| DEEP mzeN0BXR4e0 | 122 | 12.1 | 0.0 | 0 | 0.0 | 1.5 | 0.84 |
| SWALLOW JkAcCdqYJN0 | 146 | 9.3 | 3.0 | 24 | 4.4 | 6.4 | 0.98 |
| PLANT QxM2Hu70tVk | 159 | 12.6 | 5.4 | 41 | 8.5 | 2.7 | 1.36 |
| PUFFER XFFjxTllpoA | 288 | 14 | 7.8 | 65 | 23.0 | 7.3 | 6.1 |
| JELLY jw6bS-WL4F4 | 275 | 13.9 | 5.3 | 67 | 14.5 | 5.2 | 5.2 |
| EEL Ky0XPonYDcc | 288 | 16 | 0.0 | 0 | 0.0 | 1.5 | 4.5 |
| ADRIFT 4QGQhaRv4Dw | 150 | 13 | 0.0 | 0 | 0.0 | 1.6 | 6.4 |
| PRESSURE fmZfphacPPQ | 172 | 93 (1 sentence) | 8.6 | 100 | 14.8 | 7.4 | 9.1 |
| FLY 6mRR91AbxjQ | 177 | 26 | 6.2 | 67 | 12.8 | 7.7 | 8.7 |
| *control* SQUID 2819-mQEA9M | 172 | 12.4 | 1.8 | 16 | 3.0 | 5.8 | - |
| *control* HUMPBACK 4Mmo_dlsArE | 172 | 12.3 | 2.1 | 17 | 3.6 | 6.4 | - |
| *control* GW-ERAS mg2YJ04Hl9k | 153 | 10.7 | 0.3 | 3 | 0.4 | 4.7 | - |
| *control* ROCKS JavhxLs3Cs8 | 162 | 13.9 | 1.8 | 21 | 3.0 | 1.0 | - |
| *control* SKY uH-hucq-dmA | 195 | 22.9 | 0.5 | 8 | 1.0 | 3.9 | - |
| *control* GOBLIN U35yA-9nVEA | 272 | n/a | 1.9 | n/a | 5.3 | 4.2 | - |
| *control* MANTIS XffxtLGdXUQ | 172 | 14.6 | 0.0 | 0 | 0.0 | 2.4 | - |

Notes: the number count is approximate (it includes "one" used as a pronoun). Loop counts depend on how finely each annotator split loops; Shorts also have many uncounted cause-effect micro loops.

---

## 9. Outliers vs ordinary: what the top scripts do that weaker ones don't

Each comparison holds the channel, art style and narrator constant, so the difference is mostly the script.

1. **The viewer (or a human) is the one at risk.** In every channel pair the outlier uses more second person:
   - Depth Theory: SPERM 2.4% "you" words / 21% of sentences vs SQUID 1.8% / 16% and HUMPBACK 2.1% / 17%. The R1 shot count agrees: SPERM spends 12% of its 5 s windows on the diver/YOU, SQUID 3%.
   - Dumb Doggo: PLANT 5.4% / 41% vs ROCKS 1.8% / 21%.
   - Casual Geographic: PUFFER 7.8% and JELLY 5.3% vs GOBLIN 1.9%.
   - Zack D. Films: FLY 6.2%, PRESSURE 8.6% and ADRIFT (a human victim) vs MANTIS 0% (lizard vs mantis, no human).
   - Depth Theory GW-ERAS (1.0x) uses the ERAS tournament but drops a shark into the eras, not you (0.3% "you"); ERAS (113x) drops you.
   The exceptions (ORCA, DEEP) replace "you" with an even stronger master question: a paradox, or a descent into the unknown. **If there is no "you", there must be a paradox.**
2. **Immersion beats assertion in the first 20 s.** SPERM opens on a felt sensation in a scene and a rule about to break; SQUID (same template, same voice) opens on a general claim about what has been filmed. MEG (0.96x) spends ~50 s on a slow named-person story before the subject. GOBLIN (0.78x) spends its first 7 s (12% of runtime) on silent footage. Every outlier Short is talking about the threat within 1 s.
3. **Fewer raw numbers, more comparisons.** The Depth Theory controls are more number-dense (SQUID 5.8/min, HUMPBACK 6.4/min) than SPERM (3.3/min). SPERM turns almost every number into a bus, an elephant, your hand or your breath. Density of facts is not the driver; how felt each fact is, is.
4. **More jokes and less stock.** SPERM has a comic deflation every 60-75 s and only ~3% stock footage; SQUID has ~10 jokes over 10 min and 12% stock. Comedy keeps the death ladder light enough for a broad audience (PLANT, SWALLOW, PUFFER).
5. **A visible progress device.** Outliers show the shape of the video: tier board (ERAS), stopwatch (SWALLOW), countdown cards (PLANT), zone diagram (DEEP), numbered options with strike-throughs (SPERM). ROCKS has a collection shelf too, so the device helps but is not enough without a threat to the viewer.
6. **A bigger category and a famous subject.** ExtinctZoo's sea/apex videos (3.7-4.7x) beat its sky video (1.16x) with the same format. SPERM (a famous whale with a famous sinking story) beat SQUID (a little-known animal) with the same template. Choose the subject people already half-know and fear.
7. **The hook makes promises and the body keeps them in order.** ERAS pays its four teasers at 37/63/77/92%; ORCA pays hook items 1 and 2 by 25%; SPERM closes its sensation loop at 37%. SKY (1.16x) takes 62 s to state its question.
8. **Shorts start speaking about the danger immediately, never stop for breath, and never end on a CTA.** All six outlier Shorts: hook ≤6 s, joined clauses, stinger on the last word, loop. The two Shorts controls are either slow to start (GOBLIN) or have no human stake (MANTIS).

---

## 10. Writer checklist (every box must be ticked before the originality gate)

**Front matter**
- [ ] `references:` lists 2-3 corpus ids closest to the premise, with url, views and outlier_score (from `INDEX.json`).
- [ ] A beat alignment table maps each of our beats to a reference beat, its timestamp, and the device borrowed.
- [ ] A fact list with a source for every number and mechanism.

**Premise and title**
- [ ] The premise puts "you" (or a human) at risk, **or** states a paradox / descent into the unknown. Not a neutral fact tour.
- [ ] The subject is famous or half-known and feared; the category is broad (ocean, deadliest, every depth).
- [ ] The title uses one series formula (H2-H11 shapes) and the hook restates or enacts it.

**Hook**
- [ ] Shorts: ≤12 words and ≤3 s, "you" (or the victim) within the first 10 words, subject on screen in frame 1.
- [ ] Long-form: ≤25 words/10 s, or a 70-90 word immersion hook ending on the creature's name; promise + progress device on screen by 45 s.
- [ ] The hook opens one master question and lists its teasers; each teaser is paid later, in order, the first by ~35%.

**Body**
- [ ] Each rung is strictly worse (or closer to the answer) than the last; the ladder climbs on two axes.
- [ ] Every number is followed within one sentence by an everyday or you-vs-it comparison, with an on-screen scale prop.
- [ ] Re-hook cadence met: Shorts a reset every 3-6 s and a turnstile line at 45-55%; long-form a reset every ~20 s, a verbal re-hook every ~30 s, a new rung every 40-70 s.
- [ ] Long-form: 3-4 long loops opened in the first minute and closed at about 35/50/70/98%; at least 4 planted details paid off later; a "picture it again" re-immersion near 47%; a comic deflation every 60-90 s.
- [ ] Climax uses earlier facts against the viewer (options killed by callbacks, or the last item passing the learned test).
- [ ] A twist after the peak changes axis (villain swap, reality flip, opening rule turned against you, myth-bust).

**Pacing**
- [ ] Words/min: long 160-170; Shorts 180-230 (TTS).
- [ ] "You" in ≥25% of sentences (long) or ≥60% (Shorts), unless the premise is a paradox or third-person survival story.
- [ ] Average sentence 10-13 words (long) with 1-3 word punch lines; Shorts chained clauses with no full stop before the payoff.
- [ ] Numbers: long 3-5/min; Shorts 5-8/min.

**Ending**
- [ ] Shorts: stinger on the strongest word, cut within 1 s, last frame matches or contrasts the first, no CTA.
- [ ] Long-form: a bookend to the opening (or a finished board, or a mystery countdown), then either no CTA or one ≤15 s comment prompt naming the next creature.

**Safety and originality**
- [ ] No self-harm or suicide wording; death and gore handled by euphemism, jokes or cartoon dissolve (R5).
- [ ] No sentence copied from any reference; `originality_check.py` prints PASS.

---

## 11. Study these three first

1. **fGcgWaswMns: Depth Theory sperm whale** (2.31M, 14.65x). The style and voice we are copying, and the full dossier template: immersion hook, reframe, 7-rung capability ladder, options climax, twist, villain swap, bookend. Read with its control SQUID (2819-mQEA9M, `research/R1/beatmaps/`) to see which changes made it pop.
2. **nAWpLtG-kNs: Fossil, how long you'd last in every era** (12.21M, 113.57x). The ladder/countdown template with a fixed per-item checklist, a sawtooth verdict curve, a visible tier board, and a final twist that uses the opening rule. It maps directly onto "how long you'd last at every ocean depth / next to every sea creature".
3. **XFFjxTllpoA: Casual Geographic pufferfish** (7.93M, 1.69x). The best 60 s Short skeleton for our Shorts slot: title-as-promise hook, two stakes numbers, a timed body ladder, a turnstile at 46%, death told through jokes, a reality flip and a recurrence stinger. Slow it to 200-230 wpm for TTS and add 2-3 rungs to reach 70-80 s.

Next in line: **fmZfphacPPQ** (the 30 s depth ladder with a depth meter; best for code-only visuals), **VtrcKTkhDHU** (the paradox hook for a long-form open), **jw6bS-WL4F4** (the ocean Short with misdirect, pivot and turnstile).
