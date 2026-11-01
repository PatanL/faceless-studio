# Test 2 build: Zack-style castle gate shot in Blender (cc-blender-skill, headless bpy)

Internal feasibility test. Original script, set and shot; not for publication.

- **Final:** `out/blender-castle/blender-castle.mp4` (repo root `out/`, not in git): 1080x1920, 30 fps, 11.2 s, H.264 + AAC, word-highlight captions burned in.
- **Variant:** `out/blender-castle/blender-castle_plain-captions.mp4`: the same render with plain white captions (VISUAL_GRAMMAR §9 measured "no karaoke highlight" in 9/9 references; the task asked for word highlight, so the highlight version is the main file).
- **Contact sheet:** `contact_sheet.jpg` (this folder, 2 fps).

## The shot

Narration (Kokoro `am_michael` through `pipeline.audio.make` on the Spark, CPU, nice 10; 30 words, 173 wpm, `originality_check.py` PASS):

> The moment your battering ram breaks through a castle gate, an iron portcullis slams down behind you, sealing you inside a stone box with a ceiling full of murder holes.

Hook formula: second person, the accident already happening, stinger noun last ("murder holes"). References and the beat-alignment table are in `script.md` (p832whe8hrI, MKRYulCq3Mo, CRGWDiIgMZ4).

One continuous camera move (no hard cuts), every state a pure function of t:

| t (s) | words | picture |
|---|---|---|
| 0.0 | The moment | frame 0 is inside the gate passage, defender side: the doors are already bulging from a blow, splinters in the air, a murder hole visible overhead (planted early) |
| 0.10 | your battering ram | second blow on the impact SFX: the doors flex, a crack of daylight, splinters fly at the lens, camera shake |
| 1.43 | breaks through a castle gate | the doors burst open on the SFX, the draw-bar snaps into two pieces, the ram shed rolls in toward camera through the doorway |
| 2.3-3.0 | (gate) | the near half of the gatehouse is sliced away top-to-bottom (cutaway, cobalt section faces) while the camera backs out sideways through the cut |
| 3.38-3.86 | an iron portcullis | oblique rear view: the raised portcullis hangs in the chamber above the entrance and gets the green "named thing" outline on "portcullis" |
| 4.49 | slams down behind you | it drops in 0.24 s and lands on the boom SFX: snap zoom +18%, shake, dust puffs, small bounce |
| 6.28 | sealing you | cyan seal strips pulse along both portcullises' contact edges |
| 7.44-7.89 | inside a stone box | orbit to the pure side section; the passage's 12 edges glow green ("stone box" is the named thing) |
| 8.53-10.4 | with a ceiling full of murder holes | crane up over the slab: the three holes get green outlines, braziers flare, cauldrons tip and pour glowing liquid down through the holes onto the shed roof (heat-ramp orange) |
| 10.4-11.2 | (tail) | caption-free hold on the pour |

## Approach

- **Scene as code:** `build_scene.py` rebuilds the whole shot from `--factory-startup` every run, then renders the frames asked for. Nothing is downloaded; every mesh is boxes, cylinders and spheres made with bmesh. About 110 objects, 0.5 s to build.
- **Run:** `Blender -b --factory-startup --python build_scene.py -- --frames 1-336 --pct 100 --samples 48 --out out/frames` (nice 10, one Blender at a time). `--look N` renders frame N from five fixed orbit angles (the MCP `look` tool's job, headless). Word times come from `audio/captions.json`, so a new TTS take re-times every beat automatically.
- **Section cut:** the gatehouse is split at X = -1.8 into a "main" mesh (section faces tagged with the cobalt cut material at build time) and a "near" mesh that a Boolean DIFFERENCE cutter (exact solver, `material_mode = 'TRANSFER'`) sweeps through from the top in 0.42 s.
- **Look:** Zack palette tokens from VISUAL_GRAMMAR §4 converted sRGB to linear (sky gradient `#a8eefc`→`#14c8f2`, lime grass, blue-grey ashlar, tan wood, cobalt section); box-projected procedural ashlar (Brick texture + grey noise + mortar bump); procedural wood (skill Recipe 12); metallic=1 iron with roughness noise; Bevel on every hard-surface part; EEVEE Next with screen-space ray tracing + fast GI (AO-like contact darkening), soft sun (4° angle) + warm gold rim sun + cool area fills + flickering torch and brazier practicals; compositor Glare BLOOM; motion blur (shutter 0.35); Standard view transform so the token hexes land as measured.
- **Signals (meaning-locked):** green = the thing being named (portcullis, stone box, murder holes), cyan = seal, orange = heat. Implemented as inverted-hull or thin-strip emission meshes with a keyframed Transparent/Emission mix.
- **Captions:** `tools/captions.py` (Pillow) draws 12 phrase cards (2-4 words, Montserrat ExtraBold 68 px, centre at 78.3% of H, white with a soft shadow, active word `#ffd64a`), one PNG per active word, plus an ffconcat list. `tools/composite.sh` overlays them and muxes the mix on the Spark (ffmpeg, nice 10, 4 threads).

## Render time

Final: 336 frames at 1080x1920, EEVEE Next on Metal (M1 Pro), 48 TAA samples, motion blur, screen-space ray tracing + fast GI, compositor bloom.

| measure | value |
|---|---|
| render call per frame | **5.6 s mean**, 5.0 s median, 3.7 s min, 13.0 s max (frames with many emissive glows and lights cost most) |
| whole sequence | 31 min 40 s wall (scene build 0.5 s; the rest is rendering and PNG writes) |
| preview stills (432x768 or 540x960, 12-16 samples) | 0.8-1.9 s per frame; a 20-frame preview pass took about 25 s including the build |
| orbit `--look` views (324x576, 8 samples) | 0.3-3 s each |
| encode + captions + mux | about 30 s on the Mac for the intermediate (ffmpeg, 2 threads), about 20 s on the Spark for both caption variants |

The Mac was heavily loaded the whole time (load average 34-58 from other work, swap 13.4 of 14.3 GB used), so these are pessimistic numbers. Free disk stayed at 27 GB or more. One Blender process at a time, nice 10, `--factory-startup` on every run.

Iterations before the final: 5 preview passes, 1 look pass and 1 full-res timing test, about 1 h from reading the brief to the final MP4. What each pass caught:

1. Towers sat 12 m in the air. My bmesh helper picked new faces by index, and the index table was stale. Fixed by using the verts that the `create_*` ops return.
2. The opening shot from outside could not see the impact: the shed hides the ram, and the gate is recessed 1.4 m. The camera moved inside the passage, so the doors burst toward the lens.
3. After the cut, the camera sat inside the near curtain wall. The near-side curtain wall and tower were deleted, since they are never seen intact.
4. A full-frame "swirl" smear at the burst. Per-frame Euler keys wrapped through plus or minus pi, and motion blur interpolated a full spin. Fixed with `to_euler('XYZ', previous)`.
5. Seen from the side, the portcullis was edge-on and hidden inside its slot. The slot now opens into the chamber, and the drop is shot from an oblique rear angle.
6. Murder holes were invisible from slab height, and the pour drowned in bloom. The camera cranes above the slab, the holes get green tags, and coal and brazier brightness came down.
7. The left gate leaf stood in front of the drop. It is now removed with the cut.
8. Rainbow tint on the stone came from noise Color, which is RGB; switched to noise Fac. Wood zebra grain came from distortion 6; lowered to 3. A green line at the wall feet was grass showing through the bevel gaps; fixed with a floor under the walls.

## What the skills helped with (and what they didn't)

Read before each phase: `text-to-blender`, `blender-pro-workflow`, `blender-modeling`, `blender-materials`, `blender-lighting`, `blender-cameras`, `blender-animation`, `blender-rendering`, `animation-quality-gate` (pinned `a2634b5`, read from `vendor/`; nothing installed).

**Helped:**
- **Process.** The pro assembly order kept the iterations cheap. It goes world reset, block-out, camera lock, light v1, geometry, materials, light v2, detail, final, composite. So did the "render and look before reporting success" checkpoint and the contact-sheet gate (no final animation without a sheet). Every bug above was caught in a still, not in the final.
- **Hard-surface finish.** "Bevel everything" (Recipe 2 and the recovery table's "videogame-y = hard shadows + sharp geo") gave the clearest jump over the 2D/three.js prototype: every stone block, plank, rafter and bar catches a highlight.
- **Materials.** "Metallic is a switch" plus roughness noise for iron. Recipe 12 procedural wood, retuned to Zack's tan tokens. "Flat PBR looks plastic: add procedural variation" pushed the ashlar Brick + noise + mortar-bump stone.
- **Lighting.** Area/sun for soft shadows, `aim_at` (to_track_quat) for every light, warm key plus cool fill ("golden/teal"), and practicals (torches, braziers) as point lights.
- **Mechanics.** Boolean DIFFERENCE Recipe 4 is the cutaway mechanism. Naming (`GEO-/MAT-/LGT-/CAM-/RIG-/FX-`) kept 110 objects debuggable. "Set fps before animating."
- **Version notes** (via SETUP.md's 4.3 probes): `BLENDER_EEVEE_NEXT`, no `use_bloom` (so a compositor Glare BLOOM node instead), `scene.node_tree`.

**Didn't help, or had to be invented here:**
- **Headless use.** The skills assume an MCP viewport and say nothing about it. The `--look` orbit renders and the per-phase preview passes replaced `get_viewport_screenshot` and `look`.
- **Real-world dimensions.** `common-object-dimensions.md` has no castle, gate, portcullis or siege-engine entries, only an 80x200 cm interior door. Sizes came from general knowledge: a 3.6 m passage, a 4.4 m opening, a 4.6 m ram shed.
- **Format and layout.** Nothing on vertical 9:16 framing, caption safe zones or Zack's signal lexicon. Those came from VISUAL_GRAMMAR.
- **Camera motion.** No camera-path tools beyond two-key dolly and orbit recipes. A C1 Hermite spline through timed keys, plus shake and snap-zoom envelopes, was written here. The skills' Track-To constraint would have avoided the Euler-wrap smear; keying rotations directly (for shake) is what caused it.
- **Bespoke techniques written here:**
  - box-projected brick coordinates;
  - inverted-hull glow outlines with a keyed Transparent/Emission mix;
  - the section-face tagging at build time;
  - the growing pour (`bevel_factor_end`).
- **Animation guidance is generic.** Easing, keyframes and drivers are covered. Impact timing, physics-ish splinters and contact (doors flex on the blow, the portcullis lands on the boom) had to be authored as pure functions of t, as in the 2D prototype.

## Review against the 41/100 prototype

Same rubric and weights as `experiments/zackd-proto/NOTES.md` §Review. Method: 2 fps contact sheet (`contact_sheet.jpg`), a 10 fps strip over the burst (1.3-2.4 s), `tools/measure.py` on 23 rendered frames, and the pipeline's loudness report. Caveats: I built it and I scored it, so expect some bias. I did not put frames side by side with the reference sheets, and I did not listen to the audio by ear.

| area | weight | proto | this | why |
|---|---|---|---|---|
| Visual polish | 20 | 30 | **55** | **Better than the prototype:**<br>- bevels on every block, plank and bar;<br>- soft sun shadows and AO-like contact darkening;<br>- procedural wood and iron variation;<br>- local bloom on glows: the green tag stays local, not a full-frame flood;<br>- a cobalt section cut that reads as a Zack cutaway.<br>**Still cheap:**<br>- the ashlar is too regular and pale, so it reads as bathroom tiles;<br>- the lime ground fills the bottom 30-35% of every section shot;<br>- tipped cauldrons read as dark balls;<br>- the boiling pour is mostly a bloom blob;<br>- warm share is only 10% (target 15-50%) because the warm subject is small in frame. |
| Character / subject appeal | 20 | 15 | **45** | No character by design: rigid objects only, no hands. The hero is the ram shed, a warm, readable toy machine with a swinging iron-capped ram. That is far more appealing than the capsule mannequin, but there is no face or hand to care about. |
| Narration literalized | 20 | 50 | **70** | **On time:**<br>- doors flex on the first blow;<br>- they burst on "breaks" (the SFX frame);<br>- the portcullis is tagged on its noun and lands on the "slams" boom;<br>- seal strips on "sealing", the box outline on "stone box", hole tags on "murder holes";<br>- murder holes are planted overhead from frame 0.<br>**Misses:**<br>- the ram itself is unseen until 1.45 s, about 0.4-0.9 s after "battering ram";<br>- the payoff (what the holes are for) reads weakly. |
| Motion and camera | 15 | 45 | **65** | One continuous motivated move: push-in, retreat ahead of the ram, exit through the cut, oblique on the drop, orbit to the side, crane over the slab. Shake on all three hits, a snap zoom on the slam, motion blur. But there are zero cuts (ASL 11.2 s against 1.4 s), the 6-8.5 s stretch is a slow drift, and the door burst is fast but has no anticipation. |
| Captions | 10 | 78 | **70** | Geometry on spec: centre at 78.3% of H, 68 px, phrase cards of 2-4 words, ≤72% of W. The main file has the requested yellow word highlight, which VISUAL_GRAMMAR §9 says the references never use. The plain variant is on spec. |
| Audio | 15 | 50 | **50** | -14.0 LUFS integrated, LRA 0.9 (pipeline default; the Zack spec wants about -12 and LRA about 2). Impact SFX on both blows, the boom on the slam, a riser into the payoff. No foley for splinters, the shed rolling, dust or the pour. Not judged by ear. |
| **Weighted total** | | **41** | **58 / 100** | |

**VISUAL_GRAMMAR §12 colour checks:**

| check | target | measured |
|---|---|---|
| median luma | 100-175 | 157.5 |
| median saturation | 0.35-0.60 | 0.538 |
| blue share | 40-78% | 60.7% |
| warm share | 15-50% | **10.2%**, short; much of the saturated area is lime grass, outside both hue bands |
| centre minus corner | about +10 | -3.5 (no vignette, the sky is bright at the top) |

**Verdict.** Blender closes most of the surface-polish gap that sank the prototype, and it does so cheaply: about 1 h of authoring and 32 min of rendering on a loaded laptop. It is still a "clean toy diorama", not Zack's toy-real. The fixes left are art direction, not tech:
- chunkier, irregular stone with real wear;
- a bigger warm subject in frame;
- a darker or sky-coloured ground instead of flat lime;
- real cuts every 1.5 s (several cameras, not one long move);
- a proper liquid or steam effect for the payoff;
- foley.

Rigid-object mechanisms are confirmed as the lane where this stack works. The cutaway, the drop and the signal glows all read.

## Files

| file | purpose |
|---|---|
| `build_scene.py` | the whole shot: geometry, materials, lights, camera, animation, render settings |
| `script.md` | narration with references and beat table |
| `audio/captions.json`, `cues.json`, `report.json`, `waveform.png` | Kokoro word times, SFX cues, loudness report (wavs stay out of git; they are on the Spark under `~/studio/app/experiments/blender-castle/audio/`) |
| `tools/captions.py`, `tools/composite.sh` | caption cards and the Spark-side burn-in + mux |
| `tools/sheet.py`, `tools/measure.py` | contact sheets; VISUAL_GRAMMAR §12 colour checks |
| `fonts/` | Montserrat ExtraBold (OFL) |
| `SETUP.md`, `tools/*probe*`, `compat/` | test 2 setup (commit 2abd849) |
