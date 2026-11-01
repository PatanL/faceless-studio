---
episode: whatif-earth-had-rings
niche: whatif
format: short 9:16 (1080x1920), caption-led, light TTS read of the captions
template: countdown-HUD (PLAYBOOK §1A) with a closing-distance master tracker instead of a return clock
working_title: "What if Earth had rings like Saturn?"
title_keyword: "rings like Saturn"
target_runtime_s: 78
target_runtime_range_s: [75, 80]
target_words_per_min:
  captions_vo: 62          # 81 caption words / 1.30 min. PLAYBOOK §9 Shorts median 56 (43-65); TTS read 60-70
  all_on_screen_text: 125  # captions + HUD + title/end cards. PLAYBOOK median 115 (103-131)
captions: 13 (mean 6.2 words, max 8)
time_lapse: "3 days per screen second from the flip (0:07 = JUL 1) to the solstice (1:04.7 = DEC 21): 173 days / 3 = 57.7 s"
hook: "7-word title over a ticking pre-event clock on Ocean Drive at dusk; the rings land at 0:07 (9%)"
references:
  - id: "7693494009494342945"
    short: ELECTRONS (@man_ia_c)
    url: https://www.tiktok.com/@man_ia_c/video/7693494009494342945
    views: 18200000
    outlier_score: 29.13
    why_chosen: >
      Highest-outlier Short and the cleanest copy of the 80 s template we are shooting: title + pre-event
      clock over a calm named place, hard style flip at ~10% with a time factor that makes the clock honest,
      wonder and body before danger, rule line -> shorter implication line -> textless break, scale-outward
      ladder with the fastest caption cadence, full-frame interrupt near the middle, HUD status lines
      carrying the cosmic stretch, a twist that reverses an earlier good thing, then black + exact title
      repeat + one true fact. Our beat grid sits on its timings.
  - id: "7694025665993100576"
    short: POPSTAR-100x (@man_ia_c)
    url: https://www.tiktok.com/@man_ia_c/video/7694025665993100576
    views: 4900000
    outlier_score: 7.84
    why_chosen: >
      The closest premise shape: a permanent change (no vanish-and-return), carried by a distance counter
      that closes on the viewer from frame 1, a location tag in the HUD the viewer doesn't understand yet
      (its floor number; our latitude 25.8 N), a counter that reaches "here" and pays the tag off (T7, you
      are exactly where it lands), and a real-science end card that confirms the premise is grounded.
  - id: "7696143265405488416"
    short: PI=3 (@man_ia_c)
    url: https://www.tiktok.com/@man_ia_c/video/7696143265405488416
    views: 3900000
    outlier_score: 6.24
    why_chosen: >
      One geometric rule pushed through a chain of exact, checkable numbers (ours: ring radii x Sun angle ->
      the shadow's latitude on every date). Borrowed: chapter labels in the HUD every 10-18 s, "every/no"
      absolutes in the captions, the drop from planet scale back to the exact local place, "the reset
      doesn't fix it" ending, and a real dated historical fact on the end card.
playbook: research/corpus/whatif/PLAYBOOK.md §1A (S1-S10), §2 H4 + H3-style answer-in-frame, §4 loops, §5 closing-distance + scale-outward ladders, §6 T3/T7/T1, §9 Shorts pacing, §12 checklist
fact_notes:
  - "Premise (one rule): Earth gets Saturn's main rings scaled by planet radius. Saturn R = 60,268 km; B ring 92,000-117,580 km (1.527-1.951 R), Cassini Division to 122,170 km (2.027 R), A ring to 136,775 km (2.269 R). On Earth (R = 6,371 km): 9,730-14,460 km from the centre = 3,360-8,080 km up; main rings 4,730 km wide. All inside Earth's Roche limit for rock, so they stay a ring."
  - "Saturn's main rings are typically ~10 m thick (NASA Saturn facts: 'about 30 feet'). Width/thickness = 4,730 km / 10 m = 473,000:1; a 0.1 mm sheet of paper at that ratio is 47 m across."
  - "Rings settle over the equator because the planet's equatorial bulge torques them into that plane (same reason Saturn's rings sit over its equator)."
  - "Circular orbital speed v = sqrt(GM/r), GM = 398,600 km^3/s^2: 23,000 km/h at the B inner edge, 18,900 km/h at the A outer edge, ~20,700 km/h mid-ring. A satellite crossing the ring steeply at r = 1.9 R meets the grains at up to ~8 km/s (sqrt(2) x 5.74 km/s); a 5.56 mm rifle bullet is ~0.95 km/s."
  - "Sky view from Ocean Drive, Miami Beach (25.79 N), looking due south: B inner edge at 29.4 deg elevation, A outer edge at 46.6 deg; band 17.1 deg = 33 full Moons (0.52 deg each)."
  - "Ringlight EST.: the lit band covers ~0.5 sr of sky vs the full Moon's 0.00006 sr; even at a tenth of the Moon's surface brightness it beats full moonlight (0.25 lux) by ~100x, enough to cast a clear shadow. Labelled EST. on screen."
  - "Shadow model (noon meridian, Sun declination d from the NOAA series): a winter-hemisphere latitude phi is shaded by ring radius rho = cos(phi) + sin(phi)/tan(d) (Earth radii). Computed by scratch script rings.py. Dates for 25.79 N in 2026: A-ring edge arrives NOV 13, Cassini Division NOV 28, B ring DEC 7 to JAN 6, last shadow JAN 30. At the DEC 21 solstice, rho(noon) = 1.905 (B ring) and stays inside the B ring until ~4.9 h either side of noon, i.e. almost all of Miami's 10.5 h of daylight."
  - "Shadow-edge arrival dates (noon, A outer edge): Bogota 4.71 N OCT 4, Panama City 8.98 N OCT 12, Caracas 10.49 N OCT 15, Havana 23.11 N NOV 8, Miami Beach NOV 13. Distance from Miami to the nearest shadow edge along the meridian (111.19 km/deg): JUL 1 4,400 km, AUG 6 3,920, SEP 23 2,880 (a thin line on the equator), OCT 17 1,560, OCT 29 870, NOV 10 150, NOV 13 0."
  - "In July the shadow lies on the southern (winter) hemisphere, 13.8-40.1 S at noon on JUL 1 (Rio 22.9 S, Johannesburg 26.2 S, Sydney 33.9 S all inside)."
  - "Light through the rings EST.: normal optical depth B ~1.5 (range 0.5-5), A ~0.5, Cassini ~0.1; slant path factor 1/sin(d). Transmitted at noon: A ring ~19-28% (show ~25%), Cassini ~72-78% (show ~75%), B ring ~1-2% at the solstice (show ~2%). Labelled EST. on screen."
  - "Equinox: the Sun sits in the ring plane, so the rings are lit edge-on and go nearly dark, and the shadow shrinks to a line on the equator. Real precedent: Saturn's equinox on 11 Aug 2009 (Cassini imaged the rings almost vanishing). 2026 September equinox: SEP 23 00:05 UTC."
  - "Unlit side: from the September to the March equinox the Sun lights the rings' south face, so anyone north of the equator sees the unlit north face at night (as Cassini saw Saturn's rings from the unlit side). 2027 March equinox: MAR 20."
  - "Satellite band: any orbit that crosses the ring plane between 3,360 and 8,080 km altitude passes through the ring. Starlink (~550 km) is below it; GPS (20,200 km) and geostationary (35,786 km) are above it, but every orbit's plane crossing has to avoid the band."
  - "End fact: Tomkins, Martin & Cawood (2024), Earth and Planetary Science Letters 646, 118991: 21 impact craters from ~466 Ma all sit within 30 deg of the Ordovician equator, consistent with a debris ring; the authors propose its shade may have contributed to the Hirnantian glaciation (~445 Ma)."
kit_gaps: >
  Needs the whatif countdown-HUD pieces (shared with the other whatif backlog scripts, not yet in
  studio/src/kits): whatif/Hud (small-caps label, big mono number with live track, two sublines, date row
  that ticks), whatif/SerifCaption (italic serif lower third), whatif/TitleCard (serif, accent keyword,
  icon slot). New for this episode: whatif/OceanDrive (looking south down Ocean Drive: pastel Art Deco
  hotel fronts with neon on the right, palms + Lummus Park lawn + beach on the left, southern sky above the
  vanishing point; `time` dusk/day/night, `shade` 0..1), whatif/RingArch (sky arch from east to west
  horizon, B ring cream, Cassini gap, A ring grey, `lit` -1..1 where -1 = unlit side, 0 = edge-on dark,
  `earthShadow` notch at midnight, `shadowEdge` dim band sweeping across the frame), whatif/RingGlobe (flat
  side-view diagram: Earth disc with lat lines, ring drawn edge-on as a line through the equator, Sun icon on
  a seasonal arc, parallel sunbeams, shadow band on the far hemisphere), whatif/LatBand overlay for
  explainer/Map (shaded latitude band with soft edges, `from`/`to` tracks), whatif/PaperSheet (thin sheet
  vs a scale figure), whatif/GrainField (Canvas particles streaming past a small satellite icon). Reuse
  explainer/You (poses, shadow), explainer/Map (views, pins, highlight), explainer/Stat, core camera
  presets/keyframes/shake, core transitions (cut, whip, dipBlack, glitch), core grade.
palette: >
  Before the flip: warm dusk flat palette (sky #F6A96B -> #7B5EA7, hotel pastels mint #9FE3C9, flamingo
  #F7A1C4, lemon #F9E79F, palm #2E6B4F, sand #EAD7AE). Rings: B ring cream #EADFC4, A ring #CFC8B8,
  Cassini gap transparent, unlit side #22252B with a faint #6E6A62 rim. Ring shadow: grade desaturate 0.5
  + blue-grey tint #5B6B7A, opacity follows the transmission EST. Accent for the keyword and HUD numbers:
  ring gold #E8B04A. End card on near-black #0B0D10.
post_caption_cta: "Which city would you move to: under the ring, or out of its shadow?"
---

# What if Earth had rings like Saturn?

Our own script: devices and timing come from the three references, the story, place and every line are new. They use a Central Park picnic, a giant walking toward an office and a park where circles break; ours is a Miami beach street watching a shadow arrive across a calendar.

## Beat alignment

| # | Our beat | Our t | Reference id + t | Device borrowed | How we adapt it |
|---|---|---|---|---|---|
| S1 | Premise card + pre-event clock | 0:00-0:07 | 7693494009494342945 0:00 (title + HUD counting to the event); 7696143265405488416 0:00 (calm scene seeded with props that change later) | 7-word what-if title, accent keyword, icon; HUD counts down over a calm place before anything happens | Title "rings like Saturn" in ring gold with a ringed-planet glyph; HUD "RINGS FORM IN 0:07.0"; subline "SATURN'S RINGS, SCALED TO EARTH"; the empty southern sky above the street is the prop that changes |
| S1b | Location tag plant | 0:04 | 7694025665993100576 0:35 (HUD tag "level with floor 23" explained later) | A precise number in the HUD the viewer can't read yet | Subline 2 "JUL 1 · MIAMI BEACH · 25.8°N"; the latitude is paid off at 0:52 when the shadow edge lands on exactly 25.8°N |
| S2 | Place you | 0:04 | 7693494009494342945 0:05; 7694025665993100576 0:06 | Second person + a famous real place, calm | Ocean Drive at dusk, camera looking south down the street so the whole southern sky is in frame |
| S3 | Flip | 0:07 | 7693494009494342945 0:08 (hard style change + clock flip + time factor) | Clock hits zero -> hard visual change + hit; HUD flips to the master tracker with a time factor that makes the runtime honest | The arch slams across the sky with a boom; HUD flips to "RING SHADOW 4,400 KM SOUTH" + date row "JUL 1 · TIME-LAPSE 3 DAYS / SEC" (173 days = 57.7 s, so DEC 21 lands at 1:04.7) |
| S4 | Wonder, then body | 0:08-0:17 | 7693494009494342945 0:09-0:15 (harmless sky effect, then your own body) | Beautiful harmless effect first; the second one is on the viewer's body (screenshot moment) | Arch 33 Moons wide; then at midnight the ringlight throws your own shadow on the pavement. This brightness is the plant the twist reverses |
| S5 | Rule, shorter implication, silence | 0:18-0:26.5 | 7693494009494342945 0:21-0:28; 7696143265405488416 0:09 (one rule that drives every later number) | Plain-science rule line -> shorter line that implies the consequence -> ~4 s textless break | Rule: rings sit over the equator. Implication (5 words): the Sun moves. Textless: side-view diagram, the Sun icon slides down its seasonal arc and the shadow band climbs toward the equator while the date ticks into August |
| S6 | Scale-outward ladder | 0:26.5-0:35 | 7693494009494342945 0:32-0:35 (scale inversion, fastest cadence); 7696143265405488416 0:13-0:31 ("every/no" absolute lines) | Smallest-to-biggest rungs, one idea and one number each, captions ~3.5 s apart, last rung an absolute | Ring as paper (47 m sheet) -> grain speed (20,000 km/h) -> "no satellite" absolute with a bullet comparison in the HUD |
| S7 | Full-frame interrupt | 0:35-0:37 | 7693494009494342945 0:40 (white-out); 7696143265405488416 0:34 (hard cut + chapter label) | Whole frame changes to reset attention before the next scale; chapter label | Equinox: the arch goes dark edge-on and the frame drops to near-black with one thin lit line; chapter "SEP 23 · EQUINOX" plus the real Saturn 2009 precedent in the subline |
| S8 | Planet climb with closing distance | 0:37-0:52 | 7694025665993100576 0:00-0:35 (distance counter closing on you); 7693494009494342945 0:42-0:56 (HUD status lines carry a near-captionless stretch) | Live number falls toward the viewer; terse HUD status lines; captions thin out (11 s gap) | Map of the Americas with a shaded latitude band sweeping north; HUD stamps BOGOTÁ, PANAMA, CARACAS, HAVANA as the counter drops 2,880 -> 0 KM; one caption names Havana and then "you" |
| S9 | Contact: the tag pays off | 0:52 | 7694025665993100576 0:59-1:02 (counter reaches HERE, location tag explained) | Counter hits zero on the exact place; the earlier tag makes sense | HUD "RING SHADOW: ON YOU / NOV 13 · 25.8°N · A RING · NOON LIGHT ~25%"; the shadow edge rolls up Ocean Drive, no caption |
| S10 | False relief -> worse | 0:57-1:00 | PLAYBOOK T3 (one-word false resolution then "except"), corpus 6oZ9fdM0n50; 7693494009494342945 1:05 (reassuring line before the twist) | Short relief line, then the real problem with no words | The Cassini Division lets the sun back for 9 days ("A gap. The Sun is back."), then the B ring shadow drops the street to near-dark at 1:00 |
| S11 | Master loop closes + callback | 1:04.7-1:08 | 7693494009494342945 1:04-1:06 (clock completes, callback stamp naming the place); 7696143265405488416 0:56 (planet number brought back to the local place) | Tracker reaches its end; stamp names the opening place | Date row lands on DEC 21; "OCEAN DRIVE, DEC 21" stamp; caption calls back the street at noon |
| S12 | Twist | 1:08-1:11 | 7693494009494342945 1:09 (the good outcome flips into its opposite); 7696143265405488416 1:05 (the reset doesn't undo it) | One caption + one HUD equivalence; a planted good thing reverses | The ringlight planted at 0:13 is gone: at night Miami sees the rings' unlit side, a black arch with no stars; HUD "SHADOW GONE JAN 30 · BACK EVERY NOVEMBER" |
| S13 | Black + bookend + real fact | 1:11-1:18 | 7693494009494342945 1:12-1:20; 7696143265405488416 1:12-1:20 (dated historical fact); 7694025665993100576 1:15 (fact confirms the premise is real science) | ~1.5 s black, exact title repeat for the loop, one small-caps true dated fact; CTA only in the post caption | Tomkins et al. 2024: Earth may have had a ring 466 million years ago, and its shade may have helped start an ice age |

Pacing check against PLAYBOOK §9 and §12 (Shorts):

| Check | Target | Ours |
|---|---|---|
| Title | 7-9 words, held 5-8 s | 7 words, 0:00-0:05 |
| Event | ~8 s (10%) | 0:07 (9%) |
| Captions | 10-13, ≤8 words, mean ~6-7 | 13, mean 6.2, max 8 |
| Caption gaps | median 5 s (4-6), 10-15 s only while a HUD number moves | 4 / 5 / 5 / 4 / 4.5 / 3.5 / 3 / 4 / 11 / 9 / 8 / 3.5, median 4.3 s; the 11 s gap runs while the distance counter falls and city stamps pop |
| New on-screen element | every ~3.8 s | every ~3.3 s (captions, HUD sublines, chapter stamps, date row always ticking) |
| Second person | 1 place line + 1 body line before 25% | 0:04 place, 0:13 body (17%); 3 of 13 captions in total (23%) |
| Master loop | opens in hook, closes at 70-80% | shadow tracker 0:07 -> contact 0:52 -> DEC 21 at 1:04.7 (83%); spans 74% of runtime |
| Interrupt near midpoint | white-out or full frame | equinox black at 0:35 (45%) |
| Twist + outro | twist ~85%, black + title + fact last 10% | twist 1:08 (87%); outro 1:11-1:18 (9%) |
| Real numbers + precedent | every stat on screen; ≥1 dated precedent | ~20 numbers/min in HUD; Saturn equinox 11 Aug 2009; Tomkins 2024 / 466 Ma |
| Loops open at once | always ≥2 | title (0:00-1:11), pre-event clock (0:00-0:07), 25.8°N tag (0:04-0:52), shadow tracker (0:07-1:04.7), ringlight plant (0:13-1:08), "then you" (0:48-0:52), Cassini relief (0:57-1:00) |

## Hook

- **First line (title card at 0:00, also the first VO line):** What if Earth had **rings like Saturn**?
- **First visual (frame 1):** flat-vector Ocean Drive at dusk, seen from the middle of the street looking due south: mint, flamingo-pink and lemon Art Deco hotel fronts with neon fins on the right, a row of palms and the beach on the left, a classic convertible parked at the kerb, and above the vanishing point a wide, empty violet-orange southern sky. The serif title sits in the upper third with "rings like Saturn" in ring gold and a small ringed-planet glyph; the top-left HUD is already ticking: RINGS FORM IN 0:07.0.

## Script

Captions are the voiceover: Kokoro TTS (calm narrator, ~62 wpm with the holds below) reads each caption once as it appears ("km" read as kilometres, "km/h" as kilometres an hour). HUD, chapter and end-card text is on screen only. Timestamps are screen time; the date row means screen second t shows JUL 1 + 3 × (t − 7) days.

**S1 · Premise card + pre-event clock (0:00-0:07)**
- 0:00 TITLE (held to 0:05): What if Earth had **rings like Saturn**?
- 0:00 HUD label: RINGS FORM IN 0:07.0 (counts down with ms digits)
- 0:00 HUD subline: SATURN'S RINGS, SCALED TO EARTH
- 0:04 HUD subline 2: JUL 1 · MIAMI BEACH · 25.8°N

**S2 · Place you (0:04)**
- 0:04 CAPTION 1: You're on Ocean Drive, Miami Beach.

**S3 · Flip (0:07)**
- 0:07 (no caption) the arch slams in from both horizons and meets overhead-south.
- 0:07 HUD label flips: RING SHADOW · 4,400 KM SOUTH (falls along the track in the fact notes)
- 0:07 HUD date row: JUL 1 · TIME-LAPSE 3 DAYS / SEC

**S4 · Wonder, then body (0:08-0:17)**
- 0:08 CAPTION 2: An arch 33 Moons wide fills the south.
- 0:09 HUD subline: 3,400 TO 8,100 KM UP · 29° TO 47° HIGH
- 0:13 CAPTION 3: At midnight, ringlight throws your shadow.
- 0:14 HUD subline: BRIGHTER THAN A FULL MOON (EST.)
- 0:15 HUD subline 2: SHADOW NOW OVER RIO, JOBURG, SYDNEY

**S5 · Rule, implication, silence (0:18-0:26.5)**
- 0:18 CAPTION 4: Rings always circle right above the equator.
- 0:19 HUD subline: EARTH'S BULGE HOLDS THEM THERE
- 0:22 CAPTION 5: The Sun doesn't stay there.
- 0:23 HUD subline: THE SUN SWINGS 47° NORTH-SOUTH EACH YEAR
- 0:22.5-0:26.5 (no caption) the diagram's Sun slides down its arc and the shadow band climbs toward the equator; date row ticks through AUG.

**S6 · Scale-outward ladder (0:26.5-0:35)**
- 0:26.5 CAPTION 6: 4,700 km wide. Ten metres thick.
- 0:27.5 HUD subline: AS PAPER: ONE SHEET, 47 M ACROSS
- 0:30 CAPTION 7: Its grains orbit at 20,000 km/h.
- 0:33 CAPTION 8: No satellite can cross that band.
- 0:33.5 HUD subline: GRAINS HIT AT ~8 KM/S · 8× A RIFLE BULLET

**S7 · Full-frame interrupt (0:35-0:37)**
- 0:35 (no caption) hard cut: the arch goes dark, the frame drops to near-black with one thin lit line across it.
- 0:35 HUD chapter: SEP 23 · EQUINOX · RINGS EDGE-ON, DARK
- 0:35.5 HUD subline 2: SATURN'S DID THIS ON 11 AUG 2009

**S8 · Planet climb with closing distance (0:37-0:52)**
- 0:37 CAPTION 9: Now the shadow heads north.
- 0:38 HUD subline: CLOSING ~55 KM A DAY
- 0:38.7 HUD stamp: OCT 4 · BOGOTÁ
- 0:41.3 HUD stamp: OCT 12 · PANAMA CITY
- 0:42.3 HUD stamp: OCT 15 · CARACAS
- 0:48 CAPTION 10: Havana is next. Then you.
- 0:50.3 HUD stamp: NOV 8 · HAVANA
- 0:50.3-0:52 (no caption) the counter runs 300 → 0 KM.

**S9 · Contact (0:52)**
- 0:52 HUD label: RING SHADOW · ON YOU
- 0:52 HUD subline: NOV 13 · 25.8°N · A RING · NOON LIGHT ~25% (EST.)
- 0:52-0:57 (no caption) the shadow edge rolls up Ocean Drive from the south; neon signs flicker on in the middle of the day.

**S10 · False relief, then worse (0:57-1:04.7)**
- 0:57 CAPTION 11: A gap. The Sun is back.
- 0:57 HUD subline: NOV 28 · CASSINI DIVISION · NOON LIGHT ~75%
- 1:00 (no caption) the B ring's shadow lands; the street drops to near-dark.
- 1:00 HUD subline: DEC 7 · B RING · NOON LIGHT ~2% (EST.)
- 1:02 HUD subline 2: IN SHADOW ~9 OF 10.5 DAYLIGHT HOURS

**S11 · Master loop closes + callback (1:04.7-1:08)**
- 1:04.7 HUD date row lands: DEC 21 · SOLSTICE (time-lapse stops)
- 1:05 CAPTION 12: Noon on Ocean Drive looks like dusk.
- 1:05.5 HUD subline: OCEAN DRIVE, DEC 21, 12:00

**S12 · Twist (1:08-1:11)**
- 1:08.5 CAPTION 13: And tonight, the rings show their dark side.
- 1:09 HUD subline: LIT SIDE FACES SOUTH UNTIL MAR 20
- 1:10 HUD subline 2: SHADOW GONE JAN 30 · BACK EVERY NOVEMBER

**S13 · Black + bookend + fact (1:11-1:18)**
- 1:11-1:12.5 black, silence.
- 1:12.5 END: What if Earth had **rings like Saturn**? (exact title repeat, same gold keyword)
- 1:13.5 END fact (small caps, held to 1:18): 466 MILLION YEARS AGO, EARTH MAY HAVE HAD A RING · ITS SHADE MAY HAVE HELPED START AN ICE AGE

**Post caption (description, not on screen):** Saturn's rings, scaled to Earth and parked over Miami Beach. Summer nights glow bright enough to cast your shadow. Then the equinox switches them off, and their shadow starts walking north, city by city, about 55 km a day. By December the street is dim at noon, and at night the rings turn their black side toward you. Which city would you move to: under the ring, or out of its shadow? #whatif #space #saturn #pov #simulation

## Shot list

Times are screen seconds. Kit names: core = studio/src/core (camera presets pushIn/pullOut/panLeft/panRight/panUp/panDown/drift, keyframes, shake; transitions cut/whip/dipBlack/glitch; grade); explainer = studio/src/kits/explainer; whatif = the pieces listed in `kit_gaps`. whatif/Hud (top-left), whatif/SerifCaption (lower third) and title/end cards are screen-locked layers over every shot. SFX from studio/public/sfx.

| # | t_start | t_end | Shot type | Visual (kit vocabulary) | Camera move | SFX |
|---|---|---|---|---|---|---|
| 1 | 0.0 | 4.0 | Establishing, street level looking due south | whatif/OceanDrive `time: dusk`: pastel hotel fronts + neon fins right, palms + beach left, convertible at kerb, empty violet-orange sky over the vanishing point; whatif/TitleCard upper third ("rings like Saturn" gold, ringed-planet glyph); whatif/Hud countdown from 7.0 + subline "SATURN'S RINGS, SCALED TO EARTH" | core `drift` amount 0.3 | clock_ticking (0.4, to 7.0); soft surf bed (music stem) |
| 2 | 4.0 | 7.0 | Same frame, slight push | Title fades by 5.0; explainer/You pose `stand`, small, mid-sidewalk under a palm, looking up-south; HUD subline 2 "JUL 1 · MIAMI BEACH · 25.8°N" at 4.0; Caption 1 | core `pushIn` amount 0.4 | tick at 6.0, 6.5, 6.8 |
| 3 | 7.0 | 8.0 | Same frame, the flip | Hard cut at 7.0: whatif/RingArch `lit: 1` sweeps in from both horizons and locks (B cream, Cassini gap, A grey), sky grades a step deeper; HUD flips to "RING SHADOW 4,400 KM SOUTH" + date row "JUL 1 · TIME-LAPSE 3 DAYS / SEC" | core shake at 7.0 (amp 12, 0.35 s) | boom (0.9) + whoosh_long (0.5) at 7.0; drone bed starts (0.2) |
| 4 | 8.0 | 12.5 | Tilt up to the arch | whatif/RingArch fills the upper 60%; a small explainer/Map-style Moon disc pops beside it, then 33 copies tile across the band's width (count-up with explainer/Stat "33") ; Caption 2; HUD subline "3,400 TO 8,100 KM UP · 29° TO 47° HIGH" at 9.0 | core keyframes: tilt up (y −260), zoom 1.0 → 0.92 | pop ×6 staggered (0.2) at 9.5-11 |
| 5 | 12.5 | 18.0 | Night, medium on you | whatif/OceanDrive `time: night`, streetlights off; RingArch glowing with a dark Earth-shadow notch at the meridian; explainer/You casts a long crisp shadow on the pavement (shadow layer skewed from the arch's east side); Caption 3; HUD sublines at 14.0 and 15.0 | core keyframes: pan down to the figure (y +200), slow `drift` | breath (0.25) at 13.2; ding (0.2) at 15.0 |
| 6 | 18.0 | 22.5 | Diagram card, side view | whatif/RingGlobe: Earth disc with latitude lines, ring edge-on as a gold line through the equator, Sun icon upper-left (July), parallel beams, shadow band on the southern hemisphere; a small "BULGE" arrow callout (core callout `label`); Caption 4; HUD subline at 19.0 | core `pullOut` amount 0.5 | whoosh (0.3) at 18.0 |
| 7 | 22.5 | 26.5 | Same diagram, textless | Caption 5 at 22.0, then no caption: the Sun icon slides down its seasonal arc (+23° → +10°), beams tilt, the shadow band climbs toward the equator; HUD date row ticks into AUG; HUD subline "THE SUN SWINGS 47° NORTH-SOUTH EACH YEAR" at 23.0 | static, then core `pushIn` amount 0.3 | riser (0.35) 22.5 → 26.5 |
| 8 | 26.5 | 30.0 | Scale card | whatif/PaperSheet: a single sheet edge-on, then turned flat; explainer/You at scale beside it, with an explainer/ScaleBar "47 M" under the sheet; Caption 6; HUD subline "AS PAPER: ONE SHEET, 47 M ACROSS" at 27.5 | core `pullOut` amount 0.8 | tick at 26.5; whoosh (0.25) at 28.0 |
| 9 | 30.0 | 33.0 | Ring-plane close-up | whatif/GrainField: icy grains of mixed size streaming right-to-left across the frame with motion streaks; HUD keeps the shadow distance ticking; Caption 7 | core `panLeft` amount 0.7 | whoosh_long (0.4) at 30.0; static (0.15) bed |
| 10 | 33.0 | 35.0 | Same field, satellite crossing | A small satellite icon dives steeply into the grain stream and is peppered: panels shred into flecks; HUD subline "GRAINS HIT AT ~8 KM/S · 8× A RIFLE BULLET" at 33.5; Caption 8 | core shake (amp 8, 0.6 s) at 34.0 | impact (0.5) at 34.0; glitch (0.3) at 34.2 |
| 11 | 35.0 | 37.0 | Full-frame interrupt | Hard cut to near-black #0B0D10: RingArch `lit: 0` reduced to one thin lit line across the frame, faint grey band behind it; HUD chapter "SEP 23 · EQUINOX · RINGS EDGE-ON, DARK" at 35.0, subline 2 at 35.5 | none (locked) | stinger (0.6) at 35.0; music drops out |
| 12 | 37.0 | 44.0 | Map, wide on the Americas | explainer/Map `views` centred lon −75, lat 10, zoom on the Caribbean + northern South America; whatif/LatBand shading from the equator, its north edge sliding up (track from the fact notes); explainer/Map `pins` pop grey as the edge passes Bogotá (38.7), Panama City (41.3), Caracas (42.3) with matching HUD stamps; Caption 9 at 37.0; HUD subline "CLOSING ~55 KM A DAY" at 38.0 | core keyframes: pan up (lat drift north), zoom 1.0 → 1.15 | sonar_ping (0.3) on each pin; underwater_rumble low bed (0.25) 37 → 52 |
| 13 | 44.0 | 52.0 | Map, tighter on Cuba and Florida | Same map, `views` to lon −80.5, lat 24.5; LatBand edge crosses the Florida Straits; Havana pin greys at 50.3 (HUD stamp "NOV 8 · HAVANA"); a gold pin on Miami Beach pulses; HUD distance 1,200 → 0 KM; Caption 10 at 48.0 | core `pushIn` amount 0.9 | heartbeat_slow (0.35) from 48.0; sonar_ping at 50.3 |
| 14 | 52.0 | 57.0 | Street, day, looking south | whatif/OceanDrive `time: day`; the shadow edge (RingArch `shadowEdge`) rolls up the street from the vanishing point toward camera, grade to ~25% light with blue-grey tint; neon fins flicker on; explainer/You looks up; HUD "RING SHADOW · ON YOU" + subline at 52.0 | core keyframes: slow pull back as the edge approaches (zoom 1.1 → 1.0) | impact (0.6) at 52.0; drone swells |
| 15 | 57.0 | 60.0 | Same street, relief | Grade lifts to ~75%: a bright stripe of sunlight (the Cassini gap) slides across the street; a few figures step back into the light; Caption 11; HUD subline "NOV 28 · CASSINI DIVISION · NOON LIGHT ~75%" | core `drift` amount 0.3 | ding (0.35) at 57.0; music bed returns softly |
| 16 | 60.0 | 64.7 | Same street, the B ring lands | Grade drops to ~2%: near-dark noon, palms in silhouette, only neon and car headlights; HUD sublines at 60.0 and 62.0; no caption | core `pushIn` amount 0.6; shake (amp 6, 0.4 s) at 60.0 | boom (0.6) at 60.0; heartbeat (0.4) 60 → 64.7; clock_ticking (0.3) 62 → 64.7 |
| 17 | 64.7 | 68.0 | Wide, noon in the dark | Date row lands "DEC 21 · SOLSTICE" and stops; a street clock on a hotel front reads 12:00 under a dim sky; Caption 12 at 65.0; HUD subline "OCEAN DRIVE, DEC 21, 12:00" at 65.5 | none (locked) | tick (0.5) at 64.7, then silence except surf |
| 18 | 68.0 | 71.0 | Night, tilt up to the arch | whatif/OceanDrive `time: night`; RingArch `lit: −1`: a black arch cutting out the stars with only a faint grey rim; explainer/You standing where the ringlight shadow was in shot 5, now no shadow; Caption 13 at 68.5; HUD sublines at 69.0 and 70.0 | core keyframes: tilt up (y −220) | stinger (0.4) at 68.5; drone fades |
| 19 | 71.0 | 72.5 | Black | Black frame, HUD hidden | none | silence |
| 20 | 72.5 | 78.0 | End card | whatif/TitleCard on #0B0D10: exact title repeat with the gold keyword and glyph; small-caps fact at 73.5 (two lines), held to the end | none | ding (0.25) at 72.5 |

Audio: music bed (core audio `music`, volume 0.3, duckTo 0.12 under VO) warm and slow 0-7 s, wider and brighter after the flip, cut at the equinox (35.0), low and tense through the shadow approach, a brief lift at the Cassini gap (57.0), gone at the B ring (60.0), soft return for the end card. TTS reads only the 13 captions, each starting at its caption time.
