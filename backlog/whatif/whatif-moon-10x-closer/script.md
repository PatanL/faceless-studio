---
slug: whatif-moon-10x-closer
niche: whatif
format: short
aspect: "9:16"
title: "What if the Moon was 10 times closer?"
title_keyword: "10 times closer"
target_runtime_s: 80
target_runtime_range_s: [78, 82]
target_words_per_min:
  captions: 64.5          # 86 caption words / 1.333 min; PLAYBOOK Shorts median 56 (43-65)
  all_on_screen_text: 128 # 86 caption + 57 HUD + 28 title/end-card words = 171 words / 1.333 min; PLAYBOOK median 115 (103-131). Map/diagram labels (~9 words) not counted, as in the corpus counts
numbers_per_min: 16       # 21 distinct numeric readings; live meters counted once (PLAYBOOK median 14, range 7-18)
voiceover: "optional light TTS that reads the 13 captions only, verbatim, at their timestamps (~65 wpm); title, HUD and end card are never read. Music bed + SFX carry the textless stretches"
captions_count: 13
caption_words: 86
caption_mean_words: 6.6
second_person_captions: "4 of 13 (31%): place, body, top rung, twist. Above the PLAYBOOK median (18%) on purpose: three critique lenses asked for the top rung and the payoff to land on the viewer"
hook: "title card (8 words, 0:00-0:04.5) over a distance counter derived from the Moon's apparent size, which visibly quadruples by 0:01; event lands at 0:08 (10%)"
master_loop: "SEA BACK IN 57:00:00 clock, opens 0:08 at the event, closes 1:05 (71% of runtime; PLAYBOOK median 70%, range 59-78%)"
references:
  - id: "7693494009494342945"
    short: ELECTRONS
    url: https://www.tiktok.com/@man_ia_c/video/7693494009494342945
    views: 18200000
    outlier_score: 29.13
    why_chosen: "Highest-outlier Short and the cleanest skeleton. We borrow: the return clock that opens at the event (0:08) with an honest time factor; a wonder line, then a body line in POV (0:09, 0:15); a rule, then a shorter implication line, then a textless break (0:21-0:32); a ladder whose cadence peaks at 3 s (0:32-0:35); a full-frame interrupt (0:40) that wipes to a space view with a live climbing number (0:42); an '[X] BACK' label, a reassuring line and a '[place], [time] later' stamp (1:04-1:06); a twist with one HUD equivalence (1:09-1:10); black + exact title + one fact (1:12-1:15)."
  - id: "7693617402180881697"
    short: NEUTRONS
    url: https://www.tiktok.com/@man_ia_c/video/7693617402180881697
    views: 5100000
    outlier_score: 8.16
    why_chosen: "Same template, with a quiet 0:00 HUD subline planted for the twist (paid at 1:09) and a twist coda giving a longer-timescale number (1:10). We borrow: the planted subline reversed at the end; the 'But' pivot on the rule line (0:21); a black cut as the interrupt (0:28-0:31); the nearly wordless race of several moving HUD numbers before the return (0:52-1:04); the end fact held about 6 s (1:15)."
  - id: "7694025665993100576"
    short: POPSTAR-100x
    url: https://www.tiktok.com/@man_ia_c/video/7694025665993100576
    views: 4900000
    outlier_score: 7.84
    why_chosen: "Closest premise shape (H3: 'What if [X] was [N] times [bigger]?'). Frame 1 shows the answer, and a distance HUD closes on the viewer from 0:00. We borrow: the approach counter in the hook; stats turned into famous geography (0:21-0:27); the return-to-you dip that relocates the viewer at the top rung (0:35 'LEVEL WITH FLOOR 23'); the end-card science fact that closes an early loop (1:15)."
fact_file: "Fact sheet at the bottom. Every number is real or flagged EST. (equilibrium-tide maths, order of magnitude). One model drives the sea-level HUD, the clock and the Cliffs seaLevel track: see 'Tide model'."
post_caption: "What if the Moon was 10 times closer? You're under the White Cliffs of Dover when the Moon swells to 11 times its width. Midnight gets bright enough to read by. But its tides are 1,000 times stronger, so the sea drains 123 metres and you could walk to France. TV satellites get flung out of orbit. When the sea comes back, it doesn't stop at the beach. And the Moon has started falling. Which would you do first: walk to France or run for the cliffs? 👇 #whatif #pov #simulation #science #space"
originality_check: "PASS (see review.json)"
---

# What if the Moon was 10 times closer?

Engine: PLAYBOOK §1A Shorts skeleton (S1-S10). Hook formulas H3 (relatable N× multiplier, answer visible in frame 1) + H4 (a pre-event counter over a calm, named place). Ladders: closing distance (hook), then sea-level stakes (harbour → North Sea → **you** walk to France, top rung personal), then a cosmic climb by consequence (satellites → GPS → the ground itself). The return twist (T1, the return makes it worse) lands on the viewer's own spot, then a plant reversal (the 0:00 subline "drifts away" flips to "falling toward us") with an honest EST. timescale (T12).

Premise change (exactly one rule): the Moon's orbit shrinks from 384,400 km to 38,440 km (centre to centre). Same Moon, same mass, an equatorial orbit for the tide maths (declination 0, the gentlest case; see the fact sheet). Everything else follows from physics.

## Tide model (single source of truth for HUD, clock, sky and the Cliffs `seaLevel` track)

- Place: St Margaret's Bay, under the White Cliffs of Dover, 51.15°N 1.38°E (the English end of the narrowest crossing to Cap Gris-Nez, 33 km).
- Story time `t` (hours) = screen seconds − 8. Time-lapse **1 hour per second** from 0:08 to 1:05.
- Moon hour angle `H(t) = −(23.0° + 2.35°·t)` (it moves west → east, because its 20.7 h orbit outruns Earth's 23.93 h spin). It arrives at H = −23.0°, the one position where the new equilibrium tide equals today's sea level, so the sea starts exactly at today's shoreline.
- Sea level `h(t) = 246 m × (3·cos²θ − 1) / 2`, with `cos θ = cos 51.15° · cos H` (equilibrium lunar tide today 0.357 m, × 1,000 for 1/d³, × 0.69 for the solid-Earth response).
- Key values (all screen times follow from this): −20 m at 0:12.1 · −40 m at 0:15.6 · −65 m at 0:19.8 · −100 m at 0:26.5 · −120 m at 0:32.9 · **low −123 m at 0:36.5, Moon centre on the eastern horizon** · back to today's level at **1:05.0 (t = 57.0 h)**, Moon below the horizon · **high +22 m at t = 66.8 h**, Moon at lower transit (opposite side of Earth). High-to-high period 76.6 h.
- Clock time = 19:00 (equinox, local) + t. Sun: sunrise 06:00, sunset 18:00. So: night 0:08-0:19 · day 0:19-0:31 · night 0:31-0:43 · day 0:43-0:55 · night 0:55-1:07. The "67 HOURS LATER" shot is 14:00, daylight.
- Moon phase: elongation from the Sun `ψ(t) = 145° + 17.4°·t` (synodic period 20.7 h). Waxing gibbous at 0:00, **full at 0:10**, last quarter at 0:15, new at 0:20.4 (a dark disc with bright earthshine low in the ESE at dawn, beside but not over the Sun), crescent at 0:24.5, full again at 0:30.7, waning gibbous at moonset. Moonset (lowest water): lower limb touches at 0:34.6, centre at 0:36.5, gone at 0:38.4; it does not rise again before 1:20.
- Moon distance meter (the plant reversed): inside synchronous orbit, tides pull it inward at about 12 km/year (today's 3.8 cm/year × 10^5.5), i.e. 1.37 m per story hour: 38,440.000 KM at 0:08 → 38,439.936 at 0:55 → 38,439.922 at 1:05 → 38,439.908 at 1:08.3 (t = 66.8 h).

## Beat alignment table

| Our beat | Our time | Reference id + timestamp | Device borrowed | How we adapt it |
|---|---|---|---|---|
| S1 Premise card + approach counter | 0:00-0:08 | 7694025665993100576 @0:00 (giant already in frame 1, distance HUD counting down) | Answer visible in frame 1; a live distance number closing in | HUD THE MOON counts 384,400 → 38,440 KM. The number is derived from the Moon's apparent size (ease-out on 1/d), so the disc is ~4× wider by 0:01 and ~6× by 0:02 |
| S1 plant | 0:00 HUD subline | 7693617402180881697 @0:00 (quiet subline the twist pays off at 1:09) | Chekhov fact in the HUD subline | "DRIFTS 3.8 CM AWAY EACH YEAR". Its reversal is foreshadowed by a live meter from 0:55, paid by the 1:11 twist caption, and closed on the end card |
| S2 Place you | 0:05 | 7693494009494342945 @0:05; 7693617402180881697 @0:05 | Second person + a named, calm, real place | "You're under the White Cliffs of Dover." Title clears at 0:04.5 first, as POPSTAR's first caption comes after its title (@0:06) |
| S3 Flip + master clock | 0:08 | 7693494009494342945 @0:08; 7693617402180881697 @0:08 (HUD flips to a return clock + slow-motion factor at the event) | Return clock opens at the event, with an honest time factor | HUD flips to SEA BACK IN 57:00:00 / 1 HOUR PER SECOND; 57 s of screen = 57 h of story, closing at 1:05 (71%). A live SEA LEVEL meter starts falling at once, a quiet open loop under the wonder beat |
| S4 Wonder + body (one line) | 0:08.5-0:13.5 | 7693494009494342945 @0:09 + @0:15 (sensory wonder, then POV of your own hands); 7693617402180881697 @0:11 (personal HUD stat) | Harmless, sensory, on the viewer's own hands; HUD gives the number | POV hands hold an open book under the full giant Moon: "You can read a book by moonlight." HUD 120× BRIGHTER |
| S5 Rule with the pivot | 0:15 | 7693617402180881697 @0:21 ('But' opens the rule line) | "But" pivot + one plain-science rule | "But its tides are 1,000 times stronger." (1/d³) |
| S5 Implication + silence | 0:19-0:24.5 | 7693494009494342945 @0:25 (shorter line) + @0:28 (~4 s textless) | Short ominous line, then let the image deliver it | "So the sea keeps leaving." (5 words), then 3.7 s textless: dawn breaks over a draining Channel |
| S6 Ladder rung 1 (everyday object) | 0:24.5 | 7693494009494342945 @0:32 (everyday object first) | One object, one consequence | A cross-Channel ferry sits tilted on the dry chalk seabed (SEA LEVEL −91 M) |
| S6 Ladder rung 2 (famous geography) + dated precedent | 0:28 | 7694025665993100576 @0:21-0:27 (stat turned into a famous reference/setting); PLAYBOOK §12 dated precedent | Geography rung + real dated precedent | Map: the southern North Sea floor is dry; DOGGERLAND tag; HUD LAST THIS LOW: 20,000 YEARS AGO (the ice age) |
| S6 Ladder rung 3 (top rung, personal) | 0:31.5 | 7693494009494342945 @0:35 (3 s cadence peak, back to the person); 7694025665993100576 @0:35 (relocates "you" to an exact spot) | Return-to-you dip at the top rung | "You could walk to France from here." Map pins YOU (St Margaret's Bay) and CAP GRIS-NEZ, dotted 33 KM line |
| Full-frame interrupt | 0:34.5-0:39.5 | 7693617402180881697 @0:28-0:31 (black cut); 7693494009494342945 @0:40 (white-out wipes to space) | Total frame change before the scale jump | The giant Moon sets on the eastern horizon over the dry seabed, its centre crossing exactly at lowest water (0:36.5); black with stars at 0:38.5, music out |
| S7 Cosmic climb, live number | 0:39.5-0:52 | 7693494009494342945 @0:42 (live climbing HUD number) + @0:44-0:50 (rungs widen to space); 7693617402180881697 @0:43 | Space-wide view; a live number climbing; one consequence per caption | SEA LEVEL climbs back from −121 M while the rungs escalate: TV satellites flung from orbit → GPS yanked off course → the solid ground heaves (GROUND TIDE ~130 M, EST.) |
| S7 Race, nearly wordless | 0:52-1:05 | 7693617402180881697 @0:52-1:04 (clocks race with almost no captions) | Several HUD numbers moving, no captions | The clock, the climbing SEA LEVEL and, from 0:55, a falling MOON distance meter race; the foam line races the old tideline |
| S8 Return + false resolution | 1:05 | 7693494009494342945 @1:04-1:06; 7693617402180881697 @1:04-1:06 | Clock hits zero → "[X] BACK" → a reassuring line → "[place], [time] later" | SEA BACK / DOVER, 57 HOURS LATER, the exact 0:00 framing; "The tide is back at the old shoreline." |
| S9 Twist on the viewer + HUD equivalence | 1:08.3 | 7693494009494342945 @1:09-1:10 (the return makes it worse + one HUD equivalence) | Reversal 3 s after the false resolution; one equivalence line | "Then it climbs over where you stood." Drowned cutaway of your spot (18 M bar); DOVER, 67 HOURS LATER; LONDON FLOODS TWICE A WEEK |
| S9 Twist coda: plant reversed | 1:11 | 7693617402180881697 @1:09-1:10 (twist pays the 0:00 plant, then a longer-timescale number) | Plant paid + one future number, flagged | "And the Moon is falling toward us." MOON meter ticking down; TORN APART IN ~500 YEARS (EST.) |
| S10 Black + bookend + real fact | 1:13.5-1:20 | 7693494009494342945 @1:12-1:15; 7693617402180881697 @1:12-1:15 (fact held ~6 s); 7694025665993100576 @1:15 (real science closes the early loop) | Black beat, exact title repeat, one checkable fact | 12-word fact closes the 0:00 plant: the real Moon drifts 3.8 cm farther a year, timed by laser off Apollo 11's mirrors. CTA lives in the post caption only |

Pacing check against PLAYBOOK §3, §4, §9 and §12:
- Title 8 words, held 0:00-0:04.5; first caption 0:05; event at 0:08 (10%).
- 13 captions, 5-8 words (mean 6.6), 86 words = 64.5 wpm. Caption gaps 3-5.5 s (median 4.5 s). The ladder runs on 3.5 s gaps (0:24.5 / 0:28 / 0:31.5). Textless stretches: 0:20.8-0:24.5 (3.7 s, after the implication line), 0:34.5-0:39.5 (5 s, the interrupt), 0:52-1:05 (13 s, with three HUD numbers moving, inside PLAYBOOK's 10-15 s allowance).
- Something new on screen every ~3.5 s (caption, HUD line swap, cut, flip).
- Tracker moving from 0:00 to 1:13.5 with no gaps: distance counter (0:00-0:08), then the clock + SEA LEVEL meter (0:08-1:05), the MOON meter (0:55-1:13.5) and the SEA LEVEL meter to its +22 m peak (to 1:13.5).
- Master loop: SEA BACK IN clock 0:08 → 1:05 = 57 s = 71% of 80 s. Nested loops: the 0:00 plant (→ 0:55 meter → 1:11 caption → 1:14.8 fact); the falling SEA LEVEL under the wonder line (0:08.5 → paid by the 0:15 rule); low water (0:08 → 0:36.5 moonset); the "where does it stop?" climb (1:05 → 1:08.3). That makes 4 nested + master + title = ~4.5 loops/min.
- HUD: 57 words (ELECTRONS 43, NEUTRONS ~50); 10 distinct sublines: 2 persistent live meters (SEA LEVEL, MOON), 1 time factor, 1 callback stamp and 6 one-claim lines (no "X · Y" pairs). Every line is ≤ 28 characters, so each fits one row at 40 px mono.
- Numbers per minute: 21 distinct numeric readings / 1.333 min ≈ 16.

## The script

Layers: TITLE/END = centred serif card; CAPTION = lower-third italic serif (y ≈ 1400), one whole line at a time (TTS reads these lines only); HUD = top-left mono stack (x 70, y 250, width ≤ 640 so the Moon at x ≈ 800 stays clear), rows L (label), N (big figure), S1 (time factor / stamp), S2 (SEA LEVEL meter), S3 (MOON meter / one-claim line), S4 (one-claim line, twist only).

### Hook

- First line (TITLE, 0:00-0:04.5): **What if the Moon was _10 times closer_?** (the keyword in moon-silver accent)
- First visual (0:00): St Margaret's Bay under the White Cliffs at the end of dusk (blue hour): shingle foreground with a dark tideline of seaweed (the old-waterline marker), the chalk headland on the right, a flat calm Channel. A waxing gibbous Moon with a soft halo sits up and to the right above the cliff, and it is already swelling: 4× wider by 0:01. The HUD distance counter is already falling.

### Captions and HUD with timestamps

**[S1 — PREMISE CARD + APPROACH COUNTER] 0:00-0:08**
- 0:00 TITLE: What if the Moon was 10 times closer? (fades 4.1-4.5)
- 0:00 HUD L: THE MOON
- 0:00 HUD N: 384,400 KM → 38,440 KM. `d(s) = 1 / (1/384,400 + (1/38,440 − 1/384,400) · easeOutCubic(s/8))`, the same curve that scales the Moon disc (apparent size ∝ 1/d): 97,000 KM at 0:01, 62,000 at 0:02, 38,440 at 0:08
- 0:00 HUD S1: DRIFTS 3.8 CM AWAY EACH YEAR

**[S2 — PLACE YOU] 0:05**
- 0:05.0 CAPTION: You're under the White Cliffs of Dover.

**[S3 — FLIP + MASTER CLOCK] 0:08**
- 0:08.0 HUD L: SEA BACK IN
- 0:08.0 HUD N: 57:00:00, counting down 1 hour per second (minutes and seconds digits blur, like ms digits)
- 0:08.0 HUD S1: 1 HOUR PER SECOND
- 0:08.5 HUD S2 (live, to 1:13.5): SEA LEVEL −4 M (EST.), from the tide model, whole metres, sign shown

**[S4 — WONDER + BODY] 0:08.5-0:15**
- 0:08.5 HUD S3: 120× BRIGHTER (to 0:14.5)
- 0:10.0 CAPTION: You can read a book by moonlight.

**[S5 — RULE, THEN THE TURN] 0:15-0:24.5**
- 0:15.0 CAPTION: But its tides are 1,000 times stronger.
- 0:19.0 CAPTION: So the sea keeps leaving.
- 0:20.8-0:24.5 no caption (dawn; the sea slides off toward the horizon; SEA LEVEL passes −65 M at 0:19.8)

**[S6 — STAKES LADDER] 0:24.5-0:34.5**
- 0:24.5 CAPTION: Ferries sit on the bare seabed. (SEA LEVEL −91 M)
- 0:28.0 CAPTION: The North Sea floor is dry land. (−106 M)
- 0:28.0 HUD S3: LAST THIS LOW: 20,000 YEARS AGO (to 0:31.5)
- 0:31.5 CAPTION: You could walk to France from here. (−117 M; map line 33 KM)

**[INTERRUPT — MOONSET AT LOW WATER] 0:34.5-0:39.5**
- no caption. 0:34.6 the Moon's lower limb touches the eastern horizon; 0:36.5 SEA LEVEL bottoms at −123 M (EST.) as its centre crosses; 0:38.5 black with stars, HUD only

**[S7 — COSMIC CLIMB] 0:39.5-0:52**
- 0:39.5 CAPTION: TV satellites are flung from orbit. (SEA LEVEL climbing: −121 M)
- 0:44.0 CAPTION: GPS satellites get yanked off course.
- 0:48.5 CAPTION: Solid ground heaves like a tide.
- 0:48.5 HUD S3: GROUND TIDE ~130 M (EST.) (to 0:55)

**[S7 — RACE] 0:52-1:05**
- no caption. 0:55.0 HUD S3 (live, to 1:13.5): MOON 38,439.936 KM, ticking down 1.37 m per second
- 1:01 SEA LEVEL −20 M, 1:02 −14 M, 1:04 −5 M, clock to 00:00:00 at 1:05.0

**[S8 — RETURN] 1:05**
- 1:05.0 HUD L: SEA BACK (N freezes at 00:00:00, hidden at 1:08.3)
- 1:05.0 HUD S1: DOVER, 57 HOURS LATER
- 1:05.3 CAPTION: The tide is back at the old shoreline.

**[S9 — TWIST] 1:08.3-1:13.5**
- 1:08.3 HUD S1: DOVER, 67 HOURS LATER
- 1:08.3 HUD S2 freezes: SEA LEVEL +22 M OR MORE (EST.)
- 1:08.3 CAPTION: Then it climbs over where you stood.
- 1:09.3 HUD S4: LONDON FLOODS TWICE A WEEK (to 1:11)
- 1:11.0 CAPTION: And the Moon is falling toward us.
- 1:11.5 HUD S4: TORN APART IN ~500 YEARS (EST.)

**[S10 — BLACK + BOOKEND + REAL FACT] 1:13.5-1:20**
- 1:13.5 black, HUD hidden, music tail only
- 1:14.3 END: What if the Moon was 10 times closer?
- 1:14.8 END fact (held 5.2 s): REAL MOON: 3.8 CM FARTHER EACH YEAR · LASER-TIMED OFF APOLLO 11 MIRRORS
- 1:20 out (the last frame's text matches the first frame's title for the loop)

Caption word count: 86 words over 80 s = 64.5 wpm (caption-read VO). TTS spellings: "one thousand", "White Cliffs of Dover", "G P S", "T V".

### On-screen text (summary)

- TITLE / END: the 8-word question; "10 times closer" in accent. End fact: 12 words.
- HUD labels in order: THE MOON → SEA BACK IN → SEA BACK.
- HUD figures: distance 384,400 → 38,440 KM (0:00-0:08); clock 57:00:00 → 00:00:00 (0:08-1:05).
- HUD sublines (10): DRIFTS 3.8 CM AWAY EACH YEAR · 1 HOUR PER SECOND · SEA LEVEL meter (EST.) · 120× BRIGHTER · LAST THIS LOW: 20,000 YEARS AGO · GROUND TIDE ~130 M (EST.) · MOON meter · DOVER, 57 → 67 HOURS LATER · LONDON FLOODS TWICE A WEEK · TORN APART IN ~500 YEARS (EST.).
- Map/diagram labels (not counted above): ×1,000 · DOGGERLAND · YOU · CAP GRIS-NEZ · 33 KM · 3,700 KM · GPS 20,200 KM UP · 130 M / 110 M · 18 M.

## Shot list

Kit vocabulary: core layers (`rect`, `circle`, `text`, `svg`, `particles`, `component`), core camera (keyframes, `pushIn`, `drift`, `shake`), transitions (`cut`, `fade`, `whip`, `glitch`), `grade`, explainer kit (`explainer/Ocean` with `surface`, `explainer/Map` with `views`/`pins`/`zones`, `explainer/Tag`, `explainer/You`, `explainer/ScaleBar`), SFX from `studio/public/sfx`, music from `studio/public/music`. Captions are `text` layers (core `captions.enabled: false`, `audio.duckOn: 'none'`).

NEW what-if kit pieces (flat SVG/Canvas, no generated imagery), cut to the cheapest set that covers the script:
- `whatif/Hud` (shared with every whatif episode): rows L/N/S1-S4, mono font, live `track`/formula values, tabular numerals.
- `whatif/Moon`: disc + ~8 hand-drawn maria polygons, `phase` (with earthshine on the dark side), glow halo. Takes `sizeDeg`, `az`, `alt` and the shot's `fov`/`bearing`/`pitch`, and draws at `sizeDeg × 1080 / fovH` px. It sits on its own layer with `depth: 0`, so no camera move scales it.
- `whatif/Cliffs`: the one hero set (St Margaret's Bay). Owns the whole frame: a sky gradient driven by `clockHour` (blue hour, night, dawn, day, dusk), a star layer, the chalk headland, the shingle with the tideline wrack, a sea surface with horizon and moon-glitter dash band, and exposed seabed bands (wet chalk platform, sand, dark rock, dry seabed to the horizon) revealed by `seaLevel` (metres, from the tide model) so the water reads as retreating, not just falling. Takes `bearing` 144 (hero) / 125 (sea view) / 90 (east, moonset) and `fovH`.
- `whatif/Ferry`: one side-view hull SVG with a `tilt` prop.
- `whatif/OrbitView`: a plain blue Earth disc with a day/night terminator (no continents), the Moon's ring, a GEO dot ring, a GPS dot ring, a dashed Roche ring and a `scatter` track that throws the satellite dots off their rings. 9:16 layout: GEO ring 900 px across, Earth 136 px, Moon 37 px, Moon ring 820 px. Tags sit at opposite sides with leader lines.
- `whatif/DiagramCard` (shared with whatif-friction-off-5-seconds), `kind: 'groundTide'`: a cliff cross-section with a 110 M cliff bar next to a 130 M ground-tide arrow.
- Map extensions (in `explainer/Map`, so overlays never drift during a zoom): a `channel` region in `mapdetail.ts` (~150 hand-placed vertices: SE England, the Thames mouth, Pas-de-Calais, the Low Countries, Denmark, S Norway); a solid-fill style for the existing `zones` (3 hand-drawn bathymetry polygons: strait band, the Southern Bight + Dogger Bank, everything south of ~57°N except the Norwegian Trench); a `paths` prop (dotted line with a label).
- Fonts: one serif with italics (Source Serif 4) and one mono (JetBrains Mono) via @fontsource, installed with npm on the Spark and loaded in `waitForFonts`.

| t_start | t_end | shot | visual (kit vocabulary) | camera | SFX / music |
|---|---|---|---|---|---|
| 0:00 | 0:08 | hero wide, `Cliffs` bearing 144°, fovH 30° (vertical 51°), horizon at y 80% | `whatif/Cliffs` (`clockHour` 19:00, blue hour; the hook runs in real time; `seaLevel` 0; wrack line on the shingle). `whatif/Moon` at az 151°, alt 35° (x ≈ 800, y ≈ 215), `phase` 0.85 waxing, `sizeDeg` 0.52 → 5.78 on the 1/d ease-out (19 px with halo at 0:00, 75 px at 0:01, 208 px at 0:08). TITLE text layers 0:00-4.5. HUD distance mode | static (the Moon's growth is the motion) | music `documentary_pulse` from 0:00 (low); `tick` cues at a fixed 4 per second, 0:00-0:08; `riser` 5.0-8.0 |
| 0:08 | 0:09.5 | flip, same framing | Moon locks at 5.78°. `grade` snaps from blue hour to silver-blue (hue/saturate + screen overlay, vignette 0.2). Glitter band widens on the sea. HUD flips; SEA LEVEL meter appears at 0:08.5 | `shake` 0.35 s, amplitude 10 | `boom` 0:08; `underwater_rumble` low loop starts (music track) |
| 0:09.5 | 0:15 | POV, looking up SSE, fovH 40° | Lower third: two `explainer/You`-style POV hands holding an open book (svg), crisp moon-shadow of the thumb on the page. Upper half: the full giant Moon (az 148° → 135°, alt 34° → 29°: it slides ~12° left-and-down across the shot), bright sky, stars faded out | slow `pushIn` 0.3 | `whoosh` soft at 0:09.5 |
| 0:15 | 0:19 | sea view, `Cliffs` bearing 144°, fovH 30° | Night (02:00-06:00), last-quarter Moon. The waterline is far out on the chalk platform (−37 → −60 m); the Moon (alt 29° → 24°, moving left) above the sea. `svg` arrow from Moon to sea; `explainer/Tag` "×1,000" pops at 0:15.4 | `drift` | `stinger` low at 0:15 |
| 0:19 | 0:24.5 | sea view, `Cliffs` bearing 125°, fovH 30° | Dawn: `clockHour` 06:00 → 11:30; the sea drains to the horizon (−60 → −91 m), wet seabed bands turn dry; the dark new Moon with blue earthshine low in the ESE (alt 24° → 17°), beside the rising Sun. Textless from 0:20.8 | locked off | `whoosh_long` 0:19.5 |
| 0:24.5 | 0:28 | wide, `Cliffs` bearing 125°, daylight | `whatif/Ferry` sits on the dry chalk seabed ~2 km offshore, `tilt` 7°; crescent Moon pale in the day sky (alt 17°) | `pushIn` 0.4 toward the ferry | `door_creak` at 0:25 (low volume, used as hull groan) |
| 0:28 | 0:31.5 | map, North Sea | `explainer/Map` `views` [{t 0, lon 3.5, lat 54, zoom 30}], `channel` detail region, `zones` solid sand-coloured shelf polygons fading in over the blue (strait band, Southern Bight + Dogger Bank, shelf south of 57°N), Norwegian Trench stays blue; `explainer/Tag` "DOGGERLAND" over the Dogger Bank | `whip` in (up); map zoom 30 → 26 | `whoosh` on the whip |
| 0:31.5 | 0:34.5 | map, strait | `Map` `views` [{t 0, lon 1.48, lat 51.01, zoom 500}] (frame ≈ 50 km wide); `pins` YOU (1.38, 51.15) and CAP GRIS-NEZ (1.58, 50.87); `paths` dotted line between them drawing 0 → 1 over 1.5 s, label "33 KM"; the strait floor in sand colour, two small blue pools at the Fosses Dangeard | map zoom from 30 (cut) to 500 over 0.6 s, then hold | `pop` per pin; `click` as the line completes |
| 0:34.5 | 0:38.5 | east view, `Cliffs` bearing 90°, fovH 40° | Night 21:30 → 01:30: dry seabed to the horizon under hard light from a waning gibbous giant Moon (5.78°). Its lower limb touches the eastern horizon at 0:34.6, its centre crosses at 0:36.5 (lowest water), its last sliver goes at 0:38.4; the light drains from the scene as it sinks | locked | music fades out 0:36.5-0:38.5 |
| 0:38.5 | 0:39.5 | black | `rect` black + `particles` `stars` (sparse, slow twinkle); HUD only | none | `breath`-quiet; silence |
| 0:39.5 | 0:44 | space, `whatif/OrbitView` | Earth disc, Moon ring, GEO dot ring outside it; the Moon passes the GEO dots and they `scatter` off the ring; `Tag` "3,700 KM" on the gap with a leader line | `fade` in; slow `drift` | music `tension_pulse` from 0:39.5; `stinger` 0:39.5 |
| 0:44 | 0:48.5 | space, `OrbitView` zoomed on the GPS ring | GPS dots (26,560 km ring) wobble and drift off their dotted ring; `Tag` "GPS 20,200 KM UP" | `pushIn` 0.4 | `glitch` sfx at 0:45 (low) |
| 0:48.5 | 0:52 | diagram | `whatif/DiagramCard` `groundTide`: cliff cross-section, dashed "today" ground line, the ground block rising and sinking; bars "110 M" (cliff) and "130 M" (ground tide) | static | `underwater_rumble` swells |
| 0:52 | 0:58 | sea view, `Cliffs` bearing 125°, fovH 30° | Time-lapse 15:00 → 21:00 (sunset at 0:55 mid-shot, sky from `clockHour`): the sea floods back across the seabed toward shore (−72 → −37 m); the ferry still aground | locked | `clock_ticking` loop starts 0:52 (music track, `loop`) |
| 0:58 | 1:05 | low close, shingle, bearing 144°, fovH 50° | Night 21:00 → 04:00: the foam line races up the chalk platform and shingle toward the seaweed tideline from 0:00 (−37 → 0 m), reaching it at 1:05.0 | slow `pushIn` 0.3 | denser `tick` cues 1:02-1:05 (8 per second); `riser` 1:01-1:05 |
| 1:05 | 1:08.3 | callback, exact 0:00 framing (bearing 144°, fovH 30°) | `glitch` 0.2 s in. Night 04:00, empty sky where the Moon hung (it is below the horizon on the far side of Earth), sea exactly at the wrack line, calm | locked, matches 0:00 | `impact` 1:05; `clock_ticking` ends |
| 1:08.3 | 1:11 | drowned cutaway, same bearing | `explainer/Ocean` `surface` 0.22 (afternoon sky above, `skyTop`/`skyBottom` day blue), underwater: the drowned shingle, the wrack line and the cliff foot below; a dashed ghost `explainer/You` outline standing on the shingle; `explainer/ScaleBar` from the surface down to the ghost, "18 M" | slow `pushIn` 0.3 | `boom` muffled 1:08.3; `bubbles` low |
| 1:11 | 1:13.5 | space, `OrbitView` | The Moon's ring tightens on a visible spiral (exaggerated, as an animation of the trend); dashed Roche ring "18,000 KM"; MOON meter ticking in the HUD | `pushIn` 0.5 toward Earth | `riser` short; music out by 1:13.5 |
| 1:13.5 | 1:14.3 | black | `rect` black, HUD hidden | none | silence |
| 1:14.3 | 1:20 | end card | Centred serif title (keyword in accent), the small-caps fact appears at 1:14.8 and holds to 1:20 | static | soft `ding` 1:14.8 |

Production notes:
- Night is drawn as stylised navy with lit chalk (readable on a phone); the 0:00 blue hour and the 1:05 night share the composition but not the grade, on purpose (1:05 = 04:00, 57 h later, Moon set).
- The Moon's sky motion follows the tide model (about 2° per screen second). In every Cliffs shot its x/y comes from `az`/`alt` through the shot's `bearing`/`fovH`, so it never jumps between cuts.
- `gen_storyboard.py` in this folder holds the tide model and writes `storyboard.json` from these tables (validated against `studio/src/core/schema.ts`). Captions are text layers asking for `italic: true`, but core `TextLayer` has no italic flag yet (kit gap), so they render upright until it lands.
- Audio: music entries are `documentary_pulse` 0:00-0:38.5 and `tension_pulse` 0:39.5-1:13.5, plus `underwater_rumble` (0:08-0:38.5, loop) and `clock_ticking` (0:52-1:05, loop) as looped music-track beds with `duckTo` equal to their volume. All other cues are one-shots from `studio/public/sfx`. No pitched variants are needed.

## Fact sheet (sources to cite in the post / fact file)

- Moon mean distance 384,400 km; 10× closer = 38,440 km centre to centre (about 32,000 km above Earth's surface to the Moon's centre; its near side ~30,300 km up). Moon diameter 3,474 km.
- Apparent size from Dover at alt 35°: slant range 34,430 km → 5.78° (today 0.523°): **11× wider, ~120× the area**. Full moonlight scales with area: ~0.25 lux today → ~30 lux, enough to read by (a dim room). The HUD says 120×.
- Tidal force ∝ 1/d³: 10× closer = 1,000×. Equilibrium lunar tide today: 0.357 m × (3cos²θ − 1)/2. × 1,000 × 0.69 (1 + k₂ − h₂, the ocean relative to the flexing ground) = 246 m. At 51.15°N with the Moon at declination 0: high water +22 m (Moon at transit), low water −123 m (Moon on the horizon) (EST., equilibrium maths; real coasts amplify or damp it, and with today's orbital tilt the declination swings ±18-28° every orbit, which makes some high tides several times higher, roughly +25 to +150 m: hence "OR MORE").
- Timing: orbital period 27.32 d / 10^1.5 = 20.7 h, shorter than Earth's 23.93 h sidereal day, so the Moon moves west → east across the sky (it would rise in the west, like Phobos; it does not rise again inside this video). Apparent lunar day = 1/(1/20.7 − 1/23.93) = 153 h, so high water comes every 76.6 h (2.2 per week, "twice a week"). From an arrival with the sea at today's level: low water after 28.5 h, back to today's level after 57.0 h, high water after 66.8 h.
- Strait of Dover: 33.3 km at its narrowest (South Foreland, by St Margaret's Bay, to Cap Gris-Nez; Dover to Calais is ~40 km). Mostly 35-55 m deep, with channels to ~65 m and the Fosses Dangeard pits deeper still, so it is mostly dry below about −65 m (0:19.8) and stays dry for ~33 h (EST.), long enough to walk the 33 km (~7 h).
- Southern North Sea mostly under 50 m; Dogger Bank 15-36 m; North Sea mean depth ~95 m; the Norwegian Trench reaches ~700 m and stays wet. Sea level was ~120 m lower at the Last Glacial Maximum, about 20,000 years ago. Doggerland (the land bridge) was last fully flooded ~8,000 years ago (6500-6200 BCE). The HUD uses the 20,000-year date with the −120 m level.
- Dover harbour berths are ~10-12 m deep: every ferry is aground by −20 m (0:12). The cliffs at St Margaret's Bay and Dover reach ~110 m.
- Geostationary orbit: 42,164 km from Earth's centre (35,786 km altitude), only ~3,700 km outside the new Moon orbit. The Moon's Hill radius there is ~6,150 km, and at closest pass its pull on a GEO satellite (0.35 m/s²) beats Earth's (0.22 m/s²), so TV satellites are flung away, captured or crashed. GPS orbits at 26,560 km (20,200 km up): the Moon's pull reaches ~6% of Earth's at each pass (today ~0.007%), so the orbits are pumped off course within days (EST.).
- Solid-Earth tide: today ~0.13 m range at Dover from the Moon (h₂ ≈ 0.61). × 1,000 ≈ 130 m up and down every 38 h (EST.), more than the 110 m cliffs. Tidal stresses at that level (MPa) are comparable to earthquake stress drops (EST.; not claimed on screen).
- Falling Moon: inside synchronous orbit, tidal drag pulls a moon inward (Phobos is closing on Mars by ~1.8 m per century). Rate scales as a^−5.5: today's +3.8 cm/yr × 10^5.5 ≈ −12 km/yr at 38,440 km (1.37 m per hour). Integrating (a^6.5 falls linearly) gives ~490 years to the fluid Roche limit (~18,400 km) and ~492 to the rigid limit (~9,500 km): "~500 YEARS (EST.)". This assumes today's k₂/Q; at different tidal frequencies and with shelf-draining tides that could be several times faster or slower, so read it as hundreds to a few thousand years. Earth spins up as it absorbs the angular momentum (day ~16-20 h), but the synchronous orbit stays outside the Moon the whole way down, so the fall does not stop.
- Today the Moon recedes ~3.8 cm/year, measured by lunar laser ranging off retroreflectors left by Apollo 11 (July 1969), Apollo 14/15 and two Lunokhod rovers.
- Elevations: much of central London lies 5-20 m above sea level, and the Thames is tidal to Teddington, so a +22 m high water floods much of central London about twice a week (EST.).
- Dropped from screen, kept for comments: eclipses (the Moon would be 11× wider than the Sun; a central solar eclipse happens somewhere at nearly every new moon, every ~20.7 h, and a total lunar eclipse at nearly every full moon); weight change (directly under the Moon a 70 kg person weighs ~10 g less; at Dover with the Moon low, ~5 g more).
- Verify before render: strait depth wording, London elevation wording, GPS perturbation estimate.
