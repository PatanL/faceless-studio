# Explainer kit ("you vs. X", ocean/animal style)

**Default look: house style "Lantern & Ink"** (`experiments/kurz-style/STYLE_BIBLE.md`, engine ported from
`experiments/kurz-style/engine/` into `house/`). Old storyboards validate and render unchanged in structure; they now
render in the house look. `pipeline/episodes/house.py` adds the per-scene light, colour script, dressing and motion, and
`pipeline/episodes/staging.py` fails the build on staging collisions.

| house piece | where | what |
|---|---|---|
| shading stack (bible §4.3) | `house/shadeFigure.tsx`, used by `Creature`, every fixed figure and `FigureSVG` | form, core shadow (multiply toward a saturated ambient), stipple terminator, deep, bounce, highlight, marks, optional glint / cast; rim gated to the edges facing the back light. Light = `scene.light` in screen space (layer flipX/rotate undone). LOD from on-screen size. Opt out per layer: `"shade": false`; tune: `"shade": {"core", "hi", "rim", "marks", "cast", "glint", "lod"}` |
| hero orca | `house/orca.tsx`, `house/figures.tsx` | the engine orca (jaw rig `jaw` 0..1, `detail`, `lid`, `look`, `finScale`); the old drawing is `pose: "flat"` |
| hero diver | `house/diver.tsx`, `house/figures.tsx` | the orca_open_v3 scuba diver (dusk suit, coral fins, amber tank, flutter kick); same 2.6 m box contract; `waveAt` (s); old drawing = `pose: "flat"` (also used for silhouettes) |
| info design (bible §11) | `ui.tsx` | `Headline` = Anton title plate (ink plate, bone text, `red` words in signal red, `sub` in tide-4, wipe in); `Tag` = lantern tag (bone pill, ink text, accent dot; `leader: [dx, dy]` px draws a ring leader to the object); `ScaleBar` = gauge (tick per unit, end rings, Anton number ticking up, unit in tide-4; above the bar when the box is short). `look: "legacy"` on any of them draws the old style |
| scene light | `scene.light` (core schema) -> `house/light.tsx` | `{setup: lantern\|daylight\|cold\|stellar, angle, sweep, keyColor, rimColor, ambient, ground, haze}` |
| background | `explainer/Ocean` -> `house/oceanBg.tsx` | palette key ramp `key` (tide, mid, deep, kelp, dusk, sky, warm, danger = coral sinking to ink), colour shift `shiftTo` / `shiftAt` / `shiftDur`, rays aimed from the key and faded above the captions, caustics, 170 marine-snow specks; `look: "legacy"` = old background |
| set dressing | `house/dressing.tsx` | `explainer/Kelp`, `FishSchool`, `Jellies`, `Rocks`, `Reef`, `Seabed`, `Ridge`, `Pod` (far orca silhouettes cruising: `n`, `dir`, `scale`, `speed`); all seeded (no two identical), `plane: far\|mid\|fore` hazes in colour math |
| light / micro | `house/fx.tsx` | `explainer/Specks`, `Glow` (emitter), `LightEvent` (`lanternOn`, `spot`, `flash`, `dim`) |
| motion | core `anim.ts`, `camera.ts` | enter types `popSpring` (uniform, never < 60 % width) and `dropSquash`; `camera.drift`, `camera.preroll` |

Flat 2D vector kit for Depth Theory–style explainers: dark teal ocean, light rays, marine snow,
grey/red creature silhouettes, bold white uppercase labels with red accents. All artwork is
original code-drawn SVG (no traced frames). Works in 16:9 and 9:16; every piece fills its layer box.

Showcase: `python3 studio/scripts/gen_explainer_showcase.py` writes
`storyboards/explainer-showcase.json` (20 s, 16:9) and `storyboards/explainer-9x16.json` (6 s).
Render on the Spark: `PROPS=studio/storyboards/explainer-showcase.json scripts/spark_render.sh Storyboard explainer/showcase.mp4`.

> Always set `"captions": {"enabled": false}` and `"audio": {...}` explicitly in a storyboard that has
> none: Remotion merges `--props` over the composition's default props, so missing keys pick up the
> test storyboard's captions/music.

Time props (`at`, `out`, track keys) are scene-local seconds. Tracks are `[{"t": 0, "v": 15}, {"t": 2, "v": 140, "ease": "out"}]`.

## Background

| name | props |
|---|---|
| `explainer/Ocean` (use as `background`) | `depth` (m, number or track; darkens gradient, fades rays), `falloff` (260), `rays` (7), `rayStrength`, `snow` (70 particles), `drift`, `surface` (true or 0..1 y: sky + waterline), `skyTop`/`skyBottom`, `vignette`, `seed`, `topColor`/`midColor`/`bottomColor` |

## Figures

`explainer/Creature` with `species`, or the fixed names below. All face right (use layer `flipX`).
Built-in idle motion (tail/fluke travelling wave, tentacle waves, fin kicks, lure glow, ear flicks).

| name | real size | extra props |
|---|---|---|
| `SpermWhale` | 16 m | `teeth`, `jaw` (deg open) |
| `ColossalSquid` | 9 m | `hooks` (true) |
| `Orca` | 8 m | |
| `GreatWhite` | 6 m | |
| `BlueWhale` | 28 m | |
| `Anglerfish` | 0.2 m | (lure glow pulses) |
| `Octopus` | 6 m span | |
| `Crocodile` | 6 m | `jaw` |
| `Hippo` | 4.5 m | `yawn` (0..1) |
| `Grizzly` | 2.4 m long / `pose: "standing"` 2.7 m | |
| `Diver` | 2.6 m with fins | `torch`, `beam` (px), `arms` ("forward"/"side"), `kick`, `bubbles`, `suit`, `fins` |
| `You` (stick figure) | 1.75 m | `pose` (stand, wave, panic, point, shrug, run), `color` |
| `Bus` / `Car` / `Elephant` | 12 / 4.5 / 3.3 m tall | `text` (bus), `color` (car) |
| `Seal` | 1.6 m (harbour seal) | |
| `Liver` | organ icon | (pair with a red glow / `shadow`) |
| `Cookiecutter` | 0.5 m (smallsharks.tsx) | `glow` (0..1 or track: green belly photophores), `collar` (dark band, true), `mouth` ("closed"/"open") |

`Orca` extras (orca_kit.tsx): `pose: "top"` (top-down, flukes sway sideways), `pose: "head"` (head-on, flippers flap),
`finScale` (dorsal fin height; 1.5 = adult male ~1.8 m).

Common: `pxPerM` (draw at true scale, centred in the box; same value on two layers = honest
comparison), `align: "bottom"`, `silhouette` (true or a colour: flat dark shape, no details),
`idle` (false freezes), `speed`, `amp`, `timeOffset` (desync identical creatures).

## Infographics

| name | props |
|---|---|
| `DepthMeter` | `depth` (track), `max`, `step`, `window` (scrolling ruler of N m), `zones` [{from,to,label,color}], `side`, `suffix` (text before the unit: "+" -> "1,000+ m"; the unit " m" is always drawn), `size` |
| `ScaleBar` | `label` ("~16 M"), `at`, `duration`, `from` (center/left), `labelSize`, `color`. Box width = bar length (`16 * pxPerM`) |
| `HeightChart` | `maxM`, `stepM`, `gap`, `size`, `entries` [{kind, label, heightM?, pose?, at?}] — px-per-metre fits both wall height and total width |
| `Stat` | `value`, `from`, `prefix`, `suffix`, `decimals`, `label`, `at`, `duration` (count-up), `size`, `color`, `box` |
| `Map` | `views` [{t, lon, lat \| place, zoom}] (log-zoom), `rings` [{place\|lon,lat, r°, at, label}], `pins` [...], `highlight` [continent keys], `grid`, `zones` [{points [[lon,lat]], at, color, label (\n ok), labelAt [lon,lat], labelAnchor}] (hatched areas drawn under the coast), rings `labelSide: "left"`. Zoom >= `detailZoom` (4) swaps in hi-res coastlines from `mapdetail.ts` (Iberia + Maghreb). Coarse land includes the Hawaiian islands. A place pin without coastline in `mapdata.ts` shows open ocean at high zoom: keep zoom <= 3 or add the island rings. Places: see `mapdata.ts` `PLACES` |
| `Timer` | `from`, `to`, `at`, `rate`, `style` (box/ring), `format` (mm:ss / s), `label`, `warnBelow`, `size` |
| `Options` | `title`, `items`, `at`, `stagger`, `itemAt` [t per item], `hidden` [{index, until, text: "???"}] (answer withheld until spoken), `strikes` [{index, at}], `select` {index, at}, `size`, `struckColor` |
| `Sailboat` | side view across the waterline (waterline at `waterline` 0.5 of the box; use the background's layer depth so they stay locked). `snapAt` (rudder snaps off), `hits` [t], `list` (deg track), `sink` (px track), `bob` |
| `SpeedBars` | `title`, `rows` [{label, value, unit, color, text}], `max`, `at`, `duration`, `stagger`, `size` |
| `Headline` | `text` (\n for lines), `sub`, `color` (white/red/...), `underline`, `size`, `align`, `at`, `out` |
| `Tag` | `text`, `accent`, `size`, `align`, `at`, `out` |

Colours: `red`, `yellow`, `green` keywords or any CSS colour. Palette in `util.ts` (`C`).

## Files

`util.ts` helpers (tracks, easing, path warp, splines) · `figure.ts` figure contract ·
`marine.tsx` `land.tsx` `people.tsx` drawings · `creature.tsx` figure registry + `explainer/Creature` ·
`ocean.tsx` background + depth meter · `ui.tsx` infographics · `mapdata.ts` simplified landmasses ·
`index.tsx` registrations.
