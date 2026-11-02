# Story lane: checking the "viral animated Shorts with Claude" tutorial against RicksClips3000

Checked 2026-11-02. Source: YouTube "How to Make Viral Animated Shorts Using Claude (Full Workflow)" by Mr omi
(OtbLL6OBNE4, 122K views). Transcript: Spark `~/studio/refs/ig/lesson_OtbLL6OBNE4.txt`. The 20 Shorts it studied are
RicksClips3000's own: its repo names `01_Mz72MuPgnGY`, and the hooks it quotes are from our list (grave bell, mirror
horse race, knight loophole, button town). Its claims about "the channel" are claims about our story-lane reference.

## What was measured

- **References:** 8 RicksClips3000 Shorts at 720x1280, 30 fps. They are on the Spark as `~/studio/refs/ig/ricks720_<id>.webm`.
  The two older `ricks_*.webm` files are 360x640, so all 8 were downloaded again at 720p.
  - 7xS87iActkU Railroads, 7.2M
  - VS1Z_Q-Klt8 Jar, 30M
  - Mz72MuPgnGY Storm oil, 10M
  - 5WMQhPObNqQ Mirror, 4.5M
  - ZDy3xXA2iHk Button, 3.1M
  - GM9UKnZ6JFw Grave bell, 10M
  - jpFJ8Z_F-qU Knight, 1.5M
  - 0m6G8pDtzNs Japan job, 15M
- **Ours:** `out/story-chess-turk/story-chess-turk_v4.mp4`. It is byte-identical to the Spark's `story-chess-turk_9x16.mp4`.
- **Tools:** every tool runs on every frame unless marked otherwise.
  - `research/frame-analysis/tools/frame_metrics.py` finds hard cuts, flashes and gradual transitions.
  - `pipeline/qa/frames30.py` writes 2 s every-frame sheets and one-frame jump flags.
  - Three new research tools came out of this check:
    - `camera_motion.py`: a sub-pixel phase-correlation similarity fit on 9 tiles, with the caption band excluded.
      I checked it on a synthetic clip with a known path:
      - a still hold reads 0.004 px/f;
      - a 0.25 px/f drift reads 0.29;
      - a 23 f smootherstep move of 100 px reads peak 8.2 px/f (expected 8.15) and an equivalent length of 24 f;
      - a 0.20 %/f push-in reads 0.15 %/f, so push-in rates are under-read by about 25 %.
    - `look_stats.py`: tone, black level, shadow and highlight colour, ink on edges, and soft (lens-blurred) edges.
      It reads every 3rd frame at 720x1280 and masks the caption band.
    - `speech_pace.py`: words per second, pauses and the "You see" positions, from word timings. For the references
      those timings come from YouTube's English ASR json3. For ours they come from `captions.json` (Kokoro).
  - A dissolve detector checks whether frame j is a blend of frames j-5 and j+5. Its counts are a lower bound.
    VS1Z has one more dissolve, at 13.4 s, that I confirmed by eye.
- **Data:** `research/references/data/story_lane_check_data.json`. Working files are on the Spark in
  `~/studio/scratch/storylane/`.
- **Speed units:** px/frame at 720x1280. Speed = 2·|translation at 360 px wide| + (|zoom| + |roll|)·734. The repo uses
  the same definition.

## 1. Verdict on each claim

### Script

| Claim | Holds? | Measured (8 refs) | Ours |
|---|---|---|---|
| Paradox stated as fact in sentence 1, no intro | **Yes** | 8/8 (e.g. "They buried a man alive with a bell tied to his finger.") | Yes ("He built a chess robot that could beat anyone, and before every game, he opened it up to prove it was empty.") |
| Escalate → pivot → payoff → twist last line | **Yes** | All 8 end on an ironic last line, and the video stops on the last word | Yes (ends "a man in a box, playing by candlelight.") |
| Pivot with "You see," (14/20) | **Half right** | "You see" appears in 7/8, but it does two different jobs. In 4/8 (0m6, 5WM, GM9, Mz7) it flips into the mechanism at 67-91 % of the runtime. In 4/8 (GM9, jpF, 7xS, VS1Z) it opens the backstory right after the hook, at 5-11 %. GM9 uses both. ZDy3 never says it | One, at 9.8 % (the backstory-bridge use) |
| ~4 words per second | **Roughly** | 3.33-3.89 wps, median 3.75 (7xS is the slow one at 3.33) | **3.13** |
| Near-zero dead air | **Yes** | 0-1 pause ≥ 0.8 s per video; summed excess ≤ 0.44 s | **5 pauses, 3.6 s** |

### Visuals

| Claim | Holds? | Measured | Ours |
|---|---|---|---|
| Real 3D world, flat 2D characters | **Yes** (by eye and by fit) | Sets show perspective and parallax. The similarity fit fails on 68-341 frames per video, mostly 3D dolly parallax. Characters are flat cards | Flat layered sets: only 18 frames fail the fit |
| Characters lit and shadowed by the key light | **Partly** | Cards take on the scene colour (blue at night, warm by lamps) and have contact or cast shadows. I saw no form shading on faces. Faces stay near white | Characters in their own flat colours |
| Black ink on ~3/4 of the 3D edges | **Most, not 3/4, by our measure** | Median share of strong edges with an ink line within 2 px: 54-66 % per video. The repo's hand scans say 74 % (36/49); its automated count says 45 % | **17 %** |
| Saturated colour | **Yes, moderately** | HSV S median 0.41-0.61; colourfulness 23-34 | **0.73; colourfulness 60.** Ours is about twice as colourful: over-saturated, not under |
| Warm highlights, cool blue shadows | **Mostly** | Shadows (Y' < 0.3, non-ink) have b* < 0 in 44-89 % of frames in 6/8. The median shadow hue is 295-306° in Lab (violet-blue, a* > 0) in 6/8. 7xS (36°) and jpF (48°) have warm shadows. Highlights have b* > 0 in 48-94 % of frames, but only mildly warm (median b* −1 to +21) | Shadow hue 306°, the same family, but chroma about 83 against ≤ 35: our "shadows" are big indigo fills |
| No pure black | **Mostly** | Median frame has 0 % black area (Y' < 0.06, excluding lines). Non-ink p5 is 0.09-0.23. But Mz7 (night sea) has > 1 % black area in 51 % of its frames, 5WM in 23 %, GM9 in 17 % | 0 % black; non-ink p5 0.14 (in range) |
| Purple shadows at sunset | **Plausible (by eye)** | VS1Z's sunset at 29.6 s has a violet-pink sky and violet shade. I didn't measure it separately | — |
| Lighting follows the story; deep night blue at the explanation | **2 of 4** | Of the 4 videos whose late "You see" starts the explanation: Mz7's frame b* goes −1 → −54 after it (night blue) and 0m6's goes −8 → −30 (luma 0.58 → 0.37). 5WM only gets darker (0.50 → 0.40), not bluer. GM9 gets brighter and warmer (sunrise). Lighting does change by beat in every video | Indigo almost throughout |
| Background lens blur | **Yes, mild** | Soft-edge share 4-15 % of strong edges (median per video), edge acutance 0.32-0.42. Clear DOF on close-ups by eye (e.g. VS1Z 13.6 s) | 1.5 %, acutance 0.47: everything razor sharp |
| ~3.5 heads tall, thin limbs | **Roughly** (by eye, 6 frames) | Adults about 3-3.5 heads, single-line stick limbs, round heads | Similar stick build; not measured |

### Camera

| Claim | Holds? | Measured | Ours |
|---|---|---|---|
| 12/20 have ≤ 1 hard cut | **Yes, stronger** | 7/8 have ≤ 1 hard cut (cuts per video: 1, 1, 3, 0, 0, 1, 0, 0). But scene changes are often **6-8 frame dissolves**: at least 0-9 per video (VS1Z ≥ 10). The repo's own STYLE_BIBLE says the same | **20 hard cuts** (+ 54 one-frame jumps flagged by frames30, against 0-12) |
| The camera travels into the next moment | **Yes, alongside dissolves** | 15-25 "gradual transitions" per video, most of them fast continuous camera travel (crane, whip, push-through) | 6 |
| Moves ease over ~23 frames | **At the short end** | Move length as an equivalent smootherstep (FWHM / 0.54): median 24-63 f per video, about 40 f across videos. Peaks median 15-27 px/f | 20 f, but only 2.1 moves per 10 s against 5.1-9.6 |
| Camera moving in ~65 % of frames, slow push-ins | **Understated** | Moving (≥ 0.3 px/f) in 96-100 % of fitted frames; ≥ 2 px/f in 77-92 %; dead-still 0-4 %. Median speed 5.8-11 px/f. In quiet frames (translation < 2 px/f) the zoom is active in 69-89 % and pushes in in 43-80 %, at about 0.2-0.47 %/f. The tutorial's "65 %" is the repo's ≥ 2 px/f class; its first "80 % still" was wrong, as the tutorial itself admits | **Still in 30 %**, moving 70 %, ≥ 2 px/f only 24 %. Median speed 0.58 px/f (10-19x slower). Quiet-frame zoom active 29 %, 0.10 %/f |

### Build and repo

| Claim | Holds? | Notes |
|---|---|---|
| RicksClips is made in three.js | **Unverified** | It's the tutorial author's hunch ("Maybe these shorts are made with 3JS"). The look fits any real-time toon 3D renderer. What is true: the tutorial's own Short is three.js inside Remotion |
| @remotion/three, free 3D models, code-painted textures, edge-detection ink, DOF, agents split by files | **Yes, for their build** | All in the repo: Kenney CC0 models (not included), Canvas2D textures, a separate ink Pass before DOF, 64-tap lens blur, five file-owner sandboxes |
| "5,000 reference images" | **No** | The repo has 38 full frames + 20 contact sheets (1,200 frame tiles) = 58 image files |

## 2. Ours against theirs: biggest gaps (ranked)

1. **Camera grammar: we cut and sit, they glide and never stop.**
   - Hard cuts: 20 for us, 0-3 for them.
   - Median camera speed: 0.58 px/f for us, 5.8-11 for them.
   - Dead-still frames: 30 % for us, 0-4 % for them.
   - Moves per 10 s: 2.1 for us, 5-10 for them.
   - Push-ins during holds: 29 % of quiet frames for us, 69-89 % for them.
   - Our storyboard also adds a slow sine "shake" (amplitude 3, 0.22 Hz). The repo measures no hand-held float in the reference.
   - This is the cheapest gap to close and needs no 3D.
2. **Flat sets against a 3D world.**
   - No parallax: 18 frames fail the similarity fit for us, 68-341 for them.
   - Ink on 17 % of edges, against 54-66 %.
   - No lens blur: 1.5 % soft edges, against 4-15 %.
   - No light pools or cast shadows.
3. **Colour is too loud and too dark in the middle.**
   - Saturation 0.73 against 0.41-0.61.
   - Colourfulness 60 against 23-34.
   - Median luma 0.24 against 0.31-0.58.
   - Shadow chroma about 83 against ≤ 35.
   - House style A's indigo fills read as "flat poster". The reference reads as "lit storybook".
4. **Narration is slower and pausier.** 3.13 wps against 3.33-3.89 (median 3.75), and 3.6 s of pauses against ≤ 0.44 s.
   At their pace our 207 words would take about 55 s. Either write about 240 words for 64 s, or speed up Kokoro and cut the pauses.
5. **Already matching:**
   - the hook shape;
   - the "You see," backstory bridge;
   - the twist ending;
   - the black level;
   - no pure black;
   - violet-blue shadow hue;
   - mean luma (0.41, in range).

## 3. The GitHub repo (mromidev/claude-animated-shorts)

- **Where and what:** cloned read-only at `~/studio/third_party/mromidev-claude-animated-shorts/repo`. Commit `e3b817b` (2026-11-01), 36 MB, MIT, 308 stars.
- **What I did and didn't do:** I read the README, SKILL.md, STYLE_BIBLE, CONTEXT and the motion, outlines and grade reports. I skimmed the ink, story and build sources and the helper scripts. Nothing was run, and nothing was installed into any Claude config.
- **Safety scan:** the scripts only call ffmpeg/ffprobe and copy files. There are no network calls.

**What's in it**
- `SKILL.md`: the pipeline (facts → script at ~3.7 wps → voice + words.json → shot plan in `story.ts` → world →
  characters → post → synthesized sound → stills and side-by-sides → render → frame QA). Also final look values and a
  "look-match loop": one measuring agent per topic, then one owner per file in sandboxes, merge, then a fresh verifier
  scoring each area out of 10.
- `references/reports/*.md`: seven measured reports (motion, depth, textures, characters, lighting, outlines, grade).
  Each has numbers, method and a TypeScript/GLSL recipe. The best are motion.md (camera grammar table), outlines.md
  (ink widths per edge type) and grade.md (tone targets).
- `templates/bridge/*.ts(x)`: the whole three.js source of their bridge Short.
  - `ink.ts`: world-only normal + depth re-render; ink where the 2nd difference of 1/z jumps and on normal creases; its own Pass before DOF; a `NOINK` layer for character cards and sky.
  - `lensblur.ts`: 64-tap gather.
  - `grade.ts`.
  - `lights.ts`: day and golden presets.
  - `shade.ts`: two-tone shading.
  - `paint.ts`: Canvas2D painted textures.
  - `toon.ts`: a `Pen` drawing API for characters, with 14 faces.
  - `cast.ts` / `cardshade.ts`: billboard cards lit by the scene.
  - `story.ts`: SHOTS, CAMS, DOF and KICKS tables.
- `templates/audio/`: synthesized SFX and a march score with ducking. We have our own.
- **Caveats for us:**
  - The scripts are Windows-specific (a `chrome.exe` path, TEMP).
  - They assume a GPU via ANGLE. Our Spark rule forbids the GPU, so WebGL there would run on SwiftShader (CPU).
  - `public/` (the Kenney models, ~1.3 GB of bundle copies) isn't in the repo.
  - STYLE_BIBLE.md's "ease-out bursts, holds 80 %" is superseded by its own motion.md.

**Licence**
- **Code and docs:** MIT ("Copyright (c) 2026 Mr omi"). We may reuse, adapt and ship the rules, numbers and code, if
  any substantial copied portion keeps the copyright and permission notice. If we port `ink.ts` or `lensblur.ts`, add
  the MIT notice in the file header.
- **Reference frames and sheets (`references/frames`, `references/sheets`):** these are screenshots of RicksClips3000's
  videos. Mr omi can't license someone else's frames, and his README says they're "for style study only". Don't copy
  them into our repo or use them as assets. Our own 720p downloads on the Spark do the same study job.
- **Kenney models:** CC0, but fetch them from kenney.nl ourselves.
- **The measured numbers:** facts, so they're free to use. Our own measurements above are better anyway.

## 4. Plan for our story lane

**Goal:** close gaps 1-4 in order of cost, and prove each with the same tools against the 8 references (docs/PARITY.md).

1. **Camera grammar.** About a day, and it works in the current 2D kit, so it comes before any 3D.
   - **Changes:**
     - Hard cuts only on big jumps (target ≤ 3 per Short).
     - Place changes become 6-8 f dissolves or a camera move that carries through to the new place.
     - Every hold creeps in at 0.2-0.35 %/f, with about 0.6 %/f on punch words.
     - Reframes become smootherstep glides of 24-40 f, peaking at ≤ 25 px/f at 720p.
     - About 6 moves per 10 s.
     - Remove the sine float.
     - Impacts get a 6-7 f kick that flips sign every frame.
   - **Targets (camera_motion.py, frame_metrics.py, frames30):**
     - moving ≥ 95 %;
     - median speed ≥ 5 px/f;
     - quiet-frame zoom active ≥ 70 %;
     - ≤ 3 hard cuts;
     - ≤ 12 one-frame jumps.
2. **Narration pace.** Script about 240 words per 64 s at Kokoro speed ~1.1-1.15. Gaps ≥ 0.8 s: at most 1. Keep the
   paradox hook. Use "You see," either as the backstory bridge after the hook or as the pivot into the mechanism, not
   both. Target 3.6-3.9 wps.
3. **3D feasibility test.** Half a day, in `experiments/three-lane/`, not the kit.
   - Install `@remotion/three` + three + @react-three/fiber + postprocessing pinned to our Remotion 4.0.539.
   - Render one 1080x1920 frame of a test room with an ink Pass and DOF:
     - on the Spark (SwiftShader, CPU, `--concurrency=2`);
     - on the Mac slot through `scripts/render.sh`.
   - Record seconds per frame. If the Spark costs more than ~3 s per frame (about 1.7 h per Short), render the 3D lane at 720x1280 and upscale (the reference itself is served at 720p), or prefer the Mac slot.
4. **One 3D set, end to end.** A chess-turk palace hall: Kenney CC0 props recoloured to our palette, Canvas2D painted
   wood, stone and plaster with dark seams, and two-tone toon shading (warm key, violet-blue shade). Add fog in the
   horizon colour.
   - **Ink:** our own Pass before DOF, following the outlines.md approach (MIT notice if ported).
   - **Lens blur:** on close and medium shots only.
   - **Grade targets (look_stats.py):**
     - saturation 0.42-0.60;
     - colourfulness 25-34;
     - mean luma 0.36-0.56;
     - non-ink p5 0.09-0.23;
     - shadow hue 290-310°, chroma ≤ 35;
     - ink_edge 0.55-0.65;
     - soft_edge 5-15 %.
5. **Characters as lit cards.**
   - Draw our existing stick/Person rigs to a canvas texture on camera-facing planes, on a NOINK layer, lit by the scene light, with contact shadows.
   - Proportions: about 3-3.5 heads, thin limbs.
   - Animation: blinks every 0.5-2.3 s, walk bob 3-7 %, acting beats 0-3 f before the word.
6. **Story lighting.** A per-beat light table (day → golden → night). Use night blue for the explanation when the story allows, as Mz7 and 0m6 do.
7. **Parity run.** Re-measure the remade chess-turk (or the next story Short) against these 8 with the same commands,
   log it in docs/PARITY_LOG.md, then run the blind panel.
   - Agent split for steps 4-5, by files in worktrees, one owner each: camera/story, world/lights/grade, materials/paint/build, characters, post (ink/DOF). Merge file by file.

**Build first:** step 1 (camera) and step 2 (pace) in the current kit, because they close the largest measured gaps
cheaply. Then step 3, the WebGL feasibility test, because the CPU-only render cost decides whether the 3D world is
practical on the Spark.
