# Zack D. Films format: VISUAL_GRAMMAR (spec for kit builders)

> Internal research only. This describes the *look* so our code-built kit can reach the same grammar with **our own** characters, props, sets and brand. Never trace, copy or recreate Zack D. Films' characters, sets, logos or shots (BRIEF hard rule 5). The story and pacing rules are in `PLAYBOOK.md`.

**Sources and method.**
- The 10 annotated videos in this folder (sections 5-6 of each file) and their contact sheets in `sheets/`.
- Measured on the Spark CPU (PyAV + numpy, 2 fps over every reference video): palette (k-means), median luma and saturation, hue shares, centre-minus-corner luma and caption geometry. Targeted colour probes on about 40 specific moments (2 probes missed their moment and are not used).
- Script and raw JSON are on the Spark in `~/studio/tmp_zackd_palette/` (`palette.py`, `probe.py`, `palette.json`). They are not in the repo.
- Three references were only served at 360x640 and one at 480x854, so their hex values carry about ±5% compression error. Treat every hex here as a **target to tune against**, not a pixel truth.
- Camera-move magnitudes (zoom %, shake amplitude) are estimates from the 1-4 fps contact sheets, marked "est.".

---

## 1. Target look in one paragraph

**"Toy-real" CG**: believable objects, creatures and people rendered clean and bright, as if lit for a product shot, with cartoon conventions (glow outlines, arrows, stink vapour, thought bubbles) dropped into that real-looking world. A cool **cobalt and cyan world** holds a **warm subject**. The light is high-key and soft even for corpses and wounds. Nothing is grimy, grainy or dark for the sake of mood. The camera always moves, and the narration is translated literally into pictures.

We cannot reach Zack's fidelity (groomed fur, subsurface skin, mocap acting) in code, and we should not try. The imitator data says a **distinct hand-built CG look beats generic AI video** (cg-3d channels 4/7 at a 10K median vs ai-3d 6/43), and low-poly accounts are among the biggest off-YouTube. So:
- **Keep the grammar** (palette logic, lighting, cutaways, signal icons, camera, cut rhythm, captions) **exactly**.
- **Simplify the surfaces**: low-poly or 2.5D shaded forms with smooth gradients, crisp silhouettes, glossy highlights and soft contact shadows.
- **Choose subjects that are rigid objects** (machines, buildings, tools, everyday objects) over fur, wet skin or flesh (see PLAYBOOK section 11).

Two implementation paths; both must hit the values below.
- **(A) Low-poly 3D in the browser** (for example Remotion with a WebGL scene). Not installed in `studio/` today, and CPU WebGL rendering speed on the Spark is unmeasured, so it needs a one-shot benchmark first.
- **(B) 2.5D layered SVG/Canvas**: forms built from gradient-shaded shapes, with parallax layers standing in for camera moves. Works with the current kit stack.

---

## 2. Frame, safe zones and composition

| Item | Spec | Measured basis |
|---|---|---|
| Canvas | 1080x1920, 30 fps, 9:16 | refs are 720x1280 / 608x1080 / 480x854 / 360x640 at 29.97-30 fps |
| Caption line | **single line, centred, vertical centre at 78.3% of H** (y ≈ 1503 px) | caption band centre 0.780-0.784 in all 9 captioned videos |
| Subject zone | key action between **10% and 72% of H**; nothing important under the caption band | every shot list keeps the subject above the lower third |
| Bottom 14% | treat as covered by the Shorts title/channel overlay; background only | caption sits just above it |
| Right edge | keep faces and key objects out of x > 86% between y 45-85% (the Shorts action buttons) | |
| Subject size | the subject or the named part fills **35-70% of the frame** in most shots; macro inserts fill 60-100% | contact sheets |
| Victim / environment as wall | big things are shown as a surface filling ≥50% of frame (the whale, the car door, the ceiling), so scale is felt not shown | CRG, p832, NEg |
| Horizon / angle | default slightly **low angle** (camera at subject's chest or below, looking up 5-15°, est.) against a bright sky or wall gradient | CRG, sloth, yud, 1Rd3 |
| Depth | 3 planes in most shots: foreground prop or body part (often blurred), the sharp subject, a soft gradient background | |

---

## 3. Proportions and character design

**Zack's people.** Semi-real adults at about **7-7.5 heads** tall, with slightly enlarged eyes and big readable expressions (grimace, recoil, bewildered hand to temple). Kids at about 5 heads. They look like cheap game-cinematic assets, and the detail budget goes to the subject, not the people. Humans are often only **hands and forearms**: in POV shots the forearms enter from the bottom corners and fill the lower 35-45% of the frame.

**Our spec (code-friendly, deliberately not a copy):**

| Element | Spec |
|---|---|
| Adult human | **1:5.5-6 heads** (stylised, between Zack's semi-real and Bob-style chibi), head 1.15x, hands 1.2x for readability, simple face: large brows and mouth shapes doing the acting, eyes 1.2x. No attempt at realistic skin. |
| Kid | 1:4-4.5 heads |
| Identity | **one flat, saturated wardrobe colour per character**, held for the whole video (and across ages). The antagonist or "other person" gets the complementary colour. |
| Expressions | at least 5 swappable states: neutral, pained, shocked (mouth open toward camera), relieved (eyes closed), bewildered. Expression changes land on the spoken word. |
| Faceless roles | causes and villains are shown from behind or for ≤0.2 s; helpers are gloved hands only. |
| Hero animal or object | real anatomy or real engineering, plus **one** cute or legible exaggeration: a large glossy eye (1.3-1.5x), an oversized handle, a readable face-like front. |
| Scale cheats | small causes (a bullet, a seed, a part) are drawn **3-10x real size** whenever they have to read on a phone; props in macro fill the frame. |
| Crowds | instanced extras in muted clothes so the hero's colour pops. |

---

## 4. Palette

### 4.1 Measured tone and colour statistics (2 fps over each full video)

| id | median luma (0-255) | luma p10-p90 | median saturation | blue share (hue 180-240°) | warm share (0-60°) | centre minus corner luma |
|---|---|---|---|---|---|---|
| yudJI1L8jlI eagle | 172 | 83-203 | 0.37 | 50% | 35% | +9 |
| MKRYulCq3Mo machine | 139 | 87-164 | 0.24 | 76% | 23% | 0 |
| W3NlT3SKkmQ ear | 125 | 91-183 | 0.26 | 40% | 46% | +8 |
| -7MDLZCb1Mw sloth | 117 | 65-160 | 0.49 | 25% | 50% | +12 |
| NEgarf1vDTU maggots | 109 | 90-129 | 0.24 | 50% | 27% | -6 |
| 1Rd3_pXs6DU product | 106 | 29-154 | 0.50 | 33% | 50% | +2 |
| 0BZ1C83I2R4 outlet | 88 | 68-112 | 0.43 | 65% | 22% | +18 |
| CRGWDiIgMZ4 shark | 69 | 60-92 | 0.60 | 78% | 15% | +24 |
| p832whe8hrI car | 56 | 34-82 | 0.59 | 68% | 14% | +12 |
| jHbhgBgaA34 posture | 53 | 38-125 | 0.63 | 59% | 19% | +58 |
| **median** | **108** | | **0.46** | **55%** | **25%** | **+10** |

"Share" = share of saturated pixels (saturation >0.25, value >0.15) by hue.

Read-outs:
- **Blue + warm = about 80% of all saturated colour.** It is a complementary teal/cobalt vs orange/salmon/tan split in every video. Green, purple and magenta appear only as signals and accents.
- **Two tone registers.** "Bright" (sky, clinic, gallery, outdoors: median luma 105-172) and "moody blue" (underwater, night interiors, inside a wall: 53-88). Even the moody register is blue and saturated, never grey-black.
- **Vignette is mild** (centre about 10 luma levels brighter than the corners), except the night interiors (+58).

### 4.2 Palette tokens (measured hex; tune to taste, keep the relationships)

**World: bright register**

| Token | Hex | Where measured |
|---|---|---|
| `sky.top` | `#12d4f6` | eagle field, top of frame (`#1fc0fe` festival, `#3bb8e7` canopy) |
| `sky.horizon` | `#95ebfc` | eagle field, mid frame. Use a **vertical gradient top to horizon**, almost a studio backdrop. |
| `sky.halo` | `#aee2f6` | brightest sky directly behind the subject |
| `wall.clinic` | `#b6e6f4` | pale powder-blue interior |
| `wall.room` | `#6289b5` | ordinary room wall (real-world scale) |
| `wall.apartment` | `#357ea4` | saturated cyan-blue apartment |
| `wall.hall` | `#7197a8` | pale blue-grey corridor |
| `wall.alt.olive` | `#505442` | "different place" colour (a second apartment) |
| `grass` | `#7fb03a` (est., lime-green) | toy-like lawns and fields |

**World: moody register**

| Token | Hex | Where measured |
|---|---|---|
| `wall.cobalt.lit` | `#233c74` | night bedroom wall in the key light |
| `wall.cobalt.shade` | `#193164` | same wall in shadow |
| `night.deep` | `#080e1c` | darkest corners (never pure black) |
| `office.deep` | `#00315f` | dark office blue |
| `gallery.night` | `#26314e` | room dimmed for a time skip |
| `ocean.upper` | `#274c78` | open water, upper half |
| `ocean.mid` | `#21436b` | most common colour in the shark video (28% of pixels) |
| `ocean.deep` | `#1a2c47` | water toward the bottom of frame |
| `lake.bed` | `#0b273f` | the "trapped" world |

**Diagram and cutaway backgrounds (flat, no environment)**

| Token | Hex | Use |
|---|---|---|
| `cutaway.royal` | `#0560a0` | first anatomy or mechanism cutaway |
| `cutaway.cyan` | `#2cb5cb` | later cutaways (lighter = "we are inside now") |
| `diagram.blue` | `#5087b1` | a flat explainer-mode background (rewind beat) |
| `micro.rust` | `#4e241a` (radial, lighter centre `#6b3a2a` est.) | microscopic scale; **inverts the scheme**: warm background, cool subject |

**Warm subject materials**

| Token | Hex | Use |
|---|---|---|
| `flesh.lit` | `#dd7777` | salmon-pink flesh or skin in the key light |
| `flesh.mid` | `#a57266` | body midtone |
| `flesh.shadow` | `#73514f` | body shadow |
| `blood` | `#842f3e` | deep crimson, used only as stylised ink clouds |
| `skin.warm` | `#c5a3a1` / `#b07056` | human skin light / mid |
| `wood.tan` | `#ceb28a` / `#9f7547` | furniture, floors, beaks, bone |
| `brown.dark` | `#413325` | dung, soil, deep wood |
| `copper` | `#b87333` (est.) | pipes, bullets, fittings |

**Signal colours (meaning, not decoration). Each one is used for one meaning only within a video.**

| Token | Hex (core / falloff) | Meaning |
|---|---|---|
| `sig.tag.green` | `#2edb31` / `#57bf44` | "this thing, the one being named": glow outline on the named object; also smell vapour |
| `sig.outline.lime` | `#7dfa6e` | structure outlines inside a cutaway (walls of a canal, layers) |
| `sig.cyan` | `#38d4eb` / `#2cb5cb` | direction arrows, on-screen numbers, seal or rim glows, electricity |
| `sig.chevron` | `#b5ddff` | motion-diagram overlay (rotation rings), pale so it sits in the palette |
| `sig.pain` | `#ff300a` core, `#b65c3a` halo | pain glow on a body part, plus red lightning-bolt icons |
| `sig.force.red` | `#e5322b` (est.) arrows; full-frame tint `#96524e` | force arrows; failure = the whole frame flushes toward red for 0.5-1 s |
| `sig.payoff.purple` | `#c47eee` / `#834998` | the one hue saved for the payoff (it appears nowhere else in that video) |
| `sig.hud.purple` | `#a271e9` / `#7454d5` | machine point-of-view grade |
| `sig.material.magenta` | `#ec7be8` | a loud colour for a new material in macro (putty, glue) |
| `sig.highlight.yellow` | `#e3c671` | highlight outline on an input object |
| `sig.heat ramp` | `#e5322b` → `#ff9a1f` → `#ffe44d` → `#ffffff` → `#2c7be5` (est.) | invisible quantity (pressure, temperature) shown as a colour fill |

**Wardrobe ID colours (examples of the "one flat colour per character" rule)**: lilac `#9a5baa`, green `#68c973`, salmon pink `#eb787a`, white tee `#f4f3f0`. Pick our own set from these hue families with ≥90° of hue between hero and antagonist.

### 4.3 Palette rules

1. **One cool world, one warm subject.** The background (60-75% of pixels) sits in hue 190-235°. The subject sits in 0-45°. The subject must be the warmest and usually the brightest region in frame.
2. **Each location gets its own wall colour** (cyan-blue flat, grey-blue hall, olive upstairs). A wall-colour change is a scene change.
3. **Each new material gets its own loud accent** so it reads at thumbnail size (magenta putty, yellow beak, green nozzle).
4. **Save one hue for the payoff** (purple charging UI): never use it earlier in the video.
5. **Signals are meaning-locked**: green = "named thing", red = force or failure, cyan = direction, number, energy. Never use a signal colour as plain decoration.
6. **No pure black, no pure grey.** Shadows go navy (`#080e1c`), and greys lean blue.
7. **Bright register is the default.** Use the moody register only when the story's place is underwater, at night or inside something, and still keep it saturated.

---

## 5. Lighting

| Element | Spec |
|---|---|
| Key | large, soft, from above and in front of the camera (est. 30-45° elevation, 20-40° off axis). Soft-edged shadows only. |
| Fill | environment colour (sky cyan or wall cobalt) at about 40-60% of key (est.), so shadows take the world's blue. |
| Rim | warm gold rim (`#ffd9a0` est.) on the subject's back edge and on cutting edges (teeth, blades, rims of plugs). The rim is what makes the warm subject pop against blue. |
| Sky halo | the background gradient is brightest **directly behind the subject**, so silhouettes read at a glance. |
| Ambient occlusion | strong in creases, grout and contact points; soft contact shadows under every object resting on a surface. |
| Underwater | moving caustic ripples on surfaces, volumetric light shafts from the top, floating particles and bubbles in every shot, haze fading to `ocean.deep` at the bottom. |
| Emissive | glows, energy and screens have bloom (about 1.5-3% of frame width blur, screen blend, est.). |
| Practicals | warm lamps (caged wall lamps, a bedside lamp) in home or inside-wall scenes. |
| Mood | changes through **colour grade or room dimming**, never by making a scene dark and contrasty. A **time skip** = the whole room dims to `gallery.night` over about 0.3-0.5 s and comes back up. |
| Dark subjects | a skeleton, a wound or a dead body is lit like a furniture catalogue: same high-key light as everything else. |
| Depth of field | shallow on close-ups and macros (background clearly soft); deep on wides. |

2.5D recipe (path B): a radial highlight gradient offset toward the key on every form; a 2-4 px rim stroke in the rim colour at 50-70% opacity on the side away from the key; an inner shadow (multiply, `#0a1530` at 20-30%) on the shadow side; a blurred ellipse contact shadow (multiply, 35-50%) under objects; an animated caustic texture (screen, 10-20%) for underwater.

---

## 6. Materials

| Material | Look | Code approximation |
|---|---|---|
| Glossy plastic / ceramic | clean white or pastel, one sharp white specular hotspot, soft reflections | a gradient body plus one small white ellipse highlight at 70-90% opacity |
| Brushed / polished steel | grey-blue with streaky linear highlights | a linear gradient with 2-3 thin bright bands |
| Copper / brass | warm orange-gold with bright edges | gradient `#7a4a24` → `#e0a060` (est.), white edge highlight |
| Glass | transparent, refraction stripes, bright edge lines, sometimes liquid inside | 10-20% fill, 2 px bright edge, 1-2 diagonal highlight stripes |
| **X-ray / hologram** (hidden internals) | translucent cyan body with glowing edges and visible inner parts | fill `sig.cyan` at 30-45%, bright 2 px edge, inner glow, inner parts drawn at full opacity |
| Cutaway section | the object is sliced; cut faces are flat-filled (black, or shown as real layers: brick, insulation, timber) | a clip path; fill the cut face flat; layers as stacked bands |
| Wet skin / creature | subsurface warmth, glossy specular, small floating particles around it | warm gradient, specular streak, bloom; **keep creature screen-time low in code** |
| Water / liquid | refractive blobs and droplets with white highlight edges; particle splashes | blob path, 2 px white edge on the light side, a small highlight dot |
| Gross matter | **styled as food or toys**: marbled salmon flesh with a fat rim, amber/orange cartoon fluid, cute translucent larvae, clean ivory bone | never realistic textures; saturated, glossy, rounded |
| Smell / gas | translucent green volumetric vapour (`sig.tag.green` at 25-40%) or wavy stink lines | animated blurred blobs or sine-wave strokes |
| Fabric | flat-colour clothing with simple folds; the colour is the identity | one flat colour plus a darker fold shape |

---

## 7. Camera language

**Rule zero: every shot moves.** The only near-static holds in the corpus are the last 1-2 s, a planted reaction beat, or a locked macro in which the *object* moves.

| Move | Use | Parameters (est. unless stated) |
|---|---|---|
| **Slow push-in** | the default on almost every shot; reveals and explanations | scale 1.00 → 1.06-1.12 over the shot, ease-in-out |
| **Crash-zoom / push-through** | changing scale: body to cutaway, animal to microscopic, outside to inside | 0.2-0.45 s (measured on the sloth video: 0.45 s wide, smear 0.2 s, macro by 0.65 s), heavy motion blur, scale ×3-×10 |
| **Whip pan / smear** | change of place or time | 2-6 frames (0.07-0.2 s) of directional blur; about half of all transitions in the car and eagle videos |
| **Follow the cause** | a long guided move riding the bullet, the energy, the food through the machine | one continuous move of 3-7 s, carrying 2-3 lines (measured: 4.6 s orbit and 7.3 s reveal in the maggots video) |
| **Orbit** | reveal what's behind a subject, or turn a still object | 15-45° over 2-5 s |
| **Crane / tilt** | location changes along a vertical (canopy to floor, up to the ceiling hole) | vertical moves mirror each other (down for "goes down", up for "comes back") |
| **Top-down** | diagram moments (rotation, crowd clearing, a body on the floor) | locked or slowly rotating |
| **Low angle up** | heroes, threats, things that are big | 5-20° up |
| **POV with handheld** | "you" trapped and acting | constant gentle drift; shake on impacts of about 1-2% of frame, 3-6 Hz, decaying over about 0.3 s |
| **Snap zoom** | stings, a nozzle firing, the bite | scale +15-25% in 4-6 frames |
| **Barrel roll / inversion** | rush during travel | once per video at most |
| **Slow motion** | the gross or comic peak only | 0.3-0.5x speed for 1.5-2.5 s |

Rules:
- **The camera follows the cause** (the energy, the food, the bullet, the smell). The camera's path is the explanation.
- **Scale changes always go through a crash-zoom or push-through**, never a plain cut.
- **Hard cuts are for changes of world** (inside the wall to outside, normal scale to micro, story to second example). One-take videos keep to 1-3 hard cuts.
- **First and last shot as a pair**: the same composition (the loop), or opposite angles (straight up / straight down).
- **No dissolves between places** (one dissolve is used for montage inside a place); no wipes; no text cards.

---

## 8. Shot lengths and cut rhythm

| Measure | Value |
|---|---|
| Average shot length | **median 1.4 s** (range 1.2-2.0 over 9 narrated videos); about 7 pictures per 10 s |
| Hook shots (0-15%) | 0.2-1.5 s; 3-4 different images in the first 5 s |
| Mechanism or explanation hold | 2-4 s (a macro of the part, a cross-section, an x-ray inset) |
| **Money shot** | **2-5 s**, the longest hold of the video (a slow push on the result) |
| After the payoff | 0.5-1.5 s per shot (cutting speeds up once the image has landed) |
| Story half of a dread piece | long continuous moves of 3-7 s (the edit slows as dread builds) |
| Transitions | whip/smear 2-6 frames; crash-zoom 0.2-0.45 s; flash to white 2-3 frames for a time jump; one black frame for an act break |
| Final tail | 0.5-0.9 s, no caption |
| Sync | **a new picture or overlay within 0.5 s of each spoken noun**; cuts on phrase boundaries; a picture change on most caption chunks |

Overlay timing: a glow, arrow or icon appears **on the word** (±3 frames), holds while the clause is spoken, and fades over 6-10 frames.

---

## 9. Captions

| Property | Spec | Measured basis |
|---|---|---|
| Position | horizontally centred; **vertical centre at 78.3% of H** (≈1503 px at 1920) | 0.780-0.784 in 9/9 captioned videos |
| Size | **font-size ≈ 68 px at 1080x1920** (3.5% of H); text band (ascender to descender) 57-72 px | white-text band 2.96-3.75% of H, median 3.4% |
| Width | single line, normally **≤72% of W**; never wraps | p90 line width 57-71% of W (one outlier at 91%) |
| Font | heavy rounded or geometric sans, weight 800 (900 for the shortest chunks). Our kit already bundles **Montserrat 800**; a rounded face (for example Nunito 800/900) is closer if added | visual |
| Colour | pure white `#ffffff`; **no keyword colour, no karaoke highlight, no emoji** | 9/9 |
| Legibility | soft drop shadow, no box: `0 3px 8px rgba(0,0,0,0.6)` plus `0 0 2px rgba(0,0,0,0.35)`; optional 1.5 px dark outline (one video uses it) | shadow pixels measured as dark navy over blue walls |
| Chunking | **2-3 words per card** (mean 2.4-2.6, range 1-4), split at phrase boundaries ("into tiny pieces"), never mid-phrase | 35 cards per 31-32 s in two videos |
| Timing | each card 0.4-1.2 s (mean about 0.9 s), locked to the voice; cards change while the voice runs, never pile up | |
| Case and punctuation | sentence case as spoken (capital on sentence starts, otherwise lower case); punctuation dropped except apostrophes and contractions | |
| Animation | none, or a 2-3 frame fade/pop at most; no bounce, no scale-pop per word | |
| Exceptions | no caption in the 0.5-0.9 s tail; the wordless format has **no captions at all**; on-screen numbers and UI text live inside the world, never as caption-style text | |

Note for the kit: the current `studio/src/core/captions.tsx` vertical default is 104 px with optional backing boxes and highlight modes. A Zack-style theme needs about 68 px, no backing, no highlight and the fixed 78.3% centre.

---

## 10. In-world graphics and icons (the "literalize" lexicon)

Use only these, each meaning-locked. Specs for building them:

| Icon | Build spec |
|---|---|
| **Glow outline (named object)** | 4-8 px outer stroke in `sig.tag.green` (or `sig.highlight.yellow` for an input) with a 12-20 px blur halo at 50%; on for the length of the naming clause |
| **Force arrows** | 3D-looking cone arrows in `sig.force.red`, 3-8 of them converging on the surface, pulsing gently in scale (±5%) |
| **Direction arrow** | one long `sig.cyan` arrow, with an optional value label (cyan, same caption font, inside the world, units correct) |
| **Rotation ring** | 12-16 pale chevrons (`sig.chevron`) in a circle around the subject, rotating with it |
| **Pain** | red-orange radial glow on the body part (`sig.pain`) plus three small red lightning bolts popping above it with a 2-frame stagger |
| **Voice / sound** | 3-4 concentric rings expanding from the speaker's mouth |
| **Smell** | green translucent vapour or 2-3 wavy stink lines rising |
| **Failure** | a full-frame red multiply tint (`#96524e` at about 35%) in 4-6 frames, held, then out |
| **Time** | a wall calendar flipping about 2 times a second, a clock prop, or the room dimming to night and back; never on-screen dates as overlay text |
| **X-ray inset** | a circular hole opening in the surface (scale 0 → 1 in 6-8 frames) showing the internals in the x-ray material |
| **Thought bubble** | a cloud-edged bubble top-left replaying an earlier shot, 1-1.5 s |
| **Machine POV** | a purple grade (`sig.hud.purple`) with scan rings and a crosshair locking on |
| **Simile prop** | a cartoon version of the simile object pops in beside the action (scale 0 → 1.1 → 1 in 6 frames) and copies the motion |
| **Brand** | our own mark printed or embossed on an in-world prop (a shirt, a machine plate, a bottle label). Never a corner bug, intro or end card |

---

## 11. Sound (for the kit's mix presets)

- One calm, even, deadpan narrator; no performed fear or excitement, even at the payoff.
- A continuous music/SFX bed **6-8 dB under the voice**, running through every sentence gap; there is no true silence until the tail.
- Master loud and compressed: **about -11.5 to -12 LUFS integrated**, LRA about 2 LU.
- Foley on every visible action (click, thud, whip, splash, crunch); one loudness step up (about +15 dB) when a machine "turns on" in wordless pieces.

---

## 12. Acceptance checks for a kit render (compare against section 4.1)

Run the same measurement on our render (`~/studio/tmp_zackd_palette/palette.py` on the Spark, CPU, nice 10) and check:

- [ ] Median luma 100-175 for a bright-register video, 50-90 for a moody one.
- [ ] Blue share (hue 180-240°) 40-78% and warm share (0-60°) 15-50% of saturated pixels; blue + warm ≥70%.
- [ ] Median saturation 0.35-0.60.
- [ ] Caption centre measured at 0.78 ±0.005 of H, band 3.0-3.8% of H, single line, ≤72% of W.
- [ ] Average shot length 1.2-1.8 s; no shot without camera or object motion except the tail; money-shot hold 2-5 s.
- [ ] Every spoken noun has its picture within 0.5 s (spot-check 10 nouns against the storyboard timings).
- [ ] Signal colours appear only with their meaning; the payoff hue appears nowhere before the payoff.
- [ ] Frame 0 shows the action; the last frame matches frame 0's composition (or the planned mirror).
- [ ] Look at the contact sheet next to `sheets/<closest ref>.jpg`: the subject should be the warmest, brightest thing in each tile, and nothing should read as grimy, grey or dark-for-mood.
