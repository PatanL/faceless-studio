# Autonomous iteration prompt

Paste the block below into a new Claude Code session opened on `~/Documents/faceless-studio`, after `/loop ` (no interval, so it paces itself). Edit the GOAL lines first if the plan has changed.

```
You are running the faceless studio unattended while the owner is at work. Read BRIEF.md, FEEDBACK.md, docs/HOUSE_STYLE.md, docs/FEEDBACK_LOG.md and research/references/OWNER_REFERENCES.md before doing anything.

GOAL 1 (first, owner's call): reach production-quality parity with ONE reference channel first: RicksClips3000 (owner, 2026-11-02), i.e. the story lane: 2D characters lit in a 3D world built with @remotion/three, a history mechanism told paradox-first with a "You see" reveal at about 2/3, topics set in a place the camera can travel through (research/library/LANE_PRINCIPLES.md, research/references/STORY_LANE_TUTORIAL_CHECK.md). Parity is defined and verified as in docs/PARITY.md (measured checks within the references' range, a blind side-by-side judge panel, then the owner's phone check). Log every attempt in docs/PARITY_LOG.md. All parity work goes to this lane until it passes. Other lanes get no new parity work, though their finished videos can still be posted. Everything below serves this first; views are the second goal.

GOAL 2: grow the channel. Keep testing lanes until one video reaches 10K views, then lock to that style (owner's rule). Work on the highest-ROI parts with specialist agents, continuously:

1. VIDEOS (main lane): make every new Short with the specialist workflow: Workflow({scriptPath: "scripts/workflows/video_pipeline.js", args: {lane, slug, brief, refs}}). It runs research (reference breakdowns, comment mining, fact check), a 3-writer script panel with 3 judges and an editor, a shot planner and art director, a builder and audio specialist, then every-frame review plus hook/logic/motion/readability/sound critics and an adversarial final judge, with fix rounds until the ship bar or 3 rounds, then a caption. The main lane is story (RicksClips); new builds go there. Finished Shorts from the other lanes (kurz explainer in style A; zackd what-if) can still go out, but start no new ones until the story lane passes parity. Aim for 2 finished Shorts a day. Read each run's result, check the frames yourself, and send the phone MP4 + caption to the owner.
2. VISUAL R&D (in parallel, one agent at a time): the biggest quality gap is the RicksClips look: lit 3D sets with ink outlines, painted textures and lens blur, flat characters that catch the key light and cast shadows, and light that follows the story (see docs/PARITY_LOG.md for what the panel failed). Test approaches head to head on the same 10 s shot and adopt what wins: Codex plates with 2.5D motion, Blender on the Mac (EEVEE, CC0 assets), better kit components. Write results to docs/RND_LOG.md and port winners into the pipeline.
3. LEARNING: references are evidence too: for each lane, compare the reference channels' outliers with their own ordinary videos to extract first principles (hook, premise, pacing, length, payoff), and feed them into the workflow prompts. Log every posted Short as an experiment in docs/EXPERIMENTS.md (variable tested, expectation, then 48 h / 7 d numbers). When posted videos have data (data/inbox/ screenshots or CSVs, or the analytics APIs once connected), find where viewers drop off and feed the lessons into FEEDBACK.md principles (general, not incidents) and the workflow prompts.
4. POSTING: when a Short is finished, send it with its caption and ask the owner; publish to Instagram and YouTube through pipeline/publish only after the owner says yes in chat.

RULES:
- Never publish or schedule anything without the owner's yes in chat for that video.
- Renders, TTS and heavy ffmpeg run on the DGX Spark, CPU only (never the GPU), nice -n 10, one Remotion render at a time, concurrency 2.
- Never delete anything; never spend money or use paid APIs; never enter credentials.
- Keep the Mac's free disk above 15 GB; if it drops below, stop rendering and say so.
- Keep FEEDBACK.md general; put dated notes in docs/FEEDBACK_LOG.md.
- Commit each working step to main with a clear message.
- If usage runs low, stop starting new agents and write status; resume after usage resets (check usage, not the clock).

EACH ITERATION: pick the next unfinished step, do it, verify by looking at the frames yourself, then append 3-5 lines to docs/OVERNIGHT_LOG.md (what changed, what still looks wrong, file paths). Send finished videos and comparison sheets with SendUserFile so they reach the owner's phone. Keep going while there is useful work; if nothing useful is left, and write a short summary at the top of docs/OVERNIGHT_LOG.md.
```
