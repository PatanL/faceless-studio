---
episode: whatif-light-walking-speed
niche: whatif
format: short 9:16 (1080x1920), caption-led, optional light TTS read of the captions only
template: countdown-HUD ("N seconds" template, R3 report rec. 1), house HUD wording (see HUD state table)
working_title: "What if light walked for 5 seconds?"
target_runtime_s: 78
target_words_per_min: 55   # 71 caption words / 78 s = 54.6 wpm (PLAYBOOK §9 Shorts: 56 median, 43-65). Title, HUD and end card are on screen only, never read.
captions: 11 (mean 6.5 words, max 8)
slow_motion_factor: 11   # event 5.0 s fills screen 0:07.0-1:02.0 = 55 s; after the return, time runs at 1x
references:
  - id: "7693494009494342945"
    short: ELECTRONS (@man_ia_c)
    url: https://www.tiktok.com/@man_ia_c/video/7693494009494342945
    views: 18200000
    outlier_score: 29.13
    why_chosen: >
      Cleanest countdown-HUD Short in the corpus (PLAYBOOK §13 #1). We borrow its beat skeleton and proportions:
      pre-event clock, flip with an 11x return clock, wonder then the viewer's own hands in POV, rule -> short
      implication -> textless break, a 3 s cadence peak on the ladder, midpoint white-out, cosmic climb carried by
      a live HUD line, return + reassuring line, a twist caused by the return itself with one HUD equivalence,
      black + title repeat + fact.
  - id: "7693305573487562016"
    short: OXYGEN (@man_ia_c)
    url: https://www.tiktok.com/@man_ia_c/video/7693305573487562016
    views: 13400000
    outlier_score: 21.45
    why_chosen: >
      Closest twist mechanics: a baseline reading on the pre-event HUD that becomes a delta at the flip, a city
      rung stated with an absolute "every", a 4 s setup/payoff pair inside the ladder, a by-product planted with
      its own live rising meter, and that by-product reacting the moment the missing thing returns, closed on screen.
  - id: "7696143265405488416"
    short: PI=3 (@man_ia_c)
    url: https://www.tiktok.com/@man_ia_c/video/7696143265405488416
    views: 3900000
    outlier_score: 6.24
    why_chosen: >
      Closest premise: one physical constant changed for 5 s. Borrowed: one ratio drives every number on screen
      (here c / 1.4 m/s), exact odd numbers in the HUD, ordinary props seeded in the calm scene that each pay off
      later, a hard cut to the sky for the scale jump, and a real "this nearly happened" end fact.
playbook: research/corpus/whatif/PLAYBOOK.md §1A (S1-S10), §5 (scale outward + closing distance + return-to-you dip), §6 T1/T2, §9 Shorts pacing, §12 checklist
evidence_topic_demand: "Worlds In Motion 'What If Light Was Really Slow?' 4.26M; Airplane Mode speed-of-light 36.4M (149 s); The Action Lab 'Slowing the Speed of Light to 2 m/s' 3.01M; @man_ia_c pi=3 constant change 3.9M (6.24x). Slow-light videos exist, so the differentiators are the 5-second HUD template, the black city with a growing bubble of light, and the car that shows up after it passed you."
post_caption: >
  For 5 seconds, light moves at walking pace. Only light changes; your body, sound and chemistry work as normal.
  The city goes black. Your own hand shows up half a second late. A car passes a metre from you before you can
  see it, then appears driving backwards. Then light comes back, and five seconds of it arrive at once.
  Which would you watch first: your hand, your friend, or the car? And which constant should we slow down next?
post_description_fact: "Stopped light is real: Liu, Dutton, Behroozi & Hau, Nature 409, 490-493 (2001), halted a light pulse in ultracold sodium and released it. In 1999 the same Harvard lab slowed light to 17 m/s (61 km/h, 38 mph, city-traffic speed): Hau, Harris, Dutton & Behroozi, Nature 397, 594-598."
---

# What if light walked for 5 seconds?

Original script. Structure, timing proportions and devices are borrowed from the three references above. No wording, characters, places or story are taken from them. ELECTRONS and PI=3 are set in a park and OXYGEN on a rooftop bar; ours is a Tokyo street crossing at night. The whole consequence chain is our own: a black city with a growing bubble of light, a hand that arrives late, sound beating light, a car that is seen only after it passed, signals stuck mid-air, and every lamp's piled-up light arriving at once.

## Premise rule (held for the whole video)

For 5 seconds the speed of light everywhere drops to 1.4 m/s, normal walking pace. Nothing else changes: sources shine as usual, sound travels at 343 m/s, atoms, nerves and chemistry work as normal (stated in the post caption; a genre convention). Every number on screen follows from one ratio: 299,792,458 / 1.4 = 214,137,470.

What you see follows from two facts:

1. **Light already in flight keeps its spacing but moves 214,137,470x slower**, so the light it delivers drops by the same factor. Anything whose new light has not reached you yet looks black. That is the whole city at the flip.
2. **New light leaves every source at the usual power**, packed 214,137,470x denser, so it is normally bright when it arrives, but late by distance / 1.4 m/s. What you can see is a **bubble of light growing from your eyes at 1.4 m/s** (radius 7.0 m at the end). Inside it, everything is lit and running late. Outside it, black.

## Fact file (every on-screen number, with working)

Screen time t (seconds); event time tau = (t - 7.0) / 11 for 7.0 <= t <= 62.0. Bubble radius R = 1.4 x tau = 0.12727 x (t - 7.0) m.

- **Walking pace** 1.4 m/s (standard gait-study figure). c = 299,792,458 m/s (exact). Ratio 214,137,470 (exact to the integer).
- **Darkness outside the bubble.** In-flight light delivers 1/214,137,470 of normal: a lit night street (~10-20 lux) falls to ~1e-7 lux; even an LED billboard (~1,000 cd/m2) falls to ~5e-6 cd/m2, which an eye that was looking at a lit street a second ago cannot see. Physically this is black. We draw the far world as a 6%-opacity ghost so viewers can keep track of the layout; this is an artistic allowance, noted here and never claimed on screen.
- **Bubble on the ground.** Eye height 1.6 m, so the ground under you lights only once R > 1.6 m (tau 1.14 s, screen 0:19.6). Lit ground radius = sqrt(R^2 - 1.6^2). Figures light up when their distance from your eyes is <= R and then play forward from their pose at the flip, delayed by distance / 1.4.
- **Your body.** Forearm near the elbow ~0.3 m from your eyes: lit at 0:09.4. Hand at arm's length 0.7 m: dark for 0.5 s, lit at 0:12.5. After that it is always 0.5 s behind where you feel it (HUD HAND: 0.5 S LATE).
- **Sound.** 343 m/s at 20 C = 245.0 x 1.4 m/s (HUD SOUND: 245x FASTER).
- **Shutter click (plant).** The tourist 4.0 m away takes a flash photo at tau 0.30 (0:10.3). The click reaches you 4 / 343 = 0.012 s later, i.e. at once. The flash's light needs 4.0 / 1.4 = 2.857 s, so it arrives at tau 3.157 = 0:41.7. The flash shows 2.86 s after it fired (HUD FLASH: 2.86 S LATE).
- **Friend** 3.0 m away (same eye height): lit at tau 2.143 = 0:30.6, frozen in her pose at the flip (arm halfway up a wave started at 0:06.0), then waving 2.14 s late. **Tourist** 4.0 m: lit at 0:38.4.
- **The car.** 50 km/h = 13.9 m/s = 9.9x the new light speed (HUD CAR: 10x FASTER THAN LIGHT). It passes along the near lane with its side 1.0 m from your eyes, closest at tau_c = 1.773 (0:26.5). It moved through the lit part of the road, but you could not see it: the road you see there is 0.7 s old, from before the car arrived. Light it emitted at time tau_c + u reaches you at tau_c + u + sqrt((13.9 u)^2 + 1.0^2) / 1.4. The earliest arrival is at u = -0.0073 s, tau 2.483 = **0:34.3, 0.71 s after it passed you**. From then on each instant brings light from two emission times, so you see **two copies**: one shows earlier and earlier positions (it moves back the way the car came, about 1.5 m/s, nose still forward: it looks like it is reversing) and one moves on in the car's direction at about 1.3 m/s. Positions from the closest point (m): 0:35.0 -0.54 / +0.32; 0:38.0 -1.23 / +0.94; 0:41.7 -1.87 / +1.48; 0:44.0 -2.24 / +1.79. This is the light version of what a faster-than-sound jet does to its own sound.
- **Radio is light.** Phone, Wi-Fi and GPS signals also travel at 1.4 m/s; in 5 s none gets more than 7 m. A cell mast 300 m away is 214 s away. GPS satellites at 20,200 km: 20,200,000 / 1.4 = 1.44e7 s = 167 days (HUD GPS ETA: 167 DAYS).
- **Sky** (travel time at 1.4 m/s; HUD only, so no caption makes a hypothetical claim). Moon 384,400 km: 2.75e8 s = 8.70 years. Sun 149,597,870.7 km: 1.07e11 s = 3,386 years. Proxima Centauri 4.2465 light-years: 4.2465 x 214,137,470 = 909 million years. Moonlight and starlight already in flight are 214,137,470x dimmer too, so the sky is black from the flip on. The Moon is full and rising in the east (a full Moon rises around sunset, opposite the Sun), so it is up on an early evening.
- **Pile-up (plant).** Every source keeps emitting; its new light piles up within 1.4 x tau of it, 214,137,470x denser than normal (HUD LIGHT PILED UP: x.xx S = tau, reaching 5.00 S at the return).
- **Return / twist.** At 1:02.0 light is back at c. All the light still on its way to you speeds up 214,137,470x. Light that had piled up in up to 7.0 m now crosses that distance in 7 / c = 23 ns, so each source delivers its backlog as a pulse at **214,137,470x normal brightness** lasting at most 23 ns. For sources farther than 7 m the backlog is all 5 s. For things inside the bubble it is only their last r / 1.4 s (friend 2.14 s, hand 0.5 s). Total energy is just the normal light of those seconds; only the delivery is compressed. Your retina adds it all up at once, like a long-exposure photo: cars become streaks, the crowd becomes smears, and the signal shows red and green together. The friend's arm becomes a short fan of 5 poses, not 12. A bright flash leaves an afterimage for a few seconds. We state the brightness ratio and nothing about injury.
- **Signal.** The pedestrian signal across the road is about 15 m away, outside the 7 m bubble for the whole event. It turns green at tau 4.0 (0:51.0), unseen. That change shows up only in the afterimage and in the bookend.
- **End fact.** Liu, Dutton, Behroozi & Hau, "Observation of coherent optical information storage in an atomic medium using halted light pulses", Nature 409, 490-493 (25 Jan 2001): a light pulse was brought to a stop in a cloud of ultracold sodium atoms and later released. The 1999 result (17 m/s = 61 km/h = 38 mph, city-traffic speed, not cycling speed; Nature 397, 594-598) goes in the post description.
- **Removed on purpose.** The old Doppler colour beat (red signal reads green) is gone. Its source was outside the bubble, and its relativistic formula did not fit a premise where cars outrun light. The sound and car rungs replace it as the "different kind of effect".

## Beat alignment table

| our beat | our t | reference id + t | device borrowed | how we adapt it |
|---|---|---|---|---|
| S1 premise card + pre-event clock | 0:00-0:07 | ELECTRONS 0:00 (title + countdown); OXYGEN 0:00-0:07 (baseline readout 14.7 PSI) | 7-word title, accent keyword + icon, ms countdown, a baseline subline that becomes a delta | "walked" in amber; LIGHT SLOWS IN 0:07.000; subline 299,792,458 M/S, which flips to 1.4 M/S at the event |
| S2 place you + seeded props | 0:04.5 | ELECTRONS 0:05 (you + named place); PI=3 0:05-0:07 (props that each break later) | second-person line naming a real place; busy calm scene with props | Shibuya Crossing at night: cars streaming past, a friend starting to wave, a tourist raising a phone, the red signal, a full Moon. Each gets its own beat |
| S3 flip | 0:07 | ELECTRONS 0:08 (hard style flip + return clock + 11x); OXYGEN 0:08 (silent tell + delta) | hard change + hit; HUD flips to a return countdown with a slow-motion factor | Everything goes black except a small glow around your head; HUD 1.4 M/S = WALKING PACE, then TIME SLOWED 11x |
| S4a wonder | 0:08 | ELECTRONS 0:09 (first effect is visual and harmless) | a sense-level effect that explains the new look | "The whole city just went black." |
| S4b body first, POV | 0:10.8-0:19.5 | ELECTRONS 0:15 (the viewer's own hands, POV) | effect lands on your own body, shown in first person | POV: light crawls up your arm and your hand appears at 0:12.5, then always 0.5 s behind where you feel it; exact number in the HUD only |
| S5 rule -> implication -> textless break | 0:19.5-0:30.6 | ELECTRONS 0:21 / 0:25 / 0:28 (rule, 4-word implication, ~4 s without text) | plain rule, a shorter line the viewer completes, then a break while the image changes | "Sound now travels faster than light." / "So does every car." / textless: a car roars past 1 m away through the lit, empty road; wind hits you, nothing is visible |
| S6 rung: person | 0:30.6-0:31 | ELECTRONS 0:35 (person rung); PI=3 0:41 (back to a person) | the ladder moves to another person, exact delay in the HUD | The bubble reaches your friend; she lights up frozen mid-wave |
| S6 rung: vehicle (danger), cadence peak | 0:34.3 | ELECTRONS 0:32-0:35 (captions 3 s apart at the ladder climax); OXYGEN 0:22 / 0:26 (4 s setup -> payoff) | two rungs 3.5 s apart; the 0:26.5 roar is paid off by the image | "Then the car appears, driving backwards." Two copies slide apart in front of you |
| S6 -> midpoint white-out | 0:41.7 | ELECTRONS 0:40 (white-out); PI=3 0:05 (a seeded prop pays off) | full white frame resets attention; a loop planted early closes | The shutter click heard at 0:10.3 becomes the flash that finally reaches your eyes, 31 s later |
| S7a city rung | 0:44 | OXYGEN 0:17 (city rung, absolute "every") | "every [system]" line at city scale | "Every phone signal is stuck mid-air." on the tourist's phone; HUD GPS ETA: 167 DAYS |
| S7b cosmic climb | 0:47-0:54 | ELECTRONS 0:42-0:56 (one live HUD line climbs, captions stop); PI=3 0:34 (hard move to the sky) | jump to the sky; one HUD line swapping and climbing on a log scale; no captions | Black sky with a ghost Moon; MOONLIGHT ETA 8.7 YEARS -> SUNLIGHT 3,386 -> STARLIGHT spins to 909,000,000 YEARS |
| S7c plant + return-to-you dip | 0:54-1:02 | OXYGEN 0:28 (by-product planted with a live rising meter); PI=3 0:56 (big scale brought back to this place) | the by-product is named in a caption with its own meter; the camera comes back down to you | "But every lamp keeps pouring out light." MEANWHILE inset; HUD LIGHT PILED UP 4.27 -> 5.00 S; your bubble reaches 7 m |
| S8 return + reassuring line | 1:02.0-1:02.5 | ELECTRONS 1:02-1:05 (zero, BACK, reassuring line) | clock zero, status flip, a calm line | LIGHT BACK; "Light is back. All five seconds of it." (the reassurance and the turn in one line) |
| S9 twist | 1:02.0-1:08.0 | ELECTRONS 1:09-1:10 (the return causes the second event + one HUD equivalence); OXYGEN 0:56-1:02 (planted by-product reacts with the returning element, closed on screen) | one twist, one caption + one HUD number, closed on screen | Hard flash, then a long-exposure afterimage of the last 5 s; HUD 214,137,470x BRIGHTER; "Everything you missed hits your eyes at once." |
| S9b bookend | 1:08.0-1:09.5 | ELECTRONS 1:06 (callback to the opening place) | return to the opening frame | Frame 1's framing again; the signal is now green and the crowd surges. No text |
| S10 black + title + real fact | 1:09.5-1:18 | ELECTRONS 1:12-1:20; PI=3 1:12-1:20 (real "it happened" fact) | black, exact title repeat for the loop, small-caps dated fact | Harvard 2001: a light pulse stopped, then let go. CTA only in the post caption |

## The script

Timestamps are screen time (m:ss.s). CAPTION = italic serif lower third (also the VO line if VO is used; VO reads captions only). HUD = top-left block with three fixed slots, L (small-caps label), T (mono clock with ms digits) and S (one small-caps subline that is replaced, never stacked); see the HUD state table. The frame always shows what "you" see: lit if its light has reached your eyes, a dark ghost otherwise. The only exceptions are explicitly boxed (the MEANWHILE inset) or sound (ripple glyphs mark where a sound comes from in the dark).

### Hook

- **First line (title card, 0:00, not read):** What if light **walked** for 5 seconds? ("walked" in amber; icon: a small glowing dot with two footprints)
- **First visual (frame 1, also the cover):** Shibuya Crossing at night, flat 2D vector, high three-quarter view from just behind and above you on the kerb. Everything is moving: two lanes of cars stream past right in front of you, the crowd mills and walks along the far kerb, giant screens scroll, neon flickers, the red pedestrian signal's wait bar ticks down, the tourist on your right lifts a phone, a full Moon rises over the towers. Nothing is frozen before 0:07. HUD already ticking: LIGHT SLOWS IN 0:07.000 / 299,792,458 M/S.

### S1 Premise card + pre-event clock (0:00-0:07.0)

- 0:00.0 TITLE (fades 4.1-4.5): What if light walked for 5 seconds?
- 0:00.0 HUD: LIGHT SLOWS IN 0:07.000 (counts down) / 299,792,458 M/S
- 0:03.0 the tourist raises her phone. SFX: tick under the HUD, city bed, cars passing.

### S2 Place you (0:04.5-0:07.0)

- 0:04.5 CAPTION 1: You're at Shibuya Crossing, waiting on red.
- 0:06.0 your friend, 3 m to your left, turns and starts to wave; her arm is halfway up at 0:07.0.

### S3 Flip (0:07.0)

- 0:07.0 HUD: LIGHT RETURNS IN 0:05.000 / 1.4 M/S = WALKING PACE
- Visual: hard cut, same framing, pushed in on you. The whole world drops to black (a 6% ghost of the layout remains). Only a small sphere of light around your head is lit: your face, your hair. The city's sound carries on as normal. SFX: impact, then the city bed continues.

### S4 Wonder, then your body (0:08.0-0:19.5)

- 0:08.0 CAPTION 2: The whole city just went black.
- 0:09.5 HUD S: TIME SLOWED 11x
- 0:10.3 (no text) a camera shutter clicks in the dark to your right; a small ripple glyph marks where it came from. Nothing lights up. Plant (sound only, no picture).
- 0:10.8 POV cut: your arm held out into the black. The sleeve near you is lit; the light edge crawls toward your fingers.
- 0:10.8 CAPTION 3: Even your own hand is dark, until...
- 0:12.5 your hand lights up.
- 0:13.0 HUD S: HAND: 0.5 S LATE. You wiggle your fingers: a dotted outline (where you feel your hand) moves at once; the lit hand you see stays still until 0:18.5, then follows.

### S5 Rule, implication, textless break (0:19.5-0:30.6)

- 0:19.5 Wide again. Your bubble now reaches the kerb under your feet. Sound ripples come from all over the dark: the crossing chime, voices.
- 0:19.5 CAPTION 4: Sound now travels faster than light.
- 0:19.5 HUD S: SOUND: 245x FASTER
- 0:23.0 CAPTION 5: So does every car.
- 0:24.0 HUD S: CAR: 10x FASTER THAN LIGHT
- 0:25.0-0:30.6 (no captions) The lit patch of road in front of you is empty. At 0:26.5 an engine roar and horn sweep left to right a metre in front of you; the wind whips your jacket and hair and a paper cup tumbles inside the bubble. You still see an empty road. SFX: whoosh_long + boom (low), horn.

### S6 Ladder: a person, a car, a flash (0:30.6-0:44.0)

- 0:30.6 the bubble reaches your friend; she lights up frozen mid-wave, then her wave carries on, slow and late.
- 0:31.0 CAPTION 6: Your friend lights up, still mid-wave.
- 0:31.0 HUD S: FRIEND: 2.14 S LATE
- 0:34.3 the car pops into view a metre in front of you, then splits into two copies that slide apart: one creeps on, the other reverses back the way it came.
- 0:34.5 CAPTION 7: Then the car appears, driving backwards.
- 0:38.4 the bubble passes the tourist; she lights up, phone raised.
- 0:41.7 WHITE-OUT: the flash from 0:10.3 finally reaches your eyes. Full white for 1.0 s; the HUD switches to dark ink so it stays readable. SFX: stinger + whoosh.
- 0:41.7 HUD S: FLASH: 2.86 S LATE
- 0:42.7-0:44.0 the white fades back to the crossing; the tourist lowers her phone.

### S7 City, then sky, then back to you (0:44.0-1:02.0)

- 0:44.0 Insert: the tourist's phone screen (inside your bubble, so lit): no signal bars, a spinner.
- 0:44.0 CAPTION 8: Every phone signal is stuck mid-air.
- 0:44.0 HUD S: GPS ETA: 167 DAYS
- 0:47.0 Fast in-scene whip up to the sky: black, with a ghost full Moon over ghost towers and a few ghost stars.
- 0:47.5 HUD S: MOONLIGHT ETA: 8.7 YEARS
- 0:49.5 HUD S: SUNLIGHT ETA: 3,386 YEARS
- 0:51.0 HUD S: STARLIGHT ETA: ... YEARS (counter spins up, lands on 909,000,000 at 0:52.5)
- 0:53.0-0:54.0 Camera drops back down to the crossing.
- 0:54.0 CAPTION 9: But every lamp keeps pouring out light.
- 0:54.0 MEANWHILE inset (boxed, labelled): a neon sign in the dark with a thick, glowing halo of trapped light growing around it.
- 0:54.0 HUD S: LIGHT PILED UP: 4.27 S (live, = tau, reaches 5.00 S at 1:02.0)
- 0:57.5 Wide pull-out: your bubble, ~6 m across the kerb and road, the only light in a black city; its edge leaves the frame by 1:01. SFX: riser.
- 1:01.0 HUD return clock under 0:00.100.

### S8 Return (1:02.0)

- 1:02.0 HUD: LIGHT BACK / 0:00.000 (clock disappears at 1:02.6)
- 1:02.0 Visual: hard white flash (0.4 s). SFX: impact + stinger.
- 1:02.5 CAPTION 10: Light is back. All five seconds of it.

### S9 Twist (1:02.4-1:09.5)

- 1:02.4 the flash fades into an afterimage: a long-exposure picture of everything you missed. Cars are long light streaks across the road, the crowd is smeared, the signal glows red and green at once, your friend's arm is a fan of five poses, and the passing car is a double ghost. It fades slowly while the normal crossing comes up underneath.
- 1:03.0 HUD S: 214,137,470x BRIGHTER
- 1:05.5 CAPTION 11: Everything you missed hits your eyes at once.
- 1:08.0 the afterimage is gone: the same framing as frame 1, normal neon light, the signal now green, the crowd surging onto the crossing, your friend still waving. The HUD fades out (1:08.0-1:08.5). No text.

### S10 Black + bookend + real fact (1:09.5-1:18.0)

- 1:09.5 Black, 1.0 s. Music out; one tick.
- 1:10.5 END TITLE (exact repeat): What if light walked for 5 seconds?
- 1:11.5 END FACT (small caps, held to 1:18.0): HARVARD, 2001 · LENE HAU'S LAB STOPPED A PULSE OF LIGHT IN ULTRACOLD ATOMS, THEN LET IT GO.
- Post caption: see front matter (premise retold + "your hand, your friend, or the car?" + "which constant next?").

### Caption list for TTS / caption layers (11 lines, 71 words)

| # | in | out | text | words |
|---|---|---|---|---|
| 1 | 0:04.5 | 0:07.0 | You're at Shibuya Crossing, waiting on red. | 7 |
| 2 | 0:08.0 | 0:10.6 | The whole city just went black. | 6 |
| 3 | 0:10.8 | 0:14.0 | Even your own hand is dark, until... | 7 |
| 4 | 0:19.5 | 0:22.8 | Sound now travels faster than light. | 6 |
| 5 | 0:23.0 | 0:25.0 | So does every car. | 4 |
| 6 | 0:31.0 | 0:34.0 | Your friend lights up, still mid-wave. | 6 |
| 7 | 0:34.5 | 0:38.0 | Then the car appears, driving backwards. | 6 |
| 8 | 0:44.0 | 0:47.0 | Every phone signal is stuck mid-air. | 6 |
| 9 | 0:54.0 | 0:57.5 | But every lamp keeps pouring out light. | 7 |
| 10 | 1:02.5 | 1:05.2 | Light is back. All five seconds of it. | 8 |
| 11 | 1:05.5 | 1:08.0 | Everything you missed hits your eyes at once. | 8 |

### Pacing check against PLAYBOOK §9 / §12 (Shorts)

- Title 7 words, held 4.5 s (clears before caption 1) over a running countdown; event at 0:07.0 (9%).
- 11 captions, 71 words, mean 6.5, max 8: **54.6 wpm** over the runtime (corpus 43-65, median 56).
- Caption gaps (s): 3.5, 2.8, 8.7, 3.5, 8.0, 3.5, 9.5, 10.0, 8.5, 3.0. Median 5.75 s (range 4-6). The long gaps are the POV hand demo (HUD + hand reveal + lag), the textless car pass, and the sky climb, where the HUD number moves. Cadence peak on the ladder: 0:31.0 -> 0:34.5 (3.5 s), then the white-out.
- All on-screen text about 166 words (title x2 14, captions 71, HUD labels 8, HUD sublines ~52, MEANWHILE 1, ring tag, end fact 16) = **~128 wpm** (corpus 103-131).
- Numbers on screen: about 22 (two clocks, 299,792,458, 1.4, 11, 0.5, 245, 10, 2.14, 2.86, 167, 8.7, 3,386, 909,000,000, the live pile-up and ring values, 214,137,470, "5" in the title, "five" in caption 10, 2001) = **~17/min** (corpus 7-18). Only 1 of 11 captions carries a number ("five"); every exact figure lives in the HUD.
- Second person in 4 of 11 captions (36%: 1, 3, 6, 11). That is above the Shorts range (7-18%); this premise is about what you see, so the place line, the body line, the friend and the twist need it. No more were added.
- Pivot words: "until" (3), "So" (5), "Then" (7), "But" (9).
- Something new on screen about every 3 s (captions, 15 HUD swaps, the hand, friend, car and tourist reveals, the white-out, the whip, the inset, the return flash).
- Loops: the return clock 0:07-1:02 (70.5% of runtime, closes at 79.5%); the bubble radius (0:07-1:02); the shutter click -> flash (0:10.3-0:41.7); the car's roar -> image (0:26.5-0:34.3); the friend's wave (0:06-0:30.6); the piled-up light (0:54-1:02, paid at 1:05.5); the series question in the post caption (open on purpose).
- Return 79.5%, twist caption 84%, black + title + fact in the last 11%.
- Runtime 78 s, above TikTok Creator Rewards' 60 s floor; do not trim below ~62 s.

## HUD state table

Component whatif/Hud at (70, 250) top-left, inside SAFE_AREA, depth 0 (it never moves with the camera), z above everything except the white flashes. It takes a global t0 per scene, so the clock is continuous across cuts. Slots: **L** label (small caps), **T** clock (JetBrains Mono, tabular-nums, ms digits), **S** one subline (small caps, 2-5 words, replaces the previous one). `invert` windows switch to dark ink during white frames.

| from | to | L | T | S |
|---|---|---|---|---|
| 0:00.0 | 0:07.0 | LIGHT SLOWS IN | 0:07.000 -> 0:00.000 | 299,792,458 M/S |
| 0:07.0 | 0:09.5 | LIGHT RETURNS IN | 0:05.000 -> (runs to 1:02.0, = 5 - tau) | 1.4 M/S = WALKING PACE |
| 0:09.5 | 0:13.0 | " | " | TIME SLOWED 11× |
| 0:13.0 | 0:19.5 | " | " | HAND: 0.5 S LATE |
| 0:19.5 | 0:24.0 | " | " | SOUND: 245× FASTER |
| 0:24.0 | 0:31.0 | " | " | CAR: 10× FASTER THAN LIGHT |
| 0:31.0 | 0:41.7 | " | " | FRIEND: 2.14 S LATE |
| 0:41.7 | 0:44.0 | " (invert 41.7-42.9) | " | FLASH: 2.86 S LATE |
| 0:44.0 | 0:47.5 | " | " | GPS ETA: 167 DAYS |
| 0:47.5 | 0:49.5 | " | " | MOONLIGHT ETA: 8.7 YEARS |
| 0:49.5 | 0:51.0 | " | " | SUNLIGHT ETA: 3,386 YEARS |
| 0:51.0 | 0:54.0 | " | " | STARLIGHT ETA: {v} YEARS (v 3,386 -> 909,000,000 log-ease by 0:52.5, then held) |
| 0:54.0 | 1:02.0 | " | " | LIGHT PILED UP: {v} S (v = (t-7)/11, 2 decimals) |
| 1:02.0 | 1:08.0 | LIGHT BACK (invert 62.0-62.4) | 0:00.000 until 1:02.6, then hidden | (none until 1:03.0) 214,137,470× BRIGHTER |
| 1:08.0 | 1:08.5 | fade out | | |

In-world (not HUD): the bubble edge carries a small tag with R in metres ("3.4 M"), from 0:19.5 to 1:02.0, drawn by whatif/CrossingSet.

## Kit vocabulary and build notes

- **Projection (one for the whole street):** high three-quarter view from behind and above you. 100 px per metre across the frame; ground depth compressed by scaleY 0.55. You stand on the kerb with your feet at (540, 1180) and your head near y 1005, above the caption band (captions sit at y 1400). Friend: 3.0 m left (x 240). Tourist: 4.0 m right (x 940). Near lane: the car's side 1.0 m in front of you (its ground centreline 1.85 m ahead, y ~1078; you are drawn in front of it). The far kerb, crowd, signal (~15 m) and towers are in the upper half. The bubble is drawn as a soft sphere glow centred on your head (screen radius 100 x R px) plus the lit ground ellipse (rx = 100 x g, ry = 55 x g, g = sqrt(R^2 - 1.6^2)). At 7 m the bubble is wider than the frame by 1:01; that is intended.
- **No scene grade and no camera shake anywhere.** The darkness, ghosting, exposure and shakes are drawn inside whatif/CrossingSet (props), so the HUD and the captions (depth-0 layers) are never tinted or shaken. **Every scene boundary while the HUD is visible is a hard cut**; the whip to the sky and the drop back are in-scene camera keyframes (depth-0 layers do not move). White flashes are full-frame white rect layers below the HUD (the HUD inverts).
- **Shared whatif kit (also needed by the other whatif backlog scripts; names match whatif-friction-off-5-seconds):** whatif/Hud (slots L/T/S + live tracks + invert windows), whatif/SerifCaption (planned; the storyboard draws captions as whole-sentence text layers, core captions disabled), whatif/TitleCard (storyboard draws it as text + svg layers), whatif/EndCard (same). Fonts: Source Serif 4 italic and JetBrains Mono via @fontsource, installed on the Spark only, registered in waitForFonts.
- **Episode components:**
  - **whatif/CrossingSet** (the big one, ~400-600 LOC): road, zebra stripes, kerbs, tower silhouettes, neon blocks, giant screens, crowd of 15-25 explainer/You figures, cars, signal, friend, tourist, Moon, all drawn as world objects with positions in metres. Light model props: `clock {flipAt 7.0, returnAt 62.0, slowmo 11, c 1.4}`, `viewer {x, y, eyeH 1.6}`, `ghost 0.06`. Every object is drawn at its own delayed time: tau_obj = tau - r/1.4, lit only if tau_obj >= 0 (whole-figure granularity), otherwise drawn from the ghost copy. The car uses the two-branch image formula from the fact file. Other props: `exposure {from, to, samples}` for the afterimage (N copies at 1/N opacity, screen blend), `shake [{at, duration, amplitude}]`, `views` (wide, close, skyline).
  - **whatif/RadialSplit** (~120 LOC, generic, reusable): renders the same set twice (lit and ghost) and clips the lit copy by the ground ellipse + head sphere for radius track R. CrossingSet uses it internally.
  - **whatif/PovHand** (shared with whatif-you-100x-taller's planned POV hand): one flat SVG forearm + hand, drawn twice: a dotted "felt" copy that moves on time and a solid "seen" copy delayed by 0.5 event s (5.5 screen s). A light edge sweeps from the elbow (lit 0:09.4) to the fingertips (0:12.5).
  - **whatif/SkyBodies**: full Moon disc, stars, two satellite dots, at ghost opacity; can share the Starfield with whatif-sun-gone-5-seconds.
  - **whatif/Inset**: a boxed MEANWHILE card; here a neon sign with a growing dense halo (radius = 1.4 x tau in the inset's own scale).
  - **whatif/PhoneScreen**: small phone face with signal bars and a spinner (no text).
- **explainer/You edits** (kit, targeted): `armR` / `armL` [upper, fore] degree tracks (for the friend's half-raised wave and the delayed wave), `phone: true` (the tourist), `time` override (so CrossingSet can draw a figure at a delayed or frozen time, and the afterimage can draw 5 copies), and a `walk` pose whose stride follows `time` (the current `run` legs ignore idle, so a frozen stride is impossible).
- **Cheap equivalents:** the white-outs are rect layers with opacity keyframes; the sound ripples are an inline svg (three arcs) with opacity keyframes; the 0:47 whip is a 0.35 s camera keyframe on a tall scene.
- **Audio:** music documentary_pulse (0-7, low), tension_pulse (7-62), drone loop (7-62); SFX that exist: tick, click (shutter), whoosh_long + boom (car pass), stinger, whoosh, riser, impact, clock_ticking, ding (crossing chime). To synthesize on the Spark with ffmpeg: city_bed (filtered pink noise + far voices), car_horn (two detuned square tones, 0.4 s), afterimage_ring (4 kHz sine, fade). Until they exist, the storyboard uses drone / whoosh_long / ding as stand-ins (marked in notes).

## Shot list

| t_start | t_end | shot | visual (kit vocabulary) | camera | SFX |
|---|---|---|---|---|---|
| 0:00.0 | 0:04.5 | wide establishing, title over (cover) | whatif/CrossingSet wide, light normal: cars streaming in both lanes, crowd walking (You `walk`), screens scrolling, signal red with wait bar, tourist raises phone at 0:03, Moon rising; title layers (icon + "walked" amber) centred in the upper third; HUD | slow drift (keyframes, zoom 1.0 -> 1.03) | tick per second, city bed (drone stand-in), cars passing |
| 0:04.5 | 0:07.0 | wide, caption 1 | same; friend turns and starts to wave at 0:06 (armR track) | push in toward you (zoom 1.03 -> 1.25) | ticks speed up |
| 0:07.0 | 0:10.8 | flip, close on you | CrossingSet `slow` mode: world to ghost 6%, a glow sphere around your head (R 0.0 -> 0.48 m; soft falloff so it reads); internal shake 0.3 s at 0:07.0; ripple glyph at the tourist's dark position at 0:10.3 | close (zoom 2.4 on your head), slow pull to 2.0 | impact; click at 0:10.3 |
| 0:10.8 | 0:15.8 | POV, your arm | whatif/PovHand over black with ghost neon bokeh; light edge reaches the fingertips at 0:12.5; dotted felt hand starts wiggling at 0:13.0 | static, slight drift | soft whoosh |
| 0:15.8 | 0:19.5 | POV, push-in step | same; the seen hand still frozen until 0:18.5, then follows | push in (1.0 -> 1.12) | tick |
| 0:19.5 | 0:25.0 | wide, rule | CrossingSet slow: bubble R 1.59 -> 2.29 m; ground lights from 0:19.6; ring tag; ripple glyphs from the dark (chime, voices) | zoom 1.35 -> 1.25 | ding (chime stand-in), city bed |
| 0:25.0 | 0:30.6 | wide, textless car pass | lit road ahead empty; at 0:26.5 wind: your jacket/hair whip, a paper cup tumbles inside the bubble (internal shake small) | static then tiny push | whoosh_long + boom (low) at 26.2-27.0, horn stand-in |
| 0:30.6 | 0:34.3 | wide two-shot, friend | the bubble edge reaches the friend at 0:30.6: she lights up mid-wave, then waves slowly | slow pan left (x 50% -> 46%) | soft ding at the reveal |
| 0:34.3 | 0:41.7 | wide, car image | the car pops in a metre in front of you at 0:34.3 and splits: copy A reverses left, copy B creeps right (positions from the fact file); tourist lights up at 0:38.4 | pan back right (46% -> 52%), zoom 1.2 -> 1.1 | riser starts 0:39 |
| 0:41.7 | 0:44.0 | full-frame white-out | white rect opacity 1 (41.7-42.7), fades 42.7-43.5 to the crossing; tourist lowers phone | none | stinger + whoosh |
| 0:44.0 | 0:47.0 | insert, tourist's phone | whatif/PhoneScreen held in the tourist's lit hand, no bars, spinner; dark ghost street behind | push in | phone_buzz (soft) |
| 0:47.0 | 0:54.0 | sky | tall scene: CrossingSet skyline strip low, whatif/SkyBodies above (ghost Moon, stars, two satellites); camera whips up 0.35 s at 0:47.0, holds, drops back down 0:53.0-0:54.0 | camera keyframes only | whoosh_long at 47.0 and 53.0 |
| 0:54.0 | 0:57.5 | wide + inset | CrossingSet slow (bubble 6.0 m); whatif/Inset MEANWHILE at (540, 760), 520x320: neon sign with growing halo | static | drone swells |
| 0:57.5 | 1:02.0 | wide pull-out | bubble 6.2 -> 7.0 m, edge leaves the frame by 1:01; HUD clock under 0:00.100 at 1:01.0 | pull out (zoom 1.0 -> 0.85) | riser peaks at 1:02 |
| 1:02.0 | 1:05.5 | return + afterimage | white rect 62.0-62.4; CrossingSet `exposure` (samples 12; far objects 5 s, friend 2.14 s) at opacity 1 -> 0.55; normal crossing fading up underneath | static | impact + stinger, then afterimage ring (stand-in drone) |
| 1:05.5 | 1:08.0 | twist hold | same afterimage, opacity 0.55 -> 0.15 | slow push in | heartbeat_slow |
| 1:08.0 | 1:09.5 | bookend | CrossingSet normal, frame-1 framing; signal green, crowd surging, friend waving; HUD fades out | static | city bed returns |
| 1:09.5 | 1:10.5 | black | black | none | one tick, music out |
| 1:10.5 | 1:18.0 | end card | title layers repeated exactly on near-black ("walked" amber); fact line at 1:11.5 | static | room tone (silence) |
