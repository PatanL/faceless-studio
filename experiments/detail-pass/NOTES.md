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

---

# Orca opening, detail pass (`src/scenes/OrcaOpenDetail.tsx`, composition `OrcaOpenDetail`)

The approved 10 s v3 opening (`kurz-style/engine/src/scenes/OrcaOpen.tsx`, `out/kurz-engine/orca_open_v3.mp4`), re-set with this folder's generators and asset-gen's path-B hero, as a fair A/B:

- **Same beats, camera and type:** the same 292 frames (9.733 s), the same four camera moves, the same caption phrases and word timings, title plate, counters, cars, YOU figure, guides and tags.
- **Same audio:** the episode's `mix.wav` muxed by the same ffmpeg step. The decoded audio of both clips has the same MD5.
- **Deliverables:**
  - `out/detail-pass/orca_open_detail.mp4` (render `r3`)
  - `out/detail-pass/sbs.jpg` (copied to `proof/orca_sbs.jpg`). Row 1 is v3 and row 2 is the detail pass, at 1.0, 3.6, 5.5, 7.2 and 9.3 s. Row 3 is Kurzgesagt `D_0126_reef`, `D_0630_dumbo-octopus` and `W_0222_whale` (environment, hero close-up, scale beat).

## What changed vs v3

**Hero.** The asset-gen path-B orca: Codex reference, then extraction, then a hand rig with the one-light shading stack and 187 measured marks (50 scars, 137 dots and pores).
- `src/assets/OrcaB.tsx` is a small **fork** of `asset-gen/orca-b/OrcaB.tsx`. The geometry JSON is still imported read-only from asset-gen.
- Fork change 1: the eye lid is clipped to the eye disc, inside a skin socket. The original drew a square skin-coloured block over the eye-patch edge, which showed at the 2× push-in.
- Fork change 2: lit-side marks are a lower value step, +0.13 / +0.20 L instead of +0.34 / +0.5. They read as texture, not as bright specks.
- `OrcaHero.tsx` rotates the screen-space light into the pitched body, so the key stays fixed, and adds seeded blinks and the menace lid.
- Scene anchors (fluke tip, snout, fin tip, back) are recomputed with OrcaB's swim-wave formula (`orcaPt`). The YOU figure is scaled so its head lands exactly on the fin tip.

**Set (FEEDBACK 2026-11-01, logical consistency).** v3 put tropical stony corals and jellies behind an orca. This is a cold-water **kelp forest over a rocky reef**:
- Golden giant-kelp columns reaching the surface, on a deep hazy plane plus the frame-edge back plane.
- Boulders with coralline-algae crusts, vase, ball and tube sponges, cold-water soft corals, a few red gorgonians, plumose anemones, urchins, sea stars, shells and surfgrass.
- Fish: herring (orca prey), surfperch, kelp wrasse and sand lance.
- **No distant pod.** At far-plane size their silhouettes read as sharks, and the owner has ruled out background sharks.
- All placement is `scatter.ts` (families, edge bias, a calm ellipse around the hero's swim path) from pure data in `orcaLayout.ts`. `scripts/orca_manifest.ts` counts from the same data.
- `VarKelp` gained an optional `blade` colour.

## Metrics (render `r3`; v3 measured with the same tools in the same session)

`frame_judge.sh` on a 0.5 s grid (19 frames) and `judge_metrics.sh` on the 2 s grid. Data: `data/orca_r3/`, `data/orca_v3ref/`.

| id | metric | Kurzgesagt W / D (env) | ours (orca pilot) | v3 (same tools) | **detail pass r3** | target | |
|---|---|---|---|---|---|---|---|
| D1 | shapes / frame | 137 / 112 | 116 | 190 (2 s: 203) | **215** (2 s: 199) | ≥ 110 | PASS |
| D2 | micro-details / frame | 633 / 658 | 584 | 1834 (1891) | **1896** (2000) | ≥ 600 | PASS |
| D3 | small specks / frame | 124 / 134 (165–371) | 63 | 285 (159–367) | **406** (227–471; 2 s: 404) | ≥ 120, ≥ 150 env | PASS the floor, about 10 % above the Kurzgesagt env top |
| D4 | edge density | 0.047 / 0.042 | 0.026 | 0.0699 | **0.0677** (0.054–0.086; 2 s: 0.0686) | 0.040–0.08 | PASS |
| D5 | outline response | 0.004 / 0.025 | 0.29 | 0.042 (2 s: 0.037) | **0.051** (2 s: 0.052) | ≤ 0.05 | FAIL by 0.001–0.002; see below |
| J4 | named objects / frame | 15–60 | 5–8 | – | **124 median** (60–147; 38–97 fish), **18 kinds** | ≥ 15 | PASS |
| J4 | hero surface marks | dozens–hundreds | 0–3 | ~40 | **187** (dots 137, scars 50; body 115, near flipper 33, dorsal 31) | ≥ 30 | PASS |
| §8 | calm field | top cluster 33–41 % | | 0.187 | **0.254** top cluster; 65 % of 40 px tiles edge-free; design ellipse 39.9 % | 30–50 % | top cluster below range |
| P4 / P5 | grey / hue families | | | 0.050 / 3 (2 s: 0.055 / 2) | 0.051 / 2 (2 s: 0.065 / 2) | ≤ 0.04 / ≥ 3 | both FAIL (v3 also fails P4) |

Render on the Spark: CPU, nice 10, concurrency 4, render lock. **29.1 s for 9.7 s** of video (3.0 s per second of video) at load 3.4–10.8, plus 2.9 s of texture and mux. v3 took 41.9 s.

**Reading.**

- **D5 is the type, not the art.** The blackhat line map shows the hits on the caption stroke, the title plate, the YOU and FIN tags and the diver.
  - With `--props '{"off":["type"]}'`, D5 is 0.016–0.022 at frames 30, 120 and 270. With type it is 0.047–0.052.
  - The type is identical to v3. Our open-water band is a little lighter, so the black caption stroke clears the 45 L* blackhat threshold more often.
  - The remaining non-type hits are the dark sliver between OrcaB's bone patches and its belly rim.
- **D3 is about 10 % above the env range.**
  - Speck maps put about 100 counted specks on the orca's marks. These are the hero marks Kurzgesagt also carries.
  - The rest comes from herring, micro, kelp and the reef.
  - Already cut while iterating: the herring school, far schools and micro (45 / 45 / 32), plus the lower mark tone. The stills median was 371, but x264 and the texture pass add about 35.
- **D4 sits mid-range.** The kelp forest was the edge driver: 0.12 on the first stills. Thinning the groves, moving the columns to a hazier depth-0.2 plane and lowering the mid-reef anchor count brought it down.

**My read side by side (`sbs.jpg`):**

- **Better than v3:**
  - The hero has a real head mass, teeth, eye socket, saddle and rake-mark texture.
  - The set makes sense for an orca.
  - The upper frame is no longer empty, because the kelp columns and herring reach it.
- **Worse than v3:**
  - Colour breadth. The cold set is teal plus golden kelp, and the warm reef masses mostly sit off-frame below the captions (P5 2).
  - The boulders read as plain loaves.
- **Against the Kurzgesagt reef (`D_0126`),** both are far less saturated and less layered.
- **Next levers:**
  - A sunlit golden-kelp canopy mass near the top (warm family, calm-field share).
  - Coralline-pink and purple-urchin accents on the boulders.
  - Fixing the bone-patch sliver in `OrcaB`.
  - Darkening the caption stroke halo, or using a softer caption plate, to pull D5 under 0.05.

## Run

```bash
rsync -a --exclude node_modules --exclude out --exclude build ~/Documents/faceless-studio/experiments/detail-pass/ dgx-spark:~/studio/app/experiments/detail-pass/
rsync -a ~/Documents/faceless-studio/experiments/asset-gen/orca-b/orca_geom.json dgx-spark:~/studio/app/experiments/asset-gen/orca-b/
ssh dgx-spark 'bash ~/studio/app/experiments/detail-pass/scripts/orca_stills.sh s9 0 60 105 150 195 240 288'  # stills + quick metrics
ssh dgx-spark 'bash ~/studio/app/experiments/detail-pass/scripts/orca_render.sh r4'                           # video + mix + all metrics
ssh dgx-spark 'cd ~/studio/app/experiments/detail-pass && FRAME=60 bash scripts/orca_ablate.sh'               # D4/D5/specks per system
python3 -I scripts/orca_sbs.py ../../out/detail-pass/sbs.jpg ../../out/kurz-engine/orca_open_v3.mp4 ../../out/detail-pass/orca_open_detail.mp4 1.0,3.6,5.5,7.2,9.3 <ref stills...>
```

`remotion.config.ts` aliases `react` and `react-dom` to this project's copy, and `tsconfig.json` maps their types. That way the JSON and any code imported from outside the entry folder never pull in a second React.

---

# Judge verdict: `orca_open_detail.mp4` (r3) vs v3 (59)

Strict pass with `kurz-style/JUDGE_RUBRIC.md` (revised identity gate), 2026-11-01. Judged from frames, not descriptions:
- full-res frames of both clips at 0, 1, 2, 3.5, 5, 6.5, 8 and 9.6 s, side by side;
- 2× crops of the hero head (3.5 s) and tail (5 s) next to v3's;
- 0.25 s strips over 2.0–4.0 s and 6.5–8.5 s;
- the Kurzgesagt targets `D_0126_reef`, `D_0056_shallows-sub`, `W_0222_whale` and `D_0630_dumbo-octopus`.

The metrics are `data/orca_r3/` and `data/orca_v3ref/`. I did not re-run them.

**Checks I did re-run:**
- Both clips decode to **291 frames / 9.7 s**, not 292 / 9.733 s. They match each other, so the A/B is still fair.
- The audio MD5 is identical (`621ed4f7…`).
- Not re-run: the D5 "type only" ablation and `motion_pair.sh`.

## Score: **59 / 100, the same as v3. TIS tier.**

| category | max | v3 | **detail r3** | why |
|---|---|---|---|---|
| 2.1 illustration | 20 | 12 | **13** | **Better than v3:**<ul><li>The hero now has a head mass, a socketed eye, a gum line with teeth, a throat patch, a grey saddle and 187 marks that read as rake texture.</li></ul>**Defects at 2×:**<ul><li>The cyan rim is an even-width line around the jaw, throat, belly and near flipper. It reads as an **outline**.</li><li>The throat patch is a hard polygon.</li><li>The flipper root shows a pale cuff with a ring seam.</li><li>The dorsal root has a notch sliver (5 s).</li><li>The edge-on fluke at 5–6.5 s reads as a **needle**, with a step where it joins the peduncle.</li><li>Supporting objects are weak: the kelp blades are flat, unshaded olive lozenges, and the boulders are loaves with camo-sticker colour patches.</li></ul> |
| 2.2 lighting | 12 | 8 | **8** | One key from the upper left; the rays agree with it. The kelp blades take no light. The light event still can't be read at phone size. |
| 2.3 depth | 12 | 8 | **8** | The upper frame is now filled: kelp columns on 2–3 hazed planes, plus herring. But the lower third is big flat teal rock slabs. The soft cropped foreground appears in < 60 % of frames. |
| 2.4 colour | 10 | 5 | **4** | Capped at 6: P4 0.065 (worse than v3's 0.055) and P5 2. The frame is almost all teal and olive. The warm masses (coral, tube sponges) that v3 had are mostly gone or below the caption line. Next to `D_0126` it reads as desaturated. |
| 2.5 detail | 10 | 6 | **6** | Capped at 6 because D5 fails (0.052). Without the cap I would give 7: ≥ 15 named objects, ≥ 150 specks, and the densest detail sits on the hero. It stays short of 8 because the kelp blades are stamped from one lozenge and detail is spread across the frame rather than concentrated. |
| 2.6 motion | 14 | 8 | **8** | Same blocking as v3, so the same defects:<ul><li>a near-hold at 2.25–3.0 s;</li><li>**cars still pass through the orca** at 6.75 s and 7.25 s.</li></ul>The swim wave and blinks are fine. |
| 2.7 camera | 8 | 5 | **5** | Capped at 5: M3 is 8.0 s per new composition (it fails on v3 too). There is only one transition kind. |
| 2.8 type | 6 | 4 | **4** | Identical to v3. The YOU tag touches the caption at about 1 s. |
| 2.9 sound | 8 | 3 | **3** | Identical mix. A1–A3 pass; there are no SFX. |
| **total** | 100 | **59** | **59** | |

**Identity gate: PASS.**
- P1 is 1.0 and P2 is 0.
- The orca is our own design, from our own Codex reference. The YOU figure and the kelp set are ours.
- No reference composition coincides.

**Tier gaps (all unchanged from v3):**

| role | time | reference | gap |
|---|---|---|---|
| H | 1.0 s | `W_0000` | 2 |
| X | 3.5 s | `D_0630` | 2 |
| E | 0 s | `D_0126` | 2 |
| P | 6.5 s | `W_0222` | 1 |

**Net.** The hero gained a point and colour lost one. The detail work is real, but it doesn't move the score:
- it is hidden by the D5 cap;
- it is offset by colour loss;
- and §8 density was never what made Kurzgesagt frames look more crafted.

## §8 metrics vs Kurzgesagt (2 s grid unless noted)

| metric | Kurzgesagt W / D | v3 | r3 | reading |
|---|---|---|---|---|
| D1 shapes | 137 / 112 | 203 | 199 | Passes the floor, but **1.5–1.8× above** Kurzgesagt, not "in range" |
| D2 micro | 633 / 658 | 1891 | 2000 | **3× above** Kurzgesagt |
| D3 specks | 124 / 134 (165–371 env) | 288 | 404 (227–471 per frame) | About 10 % above the env top. Yes, this is in or near range |
| D4 edge density | 0.047 / 0.042 | 0.070 | 0.069 | Passes the 0.04–0.08 band, but **1.5× Kurzgesagt** |
| D5 outline | 0.004 / 0.025 | 0.037 | **0.052 FAIL** | 2–13× Kurzgesagt.<ul><li>The type ablation (0.016–0.022 without type) is plausible but not re-verified.</li><li>The bright cyan rim on the orca reads as an outline by eye, but blackhat D5 doesn't count bright lines, so the metric understates this.</li></ul> |
| named objects / env frame | 15–60 | – | 124 by manifest; about 25–35 legible by eye | PASS. Most herring are dim darts that the eye doesn't count as objects |
| hero marks | dozens–hundreds | about 40 | 187 | PASS. In the Kurzgesagt range |
| calm field top cluster | 33–41 % | 0.187 | 0.254 | Below range. Better than v3 |
| P4 grey / P5 families | | 0.055 / 2 | 0.065 / 2 | Both fail, and P4 is worse |

**In short:** we now exceed Kurzgesagt on edges and micro detail and match it on specks and hero marks. The remaining gap is not density: Kurzgesagt is **fewer, larger, saturated, colour-separated masses with a few crisp marks**. We are more edges at lower chroma.

## What now reads at Kurzgesagt level, and what doesn't

- **Reads at the tier:**
  - The hero's mark density and rake texture at 1×.
  - The head construction: socket, teeth and saddle.
  - The world logic: a cold kelp forest with prey fish, no tropical corals, no shark-like far pod.
  - The micro layer and specks.
  - The filled upper frame.
- **Doesn't read at the tier:**
  - Colour breadth and saturation, which is the biggest visible gap against `D_0126`.
  - The rim drawn as an outline.
  - The edge-on fluke.
  - The part seams.
  - Kelp that reads as bamboo: no floats, no ruffle, no shading.
  - Boulders with sticker patches.
  - The empty slab lower third.
  - The inherited staging and type defects.

## Did the Codex assets help? Which path goes into the kit?

- **Yes, for the hero, through path B (structured).** Path B gave the visible gains:
  - the head mass, socket, throat patch and teeth;
  - 187 measured marks that read as texture.
  
  It is also relightable and rigged, and the push-in held up once the eye-socket fork fix was in. **Put path B into the kit for heroes and characters**, after:
  - tapering the rim by N·L and capping its width, so it stops reading as an outline;
  - opening the fluke's planform with a slight yaw, or a bent pose at 5–6.5 s;
  - closing the flipper-root cuff and the dorsal-root sliver.
- **Path A (vectorized) was not used here and should not go into the kit as is.**
  - Its light is baked, so it can't be relit or rigged.
  - Its edge density is about 4× Kurzgesagt (asset-gen reef 0.17 vs 0.042–0.047), which would push D4 out of band.
- **Where Codex can still help is the set's art direction,** not its density. The procedural set's weakness is colour and silhouette design, so a Codex plane-split reference can serve as a colour and composition target. That is untested.

## Top 5 remaining gaps (can code close them?)

1. **Colour script and saturation (P4 0.065, P5 2): yes, in code.**
   - Add a sunlit golden-kelp canopy mass in the top third.
   - Add coralline-pink crust and purple urchins as large masses above the caption line.
   - Raise the chroma of the set to a ≥ 4-family ramp.
   - Shift the key at the proof beat.
2. **Hero finish at 2×: yes, in the OrcaB rig.**
   - The rim is drawn as an outline.
   - The fluke reads as a needle edge-on.
   - The flipper-root cuff, the dorsal-root sliver and the polygonal throat patch need fixing.
3. **Set-piece drawing: mostly yes, in code.**
   - Kelp: blades need pneumatocysts, ruffled edges and the shading stack, with varied blade shapes.
   - Boulders: the crust should be clustered marks and an edge-hugging crust band, not blobs.
   - The lower third needs a mid-value reef mass instead of flat slabs.
   - Codex plane references would help art direction.
4. **Detail distribution vs Kurzgesagt (D2 3×, D4 1.5×, calm 0.25 vs 0.33–0.41): yes, in code.**
   - Trade herring darts and thin stalks for fewer, larger colour masses.
   - Widen the open-water gradient.
   - Concentrate marks on the hero and at the frame edges.
5. **Inherited staging, type and sound: mostly yes, in code.**
   - Cars pass through the orca at 6.75–7.25 s.
   - There is a near-hold at 2.25–3.0 s.
   - The YOU tag touches the caption at about 1 s.
   - The caption stroke pushes D5 to 0.052; a softer plate or halo fixes it.
   - M3 is 8.0 s; add a composition change or a second transition kind.
   - SFX need a licensed or CC0 library. Their placement is code.

```json
{
  "video": "out/detail-pass/orca_open_detail.mp4",
  "judge_date": "2026-11-01",
  "metrics_file": "experiments/detail-pass/data/orca_r3/JUDGE_METRICS.txt",
  "sheet": "out/detail-pass/sbs.jpg",
  "motion_strips": [],
  "scores": {"illustration": 13, "lighting": 8, "depth": 8, "colour": 4, "detail": 6,
             "motion": 8, "camera": 5, "type": 4, "sound": 3},
  "caps_applied": ["2.4 <= 6 (P4 0.065, P5 2)", "2.5 <= 6 (D5 0.052)", "2.7 <= 5 (M3 8.0 s)"],
  "total": 59,
  "baseline_v3_total": 59,
  "pairs": [
    {"role": "H", "ours_t": "0:01", "ref": "kurz-bio/stills/W_0000_tumor-creature.jpg", "tier_gap": 2,
     "defects": [{"t": "0:01", "bible": "§11", "note": "YOU tag touches caption"},
                 {"t": "0:01", "bible": "§2.5", "note": "teal/olive only, low chroma"}]},
    {"role": "X", "ours_t": "0:03.5", "ref": "kurz-bio/stills/D_0630_dumbo-octopus.jpg", "tier_gap": 2,
     "defects": [{"t": "0:03.5", "bible": "§4", "note": "cyan rim reads as even-width outline on jaw/throat/flipper; flipper-root cuff seam; polygonal throat patch"},
                 {"t": "0:05", "bible": "§4", "note": "edge-on fluke reads as a needle; dorsal-root sliver"}]},
    {"role": "E", "ours_t": "0:00", "ref": "kurz-bio/stills/D_0126_reef.jpg", "tier_gap": 2,
     "defects": [{"t": "0:00-0:10", "bible": "§2.5", "note": "P5 2, warm masses lost vs v3"},
                 {"t": "0:00-0:10", "bible": "§8", "note": "stamped flat kelp lozenges; sticker-patch boulders; flat slab lower third"}]},
    {"role": "P", "ours_t": "0:06.5", "ref": "kurz-bio/stills/W_0222_whale.jpg", "tier_gap": 1,
     "defects": [{"t": "0:06.75-0:07.25", "bible": "§9", "note": "cars pass through the orca (inherited from v3)"}]}
  ],
  "identity_gate": {"P1": 1.0, "P2": 0.0, "no_borrowed_designs": true, "no_tracing": true, "pass": true},
  "tier": "TIS",
  "codex_assets": {"helped": true, "kit_path": "B structured (heroes)", "vectorized_A": "not for kit as is: baked light, about 4x Kurzgesagt edge density"},
  "top_fixes": ["colour script and saturated warm masses above the caption line (§2.5)",
                "OrcaB rim taper, fluke planform, root seams (§4)",
                "fewer, larger, shaded set masses instead of edge density (§8)"]
}
```
