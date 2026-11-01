---
episode: whatif-friction-off-5-seconds
niche: whatif
format: short 9:16 (1080x1920), caption-led with a light TTS read of the captions only
template: countdown-HUD (house HUD wording, see "HUD state table")
working_title: "What if friction switched off for 5 seconds?"
target_runtime_s: 78
target_words_per_min: 62   # 80 caption words / 78 s. Titles, HUD and end card are on screen only, never read (PLAYBOOK §9 Shorts: 56 median, 43-65; TTS read 60-70)
captions: 13 (mean 6.2 words, max 8)
slow_motion_factor: 11   # 5 story-seconds fill 0:07-1:02 = 55 s of screen time; the 11x keeps running through the landing (1:02-1:06.2), then time returns to 1x
references:
  - id: "7693494009494342945"
    short: ELECTRONS (@man_ia_c)
    url: https://www.tiktok.com/@man_ia_c/video/7693494009494342945
    views: 18200000
    outlier_score: 29.13
    why_chosen: >
      Same 80 s 9:16 caption-led format and the cleanest version of the countdown-HUD template
      (pre-event clock, flip at ~10% with a slow-motion factor, body-first wonder, rule -> short
      implication -> textless break, outward ladder, full-frame interrupt, return + callback stamp +
      false resolution, twist, black, title repeat, fact). Our beat grid follows its proportions,
      with the event, interrupt, black and end card shifted 1-2 s off its exact timings.
  - id: "7693305573487562016"
    short: OXYGEN (@man_ia_c)
    url: https://www.tiktok.com/@man_ia_c/video/7693305573487562016
    views: 13400000
    outlier_score: 21.45
    why_chosen: >
      Closest physical (not cosmic) premise: consequences hit everyday objects and the ground under
      "you" (2D-friendly). Borrowed: a baseline reading on the HUD before the event, a silent "tell"
      object at the flip, stat-then-consequence rungs, a planted by-product with its own rising HUD
      meter that comes back at the end, and a closing-distance meter that reaches the viewer.
  - id: "7693617402180881697"
    short: NEUTRONS (@man_ia_c)
    url: https://www.tiktok.com/@man_ia_c/video/7693617402180881697
    views: 5100000
    outlier_score: 8.16
    why_chosen: >
      Turns the premise into a personal running stat (your weight -> our "YOU: N MPH"), keeps a
      textless breather inside the playful phase, and runs a second clock in the SAME units as the
      return clock (seconds) that races it with almost no captions (our impact countdown). Also the
      return that does not undo the damage (our T1 twist).
playbook: research/corpus/whatif/PLAYBOOK.md §1A (S1-S10), §5 ladders (scale outward + return-to-you dip + closing distance), §6 T1/T2/T10/T12, §9 Shorts pacing, §12 checklist
fact_notes:
  - "PLACE. Lombard Street's crooked block (Hyde St to Leavenworth St, San Francisco) has 8 hairpin turns and is about 412 ft long in a straight line (about 600 ft along the bends). The HILL's natural grade there is about 27%, which is why the road was made crooked in 1922; the road surface itself is only about 16%. Everything in this video slides straight down the fall line (over hedges and planter beds), not along the road, so 27% is the right number. The sidewalks are staircases, so 'you' stand on the brick roadway, just below hairpin 5, about 120 ft (straight downhill) above a garden wall at the last bend."
  - "SLIDE (no friction, air drag off too). 27% grade = 15.1 deg; a = g sin 15.1 deg = 2.56 m/s^2 for everything, whatever its mass. After 5 s: 12.8 m/s = 28.6 mph, 32.0 m = 105 ft. On screen (t = screen seconds, tau = (t - 7)/11 = story seconds): speed_mph = 0.521 x (t - 7); slid_ft = 4.2 x tau^2; pile_ft = 120 - slid_ft (53 ft at 0:51, 37 ft at 0:56, 15 ft at 1:02); return_s = 5 - tau. Because everything accelerates equally, nothing from higher up catches you; the pile at the last bend is made of things that started lower down (parked cars, boards, other people's shirts) and hit the wall first."
  - "AIR DRAG. We switch air resistance off too (HUD: AIR DRAG OFF TOO). That is a simplification: most of a body's drag is pressure drag, not skin friction. With normal drag you would reach about 25 mph instead of 29 after 5 s; the twist works either way."
  - "RACE. With no friction you would reach the pile at tau = sqrt(2 x 36.6 m / 2.56) = 5.35 s, so the impact countdown reads 1.35 s at 0:51 against a return clock of 1.00 s: the return wins by 0.35 s and stays 0.35 s ahead (both count story seconds)."
  - "STOPPING (the twist number). When friction returns you are skidding DOWN a 27% grade, so deceleration = g (mu cos 15.1 deg - sin 15.1 deg). We use mu = 0.7 for a body sliding on brick/road, the upper end of the ~0.45-0.75 range used in pedestrian-accident reconstruction; any lower mu makes the stop longer, so this is the most generous case for you. a = 9.81 x (0.676 - 0.261) = 4.07 m/s^2. Stopping from 12.8 m/s takes 20.1 m = 66 ft. The pile is 15 ft away, so you hit it at v = sqrt(12.79^2 - 2 x 4.07 x 4.57) = 11.2 m/s = 25 mph, the speed of a fall from 6.4 m = 21 ft (v^2 / 2g). With the 11x slow motion still running, the 0.38 s skid fills 4.2 s of screen: impact at 1:06.2."
  - "KNOTS, NAILS, SCREWS, THREAD. Knots, nails in wood and spun yarn all hold only by friction. A screw holds because its threads are an inclined plane locked by friction; with none, any axial load spins it back out. Cotton staple fibres are about 2.2-3.5 cm (about 1 inch) long; thread is those fibres twisted, and twist works only through fibre-on-fibre friction. Simplification: we treat every shirt as staple-fibre fabric; continuous-filament polyester would fall apart into loose strands rather than fluff (the weave is still held by friction at every crossing)."
  - "SHIRTS METER. 'SHIRTS UNRAVELLED IN SF' climbs to 808,000 = San Francisco's population (US Census estimate, July 2023, about 808,000), assuming one worn shirt per resident. Stylised counter, not a measurement."
  - "CARS. All braking and steering is tyre friction; each tyre touches the road on a contact patch roughly the size of a postcard (about 150-200 cm^2), so a car's grip is four postcards of rubber."
  - "CABLE CAR. The Powell-Hyde line runs on Hyde St and stops at the top of the crooked block. A cable car moves by clamping a grip onto a cable that runs at a constant 9.5 mph in a slot under the street, and the cable itself is driven by friction on the powerhouse sheaves (Washington & Mason). With no friction the grip lets go and the cable coasts. A car carries up to about 60 people; we show 30 riders."
  - "FAULT (top rung; honest speculation, PLAYBOOK T12). The San Andreas Fault runs just offshore west of San Francisco and is locked by friction between earthquakes; strain has been building since 1906. Real dated precedent: the 18 April 1906 earthquake (M~7.9) ruptured about 296 mi of the fault, with surface offsets up to about 20 ft (6 m) in Marin County. Our HUD slip number is an order-of-magnitude estimate, not a prediction: with friction gone the fault's whole shear stress drops (taken as ~10 MPa); for a ~15 km deep fault in rock with shear modulus 30 GPa that relaxes as slip D = stress x depth / modulus = about 5 m (16 ft), reached over a rise time of about depth / shear-wave speed = 15 km / 3.5 km/s = 4.3 s. On screen: slip_ft = 16 x min(1, tau / 4.3) -> 13 ft at 0:44, 15 ft at 0:51. Shown with '(EST.)'."
  - "END FACT. Holmberg & Erdemir (2017), Friction 5(3):263-284: about 23% of the world's total energy use goes to tribological contacts, 20% of it (103 EJ) to overcoming friction. Cite in the post description."
kit_gaps: >
  None of the whatif pieces exist yet (studio/src/kits/whatif is not created). Build Hud, TitleCard and SerifCaption once in
  studio/src/kits/whatif, shared with the other whatif backlog scripts, and pass a 10 s gate render before this episode.
  whatif/Hud: status chip line (FRICTION ON/OFF with a dot), one big number line (live track, ms digits, mono font
  with tabular-nums, e.g. @fontsource/jetbrains-mono, installed on the Spark only), up to three small-caps sublines,
  each either static text or a template with a live value track; driven by the HUD state table below.
  whatif/SerifCaption: one whole caption per page (no 6-word split; the core Captions schema caps maxWords at 6, so core
  captions stay disabled), italic serif (@fontsource/source-serif-4 italic, Spark only), 2 lines max at 860 px, lower
  third above y = 1480. whatif/TitleCard: serif title with an accent keyword and an icon slot (here a shoelace bow).
  whatif/DiagramCard: flat explainer card template used 4x (nail + screw, thread fibres, cable-car grip in its slot,
  fault cross-section). Backgrounds, only two: whatif/LombardMap (one tall three-quarter map of the crooked block and
  the blocks around it, Coit Tower, the Bay, and a stylised, not-to-scale west edge with the San Andreas offshore as a
  red dashed line; shots 1, 10, 13, 14, 15 and 16b are camera keyframes on it, the aerial is a pullOut to zoom ~0.35)
  and whatif/SlopeStrip (one side-on strip of the 15 deg slope: bricks, kerb, low hedge, Victorian row-house fronts,
  garden wall at the right end; a `variant: "hyde"` adds the cable slot; shots 2, 3, 5, 7, 9, 11, 16 and 17).
  Props: whatif/ShoePair (two states, tied / loose, crossfade, lace ends sway), whatif/TopDownCar (small, for the map;
  tyre rects can glow), whatif/CableCar (side view, 30 rider heads in the windows), whatif/RowHouse (siding boards,
  steps and bay window as separate rect layers that slide apart with keyframes; no new physics code), whatif/DebrisField
  (80-120 seeded glyphs: button, nail, bolt, thread curl; motion stretch via scaleY + layer blur), whatif/FluffPile
  (heap + puff burst), whatif/BrickTexture (scrolling brick tile for the POV shot 4), whatif/FluffWisps (wisps peeling off a shirt outline), whatif/Streaks (one screen-space diagonal
  streak overlay at low opacity, instead of editing every asset). explainer/You needs a `shirt` prop (filled tee with
  colour, with an `unravel` 0..1 value) and three poses, `slide` (upright, tilting back), `sprawl` (lying on the back,
  feet first) and `sitUp` (shot 17; `shrug` is the fallback). Reuse explainer/Car (side-on only), core camera keyframes/shake, transitions (cut, fade, whip), grade.
  Audio: no calm/warm music bed exists in studio/public/music (only deep_ocean, documentary_pulse, dread,
  tension_pulse); add one for 0-7 s and the end card. All SFX cues used below exist in studio/public/sfx.
palette: >
  Before the flip and after the return: warm golden-hour flat palette (brick #B5523B, hedge #3F6B3A, hydrangea #8E7CC3,
  sky #F2B880 -> #F7D9A8). After the flip ("frictionless"): grade hue/saturate toward cool cyan (hue -18, saturate 0.75,
  brightness 1.05) plus a screen-blend cyan overlay (#9FE8FF, opacity 0.18) and the whatif/Streaks overlay; check one
  Spark-rendered frame (a multiply tint over the warm palette goes muddy teal). Accent for the keyword and HUD numbers:
  amber #FFB547.
---

# What if friction switched off for 5 seconds?

Original script. Structure, timing proportions and devices are borrowed from the three references above; no wording, story, place or image is taken from them (they use Central Park, a rooftop bar and cosmic explosions; ours is a steep San Francisco street, unravelling clothes and a locked fault). The HUD wording is our own house style (status chip + "BACK ON IN" + "GRIP RESTORED" + "T+5 S" stamp), not the references' template phrases.

## Beat alignment

| # | Our beat | Our t | Reference id + t | Device borrowed | How we adapt it |
|---|---|---|---|---|---|
| S1 | Premise card + pre-event clock | 0:00-0:07 | 7693494009494342945 0:00 (title + pre-event HUD countdown, scope subline); 7693305573487562016 0:00-0:07 (baseline reading "AIR PRESSURE 14.7 PSI") | Short what-if title, accent keyword, tiny time window; HUD counting down to the event; a scope subline plus a baseline reading | Title keyword "friction" in amber with a shoelace-bow icon (the specific thing, not an abstract icon). HUD "FRICTION ● ON / OFF IN 6.900 S". Scope subline "EVERY STEP YOU TAKE NEEDS IT" plants caption 3; baseline "HILL GRADE 27%" comes in at 0:02, the number that drives every later stat. Title clears at 0:04.5, before caption 1 |
| S2 | Place you | 0:04.5 | 7693494009494342945 0:05; 7693617402180881697 0:05 | Second person + a named, famous real place, calm | "You're on Lombard Street, San Francisco." over the hairpins; you stand on the brick roadway with the slope already visible |
| S3 | Flip | 0:07 | 7693494009494342945 0:08 (style flip + 11x); 7693305573487562016 0:08 (silent tell object, flame cuts out) | Clock hits zero -> hard style change + hit; HUD flips to a return countdown with a slow-motion factor; one object reacts with no words | Warm street grades to glossy cyan; a parked hatchback starts sliding with its wheels not turning. HUD "FRICTION ○ OFF / BACK ON IN 5.000 S / SLOW-MO ×11 / AIR DRAG OFF TOO" (5 s x 11 = 55 s, return lands at 1:02) |
| S4 | Wonder, body first + breather | 0:08-0:17 | 7693494009494342945 0:09-0:21 (harmless wonder on your own body); 7693617402180881697 0:11-0:20 (personal running stat, then 4 s textless breather) | First effects harmless and on your body; a personal running stat; a textless hold before the rule | Laces untie themselves (the screenshot moment), then you glide downhill at walking pace without taking a step; HUD starts "YOU: 2.1 MPH". 0:13.6-0:17 textless (3.4 s): you glide past hydrangeas, laces drifting |
| S5 | Rule, short implication, textless break | 0:17-0:26 | 7693494009494342945 0:21-0:32 (rule -> 4-word implication -> 4 s textless dissolve) | Plain science rule -> shorter line that implies the consequence -> 3-4 s textless break while the image breaks | Rule points forward: nails hold wood only by friction. Implication (4 words): screws too. 0:22.6-0:26 textless: a Victorian row house's siding, steps and bay window slide apart |
| S6 | Ladder: micro -> personal dip -> street -> city | 0:26-0:40 | 7693305573487562016 0:13-0:35 (stat -> consequence rungs; by-product planted at 0:26 with a rising meter at 0:28); 7693494009494342945 0:32-0:35 (fastest cadence) | 3-5 rungs, one idea and one number each, caption cadence peaks (~3.5 s); a planted by-product gets its own rising HUD meter | Thread (1-inch fibres) -> YOUR shirt (return-to-you dip) with the plant meter "SHIRTS UNRAVELLED IN SF" climbing to 808,000 -> cars (4 postcard-sized grip patches) -> the Hyde St cable car with 30 riders (cable at 9.5 mph) |
| S7 | Full-frame interrupt | 0:40-0:43 | 7693494009494342945 0:40 (white-out); 7693617402180881697 0:28 (black + colour change) | One full-frame interrupt near the midpoint that wipes to a bigger scale | Whip down into a full frame of loose buttons, nails and bolts sliding past the lens; white flash at 0:42 wipes to the aerial |
| S8 | Crust-scale top rung + racing clock | 0:43-1:02 | 7693494009494342945 0:42-0:56 (live climbing HUD number over the widest view); 7693617402180881697 0:50-1:04 (second countdown in seconds races the return clock, near-wordless) | Widest view with a live climbing number; a second countdown in the same units races the main clock; captions thin out | Pull out over San Francisco to the San Andreas Fault: "SAN ANDREAS: SLIPPED 13 FT (EST.)" climbing, with 1906 as the real dated precedent. Then back to you: "PILE-UP AHEAD: 53 FT · IMPACT IN 1.35 S" against "BACK ON IN 1.000 S"; 11 s with only the numbers moving |
| S9 | Return + bookend + false resolution | 1:02-1:05 | 7693494009494342945 1:02-1:06 (clock zero, status flip, reassuring line, place callback); 7693617402180881697 1:04-1:06 | Clock reaches zero, status flips, a reassuring line, a callback stamp naming the opening place; aftermath version of the opening shot | "GRIP RESTORED", the reassuring caption, the stamp "T+5 S · LOMBARD ST" over a 1.2 s re-frame of shot 1 (cars in the hydrangea beds, siding down, the cable car gone) |
| S10 | Twist | 1:04-1:09.5 | 7693305573487562016 0:56-1:02 (closing-distance meter reaches you; by-product pays off); 7693617402180881697 1:09 (the return does not undo it); PLAYBOOK T1/T10 | The fix doesn't save you and the damage stays; one caption + HUD equivalences; bathos landing | HUD "STOPPING DISTANCE: 66 FT · PILE: 15 FT" -> impact at 25 mph (= a 21 ft fall) into the heap of the city's unravelled shirts. Caption: nothing that came apart goes back; HUD "YOUR SHIRT: IN THE PILE"; the camera pulls back on a naked, unnailed hill |
| S11 | Black + bookend + real fact | 1:09.5-1:18 | 7693494009494342945 1:12-1:20; 7693305573487562016 1:10-1:20 | ~1.5 s black, exact title repeat for the loop, one small-caps true fact; CTA only in the post caption | Fact: ~20% of the world's energy goes to fighting friction (Holmberg & Erdemir 2017), and every knot you've ever tied depends on it (calls back the laces) |

Pacing check vs PLAYBOOK §9 / §12 (Shorts): title 8 words, held 4.5 s over a moving clock (hook runs to the event at 0:07 = 9%); return at 1:02 (79%); twist caption 1:06.5 (85%); black 1:09.5 (89%). 13 captions, 80 words, mean 6.2, max 8, 62 wpm (VO reads captions only). Caption gaps 3.5/3/6/4/5/3.5/3.5/4/7/5/13.5/4 s (median 4 s; the 13.5 s gap runs while three HUD numbers move). New on-screen element about every 3 s (captions, HUD swaps and cards; see HUD state table). Second person: 4 of 13 captions (31%), above the Shorts median, kept on purpose for the body-first and personal-dip beats. Open loops: title (0:00-1:09.5), pre-event clock (0:00-0:07), master return clock (0:07-1:02, 71% of runtime), speed tracker (0:11-1:06), shirts plant meter (0:30-1:07), fault meter (0:44-0:51), impact race (0:51-1:06); at least two open at every point after 0:07. Placement (0:04.5) and the body beat (0:08) both land inside the first quarter. Real dated precedent on screen: 1906 (caption 11).

## Hook

- **First line (on screen at 0:00, NOT read by the VO):** What if friction switched off for 5 seconds?
- **First visual (frame 1):** warm golden-hour flat-vector Lombard Street from just below hairpin 6, looking up the brick switchbacks between low hedges and purple hydrangeas; two cars creeping down; the Hyde St cable car, riders in the windows, at the top of the frame. Serif title centred in the upper third, "friction" in amber, a small shoelace-bow icon. Top-left HUD already ticking: FRICTION ● ON / OFF IN 6.900 S.

## Script

Captions are the voiceover: TTS (Kokoro, calm narrator, about 60 wpm with the holds below) reads each caption once as it appears, using the VO spelling where it differs. The opening title, the end-card title repeat, the end fact and all HUD text are on screen only and never read. Timestamps are screen time.

**S1 · Premise card + pre-event clock (0:00-0:07)**
- 0:00 TITLE (fades out 4.1-4.5): What if **friction** switched off for 5 seconds?
- 0:00 HUD: see the HUD state table (FRICTION ● ON / OFF IN 6.900 S / EVERY STEP YOU TAKE NEEDS IT; HILL GRADE 27% at 0:02)

**S2 · Place you (0:04.5)**
- 0:04.5 CAPTION 1: You're on Lombard Street, San Francisco.

**S3 · Flip (0:07)**
- 0:07 (no caption) HUD flips: FRICTION ○ OFF / BACK ON IN 5.000 S / SLOW-MO ×11 / AIR DRAG OFF TOO
- Tell object: a parked hatchback starts sliding downhill with its wheels not turning.

**S4 · Wonder, body first (0:08-0:17)**
- 0:08 CAPTION 2: Your shoelaces untie themselves.
- 0:11 CAPTION 3: You glide downhill without taking a step.
- 0:13.6-0:17 (no caption, 3.4 s breather) you glide past the hydrangeas at walking pace, laces drifting like weed in water.

**S5 · Rule, implication, textless break (0:17-0:26)**
- 0:17 CAPTION 4: Nails hold wood only by friction.
- 0:21 CAPTION 5: So does every screw.
- 0:22.6-0:26 (no caption, once the caption 5 read ends) a row house's siding boards, porch steps and bay window slide apart down the slope.

**S6 · Ladder (0:26-0:40)**
- 0:26 CAPTION 6: Cotton thread is 1-inch fibers, twisted tight. (VO: "Cotton thread is one-inch fibers, twisted tight.")
- 0:29.5 CAPTION 7: Your shirt unravels into fluff.
- 0:33 CAPTION 8: No car can brake or steer.
- 0:37 CAPTION 9: Cable cars grip their cable by friction.

**S7 · Full-frame interrupt (0:40-0:43)**
- 0:40 (no caption) whip down into a wall of loose buttons, nails and bolts sliding past the lens; white flash at 0:42.

**S8 · Top rung + racing clock (0:43-1:02)**
- 0:44 CAPTION 10: The San Andreas Fault is locked by friction.
- 0:49 CAPTION 11: In 1906, it slipped about 20 feet. (VO: "In nineteen-oh-six, it slipped about twenty feet.")
- 0:51-1:02 (no caption) only the HUD numbers move: BACK ON IN 1.000 -> 0.000 S, IMPACT IN 1.35 -> 0.35 S, PILE-UP AHEAD 53 -> 15 FT, YOU 23 -> 29 MPH.

**S9 · Return + bookend + false resolution (1:02-1:05)**
- 1:02 HUD: FRICTION ● ON / GRIP RESTORED
- 1:02.5 CAPTION 12: Everything grips again, just like before.
- 1:03 HUD stamp: T+5 S · LOMBARD ST (over the re-framed opening shot)

**S10 · Twist (1:04-1:09.5)**
- 1:04.2 HUD: STOPPING DISTANCE: 66 FT · PILE: 15 FT (YOU counts down 27 -> 25 MPH as you skid)
- 1:06.2 (no caption) you plough, slapstick not gory, into the heap of the city's unravelled shirts; fluff puffs up and settles.
- 1:06.4 HUD: IMPACT 25 MPH ≈ A 21-FT FALL
- 1:06.5 CAPTION 13: But nothing that came apart goes back.
- 1:07 HUD: YOUR SHIRT: IN THE PILE. You sit up, shirtless, laces still undone; one shirt button rolls to a stop beside you; the camera pulls back on the hill: boards down, nails lying loose, cars in the flower beds.

**S11 · Black + bookend + fact (1:09.5-1:18)**
- 1:09.5-1:11 black, silence.
- 1:11 END (not read): What if **friction** switched off for 5 seconds? (exact title repeat, same amber keyword)
- 1:12 END fact (small caps, not read, held to 1:18): ABOUT 20% OF THE WORLD'S ENERGY IS SPENT FIGHTING FRICTION. EVERY KNOT YOU'VE EVER TIED DEPENDS ON IT.

**Post caption (description, not on screen):** Five seconds without friction on Lombard Street, a 27% hill in San Francisco. Your laces let go first. Then the nails and screws, then every thread you're wearing. Cars can't brake or steer, the Hyde St cable car loses its grip, and the San Andreas Fault comes unlocked. When friction switches back on you're doing 29 mph, and you need 66 ft to stop. What would you miss first: your laces, your shirt or your brakes? Source for the end fact: Holmberg & Erdemir, Friction 5:263-284 (2017). #whatif #physics #sanfrancisco #pov #simulation

## HUD state table

The HUD is one screen-locked whatif/Hud layer (top-left, inside SAFE_AREA: x >= 70, y >= 230). Line L = status chip, line T = big mono number, S1-S3 = small-caps sublines (S3 is used only from 0:30). Every live value comes from the formulas in fact_notes, never typed by hand: speed = 0.521 x (t - 7), tau = (t - 7)/11, pile = 120 - 4.2 x tau^2, impact = 5.349 - tau, slip = 16 x min(1, tau/4.3). A cell with "-" means the line is hidden.

| Screen t | L (status) | T (big number) | S1 | S2 | S3 |
|---|---|---|---|---|---|
| 0:00-0:02 | FRICTION ● ON | OFF IN 6.900 -> 4.900 S (real time) | EVERY STEP YOU TAKE NEEDS IT | - | - |
| 0:02-0:07 | FRICTION ● ON | OFF IN 4.900 -> 0.000 S | EVERY STEP YOU TAKE NEEDS IT | HILL GRADE 27% | - |
| 0:07-0:11 | FRICTION ○ OFF | BACK ON IN 5.000 -> 4.636 S (story time, 5 - tau) | SLOW-MO ×11 | AIR DRAG OFF TOO | - |
| 0:11-0:23 | FRICTION ○ OFF | BACK ON IN 4.636 -> 3.545 S | SLOW-MO ×11 | YOU: 2.1 -> 8.3 MPH (live) | - |
| 0:23-0:30 | FRICTION ○ OFF | BACK ON IN 3.545 -> 2.909 S | NAILS + SCREWS: BACKING OUT | YOU: 8.3 -> 12.0 MPH | - |
| 0:30-0:33 | FRICTION ○ OFF | BACK ON IN 2.909 -> 2.636 S | NAILS + SCREWS: BACKING OUT | YOU: 12.0 -> 13.5 MPH | SHIRTS UNRAVELLED IN SF: 0 -> 224,000 (live) |
| 0:33-0:37 | FRICTION ○ OFF | BACK ON IN 2.636 -> 2.273 S | CARS: NO BRAKES · NO STEERING | YOU: 13.5 -> 15.6 MPH | SHIRTS UNRAVELLED IN SF: 224,000 -> 467,000 |
| 0:37-0:44 | FRICTION ○ OFF | BACK ON IN 2.273 -> 1.636 S | HYDE ST CABLE CAR · 30 RIDERS · SLIDING | YOU: 15.6 -> 19.3 MPH | SHIRTS UNRAVELLED IN SF: 467,000 -> 735,000 |
| 0:44-0:51 | FRICTION ○ OFF | BACK ON IN 1.636 -> 1.000 S | SAN ANDREAS: SLIPPED 13 -> 15 FT (EST.) | YOU: 19.3 -> 22.9 MPH | SHIRTS UNRAVELLED IN SF: 735,000 -> 808,000 (holds from 0:50) |
| 0:51-0:56 | FRICTION ○ OFF | BACK ON IN 1.000 -> 0.545 S | PILE-UP AHEAD: 53 -> 37 FT · IMPACT IN 1.35 -> 0.89 S | YOU: 22.9 -> 25.5 MPH | SHIRTS UNRAVELLED IN SF: 808,000 |
| 0:56-1:02 | FRICTION ○ OFF | BACK ON IN 0.545 -> 0.000 S | PILE-UP AHEAD: 37 -> 15 FT · IMPACT IN 0.89 -> 0.35 S | YOU: 25.5 -> 28.6 MPH | SHIRTS UNRAVELLED IN SF: 808,000 |
| 1:02-1:03 | FRICTION ● ON | GRIP RESTORED | PILE-UP AHEAD: 15 FT | YOU: 29 MPH -> skidding | - |
| 1:03-1:04.2 | FRICTION ● ON | GRIP RESTORED | T+5 S · LOMBARD ST | YOU: 28 MPH | - |
| 1:04.2-1:06.2 | FRICTION ● ON | GRIP RESTORED | STOPPING DISTANCE: 66 FT · PILE: 15 FT | YOU: 27 -> 25 MPH (decelerating, 4.07 m/s^2) | - |
| 1:06.2-1:07 | FRICTION ● ON | GRIP RESTORED | IMPACT 25 MPH ≈ A 21-FT FALL | YOU: 0 MPH | - |
| 1:07-1:09.5 | FRICTION ● ON | GRIP RESTORED | IMPACT 25 MPH ≈ A 21-FT FALL | YOU: 0 MPH | YOUR SHIRT: IN THE PILE |
| 1:09.5-1:18 | hidden | hidden | hidden | hidden | hidden |

Speed track check (0.521 x (t - 7)): 2.1 at 0:11, 8.3 at 0:23, 12.0 at 0:30, 13.5 at 0:33, 15.6 at 0:37, 19.3 at 0:44, 22.9 at 0:51, 25.5 at 0:56, 28.6 at 1:02. Pile check: 53 ft at 0:51, 37 ft at 0:56, 15 ft at 1:02. Shirts meter = 808,000 x (1 - (1 - p)^2), p = (t - 30)/20 clamped to 0..1 (0 at 0:30, 808,000 at 0:50, then holds). Skid speed after the return falls linearly from 28.6 at 1:02 to 25.1 at 1:06.2 (28 at 1:03, 27 at 1:04.2).

## Shot list

Times are screen seconds. Kit names: core = studio/src/core (camera presets/keyframes/shake, transitions, grade, callouts); explainer = studio/src/kits/explainer; whatif = the pieces listed in `kit_gaps`. whatif/Hud (top-left), whatif/SerifCaption (lower third, above y = 1480) and the title/end cards are screen-locked layers (depth 0) over every shot. Only two backgrounds: LombardMap (M) and SlopeStrip (S).

| # | t_start | t_end | Shot type | Visual (kit vocabulary) | Camera | SFX (studio/public/sfx) |
|---|---|---|---|---|---|---|
| 1 | 0.0 | 4.5 | Establishing, low three-quarter up the hairpins | M, golden hour, keyframe "low": hairpins 4-7 rising, hedges, hydrangeas, row houses, cable car with riders on Hyde St at the top; explainer/Car x2 creeping down (0.3 m/s); whatif/TitleCard (shoelace icon), fades 4.1-4.5 | core camera keyframes: slow drift up (y -60, zoom 1.0 -> 1.04) | clock_ticking (0.4, to 7.0) |
| 2 | 4.5 | 7.0 | Medium, side-on, you on the brick roadway | S: explainer/You pose `stand` (shirt prop, colour #3A8FD6) mid-frame on the bricks, hatchback parked at the kerb uphill of you (the tell); Caption 1 | core `pushIn` 0.5 | tick at 6.0, 6.5, 6.8 |
| 3 | 7.0 | 8.0 | Same frame, style flip | Hard cut on 7.0 to the frictionless look (grade hue -18, saturate 0.75 + cyan screen overlay + whatif/Streaks); hatchback starts sliding, wheels still; HUD flips | core shake at 0.0 (amp 14, 0.35 s) | impact (0.9) + glitch (0.4) at 7.0; drone bed (0.25, 7.0-62.0) |
| 4 | 8.0 | 11.0 | POV close-up down at your own shoes | whatif/ShoePair crossfades tied -> loose over 8.3-10.2; lace ends sway like weed in water; brick texture drifts slowly past; Caption 2 | core keyframes: tilt down (y +120) then slow drift | whoosh (0.3) at 8.3 |
| 5 | 11.0 | 17.0 | Medium, side-on glide (wonder, then textless breather 13.6-17) | S: You pose `slide`, upright, arms out, gliding with a 2-ghost trail; hatchback glides alongside at the same speed; hydrangeas pass; Caption 3 | core keyframes: track right with the figure, zoom 1.0 -> 1.08 | whoosh_long (0.35) at 11.2 |
| 6 | 17.0 | 22.0 | Diagram card | whatif/DiagramCard: nail in a wood cross-section, fibres pressing the shank, "FRICTION" arrows fade to 0 and the nail slides out (Caption 4 at 17.0); at 21.0 the card swaps to a screw whose thread spins it back out (Caption 5 at 21.0) | core `pushIn` 0.6 | click (0.5) at 18.5; tick at 21.0 |
| 7 | 22.0 | 26.0 | Medium, textless break | S: whatif/RowHouse on the slope: siding boards, porch steps and the bay window slide apart and downhill (rect layers + keyframes); nails drift out as small glyphs | core `panLeft` 0.5 | riser (0.35) 22.0-26.0; pop (0.3) x3 staggered |
| 8 | 26.0 | 29.5 | Diagram card | whatif/DiagramCard: one thread magnified into short twisted fibres with a "1 IN" bracket (core callout `label`), fibres sliding along each other; Caption 6 | core `pullOut` 0.6 | tick at 26.0 |
| 9 | 29.5 | 33.0 | Medium, side-on, you now sliding on your back | S: You pose `sprawl` (lying back, feet first); whatif/FluffWisps peel off YOUR shirt (unravel 0 -> 1) and off 3 other sliding people; everyone's fluff slides along with them; Caption 7 | core `panDown` 0.5 | whoosh (0.3) at 29.7 |
| 10 | 33.0 | 37.0 | High three-quarter of hairpins 4-6 | M, keyframe "high": whatif/TopDownCar x3 sliding straight across the hairpins through a hydrangea bed instead of turning; brake lights on (red circle layers) with no effect; 4 tyre rects on one car glow amber, label "EACH ≈ A POSTCARD", then fade to grey; Caption 8 | core keyframes: pan down + rotate 0 -> 2 deg | whoosh_long (0.45) at 33.4; impact (0.4) at 35.5 |
| 11 | 37.0 | 40.0 | Side view on Hyde St + inset | S `variant: "hyde"`: whatif/CableCar with 30 rider heads sliding downhill, bell motion lines; inset whatif/DiagramCard (top-right): the grip in its slot letting go of the cable, label "CABLE 9.5 MPH"; Caption 9 | core keyframes: tilt up (y -160), zoom 1.0 -> 1.12 | ding (0.6) at 37.3; ding (0.3) at 38.5 |
| 12 | 40.0 | 43.0 | Full-frame interrupt | core transition `whip` (down, 0.3) into whatif/DebrisField (100 glyphs streaming past, scaleY stretch + blur 4); a full-frame white rect with opacity keyframes 0 -> 1 over 42.0-42.4, held to 43.0 | core shake (amp 10, 1.0 s) | whoosh_long (0.6) at 40.0; stinger (0.6) at 42.0 |
| 13a | 43.0 | 48.0 | Aerial pull-out to the fault | `fade` transitionIn from white. M pullOut from Lombard to zoom ~0.35: tiny cars and dots sliding down every hill, the Bay, Coit Tower, and the San Andreas as a red dashed line off the stylised west coast; Caption 10 at 44.0 | core keyframes: zoom 1.0 -> 0.35, then drift | underwater_rumble (0.3) as a low bed 43.0-62.0 |
| 13b | 48.0 | 51.0 | Diagram card | whatif/DiagramCard: fault cross-section, two crust blocks sliding past each other; bracket "1906: ~20 FT" next to the live "NOW: 15 FT (EST.)"; Caption 11 at 49.0 | core `pushIn` 0.4 | boom (0.35) at 48.2 |
| 14 | 51.0 | 56.0 | Back to you, behind-and-above chase | M, keyframe "chase": You `sprawl` sliding feet first straight down the fall line, bumping over low hedges and planter beds (not following the road); ahead at the last bend the pile-up: cars, boards and a white fluff heap against the garden wall | core keyframes: follow figure, zoom 1.0 -> 1.25 | heartbeat (0.35) from 51.0 |
| 15 | 56.0 | 62.0 | Tight race | Same chase, tighter; no caption; the heap grows in frame | core `pushIn` 1.0 | heartbeat_fast (0.45) 56.0-62.0; clock_ticking (0.4) 59.0-62.0 |
| 16a | 62.0 | 63.0 | Medium, side-on skid | Hard cut to the warm palette (grade off): you hit the bricks and skid, grit flecks and a brick-dust trail; Caption 12 at 62.5 | core shake (amp 16, 0.5 s) at 0.0 | impact (0.9) at 62.0; drone and rumble beds cut |
| 16b | 63.0 | 64.2 | Bookend re-frame of shot 1 | M, keyframe "low" (same as shot 1), warm: aftermath: cars in the hydrangea beds, siding down, the cable car gone from Hyde St, fluff drifting; HUD stamp "T+5 S · LOMBARD ST" | none | whoosh (0.25) at 63.0 |
| 16c | 64.2 | 66.2 | Side-on skid toward the pile | S: skid continues, slowing, garden wall and fluff heap entering frame right; HUD "STOPPING DISTANCE: 66 FT · PILE: 15 FT" | core keyframes: track right, slow | heartbeat (0.3) 64.2-66.2 |
| 17 | 66.2 | 69.5 | Wide, low, at the pile | You plough into whatif/FluffPile (puff burst, settle); sit up shirtless, laces undone; one shirt button rolls to a stop beside you; camera pulls back on the damaged hill; Caption 13 at 66.5 | core keyframes: hold, then pull back (zoom 1.15 -> 0.95) from 67.5 | pop (0.7) at 66.2; whoosh (0.3) at 66.4 |
| 18 | 69.5 | 71.0 | Black | Black frame, HUD hidden | none | silence |
| 19 | 71.0 | 78.0 | End card | whatif/TitleCard on near-black (#0B0D10): exact title repeat with amber "friction"; small-caps fact at 72.0 (two lines), held to the end | none | ding (0.25) at 71.0 |

Audio: music bed (core audio `music`, volume 0.3, duckTo 0.12 under VO) calm and warm 0-7 s (new bed needed), filtered and sparse after the flip, cut at 62.0, soft return for the end card. TTS VO reads only the 13 captions, each starting at its caption time. Kokoro timing checks: caption 1 (6 words, about 2.3 s) ends by about 6.8, before the 7.0 hit (if it runs long, start it at 4.4); caption 12 (6 words) ends by about 64.8, well before caption 13 at 66.5.

Storyboard: `storyboard.json` in this folder is valid against studio/src/core/schema.ts (22 scenes, 78.00 s; captions drawn as text layers, core captions disabled; HUD state table passed to whatif/Hud as props with each scene's global start `t0`). The whatif/* components render as magenta "missing" boxes until the kit exists; the timing, captions, camera, grade, transitions and SFX are final. Regenerate it with `python3 backlog/whatif/whatif-friction-off-5-seconds/gen_storyboard.py backlog/whatif/whatif-friction-off-5-seconds/storyboard.json` after any timing change.
