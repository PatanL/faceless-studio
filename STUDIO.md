# Faceless Studio: operating manual

This is how to run everything. `PLAN.md` covers goals and `BRIEF.md` covers rules; this file covers practice.
Last updated 2026-11-01 ~11:20 UTC (lane H2); house style section 2026-11-02 ~02:00 UTC.

## 0. Machines and hard rules (from BRIEF.md, enforced)

| | Mac `~/Documents/faceless-studio` | DGX Spark `ssh dgx-spark`, `~/studio/app` |
|---|---|---|
| Role | Source of truth (git), editing, reading results | All heavy work: TTS, whisper, Remotion renders, stills, thumbs, yt-dlp, ffmpeg |
| Never | Renders, Chrome, TTS, npm installs, yt-dlp fan-outs (Blender owns this Mac; 16 GB RAM) | **The GPU.** Always `CUDA_VISIBLE_DEVICES=""` |
| Disk | Keep > 20 GB free (42 GB at last check). `out/` < 2 GB (454 MB now) | Keep > 100 GB free (533 GB). Downloads go in `~/studio/refs/` |
| CPU | Small things only (git, python builders, a few ffmpeg frames) | All our jobs together use **≤ 12 threads**, started with `nice -n 10`. Remotion `--concurrency=4`, TTS 4 threads, whisper `-t 4`, ffmpeg `-threads 2-4` (max 3 at once), numpy/torch `OMP_NUM_THREADS=2` |

Other rules: no AI video generation (everything visual is code). Local TTS on CPU is allowed. Scripts are
original: references are for structure only, and every script passes the originality gate. Look at your own
render before calling it done. Commit small, don't push. Several agents edit the kits at once, so re-read a
file right before you edit it.

Sync the code to the Spark with `SKIP_NPM=1 scripts/spark_sync.sh` (rsync, no `--delete` unless `SYNC_DELETE=1`).
Spark env: `source ~/studio/app/scripts/spark_env.sh` (nvm node 22, static ffmpeg in `~/studio/bin`, venv
`~/studio/.venv` with kokoro/piper/faster-whisper). First-time install: `scripts/spark_bootstrap.sh` (run it on the Spark).

## 1. Make an episode (topic -> MP4)

Pipeline: `script.md` -> Kokoro voice + word timings + mix -> `storyboard.json` -> Remotion render -> MP4.
Full commands are in `episodes/README.md`. Short version:

```bash
# 1. Script: episodes/<slug>/script.md from pipeline/templates/{explainer,horror}.md.
#    Front matter must cite 2-3 corpus references (research/corpus/<niche>/) plus a beat alignment table.
python3 scripts/originality_check.py episodes/<slug>/script.md research/corpus research/library/transcripts   # must PASS

# 2. Voice, captions and mix (Spark, CPU)
SKIP_NPM=1 scripts/spark_sync.sh
ssh dgx-spark 'source ~/studio/app/scripts/spark_env.sh && cd ~/studio/app && TTS_THREADS=4 nice -n 10 \
  python -m pipeline.audio.make episodes/<slug>/script.md --id <slug> --meta-out episodes/<slug>/audio'
rsync -a dgx-spark:~/studio/app/episodes/<slug>/audio/ episodes/<slug>/audio/

# 3. Storyboard (light python; scene builders in pipeline/episodes/{explainer,horror}_eps.py,
#    or the generic shots.json route: python3 -m pipeline.episodes.auto <slug> --check)
python3 -m pipeline.episodes.build <slug>

# 4. Readiness gates (no rendering)
python3 scripts/check_storyboards.py episodes/<slug>/storyboard.json   # components registered, audio present (run on the Spark for audio), holds
ssh dgx-spark 'source ~/studio/app/scripts/spark_env.sh && cd ~/studio/app/studio && npm run validate -- ../episodes/<slug>/storyboard.json'

# 5. Look-dev stills (cheap, no render lock), then render the first 10 s, then the full video
scripts/spark_stills.sh episodes/<slug>/storyboard.json 0.5,3,8,15,30 out/stills/<slug>.jpg
CONC=4 PROPS=episodes/<slug>/storyboard.json scripts/render.sh Storyboard <slug>.mp4 --frames=0-299
CONC=4 PROPS=episodes/<slug>/storyboard.json scripts/render.sh Storyboard <slug>.mp4

# 6. Extras: 16:9 cut, thumbnails, QA sheet against the references
python3 -m pipeline.episodes.reformat <slug> && CONC=4 PROPS=episodes/<slug>/storyboard_16x9.json scripts/render.sh Storyboard <slug>_16x9.mp4
OUT=pilots/<slug>/thumbs scripts/thumbs_render.sh episodes/<slug>/thumbs.json
scripts/side_by_side.sh out/<slug>.mp4 <explainer|horror>
python3 scripts/loudness_timeline.py out/<slug>.mp4      # horror: the scare must be the loudest moment
```

`scripts/render.sh` is the render dispatcher (same args/env as `spark_render.sh`, which it calls for the Spark slot and
which still works on its own). It prints `[render] slot: spark|mac (<why>)`: the Spark when `~/studio/locks/render.lock`
is free; the Mac when that lock is held and the Mac has >= 5 GB available RAM, >= 20 GB free disk and no other Mac
render (`nice -n 15`, `--concurrency=2`, inputs pulled from the Spark, MP4 pushed back to the Spark's `studio/out/`);
otherwise it waits for the Spark. `RENDER_SLOT=spark|mac` forces a slot (the Mac rules still apply),
`RENDER_DRY_RUN=1` only prints the decision. On the Spark (`STUDIO_LOCAL=1`) it always uses the Spark.
`spark_render.sh` serializes Spark renders with `~/studio/locks/render.lock`. Finished MP4s come back to `out/`, and
pilots live in `out/pilots/<slug>/` with `titles.md`, `description.md`, `thumbs/` and `qa/`.
`mix.wav` exists only on the Spark (`studio/public/episodes/<slug>/`, gitignored). Rerun step 2 if it is missing.

## 2. Kit inventory (screenshots to look at)

| Kit | Code | What it gives you | Look at |
|---|---|---|---|
| core | `studio/src/core/` (`schema.ts` is the source of truth) | Storyboard schema, scenes and layers, camera presets and shake, transitions (cut/fade/dipBlack/whip/glitch), callouts, grade, word captions (pill, phrase pages, emphasis), audio (voice/music ducking/sfx) | `out/b2/sheet-v2.jpg`, `out/b2/sheet-16x9.jpg`, `out/b2/still-16x9-lowerthird.jpg`, `out/B5/b5-audio-demo-sheet.jpg` |
| explainer | `studio/src/kits/explainer/` + `README.md` | `Ocean` background; 25+ creatures at true scale (`pxPerM`): SpermWhale, ColossalSquid, Orca (poses), GreatWhite, BlueWhale, Anglerfish, Octopus, Crocodile, Hippo, Grizzly, Seal, Diver, `You` stick figure, Bus/Car/Elephant/GolfCart/Jet/Sauropod; anatomy (WhaleHeart/Tongue/Throat, Liver, Krill); infographics: DepthMeter, ScaleBar, HeightChart, Stat, Map, Timer, Options, SpeedBars, Headline, Tag, Balance, ECG | `out/explainer/sheet-v3.jpg`, `out/explainer/fv3/00-15.png`, `out/explainer/showcase-v3.mp4`, `out/queue/h2_explainer-*.jpg` |
| horror | `studio/src/kits/horror/` + `README.md` | HandPhone/Phone (chat, lock, call, banners, typing), FeaturePhone; characters Protagonist "Nora" and Neighbour/Stranger "Mr. Hale" (8 expressions, poses, talk flaps); sets FrontDoor, Peephole, Hallway, ElevatorPanel, Bedroom, LivingRoom, Stairwell; fx Flicker, Vignette, Heartbeat, Glitch, RedText, Darkness, EndCard | `out/b4/sheet_v2.jpg`, `out/b4/horror-showcase.mp4`, `out/stills/hand_check.jpg`, `out/queue/h2_horror-*.jpg` |
| thumbs | `studio/src/kits/thumbs/` + `README.md` | 1280x720 and 1080x1920 thumbnails. Explainer templates eye/scale/abyss, horror templates door/chat/hallway, 2-4 words, one red accent | `out/pilots/*/thumbs/sheet_16x9.jpg`, `out/thumbs/episodes/` |
| whatif | **not built** | The backlog storyboards reference ~60 `whatif/*` components (Hud, Moon, GiantYou, ...) | n/a (they render as magenta "missing" boxes) |
| demo | `studio/src/kits/demo/` | Minimal example kit | n/a |

Pilots (the quality bar): `out/pilots/explainer-orca/`, `out/pilots/explainer-blue-whale/`, `out/pilots/horror-pinned-rules/`.
Their QA sheets: `out/qa/*_viewer.jpg` and `*_visual.jpg`, plus `out/pilots/*/qa/`.

## 3. Quality rubric (a video ships only if every line passes)

Each line comes from the pilot fix rounds and the side-by-side review against `research/library/review-refs/`.

**Script**
1. Grounded: cites 2-3 corpus references, has a beat alignment table, and follows the PLAYBOOK pacing for its niche (`research/corpus/<niche>/PLAYBOOK.md`).
2. `originality_check.py` prints PASS: no shared 8-word run and < 2 % shared 5-grams with any single source.
3. Hook: 10-12 words in the second person, and the premise lands in the first 2-3 s. No CTA or intro. Loop bookend: the last line sets up a rewatch.
4. Pace: explainer ~180-205 wpm, horror contradiction or threat by ~11 s, a re-hook every 8-12 s. Facts are checked (`facts to verify` in the front matter).

**Picture**
5. Frame 0 works as a cover: readable subject + headline, no empty first frames at scene cuts.
6. No visual hold over **3.0 s** (`build.py` / `check_storyboards.py` "hold" column). Pilots enforce this strictly.
7. No magenta "missing" boxes, no clipped or overlapping text, nothing important below 66 % of the height (platform UI), creatures recognisable and at honest scale against their partner.
8. Captions: phrase-complete pages, 1-4 words, clear of the phone and of subjects, red **only** on emphasis words (never stopwords).
9. Horror: chat screens are readable (at most ~5 lines visible, big type), there's a reaction cut every ≤ 3 s, and the end card is held ≥ 1.7 s.

**Sound**
10. No dead air over 0.6 s inside speech. Music ducks under the voice. Horror: the scare is the loudest moment (`loudness_timeline.py`).

**Package and review**
11. `titles.md` (3 options), `description.md`, thumbnails in both formats, 9:16 master (+16:9 cut for explainers).
12. Side-by-side sheet vs references (`scripts/side_by_side.sh`) reviewed by a second agent: "same or better" on every shot class, or it goes back for a fix round.
13. Platform check (R5): original content only, no reused footage, AI-voice disclosure where the platform asks for it.
14. Explainers are in the house style (next section): the gate's `staging` and `house_style` checks pass.

## House style: Lantern & Ink

**Every explainer is made in the "Lantern & Ink" house style.** The owner saw the rebuilt orca
(`out/kurz-engine/orca_open_v3.mp4`, then the full pilot `out/lantern/orca_full_v2.mp4`) and called it "way better"
than the old flat kit; the judge scored it 59/100 (TIS tier) against 24 for the old kit
(`experiments/kurz-style/JUDGE_RUBRIC.md`). The spec is `experiments/kurz-style/STYLE_BIBLE.md`; the judge's notes and
remaining gaps are in `experiments/kurz-style/engine/NOTES.md` ("Judge").

| Layer | Where | What it does |
|---|---|---|
| Kit | `studio/src/kits/explainer/house/` (+ `README.md` house table) | the 9-layer shading stack on every figure (`shade` per layer), scene light (`scene.light`), the Ocean palette key ramp + colour shift (`key`, `shiftTo`), seeded set dressing (`Kelp`, `Reef`, `Rocks`, `Jellies`, `FishSchool`, `Ridge`, `Pod`), the title plate / lantern tag / gauge info design, the engine orca and diver |
| Motion | `studio/src/core/anim.ts`, `camera.ts` | `popSpring` (never thinner than 60 % width: the polish-2d YOU-pop fix), `dropSquash`, camera `drift` + `preroll`, iris / wipe transitions |
| House pass | `pipeline/episodes/house.py` | run on every explainer storyboard, hand builders (`build.py`) and `shots.json` (`auto.py`) alike: light + key sweep, key ramp and one colour SHIFT on the scale beat, warm lift on proof beats, the orca_open_v3 set behind every Ocean scene (blurred foreground in >= 60 % of scenes), YOU tag leaders, popSpring/dropSquash, drift, cuts -> transitions, grade |
| Staging checker | `pipeline/episodes/staging.py` | fails the build on a prop through the hero, a label on the captions or on a figure, a clipped number, a label outside the safe area, a headline repeating the caption, freeze-then-abrupt-push, no colour shift |
| Gate | `pipeline/qa/house_style.py` (+ `house_metrics.py`) | `staging` (storyboard built in the house style + the checker) and `house_style` (JUDGE_RUBRIC automatic metrics on the MP4) |

**Writing a storyboard.** Use kit figures (they are shaded; inline svg is flat), let the pass add the set, and steer the
colour script with scene `_house` marks: `{"shift": {"at": "@word", "to": "warm"}}` on the scale/turn beat,
`{"key": "danger"}` on threat beats, `{"set": false}` for a full-frame card. `allowOverlap: true` only for a real contact
beat. The full shots vocabulary is in the `pipeline/episodes/auto.py` docstring; the storyboard artist's rules are in
`pipeline/prompts/shots_explainer.md`. A hand builder module sets `HOUSE_STYLE = True` (opt out per slug with `HOUSE_SKIP`,
tune with `HOUSE_OPTS`, e.g. `{"pod": "orca"}`). The horror kit is not touched by any of this.

**Gate thresholds** (`pipeline/qa/house_style.py`, calibrated on the Spark 2026-11-01; numbers equal
`experiments/kurz-style/tools/house/judge_metrics.sh`):

| id | metric | FAIL | WARN (bible target) | new orca (orca_full_v2) | old-kit orca |
|---|---|---|---|---|---|
| P5 | hue families per frame | < 2 | < 3 | 3 | **1** |
| D3 | small specks per frame | < 100 | < 120 | 192 | **63.5** |
| D4 | edge density | < 0.035 | outside 0.040-0.08 | 0.058 | **0.029** |
| D5 | outline response | > 0.12 | > 0.05 | 0.091 (WARN) | **0.13** |
| M5 | hard cuts / min | > 6 | > 2 | 0.71 | **7.99** |
| P3 / P4 / D2 / M1 / M2 | saturation / grey / micro-details / alive / near-still | outer bounds | bible targets | pass | pass |
| P7 / D1 / M3 / M4 | pure white / shapes / s per new composition / s per change | never | bible targets | M3 8.2 s (WARN) | P7, D1, M3 WARN |

Gate on the final orca render (`orca_full_v2.mp4`, Spark, 86 s): **PASS**, `staging` PASS, `house_style` WARN (D5 0.091,
M3 8.2 s), every other check PASS except the usual captions-at-77 % safe-area WARN
(`experiments/kurz-style/data/house/gate_orca_full_v2.json`). The old-kit orca with its old storyboard: **FAIL** on
`staging` (no scene light, 15 collisions) and `house_style` (P5, D3, D4, D5, M5) (`gate_old_orca_9x16.json`).
Re-calibrate when the look changes: run `house_metrics.py` on the new and the old orca and keep every FAIL line
between them (D5 has the narrowest margin). Known gaps the WARN lines show: outlines (caption stroke, tag text: D5)
and composition cadence (M3, a new picture every ~8 s vs the 3.5 s target).

Measure one video by hand (Spark, ~1 min, nice 10, 2 threads):
`~/studio/venvs/r2/bin/python -I pipeline/qa/house_metrics.py <video.mp4> <outdir>` then
`python3 -m pipeline.qa.house_style <outdir>/house_metrics.json`.

## 4. Daily research automation (Spark cron, no LLM)

- **What runs:** at `0 6 * * *` America/Chicago (Spark local time, 12:00 UTC), the user crontab runs
  `~/studio/app/scripts/research_daily.sh`, which calls `research/automation/daily_pull.py`.
  It is niced, single-process, CPU only, guarded by a flock (`~/studio/locks/research_daily.lock`), and takes ~3 min.
- **What it does:** `yt-dlp --flat-playlist -J` (metadata only, never media) for the 35 channels in
  `research/automation/channels.json`: the PLAN reference channels (Depth Theory, mraevq, udhwkz, Awaken) plus the
  similar channels found by R1-R3 and the library. YouTube polls the Videos + Shorts tabs, TikTok polls the profile,
  30 newest uploads each. It computes `outlier_score = views / median(views, same channel + same format)`.
  For the median it skips uploads younger than 3 days, using the TikTok timestamp or, for YouTube, our own first_seen.
- **Outputs (on the Spark, under `~/studio/app/research/`):** `library.jsonl` gets appended rows: `video`
  (new, score ≥ 1.5, or top 3 of the tab), `channel` (median, top outlier, errors) and `run`.
  `library.state.json` holds first_seen and last views. `daily/<date>.md` + `daily/latest.md` list the top outliers per niche, with NEW flags and view deltas.
  These paths are excluded from `spark_sync.sh`, so a Mac sync never clobbers them.
- **Bring it to the Mac:** `scripts/pull_research.sh`, then commit `research/library.jsonl` and `research/daily/` when useful.
- **Manage:** run it now with `ssh dgx-spark '~/studio/app/scripts/research_daily.sh'`. Logs: `~/studio/logs/research_daily/<date>.log`.
  Reinstall or remove the cron line with `scripts/install_research_cron.sh [--remove]`, which keeps other users' crontab lines.
  To add a channel, append it to `channels.json`. To pause one, set `"enabled": false` on it.
- **Limits:** full per-video `yt-dlp -j` on YouTube is bot-blocked from the Spark ("Sign in to confirm you're not
  a bot"), but flat listings work, so YouTube rows have no upload date, likes or comments. TikTok rows have all of them.
  Instagram (bob.figures.it.out) can't be polled. The first run (2026-11-01 11:08 UTC) had 35 channels, 1,058 uploads and 0 errors in 163 s.

## 5. Queue: next episodes to render after the reset

Status checked 2026-11-01 ~11:15 UTC. All 12 `episodes/*/storyboard*.json` pass zod validation (`npm run validate`).
Every component they use is registered, and every `mix.wav` exists on the Spark. On the 7 non-pilot episodes
below, the storyboards were **rebuilt with the current builders**, so they now carry the pilot fix-round kit changes
(caption style and paging, phone framing, emphasis rules). Stills from the rebuild are in `out/queue/h2_<slug>.jpg` (8 frames each, no magenta boxes).
None of them has had a pilot-style fix round yet, so each one fails rubric line 6 (holds). Give each one fix round, then render.

| # | Slug | Len | Max hold | Known gaps from the stills (out/queue/) | Next step |
|---|---|---|---|---|---|
| 1 | explainer-saltwater-croc | 85.0 s | 6.2 s | Strongest look: full sets, options list, scale bar. Long holds in p09-p11 | holds fix -> render -> 16:9 + thumbs |
| 2 | explainer-pressure-ladder | 88.9 s | 5.4 s | 1,000 m and 3,302 m frames are almost empty (meter only) | add depth creatures/labels in p03-p05, holds |
| 3 | horror-mom-two-chats | 74.9 s | 5.8 s | Phone opens on an empty chat (top 2/3 blank). Bottom captions overlap chat bubbles in close-ups | chat prefill, move captions to top in phone close-ups |
| 4 | horror-roommate-two-rooms | 71.0 s | 5.9 s | Same empty-chat open. Good red grade on the climax | same as #3 |
| 5 | horror-elevator-maintenance | 79.1 s | 5.1 s | A full-black frame ~59 s (blackout: check that it's intended and ≤ 1 s). Captions over bubbles | same as #3 |
| 6 | horror-member-41 | 81.7 s | 7.2 s | Captions collide with bubbles in phone close-ups. Holds in p01-p02 (7 s) | same as #3 + extra cuts in p01-p02 |
| 7 | explainer-anglerfish | 83.9 s | 6.5 s | Several frames are just a glow on black (p01, p11-p12). Frame 0 has a tiny diver, so the cover is weak | frame-0 cover, fill empty dark frames, holds |

Other items:
- **Pilots** (orca, blue-whale, pinned-rules) are rendered in `out/pilots/`. Note that `explainer-blue-whale/storyboard_16x9.json`
  (86.6 s) is older than its 9:16 master (70.1 s), so rerun `python3 -m pipeline.episodes.reformat explainer-blue-whale` before the next 16:9 render.
- **New episodes in progress by other lanes:** `episodes/explainer-short-cookiecutter-shark/`, `episodes/explainer-giant-pacific-octopus/`.
- **What-if backlog** (`backlog/whatif/*/storyboard.json`, 8 Shorts + 1 long): these pass zod but use 4-20 unregistered
  `whatif/*` components each. They are **blocked on a whatif kit** (or on remapping to explainer/horror components). Readiness check:
  `python3 scripts/check_storyboards.py backlog/whatif/*/storyboard.json`.
- **Script-only backlog** (originality PASS, no audio or storyboard yet): `backlog/explainer/*` (10) and `backlog/horror/*` (10).
  Run steps 2-5 of section 1 for each. Pick topics from `backlog/<niche>/TOPICS.md` and today's `research/daily/latest.md`.

## 7. Operator loop

One Claude Code session (tmux `studio-op` on the Spark, `~/studio/app`) makes 2 explainer Shorts a day, each modeled
on one viral source, then gates, reviews, posts through Buffer (drafts until auto is switched on), measures and runs
one-variable experiments. Its standing instructions are `OPERATOR.md`; the design is `docs/OPERATOR_DESIGN.md`.

- **Start / watch / stop** (from the Mac or the Spark): `scripts/operator_tmux.sh start|attach|status|rotate|stop`.
  `stop` writes `data/operator/STOPPED` so the watchdog leaves it down; `start` clears it.
- **Watchdog** (system cron every 15 min, human-installed with `scripts/install_operator_cron.sh`): resumes a dead
  session, rotates it daily between 04:00 and 06:00 America/Chicago, and types `operator tick` when the heartbeat is
  over 45 min old and a job is due.
- **Human switches**: `scripts/operator_ctl.sh status|pause|unpause|mode <platform> draft|auto|disclosure <platform> yes|no`.
  A platform posts automatically only with `APPROVAL_MODE=auto` (in `~/studio/.env`, read at session start), `mode=auto`
  and `disclosure_ok_auto=true`; otherwise every post is a Buffer draft to approve. Messages for you: `data/operator/HUMAN.md`.
- **Permissions**: the session runs with `--permission-mode dontAsk` and the allowlist `~/studio/operator_settings.json`
  (review and copy `scripts/operator_settings.example.json`), plus the PreToolUse guard `pipeline/ops/guard.py`, which
  blocks auto posting while `APPROVAL_MODE` is not `auto`, secrets, switches, cron, push and edits outside the
  operator's own outputs, in every permission mode. `bypassPermissions` is refused in drafts mode.
- **State and jobs**: `python -m pipeline.ops.state show --brief`, `python -m pipeline.ops.due`,
  `python -m pipeline.ops.run auto|start|plan <job>`, `python -m pipeline.ops.budget check`. Job logs:
  `~/studio/logs/operator/`. `python -m pipeline.ops.run plan <job_id>` prints a job's commands without running them.
- **Bring results to the Mac**: `scripts/pull_ops.sh [--proposals]` (Spark-owned paths, no media), then commit.
- **Kill rule**: after 30 YouTube videos, median 7-day views per video vs 10,000 plus trend (`data/killrule.json`); on
  `stop` the loop pauses itself and writes HUMAN.md.
