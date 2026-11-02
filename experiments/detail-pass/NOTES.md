# Detail pass: procedural generators for STYLE_BIBLE §8 density

A separate Remotion entry (`src/index.ts`) that imports `experiments/kurz-style/engine` read-only (planes, light, atmosphere, `<Shaded>`, palette). `node_modules` is a symlink to the engine's, so there is one React. Nothing in `studio/`, `pipeline/` or the engine was edited.

**Showcase:** `out/detail-pass/detail_v10.mp4` (repo root `out/`, 4 s, 1080x1920, texture pass applied). Proof images are in `proof/`; measured data is in `data/judge_v10/`.

## Generators (`src/detail/`)

| file | what it does |
|---|---|
| `scatter.ts` | Seeded placement per plane. **Families:** an anchor (rock, brain coral, vase sponge, table coral, antler coral) with 1-5 smaller satellites. **Edge bias:** p(x) ∝ (1-e) + e·\|2u-1\|^1.2. **Calm field:** an ellipse in which nothing is placed; near its feathered edge an object is rejected with probability equal to the calm weight, measured at the object's top. **Depth rows:** perspective scale and back-to-front sort. Kelp `grove()` varies height, lean, bend and blade style. |
| `species.ts`, `schools.ts`, `Fish.tsx` | 7 parametric fish body plans: scad, tang, lancer, trunkfish, anthias, wrasse and grunt. Each fish varies in depth, peak, tail, fins, colour drift and pattern. Shading is back, body and belly tones plus a lit back edge, gill, eye and pattern. Schools use a sunflower formation with per-fish heading noise, size, tail-beat phase and rate. Far schools are flat silhouettes. Also an eagle-ray silhouette. |
| `flora.tsx` | Rock (strata, algae patches, surface marks), brain coral (meander ridge-and-groove), antler coral (recursive branches), table coral, tube sponges, vase sponge, ball sponge, finger coral, varied kelp, sea grass, urchin, sea star, shell and far mound. Shading uses a mask-free **stack**: rim tone, core-shadow tone, base shrunk and nudged toward the key, then a highlight plane. That gives a hard crescent, a lit plane and a rim for 3-4 paths, with no outlines. `lod="far"` keeps L0/L1 only. |
| `Micro.tsx` | Marine snow, plankton and micro-bubbles, always on, on 3 planes so they parallax. Bean-shaped specks in 3 tints per plane. 240 rendered per frame (far 90, mid 85, near 65). |
| `marks.ts`, `SurfaceMarks.tsx` | Surface-mark generator. Input is a hero path plus the light. Clustered marks (spot groups with a ring centre, scars, dash clusters, pore clouds, scale arcs) go **only in the lit region**: the exact complement of Shaded's core-shadow mask. Marks stay off the rim crescent and the silhouette edge. Values are ±6-10 % of the base L. Glints get their own pass in the highlight plane. Seeded and cached, so marks never swim. |
| `pathgeo.ts` | Path flattening and point-in-polygon tests. Pure, so the node manifest script runs the same code. |

The hero is `src/assets/turtleGeom.ts` and `Turtle.tsx`, an original sea turtle in three-quarter dorsal view:
- **Carapace:** 5 vertebral, 8 costal and 24 marginal scutes. Costal seams radiate from the vertebral joints. Seams are pale strokes. Tortoiseshell blotches and wedges, plus a growth ring per scute.
- **Skin:** a rounded-hex scale tessellation on the head and flippers, a beak sheath and a brow plate.
- **Motion:** front flippers make a power stroke with follow-through (the tip rotates more than the root), plus a head bob.
- **Shading:** two `<Shaded>` groups with warm shadow targets, so shadows don't go muddy.

## Results (`scripts/render.sh v10` on the Spark: CPU, nice 10, concurrency 4, render lock)

Render time was 17.8 s for 4 s of video, at load 8.6.

| id | metric | Kurzgesagt W / D (env stills) | ours (orca pilot) | engine showcase | **detail_v10** | target | |
|---|---|---|---|---|---|---|---|
| D1 | shapes / frame | 137 / 112 | 116 | 186 | **204** (2 s grid: 216) | ≥ 110 | PASS |
| D2 | micro-details / frame | 633 / 658 | 584 | 1866 | **2115** (2166) | ≥ 600 | PASS |
| D3 | small specks / frame | 124 / 134 (165-371) | 63 | 266 | **582** (min 563, max 620) | ≥ 120; ≥ 150 env | PASS, above the Kurzgesagt env range (see below) |
| D4 | edge density | 0.047 / 0.042 | 0.026 | 0.061 | **0.0751** (per frame 0.073-0.077) | 0.040-0.08 | PASS, near the top |
| D5 | outline response | 0.004 / 0.025 | 0.29 | 0.020 | **0.000** | ≤ 0.05 | PASS |
| J4 | named objects in frame | 15-60 | 5-8 | - | **208 median** (200-212; 67-79 set-dressing pieces, 133 fish), **21-23 kinds** | ≥ 15 | PASS |
| J4 | hero surface marks | dozens to hundreds | 0-3 | - | **159 marks in 30 clusters**, all lit: shell 92, head 29, near flippers 38; spots 59, pores 59, dash 16, glint 11, scar 8, arcs 6 | ≥ 30 | PASS |
| §8 | calm field | 33-41 % top-cluster share | | | **34.7 %** design ellipse; top-cluster share 0.29 median (0.25-0.35); 61 % of 40 px tiles carry no edge | 30-50 % | about at the floor |

P1-P8 and M1-M5 also pass: P4 grey 0.033, P5 5 hue families, 0 cuts, 100 % frames alive. A1/A2 fail only because the clip is muted.

Named-object and mark counts come from `scripts/manifest.ts`, which runs the same layout and generator code the scene renders and projects each object through the plane camera. D1-D5 come from `kurz-style/engine/scripts/frame_judge.sh` (0.5 s grid) and `tools/house/judge_metrics.sh` (2 s grid). `tools/specks.py` is the same D3 counter, per frame. `tools/calm.py` is the edge-free tile share.

## Notes, honestly

- **D3 is about 1.6× the top of the Kurzgesagt environment range.** Ablation (v6, frame 60) shows where it comes from:
  - The micro layer itself is only about 100 of the counted specks. Far specks are under the counter's threshold.
  - The rest is small bright detail: polyp dots, branch tips, fish bellies and eyes, mark glints and sand pebbles. That is mid reef about 115, schools about 90, front reef about 75, turtle about 55 and seabed about 40.
  - To match Kurzgesagt 1:1, thin the polyp and tip dots before touching the micro layer.
- **D4 sits at 0.075.** Getting from 0.098 to there took, in order:
  - Moving the kelp groves to a hazier back plane at depth 0.45, haze 0.42.
  - Fewer and chunkier front-row corals.
  - Rims only on forms with R > 40, mixed toward the shadow tone.
  - Keeping hero internal texture (seams, scale cells, streaks) within about ±12 % L, so it reads by eye but stays under Canny's thresholds. This is how Kurzgesagt gets dense marks with a low edge count.
  - Note that `frame_metrics.py` squashes a 9:16 frame to 640x360, so vertical forms such as kelp and tubes are over-weighted.
- **The calm field is at the floor of 30-50 %.** The open-water band uses a narrow value range (`OPEN_HI` to `OPEN_LO`). Widening the gradient drops the top-cluster share to 0.20.
- **No Codex image assets were used.** Everything is procedural SVG, so it stays seeded, resolution-free and lit by the scene light. Codex-generated textures would be a later option for hero drawing, not density.
- **Still short of Kurzgesagt tier (my read):**
  - The reef reads assembled rather than illustrated.
  - The rocks are generic blobs.
  - The far mounds are plain.
  - The turtle's head has few sub-forms (no jaw or cheek mass).
  - Not judged side by side with `JUDGE_RUBRIC.md`.

## Run

```bash
rsync -a --exclude node_modules --exclude out --exclude build \
  ~/Documents/faceless-studio/experiments/detail-pass/ dgx-spark:~/studio/app/experiments/detail-pass/
ssh dgx-spark 'bash ~/studio/app/experiments/detail-pass/scripts/stills.sh v11 0 60 105'   # stills + quick metrics
ssh dgx-spark 'bash ~/studio/app/experiments/detail-pass/scripts/render.sh v11'            # video + texture pass + all metrics
ssh dgx-spark 'cd ~/studio/app/experiments/detail-pass && bash scripts/ablate.sh'          # D4/specks with one system off
```
