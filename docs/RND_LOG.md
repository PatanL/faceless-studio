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
