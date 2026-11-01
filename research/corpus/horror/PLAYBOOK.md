# Horror PLAYBOOK: viral skeleton, devices, pacing

Built 2026-11-01, about 09:05 UTC, from the 12 annotated scripts in this folder (`<id>.md`, `raw/<id>.txt`, `SOURCES.md`), the 4 alternates in `raw/_alt/`, and **controls** from `research/library/` (horror videos at or near their channel median, with transcripts in `research/library/transcripts/` and teardowns in `research/library/videos/<id>.json`).

**Revised about 12:40 UTC with the expansion** (SOURCES.md "Expansion"): 12 more annotated outliers and 1 same-template control (FDLk6TlVTq0). The corpus is now **24 outliers + 8 controls**. All medians in §2, §3, §6 and §7 are recomputed over the full set; where the first 12 and the expansion disagree, both are shown. The changes are summarised in §10.
- Machine-readable index: `INDEX.json` (25 rows; `batch` = original12 | expansion, `role` = outlier | CONTROL). Each `beat_sequence` there uses the B1–B12, S1–S10 and P2 tags from §1.
- Pacing numbers come from `tools/pacing_stats.py` (output `tools/pacing_stats.json`; it now also writes `summary.corpus_orig12` and `summary.corpus_expansion`), not from memory. Re-hook and open-loop counts come from the tables in each annotated file.
- Lexical caveat: 8bo9yZvedUM and 02nCBx8WqW0 are unpunctuated auto-subs and x--ui6_mAxE is one sentence, so they are left out of the sentence-level medians (sentence length, punch lines, % "you" sentences, questions). 6WfCF7KsLaQ and 02nCBx8WqW0 open on a silent title card, so they are left out of "words in the first 10 s".

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

**Expansion outliers** (added 12:08 UTC; all but one from channels not in the first 12):

| id | short name | fmt | dur | views | outlier |
|---|---|---|---|---|---|
| wh9ESTS69Dk | DEAD-CHILD-TEXTS (Texty Stories) | silent chat recording | 6:18 | 249K | **165.8** (vs a 1.5K median: a channel breakout, not a format win) |
| 8bo9yZvedUM | HOME-ALONE-READALONG (Luke Davidson) | host reads a chat aloud | 10:21 | 16.2M | **34.1** |
| 7650872317119057168 | FAKE-ROOMMATE (@melovebz) | narrated story, "full story" compile | 9:26 | 134K | 23.8 |
| gDNMSoGSZgQ | DOG-RULE (The Story Vault) | narrated Short | 0:59 | 20K | 19.8 |
| kJCVK8xTkPk | TWO-WINDOWS (Resident Guidance) | rules guidance, 16:9 | 5:14 | 13K | 17.4 |
| 7659482056656735521 | TWO-SUSPECTS (@lehwh7) | narrated story, complete episode | 9:45 | 1.9M | 11.2 |
| x--ui6_mAxE | BACKSEAT (Wansee Short) | 15 s micro-story | 0:15 | 142K | 9.5 |
| shTJ7_kRNJ8 | NIGHT-BUS (NightProtocol) | rules story, 7 chapters, 16:9 | 10:33 | 3.2K | 7.6 (1 day old) |
| 02nCBx8WqW0 | APP-STALKER (Llama Arts) | animated true story | 4:46 | 11.9M | 6.4 |
| 6WfCF7KsLaQ | VIDEO-CHAT-GAME (Horror Shorts Party) | narrated true story + chat UI | 5:25 | 1.28M | 5.1 |
| hPWu7UAovxk | TEXTS-THEN-BACKSTORY (Mr. Nightmare) | narrated anthology of 3 | 9:21 | 5.0M | 5.0 |
| cWgSgd-QcOY | HAUNTED-HOUSE-LIST (Lighthouse Horror) | snarky rules listicle | 22:06 | 505K | 2.6 |

The **controls** used in §6 are videos at about 1× their channel median, mostly from the same channels. The expansion added **FDLk6TlVTq0** (Resident Guidance, 5:35, 1.4×, PIGEONS), the same narrator, kit, length and five-rule template as TWO-WINDOWS, which makes it the cleanest pair in the corpus.

| id | channel | dur | outlier |
|---|---|---|---|
| 7696062340852190496 | @udhwkz | 2:48 | 0.77 |
| 7665304797242821921 | @mraevq | 7:02 | 1.06 |
| xKgepVHATm4 | WrONG Rules | 1:00 | 1.00 |
| epzTfKxp16E | Wansee | 5:12 | 1.16 |
| KJfJKo400b0 | twezed | 9:56 | 0.94 |
| dqEIz_8bP-8 | lehwh7 | 11:01 | 1.01 |
| 0xzpKw7To98 | Texty Stories | 13:45 | 1.03 |
| FDLk6TlVTq0 | Resident Guidance | 5:35 | 1.41 |

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

The expansion (24 outliers) keeps this paragraph. Two qualifiers:
- **The title can carry the hook** on YouTube. Then the threat may arrive as late as 31–48% *if* the setup has its own engine: a bribe auction, a comic stranger, a sympathy reversal (8bo9yZvedUM, 02nCBx8WqW0, 6WfCF7KsLaQ). Those are 5–6× hits, apart from the host-led 34× one. Our narrated pilots should still contradict by 11 s.
- **The first 30 s decide more than the middle.** TWO-WINDOWS (17.4×) and its same-template control PIGEONS (1.4×) have the same cadence. The control's middle is even denser in threat beats. The outlier shows the impossible thing by 0:10 and makes "you" act in it; the control spends 28 s on a normal baseline.

---

## 1. Canonical viral skeleton

The corpus has three lengths:
- **Shorts**: 15–100 s, chat, rules, broadcast or a narrated folk-rule story. The 15 s BACKSEAT is the floor: one place, two people, one transformation.
- **Story**: 150–360 s narrated TikTok / YouTube "long-form" for this niche, with a sweet spot of 165–250 s.
- **Long**: 9–11 min, either a *complete* episode (FAKE-ROOMMATE, TWO-SUSPECTS, both ending on "the end") or a chaptered format (NIGHT-BUS's 7 rules, TEXTS-THEN-BACKSTORY's 3 stories, HOME-ALONE-READALONG's host). Outlier medians are about the same in every length bucket: ≤100 s 18.6× (n 5), 100–300 s 17.6× (n 9), 300–700 s 17.4× (n 9). The single 22-min hit is 2.6×.

The 10–20 min library uploads at ~1× (twezed, lehwh7, Texty Stories) show what happens when the story skeleton is stretched without the micro cadence. The expansion's 9–11 min hits keep a 6–9 s median jolt. See §1C.

### 1A. Story (150–360 s): beats B1–B12

% values are medians across the 10 narrated or rules stories of the first 12, with ranges in brackets; the expansion's 11 stories and long videos are folded into the ranges and exemplars (bold ranges changed with the expansion). The seconds columns use a **3:00** cut (180 s) and a **6:00** cut (360 s). The hook is capped in absolute seconds, not scaled.

| # | Beat | % of runtime | s @180 | s @360 | What happens | Exemplars |
|---|---|---|---|---|---|---|
| B1 | **Hook: threat + rule or false safety** | 0–5% (2–7) | 0–6 (≤9) | 0–6 (≤14) | Line 1 puts a danger in a place the viewer knows, or states a taboo as common knowledge. Lines 2–3 add a reason or an official all-clear that will be undercut. Median **27 words / 6 s**. The threat is visible in frame 1. No intro, no title card, no greeting. | HEARSE-P1, SIEGE-CHAT, SIEGE-OVERLAY, TRUCKER-RULES, FLOOR-PHRASE, DORM-RULES |
| B2 | **Rules / false safety laid down** | 3–10% (2–17) | 5–18 | 10–36 | The world's law gets spoken: a mentor's maxim, a numbered list, an official "it's over", a protective ritual with "remember this". The rules become Chekhov's guns; the viewer starts counting violations. | TRUCKER-RULES, HEARSE-P1, DORM-RULES, MOM-NOTE, SIEGE-CHAT |
| B3 | **Intrusion at the barrier** | lands at **~6%** (**0–48**; title-carried YouTube true stories 31–48%) | ~11 | ~20 | A knock, a stranger, a rule broken, a trigger spoken. The threat is now at *my* door or inside *my* space, often dressed as help (police, staff, a supervisor). The hero nearly complies. | SIEGE-OVERLAY (5 s), FLOOR-PHRASE (3 s), SIEGE-CHAT (11 s), TRUCKER-RULES (10 s), DOG-RULE (rule broken by 10 s), NIGHT-BUS (11%), HOTEL-DOOR (45 s, the title carries it), APP-STALKER (31%), VIDEO-CHAT-GAME and HOME-ALONE-READALONG (48%) |
| B4 | **First proof: the trusted thing is wrong** | 8–20% (2–28) | 15–36 | 30–72 | A countable clue (N marks equals N confirmations), an omniscient overlay, a radio report that matches, or a rule that backfires on the first try. The viewer now knows more than the neighbours. | SIEGE-CHAT (11%), SIEGE-OVERLAY (2%), TRUCKER-RULES (17%), DORM-RULES (9%), FLOOR-PHRASE (25%) |
| B5 | **Pressure ladder** | 15–45% | 27–81 | 54–162 | 3–6 rungs, one every ~8 s (physical rungs ~3 s). Each rung removes a safe channel or brings the threat closer. A companion speaks the viewer's objections and gets shut down. Each rung ends on a 3–5 word verdict line. | SIEGE-CHAT, SIEGE-OVERLAY, HEARSE-P1 (ritual), FLOOR-PHRASE, HOTEL-DOOR (door ladder) |
| B6 | **Isolation** | 40–55% (16–66) | 72–99 | 144–198 | Signal gone, help far away (give a number: km, minutes), the ally silenced or muted. Often only the enemy's channel still works. | SIEGE-CHAT (49–61%), SIEGE-OVERLAY, FARM-FLASHFWD, HOTEL-DOOR |
| B7 | **Lull + plant** (≤ 20–25 s) | 40–50% | 72–90 | 144–180 | The only breather. A hidden face, a quiet car, a kindness; plant the object, charm or phone that saves or betrays later. **The weakest stretch in every source.** Keep it under 25 s and give it one foreshadow line. | HEARSE-P1 (45–50%), TRUCKER-RULES (31–45%, too long), SIEGE-OVERLAY (43–51%), FLOOR-PHRASE |
| B8 | **Midpoint turn** | 45–60% (**42–53%** in the expansion) | 81–108 | 162–216 | The frame flips: a personal link to the threat, a rule inverted, the "monster" turns out to be the real expert, or "not him, but what's in him". | DORM-RULES (50–63%), HEARSE-P1 (50%), HEARSE-P2 (55–65%), TEXT-FIGURE (50%), CLASSMATE-PSA (43%), FAKE-ROOMMATE (42%, counter-accusation), NIGHT-BUS (52%, the pre-announced rule pays), TEXTS-THEN-BACKSTORY (53%, wrong sender) |
| B9 | **Peak contact** | starts at **~70%** (**41–95**), runs 60–80% | 108–144 | 216–288 | A sensory or physical hit: a touch, a mirror ritual, an assault, eyes in the safe place. **One** scariest image, held still for ~4 s. Every story in the pool puts it after 45%. | HEARSE-P1 (67–78%), FLOOR-PHRASE (61–74%), MOM-NOTE (76–82%), SIEGE-OVERLAY (72%), HOTEL-DOOR (68–80%), FAKE-ROOMMATE (70%), TWO-WINDOWS (68%), TWO-SUSPECTS (69%), APP-STALKER (66%), HAUNTED-HOUSE-LIST (77%). Outliers: DEAD-CHILD-TEXTS puts its only image at 41% (an *empty* doorway), DOG-RULE its grin at 95% |
| B10 | **Lifeline under a clock** | 72–90% | 130–162 | 259–324 | A left-behind phone, a 30 s battery, the real authority on a failing line, or a call to family. Ask the viewer's questions out loud and get answers in rising order. | SIEGE-CHAT (80–97%), SIEGE-OVERLAY (31–43% in the 6-min cut), FLOOR-PHRASE, HOTEL-DOOR |
| B11 | **Truth twist** | lands at **~88%** (**53–98**) | ~160 | ~320 | The authority never existed, one killer is really a crew, a private fact contradicts the companion, the helper betrays, the victim's own number answers as the entity, or (after safety) it was worse than you knew. | SIEGE-CHAT (90–96%), HEARSE-P1 (93%), FLOOR-PHRASE (98%), TEXT-FIGURE (93%), HOTEL-DOOR (88%), DORM-RULES (59%, early variant), DEAD-CHILD-TEXTS (94%), TWO-WINDOWS (98%), TWO-SUSPECTS (86%), HAUNTED-HOUSE-LIST (87%); compiled "full stories" twist earlier and twice (FAKE-ROOMMATE 76% then 86%) |
| B12 | **Cliffhanger / sign-off** | last **~5%** (1–12) | 171–180 | 342–360 | Cut at the moment of greatest need: a new imperative from an unknown sender, a new rule from a new authority, a diagnosis with no remedy, the possessed one asking for control. The final shot bookends the opening shot. Only a "part" or "full story" card, never a spoken subscribe. | all 12; complete long episodes close instead (FAKE-ROOMMATE, TWO-SUSPECTS) |

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

**Expansion: what the 9–11 min hits add.** Five more long hits (5–34×) confirm that the micro cadence is what survives length. Their median jolts are 6–9 s, set against 15–45 s in the long controls. They also show three chassis that make 10 minutes skimmable:
- **Swinging master loop** (FAKE-ROOMMATE, TWO-SUSPECTS): one "who is the monster" question flips every 30–70 s (8–10 swings). Two suspects accuse each other and each gives the hero a talisman. A third-party online helper supplies the rules and turns out to be compromised.
- **Numbered chapters** (NIGHT-BUS, HAUNTED-HOUSE-LIST): a rule every 63–75 s, shown as YouTube chapters. Each rule runs header → why instinct fails → anomaly → sub-rule → consequence → a case-file sting. Then a hard cut into the next header, so a scare is never followed by a lull. Pre-label the failure rule early ("remember rule four") and put the mid-roll comment CTA just before it.
- **Anthology with a count** (TEXTS-THEN-BACKSTORY): announce N stories and order them by twist size, not by violence. A "this last one" line is its own re-hook. A moral after each story gives a breath about every 3 min.
- The 22-min HAUNTED-HOUSE-LIST is the weakest ratio (2.6×), with a 12.5 s median jolt and a 48 s lull. Past about 11 min the corpus has no strong hit.

### 1D. Story engines

All thirteen engines share the skeleton but weight different beats (the last five came with the expansion).

| Engine | Spine | Beats it stretches | Sources |
|---|---|---|---|
| **Locked-door siege** (fake authority + compromised group chat) | a door the hero must not open; three channels (door, chat, call) each confirm the twist from a different side | B4 count-match, B5 chat replay, B10 countdown call | SIEGE-CHAT, SIEGE-OVERLAY |
| **Taboo rule broken** (job or folk rule) | rules stated in the hook; a stranger breaks one; the trusted companion mirrors it | B2, B5 ritual, B9 mirror | HEARSE-P1/P2, TRUCKER-RULES |
| **Forbidden ordinary phrase** | one polite act, used 4–6 times; each reactor is closer to the hero and costs more | B3 repeated, B10 oracle | FLOOR-PHRASE |
| **Two rival authorities** | the rules that are supposed to protect backfire; the "monster" is the real expert | B2 twice, B8 rule inversion, B11 evidence | DORM-RULES |
| **Rules note** (absent guardian, second-person imperatives) | the list *is* the story; if/then branches; at least two planted contradictions | B2/B5 merged, two peaks (35–42%, 75–82%) | MOM-NOTE, BciSW_2VMZg |
| **Broadcast PSA** | third-person lore, then "in your [place]" at ~45%, then rules | S3 symptoms, S6 turn | CLASSMATE-PSA |
| **Chat thread** | you hold the listener's phone while the horror happens elsewhere | S7 ladder, S10 voice swap | TEXT-FIGURE, FARM-FLASHFWD |
| **True-story confession** | the title states the incident; cozy setup works as irony; a door ladder (or a **contact-channel ladder**: each block is beaten faster, with the same notification line as a sting); a retro-reveal after safety | B2 long, B5 door/channel ladder, B11 after rescue | HOTEL-DOOR, APP-STALKER, VIDEO-CHAT-GAME |
| **Suspect hunt with an online helper** | a stranger-expert gives one checkable tell in the hook; the tell fires on suspect 1, then suspect 2, then the narrator or the helper | B2 rules from the helper, B8 counter-accusation, B11 knowledge slip | FAKE-ROOMMATE, TWO-SUSPECTS |
| **Cold-open anomaly + procedure** (second-person guidance) | show the impossible thing by 0:10 and make "you" act in it; numbered rules pinned to one continuous evening; the longest rule is the closest contact; the bonus rule replays the open from the other side | B1 scene, B5 one rule per 36–66 s, B11 inversion at 98% | TWO-WINDOWS, NIGHT-BUS (control: PIGEONS) |
| **Texts first, context second** | read the raw thread cold, stop on a cliff marker, then retell the same minutes from outside the phone | B4 cliff marker, B8/B11 reversal in the retelling | TEXTS-THEN-BACKSTORY |
| **Haunted person's own phone** (grief chat) | the viewer holds the victim's phone; a polite, pleading voice; the living person shouts; a second thread brings a sceptic; the evidence erases itself | S6 at the door, S8 silence, S10 vanished thread | DEAD-CHILD-TEXTS (and HOME-ALONE-READALONG for the protector-away variant) |

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
| H13 | **[Title rule] as line 1 → a present-tense scene of [an impossible duplicate] by 0:10 → "you" do the act → a one-word sting → "[N] rules"** | Show the wrongness, make the viewer complicit, then offer procedure as the lifeline | TWO-WINDOWS 13K, 17.4× (its baseline-first sibling PIGEONS got 1.4×) |
| H14 | **[Shocking custom]. There is one rule: [rule].** → the rule is broken by 10 s | H1/H2 compressed for a Short: rule, then violation, then the rest is punishment | DOG-RULE 20K, 19.8× |
| H15 | **[Exact hour] + [ordinary noise] for [N] nights → I ask online → a stranger names it + quotes one checkable tell** | A countable pattern, then an outside expert whose rule becomes the engine (and later the twist) | FAKE-ROOMMATE 134K, 23.8×; TWO-SUSPECTS 1.9M, 11.2× |
| H16 | **Lock-screen notification from an unknown sender → "who is this" → it claims to be [dead close person]** | Phone-native, silent, and the viewer holds the victim's own phone; grief instead of threat | DEAD-CHILD-TEXTS 249K, 165.8× |
| H17 | **Spoil the event and the hour, withhold who and what happens** ("someone breaks in at [time]"; "spoiler: he's dead") | Buys a long non-horror setup, if that setup has its own engine | HOME-ALONE-READALONG 16.2M, 34.1×; HAUNTED-HOUSE-LIST 2.6× |
| H18 | **Title spoken as a rule + three escalating don'ts + "even if [friend] does"**, then a second hook: **"[N] rules; remember rule [K]"** | Premise and main loop stated by 15 s; the pre-announced failure point carries the first half | NIGHT-BUS 3.2K in 1 day, 7.6× |
| H19 | **"[N] [threads], each scarier with [context]"** | A format promise with a count works as a progress bar | TEXTS-THEN-BACKSTORY 5.0M, 5.0× |
| H20 | **A persistent caption: "[kind act], but she was…"**, on screen in every frame | The open loop is literally visible; the narration only has to close it | BACKSEAT 142K, 9.5× |

**Combination rule seen in every hit:** a **place the viewer knows** + a **rule or official reassurance** + a **contradiction from a source the hero can't dismiss**, all inside the first 10 s.
- The two top narrated outliers (SIEGE-OVERLAY 66.7×, HEARSE-P1 63.1×) both contradict their own opening line by 5–7 s. The expansion's strongest hooks do the same with a scene: TWO-WINDOWS shows the impossible double by 0:10, and DOG-RULE breaks its rule by 0:10.
- Hook length over all 24: median **26 words / 8 s** (range 5–79 words, 1–15 s). The first 12 alone: 27.5 words / 7 s; the expansion: 25 words / 8 s. Median **42.5 words** spoken in the first 10 s (8–80).
- The weak hooks in the expansion are all YouTube uploads whose **title** does the work: APP-STALKER and VIDEO-CHAT-GAME open on a 7–10 s silent title card, and HAUNTED-HOUSE-LIST takes 64 s. They are the lowest ratios in the set (2.6–6.4×).
- **Never** open on atmosphere alone, mid-list, or mid-scene for cold viewers.

---

## 3. Re-hook cadence

| Layer | Shorts (60 s) | Story (150–360 s) |
|---|---|---|
| New bubble, caption or spoken line | **~1.1 s** per bubble (TEXT-FIGURE, FARM-FLASHFWD); the chat panel resets every 6–9 s | a caption card every ~2 s (1.4–2.4 s) |
| Picture change | the panel reset or pictogram every ~3 s | a cut or punch-in every **2–3 s** (TikTok dubs); 3–6 s (YouTube 16:9) |
| **Jolt** (a new anomaly, a rule, a question, a "just then", a number, a notification) | median **2.5–3.5 s**; 4–5 s in the first half, 1.5–2 s in the second. Narrated Shorts run faster still: DOG-RULE 2 s, BACKSEAT 1.7 s | median **6.5 s** across all 24 (range 1.7–16). First 12: 6 s; expansion: 8 s; the 9–11 min hits hold 6–9 s. It tightens to 3–5 s in the last third (APP-STALKER and HOME-ALONE-READALONG drop to 3–8 s and 4–5 s at the siege) |
| Longest dry stretch allowed | ≤ 5 s (DOG-RULE max 6.5 s) | observed median **19.5 s** over all 24 (first 12: 17.5 s, max 27). The expansion's longer gaps are a host aside (39 s), placed listicle lulls (42–48 s) and the silent chat's 54 s. **Target unchanged: ≤ 25 s, once** |
| Rhetorical question | — | every ~4–5 s in inner-monologue engines (FLOOR-PHRASE: 35 questions in 166 s) |
| Master question restated in fresh words | — | every 20–30 s (FLOOR-PHRASE 5×, DORM-RULES 2× during the wait); in long whodunits the *answer* swings instead, about every 30–70 s (FAKE-ROOMMATE 8 swings, TWO-SUSPECTS 10) |
| Channel or format switch (narration ↔ chat ↔ call ↔ overlay ↔ title card) | — | every 30–40 s; title cards every 10–15 s in the rules format; a numbered rule chapter every 36–75 s in guidance and long rules videos; a helper-channel return every 60–80 s in the suspect-hunt engine |
| Big jolt / set piece | every 12–20 s | every 30–60 s (long-form) |
| Silence as a re-hook | 1 beat (unanswered name checks) | 1–3 beats of 3–8 s with SFX (HOTEL-DOOR's knock; FLOOR-PHRASE's dead air before the kicker) |

**Hard cap:** never go **>25 s** without a jolt. The two weakest stretches in the corpus are TRUCKER-RULES' 23 s lull and HEARSE-P1's 24 s explanation. The udhwkz control's 30–40 s stall is the thing it does worst (§6).
- The expansion's longer dry stretches all sit in formats we are not copying: a host who is the attraction himself, a 22-min listicle, or a silent chat whose 166× is against a 1.5K median.
- PIGEONS (1.4×) has a 28 s jolt-free *opening*. That is the one place a gap is fatal.
- **Teaser lines** ("that's when…", "something I'll never forget") are a cheap way to bridge a gap: they announce a shock 2–4 s before it lands (VIDEO-CHAT-GAME, 6 uses).
- **Cliff markers** ("this is where the texts ended") freeze a loop and promise its other side (TEXTS-THEN-BACKSTORY).

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
| **Typography** (chat) | normal → ALL CAPS → broken lowercase → calm sentence case from the entity (the scariest register). Inverted: the *living* person shouts while the entity stays polite, and the entity's single caps line lands at ~59% | TEXT-FIGURE, FARM-FLASHFWD, DEAD-CHILD-TEXTS |
| **Contact channel** | add → message → remove → faster message → block → new account, faster again → a photo of my house → the window | APP-STALKER |
| **Odds** | 1 in 6 → proof it is real → 5 in 6 | VIDEO-CHAT-GAME |
| **Social stakes** (no danger yet) | threat to tell a parent → bribe → higher bribe → deal; it carries 46% of the runtime, then the distance ladder takes over | HOME-ALONE-READALONG |
| **Inward** | hallway → the family → the hero's own mind (nested dreams he cannot exit) → the one outside helper | TWO-SUSPECTS, FAKE-ROOMMATE (the narrator) |
| **Reality descent** | seen → denied by a witness → evidence erased | DEAD-CHILD-TEXTS |
| **Case-file costs** | each rule's case file comes from a more official source with a worse cost (student → company → city) | NIGHT-BUS |
| **Rule closeness** (guidance) | each rule moves the threat one step: street → step → count → lift → your floor → your sill → you | TWO-WINDOWS, PIGEONS |

Rung spacing: physical rungs ~3 s apart, supernatural or information rungs ~15 s apart. Plant every rung that pays off later as a hyper-specific detail: a plate, a room number, a count, a colour.

### 4B. Twist / payoff patterns

| # | Pattern | Where | Sources |
|---|---|---|---|
| T1 | **Fake authority**: the officer, manager, supervisor, staff member, online helper or the expected rescuer's voice is the threat | B3 → B11 | SIEGE-CHAT, SIEGE-OVERLAY, DORM-RULES, HOTEL-DOOR, DOG-RULE (the protector's voice at the hiding place), TWO-SUSPECTS (the helper) |
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
| T12 | **Protective object becomes the victim**: the talisman is shown damaged or changed | S9 | BciSW_2VMZg, TWO-SUSPECTS (both talismans crack) |
| T13 | **Narrator is the monster**: the "I" shows the hook's own tell; the investigation was bait | B11 (76%) | FAKE-ROOMMATE |
| T14 | **Knowledge slip**: the helper says one thing he could not know; fair play, checkable by the viewer | B11 (~80%) | TWO-SUSPECTS |
| T15 | **Evidence erases itself**: the thread, photo or log is blank when the hero tries to show it | S10 / B11 | DEAD-CHILD-TEXTS |
| T16 | **The last rule explains the haunting as man-made**: each sign is mapped one-to-one to a mundane cause, and the list was a confession | B11 (87%) | HAUNTED-HOUSE-LIST |
| T17 | **Perspective inversion**: the opening scene is replayed from the other side, so the rule now describes *you*; or the title rule is re-read with one added clause | B11 (97–98%) | TWO-WINDOWS, NIGHT-BUS |
| T18 | **Retelling reverses the thread**: an innocent line in the raw texts becomes reconnaissance; a hidden listener in a replayed scene | B8 / B11 | TEXTS-THEN-BACKSTORY |
| T19 | **Subverted twist**: a trust test (is the all-clear real?), answered "yes", then a planted promise closes as the last line | B11 | HOME-ALONE-READALONG |

Rule: **close one loop and open a bigger one within ~5 s** (HEARSE-P2 does this at every act break).

### 4C. Endings and CTAs

None of the 12 has a spoken subscribe. In the expansion only the host-led HOME-ALONE-READALONG asks for likes, and NIGHT-BUS asks one in-premise comment question at 49%. Endings, ranked by how often they appear (10–14 came with the expansion):

1. **Hard cut at the point of greatest need**: a new imperative from an unknown sender, the possessed companion asking for control, the expert naming the entity with no remedy. (SIEGE-CHAT, HEARSE-P1, HEARSE-P2, FLOOR-PHRASE)
2. **New rule from a new authority**, mirroring the old fake authority's phrasing so the ally is suspect too. (DORM-RULES)
3. **Enemy eavesdrop**: the villains' plan converges on the hero, followed by a "full ending" CTA at peak danger. (SIEGE-OVERLAY)
4. **Soft landing plus a forbidden next document**: episode-count stakes ("make it to day [N+1]"), then a to-be-continued card. (MOM-NOTE)
5. **Threat turned on "you"**, trailing off with an ellipsis. (TEXT-FIGURE)
6. **Brand sign-off plus a signal-lost card**, with the CTA written as broadcast copy. (CLASSMATE-PSA)
7. **Blur plus a "full story ↓" card**. (FARM-FLASHFWD)
8. **Fake win plus a lingering aftermath image**. (TRUCKER-RULES)
9. **Standalone**: "never forgot it", plus a **silent visual sting** that returns to the opening place with an ambiguous figure. (HOTEL-DOOR)

10. **Threat moves into the viewer's phone or house**: a text the morning after, a "any new request could be him" line, a phone PSA, a "your house" threat. (NIGHT-BUS, APP-STALKER, TEXTS-THEN-BACKSTORY, HAUNTED-HOUSE-LIST)
11. **Anthology file card**: a file number as the series hook, with no part label. (TWO-WINDOWS, NIGHT-BUS; the control PIGEONS shows a quieter, numberless card)
12. **Closed "the end"**, plus a moral swerve or a new status quo (the hunter duo, the helper joins). This fits a compiled full story, not a Part 1. (FAKE-ROOMMATE, TWO-SUSPECTS)
13. **Seamless loop**: the last frame leads back into frame 1 under a persistent caption. (BACKSEAT)
14. **Anticlimax realism**: an ordinary exit, never reported, a moral question for the comments. (VIDEO-CHAT-GAME)

The last shot repeats the first shot in HEARSE-P1, CLASSMATE-PSA and HOTEL-DOOR. The last *line* echoes the first (ring structure) in NIGHT-BUS, TWO-WINDOWS, HAUNTED-HOUSE-LIST and APP-STALKER.

Avoid:
- a mid-sentence cut **with no part label** (udhwkz control, 0.77×);
- an app-download funnel line as the ending (mraevq control, 1.06×);
- jump-scare-only endings.

### 4D. Open loops

- Median **2.55 opened per minute** over all 24 (0.5–12). Stories run 1.1–3.6/min; 9–11 min videos run 1.1–1.6/min; Shorts run 6–12/min (BACKSEAT 12, DOG-RULE 10).
- Micro loops close in **2–10 s**. The main loop closes in B10–B11.
- **3–6 loops stay open at the end** for a series (median over all 24: **4**, range 0–6; the first 12: 4.5).
- The expansion adds two other shapes. Complete long episodes close nearly everything and leave only loose ends (FAKE-ROOMMATE 2, TWO-SUSPECTS's small ones). True stories leave **one** loop, aimed at the viewer's own phone (APP-STALKER, TEXTS-THEN-BACKSTORY).
- One **never-closed identity loop** can carry a whole video (DEAD-CHILD-TEXTS: ghost or grief).
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
- **Two series shapes without part labels** (expansion):
  - **Anthology file numbers**: TWO-WINDOWS "file 017", NIGHT-BUS "file 015". Each upload is a pilot, so there is no sequel decay to fight.
  - **"Full story" compiles**: several parts stitched into one 9–10 min upload with "the end" (FAKE-ROOMMATE 23.8×, TWO-SUSPECTS 11.2×). A repost account can turn a series into one long hit.
  - For us, a numbered anthology fits the rules and guidance format best.

---

## 6. Outliers vs ordinary

Same channel, same art, same voice:

| Pair | Hit | Control | What the hit does that the control doesn't |
|---|---|---|---|
| **@udhwkz** | HEARSE-P1 63×, TRUCKER-RULES 20×, FLOOR-PHRASE 18×, SIEGE-CHAT 11× | 7696062340852190496, 0.77× (dead body on a train) | Same title, same 364 wpm, similar numbers per minute (4.3 vs 3.6–5.8). The control's **words** are as dense; its **events** are not. It has a 30 s theory monologue and a 40 s stretch with no new threat. Its premise is a generic body, not an ownable rule or trigger. Its cover frame shows no visible threat. It cuts mid-sentence with no part promise. |
| **@mraevq** | SIEGE-OVERLAY 67×, 7664930759395888416 40×, 7666044652910316833 30×, DORM-RULES 18× | 7665304797242821921, 1.06× (fog creature on a train) | The control's hook is decent: a monster sighting and a parent's fear. But **nothing contradicts a trusted source in the first 10 s**, its jolts come every 30–45 s (vs 11 s and 4 s in the hits), and it ends on an app-download funnel. |
| **WrONG Rules** | MOM-NOTE 31×; BciSW_2VMZg 11× | xKgepVHATm4, 1.0× | **A natural experiment.** The control is essentially MOM-NOTE's last 75 s (the same rules) re-posted as "Pt2" with no hook: no addressee, no stakes, no lifeline line, no setup, no talisman. 9.4K views vs 291K. Its same-day sibling BciSW_2VMZg opens on an urgent presupposing order and got 11×. **The first 10 s is worth about 10–30×.** |
| **Wansee** | HOTEL-DOOR 9× (1.52M) | epzTfKxp16E, 1.16× | The hit's title states the incident, so the slow setup reads as irony. The control's title is a vague clock time, its first wrongness comes at 25 s, it runs 311 s, and its jolts come every 15–20 s (vs a 6.5 s median). |
| **Chat Shorts vs long chat** | TEXT-FIGURE 25.5×, FARM-FLASHFWD 10.4× (60 s); DEAD-CHILD-TEXTS 165.8× (6:18) | Texty Stories 0xzpKw7To98, 1.03× (13:45) | The hits put a bubble every 1.1 s with a jolt every 2.5–3.5 s. Long chat stories put a jolt every 40–60 s, with time-skip cards about every 200 s. The same channel's 6:18 breakout runs a jolt only every 16 s, but it has an emotional engine (a dead child) and a **thread-level device every 60–90 s** (notification, photo, silence, second thread, erased thread). Keep chat horror at 60 s by default. A 4–6 min chat needs those thread devices. |
| **Resident Guidance** (same narrator, kit, length, five-rule template) | TWO-WINDOWS 17.4× | PIGEONS FDLk6TlVTq0, 1.4× | **The cleanest pair in the corpus.** See the table below. The control's threat beats come *more* often (a 13–14 s mean vs 16 s), so cadence did not decide it. The first 30 s and the premise did (n = 1 pair). |

**Resident Guidance pair, line by line** (from `FDLk6TlVTq0.md`):

| | TWO-WINDOWS 17.4× | PIGEONS 1.4× | Lesson |
|---|---|---|---|
| Line 1 | the title rule, in red | a filler word + a normal baseline | open on the rule or the anomaly |
| Anomaly shown | 0:10, as a scene | 0:28, as a statement | wrongness inside 10 s |
| Viewer's role in the open | does the act | watches | make "you" act |
| Threat | a human double | animals | human-shaped beats animal |
| Timeline | one evening and the next morning | loose days | pin the rules to one night |
| Longest rule | the face-to-face visit (21%) | the gaze rule, with the least plot (21%) | give the most time to the closest contact |
| Lines for you to say | yes (counter-phrases) | none | give the viewer words |
| Final inversion | the anomaly is inside your house | you may be chosen next | end with the threat in your space |
| wpm | 141–147 | 121–125 | don't drop much below ~140 in English narration |

**Stat check** (`tools/pacing_stats.json`, hits = all 24 corpus outliers, controls = the 8 at about 1×; the first-12-only figures from 09:05 are in brackets):

| Metric | Hits median | Controls median | Reads as |
|---|---|---|---|
| words/min | 205 [254] | 184 [213] | **No signal** within a channel: the udhwkz control is at 364. The hits' median fell because the expansion is mostly English-native YouTube |
| numbers/min | 2.9 [3.6] | 2.35 [2.0] | weak plus: hits name more counts, distances and times |
| questions/min | 1.65 [3.3] | 3.2 [3.6] | no signal (it depends on the format) |
| % sentences with "you" | 19.6 [14.5] | 14.9 [13.4] | no signal overall; rules and guidance formats run 21–59% |
| sentence median (words) | 8 [7.5] | 7.5 [8.0] | no signal |
| words in the first 10 s | 42.5 [43.5] | 35.5 [38] | small, consistent |
| **jolt interval** | **6.5 s** (1.7–16) [6] | **15–45 s** (library teardowns); PIGEONS 3.5 s for all beats, 13–14 s for threats | **strong, but not sufficient** (PIGEONS) |
| **first contradiction of a trusted source, or first anomaly** | ≤ 11 s in 16 of the 24 (median outlier of those 16: **18.3×**). 2 more land at 12–15 s (DEAD-CHILD-TEXTS, NIGHT-BUS). The 6 that are later all lean on a YouTube title or a sequel (HEARSE-P2, HOTEL-DOOR, HOME-ALONE-READALONG, APP-STALKER, VIDEO-CHAT-GAME, TEXTS-THEN-BACKSTORY): median **7.7×** | 25–30 s or never (PIGEONS 28 s, epzTfKxp16E 25 s, the mraevq control never) | **strongest single signal** |
| longest dry stretch | 19.5 s [17.5] | 30–45 s, plus a 28 s *opening* in PIGEONS | **strong** |

**Bottom line** (it held with the expansion):
- **Event density beats word density.** Every 6–8 s something new is wrong. That holds at 10 minutes too.
- **The trusted thing is contradicted inside 10 s.**
- **There is a rule the viewer can count against.**
- **The cover frame (frame 0) shows the threat.**
- **New:** cadence alone does not make an outlier. The opening 30 s and an ownable, human-shaped premise decide it (PIGEONS vs TWO-WINDOWS).

Speeding up the TTS did not save the udhwkz control.

---

## 7. Pacing stats

From `tools/pacing_stats.py` over the **24 corpus outliers** (the first 12 plus the expansion; the control FDLk6TlVTq0 is counted with the controls). Chat bubbles count as sentences (now including wh9ESTS69Dk). "Jolt" and "loop" counts come from each annotated file via `INDEX.json`. Brackets give **[first 12 | expansion]** where they differ.

| Stat | Median | Range | Notes / target for our scripts |
|---|---|---|---|
| **Words/min** | **205** [254 \| 165] | 69–389 | The median moved because of the format mix, not because pacing changed. By format: translated narrated TikTok **272** (208–389, n 10; the TTS is sped up about 1.3–1.5×); English-native YouTube narration and rules **158** (140–202, n 10); TTS-read chat Shorts **260** (245–274); a silent or host-read chat 69–136. **Our target is unchanged:** narrated story at 230–270 wpm (Kokoro at about 1.2–1.3×), rules or broadcast at 140–180 (TWO-WINDOWS 141–147 vs its control's 121–125: keep it ≥ 140), chat at 250–275 read speed. |
| **Hook length** | **26 words / 8 s** [27.5 / 7 \| 25 / 8] | 5–79 words / 1–15 s | Core hook ≤ 8 s and ≤ 30 words; extended hook to the first turn ≤ 15 s |
| Words in the first 10 s | 42.5 | 8–80 | Excludes the two videos that open on a silent title card |
| **Sentence length** (median of medians) | **7.5 words** | 4–16 | n 21 (unpunctuated auto-subs excluded). Narrated: 5–12-word lines broken up by 3–5-word verdict lines. Chat: 4–5 words per bubble, max 9–10. True-story setups run 20–30-word sentences and drop to 1–5 words at the trigger (VIDEO-CHAT-GAME) |
| Punch lines (≤4 words) | 17% of sentences | 2–64% | Chat 49–64%, rules 20–27% (PIGEONS 44%: fragments without events don't help), narration 12–22%. Put one at every spike. |
| **% sentences with second person** | **19%** [14.5 \| 24] | 3–59 | By format: first-person narrated stories 3–13%; dialogue-heavy 16–28%; rules, guidance or broadcast **21–59%** (median 39, n 5) |
| "you" per 100 words | 2.4 | 0–10 | First person ("I/me/we") per 100 words: 7.4 |
| **Numbers per minute** | **2.9** [3.6 \| 2.3] | 0–5.8 | Translated narrated stories 2.2–5.8: distances, counts, room numbers, clock times, battery seconds. English YouTube 1.5–4.8 (NIGHT-BUS 4.8 with case-file years and stop counts). Chat 0–1. Target 3–5 in narrated stories. |
| Rhetorical questions per minute | 2.4 | 0–11.6 | Inner-monologue engines run 4–12; rules and guidance run ~0 |
| Rule / prohibition words per minute | 1.5 | 0–7.4 | Rules formats 3.4–7.4 |
| **Jolt (re-hook) interval** | **6.5 s** [6 \| 8] | 1.7–16 | Shorts 1.7–3.5; stories 4–11; 9–11 min hits 6–9; silent chat 16 |
| Longest dry stretch | 19.5 s [17.5 \| 21.5] | 2.5–54 | Cap at 25 (see §3) |
| **Open loops per minute** | **2.55** [2.9 \| 1.6] | 0.5–12 | Stories 1.1–3.6; long 1.1–1.6; Shorts 6–12 |
| Loops open at the end | 4 [4.5 \| 3] | 0–6 | Series 3–6; standalone 0–2; complete long episodes ≤ 2 |
| Cut / picture change | 2–3 s | 1–6 s | Guidance pictograms 3–5 s; BACKSEAT has only 3 shots but motion every ~1.5 s |
| Threat onset (B3) | ~6% | 0–48% | Above 15% only when the YouTube title carries the hook (§2) |
| Midpoint turn | ~50% | 42–63% | — |
| Biggest twist position | ~88% | 53–98% | — |
| Scariest image position | ~70% | 41–95% | Most land at 60–80%. The extremes: an empty doorway at 41% (DEAD-CHILD-TEXTS), a grin at the hiding place at 95% (DOG-RULE) |
| Cliffhanger block | ~5% | 1–12% | — |

Per-source rows: `INDEX.json` (wpm, hook, jolt, loops) and `tools/pacing_stats.json` (all lexical stats, plus the alternates, the extra hits and the controls). The first-12-only and expansion-only lexical medians are in `summary.corpus_orig12` and `summary.corpus_expansion`.

---

## 8. Writer checklist (every box must be ticked before TTS)

**Premise**
- [ ] One **ownable rule, trigger or signature** (a sign that announces the threat, a forbidden act, an exact count) that the viewer can track. A generic monster or a generic body is not enough.
- [ ] Set at a **barrier the viewer knows**: a door, a phone or chat, a car, a bed, a classroom, a hotel room.
- [ ] The threat is **human-shaped** (a double, an impostor, a voice you trust) rather than an animal or an ambient force (TWO-WINDOWS 17.4× vs PIGEONS 1.4×).
- [ ] Original story, names, numbers and setting. Not any of the corpus premises (`<id>.md` §3 lists what not to reuse).

**First 10 seconds**
- [ ] Line 1 (≤12 words) names a concrete place or object plus a danger or rule. The threat is visible in frame 0, which is also the cover.
- [ ] Core hook ≤30 words and ≤6 s. A trusted source (official chat, authority, rule, guardian) gets **contradicted by ≤11 s**.
- [ ] No intro, no greeting, no channel name (an ident is fine only in the broadcast format). Never open mid-list or mid-scene, and never on a normal baseline or a silent title card.
- [ ] Rules and guidance format: the cold open shows the anomaly as a scene and makes "you" act in it before the first rule card.

**Body**
- [ ] A jolt at least every **8 s** (median target 6 s). Nothing dry for more than **25 s**, and only once (the lull, ≤25 s, placed at 40–50%).
- [ ] At least 2 rules or warnings stated, at least 1 broken; one of them is a "remember this" plant that pays off later.
- [ ] Two escalation ladders running together (for example proximity and channel removal), switching whenever one stalls. Every rung removes a safe channel or brings the threat closer.
- [ ] ≥2 hyper-specific plants (an ID, a room number, a count, a colour, a time), with at least one paid off inside the video.
- [ ] A viewer-proxy voice (a companion, the chat, the listener) speaks the objections and gets answered or shut down.
- [ ] Numbers: about 3–5 per minute in narrated stories (distance to help, minutes, battery seconds, counts).
- [ ] Midpoint turn at 45–60%. The scariest image appears **once**, at 60–80%, and holds still for about 4 s.
- [ ] A lifeline under a clock (a battery, a call, a deadline) somewhere in 70–90%.
- [ ] Rules format: all rules pinned to one continuous night; the longest rule is the closest contact; every rule chapter ends on a sting followed by the next header within 4 s; one rule's failure is pre-announced early.
- [ ] Long (>5 min): a swinging master loop, numbered chapters or a story count; the jolt median stays ≤ 9 s.
- [ ] The truth twist lands at 85–95% and reframes an authority, a helper or a "safe" object.

**Ending**
- [ ] Hard cut at the moment of greatest need, a new rule from a new authority, or a threat turned on "you" (inside your house or your phone). The last shot bookends the first; the last line can re-read the first rule.
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

**From the expansion, read next:**
4. **kJCVK8xTkPk (TWO-WINDOWS, 17.4×) next to FDLk6TlVTq0 (PIGEONS, 1.4×)**. This is our building-rules premise in the code-only look we can build: line art, overlays, a rule tracker, red/yellow caption code and two glitch stings. Read the pair together to see what the first 30 s are worth.
5. **7650872317119057168 (FAKE-ROOMMATE, 23.8×)**: the hook's diagnostic tell fires three times, the last time on the narrator. It is the template for a 9–10 min complete episode at ~260 wpm.
6. **wh9ESTS69Dk (DEAD-CHILD-TEXTS, 165.8×)**: thread-level chat devices our chat kit can do cheaply (lock-screen notification, live typing, a held photo bubble, a 26 s silence, a banner switch to a second thread, the erased thread).

---

## 10. What changed with the expansion

The sample is now 24 outliers and 8 controls (it was 12 and 7). There are 12 new outliers and 1 new same-template control. Ten of the new outliers come from channels not in the first 12, and 6 run longer than 9 min.

**What held**
- **Contradiction or anomaly inside ~10 s is still the strongest signal.** 16 of 24 do it, median 18.3×. The 6 that don't all lean on a YouTube title or a sequel, median 7.7×. New confirmations: 7650872317119057168 (premise at 0:08), gDNMSoGSZgQ (rule broken by 0:10), kJCVK8xTkPk (double shown by 0:10), 7659482056656735521 (the vanishing sound at 0:05).
- **Event density over word density.** The jolt median is 6.5 s over all 24, and the 9–11 min hits keep 6–9 s (7650872317119057168, 7659482056656735521, 8bo9yZvedUM, hPWu7UAovxk, shTJ7_kRNJ8). wpm still shows no signal: English YouTube hits run 140–202 and the TikTok dubs 208–389.
- **Skeleton timings.** Midpoint ~50% (42–53% in the new ones), scariest image ~70%, twist ~88%. The stories still have no spoken subscribe (only the host-led 8bo9yZvedUM asks), still use a part, file or "full story" device as the CTA, and still use first and last line ring structure.
- **The hook shape.** Median 26 words / 8 s, close to the 27.5 / 7 of the first 12 (the 09:05 text had 6 s).

**What shifted**
- **Medians moved with the format mix.** wpm 254 → 205, open loops per minute 2.9 → 2.55, loops open at the end 4.5 → 4, longest dry stretch 17.5 → 19.5 s. The expansion is mostly English-native YouTube and long complete episodes. The per-format targets in §7 are unchanged.
- **Length.** The "keep it 165–250 s" default stays, but long is no longer a red flag. Outlier medians are about 17–19× in every bucket from 15 s to 11 min (§1). Only the 22-min cWgSgd-QcOY (2.6×) is weak.
- **Late threat onset is possible on YouTube** when the title spoils the event and the setup has its own engine (8bo9yZvedUM at 48%, 6WfCF7KsLaQ at 48%, 02nCBx8WqW0 at 31%). We don't copy this for TikTok-style narration.
- **"Cadence decides" is now "the open decides, cadence sustains".** kJCVK8xTkPk (17.4×) and FDLk6TlVTq0 (1.4×) share narrator, kit, length and template. The control's threat cadence is denser, yet it opens on 28 s of baseline with an animal threat and no role for "you".
- **"Keep chat at 60 s" is now a default, not a rule.** wh9ESTS69Dk runs a silent 6:18 chat with a 16 s jolt median. It gets by on grief plus a thread-level device every 60–90 s (its 166× is against a 1.5K median).

**New patterns** (each added to the section shown)
- Hooks H13–H20 (§2): a cold-open impossible double (kJCVK8xTkPk), a custom plus one rule broken by 10 s (gDNMSoGSZgQ), an exact hour plus a night count plus an online expert's tell (7650872317119057168, 7659482056656735521), a lock-screen message from the dead (wh9ESTS69Dk), spoil the event and withhold the outcome (8bo9yZvedUM, cWgSgd-QcOY), a title rule plus a pre-announced failure rule (shTJ7_kRNJ8), a format promise with a count (hPWu7UAovxk), a persistent "but she was…" caption (x--ui6_mAxE).
- Engines (§1D): suspect hunt with an online helper; cold-open anomaly plus procedure; texts first, context second; the haunted person's own phone; true story with a contact-channel ladder (02nCBx8WqW0, 6WfCF7KsLaQ).
- Long-form chassis (§1C): a swinging master loop with mirrored accusations and competing talismans (7659482056656735521, 7650872317119057168); numbered rule chapters with case-file stings and the mid-roll CTA before the pre-announced failure (shTJ7_kRNJ8, cWgSgd-QcOY); an anthology ordered by twist size (hPWu7UAovxk).
- Twists T13–T19 (§4B): the narrator is the monster (7650872317119057168); the helper's knowledge slip (7659482056656735521); evidence erases itself (wh9ESTS69Dk); the last rule explains the haunting as man-made (cWgSgd-QcOY); a perspective inversion of the opening rule (kJCVK8xTkPk, shTJ7_kRNJ8); the retelling reverses the thread (hPWu7UAovxk); a subverted twist plus a promise callback (8bo9yZvedUM).
- Ladders (§4A): contact channel, odds, social-stakes auction, inward, reality descent, case-file costs, rule closeness.
- Devices worth building into our kits:
  - an inverted caps register (the living person shouts, the entity stays polite) and the line-migration refrain (wh9ESTS69Dk);
  - a protector named as the next arrival, then that voice used as the lure (gDNMSoGSZgQ);
  - teaser lines that announce a shock 2–4 s ahead (6WfCF7KsLaQ) and cliff markers (hPWu7UAovxk);
  - a rule tracker, exhibit cards, a counter that turns red on the wrong number, and a file-number end card (kJCVK8xTkPk, FDLk6TlVTq0);
  - a 1.3 s silent reveal and a seamless loop back to frame 1 (x--ui6_mAxE).
- Series (§5): anthology file numbers and "full story" compiles as two ways to serialize without sequel decay.

**Still thin**
- Most new pairs have n = 1. The expansion has one same-template control (FDLk6TlVTq0).
- shTJ7_kRNJ8 was 1 day old at 3.2K views.
- wh9ESTS69Dk's ratio is against a quiet recent window.
- Treat these as hypotheses to test in pilots, not as rules.

---

## 11. Chinese source mechanics

Added 2026-11-01, about 15:30 UTC, from the 10 source studies in `research/corpus/horror-cn/` (`BV*.md`; the channel map is in `SOURCES.md`). These are the Chinese originals behind most of this corpus's TikTok reposts. **They teach mechanics only.** How to turn a source's mechanics into an original story is in `research/corpus/horror-cn/TRANSPOSE_RULES.md`. The plot gate is `python3 scripts/plot_similarity.py <script.md> research/corpus/horror-cn`, and it runs next to `originality_check.py`.

### 11A. Source key

"Best EN" is the biggest English repost found. "×" is that repost's views over the Bilibili plays.

| Short name | Study | Channel | Length | Bilibili plays | Best EN repost | × |
|---|---|---|---|---|---|---|
| CN-HEARSE | BV1TEJ164EHc 拦车孝 | 异常收录档案 | 21:33 | 740.6K | udhwkz Part 1, 2.2M | 3.0 |
| CN-GRINDER | BV1qbL56CE74 磨牙怪 | 杰出影视本人 | 8:09 (chapter) | 41.8K (68-min compilation) | lehwh7, 1.9M | n/a |
| CN-SIEGE | BV1nEoYBBEXE killer + danmaku | 杰出影视本人 | 7:21 | 151.7K | mraevq, 717K | 4.7 |
| CN-DINO | BV1fR7szYEDq 迷雾恐龙 | 杰出影视本人 | 7:47 | 230.5K | mraevq, 326K (+ lehwh7 305K) | 1.4 (2.7 combined) |
| CN-IMPOSTOR | BV14EiCBdEUh 迷雾伪行 | 杰出影视本人 | 15:45 | 49.6K | lehwh7, 529K | **10.7** |
| CN-TRAIN | BV1WchTz9Ejt 迷雾列车 | 杰出影视本人 | 15:06 | 167.7K | lehwh7, 508K | 3.0 |
| CN-SLEEP | BV1oPbFzDEX6 迷雾沉睡 | 杰出影视本人 | 14:49 | 186.9K | lehwh7, 486K | 2.6 |
| CN-ESCAPE | BV1JhKP6FEjr night escape | 杰出影视本人 | 18:44 | 53.6K | mraevq, 428K | **8.0** |
| CN-DUMPLING | BV1dbwuz3EvY 迷雾疑凶 | 杰出影视本人 | 18:59 | **524.6K** | ChenJie Horror (YouTube), 12K | 0.02 |
| CN-CURTAIN | BV1DbK563Eih 诡夜红床 | 夏哭有点怂 | 13:35 | 53.6K | mraevq Part 1, 194K | 3.6 |

### 11B. Mechanics catalogue (frequency across the 10 sources)

Ids M1–M26 are the ones `TRANSPOSE_RULES.md` uses. "Short" means it fits a 60–90 s video; "Series" means it needs multi-part room.

| Id | Mechanic | n/10 | Sources | Short | Series | Notes |
|---|---|---|---|---|---|---|
| M1 | Premise complete in ≤ 10 s; the title is the premise in one sentence | **10** | all | ✓ | ✓ | Median 7 s (6–10). No intro or title card anywhere |
| M2 | A world or insider rule stated early (trade lore, one survival rule, a note) | 9 | all but DINO (SIEGE: a game-rule promise only) | ✓ | ✓ | Single rule in 5 (GRINDER, TRAIN, SLEEP, ESCAPE, DUMPLING); a list in 3 (M4) |
| M3 | The rule backfires, inverts, or was planted by the threat | 6 | IMPOSTOR, CURTAIN, TRAIN, DUMPLING, SLEEP, GRINDER | ✓ (one backfire) | ✓ | The identity seed in CURTAIN (0:19) and IMPOSTOR (2:23) |
| M4 | Numbered rule list (2+ rules delivered together) | 3 | HEARSE, IMPOSTOR, CURTAIN | ✓ | ✓ | Rules are spoken or on a phone; no source shows a rule card |
| M5 | A trusted source is shown wrong | **10** | all | ✓ | ✓ | First flip median **15%** of runtime (2–32%) |
| M5b | The helper, guide or ally is the threat | 5 | GRINDER, SIEGE, TRAIN, SLEEP, DUMPLING (CURTAIN ambiguous) | ✓ (as the last beat) | ✓ | 杰出影视's house move: the guide is the villain |
| M6 | Authority carousel (3+ adviser handoffs, each discrediting the last) | 3 | CURTAIN (6 handoffs, about every 2 min), GRINDER, IMPOSTOR | ✗ | ✓ | Needs about 2 min per handoff |
| M7 | Count / number clue (headcount, distance, weight, schedule, clock) | **10** | all | ✓ | ✓ | Lands by 0:19 in SIEGE, 0:43 in DUMPLING. Viewers repeat the number in comments |
| M8 | Barrier: a knock or voice at the door, bed or seat | 7 | GRINDER, SIEGE, DINO, SLEEP, ESCAPE, DUMPLING, CURTAIN | ✓ | ✓ | The vehicle stories (HEARSE, TRAIN) and IMPOSTOR use none |
| M9 | A phone rings nearby and exposes a lie or a body | 3 | DINO, SLEEP, SIEGE (weak) | ✓ | ✓ | Pays off within 10 s, so it's cheap |
| M10 | Isolation with one live channel; help delayed (a number: km, minutes) | 7 | HEARSE, SIEGE, DINO, TRAIN, SLEEP, ESCAPE, DUMPLING | ✓ | ✓ | "No signal, but the chat works" (SLEEP) keeps the phone UI alive |
| M11 | An outside check or visible second channel falsifies an insider (call, overlay, news app, feed) | 6 | HEARSE, SIEGE, DINO, IMPOSTOR, SLEEP, CURTAIN | ✓ | ✓ | The strongest Short device: SIEGE's overlay at 0:09 |
| M12 | Two suspects or rotating suspicion, mirrored accusations | 6 | GRINDER, IMPOSTOR, TRAIN, SLEEP, DUMPLING, CURTAIN | ✗ | ✓ | The "who is lying" swing every 30–70 s (§1C) |
| M13 | Protective object saves once then fails, or turns out to be the opposite | 4 | HEARSE, GRINDER, IMPOSTOR, CURTAIN | ✓ (one flip) | ✓ | Paired tokens from rival advisers in GRINDER |
| M14 | A test for human vs not (shibboleth, touch, machine, question) | 6 | GRINDER, SIEGE, IMPOSTOR, ESCAPE, DUMPLING, CURTAIN | ✓ | ✓ | Lived knowledge beats book knowledge (IMPOSTOR). Needs a native question |
| M15 | Knowledge-leak tell ("how do you know that?") | 7 | HEARSE, GRINDER, DINO, TRAIN, SLEEP, DUMPLING, CURTAIN | ✓ | ✓ | The hero flags it, then the story buries it under action (SLEEP 4:51) |
| M16 | An early proof death: a bystander or rule-breaker | 7 | HEARSE, SIEGE, DINO, IMPOSTOR, SLEEP, ESCAPE, DUMPLING | ✓ | ✓ | First death median **10%** (n = 8; GRINDER and CURTAIN have none on screen) |
| M17 | A countdown or visible timer (days, battery, body mark, growth, loop window) | 7 | HEARSE, GRINDER, SIEGE, DINO, TRAIN, SLEEP, CURTAIN | ✓ | ✓ | Always spoken, never a numeral on screen except TRAIN's speed display |
| M18 | Loop, reset or nested dream | 4 | TRAIN, DUMPLING, GRINDER, SLEEP | ✗ | ✓ | TRAIN's loop is 2:00 of screen time per 2-minute loop |
| M19 | Frame break: it's a show, a simulation, hypnosis or an illusion | 5 | SIEGE, TRAIN, SLEEP, DUMPLING, CURTAIN | ✓ (as the reveal only) | ✓ | Danmaku compare TRAIN to *Source Code*; frame breaks read as derivative fast |
| M20 | A mimic or impostor uses a familiar voice, face or memory | 6 | GRINDER, SIEGE, DINO, IMPOSTOR, SLEEP, ESCAPE | ✓ | ✓ | ESCAPE's mimic proves itself with a domestic detail |
| M21 | Hero ahead: a withheld action or deduction revealed after the escape | 6 | GRINDER, SIEGE, IMPOSTOR, SLEEP, DUMPLING, CURTAIN | ✓ | ✓ | Explain after the escape, never before (SIEGE 5:38) |
| M22 | The narrator is implicated (culprit, monster, conspirator, "you're the ghost") | 5 | DINO, IMPOSTOR, TRAIN, DUMPLING, CURTAIN | ✓ (last line) | ✓ | Earned in TRAIN; asserted in DINO and DUMPLING (viewers say "???") |
| M23 | Villain-to-victim or hidden protector | 4 | HEARSE, GRINDER, ESCAPE, CURTAIN | ✗ | ✓ | HEARSE's back quarter is melodrama; the English repost never reached it |
| M24 | Group-chat chorus and disbelief | 3 | SIEGE, DINO, SLEEP | ✓ | ✓ | Fewer than in the English pool; most sources narrate the chat |
| M25 | Overheard enemy or outside voices | 3 | SIEGE, TRAIN, ESCAPE | ✓ (cliffhanger) | ✓ | SIEGE ends on one |
| M26 | Expert lore dump that names the entity | 6 | HEARSE, GRINDER, IMPOSTOR, SLEEP, ESCAPE, CURTAIN | ✗ | ✓ | Keep under 40 s, right after a shock (IMPOSTOR) |

**Warning channel** (how the premise arrives): phone UI (DM, group chat, SMS) in 4 (GRINDER, SIEGE, IMPOSTOR, SLEEP); a paper note in 2 (TRAIN, DUMPLING); spoken by an insider or authority in 3 (HEARSE, ESCAPE, CURTAIN); the threat itself speaks at the door in 1 (DINO). Six of the ten have no chat UI at all, so the genre runs fine on narration plus one prop. Our chat kit is an upgrade on the sources, not a copy.

**Endings:** a villain win or last-line sting in 4 (DINO, IMPOSTOR, TRAIN, DUMPLING); closed, sacrifice or tearjerker in 2 (HEARSE, ESCAPE); a generational loop in 1 (SLEEP); ambiguous and selfish in 1 (CURTAIN); a hard cliffhanger in 1 (SIEGE); closed plus a franchise tag in 1 (GRINDER). Only SIEGE leaves the danger open, and it's the one whose viewers ask for a sequel.

### 11C. Beat timing (medians over the 10 sources)

| Measure | Median | Range | Notes |
|---|---|---|---|
| Length | 15:00 | 7:21–21:33 | Three are under 8 min (SIEGE, DINO, GRINDER). The rest are "一口气看完" (watch-in-one-go) compilations |
| Premise complete | **7 s** | 6–10 s | Same as the English pool's 8 s hook (§2) |
| First trusted-source flip | **15%** | 2–32% | SIEGE 2%, DINO 7%, DUMPLING and TRAIN 14%, HEARSE 32% |
| First death on screen or in report | **10%** | 1–30% (n = 8) | |
| Main twist (the one that re-sorts the story) | **85%** | 67–98% | Matches the English pool's ~88% (B11) |
| Turn interval (new threat, reveal or reversal) | **18 s** | 14–35 s | **14 s** under 8 min; **27 s** at 13 min and longer. The longest sag sits at ~50% (a "deduction sag") |
| Twists | **12.5** per story | 9–19 | **0.9 per min** (one every ~68 s); 1.35/min in the short sources, 0.8/min in the long ones |
| Text density | **370 hanzi/min** | 325–393 | One caption line every 1.5–2.1 s, 9–12 hanzi each |
| English TTS dub speed | **~238 wpm** | 190–364 | udhwkz runs 364 wpm; lehwh7 about 250 |

### 11D. What transfers to 60–90 s Shorts

- **The first 10–15% of a Chinese source is already a complete Short skeleton.** SIEGE's 0:00–0:57 has the all-clear, the knock, the overlay contradiction, the count and the chat pressure: five mechanics in 57 s. CURTAIN's 0:00–0:31 has the accusation, the rule, the backfire and the cover story. DINO's 0:00–0:31 has the premise, the knock, the creature's speech, the call and the confession.
- **The English spikes are first-part cuts.** udhwkz's 2.2M HEARSE Part 1 is source 0:00–4:28 (21%). mraevq's 194K CURTAIN (18×) is 0:00–3:45 (28%). Reposters stop at the first big question. They never reach the lore, the remedies or the melodrama.
- **A Short takes one engine and 3–4 mechanics.** Use M1 + M2 + M11 (or M5) + M7, then one of M15, M9 or M20, then end on a new rule from a new authority (M3) or a last-line implication (M22 lite). Map it onto S1–S10 (§1B): the rule is S1/S4, the flip is S2/S5, the count is S3, the turn is S6 at ~50%, and the sting is S10.
- **Keep the source tempo, not its length.** Turns every 14 s are the short-source median. A Short needs the English pool's 2.5–3.5 s jolt (§3), so compress three source beats into one paragraph.
- **What doesn't fit a Short:** M6 carousels, M12 two-suspect whodunits, M18 loops, M23 villain-to-victim melodrama, M26 lore dumps and generational codas. CN-DUMPLING is the studio's biggest Chinese hit (524.6K) and barely travelled (12K): fair-play procedure needs runtime.
- **What travels best:** phone, text or parent-warning premises. The highest English multiples are IMPOSTOR (10.7×, an unknown-number text) and ESCAPE (8.0×, a parent's unexplained warning). Absurd creatures travel when the door frame stays (DINO 631K across two reposts).
- **Native surface, borrowed engine.** China-specific satire, folk-religion props and IP parodies don't appear in English at all (`SOURCES.md`). Folk cosmology needs a Western rule system: SOPs, bylaws, machine behaviour (`TRANSPOSE_RULES.md` §3).

### 11E. What needs a multi-part series

- **Engines that need room:** the carousel (CURTAIN: 6 handoffs in 13:35), loops (TRAIN: ~2 min per loop), two-suspect hunts (GRINDER, DUMPLING), mentor chains with remedies (HEARSE) and frame breaks with a proof sequence (DUMPLING).
- **Where the sources and reposters cut:**
  - On a new rule from a new authority. CURTAIN Part 1 ends at 28%: "it will go find someone else".
  - On the companion asking for control (HEARSE 4:28, 21%) or an entity named with no remedy (HEARSE 8:44, 41%).
  - On a withheld name: the hero knows who did it and asks one question first (DUMPLING 7:45, 41%).
  - On an antagonist's silent, calm reaction: the uncle smiles and doesn't chase (IMPOSTOR 8:25, 53%, the Bilibili paywall cut).
  - On a door decision. "Should I go out?" (CURTAIN 7:54, 58%).
  - Parts end on a decision or a rule, never on a death.
- **The compilation beats the parts.** CURTAIN's Part 3 alone got 2.1K and its compilation got 53.6K (about 25×); the same channel's 吓吓打墙 got 2.8K for Part 1 and 54.4K for the compilation. This matches §5's sequel decay. Post parts for reach and a full-story compile for the binge, and hook each part cold.
- **Series identity:** a recurring hero with one costume code (Chen Jie's neon jacket) plus a recognisable house move (the helper is the villain). For us that means a numbered anthology (§5) with one recurring narrator voice and one recurring move, never the studio's.

### 11F. Use rules

- These stories are web-fiction adaptations that several studios animated. Retelling one is an originality failure and a rights problem, even with every name changed.
- From one source keep at most three generic mechanics, change the order or role of one, and add one it doesn't use (`TRANSPOSE_RULES.md` §1, §4).
- Before TTS, both gates must PASS:
  - `python3 scripts/originality_check.py <script.md> research/corpus research/library/transcripts`
  - `python3 scripts/plot_similarity.py <script.md> research/corpus/horror-cn`
  
  The plot gate FAILs on 3+ specific events in a source's order, 3+ of its twists in order, or a source name plus a signature clue. Shared generic mechanics never fail it.
