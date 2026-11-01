# Operator loop: design and lane interfaces

Status: design, 2026-11-01. Owner of this file: the design lane (nobody else edits it; a lane that needs an
interface change writes the request at the bottom of its own README and the integrator folds it in here).

Read with `BRIEF.md` (rules), `STUDIO.md` (practice), `research/CODE_REVIEW_FINDINGS.md` (F01-F29) and
`research/corpus/explainer/PLAYBOOK.md` (beat skeleton, hook codes H1-H21).

## 0. What we are building

One resumable Claude Code session (the **operator**) runs in tmux on the DGX Spark and, every day:

1. picks 2 existing viral explainer videos (outliers) from `research/library` + `research/daily`, one per slot;
2. makes one original explainer Short per source: the source gives the **topic angle, beat structure, pacing and
   hook type**; the script wording and every visual are ours (originality gate + a new sameness gate);
3. gates it (deterministic checks plus one combined visual and viewer LLM review);
4. posts it to TikTok, YouTube Shorts and Instagram Reels through Buffer's API (Buffer **drafts** that a human
   approves first; **auto** scheduling later, per platform, behind a switch);
5. collects metrics at 48 h and 7 d, including YouTube audience-retention curves, and maps retention drops to
   storyboard scenes, beats and lines;
6. runs **one-variable experiments** (hook, script structure or visuals), decides them with a fixed rule, and folds
   winners into a learned-rules overlay at once and into the playbooks, templates and kit through reviewed patches;
7. after ~30 YouTube videos, evaluates the **kill rule** (median 7-day views per video against 10k, plus trend).

Five lanes build it in parallel. Each lane owns a disjoint set of files (section 3). Lanes talk only through
the files and CLIs defined in sections 4-5.

Non-goals (for now): horror and what-if niches (the interfaces take `--niche`, but only `explainer` is wired),
long-form 16:9 uploads, comment replies, paid promotion.

## 1. Topology

### 1.1 Machines

| | Mac `~/Documents/faceless-studio` | Spark `~/studio/app` |
|---|---|---|
| Role | git source of truth for **code, kits, prompts, docs**. Other lanes keep developing here | Runs the operator, every make, gate, publish and analytics job. Source of truth for **operator data** (ledgers, operator episodes, auto-annotations) |
| Heavy work | never (Blender owns the Mac) | CPU only, `CUDA_VISIBLE_DEVICES=""`, `nice -n 10`, all our jobs together <= 12 threads |
| Secrets | none | `~/studio/.env` and `~/studio/secrets/` (mode 600, outside the repo copy, never synced, never printed) |

The Spark copy is not a git checkout. Code reaches it only through `scripts/spark_sync.sh` (Mac -> Spark).
Operator outputs reach the Mac only through `scripts/pull_ops.sh` (Spark -> Mac, new, owned by L5), after which
a Mac session commits them.

### 1.2 Local mode

The operator runs `studio-make` **on the Spark**, so `pipeline/make.py` and the render scripts need a local mode:

- `STUDIO_LOCAL=1` (set by `scripts/operator_tmux.sh`; also implied by `SPARK_HOST=local`) means:
  `Make.spark(cmd)` runs `bash -c "$ENV; cmd"` locally in `~/studio/app`; `sync()` and `pull()` are no-ops;
  `claude()` runs `claude -p` locally; `scripts/spark_render.sh`, `scripts/spark_stills.sh` and
  `scripts/thumbs_render.sh` run their remote block with plain `bash -s` and replace the rsync pull by a local
  copy from `studio/out/<name>` to `out/<name>`.
- Mac mode (no `STUDIO_LOCAL`) keeps working exactly as today, with the F-fixes.

### 1.3 Spark-owned paths (never pushed from the Mac)

One list, `scripts/spark_owned.txt` (owned by L1), is used by `spark_sync.sh` as `--exclude` **and** delete-protect
filters, and by `scripts/pull_ops.sh` as the pull list:

```
/data/
/episodes/op-*/
/research/corpus/*/auto/
/research/library.jsonl
/research/library.state.json
/research/daily/
/studio/public/episodes/
/studio/public/music/*.wav
/episodes/*/audio/
/out/
```

Consequences: a Mac sync can never overwrite or delete an operator episode, a ledger, an auto-annotation, a mix
or audio timings (fixes F25, F26 for these paths); operator episodes are prefixed `op-` so the rule is one glob.

### 1.4 Code lock

A Mac sync that lands while the operator is mid-step could hand Remotion half-updated kit files. So:

- `spark_sync.sh` runs the remote rsync under an exclusive lock:
  `--rsync-path="flock -w 1800 \$HOME/studio/locks/code.lock rsync"`.
- `pipeline/make.py` in local mode holds a **shared** lock (`flock -s ~/studio/locks/code.lock`) for the duration
  of each step (script, tts, shots, storyboard, review, render, package, thumbs), never across steps, so a Mac
  sync waits at most one step.
- npm installs run under `~/studio/locks/render.lock` (F08, F27).

Lock files (all in `~/studio/locks/`): `render.lock` (one Remotion render or npm ci at a time, existing),
`code.lock` (above), `make.lock` (one operator make at a time, exclusive, taken by `pipeline/ops/run.py`),
`ytdlp.lock` (one yt-dlp process at a time for the operator), `research_daily.lock` (existing).

### 1.5 Thread budget per job

| Job | Threads | Notes |
|---|---|---|
| make: TTS | 4 (`TTS_THREADS=4`) | runs in parallel with the shots step (claude, ~0 CPU) |
| make: render | Remotion `--concurrency=4` (about 10 cores) | default and cap 4 (F28); `--concurrency=2` if a whisper/TTS job of ours runs |
| whisper (annotate) | `-t 4`, `OMP_NUM_THREADS=4` | never during a render: `pipeline/sources.py` holds `render.lock` while it transcribes |
| gate (ffmpeg) | `-threads 2`, at most 2 ffmpeg at once | |
| analytics / publish | 1 | network-bound |

Rule of thumb for L5's scheduler: at most one make and one light job (gate, publish, analytics) at once.

## 2. The daily loop

Times are America/Chicago (Spark local; set `TZ=America/Chicago` explicitly in every cron/ops script because
`/etc/timezone` says UTC while `date` prints CST). All timestamps written to files are UTC ISO-8601 with `Z`.

| Local time | Job (job type) | Lane code it runs |
|---|---|---|
| 04:00 | `rotate`: fresh operator session (state lives in files) and cron re-arm | L5 `scripts/operator_tmux.sh rotate` |
| 06:00 | research daily pull (existing system cron) | existing `scripts/research_daily.sh` |
| 06:30 | `make` slot A: experiment assignment, source pick, make, gate | L4 `experiments assign`, L1 `studio-make --source auto`, L2 `pipeline.qa.gate` |
| after make A | `review` slot A: operator LLM review per `pipeline/qa/REVIEW_PROMPT.md`, at most one fix round | operator + L1 `--from review` |
| after review A | `publish` slot A: Buffer drafts (or scheduled posts) for 11:30 | L3 `pipeline.publish.post` |
| 08:45 | `make` slot B, then review B, publish B for 18:30 | same |
| every 30 min | `status`: refresh Buffer post states, capture external ids | L3 `pipeline.publish.status` |
| published + 48 h | `metrics48` | L4 `pipeline.analytics.collect --window 48h`, then `align` |
| published + 7 d | `metrics7d` | L4 `collect --window 7d`, `align`, `heatmap` for the source |
| daily 21:00 | `tiktok_inbox`: ingest any TikTok screenshots/CSVs dropped by the human | L4 `tiktok_import` (+ operator vision for screenshots) |
| Mon 07:30 | `learning`: decide experiments, update rules overlay, write LEARNING.md, open the next experiment, write repo proposals | L4 `pipeline.analytics.learning`, `experiments decide` |
| Mon 07:30 and every 5th YouTube 7-d row after 30 | `killrule` | L4 `pipeline.analytics.killrule` |

Slot times, make start times and windows live in `data/operator/config.json` (section 5.19), not in code.

Failure policy (enforced by L5): a failed step is retried once from that step (`--from <step>`); a second failure
marks the source `rejected` (reason recorded) and, if the slot's publish time is still >= 3 h away, picks the next
source; otherwise the slot is skipped. Nothing is posted that lacks `gate.json` PASS and `review.json` PASS. Two
failed slots in a row, any exit code 5 (claude unavailable), or a budget stop pauses the loop and writes
`data/operator/HUMAN.md`.

## 3. Lanes and file ownership

A lane edits only the files it owns. Everything else is read-only to it. New files go only under the lane's own
paths. Tests: each lane adds `tests/test_<lane>_*.py` (L1 also owns the existing `tests/test_make.py`,
`tests/test_auto_resolve.py`, `tests/test_spark_scripts.py`, and removes their xfail markers when a fix lands).
No lane edits `BRIEF.md`, `PLAN.md`, `research/corpus/**` (except L1 writing `research/corpus/*/auto/` on the
Spark at runtime), `studio/src/**`, `pipeline/audio/**`, `pipeline/templates/**` or the existing prompts other
than the ones listed below. Durable changes to playbooks, templates and kit come from L4 proposals that a Mac
session applies (section 9.7).

| Lane | Owns (create/edit) | Writes at runtime (Spark) |
|---|---|---|
| **L1 make** | `pipeline/make.py`, `studio-make`, `pipeline/sources.py`, `pipeline/sources_kit_fit.json`, `pipeline/episodes/auto.py`, `pipeline/prompts/script_explainer_source.md`, `pipeline/prompts/annotate_explainer.md`, edits to `pipeline/prompts/review.md` and `pipeline/prompts/package.md` (add the `{review_notes}` slot and the `package.json` output), `scripts/spark_sync.sh`, `scripts/spark_render.sh`, `scripts/spark_stills.sh`, `scripts/thumbs_render.sh`, `scripts/spark_owned.txt`, `tests/test_make.py`, `tests/test_auto_resolve.py`, `tests/test_spark_scripts.py`, `tests/test_l1_*.py` | `episodes/op-*/` (script.md, source.json, variant.json, shots.json, storyboard.json, beatmap.json, package.json, titles.md, description.md, thumbs.json, make_status.json, make.log), `out/op-*/` (MP4, sheet, thumbs), `research/corpus/explainer/auto/`, `data/sources.jsonl` |
| **L2 gate** | `pipeline/qa/` (all files, incl. `REVIEW_PROMPT.md`, `gate.py`, `sameness.py`, `fingerprint.py`, `sheet.py`), `tests/test_l2_*.py` | `out/<slug>/qa/gate.json`, `out/<slug>/qa/fingerprint.json`, `out/<slug>/qa/sbs.jpg`, `out/<slug>/qa/stills.jpg`, `out/<slug>/qa/gate.log` |
| **L3 publish** | `pipeline/publish/` (all files, incl. `buffer.py`, `queries.graphql`, `host.py`, `captions.py`, `post.py`, `status.py`, `schedule.py`, `README.md`), `tests/test_l3_*.py` | `data/posts.jsonl`, `out/<slug>/publish/captions.json`, `data/buffer_schema.json` |
| **L4 analytics** | `pipeline/analytics/` (all files, incl. `youtube.py`, `instagram.py`, `tiktok_import.py`, `TIKTOK_IMPORT.md`, `heatmap.py`, `align.py`, `collect.py`, `experiments.py`, `learning.py`, `killrule.py`, `README.md`), `tests/test_l4_*.py` | `data/metrics.jsonl`, `data/alignments.jsonl`, `data/heatmaps/`, `data/experiments.jsonl`, `data/learned/rules.json`, `data/learning/`, `data/proposals/`, `data/killrule.json`, `out/<slug>/analytics/` |
| **L5 operator** | `OPERATOR.md`, `scripts/operator_tmux.sh`, `scripts/operator_watchdog.sh`, `scripts/install_operator_cron.sh`, `scripts/operator_ctl.sh`, `scripts/pull_ops.sh`, `scripts/operator_settings.example.json`, `pipeline/common/` (`jsonl.py`, `env.py`, `timeutil.py`, `locks.py`), `pipeline/ops/` (`state.py`, `due.py`, `run.py`, `budget.py`, `config.default.json`), the new section "7. Operator loop" at the end of `STUDIO.md` (only that section), `tests/test_l5_*.py` | `data/operator/` (state.json, config.json, HUMAN.md, journal.md, jobs/), `~/studio/logs/operator/` |

`pipeline/common/` is the only shared library. L5 lands it in its **first commit** (signatures in section 4.4,
small enough to write in minutes); the other lanes import it and do not copy it.

## 4. Shared conventions

### 4.1 Ids

- **slug** (operator episodes): `op-YYYYMMDD-<slot>-<topic>`; `YYYYMMDD` is the local date of the post slot, `slot`
  is `a` or `b`, `topic` is `slugify(topic)` without the niche prefix, max 5 words. Example
  `op-20261102-a-pistol-shrimp`. `--niche explainer` is always passed explicitly (do not infer from the prefix).
- **source_id**: the platform video id as used in `research/library` (`fGcgWaswMns`, TikTok numeric id).
- **post_key**: `<slug>:<platform>`, platform in `youtube | tiktok | instagram`.
- **experiment_id**: `EXP-NNN` (zero-padded, increasing).
- **job_id**: `<YYYYMMDD>-<slot|na>-<type>[-<post_key>]`, e.g. `20261102-a-make`, `20261102-na-metrics48-op-20261102-a-pistol-shrimp:youtube`.

### 4.2 Paths

Repo-relative paths are relative to `~/studio/app` on the Spark (and to the repo root on the Mac). `DATA` =
`data/` under that root. Secrets live outside it: `~/studio/.env`, `~/studio/secrets/`.

### 4.3 Ledgers (JSONL)

All `data/*.jsonl` files are **append-only**, one JSON object per line, UTF-8, `\n`. Every row has `"v": 1` (schema
version) and `"at"` (UTC ISO write time). State changes are new rows; readers take the **latest row per key**.
Appends go through `pipeline.common.jsonl.append`, which takes an `flock` on `<file>.lock`, writes one line and
fsyncs. Nobody rewrites a ledger in place. Each ledger has exactly one writing lane (table in section 3).

### 4.4 `pipeline/common` (L5, first commit)

```python
# pipeline/common/jsonl.py
def append(path: str, row: dict) -> None            # adds v=1 and at=now if missing; flock + fsync
def read(path: str) -> list[dict]                     # [] if missing; skips (and logs) a bad line
def latest(path: str, key: str) -> dict[str, dict]    # last row per row[key]
# pipeline/common/env.py
def load_env(path="~/studio/.env") -> dict[str, str]  # KEY=VALUE lines, # comments, no export, no shell eval; missing file -> {}
def require(names: list[str]) -> tuple[dict, list[str]]  # (values, missing names); callers switch to dry-run if missing
def redact(s: str) -> str                             # replaces every loaded secret value with "***"
# pipeline/common/timeutil.py
TZ = ZoneInfo("America/Chicago")
def now_utc() -> datetime; def iso(dt) -> str; def parse(s) -> datetime; def local_date(dt=None) -> str
# pipeline/common/locks.py
@contextmanager
def flock(name: str, shared=False, timeout_s=1800)    # ~/studio/locks/<name>.lock (Mac: a temp dir)
```

### 4.5 Credentials and dry-run

No code contains, prompts for, or writes a credential. Code reads `~/studio/.env` (via `load_env`) and the token
files named there. If any variable a command needs is missing, the command prints
`DRY-RUN: missing <NAMES> in ~/studio/.env` and runs in `--dry-run` (it still builds every payload, writes it to the
ledger with `status: "dry_run"`, and exits 0). `--dry-run` can also be forced. A human creates the `.env` file and
runs the one-time OAuth consents; agents never do (BRIEF rules plus the safety rules: no entering credentials).

| Variable | Used by | Meaning |
|---|---|---|
| `BUFFER_API_KEY` | L3 | Buffer API access token (Bearer) |
| `BUFFER_API_URL` | L3 | default `https://api.buffer.com` |
| `BUFFER_ORG_ID` | L3 | optional; default the first organization the key sees |
| `BUFFER_CHANNEL_YOUTUBE`, `BUFFER_CHANNEL_TIKTOK`, `BUFFER_CHANNEL_INSTAGRAM` | L3 | Buffer channel ids (`python -m pipeline.publish.buffer channels` lists them so the human can copy them in) |
| `PUBLIC_HOST_MODE` | L3 | `cloudflared` (default) or `static` |
| `PUBLIC_BASE_URL` | L3 | only for `static`: a public URL that maps to the local file server |
| `CLOUDFLARED_BIN` | L3 | default `~/.local/bin/cloudflared` (already installed on the Spark) |
| `YT_CLIENT_SECRETS_FILE` | L4 | default `~/studio/secrets/yt_client_secret.json` (the user's own Google Cloud "Desktop app" OAuth client) |
| `YT_TOKEN_FILE` | L4 | default `~/studio/secrets/yt_token.json` (written by the one-time consent, mode 600) |
| `YT_CHANNEL_ID` | L4 | our channel id (`UC...`) |
| `IG_USER_ID` | L4 | Instagram professional account id (Graph API) |
| `IG_ACCESS_TOKEN` | L4 | long-lived Graph API token with `instagram_basic`, `instagram_manage_insights` |
| `META_GRAPH_VERSION` | L4 | Graph API version string the human sets (e.g. the current `vNN.0`) |
| `YTDLP_COOKIES_FILE` | L1, L4 | optional, user-supplied cookies file for yt-dlp when YouTube bot-blocks the Spark |
| `STUDIO_CLAUDE_MODEL` | L1 | existing (default `opus`) |

### 4.6 Exit codes (every CLI in this design)

`0` ok (including dry-run) · `1` step failed (details in the log and status file) · `2` usage error ·
`3` budget cap reached · `4` nothing to do / no candidate (e.g. no unused source) · `5` dependency unavailable
(claude auth expired, API 401/403, tunnel failed) · `6` blocked by a gate (not PASS).

### 4.7 Single writer per file

Each JSON artifact below names its writer. A second lane that wants to add information writes its own file. In
particular `gate.json` (L2) and `review.json` (operator) are separate, and `posts.jsonl` (L3) is never written by L4.

## 5. Shared schemas

Fields marked `?` may be `null`. Times `t0/t1` are seconds from the start of the video.

### 5.1 `episodes/<slug>/source.json` (L1 writes; L2, L4, operator read)

```json
{
  "v": 1, "source_id": "fGcgWaswMns", "url": "https://www.youtube.com/watch?v=fGcgWaswMns",
  "platform": "youtube", "format": "long|short|tiktok", "title": "...", "channel": "Depth Theory",
  "views": 2307237, "outlier_score": 14.65, "duration_s": 599, "picked_at": "2026-11-02T12:30:05Z",
  "pick": {"rank": 1, "score": 7.42, "reasons": ["kit_fit:SpermWhale", "outlier 14.65"], "candidates_considered": 41},
  "corpus_file": "research/corpus/explainer/fGcgWaswMns.md | research/corpus/explainer/auto/<id>.md",
  "transcript_file": "research/library/transcripts/<id>.txt | research/corpus/explainer/auto/raw/<id>.txt",
  "angle": "one line: the topic angle we borrow, in our words",
  "hook": {"code": "H1", "shape": "PLAYBOOK shape name", "first_speech_s": 0.2, "words": 11},
  "beats": [
    {"i": 0, "label": "HOOK", "playbook": "S1", "t0": 0.0, "t1": 29.0, "pct0": 0.0, "pct1": 4.8,
     "device": "2P calm + broken rule", "purpose": "..."}
  ],
  "pacing": {"wpm": 183, "avg_shot_s": 1.2, "rehook_s": 9.0},
  "skeleton": [
    {"i": 0, "label": "HOOK", "from_beats": [0], "target_pct0": 0, "target_pct1": 5, "target_s": [0, 3.5], "device": "..."}
  ],
  "target": {"runtime_s": [65, 85], "words": [210, 260]},
  "heatmap_file": "data/heatmaps/<id>.json ?"
}
```

`beats` describe the source; `skeleton` is the compressed beat plan for our 65-85 s Short (long-form sources are
compressed onto the PLAYBOOK 1b Shorts skeleton, keeping the source's order of devices). The script prompt gets
`skeleton`, `hook`, `pacing` and `angle`, never the transcript wording.

### 5.2 `episodes/<slug>/variant.json` (L1 writes from CLI flags; L2, L4 read)

```json
{"v": 1, "experiment_id": "EXP-003 ?", "arm": "control|treatment ?",
 "variables": {"hook.type": "H6", "visual.cover": "scale"},
 "rules_version": "2026-11-09T13:30:00Z", "directives": ["Use hook shape H6 (unnamed predator paradox)..."]}
```

Variable keys (the only ones experiments may set; L1 maps each to a prompt directive, L2 checks the outcome
where it can):

| Key | Values | Lever |
|---|---|---|
| `hook.type` | `source` (copy the source's hook code) or `H1`..`H21` | script prompt |
| `hook.max_words` | int 5-14 | script prompt; L2 checks |
| `hook.visual` | `subject_full`, `subject_eye`, `you_vs_subject`, `headline_only` | shots prompt |
| `structure.skeleton` | `source`, `playbook_list`, `playbook_ladder` | script prompt (which skeleton to follow) |
| `structure.turnstile_pct` | int 40-70 | script prompt |
| `structure.ending` | `loop_callback`, `stinger_fact`, `twist_question` | script prompt |
| `pace.wpm` | int 170-215 | TTS speed + script length |
| `pace.rehook_s` | float 6-12 | script prompt; L2 checks |
| `visual.max_hold_s` | float 1.5-3.0 | auto.py hold check; L2 checks |
| `visual.cover` | `scale`, `eye`, `abyss`, `headline` (thumbs templates) | shots + thumbs |
| `visual.shot_mix` | `creature_heavy`, `infographic_heavy`, `balanced` | shots prompt; L2 measures |
| `visual.caption_style` | `pill`, `page` | storyboard captions |

### 5.3 `episodes/<slug>/make_status.json` (L1 writes, atomically, after every step; L5 reads)

```json
{"v": 1, "slug": "op-20261102-a-pistol-shrimp", "niche": "explainer", "source_id": "...",
 "status": "running|done|failed|budget_stop", "step": "render", "steps_done": ["script", "tts", "shots"],
 "started_at": "...", "finished_at": "... ?", "exit_code": 0, "error": "?",
 "usage": {"script": {"input_tokens": 0, "output_tokens": 0, "cache_read_tokens": 0, "cache_creation_tokens": 0,
                      "cost_usd": 0.0, "duration_s": 0, "exit": 0}},
 "usage_total": {"weighted_tokens": 0, "cost_usd": 0.0},
 "outputs": {"mp4": "out/<slug>/<slug>_9x16.mp4", "sheet": "out/<slug>/<slug>_sheet.jpg",
             "thumbs_dir": "out/<slug>/thumbs/", "duration_s": 74.2, "mp4_sha256": "..."}}
```

`usage` comes from `claude -p --output-format json` (`usage` and `total_cost_usd` in its result). Weighted tokens
= `input + output + cache_creation + 0.1 * cache_read` (the budget unit used everywhere).

### 5.4 `episodes/<slug>/beatmap.json` (L1 writes at the storyboard step; L2, L4 read)

One row per storyboard scene, the bridge between script, shots, video time and retention:

```json
{"v": 1, "slug": "...", "duration_s": 74.2, "fps": 30,
 "scenes": [{"scene_id": "p01", "p": 1, "t0": 0.0, "t1": 2.72, "beat": "HOOK", "skeleton_i": 0,
             "source_beat_i": [0], "text": "narration of this paragraph",
             "components": ["explainer/Octopus", "explainer/You"], "background": "explainer/Ocean",
             "max_hold_s": 1.9, "caption_pages": [{"t0": 0.11, "t1": 1.5, "text": "A giant Pacific octopus"}]}]}
```

`t0/t1` use the frame-accurate cumulative rounding of F20 (`start_i = round(cum_i * fps) / fps`).

### 5.5 `episodes/<slug>/package.json` (L1's package step writes, besides titles.md/description.md; L3 reads)

```json
{"v": 1, "title_pick": 0, "titles": ["...", "...", "..."], "yt_title": "<= 100 chars",
 "yt_description": "...", "short_caption": "1-2 lines for TikTok/IG", "hashtags": ["#orca", "#ocean"],
 "thumb_pick": "out/<slug>/thumbs/<file>_9x16.jpg", "facts_to_verify": ["..."]}
```

If `package.json` is missing, L3 parses `titles.md` (bold title of the "Pick" row) and `description.md`
(first section) as the pilots format them.

### 5.6 `out/<slug>/qa/gate.json` (L2 writes; operator, L3 read)

```json
{"v": 1, "slug": "...", "at": "...", "verdict": "PASS|FAIL", "warn_count": 1,
 "mp4": "out/<slug>/<slug>_9x16.mp4", "mp4_sha256": "...",
 "checks": {
   "duration":     {"status": "PASS|WARN|FAIL", "value": 74.2, "threshold": ">= 61", "detail": ""},
   "originality":  {"status": "PASS", "value": {"max_run": 6, "max_5gram_share": 0.012, "vs_source_5gram_share": 0.004}},
   "sameness":     {"status": "PASS", "value": {"vs": ["op-..."], "max": {"title": 0.31, "hook": 0.22, "beats": 0.55, "shot_mix": 0.71, "thumb_hamming": 21}}},
   "loudness":     {"status": "PASS", "value": {"I_lufs": -14.1, "true_peak_dbtp": -1.2}},
   "black_frames": {"status": "PASS", "value": []},
   "frozen":       {"status": "PASS", "value": [], "threshold": "no freeze > visual.max_hold_s + 0.5"},
   "missing_kit":  {"status": "PASS", "value": 0, "detail": "magenta pixel share in sampled frames"},
   "captions":     {"status": "WARN", "value": [{"t": 31.2, "issue": "page overlaps subject bbox"}]},
   "safe_area":    {"status": "PASS", "value": []},
   "hook":         {"status": "PASS", "value": {"words": 11, "first_speech_s": 0.2}},
   "disclosure":   {"status": "PASS", "detail": "AI-voice line present in package"},
   "variant":      {"status": "PASS", "value": {"pace.rehook_s": 8.7}}
 },
 "sheets": {"sbs": "out/<slug>/qa/sbs.jpg", "stills": "out/<slug>/qa/stills.jpg"}}
```

Verdict is FAIL if any check is FAIL. WARN never blocks but is shown to the reviewer.

### 5.7 `out/<slug>/qa/fingerprint.json` (L2 writes for every gated episode; L2 reads past ones)

```json
{"v": 1, "slug": "...", "title": "...", "hook": "first narration sentence", "topic": "pistol shrimp",
 "beat_seq": ["HOOK", "STAKES", "RUNG", "RUNG", "TURN", "PEAK", "TWIST", "STINGER"],
 "shot_mix": {"explainer/Ocean": 12, "explainer/Stat": 4}, "thumb_dhash": "16-hex", "cover_dhash": "16-hex",
 "source_id": "...", "hook_code": "H6"}
```

### 5.8 `out/<slug>/qa/review.json` (the operator writes, following `pipeline/qa/REVIEW_PROMPT.md`; L3 reads)

```json
{"v": 1, "slug": "...", "at": "...", "round": 1, "verdict": "PASS|FIX|REJECT",
 "viewer_score": 82, "scores": {"hook": 8, "clarity": 8, "pacing": 7, "visual": 8, "vs_source": "same|better|worse"},
 "must_fix": [{"t": 12.4, "scene_id": "p04", "issue": "...", "fix": "..."}], "nice_to_have": ["..."],
 "files_viewed": ["out/<slug>/qa/sbs.jpg", "out/<slug>/qa/stills.jpg"], "gate_sha": "sha256 of gate.json",
 "tokens_estimate": 60000}
```

PASS needs `viewer_score >= 75`, no `must_fix`, and `vs_source` not `worse`. FIX means one fix round:
the operator writes `episodes/<slug>/review_notes.md` and runs `studio-make --slug <slug> --from review
--review-notes episodes/<slug>/review_notes.md`, then gate and review again (round 2, final).

### 5.9 `out/<slug>/publish/captions.json` (L3 writes)

```json
{"v": 1, "slug": "...", "youtube": {"title": "...", "description": "...", "tags": ["..."]},
 "tiktok": {"text": "..."}, "instagram": {"text": "..."},
 "disclosure_line": "Narration: synthetic AI voice (Kokoro TTS). Animation: original 2D vector art."}
```

The disclosure line is appended to every platform's text if missing. Limits enforced: YouTube title <= 100,
description <= 5000; Instagram <= 2200 chars and <= 30 hashtags; TikTok <= 2200 chars. `#shorts` on YouTube.

### 5.10 `data/posts.jsonl` (L3 writes; L4, L5 read)

```json
{"v": 1, "at": "...", "post_key": "op-20261102-a-pistol-shrimp:youtube", "slug": "...", "platform": "youtube",
 "source_id": "...", "experiment_id": "EXP-003 ?", "arm": "control ?",
 "mode": "draft|auto", "dry_run": false, "status": "dry_run|draft|scheduled|sending|published|failed|missed|deleted",
 "buffer_channel_id": "...", "buffer_post_id": "... ?", "scheduled_at": "...", "published_at": "... ?",
 "external_id": "YouTube video id / IG media id / TikTok id ?", "external_url": "?",
 "title": "...", "caption_sha256": "...", "video_sha256": "...", "duration_s": 74.2, "error": "?"}
```

Key = `post_key`. Manual posts (pilots posted by hand) may be added with `"mode": "manual"` by
`python -m pipeline.publish.post --record-manual <slug> <platform> <external_url>` so analytics covers them.

### 5.11 `data/metrics.jsonl` (L4 writes)

```json
{"v": 1, "at": "...", "post_key": "...", "slug": "...", "platform": "youtube", "external_id": "...",
 "window": "24h|48h|7d|28d", "age_h": 49.5,
 "source": "yt_analytics|yt_data|ig_graph|tiktok_csv|tiktok_screenshot",
 "views": 0, "engaged_views": "?", "likes": 0, "comments": 0, "shares": 0, "saves": "?", "subs_gained": "?",
 "avg_view_s": 0.0, "avg_view_pct": 0.0, "watch_time_min": 0.0, "reach": "?", "viewed_vs_swiped_pct": "?",
 "retention": {"x": [0.01, 0.02], "watch_ratio": [1.0, 0.93], "relative": [0.51, 0.49]} ,
 "derived": {"hold_3s": 0.71, "hold_50pct": 0.38, "completion": 0.22},
 "raw_file": "data/raw/<post_key>-<window>.json ?", "error": "?"}
```

`retention` is null where the platform gives no curve (Instagram API, most TikTok imports). `x` is
`elapsedVideoTimeRatio`; `watch_ratio` is `audienceWatchRatio`; `relative` is `relativeRetentionPerformance`.
`derived.hold_3s` = watch_ratio interpolated at `3 / duration_s`.

### 5.12 `data/heatmaps/<video_id>.json` (L4 writes)

```json
{"v": 1, "video_id": "...", "fetched_at": "...", "duration_s": 599, "status": "ok|none|blocked|error",
 "points": [{"start": 0.0, "end": 5.99, "value": 1.0}], "error": "?"}
```

### 5.13 `data/alignments.jsonl` (L4 writes)

```json
{"v": 1, "at": "...", "kind": "own|source", "post_key": "... ?", "video_id": "...", "slug": "... ?", "window": "7d",
 "curve": "retention|heatmap", "duration_s": 74.2,
 "scenes": [{"scene_id": "p04", "beat": "RUNG", "skeleton_i": 3, "t0": 9.1, "t1": 14.9,
             "ret0": 0.66, "ret1": 0.58, "drop": 0.08, "drop_per_s": 0.014, "z": 1.9, "rel_mean": 0.47,
             "components": ["explainer/Stat"], "line": "narration text"}],
 "top_drops": [{"t": 12.4, "scene_id": "p04", "beat": "RUNG", "drop_per_s": 0.03, "caption": "page text at t"}],
 "summary": {"hold_3s": 0.71, "worst_beat": "TURN", "best_beat": "HOOK"}}
```

### 5.14 `data/experiments.jsonl` (L4 writes; L1 reads assignments via the CLI; L5 reads)

Row types (key `experiment_id`, plus `slug` for assignments):

```json
{"v": 1, "type": "experiment", "experiment_id": "EXP-003", "dimension": "hook|structure|visual",
 "variable": "hook.type", "control": "source", "treatment": "H6", "hypothesis": "...",
 "primary_metric": "youtube.derived.hold_3s", "secondary": ["youtube.avg_view_pct", "youtube.views@7d"],
 "min_n_per_arm": 6, "max_n_per_arm": 10, "status": "running|decided|aborted", "opened_at": "..."}
{"v": 1, "type": "assignment", "experiment_id": "EXP-003", "slug": "...", "date": "2026-11-02", "slot": "a", "arm": "control"}
{"v": 1, "type": "result", "experiment_id": "EXP-003", "n": {"control": 6, "treatment": 6},
 "medians": {"control": 0.62, "treatment": 0.70}, "paired_wins": "5/6", "effect": 0.08,
 "decision": "adopt|reject|inconclusive|extend", "notes": "..."}
{"v": 1, "type": "promotion", "experiment_id": "EXP-003", "target": "rules|playbook|template|kit|prompt",
 "key": "hook.type", "value": "H6", "proposal": "data/proposals/2026-11-16-EXP-003.patch ?",
 "status": "overlay_applied|proposed|repo_applied|declined"}
```

Design rules: one running experiment at a time (one variable); all other variables come from `rules.json`;
arms alternate by slot and day (even local day: A = control, B = treatment; odd day: swapped) so slot time is
balanced; decision at `min_n_per_arm` (extend to `max_n_per_arm` if inconclusive): **adopt** if the treatment
median of the primary metric beats control by >= 10 % relative **and** the treatment wins >= 2/3 of same-day pairs
**and** no secondary metric is worse by > 15 %; **reject** if control wins by the same rule; otherwise
**inconclusive** at max n (keep control). Views are a secondary metric only (topic noise dominates them).

### 5.15 `data/learned/rules.json` (L4 writes; L1 reads into every prompt; L2 reads thresholds)

```json
{"v": 1, "updated_at": "...", "defaults": {"hook.type": "source", "hook.max_words": 12, "structure.skeleton": "source",
 "pace.rehook_s": 9, "visual.max_hold_s": 3.0, "visual.cover": "scale", "visual.shot_mix": "balanced"},
 "notes": ["short learned statements with evidence ids, max 12"],
 "history": [{"experiment_id": "EXP-003", "key": "hook.type", "old": "source", "new": "H6", "at": "..."}]}
```

If the file is missing, L1 uses the same defaults (they are also in `pipeline/ops/config.default.json`).

### 5.16 `data/sources.jsonl` (L1 writes)

```json
{"v": 1, "at": "...", "source_id": "...", "url": "...", "status": "picked|annotated|used|rejected|unavailable",
 "slug": "... ?", "reason": "?", "score": 7.42}
```

"Unused" = no row with status `used`, `rejected` or `unavailable` (latest row per `source_id`). `picked` that is
older than 24 h without `used` counts as unused again (a crashed make).

### 5.17 `data/killrule.json` (L4 writes; L5 acts)

```json
{"v": 1, "at": "...", "n_videos": 30, "target_views_7d": 10000, "median_views_7d": 4200,
 "first10_median": 2100, "last10_median": 7800, "theil_sen_slope_per_video": 190.0,
 "verdict": "insufficient|continue|extend|stop", "extended_once": false, "explanation": "..."}
```

Rule: only YouTube rows with `window: "7d"` count, one per published video. `n < 30` -> `insufficient`.
`median >= 10000` -> `continue`. Else if `last10_median >= 5000` and slope > 0 and not yet extended -> `extend`
(re-check after 15 more videos). Else -> `stop`. Re-evaluated after every 5th new 7-d row once n >= 30.

### 5.18 `data/operator/state.json` (L5's `pipeline.ops.state` writes; only the operator and `pipeline/ops/*` touch it)

```json
{"v": 1, "session": {"started_at": "...", "last_resume_at": "...", "heartbeat_at": "...", "tmux": "studio-op"},
 "paused": false, "pause_reason": "?",
 "crons": [{"name": "tick", "schedule": "*/20 * * * *", "id": "session cron id ?"}],
 "jobs": {"20261102-a-make": {"type": "make", "slug": "op-...", "due_at": "...", "status": "pending|running|done|failed|skipped",
          "attempts": 1, "pid": 12345, "started_at": "...", "finished_at": "?", "log": "~/studio/logs/operator/<job_id>.log",
          "exit_code": "?", "next": ["20261102-a-review"]}},
 "budget": {"week": "2026-W45", "weighted_tokens": 0, "videos": 0, "operator_tokens_estimate": 0},
 "experiment": {"active": "EXP-003 ?"},
 "counters": {"published": {"youtube": 0, "tiktok": 0, "instagram": 0}, "consecutive_failed_slots": 0}}
```

Written atomically (`.tmp` + `os.replace`) under `flock("state")`.

### 5.19 `data/operator/config.json` (human-editable switch; `pipeline/ops/config.default.json` holds defaults)

```json
{"v": 1, "tz": "America/Chicago", "paused": false,
 "mode": {"youtube": "draft", "tiktok": "draft", "instagram": "draft"},
 "disclosure_ok_auto": {"youtube": false, "tiktok": false, "instagram": false},
 "slots": [{"slot": "a", "make_at": "06:30", "post_at": "11:30"}, {"slot": "b", "make_at": "08:45", "post_at": "18:30"}],
 "metrics_windows_h": [48, 168], "learning": {"weekday": "MON", "at": "07:30"},
 "budget": {"weighted_tokens_per_video": 2500000, "weighted_tokens_per_week": 40000000,
            "operator_tokens_per_day_estimate": 1500000, "max_fix_rounds": 1, "max_make_hours": 3},
 "sameness": {"last_n": 10}, "kill_rule": {"after_videos": 30, "target_views_7d": 10000},
 "notify": {"human_file": "data/operator/HUMAN.md"}}
```

`mode.<platform> = "auto"` takes effect only if `disclosure_ok_auto.<platform>` is also true (section 8.5). Only
the human flips either, by editing the file or with `scripts/operator_ctl.sh mode <platform> auto`.

## 6. L1 make

### 6.1 CLI

```
studio-make --source <url|id|auto> [--niche explainer] [--slot a|b] [--date YYYY-MM-DD]
            [--experiment EXP-003:treatment] [--variant key=value ...] [--review-notes path]
            [--review-rounds N] [--budget-tokens N] [--dry-run-claude] [--from STEP | --steps a,b]
studio-make --slug op-... --from review --review-notes episodes/<slug>/review_notes.md
python -m pipeline.sources pick --niche explainer [--exclude id,...] [--json]    # prints the pick, writes nothing
python -m pipeline.sources annotate <source_id>                                   # transcript + corpus annotation
python -m pipeline.sources skeleton <source_id> --out episodes/<slug>/source.json
```

`--source auto` = `pick`, then `annotate` if `research/corpus/explainer/<id>.md` and `.../auto/<id>.md` are both
missing, then `skeleton`, then the normal steps. The slug is derived (`op-<date>-<slot>-<topic>`); `--slot` and
`--date` default to the next empty slot. `--experiment` reads the variable and value of that arm from
`data/experiments.jsonl`; `--variant` overrides individual keys; both end up in `variant.json`. Steps unchanged
(`script, tts, shots, storyboard, review, render, package, thumbs, collect`), plus a `source` step before `script`.

### 6.2 `pipeline/sources.py`

- Candidates: `research/library/videos/*.json` with `niche == explainer` and role `outlier`, plus
  `research/library.jsonl` rows `type == video`, `niche == explainer`, `outlier_score >= 3.0` (long) or `>= 1.5`
  (short/tiktok), `views >= 300000`.
- Drop: used/rejected/unavailable sources (5.16), titles that are only hashtags or memes, sources whose topic matches
  any of the last 10 published fingerprints (`topic` equal or title Jaccard >= 0.5).
- Score: `log10(views) + 1.5*log10(outlier_score) + kit_fit + 0.5*is_short + 0.3*has_transcript + 0.3*has_corpus`.
  `kit_fit` from `pipeline/sources_kit_fit.json` (keyword -> kit component, weight; e.g. `orca -> explainer/Orca, 1.0`;
  topics with no component get 0 and still qualify if the subject can be one simple inline silhouette). Ties
  break on `source_id`. Deterministic, no LLM.
- Annotate (Spark, niced, `flock("ytdlp")`): subtitles via `yt-dlp --skip-download --write-auto-subs`; if none,
  audio download into `~/studio/refs/explainer/` and faster-whisper `-t 4` under `flock("render")`; transcript ->
  `research/corpus/explainer/auto/raw/<id>.txt`; then `claude -p` with `pipeline/prompts/annotate_explainer.md`
  writes `auto/<id>.md` (same table format as the hand-made corpus files) and `auto/<id>.index.json` (one
  INDEX.json-shaped entry incl. `beat_sequence`). Never edits `INDEX.json`. A YouTube bot-block or failed download
  -> `sources.jsonl` status `unavailable`, exit 4 if no other candidate.
- Skeleton: maps the source beats onto the PLAYBOOK 1b Shorts skeleton (S1-S7) for 65-85 s, writes `source.json`.

### 6.3 Prompt `pipeline/prompts/script_explainer_source.md`

Placeholders: `{topic} {slug} {source_json} {skeleton_table} {hook_directive} {variant_directives} {learned_rules}
{pacing}`. Same hard rules as `script_explainer.md`, plus: the source is reference #1 in `references:` with a beat
alignment table against the source's beat timestamps; 1-2 more corpus neighbours; never paraphrase a source line;
runtime 65-85 s (never under 61 s); originality check runs against the source transcript too.

### 6.4 Unattended-safety fixes (must land; each removes its xfail)

| Id | File | Fix (from CODE_REVIEW_FINDINGS) |
|---|---|---|
| F01 | make.py | `claude()` returns the exit status and parsed JSON; non-zero -> `Fail` (exit 5 on auth errors). Move the old output aside before the call; success requires a new mtime and a changed hash |
| F02 | make.py | store `narration_sha256` in `shots.json` (`_script_sha`); replan when it differs; `--rewrite`/`--script` imply `--reshot` |
| F03 | auto.py + make.py | write `storyboard.json.tmp`, zod-validate it, `os.replace` on PASS; make pulls only after PASS |
| F04 | make.py | snapshot `shots.json` + `storyboard.json` before each review round; on `Fail` restore, rebuild, log `review round N rejected`, continue to render |
| F05 | auto.py | resolve anchors only under time keys; anchor grammar `^@[\w'*-]+(#\d+)?(\.end)?([+-][\d.]+)?$`; bad `#n` -> `AnchorError` |
| F06 | make.py | `pull()` uses `check=True`, one retry, then compares `sha256sum` local vs remote (no-op in local mode) |
| F07 | spark_sync.sh + make.py | generic syncs exclude `episodes/*/{shots.json,script.md,titles.md,description.md,thumbs.json,package.json}` and the Spark-owned list; make pushes its own episode dir explicitly |
| F08 | spark_sync.sh + auto.py | npm step under `flock render.lock`; `zod_validate` returns `ok=False` on the Spark or with `STUDIO_REQUIRE_ZOD=1` when zod is missing |
| F25 | spark_sync.sh | protect filters from `spark_owned.txt` for `--delete` |
| F26 | spark_sync.sh | exclude `/episodes/*/audio/` from the push (plus `--update` for the rest) |
| F27 | spark_render.sh, thumbs_render.sh | sync with `SKIP_NPM=1`; npm inside the same `flock` as the render |
| F28 | spark_render.sh | `CONC` default 4, cap 4, warn when clamped |
| F29 | spark_render.sh | `setsid` + `trap 'kill -- -$PGID' EXIT HUP INT TERM`, render with `9>&-`; Mac side uses `ssh -tt` |

Also: local mode (1.2), code lock (1.4), `make_status.json` (5.3), `beatmap.json` (5.4), `package.json` (5.5),
`--review-notes` passed into `review.md` as `{review_notes}`, a per-video budget check before every claude step
(exit 3 when `usage_total.weighted_tokens` would exceed `--budget-tokens`).

### 6.5 Acceptance

`python3 -m unittest discover -s tests` with the F01-F08 and F25-F29 xfail markers removed and passing;
`studio-make --source auto --dry-run-claude` on the Spark picks a source, writes `source.json` and stops cleanly
before the script step; one real end-to-end make on the Spark produces an MP4 >= 61 s plus all files in 5.1-5.5,
and its contact sheet has been looked at.

## 7. L2 gate

### 7.1 CLI

```
python -m pipeline.qa.gate <slug> [--last-n 10] [--source-frames auto|none] [--json]
python -m pipeline.qa.fingerprint <slug>             # rebuild one fingerprint (also run by gate)
python -m pipeline.qa.sheet <slug>                   # side-by-side sheet only
```

Runs on the Spark (ffmpeg `-threads 2`, niced). Exit 0 on PASS, 6 on FAIL, 1 on error.

### 7.2 Checks (thresholds are constants in `pipeline/qa/gate.py`, overridable by `rules.json` where noted)

| Check | Method | FAIL | WARN |
|---|---|---|---|
| duration | ffprobe | < 61.0 s | > 90 s |
| originality | `scripts/originality_check.py` on the narration against `research/corpus` (recursive, includes `auto/`) and `research/library/transcripts`, plus a direct comparison with the source transcript | checker FAIL, or vs-source 5-gram share >= 1 % or a shared run >= 6 words | |
| sameness | vs fingerprints of the last N published slugs (posts.jsonl, status published/scheduled/draft) | title char-trigram cosine >= 0.6; hook cosine >= 0.6; same `topic` within last 10; thumb dHash Hamming <= 8 | beat_seq normalized edit distance <= 0.1 vs 3+ of the last N (templated storyline risk); shot_mix cosine >= 0.95 |
| loudness | `ffmpeg ebur128` | I outside -14 +-1.5 LUFS, true peak > -0.5 dBTP | true peak > -1.0 |
| black / blank | `blackdetect d=0.25` and near-uniform frames | any black run > 0.5 s not marked intended in shots | |
| frozen | `freezedetect n=0.003` | freeze > `visual.max_hold_s` + 0.5 s | |
| missing kit | magenta (#FF00FF +- 8) share on 1 fps sampled frames | > 0.2 % of any frame | |
| captions | from `beatmap.json` caption pages and storyboard layer boxes: overlap of the caption box with subject boxes, red on stopwords, pages > 4 words | | any (reviewer decides) |
| safe area | caption or text box below 66 % height or within 5 % of the edges | text box below 80 % | below 66 % |
| hook | words of the first sentence, first speech time | first speech > 1.0 s | words > `hook.max_words` |
| disclosure | AI-voice line present in package.json/description.md | missing | |
| variant | measured value of each variable in `variant.json` | | off by > 20 % |

### 7.3 Sheets

`sbs.jpg`: two rows per beat of the skeleton: our frame at the beat midpoint over the source frame at the
matched source beat midpoint (source frames from `~/studio/refs/explainer/<id>.mp4` or its `_frames/` folder; if
the source video is not on disk and cannot be fetched, the source row shows the beat label only). Reuse
`scripts/side_by_side.sh` logic; do not edit that script (read-only), call it or reimplement in `pipeline/qa/sheet.py`.
`stills.jpg`: 12 frames, including frame 0 (the cover) and the last frame (loop check).

### 7.4 `pipeline/qa/REVIEW_PROMPT.md`

The prompt the operator follows for the one combined LLM review per round: inputs (`sbs.jpg`, `stills.jpg`,
`script.md`, `source.json`, `gate.json` WARN lines, the last 3 published `stills.jpg` for sameness by eye), the
STUDIO.md section 3 rubric condensed to a checklist, a "first-time viewer" pass (would you swipe at 1 s / 3 s /
the turnstile?), and the exact `review.json` output (5.8). Hard cap: <= 6 images read per round.

### 7.5 Acceptance

Gate run on the five existing pilot cuts (copy as fixtures by slug, no edits): they PASS duration, loudness,
missing-kit; a synthetic fixture with a 1 s black gap, a 55 s cut and a copied 9-word source line each FAIL with the
right check; a sheet has been opened and looked at.

## 8. L3 publish

### 8.1 CLI

```
python -m pipeline.publish.buffer channels [--dry-run]             # list org + channel ids (for the human to fill .env)
python -m pipeline.publish.buffer introspect                       # saves data/buffer_schema.json
python -m pipeline.publish.post <slug> --slot-at <ISO> [--platforms youtube,tiktok,instagram] [--mode draft|auto] [--dry-run]
python -m pipeline.publish.post --record-manual <slug> <platform> <url>
python -m pipeline.publish.status [--all-open]                     # refresh open posts, append status rows
python -m pipeline.publish.schedule next --date YYYY-MM-DD         # slot datetimes from config (used by L5)
```

### 8.2 Preconditions (post.py refuses with exit 6 otherwise)

`gate.json.verdict == PASS`, `review.json.verdict == PASS`, `gate.json.mp4_sha256 == sha256(mp4)`,
`review.json.gate_sha` matches the current `gate.json`, no existing non-failed row for the `post_key`
(idempotent), `config.paused == false`.

### 8.3 Buffer client

- GraphQL over HTTPS POST to `BUFFER_API_URL`, `Authorization: Bearer $BUFFER_API_KEY`. All operations live in
  `pipeline/publish/queries.graphql`. **Before coding the mutations, L3 runs `introspect` (or reads Buffer's API
  docs) and pins the actual field names** (organization and channel listing, post creation with a video asset,
  draft vs queue/schedule, post status, the published post's external link). Don't guess field names; if a
  needed capability is missing (for example YouTube title or TikTok video via the API), record it in
  `pipeline/publish/README.md` and fall back to draft-only for that platform.
- Draft mode: create a Buffer **draft** per platform with the intended `scheduled_at` stored in our ledger (and on
  the draft if the API allows it). A human approves in Buffer. Auto mode: create a scheduled post at the slot time.
- Rate limits and retries: exponential backoff on 429/5xx (max 4 tries), no retries on 4xx other than 429.
  Never log the key (`env.redact`).

### 8.4 Temporary public video URL (`pipeline/publish/host.py`)

```python
with hosted(mp4_path, ttl_s=1800) as url:   # https://<random>.trycloudflare.com/<32-hex token>/<slug>.mp4
    ...create posts..., wait until Buffer reports each asset processed (or ttl)
```

- Local server bound to `127.0.0.1` on a random port that serves **only** that one file at an unguessable token
  path (404 for anything else, no directory listing, Range support, GET/HEAD only).
- `PUBLIC_HOST_MODE=cloudflared`: `cloudflared tunnel --url http://127.0.0.1:<port> --no-autoupdate` (quick tunnel, no
  account), parse the `trycloudflare.com` URL from its log, check it with a HEAD request through the tunnel,
  kill the process group on exit. `static`: `PUBLIC_BASE_URL` + token path.
- The context manager always tears down the tunnel and server, including on exceptions; ledger row records
  `host: {mode, opened_at, closed_at}` but never the URL after close.

### 8.5 Captions and disclosure

`captions.py` builds 5.9 from `package.json` (fallback: titles.md/description.md). The disclosure line is on every
platform. Platform AI toggles (YouTube "altered or synthetic content", TikTok "AI-generated content", Instagram
"AI info") may not be settable through Buffer: L3 documents which are. If a toggle is not settable, that platform
stays in draft mode (the human sets the toggle on approval) until the human sets `disclosure_ok_auto.<platform>`
after checking. Made-for-kids: No. Never add library music (the Shorts > 60 s claimed-content block).

### 8.6 Acceptance

Without `.env`: `post --dry-run` on a gated fixture writes three `dry_run` rows with full payloads and a
captions.json; `host.py` serves a test file through a real quick tunnel and closes it (HEAD 200, then
unreachable); unit tests for caption limits and idempotency. With the human's key: `channels` lists the three
channels and one real draft reaches Buffer (human confirms in the Buffer app).

## 9. L4 analytics and learning

### 9.1 CLI

```
python -m pipeline.analytics.youtube auth            # human-run, one time; prints a consent URL (see 9.2)
python -m pipeline.analytics.collect --due | --post-key K --window 48h|7d [--dry-run]
python -m pipeline.analytics.tiktok_import <file.csv> [--post-key K]
python -m pipeline.analytics.heatmap <video_id|url> [--force]
python -m pipeline.analytics.align <slug> --window 7d | --source <video_id>
python -m pipeline.analytics.experiments assign --date YYYY-MM-DD --slot a|b    # prints {"experiment_id","arm","variables"} or {}
python -m pipeline.analytics.experiments open --dimension hook|structure|visual  # proposes the next one from LEARNING (operator confirms)
python -m pipeline.analytics.experiments decide [--dry-run]
python -m pipeline.analytics.learning --week 2026-W46
python -m pipeline.analytics.killrule
```

### 9.2 YouTube (installed-app OAuth)

- Scopes: `https://www.googleapis.com/auth/yt-analytics.readonly` and `https://www.googleapis.com/auth/youtube.readonly`.
- `auth`: loopback flow on the Spark at `127.0.0.1:8765`; the human runs `ssh -L 8765:127.0.0.1:8765 dgx-spark`
  from the Mac, opens the printed URL in their own browser and consents; the token goes to `YT_TOKEN_FILE` (600).
  Agents never run the consent.
- Per video at each window: Data API `videos.list part=statistics,contentDetails` (views, likes, comments,
  duration) and Analytics `reports.query ids=channel==MINE`, `filters=video==<id>`:
  (a) totals `views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,likes,shares,subscribersGained`
  (+ `engagedViews` if the API accepts it), (b) retention `dimensions=elapsedVideoTimeRatio`,
  `metrics=audienceWatchRatio,relativeRetentionPerformance`. Analytics data lags 1-3 days: an empty answer at 48 h
  is retried every 12 h up to 96 h, and the row is written with `age_h` as collected.

### 9.3 Instagram (Graph API)

Resolve `external_id` by listing `/{IG_USER_ID}/media?fields=id,permalink,timestamp,caption,media_product_type` and
matching the Buffer post (permalink if Buffer returns it, else timestamp +- 15 min and caption prefix). Insights
`/{media-id}/insights` for Reels metrics (views, reach, likes, comments, shares, saved, total_interactions,
average watch time). Metric names change between Graph versions: request them one by one, keep what returns,
record unknowns in `raw`.

### 9.4 TikTok (manual)

The human drops TikTok Studio screenshots or a CSV into `data/inbox/tiktok/` on the Spark. CSV columns (header
required): `tiktok_url_or_id,captured_at,views,likes,comments,shares,saves,avg_watch_s,full_watch_pct,new_followers,retention`
with `retention` as `s:pct;s:pct;...` (optional). For screenshots, the operator reads the image and writes that
CSV following `pipeline/analytics/TIKTOK_IMPORT.md`, then runs `tiktok_import`. Processed files move to
`data/inbox/tiktok/done/`. Rows carry `source: tiktok_csv|tiktok_screenshot`.

### 9.5 Heatmap (Most replayed)

`yt-dlp -J --skip-download` on the Spark under `flock("ytdlp")`, `nice -n 10`, one process, with
`--cookies $YTDLP_COOKIES_FILE` if set; read `heatmap` (list of start, end, value). Spark per-video `-J` is often
bot-blocked: then `status: blocked` and no retry for 7 days. Used for (a) each source at pick time (L1 may call the
CLI) and (b) weekly for the top-20 explainer outliers of `research/daily` to learn which source beats hold
attention (`align --source`, alignment `kind: source`).

### 9.6 `align.py`

Input: retention (or heatmap) curve + `beatmap.json`. Convert `x` to seconds (`x * duration_s`), smooth with a
3-point median, compute per-scene `ret0/ret1/drop/drop_per_s`, z-score of `drop_per_s` against the episode's own
scenes, `rel_mean` from `relativeRetentionPerformance`, top 3 drops with the caption page on screen at that time.
Ignore the first 2 % (hook settling) and the last 3 % (end spike from loops) for drop ranking, but report them.

### 9.7 Learning and fold-in

- `learning.py` (weekly): reads metrics, alignments, experiments, fingerprints; writes `data/learning/<week>.md`
  and copies it to `data/learning/LEARNING.md`. Sections: scoreboard (per video: views 48 h / 7 d per platform,
  hold_3s, avg_view_pct, source, arm), beat-level table (median drop_per_s by beat label and by component), source
  vs ours (did our version keep the source's best beat?), experiment status, kill-rule status, 3 candidate next
  experiments ranked by the largest beat-level loss. Deterministic text; the operator may add a short "Operator
  notes" section at the end.
- `experiments decide` applies the rule in 5.14. On **adopt**: update `data/learned/rules.json` at once (overlay,
  used by the next make) and write a `promotion` row; for durable changes write a patch to
  `data/proposals/<date>-<exp>.patch` against PLAYBOOK, templates, prompts or kit files (L4 generates the text; it
  never applies it). A Mac session applies proposals after review (`scripts/pull_ops.sh --proposals` lists them),
  commits, and syncs; then marks `repo_applied`.

### 9.8 Acceptance

Unit tests with recorded API fixtures (no network): collect -> metrics rows; align on the octopus beatmap with a
synthetic curve -> drop lands in the expected scene; experiments decide on synthetic data hits adopt, reject and
inconclusive; killrule on 30 synthetic rows hits each verdict. Without `.env`, `collect --due` exits 0 in
dry-run and lists what it would fetch.

## 10. L5 operator

### 10.1 Files

- `OPERATOR.md` (repo root): the operator's standing instructions. Contents: role and limits (BRIEF rules, no
  credentials, never flip `mode`/`disclosure_ok_auto`, never apply proposals, never edit Mac-owned files on the
  Spark), the resume protocol, the tick procedure, job handlers (which CLI, success criteria, what to read),
  review procedure (REVIEW_PROMPT.md), escalation (HUMAN.md), budget rules, kill-rule handling.
- `scripts/operator_tmux.sh start|attach|resume|rotate|stop|status`: tmux session `studio-op` on the Spark,
  `cd ~/studio/app`, `export STUDIO_LOCAL=1 TZ=America/Chicago CUDA_VISIBLE_DEVICES=""`,
  `source scripts/spark_env.sh`, then `claude` with the opening prompt "Read OPERATOR.md and run the resume
  protocol." `resume` uses `claude --continue` if the last session is < 24 h old, else a fresh session. `rotate`
  stops the session cleanly between jobs and starts a fresh one. Works from the Mac via `ssh -t dgx-spark`.
- `scripts/operator_watchdog.sh` (system cron every 15 min, installed by `scripts/install_operator_cron.sh`, which
  keeps other users' crontab lines like the existing research installer): if `state.heartbeat_at` is > 45 min
  old and a job is overdue, sends the tick prompt with `tmux send-keys`; if the tmux session is gone, runs
  `operator_tmux.sh resume`. Installing the cron line is a human step.
- `scripts/operator_settings.example.json`: a recommended Claude Code permission allowlist for unattended runs
  (python -m pipeline.*, studio-make, scripts/*.sh, ffmpeg/ffprobe, read-only git). It is an example only; the
  human decides whether to install it. No lane changes permission settings.
- `scripts/operator_ctl.sh pause|unpause|mode <platform> draft|auto|status`: edits `data/operator/config.json` for the human.
- `scripts/pull_ops.sh [--proposals]` (Mac): rsync the Spark-owned paths in `spark_owned.txt` except media
  (`--exclude '*.mp4' --exclude '*.wav'`), into the Mac repo, for commits and review.
- `pipeline/ops/`:
  - `state.py`: load/save (5.18), heartbeat, job transitions.
  - `due.py`: pure function `(config, state, posts, metrics, now) -> [jobs due]`; creates make jobs for today's
    slots, metrics jobs at `published_at + 48 h / 7 d`, weekly learning, killrule triggers; idempotent by job_id.
  - `run.py <job_id>`: runs a deterministic job detached (`setsid nohup`, log to `~/studio/logs/operator/<job_id>.log`,
    under `flock("make")` for makes), updates state on exit. The operator never blocks a tool call for more than
    ~2 min; it starts jobs with `run.py` and checks them on the next tick.
  - `budget.py`: sums `make_status.usage_total` per ISO week + the operator's own estimate; `check(kind)` -> ok,
    soft (skip optional work), hard (exit 3).

### 10.2 Resume protocol (first thing in every session, and after any compaction)

1. Read `OPERATOR.md`, `data/operator/config.json`, `data/operator/state.json`, the tail of `data/operator/journal.md`.
2. **Re-arm schedules first**: list session crons; create the missing ones (`tick` every 20 min with the prompt
   "operator tick"; one-shot wake-ups for the next make and post times). Write their ids to `state.crons`.
3. Reconcile: for each job `running`, check its pid and `make_status.json`/log; mark done/failed accordingly. A
   make that died mid-step resumes with `--from <step>` (allowed once).
4. Run `python -m pipeline.ops.due` and handle due jobs in order: overdue publish, review, make, metrics, learning.
5. Update `heartbeat_at`, append 1-3 lines to `journal.md` (what ran, what is next).

### 10.3 Tick procedure

`due` -> for each due job: deterministic jobs via `run.py`; LLM jobs (review, TikTok screenshot transcription,
experiment opening, failure triage, weekly operator notes) done in-session. After each job: state + journal.
Tick ends in < 10 min of session time.

### 10.4 Budget caps (defaults in config 5.19)

- Per video: 2.5M weighted tokens across make's claude steps (script, shots, review rounds, package, annotate)
  plus the operator's review estimate. At 80 %: skip optional review rounds. At 100 %: make exits 3; the slot is
  skipped.
- Per week: 40M weighted tokens (14 videos at about 2M plus operator overhead). At 80 %: one video per day; at
  100 %: pause makes until Monday, keep metrics jobs running.
- Wall clock: a make over 3 h is killed (process group) and counts as a failure.

### 10.5 Human-approval switch

`config.mode.<platform>` (draft by default) plus `disclosure_ok_auto.<platform>`; `config.paused` stops new makes
and posts (metrics continue). The operator only reads them. In draft mode the operator writes the drafts' list to
`HUMAN.md` ("approve in Buffer by 11:30") and marks posts `missed` if still unapproved 6 h after the slot.

### 10.6 Kill rule handling

On `killrule.verdict == stop`: set `paused: true`, `pause_reason: kill_rule`, write HUMAN.md with the numbers and
LEARNING.md summary, stop making. `extend`: note it and continue. `continue`: note it.

### 10.7 Acceptance

`due.py` unit tests over a simulated 10-day calendar (makes at slot times, metrics at +48 h / +7 d, Monday
learning, no duplicates after a simulated restart); `operator_tmux.sh start/status/stop` on the Spark; a dry-run
day with fixtures: tick -> make (dry) -> gate (fixture) -> review (fixture) -> publish dry-run -> rows in
posts.jsonl.

## 11. Build order and integration

1. **Hour 0:** L5 commits `pipeline/common/` and `pipeline/ops/config.default.json`. L1 commits
   `scripts/spark_owned.txt` and the sync/render fixes (F25-F29) first: nothing else is safe to test on the Spark
   until a Mac sync cannot clobber Spark output.
2. **In parallel:** L1 (sources, local mode, F01-F08), L2 (gate on existing pilots), L3 (dry-run client, host,
   captions), L4 (collectors with fixtures, align, experiments), L5 (state, due, run, tmux).
3. **Integration (one lane, after all five land):** one dry-run day on the Spark, then one real make + gate +
   review + Buffer draft (with the human's `.env`), then hand the loop to the operator in draft mode.

Each lane commits only its own files, with messages ending in the Co-Authored-By line, and never pushes.

## 12. Risks and open questions

- **Buffer API coverage.** Field names and whether video posts, YouTube titles, TikTok and drafts are supported
  must be confirmed by introspection before L3 codes against them; per-platform fallback is draft-only.
- **AI-disclosure toggles** may not be reachable through Buffer, which keeps that platform in draft mode.
- **YouTube bot-blocking from the Spark** limits yt-dlp per-video metadata, subtitles and heatmaps; the library
  and corpus already hold transcripts for 60+ videos, and cookies are optional and user-supplied.
- **Topic noise vs one-variable tests:** experiments use retention metrics (hold_3s, avg_view_pct), alternate arms
  across slots and days, and treat views as secondary.
- **Templated-content policy (YouTube inauthentic content):** the sameness gate and source rotation keep scripts,
  structures and scenes distinct; beat skeletons repeated 3+ times in the last 10 videos raise a WARN for the reviewer.
- **Context growth** in a long-lived session: state lives in files, and the session is rotated daily at 04:00.
