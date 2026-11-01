# Kurzgesagt style study: biology, animals, ocean

This is an internal style study. It describes how Kurzgesagt builds its frames so we can reach the same level of craft in code (Remotion/SVG/Canvas/WebGL). Copy the methods, never their characters, assets or compositions. Their duck-like birds, the cell faces as drawn, and specific scenes such as the submarine porthole HUD and the elephant/whale panels belong to them.

## Sources and how to read frame references

| ID | Video | Views | Length | Why |
|---|---|---|---|---|
| **W** | `1AElONvi9WQ` "Why Blue Whales Don't Get Cancer – Peto's Paradox" | 27M | 7:06 | Animals, cells, scale comparisons, data panels |
| **D** | `PaErPyEnDvk` "What's Hiding at the Most Solitary Place on Earth? The Deep Sea" | 25M | 11:19 (content to 10:04, then sponsor) | Ocean, depth descent, light in darkness |

These are the two most-viewed Kurzgesagt videos whose subjects are closest to ours (orca, blue whale, ocean). The other high-view biology videos are immune-system and virus videos. The full channel list sorted by views is in `data/kurz-bio/channel_videos_by_views.txt`.

- Downloaded on the Spark at 1920×1080, **60 fps**, AV1 (`~/studio/refs/kurz-bio/`).
- 2-second frames: `~/studio/refs/kurz-bio/f2/`. 0.25-second bursts (6 stretches × 5 s): `burst/`.
- Local copies, which git ignores (`refs/` is in `.gitignore`):
  - `refs/kurz-bio/stills/`: 40 full-resolution stills, named `<W|D>_<mmss>_<what>.jpg`.
  - `refs/kurz-bio/sheets/`: 2 s contact sheets (`<id>_2s_NN.jpg`), burst sheets (`burst_*.jpg`), transition sheets (`trans_*.jpg`) and a labelled index of the stills (`stills_index.jpg`).
  - `refs/kurz-bio/crops/`: full-resolution detail crops.
- Numbers: `data/kurz-bio/*.json`. Scripts: `tools/kurz-bio/`.

**Reference notation:** `W 3:18` means video W at 3:18. If a still exists for that time it is `stills/W_0318_*.jpg`. Contact-sheet labels give the real timestamp: a 2 s frame `k` was sampled at `2k+1` s, which I checked against exact seeks to within 1 frame. Times quoted from the 2 s sheets are accurate to ±1 s. Stills, bursts and the motion and audio numbers use exact timestamps.

Burst stretches (4 fps × 5 s):

| Burst | Content |
|---|---|
| `burst_W1_0000` | Hero creature, ambient motion |
| `burst_W2_0220` | Split-panel slide, whale |
| `burst_W3_0316` | Iris reveal, cell morph |
| `burst_D1_0124` | Reef, depth layers |
| `burst_D2_0248` | Fish schools, twilight zone |
| `burst_D3_0526` | Anglerfish in darkness |

Transition sheets:

| Sheet | Content |
|---|---|
| `trans_T1_bubblewipe` | D 1:37 |
| `trans_T2_diagwipe` | W 0:04.5 |
| `trans_T3_zoomthrough` | W 0:21.5 |
| `trans_T4_panelslide` | W 2:24.5, iris at 8 fps |
| `trans_T5_lightreveal` | D 4:46 |

---

## 0. Ten-line summary (what separates them from us)

1. **Colour discipline.** Each frame has 1 key background hue, 1 complementary subject hue and 2–3 accent hues.
   - Median: 7–8 colour clusters, 3.5–5 hue families, 94–98 % of pixels with saturation > 0.6.
   - 0 % pure black and < 0.5 % pure white.
2. **Hue-shift shading on flat shapes, with no gradients on objects.**
   - Shadows rotate the hue 10–25° toward blue/violet and lose only 0.05–0.30 in value.
   - Highlights rotate toward cyan or pink and lose 0.2–0.4 in saturation.
3. **No black outlines.** Separation comes from value and hue contrast, plus thick same-family rims around cells.
4. **Everything is rounded**, built from capsules, round-cap strokes and blobs. Sharp triangles appear only on threats (teeth, spikes, fins).
5. **Light is diegetic in dark scenes.**
   - A light cone recolours whatever it touches. Outside the cone, objects drop to background-indigo silhouettes.
   - Only emissive things glow.
6. **Depth comes from 3–5 planes.** Far planes are tinted toward the background colour (saturation about 0.3–0.65) and stay crisp; blur is rare.
7. **Everything is animated on every frame at 60 fps.**
   - 0 % duplicate frames in two tested stretches.
   - Only 2–2.7 % of 30 fps frames are fully frozen.
   - There is always ambient life: tentacle sway, particles, bubbles, blinks.
8. **The camera almost never cuts and almost never stops.**
   - Hard cuts: 13 in W's 426 s and 4 in D's 603 s of content.
   - A big visual change still lands every 2.2–2.9 s (median), through wipes, moves and reveals.
   - Slow camera drift (3–60 px/s) is active 43–55 % of the time.
9. **Micro-detail density.**
   - 150–370 small marks per frame: marine snow, bubbles, organelles, spots, scratch-dash textures.
   - About 15–60 "objects" per scene.
10. **Text is sparse and designed.** It appears as tags with hard offset shadows, a depth counter HUD and big section title cards, never as burned-in captions.

---

## 1. Palette

### 1.1 Global measurements (all 2 s frames of the content, W n=212, D n=302)

| metric | W (cells/animals) | D (ocean) |
|---|---|---|
| k-means(10) clusters with ≥ 2 % coverage (median) | 8 | 7 |
| hue families (30° bins with ≥ 3 % of chromatic px), p10/p50/p90 | 2 / 5 / 7 | 1 / 3.5 / 6 |
| 4-bit colour bins covering 90 % of pixels, p10/p50/p90 | 9 / 31 / 86 | 4 / 30 / 103 |
| largest single colour (background) coverage, p10/p50/p90 | 21 / 33 / 65 % | 23 / 41 / 70 % |
| per-frame median saturation (HSV), p10/p50/p90 | 0.58 / 0.82 / 0.94 | 0.79 / 0.99 / 1.00 |
| per-frame median value, p10/p50/p90 | 0.68 / 0.96 / 0.98 | 0.18 / 0.54 / 0.97 |
| % pixels with S > 0.6 (median frame) | 93.7 % | 97.9 % |
| % pure black (V < 0.05) | 0.0 % | 0.0 % |
| % near-white (S < 0.12, V > 0.92) median / p90 | 0.5 / 2.8 % | 0.2 / 1.8 % |
| frames with a dark background (dominant V < 0.35) | 0.9 % | 47.7 % |

The darkest colour in either video is a deep saturated indigo: `#02001a`–`#060024` (H 244–250°, S 1.0, V 0.10–0.14), seen in the vignette corners of D 5:28 and D 4:50. White is used only for teeth, eye glints, tusks, specular highlights and text. Grey never appears; even the "grey" robot sub in D 1:26 is `#83a8bb` (S 0.30, blue-tinted by depth).

### 1.2 Colour script

The background hue follows the story. In D, depth is encoded in colour. The table shows the median dominant background colour per 30 s window (`data/kurz-bio/f2_D.json`):

| D time | dominant hue | dominant V | scene |
|---|---|---|---|
| 1:00–2:00 | 211–214° | 0.94–0.96 | Shallow reef, shelf |
| 2:30 | 242° | 0.62 | Twilight zone |
| 3:00–3:30 | 252° | 0.25–0.29 | Bioluminescence |
| 4:30 | 250° | 0.14 | Midnight zone |
| 6:00 | 250° | 0.15 | Abyss |
| 9:00–9:30 | 231→215° | 0.77→0.96 | Ascent back to the surface (bookend) |

So the ocean video rotates about 40° in hue (cyan-blue → indigo) and loses 0.8 in value as you descend. In W, each section gets its own key background colour, and the subject is always the complement:
- Orange/pink intro (W 0:00)
- Blue cell world (W 0:36)
- Periwinkle protein world (W 0:50–1:12)
- Pink molecule storm (W 1:18)
- Yellow tissue (W 1:24, 3:04)
- Royal-blue data screens (W 2:22)
- Purple/indigo game map (W 5:36)

### 1.3 Hex values per scene type (k-means of stills, cluster share in brackets)

| scene type | background | subject / mid | accents | refs |
|---|---|---|---|---|
| warm creature intro | top-centre `#f69f50` → sides `#e26956` → bottom corners `#e03c60` (2-axis gradient, see §5) | magenta `#d61779`, shadow `#a70194` → `#77019a` → `#411293` | highlight `#f25199`; rain streaks are a lighter, warmer tint of the background | W 0:00 |
| cell tissue | `#fdf378` (62 %), `#fae343` | cell body `#f9d043`/`#f4943e`, rim `#ee5d43`/`#ef4844` | organelles teal `#25b198`, nucleus violet `#6a06dd`/`#8414b9`, gloss `#d2a4fb` | W 1:26, W 3:04, W 3:18 |
| antagonist cell | (on yellow) | `#aa32d2` base, `#7d1ab0` mid, `#660385` shadow, rim `#ab0098` | highlight `#b368d5`, specular `#d2a4fb` | W 3:18, crop `c_cancer_cell` |
| data / scale screen | royal blue `#073dc2` centre, `#0527b2` edges | whale back `#0418ab`, white belly `#f5f3f1`, baleen `#f8d6b5` | tags teal `#10b8c8` and mint `#13e3b7`, tag shadow `#000090`, side panel yellow `#fae32f`, progress bar `#bf9afa` with white rim and magenta dot `#bd008b` | W 2:22 |
| savanna | sky `#fce758`, hills `#f8d75e` | elephant `#1980f8` / `#1c30eb` / `#51acf6` | ground red-orange `#f05f44`/`#ed371c`, trees magenta `#e64a9e` | W 4:10 |
| shallow ocean | `#0d6ef7`, `#1b8cf9`, `#2cc1fa`, surface `#2decf6` | sand `#9bfcef`, far reef `#4e7ce6`, `#83a8bb` | coral magenta `#c3159e`, violet `#5006d4`, orange `#ef9f13`, clownfish `#ed743e` | D 0:56, D 1:26 |
| twilight zone | `#0704a3`, `#1317ca`, `#1029ea` | hero fish cyan `#16e4ed`, school `#ce06b2`/`#ea4d51`/`#f6b50f` | far fish violet `#6924a7`, caustic net `#1355ec` | D 2:50 |
| bioluminescent dark | `#0c013f` (63 %), `#180c53` | jelly glass `#bbb6cc`/`#8c86bf` (translucent) | neon cyan `#6ce4f9`, pale yellow `#fbf8bb`, warm `#f3cb8d`, core white `#f5faf3` | D 3:04 |
| midnight / abyss | `#0e0149`, `#100156`, vignette `#03001c` | angler `#b806a9`/`#8607a9` | lure/fin-tip cyan `#49ccea`, `#24f0dc`; warm orange `#f59d07` (dumbo) | D 5:28, D 6:30 |
| searchlight floor | unlit `#140d3c` | lit floor `#73fcdb`/`#69eed5` | nodules violet `#7c5ae2`, coral pink | D 7:06 |

**Colours per frame (rule of thumb):** 1 background key (30–70 % of the frame), 1–2 background tints (gradient and atmospheric layers), 1 subject family as a base/shadow/highlight trio, 2–3 small accents in complementary or triadic hues. In practice that is 7–8 clusters of at least 2 % each, while dozens of exact hexes exist because of the shading trios.

---

## 2. Shape language

- **Geometric-organic hybrid.** Silhouettes are organic (blobs, tentacles, fish), but every part is built from simple primitives: circles, capsules (stadiums), rounded rectangles, and constant-width strokes with round caps.
  - Tentacles in W 0:00 are about 40–60 px wide (at 1080p), constant width with round caps.
  - Coral in D 1:26 is made of round-capped branches.
- **Corner radii.** Essentially everything is rounded.
  - Organic shapes have no visible corners at all.
  - UI frames (D 2:08 porthole HUD) use large radii, about 25–35 % of box height.
  - Data tags (W 2:22) are the exception: sharp rectangles, 0–4 px radius.
- **Sharpness is semantic.** Sharp triangles are kept for teeth (D 5:28, D 5:48), spikes and fin rays, which signal danger. Friendly characters have no points.
- **No black outlines.** Separation comes from:
  1. Value and hue contrast against the background. Subjects are complementary: a purple cell on yellow (W 3:18), a blue elephant on a yellow/red savanna (W 4:10), an orange dumbo octopus on indigo (D 6:30).
  2. **Thick self-colour rims** around cells: a darker or more saturated band of the same family, about 18–24 px at 1080p. Examples: the red-orange `#ee5d43` rim around yellow cells and the lighter `#ab0098` rim on the cancer cell (crop `c_cancer_cell`).
  3. **Thin white or light contour lines** on some animals for pop on dark water: about 5–7 px on the twilight fish (crop `c_fish`), and the whale's dorsal contour.
- **Line weights (1080p):**
  - Decorative interior strokes: 6–12 px.
  - Neon jelly strokes: about 10–14 px plus glow.
  - Tentacles and limbs: 25–60 px.
  - Every stroke uses round caps and joins.
- **Interior pattern marks** are flat shapes, not texture images: whale spots (W 2:22), fish scale "C" arcs and hex patterns (`c_fish`), baleen arcs, elephant pores.

---

## 3. Shading recipe per object

Objects never use smooth gradients. Each object is a stack of 3–6 flat layers with hard edges. The values below are measured from crop clusters (`tools/kurz-bio/crop_clusters.py`).

| layer | how it's drawn | measured examples (base → layer) |
|---|---|---|
| **1. Base** | flat fill, 50–65 % of the object | elephant `#1980f8` (H212 S.90 V.97); cancer cell `#aa32d2` (H284 S.76 V.82); tumour `#d61779` (H329 S.89 V.84) |
| **2. Shadow side** | flat, hard-edged shape on the side away from the key light (bottom/right/back; light comes from the top-left). It follows the form and is 20–40 % of the object. **Hue rotates toward blue/violet; value drops only a little; saturation stays the same or rises.** | elephant → `#1c30eb` (**ΔH +22°, ΔV −0.05**); cell → `#7d1ab0` (ΔV −0.13) → core `#660385` (ΔV −0.30); tumour → `#a70194` (ΔH −23° toward violet, ΔV −0.18) → `#77019a` → `#411293` (deepest folds, H261) |
| **3. Highlight** | crescent or capsule following the lit contour, inset from the edge by about 0.5–1× its own width, or a broad lighter plane on top surfaces. **Lower saturation, slight hue shift toward cyan (blues) or pink (magentas), V up 0.05–0.15.** | elephant `#51acf6` (H206 **S.67**); tumour `#f25199` (H333 S.67 V.95); cancer cell `#b368d5` (S.51) |
| **4. Specular** | 1–2 small, near-white bean or ellipse shapes on glossy parts: nuclei, eyes, bubbles | nucleus gloss `#d2a4fb` (S.35 V.98) as a bean shape (W 3:18); eye glints pure-ish white |
| **5. Rim** | cells and blobs: outer band of the same family, darker or more saturated (§2). In dark scenes, a lighter edge plus cyan **glow dots** on tips (fins, lure) | angler edge `#b850b8`; fin-tip dots `#49ccea` with a 10–20 px soft glow (D 5:28, crop `c_angler`) |
| **6. Cast / contact shadow** | **flat offset copy, not blurred**: a darker tint of the *background* (not black), offset about 8–15 px down/right, about 30–50 % opacity, or a flat ellipse under feet | tentacle shadow `#d8366e` on the nearby background `#f15666`: a darker, more saturated pink (W 0:00, lower tentacles); contact ellipse under the rhino (W 0:14); tags use a solid offset block (§10) |
| **7. Surface marks** | sparse micro-marks in base ±10 % value: clusters of 3–5 short round-capped dashes ("scratches") or dots (pores, freckles) | tumour dashes (crop `c_tumor_highlight`), elephant pores (crop `c_elephant`), dumbo freckles (D 6:30), whale spots |
| **8. Inner glow / emissive** (dark scenes only) | additive or screen soft glow, radius about 20–60 px, 30–60 % opacity; the core goes toward white | jelly: stroke `#6ce4f9`/`#fbf8bb`, core `#f5faf3`, halo onto `#210e51` (D 3:04, crop `c_jelly_glow`); sub headlights; lure (D 5:44) |
| **9. Translucency** | glass-like bodies are a semi-transparent tint (about 40–60 %) plus internal structure lines | jelly bells `#bbb6cc` over `#0c013f`; porthole glass glare = big soft lighter shapes at about 10–15 % white (D 2:08) |

**Inferred blend modes:**
- Shadows and highlights behave like normal-blend flat fills with hand-picked colours, not multiply.
- Glows behave like screen/add.
- Atmospheric fade behaves like a normal-blend overlay of the background colour (§6).

**Code recipe.** For an SVG/Canvas object, derive the trio from one base colour in OKLCH or HSV:
- `shadow = rotate(base, +15..25° toward 260°) with L −0.05..−0.25`
- `hi = rotate(base, −8° toward cyan or +5° toward pink) with S ×0.7 and L +0.08`
- Clip the shadow and highlight shapes to the base path, which gives hard edges for free.

---

## 4. Lighting

- **Key light top-left.** Highlights sit on upper-left contours across both videos: W 0:00 tumour, W 3:18 cell nucleus gloss, W 4:10 elephant. Shading is graphic, not physical; there is no attempt at consistent normals.
- **Background lighting = soft radial or linear gradient** (the only smooth gradients in the image), measured with 9×9 samples:
  - W 2:22: centre `#0741c6` (V .78) vs corners `#0424b0` (V .68), so **+0.10 V at the centre**.
  - W 0:00: top-centre `#f69f50` (H28) → sides `#e26956` (H8) → bottom corners `#e03c60` (H346). This is **a 40° hue rotation top→bottom plus a radial falloff**.
  - W 1:26 yellow: almost flat (`#fdf378`), with only a slight warm corner `#f9d63c`.
- **Dark scenes: the vignette is the light.**
  - D 5:28: centre `#100156` (V .34) vs corners `#02001a` (V .10). The falloff is a large **soft-edged disc**, so the scene reads as "seen through the light of the sub".
  - D 4:50: background `#060024` (V .14); the beam area is lifted to `#131a74`.
- **Light cones (searchlights) recolour the world.**
  - Cone interior = same hue, value lifted. D 4:10: `#4a00f0` (V .94) inside vs `#170057` (V .34) outside.
  - The cone fades along its length, from bright near the source to the background at the tip.
  - Objects inside the cone are drawn in full colour; parts outside drop to dark indigo silhouettes. D 6:30: the dumbo body is lit orange `#f59d07` while the tentacles outside the beam are `#2c1e83`.
  - D 7:06: the lit floor is mint `#73fcdb` and the unlit floor `#140d3c`. The same objects are drawn twice, lit and unlit, and masked by the cone.
  - **Code recipe:** render each scene twice (lit palette and unlit palette) and composite with the cone or disc as a mask.
- **Light rays in shallow water:** wide, soft-edged diagonal beams at about 5–12 % white, slowly swaying (D 0:56, D 1:26 top right).
- **Caustics:** a network of lighter, rounded cell shapes along the surface band (D 2:50 top: `#1355ec` net over `#0704a3`; D 1:38 shelf map). It is drawn as flat shapes, animated with slow morphing.
- **Bloom:** only on emissive objects: sub lights, jellies, lure, sun, fin-tip dots, and the "inner glow" of electric or neon elements. Non-emissive edges are razor-crisp.

---

## 5. Depth

| scene | planes | treatment per plane | ref |
|---|---|---|---|
| reef | 5 | (1) **Foreground coral** cropped by the frame edge: most saturated, largest, full shading. (2) **Mid**: fish and sub, normal colour, about 5–12 % of frame height. (3) **Far reef**: flat silhouettes tinted 40–60 % toward the water blue (`#4e7ce6` S.66, `#83a8bb` S.30), no interior shading. (4) **Water column**: bubbles at 30–60 % alpha, particles. (5) **Surface band + light rays + caustics.** | D 1:26, crops `c_reef_fg`, `c_reef_mid`, burst `D1_0124` |
| twilight school | 4 | Hero fish (35 % of frame height) → mid school (8–10 %) → far tiny fish (1–3 %, desaturated violet `#6924a7`, low contrast) → translucent jellies at the bottom edge (about 50 % alpha) + surface net at the top | D 2:50, burst `D2_0248` |
| deep / abyss | 3 | foreground marine snow (larger, sharper specks) → subject → background disc/vignette (+ dim far fish, slightly soft) | D 5:28, D 6:30 |
| cell tissue | 2–3 | Hero cell → surrounding cells (same scale, full colour, cropped at the frame edges) → background blob pattern in a slightly darker tint of the background (`#fae343` blobs on `#fdf378`) | W 3:18, W 1:26 |

**Rules:**
- **Atmospheric fade = mix toward the background colour.** Far objects end at S 0.3–0.65 and a value close to the background. They are also simplified: no highlights, no marks.
- **Blur is rare.**
  - Mid and far planes are crisp in almost all frames. Only dim background fish in the darkest scenes, and some glows, look softened by about 2–4 px.
  - Depth of field is suggested by fade, not blur.
- **Scale steps** between planes are large, about 3–5× per plane.
- **The foreground frames the shot.** A dark or saturated foreground element is cropped by the bottom or side edge in most landscape shots: D 1:26 coral, W 4:10 grass tufts `#ed371c`, W 0:14 plants.
- **Parallax.**
  - Visible in the long tracking moves: D 1:45–2:04 continental-slope scroll, D 7:32 depth chart.
  - My per-band phase correlation on the reef burst was inconclusive (peak < 0.1) because every layer also animates on its own. Treat parallax as a visible constant, not a measured one.
  - When building, use about 1.0 / 0.6 / 0.3 / 0.1 speed for foreground / mid / far / background-gradient as a starting point.

---

## 6. Texture

- **No film grain or paper texture.** The residual noise standard deviation in flat regions is 0.8 (median, both videos), which is codec-level. A grain overlay would read as a different style.
- **Flat-fill dominance.** Per frame (Sobel on luminance), the median frame is 85–87 % flat-fill pixels, 8–9 % soft gradient (background gradients, glows) and about 5 % edge pixels.
- **Texture comes from vector micro-marks:**
  - dash clusters ("scratches") and dot pores (§3 layer 7);
  - repeating pattern shapes such as fish scale arcs, baleen arcs and hex cells;
  - background blob patterns: a slightly darker tint of the background, large rounded blobs at about 3–5 % value difference (W 0:36, W 1:24 yellow, W 4:32 purple, D 1:38).
- **Diagonal motion streaks** (rain, speed): round-capped capsules in a lighter background tint at about 30–50 % alpha, falling continuously (W 0:00).

---

## 7. Detail density

- **Objects per frame.** Measured as connected components brighter than the local background (`tools/kurz-bio/particles.py`).
  - Small specks (6–400 px²): reef 371, anglerfish 283, porthole 280, fish school 206, dumbo 165, marine snow 168.
  - Medium shapes (400–5000 px²): reef 157, fish school 90, marine snow 55.
  - Even the "minimal" data frame (W 2:22) has 58 specks and 49 medium shapes: spots, bubbles, label parts.
- **Named objects (hand count):**
  - reef D 1:26: about 35 (corals of 8+ types, 6 fish species, sub, bubbles, sea star, keyboard, bottle, starfish);
  - tissue W 3:18: 13 cells × about 10 organelles each;
  - fish school D 2:50: about 25 fish + jellies + shrimp;
  - anglerfish D 5:28: 1 hero + 1 prey + about 280 marine-snow specks + 6 glowing filaments.
- **Hero vs detail balance.** One hero occupies 25–45 % of frame height. A calm, large background colour covers 33–41 % of the frame (median top-cluster share). Detail is concentrated around the hero and at the frame edges, while the centre-background stays calm.
- **Micro-detail always present:**
  - marine snow: bean-shaped specks with a median area of 49 px², about 7×7 px, 2–3 tints of the background;
  - bubbles with highlight crescents;
  - drifting organelles, stars, dust;
  - in dark scenes, tiny faint far fish.

---

## 8. Character design rules (study only, never reuse their designs)

- **Construction.** 5–15 large rounded primitives plus pattern marks. Limbs are constant-width round-capped strokes. Silhouettes are recognisable at thumbnail size: the whale's head and baleen, the clownfish stripes, the anglerfish jaw and lure.
- **Eyes are the main expressive tool.**
  - Pupil: dark indigo or violet, never black (`#410968` on cells).
  - Highlights: 1 large and 1 small white glint, upper-left.
  - Fish and animals often get a coloured iris ring (yellow ring `#f6b50f` on the twilight fish, white ring on the dumbo).
  - Cute agents (cells, W 4:38, crop `c_face_cells`) have a tiny dark dash mouth, two blush ellipses (`#ee5560`) beside the eyes, and the face placed low and wide on the body.
  - Expressions come from brows and eye shape: `> <` squints, closed arcs, worried brows (W 3:18 sad cancer cell), wide eyes.
- **Colour role.**
  - Good or neutral agents: warm yellows, oranges and pinks, round.
  - Threats: purple or magenta, tentacled, white triangular teeth (W 0:00 tumour creature, W 3:30, D 5:28, D 5:48).
  - Hue coding stays consistent across the whole video: cancer is always purple.
- **Real animals stay natural.** Whale, elephant, seal and fish get no human mouths; any personality comes through the eyes and the pose. Only biological agents (cells, viruses) get full cartoon faces.
- **Morphing identity.** A character changes state by morphing colour and shape in place rather than cutting: the cell turns orange → purple, grows about 1.3× with an overshoot and sprouts tentacles in about 0.75 s (W 3:17.25–3:18.0, burst `W3_0316`).

---

## 9. Motion craft

### 9.1 Measurements

From `tools/kurz-bio/motion.py`, which decodes the whole video at 30 fps at 256×144 and computes frame differences and phase correlation (`data/kurz-bio/motion_*_summary.json`).

| metric | W | D (content to 10:03) |
|---|---|---|
| native frame rate | 60 fps | 60 fps |
| duplicate frames at 60 fps (W 2:20–2:26, D 1:24–1:34) | **0 %** | **0 %** |
| fully frozen frames (no pixel changes > 6 levels) | 2.0 % | 2.7 % |
| "quiet" frames (< 1 % of pixels changing: only ambient motion) | 21 % | 19 % |
| longest quiet run | 6.2 s (W 6:23, the held 2 g tumour comparison) | 7.1 s (D 9:50, the surfacing breather) |
| hard cuts | **13 in 426 s** | **4 in 603 s** (0:12.6, 0:36.4, 0:52.9, 3:01.3) |
| big visual changes (≥ 25 % histogram change within 0.5 s), median interval | **2.2 s** | **2.9 s** |
| global motion speed (non-transition frames), p25/p50/p75/p90 | 1 / 4 / 18 / 171 px/s | 6 / 19 / 144 / 292 px/s |
| time share: still (< 3 px/s) / slow drift (3–60) / pan (60–400) / whip (> 400) | 43 / 43 / 11 / 4 % | 14 / 55 / 24 / 7 % |

Speeds are in 1080p pixels per second.

### 9.2 Rules derived

- **Animate at 60 fps on every frame**, with interpolated tweens rather than held-pose stepped animation.
- **Something always moves.** Even "holds" have:
  - tentacle tips cycling with phase offsets (burst `W1_0000`: every tip moves in every 0.25 s frame while the body breathes slowly);
  - rain streaks falling;
  - particles drifting (D 5:28 marine snow) and bubbles rising (D 1:26);
  - fins and tails sweeping, eyes blinking;
  - slow light-ray sway.
- **Camera drift is constant and gentle.** Velocity profiles are bell-shaped (ease-in-out), with ramps of about 1–4 s. Examples (px/s):
  - D 2:54–3:08: 2 → 6 → 11 → 12 → 5 over 14 s, a slow downward drift.
  - D 9:13–9:22: 3 → 21 → 42 → 26 → 3 over 8.6 s.
  - W 2:45 scale-bar move: 22–38 px/s, oscillating gently over 8 s.
  - Median ease-in about 0.6–1.1 s and ease-out about 0.6–0.7 s on the shorter moves (n = 29 W, 53 D).
  - Use sine or cubic in-out for drifts and a stronger expo-out for arrivals.
- **Pops and overshoot.** Elements enter by scaling from 0 with an overshoot of about 10–30 % that settles in about 0.25–0.5 s: labels (W 2:22 tags), the cell growth (W 3:17.5–3:18.25), the title letters assembling from bacteria (W 2:26.0–2:27.0).
- **Secondary motion** on every appendage: tentacles (W 0:00), whale tail (W 2:22.5–2:24.75, a full tail-fluke stroke with the body following through), fish fins, jelly tendrils (D 3:04), lure wobble (D 5:28).
- **Counters and bars animate continuously.** The depth counter ticks 5633 → 6002 m over 7:32–7:42, and progress bars fill (W 2:08–2:22).

### 9.3 Cut rhythm and transitions (catalogue)

There are almost no hard cuts. Change comes from **transitions inside a continuous world**. Each transition below has a measured duration (transition sheets):

| transition | how | duration | ref |
|---|---|---|---|
| diagonal wipe into schematic mode | A straight-edged wipe at about 45° slides across. Behind it, the same subject is redrawn as a flat diagram with callout lines and info panels (detailed → schematic match). | ≈ 0.75 s, ease-out | W 0:04.75–0:05.5, `trans_T2` |
| iris-in (circle close) | A circle shrinks onto the subject over the new background colour, ending in a dot. The next scene then assembles from flying pieces. | ≈ 0.4 s | W 2:25.5–2:25.9, `trans_T4` |
| iris-out reveal | A circle expands from a point and reveals the next scene | ≈ 0.5 s | W 3:16.75, burst `W3_0316` |
| split-panel push | Panels slide horizontally; the new panel pushes the old one out (comparison A → B) | ≈ 2 s, ease-in-out | W 2:20.5–2:22.5, burst `W2_0220` |
| bubble-burst wipe | Dozens of overlapping bubbles (2–3 tints) cover the frame and clear to reveal the new location. Ocean-themed. | ≈ 0.8 s | D 1:37.6–1:38.4, `trans_T1`; also D 2:18, 8:20, 9:22 |
| push-in through the subject | A scalpel cuts, the camera pushes in about 1.6× on the cut surface, then a hard cut to the next scale (a dot on the plain background) | 1.25 s push | W 0:24.75–0:26.25, `trans_T3` |
| light-reveal dolly | In darkness, the beam grows and reveals the subject while the camera dollies in about 2.5× | ≈ 5 s | D 4:46–4:51, `trans_T5` |
| continuous descent | A cross-section chart scrolls vertically with a live depth counter; it acts as a chapter divider | 10–20 s | D 4:32–4:38, 7:32–7:50, 8:16 |
| in-place morph | The subject changes colour or form instead of cutting | 0.5–1 s | W 3:17, W 5:14–5:24 (cell multiplies into a grid) |
| hard cut | Used to jump scale or for punchlines, rarely | – | W 0:26.6, D 0:12.6 |

**Rhythm:** a big visual change every 2–3 s while the "shot" lasts 10–30 s. The cold open runs about 26 s (W 0:00–0:27, D 0:00–0:26), then a 4–5 s logo jingle (W 0:27–0:32, D 0:26.7–0:36), then the body.

---

## 10. Typography and on-screen text

- **Typeface.** A bold geometric sans with round counters, upright, tight spacing, and a double-storey `a` in "Years" (crop `c_type_label`). I have not identified the exact face; the closest free stand-ins to test are Montserrat Bold/ExtraBold and Nunito Sans Black. Do not use their logo lockup.
- **Data tags (W 2:22, crop `c_type_label`):**
  - Flat rectangle with 0–4 px radius.
  - Two-tone text: the number in white, the unit in a light tint of the tag colour (tags `#10b8c8` teal, `#13e3b7` mint).
  - Hard offset shadow block, about +14 px x and +14 px y at 1080p, in saturated navy `#000090` (sampled), with no blur.
  - Cap height about 45–55 px (≈ 4.5–5 % of frame height); tag height about 85 px; padding about 0.4× tag height.
- **Section title cards** (W 2:40 "Solution 1: EVOLVE / Or Become a Blob of Cancer", W 4:18 "HYPERTUMORS"):
  - Centred 3-line lockup: small kicker, huge all-caps word (cap height about 100–120 px), small subtitle.
  - White, over the scene's dimmed and blurred background pattern.
  - The word then scales up past the camera as a wipe (W 2:42 "EVOL…").
- **Zone and name labels** (D 1:40 "Continental Shelf", 4:40 "Midnight Zone", 6:04 "Abyssal Plain"): small pills with about 30 px text, magenta/indigo or mint, placed top-centre or bottom-centre, appearing for about 2–4 s.
- **HUD progress device** (D 2:08 "275 m", D 5:04 "1023 m"): a persistent top-left counter in yellow italic bold on a violet pill with a double cyan frame. It runs from 2:04 to the bottom. This is the same idea as our FEEDBACK B6 progress device; build our own visual design.
- **Callouts:** thin straight leader lines (about 3 px, white or light) with a dot or ring at the anchor point and a framed info panel (W 0:05.75, W 3:34 "Proto-Oncogene").
- **Frequency.** Text appears roughly every 15–40 s, never as subtitles. Numbers on screen are always literal: "100,000,000 Billion Cells", "1000 m", "10,222 m".

---

## 11. Sound design

Measured from the audio track and captions (`tools/kurz-bio/audio.py`, ffmpeg `ebur128`). I did not listen to the audio; these are numbers only.

| metric | W | D |
|---|---|---|
| integrated loudness | **−16.0 LUFS** | **−16.9 LUFS** |
| loudness range (LRA) | 2.3 LU (very consistent) | 4.2 LU |
| narration rate during cues / over the whole video | 170 / 155 wpm | 160 / 124 wpm |
| speech RMS (50 ms windows) p50 | −17.1 dBFS | −18.1 dBFS |
| non-speech gaps RMS p10 / p50 | −31 / −22 dBFS | −34 / −24 dBFS |
| true silence (< −50 dBFS) | 0.02 % of the time, longest 0.05 s | 0.4 %, longest 1.45 s |
| narration-free stretches | intro sting only | intro jingle + captioned "[♪ Deep Sea Ambience ♪]" stretch at 9:29 (ascent, about 30 s) |

**Rules derived:**
- **Music never stops.** There is effectively zero digital silence. The bed sits about 5–7 dB under speech (gap p50) and about 14–16 dB under speech in the quietest gaps (gap p10).
- **Narration is fast and dense** (160–170 wpm while speaking). Visuals carry the short pauses. One long ambience breather in D marks the emotional "return to the surface" bookend.
- The loudness target for our mixes should be about −16 LUFS integrated, LRA ≤ 4 LU.
- **SFX:** the high-frequency onset proxy found about 0.8 transients/s inside non-speech gaps in D: bubbles, pops, UI blips and whooshes at transitions. Caveat: the proxy can't separate SFX from music hits.
- **Jingle.** A short signature intro (about 4 s) after a 26 s cold-open hook. We need our own sonic logo, not theirs.

---

## 12. What this means for our pipeline (input to STYLE_BIBLE / JUDGE_RUBRIC)

1. **Palette engine.**
   - Per scene: a key background hue, its complement for the subject, and 2–3 accents.
   - Generate shading trios with an OKLCH hue-shift function (§3).
   - Ban `#000`, ban greys, cap near-white at ≤ 2 % of the frame.
   - Script hue and value across the episode: for the ocean, 211° → 250° hue and V 0.96 → 0.14 with depth.
2. **Object builder.** Every illustrated object has, at minimum:
   - base + hard shadow shape + highlight crescent + 1 specular;
   - rims on blobs/cells;
   - 3–8 surface micro-marks;
   - round caps everywhere.
3. **Lighting pass for dark scenes.** Lit and unlit palettes composited through a cone or disc mask, plus additive bloom only on emissives.
4. **Depth pass.** 3–5 planes; far planes mixed 40–60 % toward the background, simplified and not blurred; a foreground crop element in landscape shots; parallax speeds of about 1 / 0.6 / 0.3 / 0.1.
5. **Ambient motion layer, never off:**
   - particles: 150–300 specks in dark scenes;
   - bubbles and light-ray sway;
   - per-appendage sine wobble with phase offsets;
   - blinks every 2–5 s;
   - camera drift of 3–60 px/s with 1–4 s eases.

   Render at 60 fps or at least smooth 30 fps; never hold frames.
6. **Transitions instead of cuts.** Build a library (diagonal wipe, iris in/out, bubble wipe, panel push, push-in, light reveal, morph) and target a big visual change every 2–3 s.
7. **Judge metrics we can compute automatically on our renders** with the same scripts:
   - per-frame S median ≥ 0.8;
   - pure-black share 0 %;
   - k-means clusters ≥ 2 % between 6 and 9;
   - flat-fill pixels 80–92 %;
   - frozen frames ≤ 3 %;
   - big-change interval 2–3.5 s;
   - hard cuts ≤ 2/min;
   - loudness −16 ± 1 LUFS.
