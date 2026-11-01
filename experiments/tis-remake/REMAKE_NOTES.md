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
