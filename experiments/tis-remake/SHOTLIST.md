# TIS AK-12 Short: shot list (internal benchmark, never published)

Reference: The Infographics Show, "Why the Russian Military Switched to the AK-12",
https://www.youtube.com/shorts/syVYb73Yj38 (uploaded 2023-09-30, 1.83M views), 56.0 s, 1080x1920, 30 fps, VP9 + Opus.
Local media (git-ignored): Spark `~/studio/refs/tis-ak12/` (ref.mp4, audio.wav, f025/ every 0.25 s, f30/ every frame,
stills_full/ 64 PNGs); Mac `experiments/tis-remake/ref/` (sheets/, transitions/ per-frame strips, stills/ 64 at 720x1280,
transcript.json, words.tsv, scenes04.txt). Reproduce with `tools/analyze_ref.sh`.

Coordinates are in 1080x1920 pixels, (0,0) top-left. Times are in seconds. Hex values come from median-cut palettes of
the full-res stills (`tools/palette.py`), so they are ±3 per channel. Flag, clipboard, FX and a few small-prop colours
were eyeballed from the 720p stills (verify them before matching exactly). "A/B/C…" name the character designs.

**Count: 26 shots** (one shot = one framing; a framing reached by a continuous camera move counts as its own shot)
inside **10 scene blocks**, joined by **9 transitions** (5 matte/blob wipes, 2 diagonal slash wipes, 1 iris, 1
explosion cover). Only 6 hard-ish cuts register at a 0.12 scene threshold (2.63, 7.23, 15.47, 22.03, 44.57, 50.0), and
several of those are camera moves, not cuts. Average framing length is 2.15 s, and the frame is never still: some
camera or character motion runs on every frame.

---

## 0. Global layers and rules (apply to every shot)

Layer order, back to front: **BG plate** (sky or wall) → **mid set** (buildings, huts, props) → **characters** →
**foreground props** (crates, hedgehogs, desk) → **FX** (sparkles, muzzle flash, explosion) → **UI icon layer**
(calendar, clipboard; these are pinned to the screen and ignore the camera) → **caption box** → **transition matte**
(above everything except the captions; the captions swap separately).

### Captions (start 2.75 s, all the way to the end)
- Box: `rgba(0,0,0,0.70)`, solved from two backgrounds (tan #C4A074 → #3A3022, purple #5836D2 → #19103F). Corner radius
  about 36 px. Centred horizontally. For 4-line pages it spans x 76–1004 (928 px wide) and y 1282–1717 (435 px tall). The
  width hugs the longest line plus about 40 px padding each side (3-line pages are narrower and shorter, with the top
  edge at about y 1300 and the bottom about y 1690). The box stays vertically centred on about y 1500 (78 % of the height).
- Text: white #FFFFFD, centred, 4 lines (sometimes 3), font size about 66 px, line pitch about 100 px (rows at
  1321/1420/1520/1620), medium weight. The face is a rounded-terminal geometric humanist sans with a slightly square
  "o", a single-storey "g" and a straight-tailed "y". Closest Google fonts to test: **K2D Medium**, Kanit Light/Regular,
  Mitr Light. No stroke, no shadow, no per-word highlight, no word-by-word reveal.
- Paging: 13 pages of 12–17 words. Pages break mid-sentence ("…But much like with most" / "things for Russia lately,…"). A
  page appears about 0.15–0.25 s **before** its first word is spoken, with a hard swap (no fade), except at 26.0 s, where
  it cross-dissolves over 2 frames under the iris. The caption text paraphrases the voice slightly ("Moscow, mired in its
  war" for "Moscow Mired and its war"; "out like hoped").
- Page timings: 2.75 · 7.2 · 11.5 · 15.5 · 19.25 · 22.6 · 26.1 · 30.5 · 35.2 · 40.0 · 44.75 · 48.4 · 51.75 → end.

### Hook title pills (0.13–2.9 s only; no caption box during the hook)
- Pill 1: yellow #EBD10D (lighter edge #EDD722). Text "WHY DID RUSSIA SWITCH" in dark #2E2A12, heavy geometric
  caps (Montserrat ExtraBold / Gilroy Black class), cap height about 60 px. The pill spans y 180–322 and runs from x
  about 0 to 1020, with a corner radius of about 20 px. Hard drop shadow: a darker olive/brown #63511B duplicate offset
  about 8 px down and 8 px right, with no blur.
- Pill 2: red #E23536 with shadow #AA2D23. Text "TO THE AK-12 RIFLE?" in near-white #FCEDE6 at the same weight, about
  0.85× the size. It spans y about 378–492, centred.

### Character kit (all humans)
- Flat vector with **no outlines**. Every shape is a filled path, and shading is done with flat darker or lighter shape
  overlays.
- Head: rounded rectangle, skin #F6BE98 with a shadow shape #E5B08C on the far side of the face, and pink cheek blush
  ovals (about #F0A090 at 60 %). Eyes: a green iris #5D8A1E (Russian soldiers) or blue #2563B0 (Ukrainian soldier, the
  leader), with a dark pupil and a small white glint. Brows are thick dark bars that carry the expression. The mouth is
  a dark shape #2B1A15 with a red tongue or white teeth, inside the beard silhouette.
- Facial hair defines the identity: A full black beard; B brown goatee; C black beard firing; D moustache; E brown
  hair and goatee; F moustache; G (Ukrainian) brown beard.
- Hands are **plain skin circles** #EFC5A8 (no fingers, except the pointing hand in S04, which has an index finger).
  The hand circle sits on top of the gun.
- Helmet: camo #6D674A / #4A482F / #84856F with goggles on the brim (strap #303025, lenses #333332 with a lighter
  #58574C highlight band).
- Uniform camo: base #6D674A, blotches #4A482F, #303025, #84856F and #A6B27F, as rounded-capsule blobs (not pixel
  camo). The plate carrier is a darker #4A482F with pouches drawn as rounded rectangles plus one darker inner shape,
  and a buckle (light #BEBAB7 rounded-rectangle outline).
- Flag patch (RU or UA) on the upper arm, as a small rounded rectangle with a grey border.
- Boots are near-black #1F1D18 with a #3A3933 top highlight.
- Guns: metal #2E312C / #3C3F3C / #272E32 with a lighter top-edge strip #58574C. AK-47 furniture is wood #B4532F
  with a darker #8A3A20 edge. The AK-12 is all black, with a picatinny rail drawn as a row of small dark squares and a
  vented handguard (rounded slots).
- Rig: standard cut-out puppet. Pivots at the neck, shoulders, elbows, hips and knees. The head bobs while talking, and
  mouth shapes alternate (open O, teeth grin, closed) at about 6–8 Hz with the voice. There are blinks. Hands move on
  arcs with ease-in-out. Characters breathe (torso scale y 1.00↔1.01) when idle.

### Sky and clouds
Sky is a flat light blue (#D0E5FA, or #AEDDFA in UA scenes, or #94A2EB lavender in the S17 ruins). Clouds are puffy
groups of overlapping circles, white #F7FBFD with a light grey-blue underside #C7E1F0. They drift slowly left at about
10 px/s.

### Camera grammar
Every framing drifts. Ken-Burns pushes (scale +3–8 % over the shot) and **dutch rotations of ±5–20°** are common, and
big moves between framings are fast ease-in-out (0.4–0.9 s, cubic or quint). The camera often ends a move with the
subject in a CU, then the next scene starts wide. There is no motion blur on moves, except the whip/slash wipes.

### Audio
A continuous music bed sits under the voice: gaps between words read -24 to -26 dB mean, the same as speech windows,
so the bed is fairly loud. The bed fades out by 55.7 s (-42 dB). The voice is a male US narrator at about 205 wpm
(185 words in 55.3 s). Cuts and wipes land on the **first word of a new sentence** (±0.1 s).

---

## Scene block 1: Hook title (0.00–2.90)

### S01 · 0.00–2.90 · AK-12 hero on a swirl sunburst
- **On screen:** a full-frame swirl sunburst (curved spiral rays from a centre at about (540,1140)) of alternating
  orange #F66D00 / #F7770D and yellow-orange #F88F14 / #F8AE1D rays, darkening to red-orange #F54602 / #F65403 at the
  frame edges (radial vignette). A fine diagonal hatch texture runs over the whole BG at about 6 % contrast (45° lines
  about 6 px apart). The AK-12 rifle sits centred at about (540,960). It is about 760 px long and rotated -25° (muzzle up
  and right), all black #2E312C with a #58574C top-edge strip and a vented handguard. Title pills 1 and 2 are
  overlaid. The rifle has no shadow.
- **Frame 0:** sunburst and rifle only (no title). The subject is on screen in frame 1.
- **Motion:**
  - The BG swirl rotates slowly clockwise, about 6°/s, linear.
  - The rifle floats with a ±6 px vertical bob and a ±1° rotation on a 2 s sine.
  - Sparkles: a white #FFFFFF 4-point star (concave sides). One grows on the receiver at 0.50 s (0→160 px, 0.25 s ease-out),
    then a second smaller one pops at the mag at 1.25 s. Each sparkle scales up, rotates about 30° and shrinks back to 0
    over about 0.5 s.
  - Pill 1 slides in from off-screen right (x +1080 → 0) from 0.13 to 0.50 s with a strong ease-out (expo), no
    overshoot, and the text clips inside the pill as it slides.
  - Pill 2 slides in from the right from 0.95 to 1.30 s with the same easing.
  - The pills hold until the wipe.
- **Camera:** static.
- **Transition out (2.87–3.20, 10 frames):** a **silhouette matte wipe**. The incoming S02 frame is revealed through an
  organic mask shaped like an oversized soldier silhouette (helmet dome first). It enters from the top-right corner,
  rotates slightly and scales up until it covers the frame by 3.2 s. The outgoing frame stays static under it. The mask
  edge is hard (no feather) and there is no border.
- **Caption:** the first page "Moscow, mired in its war / in Ukraine, announced it / would be switching from / the famed
  AK-47" hard-cuts in at 2.75, before the wipe.
- **VO:** "Why did Russia switch to the AK-12 rifle?" (0.00–2.4)

## Scene block 2: Russian base, the old rifle (2.90–14.0). One continuous set; the camera travels inside it.

Set: an olive quonset hut. Arch #69654C with a lighter rim band #ABA479, a door recess #333332, and door-frame struts
#53533D drawn as rounded bars. A second hut stands left and behind it at 70 % scale. The ground is grass #A9B281, with a
path strip #DBCEC3 and dirt #C4A074 in front. The sky is #D0E5FA with cloud groups. Russian flags (white #FFFFFF / blue
#0039A6 / red #D52B1E, in rounded-rectangle frames with a light grey border #E6E6E6) fly on dark grey poles #3A3933 with
a ball finial. A steel lattice watchtower #2B2B2B sits on the right edge.

### S02 · 2.90–4.50 · MCU soldier A at the hut door, dutch angle
- **On screen:** soldier A (full black beard #1F1D18, black hair, helmet with goggles, green eyes) fills the right
  60 % of the frame, cut off at mid-thigh. He holds an AK-47 diagonally across his chest (wood furniture #B4532F,
  mag #2E2D2A). The left hand circle grips the handguard at about (220,620) and the right hand circle the pistol grip at
  about (520,840). The door's dark recess is behind him on the left, and the hut arch curves at the top right.
- **Composition:** horizon tilt -18° (the ground line rises to the left). The head is at about (640,450), the RU patch
  at (980,820), and the caption box covers the waist.
- **Motion:** A talks (mouth open/closed at the speech rate) and his brows lower (stern). The head bobs ±4 px. The gun
  sways slightly with the arm (±2°).
- **Camera:** slow push-in (scale 1.00→1.03) with a small counter-clockwise drift.
- **Caption:** page 1.
- **VO:** "Moscow, mired in its war in Ukraine, announced…"

### S03 · 4.50–5.60 · Pull-out reveal (camera move)
- **Motion:** a single fast zoom-out from MCU to wide (scale about 3.2 → 1.0) **while rotating from -18° to about -3°**,
  ease-in-out cubic, centred on A. Soldier B enters frame left as the frame widens; he is already there in the set (no
  separate animation). Flags and the watchtower come into view at the top. A keeps talking.
- **Caption:** page 1.
- **VO:** "…it would be switching from…"

### S04 · 5.60–8.10 · Wide two-shot: B points, A shows the AK-47
- **On screen:** the full set at about 1.0 scale with a slight -3° tilt. Soldier B (brown goatee #6B3B1E, scowl, left at
  x≈220, full body, feet at y≈780) points at A with an index finger hand. A stands on the right at x≈530, holding the
  AK-47 diagonally. The big flag is at (460,150) and the small flag at (110,200). The tower is on the right edge.
- **Layer order:** sky → clouds → back hut → tower → front hut → flags → ground → B → A → caption.
- **Motion:**
  - B's pointing arm extends and stabs twice (rotate from the shoulder about 10°, ease-in-out, 0.4 s each).
  - A turns the gun upright (from 6.9 to 7.6 s the rifle rotates from -45° to about -80° and lifts), then raises it above
    his shoulder as if handing it off, and it exits frame top-right by 8.3.
  - Both characters blink, and their mouths move only for the one "speaking".
  - Flags wave (a 2-frame shape cycle or a sine skew on the flag cloth, ±3°).
- **UI:** at 7.25 a **calendar icon** pops in at the top-left (x 50–270, y 85–260). It is a white rounded square
  #FDFDFD with a light-grey bottom shadow band #EAEAE8, a red header #C12B29 with 4 dark ring loops, and a soft drop
  shadow (about 8 px y offset, 20 % black). It enters with scale 0→1.1→1.0 over 0.3 s (back-out) and is **pinned to the
  screen** from here to 14.0, ignoring all camera moves.
- **Camera:** an almost imperceptible push (1.00→1.02).
- **Caption:** page 1, then page 2 at 7.2 ("to a more versatile model / in 2023, and testing was / ongoing on the new
  model.").
- **VO:** "…the famed AK-47 to a more versatile model…"

### S05 · 8.10–9.00 · Push and rotate onto A's chest; the calendar types "2023"
- **Motion:**
  - The camera pushes from wide to a chest CU on A (scale 1.0 → 3.0) while **rotating +15° clockwise**, ease-in-out
    over 0.9 s. B slides out of frame left.
  - A's hands come back down holding the **AK-12** (a prop swap hidden by the raise in S04). The hand circles pass
    close to the lens and read as big skin discs.
- **UI:** the calendar's date types in digit by digit in red #C12B29, bold rounded font, about 70 px: "2" at 8.47, "20"
  at 8.63, "202" at 8.80, "2023" at 8.97 (one digit every 5 frames). There is no cursor or pop per digit.
- **VO:** "…model in 2023,…" (the digits finish as "2023" is spoken at 8.58–9.0)

### S06 · 9.00–11.30 · CU AK-12 in A's hands, sparkles
- **On screen:** the AK-12 receiver and handguard run diagonally (about -55°) across the upper-middle frame, against
  A's camo torso and the dark door recess #333333. One hand circle sits at about (360,420), sliding on the gun.
- **FX:** big white 4-point sparkles. At 9.25 a 300 px sparkle appears on the receiver, and at 9.50–10.0 another grows
  to about 450 px with a small secondary star beside it. Each scales 0→1→0 over about 0.5 s with a 20–40° spin.
- **Motion:** the gun rotates slowly clockwise (about 5° over the shot) and drifts up. From 10.75 to 11.30 the hands lift
  the gun up and out of frame top-right.
- **Camera:** drift right and down (about 120 px), linear-ish.
- **Caption:** page 2.
- **VO:** "…and testing was ongoing on the new model."

### S07 · 11.30–14.00 · Clipboard checklist next to B's face
- **On screen:** soldier B's face on the left edge (cropped by the frame: brown beard, big grin #FFFFFF teeth, green
  eyes) in MCU, plus his camo shoulder and buckle.
- **Clipboard:** a navy board #2F3E55, a white sheet #FDFDFD, a yellow clip #F2C94C with a darker base #E0A82E and a skin
  hand behind it. Three rows each hold a rounded checkbox outline #D0D0D0 and 3 grey text bars #CFCFCF. The clipboard is
  held up on the right at about (560–900, 330–1000), rotated +5°.
- **UI:** the calendar is still pinned top-left.
- **Motion:**
  - The clipboard **swings up from below the frame** (11.35–11.75), rotating from +30° to +5° around its bottom with
    back-out easing.
  - The camera pans left at the same time (11.5–11.9) to bring B's face in.
  - Green check marks #2DB34A pop into the boxes at 12.25, 12.75 and 13.25. Each scales 0→1.15→1 over 0.2 s, with the
    box filling with green and a white tick.
  - B grins and nods (head rotate ±3°) at each tick.
- **Camera:** slow push 1.00→1.04.
- **Transition out (13.95–14.25, 9 frames):** a **silhouette matte wipe**. The incoming firing-range frame is revealed
  through the silhouette of the kneeling shooter (S08's character, scaled about 4×). It flies in from the bottom-right and
  shrinks toward its final place, so the matte effectively becomes the character. The **muzzle flash of the incoming
  shot is visible early** in the matte, at 14.03.
- **Caption:** page 3 at 11.5 ("On the surface, this new / gun has some great / features. With a 16 - / inch barrel, it
  can fire").
- **VO:** "On the surface, this new gun has some great features." · the wipe lands on "With a 16-inch barrel"

## Scene block 3: Firing range (14.0–22.0)

Set: an outdoor range. A beige corrugated hangar wall #C8C0A5 / #DFD1C2 with a curved arch edge, a roller door #B99F7A
with horizontal slats and a dark lintel #4A3F35, and a dark plinth strip with vertical posts #3C372E along the base. Bay
signs: white rounded plates #FFFFFF with black heavy digits "270" (sign at (930–1015, 115–155) scaled) and a big "A".
The ground is sand #CCB69A with long lighter capsule streaks #DFD2C3 (wind-swept dust bands, horizontal), and the
target zone has a barbed-wire fence on the horizon, a lifeguard-style tower on the left and a watchtower post #3C372E.

### S08 · 14.25–16.00 · Soldier C kneeling, firing the AK-12 (side view)
- **On screen:** C (black beard, black hair, angry brows) kneels on the right knee facing right at about x 870–1140,
  y 315–820 in the 720-wide still, which is about 40 % of the frame width. He shoulders the AK-12. Its muzzle flash is a
  6–8 point star burst, orange #F7931E with a yellow core #FFD34D and red-orange tips #E8542A, about 110 px. The
  hangar wall and door are behind him and the sign "270" is upper middle.
- **Motion:**
  - Burst fire: the muzzle flash flickers every 2–3 frames (alternating 2 star shapes and scales 0.8–1.2) for the
    whole shot.
  - The gun recoils 6–10 px back along its axis with each flash, and the head and shoulders recoil 2–3 px.
  - Small brass casings eject up and right as tiny yellow rounded rectangles (barely visible).
- **Camera:** static from 14.25 to 16.0.
- **Caption:** page 3, then page 4 at 15.5 ("700 rounds per minute and / has a two-round burst / function. It's also
  well").
- **VO:** "With a 16-inch barrel, it can fire 700 rounds a minute,…"

### S09 · 16.00–17.00 · Truck right along the range (camera move)
- **Motion:** the camera trucks right about 1.3 frame-widths in 1.0 s (ease-in-out). C keeps firing and exits left, the
  "A" bay sign passes, and the hangar's arch end and the open range with its tower enter. Parallax: the far fence and
  tower move at about 0.6× the ground speed.
- **VO:** "…and it has a two-round burst…"

### S10 · 17.00–18.20 · Target settles
- **On screen:** a round archery target on a wooden tripod (legs #6E4B3A) at centre-left (about x 140–520, y 260–830
  scaled). Rings: outer face #2F3B45 with a dark rim, white #FFFFFF, light blue #5DADE2, red #E74C3C, yellow #F7C548
  bullseye. Bullet holes are black dots with grey star splinters.
- **Motion:** the target eases into its final position (the camera's truck ends with a soft settle). At 17.0–17.4 the
  target **rotates slightly toward the camera** (a 3D-ish y-turn faked with an x scale of 0.85→1.0). New bullet holes pop
  in (2 frames each) in a burst of two.
- **Caption:** page 4.
- **VO:** "…function."

### S11 · 18.20–19.60 · Soldier D pops in beside the target
- **On screen:** soldier D (moustache #4A2A1A, helmet with goggles, full plate carrier, RU patch) stands right of the
  target, full body (feet at y≈850 scaled), holding an AK-12 fitted with accessories (optic, foregrip, rail, suppressor)
  at hip level. The muzzle rests in front of the target.
- **Motion:** D **grows from a dot to full size** between 18.23 and 18.60 (scale 0→1, anchored at the feet, ease-out
  cubic, no overshoot). From 19.25 he raises the rifle to his chest (about 25° rotation, ease-in-out 0.4 s). Blinks.
- **Caption:** page 5 at 19.25 ("suited for accessories, / and has a lower recoil. / But much like with most").
- **VO:** "It's also well-suited for accessories…"

### S12 · 19.60–21.95 · Push-in to D, heart eyes
- **Motion:**
  - The camera pushes from full body to an MCU of D's head and gun (scale 1.0→2.6) while **rotating +12°**, ease-in-out
    over about 1.2 s (19.9–21.1), then holds with a slow drift.
  - D's eyes switch to **pink hearts** #E8457C with a darker edge at 20.25 (a hard swap). The hearts pulse (scale
    1.0↔1.15 at about 3 Hz).
  - D smiles (mouth corners up) and hugs the gun to his chest.
- **Transition out (21.97–22.30, 10 frames):** a **diagonal slash wipe**. Long tapered streaks at about -30° (lower-left
  to upper-right), 20–120 px thick, alternating between the incoming and outgoing frame. They sweep across, the outgoing
  image smears along the streak direction (directional blur on the slices), and by 22.3 only the incoming frame is left.
  It reads as a speed whip.
- **Caption:** page 5.
- **VO:** "…and has a lower recoil."

## Scene block 4: The leader's office (22.0–26.0)

### S13 · 22.00–26.00 · Russian leader at his desk with the AK-12
- **On screen:** a stylised caricature of a Russian head of state, but **our remake must use a generic, unnamed
  official** (rule 5: original characters, and no real-person likeness needed for the benchmark). He has grey-brown
  thinning hair #A08E6F, a navy suit #27303D / #171F2C, a white shirt, a red tie #C0392B and blue eyes. He sits behind a
  heavy mahogany desk (top #85402E, front panels #752E22 with lighter bevel lines #94644D and a dark shadow #29110E) with
  the AK-12 lying across it, plus a stack of papers and blue folders on the left.
  - The room is wood panelling #542A17 with taller arched panels #643827 / #6F3A28 and a darker gap shadow #351815.
  - A gold double-headed-eagle emblem #F2B32A sits at top centre.
  - Orange-gold table lamps #F7A824 sit at the lower corners.
  - There is a pale wall strip #DAB696 at the top right.
- **Composition:** symmetric. The head is at about (540,560) and the desk edge at y≈1020. The caption overlays the
  desk front.
- **Motion:**
  - He scratches the back of his head, worried: the arm cycles up and down, 22.3–23.8.
  - The hand then comes to rest on the gun, and he taps it.
  - Mouth: small "o" shapes. Brows rise (concern). Slow blinks.
- **Camera:** slow push 1.00→1.12 over 4 s, linear, with a slight rise.
- **Transition out (25.97–26.33):** an **iris wipe**. A circle opens from the frame centre (about (540,900)) from 0 to past
  the corners in 0.33 s (ease-in). The circle edge has a soft semi-transparent rim (about 40 px, 40 % white or grey
  ring) and a slight lens-blur/refraction look. The caption box cross-dissolves to the next page during the iris.
- **Caption:** page 6 at 22.6 ("things for Russia lately, / things aren't turning / out like hoped.").
- **VO:** "But much like with most things for Russia lately, things aren't turning out like hyped."

## Scene block 5: The ruined city, mode selector (26.0–32.4)

Set: a bombed city. The street is slate #7F92A7 with lighter capsule streaks. A tall cream apartment block #E2D5BA sits
right, with dark navy windows #201940, broken frames, crack lines #7B675D and exposed bricks. A collapsed concrete
frame on the left has twisted rebar beams #7B4B4B / #5C3A3A drawn as rounded bars. A mauve ruin wall #8E6A73 / #4A555C
stands behind, with a blue-grey distant ruin #4A555C, and the sky is #B1D6EA with big clouds.

### S14 · 26.00–28.00 · Four soldiers in a squad line
- **On screen:** four Russian soldiers (B, A, F and a blond one with blue eyes) stand side by side in a tight line
  (about x 120–720, y 410–790 scaled to 720), rifles at low ready, knees bent in a "patrol crouch". The tower block is
  behind on the right and the rebar ruin on the left.
- **Motion:**
  - A marching cycle: alternating knee bends and 4–6 px vertical bob, offset per soldier (a stagger of about 3 frames).
  - The rifles bob with the bodies.
  - The soldiers glance at each other with head turns.
- **Camera:** push-in (1.0→1.6) drifting toward the right-hand soldier's gun, ease-in, accelerating into S15.
- **Caption:** page 7 at 26.1 ("The mode selector on the / new rifle was designed / in a poor and uncomfortable /
  way, making it far too").
- **VO:** "The mode selector on the new rifle was designed…"

### S15 · 28.00–30.40 · ECU on the mode selector (hand over receiver)
- **On screen:** an extreme close-up. A giant skin hand circle #EFC5A8 (about 380 px diameter) sits over the rifle
  receiver #2E312C with its vented slots, against the plate carrier with its pouches and buckle (#6D674A / #4A482F, buckle
  #BEBAB7).
- **Motion:** the push continues and then settles (28.0–28.8, ease-out). The hand fumbles: it shifts ±10 px and rotates
  slightly, 2–3 small taps (suggesting the awkward selector).
- **Camera:** slow drift down and left.
- **Caption:** page 7.
- **VO:** "…in a poor and uncomfortable way,…"

### S16 · 30.40–32.43 · Tilt up to soldier E grimacing
- **Motion:** the camera tilts and pans up (30.4–31.2, ease-in-out) from the hand to the face of E (brown hair
  #6B4A2A, goatee, green eyes, worried frown, mouth open). The camera rotates -8° during the move.
- **On screen:** E in MCU, RU patch, the gun across the bottom, and the ruined cream building and slate sky behind.
- **Motion:** E talks and complains (mouth cycle, brows tilted up in the middle).
- **Transition out (32.43–32.80, 11 frames):** an **organic blob matte wipe**. The incoming S17 frame grows inside an
  irregular rounded blob that starts at E's mouth and hand (about (600,800)). The blob expands with wobbling lobes, like
  ink spreading, until it covers the frame.
- **Caption:** page 8 at 30.5 ("easy to switch between / modes. The gun was also / proving unreliable, with / many guns
  quickly being").
- **VO:** "…making it far too easy to switch between modes."

## Scene block 6: The front line, pink city (32.4–38.6)

Set palette (a warm pink-sunset ruin): lavender sky #94A2EB with cloud groups #DECECE / #94A1F1. Salmon / pink
apartment blocks #FCD5B1 / #F6C2B1 / #EFAA9B with darker pink sides #DD7480 / #C36170, and windows #451233 / #602A3A
(some blown out). A collapsed red block #C4675E sits mid-ground, the rubble is dark #2A1B17 / #7A504A, and the ground is
pink #ECB8A9 with dusty-rose #D89998. The foreground street is plum-brown #7A4F49.

### S17 · 32.50–34.50 · MCU soldier F (UA patch) yelling in the ruins
- **On screen:** F (moustache, blue eyes, fierce brows, mouth wide open yelling #C0392B inside) sits large on the
  left 70 % of the frame. He holds an AK-47 with wood furniture low at the bottom and wears a **Ukrainian flag patch**
  (blue #0057B7 / yellow #FFD700). In the background, two small soldiers fire from behind a rubble barricade, with tiny
  muzzle flashes.
- **Motion:**
  - F yells (mouth wide, head forward 10 px, brows down) and blinks.
  - The background soldiers loop a firing cycle with flash flicker.
  - The clouds drift.
- **Camera:** slow push (1.0→1.05). At 34.5 it starts an ease-in truck to the right.
- **Caption:** page 8.
- **VO:** "The gun was also proving unreliable,…"

### S18 · 34.50–35.25 · Truck right into the tower block; explosion cover
- **Motion:** the camera trucks right about 0.8 frame-widths (34.5–35.0, ease-in-out). F exits left, and the tall
  salmon apartment block fills the right side.
- **Transition (34.9–35.25):** an **explosion cover**. A large orange starburst explosion (8 long tapered points, orange
  #F7931E, yellow core #FFD34D, red #E8542A outer glow) **enters from the bottom-right corner, swings across and
  scales up** to about 600 px, passing over the frame. Under its cover the camera jumps down and right into S19, and the
  explosion exits at the bottom-left by 35.27.
- **VO:** "…with many guns quickly being…"

### S19 · 35.25–38.55 · Barricade: hedgehogs, barbed wire, two soldiers
- **On screen:** the pink apartment wall (cracked, windows blown open in dark plum) fills the top 55 %. A row of Czech
  hedgehogs (big crossed grey beams #625850 / #7A7068 with a lighter top stripe and rounded ends) runs across y≈760–900,
  with 4–5 strands of barbed wire (black lines with small X barbs #251716) between them. One soldier stands behind the
  wire aiming an AK-12 left (about (1170,450) in the 720 still), and one lies prone in front with an AK-12 (y≈760). Both
  wear RU patches. The street is #7A4F49.
- **Motion:**
  - The standing soldier fires a burst (flash flicker), and recoil kicks in.
  - The prone soldier crawls with a slow elbow-crawl loop (body slides about 30 px, legs alternate).
  - Small sparks pop off the hedgehogs.
- **Camera:** slow truck left→right (about 200 px over 3 s), linear.
- **Transition out (38.55–38.93):** an **organic blob matte wipe**. A beige (#E6C394) irregular shape with wobbly lobes
  grows from the top-left and the left edge, carrying the incoming armoury frame. A few small pink debris blobs (outgoing
  colour) fly off and fade along the matte edge.
- **Caption:** page 9 at 35.2 ("adapted to disable the / two - round burst fire / mode. So while the / AK - 12 is likely
  to").
- **VO:** "…adapted to disable the two-round burst fire mode."

## Scene block 7: The armoury (38.6–44.5)

Set: a warm sand interior, wall #E6C394 with large paler capsule "cloud" shapes #EDCCA4 / #EDD5AE as wall texture.
Black-and-yellow pallet-rack shelving (uprights #2B231E, beams #F2C12E) holds green ammo bags / sandbags #6E8E3A /
#4F6B2A and cardboard boxes #C39D60 with darker flaps #8B7953. A wooden issue table (top #DDB07D, legs #C39D60) holds
folded uniforms and green kit bags. The floor is #C39D60.

### S20 · 38.70–41.00 · Three soldiers queue; quartermaster officer issues rifles
- **On screen:** three soldiers (D-style moustache, A black beard, B brown goatee) stand in a line on the left (x 60–440
  scaled to 720, feet at y≈790). They have hand circles at their sides, and one scratches his head. An officer in a
  peaked field cap with rank stars on his shoulder boards and a chest ribbon bar leans over the table on the right,
  holding out a rifle. Shelves stand behind them.
- **Motion:**
  - The officer slides an AK across the table toward the first soldier, then lifts it (39.5–40.5).
  - The soldiers shift weight. The middle soldier talks, and the right one scratches his helmet (an arm loop).
- **Camera:** from 40.5, a push toward the centre-right with a +6° rotation, ease-in.
- **Caption:** page 9, then page 10 at 40.0 ("continue being Russia's / weapon of choice, as / opposed to the Cold War /
  - era AK-47, Russia has").
- **VO:** "So while the AK-12 is likely to continue being Russia's weapon of choice,…"

### S21 · 41.00–44.50 · MCU soldier B holding his newly issued rifle (tilted)
- **On screen:** soldier B (brown goatee, green eyes, mouth open in an "o") in MCU on the left. He holds a black AK
  vertically against his chest. The officer's arm and cap are cut off on the right edge, and the camo body fills the
  bottom half.
- **Motion:** after the push (41.0–41.8, scale 1.0→2.4, rotate +12°, ease-in-out), B talks with a slow head tilt.
- **Camera:** slow drift.
- **Transition out (44.43–44.80):** a **diagonal slash wipe** to purple, as at 21.97. The streaks at -30° carry the
  purple frame (#5836D2) and the outgoing image smears along them.
- **Caption:** page 10.
- **VO:** "…as opposed to the Cold War-era AK-47,…"

## Scene block 8: Russia ball robot (44.75–49.75)

### S22 · 44.75–47.20 · Russia countryball on robot legs juggling old rifles
- **On screen:** a flat purple BG #5836D2 with lighter diagonal rounded streaks #6541D5 (capsules about 40 px wide at
  45°) and a few dots, all drifting down and left slowly. In the centre (about (400–600, 380–780) scaled to 720) is a
  **Russia flag ball** (white #FFFFFF / blue #0C0B97 / red #F71617 bands) inside a thick dark-grey ring #3F3C45 with a
  lighter rim #615E64. It has two large soft highlight blobs (lighter blue and red overlays at about 30 %) on the lower
  half and a white eye-visor band (a rounded rectangle #E4E2E4 with two black pupils). Two segmented robot arms
  (capsule links #3F3C45 with #615E64 highlights) each hold an AK, an AK-47 with wood furniture on the left and an AK-12
  on the right. It stands on two segmented legs with tread-like feet.
- **Motion:**
  - The legs do a nervous shuffle (alternating lifts, 4 Hz).
  - The arms wave the rifles (±10° sine).
  - The ball bounces ±8 px.
  - A sweat drop (white teardrop) sits in the middle of the face from 46.0.
- **Camera:** static at first, then pushes in from 47.2.
- **Caption:** page 11 at 44.75 ("increasingly been going / back to the earlier / models of the rifle that / don't
  include some of").
- **VO:** "…Russia has increasingly been going back to the earlier models of the rifle…"

### S23 · 47.20–49.70 · Push-in to the ball's worried face
- **Motion:** the camera pushes slowly, then faster (scale 1.0→2.8, ease-in, 47.2–49.3), ending with the ball's
  face filling the frame. The brows (grey capsules) tilt up in worry, and the eyes dart left and right. The sweat drop
  slides down 20 px.
- **Transition out (49.70–50.10, 12 frames):** an **organic splatter matte**. The incoming Ukraine frame appears inside a
  small irregular splat at the ball's centre (about (640,700)) that grows fast with spiky, ink-like lobes. Long purple
  tendrils from the outgoing frame trail off at the bottom-left for 2–3 frames.
- **Caption:** page 12 at 48.4 ("the newest features. / All the while, modern / weaponry keeps pouring").
- **VO:** "…that don't include some of the newest features."

## Scene block 9: Ukrainian camp (50.0–56.0)

Set: a green hilly field. Sky #AEDDFA / #DCEFFD with many cloud groups, two Ukrainian flags (#0057B7 / #FFD700, in
the same rounded framed style as the RU flags) on poles, and a green watchtower #526F39 on the left. A green quonset
#648A42 / #526F39 has a navy door #2E3A5A, and a green military tent #4A6833 sits behind it. Grass is #7A8F28 /
#6E9649. In the foreground are olive ammo crates #6D7142 / #4E5338 with handles, latches and darker panel insets.

### S24 · 50.00–52.40 · Wide camp, a Ukrainian soldier behind the crates
- **On screen:** soldier G (brown beard, blue eyes, UA patch, multicam #A0A463 / #6D7142) peeks over the crates at
  centre-right, holding a rifle. The crates fill the bottom third.
- **Motion:** G pops up from behind a crate (51.5–52.0), lifts his M4/AR-style rifle into view and talks. The flags wave
  and the clouds drift.
- **Camera:** gentle push (1.0→1.05).
- **Caption:** page 12, then page 13 at 51.75 ("into Ukraine - making / Russia's new rifles look / outdated from moment
  one.").
- **VO:** "All the while, modern weaponry keeps pouring into Ukraine,…"

### S25 · 52.40–54.00 · Push and rotate toward G
- **Motion:** the camera pushes from wide to G at MCU (scale 1.0→3.0) while rotating about -15°, ease-in-out
  (52.4–53.8). The crates and hut slide past as foreground parallax (the crates move about 1.3× faster).
- **VO:** "…meaning Russia's new rifles look…"

### S26 · 54.00–56.00 · CU of G showing off his M4, sparkles (end)
- **On screen:** G in a tilted MCU on the right (grinning, white teeth), holding the M4/AR-15 (grey-black #3A3F45 /
  #555B63, flat-top rail, carry handle, curved mag) diagonally in both hand circles. The BG is plain dark green #4A6833.
- **FX:** big white 4-point sparkles. At 54.4 one appears at the top of the rifle (grows to about 500 px), a second smaller
  one at the receiver at 54.75, then one more at 55.1. Each scales 0→1→0 over about 0.5 s with a spin. There is a tiny
  sparkle on the receiver.
- **Motion:** G lifts the rifle proudly (+10° rotation, ease-out) and bobs his head.
- **Camera:** slow push and drift. The video **ends on this frame at 56.0 with no end card, logo or CTA**. The music
  fades out.
- **Caption:** page 13.
- **VO:** "…outdated from moment one."

---

## Transition index

| # | time | from → to | type | duration |
|---|---|---|---|---|
| 1 | 2.87 | S01 → S02 | silhouette matte (soldier shape, top-right, scale-up) | 10 f |
| 2 | 13.95 | S07 → S08 | silhouette matte (kneeling shooter, bottom-right) | 9 f |
| 3 | 21.97 | S12 → S13 | diagonal slash/streak wipe, -30°, directional smear | 10 f |
| 4 | 25.97 | S13 → S14 | iris from centre with soft refractive rim | 10 f |
| 5 | 32.43 | S16 → S17 | organic blob from the mouth/hand | 11 f |
| 6 | 34.90 | S18 → S19 | explosion starburst cover with a camera jump | 11 f |
| 7 | 38.55 | S19 → S20 | organic beige blob from top-left plus debris | 11 f |
| 8 | 44.43 | S21 → S22 | diagonal slash wipe to purple | 11 f |
| 9 | 49.70 | S23 → S24 | organic splatter from the face centre, with tendrils | 12 f |

Plus 8 large in-scene camera moves that change framing: 4.5 pull-out+rotate, 8.1 push+rotate, 11.5 pan, 16.0 truck,
19.9 push+rotate, 28.0 ECU push, 30.4 tilt-up, 41.0 push+rotate, 47.2 push, 52.4 push+rotate.

## Asset inventory for the remake

**Characters (8 rigs):** A, B, C, D, E/F (one rig with hair and patch swaps), G (UA), the blond squad soldier, the
officer (cap variant), a generic official (replacing the real-leader caricature) and the Russia ball robot.

**Guns (3):** AK-47, AK-12 (plain plus a with-accessories variant) and M4.

**Sets (8):** hook sunburst, RU base, firing range, office, grey ruins, pink ruins, armoury, purple BG, UA camp.

**Props:** clipboard, calendar, target, hedgehogs plus wire, crates, flags.

**FX:** 4-point sparkle, muzzle flash, explosion starburst, heart eyes, sweat drop.

**Transitions:** silhouette matte, blob/splatter matte, slash wipe, iris, explosion cover.
