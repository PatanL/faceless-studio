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
