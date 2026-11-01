# The Infographics Show style study (measured)

This is an internal study. The goal is to learn the **style rules** behind The Infographics Show (TIS), the owner's example of "clearly better than us", so we can author our own art in code (Remotion, SVG, Canvas, WebGL). We do not copy their characters (the recurring lab tech, scientists, reaper, politician caricatures), their stock-vector environments or their compositions.

Read this next to `study-kurz-space.md` and `study-kurz-bio.md`. Kurzgesagt is the target. TIS is the step between us and Kurzgesagt, and several numbers below use the same tool as those studies, so the three can be compared column by column.

## Sources and method

| key (file prefix) | video | id | uploaded | views (2026-11-01) | length | fps |
|---|---|---|---|---|---|---|
| **fDz** | World War 3 Protocol. Why Global Nuclear Annihilation Is Inevitable. (owner's example; a compilation of 10 earlier episodes) | `fDzCHPWkou4` | 2026-10-31 | 193 k | 3:11:22 | 30 |
| **O4y** | What Lethal Radiation Does to Your Body (Hour by Hour) | `O4yWBv2Nj68` | 2026-10-04 | 2.49 M | 18:07 | 60 |
| **UOUM** | Voyager 2 Discovered Something Strange at the Edge of Our Solar System | `UOUM1QT5GgU` | 2026-09-24 | 1.95 M | 33:15 | 60 |

O4y and UOUM are the 2nd and 3rd most-viewed of the channel's last 60 uploads. The 1st, `MgngwkPAuqQ` "The AI bubble is about to pop" (3.9 M), was skipped because it is finance commentary. The two picked are body and space explainers, which match our niche.

On the Spark (`~/studio/refs/kurz-style/infographics/`, CPU only, `nice -n 10`, ≤ 4 ffmpeg threads per job):
- 1080p video. O4y and UOUM are H.264 1080p60. fDz is VP9 1080p30, downloaded over HLS because the progressive stream was throttled to about 50 KB/s.
- Frames every 2 s: 544 (O4y), 997 (UOUM) and 5741 (fDz).
- Frames every 0.25 s plus every source frame (640 px) over three 5-second stretches per video:

| stretch | video and time | what happens |
|---|---|---|
| reaper | O4y 0:16–0:21 | whip transition, then a pull-back over a night graveyard |
| infobuild | O4y 1:24–1:29 | static infographic board building up |
| fall | O4y 2:06–2:11 | character collapses, flash and camera shake |
| launch | UOUM 0:08–0:13 | launch pad, then a split-screen with archival film |
| helio | UOUM 0:46–0:51 | space pull-out and kinetic label |
| scientist | UOUM 2:04–2:09 | slide transition, then a speech bubble pop |
| sitroom | fDz 0:00:20–0:00:25 | ring zoom-through into a situation room |
| face | fDz 0:50:40–0:50:45 | close-up acting, then a white flash |
| mushroom | fDz 2:00:20–2:00:25 | pull-back on a nuclear cloud, then a hard cut |

- Per-frame scene scores (160 px proxy, every frame) give the cut and transition rhythm.
- EBU R128 loudness, 0.1 s band envelopes and spectrograms give the sound measurements.
- The same tools were run on our own pilot `out/pilots/explainer-orca/explainer-orca_16x9.mp4` as a baseline ("ours").

Tools are in `tools/tis/` (committed). Raw outputs are in `data/tis/` (committed):

| tool | what it measures | output in `data/tis/` |
|---|---|---|
| `extract.sh`, `extract1.sh`, `dense.sh`, `scores.sh` | 2 s grid, 0.25 s and full-rate stretches, per-frame scene scores | — |
| `frame_metrics.py` + `aggregate.py` | palette, colour counts, S/V, outline response, edge density, gradient share, grain, vignette, defocus share; split by dark, mid and light frames | `*_stats.txt`, `stills_metrics.json` |
| `../frame_stats.py` (the Kurzgesagt studies' tool) + `kfs_summary.py` | numbers comparable 1:1 with `study-kurz-*.md` §1 | `palette_comparable.txt`, `*_frame_stats.json` |
| `cuts.py` | hard cuts, animated transitions, shot lengths, share of frames that are moving | `*_scene_events.json`, `*_stats.txt` |
| `gridchange.py` | how often the picture changes (consecutive 2 s frames) | `*_stats.txt` |
| `motion.py` + `easefit.py` | camera scale, pan and rotation per frame (ORB + RANSAC), ambient residual, easing fits | `motion/*.csv` |
| `density.py` | shapes and micro-details per still | `stills_density.txt` |
| `probe.py` | pixel, line and box probes for the shading recipes | — |
| `audio.sh` + `audio.py` | loudness, music bed, pauses, transition-locked SFX test | `*_audio.txt` |
| — | our orca pilot through the same tools | `ours_orca_baseline.txt` |

Reference images are local only and ignored by git (`refs/`, see `.gitignore`; third-party frames are not committed):
- `refs/infographics/stills/*.jpg`: 40 full-resolution stills. They are named `O4y_MMSS`, `UOUM_MMSS` and `fDz_HMMSS` (`fDz_20550` = 2:05:50).
- `refs/infographics/sheets/<id>_2s_NN.jpg`: 2-second contact sheets for O4y and UOUM, 100 frames each, labelled with timestamps.
- `refs/infographics/sheets/fDzCHPWkou4_10s_NN.jpg`: 10-second sheets for the 3-hour fDz.
- `refs/infographics/sheets/<id>_dense_<stretch>_00.jpg`: the 0.25-second sheets.
- `refs/infographics/sheets/spec_*.png`: audio spectrograms.
- The Spark keeps everything (all grid frames, videos, full-rate PNGs) under `~/studio/refs/kurz-style/infographics/`.

**How to read references:** "O4y 0:18" means video O4y at 0:18; its still is `refs/infographics/stills/O4y_0018.jpg` when one exists. Otherwise, look at that timestamp in the 2 s contact sheets.

Caveats:
- YouTube compression sets a noise floor, so film grain cannot be measured; the "grain" metric reads about 0.6 for every source, ours included.
- The scene-score transition threshold (windowed sum ≥ 0.2) was checked by eye against the sheets for O4y. fDz is 30 fps, so its windows are 10 frames and its counts are slightly less comparable.
- Fonts are identified by eye, not confirmed.
- Sound conclusions come from signal analysis without listening. §11 says what could and could not be separated.

---

## 0. Summary: what TIS does that we don't (and where TIS is still below Kurzgesagt)

1. **The picture changes about every 3 s, but it rarely cuts.**
   - A new composition arrives every 3.2 s (O4y), 2.8 s (UOUM) and 3.1 s (fDz).
   - A visible change arrives every 2.0–2.3 s.
   - Ours: a new composition every 10.6 s.
   - TIS gets there by moving the camera through one large illustrated set and adding overlays, not by cutting. There are 0 hard cuts in UOUM's 33 minutes.
2. **Characters act in every scene.** A recurring cast of flat rigs is animated at 60 fps with 0–7 % duplicate frames. Ours has no characters.
3. **Each scene owns one colour key**, for example a purple room, a teal night or a cream infographic board.
   - Median 8–9 colour clusters per frame; the largest covers 25–29 % and the top three about 60 %.
   - TIS uses 3–4 hue families per frame. Ours uses 1.
4. **The picture is light and low-saturation.**
   - Chromatic saturation median 0.52–0.57, against 0.76–0.97 for Kurzgesagt and 0.70 for ours.
   - Median value 0.68–0.81 in non-space videos, against 0.31 for ours.
   - Near-white covers 2.6–13 % of the frame (cards, lab coats, boards). Kurzgesagt keeps it at 0.2 %.
5. **Shading is minimal: two flat tones with a hard split.**
   - Skin shadow ΔL* −3.5 to −8, cloth −5 to −6, buildings −11, planets −15 to −20.
   - There are no highlights or rim lights on characters.
   - This is the main craft gap to Kurzgesagt, which uses hue-shifted multi-tone shading, rims and glows (see `study-kurz-bio.md` §3).
6. **Glows are reserved for emitters:** the moon, the sun, stars, explosions and some infographic accents. There is no global bloom.
7. **Depth comes from 3–5 value-stepped planes.** Far planes are lighter and less saturated; near planes are dark, saturated silhouettes. There is also real depth-of-field blur (σ ≈ 20 px) on foreground and background elements.
8. **The camera eases out after every transition, then keeps drifting.**
   - Moves fit out-quad, out-quart or out-sine and reach 90 % of their travel in about 0.9–1.6 s.
   - Long holds use a linear 8–10 %/s pull-back or push.
9. **Detail density** is about 1.5–2× ours.
   - Median 142 shapes and 843 micro-details per frame (ours: 53–126 and 331–604).
   - Edge density 0.040–0.051 (ours: 0.026).
   - Much of this density comes from detailed flat-vector environments (inferred: stock-vector packs).
10. **Text is designed UI, not captions:** date and time cards, speech bubbles, heavy all-caps title cards, kinetic labels and a permanent logo bug. They never burn in captions.
11. **Sound:** narration at about 180 wpm, compressed to an LRA of 2.1–2.6 LU, over a continuous music bed 12–20 dB below the voice. The mix never drops to silence. No consistent whoosh on transitions could be detected.

---

## 1. Palette

**Whole-video statistics.** The Kurzgesagt tool (`tools/frame_stats.py`) was run on frames every 4 s (O4y, UOUM) or every 10 s (fDz). Output: `data/tis/palette_comparable.txt`.

| metric | O4y (body) | UOUM (space) | fDz (WW3) | Kurzgesagt L (space, from `study-kurz-space.md`) | **ours (orca)** |
|---|---|---|---|---|---|
| median saturation, all px | 0.23 | 0.43 | 0.36 | 0.82 | 0.75 |
| median saturation, chromatic px | 0.57 | 0.57 | 0.52 | 0.76 | 0.70 |
| median value | **0.81** | 0.37 | 0.68 | 0.62 | **0.31** |
| dark-background frames (border V < 0.25) | 6 % | 39 % | 6 % | 25 % | 63 % |
| hue families per frame, median (p10–p90) | 3 (2–5) | 3 (1–5) | 4 (2–6) | 3 (1–7) | **1 (1–3)** |
| 4-bit bins covering 80 % / 95 % | 12 / 52 | 11 / 54 | 17 / 78 | 13 / 61 | 10 / 26 |
| largest cluster / top-3 coverage | 29 % / 61 % | 25 % / 59 % | 26 % / 58 % | 30 % / 64 % | 18 % / 50 % |
| near-white share (V > 0.92, S < 0.15) | **13.4 %** | 3.6 % | 2.6 % | 0.2 % | 1.9 % |
| dark share (V < 0.2) | 0.1 % | 9.1 % | 0.5 % | — | 18.9 % |

**Hue mix of chromatic pixels:**
- O4y: red–orange 0–30° = 22 %, cyan 180–210° = 24 %, magenta-red 330–360° = 15 %, blue 210–240° = 12 %.
- UOUM: blue 210–240° = 26 %, cyan = 21 %, violet 240–270° = 16 %, red = 13 %.
- fDz: spread across all hues, with cyan 22 %, red 17 %, blue 13 % and orange 11 %.
- Ours: **94 % in a single 30° bin** (cyan 180–210°).

**Colours per frame** (`frame_metrics.py`, k-means k = 10, clusters ≥ 2 % of the frame): median 9 (O4y), 8 (UOUM), 9 (fDz).

**Brightness classes:**

| | dark (mean L* < 30) | mid | light (≥ 70) |
|---|---|---|---|
| O4y | 7 % | 42 % | 52 % |
| UOUM | 34 % | 61 % | 5 % |
| fDz | 8 % | 68 % | 25 % |
| ours | median frame L* 27 (everything dark) | | |

**Hex palette per scene type.** Values are k-means colour : coverage %, or point probes (`tools/tis/probe.py`).

| scene type | ref | key / background | mid tones | accents |
|---|---|---|---|---|
| Warm-dim interior with character | O4y 0:00 | wall `#674064` (52 %) | shirt `#bfb1a5` / `#a19388`, metal `#aa9dc5`, hair `#36231c` | skin `#f5977e` / `#ea8d7e`, white tee `#fdfaf5` |
| Night exterior, monochrome | O4y 0:18 | sky `#055669`, far hills `#378d9c` | mid ground `#268394`, tombstones `#022d40` | FG `#011a1f`, moon `#fefefe`, icons `#fadf5a` |
| Industrial lab, desaturated | O4y 0:24 | `#6c655c` (23 %), `#a1998d` | `#b3a9a0`, `#787570`, `#90887f` | UI card `#f8f8f8`, icon `#f59806` / `#0203fd` |
| Title card | O4y 0:38 | `#161837` (54 %), `#281e48` | blurred motif pattern `#4c3762`, `#3a2a53` | text `#ede9ea` |
| Infographic board | O4y 0:52, O4y 3:16 | cream `#fef6eb` / `#f8f3ea` (65 %) | icon wallpaper about 6 % darker than the cream | card headers `#205088`, `#e5642d`, `#683790`, `#089587`; yellow liquid `#ebcb7e` |
| Clinical teal | O4y 2:42, O4y 2:56 | tile wall `#45c2ae` (34–49 %) | uniform `#c2b7aa` / `#a89c8e` | water `#11defb` with highlight `#baf4ff`, skin `#e78c7d` |
| Macro body (one hue) | O4y 8:30 | `#76192d` (47 %) | `#ad213c`, `#9b1f36` | `#cf2842` |
| Deep space | UOUM 0:00, UOUM 0:22 | `#020441` / `#000235` / `#000127` (≈ 75 %) | dust `#312e4e` | specks `#fafbfc`, planets `#ebd047`, `#6d97c3` |
| Daylight sky | UOUM 0:08 | gradient `#0b7dd5` → `#73ebd8`, horizon `#b4fafc` | far hills `#5ed5d9`, ground `#76505d` | pink-red gantries, white rocket `#dadada` |
| Star close-up | UOUM 0:30 | `#261d1b`, `#402820` | `#663725`, `#ea8228` | `#faf641`, `#ea3e0f` |
| Nebula | UOUM 11:56 | `#25044c` (22 %) | `#4c1e6f`, `#6d4387`, `#946ba5` | `#dbd3ef`, white starbursts |
| Gas giant, muted | UOUM 20:16 | `#4a595d`, `#3f4041` | `#a07665`, `#80594f`, `#665961` | probe gold, white swirl strokes |
| Mission control | UOUM 1:56, UOUM 21:32 | `#c0b2a0`, `#545675` | `#6e798b`, `#8e8fa7` | screen navy `#263a60`, `#1b1f39` |
| Situation room | fDz 0:00:20 | `#472f56`, `#312343` | `#564f8a`, `#7076b3` | monitor blues, camo |
| Nuclear blast over city | fDz 2:00:20 | sky `#ca7236` / `#e38b36` (textured) | skyline `#643432`, `#b65733` | cloud `#fdffb2` → `#43100c`, embers red |
| Dusk skyline | fDz 2:00:40 | `#e39baa`, `#f1b0a9` | `#76565b`, `#778092` | `#76a59b`, `#c38fba` |
| Neon city | fDz 0:15:30 | `#2e065e`, `#19023b` | `#470f82`, `#5a19b0` | `#af44ae`, `#781ce2` |
| Flat diagram on colour | fDz 0:09:00 | `#3f0264` (76 %) | globe greys `#aab5bc` | landmark colours |

**Rules derived from this:**
- **One key per scene, then neutrals.** The background or set colour takes 25–50 % of the frame. Characters and props sit on top in their own fixed, mostly low-saturation colours: khaki `#b4a699` is S 0.15, lab coats are near-white.
- **Lighter and greyer than Kurzgesagt.** Chromatic saturation is about 0.55 against Kurzgesagt's 0.76–0.97. White UI and white coats are common.
- **Complementary pairing.** A cool set colour (teal, navy, purple) sits under warm skin (hue 8–12°) and yellow or orange accents: radiation icons `#fadf5a` on teal, the sun `#faf641` on navy.
- **Our gap is the opposite of TIS.** We are saturated, dark and monochrome: one hue family, 19 % of pixels below V 0.2.

---

## 2. Shape language

**No silhouette outlines on characters, sets or planets.**
- The outline metric is the share of edges that are a thin dark line ≥ 45 L* darker than their surroundings. Median: 0.086 (O4y), 0.102 (UOUM), 0.052 (fDz).
- Character close-ups score 0.003–0.04 (O4y 1:04, O4y 2:28, fDz 0:50:40).
- High scores come from text cards (O4y 0:38: 0.48) and dark UI (UOUM 2:06: 0.55, the black bubble text). They do not come from linework.
- Ours measures 0.29, mostly from dark text and thin strokes on dark water.

**Where lines do appear:**
- 1–3 px internal detail lines on machines: dish ribs and the truss on the probe (UOUM 20:16), stair stringers (UOUM 0:08), monitor UI (fDz 0:00:20).
- 2 px white strokes for storm swirl rings (UOUM 20:16).
- Glasses (O4y 8:06).
- About 3 px coloured borders on infographic cards (O4y 0:52).
- Dark contour icons on the boards (the barrel, O4y 0:52).

**Geometry:**
- Characters are rounded rectangles and tubes.
  - Arms are constant-width tubes (about 110 px at close-up, UOUM 2:06) with no elbow break.
  - Hands are plain skin-coloured circles (≈ 55 px, O4y 0:18) or mitten shapes (UOUM 2:06).
  - Heads are egg shapes. Hair is one lobed blob.
- Clouds and explosions are stacks of overlapping circles: about 25 circles per cloud layer and 4–5 layers (fDz 2:00:20, fDz 2:05:50).
- Sky clouds are flat streak shapes with pointed ends (UOUM 0:08).
- Buildings and machines are sharp-cornered boxes with a 2-tone side face (fDz 2:00:20, O4y 0:24).

**Corner radii (estimated by eye at 1080p):**
- date and time cards ≈ 8 px;
- infographic cards ≈ 16 px;
- speech bubbles ≈ 24 px (UOUM 2:06);
- title text sits on no box (O4y 0:38).

**Stock-like environments.** City skylines, the Middle-East old town (fDz 2:05:50), the neon city (fDz 0:15:30) and the moon window view (UOUM 21:32) have a denser, more painterly vector style than the characters: brick strokes, palms, window rows. This is inferred, not confirmed: TIS composites licensed flat-vector environments with its own character rigs. For us, the code equivalent is a library of procedural set generators (skylines, interiors, landscapes) that we write ourselves.

---

## 3. Shading recipe per object (inferred from pixel probes)

Blend modes are inferred from values. "Flat" means a constant fill with no gradient inside the shape.

| object | ref | base | shadow side | highlight | rim | inner glow | cast shadow |
|---|---|---|---|---|---|---|---|
| Skin, close-up | O4y 0:00 | `#f5977e` (L* 71.6) | `#ea8d7e` (L* 68.1): ΔL* −3.5, hue −4° (redder), hard vertical split down the face centre | none | none | none | neck `#dd7f77` (ΔL* −8.4) under the jaw |
| Skin, tilted head | O4y 2:42 | `#f39780` (71.4) | `#e07f79` (63.7): ΔL* −7.7, hue −8°, diagonal split | none | none | none | — |
| Khaki shirt | O4y 0:00, O4y 2:42 | `#b4a699` (69.0) / `#c5b7aa` (75.2) | `#a6988b` (63.7) / `#b2a897` (69.3): ΔL* −5.3 to −5.9 | none | none | none | pockets and collar drawn as darker flat shapes |
| Lab coat | O4y 8:06 | `#e7e1e1` (90.0) | 3 flat steps: `#d8d6d7` (85.8), `#bfbbbc` (76.2), `#adabac` (70.2) | none | none | none | none |
| Hair | O4y 0:00, O4y 2:42 | `#36231c` (L* 15.9), one tone | none | none | none | none | none |
| Planet (Uranus) | UOUM 11:44 | `#b9eaf9` (90) | band `#a5dff3` (85.6); terminator crescent `#66b2ed`–`#81c0eb` (70–75): ΔL* −15 to −20, S +0.2 to +0.3, hue +10° (bluer); a large offset circle with a hard edge | lighter flat cloud streaks `#d7f2fa` | none | none | — |
| Building | fDz 2:00:20 | front `#889aa4` (62.5) | side `#727b82` (51.1): ΔL* −11 | window glint `#6dd9db` (80.7) on dark glass `#005263` (31.7): one diagonal light band per pane | none | none | none |
| Rocket (cylinder) | UOUM 0:08 | `#dadada` (87.1) | 3 vertical flat stripes: `#cdcdcd` (82.4) / `#dadada` / `#e9e9e9` (92.3) | brightest stripe right of centre | none | none | none |
| Telescope (cylinder) | UOUM 11:56 | `#d5d6ff` (86.7) | ring stripes `#b0b1f2` (74.2): ΔL* −13, same hue | none | none | none | none |
| Nuclear cloud | fDz 2:00:20 | 5 tones by height: `#fdffb2` (98) → `#faea70` (92) → `#f59524` (70) → `#c60f2e` (42) → base `#43100c` (13) | lower = darker, redder | top layer near-white | pale torus ring `#cd943d` with a lighter edge | — | dark smoke under the cap |
| Water / splash | O4y 2:42 | `#11defb` (81.5) | none | elongated white specular `#baf4ff` (92.7), about 20–30 % of the drop's length | none | — | none |
| UI card | O4y 0:24, UOUM 0:08 | `#fdfbfc` | — | — | — | — | soft drop shadow: L* 62 → 72 over 14 px below and 12 px right (≈ 35–40 % black, blur ≈ 12 px, offset ≈ 4 px) |
| Title text | O4y 0:38 | `#ede9ea` (92.5) | — | — | — | — | 3–4 px directly below, only ΔL* −4 against the background (almost invisible) |

**Rules:**
- **Two flat tones, with a hard edge.** Shadow deltas are small on people (skin ΔL* 3–8, cloth 5–6) and larger on environment objects (buildings 11, cylinders 5–13 per stripe, planets 15–20).
- **Hue shift is mild:** 4–8° on skin (toward red), about 10° on planets (toward blue). Kurzgesagt shifts 10–25° toward blue or violet. Shadows gain saturation (planet +0.2 to +0.3).
- **Highlights are rare.** They appear only on water, glass and window glints and the tops of clouds. Characters get no highlight, rim light or inner glow.
- **Cylinders are faked with 2–3 flat vertical stripes**, not gradients.
- **Cast shadows are mostly absent.** Characters stand without ground shadows (O4y 0:18, UOUM 2:06). Only UI cards cast soft shadows.

---

## 4. Lighting

**No consistent light direction.** Each character rig has a fixed split side, and sets are lit evenly.

**Emissive glows (radial, additive or screen-like):**
- **Moon** (O4y 0:18): a flat white disc r ≈ 170 px. Measured along the horizontal line y = 120 from x = 1230 to 1700, the glow falls from L* 99.7 at the disc edge (x ≈ 1380) to the sky (L* 35) by x ≈ 1640 (≈ 260 px).
  - Half-way (L* ≈ 67) is reached ≈ 55 px past the edge.
  - The halo takes the sky's hue: H 191°, saturation rising 0.28 → 0.95 across the falloff.
  - The falloff is roughly exponential.
- **Sun** (UOUM 0:48): a core r ≈ 45 px at L* 99, then a yellow ring `#fff384`, then the background over ≈ 90 px. The hue turns from 55° to 230° as the glow fades into navy.
- **Starbursts** (UOUM 11:56): a white core ≈ 60 px wide plus 4–6 thin rays 150–250 px long; the glow fades to the nebula (L* 58) over ≈ 120 px. Smaller sparkles are 4-point stars 20–60 px across (UOUM 0:48).
- **Infographic glows:** an orange radial glow behind rotating arrows (O4y 0:52) and red-pink pulses on "criticality" (O4y 1:24 to 1:29, `O4yWBv2Nj68_dense_infobuild_00.jpg`).
- **Flashes:** a full-screen white bloom sweeps in from the right over about 1.5 s (fDz 0:50:43–0:50:45, `fDzCHPWkou4_dense_face_00.jpg`). A cyan ring burst marks a radiation flash (O4y 2:08.3, `O4yWBv2Nj68_dense_fall_00.jpg`).

**Scene relighting is done with colour keys, not light.**
- At night (O4y 0:18) the whole set is one teal family.
- The character is tinted toward it: the shirt goes from `#b4a699` (day, O4y 0:00) to `#949f99`, ΔL* −4.5, hue 28° → 147°. This is a colour overlay on the rig, not new shading.

**Light rays:** rare. The only examples are broad, very subtle lighter wall panels (O4y 0:00, ΔL* +2–3) and beams in title-card motif patterns. Volumetric light cones (Kurzgesagt's diegetic light) were not seen in these samples.

**Bloom:** only around emitters. The vignette is neutral: corner-to-centre L* ratio median 0.95–0.98 in mid and light frames. Space frames are darker at the edges (0.43–0.49), because the bright subject sits in the middle.

---

## 5. Depth

**Value-stepped planes.** The night graveyard (O4y 0:18) has 5 planes measured on the still:

| plane | sample | L* | S |
|---|---|---|---|
| sky | `#055669` | 33 | 0.95 |
| far mountains | `#378d9c` | 54 | 0.65 |
| mid ground | `#268394` | 50 | 0.74 |
| mid tombstones | `#022d40` | 17 | 0.97 |
| foreground silhouettes | `#011a1f` / `#02161f` | 6–8 | 0.94–0.97 |

The rule is that far planes are lighter and less saturated (atmospheric), and the nearest planes are near-black silhouettes in the key hue.

**Daylight atmospheric fade** (UOUM 0:08):
- The sky gradient runs from `#0b7dd5` (L* 51, H 206°) at the top to `#73ebd8` (L* 86, H 170°) at y = 560, then a pale horizon band `#b4fafc` (L* 94).
- The far hills `#5ed5d9` (L* 79–80) sit about 15 L* below the horizon band.

**Depth of field:**
- Measured with `blur_frac`, the share of textured 40 px tiles whose Laplacian variance is under 15 % of the frame's 90th percentile. Median 0.40 (O4y), 0.38 (UOUM), 0.37 (fDz); this includes motion blur.
- The foreground fire in UOUM 0:48 fades from L* 28.6 to 1.6 over ≈ 60 px, which suggests a Gaussian σ ≈ 20 px.
- Blurred backgrounds sit behind title cards (O4y 0:38: a radiation-icon motif pattern) and in the dark lab (O4y 8:06, right side).

**Parallax and planes in motion:**
- On the reaper pull-back (O4y 0:17.3–0:21), the residual motion after the global camera fit is 2.2 % of pixels per frame, the expected signature of planes moving at different rates.
- The foreground tombstones and grass move faster than the hills. Each plane is not tracked separately.
- **Plane count:** 3–5 in environment shots, 2 in character close-ups (character plus blurred set).

**Ours:** a single gradient-water plane with small subjects. There is no foreground plane and no near-black silhouette layer.

---

## 6. Texture

- **Grain:** the high-pass residual in flat areas is 0.59 / 0.58 / 0.66 (O4y / UOUM / fDz), the same as ours (0.60). That is the compression floor, so there is no measurable film grain.
- **Painted background textures:** these are the visible "richness" layer.
  - The nuclear sky (fDz 2:00:20) is mottled. A 400 × 300 patch has per-channel std 10–19 and 9–13 4-bit colours covering ≥ 1 % each, where a flat fill would have 1–2.
  - The lab (O4y 0:24) has smudge and stain overlays on the metal panels.
  - The heliosphere (UOUM 0:48) has low-opacity smoke wisps.
- **Gradients only on big fields.**
  - `grad_frac` is the share of flat-region pixels sitting on a smooth ramp: median 0.23 (O4y), 0.26 (UOUM), 0.21 (fDz). Ours is 0.50.
  - TIS gradients are skies, space nebulae and big glows. Objects are flat.
- **Patterns:**
  - Tone-on-tone line-icon wallpaper on infographic boards (O4y 0:52, O4y 3:16): 2 px strokes about 6–8 % darker than the cream.
  - Motif patterns behind title cards (O4y 0:38).
  - Camouflage on uniforms (fDz 0:00:20).
  - Brick dashes on stock buildings (fDz 2:05:50).

---

## 7. Detail density

`density.py` on the 40 stills (960 × 540 proxy, 16-colour segmentation):

| | shapes ≥ 0.03 % of frame | micro-details (4–149 px regions) |
|---|---|---|
| TIS, median (p10–p90) | **142** (64–286) | **843** (439–1827) |
| ours (6 orca frames) | 53–126 | 331–604 |

| | edge density (Canny px / all px), median (p10–p90) |
|---|---|
| O4y | 0.043 (0.022–0.095) |
| UOUM | 0.040 |
| fDz | 0.051 (0.020–0.092) |
| ours | 0.026 |

- **Densest frames:**
  - plasma field (UOUM 1:32): 399 shapes;
  - neon city (fDz 0:15:30): 358;
  - mission control (UOUM 1:56): 335, with 2987 micro-details;
  - infographic board (O4y 3:16): 334;
  - lab (O4y 0:24): 210.
- **Sparsest frames:** character close-ups at 36–45 shapes (O4y 1:04, O4y 2:28, fDz 0:50:40) and full-screen text cards.
  - TIS alternates **sparse close-ups** (one face and a flat set) with **dense establishing frames**.
- **Micro-detail vocabulary:**
  - Stars: 100–200 dots of 2–6 px plus 4–10 four-point sparkles in three sizes (UOUM 0:48, UOUM 11:56).
  - Coloured dust dots, teal and pink, in space (UOUM 0:48).
  - About 60 diagonal red ember dashes over the nuclear sky (fDz 2:00:20).
  - Floating hazard icons, about 9 per frame (O4y 0:18).
  - Rivets, vents and UI glyphs on machines (O4y 1:36–1:52, UOUM 1:56).
- **Meaningful objects per frame:** about 5–20 by eye, and up to about 40 in stock city frames.

---

## 8. Character design rules (study only; never reuse their characters)

**Proportions:** about 5.9 heads tall (O4y 0:18: head ≈ 90 px of a 535 px figure). Close-ups crop at chest height (O4y 0:00, fDz 0:50:40).

**Head:**
- An egg or rounded box, with half-circle ears in the skin shadow tone.
- Eyes are small solid dark ovals (≈ 25 × 35 px at close-up, by eye), with no whites in the current rig.
- Brows are thick dark strokes with rounded caps; they carry most of the expression (O4y 2:42).
- The nose is usually absent; the older rig uses a lighter blob (fDz 0:50:40).
- The mouth is a dark shape with a white teeth band and a pink tongue (O4y 0:00, UOUM 2:06).
- Optional details: two diagonal blush strokes (UOUM 2:06) and a beard drawn as one dark shape.

**Hair:** one flat dark shape with a lobed silhouette, with no highlight (`#36231c`, O4y 0:00).

**Body:**
- A trapezoid torso. Clothing detail comes from darker flat shapes (pockets, collar, lapels) plus button dots.
- Tube arms with circle or mitten hands; boots are simple blocks.

**Shading:** a 2-tone split on skin (§3); clothing has one shadow tone; there are no outlines.

**A recurring cast:** the same lab-tech rig carries O4y; a bearded scientist and a younger scientist appear across UOUM; generic military and press characters appear across fDz. Consistency comes from reusing one rig library, with costume and colour swaps per scene.

**Acting:**
- Head tilts and turns, brow changes, mouth flaps and body leans (fDz 0:50:40–0:50:42).
- Full-body falls with squash (O4y 2:06–2:11), gestures with props such as a tablet or clipboard (UOUM 2:06), and walk cycles (O4y 0:18).
- Animation runs on every frame: duplicate frames are 0 % in four of the six 60 fps stretches, 3 % in helio and 7 % in the fall.

**Caricatures of real politicians** appear in fDz (0:01:30, 0:03:20). Our rules exclude this.

---

## 9. Motion craft

**Always-on motion** (`cuts.py`, per-frame scene score):

| | O4y | UOUM | fDz (30 fps) | ours |
|---|---|---|---|---|
| frames with any change (score > 0.001) | 67 % | 66 % | 48 % | 37 % |
| fully static frames (score ≤ 0.0005) | 17 % | 20 % | 38 % | 50 % |
| new composition every (gridchange) | 3.2 s | 2.8 s | 3.1 s | **10.6 s** |
| visible change every | 2.3 s | 2.0 s | 2.1 s | 2.2 s |
| longest hold of an unchanged picture | 14 s | 6 s | 18 s | 2 s |
| scene-change events per minute | 5.4 | 4.5 | 6.8 | 9.6 |
| hard cuts | 8 in 18 min | **0** in 33 min | 220 in 3 h 11 min | 3 in 75 s |
| shot length median (p10–p90) | 9.4 s (3.5–19.5) | 10.3 s (2.1–26.9) | 6.2 s (1.0–18.9) | 4.3 s (3.1–11.9) |

The scene-change events are mostly animated transitions, not cuts. "Sustained fast motion" runs (spinning vortices, particle storms) are filtered out: 2 in O4y and 10 in UOUM.

**Reading the table:**
- Ours already changes something every 2.2 s, but it is the same composition evolving: 73 % of our 2 s pairs are "evolved", and only 19 % are "new".
- TIS delivers a **new picture** 62–72 % of the time, mostly through camera moves inside a large set and through overlays.
- The ambient motion that keeps TIS frames "alive" includes:
  - camera drift (§9 Camera);
  - character idle acting;
  - floating icons (O4y 0:18);
  - boiling clouds and embers (fDz 2:00:20: 8.7 % of pixels changing per frame beyond the camera move);
  - monitors flickering (fDz 0:00:24);
  - twinkling stars.

**Camera moves** (`motion.py` + `easefit.py`, from full-frame-rate stretches; pan in 1080p px):

| stretch | move | total | 50 % / 90 % of travel at | best fit (RMSE) |
|---|---|---|---|---|
| UOUM 2:04 (scientist) | arrival pan after a slide transition | 2127 px in 2.6 s, peak 1640 px/s | 0.75 s / 1.57 s | **out-quad** 0.039 |
| UOUM 0:08 (launch) | pull-back landing | −16.7 % in 1.8 s | 0.30 s / 0.87 s | **out-quart** 0.018 |
| O4y 2:06 (fall) | push-in on the character | +50 % in 2.1 s | 0.52 s / 1.40 s | **out-quad** 0.048 |
| UOUM 0:47 (helio) | pan | 128 px in 1.3 s | 0.47 s / 1.12 s | out-sine 0.070 |
| UOUM 0:48.4 (helio) | pull-out | −26 % in 1.0 s | 0.45 s / 0.77 s | **in-out sine** 0.056 |
| O4y 0:17.3 (reaper) | pull-back over the graveyard | −38 % in 3.6 s (≈ −10 %/s) | 1.20 s / 2.80 s | out-sine 0.021 |
| fDz 2:00:20 (mushroom) | slow pull-back on the hold | −34 % in 4.0 s (−8.5 %/s, constant) | 1.97 s / 3.53 s | **linear** 0.014 |
| fDz 0:00:21.5 (sitroom) | push-in with rotation | +32 % in 3.5 s, about +6.6° roll (summed per-frame estimate) | 2.10 s / 2.97 s | in-out sine 0.109 |
| O4y 1:24 (infobuild) | static board | < 0.2 %/s | — | locked |

- After a move "lands", the camera **keeps creeping**: +1 to +3 %/s zoom on the scientist (UOUM 2:06.5–2:09) and about ±1 %/s on the launch pad. It is only fully locked on infographic boards.
- **Camera shake** follows impacts. In the fall (O4y 2:08.25–2:09.0) the pan speed spikes to 420–995 px/s for 0.75 s with ±1° roll flips, then settles.
- These moves are much bigger and faster than Kurzgesagt's (+0.76 %/s pushes). TIS uses the camera as its main source of energy.

**Transition vocabulary** (each with a reference):

| transition | ref |
|---|---|
| Whip pan with horizontal motion blur, 0.25–0.35 s; scene scores spread over about 18 frames | O4y 0:17.0–0:17.3, `O4yWBv2Nj68_dense_reaper_00.jpg` |
| Ring/iris zoom-through: a white ring expands out of a clock face into the next scene | fDz 0:00:20.5–0:00:21, `fDzCHPWkou4_dense_sitroom_00.jpg` |
| Slide-in of the next scene with a fast decelerating pan (out-quad), then a speech bubble pops | UOUM 2:04–2:06, `UOUM1QT5GgU_dense_scientist_00.jpg` |
| Zoom-blur push out of a prop (a folder photo becomes the full frame) | UOUM 11:42–11:44 |
| Slice/strip wipe: horizontal maroon bars carry a stat ("80 % OF SURFACES") across a scene | UOUM 21:30–21:32, still `UOUM_2132.jpg` |
| Split screen with archival film sliding in from the right | UOUM 0:10–0:13, `UOUM1QT5GgU_dense_launch_00.jpg` |
| Hard cut on an impact (mushroom cloud to top-down debris) | fDz 2:00:24.07 |
| White flash bloom | fDz 0:50:43 |
| Countdown cards: big chrome "#50 … #1" on grey, one per list item (every ≈ 40 s) | UOUM 0:20, 1:06, 1:52 |

**Element entrances:**
- **Info cards** grow upward from the bottom edge in about 0.5 s, header band first; content pops in afterward with a staggered scale-in of atoms and particles (O4y 1:26–1:29, `O4yWBv2Nj68_dense_infobuild_00.jpg`).
- **Kinetic labels** build letter by letter, each letter dropping and scaling in, about 70 ms apart ("HELIOSPHERE" at UOUM 0:48.25–0:49.25, `UOUM1QT5GgU_dense_helio_00.jpg`).
- **Speech bubbles** pop with rotation overshoot: the text starts at about −15° and settles to −3° within about 0.5 s (UOUM 2:05.6–2:06.2).
- **Date and time cards** slide in from the left edge, and their text wipes in (fDz 0:00:20.8, UOUM 0:09.3 "VOYAGER II").

**Secondary motion:** water spray and droplets (O4y 2:38–2:46), smoke puffs (O4y 2:00–2:04, fDz 2:00:24), recoil and camera shake after hits, cloud boil, and drifting embers.

---

## 10. Typography and on-screen text

| element | ref | font (by eye) | size at 1080p | colour | placement | effects |
|---|---|---|---|---|---|---|
| Title cards | O4y 0:38 | heavy geometric sans, all caps (Montserrat ExtraBold/Black class) | cap height ≈ 70 px (6.5 % of frame height), line pitch 132 px, up to 1500 px wide | `#ede9ea` | centred, 2 lines | almost invisible drop shadow (3–4 px, ΔL* −4) over a blurred, dark key-colour motif pattern |
| Date/time cards | O4y 0:24, UOUM 0:08, UOUM 11:56 | label "DATE:" in a light weight (cap ≈ 38 px); value in a bold rounded geometric sans, mixed case (cap ≈ 60–65 px) | — | white card `#fdfbfc`; icons in flat orange `#f59806` (calendar) or pure blue `#0203fd` (clock) | flush to the left edge at y ≈ 108–268, a second card below at y ≈ 330–490 | soft drop shadow |
| Speech bubbles | UOUM 2:06, UOUM 11:04 | rounded geometric sans, sentence case | x-height ≈ 55 px | black on white | 2 lines | rounded rect r ≈ 24 px with a pointed tail toward the mouth |
| Labels | UOUM 0:48, UOUM 20:30 | white caps | — | white, or a dark caps chip | — | arrow pointers; chips like "ANTICYCLONIC STORM" |
| Info cards | O4y 0:52 | heavy caps | — | navy-black text on cream; white caps on a saturated header band | — | — |
| Counters, readouts | O4y 7:44–7:52 | — | — | — | inside the scene: vitals monitors with "5:45 PM", thermometer gauges (O4y 9:12–9:18) | — |
| Logo bug | all frames | — | ≈ 105 × 105 px icon + "THE INFOGRAPHICS SHOW" | white text | bottom-left, about (25, 950)–(430, 1055) | permanent |

- **No burned-in captions** anywhere in the three videos.
- **An "authenticity" badge** at UOUM 0:00–0:04 reads "NO AI USED IN THE VIDEO – 100% HUMAN CREATED". The channel advertises hand-made animation, so our code-authored art must not look generated.

---

## 11. Sound design

Measured with `audio.sh` / `audio.py` (output: `data/tis/*_audio.txt`; spectrograms in `refs/infographics/sheets/spec_*.png`).

| | O4y | UOUM | fDz (first 30 min) |
|---|---|---|---|
| integrated loudness | −20.2 LUFS (DRC stream) | −15.3 LUFS | −12.7 LUFS |
| loudness range | 2.4 LU | 2.1 LU | 2.6 LU |
| narration speed (manual subtitles) | 179 wpm | 183 wpm | — (auto-subs only) |
| full-band level, voice vs pauses | −24.9 vs −41.7 dBFS | −19.1 vs −31.4 dBFS (bed 12 dB under the voice) | — |
| < 150 Hz in pauses | −44.5 dBFS | −33.6 dBFS | — |
| 0.1 s windows below −45 dBFS | 0.1 % | 0.1 % | — |
| voice pauses ≥ 0.3 s | — | 14 per min, median 0.5 s | — |

- **Mastering:** narration is compressed hard (LRA ≈ 2–2.6 LU) and mastered loud in the original stream (−12.7 LUFS for fDz). O4y's −20.2 LUFS comes from the DRC variant YouTube served, so do not use it as a target.
- **Music bed:**
  - It runs the whole time. In O4y the full band sits around −44 dBFS in pauses, about 17–19 dB under the voice.
  - Spectrograms show steady energy under 100 Hz and sustained tonal lines around 300 and 600 Hz (pads) running under the speech (`spec_O4y_12-24.png`).
  - **The mix is never silent:** 0.1 % of windows fall below −45 dBFS.
- **Pacing:** UOUM has 14 pauses ≥ 0.3 s per minute (median 0.5 s), so a short breath lands about every 4 s.
- **SFX on transitions: not detected.**
  - The test compared the rise in > 5 kHz, < 150 Hz and full-band energy in ±0.3 s around each detected transition with 600 random times.
  - The rises at transitions were no larger than at random times. Examples: > 5 kHz median rise 20.2 vs 21.1 dB (O4y), < 150 Hz 7.5 vs 7.5 dB.
  - The spectrogram around the O4y 0:17 whip shows no broadband whoosh.
  - **Inference:** TIS relies on voice plus a music bed. SFX, if present, are quiet or sparse and are not tied to cuts. **This needs a listening check before it is turned into a rule.**

---

## 12. What this means for our code (input for STYLE_BIBLE.md / JUDGE_RUBRIC.md)

TIS shows how far **craft organisation** goes with simple drawing:
- a rig library;
- one large set per scene with a moving camera;
- colour keys per scene;
- UI cards and overlays;
- a new picture every 3 s.

Kurzgesagt adds the **illustration craft** that TIS lacks: hue-shifted multi-tone shading, rims, diegetic light, micro-texture and saturation discipline. For our code, take TIS's structure and Kurzgesagt's rendering.

**Measurable targets this study supports** (judge checks, scored per 2 s grid of our renders):
1. **New composition every ≤ 3.5 s**, with `gridchange.py` "seconds per NEW picture" ≤ 3.5; TIS is 2.8–3.2 and we are 10.6. Use camera moves inside a large set, cutaways and overlays, not just hard cuts. Hard cuts can stay under 1 per minute.
2. **Hue families per frame ≥ 3 (median)**, against our 1. Each scene gets its own key colour; consecutive scenes should change key.
3. **Dark-pixel share (V < 0.2) ≤ 10 %** outside space scenes, against our 19 %. **Median value ≥ 0.5** outside space and night scenes.
4. **Detail:** median ≥ 140 shapes and ≥ 800 micro-details per frame (`density.py`), and edge density ≥ 0.04.
5. **Characters:** a reusable rig library with 2-tone split shading (skin shadow ΔL* 4–8 with a hue shift of −5 to −10°). Animate on every frame, with brows and mouth always in play. Tint rigs toward the scene key at night.
6. **Depth:** 3–5 planes per environment shot. Far planes get L* +15 to +20 and S −0.3. Use a near-black key-hue foreground silhouette plane, and one Gaussian-blurred plane (σ 15–25 px) on close-ups.
7. **Camera:** after every transition, an out-quad or out-quart landing that reaches 90 % in 0.9–1.6 s. Then drift at 1–3 %/s, or run a linear 8–10 %/s pull or push on held establishing shots. Add shake (≈ 400–1000 px/s for ≤ 0.75 s) only on impacts. Lock the camera on info boards.
8. **Transitions** (have at least these, in code): whip pan with directional blur 0.25–0.35 s, ring/iris zoom-through, slide-in plus out-quad landing, zoom-blur push into a prop, strip wipe, white flash bloom.
9. **UI kit:**
   - date and time cards flush left with soft shadows;
   - speech bubbles (r ≈ 24 px) that pop with rotation overshoot;
   - info cards that grow from the bottom with coloured header bands;
   - per-letter kinetic labels (≈ 70 ms stagger);
   - full-screen heavy-caps title cards over a blurred key-colour motif pattern.
10. **Glow recipe for emitters:** a flat disc plus exponential halo (half-intensity ≈ 55–60 px past the edge on a 170 px disc) tinted toward the background hue. Add starbursts with 4–6 thin rays. Never bloom non-emitters.
11. **Audio:** narration 175–185 wpm, LRA ≤ 3 LU, about −14 LUFS master. A continuous music bed 12–20 dB under the voice, never silent.

**Where we should exceed TIS and copy Kurzgesagt instead:** shading depth (multi-tone hue-shift shading plus rims), saturation discipline (chromatic S ≈ 0.75 rather than TIS's 0.55), restrained white, and texture.

**Reproduce:**
- Spark: `bash tools/tis/extract.sh <video> <out>`, `bash tools/tis/scores.sh <video> <out>/scores.txt`, `bash tools/tis/dense.sh <video> <out> <label> <start_s>`.
- Then run the Python tools with `~/studio/venvs/r2/bin/python -I` (numpy, opencv, PIL).
