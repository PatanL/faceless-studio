# What-if PLAYBOOK — viral skeleton, devices, pacing

Built 2026-11-01 ~09:20 UTC from the 12 annotated scripts in this folder (`<id>.md`, `raw/<id>.txt`, `SOURCES.md`), the R3 teardown (`research/R3/report.md`) and **controls**: 29 IFOLOGY + 4 Awaken long-form transcripts in `research/R3/transcripts/` and 22 @man_ia_c TikTok post captions in `research/R3/raw/r3_videos.json`. Machine-readable index: `INDEX.json` (each video's `beat_sequence` uses the S1–S10 / L1–L11 tags from §1). Pacing numbers come from `tools/pacing_stats.py` (output `tools/pacing_stats.json`), not from memory.

**Use rules.** Borrow structure, timing and devices only. Never borrow wording, characters, footage or audio (BRIEF rule 5). This file holds no source line longer than 6 words; everything below is an abstracted pattern with `[slots]`. Before writing, pick the 2–3 closest corpus scripts, cite them in front matter and fill a beat-alignment table (BRIEF Update 09:00). Run `scripts/originality_check.py` until PASS.

Source key (views, outlier = views ÷ channel's same-format median):

| id | short name | fmt | views | outlier |
|---|---|---|---|---|
| 7693494009494342945 | ELECTRONS (@man_ia_c) | 80 s 9:16 | 18.2M | 29.13 |
| 7693305573487562016 | OXYGEN (@man_ia_c) | 80 s | 13.4M | 21.45 |
| 7693617402180881697 | NEUTRONS (@man_ia_c) | 80 s | 5.1M | 8.16 |
| 7694025665993100576 | POPSTAR-100× (@man_ia_c) | 80 s | 4.9M | 7.84 |
| 7696143265405488416 | PI=3 (@man_ia_c) | 80 s | 3.9M | 6.24 |
| 6oZ9fdM0n50 | RESTART (Awaken) | 6:58 | 4.22M | 14.44 |
| b6jmbFcJZCY | EVERY-HUMAN (OminiAM) | 12:06 | 1.08M | 107.01 |
| DK4EOHCrVvM | WEALTH (ConChaser) | 10:47 | 1.17M | 8.68 |
| J3XahLkDEzU | LAST-HUMAN (Oddly Elsewhere) | 11:00 | 914K | 6.11 |
| _lu85gSD39k | BILLION-YEARS (OminiAM) | 13:09 | 413K | 41.02 |
| y300HjYnHPw | 10X-FASTER (IFOLOGY) | 10:19 | 868K | 8.38 |
| YznR5NmI3bc | STOP-TIME (IFOLOGY) | 10:10 | 636K | 6.15 |

---

## 0. The niche in one paragraph

A what-if wins when **one rule of reality changes**, the viewer is **placed inside it**, and a **visible tracker** (countdown, year badge, floating number, distance counter) advances toward a **promised payoff** that the hook sets up and the last 15% delivers with a **reversal**. Everything between is a **ladder**: each rung is one idea, one real number, one step bigger or closer to "you" than the last. The format is cheap to build in code because the tracker, the numbers and the diagrams are typography and flat shapes.

---

## 1. Canonical viral skeleton

### 1A. Shorts (9:16, 75–85 s, caption-led, optional light VO) — template of all five @man_ia_c hits

Seconds assume 80 s. % are medians across the 5 Shorts (range in brackets).

| # | Beat | % of runtime | Seconds (80 s) | What happens | Exemplars |
|---|---|---|---|---|---|
| S1 | **Premise card + pre-event clock** | 0–10% (6–10) | 0–8 | Title question (7–9 words), keyword in accent colour, icon. HUD counts down to the event over a calm, recognisable place. HUD subline plants scope ("every [X] has it") or a baseline reading. | all 5; cleanest ELECTRONS, PI=3 |
| S2 | **Place you** | 5–10% | 4–8 | One second-person line naming a real, famous place. Calm image, props that will fail later. | ELECTRONS, OXYGEN, NEUTRONS (PI=3 shows but doesn't name) |
| S3 | **Flip** | ~10% | 8 | Clock hits zero → hard style change (normal → wireframe/strange) + hit. HUD flips to a **return countdown** (or elapsed counter) with a slow-motion factor (~9–11×) that explains why a few seconds fill a minute. | ELECTRONS, NEUTRONS, PI=3, OXYGEN |
| S4 | **Wonder / body first** | 10–25% | 8–20 | First effect is harmless, sensory and on the viewer's own body or hands, or turned into a personal stat (your weight, your ears). The screenshot moment. | ELECTRONS (hands), NEUTRONS (weight), OXYGEN (ears) |
| S5 | **Rule, then the "but" turn** | 25–35% | 20–28 | One plain-science rule line, then a shorter line that implies the consequence without saying it, then 3–4 s with no text while the image breaks. | ELECTRONS, NEUTRONS, PI=3 |
| S6 | **Scale-outward ladder** | 35–62% | 28–50 | 3–5 rungs: smallest everyday object → street → person/crowd → city. Each caption = one stat or one consequence. Caption cadence peaks (~3 s). Ends in a white-out or full-frame interrupt. | ELECTRONS, OXYGEN, PI=3, NEUTRONS |
| S7 | **Planet/cosmic climb or race** | 55–80% | 44–64 | Wide/space view, a **live climbing number** in the HUD ("[thing] is now N [units]"), terse status lines. Optional second countdown racing the main clock. Captions thin out; the HUD carries re-hooks. | ELECTRONS, NEUTRONS (Moon race), OXYGEN (false calm) |
| S8 | **Return (master loop closes)** | 78–82% | 62–66 | Clock reaches zero, HUD shows "[X] BACK", a reassuring line, a callback stamp "[place], [N] seconds later". | ELECTRONS, NEUTRONS, PI=3, OXYGEN |
| S9 | **Twist** | 82–90% | 66–72 | The return does not fix it: it causes a second disaster, or the damage stays, or a planted by-product reacts. One caption + one HUD equivalence. | all 4 vanish/constant hits; POPSTAR uses "you are exactly where it lands" |
| S10 | **Black + bookend + real fact** | 90–100% (8–13) | 72–80 | ~1–2 s black, the title repeats exactly (seamless loop), one small-caps **true, checkable fact** tying the premise to your body or to history. Comment CTA goes in the **post caption**, not on screen. | all 5 |

Shape: hook + place ≈ 10%, event body ≈ 68–70% (median), return + twist ≈ 12.5%, outro ≈ 10%.

### 1B. Long-form (16:9, 7–13 min; sweet spot 10–12 min)

% are medians across the 7 long-form scripts. Seconds given for a 10:00 (600 s) and a 7:00 (420 s) cut.

| # | Beat | % of runtime | s @600 | s @420 | What happens | Exemplars |
|---|---|---|---|---|---|---|
| L1 | **Cold open** | 0–6% (2–7) | 0–35 | 0–25 | Ordinary second-person moment (or a present-tense true fact with a big number) → the impossible change inside the first 1–2 sentences → 2–3 sensory traces → an exception ("everyone… except you") → stakes line. Opens the master loop; the best also run a **trailer** of dated payoffs. Premise stated by ~8 s. | LAST-HUMAN, STOP-TIME, 10X-FASTER, RESTART, EVERY-HUMAN, WEALTH |
| L2 | **Title question + rules** | 6–9% (2–3% long) | 35–55 | 25–38 | Restate the title. State the one changed variable, the constraint (one-way, slow-motion, "this stays normal") and a plant: "remember this, it matters later". Optional silent title card (5–8 s). | 10X-FASTER, BILLION-YEARS, EVERY-HUMAN, RESTART |
| L3 | **Grounding: real numbers** | 9–20% (~12) | 55–120 | 38–85 | "Here's how it works." Baseline number → multiplied number → 2–3 everyday comparisons → a famous real record or study. On-screen number for every stat. | RESTART (doubling ladder), 10X-FASTER (speed ladder), STOP-TIME (science ladder) |
| L4 | **Honeymoon / wonder** | 15–28% (~9–12) | 90–170 | 63–118 | "At first…" montage of 4–6 perks rising in scale, with one early crack that foreshadows the real flaw. Or wonder beats in the new world. | 10X-FASTER, STOP-TIME, LAST-HUMAN, WEALTH (Plan A) |
| L5 | **First turn** (false resolution → "except") | at ~20–30% | ~120–180 | ~85–125 | One-word false resolution, then the problem. Then a **numbered problem ladder** (problem one/two/three) or the first collapse with a mechanism + dated precedent. | RESTART, 10X-FASTER, STOP-TIME, LAST-HUMAN |
| L6 | **Chapter ladder** | 25–60% | 150–360 | 105–250 | Chapters every 60–75 s, each opened by a stamp (DAY n / YEAR n / N YEARS / RULE n). Inside: stamp → mechanism → one big number → real precedent → one-line ironic button. One emotional chapter (animal, family). Pay the shortest hook promise first. | EVERY-HUMAN, LAST-HUMAN, BILLION-YEARS, WEALTH |
| L7 | **Midpoint re-hook / rug pull** | ~45–60% | 270–360 | 190–250 | "None of that was the real problem", or an explicit return to the cold-open mystery, or the counter-intuitive twist chapter. The planted rule from L2 pays off here or soon after. | 10X-FASTER (43%), WEALTH (57%), EVERY-HUMAN (35%), RESTART (62%) |
| L8 | **Low point → reversal** | 55–78% | 330–470 | 230–330 | Emotional floor (either/or question, moral low, loss), then a "but" turn toward hope or a solution: real-world analogue, survival cases of rising closeness to the viewer, or the hero's change of heart. | RESTART, WEALTH, STOP-TIME, 10X-FASTER |
| L9 | **Climax / master payoff** | ~78–90% | 470–540 | 330–380 | The master loop from L1 closes with the biggest number or most human detail in the video; a planted rule/number is used to win (or the stranding rule bites). | EVERY-HUMAN, BILLION-YEARS, WEALTH, 10X-FASTER |
| L10 | **Bookend + thesis** | ~88–97% | 530–580 | 370–405 | Return to the opening place/object, rapid recap of 4–5 milestones, a one-line reframe of what the video meant, or a bathos punchline. | EVERY-HUMAN, BILLION-YEARS, RESTART, LAST-HUMAN |
| L11 | **CTA** | last 2–4% | 580–600 | 405–420 | A personal pick-one/choice question that restates the premise; optional series hook (open villain, "which stop/next"). No mid-roll asks. | all 7 |

Ending stack (L9–L11) ≈ 11% median (range 6–24%; the 24% is 10X-FASTER's franchise act).

**Three long-form engines** share this skeleton but weight it differently:

| Engine | Spine | L3–L6 is… | Sources |
|---|---|---|---|
| **Timeline** ("everything X stopped now", "you travel N years") | a time ladder on a log scale with a persistent clock/year badge | chapters = time stamps (~25–75 s each) | EVERY-HUMAN, BILLION-YEARS, LAST-HUMAN |
| **Thought experiment** ("can N people/things do [huge]?") | a single number target, tested and broken | maths ladder → twist → mechanism → historical proof → reversal | RESTART |
| **Power story** ("what if you could/were [power ×N]") | rules → honeymoon → cost → corruption/rescue | character story with blueprint science inserts every 15–40 s | 10X-FASTER, STOP-TIME, WEALTH |

---

## 2. Hook formulas (abstracted)

Hook = everything up to the first beat after the premise is fully stated. Views are the sources' own.

| # | Formula (slots) | Mechanism | Sources (views) |
|---|---|---|---|
| H1 | **What if [invisible ingredient of everything] vanished for [3–5] seconds?** | tiny time window + something everyone has but never sees; the window promises a fast payoff and sets up the return twist | ELECTRONS 18.2M, OXYGEN 13.4M, NEUTRONS 5.1M (iron 2.7M, not in corpus) |
| H2 | **What if [known constant] was exactly [round value] for [N] seconds?** | a "forbidden" tiny change people half-remember (π ≈ 3.14) | PI=3 3.9M |
| H3 | **What if [ordinary person/thing] was [relatable N]× [bigger/faster]?** | relatable multiplier, answer already visible in frame 1 | POPSTAR-100× 4.9M; 10X-FASTER 868K (its 1,000× twin got 174K) |
| H4 | **Pre-event countdown on a calm, named place** (visual hook, no sentence) | the ticking clock is the hook; nothing breaks until ~8 s | all 5 Shorts |
| H5 | **You + mundane routine + impossible change inside sentence one** | in-medias-res; premise shown before it is named | STOP-TIME 636K, LAST-HUMAN 914K, RESTART 4.22M |
| H6 | **Power solves a micro-crisis before it is named**, a witness reacts, then the title question | show → name; a bystander gag gives a second voice | 10X-FASTER 868K, STOP-TIME 636K |
| H7 | **Everyone/everything [gone] — then a self-correction leaves exactly one exception** | "almost" opens a 2-second loop and narrows the story to the scarce resource | RESTART 4.22M, LAST-HUMAN 914K, STOP-TIME 636K |
| H8 | **Tiny resource vs enormous goal, with a joke** ("[2] strangers vs [8 billion]") | scale contrast states the master question | RESTART 4.22M |
| H9 | **True right-now fact with a big number → narrator performs the trigger → rules remove objections** | present-tense reality, then a gesture = time zero | EVERY-HUMAN 1.08M |
| H10 | **Trailer of dated consequences** (in hours… in [N] days… in a week…) + one undated master mystery | 3–4 promises paid in order of length; the first paid ~25 s after the hook | EVERY-HUMAN 1.08M |
| H11 | **Impossible exact number on the least likely person**, read in full, then your own modest number + a flash-forward warning | withheld reveal + personal stake + time-boxed dread | WEALTH 1.17M |
| H12 | **One-way trip + irreversible rule + promise of repeated reveals + destination tease + a mute sidekick** | the constraint is the master loop (93% of runtime); route shown in first 15 s | BILLION-YEARS 413K |

Combination rule seen in every hit: **premise + personal position + a clock or number that is already moving**. The top four by outlier score (EVERY-HUMAN 107×, BILLION-YEARS 41×, ELECTRONS 29×, OXYGEN 21×) all show a running tracker within the hook.

---

## 3. Re-hook cadence

| Layer | Shorts (80 s) | Long-form |
|---|---|---|
| Any new on-screen element (caption, HUD flip/subline, card) | every **3.8 s** median (3.2–3.8) | — |
| New caption / spoken sentence | every **5.0 s** median (gap medians 4–6 s; peak 3 s at the ladder climax; stretch to 10–15 s only while a HUD number moves) | sentence ~every 3.5 s |
| Verbal re-hook (question, "but/except" pivot, tease, ominous one-liner, character cut-in) | every caption is one | every **~30 s** median (17–33 s); pivot words **1.5/min** median (0.4–2.3) |
| Hard visual change / pattern interrupt | every 7–15 s (style flip, dissolve, white-out, black) | register switch (story ↔ diagram board) every 15–40 s |
| Chapter stamp (DAY n / YEAR n / RULE n / N YEARS / chapter label) | every 10–18 s when used (PI=3 has 4 chapter labels) | every **60–75 s** (46–87 s) |
| Tracker update (counter, badge, floating number) | every frame (HUD ticks with ms digits) | every 8–30 s (WEALTH: a dollar figure ~every 8 s; EVERY-HUMAN clock median 25 s) |
| Comedy button (one-word deadpan, gag, character line) | rare (POPSTAR's deadline gag) | every 30–60 s in story engines; drop them in the last act so sincerity lands |

Never leave **>35 s** of long-form without one of: a stamp, a question, a tease or a number change (EVERY-HUMAN's max gap). Long self-propelled stretches (a rescue with a ticking clock, a character parade) are the only exception.

---

## 4. Open loops

| Stat | Shorts | Long-form |
|---|---|---|
| Documented loops per minute | **3.75** median (3.0–4.5) | **1.16** median (0.56–1.55) |
| Master loop span | **70%** median (59–78%) of runtime (return clock), closing at 69–80% | **≥78%** in 6 of 7 (78–93%); the outlier is 10X-FASTER whose "stays normal" plant spans 39% and is then replaced by a series loop |
| Loops open at once | always ≥2 (they overlap; a new one opens before the old closes) | 2–3 at almost every point |
| Left open on purpose | 1 (pushed to the post caption question) | 1–2 (series villain, unknowable mystery) |

Patterns:
- **Master + nested shorts.** One long loop from ~5% to ~85%, with 4–6 short loops of 5–40 s inside (RESTART, EVERY-HUMAN, LAST-HUMAN).
- **Hook promises paid shortest-first.** Pay the first trailer promise within ~10% of runtime to prove promises are real; hold the biggest to ~85–90% (EVERY-HUMAN).
- **Planted rule, dismissed.** A cost or flaw is stated early and waved away with a one-word false resolution; it comes due 2–4 min later (STOP-TIME, 10X-FASTER, RESTART).
- **Tracker number.** "Keep this number in mind, it grows": advanced once per act, final value in the climax (BILLION-YEARS day length; WEALTH your number; Shorts HUD sublines).
- **Chekhov by-product.** Something created on rung 2 reacts at the return (OXYGEN hydrogen; LAST-HUMAN radio bubble).
- **Personal thread checked at every act break.** Your own number/body/home is revisited each act (WEALTH, LAST-HUMAN dog).

---

## 5. Escalation ladders

Every hit runs at least one; the strongest run two at once (scale + stakes, or time + threat).

| Ladder | Rungs (abstract) | Sources |
|---|---|---|
| **Scale outward** | your senses → your body → smallest object → street props → vehicles/buildings → city → planet → neighbour body/galaxy | all 5 Shorts |
| **Return-to-you dips** | the climb drops back to the viewer at ~50% (eyes, hands, floor) and again at the end, each drop followed by a bigger jump | PI=3, POPSTAR, NEUTRONS |
| **Closing distance** | threat N ft away → one body part → your exact floor → HERE | POPSTAR |
| **Log time** | seconds → hours → days → a week → years → centuries → millennia → millions → billion; each chapter jumps 3–10× | EVERY-HUMAN, BILLION-YEARS, LAST-HUMAN |
| **Number doubling/multiplying** | A becomes B becomes C (×4 each step) → apparent success → "except" | RESTART, WEALTH ($5 → $64.8B by 33%) |
| **Cost ladder** | cosmetic → money → biology → lethal danger | 10X-FASTER, STOP-TIME |
| **Threat ladder** | comfort → infrastructure → food → body → mind → loneliness → mortality → cosmic | LAST-HUMAN |
| **Moral slope** | harmless fix → small cheat → revenge → theft → choosing wrong when someone needs help | STOP-TIME |
| **Stakes swap** | numbers fall while human stakes rise: money → trust → family → a life | WEALTH |
| **Shrinking object, growing time** | what lasts: monuments → carvings → a rock layer → footprints → a record of a human voice | EVERY-HUMAN act 3 |
| **Hope ladder (reversal)** | survival cases of rising scale and closeness: a few birds → a colony → a small human group → your own ancestors | RESTART |

Rung rules: one idea per rung; one real number per rung; each rung bigger, faster, closer or more personal than the last; the top rung is the most human or most personal, not just the biggest.

---

## 6. Twist and payoff patterns

| # | Pattern | Sources |
|---|---|---|
| T1 | **The undo makes it worse** — the thing returns and causes a second, equal disaster, or decays, or the damage stays | ELECTRONS, NEUTRONS, PI=3 |
| T2 | **Planted by-product reacts** with the returning element; equation completes with a true, surprising result | OXYGEN |
| T3 | **One-word false resolution → "except"** at a specific step | RESTART, STOP-TIME |
| T4 | **"None of that was the real problem"** — the explicitly unchanged variable is the flaw | 10X-FASTER |
| T5 | **Rule revision** — each new rule reinterprets earlier scenes (4 revisions, 2–3.5 min apart) | WEALTH |
| T6 | **Counter-intuitive relief** backed by a real precedent (nature thrives, a species survived from a handful) | EVERY-HUMAN, RESTART |
| T7 | **You are exactly where it lands** — a location tag the viewer didn't understand is explained | POPSTAR |
| T8 | **Stranding** — the irreversible hook rule finally bites; the sidekick gag turns tender | BILLION-YEARS |
| T9 | **Two-stage reveal** — first answer, then "even that isn't the last", ending on the most human detail | EVERY-HUMAN |
| T10 | **Bathos** — cosmic event lands on the smallest domestic detail | LAST-HUMAN, POPSTAR |
| T11 | **Universe reveal** — strangers who already know, a team from other episodes, an antagonist who cancels the power | 10X-FASTER, STOP-TIME |
| T12 | **Honest speculation flag** — say aloud where agreed science ends before the speculative payoff | LAST-HUMAN, BILLION-YEARS |

---

## 7. Endings and CTAs

- **Shorts:** black 1–2 s → exact title repeat (the last frame matches the first, so the replay loops) → one small-caps real fact (a % of your body, a dated historical event) held ~6 s. No on-screen CTA. Post caption = premise retold in 4–8 escalating sentences + a comment prompt: *which one next / which would break first near you / would you have held on*. All 5 hits.
- **Long-form ending stack:** master payoff → bookend to the opening place or object → recap of 4–5 milestones (icon timeline or thumbnail grid) → one-line thesis or moral → **personal choice question** that restates the premise (who would you pick, which stop, which one thing survives, binary dilemma) → optional series hook. Subscribe asks are rare (only EVERY-HUMAN, framed as an identity compliment); no corpus video asks mid-roll.
- The CTA question is always answerable by everyone (no wrong answers) and uses options the video already showed (BILLION-YEARS: the 10 stops).

## 8. Series / part-2 mechanics

- **Swap the variable, keep the template.** @man_ia_c's three biggest hits (electrons, oxygen, neutrons) came within 2 days of each other on an identical template; the comment CTA harvests the next variable.
- **Fatigue is real.** Same-template follow-ups decay when the premise is a near-repeat or less fundamental: hydrogen 0.67×, "lost a proton" 0.24× (after "gained a proton" 1.92×). Pop-star sequel (10 billion×) 3.36× vs the original's 7.84× (~43%).
- **Long-form "Part 2/3" halves each time:** IFOLOGY Zombie 93K → 47K → 40K; Awaken Last Guy → Last Girl 401K → 184K. Make **standalone episodes** that share a universe instead (IFOLOGY's team crossovers as the cliffhanger act; STOP-TIME, 10X-FASTER), and leave exactly one loop open (a villain, a "who else moves?") for the next episode.
- Never put "Part 2" in a title. Put the shared element (HUD design, sidekick, team, recurring home set) in the video instead.

---

## 9. Pacing stats (measured)

From `tools/pacing_stats.json`. Sentences split on . ? ! in auto-subs; "second person" = sentences containing you/your/you're/yourself; numbers = digit tokens + number words (two…trillion, half, percent).

### Long-form (7 corpus scripts)

| Metric | Median | Range | Notes |
|---|---|---|---|
| Words per minute | **154** | 134–186 | explainer-led (RESTART, EVERY-HUMAN, LAST-HUMAN, BILLION-YEARS) 134–154; story-led (WEALTH, STOP-TIME, 10X-FASTER) 165–186 |
| Total words | 1,783 | 934–2,029 | for 7–13 min |
| Cold-open hook length | **87 words / 34 s** | 44–119 words, 13–49 s | premise stated by **8 s** median (4–13 s) |
| Sentence length (mean words) | **9.0** | 7.2–11.6 | median sentence 8 words |
| Punch lines (≤3-word sentences) | **14.7%** | 8–23% | |
| % sentences in second person | **33%** | 5–59% | story engines 48–59%; EVERY-HUMAN is 5% ("I" narrator + "right now" facts) |
| "you" words per 100 words | 3.8 | 0.7–9.2 | |
| Numbers per minute | **4.7** | 1.3–8.2 | RESTART and WEALTH ~8/min; STOP-TIME 1.3 is the floor |
| Questions per minute | 0.66 | 0–1.6 | auto-subs drop some "?" |
| Pivot words (but/except/until/here's/problem…) per min | **1.5** | 0.4–2.3 | |
| Open loops per minute | **1.16** | 0.56–1.55 | |
| Verbal re-hook interval | **~30 s** | 17–33 s | |
| Chapter stamp interval | 60–75 s | 46–87 s | |

### Shorts (5 corpus scripts, 80 s each, caption-only originals)

| Metric | Median | Range | Notes |
|---|---|---|---|
| Caption words per minute | **56** | 43–65 | ~11 captions; TTS read of captions should stay ~60–70 wpm with the same holds |
| All on-screen text per minute (title, HUD, end card) | 115 | 103–131 | |
| Title (hook) length | **7 words**, held **5–8 s** | 7–9 words | event lands at 8 s (10%) in 4/5 |
| Captions per video | 11 | 11–13 | |
| Caption length (mean words) | **6.7** | 5.3–7.3; max 7–10 | one claim per caption, no subordinate clauses |
| Caption gap | **5.0 s** median | 4.0–6.0 (means 4.7–6.4) | |
| New on-screen element every | 3.8 s | 3.2–3.8 s | |
| Captions in second person | **18%** (= 1–2 lines) | 7–18% | one "you are in [place]" line + one body line; PI=3 has exactly one "your" line at 51% |
| Numbers per minute (all text) | **14** | 7–18 | most live in the HUD, not the captions (0–5 numeric captions) |
| Open loops per minute | **3.75** | 3.0–4.5 | |

---

## 10. Outliers vs ordinary (what the top scripts do that weaker ones don't)

### 10A. Long-form, within one channel (IFOLOGY, n = 29, same style/voice/team)

Spearman ρ between outlier score and each metric (controls in `research/R3/transcripts/`):

| Metric | ρ | Top 10 (≥2×) median | Bottom 10 (<0.8×) median |
|---|---|---|---|
| Words per minute | **+0.79** | 184 | 170 |
| Pivot words per minute | **+0.73** | 2.0 | 1.1 |
| "you" words per 100 | **+0.73** | 8.4 | 4.6 |
| % second-person sentences | **+0.70** | 51% | 31% |
| "you" words in first 30 s | **+0.57** | 12 | 7 |
| Punch-line share | −0.43 | 15.8% | 17.6% |
| Duration | −0.33 | 701 s | 999 s |
| Numbers per minute | −0.29 | 3.0 | 4.0 |

Reading: within a story channel, **density of "you", turns and pace** separates winners from the rest; longer runtimes and more one-liner jokes don't help. Topic is the biggest confound: classic universal powers and N× multipliers (~174–200K median) beat places/scenarios (~42K) and IP/celebrity premises (~15K) (R3). Recency also biases older uploads up.

### 10B. Same style, opposite results (Awaken)

RESTART (14.4×) and *Could 8 Billion People Live in ONE City?* (0.08×) share the flat-2D look. The hit has **two characters with a ticking problem**, a **false resolution then "except"**, 8.2 numbers/min and 0.57 questions/min. The flop asks ~2 questions/min about abstract "humanity" with only 9% second person. **Questions without a person at stake don't hook.** The 3D *Last Guy* (1.37×) opens with the premise but no tracker and no real-number ladder.

### 10C. Same template, opposite results (@man_ia_c TikTok, post captions)

| Hits (4–29×) | Weak in the same template (0.24–1×) |
|---|---|
| The changed thing is an **invisible ingredient** of everything (electrons, oxygen, neutrons, iron) or a half-remembered constant (π) | Disasters with no rule change (tsunami 0.97×, meteor 0.79×, wave 0.55×, earthquakes 0.57×) |
| **"You are in [named place]"** + a **body-first** effect | Abstract, no body: Earth left the universe 0.69× |
| A **tight time window** + a **return twist** | Familiar premises: Earth stops spinning 0.46×, gravity off 0.86× |
| One rule → a chain of calculated, exact numbers | Near-repeats: lost a proton 0.24× after gained a proton |
| A true fact at the end | A meta "stay until the end" ask instead of a twist (hydrogen 0.67×) |
| Like rate 4.8–11.5% | Like rate 0.9–4.5% (the weak ones listed) |

### 10D. What the very top share across channels

The four highest outlier scores (EVERY-HUMAN 107×, BILLION-YEARS 41×, ELECTRONS 29×, OXYGEN 21×) all have: (1) a **running tracker** on screen from the hook to the end (clock, year badge, return countdown); (2) a **master loop held to ≥85%** (in Shorts, the return clock spans ~70% and closes at ~80%); (3) a **ladder on a log or outward scale**, so the viewer can feel how many rungs are left; (4) a **payoff that lands on the viewer** (your body, your house, a human trace); (5) **real, checkable numbers** plus at least one real dated precedent. Second person is not required (EVERY-HUMAN is 5%); **the viewer's position is** (here, right now, your house).

---

## 11. Device catalog (approximate frequency: regex-tagged beat/device cells across the 1,321 annotated lines)

| Device family | Tagged lines | Use it for |
|---|---|---|
| Number / stat / counter / ratio | 259 | every rung; on screen as a chip, pill or HUD number |
| Open loop / tease / plant / cliffhanger | 157 | see §4 |
| Ladder / list / rule of three / anaphora | 99 | rapid montages, recaps, "year N, [build]" lines |
| Humour / gag / bathos | 86 | comedy button every 30–60 s in story engines |
| Callback / bookend | 69 | 3+ long plants paid off; bookend location in last 90 s |
| Twist / reversal / false resolution | 67 | §6 |
| Second-person placement | 67 | sentence one; body beats; final question |
| Analogy / comparison | 58 | one everyday analogy per chapter/stop (spare tire, blink) |
| One-word / deadpan punch line | 55 | end of sub-beats; false resolutions |
| Rhetorical question | 48 | micro re-hook every ~30 s |
| Signpost / pivot ("but", "except", "here's why") | 40 | 1.5/min |
| Character / second voice | 39 | voices the viewer's reaction; every 30–60 s in stories |
| Authority / study / dated precedent | 32 | one real dated case per chapter; one per Short (end card) |
| Pattern interrupt (silence, white-out, black) | 28 | before the scale jump; before the twist |
| Sensory detail | 25 | cold open traces; arrival at each stop |

---

## 12. Writer checklist (a script must satisfy all that apply)

**Both formats**
- [ ] Premise changes exactly **one** rule of reality, universal (no IP, no real celebrity, no disaster-only premise).
- [ ] Front matter `references:` lists 2–3 corpus ids with url, views, outlier_score; a **beat-alignment table** maps each of our beats → reference beat + timestamp + device borrowed.
- [ ] A **tracker** (countdown, elapsed counter, year badge, floating number, distance) is on screen from the hook to the payoff.
- [ ] Master loop opens in the hook and closes at ~70–80% (Shorts) / ≥80% (long-form) of runtime.
- [ ] At least one **ladder** where each rung is bigger, faster, closer or more personal; one idea per rung.
- [ ] Every stat is real, sourced in a fact file, and shown as an on-screen number. At least one **real dated precedent**.
- [ ] A **reversal** in the last 20% (T1–T12), built from something planted earlier.
- [ ] Ending calls back the opening place or object.
- [ ] Final ask is a no-wrong-answer personal choice tied to the premise.
- [ ] `python3 scripts/originality_check.py <script.md> research/corpus research/library/transcripts` prints PASS.

**Shorts (75–85 s)**
- [ ] Title question 7–9 words, keyword highlighted, held 5–8 s over a pre-event countdown.
- [ ] Event at ~8 s (10%) with a style flip and a slow-motion factor that makes the clock add up.
- [ ] One "you are in [named real place]" line and one body-first line before the 25% mark.
- [ ] 10–13 captions, ≤8 words each (mean ~6–7), new caption every 4–6 s, something new every ~4 s.
- [ ] Rule line → shorter implication line → 3–4 s textless break → scale jump.
- [ ] White-out or full-frame interrupt near the midpoint.
- [ ] Return at ~80%, twist at ~85%, black + exact title repeat + one true fact in the last 10%.
- [ ] Comment question in the post caption, not on screen. Caption-read VO (if any) ~60–70 wpm.

**Long-form (7–13 min)**
- [ ] Cold open ≤50 s / ≤120 words (target ~35 s / ~90), premise stated by ~10 s, impossible change inside the first two sentences, no channel intro.
- [ ] Rules stated with one explicit "remember this" plant that pays off at 40–60%.
- [ ] 145–155 wpm for explainer/timeline engines; 175–185 for power stories. Mean sentence 8–9 words, ~15% punch lines.
- [ ] Second person in ≥45% of sentences for power stories (≥25% otherwise), and in the first sentence.
- [ ] Re-hook every ≤30 s (no gap >35 s); chapter stamp every 60–75 s; ~1 new loop per minute; ≥1.5 pivots/min.
- [ ] ≥4 numbers per minute on average.
- [ ] First turn by ~25%; midpoint re-hook at 45–60%; climax ~80%; ending stack ≤12% of runtime.
- [ ] 3+ plants longer than 3 min paid off; one loop optionally left open for the series.
- [ ] Each beat type has its own visual mode (story set / diagram board / chapter stamp).

---

## 13. Study these three first

1. **ELECTRONS — 7693494009494342945** (18.2M, 29.13×). The cleanest Shorts template: countdown → place → flip → wonder → rule → outward ladder → white-out → cosmic climb → return → twist → bookend fact. Every beat maps to a code component (HUD, wireframe line art, particles, white-out, serif cards). Read `7693494009494342945.md` §3.
2. **EVERY-HUMAN — b6jmbFcJZCY** (1.08M, 107×). The highest outlier and the best code-only long-form: a right-now hook, a trailer of dated promises paid shortest-first, a persistent time-since HUD with a scrubber, log-scale chapters with ironic buttons, a two-stage master reveal, and a recap + thesis ending. Read `b6jmbFcJZCY.md` (Structure summary + Transferable skeleton).
3. **RESTART — 6oZ9fdM0n50** (4.22M, 14.44×). The biggest long-form view count and ~80% flat 2D: a second-person cold open with a self-correction, a doubling ladder to a one-word false resolution, then mechanism → historical proof → escalation to an emotional floor → hope ladder → honest verdict with a hard number → choice CTA. Read `6oZ9fdM0n50.md`.

Next if you are writing a power story: **10X-FASTER — y300HjYnHPw** (rules + plant → honeymoon → numbered problems → rug pull → real analogue → rescue → universe hook).
