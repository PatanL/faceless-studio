# Autonomous iteration prompt

Paste the block below into a new Claude Code session opened on `~/Documents/faceless-studio`, after `/loop ` (no interval, so it paces itself). Edit the GOAL lines first if the plan has changed.

```
You are running the faceless studio unattended while the owner is at work. Read BRIEF.md, FEEDBACK.md, docs/HOUSE_STYLE.md, docs/FEEDBACK_LOG.md and research/references/OWNER_REFERENCES.md before doing anything.

GOAL: keep testing formats until one video reaches 10K views; only then lock the channel to one style (owner's rule). Until then, don't commit to one character style or topic lane. In order:
1. Make three different ~60 s test Shorts, each a different style and topic lane, all in house style A colours with the scored soundtrack at the approved level:
   a. A RicksClips/Zack D.-type story (a clever trick or loophole from history) with simple round-head stick-figure characters (build a minimal character kit only as far as this Short needs).
   b. A Kurzgesagt-Shorts/ocean-type explainer with the existing kit (orca hero, settings, maps, boards).
   c. A third lane of your choice from research/references/OWNER_REFERENCES.md that our code can make (for example a Zack D.-style second-person "what happens if" Short).
   Pick each topic from a proven viral source with pipeline/ingest and write our own script. For one of them, also try Codex background plates (experiments/asset-gen, style A board attached) animated with parallax, against our flat sets.
2. Review every frame of each (pipeline/qa/frames30.py, REVIEW_PROMPT section 3, frame reviewers per ~10 s), compare with that lane's references side by side, fix what a viewer would notice most, rebuild. Up to 3 rounds per Short or until the ship bar in FEEDBACK.md is met.
3. If time remains, make one more Short in whichever lane looks strongest so far.

RULES:
- Never post or schedule anything; finished videos go to out/ as drafts only.
- Renders, TTS and heavy ffmpeg run on the DGX Spark, CPU only (never the GPU), nice -n 10, one Remotion render at a time, concurrency 2.
- Never delete anything; never spend money or use paid APIs; never enter credentials.
- Keep the Mac's free disk above 15 GB; if it drops below, stop rendering and say so.
- Keep FEEDBACK.md general; put dated notes in docs/FEEDBACK_LOG.md.
- Commit each working step to main with a clear message.
- If usage runs low, stop starting new agents and write status; resume after usage resets (check usage, not the clock).

EACH ITERATION: pick the next unfinished step, do it, verify by looking at the frames yourself, then append 3-5 lines to docs/OVERNIGHT_LOG.md (what changed, what still looks wrong, file paths). Send finished videos and comparison sheets with SendUserFile so they reach the owner's phone. Stop the loop when step 3 is done or nothing useful is left, and write a short summary at the top of docs/OVERNIGHT_LOG.md.
```
