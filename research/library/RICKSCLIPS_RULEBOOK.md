# RicksClips3000 craft rule book (story lane)

Built 2026-11-02 from an every-frame (30 fps) study of all 24 story-style RicksClips3000 Shorts (2026-10-07 to
11-01), plus the measured metrics for the same 24. Internal research only: no reference frames are in the repo, and
nothing here (characters, scripts, compositions) is for reuse. We copy the craft, not the content.

**Sources**

- **Frame study:** one frame reviewer per video read every frame on 2 s frames30 sheets (16-39 sheets per video, 640
  sheets in total). They wrote shot lists, character animation, lighting, effects, sets, captions, micro-details and
  flaws, each with frame numbers. The sheets and their JSON stay on the Spark (`~/studio/refs/lanes/ricks/f30root`).
- **Measured:** `research/references/data/ricks24_metrics.json`. It covers all 24 at 240x426, measured with
  frame_metrics, camera_motion, look_stats, speech_pace and frames30. `story_lane_check_data.json` holds 720p numbers
  for 8 of them.
- **Our state:** `docs/PARITY_LOG.md` (v5, v6, the v6 blind panel, and the v7 3D check), the 3D kit in
  `experiments/three-lane/src/kit/` and the stick rig in `studio/src/kits/explainer/stick/person.tsx`.

**How to read the numbers**

- **"n/24"** is how many of the 24 videos follow the rule.
  - Measured rules are counted exactly.
  - Observed rules are counted from the reviewers' notes. Treat those counts as ±2, because a reviewer who didn't
    mention something may still have seen it.
- **Ranges** are min / median / max across the 24 videos.
- **Frame refs** are `video id F<frame>` at 30 fps.
- **Camera speed** is in px/frame at 720p-equivalent scale. The 240p reading agrees with the 720p one within about
  10 %.
- **Resolution-bound metrics:** ink_edge, soft_edge and acutance depend on resolution, so a 240p number can't be
  compared with a 720p number. The 720p ranges for 8 references are quoted where they matter.
- **Video ids:** the short forms are the first 4 characters (`0m6G` = 0m6G8pDtzNs).

**Sample.** 24 videos.
- **Top 8** (8.7-30.7M views): VS1Z, 0m6G, eQR3, PL-Y, GM9U, Mz72, 7xS8, lnYL.
- **Middle 8:** PLe2, TgyH, nzbk, LC8h, WbRd, VKsa, hdhg, DEe0.
- **Bottom 8** (0.1-4.6M): 5WMQ, eSRn, ZDy3, jpFJ, uRkL, t3OX, _sUA, CJwg.
- **Older 12** (10-07 to 10-19): WbRd, eSRn, uRkL, PL-Y, TgyH, hdhg, eQR3, CJwg, PLe2, _sUA, jpFJ, VS1Z.
- **Newer 12** (10-19 to 11-01): lnYL, nzbk, 0m6G, VKsa, GM9U, DEe0, t3OX, LC8h, ZDy3, 5WMQ, Mz72, 7xS8.

---

## 1. The rules

### 1.1 Shots and camera

| # | Rule | n/24 | Range (min / median / max) | Frame refs |
|---|---|---|---|---|
| C1 | **The camera never parks.** It moves (≥ 0.3 px/f) in almost every frame. | 24/24 measured | moving 95.3 / 99.7 / 100 %; dead-still frames 0 / 0.3 / 4.7 % | 0m6G F146-F235 (one truck, pan and push through a door); 7xS8 F112-F269 |
| C2 | **The camera moves at real speed.** | 24/24 | median speed 3.1 / 5.6 / 17.2 px/f (720p refs 5.8-11.1) | lnYL F0-F53 (orbit, push along the barrel, through the muzzle) |
| C3 | **Moves are frequent and eased.** Each move eases in and out; none is linear end to end. | 24/24 | 3.8 / 6.2 / 13.4 moves per 10 s; smootherstep-equivalent length 18.5 / 40.7 / 114 f; attack 4.5 / 11.8 / 20.5 f; release 4.5 / 10.8 / 34 f; peak 10.8 / 19.3 / 29.3 px/f | 0m6G F0-F12 (dolly-in, most travel in F0-F9, settles by F12); TgyH F1140-F1165 (5 f in, 12 f fast, 6 f settle) |
| C4 | **Every hold pushes in.** Quiet frames still zoom, mostly inward. | 24/24 | zoom active in quiet frames 68 / 82 / 97 %; push-in share 48 / 69 / 88 %; rate 0.18 / 0.24 / 0.76 %/f (the tool under-reads by about 25 %) | 0m6G F900-F998 (1.7x push on the boss's face); Mz72 F1494-F1572 |
| C5 | **Some moves are snap whips.** A whip reaches its peak in 3 frames or fewer, at 25 px/f or more. | 23/24 | 0 / 5 / 14 per video | 0m6G F45-F49 (crane up after the ejector seat); LC8h F430-F433 (crash zoom to the holster) |
| C6 | **The opening is one continuous move.** The first dissolve or cut comes only after the hook has played out. | 24/24 observed | first non-camera transition at 0.7 / 3.4 / 12.4 s | ZDy3 F0-F370 (12.3 s, one take); hdhg F0-F226 (fall, then into the eye) |
| C7 | **Frame 0 is already in motion**, from the camera or a character mid-action. | 23/24 (not VKsa: 33 f locked) | camera clearly travelling within F0-F10 in about 15/24 | jpFJ F0 (pouch mid-air); eQR3 F0-F11 (walker leaving frame) |
| C8 | **The camera follows a motivated path:** a thrown object, a cable, a string, a falling drop or a bullet. | ~15/24 | follow length 10-60 f | GM9U F60-F99 (up the bell string); uRkL F711-F733 (tilts with the sap drop, then catches it landing on the head); eSRn F683-F697 (along the power cable) |
| C9 | **The camera flies through an object into the next place:** a window, eye, pupil, screen, photo, door, hull hole or muzzle. | ~19/24 | through-move 5-20 f | hdhg F197-F227 (into the pupil, iris opens on the brain office); lnYL F69-F79 (through the hull hole); t3OX F205-F239 (through the shop glass) |
| C10 | **Dutch roll appears on wide or dramatic moves** (5-35°). | ~10/24 | — | 0m6G F146-F199 (5-10° held); PL-Y F862-F892 (board levels from -15° to 0) |

**Older vs newer.** Newer videos move faster and more sharply:
- median speed: 6.2 against 5.0 px/f;
- attack: 8.5 against 14.5 f;
- peak: 23.5 against 15.9 px/f;
- snaps: 7 against 3 per video.

**Top vs bottom.** The top tier's camera is faster: median speed 7.8 against 5.8 px/f.

### 1.2 Transitions

| # | Rule | n/24 | Range | Frame refs |
|---|---|---|---|---|
| T1 | **Few hard cuts.** | 24/24 have ≤ 3; 11/24 have none | 0 / 1 / 3 | VS1Z F92 (its only cut) |
| T2 | **The default scene change is a short cross-dissolve.** | 24/24 observed | about 4 / 12 / 20 per video; 2 / 6 / 17 frames each, typically 5-8 | GM9U F394-F403 (10 f, lit window into the attic); VS1Z (19 of its 20 changes are 3-6 f dissolves) |
| T3 | **Gradual transitions dominate:** dissolves plus fast camera travel. | 24/24 measured | 6 / 18 / 26 per video; 9.2 / 18 / 24.8 per minute | — |
| T4 | **At least one match dissolve:** a shape or object stays in the same screen spot across the change. | ~17/24 | 1-4 per video | GM9U F1116-F1124 (wall bell to hand bell), F1386 (shovel to shovel); jpFJ F995-F999 (coin to head); 0m6G F72-F79 (the button holds its place) |
| T5 | **Frame-in-frame changes:** a shot becomes or leaves a photo, monitor, fishbowl, mirror or peephole. | ~9/24 | 8-20 f | VKsa F649-F659 (fantasy shrinks into the fishbowl); eSRn F548-F558 (bike shot becomes a polaroid); nzbk F1554-F1571 (push into the polaroid) |
| T6 | **In-world wipes:** smoke, a tree trunk, crates, curtains or a foreground pole cover the change. | ~9/24 | 3-20 f | jpFJ F144-F164 (tree trunk), F171-F189 (fish crates); 7xS8 F109-F111 (black smoke); lnYL F540-F548 (cloud wipe) |
| T7 | **Iris and circle transitions** (pupil, spyglass, peephole, can opening). | ~6/24 | 3-10 f | 5WMQ F545-F549 (iris from the buddy's eye); VKsa F370-F373 |
| T8 | **The time of day changes inside a held shot**, as a relight rather than a cut. | ~12/24 | 6-40 f | nzbk F752-F760 (day to night, 9 f); uRkL F1527-F1556 (dusk to night, about 25 f); GM9U F1560-F1576 (sunrise warms the room) |

**What the references get away with.** Reviewers flagged muddy double-exposure dissolves as a flaw in about 16/24
references (0m6G F136-F146; LC8h F935-F947). Our own frame reviewers and panel penalise ghosting, so we keep the
dissolve's *function* and avoid its ghost (see gap 3).

### 1.3 Character construction and animation

| # | Rule | n/24 | Range | Frame refs |
|---|---|---|---|---|
| A1 | **Construction.** A flat 2D character (white round head, thick dark ink outline, stick limbs, bean or capsule body) sits in a lit 3D or painted world. | 19/24 2D cards; 4/24 3D bodies with 2D decal faces (0m6G, ZDy3, CJwg, eQR3) | outline about 2-4 px at 720p | 7xS8 F0-F53; CJwg F452-F455 (decal slides round the sphere to fake a head turn) |
| A2 | **Faces are whole drawings swapped on one frame**, with no in-betweens. | 20/24 (DEe0, PL-Y, nzbk and TgyH morph over 1-4 frames, the generated-video tell) | — | 0m6G F578-F582 (one-frame change, then held 18+ f); LC8h F415-F416 |
| A3 | **Expressions are held, then swapped on the word.** | ~22/24 | typical hold 6-40 f; reaction runs 1-4 f per drawing; longest holds 40-220 f | eQR3 F388 (smile lands on "arrested."); hdhg F128-F191 (deadpan 60 f, 2-frame smirk, terrified on "terrified,"); VKsa F1043-F1263 (cheer held 220 f) |
| A4 | **Big expression vocabulary.** About 8-15 face states per lead, beyond "happy/sad": ring eyes, >< squeeze, X eyes, spiral eyes, grid-teeth grimace, half-lid smug, wink, ^^ closed-eye bliss, wavy worried mouth, dead-dot pupils. | 24/24 | — | VS1Z F1056-F1083 (waking in stages, then hair-shock spikes); t3OX F2203 (pupils lose their rings: the "memory gone" tell) |
| A5 | **Blinks are rare and short.** | 24/24 have blinks | closed for 1 / 2 / 4 f; irregular, about every 2-10 s (eQR3 has about 3 in 45 s; DEe0 one every 1.5-4 s) | VS1Z F117 (1-frame blink); Mz72 F295-F297 (half, closed, half) |
| A6 | **No idle breathing.** Bodies freeze between poses and the camera carries the life. | 21/24 (DEe0, jpFJ queue and eSRn have a 1-3 px bob) | frozen body holds of 20-60 f are common | LC8h F318-F347 (Eddie, sub-pixel only); 5WMQ F180-F239 (MC on one drawing 60 f) |
| A7 | **No lip-sync to the narrator.** Mouths change with the expression. | 24/24 | — | PL-Y (static mouth for 39 s) |
| A8 | **Quoted lines get loose mouth flaps.** | ~14/24 | new shape every 2-4 f, from 2-5 shapes | 0m6G F944-F968 (grid, flat, open-wide and open-tongue); CJwg F296-F334 |
| A9 | **Gestures and prop moves take 3-12 frames, on 1s, eased**, and land on the caption word. | ~22/24 | 3 / 6 / 12 f | VKsa F155-F157 (ticket flick, 3 f, arm overshoots F158-F162); LC8h F1070-F1078 (scroll raised in 4 poses) |
| A10 | **Walks are cheap.** Two to four leg poses, a step every few frames and a small vertical bob. Often the walker is half hidden (behind a stack or bars) or seen from behind. | ~18/24 show a walk | step 3 / 7 / 14 f | eQR3 F243-F313 (walker hidden behind the bucket stack); VS1Z F1310-F1379 (bob about every 8 f, lantern swings against it) |
| A11 | **No hair or cloth secondary motion.** Props carry the overlap: hats pop off, tags swing, keys dangle, handcuffs bounce. | 21/24 no cloth; ~16/24 prop overlap | prop settle 10-25 f | LC8h F505-F531 (hat hangs at frame top 25 f); TgyH F272-F300 (cuffs on a spring); PLe2 F1205-F1221 (price tags swing and settle) |
| A12 | **Cartoon emotion marks pop on with the expression**, with no fade: sweat drop, tears, steam puffs, anger vein, blush, colour fill of the head. | ~21/24 sweat drops | — | 7xS8 F515-F520 (purple fills the head like liquid), F600-F609 (drains); uRkL F1160-F1169 (red heat rises in the head) |
| A13 | **Squash and stretch is almost never used.** | ≤ 4/24 use it | — | t3OX F2007-F2010 (the only squash, saved for the payoff) |
| A14 | **Faces stay near white but take the scene's tint at night or by a lamp.** | ~15/24 | — | VS1Z F995-F1379 (heads graded lavender-pink in moonlight); LC8h F1290-F1304 (phone screen keys the face) |

### 1.4 Lighting and colour over the story

| # | Rule | n/24 | Range | Frame refs |
|---|---|---|---|---|
| L1 | **Each scene has one clear key light and one colour mood.** | 24/24 | — | 0m6G F0-F75 (cool fill, warm shoji backlight, red button bloom) |
| L2 | **The story has a time-of-day or mood arc:** day, golden, night, dawn. | ~20/24 | 2-5 distinct light states per video | GM9U (dusk, cross-section, snow night, candle attic, daylight flashback, sunrise); lnYL F1000-F1080 (time-lapse to dusk, the ship becomes a lantern) |
| L3 | **The explanation goes night-blue**, when there is a late reveal. | 4 of the 10 with a late "You see" | frame b* drops by 17-53 (0m6G -8 to -30, Mz72 -1 to -54, eQR3 +16 to -13, VKsa +14 to -16); GM9U goes the other way (sunrise) | Mz72 F813 on |
| L4 | **Light events land on a keyword:** a flicker, flash, colour flood, alarm wash or glow ramp. | ~15/24 | 1-4 frame pop or 6-25 f ramp | eQR3 F72-F74 (neon flickers on at "gambling"); hdhg F982 (red alarm snaps on at "frightened", fades F1060-F1066); TgyH F283-F299 (police red/blue, every 3 f) |
| L5 | **Emissive practicals with bloom:** lamps, windows, screens, buttons, glowing props. | ~22/24 | — | t3OX F236-F255 (helmet glow); 7xS8 F1152-F1260 (rail heat ramp from steel to white) |
| L6 | **Shadows are coloured, never pure black.** | 24/24 median frame has 0 % black area | median black area 0 / 0 / 9.9 %; non-ink p5 0.04 / 0.17 / 0.27 (720p refs 0.09-0.23); 6/24 (night-heavy) have > 1 % black in > 30 % of frames | — |
| L7 | **Shadow hue is violet-blue more often than warm.** | 14/24 violet-blue (Lab hue 250-330°); 10/24 warm (31-61°, one at 204°) | — | top tier median 295° against bottom 238° |
| L8 | **Grade is moderate, not loud.** | 24/24 | luma p50 0.22 / 0.47 / 0.65; HSV saturation 0.26 / 0.46 / 0.62; colourfulness 15 / 26 / 35 | — |
| L9 | **Characters get contact shadows, not form shading.** | ~18/24 | — | LC8h F60-F169 (Eddie's shadow streak); flaw where missing: VKsa, VS1Z (floating) |

**Top vs bottom.** The top tier is darker and cooler:
- luma: 0.39 against 0.48;
- frame b*: -1.8 against +3.6;
- colourfulness: 28.8 against 24.7.

**Older vs newer.** Newer videos are more colourful (28.8 against 24.1) and have more frames with black areas.

### 1.5 Effects

| # | Rule | n/24 | Range | Frame refs |
|---|---|---|---|---|
| E1 | **A 4-point star glint sits on the object being named.** | ~20/24 | lives 3-12 f; grows about 2 f, shrinks about 2 f | 0m6G F113-F117 (keys, on "worse."); PL-Y F235-F246, F269-F278 (on each named ball) |
| E2 | **Motion blur on fast camera moves, and directional smear on whips.** | ~22/24 | 3-10 f | 7xS8 F54-F59; LC8h F169-F171 |
| E3 | **No screen shake.** Impacts use a hold, a flash or particles. | 22/24 (only 7xS8 rattle F880-F933 and lnYL recoil F1337-F1340) | — | VS1Z F1836-F1860 (even the earthquake has no shake) |
| E4 | **Particle bursts on impacts and reveals:** sparks, shards, coins, paper, money rain. | ~17/24 | burst 6-40 f; 15-100 pieces | 5WMQ F37-F59 (piggy shatter, about 30 shards); lnYL F200-F260 (splinter storm); 5WMQ F1857-F1895 (money rain) |
| E5 | **Outlined cartoon puffs** for smoke, dust and steam. | ~14/24 | rise and fade over 10-35 f | lnYL F38-F53 (muzzle puff becomes the wipe); uRkL F1180-F1220 (steam puffs alternate sides of the head) |
| E6 | **Rolling counters and gauges in the world.** | ~11/24 | 3-30 f roll | uRkL F1881-F1901 (99°F to 451°F, eased, turning red near 207°F); ZDy3 F726-F729 (0046 to 0047) |
| E7 | **Speed lines are rare and brief.** | ~6/24 | ≤ 20 f | 5WMQ F1666-F1669 |
| E8 | **Scan-line and X-ray reveals** for "inside" views. | ~6/24 | wipe 5-11 f | PL-Y F371-F382 (down) and F555-F566 (up); _sUA F374-F380 |

### 1.6 Sets

| # | Rule | n/24 | Range | Frame refs |
|---|---|---|---|---|
| S1 | **Real 3D or 2.5D sets with parallax.** | 21/24 (WbRd and eSRn are flat vector, DEe0 mixed) | similarity-fit failures (3D parallax) 0.7 / 5.1 / 19 % of frames | 7xS8 (canyon, trestle, Pullman car); VS1Z (throne hall) |
| S2 | **Characters are always inked; sets are inked in about half.** Newer videos ink more. | 24/24 characters; ~12/24 sets | 720p ink-on-edges 0.54-0.66 (8 refs); 240p 0.04 / 0.18 / 0.34 (older median 0.12, newer 0.25) | GM9U (inked painterly sets); 5WMQ, 7xS8, LC8h (uninked sets, inked characters) |
| S3 | **Three to five depth layers, often with a foreground element passing the lens during moves.** | ~20/24 layers; ~14/24 foreground passes | — | ZDy3 F133-F149, F245-F253 (statue plinth and lamppost wipe past); PLe2 F265-F285 (blurred vines) |
| S4 | **Lens blur on close and medium shots.** | ~20/24 | 720p soft edges 4-15 %; 240p 26 / 41 / 55 % | VS1Z F30-F59 (candle bokeh); hdhg F560-F617 (rack focus to the device) |
| S5 | **High prop density, and the props tell the story.** | 24/24 | — | VKsa (40 ticket packs, register, scanner); 0m6G (tape outline of the removed computer, cobweb TO DO tray) |
| S6 | **Background life is sparse but present:** birds, a flag, smoke, a tumbleweed, a taxi, a ticking counter. Crowds and clouds are static. | ~20/24 have some; 0/24 have moving crowds | 1-3 ambient movers per scene | WbRd F16-F28 and F190-F209 (taxi passes twice); LC8h F203-F245 (tumbleweed); 5WMQ F911-F945 (crow on the sign) |
| S7 | **Sets are reused, re-lit or revisited.** | ~15/24 | — | 0m6G (green room reused morning, day, evening and night); jpFJ (booth used 4 times) |
| S8 | **Insert sets for explanation:** cross-sections, diagrams, macros, maps, blueprints, X-ray or thermal views. | ~18/24 | 1-4 per video | GM9U F96-F299 (soil cross-section); PL-Y F716-F852 (sleep stages as water bands); hdhg F617-F710 (blueprint) |

### 1.7 Captions and graphics

| # | Rule | n/24 | Range | Frame refs |
|---|---|---|---|---|
| G1 | **One caption style:** white heavy rounded geometric sans (Montserrat or Poppins ExtraBold class), thin dark stroke, soft drop shadow, no box, no highlight colour, no emoji. | 24/24 | — | — |
| G2 | **Mixed case with punctuation kept** ("tree,", "arrested."). | 24/24 | — | — |
| G3 | **One to three words per page, one line.** | 24/24 (mostly 1-2) | page length 1 / ~10 / 35 f; function words 2-5 f; sentence-final words 15-30 f | 7xS8 F161 ("a", 1 f, flagged unreadable); VKsa F904-F938 ("congratulations.", 35 f) |
| G4 | **Fixed position:** centred horizontally at 68-77 % of frame height (median about 71 %). It never moves. | 24/24 | cap height 2.5-4 % of frame height | — |
| G5 | **Hard swaps on the word**, with no pop, scale or fade. | 24/24 | — | — |
| G6 | **Captions run from frame 0 or 1 to the last frame, with no gaps.** | 24/24 | — | — |
| G7 | **No title card, logo, end card or subscribe prompt.** | 24/24 | — | — |
| G8 | **Explanation graphics live in the world:** signs, labels on props, counters, stamped documents, phone UIs. | 24/24 | — | PLe2 F1101 ("IMPOSSIBLE" stamp); eSRn F1345-F1385 (fine print "100% fatal", circled in red) |
| G9 | **HUD-style overlays are allowed for "measurement" shots** (X-ray, thermal, satellite, labels). | ~6/24 | — | uRkL F456-F525 (satellite HUD), F1221-F1295 (X-ray HUD) |

**Tolerated flaw.** Captions sit over faces or key action in about 20/24 references, for example 0m6G F48-F63 and
GM9U F1206-F1233. Our panel counts this as a named flaw (principle 5), so we must not copy it.

### 1.8 Pacing

| # | Rule | n/24 | Range | Notes |
|---|---|---|---|---|
| P1 | **The visual change interval stays short.** | 23/24 ≤ 3.6 s (PL-Y 7.5 s is the outlier) | median shot length 1.67 / 2.45 / 7.47 s | Measured by frame_metrics, with camera travel counted as a change |
| P2 | **No long unbroken shot.** | 24/24 ≤ 15 s | longest 4.7 / 7.8 / 14.9 s | — |
| P3 | **The place or view changes often:** a new set, angle-set, insert, diagram or POV. | 24/24 | about 7.5 / 15 / 24 changes per minute; 5 / 9 / 17 distinct places per video | Counted from the shot lists (± 2). PARITY.md's "5-8/min" counts only major settings |
| P4 | **Nothing is frozen.** | 24/24 frozen count 0 | frames30 one-frame jumps 0 / 4 / 26 (older median 6, newer 3) | Jumps over 12 occur only in the generated-video era (WbRd, eSRn, uRkL, DEe0, LC8h) |
| P5 | **Narration is dense.** | 24/24 | 3.33 / 3.70 / 4.10 words/s; dead air 0 / 0.42 / 2.4 s; gaps ≥ 0.8 s 0 / 1 / 5 | — |
| P6 | **Runtime** | — | 31 / 58 / 78 s (top median 62; newer median 63, older 45) | — |

### 1.9 Micro-details

| # | Rule | n/24 | Frame refs |
|---|---|---|---|
| M1 | **Plant a prop, pay it off later.** | ~22/24 | ZDy3 F726 / F1770 (tally counter 0047 to 0048); DEe0 F0 / F1483 (coiled phone cord); jpFJ F1035 (wheelbarrow of gold set up before the ending) |
| M2 | **The visual beat lands on the exact caption word:** a face swap, a glint or a light event. | ~22/24 | PL-Y F80 (one-frame eye pop on "wake up"); CJwg F455-F457 (innocent eyes on "teasing") |
| M3 | **Signage gags are readable on pause.** | 24/24 | 0m6G (LABOR LAW padlock, HOPE switch); 5WMQ ("NOT RESPONSIBLE FOR ERRORS IN WEIGHTS AND JOCKEYS") |
| M4 | **Extras react on staggered frames, not in sync.** | ~8/24 | 0m6G F682-F699 (about 10 f apart); hdhg F913-F916; hdhg F1121-F1124 (blink, squint, wide eyes) |
| M5 | **The joke is in the background while the narration does something else.** | ~16/24 | eQR3 F340-F363 (guard spills coffee and never looks away); lnYL F310-F370 (pirate still stuck in the rigging) |
| M6 | **The video ends on the last word.** No button or end card; it often stops mid-move. | 24/24 | 7xS8 F1954 |
| M7 | **The last image mirrors the first (visual loop).** | ~7/24 | VKsa F1700-F1731 (orbit lands on the F0 composition); hdhg F1160-F1199 |

---

## 2. Where the rules vary

- **Generated-video era (mostly older and middle uploads).** DEe0, nzbk, uRkL, PL-Y, CJwg and parts of eSRn and WbRd
  show image-to-video tells:
  - morphing face in-betweens;
  - design drift between shots (hair colour, limb length);
  - blocky dissolves;
  - jump counts of 15-26.

  The newest uploads (LC8h, ZDy3, 5WMQ, Mz72, 7xS8, GM9U, t3OX) are clean rendered 3D with hard face swaps. **The
  current craft target is the newer group.**
- **Older against newer (medians).** Newer videos are:
  - longer: 63 against 45 s;
  - more dissolve-heavy: 19 against 12 transitions;
  - faster to change: visual interval 2.24 against 2.64 s;
  - faster on camera: 6.2 against 5.0 px/f;
  - sharper in their moves: attack 8.5 against 14.5 f;
  - more heavily inked: 240p ink 0.25 against 0.12;
  - more colourful: 29 against 24.
- **Top against bottom.** The camera and colour split the tiers. Cuts, transition counts and visual interval do not.
  - Top videos are faster: camera 7.8 against 5.8 px/f.
  - Top videos are darker and cooler: luma 0.39 against 0.48; shadow hue 295° against 238°.
  - Pacing is a floor, not a lever (LANE_PRINCIPLES S7 agrees).
- **Outliers.**
  - PL-Y (13.3M): 7.5 s median shot and only 6 transitions. It still reached the top tier on its topic (S1/S3).
  - _sUA: fastest camera (17.2 px/f, 13.4 moves per 10 s), yet bottom tier. Speed alone doesn't sell.
  - WbRd and eSRn: flat vector sets, middle and bottom tiers.
  - VKsa: the only static opening.
  - 7xS8 and lnYL: the only ones with screen shake.
- **Tolerated in the references, penalised for us.** All of these appear in the references, but our blind panel (v6)
  marks a named flaw as a fail:
  - muddy dissolves;
  - captions over faces;
  - long frozen bodies;
  - unexplained artefacts (0m6G's red line at F1659; mirrored shop lettering in t3OX).

  Copy the grammar and leave out the flaws.

---

## 3. Ranked gap list (ours against the rules)

**"Ours"** means three things:
- the 3D kit (`experiments/three-lane/src/kit/*`, as used by story-vasa v5-v10);
- the stick rig it draws onto cards (`person.tsx`);
- the last logged measurements (v6 2D and the v7 3D check, in docs/PARITY_LOG.md).

story-vasa's own measurements and panel are not in PARITY_LOG yet.

**Ranking.** Gaps are ranked by expected impact on the panel's same-tier verdict. v6 failed principles 3 (show what's
said), 5 (readable: named flaws) and 7 (craft: judges named the pipeline at once).

| Rank | Rule(s) | Ours now | Status | What to build | Panel principles moved |
|---|---|---|---|---|---|
| 1 | P3 places per minute, S8 insert sets | v6: one hall for 0-27 s (panel fail 3). v7: 10 shot groups in 59 s (about 10 place changes per minute). vasa v4+: one place or angle per sentence. Few inserts (map, newspaper) | **partly** | A beat planner that requires a new place, angle-set or insert at least every 4 s (about 15 per minute, at least 7 distinct places). Add a cheap **insert-set library**: cross-section, macro on a prop with bokeh, top-down map table, blueprint sheet, X-ray or thermal HUD view, POV iris. Each reuses the ink, blur and grade chain | **3** (the direct fail), 8 (diagrams make progress visible) |
| 2 | A3, A4, A12 acting on the word | Person has 11 faces, poses blend over 0.22 s, a sweat drop only on "worried", faces set per beat in the story file | **partly** | Grow the face set: ring eyes, >< squeeze, X, spiral, grid-teeth grimace, wink, ^^ bliss, dead-dot pupils, tears, blush, anger vein, steam puffs, head colour fill. Add **word-anchored face tracks**: a helper that swaps on a caption word with hard 1-frame changes and 1-4 f reaction runs. Make poses snap in 3-6 f, not 7 | **7** (craft), **3** (each line acted), 4 |
| 3 | T2, T4, T5, C9 transition grammar | Episode3D joins places with whip pans only, by design: v1/v4/v8 reviews flagged dissolve ghosting. No match dissolves, no fly-through-object, no frame-in-frame | **partly** | Keep the whips. Add three ghost-free kit transitions: (a) **match dissolve**, where a solved framing puts the anchor object in the same screen spot in both shots and only the background blends, over 5-8 f; (b) **push through an object** (window, eye, screen, photo), where the camera path ends inside a portal mesh that carries the next shot's render target; (c) **frame-in-frame**, where the shot shrinks into or grows out of a prop's texture. Aim for 1-4 match transitions per Short | 3, 4, **7** |
| 4 | E1, E4, E5, E6 effects vocabulary | fx.ts has flames, smoke, embers, outlined puffs and an ash heap. No glints, bursts, debris, rolling counters, scan lines or speed streaks | **partly** | Add an fx library on the NOINK layer: star glint (grows 2 f, shrinks 2 f), impact ring and spark burst, debris and paper or coin particles with gravity, dust kick, rolling counter or gauge texture, scan-line reveal, brief speed streaks. Each is a deterministic function of time, cued by caption words | **3** (show what's said), 7 |
| 5 | G1-G5 caption look | House captions in the display face, UPPERCASE, cream #fff2c0 with a teal 12 px stroke, two-line phrase pages, y moved per group to avoid subjects | **not** | A `ricks` caption style: white heavy rounded sans in mixed case with punctuation, thin dark stroke and soft shadow, one line of 1-3 words, a fixed y near 0.71, hard swaps. Keep the subject-avoid logic as a **reframing** rule (the camera solver keeps faces out of the 0.64-0.78 band) rather than moving the caption. Keep the v6 no-mid-phrase page rule inside the 1-3 word limit. **Owner decision:** FEEDBACK.md principle 5 asks for whole-phrase captions; the references use 1-3 word pages | **7** (blindness: judges spotted the pipeline), 5 |
| 6 | L2-L4, T8 story light | Presets (day, golden, night, fire, explain, underwater, museum) chosen per group. `light(t)` switches presets discretely, so a mid-shot change pops | **partly** | **Tweened preset blend** (interpolate lit, shade, key, fog and grade over 6-40 f) for in-shot relights. Add **keyword light events**: flicker-on (3 f), alarm wash, glow ramp and flash, cued by caption words. Story rule: at least 2 light states per Short, with the explanation in night-blue when the story allows | 2, 3, 7 |
| 7 | L6-L8 grade inside range | v7 measured luma 0.29, non-ink p5 0.045, colourfulness 22 (all just low or crushed). The presets were lifted afterwards (comment in presets.ts) but no re-measure is logged | **partly** | Re-measure the latest vasa render with look_stats. Add a per-preset black floor test in CI (render one still per preset and check non-ink p5 ≥ 0.09). Allow warm shadows (10/24 references have them), but keep shadow chroma ≤ 35 | 7 |
| 8 | S3, S6 depth and background life | Sets are modelled with props, fog, lens blur and ink. No ambient movers and no planned foreground occluders | **not** | Ambient rigs: birds crossing, a flag or banner flutter, chimney smoke, foliage sway, a ticking counter, a passing vehicle. Aim for 1-3 per exterior. A framing helper that places one foreground prop near the lens on dolly moves (passes through in 6-20 f) | 2, 7 |
| 9 | A11 prop overlap | No generic prop physics; per-episode rigs only | **not** | Small helpers: hat pop (rises half a head, tumbles 10-25 f), pendulum swing with settle (tags, keys, lanterns), spring bounce. Trigger them from the story file | 4, 7 |
| 10 | C8, C10 motivated camera paths | CamPath glides between solved framings (0.9 s sine), holds push 25 % and orbit 9° | **partly** | A `follow(object)` camera key that tracks a thrown or falling prop for 10-60 f, and an optional roll on wide or dramatic keys (5-15°) | 3, 7 |
| 11 | A5 blinks, A8 flaps, A10 walk timing | Blink every 3.2-4.8 s, closed for 0.12 s (3.6 f). Talk flaps between 2 shapes at about 3.6 f. Walk step about 10.5 f. A constant breathing bob | **mostly done** | Blink closed for 2 f, at irregular intervals of 2-8 s. Use 3-4 mouth shapes. Walk step 6-8 f. Leave the breathing bob: it is not in the references but it isn't a flaw | 4 |
| 12 | C1-C6 camera speed and grammar, T1 cuts, P5 pace | v7: moving 99 %, median 11.4 px/f, 8.3 moves per 10 s, quiet zoom 70 %, 3 cuts. Narration 3.79 wps with no gaps | **done** (quiet zoom at the edge of range) | Raise the hold push so quiet-frame zoom sits near 80 % | — |
| 13 | G6-G8, M6, C7 opening and ending | Frame 0 is the cover with the first caption; no end card; in-world tags | **done** | — | — |

**Build order** (by impact for effort):
1. Rank 5: captions. Cheap, and it removes the instant tell.
2. Rank 2: faces on the word.
3. Rank 4: fx library.
4. Rank 1: insert sets and the beat planner.
5. Rank 3: the transitions.
6. Ranks 6-10.

Ranks 1 and 3 have the biggest effect but cost the most.

---

## 4. New measurable checks for the story lane

Add these to the parity checks (run_one.sh and parity_table.py), next to the existing ones in PARITY_LOG. Ranges
come from the 24 references. If a check is measured at 240p, ours must be downscaled to 240x426 before comparing.

| Check | How to measure | Reference range (min / median / max) | Ours now |
|---|---|---|---|
| `place_changes_per_min` | Count shot-group or insert changes in the story file (ours). For refs, count from the shot lists. Later, automate with colour-histogram scene clustering on frames30 | 7.5 / 15 / 24 per min; distinct places 5 / 9 / 17 | v7: 10 place groups in 59 s (about 10/min) plus angle changes inside the hall; v6 failed panel principle 3 |
| `shot_len_median_s`, `shot_len_max_s` | frame_metrics shot_len, with transitions counted as changes | median 1.67 / 2.45 / 3.6 (one at 7.5); max 4.7 / 7.8 / 14.9 | not logged; add |
| `transitions_per_min` | frame_metrics n_transitions / duration | 9.2 / 18 / 24.8 | not logged; add |
| `first_transition_s` | First dissolve, cut or whip from frame_metrics plus the story file | 0.7 / 3.4 / 12.4 s | add |
| `match_transitions` | Count of joins where an anchor object's screen box overlaps by IoU ≥ 0.5 across the join (from story-file projections) | ≥ 1 in about 17/24; 1-4 per video | 0 (whips only) |
| `move_attack_f`, `move_release_f`, `snap_moves` | camera_motion moves list (already computed, not yet in the table) | attack 4.5 / 11.8 / 20.5; release 4.5 / 10.8 / 34; snaps 0 / 5 / 14 (newer median 7) | add |
| `face_swaps_per_10s` (lead character) | Count face-value changes in the story file's face tracks | Estimate from the study: 3-10 per 10 s on the speaking lead (reaction runs excluded). **Measure on 4 references first** by marking the lead's face changes on frames30 sheets | add |
| `blink_closed_f`, `blink_interval_s` | Person rig parameters and story overrides | closed 1 / 2 / 4 f; interval about 2-10 s, irregular | 3.6 f; 3.2-4.8 s regular |
| `glints_per_short`, `fx_events_per_min` | Count cued fx events (glint, burst, puff, counter, light event) in the story file | glints ≥ 1 in 20/24; fx events: **estimate** 3-10 per minute, measure on 4 references | about 0-2 |
| `light_states`, `inshot_relights` | Count distinct presets used, and tweened preset blends of 6-40 f | light states 2-5 in 20/24; ≥ 1 in-shot relight in about 12/24 | presets yes; tweened relights 0 |
| `explain_frame_b_drop` | look_stats before/after the late "You see" (existing split) | where used, drop of 17-53 in b* (4 of 10); optional | — |
| `caption_words_per_page`, `caption_y_spread`, `caption_case` | From captions.json pages: words per page share ≤ 3, std of page y, upper or mixed case | ≥ 95 % of pages ≤ 3 words; y spread 0 (fixed at 0.68-0.77); mixed case | 2-line phrase pages; y moves; uppercase |
| `caption_on_face_frames` | Project the face boxes from the story file and intersect them with the caption band | 0 for us (the refs fail this, but the panel penalises it) | the avoid logic exists; add as a gate |
| `hold_frac` | camera_motion hold (dead-still share) | 0 / 0.3 / 4.7 % | not logged; add (v7 moving 99.1 %) |
| `ambient_movers_per_exterior` | Count of ambient rigs per exterior shot group in the story file | 1-3 in about 20/24 | 0 |
| `jump_flags_per_min` | frames30 jump count / duration | newer refs 0-11 per video (median 3); generated-era up to 26 | v7: 6 |
| `black_floor` (every preset) | look_stats non-ink p5 on one still per preset | ≥ 0.09 at 720p (refs 0.09-0.23); 240p 0.04-0.27 | v7 0.045 (presets since lifted, not re-measured) |

**Reference measurements still to take** (to firm up the estimated rows):
- face swaps per 10 s and fx events per minute on 4 newer references (LC8h, ZDy3, Mz72, 7xS8), marked by hand on
  frames30 sheets;
- dissolve count and length on all 24 with the blend detector from STORY_LANE_TUTORIAL_CHECK;
- 720p copies of the 16 newer-measured videos, so that ink, soft-edge and acutance ranges cover all 24 at our working
  resolution.
