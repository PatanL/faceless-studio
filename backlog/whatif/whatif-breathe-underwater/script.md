---
slug: whatif-breathe-underwater
niche: whatif
format: long_16x9 (1920x1080)
engine: power story (one change + one promise -> honeymoon -> numbered problems -> rug pull on the planted variable -> real analogue -> stranding) run along a one-way depth-stop ladder
working_title: "What If You Could Breathe Underwater, But Never Come Back Up?"   # rank 1 in titles.md; the bare same-premise title is retired to the description
generated_by: gen_storyboard.py (single source; edit the generator or script.template.md, never this file)
target_runtime_s: 443.9      # 7:23.9 incl. 2.2 s title card (VO over it), 2.0 s descent ramp, 3.5 s end-card hold
target_runtime_range_s: [390, 480]   # TOPICS.md long-form window 6:30-8:00
runtime_at_kokoro_speed_1.2_s: 460.9   # measured fallback; a further 10% slower read would be 485.6 s, and the cut list in "Notes for the build lane" brings that under 480
vo_words: 1318                # caption spelling; 1371 words as Kokoro reads them (digits expanded)
words_per_min: 178.1     # over the full runtime; Kokoro am_michael speed 1.25 (measured 207 spoken wpm inside lines; 102/102 lines timed from the Spark pass, the rest from its fit)
sentences: 174           # mean 7.6 words; 24.7% are <=3-word punch lines
second_person_sentences: 49.4%   # 86 of 174; PLAYBOOK §12 floor for power stories 45%; 8.1 you-words per 100
you_words_first_30s: 12   # IFOLOGY top-10 median 12
pivots_per_min: 3.51  # 26 hits of but/except/until/unless/here's/problem/catch/though/instead; PLAYBOOK median 1.5, IFOLOGY winners 2.0
numbers_per_min: 7.6   # 56 tokens (digits + number words, §9 counting) over the runtime; corpus range 1.3-8.2
hook: "103 words / 31.85 s cold open; first sentence 12 words; 'And you're fine' at 3.48 s; BODY readout falling from 0:04; route + wall at 0:28; DepthMeter moving from 0:30"
master_loop: "will you reach the deepest floor, past the wall, and what is left of you there?" opens 0:20-0:30, wall paid 5:47, floor 6:15 (85%), stranding answered 6:52-7:08 (96%)
tracker: "whatif/Hud: DepthMeter (moving from 0:30) + PRESSURE xN + BODY °C readout (falling from 0:04) + BORROWED fixes 0 -> 4 -> NO FIX LEFT + DAYS (from the abyss) + REMORA reaction chip + WAY BACK line; per-scene state table below"
voice: Kokoro am_michael (CPU, Spark), speed 1.25 (fallback 1.2 = ~7:40), one calm dry narrator; word-level burned-in captions from TTS timings; vo_lines.json carries the TTS spellings (digits expanded, TMAO as T-M-A-O)
kit: B3 explainer kit + core layers + 4 NEW whatif/* components (Hud, Ferry, GillDiagram, Fish) + 1 kit edit (DepthMeter marks); everything else is core layers and inline SVG strings in the generator
references:
  - id: "y300HjYnHPw"
    short: 10X-FASTER
    url: https://www.youtube.com/watch?v=y300HjYnHPw
    views: 867909
    outlier_score: 8.38
    why: >-
      Same "what if YOU could [classic power]" family and the main power-story spine. Borrowed: a short
      second-person open with the power working by ~4 s; the title question after the demo; rules that change
      one thing and plant the unchanged one ("remember it"); a baseline -> worked number ladder with a dated lab
      test; a demo gag that splits the maths; an "at first" honeymoon with one early crack; a numbered problem
      ladder; the T4 rug pull where the planted unchanged variable is the real problem; a real animal flagged as
      real that supplies the fix; and a climax decision that spends a planted number.
  - id: "_lu85gSD39k"
    short: BILLION-YEARS
    url: https://www.youtube.com/watch?v=_lu85gSD39k
    views: 413108
    outlier_score: 41.02
    why: >-
      Closest structure to a one-way depth descent. Borrowed: an irreversible rule stated in the hook that only
      bites at the end (our "you can't climb back on" -> the way back is spent), the whole route shown in the
      first 30 s, a mute companion whose reactions are a readout at every stop and who carries the tender beat at
      the end (our remora, drawn and read as a HUD chip, no second voice), a stamp card per stop, a tracker number
      planted, advanced and paid (our 8,200 m wall), a slowed last stop with a list of absences that mirrors the
      first, a recap of every stop, a quotable moral and a pick-a-stop CTA.
  - id: "6oZ9fdM0n50"
    short: RESTART
    url: https://www.youtube.com/watch?v=6oZ9fdM0n50
    views: 4221146
    outlier_score: 14.44
    why: >-
      Nearest runtime and the flat-2D look. Borrowed: the second-person cold open with a list of absences and an
      "everyone... except" narrowing, the thought-experiment maths block (first, the constraint -> real figure ->
      worked number -> one everyday conversion), the one-word false resolution -> "except" turn, a dated human
      precedent told in two sentences, the emotional floor at ~70% followed by a "but" turn, the honest verdict
      that restates the title question with a short answer, and a CTA question asked from the opening scene.
topic_evidence:
  - 'Peekaboo "Could Breathe Underwater?" 2.35M; What If (Underknown) same premise 1.59M; Ifsphere 250K (backlog/whatif/TOPICS.md row 12)'
  - 'IFOLOGY classic-power cluster median ~200K, "10x Faster" 868K (research/R3)'
  - 'Depth Theory ocean explainer 2.28M on a 6K-sub channel (PLAN.md niche table): same flat ocean look as our B3 kit'
  - 'Familiar premise (PLAYBOOK §10C fatigue): differentiated by the depth angle, the borrowed-fix promise and the stranding; see titles.md'
originality: "python3 scripts/originality_check.py backlog/whatif/whatif-breathe-underwater/script.md research/corpus research/library/transcripts -> PASS (see bottom of file)"
---

# What If You Could Breathe Underwater, But Never Come Back Up?

Episode `whatif-breathe-underwater` · 16:9 · 7:23.9 · power story on a depth-stop ladder · one Kokoro narrator (CPU on the Spark), word-level burned-in captions. Built from the B3 ocean kit plus four small whatif components.

**Premise in one line.** You fall off a ferry in the western Pacific, gasp seawater, and you're fine. The rules give you one change (oxygen from water) and one promise (each time the ocean tries to kill you, you get the fix a real animal already uses, until there isn't one). You head for the deepest floor on Earth, pick up four borrowed fixes, hit the wall where fish run out at 8,200 m, and pay for the last 2,700 m with the way back.

**What we borrow vs what is ours.** Borrowed: beat order and timing shares, and devices (plant/payoff, rules card, numbered problems, rug pull, flagged real analogue, mute companion readout, stop stamps, tracker number, stranding, recap + choice CTA). Ours: the story (ferry, remora, BODY readout, borrowed-fix promise, the wall, the trade), every sentence, every fact chain, every visual. No reference wording, character, gag or footage is reused.

**What changed in this final version (critique round 1).** 12-word first line ("fine" at 3.48 s); the tracker moves in the hook (BODY readout from 0:04, DepthMeter from 0:30); the heat drain is reframed as T4 (killing you since the ferry, blood-flow-limited ×30 at the surface, ×100 at 4 °C, hypothermia crossed at ~200 m); giant squid replaces colossal squid; the one-way rule, the trench geography and the borrowed-fix promise are in the rules; the sperm whale is a threat at the midpoint, followed by the stranding plant; the hunger loop pays on the trench floor; a mute remora companion with a readout carries the tender beat; "upgrade 4" is gone: 8,200 m is the wall and the last 2,700 m costs the way back; numbered problem ladder; decision climax; numbers cut from 10.8/min to 7.6/min; second person 49.4%; pivots 3.51/min; new assets cut from ~28 to 4 components + 1 kit edit.

## Beat alignment table

| our beat | our timestamp | reference id + timestamp | device borrowed | how we adapt it |
|---|---|---|---|---|
| L1 Cold open: fall, gasp, fine | 0:00-0:04 | y300HjYnHPw @0:00-0:09 (4-word second-person open, power shown working by 0:02, micro-loop closed before 0:10); 6oZ9fdM0n50 @0:01-0:04 (second-person moment, list of absences) | short first sentence; show-before-tell; list of absences | 12-word first line with the impossible change; "And you're fine" at 3.48 s; "No coughing. No burning." |
| L1 Companion + exception | 0:09-0:13 | _lu85gSD39k @0:24-0:29 (mute companion introduced in the hook; its reactions become a running readout); 6oZ9fdM0n50 @0:10-0:15 ("every person" -> self-correction leaves an exception) | mute sidekick whose reactions are a readout; "everyone... but you" narrowing | a remora latches on (thinks you're a shark) and gets a HUD chip; "Everyone up there breathes air. Everyone but you." |
| L1 One-way rule + route + wall + moving tracker | 0:16-0:30 | _lu85gSD39k @0:07 (one problem: it can never go back), @0:14-0:19 (destination tease); PLAYBOOK §2 combination rule (tracker already moving in the hook) | irreversible rule in the hook; whole route in the first 30 s; destination promise | "air doesn't work for you anymore. You can't climb back on"; map: the trench a few hundred km SW; route ticks light with the red 8,200 m "wall"; the meter starts moving at 0:30 |
| L2 Title + rules + plant | 0:32-0:50 | y300HjYnHPw @0:11 (title question after the demo), @0:13-0:27 (one changed rule, what stays normal, "remember that") | title question; one-variable rule; explicit plant | title asked over a 2.2 s card (no dead hold); one change + the promise "until there isn't one"; the 37 °C plant points at a readout that is already falling |
| L3 Grounding while sinking | 0:53-1:09 | 6oZ9fdM0n50 @0:38-1:27 (first, the target -> real figure -> worked number -> time conversion); y300HjYnHPw @1:20-1:29 (scientists tested it, counter-intuitive limit) | baseline -> worked number -> one everyday conversion; dated lab precedent | 1/30 -> 60 L/min -> a bathtub every 2.5 min (the only conversion); 1966 liquid-breathing mouse; the meter runs 0 -> 200 m underneath |
| L3 Demo gag | 1:15-1:19 | y300HjYnHPw @0:56-1:16 (a demo scene with a double gag splits the number run) | consequence played as a gag, sidekick reaction | no air means no voice; the remora looks relieved |
| L3 Mechanism + false resolution (first turn) | 1:21-1:34 | y300HjYnHPw @1:38-1:42 (human limit vs "yours can" number pair); 6oZ9fdM0n50 @1:30 (one-word false resolution -> "except") | number pair; one-word false resolution + except | fix 1 gills: 80% vs 25%; "Easy. Except..." at 1:34 (21%) |
| L4 Honeymoon + numbered problems | 1:39-2:22 | y300HjYnHPw @1:48-2:38 ("at first" perks rising, first crack @2:23), @2:41-3:49 (numbered problem ladder, each with a fast fix); _lu85gSD39k @0:54 (stop card) | stamp; rising perks; famous record passed; numbered problems; first crack waved away | 200 m stamp; no squeeze (ears and sinuses flood); pass 253 m; blue whale; problem 1 salt -> fix 2; problem 2 light (no fix, a loop); white fingertips "just the light" |
| L5 1,000 m stop + problem 3 | 2:26-2:35 | _lu85gSD39k @1:58-2:21 (stop template: card, sense first, expectation broken, one number) | stamp -> sensory arrival -> one number -> button | light gone; 3 in 4 glow (pays the light loop); problem 3 anglerfish; remora readout HIDING |
| L5 Rug pull (T4) | 2:41-3:09 | y300HjYnHPw @4:24-4:31 (none of that was the real problem; callback to the plant) | rug pull at ~35%; the planted unchanged variable is the killer; numbers for the danger | the BODY readout falling since 0:04 flies to centre; ×30 at the surface, ×100 at 4 °C; "You passed it a while ago" (2:41, 36%) |
| L6 Real analogue -> fix | 3:11-3:31 | y300HjYnHPw @5:41-6:03 (one real animal, "this part is real", principle reused) | real analogue flagged as real; principle reused; a cost attached | bluefin tuna exchanger = your gill trick run backwards -> fix 3; cost: you can never stop swimming (plants hunger) |
| L7 2,000 m threat + midpoint re-hook + stranding plant | 3:36-4:06 | _lu85gSD39k @4:16-4:36 (something is wrong -> named fact -> size comparison -> button); PLAYBOOK L7 (re-hook at 45-60%); _lu85gSD39k @3:52 (plant: keep this in mind) | threat by sound; size comparison; "the problem nobody warned you about"; plant for the end | sperm-whale clicks speed into a buzz aimed at you, then it turns away; giant squid; at 4:00 (54%) every fix makes you worse at everything else; deep fish don't survive the trip up |
| L8 4,000 m pressure + tracker advance | 4:11-4:51 | 6oZ9fdM0n50 @2:51-3:10 (history already ran the experiment, short dated case); _lu85gSD39k @3:52-3:57 and @6:59-7:02 (tracker number planted, then advanced) | dated human precedent; mechanism; tracker advance | 1992 chamber at 701 m -> fix 4 TMAO -> 2014 prediction: 8,200 m is "the wall on your route" (second touch of the red tick) |
| L9 Low point -> option board -> turn | 4:56-5:27 | 6oZ9fdM0n50 @4:05-4:24 (emotional floor as a question, then a "but here's the thing" turn); PLAYBOOK §4 (personal thread revisited) | floor at ~70%; options with strikes (a board, not a trip); "but" turn | DAY 4 stamp; starving; remora quiet; options board (open ocean ✗, abyss ✗, vent 1977, reef ✓ -> ✗ "can't go back up"); the floor ends ahead |
| L10 The wall + decision | 5:30-6:12 | _lu85gSD39k @11:24 (tracker final value), @11:43 (sidekick gag turns tender); y300HjYnHPw @7:05-7:11 (climax decision that uses a planted rule and number); PLAYBOOK T12 | planted number pays; companion leaves; honest speculation flag; a choice that spends the planted cost | snailfish; its 2022 cousin at 8,336 m; NO FIX LEFT; the remora drifts up; "this is our guess"; stay, or pay 2,700 m with the way back |
| L10b Final descent + payoff | 6:12-6:47 | _lu85gSD39k @10:30-10:41 (last stop, slowed), @11:09 (list of absences mirrors the first stop); PLAYBOOK T10 (bathos) | pace drop; mirrored sensory list; biggest number; human trace last | 2 s ramp; "No light. No sound." mirrors 0:04; a car on each thumbnail; hunger pays (food, and you're what sank); 2019 fibres: "your world got to it first" |
| L11 Bookend + verdict + recap + thesis | 6:52-7:08 | _lu85gSD39k @11:46-11:50 (stranding: the hook rule bites), @11:57 (recap of every stop), @12:42 (quotable moral); 6oZ9fdM0n50 @5:48-5:51 (restate the title question, short honest answer) | stranding; verdict; recap; one-line thesis | ferry still crossing, remora up there; "Yes. That part's easy."; four borrowed fixes + the way home; "Getting in was never the hard part. Getting out is." |
| L12 CTA + series loop | 7:11-7:17 | 6oZ9fdM0n50 @6:22 (CTA asked from the opening scene); _lu85gSD39k @12:56 (pick a stop from options already shown); PLAYBOOK §8 (one loop left open) | callback CTA; no-wrong-answer choice; series harvest | "back at that ferry rail: would you jump?" reef / vent / the line; "swim back up" as the next episode |

Not borrowed on purpose: a second spoken voice (one Kokoro narrator; the remora is mute and reads out through its HUD chip and body language); the 10X-FASTER universe/team act (replaced by a one-line series loop).

Pacing check against PLAYBOOK §9 / §12 (long-form):
- Cold open 103 words / 31.85 s (target ≤120 / ≤50, ~90 / ~35). First sentence 12 words, second person, impossible change inside it; "fine" at 3.48 s. Running trackers in the hook: BODY readout from 0:04, DepthMeter from 0:30. No channel intro. Title card 0:32.3-0:34.5 with the VO asking the title over it.
- 178.1 wpm over the runtime (power-story band 175-185; see the TTS note), mean sentence 7.6 words, 24.7% punch lines, 49.4% second-person sentences (≥45%), 8.1 you-words per 100, 12 you-words in the first 30 s.
- Pivots: 26 = 3.51/min (≥1.5; IFOLOGY winners 2.0): but 0:13, here's 0:16, catch 0:16, until 0:44, here's 1:21, except 1:34, but 1:48, problem 2:06, problem 2:15, problem 2:35, but 2:41, here's 2:41, problem 2:41, problem 2:44, except 3:11, instead 3:21, but 3:31, until 3:40, here's 4:00, problem 4:00, but 4:32, but 4:43, problem 4:59, unless 5:15, but 5:19, except 5:23.
- Numbers: 56 tokens = 7.6/min (≥4; corpus max 8.2). Every stat has an on-screen chip.
- Stamps: 200 M 1:39, 1,000 M 2:26, 2,000 M 3:36, 4,000 M 4:11, DAY 4 4:56, 8,200 M 5:30, 10,935 M 6:15 (gaps 47 s, 70 s, 35 s, 45 s, 33 s, 46 s; PLAYBOOK 60-75 s, range 46-87). Ours run 33-70 s, tighter than the norm, because there are seven stops in 7:23.9. Every stamp is also a tracker jump, and between stamps the BODY readout and the meter keep moving.
- Verbal re-hooks (pivot, question, plant, tease, deadpan button): 46, median gap 8.3 s, longest 28.9 s (≤35).
- First turn ("Easy. Except") 1:34 (21%, target ~25%); rug pull 2:41 (36%); midpoint re-hook 4:00 (54%, target 45-60%); low point 4:59-5:07 (67%); wall 5:47 (78%); floor 6:15 (85%); ending stack (bookend -> end) 6:52-7:23.9 = 7.1% of runtime (≤12%).
- Long plants paid: BODY readout (0:04 -> 2:44), one-way rule (0:16 -> 4:06 -> 6:09 -> 7:01), the wall (0:28 -> 4:51 -> 5:47), "until there isn't one" (0:44 -> 5:47), never stop swimming (3:31 -> 4:59 -> 6:29), remora (0:09 -> 5:50 -> 6:52), ferry (0:00 -> 6:52 -> 7:11).

## The script

Layers: **HUD** = `whatif/Hud`, top-left stack (DepthMeter ruler on the left edge with a big depth readout, PRESSURE ×N under it, BODY °C readout with a 35° line, BORROWED n · NAME counter, DAYS chip from the abyss, REMORA reaction chip, WAY BACK line once planted). **STAMP** = centred `Headline`, number in red + grey sub line, held ~2 s. **CHIP / STAT / TAG** = kit `Stat` / `Tag` that pop with each spoken number. **CAPTIONS** = core word-level captions at 88% height, content words in red. **VO** = one narrator, calm and slightly dry.

### Hook

- **First line (VO + captions, 0:00):** "You fall off a ferry in the Pacific and gasp in seawater."
- **First visual (0:00):** dusk split-waterline frame: top 35% violet-orange sky with the dark ferry hull sliding right to left, deck rail lit; bottom 65% teal water where YOU (`pose: panic`) has just punched through in a burst of bubbles. The HUD is there from frame 1: DEPTH 0 M, BODY 37.0 °C. At 3.48 s ("And you're fine") the bubbles stop and the figure floats upright; from 0:04 the BODY readout starts ticking down and nobody mentions it until the rules.

### Voiceover / captions with timestamps

Timings come from `gen_storyboard.py`: TTS word count (digits expanded) at each section's rate + 0.16 s per sentence break + 0.24 s between lines. Retime from the real Kokoro word timings at build (the storyboard captions are estimates until then). On-screen items appear on their first keyword.

#### [L1 COLD OPEN] 0:00.0–0:31.9 (TTS 207 wpm)
- 0:00.0 VO: You fall off a ferry in the Pacific and gasp in seawater.
  - 0:00.0 ON-SCREEN: HUD from frame 1: DEPTH 0 M · BODY 37.0°C; TAG `WESTERN PACIFIC`
- 0:03.5 VO: And you're fine.
  - 0:03.5 ON-SCREEN: bubbles stop; YOU floats upright
- 0:04.7 VO: No coughing. No burning. Your chest just keeps going, like you've done this forever.
  - 0:04.7 ON-SCREEN: BODY TEMP readout starts ticking down from 37.0 (no comment yet)
- 0:09.4 VO: Something bumps your back and holds on. A remora. It thinks you're a shark.
  - 0:11.0 ON-SCREEN: HUD REMORA chip: ATTACHED
- 0:13.5 VO: Everyone up there breathes air. Everyone but you.
- 0:16.4 VO: And here's the catch: air doesn't work for you anymore. You can't climb back on.
  - 0:17.0 ON-SCREEN: TAG `AIR: DOESN'T WORK FOR YOU`; red strike across the surface
- 0:20.7 VO: Under you, the floor is 4 kilometres down. The deepest floor on Earth is a trench, a few hundred kilometres south-west of you.
  - 0:21.1 ON-SCREEN: STAT `4,000 M TO THE FLOOR`
  - 0:23.7 ON-SCREEN: MAP inset: YOU pin -> dashed 300 KM line -> CHALLENGER DEEP pin
- 0:28.2 VO: And a line on your way down is a wall.
  - 0:28.2 ON-SCREEN: ROUTE ticks light: 200 · 1,000 · 2,000 · 4,000 · 8,200 (red, `THE WALL?`) · 10,935 M
- 0:30.6 VO: So you go down.
  - 0:30.9 ON-SCREEN: DepthMeter starts moving: the tracker runs from here to the end

#### [L2 TITLE + RULES] 0:32.3–0:53.1 (TTS 207 wpm)
- 0:32.3 VO: What if you could breathe underwater?
  - 0:32.3 ON-SCREEN: TITLE CARD (VO over it): WHAT IF YOU COULD BREATHE UNDERWATER? (UNDERWATER red)
- 0:34.5 VO: One change: your body can pull oxygen out of water.
  - 0:35.7 ON-SCREEN: RULE 1 `ONE CHANGE: OXYGEN FROM WATER`
- 0:38.1 VO: One promise: every time the ocean tries to kill you, you get the fix a real animal already uses.
  - 0:38.5 ON-SCREEN: RULE 2 `EVERY THREAT -> A REAL ANIMAL'S FIX`
- 0:44.1 VO: Until there isn't one.
  - 0:44.1 ON-SCREEN: RULE 3 `UNTIL THERE ISN'T ONE` (red)
- 0:45.8 VO: Everything else stays human: daylight eyes, and blood at 37 degrees.
  - 0:45.8 ON-SCREEN: card STAYS HUMAN: SKIN · EYES · 37°C BLOOD (37°C red)
- 0:50.3 VO: Keep an eye on that number. It's already moving.
  - 0:50.3 ON-SCREEN: pointer ring on the HUD BODY readout (36.8 and falling)

#### [L3 GROUNDING WHILE SINKING (0 -> 200 M)] 0:53.5–1:38.8 (TTS 207 wpm)
- 0:53.5 VO: First, the bad news: seawater holds about 30 times less oxygen than air.
  - 0:54.3 ON-SCREEN: SPEEDBARS `OXYGEN PER LITRE` AIR vs SEAWATER (~1/30)
- 0:58.5 VO: So about 60 litres of sea has to pour through you every minute.
  - 0:59.1 ON-SCREEN: SPEEDBARS `THROUGH YOU EVERY MINUTE` AIR 6 L vs WATER 60 L
- 1:02.3 VO: A bathtub every two and a half minutes.
  - 1:02.6 ON-SCREEN: TIMER ring 2:30 + TAG `1 BATHTUB`
- 1:04.6 VO: Lungs can't. Water is heavy, and lungs push it in and out the same pipe.
  - 1:06.2 ON-SCREEN: lung diagram: one pipe, arrows in and out, red ✗
- 1:09.0 VO: In 1966, a lab mouse breathed oxygen-rich liquid and lived. Breathing out was the hard part.
  - 1:09.3 ON-SCREEN: DATE CHIP 1966 · jar + mouse silhouette
- 1:15.4 VO: You try to shout for help. Nothing comes out. No air, no voice.
  - 1:16.8 ON-SCREEN: empty speech bubble `...`
- 1:19.2 VO: The remora looks relieved.
  - 1:19.2 ON-SCREEN: REMORA chip: RELIEVED
- 1:21.0 VO: So here's your first fix, borrowed from every fish alive: gills.
  - 1:23.5 ON-SCREEN: slits draw on behind the jaw; HUD BORROWED 1: GILLS (FISH)
- 1:25.0 VO: Water goes in your mouth and out behind your jaw, with your blood flowing against it.
  - 1:25.0 ON-SCREEN: GILL DIAGRAM: one-way arrows; counter-current strip WATER -> / <- BLOOD
- 1:29.7 VO: That grabs up to 80 percent of the oxygen. Your lungs managed a quarter.
  - 1:30.3 ON-SCREEN: SPEEDBARS GILLS 80% vs LUNGS 25%
- 1:34.2 VO: Easy. Except breathing water does one more thing to you, and you won't feel it yet.
  - 1:34.2 ON-SCREEN: TAG `EASY.`
  - 1:34.9 ON-SCREEN: TAG `EXCEPT...` (red); BODY readout blinks once

#### [L4 HONEYMOON + PROBLEM LADDER (200 M)] 1:39.2–2:26.3 (TTS 207 wpm)
- 1:39.2 VO: 200 metres. For a while, this is the best swim of your life.
  - 1:39.2 ON-SCREEN: STAMP `200 M · THE LAST LIGHT`
- 1:43.2 VO: Every 10 metres adds an atmosphere of pressure, crushing the air inside divers.
  - 1:43.7 ON-SCREEN: PRESSURE x21; inset DIVER air bubble shrinks
- 1:48.2 VO: But you have no air left to crush. Water floods your sinuses and ears, and water barely squeezes.
  - 1:49.8 ON-SCREEN: TAG `EARS + SINUSES: FLOODED`; YOU's water glyph stays the same size
- 1:54.2 VO: The deepest anyone has dived on a single breath is 253 metres. You pass it without noticing.
  - 1:54.7 ON-SCREEN: DepthMeter mark `253 M · DEEPEST BREATH-HOLD` slides past
- 2:00.8 VO: Then a blue whale slides under you, longer than two buses.
  - 2:02.8 ON-SCREEN: SCALEBAR ~28 M vs YOU 1.75 M; two BUS silhouettes
- 2:04.3 VO: It doesn't even look at you. Good.
  - 2:04.3 ON-SCREEN: REMORA chip: UNBOTHERED
- 2:06.3 VO: Problem one: salt. The sea you keep swallowing is about 3 times saltier than your blood.
  - 2:06.3 ON-SCREEN: TAG `PROBLEM 1: SALT`
  - 2:09.7 ON-SCREEN: SPEEDBARS SALT: SEAWATER vs YOUR BLOOD (~x3)
- 2:11.6 VO: Fish have the fix: gill cells that pump salt back out. Now so do you.
  - 2:12.6 ON-SCREEN: GILL DIAGRAM salt mode; HUD BORROWED 2: SALT PUMPS (FISH)
- 2:15.8 VO: Problem two: light. About 1 percent of the sunlight gets this deep, and your eyes were made for beaches. No fix for that.
  - 2:15.8 ON-SCREEN: TAG `PROBLEM 2: LIGHT`; STAT `LIGHT 1%`
- 2:22.9 VO: Your fingertips have gone white. You decide it's just the light.
  - 2:22.9 ON-SCREEN: TAG `FINGERTIPS: WHITE`; BODY readout 34.6, already under the 35 line

#### [L5 1,000 M · MIDNIGHT -> RUG PULL] 2:26.7–3:11.3 (TTS 207 wpm)
- 2:26.7 VO: 1,000 metres. The light isn't dim anymore. It's gone.
  - 2:26.7 ON-SCREEN: STAMP `1,000 M · MIDNIGHT`; STAT `LIGHT 0%`; PRESSURE x101
- 2:30.5 VO: Then the dark starts to sparkle: around 3 in 4 animals here make their own light.
  - 2:31.7 ON-SCREEN: bioluminescent dots; STAT `~3 IN 4 GLOW`
- 2:35.3 VO: Problem three: something glowing drifts up to your face. An anglerfish, small enough for your palm.
  - 2:35.3 ON-SCREEN: TAG `PROBLEM 3: THE NEIGHBOURS`
  - 2:39.3 ON-SCREEN: SCALEBAR ~0.2 M
- 2:41.0 VO: But here's the thing. None of that was ever the real problem.
  - 2:42.2 ON-SCREEN: grade to near-black
- 2:44.6 VO: The real problem has been killing you since the ferry, and it's on screen right now.
  - 2:47.2 ON-SCREEN: BODY readout flies from the HUD to centre: 33.9°C, red
- 2:49.2 VO: Your blood. 37 degrees, remember? The water here is 4.
  - 2:49.2 ON-SCREEN: STAT 37°C (red) vs STAT WATER 4°C (blue)
- 2:53.0 VO: Gills swap heat too. Your blood leaves them as cold as the sea.
  - 2:53.0 ON-SCREEN: GILL DIAGRAM heat mode: red heat dots leave with the water
- 2:56.8 VO: At the surface, you were losing heat about 30 times faster than you make it.
  - 2:57.6 ON-SCREEN: STAT `SURFACE: x30`
- 3:01.1 VO: Here, it's a hundred. Your gills are a radiator, and the ocean is the room.
  - 3:01.3 ON-SCREEN: STAT `HERE: x100` (~10 KW vs ~100 W)
  - 3:03.5 ON-SCREEN: radiator icon replaces the slits; heat lines into the ocean
- 3:05.6 VO: Hypothermia starts at 35 degrees. You passed it a while ago.
  - 3:05.6 ON-SCREEN: BODY readout with the 35° HYPOTHERMIA line; TAG `PASSED AT ~200 M`
- 3:09.7 VO: Down here, you've got minutes.
  - 3:12.5 ON-SCREEN: frost tint, small tremble

#### [L6 REAL ANALOGUE -> FIX 3] 3:11.8–3:36.0 (TTS 207 wpm)
- 3:11.8 VO: Except a few fish cheat the cold, and their cheat is real.
  - 3:11.8 ON-SCREEN: TAG `REAL ANIMAL: BLUEFIN TUNA`
- 3:15.1 VO: In a bluefin tuna, warm blood heading out hands its heat to cold blood coming in, through a tangle of tiny vessels.
  - 3:15.1 ON-SCREEN: TUNA cutaway: vessel tangle in the swimming muscle, warm red <-> cold blue
- 3:21.9 VO: It's your gill trick run backwards, saving heat instead of grabbing oxygen.
  - 3:22.5 ON-SCREEN: the gill counter-current strip slides in beside it with labels flipped
- 3:26.3 VO: So your third fix: a tuna's heat exchanger, between your gills and the rest of you.
  - 3:27.3 ON-SCREEN: coil between the gill slits and the torso; HUD BORROWED 3: HEAT EXCHANGER (TUNA); BODY readout climbs
- 3:31.1 VO: The readout stops falling. But tuna stay warm by never stopping, and now neither can you.
  - 3:33.1 ON-SCREEN: TAG `STOP SWIMMING = FREEZE`

#### [L7 2,000 M · THE HUNTING GROUND (MIDPOINT)] 3:36.5–4:11.3 (TTS 207 wpm)
- 3:36.5 VO: 2,000 metres. A click hits you so hard you feel it in your teeth.
  - 3:36.5 ON-SCREEN: STAMP `2,000 M · THE HUNTING GROUND`; PRESSURE x201
- 3:40.6 VO: Then faster and faster, until the clicks blur into a buzz.
  - 3:40.6 ON-SCREEN: click rings tighten into a buzz
- 3:44.2 VO: That's a sperm whale. When its clicks become a buzz, it's closing in on something.
  - 3:44.8 ON-SCREEN: SPERM WHALE glides in; SCALEBAR ~16 M
  - 3:48.7 ON-SCREEN: TAG `CLICKS -> BUZZ = CLOSING IN`
- 3:48.9 VO: You're warm, you're moving, and you're about the size of what it eats.
- 3:52.4 VO: The buzz hits you in the chest. Then the whale turns away.
- 3:55.7 VO: It wanted a giant squid, with eyes as wide as dinner plates. You don't make the cut.
  - 3:55.7 ON-SCREEN: GIANT SQUID at shared scale; STAT `GIANT SQUID · EYE ~27 CM`
- 4:00.5 VO: Here's the problem nobody warned you about: every fix makes you better at the deep, and worse at everything else.
  - 4:00.5 ON-SCREEN: three fix icons orbit YOU; TAG `BETTER DEEP · WORSE EVERYWHERE ELSE`
- 4:06.6 VO: Many deep fish brought up to the surface don't survive the trip. You're turning into one.
  - 4:06.6 ON-SCREEN: a deep fish rises on a line and comes apart
  - 4:09.8 ON-SCREEN: HUD line `WAY BACK: ?`

#### [L8 4,000 M · THE ABYSS (PRESSURE)] 4:11.8–4:56.3 (TTS 207 wpm)
- 4:11.8 VO: 4,000 metres. You land on the floor of the Pacific: mud, cold, and 400 atmospheres.
  - 4:11.8 ON-SCREEN: STAMP `4,000 M · THE ABYSS`; PRESSURE x401; DAYS chip `DAY 1`
- 4:17.8 VO: Your gills are fine. Your molecules are not.
- 4:20.6 VO: Pressure this strong squeezes your proteins out of shape. Your hands shake. Your thoughts slow.
  - 4:20.6 ON-SCREEN: protein ribbon squashes; nerve sparks
- 4:25.7 VO: In 1992, a diver in a French chamber survived the pressure of 701 metres, a human record.
  - 4:26.0 ON-SCREEN: DATE CHIP 1992; DepthMeter mark 701 M
- 4:32.9 VO: You're almost 6 times deeper. But deep fish carry a molecule called TMAO that props proteins back into shape.
  - 4:32.9 ON-SCREEN: SPEEDBARS 701 M vs 4,000 M
  - 4:35.3 ON-SCREEN: TAG `TMAO (FROM DEEP FISH)`
- 4:39.7 VO: Your fourth fix: you pack your cells with it. The shaking stops.
  - 4:40.0 ON-SCREEN: HUD BORROWED 4: TMAO (DEEP FISH)
- 4:43.0 VO: But there's a ceiling: the deeper you go, the more you need, and around 8,200 metres your cells get as concentrated as the sea.
  - 4:43.0 ON-SCREEN: TMAO-vs-depth line climbs to the dashed `AS CONCENTRATED AS SEAWATER` line at 8,200 M
- 4:51.0 VO: In 2014, scientists predicted that's where fish run out. It's the wall on your route.
  - 4:51.0 ON-SCREEN: DATE CHIP 2014
  - 4:53.4 ON-SCREEN: HUD red 8,200 mark pulses: `THE WALL`

#### [L9 THE ABYSS PLAIN · LOW POINT -> TURN] 4:56.8–5:29.7 (TTS 207 wpm)
- 4:56.8 VO: The trench is still days away. So you walk.
  - 4:56.8 ON-SCREEN: STAMP `DAY 4 · THE ABYSS PLAIN`; map inset: dashed line two-thirds done
- 4:59.5 VO: Then a brand-new problem: you're starving.
- 5:01.9 VO: Staying warm burns food, and about 1 percent of what grows in sunlight ever reaches this mud.
  - 5:04.3 ON-SCREEN: STAT `~1% OF SUNLIT FOOD REACHES THE FLOOR`
- 5:07.7 VO: The remora has gone quiet.
  - 5:07.7 ON-SCREEN: REMORA chip: QUIET
- 5:09.6 VO: So, honestly, where could you live?
  - 5:09.6 ON-SCREEN: OPTIONS `WHERE COULD YOU LIVE?` OPEN OCEAN · ABYSS · VENT · REEF
- 5:11.7 VO: The open ocean? Nothing to eat. The abyss? You're in it.
  - 5:12.5 ON-SCREEN: strike OPEN OCEAN
  - 5:14.1 ON-SCREEN: strike ABYSS
- 5:15.0 VO: Unless you find a vent, a hot spring on the seafloor crowded with life.
  - 5:15.6 ON-SCREEN: VENT tile (hypothetical); chip ALVIN · 1977
- 5:19.1 VO: But your best home is a coral reef, 30 metres down, still in the sunshine.
  - 5:19.7 ON-SCREEN: REEF tile; select REEF
- 5:23.6 VO: Except you can't go back up. Not in a body tuned for the abyss.
  - 5:23.6 ON-SCREEN: red ✗ over the REEF tile: `CAN'T GO BACK UP`
- 5:27.4 VO: And then, ahead of you, the floor just ends.
  - 5:29.2 ON-SCREEN: the mud edge drops into black

#### [L10 CLIMAX · THE LINE -> CHALLENGER DEEP] 5:30.1–6:13.4 (TTS 207 wpm)
- 5:30.1 VO: 8,200 metres. The trench walls close in.
  - 5:30.1 ON-SCREEN: STAMP `8,200 M · THE LINE`; DAYS 5
- 5:33.8 VO: Right at the line, a pale fish drifts past like a wet tissue. A snailfish.
- 5:38.2 VO: One trench north, in 2022, a camera filmed its cousin at 8,336 metres. No fish has ever been seen deeper.
  - 5:38.7 ON-SCREEN: MAP pin IZU-OGASAWARA TRENCH; DATE CHIP 2022; DepthMeter mark 8,336 M beside the red 8,200
- 5:47.3 VO: This is the wall. There's no animal left to borrow from.
  - 5:47.8 ON-SCREEN: HUD BORROWED flips to `NO FIX LEFT` (red)
- 5:50.8 VO: The remora lets go and drifts back up toward the light.
  - 5:50.8 ON-SCREEN: REMORA chip: LEAVING -> GONE
- 5:54.0 VO: From here on, this is our guess, not known science.
  - 5:54.0 ON-SCREEN: TAG `BEYOND KNOWN BIOLOGY`
- 5:57.0 VO: You can stay at the line, where your body still makes sense. Or pay for the last 2,700 metres with the only thing you have left: the way back.
  - 5:57.0 ON-SCREEN: two tiles: STAY AT THE LINE / GO DOWN 2,700 M · COST: THE WAY BACK
- 6:05.7 VO: You keep packing your cells past the limit. They swell with sea. They hold.
  - 6:05.7 ON-SCREEN: cells swell
- 6:09.9 VO: And they'll never work in the shallows again.
  - 6:09.9 ON-SCREEN: HUD line `WAY BACK: GONE`
- 6:12.3 VO: You go down.
  - 6:13.1 ON-SCREEN: HOLD: descent ramp, DepthMeter races 8,200 -> 10,900
- 6:13.5–6:15.5 HOLD (2.0 s): descent ramp, the meter races 8,200 -> 10,935; music drops to one low drone

#### [L10b THE FLOOR] 6:15.8–6:51.5 (TTS 207 wpm)
- 6:15.8 VO: 10,935 metres. Challenger Deep.
  - 6:15.8 ON-SCREEN: STAMP `10,935 M · CHALLENGER DEEP`; DAYS 6
- 6:20.1 VO: No light. No sound. Just a puff of grey mud where you land.
- 6:24.2 VO: Over 1,000 atmospheres: a small car parked on each of your thumbnails.
  - 6:24.2 ON-SCREEN: PRESSURE x1,000+
  - 6:26.0 ON-SCREEN: CAR on a thumbnail; STAT `~1.1 T / CM²`
- 6:29.2 VO: And finally, food. Amphipods, little shrimp-like scavengers, swarm over anything that sinks.
  - 6:31.2 ON-SCREEN: amphipods converge
- 6:35.2 VO: Down here, you're the thing that sank.
- 6:37.5 VO: You eat them. They nibble you back. Fair.
- 6:40.3 VO: In 2019, scientists opened up amphipods from this trench. Every single one had man-made fibres in its gut.
  - 6:40.6 ON-SCREEN: DATE CHIP 2019
  - 6:43.9 ON-SCREEN: magnifier on one amphipod: coloured fibres; STAT `100% HAD MAN-MADE FIBRES`
- 6:47.9 VO: Your first meal in 6 days, and your world got to it first.
  - 6:47.9 ON-SCREEN: one coloured fibre drifts past your face

#### [L11 BOOKEND + VERDICT + RECAP] 6:52.3–7:11.3 (TTS 207 wpm)
- 6:52.3 VO: You look up. 11 kilometres above you, the ferry is still crossing. The remora is up there somewhere.
  - 6:52.3 ON-SCREEN: camera rides up the whole column to the tiny ferry; REMORA chip: UP THERE SOMEWHERE
- 6:58.4 VO: So, could you breathe underwater? Yes. That part's easy.
  - 6:59.8 ON-SCREEN: HEADLINE `YES.`
- 7:01.9 VO: You'd need gills, salt pumps, a tuna's heat exchanger and a deep fish's chemistry. And you'd pay with the way home.
  - 7:01.9 ON-SCREEN: RECAP STRIP: 4 borrowed fixes + a red `WAY BACK ✗`
- 7:08.2 VO: Getting in was never the hard part. Getting out is.
  - 7:08.2 ON-SCREEN: HEADLINE on the trench floor

#### [L12 CTA + SERIES LOOP] 7:11.7–7:20.4 (TTS 207 wpm)
- 7:11.7 VO: So, back at that ferry rail: would you jump? And where would you stop: the reef, the vent, or the line?
  - 7:11.7 ON-SCREEN: END CARD from the ferry rail: REEF · VENT · THE LINE
- 7:17.1 VO: Want to see what happens when you try to swim back up? Tell me.
  - 7:17.1 ON-SCREEN: TAG `NEXT: SWIM BACK UP?`
- 7:20.4–7:23.9 HOLD (3.5 s): end card, music out

### HUD state per scene (generator rule)

The core has no persistent overlay, so the generator emits one `whatif/Hud` layer into every scene except the title, verdict, recap and end cards. Its props are the state at the scene start, linear `depth` and `bodyTemp` tracks to the scene end, and a `changes` list (scene-local seconds) for the step values. `focus` modes (`route`, `meter`, `temp`, `borrowed`) enlarge one element to centre for that scene; `pressure: "auto"` = ×(1 + depth/10).

| scene | t | depth (m) | pressure | body °C | borrowed | days | remora | way back | HUD focus |
|---|---|---|---|---|---|---|---|---|---|
| s01-fall | 0:00.0 | 0 | x1 | 37.0 | 0 | — | — | — | — |
| s02-fine | 0:03.5 | 0 | x1 | 37.0 | 0 | — | — | — | — |
| s03-remora | 0:09.4 | 0 | x1 | 37.0 | 0 | — | — -> ATTACHED | — | — |
| s04-ferry-leaves | 0:13.5 | 0 | x1 | 37.0 | 0 | — | ATTACHED | — | — |
| s05-air-rule | 0:16.4 | 0 | x1 | 36.9 | 0 | — | ATTACHED | — | — |
| s06-route-map | 0:20.7 | 0 | x1 | 36.9 | 0 | — | ATTACHED | — | — |
| s07-route-ruler | 0:28.2 | 0 | x1 | 36.9 | 0 | — | ATTACHED | — | route |
| s08-go-down | 0:30.6 | 0 | x1 | 36.9 | 0 | — | ATTACHED | — | — |
| s09-title | 0:32.3 | — | — | — | — | — | — | — | hidden |
| s10-rule-change | 0:34.5 | 1 -> 2 | x1 | 36.9 | 0 | — | ATTACHED | — | — |
| s11-rule-promise | 0:38.1 | 2 -> 5 | x1 -> x2 | 36.9 | 0 | — | ATTACHED | — | — |
| s12-stays-human | 0:45.8 | 5 -> 8 | x2 | 36.8 -> 36.7 | 0 | — | ATTACHED | — | — |
| s13-oxygen | 0:53.5 | 8 -> 28 | x2 -> x4 | 36.7 -> 36.5 | 0 | — | ATTACHED | — | — |
| s14-flow | 0:58.5 | 28 -> 54 | x4 -> x6 | 36.5 -> 36.3 | 0 | — | ATTACHED | — | — |
| s15-lungs | 1:04.6 | 54 -> 72 | x6 -> x8 | 36.3 -> 36.2 | 0 | — | ATTACHED | — | — |
| s16-mouse | 1:09.0 | 72 -> 99 | x8 -> x11 | 36.2 -> 35.9 | 0 | — | ATTACHED | — | — |
| s17-no-voice | 1:15.4 | 99 -> 123 | x11 -> x13 | 35.9 -> 35.7 | 0 | — | ATTACHED -> RELIEVED | — | — |
| s18-gills | 1:21.0 | 123 -> 160 | x13 -> x17 | 35.7 -> 35.4 | 0 -> 1 GILLS | — | RELIEVED | — | — |
| s19-extraction | 1:29.7 | 160 -> 178 | x17 -> x19 | 35.4 -> 35.3 | 1 GILLS | — | RELIEVED | — | — |
| s20-easy-except | 1:34.2 | 178 -> 200 | x19 -> x21 | 35.3 -> 35.1 | 1 GILLS | — | RELIEVED | — | — |
| s21-200m | 1:39.2 | 200 -> 209 | x21 -> x22 | 35.1 -> 35.0 | 1 GILLS | — | RELIEVED | — | — |
| s22-pressure | 1:43.2 | 209 -> 221 | x22 -> x23 | 35.0 -> 35.0 | 1 GILLS | — | RELIEVED | — | — |
| s23-ears | 1:48.2 | 221 -> 236 | x23 -> x25 | 35.0 -> 34.9 | 1 GILLS | — | RELIEVED | — | — |
| s24-record | 1:54.2 | 236 -> 341 | x25 -> x35 | 34.9 -> 34.8 | 1 GILLS | — | RELIEVED | — | meter |
| s25-bluewhale | 2:00.8 | 341 -> 481 | x35 -> x49 | 34.8 -> 34.8 | 1 GILLS | — | RELIEVED -> UNBOTHERED | — | — |
| s26-salt | 2:06.3 | 481 -> 615 | x49 -> x63 | 34.8 -> 34.7 | 1 GILLS | — | UNBOTHERED | — | — |
| s27-salt-fix | 2:11.6 | 615 -> 723 | x63 -> x73 | 34.7 | 1 GILLS -> 2 SALT PUMPS | — | UNBOTHERED | — | — |
| s28-light | 2:15.8 | 723 -> 904 | x73 -> x91 | 34.7 -> 34.6 | 2 SALT PUMPS | — | UNBOTHERED | — | — |
| s29-fingertips | 2:22.9 | 904 -> 1,000 | x91 -> x101 | 34.6 -> 34.3 | 2 SALT PUMPS | — | UNBOTHERED | — | — |
| s30-1000m | 2:26.7 | 1,000 -> 1,054 | x101 -> x106 | 34.3 -> 34.2 | 2 SALT PUMPS | — | UNBOTHERED | — | — |
| s31-glow | 2:30.5 | 1,054 -> 1,123 | x106 -> x113 | 34.2 -> 34.1 | 2 SALT PUMPS | — | UNBOTHERED | — | — |
| s32-angler | 2:35.3 | 1,123 -> 1,205 | x113 -> x122 | 34.1 -> 34.0 | 2 SALT PUMPS | — | UNBOTHERED -> HIDING | — | — |
| s33-rugpull | 2:41.0 | 1,205 -> 1,321 | x122 -> x133 | 34.0 -> 33.9 | 2 SALT PUMPS | — | HIDING | — | temp |
| s34-blood-vs-water | 2:49.2 | 1,321 -> 1,377 | x133 -> x139 | 33.9 | 2 SALT PUMPS | — | HIDING | — | — |
| s35-heat | 2:53.0 | 1,377 -> 1,527 | x139 -> x154 | 33.9 -> 33.8 | 2 SALT PUMPS | — | HIDING | — | — |
| s36-radiator | 3:03.5 | 1,527 -> 1,556 | x154 -> x157 | 33.8 | 2 SALT PUMPS | — | HIDING | — | — |
| s37-hypothermia | 3:05.6 | 1,556 -> 1,646 | x157 -> x166 | 33.8 | 2 SALT PUMPS | — | HIDING | — | temp |
| s38-tuna | 3:11.8 | 1,646 -> 1,693 | x166 -> x170 | 33.8 | 2 SALT PUMPS | — | HIDING | — | — |
| s39-retia | 3:15.1 | 1,693 -> 1,854 | x170 -> x186 | 33.8 -> 33.7 | 2 SALT PUMPS | — | HIDING | — | — |
| s40-exchanger | 3:26.3 | 1,854 -> 1,923 | x186 -> x193 | 33.7 -> 35.0 | 2 SALT PUMPS -> 3 HEAT EXCHANGER | — | HIDING | — | — |
| s41-keep-swimming | 3:31.1 | 1,923 -> 2,000 | x193 -> x201 | 35.0 -> 36.2 | 3 HEAT EXCHANGER | — | HIDING | — | — |
| s42-2000m-click | 3:36.5 | 2,000 -> 2,441 | x201 -> x245 | 36.2 | 3 HEAT EXCHANGER | — | HIDING | — | — |
| s43-spermwhale | 3:44.2 | 2,441 -> 2,703 | x245 -> x271 | 36.2 | 3 HEAT EXCHANGER | — | HIDING | — | — |
| s44-in-the-beam | 3:48.9 | 2,703 -> 2,901 | x271 -> x291 | 36.2 | 3 HEAT EXCHANGER | — | HIDING -> RELOCATING | — | — |
| s45-turns-away | 3:52.4 | 2,901 -> 3,092 | x291 -> x310 | 36.2 | 3 HEAT EXCHANGER | — | RELOCATING | — | — |
| s46-giant-squid | 3:55.7 | 3,092 -> 3,360 | x310 -> x337 | 36.2 | 3 HEAT EXCHANGER | — | RELOCATING | — | — |
| s47-midpoint | 4:00.5 | 3,360 -> 3,709 | x337 -> x372 | 36.2 | 3 HEAT EXCHANGER | — | RELOCATING | — | — |
| s48-way-back | 4:06.6 | 3,709 -> 4,000 | x372 -> x401 | 36.2 | 3 HEAT EXCHANGER | — | RELOCATING | — -> ? | — |
| s49-4000m | 4:11.8 | 4,000 | x401 | 36.2 | 3 HEAT EXCHANGER | 1 | RELOCATING | ? | — |
| s50-proteins | 4:20.6 | 4,000 | x401 | 36.2 | 3 HEAT EXCHANGER | 1 | RELOCATING | ? | — |
| s51-chamber | 4:25.7 | 4,000 | x401 | 36.2 | 3 HEAT EXCHANGER | 1 | RELOCATING | ? | — |
| s52-deeper | 4:32.9 | 4,000 | x401 | 36.2 | 3 HEAT EXCHANGER -> 4 TMAO | 1 | RELOCATING | ? | — |
| s53-limit | 4:43.0 | 4,000 | x401 | 36.2 | 4 TMAO | 1 | RELOCATING | ? | — |
| s54-walk | 4:56.8 | 4,000 | x401 | 36.2 | 4 TMAO | 4 | RELOCATING | ? | — |
| s55-starving | 4:59.5 | 4,000 | x401 | 36.2 | 4 TMAO | 4 | RELOCATING -> QUIET | ? | — |
| s56-options | 5:09.6 | 4,000 | x401 | 36.2 | 4 TMAO | 4 | QUIET | ? | — |
| s57-vent | 5:15.0 | 4,000 | x401 | 36.2 | 4 TMAO | 4 | QUIET | ? | — |
| s58-reef | 5:19.1 | 4,000 | x401 | 36.2 | 4 TMAO | 4 | QUIET | ? | — |
| s59-cant-go-back | 5:23.6 | 4,000 | x401 | 36.2 | 4 TMAO | 4 | QUIET | SHRINKING | — |
| s60-edge | 5:27.4 | 4,000 -> 5,224 | x401 -> x523 | 36.2 | 4 TMAO | 4 | QUIET | SHRINKING | — |
| s61-8200m | 5:30.1 | 5,224 -> 8,200 | x523 -> x821 | 36.2 | 4 TMAO | 5 | QUIET | SHRINKING | — |
| s62-cousin | 5:38.2 | 8,200 | x821 | 36.2 | 4 TMAO | 5 | QUIET | SHRINKING | — |
| s63-wall | 5:47.3 | 8,200 | x821 | 36.2 | 4 TMAO -> NO FIX LEFT | 5 | QUIET | SHRINKING | borrowed |
| s64-remora-leaves | 5:50.8 | 8,200 | x821 | 36.2 | NO FIX LEFT | 5 | LEAVING -> GONE | SHRINKING | — |
| s65-guess | 5:54.0 | 8,200 | x821 | 36.2 | NO FIX LEFT | 5 | GONE | SHRINKING | — |
| s66-decision | 5:57.0 | 8,200 | x821 | 36.2 | NO FIX LEFT | 5 | GONE | SHRINKING | — |
| s67-cells | 6:05.7 | 8,200 | x821 | 36.2 | NO FIX LEFT | 5 | GONE | SHRINKING -> GONE | — |
| s68-ramp | 6:12.3 | 8,200 -> 10,935 | x821 -> x1,000+ | 36.2 | NO FIX LEFT | 5 | GONE | GONE | — |
| s69-floor | 6:15.8 | 10,935 | x1,000+ | 36.2 | NO FIX LEFT | 6 | GONE | GONE | — |
| s70-thumbnail-car | 6:24.2 | 10,935 | x1,000+ | 36.2 | NO FIX LEFT | 6 | GONE | GONE | — |
| s71-amphipods | 6:29.2 | 10,935 | x1,000+ | 36.2 | NO FIX LEFT | 6 | GONE | GONE | — |
| s72-eat | 6:35.2 | 10,935 | x1,000+ | 36.2 | NO FIX LEFT | 6 | GONE | GONE | — |
| s73-fibres | 6:40.3 | 10,935 | x1,000+ | 36.2 | NO FIX LEFT | 6 | GONE | GONE | — |
| s74-fibre-face | 6:47.9 | 10,935 | x1,000+ | 36.2 | NO FIX LEFT | 6 | GONE | GONE | — |
| s75-look-up | 6:52.3 | 10,935 | x1,000+ | 36.2 | NO FIX LEFT | 6 | GONE -> UP THERE SOMEWHERE | GONE | — |
| s76-verdict | 6:58.4 | — | — | — | — | — | — | — | hidden |
| s77-recap | 7:01.9 | — | — | — | — | — | — | — | hidden |
| s78-thesis | 7:08.2 | — | — | — | — | — | — | — | hidden |
| s79-endcard | 7:11.7 | — | — | — | — | — | — | — | hidden |
| s80-series | 7:17.1 | — | — | — | — | — | — | — | hidden |

### On-screen text (summary)

- HUD from frame 1 (see the table): DepthMeter 0 -> 253 -> 1,000 -> 2,000 -> 4,000 -> 8,200 -> 10,935 M with route marks lit at 0:28 (8,200 red: THE WALL) plus 253 / 701 / 8,336 marks when spoken; PRESSURE ×1 -> ×1,000+; BODY 37.0 -> 34.9 at 253 m -> 33.7 -> 36.2 °C (35° line); BORROWED 1 GILLS -> 2 SALT PUMPS -> 3 HEAT EXCHANGER -> 4 TMAO -> NO FIX LEFT; DAYS 1 -> 4 -> 5 -> 6; REMORA ATTACHED / RELIEVED / UNBOTHERED / HIDING / RELOCATING / QUIET / LEAVING / GONE / UP THERE SOMEWHERE; WAY BACK ? -> SHRINKING -> GONE.
- Stamps (centred, ~2 s): 200 M · THE LAST LIGHT / 1,000 M · MIDNIGHT / 2,000 M · THE HUNTING GROUND / 4,000 M · THE ABYSS / DAY 4 · THE ABYSS PLAIN / 8,200 M · THE LINE / 10,935 M · CHALLENGER DEEP.
- Title card 0:32.3-0:34.5: WHAT IF YOU COULD BREATHE UNDERWATER? ("UNDERWATER?" red), VO over it.
- Problem tags: PROBLEM 1: SALT · PROBLEM 2: LIGHT · PROBLEM 3: THE NEIGHBOURS. Flags: REAL ANIMAL: BLUEFIN TUNA · BEYOND KNOWN BIOLOGY.
- Date chips: 1966, 1992, 2014, 1977, 2022, 2019.
- End card: WOULD YOU JUMP? · REEF · VENT · THE LINE · NEXT: SWIM BACK UP?

### Open loops

| opens | loop | closes |
|---|---|---|
| 0:03 | "and you're fine": how? | 1:21-1:29 gills |
| 0:04 | the BODY readout ticks down, unexplained | named at 0:50, paid by the rug pull 2:44-3:05, fixed 3:26 |
| 0:09 | the remora (a mute companion) | a readout at every stop; leaves at the wall 5:50; "up there somewhere" 6:52 |
| 0:16 | you can't climb back on (one-way rule) | 4:06 plant -> 5:23 -> spent 5:56-6:09 -> stranding 6:52-7:08 |
| 0:20-0:28 | master: the deepest floor, and one line on the way is a wall | wall named 4:51, hit 5:47, floor 6:15 (85%) |
| 0:44 | "until there isn't one" | 5:47 NO FIX LEFT |
| 1:34 | "one more thing... you won't feel it yet" | 2:44 |
| 2:15 | no fix for light | 2:30 everything here makes its own light |
| 2:22 | white fingertips, waved away | 3:05 hypothermia, passed at ~200 m |
| 3:31 | you can never stop swimming (it burns food) | 4:59 starving -> 6:29-6:47 food |
| 3:36 | the click: who, and is it for you? | 3:44-3:52 |
| 5:09 | where could you actually live? | 5:19 reef, struck 5:23; reopened as the CTA 7:11 (left to the comments) |
| 7:17 | what happens if you swim back up | left open for the next episode |

## Shot list

Kit vocabulary: core layers (`rect`, `circle`, `text`, `svg`, `particles` presets bubbles/dust/snow/embers/rain/stars, `component`), core camera (`pushIn`, `pullOut`, `panUp`, `panDown`, `panLeft`, `panRight`, `drift`, keyframes, `shake`), transitions (`cut`, `fade`, `dipBlack`, `whip`, `glitch`), static per-scene `grade`, core word-level `captions`, explainer kit (`explainer/Ocean` with a `depth` track, `surface`, `rays`, `snow`; `DepthMeter`; figures `BlueWhale` `SpermWhale` `ColossalSquid` (drawn with `hooks: false` as the giant-squid stand-in) `Anglerfish` `Diver` `You` `Bus` `Car` `Krill` (amphipod stand-in); `ScaleBar`, `Stat`, `SpeedBars`, `Options`, `Timer`, `Map`, `Headline`, `Tag`), SFX from `studio/public/sfx`, music from `studio/public/music`. Every creature in a shot shares one `pxPerM`.

**New-asset budget (was ~28 items):**
- NEW components (4), in `studio/src/kits/whatif/` (create `index.tsx` and add `import './whatif';` to `studio/src/kits/index.ts`; re-read that shared file first): `whatif/Hud` (wraps DepthMeter + readouts + chips; props in the HUD table), `whatif/Ferry` (hull + lit deck rail silhouette, `lights`), `whatif/GillDiagram` (head profile with slit strokes on a circle head; `mode: oxygen | salt | heat | strip`, `flip`, `slitsAt`, `flowAt`), `whatif/Fish` (one parametrised figure: `species: remora | tuna | snailfish | deepfish`, `cutaway` (vessel tangle in the swimming muscle), `translucent`, `pxPerM`).
- Kit edit (1): `explainer/DepthMeter` `marks: [{d, label, color, at}]` (~20 lines in `kits/explainer/ocean.tsx`). The ruler is linear, so shallow marks (200, 253) are shown with `focus: meter` + `window: 400` zooms, not a log scale.
- Everything else is core layers or inline SVG strings defined in `gen_storyboard.py` (seafloor, trench walls, protein ribbon, TMAO dots and chart, vent and reef tiles, jar + mouse, lung pipe, speech bubble, radiator, coil, cells, fibre magnifier, water arrows). Snow thinning = two crossfaded `particles` layers; light fading = the Ocean `depth` track; tints inside a shot = full-frame `rect` with opacity keyframes; click rings = `circle` layers with scale keyframes.

80 shots, contiguous 0:00 -> 7:23.9, longest s53-limit 13.79 s (all ≤15 s).

| # | t_start | t_end | shot type | visual description (kit vocabulary) | camera move | SFX |
|---|---|---|---|---|---|---|
| 1 | 0:00.0 | 0:03.5 | STORY wide, split waterline | `explainer/Ocean` `surface: 0.35`, dusk `skyTop` violet / `skyBottom` orange; NEW `whatif/Ferry` slides right->left along the waterline with a lit deck rail; `You` `pose: panic` just under the surface in a `particles` bubbles burst; HUD from frame 1 (DEPTH 0 M, BODY 37.0); `Tag` WESTERN PACIFIC | `shake` 0.4 s on the fall, then hold | `impact` splash; `bubbles` until the fine beat |
| 2 | 0:03.5 | 0:09.4 | STORY medium underwater | Bubbles gone; `You` relaxes to `pose: stand`, floating upright (`idle` float); a slow chest-rise `svg` arc pulses (`idle` breathe); light from above flickers | slow `pushIn` | bubbles cut dead; `heartbeat_slow` |
| 3 | 0:09.4 | 0:13.5 | STORY medium, companion intro | NEW `whatif/Fish` `species: remora` (~0.6 m, shared `pxPerM`) swims in from the left and latches on between `You`'s shoulders; HUD REMORA chip `ATTACHED` pops | `pushIn` on the latch | `pop` on the latch |
| 4 | 0:13.5 | 0:16.4 | STORY wide, split waterline (POV stand-in) | The 0:00 split frame again: the `whatif/Ferry` shrinks by keyframes (scale 1 -> 0.35) while tiny deck-rail `circle` heads stay lit; `You` small below the waterline with the remora | small `panUp` | `underwater_rumble` (engine) fading |
| 5 | 0:16.4 | 0:20.7 | STORY medium, rule beat | `You` reaches up toward the bright surface line; a red `rect` strike draws across the surface (the one-way rule); `Tag` AIR: DOESN'T WORK FOR YOU | static | `tick` on the strike |
| 6 | 0:20.7 | 0:28.2 | GRAPHIC map + stat | `Stat` 4,000 M TO THE FLOOR; then `explainer/Map` inset (western Pacific, zoom 3): pin YOU, dashed 300 KM line, pin CHALLENGER DEEP | `pullOut` | `tick`, `ding` on the pin |
| 7 | 0:28.2 | 0:30.6 | GRAPHIC full-height ruler (route) | HUD `focus: route`: the DepthMeter grows to full frame height, `max: 11000`; route marks light one by one 200 · 1,000 · 2,000 · 4,000 · **8,200 (red, THE WALL?)** · 10,935 (kit edit: DepthMeter `marks`) | `pullOut` | `tick` x5, soft `stinger` on the red line |
| 8 | 0:30.6 | 0:32.3 | STORY vertical descent | `You` rotated head-down (`rotate: 160`, `pose: run` as a kick) with the remora on its back; Ocean `depth` track starts (HUD meter leaves 0 for good) | `panDown` | `whoosh`; `riser` into the title |
| 9 | 0:32.3 | 0:34.5 | TITLE card (VO over it, no dead hold) | `explainer/Headline` WHAT IF YOU COULD / BREATHE UNDERWATER? (`red: [UNDERWATER?]`, underline) over Ocean `depth: 25`, `snow: 60`; HUD hidden for the card | static | `stinger`; music hit |
| 10 | 0:34.5 | 0:38.1 | RULE card | `You` floating with water `svg` arrows in through the mouth and out at the neck; `Tag` ONE CHANGE: OXYGEN FROM WATER | `drift` | soft `whoosh` |
| 11 | 0:38.1 | 0:45.8 | RULE card | `explainer/Options` title THE RULES, items EVERY THREAT -> A REAL ANIMAL'S FIX · UNTIL THERE ISN'T ONE (`itemAt` synced, second item drawn with a red `Tag` overlay) | static | `pop` per rule |
| 12 | 0:45.8 | 0:53.5 | RULE card + plant | `Options` STAYS HUMAN: SKIN · EYES · 37°C BLOOD (`stagger 0.8`); at r5 a pointer `circle` ring lands on the HUD BODY readout (36.8 and falling) | static, small `pushIn` | `pop` x3; `ding` on the plant |
| 13 | 0:53.5 | 0:58.5 | BOARD diagram (register switch) | Dark panel `rect` over the descending Ocean (meter keeps moving); `SpeedBars` OXYGEN PER LITRE: AIR 100 vs SEAWATER 3 (`text` ~1/30) | `cut` in; static | `tick` on the bars |
| 14 | 0:58.5 | 1:04.6 | BOARD diagram | `SpeedBars` THROUGH YOU EVERY MINUTE: AIR 6 L vs WATER 60 L; at g3 a `Timer` ring 2:30 spins next to `Tag` 1 BATHTUB | slow `pushIn` | `bubbles` (filling) |
| 15 | 1:04.6 | 1:09.0 | BOARD diagram | Inline `svg` lung with one pipe and arrows in AND out; a red ✗ `Tag` SAME PIPE IN AND OUT | static | light `impact` on the ✗ |
| 16 | 1:09.0 | 1:15.4 | HISTORY vignette | Inline `svg` jar + mouse silhouette in liquid on the dark panel; date `Tag` 1966; the mouse's chest `idle` breathe | `pushIn` | `ding` on the date; quiet `bubbles` |
| 17 | 1:15.4 | 1:21.0 | STORY gag beat | `You` close, mouth-open pose (`panic`); an empty speech-bubble `svg` with `...` pops; at g7 the remora chip reads RELIEVED and the `whatif/Fish` remora does a little `idle` sway | `pushIn` | silence beat, `pop` on the bubble |
| 18 | 1:21.0 | 1:29.7 | DIAGRAM (gills) | NEW `whatif/GillDiagram` `mode: oxygen`: head profile (circle head at close scale) with three slit strokes drawing on behind the jaw at g8+2.4; then one-way arrows mouth -> gills (conveyor texture) and the two-lane counter-current strip WATER -> / <- BLOOD with dots crossing; HUD BORROWED 1 | `drift`, then `pushIn` on the strip | `pop` + `ding` on the fix; `whoosh` on the arrows |
| 19 | 1:29.7 | 1:34.2 | BOARD diagram | `SpeedBars` OXYGEN TAKEN: GILLS 80% vs LUNGS 25% | static | `pop` on the bars |
| 20 | 1:34.2 | 1:39.2 | STORY wide (false resolution) | `You` swimming down easily; `Tag` EASY. then a red `Tag` EXCEPT... replaces it; the HUD BODY readout blinks once (HUD `blink: temp` change) | slow `panDown` | one `tick` on EXCEPT |
| 21 | 1:39.2 | 1:43.2 | STAMP + wide sunlit zone | Stamp 200 M · THE LAST LIGHT; Ocean (auto depth) `rays: 7`, `snow: 40`; `You` swimming down (rotated 75°) with the remora | `panDown` slow | `whoosh` on the stamp |
| 22 | 1:43.2 | 1:48.2 | STORY inset comparison | Inset left: `Diver` with an air-bubble `circle` that shrinks by keyframes (scale 1 -> 0.3) as PRESSURE ticks x1 -> x21; inset right: `You` with a water glyph that stays the same size | static | light `tick` per atmosphere |
| 23 | 1:48.2 | 1:54.2 | STORY close-up | `You` head close (`pxPerM` 300); short water `svg` arrows into the ear and nose; `Tag` EARS + SINUSES: FLOODED | `pushIn` | soft `bubbles` |
| 24 | 1:54.2 | 2:00.8 | HUD close-up | HUD `focus: meter` with DepthMeter `window: 400`; the yellow mark 253 M · BREATH-HOLD RECORD appears and the YOU marker slides past it | `pushIn` on the ruler | `tick`; `whoosh` as it passes |
| 25 | 2:00.8 | 2:06.3 | STORY wide, scale | `BlueWhale` passes beneath, left -> right, same `pxPerM` (14) as `You`; two `Bus` silhouettes end to end in a lower inset; `ScaleBar` ~28 M | `panRight` tracking the whale | `underwater_rumble` swell |
| 26 | 2:06.3 | 2:11.6 | BOARD diagram (problem 1) | `Tag` PROBLEM 1: SALT; `SpeedBars` SALT: SEAWATER ~35 G/L vs YOUR BLOOD ~9 G/L | `cut`; static | `tick` on the problem |
| 27 | 2:11.6 | 2:15.8 | DIAGRAM (gills, salt mode) | `whatif/GillDiagram` `mode: salt`: white salt dots leave through cells on the gill strip; HUD BORROWED 2 | `pushIn` | `pop` + `ding` |
| 28 | 2:15.8 | 2:22.9 | STORY wide (problem 2) | `Tag` PROBLEM 2: LIGHT; `Stat` LIGHT 1%; the auto-depth Ocean fades the rays as the meter passes ~300 m | slow `panDown` | `tick` |
| 29 | 2:22.9 | 2:26.7 | STORY insert (the crack) | Two `You` layers crossfade (`color` #F3F6F7 -> pale blue #CFE3F2) with opacity keyframes; `Tag` FINGERTIPS: WHITE; the HUD BODY readout reads 34.6, already below the 35 line (nobody says so yet) | `pushIn` | `heartbeat_slow` |
| 30 | 2:26.7 | 2:30.5 | STAMP + wide black water | `dipBlack` into the stamp 1,000 M · MIDNIGHT; Ocean depth ~1,000 (black), `snow: 30`; `Stat` LIGHT 0% | `drift` | music drops to `drone` |
| 31 | 2:30.5 | 2:35.3 | STORY wide (wonder) | `particles` `stars` preset in cyan/blue blinking around `You` (bioluminescence); `Stat` ~3 IN 4 GLOW | `drift` | soft `ding` blips with the glows |
| 32 | 2:35.3 | 2:41.0 | STORY close, scale (problem 3) | `Tag` PROBLEM 3: THE NEIGHBOURS; `Anglerfish` (lure glow) rises to `You`'s face at the same `pxPerM` (300); `ScaleBar` ~0.2 M beside the open hand; at m4 the remora slides behind the head (keyframes) | slow `pushIn` | `pop` on the lure |
| 33 | 2:41.0 | 2:49.2 | RUG PULL (grade + HUD fly-in) | Frame grades to near-black (`grade` vignette 0.6, brightness 0.6); at m6+2.6 HUD `focus: temp` flies the BODY readout to centre, big, red (33.9°C) | hard `pushIn` on the readout | `stinger` + `heartbeat` |
| 34 | 2:49.2 | 2:53.0 | BOARD numbers | `Stat` 37°C (red) left vs `Stat` WATER 4°C (blue) right | static | `pop` x2 |
| 35 | 2:53.0 | 3:03.5 | DIAGRAM (gills, heat mode) | `whatif/GillDiagram` `mode: heat`: red heat dots leave with the water stream; at m9 `Stat` SURFACE: x30 small, at m10 `Stat` HERE: x100 (sub ~10 KW vs ~100 W) | `pullOut` | `whoosh_long` |
| 36 | 3:03.5 | 3:05.6 | DIAGRAM metaphor | Radiator `svg` icon replaces the gill slits on `You`'s neck; wavy heat lines drift out into a wide black ocean | `pullOut` (the room is the ocean) | `whoosh_long` |
| 37 | 3:05.6 | 3:11.8 | HUD close + body | HUD `focus: temp` with the 35° HYPOTHERMIA line on the readout scale (readout 33.8, blinking); `Tag` PASSED AT ~200 M; at m12+2.8 frost-blue tint `rect` fades in and `You` gets an `idle` jitter | static, small `shake` on 'minutes' | `heartbeat_slow` slowing |
| 38 | 3:11.8 | 3:15.1 | REAL-ANIMAL vignette | `whip` in; NEW `whatif/Fish` `species: tuna` (~2.5 m) crosses at mid-depth; `Tag` REAL ANIMAL: BLUEFIN TUNA | `panLeft` with the fish | `whoosh` |
| 39 | 3:15.1 | 3:26.3 | DIAGRAM cutaway | `whatif/Fish` tuna `cutaway: true`: the vessel tangle in the red swimming muscle, counter-flow arrows warm red <-> cold blue; at f3+0.6 the gill counter-current strip (GillDiagram `mode: strip`, `flip: true`) slides in beside it with its labels flipped (callback) | `drift` | `tick` on the flip |
| 40 | 3:26.3 | 3:31.1 | STORY close (fix 3) | `You` torso close with a coil `svg` (red/blue lanes) between the neck slits and the chest; tint `rect` warms back; HUD BORROWED 3; BODY readout climbs | `pushIn` | `pop`; `ding` |
| 41 | 3:31.1 | 3:36.5 | STORY wide | `You` kicking hard downward (`pose: run`, rotated), remora on board; `Tag` STOP SWIMMING = FREEZE | `panDown` | `whoosh` |
| 42 | 3:36.5 | 3:44.2 | STAMP + clicks | Stamp 2,000 M · THE HUNTING GROUND; full-frame expanding `circle` stroke rings (one per click), `shake` 0.15 s on each; at n2 the rings come faster until they blur | `shake` on each click | `click` (loud) accelerating; `sonar_ping` tail |
| 43 | 3:44.2 | 3:48.9 | STORY wide, scale (threat) | `SpermWhale` (`jaw: 4`) glides toward `You` at shared `pxPerM` (60); `ScaleBar` ~16 M; `Tag` CLICKS -> BUZZ = CLOSING IN | `panLeft` tracking | `click` x3 |
| 44 | 3:48.9 | 3:52.4 | STORY medium (threat) | `You` small in the whale's path; ring layers converge on `You` (buzz); at n5 the remora slides around to the far side (keyframes) | `pushIn` | buzz (rapid `click`) |
| 45 | 3:52.4 | 3:55.7 | STORY wide | One last ring hits `You` full-frame; the whale banks away (rotate + x keyframes) into the dark | `shake` on the buzz hit | `boom` (low) on the hit |
| 46 | 3:55.7 | 4:00.5 | STORY wide, scale | Giant squid stand-in: kit `ColossalSquid` figure with `hooks: false`, `scale` 1.1 to read as ~10 m at the shared `pxPerM` (60); eye-ring highlight + a dinner-plate `circle` icon; `Stat` GIANT SQUID · EYE ~27 CM | slow `pushIn` on the eye | `underwater_rumble` |
| 47 | 4:00.5 | 4:06.6 | GRAPHIC (midpoint re-hook) | `You` centre with three small fix icons (slits, salt dots, coil) orbiting (`idle` spin on a group `svg`); `Tag` BETTER DEEP · WORSE EVERYWHERE ELSE | `pushIn` | soft `stinger` |
| 48 | 4:06.6 | 4:11.8 | STORY vertical (stranding plant) | A `whatif/Fish` `species: deepfish` rises on a thin line toward a bright surface band; it loses shape (scaleY keyframes 1 -> 0.4, opacity down); HUD WAY BACK: ? appears | `panUp` with the fish | `riser`; `tick` on WAY BACK |
| 49 | 4:11.8 | 4:20.6 | STAMP + wide seafloor | Stamp 4,000 M · THE ABYSS; seafloor `svg` (mud mounds) along the bottom; `You` lands (`align: bottom`) with a `dust` particles puff; PRESSURE x401; DAYS chip DAY 1 appears | `pushIn` | soft `impact` on landing |
| 50 | 4:20.6 | 4:25.7 | DIAGRAM inset | Protein ribbon `svg` with `scaleY` keyframes 1 -> 0.45 (squashed); small `embers` particles as nerve sparks; `You` gets an `idle` jitter | static | faint `glitch` sparks |
| 51 | 4:25.7 | 4:32.9 | HISTORY vignette | `Diver` (stand-in for the chamber diver, no fins/bubbles) inside a rounded `rect` chamber with a porthole `circle`; date `Tag` 1992; HUD mark 701 M; at a5 `SpeedBars` 701 M vs 4,000 M | `cut`; `pushIn` on the porthole | `ding` on the date |
| 52 | 4:32.9 | 4:43.0 | BOARD + TMAO | `SpeedBars` HUMAN RECORD 701 M vs YOU 4,000 M; at a5+2.4 the protein ribbon returns with TMAO dot `svg` pushing it back (scaleY 0.45 -> 1); `Tag` TMAO (FROM DEEP FISH); HUD BORROWED 4 at a6 | `drift` | `pop`; `ding` on the fix |
| 53 | 4:43.0 | 4:56.8 | BOARD chart (tracker advance) | TMAO-vs-depth line chart `svg` revealed with `wipeRight`, climbing to the dashed red AS CONCENTRATED AS SEAWATER · ~8,200 M line; at a8 date `Tag` 2014 and the HUD red 8,200 mark pulses THE WALL | `pullOut` | short `riser`; `ding`; soft `stinger` |
| 54 | 4:56.8 | 4:59.5 | STAMP + wide plain | Stamp DAY 4 · THE ABYSS PLAIN; `You` walking (`pose: run`, small) across the mud `svg`; `Map` inset with the dashed line two-thirds drawn | `panRight` | muffled `footsteps` |
| 55 | 4:59.5 | 5:09.6 | STORY wide (low point) | `You` very small on the mud; marine snow thins (two `particles` `snow` layers crossfade, 90 -> 15); `Stat` ~1% OF SUNLIT FOOD REACHES THE FLOOR; at w4 the remora hangs limp (`idle` off) | slow `pullOut` (isolation) | `drone` only |
| 56 | 5:09.6 | 5:15.0 | OPTION board (hypothetical, no trip) | `Options` WHERE COULD YOU LIVE? OPEN OCEAN · ABYSS · VENT · REEF; `strikes` OPEN OCEAN at w6+0.8, ABYSS at w6+2.4 | static | `pop`; `tick` per strike |
| 57 | 5:15.0 | 5:19.1 | OPTION tile (vent) | The board slides left; a VENT tile (inline `svg`: chimney, shimmering plume, red-plumed tube worms) in a rounded frame; small chip ALVIN · 1977 (on screen only) | `pushIn` on the tile | `bubbles`; `ding` on the chip |
| 58 | 5:19.1 | 5:23.6 | OPTION tile (reef) | REEF tile (inline `svg`: bright water gradient, coral silhouettes, yellow fish ovals) beside the dimmed vent tile; `Tag` REEF · 30 M · STILL IN THE SUNSHINE | static | `pop`; brief music lift |
| 59 | 5:23.6 | 5:27.4 | OPTION tile + body | A red ✗ stamps over the REEF tile with `Tag` CAN'T GO BACK UP; HUD WAY BACK: SHRINKING | small `shake` on the ✗ | `impact` |
| 60 | 5:27.4 | 5:30.1 | STORY wide (turn) | Back on the plain; the mud edge `svg` drops away into black (trench lip) in front of `You` | `panRight` to the edge | `riser` |
| 61 | 5:30.1 | 5:38.2 | STAMP + trench | Stamp 8,200 M · THE LINE; two trench-wall polygon `svg` layers close in (x keyframes); at x2 NEW `whatif/Fish` `species: snailfish` (pale, translucent) drifts across | slow `pushIn` | `underwater_rumble`; `drone` |
| 62 | 5:38.2 | 5:47.3 | MAP + HUD | `Map` (Japan to the Marianas) with pin IZU-OGASAWARA TRENCH; date `Tag` 2022; HUD mark 8,336 M lands right beside the red 8,200 | `cut`; slow map zoom | `ding`; `tick` |
| 63 | 5:47.3 | 5:50.8 | HUD close (planted rule pays) | HUD `focus: borrowed`: the BORROWED counter flips to NO FIX LEFT in red; `Tag` THE WALL | `pushIn` | `stinger` |
| 64 | 5:50.8 | 5:54.0 | STORY (tender beat) | The remora lets go of `You`'s back and drifts up and away toward a faint glow (y + opacity keyframes); REMORA chip LEAVING -> GONE | small `panUp` with the remora | music thins to one soft line |
| 65 | 5:54.0 | 5:57.0 | GRAPHIC (honesty flag) | `glitch` in; `Tag` BEYOND KNOWN BIOLOGY; `grade` desaturates | static | `glitch` |
| 66 | 5:57.0 | 6:05.7 | DECISION board (climax choice) | Two tiles: left STAY AT THE LINE · YOU CAN STILL LIVE HERE; right GO DOWN 2,700 M · COST: THE WAY BACK (red); the right tile lights at x7 end | slow `pushIn` | `tick` per tile; `heartbeat_slow` |
| 67 | 6:05.7 | 6:12.3 | DIAGRAM (speculative) | Cells `svg` (ten teal circles) swell (scale keyframes 1 -> 1.25) and hold; at x9 HUD WAY BACK: GONE | `pushIn` | `bubbles`; soft `stinger` |
| 68 | 6:12.3 | 6:15.8 | DESCENT ramp (hold) | 'You go down.' then a 2 s hold: HUD meter races 8,200 -> 10,935; upward speed lines (`particles` `rain`, negative `speed`); Ocean near-black | fast `panDown` | `whoosh_long`; music drops to one low `drone` |
| 69 | 6:15.8 | 6:24.2 | STAMP + trench floor (sensory mirror) | Stamp 10,935 M · CHALLENGER DEEP; pale sediment floor `svg`; `You` lands, a grey `dust` puff; silence; inset `Map` pin MARIANA TRENCH | slow `pushIn` | near silence; soft `impact` on the landing |
| 70 | 6:24.2 | 6:29.2 | ICON comparison | PRESSURE x1,000+; at x13+1.8 a `Car` figure sits on a big rounded `circle` 'thumbnail'; `Stat` ~1.1 T / CM² | `pushIn` | `pop` on the icon |
| 71 | 6:29.2 | 6:35.2 | STORY medium, swarm | 12 `Krill` layers (amphipod stand-ins, 3-6 cm, shared `pxPerM` 600 near the camera) converge on `You` by keyframes; distant ones = `dust` particles | slow `pushIn` | faint `bubbles` |
| 72 | 6:35.2 | 6:40.3 | STORY close (hunger payoff) | Close on `You` among the swarm; `Tag` YOU ARE THE THING THAT SANK, then at x16 `Tag` FIRST MEAL IN 6 DAYS | `pushIn` | small `pop` |
| 73 | 6:40.3 | 6:47.9 | INSET (bathos) | Date `Tag` 2019; magnifier `svg` circle on one amphipod with red/blue/yellow fibre threads in its gut; `Stat` 100% HAD MAN-MADE FIBRES | `pushIn` on the inset | `ding` on the date and on 100% |
| 74 | 6:47.9 | 6:52.3 | STORY close | Close on `You`'s face; one coloured fibre `rect` (thin, red) drifts past by keyframes | very slow `pushIn` | silence, then soft `stinger` |
| 75 | 6:52.3 | 6:58.4 | VERTICAL callback (bookend) | `You` looks up; camera rides up the whole column (background Ocean `depth` track 10,935 -> 0) to the tiny `whatif/Ferry` at the surface, the 0:00 framing, with a tiny remora dot near the hull; the HUD keeps reading 10,935 M (you stay down) | `panUp` fast, easing out | `whoosh_long` |
| 76 | 6:58.4 | 7:01.9 | VERDICT board | `Headline` COULD YOU BREATHE UNDERWATER? then YES. (red) below | static | `ding` on YES |
| 77 | 7:01.9 | 7:08.2 | RECAP strip | Four fix icons pop left -> right (gill slits, salt dots, coil, protein ribbon) with labels FISH · FISH · TUNA · DEEP FISH, then a red fifth tile WAY BACK ✗ | static | `pop` x4; `impact` on the last tile |
| 78 | 7:08.2 | 7:11.7 | THESIS | Back on the trench floor; `You` standing small; `Headline` GETTING IN WAS NEVER THE HARD PART. / GETTING OUT IS. (OUT red) | slow `pullOut` | music swells gently |
| 79 | 7:11.7 | 7:17.1 | END CARD (callback to the ferry rail) | Top third: the lit `whatif/Ferry` rail at dusk (0:00 palette); `Headline` WOULD YOU JUMP?; three tiles rebuilt as layers (REEF tile `svg`, VENT tile `svg`, THE LINE = trench-wall `svg` pair + snailfish) with labels | static | `pop` per tile |
| 80 | 7:17.1 | 7:23.9 | END CARD + series loop | Same end card; `Tag` NEXT: SWIM BACK UP? slides in above the tiles; holds 3.5 s after the VO, music out | static | `ding`; music out by the end |

## Fact sheet (verify before recording; sources go in the description)

- **Oxygen in air vs seawater.** Air is 20.9% O2, ~275-285 mg O2/L at 15-25 °C. Air-saturated seawater holds ~6.5-8 mg/L at 15-25 °C (~10 mg/L near 2 °C), so ~30-40× less ("about 30 times").
- **60 L/min (EST.).** Resting VO2 ≈ 250 mL/min ≈ 0.36 g/min. 360 mg/min ÷ (7.4 mg/L × 0.8 extraction) ≈ 61 L/min. A bathtub ≈ 150 L, so one every ~2.5 min. Resting human ventilation ≈ 6 L/min of air.
- **1966 liquid-breathing mouse.** Clark L.C. & Gollan F., *Science* 152:1755 (1966): mice breathed oxygenated fluorocarbon and survived; the work of moving a dense liquid in and out (and CO2 removal) is the known limit.
- **Gill vs lung extraction.** Counter-current gills extract up to ~80% of dissolved O2 (often quoted 80-90%); human lungs remove ~25% of inhaled O2 (21% in, ~16% out).
- **Pressure.** +1 atm per ~10 m: 200 m ≈ 21 atm, 1,000 m ≈ 101, 2,000 m ≈ 201, 4,000 m ≈ 401, Challenger Deep ≈ 1,086 bar ≈ 1.1 tonne-force per cm² (a small car per thumbnail).
- **Why air stops working (the one-way rule).** Fish gill filaments collapse and stick together in air, so a gill-breather suffocates out of water; "air doesn't work for you anymore" follows from the one change rather than adding a second one.
- **Ears and sinuses (story consequence, flagged).** Breathing water floods the lungs only; the middle ears and sinuses still hold air, and without an air supply they could not be equalised. The script makes their flooding part of the one change ("Water floods your sinuses and ears"). Fish have no air spaces to squeeze. "No bends" is not claimed.
- **Deepest breath-hold.** Herbert Nitsch reached 253.2 m (No-Limits, Santorini, June 2012), widely cited as the deepest breath-hold dive; it was not ratified and he was injured. The AIDA-ratified No-Limits record is 214 m (Nitsch, Spetses, 2007). The VO says "the deepest anyone has dived on one breath is 253 metres", not "official record". Re-check on recording day: a 2026 report says Nitsch is attempting new No-Limits depths.
- **Blue whale.** Up to ~29-30 m (kit figure 28 m); a city bus ≈ 12 m, so "longer than two buses".
- **Salt.** Seawater ~35 g/L salts (~1,000 mOsm/kg) vs blood plasma ~290 mOsm/kg (~9 g/L NaCl-equivalent), so ~3.4× ("about 3 times saltier"). Marine bony fish drink seawater and excrete Na+ and Cl- through gill ionocytes (chloride cells).
- **Light.** The sunlit zone ends where ~1% of surface light remains, up to ~200 m in clear ocean; no usable sunlight below ~1,000 m.
- **Bioluminescence.** Martini & Haddock, *Scientific Reports* 7:45750 (2017): ~76% of observed animals (Monterey Bay, surface to 3,900 m) were bioluminescent, "around 3 in 4".
- **Anglerfish.** Most deep-sea anglerfish females are under ~20 cm (kit `Anglerfish` 0.2 m).
- **Cold.** ~4 °C at 1,000 m; 1-2 °C at abyssal depths. Western Pacific surface water near the Marianas ~27-29 °C.
- **Heat drain (EST., corrected).** Heat loss through gills is limited by blood flow, not water flow: if all cardiac output (~5 L/min ≈ 5.2 kg/min) passes the gills and leaves at water temperature (true for fish gills), Q ≈ 5.2 × 3.6 kJ/kg·K × ΔT. Surface (ΔT ≈ 8-12 K) ≈ 2.5-3.7 kW ≈ ×25-37 resting output (~100 W): "about 30 times". At 4 °C (ΔT ≈ 33 K) ≈ 10 kW ≈ ×100: "a hundred". Body heat capacity ≈ 245 kJ/K, so at the surface you lose ~1 °C every 1-2 min: the HUD readout is story-time compressed but crosses the 35 °C hypothermia line around 200 m, as the VO says. This is why almost all fish are ectotherms.
- **Tuna heat exchanger.** Bluefin tuna retia mirabilia (counter-current vessel bundles) in the red swimming muscle, viscera, brain and eyes keep tissue up to ~10-20 °C above water. The heart is NOT warmed: it is fed straight from the gills and runs at water temperature ("warm fish, cold heart"; Shiels et al.; Block & Finnerty). Ours sits between the gills and the body, which is the honest version of the idea. Tuna heat comes from never stopping (ram ventilation + muscle work).
- **Sperm whale.** Males ~16-18 m; foraging dives beyond 1,000 m, recorded past 2,000 m. Clicks up to ~236 dB re 1 µPa (Møhl et al. 2003), the loudest known animal sound (underwater dB, not comparable to air; don't compare to a jet on screen). When closing on prey the click rate rises into a "buzz" (Miller, Johnson & Tyack 2004; Madsen et al.). Sound travels ~1,500 m/s in seawater.
- **Giant squid (replaces colossal squid).** *Architeuthis dux*: worldwide including the western Pacific (first filmed alive off the Ogasawara Islands, Kubodera & Mori 2005); up to ~12-13 m with tentacles, ~150-275 kg; eyes ~27 cm, among the largest of any animal (Nilsson et al. 2012), "as wide as dinner plates". Sperm whales eat them. The colossal squid lives only in the Southern Ocean, so it is out. The kit `ColossalSquid` drawing with `hooks: false` is a visual stand-in only; the label says GIANT SQUID.
- **Deep fish brought up.** Many deep-sea fish die or are badly damaged when hauled to the surface (decompression and gas expansion in swim-bladder fish, temperature shock, pressure-adapted proteins and membranes). "Many deep fish ... don't survive the trip" is the honest wording. Extending this to you is flagged as speculation at 5:54.
- **High-pressure nervous syndrome.** Tremor, nausea and slowed thinking in deep saturation divers. Comex HYDRA X (1992): Théo Mavrostomos reached a simulated 701 m in a hyperbaric chamber in France, the deepest pressure a human has survived.
- **Pressure on proteins / TMAO.** Yancey P.H. et al., *PNAS* 111:4461 (2014): muscle TMAO rises linearly with depth and would make fish cells iso-osmotic with seawater at ~8,200-8,400 m, a proposed reason fish stop there. TMAO is an osmolyte, not salt, so the VO says "as concentrated as the sea".
- **Snailfish.** A *Pseudoliparis* snailfish filmed at 8,336 m in the Izu-Ogasawara Trench south of Japan (Aug-Sep 2022; announced April 2023 by Jamieson, Minderoo-UWA Deep Sea Research Centre, with Tokyo University of Marine Science and Technology). The Mariana snailfish (*P. swirei*) lives at ~6,900-8,000 m in the Mariana Trench, so the one at our line is the cousin "one trench north". No fish has been seen deeper.
- **Food at depth.** Only ~1-2% of surface production reaches the abyssal floor as marine snow (EST.; varies by region).
- **Hydrothermal vents.** First found February 1977 on the Galápagos Rift by DSV *Alvin*: warm vent water and dense chemosynthetic communities (tube worms, clams, mussels). Vent fields also exist along the Mariana arc and back-arc; the option board treats it as a hypothetical.
- **Coral reefs.** <1% of the seafloor, ~25% of known marine species (NOAA/UNEP); most reef-building corals live above ~30-50 m.
- **Geography.** The fall is set near Guam in the western Pacific; Challenger Deep (~11.37 °N, 142.59 °E) is ~300-340 km south-west of Guam ("a few hundred kilometres"). Floor depth west/south of Guam ~3-5 km ("4 kilometres", EST.). The 4-6 day walk is story time (~3 km/h).
- **Challenger Deep.** ~10,935 m (estimates 10,902-10,994 m); 10,935 - 8,200 = 2,735 m ("the last 2,700 metres").
- **Amphipods + fibres.** Jamieson A.J. et al., *Royal Society Open Science* 6:180667 (2019), "Microplastics and synthetic particles ingested by deep-sea amphipods in six of the deepest marine ecosystems on Earth": 100% of Mariana Trench individuals contained ingested particles; FTIR identified semi-synthetic (rayon, lyocell) and synthetic (nylon, polyethylene, PVA, etc.) fibres plus some natural ramie. The VO says "man-made fibres", the chip 100% HAD MAN-MADE FIBRES; cite the paper and the Newcastle University press release. *Hirondellea gigas* lives in Challenger Deep.
- **Remora (story device).** Real remoras live near the surface on sharks, rays and whales; the one that follows you to 8,200 m is a fictional companion. Say so in the description.

## Notes for the build lane

- **TTS timing pass (done on the Spark CPU, 4 threads, nice 10):** see `review.json` -> `tts_timing`. The section rates in the generator are set from that pass. Rebuild captions from the real Kokoro word timings, not from the estimated words in `storyboard.json`.
- **Cut list if the final read runs long** (keeps the runtime under 8:00 without touching a plant or payoff): g6-g7 (no-voice gag, ~5 s), h6 (~2 s), m12 first sentence (~2 s), n7 second sentence (~2 s), w6 (~3 s), x16 (~2 s). About 16 s in total.
- **Critical path:** `whatif/Hud` (used in every scene) -> `whatif/GillDiagram` (oxygen, salt, heat, strip) -> `whatif/Ferry` -> `whatif/Fish`. The DepthMeter `marks` edit is part of the Hud task.
- **10-second gate shot:** 2:41-2:53 (rug pull: HUD `focus: temp` fly-in, grade, then GillDiagram `mode: heat` with the ×30 / ×100 stats). It exercises the Hud, the grade, `Stat` and the GillDiagram at once.
- **Visual monotony below 1,000 m:** the auto Ocean is near-black below ~1,000 m, so the abyss and trench scenes lean on the mud and trench-wall SVGs, the warm vent/reef tiles and the pale snailfish for contrast; set `bottomColor` per zone (abyss mud-brown, trench blue-black) when the Hud lane wires backgrounds.
- **Audio:** every SFX cue named exists in `studio/public/sfx`. No pitch control, so the loud whale click is `click` at full volume plus `boom` on the buzz hit. The "single low note" is `drone` as an SFX. Music beds: tension_pulse, deep_ocean, dread, documentary_pulse.
- **Captions** sit at 88% height; stamps at 45%; HUD stays in the top-left 420 × 960 box, so the map and stat insets live in the right two-thirds.
- **Description:** fact-sheet sources; "AI-generated narration (synthetic voice); animation is code-drawn"; the remora and the last 2,700 m are fiction (flagged on screen at 5:54).

## Originality gate

`python3 scripts/originality_check.py backlog/whatif/whatif-breathe-underwater/script.md research/corpus research/library/transcripts` -> PASS (2026-11-01, run on this final text; result in review.json).
