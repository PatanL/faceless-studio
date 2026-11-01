# TIS AK-12 remake v1: build notes (internal benchmark, never published)

Shot-for-shot remake of SHOTLIST.md in code: every asset is a layered SVG/React component, with no reference pixels and no traced frames. The reference audio is muxed in for timing only, and the result stays in `out/` (git-ignored).

## Layout

```
remotion/                own Remotion entry (no deps of its own; uses studio/node_modules via a symlink on the Spark)
  src/Main.tsx           timeline: 9 scene blocks, 8 matte transitions, caption layer
  src/Captions.tsx       the reference's 13 caption pages (K2D Medium, 70% black box, hard swaps)
  src/lib/anim.ts        easings, keyframes, camera (pos/scale/rotation, log-scale interpolation, parallax), lip-sync from word timings, blinks
  src/art/defs.tsx       palette tokens, capsule camo patterns (RU/UA/officer, H-glyph blobs), soft cast shadow, smear filter
  src/art/soldier.tsx    cut-out puppet: 2-bone IK arms and legs, kneel/march/stand, beard/goatee/moustache, helmet+goggles or field cap,
                         brows/mouth/eye sets (hearts, blink, sweat), skin-circle hands (pointing variant), flag patches
  src/art/guns.tsx       AK-47 (wood), AK-12 (rail, vented handguard), AK-12 with optic/foregrip/suppressor, M4; anchor points for hands
  src/art/props.tsx      clouds, pole flags, sparkle, muzzle flash, explosion, calendar, clipboard, quonset, lattice tower, target, hedgehog, wire, crates
  src/scenes/*.tsx       Hook, Base, Range, Office, Ruins, Pink, Armoury, Ball, Camp
  tools/stills.mjs       render any frames to JPEG (one bundle, one browser) for quick contact sheets
  public/fonts/          K2D Medium (OFL), Montserrat ExtraBold (OFL)
tools/sync.sh            push this folder to the Spark and link node_modules
tools/compare.sh         side-by-side MP4 + 12-pair frame sheet (runs on the Spark)
```

## Run (Spark, CPU only)

```
experiments/tis-remake/tools/sync.sh
ssh dgx-spark 'cd ~/studio/app/experiments/tis-remake/remotion && source ~/.nvm/nvm.sh && nvm use 22 && \
  export PATH=$HOME/studio/bin:$PATH CUDA_VISIBLE_DEVICES="" && exec 9>~/studio/locks/render.lock && flock 9 && \
  nice -n 10 node_modules/.bin/remotion render src/index.ts TisRemake out/remake_v1_silent.mp4 --concurrency=4 9>&- && \
  ffmpeg -i out/remake_v1_silent.mp4 -i ~/studio/refs/tis-ak12/audio.wav -map 0:v -map 1:a -c:v copy -c:a aac -shortest out/remake_v1.mp4'
ssh dgx-spark 'bash ~/studio/app/experiments/tis-remake/tools/compare.sh v1'
```

## v1 result

- `out/remake_v1.mp4`: 1080x1920, 30 fps, 1680 frames, 56.0 s, H.264 + the reference AAC audio.
- **Render time:** 35.2 s on the Spark CPU (Remotion `--concurrency=4`, `nice -n 10`, under `~/studio/locks/render.lock`, `CUDA_VISIBLE_DEVICES=""`). The audio mux took about 1 s, and `compare.sh` (side-by-side and sheet) took about 18 s.
- `out/side_by_side_v1.mp4`: reference left, remake right, reference audio.
- `out/pairs_v1_sheet.jpg`: 12 pairs at 1.25, 3.5, 6.5, 12, 14.5, 20.5, 23, 27, 33, 37, 45 and 54.75 s.

## What v1 matches

- **Timing.** All 26 framings and the 9 transitions are on the SHOTLIST times, and the caption pages swap at the measured times.
- **Transitions.** Each type is built as a matte:
  - two silhouette mattes: the incoming soldier's own body, drawn with an alpha mask;
  - two slash wipes: tapered streaks at -30°, with the outgoing frame smeared along the streak direction;
  - an iris with a soft rim;
  - three organic blob/splatter mattes (noise-modulated lobes, with debris and tendrils);
  - an explosion cover with a camera jump.
- **Camera.** Every block has its own world camera with the reference's push, pull and dutch-rotation moves. The calendar and clipboard UI are pinned to the screen.
- **Acting.** Mouths are lip-synced to the reference word timings and characters blink. B points, A swaps the AK-47 for the AK-12 off-frame, and the calendar types "2023". Checks pop with an overshoot, C fires bursts with recoil and flicker, D grows in and gets heart eyes, the official scratches his head and taps the gun, and the squad does a patrol march. The selector hand fumbles, F yells, the prone soldier crawls, and the officer hands out a rifle. The ball shuffles, waves its rifles, sweats and darts its eyes. G pops up, and the sparkles finish the end.
- **Shading.** The reference construction is followed: flat fills, one shadow-side shape per part, top-edge highlights, a rim light on the lit cheek, and soft contact shadows.

## Known gaps (v2 candidates)

- The faces are simpler than TIS's: there is no hair-strand detail, and every character uses one head shape. Officer and official proportions are approximate.
- The hero rifle in the hook reads chunkier than the reference, with fewer cut-outs, and the hook sparkles are smaller.
- The silhouettes are leaner than TIS's. Their pants are narrower and their shoulders less bulky, and the camo blobs are larger than the reference's.
- Some framings are approximate rather than measured: S06 gun angle, S19 prone pose, S21 rifle handoff timing, S24 crate layout.
- There is no secondary cloth motion (sleeves and straps), and casings and sparks are minimal.
- The official is a generic, unnamed character (rule 5), so S13 intentionally does not match the reference likeness.

## v2 (judge fix round)

Outputs: `out/remake_v2.mp4` (1080x1920, 30 fps, 1680 frames, 56.0 s; render 38 s on the Spark CPU at `--concurrency=4`, `nice -n 10`, under the render lock), `out/side_by_side_v2.mp4` and `out/pairs_v2_sheet.jpg`. New helpers: `tools/stills.sh <tag> <frames...>` renders a contact sheet of any frames, and `tools/pairs.sh <ver> <out.jpg> <cols> <times...>` builds ref|remake pairs at any times. Both run on the Spark.

Fixes applied, in order of impact:

1. **Rifles redrawn** (`art/guns.tsx`). Every gun now uses a 5-step grey ramp (`G.g0`–`g4`) in place of near-black: dark furniture, a mid-grey receiver, lit upper planes and specular top edges. Added rail teeth with lit tops, vented handguards with bevels, ribbed curved magazines, a ribbed pistol grip, the AK selector lever with a tan tip, rivets and a gold accent, plus wood grain on the AK-47. A `lod` level (0/1/2) scales micro-detail with camera distance, and the hero shots (S01, S06, S08, S12, S13, S15, S17, S21, S26) use lod 2. The hook rifle is drawn slimmer (non-uniform 2.0 x 1.78) to match the reference's long, lean read, and the launcher is restyled on the same ramp.
2. **Grips and hands** (`art/soldier.tsx`). Hand circles are 22% smaller. The support hand and arm are drawn behind the rifle, and the near hand sits on the pistol grip below the receiver, so the gun's silhouette stays readable. A also releases the rifle during the off-frame swap (7.6–8.7) instead of stretching his arms after it.
3. **Re-blocked shots.**
   - S05 is a gentle push that keeps A's face and the incoming rifle in frame.
   - S06 is a receiver close-up at about 4.5x, with the diagonal rifle as the subject.
   - S07: B is larger and less cropped.
   - S13 creeps steadily from mid (1.04x) to close (1.62x). The official is 14% larger, and a leather chair, a second paper pile, an in-tray and a pen cup are added.
   - S15 is a receiver ECU, with the thumb hunting between the grip and the selector.
   - S16 shows E large with a grimace.
   - S17 shows F at 3.3x as a left-half close-up.
   - S21 is a clean MCU of B with the rifle on a diagonal: A is out of frame and the officer appears only at the right.
   - S26 is a tight CU (about 3.3x total), with the M4 raised across the frame.
4. **Flag patches.** Each patch is drawn in its own upright space with horizontal stripes and is clamped to ±24° of upright, so it can no longer flip upside down or turn 90°.
5. **Characters.** Faces are 16% wider, with bigger ears, hair tufts under the helmet and tapered brows. Torsos are 12% wider, trousers are thicker with a thigh pocket, and boots are 18% bigger. Camo uses smaller, lower-contrast capsules with no H glyphs. The officer/quartermaster has his own build: 1.22x width, a paunch and wider trousers.
6. **Props.**
   - The target is drawn in 3/4 view, with a squashed face, a visible rim thickness and bullet holes that pop in with crack stars.
   - The S17 rubble is now a wreck: a burnt-out car, slabs, rebar, coiled wire and debris.
   - Crates have latches, inset panels with bevels, corner protectors and stencil strips.
7. **Motion.**
   - The explosion cover enters at 34.55 and fills the frame from about 34.78 to 35.12, so the cut at 35.10 happens under it. The S17 camera whips right so F is gone by about 34.75.
   - The robot ball has a crouched side-shuffle with splayed knees, a ±9° lean and varied rifle angles. Its S23 push now ends at 3.3x by 48.35, overflowing the frame.
   - The point, AK-47 raise, AK-12 landing, D's rifle raise and hug, B's new-rifle raise and G's M4 lift all overshoot and settle (outBack).
   - The hook has 8 bigger sparkles travelling along the rifle. The title pills clear by 3.0, and the S02 matte now runs 2.97–3.27 (it was 2.87–3.20).

Known gaps after v2:
- The S17 explosion lands earlier than the reference's own (about 34.9), as the judge asked.
- F still faces right rather than three-quarter to the camera.
- The S26 M4 is smaller than the reference's.
- The prone S19 soldier is still simple.

## v3 (judge fix round 2)

Outputs: `out/remake_v3.mp4` (1080x1920, 30 fps, 1680 frames, 56.0 s; render 40 s on the Spark CPU at `--concurrency=4`, `nice -n 10`, under the render lock), `out/side_by_side_v3.mp4`, `out/pairs_v3_sheet.jpg` (the standard 12 pairs) and `out/pairs_v3_fixes_sheet.jpg` (20 pairs at the judged problem times: 9.8, 18.6, 20.8, 21.5, 23, 27, 28.9, 31.5, 34.7, 34.95, 36.5, 37.6, 38.4, 39.5, 40.6, 45, 47.8, 54.75, 3.5, 33).

Fixes, in the judge's order:

1. **S12 black void** (`scenes/Range.tsx`). The sky plate now runs from y -3000 to 6000, so no rotated or pushed camera can expose the empty canvas. D is also smaller now (see 7), so the push goes to 3.55x, and the frame stays on sand and wall.
2. **Head kit** (`art/soldier.tsx`, used by about 15 shots):
   - The face is a rounded squircle path (`FACE`) with soft jaw corners, not a rectangle.
   - Each character has a hair mass under the helmet (`Look.hairStyle`): `crop` is a dark block at the back of the skull down to the sideburn (A, C, H, the officer); `side` adds a fringe tuft (B, D, G); `swoop` is a fringe that sweeps diagonally across the forehead (E, F, Blond). F is now blond, as in the reference.
   - A back-of-skull hair shape sits behind the face, and the ear sits over the sideburn.
   - The full beard, goatee and moustache are redrawn as rounded silhouettes.
3. **Acting.**
   - S14: each squad member has his own crouch, stance (`Pose.stance`), lean, gun angle and height, head tilt, step phase and speed, brows and mouth, so it is no longer a clone line.
   - S20: the queue is re-spaced (150/345/545). D stands with his thumbs in his belt, a wide stance and his head cocked. A talks with an open-palm gesture. B scratches his helmet rim with an index finger (`Pose.pointAng`), then reaches and points at the rifle the officer holds out (40.15–40.55) before taking it at 41.0.
   - Grip wrap, for every soldier holding a rifle: the near hand's thumb lies along the receiver, and the support hand's three fingertips curl round the handguard. These are drawn over the gun.
4. **S18 explosion** (`art/props.tsx` `Burst`, `scenes/Pink.tsx`). The burst is layered: three-tone tapered flame petals, overlapping fire-cloud circles, a yellow core, dark smoke puffs and flying debris. It is about 640 px across and placed low, erupting lower right at 34.74 and drifting to the lower left by about 35.34. Because it no longer covers the frame, the S18 truck right (about 860 px, 34.42–35.10) is visible again, with F exiting left.
5. **S19 rebuilt.**
   - Background: a parallax far layer (sunset sky, clouds and a pale damaged skyline). The middle block is now a lower, shell-damaged ruin, so the sky and skyline show above it. The near blocks have broken tops, and there is a pavement and kerb.
   - Hedgehogs: four chunky, shaded hedgehogs (two crossed beams plus a receding one, lit tops, dark undersides, cut-face ends, a gusset plate and bolts).
   - Soldiers: two standing soldiers with distinct stances, both firing. The prone soldier has rounded boots, padded pouches and a patch.
   - Camera: the shot opens tilted up on the blocks and sky, settles onto the barricade (35.1–36.0), then pushes in slowly to 1.17x.
   - The S19→S20 blob wipe now runs 38.30–38.68 (0.25 s earlier).
6. **Captions** (`Captions.tsx`). K2D Medium with a 1.6 px same-colour stroke for the reference's heavier weight, 78 px type, -1.2 px tracking, and a box at least 928 px wide with 52 px side padding.
7. **Scale gags.**
   - S11: D is a small figure (scale 1.08, down from 1.67) beside a bigger target, which now sits lower and further left.
   - S15: E's near hand balloons to 1.85x over the receiver (`Pose.handNScale`) and stays big through the S16 tilt. S16 frames E smaller (2.7x).
   - S26: the M4 is the hero. It is drawn 1.5x, lifted to a 45° diagonal so the magazine hangs down-left instead of sticking out sideways, and G's face is cropped at the right edge. The sparkles are bigger.
8. **Polish.**
   - The iris transition's glossy rim strokes are removed.
   - S06 is a hard cut at 9.0 to a receiver CU with no head or neck (`Pose.noHead`).
   - S22 has 64 two-tone diagonal streaks, a bigger ball (R 162), thicker legs and wider rifle waves. S23's brows act, and the ball has a terminator crescent and gloss highlights.
   - S13: the scratching hand goes behind the official's head, with the arm drawn before the head and the elbow raised.

Still open after v3: the hook rifle silhouette (S01), the S03 flag dominance, the S08 muzzle flash style, F is still in profile rather than 3/4, the S04 AK-47 swap, and S24/S25 crate perspective.
