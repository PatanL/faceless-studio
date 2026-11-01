# Why The Infographics Show looks better than our kit (AK-12 Short vs the orca pilot)

Compared: the TIS AK-12 Short (56 s, see SHOTLIST.md) and our `out/pilots/explainer-orca/explainer-orca_9x16.mp4` (75 s).
Evidence: ref/sheets/, ref/transitions/, ref/stills/, plus the orca contact sheet (one frame every 4 s). The measurements
below come from 270x480 frames at 30 fps on the Spark (`refs/tis-ak12/cmp/`).

| measure | TIS AK-12 | our orca pilot |
|---|---|---|
| mean / median abs frame difference (motion energy, 0–255 luma) | **4.96 / 3.37** | 1.76 / 0.83 |
| frames that are nearly still (diff < 0.3) | **0.06 %** | 13.7 % |
| scene changes at a 0.12 threshold | 6 in 56 s (most changes are wipes or moves, so they score low) | 7 in 75 s |
| distinct scene palettes | **9** (orange, olive, sand, mahogany, slate, pink, sand-interior, purple, green) | 1 (teal/navy: every sampled frame's palette sits between #091C25 and #668E9D) |
| characters with faces | **10** designs, all acting | 0 (the orca and the diver are silhouettes) |
| share of the frame covered by illustrated content | 100 % (full-bleed sets every shot) | about 10–25 % (small subjects in an empty gradient ocean) |
| camera moves that reframe | 10 big moves, most with **rotation** | slides and small pushes, no rotation |
| transition types | 5 kinds (silhouette matte, blob matte, slash, iris, explosion cover) | hard cuts only, on the same ocean backdrop; only the subject swaps (checked at 17.4, 28.6, 41.2 s) |

## 1. What makes TIS look better, ranked by how much each closes the gap

1. **Every frame is a full, dressed set, not an object on a backdrop.**
   - Each scene has sky, a mid-ground (huts, buildings, shelving), a ground plane with its own texture streaks, and
     foreground props (crates, hedgehogs, desk) that overlap the characters. That gives 4–6 depth layers in every shot.
   - The orca pilot puts a 300 px silhouette in a 1080x1920 gradient. Most of the screen is dark, empty water, so the
     eye has nothing to read, and at phone size it reads as "simple".
   - The gap is **set dressing density**, not rendering quality.
2. **Characters that act.**
   - TIS tells the story through people: B points, A shows the rifle, D gets heart eyes, the official scratches his
     head, F yells, the Russia ball sweats.
   - Expression comes from cheap, legible parts: brows, mouth shapes, pupils, blush, swap-in emotion glyphs (hearts,
     sweat drop), and props held in hand circles.
   - Each line of narration is literalised by an *action*, not a label: "testing" is a clipboard with ticks, "fire" is a
     muzzle-flash burst, "accessories" is a rifle with an optic, "unreliable" is soldiers fumbling, and "Russia going
     back" is a worried country-ball juggling old AKs.
   - Our kit has no human or character rig at all, which is the single biggest missing asset class.
3. **A camera that never rests, and that rotates.**
   - The near-still frame fraction is 0.06 % for TIS against 13.7 % for us, and motion energy is 2.8× ours (4× at the
     median).
   - TIS's grammar: hold a framing with a slow 3–8 % push, then a fast eased move (0.4–1.2 s) to a new framing, almost
     always with a **±5–20° dutch rotation**. It pulls out from a CU to reveal, or pushes from wide to a CU on the
     detail the voice names.
   - So a single illustrated set yields 3–5 "shots" (scene block 2 is one set and five framings over 11 s). That is why
     TIS can afford detailed sets: each one is reused across several framings.
4. **Motivated matte transitions on sentence starts.**
   - Scene changes are wipes whose *shape comes from the content*: the next shot's character silhouette flies in as the
     matte, an ink blob grows from a mouth, a slash whip follows motion, an explosion covers a camera jump.
   - Every one lands within ±0.1 s of the first word of a new sentence.
   - Our hard cuts keep the same backdrop and swap only the subject, so a scene change barely registers.
5. **A bold, warm, scene-coded palette.**
   - Each scene block gets one dominant hue family with high figure–ground value contrast: olive soldiers on light
     sky, dark-navy suit on mahogany, pink ruins with plum windows, a purple void behind the country-ball.
   - Hue shifts mark the story beats: orange hook, then RU olive, the sand range, a darker "it's not going well"
     office, pink war, a purple "abstract/meta" beat, and green for Ukraine at the end.
   - Our single teal-navy grade holds for 75 s, and its value range is low (mostly #0B202A–#2D6676), so frames blur
     together in the feed.
6. **Shape density instead of shading.** This is the surprising one:
   - TIS barely shades. There are **no outlines**, no gradients on characters, no lighting passes and no drop shadows on
     figures.
   - The richness comes from:
     - the many small flat shapes per object (camo blobs, pouches, buckles, rails, vents, cracks, bricks, window
       frames);
     - one darker "shadow side" shape per head and object;
     - one lighter "top edge" strip on hard objects (guns, beams, hedgehogs);
     - soft capsule streaks as texture on walls, ground and sky.
   - A rifle is about 25–40 shapes, a soldier about 80–120, a building facade about 150+. Our orca is about 6 shapes.
   - Closing the gap needs **asset authoring** (detail per object), not a renderer feature.
7. **Secondary motion everywhere.** Flags wave, clouds drift, muzzle flashes flicker every 2–3 frames, guns recoil,
   characters breathe and blink, the hook background rotates, and sparkles spin as they scale. Nothing on screen is
   frozen while the voice talks about it (FEEDBACK A4).
8. **Juicy micro-FX.**
   - The 4-point white sparkle (0→1→0 with a spin, about 0.5 s) is used three times as a "new/shiny" beat.
   - Other FX: the star-burst muzzle flash, the explosion starburst, check-mark pops with back-out overshoot, and the
     calendar digits typing out.
   - All are cheap and highly reusable.
9. **UI layer separate from the camera.** The calendar and clipboard are pinned to the screen while the world camera
   moves under them, which keeps a fact (2023) on screen across three framings. That is TIS's lightweight version of
   our "progress device".

## 2. Where our kit is already fine or better (keep it)

- **Typography and data overlays.** The orca's speed bars, labelled callouts ("YOU", "~8 M") and strike-through list
  are cleaner infographics than anything in this TIS Short, which has no charts at all.
- **Hook writing.** TIS's hook here is just the title as a question in pills over a hero object. It works because the
  hero object is in frame 1 (FEEDBACK B3), not because the copy is clever. Our playbook hooks are stronger, so keep
  them.
- **Captions.** TIS uses plain 4-line pages in a 70 % black box, ahead of the voice, breaking mid-sentence. That is
  functional but not better than our phrase captions. For the benchmark we copy theirs exactly; for the channel, our
  whole-phrase pages (FEEDBACK B8) remain the rule.

## 3. What this means for the build (priority order)

1. **Character rig kit.** A flat, no-outline puppet with:
   - head (skin plus a shadow-side shape and blush), a brows/mouth/eyes/blink set and emotion swaps (hearts, sweat,
     anger);
   - hand-circle hands with props parented to them;
   - camo uniform via a pattern of capsule blobs clipped to body parts;
   - hair, beard and helmet variants, so one rig makes 8 soldiers;
   - a talk cycle driven by word timestamps.
2. **Camera rig** with position, scale **and rotation** keyframes, eased with cubic/quint in-out. It needs per-layer
   parallax factors and a "hold drift" default, so no frame is ever still.
3. **Matte transition library:**
   - silhouette-of-incoming-subject matte;
   - growing organic blob or splatter matte (an SVG path with noise-driven lobes);
   - diagonal slash wipe with directional smear;
   - iris with soft rim;
   - FX-cover cut.
   Each should snap to the next sentence's first word.
4. **Set-dressing kits:** sky with circle-cluster clouds, ground with capsule streaks, quonset hut, apartment block
   (window grid, cracks, blown windows), rubble, hedgehogs and wire, shelving, crates and flags. Each needs a
   shadow-side shape plus a top-edge highlight per object, and palette tokens per scene.
5. **FX:** 4-point sparkle, star-burst muzzle flash with flicker, explosion starburst, pop-in with back-out overshoot,
   number type-on.
6. **Palette discipline:** one hue family per scene block, characters always reading against the BG by value, and a
   scene-palette change on each story beat.

The exact hex values, timings and easing for each of these are in SHOTLIST.md (section 0 has the global rules).
