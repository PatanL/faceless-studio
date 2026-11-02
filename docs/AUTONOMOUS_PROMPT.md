# Autonomous iteration prompt

Paste the block below into a new Claude Code session opened on `~/Documents/faceless-studio`, after `/loop ` (no interval, so it paces itself). Edit the GOAL lines first if the plan has changed.

```
You are running the faceless studio unattended while the owner is at work. Read BRIEF.md, FEEDBACK.md, docs/HOUSE_STYLE.md, docs/FEEDBACK_LOG.md and research/references/OWNER_REFERENCES.md before doing anything.

GOAL (in order; move on only when the current step meets the ship bar):
1. Build a round-head stick-figure character kit in house style A (studio/src/kits/explainer/): expressions, mouth shapes, poses, walk, period costumes and hats, like the RicksClips3000 characters but our own design. Prove it with rendered stills and a 10 s clip.
2. Make one ~60 s test Short on a RicksClips/Zack D.-type story (a clever trick or loophole from history; pick a proven viral source with pipeline/ingest, write our own script). Make two versions of the sets: our flat style-A sets, and Codex background plates (experiments/asset-gen, style A board attached) animated with parallax and camera moves. Use the scored soundtrack at the approved level.
3. Review every frame (pipeline/qa/frames30.py, REVIEW_PROMPT section 3, frame reviewers per ~10 s), compare with the RicksClips references side by side, fix what a viewer would notice most, rebuild. Repeat until the ship bar in FEEDBACK.md is met or 4 rounds are done.
4. If time remains, make 2 more Shorts the same way on different stories.

RULES:
- Never post or schedule anything; finished videos go to out/ as drafts only.
- Renders, TTS and heavy ffmpeg run on the DGX Spark, CPU only (never the GPU), nice -n 10, one Remotion render at a time, concurrency 2.
- Never delete anything; never spend money or use paid APIs; never enter credentials.
- Keep the Mac's free disk above 15 GB; if it drops below, stop rendering and say so.
- Keep FEEDBACK.md general; put dated notes in docs/FEEDBACK_LOG.md.
- Commit each working step to main with a clear message.
- If usage runs low, stop starting new agents and write status; resume after usage resets (check usage, not the clock).

EACH ITERATION: pick the next unfinished step, do it, verify by looking at the frames yourself, then append 3-5 lines to docs/OVERNIGHT_LOG.md (what changed, what still looks wrong, file paths). Send finished videos and comparison sheets with SendUserFile so they reach the owner's phone. Stop the loop when step 4 is done or nothing useful is left, and write a short summary at the top of docs/OVERNIGHT_LOG.md.
```
