---
episode: whatif-everyone-born-same-day
niche: whatif
status: BLOCKED-ON-KIT          # studio/src/kits/whatif does not exist yet; build only after the gate shot below passes review (PLAN.md 10-second rule)
gate_shot: "{{S:s10-pyramid-collapse}}-{{S:s12-keep-date}}: shots 10-11, the real 2024 pyramid draining into one amber bar, then the grey 'old world on loan' bands (needs whatif/Pyramid + whatif/IconRows + whatif/Pill only)"
format: long-form 16:9 (1920x1080), single narrator VO + burned-in word captions
engine: "Timeline (PLAYBOOK §1B) with a thought-experiment number spine: one cohort walks up a YEAR ladder while a population pyramid tracks it"
working_title: "What If Everyone On Earth Was Born On The Same Day?"
title_keyword: "the same day"
generated_by: gen_storyboard.py   # VO, timestamps, metrics, shot list and storyboard.json all come from that one file; edit there, not here
target_runtime_s: {{RUNTIME}}          # {{RUNTIME_MMSS}} = narration 0:00-{{NARR_END}} + 0.6 s + 10 s end screen (PLAYBOOK long-form 7-13 min)
target_words: {{WORDS}}               # measured on the VO below (gen_storyboard.py)
target_words_per_min:
  spoken: {{WPM_SPOKEN}}              # TTS speech time only; per-section Kokoro rate 148-166 (hook 158, data chapters 164-166, low point 148, payoff 148, ending 152-156)
  overall_narrated_span: {{WPM}}      # {{WORDS}} words / 0:00-{{NARR_END}}, including the 5 s silent title card and every pause (PLAYBOOK long-form median 154; RESTART 143, EVERY-HUMAN 147)
pacing_measured:                 # all computed by gen_storyboard.py from the VO lines; sentences split on . ? !
  hook: "{{HOOK_WORDS}} words / 0:00-{{HOOK_END}}; premise stated by 0:08 (line 2); trailer of 3 dated promises (DAY 1, 6, 65) + a withheld master question inside the hook"
  sentences: {{SENTS}}
  sentence_mean_words: {{SENT_MEAN}}       # PLAYBOOK median 9.0
  punch_lines_pct: {{PUNCH}}              # sentences of 1-3 words; PLAYBOOK 14.7% (8-23%)
  second_person_pct: {{SECOND}}            # sentences containing you/your/you're/yours; PLAYBOOK median 33%, checklist >=25%
  you_words_first_30s: {{YOU30}}
  pivots_per_min: {{PIVOTS}}             # but / except / until / here's / problem / catch / though / instead; target >=1.5
  questions: {{QUESTIONS}}
  numbers_per_min: {{NUMS}}             # digit tokens + number words in the VO (target >=4); HUD/pills add more
  chapter_stamps: "{{CHAPTERS}} (median gap {{CH_MED}} s, max {{CH_MAX}} s)"
  master_loop: "opens {{T:h9}} ('a birthday none of the other eight billion ever had') -> closes {{T:p2}}-{{T:p3}} ({{P:p2}}% of runtime)"
  second_stage_reveal: "{{T:p5}}-{{T:p7}} ({{P:p5}}-{{P:p7}}%): the family at the table, all different birthdays, and the 0:00 birth counter back to four a second"
  plants: "dated rule 'thirtieth birthday' {{T:r4}} -> paid {{T:m2}} ({{P:m2}}%); trailer '65' {{T:h8}} -> {{T:r65a}}; master loop {{T:h9}} -> {{T:p2}}; birth counter 0:00 -> {{T:p7}}; ninety-kid class {{T:y6c}} -> {{T:r80d}} and {{T:b2}}; hand-holding {{T:y1b}} -> {{T:b5}}; Japan's two bumps {{T:e4}} -> {{T:rv3}}"
  ending_stack: "bookend + recap + thesis + CTA {{T:b1}}-{{NARR_END}} (~11%), then 10 s end screen"
voice: "Kokoro-82M on Spark CPU (CUDA_VISIBLE_DEVICES='', torch threads 4), one warm narrator, no character voices; numbers are written out in the VO exactly as they must be spoken"
music: "studio/public/music/documentary_pulse.m4a only, with planned silence drops (YEAR 30 interrupt, YEAR 125 stamp) and a 0.12 bed under the YEAR 80 low point. Optional later task: synthesise a 30 s music-box/marimba loop with sox on the Spark CPU; not required for render."
references:
  - id: "6oZ9fdM0n50"
    short: RESTART
    url: https://www.youtube.com/watch?v=6oZ9fdM0n50
    views: 4221146
    outlier_score: 14.44
    why_chosen: "Closest premise and format: a flat-2D Awaken demography thought experiment (8 billion target, generations, maths ladder) at 6:58. Borrowed devices: the H7 self-correction that leaves the scarce resource (@0:15), the 7 s silent title card (@0:31), a target number then a sceptic-friendly concession (@1:09), the one-word false resolution then 'except' at a specific step (@1:30), 'history already ran this' dated proof in short sentences (@2:51-3:10), the porch low point with an either/or question (@4:05), the 'but' turn into a hope ladder of dated real cases rising in closeness to the viewer, ending on a 'you're proof' rung (@4:20-5:36), and a personal choice CTA that bookends the opening image (@6:22)."
  - id: "b6jmbFcJZCY"
    short: EVERY-HUMAN
    url: https://www.youtube.com/watch?v=b6jmbFcJZCY
    views: 1076474
    outlier_score: 107.01
    why_chosen: "Highest outlier in the corpus and the timeline-engine template: present-tense true number in line one (@0:00), narrator-performed time-zero (@0:07), rules that remove objections (@0:16), mundane sensory traces (@0:20), a trailer of dated consequences paid shortest-first (@0:30-0:36, first paid @1:14), an undated master mystery held to ~87% (@0:38 -> @10:34), a persistent time HUD + bottom milestone scrubber (@0:49), the consequence chain of hidden human labour (@1:29-1:48), 'this is the countdown from the start' callback when a dated promise comes due (@3:22), one-line ironic chapter buttons (@1:25, @4:10, @5:54), a two-stage final reveal ending on the most human detail (@10:08-10:34), and a bookend recap + anaphora thesis with callbacks (@10:40-11:22)."
  - id: "J3XahLkDEzU"
    short: LAST-HUMAN
    url: https://www.youtube.com/watch?v=J3XahLkDEzU
    views: 914047
    outlier_score: 6.11
    why_chosen: "Our back half is an ageing diary of one cohort ending in a sole survivor. Borrowed: sensory traces in the cold open (@0:04), the fantasy-phase perks before the first threat (@0:30-1:00), YEAR-N chapter signs inside the scene (@2:02, @9:27), a personal thread revisited at act breaks (the dog: plant @0:14, paid @4:14, aged @8:31, gone @9:33; ours is the ringed YOU figure), the old-age chapter stated plainly (@9:27-10:11), the honest speculation flag right before the payoff (@10:22-10:24), a precise final number (@10:30), and ending on a small human detail rather than the biggest number."
secondary_references:          # device-only borrowings, cited where used in the table
  - id: "y300HjYnHPw"
    short: 10X-FASTER
    url: https://www.youtube.com/watch?v=y300HjYnHPw
    views: 867909
    outlier_score: 8.38
    used_for: "the explicit 'remember this' plant of one rule (@0:20-0:27) and the midpoint rug pull that recasts the earlier problems as a warm-up, then calls back the plant (@4:24-4:31). Device only; our pivot line is our own wording."
fact_file: "Fact sheet at the bottom. Every on-screen number is real and sourced, or marked EST. (our arithmetic from the stated real inputs, model in the fact sheet)."
post_caption_cta: "Would you rather be one of the eight billion who share one birthday, or one of their kids, born into a world where every grown-up is the same age?"
---

# What If Everyone On Earth Was Born On The Same Day?

**One rule changes:** every person alive is born on the same morning, year included: 8,000,000,000 babies. To keep them alive, 2,000,000,000 adults from the old world are **on loan** (grey on every chart, one per four babies). They raise the cohort, and **on its thirtieth birthday they hand everything over and step out of the story**. That exit is a stated rule with a date, planted at {{T:r4}} and paid at {{T:m2}}; nobody claims they all die of old age at 50-75. Everything else is real demography (current UN life tables and fertility) applied to one bar instead of a pyramid.

**Spine (tracker on screen from 0:08 to {{T:p7}}):** top-left `whatif/Hud`. Until {{T:r6}} it reads `YEAR 0 · EVERYONE IS 0` with `BABIES 8,000,000,000` / `ADULTS 2,000,000,000`. From {{T:r6}} it has two counters, `TOTAL ALIVE` (cohort + echoes + borrowed adults) and `YOUR AGE GROUP` (cohort only), plus a personal line `YOUR ODDS OF BEING THE LAST: 1 IN N` that updates at each act break (8 BN at {{T:h9}}, 7.5 BN at YEAR 30, 6.3 BN at 65, 3.8 BN at 80, 40 M at 100, 40,000 at 110, 40 at 120, then 1). A bottom `whatif/Scrubber` runs DAY 1 -> 125 with one icon per milestone, used identically everywhere: bottle `DAY 1`, desk `6`, key `30`, rocking chair `65`, candle `?`/`125`. The recurring board is `whatif/Pyramid`: the real 2024 world pyramid collapses into one amber bar at age 0, then the bar climbs one band per chapter, grey bands sit above it until the handover, teal echo bands grow under it from YEAR 20, and the shape slowly rebuilds into a pyramid.

**Personal thread:** "you" is one amber `whatif/Person` with a cream ring, seen in the crib field (0:00), the YOU crib ({{T:h3}}), the night-feed close-up ({{T:d4}}), the 90-kid class ({{T:y6c}}), graduation and the job queue ({{T:y18b}}), the bench ({{T:y18g}}), the recipe card ({{T:m8}}), the retirement walk-out ({{T:r65b}}), the porch ({{T:r80a}}) and the last kitchen ({{T:p2}}, ring shown with a `?`).

**Three visual modes (PLAYBOOK §12):** STORY = six flat 2D sets with stick-figure people (amber = the cohort, grey = old world, teal = echo); BOARD = navy chart board with the pyramid, stat pills and source lines; STAMP = full-width `whatif/YearStamp` chapter card (Anton year + small-caps subtitle, held >= 1.8 s) that flips in over the last frame.

**Frame zones (16:9):** HUD top-left (x 96, y 60-230); corner stamps top-right; `whatif/Pill` top-centre at y ~150 with its source line top-right; core word captions at y 0.82 (78-86%); `whatif/Scrubber` at y 94-98%. Nothing else is placed in the bottom 15%.

## Beat alignment table

| Our beat | Our time | Reference id + timestamp | Device borrowed | How we adapt it |
|---|---|---|---|---|
| L1a right-now fact + running tracker | 0:00-{{T:h2}} | b6jmbFcJZCY @0:00-0:01; PLAYBOOK §2 combination rule (tracker moving in the hook, top-4 outliers) | Present-tense true number before any fiction (H9) | Real births (~4 a second) on a live counter over an already-impossible frame: an endless field of cribs to the horizon, filling 4 per second |
| L1b impossible change in sentence two | {{T:h2}}-{{T:h3}} | b6jmbFcJZCY @0:07-0:13; 6oZ9fdM0n50 @0:10 | Narrator sets time-zero; premise at maximum scale ("every person") | "you, and everyone alive, born on the same morning"; 60 rows of a year's dots slam into one block |
| L1c sensory traces | {{T:h3}}-{{T:h5}} | b6jmbFcJZCY @0:20 (still-hot coffee, rolling cars); J3XahLkDEzU @0:04 (steaming coffees, a card machine beeping) | 2-3 mundane sensory details that make the impossible feel present | Eight billion cries at once; the planet smelling of warm milk |
| L1d self-correction exception | {{T:h5}} | 6oZ9fdM0n50 @0:15 (H7) | One-line "not quite everyone" that leaves the scarce resource | The 2 billion borrowed adults, stated once as the concession; HUD `BABIES 8 BN · ADULTS 2 BN` |
| L1e trailer of dated promises | {{T:h6}}-{{T:h9}} | b6jmbFcJZCY @0:30-0:36 (H10), first paid @1:14 | 3 time-stamped consequences, each an on-screen tick, paid shortest-first | DAY 1 (four babies each) paid {{T:d4}}; age 6 (ninety kids) paid {{T:y6c}}; 65 (one Monday) paid {{T:r65a}} |
| L1f master question | {{T:h9}} | b6jmbFcJZCY @0:38 (withheld answer) -> @10:34 | Undated mystery whose answer is held back, not stated | "a birthday none of the other eight billion ever had"; the answer (the 125th, with nobody else turning that age) is held to {{T:p2}} |
| L2a silent title card | {{TITLE_T}}-{{TITLE_END}} | 6oZ9fdM0n50 @0:31-0:38 | 5-8 s music-only card restating the question | 5 s title over the single amber bar, keyword "the same day" in amber |
| L2b rules + dated plant | {{T:r1}}-{{T:r5}} | b6jmbFcJZCY @0:16 (rules remove objections); y300HjYnHPw @0:20-0:27 (one stated rule + explicit "remember" plant); b6jmbFcJZCY @0:36 (on-screen countdown to a dated event) | Objection-killing rules, one fair concession, one dated rule the viewer is told to hold | No clones / no time machine; adults on loan at 1:4; "on your thirtieth birthday, they hand everything over"; new scrubber tick `30` + `HANDOVER IN 30 YEARS` chip |
| L2c start the clock | {{T:r6}} | b6jmbFcJZCY @0:49 | One short line that starts the tracker | "Happy birthday, everyone." HUD switches to TOTAL ALIVE / YOUR AGE GROUP |
| L3 DAY 1: grounding + promise 1 + consequence chain | {{T:d1}}-{{T:y1a}} | 6oZ9fdM0n50 @0:38-1:09 (target number -> real baseline -> "let's be generous" concession); b6jmbFcJZCY @1:14 (first promise paid) and @1:29-1:48 (who runs the plants that need people -> dominoes) | Baseline -> our number -> a one-person rung -> a consequence chain -> a concession -> deadpan button | 360,000/day vs 60 years before lunch; one adult's 40 feeds + 40 diapers; who runs power, farms, hospitals with 2 BN adults on night feeds; "we'll be kind" rule removes starvation; "nobody sleeps for a year" |
| L4 honeymoon + gag | {{T:y1a}}-{{T:y6a}} | J3XahLkDEzU @0:30-0:56 (fantasy-phase perks with comic exaggeration); 6oZ9fdM0n50 @1:30 (false resolution -> "except") | 3-4 perks rising in warmth, a deadpan logistics gag, then a crack line | Species walks in weeks; one bakery order for 8 BN cakes; nobody too old for the swings; "fairest world... until you turn six" |
| L5a YEAR 6 (promise 2 paid) | {{T:y6a}}-{{T:y6d}} | b6jmbFcJZCY @2:17-2:34 (chapter stamp -> named problem -> number pays the trailer item) | Stamp -> "here's the problem" -> one ratio | Fewer than 100 M teachers -> ~90 per class vs today's ~23 |
| L5b dated precedent + button | {{T:y6d}}-{{T:y18a}} | 6oZ9fdM0n50 @2:51-3:10 (history already ran it; short sentences ending on finality); b6jmbFcJZCY @4:10 (one-line ironic button) | "Impossible?" -> a real country ran a small version -> 3-gate cascade -> scale back to us -> button | Romania 1966-67 births nearly doubled; maternity -> school -> university; ×2 vs ×22,000; "year-group photo taken from orbit" |
| L6a YEAR 18 (one merged capacity beat) | {{T:y18a}}-{{T:e1}} | b6jmbFcJZCY @2:40-2:42 (one named place generalised to every place); 6oZ9fdM0n50 @1:40 (relatable comic line) | One combined number -> a dated real crisis -> "for you, the whole planet" -> comedy button | University places 1 per 32 + 3.5 BN jobs in one sentence; Spain 2013; "dating is easy"; strollers set up the echo |
| L6b echo chapter (before YEAR 30) | {{T:e1}}-{{T:m1}} | 6oZ9fdM0n50 @1:12-1:24 (simple multiplier rule -> derived number); J3XahLkDEzU @0:14 -> @4:14 (a detail planted to be paid later) | Simple rule -> big derived number -> named concept -> real dated example, planted for later | TFR ~2.2 -> ~8 BN babies mostly inside 20 years (YEAR 20-45); "echo"; Japan's 1947-49 and 1971-74 bumps, paid at {{T:rv3}} |
| L7 midpoint rug pull (dated plant paid) | {{T:m1}}-{{T:r65a}} ({{P:m1}}%) | y300HjYnHPw @4:24-4:31 (rug pull recasts earlier problems + calls back the planted rule); b6jmbFcJZCY @3:22 ("this is the countdown from the start"); b6jmbFcJZCY @1:34-1:36 (anaphora of hidden human roles) | Own-words pivot -> explicit "date from the rules" callback -> the surprise consequence -> role anaphora | "But exams and jobs turn out to be the easy part." The adults step out on the date; the job shortage flips into every senior job being yours; surgeon still in training; judge, pilot, power-station engineer: thirty; no child has a grandparent |
| L8a YEAR 65 (promise 3 paid) | {{T:r65a}}-{{T:r80a}} | b6jmbFcJZCY @3:22-3:48 (promise callback -> mechanism -> "the problem is" -> number) and @5:54 (ironic button) | Promise callback -> event -> "here's the catch" -> real comparator -> our ratio -> button | ~6.3 BN retire on one Monday; the echo carries it; Japan 1:2 vs ours 3:4; "every golf course booked solid" |
| L8b emotional floor | {{T:r80a}}-{{T:rv1}} | 6oZ9fdM0n50 @4:05 (porch low point + either/or question); J3XahLkDEzU @9:27-9:33 (old-age chapter, loss stated plainly) | Quiet time-skip, plain statement of loss, fragment ladder, either/or question | YEAR 80: half gone, ~4x today's funerals, half of the ninety-kid class; "worth it, or losing everyone together?" |
| L8c reversal with evidence | {{T:rv1}}-{{T:c1}} | 6oZ9fdM0n50 @4:20-5:36 ("but" turn -> dated real cases rising in closeness -> "you're proof" rung); b6jmbFcJZCY @4:14-4:37 (counter-intuitive relief backed by a precedent) | Mechanism -> dated real cases -> a checkable number -> a "you" rung | Japan's peaks: 2.7 M (1949) -> 2.1 M (1973) -> the expected third wave never came; your birthday 8 BN in a day vs the echo's busiest day ~1.5 M (EST.); your family has birthdays in every month |
| L9a centenarians + authority | {{T:c1}}-{{T:c5}} | 6oZ9fdM0n50 @2:12 ("one study estimated"); b6jmbFcJZCY @8:46 (rate-based number) | One cited study turned into a rule the viewer can run | ~40 M at 100 (EST.), >50x today's ~0.72 M; Barbi et al. 2018: ~50% a year past 105 as a coin toss |
| L9b speculation flag | {{T:c5}} | J3XahLkDEzU @10:22-10:24 (T12) | Say aloud where firm data ends, right before the payoff | "less a forecast and more a dice roll"; `ESTIMATE` stamp on the HUD |
| L9c halving ladder | {{T:c6}}-{{T:c9}} | 6oZ9fdM0n50 @1:17-1:24 ("two becomes eight" ladder), run in reverse | Rhythmic number ladder, every step a count with its unit | "forty thousand... twenty thousand at a hundred and eleven. Then ten thousand. Five thousand... a few dozen of you"; HUD shows the age at each step |
| L9d record + master payoff (stage 1) | {{T:c9}}-{{T:p5}} | 6oZ9fdM0n50 @6:01-6:14 (hard number vs you); J3XahLkDEzU @10:30 (exact final count) | Real record -> "one of you beats it" -> exact final stamp -> the withheld answer | Calment 122 y 164 d; YEAR 125, ALIVE 1; "the birthday none of the others ever had": nobody else turning that age |
| L9e second-stage reveal (reversal in the last 20%) | {{T:p5}}-{{T:b1}} ({{P:p5}}-{{P:p7}}%) | b6jmbFcJZCY @10:08-10:34 (a second answer after the first, ending on the most human detail) | A new reveal after the payoff, built from plants | Pull out: family of every age, every one born on a different day (pays the echo + reversal); the 0:00 counter is back to four babies a second (pays line 1) |
| L10 bookend + recap + thesis | {{T:b1}}-{{T:cta1}} | b6jmbFcJZCY @10:40-11:22 (back to time-zero, milestone recap, anaphora thesis with three callbacks); 6oZ9fdM0n50 @6:22 (bookend to the opening image) | Return to the opening image, icon recap, reframe, 3-callback anaphora | Crib field -> recap icons; "the gaps between us"; "someone holding your hand / teaching ninety kids / handing over the keys" (callbacks {{T:y1b}}, {{T:y6c}}, {{T:m3}}); "a relay race" |
| L11 CTA | {{T:cta1}}-{{NARR_END}} | 6oZ9fdM0n50 @6:22 (personal choice that bookends the opening); PLAYBOOK §7 (binary dilemma from options the video showed) | No-wrong-answer binary choice | The cohort or the echo, both shown throughout |
| End screen | {{NARR_END}}-{{RUNTIME_MMSS}} | 6oZ9fdM0n50 @6:31 | End cards over the bookend set | Two end cards over the blurred one-candle kitchen |

## The script

Layers: **VO** = narration (TTS; also drives word-level captions at y 0.82); **HUD** = top-left YEAR badge + counters + odds line; **PILL** = top-centre stat pill with its source line top-right; **STAMP** = chapter card; **TAG** = short small-caps keyword label. Timestamps below are computed from word counts at the stated per-section TTS rate with 0.12 s between lines; after TTS, re-time from Kokoro's word timings.

### Hook

- **First line (VO, 0:00):** "Every second, about four babies are born somewhere on Earth."
- **First visual (0:00):** the already-impossible frame: an endless field of cribs to the horizon at dawn, side-on rows shrinking into the distance. They are empty, and four light up amber every second under a live corner counter `BIRTHS THIS SECOND: 4`. One front crib carries a cream ring marked YOU. At {{T:h3}} every crib fills at once.

### Voiceover, captions and on-screen text with timestamps
{{VO}}

VO: {{WORDS}} words, 0:00-{{NARR_END}} ({{WPM}} wpm over the narrated span, {{WPM_SPOKEN}} wpm spoken). {{SENTS}} sentences, {{SECOND}}% in second person.

### On-screen text summary

- HUD: `YEAR n` badge (DAY 1, 0 -> 125) + subline; hook counters `BABIES 8,000,000,000` / `ADULTS 2,000,000,000`; from {{T:r6}} `TOTAL ALIVE` and `YOUR AGE GROUP` (keyframes below); odds line `YOUR ODDS OF BEING THE LAST: 1 IN N`; survivors mode from YEAR 100 with an `ESTIMATE` stamp.
- STAMPS: DAY 1, YEAR 1, YEAR 6, YEAR 18, YEAR 24, YEAR 30, YEAR 65, YEAR 80, YEAR 100, YEAR 110, YEAR 125.
- TAGS: ONE MORNING, NO CLONES, NO TIME MACHINE, SAME PLANET · SAME CITIES, HANDOVER IN 30 YEARS, KEEP THIS DATE, RULE 2: LIGHTS ON · NOBODY HUNGRY, SLEEP: 0, FIRST STEPS: EVERYONE, OLDEST KID ON THE SWINGS: 1, YEAR-GROUP PHOTO: 7,700,000,000, AGE GAP: 0, THE ECHO, HANDOVER IN 0 YEARS, OLDEST PERSON ALIVE: 30, OPEN TODAY: EVERY SENIOR JOB, GRANDPARENTS: 0, TEE TIMES: SOLD OUT, ECHO OF THE ECHO, NEVER CAME, EACH WAVE: LOWER AND WIDER, ESTIMATE, THE GAPS, IT'S A RELAY.
- PILLS (each with a source line): ~132 M a year; 1 adult : 4 babies; ~60 years of births; 40 feeds + 40 diapers (EST.); ~3.5 BN employed; births nearly doubled (Romania); ~250 M university places · 1 per 32; Spain under-25 unemployment ~56%; ~2.2 children per woman; ~6.3 BN retirees (EST.); Japan 1:2 vs 3:4; ~4x today's yearly deaths (EST.); Japan births 1949 2.7 M / 1973 2.1 M; busiest birth day 8 BN -> ~1.5 M (EST.) -> today ~360,000; ~40 M aged 100 (EST.) vs ~0.72 M today; 105+ ~50% each year; record 122 y 164 d.

**HUD keyframes (whatif/Hud spec; EST. from the fact-sheet model):**

| At | YEAR | TOTAL ALIVE | YOUR AGE GROUP | odds line |
|---|---|---|---|---|
| {{T:h3}}-{{T:r6}} | YEAR 0 | (hook mode) BABIES 8,000,000,000 · ADULTS 2,000,000,000 from {{T:h5}} | — | 1 IN 8,000,000,000 from {{T:h9}} |
| {{T:r6}} | YEAR 0 | 10,000,000,000 | 8,000,000,000 | — |
| {{T:d1}} | DAY 1 | 10,000,000,000 | 8,000,000,000 | — |
| {{T:y1a}} | YEAR 1 | 9,800,000,000 | 7,800,000,000 | — |
| {{T:y6a}} | YEAR 6 | 9,700,000,000 | 7,700,000,000 | — |
| {{T:y18a}} | YEAR 18 | 9,900,000,000 | 7,600,000,000 | — |
| {{T:e1}} | YEAR 24 | 9,900,000,000 -> 11,800,000,000 (counts up over e2) | 7,600,000,000 | — |
| {{T:m1}} | YEAR 30 | 14,700,000,000, then 13,000,000,000 when the grey bands lift | 7,500,000,000 | 1 IN 7,500,000,000 |
| {{T:r65a}} | YEAR 65 | 21,200,000,000 | 6,300,000,000 | 1 IN 6,300,000,000 |
| {{T:r80b}} | YEAR 80 | 22,200,000,000 | 3,800,000,000 | 1 IN 3,800,000,000 |
| {{T:c1}} | YEAR 100 | (survivors mode, hidden) | ~40,000,000 | 1 IN 40,000,000 |
| {{T:c6}} / {{T:c7}} / +2.6 s / +3.6 s / {{T:c8}} | 110 / 111 / 112 / 113 / 120 | — | 40,000 / 20,000 / 10,000 / 5,000 / ~40 | 1 IN 40,000 ... 1 IN 40 |
| {{T:c10}} | YEAR 122 | — | ~7 | 1 IN 7 |
| {{T:p1}} | YEAR 125 | — | 1 | 1 IN 1 |

## Shot list

**Status: BLOCKED-ON-KIT.** `studio/src/kits/` has demo, explainer, horror and thumbs only, and `kits/index.ts` registers no `whatif/*`. Build order: (1) `whatif/Pyramid`, `whatif/IconRows`, `whatif/Pill` -> render the gate shot ({{S:s10-pyramid-collapse}}-{{S:s12-keep-date}}) at 1080p on the Spark (`--concurrency=4`) and get it reviewed; (2) only then `whatif/Hud`, `whatif/Scrubber`, `whatif/YearStamp`, `whatif/Person`, `whatif/Crowd`, `whatif/Set`; (3) the rest.

Kit vocabulary: core layers (`rect`, `circle`, `text`, `svg`, `particles`, `component`), camera presets `pushIn`/`pullOut`/`panLeft`/`panRight`/`panUp`/`panDown`/`drift` or explicit camera keyframes (there is no `zoom` preset), `shake`; transitions `cut`/`fade`/`dipBlack`/`whip`/`glitch`; `grade` (brightness/tint/vignette; no blur: use layer `blur`); core word captions; explainer kit `explainer/Stat`, `explainer/Tag`, `explainer/Headline`, `explainer/SpeedBars`, `explainer/Map` (continent keys northAmerica/southAmerica/eurasia/africa/australia/antarctica for `highlight`; countries are lon/lat pins + rings), `explainer/Options` (text-only list), `explainer/Timer`, `explainer/Bus`; SFX names exactly as in `studio/public/sfx` (no pitch field, so nothing is "pitched"). Fonts: Montserrat + Anton only (already bundled); YearStamp and the title use Anton.

NEW `whatif` kit (all flat SVG, no generated imagery):
- `whatif/Hud` {mode hook|year|survivors, year, sub, babies, adults, total, cohort, odds, estimate, ladder[{t, year, cohort, odds}], changes[{at, state}]}
- `whatif/Scrubber` {max 125, dot (year), ticks[{year, icon, label, lit}], marker{year, label}}: one icon per milestone: bottle DAY 1, desk 6, key 30, rockingChair 65, candle 125
- `whatif/Pyramid` {bands[{age, value (millions), male, kind world2024|cohort|old|echo|echo2, outline, liftAt, growAt}], scale {refValueM 700 = 40% of half-width; overflow clip + chevron + "×12" label}, morphTo/morphAt/morphDur, pin{age, at, glow}, smooth{at, dur}, glowGaps, dim, source}. Band data for 2024 is in storyboard.json (21 bands, UN WPP 2024 approx.; swap in the exact CSV values).
- `whatif/YearStamp` {year, sub, corner}; full-width version held >= 1.8 s
- `whatif/Person` {age baby|kid|teen|adult|elder (scale + head ratio; elder = bent spine + cane), pose stand|walk|sit|hold|point, hat none|cap|scrubcap|wig|hardhat, color, you (cream ring + tiny YOU tag), youQuestion}: 5 ages x 5 poses + 4 hats. No faces.
- `whatif/Crowd` {age, count <= 500 animated, rows, color, pose, youIndex, fill/fillAt, fadeOut/fadeAt, halvings[], pattern: static SVG pattern fade beyond row 4, frozen}
- `whatif/Set` {name ward|classroom|office|park|porch|kitchen, light, view, props}: six sets reused throughout (ward = crib field; classroom = door queue / interior / hall; office = desks / street side; park = walk / swings / bench / aerial / path; porch; kitchen = cake table / recipe card / bakery counter / final scene)
- `whatif/Cake` {candles, lit, front}; `whatif/IconRows` {rows[{label, a, b, at}]}; `whatif/Pill` {text, source, at}
- `whatif/Icon` {name}: 18 icons: crib, bottle, diaper, desk, backpack, mortarboard, chair, key, rockingChair, candle, powerStation, farm, hospital, coin, dice, pin, stroller, flag (plus `elder`/`paper` glyphs reused from Person/rect). Helpers built from Icon: `IconRow`, `IconPile`, `RecapRow`, `MonthGrid`, `DateTags`, `DotStrip`, `GateCascade`, `MiniPyramid`, `LineChart` (simple svg path; series `japanBirths` 1945-2010 from MHLW).

Asset count: 13 components + 1 rig + 6 sets + 18 icons ≈ 38.

Palette: cohort amber `#F2B33D`, old world grey `#9AA3AE`, echo teal `#3FB8AF`, board navy `#13213A`, paper cream `#F4EEDF`, alert red `#E2554B`.

{{SHOTS}}

{{SHOTCOUNT}} contiguous shots, 0:00-{{RUNTIME_MMSS}}. Transitions are centred on cuts and never change length. Every STAMP shot is >= 1.8 s; the next VO line starts under the stamp. Shot 36 holds until 0.8 s after "planet" so the flood lands on the word.

## Fact sheet (sources to cite in the description / fact file)

- **World population** ~8.2 billion (UN World Population Prospects 2024), rounded to 8 billion for the cohort. The borrowed adults are extra: 8 B babies + 2 B adults = 10 B at YEAR 0 (HUD shows both).
- **Births** ~132 million a year (UN WPP 2024) = ~360,000 a day = ~4.2 a second. 8.0 B / 132 M ≈ 61 years of births ("sixty years' worth"). 8 B / 360,000 ≈ 22,000 days of births (`×22,000`).
- **Carers:** 8 B / 4 = 2 B adults, ages 20-45 at YEAR 0. US infant-care guidance (Caring for Our Children, AAP/APHA) is 1:3 under 12 months; many state licensing rules allow 1:4. The VO says "one per four babies" and does not claim the guideline. Their exit on the cohort's 30th birthday is a rule of the thought experiment, not mortality. Under real life tables ~85% of them (~1.7 B, then aged 50-75) would still be alive at YEAR 30, so the HUD drops `TOTAL ALIVE` from 14.7 B to 13.0 B at the handover.
- **Feeds/diapers:** newborns feed ~8-12 times and use ~8-12 diapers a day (AAP HealthyChildren). Four babies x ~10 ≈ 40 feeds + 40 changes per adult per day (EST.).
- **Jobs:** ILO World Employment and Social Outlook: ~3.5-3.6 billion people employed (2024).
- **Teachers:** UNESCO Global Report on Teachers (2024): ~94 million teachers, pre-primary to secondary ("fewer than a hundred million"). 8 B / ~90 M ≈ 89 ("about ninety"). Global primary pupil-teacher ratio ~23 (UNESCO UIS).
- **Romania:** Decree 770 (October 1966) banned abortion and most contraception. Live births 1966 ~273,700 -> 1967 ~527,800 (crude birth rate 14.3 -> 27.4 per 1,000). The "decreței" cohort strained maternity wards, schools and university admission into the late 1980s. **Verify exact counts against INS Romania before render.**
- **University places:** UNESCO UIS ~254-264 million tertiary students (2020s). 8 B / 250 M = 32.
- **Spain 2013:** under-25 unemployment rate ~55-57% in 2013 (Eurostat; 56.4% Feb 2013). That is the share of under-25s **in the labour force** who were unemployed, so the VO says "more than half of young Spaniards looking for work"; the share of all young people unemployed was ~21-22%. **Re-check the monthly Eurostat series before render.**
- **Fertility:** global total fertility rate ~2.25 (UN WPP 2024). Echo model: 4 B women x survival to the childbearing ages x TFR 2.2, age-specific fertility normal(mean 28, sd 6) -> ~8.2 B births, ~90% within ±10 years of YEAR 28 ("about eight billion babies, most of them inside twenty years", EST.). Births start ~YEAR 18, so the YEAR 24 chapter comes before YEAR 30 and the YEAR 30 pyramid already shows echo bands at ages 0-12.
- **Model (EST.), used for every HUD number:** a world period life table (UN WPP-like: l20 0.95, l45 0.91, l65 0.785, l80 0.48), TFR 2.2 constant, the carers removed at YEAR 30. Results: TOTAL ALIVE 9.9 B (yr 18), 11.8 B (24), 14.7 -> 13.0 B (30), 15.9 B (45), 21.2 B (65), 22.2 B (80). Cohort 7.6 B (18), 7.5 B (30), 6.3 B (65), 3.8 B (80). Echo peak 550 M births a year ≈ 1.5 M a day (YEAR ~27); the echo's echo peaks at ~400 M a year ≈ 1.1 M a day (YEAR ~55); today ~360,000 a day.
- **Japan's booms:** first baby boom 1947-1949 ("dankai"), peak 2,696,638 births in 1949; second boom 1971-1974 ("dankai junior"), peak 2,091,983 in 1973 (MHLW vital statistics). A third boom expected around 2000 when the dankai juniors reached their late 20s did not happen (births kept falling, to ~1.19 M in 2000).
- **Japan dependency:** 2023, ~29% aged 65+, ~59% aged 15-64 -> old-age dependency ≈ 49 per 100 ("one retiree for every two working-age adults").
- **Our YEAR 65:** survival to 65 under current world life tables ≈ 78% -> ~6.3 B ("over six billion", EST.). Workers aged 20-64 (mostly the echo) ≈ 8.4 B -> 6.3 / 8.4 ≈ 0.75 ("three for every four", EST.).
- **YEAR 80:** l80 ≈ 0.48 -> ~3.8 B alive ("half of you are gone"). Deaths that year ≈ 8 B x (l80 - l81) ≈ 256 M vs ~62 M deaths a year worldwide today (UN WPP) ≈ 4x (EST.).
- **Centenarians:** ~722,000 alive worldwide in 2024 (UN WPP 2024, via Pew Research). Cohort share reaching 100 assumed ~0.5% (between the current world and US rates) -> ~40 M (EST.); 40 M / 0.72 M ≈ 55 ("more than fifty times").
- **Mortality plateau:** Barbi, Lagona, Marsili, Vaupel and Wachter, "The plateau of human mortality: Demography of longevity pioneers", *Science* 360 (2018): Italians aged 105+ face a roughly constant ~50% annual risk of death.
- **Halving ladder:** about 1 in 1,000 centenarians reaches 110 -> ~40,000 (EST.). Halving yearly: 111 ≈ 20,000, 112 ≈ 10,000, 113 ≈ 5,000 ... 120 ≈ 40, 122.5 ≈ 7, 125 ≈ 1. The VO says the unit at every step.
- **Record:** Jeanne Calment (France), 21 Feb 1875 - 4 Aug 1997, 122 years 164 days, the longest verified human lifespan.
- All "EST." numbers are our arithmetic from the inputs above and are labelled EST. on screen wherever they appear in a pill.
