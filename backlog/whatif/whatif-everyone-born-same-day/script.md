---
episode: whatif-everyone-born-same-day
niche: whatif
status: BLOCKED-ON-KIT          # studio/src/kits/whatif does not exist yet; build only after the gate shot below passes review (PLAN.md 10-second rule)
gate_shot: "0:47-1:01: shots 10-11, the real 2024 pyramid draining into one amber bar, then the grey 'old world on loan' bands (needs whatif/Pyramid + whatif/IconRows + whatif/Pill only)"
format: long-form 16:9 (1920x1080), single narrator VO + burned-in word captions
engine: "Timeline (PLAYBOOK §1B) with a thought-experiment number spine: one cohort walks up a YEAR ladder while a population pyramid tracks it"
working_title: "What If Everyone On Earth Was Born On The Same Day?"
title_keyword: "the same day"
generated_by: gen_storyboard.py   # VO, timestamps, metrics, shot list and storyboard.json all come from that one file; edit there, not here
target_runtime_s: 504.5          # 8:24 = narration 0:00-8:13 + 0.6 s + 10 s end screen (PLAYBOOK long-form 7-13 min)
target_words: 1242               # measured on the VO below (gen_storyboard.py)
target_words_per_min:
  spoken: 158.4              # TTS speech time only; per-section Kokoro rate 148-166 (hook 158, data chapters 164-166, low point 148, payoff 148, ending 152-156)
  overall_narrated_span: 150.9      # 1242 words / 0:00-8:13, including the 5 s silent title card and every pause (PLAYBOOK long-form median 154; RESTART 143, EVERY-HUMAN 147)
pacing_measured:                 # all computed by gen_storyboard.py from the VO lines; sentences split on . ? !
  hook: "98 words / 0:00-0:38; premise stated by 0:08 (line 2); trailer of 3 dated promises (DAY 1, 6, 65) + a withheld master question inside the hook"
  sentences: 147
  sentence_mean_words: 8.4       # PLAYBOOK median 9.0
  punch_lines_pct: 19.0              # sentences of 1-3 words; PLAYBOOK 14.7% (8-23%)
  second_person_pct: 34.0            # sentences containing you/your/you're/yours; PLAYBOOK median 33%, checklist >=25%
  you_words_first_30s: 7
  pivots_per_min: 2.19             # but / except / until / here's / problem / catch / though / instead; target >=1.5
  questions: 10
  numbers_per_min: 19.9             # digit tokens + number words in the VO (target >=4); HUD/pills add more
  chapter_stamps: "DAY 1 1:10, YEAR 1 1:51, YEAR 6 2:14, YEAR 18 2:50, YEAR 24 3:24, YEAR 30 3:53, YEAR 65 4:29, YEAR 80 4:58, YEAR 100 5:58, YEAR 110 6:21, YEAR 125 6:47 (median gap 34 s, max 60 s)"
  master_loop: "opens 0:32 ('a birthday none of the other eight billion ever had') -> closes 6:51-6:55 (82% of runtime)"
  second_stage_reveal: "7:04-7:14 (84-86%): the family at the table, all different birthdays, and the 0:00 birth counter back to four a second"
  plants: "dated rule 'thirtieth birthday' 0:59 -> paid 3:53 (46%); trailer '65' 0:27 -> 4:29; master loop 0:32 -> 6:51; birth counter 0:00 -> 7:14; ninety-kid class 2:19 -> 5:07 and 7:24; hand-holding 1:52 -> 7:43; Japan's two bumps 3:36 -> 5:26"
  ending_stack: "bookend + recap + thesis + CTA 7:22-8:13 (~11%), then 10 s end screen"
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

**One rule changes:** every person alive is born on the same morning, year included: 8,000,000,000 babies. To keep them alive, 2,000,000,000 adults from the old world are **on loan** (grey on every chart, one per four babies). They raise the cohort, and **on its thirtieth birthday they hand everything over and step out of the story**. That exit is a stated rule with a date, planted at 0:59 and paid at 3:53; nobody claims they all die of old age at 50-75. Everything else is real demography (current UN life tables and fertility) applied to one bar instead of a pyramid.

**Spine (tracker on screen from 0:08 to 7:14):** top-left `whatif/Hud`. Until 1:08 it reads `YEAR 0 · EVERYONE IS 0` with `BABIES 8,000,000,000` / `ADULTS 2,000,000,000`. From 1:08 it has two counters, `TOTAL ALIVE` (cohort + echoes + borrowed adults) and `YOUR AGE GROUP` (cohort only), plus a personal line `YOUR ODDS OF BEING THE LAST: 1 IN N` that updates at each act break (8 BN at 0:32, 7.5 BN at YEAR 30, 6.3 BN at 65, 3.8 BN at 80, 40 M at 100, 40,000 at 110, 40 at 120, then 1). A bottom `whatif/Scrubber` runs DAY 1 -> 125 with one icon per milestone, used identically everywhere: bottle `DAY 1`, desk `6`, key `30`, rocking chair `65`, candle `?`/`125`. The recurring board is `whatif/Pyramid`: the real 2024 world pyramid collapses into one amber bar at age 0, then the bar climbs one band per chapter, grey bands sit above it until the handover, teal echo bands grow under it from YEAR 20, and the shape slowly rebuilds into a pyramid.

**Personal thread:** "you" is one amber `whatif/Person` with a cream ring, seen in the crib field (0:00), the YOU crib (0:08), the night-feed close-up (1:18), the 90-kid class (2:19), graduation and the job queue (2:51), the bench (3:15), the recipe card (4:22), the retirement walk-out (4:32), the porch (4:56) and the last kitchen (6:51, ring shown with a `?`).

**Three visual modes (PLAYBOOK §12):** STORY = six flat 2D sets with stick-figure people (amber = the cohort, grey = old world, teal = echo); BOARD = navy chart board with the pyramid, stat pills and source lines; STAMP = full-width `whatif/YearStamp` chapter card (Anton year + small-caps subtitle, held >= 1.8 s) that flips in over the last frame.

**Frame zones (16:9):** HUD top-left (x 96, y 60-230); corner stamps top-right; `whatif/Pill` top-centre at y ~150 with its source line top-right; core word captions at y 0.82 (78-86%); `whatif/Scrubber` at y 94-98%. Nothing else is placed in the bottom 15%.

## Beat alignment table

| Our beat | Our time | Reference id + timestamp | Device borrowed | How we adapt it |
|---|---|---|---|---|
| L1a right-now fact + running tracker | 0:00-0:03 | b6jmbFcJZCY @0:00-0:01; PLAYBOOK §2 combination rule (tracker moving in the hook, top-4 outliers) | Present-tense true number before any fiction (H9) | Real births (~4 a second) on a live counter over an already-impossible frame: an endless field of cribs to the horizon, filling 4 per second |
| L1b impossible change in sentence two | 0:03-0:08 | b6jmbFcJZCY @0:07-0:13; 6oZ9fdM0n50 @0:10 | Narrator sets time-zero; premise at maximum scale ("every person") | "you, and everyone alive, born on the same morning"; 60 rows of a year's dots slam into one block |
| L1c sensory traces | 0:08-0:16 | b6jmbFcJZCY @0:20 (still-hot coffee, rolling cars); J3XahLkDEzU @0:04 (steaming coffees, a card machine beeping) | 2-3 mundane sensory details that make the impossible feel present | Eight billion cries at once; the planet smelling of warm milk |
| L1d self-correction exception | 0:16 | 6oZ9fdM0n50 @0:15 (H7) | One-line "not quite everyone" that leaves the scarce resource | The 2 billion borrowed adults, stated once as the concession; HUD `BABIES 8 BN · ADULTS 2 BN` |
| L1e trailer of dated promises | 0:21-0:32 | b6jmbFcJZCY @0:30-0:36 (H10), first paid @1:14 | 3 time-stamped consequences, each an on-screen tick, paid shortest-first | DAY 1 (four babies each) paid 1:18; age 6 (ninety kids) paid 2:19; 65 (one Monday) paid 4:29 |
| L1f master question | 0:32 | b6jmbFcJZCY @0:38 (withheld answer) -> @10:34 | Undated mystery whose answer is held back, not stated | "a birthday none of the other eight billion ever had"; the answer (the 125th, with nobody else turning that age) is held to 6:51 |
| L2a silent title card | 0:38-0:43 | 6oZ9fdM0n50 @0:31-0:38 | 5-8 s music-only card restating the question | 5 s title over the single amber bar, keyword "the same day" in amber |
| L2b rules + dated plant | 0:43-1:06 | b6jmbFcJZCY @0:16 (rules remove objections); y300HjYnHPw @0:20-0:27 (one stated rule + explicit "remember" plant); b6jmbFcJZCY @0:36 (on-screen countdown to a dated event) | Objection-killing rules, one fair concession, one dated rule the viewer is told to hold | No clones / no time machine; adults on loan at 1:4; "on your thirtieth birthday, they hand everything over"; new scrubber tick `30` + `HANDOVER IN 30 YEARS` chip |
| L2c start the clock | 1:08 | b6jmbFcJZCY @0:49 | One short line that starts the tracker | "Happy birthday, everyone." HUD switches to TOTAL ALIVE / YOUR AGE GROUP |
| L3 DAY 1: grounding + promise 1 + consequence chain | 1:10-1:51 | 6oZ9fdM0n50 @0:38-1:09 (target number -> real baseline -> "let's be generous" concession); b6jmbFcJZCY @1:14 (first promise paid) and @1:29-1:48 (who runs the plants that need people -> dominoes) | Baseline -> our number -> a one-person rung -> a consequence chain -> a concession -> deadpan button | 360,000/day vs 60 years before lunch; one adult's 40 feeds + 40 diapers; who runs power, farms, hospitals with 2 BN adults on night feeds; "we'll be kind" rule removes starvation; "nobody sleeps for a year" |
| L4 honeymoon + gag | 1:51-2:14 | J3XahLkDEzU @0:30-0:56 (fantasy-phase perks with comic exaggeration); 6oZ9fdM0n50 @1:30 (false resolution -> "except") | 3-4 perks rising in warmth, a deadpan logistics gag, then a crack line | Species walks in weeks; one bakery order for 8 BN cakes; nobody too old for the swings; "fairest world... until you turn six" |
| L5a YEAR 6 (promise 2 paid) | 2:14-2:28 | b6jmbFcJZCY @2:17-2:34 (chapter stamp -> named problem -> number pays the trailer item) | Stamp -> "here's the problem" -> one ratio | Fewer than 100 M teachers -> ~90 per class vs today's ~23 |
| L5b dated precedent + button | 2:28-2:50 | 6oZ9fdM0n50 @2:51-3:10 (history already ran it; short sentences ending on finality); b6jmbFcJZCY @4:10 (one-line ironic button) | "Impossible?" -> a real country ran a small version -> 3-gate cascade -> scale back to us -> button | Romania 1966-67 births nearly doubled; maternity -> school -> university; ×2 vs ×22,000; "year-group photo taken from orbit" |
| L6a YEAR 18 (one merged capacity beat) | 2:50-3:24 | b6jmbFcJZCY @2:40-2:42 (one named place generalised to every place); 6oZ9fdM0n50 @1:40 (relatable comic line) | One combined number -> a dated real crisis -> "for you, the whole planet" -> comedy button | University places 1 per 32 + 3.5 BN jobs in one sentence; Spain 2013; "dating is easy"; strollers set up the echo |
| L6b echo chapter (before YEAR 30) | 3:24-3:48 | 6oZ9fdM0n50 @1:12-1:24 (simple multiplier rule -> derived number); J3XahLkDEzU @0:14 -> @4:14 (a detail planted to be paid later) | Simple rule -> big derived number -> named concept -> real dated example, planted for later | TFR ~2.2 -> ~8 BN babies mostly inside 20 years (YEAR 20-45); "echo"; Japan's 1947-49 and 1971-74 bumps, paid at 5:26 |
| L7 midpoint rug pull (dated plant paid) | 3:48-4:29 (45%) | y300HjYnHPw @4:24-4:31 (rug pull recasts earlier problems + calls back the planted rule); b6jmbFcJZCY @3:22 ("this is the countdown from the start"); b6jmbFcJZCY @1:34-1:36 (anaphora of hidden human roles) | Own-words pivot -> explicit "date from the rules" callback -> the surprise consequence -> role anaphora | "But exams and jobs turn out to be the easy part." The adults step out on the date; the job shortage flips into every senior job being yours; surgeon still in training; judge, pilot, power-station engineer: thirty; no child has a grandparent |
| L8a YEAR 65 (promise 3 paid) | 4:29-4:56 | b6jmbFcJZCY @3:22-3:48 (promise callback -> mechanism -> "the problem is" -> number) and @5:54 (ironic button) | Promise callback -> event -> "here's the catch" -> real comparator -> our ratio -> button | ~6.3 BN retire on one Monday; the echo carries it; Japan 1:2 vs ours 3:4; "every golf course booked solid" |
| L8b emotional floor | 4:56-5:18 | 6oZ9fdM0n50 @4:05 (porch low point + either/or question); J3XahLkDEzU @9:27-9:33 (old-age chapter, loss stated plainly) | Quiet time-skip, plain statement of loss, fragment ladder, either/or question | YEAR 80: half gone, ~4x today's funerals, half of the ninety-kid class; "worth it, or losing everyone together?" |
| L8c reversal with evidence | 5:18-5:58 | 6oZ9fdM0n50 @4:20-5:36 ("but" turn -> dated real cases rising in closeness -> "you're proof" rung); b6jmbFcJZCY @4:14-4:37 (counter-intuitive relief backed by a precedent) | Mechanism -> dated real cases -> a checkable number -> a "you" rung | Japan's peaks: 2.7 M (1949) -> 2.1 M (1973) -> the expected third wave never came; your birthday 8 BN in a day vs the echo's busiest day ~1.5 M (EST.); your family has birthdays in every month |
| L9a centenarians + authority | 5:58-6:16 | 6oZ9fdM0n50 @2:12 ("one study estimated"); b6jmbFcJZCY @8:46 (rate-based number) | One cited study turned into a rule the viewer can run | ~40 M at 100 (EST.), >50x today's ~0.72 M; Barbi et al. 2018: ~50% a year past 105 as a coin toss |
| L9b speculation flag | 6:16 | J3XahLkDEzU @10:22-10:24 (T12) | Say aloud where firm data ends, right before the payoff | "less a forecast and more a dice roll"; `ESTIMATE` stamp on the HUD |
| L9c halving ladder | 6:21-6:34 | 6oZ9fdM0n50 @1:17-1:24 ("two becomes eight" ladder), run in reverse | Rhythmic number ladder, every step a count with its unit | "forty thousand... twenty thousand at a hundred and eleven. Then ten thousand. Five thousand... a few dozen of you"; HUD shows the age at each step |
| L9d record + master payoff (stage 1) | 6:34-7:04 | 6oZ9fdM0n50 @6:01-6:14 (hard number vs you); J3XahLkDEzU @10:30 (exact final count) | Real record -> "one of you beats it" -> exact final stamp -> the withheld answer | Calment 122 y 164 d; YEAR 125, ALIVE 1; "the birthday none of the others ever had": nobody else turning that age |
| L9e second-stage reveal (reversal in the last 20%) | 7:04-7:22 (84-86%) | b6jmbFcJZCY @10:08-10:34 (a second answer after the first, ending on the most human detail) | A new reveal after the payoff, built from plants | Pull out: family of every age, every one born on a different day (pays the echo + reversal); the 0:00 counter is back to four babies a second (pays line 1) |
| L10 bookend + recap + thesis | 7:22-7:59 | b6jmbFcJZCY @10:40-11:22 (back to time-zero, milestone recap, anaphora thesis with three callbacks); 6oZ9fdM0n50 @6:22 (bookend to the opening image) | Return to the opening image, icon recap, reframe, 3-callback anaphora | Crib field -> recap icons; "the gaps between us"; "someone holding your hand / teaching ninety kids / handing over the keys" (callbacks 1:52, 2:19, 3:55); "a relay race" |
| L11 CTA | 7:59-8:13 | 6oZ9fdM0n50 @6:22 (personal choice that bookends the opening); PLAYBOOK §7 (binary dilemma from options the video showed) | No-wrong-answer binary choice | The cohort or the echo, both shown throughout |
| End screen | 8:13-8:24 | 6oZ9fdM0n50 @6:31 | End cards over the bookend set | Two end cards over the blurred one-candle kitchen |

## The script

Layers: **VO** = narration (TTS; also drives word-level captions at y 0.82); **HUD** = top-left YEAR badge + counters + odds line; **PILL** = top-centre stat pill with its source line top-right; **STAMP** = chapter card; **TAG** = short small-caps keyword label. Timestamps below are computed from word counts at the stated per-section TTS rate with 0.12 s between lines; after TTS, re-time from Kokoro's word timings.

### Hook

- **First line (VO, 0:00):** "Every second, about four babies are born somewhere on Earth."
- **First visual (0:00):** the already-impossible frame: an endless field of cribs to the horizon at dawn, side-on rows shrinking into the distance. They are empty, and four light up amber every second under a live corner counter `BIRTHS THIS SECOND: 4`. One front crib carries a cream ring marked YOU. At 0:08 every crib fills at once.

### Voiceover, captions and on-screen text with timestamps

**[L1 COLD OPEN] 0:00-0:38** (TTS 158 wpm)
- 0:00 VO: Every second, about four babies are born somewhere on Earth.
- 0:00 ON-SCREEN: counter `BIRTHS THIS SECOND: 4` ticking in the corner over the crib field; PILL `~132 MILLION A YEAR`
- 0:03 VO: Now imagine you, and everyone alive, born on the same morning.
- 0:04 ON-SCREEN: 60 rows of 365 dots (`60 YEARS OF BIRTHS`) slam into one block; TAG `ONE MORNING`
- 0:08 VO: Same day as you. Same year as you.
- 0:08 ON-SCREEN: every crib fills at once; the YOU crib gets its ringed baby; HUD in: `YEAR 0 · EVERYONE IS 0`
- 0:11 VO: Eight billion newborns crying at once. The planet smells of warm milk.
- 0:11 ON-SCREEN: HUD `BABIES 8,000,000,000`
- 0:13 ON-SCREEN: warm milk-steam drifts over the field
- 0:16 VO: Not quite everyone, though: two billion borrowed adults are here to hold you.
- 0:17 ON-SCREEN: HUD adds `ADULTS 2,000,000,000`
- 0:21 VO: On day one, each adult gets four of you.
- 0:21 ON-SCREEN: scrubber draws in; tick `DAY 1` with bottle icon
- 0:24 VO: At six, your class has ninety kids.
- 0:24 ON-SCREEN: scrubber tick `6` with desk icon
- 0:27 VO: At sixty-five, you and the whole human race retire on one Monday.
- 0:27 ON-SCREEN: scrubber tick `65` with rocking-chair icon
- 0:32 VO: And one of you will get a birthday none of the other eight billion ever had.
- 0:32 ON-SCREEN: scrubber end tick `?` with unlit candle; HUD line `YOUR ODDS OF BEING THE LAST: 1 IN 8,000,000,000`

**[L2 TITLE CARD + RULES] 0:38-1:09** (TTS 158 wpm)
- 0:38 TITLE (music only, 5 s): What If Everyone On Earth Was Born On _The Same Day_?
- 0:43 VO: The rules. No clones. No time machine. Same planet, same cities.
- 0:44 ON-SCREEN: TAGs `NO CLONES` `NO TIME MACHINE` struck through; `SAME PLANET · SAME CITIES`
- 0:47 VO: One change: everyone alive shares your birthday, right down to the year.
- 0:48 ON-SCREEN: PYRAMID: the real 2024 world pyramid drains into one amber bar at age 0 (overflow chevron `×12`)
- 0:52 VO: To keep you alive, two billion adults are on loan from the old world: one per four babies.
- 0:53 ON-SCREEN: grey bands `THE OLD WORLD · 2,000,000,000 ON LOAN`; inset `1 ADULT : 4 BABIES`
- 0:59 VO: They raise you. Then, on your thirtieth birthday, they hand everything over and step out of the story.
- 1:01 ON-SCREEN: new scrubber tick `30` with key icon; chip `HANDOVER IN 30 YEARS`
- 1:06 VO: Keep that date in mind.
- 1:06 ON-SCREEN: pin drops on the grey bands; TAG `KEEP THIS DATE`
- 1:08 VO: Happy birthday, everyone.
- 1:08 ON-SCREEN: HUD switches to `TOTAL ALIVE 10,000,000,000` / `YOUR AGE GROUP 8,000,000,000`; scrubber dot starts

**[L3 DAY 1] 1:10-1:50** (TTS 164 wpm)
- 1:10 VO: Day one.
- 1:10 ON-SCREEN: STAMP `DAY 1` / `EIGHT BILLION BIRTHDAYS`
- 1:10 VO: Normally, the world handles about three hundred and sixty thousand births a day.
- 1:12 ON-SCREEN: bars `NORMAL DAY ~360,000`
- 1:15 VO: Today, you're sixty years' worth before lunch.
- 1:15 ON-SCREEN: bar `TODAY 8,000,000,000` overflows; PILL `~60 YEARS OF BIRTHS`
- 1:18 VO: That's the first promise: every adult on Earth has four newborns, and newborns feed every few hours, all night.
- 1:18 ON-SCREEN: the `DAY 1` bottle tick lights (promise 1 paid)
- 1:25 VO: That's around forty feeds and forty diaper changes, per adult, per day.
- 1:25 ON-SCREEN: stat `40 FEEDS + 40 DIAPERS / ADULT / DAY (EST.)`
- 1:30 VO: Here's the problem: who's running the power stations? The farms? The hospitals?
- 1:30 ON-SCREEN: three panels light: power station, farm, hospital, each tagged `UNSTAFFED?`
- 1:34 VO: Yesterday, three and a half billion people had jobs. Today, there are two billion adults, all of them up at night with you.
- 1:34 ON-SCREEN: bars `JOBS YESTERDAY ~3.5 BN` vs `ADULTS TODAY 2 BN · ALL ON NIGHT FEEDS`
- 1:43 VO: Fine. We'll be kind: the lights stay on, and nobody goes hungry.
- 1:43 ON-SCREEN: tags flip to ticks; TAG `RULE 2: LIGHTS ON · NOBODY HUNGRY`
- 1:47 VO: But nobody on Earth sleeps for about a year.
- 1:48 ON-SCREEN: TAG `SLEEP: 0`

**[L4 YEARS 1-5] 1:51-2:14** (TTS 160 wpm)
- 1:51 VO: Then it gets lovely.
- 1:51 ON-SCREEN: corner STAMP `YEAR 1`
- 1:52 VO: Over a few months, the whole species learns to walk, clinging to somebody's hand.
- 1:53 ON-SCREEN: TAG `FIRST STEPS: EVERYONE`
- 1:58 VO: Your birthday is a planet-wide holiday. Somewhere, a bakery gets an order for eight billion cakes.
- 2:00 ON-SCREEN: receipt rolls off-frame `ORDER: 8,000,000,000 CAKES`
- 2:04 VO: Nobody is the baby of the family. Nobody is ever too old for the swings.
- 2:04 ON-SCREEN: TAG `OLDEST KID ON THE SWINGS: 1`
- 2:10 VO: It's the fairest world there's ever been. Until you turn six.
- 2:12 ON-SCREEN: the desk tick blinks

**[L5 YEAR 6] 2:14-2:49** (TTS 164 wpm)
- 2:14 VO: Year six.
- 2:14 ON-SCREEN: STAMP `YEAR 6` / `FIRST DAY OF SCHOOL`
- 2:15 VO: The first day of school is one Monday, for everybody.
- 2:19 VO: Here's the problem: Earth has fewer than a hundred million teachers, so your class has about ninety kids in it. Today's average is twenty-three.
- 2:21 ON-SCREEN: stat `~90 KIDS PER TEACHER` / grey `TODAY ~23`; desk tick lights (promise 2 paid)
- 2:28 VO: Sound impossible? One country already ran a small version.
- 2:29 ON-SCREEN: map pin + ring on Romania; chip `1966`
- 2:31 VO: In nineteen sixty-six, Romania banned abortion almost overnight, and the next year, births nearly doubled.
- 2:32 ON-SCREEN: bars `1966 ~274,000` -> `1967 ~528,000`
- 2:37 VO: That one bulge jammed maternity wards, then classrooms, then university entrance, for twenty years.
- 2:37 ON-SCREEN: gates `MATERNITY` -> `SCHOOL` -> `UNIVERSITY` flash red
- 2:42 VO: Romania doubled one year. You're sixty years in a single morning.
- 2:42 ON-SCREEN: bars `ROMANIA ×2` vs `YOU ×22,000`
- 2:46 VO: Your year-group photo has to be taken from orbit.
- 2:47 ON-SCREEN: camera flash; TAG `YEAR-GROUP PHOTO: 7,700,000,000`

**[L6 YEAR 18] 2:50-3:23** (TTS 166 wpm)
- 2:50 VO: Year eighteen.
- 2:50 ON-SCREEN: STAMP `YEAR 18` / `EVERYONE GRADUATES`
- 2:51 VO: Everyone on Earth finishes school on the same day.
- 2:54 VO: The world has a quarter of a billion university places, about one per thirty-two of you, and three and a half billion jobs, with the old world sitting in most of them.
- 2:55 ON-SCREEN: 32 chairs, one lit; PILL `~250 M UNIVERSITY PLACES`
- 3:00 ON-SCREEN: stat `~3.5 BN JOBS / 8 BN APPLICANTS`
- 3:06 VO: In twenty thirteen, more than half of young Spaniards looking for work couldn't find any. They called it a crisis.
- 3:06 ON-SCREEN: map pin + ring on Spain; chip `2013`; PILL `SPAIN, UNDER-25 UNEMPLOYMENT ~56%`
- 3:13 VO: For you, it's the whole planet.
- 3:14 ON-SCREEN: every continent fills amber on 'planet'
- 3:15 VO: Dating is easy, though. Everyone is exactly your age.
- 3:17 ON-SCREEN: TAG `AGE GAP: 0`
- 3:19 VO: Which is why, a few years later, you all have kids. At once.
- 3:21 ON-SCREEN: strollers pop in across the park

**[L6b YEAR 24, THE ECHO] 3:24-3:47** (TTS 164 wpm)
- 3:24 VO: Year twenty-four.
- 3:24 ON-SCREEN: corner STAMP `YEAR 24`
- 3:25 VO: At a bit over two children per woman, a second wave rolls in: about eight billion babies, most of them inside twenty years.
- 3:25 ON-SCREEN: PILL `~2.2 CHILDREN PER WOMAN`; teal bands grow under the amber bar; HUD `TOTAL ALIVE` 9.9 -> 11.8 BN
- 3:33 VO: Demographers would call your kids an echo.
- 3:34 ON-SCREEN: TAG `THE ECHO`
- 3:36 VO: Japan has one: a boom after the Second World War, then a smaller one in the early seventies, when those babies had babies.
- 3:37 ON-SCREEN: mini Japan pyramid, chips `1947-49` and `1971-74`, arrow parent bulge -> child bulge
- 3:45 VO: Yours is the loudest echo in history.

**[L7 YEAR 30, MIDPOINT RUG PULL] 3:48-4:29** (TTS 156 wpm)
- 3:48 VO: But exams and jobs turn out to be the easy part.
- 3:48 ON-SCREEN: music cuts; the `KEEP THIS DATE` pin glows; scrubber key tick `30` flashes; chip `HANDOVER IN 0 YEARS`
- 3:53 VO: Year thirty. The date from the rules.
- 3:53 ON-SCREEN: corner STAMP `YEAR 30`
- 3:55 VO: On your thirtieth birthday, two billion adults hand over the keys and step out. All at once.
- 3:58 ON-SCREEN: every grey band lifts off the pyramid together; HUD `TOTAL ALIVE` 14.7 -> 13.0 BN
- 4:02 VO: Look at the chart. Nobody on Earth is older than you.
- 4:03 ON-SCREEN: TAG `OLDEST PERSON ALIVE: 30`
- 4:06 VO: At eighteen, there weren't enough jobs. But at thirty, every senior job on the planet is suddenly yours.
- 4:09 ON-SCREEN: TAG `OPEN TODAY: EVERY SENIOR JOB`
- 4:14 VO: The most experienced surgeon alive is still finishing their training.
- 4:14 ON-SCREEN: panel `SURGEON · STILL IN TRAINING`
- 4:17 VO: Every judge, every pilot, every power-station engineer: thirty. Same as you.
- 4:17 ON-SCREEN: panels `JUDGE 30` `PILOT 30` `POWER STATION 30`
- 4:22 VO: Your kids will never meet a grandparent. And nobody is left to ask how anything used to work.
- 4:22 ON-SCREEN: TAG `GRANDPARENTS: 0`

**[L8 YEAR 65, TRAILER PAID] 4:29-4:55** (TTS 164 wpm)
- 4:29 VO: Year sixty-five. The retirement promise comes due.
- 4:29 ON-SCREEN: STAMP `YEAR 65` / `ONE MONDAY`; rocking-chair tick lights (promise 3 paid)
- 4:32 VO: On one Monday, over six billion of you stop working, and every pension on Earth starts paying at once.
- 4:32 ON-SCREEN: stat `~6.3 BN RETIREES (EST.)`; HUD odds `1 IN 6,300,000,000`
- 4:39 VO: Here's the catch: who does the work? Your kids, the echo, now twenty to forty-five.
- 4:45 VO: Japan, the oldest big country today, has about one retiree for every two working-age adults. You have three for every four.
- 4:45 ON-SCREEN: icon rows `JAPAN TODAY 1 : 2`
- 4:50 ON-SCREEN: icon rows `YOUR WORLD 3 : 4`
- 4:52 VO: Every golf course on Earth is booked solid.
- 4:53 ON-SCREEN: TAG `TEE TIMES: SOLD OUT`

**[L8b YEAR 80, LOW POINT] 4:56-5:17** (TTS 148 wpm)
- 4:56 VO: Then come the hard years.
- 4:58 VO: Year eighty. Half of you are gone.
- 4:58 ON-SCREEN: corner STAMP `YEAR 80`; HUD `YOUR AGE GROUP 3,800,000,000`; odds `1 IN 3,800,000,000`
- 5:01 VO: The world holds four times today's funerals, and nearly every one is for someone your age.
- 5:01 ON-SCREEN: PILL `~4× TODAY'S YEARLY DEATHS (EST.)`
- 5:07 VO: Your friends. Your partner. Half of that ninety-kid classroom.
- 5:09 ON-SCREEN: the class photo from YEAR 6 loses half its faces
- 5:11 VO: Was sharing every birthday worth it? Or did it just mean losing everyone together?

**[L8c REVERSAL] 5:18-5:57** (TTS 160 wpm)
- 5:18 VO: But look at the chart again.
- 5:20 VO: Under your shrinking bar sits the echo, and under that, the echo's echo, lower and wider.
- 5:22 ON-SCREEN: TAG `ECHO OF THE ECHO`
- 5:26 VO: Japan already showed you how this ends.
- 5:29 VO: Its first boom peaked at two point seven million babies in nineteen forty-nine.
- 5:29 ON-SCREEN: chip `1949 · 2.7 M BIRTHS`
- 5:34 VO: The echo, in nineteen seventy-three, peaked at two point one million, spread across more years.
- 5:34 ON-SCREEN: chip `1973 · 2.1 M BIRTHS`
- 5:40 VO: But the third wave everyone expected around two thousand? It never really showed up.
- 5:40 ON-SCREEN: dotted bump `EXPECTED ~2000`; TAG `NEVER CAME`
- 5:45 VO: Your birthday put eight billion babies into one day. The echo's busiest day has about one and a half million.
- 5:45 ON-SCREEN: bars `YOUR BIRTHDAY 8,000,000,000` vs `ECHO'S BUSIEST DAY ~1,500,000 (EST.)` vs `TODAY ~360,000`; TAG `EACH WAVE: LOWER AND WIDER`
- 5:53 VO: By the time you're a hundred, your family has birthdays in every month.
- 5:53 ON-SCREEN: 12-month calendar inset fills with family birthdays

**[L9 YEARS 100-110, CLIMB] 5:58-6:21** (TTS 160 wpm)
- 5:58 VO: Year one hundred.
- 5:58 ON-SCREEN: STAMP `YEAR 100` / `THE CENTURY`; HUD switches to survivors mode
- 5:59 VO: Roughly forty million of you are still here, more than fifty times today's centenarians.
- 5:59 ON-SCREEN: stat `~40,000,000 AGED 100 (EST.)` / grey `TODAY ~0.72 M`; HUD odds `1 IN 40,000,000`
- 6:05 VO: But past a hundred and five, each birthday is a coin toss.
- 6:09 VO: A twenty eighteen study of Italy's oldest people found about half die before their next birthday, every year.
- 6:10 ON-SCREEN: PILL `105+: ~50% EACH YEAR` / source `Barbi et al., Science, 2018`
- 6:16 VO: From here on, this is less a forecast and more a dice roll.
- 6:17 ON-SCREEN: `ESTIMATE` stamp lands on the HUD

**[L9c YEAR 110, HALVING LADDER] 6:21-6:46** (TTS 154 wpm)
- 6:21 VO: At a hundred and ten, forty thousand of you.
- 6:21 ON-SCREEN: corner STAMP `YEAR 110`; HUD survivors `40,000`; odds `1 IN 40,000`
- 6:25 VO: Twenty thousand at a hundred and eleven. Then ten thousand. Five thousand.
- 6:25 ON-SCREEN: HUD `20,000` (YEAR 111)
- 6:28 ON-SCREEN: HUD `10,000` (YEAR 112)
- 6:29 ON-SCREEN: HUD `5,000` (YEAR 113)
- 6:30 VO: By a hundred and twenty, a few dozen of you.
- 6:30 ON-SCREEN: HUD `YEAR 120 · ~40`; odds `1 IN 40`
- 6:34 VO: The longest life on record is Jeanne Calment's: a hundred and twenty-two years and five months.
- 6:34 ON-SCREEN: PILL `RECORD: 122 YEARS, 164 DAYS (1875-1997)`; `122` marker on the scrubber
- 6:40 VO: With that many people rolling the same dice, one of you very likely beats her.
- 6:42 ON-SCREEN: the scrubber dot creeps past 122

**[L9d YEAR 125, MASTER PAYOFF + SECOND STAGE] 6:47-7:21** (TTS 148 wpm)
- 6:47 VO: Year one hundred and twenty-five. One of you is left.
- 6:47 ON-SCREEN: STAMP `YEAR 125` / `ALIVE: 1`; HUD odds `1 IN 1`
- 6:51 VO: And here's the birthday none of the others ever had.
- 6:55 VO: For the first time in their life, nobody else on Earth is turning the same age.
- 6:56 ON-SCREEN: one lit candle
- 7:02 VO: Eight billion birthdays, down to one.
- 7:04 VO: But that isn't the strangest part. Look who's at the table.
- 7:06 ON-SCREEN: pull out: family of every age around the table
- 7:09 VO: Grandkids. Great-great-grandkids. Every one of them born on a different day.
- 7:10 ON-SCREEN: date tags pop over the family: `MAR 3` `JUL 19` `FEB 29` `NOV 1` ...
- 7:14 VO: And outside, the counter from the very first second is back to normal: about four babies a second.
- 7:15 ON-SCREEN: corner counter `BIRTHS THIS SECOND: 4` returns from 0:00; candle tick lights; HUD and scrubber fade out

**[L10 BOOKEND + RECAP + THESIS] 7:22-7:59** (TTS 152 wpm)
- 7:22 VO: Go back to that first morning.
- 7:24 VO: Sixty years of births before lunch. Ninety kids to a class. Every job handed over in a day. One last candle.
- 7:25 ON-SCREEN: recap icons `DAY 1 · 60 YEARS OF BIRTHS` `YEAR 6 · 90 PER CLASS` `YEAR 30 · THE HANDOVER` `YEAR 65 · ONE MONDAY` `YEAR 125 · ONE CANDLE`
- 7:33 VO: All of it came from removing one thing: the gaps between us.
- 7:34 ON-SCREEN: TAG `THE GAPS`
- 7:38 VO: But in the real world, somebody is always a few steps ahead of you.
- 7:43 VO: Someone holding your hand while you learned to walk. Someone teaching ninety kids. Someone handing over the keys.
- 7:50 VO: A population pyramid isn't really a chart. It's a relay race, and it only works if somebody is right behind you.
- 7:53 ON-SCREEN: TAG `IT'S A RELAY`

**[L11 CTA] 7:59-8:13** (TTS 156 wpm)
- 7:59 VO: So, would you rather be one of the eight billion, sharing your birthday with the whole planet?
- 8:00 ON-SCREEN: card 1 `THE COHORT · ONE BIRTHDAY WITH 8 BN`
- 8:06 VO: Or one of their kids, born into a world where every grown-up is exactly the same age? Tell me below.
- 8:06 ON-SCREEN: card 2 `THE ECHO · EVERY GROWN-UP THE SAME AGE`

**[END SCREEN] 8:14-8:24**
- 8:14 two end-screen cards over the blurred one-candle kitchen; music out by 8:24

VO: 1242 words, 0:00-8:13 (150.9 wpm over the narrated span, 158.4 wpm spoken). 147 sentences, 34.0% in second person.

### On-screen text summary

- HUD: `YEAR n` badge (DAY 1, 0 -> 125) + subline; hook counters `BABIES 8,000,000,000` / `ADULTS 2,000,000,000`; from 1:08 `TOTAL ALIVE` and `YOUR AGE GROUP` (keyframes below); odds line `YOUR ODDS OF BEING THE LAST: 1 IN N`; survivors mode from YEAR 100 with an `ESTIMATE` stamp.
- STAMPS: DAY 1, YEAR 1, YEAR 6, YEAR 18, YEAR 24, YEAR 30, YEAR 65, YEAR 80, YEAR 100, YEAR 110, YEAR 125.
- TAGS: ONE MORNING, NO CLONES, NO TIME MACHINE, SAME PLANET · SAME CITIES, HANDOVER IN 30 YEARS, KEEP THIS DATE, RULE 2: LIGHTS ON · NOBODY HUNGRY, SLEEP: 0, FIRST STEPS: EVERYONE, OLDEST KID ON THE SWINGS: 1, YEAR-GROUP PHOTO: 7,700,000,000, AGE GAP: 0, THE ECHO, HANDOVER IN 0 YEARS, OLDEST PERSON ALIVE: 30, OPEN TODAY: EVERY SENIOR JOB, GRANDPARENTS: 0, TEE TIMES: SOLD OUT, ECHO OF THE ECHO, NEVER CAME, EACH WAVE: LOWER AND WIDER, ESTIMATE, THE GAPS, IT'S A RELAY.
- PILLS (each with a source line): ~132 M a year; 1 adult : 4 babies; ~60 years of births; 40 feeds + 40 diapers (EST.); ~3.5 BN employed; births nearly doubled (Romania); ~250 M university places · 1 per 32; Spain under-25 unemployment ~56%; ~2.2 children per woman; ~6.3 BN retirees (EST.); Japan 1:2 vs 3:4; ~4x today's yearly deaths (EST.); Japan births 1949 2.7 M / 1973 2.1 M; busiest birth day 8 BN -> ~1.5 M (EST.) -> today ~360,000; ~40 M aged 100 (EST.) vs ~0.72 M today; 105+ ~50% each year; record 122 y 164 d.

**HUD keyframes (whatif/Hud spec; EST. from the fact-sheet model):**

| At | YEAR | TOTAL ALIVE | YOUR AGE GROUP | odds line |
|---|---|---|---|---|
| 0:08-1:08 | YEAR 0 | (hook mode) BABIES 8,000,000,000 · ADULTS 2,000,000,000 from 0:16 | — | 1 IN 8,000,000,000 from 0:32 |
| 1:08 | YEAR 0 | 10,000,000,000 | 8,000,000,000 | — |
| 1:10 | DAY 1 | 10,000,000,000 | 8,000,000,000 | — |
| 1:51 | YEAR 1 | 9,800,000,000 | 7,800,000,000 | — |
| 2:14 | YEAR 6 | 9,700,000,000 | 7,700,000,000 | — |
| 2:50 | YEAR 18 | 9,900,000,000 | 7,600,000,000 | — |
| 3:24 | YEAR 24 | 9,900,000,000 -> 11,800,000,000 (counts up over e2) | 7,600,000,000 | — |
| 3:48 | YEAR 30 | 14,700,000,000, then 13,000,000,000 when the grey bands lift | 7,500,000,000 | 1 IN 7,500,000,000 |
| 4:29 | YEAR 65 | 21,200,000,000 | 6,300,000,000 | 1 IN 6,300,000,000 |
| 4:58 | YEAR 80 | 22,200,000,000 | 3,800,000,000 | 1 IN 3,800,000,000 |
| 5:58 | YEAR 100 | (survivors mode, hidden) | ~40,000,000 | 1 IN 40,000,000 |
| 6:21 / 6:25 / +2.6 s / +3.6 s / 6:30 | 110 / 111 / 112 / 113 / 120 | — | 40,000 / 20,000 / 10,000 / 5,000 / ~40 | 1 IN 40,000 ... 1 IN 40 |
| 6:40 | YEAR 122 | — | ~7 | 1 IN 7 |
| 6:47 | YEAR 125 | — | 1 | 1 IN 1 |

## Shot list

**Status: BLOCKED-ON-KIT.** `studio/src/kits/` has demo, explainer, horror and thumbs only, and `kits/index.ts` registers no `whatif/*`. Build order: (1) `whatif/Pyramid`, `whatif/IconRows`, `whatif/Pill` -> render the gate shot (0:47-1:01) at 1080p on the Spark (`--concurrency=4`) and get it reviewed; (2) only then `whatif/Hud`, `whatif/Scrubber`, `whatif/YearStamp`, `whatif/Person`, `whatif/Crowd`, `whatif/Set`; (3) the rest.

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

| # | t_start | t_end | shot type | visual description (kit vocabulary) | camera move | SFX |
|---|---|---|---|---|---|---|
| 1 | 0:00.0 | 0:03.9 | STORY extreme wide (impossible frame 0) | `whatif/Set` `ward` = the crib field: side-on rows of cribs to the horizon at dawn (per-row scale for depth, `whatif/Crowd` age baby capped at 480 near cribs + static pattern fade beyond row 4). Cribs are empty; 4 light up amber each second. Corner `explainer/Stat` counter `BIRTHS THIS SECOND: 4`. One front crib carries the cream YOU ring, still empty. `whatif/Pill` `~132 MILLION A YEAR`. | slow `pullOut` 0.3 | `documentary_pulse` bed in low; soft `pop` per lit crib |
| 2 | 0:03.9 | 0:08.2 | BOARD graphic | Navy board: 60 rows x 365 columns of amber dots labelled `60 YEARS OF BIRTHS` slide together from both sides into one bright block; `explainer/Tag` `ONE MORNING`. | `pullOut` 0.15 as the strip compresses | `whoosh_long`, `impact` when the block lands |
| 3 | 0:08.2 | 0:11.4 | STORY wide | Back on the crib field: every crib fills at once with an amber baby (`whatif/Crowd` fill 0 -> 1 in 0.5 s); the YOU crib's baby gets its cream ring. `whatif/Hud` fades in top-left `YEAR 0 · EVERYONE IS 0`. | keyframed push to the YOU crib (zoom 1 -> 1.25) | `stinger` + music swell (no layered-breath crowd) |
| 4 | 0:11.4 | 0:16.1 | STORY extreme wide | The full field, tiny `waa` glyphs popping above cribs; cream milk-steam `particles` (dust preset, rising) drift across. HUD `BABIES 8,000,000,000`. | `pullOut` 0.5 (ease out) | music swell holds; soft `pop`s |
| 5 | 0:16.1 | 0:21.1 | STORY medium | Grey adult `whatif/Person` (pose hold) figures stand up between the cribs, one per four cribs; one holds the YOU baby. HUD adds `ADULTS 2,000,000,000`. | `drift` | music drops to bass only |
| 6 | 0:21.1 | 0:32.1 | BOARD trailer | Navy board; `whatif/Scrubber` draws in along the bottom (DAY 1 -> 125). Ticks pop with the VO: bottle `DAY 1`, desk `6`, rocking chair `65`, each with a small vignette above it (one grey adult + 4 cribs; a 9x10 grid of kids; one calendar page `MONDAY`). | keyframed pan right along the ticks | `tick` + `pop` per milestone |
| 7 | 0:32.1 | 0:38.6 | STORY close-up | `whatif/Set` `kitchen` at night: `whatif/Cake` with a forest of ~120 unlit candles, one candle in front; scrubber end tick `?` with candle icon; HUD line `YOUR ODDS OF BEING THE LAST: 1 IN 8,000,000,000`; amber light falls off at the edges (`grade` vignette 0.45). | slow `pushIn` toward the front candle | `riser` into the title card |
| 8 | 0:38.6 | 0:43.6 | TITLE card (5 s, music only) | `explainer/Headline` in Anton, centred on navy: What If Everyone On Earth Was Born On _The Same Day_? (keyword amber); behind it a single amber bar (`whatif/Pyramid`, one band at age 0). | static | music hit on the cut; no VO |
| 9 | 0:43.6 | 0:47.9 | BOARD | `explainer/Tag` `NO CLONES` then `NO TIME MACHINE`, each crossed by an animated red strike-through `rect` (no clone-vat or time-machine drawings); then `SAME PLANET · SAME CITIES`. | `drift` | `click` x2 on the strikes |
| 10 | 0:47.9 | 0:52.6 | BOARD signature shot (GATE SHOT, part 1) | `whatif/Pyramid` starts as the real 2024 world pyramid (21 bands, male left / female right, data in storyboard), then `morph` over 3 s: every band drains sideways into one amber bar at age 0. Fixed x-scale: 0.7 BN = 40% of half-width; the 8 BN bar (x12) clips at the board edge with an overflow chevron and a `×12` label; camera eases out (zoom 1 -> 0.85) as the bar lands. | hold, then keyframed ease-out zoom 1 -> 0.85 | `whoosh_long` + `underwater_rumble` as the drain |
| 11 | 0:52.6 | 1:01.1 | BOARD (GATE SHOT, part 2) | Pyramid adds grey bands at ages 20-45 labelled `THE OLD WORLD · 2,000,000,000 ON LOAN`; `whatif/IconRows` `1 ADULT : 4 BABIES` inset bottom-right; `whatif/Pill` source `infant-care ratio guidance`. | static | `pop` on bands and inset |
| 12 | 1:01.1 | 1:08.5 | BOARD detail | `whatif/Scrubber` returns with a new tick at 30 (key icon); chip `HANDOVER IN 30 YEARS`; on r5 a red pin drops onto the grey bands; `explainer/Tag` `KEEP THIS DATE`. | keyframed zoom 1 -> 1.15 on the pin | `tick` on the new tick; `ding` on the pin |
| 13 | 1:08.5 | 1:10.1 | STORY wide | Back to the crib field; paper bunting and one balloon per front-row crib pop up; HUD switches to `TOTAL ALIVE 10,000,000,000` / `YOUR AGE GROUP 8,000,000,000`; the scrubber dot starts moving. | `pullOut` 0.1 | `pop` cascade; music returns full |
| 14 | 1:10.1 | 1:11.9 | STAMP | `whatif/YearStamp` full width `DAY 1` / `EIGHT BILLION BIRTHDAYS` (Anton). | flip-in (`whip` up) | `whoosh` |
| 15 | 1:11.9 | 1:18.5 | BOARD | `explainer/SpeedBars`: `NORMAL DAY ~360,000` (thin) vs `TODAY 8,000,000,000` (runs off the right edge); `whatif/Pill` `~60 YEARS OF BIRTHS`. | keyframed pull out to fit the long bar | `tick` on bar 1; `whoosh_long` as bar 2 overflows |
| 16 | 1:18.5 | 1:30.0 | STORY close-up (one-person rung) | `whatif/Set` `ward` at night, close: one grey adult `whatif/Person` (pose hold) between four cribs, the YOU baby in one; a wall `explainer/Timer` (ring) spinning fast; the `DAY 1` bottle tick lights (promise 1 paid). On d5: `explainer/Stat` `40 FEEDS + 40 DIAPERS` / `PER ADULT, PER DAY (EST.)` and a pile of instanced diaper icons grows beside the adult, with `explainer/Bus` for scale. | `pushIn` 0.4 | `ding` on the tick; `clock_ticking`; `pop` per diaper |
| 17 | 1:30.0 | 1:43.1 | BOARD consequence chain | Three navy panels light in sequence: power station, farm, hospital icons, each with a red `UNSTAFFED?` tag. On d7: `explainer/SpeedBars` `JOBS YESTERDAY ~3.5 BN` vs `ADULTS TODAY 2 BN · ALL ON NIGHT FEEDS`; source ILO. | `drift` | `click` per panel; `tick` on the bars |
| 18 | 1:43.1 | 1:47.6 | BOARD | The three `UNSTAFFED?` tags flip to green ticks; `explainer/Tag` `RULE 2: LIGHTS ON · NOBODY HUNGRY`. | static | `ding` |
| 19 | 1:47.6 | 1:51.3 | STORY button | The adult from s16 asleep standing up; all four babies wide awake; `explainer/Tag` `SLEEP: 0`. | `pushIn` micro | silence beat, then one `click` |
| 20 | 1:51.3 | 1:58.3 | STORY wide, warm | `whatif/Set` `park`: a wave of amber toddlers (`whatif/Crowd` age kid, pose walk) take first steps left to right, each holding a grey adult's hand; the YOU toddler mid-frame; corner `whatif/YearStamp` `YEAR 1`; Tag `FIRST STEPS: EVERYONE`. | slow `panRight` with the wave | soft `footsteps`; music lifts |
| 21 | 1:58.3 | 2:04.4 | STORY gag | Split: left, `explainer/Map` at global zoom, every continent highlighted amber, plain amber pins (no cake glyphs); right, `whatif/Set` `kitchen` counter where a receipt `rect` rolls off the bottom of frame: `ORDER: 8,000,000,000 CAKES`. | `drift` | `pop` per pin; `typing` as the receipt prints |
| 22 | 2:04.4 | 2:10.2 | STORY | `whatif/Set` `park` playground: a swing set full of same-size amber toddlers, no older kids anywhere; Tag `OLDEST KID ON THE SWINGS: 1`. | `drift` | music only |
| 23 | 2:10.2 | 2:14.7 | STORY transition | The park freezes (all idles stop); the desk tick on `whatif/Scrubber` blinks. | keyframed push toward the scrubber tick | `tick` x2, low `stinger` |
| 24 | 2:14.7 | 2:16.6 | STAMP | `whatif/YearStamp` `YEAR 6` / `FIRST DAY OF SCHOOL`. | `whip` up | `whoosh` |
| 25 | 2:16.6 | 2:19.3 | STORY wide | `whatif/Set` `classroom` (door view): a queue of amber kids with backpack icons wraps out of the door and off-frame. | `panLeft` along the queue | school bell = `ding` x3 fast |
| 26 | 2:19.3 | 2:28.2 | STORY interior | `whatif/Set` `classroom`: one grey teacher `whatif/Person` (pose point) at the chalkboard facing a 9 x 10 grid of amber kids on the floor; the YOU kid ringed in the back row; `explainer/Stat` `~90` / small grey `TODAY ~23`; the desk tick lights (promise 2 paid). | `pullOut` 0.4 to reveal the whole class | soft `boom` on the 90; `ding` on the tick |
| 27 | 2:28.2 | 2:32.5 | BOARD | `explainer/Map` flies from global to Romania via `views` (lon 25, lat 46, zoom 5); a pin + pulsing ring at (25, 46) labelled `ROMANIA` (no country polygon); chip `1966`. | map `views` keyframes (no camera zoom preset) | `whoosh` |
| 28 | 2:32.5 | 2:37.3 | BOARD | Two bars grow side by side: `1966 ~274,000` -> `1967 ~528,000`; source line `INS Romania (verify)`. | static | `tick` + `ding` |
| 29 | 2:37.3 | 2:42.5 | BOARD cascade | The 1967 bulge as one amber block on a mini Romania pyramid slides upward through three labelled gates `MATERNITY` -> `SCHOOL` -> `UNIVERSITY`, each flashing red as it squeezes through. | `panUp` following the block | `whoosh` per gate |
| 30 | 2:42.5 | 2:46.7 | BOARD comparison | `explainer/SpeedBars` `ROMANIA ×2` (short) vs `YOU ×22,000` (runs off-frame). | `pullOut` | `whoosh_long` |
| 31 | 2:46.7 | 2:50.4 | STORY button | `whatif/Set` `park` from very high: rows of amber kids filling every field to the horizon (static pattern); a white camera-flash `rect` pulse; Tag `YEAR-GROUP PHOTO: 7,700,000,000`. | `pullOut` 0.6 | `click` as shutter |
| 32 | 2:50.4 | 2:52.2 | STAMP | `whatif/YearStamp` `YEAR 18` / `EVERYONE GRADUATES`. | `whip` up | `whoosh` |
| 33 | 2:52.2 | 2:54.6 | STORY wide | `whatif/Set` `classroom` (hall): rows of amber teens toss mortarboard icons at the same instant; the YOU teen front-left. | `pullOut` 0.3 | `pop` cascade |
| 34 | 2:54.6 | 3:00.6 | STORY | 32 chair icons in a row, one lit amber with a mortarboard; 31 amber teens look at it; `whatif/Pill` `~250 M UNIVERSITY PLACES`. | `panRight` along the row | `pop` on the lit chair |
| 35 | 3:00.6 | 3:06.3 | STORY wide | `whatif/Set` `office`: grey old-world `whatif/Person` figures (pose sit) at desks behind glass; an amber queue (the YOU teen near the front) runs out of the door and off-frame as an amber path; `explainer/Stat` `~3.5 BN JOBS` / `8 BN APPLICANTS`. | `pullOut` from the door | `footsteps` shuffle; `notify` pings |
| 36 | 3:06.3 | 3:15.9 | BOARD | `explainer/Map` to Spain via `views` (lon -3.7, lat 40.4, zoom 5) with a pin + ring `SPAIN`; chip `2013`; `whatif/Pill` `SPAIN, UNDER-25 UNEMPLOYMENT ~56%`. On 'planet' the view pulls to global and all six continent keys highlight amber. Shot holds 0.8 s past 'planet'. | map `views` keyframes in, then out to global | `whoosh`; `whoosh_long` on the flood |
| 37 | 3:15.9 | 3:19.3 | STORY button | `whatif/Set` `park` bench: two amber 18-year-old `whatif/Person`s (pose sit), identical height; Tag `AGE GAP: 0`. | static | `ding` |
| 38 | 3:19.3 | 3:24.4 | STORY | Same bench, now with a stroller icon beside it; across the park a whole row of strollers pops in at once. | `pullOut` 0.5 | `pop` cascade |
| 39 | 3:24.4 | 3:33.8 | BOARD | Corner `whatif/YearStamp` `YEAR 24` over `whatif/Pyramid`: amber bar at 24, grey bands at 44-69, teal echo bands growing at ages 0-5; `whatif/Pill` `~2.2 CHILDREN PER WOMAN`; HUD `TOTAL ALIVE` counts 9.9 -> 11.8 BN. | `pullOut` 0.2 | music returns; `pop` per teal band |
| 40 | 3:33.8 | 3:45.0 | BOARD | Tag `THE ECHO`; inset mini Japan pyramid with two bulges, chips `1947-49` and `1971-74`, an arrow from parent bulge to child bulge. (Planted here; paid in the reversal.) | keyframed push to the inset | `sonar_ping` x2 (echo) |
| 41 | 3:45.0 | 3:48.0 | STORY wide | `whatif/Set` `park`, now crowded with teal toddlers and amber parents (the YOU parent with a teal kid). | `pullOut` | music swell (no breath murmur) |
| 42 | 3:48.0 | 3:53.1 | BOARD interrupt | Music cuts; the navy board goes dark except the `KEEP THIS DATE` pin from s12 glowing on the grey bands; the key tick `30` flashes; chip `HANDOVER IN 0 YEARS`. | slow `pushIn` | silence, then `heartbeat_slow` once |
| 43 | 3:53.1 | 4:02.6 | BOARD signature shot | Corner `whatif/YearStamp` `YEAR 30`; `whatif/Pyramid` at YEAR 30: amber bar at 30, teal echo bands at 0-12 below it, grey bands at 50-75 above. On m3 every grey band lifts off the top together (they step out; nobody dies) and a key icon drops from the grey into the amber bar; HUD `TOTAL ALIVE` 14.7 -> 13.0 BN. | static | `whoosh_long` as the grey lifts; `ding` on the key |
| 44 | 4:02.6 | 4:06.9 | BOARD | Same pyramid, nothing above the amber bar; Tag `OLDEST PERSON ALIVE: 30`. | keyframed push on the empty space above the bar | faint `static` |
| 45 | 4:06.9 | 4:14.0 | STORY wide (callback to s35) | `whatif/Set` `office` from s35, now with empty desks; the amber queue walks in and sits (YOU at the corner office); Tag `OPEN TODAY: EVERY SENIOR JOB`. | `panRight` | `footsteps` |
| 46 | 4:14.0 | 4:22.3 | BOARD role panels | Four navy panels, each an amber 30-year-old `whatif/Person` with a hat: scrubcap `SURGEON · STILL IN TRAINING`, then wig `JUDGE 30`, cap `PILOT 30`, hardhat `POWER STATION 30` (no cockpit/OR/court sets). | `drift` | `click` per panel |
| 47 | 4:22.3 | 4:29.7 | STORY quiet | `whatif/Set` `kitchen`: the amber YOU adult holds an old recipe card in grey handwriting nobody can ask about; a teal kid at the table; an empty chair; Tag `GRANDPARENTS: 0`. | slow `drift` | room tone only (music still out) |
| 48 | 4:29.7 | 4:32.3 | STAMP | `whatif/YearStamp` `YEAR 65` / `ONE MONDAY`; the rocking-chair tick on `whatif/Scrubber` lights. | `whip` up | `whoosh`; `ding` on the tick |
| 49 | 4:32.3 | 4:39.4 | STORY wide | `whatif/Set` `office` street side at 9:00: every door opens and amber elders (`whatif/Person` age elder, pose walk, holding a box) walk out at once; YOU among them; `explainer/Stat` `~6.3 BN RETIREES (EST.)`; HUD odds `1 IN 6,300,000,000`. | `panRight` along the street | `whoosh` as doors swing; `footsteps` |
| 50 | 4:39.4 | 4:45.0 | STORY | `whatif/Set` `office`: a single teal worker at a desk behind a tower of paperwork (stacked `rect`s). | `pushIn` | `typing` |
| 51 | 4:45.0 | 4:52.8 | BOARD | `whatif/IconRows`: `JAPAN TODAY 1 : 2`, then `YOUR WORLD 3 : 4` stacks beneath; source `Japan Statistics Bureau 2023`. | static | `tick` per row |
| 52 | 4:52.8 | 4:56.2 | STORY button | `whatif/Set` `park`: a long queue of amber elders with a single flag icon at the far end; Tag `TEE TIMES: SOLD OUT`. | `panRight` | `ding` |
| 53 | 4:56.2 | 5:01.3 | STORY dusk | `whatif/Set` `porch` at sunset: two amber elders in rocking-chair icons, one is YOU; corner `whatif/YearStamp` `YEAR 80` on r80b; HUD `YOUR AGE GROUP 3,800,000,000`. | slow `pullOut` | music thins (`documentary_pulse` at 0.12) |
| 54 | 5:01.3 | 5:11.6 | STORY quiet | The 90-kid class grid from s26 returns as a framed photo on the porch wall; figures fade out of it to half (`whatif/Crowd` fadeOut 0 -> 0.5); `whatif/Pill` `~4× TODAY'S YEARLY DEATHS (EST.)`. | slow `pushIn` on the photo | `heartbeat_slow` under |
| 55 | 5:11.6 | 5:17.7 | STORY quiet | The porch again: the YOU elder alone; the second rocking chair still rocking, empty. | static | silence |
| 56 | 5:17.7 | 5:26.6 | BOARD signature shot | `whatif/Pyramid` YEAR 80: shrinking amber bar at 80, teal echo bands at 35-62, a softer second-echo band below; bands widen and blur (smoothed `bands` track); Tag `ECHO OF THE ECHO`. | `pullOut` 0.3 | `sonar_ping` soft x2; music returns |
| 57 | 5:26.6 | 5:45.5 | BOARD (plant from s40 paid) | Japan births line chart (`svg` path, 1945-2010): chip `1949 · 2.7 M`, chip `1973 · 2.1 M`, then a dotted bump outline `EXPECTED ~2000` with nothing under it; Tag `NEVER CAME`. Source `MHLW vital statistics`. | `panRight` along the line | `tick` per chip; `knock` on NEVER CAME |
| 58 | 5:45.5 | 5:53.1 | BOARD | `explainer/SpeedBars`: `YOUR BIRTHDAY 8,000,000,000` (off-frame) vs `ECHO'S BUSIEST DAY ~1,500,000 (EST.)` vs `TODAY ~360,000`; Tag `EACH WAVE: LOWER AND WIDER`. | `pullOut` | `tick` per bar |
| 59 | 5:53.1 | 5:58.4 | BOARD | The chart outline morphs toward a pyramid; a thin cream outline of the 2024 pyramid from s10 overlays; inset: a 12-month calendar grid where each month lights with a family figure (`BIRTHDAYS IN YOUR FAMILY: 12 MONTHS`). | static | soft `riser` |
| 60 | 5:58.4 | 6:05.0 | STAMP + BOARD | `whatif/YearStamp` `YEAR 100` / `THE CENTURY` (held 1.8 s), then the board: HUD switches to survivors mode; `explainer/Stat` `~40,000,000 AGED 100 (EST.)` with grey `TODAY ~0.72 M`; odds `1 IN 40,000,000`. | `whip` up into the board | `whoosh`; `ding` |
| 61 | 6:05.0 | 6:16.5 | BOARD | A coin icon flips every 1.5 s above a row of 10 elder icons; half grey out each flip; `whatif/Pill` `105+: ~50% EACH YEAR` with source `Barbi et al., Science, 2018`. | static | `click` per flip |
| 62 | 6:16.5 | 6:21.8 | BOARD | A red `ESTIMATE` stamp lands across the HUD; a dice icon tumbles in. | `shake` 0.15 s | `knock` (dice clack) x2 |
| 63 | 6:21.8 | 6:34.2 | BOARD countdown | Corner `whatif/YearStamp` `YEAR 110`; HUD survivors `40,000` -> `20,000` (111) -> `10,000` (112) -> `5,000` (113) -> `~40` (120) on the VO beats while a `whatif/Crowd` elder grid halves each beat; odds line follows (`1 IN 40,000` ... `1 IN 40`). | keyframed push, one step per halving | `tick` per halving, getting quieter |
| 64 | 6:34.2 | 6:40.6 | BOARD | `whatif/Pill` `RECORD: 122 YEARS, 164 DAYS (1875-1997)` beside a generic cream elder silhouette (no likeness); a `122` marker drops onto the scrubber. | keyframed pan right to the 122 marker | `ding` |
| 65 | 6:40.6 | 6:46.9 | BOARD | The dice roll again; the scrubber dot creeps past the 122 marker; HUD `~7`. | slow `pushIn` | `knock` x2; `riser` |
| 66 | 6:46.9 | 6:51.6 | STAMP | `whatif/YearStamp` `YEAR 125` / `ALIVE: 1`; HUD survivors `1`, odds `1 IN 1`. | `dipBlack` in, stamp fades up | music out; one `heartbeat_slow` |
| 67 | 6:51.6 | 7:05.0 | STORY close | `whatif/Set` `kitchen`, morning: one amber elder at the table wearing the YOU ring with a small `?` (maybe it's you); `whatif/Cake` with one lit candle. | slow `pushIn` on the elder | room tone; music returns very soft |
| 68 | 7:05.0 | 7:14.1 | STORY wide (second-stage reveal) | Pull out from the elder to reveal the whole table: teal, cream and new-colour `whatif/Person`s of every age (kid to adult), each with a small date tag (`MAR 3`, `JUL 19`, `FEB 29`, `NOV 1` ...). | keyframed pull out (zoom 1.3 -> 1.0) | soft `pop` per date tag |
| 69 | 7:14.1 | 7:22.0 | STORY extreme close | Corner counter `BIRTHS THIS SECOND: 4` from s01 returns and flicks, through the kitchen window; then the single candle flame; the scrubber candle tick lights; HUD and scrubber fade out together. | keyframed push to the flame, then hold | soft `pop` x4/s under the counter; a `breath` out, flame stays lit |
| 70 | 7:22.0 | 7:33.1 | STORY bookend + recap | `glitch` 0.2 s back to the s01 crib-field framing; the cribs dissolve into a horizontal recap icon timeline: bottle `DAY 1`, desk `YEAR 6`, key `YEAR 30`, rocking chair `YEAR 65`, candle `YEAR 125` (the same icons as the scrubber ticks). | locked on the 0:00 composition, then pan right along the icons | `pop` per icon |
| 71 | 7:33.1 | 7:38.0 | BOARD | `whatif/Pyramid` 2024 real shape again; the gaps between bands glow; Tag `THE GAPS`. | `pushIn` 0.1 | music swells gently |
| 72 | 7:38.0 | 7:50.9 | STORY (three callbacks) | `whatif/Set` `park` path, side-on: a toddler holding an adult's hand (callback 1:3x first steps), a teacher with a few kids (callback YEAR 6), an older figure handing a key to a younger one (callback YEAR 30); every figure a different shirt colour. | slow `panRight` along the path | soft `footsteps` |
| 73 | 7:50.9 | 7:59.6 | STORY | The same figures in one line, `point` poses; a glowing cream `circle` (the baton) travels along a path from elder to adult to teen to child; Tag `IT'S A RELAY`. | `panLeft` following the baton back to the child | soft `whoosh` per hand-off |
| 74 | 7:59.6 | 8:14.5 | CTA board | `explainer/Options` (text-only list, title `PICK ONE`): `THE COHORT · ONE BIRTHDAY WITH 8 BN` / `THE ECHO · EVERY GROWN-UP THE SAME AGE`, staggered in with the VO. | static | `pop` per item |
| 75 | 8:14.5 | 8:24.5 | END SCREEN | The one-candle kitchen set with `blur` 12 on the background layer (core `grade` has no blur); two end-card placeholder `rect`s. | static | music out by the end |

75 contiguous shots, 0:00-8:24. Transitions are centred on cuts and never change length. Every STAMP shot is >= 1.8 s; the next VO line starts under the stamp. Shot 36 holds until 0.8 s after "planet" so the flood lands on the word.

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
