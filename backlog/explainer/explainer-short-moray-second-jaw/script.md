---
id: explainer-short-moray-second-jaw
niche: explainer
format: Short 9:16 (1080x1920)
ending: loop
title: How A Moray Eel Bites You
alt_titles:
  - The Reef Hole With Two Mouths
  - Why You Never Hand-Feed A Moray Eel
series_formula: "How [ocean animal] [hurts] you" (PLAYBOOK §7, the Zack D. Films series formula; 6mRR91AbxjQ "How Horseflies Bite You"). Line 1 acts the title out as a risky act in progress (your fingers at the hole), and the body pays it off with the real bite mechanism and the real bite setting (hand-feeding).
target_runtime: "71.65 s MEASURED (Kokoro pilot on the Spark CPU: speech 0.11-71.45 s, then the loop tail; audio/report.json). The window is 66-80 s and it must never go under 61 s (TikTok Creator Rewards minimum, see section 6). If a re-voice ever comes in under 64 s, use [speed: 0.92]; do not pad the script."
target_words_per_min: "PLAYBOOK §8 TTS band is 180-230. 221 words, measured: 186 wpm over the speech span, 185 wpm over the full runtime. The hook is read at body speed (FLY reads its hook at or below body speed so the number lands)."
timing_model: "MEASURED. A Kokoro am_michael 0.96 pilot ran on the Spark CPU (TTS_THREADS=2, nice 10, 2026-11-01 ~11:49 UTC): 72.05 s raw, mix 71.65 s, -14.0 LUFS, timing coverage 1.0. Word timings are in audio/captions.json, and every timestamp in this file and in storyboard.json comes from them. The calibrated pre-TTS estimate in gen_storyboard.py (--estimate) predicted 70.9 s, within 1%. The previous draft's 190 wpm body / 240 wpm hook model was wrong at 0.96. The pilot mix is at studio/public/episodes/explainer-short-moray-second-jaw/mix.wav on the Spark."
voice: am_michael
speed: 0.96
voice_notes: Kokoro am_michael at speed 0.96 (pipeline/audio/config.py default), dry and matter-of-fact. Measured paragraph gaps are 0.1-0.3 s. The one deliberate longer beat is before "Relax." ([pause: 0.2] + gap = 0.4 s measured, with the music drop). No silence is longer than 0.5 s.
music: deep_ocean
music_notes: "deep_ocean bed, ducked under VO. It drops out for the turnstile line: entry 1 ends at the start of 'Relax.' (fadeOut 0.25) and entry 2 starts at 'If you were a fish' (fadeIn 0.3). That is two music entries, because the schema has no mute cue."
references:
  - id: 6mRR91AbxjQ
    url: https://www.youtube.com/shorts/6mRR91AbxjQ
    title: How Horseflies Bite You (Zack D. Films)
    views: 13689674
    outlier_score: 1.71
    why_chosen: "Closest format: one creature's mouthparts told part by part to 'you'. We borrow the counted inventory as a progress bar ('mouth one / mouth two' chip), one everyday-tool analogy per part shown literally for ~1 s (fish hooks, a monster-movie mouth), damage moving one layer deeper (hand -> you as prey -> swallowed), a yellow highlight on the part being named, the purpose reveal in the last clause (0:24.9) and a last frame that matches frame 1."
  - id: XFFjxTllpoA
    url: https://www.youtube.com/shorts/XFFjxTllpoA
    title: What if You Ate The Most Poisonous Animal in the World? (Casual Geographic)
    views: 7931305
    outlier_score: 1.69
    why_chosen: "The 60 s skeleton that carries a mechanism Short past one minute. We borrow the false-reassurance turnstile at ~46-50% with a new background on the next word (0:27), the worst outcome told as a joke tied to an everyday thing (0:33-0:41), the one-clause mechanism aside paid in the next line (0:17-0:21), and the reality flip where a safety rule is broken by an ordinary human habit (0:43-0:47)."
  - id: jw6bS-WL4F4
    url: https://www.youtube.com/shorts/jw6bS-WL4F4
    title: Why This Tiny Jellyfish Is Much Worse Than You Think (Casual Geographic)
    views: 6716278
    outlier_score: 1.43
    why_chosen: "Ocean Short with a comic misdirect list (famous threats plus one absurd item, 0:03-0:08), then a pivot, then the subject named at ~17% against a scale prop (0:10), and a re-hook right after the most graphic image (0:31). Its button is a callback to an opening detail (0:54). We drop its self-harm hook angle (R5 / ad safety)."
rival_same_topic:
  id: CQXRzLX6aXk
  url: https://www.youtube.com/shorts/CQXRzLX6aXk
  title: Moray Eels Have Two Sets Of Jaws (Zack D. Films)
  views: 9926864
  note: "This is the demand evidence and our closest rival (~1.0x a ~10M channel median). Its transcript is now in research/library/transcripts/CQXRzLX6aXk.txt (en-orig auto-subs, fetched on the Spark), so the originality gate checks against it. That video is a 34 s, third-person, mechanism-only clip: catch, throat jaw, swallow, then why (slim body, holes, narrow head, poor suction). Ours shares none of its wording. It differs in POV (you, your hand, you as the fish), the bite-on-a-human ladder, the turnstile, the hand-feeding twist and the loop. We also deliberately drop its 'narrow head' explanation (see section 5, F3)."
demand_evidence: "CQXRzLX6aXk 9.9M (above); Zack D. Films 'Japanese Eels Can Escape A Fish's Stomach' 34M (3.4x); Caters moray-attacks-diver clip 638K. See backlog/explainer/TOPICS.md row 13 and backlog/explainer/evidence/zackd_shorts.jsonl."
originality: "python3 scripts/originality_check.py backlog/explainer/explainer-short-moray-second-jaw/script.md research/corpus research/library/transcripts -> PASS (see review.json)"
status: "final script 2026-11-01 ~11:55 UTC. Facts in section 5 checked. The TTS pilot is measured and the storyboard is timed to it. Ready to render."
---

# How A Moray Eel Bites You (Short)

**Premise.** Your fingers are resting at a dark gap in a reef wall. Inside is a moray eel, and a moray has two mouths: the front jaw, and a second jaw in its throat (the pharyngeal jaw). The ladder stays on you. First, mouth one's teeth curve back like fish hooks (shape only). Then it bites a hand in its home without looking. Then the worst thing you can do is pull, because the hooks point inward. That is the most graphic beat, and a handshake joke closes it. The turnstile reassures you ("it's not trying to eat you"), which is true for a wild moray defending its hole. Then the viewer becomes the fish and meets mouth two: the throat jaw launches, grabs and hauls you down hand over hand. That is the spectacle peak, and the spine closes at ~75%. The twist breaks the turnstile's rule. Plenty of bites come from the friendly morays people feed by hand. They have learned that fingers smell like fish, and they can barely see. So the stinger is a purpose reveal that reverses the turnstile: this time it really is trying to eat your fingers. The last word, "fingers", runs straight into line 1 ("Your fingers...") on the loop.

**Honesty note.** The throat jaw has no record of doing anything to a person; it is a swallowing tool for prey. So mouth two is only ever met "if you were a fish". The hook promises a hole with two mouths (true) and never says mouth two touches your hand, and the stinger does not mention the second mouth. The joke beats make no injury claims. The "counting to nine" finger-loss joke from the previous draft is gone. Finger loss is reported (see F9), but only through secondary sources, so it is not used as a punchline.

**Spine loop:** what is mouth two? It opens in line 1. The chip counts mouth 1 at 0:14.1 and mouth 2 at 0:40.3 (56%), and the loop is paid off fully at "until you're gone" (0:53.9, 75%).
**Second loop:** is it trying to eat you? "Relax, it's not" at 0:36.5 (51%), reversed by the stinger at 1:08.4-1:10.7.
**Progress device:** a two-slot chip at the top-left, `MOUTH 1 · MOUTH 2`. Slot 1 lights yellow on "one" (0:14.1) and slot 2 lights red on "two" (0:40.3), then flashes on "launches" (0:46.7). This is the 6mRR91AbxjQ counted-inventory device, here counting two jaws.

## 1. Beat alignment

Our times are measured Kokoro word starts (`audio/captions.json`, speed 0.96, total 71.65 s). Reference times were rechecked against `research/corpus/explainer/6mRR91AbxjQ.md`, `XFFjxTllpoA.md` and `jw6bS-WL4F4.md`.

| # | Our beat | Our time (% of 71.65 s) | Reference id + timestamp | Device borrowed | How we adapt it |
|---|---|---|---|---|---|
| 1 | S1 HOOK: risky act in 2P + counted promise | 0:00.1-0:02.7 (0-4%), 9 words | 6mRR91AbxjQ 0:00.2-0:05.4 (title as a 2P scenario, then a count; hook read slower than the body); XFFjxTllpoA 0:00 (title as a promise) | A count in the hook that works as a progress bar; "you" in word 1 | The count is "two mouths". The moray is on screen in frame 1 (two pale eyes in the gap) but named only at 0:08.7. Read at body speed, not faster. |
| 2 | S2 MISDIRECT (comic list) + PIVOT | 0:02.9-0:08.3 (4-12%) | jw6bS-WL4F4 0:03-0:08 (comic list of famous threats ending on an absurd item, laugh by ~0:05), 0:08 (pivot) | Misdirect list, then pivot to the unseen threat | Voiced list: sharks, jellyfish, "one suspicious crab" (the absurd item). An Options card ticks each (SVG ticks). On "never" the camera whips back to the crack, and a red ring with `NOT ON THE LIST` lands on "crack". |
| 3 | S2 REVEAL + SCALE | 0:08.4-0:13.6 (12-19%) | jw6bS-WL4F4 0:10 (named at ~17% next to a scale prop) | Name the subject late, against a size the viewer knows | Named at 0:08.7 (12%). Honest scale card at 300 px/m: a 3 m giant moray beside YOU 1.75 m. Spoken as "longer than you're tall". |
| 4 | S3 RUNG 1: mouth one, hooked teeth (plant) | 0:13.8-0:18.5 (19-26%) | 6mRR91AbxjQ 0:05.4-0:09.5 (first part + household-tool analogy), 0:11.3 (analogy shown literally ~1 s) | Counted part + one tool analogy shown literally | Teeth curve back, and for ~1.1 s the tooth row is overlaid with steel fish hooks. Shape only: the consequence is held back to rung 3 (PLAYBOOK §4, plant then pay). Chip slot 1 lights. |
| 5 | S3 RUNG 2: it bites a hand in its home | 0:18.7-0:23.7 (26-33%) | 6mRR91AbxjQ 0:09.5 ("two more" escalator: harsher, with a violent verb aimed at you); XFFjxTllpoA 0:23 (comic understatement at the end of a line) | Next part strictly worse, aimed at you; a deflating tag | "Bitten first, questions later" lands as the head lunges out of the gap (impact, shake). It plants the eyesight fact that the twist pays off. |
| 6 | RE-HOOK: rhetorical question (micro loop) | 0:23.9-0:27.4 (33-38%) | PLAYBOOK §3 re-hook device 1 (RQ answered in 1-3 words: SPERM, ERAS, PLANT, ORCA); no Shorts exemplar, so this one is long-form-derived | Question answered in one word in the next line | "The worst thing you can do next is the first thing you'll do." The answer comes 0.2 s later: "Pull." |
| 7 | S3 RUNG 3: pull (callback pays the plant) | 0:27.6-0:33.0 (39-46%) | 6mRR91AbxjQ 0:12.3-0:15.6 (analogy turned into motion, damage goes one layer deeper, the worst verb on "you"); PLAYBOOK §4 "facts become the weapon" | Callback to an earlier rung kills the obvious escape | The hooks overlay comes back; the red arrow and `DON'T PULL` land on "yanking". This is the most graphic beat, and it shows no wound. |
| 8 | Joke punch on the worst image | 0:33.2-0:36.1 (46-50%) | XFFjxTllpoA 0:33-0:41 (the worst outcome said as a joke about an everyday thing) | Gallows joke instead of a gore statement | The handshake you don't get to end. Tag: `YOU LET GO SECOND`. |
| 9 | S4 TURNSTILE (false reassurance) | 0:36.5-0:38.5 (51-54%) | XFFjxTllpoA 0:27 (6-word false reassurance at 46%, new background on the turn); jw6bS-WL4F4 0:31 (re-hook right after the most graphic image, 53%) | 4-7 word reassurance, then a background change on the next word | "Relax, it's not trying to eat you." (7 words.) The reason holds: a wild moray in its hole bites to defend, not to feed. Music drops, plain dark card with an SVG tick, then a hard cut to teal on "If". |
| 10 | Spine payoff: you as the fish meet mouth two | 0:38.6-0:40.7 (54-57%) | 6mRR91AbxjQ 0:18.1 ("next" reopens the inventory after the peak and switches axis, pain -> disgust) | Inventory continues on a new axis | The axis turns outside-in: the viewer becomes the prey (You fades out, Fish pops in). Chip slot 2 lights on "two". |
| 11 | S3 MECHANISM aside | 0:40.9-0:44.1 (57-62%), 12 words, 3.2 s | XFFjxTllpoA 0:17-0:21 (real term + plain verb, paid within 4 s); 6mRR91AbxjQ 0:20.6 (one-clause mechanism) | 3-4 s aside, paid off in the very next line | "Its throat can't suck you in, so a second jaw does it." The term `PHARYNGEAL JAW` is shown, not said. It pays off on "launches". |
| 12 | S5 PEAK (spectacle): the throat jaw launches | 0:44.2-0:49.5 (62-69%) | 6mRR91AbxjQ 0:11.3 (analogy shown literally for ~1 s), 0:09.5-0:15.6 (a motion verb taking the damage a layer deeper) | Literal analogy + the most shareable image at the peak | Cutaway: the oral jaw closes, the yellow throat jaw slides forward out of the throat (0.35 s), and on "monster-movie mouth" the tag `A MOUTH INSIDE A MOUTH` appears (generic, no film IP). |
| 13 | S5 PEAK close: ratchet, spine closes | 0:49.6-0:54.3 (69-76%) | 6mRR91AbxjQ 0:15.6 (first full stop right after the worst image); XFFjxTllpoA 0:41 (loop A closes at ~70%) | Peak ends on a finality word; spine closes in the corpus 64-100% band | The ratchet is one clause ("hand over hand"): 4 grabs ticking `1 2 1 2`, and the fish slides behind the head shell on "gone". |
| 14 | S6 TWIST: reality flip, the rule broken | 0:54.6-0:59.5 (76-83%) | XFFjxTllpoA 0:43-0:47 (the hypothetical really happens on purpose; the safety rule broken by a human habit); PLAYBOOK §5 "opening rule turned against you" | Change axis after the peak: the hidden threat becomes the tame one people create | The turnstile's rule ("not trying to eat you") was true of the wild moray. The friendly, hand-fed ones break it. DipBlack, then a feeding-site wide (Diver + moray half out of the wall). |
| 15 | TWIST mechanism in 2P | 0:59.7-1:04.3 (83-90%) | XFFjxTllpoA 0:47 ("safe if..., but one small error"); jw6bS-WL4F4 0:41-0:45 (a specific 2P scenario: "if you're swimming") | 2P conditional; one human habit causes the danger | "If you've ever fed one by hand, you taught it that fingers smell like fish." Smell lines drift from the hand to the moray. |
| 16 | Callback (stack the plant) | 1:04.5-1:08.2 (90-95%) | jw6bS-WL4F4 0:54 (button: callback to an opening detail + comic line) | Callback to an early plant | The eyesight plant from 0:19.0 comes back: "it can't tell which part is the fish". The fish fades out, leaving only a ghost outline at your fingers. |
| 17 | S7 STINGER (purpose reveal) + loop | 1:08.4-1:11.5 (95-100%), 10 words, loop tail to 1:11.65 | 6mRR91AbxjQ 0:24.9-0:27.6 (purpose reveal in the last clause, then the final frame = frame 1); XFFjxTllpoA 0:55 (no CTA, hard stop) | End on the strongest word, cut within 1 s, seamless loop | "This time, it really is trying to eat your fingers." It reverses the turnstile, ends on "fingers", and the frame-1 layers are reused verbatim, so the loop reads "...your fingers. / Your fingers just brushed a hole with two mouths." |

### Open loops

| Loop | Opens | Closes | Target (PLAYBOOK §8) |
|---|---|---|---|
| Spine: "two mouths" (what is mouth two?) | 0:00 | 0:40.3 named, 0:53.9 fully paid ("until you're gone", 75%) | spine closes 64-100% (median ~70%) |
| Who is it after? (the misdirect) | 0:02.9 | 0:07.2 ("the crack") | 2-6 s micro |
| Micro: what is the worst move? | 0:23.9 | 0:27.6 ("Pull.") | 1-3 s |
| Turnstile: is it really not trying to eat you? | 0:36.5 | 1:08.4-1:10.7 (stinger reverses it) | runs to the end on purpose |
| Micro: why a second jaw? | 0:40.9 | 0:46.7 ("launches") | 4-6 s |
| Twist: which moray bites? | 0:54.6 | 1:04.3 | twist 75-90% |
| Replay | 1:11.45 (the last word "fingers" + the frame-1 layers) | line 1 on replay | loop |

A micro loop or re-hook opens about every 8-12 s: 2.9, 13.8 (count card), 23.9, 36.5, 40.9, 54.6, 64.5.

## 2. Pacing self-check (PLAYBOOK §8 / §10)

| Metric | Target | This script (measured Kokoro pilot) |
|---|---|---|
| Runtime | 60-90 s, never < 61 s | 71.65 s |
| Words / wpm | 180-230 (TTS) | 221 words / 186 wpm speech, 185 overall |
| Hook | ≤ 12 words, ≤ 3 s, "you" in first 10 words, subject on screen in frame 1 | 9 words, 2.6 s (0.11-2.71 s), "Your" is word 1, eyes in the gap (and a 0.75 s x-ray of the throat jaw) from frame 0 |
| Subject named | late, after it is shown | 0:08.7 (12%) |
| First rung | ≤ 8 s | the misdirect pivot at 0:06.9, the reveal at 0:08.4, the first counted rung at 0:13.8 (the jw6bS-WL4F4 misdirect shape carries 0:03-0:10, as in the reference) |
| Explicit verbal re-hooks | Shorts median ~10 s (6.5-23) | 6.9 (pivot), 13.8 (count card), 23.9 (RQ), 36.5 (turnstile), 38.6 (you as fish), 54.6 (twist), 64.5 (callback). Max gap 16.0 s (38.6 -> 54.6), filled by the launch/ratchet action and the chip flash |
| Turnstile | 45-55%, 4-7 words | 0:36.5 = 51%, 7 words |
| Peak | 55-75% | mouth two named at 56%, launch 65%, spine closes 75% |
| Twist | 75-90% | 0:54.6-1:08.2 = 76-95% |
| Stinger | 90-100%, 4-15 words, no CTA | 1:08.4 = 95.5%, 10 words, ends on "fingers", no CTA, no advice |
| "You" in sentences | ≥ 60% | 15 of 18 (83%). Only the twist line, the callback line and the bare "Pull." have no "you" |
| "You" words | 12-20 / min, ≥ 5% of words | 20 = 16.7 / min, 9.0% of words. There is no stretch without "you" in the middle (the previous draft had a 23 s gap) |
| Numbers | 5-8 / min | 6 spoken number words (two, one crab, three metres, mouth one, mouth two, second) = 5.0 / min, or ~8.4 / min with the stats.py method that also counts pronoun "one". The one hard measure, 3 m, comes with the you-comparison "longer than you're tall", and 1.75 m sits beside it on screen |
| Sentence shape | Shorts avg 12-16, chained, few full stops before the payoff | 18 sentences, avg 12.3 words, longest 17. The punch lines are "Pull." and the 7-word turnstile |
| Rung length | a new rung every 3-6 s | every paragraph is 2.0-5.4 s of speech (the longest are the misdirect and the pull, 5.4 s) |
| Jokes | none needed before the midpoint; every 4-6 s in comedy Shorts after it | crab 0:06.0, questions later 0:22.7, handshake 0:33.8, as-a-fish 0:39.1, monster-movie mouth 0:48.3, which part is the fish 1:06.8 |
| Pauses | none over 0.5 s | measured: 0.4 s before "Relax." (deliberate, music drop) and 0.3 s before the twist (dipBlack); all others 0.1-0.3 s |

## 3. Script (voiceover = burned-in captions)

Hook first line: **"Your fingers just brushed a hole with two mouths."**
Hook first visual: **the reef wall fills the frame. A black oval gap sits at the centre (y 38%), with two small pale eyes and a lip line inside it. A bare hand in a blue wetsuit sleeve reaches in from the right, fingertips ~40 px from the gap. The headline `2 MOUTHS` is red, and the chip `MOUTH 1 · MOUTH 2` sits top-left with both slots dark. Frame 0 is the cover and the loop frame.**

Captions: 3 words per card, y 0.70, fontSize 88, uppercase. Emphasis (red) on: two, mouths, hooks, pull, bitten, second, gone, friendly, fingers. On-screen text uses kit Headline/Tag white uppercase with one red accent per scene. Ticks and crosses are SVG primitives, never ✓/✗ glyphs.

### S1 HOOK (0:00.1-0:02.7)

**[0:00.1]** Your fingers just brushed a hole with two mouths.
  *On screen:* `2 MOUTHS` (red), chip with both slots dark; eyes blink at 1.4 s

### S2 MISDIRECT + PIVOT (0:02.9-0:08.3)

**[0:02.9]** You checked for sharks, jellyfish and one suspicious crab, never the crack you're touching.
  *On screen:* `CHECKED FOR`: SHARKS / JELLYFISH / SUSPICIOUS CRAB, each with an SVG tick on its word, then on "never" a whip back to the gap; on "crack" a red ring + `NOT ON THE LIST`

### S2 REVEAL + SCALE (0:08.4-0:13.6)

**[0:08.4]** It's a moray eel's home, and the biggest reach three metres, longer than you're tall.
  *On screen:* `MORAY EEL`, then the scale card: `GIANT MORAY: UP TO ~3 M` vs `YOU: 1.75 M`

### S3 RUNG 1: MOUTH ONE (0:13.8-0:18.5)

**[0:13.8]** Mouth one is right by your hand, its teeth curved backwards like fish hooks.
  *On screen:* chip slot 1 lights yellow on "one" · `TEETH CURVE BACKWARD` · hooks overlay the tooth row for ~1.1 s on "hooks"

### S3 RUNG 2: THE BITE (0:18.7-0:23.7)

**[0:18.7]** It can barely see you, so a hand in its home gets bitten first, questions later.
  *On screen:* `EYESIGHT: POOR` (eyes dim) · on "bitten", the head lunges out of the gap + `DEFENDING ITS HOME` (red) · `QUESTIONS: LATER`

### RE-HOOK (0:23.9-0:27.4)

**[0:23.9]** And the worst thing you can do next is the first thing you'll do.
  *On screen:* `WORST MOVE?` (red) · `= FIRST INSTINCT`

### S3 RUNG 3: PULL (0:27.6-0:33.0)

**[0:27.6]** Pull. Those hooks point inward, so yanking back drags your hand across every one.
  *On screen:* `PULL` (red) + SVG cross · `POINT INWARD` · on "yanking", the red arrow outward, the tooth row glows red, `DON'T PULL`; no wound, no blood

### PUNCH (0:33.2-0:36.1)

**[0:33.2]** It's the one handshake on the reef you don't get to end.
  *On screen:* `THE HANDSHAKE` · `YOU LET GO SECOND`

### S4 TURNSTILE (0:36.5-0:38.5)

**[0:36.5]** Relax, it's not trying to eat you.
  *On screen:* `IT'S NOT TRYING TO EAT YOU` + SVG tick (green), held alone on a dark card; the music is out

### S5 PEAK (0:38.6-0:54.3)

**[0:38.6]** If you were a fish, you'd meet mouth two.
  *On screen:* YOU fades out and a grey fish pops in its place, `YOU (AS A FISH)` · `MOUTH 2` (red) · chip slot 2 lights red on "two"

**[0:40.9]** Its throat can't suck you in, so a second jaw does it.
  *On screen:* `WEAK SUCTION` + a cross over stalled flow lines · the throat jaw glows yellow · `PHARYNGEAL JAW`

**[0:44.2]** The front teeth catch you, then that jaw launches out of its throat like a monster-movie mouth.
  *On screen:* `MOUTH 2: THROAT JAW` · `A MOUTH INSIDE A MOUTH` · chip slot 2 flashes on "launches"

**[0:49.6]** It grabs you, and the jaws swap grips, hand over hand, until you're gone.
  *On screen:* `HAND OVER HAND` · grab counter `1 2 1 2` · the fish slides behind the head shell on "gone"

### S6 TWIST (0:54.6-1:08.2)

**[0:54.6]** But plenty of bites come from the friendly ones, the morays people feed by hand.
  *On screen:* `THE FRIENDLY ONES` (red) · `FEEDING SITES`

**[0:59.7]** If you've ever fed one by hand, you taught it that fingers smell like fish.
  *On screen:* `YOU TAUGHT IT` · `FINGERS = FISH SMELL` (yellow), with smell lines drifting from the hand to the moray

**[1:04.5]** And it can barely see, so it can't tell which part is the fish.
  *On screen:* `EYESIGHT: POOR` · the fish fades out, leaving a ghost outline at the fingertips · `WHICH PART IS THE FISH?`

### S7 STINGER (1:08.4-1:11.45, loop tail to 1:11.65)

**[1:08.4]** This time, it really is trying to eat your fingers.
  *On screen:* hard cut to the frame-1 layers verbatim (`2 MOUTHS`, chip dark, hand at the gap); on "fingers", a red ring snaps onto the fingertips; the voice stops and the mix ends 0.2 s later (loop ending), then the loop

### Narration block (pipeline input: one paragraph = one scene)

```narration
[music: deep_ocean] Your fingers just brushed a hole with two mouths.

You checked for sharks, jellyfish and one suspicious crab, never the crack you're touching.

It's a moray eel's home, and the biggest reach three metres, longer than you're tall.

Mouth one is right by your hand, its teeth curved backwards like fish hooks.

It can barely see you, so a hand in its home gets bitten first, questions later.

And the worst thing you can do next is the first thing you'll do.

Pull. Those hooks point inward, so yanking back drags your hand across every one.

It's the one handshake on the reef you don't get to end.

[pause: 0.2] Relax, it's not trying to eat you.

If you were a fish, you'd meet mouth two.

Its throat can't suck you in, so a second jaw does it.

The front teeth catch you, then that jaw launches out of its throat like a monster-movie mouth.

It grabs you, and the jaws swap grips, hand over hand, until you're gone.

[pause: 0.2] But plenty of bites come from the friendly ones, the morays people feed by hand.

If you've ever fed one by hand, you taught it that fingers smell like fish.

And it can barely see, so it can't tell which part is the fish.

This time, it really is trying to eat your fingers.
```

SFX cues live in `storyboard.json` (word-anchored), not in the narration, so the auto-SFX regexes in config.py do not double them. Pronunciation check on the pilot: "moray" should come out as /məˈreɪ/ or /ˈmɔːreɪ/. If Kokoro says "Murray", respell it as "mor-ay" in the narration only.

## 4. Shot list

The storyboard is `storyboard.json`, built by `gen_storyboard.py` from the measured word timings. It is zod-valid (`npm run validate` on the Spark, schema md5 5e02b4bb identical to the Mac), and `scripts/check_storyboards.py` on the Spark reports it ready: all components registered, audio present, longest visual hold 2.5 s. A 14-21 frame stills sheet was rendered on the Spark and reviewed: `out/stills/explainer-short-moray-second-jaw_storyboard.jpg`. Times below are scene starts. Every split inside a scene is anchored to the word in quotes, not to a guessed second.

Kit components used: Ocean, Options, Headline, Tag, ScaleBar, You, Diver, GreatWhite. Inline static SVG, the **minimum set of 7 unique drawings** (12 states):
1. coral wall with an evenodd hole, plus a hole-dark oval
2. moray: side head closed / side head open (recurved teeth), plus one full side body
3. hand in a wetsuit sleeve (one pose; the fed fish is a separate layer at the fingertips)
4. jaw cutaway as 5 stacked layers (cavity < fish < throat jaw < head shell with an evenodd window < upper/lower oral jaw)
5. grey reef fish (plus a ghost-outline variant)
6. steel fish-hook row overlay
7. primitives: tick, cross, red arrow, red ring, smell lines, flow lines, eye-dim pill

There is no rope, no counting hands, no front-facing moray, no extra rock and no grouper. All motion is layer transforms and opacity. Occlusion comes from stacking order, never masks: the head inside the hole sits behind the wall layer. For the lunge, a second head layer in front of the wall scales up from the gap. Inside the cutaway, the fish disappears behind the opaque part of the head shell.

| # | scene (start) | visual | camera | SFX |
|---|---|---|---|---|
| 1 | s01_hook 0:00.0 (2.75 s) | Ocean depth 12; the wall top sits at y 28% so headlines read on dark water; hole + eyes (blink at 1.4 s) + wall + hand (eases in 15 px and back); a yellow x-ray of the throat jaw glows inside the gap for 0-0.75 s (shown, not named); Headline `2 MOUTHS` red; chip dark | zoom 1.00 -> 1.05 | underwater_rumble vol 0.13 (≈ -18 dB); bubbles |
| 2 | s02_misdirect 0:02.8 (5.6 s) | wide: Diver (side, kicking) left, GreatWhite grey silhouette drifting far right, Options `CHECKED FOR` items on "sharks"/"jellyfish"/"crab", SVG tick per item -> on "never" (0:06.9) the wide layers end and the gap close-up starts; red ring + `NOT ON THE LIST` on "crack" (0:07.2); the eyes blink | zoom 1.0 -> 0.94, snap to 1.0 on "never" (whip feel), then -> 1.04 | pop x3 on the items; whoosh before "never"; sonar_ping on "touching" |
| 3 | s03_reveal 0:08.3 (5.4 s) | the closed head slides forward inside the gap (behind the wall) on "moray"; hand eases back; `MORAY EEL` -> on "biggest" (0:10.6) a hard swap to the scale card: the body slides in at 300 px/m (900 px = 3 m), ScaleBar `GIANT MORAY: UP TO ~3 M` grows from the left on "three"; You (stand, 1.75 m = 525 px, same pxPerM) pops in on "longer" with `YOU: 1.75 M` | drift | whoosh_long; ding on "longer" |
| 4 | s04_rung1 0:13.7 (4.9 s) | open side head, big, on teal; the yellow tooth-row glow fades in on "teeth"; the fish-hook overlay for 1.1 s on "hooks" (0:18.0); the hand at the right edge; `TEETH CURVE BACKWARD`; chip slot 1 lights on "one" | zoom 1.00 -> 1.08 | click on "one"; tick on "hooks" |
| 5 | s05_rung2 0:18.6 (5.2 s) | gap close-up; the eye-dim pill + `EYESIGHT: POOR` on "barely"; the hand pushes 90 px toward the gap on "hand"; on "bitten" (0:21.7) the open head (in front of the wall) scales 0.35 -> 1.0 out of the gap in 0.18 s; `DEFENDING ITS HOME` red; `QUESTIONS: LATER` | zoom 1.00 -> 1.12 on "bitten", shake 0.35 s | impact + stinger on "bitten" |
| 6 | s06_rq 0:23.8 (3.7 s) | held bite tableau (wall, hand, open head); `WORST MOVE?` red on "worst"; `= FIRST INSTINCT` on "first" | slow push 1.12 -> 1.17 (the wall top never reaches the headline); grade saturate 0.8, vignette 0.3 | heartbeat_slow on "first" |
| 7 | s07_pull 0:27.5 (5.6 s) | `PULL` red (110 px) + SVG cross on the cut; open head big; the hook overlay returns on "hooks"; on "yanking" (0:30.3) the hand jerks 40 px right and settles back, the red arrow wipes out, the tooth glow turns red, `DON'T PULL`; `POINT INWARD` | pushIn 0.4; small shake on "yanking" | impact; click; glitch on "yanking" |
| 8 | s08_handshake 0:33.1 (3.3 s) | bite tableau again; `THE HANDSHAKE` on "handshake"; `YOU LET GO SECOND` on "end" | slow 6 Hz "handshake" shake (amplitude 6), zoom 1.10 -> 1.04 | pop on "end" |
| 9 | s09_turnstile 0:36.4 (2.1 s) | dark Ocean card; Headline `IT'S NOT TRYING TO EAT YOU`; SVG tick pops on "eat" | static | music entry 1 ends at 0:36.4; ding (soft) on "eat" |
| 10 | s10_fish 0:38.5 (2.3 s) | hard cut to teal on "If"; You (shrug) fades out as a grey fish pops in on "fish"; `YOU (AS A FISH)`; `MOUTH 2` red; chip slot 2 lights on "two" (0:40.3) | pushIn 0.3 | music entry 2 fades in; pop; riser on "meet" |
| 11 | s11_suction 0:40.8 (3.4 s) | cutaway (5 stacked layers, lower jaw open 14°), the fish at the mouth; flow lines stall + SVG cross on "can't"; `WEAK SUCTION`; on "second", a glow copy of the throat jaw fades in at the throat; `PHARYNGEAL JAW` | pushIn 0.3 | bubbles on "suck" |
| 12 | s12_launch 0:44.1 (5.4 s) | the fish moves into the mouth and the lower jaw snaps shut on "catch"; on "launches" (0:46.7) the throat jaw slides forward 0.35 s (ease out) into the mouth window; `MOUTH 2: THROAT JAW`; `A MOUTH INSIDE A MOUTH` on "monster"; chip slot 2 flashes | zoom 1.0 -> 1.15 toward the throat on "launches" | click on "catch"; whoosh on "launches"; riser into s13 |
| 13 | s13_ratchet 0:49.5 (5.0 s) | 4 grab cycles from "and" to "gone": the lower jaw opens, the throat jaw hauls the fish 120 px back, the jaw re-bites; Tags `1 2 1 2`; the fish passes behind the opaque head shell and is gone on "gone"; `HAND OVER HAND` | zoom 1.15 -> 1.05, shake on "grabs" | impact on "grabs"; click x4; whoosh_long on "gone" |
| 14 | s14_twist 0:54.5 (5.1 s) | dipBlack 0.3 s; a bright reef (depth 6); the wall at the lower left, the moray body sliding out of its hole toward the diver on "friendly"; Diver (arms forward) right; a fish pops at the diver's hand on "feed"; `THE FRIENDLY ONES` red; `FEEDING SITES` | pullOut 0.4 | whoosh_long; sonar_ping on "friendly" |
| 15 | s15_taught 0:59.6 (4.8 s) | CU: the closed head (left, facing right) + the hand holding a fish (right); smell lines drift from the hand to the snout on "smell"; `YOU TAUGHT IT`; `FINGERS = FISH SMELL` | drift | bubbles |
| 16 | s16_cantsee 1:04.4 (3.9 s) | same CU; the eye-dim pill on "barely"; on "which" the fish fades out and a ghost outline pulses at the fingertips; `WHICH PART IS THE FISH?` | zoom 1.0 -> 1.1 toward the hand | tick on "which" |
| 17 | s17_stinger 1:08.3 (3.3 s) | the frame-1 layers verbatim (deep-copied from s01), `2 MOUTHS`, chip dark; a red ring snaps onto the fingertips on "fingers" (1:10.7); the mix ends 0.2 s after the last word, hard stop | zoom 1.05 -> 1.00 (ends exactly at the s01 frame-0 framing) | heartbeat_slow (single) on "fingers"; the bed plays through the seam (loop ending) |

## 5. Facts (checked; sources)

| # | Claim in VO / on screen | Status | Source |
|---|---|---|---|
| F1 | Morays have a second, mobile set of jaws in the throat (pharyngeal jaws) that move forward into the mouth, grab prey and pull it into the oesophagus | verified | Mehta & Wainwright 2007, *Nature* 449:79-82, "Raptorial jaws in the throat help moray eels swallow large prey"; UC Davis press release / ScienceDaily, Sept 2007 |
| F2 | The oral jaws release while the pharyngeal jaws hold, repeatedly ("swap grips, hand over hand") | verified as a simplification | Mehta & Wainwright 2007 (repeated protraction and retraction; oral jaws release while pharyngeal jaws hold). We no longer claim the front teeth "bite further along" |
| F3 | "Its throat can't suck you in" (weak suction) | verified, worded to the mechanism | Mehta & Wainwright 2007; *J Exp Biol* 210:495-504 (reduced hyoid / weak suction). The "head too narrow" line, which the rival also uses, is dropped (originality nice-to-have) |
| F4 | Teeth curve backwards (recurved, pointing toward the throat) | verified | Mehta & Wainwright 2007 figures; Florida Museum ichthyology profiles |
| F5 | The biggest reach three metres, longer than you're tall (1.75 m) | verified for the giant moray | FishBase, *Gymnothorax javanicus*, max ~300 cm. The tag says `GIANT MORAY: UP TO ~3 M`. "Almost twice your height" is gone |
| F6 | Barely see; hunt mainly by smell (tubular nostrils) | verified | Smithsonian Ocean, FishBase, Florida Museum; also Healthline, "Moray eel bite" |
| F7 | A hand in its crevice gets bitten defensively | verified | DAN marine-life injury material; Healthline; Wikipedia "Moray eel" (most attacks follow disturbance of the burrow) |
| F8 | Pulling back makes it worse, because the recurved teeth tear more tissue (first aid: don't yank free) | verified, worded as mechanism only ("drags your hand across every one") | Healthline "Moray eel bite"; wetwebmedia (DangMorayArt); DAN. No "tears more than the bite did" magnitude claim |
| F9 | Plenty of bites happen during hand-feeding by divers; fed morays lose their caution and approach | verified as "plenty", not "most" | Wikipedia "Moray eel" (an increasing number occur during hand-feeding; banned in some places); oceanearthtravels.com (fed morays approach divers and some have injured the person holding the food); Smithsonian Ocean (feeding bites; hand-feeding banned on the Great Barrier Reef). Finger loss during hand-feeding is reported (Wikipedia; Healthline mentions loss of a digit as a rare outcome), but only second-hand, so no VO line or joke depends on it |
| F10 | Hand-fed morays learn that hands come with food, and with poor eyesight can't tell the hand from the fish ("this time it really is trying to eat your fingers") | supported (feeding-conditioned bite) | Same as F6 + F9 (smell-led feeders lose caution once fed; a feeding bite, not a defensive one) |
| F11 | Rhythmic gaping is breathing (not shown as a threat; no VO line) | verified, visual only | FishBase / Smithsonian Ocean |

Dropped from the previous draft: "anything you push in can't slide back out" (absolute), "almost twice your height" (1.7x, only for the largest), "counting to nine" (finger loss as a punchline), "tears more than the bite did" (magnitude claim with no source), and "head too narrow" (the paper's mechanism is the hyoid).

## 6. Safety, policy and packaging notes

- No wound, no blood and no injury image anywhere. The bite is a closed or open head on a whole hand; the "pull" beat is an arrow and a red glow. The joke beats (crab, questions later, handshake, as-a-fish, monster-movie mouth, which part is the fish) make no injury claims.
- No self-harm wording, no CTA, no safety-advice ending; not made for kids.
- "Monster-movie mouth" is a generic analogy. No film's creature, name, title or design is drawn or named.
- Policy, cited directly (research/R5 is still empty, so R5 must confirm before posting):
  - TikTok Creator Rewards Program counts only videos longer than 1 minute (TikTok Help Center, "Creator Rewards Program"). Ours runs 71.65 s (measured).
  - YouTube asks creators to disclose realistic altered or synthetic content (YouTube Help, "Disclosing use of altered or synthetic content", answer 14328491). A stylised 2D cartoon with TTS narration is not realistic content, but we disclose the voice in the description anyway.
  - YouTube Partner Program inauthentic (mass-produced / repetitious) content policy (YouTube Help, answer 1311392). Our art and script are original. The beat sheet differs from our other Shorts: risky-act hook + plant/pay ladder + turnstile-rule-broken twist. Compare the blue-whale paradox/scale ladder and the box-jelly countdown.
- Description template: "Original animation. Narration: synthetic voice (Kokoro TTS). Facts: Mehta & Wainwright 2007 (Nature) on moray pharyngeal jaws; FishBase."
- Originality: original wording only. The corpus gave structure (counted inventory, literal analogy, turnstile, joke peak, reality flip, purpose-reveal stinger, loop frame). The rival same-topic transcript (CQXRzLX6aXk) is now inside the gate's search path.

## 7. Kit work (recommended, not blocking)

- `explainer/Moray` species in `marine.tsx`, the way SpermWhale and Crocodile are built: `jaw` (deg open), swimWarp body undulation, pose `head` (side head crop), true size 3 m. It would replace `SVG_MORAY_BODY` and `SVG_HEAD_*` in shots 3-8 and 14-16, and give s03 a real slide-out with a body wave instead of the rigid slide.
- `explainer/CoralWall` with a `holes` prop (evenodd cutouts). It would be reusable for any den or crevice creature (octopus, mantis shrimp, stonefish).
- Thumbs: moray subject for `studio/src/kits/thumbs` (see thumbnail.md).
