---
slug: whatif-calcium-gone-5-seconds
niche: whatif
format: short_9x16 (1080x1920), caption-led, calm Kokoro TTS reads the title and the captions only (CPU, Spark)
template: countdown-HUD, house wording (status chip ONLINE/OFFLINE, "ONLINE IN" clock, X-ray signature look)
working_title: "What if calcium disappeared for 5 seconds?"   # on-screen title and exact end-card repeat; alternatives ranked in titles.md
target_runtime_s: 84
target_runtime_range_s: [75, 85]
target_words_per_min:
  captions: 54          # 76 caption words / 84 s. PLAYBOOK §9 Shorts median 56 (43-65)
  voiceover: 59         # title (7) + captions (76) = 83 words; PLAYBOOK TTS caption-read 60-70
  all_on_screen_text: 148   # PLAYBOOK median 115 (103-131); over the band because the HUD carries one exact number per rung (see Word counts)
caption_count: 12       # PLAYBOOK 11 (11-13)
mean_caption_words: 6.3 # PLAYBOOK 6.7, max 8
event_at_s: 7.0         # 8.3% of runtime
slow_motion_factor: 12  # 5 s of story over 60 s of screen (0:07 -> 1:07)
master_loop: "ONLINE IN" countdown, 0:07 -> 1:07 (60 s = 71% of runtime, closes at 79.8%)
twist_at_s: 70.5        # 83.9%
references:
  - id: "7693494009494342945"
    short: ELECTRONS
    url: https://www.tiktok.com/@man_ia_c/video/7693494009494342945
    views: 18200000
    outlier_score: 29.13
    why: >-
      Same "basic ingredient vanishes for 5 s" hook (H1) and the cleanest 80 s skeleton in the corpus.
      Borrowed structure: pre-event clock over a named place, hard style flip with a slow-motion factor,
      harmless wonder on your own hands first, rule line then a shorter implication then a textless break,
      fastest caption cadence at the human peak, midpoint white-out, planet shot with a live climbing number,
      superlative top rung plus a terse status line, return + false resolution + stamp, twist, black,
      title repeat, small-caps fact. Our times sit 1-5 s off its timings and our HUD wording is our own.
  - id: "7693617402180881697"
    short: NEUTRONS
    url: https://www.tiktok.com/@man_ia_c/video/7693617402180881697
    views: 5100000
    outlier_score: 8.16
    why: >-
      Closest body-first shape: a personal HUD stat with a relatable comparison (their weight vs a child;
      our 1.1 kg vs a carton of milk), POV hands in the playful phase, the "each person" human climax right
      before the white-out, and its strongest device, a second countdown in the same units that races the
      return clock through a near-wordless stretch. Also the twist family where the returning particles,
      on their own, do something new and pay an early plant.
  - id: "7693305573487562016"
    short: OXYGEN
    url: https://www.tiktok.com/@man_ia_c/video/7693305573487562016
    views: 13400000
    outlier_score: 21.45
    why: >-
      Material-world ladder like ours (the element is a big share of everyday matter): a baseline reading
      before the event, a silent tell object at the flip, "% of" rule line, a built-world stat rung, a rung
      that snaps back to the viewer's own footing, HUD meter swaps instead of captions, and a rising HUD meter
      planted mid-video that comes due at the return.
playbook: research/corpus/whatif/PLAYBOOK.md §1A S1-S10, §5 (scale outward + return-to-you dip + closing distance), §6 T1 + T7, §9 Shorts pacing, §12 checklist
topic_evidence:
  - 'What If (Underknown) "What If We Didn''t Have Bones and Turned Into Human JELLYFISH?" 4.42M (boneless-body demand)'
  - '@man_ia_c "iron" body-level vanish Short 2.7M (4.3x)'
  - 'Whitespace check rerun 2026-11-01 10:46Z on the Spark (backlog/whatif/evidence/checks-0903/calcium-whatif-ytsearch.txt): "what if calcium disappeared / vanished / all calcium disappeared from earth" returns supplement videos plus one on-topic upload, "The Day Calcium Vanished... (funny)", 344 views. No calcium what-if with traction exists.'
originality: "python3 scripts/originality_check.py backlog/whatif/whatif-calcium-gone-5-seconds/script.md research/corpus research/library/transcripts -> PASS (see review.json)"
---

# What if calcium disappeared for 5 seconds?

Episode `whatif-calcium-gone-5-seconds` · 9:16 · 84 s · countdown-HUD template in house wording · caption-led, calm TTS read of the title and captions only.

**The idea in one line.** On an X-ray, the white is calcium. We scan the Colosseum queue in X-ray, every white glow blinks out, and for five slowed-down seconds everything held up by calcium lets go: your fingers, the queue, a marble bust, the travertine under your feet, the Colosseum, concrete, your house, every heartbeat, chalk cliffs, Everest's summit and the reef. Then the calcium comes back exactly where it was, and nobody is standing there anymore.

## Beat alignment table

Reference timestamps are from the annotated corpus files `research/corpus/whatif/<id>.md` (re-checked for this version). We take only structure, timing and devices, never wording.

| # | Our beat (PLAYBOOK tag) | Our time | Reference id @ timestamp | Device borrowed | How we adapt it |
|---|---|---|---|---|---|
| 1 | S1 Premise card + pre-event clock | 0:00–0:05 | 7693494009494342945 @ 0:00 (title, icon, HUD countdown, scope subline); 7693617402180881697 @ 0:00 (subline as a quiet plant) | 7-word title with accent keyword and icon, clock counting to the event, scope line that the ending pays | Keyword "calcium" in X-ray cyan with a bone glyph. Scope line "IN EVERY BONE, HEARTBEAT AND LIMESTONE" plants three rungs (0:08 bone, 0:20.5–0:31.5 limestone, 0:38.5 heartbeat). Second subline gives a dated precedent: "STANDING SINCE AD 80". |
| 2 | S2 Place you | 0:05–0:07 | 7693494009494342945 @ 0:05; 7693305573487562016 @ 0:05 | One second-person line naming a famous real place; calm "before" image with tell objects | The Colosseum queue. The Colosseum is travertine (a limestone), so the place itself is a rung. Tell objects: a marble bust on a granite plinth beside the queue, a travertine kerb under it. Both are paid in order at 0:20.5 and 0:27.5. |
| 3 | Baseline look before the delta | 0:05.5–0:07 | 7693305573487562016 @ 0:00–0:07 (baseline reading "AIR PRESSURE" before the event) | Show the normal value first so the change reads as a delta | An X-ray scan line sweeps the frame; every calcium thing glows white for 1.5 s with the HUD flash "WHITE = CALCIUM". The viewer learns the code before it is broken. |
| 4 | S3 Flip + master loop | 0:07 | 7693494009494342945 @ 0:08 (hard style flip, slow-motion factor); 7693305573487562016 @ 0:08 (silent tell: the flames cut out) | Clock hits zero, hit, HUD flips to a return countdown, slow-motion factor makes the clock add up | Every white glow blinks out in two frames (our silent tell). Status chip flips to OFFLINE, clock "ONLINE IN 5.000 S" runs at 1/12 speed ("X-RAY TIME ×12"). |
| 5 | S4 Wonder on your own hands | 0:08–0:13.5 | 7693494009494342945 @ 0:15 (first-person POV of your hands, harmless wonder); 7693617402180881697 @ 0:13 (POV hands, slightly funny) | Smallest harmless, slightly funny effect on the viewer's body = the screenshot moment | POV of your X-ray hands: the finger bones are outline-only now and the fingers droop and wobble like gummy worms (demineralised bone is bendy collagen). |
| 6 | S4 Personal stat | 0:11 | 7693617402180881697 @ 0:11 (HUD personal weight) + @ 0:13 (relatable comparison) | Physics turned into a number about you, then an everyday equivalent | HUD "YOU: −1.1 KG ≈ A CARTON OF MILK". It is also the plant the twist pays at 1:11. |
| 7 | S4 Same effect on the crowd, still playful | 0:13.5–0:20.5 | 7693305573487562016 @ 0:09 ("everyone" gets the bodily effect at once); 7693617402180881697 @ 0:16–0:20 (people around you start to float, breather); 7693617402180881697 @ 0:26 (HUD hands over a scale number) | Person → crowd, still harmless, then a crowd number in the HUD | The whole queue wobbles like inflatable tube men; nobody falls yet. HUD crowd stat "1.7 TRILLION BONES: SOFT" (206 × 8.2 billion). |
| 8 | S5 Rule line (rung 1: object) | 0:20.5 | 7693305573487562016 @ 0:13 ("% of" rule); 7693494009494342945 @ 0:21 (plain-science rule) | One plain rule with a percentage | "Marble is 40% calcium by weight." over the bust from 0:00 sagging on its plinth (the plinth is granite and stays square). Pie chip fills 40%. |
| 9 | S5 Shorter implication | 0:24 | 7693494009494342945 @ 0:25 (shorter line that lets the viewer finish the logic) | Implication without the consequence | "The Colosseum is made of it." HUD gives the Colosseum's number: 100,000 m³ of travertine. |
| 10 | S5 Textless break (rungs 2-3: kerb, monument) | 0:27.5–0:31.5 | 7693494009494342945 @ 0:28 (4 s with no caption while matter breaks); 7693617402180881697 @ 0:28–0:31 (no caption, hard visual change) | 3–4 s with no caption while the image delivers the consequence | First real collapse in the video: the travertine kerb crumbles under the queue, the arcade pours away, and you and the queue fold into heaps. |
| 11 | Mid-video plant (rising/closing meter) | 0:29.5 | 7693305573487562016 @ 0:28 (new HUD meter that plants the ending) | A HUD meter introduced on one rung that comes due at the return | "SAND: 39 M AWAY": the Colosseum's sand starts sliding toward the queue. Paid by the race at 0:55 and the landing at 1:08.2. |
| 12 | S6 Material rung + live counter | 0:31.5–0:35 | 7693305573487562016 @ 0:30 (stat rung on the built world) | Built-world rung, HUD carries the number | "Concrete loses its glue." HUD counter "CONCRETE FAILING: 0 → 550 BILLION T" runs over the concrete cross-section and your house (both concrete), ending at 0:38.5. |
| 13 | S6 Return-to-you rung | 0:35–0:38.5 | 7693305573487562016 @ 0:35 (ladder snaps back to the viewer's own footing) | The climb drops back to the viewer | "Your house caves in on itself." A generic house tagged YOUR HOUSE; foundations, mortar and plaster give way. |
| 14 | S6 Human peak, fastest cadence | 0:38.5–0:41.5 | 7693617402180881697 @ 0:37 ("each person" climax right before the white-out); 7693494009494342945 @ 0:35 (captions 3 s apart at the peak) | Most human, most shareable line right before the interrupt; captions closest together | "8.2 billion hearts stop at once." Back on your chest: the heart outline is still. HUD "YOUR HEART: 3 BEATS MISSED" (70 bpm × 2.6 story-seconds). Captions at 31.5 / 35 / 38.5 (3.5 s apart). |
| 15 | Midpoint white-out | 0:41.5–0:43.5 | 7693494009494342945 @ 0:40; 7693617402180881697 @ 0:40–0:42 (white-out as the wipe from ground to planet) | Full-frame interrupt that wipes from ground scale to planet scale | The dust of every city at once, tinted pale cyan so "pure white = calcium" stays true until the return. |
| 16 | S7 Planet counter + fast montage | 0:43.5–0:55 | 7693494009494342945 @ 0:42 (live climbing counter over a planet shot); 7693617402180881697 @ 0:43; 7693305573487562016 @ 0:39 (meter swap instead of a caption) | Wide view with a planet-level live number; HUD swaps carry the rungs | Flat world map in X-ray grade, "LAND CAVING IN: 0 → 15.2%" (the share of ice-free land on carbonate rock). Under it, quick cuts with their own HUD meters: Dover cliffs 110 → 0 m, Everest 8,849 → 8,600 m, reef 0 → 2,300 km. |
| 17 | S7 Superlative top rung + terse status | 0:48.5–0:52 | 7693494009494342945 @ 0:50 (superlative top rung) + @ 0:56 (terse HUD status line) | Superlative, then a two-word status in the HUD | "Everest is no longer the tallest mountain." HUD "K2: 8,611 M" next to the Everest meter stopping at 8,600. |
| 18 | S7 Race (closing distance, same units) | 0:55–1:07 | 7693617402180881697 @ 0:50 (forward-threat caption) + @ 0:52 (second countdown races the return clock, ~14 s nearly wordless, return wins) | Two clocks in the same units racing through a near-wordless stretch | "Back in Rome, the sand keeps coming." HUD "SAND: 13 M AWAY" and "REACHES YOU IN 1.100 S" against "ONLINE IN 1.000 S". The return wins by 0.1 s. 12 s with no caption while both clocks run. |
| 19 | S8 Return + false resolution + stamp | 1:07–1:10.5 | 7693494009494342945 @ 1:02–1:06; 7693617402180881697 @ 1:04–1:06 | Clock hits zero, status flip, reassuring line, a stamp tying back to the opening | Chip flips to BACK ONLINE, every white re-glows, "Every calcium atom reappears exactly where it vanished." Stamp "1,946 YEARS · 5 SECONDS" (pays "STANDING SINCE AD 80"). |
| 20 | S9 Twist (T1 + T7) | 1:08.2–1:14.5 | 7693617402180881697 @ 1:09–1:10 (the returning particles, on their own, do something new and pay a 0:00 plant); PLAYBOOK §6 T7 (7694025665993100576 @ 0:59, you are exactly where it lands) | One twist caption + one HUD line built on an earlier plant | The sand still arrives (the return did not save you). Camera rises: white ghost skeletons hang upright where everyone stood, a white ghost Colosseum hangs over its own sand. "But you're not standing there anymore." HUD "YOUR 1.1 KG: 1 M ABOVE YOU", then "YOUR HEART: STILL 0 BPM". The ghosts start to sift down. |
| 21 | S10 Black + exact title repeat + true fact | 1:14.5–1:24 | 7693494009494342945 @ 1:12–1:20; 7693305573487562016 @ 1:10–1:20; 7693617402180881697 @ 1:12–1:20 | ~1.5 s black, identical title card, small-caps checkable fact held ~7 s, CTA only in the post caption | 14-word fact about your bones and heartbeat (pays the scope line and the heart rung). |

## Script

Text layers stay in fixed positions throughout. TITLE and END sit mid-frame in a serif face. Each CAPTION sits low in slanted serif: one idea, 8 words or fewer. HUD: top-left block with a status chip (CALCIUM ● ONLINE / OFFLINE / BACK ONLINE), one large monospaced clock line with millisecond digits and up to two small-caps sublines (S1, S2). **VO** reads the title and each caption, nothing else (Kokoro, calm, about 60 wpm with holds). Times are global seconds.

**Hook.** First line on screen and in VO: "What if calcium disappeared for 5 seconds?" First visual: a sunny flat-vector Colosseum with a tourist queue in front, YOU tagged in it, and the HUD already counting "OFFLINE IN 7.000 S". Nothing breaks until 0:07; the clock is the hook.

### HOOK (S1) 0:00.0 – 0:05.0
- 0:00.0 TITLE: What if **calcium** disappeared for 5 seconds?  (keyword in cyan, bone glyph above)
- 0:00.3 VO: What if calcium disappeared for five seconds?
- 0:00.0 HUD chip: CALCIUM ● ONLINE · clock: OFFLINE IN 7.000 S, counting down in real time
- 0:00.0 HUD S1: IN EVERY BONE, HEARTBEAT AND LIMESTONE
- 0:02.5 HUD S2: STANDING SINCE AD 80

### PLACE YOU (S2) 0:05.0 – 0:07.0
- 0:05.0 CAPTION + VO: You're queuing at the Colosseum in Rome.
- 0:05.5 (no new caption) X-ray scan line sweeps down the frame; every calcium thing glows white
- 0:05.8 HUD S1: WHITE = CALCIUM

### FLIP (S3) 0:07.0
- 0:07.0 every white glow blinks out at once. HUD chip: CALCIUM ● OFFLINE · clock: ONLINE IN 5.000 S, counting down at 1/12 speed
- 0:07.0 HUD S1: X-RAY TIME ×12 (S2 clears)

### WONDER, BODY FIRST (S4) 0:08.0 – 0:20.5
- 0:08.0 CAPTION + VO: Every finger bends like a gummy worm.
- 0:11.0 HUD S1: YOU: −1.1 KG ≈ A CARTON OF MILK
- 0:13.5 CAPTION + VO: The whole queue starts to wobble.
- 0:17.0 HUD S1: 1.7 TRILLION BONES: SOFT

### RULE + TURN (S5) 0:20.5 – 0:31.5
- 0:20.5 CAPTION + VO: Marble is 40% calcium by weight.  (HUD S1 clears; the pie chip carries the 40%)
- 0:24.0 CAPTION + VO: The Colosseum is made of it.
- 0:24.0 HUD S1: 100,000 M³ OF TRAVERTINE
- 0:27.5 – 0:31.5 no caption. The kerb crumbles, the arcade pours away, the queue folds.
- 0:29.5 HUD S1 (counting down): SAND: 39 M AWAY

### OUTWARD LADDER (S6) 0:31.5 – 0:43.5
- 0:31.5 CAPTION + VO: Concrete loses its glue.
- 0:31.5 HUD S1 (climbing to 0:38.5): CONCRETE FAILING: 0 → 550 BILLION T
- 0:35.0 CAPTION + VO: Your house caves in on itself.
- 0:38.5 CAPTION + VO: 8.2 billion hearts stop at once.
- 0:38.5 HUD S1: YOUR HEART: 3 BEATS MISSED
- 0:41.5 – 0:43.5 pale-cyan white-out (the dust of every city). No caption; HUD at 40% opacity.

### PLANET CLIMB + RACE (S7) 0:43.5 – 1:07.0
- 0:43.5 HUD S1 (climbing to 0:55): LAND CAVING IN: 0 → 15.2%
- 0:46.0 HUD S2 (counting down): DOVER CLIFFS: 110 → 0 M
- 0:48.5 CAPTION + VO: Everest is no longer the tallest mountain.
- 0:48.5 HUD S2 (counting down): EVEREST: 8,849 → 8,600 M
- 0:50.5 HUD S2: K2: 8,611 M
- 0:52.0 HUD S2 (climbing): REEF COLLAPSED: 0 → 2,300 KM
- 0:55.0 CAPTION + VO: Back in Rome, the sand keeps coming.
- 0:55.0 HUD S1 (counting down): SAND: 13 M AWAY → 1.2 M at 1:07
- 0:55.0 HUD S2 (counting down): REACHES YOU IN 1.100 S → 0.100 S at 1:07
- 1:01.0 the main clock turns red under 0.500 S (no new words). 12 s with no caption: only the two clocks move.

### RETURN (S8) 1:07.0 – 1:10.5
- 1:07.0 clock reads ONLINE IN 0.000 S; chip flips: CALCIUM ● BACK ONLINE. Every white re-glows.
- 1:07.0 HUD S2: 1,946 YEARS · 5 SECONDS
- 1:07.5 CAPTION + VO: Every calcium atom reappears exactly where it vanished.
- 1:08.2 the sand reaches the queue anyway (HUD S1 reads SAND: 0.0 M AWAY and holds)

### TWIST (S9) 1:10.5 – 1:14.5
- 1:10.5 CAPTION + VO: But you're not standing there anymore.
- 1:11.0 HUD S1: YOUR 1.1 KG: 1 M ABOVE YOU
- 1:12.5 HUD S2: YOUR HEART: STILL 0 BPM

### OUTRO (S10) 1:14.5 – 1:24.0
- 1:14.5 – 1:16.0 black, silence, HUD hidden
- 1:16.0 END: What if **calcium** disappeared for 5 seconds?  (identical to the opening card; not read)
- 1:16.8 END fact (small caps, held to 1:24; not read): 99% OF YOUR CALCIUM SITS IN BONES AND TEETH. THE REST TRIGGERS YOUR HEARTBEAT.

### Post caption (not on screen)
Five seconds without calcium, in the queue for the Colosseum. Your fingers went bendy. The whole queue folded. A marble bust sagged, the Colosseum poured away, concrete let go and 8.2 billion hearts skipped three beats. The White Cliffs of Dover slid into the sea and Everest lost its crown to K2. Then every atom came back exactly where it had been, a metre above where you were lying. Which element should vanish next? #whatif #pov #simulation #science

### Word counts and pacing (checked by script, see review.json)
- Captions: 12 lines, 76 words, mean 6.3, longest 8. Caption rate 54 wpm over 84 s.
- VO: title (7) + captions (76) = 83 words, 59 wpm. Every VO line ends before the next caption starts (longest line 8 words, about 3 s at Kokoro pace; tightest gap 3.0 s).
- All on-screen text: 207 words (captions 76, title 7, end title 7, fact 14, HUD 103 counting every HUD string once with numbers and clock labels), about 148 wpm. That is over the PLAYBOOK band (103-131; ELECTRONS has 43 HUD words). The surplus is deliberate: every rung carries one exact number in the HUD (critique: a chain of exact consequence numbers), and two-thirds of the HUD words are numbers or 2-4-word meters that are glanced at, not read. If the gate review finds the HUD busy, cut in this order: WHITE = CALCIUM, 100,000 M³ OF TRAVERTINE, YOUR HEART: STILL 0 BPM (−11 words, 140 wpm).
- Second-person captions: 3 of 12 (25%): the place line, the house rung and the twist. Corpus Shorts median 18% (7-18%). We sit one line over on purpose so the 50% dip and the payoff land on the viewer (PLAYBOOK §5 return-to-you dips, §10D payoff on the viewer). The heart, sand and 1.1 kg lines put "YOU/YOUR" in the HUD instead of in captions.
- Caption gaps (start to start): 3.0, 5.5, 7.0, 3.5, 7.5, 3.5, 3.5, 10.0, 6.5, 12.5, 3.0 s. Median 5.5 s. Five gaps run over 6 s, and each is covered: 13.5→20.5 by the HUD crowd stat at 0:17; 24→31.5 by the designed textless break plus the sand meter at 0:29.5; 38.5→48.5 by the white-out (0:41.5), the land counter (0:43.5) and the Dover meter (0:46); 48.5→55 by HUD swaps at 0:50.5 and 0:52; 55→67.5 by two moving clocks (the PLAYBOOK tolerates a 10-15 s caption gap when the tracker keeps ticking) plus the red clock at 1:01 and the status flip at 1:07.
- New on-screen element about every 2.6 s; the HUD clock moves every frame from 0:00 to 1:07.

### Open loops
- Pre-event clock: opens 0:00, closes 0:07.
- Master return clock: opens 0:07, closes 1:07 (60 s, 71% of runtime, closing at 79.8%).
- Scope plant "bone, heartbeat, limestone": paid at 0:08 (bone), 0:20.5–0:31.5 (limestone), 0:38.5 (heartbeat).
- The 1.1 kg number: opens 0:11, paid by the twist subline at 1:11.
- Tell objects (bust, kerb): open 0:00, paid at 0:20.5 and 0:27.5; both come back as ghosts in the twist.
- Sand meter: opens 0:29.5, races the clock 0:55–1:07, lands 1:08.2.
- AD 80: opens 0:02.5, paid by the return stamp at 1:07.
- Your heart: opens 0:38.5, paid in-story at 1:12.5 and by the end fact at 1:16.8.
- Left open for comments: "Which element should vanish next?" (post caption, PLAYBOOK §8 series harvest).

## HUD state table

One `whatif/Hud` instance per scene (core has no persistent overlay), fed the global start time `t0` of its scene so the clock stays continuous across cuts. Slots: L = status chip, T = clock line, S1/S2 = sublines. τ = story seconds = (t − 7) / 12.

| Slot | From | To | Text | Value track / formula |
|---|---|---|---|---|
| L | 0.0 | 7.0 | CALCIUM ● ONLINE | chip dot white |
| L | 7.0 | 67.0 | CALCIUM ● OFFLINE | chip dot hollow red |
| L | 67.0 | 74.5 | CALCIUM ● BACK ONLINE | chip dot white |
| T | 0.0 | 7.0 | OFFLINE IN {v} S | v = 7.000 − t, 3 decimals, clamp 0 |
| T | 7.0 | 67.0 | ONLINE IN {v} S | v = 5 − τ, 3 decimals; colour red from 61.0 (v < 0.5) |
| T | 67.0 | 74.5 | ONLINE IN 0.000 S | frozen, white |
| S1 | 0.0 | 5.8 | IN EVERY BONE, HEARTBEAT AND LIMESTONE | static |
| S1 | 5.8 | 7.0 | WHITE = CALCIUM | static, white glow |
| S1 | 7.0 | 11.0 | X-RAY TIME ×12 | static |
| S1 | 11.0 | 17.0 | YOU: −1.1 KG ≈ A CARTON OF MILK | static |
| S1 | 17.0 | 20.5 | 1.7 TRILLION BONES: SOFT | static |
| S1 | 24.0 | 29.5 | 100,000 M³ OF TRAVERTINE | static |
| S1 | 29.5 | 31.5 | SAND: {v} M AWAY | v = 40 − 12.08 (τ − 1.79), 0 decimals (39 → 37) |
| S1 | 31.5 | 38.5 | CONCRETE FAILING: {v} BILLION T | 0 → 550, ease out, 0 decimals |
| S1 | 38.5 | 43.5 | YOUR HEART: 3 BEATS MISSED | static; 40% opacity 41.5–43.5 |
| S1 | 43.5 | 55.0 | LAND CAVING IN: {v}% | 0 → 15.2, ease out, 1 decimal |
| S1 | 55.0 | 71.0 | SAND: {v} M AWAY | same formula, 1 decimal, clamp 0 (13.3 → 0.0 at 68.2, then holds) |
| S1 | 71.0 | 74.5 | YOUR 1.1 KG: 1 M ABOVE YOU | static |
| S2 | 2.5 | 7.0 | STANDING SINCE AD 80 | static |
| S2 | 46.0 | 48.5 | DOVER CLIFFS: {v} M | 110 → 0 |
| S2 | 48.5 | 50.5 | EVEREST: {v} M | 8,849 → 8,600, thousands separator |
| S2 | 50.5 | 52.0 | K2: 8,611 M | static |
| S2 | 52.0 | 55.0 | REEF COLLAPSED: {v} KM | 0 → 2,300, thousands separator |
| S2 | 55.0 | 67.0 | REACHES YOU IN {v} S | v = 5.1 − τ, 3 decimals (1.100 → 0.100) |
| S2 | 67.0 | 72.5 | 1,946 YEARS · 5 SECONDS | static |
| S2 | 72.5 | 74.5 | YOUR HEART: STILL 0 BPM | static |

## Shot list

Kit vocabulary: core layers (`rect`, `circle`, `text`, `svg`, `particles`, `component`), `transitionIn` (`cut`, `fade`, `dipBlack`, `whip`, `glitch`), camera presets or keyframes + `shake`, `grade`. Reused from the explainer kit: `explainer/You` (daylight queue only), `Tag`, `Stat`, `DepthMeter`, `Map` (with the two small edits in Build notes). **NEW** whatif kit components (8): `whatif/Hud`, `whatif/TitleCard` (with a `fact` prop for the end card), `whatif/XrayFigure`, `whatif/Colosseum`, `whatif/Statue`, `whatif/ConcreteSection`, `whatif/House`, `whatif/Strata`. Captions are drawn as whole-sentence text layers. SFX cue names are files in `studio/public/sfx/`.

X-ray rule for the whole video: X-ray mode = navy-black #050B18, cyan #7FE3FF 2 px outlines, calcium filled pure white #FFFFFF. Pure white appears only 0:05.5–0:07.0 and from 1:07.0. Between 0:07 and 1:07 nothing on screen is pure white (the white-out is pale cyan #D8F6FF).

| # | t_start | t_end | Shot | Visual (kit vocabulary) | Camera | SFX |
|---|---|---|---|---|---|---|
| 1 | 0:00.0 | 0:05.5 | Wide establishing + title | `background: gradient` noon sky #8EC9F0 → #F4E3C1. NEW `whatif/Colosseum` (`mode: day`), a simple 3-tier arcade elevation with the attic and the broken outer ring on the right. Queue of 9 `explainer/You` (`pose: stand`, muted colours) on a travertine kerb strip (`rect`), YOU in white with `Tag` "YOU". NEW `whatif/Statue` (marble bust on a granite plinth) beside the queue. NEW `whatif/TitleCard`, bone glyph `svg` above. NEW `whatif/Hud`. | `drift` 0.4 | `clock_ticking` vol 0.25; soft bed from 0:00 |
| 2 | 0:05.5 | 0:07.0 | X-ray scan (baseline) | Same framing. A cyan scan line (`rect`, 6 px, glow) sweeps top to bottom 5.5–5.8; behind it the scene redraws in X-ray mode: NEW `whatif/XrayFigure` ×9 at the `explainer/You` hip positions (skeletons glowing white, YOU's heart a pulsing cyan outline at 70 bpm), Colosseum and kerb filled white, bust white, granite plinth outline-only. | slow `pushIn` (1.0 → 1.06) | `sonar_ping` at 5.5; `tick` at 5.0, 6.0 |
| 3 | 0:07.0 | 0:08.0 | Blink-out (flip) | Every white fill drops to empty outline in 2 frames; YOU's heart outline stops on the next beat. HUD flips. | `shake` at 0 (amplitude 10, 0.3 s) | `impact` at 0; `glitch` vol 0.4 at 0 |
| 4 | 0:08.0 | 0:13.5 | POV hands (wonder) | `whatif/XrayFigure` `view: hands`: two raised X-ray hands in the foreground, the Colosseum outline behind (Colosseum `sag` 0 → 0.05, barely). Finger chains droop and wobble (`bend` track 0 → 0.8, wobble 3 Hz). | keyframes: tiny bob, push 1.0 → 1.05 | `pop` vol 0.3 at 1.2, 2.0 |
| 5 | 0:13.5 | 0:20.5 | Queue wobble (crowd) | `whatif/XrayFigure` ×9 `view: body`, `sway` track 0 → 1 (arms flop, torsos sway like tube men, still standing; `slump` ≤ 0.15). Colosseum `sag` 0.05 → 0.15. | `pullOut` from YOU (zoom 1.5 → 1.0) | `whoosh` vol 0.3 at 0.3 |
| 6 | 0:20.5 | 0:24.0 | Rung 1: bust | `whatif/Statue` close-up, `mode: xray`, `melt` 0 → 0.7 (util.ts warp pulls the bust down into wax-like drips; granite plinth stays square). Pie chip: `svg` 40% wedge + `explainer/Stat` 0 → 40 suffix "%". | `pushIn` 1.0 → 1.1 | `click` at 0.4 |
| 7 | 0:24.0 | 0:27.5 | Implication: the Colosseum | Colosseum `mode: xray` full facade, `sag` 0.15 → 0.25 (arches start to bow). Queue foreground, kerb visible. | slow `panUp`, then tilt down to the kerb by 3.5 | `drone` vol 0.25 from 0 |
| 8 | 0:27.5 | 0:31.5 | Textless break: kerb → arcade → queue | 0.0–0.8 the kerb crumbles to grit; 0.8–2.5 arches lose their edges and pour (`pour` 0 → 1: ≤ 500 seeded grains + a growing mound path inside the component); 1.3–2.7 the 9 figures fold in a 0.15 s stagger (`slump` 0.15 → 1); 2.0–4.0 a sand tongue slides out from the wall base toward the queue (`sandFront` track). | slow `panUp` + `shake` at 1.5 (amplitude 6, 2.5 s, no decay) | `underwater_rumble` 0–4 (as rumble); `boom` vol 0.4 at 0.9 |
| 9 | 0:31.5 | 0:35.0 | Rung: concrete | NEW `whatif/ConcreteSection` (X-ray only): square cut of concrete, grey gravel and sand grains in an empty dotted binder web; grains slip and pile, a few limestone-aggregate grains crumble too. | `pushIn` 1.0 → 1.15 | `static` vol 0.2 0.2–3.4 (gravel trickle) |
| 10 | 0:35.0 | 0:38.5 | Rung: your house | NEW `whatif/House` (X-ray only, generic two-storey house on a concrete slab): plaster and mortar outlines go dotted, walls cave in (`cave` 0 → 1); `Tag` "YOUR HOUSE". At 2.5 pull back: a row of the same house caving in. | `pullOut` (zoom 1.2 → 0.85) | `boom` at 0.6 |
| 11 | 0:38.5 | 0:41.5 | Human peak: your heart | Back in Rome: YOU's folded `XrayFigure` heap, chest close-up; the heart outline is still; a flat cyan ECG line runs across the frame bottom-left (`svg`). | hold, push 1.0 → 1.04 | `heartbeat_slow` once at 0.1, then silence of the bed for 1.5 s |
| 12 | 0:41.5 | 0:43.5 | White-out | Core layers only: dust billows up from the bottom (`particles` `dust` 300, pale cyan) and a full-frame `rect` #D8F6FF fades 0 → 1 by 1.2; HUD at 40%. | `shake` at 0 (amplitude 14, 0.6 s) | `whoosh_long` 0–2 |
| 13 | 0:43.5 | 0:46.0 | Planet: world map | `transitionIn: fade` 0.5. `explainer/Map` flat world at zoom 1 (lon 20, lat 15), land #0C2233, `strokeColor` cyan; ~40 carbonate-region `dots` (south China, Mediterranean, Dinarides, Middle East, Florida/Yucatán, Nullarbor…) pulse and dim as the land counter climbs. | `drift` 0.3 | `riser` vol 0.3 from 0 |
| 14 | 0:46.0 | 0:48.5 | Montage: Dover | NEW `whatif/Strata` `profile: cliff`: 110 m chalk face with flint bands over the Channel, crumbling top-down into a pale plume; `explainer/DepthMeter` ruler on the right (110 → 0, suffix " M"). | `panDown` | `whoosh` at 0.2 |
| 15 | 0:48.5 | 0:52.0 | Montage: Everest | `whatif/Strata` `profile: peak`: summit pyramid band (Qomolangma limestone, 8,849–8,600 m, tiny trilobite fossils) and the Yellow Band below drawn half-dotted; the top band crumbles and slides off; DepthMeter 8,849 → 8,600. At 2.0 a small K2 silhouette pin-in on the right edge with its 8,611 tick, now higher. | `panUp` to summit, `shake` at 1.0 (amplitude 5, 1 s) | `impact` vol 0.4 at 1.0; `drone` vol 0.25 |
| 16 | 0:52.0 | 0:55.0 | Montage: reef | `explainer/Map` Queensland coast (views lon 147 lat −18 zoom 5), reef as a dotted cyan `dots` line along the shelf (lat −10.7 to −24.5), dots go out north to south with `out` times. | Map views keyframes | `bubbles` vol 0.3 |
| 17 | 0:55.0 | 1:01.0 | Race (wide) | Rome, low wide over the 9 heaps on the crumbled kerb; Colosseum mound behind; the sand tongue creeps in from the right (`sandFront` 13 → 7 m, mapped to screen x). | `drift` 0.2 | `clock_ticking` vol 0.4; `drone` vol 0.3 |
| 18 | 1:01.0 | 1:07.0 | Race (tight) | Low tight on YOU's heap, sand edge closing (7 → 1.2 m). | `pushIn` 1.0 → 1.2 | `clock_ticking` vol 0.6; `heartbeat_fast` vol 0.25 (as tension, not YOU's heart) |
| 19 | 1:07.0 | 1:09.5 | Return + false resolution | `transitionIn: glitch` 0.2. Same tight frame: pure white light floods in from above the frame edge (the glows are back, but up there). 1.2: sand edge washes over the heap's feet (`sandFront` 0), small dust puff. | hold | `stinger` at 0; `impact` vol 0.3 at 1.2 |
| 20 | 1:09.5 | 1:14.5 | Twist reveal | Camera rises: white ghost skeletons (`XrayFigure` `ghost: true`, standing pose, `offsetY` +1 m) hang upright over each heap; the ghost bust floats over its puddle on the granite plinth; a white ghost Colosseum (`Colosseum` `ghost: true`) hangs over its sand mound. At 3.0 the ghosts start to sift down as white powder (`ghostFall` 0 → 0.2). Stylised line art, no gore. | keyframes: `panUp` + `pullOut` (zoom 1.4 → 1.0) | `impact` vol 0.5 at 1.0; bed cuts at 4.8 |
| 21 | 1:14.5 | 1:16.0 | Black | `background: color` #000; HUD hidden. | none | silence |
| 22 | 1:16.0 | 1:24.0 | End card | `whatif/TitleCard` same as 0:00 with `fact`; fact fades in at 0.8 and holds to the end. | none | `ding` vol 0.2 at 0.8; bed tail |

## Fact sheet (verified 2026-11-01 unless flagged)

| # | Claim on screen | Value used | Source / status |
|---|---|---|---|
| 1 | Calcium in an adult body | 1.1 kg (1.0–1.2 kg) | Standard physiology value (Guyton & Hall, *Textbook of Medical Physiology*, calcium chapter; Institute of Medicine 2011 DRI report for calcium). The NIH ODS sheet gives only the 99% share, so it is cited for row 2 only. |
| 2 | 99% in bones and teeth | 99% | NIH Office of Dietary Supplements, Calcium fact sheet. |
| 3 | 1.1 kg ≈ a carton of milk | 1 L of milk ≈ 1.03 kg | Milk density ~1.03 g/mL. |
| 4 | Fingers bend like gummy worms | demineralised bone is flexible collagen (about 30% of bone mass) | The acid-demineralised "vinegar bone" demo. Without calcium the muscles cannot contract either, so limbs go limp. |
| 5 | 1.7 trillion bones | 206 × 8.2 billion = 1.69 trillion | Adult bone count; UN World Population Prospects 2024 (about 8.2 billion in 2025–26). Children have more bones, so this is a floor. |
| 6 | Timing of the wobble and the fold | story τ = 0.1–1.9 s | **Stylised.** A real body losing all bone stiffness would buckle within about a second; we let the fold land at τ ≈ 1.8 s so the playful phase reads first. Kept consistent: nothing in Rome is shown falling before 0:27.5. |
| 7 | Marble is 40% calcium by weight | CaCO₃: 40.08 / 100.09 = 40.0%; statuary marble is ~98–99% calcite | Molar masses. Natural limestone runs lower, which is why the rule line names marble. |
| 8 | Bust plinth survives | granite has little calcium (mostly quartz and feldspar) | Geology basics; the plinth stays square on screen. |
| 9 | The Colosseum is made of it; 100,000 m³ of travertine; standing since AD 80 | travertine = CaCO₃; ~100,000 m³; inaugurated AD 80 under Titus; 1,946 years by 2026 | Parco archeologico del Colosseo; Encyclopaedia Britannica. |
| 10 | Kerb under the queue | Roman kerbs are commonly travertine | Rome street practice (cordoli in travertino). Stylised. |
| 11 | Sand front 40 m → 0 m, reaches the queue at T+5.10 s | d = 40 − 12.08 (τ − 1.79) m | **Stylised.** The queue is placed 40 m from a 48 m wall; a granular collapse of a tall wall runs out about one wall height, with a front speed of order √(gH)/2 ≈ 11 m/s. Chosen so the return wins by 0.1 s. |
| 12 | Concrete loses its glue | Portland cement CaO 60–67%; the binder is calcium silicate hydrate | Taylor, *Cement Chemistry*. Much concrete aggregate is limestone too, so some gravel crumbles on screen. |
| 13 | Concrete failing: 550 billion t | concrete is the largest human-made mass category, about half of ~1.1 Tt (≈ 549 Gt in Extended Data Table 1) | Elhacham et al., *Nature* 588, 442–444 (2020). Checked the paper on 2026-11-01: total ≈ 1.1 Tt and concrete is the dominant category. The table cell is an image, so the exact 549 Gt is read from the table, not extracted as text. HUD rounds to 550. |
| 14 | Your house caves in | concrete slab/foundation, cement or lime mortar, gypsum plaster and drywall (CaSO₄·2H₂O, 23% Ca) | Building-materials basics. |
| 15 | 8.2 billion hearts stop; 3 beats missed | Ca²⁺ triggers excitation–contraction coupling in heart muscle; at 70 bpm, 2.6 story-seconds = 3.06 beats | Physiology texts (Guyton & Hall). The current beat relaxes and the next one never comes. |
| 16 | Land caving in: 15.2% | karstifiable carbonate rock covers 15.2% of the ice-free continental surface | Goldscheider et al. 2020, *Hydrogeology Journal* 28, 1661–1677 (World Karst Aquifer Map). |
| 17 | Dover cliffs 110 → 0 m | chalk = coccolith calcite; cliffs up to ~110 m | National Trust / BGS. |
| 18 | Everest 8,849 → 8,600 m; no longer the tallest; K2 8,611 m | Qomolangma Formation (Ordovician limestone with fossils) runs from the summit down to the Qomolangma detachment at ~8,600 m; K2 is 8,611 m | Searle et al. (Everest geology); China–Nepal 2020 survey (8,848.86 m). **Caveat:** the Yellow Band below (~8,200–8,600 m) is marble and calc-silicate, so by our own rule the summit could drop toward ~8,200 m. We show 8,600 as the floor of the honest minimum and draw the Yellow Band half-dotted; either way Everest ends below K2. |
| 19 | Reef collapsed: 2,300 km | Great Barrier Reef ≈ 2,300 km of aragonite/calcite reef | GBRMPA. The counter is labelled as collapse spreading, not calcium leaving gradually. |
| 20 | X-ray time ×12 | 5 story-seconds over 60 screen-seconds (0:07 → 1:07) | Internal consistency. |
| 21 | Twist rule | every calcium atom reappears at the coordinates it vanished from; bodies have folded, so a skeleton's calcium returns about 1 m above the heap (a standing skeleton's mass centre is ~1 m up; a folded heap's is ~0.2 m) | **Our in-world rule**, stated on screen in the false-resolution line. What lone calcium would do chemically (it would be reactive metal, not bone mineral) is left out; "white = calcium" is our visual rule. |
| 22 | End fact | 99% in bones and teeth; the rest includes the Ca²⁺ that triggers each heartbeat | NIH ODS; physiology texts. "Triggers" chosen over "starts" (the pacemaker cycle begins with a Na⁺ current) and "powers". |

## Build notes (producibility)

- **Gate first.** `whatif/XrayFigure` is the critical path. It must pass a 10-second gate render (PLAN rule) on the Spark before any other new asset is built: shots 4 + 5 + 8 (hands wobble, queue sway, staggered fold).
- **whatif/XrayFigure.** A joint chain reusing `explainer/You`'s joint layout (figure.ts), so the daylight queue at 0:00–0:05.5 lines up with the skeletons at the scan. Props: `view: hands | body`, `bend` track (finger/limb curvature), `sway` track (arm flop + torso sway, sine), `slump` 0..1 track interpolating stand → heap keyframe poses (no physics), `glow` 0..1 (white bone fill), `heart` {bpm, stopAt}, `ghost: true` + `offsetY` + `ghostFall` (twist), `timeOffset` for the stagger. Stylised line art only.
- **whatif/Hud** (standardised name; 6 other backlog scripts use it): props `t0` (global start of the scene), `lines` {L, T, S1, S2} as segment lists `{from, to, text, track?, decimals?, thousands?, color?}` exactly as in the HUD state table, `chip` state, `opacity` track (40% during the white-out), mono font with tabular-nums. Placed at x ≥ 70, y ≥ 250 (inside SAFE_AREA top 230 / left 70).
- **Fonts.** Core bundles only Montserrat and Anton. Install `@fontsource/source-serif-4` (400/600/700 + 600 italic) and `@fontsource/jetbrains-mono` (500/700) with npm **on the Spark**, import them in `studio/src/core/fonts.ts` and add them to the `waitForFonts` load list. Shared with friction-off and the other whatif scripts.
- **Captions.** Drawn as whole-sentence `text` layers (core captions disabled: `maxWords` is capped at 6 and core captions are uppercase Montserrat with pop). Style: Source Serif 4 italic 600, 62 px, white, soft shadow, max width 860 px, 2 lines max, centre y = 1400 so the block clears SAFE_AREA bottom (1920 − 440 = 1480). No pop, no highlight. Core `TextLayer` has no font-style field yet: add `italic: boolean` (maps to CSS font-style) in schema.ts and layers.tsx; the storyboard already sets `italic: true` on every caption (zod strips it until then, so it still validates).
- **explainer/Map edits (~25 lines in ui.tsx MapView).** Add `dots: [{lon, lat, at, out, r, color}]` drawn as small circles that fade in at `at` and out at `out`, and a `strokeColor` prop for the land outline (now hard-coded #4f8a80). Use the existing `landColor`. Shot 13 is a flat world view at zoom 1 (the map is equirectangular; no globe).
- **Particles.** No pigeons, no shell particles, no core `particles` with gravity. The Colosseum's pour is a seeded grain system (≤ 500 grains) plus a growing mound path inside `whatif/Colosseum`. The only core `particles` layer is the white-out dust (preset `dust`, 300).
- **whatif/Colosseum.** Parametric arcade (3 tiers × N arches from one arch path + attic + broken right edge). Props: `mode: day | xray`, `glow` track, `sag` track (util.ts warp), `pour` track (grains + mound), `sandFront` track (metres from the wall, mapped to screen x with the queue at 40 m), `ghost: true` (white full facade floating over the mound). Simple elevation of a real landmark; no photo reference copied.
- **whatif/Statue.** One asset: a generic marble bust (not a real artwork) on a granite plinth, standing beside the queue from 0:00. Props `mode`, `glow`, `melt` 0..1 (warp + drips), `ghost`. Used in shots 1, 2, 6 and 20.
- **whatif/Strata** (Cliff + Peak merged): `profile: cliff | peak`, `bands` [{fromM, toM, label, style: solid | dotted | half}], `fossils`, `crumble` track. Rulers are `explainer/DepthMeter` (`window`, `suffix: " M"`, depth track), not HeightChart.
- **X-ray-only assets.** ConcreteSection, House and Strata are drawn in X-ray mode only. Only Colosseum, Statue and the queue need a daylight mode, and the daylight queue is plain `explainer/You`.
- **No extra components.** White-out = core rect + particles with opacity keyframes. End card = `whatif/TitleCard` with a `fact` prop. Pie chip = an `svg` wedge + `explainer/Stat`. ECG line, bone glyph and scan line are inline `svg`/`rect` layers. Cut from the earlier draft: souvenir cart, pigeons, isolated travertine block, seashells, Skyline with rebar.
- **Render cost.** Cap per-frame SVG nodes (grains ≤ 500, carbonate dots ≤ 60, reef dots ≤ 80) to stay inside Remotion `--concurrency=4` on the Spark CPU. 2,520 frames at 30 fps.
- **Audio.** The bed runs 0:00–1:14.3, then the end-card tail; no mid-video silence edit. A calm bed for 0:00–0:07 and the end card does not exist yet in `studio/public/music` (only deep_ocean, documentary_pulse, dread, tension_pulse); use `documentary_pulse` at low volume until one is added. Every SFX cue above exists in `studio/public/sfx`.
- **Content.** Every body beat is stylised cyan line art: no blood, no faces in pain; heaps read as folded skeleton outlines, ghosts as white powder. Real places are drawn as simple silhouettes and map outlines only. Storyboard: `storyboard.json` next to this file, generated by `gen_storyboard.py`.
