# polish-2d: polish pass on the orca pilot's first 10 s (Test 1 build)

**What it is.** A separate Remotion entry (`src/index.ts`) that imports the live kit (`studio/src`) without changing it. It re-renders frames 0-299 of `episodes/explainer-orca/storyboard.json` with the polish techniques from `docs/POLISH_IDEAS.md` and the same narration. The A/B baseline is the live pipeline's own entry (`studio/src/index.ts`, composition `Storyboard`, the same props file, the same encoder config), rendered over the same frames.

**Outputs**, pulled back to the Mac in `out/polish-2d/`. All are 1080x1920, 30 fps, 10.0 s.

| File | What |
|---|---|
| `out/polish-2d/baseline10.mp4` | Live pipeline, first 10 s |
| `out/polish-2d/polish10.mp4` | This experiment, first 10 s |
| `out/polish-2d/ab_side_by_side.mp4` | Left: baseline. Right: polish. Plays the polish audio |
| `out/polish-2d/ab_sheet.jpg` (also `results/ab_sheet.jpg`) | Matched stills at 0.0, 1.5, 2.6, 5.6, 7.1, 7.6 and 8.4 s |
| `out/polish-2d/strip_{baseline10,polish10}.jpg` | Every frame of the car drops, frames 206-225 |

The Spark copies are in `~/studio/app/experiments/polish-2d/out/`. That folder also holds every variant MP4.

**Code and inputs.** Built against repo HEAD `3cfa3c1`, with Remotion 4.0.539 from `studio/node_modules`. Nothing in `studio/src`, `pipeline/`, `scripts/` or `episodes/` was edited.

## Reproduce (on the Spark)

```
rsync -a --exclude node_modules --exclude out --exclude build --exclude public experiments/polish-2d/ dgx-spark:studio/app/experiments/polish-2d/
ssh dgx-spark 'cd ~/studio/app/experiments/polish-2d && bash render.sh && bash ab.sh'
```

What the scripts do:
- **`render.sh`** symlinks `node_modules` to `../../studio/node_modules`, so both trees share one `remotion` and `react` instance. It builds the grain tile and the A/B audio (`audio/make_audio.py`), takes `~/studio/locks/render.lock`, bundles both entries, then renders.
- **Render settings.** Every render is `--concurrency=4`, `nice -n 10`, `CUDA_VISIBLE_DEVICES=""`, with swangle software GL.
- **Variants and timing.** The script renders each composition in turn, bracketed by baseline runs, and appends the times to `results/times.tsv`.
- **Startup cost.** `FRAMES=0-1 TAG=_startup bash render.sh Base Polish10` measures the fixed cost of each render.
- **Bundle.** The baseline bundle gets a slim public dir that holds only `mix.wav`; the real `studio/public` is 1.5 GB. Frames are unaffected. `kit10.mp4`, the live `Episode` rendered through this entry, is byte-identical in size to `baseline10.mp4` (3,668,727 B).

## What was applied

All of it is a storyboard transform (`src/polish.ts`) plus new components registered under `polish/*` (`src/fx.tsx`, `src/lit.tsx`, `src/spring.tsx`). Grain is the one exception: `src/PolishedEpisode.tsx` is `Episode.tsx` with a single change, the grain. Section numbers below refer to POLISH_IDEAS.

| Group | Technique | How | Source |
|---|---|---|---|
| Lighting | Rim light on every figure (orca, diver, YOU, cars) | `polish/Lit` wraps `getFigure`/`makeCtx` from `kits/explainer/creature.tsx`. Rim = body minus the body shifted away from the light (SVG mask), filled `#c9f3ff` at 0.62. Rim width is 6 px on the orca and 3.5 px on small figures. One light for the whole shot (angle 80°, from the upper left); flipped layers mirror it | 1a, ME L1 |
| | Form shading | Gradient along the light direction, masked to the body: cool highlight 0.16 on the lit side, deep-water blue `#03141d` 0.42 on the far side (not black) | 3c, ME L1 |
| | Halo behind the orca | Radial-gradient div that copies the orca layer's x/y/keyframes. Alpha 0.2 (p00) or 0.16 (p01), slow 0.25 Hz pulse | 1b |
| | Surface glow + 5 god rays | `polish/Light`: one SVG on a 0.25-depth plane. Rays lean with the light, breathe on independent phases, and fade to 0 at 60% of H, above the caption band | 1d |
| Depth | Far pod | `polish/FarPod`: 3 orca silhouettes in the water colour, 150-250 px, swimming slowly. Depth 0.35, whole-layer CSS blur 2.5 px, opacity 0.55/0.38. It literalises "wild killer whales" | 2a, 2b, 2c |
| | Haze sheet | `polish/Haze` at depth 0.5: transparent at the top to `rgba(3,16,24,.42)` at the bottom. It also darkens the caption band | 2c |
| | Foreground bokeh | `polish/Bokeh` at depth 1.5: 11 radial-gradient specks (no per-speck blur), only in the outer 22% of the width and outside the caption band. The first try let them cross the orca, where they read as smudges on its face | 2a, 6a |
| | Lateral camera drift | p01 camera x goes 48.6% → 51.4% over the scene (the original was zoom only), so the planes separate | 2a |
| Motion | Camera pre-roll | The p00 pull-back now moves on frame 1. The schema rejects negative keyframe `t`, so the pre-rolled inOut curve is baked into linear keys every 2 frames; frame 0 keeps the cover framing | 7, ME R10 |
| | Punch-ins with overshoot | Camera keys with `ease: out` that zoom in by > 0.08 within ≤ 0.3 s become `backOut` (about 10% overshoot) | 4a, 4b |
| | Car drops | `polish/Spring` replaces the kit's `drop` (bounce easing). A gravity fall over 0.22 s, a slight stretch while falling, then a 22% volume-keeping squash on landing that springs back. A 3.5 px camera kick on each landing | 4b, 4d, 7 |
| | YOU pop | Spring scale with overshoot; the vertical axis leads the horizontal by 2 frames (follow-through). Replaces `pop` (backOut) | 4a, 4c |
| | Secondary motion | In the diver → tether → YOU-tag chain, the tag now follows the diver's float 0.16 s late and the tether 0.07 s late. Before, the tag was rigid while the diver floated (FEEDBACK A3/A4) | 4c |
| | Orca body pitch | Idle sway of 0.7° at 0.22 Hz on top of the kit's tail beat | 4c |
| | Hand-held drift | `camera.shake` with `decay: false`, 4 px, 0.22 Hz, no roll (the kit already supports this) | 2a, ME camera |
| Texture | Grain | The `feTurbulence` grain is turned off. A static 512 px noise tile, world-locked (it follows the active scene's camera at depth 0.6), overlay at 0.10 | 3a proposal 2 |
| Grade | Scene grade | brightness 1.02, contrast 1.05, saturate 1.12. Constant within each scene (M3) | 4e, M3 |
| Sound | 16 designed cues + a bed on top of the same `mix.wav` | `audio/cues.json`, built by `audio/make_audio.py`: a whoosh on the pull-back, a low impact on "kill", a thump on the punch-in, ticks for each headline/tag, a zip and click for the scale bar, 4 pitch-varied thuds for the cars, a pop for YOU, a whoosh into the whip, and an `underwater_rumble` bed at -37 dB RMS. Each cue gets a pitch variant, a 90 Hz high-pass, a peak target and a 5 ms fade-in. The sum goes through a -1.5 dBFS limiter | 8.1-8.5 |

## Render time vs baseline

10 s (300 frames), concurrency 4, Spark CPU. Load average was 9-15 during the runs. Another of our jobs, a Fish-S2 CPU TTS test using about 4-5 cores, was running at the same time. Data: `results/times.tsv`, `results/summary.tsv`.

| Composition | Runs | Wall s | vs base | Net s (minus 1.7 s startup) | Net vs base | File MB |
|---|---|---|---|---|---|---|
| **Base** (live pipeline) | 7 | 11.41 (sd 0.39) | 1.00 | 9.71 | 1.00 | 3.67 |
| Kit10 (live `Episode` through this entry) | 2 | 11.80 | 1.03 | 10.10 | 1.04 | 3.67 |
| Kit10NoGrain (live kit, `overlays.grain = 0`) | 2 | 9.10 | **0.80** | 7.40 | **0.76** | 3.67 |
| **Polish10** (everything) | 4 | 15.28 | **1.34** | 13.58 | **1.40** | 5.48 |
| Polish10NoGrain | 2 | 12.20 | **1.07** | 10.50 | 1.08 | 4.61 |
| Polish10NoLight | 1 | 13.50 | 1.18 | 11.80 | 1.21 | 4.98 |
| Polish10NoDepth | 1 | 13.30 | 1.17 | 11.60 | 1.19 | 5.56 |

How the cost splits, per 10 s of video, from the variants:
- **Lighting:** +1.8 s.
- **Depth planes:** +2.0 s.
- **Grain tile:** +3.1 s.
- **Motion, sound and grade:** about 0 s, within noise. Motion is per-frame maths, and sound is mixed outside Chrome.
- The single-run variants are ±0.4 s.

Findings:
1. **The live grain is invisible and expensive.** `Episode.tsx` draws `feTurbulence` at `0.18 * 0.04 = 0.7%` opacity. With it switched off, the MP4 is the same size within 43 bytes (3,668,727 vs 3,668,770 B): after JPEG intermediates and x264 at CRF 18, nothing of it survives. Yet it costs **+24% of render time** (9.10 s vs 11.41 s wall).
2. **The polish without grain costs +7% over what we ship today.** All the lighting, depth, motion, grade and sound renders in 12.2 s against the baseline's 11.4 s, because it drops the invisible grain. Compared with a flat kit that also has no grain, the visual layers cost +42% net (7.4 → 10.5 s). That is in line with the bench's `KurzStackNoGrain` (+29% calm) plus the 4x figure draws for the rim.
3. **The world-locked grain tile is not worth it.** At overlay 0.10 it is barely visible on the dark water (1:1 crops at t = 5 s with and without it are almost the same). It costs +3.1 s (+25%) and +0.9 MB (+19%). It is not cheaper than `feTurbulence` here: compositing an overlay-blended, camera-transformed 1.7x-frame div costs more than the bench's untransformed tile. Do not adopt it. If texture is wanted, bake it into background art.
4. **File size.** 5.48 MB for the polish vs 3.67 MB for the baseline, about 4.4 vs 2.9 Mbit/s. Without the grain tile it is 4.61 MB; the extra bytes come from the rays, bokeh and moving planes.
5. **Loudness is matched.** Polish -14.0 LUFS, peak -1.4 dBFS. Baseline -14.2 LUFS, peak -1.3 dBFS. The designed SFX stem alone is -29.9 LUFS, peak -14.1 dBFS: about 16 LU under the mix, so it accents and does not compete. A 200 Hz high-pass removes 3.4 dB of the SFX stem (ME A4 allows ≤ 12 dB), so the cues keep their body on phones. Not done: the per-word 1-4 kHz voice-vs-SFX check (ME A3) and SFX ducking under words.

## What it looks like (honest read of the frames)

These are my reads of the stills and the car-drop strips, not a judged score.
- **Biggest visible gains:**
  - the rim and form shading give the orca a lit top edge and volume;
  - the god rays and surface glow give the water a light source;
  - the car drops now land with a squash and a camera kick instead of a rubbery bounce;
  - the YOU tag hangs off the diver instead of floating rigidly beside it.
- **Small effects:** the far pod and the haze add depth in wide frames but are subtle at phone size. The halo and the grain are close to invisible.
- **Still far from Kurzgesagt-tier:**
  - the figures are still flat kit shapes, with no secondary detail, highlights or texture in the illustration;
  - the layout and typography are unchanged.
  - This pass improves lighting, depth and motion craft. It does not close the illustration gap (FEEDBACK log, "the gap is authoring").
- **Unchanged by design:** frame 0 (the cover) keeps its framing; the pre-roll changes frames ≥ 1 only. The captions are unchanged.

## What would need to change in the kit to make this the default

These are targeted changes, cheapest and most valuable first. None were made here. Core files are shared, so each should be its own commit that says it touches core.

1. **Drop the invisible grain.** `pipeline/episodes/build.py` emits `overlays.grain: 0.04`. Set it to 0, or remove the `feTurbulence` `Grain` from `core/Episode.tsx`. This gives -24% render time with no visible change. On its own it pays for most of the polish below.
2. **Figure lighting** in `kits/explainer/creature.tsx`:
   - give `Creature` a `light` prop and port `src/lit.tsx`'s mask approach (body, rim mask, shade mask: four draws of the same paths);
   - add `scene.light = {angle, color}` in `core/schema.ts` so every figure in a shot shares one light;
   - pass `flipX` into kit props (`LayerView` already knows it).
3. **New FX components** in a new file such as `kits/explainer/fx.tsx`: `Light`, `FarPod`, `Haze`, `Bokeh` and `Halo` from `src/fx.tsx`. `build.py` should emit the four planes for every underwater wide scene with the depth presets used here: far 0.35, haze 0.5, light 0.25, foreground 1.5.
4. **Spring anims in `core/anim.ts`:** a `dropSquash` and a `popSpring` anim type (the logic in `src/spring.tsx`), and a `transformOrigin` on layers. `build.py` would then emit those instead of `drop` and `pop`.
5. **Camera** (`core/schema.ts`, `core/camera.ts`):
   - allow a negative `t` on camera keyframes (`Seconds` is `min(0)` today), or add `camera.preroll`, so the pre-roll doesn't need baked keys;
   - have `build.py` emit `backOut` for punch-ins, a low drift shake (`decay: false`), and a lateral x drift on long scenes. All three already work with the current schema.
6. **Attached labels.** When `build.py` attaches a tag and tether to a figure, it should give them the figure's idle with a phase lag (`lagPhase()` in `src/polish.ts`). Idle `phase` already exists.
7. **`layer.blend` is a no-op in the kit.**
   - **Why.** `SceneView` wraps each layer in its own transformed plane div. A transform creates a stacking context, which isolates `mix-blend-mode`. So `blend: "screen"` composites against transparency.
   - **Status.** This follows from the CSS compositing spec. It is not yet confirmed with a render; a one-frame test would settle it.
   - **What this experiment did.** Its FX use normal alpha.
   - **Fixes.** Either put `mixBlendMode` on the plane div when the layer sets `blend`, or document that `blend` only works on screen-space overlays (as the grain and vignette in `Episode.tsx` do).
8. **Sound** (`pipeline/audio/`): generate one cue per `enter` anim, camera punch and drop landing, with pitch variants, from the same storyboard data `build.py` already has. `audio/cues.json` here is the hand-written version for 10 s. Add the per-word ducking and the phone-mix check before shipping it pipeline-wide.
9. **Scene grade.** `build.py` emits `grade: {brightness 1.02, contrast 1.05, saturate 1.12}` for explainer scenes. It is free, and it is constant per scene (M3).

## Caveats

- **Scope.** Only the first 10 s (p00, p01, and the first 0.37 s of p02) were polished and judged. Other scenes would need their own light direction and their own placement of the far pod and bokeh.
- **Timing noise.** The times come from a shared box with another job of ours running. The baseline spread was ±0.4 s (sd), and the NoLight and NoDepth splits are single runs.
- **Concurrency.** The task asked for concurrency 4. BRIEF's budget asks for 2 while another of our TTS jobs runs; the box load stayed at 9-15 out of 20 cores.
- **Not run:** the ME QA probes (`luma_steps`, `caption_contrast`, `phone_mix`).
