# R&D log

Append-only. One dated section per experiment: setup, numbers, verdict. Never rewrite someone else's entry.

## 2026-11-02 ~11:20 UTC: 3D render cost for the story lane (@remotion/three on the Spark and the Mac)

**Question.** Can @remotion/three 3D sets (toon shading, ink outlines, lens blur) render 2 story Shorts a day
(~60-65 s, 30 fps, ~1900 frames each, ~3 full renders per Short for fix rounds) on our hardware?
This is step 3 of the plan in `research/references/STORY_LANE_TUTORIAL_CHECK.md` section 4.

**Setup** (`experiments/three-lane/`, its own Remotion project, not the studio kit)
- remotion, @remotion/cli, @remotion/three 4.0.539 (same as `studio/package.json`), react/react-dom 19.1.0,
  three 0.186.1, @react-three/fiber 9.8.2, postprocessing 6.39.5 (no @react-three/postprocessing: the composer is
  driven by hand from a priority-1 `useFrame`). Lockfile committed.
- Set: a palace-hall corner. Plank floor, two plaster walls with a red lacquer wainscot and top beam, a lattice window
  with sky behind it, a lacquer pillar, a rug, and 3 Poly Haven props: cabinet, tea table, armchair (~21k tris
  together). Canvas2D-painted textures. Two-tone shading: warm lit colour, violet-blue shade, with real shadow-map
  visibility from one warm key light (2048² shadow map). Fog in the warm horizon colour.
- Character: a camera-facing card with a canvas-drawn round-head stick figure, redrawn every frame (breathing bob).
  It sits on the NOINK layer, takes the light colour (warm when lit, violet-blue under a cast shadow), casts a
  cut-out shadow and has a multiplied contact blob.
- Post: RenderPass (MSAA 4, HalfFloat) → InkPass (world-only normal+depth re-render, depth-jump + crease edges,
  up to 9 px search in 4 directions) → lens blur pre (16 taps) → lens blur main (64 + 32 near taps) →
  Neutral tone map + mild grade (S-curve, violet shadow tint, warm highlights, vignette).
  Ink, lens blur, grade and two-tone are ported from mromidev/claude-animated-shorts `templates/bridge/`
  (MIT, full notice in each file header).
- Camera: a 90-frame (3 s) smootherstep dolly. It pushes in ~1.6 m and trucks left ~0.85 m, so parallax shows
  (the window slides out of frame and the cabinet moves against the character).
- Compositions: `Hall1080` (1080x1920), `Hall720` (720x1280), `Hall1080NoMSAA`, and `GLInfo`, which prints the
  WebGL renderer strings into the frame.
- All renders went through the dispatcher:
  `PROJ=experiments/three-lane ENTRY=src/index.ts CONC=2 RENDER_SLOT=spark|mac scripts/render.sh <Comp> <out> --frames=0-89 [--gl=...] --timeout=240000`.
  Spark: `--gl=swangle`, CUDA_VISIBLE_DEVICES="", nice 10, `--concurrency=2`, under `~/studio/locks/render.lock`.
  Mac: nice 15, `--concurrency=2`, Chrome for Testing.
  - For a new PROJ, spark_render.sh runs `npm ci` itself (inside the lock) when `package-lock.json` changes. I
    installed once on the Spark with nice and wrote `node_modules/.lockhash`. The Mac slot ran its own `npm ci`.

**Assets + licences** (`experiments/three-lane/ASSETS.md`)
- Poly Haven glTF 1k (author Kirill Sannikov), all **CC0** (https://polyhaven.com/license, read 2026-11-02):
  - Chinese Cabinet: https://polyhaven.com/a/chinese_cabinet
  - Chinese Tea Table: https://polyhaven.com/a/chinese_tea_table
  - Chinese Armchair: https://polyhaven.com/a/chinese_armchair
- Downloaded via api.polyhaven.com / dl.polyhaven.org. 5.4 MB, committed in `experiments/three-lane/public/`.
- Kenney was not used: kenney.nl returns HTTP 403 to scripted requests, and we did not work around it.
- Nothing came from the mromidev repo's `references/frames` or `references/sheets`.

**GL renderer (headless Chrome, read by the `GLInfo` composition)**

| Machine | `--gl` | UNMASKED_RENDERER |
|---|---|---|
| Spark | `swangle` | ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (LLVM 10.0.0) (0x0000C0DE)), SwiftShader driver): CPU only |
| Spark | none (default) | the same SwiftShader string (no GPU is used either way) |
| Spark | `swiftshader` | **no WebGL at all**: Chrome 157 removed the legacy SwiftShader GL, so use `swangle` |
| Mac | `angle` or none | ANGLE (Apple, ANGLE Metal Renderer: Apple M1 Pro): GPU |

**Seconds per frame** (90-frame renders, concurrency 2)
- T90 = dispatcher-reported render time for frames 0-89.
- T1 = the same command for one frame (bundle, browser start, model load, shader compile, encode).
- s/frame = (T90 − T1) / 89.

| Machine | Resolution | Renderer | MSAA | T90 | T1 | `remotion still` (1 frame) | **s/frame** |
|---|---|---|---|---|---|---|---|
| Spark (20 cores, CPU) | 1080x1920 | SwiftShader (swangle) | 4 | 87.5 s (3 runs: 87.50 / 87.52 / 87.53) | 9.07 s | 8.0 s (2 runs) | **0.88** |
| Spark | 1080x1920 | SwiftShader | 0 | 69.4 s | (9.07 s) | | **0.68** |
| Spark | 720x1280 | SwiftShader | 4 | 48.3 s | 9.05 s | 6.7 s (2 runs) | **0.44** |
| Mac (M1 Pro, 16 GB) | 1080x1920 | ANGLE Metal (GPU) | 4 | 33 s | 6 s | (the 1-frame dispatcher render, 6 s, stands in: no hand-started Mac render) | **~0.30** (the Mac timer has 1 s resolution) |

- **Spark CPU while rendering 1080:** the Chrome GPU process (SwiftShader) used **8.0-8.4 cores** with MSAA and
  9.3-9.9 without it. node and the compositor used ~0.1. That fits the ≤ 12-thread budget, but leaves only ~3 cores
  for anything else of ours during a 3D render. Remotion has no flag to cap SwiftShader's thread pool.
- **Upscale (720 → 1080, lanczos, x264 crf 18, 4 threads, Spark):** 2.2 s per 90 frames, ~45 s per Short.

**Per Short and per day** (1900 frames; 6 full renders a day = 2 Shorts × 3 renders)

| Route | Per Short | 6 renders/day |
|---|---|---|
| Spark 1080, MSAA 4 | 0.88 × 1900 + 9 s ≈ **28 min** | **2.8 h** |
| Spark 1080, no MSAA | ≈ 22 min | 2.2 h |
| Spark 720 + upscale | ≈ 14 min + 1 min | 1.5 h |
| Mac 1080 (Metal) | ≈ 10 min | 1.0 h, when the Mac slot is free (see below) |

**Frames to look at**
- `experiments/three-lane/out/spark1080_f45.jpg`: the Spark 1080 render, frame 45.
- `spark1080_dolly_f0_45_89.jpg`: the dolly.
- `mac1080_f45.jpg`: the Mac render matches the Spark render by eye.
- `spark720_f45.jpg`.

What the frames show:
- Ink on the table, cabinet, wainscot and wall corner. Background lens blur, with the character card crisp.
- A warm key and violet-blue cast shadows on the wall and rug. The character card is tinted and casts a shadow.
- At this shot size, 720 upscaled and 1080 without MSAA are hard to tell apart from 1080 with MSAA 4.
- `look_cInf18_f45.jpg` is a lesson: with a stronger lens blur (cInf 18 px, ~4 px CoC one metre behind focus), the
  ink on mid-ground props is blurred away. cInf 10 keeps it. The ink-before-DOF order is right, but DOF strength has
  to leave the mid-ground lines readable.

**Verdict: practical at 1080x1920 on the Spark (CPU, SwiftShader), with 720 + upscale as the fallback.**
- 0.88 s/frame is 3.4x under the check's ~3 s/frame limit.
- A full Short takes ~28 min, and a day's 6 full renders take ~2.8 h of the single render lock.
- The Mac (Metal) is ~3x faster (~10 min/Short), but it is not a dependable slot. Today the first attempt was refused at
  4.80-4.96 GB free RAM (the limit is 5 GB). The one retry, 4 min later, went through at 5.12 GB.

**Caveats:**
- This test set is light: one room, 3 props, one card. Cost is mostly per pixel: 720 costs 0.50x of 1080 for 0.44x
  of the pixels, and the ink and lens-blur gathers dominate. So more props add less than more post or more
  resolution does.
- Production adds characters (a canvas redraw each), crossfade frames (two canvases on ~60-80 frames per Short),
  bigger worlds and the 2D caption/overlay layers.
  - Budget 2-3x: 1.8-2.6 s/frame, or 1-1.4 h per Short at 1080. That is still under the threshold, but 6 renders
    would hold the shared render lock 6-8 h a day.
  - If production frames land above ~1.5 s/frame, render the 3D lane at 720x1280 and upscale (the reference is served
    at 720p anyway), or drop MSAA (−23 %).
- Fix rounds should re-render only the changed `--frames` range, not the full Short.

**Next:** plan step 4 (one 3D set, end to end), with a real 10 s story section to re-measure s/frame under
production load (crossfades, 2 characters, captions).

**Addendum (same day, story-chess-turk v5, the 2D baseline).**
- The finished 2D v5 Short renders 1767 frames in ~93 s on the Spark (CPU, concurrency 2), about 0.05 s per frame.
  That includes the set lens blur, ink and grade.
- The 3D test frame costs 0.88 s per frame, about 17x more. That is still ~28 min per Short, so the verdict stands.
- The measured gap that the 2D kit cannot close is real parallax:
  - In v5 the set moves at depth 0.9 against 1.0 for the characters.
  - Every hold must drift between checked framings so that nobody gets cut by an edge.
  - In 3D the dolly would move the world while the subject stays framed. That is the case for plan step 4 (one 3D set, end to end).

## 2026-11-02 ~14:10 UTC: src/next parity pieces for the 3D story kit, proven in KitLab (visuals track)

**Question.** Can the RicksClips rule book's gaps 1-6 be closed with new kit pieces, measured against the 24
references' ranges? The coordinator added two more on the v14 panel: set detail density and character framing.

**Setup**
- The pieces live in `experiments/three-lane/src/next/`, new files only (the kit was shared with the story-vasa pass).
  Wiring is in `src/next/INTEGRATION.md`.
- **Proving reel:** composition `KitLab` (entry `src/next/index.ts`).
  - 36.9 s, 14 shot groups, 9 places.
  - The narration is our own lab text (a lighthouse keeper's clock), with word timings synthesised at 3.7 wps.
    There is no voice track.
- **Render:** Mac slot, niced 15, one render at a time, gated on ≥ 5.2 GB RAM and ≥ 15 GB disk, under the Mac
  render lock. 1107 frames at 1080x1920 took 2:09 (**0.12 s/frame**, ANGLE Metal, concurrency 2).
  - `repair_frames.py` replaced 1 tiled-mosaic frame.
  - Nothing ran on the Spark.
- **Files:**
  - render: `experiments/three-lane/out/kitlab/kitlab_v4r.mp4` (sha 2454f4ee…, not committed);
  - phone copy: `out/kitlab/kitlab_v4_phone.mp4` (720p, 9.0 MB).
  - All numbers below are in `research/references/data/kitlab_v4_measure.json`.
- **Measurement:** ours at 240x426, like the references in `ricks24_metrics.json`, with `frame_metrics`,
  `camera_motion`, `look_stats` and `frames30`. New tools:
  - `src/next/tools/ghost_check.py`
  - `src/next/tools/look_density.py`
  - `src/next/tools/plan_kitlab.ts`
  - `src/next/tools/cast_check.ts`

**KitLab v4 against the 24 references (240p; min / median / max)**

| Check | Refs | KitLab v4 | |
|---|---|---|---|
| transitions / min | 9.2 / 18 / 24.8 | 21.1 | in |
| hard cuts | 0 / 1 / 3 | 0 | in |
| shot length median · max (s) | 1.67 / 2.45 / 7.47 · 4.7 / 7.8 / 14.9 | 2.8 · 4.3 | median in; max just under the refs' min (the 4 s rule does that) |
| first transition (s) | 0.03 / 0.65 / 8.5 | 3.4 | in |
| moving % · dead-still % | 95.3 / 99.7 / 100 · 0 / 0.3 / 4.7 | 97.3 · 2.7 | in |
| median speed · moves / 10 s (px/f) | 3.1 / 5.6 / 17.2 · 3.8 / 6.2 / 13.4 | 9.8 · 7.6 | in |
| attack · release · peak (f, f, px/f) | 4.5 / 11.8 / 20.5 · 4.5 / 10.8 / 34 · 10.8 / 19.3 / 29.3 | 12 · 10 · 25.6 | in |
| snaps | 0 / 5 / 14 | 4 | in |
| quiet zoom % · push-in share % | 68 / 82 / 97 · 48 / 69 / 88 | 83 · 62 | in |
| frames30 jumps · frozen | 0 / 4 / 26 · 0 | 16 · 0 | in (above the newer refs' 0-11) |
| luma · saturation · colourfulness | 0.15 / 0.44 / 0.66 · 0.26 / 0.46 / 0.62 · 15 / 26 / 35 | 0.31 · 0.45 · 22 | in |
| non-ink p5 · black area · shadow chroma | 0.04 / 0.17 / 0.27 · 0 / 0 / 0.10 · 6 / 16 / 34 | 0.12 · 0 · 15.5 | in |
| ink edge · soft edge (240p) | 0.04 / 0.18 / 0.34 · 0.26 / 0.41 / 0.55 | 0.47 · 0.16 | **out** (kit-wide: see below) |

**Per piece**

1. **Cutaways + planner** (`cutaways.ts`, `pov.tsx`, `planner.ts`).
   - Six insert sets are in the reel: macro, cross-section, blueprint, map with route, X-ray scan room, spyglass POV.
   - Plan check: 25 place or view changes (40.7 / min), place changes **21.2 / min** (refs 7.5 / 15 / 24), 9 places
     (refs 5 / 9 / 17).
   - Longest hold 2.9 s, median 1.43 s, **0 holds over 4 s**.
   - The planner names the word starts to cut on when a hold is flagged.
2. **Set detail density** (coordinator; `dressing.ts`, `tools/look_density.py`). Measured on frames30 tiles
   (caption band masked), refs min / median / max:

   | | Edge density | Flat 6x6 blocks | Texture (mean abs Laplacian) |
   |---|---|---|---|
   | 24 refs | 0.054 / 0.092 / 0.167 | 0.13 / 0.40 / 0.58 | 7.9 / 14.7 / 24.8 |
   | Vasa v14 | 0.073 | 0.48 | 13.4 |

   - **A/B** (DressLab: the same 4 sets and cameras, bare against dressed):
     - edge density 0.045 → **0.074** (+63 %);
     - texture 6.9 → 10.4;
     - flat share 0.72 → **0.55**.
   - The deck (0.061 → 0.096, flat 0.64 → 0.50) and the gear room (0.071 → 0.130, flat 0.54 → 0.24) reach the refs'
     median.
   - The lamp room (0.044 → 0.060) and the night sea (0.005 → 0.009) stay short: they need more set dressing, not
     just texture.
   - The KitLab reel overall stays at 0.075 / flat 0.51, because it is mostly inserts and big character close-ups.
3. **Character framing** (coordinator; `castframe.ts`, `tools/cast_check.ts`). Measure: lead head height ÷ frame height.
   - **Refs:** marked by hand on 120 gridded frames30 samples (5 per ref). With a character on screen the median is
     **0.08** (per-video medians 0.035 / 0.08 / 0.25); 47 % of samples are ≥ 0.07; 29 % have no character.
   - **Vasa v14:**
     - by hand, 10 samples: 0.015;
     - projected from its story file: median **0.028**, 29 % ≥ 0.07;
     - 8 of 14 groups are specks (< 0.05): test, guns, wobble, launch, gusts, sinking, ballast, warning.
   - **KitLab v4 with `castKey` presets** (close 0.20, medium 0.11, wide 0.06): median **0.137**, 82 % ≥ 0.07.
   - An automatic head finder was tried and dropped: it found only about half of KitLab's projected heads.
4. **Acting on the word** (`actor.tsx`, `acting.ts`).
   - The Actor has 27 whole-face drawings swapped on one frame, no idle breathing, and no lip-sync.
   - Lead face track: 14 held swaps in 15.8 s on screen = **8.8 per 10 s** (rule-book estimate 3-10). Holds are a
     median 36 f, min 6 f (refs typical 6-40). There are 2 reaction runs of 2 f, and no 5-frame strays.
   - Blinks are closed 2 f (refs 1 / 2 / 4), 2.1-7.2 s apart and irregular (refs about 2-10 s).
   - Marks seen on screen: sweat, tears, steam, blush and a purple head fill (rises over 6 f).
   - Prop follow-through: the dangling key and lantern swing, the hammer, a sailor's hat pop, and the bell-rope tassel.
5. **Ghost-free joins** (`EpisodeNext.tsx`, `match.ts`). The reel has 7 whips, 2 match dissolves, 2 push-throughs
   (eye → X-ray, window → sea) and 2 frame-in-frame joins (outOf, into).
   - **Global blend detector** (frame j ≈ a·F(j−5) + (1−a)·F(j+5)): **0 blend frames in v4**. As controls,
     story-vasa v1 (opacity dissolves) gives 37 and v10 (kit whips) gives 3.
   - **Pixel "mixed" share** inside each join window:
     - match dissolves max 0.04 / 0.30;
     - push max 0.19 / 0.27;
     - frame-in-frame max 0.13 / 0.16;
     - kit whips max 0.37-0.67 (their blur);
     - a synthetic 7-frame cross-dissolve of the same frames reads 1.00.
   - Match anchors land on the same screen spot within 1 px (key bow → stone; drawn gear → gear).
6. **Effects** (`fx2.ts`). There are 11 cued effects in 37 s:
   - 4 glints (grow 2 f, shrink 2 f);
   - 2 bursts;
   - 1 debris throw (28 splinters, gravity and a bounce);
   - 2 rolling counters;
   - 1 scan-line reveal (9 f);
   - 1 puff.

   That is about 18 per minute, above the rule book's 3-10 estimate, as befits a lab. No screen shake.
7. **Reference captions, opt-in** (`captions.tsx`; the default stays the house style).
   - 76 pages, 100 % with ≤ 3 words (1.78 on average: 27 one-word, 39 two-word and 10 three-word pages).
   - Page length 6 / 12 / 28 f (refs 1 / ~10 / 35). 0 pages end on a function word.
   - Fixed y 0.71, mixed case, hard swaps from frame 0 to the end.
   - Caption over the lead's face: 19 frames. 17 of them are the push into her eye, where the face *is* the frame;
     2 are at the window.
8. **Light arc** (`lightarc.ts`).
   - 6 light states: golden, day, museum, night, explain (night-blue X-ray), dawn.
   - 2 in-shot relights: night → dawn over 24 f, day → golden over 15 f.
   - Keyword events: an alarm wash on "stopped." (pulsing every 6 f for 1 s), a 2-frame flash on "hammered", and a
     glow ramp on "dawn.".

**Verdict.** Every piece works and measures inside the reference ranges where a range exists. Open items:
- **Ink and soft edge** are out of range kit-wide (ink 0.47 against ≤ 0.34; soft 0.16 against ≥ 0.26 at 240p): the
  Stage's lens blur is fixed at cInf 10 and the ink is wide. This needs the kit change in INTEGRATION.md (per-group
  lens strength) once the kit is free.
- **frames30 jumps** are 16 (inside the 0-26 range, above the newer refs' 0-11). They come from the fast X-ray glide
  (673-678), the eye push's last frames and the match reveals.
- **Detail:** dressing lifts a set to the refs' median, but rooms and night seas need more props than KitLab gives them.

## 2026-11-02 ~15:50 UTC: kit integration of src/next, gates, and the story-vasa v15 regression

**What changed in the kit.** Commits b87637b, ad1d196 and be61972; details are in
`experiments/three-lane/src/next/INTEGRATION.md`.
- **The Actor** is Stage's default character (`classic: true` keeps stick/Person).
- **Lens:** `GroupSpec.lens` sets the blur per group, and the kit default goes from cInf 10 to 12.
- **Light** accepts preset objects.
- **Joins:** the match, push, into and outOf joins live in Episode3D.
- **The whip** no longer fades the incoming shot in during its overlap frames. It wipes the shot in behind a feathered
  edge over 5 frames (60 %-wide band).
- **Reference captions** stay opt-in (`captions="ricks"`). The owner hasn't decided.
- **Sky and water:**
  - The sky dome and a ring of inked clouds follow the camera inside the 400 m far plane. A 1200 m dome had been
    clipped all along, so Vasa's skies were the flat background colour.
  - Wave strokes scroll over any `extra.water`.
- **Labels:** world labels are kept at least 64 px tall.
- **Gates** (`kit/gates.ts`): no hold over 4 s, no speck figures, nothing cut by the edge, and HUD readouts never
  backwards (`kit/hud.ts` has `progress` / `steadyGauge` to build them).
  - They fail the render in Episode3D; Vasa3D and Turk3D are set to warn.
  - `scripts/framing.ts` runs the same gates and exits 1 on a failure.

**Is the 240p ink / soft-edge miss real?** A resolution and encoder check says it isn't a real look gap. I measured
look_stats on the same video three ways:

| Copy | Vasa v15 ink · soft · acutance | KitLab v4 ink · soft |
|---|---|---|
| 720p | 0.585 · 6.7 % · 0.369 (8 refs: 0.54-0.66 · 3.8-14.6 % · 0.32-0.42) | 0.66 · 2.6 % |
| Clean 240p | 0.36 · 0.22 | — |
| YouTube-like 240p (bicubic, 120 kb/s) | 0.28 · 0.46 · 0.185 (24 refs at 240p: ≤ 0.34 · 0.26-0.55 · ~0.19) | 0.42 · 0.42 |

- The 24 references only exist as YouTube 240p encodes, so ink and soft edge are compared at 720p against the 8 refs.
- There, Vasa is in range. KitLab still has too little lens blur (soft edge 2.4 %); the per-group lens is its fix.

**Regression: story-vasa v15 re-rendered on the integrated kit.**
- Mac, 1862 frames, about 7 min (0.22 s/frame), niced 15, under the render lock. No mosaic frames.
- Its storyboard and story file are unchanged; `episodes/*` was only read.
- File: `experiments/three-lane/out/kitlab/vasa_v15kr.mp4` (not committed).
- Both videos were measured with the same tools:
  - 720p copy against the 8 refs (the PARITY_LOG method);
  - 240p copy against the 24 refs (the rule book method).

| Check (720p, 8 refs) | Range | v15 original | v15 on the kit |
|---|---|---|---|
| hard cuts | 0-3 | 1 | 1 |
| frames30 jumps | 0-12 | 7 | 12 |
| moving % · median px/f | 96.4-100 · 5.8-11.1 | 99.9 · 6.35 | 100 · 6.96 |
| moves / 10 s | 5.1-9.6 | 9.83 (high by this measure; PARITY_LOG's method read 8.86) | 10.6 (high) |
| quiet zoom % | 69-88 | 82.2 | 82.9 |
| saturation · colourfulness | 0.41-0.61 · 23-34 | 0.564 · 29.2 | 0.563 · 27.9 |
| luma p50 · non-ink p5 | 0.31-0.58 · 0.09-0.23 | 0.316 · 0.138 | 0.321 · 0.141 |
| shadow chroma | 9-35 | 20.5 | 20.5 |
| ink · soft · acutance | 0.54-0.66 · 3.8-14.6 % · 0.32-0.42 | 0.585 · 6.7 % · 0.369 | 0.556 · 6.6 % · 0.368 |
| blend (dissolve) frames | — | 4 (two kit whips) | **0** |

- **At 240p** against the 24 refs, the regression is in range on every camera, pace and look check:
  - transitions 15.5/min;
  - shot length median 3.3 s, longest 8.0 s;
  - moves 9.99 per 10 s;
  - snaps 3;
  - jumps 12.

  The exceptions are ink and soft edge, as above.
- **Whip tuning, measured on Vasa:**
  - a hard 3-frame wipe gave 16 jumps;
  - a 40 % feather over 3 frames gave 15;
  - the shipped 60 % feather over 5 frames gives 12.

  Per-frame change at the 9.07 s whip: the opacity fade gave 35 / 23 / 23, the hard wipe 27 / 40 / 31, so the
  change has to be spread over more frames.
- **Gates on Vasa** (the warn report). Vasa is final, so it was not changed:
  - **cast:** 9 speck groups — test, guns, wobble, launch, gusts, sinking, ballast, warning, warning2 (median head
    0.023, 29 % ≥ 0.07);
  - **edge:** 10 cuts — the launch crowd at 22.2 s, gusts at 26.0 s, the hearing figures at 37.7-40.3 s, the admiral
    at 61.7 s;
  - **hud:** the heel gauge reverses 19 times;
  - **hold:** clean.

  These are the round-4 panel's own flaws: small sailors, the crowd cut, the gauge reading backwards.
- **KitLab passes every gate.**

**KitLab v7 on the finished kit.**
- **File:** `experiments/three-lane/out/kitlab/kitlab_v7r.mp4`, with phone copy `kitlab_v7_phone.mp4`. One mosaic
  frame was repaired.
- **Against the 24 refs (240p):** in range on transitions (22.8/min), shot median (2.3 s), moves (8.9 per 10 s) and
  jumps (15). The longest shot is 4.3 s, just under the refs' minimum of 4.7 s: the 4 s rule does that.
- **Against the 8 refs (720p):** five checks are out:
  - jumps 15 (max 12);
  - colourfulness 22.9 (min 23.3);
  - luma 0.31 (min 0.314);
  - ink 0.658 (max 0.657);
  - soft edge 2.5 % (min 3.8 %).

  These are lab-content effects (night rooms, flat inserts, close-ups at a fixed focus), not kit regressions. Vasa on
  the same kit is in range on all of them.
- **0 blend frames.** The whips' mixed-pixel share fell from 0.37-0.67 to 0.19-0.30.

## 2026-11-03 ~04:15 UTC: kit round 2, craft and faces (owner priority: the face), Barca benchmark

Commits 4d3dd37 (library, lighting, density, kneel, arms, still gate), dd51a78 (faces), bc3a916 (craft round 4) and the
commit that adds this entry (still-gate fix, Barca mechanism move, docs). Kit usage is in
`experiments/three-lane/src/next/INTEGRATION.md`, "Round 2 kit additions".

**Built.**
- **CC0 model library:** 38 Poly Haven models, geometry only, fetched from the official API by
  `scripts/fetch_models.py`, licences in `public/models/ph/LICENSES.md`. Every model is restyled to our look with painted
  materials (`kit/models.ts`). Built pieces are in `kit/architecture.ts`. Kenney (403 to scripted requests) and
  Quaternius (itch.io browser flow) were not scraped.
- **Light and post:**
  - soft PCF shadows;
  - `sun: "auto"` side key;
  - hemisphere fill and rim in the two-tone shader;
  - NEUTRAL tone map;
  - **selective** bloom (set glows and `userData.bloom` only);
  - SSAO available per group but off (it put grain on the heads).
- **Density presets** (`kit/density.ts`): `fill` and `crowd`, with `campLow` for foregrounds.
- **Actor:** a real kneel, and arms inked as one silhouette with the hand.
- **Visible-change gate:**
  - `still` in `kit/gates.ts`, plus `scripts/visible_change.py` on renders (calibrated on the 8 refs: their 2 s windows
    never have a median frame difference under 1.5);
  - Barca showed the gate was blind to two cases, both now fixed: a camera drift that a 4 m grid overstated (the grid
    now sits at the subject's depth), and small figures acting (only figures at least 0.2 of the frame height count).
- **Bricks:** `box(..., uvTile)` gives world-scaled bricks.

**Faces (owner priority).**
- **Study:** `src/next/tools/face_study.py`, 103 reference heads, numbers only kept. Medians (IQR):
  - aspect 1.15;
  - outline 5.8 % of D (4.1-7.2);
  - lit 0.97, darkest 0.87 (0.78-0.90), darker toward the lower right (47°);
  - eye height 0.157 D, eye gap 0.235 D, eye stroke 0.072 D, brow stroke 0.061 D.

  Radial profiles of the matched ref crop showed the lit head is clipped white (255) with a cool grey crescent away
  from the light.
- **Rebuild:**
  - card rasters scale with their size on screen (close-ups were upscaled ~3x, so lines went soft and the grade
    tinted the edges navy);
  - the head is shaded in the card shader as a sphere: its target output is inverted through the tone map so the lit
    side is white, with a cool crescent toward a blend of the key and an upper-left studio light;
  - near-black ink everywhere;
  - an organic head with a tapered outline;
  - plain oval eyes, curved lids, arched tapered brows and tapered mouths;
  - soft contact shadows under hats and hair;
  - a soft cheek tint (a one-line removal in `actor.tsx` if the owner dislikes it);
  - the soft cap and the messy hair redrawn;
  - all 27 expressions kept.
- **Measured on the final smith close-up:** lit 0.988, darkest 0.859, gradient strength 0.070 (ref median 0.069),
  outline 4.7 % of D (in the IQR).
- **Blind face A/B:** our face against the matched ref (Mz72 10.7 s) at matched head scale, hidden A/B order, fresh judges;
  two judges per round from round 10.

| Round | Same tier (ours ≥ ref) | Note |
|---|---|---|
| 1-7 | 0 of 2 each | conf 4-5 → 3; grain, lavender cast, navy rings, double brows, flat head |
| 8 | 1 of 2 | smith same tier |
| 9-11 | 0 | flat head, hat pasted on, white notches |
| 12 | 1 of 4 | |
| 13 | 2 of 4 | one judge: both pairs same tier |
| 14-15 | 0 of 4 | conf 2-3, "close to same tier" |
| 16 | 2 of 4 | smith same tier for both judges |
| 17 | 0 of 4 | conf 2-3; a lid-patch artefact (fixed after) |

  Not same tier in most pairs yet. The cap character still loses on "the beanie looks pasted on", and some judges
  still find the line weight uniform. Stills: `scratchpad/kitlab/face/faces_after_sheet.jpg` (session scratch).

**Craft loop (4 Barca shots against matched ref frames, blind, craft only).**

| Round | Wins | Note |
|---|---|---|
| 0 (v14) | 1 of 4 | macro ours |
| 1-3 | 1 of 4 | |
| 4 (two judges) | 1 of 4 both | |

- The macro wins; hook, wall and section lose with confidence 3-4.
- The remaining notes are mostly lighting mood and composition:
  - flat daylight against the refs' night scenes with lanterns;
  - empty sky;
  - the section's dark bottom band and plain back wall;
  - small figures in the section.

  Those are story-file choices (light presets, cameras); the kit can now do them (glows bloom, light arcs, night presets).
- A global cosine-modelling increase was tried and reverted (no visible gain).

**Barca benchmark on the upgraded kit.**
- **Render:** Mac, niced, under the lock, about 3.5 min. One mosaic frame was repaired. Audio is muxed from v14.
- **Files:** `experiments/three-lane/out/kitlab/barca_r2.mp4`, phone copy `barca_r2_phone.mp4` (13.5 MB). Not
  committed.
- **Gates:** clean (20.8 place changes/min, 11 places, longest hold 3.89 s, cast median 0.117, 63 % ≥ 0.07).

| Check (720p, 8 refs) | Range | v14 | r2 |
|---|---|---|---|
| hard cuts · jumps | 0-3 · 0-12 | 2 · 7 | 2 · 6 |
| moving % · median px/f | 96.4-100 · 5.8-11.1 | 98.8 · 6.69 | 99.5 · 6.78 |
| moves / 10 s | 5.1-9.6 | 10.4 (high) | 10.4 (high) |
| quiet zoom % | 69-88 | 81.1 | 90.6 (high; 24 refs: up to 96.8) |
| saturation · colourfulness | 0.41-0.61 · 23-34 | 0.501 · 23.5 | 0.406 · 21.6 (both low; in the 24-ref range) |
| luma · non-ink p5 · shadow chroma | 0.31-0.58 · 0.09-0.23 · 9-35 | 0.519 · 0.225 · 16.1 | 0.471 · 0.131 · 16.8 |
| ink · soft · acutance | 0.54-0.66 · 3.8-14.6 % · 0.32-0.42 | 0.596 · 6.0 · 0.331 | 0.636 · 4.8 · 0.336 |
| visible change p5 · p25 · quiet share · still windows | refs p5 ≥ 1.75 | 1.83 · 2.68 · 0.205 · 0-2.3 s, 9.7-12.8 s | 2.14 · 2.97 · 0.117 · none |

- **At 240p against the 24 refs:** everything is in range except ink and soft edge, the known encoder artefact.
- **Saturation:** the drop comes from the whiter heads and paler sand. One small fix is lifting the Barca world
  saturation.

## 2026-11-03 ~07:00 UTC: round 3: replication lessons in the kit, and camera smoothness

The test bed is the VS1Z 20 s replica (internal study only). Renders v4-v10 are in `out/study/VS1Z/renders/`, the
sheets in `out/study/VS1Z/compare/v4`-`v10`, and the three-way side-by-side (reference | v3 | v10) is
`out/study/VS1Z/VS1Z_side_by_side_v10_phone.mp4` (9.8 MB). Everything was rendered on the Mac at concurrency 1, niced,
under the lock. Kit usage is in INTEGRATION.md, "Round 3 kit additions".

**Look (lessons 1-4).**
- **Hero props:**
  - sculpted gold dragon heads in a real metal (scale normal maps, spec, a painted env);
  - a cast-relief jar;
  - toads and bronze orbs.
- **Interior kit:**
  - fluted columns with gold capitals, pointed arcades, a rose window, banners, a carved gold throne;
  - runners and candelabras;
  - a `candle` preset measured on the master's hall (mean RGB 133/112/100, luma p10/p50 60/113), a warm key over
    grey-lavender stone.
- **Depth:** bokeh discs and a foreground-mass helper.
- **Costumes:** court costumes with trims, crossed collars, patterns, robes, sashes, lamellar armour, a guan and a mian.
- **Colour:** v4 went too warm and dark (hook luma p50 56 against 113). It was re-measured and corrected in v5. The
  hook's colour, measured as mean RGB and luma p10/p50: master 133/112/100 and 60/113; v3 110/79/76 and 26/84; v4
  100/65/45 and 29/56; v10 137/104/93 and 49/108.
- **Block dE stays 29-35:** it is dominated by layout (our own sets by design), so it is not a useful look target here.

**Per-shot match** (0.7 × judgement + 0.3 × measured; framing, props and look come from one fresh blind judge who saw v3
and v10 side by side against the reference):

| Shot | v3 (study's own score) | v3 (blind judge) | v10 | Props / look, v3 → v10 |
|---|---|---|---|---|
| 1 hook take | 7.0 | 6.7 | 7.1 | 3/4 → 6/5 |
| 2 warning, travel, laugh | 7.3 | 6.6 | 6.3 | 3/4 → 4/4 |
| 3 jar orbit to frog | 5.7 | 5.7 | 6.0 | 3/4 → 6/5 |
| 4 balcony crane | 6.4 | 6.0 | 6.5 | 4/4 → 4/4 |
| 5 weeks later | 6.2 | 5.7 | 5.9 | 3/4 → 5/5 |

- **Below target.** No shot reaches 8. With SSIM ~0.2, the measured term caps a shot near 7.5 even at an 8.5 judgement.
- **Remaining look gaps (judge):**
  - the dragons read dark bronze against the master's bright polished gold;
  - shot 2's bell falls to silhouette in the wide;
  - the balcony has no painted town or spires;
  - the throne room is plainer.
- **Judge variance:** an earlier judge rated v9 look 6 on shots 1-3 and 5.

**Camera smoothness (owner).**
- **Tool:** `scripts/cam_smooth.py`. Per-frame raw motion from camera_motion.py (translation, zoom, roll at 720 px),
  with speed, acceleration, jerk, velocity steps, ramps and hold jitter. The cuts, dissolves and speed-line frames are
  left out for both videos.
- **Where ours was rough (v3):**
  - one-frame starts and stops at key joins: lin → io and in/out segments; the crane start 1.4 → 55 px/f at F59; the
    stop 33 → 2 at F171; the fly-past start 7 → 58 at F159;
  - not jitter: our holds were steadier than the master's.
- **Fix (`kit/campath.ts`):**
  - every path is filtered in time by a Gaussian of 4 frames, so velocity and acceleration are continuous;
  - snaps (`ease: "snap"`, `sharp`) keep their own window, and the filter never reaches across them;
  - `soft: n` widens a long fly-past;
  - aim is slerped on the position's ease;
  - camera motion blur comes from the path's real per-frame motion (`kit/camblur.ts`, 180° shutter).
- **Gate:** `smooth` in `kit/gates.ts`. No velocity step above 44 px/f² at 1080 (the master's max, 29.5 at 720) outside
  snaps and joins, and hold reversals ≤ 10 %. The study and Barca both pass.

| Measure (720 px) | Master | v3 | v9 | v10 |
|---|---|---|---|---|
| accel p50 / p95 / p99 / max | 0.70 / 13.9 / 24.0 / 29.5 | 0.19 / 10.7 / 29.4 / **55.1** | 0.24 / 8.1 / 18.5 / **26.7** | 0.25 / 8.2 / 18.3 / 31.9* |
| jerk p50 / p95 / p99 / max | 0.99 / 16.0 / 30.8 / 53.2 | 0.32 / 7.8 / 29.5 / **71.6** | 0.31 / 8.8 / 23.5 / **31.8** | 0.33 / 8.0 / 22.6 / 56.2* |
| velocity steps | 57 | 37 | 35 | 31 |
| hold jitter (mean accel) · reversals | 0.39 · 4.9 % | 0.16 · 0 % | 0.16 · 0.6 % | 0.18 · 0.6 % |

\* v10's camera is the same as v9's. Its max is a single-frame phase-correlation spike at F199 (15.8 → 32.2 → 11.1 px/f),
not a camera step.

- **Still outside the master's range:** the median attack and release of the measured moves. These are unreliable:
  our fast moves border frames the fit cannot solve.

## 2026-11-03 ~08:30 UTC: round 3: world building and the shot-3 pass

**Detail by region.**
- Measured with `scripts/detail_gate.py` on VS1Z F0-F599, every 10th frame.
- Each value is a median; the reference's run is `out/study/VS1Z/detail_ref.json`.

| Region · measure | Master | v11 (before) | v13 (world-built) |
|---|---|---|---|
| hero edge · texture | 0.145 · 24.8 | 0.126 · 18.1 | 0.129 · 21.1 |
| background edge · texture | 0.122 · 16.5 | 0.072 · 9.6 | 0.106 · 10.8 |
| midground edge · texture | 0.098 · 13.8 | 0.090 · 9.9 | 0.105 · 12.9 |

- **Gate (80 % of the master's median):**
  - v11 failed four checks: hero texture, background edge and texture, midground texture.
  - v13 fails one: background texture, at 65 %.
- **Hand counts on 6 matched frames (master / v11 / v13):**
  - objects: F12 16/12/15, F175 10/6/6, F290 28/22/30, F560 20/12/18;
  - balcony object kinds: 20/10/14;
  - moving background things: the master has flames and in-place reactions; v13 adds 3 walking servants, 4 shifting
    courtiers, birds, smoke and flags.

**What moved the numbers.**
- Smaller stone courses, finer floor tiles, stone columns and less lens blur in the hall: background edge went 0.074
  (v12, dressing only) → 0.106.
- The dressing itself (tapestries, shelves, plants, chandeliers, extras, the painted town) added objects but little
  measured edge, because it sits in the blurred background.

**Still short.**
- **Background texture** (65 %): the master's walls and windows carry painted fine detail.
- **The emperor close-up's throne:** a flat panel hides the carved throne.
- **The balcony's painted mountains** are covered by the town card's haze band.

**Shot 3, pass 2.** Start at −40°, a lens push to the dragon, then a lens tilt to the frog from the same spot.
- Vertical correlation with the master is now positive (0.41; it was −0.28).
- Within 1 frame: orbit start (227 / 228) and zoom start (251 / 251).
- Late: orbit end and push start, 12 frames each.
- Tilt: it starts 8 frames early and is about a third of theirs (−3.4 / −1.1 against −12.1 / −9.0 px/f).

**Camera smoothness (v13 against the master).**
- Accel max 30.9 (master 29.5).
- Jerk max 28.8 (master 53.2).
- Hold jitter 0.18 (master 0.39).

## 2026-11-03 ~09:30 UTC: round 3 pilot: Codex key frames as targets, 2.5D projection, a code-sculpted SDF dragon

The owner's rule is that everything is built in code. The Codex key frames are the reference.
`experiments/asset-gen/gen_one.sh` now takes the newest `~/.codex/generated_images` file. The hook's key frame is
`experiments/asset-gen/gen/kf_hook_shot1.png`. The side-by-side (theirs | key frame | 2.5D | code) is
`out/study/VS1Z/VS1Z_pilot_keyframe_side_by_side_phone.mp4`.

**Main path: the hook in code.**
- **Dragon:** `scripts/sdf_dragon.py` sculpts the head as signed distance fields:
  - cranium, snout, nose pad, lips, brows and cheeks;
  - an open jaw with the mouth cavity cut;
  - segmented horns, a mane, beard fins, a crest and an S-curved neck.

  It uses smooth unions and is meshed with marching cubes (83k triangles). It carries a gold scale normal map and our
  ink, and `kit/codemodels.ts` places the teeth, eyes and whiskers at its anchors.
- **Foreground:** world-placed props after the key frame (candles in a bowl, an incense burner, a table with scrolls and
  a brush pot).
- **Hook detail (F0-F58):** hero edge and texture 0.140 · 18.8. That matches theirs (0.138 · 19.1); v13 was 0.128 ·
  17.3. It is well under the key frame (0.194 · 29.4).
- **Motion:** shot-1 correlation 0.77.

**Trial: key frame + depth (2.5D).**
- **Build:** Depth Anything V2 small (official weights, run on MPS) gives depth. A camera-space grid is textured from
  the key camera (`kit/plate.ts`, `scripts/kf_depth.py`, `scripts/kf_plate.py`), and our live inventor card stands on
  the painted one.
- **Measured limits** (share of the frame stretched beyond rigid magnification · frame coverage):
  - push 0.1 m: 2.9 % · 100 %;
  - orbit 1° (about 3.2 m): 7.6 % · 97.6 %;
  - truck 5 cm: 6.3 % · 97.6 %;
  - tilt 1°: 0 % · 97.6 % (the plate's edge shows);
  - zoom: never stretches, but a 941 px key frame is upscaled 2.9× at a 2.5× lens push.

  So the hook's 3× push works only as a lens push (zoom) plus about 0.1 m of dolly, and the crane over the jar is out
  of reach.
- **Hook detail:** 0.160 · 19.9 on the hero, and 0.161 · 15.7 on the background (closest to the key frame).

**Shot 3 with the SDF dragons.**
- The orbit is unlimited in full 3D.
- Region detail is under v13's procedural head (hero texture 14.8 against 21.0; theirs 21.2): the heads read dark in
  the orbit's shade.
- Motion correlation is unchanged (0.11).

## 2026-11-03 ~10:30 UTC: the code path: dragon fix, and the Myeongnyang v3 hook built in code

**Owner decision.** Full code with SDF-sculpted props; no 2.5D for now.

**Dragon fix** (VS1Z hook, F0-F58, `out/study/VS1Z/renders/ours_hookfix.mp4`):
- a shorter, rising snout and a big nose bulb;
- the jaw opened wider and the ball brought forward into it;
- larger, brighter scales (6 rows, `#ffcf4a`, roughness 0.24);
- an unshadowed hero fill light that only the PBR metals see.

Hook detail moved from 0.140 · 18.8 / 0.108 · 10.9 to 0.143 · 19.7 / 0.120 · 12.7 (hero · background, edge · texture).
Theirs is 0.138 · 19.1 / 0.068 · 10.0; the key frame is 0.194 · 29.4 / 0.186 · 19.8.

**Myeongnyang v3 hook** (`src/study/myeong/hook.tsx`, composition `MyeongHook`, 3.7 s).
- **Reference:** `experiments/asset-gen/gen/kf_myeong_v3.png`. A Codex key frame from our style board, with East Asian
  warships (a panokseon bow and atakebune), dusk, an anonymous admiral letting the anchor go.
- **The code build:**
  - the episode's strait world (cliffs, current streaks, whirlpools, the Japanese fleet with lanterns), used read-only;
  - the bow deck, the painted hull and rail, a carved SDF dragon post (lacquer), dark dusk water;
  - the anchor (wood and riveted iron) with its chain and rope mid-drop, a splash (spray, foam ring, burst);
  - laughing sailors on the near enemy decks;
  - the admiral framed by subject, with the camera already moving at frame 0.
- **Render:** `experiments/three-lane/out/kitlab/myeong_hook_v2.mp4`.
- **Detail against the reference** (edge · texture):
  - hero 0.108 · 11.8 against 0.255 · 32.5;
  - background 0.060 · 6.9 against 0.187 · 24.3;
  - midground 0.043 · 4.0 against 0.276 · 34.8.

  That is about 1/3 to 1/8 of the reference.
- **Short of the reference:**
  - the composition: our camera runs along the hull, so the rail fills more of the frame as the push goes on;
  - the cliffs are low green hills, not rock walls with pines;
  - the sky is a flat dusk gradient with no cloud bands;
  - the water has streaks but no foam crests or depth;
  - the enemy ships are coarse boxes with plain banners;
  - the admiral is smaller (head 0.15 against 0.2) and his rope hand is not on the rope.

Side-by-side (the VS1Z hook fix, then the Myeongnyang reference and ours):
`out/study/VS1Z/round3_codepath_side_by_side_phone.mp4`.

## 2026-11-03 ~11:00 UTC: Myeongnyang hook pass 2 (camera, admiral, sky, foam, cliffs)

**Built** (`src/study/myeong/hook.tsx`):
- the admiral's head at 0.2 of the frame;
- his hand placed on the rope, computed from the card's point pose;
- a painted dusk sky with lit cloud bands;
- 260 foam crests drifting with the current;
- sculpted rock cliffs (noise-displaced columns) with pines on both shores;
- only the bow is built, so no rail runs past the lens.

**Not built:** the atakebune rework.

**Composition** (`out/kitlab/myeong_hook_v3.mp4`): it regressed.
- I tried four camera keys. Each frames his head at 0.2 from outboard of the bow, but that puts the hull and rail
  between the lens and the water: the anchor and the splash are hidden behind the hull, and the long lens leaves little
  sky.
- Pass 1 (`myeong_hook_v2.mp4`) still shows the anchor drop better.

**Detail against the reference** (edge · texture; pass 1 → pass 2, reference):

| Region | Pass 1 | Pass 2 | Reference |
|---|---|---|---|
| hero | 0.108 · 11.8 | 0.144 · 17.0 | 0.255 · 32.5 |
| background | 0.060 · 6.9 | 0.107 · 12.6 | 0.187 · 24.3 |
| midground | 0.043 · 4.0 | 0.106 · 13.5 | 0.276 · 34.8 |

The gain comes mostly from the rail and hull textures, not from the reference's content.

**The fix the reference implies.** Turn the hero ship, not the camera: lay the bow broadside across the frame
(bow toward the lens's left, the hull side facing away), with the camera low over the water off the bow's quarter. Then:
- the rail runs across the lower left;
- the water and the anchor drop fill the right;
- the fleet sits up the strait behind him.

Side-by-side (reference | pass 1 | pass 2): `out/study/VS1Z/myeong_hook_pass2_side_by_side_phone.mp4`.
