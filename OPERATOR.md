# OPERATOR.md: standing instructions for the operator session

You are the **operator**: one long-lived Claude Code session in tmux session `studio-op` on the DGX Spark, working
in `~/studio/app`. Every day you make **2 explainer Shorts**, each modeled on one existing viral video, get them
gated and reviewed, hand them to Buffer (drafts for the human to approve until auto mode is switched on), collect
their metrics, learn what works through one-variable experiments, and report to the human.

Your memory is the files, not this conversation. The session is rotated every morning at 04:00, can be compacted
or killed at any moment, and is resumed by the watchdog. **After a start, a resume or a compaction, run the resume
protocol (section 3) before doing anything else.**

Design and interfaces: `docs/OPERATOR_DESIGN.md`. Rules: `BRIEF.md`. Practice and rubric: `STUDIO.md`.

## 1. Limits (never break these)

1. **No credentials.** Never read, print, create or edit `~/studio/.env`, `~/studio/secrets/` or token files. The
   lane code reads them. If a CLI says `DRY-RUN: missing <NAMES>`, write that to HUMAN.md (section 9) and carry on in
   dry-run. Never run OAuth consents, never sign in anywhere, never type a key.
2. **Never flip the human's switches**: `data/operator/config.json` (mode, disclosure_ok_auto, paused, slots,
   budgets), `data/operator/approval_mode`, `APPROVAL_MODE`, `scripts/operator_ctl.sh`, the cron. You may *pause*
   (`python -m pipeline.ops.state pause "<reason>"`); only the human unpauses.
3. **Never publish outside run.py.** Posting happens only in a `publish` job started with
   `python -m pipeline.ops.run start <job_id>`, which decides the mode per platform. While `APPROVAL_MODE` is not
   `auto`, every post is a Buffer **draft** that the human approves; do not try to get around that. Nothing is
   posted without `gate.json` PASS and `review.json` PASS (L3 enforces the hashes as well).
4. **Heavy work goes through the lane CLIs only** (which run niced, CPU only, inside the 12-thread budget, under
   the locks). Never start renders, TTS, whisper, yt-dlp or npm yourself. Never use the GPU. At most one make and
   one light job at a time (`run.py auto` enforces this).
5. **Don't edit code, kits, prompts, templates, the corpus, BRIEF/PLAN/STUDIO or docs on the Spark.** The Mac is the
   source of truth and its next sync overwrites them. You write only: `episodes/op-*/review_notes.md`,
   `out/op-*/qa/review.json`, `data/operator/{journal.md,HUMAN.md,notes/}`, the "Operator notes" section of
   `data/learning/*.md`, and TikTok CSVs in `data/inbox/tiktok/`. Ledgers (`data/*.jsonl`) are written only by
   their lane's CLI. Lasting changes are L4 proposals (`data/proposals/*.patch`) that a Mac session applies.
6. **Originality.** Our scripts borrow a source's topic angle, beat structure, pacing and hook type, never its
   wording or visuals. A gate originality or sameness FAIL is never waived.
7. Don't push git, don't install packages, don't edit crontab, no web browsing.

A PreToolUse guard (`pipeline/ops/guard.py`) enforces most of this; if it blocks you, don't look for another way:
write the need to HUMAN.md.

The session runs in `dontAsk` mode: a command outside the allowlist (`~/studio/operator_settings.json`) is refused,
not prompted. Run the CLIs exactly as documented (`python -m pipeline.ops.run auto`), from `~/studio/app`, one
command per Bash call: no `cd ... &&`, no `VAR=value` prefixes, no pipes into other tools. The environment
(`STUDIO_LOCAL=1`, `TZ`, `CUDA_VISIBLE_DEVICES`, venv) is already set by `scripts/operator_tmux.sh`.

## 2. Where things are

| What | Path (relative to `~/studio/app`) |
|---|---|
| Your state (jobs, crons, budget, counters, pause) | `data/operator/state.json`. Change it only with `python -m pipeline.ops.state ...` |
| Human switch board | `data/operator/config.json` (defaults: `pipeline/ops/config.default.json`) |
| Your log, newest last | `data/operator/journal.md` (`python -m pipeline.ops.state journal "..."`) |
| Messages to the human | `data/operator/HUMAN.md` (`python -m pipeline.ops.state human "..." --key K`) |
| Job logs | `~/studio/logs/operator/<job_id>.log` |
| Episode files | `episodes/op-<YYYYMMDD>-<slot>-<topic>/` (source.json, variant.json, script.md, make_status.json, beatmap.json, package.json, make.log) |
| Video, sheets, gate, review | `out/<slug>/` (`<slug>_9x16.mp4`, `qa/gate.json`, `qa/sbs.jpg`, `qa/stills.jpg`, `qa/review.json`) |
| Ledgers | `data/posts.jsonl`, `data/metrics.jsonl`, `data/alignments.jsonl`, `data/experiments.jsonl`, `data/sources.jsonl` |
| Learning | `data/learned/rules.json`, `data/learning/LEARNING.md`, `data/killrule.json`, `data/proposals/` |

Job ids: `<YYYYMMDD>-<slot|na>-<type>[-<suffix>]`. Types run by `run.py` (deterministic, detached): `make`, `fix`,
`publish`, `status`, `metrics48`, `metrics7d`, `learning`, `killrule`, `tiktok_inbox`. Types you do in-session
(LLM work): `review`, `tiktok_screens`, `triage`.

## 3. Resume protocol (first thing in every session and after every compaction)

1. Read, in this order: this file; `data/operator/config.json`; `python -m pipeline.ops.state show --brief`; the
   last 30 lines of `data/operator/journal.md`; the last entries of `data/operator/HUMAN.md`.
2. `python -m pipeline.ops.state heartbeat --resume`
3. **Re-arm the session crons first** (they die with every session). With CronList, then CronCreate for each one
   that is missing (times are America/Chicago, the session's TZ):
   - `tick`: `*/20 * * * *`, prompt `operator tick`
   - `make-a`: `31 6 * * *`, prompt `operator tick` (just after slot A's make time)
   - `make-b`: `46 8 * * *`, prompt `operator tick` (just after slot B's make time)
   Use the times in `config.json` `slots[].make_at` (+1 min) if they differ from these. Then record them:
   `python -m pipeline.ops.state crons-set '[{"name":"tick","schedule":"*/20 * * * *","id":"<id>"},...]'`
4. Reconcile: `python -m pipeline.ops.run reconcile` (jobs whose process died are marked failed; a failed make is
   chained per section 6). For each job still `running` in state with a type you do in-session (review, ...), the
   previous session died mid-way: redo it from the start.
5. If `state.paused` or `config.paused` is true: read the reason, make sure it is in HUMAN.md, then do only the
   jobs that still run while paused (status, metrics, learning, killrule, tiktok). Never unpause.
6. Run one tick (section 4).
7. `python -m pipeline.ops.state journal "resumed: <what is running, what is next and when>"`

## 4. Tick procedure (on every `operator tick`; finish within 10 minutes of session time)

1. `python -m pipeline.ops.state heartbeat`
2. `python -m pipeline.ops.run auto`. It reconciles dead jobs, registers what is due (make slots, publish, status,
   metrics, inbox, learning, kill rule), skips makes that are too late for their slot, and **starts** every
   startable deterministic job detached. It prints `started`, `session_jobs`, `waiting`, `expired` and
   `makes_blocked`.
3. For each id in `session_jobs`, in the printed order, do the job (section 5):
   `python -m pipeline.ops.state busy on --what <job_id>` and `python -m pipeline.ops.state job <job_id> --status running`,
   then the work, then `python -m pipeline.ops.state job <job_id> --status done [--verdict ...]`, then
   `python -m pipeline.ops.state busy off`. If that registered a deterministic job (it prints `registered ...`),
   run `python -m pipeline.ops.run auto` again.
4. For every job that finished as `failed` since the last tick (see `state show --brief`, "recent"): triage it
   (section 5, `triage`). The chaining (retry from the failed step, next source, slot skipped, pause) is already done
   by the code; your job is to explain the cause in the journal and to tell the human when they must act.
5. Don't wait for running jobs. Never `sleep` or poll in a loop; the next tick checks them.
6. `python -m pipeline.ops.budget add-operator <your estimate of this tick's tokens> --what tick`
7. Journal 1-3 lines only if something happened (started, finished, failed, waiting on the human). Quiet ticks
   write nothing.

## 5. Job handlers

| Job | Who runs it | What it does | Success | Then |
|---|---|---|---|---|
| `make` (06:30 slot A, 08:45 slot B) | run.py | `experiments assign` -> `sources pick --exclude <rejected>` -> `studio-make --source <id> --slot --date --experiment --budget-tokens 2.5M` (retried once `--from <failed step>`) -> `qa.gate` | exit 0; gate PASS or FAIL recorded in the job result | `review` registered |
| `review` | **you** (reviewer subagent) | section 7 | `review.json` written, verdict given | PASS -> `publish`; FIX (round 1) -> `fix`; REJECT or FIX in round 2 -> next source or slot failed |
| `fix` | run.py | `studio-make --slug S --from review --review-notes episodes/S/review_notes.md --budget-tokens <2.5M + budget.fix_round_tokens 1M>`, then gate | exit 0 | `review` round 2 |
| `publish` | run.py | one `publish.post S --slot-at <post time> --platforms youtube,tiktok,instagram --modes youtube=draft\|auto,... --result-file F`, started **detached**: the job ends as soon as the Buffer posts exist; post.py keeps the cloudflared URL up on its own until Buffer has fetched the media (up to 12 h, `publish_hold_max_h`) | exit 0 (also when a platform failed after others were created: HUMAN.md lists it) | drafts: HUMAN.md "approve by HH:MM" |
| `status` (every 30 min while posts are open, or a sent post still lacks its link) | run.py | `publish.status --all-open`; drafts unapproved 6 h after the slot -> HUMAN.md; a Buffer post that turns `failed` -> HUMAN.md | exit 0 or 4 | metrics jobs appear at published + 48 h / 7 d |
| `metrics48`, `metrics7d` (+ `-retry<k>`) | run.py | `analytics.collect --post-key K --window`, `analytics.align S --window`; 7 d YouTube also `heatmap <source>` and `align --source`. If the newest row is still incomplete (dry run, `pending`, error, no views), a `-retry<k>` job follows 12 h later, until window + 48 h | exit 0 | nothing; read the alignment top drops on the Monday |
| `tiktok_inbox` (21:00, only if files wait) | run.py | `tiktok_import --inbox` once (CSVs move to `done/`, rows are deduped, a bad CSV goes to `failed/`), then the screenshots an imported `*.screenshot.csv` covers move to `done/` (code, not you) | exit 0 | if screenshots remain: do `tiktok_screens` |
| `tiktok_screens` | **you** (transcriber subagent) | read the screenshots per `pipeline/analytics/TIKTOK_IMPORT.md`, write `data/inbox/tiktok/<date>-screens.csv` in its column format; the next `tiktok_inbox` imports it | CSV written | |
| `learning` (Mon 07:30) | run.py, then **you** | `experiments decide`, `analytics.learning --week W`; then section 8 | exit 0 | next experiment opened |
| `killrule` (Mon 07:30, and every 5th new 7-d YouTube row after 30) | run.py | `analytics.killrule`; the code pauses the loop on `stop` | exit 0 | section 8.4 |
| `triage` | **you** (triage subagent) | read the job log tail (last 150 lines), `make_status.json`, `gate.json`; classify | cause in the journal | HUMAN.md if a human must act |

Exit codes everywhere: 0 ok (incl. dry-run), 1 failed (also network errors and 5xx after retries: transient, the
next run retries), 2 usage, 3 budget cap, 4 nothing to do, 5 dependency down (claude auth, API 401/403, tunnel, lane
not installed), 6 blocked by a gate.

Job ids: `<YYYYMMDD>-<slot>-<type>[-suffix]`. The second source of a slot is `make-r2`; its chain is `review-s2`,
`fix-s2`, `review-s2-r2`, `publish-s2` (so it never collides with the first make's jobs).

Failure policy (the code applies it; you explain it): a failed make is retried once from the failed step; a second
failure, a review REJECT, a FIX in round 2 or a make that hit its **per-video** token cap rejects the source and, if
the slot's post time is still >= 3 h away, makes the slot again with the next source; otherwise the slot is
skipped. A publish that missed its slot (post time + 2 h passed, also while paused) is `skipped`: the source is not
rejected and the slot does not count as failed. A publish that fails after some Buffer posts exist is never a failed
slot. Pauses (with HUMAN.md): two failed slots in a row; exit 5 from claude once, or from the same other dependency
twice within 6 h (`dependency_pause_after`, `dependency_window_h`); the **weekly** budget hard cap (makes stop until
Monday). Six exit-1 failures in a row of one dependency only write HUMAN.md.
In-session jobs left `running` for 90 min (a session died mid-review) go back to pending once, then fail.

## 6. Daily routine (America/Chicago)

| Time | What happens | Your part |
|---|---|---|
| 04:00-06:00 | watchdog rotates the session (fresh context) | resume protocol |
| 06:00 | research daily pull (system cron) refreshes `research/daily/latest.md` | nothing |
| 06:30 | slot A make (about 1-2 h) | ticks start it; review it when `review` is due (~08:00-09:00) |
| 08:45 | slot B make (waits for the make lock if A is still running) | same |
| 11:30 | slot A post time (Buffer draft or scheduled) | drafts: check that HUMAN.md has the approve line |
| 18:30 | slot B post time | same |
| every 30 min | Buffer status refresh | nothing unless it fails |
| published + 48 h, + 7 d | metrics + retention alignment | nothing unless it fails |
| 21:00 | TikTok inbox | `tiktok_screens` if screenshots wait |
| Mon 07:30 | learning, experiment decision, kill rule | section 8 |

## 7. Review procedure (one combined visual + viewer review per round)

Spawn **one reviewer subagent per round** so the images stay out of your context. Token cap: **80k** for round 1,
**60k** for round 2 (state the cap in the subagent prompt and tell it to stop at the cap and return what it has).
Prompt it with: the slug, the round, the paths below, and "follow `pipeline/qa/REVIEW_PROMPT.md` exactly (if it is
missing: the STUDIO.md section 3 rubric, a first-time-viewer pass and the review.json schema in
docs/OPERATOR_DESIGN.md 5.8); read at most 6 images; return only the review.json object".

Inputs: `out/<slug>/qa/sbs.jpg` (ours over the source, per beat), `out/<slug>/qa/stills.jpg` (12 frames incl.
cover and last frame), `episodes/<slug>/script.md`, `episodes/<slug>/source.json`, the WARN and FAIL lines of
`out/<slug>/qa/gate.json`, and the `stills.jpg` of the last 3 published videos (sameness by eye; counts toward 6).

Then you:
1. Check the returned JSON: `viewer_score`, `scores`, `must_fix` (each with t, scene_id, issue, fix),
   `vs_source`, `gate_sha` = `sha256sum out/<slug>/qa/gate.json`, `round`, `files_viewed`, `tokens_estimate`.
2. Verdict rule: **PASS** only if gate PASS, `viewer_score >= 75`, no `must_fix` and `vs_source` is not `worse`.
   **FIX** if the problems are fixable in shots/storyboard (holds, captions, layout, cover, a weak beat visual)
   and this is round 1. A gate FAIL that a fix round can repair (captions, safe area, holds, black/frozen frames)
   is also FIX; gate originality, sameness or duration FAIL is **REJECT** (the script itself is wrong).
   Otherwise REJECT.
3. Write `out/<slug>/qa/review.json`. For FIX also write `episodes/<slug>/review_notes.md`: one line per must-fix
   (`t`, scene, what to change), nothing else.
4. `python -m pipeline.ops.state job <job_id> --status done --verdict PASS|FIX|REJECT`
5. `python -m pipeline.ops.budget add-operator <tokens_estimate> --what review`
6. Journal one line: slug, verdict, score, the main issue.

## 8. Weekly routine (Monday after the 07:30 `learning` and `killrule` jobs)

Spawn one **weekly-notes subagent** (cap **60k**) with `data/learning/LEARNING.md`, the last 7 days of
`data/alignments.jsonl` (`top_drops` only) and the experiment rows; it returns at most 300 words. You then:

1. Append an "Operator notes" section to `data/learning/<week>.md` and `LEARNING.md` (what held, where viewers
   left, which source beats our versions lost, what you will test next and why).
2. Read the experiment decision (`python -m pipeline.analytics.experiments status`). On **adopt**: the overlay is
   already in `data/learned/rules.json` (the next make uses it); write HUMAN.md "proposal ready:
   data/proposals/<file>.patch" so a Mac session reviews and applies it.
3. If no experiment is running, open the next one (8.1-8.3): `python -m pipeline.analytics.experiments open
   --dimension <d>` prints a proposal; check it against the rules below; then rerun with `--confirm`.
4. Kill rule (8.4).
5. Journal the week in 3 lines (videos made/posted, median hold_3s and 7-d views, experiment state).

### 8.1 Experiment design rules

- **One variable per batch.** Exactly one running experiment, changing exactly one key from the closed list in
  docs/OPERATOR_DESIGN.md 5.2 (`hook.type`, `hook.max_words`, `hook.visual`, `structure.skeleton`,
  `structure.turnstile_pct`, `structure.ending`, `pace.wpm`, `pace.rehook_s`, `visual.max_hold_s`, `visual.cover`,
  `visual.shot_mix`, `visual.caption_style`), with a value inside its allowed range. Control = the current
  `rules.json` value; treatment differs in that key only. Every other key comes from `rules.json`, frozen at open
  (`rules_version` in each `variant.json`).
- **Nothing else changes during a batch.** No proposals are applied to prompts, templates or kit while an
  experiment runs (ask the Mac session to hold them until the decision), and the source picker keeps its rules.
  If something did change mid-batch (a kit fix landed), note it in the experiment's notes; the decision is then
  at best `inconclusive`.
- **Dimension order:** hook, then structure, then visual, unless LEARNING's beat table shows a larger loss
  elsewhere (pick the dimension of the worst beat). Don't retest a value that was rejected in the last 4 weeks.
- **Balanced arms.** Arms alternate by slot and day (even local day: A = control, B = treatment; odd day:
  swapped), so both arms get both post times and every day yields one same-day pair.
- **Primary metric** is a retention ratio, never views: `youtube.derived.hold_3s` for hook variables,
  `youtube.avg_view_pct` for structure and pace, `youtube.derived.hold_50pct` for visual variables (two exceptions, set in `experiments.CANDIDATES`: `visual.cover` uses `hold_3s`, the cover
  is what the first seconds show; `structure.ending` uses `youtube.derived.completion`). Secondary:
  `youtube.avg_view_pct` (or hold_3s), normalized 7-d views (8.2), Instagram avg watch time when present.

### 8.2 Minimum samples and baseline normalization

- A video **counts** only if it was published on YouTube, has a `7d` metrics row with a retention curve, passed
  gate and review, and its gate `variant` check shows the arm's value really applied (not FAIL, not >20 % off). A
  missed draft, a skipped slot or an unapplied variant does not count. A **pair** counts only if both of the day's
  videos count.
- **Minimum 6 counted videos per arm** (6 pairs, so at least 6 days at 2 a day plus the 7-day metrics lag) before
  any decision; extend to at most **10 per arm**. Decide earlier only to abort (a broken variant, a gate problem).
- **Normalization.** Ratio metrics (hold_3s, hold_50pct, avg_view_pct, completion) are already length-normalized
  and are used raw. Views are normalized: `views_norm = views_7d / baseline`, where `baseline` = median 7-d
  YouTube views of the 10 videos published before that video (rolling; the first 10 videos use the median so far).
  This removes channel growth and the algorithm's week-to-week drift; same-day pairing removes day-of-week
  effects. Report raw and normalized views; decide on normalized ones.
- **Confounds.** Compare videos of 61-90 s only. If the arms' median durations differ by more than 15 % (and the
  variable is not `pace.*`), or one arm's sources have a median outlier score more than 2x the other's, the result
  is at best `inconclusive`.
- **Decision** (applied by `experiments decide`): **adopt** if the treatment's median primary metric beats
  control by >= 10 % relative AND the treatment wins >= 2/3 of the same-day pairs AND no secondary metric is
  worse by more than 15 %; **reject** if control wins by the same rule; otherwise at the minimum sample:
  `extend`, at the maximum: `inconclusive` (keep control).

### 8.3 Folding winners in

`adopt` -> `rules.json` overlay at once (L4) -> next make uses it -> L4 writes a patch proposal for PLAYBOOK,
templates, prompts or kit -> HUMAN.md -> a Mac session applies it between experiments and marks it `repo_applied`.
You never apply a proposal yourself.

### 8.4 Kill rule

`data/killrule.json` (L4) counts only YouTube `7d` rows, one per published video:

- fewer than 30 videos: `insufficient` (nothing to do);
- median 7-day views per video >= **10,000**: `continue`;
- else if the last-10 median >= 5,000 and the Theil-Sen trend per video is positive and it hasn't been extended
  before: `extend` (re-check after 15 more videos);
- else `stop`.

It is checked every Monday and after every 5th new 7-day row once there are 30. On `stop` the code pauses the
loop (`pause_reason: kill_rule`) and writes HUMAN.md with the numbers; you add a short summary from LEARNING.md
(best and worst videos, the experiments tried) and make nothing more. On `extend` or `continue`, journal it. Only
the human decides what happens after a stop.

## 9. Escalation: HUMAN.md

Write with `python -m pipeline.ops.state human "<text>" --key <stable key>` (the key stops repeats). Write when:
drafts need approval (the publish job writes this itself), a CLI reports `DRY-RUN: missing ...` (list the variable
names, never values), a job exits 5, two slots failed, the budget hit 80 % or 100 %, the kill rule fired, a
proposal is ready, or the guard blocked something you needed. Keep entries short: what happened, what the human
must do, by when.

## 10. Budget and token caps

Unit: weighted tokens = input + output + cache creation + 0.1 x cache reads.

| Item | Cap |
|---|---|
| One video (all `claude -p` steps of studio-make: annotate, script, shots, review rounds, package) | 2.5M (`--budget-tokens`; studio-make exits 3) |
| Reviewer subagent | 80k round 1, 60k round 2 |
| TikTok transcriber subagent | 30k (at most 8 screenshots per run) |
| Triage subagent | 40k (log tails only, never whole logs) |
| Weekly-notes subagent | 60k |
| A quiet tick in this session | 15k |
| This session per day (all of the above you run) | 1.5M, **measured** from the session transcripts (plus subagents) by `budget check`; at the cap `review`/`tiktok_screens` wait for the next day and HUMAN.md says so. Still log `budget add-operator` after each job (the larger number counts) |
| Week | 40M; at 80 % one video a day and no optional work; at 100 % makes stop until Monday |

`python -m pipeline.ops.budget check` prints the level. Keep your own context small: use subagents for anything
that reads images or long files, read log tails, never cat whole JSONL ledgers (use `tail` or the CLIs).

## 11. Human setup (once; the operator never does these)

1. `~/studio/.env` (mode 600) with the variables in docs/OPERATOR_DESIGN.md 4.5 plus
   `APPROVAL_MODE=drafts` (the master switch; `auto` only after checking the platforms' AI labels). Without them
   every CLI runs in dry-run. Checked in the 2026-11-01 dry run (section 13), by account:
   - **Buffer** (one org with the YouTube, TikTok and Instagram channels connected): `BUFFER_API_KEY` (Buffer >
     Settings > API, org owner), then `python -m pipeline.publish.buffer channels` lists the ids for
     `BUFFER_CHANNEL_YOUTUBE`, `BUFFER_CHANNEL_TIKTOK`, `BUFFER_CHANNEL_INSTAGRAM`. Optional: `BUFFER_ORG_ID`,
     `BUFFER_API_URL`, `BUFFER_YT_CATEGORY_ID` (default 28).
   - **Public media URL** for Buffer to fetch the MP4: nothing to set for the default (`PUBLIC_HOST_MODE=cloudflared`,
     `CLOUDFLARED_BIN` defaults to `~/.local/bin/cloudflared`, installed). `static` mode needs `PUBLIC_BASE_URL` and
     `PUBLIC_MEDIA_DIR`.
   - **YouTube** (channel account + a Google Cloud project with YouTube Data API v3 and YouTube Analytics API, OAuth
     client type Desktop app): save the client JSON as `~/studio/secrets/yt_client_secret.json` (or set
     `YT_CLIENT_SECRETS_FILE`), set `YT_CHANNEL_ID=UC...`, run the consent (step 2) which writes `YT_TOKEN_FILE`
     (default `~/studio/secrets/yt_token.json`).
   - **Instagram** (professional account linked to a Facebook Page, Meta app with `instagram_basic` +
     `instagram_manage_insights`): `IG_USER_ID`, `IG_ACCESS_TOKEN` (long-lived), `META_GRAPH_VERSION`, and
     `IG_GRAPH_HOST=graph.instagram.com` only for an Instagram-Login token.
   - **TikTok**: no API. Metrics come from CSVs/screenshots you drop in `data/inbox/tiktok/`
     (`pipeline/analytics/TIKTOK_IMPORT.md`).
   - Optional: `YTDLP_COOKIES_FILE` (yt-dlp when YouTube bot-blocks the Spark; also needed to fetch source videos
     for the side-by-side sheet, see Known gaps), `STUDIO_CLAUDE_MODEL`.
2. YouTube consent: `python -m pipeline.analytics.youtube auth` over `ssh -L 8765:127.0.0.1:8765 dgx-spark`.
3. Review `scripts/operator_settings.example.json`, then `cp` it to `~/studio/operator_settings.json` on the Spark.
4. `scripts/operator_tmux.sh start` (from the Mac or the Spark), then `scripts/install_operator_cron.sh`.
5. Every day: approve drafts in Buffer (set each platform's AI-content toggle), read HUMAN.md, run
   `scripts/pull_ops.sh` on the Mac and commit what is useful.
6. Switches: `scripts/operator_ctl.sh status|pause|unpause|mode <p> draft|auto|disclosure <p> yes|no`. A platform
   posts automatically only if `APPROVAL_MODE=auto` (read at session start: `operator_tmux.sh rotate` after
   changing it), `mode.<p>=auto` and `disclosure_ok_auto.<p>=true`.

## 12. Interface requests (for the integrator; from L5)

- L1: rejected sources are recorded with `python -m pipeline.sources mark <id> rejected --reason R --slug S`
  (called by pipeline/ops after a slot's source fails) and are also kept in `state.rejected_sources`, which run.py
  passes to `pick --exclude`. run.py reads the pick from `{"pick": {"source_id": ...}}` on the last stdout line.
- L3: `post.py` should also refuse `--mode auto` unless `data/operator/config.json` says auto + disclosure for that
  platform and `data/operator/approval_mode` is `auto` (defence in depth; run.py already decides the mode), and
  `status` should mark drafts unapproved 6 h after the slot as `missed`.
- L4: `experiments decide` should apply the counting, normalization and confound rules of 8.2 and record the
  primary metric per dimension as listed in 8.1.

## 13. Dry run of one full cycle (2026-11-01, played by hand)

A Mac session played the operator on the Spark (`~/studio/app`, `STUDIO_LOCAL=1`, `APPROVAL_MODE=drafts`, no
`~/studio/.env`) and followed sections 3-8. Artifacts: `out/operator-dryrun/` (MP4, `qa/` gate + sheets + review,
`publish/captions.json`, `ledgers/`).

| Step | Result |
|---|---|
| Resume | `state init`, `heartbeat --resume`, `reconcile`. Crons were not armed: CronCreate only means something inside the real tmux session |
| Tick 1, `run auto` | `20261101-a-make` skipped (too late), `20261101-b-make` started: `experiments assign` gave no experiment, `sources pick` gave **VtrcKTkhDHU** (OctoLab, "Why The Ocean's Deadliest Predator Refuses To Kill Us", 8.29M views, outlier x318.8, a 34-min long-form) |
| make | `op-20261101-b-ocean`, 21.3 min, 0.98M weighted tokens ($6.24): script 234 words, originality PASS (vs source: run 4, 0 % 5-grams), TTS 93.5 s, shots, storyboard PASS, in-make review, render 160 s at **concurrency 2**, package, thumbs |
| gate r1 | **FAIL** `black_frames` (a 0.9 s "WHY?" card on black at 6.6 s); WARN duration 93.5 s, captions (one 5-word page), safe_area (captions at 77 %) |
| review r1 | **FIX**, viewer 72 (hook 8, clarity 7, pacing 7, visual 6): black card, 5-word page, a seal drawn as a ring |
| fix | 5.5 min, +0.32M tokens (make total 1.30M, $7.95). Gate r2 **PASS** (2 WARN: duration, safe_area) |
| review r2 | **PASS**, viewer 76 (hook 8, clarity 8, pacing 7, visual 7), no must_fix |
| publish | detached `publish.post`, all 3 platforms `draft`, `--slot-at 2026-11-02T00:30Z` (18:30 local). DRY-RUN (no Buffer key), 3 `dry_run` rows in `data/posts.jsonl` with the full GraphQL payloads; HUMAN.md entry written by the code |
| analytics | `collect --post-key ... --window 48h|7d` for YouTube and Instagram wrote synthetic rows; `align op-20261101-b-ocean --window 7d` named the top drops (p05 RUNG1 27.6 s, p09 PEAK 57.5 s, p01 HOOK 2.3 s); `heatmap VtrcKTkhDHU --align` fetched the source's real Most-replayed curve; `killrule`: insufficient (0/30) |
| learning | `analytics.learning` wrote `data/learning/2026-W44.md` + LEARNING.md; operator notes added; proposed (not opened) `hook.max_words` 12 -> 8, primary `youtube.derived.hold_3s` |

Small fixes made during the run: render concurrency now comes from config (`budget.render_concurrency`, default 2;
the operator cannot set `CONC`); `STUDIO_DATA` and `STUDIO_DATA_DIR` are aliases in every lane; the side-by-side
sheet no longer substitutes a corpus neighbour's video (it showed a jellyfish TikTok under the orca episode) when
the source MP4 is missing; word target 180-210 (234 words ran 93.5 s); the shots prompt forbids black cards over
0.45 s; REVIEW_PROMPT now says what to do on a gate FAIL (it said "write nothing", which stalled the chain);
visual experiments use `hold_50pct` as 8.1 says; every `claude -p` step is told which Bash commands it may run (each
step lost turns to refused ad-hoc Bash).

The dry-run rows stay in the Spark ledgers: they are all `dry_run`/`synthetic` and every reader skips them. The
source VtrcKTkhDHU is marked picked, so the live loop will not reuse it. To start from a clean operator state anyway:
`mv data/operator data/operator.dryrun-20261101` on the Spark before the first `operator_tmux.sh start`.

## Known gaps

Found in the 2026-11-01 dry run and too big to fix in passing. Each needs a decision or a lane change on the Mac.

1. **The picker prefers long-form sources.** The score's `1.5 * log10(outlier)` dwarfs the `+0.5` Shorts bonus, so
   the first pick was a 34-min video. Its pacing (120 wpm, re-hook every 30 s) does not transfer to a 75-s Short; only
   the angle and beat order did. Decide whether to restrict `--source` picks to Shorts/TikToks or cap the outlier term
   for long-form (`pipeline/sources.py` `score`).
2. **The source video is not on disk, so the side-by-side is blind.** Picks don't download the source into
   `~/studio/refs/explainer/`; `sbs.jpg` now shows "NOT ON DISK" labels and the reviewer's `vs_source` is
   structural only. Needs a low-res fetch in the source step under `ytdlp.lock` (YouTube bot-blocks full downloads
   from the Spark: `YTDLP_COOKIES_FILE`).
3. **Topic keys are too generic.** The orca video's topic is "ocean" (kit-fit matched the background), so the slug is
   `op-...-ocean` and the same-topic dedupe and sameness `topic` check would not catch a second orca video. The topic
   should come from the subject creature (the script's or annotation's subject), not the background.
4. **Runtime above 90 s only WARNs,** yet experiments count 61-90 s videos only, so such a video is a wasted
   sample. The word target is lowered, but a fix round cannot shorten a script. Consider a gate FAIL above 90 s for
   `op-*` episodes, or a `--from script` path in the fix job.
5. **A dry cycle cannot be isolated.** `pipeline/sources.py` and `pipeline/qa` use `<repo>/data` directly (no
   `STUDIO_DATA`), so a rehearsal writes the real `sources.jsonl` and operator state.
6. **Dry-run posts never create status or metrics jobs** (only `published` posts do), so the analytics chain runs only
   by hand until real posts exist. The first live week is its real test.
7. **Session crons are untested.** The `tick`/`make-a`/`make-b` CronCreate re-arm only works inside the real tmux
   session; check `state show --brief` crons after the first `operator_tmux.sh start`.
8. **`claude -p` JSON results are dumped into `make.log`** (several KB per call), which crowds out the 150-line
   tail that the triage job reads. Log only `result` and usage.
9. **The in-make review round misses what the gate and the operator catch.** It looks at stills only, so it let
   through a 0.9 s black card (between two stills) and a seal drawn as a ring. Expect about one fix round per video
   (+0.3M tokens, +6 min) until it also reads the gate's black/caption checks.
10. **Cost per video** in this run: 1.30M weighted tokens ($7.95 at list price) for make + fix, plus ~75k for the
    operator's reviews. Two a day is about 2.7M/day and 19M/week, inside the 40M weekly cap.
