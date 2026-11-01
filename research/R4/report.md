# R4 report

_Saved by the orchestrator from the lane's returned findings (subagents cannot write report files). Outputs: /Users/patrickliu/Documents/faceless-studio/research/R4/bob_reels_grid.json, /Users/patrickliu/Documents/faceless-studio/research/R4/bob_thumbs_sheet.jpg, /Users/patrickliu/Documents/faceless-studio/research/R4/thumbs/ (12 reel cover JPGs), /Users/patrickliu/Documents/faceless-studio/research/R4/frames/DfFvQ2Gugdh_overview.png, /Users/patrickliu/Documents/faceless-studio/research/R4/frames/DfFvQ2Gugdh_caption_closeup.png, /Users/patrickliu/Documents/faceless-studio/research/R4/frames/DfFvQ2Gugdh_motion_5-7s_55-57s.png, /Users/patrickliu/Documents/faceless-studio/research/R4/frames/DfDWtvrujpN_overview.png, /Users/patrickliu/Documents/faceless-studio/research/R4/frames/De0mFhMO4y7_overview.png, /Users/patrickliu/Documents/faceless-studio/research/R4/flashloop/posters_sheet.jpg, /Users/patrickliu/Documents/faceless-studio/research/R4/flashloop/reply_imgs_sheet.jpg, /Users/patrickliu/Documents/faceless-studio/research/R4/flashloop/polystoriesdaily.json, /Users/patrickliu/Documents/faceless-studio/research/R4/flashloop/meanwhileanimations.json, /Users/patrickliu/Documents/faceless-studio/research/R4/flashloop/*.jpg (5 video posters + 3 reply images)_

R4 research is finished, but research/R4/report.md was NOT written: the harness blocks subagents from writing report .md files. The full findings are below for the orchestrator to save as report.md. All supporting assets are in research/R4/ (3.3 MB).

METHOD: Claude desktop built-in browser, logged out, plus WebFetch. I logged in nowhere and entered no credentials. I closed IG sign-up modals and read the DOM. TikTok metadata came from yt-dlp --flat-playlist on the Spark (copies in ~/studio/refs/R4/).

== 1. bob.figures.it.out (Instagram) ==
- Profile: 155K followers, 0 following, bio "Figuring it out" plus a linktree link.
- Login wall is partial:
  - Visible logged out: the profile grid with views, and each reel page (caption, likes, comments, top comments, playable video).
  - Needs login: "Show more posts" and the IG JSON API (401 require_login).
  - So the data covers only the latest 12 reels.

Engagement, latest 12 reels (Oct 21–31): about 28.3M views in total, median about 1.2M, floor about 650K. Views per reel run about 8x the follower count. Like/view is about 7–8%. Posting rate is about 1 per day. All are 73–113 s.

| Reel | Title | Views | Likes | Comments | Length |
|---|---|---|---|---|---|
| DfFvQ2Gugdh | When it can't wait while driving | 7.3M | 515K | 3K | 92 s |
| DfDWtvrujpN | When you make the wrong choice (dress) | 7.3M | 515.5K | 4.9K | 87 s |
| DfAoEQOOvnh | Bed time conversations | 3.7M | 307K | 2.4K | 113 s |
| De0mFhMO4y7 | Taking up the bed | 2.6M | 168K | — | 74 s |
| DfIYQM0O9xR | Couples costume | 1.8M | 137K | — | 100 s |
| De-DytvuLcF | Talking during the show | 1.4M | 97.5K | — | 77 s |
| De7koTfOKeE | Personal photographer | 1M | 79.5K | — | 85 s |

The other five reels (never ready on time, five more minutes, parking, wasn't hungry, dreams) got 655K–796K views each.

Caption template: hook + #relationship #couplehumor #relationshipgoals #couples, plus #howitworks / #zackdfilms (deliberately borrowing the Zack D. Films audience). Share CTAs appear ("Send this to someone who…").

FORMAT: Zack D. Films-style second-person, deadpan, profane narrator. Script structure: the partner says something vague → the narrator takes it literally → escalating absurd consequences → a swear-word punchline. Example: "Your girlfriend says 'look'… you assume she means something related to the f***ing road… (dog outside a café, family on a crosswalk)… f***ing dog".
- Characters: two fixed low-poly 3D characters, Bob (bald, orange tee) and his girlfriend (brunette, purple tee). Expression swaps, no lip-sync.
- Sets: 3–4 reused sets (blue living room with sofa, bedroom, car seen through the windshield, a few exteriors).
- Shots: about 15–25 per reel, each held 3–6 s. Setups are a wide two-shot, close-ups of each character, and prop inserts. Motion is minimal (slow push-ins, small pose changes).
- Captions: bold italic white uppercase, 2 lines, lower-middle, with the current word highlighted in a red box.
- Cover: a white rounded-rectangle title card in a condensed font.
- Audio: I could not hear it. The captions imply one continuous male voiceover, probably TTS.

CODE-ONLY FIT:
- The format is easy. It uses the same machinery as the horror kit: 2 characters with expression swaps, static sets, word-highlight captions, single-voice TTS, slow pushes.
- The look is medium effort. The faceted low-poly style can be made procedurally with @remotion/three (flatShading icosphere heads). Pre-rendered pose stills plus Ken Burns moves would be cheaper. A 2D vector version is low effort.
- Originality: use our own characters and pair (roommates, parent and teen, owner and pet).
- Flag for R5: the profanity limits YouTube ad suitability, so a clean or bleeped variant is needed for YT.

== 2. @flashloop_ai (X) ==
- This is not a channel. It markets an AI video generator ("Flashloop faceless studio"), which is off-limits for us under BRIEF rule 4.
- Profile: 727 followers, 273 posts, joined Feb 2026, bio "Your AI studio for content that goes viral | 25B+ views".
- Its own posts get only 36–66 views each.
- Login wall:
  - Visible logged out: only the 5 latest posts (Oct 29–31) and their status pages.
  - Needs login: older posts, the Media tab and the video players.
  - WebFetch returns 402.
- Value: each post breaks down a viral faceless account. The formats it points to:

(a) @polystoriesdaily (TikTok), "What if X doubled every second" with a giant counter. Example: the pee-pressure video, 8 psi → 16,384 psi → splits the earth. The post calls the format "one dumb rule and a counter".
- yt-dlp: 8 videos since Oct 21. Top 1.7M views / 148K likes (110 s), then 764K, 419K, 336K, 269K. Videos run 59–117 s.
- Look: low-poly / voxel characters, serif question title, big counter.

(b) @meanwhileanimations (TikTok), "What if every [X] disappeared?". A New Year's countdown hits zero, then 5–6 consequence scenes in one simple 3D city, ending on a comments question; a flipped version is posted next.
- yt-dlp: 13 videos, 106.6K followers.
- Top: "What if all women died?" 33.1M views / 4.7M likes; "What if every Man on Earth disappeared?" 19.3M / 3.8M.
- 7 more are over 1M (pregnant men, Vesuvius today, free healthcare, smartphones vanish, immigrants vanish, dam break). Floor about 450K. Length 78–218 s.

(c) @clayrified_ (IG), clay-look moral parables and folk riddles (e.g. "make this line shorter" chalk king). 239K followers, 52 posts. Pinned reels at 37.8M / 10.7M / 4.8M; recent reels 13K–1.2M.

(d) Cartoon product ads (hair serum, 9.7M). This is a B2B ad service, so skip.

FACELESS IDEAS (ours, using the formats only):
1. Doubling-counter what-if. This is the best code-only fit and the lowest cost: an animated counter, scale comparisons, one simple character and a serif title, reusing explainer-kit parts. Our own seeds:
   - heartbeat doubles every minute
   - each step twice as long
   - phone volume doubles on every ring
   - gravity +10% per day
   - hiccups twice as loud each time
2. Countdown-vanish what-if. This has the biggest views and is good in 2D infographic style (maps, city silhouettes, counters, charts), i.e. the explainer kit with a new script template. Safer topics:
   - all satellites
   - all bees
   - the internet for a year
   - all cars
   - the Moon
3. Couple-humour narrator (Bob format). High, consistent views, and one per day is sustainable. Code-only: yes in 2D, medium in low-poly 3D.
4. Public-domain parables and riddles in our own words. The story works in code, but convincing clay does not; use a 2D storybook or paper-cut style instead.

RECOMMENDATIONS:
- Consider doubling-counter what-if as a cheap extra pilot or kit variant.
- The Bob format suits the horror kit's machinery and would make a good 4th kit.
- Hand meanwhileanimations and polystoriesdaily to R3 (what-if lane).
- Flag the divisive topics and the profanity to R5.
- Downloaded only small covers and contact-sheet frames, for study. Reuse no footage, audio or text.

NOT DONE: no git commit. The repo has no commits yet, and report.md still needs to be written by the parent, so I left the first commit to the orchestrator.
