# horror kit (B4)

Phone-chat horror story kit: flat 2D cartoon, dark muted night palette, thick dark outlines.
Everything here is original art drawn in code (SVG and CSS). Example: `storyboards/horror-showcase.json`
(20 s, 9:16), built by `scripts/gen_horror_showcase.py`. Rendered: `out/b4/horror-showcase.mp4`.

All components are `{"type": "component", "name": "horror/<Name>", "props": {...}}`. Times in props are
scene seconds. Most components also take `glitch: [{at, duration, amount}]`, which RGB-splits and
slice-shifts that component.

## Devices

| Name | What it is | Key props |
|---|---|---|
| `horror/HandPhone` | A big cartoon hand holding the phone from below, with the thumb over the screen. Use it as a full-frame layer. | `phone` (all Phone props), `phoneWidth` 0.7, `cx`/`cy`, `tilt`, `side` right/left, `taps [{at,x,y}]`, `tremble` px, `trembleCues`, `thumbReach` |
| `horror/Phone` | The phone alone, scaled to fit its box | `mode` chat/lock/call/off, or `screens [{t, mode}]`; `members {name: {color, initials}}`; `chat`, `lock`, `call`; `banners [{at, duration, app, title, text}]`; `vibrate [{at, duration, amount}]`; `dim` |
| `horror/FeaturePhone` | An old candybar phone with an LCD | `sms {from, text, at, cps}`, `header`, `clock`, `lcd`, `backlight`, `vibrate` |

- `chat`: `title`, `count` (members), `subtitle`, `dayLabel`, `unread` + `unreadFrom` (the red badge counts up as messages arrive), `accent`,
  `messages [{from, text, at, me, kind:'alert'}]`, `typing [{from, at, until}]` (typing dots plus "X is typing…" in the header), `draft`, `clock`, `battery`.
  Each message pops in at `at`, the newest one pushes the list up, and older ones scroll off the top.
- `lock`: `time`, `date`, `notifications [{at, app, title, text}]` (they stack, newest first).
- `call`: `name`, `sub`, `label`, `at`, `connectedAt` (switches to a running call timer).

## Characters (8 expressions each, auto blink, mouth flap)

`horror/Protagonist` ("Nora": a dark bob with a ragged fringe and an olive hoodie) and `horror/Neighbour`
(alias `horror/Stranger`: "Mr. Hale", gaunt, grey comb-over, pencil moustache, maroon cardigan).
Both are drawn waist-up in a 500x760 art box, so give the layer the same ratio, for example `"width": 640, "height": 973`,
`"y": "100%", "anchorY": 1`.

- Protagonist set: `neutral worried scared terrified suspicious shocked relieved angry`
- Neighbour set: `neutral smile grin blank angry sad surprised sly`. Either character can use any expression.
- `expr`, or `exprs [{t, e}]` for timed swaps (each swap gets a small pop). `talk [[from, to], ...]` makes the mouth flap.
- `pose`: `idle`, `phone` (holding a glowing phone that lights the face from below), `ear` (on a call), `cover` (hands over the mouth).
- `lookX`/`lookY` (-1..1), `tilt`, `light` none/phone/red, `silhouette` (black shape with eye glints),
  `blink` false to stop blinking, `colors {hair, top, topShade, skin, shirt}` to recolour.

## Backgrounds (1080x1920 art, crops to any box, works in 16:9 too)

| Name | Props |
|---|---|
| `horror/FrontDoor` | `knocks [t...]` (door rattles, impact marks), `chain` on/off, `hallLight`, `feet` (bool or [from,to]: a shadow under the door), `handle [{at,duration}]` (the lever jiggles), `peepholeGlow`, `flicker` |
| `horror/Peephole` | `figure` neighbour/silhouette/none, plus the Neighbour props (`expr(s)`, `talk`, `look*`), `lean`, `flicker`, `radius` |
| `horror/Hallway` | `flicker`, `lights` 1-3, `endDoor`, `runner`, `figure` (0..1 silhouette), `figureDepth` (0 near .. 1 far) |
| `horror/ElevatorPanel` | `from`, `to`, `at`, `perFloor` (the red floor counter climbs and the arrow blinks), `floors`, `target`, `pressed [{at, floor}]`, `flicker` |
| `horror/Bedroom` | `lamp` 0..1, `wardrobeOpen` 0..1, `rain`, `phoneGlow`, `flicker` |
| `horror/LivingRoom` | `lamp`, `tv` off/static/glow, `flicker` |
| `horror/Stairwell` | `floor` ("7"), `flicker`, `exit` |

To blur a set behind a phone, use it as a layer instead of the background: `{"type":"component","name":"horror/Bedroom","blur":10,"opacity":0.7}`.

## Effects (full-frame overlays: `"depth": 0`, high `z`)

| Name | Props |
|---|---|
| `horror/Flicker` | `strength`, `rate`, `seed`, `blackouts [{at,duration}]`, `from`/`to` |
| `horror/Vignette` | `amount`, `color` ("r,g,b"), `inner`, `pulse` Hz |
| `horror/Heartbeat` | `bpm`, `bpmTo` (speeds up), `color`, `intensity`, `from`/`to` (red edges throb lub-dub) |
| `horror/Glitch` | `cues [{at,duration,amount}]` or `amount` (inverted or hue-shifted bands, RGB tear lines, blocks, scanlines) |
| `horror/RedText` | `text`, `at`, `duration`, `style` flash/neon/scrawl, `fontSize`, `strobe` Hz, `cps` typewriter, `shake` |
| `horror/Darkness` | `x`, `y`, `radius`, `darkness`, `color`, `flicker` (dark room with one light pool) |

Screen shake uses the core camera: `"camera": {"shake": [{"at": 0.4, "duration": 0.2, "amplitude": 20}]}`.
Scene cuts can use the core `glitch`, `dipBlack` or `whip` transitions.

## Captions

Burned-in captions come from the core caption track. The style used in the showcase, at the top of the frame and clear of the phone:
`{"fontSize": 76, "highlight": "#ff4b55", "uppercase": false, "strokeWidth": 12, "y": 0.15}`, `maxWords` 3, `maxChars` 16.
In phone scenes, keep `HandPhone.cy` at about 0.585 so the caption has room above the phone.
