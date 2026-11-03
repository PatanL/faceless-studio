# src/next pieces: integrated into the kit

**Status (2026-11-02):** integrated into `src/kit/` (commit b87637b and later). Every module named below now lives in
`src/kit/<name>` (`src/next/` keeps only the KitLab / DressLab reels and the measuring tools), and the "kit change once
free" items are done:

| Item | Where it landed |
|---|---|
| The Actor | Stage draws `people` as the Actor (`classic: true` on a PersonSpec keeps the old stick/Person) |
| Per-group lens | `GroupSpec.lens` (`{ cInf, maxCoC }`); the kit default goes from cInf 10 to 12 (`Stage.LENS`) |
| Light preset objects | `GroupSpec.light` takes a name, a Preset object, or a function returning either |
| Joins | in `Episode3D` (`GroupSpec.join`): match, push, into, outOf; the whip is kept |
| Whip ghosting | the whip's overlap frames now wipe the incoming shot in behind a hard edge instead of fading it in |
| Reference captions | `Episode3D captions="ricks"`, **still opt-in**; the house style stays the default |
| Kit life | clouds drift round any sky dome (the dome and the clouds now follow the camera inside the far plane); wave detail scrolls over a set's `extra.water`; a group opts out with `clouds: false` / `waves: false` |
| Label size | world labels (`tagSprite`) are kept at least 64 px tall on screen |

**Gates** (`kit/gates.ts`) run in `Episode3D` and fail the render unless the episode passes `gates="warn"`. Vasa3D and
Turk3D pass "warn": they were finished before the gates existed. The same gates run in `scripts/framing.ts`, which
exits 1 on a failure.

| Gate | Fails when | Escape hatch |
|---|---|---|
| hold | any view is held for more than 4 s | — |
| cast | a group's figures are specks (median head < 0.05 of the frame height); or fewer than 25 % of the frames with figures have a head ≥ 0.07 | mark the group `establishing` or `insert` |
| edge | a head is cut, a body crosses the left or right edge, or a `keepInFrame` box is cut, for 8 or more frames outside a join | — (bottom crops and face close-ups are allowed) |
| hud | a progress readout goes backwards, or a gauge reverses by more than its tolerance outside the story's `allowBack` windows | wrap readouts in `kit/hud.ts` `progress` / `steadyGauge` |

The sections below are the original wiring notes. Paths in them read `src/kit/` now.

Render KitLab (Mac slot, one render at a time):

```bash
cd experiments/three-lane
npx remotion render src/next/index.ts KitLab out/kitlab/kitlab.mp4 --gl=angle --concurrency=2 --chrome-mode=chrome-for-testing
python3 scripts/repair_frames.py out/kitlab/kitlab.mp4 out/kitlab/kitlab_r.mp4 --bundle <bundle> --props props.json --comp KitLab --gl angle
# DressLab (bare/dressed A/B): props {"bare": true|false}
# plan / acting / caption / join checks without rendering:
node_modules/.bin/esbuild src/next/tools/plan_kitlab.ts --bundle --platform=node --outfile=/tmp/plan.cjs --loader:.woff=empty --loader:.woff2=empty --loader:.css=empty && node /tmp/plan.cjs > plan.json
# ghost check of every join in a render (windows come from the plan output):
python3 -I src/next/tools/ghost_check.py ffmpeg out/kitlab/kitlab.mp4 plan.json ghost.json --control
```

Rule-book references are to `research/library/RICKSCLIPS_RULEBOOK.md` (gap table, section 3; checks, section 4).

Order below = the work order: cutaways (1), then the coordinator's two additions (1b detail density, 1c character
framing), then acting, transitions, effects, captions, light.

---

## 1. Cutaway sets and the 4-second planner (gap 1: P3, S8)

| File | What |
|---|---|
| `cutaways.ts` | `crossSectionSet`, `macroSet`, `mapSet` + `routeRig`, `blueprintSet` + `drawOnRig`, `xraySet` + `xrayPanel` |
| `pov.tsx` | `PovMask` overlay (spyglass, keyhole, binoculars; iris in/out 3-10 f) and `povKey` |
| `planner.ts` | `viewChanges`, `planReport`, `planText`: every place / view change, holds, flags > 4 s, split suggestions on caption words |

Use in a story file (no kit change):

```ts
import { crossSectionSet, routeRig, mapSet } from "../next/cutaways";
groups.push({ id: "soil", t0, t1, xfade: 0.4, light: "day", set: () => crossSectionSet({ cavity: { x: 0, y: -0.2, w: 1.1, h: 2.4 }, frame: true }),
  cam: [...], people: [], rigs: [/* put things in ctx.set.extra.cavity */] });
groups.push({ id: "route", ..., set: () => mapSet({ places, route }), rigs: [routeRig(t0 + 0.1, t1 - 0.2, [t0, t1 - 0.2])] });
```

- Every set is a normal `SetBuild`, so the ink pass, lens blur, grade and presets apply unchanged.
- `macroSet` paints its bokeh into the back wall. The kit's lens blur is fixed at `cInf = 10` in Stage, which is too
  weak for a real macro.
- POV: add `<PovMask t0 t1 kind="spyglass" enter="open" exit="open" />` to the episode overlays for the POV group's
  range, and use `povKey(t, feet, look)` for the camera.
- Planner: call `planReport(story.groups, words)` at the end of `buildStory` and `console.warn(planText(report))`, or
  run it in node (see `tools/plan_kitlab.ts`).
  - Optional fields on a group: `place` (the same string for revisits of a set) and `insert: true` (cutaways).
    The report then counts places and inserts properly.
  - A flagged hold lists the word starts where a cutaway or a new angle can go.

**Kit change once free:**
- In `Stage.tsx`, read a per-group lens strength: `fx.lens.cInf = g.lens ?? 10`. Macro shots want 18-24.
- In `Episode3D`, call `planReport` and fail the build (or warn) when `flagged.length > 0`.

## 1b. Set detail density and prop dressing (coordinator item, after the v14 panel)

**What was measured.** `tools/look_density.py` reads frames30 sheets at 240p, with the caption band masked.

| Set | Edge density | Flat 6x6 blocks | Texture energy |
|---|---|---|---|
| 24 refs (median) | 0.092 | 0.40 | — |
| Vasa v14 | 0.073 | 0.48 | below the ref median |

Our sets are flatter: bare colour, empty water and sky. The numbers are in `docs/RND_LOG.md`.

| File | What |
|---|---|
| `dressing.ts` | Textures: `grainPlanks` (grain, knots, gaps, nails, a lit gradient), `stoneCourses` (mortar, lit edges, moss), `richWater` (strokes, troughs, foam) |
| | Props: `crate`, `barrel`, `ropeCoil`, `sack`, `bucket`, `net`, `bollard`, `lanternPost` |
| | `dress(root, { area, n, kit, keep })`: a deterministic scatter that keeps out of actor spots and camera paths |
| | `clouds(root, {...})`: inked painted cloud cards |

Use today, inside any set function or a rig:

```ts
const s = harbourSet(); dress(s.root, { area: [x0, z0, x1, z1], y: 1.8, n: 12, kit: ["crate", "barrel", "ropeCoil", "sack"], keep: [actorBoxes] });
clouds(s.root, { n: 9, x: [-90, 90], y: [30, 70], z: [-240, -160], size: 60 });
// swap a flat material: lambert({ map: grainPlanks([6, 1], { hue: 28, light: 44 }) }) / richWater([60, 60])
```

**Measured effect** (DressLab A/B: the same 4 sets and cameras, bare against dressed):
- edge density 0.045 → 0.074;
- flat share 0.72 → 0.55.

The deck and the gear room reach the refs' median. Rooms and night seas need more props than KitLab gives them.

**Kit change once free:** give `paint2.ts`'s flat painters (`darkBoards`, `paving`, `stoneWall`) the plank-gap and
lit-gradient treatment of `grainPlanks` / `stoneCourses`, or replace them with these.

## 1c. Character framing: cast-size presets and check (coordinator item)

**What was measured.** Head height ÷ frame height, with the lead character on screen.

| | Median head size | Frames with head ≥ 0.07 | How measured |
|---|---|---|---|
| 24 refs | 0.08 (per-video medians 0.035-0.25) | 47 % | marked by hand, 120 gridded samples |
| Vasa v14 | 0.028 | 29 % | projected from its story file by `tools/cast_check.ts` |

- In Vasa v14, 8 of 14 groups are flagged as specks: test, guns, wobble, launch, gusts, sinking, ballast and warning.
- The hand-marked Vasa samples agree with the projection: 0.015.

| File | What |
|---|---|
| `castframe.ts` | `castKey(t, feet[], "close" \| "medium" \| "wide", az, el, fov, scale, extraBoxes)`: solves the framing, then dollies until the biggest head hits 0.20 / 0.11 / 0.06 of the frame height, keeping heads above the caption band |
| | `headFrac(g, t, feet)` |
| | `castCheck(groups, castOf)`: per-group median head size and share ≥ 0.07; flags groups under 0.05 |
| `tools/cast_check.ts` | runs the check on Vasa (`node cast.cjs vasa ../../episodes/story-vasa/storyboard.json`) or KitLab |

Use today in a story file: `cam: [castKey(t0, [A, B], "medium", 15, 6, 36), ...]`.
- Inside a room, wrap the call in `setRoom(box)` / `setRoom(null)`, as `fit` is.
- The rule to aim for: about half of all frames with a head ≥ 0.07, and wide shots (head < 0.05) only for establishing
  shots and inserts.

**Kit change once free:** call `castCheck(story.groups, peopleCast)` in `Episode3D` next to `planReport`, and warn on
`flagged`.

## 2. Acting tied to words (gap 2: A2-A12, M2, M4)

| File | What |
|---|---|
| `actor.tsx` | `Actor`, a drop-in twin of stick/Person (same 600x700 box, costumes, poses, items, prop names), with the acting rules built in |
| `acting.ts` | `faceTrack` (hard swaps on caption words, optional 1-4 f reaction runs), `poseTrack`, `markAt`, `fillAt`, `wordT`, `checkFaceTrack` |
| `actorCard.tsx` | `actorCard` (a drop-in for Stage's `personCard`) and `actorRig` (an Actor as a rig: usable now) |

**What the Actor changes against Person:**
- **No idle breathing.** The body is frozen between poses; only a walk bobs it.
- **No lip-sync.** `talk` / `quote` windows get loose flaps from 4 shapes, a new shape every 3 f.
- **Blinks.** Irregular, 2-8 s apart, closed 2 f (`blinkF` 1-4, `blinkHalf` adds half-lid frames, or set `blinks: [t…]` by hand).
- **Pose snaps** take `snapF` frames (default 4) with a small overshoot.
- **Prop follow-through:**
  - dangling `key`, `tag` and `lantern` swing and settle after each snap;
  - the `hammer` follows through;
  - `hatPop: [t]` throws the hat up and lands it, tumbling.
- **27 whole-face drawings.** Person's 11 keep their names. The 16 new ones are:
  terrified, stunned, scream, grimace, squeeze, cackle, dizzy, dead, wink, bliss, deadpan, sly, blank, sob, furious,
  puzzled.
- **Emotion marks** pop on with no fade:
  - `marks`: sweat, tears, steam, vein, blush;
  - `fill`: the head fills with a colour, rising over `rise` s on 1s.
- **New poses:** strikeUp, strike, cheeks, facepalm.
- **New costumes:** keeper, apprentice.
- **New items:** tag, lantern, hammer, photo.

Usage today (no kit change), as a rig:

```ts
import { actorRig } from "../next/actorCard";
import { faceTrack, poseTrack, markAt, fillAt } from "../next/acting";
const words = T.words;                       // the Kokoro word timings (global seconds)
const faces = faceTrack(words, "worried", [{ word: "stopped.", face: "stunned" },
  { word: "terrified.", face: "terrified", react: [{ face: "blank", frames: 2 }] }], t0);
rigs: [actorRig({ id: "ada", at: () => A, faceTo: () => B, props: () => ({ costume: "admiral", seed: 5, face: faces,
  pose: poseTrack(words, "stand", [["stopped.", "shrug"]], t0), marks: [markAt(words, "stopped.", "sweat")],
  fill: [fillAt(words, "terrified.", "#8a63d2")] }) })]
```

- `faceTrack` searches all words. Use `after` (seconds) to pick an occurrence after a time.
- `Timing.w(scene, word)` stays the scene-scoped lookup.
- Staggered extras (M4): give each extra the same cue with `lead: -8`, `-15` (frames late).

**Kit change once free** (one line, which makes every `people` entry an Actor). In `Stage.tsx`, inside `world`'s
`useMemo`, replace

```ts
const rec = personCard(...)
```

with

```ts
const rec = (p as { actor?: boolean }).actor ? actorCard(...) : personCard(...)
```

using the same two arguments, and import `actorCard` from `../next/actorCard`. Then a story sets `actor: true` on a
PersonSpec.
- Caption avoidance (`captionCues`) keeps working, because people stay in `g.people`.
- Actor cards are 820 svg units tall against Person's 740 (headroom for hat pops). Their feet stay on the card's
  bottom edge, so placement is unchanged.

## 3. Transitions that don't ghost (gap 3: T2, T4, T5, C9)

| File | What |
|---|---|
| `EpisodeNext.tsx` | `EpisodeNext`, Episode3D with a per-group `join`; `layersOf` (frame ranges + styles, testable in node) |
| `match.ts` | `camAt`, `project`, `boxRect`, `matchKey` (frame an anchor at a screen spot and size), `quadPortal`, `circlePortal`, `quadAt`, `homography` |

Joins (`NextGroup.join`; the default comes from `xfade`, as in Episode3D):

| kind | What it does | Ghost-free because |
|---|---|---|
| `whip` | the kit's whip, ported with the same numbers | unchanged: the two shots overlap only in the 2 most-smeared frames |
| `cut` | hard cut | — |
| `match` | the incoming shot is framed by `matchKey` so its anchor sits where the outgoing anchor was, then it is revealed by a hard-edged disc that grows from the anchor over 6-8 f | each pixel switches once from A to B; only a 40 px feathered rim mixes |
| `push` | the camera pushes through an opening in the outgoing shot (window `quadPortal`, eye `circlePortal`); the incoming shot shows through the opening's outline until it fills the frame | a clip, not a blend |
| `into` | the outgoing shot freezes and shrinks into a prop of the incoming shot (homography onto the prop's projected quad) and stays there | an opaque inset; frozen with `<Freeze>`, so it costs no further renders |
| `outOf` | the incoming shot starts frozen inside a prop of the outgoing shot and grows out of it, then starts moving | as `into` |

**Story-file recipe:**
- **match:**
  - `cam[0] = matchKey(t0, anchorBoxIn, boxRect(prevGroup, t0, anchorBoxOut), az, el, fov)`
  - `join: { kind: "match", frames: 7, anchor: (t) => { const r = boxRect(thisGroup, t, anchorBoxIn); return [r.cx, r.cy]; } }`
- **push:**
  - the outgoing group's last cam key goes 0.1-0.2 m **past** the opening (the glide is still moving when the incoming takes over);
  - `join: { kind: "push", frames: 16, portal: circlePortal(prev, eyeAt, 0.05) }`.
- **into / outOf:** `quad: quadAt(groupWithTheProp, [TL, TR, BR, BL])`. Use a 9:16 picture area, so the shot maps
  without distortion.

Switch an episode over:
- `Vasa3D`: `<EpisodeNext storyboard={props} build={buildStory} overlays={...} />`, with the same props as Episode3D.
- Groups without `join` behave exactly as before.

**Kit change once free:**
- Move `layersOf` / `LayerView` into `Episode3D`, replacing its `Fade`. The whip code inside is the same.
- Optional: `into` should default `until` to the incoming group's end *including* its out-whip. Today it ends at
  `t1`, so an inset vanishes during an out-whip.

## 4. Effects (gap 4: E1, E4, E6, E8)

| File | What |
|---|---|
| `fx2.ts` | `glints` (4-point star, grows 2 f, shrinks 2 f, life 3-12 f), `burst` (inked ring + spark stars, 8-12 f), `debris` (15-100 inked shards / coins / paper / splinters, gravity, one bounce, spin), `counter` (rolling odometer plate, eased, red past `warnAt`), `scanPanel` + `scan` (scan-line reveal, 5-11 f) |

All of them are Rig factories, deterministic in time and on the NOINK layer. Cue them with `wordT(words, "word")`:

```ts
rigs: [glints([{ at: [x, y, z], t: wordT(words, "key"), size: 0.07 }]),
  burst([{ at: slot, t: hit, size: 1.1 }]), debris([{ at: slot, t: hit, n: 28, kind: "splinter", floorY: 0.2 }]),
  counter({ at, w: 1, digits: 4, from: 0, to: 0, t0: 0, t1: 1, steps: [[t0, 41], [wordT(words, "inch"), 42]], label: "INCHES" })]
```

There is no screen shake anywhere (E3). For an impact, use a `flash` light event (section 6) + `burst` + `debris`.

## 5. The reference caption style: opt-in only (gap 5: G1-G6)

`captions.tsx` has `RicksCaptions`, `ricksPages` and `ricksCaptionStats`. **It is not the default.** FEEDBACK.md
principle 5 asks for whole-phrase captions, and the owner has to choose this style.

**What it does:**
- **Look:** white Montserrat 800, mixed case with the punctuation kept, a thin dark stroke and a soft shadow. No box,
  no highlight.
- **Pages:** 1-3 words on one line. Function words ride with the next word, and a page never ends on one.
  Punctuation closes a page.
- **Position:** a fixed centre at y = 0.71.
- **Timing:** hard swaps, from frame 0 to the last frame.

To opt in: `<EpisodeNext captions="ricks" … />`. The default is `"house"`, the studio CaptionTrack with
`captionCues`, unchanged.

**If the owner chooses it:**
- The caption no longer moves to dodge faces, so the camera has to.
- Keep heads out of the 0.64-0.78 band with `fit(..., { b: 0.62 })` on chest-up shots.
- `tools/plan_kitlab.ts` shows the gate (`captionOnFace`).

## 6. Light that follows the story (gap 6: L2-L5, T8)

`lightarc.ts` provides `lightArc(arc, events)`, `blendPreset`, `mixKey` and `arcStats`.

```ts
light: lightArc([[t0, "night"], [wordT(words, "until"), "dawn", 0.8]],            // in-shot relight over 24 f
  [{ kind: "alarm", t: wordT(words, "stopped."), dur: 1.0, every: 6 },            // red wash pulsing every 6 f
   { kind: "flash", t: hit, frames: 2 }, { kind: "ramp", t, dur: 0.5, to: "golden" }, { kind: "flicker", t, to: "day" }])
```

- `lightArc` returns a `(t) => key` function. Each blend is registered in the kit's `PRESETS` table under a generated
  `~a>b@u` key (quantised to 1/48), so `GroupSpec.light` works with no kit change.
- New moods: `dawn`, `dark` (for flicker-on), `alarm` and `flash`. The kit's own presets are untouched.
- Story rule (rule book L2/L3): at least 2 light states per Short, and the explanation in night-blue (`explain`) when
  the story allows.

**Kit change once free:**
- In `Stage.tsx`, accept `light: (t) => Preset` objects as well as names. This drops the registry.
- Optionally tween `PRESETS` switches between groups of the same place.

## Caption hybrid: the reference look with whole-phrase pages (story lane default from story-barca-shield)

The coordinator's 2026-11-02 decision combines two things: the RicksClips caption look (`RicksCaptions`: white
Montserrat 800, mixed case, one line, fixed at y 0.71) and the house phrase rule for the page breaks, so no page splits
a phrase.

| Where | Change (opt-in) |
|---|---|
| `pipeline/episodes/phrases.py` | `caption_rule: "phrase1"` keeps the phrase rule's boundaries on a single line: at most 5 words and 25 characters, with the length cost starting at 14 characters. `"phrase"` and the default paging are unchanged (the stored story-vasa pages reproduce exactly). |
| `kit/captions.tsx` | `brPages(words, endT)` builds pages from the pipeline's `Word.br` breaks, with the reference timing: from frame 0 to the last frame, hard swaps, no gaps. `RicksCaptions breaks="phrase"` uses them. |
| `kit/Episode3D.tsx` | `captions="ricks-phrase"` renders the reference look with those pages. `"house"` (the default) and `"ricks"` are unchanged. |

Long pages shrink to fit one line, as `RicksCaptions` already did (about 63 px type at 25 characters).

Because the caption no longer moves, the camera has to keep faces out of the 0.64-0.78 band. Use `castKey` "close" (it
keeps head bottoms at or above 0.6) or `fit(..., { b: 0.62 })` on chest-up shots.

## Round 2 kit additions (craft and faces): what a story file can use

All of this is in `src/kit` already; nothing needs wiring. Details and measurements: `docs/RND_LOG.md`, round 2.

| Piece | Use |
|---|---|
| `kit/models.ts` | `model(id, { scale, tint, seed })` places a restyled CC0 Poly Haven model (38 ids in `LIBRARY`; licences in `public/models/ph/LICENSES.md`). Episode3D preloads them. |
| `kit/architecture.ts` | `tent`, `cart`, `stall`, `wallRun`, `roundTower`, `house`, `palm`, `well`, `standard`, `cloth`, `mudBrick`. |
| `kit/density.ts` | `fill(root, preset, [x0, z0, x1, z1], { n, keep, seed, face })` with `camp`, `campLow` (no tall standards: use it in foregrounds), `market`, `street`, `wallfoot`, `workshop`, `shore`; `crowd(id, area, n, { costumes, faces, poses, face })` returns `PersonSpec[]`. |
| `kit/sets.ts` `box(..., cast, uvTile)` | World-scaled UVs: one texture tile per `uvTile` metres on every face (paint the material with repeat `[1, 1]`). |
| `GroupSpec.sun: "auto"` | A side key at 75° to the lens, shadows fitted to the shot. |
| `GroupSpec.alive` | Windows where something visibly changes though the camera and figures are still (the `still` gate counts them). |
| `GroupSpec.bloom`, `userData.bloom` | Bloom is selective: the set's `glows` and any object with `userData.bloom = true`. Heads and white cloth never glow. |
| `GroupSpec.ao` | SSAO, off by default (it put grain on the white heads). |
| Actor `kneel: 0..1` | A real kneel; arms are inked as one silhouette with the hand. |
| Faces | Automatic: the head is shaded by the card shader as a sphere (white, a cool crescent away from the light); card rasters scale with their size on screen, so close-ups stay crisp. |

Gates added: `still` (nothing visibly changes for more than 2 s: camera under 2.5 px/frame, figures unchanged, no
`alive` window) and the edge gate's lens-loom check (a figure under 1 m from the lens in a group shot).
`scripts/visible_change.py` is the post-render twin of `still`.
