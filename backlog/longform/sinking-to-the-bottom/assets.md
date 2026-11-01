# Assets: sinking-to-the-bottom

Every unique asset the shot list uses, with where it lives today. Checked on 2026-11-01 ~12:55 UTC, revised 13:15 UTC for revision 2 (90 shots / 124 windows) against `studio/src/kits/explainer/index.tsx` (registered components), `README.md` (props), `studio/public/sfx/`, `studio/public/music/` and the backlog parent's `backlog/explainer/explainer-sinking-every-1000m/gen_storyboard.py` (which already holds most one-off SVG strings).

Status key:
- **KIT**: exists in `studio/src/kits/explainer/` and is registered. Use as is.
- **KIT + PROP**: exists, needs one new prop.
- **PARENT SVG**: a static SVG string already drawn in the parent's `gen_storyboard.py`. Copy it into this episode's generator; no kit change.
- **CORE**: built from core layer types (`rect`, `circle`, `text`, `particles`, `svg`) in `studio/src/core/layers.tsx`. No new file.
- **NEW**: does not exist anywhere yet. Must be built before the render (by a kit lane; this writing lane does not edit kits).

Shots column = how many of the 90 shots use it, counted from the layers + components columns of `shotlist.md` revision 2. (Revision 1 said Ocean was the background in all 88 shots; the parent overrides it to black/dark in 38, so it is 54 of 90 here.)

## 1. Kit components

| Asset | Status | Shots | Used for | Notes / props needed |
|---|---|---|---|---|
| `explainer/Ocean` | KIT | 54 (background; the other 36 are `bg black` / `bg dark`) | depth-lit water, rays, marine snow, surface | `depth` from the global track; `surface` 0.55 in s01 and s81 only; s82 runs depth 0->400 with the surface rising. s46 is NOT a surface shot (parent bg black) |
| **`explainer/DepthMeter`** | **KIT + 2 PROPS (render blocker)** | 56 (HUD) | HUD ruler right, zones | See §1b. The parent already passes `markers`; today's DepthMeter silently ignores it, so no flags render. Also needs `lock` for s72 |
| `explainer/You` | KIT | 61 | the viewer on the sled | poses stand / panic / point / shrug; `color` white -> pale blue (cold) -> orange after cheat 1; amber blush tint for "shrimpier" (s65 2/2) |
| `explainer/SpermWhale` | KIT | 3 | s14 pass, s23 scars, s67b option 2 icon | shared `pxPerM` with YOU |
| `explainer/ColossalSquid` | KIT (variant optional) | 3 | t1, s20, s22 | `hooks: false`; optional `variant: "giant"` |
| `explainer/Bus` | KIT | 1 | squid length ghost (s20). No longer used in s08 (rule 3 now compares to space) | |
| `explainer/Car` | KIT | 1 | fingertip motif 4/4 (s73) | |
| `explainer/Options` | KIT | 8 | THE RULES, COLOURS LEFT, STRATEGY, CAN YOU SAVE YOURSELF? (s67b, 3 strikes), FINAL READING board, KILLED YOU (s80, 3 strikes), held board | `strikes`, `hidden`, `select` exist |
| `explainer/Stat` | KIT | 14 | numbers only (adds 222 MIN in s67b and +31% in s73) | |
| `explainer/Tag` | KIT | 63 | labels, rulings, jokes on screen | |
| `explainer/Headline` | KIT | 20 | red/green cards (adds the 65% flip card, 0 CHEATS LEFT, NOBODY IS COMING, OURS) | |
| `explainer/SpeedBars` | KIT | 3 | breath vs trip (s36), TMAO (s62), PCB (s79) | bars only grow: limit row last |
| `explainer/ScaleBar` | KIT | 3 | squid ~12 M, dumbo **~35-43 CM**, amphipod **~4 CM (3-5)** | |
| `explainer/Map` | KIT | 1 | s53 | zoom <= 3 |
| `explainer/Timer` | KIT | 1 | s01 | `style: "ring"` |
| **`explainer/AliveMeter`** | **NEW (render blocker, no fallback)** | the parent's storyboard.json places it 53 times: the HUD on every descent shot + 16 big-meter verdict shots | YES / MOSTLY / ? / BARELY / NO, DEATH 1-3 stamps, needle | See §1b. The revision-1 "Headline + rect" fallback is withdrawn: it would mean ~50 hand placements and loses the needle that s26 (spin), s31, s74 (slide toward NO, stop at BARELY, YES) and the 65% flip state depend on |
| **`explainer/BeakedWhale`** | **NEW** | 4 | t2, s33 (silhouette + long shadow on "not alone"), s34, s67b option 3 | ~6 m, grey, short beak, scar lines, `silhouette` |
| **`explainer/DumboOctopus`** | **NEW** | 1 | s48 | ~35-43 cm total length, ear-fin flap idle |
| **`explainer/DeepFish`** (grenadier) | **NEW** | 2 shots / 3 windows | s42 (2 windows: dead bait fish, then grenadiers nose in), s44 (circling) | `dead`, `timeOffset` |
| **`explainer/Snailfish`** | **NEW** | 5 (+ thumbnail B) | t3, s60, s61, s63, s64 | `juvenile`, `xray`, `silhouette` |
| **`explainer/Amphipod`** | **NEW** | 5 | s65 cheat 3 (amber, xray inset), s68, s69, s78, s78b | `color`, `xray` gut window, leg ripple |

### 1b. Specs for the two render blockers

**AliveMeter** (`studio/src/kits/explainer/AliveMeter.tsx`, NEW). Props: `state` (string or step track [{t, v}], v in YES / MOSTLY / ? / BARELY / NO, colours green / lime / yellow / orange / red; needle eases between state angles over 0.45 s, ease out), `needle` (optional raw angle track, overrides `state` for s74's slide toward NO and stop), `stamp` [{at, text, color}] (scale 1.6 -> 1 slam in 0.15 s, 2 s hold, fade), `spin` [{at, duration}] (s26 "?"), `size`, `mode` ("alive" | "lives", the teal LIVES HERE? panel for the 65% flip, lines 40-42), `frame` ("normal" | "red", the END GAME state from s65b on). The HUD instance sits at left, size 1; verdict shots use size 1.3-1.6.

**DepthMeter additions** (`studio/src/kits/explainer/DepthMeter.tsx`, targeted edit by the kit lane). `markers` [{depth, label, color}]: each flag is drawn on the scrolling ruler itself, so it moves with the ruler's own transform (no per-frame keyframes in the storyboard); the ruler window is 1,400 m, so a flag is visible only while its depth is inside the window, and flags below the window show as a small arrow + label pinned to the bottom edge ("6,957 M below") so s49's "marker far below YOU" reads. Flags used: 701 (human record), 1,400 (2x record), 2,992 (beaked whale), 3,682 (average seafloor), 6,957 (deepest octopus), ~8,200 (fish limit, red), 8,849 (one Everest), 10,898 (the bag, hidden until 8:59, `revealAt`). `lock` {at, depth, color}: from `at` the readout freezes at `depth` (10,935) and the readout box gets a 6 px red frame with a 0.2 s pulse (s72 2/2). `waterTint` (optional colour track): the teal water line at the 65% flip.

## 2. One-off SVG and core layers

| Asset | Status | Shots | Used for |
|---|---|---|---|
| SLED | PARENT SVG `SLED` | 49 | every shot with parent `sled=True` |
| BOAT_CRANE | PARENT SVG `BOAT` | 3 | s01, s46 column top, s81 (empty crane) |
| TRENCH_WALL | PARENT SVG `WALL` (tall 700x2400, scrolls) | 23 (+ a second **flipX** copy in s51 2/2 for the far wall) | 3:54 to the floor |
| COLUMN_CUTAWAY | PARENT SVG `COLUMN` / `COL_TOP` / `SECTION` | 9 | s37-s38, s46, s66, s67b, s80, s82 |
| FINGERTIP_TILE | PARENT SVG `FINGERTIP` | 5 | boxer -> piano -> cow -> car; cow callback in s67b 5/5 |
| PIANO / COW | PARENT SVG `PIANO`, `COW` | 1 / 2 | s47; s57 + s67b |
| HYDRA_CHAMBER | PARENT SVG `CHAMBER` | 1 | s11 |
| SUB (+ STRIKE) | PARENT SVG `SUB`, `STRIKE` | 2 | s08 rule 3, s67b option 2 |
| FROST_VIGNETTE | PARENT SVG `FROST` / `VIGNETTE` | 2 | s28-s30 |
| SHELLS | PARENT SVG `SHELL` | 1 | s40 (tag now SHELLS START DISSOLVING HERE) |
| CAMFRAME + BONES + MUDFLOOR | PARENT SVG `CAMFRAME`, `BONES` (not "SKELETON"), `MUDFLOOR` | 2 | s42-s43 bait cam (windows 57-59) |
| MUD_CLOUD | PARENT SVG `MUDCLOUD` | 3 | s55, s56, s67b option 1 icon |
| PLATES | PARENT SVG `PLATES` | 1 | s52 |
| PROTEIN_RIBBON / MEMBRANE | PARENT SVG `PROTEIN`, `MEMBRANE` | 5 / 1 | s58, s59, s61, and the new callbacks: s64 (squashes further), s65 (holds shape), s74 (bends, springs back) |
| EVEREST | PARENT SVG `EVEREST` | 1 | s66 |
| BRANCH / THUMB_TILE | PARENT SVG `BRANCH`, `THUMB` | 1 each | s68 |
| GUT_XRAY | PARENT SVG `XRAY_GUT` | 3 | s69, s78, s78b |
| FIBRES | PARENT SVG `FIBRES` | 1 | s78 |
| XENO_LUMPS | PARENT SVG `XENO` | 1 | s72 1/2 (silent, on screen only) |
| MUDFLOOR / ROV_LIGHT / BAG | PARENT SVG `MUDFLOOR`, `ROV_LIGHT`, `BAG` | 4 / 1 / 3 | landing, s76, bag reveal, punch, bookend drift; thumbnail C |
| **BLOB** (dashed unreadable outline) | PARENT SVG `BLOB` | 2 | t4_unknown and s76_turn: the twist's mystery shape (it resolves into the BAG in s77) |
| EYE | CORE `circle` x2 (pale disc + dark pupil, scaleY open; one notation everywhere) | 3 | t1, s19, s21 (pupil x keyframe slides toward YOU on "turned toward you") |
| SONAR / SUCKER_RINGS / SCAR_RINGS | CORE `circle` (stroke) | 1 each | s13, s22, s23 |
| THOUGHT_BUBBLE | CORE `circle` + ColossalSquid `silhouette` | 1 | s15 |
| MICROSCOPE_FRAME | CORE `circle`, filled `#0b2a3a` + white 10 px stroke (as the parent does). Core `layers.tsx` has **no mask**; if a true porthole is wanted, use an evenodd ring SVG (outer rect minus circle) instead | 1 | s58 |
| LIMIT lines | CORE `rect` (dashed via svg) | 4 | s12, s63, s63b, s64 |
| FEELERS (two thin amber lines on YOU's head) | CORE `rect` x2, rotate keyframe | 1 | s65 2/2 "shrimpier" |
| Particles (biolum, swarm, eyes, mud) | CORE `particles` | 4 | s16, s43, s45, s55 |
| DEATHS / CHEATS LEFT | CORE `text` | HUD | from 0:23 / 0:44; red frame state from s65b |

## 3. Audio

| Asset | Status | Used |
|---|---|---|
| Music `deep_ocean.m4a` | KIT | bed; out for the three DEATH stamps and from the 8:54.1 turn to the bag reveal (8:58.9) |
| SFX (17 files) | KIT (`studio/public/sfx/*.wav`, all present) | per window in shotlist.md |
| Narration | NEW (render step) | 62 Kokoro am_michael lines at speed 1.0, Spark CPU only (`CUDA_VISIBLE_DEVICES=""`, `torch.set_num_threads(4)`, `nice -n 10`); 22 lines have no measured duration yet (list in script.md `timing_source`) |

## 4. Thumbnail assets (see thumbnail.md)

| Asset | Status |
|---|---|
| thumbs templates `eye`, `abyss`, `scale` | KIT |
| `humanArt` = `explainer/You` with torch glow + SLED | KIT + PARENT SVG |
| Giant squid eye subject (concept A, IT SEES YOU; now paid by line 13 "it has turned toward you" at 2:05-2:17, 21%) | KIT placeholder `squid` |
| Snailfish engraving (concept B) | **NEW** |
| Bag-as-ghost engraving (concept C) | **NEW** (BAG re-drawn in scratchboard style) |

## 5. Build gate, order, effort and render estimate

**Gate 0 (before any storyboard build): re-measure.** On the Spark, CPU only: run Kokoro am_michael 1.0 on the 22 estimated lines (6, 13, 18, 30, 31, 40, 42-45, 47-50, 52, 53, 56-61; ~240 words, about 2-4 min CPU at 4 threads, `nice -n 10`, one job at a time). Write `durations.json`, regenerate `timing.json` from it, re-time `shotlist.md` and the chapters in script.md + description.md, and confirm runtime <= 600 s (if over: hold 5.0 -> 4.5 s, then drop line 30's last sentence). Every anchor from 0:53.4 depends on this. Then rerun `scripts/originality_check.py` if any wording changed.

**Gate 1: generator delta.** Port the parent's `gen_storyboard.py` into this episode (it reads `script.md` and `durations.json`). Its `A()` raises KeyError when an anchor phrase is missing, so these anchors must change with the new text:
- s64_death3: new anchors `T(43,'It turns back')`, `T(43,'runs out')`, `T(43,'No.')` (DEATH 3 stamp).
- s65_cheat3: `T(44,'Cheat number three')`, `T(44,'shrimpier')`; s65b_reset (NEW): `T(45,'Die again')`.
- s67_rescue is retired; s67b_options (NEW): Options title `CAN YOU SAVE YOURSELF?`, items [FLOAT UP, WAIT FOR RESCUE, HOLD YOUR BREATH], `select` on `T(47,'float up')`, `T(48,'Wait for rescue')`, `T(49,'Hold your breath')`; strikes on `T(47,'buried you once')`, `T(48,'Nobody is coming.')`, `T(49,'The squeeze is.')`; 3 whoosh/impact SFX on the strike anchors.
- s71_xeno is retired; its lumps move into s72_landing 1/2 at `T(52,'Ten kilometres')`; landing thump at `T(52,'thumps')`, lock at `T(52,'This is the bottom')`.
- s73_car: `T(53,'a third stronger')` for the +31% Stat. s74_last_test: needle slide at `T(53,'slides toward no')`, stop at `T(53,'and stops')`, YES at `T(53,'Yes.')`.
- s77_bag: `T(56,'a single-use plastic bag')` (revision 1's `T(54,'No cheats,')` no longer exists). s77b_punch (NEW): `T(57,'beat you here')`, `T(57,'No cheats.')`, `T(57,'No help.')`. Tag text per shotlist window 114 (lowercase anchor `No cheats.` is a new sentence here, so the capital is correct).
- s78_fibres: `T(58,'the amphipod you met')`, `T(58,'tested included plastic')`. s78b_speck (NEW): `T(59,'Ours.')`.
- s79_pcb: `T(60,'PCBs')`, `T(60,'nearest factory')`.
- s80_swap: Options title `KILLED YOU`, items [THE COLD, THE MUD, THE FISH'S CEILING], 3 strikes + 3 whooshes on `T(61,'cold,')`, `T(61,'mud,')`, `T(61,'ceiling:')`; Headline at `T(61,'The newest')` (capital T; revision 1's `'squid,'`, `'crushing weight,'`, `'the newest arrival'` are gone).
- s60_snailfish: flip card + `mode: "lives"` at `T(40,'the question changes')`, back to `"alive"` at `T(43,'It turns back')`.
- s21_eye_face: pupil slide at `T(13,'turned toward you')`.
- Background / sled / hud / wall flags: keep the parent's (shotlist layers column now mirrors them); new shots use s65b ocean+wall+hud+sled, s67b black, s77b black, s78b dark.

**Build order + effort (agent-hours, before QA).** AliveMeter ~2 h (5 states, needle ease, raw needle track, spin, stamp slam/hold, `mode`, `frame`); DepthMeter markers + lock + waterTint ~0.75 h; Snailfish (juvenile / xray / silhouette) ~1.5 h; Amphipod (colour / xray / leg ripple) ~1 h; DeepFish (dead / timeOffset) ~0.75 h; BeakedWhale ~0.75 h; DumboOctopus ~0.75 h; thumbs Snailfish art + scratchboard BAG ~1 h; porting the generator + the delta above ~1 h. **Total ~9.5-10 h.** Optional: ColossalSquid `variant: "giant"`.

**Render estimate.** ~17,990 frames (599.6 s) at 1920x1080 / 30 fps. Baseline: the orca 16:9 cut (75 s) rendered in ~72 s at `--concurrency=4`. This episode's frames are heavier (HUD on 56 shots, the tall 700x2400 scrolling WALL SVG, particles), so plan **~15-25 min at concurrency 4** (~10 cores, `nice -n 10`, nothing else of ours running) or **30-50 min at concurrency 2** if any TTS / whisper / render of ours is running. Sequence: render the first 10 s + look-dev stills (one per zone) and Read them; then chunked `--frames` ranges (6 x ~3,000 frames) under the render lock so one failure costs one chunk, then concat. Spark only; never the Mac.
