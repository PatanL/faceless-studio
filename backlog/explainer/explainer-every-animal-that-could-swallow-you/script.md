---
slug: explainer-shoulder-test
folder_slug_legacy: explainer-every-animal-that-could-swallow-you   # backlog path kept so links don't break; promote to episodes/explainer-shoulder-test/
niche: explainer
format: long
aspect: "16:9"
working_title: "Could Any Ocean Giant Actually Swallow You? (The Shoulder Test)"
title_options:   # full ranked list with reference patterns: titles.md
  - "Could Any Ocean Giant Actually Swallow You? (The Shoulder Test)"
  - "We Held a Ring the Width of Your Shoulders Up to Six Ocean Giants"
  - "Only One Throat in the Ocean Might Fit You (Nobody's Measured It)"
title_formula: "Question-form H2 (title as a test on you) + parenthetical qualifier, the shape of SWALLOW's '(Only One Actually Can)' turned into our own device name; answers 'no, but…' honestly"
target_runtime_s: 594.2        # 9:54.2, measured: Kokoro am_michael 0.96 per line on the Spark CPU + planned pauses (timeline.json)
target_runtime_range_s: [540, 600]
vo_source: vo_lines.json       # one entry per spoken line with its pause; timing.py turns durations.json into timeline.json
tts_read: "Kokoro am_michael, speed 0.96: 162 wpm speech-only. Pauses after lines 0.15 s, after micro-loop questions 0.35 s, after punch lines 0.5-0.55 s, after verdict stamps 0.65 s"
target_words_per_min: 153      # 1,519 VO words / 9.90 min overall (SWALLOW 145, SPERM 168; PLAYBOOK long 160-170 is a speech rate: ours 162)
hook_words: 23                 # 7.6 s (0:00.2-0:07.8); "you" is word 1; PLAYBOOK short-hook mode <= 25 words / <= 10 s
board_on_screen_s: 36.2        # empty board slides in under the gauge rule (R5)
first_rung_s: 44.8             # "#6 BLUE WHALE" card; PLAYBOOK §8/§10 long-form target <= 45 s
pacing_measured:               # python3 timing.py
  sentences: 161
  avg_sentence_words: 9.4      # SWALLOW 9.3-10.7; punch lines every 8-15 s; a few setup sentences joined (R2, R5, B10)
  you_pct_of_sentences: 27     # target >= 25%
  you_pct_of_words: 3.0        # target >= 3%
  numbers_per_min: 6.2         # digits + number words; high because the gauge is numeric (SWALLOW 6.4). Every number has an object or the gauge
  structural_unit_s: 70        # a new numbered giant every 58-90 s
  verbal_rehook_s: 22          # see the re-hook map
  visual_hold_max_s: 3.0       # scripts/check_storyboards.py on storyboard.json
references:
  - id: JkAcCdqYJN0
    short: SWALLOW
    url: https://www.youtube.com/watch?v=JkAcCdqYJN0
    views: 332151
    outlier_score: 15.82
    why_chosen: "Closest premise (animals judged on whether a throat passes you). We borrow structure only: one metric stamped on every rung, a record that is declared, broken and retired, a could-vs-has distinction before the last answer, a one-breath recap. We deliberately do NOT follow its order or anecdote framing: our test is a physical gauge with a number for every rung, our ladder is presentation-by-fame with board-by-number (sawtooth), the humpback cases are one composite sentence led by the gauge, the whale shark opens on bomb carbon and a POV from inside the sieve, and our 'has' answer is our rubbish, not an animal."
  - id: fGcgWaswMns
    short: SPERM
    url: https://www.youtube.com/watch?v=fGcgWaswMns
    views: 2307237
    outlier_score: 14.65
    why_chosen: "House voice and visual grammar (dark-teal ocean, scale bars vs buses, stick-figure YOU, kicker words) and five devices: rivals conceded first, rhetorical questions answered in 1-3 words, one honest 'never proven' admission, an escalating re-immersion at ~45%, and the reassurance flip + villain swap after the peak."
  - id: nAWpLtG-kNs
    short: ERAS
    url: https://www.youtube.com/watch?v=nAWpLtG-kNs
    views: 12209257
    outlier_score: 113.57
    why_chosen: "Highest-outlier ladder. We borrow the hook -> teasers -> rules -> empty board order, teasers paid in order, the 'just you, no tools' rule turned around at the end, the sawtooth verdict curve, the peak declared one item early, and the finished board held as comment bait."
device_sources:   # single devices only, cited in the table
  - {id: VtrcKTkhDHU, short: ORCA, views: 8289332, outlier_score: 318.82, device: "withheld identity (0:08); myth-bust on the famous name (1:21)"}
fact_file: "section 'Fact sheet' at the bottom; every figure is the most generous one we found, hedged in the VO, with its source"
music: "deep_ocean (0:00-4:28) · documentary_pulse under rungs #3-#2 (4:28-6:57) · deep_ocean low, no jokes, for #1 (6:57-8:18) · dread from the twist (8:18-9:21, grade drops with it) · deep_ocean for the board and bookend"
post_caption_cta: "Which ocean giant should we hold the ring up to next?"
---

# Could Any Ocean Giant Actually Swallow You? (The Shoulder Test)

**Premise (one line):** Six ocean giants get one test: a red ring the width of your shoulders (about 45 cm, a party-size pizza box), held against the most generous throat estimate anyone gives. A board ranks them by that number. Nothing living clears the line, the one throat that might has never been measured and never been caught with a person in it, and the only thing on the board that has really gone down a throat that size is our rubbish.

**Engine:** PLAYBOOK §1a ladder variant. Hook H2 restated as a question on you, then ERAS's open order (hook → teaser contract → rules → empty board, all by 0:45). Two axes (§4): **the gauge number** (board order: 10 → 15 → 35 → 38 → ~40* → ? → our rubbish) × **how we know** (estimate → published figure → real engulfings → no measurement at all → a real stomach). Presentation runs by fame (biggest animal first), the board runs by number, so the verdict curve is a sawtooth: the blue whale sets the bar at 35, the next two fall under it, then the climb resumes with a declared record (humpback), a record with an asterisk (grouper), and the gauge retired (sperm whale). Twist (§5): could vs has, answered by a villain swap and the opening rule turned around ("nothing in your hands or pockets, no gear" ↔ 100 kg of rope and net, two flip-flops).

**What is ours, not borrowed:** the shoulder gauge (red ring, front-view YOU at true scale, pizza-box unit), the "most generous estimate" rule, the cm board with a red line, the 40 cm plant for smaller adults, the lineup's devices (bomb-carbon open, POV from inside the whale shark's sieve, the Zuiyo-maru rot that shows how little throat there is, the 1955 Azores squid, the anatomist's 18 m caveat), the rubbish column above the line, every line of wording.

**Board (`THE SHOULDER GAUGE`):** a cm ruler 0-60 with a solid red line at 45 (YOUR SHOULDERS), dashed lines at 40 (SMALLER ADULTS), 16 (YOUR HEAD) and 9 (YOUR FIST). One column per giant, sorted left to right by its number: a solid part for the usual estimate and a dashed cap up to the most generous one (dashed yellow = estimate only, dashed grey `?` = no measurement). It is built from core rect/text layers (no new component). Final order: basking shark ~10 · whale shark ≤15 · blue whale ≤35 · humpback ≤38 (RECORD) · goliath grouper ~40* · sperm whale ? · OUR RUBBISH (above the line, ~100 KG, HAS).

## Beat alignment table

Percentages are of the measured 594.2 s runtime.

| Our beat | Our timestamp | Reference id + timestamp | Device borrowed | How we adapt it |
|---|---|---|---|---|
| L1 Hook | 0:00.2-0:07.8 (0-1%) | JkAcCdqYJN0 @0:00 (title restated as an action on "you", scope + qualifier, 14 words) | H2 short hook | 23 words, "you" is word 1, and the hook names the test ("one test your shoulders have to pass"). The red ring snaps onto YOU in frame 1, so the test is seen before it is explained |
| L1 Teaser contract | 0:08.1-0:18.8 (1-3%) | nAWpLtG-kNs @0:07-0:19 (four teasers, most famous last, before the rules) | Teasers as a contract, paid in order | Four statements with one on-screen card per clause, paid at 1:59.7 (20%, bomb carbon), 4:54.6 (50%, the two people), 5:39.7 (57%, "the first one that inhales"), 7:29.7 (76%, "Nothing." the throat nobody has measured) |
| L2 Rivals struck off | 0:19.2 (3%) | fGcgWaswMns @0:29-0:43 (famous rivals conceded, then pivot) | Dismiss the famous threats first | Three words ("Teeth don't count.") over a two-✕ visual; the great white and orca never come back |
| L2 Rules (planted to be turned around) | 0:20.9 (4%) | nAWpLtG-kNs @0:24 ("just you yourself, no tools, no equipment"), paid @15:45-15:47 ("make tools") | Challenge rule planted, used against the premise at the end | "Nothing in your hands or pockets, no gear", paid at 8:59-9:07 when every piece of gear in the video turns out to be inside the whale |
| L2 One metric + a plant | 0:25.6-0:36.0 (4-6%) | JkAcCdqYJN0 @0:14 (a single score stamped on every entry); PLAYBOOK §4 "one planted word, paid twice" | One measurable test on every rung; a throwaway number paid later | A physical gauge (shoulders ~45 cm, a party-size pizza box) instead of a timer; "smaller adults are closer to forty, hold on to that" is paid at 6:22.5 when the grouper estimate lands on 40 |
| L3 Empty board | 0:36.2-0:44.8 (6-8%) | nAWpLtG-kNs @0:31-0:35 (empty tier list before item 1) | Progress device on screen before rung 1 | The empty cm board slides in under the gauge-rule line (no separate reveal beat); first rung card at 0:44.8 (PLAYBOOK ≤ 45 s) |
| R6 Blue whale: famous one first, busted (format-teaching rung, longest) | 0:44.8-1:52.5 (8-19%) | VtrcKTkhDHU @1:21 (myth-bust on the famous name); PLAYBOOK §5 "myth-bust on the famous one" (PLANT #1, ERAS Ice Age @14:53-15:59); fGcgWaswMns @1:06-1:15 (numbers → buses/elephants) | The best-known item is wrong in the popular telling; every number gets an object | We front-load fame on purpose: the biggest animal ever opens the list and tops out at 35 cm. The rung teaches the formula slowly: size → object → 2P scenario → RQ → gauge → mechanism → appetite → verdict stamp |
| R6 Micro-loop | 1:08.2 → 1:10.1 | fGcgWaswMns @1:50 → 1:56 ("what does it eat?" → "Squid.") | Rhetorical question answered in 1-3 words (PLAYBOOK §3 #1) | "So what stops you?" → "The throat." Five more of these, all fresh wording: 3:20.9, 6:09.6 → 6:12.3, 6:22.5, 7:27.6 → 7:29.7, 8:25.2 → 8:29.7 |
| R5 Whale shark: withheld noun + bomb carbon open | 1:52.5-2:11.8 (19-22%) | VtrcKTkhDHU @0:08 (identity withheld, named later); nAWpLtG-kNs teaser 1 paid | Withheld identity as a re-hook; first teaser paid at ~20% | Card reads `#5 ???` until "Meet the whale shark" at 2:11.8; the rung opens on its strangest fact instead of its size |
| R5 POV from inside the sieve | 2:21.6-2:52.4 (24-29%) | PLAYBOOK §1a per-rung step 3 (present-tense 2P scenario, 3-5 actions); fGcgWaswMns @1:12 (object comparison) | 2P scenario + everyday object for the number | Night, boat lights, plankton, "the glow goes dark"; then the view from inside: filter pads, and behind them the throat (a quarter to a cereal bowl, ≤ 15 cm) |
| R6/R5/R4 Sawtooth verdicts | 1:46.5 (18%) · 2:56.9 (30%) · 4:05.4 (41%) | nAWpLtG-kNs @7:12 ("a few months", a high) → @8:34 ("a couple weeks", first drop, 53%) | The ladder breaks after a climb, so placement is not predictable | Fame order vs number order: the blue whale sets the bar at 35; the whale shark drops under it; the basking shark's column first rises past the blue whale on the board (the scariest mouth), hovers, then falls to the floor below the whale shark |
| R4 Gross-out tied to the test | 3:33.8-4:05.4 (36-41%) | PLAYBOOK §1a L5 (most shareable / gross-out fact at 40-45%); JkAcCdqYJN0 @3:44 (gross-out escalation) | Gross-out peak just before the midpoint | The 1977 Zuiyo-maru "sea monster": as a basking shark rots the jaws and gills drop away first, which shows how little throat sits behind that face (~10 cm, sharp bend) |
| Re-immersion that escalates | 4:12.3-4:28.2 (42-45%) | fGcgWaswMns @4:43-4:53 (picture it again, every rung stacked into one scarier image) | Mid-video re-immersion | Not a recap of eliminations: three shadows have passed over you, the three left are different: one has had people in its mouth, one inhales, one has teeth. The board flashes small in the corner as a progress check |
| R3 Humpback: gauge first, record declared | 4:28.2-4:49.4 (45-49%) | JkAcCdqYJN0 @2:56 ("new record" on its running score); nAWpLtG-kNs @14:45 (peak declared one item before the end) | The running metric sets a record | Led by the number (fist → 38 cm stretched, the widest published), declared the record, still short of 45 and of a smaller adult's 40 |
| R3 Real cases, one composite line | 4:49.4-5:06.6 (49-52%) | PLAYBOOK §4 hypothetical → real (PUFFER, SWALLOW) | Hypothetical becomes documented | Told as a consequence of the gauge ("which is why both … lived to tell you"), both cases in one sentence (Cape Cod 2021, Strait of Magellan 2025), no reveal beat, no "what if" framing |
| R2 Grouper: entry by mechanism | 5:39.7 (57%) | fGcgWaswMns @1:42-1:47 ("a humpback filters … a sperm whale grabs") | Mechanism contrast as a turn | "Every giant so far was a strainer. This is the first one that inhales" (the entry line is about the mechanism, not about worry or reality) |
| R2 Gauge: no number, estimate, plant paid | 6:09.6-6:36.5 (62-67%) | fGcgWaswMns @2:58 → 3:01 (RQ → 2-word answer); PLAYBOOK §4 planted number | Micro-loop + payoff of the 0:32 plant | "How wide does that mouth open?" → "Nobody knows." A scaled-up estimate (~40, dashed yellow) lands on the smaller-adult line: stuck at 45, too close to call at 40 |
| R2 Folklore undercut | 6:36.5 (67%) | JkAcCdqYJN0 @5:57 (zero confirmed cases undercuts the scariest build) | Folklore vs record | One plain line, our wording ("We couldn't find a single one that holds up"); the board stamp is "~40*", a record with an asterisk |
| R1 Sperm whale: prey proof | 6:57.0-7:27.6 (70-75%) | fGcgWaswMns @1:56 ("Squid. And not small ones.") | Prey bigger than you as the capacity proof | 1955 Azores: a giant squid recovered nearly whole, ~10 m with tentacles, reported ~180 kg, "more than two of you" |
| R1 The gauge breaks and is retired | 7:27.6-8:00.4 (75-81%) | JkAcCdqYJN0 @6:12 (host refuses to score) and @7:37 (stopwatch put away) | Breaking a learned routine is a re-hook | "What does the ring say?" → "Nothing." No one has measured it; the anatomist's yes needs an 18 m+ bull; then the ring physically drops off-frame ("So you put the ring down") |
| R1 One honest admission | 7:46.8 (79%) | fGcgWaswMns @3:54 ("that idea has never been proven") | Once per video, admit what is unproven | Nobody has watched a sperm whale feed, so even "swallows prey whole" is an educated guess. The other rungs state their ranges plainly |
| R1 Verdict: could vs has | 8:00.4-8:11.7 (81-83%) | JkAcCdqYJN0 @7:30 (could, but never has) | Could/has split before the last answer | "Could the biggest bulls fit you? Possibly. Has one ever? … no reliable case." Column `?` crosses the red line, dashed grey |
| Reassurance flip | 8:11.7 (83%) | fGcgWaswMns @7:05-7:33 (it barely notices you) | Second payoff right after the darkest verdict | "You're not on its menu. You're barely in its way." |
| TWIST: the "has" answer + tone drop | 8:17.4-8:41.8 (84-88%) | fGcgWaswMns @5:00 → 5:04 ("Has it ever …?" → "Yes, once"); @7:52-8:30 (the real danger runs the other way; stomachs with plastic and nets); JkAcCdqYJN0 @8:17-8:27 (muted palette for the real cases) | Question answered "Yes."; villain swap; sober tone saved for the real thing | The board's last slot, above the line, is filled by something that really went down that throat: ~100 kg of rope, net and bags (Harris 2019), "more than you weigh", hedged "built up over time". Grade and music drop here, not at the sperm whale |
| Rule turned around | 8:58.9-9:12.0 (91-93%) | nAWpLtG-kNs @15:45-15:47 (the no-tools rule turned against you) | Opening rule used against the premise | "You went in with nothing in your hands … not even flip-flops. The only gear in this whole video ended up inside the whale." |
| BOOKEND: one-breath recap + finished board | 9:20.4-9:43.8 (94-98%) | JkAcCdqYJN0 @8:37 (every verdict recapped in one breath); nAWpLtG-kNs @16:01-16:05 (finished board held, no outro) | Verdict lines written to be recapped; board held as comment bait | Seven columns pulse as they are named, then the 0:00 tableau returns empty and YOU swims home |
| CTA | 9:43.8-9:54.2 (98-100%) | fGcgWaswMns @9:47 (comment the next creature); JkAcCdqYJN0 @9:07 (joke CTA that calls back the first entry) | One comment prompt + a joke button | "Which giant should we hold the ring up to next?" + a callback to rung #6's "very confusing krill" |

**Re-hook map (spoken turns, ~22 s apart):** 0:03 test named · 0:08 teasers · 0:19 "Teeth don't count." · 0:32 "Hold on to that." · 0:45 #6 card · 1:01 2P scenario · 1:08 "So what stops you?" · 1:26 confusing krill · 1:39 "It won't miss you." · 1:52 "#5 ???" (withheld) · 1:59 bomb carbon · 2:11 "Meet the whale shark" · 2:21 night scenario · 2:32 POV from inside · 2:46 "not a contest" · 3:02 "worst idea yet" · 3:21 "So why don't you end up inside?" · 3:30 speed bump · 3:34 "how little sits behind that face" · 3:47 rot reveal · 4:12 "Now picture the opening again" · 4:21 "The next one has had people in its mouth" · 4:30 "Run the gauge first" · 4:41 record · 4:49 "Which is why…" · 5:13 sock · 5:21 lifeguard · 5:32 piano · 5:39 "first one that inhales" · 6:03 wreck · 6:09 "So how wide…?" → "Nobody knows." · 6:22 "Remember the number…?" · 6:36 folklore · 6:51 asterisk · 6:57 "the one you've been waiting for" · 7:06 "bigger than you" · 7:27 "what does the ring say?" → "Nothing." · 7:47 "here's the honest part" · 7:55 ring put down · 7:60 could/has · 8:11 reassurance · 8:17 "That should be the end." · 8:25 "So has a sperm whale ever…?" → "Yes." · 8:59 "Remember the rules?" · 9:12 villain swap · 9:20 final board.

**Comic deflations (every 25-70 s, each followed by a 0.5-0.55 s pause):** confusing krill 1:26 · "wet, alive and deeply offended" 1:34 · cereal bowl vs pizza box 2:46 · speed bump 3:30 · sandwich and sock 5:13 · lifeguard 5:21 · grand piano with fins 5:32 · the asterisk 6:51 · "barely in its way" 8:11 · the krill callback 9:48. None between 6:57 and 8:11 (the sperm whale is played straight) or between 8:17 and 9:20 (the twist).

**Long loops and plants:** L1 "will your shoulders fit?" (0:03 → board top at 8:29, the "has" answer) · L2 teaser contract (0:08 → 1:59 / 4:54 / 5:39 / 7:29) · L3 the board (0:36 → finished 9:20) · L4 "no gear" rule (0:21 → 8:59) · L5 the 40 cm plant (0:32 → 6:22) · L6 the record (4:41 → asterisk 6:51 → gauge retired 7:55). Smaller plants: buses (0:50 → 7:01 weight), pizza box (0:26 → 2:46 → 9:38), the red ring (0:01 → every gauge → dropped 7:55 → CTA "hold the ring up"), the confusing krill (1:26 → 9:48), the flip-flop (8:47 → 9:02 → 9:12 last image).

## The script

### Hook

- **First line (0:00.2):** "You're about to be fed to six ocean giants."
- **First visual (frame 1):** The stick-figure YOU floats under a bright surface, arms out. Six dark silhouettes (blue whale, whale shark, basking shark, humpback, grouper, sperm whale) circle at three depths. On "giants" a red ring snaps tight around YOU's shoulders with a click.

### Voiceover / captions with timestamps

Generated by `timing.py --md` from `vo_lines.json` and the Kokoro durations measured on the Spark (am_michael, speed 0.96, CPU). Line starts include the planned pauses (0.15 s after a line, 0.35 s after a micro-loop question, 0.5-0.55 s after a punch line, 0.65 s after a verdict stamp). Captions are the VO, word by word, with Kokoro word timings (storyboard `captions.words`). ON SCREEN is the kicker (Headline, top centre, white caps, red accent word).

<!-- GENERATED:VO -->
#### [L1 HOOK] 0:00.2

- **H1 · 0:00.2–0:03.1** You're about to be fed to six ocean giants.  
  ON SCREEN: `SIX GIANTS. ONE OF YOU.`
- **H2 · 0:03.2–0:07.8** There's one test your shoulders have to pass: will they fit down the throat?  
  ON SCREEN: `DO YOUR SHOULDERS FIT?`

#### [L1 TEASERS] 0:08.1

- **T1 · 0:08.1–0:18.8** On the way: a fish dated by nuclear bombs, a whale that has held people in its mouth, a fish that inhales sharks, and one throat nobody has measured.  
  ON SCREEN: `BOMB-DATED · PEOPLE IN ITS MOUTH · INHALES SHARKS · NEVER MEASURED`

#### [L2 RULES] 0:19.2

- **R1 · 0:19.2–0:20.6** Teeth don't count.  
  ON SCREEN: `GREAT WHITE ✕  ORCA ✕`
- **R2 · 0:20.9–0:25.5** The rules: just you, nothing in your hands or pockets, no gear.  
  ON SCREEN: `JUST YOU · NO GEAR`

#### [L2 GAUGE] 0:25.6

- **R3 · 0:25.6–0:32.1** Across the muscle, your shoulders are about forty-five centimetres: a party-size pizza box.  
  ON SCREEN: `~45 CM ≈ PARTY-SIZE PIZZA BOX`
- **R4 · 0:32.2–0:36.0** Smaller adults are closer to forty. Hold on to that.  
  ON SCREEN: `SMALLER ADULTS ~40 CM`

#### [L3 BOARD] 0:36.2

- **R5 · 0:36.2–0:44.4** To pass, a throat must open wider than this red ring, and every giant gets the most generous estimate we could find.  
  ON SCREEN: `PASS = WIDER THAN THE RING · THE SHOULDER GAUGE`

#### [R6 BLUE WHALE] 0:44.8

- **B1 · 0:44.8–0:49.8** Number six: the biggest animal known to have ever lived. The blue whale.  
  ON SCREEN: `#6 BLUE WHALE`
- **B2 · 0:50.0–0:54.7** Around thirty metres. That's two and a half school buses, nose to tail.  
  ON SCREEN: `~30 M ≈ 2.5 BUSES`
- **B3 · 0:54.9–1:01.1** One lunge can take in more water than the whale itself weighs, and you'd be one small part of it.  
  ON SCREEN: `1 GULP > ITS OWN WEIGHT`
- **B4 · 1:01.2–1:08.0** So you're floating at the surface. A shadow rises under you, the jaw drops, and you go in with the water.

#### [R6 GAUGE] 1:08.2

- **B5 · 1:08.2–1:09.7** So what stops you?  
  ON SCREEN: `WHAT STOPS YOU?`
- **B6 · 1:10.1–1:11.1** The throat.  
  ON SCREEN: `THE THROAT`
- **B7 · 1:11.6–1:16.0** Most estimates put it somewhere between a grapefruit and a dinner plate.  
  ON SCREEN: `GRAPEFRUIT → DINNER PLATE`
- **B8 · 1:16.2–1:22.3** The widest claim out there is a small beach ball, about thirty-five centimetres. We'll take it.  
  ON SCREEN: `WIDEST CLAIM: ~35 CM`
- **B9 · 1:22.5–1:25.7** Your shoulders still win by more than a hand's width.  
  ON SCREEN: `35 vs 45`

#### [R6 MECHANISM] 1:26.2

- **B10 · 1:26.2–1:33.9** The whale pushes the water out through its baleen and keeps the krill, and you are a very large, very confusing krill.  
  ON SCREEN: `BALEEN`
- **B11 · 1:34.4–1:38.9** Out you go with the seawater. Wet, alive and deeply offended.

#### [R6 APPETITE] 1:39.5

- **B12 · 1:39.5–1:46.4** And it won't miss you. In feeding season it eats about sixteen tonnes of krill a day, ten cars' worth.  
  ON SCREEN: `~16 T / DAY ≈ 10 CARS`

#### [R6 VERDICT] 1:46.5

- **B13 · 1:46.5–1:51.8** Biggest animal ever, and it tops out at thirty-five. Size isn't your problem.  
  ON SCREEN: `BLUE WHALE · ~35 CM AT MOST`

#### [R5 WHALE SHARK] 1:52.5

- **W1 · 1:52.5–1:55.7** Number five comes with a strange birth certificate.  
  ON SCREEN: `#5 ???`

#### [R5 BOMB CARBON] 1:56.0

- **W2 · 1:56.0–1:59.5** For decades nobody could tell how old these fish get.
- **W3 · 1:59.7–2:08.2** Then, in 2020, researchers dated the rings in their spines using carbon that Cold War bomb tests left in the sea.  
  ON SCREEN: `2020 · BOMB CARBON`
- **W4 · 2:08.4–2:11.5** One of them had been alive for about fifty years.  
  ON SCREEN: `~50 YEARS`

#### [R5 WHALE SHARK] 2:11.8

- **W5 · 2:11.8–2:21.5** Meet the whale shark. No fish alive is bigger: it grows to about eighteen metres, with a mouth a metre and a half wide, almost your height.  
  ON SCREEN: `#5 WHALE SHARK · MOUTH ~1.5 M`

#### [R5 SCENARIO] 2:21.6

- **W6 · 2:21.6–2:31.4** It's night. You're floating under a boat's lights, where the plankton gathers, and the shark rises into the glow, mouth open. Then the glow goes dark.

#### [R5 GAUGE] 2:31.7

- **W7 · 2:31.7–2:39.3** From inside, the view is a sieve: spongy filter pads in front of the gills, and somewhere behind them, the throat.
- **W8 · 2:39.5–2:45.7** Estimates for it run from a quarter to a cereal bowl, fifteen centimetres at the very most.  
  ON SCREEN: `THROAT ≤ ~15 CM ≈ A CEREAL BOWL`
- **W9 · 2:45.8–2:51.9** A cereal bowl against a pizza box. That's not a contest, it's a misunderstanding.

#### [R5 EXIT] 2:52.4

- **W10 · 2:52.4–2:56.6** The water leaves through the gills, and you leave the way you came in.

#### [R5 VERDICT] 2:56.9

- **W11 · 2:56.9–3:02.1** Fifteen centimetres, nowhere near you. It drops in under the blue whale.  
  ON SCREEN: `WHALE SHARK · ≤15 CM`

#### [R4 BASKING SHARK] 3:02.7

- **K1 · 3:02.7–3:06.9** Number four looks like the worst idea yet. The basking shark.  
  ON SCREEN: `#4 BASKING SHARK`
- **K2 · 3:07.1–3:15.0** The second-biggest fish in the sea cruises for hours with its mouth open a metre wide, wide enough for you to swim into.  
  ON SCREEN: `MOUTH ~1 M`
- **K3 · 3:15.2–3:20.7** It strains about two million litres of water an hour, most of an Olympic pool.  
  ON SCREEN: `~2,000,000 L / HOUR`

#### [R4 RQ] 3:21.0

- **K4 · 3:21.0–3:23.1** So why don't you end up inside?  
  ON SCREEN: `SO WHY NOT YOU?`

#### [R4 MECHANISM] 3:23.4

- **K5 · 3:23.4–3:30.0** It doesn't gulp or suck. It swims with the door open, and the door is a comb of gill rakers.
- **K6 · 3:30.2–3:33.3** Drift in and you're not food. You're a speed bump.  
  ON SCREEN: `SPEED BUMP`

#### [R4 GROSS-OUT] 3:33.9

- **K8 · 3:33.9–3:47.3** Here's how little sits behind that face. In 1977 a Japanese trawler hauled up a rotting carcass off New Zealand: long neck, four flippers. The papers called it a sea monster.  
  ON SCREEN: `1977 · SEA MONSTER?`
- **K9 · 3:47.4–3:56.6** Tissue tests said basking shark. As one rots, the jaws and gills drop away first, leaving something that looks like a dinosaur.  
  ON SCREEN: `IT WAS A SHARK`

#### [R4 GAUGE] 3:56.7

- **K10 · 3:56.7–4:05.3** Take away that mouth and there isn't much throat. One old museum account puts it at about ten centimetres, with a sharp bend.  
  ON SCREEN: `THROAT ~10 CM + A BEND`

#### [R4 VERDICT] 4:05.5

- **K11 · 4:05.5–4:11.7** The scariest mouth on the list, and it ends up at the very bottom, below even the whale shark.  
  ON SCREEN: `BASKING SHARK · ~10 CM`

#### [RE-IMMERSION] 4:12.4

- **X1 · 4:12.4–4:16.2** Now picture the opening again: just you, and six shadows.
- **X2 · 4:16.4–4:21.1** Three have already passed over you. The three still circling are different.
- **X3 · 4:21.3–4:27.7** The next one has had people in its mouth. The one after that inhales. And the last one has teeth.

#### [R3 HUMPBACK] 4:28.3

- **U1 · 4:28.3–4:30.2** Number three. The humpback.  
  ON SCREEN: `#3 HUMPBACK`

#### [R3 GAUGE] 4:30.4

- **U2 · 4:30.4–4:35.8** Run the gauge first. A humpback's throat is normally about the size of your fist.  
  ON SCREEN: `THROAT ≈ YOUR FIST`
- **U3 · 4:36.0–4:41.4** Stretched for a big meal, the widest figure published is about thirty-eight centimetres.  
  ON SCREEN: `STRETCHED: ~38 CM`
- **U4 · 4:41.6–4:48.9** The widest throat yet, and still most of a hand short. Even a smaller adult, at forty, doesn't go down.  
  ON SCREEN: `NEW RECORD · STILL SHORT`

#### [R3 REAL CASES] 4:49.4

- **U5 · 4:49.4–4:54.5** Which is why both people known to have been inside one lived to tell you about it.
- **U6 · 4:54.6–5:06.4** A diver hunting lobster off Cape Cod in 2021, and a kayaker in the Strait of Magellan in 2025. Each was back in open water within a minute.  
  ON SCREEN: `2021 · CAPE COD  /  2025 · CHILE`

#### [R3 MECHANISM] 5:06.6

- **U7 · 5:06.6–5:13.5** Humpbacks lunge through schools of fish with their mouths wide open, and now and then, you're one of the fish.
- **U8 · 5:13.6–5:21.1** Biologists call that engulfed, not swallowed. It's the whale version of biting a sandwich and finding a sock.  
  ON SCREEN: `ENGULFED ≠ SWALLOWED`

#### [R3 VERDICT] 5:21.4

- **U10 · 5:21.4–5:27.1** Thirty-eight centimetres, the record so far. A lifeguard with a very large mouth.  
  ON SCREEN: `HUMPBACK · ~38 CM · RECORD`

#### [R2 GROUPER] 5:27.7

- **G1 · 5:27.7–5:32.0** Number two is smaller than anything yet. The goliath grouper.  
  ON SCREEN: `#2 GOLIATH GROUPER`
- **G2 · 5:32.2–5:39.2** Up to about two and a half metres and around three hundred and sixty kilos. A grand piano with fins.  
  ON SCREEN: `~360 KG ≈ A GRAND PIANO`

#### [R2 MECHANISM] 5:39.8

- **G3 · 5:39.8–5:46.7** Every giant so far was a strainer. This is the first one that inhales, and you're right in front of it.  
  ON SCREEN: `IT INHALES`
- **G4 · 5:46.8–5:55.8** It flares its mouth so fast that the water rushes in, and so does whatever is in front of it: lobsters, fish, turtles, sharks.

#### [R2 PROOF] 5:56.0

- **G5 · 5:56.0–6:03.3** Off southwest Florida, an angler filmed one take a hooked blacktip shark more than a metre long in a single gulp.  
  ON SCREEN: `SHARK ~1.2 M · ONE GULP`

#### [R2 SCENARIO] 6:03.6

- **G6 · 6:03.6–6:09.4** So you're drifting over a wreck. Something the size of a sofa slides out from under the hull.

#### [R2 RQ] 6:09.6

- **G8 · 6:09.6–6:12.0** So how wide does that mouth open?  
  ON SCREEN: `HOW WIDE?`
- **G9 · 6:12.3–6:13.6** Nobody knows.  
  ON SCREEN: `NO PUBLISHED NUMBER`

#### [R2 GAUGE] 6:14.1

- **G10 · 6:14.1–6:22.3** No one has published a gape for a giant one. Scale up a smaller grouper and you get about forty centimetres, and that's a guess.  
  ON SCREEN: `~40 CM (ROUGH ESTIMATE)`
- **G11 · 6:22.5–6:25.5** Forty. Remember the number you were holding on to?
- **G12 · 6:25.8–6:36.3** At forty-five, you go in head first until your shoulders hit the corners of the jaw, and everything stops. At forty, on paper, it's too close to call.  
  ON SCREEN: `45: STUCK · 40: TOO CLOSE TO CALL`

#### [R2 FOLKLORE] 6:36.6

- **G13 · 6:36.6–6:43.8** Dive boats are full of stories about groupers swallowing people like you. We couldn't find a single one that holds up.  
  ON SCREEN: `STORIES THAT HOLD UP: 0`

#### [R2 SEAM] 6:43.9

- **G14 · 6:43.9–6:51.3** Their real problem is us. They were fished so hard that the United States banned harvesting them in 1990.  
  ON SCREEN: `1990 · HARVEST BAN`

#### [R2 VERDICT] 6:51.5

- **G15 · 6:51.5–6:56.4** Forty, give or take a lot. It edges past the humpback, with an asterisk.  
  ON SCREEN: `GROUPER · ~40 CM*`

#### [R1 SPERM WHALE] 6:57.0

- **S1 · 6:57.0–7:00.7** Number one. The one you've been waiting for. The sperm whale.  
  ON SCREEN: `#1 SPERM WHALE`
- **S2 · 7:00.9–7:05.8** Up to about sixteen metres and forty tonnes, three school buses' worth.  
  ON SCREEN: `~16 M · ~40 T ≈ 3 BUSES`

#### [R1 PREY] 7:05.9

- **S3 · 7:05.9–7:11.3** And unlike everything so far, it hunts things bigger than you. Giant squid.  
  ON SCREEN: `PREY BIGGER THAN YOU`
- **S4 · 7:11.6–7:21.6** In 1955, whalers off the Azores found a giant squid inside one, nearly whole, about ten metres long with its tentacles.  
  ON SCREEN: `1955 · AZORES · ~10 M SQUID`
- **S5 · 7:21.8–7:27.2** Its weight was reported at around a hundred and eighty kilos. More than two of you.  
  ON SCREEN: `~180 KG (REPORTED) ≈ 2+ OF YOU`

#### [R1 GAUGE] 7:27.6

- **S6 · 7:27.6–7:29.4** So, what does the ring say?
- **S7 · 7:29.7–7:30.6** Nothing.  
  ON SCREEN: `NO MEASUREMENT`
- **S8 · 7:31.1–7:40.7** Nobody has measured it. The closest we have is the anatomist Joy Reidenberg, who says a very big adult bull could swallow a person.
- **S9 · 7:40.9–7:46.5** But she means one of eighteen metres or more, bigger than most bulls anyone sees.  
  ON SCREEN: `BIG BULLS ONLY · ~18 M+`

#### [R1 HEDGE] 7:46.8

- **S10 · 7:46.8–7:55.1** And here's the honest part: nobody has ever watched one feed, so even 'it swallows prey whole' is an educated guess.  
  ON SCREEN: `NEVER SEEN FEEDING`

#### [R1 GAUGE RETIRED] 7:55.4

- **S11 · 7:55.4–8:00.0** So you put the ring down. This is the one throat the gauge can't measure.

#### [R1 VERDICT] 8:00.4

- **S12 · 8:00.4–8:08.4** Could the biggest bulls fit you? Possibly. Has one ever? Two centuries of whaling records hold no reliable case.  
  ON SCREEN: `COULD: BIG BULLS  ·  HAS: NEVER`
- **S13 · 8:08.7–8:11.1** Top of the board, with a question mark.  
  ON SCREEN: `SPERM WHALE · ?`

#### [REASSURANCE FLIP] 8:11.7

- **F1 · 8:11.7–8:16.8** And it wouldn't even be trying. You're not on its menu. You're barely in its way.  
  ON SCREEN: `YOU: NOT ON THE MENU`

#### [TWIST] 8:17.4

- **V1 · 8:17.4–8:24.9** That should be the end, and you should be swimming home. But the board still has one empty space, above the line.
- **V2 · 8:25.2–8:29.3** So has a sperm whale ever swallowed something heavier than you?
- **V3 · 8:29.7–8:30.4** Yes.  
  ON SCREEN: `YES.`

#### [TWIST EVIDENCE] 8:31.0

- **V4 · 8:31.0–8:41.7** In 2019, one stranded on the Isle of Harris in Scotland with about a hundred kilos of rope, netting and bags in its stomach. More than you weigh.  
  ON SCREEN: `2019 · SCOTLAND · ~100 KG`
- **V5 · 8:41.8–8:47.1** It built up over time, not in one gulp. But all of it went down that throat.
- **V6 · 8:47.4–8:58.6** A year earlier, one in Indonesia held a hundred and fifteen plastic cups, twenty-five bags and two flip-flops. About six kilos, a bowling ball's worth.  
  ON SCREEN: `115 CUPS · 25 BAGS · 2 FLIP-FLOPS`

#### [RULE CALLBACK] 8:58.9

- **V7 · 8:58.9–9:07.0** Remember the rules? You went in with nothing in your hands and nothing in your pockets. No net, no rope, not even flip-flops.  
  ON SCREEN: `THE RULES: NO GEAR`
- **V8 · 9:07.3–9:11.4** The only gear in this whole video ended up inside the whale.  
  ON SCREEN: `ALL THE GEAR → INSIDE THE WHALE`

#### [VILLAIN SWAP] 9:12.0

- **V9 · 9:12.0–9:19.8** Nothing in the ocean is swallowing people whole. But it is swallowing what people leave behind, one flip-flop at a time.

#### [BOOKEND] 9:20.5

- **E1 · 9:20.5–9:22.0** So, the final board.  
  ON SCREEN: `FINAL BOARD`
- **E2 · 9:22.2–9:38.1** Basking shark, ten centimetres. Whale shark, a cereal bowl. Blue whale, a beach ball at best. Humpback, the record. Grouper, the record with an asterisk. Sperm whale, a question mark. And above the line, our rubbish.
- **E3 · 9:38.5–9:43.3** Six giants, one pizza box of shoulders, and you get to swim home.

#### [CTA] 9:43.9

- **C1 · 9:43.9–9:48.2** Which giant should we hold the ring up to next? Tell us in the comments.  
  ON SCREEN: `NEXT GIANT? ↓`
- **C2 · 9:48.5–9:53.6** Just don't say the blue whale. It's still looking for that very confusing krill.
<!-- /GENERATED:VO -->

### On-screen text (summary)

- **Kickers** (`explainer/Headline`, top centre, white caps, one red word) as listed under ON SCREEN, about one every 4-8 s.
- **The gauge** (core layers, no new component): front-view YOU drawn at true scale (head 16 cm, shoulders 45 cm across the deltoids, hips 36 cm) inside a red 45 cm ring; the throat ring (cyan) grows on the spoken numbers. Both rings are drawn as hoops round the shoulders. Solid = the usual estimate, dashed = the most generous one, dashed yellow = estimate only, flickering `?` = no measurement. Readouts: blue whale 10 → 25 → 35 · whale shark 2.5 → 15 · basking shark ~10 + a drawn bend · humpback 10 → 38 · grouper ~40 (estimate) · sperm whale `?` (ring retired at 7:55).
- **The board** `THE SHOULDER GAUGE`: updates at 1:46.5, 2:56.9, 4:05.4 (hover then fall), 5:21.3, 6:51.4, 8:00.4, 8:17.4 (empty slot above the line pulses), 9:20.4 (finished, each column pulses as named), 9:43.8 (dimmed under the CTA).
- **Number cards** (`Tag`, red): `#6 BLUE WHALE` … `#1 SPERM WHALE`, counting down to the top; #5 shows `#5 ???` until the name.
- **Date stamps:** 2020, 1977, 2021, 2025, 1990, 1955, 2019, 2018.
- **End card:** finished board 9:20.4-9:38.4, bookend tableau, then `NEXT GIANT? ↓` over the dimmed board.

## Shot list

Every shot starts on a VO line id and every beat inside it is anchored to a spoken word in `gen_storyboard.py` (`c.w("B9", "win")`), so a new TTS pass re-times the whole storyboard: `measure_tts.py` (Spark) → `timing.py` → `gen_storyboard.py`. Times below are from the current measured read. Where nothing changes on screen for more than 3 s, the generator adds a small camera punch-in on the next sentence start (max hold 3.0 s).

Kit vocabulary: `studio/src/kits/explainer/README.md`. Existing and used: `Ocean`, `BlueWhale` (`gape`), `SpermWhale` (`teeth`), `GreatWhite` (also the silhouette for the blacktip shark), `Orca`, `ColossalSquid` (`hooks` false, giant-squid stand-in), `WhaleThroat` (pilot 3's 0.34 m ring = the beach-ball figure), `You`, `Diver`, `Bus`, `Car`, `Options`, `ScaleBar`, `Stat`, `Map` (zoom ≤ 3, ring markers, no coastline close-ups), `DepthMeter`, `Headline`, `Tag`. **New figures (4, marked \*):** `WhaleShark` (18 m, `jaw`), `BaskingShark` (10 m, `jaw` with gill arches and raker comb, `rot` 0..1 fading the lower jaw, gills and fins), `Humpback` (15 m, `pleats`, `pose: "lunge"`), `GoliathGrouper` (2.5 m, `flare`). All side views facing right; head-on moments use the open jaw plus a vertical `ScaleBar`. Megamouth and leatherback are cut. **No new UI components:** the gauge, the board, the front-view YOU and every prop (pizza box, cereal bowl, grapefruit, plate, beach ball, fist, vertebra rings, mushroom icon, boat lights, sieve, raker comb, pool, carcass, newspaper, sandwich, piano, wreck, speech bubble, hook, stomach cutaway, net ball, debris set: cup/bag/flip-flop/bowling ball/scale) are core rect/circle/text/inline-SVG layers written by the generator. Plankton, krill and fish balls are `particles` layers moved with keyframes. YOU is one look: the `You` stick figure in scenes and its front-view gauge drawing for measurements; `Diver` appears only as the 2021 Cape Cod diver. Grade: base teal; the tone drop is its own scene from V1 (saturate 0.4, vignette 0.5, tint) entered through a 1.2 s fade, because grades cannot animate inside a scene. No full-frame white flashes. SFX names are all in `studio/public/sfx/`; music beds in `studio/public/music/`.

<!-- GENERATED:SHOTS -->
| # | Starts on (VO line) | t_start | t_end | Shot type | Visual (kit vocabulary; * = new figure) | Camera | SFX |
|---|---|---|---|---|---|---|---|
| 1 | H1 "You're about to be…" | 0:00.0 | 0:08.0 | Hook wide | `explainer/Ocean` surface 0.12; `You` floats under the surface; six silhouettes (BlueWhale, WhaleShark*, BaskingShark*, Humpback*, GoliathGrouper*, SpermWhale) circle on 3 parallax depths; red 45 cm ring snaps round YOU's shoulders on "giants"; kicker | slow push-in 1.0→1.08 | underwater_rumble bed; click on ring snap |
| 2 | T1 "On the way: a…" | 0:08.0 | 0:19.1 | Teaser contract | 4 cards, one per clause, each a 1.05 push: vertebra rings + mushroom icon (BOMB-DATED) · humpback mouth + tiny YOU (PEOPLE IN ITS MOUTH) · grouper flare + shark silhouette (INHALES SHARKS) · sperm whale head with a `?` throat ring (NEVER MEASURED) | cut per clause | whoosh per card; stinger on "measured" |
| 3 | R1 "Teeth don't count.…" | 0:19.1 | 0:20.7 | Strike-off | `GreatWhite` and `Orca` side by side (`pxPerM` 40); red ✕ stamps; kicker TEETH DON'T COUNT | slight pan L→R | impact ×2 |
| 4 | R2 "The rules: just you,…" | 0:20.7 | 0:25.5 | Rules card | `Options` title RULES, items JUST YOU / NOTHING IN YOUR HANDS / NOTHING IN YOUR POCKETS / NO GEAR (itemAt on the words); `You` pose shrug right | static | tick per item |
| 5 | R3 "Across the muscle, your…" | 0:25.5 | 0:32.1 | Gauge reveal | Front-view YOU (inline SVG at true scale: head 16, shoulders 45, hips 36 cm); `ScaleBar` ~45 CM across the shoulders; party-size pizza box slides in under it at the same width | push-in to shoulders | pop; ding on "pizza" |
| 6 | R4 "Smaller adults are closer…" | 0:32.1 | 0:36.0 | Smaller adult | A dashed 40 cm YOU outline slides in beside the 45 cm one; kicker SMALLER ADULTS ~40 CM; on "hold" a small `40` pin tag drops into the corner and stays for the rest of the setup (the plant paid at G11) | static | pop; click on "hold" |
| 7 | R5 "To pass, a throat…" | 0:36.0 | 0:44.7 | Gauge rule + empty board | Red ring grows round the front-view YOU ("PASS = WIDER THAN THE RING"), then on "estimate" the empty board slides in over it: a cm ruler with the red 45 line, dashed 40 / head 16 / fist 9 lines, seven empty slots | pull-out | riser short; whoosh_long on the board |
| 8 | B1 "Number six: the biggest…" | 0:44.7 | 0:49.8 | Size | `Tag` #6 BLUE WHALE; `BlueWhale` `pxPerM` 45 crossing frame; `ScaleBar` ~30 M | slow pan following the whale | underwater_rumble swell |
| 9 | B2 "Around thirty metres. That's…" | 0:49.8 | 0:54.7 | Scale compare | 2.5 × `Bus` nose to tail under the whale at the same `pxPerM`; kicker ~30 M ≈ 2.5 BUSES | static | pop ×3 on the buses |
| 10 | B3 "One lunge can take…" | 0:54.7 | 1:01.1 | Lunge | `BlueWhale` `gape` 0→1 (jaw drop, pleated pouch balloons); kicker 1 GULP > ITS OWN WEIGHT; a tiny YOU dot rides the inflow | push-in on the jaw | whoosh_long, bubbles |
| 11 | B4 "So you're floating at…" | 1:01.1 | 1:08.1 | 2P scenario | `You` at the surface (`surface` 0.2); a BlueWhale silhouette rises from below; on "drops" the jaw opens (`gape`), on "in" YOU slides into the mouth and the frame dips to the dark mouth interior | camera drops with YOU; shake 0.3 s on the gulp | underwater_rumble, bubbles, whoosh |
| 12 | B5 "So what stops you?…" | 1:08.1 | 1:11.4 | Micro-loop | Dark mouth interior; kicker WHAT STOPS YOU? → on "throat" cut to `WhaleThroat` close-up (throat ring ~0.34 m) | slow push | heartbeat_slow; ding on "throat" |
| 13 | B7 "Most estimates put it…" | 1:11.4 | 1:26.0 | Gauge #6 | Front-view YOU + red 45 ring; cyan throat ring grows grapefruit → plate (solid, 10→25 cm) then a yellow dashed cap to 35 cm as a small beach ball pops in; icons grapefruit/plate/ball beside; kicker 35 vs 45 | static, slight push on "win" | tick on each icon, sonar_ping on the ring, impact soft on "win" |
| 14 | B10 "The whale pushes the…" | 1:26.0 | 1:39.3 | Baleen flush | BlueWhale close-up, `gape` 1; baleen curtain; `Krill` particles stay while the water arrows (svg) push out; YOU tumbles out the side (pose panic → shrug), drip lines; kicker BALEEN | slight pan; shake 0.2 s at the exit | whoosh, bubbles; pop on "offended" |
| 15 | B12 "And it won't miss…" | 1:39.3 | 1:46.4 | Appetite | `Stat` 16 suffix " TONNES / DAY" count-up; a row of 10 `Car`s; tiny YOU at the end labelled ROUNDING ERROR | push-in on the tiny YOU | ding |
| 16 | B13 "Biggest animal ever, and…" | 1:46.4 | 1:52.3 | Verdict #6 | Board: BlueWhale column grows (solid to 25 = most estimates, dashed cap to 35 = widest claim) and stops under the red 45 line; stamp BLUE WHALE · ~35 CM AT MOST | static | impact low; stinger tail |
| 17 | W1 "Number five comes with…" | 1:52.3 | 2:11.7 | Withheld noun + bomb carbon | Kicker #5 ???; vertebra cross-section with growth rings; a red spike ring sweeps through on "Cold War"; small flat mushroom icon top-left (non-graphic); `Stat` ~50 YEARS | push-in to the rings | tick per ring; ding on "fifty" |
| 18 | W5 "Meet the whale shark.…" | 2:11.7 | 2:21.5 | Size | Kicker #5 WHALE SHARK; `WhaleShark`* jaw open, `ScaleBar` ~1.5 M (vertical) across the mouth with YOU standing beside it (1.75 m) | pull-out from the mouth | whoosh |
| 19 | W6 "It's night. You're floating…" | 2:21.5 | 2:31.6 | 2P night scenario | Night surface (`surface` 0.15, dark sky); boat hull + light cone (svg) at top; plankton particles gather in the cone; YOU floats in the glow (no gear); the WhaleShark* rises mouth-open into the cone; on "dark" the frame goes black-red (inside) | slow creep-in; dip to dark | bubbles; underwater_rumble on "rises" |
| 20 | W7 "From inside, the view…" | 2:31.6 | 2:52.3 | Gauge #5 from inside | POV inside the mouth: full-frame sieve (filter pads) with the dark throat hole centre; on "throat" cut to the gauge: front-view YOU + red ring, cyan throat ring grows from a quarter (2.5 cm, solid) to 15 cm (dashed cap); cereal-bowl icon pops; pizza box under YOU; kicker THROAT ≤ ~15 CM ≈ A CEREAL BOWL | push-in on the tiny ring | pop on "bowl", click |
| 21 | W10 "The water leaves through…" | 2:52.3 | 2:56.8 | Exit | The water jets out through the gill slits (arrows); YOU drifts back out of the mouth the way it came in; the WhaleShark* cruises on, unbothered | shake 0.15 s | whoosh, bubbles |
| 22 | W11 "Fifteen centimetres, nowhere near…" | 2:56.8 | 3:02.6 | Verdict #5 (drop) | Board: the blue whale column slides right; the WhaleShark column grows to 15 (solid to 2.5, dashed cap) in slot 1, below it; stamp WHALE SHARK · ≤15 CM | static | whoosh down, impact |
| 23 | K1 "Number four looks like…" | 3:02.6 | 3:20.8 | Face + filter rate | Kicker #4 BASKING SHARK; `BaskingShark`* jaw fully open, gill arches + raker comb visible, `ScaleBar` ~1 M (vertical) on the mouth; then `Stat` 2,000,000 L / HOUR with an Olympic-pool outline filling beside it | slow push into the mouth | underwater_rumble; bubbles loop |
| 24 | K4 "So why don't you…" | 3:20.8 | 3:33.7 | Speed bump | Kicker SO WHY NOT YOU?; YOU drifts into the open mouth, bonks into the raker comb (svg), the shark swerves; `Tag` SPEED BUMP (yellow) | side tracking; bump shake 0.1 s | pop (bonk), whoosh |
| 25 | K8 "Here's how little sits…" | 3:33.7 | 3:47.3 | Sea monster (gross-out) | Night deck kept minimal: newspaper card (svg) with a lumpy long-necked carcass silhouette; `Headline` 1977 · SEA MONSTER? stamp; non-graphic | slow push | drone; stinger on "monster" |
| 26 | K9 "Tissue tests said basking…" | 3:47.3 | 4:05.3 | Rot diagram + gauge | Diagram: BaskingShark* outline; `rot` 0→1 fades the lower jaw, gills and fins; the remains morph to the 1977 carcass outline ("dinosaur"); then the throat: a cyan ~10 cm ring with a sharp bend drawn behind it next to the red 45 ring; kicker THROAT ~10 CM + A BEND | static, then push on the ring | tick; stinger tail |
| 27 | K11 "The scariest mouth on…" | 4:05.3 | 4:12.2 | Verdict #4 (sawtooth drop) | Board: the BaskingShark column first rises past the blue whale (to ~38, "the scariest mouth"), hovers, then falls to 10, below even the whale shark (the others slide right); stamp BASKING SHARK · ~10 CM | static | whoosh down, impact |
| 28 | X1 "Now picture the opening…" | 4:12.2 | 4:28.1 | Re-immersion (escalates) | Exact replay of the 0:00 tableau (same seed); the three strainers already ranked (BlueWhale, WhaleShark, BaskingShark) fade grey with a ✕ on "passed"; the three left (Humpback, GoliathGrouper, SpermWhale) darken to red-black one by one on "people", "inhales", "teeth"; the board flashes small top-right with its 3 columns | slow push-in matching 0:00 | heartbeat_slow; tick ×3; heartbeat on "teeth" |
| 29 | U1 "Number three. The humpback.…" | 4:28.1 | 4:49.2 | Gauge first (#3) | Kicker #3 HUMPBACK; `Humpback`* silhouette top-right; front-view YOU + red ring; a fist icon, then the cyan ring grows from fist (10, solid) to 38 cm (dashed cap) — the closest yet, a yellow NEW RECORD stamp, still inside the red ring | static; slow push on "short" | sonar_ping on the ring; ding + click on "record" |
| 30 | U5 "Which is why both…" | 4:49.2 | 5:06.4 | Real cases (composite) | `Map` Atlantic-wide (zoom ≤ 2): pins Cape Cod (lon -70.2, lat 41.9) "2021" and Strait of Magellan (lon -70.9, lat -53.2) "2025"; per pin a 1 s flat vignette (diver / kayak silhouette in a mouth → back in open water); kicker 2021 · CAPE COD / 2025 · CHILE | map pans between pins | sonar_ping per pin |
| 31 | U7 "Humpbacks lunge through schools…" | 5:06.4 | 5:21.2 | Lunge + word gag | `Humpback`* vertical lunge through a fish ball (particles) with YOU inside the ball; then `Headline` ENGULFED ≠ SWALLOWED with a sandwich + sock inset | camera tilts up with the lunge | whoosh_long, bubbles; pop on "sock" |
| 32 | U10 "Thirty-eight centimetres, the record…" | 5:21.2 | 5:27.6 | Verdict #3 (record) | Board: the Humpback column grows past the blue whale to 38 (solid to fist, dashed cap), RECORD label; stamp HUMPBACK · ~38 CM · RECORD; lifeguard whistle icon gag | static | impact, ding |
| 33 | G1 "Number two is smaller…" | 5:27.6 | 5:39.6 | Size (#2) | Kicker #2 GOLIATH GROUPER; `GoliathGrouper`* next to YOU at true scale (`pxPerM` 260); grand piano silhouette (svg) drops in on "piano"; kicker ~360 KG ≈ A GRAND PIANO | static, slight push | underwater_rumble; pop on "piano" |
| 34 | G3 "Every giant so far…" | 5:39.6 | 5:55.8 | Suction | Kicker IT INHALES; `GoliathGrouper`* `flare` 0→1 in 6 frames on each prey word; lobster, fish, turtle, shark icons (svg / GreatWhite silhouette) pulled in one after another | quick push on each gulp | whoosh ×4 short |
| 35 | G5 "Off southwest Florida, an…" | 5:55.8 | 6:03.5 | Proof | `Map` Gulf of Mexico (zoom 3) pin SW Florida (lon -81.9, lat 26.3); vignette: fishing line + hooked shark (GreatWhite silhouette as blacktip stand-in) inhaled by the grouper; kicker SHARK ~1.2 M · ONE GULP | static | impact |
| 36 | G6 "So you're drifting over…" | 6:03.5 | 6:09.4 | 2P wreck | Wreck hull silhouette on the seabed (`Ocean` depth 25); YOU drifting over it (no gear); a sofa-sized shape slides out from under the hull | slow creep-in | drone; boom ×2 under "hull" |
| 37 | G8 "So how wide does…" | 6:09.4 | 6:36.4 | Micro-loop + gauge #2 | Kicker HOW WIDE? → NOBODY KNOWS / NO PUBLISHED NUMBER; then the gauge: front-view YOU (45) beside the dashed 40 outline; yellow dashed throat ring ~40 (ESTIMATE); on "stops" YOU's shoulders hit the ring and the frame holds (idle off) with a glitch on the freeze; kicker 45: STUCK · 40: TOO CLOSE TO CALL | push-in; freeze 0.5 s | tick; impact + glitch on "stops" |
| 38 | G13 "Dive boats are full…" | 6:36.4 | 6:51.3 | Folklore + ban | Dive-boat speech bubbles ("IT ATE A DIVER!") each stamped with a red ✕, kicker STORIES THAT HOLD UP: 0; then `Headline` 1990 · HARVEST BAN over a fishing hook with a red ✕ | static | pop ×3, impact |
| 39 | G15 "Forty, give or take…" | 6:51.3 | 6:56.9 | Verdict #2 (asterisk) | Board: the Grouper column (yellow, dashed = estimate only) rises to ~40, just past the humpback, with a big asterisk; stamp GROUPER · ~40 CM* | static | impact; click on "asterisk" |
| 40 | S1 "Number one. The one…" | 6:56.9 | 7:05.8 | Size (#1) | Kicker #1 SPERM WHALE; `SpermWhale` `teeth` on, `ScaleBar` ~16 M; 3 × `Bus` icons stacked as a weight comparison (`Stat` ~40 T); music thins (deep_ocean low, no jokes from here) | slow pan along the body | underwater_rumble |
| 41 | S3 "And unlike everything so…" | 7:05.8 | 7:27.5 | Prey | `DepthMeter` 0→1,000 m quick; whale in near-dark meets a giant squid (`ColossalSquid` `hooks` false as stand-in); `Map` inset Azores pin 1955; the stomach cutaway (svg) with a near-whole squid inside; `Stat` ~180 KG (REPORTED) + two YOU figures on a scale | track down with the whale | sonar_ping, drone; ding on "two" |
| 42 | S6 "So, what does the…" | 7:27.5 | 7:46.6 | Gauge #1: no number | Front-view YOU + red ring; the throat ring flickers (no size), a big `?`; kicker NO MEASUREMENT; then ScaleBar comparison 16 M (typical big bull) vs 18 M+ (the anatomist's "very big adult bull") with SpermWhale silhouettes; kicker BIG BULLS ONLY · ~18 M+ | static | tick; heartbeat_slow |
| 43 | S10 "And here's the honest…" | 7:46.6 | 7:55.2 | Honest hedge | Dark water, the whale fades into the deep as the depth grade drops; `Tag` NEVER SEEN FEEDING; small quote marks around "SWALLOWS PREY WHOLE?" | slow push, no shake | drone only |
| 44 | S11 "So you put the…" | 7:55.2 | 8:00.3 | Ring retired | The front-view YOU with the red ring; on "down" the ring drops off-frame and spins away (the gauge is retired) | static | click; low whoosh on the fall |
| 45 | S12 "Could the biggest bulls…" | 8:00.3 | 8:11.6 | Verdict #1 | Board: a grey dashed SpermWhale column with a large `?` rises through the red line ("COULD: BIG BULLS"), then a small stamp HAS: NEVER under it; kicker COULD: BIG BULLS · HAS: NEVER | static | impact soft |
| 46 | F1 "And it wouldn't even…" | 8:11.6 | 8:17.2 | Reassurance flip | Wide: the SpermWhale glides past a tiny YOU without turning; `Tag` YOU: NOT ON THE MENU; a squid icon floats by and the whale turns toward it instead | slow pan | bubbles |
| 47 | V1 "That should be the…" | 8:17.2 | 8:30.9 | Twist (tone drop) | Grade drops (saturate 0.4, vignette 0.5) and music cuts to dread through a 1.2 s fade; the board returns with one empty slot above the red line pulsing; kicker YES. on "yes" | slow push | stinger on "yes" |
| 48 | V4 "In 2019, one stranded…" | 8:30.9 | 8:47.2 | Evidence: Scotland | `Map` UK + N Atlantic (zoom 3, Great Britain is coarse: ring marker, no coastline close-up) pin Isle of Harris (lon -7.0, lat 57.8) "2019"; stomach cutaway (svg) fills with a rope-and-net ball (svg); `Stat` ~100 KG; a YOU silhouette on a scale reads less ("MORE THAN YOU WEIGH") | map then cut to the cutaway; slow push | sonar_ping; drone |
| 49 | V6 "A year earlier, one…" | 8:47.2 | 8:58.8 | Evidence: Indonesia | `Map` pin Wakatobi (lon 123.6, lat -5.5) "2018"; icon row counts in (`Debris`: 115 cups, 25 bags, 2 flip-flops) with `Stat` per icon; a bowling ball drops beside "~6 KG" | map; icon row stagger | pop per icon (fast); ding on each total |
| 50 | V7 "Remember the rules? You…" | 8:58.8 | 9:11.9 | Rule callback | Replay of the 0:16 RULES card (`Options`, same layout); on "net", "rope", "flip-flops" matching icons (rope coil, net, flip-flop) slide out of the card into the stomach cutaway, which now holds every piece of gear in the video; kicker ALL THE GEAR → INSIDE THE WHALE | static | whoosh per item; stinger tail on "whale" |
| 51 | V9 "Nothing in the ocean…" | 9:11.9 | 9:20.3 | Villain swap | Pull back from the gear-filled stomach to the whole whale swimming, then up to YOU floating free at the surface while a single flip-flop drifts down past the camera | long pull-out | drone fade; bubbles |
| 52 | E1 "So, the final board.…" | 9:20.3 | 9:38.3 | Final board | The finished board, colour back to normal; each column pulses as its verdict is read (basking shark, whale shark, blue whale, humpback, grouper, sperm whale, our rubbish); held as comment bait | static, hold | tick per column |
| 53 | E3 "Six giants, one pizza…" | 9:38.3 | 9:43.7 | Bookend | Back to the 0:00 composition, now empty of shadows; YOU swims up out of frame toward the surface; the red ring is gone | slow tilt up | whoosh; deep_ocean swells (gain automation) |
| 54 | C1 "Which giant should we…" | 9:43.7 | 9:54.2 | CTA | Finished board returns small; `Headline` NEXT GIANT? ↓; on "blue whale" a BlueWhale silhouette glides across the bottom with `gape` open and a krill cloud, and YOU (pose panic) scoots out of frame | static; hard cut to black at the end | pop; stinger |
<!-- /GENERATED:SHOTS -->

## Fact sheet

Rule used in the VO: every giant gets the most generous figure we could find from a named source; ranges are stated plainly, and the single honest admission is at 7:47 (S10). Re-check every row marked ⚠ before posting.

| Claim in VO | Value used | Source / note |
|---|---|---|
| Your shoulders "across the muscle" | ~45 cm typical adult; smaller adults ~40 | Bideltoid (soft-tissue) breadth, not the bony biacromial width (~36-41 cm), which would let a small adult "pass" the humpback. Civilian UK adults (Pheasant & Haslegrave, *Bodyspace*): men ~46.5 cm, women ~39.5 cm; US Army ANSUR II runs a few cm wider. ⚠ confirm the exact table means before posting |
| Party-size pizza box | ~46 cm | An 18-inch pizza box. Pilot 3 and the earlier draft used a 16-inch (40.6 cm) "large" box; changed with the gauge |
| Your head / your fist (board guide lines) | ~16 cm / ~9 cm | Typical adult head breadth ~15-16 cm; hand breadth ~8-9 cm (a "hand's width" in B9 = ~9 cm; 45 − 35 = 10 cm) |
| Blue whale: heaviest animal known, ~30 m | ~30 m; 2.5 buses (12 m) | NOAA Fisheries. "Known to have ever lived" hedges the 2023 *Perucetus* claim (since revised down) |
| One lunge can take in more water than the whale weighs | qualitative | Goldbogen et al., lunge-feeding papers (engulfed water mass can exceed body mass) |
| Blue whale throat | most estimates grapefruit → dinner plate (~10-25 cm); widest claim a small beach ball (~35 cm) | Popular sources give 4-10 in (10-25 cm); the beach-ball comparison (e.g. Baleines en direct) is the widest claim we found and is what pilot 3 said on screen (its `WhaleThroat` ring is 0.34 m). Using it keeps the channel consistent: even the beach ball loses to 45 cm |
| ~16 t of krill a day = ten cars' worth | 16 t / ~1.5 t per family car ≈ 10.7 | Savoca et al. 2021, *Nature* (feeding-season intake) |
| Whale shark: bomb-carbon ageing, 2020, ~50 years | ~50 yr | Ong, Meekan et al. 2020, *Frontiers in Marine Science* (radiocarbon from 1950s-60s nuclear tests used to date vertebral growth bands); one shark ~50 years |
| Whale shark size / mouth | up to ~18 m / ~1.5 m wide | Georgia Aquarium; standard references |
| Whale shark throat | a quarter (~2.4 cm) → ≤ ~15 cm | Georgia Aquarium: "often compared to the size of a quarter"; secondary sites give 10-15 cm (unsourced). We use 15 as the most generous figure. Cereal bowl ≈ 15 cm |
| Basking shark: 2nd-biggest fish, mouth ~1 m, ~2 million L/h | ~2,000,000 L/h ≈ 80% of an Olympic pool (2.5 million L) | Natural History Museum London; Marine Conservation Society |
| Filters with gill rakers, doesn't gulp or suck | ram filter feeder | Standard references |
| Zuiyo-maru carcass | April 1977, off New Zealand; tissue tests pointed to a basking shark; the jaws and gill region fall away first as it rots | Kuban (TalkOrigins); standard references |
| Basking shark throat | ~10 cm with a sharp bend | ⚠ secondhand quote of E. W. Gudger (AMNH): "only four inches wide, with a sharp elbow or bend behind the opening"; the species in that quote needs confirming. If it turns out to refer to the whale shark, change K10 to "nobody has published a figure" and keep the bottom placement on mechanism |
| Humpback throat | ~ fist; stretched for a big meal ~38 cm (15 in) | National Geographic, 15 June 2021 ("Most whales can't really swallow a human. Here's why"): "roughly the size of a human fist", "can only stretch to about 15 inches in diameter". The VO says "the widest figure published" |
| Two people inside a humpback's mouth | Cape Cod lobster diver, June 2021, ~30-40 s; kayaker, Strait of Magellan, Chile, Feb 2025, seconds (filmed by his father) | AP, CBS, BBC coverage. No names used. "Within a minute" covers both |
| "Engulfed, not swallowed" | expert framing | Whale and Dolphin Conservation / Center for Coastal Studies comments on the 2021 case |
| Goliath grouper size | up to ~2.5 m, ~360 kg; grand piano ~300-500 kg | NOAA Fisheries / Florida FWC |
| Suction feeding | "a rapid expansion and opening of the mouth … sucked in and swallowed whole" | Florida FWC species profile |
| Grouper swallowing a hooked ~1.2 m (4 ft) blacktip | SW Florida, August 2014, filmed by an angler | Widely reported (e.g. "goliath grouper eats 4-foot shark in one bite"). ⚠ replace the YouTube id in `backlog/explainer/evidence/q2_goliath_grouper_swallow_diver.jsonl` with a news citation; keep "blacktip" only if that article says so |
| Grouper gape | no published figure; "about forty centimetres, a guess" | Our scaling: Mihalitsis & Bellwood 2017, *PLoS ONE* (PMC5590994): a small grouper (*Cephalopholis urodeta*) swallowed prey up to 27% of its standard length deep (18% after prey compression). Goliath 2.5 m TL ≈ 2.1 m SL → 38 cm (compressed) to 57 cm (uncompressed fish). Human shoulders barely compress, so we use the low end, ~40, and call it a guess on screen (dashed yellow, asterisk) |
| No verified grouper-swallows-diver case | folklore only | We found no documented case |
| US harvest ban | 1990 (federal waters) | NOAA / FWC. Florida reopened a tiny lottery harvest in 2023 (not mentioned; "banned in 1990" is accurate) |
| Sperm whale size | ~16 m, ~40 t; school bus ~12-13 t → "three school buses' worth" | NOAA Fisheries |
| 1955 Azores giant squid | ~10 m with tentacles (34 ft), nearly whole; weight reported ~184 kg (405 lb) | R. Clarke, "A giant squid swallowed by a sperm whale", *Norsk Hvalfangst-Tidende* 1955 (10): 589-593, via Budker 1959. The weight has been questioned, so the VO says "reported" and "around a hundred and eighty" ⚠ check the primary paper |
| Joy Reidenberg: a very big adult bull could swallow a person | ~18 m or more, bigger than most bulls seen | *Science News*, 10 Sept 2026, "Could a whale swallow a person whole?". The same piece: the sperm whale's larynx sits off to the left, which widens the throat; nobody has watched sperm whales feed, and researchers aren't sure they swallow prey whole (S10). **Correction to the previous draft:** Reidenberg's "I can barely get my arm down the throat" is about fin whales, not sperm whales, so the old "another researcher could barely fit an arm" line was wrong and is gone |
| No reliable case of a person inside a sperm whale | qualitative | The 1891 "James Bartley" story is debunked and not mentioned |
| Isle of Harris stranding | Dec 2019, ~100 kg ball of rope, netting, bags; more than an adult weighs | Scottish Marine Animal Stranding Scheme / BBC. SMASS said the debris built up in the stomach (VO: "built up over time, not in one gulp") |
| Wakatobi, Indonesia stranding | Nov 2018: 115 cups, 25 bags, 4 bottles, 2 flip-flops, ~6 kg total; bowling ball 5-7 kg | WWF Indonesia via AP, NPR, CBS. The VO lists cups, bags and flip-flops only (all true; bottles omitted for length) |
| Not on the menu | qualitative | Sperm whale diet is mostly cephalopods; no pattern of attacks on swimmers |

Cut since the last draft (and why): Spain 2018 (third stranding stat in a row, no anchor), megamouth (seventh animal, same verdict), the orca-rescue bonus (12 s, unrelated to the test), the leatherback CTA (no setup), the "barely fit an arm" line (misattributed), the 38-vs-40 "−2 CM" duel (false precision on a popular figure; the humpback is now 38 vs 45 with the smaller-adult 40 shown as a dashed line).

## Writer checklist (PLAYBOOK §10)

- [x] Front matter cites three corpus scripts (SWALLOW, SPERM, ERAS) with stats, plus ORCA as a device source; beat alignment table re-checked line by line against the annotated transcripts in `research/corpus/explainer/` (every timestamp is in the table)
- [x] "You" at risk; famous subjects; title as a question on you with our own qualifier (titles.md)
- [x] Hook 23 words / 7.6 s, "you" at word 1, the test on screen in frame 1; board on screen at 0:36.2, first rung at 0:44.8
- [x] Teasers paid in order at 20% / 50% / 57% / 76%
- [x] Two axes (gauge number × how we know); every rung has a number on the same board, and the board is ordered strictly by it; sawtooth from fame order vs number order
- [x] Every number paired with an object or the gauge (buses, cars, quarter, cereal bowl, Olympic pool, fist, piano, "two of you", "more than you weigh", bowling ball)
- [x] Re-immersion at 4:12 (42%) that escalates; gross-out at 3:34-3:57 (36-40%); one honest admission (7:47); 6 rhetorical micro-loops
- [x] Running device set, broken and retired: record (4:41) → asterisk (6:51) → ring put down (7:55)
- [x] Climax could/has at 8:01 (81%); the title's real answer, the "has" slot, lands at 8:29-8:42 (86-88%) with the tone drop; rule turned around at 8:59 (91%)
- [x] Bookend recap + finished board; one comment CTA with a callback joke; no subscribe plea
- [x] No gore: strandings and the carcass are flat icons and silhouettes; no self-harm wording
- [x] Comic punch lines get 0.5-0.55 s of air; total 594.2 s ≤ 600 s
- [x] `python3 scripts/originality_check.py backlog/explainer/explainer-every-animal-that-could-swallow-you/script.md research/corpus research/library/transcripts` → PASS (see review.json)
- [ ] Before posting: the ⚠ rows above; R5 policy check (research/R5 is still empty): AI-voice disclosure, templated-series "inauthentic content" risk, ad suitability of the stranding beat (kept non-graphic)
