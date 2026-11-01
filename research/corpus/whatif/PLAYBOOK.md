# What-if PLAYBOOK — viral skeleton, devices, pacing

Built 2026-11-01 ~09:20 UTC from the 12 annotated scripts in this folder; **revised ~12:50 UTC with the 13-script expansion (25 annotated scripts, 10 channels)**. The changes are summarised in §14. Sources: `<id>.md`, `raw/<id>.txt`, `SOURCES.md`, the R3 teardown (`research/R3/report.md`) and **controls**: 29 IFOLOGY + 4 Awaken long-form transcripts in `research/R3/transcripts/` and 22 @man_ia_c TikTok post captions in `research/R3/raw/r3_videos.json`. Machine-readable index: `INDEX.json` (each video's `beat_sequence` uses the S1–S10 / L1–L11 tags from §1). Pacing numbers come from `tools/pacing_stats.py` (output `tools/pacing_stats.json`), not from memory.

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
| *Expansion (12:08 UTC)* | | | | |
| 2d6Ciu3INeA | GROW-1CM (What If, narrated Short) | 2:52 9:16 | 3.32M | 69.27 |
| VZ27faCr8UU | BLACK-HOLE-NS (What If, narrated Short) | 2:32 9:16 | 435K | 9.06 |
| AV1zVKuEtFc | SUN-GONE (SolarBalls, character skit Short) | 1:21 9:16 | 7.77M | 5.97 |
| 7693888660256722208 | IRON (@man_ia_c) | 80 s 9:16 | 2.7M | 4.32 |
| YayPaipjNAM | SHRINK (What If Animations, caption-only long) | 6:45 | 873K | 622.86 |
| 8fADp43wJwU | LAST-LIGHT (xkcd's What If?) | 5:04 | 10.4M | 4.34 |
| Q9F0z4CR0gM | ASTEROIDS (What If) | 23:37 | 3.10M | 5.38 |
| n1CYFTKR_B0 | NO-CLOTHES (OminiAM) | 10:58 | 297K | 30.27 |
| DgftZCQe8sI | LAST-HUMAN-2 (OminiAM) | 12:40 | 243K | 24.79 |
| K_56-ZqYviY | UNDERWATER (Oddly Elsewhere) | 10:02 | 709K | 4.76 |
| eiBR6wlwPfA | WOMB (WatchData, text-card timeline) | 3:02 | 2.25M | 11.19 |
| rzoq6AOgudA | NOCTURNAL (If Humans, wordless sketch) | 1:30 16:9 | 2.12M | 16.04 |
| DOEQgRAFeI0 | HIBERNATE (If Humans, story sketch) | 4:43 | 1.67M | 12.64 |

Outlier scores are channel-relative. The big established channels (What If 8.99M subs, SolarBalls, xkcd, WatchData) have large medians, so their 4–10× means far more reach than 25–600× on a weeks-old channel (OminiAM, What If Animations).

---

## 0. The niche in one paragraph

A what-if wins when **one rule of reality changes**, the viewer is **placed inside it**, and a **visible tracker** (countdown, year badge, floating number, distance counter) advances toward a **promised payoff** that the hook sets up and the last 15% delivers with a **reversal**. Everything between is a **ladder**: each rung is one idea, one real number, one step bigger or closer to "you" than the last. The format is cheap to build in code because the tracker, the numbers and the diagrams are typography and flat shapes.

---

## 1. Canonical viral skeleton

### 1A. Shorts (9:16, 75–85 s, caption-led, optional light VO) — template of all six @man_ia_c hits

Seconds assume 80 s. % are medians across the 5 original Shorts (range in brackets). IRON (6th) fits every row, with two shifts: the return lands earlier (68%), and S9 becomes a **delayed consequence** with its own third clock (70–90%). The other Short variants are in §1A+.

| # | Beat | % of runtime | Seconds (80 s) | What happens | Exemplars |
|---|---|---|---|---|---|
| S1 | **Premise card + pre-event clock** | 0–10% (6–10) | 0–8 | Title question (7–9 words), keyword in accent colour, icon. HUD counts down to the event over a calm, recognisable place. HUD subline plants scope ("every [X] has it") or a baseline reading. | all 5; cleanest ELECTRONS, PI=3 |
| S2 | **Place you** | 5–10% | 4–8 | One second-person line naming a real, famous place. Calm image, props that will fail later. | ELECTRONS, OXYGEN, NEUTRONS (PI=3 shows but doesn't name) |
| S3 | **Flip** | ~10% | 8 | Clock hits zero → hard style change (normal → wireframe/strange) + hit. HUD flips to a **return countdown** (or elapsed counter) with a slow-motion factor (~9–11×) that explains why a few seconds fill a minute. | ELECTRONS, NEUTRONS, PI=3, OXYGEN |
| S4 | **Wonder / body first** | 10–25% | 8–20 | First effect is harmless, sensory and on the viewer's own body or hands, or turned into a personal stat (your weight, your ears). The screenshot moment. | ELECTRONS (hands), NEUTRONS (weight), OXYGEN (ears) |
| S5 | **Rule, then the "but" turn** | 25–35% | 20–28 | One plain-science rule line, then a shorter line that implies the consequence without saying it, then 3–4 s with no text while the image breaks. | ELECTRONS, NEUTRONS, PI=3 |
| S6 | **Scale-outward ladder** | 35–62% | 28–50 | 3–5 rungs: smallest everyday object → street → person/crowd → city. Each caption = one stat or one consequence. Caption cadence peaks (~3 s). Ends in a white-out or full-frame interrupt. | ELECTRONS, OXYGEN, PI=3, NEUTRONS |
| S7 | **Planet/cosmic climb or race** | 55–80% | 44–64 | Wide/space view, a **live climbing number** in the HUD ("[thing] is now N [units]"), terse status lines. Optional second countdown racing the main clock. Captions thin out; the HUD carries re-hooks. | ELECTRONS, NEUTRONS (Moon race), OXYGEN (false calm) |
| S8 | **Return (master loop closes)** | 78–82% (IRON 68%) | 62–66 | Clock reaches zero, HUD shows "[X] BACK", a reassuring line, a callback stamp "[place], [N] seconds later". | ELECTRONS, NEUTRONS, PI=3, OXYGEN, IRON |
| S9 | **Twist** | 82–90% (IRON 70–90%) | 66–72 | The return does not fix it: it causes a second disaster, or the damage stays, or a planted by-product reacts. One caption + one HUD equivalence. Variant: cut back to the opening shot as false calm, one small permanent change, then a **third countdown** that time-skips to a delayed hit (IRON). | all 5 vanish/constant hits; POPSTAR uses "you are exactly where it lands" |
| S10 | **Black + bookend + real fact** | 90–100% (8–13) | 72–80 | ~1–2 s black, the title repeats exactly (seamless loop), one small-caps **true, checkable fact** tying the premise to your body or to history. Comment CTA goes in the **post caption**, not on screen. | all 5 |

Shape: hook + place ≈ 10%, event body ≈ 68–70% (median; IRON 58%), return + twist ≈ 12.5% (IRON 22%, because its twist has its own clock), outro ≈ 10%.

### 1A+. Other Short variants (from the expansion)

| Variant | Length / pace | Spine | Beat timing | Sources |
|---|---|---|---|---|
| **Narrated size/time ladder** | 2:30–2:55, ~150–165 wpm, ~420 words, one narrator, "you" in 74–88% of sentences | premise line (12 words, ≤4 s) → two checkable maths rungs → honest real-science off-ramp that sounds like an ending (~8–20%) → "ignore that" pivot that opens the master loop → scale acts of ~11–17% each → biggest real number → sting cut mid-sentence so the replay finishes it | off-ramp by 20%; space/threshold crossing at ~50%; "keeps going" re-hooks at ~50% and ~70%; master loop 74–78% | GROW-1CM, BLACK-HOLE-NS |
| **Character skit** | ~80 s, ~160 wpm dialogue, ~210 words, 4–5 personified objects | idle question + underselling answer → the subject overhears → real fact as a threat → third-character explainer over 2–3 s line-art diagrams → bluff → calm "until" sting with a real far-future version → silent end card | first turn 14%; threat peak 32%; false resolution 75%; sting 88% | SUN-GONE |
| **Wordless gag montage** (16:9, 90 s) | ~27 wpm; a cut every ~3.5 s; 90% of the words in the last 18% | brand sting → premise shown by a time-lapse → 5 matched-frame inversions (same place, two lightings) → one short dialogue scene that flips idioms and pays a plant from 0:10 | first inversion 20%; payoff scene 76–98% | NOCTURNAL |

### 1B. Long-form (16:9, 5–24 min; sweet spot still 10–13 min)

% were measured across the original 7 long-form scripts. The 5 new narrated long-forms (LAST-LIGHT, ASTEROIDS, NO-CLOTHES, LAST-HUMAN-2, UNDERWATER) fit the same rows. They move three timings: the **first turn comes earlier** (13–22%), the **midpoint re-hook spreads later** (57–72%), and the **master payoff lands later** (87–95%). The bands below include them. Seconds are given for a 10:00 (600 s) and a 7:00 (420 s) cut.

| # | Beat | % of runtime | s @600 | s @420 | What happens | Exemplars |
|---|---|---|---|---|---|---|
| L1 | **Cold open** | 0–6% (2–7) | 0–35 | 0–25 | Ordinary second-person moment (or a present-tense true fact with a big number) → the impossible change inside the first 1–2 sentences → 2–3 sensory traces → an exception ("everyone… except you") → stakes line. Opens the master loop; the best also run a **trailer** of dated payoffs. Premise stated by ~8 s. | LAST-HUMAN, STOP-TIME, 10X-FASTER, RESTART, EVERY-HUMAN, WEALTH, LAST-HUMAN-2, NO-CLOTHES. Variants: a riddle the viewer half-solves, premise never stated (UNDERWATER); a named reader's question read in full (LAST-LIGHT); a famous real benchmark before the premise (ASTEROIDS, premise at 34 s) |
| L2 | **Title question + rules** | 6–9% (2–3% long) | 35–55 | 25–38 | Restate the title. State the one changed variable, the constraint (one-way, slow-motion, "this stays normal") and a plant: "remember this, it matters later". Optional silent title card (5–8 s). | 10X-FASTER, BILLION-YEARS, EVERY-HUMAN, RESTART |
| L3 | **Grounding: real numbers** | 9–20% (~12) | 55–120 | 38–85 | "Here's how it works." Baseline number → multiplied number → 2–3 everyday comparisons → a famous real record or study. On-screen number for every stat. | RESTART (doubling ladder), 10X-FASTER (speed ladder), STOP-TIME (science ladder) |
| L4 | **Honeymoon / wonder** | 15–28% (~9–12) | 90–170 | 63–118 | "At first…" montage of 4–6 perks rising in scale, with one early crack that foreshadows the real flaw. Or wonder beats in the new world. | 10X-FASTER, STOP-TIME, LAST-HUMAN, WEALTH (Plan A) |
| L5 | **First turn** (false resolution → "except") | at ~13–30% (new five: 13–22%) | ~80–180 | ~55–125 | One-word false resolution, then the problem. Then a **numbered problem ladder** (problem one/two/three) or the first collapse with a mechanism + dated precedent. | RESTART, 10X-FASTER, STOP-TIME, LAST-HUMAN, LAST-LIGHT (nuclear hope crushed at 18%), LAST-HUMAN-2 (grid at 10%), UNDERWATER (inciting incident 17%) |
| L6 | **Chapter ladder** | 25–60% | 150–360 | 105–250 | Chapters every 60–75 s, each opened by a stamp (DAY n / YEAR n / N YEARS / RULE n). Inside: stamp → mechanism → one big number → real precedent → one-line ironic button. One emotional chapter (animal, family). Pay the shortest hook promise first. Chapter length now 38–75 s (median ~50–55 s). | EVERY-HUMAN, LAST-HUMAN, BILLION-YEARS, WEALTH, LAST-HUMAN-2 (13 stamps, HOUR 1 → YEAR 57), NO-CLOTHES (10 chapters, each ending on a one-line button) |
| L7 | **Midpoint re-hook / rug pull** | ~43–72% (median ~60%) | 270–360 | 190–250 | "None of that was the real problem", or an explicit return to the cold-open mystery, or the counter-intuitive twist chapter. The planted rule from L2 pays off here or soon after. | 10X-FASTER (43%), WEALTH (57%), EVERY-HUMAN (35%), RESTART (62%), UNDERWATER drowned town (59%), LAST-LIGHT front-runner (57%) then wildcard (71%), NO-CLOTHES cloth → computers (63–70%), ASTEROIDS cold-open loop closes (67%) |
| L8 | **Low point → reversal** | 55–78% | 330–470 | 230–330 | Emotional floor (either/or question, moral low, loss), then a "but" turn toward hope or a solution: real-world analogue, survival cases of rising closeness to the viewer, or the hero's change of heart. | RESTART, WEALTH, STOP-TIME, 10X-FASTER |
| L9 | **Climax / master payoff** | ~78–95% (new five: 87–95%) | 470–540 | 330–380 | The master loop from L1 closes with the biggest number or most human detail in the video; a planted rule/number is used to win (or the stranding rule bites). | EVERY-HUMAN, BILLION-YEARS, WEALTH, 10X-FASTER, UNDERWATER (two-word reveal at 87%), LAST-HUMAN-2 (your death at 89%), LAST-LIGHT (answer at 94%) |
| L10 | **Bookend + thesis** | ~88–97% | 530–580 | 370–405 | Return to the opening place/object, rapid recap of 4–5 milestones, a one-line reframe of what the video meant, or a bathos punchline. | EVERY-HUMAN, BILLION-YEARS, RESTART, LAST-HUMAN |
| L11 | **CTA** | last 2–4% | 580–600 | 405–420 | A personal pick-one/choice question that restates the premise; optional series hook (open villain, "which stop/next"). No mid-roll asks. | all 7 |

Ending stack (L9–L11) ≈ 11% median (range 6–24%; the 24% is 10X-FASTER's franchise act). Measured after the master payoff only, the new five run 4–16% (median ~10%): it held.

**Long-form engines** share this skeleton but weight it differently (the first three are from the original sample, the rest from the expansion):

| Engine | Spine | L3–L6 is… | Sources |
|---|---|---|---|
| **Timeline** ("everything X stopped now", "you travel N years") | a time ladder on a log scale with a persistent clock/year badge | chapters = time stamps (~25–75 s each) | EVERY-HUMAN, BILLION-YEARS, LAST-HUMAN |
| **Thought experiment** ("can N people/things do [huge]?") | a single number target, tested and broken | maths ladder → twist → mechanism → historical proof → reversal | RESTART |
| **Power story** ("what if you could/were [power ×N]") | rules → honeymoon → cost → corruption/rescue | character story with blueprint science inserts every 15–40 s | 10X-FASTER, STOP-TIME, WEALTH |
| **Candidate chase** ("when would the last [X]…?") | one exact question, candidates eliminated in order of lifespan | rapid rungs of 9–44 s, each "it dies of [cause] after [time]", then a hedged front-runner, a false ending and a wildcard that wins | LAST-LIGHT |
| **Stack the extremes** ("every [X] at once") | 5 named cases, ordered by deadliness, combined at the end | repeated card (identity → size → history/odds → today → cascade → verdict), each card adds one new mechanism, "you know the drill" by card 5 | ASTEROIDS |
| **Alt history** ("what if humans never [invented X]") | real science first (~20%), then the fork, then a ladder of what is lost | chapters of 38–75 s on a time spine, ending in thesis + callback montage | NO-CLOTHES |
| **Worldbuilding story** (premise never said) | a hero's journey inside the changed world | dramatic-irony decodes every ~45 s (things from our world described by someone who doesn't know them), science folded into the story | UNDERWATER |
| **Caption-only sim, long** | the @man_ia_c HUD + serif captions at 16:9 | one caption every ~7.7 s, a HUD comparison rung every ~22 s, black/white cuts between worlds, two fake deaths in the first 44% | SHRINK |
| **Scrolling card timeline** (no narration) | fixed card rate, accelerating clock | ~50 cards at ~3.5 s; time unit jumps (hours → days → weeks → months → years → century); genre turn at ~52% | WOMB |
| **Story sketch** (no narrator) | a three-act fable inside the premise | world rules by montage, plant, honeymoon montage, single-gesture turn at ~67%, countdown time cards, word-for-word bookend | HIBERNATE |

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
| H13 | **Here's what would happen if you [tiny constant rate]** + two checkable ×60 rungs in 9 s | the premise is the first sentence; the maths proves the ladder is real and starts it moving | GROW-1CM 3.32M (69×), BLACK-HOLE-NS 435K |
| H14 | **Flash-forward image + "you can't stop [verb]ing" + a counter already moving** | shows the payoff from ~20% in, before the title card | SHRINK 873K (623×) |
| H15 | **Named reader's question read out in full**, then "start with the obvious" | an outside voice owns the question; the title is answered exactly at the end | LAST-LIGHT 10.4M |
| H16 | **A riddle about our world told from inside the changed one** (premise never stated) | the viewer half-solves it in 5 s and stays to be proved right | UNDERWATER 709K |
| H17 | **Imagine waking up tomorrow without [X]** → two-step rule-out (not stolen, never invented) → obvious joke dismissed → 3 teases of rising surprise | three specific loops (a place, your phone, a thesis) paid shortest-first | NO-CLOTHES 297K (30×) |
| H18 | **Micro-absences** (no notifications, silent street, steaming coffee) → premise implied from word one, stated at ~29 s → 3-question stack → format promise ("hour by hour") | a format promise turns the chapter stamps into kept promises | LAST-HUMAN-2 243K (25×) |
| H19 | **Famous real benchmark first** (a known catastrophe, then "if it hit today") → premise → fake spoiler | borrows a known event's dread; premise late (34 s) but the benchmark is a loop closed at 67% | ASTEROIDS 3.10M |
| H20 | **Idle question asked casually, undersold, overheard by the subject** | the hook builds a character with a grudge in 11 s instead of selling a fact | SUN-GONE 7.77M |
| H21 | **No spoken hook: title + brand sting, premise shown** (time-lapse, montage, countdown cards) | works only with a title that already hooks and a returning audience | NOCTURNAL 2.12M, HIBERNATE 1.67M, WOMB 2.25M |

Combination rule seen in every hit: **premise + personal position + a clock or number that is already moving**. The top four by outlier score (EVERY-HUMAN 107×, BILLION-YEARS 41×, ELECTRONS 29×, OXYGEN 21×) all show a running tracker within the hook. With the expansion it still holds for the two new top scores (SHRINK 623×: size counter on frame 1; GROW-1CM 69×: a time stamp every ~10 s). The exceptions are the sketch channels (If Humans, SolarBalls), where a character or picture gag replaces the tracker. Long-form hook length over all 12 narrated long-forms: **median ~88 words / ~34 s** (33–123 words, 10–49 s); unchanged from the first sample.

---

## 3. Re-hook cadence

| Layer | Shorts (80 s, caption sims) | Narrated Shorts (2.5–3 min) | Long-form |
|---|---|---|---|
| Any new on-screen element (caption, HUD flip/subline, card) | every **3.7 s** median (3.0–3.8) | new fact/image every ~4 s | caption-only long: caption every ~7.7 s; card timeline: card every 3.5 s |
| New caption / spoken sentence | every **4.75 s** median (gap medians 4–6 s; peak 3 s at the ladder climax; stretch to 10–15 s only while a HUD number moves) | sentence every ~4 s | sentence ~every 3.5 s |
| Verbal re-hook (question, "but/except" pivot, tease, ominous one-liner, character cut-in) | every caption is one | time/scale milestone every ~10 s; turn phrase every 15–40 s; pivots **~3/min** (1.4–3.6) | every **~30 s** median (17–43 s); pivot words **1.5/min** median (0.4–2.4) |
| Hard visual change / pattern interrupt | every 7–15 s (style flip, dissolve, white-out, black) | — | register switch (story ↔ diagram board) every 15–40 s; sketches cut every 3.5–10 s |
| Chapter stamp (DAY n / YEAR n / RULE n / N YEARS / chapter label) | every 10–18 s when used (PI=3 has 4 chapter labels) | one per scale domain, ~20–30 s | every **~50–60 s** median (25–112 s; ASTEROIDS' case cards every 170–300 s) |
| Tracker update (counter, badge, floating number) | every frame (HUD ticks with ms digits) | spoken time stamp every ~10 s (GROW-1CM) or none (BLACK-HOLE-NS) | every 8–30 s (WEALTH: a dollar figure ~every 8 s; EVERY-HUMAN clock median 25 s; SHRINK comparison subline ~22 s) |
| Comedy button (one-word deadpan, gag, character line) | rare (POPSTAR's deadline gag) | one deadpan line right after the darkest beat | every 30–60 s in story engines; drop them in the last act so sincerity lands (ASTEROIDS keeps them to the end; it is a documentary voice, not a story) |

Never leave **>35 s** of long-form without one of: a stamp, a question, a tease or a number change (EVERY-HUMAN's max gap). Long self-propelled stretches (a rescue with a ticking clock, a character parade) are the only exception. The expansion adds two more exceptions: a stretch filled by **back-to-back analogies** (BLACK-HOLE-NS, 28 s) and a caption-only stretch held by a **continuously moving counter** (SHRINK, max 58 s between macro re-hooks).

---

## 4. Open loops

| Stat | Shorts | Long-form |
|---|---|---|
| Documented loops per minute | **3.75** median (3.0–4.5); IRON 6.0 (8 loops) | **~1.2–1.3** median over 12 (0.25–2.2): original 7 median 1.16, new five 0.25 (ASTEROIDS), 1.3, 1.5, 1.5, 2.2 (LAST-LIGHT) |
| Master loop span | **70%** median (58–78%) of runtime (return clock), closing at 68–80%; narrated Shorts 74–78%, skit 62% | **≥78%** in 11 of 12 (78–95%); the new five are all 85–95%. The outlier is still 10X-FASTER, whose "stays normal" plant spans 39% and is then replaced by a series loop |
| Loops open at once | always ≥2 (they overlap; a new one opens before the old closes) | 2–3 at almost every point |
| Left open on purpose | 1 (pushed to the post caption question) | 1–2 (series villain, unknowable mystery) |

Patterns:
- **Master + nested shorts.** One long loop from ~5% to ~85%, with 4–6 short loops of 5–40 s inside (RESTART, EVERY-HUMAN, LAST-HUMAN).
- **Hook promises paid shortest-first.** Pay the first trailer promise within ~10% of runtime to prove promises are real; hold the biggest to ~85–90% (EVERY-HUMAN).
- **Planted rule, dismissed.** A cost or flaw is stated early and waved away with a one-word false resolution; it comes due 2–4 min later (STOP-TIME, 10X-FASTER, RESTART).
- **Tracker number.** "Keep this number in mind, it grows": advanced once per act, final value in the climax (BILLION-YEARS day length; WEALTH your number; Shorts HUD sublines).
- **Chekhov by-product.** Something created on rung 2 reacts at the return (OXYGEN hydrogen; LAST-HUMAN radio bubble).
- **Personal thread checked at every act break.** Your own number/body/home is revisited each act (WEALTH, LAST-HUMAN dog, LAST-HUMAN-2 dog, UNDERWATER grandfather's chart).
- **Format promise as a loop.** "Hour by hour, year by year" or "when each one might turn off" makes every chapter stamp a kept promise (LAST-HUMAN-2, LAST-LIGHT).
- **Plants that close 4.5–6.5 min later**, layered under 2–10 s micro-teases at chapter seams, so 3–4 loops are open at almost every point (LAST-HUMAN-2, UNDERWATER).
- **The eliminated candidate returns.** A thing ruled out early comes back in a new form as the answer (LAST-LIGHT: nuclear out at 22%, wins at 71%).
- **A loop deliberately left unanswered in the middle** (ASTEROIDS' interstellar mystery, "either way") is fine if the master loop is strong.

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
| **Scale inward** (mirror of scale outward) | room → rug → mite → blood → cell → DNA → atom → nucleus → quark → the limit of measurement; the last rungs swap objects for limits | SHRINK |
| **Identity ladder** | human → monster → "no longer human" → planet-like body → galaxy → the universe itself | GROW-1CM |
| **Candidate elimination by lifespan** | hours → days → years → decades → a century → centuries; cause of death moves people → maintenance → wear → chemistry → physics | LAST-LIGHT |
| **Verdict scorecard** | each case ends on a graded verdict (local → regional → not extinction → extinction → total reset) | ASTEROIDS |
| **What's-lost ladder** | comfort → continents → body traits → home → identity → industry → computers → leaving Earth | NO-CLOTHES |
| **Circle of impact** | you → one family member → experts → the world's media → everyone like you → society → every institution | WOMB |
| **Crossing lines** | loot rises while the crew falls (4 → 3 → 2 → 1); the whole video is that picture | HIBERNATE |
| **Concept ladder** | boundary → time paradox → body → loophole → geometry → time → end of physics (bigger in idea, not in size) | BLACK-HOLE-NS |
| **Inside-out journey** | closed city → off the map → the past (drowned town) → danger → taboo → the open world | UNDERWATER |

Rung rules: one idea per rung; one real number per rung; each rung bigger, faster, closer or more personal than the last; the top rung is the most human or most personal, not just the biggest. New from the expansion: **the scale ladder can end on a real limit instead of an object** (Planck length, the observable universe), which gives an "endless" premise a true ending (SHRINK, GROW-1CM). In a repeated-card format, give **each rung one new mechanism** so it is not a re-run (ASTEROIDS).

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
| T12 | **Honest speculation flag** — say aloud where agreed science ends before the speculative payoff | LAST-HUMAN, BILLION-YEARS, SHRINK, BLACK-HOLE-NS |
| T13 | **Delayed consequence** — the return looks like a fix; a false-calm repeat of the opening shot, one permanent small change, then a third clock to a bigger hit minutes later | IRON |
| T14 | **The eliminated candidate wins** — something ruled out early returns in a new form as the answer, after a hedged front-runner and a false ending | LAST-LIGHT |
| T15 | **The premise saves you** — each threat is escaped by the premise itself (you shrink past it), which drops you into the next world | SHRINK |
| T16 | **Word-for-word bookend** — an early boast repeated at the end over an image that reverses it | HIBERNATE |
| T17 | **Bluff, then the real slow version** — the threat is called off, then a calm "until" adds the true far-future version of the same threat | SUN-GONE |
| T18 | **Decode payoff** — the riddle from the hook happens to the hero; myth-busts in a row; a 2-word reveal; a childhood rhyme's joke reversed | UNDERWATER |
| T19 | **"You" dies** — the timeline needs an end state: your death in the second person, then deep time and what lasts | LAST-HUMAN-2, WOMB |
| T20 | **Fake ending by real science** — an honest "here is how it really ends" early, waved off to open the master loop | GROW-1CM |

---

## 7. Endings and CTAs

- **Shorts:** black 1–2 s → exact title repeat (the last frame matches the first, so the replay loops) → one small-caps real fact (a % of your body, a dated historical event) held ~6 s. No on-screen CTA. Post caption = premise retold in 4–8 escalating sentences + a comment prompt: *which one next / which would break first near you / would you have held on*. All 5 hits.
- **Long-form ending stack:** master payoff → bookend to the opening place or object → recap of 4–5 milestones (icon timeline or thumbnail grid) → one-line thesis or moral → **personal choice question** that restates the premise (who would you pick, which stop, which one thing survives, binary dilemma) → optional series hook. Subscribe asks are rare (only EVERY-HUMAN, framed as an identity compliment); no corpus video asks mid-roll.
- The CTA question is always answerable by everyone (no wrong answers) and uses options the video already showed (BILLION-YEARS: the 10 stops; LAST-HUMAN-2 turns its on-screen epitaph into "what would you write?").
- **Loop cut** (expansion): both narrated What If Shorts end with the final sentence cut off on a joining word, so the replay's first line finishes it (GROW-1CM, BLACK-HOLE-NS). A silent subscribe card or a brand-pun card is the sketch-channel ending (SUN-GONE, NOCTURNAL, HIBERNATE).
- **No-CTA endings are common in the expansion**: SHRINK, LAST-LIGHT, UNDERWATER, ASTEROIDS and HIBERNATE have no comment question. An exact answer to the title (LAST-LIGHT), a real limit (SHRINK) or a reversed bookend (HIBERNATE) does the CTA's job.

## 8. Series / part-2 mechanics

- **Swap the variable, keep the template.** @man_ia_c's three biggest hits (electrons, oxygen, neutrons) came within 2 days of each other on an identical template; the comment CTA harvests the next variable.
- **Fatigue is real.** Same-template follow-ups decay when the premise is a near-repeat or less fundamental: hydrogen 0.67×, "lost a proton" 0.24× (after "gained a proton" 1.92×). Pop-star sequel (10 billion×) 3.36× vs the original's 7.84× (~43%).
- **Long-form "Part 2/3" halves each time:** IFOLOGY Zombie 93K → 47K → 40K; Awaken Last Guy → Last Girl 401K → 184K. Make **standalone episodes** that share a universe instead (IFOLOGY's team crossovers as the cliffhanger act; STOP-TIME, 10X-FASTER), and leave exactly one loop open (a villain, a "who else moves?") for the next episode.
- Never put "Part 2" in a title. Put the shared element (HUD design, sidekick, team, recurring home set) in the video instead.
- Expansion checks: the 4th particle in the @man_ia_c template (IRON, 4.32×) scored below the first three (8–29×), so the template still decays. The same premise from a second channel can still break out: LAST-HUMAN-2 (OminiAM, 25×) a week after LAST-HUMAN (Oddly Elsewhere, 6×). Both channels re-use their series grammar (brand sting, recurring sets) rather than "Part 2" (If Humans, SolarBalls, What If).

---

## 9. Pacing stats (measured)

From `tools/pacing_stats.json` (re-run 12:45 UTC over all 25 raw transcripts; the script now sorts each file into a format group and prints group medians). Sentences split on . ? ! in auto-subs; "second person" = sentences containing you/your/you're/yourself; numbers = digit tokens + number words (two…trillion, half, percent). Hook lengths and loop counts are read from the annotated `.md` files, not the script. AV1zVKuEtFc (SUN-GONE) has unpunctuated auto-subs, so its sentence metrics are left out.

### Long-form, narrated (12 scripts: original 7 + LAST-LIGHT, ASTEROIDS, NO-CLOTHES, LAST-HUMAN-2, UNDERWATER)

| Metric | Median (12) | Range | Was (7) | Notes |
|---|---|---|---|---|
| Words per minute | **153** | 134–219 | 154 (134–186) | xkcd's LAST-LIGHT (219) is a dense expert read with 21-word sentences. Without it the range is 134–186. Timeline/explainer engines 135–155; story-led power stories 165–186 |
| Total words | 1,780 | 934–3,186 | 1,783 | ASTEROIDS is 23.6 min |
| Cold-open hook length | **~88 words / ~34 s** | 33–123 words, 10–49 s | 87 / 34 s | premise stated by ~8–10 s median (3–34 s); stated late on purpose by ASTEROIDS (34 s, benchmark first) and LAST-HUMAN-2 (29 s, implied from word one); never stated in UNDERWATER |
| Sentence length (mean words) | **9.8** | 7.2–21.0 | 9.0 | 8.6–10.8 for 10 of 12 |
| Punch lines (≤3-word sentences) | **11.8%** | 0–23% | 14.7% | the new five are lower (0–10%); story engines still 13–23% |
| % sentences in second person | **27%** | 0–59% | 33% | story engines 48–59%; LAST-LIGHT 0% ("we", reader question) and ASTEROIDS 14.5% (placed in the same slot of every cascade) |
| "you" words per 100 words | 3.6 | 0–9.2 | 3.8 | |
| Numbers per minute | **3.5** | 0.9–8.2 | 4.7 | lower in the new five (0.9–3.3); LAST-HUMAN-2 at 25× has 0.9 |
| Questions per minute | 0.55 | 0–1.6 | 0.66 | auto-subs drop some "?" |
| Pivot words (but/except/until/here's/problem…) per min | **1.5** | 0.4–2.4 | 1.5 | held |
| Open loops per minute | **~1.2–1.3** | 0.25–2.2 | 1.16 | from the annotated loop tables |
| Verbal re-hook interval | **~30 s** | 17–43 s | ~30 s | ASTEROIDS 43 s is the slowest |
| Chapter stamp interval | ~50–60 s | 25–112 s (case cards 170–300 s) | 60–75 s | |

### Shorts, caption-only sims (6 scripts: 5 original + IRON; 80 s each)

| Metric | Median (6) | Range | Notes |
|---|---|---|---|
| Caption words per minute | **56** | 43–65 | ~11 captions; TTS read of captions should stay ~60–70 wpm with the same holds |
| All on-screen text per minute (title, HUD, end card) | 118 | 103–164 | IRON is the densest (164) and has the lowest score of the six |
| Title (hook) length | **7 words**, held **5–8 s** | 7–9 words | event lands at 8 s (10%) in 5/6 |
| Captions per video | 11 | 11–13 | |
| Caption length (mean words) | **6.7** | 5.3–7.3; max 7–10 | one claim per caption, no subordinate clauses |
| Caption gap | **4.75 s** median | 4.0–6.0 (means 4.7–6.4) | IRON front-loads: 8 captions in the first 26 s, then the HUD carries the rest |
| New on-screen element every | 3.65 s | 3.0–3.8 s | |
| Captions in second person | **18%** (= 1–2 lines) | 7–23% | |
| Numbers per minute (all text) | **14.6** | 7–25 | most live in the HUD, not the captions (0–5 numeric captions) |
| Open loops per minute | **3.75** | 3.0–6.0 | IRON 6.0 |

### Shorts, narrated (3 scripts, new)

| Metric | GROW-1CM | BLACK-HOLE-NS | SUN-GONE (skit) | Use |
|---|---|---|---|---|
| Duration | 172 s | 152 s | 81 s | VO Shorts can run 2.5–3 min if the VO pivots every ~15 s |
| Words / wpm | 436 / 152 | 418 / 165 | 213 / 158 | **~158 wpm** median |
| % sentences with "you" | 88% | 74% | n/a | near-total second person |
| Numbers per minute | 4.9 | 0 | 0.7 | a moving number is optional here; the 69× one has it |
| Pivots per minute | 1.4 | 3.6 | 3.0 | |
| Hook | 12-word premise in ~2 s + 2 maths rungs (29 words / 9 s) | 12 words / 4 s | 26 words / 11 s (two voices) | |
| Ending | mid-sentence loop cut | mid-sentence loop cut | silent subscribe card | |

### Other formats (1–2 scripts each, new)

| Format | Key numbers |
|---|---|
| Caption-only long (SHRINK, 405 s) | 50 captions, 229 caption words, mean **4.6 words** (max 8), **34 caption wpm**, a caption every **7.7 s** (4–13 s), a HUD comparison subline every ~22 s, a macro re-hook every ~30 s (max 58 s), 33% of captions in second person, hook 12 words of text in ~10 s |
| Scrolling card timeline (WOMB, 182 s) | 50 cards, one every **3.5 s**; title 4.8 words, body 14.5 words; 80 title words/min (318 with bodies, which are optional reading); 54% of card lines in second person; time-unit jump every ~8–30 s, a major re-hook every ~9 s |
| Sketch (NOCTURNAL 90 s, HIBERNATE 283 s) | 27 and 62 wpm; a cut every 3.5–10 s; story turns every ~17 s (HIBERNATE); 24–44% of spoken lines ≤3 words; 0–1 numbers per minute |

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

IRON (4.32×, like rate 4.8%) sits between the two columns. It has every hit feature, but it is the 4th particle on the same template and carries the most on-screen text (164 words/min, 25 numbers/min vs 103–131 and 7–18). Read it as template fatigue plus over-dense HUD, not as a failed structure.

### 10D. What the very top share across channels

The four highest outlier scores (EVERY-HUMAN 107×, BILLION-YEARS 41×, ELECTRONS 29×, OXYGEN 21×) all have: (1) a **running tracker** on screen from the hook to the end (clock, year badge, return countdown); (2) a **master loop held to ≥85%** (in Shorts, the return clock spans ~70% and closes at ~80%); (3) a **ladder on a log or outward scale**, so the viewer can feel how many rungs are left; (4) a **payoff that lands on the viewer** (your body, your house, a human trace); (5) **real, checkable numbers** plus at least one real dated precedent. Second person is not required (EVERY-HUMAN is 5%); **the viewer's position is** (here, right now, your house). The two new top scores fit all five: SHRINK (623×) has the falling YOUR SIZE counter from frame 1, a master loop to 96%, a log-scale inward ladder, the payoff on "you" (closer in size to the universe than to the bottom of physics) and real facts on every rung; GROW-1CM (69×) has a time stamp every ~10 s, a master loop of 78%, a log-scale outward ladder and an identity payoff on "you".

### 10E. Expansion pairs (same channel or same premise; no new low-performer controls were added)

| Pair | Higher | Lower | What differs |
|---|---|---|---|
| What If, narrated Shorts | GROW-1CM 69× | BLACK-HOLE-NS 9× | Same host voice, pace (152 vs 165 wpm), heavy "you" (88% vs 74%), loop-cut ending. The hit has a **moving number** (a time stamp every ~10 s, 4.9 numbers/min) and a log ladder the viewer can count; the other has 0 numbers and relies on concepts and analogies |
| Same premise, two channels | LAST-HUMAN-2 (OminiAM) 25× | LAST-HUMAN (Oddly Elsewhere) 6× | Both use the same science beats: grid and blackout sky, reactors shut down, food rots, the space station falls, scurvy, water wrecks buildings, nature returns. The premise forces those beats. The 25× one adds a **format promise** and 13 chapter stamps (vs 9), puts more facts per chapter, kills "you" at the end and asks a CTA question; the 6× one is a diary with jokes and a twist. Absolute views favour the 6× (914K vs 243K, a week older): the scores are relative to each channel |
| OminiAM, all four | 25–107× | (channel median) | All 147–154 wpm, chapter/timeline spine, real science before speculation, a 45–50 s hook with 3 teases or questions, a personal choice CTA. Numbers per minute vary (0.9–3.7) and second person varies (5–41%), so neither drives their wins |
| If Humans | NOCTURNAL 16× (90 s, ~0 words) | HIBERNATE 12.6× (283 s story) | The shorter, wordless gag premise beat the narrative one; both open on the brand sting with no spoken hook |
| Oddly Elsewhere | LAST-HUMAN 6.1× | UNDERWATER 4.8× | Both second-person narrative at 145–154 wpm; UNDERWATER never states the premise. Both are outliers, so this pair says little |

Corpus-wide check: over the 12 narrated long-forms, no pacing metric tracks outlier score (Spearman |ρ| ≤ 0.47; questions/min +0.47 and duration +0.45 come from the four long OminiAM uploads, wpm −0.31). Across channels the score mostly measures channel size and age. **The within-channel IFOLOGY result (10A) is still the only clean pacing signal**: more "you", more pivots and a faster pace inside one story channel. Structural features (tracker, master loop, log ladder, payoff on the viewer) are the cross-channel signal.

---

## 11. Device catalog (approximate frequency: regex-tagged beat/device cells across the 1,321 annotated lines of the original 12)

Counts were not re-run for the expansion. New devices it adds, each in at least one hit: **matched-frame swap** (same place, two lightings: NOCTURNAL); **selective deletion** (the object goes, its people stay: IRON); **dramatic-irony decode** (UNDERWATER); **outside-vs-inside viewpoint pair** (BLACK-HOLE-NS); **real-science off-ramp** (GROW-1CM); **first-hand operator quotes** as authority (LAST-LIGHT); **themed sponsor read** with fictional headlines about the case just shown (ASTEROIDS, at 21%); **flat literal icons** that carry a card on their own (WOMB); **fake deaths by cut to black** (SHRINK); **mid-sentence loop cut** (What If Shorts).

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
- [ ] Keep all on-screen text ≤ ~130 words/min and the HUD readable (IRON at 164 is the weakest of the six).

**Narrated Shorts (2:30–3:00, optional variant)**
- [ ] Premise is sentence one (≤12 words, ≤4 s); 2 checkable maths rungs by ~9 s.
- [ ] ~155–165 wpm, "you" in most sentences, a time/scale milestone every ~10 s, a turn phrase every 15–40 s.
- [ ] One honest real-science off-ramp by ~20%, then a pivot that opens the master loop (ends ~75–80%).
- [ ] Ends on the biggest real number, then a sentence cut mid-way so the replay completes it. No CTA.

**Long-form (7–13 min)**
- [ ] Cold open ≤50 s / ≤120 words (target ~35 s / ~90), premise stated (or unmistakably shown) by ~10 s, impossible change inside the first two sentences, no channel intro. If the hook leads with a real benchmark instead, close that benchmark loop by ~2/3.
- [ ] Rules stated with one explicit "remember this" plant that pays off at 40–60%.
- [ ] 145–155 wpm for explainer/timeline engines; 175–185 for power stories. Mean sentence 8–10 words, 8–15% punch lines.
- [ ] Second person in ≥45% of sentences for power stories (≥25% otherwise), and in the first sentence.
- [ ] Re-hook every ≤30 s (no gap >35 s); chapter stamp every 60–75 s; ~1 new loop per minute; ≥1.5 pivots/min.
- [ ] ≥3 numbers per minute on average (real and checkable). Timeline engines can go lower if each chapter has one real fact.
- [ ] First turn by ~15–25%; midpoint re-hook at 45–70%; master payoff 80–95%; ending stack after the payoff ≤12% of runtime.
- [ ] 3+ plants longer than 3 min paid off; one loop optionally left open for the series.
- [ ] Each beat type has its own visual mode (story set / diagram board / chapter stamp).

---

## 13. Study these three first

1. **ELECTRONS — 7693494009494342945** (18.2M, 29.13×). The cleanest Shorts template: countdown → place → flip → wonder → rule → outward ladder → white-out → cosmic climb → return → twist → bookend fact. Every beat maps to a code component (HUD, wireframe line art, particles, white-out, serif cards). Read `7693494009494342945.md` §3.
2. **EVERY-HUMAN — b6jmbFcJZCY** (1.08M, 107×). The highest outlier and the best code-only long-form: a right-now hook, a trailer of dated promises paid shortest-first, a persistent time-since HUD with a scrubber, log-scale chapters with ironic buttons, a two-stage master reveal, and a recap + thesis ending. Read `b6jmbFcJZCY.md` (Structure summary + Transferable skeleton).
3. **RESTART — 6oZ9fdM0n50** (4.22M, 14.44×). The biggest long-form view count and ~80% flat 2D: a second-person cold open with a self-correction, a doubling ladder to a one-word false resolution, then mechanism → historical proof → escalation to an emotional floor → hope ladder → honest verdict with a hard number → choice CTA. Read `6oZ9fdM0n50.md`.

Next if you are writing a power story: **10X-FASTER — y300HjYnHPw** (rules + plant → honeymoon → numbered problems → rug pull → real analogue → rescue → universe hook).

From the expansion, by job:
- Caption-only long-form, or a scale ladder: **SHRINK — YayPaipjNAM** (623×; `YayPaipjNAM.md` Transferable skeleton).
- A narrated 2–3 min Short: **GROW-1CM — 2d6Ciu3INeA** (69×; off-ramp + pivot + log ladder + loop cut).
- A question with one exact answer: **LAST-LIGHT — 8fADp43wJwU** (10.4M; candidate chase + eliminated-candidate twist).
- A timeline that needs no narration: **WOMB — eiBR6wlwPfA** (cheapest to build: one card component + a scroll).
- A @man_ia_c Short with a delayed twist: **IRON — 7693888660256722208**.

---

## 14. What changed with the expansion

Added at 12:08–12:35 UTC: 13 annotated scripts (6 new channels, 4 new outliers from known channels, 7 new sub-formats). Stats re-run over all 25. No ordinary controls were added, so §10A–10C are unchanged and §10E uses within-channel and same-premise pairs only.

**What held**
- The structural core: one changed rule + the viewer's position + a tracker that is already moving + a master loop to ≥78% + a log-scale ladder + a payoff on the viewer. It holds in both new top scores (SHRINK YayPaipjNAM 623×, GROW-1CM 2d6Ciu3INeA 69×) and in 11 of 12 narrated long-forms (new five 85–95%: 8fADp43wJwU, Q9F0z4CR0gM, n1CYFTKR_B0, DgftZCQe8sI, K_56-ZqYviY).
- Long-form pace and turns: median **153 wpm** (was 154), **1.5 pivots/min** (unchanged), re-hook **~30 s**, hook **~88 words / ~34 s** (was 87 / 34).
- The @man_ia_c Short template: IRON (7693888660256722208) fits every S-beat; caption length, cadence and second-person share did not move (6.7 words, ~4.75 s, 18%).
- Series fatigue: the 4th particle on the same template scored lowest (4.32×).

**What shifted**
- Second person in long-form fell from 33% to **27%**, numbers/min from 4.7 to **3.5**, punch lines from 14.7% to **11.8%**. Expert and documentary voices (8fADp43wJwU 0% "you", Q9F0z4CR0gM 14.5%) and a 25× timeline at 0.9 numbers/min (DgftZCQe8sI) show these are style choices, not requirements. The IFOLOGY within-channel result (more "you" and pivots win) still stands for story engines.
- Beat timings: the first turn now comes earlier (13–22% in the new five), the midpoint spreads later (57–72%) and the master payoff lands later (87–95%; DgftZCQe8sI 89%, K_56-ZqYviY 87%, 8fADp43wJwU 94%).
- Chapter stamps now come more often: ~50–60 s median (was 60–75 s). DgftZCQe8sI runs 13 stamps in 651 s; n1CYFTKR_B0's chapters are 38–75 s.
- Shorts are not capped at 85 s: narrated What If Shorts run 2:32–2:52 at ~158 wpm (2d6Ciu3INeA, VZ27faCr8UU).
- A CTA question is optional: 5 of the 13 new videos have none (YayPaipjNAM, 8fADp43wJwU, K_56-ZqYviY, Q9F0z4CR0gM, DOEQgRAFeI0).

**New patterns**
- Hooks H13–H21 (§2): tiny-rate premise + ×60 rungs, flash-forward + counter, a named reader's question, a riddle from inside the world, imagine + rule-outs + 3 teases, micro-absences + format promise, a famous benchmark first, a casually asked question that is overheard, and no spoken hook at all (sketch and card channels).
- Engines (§1B): candidate chase (8fADp43wJwU), stack the extremes (Q9F0z4CR0gM), alt history (n1CYFTKR_B0), worldbuilding story (K_56-ZqYviY), caption-only long (YayPaipjNAM), scrolling card timeline (eiBR6wlwPfA), story sketch (DOEQgRAFeI0). Short variants (§1A+): narrated ladder (2d6Ciu3INeA, VZ27faCr8UU), character skit (AV1zVKuEtFc), wordless gag montage (rzoq6AOgudA).
- Twists T13–T20 (§6): delayed consequence with a third clock (IRON), the eliminated candidate wins (8fADp43wJwU), the premise saves you (YayPaipjNAM), a word-for-word bookend (DOEQgRAFeI0), a bluff and then the real slow version (AV1zVKuEtFc), a decode payoff (K_56-ZqYviY), "you" dies (DgftZCQe8sI, eiBR6wlwPfA), a fake ending by real science (2d6Ciu3INeA).
- Ladders (§5): scale inward, identity, candidate lifespan, verdict scorecard, what's lost, circle of impact, crossing lines, concept, inside-out.
- Two code-cheap formats with proven reach, both a good fit for our kit: **caption-only long-form** (YayPaipjNAM: HUD + serif captions, ~230 words for 6:45) and the **scrolling card timeline** (eiBR6wlwPfA: one card component, 50 cards, no VO).
- Sponsor placement, if ever needed: themed to the episode, at ~21% right after the first case and a cliffhanger bridge (Q9F0z4CR0gM).

**Caveats**
- Outlier scores are channel-relative. 623× (6K-sub channel) and 4.3× (xkcd, 1.38M subs, 10.4M views) are not comparable sizes. Three expansion picks are older than their channel's 60-upload window (AV1zVKuEtFc, eiBR6wlwPfA, 8fADp43wJwU), so they are scored against today's median.
- Frames were not checked for 2d6Ciu3INeA or VZ27faCr8UU; their visual notes are inferred from the script. SUN-GONE's sentence metrics are excluded (no punctuation).
