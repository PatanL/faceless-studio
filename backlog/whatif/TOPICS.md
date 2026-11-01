# What-if backlog: topic selection

Niche: "what if" scenarios in a flat 2D, code-only style. Each one makes a single impossible change to a familiar world, then escalates the consequences with counters, maps and graphs.
Mix: **8 Shorts (60–90 s, 9:16, vertical-native)** + **2 long-form (6–8 min, 16:9)**.
Selected 2026-11-01 at about 09:05 UTC. View counts come from yt-dlp metadata read today.

## Evidence used

- `research/R3/report.md` + `research/R3/topics.json`: teardown of Awaken, IFOLOGY and TikTok @man_ia_c, with 20 ranked topics.
- `research/library/candidates-whatif.json`: outlier scores against channel medians, including the adjacent channels ConChaser, Oddly Elsewhere and OminiAM.
- `backlog/whatif/evidence/*.txt`: 23 earlier `ytsearch15` topic checks, plus the "What If" channel's recent long-form and Shorts tabs.
- **New checks for this file** (Spark, `~/.local/bin/yt-dlp --flat-playlist`): 35 `ytsearch15/20` queries (20 topic queries and 15 Shorts-angle queries) and a re-pull of @man_ia_c's TikTok listing. That account has posted nothing new since Oct 28, so R3's numbers still hold. Raw results are in `backlog/whatif/evidence/checks-0903/` (Spark: `~/studio/refs/topics_whatif/`).
- `episodes/` and `stories/` don't exist yet, so nothing here duplicates existing work. `research/corpus/whatif/` isn't built yet either (see writer notes).

**What the checks say:**
1. The "X disappeared for N seconds" Short is the outlier engine. @man_ia_c's medians are 625K, with *electrons* at 18.2M (29x) and *oxygen* at 13.4M (21x). Body- and object-level consequences beat cosmic and disaster ones on that account: *Earth stopped spinning* got 0.46x and disasters 0.5–1x.
2. Shorts cut down from long-form fail. The "What If" channel's Shorts tab has a median of about 40K against long-form videos of 1M+. IFOLOGY's Shorts get about 15K. Every Short below is a vertical-native script.
3. The obvious premises are saturated: oxygen for 5 s, gravity off, Earth stops spinning, everyone jumps at once. Vsauce, What If, Peekaboo Kidz and dozens of 100-view clones all cover them. Searches for friction, calcium and "light at walking speed" turn up proven demand from adjacent videos but **no strong vertical version**.
4. Long-form: humanity-scale data stories (Awaken *Restart Humanity* at 4.2M, 23x) and classic "what if YOU could" powers (IFOLOGY medians around 200K, *10x Faster* 868K) both work. IP and celebrity premises fail (0.17–0.34x).

## 14 candidates

| # | Slug | Format | Premise (one line) | Key evidence | 2D cost | Verdict |
|---|---|---|---|---|---|---|
| 1 | whatif-friction-off-5-seconds | Short | Friction switches off on a city street: knots untie, nails slide out, clothes unravel, everyone slides downhill | What If "No Friction for 1 Minute?" 1.05M; Action Lab "Strange Limit of Frictionless Motion" 1.46M; best vertical competitor 8.4K | low | **PICK** |
| 2 | whatif-calcium-gone-5-seconds | Short | Every skeleton goes soft, and so do marble, limestone, chalk cliffs and concrete | What If "Didn't Have Bones… Human JELLYFISH" 4.42M; @man_ia_c *iron* 2.7M (4.3x); no direct "calcium" video found | low | **PICK** |
| 3 | whatif-light-walking-speed | Short | Light now moves at 1.4 m/s, so everything you see is seconds old and colours shift as you walk | Worlds In Motion "What If Light Was Really Slow?" 4.26M; Airplane Mode speed-of-light 36.4M (149 s); @man_ia_c *π = 3* 3.9M (6.2x) | low | **PICK** |
| 4 | whatif-sun-gone-5-seconds | Short | The Sun vanishes for 5 s and nothing happens for 8 min 20 s. Then a 5-second shadow sweeps across the solar system | Vsauce "What If The Sun Disappeared?" 20.9M; SolarBalls 7.77M (82 s); BRIGHT SIDE 7.78M; Shorts competitors under 1K | low | **PICK** |
| 5 | whatif-moon-10x-closer | Short | The Moon at 38,400 km: 10x wider in the sky, 1,000x the tides, a day spent watching the sea leave | yeti dynamics "Moon at the same distance as the ISS" 5.38M (102 s); yeti "Moon replaced with planets" 87.9M (103 s); StarTalk "20 Times Closer" 765K | very low | **PICK** |
| 6 | whatif-you-100x-taller | Short | You wake up 170 m tall. The square-cube law says your legs are already breaking | @man_ia_c "pop star 100 times taller" 4.9M (7.8x) + "10 billion times" 2.1M (3.4x); What If "Grew 1cm Every Second" Short 3.3M; Infographics "1000 feet Tall" 1.41M | low | **PICK** |
| 7 | whatif-oceans-turn-fresh | Short | All the salt leaves the sea overnight. Reefs die of osmosis, the Gulf Stream stalls, Europe freezes | What If "All the Sea Water… Fresh Water Overnight?" 5.93M; Ridddle 4.33M; AumSum 2.17M | very low (ocean kit) | **PICK** |
| 8 | whatif-earth-had-rings | Short | Earth gets Saturn-style rings. The ring shadow drops a permanent winter on one latitude, and satellites become impossible | What If "Rings Like Saturn Tomorrow?" 5.04M; AumSum 4.11M; Joe Scott 2.78M; Peekaboo 2.64M; SolarBalls trash rings 2.15M | very low | **PICK** |
| 9 | whatif-sodium-gone-3-seconds | Short | Every nerve signal stops for 3 s: 8 billion people drop at once, then wake up | AumSum "What if Salt Disappeared?" 1.50M; What If "No Salt in the World?" 724K | low | reserve: its "everyone collapses" beat is too close to #2, and demand is weaker |
| 10 | whatif-dna-gone-5-seconds | Short | Your DNA vanishes and you feel fine. Here is how long "fine" lasts | xkcd's What If? "How long would you survive with no DNA?" 2.57M; What If "DNA Suddenly Disappeared?" 375K | med (cell-level visuals) | reserve: hard to make concrete in 80 s, and xkcd owns the angle |
| 11 | whatif-everyone-born-same-day | Long | 8 billion babies, one birthday. Each life stage then hits the whole world at once: schools, jobs, retirement, the last survivor | Awaken "Can 2 People Really Restart Humanity?" 4.22M (23x); RealLifeLore "Every Human Ever Born Came Back to Life" 6.49M; Infographics "No Babies Born for a Year" 887K; no direct competitor | low (charts) | **PICK** |
| 12 | whatif-breathe-underwater | Long | You fall off a ferry mid-Pacific, take a panicked breath, and you're fine. Then pressure, cold, the dark and the neighbours | Peekaboo "Could Breathe Underwater?" 2.35M; What If 1.59M; Ifsphere 250K; IFOLOGY classic-power median ~200K; Depth Theory ocean explainer 2.28M on 6K subs | very low (B3 ocean kit) | **PICK** |
| 13 | whatif-never-need-sleep | Long | You stop needing sleep: 2,900 extra hours a year, and what the world does with a species that never switches off | TED-Ed "if you didn't sleep" 15.0M; Peekaboo "Stopped SLEEPING" 12.5M; Infographics 806K; What If "No Longer Needed Sleep" 399K | low | reserve: the top videos are about sleep *deprivation*, the "superpower" version proves weaker (399K), and there's no ready-made counter/graph spine |
| 14 | whatif-humans-photosynthesize | Long | Green skin, and the maths of how many square metres of you it takes to skip lunch | TheTalentlessWriter 271K; Reactions 84K | low | reserve: weakest demand in the set |

Considered and dropped as saturated: *Earth stops spinning for 1 s* (Vsauce 21.5M and What If 6.7M; @man_ia_c's version got 0.46x; dozens of clones under 400 views), *gravity off/reversed for 5 s* (What If 2.33M, Peekaboo 3.26M; IFOLOGY's Short got 13K), *oxygen for 5 s* (BuzzFeed 11.2M, What If 15.1M, @man_ia_c 13.4M), *everyone jumps at once* (Vsauce 40.4M).

## Final 10

### Shorts (60–90 s, 9:16, countdown-HUD template from R3)

1. **whatif-friction-off-5-seconds**: "What if friction disappeared for 5 seconds?" — *Evidence:* the @man_ia_c "disappears for N s" formula (electrons 18.2M at 29x, oxygen 13.4M at 21x); What If's 1-minute long-form got 1.05M and Action Lab got 1.46M, while the best vertical take found has only 8.4K. The demand is proven and the slot is open.
2. **whatif-calcium-gone-5-seconds**: "What if calcium disappeared for 5 seconds?" — *Evidence:* What If "What If We Didn't Have Bones and Turned Into Human JELLYFISH?" got 4.42M, so boneless-body demand is proven. @man_ia_c's body-level *iron* got 2.7M (4.3x). No calcium video exists on YouTube, giving the highest originality in the set.
3. **whatif-light-walking-speed**: "What if light slowed to walking speed for 5 seconds?" — *Evidence:* Worlds In Motion "What If Light Was Really Slow?" 4.26M, Airplane Mode 36.4M and The Action Lab "Slowing the Speed of Light to 2 m/s" 3.01M. @man_ia_c *π = 3* (3.9M, 6.2x) shows that changing a physics constant works in the 80 s format.
4. **whatif-sun-gone-5-seconds**: "What if the Sun disappeared for 5 seconds?" The hook is the twist that nothing happens for 8 min 20 s. — *Evidence:* Vsauce 20.9M, BRIGHT SIDE 7.78M and SolarBalls 7.77M at 82 s, a vertical-length proof. Existing Shorts are all under 1K, and none uses the light-delay twist.
5. **whatif-moon-10x-closer**: "What if the Moon was 10 times closer?" — *Evidence:* yeti dynamics "If the Moon were at the same distance as the ISS" 5.38M (102 s) and "Moon replaced with some of our planets" 87.9M (103 s). Sky-scale comparisons are the cheapest visuals in 2D. We add a tide counter and a coastline map so it isn't just a skybox.
6. **whatif-you-100x-taller**: "What if you were 100 times taller?" — *Evidence:* @man_ia_c "pop star 100 times taller" 4.9M (7.8x) and its sequel 2.1M; What If "Grew 1cm Every Second" Short 3.3M, its channel's best Short by 7x. We use "you", never a celebrity, which avoids the IP/likeness penalty R3 found.
7. **whatif-oceans-turn-fresh**: "What if the oceans turned to fresh water overnight?" — *Evidence:* What If "All the Sea Water on Earth Became Fresh Water Overnight?" 5.93M and Ridddle 4.33M. Two independent multi-million hits make the demand clear. It reuses the B3 ocean kit (reef, fish, depth gradient) plus a salinity counter and a Gulf Stream map.
8. **whatif-earth-had-rings**: "What if Earth had rings like Saturn?" — *Evidence:* What If 5.04M, AumSum 4.11M, Joe Scott 2.78M, Peekaboo 2.64M and SolarBalls 2.15M. The demand is broad across five channels. The What If channel's own 12K Short was a long-form cut-down, which is the failure mode R3 found, not proof that the topic fails as a Short. The visuals are arcs and a shadow band over a flat skyline.

### Long-form (6–8 min, 16:9)

9. **whatif-everyone-born-same-day**: "What If Everyone On Earth Was Born On The Same Day?" — *Evidence:* Awaken "Can 2 People Really Restart Humanity?" 4.22M (23x) is the same flat-2D demography data story (timeline stamps, population chart). RealLifeLore "Every Human Ever Born Came Back to Life" 6.49M and Infographics "What if No Babies Were Born for a Year" 887K show demand for whole-population thought experiments. No direct competitor exists. The spine is a population pyramid collapsing into a single bar plus "YEAR 18 / YEAR 65" stamps.
10. **whatif-breathe-underwater**: "What If You Could Breathe Underwater?" — *Evidence:* Peekaboo 2.35M and What If 1.59M on this exact title. It uses IFOLOGY's classic "what if YOU could" power format (cluster median ~200K) and the ocean genre behind Depth Theory's 2.28M on 6K subs. It reuses the B3 explainer kit almost entirely (depth meter, scale bars, creatures, YOU figure).

## Reserve (next in line)

whatif-never-need-sleep (long), whatif-sodium-gone-3-seconds, whatif-dna-gone-5-seconds, whatif-humans-photosynthesize (long). From R3's list but not checked here: *air as thick as water for 5 s* (no comparable found), *all metal turns to rubber for 5 s*, *one world time zone* (Map Men's time-zone video got 5.4M, but no what-if comparable).

## Notes for script writers

- **Corpus:** `research/corpus/whatif/` didn't exist when this was written (09:05 UTC). Per BRIEF Update 09:00, use it once it lands. Until then, cite the comparables above and the `research/library/videos/*.json` / `research/R3/transcripts/` entries, put the 2–3 closest in front matter (`references:`), add the beat alignment table, and pass `scripts/originality_check.py`.
- **Shorts template (R3):** 0–3 s serif title with the keyword in colour. A countdown HUD runs the whole video ("FRICTION RETURNS IN 0:04.8"). The hook is second person in a named real place, with 5–7 escalating beats of 8–12 s each and one caption line per beat. Close on a "returns" beat, then an end card with one real fact and "Which one next?". Target 75–80 s, which clears TikTok's 1-minute Creator Rewards minimum.
- **Long-form template:** a "you" cold open of up to 30 s, then "here's how it works" with real numbers, then a timeline or stakes ladder with stamps and counters, then options or a verdict, then a payoff that returns to the opening scene. Target 6:30–8:00. Every long-form Short must be its own vertical script, never a cut-down.
- **Comparables are for topic demand only.** Several are Vsauce, What If (Underknown), Peekaboo or xkcd. Never borrow their wording, their specific gags or their order of beats beyond general devices.
- **Facts to verify before recording (leads, not script copy):**
  - friction: knots, nails and woven yarn hold by friction.
  - calcium: about 99% of the body's calcium is in bones and teeth; marble, limestone and chalk are CaCO3; cement is mostly calcium silicates. Keep the visuals stylised, not gory.
  - light: Lene Hau's 1999 Bose-Einstein-condensate experiment slowed light to about 17 m/s.
  - sun: sunlight takes about 8 min 20 s to arrive; the 2017 neutron-star merger (GW170817) showed gravity changes also travel at about light speed.
  - moon: currently about 384,400 km away; tidal force scales with 1/r³; the Moon recedes about 3.8 cm a year (Apollo retroreflectors).
  - 100x taller: square-cube law (weight ×1,000,000, bone cross-section ×10,000); Galileo described it in *Two New Sciences*, 1638.
  - oceans: mean salinity is about 3.5%.
  - rings: a 2024 Monash study (Tomkins et al.) proposed that Earth had a ring about 466 million years ago.
  - born same day: about 130M births a year today; check the Awaken-style fertility and age-structure numbers against UN WPP.
  - breathe underwater: seawater holds about 1/30–1/40 of the oxygen air does; Kylstra and Clark's 1960s liquid-breathing mice.
