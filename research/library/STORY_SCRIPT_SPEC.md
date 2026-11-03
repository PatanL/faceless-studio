# Story script spec (RicksClips3000 parity, story lane)

Measured 2026-11-02 on all 24 RicksClips3000 story-style Shorts (2026-10-07 to 11-01). Internal research: the
numbers are facts about their videos; every example line below is ours. Use with `research/library/LANE_PRINCIPLES.md`
(topic choice: S1-S6, S-env), which matters more than anything here: the judge below can't tell a weak topic from a
strong one (How a Mirror Rigged a Horse Race, bottom tier, scores 86 on craft).

- **Data:** `research/references/data/ricks24_beats.json` (words with timings, sentences, hand-coded beats, per-video
  metrics; text and timings only). Build script and hand coding: `ricks24_beats_build.py`, `ricks24_beats_ann.py` next to it.
- **Timings:** the 8 refs with audio (the 720p copies) were transcribed with faster-whisper medium.en on the Mac; the
  other 16 use the YouTube en-orig vtt word onsets, which agree with whisper to a median 0.04-0.10 s (p90 0.12-0.20 s).
  Pauses are exact (to whisper's ~50 ms) for the 8 and estimated for the 16 (counts within ~25 %).
- **Tiers:** by views, top 8 (8.7-30.7M), middle 8 (5.9-8.4M), bottom 8 (0.10-4.6M). "Rest" = middle + bottom.
- **Judge:** `pipeline/qa/script_judge.py` scores a script against this file; rubric items via
  `pipeline/qa/SCRIPT_JUDGE_PROMPT.md`. On the references it gives top median 90.6, middle 70.0, bottom 63.9
  (`research/library/script_reports/calibration_ricks24.txt`).
- **Lever vs floor.** A *lever* splits the top 8 from the rest; a *floor* is shared by every tier (needed, but it
  won't make a hit). n = 8 vs 16, so levers are medium confidence at best.

## Top 10 rules

1. **Teach 4-7 real facts, and no more.** The top 8 teach a median of 5 distinct real-world claims (2-7); 7/8 teach
   at least 4, against 5/16 of the rest. Above 7 the story turns into a list. *(lever)*
2. **Use few numbers: 1-5 number tokens in the whole script.** Top median 3 (1-5), rest median 5.5 (up to 15). One
   hero number is enough; turn the others into pictures ("taller than the mast", "a finger-wide gap"). *(lever)*
3. **Four escalation steps, about 5-10 s each.** Top median 4 steps (2-6), each a median 7.2 s; 6/8 top have 4 or
   more, against 4/16 of the rest. Each step is a time jump plus a new event that makes the odd act look worse. *(lever)*
4. **Finish the setup by 30 % of the runtime.** The first escalation step starts at 17-34 % in the top 8 (median
   30 %), 38 % in the rest (up to 53 %). *(lever, medium-low)*
5. **Turn into the reason at 55-80 %, once.** 7/8 top have a pivot sentence, at 55-81 % (median 66 %). It is the
   phrase "You see" in only 3/8 top; the others turn with "Inside the jar...", "That's because...", "Wait, practiced?".
   "You see" works in two places only: the backstory bridge right after the hook (<= 12 %, 4/8 top, 2/16 rest) or
   the pivot (60-81 %). Never in the middle. *(floor for having a pivot; placement is a floor too)*
6. **Explain in 30-50 words, slower.** Mechanism: top 32-49 words, 9-15 s, 15-32 % of the script. The top 8 slow
   down after the pivot (3.58 w/s in the mechanism, 3.51 on the last line, against 3.67 overall); the rest speed up
   (3.84 and 4.17). Use one everyday comparison if it helps. *(lever, low-medium)*
7. **Hook: one declarative sentence of 9-21 words, said in 3-5.5 s, showing the odd act.** Top hook median 14 words,
   4.1 s. A second short sentence may complete the paradox (2/8 top). No question, no date or place opener, no
   "imagine" in the top 8. Frame 0 shows the protagonist doing the act in all 24. *(floor)*
8. **3.4-3.9 words/s, short gaps, nothing long.** All 24 sit at 3.36-4.09 w/s (top median 3.67). Gaps >= 150 ms:
   2.3-5.5 per 10 s, mean 0.22 s, longest 0.30-0.50 s; at most one gap >= 0.4 s and none >= 0.8 s. About 45 % of the
   gaps are at full stops and most of the rest at commas. *(floor)*
9. **Give the doubters a line, and get two laughs.** Top median 2 character lines (0-5; >= 2 in 5/8 top vs 5/16
   rest) and 2 jokes (1-4; >= 2 in 6/8 top vs 6/16 rest), usually the same lines: a jeer at the odd act, a deadpan
   aside. At least one reversal, where the mockers are proved wrong. *(lever, low-medium)*
10. **End on the payoff, 11-24 words, and stop.** Last line top median 16.5 words; it lands the consequence (the
   palace falls, the wave hits the pirates, the train jumps the rails), never a question (0/8 top, 2/16 rest), never
   an epilogue; the video ends 0.1-0.5 s after the last word. *(floor)*

Also a floor: **name something on screen in every sentence.** At the midpoint of each sentence the thing it names
is in frame for a median 97 % of sentences in the top 8 (93 % in the rest, never below 68 %). And: 55-65 s, 200-245
words, sentence median 10-15 words, longest about 25.

## All measured rules

| Rule | Target | Top 8 (median, range) | Rest 16 | Lever? | Judge check |
|---|---|---|---|---|---|
| Runtime | 55-65 s | 62 (39-65) | 56.5 (31-78) | floor (the two shortest are the two lowest) | `runtime_s` |
| Words | 200-245 | 219 (145-247) | 206 (112-295) | floor | `words` |
| Words/s (speech span, pauses in) | 3.4-3.9 | 3.67 (3.36-3.84) | 3.72 (3.47-4.09) | floor | `wps` |
| Gaps >= 150 ms per 10 s | 2.3-5.5 | 3.7 (3.0-5.4) | 3.8 (2.3-5.5) | floor | `pauses_per_10s` |
| Gaps >= 0.4 s / >= 0.8 s | <= 1 / 0 | 0 (0-1) / 0 | 0 / 0 (whisper refs) | floor | `pauses_ge400` |
| Total gap time | about 4-7 s per minute | 5.1 s (3.9-7.1) | 4.2 s (3.3-6.3) | floor | report |
| Mechanism + last line pace vs overall | equal or slower | -0.1 to -0.2 w/s | +0.2 to +0.5 w/s | lever (low) | `mech_slower` |
| Hook words | 9-21 | 14 (9-21) | 14.5 (8-23) | floor | `hook_words` |
| Hook spoken in | 3-5.5 s | 4.1 (3.0-5.4) | 3.8 (2.2-6.4) | floor | `hook_s` |
| Hook form | declarative odd act or paradox fact | 8/8 | 15/16 (one question hook, #23) | floor | `hook_form` |
| Setup ends at | <= 30-35 % | 30 % (17-34) | 38 % (16-53) | lever (medium-low) | `setup_end_pct` |
| Escalation steps | 3-6 (aim 4) | 4 (2-6); >= 4 in 6/8 | 2.5 (0-7); >= 4 in 4/16 | **lever** | `esc_steps` |
| Escalation step length | 5-10 s | 7.2 (4.9-10.4) | 7.9 (5.2-11.7) | floor | report |
| Pivot present | yes | 7/8 (Cannonballs is a levels ladder) | 15/16 | floor | `pivot_pct` |
| Pivot position | 55-80 % | 66 % (55-81) | 71 % (21-91) | floor | `pivot_pct` |
| "You see" | <= 12 % or 60-81 %, at most 2 | 7/8 use it; 4/8 as the early bridge | 9/16 use it; 2/16 early | floor | `you_see` |
| Payoff after the explanation | yes | 7/8 | 11/16 | weak | rubric |
| Mechanism words | 30-50 | 40.5 (32-49) | 37 (14-92) | the top 8 never run long | `mech_words` |
| Mechanism time | 9-15 s | 11.3 (8.9-15.5) | 10.3 (3.4-32) | same | report |
| Distinct facts | 4-7 | 5 (2-7); >= 4 in 7/8 | 2 (0-6); >= 4 in 5/16 | **lever** | rubric `facts` |
| Number tokens | 1-5 | 3 (1-5) | 5.5 (1-15) | lever | `numbers` |
| Character lines | 1-3 | 2 (0-5); >= 2 in 5/8 | 1 (0-4); >= 2 in 5/16 | lever (low) | `dialogue` |
| Jokes | 2-4 | 2 (1-4); >= 2 in 6/8 | 1 (0-5); >= 2 in 6/16 | lever (low) | rubric `jokes` |
| Reversals | 1-2 | 1 (0-3) | 1 (0-2) | floor | rubric `reversal` |
| Sentences | 14-20 | 16.5 (9-21) | 14 (9-23) | weak | report |
| Sentence length | median 10-15, longest <= 30 | 12.5 (10-27), longest 25 | 14, longest 27 | weak | `sentence_len` |
| Punch lines (<= 6 words) | 10-35 % of sentences | 15 % (0-33) | 11 % (0-36) | floor | `sentence_len` |
| "you" per 100 words | not a lever | 2.3 (0.9-9.7) | 1.6 (0-9.6) | none (S7) | report |
| Sentences that name what's on screen | >= 90 % | 97 % (70-100) | 93 % (68-100) | floor | rubric `shootable_share` |
| Last line | 11-24 words, no question | 16.5 (11-33); 0/8 questions | 16 (6-22); 2/16 questions | floor | `last_line` |
| Video after the last word | <= 0.5 s | 0.2 (0.1-0.5) | 0.2 (0.1-0.8) | floor | `last_line` |

## Beat sheet template (a 62 s Short, ~225 words at 3.65 w/s)

| Beat | Target seconds | % of runtime | Words | What it does |
|---|---|---|---|---|
| Hook | 0.0-4.5 | 0-7 | 12-18 | One sentence. The protagonist does the strange thing (or a law/fact contradicts what everyone sees). It is frame 0. |
| Doubt or bridge | 4.5-8 | 7-13 | 5-20 | Either the crowd mocks the act (a short line or a jeer) or "You see," opens the backstory. Not both at length. |
| Setup | 8-18 | 13-30 | 30-40 | Who, where, what's at stake, the device or rule seen plainly. Two or three sentences. Ends by 30 %. |
| Escalation 1-4 | 18-41 | 30-66 | 4 x 18-28 | Four time jumps. Each: a new event, the odd act looks worse, someone reacts (jeer, joke, threat). The last one is a cliffhanger: the disaster is visible and about to land. |
| Pivot | ~41 | 60-70 | 6-16 | One sentence that turns to the reason. "You see," is fine here; so is a plain "Inside the ... was ...". |
| Mechanism | 41-53 | 66-85 | 30-45 | The physical cause, step by step, each step a picture. One everyday comparison at most. Read slightly slower. |
| Payoff + last line | 53-61.8 | 85-100 | 15-25 | The consequence lands, ideally on the mockers. The last line names the payoff image and ends the video within 0.3 s. No epilogue, no question, no moral. |

Escalation steps run 5-10 s; if one needs more than 10 s it is two steps or it is padding.

## Line craft: do and don't (our own examples)

**Hook**
- Do: "A shogun paid his carpenters to build a floor that squeaks." (11 words, an odd act that is frame 0.)
- Do: "Every soldier in the city was ordered to lay his shield flat on the ground." (paradox you can see.)
- Don't: "In 1603, in Kyoto, Japan, a new castle was being built." (date and place first; nothing strange yet.)
- Don't: "Have you ever wondered why some floors squeak?" (question hook; 0/8 top.)

**Setup and doubt**
- Do: "The court thinks the floor is broken. A minister jokes that the shogun's guards can go home now." (a doubter's line and a laugh in the same beat.)
- Don't: "The castle had many rooms, gardens and gates, built by hundreds of workers over many years." (facts with no doubt and no stakes.)

**Escalation**
- Do: "Weeks later, a guest tiptoes to the shogun's door. Every board chirps like a bird." (time jump, new event, sound you can show.)
- Don't: "Over the following decades, many events took place at the castle." (no event, no picture.)

**Numbers**
- Do: one hero number, the rest as pictures: "The river splits in two, and the bigger half goes where the farms are."
- Don't: "In 256 BC, 4 metres of water, 60 % of the flow, 2,000 years, 5,300 square kilometres." (the top 8 never use more than 5.)

**Pivot and mechanism**
- Do: "You see, every nail sits in a metal clip, and when a board bends, the nail rubs the clip and sings." (a cause you can draw.)
- Do: "Think of a full bucket on a stool: heavy low, it stands; heavy high, one nudge and it goes." (one comparison, then back to the story.)
- Don't: "This is due to the frictional properties of the fastening system, which engineers call..." (term first, picture never.)
- Don't: put "You see" at 30-50 %: it turns the story into an explainer half-way through.

**Ending**
- Do: "The only guest who never made a sound was the one the floor was built for." (the payoff, then stop.)
- Don't: "Today, the castle is a museum that millions of tourists visit every year." (epilogue after the payoff.)
- Don't: "Would you have walked across that floor?" (question ending; 0/8 top.)

## Delivery notes for our TTS (Kokoro, am_michael)

- Our posted Chess Turk v4 ran 3.11 w/s with 6 gaps >= 0.4 s (9.4 s of gaps in total); story-vasa v1 (speed 1.34)
  runs 4.00 w/s with 2 gaps >= 0.4 s (both measured the same way as the references: whisper on the rendered audio).
  The current Chess Turk script at speed 1.28 reads 3.78 w/s. Target 3.6-3.8 w/s with no gap >= 0.4 s: speed about
  1.25-1.28 with `paragraph_pause` <= 0.08, then measure the render.
- Kokoro's `captions.json` word ends abut the next word, so it shows almost no gaps. Pace from it is fine; for the
  gap checks run whisper on the rendered audio and pass that to the judge with `--timings`.
- Keep sentence breaks near 0.2-0.3 s; the references pause about as often at commas as at full stops.
- Read the mechanism and the last line a touch slower than the rest (top 8: about 0.1-0.2 w/s slower), never faster.

## How the judge maps to this spec

`python3 -m pipeline.qa.script_judge <slug>` reads `episodes/<slug>/script.md` and, when it exists,
`audio/captions.json` (or `--timings` from a whisper dump of the render). It finds the hook, setup, escalation steps,
pivot, mechanism and last line by phrase heuristics (calibrated on the 24: escalation steps within about +-1.4,
pivot sentence right in 15/24), prints the beat map so a human can correct it with `--beats`, and scores 18 measured
checks plus 7 rubric items. Scores: references top 90.6, middle 70.0, bottom 63.9 (deterministic part). Reports for
our scripts: `research/library/script_reports/`.

## Required alongside the judge: the cold-reader test (2026-11-02)

`script_judge.py` checks structure, not whether a viewer follows the story. Before voicing, every story script also
passes `pipeline/qa/cold_read.py` / `COLD_READ_PROMPT.md`: a fresh agent reads only the narration, retells who / what
/ why / twist, and flags lines it had to reread (`lost` or `slowed`), unexplained terms, logic jumps and claims that
sound wrong. The pass requires every beat retold, no `lost` line and no blocking jump. Hooks are chosen with
`research/library/HOOK_BANK.md` (rubric and blind ranking).
