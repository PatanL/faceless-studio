# Faceless Content Studio — Goal & Parallel Plan

Window: now → weekly usage reset (~7:00 AM, 14:00 UTC). 65% of weekly quota is unused and expires at reset.

## Goal

By reset, have a **reusable, code-only video pipeline** (no video-generation models) that turns a topic into a finished video, proven by **3 pilot videos ready to post**:

1. A working `topic → script → storyboard JSON → voice → captions → render → MP4` pipeline, one command.
2. Two 2D style kits: **ocean/animal "you vs. X" explainer** (Depth Theory style) and **phone-chat horror story** (mraevq / udhwkz style).
3. A source-linked research library: 50+ analyzed videos across the niches (outlier score, title, thumbnail, script beats, shot list).
4. Each pilot passes a side-by-side quality review against reference frames **before** we scale to more videos.

5. **Finish Codex's Awaken recreation** (Part B): a v13 full 8:14 cut where every section has been reworked against the reference by its own agent, with a side-by-side comparison. Target is "mostly the same, same or better graphics", not pixel-exact.

Two tracks run at once on separate hardware: **Part A (new studio) on the Spark CPU**, **Part B (Blender recreation) on the Mac GPU**.

## What we learned from the Codex run (01a18c4d…, "Recreate the YouTube video style")

- 14.4M tokens, ~34 hours of agent time, 12 full 8:14 versions of the Awaken "Last Guy on Earth" recreation — still crude. Codex's own verdict: the bottleneck was modeling/visual matching and prioritization, not render speed.
- It assembled and verified the whole film before any single shot looked good. **Rule now: one 10-second shot must pass review before anything scales.**
- It filled the Mac to 4 GB free (75 GB of frames and .blend backups). The Mac has **29 GB free** now. **Rule now: frames and renders live on the Spark; only final MP4s come back to the Mac.**
- Reusable: Blender/Python scene scripts + a 245 MB editable source (`~/Documents/Codex/2026-10-30/i-wa/outputs/recreation-full-494s-v12-source.zip`). Useful later for 3D, not for tonight.
- The two forked chats (01a19363-64b5…, 01a19363-a6c5…) and 01a19398… were Codex sub-agents of that thread (logging Flashloop, clock/bus/park shots). Reference log: `~/Documents/Codex/2026-10-30/i-wa/outputs/animation-references.json`.

## Niche assessment (checked tonight)

| Niche | Reference | Evidence | Visual style | Code-only difficulty |
|---|---|---|---|---|
| Ocean/animal "you vs. X" | Depth Theory — *Why You'd Never Want To Meet A Sperm Whale* | **2.28M views on a 6K-sub channel**, 10 min, posted Oct 27 | Flat 2D vector: dark-teal ocean gradient, whale/squid silhouettes, scale bars (whale vs. city bus), stick-figure "YOU", data callouts, map, timer, option lists, one realistic stock shot | **Low** — ideal first pilot |
| Phone/apartment horror | @mraevq (717K views, 6 min), @udhwkz (376K, 4 min) | Strong engagement (50K / 25K likes) | Simple 2D cartoon, 1–2 characters with expression swaps, static apartment backgrounds, **group-chat phone screens**, burned-in captions | **Low** — chat screens are pure code |
| 3D "What if" | Awaken — *What if You're The Last Guy on Earth?* | 400K views, 14K subs | Stylized 3D, many characters and sets | **High** — defer |
| ? | bob.figures.it.out (Instagram) | yt-dlp can't read Instagram; not yet viewed | Unknown | Research lane R4 |

Caution: both horror TikToks show Chinese UI text under English captions — they look like **translated reposts of Chinese animated suspense series**. Study the format; write original stories. Lane R5 checks YouTube's reused/"inauthentic" content and TikTok Creator Rewards rules before anything is posted.

## Stack

| Layer | Choice | Why |
|---|---|---|
| 2D render | **Remotion** (React/TSX → MP4) | Agents write TSX well; deterministic; CPU render via headless Chrome; parallel frame rendering on the Spark's 20 cores |
| 3D (later) | Blender, Cycles CPU on Spark | EEVEE needs a GPU; Spark GPU is busy |
| Voice | Local TTS on Spark CPU (Kokoro-82M or Piper) | Speech model, not a video model — confirm OK |
| Captions | TTS word timings, or whisper.cpp alignment on CPU | Word-level burned-in captions |
| Research | yt-dlp metadata + auto-subs + ffmpeg frame sheets | Verified tonight on YouTube and TikTok |

## Machines

| Machine | Role | Limits |
|---|---|---|
| Mac (M1 Pro, 16 GB, 29 GB free) | Orchestrator, Claude Code agents, quick previews | No full renders, no frame caches |
| DGX Spark `dgx-spark` (20 CPU cores, ~49 GB free RAM, 704 GB free disk, Claude Code installed) | All renders, TTS, transcription, downloads, project repo | **CPU only — do not touch the GPU.** Needs ffmpeg, Node, Remotion, Chrome deps, TTS installed |

Project root: `dgx-spark:~/studio` (git repo). Each build lane works in its own subfolder or branch.

## Parallel lanes

### Wave 1 — start immediately (≈12 agents, all independent)

Research (read-only, cheaper model is fine):

- **R1 Depth Theory teardown** — every upload: views, view/sub ratio, outlier score vs. channel median, title formula, thumbnail composition, transcript beat map (hook → stakes → escalation → "your options" → payoff), shot taxonomy with timestamps. Also find 5 similar channels.
- **R2 Horror chat-story niche** — find the original Chinese series and 15–20 top English accounts; script structure (hook line, rules/warnings, fake-authority twist, cliffhanger), chat-beat patterns, length vs. views, part-1/part-2 series mechanics.
- **R3 What-if niche** — Awaken, IFOLOGYFILMS, @man_ia_c: topic list, outliers, title patterns (for a later 3D or 2D what-if lane).
- **R4 bob.figures.it.out + @flashloop_ai** — via the browser; report the format and whether it fits code-only production.
- **R5 Policy and monetization** — YouTube reused/inauthentic content rules, AI-voice disclosure, TikTok Creator Rewards (>1 min) eligibility, Shorts vs. long-form for each niche.

Build (on Spark, strongest model):

- **B1 Spark bootstrap** — install ffmpeg, Node 20, Remotion + Chrome deps, TTS, whisper.cpp; benchmark a 30-second 1080p Remotion render at different concurrency; report seconds-per-video-second.
- **B2 Remotion core** — storyboard JSON schema (scenes, layers, camera moves, captions, SFX cues) → video; 9:16 and 16:9; word-level captions; transitions; parallax/pan/zoom camera; render CLI.
- **B3 Explainer kit** — SVG library and scene components: ocean depth gradient with particles and light rays, 10 sea creatures, diver, stick-figure "YOU", scale-comparison bar with everyday objects, stat callout, map pin/zoom, countdown timer, "your options" list, depth meter.
- **B4 Horror kit** — phone component (group chat, typing dots, message pop-in, notifications, incoming call, lock screen), 2 puppet characters × 8 expressions + blink/mouth flap, 6 backgrounds (door + peephole, hallway, elevator panel, bedroom, living room, stairwell), dark grade, flicker, heartbeat/vibration hooks.
- **B5 Audio** — TTS voices per niche, word timestamps → caption JSON, loudness normalization, music bed + ducking, SFX folder with cue names.
- **B6 Thumbnail generator** — code-rendered thumbnails from the same SVG kits, 3 variants per video.

Gate at ~1h: B1 benchmark done, B2 renders a 10-second test, R1/R2 deliver beat maps.

### Wave 2 — pilots (≈1h → 4h)

- **S1 Script agent** — turns R1/R2 beat maps into niche templates; writes 5 explainer + 5 horror scripts with storyboard JSON.
- **P1 Explainer pilot** — "Why you'd never want to meet a colossal squid" (or best R1 topic). 10-second shot → review → full 60–90s 9:16 + a 16:9 cut.
- **P2 Horror pilot** — original apartment-chat story, 60–90s, part-1 cliffhanger.
- **P3 Repeatability test** — a second video in whichever style is further along, made by the pipeline with no hand-edited TSX. If it needs hand edits, those become kit fixes.
- **Q1 Reviewer** — independent agent; compares pilot frames to reference frames on a rubric (composition, readability, motion, pacing, audio); returns a ranked fix list. Runs after every 10-second gate and every full render.

### Wave 3 — harden (≈4h → reset)

- One command: `studio make --niche explainer --topic "orca"` → MP4 + thumbnails + title options + description.
- Scheduled research job on Spark (daily: new outliers → library → topic queue).
- Queue a batch of 5–10 storyboards to render after the reset.
- Write `STUDIO.md`: how to run, kit inventory, quality rubric, disk rules.

## Part B — Finish the Awaken recreation (Mac)

### Current state (checked tonight)

- Latest deliverable: `outputs/recreation/recreated-full-494s-v12.mp4` + `comparison-full-494s-v12.mp4` (reference left).
- Latest native project: `work/phase42-union-stage/reconstruction-phase42-union.blend` (178 MB, Blender 4.3.2, EEVEE) + `timeline-phase42-union.json` (166 shots, 14,820 frames @ 30 fps).
- Codex had three unfinished candidates: grid40 (reviewed, not applied), captain41 (needs arm animation, console, water), earth42 (blackout animation).
- Root: `~/Documents/Codex/2026-10-30/i-wa`. Codex's goal is paused; **don't resume it in Codex while Claude works on these files.**
- Sampled v12 vs reference: opening, newsroom, crowd, captain, playground, stadium are close. Clearly off in framing or content: apartment facade (~45s), phone livestream (~85s), bedroom (~160s), street chase (~185s), plaza (~215s), ledger (~300s), nursery (~350s), Rosie 1942 (~400s), elder rooftop (~465s). Common gaps everywhere: camera framing, softer lighting/bloom/depth of field, character proportions and motion.

### Hardware rules

- EEVEE needs a GPU, so recreation renders stay on the Mac (Spark's GPU is held by a 44.6 GB Python job; Spark's apt Blender is 4.0, older than the project's 4.3).
- Mac has 16 GB RAM: **max 2 Blender processes at once**, enforced by a render-queue lock (`work/render-slots/`). Section agents iterate on isolated per-section .blend files at 960×540 previews; only the integrator renders 1080p.
- Frames: after encoding, move PNGs to `dgx-spark:~/studio/recreation-frames/` and delete them locally. Mac never below 20 GB free.
- Spark CPU helps Part B with frame extraction, reference contact sheets, SSIM/LPIPS comparison metrics and encoding.

### Section agents (12, one per section, each owns its scenes only)

| # | Range | Scenes | Known gaps |
|---|---|---|---|
| S1 | 0:00–0:20 | clock, street, bus, couple, cart, park, bench, newsroom, sofa, apartment | Already heavily worked; polish lighting/bloom |
| S2 | 0:20–1:02 | window exterior, bed daydream, pink garden, apartment facade, pilot cabins, city crowd | Facade composition |
| S3 | 1:02–1:41 | LED title, sunrise city, missing notices, livestream room, phone livestream, dusk city, power-grid street | Phone screen layout |
| S4 | 1:41–2:29 | night Earth (earth42), trucks, grocery, container ship, ship bridge, fire station, mine, barracks, summit, reception, hospital, cryo lab, population graph | earth42 candidate, ship bridge lighting |
| S5 | 2:29–3:11 | sleeping hero, bachelor door, blue bedroom, bathroom mirror, deadpan, apartment entrance, day street chase | Bedroom camera, chase framing |
| S6 | 3:11–4:05 | overhead chase, laundromat, boutique alley/disguise, disguised street, plaza fall, restroom memorial, news wall, billboards, merch, monument | Plaza camera |
| S7 | 4:05–4:52 | facility chair, cross briefing (captain41), facility reception, beach VIP lounge, cabana clinic, biology counter | captain41 arm/console/water |
| S8 | 4:52–5:17 | Morocco gateway, sultan, appointment ledger, suite queue, clinic corridor, flirt, aerial queue, whiteout, eons globe, hero faints | Ledger book |
| S9 | 5:17–5:52 | IVF bedside, ICSI lab, microscopic ICSI, vial, IVF network, control room, Project 001, sample counter, pool, maternity, Tokyo/São Paulo/Lagos nurseries, first boy | Nursery characters |
| S10 | 5:52–6:37 | five cities celebrate, babies grid, clinic factory, first ten years, playground, bench warning, corkboard, chromosome lineage, descendant crowd, women build | — |
| S11 | 6:37–7:24 | Rosie 1942, aircraft factory, today, power grid (grid40), trucks, pilots, ship captain, rooftop lights, concert, university, graduation, stadium, reunion wall, reboot street, stairwell, monument | Rosie, grid40 candidate |
| S12 | 7:24–8:14 | dad grocer, merch wall, Father's Day, elder rooftop, shop street, balloon sky, beach finale | Rooftop camera |

Each section agent:

1. Extracts reference frames for its range (every shot's first/mid/last frame + motion contact sheets) and the matching v12 frames.
2. Writes a ranked gap list per shot (framing, lighting, character, motion, props, text).
3. Appends only its scenes into `work/sections/S#/S#.blend`; never writes the master project.
4. Fixes the worst gaps first; renders 960×540 keyframes through the render queue; side-by-side vs reference.
5. **Gate at 45 min:** must show a before/after comparison that the reviewer scores as better, or it reverts to v12 for that shot and moves on.
6. Hands off: section .blend + changed frame ranges + comparison sheet + notes.

Plus:

- **I1 Integrator (single writer)** — merges accepted section scenes into `reconstruction-phase43.blend`, renders changed ranges at 1080p, encodes v13 + comparison, moves frames to Spark.
- **Q2 Reviewer** — independent agent, scores each section's before/after against the reference; nothing is integrated without its pass.

Cadence: sections deliver in rolling order; integrator does a v13 partial at ~2.5h, full v13 at ~4.5h.

## Concurrency map

| Where | What | Agents |
|---|---|---|
| Mac — this session | Part B orchestrator: S1–S12, I1, Q2 | ~14 (Blender limited to 2 at once) |
| Spark — Claude Code there (`claude` 2.1.316 is installed) | Part A orchestrator: R1–R5, B1–B6, then S1/P1–P3/Q1 | ~11 → 6 |

Running Part A's agents on the Spark keeps the Mac's 16 GB for Blender. Check that Spark's Claude Code is logged into the same account so it draws from the same quota that resets at 7 AM.

## Budget and guardrails

- Peak ≈12–15 concurrent agents in wave 1, ≈6–8 in waves 2–3. Research lanes on a cheaper model; build/pilot lanes on the strongest.
- Every build lane must show a rendered clip, not just code, before it reports done.
- Hard stop on any lane that spends 45 minutes without a reviewable render.
- Spark: no GPU, keep >100 GB free. Mac: never below 20 GB free.

## Decisions needed

1. Pilots: explainer + horror (recommended), or include 3D what-if?
2. Local TTS voice OK?
3. Run lanes as visible Claude Code sessions (one per lane) or as a background multi-agent workflow from this session?
4. OK to raise the per-workflow agent cap from 10 to ~15 for Part B?
