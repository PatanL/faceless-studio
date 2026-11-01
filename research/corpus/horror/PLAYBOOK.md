# Horror PLAYBOOK: viral skeleton, devices, pacing

Built 2026-11-01, about 09:05 UTC, from the 12 annotated scripts in this folder (`<id>.md`, `raw/<id>.txt`, `SOURCES.md`), the 4 alternates in `raw/_alt/`, and **controls** from `research/library/` (horror videos at or near their channel median, with transcripts in `research/library/transcripts/` and teardowns in `research/library/videos/<id>.json`).
- Machine-readable index: `INDEX.json`. Each `beat_sequence` there uses the B1–B12, S1–S10 and P2 tags from §1.
- Pacing numbers come from `tools/pacing_stats.py` (output `tools/pacing_stats.json`), not from memory. Re-hook and open-loop counts come from the tables in each annotated file.

**Use rules.**
- Borrow structure, timing and devices only. Never borrow wording, names, plots, footage or audio (BRIEF rule 5). Every TikTok source here is a translated repost of a Chinese animated series, so its story is not ours to adapt either.
- This file has no source line longer than 6 words. Everything below is an abstracted pattern with `[slots]`.
- Before you write, pick the 2–3 closest corpus scripts, put them in your front matter, and fill in a beat-alignment table (BRIEF Update 09:00).
- Run `python3 scripts/originality_check.py <script.md> research/corpus research/library/transcripts` until it prints PASS.

### Source key

Outlier = views ÷ the channel's median views (the basis for each is in `SOURCES.md`).

| id | short name | fmt | dur | views | outlier |
|---|---|---|---|---|---|
| 7654526047005723937 | SIEGE-OVERLAY (@mraevq) | narrated story, group chat + floating comments | 5:57 | 717K | **66.7** |
| 7702661541224566049 | HEARSE-P1 (@udhwkz) | narrated story, Part 1 | 3:21 | 2.2M | **63.1** |
| cVUJmsVkUW4 | MOM-NOTE (WrONG Rules) | rules note, 16:9 | 2:15 | 291K | **31.0** |
| T42u5xhrq-0 | TEXT-FIGURE (Textify) | chat Short | 1:00 | 869K | **25.5** |
| 7692268145888873760 | TRUCKER-RULES (@udhwkz) | narrated story | 2:46 | 695K | 19.9 |
| omuJBFs2L6c | CLASSMATE-PSA (Dusk Broadcast) | broadcast PSA | 1:37 | 763K | 18.6 |
| 7670495663624408352 | DORM-RULES (@mraevq) | narrated story | 2:55 | 194K | 18.0 |
| 7694996216505060641 | FLOOR-PHRASE (@udhwkz) | narrated story | 2:45 | 613K | 17.6 |
| 7659677578365537569 | SIEGE-CHAT (@udhwkz) | narrated story, group chat | 4:09 | 376K | 10.8 |
| gzXY52lcAcI | FARM-FLASHFWD (Textify) | chat Short, Part 1 | 0:59 | 353K | 10.4 |
| 7702661471641128224 | HEARSE-P2 (@udhwkz) | narrated story, Part 2 | 3:11 | 343K | 9.9 |
| Qz-TrB6W2SM | HOTEL-DOOR (Wansee) | first-person true story, 16:9 | 2:48 | 1.52M | 9.0 |

The **controls** used in §6 are videos at about 1× their channel median, mostly from the same channels:

| id | channel | dur | outlier |
|---|---|---|---|
| 7696062340852190496 | @udhwkz | 2:48 | 0.77 |
| 7665304797242821921 | @mraevq | 7:02 | 1.06 |
| xKgepVHATm4 | WrONG Rules | 1:00 | 1.00 |
| epzTfKxp16E | Wansee | 5:12 | 1.16 |
| KJfJKo400b0 | twezed | 9:56 | 0.94 |
| dqEIz_8bP-8 | lehwh7 | 11:01 | 1.01 |
| 0xzpKw7To98 | Texty Stories | 13:45 | 1.03 |

There are also four **extra library outliers**: 7664930759395888416 (@mraevq, 15:18, 39.8×), 7666044652910316833 (@mraevq, 6:43, 30.3×), BciSW_2VMZg (WrONG Rules, 0:50, 11.0×) and Xv32FAAUI-0 (Texty Stories, 12:52, 7.5×).

---

## 0. The niche in one paragraph

A horror short goes viral when, within the first 10 seconds:
1. a **rule** gets stated, or something **trusted** gets declared safe;
2. a **threat arrives at a barrier the viewer recognises**: a door, a phone, a car seat, a bed;
3. a source the hero (or viewer) can't ignore says **the trusted thing is lying**.

After that the video is a **ladder**. Each rung either takes away one safe channel (chat, signal, ally, door) or brings the threat one step closer (building, door, room, bed, phone, "you"). A new jolt arrives about every 6 s.

- The **scariest image appears once**, late (about 65–80% through), and holds still.
- The **truth twist** lands in the last 10–12%. Usually it shows that an authority figure, a helper or a "safe" object was the danger all along.
- The video **stops** with 3–6 loops still open. There is no spoken subscribe. The cut itself, or a "part / full story" card, is the call to action.

All of this is cheap to build in code: chat panels, peepholes, rule cards, broadcast pictograms and flat puppets with 4–5 expressions.

---

## 1. Canonical viral skeleton

The corpus has two lengths:
- **Shorts**: 50–100 s, chat, rules or broadcast.
- **Story**: 150–360 s narrated TikTok / YouTube "long-form" for this niche, with a sweet spot of 165–250 s.

The 10–20 min library uploads at ~1× (twezed, lehwh7, Texty Stories) show what happens when the story skeleton is stretched without the micro cadence. See §1C.

### 1A. Story (150–360 s): beats B1–B12

% values are medians across the 10 narrated or rules stories, with ranges in brackets. The seconds columns use a **3:00** cut (180 s) and a **6:00** cut (360 s). The hook is capped in absolute seconds, not scaled.

| # | Beat | % of runtime | s @180 | s @360 | What happens | Exemplars |
|---|---|---|---|---|---|---|
| B1 | **Hook: threat + rule or false safety** | 0–5% (2–7) | 0–6 (≤9) | 0–6 (≤14) | Line 1 puts a danger in a place the viewer knows, or states a taboo as common knowledge. Lines 2–3 add a reason or an official all-clear that will be undercut. Median **27 words / 6 s**. The threat is visible in frame 1. No intro, no title card, no greeting. | HEARSE-P1, SIEGE-CHAT, SIEGE-OVERLAY, TRUCKER-RULES, FLOOR-PHRASE, DORM-RULES |
| B2 | **Rules / false safety laid down** | 3–10% (2–17) | 5–18 | 10–36 | The world's law gets spoken: a mentor's maxim, a numbered list, an official "it's over", a protective ritual with "remember this". The rules become Chekhov's guns; the viewer starts counting violations. | TRUCKER-RULES, HEARSE-P1, DORM-RULES, MOM-NOTE, SIEGE-CHAT |
| B3 | **Intrusion at the barrier** | lands at **~6%** (1–27) | ~11 | ~20 | A knock, a stranger, a rule broken, a trigger spoken. The threat is now at *my* door or inside *my* space, often dressed as help (police, staff, a supervisor). The hero nearly complies. | SIEGE-OVERLAY (5 s), FLOOR-PHRASE (3 s), SIEGE-CHAT (11 s), TRUCKER-RULES (10 s), HOTEL-DOOR (45 s, the title carries it) |
| B4 | **First proof: the trusted thing is wrong** | 8–20% (2–28) | 15–36 | 30–72 | A countable clue (N marks equals N confirmations), an omniscient overlay, a radio report that matches, or a rule that backfires on the first try. The viewer now knows more than the neighbours. | SIEGE-CHAT (11%), SIEGE-OVERLAY (2%), TRUCKER-RULES (17%), DORM-RULES (9%), FLOOR-PHRASE (25%) |
| B5 | **Pressure ladder** | 15–45% | 27–81 | 54–162 | 3–6 rungs, one every ~8 s (physical rungs ~3 s). Each rung removes a safe channel or brings the threat closer. A companion speaks the viewer's objections and gets shut down. Each rung ends on a 3–5 word verdict line. | SIEGE-CHAT, SIEGE-OVERLAY, HEARSE-P1 (ritual), FLOOR-PHRASE, HOTEL-DOOR (door ladder) |
| B6 | **Isolation** | 40–55% (16–66) | 72–99 | 144–198 | Signal gone, help far away (give a number: km, minutes), the ally silenced or muted. Often only the enemy's channel still works. | SIEGE-CHAT (49–61%), SIEGE-OVERLAY, FARM-FLASHFWD, HOTEL-DOOR |
| B7 | **Lull + plant** (≤ 20–25 s) | 40–50% | 72–90 | 144–180 | The only breather. A hidden face, a quiet car, a kindness; plant the object, charm or phone that saves or betrays later. **The weakest stretch in every source.** Keep it under 25 s and give it one foreshadow line. | HEARSE-P1 (45–50%), TRUCKER-RULES (31–45%, too long), SIEGE-OVERLAY (43–51%), FLOOR-PHRASE |
| B8 | **Midpoint turn** | 45–60% | 81–108 | 162–216 | The frame flips: a personal link to the threat, a rule inverted, the "monster" turns out to be the real expert, or "it isn't him, it's what's in him". | DORM-RULES (50–63%), HEARSE-P1 (50%), HEARSE-P2 (55–65%), TEXT-FIGURE (50%), CLASSMATE-PSA (43%) |
| B9 | **Peak contact** | starts at **~67%** (47–80), runs 60–80% | 108–144 | 216–288 | A sensory or physical hit: a touch, a mirror ritual, an assault, eyes in the safe place. **One** scariest image, held still for ~4 s. Every story in the pool puts it after 45%. | HEARSE-P1 (67–78%), FLOOR-PHRASE (61–74%), MOM-NOTE (76–82%), SIEGE-OVERLAY (72%), HOTEL-DOOR (68–80%) |
| B10 | **Lifeline under a clock** | 72–90% | 130–162 | 259–324 | A left-behind phone, a 30 s battery, the real authority on a failing line, or a call to family. Ask the viewer's questions out loud and get answers in rising order. | SIEGE-CHAT (80–97%), SIEGE-OVERLAY (31–43% in the 6-min cut), FLOOR-PHRASE, HOTEL-DOOR |
| B11 | **Truth twist** | lands at **~89%** (55–98) | ~160 | ~320 | The authority never existed, one killer is really a crew, a private fact contradicts the companion, the helper betrays, the victim's own number answers as the entity, or (after safety) it was worse than you knew. | SIEGE-CHAT (90–96%), HEARSE-P1 (93%), FLOOR-PHRASE (98%), TEXT-FIGURE (93%), HOTEL-DOOR (88%), DORM-RULES (59%, early variant) |
| B12 | **Cliffhanger / sign-off** | last **~5%** (1–10) | 171–180 | 342–360 | Cut at the moment of greatest need: a new imperative from an unknown sender, a new rule from a new authority, a diagnosis with no remedy, the possessed one asking for control. The final shot bookends the opening shot. Only a "part" or "full story" card, never a spoken subscribe. | all 12 |

Shape: setup (B1–B3) ≈ 10%, investigation and pressure (B4–B7) ≈ 40%, turn and peak (B8–B9) ≈ 30%, lifeline, twist and cut (B10–B12) ≈ 20%. Early loops close before 50%; loops opened after 50% stay open.

**Sequel variant P2** (HEARSE-P2): a cold open mid-scene with no recap → a jolt by 6% → a fast physical ladder → pay off a Part-1 plant by ~45% → falsify the companion's story with an outside check → name the entity in the last 2% with no remedy. The hard hook only arrives at 0:20, and P2 got **16% of P1's views** (§5).

### 1B. Shorts (50–100 s): beats S1–S10

Seconds assume a **60 s** chat or rules Short; the broadcast PSA runs the same beats at 97 s. % values are medians across TEXT-FIGURE, FARM-FLASHFWD, CLASSMATE-PSA and the alt BciSW_2VMZg.

| # | Beat | % | s @60 | What happens | Exemplars |
|---|---|---|---|---|---|
| S1 | **Hook** | 0–5% | 0–3 | A late-night text with a mood line; an all-caps flash-forward order; an urgent imperative that presupposes the viewer is already inside ("your [talisman]"); or a brand ident plus an attention command. 4+ bubbles or 2 lines in the first 3 s. | TEXT-FIGURE, FARM-FLASHFWD, BciSW_2VMZg, CLASSMATE-PSA |
| S2 | **Named threat / premise paid** | 5–12% | 3–7 | Name the source of the danger (a channel, an app, "one extra [person]"). The title promise is paid by about 12%. | TEXT-FIGURE (0:03), CLASSMATE-PSA (0:11) |
| S3 | **Setup + plant** | 8–25% | 5–15 | Describe it vaguely through the senses. Plant **one odd detail** that will come back as the threat. | TEXT-FIGURE (0:13 plant → 0:42 payoff), BciSW_2VMZg (doll) |
| S4 | **Rule or warning, stair-stepped** | 23–38% | 14–23 | A common-sense warning gets ignored, or rule 2 arrives. The source starts acting alive in 3 rising lines. | TEXT-FIGURE, CLASSMATE-PSA (symptom list), FARM-FLASHFWD |
| S5 | **Exit closed / unsettling reassurance** | 38–50% | 23–30 | The obvious fix fails ("I can't"). Or a calm line implies that harm is expected. | TEXT-FIGURE, BciSW_2VMZg, FARM-FLASHFWD (rescuer 30+ min away) |
| S6 | **Turn at ~50%** | 43–55% | 26–33 | A sound, or "in **your** [place]". The threat crosses from the source into the viewer's space. Use the video's only full-frame colour flash here. | TEXT-FIGURE (52%), CLASSMATE-PSA (43–48%), BciSW_2VMZg (55%) |
| S7 | **Proximity / panic ladder** | 50–78% | 30–47 | Distance shrinks rung by rung (corner, closer, bed). The typography gets louder (CAPS). A weapon or a new sense. | TEXT-FIGURE, FARM-FLASHFWD, CLASSMATE-PSA |
| S8 | **Climax + silence beat** | 78–90% | 47–54 | Distance reaches zero. Two unanswered name checks; in chat, the gap itself is the scare. | TEXT-FIGURE |
| S9 | **Proof** | 88–92% | 53–55 | The only image in the video, or the talisman shown changed. | TEXT-FIGURE (photo), BciSW_2VMZg (corrupted doll) |
| S10 | **Twist on "you" / series card** | 92–100% | 55–60 | The victim's thread replies calmly as the entity and threatens the phone owner, or a relief line gets taken back ("for now"), or the screen blurs to a "full story" card. | TEXT-FIGURE, BciSW_2VMZg, FARM-FLASHFWD |

Shape: hook and premise ≈ 12%, creep ≈ 38%, physical horror ≈ 35%, proof and twist ≈ 10–15%. The **turn sits at 50%**.

### 1C. Long-form (5–15 min)

Only two long uploads in the pool beat their channel by more than 10×: SIEGE-OVERLAY at 5:57 and 7664930759395888416 at 15:18 (39.8×). Both run B1–B12 as **one master loop** and repeat B3–B9 as **set pieces every 30–60 s**:
- A one-line rule is planted in the first 3 s and comes back as the climax's last spoken line.
- Lore drops are scheduled 3–4 times, each one a withheld answer that gets partly released.
- The channel switches (narration, chat, overlay, call, radio) every 30–40 s.
- The midpoint reversal comes at ~33%, the climax at ~75%, and the cliffhanger takes the last 10%.

The 10–20 min controls at about 1× (twezed, lehwh7, Texty Stories) keep a similar 25–60 s macro cadence but **lose the 4–11 s micro jolts in between** (§6). Default to 165–250 s. Go long only for a serialized cast and only with the micro cadence intact.

### 1D. Story engines

All eight engines share the skeleton but weight different beats.

| Engine | Spine | Beats it stretches | Sources |
|---|---|---|---|
| **Locked-door siege** (fake authority + compromised group chat) | a door the hero must not open; three channels (door, chat, call) each confirm the twist from a different side | B4 count-match, B5 chat replay, B10 countdown call | SIEGE-CHAT, SIEGE-OVERLAY |
| **Taboo rule broken** (job or folk rule) | rules stated in the hook; a stranger breaks one; the trusted companion mirrors it | B2, B5 ritual, B9 mirror | HEARSE-P1/P2, TRUCKER-RULES |
| **Forbidden ordinary phrase** | one polite act, used 4–6 times; each reactor is closer to the hero and costs more | B3 repeated, B10 oracle | FLOOR-PHRASE |
| **Two rival authorities** | the rules that are supposed to protect backfire; the "monster" is the real expert | B2 twice, B8 rule inversion, B11 evidence | DORM-RULES |
| **Rules note** (absent guardian, second-person imperatives) | the list *is* the story; if/then branches; at least two planted contradictions | B2/B5 merged, two peaks (35–42%, 75–82%) | MOM-NOTE, BciSW_2VMZg |
| **Broadcast PSA** | third-person lore, then "in your [place]" at ~45%, then rules | S3 symptoms, S6 turn | CLASSMATE-PSA |
| **Chat thread** | you hold the listener's phone while the horror happens elsewhere | S7 ladder, S10 voice swap | TEXT-FIGURE, FARM-FLASHFWD |
| **True-story confession** | the title states the incident; cozy setup works as irony; a door ladder; a retro-reveal after safety | B2 long, B5 door ladder, B11 after rescue | HOTEL-DOOR |

---

## 2. Hook formulas (abstracted)

The hook is everything up to the first jolt after the premise is fully stated. Views and outliers are the sources' own figures.

| # | Formula (slots) | Mechanism | Sources (views, outlier) |
|---|---|---|---|
| H1 | **Everyone in [trade/place] knows you never [act]**, then the polite reason, then the real, fearful reason | Insider taboo as common knowledge, debunked into fear; the viewer waits for someone to break it | HEARSE-P1 2.2M, 63.1×; also tB9Ln4eINus (world rule, 4.7×) |
| H2 | **Do you know the rules for [job]? [rule], [rule], [rule]. [Mentor] taught me. Tonight I broke all of them.** | Rule list plus a confession; the viewer knows which rule is about to break | TRUCKER-RULES 695K, 19.9× |
| H3 | **[Danger] loose in my building → the official channel says it's over (with a number) → a knock** (+ optional: **an impossible source says the visitor is the danger**) | False safety, reversed by 5–11 s. The overlay variant adds dramatic irony in 7 s: the viewer knows more than the neighbours | SIEGE-OVERLAY 717K, **66.7×**; SIEGE-CHAT 376K, 10.8× |
| H4 | **I was [doing a mundane thing] when [a stranger] looked at *me* like I was the monster**, then the innocent trigger is spoken | Role inversion; the engine of the whole story is planted in under 5 s | FLOOR-PHRASE 613K, 17.6× |
| H5 | **[Ordinary object in a colour tag] → an authority goes pale → a death-linked origin → "your [close person] is not human"** | Authority fear works as proof; an accusation in "you" form | DORM-RULES 194K, 18.0× |
| H6 | **[Warm address: you're safe for now]. But skip one instruction and you die. This [document] is your lifeline. Got it?** | A warm-to-lethal flip at calm speed; the contrast does the work, not the pace | MOM-NOTE 291K, **31.0×** (its hookless re-cut got 1.0×, §6) |
| H7 | **[Urgent order: act now]. Make sure your [talisman] is nearby.** | Presupposition: the viewer is already inside the story and owns the object | BciSW_2VMZg 104K, 11.0× |
| H8 | **[Brand ident]. Pay attention. [Vague official event at scale] → [one countable anomaly]** | Institutional deadpan; the title promise is paid by 12 s | CLASSMATE-PSA 763K, 18.6× |
| H9 | **[Late-night text: you up?] [can't sleep] [I'm doing a mildly risky thing] [named source]** | A familiar intimate opener; 4 bubbles in 3 s; the genre is flagged in bubble 3 | TEXT-FIGURE 869K, 25.5× |
| H10 | **Flash-forward: a trusted figure's all-caps order about unnamed "them" → refusal → where are you?** then a cut back to a calm present | The ceiling is set in 1 s; every calm decision afterwards reads as a mistake | FARM-FLASHFWD 353K, 10.4× |
| H11 | **In-medias-res flight from an unnamed "it" + a one-line rule in the first 3 s + casualty proof by 8 s** (or: backstory line → "but [N months] later, it came to my door" → the monster speaks by 5 s) | Zero preamble; the rule is paid at the climax | 7664930759395888416 428K, 39.8×; 7666044652910316833 326K, 30.3× |
| H12 | **Title states the incident outright; audio = age + "this happened" + an unfamiliar place** | The title carries the hook, so a cozy setup reads as dramatic irony. Fails if the title is vague (control epzTfKxp16E, 1.16×) | HOTEL-DOOR 1.52M, 9.0× |

**Combination rule seen in every hit:** a **place the viewer knows** + a **rule or official reassurance** + a **contradiction from a source the hero can't dismiss**, all inside the first 10 s.
- The two top outliers (SIEGE-OVERLAY 66.7×, HEARSE-P1 63.1×) both contradict their own opening line by 5–7 s.
- Hook length: median **27 words / 6 s** (range 5–57 words, 1–14 s). Median **43 words** spoken in the first 10 s.
- **Never** open on atmosphere alone, mid-list, or mid-scene for cold viewers.

---

## 3. Re-hook cadence

| Layer | Shorts (60 s) | Story (150–360 s) |
|---|---|---|
| New bubble, caption or spoken line | **~1.1 s** per bubble (TEXT-FIGURE, FARM-FLASHFWD); the chat panel resets every 6–9 s | a caption card every ~2 s (1.4–2.4 s) |
| Picture change | the panel reset or pictogram every ~3 s | a cut or punch-in every **2–3 s** (TikTok dubs); 3–6 s (YouTube 16:9) |
| **Jolt** (a new anomaly, a rule, a question, a "just then", a number, a notification) | median **2.5–3.5 s**; 4–5 s in the first half, 1.5–2 s in the second | median **6 s** across the 12 (range 2.5–11). It tightens to 3–5 s in the last third |
| Longest dry stretch allowed | ≤ 5 s | median **17.5 s**, max 27 s, and only once (the B7 lull) |
| Rhetorical question | — | every ~4–5 s in inner-monologue engines (FLOOR-PHRASE: 35 questions in 166 s) |
| Master question restated in fresh words | — | every 20–30 s (FLOOR-PHRASE 5×, DORM-RULES 2× during the wait) |
| Channel or format switch (narration ↔ chat ↔ call ↔ overlay ↔ title card) | — | every 30–40 s; title cards every 10–15 s in the rules format |
| Big jolt / set piece | every 12–20 s | every 30–60 s (long-form) |
| Silence as a re-hook | 1 beat (unanswered name checks) | 1–3 beats of 3–8 s with SFX (HOTEL-DOOR's knock; FLOOR-PHRASE's dead air before the kicker) |

**Hard cap:** never go **>25 s** without a jolt. The two weakest stretches in the corpus are TRUCKER-RULES' 23 s lull and HEARSE-P1's 24 s explanation. The udhwkz control's 30–40 s stall is the thing it does worst (§6).

---

## 4. Escalation ladders, twists, endings

### 4A. Escalation ladders (use two at once and switch whenever one stalls)

| Ladder | Rungs (abstract) | Sources |
|---|---|---|
| **Proximity** | district → building → my door → my room → my bed → my phone → **you** | CLASSMATE-PSA, TEXT-FIGURE, SIEGE-CHAT, HEARSE-P1 (road → stranger → cab → driver's seat) |
| **Channel removal** | chat → phone → signal → ally → door → last lifeline (battery) | SIEGE-CHAT, SIEGE-OVERLAY |
| **Enemy scaling** | one person → armed → a crew → a leader with a plan | SIEGE-OVERLAY, SIEGE-CHAT |
| **Reactor closeness** | stranger → stranger → system → the "safe" stranger → family | FLOOR-PHRASE |
| **Sensory** | sound → approach → voice → touch, peaking near 47%, then the **information ladder** takes over (lie → remains → motive → *our* room) | DORM-RULES |
| **Volume** | knock → polite request → silence → shouted command → screaming | HOTEL-DOOR |
| **Barrier** | room door → it has a key → smaller locked room | HOTEL-DOOR, SIEGE-OVERLAY |
| **Measurable deltas** | worse / longer / heavier than an earlier state | HEARSE-P2 (the mark grows) |
| **Typography** (chat) | normal → ALL CAPS → broken lowercase → calm sentence case from the entity (the scariest register) | TEXT-FIGURE, FARM-FLASHFWD |

Rung spacing: physical rungs ~3 s apart, supernatural or information rungs ~15 s apart. Plant every rung that pays off later as a hyper-specific detail: a plate, a room number, a count, a colour.

### 4B. Twist / payoff patterns

| # | Pattern | Where | Sources |
|---|---|---|---|
| T1 | **Fake authority**: the officer, manager, supervisor or staff member is the threat | B3 → B11 | SIEGE-CHAT, SIEGE-OVERLAY, DORM-RULES, HOTEL-DOOR |
| T2 | **Count match**: N marks on the visitor = N confirmations in the chat | B4 (~11%) | SIEGE-CHAT; SIEGE-OVERLAY (victim number) |
| T3 | **Rule inversion**: the protective rule was the trap; the opposite is true | B8 (50–63%) | DORM-RULES, MOM-NOTE (contradictions), BciSW_2VMZg |
| T4 | **Mirror ritual**: the trusted companion repeats the stranger's uncanny act beat for beat, one detail worse | B9 (67–78%) | HEARSE-P1 |
| T5 | **Outside check falsifies the backstory**: a short question from family kills the companion's story | B11 | HEARSE-P1 (private fact), HEARSE-P2 |
| T6 | **Voice swap**: the victim's own channel speaks calmly as the entity | S10 / B11 | TEXT-FIGURE; 7666044652910316833 (a dead man's phone calls) |
| T7 | **Planted identifier pays off**: an ID or room number from early on proves the link | B8 / B11 | HEARSE-P2, DORM-RULES |
| T8 | **Retro-reveal after safety**: relief first, then it was worse than you knew | B11 | HOTEL-DOOR, epzTfKxp16E |
| T9 | **Trusted human betrays / exiles** the hero | B12 kicker | FLOOR-PHRASE, SIEGE-OVERLAY (ally) |
| T10 | **Scale-up**: one killer becomes a crew; the authority never existed | B10–B11 | SIEGE-CHAT, SIEGE-OVERLAY |
| T11 | **Fake win**: the hero shakes off what was really the warning | B12 | TRUCKER-RULES |
| T12 | **Protective object becomes the victim**: the talisman is shown damaged or changed | S9 | BciSW_2VMZg |

Rule: **close one loop and open a bigger one within ~5 s** (HEARSE-P2 does this at every act break).

### 4C. Endings and CTAs

None of the 12 has a spoken subscribe. Endings, ranked by how often they appear:

1. **Hard cut at the point of greatest need**: a new imperative from an unknown sender, the possessed companion asking for control, the expert naming the entity with no remedy. (SIEGE-CHAT, HEARSE-P1, HEARSE-P2, FLOOR-PHRASE)
2. **New rule from a new authority**, mirroring the old fake authority's phrasing so the ally is suspect too. (DORM-RULES)
3. **Enemy eavesdrop**: the villains' plan converges on the hero, followed by a "full ending" CTA at peak danger. (SIEGE-OVERLAY)
4. **Soft landing plus a forbidden next document**: episode-count stakes ("make it to day [N+1]"), then a to-be-continued card. (MOM-NOTE)
5. **Threat turned on "you"**, trailing off with an ellipsis. (TEXT-FIGURE)
6. **Brand sign-off plus a signal-lost card**, with the CTA written as broadcast copy. (CLASSMATE-PSA)
7. **Blur plus a "full story ↓" card**. (FARM-FLASHFWD)
8. **Fake win plus a lingering aftermath image**. (TRUCKER-RULES)
9. **Standalone**: "never forgot it", plus a **silent visual sting** that returns to the opening place with an ambiguous figure. (HOTEL-DOOR)

The last shot repeats the first shot in HEARSE-P1, CLASSMATE-PSA and HOTEL-DOOR.

Avoid:
- a mid-sentence cut **with no part label** (udhwkz control, 0.77×);
- an app-download funnel line as the ending (mraevq control, 1.06×);
- jump-scare-only endings.

### 4D. Open loops

- Median **2.9 opened per minute** (1.5–8.0). Stories run 1.5–3.6/min; 60 s Shorts run 6–8/min.
- Micro loops close in **2–10 s**. The main loop closes in B10–B11.
- **3–6 loops stay open at the end** (median 4.5).
- Standalones close most of them: DORM-RULES closes 6 of 8, and HOTEL-DOOR closes all of them and re-opens one with a visual sting.

Loop types that recur:
- what happens if the rule breaks
- is the authority real
- who is watching
- what is the unnamed "it"
- the companion's odd look
- the planted object
- will the lifeline work

---

## 5. Series / Part-2 mechanics

- **Sequel decay is steep.** Part 2 got **16%** of Part 1's views (HEARSE-P2 vs P1). TopScaryClips' part 3 got **8%** of part 2 (41K vs 498K). WrONG Rules posted Pt2 and Pt3 on the **same day**: Pt2, which opens mid-list, got 1.0×; Pt3, which opens on an urgent hook, got 11.0×. **Each part must hook cold viewers in ≤3 s** as if it were a pilot.
- **Post order:** upload Part 2 first, then Part 1 a few seconds later, so Part 1 sits on top of the profile grid (udhwkz did this 9 s apart).
- **Plant for the next part:** ≥2 unpaid specifics (an ID, a number, a stated statistic) in Part 1. Pay one by ~45% of Part 2, then open a bigger loop.
- **Label:** "Part 1", "Day 1" or "(Pt[N])" in the title, plus episode-count stakes in the last line (MOM-NOTE). TikTok repost accounts use recurring character-name hashtags so a series can be binged (mraevq).
- **Cut point:** cut at the highest danger with one new imperative or diagnosis. Close the early loops so the viewer feels paid, and leave every loop opened after 50% open.
- **Standalone is fine:** HOTEL-DOOR (1.52M) and DORM-RULES close most loops and still leave one survival or trust question open.

---

## 6. Outliers vs ordinary

Same channel, same art, same voice:

| Pair | Hit | Control | What the hit does that the control doesn't |
|---|---|---|---|
| **@udhwkz** | HEARSE-P1 63×, TRUCKER-RULES 20×, FLOOR-PHRASE 18×, SIEGE-CHAT 11× | 7696062340852190496, 0.77× (dead body on a train) | Same title, same 364 wpm, similar numbers per minute (4.3 vs 3.6–5.8). The control's **words** are as dense; its **events** are not. It has a 30 s theory monologue and a 40 s stretch with no new threat. Its premise is a generic body, not an ownable rule or trigger. Its cover frame shows no visible threat. It cuts mid-sentence with no part promise. |
| **@mraevq** | SIEGE-OVERLAY 67×, 7664930759395888416 40×, 7666044652910316833 30×, DORM-RULES 18× | 7665304797242821921, 1.06× (fog creature on a train) | The control's hook is decent: a monster sighting and a parent's fear. But **nothing contradicts a trusted source in the first 10 s**, its jolts come every 30–45 s (vs 11 s and 4 s in the hits), and it ends on an app-download funnel. |
| **WrONG Rules** | MOM-NOTE 31×; BciSW_2VMZg 11× | xKgepVHATm4, 1.0× | **A natural experiment.** The control is essentially MOM-NOTE's last 75 s (the same rules) re-posted as "Pt2" with no hook: no addressee, no stakes, no lifeline line, no setup, no talisman. 9.4K views vs 291K. Its same-day sibling BciSW_2VMZg opens on an urgent presupposing order and got 11×. **The first 10 s is worth about 10–30×.** |
| **Wansee** | HOTEL-DOOR 9× (1.52M) | epzTfKxp16E, 1.16× | The hit's title states the incident, so the slow setup reads as irony. The control's title is a vague clock time, its first wrongness comes at 25 s, it runs 311 s, and its jolts come every 15–20 s (vs a 6.5 s median). |
| **Chat Shorts vs long chat** | TEXT-FIGURE 25.5×, FARM-FLASHFWD 10.4× (60 s) | Texty Stories 0xzpKw7To98, 1.03× (13:45) | The hits put a bubble every 1.1 s with a jolt every 2.5–3.5 s. Long chat stories put a jolt every 40–60 s, with time-skip cards about every 200 s. Keep chat horror at 60 s. |

**Stat check** (`tools/pacing_stats.json`, hits = the 12, controls = the 7 at about 1×):

| Metric | Hits median | Controls median | Reads as |
|---|---|---|---|
| words/min | 254 | 213 | **No signal** within a channel: the udhwkz control is at 364 |
| numbers/min | 3.6 | 2.0 | weak plus: hits name more counts, distances and times |
| questions/min | 3.3 | 3.6 | no signal |
| % sentences with "you" | 14.5 | 13.4 | no signal (it depends on the format) |
| sentence median (words) | 7.5 | 8.0 | no signal |
| words in the first 10 s | 43.5 | 38 | small |
| **jolt interval** | **6 s** (2.5–11) | **15–45 s** (library teardowns) | **strongest signal** |
| **first contradiction of a trusted source** | ≤ 11 s (6 of 7 narrated hits) | 25 s or never | **strong** |
| longest dry stretch | median 17.5 s, max 27 | 30–45 s | **strong** |

**Bottom line:**
- **Event density beats word density.** Every 6 s something new is wrong.
- **The trusted thing is contradicted inside 10 s.**
- **There is a rule the viewer can count against.**
- **The cover frame (frame 0) shows the threat.**

Speeding up the TTS did not save the udhwkz control.

---

## 7. Pacing stats

From `tools/pacing_stats.py` over the 12 corpus transcripts. Chat bubbles count as sentences. "Jolt" and "loop" counts come from each annotated file.

| Stat | Median | Range | Notes / target for our scripts |
|---|---|---|---|
| **Words/min** | **254** | 144–389 | By format: translated narrated TikTok **281** (208–389; the TTS is sped up about 1.3–1.5×), English-native YouTube **160** (144–179), chat Shorts **260** (245–274). **Our target:** narrated story at 230–270 wpm (Kokoro at about 1.2–1.3×), rules or broadcast at 145–180, chat at 250–275 read speed. |
| **Hook length** | **27 words / 6 s** | 5–57 words / 1–14 s | Core hook ≤ 6 s and ≤ 30 words; extended hook to the first turn ≤ 14 s |
| Words in the first 10 s | 43.5 | 24–80 | — |
| **Sentence length** (median of medians) | **7.5 words** | 4–12 | Mean 9.6. Narrated: 5–12-word lines broken up by 3–5-word verdict lines. Chat: 4–5 words per bubble, max 9. |
| Punch lines (≤4 words) | 18% of sentences | 2–55% | Chat 49–55%, rules 20–24%, narration 13–22%. Put one at every spike. |
| **% sentences with second person** | **14.5%** | 2.7–39 | By format: first-person narrated stories 3–13% (the "you" lives in dialogue or a generic "you never"); dialogue-heavy 16–28%; rules or broadcast **28–59%** (CLASSMATE-PSA has no "you" before 20%, then it dominates after the turn) |
| "you" per 100 words | 2.0 | 0.2–5.9 | first person ("I/me/we") per 100 words: 6.2 |
| **Numbers per minute** | **3.6** | 0–5.8 | Narrated stories 4.1 (2.2–5.8): distances, counts, room numbers, clock times, battery seconds. Chat 0–1. |
| Rhetorical questions per minute | 3.3 | 0–11.6 | Inner-monologue engines run 4–12 |
| Rule / prohibition words per minute | 1.65 | 0.4–7.4 | Rules formats 4–7.4 |
| **Jolt (re-hook) interval** | **6 s** | 2.5–11 | Shorts 2.5–3.5; stories 4–11 |
| Longest dry stretch | 17.5 s | 5–27 | Cap at 25 |
| **Open loops per minute** | **2.9** | 1.5–8.0 | Stories 1.5–3.6; 60 s Shorts 6–8 |
| Loops open at the end | 4.5 | 0–6 | Series 3–6; standalone 0–2 |
| Cut / picture change | 2–3 s | 1–6 s | — |
| Biggest twist position | ~89% | 55–98% | — |
| Scariest image position | ~67–78% | 47–82% | — |
| Cliffhanger block | ~5% | 1–10% | — |

Per-source rows: `INDEX.json` (wpm, hook, jolt, loops) and `tools/pacing_stats.json` (all lexical stats, plus the alternates, the extra hits and the controls).

---

## 8. Writer checklist (every box must be ticked before TTS)

**Premise**
- [ ] One **ownable rule, trigger or signature** (a sign that announces the threat, a forbidden act, an exact count) that the viewer can track. A generic monster or a generic body is not enough.
- [ ] Set at a **barrier the viewer knows**: a door, a phone or chat, a car, a bed, a classroom, a hotel room.
- [ ] Original story, names, numbers and setting. Not any of the corpus premises (`<id>.md` §3 lists what not to reuse).

**First 10 seconds**
- [ ] Line 1 (≤12 words) names a concrete place or object plus a danger or rule. The threat is visible in frame 0, which is also the cover.
- [ ] Core hook ≤30 words and ≤6 s. A trusted source (official chat, authority, rule, guardian) gets **contradicted by ≤11 s**.
- [ ] No intro, no greeting, no channel name (an ident is fine only in the broadcast format). Never open mid-list or mid-scene.

**Body**
- [ ] A jolt at least every **8 s** (median target 6 s). Nothing dry for more than **25 s**, and only once (the lull, ≤25 s, placed at 40–50%).
- [ ] At least 2 rules or warnings stated, at least 1 broken; one of them is a "remember this" plant that pays off later.
- [ ] Two escalation ladders running together (for example proximity and channel removal), switching whenever one stalls. Every rung removes a safe channel or brings the threat closer.
- [ ] ≥2 hyper-specific plants (an ID, a room number, a count, a colour, a time), with at least one paid off inside the video.
- [ ] A viewer-proxy voice (a companion, the chat, the listener) speaks the objections and gets answered or shut down.
- [ ] Numbers: about 3–5 per minute in narrated stories (distance to help, minutes, battery seconds, counts).
- [ ] Midpoint turn at 45–60%. The scariest image appears **once**, at 60–80%, and holds still for about 4 s.
- [ ] A lifeline under a clock (a battery, a call, a deadline) somewhere in 70–90%.
- [ ] The truth twist lands at 85–95% and reframes an authority, a helper or a "safe" object.

**Ending**
- [ ] Hard cut at the moment of greatest need, a new rule from a new authority, or a threat turned on "you". The last shot bookends the first.
- [ ] Early loops closed before 50%. 3–6 loops open at the cut for a series, 0–2 for a standalone.
- [ ] No spoken subscribe or app funnel. For a series: a part label in the title or card, plus ≥2 unpaid plants. Post Part 2 first.

**Pacing**
- [ ] wpm on target for the format (§7). Sentence median 6–9 words, plus 3–5-word punch lines at the spikes.
- [ ] Second-person share on target for the format (narrated 5–15%, rules or broadcast ≥30% after the turn).
- [ ] 1–3 timed silences (3–8 s with SFX) marked in the script for the TTS.

**Paperwork**
- [ ] Front matter `references:` 2–3 corpus ids with url, views and outlier_score, plus a beat-alignment table (our beat → B/S tag → reference timestamp → device borrowed).
- [ ] `scripts/originality_check.py` prints PASS.

---

## 9. Study these three first

1. **7702661541224566049 (HEARSE-P1, 2.2M, 63.1×)**: the cleanest **full skeleton**.
   - A rule in the first second.
   - A minor rule broken before it is stated.
   - A stranger's ritual, then its explanation, then the trusted companion mirroring it.
   - A false close, then a contradiction, then the cliffhanger with a bookend shot.
   - Read with its sequel HEARSE-P2 for series mechanics and the 16% sequel decay.
2. **7654526047005723937 (SIEGE-OVERLAY, 717K, 66.7×)**: the **exact target format** for our phone-chat kit.
   - The building chat's all-clear, a knock, then an omniscient contradiction, all by 7 s.
   - Three channels (door, chat, call) take turns.
   - A 30 s battery call at the midpoint, a double twist, then the villain-eavesdrop cliffhanger.
   - Pair it with the tighter 249 s cousin **7659677578365537569** (SIEGE-CHAT) for the count-match device and 3–5 s jolts in the last third.
3. **T42u5xhrq-0 (TEXT-FIGURE, 869K, 25.5×)**: the **60 s chat Short** timing reference.
   - A bubble every 1.1 s, a turn at 50%.
   - The CAPS typography ladder, the silence beat, one image at 90%, then the voice swap onto "you".

**Runner-up for the cheapest build:** **cVUJmsVkUW4 (MOM-NOTE, 31×)**, the rules-note format with title cards and colour keywords. Read it next to its hookless 1.0× re-cut xKgepVHATm4 to see what the hook is worth.
