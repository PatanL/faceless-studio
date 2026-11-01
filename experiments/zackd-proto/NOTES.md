# zackd-proto: can the code-only stack reach the Zack D.-style look?

Internal feasibility test only. We used the format research (`research/corpus/zackd/VISUAL_GRAMMAR.md`, `PLAYBOOK.md`) to learn the format. The script, character, set and shots are original and are not meant for publication.

**Answer: yes, for the grammar. Not yet for the polish.** A 12.9 s, 1080x1920 low-poly 3D shot rendered in **58-60 s wall time** on the Spark CPU (`--concurrency=2`, nice 10, SwiftShader WebGL), bundling included. It lands inside the reference ranges on luma, saturation, hue split, caption geometry and loudness range (table below). It reads as "toy low-poly". It does not read as Zack's "toy-real": there is no subsurface skin, no bloom pass, no ambient occlusion, and the character is made of primitives and has no acting rig.

- Render: `out/zackd-proto/zackd-proto.mp4` (Mac). The Spark copy is `~/studio/app/experiments/zackd-proto/out/zackd-proto.mp4`.
- Contact sheet at 2 fps: `contact_sheet.jpg`.

## What the shot is

The beat is a survival "what to do if" line said in the second person and acted out literally on screen. It follows the hook formula H3 (an "If you…" mishap fused to the instruction) and squeezes the p832 failure-then-release ladder into one sentence. Wording is ours, and `originality_check.py` prints PASS.

> If you ever get locked inside a walk-in freezer, don't burn your body heat pounding on the steel door, because right beside the latch is a glow-in-the-dark knob that pushes it open from inside.

34 words in 12.2 s, which is 167 wpm (inside the playbook's 165-180 target). The voice is Kokoro `am_michael` 0.96 through the existing `pipeline.audio.make`, explainer niche, `ending: loop`. Kokoro gave 100% of the word timings. The mix has the `documentary_pulse` bed plus marker SFX: knock3 on "pounding", whoosh on the whip, click on "pushes", creak on "open".

The shot has 8 pictures in 12.9 s, an average shot length (ASL) of 1.6 s. One character (orange hoodie: the warm subject against cobalt and cyan). One set (a walk-in freezer, plus the warm room seen through its door).

| t (s) | words | picture / literal device |
|---|---|---|
| 0.0 | If you ever get locked | frame 0 is the action: the door slams shut on the warm light, with a camera shake on the slam and a startled turn |
| 1.36 | inside a walk-in | whip-smear into a low-angle wide: racks, frosted boxes, icicles, floating ice motes |
| 2.38 | freezer | face close-up: frosted brows, chattering teeth, breath puffs, shiver |
| 3.35 | don't burn your body heat | **heat literalized**: an orange aura plus wisps that leave the body and cool to cyan (heat-ramp signal) |
| 4.80 | pounding on the steel door | over the shoulder, fists strike on each knock SFX with a screen shake per hit; each knock visibly drains heat; **red failure flush** on "door" |
| 6.84 | because right beside the latch | whip to the inside face of the door; a yellow input-highlight outline lands on "latch" |
| 8.73 | is a glow-in-the-dark knob that pushes it | money shot (2.3 s hold): the room dims and the knob glows `sig.tag.green` with an outline shell and halo; a POV forearm enters and a fingertip pushes the knob 2 cm on "pushes" |
| 11.06 | open from inside + 0.6 s tail | hard cut to the frame-0 wide: the door swings open, warm light floods the floor, the camera pulls back to the exact frame-0 framing (loop seam) |

## Measured against VISUAL_GRAMMAR section 12

We ran the reference measurement code (`~/studio/tmp_zackd_palette/palette.py`) through `measure.py`.

| check | target | ours |
|---|---|---|
| median luma (bright register) | 100-175 | **131.5** (p10-p90 104-143) |
| median saturation | 0.35-0.60 | **0.376** |
| blue share / warm share | 40-78% / 15-50%, sum ≥70% | **56% / 30%** (86%) |
| centre minus corner luma | about +10 | **+27.6**: our CSS vignette is too strong; halve it |
| caption centre / band / width p90 | 0.78 ±0.005 / 3.0-3.8% / ≤72% | **0.785 / 3.28% / 69.6%** |
| loudness | about -12 LUFS, LRA about 2 | -14.1 LUFS, LRA 1.3 (pipeline default; the Zack spec wants about 2 dB hotter) |
| ASL / money-shot hold / tail | 1.2-1.8 s / 2-5 s / 0.5-0.9 s | 1.6 s / 2.3 s / 0.6 s |

## Approach

- **Path A from the grammar (low-poly 3D in the browser)**, using its own Remotion project in this folder: `remotion` 4.0.539 + `@remotion/three` 4.0.539 + `@react-three/fiber` 9.8.1 + `three` 0.185.1. The `npm install` on the Spark took 10 s. Nothing in `studio/src` is imported, because a second copy of `remotion` from another node_modules would break the contexts. The captions were therefore re-implemented in about 80 lines.
- Every value is a pure function of `t` (`src/timeline.ts`): shot list with eased push-ins, whip windows, shake impulses, door angle, light levels, heat level, poses and expressions. Any frame renders on its own, which is what makes parallel rendering deterministic.
- Lighting follows grammar section 5:
  - a hemisphere fill in world blue;
  - a soft key from above and in front with PCF shadows;
  - a warm gold rim light re-aimed every frame so it always sits behind the subject relative to the camera;
  - a warm spot through the doorway as the payoff practical.
- `flat` (no tone mapping) keeps the palette hexes predictable.
- Post effects are done in the DOM, not in WebGL:
  - the whip smear is an SVG `feGaussianBlur stdDeviation="X 0"` plus a translate, over 3 frames each side of the cut;
  - shake is a CSS translate;
  - the failure flush is a multiply layer;
  - the vignette is a radial gradient.
- Captions follow grammar section 9: one line, 68 px Montserrat 800, white with a soft shadow, no box, 2-3 word cards cut at phrase boundaries and locked to the Kokoro word times, auto-shrunk so a card never exceeds 72% of the width.
- The task asked for "word-highlight captions", but section 9 measured "no karaoke highlight" in 9/9 references. The highlight therefore exists as a prop (`highlight: true` dims the not-yet-spoken words of the card) and is **off** in the render.

## Time it took

About 17 min wall time from reading the brief to the final MP4 (20:18-20:35 UTC), with no prior 3D code in the repo:

| step | time |
|---|---|
| npm install | 10 s |
| TTS + mix | 20 s |
| still passes (bundle + 6-12 PNGs) | about 27 s each, 2.3-2.9 s per still frame after bundling |
| full render | 58-60 s for 387 frames, about 0.15 s per frame per tab at concurrency 2 |

The load average was 7-33 from other jobs.

**CPU WebGL is not the bottleneck.** The open question in the grammar, "CPU WebGL rendering speed on the Spark is unmeasured", is answered: a 35 s Short with this scene complexity should render in about 3 min.

## What was hard

1. **Camera placement without a viewport.** Every framing bug cost one still pass:
   - the camera sat inside a shelf rack;
   - the face close-up was too close;
   - the POV hand covered the knob.

   A real kit needs a "frame this object at N% of H from angle A" helper instead of hand-typed positions.
2. **Arms and hands.** Forward kinematics with Euler angles on capsules is fiddly. Fists hitting the door and a fingertip landing on a 9 cm knob had to be solved by hand: the POV forearm is placed by two points instead of by the character's own arm. Zack's "hands only in POV" convention helps here.
3. **Glow and bloom.** There is no post-processing pass. A green outline shell plus an additive halo sprite plus emissive reads well. The first attempt, a point light, flooded the whole frame green.
4. **Units mismatch bugs.** One example: the knob push was 0-1 m instead of 0-2 cm, so the knob vanished into the door. Pure-function timelines make these easy to find in stills.
5. **Light count must stay constant.** Lights are always mounted with intensity 0 instead of being conditionally rendered, because a change in light count recompiles every shader.

## The look gap (honest)

- **Reads as Zack-grammar:**
  - frame 0 is the action;
  - every noun gets its picture;
  - the camera always moves;
  - the cool-world/warm-subject palette;
  - meaning-locked signals (green = named thing, yellow = input, red = failure, heat ramp);
  - captions;
  - the loop seam.
- **Reads cheaper than Zack:**
  - a primitive-built body (capsules, a sphere head) with a bowl-cut hair cap;
  - no fingers except the POV hand;
  - no cloth folds;
  - flat walls without ambient occlusion (AO) or texture;
  - shadows are hard-ish PCF;
  - no depth of field;
  - the heat aura draws over the body (it ignores depth) and looks more "glow filter" than "volumetric".

  This is the "distinct hand-built low-poly" look the imitator data favours (cg-3d 4/7 at 10K+). It is not photoreal, and should not try to be.

## What a full kit would need

1. **Character system:**
   - a reusable rigged low-poly person (glTF built once in Blender by hand, or procedural), with real joints, 2-bone IK for hands and feet, and 5+ expression presets (blendshapes or swappable mouth/brow meshes);
   - wardrobe colour as a prop.

   This is the biggest gap.
2. **Prop library:** 30-50 rigid low-poly props for the recommended "how old things worked" and history lane (castle wall, gate, lever, gears, rope, cart, tools). Rigid objects are where this stack already looks good.
3. **Shot helpers:**
   - `frame(object, coverage, angle)` and `follow(path)`;
   - an orbit/crane/crash-zoom library;
   - shake and whip presets taken from grammar section 7, with numbers.
4. **Signal-icon library:** green outline, yellow highlight, red force arrows, cyan direction arrow, chevron ring, pain bolts, stink vapour, x-ray inset (a stencil or clip-plane cut-away), thought bubble, calendar flip. Each needs a meaning lock-check in QA.
5. **Look upgrades worth their CPU cost** (benchmark each):
   - `@react-three/postprocessing` bloom + SSAO;
   - soft shadows (VSM or PCSS);
   - baked AO on static props;
   - fake depth of field on close-ups (render the background layer blurred).
6. **Storyboard schema:** words map to shots, cues and icons (JSON), so a writer's beat table drives the render the way `studio/src/core` does for the 2D kits. The audio pipeline already supplies word times and cue times.
7. **Mix preset:** a Zack theme at about -12 LUFS, a bed 6-8 dB under the voice, and foley on every visible action.
8. **QA:** run `measure.py` on every render, with the section 12 thresholds as a gate, and halve the vignette.

## Files

| file | purpose |
|---|---|
| `src/timeline.ts` | word times, shots, every state function |
| `src/Scene.tsx` | lights, camera rig, actors |
| `src/Set.tsx` | freezer set, door, latch, knob glow |
| `src/Character.tsx` | person, poses, expressions, POV arm |
| `src/fx.tsx` | frost motes, breath, heat aura |
| `src/Captions.tsx` | captions |
| `src/Proto.tsx` | composition and DOM post effects |
| `script.md` | narration |
| `public/audio/*.json` | word and cue times; the wavs stay on the Spark |
| `stills.sh` | bundle once, then render still PNGs (Spark) |
| `measure.py` | grammar section 12 measurement |

To reproduce on the Spark, from this folder: `npm ci`, then `python -m pipeline.audio.make experiments/zackd-proto/script.md --niche explainer --id zackd-proto --out experiments/zackd-proto/public/audio` (from `~/studio/app`), then `nice -n 10 npx remotion render src/index.ts ZackdProto out/zackd-proto.mp4 --concurrency=2 --gl=swangle`.

## Review

Strict review of `out/zackd-proto/zackd-proto.mp4` (12.9 s). Method: I pulled frames on the Spark CPU (ffmpeg, nice 10, 2 threads): 10 fps over the hook (0-1.6 s), 6 fps over the knock and the payoff, 30 fps across the 6.84 s whip, 6 fps over the latch shot, plus 9 matched pairs of 540x960 frames. Each pair puts one of our shots beside the closest shot type in **p832whe8hrI** (trapped-car survival: POV hands, failure flush, green tag, breaker payoff), **jHbhgBgaA34** (human acting: pained close-ups, pain bolts, face macro) or **0BZ1C83I2R4** (rigid-object world, hand-held payoff). Loudness is from `ebur128` on all three files. The work files are in `~/studio/tmp_review/` on the Spark (`pair*.jpg`, `strip_*.jpg`). I did **not** listen to the audio by ear, so the audio score covers only the levels and the cue placement.

### Scores

| area | weight | score /100 | why |
|---|---|---|---|
| Visual polish | 20 | **30** | The palette logic is right: cool world, warm subject, no greys. The surfaces are not. Every wall, door and floor is an untextured flat plane with no AO, no bevels and no contact shadows except under the knob. The latch is a plain box and the knob is a bare sphere. In the 0BZ1 frames every rigid prop has wear, bevels, specular breakup and bloom. For 2.3 s the knob glow turns the **whole frame green**, so the cool world is gone during the money shot. The heat aura flattens the shot to beige: the subject, the door and the legs all turn the same tan. The "red failure flush" measures as a mauve-grey multiply over blue and does not read as red. |
| Character appeal | 20 | **15** | It is a capsule mannequin: a sphere head, a bowl hair cap, sphere fists and mitten hands. Front-facing time is about 2.4 s of 12.9 s; the hook, the knock and the payoff all show his back. There are no in-betweens: the knock snaps between two key poses. He stands frozen for the whole hook and the whole payoff, so when the door opens there is no relief, no step and no expression. Beside the jHbhg close-up (pair 2) ours reads as a children's-app placeholder. This is the gap a viewer notices first. |
| Narration literalized | 20 | **50** | Every clause has a picture assigned, and the timing is within the 0.5 s rule. Several of those pictures don't read, though:<br>- "pounding": the fist never touches the door. The arm alternates between overhead and a forward reach, with nothing at the point of contact.<br>- "the latch": it is a featureless box, and the yellow highlight shows up as a misaligned flat L-plate behind it, not an outline glow.<br>- "glow-in-the-dark knob": the knob is already on screen, unlit, before it is named.<br>- "pushes it open": the POV mitten touches the knob, then a hard cut lands on a door that is already ajar.<br>- "locked inside": frame 0 is a slow swing behind a still figure, not a slam.<br>The p832 pairs show the bar: hands flat on the glass with a red flush, and a breaker cracking the glass on the word. |
| Motion and camera | 15 | **45** | Push-ins run on every shot. The whip smear at 6.84 s is clean, 3 frames each side, and is the most convincing effect in the piece. There is shake on the knocks. Against that: the subject barely moves in the first 1.3 s, the latch shot is about 1.9 s of near-static push on two primitives, there is no crash-zoom or snap-zoom anywhere, and the payoff is a pull-back on a figure that doesn't move. In the references the camera follows a moving cause; here it mostly frames poses. |
| Captions | 10 | **78** | Geometry is on spec (0.785 / 3.28% / 69.6%). The 2-3 word chunking is correct. Lost points:<br>- the first card is still fading in at 0.1 s, and the card is ghosted at about 50% opacity through the whip (the spec allows a 2-3 frame pop at most);<br>- "is a glow-in-the-dark" makes a long 4-token card;<br>- Montserrat is visibly squarer than the rounded face in the references. |
| Audio | 15 | **50** | -14.1 LUFS / LRA 1.3. p832 measures **-11.6 / 2.1** and jHbhg -14.1 / 2.8, so we are 2.5 dB quieter than the survival reference and flatter than both. Foley is missing on visible actions: no slam at frame 0 (the hook action is silent), no whoosh on the 1.36 s whip (only the 6.84 s whip has one), and nothing for the chattering teeth or the shiver. knock3 is one 1.3 s sample rather than one hit per visible strike. The voice is Kokoro TTS against Zack's human deadpan narrator; I have not judged it by ear. |
| **Weighted total** | | **41 / 100** | The three Zack references I compared would score about 90 or more on this rubric. |

### Would a scrolling viewer accept it as the same tier?

**No.** The first frame is the back of a capsule figure standing in a flat blue box. In under a second that reads as "Roblox / kids' cartoon / test render", not "Zack D. Films". Viewers will not judge it as a slightly cheaper version of the same thing; they will file it as a different, lower genre. It is also below the good *hand-built low-poly* accounts the imitator data favours. Those accounts look art-directed: faceted models with deliberate bevels, baked AO, a consistent stylised character and real hands. Ours looks like default primitives. The grammar (palette split, cut rhythm, caption block, signal colours, loop seam) is genuinely in range, but the grammar is invisible to a viewer unless the surface clears the quality bar first.

### Biggest gaps, in order

1. **The human, and above all the hands.** Zack's people are mostly forearms and hands in POV, plus a few big-expression faces. We need an authored, rigged character with real fingers and facial controls, and a separate POV hand rig (flat palm, push, grab, point). This is an asset to author once in Blender or source under a license, not something to code. None of the signal or camera work matters while the hands are spheres.
2. **Surface finish on rigid props and sets:** bevels, baked AO, roughness/normal breakup and contact shadows on every prop, plus a bloom pass so glows stay local (no full-frame green flood). This is the cheapest gap to close, and it is where code-3D can actually get near the reference (0BZ1-style objects).
3. **Actions that make contact.** Fist on steel, finger depressing the knob, the door visibly swinging *because* of the push, the character stepping into the warm light. Every literal verb needs an on-frame cause-and-effect, with a foley hit on the frame of contact.
4. **Camera that follows the cause:** a crash-zoom or snap-zoom on the reveal (the knob), a follow move on the payoff, and no 1.9 s holds on static primitives.
5. **Mix:** about -12 LUFS, foley on every visible action, and one SFX per strike.

### 2D or 3D?

**3D, but only in a narrow lane, and only after the hand/character asset exists.**
- 2.5D SVG would not reach "same tier" either. It would be a different format: a 2D explainer that viewers don't compare to Zack at all, in a lane our existing kits already cover. It also gives up the format's main hook, the toy-real 3D world.
- The prototype shows where code-3D already works. The rigid-object shots (door, latch, knob, whip smear) are plain but structurally sound, and they have a clear upgrade path (bevels, AO, bloom). The shots that fail are all character shots.

So the bet is:
- choose 3D for rigid-object and mechanism subjects ("how X works", the history and old-tech lane in PLAYBOOK section 11);
- keep humans to POV hands plus at most one or two short face reactions per video;
- don't publish character-acting stories in this stack until a rigged, finger-capable character exists.

Before committing to the lane, benchmark bloom + SSAO + soft shadows on SwiftShader. The 58-60 s render time we measured has no post-processing in it, and that number will change.
