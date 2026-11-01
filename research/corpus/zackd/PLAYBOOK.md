# Zack D. Films format PLAYBOOK (internal format research)

> Internal research only, to learn the format. Never reuse Zack D. Films' scripts, wording, characters, sets, props, brand marks or footage in anything we publish (BRIEF hard rule 5). Every script that cites a video here must list it under `references:`, include a beat-alignment table and pass `scripts/originality_check.py`.

Built 2026-11-01 from:
- `CHANNEL.md` / `channel.json`: 400 newest Shorts (387 mature), cluster, title and length stats.
- `IMITATORS.md` / `imitators.json`: 63 imitator channels, 39 of them under 6 months old.
- 10 annotated videos (7 outliers, 3 controls), each with a full transcript, a line table, a shot list and a transferable skeleton in its section 7:

| id | role | outlier | views | cluster | sub-format (skeleton in that file) |
|---|---|---|---|---|---|
| `0BZ1C83I2R4` | outlier | 6.0x | 66M | how-it-works (really fiction) | wordless fake explainer: "secret crew inside an everyday object" |
| `yudJI1L8jlI` | outlier | 5.1x | 51M | heartwarming | "creature gets a custom fix" build ladder |
| `CRGWDiIgMZ4` | outlier | 4.07x | 57M | nature | one creature, one mechanism, late reframe, grammatical loop |
| `1Rd3_pXs6DU` | outlier | 3.9x | 39M | fiction skit | "(Patent Pending)" deadpan fake product |
| `W3NlT3SKkmQ` | outlier | 3.36x | 47M | life hack / body | second-person "fix it with your body" how-to that is mostly *why* |
| `p832whe8hrI` | outlier | 3.09x | 21M | survival | trapped-POV failure ladder with a counterintuitive release |
| `NEgarf1vDTU` | outlier | 2.64x | 29M | gross / true story | domestic anomaly, then the hidden source |
| `MKRYulCq3Mo` | control | 1.04x | 10M | how-it-works | machine that mirrors a body process, absurd-purpose twist |
| `-7MDLZCb1Mw` | control | 1.00x | 14.6M | nature | "gross but useful" symbiosis cycle |
| `jHbhgBgaA34` | control | 1.00x | 10.6M | body | slow-harm time-lapse, moral, second-case sting |

Companion spec for the kit builders: `VISUAL_GRAMMAR.md` (proportions, measured palette hex values, lighting, materials, camera, shot lengths, captions).

Small-sample warning: 7 outliers and 3 controls. Any "outliers do X, controls don't" claim below is a hypothesis with its counts shown, not a law.

---

## 0. The format in ten lines

1. A **28-40 s** (median 33 s) vertical 3D short. One calm, deadpan narrator speaks from **0.0 s** at about **170 wpm** and never stops until the last 0.5-0.9 s.
2. **Frame 0 is already the action**: a bite in progress, a bullet in flight, a maggot on a bulb, a hand plugging in a charger. There is never an intro, logo, presenter or "did you know".
3. One **mechanism** is the content. Even the stories, gags and how-tos spend 40-75% of their runtime on "how it physically happens".
4. **Literalize every line**: each spoken noun or verb gets its own picture within about 0.5 s, and each abstract word gets a prop or icon (pressure = arrows, smell = green vapour, time = a calendar or the room dimming).
5. The camera **never stops moving**, a new picture comes about every **1.4 s**, and transitions are whip-blurs, crash-zooms and push-throughs into cutaways.
6. The world is **bright, clean, high-key and toy-real**: cobalt and cyan worlds with a warm subject, even when the subject is a corpse or a wound.
7. **Escalation is by kind, not amount**: each rung brings a new tool, a new field of science, a new sense or a new scale.
8. A **late reframe** (median about 80% of runtime) recolours what was already shown, usually by bringing back a noun from the first 30%.
9. The ending mirrors the opening (same verb, same place, same framing), puts the strongest word last, and loops. There is **no CTA and no moral** in any of the 7 outliers.
10. The title is Title Case, about 7 words, plus one emoji used as a genre label. "Why X" and "The X" (short noun phrase) titles beat "The Person Who Did Y".

---

## 1. The canonical skeleton (narrated mechanism Short)

Timings are % of runtime. They come from the 9 narrated videos and are tuned to what the 6 narrated outliers did. Target: **30-35 s, 85-100 words, 165-180 wpm, 20-26 shots.**

| % of runtime | Beat | Job | Measured in the corpus |
|---|---|---|---|
| 0-2% | **Frame 0** | The action or anomaly is already on screen before the first word. No establishing shot longer than 0.5 s. | 10/10 videos. The longest pre-action wide is 0.45 s (sloth). |
| 0-15% | **Hook sentence** | One sentence of 13-22 words, the fastest stretch of the video (about 190-210 wpm). It states the situation or the action in progress, restates or assumes the title, and ends on a comma or a stinger word. | Hook ends at 11-16% (median 15%). Hook wpm median 196 (138-224). |
| 15-30% | **Stakes / first step** | One concrete consequence, or the first part of the mechanism. Show one try-and-fail, or the smallest part acting. | Problem fully stated by 28% (eagle); first block by 13% (car). |
| 30-55% | **Mechanism ladder** | 2-4 steps, one clause and one picture each, joined by a connector (then / next / so / but / now). Each step changes scale, tool, place or field of science. A pivot word about every 4.5 s. | Pivot interval 3.5-5.8 s. |
| 50-70% | **Money shot** | The single image people remember, held 2-5 s: the longest hold in the video. It is gross-but-satisfying, a spectacle, or a precise shape. | Measured 40-76%, median about 60% (round plug 40-52%, spray 54-63%, canal blob 57-63%, outlet arcs 62-68%, dung larva 62-68%, sample 68-75%, beak slide 73-76%). |
| 65-88% | **Turn / reframe** | A pivot word, then a reinterpretation of what was already shown. A force, clue or phrase planted in the first 30% comes back and flips meaning (the enemy becomes the key, the attack becomes a strategy, the throwaway step becomes the mechanism). | Narrated outliers: 63, 78, 82, 86, 87, 92% (median about 84%). |
| 85-100% | **Mirrored payoff + loop** | The payoff reuses the opening's verb, noun or location. The strongest word is the last word. Then a 0.5-0.9 s tail with no caption, and a hard stop. The last frame or clause leads back into frame 0. | 7/7 outliers have a strong loop seam; 0/3 controls do. Tail median 0.7 s. |

### Where each video hit the beats

| video | hook ends | money shot | turn | payoff | loop type |
|---|---|---|---|---|---|
| CRG shark (4.07x) | 27% (hook + 2 mechanism steps in one sentence) | 40-52% | 66% "why" turn, 78% twist | 90-100% | grammatical: the last clause runs into the first |
| yud eagle (5.1x) | 15% | 73-76% (part slides on) | none (build ladder) | 86-100% mirrors the failure verb | calm hero hold, then the violent frame 0 |
| 1Rd3 product (3.9x) | 15% | 54-63% (gross peak) | 46% complication, 92% reversal | 92-100% | same hero, same set as frame 0 |
| W3N ear (3.36x) | 12% | 57-63% | 63% callback | 88-100% ends on the title's noun | title echo, hard end |
| p832 car (3.09x) | 13% | 61% bottom wide | 82% flip | 90-100% first try now works | bright lake = frame 0 |
| NEg maggots (2.64x) | 11% | 87-98% reveal | 51% subject swap | 87-98% | spatial: ceiling at the start, floor at the end |
| 0BZ outlet (6.0x, wordless) | 8% (visual) | 62-68% | gag lands 22-35% | 90-100% | bookend: charger, then the phone |
| MKRY machine (control) | 15% | 68-75% | 75% purpose, 88% twist | 88-97% | weak (gallery cut to POV plate) |
| sloth (control) | 12% | 62-68% | **14%** (flip given away early) | 90-100% explicit thesis | visual only |
| posture (control) | 16% | 74-77% | 77% second-case transfer | 90-100% sting | weak (different character) |

### Sub-format skeletons (use the matching file's section 7)

| If the premise is... | Use the skeleton in | Shape |
|---|---|---|
| A creature's or object's single strange mechanism | `CRGWDiIgMZ4.md` | answer-first, 3 acts, same contrast pair twice, loop |
| A thing gets fixed or built | `yudJI1L8jlI.md` | injury, broken routine, 3 build steps, mirrored payoff |
| "If you..." body or household problem | `W3NlT3SKkmQ.md` | plant a step early, 40%+ on why, release payoff |
| "What to do if..." danger | `p832whe8hrI.md` | 3 failed tries from 3 fields, bottom, counterintuitive move, flip |
| A strange discovery, true-story style | `NEgarf1vDTU.md` | one unit, then many, then everywhere, two clues, noun-drop reveal |
| A machine that copies something familiar | `MKRYulCq3Mo.md` | input-to-output hook, rewind, stages, serious use then absurd use |
| A fake product (comedy) | `1Rd3_pXs6DU.md` | pain, pun product, deadpan feature ladder, misuse peak, reversal |
| A wordless gag about an everyday object | `0BZ1C83I2R4.md` | mundane action, cutaway, crew, one barked line, Rube Goldberg, back to reality |
| A habit's cost over a lifetime | `jHbhgBgaA34.md` | habit constant, clock races, cost in a moment that matters, transfer |
| A cycle in nature | `-7MDLZCb1Mw.md` | only with its section 8 fixes (late reveal, one image, looping last line) |

---

## 2. Hook formulas (slots only; write fresh words)

Hard rules seen in 9/9 narrated videos: speech starts at 0.0 s; no question to camera; no "did you know"; no channel name; no setup of who or where. The title carries the noun, so the hook can start mid-action.

| # | Formula (slots) | Seen in | Stats |
|---|---|---|---|
| H1 | **Dangling action clause with a pronoun**: "[While/As] [pronoun] [present verb]s the [victim], [smallest part] [body verb]..." The noun is withheld for several seconds because the title supplies it. | CRG (4.07x) | 5 words in 1.7 s; the noun arrives at 8 s |
| H2 | **Cause object first, already hitting a named part**: "The [cause object] [motion verb] into the [creature]'s [specific part], [destruction verb]-ing..." No villain, no place. | yud (5.1x) | 15 words, 174 wpm; the break shows on screen at 3.7 s |
| H3 | **Second-person conditional mishap fused to the first instruction**: "If you [common mishap] and [annoying result], [imperative]..." | W3N (3.36x); 1Rd3 uses "If you [body need] but [obstacle], just [tech gesture] [pun product]" | 13 words in 3.5 s (224 wpm), the fastest hook in the corpus |
| H4 | **"Picture yourself" + sudden everyday disaster + the obvious move + a named force that blocks it**, in one sentence | p832 (3.09x) | premise in 1.9 s; 22 words in 6.7 s |
| H5 | **One small wrong thing during a chore, with a direction word**: "A [single unit of anomaly] [verb] from her [location] as she was [chore]..." | NEg (2.64x) | 13 words, about 210 wpm; restates the title within 2 s |
| H6 | **Whole story compressed, stinger last**: "The [input] was [verb]ed in, and [time gap] later it [came out as] [gross output]." | MKRY (control) | 16 words, 201 wpm |
| H7 | **Symptom + the habit the viewer is doing right now + dismissal** | posture (control) | 20 words, 207 wpm |
| H8 | **Named subject + disgust verb + two small actors + an early "not a bad thing" flip** | sloth (control) | 9 words, 138 wpm. **Weakest pattern**: it gives the reframe away at 14% |
| H9 | **Wordless**: a hand does the most common action with an everyday object, then the camera slips behind its surface into a hidden world at 0.5 s | 0BZ (6.0x) | no words until 4.5 s; the title is the only verbal hook |

Hook craft rules:
- Put the **visual hook before the verbal one**. In 10/10 videos the first frame shows the most unusual thing available (the bite, the bullet, the larva, the pained face).
- Say the hook **faster than the body** (hook median 196 wpm against 170 overall).
- End the hook on a **comma** (it runs straight into the next clause, so there is no exit point) or on a **stinger noun** (the grossest or strangest word last).
- **Never hedge** in the hook. The only hook with hedges ("not necessarily", later "may even") is the weakest control.

### Title formulas (from 387 mature titles in `CHANNEL.md`)

| Pattern | n | Median views | Median outlier | Use |
|---|---|---|---|---|
| "The [Short Noun Phrase]" ("The ___ Paradox") | 29 | 12M | **1.22** | best template |
| "Why [X] [Odd Fact]" | 46 | 12M | **1.12** | best explainer template |
| "What Is / What Happens..." | 6 | 13M | 1.09 | small n |
| "How [X] [Verb]" ("How [creature] [verb]s [victim]") | 61 | 10M | 1.03 | the workhorse |
| Subject + verb headline ("[Creature] Gets A [Tech] [Part]") | 53 | 10M | 1.03 | gives away the outcome on purpose |
| "How To [X]" | 42 | 10M | 0.91 | best when "your body" is in it |
| "How [X] Works" (literal) | 27 | 8.6M | 0.84 | only for objects everyone touches daily |
| "The [Noun] Who/That [Did Y]" | 42 | 7M | **0.78** | avoid: it summarises the story |
| Gerund ("Turning A ___ Into ___") | 23 | 7.2M | **0.72** | avoid |

- Title Case, about 7 words, exactly one trailing emoji used as a genre label: thinking face = explainer, open-mouth = wow, fearful = danger, screaming = shock, nauseated = gross, crying or smiling-with-tear = emotional, smirk = trick. Shock and gross emojis (14M and 12M medians) beat the neutral thinking/open-mouth workhorses (9.9M).
- The title is a **contract the video pays at 0 s**: the hook restates or assumes it. The wordless outlet video deliberately breaks the contract (a real explainer title on a fiction gag), and that bait-and-switch is part of the joke.

---

## 3. "Literalize every line": the visual grammar in one page

The engine of the format: **the picture is a literal translation of the narration, beat by beat, and the narration never says "as you can see".** Numbers and hex values are in `VISUAL_GRAMMAR.md`.

1. **Every noun and verb gets its own picture within about 0.5 s of being spoken.** "Grinder" goes inside the grinder; "slid onto" shows the part dropping from the top of frame; "skeleton" lands as the pull-back reveals the body. Cuts and reframes land on phrase boundaries, never mid-word.
2. **Every abstract word gets a prop or an icon.** Diagrams with text labels are never used. The corpus lexicon:

| Abstract idea | Literal device | Seen in |
|---|---|---|
| force, pressure | glowing red cone arrows converging on the object | p832 |
| direction, gravity | one bright cyan arrow, plus a number shown only on screen | W3N |
| the thing being named right now | a green or yellow glow outline on that object | p832, MKRY |
| seal, contact | a cyan rim glow tracing the edge | W3N |
| invisible quantity (pressure, heat) | a colour ramp filling the cross-section (red, orange, yellow, white, blue) | W3N |
| rotation, twist | a ring of pale chevrons circling the subject (the one diagram overlay) | CRG |
| smell | translucent acid-green vapour or wavy stink lines | NEg, MKRY |
| pain | red-orange glow on the body part plus three red lightning bolts | posture |
| a voice calling | concentric rings | posture |
| failure | the whole frame flushes red | p832 |
| time passing | a wall calendar flipping, the room dimming to night blue and back, light changing in a window, a clock prop | posture, MKRY, p832 |
| "equal" | two props (one inside, one outside) glowing the same colour | p832 |
| hidden mechanism | a cut-out hole or x-ray inset in the surface; cross-sections with flat-filled cut faces | p832, MKRY, 0BZ |
| a simile | a cartoon version of the simile object pops into frame and copies the motion | W3N (plunger) |
| a folk idiom | the idiom built literally, at full production value | 0BZ (hamster wheel) |
| a machine's view | a purple-tinted HUD with scan rings and a crosshair | 1Rd3 |
| a memory or flashback | a cloud-edged thought bubble replaying the opening | yud |

3. **Narration person = camera person.** "You" trapped and acting: first-person POV (forearms only). "You" changing over time: third person (the face has to age). "He/she/it": third person, cinematic.
4. **Scale is a storytelling tool.** Victims are walls filling half the frame; small causes are drawn about 10x real size so they read on a phone; scale changes always go through a crash-zoom or push-through.
5. **The picture knows one thing the voice doesn't.** A planted sign that gives away the twist, a background extra who becomes the victim of an unnarrated gag, a second victim that shows the habit is general. This is the rewatch reward, and it costs no words.
6. **The brand is a prop**, never an overlay: printed on a T-shirt, a 3D-printer bed, a glue bottle, a dung pellet, a festival arch. For us: our own mark, on our own props.
7. **Gross is styled as food or toys.** Flesh plugs look like marbled salmon, faeces is amber cartoon fluid, larvae are cute and translucent, the skeleton is clean ivory and still dressed. The bright lighting never changes for dark subjects.

---

## 4. Escalation patterns

Every ladder escalates by **kind**: each rung adds a new tool, place, sense, field of science or scale. None of the 10 videos repeats a rung at a bigger size.

| Ladder | Rungs | Seen in | When to use it |
|---|---|---|---|
| **Part to whole to result to reason** | smallest part, biggest part (+ simile), whole body moves, precise result, unexpected aftermath, why | CRG | one creature or object mechanism |
| **Failure ladder** | the obvious move (blocked by physics), the system (blocked by engineering), a special tool (blocked by materials), bottom, the scary counterintuitive move, the first blocker reverses | p832 | danger, defence, "what to do if" |
| **Build ladder** | injury, broken routine, capture the shape, fabricate (the title's tech word), attach in 3 quick verbs, mirrored payoff | yud | repairs, inventions, how a thing was made |
| **Anomaly ladder** | one unit, many, every surface, appeal to authority, a second sense from independent witnesses, the subject swaps to the source, isolation, authority arrives, threshold, noun-drop reveal | NEg | discoveries, mysteries, true-story style |
| **Effort-to-release ladder** | passive step, seal, repeated force, release (the climax is letting go) | W3N | body or household how-tos |
| **Machine stage ladder** | mechanical, chemical, biological (scale drops to micro), time skip, compression with a repeated word, sensory proof, serious purpose, absurd purpose | MKRY | processes, factories, machines |
| **Time ladder** | habit fixed, life stages flash past, awareness, fake fix, decades skip, the cost lands in a moment that matters | posture | slow harms, compounding |
| **Deadpan feature ladder** | real-sounding tech step, step, ritual, misuse triggers an absurd defence (the gross peak), deadpan button, list of three, reversal | 1Rd3 | fake products |
| **Rube Goldberg sandwich** | mundane outside, impossible space, idle operator jolted, true power source (the gag), effort, transmission, spectacle, travel, back to reality, ordinary result | 0BZ | wordless object gags |

Common rules:
- **Plant early, pay late.** The key noun of the reversal (pressure, the throwaway first step, the smell, "tell yourself") is planted in the first 30%.
- Each failure or step gets **one named mechanism from a different field**, so every rung teaches one new fact.
- **The stakes switch type at the top rung**: physical to emotional (posture), gross to sad (maggots), gross to social irony (machine), spectacle to personal sting (product).
- **Pace follows the content.** Builds and procedures speed up toward the end (eagle 174 to 194 wpm); dread and reveals slow down (maggots reveal at about 136 wpm; the car's "wait" section at 169).

---

## 5. Punchline, twist and ending patterns

| Pattern | Mechanic | Seen in |
|---|---|---|
| **Reframe, not a new fact** | The twist adds nothing new to the picture; it re-reads what was shown (the attack was a deliberate partial meal) | CRG |
| **The first enemy becomes the key** | The force that blocked try 1 is what finally releases it; repeat its name 2-3 times so the flip is easy to follow | p832 |
| **The throwaway step was half the mechanism** | A step given with no reason at 12% is explained at 63% | W3N |
| **Mirrored problem and payoff** | The failure line and the payoff line share one verb; the payoff also names the inciting cause again | yud |
| **Noun-drop reveal** | One concrete noun answers two clues and implies elapsed time; the causal link is never said | NEg |
| **Serious use, then absurd use** | "[noun] did [serious thing], while other [noun] [absurd thing]", ending on the twist word | MKRY |
| **Role reversal** | The familiar last step of the parodied ritual, then a 5-7 word "even though" flip; the screen delivers the specifics (praise first, a pause, then the insult) | 1Rd3 |
| **Understated recurrence** | A mildly ominous "it comes back" clause that grammatically leads into the first line | CRG |
| **Sting on the last word** | The final syllable lands on the impact (the bite), then a cut within a second | posture |
| **Inverted "but"** | Every earlier "but" brings bad news; the last one brings good news | p832 |

Ending rules (all 7 outliers):
- **No CTA, no "follow for more", no moral, no explicit summary.** The two controls that state a thesis or a moral (sloth, posture) are the ones with weak loops.
- **Strongest word last** in every sentence, especially the final one.
- **Tail 0.5-0.9 s** with no caption: a hero hold, a slow overhead drift or a reaction shot. Then a hard stop.
- **Loop seam**: the last frame matches frame 0's composition, or the last clause grammatically feeds the first, or the last location mirrors the first (floor and ceiling). The outliers' low like rates (median 1.85% against the controls' 3.0%) fit a replay-driven watch: people loop them rather than react.

---

## 6. Pacing stats

| id | role | sec | words | wpm | hook (words / s / wpm) | shots | ASL (s) | sentences | pivot every | like rate |
|---|---|---|---|---|---|---|---|---|---|---|
| CRGWDiIgMZ4 | out | 27.7 | 75 | 167 | 22 / 7.5 / 176 | 17 | 1.6 | 3 | acts split by breaths | 1.56% |
| yudJI1L8jlI | out | 35.5 | 100 | 172 | 15 / 5.2 / 174 | 25 (21 + 4 whips) | 1.4 | 6 | 3-5 s (new step) | 1.85% |
| 1Rd3_pXs6DU | out | 45.0 | 123 | 168 | 20 / 7.0 / 172 | 37 | 1.2 | 9 | 3.5-4.5 s | 2.5% |
| W3NlT3SKkmQ | out | 30.0 | 88 | 179 | 13 / 3.5 / 224 | 15 | 2.0 | 5 | 3-4 s | 1.94% |
| p832whe8hrI | out | 53.5 | 147 | 167 | 22 / 6.7 / 196 | 33 | 1.6 | 13 | 5.5 s | 2.9% |
| NEgarf1vDTU | out | 33.1 | 92 | 170 | 13 / 3.7 / 210 | 17 | 1.9 | 7 | about 4.7 s | 1.7% |
| 0BZ1C83I2R4 | out | 24.2 | 9 | 22 | visual, 0.5 s | 1 cut, about 13 setups | about 1.8 (setups) | 1 line | new framing every 1.5-2 s | 1.31% |
| MKRYulCq3Mo | ctrl | 32.4 | 90 | 172 | 16 / 4.8 / 201 | 25 | 1.3 | 6 | 5.8 s | 2.6% |
| -7MDLZCb1Mw | ctrl | 31.2 | 85 | 167 | 9 / 3.9 / 138 | 26 (22 + 4) | 1.4 | 5 | location change only | 3.0% |
| jHbhgBgaA34 | ctrl | 36.2 | 106 | 179 | 20 / 5.8 / 207 | 27 | 1.3 | 5 | 4.4 s | 3.4% |

**Medians over the 9 narrated videos (range):**

| Metric | Median | Range | Our target |
|---|---|---|---|
| Duration | **33.1 s** | 27.7-53.5 | 28-36 s for mechanism Shorts; 45-60 s only for stories and skits |
| Words | **92** | 75-147 | 80-100 |
| Words per minute | **170** | 167-179 | 165-180 overall; hook fastest, mechanism never above about 195, a reveal may slow to about 140 (the control that rushed its middle at 216 underperformed) |
| Hook sentence | **16 words / 5.2 s** | 9-22 words / 3.5-7.5 s | 13-20 words, done by 15% |
| Hook speed | **196 wpm** | 138-224 | 185-210, faster than the body |
| First spoken word | **0.0 s** | 0.0 in 9/9 | 0.0 s |
| Sentences | **6** | 3-13 | 5-8 |
| Words per sentence | **16.7** | 11.3-25 | 12-18; chain clauses with and / but / so / until |
| Gaps between sentences | 0.3-0.6 s | max 0.62 s (before the maggots turn) | 0.3-0.5 s; one longer pause allowed right before the turn |
| Pivot-word interval | **about 4.5 s** | 3.5-5.8 s | every 4-5 s |
| Average shot length | **1.4 s** | 1.2-2.0 | 1.3-1.6 s (about 7 pictures per 10 s) |
| Caption chunk | **2.4-2.6 words / 0.9 s** | 1-4 words / 0.4-1.2 s | 2-3 words |
| Tail after the last word | **0.7 s** | 0.5-1.1 | 0.5-0.9 s, caption-free |
| Audio | a bed under the whole voice; master about -11.5 to -12 LUFS; bed 6-8 dB under the voice; no true silence until the tail | | same |

Length vs views at channel level (176 mature with duration): the rank correlation is only +0.16, and the median outlier is flat (0.94-1.04) from 26 to 60 s. The 6 videos over 60 s (story formats) all did 1.0-2.5x. **Length is not a lever for mechanism Shorts; keep them tight.**

---

## 7. Topic clusters ranked by median and evergreen-ness

From `CHANNEL.md` (387 mature Shorts, about 2026-08 to 2026-10). "Evergreen" is our judgement: will a video on this topic still get searched and recommended in two years? "Code fit" is how well a code-only kit (Remotion, SVG, low-poly) can render the cluster's typical subject.

| Rank | Cluster | n | Median | p75/p25 | ≥2x share | Evergreen | Code fit | Read |
|---|---|---|---|---|---|---|---|---|
| 1 | Nature (animal and plant mechanisms) | 46 | **14.0M** | 1.65 | 11% | **High** | Low-medium (fur, flesh and wet skin are the hardest materials in code) | Highest and steadiest big cluster |
| 2 | Eerie true mystery | 6 | 14.0M | 1.86 | 17% | Medium | Medium | n=6, too small to trust |
| 3 | History and origins | 22 | **13.0M** | 2.18 | 9% | **High** | **High** (objects, buildings, tools, cutaways) | Second-highest median, timeless |
| 4 | Gross-out | 10 | 12.5M | **1.34** | 10% | High | Medium | Steadiest, but ad-suitability risk (section 9) |
| 5 | Fiction skits ("(fiction)", "(Patent Pending)") | 14 | 12.0M | 2.36 | **21%** | Medium (holiday tales are seasonal) | Medium (needs character acting) | The lottery tickets |
| 6 | Puzzles, riddles, thought experiments | 22 | 11.0M | 2.00 | 14% | **High** | High | Underrated: steady and code-friendly |
| 7 | Survival, danger, accidents | 21 | 11.0M | 2.38 | 14% | High | Medium | Crowded with imitators (0/6 hit 10K) |
| 8 | What-if hypotheticals | 15 | 11.0M | 2.24 | 7% | High | Medium | Crowded with imitators |
| 9 | Inside your body and health | 22 | 10.0M | 1.35 | 0% | High | Medium | Steady but never breaks out; most saturated imitator lane |
| 10 | Psychology, life lessons | 21 | 10.0M | 1.55 | 5% | High | Medium | Steady, rarely breaks out; earns likes not views |
| 11 | How it works, inventions, tech | 48 | 9.3M | 2.40 | 8% | **High** | **High** | The object must be something everyone touches |
| 12 | Heartwarming, rescue | 42 | 9.2M | 2.20 | 17% | Medium | Low-medium (animals) | Source of the biggest hits (prosthetics franchise) |
| 13 | Life hacks, DIY, food | 52 | 9.0M | 2.45 | 12% | Medium (claims age, safety risk) | Medium | Weakest median outlier (0.79x) |
| 14 | Odd true news | 36 | 8.0M | **3.08** | 11% | **Low** (news-pegged) | Medium | Widest spread; Meta "tragedy" monetization risk |
| 15 | Pop culture, film behind-the-scenes | 10 | 5.9M | 1.78 | 20% | Low (tied to releases) | Low (IP) | Lowest for Zack, yet the best lane for imitators (section 8) |

**Best combination of high median, low variance and evergreen:** nature, history and origins, gross-out, puzzles. **Best combination for a code-only kit:** history and origins, how-it-works (everyday objects), puzzles.

---

## 8. Outliers vs controls: what the top videos do that ordinary ones don't

The controls are not bad videos: they still did 10-14.6M. The difference between a 1x and a 3-6x Zack video is mostly **replay**. Outliers have *lower* like rates (median 1.85%, range 1.31-2.9%) than controls (median 3.0%, 2.6-3.4%) and the channel (3.5%), so they spread through loops and reach, not reactions.

| Lever | Outliers (n=7) | Controls (n=3) | Strength of signal |
|---|---|---|---|
| **Strong loop seam** (last frame or clause leads into frame 0) | 7/7 | 0/3 | strongest |
| **No moral, thesis or explicit summary at the end** | 7/7 | 1/3 (machine only) | strong |
| **One hero image held 2-5 s** (round plug, beak sliding on, slow-motion spray, drip, outlet arcs, skeleton, car on the lake bed) | 7/7 | 1/3 (the sample on the pedestal) | strong |
| **Immediate physical stakes** (a bite, a bullet, drowning, a death, a spray in the face) or the viewer's own body or daily object | 7/7 | 1/3 (posture, slow and abstract) | medium |
| **No hedges** ("may", "not necessarily") | 7/7 | 2/3 | medium |
| **Late reframe** (after 60%) | 6/6 narrated | 2/3 | weak: needed but not enough |
| Hook speed, total length, total words, overall wpm | no difference | no difference | none |
| Pace shape | fast hook, then either even (shark 164-177) or deliberately slowed for a reveal (maggots ends at about 136 wpm) | the sloth rushed its middle (216 wpm) after a slow hook | anecdotal: never rush the mechanism |

Same-cluster pairs:
- **Nature**: shark (4.07x) vs sloth (1.00x). Both 167 wpm. The shark starts mid-bite with a pronoun, holds one satisfying image, reframes at 66% and loops grammatically. The sloth names its subject, reveals the flip at 14%, spreads its peak over 5 cycle steps, hedges twice and ends on an explicit thesis.
- **How-it-works**: outlet (6.0x) vs machine (1.04x). The outlet video uses an object every viewer touched today and a folk image they half-believe. The machine is an unnamed art installation nobody has seen, and its loop is broken by a hard cut.
- **Body**: water-in-ear (3.36x) vs posture (1.00x). The ear video solves a problem in 30 s and ends in physical relief. The posture video lectures (moral + second example) and ends on a different character.

**Rules for our scripts:** start mid-action, build to one image, hold the reveal past 60%, make the last line or frame run into the first, never state the moral, never hedge, never rush the mechanism.

---

## 9. Imitator base rate: the verdict

From `IMITATORS.md` (63 channels; 39 YouTube channels under 6 months old).

**Odds that a new channel in this format reaches a 10K median: about 1 in 10, and about 1 in 20 in the core body niche.**
- Sample: 5 of 39 new channels (13%) have a median of 10K or more. Discovery through hashtag pages is biased toward channels that already get views, and dead or deleted channels are invisible, so the true rate is probably **5-10%**.
- **The usual outcome is a 1.2K median** (IQR 760-1.8K), then quitting: 16 of the 19 channels that stopped posting stalled below 10K.
- **Volume does not rescue a weak start**: 19 channels with 30 or more Shorts still sit under 10K (for example 92 uploads at a 143 median; 284 uploads at 5K). The winners show it early: one at a 78K median after 22 uploads, one at 12K after 6, and the ones with data already had 26K+ first-20 medians.
- **Saturation**: the 2026 Jul-Oct cohort (33 channels) sits at a 1.2K median with 3/33 at 10K. The body niche has 22 new channels and 1 winner.

| Sub-niche group (new channels) | n | Median of medians | At 10K+ |
|---|---|---|---|
| Body / "what happens if you..." | 22 | 1.1K | 1 |
| Survival / what-if | 6 | 0.8K | 0 |
| How-it-works / science | 5 | 1.4K | 0 |
| **History / military / pop-culture** | 6 | **23K** | **4** |

**What separates the imitators that made it** (new-channel winners 3DDose, Ctrlzfilms01, FixmyReading, ThePostulator, shwededfilms, plus the off-YouTube accounts):
1. **A sub-niche with an existing fan community**, not Zack's own core: game characters, superheroes and anime, military gear, history, religious mysteries. 4 of the 5 new YouTube winners. The fandom does the sharing.
2. **A repeatable series premise in the title** with one variable slot: "[Paradox]: [Franchise] Edition", "[N] Levels Of [Thing]", "[Old Thing] Vs [Modern Thing]", "What's Behind [Character]'s [Feature]?". Every winner has one; most losers title each video from scratch.
3. **A hand-built CG look, not generic AI video.** cg-3d: 4/7 channels at 10K+ (median of medians 12K). ai-3d: 6/43 (1.2K). ai-photoreal: 0/4. Low-poly accounts (Zeck Felms, polystoriesdaily, bob.figures.it.out) are among the biggest off-YouTube. Style and niche overlap, so this is a hint, not proof, but it favours us: code-rendered is by definition not the AI look.
4. **Comedy and a recurring cast or premise off YouTube**: the TikTok and Instagram breakouts (1.1M, 302K and 1.2M medians) are what-if society simulations, what-if comedy and a recurring couple. None of them is a fact channel.
5. **A fast verdict**: success shows within the first 20-50 uploads or not at all.
6. (Not for us now) **Language arbitrage**: Vietnamese and Bengali body/science channels reached 17-29K medians.

The one body-niche winner (FixmyReading, 25K) puts the original channel's name in its hashtags, which is a search-riding tactic we will not use.

---

## 10. Monetization notes

### Gross-out, sexual and violent topics vs ad suitability

Key rule: **on YouTube Shorts, views of content that conflicts with the advertiser-friendly guidelines are excluded from revenue sharing entirely** ("only views of content that follow our advertiser-friendly guidelines will be eligible", Shorts monetization policy). On Shorts, "limited ads" effectively means **zero revenue for that video**, so treat yellow as red.

What the advertiser-friendly guidelines say (support.google.com/youtube/answer/6162278; animated = "dramatized"):

| Topic | Full ads (green) | Limited (yellow, so zero on Shorts) | No ads |
|---|---|---|---|
| Shocking / gross | light or moderate, "obscured or shown in context for educational, documentary" purposes; procedures that focus on the procedure, not the body parts | graphic body parts "unobscured or intended to shock" | the whole purpose is to shock; gruesome parts filling much of the runtime even with context |
| Sexual | non-graphic sex education; jokes and innuendo without vulgar terms | innuendo like moaning sounds; animated sex acts in sex ed | sexual topics such as fetishes, tips, experiences; **sexual content in the thumbnail** |
| Violence (animated) | unrealistic, playful, fleeting | serious injury with the aftermath visible | ultra-graphic acts and injuries |
| Firearms | unmodified guns in a safe setting | guns used outside a controlled environment | **gun creation, modification, assembly or disassembly** |

Thumbnails and titles are judged separately and can be stricter.

What this means for the Zack format:
- **Zack's styling is the mitigation**: food-like flesh, amber cartoon fluid, a clean ivory skeleton, high-key light, an educational "how it works" frame. The gross-out cluster (12.5M median, the steadiest) mostly stays green because the gross beat is a short peak inside a mechanism, not the whole video.
- **Our rule:** gross is allowed as a 2-5 s money shot inside an explained mechanism, styled as food or toys, never in frame 0 of a real-injury story, never in the thumbnail. No gore longer than about 15% of runtime.
- **Sexual and toilet humour:** the "(Patent Pending)" bathroom skits are innuendo-free bodily humour and probably green. Anything sexual (fetishes, "tips", experiences, sexual thumbnails) is no-ads, and even green sex-ed sits in a "made for kids" grey zone because animation is a kids factor. **We skip sexual topics entirely**; the upside does not justify the revenue and policy risk.
- **Firearm internals ("how a gun's mechanism works") are no-ads.** Any history or military lane must stay away from firearm assembly or disassembly cutaways.

### YouTube vs TikTok vs Facebook

| | YouTube Shorts | TikTok | Facebook (Reels) |
|---|---|---|---|
| Eligibility | YPP: 1,000 subs + 10M qualified Shorts views in 90 days, then a manual channel review (R5) | Creator Rewards: 10K followers, 100K views in 30 days, 18+ (R5) | Content Monetization program, eligibility shown in the Professional Dashboard; third-party guides disagree on thresholds and on whether it is invite-only (unverified) |
| Length | any Shorts length; the house 28-40 s is fine | **only posts of at least 1 minute earn** (R5), so the 28-40 s house format earns nothing there | not measured |
| Ad suitability | non-advertiser-friendly views excluded from the Shorts pool | originality-focused; unoriginal or reused content loses For You eligibility | Meta's monetization policies restrict "tragedy and conflict" (real deaths, casualties, injuries), sexual/suggestive and objectionable content (secondary sources; the official page was not fetched) |
| Originality | reused or "inauthentic" content is ineligible (R5) | same | March 2026 push: unoriginal posts are deprioritised and can be demonetized |
| Fit for this format | the home platform; our data is all from here | the new viral imitators are here (what-if comedy, society sims), but rewards need 60 s+ cuts | a large audience for short animated explainers is often reported, but **we have no Facebook data**; Zack's Facebook and TikTok numbers could not be pulled (TikTok handle mismatch, Instagram needs login) |

Implications:
- **True-tragedy topics** (the maggots/lonely-death story, "drifted at sea", odd news) carry Facebook monetization risk even when YouTube treats them as green. Prefer mechanism topics.
- **TikTok needs a second cut.** Either a 60-75 s story version (Zack's few 60 s+ videos did 1.0-2.5x) or treat TikTok as reach only.
- All platforms need the AI-voice disclosure we already use (R5): YouTube "AI use = Yes", TikTok "AI-generated content" on, Meta AI label.
- Shorts revenue per view is low (third-party estimates are cents per thousand views; not verified here). This format pays through volume and through funnelling viewers to long-form, not through per-Short revenue.

---

## 11. Recommendation: which sub-niche a new code-only channel should enter

**Enter "how old things actually worked": history and engineering mechanisms, built around cutaways of objects.** Castles and their defences, siege engines, ancient locks and doors, ships and canals, armour, Roman and medieval machines, the first versions of everyday objects. Leave out firearm internals and real tragedies. Run it as recurring series premises, in a distinct code-rendered low-poly/toy-real look. Use the Zack skeleton (section 1), usually with the **failure ladder** ("an attacker tries three things; each one is defeated by a feature") or the **part-to-reason ladder** with a late reframe ("the odd feature was the point").

Why this one:
1. **It ranks high on Zack's own data.** History and origins has a 13.0M median, the second-highest cluster, it is evergreen, and "Why X" (1.12x) and "The X" (1.22x) titles fit it naturally.
2. **It is the only imitator lane where new channels usually win.** History, military and pop-culture: 4 of 6 new channels at 10K+ (23K median of medians), against 1 of 22 in body and 0 of 6 in survival/what-if. The sample is small and biased, but the gap is large.
3. **It suits code better than any other cluster.** The protagonist is a rigid object, and rigid objects, cutaways, x-ray glows, arrows, gears and stone are exactly what a code kit renders well. Fur, wet skin, flesh and acting humans (nature, body, heartwarming, skits) are where a code render looks cheapest next to Zack's.
4. **It is ad-safe by default.** Mechanisms, engineering and history in an educational frame are green, as long as we avoid firearm assembly/disassembly, visible serious injuries and real tragedies.
5. **It has fan-community pull without IP risk.** Military-history and medieval fans share content like the pop-culture fandoms do, but we never need anyone else's characters. (Pop culture is where imitators win most, but it means trademarked characters we cannot and will not copy.)
6. **It works as series premises with one variable slot**, which is what every winning imitator has: "Why [Old Thing] Had [Odd Feature]", "How [Defence] Stopped [Attack]", "[Old Tool] Vs [Modern Tool]", "The [Thing] Paradox".

**Upside slot (about 20-25% of uploads):** a **wordless "secret crew inside an everyday object" gag series** with our own recurring low-poly crew (the outlet video's skeleton, 6.0x, 66M). It needs no translation, it matches the "recurring cast + comedy" pattern behind every off-YouTube breakout, and it cross-posts to TikTok, Reels and Facebook for reach. Treat it as lottery tickets: fiction skits are Zack's highest-variance cluster (21% at 2x or more, but a wide spread).

**Do not enter:**
- Body / "what happens if you..." (most saturated, 1/22).
- Survival what-if (0/6).
- Pop-culture IP (IP and trademark risk).
- Gross, sexual or true-tragedy as a lead lane (Shorts revenue exclusion, Meta tragedy rule).
- Nature as this channel's lead. It is Zack's steadiest cluster, but code renders creatures weakly, and our ocean/animal explainer kit already covers that ground.

**Expectations and kill rule:** budget for the base case of about a 1K median after 30-50 uploads. If the median is under 3K at 30 uploads, change the niche, not the volume (IMITATORS.md). One upload a day is enough to read the signal; Zack's 5 a day is a lottery strategy that only works with his 10M floor.

---

## 12. Writer checklist (every Zack-format script)

- [ ] `references:` lists the 2-3 closest corpus videos (id, url, views, outlier_score) and a beat-alignment table (our beat, their beat + timestamp, the device borrowed). No wording borrowed.
- [ ] Title: Title Case, about 7 words, one genre emoji; "Why X" or "The X" preferred; never "The Person Who Did Y" or a gerund.
- [ ] Frame 0 shows the action or anomaly; the first word is at 0.0 s; no intro, question to camera or channel name.
- [ ] Hook: one sentence, 13-20 words, done by 15%, said faster than the body, ending on a comma or a stinger noun.
- [ ] 80-100 words, 165-180 wpm overall, no mechanism sentence above about 195 wpm; a pivot word every 4-5 s; gaps ≤0.6 s.
- [ ] Each ladder rung is a new kind (tool, place, sense, field, scale), not more of the same.
- [ ] One money shot, held 2-5 s, at about 50-70%.
- [ ] The reframe lands after 60% and reuses a noun planted in the first 30%.
- [ ] The last sentence mirrors the opening (verb, noun or place) and ends on its strongest word; the last frame matches frame 0; 0.5-0.9 s caption-free tail.
- [ ] No moral, no thesis line, no hedges, no CTA.
- [ ] Every noun has a shot within 0.5 s; every abstract word has a prop or icon from section 3; one picture-only detail rewards rewatching.
- [ ] Ad check: no firearm internals, no visible serious injury, no real tragedy, no sexual topic, gross ≤15% of runtime, nothing gross in the thumbnail.
- [ ] Facts sourced in the description; every unit on screen checked (the ear video printed m/s for an acceleration).
- [ ] `python3 scripts/originality_check.py <script.md> research/corpus research/library/transcripts` prints PASS.

## Sources

- Annotated videos: the 10 files listed at the top of this playbook, with contact sheets in `sheets/`.
- Channel and imitator data: `CHANNEL.md`, `channel.json`, `IMITATORS.md`, `imitators.json`.
- Policy: `research/R5/report.md`; [YouTube advertiser-friendly content guidelines](https://support.google.com/youtube/answer/6162278); [YouTube Shorts monetization policies](https://support.google.com/youtube/answer/12504220); [Meta, "Rewarding Original Creators on Facebook" (Mar 2026)](https://about.fb.com/news/2026/03/rewarding-original-creators-on-facebook/); [Facebook creators blog, supporting original content](https://creators.facebook.com/blog/supporting-original-content-on-facebook); Meta monetization restriction categories from secondary coverage only: [TechCrunch 2017](https://techcrunch.com/2017/09/13/facebook-monetization-2/), [Tubefilter](https://www.tubefilter.com/?p=101172). Facebook eligibility thresholds: third-party guides only, unverified.
