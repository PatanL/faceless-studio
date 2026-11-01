---
episode: whatif-sun-gone-5-seconds
niche: whatif
format: short, 9:16, 1080x1920
working_title: "What if the Sun vanished for 5 seconds?"   # 8 words; "vanished", not @man_ia_c's "disappeared" (sameness rule, see Post plan)
target_runtime_s: 80
target_words_per_min:
  voiceover_incl_title: 59      # 79 spoken words (title + 13 captions, numbers read as words) / 80 s; PLAYBOOK TTS read of captions ~60-70
  captions_only: 52.5           # 70 caption words / 80 s; PLAYBOOK Shorts caption median 56 (43-65)
  all_on_screen_text: ~118      # captions + title x2 + HUD + panel labels + end fact; PLAYBOOK median 115 (103-131)
captions: 13 (70 words, mean 5.4, max 7)   # PLAYBOOK 10-13, mean 5.3-7.3, max 7-10; one claim per caption
caption_gap_median_s: 5.1                  # PLAYBOOK 5.0 (4.0-6.0); longest in-body voice silence 5.6 s (0:33.7-0:39.3, holds the midpoint interrupt)
new_onscreen_element_every_s: ~3.3         # PLAYBOOK median 3.8
voice: Kokoro-82M am_michael, speed 0.96, Spark CPU (pipeline/audio explainer settings). Reads the title + the 13 captions only. HUD, panel labels, title repeat and end fact are silent. Line lengths below were measured on the Spark (10:36 UTC run of a per-line timing script, 4 threads, nice 10).
house_look: whatif house kit shared with whatif-friction-off-5-seconds (upright serif captions, amber accent #FFB547, JetBrains Mono T+ clock with a speed chip, split-screen vantage labels). Deliberately not the @man_ia_c italic lower third / return-countdown HUD.
references:
  - id: "7693494009494342945"
    short: ELECTRONS
    url: https://www.tiktok.com/@man_ia_c/video/7693494009494342945
    views: 18200000
    outlier_score: 29.13
    why_chosen: Same H1 title formula and the same 80 s 9:16 three-layer text system (title card, lower-third caption, top-left HUD). We follow its spine of countdown, flip, wonder, rule plus short implication, textless break, ladder, mid-video full-frame interrupt, return and callback stamp, twist with a one-line HUD equivalence, black, title repeat and fact. Its twist caption + HUD equivalence pair (1:09-1:10) is the model for our twist.
  - id: "7693617402180881697"
    short: NEUTRONS
    url: https://www.tiktok.com/@man_ia_c/video/7693617402180881697
    views: 5100000
    outlier_score: 8.16
    why_chosen: Closest on clock mechanics and plants. Its frame-1 HUD subline is paid by the twist (0:00 -> 1:09); we plant ONE YEAR at 0:00 and pay it at 1:08.3. Also borrowed - the personal HUD stat in the body beat (0:11 YOUR WEIGHT), a huge HUD energy equivalence (0:26 EVERY GRAM), closing one loop and opening a longer one on the same beat (0:08), and the "[place], N later" stamp (1:06).
  - id: "7693305573487562016"
    short: OXYGEN
    url: https://www.tiktok.com/@man_ia_c/video/7693305573487562016
    views: 13400000
    outlier_score: 21.45
    why_chosen: Best model for a silent event with a baseline readout. Its HUD shows a normal reading before the event and the delta on the event (0:00-0:08), swaps meters when captions space out (0:39), snaps the ladder back to the ground under you (0:35), and runs a distance countdown to HERE (0:56-1:02). We borrow the baseline (sunlight on you in W/m2, 0 W/m2 on the cut), the meter swaps and the closing-distance readout.
secondary_references:
  - id: "7694025665993100576"
    short: POPSTAR-100x
    url: https://www.tiktok.com/@man_ia_c/video/7694025665993100576
    views: 4900000
    outlier_score: 7.84
    why_chosen: Device only - the closing-distance HUD that counts a threat's distance down to HERE across the whole video (0:00 THE STAR 2,020 ft -> 1:02 HERE). Our S6 runs the same device for the shadow (148.1 million km -> HERE at 0:38.1).
---

# What if the Sun vanished for 5 seconds?

**Twist premise.** The Sun blinks out for 5 seconds. On the beach nothing changes: its light and its gravity are both still on the way, so Earth keeps circling an empty spot. A 1.5-million-km gap of no light and no pull rolls outward at light speed, darkens Mercury and Venus, and reaches you 8 min 19 s after the Sun vanished. For 5 seconds Earth is dark and unpulled: it misses 12 hours' worth of all human energy use in sunlight and slides 7.4 cm off course on a straight line. Then everything comes back, but that palm's width grows to 149 km within 3 months, and every year of your life is now 47 µs longer.

**Why it should work, and where it is weak (PLAYBOOK §10C).** One invisible rule (light and gravity share one speed limit), a named place, a body line, a tight window, a return twist that lands on the viewer, exact computed numbers and a dated true fact at the end. Weak spot, said plainly: the 8-minute delay is the stock answer to this question (Vsauce "What If The Sun Disappeared?" 20.9M, plus MinutePhysics and Bright Side), so science-literate viewers will see it coming. The novelty has to come from what those videos skip, and the script leads with it: Earth still orbiting an empty spot in the first 10 s (the gravity half), the 5-light-second shell as a closing-distance threat, the 12-hour energy number, the 7.4 cm drift, and the permanent 149 km / 47 µs change. The "5 seconds" framing itself is new only among Shorts with under 1K views (backlog/whatif/TOPICS.md #4).

## Beat alignment table

| Our beat | Our time | Reference id + timestamp | Device borrowed | How we adapt it |
|---|---|---|---|---|
| S1 Premise card, pre-event clock, plant, baseline | 0:00-0:07 | ELECTRONS 0:00 (title + countdown + scope subline); NEUTRONS 0:00 (frame-1 HUD fact paid at 1:09); OXYGEN 0:00-0:07 (baseline instrument reading) | 7-9 word what-if title with one accent keyword; HUD counting down to the event; a quiet frame-1 plant; a normal reading that changes later | Title (8 words, "Sun" amber) sits in the beach panel, below the split seam. HUD: SUN VANISHES IN 0:07.000. S1 plant ONE YEAR: 365.256 DAYS (paid 1:08.3). S2 baseline SUNLIGHT ON YOU: 1,000 W/M² from 0:02 (paid 0:38.6 as 0 W/M²) |
| S2 Place you | 0:05.1 | ELECTRONS 0:05; NEUTRONS 0:05; OXYGEN 0:05 | Second-person line naming a real place, after the title clears | Copacabana at noon. The title clears at 0:05.0, so the caption never overlaps it |
| S3 Flip that changes half the frame | 0:07 | ELECTRONS 0:08 (clock flip + time factor + style change); OXYGEN 0:08 (the event is silent: flames vanish and a number changes) | Hard change on the clock's zero, plus a hit; one persistent tracker starts | Only the AT THE SUN panel changes (white flash ring, disc gone). The beach panel (COPACABANA · YOUR VIEW) is untouched. The HUD flips to the master tracker: an elapsed T+ clock with a fixed end mark (/ 8:24) and a speed chip (1×). Caption "Nothing happens. Yet." opens the loop instead of closing it |
| S4 Body first, screenshot moment | 0:08-0:12 | NEUTRONS 0:11 (YOUR WEIGHT personal HUD stat), 0:13 (POV hands); ELECTRONS 0:15 (effect on your own hands) | First effect on the viewer's body, turned into a personal HUD stat | The ghost Sun: the beach sky still shows the Sun while the top panel is empty, labelled STILL SHINING. STILL PULLING. Caption "Your skin still feels warm." with the HUD stat THE LIGHT ON YOUR SKIN: 8 MIN OLD and a POV hand inset in warm light |
| Short loop closes, longer one opens | 0:07-0:12 | NEUTRONS 0:08 (one clock closes and a longer one opens on the same beat) | Close a loop and open a bigger one in the same frame | Subline AT THE SUN: BACK IN 5 S counts to zero at 0:12 with nothing broken; on that frame it becomes SHADOW: 148.1 MILLION KM AWAY, the closing-distance threat |
| S5 Rule, short implication, textless break | 0:16.3-0:25.8 | ELECTRONS 0:21 (rule), 0:25 (4-word implication), 0:28-0:32 (4 s without text); NEUTRONS 0:16-0:20 (4 s breather) | A plain-science rule line; a much shorter line that implies the consequence; 3-4 s with no caption while the picture changes | Rule "Its light needs 8 minutes 19 seconds." (0:16.3, read in 2.4 s), then 1.9 s of silence, then "So does its gravity." (0:20.6). Textless 0:21.8-0:25.8 (4.0 s) while the dark ring peels off the Sun |
| One time chip | 0:07-1:03.1 | ELECTRONS 0:08 / NEUTRONS 0:08 (a stated time factor, so the clock adds up) | Time factor shown beside the clock | One chip changes value: 1× (0:07), ▶▶ 30× (0:22), SLOW-MO 5× (0:38.6), 1× (1:03.1). The T+ clock is computed from it, so it always adds up |
| S6 Closing-distance ladder | 0:12-0:38.1 | OXYGEN 0:56-1:02 (THE FIRE counts down in ft to HERE); POPSTAR 0:00-1:02 (THE STAR distance counts to HERE, secondary ref) | A threat's distance counting down to HERE; rungs named on the way in | S1: SHADOW: N MILLION KM AWAY, from 148.1 to HERE at 0:38.1. Rungs: Mercury (caption 0:25.8, dark at 0:27.9), shadow thickness (caption 0:31.5, ScaleBar with 4 Moon-distance ticks), Venus (HUD 0:33.5). A YOU pin on Earth's orbit shows how far is left |
| Midpoint full-frame interrupt | 0:38.1 | ELECTRONS 0:40 (white-out); NEUTRONS 0:28 (black, then a new look) | One full-frame blank that resets attention | A 2-frame white rim as the shell's bright edge hits Earth, then 0.5 s of pure black with the HUD hidden and 0.4 s of hard silence |
| Delta on the cut | 0:38.6 | OXYGEN 0:08 (the baseline reading becomes a delta on the event frame) | The planted baseline is shown changed, on the cut | SUNLIGHT ON YOU: 0 W/M² · SOLAR: 0 appears the instant the HUD returns. The clock reads T+8:19.100, which is right for 0.5 s of screen at 5× slow motion |
| S7 Energy equivalence + live counters | 0:41-1:03.1 | NEUTRONS 0:26 (EVERY GRAM: 100 TONS OF TNT, a huge HUD equivalence); ELECTRONS 0:42 (live climbing number in the subline); OXYGEN 0:39 (meter swap) | One big equivalence as a climbing counter; swap meters when captions space out | S2 MISSED SUNLIGHT: N HRS OF ALL HUMAN ENERGY climbs 1.4 -> 12.3. From 0:49 S3 OFF ORBIT BY N CM climbs 1.4 -> 7.4. Two numbers move through the darkest stretch |
| Body in the dark | 0:44 | OXYGEN 0:35 (the ladder snaps back to the ground under you); NEUTRONS 0:13 (POV hands) | Drop from the event's scale back to the viewer's own body | "You can't see your own hand." POV: a faint dashed outline where your hand is and a drifting afterimage of the bright beach. This is honest: eyes cannot dark-adapt in 5 s |
| Planet view | 0:48-0:56 | ELECTRONS 0:42-0:51 (wide space view while the number climbs); NEUTRONS 0:43-0:44 | Bright space view after the interrupt, terse caption | A glowing space diagram: Earth leaves its amber orbit arc on a white tangent, the Moon alongside, the dark band's bright trailing edge on its way |
| Return-to-you dip | 0:56-1:03.1 | PLAYBOOK §5 return-to-you dips (NEUTRONS 0:13, PI=3) | Planet scale measured against your body | "It slips a palm's width off course." Palm next to a drift bar driven by the same formula as the HUD counter |
| S8 Return + callback stamp | 1:03.1-1:05.9 | ELECTRONS 1:04-1:06; NEUTRONS 1:04-1:06 | "[X] BACK", one reassuring line, a "[place], N later" stamp | SUN BACK; clock frozen at T+8:24.000; COPACABANA, 8 MIN 24 S LATER; light sweeps back over the beach; "Light and gravity return." |
| S9 Twist T1 (the damage stays and lands on you) | 1:05.9-1:11 | ELECTRONS 1:09-1:10 (twist caption + HUD equivalence); NEUTRONS 1:09-1:10 (the twist pays the frame-1 plant) | The undo does not undo it; one caption plus HUD equivalence lines | "But Earth's orbit stays shifted." HUD amplification THAT 7.4 CM BECOMES 149 KM IN 3 MONTHS (1:06.7), then the plant pays on the viewer: YOUR YEAR NOW: 365.256 DAYS + 47 µS. FOREVER. (1:08.3) |
| S10 Black + bookend + true fact | 1:11-1:20 | ELECTRONS 1:12-1:20; NEUTRONS 1:12-1:20 (fact held about 6 s) | About 1-2 s black, exact title repeat for the loop, one small-caps dated fact; CTA only in the post caption | 1.5 s black; title repeat at 1:12.5 in the frame-0 position; fact 1:13.5-1:20 (6.5 s): GW170817, light and gravity arriving together |

## Script

Layers: **TITLE** (serif card, in the beach panel), **CAPTION** (upright serif lower third above y = 1480, read by the voice), **HUD** (top-left inside SAFE_AREA: label line L, big mono clock T with a speed chip, sublines S1-S3; full table below), **PANEL** (small-caps labels inside the AT THE SUN panel, the beach panel or the space diagram). Times are screen seconds. Story time T starts at 0 when the Sun vanishes (screen 0:07.0). VO end times are cue + measured Kokoro length.

### Hook (first line + first visual)

- First visual (frame 0): 9:16 split screen. Top 40% (y 0-768): flat space panel, black with a few stars, the Sun as a bright amber disc with soft corona rings; small label SUN · 149.6 MILLION KM AWAY fades in at 0:01. Bottom 60%: flat vector Copacabana at noon: white sand, turquoise sea, the wave-pattern promenade, the green headland, umbrellas, a small Sun high in the sky at top right (the "ghost Sun" later), and a stick-figure YOU in the foreground with a short, hard noon shadow. The title sits in the beach panel's sky (y 950-1230), clear of the seam. HUD already counting.
- First line (VO + TITLE, 0:00.3-0:02.6): What if the **Sun** vanished for 5 seconds?

### Beat S1, premise card + pre-event clock (0:00-0:07)

- 0:00.0 HUD: SUN VANISHES IN / 0:07.000 counting down / S1 ONE YEAR: 365.256 DAYS
- 0:00.3 TITLE + VO (to 0:02.6): What if the Sun vanished for 5 seconds? (title held to 0:05.0, fading 4.7-5.0)
- 0:02.0 HUD S2: SUNLIGHT ON YOU: 1,000 W/M²
- 0:05.1 CAPTION + VO (to 0:06.9) (S2, place you): You're on Copacabana beach at noon.

### Beat S3-S4, the flip that changes half the frame (0:07-0:12)

- 0:07.0 PANEL top: white flash ring, the disc pops to nothing in 2 frames; label AT THE SUN. PANEL bottom: COPACABANA · YOUR VIEW. Nothing else on the beach changes.
- 0:07.0 HUD: SINCE THE SUN VANISHED / T+0:00.000 counting up (end mark / 8:24) / chip 1× / S1 AT THE SUN: BACK IN 5.0 S counting down / S2 SUNLIGHT ON YOU: 1,000 W/M² · STILL ARRIVING
- 0:08.0 CAPTION + VO (to 0:09.4): Nothing happens. Yet.
- 0:08.5 PANEL beach, next to the ghost Sun: STILL SHINING. STILL PULLING.
- 0:10.3 HUD S2: THE LIGHT ON YOUR SKIN: 8 MIN OLD
- 0:10.5 CAPTION + VO (to 0:12.1) (body): Your skin still feels warm. POV hand inset in warm light over the sand.
- 0:12.0 PANEL top: the disc pops back; label AT THE SUN: BACK. HUD S1 swaps on the same frame to SHADOW: 148.1 MILLION KM AWAY, counting down.

### Beat S5, the rule and the gravity line (0:12-0:25.8)

- 0:13.0 Top panel starts pulling out: Mercury and Venus orbits enter, and a thin dark ring, the gap in sunlight, leaves the Sun.
- 0:16.3 CAPTION + VO (to 0:18.7): Its light needs 8 minutes 19 seconds.
- 0:20.6 CAPTION + VO (to 0:21.8): So does its gravity. (1.9 s of silence before it)
- 0:22.0 HUD chip: ▶▶ 30×. The clock races from T+0:15.000. HUD S2 clears.
- 0:21.8-0:25.8 no caption (4.0 s). Whip up to the full-frame space view: the dark band peels off the Sun and expands across the inner orbits through a pale amber wash of sunlight.

### Beat S6, the shadow closes in (0:25.8-0:38.1)

- 0:25.8 CAPTION + VO (to 0:28.0): Mercury loses its sunlight first.
- 0:27.9 HUD S2: MERCURY: DARK AT T+3:13 (the Mercury dot greys as the band crosses it)
- 0:31.5 CAPTION + VO (to 0:33.7): The shadow is four Moon-distances thick. ScaleBar 1.5 MILLION KM beside the band.
- 0:33.5 HUD S2: VENUS: DARK AT T+6:01 (the Venus dot greys)
- 0:36.0 Push in on Earth and its YOU pin; HUD S1 reads SHADOW: 19.2 MILLION KM AWAY, clock T+7:15 and racing.
- 0:37.97 HUD S1: SHADOW: HERE (the band's leading edge touches the YOU pin)

### Midpoint interrupt (0:38.1)

- 0:38.07-0:38.13 2 frames of white rim (the shell's bright edge) on Earth.
- 0:38.13-0:38.63 Full-frame black, HUD hidden. 0.4 s of hard silence, then the drone.
- 0:38.63 HUD: SINCE THE SUN VANISHED / T+8:19.100 / chip SLOW-MO 5× / S1 SHADOW HERE · LIGHT BACK IN 4.9 S counting down / S2 SUNLIGHT ON YOU: 0 W/M² · SOLAR: 0

### Beat S7, five dark seconds (0:38.6-1:03.1)

- 0:39.3 CAPTION + VO (to 0:40.8): The beach goes black at noon.
- 0:41.0 HUD S2 swaps to MISSED SUNLIGHT: 1.4 HRS OF ALL HUMAN ENERGY, climbing to 12.3 at 1:03.1.
- 0:44.0 CAPTION + VO (to 0:45.4): You can't see your own hand.
- 0:49.0 CAPTION + VO (to 0:50.9): Earth stops curving and flies straight.
- 0:49.0 HUD S3: OFF ORBIT BY 1.4 CM, climbing every frame.
- 0:56.0 CAPTION + VO (to 0:57.9) (return to you): It slips a palm's width off course.
- 1:03.13 HUD S3 reaches OFF ORBIT BY 7.4 CM, S2 reaches 12.3 and S1 reaches LIGHT BACK IN 0.0 S on the same frame.

### Beat S8, return and callback (1:03.1-1:05.9)

- 1:03.13 HUD: SUN BACK / T+8:24.000 (frozen) / chip 1× / S1 COPACABANA, 8 MIN 24 S LATER / S2 MISSED: 12 HOURS OF ALL HUMAN ENERGY / S3 OFF ORBIT BY 7.4 CM
- 1:03.4 CAPTION + VO (to 1:04.8) (false resolution): Light and gravity return.

### Beat S9, twist (1:05.9-1:11)

- 1:05.9 CAPTION + VO (to 1:07.6): But Earth's orbit stays shifted.
- 1:06.7 HUD S3: THAT 7.4 CM BECOMES 149 KM IN 3 MONTHS (S2 clears)
- 1:08.3 HUD S1 (the 0:00 plant pays off): YOUR YEAR NOW: 365.256 DAYS + 47 µS. FOREVER.

### Beat S10, black + bookend + true fact (1:11-1:20)

- 1:11.0-1:12.5 black, no text, music tail only
- 1:12.5 TITLE (silent, exact repeat, same position as frame 0, "Sun" in amber): What if the Sun vanished for 5 seconds?
- 1:13.5 END FACT (small caps, silent, held to 1:20): IN 2017, LIGHT AND GRAVITY CROSSED 130 MILLION LIGHT-YEARS AND ARRIVED 1.7 S APART. SAME SPEED.

### Post caption (not on screen)

The Sun goes out for five seconds and the beach stays bright, because its light is still on the way. So is its gravity: Earth keeps circling a spot where nothing is. Eight minutes later a shadow four Moon-distances thick rolls over Copacabana. For five seconds nothing pulls on Earth, and it slides a palm's width off its path. Then it all comes back, except the year: it is now 47 microseconds longer, for good. What should vanish for 5 seconds next: the Moon or Jupiter? #whatif #space #physics #sun

## HUD state table

One screen-locked `whatif/Hud` layer (top-left, x >= 70, y >= 250, inside SAFE_AREA), repeated in every scene with `t0` = the scene's global start, so it stays continuous across cuts. L = small-caps label, T = big mono clock (JetBrains Mono, tabular-nums), C = speed chip beside T, S1-S3 = small-caps sublines. A dash means the line is hidden. Every live value is a formula, never typed by hand (t = screen seconds):

- Story time T(t): 0 before 7.0; t - 7 for 7.0-22.0; 15 + 30 (t - 22) for 22.0-38.133; 499 + (t - 38.133)/5 for 38.133-63.133; frozen at 504 = 8:24.000 after.
- Shadow distance D = 0.299792 x (499 - T) million km. Shown with 1 decimal; HERE once D < 1.5 (the shell's own thickness), i.e. from 37.97.
- tau = (t - 38.133)/5 story seconds of darkness. Light back in = 5 - tau. Missed sunlight = 2.453 x tau hours. Drift = 0.2965 x tau² cm.

| Screen time | L | T | C | S1 | S2 | S3 |
|---|---|---|---|---|---|---|
| 0.0-7.0 | SUN VANISHES IN | 0:07.000 -> 0:00.000 | - | ONE YEAR: 365.256 DAYS | from 2.0: SUNLIGHT ON YOU: 1,000 W/M² | - |
| 7.0-10.3 | SINCE THE SUN VANISHED | T+ T(t), end mark / 8:24 | 1× | AT THE SUN: BACK IN {5 - T} S | SUNLIGHT ON YOU: 1,000 W/M² · STILL ARRIVING | - |
| 10.3-12.0 | same | same | 1× | same | THE LIGHT ON YOUR SKIN: 8 MIN OLD | - |
| 12.0-22.0 | same | same | 1× | SHADOW: {D} MILLION KM AWAY (148.1 -> 145.1) | THE LIGHT ON YOUR SKIN: 8 MIN OLD | - |
| 22.0-27.94 | same | same (races) | ▶▶ 30× | SHADOW: {D} MILLION KM AWAY (145.1 -> 91.7) | - | - |
| 27.94-33.53 | same | same | ▶▶ 30× | SHADOW: {D} (91.7 -> 41.4) | MERCURY: DARK AT T+3:13 | - |
| 33.53-37.97 | same | same | ▶▶ 30× | SHADOW: {D} (41.4 -> 1.5) | VENUS: DARK AT T+6:01 | - |
| 37.97-38.133 | same | T+8:19.000 | ▶▶ 30× | SHADOW: HERE | VENUS: DARK AT T+6:01 | - |
| 38.133-38.633 | (whole HUD hidden: black interrupt) | | | | | |
| 38.633-41.0 | SINCE THE SUN VANISHED | T+8:19.100 -> | SLOW-MO 5× | SHADOW HERE · LIGHT BACK IN {5 - tau} S | SUNLIGHT ON YOU: 0 W/M² · SOLAR: 0 | - |
| 41.0-49.0 | same | same | SLOW-MO 5× | same | MISSED SUNLIGHT: {2.453 tau} HRS OF ALL HUMAN ENERGY (1.4 -> 5.3) | - |
| 49.0-63.133 | same | same -> T+8:24.000 | SLOW-MO 5× | same (-> 0.0 S) | same (5.3 -> 12.3) | OFF ORBIT BY {0.2965 tau²} CM (1.4 -> 7.4) |
| 63.133-66.7 | SUN BACK | T+8:24.000 (frozen) | 1× | COPACABANA, 8 MIN 24 S LATER | MISSED: 12 HOURS OF ALL HUMAN ENERGY | OFF ORBIT BY 7.4 CM |
| 66.7-68.3 | SUN BACK | frozen | 1× | COPACABANA, 8 MIN 24 S LATER | - | THAT 7.4 CM BECOMES 149 KM IN 3 MONTHS |
| 68.3-71.0 | SUN BACK | frozen | 1× | YOUR YEAR NOW: 365.256 DAYS + 47 µS. FOREVER. | - | THAT 7.4 CM BECOMES 149 KM IN 3 MONTHS |
| 71.0-80.0 | (hidden) | | | | | |

Spot checks: at 13.0 D = 147.8; at 22.0 T = 15 s, D = 145.1; at 27.94 T = 193.2; at 33.53 T = 360.9; at 36.0 T = 435 = 7:15, D = 19.2; at 38.133 T = 499.0; at 38.633 T = 499.1 = 8:19.100; at 49.0 tau = 2.173, drift 1.40 cm, missed 5.3 h; at 56.0 drift 3.79 cm; at 63.133 tau = 5, drift 7.41 cm, missed 12.3 h, T = 504 = 8:24.

## Shot list

Scenes are laid end to end (core schema), so no two shots overlap. Kit vocabulary: core layers (`rect`, `circle`, `text`, `svg`, `particles`, `component`), core camera (presets, keyframes, `shake`) and transitions (`cut`, `fade`, `dipBlack`, `whip`). Core camera, shake and grade act on the whole scene and layers do not clip, so in split-screen shots each panel's motion is an internal prop track of its own component (which clips to its own box), and the darkness is a layer, never a scene grade. Existing pieces: `explainer/You` (poses stand, shrug, panic, wave; a pose change is two layers with start/end), `explainer/Tag`, core `particles` preset `stars`. Shared whatif kit (same names as the rest of the whatif backlog): `whatif/Hud`, `whatif/TitleCard`, `whatif/SerifCaption`, `whatif/EndCard` (the storyboard draws title, captions and end card as core text layers until those exist). NEW for this episode: `whatif/SolarMap`, `whatif/BeachNoon`, `whatif/Hand` (one drawing, three looks). SFX are from `studio/public/sfx/`.

| # | t_start | t_end | Shot type | Visual (kit vocabulary) | Camera / motion | SFX / music |
|---|---|---|---|---|---|---|
| 1 | 0:00.0 | 0:07.0 | Split screen, title | Top 40%: `whatif/SolarMap` mode `sunClose` (amber disc + 3 corona rings, a few stars), label SUN · 149.6 MILLION KM AWAY from 0:01. Bottom 60%: `whatif/BeachNoon` (sand, sea gradient, wave-stripe promenade, headland, 3 umbrellas, small Sun top right) with `explainer/You` stand and a short hard shadow. Title text layers in the beach sky (y 950-1230). `whatif/Hud` | Beach panel's own `zoom` track 1.00 -> 1.03; no scene camera | music documentary_pulse from 0:00; `tick` at 4.0, 5.0, 6.0 |
| 2 | 0:07.0 | 0:12.0 | Split screen, event | Top: SolarMap `sunScale` track 1 -> 0 in 2 frames + a white expanding ring (`circle`, scale and opacity keyframes), label AT THE SUN. Bottom: unchanged beach; label COPACABANA · YOUR VIEW; ghost-Sun label STILL SHINING. STILL PULLING. at 1.5; You stand (0-1.0) then shrug (1.0-5.0). `whatif/Hand` (warm look) as a rounded inset at bottom right of the beach panel, 3.5-5.0 | none (the hit is the ring and the disc pop) | `impact` 0.0; beach bed continues |
| 3 | 0:12.0 | 0:22.0 | Split screen | Top: `sunScale` 0 -> 1 with backOut at 0, label AT THE SUN: BACK; from 1.0 the SolarMap `zoom` track goes 1.0 -> 0.35, revealing Mercury and Venus orbits and a thin dark ring leaving the Sun. Bottom: unchanged beach | Top panel `zoom` track only | `pop` 0.0; `clock_ticking` loop 13.0-22.0 (stops when the clock goes 30×) |
| 4 | 0:22.0 | 0:38.13 | Full-frame space diagram | `whip` (up) into SolarMap mode `inner`: pale amber radial wash = sunlight; a dark band (5 light-s, exaggerated) with thin bright leading and trailing edges expands at constant speed; Mercury, Venus and Earth dots on dashed orbits, a small YOU pin on Earth; dots grey as the band crosses them (Mercury 5.94, Venus 11.53). Core `particles` stars. ScaleBar at 9.5: `explainer/ScaleBar` labelled 1.5 MILLION KM plus 4 `rect` Moon-distance ticks. White `rect` flash at 16.07-16.13 (2 frames) | SolarMap `zoom` track continues the pull-out so Earth's orbit is in frame by 11.0; push in on the YOU pin from 14.0 | `whoosh_long` 0.0; `ding` 5.94 and 11.53 (soft); `riser` 13.5 |
| 5 | 0:38.13 | 0:38.63 | Full-frame interrupt | Pure black, HUD hidden | none | music cut at 38.13; 0.4 s silence; `drone` bed from 38.53 |
| 6 | 0:38.63 | 0:44.0 | Wide, beach dark at noon | BeachNoon under a full-frame navy `rect` (`#0B1A3A`, blend multiply). Above it in z: sparse amber office windows along the promenade (`rect`s), about 30 phone screens on the sand (small white-blue `rect`s, flicker on one by one), 4 car headlight pairs; `explainer/You` panic silhouette. No stars (eyes are not dark-adapted) | core `drift` | drone bed; `heartbeat_slow` 1.5 |
| 7 | 0:44.0 | 0:48.0 | POV, hand in the dark | Navy-black frame; `whatif/Hand` (dashed outline look, opacity 0.15); afterimage blob (soft magenta-green `circle`, blur 60, drifting and fading 1 -> 0.2) | slow core `pushIn` 0.3 | drone; `heartbeat_slow` |
| 8 | 0:48.0 | 0:56.0 | Full-frame space diagram, close on Earth | SolarMap mode `earthClose`: bright blue Earth dot, Moon dot alongside, amber dashed orbit arc curving away, Earth carrying straight on along a white tangent line, label NO PULL; the band's bright trailing edge visible sunward and closing in; core `particles` stars | slow core `pushIn` | `whoosh` (soft) 1.0 |
| 9 | 0:56.0 | 1:03.13 | Insert, scale comparison | Navy card. `whatif/Hand` (bright outline look) at true relative size to a drift bar: a core `rect` whose `scaleX` keyframes sample 0.2965 tau² every 0.5 s (3.79 cm at 0:56.0 -> 7.41 cm at 1:03.13); dashed OLD ORBIT line and solid EARTH line separated by the same keyframes | slow core `pushIn` | `tick` at 4, 5, 6, 7 cm = 0:56.50, 0:58.67, 1:00.63, 1:02.43 |
| 10 | 1:03.13 | 1:05.9 | Wide, return | Beach as shot 6, then the navy `rect` keyframes x 50% -> 150% over 0.3 s (light sweeps back), lit windows and phones fade; You panic (0-0.4) then wave | core `pullOut` 0.4 | `whoosh` 0.0; documentary_pulse back from 63.13 |
| 11 | 1:05.9 | 1:11.0 | Full-frame orbit diagram | SolarMap mode `fullOrbit`: old orbit dashed white, new orbit solid amber, offset exaggerated with label UP TO 149 KM at 0.8; Earth dot with YOU pin; `explainer/Tag` +47 µS / YEAR at 2.4 | slow core `pullOut` | `stinger` 0.0 |
| 12 | 1:11.0 | 1:12.5 | Black | Black | none | music tail, then silence |
| 13 | 1:12.5 | 1:20.0 | End card | Title repeat in the frame-0 position, "Sun" amber; small-caps fact from 1.0 (two lines), held to the end; the last frame matches frame 0's title for the loop | none | `ding` (very soft) 0.0 |

## Fact file (every number on screen)

- Sun-Earth mean distance 149.6 million km (1 AU = 149,597,870.7 km, IAU 2012); light time 499.0 s = 8 min 19 s.
- Light time at mean distance: Mercury 0.387 AU, 193.2 s = 3 min 13 s; Venus 0.723 AU, 360.9 s = 6 min 1 s. Mercury's real value swings about 2.6-3.8 min with its eccentric orbit; we show the mean.
- Shadow thickness: 5 light-seconds = 1,498,962 km = 3.90 Earth-Moon distances (384,400 km). Caption rounds to four.
- Shadow distance in the HUD: 0.299792 million km per story second, 148.1 million km at T = 5 s, HERE at T = 499 s.
- Gravity changes travel at the speed of light: GW170817 (17 Aug 2017), LIGO/Virgo with Fermi GBM; gamma rays arrived 1.7 s after the merger signal from NGC 4993, about 40 Mpc (about 130 million light-years). Over roughly 4e15 s of travel that is the same speed to about 1 part in 10^15 (Abbott et al. 2017, ApJL 848 L13; arXiv:1710.05834). The end card says "light and gravity" for the gravitational waves.
- Clear-sky noon sunlight at the surface: about 1,000 W/m² (the standard solar-panel test value). SOLAR: 0 is true on the day side; the night side is at zero anyway.
- The light on your skin at T = 0-5 s left the Sun about 8 min 19 s earlier (HUD rounds to 8 MIN OLD).
- Missed sunlight: Earth intercepts 1,361 W/m² x pi x (6,371 km)² = 1.735e17 W; in 5 s that is 8.68e17 J. World primary energy use 2023 was about 620 EJ (Energy Institute Statistical Review of World Energy 2024), or 7.08e16 J per hour, so 5 s of sunlight = 12.3 hours of all human energy use (2.453 h per story second). Top-of-atmosphere figure.
- Earth's orbital speed 29.78 km/s; the Sun's pull on Earth 0.00593 m/s². With no pull for 5 s Earth moves on its tangent, and its distance from the old circular path grows as ½·a·t² = 7.41 cm (0.2965 tau² cm). Adult palm width is about 7.5-9 cm.
- Free fall: you and Earth drift together, so nobody feels the missing pull (equivalence principle). The script no longer voices this; it stays here for comments.
- After the gap Earth has about 2.97 cm/s of outward velocity. That gives an eccentricity of about 1.0e-6, so its distance from the Sun swings by up to about 149 km, reached a quarter orbit (91 days, about 3 months) later. The semi-major axis grows by 14.8 cm, so the year lengthens by 46.9 µs (shown as 47 µs). The sidereal year is 365.256 days. Checked with an RK4 integration in `python3` (circular-orbit start, 600 s steps): drift 7.41 cm, v_r 2.97 cm/s, max offset 149 km at day 91, dT 46.9 µs.
- "Forever" is a two-body statement: the old orbit is never restored. The pulls of the other planets change Earth's orbit by far more than this over years and are chaotic over millions of years, so the 47 µs would never be measurable. A commenter can raise this, and it is the honest-speculation note (PLAYBOOK T12).
- Physics caveat: in general relativity a mass cannot simply vanish (it breaks mass-energy conservation), so "a gap in gravity moving out at light speed" is the standard pop-science idealisation of the thought experiment. It is fine as a what-if; expect comments on it.
- Eyes: in sudden darkness, light-adapted eyes need many minutes to dark-adapt, so in 5 s you would see black and an afterimage, not stars. Offices and shops on the promenade do have lights on at noon, and phone screens glow, so those are the only lit things in shot 6.
- Pacing timeline check: 1× from 0:07.0 (T = 0) to 0:22.0 (T = 15 s). TIME 30×: Mercury at T = 193.2 s lands at 0:27.94; Venus at T = 360.9 s at 0:33.53; Earth at T = 499 s at 0:38.133 (frame 1144 at 30 fps). The 0.5 s black is 0.1 s of story at 5×, so the HUD returns at T+8:19.100. TIME 5×: the 5 s gap fills 0:38.133-1:03.133; the callback stamp reads T = 504 s = 8 min 24 s.

## Production notes

- **VO timing (measured on the Spark, Kokoro am_michael 0.96):** title 2.26 s, captions 1.81 / 1.39 / 1.62 / 2.44 / 1.23 / 2.20 / 2.23 / 1.54 / 1.39 / 1.87 / 1.86 / 1.39 / 1.69 s. Every line ends at least 1.1 s before the next starts; the rule line ends at 0:18.7, so 1.9 s of silence sit before "So does its gravity." at 0:20.6. TTS spellings: "eight minutes nineteen seconds", "four Moon distances", "five seconds".
- **kit_gaps.** None of the whatif pieces exist yet (studio/src/kits/whatif is not created). Shared with the niche: `whatif/Hud` (lines L, T + chip, S1-S3 as segment lists with static text or a formula/track; `t0` per scene; tabular-nums mono), `whatif/TitleCard` / `whatif/SerifCaption` / `whatif/EndCard`, plus @fontsource/source-serif-4 and @fontsource/jetbrains-mono installed on the Spark only. This episode: `whatif/SolarMap` (modes sunClose, inner, earthClose, fullOrbit; internal `zoom` and `sunScale` tracks; band radius driven by T; clips to its own svg), `whatif/BeachNoon` (day art only; the night look is the navy multiply rect plus core layers; internal `zoom` track; clips to its own svg; about 150 lines of SVG), `whatif/Hand` (one palm SVG with `look`: warm, dashed, bright). `explainer/ScaleBar` has no tick prop, so the Moon-distance ticks are 4 core rects.
- **beach_ambience** has no source and needs no download: synthesise it on the Spark, e.g. `ffmpeg -f lavfi -i "anoisesrc=color=brown:amplitude=0.5:d=20" -af "lowpass=f=900,volume='0.6+0.4*sin(2*PI*t/7)':eval=frame,afade=t=in:d=1,afade=t=out:st=19:d=1" -ar 48000 -ac 1 studio/public/sfx/beach_ambience.wav` (or add it to pipeline.audio.synth). The storyboard leaves it out until the file exists.
- **Storyboard:** `storyboard.json` in this folder validates against studio/src/core/schema.ts (Spark, Node 22: `ok 9:16 30fps 13 scenes 80.00s`). Captions, title and end card are core text layers (core captions disabled); the HUD state table is passed to `whatif/Hud` as props with each scene's global start `t0`. Scene boundaries sit on exact frames (0:38.133 = frame 1144, 1:03.133 = frame 1894). The whatif/* components render as missing boxes until the kit exists; timing, captions, camera, transitions and SFX are final. Regenerate with `python3 backlog/whatif/whatif-sun-gone-5-seconds/gen_storyboard.py backlog/whatif/whatif-sun-gone-5-seconds/storyboard.json` after any timing change.
- **Music:** documentary_pulse 0:00-0:38.13, hard cut; `drone` bed 0:38.53-1:03.13; documentary_pulse again 1:03.13-1:11 with a 1.5 s fade.
- **Phone-screen check:** the darkest stretch is 0:38.1-0:48.0. Shot 6 has to read at phone brightness (amber windows and phone screens at full opacity above the multiply rect); shot 8 onward is a bright diagram. Check one Spark still at 0:41 and one at 0:46 before the full render.

## Post plan (monetization and sameness, pending R5)

- research/R5/ is still empty, so nothing below has been checked against a policy file. Re-check before posting.
- **Sameness.** The whatif backlog has four "... for 5 seconds" Shorts (calcium, friction, light-walking-speed, sun) on one HUD template. Do not post two of them back to back: put at least two different-format whatif posts (e.g. moon-10x-closer, earth-had-rings) between any two of them. This episode varies the formula on purpose: the title verb is "vanished" (calcium uses "disappeared", friction "switched off"), the hook device is a split-screen contradiction with vantage labels (not a single-place countdown), the master tracker is an elapsed T+ clock (not a return countdown), and the ladder is closing distance (not scale outward) (pipeline/templates/explainer.md sameness rule).
- **AI voice disclosure (decision to confirm in R5):** the Kokoro narrator is synthetic but the content is an obviously animated diagram with no realistic person, place footage or event, so on YouTube we would not tick "altered or synthetic content" (it covers realistic content) and would add "Narration: synthetic voice" to the description. On TikTok, switch on the AI-generated content label anyway (cheap and transparent).

## PLAYBOOK checklist

- One rule changed, universal, no IP: yes (the Sun vanishes; light and gravity keep their real, shared speed).
- Tracker on screen from hook to payoff: HUD clock 0:00-1:11 (pre-event countdown, then one T+ clock to the callback stamp).
- Master loop: the T+ clock "SINCE THE SUN VANISHED" opens at 0:07 and closes at 1:03.1 (span 56.1 s = 70% of runtime, closes at 79%); its end mark (/ 8:24) is on screen the whole time. Nested loops: AT THE SUN: BACK IN (0:07-0:12), SHADOW distance (0:12-0:38.1), LIGHT BACK IN (0:38.6-1:03.1), the ONE YEAR plant (0:00-1:08.3); at least two open at every point after 0:07.
- Ladder with one number per rung, closing in on you: shadow 148.1 million km, Mercury 3:13, shadow 1.5 million km thick, Venus 6:01, HERE, 0 W/m², 12.3 hours of human energy, 7.4 cm (your palm), 149 km, then your own year +47 µs (top rung, personal).
- Dated precedent: GW170817 end card.
- Reversal in the last 20%: T1, the damage stays (1:05.9), built from the 0:20.6 gravity line and the 0:00 ONE YEAR plant, and it lands on the viewer.
- Ending calls back the place: COPACABANA, 8 MIN 24 S LATER.
- Comment question only in the post text: a series-harvest question (the Moon or Jupiter).
- Title 8 words, held 0:00-0:05.0; event at 0:07 (9%); place line 0:05.1 and body line 0:10.5, both before 25%; rule line, 4-word implication, 4.0 s textless break; full-frame interrupt at 48%; return 79%, twist 82%, black + title + fact in the last 11%.
- 13 captions, 70 words, max 7, median caption gap 5.1 s; 3 of 13 captions in second person (23%, one line above the Shorts range, kept for the place, body and hand beats); VO about 59 wpm.
