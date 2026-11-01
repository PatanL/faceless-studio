# pipeline/publish: Buffer publisher (lane L3)

This lane posts a gated, reviewed explainer Short to YouTube Shorts, TikTok and Instagram Reels through Buffer's
GraphQL API. Buffer **drafts** are the default (the human approves them in Buffer); **auto** scheduling is a
per-platform switch in `data/operator/config.json`. The spec is `docs/OPERATOR_DESIGN.md` section 8. What was checked
against Buffer's docs, and what is still assumed, is in `BUFFER_NOTES.md`. Stdlib only, Python 3.11+ (Mac 3.13, Spark 3.12).

## CLI (exit codes per OPERATOR_DESIGN 4.6: 0 ok/dry-run, 1 failed, 2 usage, 4 nothing to do, 5 dependency, 6 gate)

```bash
python -m pipeline.publish.buffer channels [--dry-run]       # organizations + channel ids, for the human's .env
python -m pipeline.publish.buffer introspect [--dry-run]     # data/buffer_schema.json + checks the fields we use
python -m pipeline.publish.post <slug> --slot-at <ISO> [--platforms youtube,tiktok,instagram] [--mode draft|auto] \
        [--dry-run] [--ignore-gates] [--mp4 PATH] [--hold-max-h 12]
python -m pipeline.publish.post --record-manual <slug> <platform> <url> [--published-at ISO]
python -m pipeline.publish.status [--all-open] [--slug S] [--dry-run]
python -m pipeline.publish.schedule next --date YYYY-MM-DD [--slot a|b]
python -m pipeline.publish.host selftest                     # real quick tunnel: HEAD 200, then unreachable
python -m pipeline.publish.host serve --dir DIR --port 8787  # static-mode file server (token paths only)
```

`post` refuses (exit 6) unless `out/<slug>/qa/gate.json` is PASS, `out/<slug>/qa/review.json` is PASS,
`gate.mp4_sha256 == sha256(mp4)`, `review.gate_sha == sha256(gate.json)`, no live ledger row exists for the
post_key, and `config.paused` is false. A live row has status `draft`, `scheduled`, `sending`, `published`, `missed`
or `manual`, or is `failed` with `ambiguous: true`; `dry_run` rows never block. In a dry-run it prints the
precondition table and the payloads either way, but it writes rows only when the preconditions pass, or with
`--ignore-gates`. That flag is only for previewing an episode that has no gate yet (such as the pilots), and is
rejected without `--dry-run`.

Inputs: `episodes/<slug>/package.json` (else `titles.md` + `description.md` from `episodes/<slug>/` or
`out/pilots/<slug>/`), the MP4 from `make_status.json` (else `out/<slug>/<slug>_9x16.mp4`, else the pilot folder),
plus `source.json` and `variant.json` for the ledger. Outputs: `data/posts.jsonl` (5.10) and
`out/<slug>/publish/captions.json` (5.9). `data/buffer_schema.json` comes from `introspect`.

## Environment (`~/studio/.env` on the Spark; created by the human, never by an agent)

| Variable | Needed for | Notes |
|---|---|---|
| `BUFFER_API_KEY` | every real call | Buffer > Settings > API (publish.buffer.com/settings/api); org owner only. Absent -> dry-run |
| `BUFFER_CHANNEL_YOUTUBE`, `BUFFER_CHANNEL_TIKTOK`, `BUFFER_CHANNEL_INSTAGRAM` | `post` | ids from `buffer channels`. Any one missing for a requested platform -> dry-run |
| `BUFFER_ORG_ID` | optional | default: the first organization the key sees |
| `BUFFER_API_URL` | optional | default `https://api.buffer.com` |
| `BUFFER_YT_CATEGORY_ID` | optional | default `28` (Science & Technology); `27` = Education |
| `PUBLIC_HOST_MODE` | `post` | `cloudflared` (default, holds a quick tunnel until Buffer has published) or `static` |
| `PUBLIC_BASE_URL`, `PUBLIC_MEDIA_DIR` | `static` only | a stable public HTTPS base that serves `PUBLIC_MEDIA_DIR/<32-hex>/<slug>.mp4` |
| `CLOUDFLARED_BIN` | optional | default `~/.local/bin/cloudflared` (installed on the Spark) |

The key is never printed: dry-run shows `Authorization: Bearer ***`, and every error message goes through
`pipeline.common.env.redact`. Hosted URLs and tokens are never written to the ledger (only `host.mode`).
Tests and proofs can redirect everything with `STUDIO_ENV_FILE=<missing file>` and `STUDIO_DATA_DIR=<scratch dir>`.

## What a payload looks like (orca pilot, draft mode, abbreviated)

```json
{"channelId": "<BUFFER_CHANNEL_INSTAGRAM>", "schedulingType": "automatic", "mode": "customScheduled",
 "dueAt": "2026-11-02T17:30:00.000Z", "saveToDraft": true, "aiAssisted": true,
 "assets": [{"video": {"url": "https://<tunnel>.trycloudflare.com/<32-hex>/explainer-orca.mp4",
                       "metadata": {"thumbnailOffset": 1500}}}],
 "text": "Wild killer whales could kill you easily. ...\n\n#orca ...\n\nNarration: synthetic AI voice (Kokoro TTS). ...",
 "metadata": {"instagram": {"type": "reel", "shouldShareToFeed": true, "isAiGenerated": true}}}
```

YouTube adds `metadata.youtube {title, categoryId, privacy: public, madeForKids: false, isAiGenerated: true,
notifySubscribers: true, embeddable: true}` and uses the description as `text`, with `#shorts`. TikTok sends
`metadata.tiktok {isAiGenerated: true}`.

## Ledger rows (5.10 plus these fields)

`buffer_status` (Buffer's raw status), `host: {mode}`, and on dry-run rows `payload` (the exact GraphQL body),
`preconditions` (check -> bool) and `gates_ignored`. A failed create that might still have happened (timeout or 5xx
after send) gets `ambiguous: true`, after one reconcile attempt that looks for a post on that channel with the same
text. An adopted post carries `reconciled: true`. `status.py` appends a new row only on a change, and it is the
writer of `missed` (a draft still unapproved `drafts_missed_h` after the slot) and of `deleted` (gone from Buffer).

## Requests to the integrator (interface changes this lane needs; OPERATOR_DESIGN is not edited here)

1. **8.4 TTL:** Buffer fetches media at publish time (see BUFFER_NOTES). In cloudflared mode the publish job holds
   the tunnel until the posts are sent, for up to slot + `drafts_missed_h`, at most 12 h. L5 should run `post`
   detached (`run.py`) and give the publish job a long wall clock. Recommend `PUBLIC_HOST_MODE=static` before switching
   any platform to auto.
2. **5.5 `package.json`:** an optional `cover_offset_ms` (the frame used as the IG/TikTok cover). The default is 1500 ms.
   YouTube cover frames can't be chosen through Buffer.
3. **5.9 limits:** Instagram is 2196 UTF-16 units with line breaks counting 2, not 2200. YouTube tags have no Buffer
   field and stay informational.
4. **10.5:** `missed` is written by `pipeline.publish.status` (single writer of posts.jsonl), not by the operator.
5. **8.5 disclosure:** `isAiGenerated` exists for all three platforms, so no platform is forced to stay in draft by a
   missing field. The human still confirms on the first draft that the label actually appears, then sets
   `disclosure_ok_auto`.
6. **L4:** `external_id` for Instagram is the permalink shortcode; Buffer's experimental `Post.metrics` may cover TikTok.

## Tests

`python3 -m unittest discover -s tests -p 'test_l3_*.py'`: 25 tests covering caption limits, preconditions,
idempotency, dry-run payloads, status mapping, client retry and auth errors (urlopen mocked), and the one-file server
on 127.0.0.1. No network, no credentials.
