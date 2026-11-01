# B1: Spark bootstrap and render benchmark

Lane B1, 2026-11-01 ~08:40–09:05 UTC. Everything runs on `dgx-spark` CPU. `CUDA_VISIBLE_DEVICES=""` is set in every script, torch is the CPU build (`2.15.0+cpu`, `cuda.is_available() == False`), and the GPU was not touched.

## Headline

| Workload (30 s, 30 fps, 900 frames) | Size | Concurrency | Wall time | **Seconds per video-second** |
|---|---|---|---|---|
| B2 core storyboard (real layers, camera, captions, transitions, music + SFX) | 1080×1920 | 4 | 60.1 s | 2.00 |
| B2 core storyboard | 1080×1920 | **8** | **49.7 s** | **1.66** |
| B2 core storyboard | 1080×1920 | 12 | 55.8 s | 1.86 |
| B2 core storyboard | 1920×1080 | 8 | 45.6 s | 1.52 |
| Synthetic SVG explainer (rays, 80 particles, creature, captions, no audio) | 1080×1920 | 4 | 42.8 s | 1.43 |
| Synthetic | 1080×1920 | **8** | **38.5 s** | **1.28** |
| Synthetic | 1080×1920 | 12 | 43.3 s | 1.44 |
| Synthetic | 1920×1080 | 8 | 43.9 s | 1.46 |
| Synthetic, 3 s only (90 frames) | 1080×1920 | 8 | 10.2 s | about 7 s fixed overhead |

- **Use concurrency 8.** Going to 12 is slower: the box is shared and was heavily loaded. Load average was 38 → 83 on 20 cores during these runs (another user's nice-10 jobs plus the other lanes). Our renders run at nice 0, so they get priority over the nice-10 jobs.
- Each render has a fixed cost of about 7 s: cached webpack bundle, Chrome launch and stitching.
- After `npm ci`, the first render also re-downloads `chrome-headless-shell` linux-arm64 (about 20 s).
- A full round trip with `scripts/spark_render.sh` (rsync code, `npm ci`, Chrome download, render 30 s, pull back the MP4) took **77 s**.
- Projections at c8 on today's load (B2 core rate):
  - 60–90 s Short: about 1.5–2.5 min.
  - 10 min 16:9 video: about 15 min.
- Output checked: H.264 + AAC, yuv420p, 900 frames. Contact sheets are at `out/B1/bench_sheet.jpg` (synthetic) and `out/B1/b2core_bench_sheet.jpg` (B2 core). I looked at both: they render correctly.
- The B2 benchmark used B2's own test storyboards tiled to 30 s, in `bench/b2-props/bench30-*.json`. They are rendered with `--props`, and B2's files were not modified.

## Voice (TTS) and word timings

Samples are in `out/voices/`, each about 20 s. All scripts are original text.

| File | Engine / voice | Audio | Synth time | RTF |
|---|---|---|---|---|
| `explainer_am_michael.wav` | Kokoro-82M, am_michael (US male) | 22.9 s | 20–23 s | 0.87–1.03 |
| `explainer_af_heart.wav` | Kokoro-82M, af_heart (US female) | 21.0 s | 19–23 s | 0.91–1.10 |
| `horror_bm_george.wav` | Kokoro-82M, bm_george (UK male) | 19.9 s | 19–25 s | 0.97–1.27 |
| `explainer_piper_ryan-high.wav` | Piper fallback, en_US-ryan-high | 17.6 s | 10.8 s incl. load | 0.61 |

- **Kokoro on CPU, 6 torch threads, runs at about real time on the loaded box.** A 90 s script takes about 1.5 min, so voice is not the bottleneck.
- **Word timings come straight from Kokoro.** `*.kokoro_words.json` holds `{w, s, e}` per token in seconds. Punctuation comes as its own tokens, so the caption builder should merge each one into the previous word. These timings follow the script's exact words, so they are the recommended caption source.
- **faster-whisper (base.en, int8, CPU)** transcribed all three Kokoro clips back word for word. The only difference is number formatting ("2,000", "100"). That confirms the voices are intelligible. Whisper runs at about 1× real time under the current load. Use it only for audio without known text. Its output is in `*.whisper_words.json`.
- Timing and RTF numbers are in `out/voices/report.json`. The generator is `pipeline/tts_sample.py`.

## What's installed on the Spark (user space, no sudo)

| Tool | Where | Version |
|---|---|---|
| ffmpeg / ffprobe (static arm64) | `~/studio/bin/` | 7.0.2 |
| yt-dlp (aarch64 binary) | `~/studio/bin/yt-dlp` | 2026.10.26 |
| Node | nvm `v22.22.0` (the system one is 18.19, not used) | 22.22.0 |
| Remotion | per project via npm; Chrome is auto-downloaded to `node_modules/.remotion/` | 4.0.539 |
| Python venv | `~/studio/.venv` | 3.12, torch 2.15.0+cpu, kokoro 0.9.4, misaki 0.9.4, faster-whisper 1.2.1, ctranslate2 4.8.4, piper-tts 1.8.0 |
| Piper voice | `~/studio/models/piper/en_US-ryan-high.onnx` | |

Chrome system libraries (nss, atk, gbm, pango, asound and others) were already present. `espeak-ng` is not installed system-wide, but Kokoro uses the bundled `espeakng-loader`.

## Scripts (repo `scripts/`)

- `spark_env.sh`: run `source ~/studio/app/scripts/spark_env.sh` on the Spark. It sets CPU-only, Node 22, the `~/studio/bin` PATH and the venv.
- `spark_bootstrap.sh`: the idempotent installer that set up everything above.
- `spark_sync.sh [proj]`: rsyncs the repo to `~/studio/app`, excluding node_modules, out, .git and *.mp4. It runs `npm ci` in `proj` (default `studio`) only when package.json or the lockfile changed, tracked by a hash stamp. `SYNC_DELETE=1` mirrors deletions and `SKIP_NPM=1` skips npm.
- `spark_render.sh <Comp> [out.mp4] [remotion args]`: syncs, renders on the Spark, then pulls the MP4 back to `out/`.
  - Environment variables: `PROJ`, `ENTRY`, `CONC` (default 8, hard cap 12), `PROPS` (a repo-relative JSON path), `NO_SYNC`, `NO_PULL`.
  - Renders are serialized with `flock ~/studio/locks/render.lock`, so lanes never stack over the thread budget.
- `spark_bench.sh`: the benchmark runner used for the numbers above. It prints CSV.

Example: `PROPS=episodes/ep1/storyboard.json scripts/spark_render.sh Storyboard ep1.mp4`

## Gotchas found

1. **Commit the lockfile.** B2's `studio/package-lock.json` exists only on the Spark. Pull it back to the Mac and commit it. Until then, the first `spark_sync.sh studio` sees no stamp and runs `npm ci`, which wipes and reinstalls `node_modules`, including the Chrome download. Don't trigger that mid-render of another lane. The render lock covers renders, not syncs.
2. faster-whisper 1.2.1 fails with current PyAV when given a file path (`open() got an unexpected keyword argument 'metadata_errors'`). Pass a 16 kHz numpy array instead (`load16k()` in `pipeline/tts_sample.py`), or pin `av<15`.
3. The first Kokoro run downloads the HF weights and spaCy `en_core_web_sm` into the venv. That is done now.
4. `ssh host bash -s -- args` drops empty arguments, because ssh flattens argv into one string. The scripts quote arguments with `printf %q`. The Mac runs bash 3.2, so empty arrays need the `${a[@]+"${a[@]}"}` form.
5. `npm ci` with a package.json that has no dependencies "succeeds" with an empty `node_modules`. `spark_sync.sh` now fails loudly when `node_modules/.bin` is missing.
