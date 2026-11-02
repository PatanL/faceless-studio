# Owner feedback → standing quality rules

The owner gives the same notes repeatedly (Spark sessions Oct 30 – Nov 1, and this studio's chat). These are standing rules: every judge and every fixer reads this file. New feedback gets appended as a dated bullet, then turned into a rule or a judge check, so the owner never has to give the same note twice.

**Scope matters.** Hooks and pacing differ by format. Section A applies to everything; section B to informational/explainer videos (this studio's channel); section C only to cinematic edits (the owner's separate "Caught"/Malfoid project). Don't apply C's rules to explainers.

Gate: a video ships only if every applicable rule scores ≥ 7/10 and the hook ≥ 8/10.

## A. Every format

1. **Natural voice.** Natural pacing and prosody, no robotic cadence, no odd breaths or hiss, no unnatural pauses between paragraphs ("voice right now doesn't sound natural").
2. **Seamless audio.** Stitched lines flow with no audible seams, gaps or volume jumps. Music sits under the voice; sound effects land on the action, not a sentence late.
3. **Consistency.** Characters, objects and art style never drift between shots (scale, proportions, colours, design).
4. **Smooth, plausible motion.** No choppy movement, no snapping between poses, and nothing frozen while the narration talks about it.
5. **Process.** Study references frame by frame before building; rate /10 per rule with timestamps for each defect; show real frames or clips, not descriptions; never idle while something renders.

## B. Informational / explainer videos (this channel)

Source: `research/corpus/explainer/PLAYBOOK.md` §2 (21 hook formulas from outliers), the outlier-vs-control analysis in `research/library/INDEX.md`, and `research/corpus/zackd/PLAYBOOK.md`.

1. **The hook sells a question, not a mood.** Within ~3 s (Shorts median: 9 words) the viewer must hold a specific curiosity gap they want closed. Best-performing shapes:
   - the title as an action on "you" (H2);
   - a paradox ("could kill you, never has", H6, ORCA 8.3M);
   - the absurd true outcome first (H9);
   - the accident already happening (H10, 23.8M);
   - a conditional with a minimised first number ("if you sink just 10 m…", H4);
   - a tiny rate leading to a huge outcome (H13);
   - a known number with its owner hidden (H14).
   
   Pick the formula that fits the topic, and cite it in the script.
2. **"You" in the hook.** In the explainer outliers, the title and first line put the viewer in the scenario. Keep it unless the premise is a champion/true-story/new-evidence format (playbook §8).
3. **The subject is on screen in frame 1,** even if it is named later. Frame 0 is the cover: never black, never a bare title card.
4. **A first proof by ~5–8 s.** A number, a scale comparison or a visible consequence that shows the promise is real.
5. **Visual change every ~2.5–4.5 s,** and every line literalized on screen (the Zack D. rule: if the narration says it, the viewer sees it).
6. **A visible progress device** (depth meter, counter, scoreboard, countdown) running from the hook to the payoff.
7. **Pay off the promise clearly** and on time; no bait without a payoff. A bookend or loop back to the opening image is fine for explainers.
8. **Readable at phone size.** Captions are whole phrases (no dangling-word pages) with no text-on-text collisions, inside the safe area.

## C. Cinematic edits only (the owner's "Caught"/Malfoid project; NOT explainers)

1. The hook is motion and feeling (e.g. her running, the arm wrap), not information.
2. It feels like one continuous date: consistent locations, lead-ins and follow-throughs instead of cinematic jump cuts, motivated POV camera moves.
3. No pinned or static end frames; no looping back to the opening shot.

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
