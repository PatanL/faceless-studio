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
