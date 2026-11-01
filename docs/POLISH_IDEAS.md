# Polish ideas: taking our flat-2D Remotion explainers to the Kurzgesagt tier

Status: research for Test 1 ("Remotion's official skills plus motion-explainer's polish ideas in our 2D
pipeline"), 2026-11-01. Nothing here has been wired into the live pipeline yet. `studio/src`, `pipeline/` and
`scripts/` are unchanged. Every technique is described as a code change to our kit (`studio/src/core/*`,
`studio/src/kits/explainer/*`) for a later, targeted adoption pass, and each has a render cost measured on the Spark.

## Sources and tags

| Tag | Source | What it is |
|---|---|---|
| **[RS]** | Remotion's official agent skills, `remotion-dev/skills` @ `30d4553` (v4.0.539, the same as our pinned `remotion`). Installed project-scoped in `.claude/skills/`; the full set is in `experiments/vendor/remotion-skills/` | API-level guidance: `interpolate` and easing, `@remotion/effects`, `<HtmlInCanvas>`, motion blur, light leaks, transitions, SFX |
| **[ME]** | `Marwanenoudouar10/motion-explainer` @ `b0ec17d` (MIT), cloned read-only into `experiments/vendor/motion-explainer/`. None of its scripts were run | Rules and lessons from a 17-chapter AI-built explainer, a starter template (`src/lib/camera.tsx`, `ease.ts`, `smooth.ts`, `focusPull.tsx`, `overlays/Grain.tsx`) and QA probes |
| **[BENCH]** | Our render-cost bench, `experiments/polish-bench/` | One Remotion composition per technique, timed on the Spark |
| **[OURS]** | This studio's own proposal | Where neither source covers the point |

What each source is good for:
- **[RS] is mostly API surface.** It covers how to call things: `Easing.spring`, `output: 'perceptual-scale'`, the `effects` prop, `createEffect`, `HtmlInCanvas`, `TransitionSeries.Overlay`. It says nothing about render cost on a CPU box, or about what makes a frame look good.
- **[ME] is craft and QA.** Its most useful parts are the measured rules: no pops over 20/255, caption band contrast at least 4.5:1, a builder followed by an independent polish pass (+1.8/10), same-hue shading, at most 5 full-frame blur layers, and SFX body at 120-600 Hz.

How the two sources were brought in:
- **Remotion skills.** Five are installed in `.claude/skills/`, copied verbatim from the pinned clone: `remotion-markup`, `-captions`, `-render`, `-docs` and `-multimedia`. `.claude/skills/README.md` says why this was done instead of `npx skills add remotion-dev/skills` (no npm on the Mac, CLI telemetry).
- **Remotion skills left out.** `remotion-best-practices` and `remotion-studio` tell agents to open Studio in a browser, and `remotion-upgrade` would bump our pinned version. Both conflict with BRIEF.md.
- **motion-explainer.** It stays read-only under `experiments/vendor/`. Its README suggests cloning it into `~/.claude/skills`, which we did not do.

## How the costs were measured [BENCH]

- **Scene.** A flat-2D scene in `experiments/polish-bench/src/scene.tsx`: sky gradient, three noise ridges, a round character with a spring jump, squash/stretch, breathing and blinks, 9 swaying foreground plants, a camera push plus drift, and a caption line.
- **Compositions.** Each composition in `src/Root.tsx` is this scene plus one technique.
- **Render settings.** 1080x1920, 30 fps, 450 frames (15 s). Spark CPU: `--concurrency=2`, `nice -n 10`, swangle (software GL), `CUDA_VISIBLE_DEVICES=""`, under `~/studio/locks/render.lock`. Same encoder settings as `studio/remotion.config.ts`.
- **Load control.** The box is shared, and its load average swung between 13 and 64 across four passes. `Base` was re-rendered between compositions: every 4-5 in pass 2, every other one in passes 3-4. The cost below is the ratio to the mean of the two `Base` runs on either side (`experiments/polish-bench/summarize.py`).
- **Noise.** On a calm box the bracketing `Base` runs agreed within about ±5%, so a calm ratio under about 1.10 means "≈ free". Under load, ratios scattered by ±25%.
- **Baseline.** `Base` took 16-18 s (calm) to 23-28 s (loaded) per 15 s of video at concurrency 2: 1.1-1.9 s of render per second of video. Production renders run at concurrency 2-4 (`pipeline/ops/config.default.json`, `scripts/spark_render.sh`). So "+50%" adds roughly 30-55 s to a 60 s Short at concurrency 2.
- **Pass 1** (150 frames) was dropped: Chrome start-up of about 4-5 s swamped the differences. Its numbers stay in `results/results_run1_150f.tsv`.
- **Raw data.** Times are in `experiments/polish-bench/results/` (copied from the Spark): `results_run{2,3,4}_450f.tsv`, `postgrain.tsv` and `filesizes_MB.tsv`. The contact sheet of every variant at t = 7.5 s is `out/polish-bench/sheet.jpg`.
- **Reproduce.** On the Spark: `bash experiments/polish-bench/bench.sh [Comp ...]`. It bundles once, takes the render lock, and appends to `out/results.tsv`.

### Cost table

Each cost is the render time relative to the flat `Base` scene. "Calm" is passes 3-4, at a load average of 13-39. "Loaded" is pass 2, at a load of 27-64, close to what the box looked like during the pilots. File size is the 15 s H.264 at CRF 18 (`Base` = 0.9 MB).

| Technique | Composition | Calm | Loaded | File (MB) | Verdict |
|---|---|---|---|---|---|
| 5 parallax planes (vs 1) | `Parallax5` | 1.01 | 0.94 | 0.9 | free |
| Depth of field, CSS `blur()` on 3 planes | `DofCss` | 1.22 | 1.00 | 0.9 | cheap |
| Depth of field, SVG `feGaussianBlur` on the same planes | `DofSvg` | 1.70 | 1.54 | 1.1 | avoid; use CSS blur |
| Rim light (clipped offset stroke) + radial-gradient halo | `RimGlowGradient` | 1.06 | 1.13 | 1.3 | ≈ free |
| Glow: one SVG blur+merge filter on the subject group | `GlowSvgFilter` | 1.17 | 0.95 | 0.7 | cheap |
| Glow: CSS `drop-shadow(0 0 40px)` | `GlowCssDropShadow` | 1.00 | 0.77 | 0.8 | free |
| Glow: `<HtmlInCanvas effects={[glow()]}>` ([RS] effects) | `GlowEffectHtmlInCanvas` | n/a | **10.65** | 0.7 | do not use |
| Contact shadow, radial-gradient ellipse | `ShadowGradient` | 0.99 | 0.73 | 0.9 | free |
| Contact shadow, `feGaussianBlur` ellipse | `ShadowBlurFilter` | 0.99 | 1.11 | 0.9 | free |
| 6 light rays, gradient polygons, screen blend | `Rays` | 1.02 | 1.28 | 3.9 | cheap; the cost appears under load |
| Grain: full-frame `feTurbulence`, overlay (what `Episode.tsx` does today) | `GrainTurbulence` | **1.43** | **2.05** | 2.6 | expensive |
| Grain: tiled 512 px noise PNG, shifting, overlay | `GrainTile` | 1.15 | 1.71 | **27.4** | cheap in Chrome, heavy file |
| Grain: `noise()` from `@remotion/effects` on a `<Solid>` (WebGL/swangle) | `GrainEffect` | 1.60 | 3.01 | **117.6** | avoid |
| Grain added in ffmpeg after the render (`noise=c0s=7:c0f=t+u`, 4 threads) | `postgrain.sh` | +4.7 s per 15 s (6.6 s vs a 1.9 s plain re-encode) ≈ +29% of a calm Base | n/a | 33.9 | no cheaper than the tile; same file problem |
| 150 particles, one SVG, no filters | `Particles150` | 1.00 | 1.01 | 2.6 | free |
| 40 bokeh circles, radial-gradient fill, screen | `Bokeh40Gradient` | 1.09 | 1.12 | 1.5 | ≈ free |
| 40 bokeh circles, CSS `blur(10px)` each | `Bokeh40CssBlur` | 1.46 | 1.82 | 1.6 | avoid |
| Caustics: 2 live `feTurbulence` layers, screen | `CausticsTurbulence` | 1.63 | 1.89 | 2.4 | hero shots only |
| Caustics: 2 scrolling copies of a pre-rendered tile, screen | `CausticsTile` | 1.23 | 1.20 | **41.9** | cheap in Chrome; the tile was too fine (see 6b) |
| Light leak, `lightLeak()` on a `<Solid>`, on screen the whole 15 s ([RS] light-leaks) | `LightLeakEffect` | 1.65 | 1.66 | 3.0 | fine for about 20 frames at a cut |
| CSS grade `brightness contrast saturate` on the whole world (what `SceneView` does) | `GradeCssFilter` | 1.02 | 1.03 | 1.0 | free |
| Vignette, full-frame radial gradient | `VignetteGradient` | 0.99 | 0.93 | 1.0 | free |
| Motion blur, `<HtmlInCanvasMotionBlur samples=6>` ([RS] motion-blur) | `MotionBlurCreature`, `MotionBlurPlainChild` | **fails** | **fails** | n/a | "captureElementImage: No cached paint record for element" in headless Chrome |
| **Everything at once**: 5 planes, DoF, rim, halo, shadow, rays, 40 bokeh, 80 particles, vignette, tiled grain | `KurzStack` | **1.68** | 1.55 | 29.3 | |
| **Everything except grain** | `KurzStackNoGrain` | **1.29** | n/a | 5.0 | the realistic target |

What the table says:
1. **Depth and light are close to free; texture and filters are not.**
   - These cost within about 20% of the flat scene: five parallax planes, CSS-blur depth of field, rim plus halo, contact shadows, 150 particles, gradient bokeh, rays, a vignette and a CSS grade.
   - The full Kurzgesagt-style stack without grain is **+29%** (`KurzStackNoGrain`). On a calm box that is about 15 s more per 60 s Short at concurrency 2.
2. **Two kinds of blur are expensive: blur through an SVG filter, and blur on many small elements.**
   - CSS `filter: blur()` on a whole plane is cheap (+0-22%).
   - The same blur through SVG `feGaussianBlur` is +54-70%.
   - 40 bokeh circles that each carry `filter: blur()` cost +46-82%. Radial-gradient circles that look the same cost +9-12%.
   - [ME] P4 reached the same rule from crashes and slowdowns: "≤ 5 full-frame blur layers, one filter per group, radial gradients for glow".
3. **Grain is the most expensive common polish, in render time and in bytes.**
   - The `feTurbulence` grain that `Episode.tsx` draws today costs +43% calm and +105% loaded.
   - A tiled PNG costs +15%, but any per-pixel temporal grain makes the file 3-30x bigger at CRF 18. Platforms then re-encode it into mush.
   - Moving grain to an ffmpeg pass is not cheaper (+29%).
   - See 3a for what to do instead.
4. **Load amplifies every full-frame blend and filter.** Rays went from +2% (calm) to +28% (loaded). The tiled grain went from +15% to +71%. Budget with the loaded column while renders share the box with the other workload.
5. **`@remotion/effects` on DOM content is not viable on this box.** [RS] effects.md and html-in-canvas.md describe applying effects to DOM content by wrapping it in `<HtmlInCanvas>` and passing an `effects` array.
   - `glow()` on the character this way rendered correctly but cost **10.7x**.
   - `<HtmlInCanvasMotionBlur>` failed outright in the headless render, both with a transformed wrapper and with a plain child.
   - Effects on a canvas-native `<Solid>` work at moderate cost (light leak +65%). Use them only on the few frames where they matter, such as a light leak over a cut.
6. **The bench frames are cost proxies, not look-dev.** The caustic and grain variants are deliberately strong, and the light leak covers the whole 15 s. Tune looks on real scenes. The contact sheet is `out/polish-bench/sheet.jpg`, and a full-resolution still of the no-grain stack is `out/polish-bench/kurzstack_nograin_f225.jpg`.

---

## 1. Lighting

The Kurzgesagt look is a dark, saturated world lit by a few warm sources. The subject has a bright rim on the side facing the light, a soft halo, and a soft contact shadow. Shafts of light cross the frame with a screen blend.

### 1a. Rim light: ≈ free [BENCH: RimGlowGradient]
- **How.** Draw a copy of the silhouette stroke, shifted AWAY from the light by about 5% of the body size, clipped to the body (`clipPath` = the body shape). Only the band along the lit edge stays inside the clip. In the bench (`scene.tsx`, `Creature rim`) it is one `<circle stroke>` with a 22 px width inside `clipPath="url(#cr-clip)"`, translated (+10, +14) for a key light at the upper left.
  - The first bench pass had the sign backwards: the rim landed on the shadow side. It was caught on the contact sheet and fixed. Check the side on a still every time.
- **In our kit [OURS].** Give every figure in `kits/explainer/creature.tsx` and `marine.tsx` a `rim?: {color, width, angle}` prop.
  - The figure already owns its path, so the rim is `<g clipPath={bodyClip}><path d={body} stroke={rim.color} strokeWidth={rim.width} transform={offset(angle)} fill="none"/></g>`.
  - Derive the angle from one scene-level `light` direction (add `scene.light = {angle, color}` to `schema.ts`). Every figure in the shot is then lit from the same side, which keeps [ME] L1 ("one light direction for the whole film") and FEEDBACK A3 (consistency).
- **Colour rule [ME] L1-L3.** The rim is a lighter tone of the body's own hue, or the light's warm colour. Never screen a colour onto itself, because red on red turns pink. Sample the hero's pixels after any lighting change: olive, khaki or grey means the blend is wrong.

### 1b. Glow and halo: ≈ free as a gradient, 10.7x through `@remotion/effects` [BENCH: RimGlowGradient, GlowSvgFilter, GlowCssDropShadow, GlowEffectHtmlInCanvas]
- **Cheapest.** A `radialGradient` circle behind the subject (stops at 0.65, 0.18 and 0 alpha) with `mix-blend-mode: screen`. In our kit it can be a new layer field, `glow: {color, radius, strength}`, that `LayerView` renders as a sibling `<div>` with `background: radial-gradient(...)` before the body. Draw the focal shape after its glow, with a smaller flare, so the colour stays saturated ([ME] L4).
- **One SVG filter per group is also fine.** `feGaussianBlur stdDeviation=28` plus `feMerge` on the character group cost +17% calm and nothing measurable under load. So was CSS `drop-shadow(0 0 40px)`, which our `layer.shadow` already supports.
- **Don't.** Avoid `HtmlInCanvas` + `glow()` from `@remotion/effects` ([RS] effects.md): it cost 10.7x. Avoid a filter on each of hundreds of nodes ([ME] remotion-patterns "SVG, colour and performance").
- **Pulse it.** [ME] `ease.ts` `pulse(frame, bpm)` gives a deterministic lub-dub from 0 to 1. Drive the glow's strength with it for a "living" light such as a lure, a heart or a reactor.

### 1c. Cast and contact shadows: ≈ free [BENCH: ShadowGradient, ShadowBlurFilter]
- **How.** A flattened ellipse under the subject with a radial-gradient fill (alpha 0.7 → 0), drawn in the ground's plane. Its size and opacity shrink as the subject rises: `s = 1 - 0.45 * lift`. That one line sells a jump better than any trail. An `feGaussianBlur` ellipse costs the same.
- **In our kit [OURS].** Add a `shadow: {ground: y, spread}` prop to figures, or a generic `fx/ContactShadow` component that takes the subject's layer id and reads its sampled y. Kurzgesagt-style shadows are a darker tone of the ground's hue, never black or grey ([ME] L1).
- **Long cast shadows.** For a low sun, use a skewed silhouette copy (`transform: skewX(-40deg) scaleY(0.4)`) filled with the ground's dark tone at 40% alpha. [RS] lists `longShadows()` and `dropShadow()` in `@remotion/effects`, but they run on a canvas and carry the `HtmlInCanvas` cost above.

### 1d. Light rays (god rays) with blend modes: +2% calm, +28% loaded [BENCH: Rays]
- **How.** 6 trapezoid `<polygon>`s with a vertical `linearGradient` (alpha 0.45 → 0), in a full-frame SVG with `mix-blend-mode: screen`. Each one's opacity breathes on its own phase: `0.55 + 0.45 * sin(f/40 + i*1.7)`. Its x sways slowly.
- **In our kit.** `explainer/Ocean` already draws rays. Give them a screen blend, an independent opacity per ray from `noise1` (`anim.ts`), and fade the rays to 0 above the caption band ([ME] S3: "effects fade to 0 by y 1290").
- **Watch the caption band.** In `out/polish-bench/kurzstack_nograin_f225.jpg` the rays cross the captions. That breaks [ME] S1/S3 and FEEDBACK B8. Mask the ray layer with `mask-image: linear-gradient(black 0 62%, transparent 68%)`.
- **Cost.** It comes from the full-frame screen-blended layer, not the polygons: +2% calm, +28% loaded. Merge rays, dust and glow into ONE screen-blended SVG per scene instead of three separate full-frame blended layers.
- **Light leaks over a cut** ([RS] light-leaks.md + transitions.md): `<Solid effects={[lightLeak({seed, progress})]}>` in a screen-blended div. It costs +65% while on screen. Over a 20-frame transition that is about +0.5 s per cut. It needs `@remotion/effects` added to `studio/package.json`; per [RS] markup, add it with `npx remotion add`, on the Spark.

## 2. Depth

### 2a. 3-5 parallax planes: free [BENCH: Parallax5 vs Base]
- **What the bench showed.** Five separate composited planes (sky+far 0.3, mid 0.55, near 0.8, subject 1.0, foreground 1.4) rendered as fast as the same art in one plane.
- **We already have the machinery.** `layer.depth` plus `planeTransform()` in `core/camera.ts`, and `background.depth`. What is missing is convention and content:
  - **Depth presets [OURS].** Add named presets to `schema.ts` so storyboard writers don't invent numbers: `sky: 0.05, far: 0.3, mid: 0.55, subject: 1, fg: 1.4`.
  - **Always a foreground plane.** Almost every Kurzgesagt wide shot has dark foreground silhouettes (plants, rocks, debris) moving faster than the subject. Add `fg` components to the kit (kelp, rocks, coral, girders) that are meant to sit at depth 1.3-1.6, partly out of frame.
  - **Camera moves must be lateral as well as zoom.** A pure push-in barely separates the planes. The bench camera pans 120 px over the shot. Our `drift` preset does this; `pushIn` alone does not.
- **[ME] `camera.tsx` adds two things we lack:**
  - **Hand-held drift.** `drift * noise2D(seed, f*0.01) * 6px` plus 0.5° of roll. It is turned off (`drift={0}`) while a chart or label is being read ([ME] M5).
  - **`worldToScreen(cam, point, depth)`.** It checks that the subject at the camera's maximum zoom stays clear of the caption band. Port both into `core/camera.ts` as `shakeAt`-style pure functions.

### 2b. Depth of field: +0-22% as CSS blur, +54-70% as SVG blur [BENCH: DofCss, DofSvg]
- **How.** CSS `filter: blur(Npx)` on the whole plane div. The bench used 4 px on far, 2 px on mid and 12 px on the foreground. Our `layer.blur` already does this per layer. Use it per plane (same blur for everything on one plane, [ME] R9), never per element.
- **Rack focus.** Animate the blur between the subject plane and another plane on a beat: `interpolate(f, [b, b+12], [0, 8])` on one and the reverse on the other. [ME] `focusPull.tsx` uses this as a transition between similar silhouettes (blur 18, zoom +0.04) to avoid crossfade ghosting. Add `focus` to the `Transition` enum in `core/transitions.tsx` (blur ramp plus a small scale), next to `whip`.
- **Safety [ME] P3.** Give `overflow: hidden` to any blurred layer that can scale far past the frame. On their film, Chrome crashed with "Page crashed!" 3 times out of 3 without it.
- **Budget [ME] P4.** At most 5 full-frame blur layers per scene.

### 2c. Atmospheric fade: free [OURS]
- **How.** Farther planes are lighter, bluer and lower in contrast. In SVG kits the cheapest form is a colour decision, not an effect:
  - pass `haze: 0..1` to background components and mix their fills toward the sky colour (`interpolateColors`);
  - or, for components we can't recolour, insert a full-frame haze sheet between planes: a `<div>` with `linear-gradient(transparent, hazeColor)` at an opacity tied to depth.
- **Cost.** A full-frame gradient div with normal blend is free (the `VignetteGradient` bench is the same thing). The bench scene's ridges use pre-mixed fills (`C.far`, `C.mid`, `C.near`).
- **Rule.** Far means smaller, blurrier, slower and lower contrast, all four together ([ME] M5).

## 3. Texture

### 3a. Grain / noise: the costliest common polish [BENCH: GrainTurbulence, GrainTile, GrainEffect, postgrain.sh]
- **Today.** `Episode.tsx` draws grain as a full-frame `feTurbulence` (re-seeded every 2 frames) with `mix-blend-mode: overlay` at `0.18 * amount`. [ME] `overlays/Grain.tsx` does the same at opacity 0.07, plus a vignette.
- **Measured.** The `feTurbulence` grain is **+43% calm / +105% loaded**. A 512 px tiled noise PNG with a random `background-position` every 2 frames is +15% / +71%. `noise()` from `@remotion/effects` is +60% / +201%. Adding the grain in ffmpeg afterwards is about +29% of a calm render (4.7 s per 15 s).
- **The bigger problem is bytes.** At CRF 18 a 15 s clip goes from 0.9 MB to 27 MB (tile) or 34 MB (ffmpeg), because temporal per-pixel noise can't be compressed. Upload platforms re-encode to a far lower bitrate and smear it. The `feTurbulence` file stayed small (2.6 MB) only because its grain is softer.
- **Recommendation [OURS]:**
  1. Drop per-pixel temporal grain from explainers. Kurzgesagt's texture reads as clean shapes with soft gradients, not film grain.
  2. Where texture is wanted, use a **static or slow** texture that the encoder can predict: one tiled paper or noise PNG at 3-5% overlay, moved with the camera at the plane's depth instead of re-seeded every frame. That costs the tile's +15% or less and adds almost no bytes. This is a proposal, not yet benchmarked.
  3. Keep temporal noise only as a de-banding dither on dark gradient scenes, at very low amplitude (3b).
  4. When a storyboard sets `overlays.grain`, swap the `feTurbulence` in `Episode.tsx` for a tile.
     - A re-seeded tile measured +15% instead of +43%, so those renders get about 20% faster; a static, camera-locked tile should cost no more.
     - It is a core change: make it targeted, and say so in the commit.

### 3b. De-banding [OURS, partly unmeasured]
Deep-sea and space backgrounds are long, dark, smooth gradients. In 8-bit `yuv420p` with JPEG intermediates (`setJpegQuality(92)`), they band. Fixes, cheapest first:
1. **Dither.** Very low-amplitude temporal noise is a dither that hides banding: ffmpeg `noise=c0s=2-3:c0f=t+u`, or a tile at 2-3%, applied only to scenes with large dark gradients. Check the file size; at `c0s=7` it was 34 MB per 15 s.
2. **Gradient design.** Never stretch a 2-stop gradient across 1920 px of dark blue. Use 3-4 stops with a slight hue shift, and add a soft radial highlight. Both cost nothing.
3. **Encode settings.** Unmeasured: PNG intermediates (`Config.setVideoImageFormat('png')`) remove JPEG block banding, at a cost we have not benchmarked; x264 `-tune grain` or `aq-mode=3` in the post encode keeps dark gradients. Test both on a deep-sea scene before adopting.

### 3c. Surface texture on shapes [OURS]
Kurzgesagt shapes carry subtle inner gradients and a few hand-placed highlight and shadow shapes, not noise. Bake those into kit SVGs as `radialGradient` fills offset toward the light (the bench character uses `cx=0.38 cy=0.32`). The cost is zero. Paper or halftone textures from `@remotion/effects` (`paper()`, `halftone()`, [RS] list) are canvas-only, so they carry the `HtmlInCanvas` cost.

## 4. Motion principles

Motion is pure JS math per frame, so its render cost is ≈ 0. The bench character uses every technique below and costs nothing over a static one.

### 4a. Spring and bezier easing [RS timing.md, ME ease.ts]
- **[RS] easing.** `interpolate(f, [a, b], [x, y], {easing: Easing.spring({damping: 200}), extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})` gives a push with no bounce. `Easing.bezier(0.16, 1, 0.3, 1)` is a fast start with a soft landing. A multi-keyframe `interpolate` takes an easing array with n-1 items.
- **[RS] perceptual scale.** For scale animations, pass `output: 'perceptual-scale'`. A linear scale looks like it slows down as it grows.
- **[ME] house curves.** `EASE.out (0.16, 1, 0.3, 1)`, `inOut (0.65, 0, 0.35, 1)` for the camera, `in (0.7, 0, 0.84, 0)` for exits, `back (0.34, 1.56, 0.64, 1)` for small pops. Springs: `pop` = `{damping 14, stiffness 180, mass 0.6}`; `soft` = `{damping 200}`. Start the next action only once the previous spring has settled within 5% ([ME] T3).
- **In our kit.** `core/anim.ts` `EASES` has only cubic and `back(1.7)`. Add:
  - `outExpo: Easing.bezier(0.16, 1, 0.3, 1)` and `camera: Easing.bezier(0.65, 0, 0.35, 1)`;
  - `spring` / `springSoft`, which `sample()` evaluates as `spring({frame: (t - prev.t) * fps, fps, config})` normalised to the keyframe span;
  - a `perceptual` flag for the `scale` and `zoom` keys.
  The schema change is additive: new `EaseName` values.
- **[ME] M4.** Nothing moves linearly. Peaks get S-curves with a held beat.

### 4b. Anticipation and overshoot [ME M4, OURS]
- **How.** Before a move, dip 6-10% the other way for 4-6 frames. Then spring past the target, by an overshoot that `damping` 10-14 gives, and settle. The bench jump does `y = base - 120*spring(f-10) + 30*antic(f)`, with `antic` going 0 → 1 → 0 over frames 0-10.
- **In our kit.** Add `Anim` types `popAnticipate` and `dropSquash` in `core/anim.ts` `animAt()`, and an `anticipate: px` option on keyframes. `sample()` then inserts the dip segment automatically before a keyframe that sets it.

### 4c. Secondary motion and follow-through [ME smooth.ts, OURS]
- **Lagged sampling.** A child part (antenna, tail, fin, hair, plant tip) samples its parent's motion a few frames late: `childAngle = k * (parentX(t) - parentX(t - 0.1s))`. Everything stays a pure function of t, so out-of-order rendering is still safe. The bench plants bend their tips 2.2x more than their middles, on the same sine.
- **[ME] `smooth.ts`.** `makeKernel(frames, easing)` and `smoothAt(frame, sample, kernel)` are a causal, stateless smoothing filter. Steps in a value (a counter, a chip width) come out as eased rolls; many fast steps blend into one roll. Port it as-is into `core/anim.ts` for depth meters and counters (FEEDBACK B6 progress device).

### 4d. Squash and stretch [OURS]
- **How.** Derive it from velocity, keeping the volume: `v = pos(t) - pos(t - 1/fps)`, `sy = 1 + clamp(k*v, -0.12, 0.18)`, `sx = 1/sqrt(sy)`. Add a squash on landing: `sy` dips to 0.85 for 3 frames when `v` changes sign at the ground.
- **In our kit.** It fits as an idle-like modifier: `{type: 'squash', amount}` in `idleAt()`, given the layer's sampled y track. That needs `LayerView` to pass `sample(kfs, 'y', t - 1/fps)`, which is a 2-line change.
- **Check rigs at their extremes** ([ME] M6).

### 4e. Pops and steps [ME M1-M3]
- **M1.** Never `return null` on a visible layer. Fade it over 6-10 frames. Our `LayerView` returns null outside `[start, end)`, so any layer without an `exit` anim pops. Fix [OURS]: default `exit` to a 6-frame fade when `end` is set and no exit is given.
- **M3.** Never toggle a filter on a group whose children blend: it changes blend isolation and jumps for one frame. Our `SceneView` world `gradeFilter` sits above blended layers, so turning a grade on mid-scene would jump. Keep grades constant within a scene.

## 5. Character idle: breathing and blinks (≈ free)

- **Breathing.** It exists: idle `breathe`, with `sy *= 1 + sin(w)*a`, `sx *= 1 - sin(w)*a*0.4`. Use 0.012-0.02 at 0.2-0.3 Hz for a calm character and 0.04 at 0.6 Hz when scared.
- **Blinks [OURS].** A 4-frame close/open profile `[1, 0.2, 0.05, 0.6]` every 2.5-4.5 s, with the interval jittered by `random(seed + cycle)`. The phase is anchored to a constant, never a beat, so re-timing a beat can't change frame 0 or the END ([ME] T8). This is a prop the figure must honour (`lid: 0..1` scales the eye's `ry`), not a layer transform.
  - Add `blink?: {every: 3.2, jitter: 0.8, seed}` to figure props in `kits/explainer/creature.tsx` and `people.tsx`.
  - Also add a `look?: {x, y}` eye target with a spring, so eyes follow the action. It is the cheapest way to make a character feel aware.
- **Weight shift and micro-sway.** `sway` 0.5-1° at 0.15 Hz on the torso and `bob` 2-4 px. Never fully still while the narration talks about the character (FEEDBACK A4: "nothing frozen while the narration talks about it").

## 6. FX: particles and caustics

### 6a. Particles: ≈ free up to 150 plain circles in one SVG [BENCH: Particles150, Bokeh40Gradient, Bokeh40CssBlur]
- **Plain particles.** Our `particles` layer (one SVG, no per-particle filters) is the right design: 150 circles cost nothing measurable.
- **Bokeh.** For out-of-focus specks, fill circles with a `radialGradient` (+9-12%). Do NOT put `filter: blur()` on each one (+46-82%). [ME] `Background.tsx` uses `style={{filter: 'blur(6px)'}}` on each of 34 specks; that is the pattern to avoid.
- **Readability [ME] R4.** A beat-carrying particle needs a core of at least 8 px per 1080 px plus a 3x halo; 1-2 px dust vanishes on a phone. Ambient dust can stay small.
- **More presets [OURS].** Add `bokeh`, `sparks` (short streaks along velocity, with a stroke length from the velocity, a cheap fake motion blur) and `plankton` to `PRESETS` in `core/layers.tsx`. Spawn and despawn by fading with age, never by popping.

### 6b. Caustics (underwater light net): +63-89% as live feTurbulence, +20-23% as a tiled texture [BENCH: CausticsTurbulence, CausticsTile]
- **Live.** Two full-frame `feTurbulence type="turbulence"` layers moving in different directions. A colour matrix keeps only the thin low-value ridges (`alpha = 1.4 - 10*R`), and they are screen-blended at 0.4. It looks right, but costs +63% calm and +89% loaded.
- **Tiled.** Pre-render one seamless 512 px tile once (`remotion still` of the `CausticSource` composition, `stitchTiles="stitch"`), then scroll two copies of it with `background-position`, screen blend. It costs +20-23%.
  - The bench tile came out too fine. The 15 s file grew to 41 MB, and the sheet shows a busy net.
  - Use a lower `baseFrequency` (0.008-0.012 at 512 px), blur the tile 1-2 px, and mask it to the top 40% of the frame (light comes from the surface).
- **Recommendation.** Use the tile for any scene longer than 2 s. A live feTurbulence is fine for a single hero shot.

### 6c. Motion blur: not available on the Spark [BENCH: MotionBlurCreature, MotionBlurPlainChild]
[RS] motion-blur.md recommends `<HtmlInCanvasMotionBlur>` ("state of the art", `samples` 8, `shutterAngle` 180) and says it needs no render config. In our headless swangle render it failed with "captureElementImage: No cached paint record for element" in both variants. Use cheap fakes instead:
- the whip smear we already have (`transitions.tsx`, directional `feGaussianBlur`), for 3 frames;
- streak trails for fast small objects;
- squash-stretch along the velocity (4d).
[RS] points to Remotion's motion blur guide for other options. The installed `@remotion/motion-blur` 4.0.539 also exports `<Trail>` and `<CameraMotionBlur>` (we checked its `dist/`). They render the subtree N times, so expect about N times the cost of the blurred subtree. Not benchmarked.

## 7. Camera: multi-plane moves and match cuts

- **Multi-plane moves.** These are free (2a). The shot list should make every move lateral or vertical through the planes, not only a zoom. A depth-dive (camera y moving down through haze sheets that thicken with depth) is the signature Kurzgesagt "scale" move, and it is just keyframed `y` plus per-plane haze opacity.
- **The hook moves on frame 1 [ME] R10, remotion-patterns "Easing and motion".** Put the first camera key at frame -30, so the push is already moving at frame 0. Their fix raised early motion from 0.29 to 0.77 mean frame diff. In our `cameraAt()`, keys are scene-local seconds, so allow negative `t` on the first scene's camera keys. In FEEDBACK B3 terms, frame 0 is the cover, but frame 1 must already move.
- **Hold still while reading [ME] M5.** `drift = 0` while a chart, map or label is being read.
- **Impact shake [ME] camera.tsx.** `kickShake(frame, at, amp=14) = amp*k*exp(1-k)*exp(-(f-at-2)/8)`, with `k = (f-at)/2`: zero before the hit, peak 2 frames later, gone after about 20. Our `Shake` has an attack/decay envelope already. Add this kick shape as `shape: 'kick'`.
- **Match cuts [ME] H1-H2, remotion-patterns "Handoffs".** When the subject continues across a cut, the outgoing scene owns its END as numbers: centre, size, zoom, light, seeds, clock, facing. The incoming scene's frame 0 is built from those numbers, never from a re-guess.
  - [ME] `handoff_diff.py` checks it: mean ≤ 2/255 and max ≤ 20/255 between the real upstream END and the downstream frame 0.
  - In our storyboard JSON this becomes `scene.handoff = {from: <sceneId>}` [OURS]. The validator copies the camera and the subject layer's last sampled state into the new scene's first keyframe.
- **Opaque-underneath fades [ME] H4.** Remotion's `fade()` keeps the outgoing scene opaque. Fade outgoing translucent extras (glows, halos, rings) from 1 to 0 over the last 15 frames, or they double and then vanish at the cut. Our `fade` transition only ramps the incoming scene's opacity, so the same rule applies.
- **Transitions [RS] transitions.md.** `TransitionSeries` with `fade()`, `slide()`, `wipe()` and custom presentations, plus `TransitionSeries.Overlay` for an effect over the cut without shortening the timeline (a light leak). We have our own `transitionLook()`. The overlay idea maps to a new `overlay` field on `Transition`.

## 8. Sound design (no render-time cost)

Audio is mixed by Remotion's ffmpeg step after the frames, so none of this changes Chrome time. Sources: [ME] audio.md and rules A1-A7; [RS] sfx.md and audio.md.

1. **Every visible motion gets a sound.** Kurzgesagt's mix is dense: soft whooshes on camera moves, pops or ticks on each element appearing, a low bed per location, risers into reveals, and a hit on the payoff. Our `scene.sfx` cues are scene-local; make the storyboard writer emit one cue per `enter` anim and per camera key [OURS].
2. **Phone body [ME] A4.** Every SFX needs content at 120-600 Hz and must stay within about 10 dB of the voice through a 200 Hz high-pass. Phones drop sub-bass: their kick and impact had 51-66% of their energy below 80 Hz and vanished until a 300→140 Hz body layer was added.
3. **Voice beats SFX by 6 dB in 1-4 kHz on every word [ME] A3.** Duck risers under words, starting the duck 0.07 s early, because volume functions land about 2 frames late ([ME] A5). Our `audio.tsx` `duckAmount()` has attack/release for music only. Extend it to `sfx` clips that overlap speech.
4. **Clean edges [ME] A1-A2.** First sample at 0.000, a 3-10 ms fade-in after filters, `asetpts=PTS-STARTPTS` right after `atrim`, tails below -60 dBFS, 32-bit float intermediates. This is FEEDBACK A2 ("no audible seams"). Run their `clicks.py` probe idea on every mix.
5. **Pitch variants [ME] audio.md.** Use `asetrate=48000*1.12,aresample=48000` for repeated pops and whooshes, so ten pops don't sound copy-pasted.
6. **Synthesise beds [ME] lessons "Audio".** Generator duration sliders were unreliable, so beds were filtered brown noise plus a slow pulse in Python. Our `pipeline/audio/synth.py` already goes this way.
7. **Do not use [RS] sfx.md's list.** Its sound effects are meme clips hosted at `remotion.media` (vine-boom, bruh, wilhelm-scream). They would be fetched over the network at render time, their licence is unclear, and they are the wrong tone. Keep our local `studio/public/sfx/` library (`pipeline/audio/LICENSES.md`).
8. **Master** to -14 LUFS / -1.5 dBTP, and refuse a missed target rather than ship it ([ME] A6, `master.sh`).

---

## QA and polish passes worth adopting from motion-explainer

These map one-to-one onto FEEDBACK.md rules. The probes are stdlib Python plus ffmpeg, about 50-90 lines each, in `experiments/vendor/motion-explainer/assets/template/scripts/qa/`. We read them but did not run them. Port them after review.

| [ME] pass / probe | What it measures | Threshold | FEEDBACK rule |
|---|---|---|---|
| Builder, then an independent polish agent (orchestration.md "Polish reviewer") | Re-renders, ranks problems by impact, fixes, and measures before and after | Builders land at about 6/10; polish lifts to 7.5-8.2; never 9 in one pass | A5 process, the ≥ 7 gate |
| 270 px read test (R1) | Each beat frame at a 270 px short side gets "this reads as ___". Catches face and animal traps (R2) | Any unintended face, animal or body-part read is a bug | B5, B8 |
| `qa/picture/luma_steps.py` | Largest per-cell luma jump between frames (120 px cells), classified POP / RUN / CUT | POP > 20/255 outside a designed cut fails | A4 (no snapping) |
| `qa/picture/caption_contrast.py` | Caption band contrast with captions OFF, every frame | ≥ 4.5:1, aim for 6:1 | B8 |
| `qa/picture/handoff_diff.py` | Upstream END vs downstream frame 0 | mean ≤ 2/255, max ≤ 20/255 | A3 consistency |
| `qa/audio/phone_mix.py` | Voice vs SFX+music in 1-4 kHz per word; SFX through a 200 Hz high-pass | +6 dB; ≤ 12 dB lost | A1, A2 |
| `qa/audio/clicks.py` | One-sample jumps at clip edges | > -40 dBFS fails | A2 |
| `qa/sync_drift.py` + `beats.ts` `// sync: "<word>"` tags | Each beat vs its measured word onset | Lands on the word or 1-3 frames before | B5 ("if the narration says it, the viewer sees it") |
| Subject size (R3) | The named subject's share of the short side at its beat | ≥ 35%; non-focal layers dimmed ≥ 40% | B5 |

## Adoption order (cheapest first)

1. **Free, look-only:**
   - depth presets and a foreground plane in every wide shot (2a);
   - CSS-blur depth of field (2b);
   - haze sheets (2c);
   - gradient glow, rim and contact shadow props on figures (1a-1c);
   - blink and look-at on figures (5);
   - default 6-frame exit fades (4e).
2. **Free, motion:** spring, expo and perceptual easing in `anim.ts` (4a); anticipation anims (4b); velocity squash (4d); the [ME] `smoothAt` port for meters (4c); camera pre-roll, `kickShake` and drift-off-while-reading (7).
3. **Cheap with a rule:** rays merged into one screen-blended layer per scene and masked off the caption band (1d, +2-28%); bokeh as gradients (6a, +9-12%); caustics as a tile (6b, +20-23%).
4. **Grain:** replace the `feTurbulence` grain with a static, camera-locked texture tile, and keep temporal noise only as a light dither on dark-gradient scenes (3a/3b). Renders that set `overlays.grain` get about 20% faster, and files stay small.
5. **QA probes:** port luma_steps, caption_contrast and phone_mix into `scripts/qa/` after review, and run them in the gate.
6. **Avoid on this box:**
   - `HtmlInCanvas` + `@remotion/effects` on DOM content (10.7x);
   - `HtmlInCanvasMotionBlur` (fails headless);
   - per-element CSS blur;
   - live feTurbulence for whole scenes;
   - WebGL effects outside a few transition frames.

The combined stack measured **+29%** over flat without grain (`KurzStackNoGrain`) and **+68%** with the tiled temporal grain (`KurzStack`), both on a calm box. The stack is 5 planes, CSS depth of field, rim, halo, contact shadow, 6 rays, 40 gradient bokeh, 80 particles and a vignette. For a 60 s Short at concurrency 2, the no-grain stack costs about 15-25 s more render time. The look is in `out/polish-bench/kurzstack_nograin_f225.jpg`.
