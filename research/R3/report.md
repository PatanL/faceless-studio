# R3: "What if" niche teardown

Lane R3, 2026-11-01 (data pulled about 08:45 UTC). Covers Awaken, IFOLOGY and TikTok @man_ia_c. The ranked topic list is in `topics.json`.

## TL;DR

- **All three channels are brand new.** Their first uploads range from Oct 4 to Oct 20, 2026, so every number below is from a channel's first 2–4 weeks. Outliers are scored against each channel's own median.
- **Three proven formats, and each fits code-only production differently:**
  1. **"X disappeared for N seconds" vertical science shorts** (@man_ia_c). This is the biggest outlier engine in the niche: *electrons* 18.2M views (29x the channel median), *oxygen* 13.4M (21x), *neutrons* 5.1M (8x), *π = 3* 3.9M (6x), *iron* 2.7M (4x). Every video is 65–80 s, 9:16, with a countdown HUD, serif italic captions and an end card. TikTok labels the account's videos **"AI-generated"** (3D, likely generated). We can't copy that method, but the format itself (countdown, captions, 5–7 escalating beats, real-fact end card) is simple to build in code.
  2. **Humanity-scale thought experiments, 7–8 min long-form** (Awaken). *Can 2 People Really Restart Humanity?* got **4.2M views on a 14K-sub channel (23x median)**. Most of it is **flat 2D**: chalkboard diagrams, population trees, "YEAR 20 / +50 YEARS" stamps, data cards, a few stylised stick characters. This is the most code-friendly hit in the niche. The 3D "Last Guy on Earth" (Part B's recreation) made 401K.
  3. **"What IF You Could [power]?" long-form** (IFOLOGY). Stylised 3D characters, with **2D "science cutaways"** (white line stick figures on navy, speed lines, number callouts) making up roughly 25–35% of each video. Classic powers do best: *10x Faster* 868K (10x), *Stop Time* 636K (7.6x), *Shapeshift* 436K (5x). Pop-culture and IP topics underperform: *FNAF* 0.17x, *GTA 6 NPC* 0.34x, *LeBron* 0.22x, *Heaven/Hell* 0.4–0.5x.
- **Shorts cut from long-form flop on YouTube** for both IFOLOGY (median 15K) and Awaken (10K). Vertical-native shorts (man_ia_c) are a separate format with their own hook structure. Don't plan on YouTube Shorts cut-downs as the growth engine.
- **Recommendation:** the best first what-if pilot for the code-only studio is a **9:16 "N seconds" short** (topic #1 *friction* or #2 *calcium*). Make one countdown-HUD template that the whole series reuses, then a **long-form "What if you could breathe underwater?"** that reuses the B3 ocean explainer kit almost entirely.

## Method

- `yt-dlp` metadata (flat + full info.json) for every public upload on both YouTube channels (videos and shorts tabs) and all 22 TikToks. English auto-subs for all YouTube videos.
- Heavy work ran on the Spark (`~/studio/refs/R3/`, venv `~/studio/venvs/research`, CPU only). That covered 480p video-only copies of 7 YouTube videos and 6 TikToks, plus 20-frame contact sheets made with ffmpeg. Videos stay on the Spark. Only the JPG sheets and text transcripts came back to the Mac.
- Two IFOLOGY videos are members-only (*X-Ray Vision*, *Alter Reality*), so they have no stats.
- Outlier = views ÷ channel median (all public uploads, long and short). Views have only had 1–28 days to accumulate, so older uploads have an advantage. Where it matters I also give views per day.

## Channel 1: Awaken (YouTube @Afterimath, 14.1K subs)

**Uploads:** 4 long + 1 short, Oct 20–30. Median 184K views.

| Video | Views | x median | Length | Visual style |
|---|---|---|---|---|
| Can 2 People Really Restart Humanity? | 4.22M | 23x | 6:58 | Mostly flat 2D / 2.5D: chalkboard, genome diagrams on navy, portraits, island maps, data badges |
| What if You're The Last Guy on Earth? | 401K | 2.2x | 8:14 | Stylised 3D, many sets (Part B reference) |
| What if You Were The Last Girl On Earth? | 184K | 1.0x | 8:08 | Same 3D sequel |
| Could 8 Billion People Live in ONE City? | 23K | 0.12x | 7:07 | Flat 2D (phone notification, maps, globe, metro map, big-number cards) |
| Could 2 People Restart Humanity? (short) | 10K | 0.05x | 1:03 | cut-down |

**Title patterns:** "Can/Could [N] People [verb] [humanity-scale outcome]?" and "What if You're/You Were The Last [X] on Earth?". Sequel by gender flip (Last Guy → Last Girl) got half the views.

**Topic cluster:** humanity-scale demography and survival (population, reproduction, cities, gender). Dark-comedy tone.

**Script structure (from transcripts):** cold open in second person ("You wake up on a Monday and something is wrong…", "Tomorrow morning, your phone buzzes. So does everyone else's"). Then the stakes question ("Is there even room? What would we eat?"). Then numbered problems, each with a real study or record (Hutterite fertility, inbreeding load, Kowloon Walled City density). Then timeline jumps ("Year 20", "+75 years"). The payoff comes back to the opening characters. Dialogue lines are short ("So, it's just us?").

**Why 8 Billion in One City flopped despite the same style:** abstract "humanity" with no relatable pair of characters, and a "Could…" title without personal stakes. The hit had two strangers plus a ticking problem (inbreeding). This is my inference; n = 4.

**2D-feasibility:** high for the hit format. Almost every frame of *Restart Humanity* can be drawn as SVG and animated in Remotion: flat scenes, stick figures with black round heads, chalk lines, badges.

## Channel 2: IFOLOGY (YouTube @IFOLOGYFILMS, 48.6K subs)

**Uploads:** 30 long + 8 shorts, Oct 9–31 (about 1.5 long videos a day). Median 84K views overall, 134K for long-form.

**Outliers (long-form):** *What IF You Were 10x Faster?* 868K (10.3x), *Stop Time* 636K (7.6x), *Shapeshift* 436K (5.2x), *See 10 Seconds Into the Future* 336K (4x), *Teleport* 332K (4x), *100x Stronger* 258K (3.1x), *Indestructible* 251K (3x).
**Underperformers:** *Freddy Fazbear's Birthday* 15K, *LeBron James* 18K, *NPC in GTA 6* 29K, *Backrooms* 30K, *Heaven* 31K, *Zombie Apocalypse Part 3* 40K, *Hell* 43K. Zombie Parts 1→2→3 went 93K → 47K → 40K, so serialising long-form loses half the audience per part.

**Title pattern:** almost every title is "What IF You [Could/Were] [superpower or Nx multiplier]?", with "IF" in caps. Numeric multipliers do well (10x Faster, 100x Stronger, 1,000x Faster, Shrink 100X). "What IF You Were 10x Faster?" beat "1,000x Faster" by 5x, so the relatable number wins.

**Topic clusters (approximate medians):**

| Cluster | n | Median views |
|---|---|---|
| Classic superpowers (fly, teleport, stop time, invisibility, shapeshift, mind powers, copy powers) | 16 | ~200K |
| Nx physical multipliers (faster / stronger / shrink) | 5 | ~174K |
| Places / scenarios (zombie apocalypse x3, backrooms, heaven, hell) | 6 | ~42K |
| Pop culture / real people / IP (GTA 6, FNAF, LeBron, Charlie Kirk, President) | 5 | ~15K |

**Durations:** long-form grew from 3.5–6 min (first week) to 16–24 min (last week). Views per day: under 10 min 8.6K/day, **10–15 min 18.1K/day (best)**, 15–20 min 12.7K/day, 20+ min 14.8K/day. Raw views fall with length, but most of that is recency; views per day peak at 10–15 min. Shorts are 2–2.5 min cut-downs with a median of 15K, which doesn't work.

**Script structure:** a "you" cold open in an everyday setting (school, lunch, Saturday chores), the power triggers, a short dialogue gag. Then "So, what if you could X? Here's how it works", then real science with numbers (Usain Bolt 44 km/h, GPS clocks 38 µs/day, 330 billion cells/day). Then "you'd have a problem. Actually, three", then the escalating social story.

**Visual style:** stylised 3D (black round-headed characters, low-poly suburbs, warm lighting, heavy vignette). The **science cutaways are 2D**: white line stick figures on navy, speed lines, number callouts ("250 KM/H", "1 CALORIE / KG / KM"), grid maps, ramps. Those cutaways are directly buildable in our explainer kit.

## Channel 3: "What if?" (TikTok @man_ia_c)

**Uploads:** 22 posts, Oct 4–28. Median 625K views. Follower count not exposed by yt-dlp. Median engagement: 4.3% likes, 3.9 saves/1K, 2.1 shares/1K.

**Outliers:** *electrons disappeared for 5 s* 18.2M (29x, 2.1M likes), *oxygen disappeared for 5 s* 13.4M (21x), *neutrons* 5.1M (8x), *pop star 100x taller* 4.9M (7.8x), *π exactly 3 for 5 s* 3.9M (6.2x), *iron disappeared for 3 s* 2.7M (4.3x), *pop star 10 billion x taller* 2.1M (3.4x). **Below median:** disasters (tsunami cruise 607K, meteor at Burning Man 492K, NY wave 346K, earthquakes 357K), *Earth stopped spinning* 284K, *every atom lost a proton* 150K (a near-repeat of the proton-gain video), *plane crash* 234K (story/humour format, 65 s).

**Title / caption pattern:** "What if [fundamental thing] disappeared for [3/5] seconds?" followed by a long caption: "You're in/at [named real place]" → 3–5 escalating, number-heavy consequences → a real historical fact → a CTA question ("Which one next? 👇"). Hashtags are always `#whatif #pov #simulation #science`.

**Topic clusters:** (a) element or particle vanishes for N seconds: the hits; (b) physics constant changes (π = 3, gravity off, Earth stops): ~0.5–6x; (c) giant-human scale (pop star taller): 3–8x; (d) natural disasters: ~0.5–1x; (e) story/POV humour: ~0.4x.

**Durations:** fixed at **80 s** (19 of 22) with 65–78 s outliers. That just clears the TikTok Creator Rewards 1-minute minimum.

**Visual template (from contact sheets):** 9:16. A named real location (Central Park) at sunset in clean low-poly 3D. Serif title "What if **electrons** disappeared for 5 seconds?" with the keyword in colour. A **countdown HUD top-left** ("ELECTRONS RETURN IN 0:04.824", small caps subline "TIME SLOWED DOWN 11×"). Italic serif one-line captions in the lower third. Each beat is a style switch (wireframe city, star field, white-out, Earth from orbit). The end card is the title again on near-black with a small caps real-fact line. **TikTok shows an "AI-generated" label on every frame**, so this account uses AI video. Under BRIEF rule 4 we copy the *format*, not the method.

**2D-feasibility:** high, if we accept a stylised 2D look instead of 3D realism. The HUD, captions, title and end cards are pure typography. The beats are flat vector scenes (city silhouette, park, X-ray figure, orbit diagram) with particles and colour/shader transitions, all native to Remotion/Canvas. The most "wow" beats (wireframe city, white-out, Earth breaking apart) are easier in 2D than they look: line-art city plus glow plus particles.

## Cross-channel takeaways

1. **Hook = second-person + concrete place + instant consequence.** "You're in Central Park when…", "You wake up on a Monday and…", "You're at lunch and you knock over your juice…". All three channels open this way.
2. **Real numbers and one real historical fact per video** are what turns a fantasy into "science". Every top video has them (Rutherford 1919, Indiana π bill 1897, Hutterites, GPS clocks).
3. **Fundamental, universal premises beat IP and pop-culture premises** on every channel. They also avoid copyright and likeness problems (relevant to R5).
4. **Long-form sweet spot is about 7–15 min.** IFOLOGY's push to 20+ min isn't clearly paying off, and Awaken's hits are 7–8 min.
5. **Sequels and part 2/3 decay about 50% per step** (Zombie 1/2/3; Last Guy → Last Girl).
6. **Short cut-downs of long videos don't work on YouTube** (10–15K). Vertical-native shorts need their own template.

## Which topics work in 2D code style instead of 3D

| Reference video or format | 3D needed? | 2D code approach |
|---|---|---|
| Awaken *Restart Humanity* (4.2M) | No, it's already ~80% flat | Chalkboard + population tree + data badges + stick figures: explainer kit plus new "timeline stamp" and "population pyramid" components |
| Awaken *8 Billion in One City* | No | Maps, globe, metro-line SVG, big-number cards, phone notification (B4 phone component) |
| Awaken *Last Guy on Earth* | Yes as made; 2D possible with a different look | Too many sets and characters for a first 2D pass; leave to Part B |
| IFOLOGY science cutaways (all videos) | No | Line-art stick figures on navy, speed lines, number callouts: same family as the explainer kit |
| IFOLOGY story sections (suburb, school, stadium) | 3D as made | 2D is possible with flat backgrounds + puppet characters (B4 rig), but crowd and stadium scenes are expensive. Use story only for the cold open, then switch to explainer. |
| man_ia_c "N seconds" shorts | 3D/AI as made | Flat or line-art city + particles + HUD. Topics with **body / object** consequences (friction, calcium, metal → rubber) are much easier in 2D than **cosmic** ones (Earth exploding). |
| Disaster POVs (tsunami, meteor, wave) | Effectively yes (realism is the point) | Skip: weak performers anyway |

## Recommended what-if production plan (for S1 / a later P-lane)

1. **Template "N seconds" (9:16, 70–80 s):** title card (serif, keyword coloured) → countdown HUD that runs the whole video → 5–7 beats, each 8–12 s with one caption line → "returns" beat → end card with a real fact and "Which next? 👇". Storyboard fields: `element`, `seconds`, `location`, `beats[]{caption, scene, hud_subline}`, `end_fact`.
2. **Pilot topics:** #1 *friction* and #2 *calcium* from `topics.json`. They're original, body/object-level (so 2D-friendly), and in the strongest-performing format.
3. **Long-form follow-up:** #3 *breathe underwater* (reuses the B3 ocean kit) or #5 *born on the same day* (Awaken-style data story).
4. Avoid: IP/celebrity premises, disaster realism, multi-part series, and long-form cut-downs as Shorts.

## Top 20 topics (summary; full detail in topics.json)

| # | Topic | Format | Demand / 2D / Orig |
|---|---|---|---|
| 1 | What if friction disappeared for 5 seconds? | 9:16 short | 5 / 5 / 4 |
| 2 | What if calcium disappeared for 5 seconds? | 9:16 short | 5 / 5 / 5 |
| 3 | What if you could breathe underwater? | 16:9 long | 5 / 5 / 4 |
| 4 | What if light slowed to walking speed for 5 seconds? | 9:16 short | 4 / 5 / 5 |
| 5 | What if everyone on Earth was born on the same day? | 16:9 long | 4 / 5 / 5 |
| 6 | What if air became as thick as water for 5 seconds? | 9:16 short | 4 / 5 / 5 |
| 7 | What if you woke up at the bottom of the Mariana Trench? | 16:9 long | 4 / 5 / 4 |
| 8 | What if everyone on Earth got $1 million tomorrow? | 16:9 long | 4 / 5 / 3 |
| 9 | What if you could see every colour? | 16:9 long | 3 / 5 / 5 |
| 10 | What if you never needed to sleep again? | 16:9 long | 4 / 5 / 4 |
| 11 | What if the Sun disappeared for 5 seconds? | 9:16 short | 3 / 5 / 4 |
| 12 | What if every ant on Earth attacked at once? | 16:9 long | 4 / 5 / 4 |
| 13 | What if the internet went down for a whole year? | 16:9 long | 4 / 5 / 3 |
| 14 | What if the whole world used one time zone? | 16:9 long | 3 / 5 / 5 |
| 15 | What if you lived for 1,000 years? | 16:9 long | 4 / 5 / 3 |
| 16 | What if humans could photosynthesise? | 16:9 long | 3 / 5 / 5 |
| 17 | What if all metal turned to rubber for 5 seconds? | 9:16 short | 3 / 5 / 4 |
| 18 | What if Earth's magnetic field switched off? | 16:9 long | 3 / 5 / 4 |
| 19 | What if carbon disappeared for 5 seconds? | 9:16 short | 4 / 4 / 3 |
| 20 | Could 100 strangers on an island rebuild civilisation? | 16:9 long | 5 / 5 / 2 |

## Data and files

- `topics.json`: 20 ranked original what-if topics with hook, beats, evidence, kit reuse, scores and facts to verify.
- `raw/r3_videos.json`: 65 videos with views, likes, comments, saves, shares, duration, date, tags, description and URL.
- `raw/*_videos.json`, `raw/*_shorts.json`, `raw/awaken_ref.json`: raw yt-dlp listings.
- `sheets/<id>.jpg`: 20-frame contact sheets for 13 videos (study only).
- `transcripts/<id>.txt`: auto-sub transcripts with 30 s timestamps for 46 YouTube videos.
- Spark: `~/studio/refs/R3/` (info.json, VTTs, 480p video-only refs in `vid/`).

## Caveats

- Channels are 1–4 weeks old, so medians will move. Re-pull before committing to a series.
- man_ia_c follower count and Awaken/IFOLOGY impressions aren't available through yt-dlp.
- The TikTok scrape ran without browser impersonation and returned 22 posts. Pinned or older posts may be missing.
- Facts in `topics.json` are research leads, not verified script copy. S1 must fact-check them before recording.

## Per-channel upload tables (sorted by views)

#### Awaken (YouTube @Afterimath, 14.1K subs) — 5 public uploads, median 184K views

| # | Date | Title | Views | x median | Length | Likes % |
|---|---|---|---|---|---|---|
| 1 | 10-20 | [Can 2 People Really Restart Humanity?](https://www.youtube.com/watch?v=6oZ9fdM0n50) | 4.2M | 22.96 | 6:58 | 0.7 |
| 2 | 10-27 | [What if You’re The Last Guy on Earth?](https://www.youtube.com/watch?v=XbXiFizyGko) | 401K | 2.18 | 8:14 | 1.6 |
| 3 | 10-30 | [What if You Were The Last Girl On Earth?](https://www.youtube.com/watch?v=fFziW8Hgf84) | 184K | 1.00 | 8:08 | 1.5 |
| 4 | 10-25 | [Could 8 Billion People Live in ONE City?](https://www.youtube.com/watch?v=4OJqcmRRUYI) | 23K | 0.12 | 7:07 | 2.2 |
| 5 | 10-22 | [Could 2 People Restart Humanity? 😳 #shorts](https://www.youtube.com/watch?v=J17CZfV7u4k) | 10K | 0.05 | 1:03 | 2.7 |

#### IFOLOGY (YouTube @IFOLOGYFILMS, 48.6K subs) — 38 public uploads, median 84K views

| # | Date | Title | Views | x median | Length | Likes % |
|---|---|---|---|---|---|---|
| 1 | 10-15 | [What IF You Were 10x Faster?](https://www.youtube.com/watch?v=y300HjYnHPw) | 868K | 10.33 | 10:19 | 0.9 |
| 2 | 10-16 | [What IF You Could Stop Time?](https://www.youtube.com/watch?v=YznR5NmI3bc) | 636K | 7.57 | 10:10 | 1.3 |
| 3 | 10-21 | [What IF You Could Shapeshift?](https://www.youtube.com/watch?v=RxAhxw6Emec) | 436K | 5.19 | 22:06 | 1.1 |
| 4 | 10-22 | [What IF You Could See 10 Seconds Into the Future?](https://www.youtube.com/watch?v=Mfb3LHkFv5g) | 336K | 4.00 | 18:03 | 1.0 |
| 5 | 10-18 | [What IF You Could Teleport?](https://www.youtube.com/watch?v=0IckuPLNVF8) | 332K | 3.95 | 11:46 | 1.5 |
| 6 | 10-14 | [What IF You Were 100x Stronger?](https://www.youtube.com/watch?v=Vuc2Oyc82CI) | 258K | 3.07 | 5:28 | 1.3 |
| 7 | 10-19 | [What IF You Were Indestructible?](https://www.youtube.com/watch?v=g6wWbx4-Uy4) | 251K | 2.99 | 11:36 | 1.3 |
| 8 | 10-17 | [What IF You Could Control Gravity?](https://www.youtube.com/watch?v=qDM4u0o_4B0) | 232K | 2.76 | 18:53 | 1.5 |
| 9 | 10-10 | [What IF You Could Fly?](https://www.youtube.com/watch?v=Ltz6GOnpXvs) | 218K | 2.60 | 6:22 | 1.4 |
| 10 | 10-13 | [What IF You Could Shoot Webs?](https://www.youtube.com/watch?v=xRqMdfHKlYg) | 210K | 2.50 | 11:49 | 1.2 |
| 11 | 10-20 | [What IF You Could Copy Powers?](https://www.youtube.com/watch?v=kUY6LPPtM8U) | 203K | 2.42 | 10:29 | 1.4 |
| 12 | 10-23 | [What IF You Were 1,000x Faster?](https://www.youtube.com/watch?v=ynsBivrQ-J8) | 174K | 2.08 | 18:05 | 1.4 |
| 13 | 10-12 | [What If You Were 10x Stronger?](https://www.youtube.com/watch?v=OXjfIXOhLNY) | 172K | 2.05 | 3:29 | 1.3 |
| 14 | 10-09 | [What IF You Could Move Things With Your Mind?](https://www.youtube.com/watch?v=o8r3kpJv5gc) | 147K | 1.75 | 4:26 | 1.4 |
| 15 | 10-22 | [What IF You Could Turn Invisible?](https://www.youtube.com/watch?v=6jAsgf1muc8) | 138K | 1.64 | 19:13 | 1.7 |
| 16 | 10-24 | [What IF You Could Shrink 100X?](https://www.youtube.com/watch?v=fTquTRoe4eQ) | 131K | 1.56 | 19:53 | 1.3 |
| 17 | 10-25 | [What IF You Could Walk Through Walls?](https://www.youtube.com/watch?v=JAOcLUqdzvM) | 104K | 1.23 | 20:43 | 1.6 |
| 18 | 10-24 | [What IF You Were in a Zombie Apocalypse?](https://www.youtube.com/watch?v=Vqv9_Sr7OTU) | 93K | 1.11 | 17:13 | 1.2 |
| 19 | 10-28 | [What If You Could Control Minds](https://www.youtube.com/watch?v=PguPCPjptEg) | 85K | 1.01 | 24:17 | 1.8 |
| 20 | 10-11 | [What IF You Could Read Minds?](https://www.youtube.com/watch?v=77kcj19ianQ) | 83K | 0.99 | 5:37 | 1.7 |
| 21 | 10-27 | [What IF You Could Clone Yourself?](https://www.youtube.com/watch?v=yjL5KQAST4w) | 73K | 0.87 | 23:56 | 1.8 |
| 22 | 10-29 | [What IF You Could Control the Elements](https://www.youtube.com/watch?v=ZyXJlMgUJN0) | 65K | 0.78 | 24:19 | 1.9 |
| 23 | 10-24 | [What IF You Were in a Zombie Apocalypse? (Part 2)](https://www.youtube.com/watch?v=LJCoM5cxgnk) | 47K | 0.56 | 16:54 | 1.4 |
| 24 | 10-27 | [What IF You went to HELL?](https://www.youtube.com/watch?v=GBGCnpXH5Gs) | 43K | 0.51 | 23:44 | 1.7 |
| 25 | 10-25 | [What IF You Were in a Zombie Apocalypse? (Part 3)](https://www.youtube.com/watch?v=gfye-po-UpM) | 40K | 0.47 | 15:08 | 1.6 |
| 26 | 10-15 | [What IF You Were 10x Faster?](https://www.youtube.com/watch?v=B0CsQnzLw84) | 39K | 0.46 | 1:20 | 3.8 |
| 27 | 10-28 | [What IF You Went to Heaven?](https://www.youtube.com/watch?v=FchkaGla2a0) | 31K | 0.37 | 23:17 | 1.7 |
| 28 | 10-29 | [What IF You Woke Up in the Backrooms?](https://www.youtube.com/watch?v=RfHsNPoiLrM) | 30K | 0.35 | 16:23 | 3.8 |
| 29 | 10-18 | [What IF You Could Teleport?](https://www.youtube.com/watch?v=v9qHVzt-Yik) | 30K | 0.35 | 2:30 | 6.3 |
| 30 | 10-30 | [What IF You Were an NPC in GTA 6?](https://www.youtube.com/watch?v=FnpNcQV0W6M) | 29K | 0.34 | 12:57 | 2.1 |
| 31 | 10-26 | [What IF YOU were Lebron James?](https://www.youtube.com/watch?v=5z2TOOS1jEk) | 18K | 0.22 | 15:07 | 1.6 |
| 32 | 10-17 | [What IF You Could Control Gravity?](https://www.youtube.com/watch?v=Z6Vd7hjEcnM) | 17K | 0.20 | 2:17 | 4.5 |
| 33 | 10-23 | [What IF You Were Charlie Kirk? #shorts](https://www.youtube.com/watch?v=j7mPXFBihrk) | 15K | 0.17 | 2:03 | 3.7 |
| 34 | 10-31 | [What IF You Had Your Birthday at Freddy Fazbear's Pizza?](https://www.youtube.com/watch?v=_IvuARwjGO0) | 15K | 0.17 | 12:57 | 3.3 |
| 35 | 10-23 | [What IF You Could See 10 Seconds Into the Future?](https://www.youtube.com/watch?v=99sPdezP2MU) | 15K | 0.17 | 1:57 | 5.1 |
| 36 | 10-09 | [What IF Gravity Turned Off for 5 Seconds? #shorts #shortsfeed #viral #](https://www.youtube.com/watch?v=-8cgQIqgx74) | 13K | 0.15 | 2:01 | 2.6 |
| 37 | 10-24 | [What IF You Were the President of the United States? #shorts](https://www.youtube.com/watch?v=pdQHnarYpT8) | 12K | 0.15 | 1:54 | 3.4 |
| 38 | 10-12 | [What IF You Could Shoot Webs? #shorts](https://www.youtube.com/watch?v=EmRLqIZXseg) | 11K | 0.13 | 2:57 | 2.5 |

#### "What if?" (TikTok @man_ia_c) — 22 public uploads, median 625K views

| # | Date | Title | Views | x median | Length | Likes % |
|---|---|---|---|---|---|---|
| 1 | 10-06 | [What if electrons disappeared for 5 seconds?](https://www.tiktok.com/@man_ia_c/video/7693494009494342945) | 18.2M | 29.13 | 1:20 | 11.5 |
| 2 | 10-05 | [What if oxygen disappeared for 5 seconds?](https://www.tiktok.com/@man_ia_c/video/7693305573487562016) | 13.4M | 21.45 | 1:20 | 6.2 |
| 3 | 10-06 | [What if neutrons disappeared for 5 seconds?](https://www.tiktok.com/@man_ia_c/video/7693617402180881697) | 5.1M | 8.16 | 1:20 | 7.5 |
| 4 | 10-07 | [What if a pop star was 100 times taller?](https://www.tiktok.com/@man_ia_c/video/7694025665993100576) | 4.9M | 7.84 | 1:20 | 9.0 |
| 5 | 10-13 | [What if π was exactly 3 for 5 seconds?](https://www.tiktok.com/@man_ia_c/video/7696143265405488416) | 3.9M | 6.24 | 1:20 | 6.8 |
| 6 | 10-07 | [What if iron disappeared for 3 seconds?](https://www.tiktok.com/@man_ia_c/video/7693888660256722208) | 2.7M | 4.32 | 1:20 | 4.8 |
| 7 | 10-26 | [What if a pop star grew 10 billion times taller?](https://www.tiktok.com/@man_ia_c/video/7700921504350981408) | 2.1M | 3.36 | 1:05 | 8.6 |
| 8 | 10-09 | [What if every atom gained a proton for 3 seconds?](https://www.tiktok.com/@man_ia_c/video/7694569549122768161) | 1.2M | 1.92 | 1:20 | 6.0 |
| 9 | 10-15 | [What if TikTok didn't exist for 5 seconds?](https://www.tiktok.com/@man_ia_c/video/7696887068588313889) | 741K | 1.19 | 1:20 | 7.4 |
| 10 | 10-06 | [What if Earth fell into a black hole?](https://www.tiktok.com/@man_ia_c/video/7693428628633193760) | 650K | 1.04 | 1:20 | 2.8 |
| 11 | 10-05 | [What if gravity stopped for 60 seconds?](https://www.tiktok.com/@man_ia_c/video/7693151375273757984) | 642K | 1.03 | 1:20 | 2.4 |
| 12 | 10-05 | [What if a tsunami hit your cruise ship?](https://www.tiktok.com/@man_ia_c/video/7693094760537476384) | 607K | 0.97 | 1:20 | 2.5 |
| 13 | 10-05 | [What if gravity turned off?](https://www.tiktok.com/@man_ia_c/video/7693276132128328992) | 540K | 0.86 | 1:20 | 2.7 |
| 14 | 10-05 | [What if a meteor hit Burning Man?](https://www.tiktok.com/@man_ia_c/video/7693217592646962464) | 492K | 0.79 | 1:20 | 1.8 |
| 15 | 10-18 | [What if Earth left the universe for 5 seconds?](https://www.tiktok.com/@man_ia_c/video/7698033834897509664) | 429K | 0.69 | 1:20 | 4.5 |
| 16 | 10-08 | [What if hydrogen disappeared for 3 seconds?](https://www.tiktok.com/@man_ia_c/video/7694297218425113888) | 419K | 0.67 | 1:20 | 3.1 |
| 17 | 10-10 | [What if the earthquakes kept getting stronger?](https://www.tiktok.com/@man_ia_c/video/7695016975038303521) | 357K | 0.57 | 1:20 | 3.3 |
| 18 | 10-05 | [What if a gigantic wave hit new york?](https://www.tiktok.com/@man_ia_c/video/7693054149474258209) | 346K | 0.55 | 1:18 | 0.9 |
| 19 | 10-04 | [It's 3:14 AM. Would you press YES?](https://www.tiktok.com/@man_ia_c/video/7692834057566080289) | 294K | 0.47 | 1:12 | 1.6 |
| 20 | 10-10 | [What if the Earth stopped spinning?](https://www.tiktok.com/@man_ia_c/video/7695117668327771424) | 284K | 0.46 | 1:20 | 4.1 |
| 21 | 10-28 | [What if I survived a plane crash?](https://www.tiktok.com/@man_ia_c/video/7701810977125256480) | 234K | 0.37 | 1:05 | 7.7 |
| 22 | 10-17 | [What if every atom lost a proton for 5 seconds?](https://www.tiktok.com/@man_ia_c/video/7697719022544063776) | 150K | 0.24 | 1:20 | 3.2 |
