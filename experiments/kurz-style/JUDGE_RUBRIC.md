# Judge rubric: "Kurzgesagt-tier" (/100)

This rubric scores one rendered video, or one shot, against **reference frames placed side by side**. The question it answers: *does our frame belong to the same quality tier as the Kurzgesagt frame next to it, while still looking like our own house style?*

- The style to judge against is `STYLE_BIBLE.md` ("Lantern & Ink"). IDs such as P1, D3, M2 and J4 are its §13 checks.
- Use this rubric together with `FEEDBACK.md`, whose ship gate still applies: every rule ≥ 7/10, hook ≥ 8/10.
- Reference images are local only (`refs/`, ignored by git). The source videos are on the Spark under `~/studio/refs/kurz-bio/`, `~/studio/refs/kurz-space/` and `~/studio/refs/kurz-style/infographics/`.

**Tiers:**

| score | tier |
|---|---|
| ≥ 85 | **Kurzgesagt tier** |
| 70–84 | near tier |
| 55–69 | TIS tier |
| < 55 | below TIS (our orca pilot is about 25, see §7) |

---

## 1. Protocol

### 1.1 Automatic metrics (Spark, about 5–15 min per video)

```bash
rsync -a --exclude refs --exclude data ~/Documents/faceless-studio/experiments/kurz-style/ dgx-spark:~/studio/app/experiments/kurz-style/
ssh dgx-spark 'cd ~/studio/app/experiments/kurz-style && \
  bash tools/house/judge_metrics.sh <ours.mp4> ~/studio/refs/kurz-style/judge/<name> <name>'
```

- The run prints P1–P8, D1–D5, M1–M5 and A1–A3 with PASS/FAIL, and writes `JUDGE_METRICS.json` plus a 2 s frame grid (`grid/g_NNNNN.jpg`, where frame N is at t = 2·(N−1) s).
- Copy `JUDGE_METRICS.json` back into `data/house/judge_<name>.json`.
- **CPU budget:** the script is CPU only and niced; run one at a time while other renders run.

### 1.2 Sample eight frames by role

Take each frame from the render at full resolution (`ffmpeg -ss <t> -i ours.mp4 -frames:v 1 f_<role>.png`). If a role does not exist in the video, take the closest frame and note it.

| role | which frame |
|---|---|
| **C** cover | frame 0, the Shorts cover (FEEDBACK B3: the subject is on screen, never black) |
| **H** hook | the subject at about 1.5–3 s |
| **P** proof / scale | the first number or scale comparison, usually 5–8 s (FEEDBACK B4) |
| **E** environment wide | the widest set shot |
| **X** hero close-up | the largest view of the hero creature or object |
| **K** dark / emissive / light event | a deep, night or space beat, or a light switching on |
| **T** text / data | a frame with labels, a gauge or a big number |
| **B** bookend / ending | the payoff or final frame |

### 1.3 Pair each frame with references

For each role, pick one Kurzgesagt frame (the target) and optionally one TIS frame (the bar below the target). Choose them by scene type, not by subject. Paths are relative to `refs/`.

| role / scene type | Kurzgesagt reference (pick the closest) | TIS bar |
|---|---|---|
| C, H: creature intro | `kurz-bio/stills/W_0000_tumor-creature.jpg`, `kurz-bio/stills/D_0000_cruise-ship.jpg` | `infographics/stills/O4y_0000.jpg` |
| P: scale / proof | `kurz-bio/stills/W_0222_whale.jpg`, `kurz-bio/stills/W_0230_animal-panels.jpg`, `kurz-space/L_0m30s_jupiter-cube-isogrid.jpg` | `infographics/stills/UOUM_0048.jpg` |
| E: environment, water | `kurz-bio/stills/D_0126_reef.jpg`, `kurz-bio/stills/D_0056_shallows-sub.jpg`, `kurz-bio/stills/D_0250_fish-school.jpg` | `infographics/stills/O4y_0018.jpg` |
| E: environment, land or sky | `kurz-bio/stills/W_0410_elephant-savanna.jpg`, `kurz-space/I_7m06s_lake-landscape-pan.jpg` | `infographics/stills/UOUM_0008.jpg`, `infographics/stills/fDz_20550.jpg` |
| X: hero close-up | `kurz-bio/stills/D_0630_dumbo-octopus.jpg`, `kurz-bio/stills/W_0318_cancer-cell.jpg`, `kurz-space/L_6m54s_blue-hypergiant-nebula.jpg` | `infographics/stills/O4y_0242.jpg` |
| K: dark / emissive | `kurz-bio/stills/D_0528_anglerfish.jpg`, `kurz-bio/stills/D_0304_biolum-jellies.jpg`, `kurz-bio/stills/D_0410_searchlight.jpg`, `kurz-bio/stills/D_0706_searchlight-circle.jpg` | `infographics/stills/UOUM_1156.jpg` |
| K: space | `kurz-space/L_3m14s_sun-dark-bg.jpg`, `kurz-space/L_4m06s_bluestar-teal-starfield.jpg`, `kurz-space/L_8m04s_red-nebula.jpg` | `infographics/stills/UOUM_0022.jpg` |
| T: text / data | `kurz-bio/stills/W_0222_whale.jpg` (tags), `kurz-bio/stills/D_0434_depth-chart.jpg` (gauge), `kurz-space/L_2m26s_reddwarf-cutaway-labels.jpg` | `infographics/stills/O4y_0052.jpg` |
| B: bookend | `kurz-bio/stills/D_0012_biome-triptych.jpg`, `kurz-bio/stills/W_0610_seal.jpg` | `infographics/stills/fDz_20020.jpg` |
| macro / body | `kurz-bio/stills/W_0126_cell-yellow.jpg`, `kurz-bio/stills/W_0036_cell-cutaway.jpg` | `infographics/stills/O4y_0830.jpg` |

### 1.4 Build the side-by-side sheet and look at it

```bash
python3 -I tools/house/sbs_sheet.py out/sbs_<name>.jpg \
  "C cover - ours 0:00|f_C.png|refs/kurz-bio/stills/W_0000_tumor-creature.jpg|refs/infographics/stills/O4y_0000.jpg" \
  "E environment - ours 0:21|f_E.png|refs/kurz-bio/stills/D_0126_reef.jpg|refs/infographics/stills/O4y_0018.jpg" \
  ...
```

- Each row shows ours on the left (red frame), then the Kurzgesagt reference, then TIS. Labels must not contain `|`.
- Open the sheet at full size: Read the JPG. Then also Read a **2× crop of our hero next to a 2× crop of the reference hero**, because shading craft only shows up close.
- Never score from descriptions or from memory (FEEDBACK A5).

### 1.5 Motion evidence (two 5 s pairs)

```bash
ssh dgx-spark 'cd ~/studio/app/experiments/kurz-style && \
  bash tools/house/motion_pair.sh <ours.mp4> <t_ours> ~/studio/refs/kurz-bio/PaErPyEnDvk.mp4 84 ~/studio/refs/kurz-style/judge/<name>_pairA'
```

The tool writes a side-by-side MP4 and a 0.25 s strip JPG: two rows of ours, then two rows of the reference. Read the strip. Watch the MP4 if you can play video.

Reference clips (video, start s):

| reference | video, start (s) | what it shows |
|---|---|---|
| reef, depth layers, ambient life | D `PaErPyEnDvk`, 84 | |
| anglerfish, dark + emitter | D, 326 | |
| hero creature, ambient motion | W `1AElONvi9WQ`, 0 | |
| split-panel push | W, 140 | |
| iris and morph | W, 196 | |
| TIS whip + pull-back | `O4yWBv2Nj68`, 16 | |
| TIS character fall + shake | `O4yWBv2Nj68`, 126 | |

The TIS video is at `~/studio/refs/kurz-style/infographics/`.

Pair A: our widest moving set against the reef. Pair B: our hero action or light event against the anglerfish, or the creature clip.

### 1.6 Score, list defects, decide

1. Score every category in §2: pick a level from its anchors, then apply the caps in §3.
2. For each pair, record a **tier gap** with a timestamp, and list each defect with its timestamp and the STYLE_BIBLE section it breaks:
   - 0 = same tier;
   - 1 = slightly below;
   - 2 = clearly below, TIS-like;
   - 3 = far below, our pilot level.
3. Run the identity gate (§4).
4. Write the result in the §6 format.

---

## 2. Categories (100 points)

Each category has five levels. Pick the level whose description fits **all** sampled frames. When frames disagree, use the median frame, then drop one level if any frame is two levels lower.

The point values per level are:

| level | share | meaning |
|---|---|---|
| L0 | 0–15 % | our orca pilot |
| L1 | about 35 % | TIS level |
| L2 | about 60 % | above TIS, clearly short of the reference |
| L3 | about 85 % | same tier: side by side, the reference does not look more crafted on this aspect |
| L4 | 100 % | at least equal to the reference on every pair, with something it lacks |

### 2.1 Illustration and shading craft (20)

Checks: J2, J3, J4 (hero marks), §4 of the bible.

| level | points | description |
|---|---|---|
| L0 | 0–3 | flat silhouettes or a single tone; no shadow shape, highlight or rim |
| L1 | 7 | 2 flat tones with a hard split; no highlight or rim; few marks (TIS §3) |
| L2 | 12 | heroes have shadow + highlight, but rim, specular, bounce or stipple are missing or inconsistent; shading colours not mixed toward the ambient (greyish or blackish shadows); < 12 hero marks |
| L3 | 17 | every hero has the full stack (core shadow, stipple terminator, highlight, glint where glossy, rim, contact shadow, ≥ 12 marks); supporting objects have at least 4 layers; hue-shifted shadows; the 2× crop holds up next to the reference crop |
| L4 | 20 | as L3, plus the light moves and the shading follows it; construction and marks are as rich as KB W 3:18 or KS L 6:54 at 2× |

### 2.2 Lighting and atmosphere (12)

Checks: J3, J7, §5.

| level | points | description |
|---|---|---|
| L0 | 0–2 | no key direction; flat fill light; glow missing or smeared over everything |
| L1 | 4 | glows on emitters only, no consistent key; scene relit by tint (TIS §4) |
| L2 | 7 | consistent key on the hero, but supporting objects disagree; rays or caustics static; no lit/unlit separation in dark scenes |
| L3 | 10 | one key + rim + ambient in every frame, all objects agree; emitters have tight halos (half at ≤ 0.1 R); dark scenes use the lit/unlit pass; rays and caustics animate |
| L4 | 12 | as L3, plus at least one light event per 30 s (switch-on reveal, sweep, pulse re-tint) as strong as KB D 4:46 |

### 2.3 Depth and composition (12)

Checks: J1, J5, J6, J8, §6.

| level | points | description |
|---|---|---|
| L0 | 0–2 | 1–2 planes; subjects float on a gradient; no foreground (ours today) |
| L1 | 4 | 3–5 value-stepped planes, some blur, but no plane-gap shadows and weak foreground (TIS §5) |
| L2 | 7 | ≥ 4 planes in most environment frames, haze steps visible, foreground in under 60 % of them, little parallax |
| L3 | 10 | ≥ 4 planes in every environment frame, haze steps + plane-gap shadows + a cropped soft foreground in ≥ 60 %; parallax visible in every move; hero 25–55 % of frame |
| L4 | 12 | as L3, with compositions that read instantly at phone size and depth as convincing as KB D 1:26 |

### 2.4 Colour and palette discipline (10)

Checks: P1–P8, colour script (§2.5 of the bible).

| level | points | description |
|---|---|---|
| L0 | 0–2 | one hue family; dark and monochrome; greys or black present (orca: 1 family) |
| L1 | 3 | 3 families but desaturated and grey-heavy; lots of white (TIS: P3 0.57, P4 0.08) |
| L2 | 6 | P1–P8 pass on most frames; the key does not change between scenes; the complementary subject is weak |
| L3 | 8 | P1–P8 pass; every scene has a key ramp, a complementary subject and ≤ 2 accents; the colour script moves with the story |
| L4 | 10 | as L3, with a colour script that carries meaning (depth, danger, time) as clearly as KB D's descent |

### 2.5 Detail density and hierarchy (10)

Checks: D1–D4, J4, §8.

| level | points | description |
|---|---|---|
| L0 | 0–2 | no micro layer; specks < 100, edge density < 0.035, outlines doing the separating (orca: 63 specks, 0.026 edges, outline 0.29) |
| L1 | 4 | busy like TIS (≈ 140 shapes / 840 micro), but from stock-like set clutter; the hero itself is plain |
| L2 | 6 | D1–D5 pass; the micro layer is present but uniform; the hero has < 12 marks or the background is busier than the hero |
| L3 | 8 | D1–D5 pass; environment frames have ≥ 15 named objects and ≥ 150 specks; detail concentrated on the hero and at the frame edges; calm field |
| L4 | 10 | as L3 at the richness of KB D 1:26 / KS L 6:54 (hundreds of hand-placed-looking marks), with no clutter |

### 2.6 Motion craft (14)

Checks: M1, M2, §9.2, §9.3, §9.7. Evidence: the 0.25 s strips and the MP4.

| level | points | description |
|---|---|---|
| L0 | 0–2 | linear or stepped moves, frozen holds, no secondary motion |
| L1 | 5 | eased camera and characters, but limited ambient life; static frames common (TIS: 17–38 % static) |
| L2 | 8 | M1 ≥ 95 %; eased arrivals; some secondary motion; blinks or sways mechanical (in sync, single sine) |
| L3 | 12 | M1/M2 pass; every arrival uses the `travel` + `settle`/`pop` tokens; every appendage has follow-through with phase offsets; ambient layer per §9.3; morphs instead of cuts |
| L4 | 14 | as L3, with acting (anticipation, weight, reaction) that matches the reference clip side by side |

### 2.7 Camera, transitions and cadence (8)

Checks: M3, M4, M5, §9.4, §9.6.

| level | points | description |
|---|---|---|
| L0 | 0–1 | new composition every > 8 s or many hard cuts (orca: 10.6 s, 8 cuts/min) |
| L1 | 3 | TIS-like big eased moves, new composition ≤ 3.5 s, but camera locks between moves |
| L2 | 5 | M3–M5 pass, but transitions are one or two kinds, or parallax is not visible |
| L3 | 7 | M3–M5 pass; drift between every move; ≥ 3 transition kinds from the library; parallax in every move |
| L4 | 8 | as L3, with transitions that are motivated by the content (a bubble wipe in water, a light reveal in the dark) |

### 2.8 Typography and information design (6)

Checks: J9, J10, §11, FEEDBACK B6, B8.

| level | points | description |
|---|---|---|
| L0 | 0–1 | plain boxes or default text; collisions; unreadable at phone size |
| L1 | 2 | designed cards, but generic; labels linger |
| L2 | 4 | house fonts and sizes; lantern tags and leaders, but no progress device, or YOU missing on scale beats |
| L3 | 5 | everything in §11: lantern tags with ring leaders, Anton numbers with units, depth/scale gauge, YOU on scale beats, ≤ 2 labels + captions, safe area |
| L4 | 6 | as L3, with text animation (mask wipes, counters ticking) as clean as KB W 2:22 |

### 2.9 Sound design (8)

Checks: A1–A3, §12. Listen to the motion pairs if possible; otherwise use the metrics plus an SFX event list from the storyboard.

| level | points | description |
|---|---|---|
| L0 | 0–1 | voice only, or a bed with gaps; robotic voice (FEEDBACK A1) |
| L1 | 3 | voice + continuous bed, loudness on target, few or no SFX (TIS §11) |
| L2 | 5 | A1–A3 pass; SFX on some events, but late or generic |
| L3 | 7 | A1–A3 pass; ≥ 70 % of entrances, transitions and light events have an SFX within ±2 frames; sonar ping and foley vocabulary; bed ducked 12–18 dB under the voice |
| L4 | 8 | as L3, with sound that adds meaning (pressure thrum deepening with depth, ping pitched to the scale) |

---

## 3. Caps from automatic checks

Apply these after picking the level. A cap is the maximum points the category can get.

| condition | cap |
|---|---|
| J2 fails on any hero (missing shadow, highlight or rim) | 2.1 ≤ 12 |
| J3 fails (shadow sides disagree) in any frame | 2.1 ≤ 12, 2.2 ≤ 7 |
| J1 fails in more than 1 environment frame | 2.3 ≤ 7 |
| P5 < 3, or P3 outside 0.66–0.88, or P4 > 0.04 | 2.4 ≤ 6 |
| any of D2–D5 fails | 2.5 ≤ 6; two or more fail: ≤ 4 (D1 is a floor only) |
| M1 < 80 % | 2.6 ≤ 5; M1 80–95 %: ≤ 8 |
| M2 fails | 2.6 ≤ 8 |
| M3 > 3.5 s (Shorts) or > 5 s (long-form), or M4 outside 2.0–4.5 s | 2.7 ≤ 5 |
| M5 > 2 cuts/min | 2.7 − 2 points |
| any of A1, A2, A3 fails | 2.9 ≤ 5 |
| voice judged robotic (FEEDBACK A1 < 7) | 2.9 ≤ 3 |

---

## 4. Identity gate (pass/fail): ours, not a clone

The video **fails the rubric regardless of score** if any of these fails.

1. **P1 ≥ 0.85** (palette conformance) and **P2 ≤ 0.08** (violet/magenta band) on the median frame.
2. **No borrowed designs:** no birds, ducks or bean mascots; no faces on planets, stars or cells; no isometric grid floor with cube scale references; no porthole HUD; no Kurzgesagt or TIS logo, jingle or title lockups (STYLE_BIBLE §14).
3. **No wide-tracked thin-caps titles** and no hard offset-block tag shadows (Kurzgesagt type signatures). Titles use Anton on an ink plate; tags are lantern tags.
4. **House signatures present** in the sampled frames:
   - stipple terminator on at least one hero;
   - teal-ink darks;
   - plane-gap depth;
   - the ring motif (leaders, pad or spots);
   - the YOU figure on scale beats.

   At least 4 of these 5 must be visible.
5. **No traced or colour-picked reference frames.** Compositions must not overlay a reference frame. A quick check: place our frame and the reference at 50 % opacity; silhouettes must not coincide.

---

## 5. Verdict

**Kurzgesagt tier** requires all four of the following:
- total ≥ 85;
- every category ≥ 60 % of its points;
- identity gate passed;
- every pair's tier gap ≤ 1.

Otherwise the verdict is the tier from the score table at the top. The `FEEDBACK.md` ship gate is separate and still applies: a Kurzgesagt-tier video with a weak hook does not ship.

---

## 6. Output format

Write the judgement as Markdown followed by a JSON block, so a workflow can parse it:

```json
{
  "video": "out/.../name.mp4",
  "judge_date": "YYYY-MM-DD",
  "metrics_file": "data/house/judge_<name>.json",
  "sheet": "out/.../sbs_<name>.jpg",
  "motion_strips": ["...pairA_strip.jpg", "...pairB_strip.jpg"],
  "scores": {"illustration": 0, "lighting": 0, "depth": 0, "colour": 0, "detail": 0,
             "motion": 0, "camera": 0, "type": 0, "sound": 0},
  "caps_applied": ["2.5 <= 6 (D3 fails: 63 specks)"],
  "total": 0,
  "pairs": [{"role": "E", "ours_t": "0:21", "ref": "kurz-bio/stills/D_0126_reef.jpg", "tier_gap": 0,
             "defects": [{"t": "0:21", "bible": "§6", "note": "only 2 planes; no foreground"}]}],
  "identity_gate": {"P1": 0.0, "P2": 0.0, "no_borrowed_designs": true, "type_signatures_absent": true,
                    "house_signatures_seen": 0, "no_tracing": true, "pass": false},
  "tier": "below TIS | TIS | near | Kurzgesagt",
  "top_fixes": ["the 3 changes that would gain the most points, each tied to a bible section"]
}
```

---

## 7. Calibration

These are expected scores from frames already seen; they are not a formal judging run. A judge who scores the references far from these should re-read the anchors.

| sample | expected | why |
|---|---|---|
| our orca pilot (`out/pilots/explainer-orca/explainer-orca_16x9.mp4`) | **≈ 25** | illustration 2, lighting 3, depth 2, colour 3, detail 2, motion 5, camera 1, type 3, sound 4. Flat black-and-white orcas on one teal gradient, 1 hue family, 1–2 planes, 63 specks, a new composition every 10.6 s; loudness on target. |
| a TIS video (O4y, UOUM) | **≈ 50–60** | strong cadence, camera and cast; 2-tone shading, desaturated, grey-heavy; identity gate not applicable |
| a Kurzgesagt frame scored against another Kurzgesagt frame | **≈ 92–97** | the rubric's L3/L4 anchors are written from these frames; it fails our identity gate by design (P1 0.07–0.34, P2 0.20–0.58) |

Calibration commands and outputs:
- `data/house/judge_orca.json`: our pilot through `judge_metrics.sh`.
- `data/house/judge_kurzW.json`, `data/house/judge_kurzD.json`: Kurzgesagt W and D through the same script.
- `data/house/palette_refs.txt`: `palette_check.py` on all 120 reference stills.
