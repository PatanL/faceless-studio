# pipeline/analytics (lane L4: analytics + learning)

Spec: `docs/OPERATOR_DESIGN.md` sections 5.11-5.17 and 9. API facts: `API_NOTES.md` (verified vs assumed).
TikTok numbers: `TIKTOK_IMPORT.md`. Everything is stdlib Python 3.12, single-threaded and network-bound, so it is
safe next to a render. Run on the Spark in `~/studio/app` (`STUDIO_LOCAL=1`).

## Commands

```bash
python -m pipeline.analytics.youtube auth                      # HUMAN ONLY, once (see "One-time setup")
python -m pipeline.analytics.collect --due [--list] [--dry-run]  # what L5's metrics48 / metrics7d jobs run
python -m pipeline.analytics.collect --post-key <slug>:youtube --window 48h|7d [--dry-run]
python -m pipeline.analytics.tiktok_import --inbox | <file.csv> [--post-key K]
python -m pipeline.analytics.heatmap <video_id|url> [--force] [--align]     # Most replayed, yt-dlp -J on the Spark
python -m pipeline.analytics.heatmap --from-daily 20 --align                # weekly: top explainer outliers
python -m pipeline.analytics.align <slug> --window 7d [--platform youtube] [--curve FILE] [--no-write]
python -m pipeline.analytics.align --source <video_id> [--curve FILE] [--no-write]
python -m pipeline.analytics.experiments assign --date YYYY-MM-DD --slot a|b [--slug S]   # prints {} or {experiment_id, arm, variables}
python -m pipeline.analytics.experiments open --dimension hook|structure|visual [--confirm]
python -m pipeline.analytics.experiments decide [--dry-run]
python -m pipeline.analytics.experiments status
python -m pipeline.analytics.learning [--week 2026-W46] [--stdout]
python -m pipeline.analytics.killrule [--dry-run]
python -m pipeline.analytics.synthetic retention --duration 75 --drop 12.3:0.07 > curve.json   # test curves
python -m pipeline.analytics.beatmap <slug>                    # print the beat map align would use
```

Exit codes follow OPERATOR_DESIGN 4.6: 0 ok (incl. dry-run), 1 failed, 2 usage, 4 nothing to do (no curve yet,
no running experiment), 5 dependency (401/403, token refresh failed, network).

## Environment (`~/studio/.env` on the Spark; never in code, never printed)

| Variable | Needed for | Default |
|---|---|---|
| `YT_CHANNEL_ID` | YouTube collect (checks each video belongs to our channel) | none: dry-run without it |
| `YT_CLIENT_SECRETS_FILE` | YouTube OAuth client (the user's own Google Cloud "Desktop app" client JSON) | `~/studio/secrets/yt_client_secret.json` |
| `YT_TOKEN_FILE` | YouTube refresh token written by `youtube auth` (mode 600) | `~/studio/secrets/yt_token.json` |
| `IG_USER_ID` | Instagram professional account id | none: dry-run without it |
| `IG_ACCESS_TOKEN` | long-lived Graph token (`instagram_basic`, `instagram_manage_insights`) | none: dry-run without it |
| `META_GRAPH_VERSION` | Graph API version | `v26.0` |
| `IG_GRAPH_HOST` | `graph.facebook.com` (Facebook Login token) or `graph.instagram.com` (Instagram Login token) | `graph.facebook.com` |
| `YTDLP_COOKIES_FILE` | optional cookies for yt-dlp heatmap fetches when YouTube bot-blocks the Spark | unset |
| `YTDLP_BIN` | yt-dlp path | `~/.local/bin/yt-dlp` |
| `STUDIO_DATA_DIR` | tests only: ledger root instead of `data/` | `data/` |

When any variable a command needs is missing it prints `DRY-RUN: missing <NAMES> in ~/studio/.env` and exits 0.

## One-time setup (the human, not an agent)

1. Google Cloud console: enable "YouTube Data API v3" and "YouTube Analytics API", create an OAuth client of type
   Desktop app, save its JSON as `~/studio/secrets/yt_client_secret.json` on the Spark (`chmod 600`).
2. `ssh -L 8765:127.0.0.1:8765 dgx-spark`, then on the Spark `cd ~/studio/app && python -m pipeline.analytics.youtube auth`;
   open the printed URL in your browser, consent with the channel's account. The token lands in `YT_TOKEN_FILE`.
3. Add `YT_CHANNEL_ID=UC...`, `IG_USER_ID=...`, `IG_ACCESS_TOKEN=...` to `~/studio/.env` (`chmod 600`).

## Ledgers written (single writer: L4)

`data/metrics.jsonl`, `data/alignments.jsonl`, `data/heatmaps/<id>.json`, `data/experiments.jsonl`,
`data/learned/rules.json`, `data/learning/<week>.md` + `LEARNING.md`, `data/proposals/<date>-<exp>.patch`,
`data/killrule.json`, `out/<slug>/analytics/align-<window>-<platform>.json`.
Dry-run / synthetic rows carry `dry_run: true` or `source: synthetic` and are skipped by experiments, learning and
the kill rule. `data/proposals/*.patch` are text only: a Mac session reviews and applies them.

## How alignment names a drop

`beatmap.json` from L1 (5.4) when it exists; otherwise `beatmap.derive_from_storyboard` rebuilds it from
`storyboard.json` (F20 frame-accurate scene starts, caption words) plus the beat alignment table in `script.md`.
Caption pages are then a greedy approximation of the core pager (L1's beatmap carries the exact pages). Source videos
use `research/library/videos/<id>.json` beats (or the corpus line table's beat runs) and the corpus line table or
transcript for lines (internal use only, BRIEF rule 5).

## Interface notes for the integrator

- `pipeline/common/` (L5) was not committed yet when this lane landed, so `_common.py` imports it when present and
  otherwise uses local copies with the same signatures. Once L5's module exists nothing needs to change.
- L3's `posts.jsonl` rows should carry `source_id`, `experiment_id`, `arm`, `duration_s` and (for Instagram) the
  caption text as `caption`, as in 5.10; collect and learning read them. Instagram matching falls back to
  timestamp +- 15 min and the first 20 caption characters.
- `experiments assign` writes the assignment row (idempotent by date + slot); pass `--slug` once L1 knows it, or L1's
  `variant.json` / L3's posts rows supply the link.
- Rules defaults come from `data/learned/rules.json`, else `pipeline/ops/config.default.json` key `rules_defaults`,
  else the 5.15 defaults in `experiments.DEFAULTS`.
