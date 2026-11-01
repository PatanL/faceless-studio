# Explainer corpus: sources (12 viral outliers)

Niche: ocean/animal "you vs X" 2D explainer (Depth Theory style). Our output mix is 6 Shorts (60-90 s) and 4 long-form videos (8-10 min). The corpus therefore has 6 long-form and 6 short-form references.

Gathered 2026-11-01, ~09:00-09:25 UTC. All yt-dlp calls ran on the Spark (`~/.local/bin/yt-dlp`). Whisper ran on the Spark CPU only (`CUDA_VISIBLE_DEVICES=""`, faster-whisper small, int8, 4 threads).

`outlier_score = current views / channel median views` for the same format (long uploads for long videos, the Shorts tab for Shorts). The median basis is written on line 2 of each raw file. Raw transcripts are in `raw/<id>.txt`. Line 1 of each file is `# url | title | channel | views | outlier_score | duration`.

## The 12

| # | id | Format | Channel | Title | Views | Outlier | Dur | Transcript |
|---|---|---|---|---|---|---|---|---|
| 1 | fGcgWaswMns | long | Depth Theory | Why You'd Never Want To Meet A Sperm Whale | 2,307,237 | 14.65 | 9:59 | auto-subs |
| 2 | nAWpLtG-kNs | long | Fossil | How Long You'd Last in Every Prehistoric Era | 12,209,257 | 113.57 | 16:10 | whisper (subs 429) |
| 3 | VtrcKTkhDHU | long | OctoLab | Why The Ocean's Deadliest Predator Refuses To Kill Us | 8,289,332 | 318.82 | 33:42 | auto-subs |
| 4 | mzeN0BXR4e0 | long | Mr. Science | Why Deep Sea Creatures Get Creepier the Deeper You Go | 17,219,766 | 12.86 | 17:57 | auto-subs |
| 5 | JkAcCdqYJN0 | long | Occam | Every Animal That Could Swallow You (Only One Actually Can) | 332,151 | 15.82 | 9:11 | auto-subs |
| 6 | QxM2Hu70tVk | long | Dumb Doggo | What It's Like To Be Eaten By A Carnivorous Plant | 16,181,706 | 2.82 | 8:49 | auto-subs |
| 7 | XFFjxTllpoA | short | Casual Geographic | What if You Ate The Most Poisonous Animal in the World? | 7,931,305 | 1.69 | 0:59 | whisper (no subs) |
| 8 | jw6bS-WL4F4 | short | Casual Geographic | Why This Tiny Jellyfish Is Much Worse Than You Think | 6,716,278 | 1.43 | 0:58 | whisper (no subs) |
| 9 | Ky0XPonYDcc | short | Casual Geographic | You could've FaceTimed an Eel.... | 8,605,626 | 1.83 | 0:40 | auto-subs |
| 10 | 4QGQhaRv4Dw | short | Zack D. Films | Man Lost Floating In Ocean | 23,762,035 | 2.97 | 0:38 | auto-subs |
| 11 | fmZfphacPPQ | short | Zack D. Films | Could You Survive Extreme Ocean Pressure? | 14,711,279 | 1.84 | 0:33 | auto-subs |
| 12 | 6mRR91AbxjQ | short | Zack D. Films | How Horseflies Bite You | 13,689,674 | 1.71 | 0:28 | whisper (subs 429) |

## Why each was chosen

1. **fGcgWaswMns, Depth Theory sperm whale.** This is the seed and the style we are copying. It got 2.3M views on a 6K-sub channel (about 380x subs). Its structure: a second-person cold open ("you're floating... then you feel it"), a myth-vs-reality reframe (orcas vs the sperm whale), a size comparison (bus, elephants), a weapons and senses breakdown, an escalation into the attack scenario, and "your options". Every beat maps to the explainer kit: scale bar, stick-figure YOU, stat callouts, depth meter.
2. **nAWpLtG-kNs, Fossil "How Long You'd Last".** This is the biggest "you" survival outlier in the niche: 12M views on a 51K-sub channel, 114x the channel median. It uses a time-machine premise, then one era per segment with a survival-time verdict. The countdown/verdict device ("you're toast") fits our "how long would you last against X" Shorts and long-form ladders.
3. **VtrcKTkhDHU, OctoLab orca.** This has the most extreme outlier score found (319x, 8.3M views on an 82K-sub channel). The format is a curiosity paradox ("a predator that could obliterate us has never hunted a human. Why?"), followed by a history/myth beat and layered explanations. It is 33 min, so we only use its hook and paradox engine, which suit a long-form open.
4. **mzeN0BXR4e0, Mr. Science "creepier the deeper you go".** 17M views, 12.9x. The structure is a depth ladder: sunlight zone, then twilight, then midnight, with creatures getting stranger at each step. This is the core escalation device, and the depth-meter component renders it directly. Spinosnack (33x) and BeyondTheBlue (9.7x) reuse the same title formula, which shows the format repeats across channels.
5. **JkAcCdqYJN0, Occam "Every Animal That Could Swallow You".** 15.8x on a 2.9K-sub channel. It is the closest match to our long-form spec: 9 min, 2D, a numbered countdown (#8 to #1) with a "time survived inside" stopwatch per animal and a narrator mascot, and the title has a twist ("only one actually can"). It is directly reusable as a ranking-ladder template.
6. **QxM2Hu70tVk, Dumb Doggo carnivorous plant.** 16M views. It is a 2D "what it's like" series built on second-person POV ("picture this... your insect brain is lured in"), a numbered countdown, and comic voice breaks ("LET ME OUT!"). It shows how to keep a death-by-animal ladder light enough for a broad audience. The outlier score is the lowest of the long set (2.8x) because the channel median is already 5.7M.
7. **XFFjxTllpoA, Casual Geographic pufferfish.** 7.9M views. This is the model Short for "what if you X": a one-line hook, a timeline in minutes ("first 10 minutes... after 30-40 minutes... a few hours"), "but don't worry, it gets worse", then a twist fact (people eat it). It is narrated 2D and maps onto a timer plus symptom callouts.
8. **jw6bS-WL4F4, Casual Geographic Irukandji jellyfish.** 6.7M views. The device is small size against an enormous threat ("small enough to never see it coming", "100x worse than a cobra"), with escalating symptoms and a "that's not the worst part" re-hook. It is an ocean topic, and the escalation is the one we want in a 60 s Short.
9. **Ky0XPonYDcc, Casual Geographic eel.** 8.6M views. This is a true-story Short with an absurd hook (FaceTiming eels so they stay used to humans). It is the reference for a story-led ocean Short instead of a danger-led one, and it uses a tight setup, problem, resolution in 40 s.
10. **4QGQhaRv4Dw, Zack D. Films "Man Lost Floating In Ocean".** 23.8M views, 3x the median of a 29.5M-sub channel. A survival narrative told in 35 s: fall overboard, ship leaves, the shark bump, rescue. The style is 3D, but the beat structure works in 2D, and it is the template for an "alone in the open ocean" Short.
11. **fmZfphacPPQ, Zack D. Films "Could You Survive Extreme Ocean Pressure?".** 14.7M views. A pure depth ladder in 30 s (10 m, then 100 m, 1,000 m, 3,000 m) with one body consequence per step, ending in "implode instantly". It is the most compact version of the Depth Theory escalation and works as a depth meter plus stick figure.
12. **6mRR91AbxjQ, Zack D. Films "How Horseflies Bite You".** 13.7M views. This is the "how X hurts YOU" anatomy Short: six mouthparts explained as tools (scissors, saw, pump) in second person. It is not about the ocean, but the device of a weapon breakdown by everyday analogy is the one we use for teeth, tentacles and stingers. It is included because the "how X hurts you" title formula is the strongest Shorts hook in the animal space.

## Runners-up (not transcribed)

- 4CzYXfBeIdM, WILD VERSUS "This Is Why Orcas Are Called Killer Whales". 56M views, 83x. Auto-subs were downloaded on the Spark, but it is real or stock footage, not 2D, so its structure is less reusable.
- OZAfse9Pb4c, Meet Arnold "What If the Whale Swallowed You Alive?". 19.7M views, a 2D POV Short. It is age-gated, and yt-dlp can't fetch it without cookies.
- FcAns8s3Kiw, Spinosnack "The Deeper You Go, The Creepier Prehistoric Oceans Get" (33x), and qrfhhZ-Wvmk, BeyondTheBlue "How Long You'd Last in Every Prehistoric Ocean" (11.4x). Both use the same formulas as #4 and #2.
- 2819-mQEA9M (colossal squid, 0.79x) and 4Mmo_dlsArE (humpback whale, 0.09x) are Depth Theory controls. Their transcripts are already in `research/R1/subs/` and are useful for "what didn't pop" comparisons.

## Notes

- YouTube rate-limited subtitle downloads (HTTP 429) for #2 and #12. Those two and the two Casual Geographic Shorts with no English auto-captions were transcribed with whisper from audio downloaded on the Spark. The audio and WAVs are in `dgx-spark:~/studio/refs/explainer/corpus/audio/`, and the VTTs are in `.../corpus/subs/`.
- Auto-caption text has some ASR errors (for example "covet" for "covid" in #9, and "midget box jellyfish" or "murder guppiest" in the whisper output). Timestamps are the caption-line start times.
- None of these videos is caption-only, so no frame OCR was needed.
- Use these for structure and devices only. Never reuse their wording (see the originality gate in BRIEF.md).

## Expansion (12:08 UTC)

Twelve more sources, gathered 2026-11-01, 12:08-12:30 UTC. Eight come from channels not in the first twelve (What If, The Infographics Show, Kurzgesagt, Spinosnack, BRIGHT SIDE, BlackWater, BeyondTheBlue, WILD VERSUS). Two are the biggest new outliers from corpus channels (Fossil, Occam). One is a marked ordinary control (Casual Geographic). The set is 6 Shorts and 6 long-form videos.

Method is the same as above. All yt-dlp calls ran on the Spark (`~/studio/bin/yt-dlp`, `nice -n 10`). Auto-subs were used where YouTube served them. Six videos hit HTTP 429 on subtitles, or had no captions at all, so their audio was downloaded on the Spark and transcribed with faster-whisper small on the CPU (`CUDA_VISIBLE_DEVICES=""`, int8, 4 threads, VAD, one process). Files on the Spark are in `~/studio/refs/explainer/corpus/exp2/` (`subs/`, `audio/`, `search/`, `raw/`). Shorts medians come from fresh Shorts-tab listings on the Spark (`exp2/search/sh_<channel_id>.jsonl`). Long-form medians come from `research/library.jsonl` (the 11:08Z daily pull). Line 2 of every raw file gives the median basis.

| # | id | Format | Channel | Title | Views | Outlier | Dur | Transcript | Role |
|---|---|---|---|---|---|---|---|---|---|
| 13 | 2d6Ciu3INeA | short | What If | What If You Grew 1cm Every Second? | 3,324,843 | 69.27 | 2:52 | auto-subs | outlier |
| 14 | V15wrmD5VFs | short | The Infographics Show | What Happens When You Are Shot | 2,975,684 | 11.34 | 0:29 | whisper (subs 429) | outlier |
| 15 | ZZf1KBnH5iI | short | Spinosnack | Which Prehistoric Animal Has The Strongest Bite? | 391,946 | 4.90 | 1:30 | whisper (subs 429) | outlier |
| 16 | LpUzg3Dc-m0 | short | BRIGHT SIDE | Never Take Seashells From Beaches, Here's Why! | 104,937 | 3.68 | 0:52 | whisper (subs 429) | outlier |
| 17 | 2cK8l5Yg5w8 | short | Kurzgesagt – In a Nutshell | The Deadliest Thing in Your Kitchen | 5,194,382 | 3.58 | 1:07 | whisper (no captions) | outlier |
| 18 | PoF_doh3NOE | short | Casual Geographic | Meet the Megabat (Real Life Dracula??) | 6,504,016 | 1.38 | 0:58 | auto-subs | CONTROL |
| 19 | UNPK8PNCCmQ | long | Fossil | Would Orcas Dominate Every Prehistoric Ocean? | 3,855,897 | 35.87 | 19:07 | whisper (subs 429) | outlier (same channel as #2) |
| 20 | thtoMGvpWIU | long | Occam | How Long Would Your Pet Survive in the Wild? | 518,793 | 24.70 | 9:45 | auto-subs | outlier (same channel as #5) |
| 21 | UfbYyHuVx5M | long | WILD VERSUS | This Sheep Killed a Cow | 7,617,260 | 18.83 | 8:15 | auto-subs | outlier |
| 22 | lVV5ztC3CtI | long | Spinosnack | This NEW Evidence Just Gave T. Rex a Terrifying Buff | 1,504,773 | 7.88 | 20:11 | whisper (subs 429) | outlier |
| 23 | SDs41Ke3v4Q | long | BlackWater | Scientists Dropped Alligators Into the Deep Sea. Here's What Ate Them | 6,059,544 | 6.57 | 17:42 | auto-subs | outlier |
| 24 | qrfhhZ-Wvmk | long | BeyondTheBlue | How Long You'd Last in Every Prehistoric Ocean | 3,374,140 | 6.54 | 17:37 | auto-subs | outlier |

### Why each was chosen

13. **2d6Ciu3INeA, What If "Grew 1cm Every Second".** This is the highest-scoring Short found (69x the channel's Shorts median). It is a pure second-person time-lapse escalation: 1 minute, then 1 hour, a day, 10 days, 116 days, 11 years, and so on up to the size of the universe. Each rung has one concrete size comparison (10-story building, Eiffel Tower, Everest, the Moon) and one body consequence. It also has a "but let's ignore that, this is what if" permission beat. It is the scale-ladder device at its most extreme, and it runs about 2:50, so it also shows how the ladder holds up at the 3-minute Shorts cap.
14. **V15wrmD5VFs, Infographics Show "What Happens When You Are Shot".** 11x. It is a 29-second "what happens to YOUR body" anatomy Short: one mechanism per sentence (cavity, ricochet, fragmentation, bleeding), all in second person. It is the "how X hurts you" breakdown (compare #12) from a different channel, and the shortest script in the corpus.
15. **ZZf1KBnH5iI, Spinosnack "Strongest Bite".** 4.9x. This is a ranking-ladder Short with a single repeated unit of comparison (pickup trucks), anchored on "you" first (your bite, about 200 lb). The ladder runs from you to a lion, Dunkleosteus, a croc, T. rex, Purussaurus, Deinosuchus and Megalodon. A mid-ladder re-hook ("it still doesn't even make the top three") is followed by a reveal ("every animal that beats a T. rex lives in water"). It is the template for our "bite force ladder" and "you vs X" stat Shorts.
16. **LpUzg3Dc-m0, BRIGHT SIDE "Never Take Seashells".** 3.7x. An ocean "never do X, here's why" Short: a fake-out legend hook ("just kidding... but seriously"), then reason 1 (ecology), reason 2 (habitat) and reason 3 (it is illegal in some places). It is the warning/command title formula with a list body.
17. **2cK8l5Yg5w8, Kurzgesagt "Deadliest Thing in Your Kitchen".** 3.6x on a 1.45M Shorts median, 5.2M views. The cold open is past-tense second person ("Something in your kitchen killed you"). Then a suspect lineup (sugar, cinnamon, saffron, salt), each with a lethal dose, and a joke twist winner (bananas and antimatter), closed with "case closed". It is the "suspect ladder + absurd twist" device, and it shows how a top 2D studio paces a 65-second list.
18. **PoF_doh3NOE, Casual Geographic Megabat. CONTROL.** 1.38x, an ordinary performer from the channel behind #7-9. It is a "meet the X" profile with a "you" size hook ("if you're no taller than 5'6", this bat is bigger"), jokes, then a "they're actually harmless/important" turn. Use it against #7-9 to see what the danger-led Shorts do that this one doesn't.
19. **UNPK8PNCCmQ, Fossil "Would Orcas Dominate Every Prehistoric Ocean?".** 35.9x, the biggest new long-form outlier. It reuses the corpus #2 era-ladder engine, but with a modern animal as the traveller instead of "you". It defines its scoring terms up front ("dominate" vs "establish") and gives one verdict per era. It is the template for "Would X survive every prehistoric ocean" long-forms. Depth Theory's own mg2YJ04Hl9k (1.0x) is the matching control.
20. **thtoMGvpWIU, Occam "How Long Would Your Pet Survive in the Wild?".** 24.7x. A countdown (#8 to #1) with the same checkpoints for every entry (1 hour, 1 day, 1 week, 1 year), passed or failed. The open stacks three teasers ("wouldn't survive the first night", "wipes out raccoons", "costs less than a sandwich"). It states a rule the viewer must "remember" and later uses it to knock out favorites. It is a cleaner checkpoint/verdict device than corpus #5.
21. **UfbYyHuVx5M, WILD VERSUS "This Sheep Killed a Cow".** 18.8x, 7.6M views. It is a footage-led clip compilation, so only the narration structure transfers. It opens with a proverb twist, then a run of clash vignettes, each with one stat (weight, horn mass, double-layered skull), and the absurd-underdog title. It is included as the strongest "underdog beats bigger animal" outlier for the versus-format Shorts and long-forms.
22. **lVV5ztC3CtI, Spinosnack "NEW Evidence Gave T. Rex a Terrifying Buff".** 7.9x. A "new study" news-hook long-form. The open is a second-person myth-bust ("the movie says freeze and it can't see you; in real life freezing gets you killed"). Then it lists the upgrades as a teaser stack (vision, metabolism, bite), sets up "for decades scientists said it was overhyped", and turns with "the new evidence points to something far worse". After that, each upgrade gets its own segment: a named study, a number, and a comparison to you. Spinosnack runs it as a series (Megalodon, Mosasaurus and Spinosaurus versions are 5-7x). The "new evidence just changed X" frame works for our ocean-giant topics.
23. **SDs41Ke3v4Q, BlackWater "Scientists Dropped Alligators Into the Deep Sea".** 6.6x, 6.1M views. It opens with a real experiment's setup and an open question ("what down there could possibly eat one?"), then a three-question roadmap (why alligators, how you get them, how you sink them), an interview, and a reveal. It is the true-story mystery-box engine for deep-sea long-forms, and the long-form counterpart to the story Short #9.
24. **qrfhhZ-Wvmk, BeyondTheBlue "How Long You'd Last in Every Prehistoric Ocean".** 6.5x. It is the ocean-only copy of #2's formula on another channel. Its open says "picture this... you get dropped" and sets up an expectation it then reverses ("you'd expect a 50-ft monster... then you realize it's only about 2 ft long"). Each era gets a life-expectancy verdict. It proves the format repeats, and it is the closest long-form premise to our ocean "how long would you last" episodes.

### Expansion notes

- Rejected candidates: Spinosnack VBrlFxlDChg (10.8x) and other "#memes" Shorts are meme edits, not narrated explainers. Zack D. Films' top Shorts (outlets, hide-and-seek, Dobermans) are off-niche, and the channel already has 3 sources. The Infographics Show's other top Shorts are war and geopolitics. What If's WdPUtf3IZvM ("What Happened Immediately After the Dinosaurs Went Extinct?", 20x) is a good backup. ExtinctZoo eWu92oXtxsw (4.0x, 41 min) was left out for length.
- Every video in the expansion is narrated, so no frame-caption reading was needed. No TikTok explainer outliers were found, so all sources are YouTube.
- Whisper output has some ASR errors, for example "pushing a sign tissue" (pushing aside tissue) in #14, "Pyrosaurus/Dinosuchus" (Purussaurus/Deinosuchus) in #15, "bigs orcas" (Bigg's orcas) in #19, and "waits" (weights) in the #23 auto-subs.
- As before, use these for structure and devices only, and never reuse their wording.
