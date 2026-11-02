# explainer-p1: reference breakdown (kurz lane)

Internal structure study. Never reuse wording, footage, characters or compositions (BRIEF rule 5, FEEDBACK P7). All measurements are on the Spark, CPU only, at each video's native frame rate (`research/frame-analysis/tools/frame_metrics.py`, every frame decoded). The sheets below were checked by eye.

## 0. Topic pick

`python -m pipeline.sources pick --niche explainer --exclude VtrcKTkhDHU,UNPK8PNCCmQ,fGcgWaswMns,PsEZl1iV1h8,hsubV2gShos` (orca and sperm-whale sources excluded) ranks **nAWpLtG-kNs, "How Long You'd Last in Every Prehistoric Era"** first (score 11.15; 12.2M views; 113x channel median, the strongest outlier in the corpus). The same premise moved to the ocean, **qrfhhZ-Wvmk "...Every Prehistoric Ocean"** (BeyondTheBlue, 3.37M, 6.5x), popped again on another channel, so the formula has been proven twice. Next best: mzeN0BXR4e0 (deep sea, 17M, 13.6x). It overlaps `explainer-pressure-ladder` and `explainer-anglerfish`.

**Premise for p1:** *how long you'd last in every prehistoric ocean*, as a 75-90 s Kurzgesagt-style Short. No existing episode is prehistoric, and it switches setting every rung (FEEDBACK P3). Writer: pull era facts from `research/corpus/explainer/qrfhhZ-Wvmk.md` and its fact note (for example, Dunkleosteus is now about 3.4-4 m, not bus-sized; Cameroceras lengths are contested; Jaekelopterus is Devonian). Check every number again.

## 1. The three references

| Key | Video | Role | Views / outlier | Length, fps | Shots/min | Hard cuts/min | Shot median | Visual-event gap median | Words, wpm |
|---|---|---|---|---|---|---|---|---|---|
| **ERAS** | nAWpLtG-kNs, Fossil | topic and ladder structure | 12.24M / 113x | 970 s, 25 fps | 15.0 | 13.2 | 3.64 s | 3.36 s | 2,669, 165 |
| **WHALE** | oR3Q7RntqEw "Whales Evolved from This Animal", Kurzgesagt | lane form: a prehistoric-ocean ladder as a Kurz Short | 5.25M / 1.9x Kurz Shorts median (2.75M over 142 Shorts) | 151 s, **60 fps** | 10.7 | 6.0 | 5.12 s | 2.03 s | 411, 164 |
| **SALT** | pb9g6osg2aY "Why Is the Ocean Salty and Rivers Are Not?", Kurzgesagt | lane pace: the top ocean Kurz Short | 8.96M / 3.2x | 59.5 s, 30 fps | 20.2 | 10.1 | 2.23 s | 1.40 s | ~190, ~195 |

Correction to the long-form study: Kurzgesagt **Shorts do use hard cuts** (6-10 per minute, confirmed one frame apart on the every-frame sheets, for example SALT f69 to f70 at 2.33 s). Their long-form videos have none. Shorts mix three changes: hard cuts on a word, 0.4-1.1 s diagonal or whip wipes, and continuous camera travel (SALT's beach to river pan at 1.0-1.8 s; WHALE's surface-to-depth dive at 59-74 s).

## 2. Hook, first 3 s (every frame)

**WHALE** (`sheets/WHALE_hook_*`, every 2nd frame at 60 fps)
- f0: the cover. A full-colour jungle, the dog-sized ancestor in profile at mid-height, foreground leaves framing it. No black frame, no title.
- 0.02-1.8 s: the line "This is a whale" sits over an image that contradicts it. That **absurd claim, proved wrong by the picture**, is the whole hook.
- 1.8 s (f108): the head turns toward camera and the mouth opens on the last word. It is the first motion beat.
- 3.05 s (f183): the name tag pops in, a red-to-orange gradient pill at 20 % height, 0.15 s after the name is spoken.
- 5.1-6.4 s: the first number lands ("50 million years").
- 7.2 s: the first transition, a diagonal wipe to a yellow board.
- The opening shot holds 7.6 s. It stays alive through character animation and the tag pop, not through cuts.

**SALT** (`sheets/SALT_hook_*`, every frame at 30 fps)
- f0-f7: black, then a 0.27 s fade-in. **Do not copy this.** Our frame 0 is the cover (P1).
- 0.3-2.3 s: the title question, on screen as two lines of outlined white text at about 70 % height, over a top-down beach with two small characters.
- 1.0-1.8 s: the camera pans diagonally from the beach up to a river on "and rivers aren't". The camera travel shows the noun as it is spoken.
- 2.33 s: a hard cut, on the counter-claim's first word ("In fact"), to a giant salt shaker pouring over a river-and-sea map. The surprising answer is shown before it is explained.

**ERAS**
- f0-f6: black. 0.28-1.7 s: a fade-in on a man in a field.
- Then a **teaser montage of 28 hard cuts in 30.5 s**, one shot about every 1.1 s, one creature per question.
- 33.6-34.4 s: black. 34.5 s: the first era card. 36.9 s: the **empty tier list**, the scoreboard.
- The hook is 94 words in 31 s. In a Short, the montage idea survives only as 3 teaser shots inside 3-8 s.

## 3. Shot lists of the two Shorts (shot boundaries measured, content read off the sheets)

**WHALE** (27 shots). Each species goes through the same three steps: exhibit, then alive in its habitat, then the mechanism close-up.

| Time | Shot (angle) | Device | Line it shows |
|---|---|---|---|
| 0.0-7.6 | ancestor in jungle, side profile, mid shot | head turn at 1.8 s; name pill at 3.05 s | claim and name |
| 7.6-12.8 | flat yellow board, then two diagonal splits stacking ancestor, transitional animal and whale | lineage as split panels | "traced back to" |
| 12.8-17.5 | underwater, huge whale head filling the right half, tiny diver for scale | scale comparator | "biggest animal" |
| 17.5-20.2 | red macro texture, silhouette | "let's investigate" punctuation | |
| 20.2-23.5 | fossil skeleton on a dark field, hazard tape, evidence marker "A", map inset circle | crime-scene exhibit plus locator inset | "found in Pakistan" |
| 23.5-39.5 | aerial jungle; animal at the waterline, high angle; sunset horizon with a submerged silhouette | habitat, then behaviour | rivers, paddling, heavy bones |
| 39.5-48.4 | top-down globe, supercontinent; pins Laurasia, Gondwana, Tethys Sea | map with pinned labels on the word | continents split |
| 48.4-53.2 | red curtain opens; orange **era tag "EOCENE"**; museum plinth with a skeleton and a plaque | era card plus exhibit | "fossils from the Eocene" |
| 53.2-74.1 | the animal on a grass plain (pill tag), then a dive cut to underwater, swimming diagonally; spine highlighted | alive, then the mechanism drawn on the body | legs, kicking, spine |
| 74.1-78.1 | a hand pulls down a blueprint scroll of two outline whales | the next exhibit is "pulled down" | next exhibit |
| 78.1-89 | two whales in open water; an orange x-ray view; a yellow ring on a tiny hind limb | x-ray plus highlight ring | "hind limbs so small" |
| 89-96 | magnifying glass; a whale in a shallow bay saying "Meh" in a speech bubble | gag on the fact | "couldn't go onto land" |
| 96-106 | wide underwater crowd of modern whales; the blue whale fills the frame | radiation | "countless species" |
| 106-137 | lineage mobile on cream (one line, then branches); ear bone dropping into water with sound arcs ("Nice."); DNA machine printing a hippo; ankle bone inset; pin-and-string **evidence board** | honest caveat, then 3 numbered clues | "we don't know exactly" + 3 clues |
| 137-151 | blue whale with a **timeline scrubber bar**; rewind icon steps back through each ancestor to the opening jungle frame | rewind to the start = loop | thesis line, last half-line cut mid-sentence |

**SALT** (20 shots). It is a process loop: sea, sky, land, river, sea.

| Time | Shot | Device | Line |
|---|---|---|---|
| 0.3-2.3 | top-down beach, pan to a river | title question on screen | question |
| 2.3-6.4 | map with a giant salt shaker; mascot bird with "?" | answer first, confusion beat | counter-claim |
| 6.4-16.6 | isometric water tile on navy; sun; vapour rises to clouds; island tile slides in; rain | isometric diorama, one element added per clause | evaporation, clouds, rain |
| 16.6-20.8 | violet macro of a raindrop with CO2 molecules; **"Not to scale"** tag; pH bar | macro view plus honesty tag | acidic droplets |
| 20.8-25 | rocks in a stream; magnifier circle | magnifier inset | minerals wash out |
| 25-30.5 | high-angle river carrying orange dots down to the sea | particles show the flow | salts travel |
| 30.5-37.3 | seabed; plankton inset card; **Na and Cl tags** on pointer lines; salt-shaker icon on a pin | callout tags | leftovers = salt |
| 37.3-44.6 | penguin-like bird floating at the surface; camera sinks; dots settle to the floor | vertical camera travel | sediment balance |
| 44.6-48.4 | world map; purple tag "38 g/l" becomes orange "35 g/l" | number tag that morphs | 35 g/l average |
| 48.4-55 | river network at night, dots streaming to the coast | the same flow, re-lit | rivers just deliver |
| 55-57.2 | **the opening beach again** | bookend | "what goes in comes out" |
| 57.2-59.5 | subscribe card with mascot | CTA (we skip it) | |

## 4. How each line is shown

- **Captions:** 1-3 word chunks timed to the voice (about 0.4-0.6 s each). White, with a thin dark outline. Small: the cap height is about 3.5-4 % of frame width. Fixed low centre: 72 % of height in SALT, 78 % in WHALE. In SALT, only the title question is larger, on 2 lines. Our FEEDBACK P5 asks for whole-phrase captions, so keep that rule, but copy the low-centre fixed position and the small, unobtrusive size.
- **Names** appear as a gradient pill tag at 20-25 % height, 0.1-0.2 s after the word.
- **Numbers and terms** are coloured tags on a pointer line, pinned to the thing they describe (Na, Cl, 38 → 35 g/l, Laurasia). They are never floating text.
- **Eras** get a large orange tag over a curtain reveal (WHALE 48.4 s). ERAS uses a full-screen title card plus "N-M million years ago" for 2-4 s.
- **Scale** comes from one familiar comparator in the same frame: a diver next to the whale. ERAS uses a silhouette chart against a 1.8 m human for every predator.
- **Verbs are animated on the word:** the head turns on "whale", vapour rises on "rises", the shaker pours on "salt".
- **Honesty markers** are on screen: "Not to scale" (SALT 17 s), and the caveat about "we don't know exactly" gets its own beat (WHALE 106 s).

## 5. Payoff and loop

- WHALE ends with a **rewind through every stage back to frame 0**, and the final half-sentence runs into the opening line. That is a perfect loop with no CTA in the picture.
- SALT bookends on the opening beach, then adds a 2.3 s subscribe card. Per PLAYBOOK §6, our Shorts drop the card and cut within 1 s of the last word.
- ERAS's progress device is the **tier list**. It appears empty at 36.9 s, and an era is dragged into its row after every verdict (15 eras, 33-93 s each, median about 66 s). The final board is held for 15 s, and the safest era is announced at 14:49 (92 %). OCEANS twists at 84 %: today's ocean is the safest of all.

## 6. What to copy structurally (p1 at about 80 s, about 230 words at 170 wpm)

| p1 beat | Seconds | From |
|---|---|---|
| Hook: "you" dropped into the first ocean, with a stuck-time-machine premise. The cover frame shows the creature, and the question is spoken while on screen. | 0-3 | ERAS L1 + WHALE f0 cover |
| 3 teaser shots, one hard cut each: the scariest three, the most famous held last. Then the rules: no gear. | 3-9 | ERAS teaser montage, compressed |
| Show the progress device: a time scrubber (WHALE's bar) carrying a survival-time chip that fills like ERAS's tier row. | by 9 | WHALE 137 s, ERAS tier list |
| 6-7 era rungs of 8-10 s each, with the same slots in the same order: era tag on a curtain or wipe, then the place (map or habitat), then one predator with a scale comparator, then the verdict chip snaps into place. Each rung is a new setting, so lightness and palette shift. | 9-55 | WHALE exhibit-alive-mechanism; PLAYBOOK 1b list Short |
| The turn at about 60 %: the favourite falls (the biggest predator is not the deadliest era), or the rule is used against you. | ~50 | PLAYBOOK L5b/S4 |
| The answer at 66-90 %: the era you survive longest, plus the twist that today's ocean is the safest. | 55-72 | ERAS 92 %, OCEANS 84 % |
| Loop: rewind the scrubber through every era to frame 0, and cut mid-line into the hook. | 72-80 | WHALE 137-151 s |

**Pacing targets:**
- one visual event every 1.4-2.0 s (median), and one shot every 2.2-5 s;
- 6-10 hard cuts per minute, placed on words, plus wipes and camera travel;
- a new setting every rung (8-10 s), which also beats the 5-8 per minute of REFERENCES_ANALYSIS §4;
- a name tag on every named animal;
- one comparator per size claim.

## 7. What to beat

- Frame 0: SALT and ERAS open on black. We open on a finished cover frame, as WHALE does.
- WHALE holds its first shot for 7.6 s and one later shot for 15 s. Keep our longest single shot at 6 s or less, unless the camera is travelling.
- ERAS is a stock-CGI collage with mixed styles and meme inserts. We keep one consistent flat world (house style A), with each creature in its own habitat and at its own depth (REFERENCES_ANALYSIS rules 9-12).
- ERAS's tier list is a static screenshot board. Our progress device lives inside the frame and moves.
- ERAS spends 33-93 s per era. We spend 8-10 s, with one fact per rung and no padding.
- SALT and WHALE end on a subscribe card or a trailing half-line. We end on the strongest word, and the loop is cut on it.

## 8. Blender or not?

**No.** The kurz lane is flat 2D: HOUSE_STYLE A, with flat shapes, one shadow shape and no rendered lighting. Every frame of WHALE and SALT is flat vector. Even SALT's isometric tiles (6.4-16.6 s) are flat-shaded polygons, and our Remotion/SVG kit can draw them. Blender would add render time and nothing visible. It is also parked: FEEDBACK_LOG 2026-11-01 says "3D/Blender parked", and BRIEF rule 2 reserves the Mac's Blender for another project. ERAS's realistic CGI is the look of the Zack D. lane, not this one.

## Files

- `sheets/WHALE_hook_*`, `SALT_hook_*`, `ERAS_hook_*`: the first 3.2 s at native fps (every frame; every 2nd frame for WHALE at 60 fps).
- `sheets/*_half_*`: one frame every 0.5 s. `ERAS_open_*` covers 0-48 s every 0.5 s; `ERAS_all2s_*` is the whole video at one frame every 2 s. Marker colours: red = cut, yellow = transition, cyan = composition event.
- `sheets/WHALE_devices.jpg`: 12 device stills at 0, 3.5, 9.5, 16.5, 21.5, 49.5, 54, 76, 87, 115, 134.5 and 142 s. `sheets/SALT_stills_captions.jpg`: caption and tag stills at 1, 3, 9, 34 and 45.5 s.
- `data/*_events.json`: every-frame cuts, transitions, composition events and shots. `data/oR3Q7RntqEw.txt` / `.words.json`: whisper transcript of WHALE. `data/pb9g6osg2aY.en.vtt`: SALT subtitles. The ERAS transcript and annotation are in `research/corpus/explainer/`.
- `tools/ref_sheets.py`: native-grid contact sheets for any aspect ratio, used for everything above. The videos stay on the Spark at `~/studio/refs/explainer-p1/`.
