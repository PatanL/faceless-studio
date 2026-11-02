# pipeline/qa: L2 gate, sameness check and review sheets

Lane L2 of `docs/OPERATOR_DESIGN.md` (sections 5.6, 5.7, 7). Deterministic, no LLM, no network, no secrets.
Runs on the Spark CPU (nice 10, `CUDA_VISIBLE_DEVICES=""`, ffmpeg `-threads 2`, one ffmpeg at a time); a gate on a
75 s 1080x1920 cut takes about 12-15 s wall and about 2 cores (explainers: about 85 s with the house-style metrics).

## Commands

```bash
source ~/studio/app/scripts/spark_env.sh && cd ~/studio/app
nice -n 10 python -m pipeline.qa.gate <slug>        # exit 0 PASS, 6 FAIL, 1 error (gate.json verdict ERROR)
    [--last-n 10] [--against slug,slug] [--mp4 path] [--source-frames auto|none] [--no-sheets] [--json] [--root DIR]
python -m pipeline.qa.fingerprint <slug> [--no-video]   # rebuild out/<slug>/qa/fingerprint.json
python -m pipeline.qa.sameness <slug> [--against ...]   # sameness only, prints JSON, exit 6 on FAIL
python -m pipeline.qa.sheet <slug>                       # sbs.jpg + stills.jpg only
python -m pipeline.qa.selftest --root ~/studio/work/l2gate   # proof run in a scratch root (see below)
python3 -m unittest discover -s tests -p 'test_l2_*.py'      # 35 tests, ~3-7 s, tiny lavfi clips only
```

Writes `out/<slug>/qa/{gate.json, fingerprint.json, sbs.jpg, stills.jpg, gate.log}`. The operator's review follows
`REVIEW_PROMPT.md` and writes `review.json` (not this lane).

## Inputs it reads (all optional except the MP4 and script.md)

| File | Used for | Fallback (pilots, hand-made episodes) |
|---|---|---|
| MP4 | every media check | `make_status.json outputs.mp4` -> `out/<slug>/<slug>_9x16.mp4` -> `out/pilots/<slug>/<slug>_9x16.mp4` |
| `episodes/<slug>/script.md` | narration (originality, hook, fingerprint), `references:` | required |
| `source.json` | source id, transcript, skeleton + beats for sbs.jpg | first `references:` id; transcript from `research/library/transcripts`, `research/corpus/<niche>/{raw,auto/raw,auto}/`, `research/corpus/<niche>/<id>.md` |
| `beatmap.json` | beat sequence, caption pages, rehook / turnstile measures, sbs columns | beat-alignment table of script.md (keyword-mapped to HOOK/STAKES/RUNG/TURN/PEAK/TWIST/STINGER); 8 evenly spaced sbs columns |
| `package.json` | title pick, thumb pick, disclosure | `titles.md` "**Pick:** #N" row + its "pair with thumbnail" cell matched through `thumbs.json`; `description.md` |
| `variant.json` | thresholds and the variant check | `data/learned/rules.json` defaults, then the design defaults |
| `storyboard.json` | safe area, captions, shot mix, max hold | required for those checks (empty storyboard = they pass) |
| `audio/captions.json` | first speech time, wpm | `storyboard.captions.words` |
| `data/posts.jsonl` | sameness history (latest row per post_key; status published/scheduled/draft/sending) | `--against`; no history = sameness PASS |
| `data/operator/config.json` | `sameness.last_n` | 10 |

## Checks and thresholds (constants at the top of `gate.py` and `sameness.py`)

As in design 7.2, with these implementation notes:

- **originality**: same normalisation and limits as `scripts/originality_check.py` (imported, not copied) over
  `research/corpus` (recursive, includes `auto/`) and `research/library/transcripts`, plus the source transcript:
  FAIL at >= 1 % shared 5-grams or a shared run >= 6 words. No source transcript found = WARN.
- **safe_area**: models the renderer. Caption centres are clamped like `studio/src/core/captions.tsx`
  (`cy <= H - SAFE_AREA.bottom - 0.6 * fontSize`, SAFE_AREA read from `schema.ts`). FAIL = screen-fixed text or a
  1-line caption page ending below 80 %; WARN = anything (2-line captions) below 66 %. Edge warnings only for plain
  `text` layers (a component's box is wider than what it draws). Camera moves are not modelled.
- **captions**: WARN only (red emphasis on stopwords, beatmap pages > 4 words, caption band over a creature box in
  scenes without a camera move).
- **black_frames**: `blackdetect d=0.25 pix_th=0.10`; a run > 0.5 s FAILs unless the scene sets `intendedBlack`
  / `black_ok`, has a `Darkness`/`EndCard` layer, or a `dipBlack` transition at that cut. Near-uniform 1 fps frames = WARN.
- **frozen**: `freezedetect n=0.003 d=max_hold+0.5`.
- **missing_kit**: share of pixels within +-8 of #FF00FF in 1 fps frames at 216x384; FAIL > 0.2 % in any frame.
  Real content in pure magenta would trip it (ffmpeg's testsrc2 colour bars do).
- **variant**: measures `hook.max_words`, `pace.wpm`, `visual.max_hold_s`, `pace.rehook_s` and
  `structure.turnstile_pct` (beatmap), `visual.shot_mix` (scene majority creature vs infographic); lists the rest as
  "not measured". WARN only.

- **staging** (explainers): the storyboard was built by the house pass (scene light on every scene, no `look:
  "legacy"`) and `pipeline/episodes/staging.py` finds no violation; `[echo]` = WARN. Horror = PASS (out of scope).
- **house_style** (explainers): the automatic metrics of `experiments/kurz-style/JUDGE_RUBRIC.md` measured on the MP4
  by `house_metrics.py` (2 s grid + 30 fps motion pass; same code as `tools/house/judge_metrics.sh`, so the numbers
  match the judge's) in a python with opencv (`$STUDIO_HOUSE_PY`, else `~/studio/venvs/r2/bin/python`): about 65 s
  extra on an 85 s Short, nice 10, 2 threads, one ffmpeg at a time. Writes `qa/house/house_metrics.json` (the grid
  JPGs are deleted). FAIL lines: P5 hue families < 2, D3 specks < 100, D4 edge density < 0.035, D5 outline > 0.12,
  M5 hard cuts > 6/min, plus outer bounds on P3/P4/D2/M1/M2; the STYLE_BIBLE targets are WARN lines. Calibration and
  the table: `house_style.py` docstring and STUDIO.md "House style: Lantern & Ink". Off the Spark (Mac tests) it is a
  WARN "not measured" unless `STUDIO_HOUSE_PY` is set; on the Spark a missing opencv python is a FAIL.
- **captions** / **fingerprint** skip house set dressing (`role: dressing` or a dressing component), so the reef under
  the captions is not a collision and Kelp is never a video's "subject".

### Sameness (FAIL on any; WARN never blocks)

| Metric | Rule | Calibration (2026-11-01) |
|---|---|---|
| title char-trigram cosine | FAIL >= 0.6 | distinct scripts in the repo max 0.53 ("Why You'd Never Want To Meet An Orca" vs "... Swim With A Saltwater Crocodile"); backlog drafts of the same episode 0.64-1.0. A repeated series formula with a short subject name ("Why You'd Never Want To Meet A Hippo") will FAIL: vary the title shape inside the last 10. |
| hook (first sentence) cosine | FAIL >= 0.6 | distinct max 0.43 (narration); same-episode drafts 1.0 |
| topic | FAIL if equal after aliases (orca = killer whale, ...) or one topic's words contain the other's | topic = `topic:` front matter, else the slug (`op-YYYYMMDD-a-<topic>`, `explainer-<topic>`) |
| thumbnail dHash (64 bit) Hamming | FAIL <= 8 | near-duplicate thumb (re-graded + 4 % crop) 4; distinct explainer eye templates 11-13; **distinct horror episodes on the same door/hallway template art 3-6** (would FAIL: rotate templates) |
| narration 5-gram containment (added) | FAIL >= 0.15 | distinct max 0.069; a rewritten draft of the same episode 0.197; near-dup 0.88 |
| median frame dHash Hamming at 5 %..95 % (added) | FAIL <= 10 | re-encode with colour shift 0; distinct videos 15-26 (min: two horror chat episodes); an earlier cut of the same episode 18.5 (caught by title/hook/topic instead) |
| beat sequence normalised edit distance | WARN <= 0.1 vs 3+ of the last N | |
| shot-mix cosine | WARN >= 0.95 | orca vs blue whale 0.79 |
| cover dHash | WARN <= 8 | distinct horror kit covers can reach 8 |
| main kit subject / source video | WARN if equal | |

## Proof (Spark, 2026-11-01, scratch root `~/studio/work/l2gate`)

`python -m pipeline.qa.selftest --root ~/studio/work/l2gate` gates the three cleared pilot cuts (md5 8702a89c,
1a294416, 14376d5d, copied unchanged) in order, each against the ones before it, then a near-duplicate operator
episode `op-20261102-a-killer-whale` built from explainer-orca (reworded title and hook, five narration lines
reworded, thumbnail re-graded and cropped, MP4 re-encoded with a brightness/saturation shift, same storyboard).
Result: the three pilots PASS (1 WARN each: captions below 66 %); the near-duplicate FAILs only `sameness`
(title 0.807, hook 0.889, topic killer whale ~ orca, thumb 4, script 0.881, frames 0), exit 6. 49 s for all four.
The selftest refuses a git checkout or a `data/posts.jsonl` with non-fixture rows.

## Interface notes for the integrator (design owner folds these in)

- `fingerprint.json` adds (L2-internal) `narration_shingles`, `frame_dhashes`, `subject`, `niche`, `mp4_sha256`,
  `duration_s`, `title_from`, `beat_seq_from`, `thumb`, `shot_mix_class`, `partial`.
- `gate.json` adds `fail` (list of failing checks), `duration_s`, `niche`, `gate_s`; `checks.sameness` adds
  `value.pairs` and `hits`; a crash writes `{"verdict": "ERROR", "error": ...}` so an older PASS never survives a
  failed re-gate.
- `gate.py` takes `--against` (explicit history) and `--mp4` (override); pilots resolve from `out/pilots/<slug>/`.
- Uses `pipeline.common.jsonl.read` when L5's library exists, else an equivalent local reader.

## Environment

No secrets. Optional: `STUDIO_ROOT` (default the repo this code is in), `STUDIO_REFS` (source videos, default
`~/studio/refs`), `FFMPEG` / `FFPROBE` (default `~/studio/bin/*`, then PATH). Needs numpy (Spark venv has it);
no Pillow (labels use a built-in bitmap font; the Spark's static ffmpeg has no drawtext).
