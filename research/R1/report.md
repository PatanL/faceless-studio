# R1 report

_Saved by the orchestrator from the lane's returned findings (subagents cannot write report files). Outputs: /Users/patrickliu/Documents/faceless-studio/research/R1/videos.json, /Users/patrickliu/Documents/faceless-studio/research/R1/topics.json, /Users/patrickliu/Documents/faceless-studio/research/R1/beatmaps/fGcgWaswMns.md, /Users/patrickliu/Documents/faceless-studio/research/R1/beatmaps/mg2YJ04Hl9k.md, /Users/patrickliu/Documents/faceless-studio/research/R1/beatmaps/2819-mQEA9M.md, /Users/patrickliu/Documents/faceless-studio/research/R1/beatmaps/fGcgWaswMns.shots.csv, /Users/patrickliu/Documents/faceless-studio/research/R1/beatmaps/mg2YJ04Hl9k.shots.csv, /Users/patrickliu/Documents/faceless-studio/research/R1/beatmaps/2819-mQEA9M.shots.csv, /Users/patrickliu/Documents/faceless-studio/research/R1/beatmaps/*.shot_mix.json, /Users/patrickliu/Documents/faceless-studio/research/R1/sheets/depththeory_thumbs.jpg, /Users/patrickliu/Documents/faceless-studio/research/R1/sheets/peer_thumbs_A.jpg, /Users/patrickliu/Documents/faceless-studio/research/R1/sheets/peer_thumbs_B.jpg, /Users/patrickliu/Documents/faceless-studio/research/R1/sheets/frames/ (21 contact sheets, 5s/frame), /Users/patrickliu/Documents/faceless-studio/research/R1/subs/ (auto-subs, word timings, transcripts), /Users/patrickliu/Documents/faceless-studio/research/R1/raw/ (metadata, peer listings, cut/change JSON), /Users/patrickliu/Documents/faceless-studio/research/R1/tools/ (spark_frames.py, spark_changes.py, build_videos.py, build_shots.py, subs2txt.py, peers.py), dgx-spark:~/studio/refs/R1/*.mp4 + analysis/<id>/{f5,cuts_

R1 is done and committed as bbf801c (research/R1 only). report.md is not on disk: the harness blocks subagents from writing report files. Its content is condensed here, and everything else is in the R1 folder.

DEPTH THEORY IS A NEW CHANNEL WITH ONE HIT. It has 6,080 subs and 4 uploads posted between Oct 26 and Nov 1, with a median of 140,742 views. Views and ages were read on Nov 1 around 08:42 UTC.

| Video | Views | Age | Outlier vs median | Views/sub | Like rate | Words/min | Hard cuts/min | Visual changes/min |
|---|---|---|---|---|---|---|---|---|
| Sperm whale | 2,289,672 | 4.8 days | 16.3x (9.9x per day) | 377 | 0.41% | 168 | 3.2 | 10.5 |
| Great white, every prehistoric ocean (19:41) | 157,498 | 3.3 days | 1.1x | | | 151 | 4.6 | |
| Colossal squid | 123,985 | 6.0 days | 0.9x (0.4x per day) | | | 171 | 3.1 | |
| Humpback | 12,222 | 6 hours | 49K/day pace | | | | | |

There are no Shorts. The low like rate on the hit fits algorithm-driven reach well beyond the subscriber base.

TITLES. Three of four use "Why You'd Never Want To Meet A [Animal]". The hit and the flop share that title, so the animal choice is what mattered. The great white title, its "Still King?" crowned thumbnail and its format closely copy Fossil's "Would Orcas Dominate Every Prehistoric Ocean?" (3.8M views, 35x that channel's median).

THUMBNAILS. I looked at all four. They are a black monochrome engraving of the creature filling two-thirds of the frame, a tiny diver with a torch for scale, a red arrow, and 2-3 words naming a sense, in white with a red "YOU" ("IT HEARS YOU..", "IT SEES YOU.."). BeyondTheBlue and OctoLab use the same house style, and it does not match the video art.

VISUAL STYLES. Each upload uses a different art style:
- **Sperm whale (the hit):** flat vector with no outlines on a near-black navy gradient (about #0f2a36 at the top to #000405 at the bottom), with god rays and floating particles. The whale is a grey silhouette. Labels are white uppercase sans, with red underlined headlines (about #d9483b). Props include a yellow bus, stick-figure jokes and cream paper cards. Only about 3% is stock footage.
- **Colossal squid:** the same system with a red-brown squid, and about 12% stock footage.
- **Great white:** outlined cartoon creatures on brighter teal, kinetic captions with one orange or red emphasised word, era title cards, a time dial and a crown/check/skull scoreboard.
- **Humpback:** a third style with blueprint grids and x-ray views.

The kit should target the sperm whale look. It is the simplest to build in code and the one with proven reach.

PACING. Narration runs about 170 words per minute. Hard cuts are rare, about 3 per minute with an 18-second mean shot. A new visual idea still appears about every 5 seconds, because labels, props and counters build on one canvas with slow push-ins. In Remotion that means one scene is a single canvas with timed layers.

SCRIPT TEMPLATE. The sperm whale and squid videos reuse it almost line for line:

| % of runtime | Beat |
|---|---|
| 0-5 | Second-person hook: a comforting rule, broken by a sensory detail, then the animal is revealed. Title drop at 4-9% |
| 5-10 | "Most people think X... and yes... but" plus 3 superlatives |
| 10-20 | Scale against a bus, elephants, your hand |
| 20-60 | 3-4 escalations, each opened by a question card and closed by a joke. One callback to the hook and one recent study with year and place |
| 60-70 | "I know the question we're all thinking... let's break it down": 4-5 numbered options, each struck through with fact, analogy and joke, then a hard verdict |
| 70-78 | Twist: "here's the surprising part" (it doesn't hunt you) |
| 78-90 | The real danger is us |
| 90-96 | Ecology payoff, then a bookend back to the opening image |
| 96-100 | Comment CTA ("I do actually read them"), no subscribe ask |

Jokes land about every 55 seconds, and 10 minutes is about 1,680 words. A 60-90 second pilot works out to about 220 words. The great white video is a tournament instead: 10 eras of about 95 seconds, each with a title card, world-building, rivals on a scale bar with myth-busting sizes, a dive escape test and a verdict, plus running scoreboards.

SHOT MIX for the sperm whale video, as a share of 5-second windows: creature with labels 18%, illustrated scenes 14%, diver or "you" 12%, jokes 8%, creature alone 7%, charts 7%, stats 6%, then smaller shares of options list, sonar overlays, paper cards, scale, depth and map. Every code maps to a kit component in the beat maps.

SIMILAR CHANNELS:

| Channel | Subs | Median | Top outliers |
|---|---|---|---|
| BeyondTheBlue (closest analogue) | 258K | 289K | Every Prehistoric Ocean 3.3M (11x), Antarctic giants 2.8M, squids creepier deeper 2.8M |
| OctoLab | 82K | 26K | Why The Ocean's Deadliest Predator Refuses To Kill Us 8.2M (315x), sperm whale 1.1M (42x) |
| Fossil | 51K | 108K | How Long You'd Last in Every Prehistoric Era 12M (112x), orcas every ocean 3.8M (35x) |
| Mr. Science | 265K | 1.25M | Deep sea creatures get creepier the deeper you go 17M (13.6x) |
| Occam (flat 2D stick-figure style, closest to ours) | 2.9K | 21K | Every Animal That Could Swallow You 332K (16x), pet survival 518K (25x) |

I also checked BlackWater, Spinosnack, ExtinctZoo and WILD VERSUS; WILD VERSUS has the orca video at 56M (83x).

The format is already being copied. Searches turned up 20+ copycat channels posting the same titles within days, mostly under 500 views, so the title alone does not carry a video.

15 TOPICS, ranked by evidence (details in topics.json):
1. Orca
2. Sinking to the bottom of the ocean, depth by depth
3. How long would you last in every prehistoric ocean
4. Humboldt squid
5. Every ocean animal that could swallow you
6. Leopard seal
7. Greenland shark
8. Megalodon
9. Why Antarctic water makes giants
10. Saltwater crocodile
11. Anglerfish
12. Why orcas won't touch a sperm whale
13. Box jellyfish
14. Great white
15. Walrus

For the P1 pilot I recommend Orca, or the depth-descent video if the explainer kit is behind, since it mostly reuses the depth meter and gradient. I recommend against PLAN.md's default colossal squid: it was Depth Theory's weakest video per day, and other channels already cover it.

HOW IT WAS RUN. Metadata, auto-captions and thumbnails came from the Mac. Video downloads, frame sampling and cut detection ran on the Spark CPU in its own environment (~/studio/venvs/r1) with no GPU, keeping 150 MB of reference video in ~/studio/refs/R1. Only small contact sheets (4.1 MB) came back to the Mac. The shot labels come from looking at every 5-second frame. Captions are auto-generated, so some species names are misspelled.
