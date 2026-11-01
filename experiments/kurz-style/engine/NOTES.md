# Lantern & Ink style engine: notes

A separate Remotion entry (`src/index.ts`) that implements `../STYLE_BIBLE.md` as reusable code, plus a 4 s showcase of the orca shot. Nothing in `studio/`, `pipeline/` or `experiments/polish-2d/` was touched, and nothing imports from them. The engine has its own `package.json` with the same Remotion 4.0.539 and the same encoder config as `studio/`.

**The short answer to the owner's question.** Code can match Kurzgesagt's detail. Everything they do in After Effects and Illustrator is masks, gradients, blend modes, blur, particles and springs, and all of that renders here. What we were missing was the craft layer. This engine adds that layer *procedurally*, so every asset gets it for free: you draw a flat shape, and the engine adds shadow, light, depth and motion from one light vector.

It does not reach Kurzgesagt tier yet. The gaps are listed below; they are art-direction gaps now, not technical ones.

## Proof

All images are in `proof/`. Full MP4s are in `~/Documents/faceless-studio/out/kurz-engine/` (Mac) and `~/studio/app/experiments/kurz-style/engine/out/` (Spark).

| file | what it shows |
|---|---|
| `proof/ladder.jpg` | The shading layer built up one layer at a time on one flat group (tiles 1–9), then the same group under 3 other light directions (tiles 10–12). Nothing is redrawn; only `light.key` changes. |
| `proof/assets.jpg` | The hero orca and diver at full size, shaded only by the engine. |
| `proof/show_f000.jpg`, `show_f060.jpg`, `show_f110.jpg` | Showcase frames at 0, 2 and 3.7 s. |
| `proof/showcase_sheet.jpg` | Showcase sampled every 0.5 s. |
| `proof/sbs_kit_vs_engine_t2s.jpg` | The current kit's orca pilot at 2 s (left) next to the engine showcase at 2 s (right). |
| `out/kurz-engine/showcase_tex.mp4` | The showcase after the texture pass. This is the deliverable clip. `showcase.mp4` is the raw render. |

## What was built

### 1. Procedural shading layer: `src/shade/Shaded.tsx`

`<Shaded parts={[{d, base}, …]} />` takes a flat drawing: one path, or a group of coloured parts. Parts with `clip: true` are decals, such as the orca's eye patch, belly and saddle, or the diver's stripe and straps.

From the scene light in context, it adds:

- **Cast shadow:** offset away from the key; shrinks and fades with `lift`.
- **Form gradient:** per part, centred toward the key, ΔL ≤ 0.06.
- **Core shadow:** a hard crescent computed as the silhouette minus the silhouette shifted toward the key.
- **Stipple terminator:** 3 sub-bands with 3 dot sizes from a seeded pattern tile, so dots never swim.
- **Deep occlusion and bounce.**
- **Highlight:** crescent or inset mode.
- **Glints:** explicit, or `autoGlint`, which follows the light.
- **Rim light:** in the opposite temperature.
- **Micro-marks:** dash clusters, pores, rings, rake scars and scale arcs. Marks on the shadow side take the shadow tone.
- **Inner glow:** stepped strokes, no filter.

Design points:

- **Group-aware shading.** There is ONE terminator for the whole group, and each part gets its own shadow colour. This is why the orca's white belly and black back share a shadow line instead of shading as separate blobs.
- **The light stays in screen space.** Objects pass their own rotation or mirror as `xf`, so a flipped diver and a pitched orca are lit from the same side (rubric J3).
- **Colour math.** All colours are OKLab mixes of palette tokens (`src/lib/color.ts`). `shadowOf()` guarantees a darker result even when the base is darker than the ambient; that case is the orca's skin.
- **Levels of detail.** `lod: hero | support | far` applies bible §4.3: support objects get L0/L1/L5/L7, and far objects get L0/L1.
- **No SVG filters.** Shading uses only masks, gradients and flat fills. Every clip is a luminance mask, because `<clipPath>` cannot hold `<g>`.

### 2. Depth and atmosphere: `src/depth/Planes.tsx`, `src/depth/Atmosphere.tsx`

**Planes.**

- `<CameraProvider cam>` plus N `<Plane>`s. Presets follow bible §6:
  - field 0.05
  - far 0.3, haze 0.62
  - mid 0.6, haze 0.32
  - subject 1.0
  - fore 1.45, haze 0.8 toward ink, blur 9 px
- Haze and desaturation are computed in colour math through a plane-tint context (`useTint()`). They cost nothing at render time, and the same `<Kelp>` comes out hazed on the far plane and as an ink silhouette on the foreground.
- Each plane also takes `fade` (opacity) and a plane-gap drop shadow.

**Atmosphere.**

- `GradientField`: a ≥ 3-stop gradient with a hue shift plus a radial lift.
- `SurfaceBand`.
- `Specks`: bean-shaped marine snow that drifts and twinkles.
- `Bokeh`: gradient discs; never hazed.
- `Bubbles`: ring plus highlight crescent, with wobble.
- `Rays`: wedges that sway on noise.
- `Caustics`: a packed net of rounded cells that morphs on noise.
- `Emitter`: hue-shifted body, a halo at R+0.08R / R+0.35R, rays and sparkles.
- `Bloom`, and `LightLayer`, which puts all screen-blended light into one layer per plane.

### 3. Texture pass: `scripts/bench.sh` (ffmpeg step)

The bible's rule is "keep grain out of Chrome", because in-Chrome grain costs +43–105 %. So texture is a post pass:

`deband=1thr=0.012:2thr=0.012:3thr=0.012:range=16:blur=1,noise=c0s=4:c0f=t+u`, then x264 CRF 18 with `aq-mode=3`.

- **Deband** smooths the 8-bit steps that the JPEG intermediates and x264 leave in the big dark gradients.
- **Dither** (light temporal luma noise) stops the final encode from re-banding.
- **Cost:** 1.0 s per second of video on 4 threads.
- **File size:** +40 % (2.6 → 3.7 MB for 4 s). The bible forbids paper and film-grain textures, so this pass is a dither only.

### 4. Motion library: `src/motion/motion.ts`

All functions are pure functions of time, so frames render out of order.

- **Tokens** from bible §9.2:
  - `ease.travel`, `ease.drift`, `ease.exit`
  - `SETTLE` spring (overshoot ≤ 7 %) and `POP` spring (10–25 %)
  - `springAt()`, plus `overshootPeak()` for checks
- **Anticipation and overshoot:** `anticipate()` is a 6–10 % counter-dip followed by a spring landing. It drives the diver's wave.
- **Secondary motion:**
  - `lagged()` for follow-through
  - `chain()` for segment sway with phase lag (kelp, anemone tentacles)
  - `squash()`
- **Ambient (always on):**
  - `breathe`, `bob`, `sway`
  - `blinkAt`: seeded 2–5 s intervals, never in sync between creatures
  - `twinkle`, `pulse` (lub-dub)
- **Camera:** `cameraAt()` combines eased moves, constant drift (zoom %/s and lateral px/s) and hand-held noise of ≤ 6 px and ≤ 0.5°. A `steady` parameter fades the hand-held noise out while a label is being read.
- **Light as an actor:** the showcase key sweeps 12° across the shot, and every terminator re-computes.

### 5. Hero assets: `src/assets/`

All assets are drawn fresh in the house style. Nothing is traced from or modelled on a Kurzgesagt or TIS asset.

- **`Orca.tsx`.** A male orca in side view with a tall dorsal fin.
  - Markings: eye patch, chin-to-belly white with the flank lobe rising behind the dorsal fin, and a tide-tinted saddle.
  - Details: mouth line, blowhole, crease lines, rake scars, pores, wet-sheen glints, and the house eye (bone ring, ochre iris, ink pupil, 2 glints, a lid, seeded blinks).
  - Motion: a travelling-wave vertical tail beat through `swimBend`; near and far pectorals that follow through 0.18 s behind the body wave; breathing.
  - `lod="far"` draws the silhouette only, used for the distant pod.
- **`Diver.tsx`.** Proportioned torso 0.6 m : legs 0.9 m : fins 0.55 m.
  - Gear: dusk wetsuit with a coral stripe, BCD with D-rings, amber tank with straps and valve, hose, gauge console, knife, mask glass with glints, and regulator.
  - Motion: a flutter kick from the hip, with knee, ankle and fin each lagging the one before; the wave gesture with anticipation, overshoot and a lagging hand; a regulator bubble stream.
- **`Ocean.tsx`.**
  - Swaying kelp with shaded blades and ring-motif gas bladders.
  - Shaded rocks with barnacle rings and a moss decal.
  - Seabed with ripples and pebbles, plus sand caustics.
  - Urchins, anemones, sea grass, shells and sea fans.
  - A fish school (26 fish with 2-tone shading and eye glints).
  - Translucent jellies (40–60 % fill, inner glow, glare band).
  - A far ridge with an arch.

`src/lib/type.tsx` holds the "lantern tag" label: a bone pill, a soft shadow, and a 3 px leader ending in a 2-tone ring. Its pop uses the POP spring.

## Render cost on the Spark CPU (`scripts/bench.sh`, `data/bench.tsv`)

**Setup.**

- 1080×1920, 30 fps, `--concurrency=4`, `--muted`, `nice -n 10`, swangle, `CUDA_VISIBLE_DEVICES=""`.
- Both projects render from pre-built bundles, under the shared render lock.
- Runs alternate engine / baseline so load drift hits both. Load averages were 4–13.
- **Baseline** = the current kit: `studio/` Storyboard with `episodes/explainer-orca/storyboard.json`, frames 0–119. This is the same orca shot, with captions, at the same settings.

| | 4 s clip, wall | per second of video (incl. ~2 s browser start) | **marginal per second of video** (from the 2 s vs 4 s runs) | 60 s Short, projected |
|---|---|---|---|---|
| current kit (orca pilot) | 4.8 s | 1.2 s/s | **0.85 s/s** | ~55 s |
| engine showcase, first version | 30.4 s | 7.6 s/s | ~7.0 s/s | ~7 min |
| **engine showcase, optimised (final)** | **15.8 s** | **3.9 s/s** | **3.4 s/s** | **~3.5 min** |
| texture pass (ffmpeg, 4 threads) | 4.0 s | 1.0 s/s | 1.0 s/s | ~1 min |

The engine costs **about 4× the current kit per second of video**. That is affordable: a Short is about 3.5 min of render plus 1 min of texture pass.

**Where the cost went** (`scripts/profile.sh`, `data/profile.tsv`; 60 frames with one system switched off at a time):

- **First version: 16.4 s per 60 frames.**
  - Plane-gap drop shadows on 3 oversized planes: −5 s.
  - The shading layer: −6 s. Its masks were rasterised over a box padded by half the object's size.
  - Foreground blur: −2 s.
  - Stipple, caustics and the screen blend were within load noise.
- **Two fixes: 9.1 s per 60 frames (−45 %), with no visible change.**
  - **Tight mask boxes.** The pad is now the largest layer shift plus 24 px; `maskBox` covers fins outside the body box.
  - **Leaner planes.** The plane-gap shadow is on the subject plane only (none on mid or fore), and the overscan dropped from 260 to 160 px.
- **The shading layer now costs about 2 s per 60 frames** (9.1 s with it, 7.2 s with it off).

## Frame metrics vs the current kit (`scripts/frame_judge.sh`, `data/frame_metrics_*.json`)

Frames were sampled every 0.5 s, so a 4 s clip gives 8 frames. The bible's 2 s grid would give only 2. Targets are from STYLE_BIBLE §13.

| id | metric | target | kit orca (0–4 s) | **engine showcase (textured)** |
|---|---|---|---|---|
| P1 | palette conformance | ≥ 0.85 | 0.996 | **1.00** |
| P2 | violet/magenta share | ≤ 0.08 | 0 | **0** |
| P3 | chromatic saturation | 0.66–0.88 | 0.665 | **0.77** |
| P4 | grey mid-tones | ≤ 0.04 | 0.029 | 0.046 (raw 0.054) **FAIL** |
| P5 | hue families per frame | ≥ 3 | 1 | 2 **FAIL** |
| P6 / P7 | near-white / pure white | ≤ 0.015 / ≤ 0.003 | 0.024 / 0.0043 (fail) | **0.0035 / 0** |
| D1 | shapes per frame | ≥ 110 | 139 | **186** |
| D2 | micro-details | ≥ 600 | 816 | **1866** |
| D3 | small specks | ≥ 120 | 85 (fail) | **266** |
| D4 | edge density | 0.040–0.08 | 0.033 (fail) | **0.061** |
| D5 | outline response | ≤ 0.05 | 0.107 (fail) | **0.020** |

**Reading the table.**

- **Kurzgesagt-tier measures pass.** The engine passes every metric that separates Kurzgesagt from our pilot: specks, edges and outline response. Detail density more than doubled, and the outline look is gone.
- **What still fails** is colour breadth:
  - P5: still 2 hue families per frame. The frame is teal plus ochre; coral and kelp stay under 3 % each.
  - P4: grey. The haze on the mid plane greys the sea fans, and the shadowed white belly reads as grey.

## Honest gap to Kurzgesagt tier

This has not been scored side by side with `JUDGE_RUBRIC.md`. My read is that it is clearly above the current kit and about TIS tier on craft, but not yet at the target. The systems are in place; the remaining work is art direction:

1. **The hero is still simple.**
   - The orca is about 6 parts. A Kurzgesagt hero has 15–40, with secondary forms such as jaw, melon, the lift of the flipper root, and fluke ridges.
   - At showcase size the diver is about 250 px and reads as a pictogram.
   - Next: more sub-forms per hero, and framing that gives the hero 30–60 % of the frame width (bible J8).
2. **Colour script.** Add a warm subject mass (coral reef shelf, a sunlit sand bank) to reach P5 ≥ 3. Lower `desat` and haze on warm mid-plane objects.
3. **Environment design.**
   - The ridges are noise blobs.
   - The sea fans read as bare trees.
   - The caustic net reads as a pattern on the sand.
   - Next: hand-designed silhouettes for P1 and P2, and gentler, smaller caustics.
4. **Light events.** A 12° key sweep is too subtle to notice. The lit/unlit pass (bible §5.2) is not built yet, and it is the biggest "wow" lever for deep-sea beats.
5. **Not built yet:** the transition library (bible §9.6), `DepthGauge`, and audio. This lane was graphics only.

## Run it

```bash
# sync (Mac -> Spark), then everything runs on the Spark
rsync -a --exclude node_modules --exclude out --exclude build \
  ~/Documents/faceless-studio/experiments/kurz-style/engine \
  ~/Documents/faceless-studio/experiments/kurz-style/house \
  dgx-spark:~/studio/app/experiments/kurz-style/
ssh dgx-spark 'cd ~/studio/app/experiments/kurz-style/engine && npm install && npx tsc --noEmit'
ssh dgx-spark 'bash ~/studio/app/experiments/kurz-style/engine/scripts/stills.sh 0 60'   # ladder, assets, showcase frames
ssh dgx-spark 'bash ~/studio/app/experiments/kurz-style/engine/scripts/bench.sh'         # showcase + baseline timing + texture pass
ssh dgx-spark 'VARIANTS="none gap shade" bash ~/studio/app/experiments/kurz-style/engine/scripts/profile.sh'
ssh dgx-spark 'cd ~/studio/app/experiments/kurz-style/engine && bash scripts/frame_judge.sh out/showcase_tex.mp4 out/judge_x x'
```

## Adopting into `studio/` (later, when the owner says so)

- **Copy as-is:** `lib/color.ts`, `lib/light.tsx` and `shade/Shaded.tsx` have no dependencies beyond `remotion` and the palette JSON.
- **The kit's Figures:** wrap their flat parts in `<Shaded>`.
- **Planes:** map onto `core/layers.tsx` depth.
- **Ease tokens:** move into `core/anim.ts`, as bible §9.2 already suggests.
- **Texture pass:** add it as a pipeline post step after the render.

## Orca pilot 0–9.73 s rebuild (`src/scenes/OrcaOpen.tsx`, composition `OrcaOpen`)

The first two storyboard scenes (p00 and p01), timed to the episode's word timings. The episode's own `mix.wav` is muxed in, trimmed to 9.733 s. It is one continuous set with no hard cuts: there is a pull-back reveal, a push-in on the head where the jaw opens on teeth and the diver flinches with a bubble burst, a lit/unlit light event leading into the scale board (8 m bar with a ticking counter, four cars dropping onto a platform that dips under each one, a "≈ 6 tonnes" counter), then a push up to the dorsal fin, where the YOU figure stands next to it with equal-height guides.

New assets: `assets/Reef.tsx` (brain, tube, table, staghorn and fan corals, spires, shelf), `assets/Car.tsx`, `assets/YouFigure.tsx`, the orca jaw rig with teeth and its secondary forms (`detail`), `lib/titles.tsx` (title plate, counters, captions, unlit pass), and per-part shadow targets in `Shaded` (`ambient`).

Scripts: `scripts/orca_open_render.sh <tag>` (render, texture pass and audio mux), `scripts/orca_open_stills.sh`, and `scripts/orca_open_sheet.py` (side-by-side sheet).

**Iterations** (metrics: `data/frame_metrics_orca_open_v*.json`; timing: `data/orca_open_bench.tsv`)

| | P4 grey | P5 hue families | D5 outline | render on the Spark CPU |
|---|---|---|---|---|
| v1 | 0.037 | **2 (fail)** | **0.084 (fail)** | 38.5 s |
| v2: higher-key water ramp, the light event lifts instead of sinking to ink, reef raised, tighter B/C framing, no ink under-strokes, slimmer rim, redundant B title plate dropped | **0.054** | **2** | 0.043 | 41.6 s |
| v3: mid-plane haze no longer greys the warm masses, lantern-warm belly with tide shadows, warm jellies in the upper frame | **0.050** | 3 | 0.042 | 41.9 s |

**Known gaps in v3.**
- P4 is 0.11–0.14 on the scale-board frames (5–7.5 s). The olive seabed sits under the ink pass and reads as grey.
- The YOU tag touches the caption at about 1 s (J9).
- Above the scale board the upper half of the frame is still mostly empty water.
- Hero construction and mark density are still short of the KB references at 2×.

My own read is about 60/100 on the rubric, which is TIS tier and not yet Kurzgesagt tier.

## Judge

Strict pass with `../JUDGE_RUBRIC.md`, 2026-11-01. I judged by looking at frames: the full-res frames at 0, 2, 3.5, 5, 6.5, 8 and 9.6 s from both clips, 0.25 s motion strips (2.0–4.0 s and 6.75–8.75 s), a 2× crop of the hero head next to `refs/kurz-bio/stills/D_0630_dumbo-octopus.jpg`, and `D_0126_reef.jpg`, `W_0222_whale.jpg` and `W_0000_tumor-creature.jpg` as the target tier.
- **Rebuild:** `out/kurz-engine/orca_open_v3.mp4`.
- **Current:** `out/pilots/explainer-orca/explainer-orca_9x16.mp4`, 0–10 s.
- **Palette and detail metrics:** P and D come from `data/frame_metrics_orca_open_v3.json`.
- **Not run:** `judge_metrics.sh` and `motion_pair.sh` were not run on the Spark. So the M1–M5 and A1–A3 caps are unverified, and the motion score is a judgement from the strips.
- **Loudness:** checked locally, −14.1 LUFS integrated.
- **Cuts:** the scene-cut detector (threshold 0.3) found 0 hard cuts.

### Scores

| category | max | rebuild | current (0–10 s) | why (rebuild) |
|---|---|---|---|---|
| 2.1 illustration | 20 | **12** | 2 | The orca has the full stack: core shadow, stipple, highlight, glints, rim and marks. At 2× the construction is still simple. The head is a blunt bullet with no melon or jaw mass, and the rim reads as a cyan outline on the flipper and belly. The YOU figure is a white stick pictogram. |
| 2.2 lighting | 12 | **8** | 3 | There is one key from the upper left, and rays and glints agree. The lit/unlit event at about 5 s can't be read at phone size, and there is no dark beat. |
| 2.3 depth | 12 | **8** | 2 | There are 4 or more planes: far pod, mid kelp and ridges, subject, and blurred foreground. Parallax shows on every move. But 5–10 s has no foreground, and the upper 40 % of the frame is empty water. The foreground ink blobs read as smudges, not as kelp. |
| 2.4 colour | 10 | **5** | 2 | Capped at 6 because P4 is 0.050 (0.11–0.14 on the scale frames: the olive seabed reads as grey). One teal key runs all 10 s with no colour script. The warm masses are small and dull next to the saturated families in D_0126. |
| 2.5 detail | 10 | **6** | 2 | D1–D5 pass (190 shapes, 1834 micro, 285 specks, edge density 0.070, outline 0.042). The micro layer is stamped: every kelp leaf is the same with a ring node, every jelly has the same 3-dot bell, and the fish are identical. |
| 2.6 motion | 14 | **8** | 4 | Present: tail wave, flutter kick, follow-through, a ticking counter, platform dip and a bubble burst. Defects: 2.25–3.0 s is a near-frozen hold, the push to the head at about 3.1 s is abrupt, and at 6.75–7.0 s the cars fall through the orca's body and flipper. |
| 2.7 camera | 8 | **5** | 3 | The set is continuous with no hard cuts, and there are pull-back, push-in and push-up moves. Only one transition kind is used (camera moves); the transition library is not built. |
| 2.8 type | 6 | **4** | 3 | Strong: the Anton plate, lantern tags, ring leaders, the 2.8 → 6 tonnes counter and YOU on the scale beat. Collisions: the YOU tag touches the caption at about 1 s; the platform and cars slide under the caption "AND ITS FIN ALONE" at about 7.75 s; the "8" is clipped by the platform at 6.5 s; and the YOU leader ring lands on the figure's face as a red dot. |
| 2.9 sound | 8 | **3** | 3 | The old `mix.wav` is muxed in as is: voice plus bed, loudness on target. There is no SFX on the bubble burst, car drops, counter ticks or light event. |
| **total** | 100 | **59** | **24** | |

**Identity gate (rebuild): PASS.**
- P1 is 1.00 and P2 is 0.
- No borrowed designs: no birds or beans, no isometric cube floor.
- Titles use Anton on an ink plate; no wide-tracked caps.
- All 5 of 5 house signatures are present: stipple, teal-ink darks, plane-gap, ring motif and YOU.

**Tier gaps.** Gap 2 = clearly below the target, TIS-like.

| role | rebuild time | reference | tier gap |
|---|---|---|---|
| H | 1.0 s | W_0000 | 2 |
| P | 6.5 s | W_0222 | 1 |
| E | 0 s | D_0126 | 2 |
| X | 3.5 s | D_0630 | 2 |

**Tier: TIS tier (59), not Kurzgesagt. Not near tier either.** The rebuild is clearly better than the current pipeline (24, below TIS, matching the ≈25 calibration). It beats TIS on shading, palette discipline and information design. It loses to Kurzgesagt on drawing, colour and set design: side by side, Kurzgesagt reads as illustrated and ours reads as assembled.

**Does code limit it? No.** None of the defects is a renderer limit. They are drawing and art-direction limits.

### Top 5 remaining gaps (ranked by visual impact)

1. **Hero drawing quality at 2×.** This needs better art assets.
   - Problems: the orca head is a blunt bullet with no melon, rostrum or jaw mass; the rim reads as an outline; the YOU figure is a stick pictogram; the diver is a small pictogram.
   - The engine's shading is not the bottleneck; the path drawing is.
   - Fix: hand-drawn hero SVGs from an illustrator (human or commissioned/licensed vector sources in our own style), dropped into `<Shaded>`. Code renders them at full quality, but agent-authored paths have plateaued at this level.
2. **Colour script and value range.** Closable in code.
   - One teal key for all 10 s.
   - The grey olive seabed fails P4.
   - The warm masses are small and dull.
   - Fix: re-key the seabed and lift the chroma of the reef shelf to a ≥ 4-family saturated mass. Shift the key at the scale beat, for example warmer and brighter for "proof". Give the light event a real value swing.
3. **Repetitive, stamped set dressing and empty upper frame.** Mostly closable in code; bespoke silhouettes would benefit from art.
   - Identical kelp leaves with a ring node on every leaf, identical jellies, identical fish.
   - Noise-blob ridges.
   - The upper 40 % is empty from 5 to 10 s.
   - Fix: seeded variation in leaf shape and size, nodes on only some leaves, 3–4 jelly designs, surface light or a pod passing overhead to fill the upper frame.
4. **Staging and acting defects.** Closable in code.
   - A near-frozen hold at 2.25–3.0 s, and an abrupt push at about 3.1 s.
   - Cars fall through the orca at 6.75–7.0 s.
   - Caption collisions at about 1 s and 7.75 s, and the clipped "8" at 6.5 s.
   - Fix: block the car drop clear of the hero, keep camera drift through the hold, ease the push, and run a collision check for text boxes against moving props.
5. **Light events and sound.** Light is closable in code; sound needs a licensed or CC0 SFX library, not visual art.
   - The lit/unlit beat cannot be read at phone size.
   - There is no transition library.
   - There are no SFX on the bubble burst, car drops, counter ticks or light event.

```json
{
  "video": "out/kurz-engine/orca_open_v3.mp4",
  "judge_date": "2026-11-01",
  "metrics_file": "experiments/kurz-style/engine/data/frame_metrics_orca_open_v3.json",
  "sheet": "out/kurz-engine/orca_open_sbs.jpg",
  "motion_strips": [],
  "scores": {"illustration": 12, "lighting": 8, "depth": 8, "colour": 5, "detail": 6,
             "motion": 8, "camera": 5, "type": 4, "sound": 3},
  "caps_applied": ["2.4 <= 6 (P4 0.050 > 0.04)", "M1-M5 / A1-A3 caps unverified (judge_metrics.sh not run)"],
  "total": 59,
  "current_pipeline_total": 24,
  "pairs": [
    {"role": "H", "ours_t": "0:01", "ref": "kurz-bio/stills/W_0000_tumor-creature.jpg", "tier_gap": 2,
     "defects": [{"t": "0:01", "bible": "§11", "note": "YOU tag touches caption"},
                 {"t": "0:01", "bible": "§6", "note": "foreground ink blobs read as smudges"}]},
    {"role": "X", "ours_t": "0:03.5", "ref": "kurz-bio/stills/D_0630_dumbo-octopus.jpg", "tier_gap": 2,
     "defects": [{"t": "0:03.5", "bible": "§4", "note": "bullet head, few sub-forms, rim reads as outline"},
                 {"t": "0:02.3-0:03.0", "bible": "§9.3", "note": "near-frozen hold, then abrupt push-in"}]},
    {"role": "E", "ours_t": "0:00", "ref": "kurz-bio/stills/D_0126_reef.jpg", "tier_gap": 2,
     "defects": [{"t": "0:00", "bible": "§2.5", "note": "single teal key, warm masses dull, low hue breadth"},
                 {"t": "0:00-0:10", "bible": "§8", "note": "stamped kelp, jellies, fish"}]},
    {"role": "P", "ours_t": "0:06.5", "ref": "kurz-bio/stills/W_0222_whale.jpg", "tier_gap": 1,
     "defects": [{"t": "0:06.5", "bible": "§11", "note": "'8' clipped by platform; upper 40% empty"},
                 {"t": "0:06.8-0:07.0", "bible": "§9.2", "note": "cars fall through orca body"},
                 {"t": "0:07.75", "bible": "§11", "note": "platform and cars slide under caption"}]}
  ],
  "identity_gate": {"P1": 1.0, "P2": 0.0, "no_borrowed_designs": true, "type_signatures_absent": true,
                    "house_signatures_seen": 5, "no_tracing": true, "pass": true},
  "tier": "TIS",
  "top_fixes": [
    "§4: illustrator-drawn hero SVGs (orca head/jaw/melon, real YOU figure, larger diver) fed into <Shaded> - needs art assets",
    "§2.5/P4: re-key seabed and reef to a saturated >=4-family warm mass; shift key per beat - code",
    "§8/§6: seeded variation on kelp/jellies/fish and fill the empty upper frame; fix staging collisions - code"
  ]
}
```
