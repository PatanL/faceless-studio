# MKRYulCq3Mo: The Machine That Copies Human Digestion 😮 (Zack D. Films)

> Internal research only, to learn the format. The verbatim lines below are for structure study. Do not reuse their wording, characters, sets or visuals in anything we publish (BRIEF hard rule 5). Run `scripts/originality_check.py` on any script that cites this file.

| Field | Value |
|---|---|
| URL | https://www.youtube.com/shorts/MKRYulCq3Mo |
| Channel | Zack D. Films (29.5M subs) |
| Role in the zackd sample | **control** (outlier 1.04, a typical upload), cluster `howitworks` (how it works, inventions, tech: median 9.3M) |
| Views / likes / comments | 10,235,057 / 264,479 (2.6%) / 4,100 (0.040%) (yt-dlp info JSON, fetched 2026-11-01 on the Spark) |
| Upload date | 2026-10-22 |
| Duration | 32.4 s (608x1080, 29.97 fps). Speech runs 0:00.00-0:31.44, then about 0.9 s of picture with no voice |
| Total words | 90 in 6 sentences (avg 15 words; shortest 9, longest 19) |
| Words/min | **172** over speech (90 / 31.44 s); 167 over the full runtime. Per sentence: 201, 178, 187, 176, 161, 191 |
| Hook | Sentence 1, 0:00.00-0:04.78: **16 words in 4.8 s (201 wpm)**, the fastest sentence in the video |
| Pauses | Only 5 gaps between sentences, 0.0-0.6 s each (mean 0.36 s). No dead air |
| Pivot words | "You see" (0:05.2), "Next" (0:12.2), "about a day later" (0:15.1), "You see" (0:24.3), "while" (0:28.6): a turn every 3-9 s, mean 5.8 s |
| Shots | About 25 shots in 32.4 s, **mean 1.3 s per shot**. Only 3 hard cuts score above 0.25 on ffmpeg scene detection (0:12.6, 0:15.1, 0:30.4). The rest are continuous camera moves or 2-4 frame motion-blur transitions, so it reads as one guided tour |
| Captions | 35 caption chunks, 2.6 words and about 0.9 s each |
| Audio | A bed runs under the voice: the gaps between sentences measure -20 to -29 dB mean, not silence. Whether it is music or SFX was not identified |
| Transcript source | No auto-subs (YouTube answered HTTP 429 on the subtitle request). Audio downloaded on the Spark (`~/studio/refs/zackd/MKRYulCq3Mo/`) and transcribed with faster-whisper small, CPU int8, 4 threads, word timestamps. The text is clean; no spelling fixes were needed |
| Frames | `sheets/MKRYulCq3Mo.jpg` (1600x1408): one frame per second, t = 0-31 s, left to right and top to bottom, 8 per row (row 1 = 0-7 s, row 2 = 8-15 s, row 3 = 16-23 s, row 4 = 24-31 s). Shot timings below also used a 4 fps sheet that was not kept |

**Full transcript (verbatim, whisper, for structure study only)**

```
[0:00.00-0:04.78] The food was dropped in, and about a day later, it would come out as poop.
[0:05.24-0:11.66] You see, a grinder inside chewed the food into tiny pieces, before acid dissolved it into a soupy sludge.
[0:12.18-0:17.62] Next, bacteria broke down whatever was left, and about a day later, it passed through a separator,
[0:17.84-0:24.32] making it thicker and thicker until it was squeezed through a narrow pipe, looking and smelling like human poop.
[0:24.32-0:28.04] You see, these samples showed how bowel cancer screenings work,
[0:28.62-0:31.44] while other samples were sold to collectors as art.
```

**Fact check (do it again for any script of ours that uses a claim like this):**
- The video never names its subject. It is Wim Delvoye's art installation *Cloaca* (first shown in 2000 at MuHKA, Antwerp). It is a row of machines with a food hopper, a blender, vessels of enzymes, acid and bacteria, pumps and a separator, and it was fed about twice a day. Its output was produced roughly a day later, then vacuum-sealed and sold to collectors as art. The input, the stage order, the "about a day" and "sold as art" all hold.
- "Showed how bowel cancer screenings work": **not confirmed**. I could not find a source that ties *Cloaca* samples to bowel cancer screening. Treat it as an unchecked claim, and don't borrow it.
- Leaving out the proper nouns is a deliberate part of the format (see section 4), not an error. Our scripts still need a source for every claim, even if the voice-over never names it.

## 1. Line-by-line annotation

Beat key: HOOK (input to output in one sentence), MECH n (one machine stage), TIME-SKIP, SQUEEZE (the build to the output), PAYOFF (the sensory proof), TURN (pivot from how it works to what it was for), TWIST (the reveal that changes the meaning).
Device key: DEF (definite article with no setup: "The food"), PAST-HAB (documentary past habitual: "would", "was"), STINGER (the gross or surprising word placed last in the sentence), YS ("You see," as a rewind into the explanation), BODY-MAP (the machine verb is a body verb), TEX (texture word), REP (repetition to build), ECHO (a phrase from the hook comes back), SENSE (sense words), WITHHOLD (the subject's identity is kept back), CONTRAST ("while other ...": serious use first, absurd use second).

| # | Time | Line (verbatim, split at clauses) | Beat | Device | Purpose |
|---|---|---|---|---|---|
| 1 | 0:00.0 | The food was dropped in, | HOOK (input) | DEF, PAST-HAB, WITHHOLD | Starts mid-action with no "this is" or "meet". "The food" assumes a machine the viewer hasn't been shown yet, so the first open question is "dropped in what?" |
| 2 | 0:01.8 | and about a day later, it would come out as poop. | HOOK (output) / LOOP-OPEN | TIME-SKIP, STINGER ("poop" is the last word), PAST-HAB | The whole story, input to output, in one sentence, ending on the gross-out word. The question changes from "what is it?" to "how?", and the rest of the video answers it |
| 3 | 0:05.2 | You see, a grinder inside chewed the food into tiny pieces, | MECH 1 (grind) | YS, BODY-MAP ("chewed") | "You see" restarts the clock and announces the explanation. The machine verb is the body verb (chewing), so the title's idea, a machine that copies digestion, is shown, not stated |
| 4 | 0:08.9 | before acid dissolved it into a soupy sludge. | MECH 2 (acid) | BODY-MAP (stomach, never named), TEX ("soupy sludge", alliteration) | Second stage in the same breath. A gross texture word works as a small reward |
| 5 | 0:12.2 | Next, bacteria broke down whatever was left, | MECH 3 (bacteria) | "Next" list marker, BODY-MAP (gut flora) | A one-word scene change. Visually the biggest scale jump in the video (to the microscopic) |
| 6 | 0:15.1 | and about a day later, it passed through a separator, | TIME-SKIP / MECH 4 (separator) | ECHO ("about a day later" from line 2) | The time phrase from the hook comes back. It tells the viewer the explanation has caught up with the hook's "a day later": we are near the output |
| 7 | 0:17.8 | making it thicker and thicker | SQUEEZE | REP | Doubling the word stretches time on purpose. It is the only repetition in the script, used at the physical climax of the process |
| 8 | 0:19.8 | until it was squeezed through a narrow pipe, | SQUEEZE (extrusion) | BODY-MAP (colon and rectum, by mechanism only) | Says what the body part does without naming it. Clean words for a gross picture keep it watchable |
| 9 | 0:22.0 | looking and smelling like human poop. | PAYOFF (sensory proof) | SENSE (sight + smell doublet), ECHO / STINGER ("poop" ends the sentence again) | Closes the "how" loop: the hook's last word comes back as this sentence's last word. "Human" makes it exact and grosser. This is the gross peak, at 68-75% of runtime |
| 10 | 0:24.3 | You see, these samples showed how bowel cancer screenings work, | TURN (respectable use) | YS (second time, now for "why" not "how"), authority (medicine) | Pivot from process to purpose. It answers "why would anyone build this?" with a serious reason first, so the absurd reason that follows hits harder. (Claim unverified, see the fact check) |
| 11 | 0:28.6 | while other samples were sold to collectors as art. | TWIST / PUNCHLINE | CONTRAST ("while other"), STINGER ("art" is the last word of the video), WITHHOLD paid off | Reframes the whole thing: it was never a science machine, it was an artwork, and people paid for its output. Nothing comes after it, and the video ends 0.9 s after the last word |

## 2. Escalation ladder

Each rung is grosser, smaller or stranger than the last, then the ladder jumps from physical to social:

1. **Normal input** (0:00): a plate of ordinary food. Safe and familiar.
2. **Mechanical violence** (0:05): blades chew it up.
3. **Chemical** (0:09): acid melts it into sludge (texture gets grosser).
4. **Biological, microscopic** (0:12): bacteria eat what is left (the scale drops to micro, and the colour world flips).
5. **Time** (0:15): another day passes.
6. **Compression** (0:17-0:21): thicker, thicker, squeezed, narrow (the physical climax, with repetition).
7. **Sensory confirmation** (0:22): it looks and smells real, shown by a human who recoils (the gross peak).
8. **Legitimate purpose** (0:24): medicine (it gets serious and earns permission to be gross).
9. **Absurd purpose** (0:28): rich people buy it as art (the social twist, and the only rung that is funny instead of gross).

Shape: one long, steady gross-out climb over 75% of the runtime, a short serious step, then a sideways jump into absurdity. The video stops escalating disgust before the end and switches to irony, so the ending lands as a laugh rather than a wince.

## 3. Punchline and twist mechanics

- **The twist is withheld by omission, not hidden by misdirection.** The script never names the artist, the gallery, the city or the year, and never says "art" until the last word. The title ("The Machine That Copies Human Digestion") is withheld too. It promises a science explainer, and the ending is a different kind of story.
- **Planted on screen for rewatchers.** At 0:02-0:03 the wide shot shows "MUSEUM" lettering on the wall and a spotlit "ART EXHIBITION" sign. First-time viewers read it as set dressing. On a loop or rewatch the ending was in plain sight. This is the channel's cheap rewatch reward: the picture knows more than the voice.
- **Serious-then-absurd pair.** "These samples showed [serious use], while other samples were sold [absurd use]." The parallel subject ("samples ... other samples") makes the two uses sit side by side, and the absurd one goes last.
- **Last word = punch.** Like the hook ("poop") and the payoff ("poop"), the final sentence ends on its key noun ("art"). Every sentence in the video puts its strongest word last.
- **Hard stop.** No outro, no question, no call to action, no "follow for more". The picture holds about 0.9 s on the collector at his pedestal, then the Short loops.
- **Weak loop seam.** The last line ("...collectors as art.") into the first ("The food was dropped in...") makes partial sense (a work of art being fed again), but the cut from the gallery to the POV plate is a hard visual jump. This control video does not build a seamless loop.

## 4. Hook length and pacing

- **Hook = 1 sentence, 16 words, 4.8 s, 201 wpm.** It is a complete compressed story: input, time, output. It opens no "did you know" frame and gives no setup or name.
- Picture in the hook: 2 shots plus a time-of-day light change in 4.8 s. A POV hand action, then a wide reveal.
- The body runs at 176-187 wpm with gaps of 0.6 s or less. The turn sentence (line 10) is the slowest (161 wpm), a small brake before the punchline. The punchline sentence is fast again (191 wpm).
- Timing as % of the 32.4 s runtime: hook 0-15%; mechanism 16-55%; squeeze 55-68%; sensory payoff 68-75%; turn 75-86%; twist 88-97%; tail 97-100%.

## 5. Shot list

Times are from the 1 fps sheet and a 4 fps check sheet, accurate to about 0.25 s.

| # | Time | Shot type | What's on screen | Camera move | How the picture literalizes the line |
|---|---|---|---|---|---|
| 1 | 0:00.0-0:01.8 | POV, top-down | First-person view: two hands hold a white plate over a steel funnel bowl. The viewer's own sneakers and a white branded tee are visible below. A burger, cut in quarters, gets a glowing yellow outline on "The food". The plate tips and the pieces slide in | Locked POV, small push | "The food" gets a highlight outline as it is named. "Dropped in" is shown as the viewer doing it, which makes it second person without saying "you" |
| 2 | 0:01.8-0:02.1 | Medium side | The funnel on a steel stand with a blue pump: the machine's input end | Fast pull-back with motion blur (transition) | Bridges the hand action to the machine |
| 3 | 0:02.1-0:03.0 | Wide establishing | Dark blue gallery at night: "MUSEUM" letters on the brick wall, six glass-and-steel units hanging from a ceiling rail, and a spotlit "ART EXHIBITION" stand sign with the channel's logo | Slow dolly in | "A day later" shown as **the room going dark**: time passes through the lighting. The sign plants the twist |
| 4 | 0:03.0-0:04.0 | Medium, tracking | The lights come back up. The camera glides along the rail pipe to a vertical steel nozzle | Lateral glide, then tilt down | "It would come out": the camera travels to the output end |
| 5 | 0:04.0-0:05.2 | Medium close | The nozzle above a petri dish on a steel plate. A brown log pushes out and drops into the dish | Slow push | "As poop": the exact object on the exact word |
| 6 | 0:05.2-0:05.5 | Medium, diagram look | A blue jug pours food into the funnel against a flat cyan background | Fast reverse-feel move | "You see" = rewind. The flat cyan background marks the switch to explainer mode |
| 7 | 0:05.5-0:08.5 | Cross-section cutaway | The funnel and grinder housing shown cut open (cut faces filled black). Food chunks fall into spinning blades, and an output pipe streams small granules | Crane down, following the food | "A grinder inside" means the camera goes inside. "Chewed" and "tiny pieces" are shown as visible particle size changes |
| 8 | 0:08.5-0:09.4 | Medium wide | Back in the blue room: pump, pipes and hanging glass vessels with red stopcocks | Blur transition, then slow glide | "Before acid": we arrive at the next stage |
| 9 | 0:09.4-0:11.0 | Macro, inside liquid | Inside the vessel: dark chunks drift and shrink, with bubbles and refraction | Slow drift | "Dissolved": the chunks visibly get smaller |
| 10 | 0:11.0-0:12.6 | Low-angle close | An inverted-cone glass vessel full of brown sludge, with a red valve at the bottom | Slow push up | "Soupy sludge": the texture is shown through glass |
| 11 | 0:12.6-0:15.1 | Microscopic, isolated | A rust-orange radial gradient background. Blue rod-shaped bacteria with flagella swarm one brown lump until it crumbles | Slow push in | "Bacteria broke down": shown literally, at an impossible scale. The colours flip: warm background, cool subject |
| 12 | 0:15.1-0:15.3 | Close, from below | The underside of a vessel with brown liquid | Hard cut, quick | A re-entry beat back to the real scale |
| 13 | 0:15.3-0:16.5 | Wide | The full row of machines. A light change in the room marks time passing again | Slow lateral | "About a day later": the same lighting trick as shot 3 (a visual echo of the verbal echo) |
| 14 | 0:16.5-0:18.3 | Medium, tracking | A horizontal glass tube with a steel auger screw. A brown mass moves along it | Truck right with the material | "Through a separator": the camera rides with the material |
| 15 | 0:18.3-0:20.5 | Medium close | A T-junction feeds a vertical glass column, which visibly fills with brown | Hold, slight push and tilt | "Thicker and thicker": the column fills on each repeated word |
| 16 | 0:20.5-0:22.0 | Close | Tilt down the column to a tapered steel nozzle. A brown plug pushes out | Tilt down | "Squeezed through a narrow pipe": the narrowing is the nozzle's shape |
| 17 | 0:22.0-0:22.5 | Close | The log drops into a petri dish | Static | Lands the output |
| 18 | 0:22.5-0:24.0 | Medium close, character | A woman in a white branded tee leans in to sniff. Glowing green wavy stink lines rise from the sample and she recoils | Slight push | "Smelling": smell made visible with cartoon stink lines on a realistic render. A human reaction stands in for the viewer's |
| 19 | 0:24.0-0:24.8 | Medium | She pulls back, hand to her forehead, other palm up | Static | The comic reaction beat closes the gross peak |
| 20 | 0:24.8-0:26.0 | High-angle insert | Brown samples on a steel tray. A doctor's hand takes a swab | Slow push | "These samples": the samples are handled, not just shown |
| 21 | 0:26.0-0:28.5 | Medium close, then insert | A doctor (white coat, blue scrubs, lanyard ID badge) puts the swab in a tube. The tube is held to the lens with a readable "BOWEL CANCER screening" label | Push to insert | "Bowel cancer screenings": the label carries the words, so the claim is read as well as heard |
| 22 | 0:28.6-0:29.5 | Wide, then push | A blue wall grid of clear acrylic display boxes, each with one sample and a channel-branded label | Hard cut, push toward one box | "Other samples": many units = a product line |
| 23 | 0:29.5-0:30.3 | Close | A hand slaps a red "SOLD" sticker on a box, then lifts the box out | Static, then follow | "Were sold": a commerce sign everyone knows |
| 24 | 0:30.4-0:31.2 | Medium, character | A grey-haired man with a moustache, black suit and tie, admiring the boxed sample | Hard cut, slow push | "Collectors": the wardrobe signals wealth |
| 25 | 0:31.2-0:32.4 | Wide reveal | A classical white gallery with columns and statues. The box sits on a marble pedestal like a sculpture | Pull back | "As art": the setting itself delivers the punchline (gross object, fine-art staging) |

## 6. Visual grammar notes

- **Render style:** clean, bright, near-photoreal 3D, like a product render: soft global illumination, shallow depth of field on close-ups, and no grain or grunge. The gross subject is shown in a sterile, pretty world, and that contrast is part of why it is watchable.
- **Character design:** semi-realistic adult humans with natural proportions and slightly heightened expressions (recoil, admiration). Wardrobe sets the role at a glance: white branded tee = everyman stand-in, lab coat + scrubs + ID badge = doctor, black suit + moustache + grey hair = rich collector. Characters appear only in the last 30% of the video. The machine is the protagonist.
- **Palette:** cobalt/cerulean blue painted brick and white floor tiles as the base, brushed steel and clear glass in neutral greys, and **the brown subject as the only warm colour** in most frames, so the eye always finds it. Red is a small accent (stopcocks, blood-collection-style caps, the SOLD sticker). Two off-world palettes mark mode changes: flat cyan gradient = cross-section diagram, rust-orange radial gradient = microscopic. The micro shot inverts the main scheme (warm background, blue subject).
- **Lighting:** an even, high-key studio look. Time skips are shown by dimming the whole room to night blue and bringing it back up, with no clocks or text. Spotlights pick out set-dressing clues (the exhibition sign).
- **Materials:** brushed and polished steel, thick refractive glass with liquid inside, acrylic boxes, ceramic tile, painted brick, marble. Organic matter has a wet, crumbly, textured look, and the gross detail lives only in the subject.
- **Camera language:** mostly continuous guided moves: dolly, glide, crane following the material through the machine, push in on each new noun. The camera travels the same path as the food. Inside views are cutaway sections (black cut faces) rather than X-ray. Hard cuts are kept for changes of scale or world (micro, the art gallery). One opening POV shot puts the viewer's own hands in the frame.
- **Cut rhythm:** a new shot or a big move change about every 1.3 s. Every noun in the voice-over gets its own picture within about 0.5 s of being spoken. Transitions are 2-4 frame motion-blur whips. There are no wipes or text cards.
- **Caption style:** white bold sans, soft dark drop shadow, no box, centred horizontally at about 78% of the frame height (below the action, above the UI). 1-4 words per chunk (mean 2.6), about 0.9 s each, cut at phrase boundaries ("a grinder inside" / "chewed the food" / "into tiny pieces"). Sentence case as spoken, with no punctuation, no keyword colour, no emoji and no karaoke word highlight. The only colour emphasis is in the picture itself (the yellow outline on the food at 0:00).
- **Branding:** the channel name is built into the world as props (the tee, the exhibition sign, the tube label, the display-box labels, a wall logo) instead of a corner watermark.

## 7. Transferable skeleton (no original wording)

For any "a machine, process or creature that secretly mirrors something familiar" topic, 28-35 s, about 85-95 words at about 170-180 wpm:

1. **0-15% | Compressed outcome hook.** One sentence: [plain input] + [time gap] + [surprising or gross output], with the output word placed last. Use a definite article and past tense, as if the viewer already knows the device. Name nothing (no person, place or date). Picture: a hands-on POV action into the device, then a wide reveal of the setting that **quietly plants the final twist** (signage, location type, props).
2. **16-55% | Rewind into stages.** Open with a rewind phrase of our own. Then 3-4 stages, one clause each, linked by "before", "then" and "next". Give each machine stage a **body or everyday verb** so the comparison never has to be stated. Give each stage one texture or sense word. Picture: the camera follows the material through cutaways; each stage gets its own colour world when the scale changes (diagram background, microscopic background).
3. **About 45% | Echo the hook's time phrase.** Reuse your own hook's time marker to tell the viewer the explanation has caught up with the hook. Picture: repeat the same lighting time-skip used in the hook.
4. **55-68% | Physical climax with one repetition.** The narrowing or compressing step, with a doubled word to stretch the moment. Picture: a container visibly filling or narrowing as the word repeats.
5. **68-75% | Sensory proof plus a human reaction.** Say it is indistinguishable from the real thing, and end on the hook's stinger word (bookend). Picture: the first human character reacts physically. Make the sense visible with a graphic (lines, glow).
6. **75-86% | Respectable purpose.** Pivot from "how" to "why": a serious, sourced use. Picture: a professional character and a readable label that carries the key term.
7. **88-97% | Absurd second purpose = twist.** Structure: "[same noun] did [serious thing], while other [same noun] [absurd thing]." End on the twist word. Picture: hard cut to a world that recontextualizes the object (a commerce sign, then a prestige setting with the object staged as treasure).
8. **97-100% | Hard stop.** No outro or call to action. Hold the reveal wide for under 1 s and let it loop. The setting planted in step 1 is the rewatch reward.

Rules carried over: every sentence ends on its strongest word; one pivot word every 4-6 s; gaps of 0.6 s or less; a new picture for every noun within 0.5 s; gross detail only on the subject, inside a clean, bright, blue-and-steel style world; captions in 2-3 word phrase chunks with no styling tricks.
