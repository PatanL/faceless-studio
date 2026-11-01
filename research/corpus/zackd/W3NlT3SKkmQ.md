# W3NlT3SKkmQ: How To Get Water Out Of Your Ear (Zack D. Films)

> Internal research only, to learn the format. The verbatim lines below are for structure study. Do not reuse their wording, character, props, footage or audio in anything we publish (BRIEF hard rule 5). Any script that cites this file must pass `scripts/originality_check.py`.

| Field | Value |
|---|---|
| URL | https://www.youtube.com/shorts/W3NlT3SKkmQ |
| Title | How To Get Water Out Of Your Ear 🤔 |
| Channel | Zack D. Films (29.5M subscribers) |
| Role / cluster | outlier, lifehack/body |
| Uploaded | 2026-10-13 |
| Views | 47,301,989 (yt-dlp `view_count`, fetched 2026-11-01 on the Spark) |
| Outlier score | 3.36 (views / median of the 31 neighbouring mature uploads; channel median is about 10M) |
| Likes / comments | 917,825 likes (1.94% like rate, below the channel median of 3.5%); 8,200 comments (0.017%, also below the 0.028% median). People watched and looped it far more than they reacted to it. |
| Duration | 30.0 s. Speech runs 0:00.0 to about 0:29.5. Under 0.5 s of silence at the end (29.6-30.0). No outro, no CTA. |
| Words | 88 |
| Words/min | **179 wpm** overall (88 words / 29.5 s, about 3.0 words/s). The hook is faster at **224 wpm** (13 words in 3.5 s). After the hook, individual lines run 145-200 wpm (median about 175). |
| Sentences | 5. The first one is a conditional fused onto the first instruction ("if ... , [do X]"). |
| Format | YouTube Short, 9:16, stylised-realistic 3D (one human character plus medical cross-section cutaways). One calm male narrator over a continuous music/SFX bed, small white 1-3-word captions at about 78% of frame height. |
| Audio | Integrated loudness -11.5 LUFS (loud master). The bed between sentences sits at about -15 to -21 dB RMS against about -12 to -15 dB during speech, so it is roughly 6-8 dB under the voice. It stops with the voice at 29.6 s. |
| Transcript | faster-whisper `small.en` on the Spark CPU (int8, 4 threads), word timestamps. YouTube auto-subs failed with HTTP 429. The burned-in captions on the frames match the transcript word for word. |
| Frames | `sheets/W3NlT3SKkmQ.jpg` (1600x1424, 8x4 grid, 30 tiles, tile n = second n, row-major, no labels). I also checked the cut timing on a 4 fps sheet that was not saved. Source video: `dgx-spark:~/studio/refs/zackd/W3NlT3SKkmQ/W3NlT3SKkmQ.mp4` (360x640, 29.97 fps). |

## Full transcript (faster-whisper segments, verbatim, internal use)

```
[00.00-03.48] If you fall into a pool and water gets stuck in your ear,
[03.80-06.18] tilt that ear straight down towards your shoulder.
[06.40-09.80] Then press your palm flat over it, sealing the opening,
[09.96-12.62] and gently pump it like working a plunger.
[12.96-16.02] Each outward pull lowers the pressure under your palm,
[16.14-18.66] creating a suction that loosens the water.
[18.96-22.86] And since your ear points down, gravity pulls it toward the opening.
[23.20-26.46] When you lift your palm away, the pressure snaps back to normal,
[26.46-29.40] and the water finally slides out of your ear.
```

Fact note for our own scripts: the "palm vacuum" plus "tilt your head" method is common, low-risk home-remedy advice, so the premise holds up. The on-screen gravity label reads "9.8 m/s", but acceleration is in m/s². The physics is simplified: the suction mostly breaks the surface tension of the trapped water rather than pulling it out. Keep the confident tone, but check every mechanism and unit we put on screen.

## 1. Line-by-line annotation

Beat key: HOOK, STEP-n (instruction n), MECH-n (mechanism n), CB (callback), RELEASE, PAYOFF.
Device key: 2P = second person; COND = "if" scenario; IMP = imperative verb first; ANALOGY = household-object simile; SEQ = sequencing word (then / each / when); CAUSE = "since/because" link; CB = callback to an earlier step; FIN = "finally" release word; VIS-LIT = the visual makes the words literal; XRAY = anatomy cutaway; NUM-V = number shown only on screen.

| # | Time | Line (verbatim, internal use) | Beat | Device | Purpose |
|---|---|---|---|---|---|
| 1 | 0:00.0 | If you fall into a pool and water gets stuck in your ear, | HOOK (problem) | 2P, COND, VIS-LIT (slapstick), XRAY | Names a near-universal, slightly gross annoyance in the first 3.5 s. "If you" puts the viewer inside it. The comic bike-into-pool image holds the eye while the cutaway at 0:02 shows where the water sits, so the problem is both seen and felt before any fix arrives. Opens the loop: how do I get it out? |
| 2 | 0:03.8 | tilt that ear straight down towards your shoulder. | STEP-1 (set-up) | IMP, 2P, cyan arrow | The first instruction arrives at 3.8 s with no throat-clearing: value starts immediately. It looks like an easy, almost throwaway step, which is the plant for the callback at line 7. |
| 3 | 0:06.4 | Then press your palm flat over it, sealing the opening, | STEP-2 (seal) | SEQ ("then"), IMP, 2P, cyan rim glow on "sealing" | The word "sealing" plants the physics (an airtight chamber) before it is explained. The extreme close-up of the hand on the ear makes the step easy to copy. |
| 4 | 0:09.96 | and gently pump it like working a plunger. | STEP-3 (action) | ANALOGY (household object), VIS-LIT (a cartoon plunger prop pops into frame) | The simile turns an unfamiliar motion into one everyone knows. The prop pop-in at 0:11.5 is the only gag in the middle of the video and breaks up a 5.5 s close-up. "Gently" quietly covers safety. |
| 5 | 0:12.96 | Each outward pull lowers the pressure under your palm, | MECH-1 (why it works) | SEQ ("each"), XRAY, colour-coded pressure | Here it turns from a how-to into a how-it-works, the channel's core value. The cutaway fills with a red→orange→yellow→white→blue colour ramp, so the pressure change is visible. |
| 6 | 0:16.14 | creating a suction that loosens the water. | MECH-1 result | cause→effect, XRAY macro, motion arcs | The camera pushes into the canal and the water blob is tugged outward: a small "it's moving" moment that makes viewers want to see it come out. |
| 7 | 0:18.96 | And since your ear points down, gravity pulls it toward the opening. | MECH-2 + CB to STEP-1 | CAUSE ("since"), CB, NUM-V ("9.8 m/s" with a down arrow) | Pays off the plant from 0:04: the easy first step turns out to be half the mechanism. This gives the "oh, that's why" click and makes the method feel engineered, not folk wisdom. The number appears only on screen, so it adds authority without slowing the narration. |
| 8 | 0:23.2 | When you lift your palm away, the pressure snaps back to normal, | RELEASE (final step + MECH-3) | SEQ ("when"), IMP-implied, XRAY, sound word "snaps" | The last action is a release, not another effort. "Snaps" is a sharp, physical verb that marks the moment of tension breaking. |
| 9 | 0:26.46 | and the water finally slides out of your ear. | PAYOFF | FIN ("finally"), macro drip shot, relief face | Closes the loop with a satisfying visual (a droplet sliding off the earlobe in macro) and an emotional beat (eyes closed, relieved "ahh", then a small smile). The last words echo the title, "out of your ear", so the ending feels finished. No CTA. |

## 2. Structure and the escalation ladder

### Beat sequence with % of runtime (30 s)

| Span | Beat | Seconds | % |
|---|---|---|---|
| 0:00-0:03.6 | HOOK: universal problem, shown outside (slapstick) and inside (cutaway) | 3.6 | 12% |
| 0:03.7-0:12.9 | STEPS 1-3: tilt, seal, pump (with the analogy gag) | 9.2 | 31% |
| 0:13.0-0:19.5 | MECH-1: pressure drops, suction loosens the water (deepest cutaway) | 6.5 | 22% |
| 0:19.7-0:22.9 | MECH-2: gravity, a callback to step 1 | 3.2 | 11% |
| 0:23.0-0:26.2 | RELEASE: lift the palm, pressure returns | 3.2 | 11% |
| 0:26.3-0:29.9 | PAYOFF: drip macro, relief face | 3.6 | 12% |

Macro split: problem 12%, instructions 31%, mechanism 44%, payoff 12%. The title says "How To", but almost half the runtime is "why it works". That is the house move: a utility premise sold as a mechanism explainer.

### The escalation ladder

This is a how-to, so nothing gets more dangerous. It escalates on three other axes at once:

1. **Effort to release.** Passive (tilt) → active seal (press) → repeated force (pump) → let go (lift) → result. Tension builds through the three actions and breaks on the one non-action, the release. The release is the climax.
2. **Depth of view.** Wide (pool) → medium (girl at the pool edge) → extreme close-up (hand on ear) → anatomy cross-section → macro inside the canal (the water blob) → back out to a macro of the earlobe → medium (face). The deepest point (0:17-0:19, the blob being tugged) sits at about 60% of the runtime, the same place an explainer would put its "wow" rung.
3. **Explanation layer.** What to do (steps) → why each step works (pressure) → why the *first* step mattered (gravity callback) → what happens when you stop (pressure snaps back). Each layer reframes the one before.

**Outside/inside ping-pong.** The edit alternates between the body exterior (O) and the cutaway (I): O 0-2.2 | I 2.2-3.6 | O 3.7-12.9 | I 13.2-19.3 | O 19.7-20.9 | I 21.0-22.9 | O 23.0-24.4 | I 24.5-26.1 | O 26.3-30. After the long middle stretch the switches speed up: the last four segments are each 1.5-2 s. Every switch works as a re-hook.

### Re-hook interval

- A new instruction or mechanism clause every 3-4 s (0:03.8, 0:06.4, 0:10.0, 0:13.0, 0:16.1, 0:19.0, 0:23.2, 0:26.5).
- A visual cut about every 2 s (15 shots in 30 s). The one long hold (0:07.5-0:12.9) is broken by the cyan seal glow at 0:09 and the plunger pop-in at 0:11.5.
- Captions change every 0.5-1.2 s (1-3 words), so the screen never stays still.

### Open loops

| Loop | Opens | Closes |
|---|---|---|
| A: How do I get the water out? | Title + 0:00-0:03 (water pocket shown in the cutaway) | 0:26-0:29 (droplet slides out) |
| B: Why tilt first? (implicit; it reads as a throwaway step) | 0:03.8 | 0:19-0:22 (gravity callback) |
| C: What does pumping actually do? | 0:10 ("like a plunger") | 0:13-0:18 (pressure ramp, suction) |

## 3. Punchline / twist mechanics

- **No joke ending. The punchline is physical relief.** The last 3.5 s give three stacked releases: the verb "snaps", then the macro drip (the ASMR-like "satisfying" shot), then the character's relieved face. The viewer gets the same "ahh" the character does. That shared relief, plus the fact that it is useful, is likely why it was watched and saved far more than it was liked.
- **The plant/payoff twist.** Step 1 (tilt) is presented as a simple instruction and never explained at the time. At 0:19 the narration turns it into half the mechanism ("since ... points down"). Making a step that seemed arbitrary turn out to be essential is the only twist, and it works because it costs no extra runtime: one subordinate clause.
- **The counterintuitive moment.** The water does not come out while you push. It comes out when you *let go*. The script holds the result until the release step, so the payoff matches the action that triggers it.
- **Comic bookends instead of jokes.** The opening shot overdoes the premise (the character rides a bike straight into the pool, which the words never mention), and the middle has one visual simile gag (the plunger prop pops up beside her hand). Both are visual only; the narration stays deadpan and factual throughout.
- **Title echo.** The closing words repeat the title's object ("out of your ear"), so the Short ends on a sense of "done" and loops cleanly back to the problem shot.

## 4. Hook stats

- Hook = 13 words, 0:00.0-0:03.5 (12% of runtime), **224 wpm**, the fastest stretch of the video.
- Form: "If you" + common mishap + "and" + symptom, then a comma, then the first imperative. It does not restate the title as a question; it drops the viewer straight into the situation.
- First value (the first instruction) arrives at **3.8 s**.
- Visual hook: an action gag in frame 1 (the bike off the pool edge), a splash at 0.5 s, then a push-in through the face into the anatomy by 2.2 s. Three different images in the first 2.5 s.
- Body pace: lines run 145-200 wpm (median about 175), roughly one clause per caption group and one clause per shot.

## 5. Shot list

Times are from the 4 fps review sheet (±0.25 s). "Push-through" means the camera pushes into the body and the shot turns into the cutaway without a hard cut.

| # | Time | Shot type | What's on screen | Camera move | How the visual literalizes the line |
|---|---|---|---|---|---|
| 1 | 0:00.0-0:01.2 | High-angle wide | Girl on a pink bike with a wicker basket rides off the pool coping and crashes into the water; lounge chairs behind | Static high angle, slight follow down | "fall into a pool", exaggerated into slapstick (the bike is never mentioned) |
| 2 | 0:01.25-0:02.1 | Top-down through the water surface | Girl floating spread-eagle under the water, cheeks puffed | Fast push-in from full body to face to ear | "and water", the dunking that causes the problem |
| 3 | 0:02.2-0:03.6 | Anatomy cross-section, flat royal-blue background | Outer ear, canal, bone and cartilage layers, ossicles; a jet of water sprays into the canal and leaves a pocket sitting in it | Push-through into the cutaway, then near-static | "gets stuck in your ear", the stuck water made visible |
| 4 | 0:03.7-0:05.9 | Medium shot | Girl leaning on the pool edge tilts her head onto her shoulder; a cyan down arrow appears at 4.5 s | Slow push-in | "tilt ... straight down": the arrow spells out the direction |
| 5 | 0:06.0-0:07.4 | Medium close-up, over-the-shoulder side | Her hand rises and claps flat over her ear | Static, motion in frame | "press your palm flat over it" |
| 6 | 0:07.5-0:12.9 | Extreme close-up, half face + hand | Palm cupped over the ear, pumping; a cyan rim glow traces the palm edge on "sealing" (about 9.0 s); a blue cartoon plunger with the channel's logo pops in beside the hand at 11.5 s and pumps in sync | Very slow push-in | "sealing" → glow outline; "like a plunger" → a literal plunger prop |
| 7 | 0:13.0-0:16.6 | Anatomy cross-section resting on the forearm/palm, light-cyan background | Vertical canal section with bright green lines outlining the canal walls; the canal fills with a colour ramp red → orange → yellow → white → blue | Whip zoom in, then static | "lowers the pressure": pressure shown as a heat-map colour change |
| 8 | 0:16.75-0:19.2 | Macro inside the canal | Translucent water blob; white curved motion arcs and grey arrows pull it outward; it stretches into a hanging droplet | Push deeper into the canal | "creating a suction that loosens the water" |
| 9 | 0:19.25-0:19.6 | Transition | The cutaway dissolves back towards the arm | Pull-out / dissolve | Bridge back to the exterior |
| 10 | 0:19.7-0:20.9 | Medium close-up, canted | Girl lying with her head resting sideways on her hand, ear down, pool behind; cyan down arrow | Static, tilted frame | "your ear points down" |
| 11 | 0:21.0-0:22.9 | Anatomy cross-section, vertical canal | Cyan "9.8 m/s" label with a long down arrow; a streak of water slides down the canal wall | Slow drift downward | "gravity pulls it toward the opening", with gravity as an on-screen number |
| 12 | 0:23.0-0:24.4 | Low-angle extreme close-up from below the jaw | Eye, ear and cheek from underneath; her palm peels away from the ear | Whip-blur in, then static | "When you lift your palm away" |
| 13 | 0:24.5-0:26.1 | Anatomy cross-section, horizontal canal, cyan background | Water rushes along the canal walls, traced with white rim lines | Static | "the pressure snaps back to normal": the rush is the snap |
| 14 | 0:26.3-0:27.3 | Macro from below the earlobe, shallow depth of field | A thin trickle and droplet slide out of the ear; pool bokeh behind | Static macro | "the water finally slides out", the satisfying shot |
| 15 | 0:27.5-0:29.9 | Medium close-up, poolside | Eyes closed in relief → mouth open "ahh" → eyes open, small sideways smile | Slight head-tilt follow | The emotional payoff |

15 shots in 30 s, **about 2.0 s average**. The longest is shot 6 (5.4 s, kept alive by two overlays). Nine shots are exterior and six are cutaway or macro.

## 6. Visual grammar notes

- **Character design.** One recurring-type human: a tween girl in a semi-realistic 3D style (believable skin with pores, freckles and blotchy pink cheeks, slightly enlarged expressive eyes, two messy space buns), wearing a dusty-pink mesh sports tank with a small round chest patch. She never speaks. She acts out each instruction with clear, slightly exaggerated face acting (puffed cheeks underwater, a sideways doubtful glance, eyes closed in relief). One cute prop (a pink bike with a wicker basket) exists only for the opening gag. For our work, design our own character; do not reuse this look.
- **Palette.** Exterior: saturated pool cyan and blue, dusty pink wardrobe, warm skin, green foliage, beige paving. Cutaways sit on a **flat solid background**: deep royal blue for the first one, then a lighter turquoise/cyan for the rest. The anatomy uses textbook coding: porous beige bone, yellow fatty/cartilage tissue, pink skin, red and blue vessel stubs, cream cochlea and ossicles. Overlay graphics are one **bright cyan** (arrows, "9.8 m/s", the seal glow) plus **lime green** outlines for the walls. The pressure state uses a **red→orange→yellow→white→blue ramp**.
- **Lighting.** Bright sunny daylight with a soft key and warm skin. Specular sparkle and round white bokeh balls from the pool water. Shallow depth of field on the close-ups and macros. Cutaways are lit evenly like a studio product shot, with soft contact shadows where the section rests on the arm.
- **Materials.** Wet, glossy skin. Translucent refractive water (blobs, droplets, streaks with white highlight edges). Waxy, slightly glossy anatomy with sponge-texture bone and cell-texture fat. The cutaway reads like a cut physical model, not a flat diagram.
- **Camera language.** Constant forward motion: push-ins on almost every exterior shot. **Push-through** transitions from the outside of the body into the cross-section. Whip zooms or blurs into cutaways. A **canted frame** that matches the gravity direction of the line (head on hand). An unusual low angle from under the jaw for the release shot. A **macro** for the payoff. No static wides after the first 2 s.
- **Cut rhythm.** About 2 s per shot. The cut follows the clause: each new instruction or mechanism clause gets a new shot or a new overlay within 0.3 s of the word that triggers it. The cutaway segments get shorter towards the end (6 s → 2 s → 1.6 s), so the pace picks up into the payoff.
- **Overlays as literal translation.** Every abstract word gets a visible thing: direction → arrow, seal → glow outline, analogy → prop, pressure → colour, suction → motion arcs, gravity → number plus arrow. The narration never says "as you can see"; the picture just does it.
- **Caption style.** White semi-bold humanist sans, small (cap height about 3-4% of frame height), soft dark drop shadow, no box, no outline. 1-3 words per chunk, centred at about **78% of frame height**. Each clause starts with a capital ("Sealing the opening", "Creating a suction"). No karaoke word highlight, no emoji, no colour emphasis. Captions sit under every frame, including the cutaways.
- **Branding.** No watermark bug. The channel mark appears only *inside the world*, printed on the gag prop (the plunger cup). Note the technique only: put our own mark on an in-world prop, not as a corner logo.
- **Sound.** A single calm, unhurried narrator, mixed hot. A continuous bed (music plus splashes/SFX) about 6-8 dB under the voice and running through the sentence gaps, so there is never true silence until the last 0.4 s.

## 7. Transferable skeleton (no original wording)

For a 28-32 s second-person "fix it with your body" Short, about 85-95 words at 175-185 wpm, with a hook at about 220 wpm.

| Slot | Time | Content rule | Visual rule |
|---|---|---|---|
| 1 Hook | 0-3.5 s (≤14 words) | "If you" + an everyday mishap + the annoying result, ending on a comma so the first fix follows without a full stop | An exaggerated comic version of the mishap in frame 1, then a push-through into an anatomy/mechanism cutaway that shows the problem |
| 2 Step A (the plant) | 3.5-6 s | A simple positional instruction that seems like a minor detail. Do not explain it yet | Character acts it out; one bright overlay arrow shows the direction |
| 3 Step B (set-up) | 6-10 s | Instruction with one physics-flavoured word that plants the mechanism (closing, trapping, locking) | Extreme close-up of the hands; a glow outline on the planted word |
| 4 Step C (action) | 10-13 s | Repeated action + a household-object simile, with one safety softener ("gently", "slowly") | A cartoon version of the simile object pops into frame and copies the motion: the only gag in the middle |
| 5 Mechanism 1 | 13-19 s | "Each/every time you ..." + the invisible change + the result on the problem | Cross-section on a flat bright background; the invisible quantity shown as a colour ramp; push into a macro of the stuck thing starting to move |
| 6 Callback | 19-23 s | "And since/because" + step A's state + a second force finishing the job | Cut back to the character holding step A's pose (canted frame), then a cutaway with the force as an on-screen number and arrow (unit checked!) |
| 7 Release | 23-26 s | The final action is letting go; the system "returns/resets", with one sharp sound-verb | Unusual angle on the release; a short cutaway of the system resetting |
| 8 Payoff | 26-30 s | "and ... finally ..." + the result, ending on the title's own object noun. No CTA | A satisfying macro of the result, then the character's relief face; hard end on the last word, so the end loops back to frame 1 |

Rules to keep:
- Instructions in imperative mood; mechanism lines in present tense with "you/your" kept in. Five sentences or fewer.
- At least 40% of the runtime on *why*, even though the title promises *how*.
- Plant one step early and pay it off as part of the mechanism. That callback is the "aha".
- Every abstract noun gets a literal on-screen object (arrow, glow, prop, colour, number). Gags stay visual; the narration stays deadpan.
- Alternate body exterior and cutaway; make the cutaway segments shorter towards the end.
- Title: "How To [fix] [Common Body Annoyance]" + 🤔, Title Case, about 7 words.
