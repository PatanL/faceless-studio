---
slug: whatif-breathe-underwater
niche: whatif
format: long_16x9 (1920x1080)
engine: power story (one change + one promise -> honeymoon -> numbered problems -> rug pull on the planted variable -> real analogue -> stranding) run along a one-way depth-stop ladder
working_title: "What If You Could Breathe Underwater, But Never Come Back Up?"   # rank 1 in titles.md; the bare same-premise title is retired to the description
generated_by: gen_storyboard.py (single source; edit the generator or script.template.md, never this file)
target_runtime_s: {{M:runtime}}      # {{RUNTIME_MMSS}} incl. 2.2 s title card (VO over it), 2.0 s descent ramp, 3.5 s end-card hold
target_runtime_range_s: [390, 480]   # TOPICS.md long-form window 6:30-8:00
runtime_at_kokoro_speed_1.2_s: {{M:runtime_at_speed_1.2}}   # measured fallback; a further 10% slower read would be {{M:runtime_if_10pct_slower}} s, and the cut list in "Notes for the build lane" brings that under 480
vo_words: {{M:words}}                # caption spelling; {{M:spoken_words}} words as Kokoro reads them (digits expanded)
words_per_min: {{M:wpm_overall}}     # over the full runtime; Kokoro am_michael speed 1.25 (measured 207 spoken wpm inside lines; {{M:lines_measured}}/{{M:lines_total}} lines timed from the Spark pass, the rest from its fit)
sentences: {{M:sentences}}           # mean {{M:mean_sentence}} words; {{M:punch_pct}}% are <=3-word punch lines
second_person_sentences: {{M:second_person_pct}}%   # {{M:second_person_sentences}} of {{M:sentences}}; PLAYBOOK §12 floor for power stories 45%; {{M:you_per_100}} you-words per 100
you_words_first_30s: {{M:you_first_30s}}   # IFOLOGY top-10 median 12
pivots_per_min: {{M:pivots_per_min}}  # {{M:pivots}} hits of but/except/until/unless/here's/problem/catch/though/instead; PLAYBOOK median 1.5, IFOLOGY winners 2.0
numbers_per_min: {{M:numbers_per_min}}   # {{M:numbers}} tokens (digits + number words, §9 counting) over the runtime; corpus range 1.3-8.2
hook: "{{M:hook_words}} words / {{M:hook_end}} s cold open; first sentence {{M:first_sentence_words}} words; 'And you're fine' at {{M:fine_at}} s; BODY readout falling from {{T:c3}}; route + wall at {{T:c8}}; DepthMeter moving from {{T:c9}}"
master_loop: "will you reach the deepest floor, past the wall, and what is left of you there?" opens {{T:c7}}-{{T:c9}}, wall paid {{T:x4}}, floor {{T:x11}} ({{P:x11}}%), stranding answered {{T:b1}}-{{T:b4}} ({{P:b4}}%)
tracker: "whatif/Hud: DepthMeter (moving from {{T:c9}}) + PRESSURE xN + BODY °C readout (falling from {{T:c3}}) + BORROWED fixes 0 -> 4 -> NO FIX LEFT + DAYS (from the abyss) + REMORA reaction chip + WAY BACK line; per-scene state table below"
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

Episode `whatif-breathe-underwater` · 16:9 · {{RUNTIME_MMSS}} · power story on a depth-stop ladder · one Kokoro narrator (CPU on the Spark), word-level burned-in captions. Built from the B3 ocean kit plus four small whatif components.

**Premise in one line.** You fall off a ferry in the western Pacific, gasp seawater, and you're fine. The rules give you one change (oxygen from water) and one promise (each time the ocean tries to kill you, you get the fix a real animal already uses, until there isn't one). You head for the deepest floor on Earth, pick up four borrowed fixes, hit the wall where fish run out at 8,200 m, and pay for the last 2,700 m with the way back.

**What we borrow vs what is ours.** Borrowed: beat order and timing shares, and devices (plant/payoff, rules card, numbered problems, rug pull, flagged real analogue, mute companion readout, stop stamps, tracker number, stranding, recap + choice CTA). Ours: the story (ferry, remora, BODY readout, borrowed-fix promise, the wall, the trade), every sentence, every fact chain, every visual. No reference wording, character, gag or footage is reused.

**What changed in this final version (critique round 1).** 12-word first line ("fine" at {{M:fine_at}} s); the tracker moves in the hook (BODY readout from {{T:c3}}, DepthMeter from {{T:c9}}); the heat drain is reframed as T4 (killing you since the ferry, blood-flow-limited ×30 at the surface, ×100 at 4 °C, hypothermia crossed at ~200 m); giant squid replaces colossal squid; the one-way rule, the trench geography and the borrowed-fix promise are in the rules; the sperm whale is a threat at the midpoint, followed by the stranding plant; the hunger loop pays on the trench floor; a mute remora companion with a readout carries the tender beat; "upgrade 4" is gone: 8,200 m is the wall and the last 2,700 m costs the way back; numbered problem ladder; decision climax; numbers cut from 10.8/min to {{M:numbers_per_min}}/min; second person {{M:second_person_pct}}%; pivots {{M:pivots_per_min}}/min; new assets cut from ~28 to 4 components + 1 kit edit.

## Beat alignment table

| our beat | our timestamp | reference id + timestamp | device borrowed | how we adapt it |
|---|---|---|---|---|
| L1 Cold open: fall, gasp, fine | {{T:c1}}-{{T:c3}} | y300HjYnHPw @0:00-0:09 (4-word second-person open, power shown working by 0:02, micro-loop closed before 0:10); 6oZ9fdM0n50 @0:01-0:04 (second-person moment, list of absences) | short first sentence; show-before-tell; list of absences | 12-word first line with the impossible change; "And you're fine" at {{M:fine_at}} s; "No coughing. No burning." |
| L1 Companion + exception | {{T:c4}}-{{T:c5}} | _lu85gSD39k @0:24-0:29 (mute companion introduced in the hook; its reactions become a running readout); 6oZ9fdM0n50 @0:10-0:15 ("every person" -> self-correction leaves an exception) | mute sidekick whose reactions are a readout; "everyone... but you" narrowing | a remora latches on (thinks you're a shark) and gets a HUD chip; "Everyone up there breathes air. Everyone but you." |
| L1 One-way rule + route + wall + moving tracker | {{T:c6}}-{{T:c9}} | _lu85gSD39k @0:07 (one problem: it can never go back), @0:14-0:19 (destination tease); PLAYBOOK §2 combination rule (tracker already moving in the hook) | irreversible rule in the hook; whole route in the first 30 s; destination promise | "air doesn't work for you anymore. You can't climb back on"; map: the trench a few hundred km SW; route ticks light with the red 8,200 m "wall"; the meter starts moving at {{T:c9}} |
| L2 Title + rules + plant | {{T:t0}}-{{T:r5}} | y300HjYnHPw @0:11 (title question after the demo), @0:13-0:27 (one changed rule, what stays normal, "remember that") | title question; one-variable rule; explicit plant | title asked over a 2.2 s card (no dead hold); one change + the promise "until there isn't one"; the 37 °C plant points at a readout that is already falling |
| L3 Grounding while sinking | {{T:g1}}-{{T:g5}} | 6oZ9fdM0n50 @0:38-1:27 (first, the target -> real figure -> worked number -> time conversion); y300HjYnHPw @1:20-1:29 (scientists tested it, counter-intuitive limit) | baseline -> worked number -> one everyday conversion; dated lab precedent | 1/30 -> 60 L/min -> a bathtub every 2.5 min (the only conversion); 1966 liquid-breathing mouse; the meter runs 0 -> 200 m underneath |
| L3 Demo gag | {{T:g6}}-{{T:g7}} | y300HjYnHPw @0:56-1:16 (a demo scene with a double gag splits the number run) | consequence played as a gag, sidekick reaction | no air means no voice; the remora looks relieved |
| L3 Mechanism + false resolution (first turn) | {{T:g8}}-{{T:g11}} | y300HjYnHPw @1:38-1:42 (human limit vs "yours can" number pair); 6oZ9fdM0n50 @1:30 (one-word false resolution -> "except") | number pair; one-word false resolution + except | fix 1 gills: 80% vs 25%; "Easy. Except..." at {{T:g11}} ({{P:g11}}%) |
| L4 Honeymoon + numbered problems | {{T:h1}}-{{T:h11}} | y300HjYnHPw @1:48-2:38 ("at first" perks rising, first crack @2:23), @2:41-3:49 (numbered problem ladder, each with a fast fix); _lu85gSD39k @0:54 (stop card) | stamp; rising perks; famous record passed; numbered problems; first crack waved away | 200 m stamp; no squeeze (ears and sinuses flood); pass 253 m; blue whale; problem 1 salt -> fix 2; problem 2 light (no fix, a loop); white fingertips "just the light" |
| L5 1,000 m stop + problem 3 | {{T:m1}}-{{T:m3}} | _lu85gSD39k @1:58-2:21 (stop template: card, sense first, expectation broken, one number) | stamp -> sensory arrival -> one number -> button | light gone; 3 in 4 glow (pays the light loop); problem 3 anglerfish; remora readout HIDING |
| L5 Rug pull (T4) | {{T:m5}}-{{T:m12}} | y300HjYnHPw @4:24-4:31 (none of that was the real problem; callback to the plant) | rug pull at ~35%; the planted unchanged variable is the killer; numbers for the danger | the BODY readout falling since {{T:c3}} flies to centre; ×30 at the surface, ×100 at 4 °C; "You passed it a while ago" ({{T:m5}}, {{P:m5}}%) |
| L6 Real analogue -> fix | {{T:f1}}-{{T:f5}} | y300HjYnHPw @5:41-6:03 (one real animal, "this part is real", principle reused) | real analogue flagged as real; principle reused; a cost attached | bluefin tuna exchanger = your gill trick run backwards -> fix 3; cost: you can never stop swimming (plants hunger) |
| L7 2,000 m threat + midpoint re-hook + stranding plant | {{T:n1}}-{{T:n9}} | _lu85gSD39k @4:16-4:36 (something is wrong -> named fact -> size comparison -> button); PLAYBOOK L7 (re-hook at 45-60%); _lu85gSD39k @3:52 (plant: keep this in mind) | threat by sound; size comparison; "the problem nobody warned you about"; plant for the end | sperm-whale clicks speed into a buzz aimed at you, then it turns away; giant squid; at {{T:n8}} ({{P:n8}}%) every fix makes you worse at everything else; deep fish don't survive the trip up |
| L8 4,000 m pressure + tracker advance | {{T:a1}}-{{T:a8}} | 6oZ9fdM0n50 @2:51-3:10 (history already ran the experiment, short dated case); _lu85gSD39k @3:52-3:57 and @6:59-7:02 (tracker number planted, then advanced) | dated human precedent; mechanism; tracker advance | 1992 chamber at 701 m -> fix 4 TMAO -> 2014 prediction: 8,200 m is "the wall on your route" (second touch of the red tick) |
| L9 Low point -> option board -> turn | {{T:w1}}-{{T:w10}} | 6oZ9fdM0n50 @4:05-4:24 (emotional floor as a question, then a "but here's the thing" turn); PLAYBOOK §4 (personal thread revisited) | floor at ~70%; options with strikes (a board, not a trip); "but" turn | DAY 4 stamp; starving; remora quiet; options board (open ocean ✗, abyss ✗, vent 1977, reef ✓ -> ✗ "can't go back up"); the floor ends ahead |
| L10 The wall + decision | {{T:x1}}-{{T:x10}} | _lu85gSD39k @11:24 (tracker final value), @11:43 (sidekick gag turns tender); y300HjYnHPw @7:05-7:11 (climax decision that uses a planted rule and number); PLAYBOOK T12 | planted number pays; companion leaves; honest speculation flag; a choice that spends the planted cost | snailfish; its 2022 cousin at 8,336 m; NO FIX LEFT; the remora drifts up; "this is our guess"; stay, or pay 2,700 m with the way back |
| L10b Final descent + payoff | {{T:x10}}-{{T:x18}} | _lu85gSD39k @10:30-10:41 (last stop, slowed), @11:09 (list of absences mirrors the first stop); PLAYBOOK T10 (bathos) | pace drop; mirrored sensory list; biggest number; human trace last | 2 s ramp; "No light. No sound." mirrors {{T:c3}}; a car on each thumbnail; hunger pays (food, and you're what sank); 2019 fibres: "your world got to it first" |
| L11 Bookend + verdict + recap + thesis | {{T:b1}}-{{T:b4}} | _lu85gSD39k @11:46-11:50 (stranding: the hook rule bites), @11:57 (recap of every stop), @12:42 (quotable moral); 6oZ9fdM0n50 @5:48-5:51 (restate the title question, short honest answer) | stranding; verdict; recap; one-line thesis | ferry still crossing, remora up there; "Yes. That part's easy."; four borrowed fixes + the way home; "Getting in was never the hard part. Getting out is." |
| L12 CTA + series loop | {{T:e1}}-{{T:e2}} | 6oZ9fdM0n50 @6:22 (CTA asked from the opening scene); _lu85gSD39k @12:56 (pick a stop from options already shown); PLAYBOOK §8 (one loop left open) | callback CTA; no-wrong-answer choice; series harvest | "back at that ferry rail: would you jump?" reef / vent / the line; "swim back up" as the next episode |

Not borrowed on purpose: a second spoken voice (one Kokoro narrator; the remora is mute and reads out through its HUD chip and body language); the 10X-FASTER universe/team act (replaced by a one-line series loop).

Pacing check against PLAYBOOK §9 / §12 (long-form):
- Cold open {{M:hook_words}} words / {{M:hook_end}} s (target ≤120 / ≤50, ~90 / ~35). First sentence {{M:first_sentence_words}} words, second person, impossible change inside it; "fine" at {{M:fine_at}} s. Running trackers in the hook: BODY readout from {{T:c3}}, DepthMeter from {{T:c9}}. No channel intro. Title card {{TITLE_T}}-{{TITLE_END}} with the VO asking the title over it.
- {{M:wpm_overall}} wpm over the runtime (power-story band 175-185; see the TTS note), mean sentence {{M:mean_sentence}} words, {{M:punch_pct}}% punch lines, {{M:second_person_pct}}% second-person sentences (≥45%), {{M:you_per_100}} you-words per 100, {{M:you_first_30s}} you-words in the first 30 s.
- Pivots: {{M:pivots}} = {{M:pivots_per_min}}/min (≥1.5; IFOLOGY winners 2.0): {{PIVOT_LIST}}.
- Numbers: {{M:numbers}} tokens = {{M:numbers_per_min}}/min (≥4; corpus max 8.2). Every stat has an on-screen chip.
- Stamps: {{STAMPS}} (gaps {{STAMP_GAPS}}; PLAYBOOK 60-75 s, range 46-87). Ours run {{STAMP_MIN}}-{{STAMP_MAX}} s, tighter than the norm, because there are seven stops in {{RUNTIME_MMSS}}. Every stamp is also a tracker jump, and between stamps the BODY readout and the meter keep moving.
- Verbal re-hooks (pivot, question, plant, tease, deadpan button): {{REHOOK_N}}, median gap {{REHOOK_MED}} s, longest {{REHOOK_MAX}} s (≤35).
- First turn ("Easy. Except") {{T:g11}} ({{P:g11}}%, target ~25%); rug pull {{T:m5}} ({{P:m5}}%); midpoint re-hook {{T:n8}} ({{P:n8}}%, target 45-60%); low point {{T:w2}}-{{T:w4}} ({{P:w2}}%); wall {{T:x4}} ({{P:x4}}%); floor {{T:x11}} ({{P:x11}}%); ending stack (bookend -> end) {{T:b1}}-{{RUNTIME_MMSS}} = {{ENDING_SHARE}}% of runtime (≤12%).
- Long plants paid: BODY readout ({{T:c3}} -> {{T:m6}}), one-way rule ({{T:c6}} -> {{T:n9}} -> {{T:x9}} -> {{T:b3}}), the wall ({{T:c8}} -> {{T:a8}} -> {{T:x4}}), "until there isn't one" ({{T:r3}} -> {{T:x4}}), never stop swimming ({{T:f5}} -> {{T:w2}} -> {{T:x14}}), remora ({{T:c4}} -> {{T:x5}} -> {{T:b1}}), ferry ({{T:c1}} -> {{T:b1}} -> {{T:e1}}).

## The script

Layers: **HUD** = `whatif/Hud`, top-left stack (DepthMeter ruler on the left edge with a big depth readout, PRESSURE ×N under it, BODY °C readout with a 35° line, BORROWED n · NAME counter, DAYS chip from the abyss, REMORA reaction chip, WAY BACK line once planted). **STAMP** = centred `Headline`, number in red + grey sub line, held ~2 s. **CHIP / STAT / TAG** = kit `Stat` / `Tag` that pop with each spoken number. **CAPTIONS** = core word-level captions at 88% height, content words in red. **VO** = one narrator, calm and slightly dry.

### Hook

- **First line (VO + captions, 0:00):** "You fall off a ferry in the Pacific and gasp in seawater."
- **First visual (0:00):** dusk split-waterline frame: top 35% violet-orange sky with the dark ferry hull sliding right to left, deck rail lit; bottom 65% teal water where YOU (`pose: panic`) has just punched through in a burst of bubbles. The HUD is there from frame 1: DEPTH 0 M, BODY 37.0 °C. At {{M:fine_at}} s ("And you're fine") the bubbles stop and the figure floats upright; from {{T:c3}} the BODY readout starts ticking down and nobody mentions it until the rules.

### Voiceover / captions with timestamps

Timings come from `gen_storyboard.py`: TTS word count (digits expanded) at each section's rate + 0.16 s per sentence break + 0.24 s between lines. Retime from the real Kokoro word timings at build (the storyboard captions are estimates until then). On-screen items appear on their first keyword.
{{VO}}

### HUD state per scene (generator rule)

The core has no persistent overlay, so the generator emits one `whatif/Hud` layer into every scene except the title, verdict, recap and end cards. Its props are the state at the scene start, linear `depth` and `bodyTemp` tracks to the scene end, and a `changes` list (scene-local seconds) for the step values. `focus` modes (`route`, `meter`, `temp`, `borrowed`) enlarge one element to centre for that scene; `pressure: "auto"` = ×(1 + depth/10).

{{HUD}}

### On-screen text (summary)

- HUD from frame 1 (see the table): DepthMeter 0 -> 253 -> 1,000 -> 2,000 -> 4,000 -> 8,200 -> 10,935 M with route marks lit at {{T:c8}} (8,200 red: THE WALL) plus 253 / 701 / 8,336 marks when spoken; PRESSURE ×1 -> ×1,000+; BODY 37.0 -> 34.9 at 253 m -> 33.7 -> 36.2 °C (35° line); BORROWED 1 GILLS -> 2 SALT PUMPS -> 3 HEAT EXCHANGER -> 4 TMAO -> NO FIX LEFT; DAYS 1 -> 4 -> 5 -> 6; REMORA ATTACHED / RELIEVED / UNBOTHERED / HIDING / RELOCATING / QUIET / LEAVING / GONE / UP THERE SOMEWHERE; WAY BACK ? -> SHRINKING -> GONE.
- Stamps (centred, ~2 s): 200 M · THE LAST LIGHT / 1,000 M · MIDNIGHT / 2,000 M · THE HUNTING GROUND / 4,000 M · THE ABYSS / DAY 4 · THE ABYSS PLAIN / 8,200 M · THE LINE / 10,935 M · CHALLENGER DEEP.
- Title card {{TITLE_T}}-{{TITLE_END}}: WHAT IF YOU COULD BREATHE UNDERWATER? ("UNDERWATER?" red), VO over it.
- Problem tags: PROBLEM 1: SALT · PROBLEM 2: LIGHT · PROBLEM 3: THE NEIGHBOURS. Flags: REAL ANIMAL: BLUEFIN TUNA · BEYOND KNOWN BIOLOGY.
- Date chips: 1966, 1992, 2014, 1977, 2022, 2019.
- End card: WOULD YOU JUMP? · REEF · VENT · THE LINE · NEXT: SWIM BACK UP?

### Open loops

| opens | loop | closes |
|---|---|---|
| {{T:c2}} | "and you're fine": how? | {{T:g8}}-{{T:g10}} gills |
| {{T:c3}} | the BODY readout ticks down, unexplained | named at {{T:r5}}, paid by the rug pull {{T:m6}}-{{T:m11}}, fixed {{T:f4}} |
| {{T:c4}} | the remora (a mute companion) | a readout at every stop; leaves at the wall {{T:x5}}; "up there somewhere" {{T:b1}} |
| {{T:c6}} | you can't climb back on (one-way rule) | {{T:n9}} plant -> {{T:w9}} -> spent {{T:x7}}-{{T:x9}} -> stranding {{T:b1}}-{{T:b4}} |
| {{T:c7}}-{{T:c8}} | master: the deepest floor, and one line on the way is a wall | wall named {{T:a8}}, hit {{T:x4}}, floor {{T:x11}} ({{P:x11}}%) |
| {{T:r3}} | "until there isn't one" | {{T:x4}} NO FIX LEFT |
| {{T:g11}} | "one more thing... you won't feel it yet" | {{T:m6}} |
| {{T:h9}} | no fix for light | {{T:m2}} everything here makes its own light |
| {{T:h11}} | white fingertips, waved away | {{T:m11}} hypothermia, passed at ~200 m |
| {{T:f5}} | you can never stop swimming (it burns food) | {{T:w2}} starving -> {{T:x14}}-{{T:x18}} food |
| {{T:n1}} | the click: who, and is it for you? | {{T:n3}}-{{T:n6}} |
| {{T:w5}} | where could you actually live? | {{T:w8}} reef, struck {{T:w9}}; reopened as the CTA {{T:e1}} (left to the comments) |
| {{T:e2}} | what happens if you swim back up | left open for the next episode |

## Shot list

Kit vocabulary: core layers (`rect`, `circle`, `text`, `svg`, `particles` presets bubbles/dust/snow/embers/rain/stars, `component`), core camera (`pushIn`, `pullOut`, `panUp`, `panDown`, `panLeft`, `panRight`, `drift`, keyframes, `shake`), transitions (`cut`, `fade`, `dipBlack`, `whip`, `glitch`), static per-scene `grade`, core word-level `captions`, explainer kit (`explainer/Ocean` with a `depth` track, `surface`, `rays`, `snow`; `DepthMeter`; figures `BlueWhale` `SpermWhale` `ColossalSquid` (drawn with `hooks: false` as the giant-squid stand-in) `Anglerfish` `Diver` `You` `Bus` `Car` `Krill` (amphipod stand-in); `ScaleBar`, `Stat`, `SpeedBars`, `Options`, `Timer`, `Map`, `Headline`, `Tag`), SFX from `studio/public/sfx`, music from `studio/public/music`. Every creature in a shot shares one `pxPerM`.

**New-asset budget (was ~28 items):**
- NEW components (4), in `studio/src/kits/whatif/` (create `index.tsx` and add `import './whatif';` to `studio/src/kits/index.ts`; re-read that shared file first): `whatif/Hud` (wraps DepthMeter + readouts + chips; props in the HUD table), `whatif/Ferry` (hull + lit deck rail silhouette, `lights`), `whatif/GillDiagram` (head profile with slit strokes on a circle head; `mode: oxygen | salt | heat | strip`, `flip`, `slitsAt`, `flowAt`), `whatif/Fish` (one parametrised figure: `species: remora | tuna | snailfish | deepfish`, `cutaway` (vessel tangle in the swimming muscle), `translucent`, `pxPerM`).
- Kit edit (1): `explainer/DepthMeter` `marks: [{d, label, color, at}]` (~20 lines in `kits/explainer/ocean.tsx`). The ruler is linear, so shallow marks (200, 253) are shown with `focus: meter` + `window: 400` zooms, not a log scale.
- Everything else is core layers or inline SVG strings defined in `gen_storyboard.py` (seafloor, trench walls, protein ribbon, TMAO dots and chart, vent and reef tiles, jar + mouse, lung pipe, speech bubble, radiator, coil, cells, fibre magnifier, water arrows). Snow thinning = two crossfaded `particles` layers; light fading = the Ocean `depth` track; tints inside a shot = full-frame `rect` with opacity keyframes; click rings = `circle` layers with scale keyframes.

{{SHOTCOUNT}} shots, contiguous 0:00 -> {{RUNTIME_MMSS}}, longest {{LONGEST_SHOT}} (all ≤15 s).

{{SHOTS}}

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
- **Deep fish brought up.** Many deep-sea fish die or are badly damaged when hauled to the surface (decompression and gas expansion in swim-bladder fish, temperature shock, pressure-adapted proteins and membranes). "Many deep fish ... don't survive the trip" is the honest wording. Extending this to you is flagged as speculation at {{T:x6}}.
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
- **10-second gate shot:** {{S:s33-rugpull}}-{{S:s35-heat}} (rug pull: HUD `focus: temp` fly-in, grade, then GillDiagram `mode: heat` with the ×30 / ×100 stats). It exercises the Hud, the grade, `Stat` and the GillDiagram at once.
- **Visual monotony below 1,000 m:** the auto Ocean is near-black below ~1,000 m, so the abyss and trench scenes lean on the mud and trench-wall SVGs, the warm vent/reef tiles and the pale snailfish for contrast; set `bottomColor` per zone (abyss mud-brown, trench blue-black) when the Hud lane wires backgrounds.
- **Audio:** every SFX cue named exists in `studio/public/sfx`. No pitch control, so the loud whale click is `click` at full volume plus `boom` on the buzz hit. The "single low note" is `drone` as an SFX. Music beds: tension_pulse, deep_ocean, dread, documentary_pulse.
- **Captions** sit at 88% height; stamps at 45%; HUD stays in the top-left 420 × 960 box, so the map and stat insets live in the right two-thirds.
- **Description:** fact-sheet sources; "AI-generated narration (synthetic voice); animation is code-drawn"; the remora and the last 2,700 m are fiction (flagged on screen at {{T:x6}}).

## Originality gate

`python3 scripts/originality_check.py backlog/whatif/whatif-breathe-underwater/script.md research/corpus research/library/transcripts` -> PASS (2026-11-01, run on this final text; result in review.json).
