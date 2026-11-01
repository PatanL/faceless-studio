# Zack D. Films imitators: who copies the format and how often it works

Internal research, pulled 2026-11-01 (metadata only, Spark CPU). The goal is to learn base rates for the format. Nothing here (scripts, characters, visuals) is for reuse. Raw data: `imitators.json` (same folder). Spark copies: `~/studio/refs/zackd/imitators/`.

## Verdict: how likely a new channel in this format reaches a 10K median

**About 1 in 10, and lower in the core "your body / what if you..." niche.**

- Sample: 39 YouTube channels in the format that are less than 6 months old (first upload after 2026-05-01).
  - **Median of their per-channel median views: 1.2K** (IQR 760 to 1.8K).
  - **5 of 39 (13%) have a median of 10K or more.**
    - Counting only channels with 10 or more uploads: 4 of 31 (13%).
    - Counting only channels with 30 or more uploads: 3 of 14 (21%).
- The true rate is probably **5-10%**. The sample over-counts successes:
  - Channels were found through YouTube hashtag pages, and those pages rank videos by views.
  - Dead channels that never got a view, and deleted channels, can't be seen.
- **The usual outcome is about a 1K median, followed by quitting.** Of 31 channels at least 60 days old, 19 have not posted in 30 days. 16 of those 19 stalled below a 10K median.
- **Posting more doesn't fix a weak start.** 19 channels have 30 or more Shorts and still sit below 10K, for example:
  - UnlockedAILab: 92 uploads, median 143.
  - TheInnerRise06: 94 uploads, median 1.0K.
  - Narracrest: 93 uploads, median 1.5K.
  - PeachBuzz369: 284 uploads, median 5K.
  - The format either works within the first ~20-50 uploads or it doesn't.
- **The sub-niche matters more than anything else we measured** (new channels, under 6 months):

| Sub-niche group | New channels | Median of medians | Reached 10K |
|---|---|---|---|
| Body / "what happens if you..." (Zack's core) | 22 | 1.1K | 1 (FixmyReading) |
| Survival / what-if | 6 | 0.8K | 0 |
| How-it-works / science | 5 | 1.4K | 0 |
| History / military / pop-culture spin-offs | 6 | 23K | 4 (ThePostulator 78K, shwededfilms 160K, Ctrlzfilms01 35K, 3DDose 12K on 6 uploads) |

- **Hand-built CG looks better than AI video in this sample.** This compares channels by how their thumbnails look:
  - CG or low-poly renders (built in a 3D tool): 5 of 9 YouTube channels at 10K or more.
  - AI-generated "Pixar-like" or photoreal video: 6 of 47.
  - Most of the 2026 entrants are AI-video channels. Their look is now generic, and they sit at about a 1K median.
  - Caveat: style and niche overlap, and the CG group is small, so treat this as a hint.
  - For us (code-rendered, no AI video), a distinct, consistent rendered look is a small edge, not a guarantee.
- **Saturation: yes for the body niche; mixed overall.**

| Start cohort (YouTube) | n | Median of medians | Median 10K or more | Still active |
|---|---|---|---|---|
| 2024 | 3 | 5.0K | 1/3 | 1/3 |
| 2025 H1 | 4 | 10.9K | 2/4 | 1/4 |
| 2025 H2 | 10 | 1.35K | 2/10 | 1/10 |
| 2026 H1 | 9 | 1.3K | 3/9 | 5/9 |
| 2026 Jul-Oct | 33 | 1.2K | 3/33 | 31/33 |

  - Read with care:
    - Older cohorts are survivors (failures got deleted or were never surfaced).
    - The pattern is still clear: channels that started in 2024 to mid-2025 (Zeck Felms 1.9M; How_Tales 16K; SenseFactsIQ 17K in Bengali) did far better than the late-2025 and 2026 wave. The new wave sits at about 1.2K whatever the channel's age.
    - Within channels, the trend is flat. Of 28 channels with 30 or more uploads, 11 rose (latest 20 vs first 20 Shorts) and 9 fell.
- **The exceptions are not on YouTube's body niche.**
  - TikTok, both found by R4 because they were already viral (survivors):
    - meanwhileanimations, created 2026-10-04, median 1.1M on 13 posts (what-if society simulations).
    - polystoriesdaily, created 2026-10-22, median 302K on 8 posts (what-if comedy).
  - Instagram: bob.figures.it.out, median 1.2M (relationship comedy).
  - The pattern among these: a **recurring cast or premise and comedy, not facts**.
  - We found **no YouTube imitator in relationship comedy**. The "Bob Figures It Out" YouTube channel (24 subs) is an unrelated live-action channel.

**Implication for the studio:**
- Budget for the base case: about 1K median after 30-50 uploads.
- Do not enter the crowded body/anatomy lane with a lookalike.
- The open lanes are:
  - (a) A distinct, code-rendered look.
  - (b) A sub-niche the AI-video wave hasn't filled: history/military, pop-culture what-if, or character comedy in the bob/meanwhile style.
  - (c) Cross-posting to TikTok and Reels, where the new viral accounts actually are.
- Set a kill/pivot checkpoint at ~30 uploads: if the median is under 3K, change niche, not volume.

## Method

1. **How channels were found (YouTube):**
   - Pulled the Shorts tab of hashtag pages `#zackdfilms #zackdfilmsstyle #zackd #zackdfilm #howitworks` (400 each): 1,277 unique Shorts.
   - Mapped them to 581 channels with YouTube oEmbed.
   - Ran 20 more `ytsearch60` queries (mostly long-form noise, reaction channels and "how to make Zack D style with AI" tutorials).
   - Kept 68 candidates whose titles fit the format, mixing big and tiny channels on purpose.
2. **Stats per channel:**
   - `yt-dlp --flat-playlist -J` on the `/shorts` tab (cap 2,500) and the `/videos` tab gave every upload's view count and the subscriber count.
   - **Median** = median views of all Shorts except the newest 3 (they are still accruing views).
   - **% >=10K** uses the same set.
   - yt-dlp full extraction is bot-walled on the Spark. So upload dates were scraped from the `uploadDate` field of the watch page for about 12 evenly spaced Shorts per channel, plus the oldest and newest long video.
   - **First upload** = the earliest dated item. **Age** is counted to 2026-11-01.
3. **Format check:**
   - Built a contact sheet of 5 thumbnails per channel (top 2 by views plus the latest 3) and looked at each one.
   - Excluded 8 non-format channels, plus Zack D. Films itself as the reference (`excluded` in the JSON):
     - Archival-photo fact cards: 10secondshistory, UnseenFacts.
     - Face-cam channels: Oddrender2007, Laytharoni7, Isley.
     - Live-action clips: Voiceofvetri, nickexplainer.
     - The wrong "Bob Figures It Out".
   - `render_style` is a visual judgment from those thumbnails: `cg-3d`, `cg-lowpoly`, `ai-3d`, `ai-photoreal` or `mixed`.
4. **TikTok:**
   - yt-dlp's TikTok tag pages are broken, and most user pages fail ("Unable to extract secondary user ID").
   - Only zeckfelms (a partial list of 93 posts ending 2026-03) and the two R4 accounts are included.
   - Account creation dates are decoded from the TikTok user ID (`id >> 32` = unix time).
5. **Instagram:** bob.figures.it.out numbers come from `research/R4/report.md` (latest 12 reels, logged out). It is not pollable by yt-dlp.

**Known biases:**
- Hashtag-page discovery favours channels with views, and hashtag users are a subset of imitators.
- Deleted channels are invisible.
- Channels with fewer than 10 uploads have noisy medians.
- Channel "age" is the age of the oldest *visible* upload. 3D_Health_Animation02 has 295K subs but only Sept-2026 uploads, so it is a repurposed channel and its subs were not earned by this format. wooyeawoo is a 2021 channel that pivoted.
- Zack D. Films and Zeck Felms subs and medians are included only as reference ceilings.

## Reference points (not imitators or not in the base rate)

- **Zack D. Films** (@zackdfilms): 29.5M subs. Median 12M on the latest ~2,500 Shorts, all at 10K or more. The original.
- **Zeck Felms** (YouTube, UCPRmoN_Oq-20XBTQfagEOJA): started 2025-02. 1.26M subs, median 1.9M, 310 Shorts.
  - A parody that Zack D. Films collaborated with ("How Zeck Felms Was Born (feat Zack D. Films)").
  - It got the original's endorsement, so it is not a replicable path. It is included in the table but sits in the 2025-H1 cohort, not the new-channel base rate.
- The "imitator economy" around the format is large:
  - Reaction channels ("I Tested Every Zack D. Films Video", 1-8M views).
  - "WTF is this Zack D Films clone" roundups (C Daily, Luvhilal).
  - Many "make Zack D style Shorts with AI" tutorials. These explain the 2026 flood of AI-video entrants.

## All channels (sorted by age; YT = YouTube, TT = TikTok, IG = Instagram)

Uploads S/L = Shorts / long videos. Median = median views per Short (newest 3 excluded). Active 30d = posted in the last 30 days. TikTok follower counts were not available from the listing.

| # | Platform | Channel | Subs | First upload | Age (d) | Uploads S/L | Median | % >=10K | Max | Active 30d | Sub-niche | Style |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | YT | @VividVorTex-p4q | 5 | 2026-10-27 | 5 | 3/0 | 79 | 0.0 | 3.1K | y | myths / survival | ai-3d |
| 2 | YT | @CuriousCore.12 | 5 | 2026-10-24 | 8 | 8/0 | 94 | 0.0 | 1.7K | y | body | ai-3d |
| 3 | YT | @NLRFILMS | 6 | 2026-10-23 | 9 | 1/1 | 1.5K | 0.0 | 1.5K | y | body | ai-3d |
| 4 | TT | @polystoriesdaily | ? | 2026-10-24 | 10 | 8/0 | 302.1K | 87.5 | 1.7M | y | what-if comedy (low-poly) | cg-lowpoly |
| 5 | YT | @Twistory-YT-1 | 37 | 2026-10-21 | 11 | 10/0 | 3.3K | 28.6 | 13.0K | y | survival / physics myths | cg-3d |
| 6 | YT | @GoldenApple4845 | 6 | 2026-10-20 | 12 | 6/0 | 1.2K | 0.0 | 2.1K | y | engineering how-it-works | ai-3d |
| 7 | YT | @masadfilms | 218 | 2026-10-19 | 13 | 17/0 | 2.1K | 28.6 | 33.0K | y | engineering / odd builds | cg-lowpoly |
| 8 | YT | @zyphexplained | 13 | 2026-10-16 | 16 | 12/0 | 757 | 0.0 | 1.8K | y | body / what-if | ai-3d |
| 9 | YT | @ThePostulator | 6.7K | 2026-10-11 | 21 | 22/0 | 78.0K | 100.0 | 1.5M | y | pop-culture trivia (game characters) | cg-3d |
| 10 | YT | @RiskXplained-y6n | 65 | 2026-10-08 | 24 | 19/0 | 1.8K | 0.0 | 7.8K | y | survival / what-if | ai-3d |
| 11 | TT | @meanwhileanimations | ? | 2026-10-04 | 28 | 13/0 | 1.1M | 100.0 | 33.1M | y | what-if society simulations | cg-3d |
| 12 | YT | @IKhlakFilms | 285 | 2026-10-03 | 29 | 31/0 | 2.9K | 32.1 | 324.0K | y | body / how-it-works | ai-3d |
| 13 | YT | @3DDose | 63 | 2026-10-02 | 30 | 6/0 | 12.2K | 50.0 | 30.0K | y | military/weapons what-if | cg-3d |
| 14 | YT | @SoldierAnimations.Official | 22 | 2026-10-01 | 31 | 3/0 | 7.5K | 0.0 | 7.6K | y | war history | ai-3d |
| 15 | YT | @toonblisscar | 5 | 2026-09-30 | 32 | 12/0 | 224 | 0.0 | 1.4K | y | body / what-if | ai-3d |
| 16 | YT | @AnimaLogicexplains | 47 | 2026-09-29 | 33 | 25/0 | 850 | 4.5 | 11.0K | y | body / everyday tech | ai-3d |
| 17 | YT | @HowItWorks-k9d | 20 | 2026-09-28 | 34 | 12/0 | 1.7K | 0.0 | 3.9K | y | how-it-works mechanisms | ai-3d |
| 18 | YT | @UnknownFiles1819 | 11 | 2026-09-28 | 34 | 11/0 | 1.1K | 0.0 | 1.3K | y | body | ai-3d |
| 19 | YT | @littlezackd | 44 | 2026-09-26 | 36 | 23/0 | 926 | 0.0 | 1.7K | y | body | ai-3d |
| 20 | YT | @CurioFrame-official | 526 | 2026-09-23 | 39 | 56/0 | 1.6K | 3.8 | 130.0K | y | body (medical) | ai-3d |
| 21 | YT | @MedToonLabTV | 2 | 2026-09-22 | 40 | 11/0 | 16 | 0.0 | 1.0K | y | body | ai-3d |
| 22 | YT | @MB.Films-a | 3 | 2026-09-20 | 42 | 16/0 | 380 | 0.0 | 1.6K | n | body / memes (mixed) | mixed |
| 23 | YT | @inside-everything3D | 78 | 2026-09-18 | 44 | 19/0 | 1.4K | 0.0 | 2.9K | y | body | ai-3d |
| 24 | YT | @AlvexRfilms | 16 | 2026-09-17 | 45 | 8/4 | 1.3K | 0.0 | 1.4K | y | what-if / body | ai-3d |
| 25 | YT | @FactLab-h9b | 35 | 2026-09-14 | 48 | 31/0 | 1.2K | 0.0 | 4.1K | y | animals / body | ai-3d |
| 26 | YT | @vickydfilms | 118 | 2026-09-13 | 49 | 70/1 | 661 | 0.0 | 2.5K | y | survival / body | ai-photoreal |
| 27 | YT | @viraldfilms | 104 | 2026-09-13 | 49 | 42/6 | 515 | 0.0 | 4.7K | y | survival / body stories | ai-photoreal |
| 28 | YT | @3D_Health_Animation02 | 295.0K | 2026-09-07 | 55 | 62/0 | 533 | 0.0 | 6.5K | y | body (anatomy) | ai-3d |
| 29 | YT | @FixmyReading | 1.9K | 2026-09-03 | 59 | 52/4 | 25.0K | 79.6 | 89.0K | y | what-if / body | ai-3d |
| 30 | YT | @TheZyroVault | 27 | 2026-09-03 | 59 | 16/0 | 928 | 0.0 | 2.4K | y | what-if survival | ai-photoreal |
| 31 | YT | @Inscopia | 31 | 2026-09-02 | 60 | 38/2 | 935 | 0.0 | 5.1K | y | body / what-if | ai-3d |
| 32 | YT | @TheInnerRise06 | 209 | 2026-09-02 | 60 | 94/0 | 1.0K | 3.3 | 29.0K | y | history (ancient daily life) | ai-3d |
| 33 | YT | @AnatoVerse3D-x2b | 543 | 2026-08-21 | 72 | 53/1 | 858 | 4.0 | 267.0K | y | animals/nature how-it-works | ai-3d |
| 34 | YT | @ShadeTheory-Official | 26 | 2026-08-18 | 75 | 14/0 | 1.3K | 0.0 | 2.0K | y | body / mixed anime | mixed |
| 35 | YT | @mato1956usa | 22 | 2026-07-26 | 98 | 11/2 | 1.2K | 0.0 | 6.3K | n | body / animals | ai-3d |
| 36 | YT | @Curious3D-712 | 360 | 2026-06-23 | 131 | 41/0 | 1.4K | 7.9 | 60.0K | y | how-it-works mechanisms | ai-3d |
| 37 | YT | @Ctrlzfilms01 | 16.1K | 2026-06-17 | 137 | 51/1 | 34.5K | 87.5 | 11.0M | y | pop-culture what-if (superheroes/anime) | ai-3d |
| 38 | YT | @Felixgsxw | 30 | 2026-06-12 | 142 | 25/0 | 516 | 0.0 | 1.5K | y | body (photoreal AI presenter) | ai-photoreal |
| 39 | YT | @ishxfilms | 80 | 2026-06-07 | 147 | 32/2 | 1.1K | 0.0 | 5.3K | n | body / earth science | ai-3d |
| 40 | YT | @shwededfilms | 43.1K | 2026-05-17 | 168 | 49/1 | 159.5K | 82.6 | 4.3M | y | history / pop-culture | cg-3d |
| 41 | YT | @TheBioCircuit | 41 | 2026-05-10 | 175 | 9/0 | 1.1K | 0.0 | 2.7K | n | body | ai-3d |
| 42 | YT | @UnlockedAILab | 55 | 2026-04-28 | 187 | 92/0 | 143 | 2.2 | 36.0K | n | body | ai-3d |
| 43 | YT | @PixelUS0 | 414.0K | 2026-04-22 | 193 | 72/0 | 30.0K | 92.8 | 9.2M | y | religion / history mysteries | cg-3d |
| 44 | YT | @WeirdlyExplained_YT | 30 | 2026-01-31 | 274 | 27/1 | 1.3K | 0.0 | 3.0K | n | survival / body | ai-3d |
| 45 | YT | @FactMorph-h3e | 73 | 2025-12-22 | 314 | 27/0 | 1.1K | 0.0 | 2.1K | n | science facts | ai-3d |
| 46 | YT | @jcsmicroverse | 129 | 2025-12-22 | 314 | 86/0 | 1.2K | 2.4 | 18.0K | n | body (micro) | ai-3d |
| 47 | YT | @Insane3D-00 | 35 | 2025-12-09 | 327 | 10/0 | 1.0K | 0.0 | 2.1K | n | body | ai-3d |
| 48 | YT | @Narracrest | 431 | 2025-11-30 | 336 | 93/4 | 1.5K | 0.0 | 9.3K | n | body / what-if comedy | ai-3d |
| 49 | YT | @giaimakhoahoc1 | 83.5K | 2025-11-25 | 341 | 434/0 | 29.0K | 86.8 | 3.8M | y | science / body | ai-3d |
| 50 | YT | @ThoughtSparkFilms | 218 | 2025-11-13 | 353 | 5/0 | 1.2K | 40.0 | 27.0K | n | physics what-if | ai-3d |
| 51 | YT | @KineVerse5 | 73 | 2025-10-21 | 376 | 53/0 | 1.1K | 0.0 | 3.2K | n | science facts | ai-3d |
| 52 | YT | @WaterWhiteee | 166 | 2025-10-10 | 387 | 29/0 | 7.0K | 46.2 | 32.0K | n | body / military (mixed) | ai-3d |
| 53 | YT | @VoidFiles-L | 18.1K | 2025-09-14 | 413 | 38/0 | 4.3K | 40.0 | 1.6M | n | body / evolution | cg-3d |
| 54 | YT | @NoahFilms375 | 324 | 2025-08-10 | 448 | 56/0 | 11.0K | 52.8 | 35.0K | n | weapons / objects history | ai-3d |
| 55 | YT | @How_Tales | 5.0K | 2025-05-26 | 524 | 58/2 | 16.0K | 61.8 | 1.2M | n | what-if / body / sports | ai-3d |
| 56 | YT | @scire_arts4628 | 44 | 2025-05-16 | 534 | 16/19 | 1.8K | 7.7 | 12.0K | n | mixed / body | ai-3d |
| 57 | YT | @Darkdmatter | 543 | 2025-03-15 | 596 | 66/0 | 5.7K | 41.3 | 88.0K | n | what-if physics/body | cg-3d |
| 58 | YT | Zeck Felms | 1.3M | 2025-02-11 | 628 | 310/15 | 1.9M | 100.0 | 97.0M | y | parody how-it-works (Zeck Felms) | cg-lowpoly |
| 59 | TT | @zeckfelms | ? | 2025-02-11 | 631 | 93/0 | 1.9M | 100.0 | 34.9M | n | parody how-it-works (Zeck Felms TikTok) | cg-lowpoly |
| 60 | YT | @SenseFactsIQ | 75.8K | 2024-09-16 | 776 | 64/0 | 17.0K | 65.6 | 2.2M | n | body / what-if | ai-3d |
| 61 | YT | @PeachBuzz369 | 45.3K | 2024-09-13 | 779 | 284/29 | 5.0K | 37.4 | 3.6M | y | military tech | ai-3d |
| 62 | YT | @wooyeawoo | 386.0K | 2021-02-21 | 2079 | 447/8 | 1.5K | 16.2 | 97.0M | n | mixed (repurposed 2021 channel) | mixed |
| 63 | IG | bob.figures.it.out | 155.0K | ? | ? | 12/0 | 1.2M | 100.0 | 7.3M | y | relationship comedy (Bob + girlfriend) | cg-lowpoly |
