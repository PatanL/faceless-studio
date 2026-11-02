# Owner's reference accounts (collected 2026-11-01, not piloted)

The owner is collecting references for future formats. Don't start pilots from this list without the owner's go-ahead.

| Account | What it is | How it's made (best guess) | Numbers seen | Code-only fit |
|---|---|---|---|---|
| bob.figures.it.out (IG) | Relationship comedy: deadpan second-person narrator, literal-minded escalation, punchline | Two fixed low-poly 3D characters, 3–4 reused sets, expression swaps, TTS voice | 155K followers; median ~1.2M views/reel, top 7.3M (research/R4/report.md) | Easy (our kit machinery). Needs our own cast; clean version for YouTube (profanity) |
| capisean_capisara (IG) | "Couple life, but make it capybara": same couples humour with a cute capybara couple. Original series by @oleh_tishechko | Pixar-like 3D, almost certainly an AI video model | 205K followers; reels behind the login wall | Premise yes, look no (needs video model). Lesson: cute animal cast lifts couples premises |
| amodiniolga_art (IG), reel De19SpSNL6v | 19 s emotional mother/daughter Pixar-style short, no narration, music-led (Russian caption, tagged AI) | AI video model | 1.76M likes, 7K comments (posted 2026-10-23) | No (video model) |
| grumo.2004 | Dogs replacing people in viral funny clips | Not checked: yt-dlp couldn't read it as a TikTok account (private/embedding off, or it's on another platform). Need a link to one post | — | Unknown |
| goldenretrieverswitze | Golden-retriever jokes (German name) | Not checked, same as above | — | Unknown |
| antrofrog_ (X) | Painterly 2D character vignettes (a frog-like guy in a black coat doing absurd gags around New York), cut to a song | AI video (bio: "an artist with zero skills so I just use AI"); 1080p 24 fps; owner's idea: Codex image frames plus reference motion | Joined Sep 2026, 33.2K followers; pinned "Englishman in New York" 33M views, 293K likes, 34K reposts | Look needs image-to-video or very heavy code animation. Note: it's set to a commercial song, which would be claimed on YouTube |
| loxiv.stories (IG), reel De6wom9MexO | A buff macho man who transforms into a cute, soft guy at home. Owner: the second recurring pattern, a **transformation hook and payoff** (the first being relatable couples) | Not checked: the reel is audience-restricted, so it can't be fetched logged out | — | Premise yes (a two-state character swap is easy in code); look unknown |
| mama.clubnika (IG), post 9e3EZHM1S9g | Relatable cartoons (owner). Russian account, 465K followers; bio is a sewing business plus "teaching AI"; story highlights "Мульт Ai" (AI cartoons) and "Кино Ai" (AI film) | AI video, by the highlight names. The post needs a login (not a YouTube ID; Instagram returned no media logged out) | 465K followers | Same as amodiniolga_art: emotional/relatable AI cartoon look needs a video model |
| funny.ai.moments (IG, "Funny & Fantasy AI"), reel De8pKfovnya | A pug and a French bulldog standing at a kitchen counter making coffee badly: pouring misses, grounds and milk spill, the pug stares at camera. 15 s, no narration, caption "Monday morning brain be like...". Owner: it reuses a format first seen as an old-couple cartoon making coffee | Photoreal AI video (same shot throughout, phone-camera look). A real-brand jar sits in frame | 732K likes, 6.4K comments (posted 2026-10-26) | No (photoreal video model). The idea, a proven viral bit recast with animals, transfers |
| vi_skh (IG), reel De6W4ZITnJh | Another couples account (owner). Profile "vi \| ai series • claude • tools": AI creatives and series episodes; a Higgsfield creative partner (affiliate link in bio) who says they work with Claude every day | AI video via Higgsfield (an AI video platform). The reel needs a login | 43.9K followers | Look no (video model); couples premise yes |
| bim_and_tim (IG) | "AI cartoons: Tim the Cat & Bim the Puppy", a cute recurring pet pair; created by @tavivna, takes custom cartoon orders | AI video (bio says AI cartoons) | 28.2K followers | Owner: this kind needs the AI-cartoon look to sell the animals' cuteness, so it's a video-model format |

Reference media on the Spark: ~/studio/refs/ig/ (De19SpSNL6v.mp4, antrofrog_2116118225582718976.mp4).

## Patterns the owner has named so far

1. **Relatable couples/family life** (bob.figures.it.out, capisean_capisara, amodiniolga_art, mama.clubnika, vi_skh): shareable to a partner or parent; cute or distinctive recurring characters.
2. **Transformation hook and payoff** (loxiv.stories): open on one extreme version of a character, pay off with the opposite (macho outside → cute at home). The hook sets an expectation and the payoff flips it.
3. **Recast a proven viral bit with animals** (funny.ai.moments, grumo.2004, goldenretrieverswitze): take a clip or format that already went viral (an old couple making coffee, a famous funny moment) and replay it with dogs or other animals in the human roles. The original's success de-risks the premise, and the animal swap makes it new and cute.

## Owner's direction (2026-11-01)

- **Code-made explainers** keep the Bob-figures-it-out style of narration and premise (second person, literal escalation, punchline) as an option for the explainer channel.
- **Cute cartoon couples/pets** (bim_and_tim, capisean_capisara and similar) need the AI-cartoon look. The owner is considering a GPU to run MiniMax H3 for that lane.
- **Licence check (MiniMax H3 open weights, Hugging Face LICENSE, 2026-08-02):** the weights are licensed only for the "Applicable Territory", which excludes the United States, the EU, the UK and South Korea. Running the downloaded weights locally in the US isn't covered by that licence. The hosted API (platform.minimax.io; also on OpenRouter as minimax/hailuo-3, from about $0.13 per generated second) has its own terms; check them. Commercial use over $20M yearly revenue needs written permission, and products must display "MiniMax H3".

## Channel direction candidate: RicksClips3000 (YouTube), 2026-11-01

Owner is leaning toward Rick's Clips / Zack D. Films / Kurzgesagt-Shorts topics, made in our own animation style.

- **Numbers (latest 60 Shorts):** median 497K views, 25 of 60 over 1M, top 30M ("The Ancient Jar That Warned an Empire"), then 15M ("The Job Nobody Wants in Japan"), 13M, 13M, 10M, 10M. Lowest 46K. Shorts run ~65 s.
- **Topics:** clever true-ish stories with a twist or loophole, mostly history and odd rules: an ancient earthquake-warning jar, Japan's gambling-law window, sailors' storm oil, the grave bell, a mirror that rigged a horse race, why cashiers win the lottery, a knight's loophole, levels of pirate cannonballs, what-if teleportation.
- **Look:** simple round-head stick-figure characters (dot eyes, small expressive mouths, thin line limbs, period hats and costumes) placed into rich, colourful 3D-rendered or painted environments (castles, rail yards, canyons), with fast camera moves, one or two words of caption at a time, and a narrator.
- **Code fit:** the characters are the easiest thing we could build (simpler than the orca). The sets are the heavy part: our flat style A sets, or Codex-generated background plates animated with parallax and camera moves (stills, not video).
- Frames: ~/studio/refs/ig/ricks_*.webm and ricks_*.jpg on the Spark.

## Owner note: couples niche (2026-11-01)

- The owner already covers relatable couples content a little on their Harry Potter AI shipping account, so this studio doesn't need to start there.
- For the future: a **cartoon-style** couples/relatable channel could reach a broader audience than a fandom-specific one (relatable to everyone, not just Harry Potter fans). Parked, not planned.
