# Kurzgesagt space/physics style study (measured)

Internal study. The goal is to learn the **style rules** behind Kurzgesagt's space scenes so we can author our own art in code (Remotion, SVG, Canvas, WebGL). We do not copy their characters (the birds, the faced planets, the duck), their assets or their compositions. Everything below describes recipes and numbers, not designs to trace.

## Sources and method

| key | video | id | uploaded | views (2026-11-01) | length |
|---|---|---|---|---|---|
| **L** | The Largest Star in the Universe – Size Comparison | `3mnSDifDSxQ` | 2020-09-22 | 35.8 M | 11:59 |
| **I** | Why Black Holes Could Delete The Universe – The Information Paradox | `yWO-cvGETRQ` | 2017-08-24 | 32.4 M | 10:12 |

These are the two most-viewed space/physics videos in the channel's upload list (yt-dlp flat listing, 255 videos; only non-space titles rank higher). **L is the current house style** (soft glows, gradients, light rays, speckle textures). **I is the 2017 style** (flatter, glows built from stepped colour bands, more saturated). Where the two differ, L is the target.

On the Spark (`~/studio/refs/kurz-space/`, CPU only, `nice -n 10`):
- 1080p60 H.264 + Opus audio, merged to mp4.
- Frames every 2 s (665 frames). Frames every 0.25 s over three 5-second stretches: **A** = L 1:18–1:23 (character planet and star ignition), **B** = L 6:52–6:57 (surface eruption, then a cut to a blue hypergiant in a nebula), **C** = I 7:03–7:08 (wipe into a landscape pan).
- Measurement scripts are in `tools/` (committed). Raw outputs are in `data/` (committed):
  - `frame_stats.py`: per-frame k-means palette, colour-bin counts, HSV percentiles, border colour, grain.
  - `motion_cuts.py`: per-frame difference at 30 fps, cuts and transitions, static frames.
  - `band_track.py`: phase-correlation tracking of horizontal bands (camera pans, parallax).
  - `zoom_est.py`: slow zoom and drift estimates.
  - `pop_curve.py`: object entry and settle curves at 60 fps.
  - `probe.py`: pixel, line and radial probes on stills.
  - `audio_sync.py`: band energy around visual events.
  - `sheet.py`: contact sheets.

Reference images are local only and ignored by git (`refs/`, see `.gitignore`):
- `refs/kurz-space/*.jpg`: 40 full-resolution stills, named `<L|I>_<m>m<ss>s_<what>.jpg`.
- `refs/kurz-space/sheets/<id>_2s_NN.jpg`: 2-second contact sheets, 64 frames each, with timestamps.
- `refs/kurz-space/sheets/q_<A|B|C>_*.jpg`: 0.25-second sheets.

In this document, **"L 6:54"** means video L at 6:54. The matching still is `refs/kurz-space/L_6m54s_*.jpg` when one exists. Otherwise, look at that timestamp in `sheets/3mnSDifDSxQ_2s_*.jpg` (L) or `sheets/yWO-cvGETRQ_2s_*.jpg` (I).

Caveats:
- YouTube compression erases sub-2-level noise, so grain could not be measured (see §6).
- Pan tracking uses integer pixel steps, and the 10-frame chaining keeps the error below 1%.
- Audio proxies could not separate sound effects from voice (§11).

---

## 1. Palette

**Whole-video statistics** (2-second frames; outro and credits excluded; L n=305, I n=298):

| metric | L (2020) | I (2017) |
|---|---|---|
| median saturation (all pixels) | **0.82** | **1.00** |
| median saturation of chromatic pixels | 0.76 | 0.97 |
| median value (brightness) | 0.62 | 0.45 |
| frames with a dark background (border V < 0.25) | 25 % | 28 % |
| hue families per frame (30° bins, each ≥ 3 % of chromatic pixels): median, range | **3** (1–7) | **3** (1–7) |
| 4-bit colour bins covering 80 % of pixels (median) | 13 | 7 |
| 4-bit colour bins covering 95 % of pixels (median, p10–p90) | 61 (18–138) | 44 (7–151) |
| coverage of the single largest colour cluster (median) | 30 % | 41 % |
| coverage of the top 3 colour clusters (median) | 64 % | 76 % |
| near-white pixels (V > 0.92, S < 0.15), median share of frame | 0.2 % | 0.4 % |

The hue distribution across the video uses 30° bins (0 = red).
- L: blue-violet 240–270° = 40 %, blue 210–240° = 21 %, cyan 180–210° = 10 %, magenta-red 330–360° = 11 %, red 0–30° = 6 %, orange-yellow 30–60° = 6 %. Green (60–150°) is about 0 %.
- I: 240–270° = 46 %, 270–300° = 13 %, 150–180° = 11 %, warm hues ≈ 3 %.

**Rules derived from this:**
- **Cool field, warm subject.** About 70 % of chromatic pixels are blue to violet. Warm hues (red, orange, yellow) appear only on the hero object (the stars). Yellow-green and green are almost absent in space scenes.
- **Very saturated, mid-dark values.** Almost nothing is grey. Even the "dark" backgrounds are saturated navy (#02112e is S 0.95 and V 0.18), never black.
- **Few colours per frame.** The top three flat colours cover two thirds of the frame, and about 13 colour bins cover 80 % of it. The variety comes from small accents, not from many mid-sized fields.
- **White is rare and reserved for heat.** Near-white covers 0.2 % of a median frame. It appears only on the hottest highlights: the star rim crescent, flare cores and sparkle centres (L 1:22.5, L 1:48, L 5:50).

**Hex palette per scene type** (k-means colour : coverage %, measured on the named still or 2-second frame):

| scene type | ref | background | mid tones | accents |
|---|---|---|---|---|
| Deep-space field | L 0:14, L 3:14, L 2:58 | `#010727`–`#02112e` (85–93 %) | star specks `#0d2140`, `#0e334f` | subject only |
| Isometric "lab" floor | L 0:30, L 0:44, L 2:26 | `#3c2da0` (60 %) with grid lines `#332197` | cast shadow `#251882`, cube faces `#796ff6` / `#573ecd` / `#170b5f` | object colours |
| Yellow star (Sun-type) | L 3:14 | `#02112e` | core `#f8da22` → limb `#e64200` | spots `#780a18`, glow `#9f2f1b` → `#370d24` |
| Gas giant (banded) | L 0:22, L 0:30 | — | bands `#10bba8`, `#ab2333`, `#1488cd`, `#0b5fa6`, `#c94b0d` | spot rings |
| Red dwarf, red nebula | L 2:34, L 8:04 | `#02112e`, `#24011b` / `#3b001a` | `#57011d`, `#8c0528`, `#3b077a` | `#bc1b06`, `#ee710a`, `#f5d133` |
| Red hypergiant field | L 8:50 | `#7b001e`, `#3e0011`, `#1f000b` | `#aa0617`, `#95011a` | `#c70c11` (one hue family, value steps only) |
| Blue star, teal nebula | L 4:06, L 6:54 | `#021032`, `#041a45` | `#296c99`, `#164991`, `#36b69e` (mint nebula) | `#55e0ef`, `#2395ee`, `#d0f2fb` |
| Opening nebula | L 0:02 | `#010729`, `#041537`, `#04244b` | `#083d72`, `#0a5887` | `#1f95a0`, `#2dd2ce` |
| Fusion "particle soup" (macro) | L 1:10 | `#f38521` | `#f6b117`, `#f59c19`, `#f7c311` | `#bd1c38`, `#f9edae` |
| Black hole, dark (2017) | I 0:34, I 9:12 | `#0d0029`, `#12003a` | `#150a52`, `#213870` | `#279db1`, `#d811b3` |
| Night landscape | I 7:06 | sky `#240073` → `#0f0450` | hills `#073e99` → `#0b90cb` → `#15c1e7` | grass `#13e3fd`, dock `#fce3a8` |
| Interior / character | L 8:36, I 3:26 | `#021743`, `#5100db` | `#0f1c59`, `#092d6e` | `#46abbe`, `#60022a`, warm skin and beak tones |

---

## 2. Shape language

- **No outlines.** Shapes are separated only by value and hue contrast (all stills). The only drawn strokes are information graphics: label leader lines (about 4 px with round caps, L 0:30), wireframe globes and orbits (2–3 px, L 2:58, L 9:02, I 7:22), and HUD panels (I 4:00).
- **Geometric base, organic surface.** The silhouettes are perfect circles, cubes and rounded rectangles. Everything that lives on or around them is organic:
  - wavy band edges with drips and blob bridges (gas giants, L 0:22);
  - metaball-like plasma rims (L 6:54);
  - blobby nebula clouds with tapered tails (L 0:02, L 8:04, L 9:56).
- **Corner radii.**
  - Machines and props use generous radii: monitor bezel ≈ 60 px at 1080p, about 6 % of the object's width (L 8:36). Keys and buttons are pills (fully rounded).
  - Data tags are rounded rectangles with radius ≈ 6 px and a small triangular pointer (L 2:00 timeline).
  - Isometric cubes keep sharp corners (L 0:30).
- **Concentric-ring motif.** Spots, craters, sunspots, bubbles and planet storms are always concentric rings of 2–3 tones, never single discs (L 3:14, L 1:58, L 6:54, L 0:30 storm).
- **Small-shape families repeat in clusters**:
  - corona "C"-shaped flame crescents around star limbs (L 3:14: about 60 crescents of 20–40 px);
  - surface speckle dots (hundreds of 2–6 px dots, L 3:14, L 6:54);
  - detached bubbles near plasma rims (L 6:54).
- Line weights at 1080p:
  - leader lines ≈ 4 px;
  - wireframes 2–3 px;
  - sparkle arms 1–2 px;
  - grid lines ≈ 3 px, only 6 % darker than the floor (`#332197` on `#3c2da0`).

---

## 3. Shading recipe per object (inferred from pixel probes)

Two lighting models are used, and they never mix:
- **Opaque bodies** (planets, cubes, characters) get a **hard-edged shadow shape** and a **soft highlight disc**.
- **Luminous bodies** (stars) are not darkened at all. They get a **hue-rotating radial gradient** plus a glow.

### 3a. Opaque planet (gas giant, L 0:30 `L_0m30s_jupiter-cube-isogrid.jpg`)

| layer | how it looks | measured / inferred |
|---|---|---|
| Base | flat bands with wavy edges, blob spots, one ring storm | band colours in §1 |
| Highlight disc | a large circle about 70 % of the planet's diameter, offset to the upper left, slightly lighter | the same band inside vs. outside gains about +12–15 % toward white (`#10bba8` → `#34c0b3`; `#a11d34` → `#ba3853`). This is about a 13 % white normal or screen overlay. The disc edge is hard. |
| Shadow crescent | hard-edged crescent on the lower right, about 13 % of the radius thick at the equator and thicker toward the bottom | `#a11d34` → `#6c0728`: V 0.63 → 0.42 (−33 %), S 0.82 → 0.94, hue −10° toward magenta. This equals a **multiply with ≈ `#ab3dc4`**: the shadow takes the hue of the violet environment, not black. |
| Rim | no outline. On the shadow side, a thin lighter blue edge picks up the environment colour (bounce/rim light) | 1–2 px transition to the background |
| Cast shadow | a soft ellipse on the floor, offset away from the light | floor `#3c2da0` → `#251882` (multiply ≈ (0.62, 0.53, 0.81), slight blue shift), plus a darker contact core `#331269` (hue 263°, i.e. ambient occlusion pushed toward magenta) |

### 3b. Isometric prop (cube, L 0:30)

- Faces: top `#796ff6` (V 0.96), left `#573ecd` (V 0.80), right `#170b5f` (V 0.37). The value ratios are **1.00 / 0.83 / 0.39**, and all three faces keep the same hue (≈ 245–250°).
- The top face has a glassy diagonal stripe `#83acee` (hue rotated −30° toward blue), like a reflection band.
- The long cast shadow falls to the lower right in the same multiply colour as the planet's cast shadow, so the light direction is consistent within a set.

### 3c. Yellow star (L 3:14 `L_3m14s_sun-dark-bg.jpg`, radius R ≈ 335 px)

| layer | measured |
|---|---|
| Body gradient | radial from core `#f8da22` (H 52°, V 0.97), flat to 0.45 R, then **hue rotates to `#e64200` at the limb (H 17°)**. Value stays at 0.90 or above. Limb darkening is done with hue, not value. |
| Lit-side rim | a bright crescent `#facf2b` about 10 px wide just inside the limb on the left, with a dark red line `#c8150d` (about 6 px) inside it. This is a double stroke made of two offset crescents. |
| Spots | concentric donuts with 3 tones (dark red outer, orange, light inner), 40–120 px, a few showing white-hot centres (L 2:00) |
| Texture | hundreds of 2–6 px darker speckle dots over the body |
| Corona | a ring of small C-shaped crescents (`#f5bc1e` / `#e2550c`) standing just off the limb |
| Glow | luminance excess over the background (L 16): +82 at R+5, +53 at R+25, +16 at R+45, +7 at R+65, about 0 at R+105. This is a **tight halo of about 0.1 R with a faint tail to 0.3 R**. The glow's **hue rotates outward**: H 9° → 348° → 327° → 251°, i.e. red, then magenta, then into the navy background. |
| Light rays | 16–20 soft radial wedges reaching about 1.4–1.5 R, at ≈ 10–15 % opacity (visible at L 3:14 and L 4:06) |

### 3d. Blue star (L 6:54 `L_6m54s_blue-hypergiant-nebula.jpg`, R ≈ 390)

- Body: radial gradient from `#55fffd`/`#8dfefb` (hottest, about 0.2 R) through `#52eaf4` to `#4380e8` at the limb. Hue rotates **179° → 218°**, and value stays at 0.91 or above.
- Outer plasma: a wobbly white-blue blob ring `#72d7f8`/`#d0f2fb`, 30–40 px thick, with detached droplets and bubble rings around it.
- Glow: falls to the background (`#09234d`) by R+130.
- Light rays behind the star; ring-shaped spots with white glowing cores.

### 3e. Rim light from a neighbouring light source (L 1:22.5 `L_1m22s50_ignition-eclipse.jpg`)

A dark planet in front of a star gets a **two-band rim** on the side facing the star:
1. a pure white band (`#fefefe`) about 12 px wide;
2. a saturated orange band (`#f4972f`) about 25 px wide;
3. then the planet's own shadowed colour (`#650434`).

The edges are hard. This is how they sell backlighting without blur.

### 3f. Stepped glow (2017 style, I 0:52, I 0:44)

The glow is built from 3–5 flat concentric bands (cyan → magenta → violet → indigo, I 0:52), with no blur. It reads as "graphic", and L replaced it with real gradients. Use stepped bands only for diagrams and HUD-like graphics.

---

## 4. Lighting

- **One key light per scene**, almost always the star in frame or just off it. Opaque objects show it through the highlight-disc position, the shadow crescent side and the rim side (L 0:30, L 1:22.5, L 2:26).
- **Glow on every emitter**: stars, sparkles, moon, tiny star specks (soft dots, I 7:06), screen content (L 8:36: the monitor image glows violet onto the bezel).
- **Light rays.** Soft wedge rays behind stars (L 3:14, L 6:54, L 4:42). Hard white ray bursts appear only at climaxes: flare at L 1:48, supernova at L 5:50, eruption at L 6:52.
- **Lens artefacts** are used deliberately at moments of intensity:
  - L 1:21–1:23: a grey disc ghost (`#4d536b`, about 30 % opacity) plus a purple hexagonal aperture ghost (`#8a6ab7`), sliding against the light's motion;
  - L 1:48: a 4-point star flare with arms about 0.4 of the frame width.
- **Sparkles** (L 6:54 crop): 4-point crosses with thin arms (1–2 px, ±60–80 px long), a soft round core glow, and sometimes a thin ring halo. Size-varied and sparse: about 10–15 per frame in nebula shots.
- **Bloom** stays tight. Measured halos fall to the background within 0.1–0.3 R. There is no full-frame haze. Bright areas stay crisp-edged, and the glow sits *behind or around* the shape, never smearing over its interior.
- **Flash transitions to white** at peak events (L 5:50 → 5:52 → "RED GIANTS" on white at 5:54; L 7:52; L 9:52). White fills the whole frame for about 0.5–2 s.

---

## 5. Depth

**Space scenes (L), 3–5 planes:**
1. a flat saturated background colour, never pure black;
2. low-contrast large shapes (nebula clouds 2–3 tones above the background, L 2:34, L 6:54, L 8:04);
3. a star/dust field of two sizes (measured density **170–270 specks per megapixel**, about 350–560 per 1080p frame; median speck about 28 px area ≈ 6 px diameter; the largest are soft glows up to about 30 px);
4. the hero object, plus labels;
5. a foreground element cropped by the frame edge: a planet arc in the bottom-right corner (L 6:54), a giant planet limb (L 0:12, L 10:16), or bubbles and sparkles in front.

**Landscape (I 7:06 `I_7m06s_lake-landscape-pan.jpg`), 6 planes.** Value rises monotonically toward the camera, and hue moves from violet-blue to cyan:

| plane | colour | H | V |
|---|---|---|---|
| sky (top → horizon, darker toward horizon) | `#240073` → `#0f0450` | 259° → 249° | 0.45 → 0.31 |
| mountains (lit / shade facet) | `#1c478b` / `#173a7a` | 217–219° | 0.55 / 0.48 |
| far hill | `#073e99` | 217° | 0.60 |
| mid hill | `#0b90cb` | 198° | 0.80 |
| near hill | `#15c1e7` | 191° | 0.91 |
| foreground grass | `#13e3fd` | 187° | 0.99 |

- **Atmospheric fade = value plus hue toward the sky, not desaturation.** Saturation stays at 0.8–1.0 on every plane, and each plane adds about +0.1 V.
- Depth blur is almost never used. Background planes stay crisp. Softness appears only on glowing specks.
- **Parallax is subtle.** In the measured pan (C, 6 s), the background bands (sky, mountains, hills) moved the same 938 px at 1920 width, and the foreground band moved 1042 px (**1.11×**). Kurzgesagt moves most layers together and gives only the nearest layer extra speed.
- **Scale-comparison staging** (the format of L): objects stand on the isometric floor (L 0:30). Depth comes from the floor grid, cast shadows and the cube scale reference, not from perspective.

---

## 6. Texture

- **No measurable grain.** In flat regions, the median absolute residual against a 3×3 blur is 0.0 levels on every frame (`data/*_2s.json`, `grain`). Either there is none or YouTube compression removed it. Any noise texture we add must be ≤ 2 % opacity or it will look dirtier than the reference.
- **Gradients are used, but sparingly.** They appear on emissive bodies (star radial gradients, §3c/3d), glows and light rays, and as large soft light spill. In L 2:00 the floor near the star shifts from `#3c2da0` (H 248°, S 0.73) to `#654994` (H 262°, S 0.50) at about the same value. The warm glow is added over the floor (screen/add with a pink-orange tint), which desaturates it and warms its hue instead of brightening it. The spill reaches about 0.5 R beyond the limb. The sky in I 7:06 is a vertical gradient.
- **Texture is made of discrete shapes, not pixels**:
  - speckle dots (star surfaces: hundreds per star);
  - repeated crescents and bubbles;
  - band patterns with drip edges.
  
  This is "hand-placed micro-detail", which code can generate procedurally (seeded scatter with size and tone jitter).

---

## 7. Detail density

Approximate counts in L 6:54:
- 1 hero star;
- about 30 surface rings and bubbles, 200+ surface speckles;
- about 14 nebula blobs in 3 tones;
- about 12 sparkles;
- about 300 background dust specks;
- 1 foreground planet arc;
- light rays.

Other frames:
- L 3:14: 1 star, about 60 corona crescents, about 15 spots, hundreds of speckles, 16–20 rays, about 125 visible background specks on the left third alone (207 per megapixel).
- L 0:30: 2 planets, 2 cubes, 2 labels, 1 floor grid, about 20 surface motifs on Jupiter.

Rules:
- **There is always a micro layer.** Every frame has a field of tiny elements (stars, dust, speckles, bubbles) on top of the 1–3 large shapes.
- **Hierarchy by size**: one hero at 30–60 % of frame height, 0–4 supporting objects at 5–25 %, and hundreds of micro elements at 0.2–1 %.
- **Detail lives on the hero.** The background stays calm (low contrast), and the hero carries the dense texture.

---

## 8. Character design rules (study only, never reuse their characters)

Seen at L 0:44 (faced brown dwarf), L 8:36, L 10:36 and L 11:24 (birds), I 0:00 (black hole face), I 1:04 (swimmer), I 1:24 (astronaut), I 3:26 (penguin lecturer), I 4:50 (duck with mirror).

- **Objects become characters by adding only eyes**: big round eyes with a coloured sclera that matches the body palette (yellow on the brown dwarf), small pupils, and eyelid shapes that carry the emotion (worried brows, half-closed lids). At most a tiny mouth. The face sits high on the body, and the body's own pattern stays intact (L 0:44, L 1:18–1:22).
- **Creatures are bean or blob silhouettes** with no outlines, 2–3 flat tones (base, one shadow shape, one highlight shape), stick limbs drawn as thick round-capped strokes, and flat beaks and feet in a contrasting warm colour.
- **Eyes are white ovals with a black pupil**, often only one eye visible in profile. Expressions use a simple lid cut.
- **Characters stay small** in scene shots (15–30 % of frame height) and are posed in action. They are props in an environment, not talking heads.
- **Hero humans and astronauts get more value steps** (I 1:24: white suit with lavender shadow shapes, a visor reflection band) but still no outlines.
- **Character palettes are pulled from the scene palette.** Characters do not bring new hues, except one warm accent (beak, feet).

---

## 9. Motion craft

**Always-on motion (L, 30 fps difference analysis, `data/L_motion.json`):**
- Seconds with essentially no motion (energy < 5): **5.4 %** (39 of 718).
- Fully frozen runs ≥ 1 s: 11 in the whole video. The longest are 5.6 s (a twinkling-only star map, L 7:30) and 3.2 s (white flash/title, L 5:52). All others are 1–2 s.
- I: 9.3 % of seconds are near-static, and frozen runs are ≤ 3.3 s.
- What moves during "holds": twinkling specks, rotating or bubbling star surfaces, a corona that crawls, drifting nebula (L 6:54, top and bottom bands drifting ±2–3 px/s in opposite directions = slow rotation), blinking and glancing eyes (A sheet: the eyes move twice in 4 s), and slow camera pushes.

**Camera:**
- Slow push-in on held subjects: **+0.76 %/s** zoom (L 6:54.5 → 6:58.5).
- The opener nebula pushes in at ≥ 2.7 %/s (L 0:02).
- Many scale-comparison shots keep the camera locked (L 2:48, L 3:48, L 8:36: < 0.1 %/s).
- **Pan ease:** in shot C (I 7:03.6–7:09.6), the position fits **ease-out quad** (RMSE 0.024; ease-out sine 0.034; ease-out cubic 0.11; linear 0.16). Speed falls about linearly from ≈ 340 px/s to ≈ 50 px/s over 6 s, and the camera keeps drifting instead of stopping.

**Object entrances (60 fps, L 0:29.55–0:31.0, the cube sliding in from the bottom-right corner, `tools/pop_curve.py`):**
- Travel of 459 px (cx 1873 → 1414) over **1.1 s**, position fitting **ease-out quad**: 27 % at 0.15 s, 50 % at 0.30 s, 71 % at 0.45 s, 85 % at 0.65 s, 94 % at 0.85 s.
- Settle: after arrival, the measured height oscillates 407 → 380 (−6.6 %) → 410 → 390 (−4 %) → 407 px, a damped wobble with a period of about 0.35–0.4 s that settles by 31.0 s. This is likely a squash/stretch settle (secondary motion). Width stays at 392 px.

**Cut rhythm:**

| | L | I |
|---|---|---|
| hard cuts (1–2 frames) | 20 | 26 |
| fast animated transitions (whip, zoom-through, wipe), duration median / p90 | 30, 0.20 s / 0.33 s | 52, 0.15 s / 0.30 s |
| detected shot-level events, median gap | 10.8 s | 5.4 s |
| **new visual element (any change: object, label, cutaway, move), counted by hand in L 0:26–1:06** | **≈ every 2.4 s** (17 changes in 40 s) | — |

So **shots are long (≈ 6–20 s), but something new enters every 2–3 s within the shot**. Kurzgesagt cuts rarely. It keeps the eye busy by adding and transforming elements in place: labels appear, a cube slides in, the planet splits into a cutaway (L 0:34, L 1:04, L 2:26), a second star rolls in.

**Transition vocabulary (frame references):**
- Zoom/slide match: Earth pulls back, then the giant planet slides in (L 0:12–0:20).
- Cutaway split: the planet halves rotate open to show layers (L 0:34, L 1:04, L 2:26, L 5:00).
- Horizontal wipe in 0.25 s (I 7:03.0–7:03.25, `q_C_bh_7m03_01.jpg`).
- Flash to white, then a title card on white (L 5:50–5:54).
- Iris/ring burst (L 2:16, L 9:52).
- Split screen with a tinted half (L 2:06–2:18).
- Fast eruption (L 6:52) with a hard cut to the next subject at 6:54.25 (`q_B_star_6m52_01.jpg`).
- Fade through the starfield (L 7:30).

**Easing defaults to adopt:** ease-out quad for travel and pans, a short damped overshoot (≤ 7 %, 2 cycles, about 0.35 s period) on arrival, and constant slow drift (0.5–1 %/s zoom or 2–5 px/s) on holds.

---

## 10. Typography and on-screen text

- **Object labels** (L 0:30, L 2:26, L 3:20):
  - geometric sans, semi-bold, pale lavender (≈ `#c0c4f4`, estimated visually) on the floor colour;
  - cap height ≈ 36 px at 1080p (3.4 % of frame height);
  - underlined by a 4 px round-capped leader line in the saturated floor accent `#6d60e1`, with a 30–45° kink at the end pointing toward the object;
  - sub-labels (mass, radius, lifespan) at about 55 % size and lower contrast below the name (L 2:24 "Red Dwarf / Mass 100 × Jupiter's mass").
- **Section titles (L)**:
  - all caps, thin geometric sans, **very wide tracking (≈ 0.5–0.6 em)**, white on navy or navy on white;
  - small: cap height ≈ 2 % of height, centred, stacked over 2–5 lines;
  - tiny lowercase connector words between the lines ("THINGS / that would / LIKE / to be / STARS", L 0:08);
  - also laid over the hero (L 1:26 "MAIN SEQUENCE STARS" on the star).
- **2017 titles (I)**: bold caps in a Montserrat-like font, large (I 0:52 "EVENT HORIZON" at about 13 % of frame height), and framed cards with corner brackets (I 2:34, I 4:30).
- **Data tags**: rounded flags with a pointer, saturated fills (Birth `#0ebb69`, Main Sequence `#efa212`, Giant Phase `#b42a48`), white text, and a progress bar underneath (L 1:52–2:16).
- Little text overall. Labels stay up only while the object is discussed. There are no subtitles burned into the picture.

---

## 11. Sound design

Measured on the downloaded YouTube audio:
- **Integrated loudness**: −16.5 LUFS (L) and −15.1 LUFS (I). **Loudness range 2.8 / 2.6 LU**, i.e. heavily compressed and even.
- **Never silent**: L has 0 stretches ≥ 0.4 s below −45 dBFS, and I has 1. A continuous music or ambience bed sits under everything.
- **Narration pace**: 150 wpm (L) and 165 wpm (I) over the narrated span; 166 / 191 wpm inside cues. Only one narration gap over 1.5 s in L (the outro).
- **Music-only breather**: in I, a 10.9 s gap after the hook (0:15–0:26), filled with music and sound effects, before the title sting "Black holes in a nutshell".
- The sound-effect proxy (high-band rise at visual events vs. random times, `data/*_audio.json`) was **inconclusive**: high-frequency onsets (≈ 107/min) are dominated by speech consonants. To quantify sound effects, a voice/music separation step is needed (e.g. Demucs on CPU), which was not done here.

General knowledge, not measured here: Kurzgesagt's music and sound effects are made by Epic Mountain. The score is a soft synth/orchestral ambient bed. Sound effects are small, tonal and frequent: plinks and chimes on pop-ins, airy whooshes on transitions, deep booms with sub-bass on explosions and flashes. They land on the animation frame.

---

## 12. What this means for our code (input for STYLE_BIBLE.md)

1. **Palette tokens per scene type** from §1. Space scenes are cool violet/navy fields with one warm hero. Background V is 0.15–0.20 and saturated. Never use #000 or grey.
2. **Two shader recipes:**
   - Opaque: base + a 13 % light disc at the upper left + a hard crescent multiplied by the environment hue (about −33 % V, −10° hue) + a soft cast shadow (floor × ≈ 0.6) with a darker contact core.
   - Emissive: a radial gradient rotating 35–40° of hue toward red or blue at the limb with value kept, a double rim crescent, a tight halo (0.1 R) plus a faint tail (0.3 R) with outward hue rotation, and 16–20 soft rays at 10–15 %.
3. **Micro-detail generators**: seeded speckles (hundreds per hero), concentric-ring spots, corona crescents, and a two-size star field at ≈ 200 per megapixel with soft glow on the largest 10 %.
4. **Depth**: 3–5 planes, value +0.1 per plane toward the camera, hue shift toward the sky with depth, no blur, parallax ≈ 1.1× on the nearest layer only, and a cropped foreground element in most space shots.
5. **Motion**: ease-out quad for travel and pans, a damped ≤ 7 % settle on arrival, always-on ambient motion (≤ 5 % static seconds; no frozen hold over 2 s except title cards), and a new element every 2–3 s inside long shots.
6. **Typography**: a wide-tracked thin-caps title style plus semi-bold labels with kinked leader lines.
7. **Audio**: a continuous bed, LRA ≈ 3 LU, about −16 LUFS for YouTube delivery, 150–165 wpm narration, and one music-only breather after the hook.
