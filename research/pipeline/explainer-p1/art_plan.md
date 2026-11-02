# explainer-p1: art plan (kurz lane, house style A)

Art director's plan for `episodes/explainer-p1/script.md` ("How Long You'd Last in Every Prehistoric Ocean", 9:16,
~56-60 s). It covers the settings, the look of each setting, what is a Codex plate and what is built in code, and the
pieces still to build. Everything on screen stays ours (FEEDBACK P7, BRIEF rule 5).

## 0. Blender: no

The answer is no. This is a Kurzgesagt-type Short, so it uses flat 2D house style A, built in Remotion and SVG.

- Every frame of WHALE and SALT is flat vector art (refs/BREAKDOWN.md §6).
- 3D/Blender is parked (docs/FEEDBACK_LOG.md, 2026-11-01).
- The realistic CGI variant belongs only to the Zack D. lane (docs/HOUSE_STYLE.md).

The Codex plates below are style-A art, vectorized and placed as layers. No 3D is involved anywhere.

## 1. The look: one flat world, five oceans

Every rung is a new place with its own palette and lightness. Viewers should be able to tell the era from the
background alone, even during the 0.2 s rewind frames.

| Era (rung) | Place | Palette (style A swatches) | Light | Measured L* (plate / water band) | Era accent (curtain, era tag rim, scrubber tick) |
|---|---|---|---|---|---|
| Cambrian, 508 Ma (hook, rung 1, loop) | Sunlit shallows by a barren rock shore. The land has no life yet. | aqua `#0de9e0`, sea green, pale sand, lavender-grey rock; violet and orange sponges | day, the brightest | 83 / 82 | aqua `#0de9e0` |
| Late Devonian, 360 Ma | Murky inland sea over oxygen-poor mud: almost empty, a few crinoids and shells | teal and blue-green bands, low contrast, olive mud | overcast | 40 / 40 | sea green `#0bd4a4` |
| Late Cretaceous, 70 Ma | Warm shallow sea at sunset with a far low island of conifers | royal blue and violet water; orange, magenta and violet sky; yellow sun with one halo ring | dusk | 35 / 28, the darkest water | orange `#fc6e0e` |
| Miocene, 15 Ma | Open ocean far from any coast: no floor, rays fade out before mid-frame | cyan just under the surface, royal blue, then indigo and violet | day, at 40 m | 40 / 40, with the lower half near 25 | violet `#932efc` |
| Today | A beach coast with green hills and a small lighthouse | sky cyan, sun yellow, golden sand, green seagrass | day, bright again | 74 / 71 | sun yellow `#fddf35` |
| Today, from below (s10) | The shark's view up at the surface | sky cyan to royal blue | day, one step darker | 54 | (same as today) |

The lightness ladder runs 83 → 40 → 28 (water) → 40 → 74. The water gets darker as the predators get worse, the
Cretaceous "Seconds" beat is the darkest, and today returns to the hook's brightness. The Miocene plate is lit by
its surface band. Frame the Miocene shots on the lower two thirds (L* about 25-30) except when YOU is shown at the
surface. That keeps the "crumb" beat dark and makes the whale's arrival stand out.

The mean-colour difference between neighbouring rungs is CIEDE76 30-80, which is well above the ≥ 10 that
REFERENCES_ANALYSIS rule 5 requires. Cambrian split to Cambrian floor is only 1.6, so it is planned as one setting
seen from a new camera position (same `place`, same depth band), not as a setting change.

Measurements are in `plates.json` (`tools/plate_prep.py`).

**World rules for this episode** (FEEDBACK P2):
- **No modern life before "today".** No fish schools, kelp, coral, jellies or seals in a prehistoric rung, and no
  fish at all in the Cambrian. That is why there are two new biomes (§2), which have no modern dressing.
- **Era props only on their rung:** sponges and microbial mounds in the Cambrian; crinoids and brachiopod shells in
  the Devonian; ammonite, sea turtle and conifer island in the Cretaceous; a small baleen whale in the Miocene;
  seagrass, lighthouse, fishing boat and longline today.
- **Cambrian shore:** bare rock, with no plant on land.
- **Mosasaurus:** an air breather, so it is shown surfacing (script line). Show its nostrils and a flat spray ring,
  never a blowhole spout.
- **Miocene whale:** a small cetothere-like baleen whale, about 6-8 m. Do **not** use `explainer/BlueWhale`: a
  25 m blue whale would dwarf a 15-18 m megalodon, break the size ladder, and is the wrong era.
- **Comparators:** the car and the bus are ghost silhouettes and appear only on their word (§4).

## 2. Settings

The paste-ready settings, one entry per narration paragraph, are in **`settings_plan.json`**. They use the
`pipeline/episodes/settings.py` schema, with "@word" anchors that `settings.fill()` resolves against the TTS word
timings.

I validated them against synthetic 190 wpm word timings:
- `settings.validate` reports OK.
- There are 25 setting runs in ~58 s, about 25 changes a minute. The references manage 5-8, and our MIN_PER_MIN is
  5: a Short's era ladder changes on every rung.
- The longest run is 7.5 s: the Miocene, s7-s9, where the camera keeps moving.
- The comparator (analogy) windows last 1.3-1.9 s.

**New biomes (small targeted edit to `pipeline/episodes/settings.py`, shared core):**
- `prehistoric_shallows`: water and floor, 0-60 m, keys tide/sky/kelp/mid. Dressing is limited to Rocks, Seabed,
  Specks and Ridge, with no ambient species.
- `prehistoric_open`: water with no floor, 0-200 m, keys royal/tide/mid/dusk/sky. Dressing is Specks only.
- `HABITAT`: "you" may enter both biomes. anomalocaris, trilobite, dunkleosteus and mosasaurus live only in the
  prehistoric biomes, and megalodon only in `prehistoric_open`. The staging gate then rejects a megalodon off a modern
  coast or an orca in the Devonian.
- house.py needs no change: neither biome has a dressing branch, so the pass adds nothing modern. The 20
  house-style tests pass.

Settings by scene:

| Scene | Setting segments (kind · biome · place · depth · waterline · light) | Built as |
|---|---|---|
| s1 hook | place · prehistoric_shallows · Cambrian sea, 508 Ma · 2 m · 0.37 · day | plate `cambrian_split` |
| s2 teasers | Cambrian (as s1), then @armour Devonian · 20 m · overcast, then @jaws place · prehistoric_open · Late Cretaceous · 3 m · dusk, then @teeth **board** (ink) | plate, then plate macro (1.35x, from the SVG), then **code** Ocean dusk key, then **code** board |
| s3 rules | Cambrian split, wide | plate |
| s4 rung 1 | Cambrian · 4 m · no surface (dive), then @You back at the surface | plate `cambrian_under`, then `cambrian_split` |
| s5 Devonian | Devonian · 20 m, then @as **analogy** (ghost car), then @bone place, then @You're "under you" · 6 m | plate `devonian` throughout; the last segment is a CUT looking up |
| s6 Cretaceous | Cretaceous sunset · 2 m · 0.327 · dusk, then @as **analogy** (ghost bus), then @It place, then @Seconds · 12 m · night | plate `cretaceous_dusk`, then **code** violet field |
| s7 Miocene | Miocene open ocean · 40 m · day, then @longer **analogy** (ghost bus), then @But place | plate `miocene` |
| s8 turn | Miocene, wide | plate |
| s9 today | Miocene (scrubber races), then @today coastal_surface · a beach today · 2 m · 0.316 · day | plate whip, then plate `today_coast` |
| s10 | coastal_surface · from below · 12 m | plate `today_below` + code hull and longline |
| s11 stinger and loop | today coast, then @hunter Miocene, then +0.18 Cretaceous, then +0.36 Devonian, then @you Cambrian frame 0 | plates (the rewind) |

**Timing fix for the loop.** The script starts the rewind on "is", but "is → you" lasts about 0.25 s at 190 wpm,
which is too short for four eras.
- The plan pops the YOU pill on "scariest" (still on the today coast).
- The rewind starts on "hunter", at about 0.18 s per era.
- It lands on the Cambrian frame 0 on "you".

If the TTS runs "hunter is you" in under ~0.55 s, add a 0.15 s gap before "you" in the voice track. Don't drop eras:
the rewind is the payoff.

Settings fields for the waterline use the **measured** plate values: 0.37, 0.327 and 0.316. YOU's head and the
mosasaur's nostrils must sit exactly on them.

## 3. Plates vs code

Lesson from explainer-sperm-whale (OVERNIGHT_LOG r3): a reviewer picked **plates in 5 of 6 place settings**. Flat
code sets "read as banded fields next to Kurzgesagt's layered art". Code won only where a waterline moved with a
gauge. This episode has no depth gauge, and every waterline shot is a fixed cut-away, so plates win almost
everywhere.

The kit also has **no prehistoric set dressing**: Reef, Kelp, FishSchool and Jellies would all be anachronisms. The
plates give each era its identity (sponges and barren rock, crinoid mud, the conifer island at sunset) at no build
cost.

| Use a **Codex plate** (far and mid planes, static) | Build in **code** (anything that moves, is compared, or is abstract) |
|---|---|
| All 7 place backgrounds (§5) | Every creature, YOU, the trilobite, the prey fish, ammonite, turtle, whale, modern shark, fishing hull and longline |
| The rewind frames (each era must read in 0.2 s; a plate's identity does that) | The **foreground framing plane** (§4): a parallax plane at depth 1.45, which a plate cannot provide |
| Teaser 1 (Devonian macro, the plate's SVG at 1.35x) | Teaser 2 (jaws from below: Ocean rig dusk key; the creature fills the frame) |
|  | The "Seconds" cut: one violet-indigo field with the jaws in silhouette (a plate adds nothing to a flat field) |
|  | Boards: the tooth beside a hand (s2), and any number board |
|  | Ghost comparators (arm, car, bus, hand) and all UI: TimeScrubber, survival chip, name pills, era tag and curtain, Tag pointers, captions, the NOT KNOWN stamp, the ≈100 MILLION counter |
|  | Surface events: splash ring, spray ring, wake, bubbles |

**How a plate goes into the storyboard.** Use the same pattern as `episodes/explainer-sperm-whale/plates.py`:
- **Plate layer:** the plate is an image layer, not the background. Settings: `fit: cover`, 1296×2304, depth 0.12,
  z -80, and a slow push from scale 1.0 to 1.045 across the scene.
- **Dressing:** drop the house dressing except Specks.
- **Bubbles:** add the sparse foreground bubble plane (depth 1.45).
- **In-scene changes:** an in-scene setting change gets its own plate layer, timed to its segment.
- **Boards:** boards and the violet field stay code.
- **Choosing the plate:** a ~10-line `plates.py` for p1 can key plates on the `plate` field in `settings_plan.json`
  instead of guessing from the biome.

**Resolution.** The Codex plates are 941×1672. A Lanczos upscale to the 1.2x overscan size goes soft, so
`tools/plate_prep.py` vectorizes each plate with vtracer at the "medium" preset (NOTES.md Path A: 44-102 paths,
PSNR 28-40 dB against the PNG). It then rasterizes the plates crisp at 1296×2304 into
`studio/public/plates/explainer-p1/*.jpg` (804 KB total). For push-ins beyond 1.2x (the teaser macro), use the SVG in
`experiments/asset-gen/vec/p1_<name>_medium.svg` directly. It stays sharp at any zoom.

## 4. Code-built pieces (to build)

**Figures (new art, style A: few rounded parts, one flat shadow shape, small eye with one glint, no outlines)**

The cover concept `gen/p1_cover_A.png` and the lineup `gen/p1_creatures_A.png` are art direction only. Check every
anatomy point against fossil reconstructions; the lineup gets several wrong (notes below).

- **YOU, treading water.** This is a new figure; the kit's `explainer/You` has no swim pose and draws a navy
  outline, which is off style A.
  - Follow the cover concept: a round head, short dark hair, dot eyes with a glint, and a sea-green shirt (aqua
    `#0de9e0` shadow tone). Make it head-and-shoulders above the line.
  - Arms scull below the surface; legs kick slowly (the kick slows on "give out").
  - It needs a waterline clip, so the body under the water is tinted one step toward the water colour.
  - Two scales: the hero (frame 0, s3, s9, s11; head about 14 % of the frame height) and the speck (s7 "crumb").
  - The same figure appears in every era; only the water tint changes.
- **Anomalocaris** (~60 cm).
  - Body: a flat oval made of segments.
  - Swimming flaps: a row of overlapping **lateral** flaps along each side, which ripple as a travelling wave. The
    lineup wrongly draws them as legs under the body.
  - Tail: a fan of three pairs of blades.
  - Eyes: two large stalked eyes on top of the head, set **sideways**, not cartoon-forward.
  - Head appendages: two spiny frontal appendages curled under the head. They flare on "scariest", and on "crack a
    shell" they bend and bounce off the trilobite.
  - Colour: rose-red and orange.
- **Trilobite.** Small and oval, three lobes, a few legs that scuttle. It uses `prehistoric_shallows` only.
- **Dunkleosteus** (~3.4 m).
  - Head: a smooth armoured head-and-shoulder shield in **olive / sea green** with plate seams drawn as flat
    shadow shapes, and a round eye in a ring plate.
  - Jaws: two pairs of bony jaw-blade "fangs", no teeth. These parts get the yellow highlight ring on "bone blades".
  - Body and tail: a slate-blue body with a pale belly. The tail should be shark-like (heterocercal), not
    symmetric.
  - Mouth: it needs a jaw hinge so it can snap on "crack".
- **Small armoured prey fish** (Devonian), plus flat plate shards for the snap.
- **Mosasaurus** (~12 m).
  - Head: long and narrow with conical teeth and a jaw hinge (the s2 teaser and the "Seconds" silhouette).
  - Body: four paddle flippers. Deep blue-grey above, pale below.
  - Tail: a **downturned** fluke (hypocercal, lower lobe larger). The lineup's symmetric fluke is wrong.
  - It needs a surfacing pose with the nostrils near the snout tip.
- **Megalodon** (15-18 m).
  - It must **not read as a great white**; the modern shark swims through s9.
  - Body: bulkier and deeper, with a shorter, blunter snout.
  - Colour: a darker slate-indigo back and a white belly, scaled to fill the frame.
  - Eye: it needs an eye-swivel rig (s7, s8).
  - The lineup's megalodon is a great white and must be redesigned.
- **Modern shark** (s9): kit `explainer/GreatWhite`, small, passing by.
- **Small baleen whale** (Miocene, s7): about 6-8 m, grey-blue with throat pleats. It turns away before any bite.
- **Ammonite and sea turtle** (s6 mid plane, drifting slowly, low contrast), and a **fishing hull with a longline
  and hooks** (s10; no gore, no finning).

**Ghost comparators (scale, FEEDBACK P2 and analysis rule 4)**
- A car or bus inside a sea is illogical as a real object, so each comparator is a flat **bone-white silhouette at
  ~55 % opacity** with no outline and no detail.
- It slides in on its word, beside the animal at the same scale, and leaves with the beat.
- Its window is an `analogy` segment (`settings_plan.json`), so the habitat gate allows it.
- The same bus silhouette appears in s6 and s7, so the "longer than a bus" comparison reads at a glance.
- The "arm" in s1 is YOU's own arm. The "hand" in s2 is a hand on the ink board.

**Foreground framing plane (what Kurzgesagt has and our plates lack)**
- WHALE frames almost every shot with dark foreground leaves or rock (`refs/sheets/WHALE_hook_*`). Add one
  code-drawn plane per place at depth 1.45, kept to the bottom corners and out of the caption band (70-78 %).
- Cambrian: two big violet-shadow sponge clumps. Devonian: two crinoid stalks in dark teal. Cretaceous: none (the
  open horizon is the point). Miocene: none (a vast, empty space). Today: two seagrass tufts.
- Use each setting's darkest tone, flat, never blurred.

**UI colours.**
- Verdict chips use the script's colours: HOURS sea green, MINUTES orange, SECONDS red, HOURS? sun yellow.
- The era tag and curtain take the era accent from the §1 table.
- Name pills keep the house gradient pill at ~22 % height.
- The TimeScrubber sits at ~12 %, in bone white on a translucent ink strip; its ticks are coloured with the era
  accents.

## 5. Plates generated (Codex, style board A attached)

All the prompts are `experiments/asset-gen/prompts/p1_*.txt`: a scene description plus `style_A_common.txt`, run as
`REF=$PWD/gen/style_board_A.png ./gen_one.sh`. All images are in `experiments/asset-gen/gen/`.

| Plate | Chosen file | Use | Verdict |
|---|---|---|---|
| `cambrian_split` | `p1_plate_cambrian_split_A2.png` | s1, s3, s4 end, s11 landing | Good. Waterline 0.37, barren lavender rock shore, calm open band for YOU and Anomalocaris. A1 was rejected: its vase sponges read as clay pots. In A2 the orange pincushion sponges read slightly as urchins, which are post-Cambrian; keep them small, or paint them violet if a reviewer flags it. |
| `cambrian_under` | `p1_plate_cambrian_under_A2.png` | s4 dive | Good. Bright surface underside, sponges and microbial mounds on sand. Same palette as the split plate (planned). |
| `devonian` | `p1_plate_devonian_A.png` | s2 teaser 1, s5, rewind | Good. Murky, empty and ominous, with sparse crinoids and shells. Its faint rays are lost when vectorized; that is fine for murk. |
| `cretaceous_dusk` | `p1_plate_cretaceous_dusk_A.png` | s6, rewind | Strongest plate. Waterline 0.327, sun with halo ring, conifer island, warm reflections. |
| `miocene` | `p1_plate_miocene_A.png` | s7-s9, rewind | Good. A vast open space. Frame the lower two thirds (§1). |
| `today_coast` | `p1_plate_today_coast_A.png` | s9-s11 | Good. Waterline 0.316, lighthouse on a rocky point at the left, seagrass on sand. Our own composition (the style board's lighthouse panel is different). |
| `today_below` | `p1_plate_today_below_A.png` | s10 | Good. An empty upper-middle space for the hull and longline. |
| (art direction) | `p1_cover_A.png` | frame 0 composition | Strong. Waterline 0.39, the arm at ~45 % height, the open caption band kept clear. Build it in code on the `cambrian_split` plate; fix the Anomalocaris eyes (§4). |
| (art direction) | `p1_creatures_A.png` | creature lineup | Useful for colours and silhouettes. Anatomy errors are listed in §4. Its soft shading is off style A; the code versions use one flat shadow shape. |

## 6. Frame 0 and the loop seam

- **Frame 0 is the cover:**
  - Background: the `cambrian_split` plate at scale 1.0, push not yet started.
  - YOU: left of centre, head top at ~26 %, the chin on the 0.37 waterline. The near arm is stretched right under
    the water at ~45 %.
  - Anomalocaris: alongside the arm with its tail at the shoulder, the same length as the arm, appendages curled.
  - Scrubber: at the far left, chip "?:??".
  - Foreground: the two sponge clumps in place.
  - Text: no caption on frame 0, matching the last frame (the sperm-whale log noted that mismatch).
- **Last frame:** that exact layout. Freeze the plate push and the foreground drift at their t=0 values on the
  landing frame, so the seam is invisible.

## 7. Open items for the builder

1. Draw the new figures in §4. YOU (treading) and Anomalocaris come first, because they carry the hook (≥ 8/10).
2. Write a p1 `plates.py` (copy the sperm-whale pattern, keyed on `plate`), and paste `settings_plan.json` into the
   storyboard.
3. Re-time every anchor to the real TTS. Check the "hunter is you" span (§2).
4. Run staging after the build. If a ghost comparator trips the habitat gate, its `analogy` window is too short.
5. For the review, do a plates-vs-flat check only if a reviewer doubts a plate. The sperm-whale result already
   favours plates.
