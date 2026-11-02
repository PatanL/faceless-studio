# explainer-p1: shot plan

"How Long You'd Last in Every Prehistoric Ocean", 9:16, 1080×1920, 30 fps, kurz lane.

**Blender: no.** This plan is flat 2D in house style A, built in Remotion and SVG. Every frame of both Kurzgesagt
reference Shorts is flat vector art, 3D/Blender is parked (FEEDBACK_LOG 2026-11-01), and BRIEF rule 4 says every
visual is code. The realistic CGI look belongs to the Zack D. lane only.

Inputs: `episodes/explainer-p1/script.md` (final narration, 169 words), `refs/BREAKDOWN.md`, the WHALE and SALT
sheets in `refs/sheets/` (shot sizes and angles below were read off them by eye), `refs/data/*_events.json`
(measured pacing), docs/HOUSE_STYLE.md (style A) and REFERENCES_ANALYSIS §4.

**Timing basis.** There is no TTS yet. The times are estimates from a syllable model of Kokoro am_michael at
speed 1.1: past explainers at that speed ran 180–194 wpm with gaps, and this script has many one-word sentences, so
the model uses 179 wpm, first word at 0.15 s and last word "you" at 56.40 s, ending the video at **56.9 s**. Every
cut and event is **anchored to a word**, so re-timing to the real word timings is mechanical (see "Re-timing" below).
The script is 57 s, not the 75–90 s of the reference brief. The plan follows the script: four prehistoric rungs plus
today. If the episode is lengthened later, add rungs, not length per rung (PLAYBOOK 1b).

---

## 1. Targets: references vs this plan

Reference values were measured on every frame at native fps. Plan values are computed from the shot list below
(scratch stats script; recompute on the render with `frame_metrics.py`).

| Metric | WHALE | SALT | Plan |
|---|---|---|---|
| Shots / min | 10.7 | 20.2 | **22.1** (21 shots; 25.3 if the three 0.2 s rewind frames are counted) |
| Hard cuts / min | 6.0 | 10.1 | **11.6** (11 cuts). Without the 3-cut teaser burst taken from ERAS: 8 cuts in 50.9 s = **9.4 / min** |
| Wipes, whips, curtains | 11 in 151 s | 9 in 59.5 s | **9** + one rewind sequence |
| Median shot | 5.12 s | 2.23 s | **3.06 s**, mean 2.7 s |
| Longest shot | 15.2 s | 10.3 s | **5.3 s**, with the camera travelling the whole time; no static hold over ~2.1 s |
| Median gap between visual events (detector scale: shot changes, camera travel, large arrivals) | 2.03 s | 1.40 s | **1.58 s** (max 3.1 s). Counting every tag, pill and chip as well: 0.70 s |
| Setting changes | — | — | **10** in 57 s (Cambrian surface, Cambrian underwater, Devonian, Cretaceous aerial, Cretaceous underwater and surface, Miocene, modern coast, coast from below, rewind, frame 0) |
| Frame 0 | cover | black 0.27 s | **cover** |
| Ending | rewind, then half-line | bookend + subscribe card | rewind lands on frame 0 on "hunter", ends 0.5 s after "you" |

"Cut at least as often as the references": shots per minute beat SALT, the faster reference, and hard cuts per minute
match SALT outside the teaser burst. The median shot (3.06 s) sits between SALT (2.23 s) and WHALE (5.12 s). That is
because the rung establishing shots carry continuous camera travel instead of extra cuts, the way WHALE's dive
(59–74 s) and SALT's surface-to-floor sink (37–44 s) do.

## 2. Shot grammar: sizes and angles

**What the references do** (approximate, counted by eye from the 0.5 s sheets):

| | WHALE, 27 shots | SALT, 20 shots |
|---|---|---|
| Wide, aerial, top-down, map | ~8 (jungle aerial, Pangaea, the crowd of whales) | ~9 (beach, map, isometric tile, river, coast) |
| Medium, full-body side profile | ~8 (Pakicetus, Ambulocetus) | ~4 (seabed, the bird at the surface) |
| Close-up, extreme close-up, macro | ~7 (whale head with diver, x-ray, ear bone, magnifier, head at the waterline) | ~5 (raindrop, rock, bird close-up) |
| Flat board | ~4 (yellow board, blueprint, lineage mobile, evidence board) | ~2 |
| **Low angle from below** | 3: the whale head with a tiny diver (12.8 s), Protocetus rising to the surface (68 s), the blue whale (96 s). Always a big animal near something small, or rising to the surface | ~1 |
| **Split waterline at eye level** | 3–4 (28 s, 33.5 s, 91 s) | 1 (37.5 s, then the camera sinks) |
| High angle, top-down | ~5 | ~9 |

**Our grammar.** The premise is a person treading water while every threat comes from below, so the references'
own low-angle trigger (a big animal near a small human) recurs on every rung. The angles therefore follow these
rules:

- **Low angle from below (7 shots):** used only when a predator is close to You (S03, S06, S10, S11, S14, S19), plus
  S20, the payoff, which frames You exactly the way every predator was framed.
- **Split waterline at eye level (5 shots: S01, S08, S13, S18, S22):** the "you, treading water" home frame. It
  repeats each time the verdict lands on You.
- **High angle (2 shots, S05 and S12, plus 2 map insets):** used for arriving somewhere: dropping into the sea and
  flying into the Cretaceous sea.
- **Extreme close-up or macro (5 shots: S02, S04, S07, S10, S17):** the teasers and each rung's mechanism slot
  (the shell, the jaw blades, the shark's eye), as in WHALE's x-ray and magnifier.
- **No flat boards.** Every beat here is a place. Comparators (car, bus, hand) enter the world as same-scale
  silhouettes on their word and leave with the beat (REFERENCES_ANALYSIS rule 14).

Sizes across the 21 shots: 7 wide (33 %), 5 medium (24 %), 4 close-up (19 %), 5 extreme close-up (24 %). That is
about the references' wide-to-medium split, but with more close-ups, because the Short is about how close the
threat gets.

## 3. Screen layout (1080×1920; keep everything out of the right 12 % below 55 %, where the Shorts buttons sit)

| Band (% of height) | What sits there |
|---|---|
| 8–13 | **TimeScrubber**: a horizontal bar with 5 evenly spaced ticks (508 · 360 · 70 · 15 · TODAY), a handle, and a survival chip riding the handle. Small "NOT TO SCALE" under the bar on its first reveal only. On screen from frame 0. |
| 15–21 | **Era tag**: big, orange, solid (WHALE's "EOCENE" tag). It appears on the rung word, holds ~1.2 s, then shrinks and **docks into its scrubber tick**, which clears the band for the pill. |
| 23–27 | **Name pill**: solid colour, never a gradient (style A has no gradients; WHALE's pills are gradients), 0.15 s after the name. |
| 30–66 | Subject zone: creatures, comparators, number tags on pointer lines pinned to the object (never on a face). |
| 70–78 | **Captions**: whole phrases of 1–3 words, small, white with a thin outline, fixed at ~74 %. No tag or inset may enter this band. |

Verdict chips: HOURS = sea green `#0bd4a4`, MINUTES = orange `#fc6e0e`, SECONDS = red `#fa302a`, HOURS? = sun yellow
`#fddf35`. Each chip carries a small "BEST GUESS" tag.

---

## 4. Shot plan, line by line

Columns: **In** is how the shot starts and the word it lands on (CUT = a one-frame hard cut on the word's onset).
**Est.** is the estimated start–end in seconds. **Size and angle**: EWS/WS/MS/CU/ECU, then the camera height.
**L\*** is the target mean lightness, so each setting change shows (a jump of at least 10 in CIEDE76, REFERENCES_ANALYSIS rule 5).
**What moves** lists each word, its estimated time, and what happens on it.

### Line 1, 0.15–3.10: "The ocean's scariest hunter was once as long as your arm."

| Shot | In | Est. | Dur | Size and angle | Setting, palette, L\* | What moves |
|---|---|---|---|---|---|---|
| **S01** | frame 0 = the cover | 0.00–4.47 | 4.47 | MS moving to CU. Split waterline at eye level: sky in the top ~38 %, the line just below your chin | Cambrian shallows: aqua and sea-green water, pale sand, sponges, bare grey rock shore far back, no fish, coral or plants. L\* ≈ 75 | **f0** is a finished image: You, head and shoulders above the water, left arm stretched out just under the surface. Anomalocaris lies along the arm, the same length, its appendages curled. Scrubber handle on tick 1 ("508 MILLION YEARS AGO"), chip "?:??". Camera has pre-roll, so frame 1 is already moving: a slow push-in and tilt down along the arm, reaching a CU of arm plus animal by ~2.9 s. **"scariest"** 0.74: the appendages flare open. **"hunter"** 1.32: pill ANOMALOCARIS at 1.47 (it is never spoken; the pill names it). **"arm"** 2.88: a bracket from shoulder to fingertip, and the tag "~60 cm" on a pointer to the animal (the first proof lands by 3 s). |

### Line 2, 3.50–7.10: "Then the ocean grew armour, then jaws, then teeth the size of your hand."

Three teasers, one hard cut each, most famous last. Each is in its own rung's palette and darker than the last
(L\* 50 → 45 → 35), so the ladder's descent into danger is visible before it is explained.

| Shot | In | Est. | Dur | Size and angle | Setting, palette, L\* | What moves |
|---|---|---|---|---|---|---|
| S01 (cont.) | | | | | | **"Then"** 3.50: the scrubber handle twitches one notch right and snaps back. **"grew"** 4.28: a shadow far bigger than Anomalocaris slides through the bottom of the frame. |
| **S02** | CUT "armour" | 4.47–5.18 | 0.71 | ECU, low three-quarter front: Dunkleosteus's head shield fills the frame | Devonian, murky blue-green. L\* ≈ 50 | The plates glide past camera from left to right; one flat glint sweeps across the shield on the word. |
| **S03** | CUT "jaws" | 5.18–5.69 | 0.51 | CU, low angle from below; bright surface band at the top | Cretaceous, royal blue. L\* ≈ 45 | The mosasaur's jaw opens toward the lens on the word (fully open in 0.3 s). No contact. |
| **S04** | CUT "teeth" | 5.69–7.28 | 1.59 | ECU insert at eye level on a plain field | Miocene, royal blue to indigo. L\* ≈ 35 | One megalodon tooth drops in and settles on **"teeth"**. **"size"** 6.08: an open human hand slides up from the bottom beside it. **"hand"** 6.66: the outlines line up; tag "~18 cm". |

### Line 3, 7.28–12.50: "Drop into each ocean. No boat, just you, treading water. How long until something eats you?"

The progress device is fully readable by 8.1 s (target: by 9 s).

| Shot | In | Est. | Dur | Size and angle | Setting, palette, L\* | What moves |
|---|---|---|---|---|---|---|
| **S05** | WHIP DOWN on "Drop" (0.3 s, flat speed lines, no blur) | 7.28–11.63 | 4.35 | WS from a high angle (~60° down), then the camera descends to an MS at the waterline, at eye level | Cambrian surface, sky-cyan water. L\* ≈ 75 | **"Drop"**: You fall into frame from the top. **"ocean"** 8.06: a flat splash ring, while the scrubber's 5 ticks pop in from left to right ("each ocean") with "NOT TO SCALE". **"No boat"** 8.75: a boat icon flies in beside You; on **"boat,"** 8.95 it gets a red slash and drops away. **"just you"** 9.26–9.46: the descent ends on a split-waterline MS with You centred. **"treading water"** 9.77: the legs kick below the line (a loop that keeps running). **"How long"** 10.85: the chip pulses "?:??" and a small clock icon ticks. |
| **S06** | CUT "something" | 11.63–16.95 | 5.32 (the camera moves throughout) | MS from a low angle below, looking up at your dangling legs; levels to eye level, then tilts down to the floor | Cambrian underwater: aqua near the surface, sea green toward the floor. L\* ≈ 70 | **"eats"** 12.02: a dark shape slides across the lower frame. *(Line 4 starts.)* **"Half a billion years ago"** 13.03: the orange era tag "508 MILLION YEARS AGO" slams in, then docks into tick 1 at ~14.2. At 13.8 the camera levels to eye level and Anomalocaris rises into full view beside your legs, at the size of your arm again. **"Nothing can"** 14.50: it eyes you, then turns away. At 15.4 the camera tilts down after it to the sand: sponges and a trilobite. |

### Line 4, 12.83–19.40: "Half a billion years ago? Nothing can. It probably couldn't even crack a shell. You last until your arms give out."

Rung 1 fills the four slots: era tag (S06, in place, because we never left), place (S05–S06), predator plus
comparator (your arm), verdict (S08).

| Shot | In | Est. | Dur | Size and angle | Setting, palette, L\* | What moves |
|---|---|---|---|---|---|---|
| S06 (cont.) | | | | | | (see above) |
| **S07** | CUT "crack" | 16.95–17.83 | 0.88 | ECU macro, side view at eye level: appendages on a trilobite's shell | Cambrian floor, pale sand. L\* ≈ 65 | The appendages close on the shell; **"shell"** 17.34: they buckle and bounce off (flat arc lines), and the trilobite scuttles out of frame. The mechanism slot. |
| **S08** | WHIP UP on "You" (0.3 s; the camera rises through the surface) | 17.83–19.81 | 1.98 | CU, split waterline at eye level: your head and stroking arms | Cambrian surface. L\* 75 → 68 | **"last until"** 18.2: the sun arcs across the sky band and the sky steps one shade warmer (hours passing); your strokes slow. **"give out"** 19.00: your arms sag and your chin dips. 19.20: the chip snaps to **HOURS** (sea green) + BEST GUESS (sfx: pop). |

### Line 5, 19.81–28.10: "Armour. Dunkleosteus, a fish as long as a car, with bone blades instead of teeth, built to crack other armoured fish. You're not armoured. Minutes."

| Shot | In | Est. | Dur | Size and angle | Setting, palette, L\* | What moves |
|---|---|---|---|---|---|---|
| **S09** | CURTAIN on "Armour" (a flat curtain closes over S08 from 19.6 and parts on the word, 0.5 s) | 19.81–23.28 | 3.47 | WS at eye level underwater, slow push-in | Late Devonian inland sea: blue-green, muddy floor, a few small placoderms in the far layer. L\* ≈ 55 | The curtain parts on the era tag "360 MILLION YEARS AGO", and the handle slides to tick 2. 20.2: a map-inset circle (upper left, below the tag band) shows Late Devonian continents with a pin on the shallow sea over today's Ohio (place slot). **"Dunkleosteus"** 20.50: it glides in from the right; pill DUNKLEOSTEUS at 20.65; the era tag docks at ~21.0. **"car"** 22.77: a flat car silhouette drops in below it at the same scale (kit `Car`); tag "~3.4 m". |
| **S10** | X-RAY IRIS on "bone" (0.3 s, a circular reveal opening from the head) | 23.28–26.63 | 3.35 | ECU, low three-quarter front on the head in x-ray view, then a fast pull-out to an MCU side view | Same sea; the x-ray view is orange bone on dark plum (WHALE's x-ray), then back to normal. L\* ≈ 50 | **"blades"** 23.47: a yellow highlight ring outlines the jaw blades. **"instead of teeth"** 23.87: a small tooth icon gets a red slash beside the ring. **"built"** 24.77: x-ray off, and the camera pulls out to an MCU as a smaller armoured fish crosses. **"crack"** 25.16: the jaws snap shut on it and flat plate shards fly (no blood). The mechanism slot. |
| **S11** | CUT "You're" | 26.63–28.52 | 1.89 | MS from a low angle below: You silhouetted against the bright surface; Dunkleosteus rises toward you from the bottom of the frame | The same sea seen from below, darker. L\* ≈ 45 | **"not armoured"** 26.82: a thin outline sweeps over your torso; tag "NO ARMOUR" (red ✕) pinned at your side. **"Minutes"** 27.71: chip **MINUTES** (orange) + BEST GUESS (sfx: impact). Its jaw starts to open; the wipe comes before any contact. |

### Line 6, 28.52–36.20: "Jaws. Mosasaurus, a sea lizard as long as a bus. It breathes air, so it keeps surfacing, right where you're treading water. Seconds."

| Shot | In | Est. | Dur | Size and angle | Setting, palette, L\* | What moves |
|---|---|---|---|---|---|---|
| **S12** | DIAGONAL WIPE on "Jaws" (0.45 s, a hard-edged diagonal from bottom left to top right) | 28.52–32.16 | 3.64 | WS from a high angle (horizon at ~18 %), then the camera swoops down through the surface to an MS side profile underwater at eye level | Late Cretaceous shallow sea at sunset: royal-blue water under an orange-to-magenta sky band. L\* ≈ 62 | Era tag "70 MILLION YEARS AGO"; the handle moves to tick 3. 28.9: map inset of Late Cretaceous Europe's archipelago, pinned near Maastricht. **"Mosasaurus"** 29.01: a long shadow moves under the surface; pill MOSASAURUS at 29.16. **"sea lizard"** 30.11: the camera dives through the surface (the waterline passes up the frame) into a side profile: lizard body, flippers, tail fluke; an ammonite and a sea turtle in the mid layer. **"bus"** 31.47: a bus silhouette (kit `Bus`, ghost outline) slides in alongside at the same length; tag "~12 m". |
| **S13** | WATER-LINE WIPE UP on "breathes" (kit `wipe` up, 0.35 s; the camera breaks the surface) | 32.16–35.63 | 3.47 | CU, split waterline at eye level, then a whip-pan right to an MS | Sunset surface. L\* ≈ 62 | The snout breaks the surface; **"air"** 32.36: the nostrils puff a flat spray ring. **"keeps surfacing"** 33.07: the snout dips under and comes up again, closer. **"right where you're"** 33.97: the camera whip-pans right along the waterline to You in an MS in the foreground, the snout surfacing ~3 m behind you. **"treading water"** 34.55: your legs kick below the line; you haven't seen it. |
| **S14** | CUT "Seconds" | 35.63–36.44 | 0.81 | CU from a low angle below, silhouette | Indigo and violet. L\* ≈ 25 (the darkest frame in the video) | Only the closing jaws, as a silhouette rising under your legs. 35.78: chip **SECONDS** (red) + BEST GUESS (sfx: impact). The wipe comes while the jaw is 80 % closed: no contact. |

### Line 7, 36.44–42.60: "Teeth. Megalodon, longer than a bus. But it hunted whales. Would it even bother with a crumb like you?"

| Shot | In | Est. | Dur | Size and angle | Setting, palette, L\* | What moves |
|---|---|---|---|---|---|---|
| **S15** | DIAGONAL WIPE on "Teeth" (same wipe as S12; the edge runs the other way) | 36.44–39.50 | 3.06 | WS at eye level in open water, slow pull-out | Miocene open ocean with no floor: royal-blue bands deepening to indigo. L\* ≈ 45 | Era tag "15 MILLION YEARS AGO"; the handle moves to tick 4. **"Megalodon"** 36.94: it rises into frame from the lower left and turns into profile; pill MEGALODON at 37.09. **"longer than a bus"** 37.84: the same bus ghost slides in under it; **"bus"** 38.62: the bus is visibly shorter; a bracket and tag "~15–18 m". |
| **S16** | CUT "hunted" | 39.50–42.96 | 3.46 | WS at eye level, then a fast pull-back to EWS | Same ocean. L\* ≈ 48 | **"whales"** 39.89: a small Miocene baleen whale crosses mid-frame and the shark turns toward it (no bite). **"Would it even bother"** 40.39: the camera pulls back hard and everything shrinks; a speck at the surface, top right, is you. **"crumb"** 41.95: a magnifier circle pops onto the speck and shows You treading water (WHALE's magnifier). **"you?"** 42.34: the shark's body angles slightly toward the speck. |

### Line 8, 42.96–45.00: "Nobody really knows. Hours, maybe."

The turn starts on "But it hunted whales" (39.1 s, 69 %) and resolves here (43.0 s, 75 %). The script estimated
~62 %. The favourite falls, and the honesty beat gets its own shot (WHALE 106 s).

| Shot | In | Est. | Dur | Size and angle | Setting, palette, L\* | What moves |
|---|---|---|---|---|---|---|
| **S17** | CUT "Nobody" | 42.96–45.75 | 2.79 | ECU of the shark's eye, at eye level | Miocene. L\* ≈ 35 | 43.1: the eye swivels toward camera (toward you) and a white "?" tag appears. **"knows"** 43.93: the eye swivels away, and a "NOT KNOWN" stamp lands. **"Hours, maybe"** 44.43: chip **HOURS?** (yellow) + BEST GUESS. |

### Line 9, 45.55–50.40: "Now jump to today. Sharks kill about six people a year. You'd last until your arms give out."

| Shot | In | Est. | Dur | Size and angle | Setting, palette, L\* | What moves |
|---|---|---|---|---|---|---|
| **S18** | WHIP RIGHT on "jump" (0.39 s across "jump to", landing on "today"; the scrubber ticks streak past as flat speed lines) | 45.75–50.87 | 5.12 (the camera moves throughout) | WS, split waterline at eye level, then a push-in to a CU of You | Modern coast: sky cyan and sun yellow, a beach and lighthouse in the far layer. L\* ≈ 78 (back to the brightest) | (sfx: whoosh on "jump".) **"today"** 46.14: era tag "TODAY"; the handle sits on the last tick. **"Sharks"** 46.83: a modern shark (kit `GreatWhite`, small, no pill because it is not a named species) passes under you and ignores you. **"six people"** 47.61: tag "≈6 PEOPLE / YEAR" with six person icons popping in a row, and the small sub-line "unprovoked, 5-yr avg". **"You'd last"** 48.88: the camera pushes in to a CU of You with **the same framing as S08** (the callback), and the sun arcs again. **"give out"** 50.06: the chip flips to **HOURS** (sea green), and the Cambrian tick lights the same green. |

### Line 10, 50.87–53.90: "Meanwhile, we kill about a hundred million sharks a year."

| Shot | In | Est. | Dur | Size and angle | Setting, palette, L\* | What moves |
|---|---|---|---|---|---|---|
| **S19** | CUT "Meanwhile" | 50.87–54.14 | 3.27 | WS from a low angle below: the shark's view up toward the surface | The coast from below: cyan surface. L\* ≈ 65 → 55 | A fishing boat's hull is a silhouette at the surface. **"we"** 51.38: a longline with baited hooks drops through the water; **"kill"** 51.57: the hooks swing in. **"hundred million"** 52.35: counter tag "≈100 MILLION / YEAR" counts up fast, with the sub-tag "ESTIMATE". **"sharks"** 53.13: flat shark icons fill rows across the lower frame (no gore, no fins). The lightness drops one step. |

### Line 11, 54.14–56.65: "Today, the ocean's scariest hunter is you."

| Shot | In | Est. | Dur | Size and angle | Setting, palette, L\* | What moves |
|---|---|---|---|---|---|---|
| **S20** | CUT "Today," (sfx: stinger 0.1 s before) | 54.14–55.23 | 1.09 | MS from a low angle below: **the predator framing** from S06, S11 and S14, now on You | The modern coast from below, bright. L\* ≈ 70 | You are silhouetted against the surface; the kick slows, and the shot holds still and ominous. |
| **S21** | REWIND on "scariest" | 55.23–55.82 | 0.59 | Three frames reused from earlier shots, 0.2 s each | Palettes in reverse order | A ⏪ icon in the centre, and the scrubber handle sweeps left. The frames step back: S15 Megalodon (55.23), S12 Mosasaurus (55.43), S09 Dunkleosteus (55.63). WHALE's rewind (137–151 s), compressed. |
| **S22** | lands on "hunter" | 55.82–56.90 | 1.08 | **The exact frame-0 composition of S01** | Cambrian. L\* ≈ 75 | The chip is back to "?:??". 55.97: pill **"YOU"** pops in the ANOMALOCARIS pill's slot and style, over You. **"you"** 56.40: hold. Over the last 3 frames the pill scales out, so **the last frame equals frame 0** and the loop restarts on "The ocean's scariest hunter…". The video ends 0.5 s after "you" starts (the Shorts median is 0.5 s). |

---

## 5. All shots at a glance

| Shot | Line | In | Start | Dur | Size | Angle | Setting |
|---|---|---|---|---|---|---|---|
| S01 | 1–2 | cover | 0.00 | 4.47 | MS → CU | split waterline, eye level | Cambrian surface |
| S02 | 2 | cut | 4.47 | 0.71 | ECU | low three-quarter | Devonian teaser |
| S03 | 2 | cut | 5.18 | 0.51 | CU | low, from below | Cretaceous teaser |
| S04 | 2 | cut | 5.69 | 1.59 | ECU | eye level | Miocene teaser |
| S05 | 3 | whip down | 7.28 | 4.35 | WS → MS | high, descending to waterline | Cambrian surface |
| S06 | 3–4 | cut | 11.63 | 5.32 | MS | low → eye level → tilt down | Cambrian underwater |
| S07 | 4 | cut | 16.95 | 0.88 | ECU | eye level, macro | Cambrian floor |
| S08 | 4 | whip up | 17.83 | 1.98 | CU | split waterline | Cambrian surface |
| S09 | 5 | curtain | 19.81 | 3.47 | WS | eye level, push-in | Devonian sea |
| S10 | 5 | x-ray iris | 23.28 | 3.35 | ECU → MCU | low three-quarter → eye level | Devonian sea (x-ray) |
| S11 | 5 | cut | 26.63 | 1.89 | MS | low, from below | Devonian, below |
| S12 | 6 | diagonal wipe | 28.52 | 3.64 | WS → MS | high aerial → dives in | Cretaceous sunset sea |
| S13 | 6 | water-line wipe | 32.16 | 3.47 | CU → MS | split waterline, whip-pan | Cretaceous surface |
| S14 | 6 | cut | 35.63 | 0.81 | CU | low, from below | Cretaceous, dark |
| S15 | 7 | diagonal wipe | 36.44 | 3.06 | WS | eye level, pull-out | Miocene open ocean |
| S16 | 7 | cut | 39.50 | 3.46 | WS → EWS | eye level, pull-back | Miocene open ocean |
| S17 | 8 | cut | 42.96 | 2.79 | ECU | eye level | Miocene (eye) |
| S18 | 9 | whip right | 45.75 | 5.12 | WS → CU | split waterline, push-in | modern coast |
| S19 | 10 | cut | 50.87 | 3.27 | WS | low, from below | modern coast, below |
| S20 | 11 | cut | 54.14 | 1.09 | MS | low, from below | modern coast, below |
| S21 | 11 | rewind | 55.23 | 0.59 | (reused frames) | — | reverse |
| S22 | 11 | rewind lands | 55.82 | 1.08 | MS (= f0) | split waterline | Cambrian surface |

Hard cuts (11, all on word onsets): armour, jaws, teeth, something, crack, You're, Seconds, hunted, Nobody,
Meanwhile, Today. Transitions (9 + rewind): whip down (Drop), whip up (You), curtain (Armour), x-ray iris (bone),
diagonal wipe (Jaws), water-line wipe (breathes), diagonal wipe (Teeth), whip right (jump), rewind (scariest).
The era rungs always open on a transition (the curtain or a wipe, the brief's era-tag slot), and the threat beats
always open on a hard cut.

## 6. Continuity

- **You:** one design in every shot: style A, bare head, a plain swimsuit, no gear (the script says "No boat,
  just you"). The kit's `You` has no treading pose; add a `tread` pose (bicycle kick, sculling arms) in an
  episode-local figure rather than editing `people.tsx`. The same face and colours appear in S01, S05, S08, S11, S13,
  S16 (inside the magnifier), S18, S20 and S22.
- **Scrubber:** on screen in every shot except the ECU teasers S02–S04 and the S07 macro, where it stays but dims to
  40 %. The handle only moves on the rung words (Armour, Jaws, Teeth, jump) and in the rewind.
- **Comparators** are always flat, same-scale silhouettes that arrive on their word and leave with the beat: arm (your
  own), hand (S04), car (S09), bus (S12, S15, the same asset both times so the comparison reads), you as a speck (S16).
- **Predators never touch You.** Every threat shot cuts or wipes before contact (S11, S14, S16).
- **Habitat logic** (FEEDBACK P2): the Cambrian has no fish, coral or land plants; the Devonian has placoderms and a
  muddy floor; the Cretaceous has an ammonite and a turtle; the Miocene has no floor and a baleen whale; the modern
  coast has a beach and a lighthouse. Nothing crosses eras except You and the rewind.
- **Lightness path:** 75 (Cambrian) → 55/50/45 (Devonian) → 62 → 25 (Cretaceous, falling to the darkest beat) →
  45/35 (Miocene) → 78/65/70 (today) → 75 (frame 0). Every setting change jumps ≥ 10 L\* or changes hue family.

## 7. Sound tied to picture (from the script's markers; KURZ_MUSIC §8.2 and §8.7)

Six tonal SFX in 57 s (~6/min, matching Kurzgesagt's ~5/min). There is no whoosh on every cut: whoosh on S05 "Drop" and on S18 "jump";
pop on the HOURS chip at 19.2; impact on "Minutes" and on "Seconds"; stinger 0.1 s before "Today,". The score runs
at level from frame 0, in four sections that change on the transitions: 0–12.8 (hook and rules), 12.8–28.5
(rungs 1–2), 28.5–45.75 (rungs 3–4 and the turn, darkest), 45.75–end (today and the twist). It runs to the end at
level so the loop is seamless.

## 8. What to build (episode-local unless noted; shared kit/core files get small targeted edits only)

- **New components:** `TimeScrubber` (ticks, handle, chip, NOT TO SCALE, tick light-up, rewind mode); `EraTag`
  (orange, with the dock-to-tick move); a solid `NamePill`; the verdict chip with BEST GUESS.
- **Transitions the core does not have:** the core has `cut`, `fade`, `dipBlack`, `whip`, `iris`, `wipe` (wavy
  water line) and `glitch`. Needed: a **hard-edged diagonal wipe**, a **curtain**, an **x-ray iris**, a **rewind
  step**, and a **whip without Gaussian blur** (the core `whip` blurs, and style A forbids blur; use flat speed
  lines). The water-line `wipe` is used as-is for S13. Build these as episode-local overlay layers, or add them to
  `core/transitions.tsx` as small targeted additions, and say so in the commit.
- **New art (style A):** Anomalocaris (appendage rig), trilobite, sponges, Dunkleosteus (jaw rig plus an x-ray
  layer), a small armoured prey fish, Mosasaurus (jaw rig, nostril spray), ammonite, sea turtle, Megalodon (eye
  rig), a small Miocene baleen whale, a megalodon tooth, a hand, a boat icon, a fishing hull and longline, person
  and shark icons, the Cambrian bare-rock shore, a beach and lighthouse far layer, and the curtain.
- **Kit reuse:** `Car`, `Bus`, `GreatWhite` (modern shark), `Tag` with `leader` (pointer tags), `MapView` (insets,
  with paleo outlines), `Ocean` with `surface` (split waterline).

## 9. Re-timing to the TTS

1. Load the real word timings (`audio/captions.json` words). Put every **hard cut on the first frame at or before
   its anchor word's onset** (≤ 1 frame early). Transitions are centred so that the incoming shot is fully on screen by the
   word's onset.
2. Pills go at onset + 0.15 s, chips at onset, and camera moves start at their anchor word.
3. If a shot falls under 0.4 s after re-timing (the S03 teaser is the risk), keep it: one frame per teaser is
   allowed down to 0.3 s. Below that, merge S03 into S02 with a whip.
4. S21 needs ≥ 0.5 s between "scariest" and "hunter". If the TTS is faster, start the rewind on "ocean's" instead.
5. Re-measure the render with `research/frame-analysis/tools/frame_metrics.py` against section 1. Pass if:
   shots/min ≥ 20, hard cuts 10–12/min, median visual-event gap 1.4–2.0 s, no static stretch over 4.5 s,
   frame 0 not black, and the last frame matches frame 0 (mean |Δ| < 2 %).

## 10. Changes from the script's shot notes, and open flags

- **More cuts:** 11 (the script had 9), with new hard cuts on "something", "crack", "hunted" and "Nobody". "Drop" is a
  whip down and "today" is the landing of a whip right (the motion says the words).
- **The loop lands on "hunter", not on "you".** "is" to "you" is ~0.2 s, too short for a rewind, so the rewind runs on
  "scariest" and the YOU pill lands on the frame-0 composition. The last line then reads over the image it mirrors.
- **"breathes air"** enters through the camera crossing the waterline (the kit's water-line wipe) instead of a cut.
- **The pills are solid, not gradients** (style A). The era tag docks into the scrubber so the tag and pill bands
  never collide.
- **Flag, the turn's position:** under this timing model the turn runs from "But it hunted whales" (69 %) to
  "Nobody really knows" (75 %), not ~62 %. That is late for a PLAYBOOK turn (58–66 %). If the
  TTS confirms it, the writer could trim rung 1 (for example, drop "It probably couldn't even crack a shell", which
  saves ~2 s and S07), or this stays as is.
- **Visual fact checks:** the paleo-map outlines in the S09 inset (Late Devonian, Ohio sea) and the S12 inset (Late
  Cretaceous Europe, Maastricht); the tooth-to-hand scale (~18 cm); evenly spaced scrubber ticks (labelled NOT TO
  SCALE); the modern shark kept unnamed. The "~60 cm", "~3.4 m", "~12 m" and "~15–18 m" tags come from the
  script's fact list.
