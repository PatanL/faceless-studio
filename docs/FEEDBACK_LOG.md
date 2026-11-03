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
- 2026-11-01: owner listened to the music A/B on orca v4 and kept the new scored soundtrack (pipeline/audio/score.py, GeneralUser GS) as the default for explainers; deep_ocean stays as the fallback.
- 2026-11-01: owner: the score was too loud ("music should be background"); lowered ~6 dB (voice ~17 LU over the score). Owner confirmed the new level sounds right.
- 2026-11-01: owner listened to the orca music A/B/C and picked B: the v2 score (Kurzgesagt Shorts study) with the current sound effects. sfx_mode stays "full"; the fewer-SFX "musical" mode (C) stays available but off.
- 2026-11-01: owner rule: don't lock the channel to one style (e.g. round-head stick figures) until a video reaches 10K views; keep testing different styles and topic lanes until then.

## 2026-11-02
- Focus on one channel for quality and technique parity: RicksClips3000 (story lane). Other lanes keep posting finished videos but get no new parity work until it passes.
- Choose story topics where a 3D environment makes sense, i.e. places the camera can travel through.
- Don't rework a video once it's posted (Turk went out as v4); its lessons go into the next topic.
- The Spark overheated (89 °C) running our CPU renders and analysis, so heavy work moves to the Mac. The Spark only takes light jobs, and none while it is above 80 °C.
- "Ur supposed to decide automatically": the operator makes routine calls itself (posting, sound, captions) and reports them. Decisions made: story lane uses the story_ricks audio profile; captions are a hybrid (RicksClips look, house phrase breaks, one line, about 4 words); Vasa v15 was scheduled for 18:30 CT on YouTube and Instagram.
- Turn off the AI-generated flag on posts ("YouTube doesn't need ai label for animation renders"). The publisher defaults it off on every platform (config.ai_label), and the two scheduled Vasa posts were edited to off in Buffer.
- "Our face needs work, I like how Ricks clips face look with the shading". Story-lane heads should be lit, shaded white spheres (soft gradient away from the key light, shadow under hats) with a thick black ink outline and bold black features. Ours were flat cream discs with thin features. This is now the visual track's first item.
