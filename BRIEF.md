# Faceless Studio — shared agent brief (Part A)

Read `PLAN.md` in this folder for the goal and niche analysis. This brief is the operating rules.

## Locations

- **Source of truth (code, kits, docs, research):** Mac `~/Documents/faceless-studio` (git repo). Edit files here.
- **Runtime (installs, renders, TTS, transcription, video downloads):** DGX Spark, `ssh dgx-spark`, folder `~/studio`. Sync code with `rsync -a --exclude node_modules --exclude out --exclude .git ~/Documents/faceless-studio/ dgx-spark:~/studio/app/`, run there, and pull back only finished MP4s/PNGs you need to look at (into `~/Documents/faceless-studio/out/`, keep < 2 GB total).
- Research data: `research/<lane>/` here (JSON + markdown + small contact-sheet JPGs). Downloaded videos go on the Spark under `~/studio/refs/`, never on the Mac.

## Hard rules

1. **Never use the Spark GPU** — another job holds it. Set `CUDA_VISIBLE_DEVICES=""` for anything Python/ML (TTS, whisper). CPU only.
2. **The Mac is a secondary Remotion render slot (owner decision 2026-11-02); it is no longer reserved for Blender.** Always render through `scripts/render.sh` (same args/env as `spark_render.sh`): it uses the Spark when `~/studio/locks/render.lock` is free and the Mac only when that lock is held **and** the Mac has ≥ 5 GB available RAM and ≥ 20 GB free disk and no other Mac render is running (`~/Library/Caches/faceless-studio/render-mac.lock`). Mac renders run `nice -n 15`, `--concurrency=2`; never start a Remotion render on the Mac by hand. TTS, whisper, Demucs and other ML stay on the Spark. Small things (ffmpeg on a few frames, yt-dlp metadata `-j --skip-download`, git) are fine on the Mac. Mac free disk must stay above 20 GB.
3. The Spark has no sudo assumption: install in user space (`pip install --user`, a Python venv in `~/studio/.venv`, npm in the project, static ffmpeg arm64 build if apt isn't available). Spark has Node and Python 3.12; 20 CPU cores; ~49 GB free RAM shared with another workload — keep render concurrency ≤ 12 threads.
4. No AI video-generation models. Everything visual is code: Remotion (React/TSX), SVG, Canvas. Local TTS (Kokoro-82M or Piper) on CPU is allowed for voice.
5. Write original scripts and stories. Reference videos are for studying structure and style only — never reuse their footage, audio, characters or text. The horror TikTok references look like translated reposts of Chinese animated series; don't copy their stories.
6. Every build lane proves its work with a rendered clip or image, not just code. Look at your own renders (Read the PNG/JPG) before saying something works.
7. Commit to git in `~/Documents/faceless-studio` with clear messages when a lane finishes a usable piece. Don't push anywhere.
8. Deadlines (UTC, check `date -u`): wave 1 lanes hand off by 10:45; pilots by 12:45; hardening by 13:40.

## Layout (create as needed)

```
PLAN.md BRIEF.md STUDIO.md
research/            R1..R5 outputs
studio/              Remotion project (package.json, src/, public/)
  src/core/          storyboard schema, renderer, captions, camera, transitions
  src/kits/explainer/ src/kits/horror/ src/kits/thumbs/
pipeline/            python/node CLI: script -> storyboard -> tts -> captions -> render
scripts/             spark_sync.sh, spark_render.sh, etc.
stories/ episodes/   scripts + storyboard JSON per episode
out/                 small pulled-back results
```

## Update 08:50 UTC — Mac is out of memory

The Mac is swapping hard (16 GB RAM, ~20 GB swap used, load ~55) and the Blender recreation needs it. From now on:
- Run **all** yt-dlp calls on the Spark: `ssh dgx-spark '~/.local/bin/yt-dlp ...'` (installed). On the Mac, at most 2 concurrent yt-dlp metadata calls, never `xargs -P` fan-outs.
- ffmpeg contact sheets, whisper, TTS, npm installs: Spark only. Remotion renders: Spark, or the Mac slot via `scripts/render.sh` under rule 2 (superseded 2026-11-02).

## Update 09:00 UTC — every script must be grounded in viral scripts

- **Corpus:** `research/corpus/<niche>/` (niche = explainer | horror | whatif) holds full timestamped transcripts of top-outlier videos, each annotated line by line (beat, device, purpose), plus `research/corpus/<niche>/PLAYBOOK.md` (viral skeleton with timing %, device catalog, pacing stats). Being built now.
- **Library analysts:** also save the full timestamped transcript of every analyzed video to `research/library/transcripts/<id>.txt` (first line: url, views, outlier score).
- **Anyone writing a script** (S1, pilots, backlog writers, studio-make): before writing, pick the 2-3 corpus scripts closest to your premise and put them in the script's front matter (`references:` id, url, views, outlier_score). Include a **beat alignment table**: each of our beats → reference beat + its timestamp + the device borrowed. Match the PLAYBOOK pacing (words/min, re-hook interval, hook length). Borrow structure and devices, never wording.
- **Originality gate:** run `python3 scripts/originality_check.py <script.md> research/corpus research/library/transcripts`; it must print PASS (no shared 8-word run, <2% shared 5-grams with any single source). Fix and rerun until it passes.
- If the corpus for your niche isn't ready yet, use `research/library/videos/*.json` hooks/beats and the reference transcripts you can fetch yourself, and still cite them.

## Update 09:06 UTC — Spark CPU budget (perf agent)

Our ~/studio jobs hit ~15 of 20 cores at 09:05 (faster-whisper + whisper_run.py together) while the box also runs another user's GPU job and other workloads (load 40–65). Keep **all our Spark work together ≤ 12 threads**, and start batch jobs with `nice -n 10`:
- whisper / faster-whisper: `cpu_threads=4` (`-t 4`), one transcription process at a time per lane; `OMP_NUM_THREADS=4`.
- Python/numpy/torch/OCR: `OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2`, at most 3 shards.
- ffmpeg: `-threads 2`–`4`, at most 3 concurrent. Remotion: `--concurrency=4`. TTS: `torch.set_num_threads(4)`.
- Always `CUDA_VISIBLE_DEVICES=""`. The perf agent renices anything of ours above the budget to +10.

## Update 09:47 UTC — pilot 3 and side-by-side QA

- **Pilot 3 = `explainer-blue-whale`**, built by a separate QA workflow into `out/pilots/explainer-blue-whale/`. H1's repeatability test must pick a different episode.
- All 3 pilots (explainer-orca, horror-pinned-rules, explainer-blue-whale) get a side-by-side review against `research/library/review-refs/<niche>/` (via `scripts/side_by_side.sh`) after their own build/fix rounds finish; fixes from that review go into the kits/pipeline.
- Several agents edit the kits concurrently: re-read a file right before editing, make targeted edits (no whole-file rewrites of shared kit files), commit small and often.
- (11:30 UTC, perf) Measured: one Remotion render with `--concurrency=4` uses about **10 cores**: 4 headless tabs at ~1.2 each, plus the headless GPU process ~2.2, plus the compositor ffmpeg ~2.2. Together with TTS timing and audio mixes, ours reached 16 cores. Start Remotion with `nice -n 10`. Use `--concurrency=2` whenever another render, TTS or whisper job of ours is running, and run only one Remotion render at a time.

## Update 11:27 UTC — horror-pinned-rules is LOCKED

Only the "horror closeout" lane may edit `episodes/horror-pinned-rules/`, `pipeline/episodes/horror_eps.py`, `studio/src/kits/horror/`, `pipeline/audio/` or render/publish `out/pilots/horror-pinned-rules/`. Every other agent (including H1/H2) must not touch those paths until `out/pilots/QA.md` shows horror PASS. Shared core files (`studio/src/core/*`): targeted edits only, and say so in the commit message.
