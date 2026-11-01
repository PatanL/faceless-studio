# Zack D. Films — channel analysis (internal format research)

Internal research only, to learn the format. Do not copy scripts, characters, visuals or titles for publication.

- Channel: Zack D. Films, YouTube `@zackdfilms`, **29.5M subscribers** (yt-dlp `channel_follower_count`, fetched 2026-11-01 on the Spark).
- Data: `channel.json` in this folder. It has every video row (`videos`), cluster stats, length buckets, title patterns, the top 30 outliers and the annotation picks.
- Sample: the newest **400 Shorts** from the `/shorts` tab, about 2026-08-11 to 2026-11-01. 387 of them were at least 3 days old ("mature") and are the ones used in the stats.

## How the data was collected, and its gaps

- `yt-dlp --flat-playlist -J` on the Shorts tab gives a title and a view count for all 400. YouTube rounds these view counts to 2 significant figures (for example 10,000,000).
- `yt-dlp -j --skip-download` per video gave the exact upload date, duration, likes and comments for the **newest 183** (2026-09-24 to 2026-11-01). After that, YouTube answered "Sign in to confirm you're not a bot" for every request from the Spark IP. It was still blocked at the end of the run, and I did not try to get around it. For the older 217, dates are estimated from upload order (4.87 per day). Their duration, likes and comments are missing.
- **Warning for annotators:** downloading these videos from the Spark may hit the same wall. Try again later, slowly, before you assume a video cannot be fetched.
- TikTok: yt-dlp on `@zackdfilms` returns a different, tiny account (2 videos, about 500 views, channel "zoomy"), and `@zack.d.films` returned nothing. Instagram needs a login. Only YouTube is covered here.
- Three Zack D. videos are already in the explainer corpus: `4QGQhaRv4Dw` (man lost floating in the ocean), `fmZfphacPPQ` (ocean pressure) and `6mRR91AbxjQ` (horseflies). I avoided them in the picks below.
- **Outlier score** = views ÷ the median views of the 31 neighbouring mature uploads, centred on the video and in upload order. Videos uploaded after 2026-10-29 are left out of the stats and the picks because their views are still climbing.

## Upload cadence

- **About 5 Shorts a day, every day.** In the 39 days with exact dates, 31 days had 5 uploads, 6 days had 4, one day had 3 and one had 1. That works out to about 34 a week and about 145 a month.
- At this volume, each video is one ticket in a lottery. The channel wins because its floor is very high, not because each upload is crafted to break out.
- Weekly medians move between 6.6M and 14M with no clear trend. Week 44 is low because its videos are young. Week 39 dipped to 6.8M, then weeks 40-41 recovered to 14M.

## View distribution (387 mature Shorts)

| stat | views |
|---|---|
| median | **10.0M** |
| mean | 12.3M |
| p10 / p25 | 4.1M / 6.35M |
| p75 / p90 | 15.5M / 21.4M |
| min / max | 1.2M / 66M |

| bucket | count |
|---|---|
| < 5M | 54 (14%) |
| 5-10M | 127 (33%) |
| 10-20M | 157 (41%) |
| 20-40M | 42 (11%) |
| 40M+ | 7 (2%) |

- The spread is tight for a Shorts channel: the p90/p10 ratio is only about 5x. The worst videos still pass 1M.
- Breakouts are 3-6x the rolling median. Nothing in the sample is 20x or more.
- Engagement (newest 176 with metadata): median like rate **3.5%**, median comment rate **0.028%** (about 1 comment per 3,500 views). That is low comment engagement: people watch these passively and loop them.
- The highest like rates (5.7-8%) all go to emotional or reflective videos: "What You Have Is Someone Else's Dream", "The Boy Who Punched Back", "He Raced His Dead Dad In A Video Game". Emotion earns likes; mechanism earns views.

## Topic clusters

Each video gets one primary topic, assigned by keyword rules on the title and then checked by hand. "log10 SD" measures how much views vary within the cluster (lower is steadier). "≥2x share" is the share of the cluster's videos that are at least 2x the rolling median.

| cluster | n | median views | p25-p75 | p75/p25 | log10 SD | median outlier | ≥2x share |
|---|---|---|---|---|---|---|---|
| nature (animal and plant mechanisms) | 46 | **14.0M** | 9.4-15.3M | 1.65 | 0.25 | 1.13 | 11% |
| eerie true mystery | 6 | 14.0M | — | 1.86 | 0.14 | 0.90 | 17% |
| history and origins | 22 | **13.0M** | 8.6-18.8M | 2.18 | 0.24 | 1.15 | 9% |
| gross-out | 10 | **12.5M** | 11-14.8M | **1.34** | **0.20** | **1.25** | 10% |
| fiction skits ("(fiction)", "(Patent Pending)", parable) | 14 | 12.0M | 8.1-19M | 2.36 | 0.30 | 1.06 | **21%** |
| puzzles, riddles, thought experiments | 22 | 11.0M | 8.3-16.5M | 2.00 | 0.27 | 1.10 | 14% |
| survival, danger, accidents | 21 | 11.0M | 6.7-15M | 2.38 | 0.30 | 1.00 | 14% |
| what-if hypotheticals | 15 | 11.0M | 7.6-17M | 2.24 | 0.24 | 1.18 | 7% |
| inside your body and health | 22 | 10.0M | 8.1-11M | **1.35** | **0.19** | 1.00 | 0% |
| psychology, life lessons, relationships | 21 | 10.0M | 7.1-11M | 1.55 | **0.18** | 1.00 | 5% |
| how it works, inventions, tech | 48 | 9.3M | 6.7-16M | 2.40 | 0.27 | 1.00 | 8% |
| heartwarming, rescue, kindness | 42 | 9.2M | 6.4-14M | 2.20 | **0.31** | 0.97 | 17% |
| life hacks, DIY, food crafts | 52 | 9.0M | 5.4-13M | 2.45 | 0.32 | **0.79** | 12% |
| odd true news (crime, records, pranks) | 36 | 8.0M | 4.9-14M | **3.08** | 0.31 | 0.80 | 11% |
| pop culture, film behind-the-scenes | 10 | 5.9M | 4.9-8.6M | 1.78 | 0.34 | 0.73 | 20% |

**Highest median with the lowest variance:**

- **Gross-out** (12.5M, p75/p25 1.34, median outlier 1.25) and **nature mechanisms** (14M, 1.65, the largest cluster) are the steady winners. For a new channel these are the safest picks: high floor, rarely a flop.
- **History and origins** (13M) is also high, with medium spread.
- **Body** and **psych** are the steadiest of all (log10 SD 0.18-0.19) but sit at the channel median. They are a reliable 10M and almost never break out (0% and 5% at ≥2x).

**High variance, lottery clusters:** heartwarming, fiction skits, pop culture, life hacks and odd news. Their medians are lower, but they produce a large share of the biggest hits:

- Toucan beak 61M, eagle beak 51M, turtle tornado shelter 35M.
- "The Puber" (Patent Pending) 39M, "The Bathroom Mode" (Patent Pending) 32M.
- Spider-Man bite filming 40M, invisible-man filming 33M.

**Takeaway for our slate:** build the base on nature, gross and body mechanisms, and add a smaller share of heartwarming or fiction tickets for the upside.

## Recurring franchises

- **"(Patent Pending)" fake inventions** (7 in the sample): a deadpan product ad for an absurd gadget. Their views range from 4.8M to 39M, so they are hit or miss. The title is "The [Product Name]" plus "(Patent Pending)".
- **Animal prosthetics** (toucan, eagle, parrot, turtle harness, bottle-cap turtle shell, cow hoof, goose guiding a blind dog): consistently above median, and the source of the top 2 non-tech hits.
- **"(fiction)" or "(urban legend)" short horror or morality tales**, often around holidays (the Halloween week had 5). Long, at 49-72 s, and they outperform when they land: "The Last Doomsday Bunker" got 2.5x.
- **Second-person survival or what-to-do** ("What To Do If Your Car Sinks?" 3.1x) and **second-person body** ("How To Get Water Out Of Your Ear" 47M).

## Title patterns (387 mature)

| pattern | n | median views | median outlier |
|---|---|---|---|
| "How X ..." (mechanism or verb: "How Horseflies Bite You") | 61 | 10M | 1.03 |
| Subject + verb headline ("Toucan Gets A ...", "Stuck In The Sky ...") | 53 | 10M | 1.03 |
| **"Why X ..."** | 46 | **12M** | **1.12** |
| "How To X" | 42 | 10M | 0.91 |
| **"The [Noun] Who/That ..."** | 42 | **7M** | **0.78** |
| He/She/They + past-tense verb | 33 | 9.7M | 0.95 |
| **"The X" short noun phrase** ("The Crocodile Paradox", "The Mail Chute Mystery") | 29 | **12M** | **1.22** |
| "How X Works" (literal) | 27 | 8.6M | 0.84 |
| Gerund ("Turning A X Into Y", "Making A ...") | 23 | 7.2M | 0.72 |
| Can/Could/Would/Does You ...? | 12 | 8.1M | 1.00 |
| tagged skit "(fiction)" / "(Patent Pending)" | 11 | 10M | 1.00 |
| "What If X?" | 8 | 11.7M | 1.05 |
| "What Is / What Happens ..." | 6 | 13M | 1.09 |

- **Every title is Title Case, about 7 words** (median), and ends with exactly one reaction emoji. The emoji works as a genre label: 🤔 for an explainer, 😮 for wow, 😨 for danger, 😱 for shock, 🤢 for gross, 😢 or 🥲 for emotional, 😏 for a trick or hack.
- By first emoji: 😱 (n=18) has a 14M median, 🤢 12M, 😌 14M, 🤤 14M. The two workhorses, 🤔 (n=98) and 😮 (n=91), sit at 9.9M, and 😏 (n=15) at 7.6M. Shock and gross signals beat neutral curiosity.
- Short "Why X" or "The X" titles beat longer "The Person Who Did Y" titles: 7M median and 0.78x. Leaving the story implied works better than summarising it.
- Gerund craft titles ("Turning ...", "Making ...") are the weakest pattern (0.72x).
- Only 10% of titles use "you" or "your", but several of the biggest hits do: water out of your ear, car sinks.
- The literal "How X Works" is below median (0.84x) even though the top video of the sample, Electrical Outlets at 66M, uses it. The object matters more than the template: it has to be something everyone touches daily.

## Length vs views (176 mature with duration)

| duration | n | median views | median outlier |
|---|---|---|---|
| ≤ 25 s | 11 | 8.1M | 0.99 |
| 26-30 s | 38 | 9.75M | 1.04 |
| 31-35 s | 41 | 11M | 1.00 |
| 36-45 s | 50 | 10M | 0.94 |
| 46-60 s | 24 | 12.5M | 1.03 |
| > 60 s | 6 | 18M | **1.69** |

- The median length is **35 s** (p10 27 s, p90 52 s). The house format is a 28-40 s Short.
- Length barely predicts views: the rank correlation between duration and views is only +0.16. Inside 26-60 s the median outlier stays flat between 0.94 and 1.04.
- The 6 videos over 60 s (fiction tales, "The Bathroom Mode" at 77 s, "Why ChatGPT Contradicted Itself" at 92 s, "The Boy Who Punched Back" at 89 s) all did well, at 1.0-2.5x. That is a small sample, and they are story formats that earn the extra time.
- Mechanism explainers should stay around 24-35 s. The outlets, cookiecutter shark, water-in-ear and maggots hits are 24-33 s.

## Top outliers (mature)

| outlier | views | cluster | sec | title | id |
|---|---|---|---|---|---|
| 6.0 | 66M | howitworks | 24 | How Electrical Outlets Work | 0BZ1C83I2R4 |
| 5.1 | 51M | heartwarming | — | Eagle Gets A 3D Printed Beak | yudJI1L8jlI |
| 4.07 | 57M | nature | 28 | How Cookiecutter Sharks Bite Whales | CRGWDiIgMZ4 |
| 3.9 | 39M | fiction | — | The Puber (Patent Pending) | 1Rd3_pXs6DU |
| 3.73 | 41M | survival | — | He Drifted At Sea For 133 Days | NdKRD1j9juE |
| 3.59 | 61M | heartwarming | 38 | Toucan Gets A Custom Artificial Beak | MSPVq-5sbCg |
| 3.5 | 35M | heartwarming | — | The Turtle Shelter Built For Tornadoes | WUfJ7Ph7D44 |
| 3.4 | 34M | nature | — | Japanese Eels Can Escape A Fish's Stomach | oiet6vWOciM |
| 3.36 | 47M | lifehack/body | 30 | How To Get Water Out Of Your Ear | W3NlT3SKkmQ |
| 3.09 | 21M | survival | — | What To Do If Your Car Sinks? | p832whe8hrI |
| 3.0 | 30M | lifehack | — | How To Extract Your DNA At Home | XKnmhvNpIvw |
| 2.8 | 28M | oddnews | — | Teen Builds An Underground Cave | oFWOt8YJADk |
| 2.64 | 29M | gross | 33 | Maggots Started Falling From Her Ceiling | NEgarf1vDTU |
| 2.5 | 30M | history | 31 | How Mr. Potato Head Was Invented | XFY7-td3LA8 |
| 2.36 | 33M | popculture | 33 | How They Filmed An Invisible Man In Snow | bZoR8A2znpo |

"Why Dobermans Have Cropped Ears" (30M at only 2 days old) is a likely future outlier. It was too young to score.

## The 10 videos to annotate (7 outliers across clusters and 3 controls)

| role | id | title | views | outlier | cluster |
|---|---|---|---|---|---|
| outlier | 0BZ1C83I2R4 | How Electrical Outlets Work | 66M | 6.0 | howitworks |
| outlier | yudJI1L8jlI | Eagle Gets A 3D Printed Beak | 51M | 5.1 | heartwarming |
| outlier | CRGWDiIgMZ4 | How Cookiecutter Sharks Bite Whales | 57M | 4.07 | nature |
| outlier | 1Rd3_pXs6DU | The Puber (Patent Pending) | 39M | 3.9 | fiction |
| outlier | W3NlT3SKkmQ | How To Get Water Out Of Your Ear | 47M | 3.36 | lifehack/body |
| outlier | p832whe8hrI | What To Do If Your Car Sinks? | 21M | 3.09 | survival |
| outlier | NEgarf1vDTU | Maggots Started Falling From Her Ceiling | 29M | 2.64 | gross |
| control | MKRYulCq3Mo | The Machine That Copies Human Digestion | 10M | 1.04 | howitworks |
| control | -7MDLZCb1Mw | How Sloth Fur Hides A Tiny Ecosystem | 14M | 1.00 | nature |
| control | jHbhgBgaA34 | How Bad Posture Gets Worse Over Time | 10M | 1.00 | body |

- For survival I picked "What To Do If Your Car Sinks?" over "He Drifted At Sea For 133 Days" (3.73x). The drifting video is too close to the explainer corpus's `4QGQhaRv4Dw`, and the car video tests the second-person survival format.
- Alternates if a video cannot be fetched:
  - `XFY7-td3LA8` (history, 2.5x)
  - `oFWOt8YJADk` (odd news, 2.8x)
  - `7_RM_cycm2s` (puzzle, 2.55x)
  - `MSPVq-5sbCg` (toucan, 3.59x)
  - `NdKRD1j9juE` (drifted at sea, 3.73x)
