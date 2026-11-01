# TIS AK-12 remake: learnings (internal benchmark, never published)

This benchmark is a shot-for-shot code remake of The Infographics Show Short "Why the Russian Military Switched to the AK-12" (56 s, 1080x1920). We built it to measure our graphics gap and close it. The reference audio was used for timing only.

- Build notes: `REMAKE_NOTES.md`. Shot spec: `SHOTLIST.md`. Style measurements: `STYLE_NOTES.md`.
- Renders (git-ignored): `out/remake_v{1,2,3}.mp4`, `out/side_by_side_v{1,2,3}.mp4`, `out/pairs_v*_sheet.jpg`.

## 1. Score history

| version | judge score /100 | same tier as TIS? | what changed |
|---|---|---|---|
| v1 | **71** | no | first full remake: 26 framings, 9 transitions, puppet rig, lip-sync |
| v2 | **68** | no | grey-ramp rifles with LOD micro-detail, re-blocked shots, bulkier characters, more props |
| v3 | **71** | no | rounded head kit and hair, varied acting, grip wraps, layered burst, S19 rebuild, caption type, scale gags |

**Reading.** Three rounds plateaued at 71. v2's broad "add detail" pass *lost* 3 points, and v3 only won them back. The judge's remaining gaps are not about detail density. They are about:

1. **Wrong hero silhouettes.** The AK-12 asset reads as an AR/picatinny hybrid, and that one asset costs points in S01, S05, S06, S11 and S13.
2. **Timing and camera fidelity.** Moves land early or late, and pushes overshoot.
3. **Over-rendering.** Fingers, gradients and rails were added where TIS uses flat circles and clean shapes.

Adding detail moved the remake *away* from the reference.

## 2. Last judge (v3): per-shot gaps

The last judge scored v3 at 71. The workflow handoff that delivered the judge JSON was cut off partway through S15, so the per-shot list below stops at S14. S15–S26 and the judge's own `code_vs_art` split did not arrive. The **class** column is my reading of each gap, not the judge's:

- **code**: fixable by changing keyframes, timing or framing.
- **art**: needs a better-drawn asset.

| shot | score | judge gap (condensed) | class |
|---|---|---|---|
| S01 hook 0–2.9 | 60 | The AK-12 hero is the wrong silhouette: a bulky skeletal stock, an oversized magazine and a fat GL tube, where the ref has a slim, recognisable AK-12 with a folding stock and gold accents. Our pills settle by 0.5 s, while the ref's pills are still sliding at 0.5 (pill 1) and 1.0 (pill 2). This is the first frame of the video, so it costs the most. | art (gun) + code (pill timing) |
| S02 MCU A at door 2.9–4.5 | 78 | Close match. Our hands have fingers and thumbs, where the ref uses flat skin circles. The ref holds the AK-47 more upright and higher, and its beard and hair silhouette is sharper. | art (hands, hair) + code (gun pose) |
| S03 pull-out 4.5–5.6 | 70 | The pull-out is already wide by 5.0 s, while the ref is still mid-zoom with a strong dutch angle. Our move is early and rotates less. | code |
| S04 wide two-shot 5.6–8.1 | 75 | Our characters are about 15 % too big, which crowds the set. The ref's camo and plate-carrier detail is finer. Layout, flags and tower match. | code (scale) + art (camo, carrier) |
| S05 push to chest + calendar 8.1–9.0 | 70 | The rifle that swings up is the skeletal-stock AR hybrid, not an AK-12. The push, the rotate and the calendar are fine. | art (gun) |
| S06 CU AK-12 + sparkles 9.0–11.3 | 66 | Our receiver CU shows a picatinny-monster gun gripped by a fingered hand with a gradient. The ref is a clean AK-12 receiver under flat circle hands. The sparkles are good. | art (gun, hands) |
| S07 clipboard checklist 11.3–14.0 | 77 | B's face is too wide, with bulging green eyes and no visible hair or nose shading. The checks land about 0.3 s early. The clipboard is nearly identical. | art (face) + code (check timing) |
| S08 kneeling C firing 14.25–16.0 | 73 | Our muzzle flash is a filled orange star, where the ref uses a thin, spiky starburst. C and the rifle silhouette are off-model, but the pose and set match. | art (flash, gun) |
| S09–S10 truck to target 16.0–18.2 | 73 | The truck move skips the ref's wooden-tower beat, so the target is already in frame at 16.5. The target itself is good. | code |
| S11 D beside target 18.2–19.6 | 70 | D carries a scoped AR-style rifle, not an AK-12. D reads small and stiff next to the ref's relaxed carry. | art (gun) + code (pose) |
| S12 push to D, heart eyes 19.6–21.95 | 58 | The push overshoots (about 3.5x, against the ref's 2x with a dutch angle) and crops the chin, with the gun across the face. The hug and heart-eyes pose lands late: we are still wide at 20.0, when the ref already shows the hug. | code |
| S13 official at desk 22.0–26.0 | 76 | One of the closest shots. Our face is less caricatured than the ref's, which has a stronger brow, a hair shape and nose shading. The rifle uses the wrong silhouette again. | art (face, gun) |
| S14 squad line 26.0–28.0 | 68 | The framing is too tight, with heads and boots near the edges. The ref keeps air around a synchronised march. The iris transition is good. | code |
| S15–S26 | n/a | Truncated in the handoff. Open items carried over from v3's own notes: F is in profile, not 3/4 (S17); S24/S25 crate perspective; the S26 M4 size. | — |

**Split across S01–S14** (my classification):

- **Code-only gaps: S03, S09, S12, S14.** They average 67/100 and include the lowest judged shot (S12, 58). Each one is keyframe work, not drawing.
- **Art gaps:** dominated by **one asset, the AK-12**, which appears in 6 of the 14 judged shots. The rest are hands, faces, the flash and camo.

The fastest path to a higher score is the AK-12 redraw plus the four timing fixes.

## 3. What this benchmark proved worth porting into OUR pipeline

These items were built in `remotion/src/` and held up across the judge rounds. They are recommendations only: `studio/src/` and `pipeline/` were not touched (other work is running there).

**Copying rule (BRIEF rule 5).** Port the *mechanisms*. The TIS cast, the rifles as designed and the sets stay in this experiment. Any colours must be remapped to the house ramps in `experiments/kurz-style/STYLE_BIBLE.md` ("Lantern & Ink" bans greys, so the gun grey ramp becomes an ink/bone ramp).

### 3.1 Components

| port | from | why it earned its place |
|---|---|---|
| **Character puppet rig** (`Soldier`, `Head`, `Look`, `Pose`, `ik()`) | `art/soldier.tsx` | This is the missing asset class flagged in `STYLE_NOTES.md` §1.2, and it was the biggest single upgrade. It has 2-bone IK arms and legs, stand/kneel/march, a rounded squircle `FACE`, `hairStyle` crop/side/swoop, beard variants, brows/mouth/eye sets (hearts, blink, sweat) and props parented to hand anchors. One rig made 10 distinct characters. Port it as a generic `people` rig for the explainer kit, with `Look` presets in our palette. |
| **Lip-sync and blinks from word timings** (`wordAt`, `talkMouth`, `blinking`) | `lib/anim.ts` | It is driven directly by the whisper word JSON we already produce, so every on-screen speaker talks for free. |
| **Anchor-point props** (`ANCH`, `gunPt`) | `art/guns.tsx` | Named grip/fore/muzzle points let hands, muzzle flashes and recoil attach to any held prop. Generalise this to "held prop with anchors". |
| **LOD by camera distance** (`lod` 0/1/2) | `art/guns.tsx` | It scales micro-detail with zoom, so close-ups get detail and wides stay clean. Keep the mechanism, but cap it (see §4: detail must not change the silhouette). |
| **Micro-FX** (`Sparkle` + `SPARK_PATH`, `MuzzleFlash`, `Burst`, `Explosion`) | `art/props.tsx` | These are cheap, reusable "new/shiny", impact and cover beats. The judge praised the sparkles in S06, and `Burst` is the layered version (petals, fire cloud, core, smoke, debris). |
| **Screen-pinned UI widgets** (`Calendar` with type-on, `Clipboard` with check pops) | `art/props.tsx` | Both live in a layer above the world camera and keep a fact on screen across framings. This is the TIS form of our progress device (FEEDBACK B6). |
| **Set-dressing kit** (`CloudBand`, `PoleFlag`, `Streaks`/`streakSet`, `Hedgehog`, `Wire`, `Crate`, `Quonset`, `LatticeTower`, `Target`) | `art/props.tsx` | It covers full-bleed sets with 4–6 depth layers (`STYLE_NOTES.md` §1.1). Port the generic ones: clouds, streak texture, flags, crates, wire, towers. |
| **Upright-clamped badges** (`Flag`, ±24° clamp in its own upright space) | `art/soldier.tsx` | This fixed upside-down patches on rotated limbs. Use it for any emblem on a rotating part. |

### 3.2 Shading recipe (the TIS construction, confirmed by the judge as "close match" where we followed it)

1. Flat fills, no outlines, no gradients on characters or hands. In v2/v3 the judge penalised the hand gradient and fingers in S06.
2. One darker **shadow-side shape** per head and part.
3. One lighter **top-edge strip** on hard objects (guns, beams, hedgehogs, crates).
4. A **rim light** on the lit cheek, and a **soft contact shadow** under feet and props (`CastShadow`).
5. Hard surfaces get a **5-step value ramp** (`G.g0`–`g4`) in place of near-black: furniture, body, lit planes, specular edge. Remap it to house tokens.
6. Camo and texture come from **many small low-contrast capsules** clipped to the part (`Cap`, the camo patterns in `defs.tsx`), not from noise filters.
7. Shape budget: a rifle is about 25–40 shapes, a figure about 80–120 and a facade 150+. Density comes from small flat shapes, not from lighting.

### 3.3 Motion presets

- **Camera as `{x, y, s, r}`** with `look(worldPt, screenPt, scale, rot)`, log-scale zoom interpolation (`camLerp`) and keyed moves (`camAt`). Every move carries a ±5–20° dutch rotation. Our `studio/src/core/camera.ts` already has `zoom`/`rotate`. Port `look()` (frame a world point) and the log-scale zoom, which removes the "fast start, crawl end" feel of linear zooms.
- **Hold-drift then fast move.** Hold a framing with a slow 3–8 % push, then make an eased 0.4–1.2 s move (`inOutCubic`/`inOutQuint`). This is the grammar behind TIS's motion energy of 4.96 against our orca pilot's 1.76 (`STYLE_NOTES.md`), and it keeps frames from freezing (FEEDBACK A4).
- **Parallax per layer** (`para(cam, factor, ax, ay)`).
- **Overshoot gestures.** `outBack` with c1 = 1.9 for points, raises, pop-ins and check marks. It was added in v2 and kept.
- **Secondary motion defaults.** Flags wave, clouds drift, flashes flicker every 2–3 frames, guns recoil, figures breathe and blink.
- **Overscan plates.** The sky plate runs from y -3000 to 6000, because any pushed or rotated camera will otherwise expose the empty canvas (this caused the v2 S12 black void). Make overscan a kit default.

### 3.4 Text styles

- **Hook title pills.** Staggered slide-ins that are still moving at 0.5 s and 1.0 s, with no caption box during the hook. Lesson from the S01 gap: pills that *settle* too early read as static.
- **TIS caption page** (K2D Medium, 78 px, 1.6 px same-colour stroke, -1.2 px tracking, a 70 % black box at least 928 px wide with 52 px side padding). Keep it as an *optional* caption skin only. For the channel, our whole-phrase pages stay the rule (FEEDBACK B8).

### 3.5 Transitions (`Matte` / `Overlay` in `Main.tsx`)

- **Silhouette matte**: the incoming subject's own body, rendered as an alpha mask, flies in and scales over the frame.
- **Slash wipe**: 18 tapered streaks at -30° with staggered delays, with the outgoing frame smeared along the streak.
- **Iris**: a plain circle with no glossy rim (the rim strokes were removed in v3, and the judge called the iris "good").
- **Organic blob/splatter** (`blobPath`): noise-modulated lobes, with debris and tendrils from `Overlay`.
- **FX cover cut**: an explosion fills the frame and the camera jumps underneath it.
- **Placement rule**: every transition lands within ±0.1 s of the next sentence's first word, using the word timings.

Our `core/transitions.tsx` has only displacement-style looks. Port these five as content-shaped matte types.

### 3.6 Tooling

- `tools/pairs.sh <ver> <out.jpg> <cols> <times...>` builds ref|remake pairs at any times, and `tools/stills.sh` renders a contact sheet of arbitrary frames. Both are cheap, and both were essential for judge rounds.
- A full 56 s render takes 35–40 s on the Spark CPU (`--concurrency=4`, `nice -n 10`). Iteration is cheap, so judge rounds can be frequent.

## 4. What still needs better art (code cannot fix these)

1. **The hero rifle silhouette** (S01, S05, S06, S08, S11, S13). It needs a slim AK-12: a folding stock, the correct magazine curve, gold accents, no GL tube and no picatinny clutter. Draw it silhouette-first and check it as a solid black fill against the reference *before* adding any detail. This is the top item.
2. **Hands.** Go back to flat skin circles in close-ups (S02, S06). The v3 grip-wrap fingers and the gradient were judged worse. If grip readability needs it, keep at most a thumb lobe.
3. **Faces.** These need more caricature: a stronger brow shape, nose shading, a sharper hair and beard silhouette (S02, S07, S13), and narrower faces with less bulging eyes (B in S07).
4. **Uniform detail.** Finer camo and plate-carrier pouches and straps (S04).
5. **Muzzle flash.** A thin, spiky line starburst in place of the filled star (S08).
6. **Still open from v3:** F in 3/4 view (S17), crate perspective (S24/S25) and a simple prone pose (S19).

**Process rule for future art.** Judge the *silhouette* first and the *shading* second. Each added detail must leave the solid-fill silhouette unchanged. v2 broke this rule and lost 3 points.

## 5. Next round, if this benchmark continues

1. Code fixes (cheap, and they include the lowest judged shot):
   - S12: push to 2x with a dutch angle, and land the hug by 20.0.
   - S03: delay the pull-out and add rotation.
   - S09: add the tower beat before the target enters.
   - S14: widen the framing.
   - S01: re-time the pills.
   - S07: move the checks 0.3 s later.
   - S04: scale the characters down by 15 %.
2. A silhouette-first AK-12 redraw, used everywhere.
3. Flat-circle hands in close-ups, a spiky flash, and face caricature.
4. Re-run the judge and get the **full** per-shot JSON and `code_vs_art` for S15–S26 saved to a file (for example, `out/judge_v4.json`), so that truncated handoffs cannot lose it again.
