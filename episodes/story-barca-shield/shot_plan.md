# story-barca-shield: shot plan (pre-production, 2026-11-02)

**Timings.** Times are the voiced Kokoro word starts: storyboard.json, 214 words, 3.72 words/s, last word ending at 57.61 s.

**Build.** The build goes in `experiments/three-lane/src/barca/` (story.ts, sets.ts, Barca3D.tsx) on `EpisodeNext` with the `src/next` tools. It starts **after the visual track reports the kit integrated**; until then no kit file is touched.

**Captions.** House captions (phrase pages, `caption_rule: "phrase"`); the owner's decision on the caption style is pending.

## Rules applied (the Vasa panels' named flaws, and the new tools)

| Rule | How it is met here | Checked by |
|---|---|---|
| A place or view change at least every 4 s | 27 views in 58 s (median hold 2.1 s, longest 3.9 s); every group sets `place`, and cutaways set `insert: true` | `planReport(groups, words)` with 0 flagged holds, run in node before any render |
| Cutaway sets | map (`mapSet` + `routeRig`), the bronze shield as a macro shot (`macroSet` with a dirt ground swapped in), and a cross-section under the wall (`crossSectionSet` with the wall on top, the tunnel cavity, the shield on the surface, the countershaft) | the plan's place and insert count: at least 7 places and at least 3 inserts |
| Characters large | every people shot is a `castKey` preset: hook and dialogue **close** (head 0.20), walks **medium** (0.11); **wide** (0.06) only for the establishing shot, the map and the camp | `castCheck(groups, peopleCast)`: about half the frames with a head ≥ 0.07, no people group under 0.05 except inserts |
| The hook reads at phone size (Vasa: "30 sailors are specks") | frame 0 is the smith **close** (head ≥ 0.2), kneeling with the shield, the Persian tents over the wall behind him | `headFrac` at t = 0, 1.5 and 3.0 s ≥ 0.11 |
| Faces swap on words | `faceTrack` / `poseTrack` / `markAt` on every speaking or reacting figure (cues below); reaction runs of 1-4 f | `checkFaceTrack`: 3-10 swaps per 10 s on the lead |
| Light follows the story | `lightArc`: dusk at the hook, day for the setup, a day-dusk-day-dusk relight while the days pass, dusk at the ring, **night-blue `explain`** from "You see" (rule L3), lamplight flicker in the tunnel, a 2-frame `flash` on "broke into", night at the end | `arcStats`: at least 3 light states, at least 2 in-shot relights |
| Joins that don't ghost | `whip` between places; `match` from the Barca pin on the map to the city; `push` from the shield on "You see" down into the ground (the pivot); hard cuts only on "rings," and "broke" (2 cuts) | `ghost_check.py` on the render, using the plan's windows |
| No gauge or HUD reads backwards (Vasa: "6°, 2°, 10°") | **no HUD**. The only counter is an in-world DAY tally scratched on the wall (DAY 3 → 9, forward only), on "For days" | the counter's steps are monotonic (asserted in story.ts) |
| Labels large (Vasa: HEAVY/LIGHT too small) | every tag is ≥ 64 px cap height at 1080 wide: SOLID GROUND, HOLLOW TUNNEL, BARCA, PERSIAN ARMY, DAY n | the labels are measured in projected px from the story file (shot-plan check in story.ts) |
| Nothing that matters is cut by the frame edge | `castKey` and `fit` with the others list; replay with `scripts/framing.ts` (cut, near and caption gate) | 0 cut ranges ≥ 8 f; the caption gate is clean |
| No flat water or sky (Vasa: "flat, sparse water and sky") | `stoneCourses` walls and streets, `grainPlanks` gate and ladders, `dress()` props along the inner street (sacks, barrels, buckets, crates), `clouds()` cards in every exterior, a sky dome, dust kicks; no open water in the story | `tools/look_density.py` on frames30: edge density ≥ 0.08, flat share ≤ 0.5 |
| Every on-screen element is mentioned or obvious (Vasa: "DISTANCE meter never explained") | every label repeats a word from the narration: BARCA, PERSIAN ARMY ("a Persian army"), DAY ("for days"), SOLID GROUND ("over solid ground"), HOLLOW TUNNEL ("over a hollow tunnel"). Nothing unexplained: no HUD, no distance, no gauge | a reading of each label against the narration (listed below) |

## Places

1. Inside the wall: a strip of dirt along the inner face of the wall, the street of houses behind it, and a tower at one corner.
2. The wall walk and parapet, looking out over the plain.
3. The Persian camp on the plain: tents, banners, cook smoke and the commander's tent.
4. The gate under assault: a ram and ladders.
5. A map of the coast (inset).
6. A macro shot of the shield on the dirt (inset).
7. A cross-section under the wall (inset): the soil bands, the Persian tunnel by lamplight, and the countershaft.

## Timeline (views; ★ = a place change)

| t (s) | Words | Group / view | Set | Cast (preset) | Faces, poses and fx on words | Light | Join in |
|---|---|---|---|---|---|---|---|
| 0.00 | With an army outside the walls, | ★ hook, close: the smith kneeling, shield on the dirt; the Persian tents seen over the wall | inside the wall | smith **close** (head 0.20, above the caption band) | smith `focus`; pose kneel-hold | dusk | — |
| 1.84 | the city's bronze-smith spent every day | hook, over-the-shoulder push: the shield set down, his ear to it | inside the wall | smith close | `listen` pose on "laying" | dusk | view |
| 3.71 | laying his shield down in the dirt. | hook, low side: shield and smith | inside the wall | smith medium-close | dust kick (`debris` paper→dust, n 12) on "dirt." | dusk | view |
| 5.31 | The guards on the wall think | ★ doubt: two guards at the parapet, looking down | wall walk | guards **close** pair | guard1 `sly` → `cackle` on "cracked" (react `squeeze` 2 f); guard2 `deadpan` → `grin` | dusk | whip |
| 6.88 | has finally cracked him. | doubt: reverse, down past the guards to the smith, small below | wall walk | guards medium | guard1 pose `point` on "cracked" | dusk | view |
| 8.12 | It's about 2,500 years ago in Barca, | ★ map, wide: a route arrow from the east (PERSIAN ARMY) toward the BARCA pin | map (insert) | — | the route draws over 8.2-10.2; the BARCA pin drops and glints on "Barca," | day | whip |
| 10.96 | in what's now Libya, | map close on the pin; the coast and LIBYA lettering | map | — | LIBYA label on "Libya," | day | view |
| 12.16 | and a Persian army has the city surrounded. | ★ camp, high and wide: tents ring the walled city, the gate in the foreground | camp | soldiers small (establishing) | banners flutter (ambient) | day | **match** (the BARCA pin to the city) |
| 14.19 | For months they hammer the walls, | ★ assault: a ram hits the gate, ladders at the wall | gate | Persian soldiers medium | `burst` + `debris` (splinter) on "hammer" and on "walls,"; soldiers `furious` | day | whip |
| 15.65 | and the walls hold. | assault reverse, from the wall top: defenders push a ladder off | wall walk | defenders medium | defender `grimace` → `grin` on "hold." | day | view |
| 16.75 | But the Persians don't give up, | ★ commander's tent: the Persian commander, arms folded | camp | commander **close** | `smug`, pose `hips` | day→dusk ramp (0.6 s) | whip |
| 18.21 | and they don't go home. | camp, wide behind him: cook fires lit, tents | camp | commander medium | — | dusk | view |
| 19.27 | So the smith starts walking the inside of the wall. | ★ inner street, tracking: the smith walks with the shield | inside the wall | smith **medium** | walk; `focus` | day | whip |
| 21.57 | He sets his shield down, kneels, listens, | inner street, low front: he kneels, ear down | inside the wall | smith close | `poseTrack`: kneel on "kneels,", listen on "listens,"; face `puzzled` | day | view |
| 23.91 | then moves a few steps and does it again. | inner street, high: three dust rings where the shield has been, a fourth being set | inside the wall | smith medium | walk; marks in the dust | day | view |
| 25.76 | "Lost something?" a guard laughs. | ★ wall walk, close on the guard laughing down | wall walk | guard **close** | guard `cackle` on "laughs." (react `squeeze` 2 f); `talk` window | day | whip |
| 27.96 | "The enemy's out there, not down there." | down at the smith, the guard's arm pointing out, then down | wall walk | guard + smith medium | guard pose `point` on "out" → down on "down"; smith `deadpan` | day | view |
| 29.65 | For days, nothing. | ★ montage on the wall: the smith at new spots, DAY tally scratched on the stone, 3 → 9, forward only | inside the wall | smith medium | `counter` (in-world tally, label DAY) on "days,"; light relights | day→dusk→day (0.5 s blends) | whip |
| 30.77 | Just a dull thud, wherever he puts it. | macro: the shield dropped flat, a dust puff, **no rings** | shield macro (insert) | — | dust `debris` on "thud,"; smith's knee at the edge | day | view (cut-free, place = macro) |
| 32.79 | Then, at one spot by the wall, | ★ corner by the tower, low: the smith kneels at a new spot | inside the wall | smith **close** | face `focus` | dusk | whip |
| 34.41 | he sets it down and it rings, | macro: the shield; on "rings," an inked ring `burst` and a `glints` star on the rim | shield macro | — | `flash` 2 f on "rings,"; hard **cut** on "rings," | dusk + flash | cut |
| 36.19 | and the dust on the bronze starts to shiver. | macro, closer: dust specks hop on the bronze (looping `debris` hops) | shield macro | — | — | dusk | view |
| 37.28 | starts to shiver. | smith's face **close**, eyes wide | inside the wall | smith close | `stunned` on "shiver." (react `blank` 2 f), `sweat` mark | dusk | view |
| 38.16 | You see, while the Persians were hammering the walls, | ★ the pivot: **push** down through the shield into the cross-section; above ground the ram still hits the gate | cross-section (insert) | diggers small | ram above ground (cut-away top); light → `explain` night blue over 0.8 s | explain | **push** (`circlePortal` on the shield) |
| 40.67 | they were also digging under them. | section closer: the tunnel by lamplight, four diggers with picks | cross-section | diggers **medium** | diggers `focus`; picks swing (pose `strike`/`strikeUp` alternating, 0.5 s); lamp flicker | explain + lamp | view |
| 42.19 | Over solid ground, a bronze shield just thuds. | section, left: the shield on the surface over solid soil, label SOLID GROUND | cross-section | — | a flat, dull ring (grey, small) on "thuds." | explain | view |
| 44.91 | But over a hollow tunnel, | section slides right: the shield over the tunnel, label HOLLOW TUNNEL | cross-section | diggers medium | — | explain | view (glide) |
| 46.26 | every pick striking below makes it ring like a bell. | section close: a pick strike (`burst` at the tip) and wave rings rising through the soil to the shield, which rings (inked rings, `glints`) | cross-section | digger close | ring bursts on "pick", "ring", "bell." | explain | view |
| 48.78 | So wherever it rang, | ★ inner street at night: defenders with shovels around the smith's dust ring | inside the wall | defenders + smith **medium** | defenders `furious`; smith points | night (torches) | whip |
| 50.01 | the defenders dug straight down and broke into the tunnel from above. | section: the countershaft drops; on "broke" it breaks into the tunnel (`debris` + `flash`); the diggers turn `terrified` | cross-section | diggers medium | diggers `terrified` on "broke" (react `blank` 2 f); hard **cut** on "broke" | explain + flash | cut |
| 53.08 | An army spent months digging in secret, | ★ camp at night, high and wide: tents and fires around the dark city | camp | — | fire flicker | night | whip |
| 55.22 | and a shield lying in the dirt heard every swing. | ★ the last image: the shield in the dirt at night, close, with a slow push; a `glints` star on "heard"; a callback to frame 0 | inside the wall / shield macro | — | glint on "heard" | night | whip |
| 57.61 + 0.4 | end | the video ends within 0.5 s of the last word | | | | | |

**Joins.** 12 whips, 1 match, 1 push and 2 cuts. Hard cuts stay at 3 or fewer, and the one-frame jump budget is kept by the whip overlap (as in Vasa v11+).

## Labels and what names them

| Label | Named by |
|---|---|
| BARCA (pin) | "in Barca," |
| LIBYA (map lettering) | "in what's now Libya," |
| PERSIAN ARMY (route arrow) | "a Persian army" |
| DAY 3 … DAY 9 (tally on the wall) | "For days," |
| SOLID GROUND | "Over solid ground," |
| HOLLOW TUNNEL | "over a hollow tunnel," |

No HUD, gauge or meter.

## Open items for the build (after integration)

- **Macro ground.** `macroSet` has wood and cloth surfaces only. The shield macro needs a dirt ground (a new `surface` value is a kit change, so this goes as a plane in the episode's own set until the visual track adds it).
- **Poses.** Check that the Actor has a kneel pose and a listening head tilt. If not, use crouch-like `hold` plus the head tilt in `actor.tsx` (a kit change, so it is asked for, not made here).
- **Cast.** Persian soldier and Barca guard costumes: the closest existing costumes (`captain`, `sailor2`, `judge` and others) are to be checked against the period. Otherwise they are asked of the visual track as new costumes.
