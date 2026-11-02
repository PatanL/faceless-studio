# Feedback and decision log

Dated history of the owner's notes and decisions. Judges and builders read FEEDBACK.md (principles), not this file. Add new notes here; only fold a note into FEEDBACK.md if it reveals a missing *general* principle.

Older files cite the previous numbering. It maps onto the current principles (P) as: A1, A2 → P6 · A3, A4 → P4 · A5 → Process · B1, B2, B3, B4 → P1 · B5 → P3 · B6, B7 → P8 · B8 → P5 · C → Process (separate format).

## Log

- 2026-11-01: rules created from the Spark-session feedback and the studio chat ("quality isn't perfect/continuous, and the hook isn't good").
- 2026-11-01: owner clarified that the Spark notes were for edits and that informational videos have different optimal hooks. Split into sections A/B/C; explainer hook rules now come from the playbook's outlier formulas.
- 2026-11-01: orca pilot posted: YouTube 482 views / 26 likes (fresh channel, 3 subs), Instagram ~1,000, Facebook ~1,000, TikTok ~0 (account likely flagged; validate on YouTube + Instagram + Facebook).
- 2026-11-01: voice: the owner wants Fish Audio's S2 ("drama") model if it can run on CPU; otherwise Kokoro is good enough.
- 2026-11-01: graphics bar: the owner wants **Kurzgesagt-tier** visuals (The Infographics Show, e.g. fDzCHPWkou4, is also clearly better than us). Code can render anything After Effects does; the gap is authoring (illustration detail, shading/lighting, depth, motion craft). Target style: experiments/kurz-style/STYLE_BIBLE.md once written; judge with its JUDGE_RUBRIC.md.
- 2026-11-01: voice: the current narrator *style* (calm documentary male, like am_michael) is fine; what matters most is that it does **not sound robotic or fake**. Naturalness beats any particular timbre.
- 2026-11-01: blind voice test: the owner picked #6 (Chatterbox Turbo cloned from am_michael) and #7 (Kokoro am_michael, sentence-by-sentence, speed 1.1, no chain). Pipeline default is now #7's mode (commit above); Chatterbox Turbo stays as an A/B option.
- 2026-11-01: 3D/Blender parked. The owner rates the Awaken recreation at ~75% of the reference's detail and says stop for now; the Zack D. Films-style Blender learning lane (CC0 assets, shot ladder, overnight on the Mac) is designed but not started. Focus stays on 2D.
- 2026-11-01: owner on the Lantern & Ink orca rebuild (out/kurz-engine/orca_open_v3.mp4): "way better". It's the target look for every explainer; port into the live kit + operator default is underway.
- 2026-11-01: owner: "don't be different just to be different; some stuff is standard or obviously better." Style decisions are made on quality only. Only characters, assets, compositions and branding must be ours. Stipple terminator off by default (hard terminator); no technique bans (STYLE_BIBLE override, JUDGE_RUBRIC §4 rewritten).
- 2026-11-01 (owner, orca v2 at 0:22-0:24): **logical consistency**: every element on screen must make sense for where we are (location, depth, climate) and what the narration is about. No jellyfish and background sharks drifting beside a pod hunt, no tropical coral before an Antarctic beat. Set dressing is chosen per scene from the setting, never scattered generically. **Switch scenery more**: environments should change with the story's locations and beats (open water, ice floe, reef, deep sea, coast, map, surface, boat…) instead of one reef backdrop under every scene. Method: frame-by-frame analysis of the reference videos at their native frame rate (≥ 30 fps), then of ours, compared side by side.
- 2026-11-01: owner: don't keep growing FEEDBACK.md with specific incidents. Condensed it into 8 general principles; reviewers now do a second-by-second critical-viewer pass (`pipeline/qa/REVIEW_PROMPT.md` §3, `timeline.jpg`) instead of checking a list of past bugs.
