---
template: explainer
niche: ocean/animal "you vs. X" 2D explainer (Depth Theory style)
sources: research/R1 (beat maps fGcgWaswMns, mg2YJ04Hl9k, 2819-mQEA9M), research/corpus/explainer (12 annotated outliers), research/R5 (policy), backlog/explainer/TOPICS.md
voice: Kokoro am_michael, speed 0.96 (pipeline/audio/config.py), measured ~185-200 wpm
---

# Explainer template

Two formats share one beat grammar. The **Short** (60-90 s, 9:16) is what S1 writes now. The **long-form**
(8-12 min, 16:9) skeleton is kept here so `studio make` and backlog writers use the same beat names.

Every script lives in `episodes/<slug>/script.md`, and its storyboard in `episodes/<slug>/storyboard.json`,
built by `python3 pipeline/episodes/build.py <slug>`.

## Hard contract between script and storyboard

1. **One narration paragraph = one scene.** The builder cuts scenes at the first word of each paragraph
   (real Kokoro word timings from `episodes/<slug>/audio/captions.json`, or a wpm estimate before TTS).
   Keep paragraphs 1-3 sentences, 4-9 s of speech. Something new must appear on screen every ~5 s
   (R1: hard cuts are rare, ~3/min, but a new label, prop or counter lands every ~5 s).
2. Inside a scene, layers are timed to **word anchors** (`at("bus")`), never to guessed seconds.
3. Spell numbers as words in the narration ("fifty-six kilometres"); on-screen numbers go in `Stat`/`Tag`
   components where they can be digits.
4. Only `[sfx: ...]`, `[pause: ...]`, `[music: ...]` markers inside the narration block. Anything else is spoken.

## Short (60-90 s) beat structure

Target 210-260 spoken words (~70-85 s with Kokoro at 0.96 plus paragraph pauses). TikTok Creator
Rewards needs > 60 s (R5), so never ship under 61 s. 10-14 paragraphs.

| # | Beat | % runtime | What it does | Device (corpus) | Default kit shot |
|---|---|---|---|---|---|
| 1 | **Hook** | 0-8 | One second-person or paradox line (<= 20 words). Puts YOU in the water or states a contradiction. Opens the main loop. | paradox open (VtrcKTkhDHU 0:00), 2P scenario (fGcgWaswMns 0:00), odd-consequence claim (jw6bS-WL4F4 0:00) | creature reveal + `Headline` + `You`/`Diver` tiny for scale |
| 2 | **Scale** | 8-20 | Size against an everyday object: bus, car, elephant, your hand. True scale (`pxPerM` on both layers). | scale anchor (fGcgWaswMns 1:05, Ky0/jw6b coin) | creature + `ScaleBar` + `Bus`/`Car`/`Elephant`/`You` + `Stat` |
| 3 | **Weapon / mechanism** | 20-40 | 2-3 escalation rungs, each a concrete mechanism or number, each one step more personal. Signpost words ("And", "Then", "It gets worse"). | ladder of rungs (jw6bS-WL4F4 ESC-1..3), timeline (XFFjxTllpoA), depth ladder (fmZfphacPPQ) | `SpeedBars`, `Stat`, `Map`, `DepthMeter`, creature action |
| 4 | **Re-hook** | ~40-50 | "That's not even the worst part" / "so here's the question" — a short line that resets attention. | "not the worst part" (jw6bS-WL4F4 0:31), "the question we're all thinking" (fGcgWaswMns options beat) | `Headline` alone, camera push |
| 5 | **Your options / the answer** | 50-75 | 3-4 numbered options, struck through with a fact each, then one verdict. Or the paradox's answer. | options list (fGcgWaswMns 6:00-7:00), myth strike-through | `Options` with `strikes` + `select`, optional `Timer` |
| 6 | **Twist** | 75-90 | "Here's the surprising part": the fact that flips the premise (it doesn't hunt you; the real danger is elsewhere; it's even stranger). | twist (fGcgWaswMns 7:00 "it doesn't hunt you"), relief-with-a-sting (jw6bS-WL4F4 0:51) | new creature beat or `Map`, red `Headline` |
| 7 | **Bookend + CTA** | 90-100 | Call back to the hook image, then a comment question. No subscribe ask. | bookend (fGcgWaswMns end), callback button (jw6bS-WL4F4 0:54) | hook shot again, `Tag` with question |

Pacing rules (from the corpus): hook <= 20 words and <= 6 s; a micro re-hook every 4-6 s; one joke or
absurd comparison about every 20 s in a Short (R1 long-form: every ~55 s); the main re-hook between 40% and 55%.

## Long-form (8-12 min, 16:9) skeleton — R1, sperm whale / squid videos

| % runtime | Beat |
|---|---|
| 0-5 | Second-person hook: a comforting rule, broken by a sensory detail, then the animal. Title drop at 4-9% |
| 5-10 | "Most people think X... and yes... but" plus 3 superlatives |
| 10-20 | Scale against a bus, elephants, your hand |
| 20-60 | 3-4 escalations, each opened by a question card and closed by a joke; one callback to the hook; one recent study with year and place |
| 60-70 | "The question we're all thinking": 4-5 numbered options struck through (fact, analogy, joke), hard verdict |
| 70-78 | Twist: "here's the surprising part" |
| 78-90 | The real danger is us |
| 90-96 | Ecology payoff, bookend to the opening image |
| 96-100 | Comment CTA, no subscribe ask |

~170 wpm, ~1,680 words per 10 min, a joke every ~55 s.

## Visual grammar (kit: `studio/src/kits/explainer`)

- Background: `explainer/Ocean` with `depth` (number or track). Near-black navy at depth, `surface: true` for the waterline.
- Palette: grey/white creatures, white uppercase labels, **one red accent** per scene (`Headline color: red`, red strike-throughs).
- Layout for 9:16: picture zone y 12-60%; `Headline` at y ~14-18%; captions at y 0.70 (`fontSize` 88, `maxWords` 3); nothing important below y 77% (platform UI).
- Camera: slow `pushIn`/`drift` on almost every scene (one canvas with timed layers, not many cuts). Transitions: mostly `fade`/`cut`, `whip` on beat changes, `dipBlack` before the twist.
- Components only from the kit registry: Ocean, DepthMeter, Creature + SpermWhale ColossalSquid Orca GreatWhite BlueWhale Anglerfish Octopus Crocodile Hippo Grizzly Diver You Bus Car Elephant, ScaleBar HeightChart Stat Map Timer Options SpeedBars Headline Tag. Props an animal the kit lacks (seal, ice floe, heart, krill) are inline `svg` layers, never a new component name.

## Originality and policy gates (BRIEF update 09:00, R5)

- Front matter lists 2-3 `references:` from `research/corpus/explainer` (id, url, views, outlier_score), and the script has a beat alignment table: our beat -> reference beat + timestamp + device borrowed. Borrow devices, never wording.
- `python3 scripts/originality_check.py episodes/<slug>/script.md research/corpus research/library/transcripts` must print PASS.
- Every fact is listed under **Facts to verify** with a source to check before publishing. Facts are paraphrased.
- Sameness review (R5 "inauthentic content"): across a batch, vary the hook device, the mid-section set piece and the twist. Do not ship five "Why you'd never want to meet a [X]" titles in a row; mix "what happens to you", "you vs.", "the light in the deep" style titles.
- Not made for kids; no gore (attacks are implied, never shown injured).
