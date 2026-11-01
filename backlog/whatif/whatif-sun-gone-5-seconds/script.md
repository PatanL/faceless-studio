---
episode: whatif-sun-gone-5-seconds
niche: whatif
format: short, 9:16, 1080x1920
working_title: "What if the Sun disappeared for 5 seconds?"
target_runtime_s: 78
target_words_per_min:
  voiceover_incl_title: 67      # 87 VO words / 1.3 min; PLAYBOOK TTS read of captions = 60-70 wpm
  captions_only: 61             # 79 caption words; PLAYBOOK Shorts caption median 56 (43-65)
  all_on_screen_text: ~120      # PLAYBOOK median 115 (103-131)
captions: 14 (mean 5.6 words, max 8)   # PLAYBOOK 10-13, mean 6.7, max 7-10; one extra because the dark phase is long
new_onscreen_element_every_s: ~3.5     # PLAYBOOK median 3.8
voice: Kokoro-82M on Spark CPU, calm male or female narrator, reads title + captions only; end card is silent
references:
  - id: "7693494009494342945"
    short: ELECTRONS
    url: https://www.tiktok.com/@man_ia_c/video/7693494009494342945
    views: 18200000
    outlier_score: 29.13
    why_chosen: Same title formula (H1, "[thing] vanished for 5 seconds"), same 80 s 9:16 three-layer text system (title card, lower-third caption, top-left HUD). Its countdown -> flip -> wonder -> rule + short implication line -> textless break -> outward ladder -> mid-video full-frame interrupt -> return -> "undo makes it worse" twist -> title repeat + fact is the spine we follow beat for beat.
  - id: "7693617402180881697"
    short: NEUTRONS
    url: https://www.tiktok.com/@man_ia_c/video/7693617402180881697
    views: 5100000
    outlier_score: 8.16
    why_chosen: Closest on clock mechanics. It runs several clocks (pre-event, return, a second threat that races the return) and plants a quiet HUD fact in frame 1 that the ending pays. We borrow the multi-clock spine, the "[place], N seconds later" callback stamp and the "the fix does not fix it" ending, and invert its slow-motion rule into a fast-forward then slow-motion pair.
  - id: "7693305573487562016"
    short: OXYGEN
    url: https://www.tiktok.com/@man_ia_c/video/7693305573487562016
    views: 13400000
    outlier_score: 21.45
    why_chosen: Best model for a silent event with a baseline readout. Its HUD shows a normal measurement before the event and the delta after, swaps the HUD meter whenever a caption gap runs long, and opens with a body sensation. We borrow the baseline readout (sunlight on the beach in W/m2), the meter swap and the body-first line.
---

# What if the Sun disappeared for 5 seconds?

**Twist premise.** The Sun blinks out for 5 seconds. On the beach, nothing changes, because its light and its gravity are still on the way. The genre's "return" clock hits zero at 15% of runtime with nothing broken. Only then does the real clock start: a 1.5-million-km-thick shell of darkness and missing gravity moves out at light speed, passes Mercury and Venus, and reaches you 8 min 19 s after the Sun vanished. Earth spends 5 seconds dark and unpulled, drifts 7.4 cm off course, and never gets its exact old orbit back.

**Why it should work (PLAYBOOK §10C).** One invisible rule (the speed of light, which gravity shares) instead of a disaster; a named place and a body-first line; a tight window with a return twist; exact computed numbers; a dated true fact at the end. The subversion (the master clock closes on nothing) is new to the template; none of the existing Shorts on this topic use the delay (backlog/whatif/TOPICS.md #4).

## Beat alignment table

| Our beat | Our time | Reference id + timestamp | Device borrowed | How we adapt it |
|---|---|---|---|---|
| S1 Premise card + pre-event clock | 0:00-0:07 | ELECTRONS 0:00-0:05 (title + countdown); OXYGEN 0:00-0:07 (baseline readout) | 7-9 word what-if title with one accent keyword; HUD counting down to the event; a baseline instrument reading in the subline | Title 8 words, "Sun" in amber. HUD counts 0:07.000 to zero; subline is a baseline reading of sunlight on the sand (1,000 W/m2) that will later drop to 0. Split screen: Sun panel on top, beach panel below |
| S2 Place you | 0:03.5-0:07 | ELECTRONS 0:05; NEUTRONS 0:05 | Second-person line naming a real, famous place, calm image | Copacabana beach at noon (bright, sunlit, the opposite of a dusk park) |
| S3 Flip (inverted) | 0:07-0:08 | ELECTRONS 0:08; NEUTRONS 0:08 | Clock hits zero, hard style change and hit, HUD flips to a "returns in" countdown | Only the top (Sun) panel changes: the disc vanishes on an impact hit. The beach panel does not change at all. That non-change is the hook, said in the 2-word line that follows |
| S4 Body first | 0:10-0:13 | OXYGEN 0:09 (ears pop); NEUTRONS 0:13 (POV hands) | First effect on the viewer's own body, harmless | The body effect is that there is none: your skin is still warm. POV hand over sand, still lit |
| Early loop close (subversion) | 0:12-0:13.5 | ELECTRONS 1:02-1:04 (return clock reaches zero, "BACK") | Return countdown completes, status flip | We pay the genre's master clock at 15% instead of 80%, with nothing broken, and open the real master loop: "darkness reaches you in" |
| S5 Rule, then short implication, then textless break | 0:17-0:27.5 | ELECTRONS 0:21-0:32 (rule line, 4-word line, 4 s no text) | Plain-science rule; a much shorter line that implies the consequence; 3-5 s without captions while the picture changes | Rule: light needs 8 min 19 s. Implication: gravity shares that delay (4 words). 5 s textless while the HUD flips to fast-forward and the dark shell leaves the Sun |
| Inverted time rule | 0:22 | NEUTRONS 0:08 / ELECTRONS 0:08 ("time slowed 11x") | A stated time multiplier so the on-screen clock adds up | Inverted: TIME SPED UP 30x for the 8-minute wait (484 s in 16 s), then TIME SLOWED 5x for the 5-second gap (5 s in 25 s). The clock always adds up |
| S6 Scale-outward ladder | 0:22-0:38 | ELECTRONS 0:32-0:40; OXYGEN 0:17-0:39 (stat rungs, meter carries gaps) | 3-5 rungs, one number each, HUD carries the long caption gap | Rungs travel outward in distance and toward you in time: Mercury dark (3 min 13 s), shell thickness (1.5 million km = 4 Moon distances), Venus dark (6 min 1 s), Earth countdown. Captions thin out; HUD rungs every ~3 s |
| Midpoint full-frame interrupt | 0:38.1 | ELECTRONS 0:40 (white-out); NEUTRONS 0:35 (white-out) | One full-frame blank that resets attention | Black-out instead of white-out: the whole frame, HUD included for 0.5 s, goes black when the shell reaches Earth |
| Delta readout + meter swap | 0:41-0:49 | OXYGEN 0:08 (pressure delta), 0:28 and 0:39 (meter swaps) | Baseline reading shown again as a delta; swap the HUD meter when captions space out | Sunlight subline drops 1,000 to 0 W/m2; at 0:49 it swaps to a climbing "OFF ORBIT BY" counter |
| S7 Planet climb with live number | 0:49-1:03 | ELECTRONS 0:42-1:02 (EARTH IS NOW N MILES WIDE); NEUTRONS 0:43 | Wide space view, live climbing number in the HUD, terse captions | Earth leaves its dashed orbit line on a tangent; the counter climbs 1.4 to 7.4 cm |
| Return-to-you dip | 0:53-1:01 | PLAYBOOK §5 return-to-you dips (PI=3, NEUTRONS 0:13) | Drop from planet scale back to the viewer's body | "You don't feel a thing" (free fall: you and Earth drift together), then the drift measured against your palm |
| S8 Return + callback stamp | 1:03.1-1:07 | ELECTRONS 1:04-1:06; NEUTRONS 1:04-1:06 | "[X] BACK", reassuring line, "[place], N later" stamp | SUNLIGHT BACK; light sweeps back over the beach; COPACABANA, 8 MIN 24 S LATER |
| S9 Twist (damage stays) | 1:07-1:11 | NEUTRONS 1:09-1:10; ELECTRONS 1:09-1:10 | The undo does not undo it; one caption + one HUD equivalence | Gravity comes back but the missing 3 cm/s of inward pull is never repaid: orbit shifted up to 149 km, every year 0.00005 s longer. Pays off the gravity plant from 0:20.8 |
| S10 Black + bookend + true fact | 1:11-1:18 | all five Shorts, e.g. ELECTRONS 1:12-1:20 | ~2 s black, exact title repeat for the loop, one small-caps dated fact; CTA only in the post caption | Fact is the real 2017 measurement that gravity travels at light speed (GW170817) |

## Script

Layers: **TITLE** (centred serif card), **CAPTION** (lower-third italic serif, read by the voice), **HUD** (top-left: small-caps label / large mono clock with ms digits / small-caps subline), **PANEL** (labels inside the Sun panel or space view). Times are screen seconds. Story time T starts at 0 when the Sun vanishes (screen 0:07.0).

### Hook (first line + first visual)

- First visual (frame 0): 9:16 split screen. Top 40%: flat space panel, black with a few stars, the Sun as a bright amber disc with soft corona rings, label SUN · 149.6 MILLION KM. Bottom 60%: flat vector Copacabana at noon, white sand, turquoise sea, wave-pattern promenade, a green headland, umbrellas, a stick-figure YOU in the foreground casting a short hard shadow. HUD already counting.
- First line (VO + TITLE, 0:00.3): What if the **Sun** disappeared for 5 seconds?

### Beat S1, premise card + pre-event clock (0:00-0:07)

- 0:00.0 HUD: SUN DISAPPEARS IN / 0:07.000 counting down in real time / SUNLIGHT HERE: 1,000 W/M²
- 0:00.3 TITLE + VO: What if the Sun disappeared for 5 seconds?
- 0:03.5 CAPTION + VO (S2, place you): You're on Copacabana beach at noon.

### Beat S3, the flip that changes nothing (0:07-0:13.5)

- 0:07.0 HUD: SUN RETURNS IN / 0:05.000 counting down in real time / SUNLIGHT HERE: 1,000 W/M² (unchanged on purpose)
- 0:07.0 PANEL: the Sun disc is gone; an empty point remains, label SUN · GONE
- 0:08.0 CAPTION + VO: Nothing happens.
- 0:10.0 CAPTION + VO (S4, body): Your skin still feels warm.
- 0:12.0 HUD: SUN BACK / 0:00.000 / SUNLIGHT HERE: 1,000 W/M²
- 0:12.0 PANEL: the disc pops back, label SUN · BACK

### Beat S5, the rule and the gravity plant (0:13.5-0:27.5)

- 0:13.5 CAPTION + VO: Out there, the Sun is already back.
- 0:13.5 HUD: DARKNESS REACHES YOU IN / 8:12.500 counting in real time / SUNLIGHT HERE: 1,000 W/M²
- 0:17.0 CAPTION + VO: Its light takes 8 minutes 19 seconds to arrive.
- 0:20.8 CAPTION + VO: So does its gravity.
- 0:22.0 HUD subline: TIME SPED UP 30× (clock now races from 8:04.000)
- 0:22.0-0:27.5 no caption. Full-frame space view: a black ring, the missing 5 seconds of sunlight, peels off the Sun and expands across the inner orbits.

### Beat S6, the shadow travels outward (0:27.5-0:38.1)

- 0:27.8 CAPTION + VO: Mercury loses its sunlight first.
- 0:27.9 HUD subline: MERCURY: DARK AT 3 MIN 13 S
- 0:30.5 HUD subline: SHADOW: 1.5 MILLION KM THICK
- 0:33.5 HUD subline: VENUS: DARK AT 6 MIN 1 S
- 0:36.0 HUD subline: SUNLIGHT HERE: 1,000 W/M² (clock under 0:02, ms digits blur)

### Midpoint interrupt (0:38.1)

- 0:38.1 Full-frame black, HUD hidden for 0.5 s. Sound cuts to silence for 0.4 s.
- 0:38.6 HUD: SUNLIGHT RETURNS IN / 0:05.000 / TIME SLOWED 5×

### Beat S7, five dark seconds (0:38.6-1:03.1)

- 0:40.0 CAPTION + VO: The beach goes black at noon.
- 0:41.0 HUD subline: SUNLIGHT HERE: 0 W/M²
- 0:44.5 CAPTION + VO: Every solar panel drops to zero.
- 0:49.0 CAPTION + VO: Earth stops curving and flies straight.
- 0:49.0 HUD subline: OFF ORBIT BY 1.4 CM (climbs every frame)
- 0:53.0 CAPTION + VO (return to you): You don't feel a thing.
- 0:57.0 CAPTION + VO: It slips a palm's width off course.
- 1:03.1 HUD subline reaches OFF ORBIT BY 7.4 CM as the clock hits 0:00.000

### Beat S8, return and callback (1:03.1-1:07)

- 1:03.1 HUD: SUNLIGHT BACK / COPACABANA, 8 MIN 24 S LATER
- 1:03.5 CAPTION + VO (false resolution): Light and gravity return. All looks normal.

### Beat S9, twist (1:07-1:11)

- 1:07.0 CAPTION + VO: But Earth's orbit stays bent.
- 1:07.5 HUD subline: ORBIT SHIFTED UP TO 149 KM
- 1:09.3 HUD subline: EVERY YEAR NOW 0.00005 S LONGER

### Beat S10, black + bookend + true fact (1:11-1:18)

- 1:11.0-1:13.0 black, no text, music tail only
- 1:13.0 TITLE (silent, exact repeat, "Sun" in amber): What if the Sun disappeared for 5 seconds?
- 1:14.0 END FACT (small caps, silent, held to 1:18): IN 2017, LIGHT AND GRAVITY WAVES FROM A NEUTRON-STAR CRASH 130 MILLION LIGHT-YEARS AWAY ARRIVED 1.7 SECONDS APART

### Post caption (not on screen)

The Sun goes out for five seconds and the beach stays bright. Its light is still in transit. So is its gravity. Eight minutes later a shadow one and a half million kilometres thick rolls over Earth, and for five seconds nothing is pulling us. Where would you want to be standing when the shadow passed? #whatif #space #physics #sun

## Shot list

Kit vocabulary: core layer types (`rect`, `circle`, `text`, `svg`, `particles`, `component`), callouts (`title`, `lowerThird`, `label`, `stat`), transitions (`cut`, `fade`, `dipBlack`, `whip`, `glitch`), camera presets (`pushIn`, `pullOut`, `panUp`, `panDown`, `drift`) plus `shake`, scene `grade`. Existing components: `explainer/You`, `explainer/Stat`, `explainer/Tag`, `explainer/ScaleBar`. Components marked NEW must be built for this lane (they are also what the other whatif Shorts need): `whatif/HUD`, `whatif/SolarMap`, `whatif/BeachNoon`, `whatif/Starfield`. SFX cues are from `studio/public/sfx/`; `beach_ambience` is NEW (needs a CC0 loop).

| # | t_start | t_end | Shot type | Visual (kit vocabulary) | Camera move | SFX |
|---|---|---|---|---|---|---|
| 1 | 0:00.0 | 0:07.0 | Split screen, title card | Top 40%: NEW `whatif/SolarMap` close on the Sun (amber `circle` + 3 corona rings, `particles` starfield, `label` "SUN · 149.6 MILLION KM"). Bottom 60%: NEW `whatif/BeachNoon` (sand, sea gradient, wave-pattern promenade `svg`, headland, umbrellas) with `explainer/You` pose stand, short hard shadow. `title` callout centre with "Sun" in amber. NEW `whatif/HUD` top-left counting | Slow `pushIn` on bottom panel (amount 0.3) | beach_ambience (NEW) low; `tick` each whole second from 0:04 |
| 2 | 0:07.0 | 0:12.0 | Split screen, event | Top: Sun disc scales to 0 in 2 frames, corona rings fade, empty point marker. Bottom: identical, no change; `explainer/You` pose shrug at 0:08 | `shake` on top panel only at 0:07 (amplitude 10, 0.3 s); bottom static | `impact` at 0:07.0, then beach_ambience continues unbroken |
| 3 | 0:10.0 | 0:12.0 | Insert, POV | Flat POV hand (NEW `svg`, skin tone) held over sunlit sand, warm `grade` tint, heat shimmer `particles` | `drift` | beach_ambience |
| 4 | 0:12.0 | 0:22.0 | Split screen | Top: Sun disc pops back (`pop` enter), `label` "SUN · BACK". Bottom: unchanged beach | Top `pullOut` from 0:13.5 to reveal Mercury and Venus orbit rings | `pop` at 0:12.0; `clock_ticking` from 0:13.5 |
| 5 | 0:22.0 | 0:38.1 | Full-frame space diagram | `whip` up to full-frame `whatif/SolarMap`: Sun, dashed orbit rings for Mercury, Venus, Earth, flat planet dots, a black annulus (5 light-seconds thick at diagram scale, exaggerated, with `label` "5 SECONDS OF MISSING SUNLIGHT") expanding at constant speed. Each planet dot turns grey as the ring crosses it (Mercury 0:27.9, Venus 0:33.5). `explainer/ScaleBar` beside the ring at 0:30.5 labelled "1.5 MILLION KM" with 4 small Moon-distance ticks | Continuous `pullOut` so Earth's orbit enters frame by 0:33; at 0:36 `pushIn` on the Earth dot | `whoosh_long` at 0:22.0; `riser` from 0:33.5 to 0:38.0; `ding` (soft) at 0:27.9 and 0:33.5 |
| 6 | 0:38.1 | 0:38.6 | Full-frame interrupt | Pure black `rect`, HUD hidden | none | hard silence 0.4 s, then `drone` starts |
| 7 | 0:38.6 | 0:49.0 | Wide, beach at night-at-noon | `whatif/BeachNoon` with `grade` brightness 0.08, tint deep blue; NEW `whatif/Starfield` brightest stars only; city windows along the promenade lit as small amber `rect`s; `explainer/You` pose panic silhouette. At 0:44.5 cut to rooftop with dark solar-panel grid (`rect` array) and an `explainer/Stat` meter dropping to 0 | `drift` (slow pan left); `cut` at 0:44.5 | `drone`; `click` at 0:44.5 as the meter hits 0 |
| 8 | 0:49.0 | 0:53.0 | Full-frame space diagram, close | `whatif/SolarMap` close on Earth: dashed orbit arc curving away, Earth dot continuing on a straight tangent `svg` line, small Moon dot alongside, `label` "NO PULL" | Slow `pushIn` | `drone`; `whoosh` soft at 0:49 |
| 9 | 0:53.0 | 0:57.0 | Medium, you | Dark beach, `explainer/You` pose stand, calm, stars behind; Earth and you drawn falling together as a tiny inset `Tag` "YOU DRIFT WITH IT" | none (hold still) | `heartbeat_slow` |
| 10 | 0:57.0 | 1:03.1 | Insert, scale comparison | Flat palm silhouette (`svg`) next to an `explainer/ScaleBar` growing 0 to 7.4 cm in sync with the HUD counter; dashed "old orbit" line and solid "Earth" line separating by exactly that bar | Slow `pushIn` | `tick` per 1 cm crossed |
| 11 | 1:03.1 | 1:07.0 | Wide, return | Light sweeps left to right over the beach (`grade` brightness 0.08 back to 1 in 0.6 s, sand and sea colours return), `explainer/You` pose wave; city windows fade out | `pullOut` (amount 0.4) | `whoosh` at 1:03.1, beach_ambience back |
| 12 | 1:07.0 | 1:11.0 | Full-frame orbit diagram | `whatif/SolarMap` whole Earth orbit: old orbit dashed white, new orbit solid amber, offset exaggerated with `label` "UP TO 149 KM"; year ring tick `Tag` "+0.00005 S" | Slow `pullOut` | `stinger` at 1:07.0 |
| 13 | 1:11.0 | 1:13.0 | Black | Black `rect` | none | music tail, then silence |
| 14 | 1:13.0 | 1:18.0 | End card | `title` callout, exact repeat, "Sun" amber; small-caps fact `text` below, fades in at 1:14.0; last frame matches frame 0's title for the loop | none | none |

## Fact file (every number on screen)

- Sun-Earth mean distance 149.6 million km (1 AU = 149,597,870.7 km, IAU 2012); light time 499.0 s = 8 min 19 s.
- Light time from the Sun at mean distance: Mercury 0.387 AU, 193 s = 3 min 13 s; Venus 0.723 AU, 361 s = 6 min 1 s. Mercury's real value swings 2.6-3.8 min with its eccentric orbit; we show the mean.
- Shadow thickness: 5 light-seconds = 1,498,962 km, about 3.9 Earth-Moon distances (384,400 km).
- Gravity changes propagate at the speed of light: GW170817 (17 Aug 2017), LIGO/Virgo plus Fermi GBM, gamma rays arrived about 1.7 s after the merger signal from about 40 Mpc (about 130 million light-years); Abbott et al. 2017, ApJL 848 L13.
- Clear-sky noon sunlight at the surface: about 1,000 W/m² (the standard test value for solar panels).
- Earth's orbital speed 29.78 km/s, so 149 km in 5 s. Sun's pull on Earth 0.00593 m/s². With no pull for 5 s, the sideways drift is ½·a·t² = 7.4 cm (checked by integration in `python3`, circular-orbit approximation). Adult palm width is about 7.5-9 cm.
- Free fall: you and Earth orbit together, so losing the Sun's pull is not felt as weight change (equivalence principle).
- After the gap, Earth carries about 3 cm/s of extra outward velocity, which adds an eccentricity of about 1e-6: perihelion or aphelion shifts by up to about 149 km, and the semi-major axis grows about 15 cm, so the year lengthens by about 47 µs (0.00005 s). Same integration. These shifts are permanent until other planets' pulls (far larger) blur them.
- Pacing timeline check (TIME SPED UP 30×): screen 0:22.0 is T = 15 s; Mercury at T = 193 s lands at 0:27.9; Venus at T = 361 s at 0:33.5; Earth at T = 499 s at 0:38.1. TIME SLOWED 5×: 5 s of gap fill 0:38.1-1:03.1; the callback stamp reads T = 504 s = 8 min 24 s.

## PLAYBOOK checklist

- One rule changed, universal, no IP: yes (the Sun, plus the true speed of light and gravity).
- Tracker on screen from hook to payoff: HUD clock 0:00-1:03, then the callback stamp.
- Master loop: "darkness reaches you in" opens 0:13.5, closes 1:03.1 (81%); the decoy genre loop ("sun returns in") opens 0:07 and closes 0:12.
- Ladder with one number per rung: Mercury, shell thickness, Venus, Earth, sunlight 0 W/m², drift 7.4 cm, orbit 149 km, year +0.00005 s.
- Dated precedent: GW170817 end card.
- Reversal in last 20%: orbit stays bent (T1, built from the 0:20.8 gravity plant).
- Ending calls back the place: COPACABANA, 8 MIN 24 S LATER.
- The where-would-you-stand prompt lives only in the post text.
- Title 8 words, held 0:00-0:07; event at 0:07 (9%); place line 0:03.5 and body line 0:10 both before 25%; rule line, 4-word implication, 5 s textless break; full-frame interrupt at 49%; return 81%, twist 86%, black + title + fact in the last 9%.
