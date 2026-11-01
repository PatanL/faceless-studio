---
episode: whatif-earth-had-rings
niche: whatif
format: short 9:16 (1080x1920), caption-led, light TTS read of the captions only (title, HUD and end card are never read)
template: countdown-HUD (PLAYBOOK §1A) with a days-to-contact master countdown, a calendar scrubber and chapter labels; own outro (black frame keeps the return countdown ticking)
working_title: "What if Earth had rings like Saturn?"
title_keyword: "rings like Saturn"
target_runtime_s: 79
target_runtime_range_s: [75, 80]
target_words_per_min:
  captions_vo: 61          # 80 caption words / 1.317 min. PLAYBOOK §9 Shorts median 56 (43-65); TTS read 60-70
  all_on_screen_text: 130  # estimate: captions + HUD + title/end cards. PLAYBOOK median 115 (103-131)
captions: 13 (80 words, mean 6.2, max 8)
time_lapse: "From the flip (0:07.0 = JUN 21) the date row runs 3 days per screen second (0.1 day per frame at 30 fps): Miami contact NOV 12 at 0:55.0, solstice DEC 21 at 1:08.0. One labelled jump (DEC 21 -> JAN 30) at 1:08.0, then 3 days/s again on the return countdown. Each shot samples one fixed time of day and says so in the date row (EACH DUSK / EACH MIDNIGHT / EACH NOON)."
hook: "7-word title over a ticking pre-event clock on Ocean Drive at dusk, with the threat in the first HUD subline (THEIR SHADOW IS HEADED FOR MIAMI); rings land at 0:07 (9%) and a days-to-contact countdown starts at 144.0"
tts:
  engine: "Kokoro-82M am_michael, speed 0.96 (pipeline/audio/config.py explainer voice), Spark CPU"
  measured: "2026-11-01 on the Spark (raw clip lengths incl. ~0.3 s padding): C1 2.85, C2 3.75, C3 3.12, C4 2.67, C5 2.10, C6 3.33, C7 3.20, C8 2.58, C9 2.83, C10 2.85, C11 2.75, C12 3.77, C13 3.08 s. Every caption ends before the next caption, the flip, the textless break and the black."
references:
  - id: "7693494009494342945"
    short: ELECTRONS (@man_ia_c)
    url: https://www.tiktok.com/@man_ia_c/video/7693494009494342945
    views: 18200000
    outlier_score: 29.13
    why_chosen: >
      Highest-outlier Short and the beat grid we sit on: title + pre-event clock over a calm named place,
      hard flip at ~10% with a time factor that makes the clock honest, wonder then body, rule line ->
      shorter implication -> 4 s textless break -> the consequence of that implication, full-frame
      interrupt near the middle, HUD status lines carrying a near-captionless stretch, a clock that
      completes, a twist, black + exact title repeat + one true fact.
  - id: "7694025665993100576"
    short: POPSTAR-100x (@man_ia_c)
    url: https://www.tiktok.com/@man_ia_c/video/7694025665993100576
    views: 4900000
    outlier_score: 7.84
    why_chosen: >
      The closest premise shape: a permanent change with a counter that closes on the viewer from the
      flip, an unexplained term planted early and paid only on the end card (our 21-craters line), a
      mundane dark-humour bystander line during the approach, and contact on the exact place (T7).
  - id: "7696143265405488416"
    short: PI=3 (@man_ia_c)
    url: https://www.tiktok.com/@man_ia_c/video/7696143265405488416
    views: 3900000
    outlier_score: 6.24
    why_chosen: >
      One geometric rule pushed through a chain of exact, checkable numbers (ours: ring radii x Sun angle
      -> the shadow's latitude, light and dates). Borrowed: chapter labels every 10-18 s, "every"
      absolutes, the planet-scale number brought back to one exact local comparison, "the reset doesn't
      fix it" ending, and a real dated fact on the end card.
  - id: "b6jmbFcJZCY"
    short: EVERY-HUMAN (OminiAM, long-form)
    url: https://www.youtube.com/watch?v=b6jmbFcJZCY
    views: 1076474
    outlier_score: 107.01
    why_chosen: >
      Non-@man_ia_c reference, so the HUD is not a copy of one channel's look: a calendar engine (dated
      chapter stamps, a timeline scrubber with milestone ticks and a moving dot) and a map where named
      places go dark one after another (1:48-1:58). Ours: the JUN-FEB scrubber across the top of the HUD
      with a gold YOU tick at NOV 12, and the city-by-city march north on the map.
playbook: research/corpus/whatif/PLAYBOOK.md §1A (S1-S10), §2 H4 + combination rule, §4 loops, §5 closing-distance ladder + rung rules, §6 T7/T3/T1, §9 Shorts pacing, §10C-D, §12 checklist
fact_notes:
  - "All numbers below are printed by backlog/whatif/whatif-earth-had-rings/rings.py (pure Python; run `python3 rings.py`). The HUD tracks are generated from it, never typed by hand."
  - "Premise (one rule): Earth gets Saturn's main rings (B, Cassini Division, A) scaled by planet radius. Saturn R = 60,268 km; B ring 92,000-117,580 km (1.527-1.951 R), Cassini Division to 122,170 km (2.027 R), A ring to 136,775 km (2.269 R). On Earth (R = 6,371 km): 3,354-8,088 km up; 4,733 km wide. The faint C and D rings are left out."
  - "Thickness: Saturn's main rings are typically ~10 m thick (NASA Saturn facts: 'about 30 feet'; estimates run 10 m to ~1 km). Thickness is set by particle collisions, not planet size, so it is not scaled with the radius. On screen: 'ABOUT 10 M THICK'."
  - "Ring material: shown neutral (pale cream / grey). Bare water ice would sublimate at 1 AU, so read the scaled rings as rock-and-ice rubble. They settle over the equator because Earth's equatorial bulge torques them into that plane. The B inner edge (1.527 R) sits at the rigid-rock Roche limit (~1.5 R); the fluid/rubble limit (~3 R) covers the whole ring, so it stays a ring."
  - "Sky from Ocean Drive, Miami Beach (25.79 N), looking due south: B inner edge at 29.4 deg elevation, A outer edge at 46.6 deg; band 17.2 deg = 33 full Moons (0.52 deg each)."
  - "Ringlight EST.: the lit arch covers ~0.5-0.9 sr of sky vs the full Moon's 0.00006 sr; even at a tenth of the Moon's surface brightness it outshines full moonlight (0.25 lux) many times over. At midnight Earth's shadow blacks out the arch for ~12-34 deg of ring longitude either side of the meridian, so the light comes from the east and west halves: two soft shadows fanning north. On screen 'BRIGHTER THAN A FULL MOON (EST.)'. In northern summer Miami sees the lit (north) face."
  - "Shadow model: Sun declination d from the NOAA fractional-year series at local solar noon. At noon a winter-hemisphere latitude phi looks at the Sun through the ring plane at rho = cos(phi) + sin(phi)/tan|d| Earth radii; other hours use the exact ray/plane intersection. Light through a ring: direct beam exp(-tau/|sin d|), normal optical depth B 1.5 (range 0.5-5), Cassini 0.1, A 0.5; diffuse light ignored, so shaded values are lower bounds. All labelled EST."
  - "Dates use the crossing day (the noon edge passes the latitude between that day's noon and the next). Noon shadow band, Miami meridian: JUN 21 13.9-41.1 S; JUL 24 11.5-30.9 S; AUG 23 6.3-15.6 S; SEP 5 3.7-9.1 S; SEP 23 a line on the equator; OCT 15 4.4-10.8 N; NOV 12 9.9-25.6 N; DEC 21 13.9-41.0 N. Distance from Miami to the nearest edge: JUN 21 4,420 km, AUG 23 3,570, SEP 23 2,880, OCT 16 1,610, NOV 3 560, NOV 12 ~0 (20 km at noon). Closing ~16 km/day before the equinox, ~57 km/day after it."
  - "Southern hemisphere at the flip (JUN 21): Rio (22.9 S), Johannesburg (26.2 S) and Brisbane (27.5 S) under the B ring at noon (~2% light), Sydney (33.9 S) under the A ring (~28%). Still true to JUL 8 (screen 12.7 s), when Johannesburg and Brisbane move into the Cassini gap; the subline is gone by 12.5 s. Sydney is out of the band by JUL 24."
  - "Fortaleza (3.73 S) is under the B ring at noon SEP 6-13 (screen 32.7-35.0 s); direct noon light ~0% (B slant path ~9x at d = +6 deg; <1% even at tau 0.5), so 'noon goes dark'. The band there is only ~600 km wide, so the sky glows at the edges like a total eclipse; we say 'dark', not 'night'."
  - "Northern arrivals of the A-ring edge (noon): Bogota 4.71 N OCT 2, Panama City 8.98 N OCT 11, Caracas 10.49 N OCT 14, Havana 23.11 N NOV 7, Miami Beach 25.79 N NOV 12. JUN 21 -> NOV 12 = 144 days = the countdown."
  - "Miami Beach in shadow (noon): A ring from NOV 12 (~20-25% light), Cassini Division NOV 27 (~76%), B ring DEC 6 to JAN 6 (~2%), Cassini again JAN 7, A ring JAN 15, last shaded noon JAN 30. NOV 12 -> JAN 30 = 79 days in shadow. Next arrival NOV 12 2027: JAN 30 -> NOV 12 = 286 days. Same every year while the rings last."
  - "DEC 21: 10.4 h of daylight, 9.8 h of it behind the B ring."
  - "December sunlight (top of the atmosphere, daily mean, Dec 1-31): Miami normally 251 W/m2; under the rings 17 W/m2 = ~7% (EST.). That is less than Moscow's normal December (50 W/m2, 20% of Miami's normal) and about Anchorage's (20 W/m2). Robust: Miami stays below Moscow for any B optical depth >= 0.8 (tau 0.8 -> 43 W/m2; tau 1.0 -> 31; tau 2.0 -> 14); only tau 0.5 (78 W/m2, London-level) breaks it."
  - "At the December solstice the noon shadow covers 13.9-41.0 N around the planet: most of India, China south of ~41 N, Pakistan, Bangladesh, Mexico, the southern US (New York sits at the A edge), Egypt, the Middle East, most of Japan. India + China + Pakistan + Bangladesh inside the band alone is ~2.9 billion people, so the HUD says '3+ BILLION PEOPLE (EST.)'."
  - "Equinox: the Sun sits in the ring plane, so the rings are lit edge-on and the shadow shrinks to a line on the equator. Real precedent: Saturn's equinox on 11 Aug 2009 (Cassini imaged the rings almost vanishing). 2026 September equinox: SEP 23 00:05 UTC."
  - "Unlit side: from the September to the March equinox the Sun lights the rings' south face, so Miami sees the north face at night. On the unlit side the B ring (tau ~1.5) is black and hides the stars, the A ring (tau ~0.5) glows faintly from light passing through and dims the stars behind it, and the Cassini Division (tau ~0.1) shows stars through it (as in Cassini's unlit-side images). 2027 March equinox: MAR 20."
  - "Weather-app gag: forecasts report cloud cover, not ring shade, so a clear-sky icon under the ring shadow is the joke; 'still' covers apps catching up later."
  - "End fact: Tomkins, Martin & Cawood (2024), Earth and Planetary Science Letters 646, 118991: 21 impact craters from ~466 Ma all lie within 30 deg of the Ordovician equator, consistent with debris falling from a ring; the authors propose its shade may have contributed to the Hirnantian glaciation (~445 Ma). Planted at 0:18.5 ('21 ANCIENT CRATERS LINE AN OLD EQUATOR · WHY?'), paid on the end card; full citation goes in the post description."
kit_gaps: >
  Shared whatif base (not yet in studio/src/kits; build once, the other 9 whatif backlog scripts need it):
  whatif/Hud (slots CH chapter, L label, N big mono number with one decimal, K live line, S status line, D date
  row, plus a top scrubber strip JUN..FEB with a moving dot and a gold YOU tick; every slot driven by
  segment/track tables, see the HUD state table), whatif/TitleCard (serif title, gold keyword, ringed-planet
  glyph as inline SVG), and captions drawn as whole-sentence serif text layers (core captions disabled, no
  6-word page split). Fonts: one serif + one mono through @fontsource, installed on the Spark (npm in the
  project), registered in core/fonts.ts: Fraunces (title, captions) and IBM Plex Mono (HUD numbers,
  tabular-nums). This deliberately differs from the friction episode (Source Serif 4 + JetBrains Mono)
  so the whatif backlog does not share one look.
  Episode components (3): whatif/OceanDrive (one-point perspective looking due south: 3 Art Deco facade
  variants with neon fins on the right, palms + lawn + beach strip on the left, road and sidewalk to a
  vanishing point at (540, 900), southern sky; props time dusk|night|day, neonOn, neonFlicker,
  streetlights; drawn on a 1080x2600 layer at depth 1 so tilt-ups of 220-260 px never expose an edge),
  whatif/RingArch (shallow band leaving both side edges; B cream, Cassini gap, A grey; props lit 1|0|-1,
  slideIn time for the two halves entering from left and right at 7.0, earthShadowNotch, moonStack count
  for the 33 Moon discs as a repeated circle pattern across the band; lit -1 = B black, A faint translucent
  grey glow, Cassini clear), whatif/RingGlobe (flat side-view diagram: Earth disc with latitude lines,
  ring edge-on as a gold line through the equator, Sun icon on a seasonal arc driven by a declination
  track, parallel beams, noon shadow band on the far hemisphere, labels EQUATOR and BULGE).
  Done with core layers, no new component: the map's shadow band (3 rect layers per map shot, B / Cassini /
  A, y and scaleY keyframed from rings.py in the map's own equirectangular projection, blur 6, static map
  view per shot so layers and map stay aligned; the camera moves both); every grade change (full-frame
  rect layers fill #0E1620 and #5B6B7A multiply with keyframed opacity, since core Grade is per scene and
  cannot animate); the shadow edge arriving down the street (soft-edged rect centred on the vanishing point
  with keyframed scale, blur 40); the ringlight ground shadow (two blurred dark ellipses under the figure,
  fanning down-screen); headlights (two radial glow circles on the road); the neon '12:00' clock (text
  layer on a hotel fin); the weather-app pill (rect + text); grey 'passed' pins (a second explainer/Map
  pin at the same lon/lat with a later `at`); the white-gold equinox glint (rect opacity keyframes).
  Reuse: explainer/You (pose stand; no shadow prop needed), explainer/Map (static views, pins by lon/lat,
  no PLACES edit needed), explainer/Stat ("33"), core camera keyframes/shake, core transitions (cut,
  whip, fade). Dropped vs the old draft: convertible, satellites, grain field, paper sheet, analog clock,
  extra figures stepping into light. Map accuracy: mapdata.ts draws Cuba as a 4-point polygon whose north
  coast sits ~0.6 deg south of Havana; shot 12 stays Caribbean-wide (27 px/deg, error ~16 px) and the
  optional kit fix is a 12-point Cuba outline (-84.95 21.85, -84.3 22.6, -83.2 22.95, -82.4 23.18, -81.2
  23.15, -80.0 22.95, -78.3 22.45, -77.1 21.65, -75.6 21.1, -74.15 20.25, -77.2 19.9, -78.2 20.7). Audio:
  no surf or warm bed exists; the storyboard uses existing beds only (documentary_pulse, tension_pulse,
  dread, sfx/drone at low volume instead of underwater_rumble), and surf.wav is an optional Spark-
  synthesized SFX (filtered pink noise, 8 s loop).
palette: >
  Dusk: sky #F6A96B -> #7B5EA7, hotel pastels mint #9FE3C9, flamingo #F7A1C4, lemon #F9E79F, palm #2E6B4F,
  sand #EAD7AE. Noon: sky #8EC9F0 -> #CDE9F7. Night: #0B1530 -> #1B2A4A, warm streetlights #FFC872.
  Rings: B #EADFC4, A #CFC8B8, Cassini gap clear; unlit side B #15171C (opaque), A #6E6A62 at 35%
  opacity. Ring shadow: overlays #0E1620 + #5B6B7A multiply, opacity per the light EST. Accent (keyword,
  HUD numbers, YOU tick): ring gold #E8B04A. Map: ocean #0f3a4a, land #2d5a55, band B #0B0F14 55%,
  A #0B0F14 30%, Cassini #0B0F14 10%. End card #0B0D10.
post_caption_cta: "Miami, Havana or Fortaleza: where would you sit out ring winter?"
---

# What if Earth had rings like Saturn?

Our own script. We take devices and timing from the references, but the story, the place and every line are new. The references use a Central Park picnic, a giant walking toward an office, a park where circles break, and a world after a snap. Ours is a Miami Beach street that watches the rings' shadow cross the calendar, city by city, until it reaches the street and keeps coming back.

## Beat alignment

| # | Our beat | Our t | Reference id + t | Device borrowed | How we adapt it |
|---|---|---|---|---|---|
| S1 | Premise card + pre-event clock + threat | 0:00-0:07 | 7693494009494342945 0:00 (title + HUD counting to the event + scope subline); 7694025665993100576 0:00 (counter that promises arrival from frame 1) | 7-word what-if title, accent keyword, icon; HUD counts down over a calm place; the subline seeds the master stake | Title with "rings like Saturn" in gold + ringed-planet glyph; HUD "RINGS FORM IN 7.00 S"; subline "THEIR SHADOW IS HEADED FOR MIAMI" opens the shadow loop before anything happens; empty southern sky as the prop that changes |
| S2 | Place you | 0:04.1 | 7693494009494342945 0:05 | Second person + famous real place, calm | "You're on Miami's Ocean Drive." over the dusk street, looking due south |
| S3 | Flip + honest clock + master countdown | 0:07 | 7693494009494342945 0:08 (hard flip, return clock, time factor); b6jmbFcJZCY 0:55 (HUD clock + timeline scrubber appear) | Clock hits zero -> hard visual change + hit; HUD flips to the master tracker with a stated time factor; a scrubber shows how much is left | Arch slams in from both edges with a boom; HUD "RING SHADOW REACHES YOU IN 144.0 DAYS" (ticks 0.1 per frame), date row "JUN 21 · 3 DAYS / SEC · EACH DUSK", scrubber JUN..FEB with a gold YOU tick at NOV 12; chapter "1 · THE RINGS" |
| S4 | Wonder, then body | 0:08-0:17.5 | 7693494009494342945 0:09-0:15 | Harmless sky effect first, the second one on the viewer | Arch 33 Moons wide; then midnight ringlight on your street, your soft double shadow on the pavement (the plant the twist reverses); HUD carries the ring's size and the southern cities already shaded |
| S5 | Rule -> shorter implication -> textless break | 0:18-0:28 | 7693494009494342945 0:21-0:28; 7696143265405488416 0:09 (one rule drives every later number) | Plain-science rule, a 4-word implication, ~4 s with no new text while the image delivers it | Rule: the rings shade a stripe of Earth. Implication: but the Sun moves. Textless 24.1-28.0: diagram Sun slides from +15 deg to +12 deg, the shadow band climbs toward the equator; viewer completes "so the shadow moves" |
| S6 | Consequence, then the first rung | 0:28-0:38.3 | 7693494009494342945 0:32 (the caption right after the break is the implication's consequence); 7696143265405488416 0:20 (chapter label) + 0:23 (rule applied to one named everyday thing) | Consequence line first, then one concrete place with one number | "So the shadow creeps north, day by day." on the map; then the first city it darkens: Fortaleza, noon light <1% (EST.). Chapter "3 · THE WALK NORTH" |
| S7 | Full-frame interrupt | 0:38.3-0:41 | 7693494009494342945 0:40 (white-out); 7696143265405488416 0:34 (hard cut + chapter label) | Whole frame changes before the next scale; chapter label | Equinox: white-gold glint, then a full-frame edge-on diagram with the shadow as one thin line on the equator; chapter "4 · EQUINOX", "SHADOW SHRINKS TO A LINE", precedent "SATURN'S DID THIS ON 11 AUG 2009" |
| S8 | City-by-city march + closing distance | 0:41-0:55 | b6jmbFcJZCY 1:48-1:58 (named places go dark one after another on a map); 7694025665993100576 0:35-0:59 (counter closing on you); 7693494009494342945 0:42-0:56 (HUD status lines carry a near-captionless stretch) | Places darken in order on a map; the live number falls; terse status lines; captions thin out (11 s gap) | Map: band crosses the equator and marches north; pins grey out with HUD stamps OCT 02 BOGOTÁ, OCT 11 PANAMA CITY, OCT 14 CARACAS, NOV 07 HAVANA; "CLOSING ~57 KM A DAY"; caption "Havana is next. Then you." |
| S9 | Contact + bystander gag | 0:55-0:60 | 7694025665993100576 0:59-1:02 (counter reaches HERE on the exact place) + 0:50 (mundane dark-humour bystander line) | Countdown hits zero on you; a normal-life detail carries on | Countdown 0.0 -> centred stamp ON YOU; the shadow edge spreads out from the vanishing point down Ocean Drive; caption "Every weather app still says sunny." over a passer-by's phone |
| S10 | False relief -> worse | 1:00-1:03 | 6oZ9fdM0n50 1:30 (one-beat false resolution, then the problem); 7693494009494342945 1:05 (reassuring line before the turn) | Short relief line, then the real problem with no words | Cassini gap: "A gap in the rings. Sunlight." (~75%), then the B ring drops the street to ~2% at 1:03 with a boom; chapter "6 · WINTER" |
| S11 | Top rung: your city, one exact comparison | 1:03.8-1:08 | 7696143265405488416 0:52-0:56 (planet number brought back to one exact local figure); PLAYBOOK §10D (payoff lands on the viewer) | Planet-scale cause turned into a personal, checkable number; then widen | "Miami gets less December sun than Moscow." with HUD "DECEMBER SUN ~7% OF NORMAL (EST.)" and then "UNDER THE SHADOW: 14°N-41°N · 3+ BILLION PEOPLE (EST.)" |
| S12 | Loop closes -> the reset doesn't fix it | 1:08-1:12.5 | 7693494009494342945 1:02-1:04 (clock completes, status flips) + 1:09-1:10 (twist + HUD equivalence); 7696143265405488416 1:05 (the return doesn't undo it) | Tracker reaches its end, a relief status, then a one-caption reversal with a HUD line | Jump to JAN 30: "RING SHADOW · GONE" over a bright street (relief), then the HUD flips to "RING SHADOW RETURNS IN 286.0 DAYS" and caption "Then it comes back. Every November." Night: the rings show their unlit side, B black, and you have no ringlight shadow (callback to 0:12.5) |
| S13 | Black + bookend + real fact | 1:12.6-1:19 | 7693494009494342945 1:12-1:20 (black, exact title repeat, small-caps fact); 7694025665993100576 1:15 (end card closes a term planted at 0:11); 7696143265405488416 1:15 (real dated fact) | ~1.4 s near-black, exact title repeat, one true dated fact that closes an early plant | Black frame keeps only the return countdown ticking (our outro), then the title repeat; fact closes the 0:18.5 crater plant: 466 million years ago a ring may have left those craters and chilled the planet |

Pacing check against PLAYBOOK §9 and §12 (Shorts):

| Check | Target | Ours |
|---|---|---|
| Title | 7-9 words, held 5-8 s | 7 words, 0:00-0:04.5 (held 4.5 s, cut from 5 so caption 1's measured 2.85 s VO ends before the flip; the countdown carries the hook to 0:07) |
| Event | ~8 s (10%) | 0:07 (9%) |
| Running tracker in the hook | premise + position + a moving number (§2) | pre-event clock ticking from frame 1 + threat subline naming Miami; master countdown from 0:07 |
| Captions | 10-13, ≤8 words, mean ~6-7 | 13, 80 words, mean 6.2, max 8 |
| Caption gaps | median 5 s (4-6), 10-15 s only while a HUD number moves | 3.9 / 4.5 / 5.5 / 4.0 / 6.0 / 5.0 / 8.0 / 11.0 / 4.8 / 3.2 / 3.8 / 5.6, median 4.9 s; the 8 s gap holds the equinox interrupt, the 11 s gap runs while the countdown falls and four city stamps pop |
| VO fits | each line ends before the next event | measured Kokoro lengths (front matter): latest finish C13 at 1:12.5, black at 1:12.6 |
| Textless break | 3-4 s, no new text | 0:24.1-0:28.0 (C5 VO ends ~23.8; no subline pops in 22.0-28.0) |
| New on-screen element | every ~3.8 s | every ~3 s (captions, S-line swaps, chapter labels, city stamps, date row always ticking) |
| Chapter labels | every 10-18 s when used | 0:07, 0:18, 0:28, 0:38.3, 0:55, 1:03 (gaps 11 / 10 / 10.3 / 16.7 / 8) |
| Second person | 1 place line + 1 body line before 25% | 0:04.1 place, 0:12.5 body (16%); 3 of 13 captions in total (23%, above the Shorts 7-18% range on purpose: IFOLOGY "you" correlation, PLAYBOOK §10A; no more added) |
| Master loop | opens in hook, closes at 70-80% | threat subline 0:00, countdown 0:07 -> contact 0:55 (70%); the shadow loop ends JAN 30 at 1:08 (86%) and reopens as the return countdown that runs into the black |
| Interrupt near midpoint | white-out or full frame | equinox glint + full-frame diagram at 0:38.3 (48%) |
| Ladder | each rung bigger / closer / more personal; top rung most personal | Fortaleza (far, 3.7 S) -> Bogotá -> Panama -> Caracas -> Havana -> you (contact) -> your street at 20% / 75% / 2% -> your city's whole December vs Moscow (top caption) -> HUD widens to 3+ billion people |
| Twist + outro | twist ~85%, black + title + fact last 10% | twist 1:09.4 (88%); outro 1:12.6-1:19 (8%) |
| Real numbers + precedent | every stat on screen; ≥1 dated precedent | ~20 numbers/min in the HUD, all from rings.py; Saturn equinox 11 Aug 2009; Tomkins 2024 / 466 Ma |
| Loops open at once | always ≥2 | title (0:00-1:13), pre-event clock (0:00-0:07), threat subline (0:00-0:55), countdown (0:07-0:55), ringlight plant (0:12.5-1:09.4), 21-craters plant (0:18.5-1:14.5), "then you" (0:52-0:55), Cassini relief (1:00-1:03), shadow gone (1:08-1:09.4), return countdown (1:09.4-loop) |

## Hook

- **First line (title card at 0:00, on screen only, not read):** What if Earth had **rings like Saturn**?
- **First visual (frame 1, also the cover):** flat-vector Ocean Drive at dusk, seen from the middle of the street looking due south: mint, flamingo-pink and lemon Art Deco hotel fronts with neon fins on the right, a row of palms, the lawn and the beach on the left, and above the vanishing point a wide, empty violet-orange southern sky. The serif title sits in the upper third with "rings like Saturn" in ring gold and a small ringed-planet glyph. The top-left HUD is already ticking (RINGS FORM IN 7.00 S), and its subline names the threat: THEIR SHADOW IS HEADED FOR MIAMI.

## Script

The 13 captions are the voiceover. Kokoro TTS (am_michael, speed 0.96) reads each caption once as it appears. HUD, chapter, title and end-card text is on screen only. Timestamps are screen time. The date row shows JUN 21 + 3 × (t − 7) days until 1:08.0. One labelled jump goes to JAN 30, and then the clock runs at 3 days/s again.

**S1 · Premise card + pre-event clock (0:00-0:07)**
- 0:00 TITLE (fades 4.1-4.5): What if Earth had **rings like Saturn**?
- 0:00 HUD L: RINGS FORM IN · N: 7.00 S (counts down, hundredths)
- 0:00 HUD S: THEIR SHADOW IS HEADED FOR MIAMI
- 0:00 HUD D: JUN 21 · DUSK (static until the flip)

**S2 · Place you (0:04.1)**
- 0:04.1 CAPTION 1: You're on Miami's Ocean Drive.

**S3 · Flip (0:07)**
- 0:07 (no caption) the two halves of the arch slam in from the left and right edges and lock.
- 0:07 HUD CH: 1 · THE RINGS
- 0:07 HUD L: RING SHADOW REACHES YOU IN · N: 144.0 DAYS (−3.0 per second, one decimal, ticks every frame)
- 0:07 HUD K: SHADOW EDGE 4,420 KM SOUTH (live, from the rings.py track)
- 0:07 HUD D: JUN 21 · 3 DAYS / SEC · EACH DUSK (date ticks); scrubber dot starts at JUN 21, gold YOU tick at NOV 12

**S4 · Wonder, then body (0:08-0:17.5)**
- 0:08 CAPTION 2: An arch 33 Moons wide fills the south.
- 0:08.5 HUD S: 3,400-8,100 KM UP · 29°-47° HIGH
- 0:11 HUD S: SHADOW ON RIO · JOBURG · SYDNEY (held to 12.4; true until JUL 8 = 12.7)
- 0:12.5 HUD D: … · EACH MIDNIGHT
- 0:12.5 CAPTION 3: At midnight, the rings light your street.
- 0:13.5 HUD S: BRIGHTER THAN A FULL MOON (EST.)
- 0:16 HUD S: 4,700 KM WIDE · ABOUT 10 M THICK

**S5 · Rule, implication, silence (0:18-0:28)**
- 0:18 HUD CH: 2 · THE SHADOW · HUD D: … · EACH NOON
- 0:18 CAPTION 4: The rings shade a stripe of Earth.
- 0:18.5 HUD S: 21 ANCIENT CRATERS LINE AN OLD EQUATOR · WHY? (held to 22.0; diagram labels EQUATOR and BULGE carry the "why over the equator")
- 0:22 CAPTION 5: But the Sun moves.
- 0:22.0-0:28.0 HUD S empty. 0:24.1-0:28.0 no new text: the diagram Sun slides down its seasonal arc (+15° → +12°), the beams tilt, the shadow band climbs toward the equator; only the HUD number, K line and date row keep ticking (AUG 5 → AUG 23).

**S6 · Consequence, then the first rung (0:28-0:38.3)**
- 0:28 HUD CH: 3 · THE WALK NORTH
- 0:28 CAPTION 6: So the shadow creeps north, day by day.
- 0:29 HUD S: THE SUN HEADS SOUTH · THE SHADOW HEADS NORTH
- 0:33 CAPTION 7: In Fortaleza, noon goes dark.
- 0:33.5 HUD S: FORTALEZA · SEP 8 · NOON LIGHT <1% (EST.)

**S7 · Full-frame interrupt (0:38.3-0:41)**
- 0:38.3 (no caption) white-gold glint fills the frame (0.3 s), then a full-frame edge-on diagram: Sun exactly in the ring plane, the shadow a thin line on the equator.
- 0:38.3 HUD CH: 4 · EQUINOX · HUD S: SEP 23 · SHADOW SHRINKS TO A LINE
- 0:38.8 HUD K: SATURN'S DID THIS ON 11 AUG 2009 (back to the km line at 41.0)

**S8 · City-by-city march (0:41-0:55)**
- 0:41 CAPTION 8: Now it crosses into the north.
- 0:41.3 HUD S: OCT 02 · BOGOTÁ (pin greys)
- 0:44.3 HUD S: OCT 11 · PANAMA CITY
- 0:45.3 HUD S: OCT 14 · CARACAS
- 0:47 HUD S: CLOSING ~57 KM A DAY
- 0:52 CAPTION 9: Havana is next. Then you.
- 0:53.3 HUD S: NOV 07 · HAVANA
- 0:53.3-0:55 (no new caption) the countdown runs 5.0 → 0.0 DAYS and the K line 380 → 0 KM.

**S9 · Contact + bystander (0:55-0:60)**
- 0:55 HUD CH: 5 · CONTACT · L: RING SHADOW · N: ON YOU · centred stamp ON YOU (0.8 s, gold, then shrinks into the HUD)
- 0:55 HUD K: IN SHADOW · DAY 0 (counts up, 1 per 1/3 s)
- 0:55 HUD S: NOV 12 · 25.8°N · A RING
- 0:56.8 HUD S: NOON LIGHT ~20% (EST.)
- 0:56.8 CAPTION 10: Every weather app still says sunny.

**S10 · False relief, then worse (1:00-1:03)**
- 1:00 CAPTION 11: A gap in the rings. Sunlight.
- 1:00 HUD S: NOV 27 · CASSINI DIVISION · ~75%
- 1:03 (no caption) the B ring's shadow lands; the street drops to near-dark.
- 1:03 HUD CH: 6 · WINTER · HUD S: DEC 6 · B RING · NOON LIGHT ~2% (EST.)

**S11 · Top rung (1:03.8-1:08)**
- 1:03.8 CAPTION 12: Miami gets less December sun than Moscow.
- 1:04.8 HUD S: DECEMBER SUN ~7% OF NORMAL (EST.)
- 1:06.6 HUD S: UNDER THE SHADOW: 14°N-41°N · 3+ BILLION PEOPLE (EST.)
- 1:08.0 HUD D: DEC 21 · SOLSTICE (time-lapse stops)

**S12 · Loop closes, then the reset doesn't fix it (1:08-1:12.5)**
- 1:08.0 whip; HUD D: ▸▸ JAN 30 (labelled jump) · HUD L: RING SHADOW · N: GONE · K: 79 DAYS IN SHADOW · S: FULL SUN AGAIN
- 1:09.4 HUD L: RING SHADOW RETURNS IN · N: 286.0 DAYS (−3.0 per second) · D: JAN 30 · 3 DAYS / SEC · EACH MIDNIGHT; scrubber jumps to a second year with the YOU tick at NOV 12 again
- 1:09.4 CAPTION 13: Then it comes back. Every November.
- 1:10.6 HUD S: EVERY YEAR · NOV 12 TO JAN 30

**S13 · Black + bookend + fact (1:12.6-1:19)**
- 1:12.6-1:14.0 near-black; only the return countdown keeps ticking, small and centred (276.4 → 272.2 DAYS). No music.
- 1:14.0 END: What if Earth had **rings like Saturn**? (exact title repeat, same gold keyword and glyph)
- 1:14.5 END fact (small caps, two lines, held to 1:19): 466 MILLION YEARS AGO · A RING MAY HAVE LEFT THOSE CRATERS · AND CHILLED THE PLANET

**Post caption (description, not on screen):** Saturn's rings, scaled to Earth and parked over the equator. Summer nights glow bright enough to cast your shadow on Ocean Drive. Then the Sun heads south and the rings' shadow walks north, city by city: Fortaleza, Bogotá, Panama, Caracas, Havana, then Miami Beach on November 12. By December, Miami gets less sun than Moscow. The shadow leaves on January 30, and comes back every November. Real science: Tomkins, Martin & Cawood (2024, EPSL 646, 118991) found 21 craters from 466 million years ago near the old equator, a sign Earth may once have had a ring. Miami, Havana or Fortaleza: where would you sit out ring winter? #whatif #space #saturn #pov #simulation

## HUD state table

The whatif/Hud sits top-left inside the 9:16 safe area (x 70, y 250), with the scrubber strip across its top. Slots: CH = chapter (small caps, gold), L = label (small caps), N = big mono number, K = live line, S = status line, D = date row. Tracks are generated from `rings.py --json` (per screen second, linear between samples). Times are screen seconds.

| Slot | From-to | Content | Source |
|---|---|---|---|
| L / N | 0-7 | RINGS FORM IN / {7.00 → 0.00} S | linear |
| L / N | 7-55 | RING SHADOW REACHES YOU IN / {144.0 → 0.0} DAYS | 144 − 3(t − 7) |
| L / N | 55-68 | RING SHADOW / ON YOU | — |
| L / N | 68-69.4 | RING SHADOW / GONE | — |
| L / N | 69.4-74.0 | RING SHADOW RETURNS IN / {286.0 → 272.2} DAYS | 286 − 3(t − 69.4); from 72.6 the number alone moves to centre frame |
| K | 7-38.3 | SHADOW EDGE {4,420 → 2,880} KM SOUTH | rings.py track, rounded to 10 km |
| K | 38.3-41 | SATURN'S DID THIS ON 11 AUG 2009 (from 38.8) | — |
| K | 41-55 | SHADOW EDGE {2,450 → 0} KM SOUTH | rings.py track (0 forced at 55.0) |
| K | 55-68 | IN SHADOW · DAY {0 → 39} | 3(t − 55) |
| K | 68-72.6 | 79 DAYS IN SHADOW | NOV 12 → JAN 30 |
| CH | 7 / 18 / 28 / 38.3 / 55 / 63 | 1 · THE RINGS / 2 · THE SHADOW / 3 · THE WALK NORTH / 4 · EQUINOX / 5 · CONTACT / 6 · WINTER | — |
| S | as listed in the Script section | status lines (never two at once; empty 22.0-28.0) | — |
| D | 0-7 | JUN 21 · DUSK | — |
| D | 7-68 | {JUN 21 + 3(t − 7) days} · 3 DAYS / SEC · EACH {DUSK 7-12.5, MIDNIGHT 12.5-18, NOON 18-68} | — |
| D | 68-69.4 | ▸▸ JAN 30 | labelled jump |
| D | 69.4-72.6 | {JAN 30 + 3(t − 69.4)} · 3 DAYS / SEC · EACH MIDNIGHT | — |
| Scrubber | 7-72.6 | JUN … FEB strip, dot at the current date, gold YOU tick at NOV 12; resets to a new strip at 69.4 | — |

## Shot list

Times are screen seconds. Kit names: core = studio/src/core (camera keyframes, presets, shake; transitions cut/whip/fade; rect/circle/text/svg layers); explainer = studio/src/kits/explainer; whatif = the pieces listed in `kit_gaps`. whatif/Hud, the serif caption text layers and the title/end cards are screen-locked (depth 0) over every shot. SFX from studio/public/sfx.

| # | t_start | t_end | Shot type | Visual (kit vocabulary) | Camera move | SFX |
|---|---|---|---|---|---|---|
| 1 | 0.0 | 4.5 | Establishing, street level looking due south | whatif/OceanDrive `time: dusk`, neon fins on; whatif/TitleCard upper third (fades 4.1-4.5); HUD pre-event clock + threat subline | core keyframes: slow drift (zoom 1.00 → 1.03) | clock_ticking (0.4) 0.0 → 7.0 |
| 2 | 4.5 | 7.0 | Same frame, slight push | explainer/You `stand`, small, mid-sidewalk under a palm, back to camera; Caption 1 at 4.1 (starts under the title fade) | core `pushIn` 0.4 | tick at 6.0, 6.5, 6.8 |
| 3 | 7.0 | 8.0 | Same frame, the flip | Hard cut at 7.0: whatif/RingArch `lit: 1`, two halves slide in from the left and right edges and lock (0.35 s); sky one step deeper (rect overlay #2A1C4A 0 → 0.15); HUD flips to the countdown, K line, date row, scrubber; chapter 1 | core shake at 0.0 (amp 12, 0.35 s) | boom (0.9) + whoosh_long (0.5) at 7.0 |
| 4 | 8.0 | 12.5 | Tilt up to the arch | RingArch fills the upper 60%; its `moonStack` draws 33 Moon discs across the band's height one by one (8.6-10.6) with explainer/Stat "33" counting up beside them; Caption 2 | core keyframes: tilt up (y −260), zoom 1.0 → 0.94 | pop ×6 staggered (0.2) 8.6-10.6 |
| 5 | 12.5 | 18.0 | Midnight, medium on you | OceanDrive `time: night`, warm streetlights on but small; RingArch glowing with the dark Earth-shadow notch at the meridian, light from its east and west halves; you on the pavement with a soft double shadow (two blurred ellipses fanning down-screen, toward camera = north); Caption 3 | core keyframes: tilt down to the figure (y +200), slow drift | breath (0.25) at 13.2; ding (0.2) at 13.5 |
| 6 | 18.0 | 24.1 | Diagram card, side view | whatif/RingGlobe: Earth disc with latitude lines, ring edge-on as a gold line through the equator, labels EQUATOR + BULGE, Sun icon upper-left at the date's declination, parallel beams, noon shadow band on the southern hemisphere; Caption 4 at 18.0, Caption 5 at 22.0 | core `pullOut` 0.5 | whoosh (0.3) at 18.0 |
| 7 | 24.1 | 28.0 | Same diagram, textless | Sun slides down its arc (declination track +15.4° → +11.6°, from rings.py), beams tilt, band climbs toward the equator; no new text | core `pushIn` 0.3 | riser (0.35) 24.1 → 28.0 |
| 8 | 28.0 | 33.0 | Map, the Americas, wide | explainer/Map static view lon −62, lat 2, zoom 5.5 (16.5 px/deg: Rio to Miami in frame); shadow band = 3 rect layers (B / Cassini / A) at the noon band latitudes, sliding north; gold pin on Miami Beach; grey-blue pins Rio, Lima; Caption 6 | core keyframes: zoom 1.0 → 1.06 | whoosh (0.25) at 28.0; drone bed (0.15) starts |
| 9 | 33.0 | 38.3 | Same map, push toward NE Brazil | Pin on Fortaleza (lon −38.5, lat −3.7) under the B band; the B band rect deepens over it (opacity 0.55 → 0.8) and an explainer/Tag "NOON · <1%" pops beside the pin; Caption 7 | core keyframes: move centre toward Fortaleza, zoom 1.06 → 1.5 | sonar_ping (0.3) at 33.5 |
| 10 | 38.3 | 41.0 | Full-frame interrupt | White-gold glint (rect #FFF3D6 opacity 0 → 1 → 0, 38.3-38.6); then RingGlobe `edgeOn` full frame on #0B0D10: Sun in the ring plane, shadow a thin line on the equator; chapter 4 | none (locked) | stinger (0.6) at 38.3; music cuts |
| 11 | 41.0 | 47.0 | Map, band crosses north | Map static view lon −72, lat 10, zoom 7 (21 px/deg); band rects in the northern hemisphere, north edge advancing; pins Bogotá (−74.07, 4.71), Panama City (−79.52, 8.98), Caracas (−66.88, 10.49) each get a grey duplicate pin at their stamp time; Caption 8 | core keyframes: drift north (y −60), zoom 1.0 → 1.08 | sonar_ping (0.3) at 41.3, 44.3, 45.3 |
| 12 | 47.0 | 55.0 | Map, Caribbean-wide | Map static view lon −79, lat 18, zoom 9 (27 px/deg); band north edge crosses Cuba and the Florida Straits; Havana pin greys at 53.3; gold Miami Beach pin pulses (ring at 52.0); Caption 9 at 52.0 | core `pushIn` 0.6 | heartbeat_slow (0.35) from 52.0; sonar_ping at 53.3 |
| 13 | 55.0 | 60.0 | Street, noon, looking south | OceanDrive `time: day`; soft-edged dark rect centred on the vanishing point grows to fill the frame (55.0-57.0), then a full-frame shade overlay holds at ~20% light (#0E1620 0.55 + #5B6B7A multiply 0.35); neon fins flicker on; centred ON YOU stamp; a passer-by (explainer/You, second colour) holds up a phone: pill "☀ SUNNY · 79°F" (rect + text) at 56.8; Caption 10 | core keyframes: slow pull back (zoom 1.1 → 1.0) | impact (0.6) at 55.0; drone swells |
| 14 | 60.0 | 63.0 | Same street, relief | Shade overlay lifts to ~75% light (0.55 → 0.15); a bright stripe (rect, warm, blur 30) slides across the street; Caption 11 | core `drift` 0.3 | ding (0.35) at 60.0 |
| 15 | 63.0 | 68.0 | Same street, the B ring lands | Overlay to ~2% light (0.9); palms in silhouette; neon on; two headlight glow circles on the road; neon "12:00" text on a hotel fin; Caption 12 at 63.8; HUD region line at 66.6 | core `pushIn` 0.6; shake (amp 6, 0.4 s) at 63.0 | boom (0.6) at 63.0; heartbeat (0.4) 63 → 68 |
| 16 | 68.0 | 69.4 | Same street, JAN 30, full sun | Whip in; OceanDrive `time: day`, no overlay, neon off (relief); HUD GONE | none | whoosh (0.4) at 68.0; tick (0.5) at 68.1 |
| 17 | 69.4 | 72.6 | Midnight, tilt up to the arch | OceanDrive `time: night`; RingArch `lit: −1`: B black and starless, A a dim translucent grey glow, stars through the Cassini gap; you stand where you stood in shot 5, now with no ringlight shadow; Caption 13 at 69.4; HUD flips to the return countdown | core keyframes: tilt up (y −220) | stinger (0.4) at 69.4; drone fades |
| 18 | 72.6 | 74.0 | Near-black | #000 frame; HUD hidden except the return countdown number, small, centred, still ticking | none | clock_ticking (0.25) 72.6 → 74.0 |
| 19 | 74.0 | 79.0 | End card | whatif/TitleCard on #0B0D10: exact title repeat with the gold keyword and glyph; small-caps fact at 74.5 (two lines), held to the end | none | ding (0.25) at 74.0 |

Audio (existing files only): core audio `music` entries, documentary_pulse (0.22, 7.0-38.3, fadeOut 0.1) for wonder and the walk south; tension_pulse (0.22, 41.0-63.0) for the march north and contact; dread (0.22, 63.0-69.4) for the B ring; documentary_pulse again (0.18, 74.0-79.0, fadeIn 0.6) under the end card; sfx/drone as a low bed (0.15-0.25, 28.0-72.6). Nothing under 0.0-7.0 except the clock (optional surf.wav if synthesized). TTS reads only the 13 captions, each starting at its caption time; ducking follows the voice clips.
