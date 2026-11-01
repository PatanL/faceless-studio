# Explainer PLAYBOOK: ocean/animal "you vs X"

Built 2026-11-01 ~09:30 UTC from the first 12 annotated scripts; **revised ~12:50 UTC with the 12-video expansion** (11 outliers + 1 control, `SOURCES.md` "Expansion"), so it now rests on 23 outliers (12 long, 11 Shorts) and 9 controls. Files: annotated scripts `<id>.md`, transcripts `raw/`, computed stats `stats.json` (from `stats.py`), controls in `research/library/`, `research/R1/` and here (PoF_doh3NOE). Machine-readable index: `INDEX.json`. What the expansion changed is summarised in section 12.

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
| *expansion* | | | | | |
| WHATIF | 2d6Ciu3INeA | short 2:52 | What If | 3.32M | 69.27 |
| SHOT | V15wrmD5VFs | short 0:29 | The Infographics Show | 2.98M | 11.34 |
| BITE | ZZf1KBnH5iI | short 1:30 | Spinosnack | 0.39M | 4.90 |
| SHELLS | LpUzg3Dc-m0 | short 0:52 | BRIGHT SIDE | 0.10M | 3.68 |
| KITCHEN | 2cK8l5Yg5w8 | short 1:07 | Kurzgesagt | 5.19M | 3.58 |
| ORCA-ERAS | UNPK8PNCCmQ | long 19:07 | Fossil | 3.86M | 35.87 |
| PETS | thtoMGvpWIU | long 9:45 | Occam | 0.52M | 24.70 |
| SHEEP | UfbYyHuVx5M | long 8:15 | WILD VERSUS | 7.62M | 18.83 |
| TREX | lVV5ztC3CtI | long 20:11 | Spinosnack | 1.50M | 7.88 |
| GATOR | SDs41Ke3v4Q | long 17:42 | BlackWater | 6.06M | 6.57 |
| OCEANS | qrfhhZ-Wvmk | long 17:37 | BeyondTheBlue | 3.37M | 6.54 |

Controls (same channel, did not pop): SQUID 2819-mQEA9M (Depth Theory, 0.79x), GW-ERAS mg2YJ04Hl9k (Depth Theory, 1.0x), HUMPBACK 4Mmo_dlsArE (Depth Theory, too new to score), ROCKS JavhxLs3Cs8 (Dumb Doggo, 1.04x), SKY uH-hucq-dmA (ExtinctZoo, 1.16x), MEG fC4LtXFAa1M (Mr. Science, 0.96x), GOBLIN U35yA-9nVEA (Casual Geographic, 0.78x), MANTIS XffxtLGdXUQ (Zack D. Films, 1.06x), and from the expansion MEGABAT PoF_doh3NOE (Casual Geographic, 1.38x, fully annotated here). Same-channel outlier pairs added by the expansion: ORCA-ERAS vs ERAS (Fossil), PETS vs SWALLOW (Occam).

Caveats for the expansion: SHEEP is a footage-led clip compilation (only its narration structure transfers); SHOT, BITE, SHELLS, KITCHEN, ORCA-ERAS and TREX were transcribed with whisper (some name errors, listed in each file); WHATIF and KITCHEN have no contact sheet, so their visual notes are inferred.

---

## 1. The canonical viral skeleton

Every reference runs on the same engine: **one big question opened in the first seconds, a ladder of rungs that each get worse (or closer to the answer), a turn after the peak, and an ending that closes the loop and invites a replay or a comment.** There are two shapes of long-form and one shape of Short.

### 1a. Long-form (8-10 min; we make 4)

Two main variants share the open and the close. Pick one by premise:
- **Dossier** (one creature profiled, "why you'd never want to meet X"): climax at 60-75%, then a twist act. SPERM, ORCA. The **patch-notes** form (TREX) is a dossier of a famous animal where every section is "old view, then a named dated study, then a number and a comparison"; the hook's three headline claims are paid at the start, middle and end (4%, 49%, 85-95%).
- **Ladder/countdown** (N items ranked, "how long you'd last at every X", "every X that could Y"): climax inside the final item at 85-95%, with the twist built into that item. ERAS, SWALLOW, PLANT, DEEP, OCEANS, PETS, ORCA-ERAS (8 of 12 long outliers now use a ladder). Three sub-forms from the expansion:
  - **Checkpoint countdown** (PETS): the same 3-4 time stamps for every entry (hour, day, week), one stamp held back so only the winner reaches it (closed at 93%).
  - **Third-person champion tournament** (ORCA-ERAS): a famous animal, not you, takes the test in every era; scoring words are defined before any verdict, and the verdict curve reaches the top early (37%) and gets its tension from downgrades when real rivals appear (63-95%).
  - **Plan-killer ladder** (OCEANS): each rung gives you a fair escape option (scuba, shore, cage, raft) and kills it with a mechanism, about every 3 min.
- **True-story mystery box** (GATOR, new): one real, dated experiment with N identical setups and N different fates; a spoken 3-question roadmap carries a long set-up (25% of runtime), the payoffs land at about 32%, 53% and 72% as counted cliffhangers, and the last one stays unsolved.

Seconds are given for 8 min (480 s) / 10 min (600 s).

| # | Beat | % of runtime | Seconds (8 / 10 min) | What it must do | Exemplars |
|---|---|---|---|---|---|
| L1 | **Cold open hook** | 0-4% (median 3.4%) | 0-16 / 0-20 s (corpus range 5-44 s) | Open the master question. Either put "you" in a scene (immersion hook, 57-134 words) or restate the title as an action on you (short hook, 14-32 words). Name an unknown creature late (at ~80% of the hook); name a famous one in line 1 and sell the change to it instead (TREX, ORCA-ERAS). No channel intro, no "in this video". | SPERM 4.8%, ERAS 3.2%, ORCA 2.4%, DEEP 3.3%, SWALLOW 3.6%, PLANT 1.5%, ORCA-ERAS 1.6%, PETS 3.2% (with teasers), OCEANS 3.4%, TREX 3.6%, GATOR 2.1% |
| L2 | **Reframe / stakes / rules** | 4-9% | 16-43 / 20-54 s | Dismiss the famous rival or common belief, then raise our subject above it with a 3-item credential stack whose last item is a teaser. For ladders: state the challenge rules (just you, no gear), define the scoring words, and plant one rule you will break or ask the viewer to remember. A three-teaser stack drawn from the bottom, middle and top of the list is the strongest open in the corpus (PETS). | SPERM reframe, DEEP stakes, ERAS rules, SWALLOW scoring rule, ORCA myth-bust, ORCA-ERAS scoring terms, PETS teasers + rule, GATOR science stakes |
| L3 | **Promise + format reveal** | ~4-10% | by 45 / 55 s (corpus median ~48 s to first rung, range 8-78 s) | One line restating the title as what the video delivers. Show the progress device on screen: empty scoreboard, depth meter, countdown card, stopwatch, checkpoint columns. A spoken roadmap ("three questions first") works when the set-up is long (GATOR). | SPERM 0:58, DEEP 0:36, ERAS 0:35 board, SWALLOW 0:20 stopwatch, OCEANS 0:36, ORCA-ERAS 0:40 board, PETS 0:54, GATOR 0:59 roadmap |
| L4 | **Rung 1, the format-teaching unit** | 10-25% (first unit is the longest) | 48-120 / 60-150 s | Run the full per-rung formula slowly so viewers learn it. Later rungs compress it. | PLANT 31.8%, DEEP 26.7%, ERAS front-loaded (first 8 eras avg 71 s, last 7 avg 52 s) |
| L5 | **Escalation rungs 2..N-1** | 25-60% | 120-290 / 150-360 s; 40-70 s per rung (10-20 min videos: 75-100 s) | Each rung strictly worse, or closer to passing the title test. Close the first long loop at ~35% by callback. Put the most shareable / gross-out fact at 40-45%. Re-immerse "you" at ~47% ("picture the opening again, knowing all this"). In 15-20 min videos the middle rungs are the longest (where the real rivals and arguments are), not the first. | SPERM rungs 1-6, ORCA power/mind/heart, DEEP zones 2-3, ERAS first sawtooth drop at 50%, ORCA-ERAS reptile eras 47-80%, GATOR carcass 1 at 32% |
| L5b | **The 60-65% flip** (new) | 58-66% | ~290-315 / 360-390 s | Change the question the video is asking: the list flips (victim becomes threat), the obvious favourite is knocked out, the first rival that can beat the champion arrives, or the one downgrade is owned and turned into a new strength. One short line, then a visible change (board, colour, water line). | PETS flip at 61%, ORCA-ERAS first real rival at 63%, OCEANS planned peak at 63-68%, TREX nerf at 60-66%, BITE (Short) water rule at 61%, ORCA answer from 61% |
| L6 | **Climax: you vs it / the answer** | Dossier 60-75%; ladder 85-95% | Dossier 290-360 / 360-450 s | Dossier: an interactive "what would you do" with 3-4 options, each killed by a callback to an earlier rung, then a hard verdict. Ladder: the final item answers the title in the title's own words, with the comedy dropped and the tone sober. The most famous rival goes second-to-last (ORCA-ERAS Megalodon at 88-95%). | SPERM verdict at 70%, ORCA answer 61-75%, SWALLOW answer at 92%, DEEP biggest landmark at 72%, PETS winner + held-back checkpoint at 93% |
| L7 | **Twist / reversal** | 70-90% | 340-430 / 420-540 s | Flip the fear: it ignores you, or humans were the real danger, or the expected winner fails, or the opening rule is used against you, or today's ocean is the safest of all. Frame each step as "here's the part nobody tells you". | SPERM twist + villain swap 70-88%, ORCA captivity 75-91%, ERAS no-tools twist 92-99%, SWALLOW legend debunk 77-85%, OCEANS modern-ocean twist at 85%, PETS moral twist at 96% |
| L8 | **Payoff + bookend** | 88-98% | 420-470 / 530-590 s | Return to the opening scene or rule with everything learned (3 callbacks), or recap every verdict in one breath (a tiered board recap: PETS), or count down the unsolved mysteries. Flip the hook's own word (TREX: the movie version is the overrated one). End on an image, not a summary. | SPERM bookend, ORCA "next time you see the sea", DEEP mystery countdown, SWALLOW recap, PETS tier recap, OCEANS 3-callback recap, GATOR three-fates synthesis |
| L9 | **Close / CTA** | 97-100% | last 8-20 s | No spoken CTA (hold the finished board or the last image), or one comment prompt about a specific debatable item (a board row, the unsolved case, the next creature). A standard like/subscribe CTA did not stop SHEEP (18.8x) or TREX (7.9x), so the CTA is neutral; keep it last and short. | ERAS none, DEEP none, ORCA end screen only, SPERM comment CTA, PLANT/SWALLOW joke-threat CTA, ORCA-ERAS 9 s "agree?" over the board, GATOR unsolved-case prompt |

Macro proportions, median across the 11 narrated long outliers: setup (L1-L3) 5-10% (GATOR's roadmap set-up is the outlier at 25%), ladder (L4-L6) 60-80%, turn (L7) 10-25%, close (L8-L9) 3-6%.

**Per-rung formula (long-form, every rung):**
1. Entry: a rhetorical question answered in 1-3 words, or a "here's what's worse" tease, or a numbered card. (SPERM, ERAS, DEEP)
2. One or two hard numbers, each followed within one sentence by an everyday or you-vs-it comparison (bus, elephants, your hand, your one-minute breath-hold). (SPERM, ERAS, ORCA, SWALLOW)
3. A short "you" scenario in present tense, 3-5 actions, each an animation beat. (PLANT, SWALLOW, ERAS)
4. One qualified authority line (a dated study, "researchers measured"); once per video, honestly admit something is unproven. (SPERM, ORCA, SWALLOW)
5. A 1-3 word punch line and a comic deflation. (SPERM, ERAS, SWALLOW, PLANT)
6. A seam: a bonus weird fact or a verdict stamp at the very end so there is no dead air before the next rung. (SWALLOW, ERAS)
7. One recurring graphic motif per rung (scale bar, counter, meter, sonar view, map, document stamp, strike-through list). (SPERM, ERAS)
8. For speculative verdicts, one piece of **evidence from today's animals** transferred to the ancient or imagined matchup (a tactic orcas really use, a real field study, a "natural experiment" with dated numbers). It makes the verdict feel earned. (ORCA-ERAS, PETS)
9. Join rungs with a **gap or trade-off line** that the next rung answers, instead of a chapter card (a "though" tag, a cause-effect bridge, a question naming the next topic). (TREX)

### 1b. Shorts (we make 6, 60-90 s target; corpus outliers now run 29-172 s)

The first sample had no outlier over 59 s. The expansion has three: KITCHEN 67 s, BITE 90 s and WHATIF 172 s (the top Short in the corpus at 69x). All three hold length the same way: **a new rung about every 9-10 s, each with one new number or landmark, and a short "it doesn't stop" line every 15-30 s**. So 60-90 s is safe if you **add rungs, not length per rung**, add the twist beat, or run two creatures back to back. Do not slow the voice down to fill time.

Seconds are given for a 55 s Short and a 30 s Short.

| # | Beat | % of runtime | Seconds (55 / 30 s) | What it must do | Exemplars |
|---|---|---|---|---|---|
| S1 | **Hook** | 0-6% | 0-3 / 0-2 s (median 9 words, 3 s; range 3-22 words) | The title as a second-person scenario or conditional, or the absurd outcome stated first, or the accident already happening, or (new) a past-tense death you must solve, or a known target number with its owner hidden. The subject is on screen in frame 1 even if it is named later. | all 11 |
| S2 | **Stakes / anchor** | 6-20% | 3-11 / 2-6 s | Two numbers (a body count and a multiple of something feared), or a counted inventory ("N tools"), or a misdirect list of famous threats then a pivot, or **you as rung 0** (your own bite, height or breath as the unit every later number is a multiple of). | PUFFER, FLY, JELLY, EEL, ADRIFT, BITE, WHATIF |
| S3 | **Ladder rungs 1-3** | 20-48% | 11-26 / 6-14 s; a new rung every 3-6 s (60-90 s Shorts: every 8-10 s) | Each rung one notch worse; one 3-4 s mechanism aside with the real term plus a plain verb, paid off in the next line. Join rungs with "and / then / so / until" so there is no full stop to swipe on. In list Shorts, every rung fills the same 3-4 slots in the same order (name, mechanism, dose, dismissal). | PUFFER, PRESSURE, FLY, JELLY, KITCHEN, BITE |
| S4 | **Turnstile re-hook** | 45-60% | at ~25 / ~14 s, 1-2 s long | A 4-7 word false reassurance or "not the worst part" line, or a time-jump opener, or "not even top three" where the viewer's guess fails, with a background change on the next word. | PUFFER 46%, JELLY 53%, ADRIFT 48%, EEL 48%, SHOT 47% refrain, BITE 58% |
| S5 | **Peak + main loop closes** | 55-75% (60-90 s ladders: 65-91%) | 26-41 / 14-22 s | The worst outcome, said through jokes or euphemism, or the big reveal of the absurd answer. Long list Shorts hold the answer later: KITCHEN 66%, BITE 91%, WHATIF 91%. | PUFFER 70%, JELLY 53-70%, EEL 70%, ADRIFT 64-72%, FLY 57-65%, KITCHEN 66% |
| S6 | **Twist / second axis** | 60-90% | 41-50 / 22-27 s | Change axis after the peak: hypothetical becomes real, pain becomes disgust, outside becomes inside, step out of the story and rank it, or break the ladder with the least likely item (a joke winner that still fills the same slots). | PUFFER reality flip, FLY disgust axis, PRESSURE inside-to-whole-body, EEL step-out, KITCHEN joke winner at 66%, BITE land-to-water at 61% |
| S7 | **Stinger** | 90-100% | 50-55 / 27-30 s, 2-15 words | End on the strongest word (a finality word, a recurrence fact, a purpose reveal, a callback insult, a two-word verdict that closes line 1's frame). Cut within 1 s. The last frame matches or contrasts the first so the loop is seamless. No CTA. | all 11 |

Macro proportions, median across the 11: hook + stakes 15-20%, ladder 50-70%, peak/twist 15-25%, stinger 3-10%.

**Shorts in a 30-35 s mechanism format** (FLY, PRESSURE, SHOT): drop S6, merge S5 and S7, and put the payoff in the final clause. SHOT shows a variant with no numbers at all: two "mild branch, then worse branch" forks, a refrain said twice, and the one red image held for the last word.

**60-90 s list Short** (KITCHEN, BITE; WHATIF is the 3-minute version): hook 2-4 s, 4-8 rungs of 7-15 s each that get shorter toward the turn, one turn line at 58-66%, the answer at 66-91%, and a final line that repeats the hook's number or frame so it loops. A visible progress device (truck icons filling toward the hook number, a counter in the corner, a suspect line-up with stamps) does the work a scoreboard does in long-form.

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
| H12 | **Past-tense whodunit** (new) | "Something in your [familiar place] killed you" (6 words or fewer) -> which one? -> suspects, each with a dose and a dismissal -> joke winner -> case-closed verdict | KITCHEN (5.19M, 3.58) | The viewer is the victim and the detective. Works for "the deadliest thing on your beach / in a rock pool". Mark any impossible step as a joke hypothetical. |
| H13 | **Tiny rate, huge outcome** (new) | "What if you [grew/sank/drifted] [tiny unit] every [second]?" -> two time-stamped proofs within 5 s -> the final size held back to ~90% | WHATIF (3.32M, 69.27) | The tiny unit in the title does the selling. Keep every number exact (the source drifts at cosmic scale). A "this is a what-if, keep going" waiver after the honest "you'd die" answer (~20%) keeps the premise alive. |
| H14 | **Known number, hidden owner** (new) | A category question that gives away the final number (N trucks of force) but not who reaches it -> you as the baseline rung | BITE (0.39M, 4.90) | The viewer already knows the target, so every rung is measured against it. Keep the claim honest (force equal to N trucks, not crushing N trucks). |
| H15 | **Legend fake-out, then command** (new) | A superstition or curse line -> "just kidding" -> "but seriously, never [do X]" -> "here's why" | SHELLS (0.10M, 3.68) | A stacked 3-part hook (about 11 s) that works because the title is already a command. The fake personal risk at the start is paid by a real one at the end (it is illegal in places). |
| H16 | **Visceral conditional, then walkthrough** (new) | "When [it] happens to you" (3 words) restating the title -> "first" -> a continuous trip through the body, layer by layer | SHOT (2.98M, 11.34) | No number, no question: naming the visceral premise is the hook. A silent title card for 1 s over the threat object is fine only when the object is on screen. Calm clinical voice over a violent topic. |
| H17 | **Crown claim, then counterfactual drop** (new) | The champion's title stated as fact -> 3 escalating proof kills (two famous, one surprising) -> an absolute claim (nothing hunts it) -> the title restated as a counterfactual drop of today's animal into every past X -> scoring rules | ORCA-ERAS (3.86M, 35.87) | No "you" and no teasers: the pull is the absolute claim the viewer expects to see tested. The same tournament without a famous champion or defined scoring (GW-ERAS control, 1.0x) did not pop. |
| H18 | **Movie rule broken, patch notes** (new) | A famous pop-culture survival rule put to "you" -> broken in the next line (you die) -> "new evidence rebuilt it" -> 3 old labels -> 3 headline upgrades as a table of contents -> "far worse" -> a paradox thesis aimed at you | TREX (1.50M, 7.88) | For a famous animal, name it in line 1 and sell the change. Every hook item becomes a later section; three are paid at 4%, 49% and 85-95%. |
| H19 | **Dated true event, plain** (new) | Who, what, where, how deep, said as fact -> a flat "and then they left it" -> access line (I spoke to the scientist) -> what happened + why (why ranked higher) -> science stakes -> title question -> 3-question roadmap | GATOR (6.06M, 6.57) | No 2P scene and no teaser of the result: an odd true event stated plainly is enough. We have no interviewee, so use short attributed paraphrases, never invented quotes. |
| H20 | **"Imagine, no X, no you" + three-tier teasers + rule** (new) | 2P scene with a 3-item "no shelter, no food, no you" list -> title question -> one teaser each from the bottom, middle and top of the list -> fixed checkpoints -> "remember this rule" | PETS (0.52M, 24.70) | The most loaded open in the corpus (54 s): 3 teaser loops, a scoring loop, a guess loop and a rule the viewer applies. Each teaser must be specific and strange. |
| H21 | **Proverb twist** (new) | A known saying -> broken twice (not only X; Y isn't even needed) -> straight into the first clip | SHEEP (7.62M, 18.83) | 32 words in 8 s; the title clip held back to ~15%. Works for underdog versus formats. |

H5 has a near-copy in the expansion: OCEANS (3.37M, 6.54) opens with "picture this, you're dropped", concedes the viewer's monster expectation, trailers 3 monsters, then says the rules change by era. It is ERAS's formula on another channel, and it popped again.

Hook rules across all 21:
- **Median hook length:** long-form about 60 words / 20 s (range 14-134 words, 5-44 s; still two modes: short hooks of 14-32 words in 5-10 s, immersion or table-of-contents hooks of 57-134 words in 18-44 s); Shorts 9 words / 3 s (range 3-22 words, 1-6 s; stacked hooks such as SHELLS reach 33 words / 11 s).
- **"You" within the first 10 words** in 15 of 23 references. The eight that skip "you" (ORCA, DEEP, ADRIFT, EEL, ORCA-ERAS, GATOR, SHEEP, plus BITE until its baseline line at 0:04) replace it with a paradox, a forbidden place, a person in danger, an absurd outcome, a crown claim to test, an odd true event, or a known number with a hidden owner.
- **Name an unknown creature late, show it early; name a famous one at once.** SPERM names it at 0:23, ORCA at 1:23, JELLY at 0:10, PUFFER at 0:44, while each shows it (or its effect) on screen almost at once. TREX, ORCA-ERAS and BITE's category name the subject in line 1, because the change or the contest is the hook.
- **The hook carries a contract.** Every teaser or credential named in the hook is paid off later, in order, the first one by ~4-35% of runtime (ERAS, ORCA, SPERM, PETS at 1:56 / 6:32 / 7:56, TREX at 4% / 49% / 85-95%, OCEANS's first-breath tease closed by the first era).

---

## 3. Re-hook cadence

| Metric | Long-form median (range) | Shorts median (range) | Sources |
|---|---|---|---|
| Any attention reset (pivot, question, gag, cut, callback) | ~25 s (14-35) | ~4.5 s (2.5-10) | PLANT 14 s, DEEP 25 s, SPERM 30 s, ORCA-ERAS 30 (median), OCEANS 30, TREX 29, GATOR 27 (median) / PUFFER 3.5, JELLY 5, EEL 6.5, ADRIFT 4.5, PRESSURE 4.5, FLY 3, SHOT 3, SHELLS 4.5, MEGABAT control 5, WHATIF 9, BITE 10, KITCHEN 10 |
| Explicit verbal re-hook line | ~30 s (25-65) | ~10 s (6.5-30) | SPERM 30, DEEP 25, SWALLOW 42, ORCA 65, ORCA-ERAS 40 (median), PETS 25-35, TREX 29, GATOR 27, OCEANS 30, SHEEP ~60 / PUFFER 15, JELLY 23, ADRIFT 10.5, PRESSURE 9, BITE 15-20, WHATIF ~30 |
| Structural unit (new rung, item, chapter card) | ~75 s (50-300) | rungs every 3-8 s (under 60 s) or 8-10 s (60-180 s) | SPERM ~50, ERAS 62, SWALLOW 62, PETS 61, TREX 75, PLANT 65-100, OCEANS 93, ORCA-ERAS 100, DEEP 200, GATOR ~200 (carcass cliffhangers), ORCA 300 / KITCHEN 10.5, BITE 10, WHATIF 9 |
| Micro-checkpoint inside a unit (time stamp, verdict stamp) | every 5-15 s (PETS); a verdict per era every 1.5-2 min (OCEANS) | a new number every ~5 s (BITE) | PETS, OCEANS, BITE |
| Punch line / joke | every 60-90 s (comedy hosts every 8-12 s; PETS 15-25 s; host opinion line every ~2 min in TREX) | none before midpoint, then every 4-6 s (comedy Shorts); MEGABAT control every 3-4 s | SPERM, SWALLOW, PUFFER, OCEANS (17 deflations), TREX |
| Visual state change | every 2-4 s (ORCA-ERAS cut every 5-10 s) | every 1-3 s; caption card every 0.5-3 s | SPERM, PRESSURE, FLY, ADRIFT, SHOT (12-14 layers in 29 s, only 4 hard cuts) |

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
11. **"Would X save you?" plan loop** (new): offer the viewer a fair escape tool, then kill it with a mechanism, sometimes verdict first ("you still die, here's why"). 15-70 s loops about every 3 min (OCEANS); the viewer's own guess named and broken (PETS's teeth-and-claws favourite).
12. **Counted cliffhanger** (new): a counted return to setup N, an unnamed "something", then 5-8 s with no voice over the reveal shot (GATOR at 32/53/72%).
13. **Gap or trade-off bridge** (new): end a section on what the good fact leaves unexplained, so the next section is the answer (TREX, about one every 1.8 min).
14. **Comment-bait flag** (new): the host says aloud that a ruling will be argued about, which opens a short loop and pre-loads the comment section (ORCA-ERAS, about 1,600 comments).
15. **"It doesn't stop" line** (new, long Shorts): a 3-8 word line placed right after a consequence, where a viewer might think it peaked (WHATIF about every 30 s; BITE's short surprise lines every 15-20 s).

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
| **Scale x landmark** (new) | each time jump paired with one landmark of that size; four ladders climb together (time, comparison, damage, identity: person -> giant -> no longer human) | WHATIF |
| **One fixed unit** (new) | start with your own body as rung 0, then lock onto one everyday unit once numbers get big (trucks: 1.5 -> 3 -> 5 -> 9); the source of the number climbs too (felt, popular, measured, estimated) | BITE |
| **Believability, then broken** (new) | suspects get more plausible rung by rung, then the least likely item wins with the most violent result; units jump from teaspoons to nanograms as the claim gets sillier | KITCHEN |
| **Depth through the body + multiplicity** (new) | surface -> layers -> deepest vital layer -> back to the surface with the result; one path -> bouncing path -> many fragments; each fork spends its mild branch first | SHOT |
| **Escape options removed** (new) | gear -> shore -> cage -> surface -> raft, one per rung, each killed by a mechanism; after the peak, you become too small to matter, then the twist | OCEANS |
| **Sawtooth from the top** (new) | the champion wins early, then real rivals force downgrades, a rebound, and the most famous rival second-to-last | ORCA-ERAS |
| **Victim to threat** (new) | the subject dies fast -> survives near people -> becomes the wild -> damages ecosystems; the flip is announced at 61% | PETS |
| **Visibility down, size up** (new) | each fate shows less on camera (swarm -> tiny worms -> nothing) while the eater gets bigger; the biggest is never seen | GATOR |
| **Surface to engine** (new) | appearance -> childhood -> lifespan -> weapon -> movement (one owned downgrade) -> behaviour -> metabolism -> verdict | TREX |
| **Opponent type** (new) | animal -> machine -> human, places spreading across the map, with planned species breaks every ~60 s | SHEEP |

Ladder rules:
- **The facts become the weapon.** In the climax, kill each escape option with a callback to an earlier rung (SPERM). Viewers feel smart and doomed at once.
- **The peak is not the end.** After the main loop closes, change axis so the back third doesn't sag (JELLY puts its emotional peak before the literal death; PUFFER flips to "this really happens").
- **One planted word, paid twice.** Introduce a failure word early as something avoided, then pay it off partly and then totally (PRESSURE). Long-form: plant at least four throwaway details in the first third and pay each off later (ORCA has 12 plant-payoff pairs; GATOR's rope and weight pay off three times; TREX's eye-socket riddle is closed 10 min later).
- **A rule the viewer can predict with.** State one thesis rule early, tell the viewer to remember it, and call it back each time it knocks out a favourite (PETS: 4 callbacks). The viewer plays along instead of watching.
- **Spend the mild branch first.** At each fork, give the survivable or mild outcome, then the "but sometimes" worse one, so every turn feels like a fall (SHOT, PETS fake-outs, OCEANS's plan tests).

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
| **Safest era is now** (new) | After a ladder of past dangers, today's ocean is the least deadly of all, proved by one hard zero (no recorded fatal wild attacks), then "why it still feels scary" | OCEANS |
| **Joke winner in the same slots** (new) | The least likely suspect wins, but it fills the same name / dose / body-damage slots, so it reads as a real answer | KITCHEN |
| **Underdog winner** (new) | The cheap or small entry teased at the start beats the favourites (fairground goldfish, hornless sheep) | PETS, SHEEP |
| **Owned downgrade, turned** (new) | The one claim that went backwards is admitted openly, then reframed as a different strength (slow, so built for endurance) | TREX |
| **Hook word flipped** (new) | The label the hook attached to the subject (overhyped) is moved onto the myth in the verdict | TREX |
| **Both outcomes bad** (new) | Moral twist after the board: the losers die alone and the winners damage ecosystems, then a one-line practical rule | PETS |
| **Fake risk opens, real risk closes** (new) | A joke personal consequence in the hook is replaced by a real one at the end, softened into a usable rule of thumb | SHELLS |

---

## 6. Endings and CTAs

- **Shorts: 11 of 11 outliers have no CTA** (the MEGABAT control has none either). They end on the strongest word and cut within ~1 s; the last frame mirrors (FLY, ADRIFT, EEL, SHOT) or contrasts (PRESSURE) the first so the loop restarts cleanly. Stinger types: finality word (PRESSURE), recurrence fact (PUFFER), purpose reveal (FLY), callback insult (JELLY), step-out ranking (EEL), flat outcome (ADRIFT), the hook's number repeated (BITE), a two-word verdict closing line 1's frame (KITCHEN), a "you wouldn't just X, you'd Y" identity line cut on a connective (WHATIF), the one gore image held for the last word with survival left open (SHOT), a softened caveat (SHELLS, the weakest ending in the set).
- **Long-form: the three biggest first-sample outliers have no spoken CTA** (ERAS 113x, ORCA 319x, DEEP 12.9x). They end on a finished scoreboard, a moral line or a 3-part emotional button. In the expansion 6 of 6 long-forms have some CTA, including a standard like/bell/subscribe (SHEEP 18.8x) and a subscribe-as-last-word (TREX 7.9x). **The CTA is neutral, not a driver.** What matters is that it comes last, is short (9-30 s) and does not replace the payoff.
- When a CTA is used, the best ones **ask for a comment about something specific and open**: the next creature (SPERM, OCEANS, and the same line in both Depth Theory controls), the debatable board rows (ORCA-ERAS "agree or disagree?", flagged earlier in the video), or the unsolved case (GATOR's third carcass). A **joke threat** that mirrors an earlier gag also works (PLANT, SWALLOW).
- **Bookend.** 9 of 12 long-forms return to the opening image, rule, claim or promise in the last 5% (SPERM, ORCA, DEEP, SWALLOW, ORCA-ERAS's "nothing hunts them", PETS's held-back checkpoint and thesis rule, TREX's flipped hook word, OCEANS's 3-callback recap, GATOR's title question as the last unknown).
- **Finished board as comment bait.** A ranking held on screen for 5+ s at the end makes viewers argue placements (ERAS, ORCA-ERAS held 7 s, PETS's tiered recap).
- **Deliberately open endings now appear in long-form too.** GATOR leaves the third eater unknown and turns it into the CTA; SHOT leaves survival open. Leave at most one question open, and make it the one the viewer most wants answered.

---

## 7. Series and part-2 mechanics

The explainer niche runs on **series formulas, not cliffhangers.** None of the 23 references ends on a "part 2" cliffhanger (that is a horror-niche device; see `research/corpus/horror/`). The nearest is GATOR, whose close is a dated next step (a new camera rig going down soon) plus the unsolved case: a sequel loop tied to the video's own planted object, not a cut-off story.
- **Formulas proven to transfer (expansion):** the ERAS "how long you'd last in every era" engine popped again on its own channel with a famous animal as the traveller (ORCA-ERAS, 35.9x) and on another channel with an ocean-only cast (OCEANS, 6.5x). Spinosnack runs "new evidence just changed [famous animal]" as a series (TREX 7.9x; its Megalodon, Mosasaurus and Spinosaurus versions are 5-7x, per `SOURCES.md`). Occam's "how long would [X] survive" line popped twice (SWALLOW 15.8x, PETS 24.7x).
- **Fixed title formula per series:** "Why you'd never want to meet [X]" (Depth Theory, 3 videos, one fixed script template); "What it's like to [be killed by] [X]" (Dumb Doggo, 3 outliers at 1.8-2.8x); "Nothing about [X] is normal" (Mr. Science, 2 at 2.6x); "[Deadliest X] from every single period" (ExtinctZoo, 2 at 3.7-4.7x); "How [creature] [hurts] you" (Zack D. Films). Formulas transfer across channels: the "deeper you go, the creepier" and "how long you'd last in every X" titles were cloned by Spinosnack (33x) and BeyondTheBlue (11.4x) (SOURCES runners-up).
- **Split a long list into parts** only when the list is large (Dumb Doggo spiders "Part 1", 1.85x).
- **Cross-video callbacks:** a joke that references the channel's previous creature (Depth Theory sperm whale and squid both cite a "stealing dinner" link) rewards binge viewers.
- **Next-creature prompt** in the CTA feeds the topic queue and makes each video an episode.
- **For our Shorts:** use one title formula per series (for example "How [ocean animal] [hurts] you" and "Could you survive [ocean extreme]?") and keep the beat sheet identical between episodes, as Depth Theory does in long-form.

---

## 8. Pacing stats

Computed from the transcripts by `stats.py` (output in `stats.json`: word counts, "you" words, digit and number-word tokens); hook lengths, re-hooks and loops are taken from each annotation file. Recomputed at ~12:50 UTC over the full set: **12 long outliers and 11 Short outliers** (controls listed separately, never in the medians). Shorts sentence lengths for punctuation-free auto-subs (EEL, ADRIFT, PRESSURE, GOBLIN, MEGABAT) use the annotators' counts. SHEEP's words/min is taken over its narrated stretches (about 180); over its whole runtime it is 83 because 57% of it is silent footage.

| Metric | Long-form median (range), n=12 | Shorts median (range), n=11 | Our target |
|---|---|---|---|
| Words per minute | **170** (117-193). The expansion long-forms all run 172-193 | **two clusters:** narrated 171 (150-189, n=8: ADRIFT, WHATIF, SHOT, SHELLS, PRESSURE, FLY, KITCHEN, BITE); talking-head TikTok 288 (275-288, n=3, all Casual Geographic). All 11: 177 | Long 160-175 (Kokoro/Piper; get density from facts per minute, not speed). Shorts 170-210, never above 230 |
| Hook length | ~60 words / 20 s (14-134 words, 5-44 s); two modes: 14-32 words in 5-10 s, or 57-134 words in 18-44 s | 9 words / 3 s (3-22 words, 1-6 s; stacked hooks up to 33 words / 11 s) | Long: ≤30 words/10 s, or 60-100 words/20-35 s for an immersion or table-of-contents hook. Shorts: ≤12 words, ≤3 s |
| Time to first rung / format reveal | ~48 s (8-78 s) | 2-14 s (median ~6 s) | Long ≤50 s; Shorts ≤8 s |
| Average sentence length (words) | 13.3 (8.8-21.2) | 14 (10.8-26; PRESSURE is one 93-word chained sentence) | Long 10-15 with 1-4 word punches; Shorts 11-16 words, or chained clauses |
| Second person: % of all words that are you/your | **1.3%** (0-5.4%); was 2.7% on the first six | 5.4% (0-10.9%) | Depends on premise, see the note below |
| Second person: % of sentences containing "you" | 14% (0-41%), n=11 | 65% (0-100%) | 2P premise: long ≥25%, Shorts ≥60% |
| "You" words per minute | 2.5 (0-8.5) | 11.6 (0-23) | 2P premise: long 4-8; Shorts 10-20 |
| Numbers per minute (digits + number words) | 3.4 (1.5-10.4) | 5.2 (0-12.7) | Long 3-6 (up to 10 if every number is checkable and compared); Shorts 5-8 (ranking Shorts up to 12) |
| Open loops per minute (annotated loop tables) | 0.84 (0.51-1.44), n=11 | 6.4 (4.5-10.3), n=7 counted at micro-loop grain; the other 4 new Shorts were annotated with only their 1-2 spine loops | Long: 3-7 long loops opened in the first minute + ~1 new loop/min; Shorts: 1 spine loop + a micro loop or new rung every 5-10 s |
| Max short loops open at once | ~2 | 1 spine + 1 micro | same |
| Long-loop close points | ~35%, 50%, 70%, 98% (SPERM); teasers paid at 35/60/75/90% (ERAS); 4/49/85-95% (TREX); 32/53/72% (GATOR) | spine closes at 64-100% (median ~70%; 60-180 s list Shorts at 66-91%) | same |

**Second person depends on the premise.** The long-form "you" median fell because four of the six new long outliers are third-person by design (ORCA-ERAS champion, GATOR true story, TREX new evidence, SHEEP clips) and PETS casts the viewer as the owner. Where the viewer is the one tested, the outliers stay high (OCEANS 3.7% / 36%, PLANT 5.4% / 41%, ERAS 3.5% / 29%). Rule: if "you" are tested, keep long ≥3% of words / ≥25% of sentences and Shorts ≥5% / ≥60%; if the premise is a famous champion, a true story or a new-evidence dossier, 0.5-2% is normal, but put the viewer in the frame at least three times (hook, one present-tense scene, verdict), as TREX does.

Per-video computed values (for reference):

| id | wpm | avg sentence | you % words | you % sentences | you/min | numbers/min | loops/min |
|---|---|---|---|---|---|---|---|
| SPERM fGcgWaswMns | 168 | 12.7 | 2.4 | 21 | 4.0 | 3.3 | 0.90 |
| ERAS nAWpLtG-kNs | 166 | 9.1 | 3.5 | 29 | 5.8 | 3.5 | 0.62 |
| ORCA VtrcKTkhDHU | 117 | 21.2 | 0.3 | 4 | 0.3 | 1.9 | 0.83 (recount of the updated loop table; was 0.45) |
| DEEP mzeN0BXR4e0 | 122 | 12.1 | 0.0 | 0 | 0.0 | 1.5 | 0.84 |
| SWALLOW JkAcCdqYJN0 | 146 | 9.3 | 3.0 | 24 | 4.4 | 6.4 | 0.98 |
| PLANT QxM2Hu70tVk | 159 | 12.6 | 5.4 | 41 | 8.5 | 2.7 | 1.36 |
| ORCA-ERAS UNPK8PNCCmQ | 172 | 14.8 | 0.3 | 4 | 0.5 | 6.1 | 0.89 |
| PETS thtoMGvpWIU | 187 | 8.8 | 1.7 | 12 | 3.1 | 10.4 | 1.44 |
| SHEEP UfbYyHuVx5M | ~180 narrated (83 whole runtime) | ~14 (annot.) | 0.7 | n/a | 0.6 | 2.3 | n/a (one weak spine loop) |
| TREX lVV5ztC3CtI | 187 | 16.6 | 0.8 | 9 | 1.5 | 8.6 | 0.64 |
| GATOR SDs41Ke3v4Q | 193 (auto-subs keep fillers; clean ~175-180) | 17.4 | 0.9 | 14 | 1.8 | 3.4 | 0.62 |
| OCEANS qrfhhZ-Wvmk | 179 | 13.8 | 3.7 | 36 | 6.6 | 2.6 | 0.51 |
| PUFFER XFFjxTllpoA | 288 | 14 | 7.8 | 65 | 23.0 | 7.3 | 6.1 |
| JELLY jw6bS-WL4F4 | 275 | 13.9 | 5.3 | 67 | 14.5 | 5.2 | 5.2 |
| EEL Ky0XPonYDcc | 288 | 16 | 0.0 | 0 | 0.0 | 1.5 | 4.5 |
| ADRIFT 4QGQhaRv4Dw | 150 | 13 | 0.0 | 0 | 0.0 | 1.6 | 6.4 |
| PRESSURE fmZfphacPPQ | 172 | 93 (1 sentence) | 8.6 | 100 | 14.8 | 7.4 | 9.1 |
| FLY 6mRR91AbxjQ | 177 | 26 | 6.2 | 67 | 12.8 | 7.7 | 8.7 |
| WHATIF 2d6Ciu3INeA | 153 | 10.8 | 10.9 | 88 | 16.6 | 6.0 | (1 spine loop + a rung every ~9 s) |
| SHOT V15wrmD5VFs | 168 | 25.7 | 2.6 | 67 | 4.4 | 0.0 | 10.3 |
| BITE ZZf1KBnH5iI | 189 | 20.3 | 0.7 | 7 | 1.3 | 12.7 | (1 spine + 1 micro) |
| SHELLS LpUzg3Dc-m0 | 170 | 11.3 | 5.4 | 38 | 9.2 | 0.0 | (1 spine + 1 micro) |
| KITCHEN 2cK8l5Yg5w8 | 180 | 12.6 | 6.5 | 50 | 11.6 | 3.6 | (1 spine, re-opened by 3 dismissals) |
| *control* SQUID 2819-mQEA9M | 172 | 12.4 | 1.8 | 16 | 3.0 | 5.8 | - |
| *control* HUMPBACK 4Mmo_dlsArE | 172 | 12.3 | 2.1 | 17 | 3.6 | 6.4 | - |
| *control* GW-ERAS mg2YJ04Hl9k | 153 | 10.7 | 0.3 | 3 | 0.4 | 4.7 | - |
| *control* ROCKS JavhxLs3Cs8 | 162 | 13.9 | 1.8 | 21 | 3.0 | 1.0 | - |
| *control* SKY uH-hucq-dmA | 195 | 22.9 | 0.5 | 8 | 1.0 | 3.9 | - |
| *control* GOBLIN U35yA-9nVEA | 272 | n/a | 1.9 | n/a | 5.3 | 4.2 | - |
| *control* MANTIS XffxtLGdXUQ | 172 | 14.6 | 0.0 | 0 | 0.0 | 2.4 | - |
| *control* MEGABAT PoF_doh3NOE | 288 (speech span) | ~16 (annot.) | 1.6 | 19 (annot.) | 4.5 | 6.8 (4.5 spoken figures/min) | - |

Notes: the number count is approximate (it includes "one" used as a pronoun). Loop counts depend on how finely each annotator split loops; Shorts also have many uncounted cause-effect micro loops. The first-sample Shorts rows keep the annotators' wpm where it differs slightly from `stats.json` (which measures from the first caption to the last caption + 2.5 s). Whisper-transcribed rows (SHOT, BITE, SHELLS, KITCHEN, ORCA-ERAS, TREX) may differ by a few words.

---

## 9. Outliers vs ordinary: what the top scripts do that weaker ones don't

Each comparison holds the channel, art style and narrator constant, so the difference is mostly the script.

1. **The viewer (or a human) is the one at risk.** In every channel pair the outlier uses more second person:
   - Depth Theory: SPERM 2.4% "you" words / 21% of sentences vs SQUID 1.8% / 16% and HUMPBACK 2.1% / 17%. The R1 shot count agrees: SPERM spends 12% of its 5 s windows on the diver/YOU, SQUID 3%.
   - Dumb Doggo: PLANT 5.4% / 41% vs ROCKS 1.8% / 21%.
   - Casual Geographic: PUFFER 7.8% and JELLY 5.3% vs GOBLIN 1.9%.
   - Zack D. Films: FLY 6.2%, PRESSURE 8.6% and ADRIFT (a human victim) vs MANTIS 0% (lizard vs mantis, no human).
   - Depth Theory GW-ERAS (1.0x) uses the ERAS tournament but drops a shark into the eras, not you (0.3% "you"); ERAS (113x) drops you.
   - Casual Geographic again (expansion): PUFFER 7.8% and JELLY 5.3% vs the MEGABAT control 1.6% (the viewer leaves the frame after the 6 s size hook).
   The exceptions (ORCA, DEEP, and from the expansion ORCA-ERAS, GATOR, TREX, SHEEP) replace "you" with an even stronger master question: a paradox, a descent into the unknown, a famous champion with an absolute claim to test, an odd true event, or a known animal rebuilt by new evidence. **If there is no "you", there must be a paradox or a claim the viewer wants to see tested.** The sharpest test: ORCA-ERAS (35.9x) and GW-ERAS (1.0x) are both third-person era tournaments with 0.3% "you"; the outlier has a famous champion, defined scoring words, today's real hunting tactics as evidence, and verdicts it says out loud will be argued. Within Fossil, the "you" version (ERAS, 113x) still beat the champion version (35.9x).
2. **Immersion beats assertion in the first 20 s.** SPERM opens on a felt sensation in a scene and a rule about to break; SQUID (same template, same voice) opens on a general claim about what has been filmed. MEG (0.96x) spends ~50 s on a slow named-person story before the subject. GOBLIN (0.78x) spends its first 7 s (12% of runtime) on silent footage. Every outlier Short is talking about the threat within 1 s.
3. **Fewer raw numbers, more comparisons.** The Depth Theory controls are more number-dense (SQUID 5.8/min, HUMPBACK 6.4/min) than SPERM (3.3/min). SPERM turns almost every number into a bus, an elephant, your hand or your breath. Density of facts is not the driver; how felt each fact is, is.
4. **More jokes and less stock.** SPERM has a comic deflation every 60-75 s and only ~3% stock footage; SQUID has ~10 jokes over 10 min and 12% stock. Comedy keeps the death ladder light enough for a broad audience (PLANT, SWALLOW, PUFFER).
5. **A visible progress device.** Outliers show the shape of the video: tier board (ERAS), stopwatch (SWALLOW), countdown cards (PLANT), zone diagram (DEEP), numbered options with strike-throughs (SPERM). ROCKS has a collection shelf too, so the device helps but is not enough without a threat to the viewer.
6. **A bigger category and a famous subject.** ExtinctZoo's sea/apex videos (3.7-4.7x) beat its sky video (1.16x) with the same format. SPERM (a famous whale with a famous sinking story) beat SQUID (a little-known animal) with the same template. Choose the subject people already half-know and fear.
7. **The hook makes promises and the body keeps them in order.** ERAS pays its four teasers at 37/63/77/92%; ORCA pays hook items 1 and 2 by 25%; SPERM closes its sensation loop at 37%. SKY (1.16x) takes 62 s to state its question.
8. **Shorts start speaking about the danger immediately, never stop for breath, and never end on a CTA.** All 11 outlier Shorts: hook ≤6 s (SHOT's 1 s silent card shows the gun), stinger on the last word, loop. The three Shorts controls are slow to start (GOBLIN 7 s silent, MEGABAT a 4 s borrowed stitch before the first word) or have no human stake (MANTIS).
9. **The master question stays open until late** (new, MEGABAT vs PUFFER/JELLY). MEGABAT answers "is it a monster?" at 38% and spends half its runtime on a charm list with no rising stakes; the same channel's outliers keep making things worse for you until the last 10 s, and its "but don't worry" means "it gets worse", not "it's harmless". The new long Shorts agree: the answer lands at 66% (KITCHEN) or 91% (BITE, WHATIF).
10. **A loaded open beats a bare one on the same channel** (new, PETS 24.7x vs SWALLOW 15.8x, Occam). PETS opens with three specific teasers from the bottom, middle and top of the list, fixed checkpoints, and a rule to remember, and reads at 187 wpm vs 145 with more numbers (10.4/min vs 6.4); SWALLOW had a 14-word hook. Same narrator style, same countdown, so the open and the density are the difference.
11. **Checkable evidence and owned uncertainty** (new). The higher-scoring new long-forms cite dated studies and named people (TREX about 17 scientists and 21 years; PETS about 30 dated or counted facts, almost all correct), hedge about 11-15 times (ORCA-ERAS, TREX, GATOR), and admit one downgrade or one unknown openly. Admitting what is not known makes the firm verdicts more believable and gives commenters something to argue with.
12. **A visible progress device still shows up in nearly every outlier** (ORCA-ERAS five-row board, PETS checkpoint columns, OCEANS per-era verdicts, BITE's truck row, KITCHEN's suspect line-up). The MEGABAT control has none: no scale bars, no progress device, only stills.

---

## 10. Writer checklist (every box must be ticked before the originality gate)

**Front matter**
- [ ] `references:` lists 2-3 corpus ids closest to the premise, with url, views and outlier_score (from `INDEX.json`).
- [ ] A beat alignment table maps each of our beats to a reference beat, its timestamp, and the device borrowed.
- [ ] A fact list with a source for every number and mechanism.

**Premise and title**
- [ ] The premise puts "you" (or a human) at risk, **or** states a paradox / descent into the unknown / a famous champion's absolute claim to test / an odd true event. Not a neutral fact tour or a "meet the X" charm list.
- [ ] The subject is famous or half-known and feared; the category is broad (ocean, deadliest, every depth).
- [ ] The title uses one series formula (H2-H21 shapes) and the hook restates or enacts it.

**Hook**
- [ ] Shorts: ≤12 words and ≤3 s, "you" (or the victim, or you as rung 0) within the first 10-15 words, subject on screen in frame 1, first spoken word within 1 s.
- [ ] Long-form: ≤30 words/10 s, or a 60-100 word immersion / table-of-contents hook (unknown creature named last; famous creature named first); promise + progress device on screen by 50 s.
- [ ] The hook opens one master question and lists its teasers; each teaser is paid later, in order, the first by ~35%.

**Body**
- [ ] Each rung is strictly worse (or closer to the answer) than the last; the ladder climbs on two axes.
- [ ] Every number is followed within one sentence by an everyday or you-vs-it comparison, with an on-screen scale prop.
- [ ] Re-hook cadence met: Shorts a reset every 3-6 s (60-90 s Shorts: a new rung every 8-10 s) and a turnstile line at 45-60%; long-form a reset every ~25 s, a verbal re-hook every ~30 s, a new rung every 40-100 s, and one "flip" line at 58-66%.
- [ ] Shorts: the master question is not answered before ~65% (no early defusing).
- [ ] Long-form: 3-4 long loops opened in the first minute and closed at about 35/50/70/98%; at least 4 planted details paid off later; a "picture it again" re-immersion near 47%; a comic deflation every 60-90 s.
- [ ] Climax uses earlier facts against the viewer (options killed by callbacks, or the last item passing the learned test).
- [ ] A twist after the peak changes axis (villain swap, reality flip, opening rule turned against you, myth-bust).

**Pacing**
- [ ] Words/min: long 160-175; Shorts 170-210, never above 230 (TTS).
- [ ] "You" in ≥25% of sentences (long) or ≥60% (Shorts) when the viewer is tested; for champion, true-story or new-evidence premises, the viewer is put in the frame at least 3 times (hook, one scene, verdict).
- [ ] Average sentence 10-15 words (long) with 1-4 word punch lines; Shorts chained clauses with no full stop before the payoff.
- [ ] Numbers: long 3-6/min (up to 10 if each is checkable and compared); Shorts 5-8/min (ranking Shorts up to 12).
- [ ] At least one honest hedge or owned unknown; every study named with its year is real and checked.

**Ending**
- [ ] Shorts: stinger on the strongest word, cut within 1 s, last frame matches or contrasts the first, no CTA.
- [ ] Long-form: a bookend to the opening (or a finished board, or a mystery countdown), then either no CTA or one ≤20 s comment prompt about something specific (the next creature, a debatable board row, the one open question).

**Safety and originality**
- [ ] No self-harm or suicide wording; death and gore handled by euphemism, jokes or cartoon dissolve (R5).
- [ ] No sentence copied from any reference; `originality_check.py` prints PASS.

---

## 11. Study these three first

1. **fGcgWaswMns: Depth Theory sperm whale** (2.31M, 14.65x). The style and voice we are copying, and the full dossier template: immersion hook, reframe, 7-rung capability ladder, options climax, twist, villain swap, bookend. Read with its control SQUID (2819-mQEA9M, `research/R1/beatmaps/`) to see which changes made it pop.
2. **nAWpLtG-kNs: Fossil, how long you'd last in every era** (12.21M, 113.57x). The ladder/countdown template with a fixed per-item checklist, a sawtooth verdict curve, a visible tier board, and a final twist that uses the opening rule. It maps directly onto "how long you'd last at every ocean depth / next to every sea creature".
3. **XFFjxTllpoA: Casual Geographic pufferfish** (7.93M, 1.69x). The best 60 s Short skeleton for our Shorts slot: title-as-promise hook, two stakes numbers, a timed body ladder, a turnstile at 46%, death told through jokes, a reality flip and a recurrence stinger. Slow it to 200-230 wpm for TTS and add 2-3 rungs to reach 70-80 s.

Next in line: **fmZfphacPPQ** (the 30 s depth ladder with a depth meter; best for code-only visuals), **VtrcKTkhDHU** (the paradox hook for a long-form open), **jw6bS-WL4F4** (the ocean Short with misdirect, pivot and turnstile).

From the expansion, by use case:
- **qrfhhZ-Wvmk (OCEANS)** for any ocean "how long would you last" long-form: the closest premise to ours, with the plan-killer loops and the safest-era twist.
- **ZZf1KBnH5iI (BITE)** and **2cK8l5Yg5w8 (KITCHEN)** for 60-90 s list Shorts: one fixed comparison unit with a progress row, or a suspect line-up with fixed slots and a joke winner.
- **2d6Ciu3INeA (WHATIF)** for a scale ladder that holds past 60 s, and for the counter-in-the-corner visual.
- **thtoMGvpWIU (PETS)** for the loaded open (three teasers + checkpoints + rule) and the 61% flip.
- **UNPK8PNCCmQ (ORCA-ERAS)** for a third-person champion tournament ("would orcas / sperm whales / great whites survive every ocean").
- **SDs41Ke3v4Q (GATOR)** for a deep-sea true-story long-form (whale falls, bait-camera drops).
- **PoF_doh3NOE (MEGABAT control)**: read against PUFFER and JELLY before writing any "meet the X" profile.

---

## 12. What changed with the expansion

Added at ~12:50 UTC after the 12:08 expansion (11 outliers + 1 control, 8 new channels; see `SOURCES.md`). The sample is now 23 outliers (12 long, 11 Shorts) and 9 controls.

**What held**
- The engine: one master question opened in the first seconds, a ladder that climbs on two or more axes, a turn after the peak, and an ending that closes the loop. Every new outlier fits it, including the true-story (GATOR) and clip (SHEEP) formats.
- Shorts never use a CTA (11 of 11; MEGABAT control too), end on the strongest word, and loop the last frame into the first (BITE repeats the hook number, KITCHEN closes line 1's crime frame, WHATIF cuts on a connective).
- Shorts hook length: still a median of 9 words / 3 s (KITCHEN 6 words, SHOT 3, BITE 16).
- Second person still separates outliers from controls inside a channel: MEGABAT (1.6%) loses to PUFFER (7.8%) and JELLY (5.3%), as GOBLIN did; ERAS (you) beats ORCA-ERAS (champion) on the same channel.
- The hook is a contract paid in order (PETS pays its three teasers at 1:56, 6:32 and 7:56; TREX pays its three headline upgrades at 4%, 49% and 85-95%).
- A visible progress device appears in almost every outlier (ORCA-ERAS board, PETS checkpoints, BITE truck row); the control has none.
- Ladder formulas transfer across channels: the ERAS engine popped again twice (ORCA-ERAS 35.9x, OCEANS 6.5x).

**What shifted**
- **Shorts length.** The 59 s ceiling is gone: KITCHEN 67 s, BITE 90 s and WHATIF 172 s (69x, the top Short in the corpus). Length is fine as long as a new rung lands every ~9-10 s (section 1b).
- **Long-form pace.** Median words/min rose from 152 to 170 (range 117-193); every new long-form reads at 172-193 (PETS 187, TREX 187, GATOR ~175-180 clean). The TTS target moves to 160-175; we still get density from facts, not speed.
- **Long-form "you".** The median fell from 2.7% to 1.3% of words, because four new outliers are third-person by design (ORCA-ERAS, GATOR, TREX, SHEEP) and PETS makes the viewer the owner. "You" is now a premise choice, not a fixed floor (section 8 note).
- **Long-form hook length.** Median rose from 48 to ~60 words; table-of-contents hooks of 100+ words work when each item becomes a section (TREX 134 words / 39 s).
- **CTAs in long-form.** All six new long-forms have a CTA, including a standard subscribe ask (SHEEP 18.8x). The CTA is neutral; the best ones ask about one specific open item (ORCA-ERAS board rows, GATOR's third carcass).
- **Numbers per minute.** The long-form range widened to 1.5-10.4 (PETS 10.4, TREX 8.6): dense numbers work when each one is dated, checkable and compared. The median barely moved (3.0 to 3.4).

**New patterns**
- **The 60-65% flip** (L5b): PETS's list flip at 61%, BITE's land-to-water rule at 61%, ORCA-ERAS's first real rival at 63%, OCEANS's planned peak at 63-68%, TREX's owned downgrade at 60-66%.
- **New hook formulas H12-H21:** past-tense whodunit (KITCHEN), tiny rate huge outcome (WHATIF), known number hidden owner (BITE), legend fake-out then command (SHELLS), visceral conditional walkthrough (SHOT), crown claim then counterfactual drop (ORCA-ERAS), movie rule broken then patch notes (TREX), dated true event stated plainly (GATOR), three-tier teasers + rule (PETS), proverb twist (SHEEP).
- **New long-form variants:** checkpoint countdown (PETS), third-person champion tournament (ORCA-ERAS), plan-killer ladder (OCEANS), patch-notes dossier (TREX), true-story mystery box with counted cliffhangers (GATOR).
- **New devices:** a rule the viewer is told to remember (PETS), "would X save you?" plan loops (OCEANS), fixed slots per list item so a joke winner still feels real (KITCHEN), you as rung 0 with one fixed unit (BITE), evidence from today's animals for speculative verdicts (ORCA-ERAS), gap or trade-off bridges between sections (TREX), owned uncertainty and one owned downgrade (TREX, ORCA-ERAS, GATOR), a comment-bait flag spoken before an unpopular ruling (ORCA-ERAS), one planted object paid three times (GATOR's rope).
- **New control lesson** (MEGABAT PoF_doh3NOE): answering the master question at 38% and switching to a charm list is what an ordinary Short from an outlier channel looks like, even with good jokes and a strong size-vs-you hook.
- **What does not transfer:** SHEEP's 57% silent footage (real clips carry it; code visuals cannot), GATOR's interview audio (use short attributed paraphrases instead), and the fact errors flagged in SHOT, BITE, OCEANS and WHATIF.
