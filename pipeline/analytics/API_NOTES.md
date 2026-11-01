# Analytics API notes: verified vs assumed

Checked 2026-11-01 against the official docs (pages fetched that day). "Verified" means the official page states it.
"Assumed" means the code depends on it but no official page confirmed it; each assumed item says how the code copes
when it is wrong. Re-check the assumed items on the first real run (the human's `.env` and tokens).

## YouTube Analytics API v2 (`reports.query`)

Sources: <https://developers.google.com/youtube/analytics/reference/reports/query>,
<https://developers.google.com/youtube/analytics/channel_reports>, <https://developers.google.com/youtube/analytics/dimensions>,
<https://developers.google.com/youtube/analytics/metrics>, <https://developers.google.com/youtube/analytics/revision_history>.

| Item | Status | What the docs say / what the code does |
|---|---|---|
| Endpoint | verified | `GET https://youtubeanalytics.googleapis.com/v2/reports`, empty body, JSON only in v2 |
| Required params | verified | `ids` (`channel==MINE`), `startDate`, `endDate` (YYYY-MM-DD), `metrics`; optional `dimensions`, `filters` (`;`-joined), `sort`, `maxResults`, `startIndex` |
| Scopes | verified | `yt-analytics.readonly`; the page also says requests now require `youtube.readonly`. We request both |
| Response | verified | `columnHeaders[]` (`name`, `columnType`, `dataType`; dimensions first, then metrics in request order) and `rows[][]`; `rows` is **omitted** when there is no data (we treat that as "pending") |
| Audience retention report: dimension | verified | `elapsedVideoTimeRatio` is **required** and is the only dimension |
| Audience retention report: metrics | verified | one or more of `audienceWatchRatio`, `relativeRetentionPerformance`, `startedWatching`, `stoppedWatching`, `totalSegmentImpressions`. We request the first two |
| Audience retention report: filters | verified | `video` is **required and takes a single id** (no comma list); optional `audienceType`, `subscribedStatus`, `youtubeProduct`. We send `filters=video==<id>` only |
| `elapsedVideoTimeRatio` values | verified | 100 data points per video, 0.01 to 1.0; each value is the **exclusive end** of its interval; points are equally spaced in time. align.py maps `x * duration_s` to seconds |
| `audienceWatchRatio` | verified | absolute ratio of viewers watching at that point; **can exceed 1** (rewatch/loops), e.g. 1.2. align.py and derive() do not clamp |
| `relativeRetentionPerformance` | verified | 0-1 vs all YouTube videos of similar length, median 0.5. Stored as `retention.relative`, averaged per scene as `rel_mean` |
| Basic stats metrics | verified | `views`, `engagedViews`, `estimatedMinutesWatched`, `averageViewDuration`, `averageViewPercentage`, `likes`, `comments`, `shares`, `subscribersGained` are all in the basic-stats metric list with an optional `video` filter |
| `averageViewDuration` / `averageViewPercentage` | verified | exclude looping-clips traffic since 2021-12-13 |
| Shorts `views` change | verified | from 2025-03-31 a Shorts view counts every start or replay with no minimum watch time; `engagedViews` carries the old method and is available alongside `views` in all reports (revision history 2025-03-26 / 2025-04-24; definition updated 2026-08-27) |
| `engagedViews` accepted in a combined totals query | assumed | listed, but not tested with our channel. If the API answers 400, `youtube.Client.totals` retries without it and notes that in `raw.notes` |
| Retention returned for Shorts | assumed | the docs do not restrict the retention report by content type. If `rows` is missing the metrics row is written with `retention: null, pending: ["retention"]` and retried every 12 h until window + 48 h |
| Data freshness | assumed | Analytics data lags 1-3 days (common knowledge, not on these pages). Handled by the pending retry. `views` in our rows is the Data API `viewCount` (near real time), and the Analytics `views` is kept as `views_analytics` |
| Day boundaries | assumed | Analytics days are Pacific time; `startDate` is set one day before the UTC publish date to be safe |
| `youtubeProduct` values | verified | CORE, GAMING, KIDS, MUSIC, UNKNOWN (no SHORTS value; Shorts is a `creatorContentType` value, which this report does not list). Not used |

## YouTube Data API v3 (`videos.list`)

Source: <https://developers.google.com/youtube/v3/docs/videos/list>.

| Item | Status | Notes |
|---|---|---|
| `GET https://www.googleapis.com/youtube/v3/videos`, `part=statistics,contentDetails` (+`snippet`), `id=` | verified | quota cost 1 unit |
| `statistics.viewCount/likeCount/commentCount` field names, `contentDetails.duration` in ISO 8601 (`PT1M14S`) | assumed | the list page links to the resource page instead of naming them; these are the long-standing field names. `iso8601_duration` returns `None` on anything unexpected and the beatmap duration is used instead |

## OAuth (installed app, loopback)

| Item | Status | Notes |
|---|---|---|
| Loopback redirect `http://127.0.0.1:<port>/`, PKCE S256, `access_type=offline`, `prompt=consent`, token endpoint `https://oauth2.googleapis.com/token`, refresh with `grant_type=refresh_token` | assumed (standard Google installed-app flow, not re-read today) | only the human runs `python -m pipeline.analytics.youtube auth`. A failed refresh raises DependencyError (exit 5) and the operator writes HUMAN.md |

## Instagram Graph API (Reels insights)

Source: <https://developers.facebook.com/docs/instagram-platform/reference/instagram-media/insights> (showed **v26.0**).

| Item | Status | Notes |
|---|---|---|
| `GET https://<host>/<version>/<IG_MEDIA_ID>/insights?metric=<list>` | verified | `metric` required, `period` optional, no breakdowns for Reels metrics |
| Host + permissions | verified | Facebook Login: `graph.facebook.com`, `instagram_basic` + `instagram_manage_insights` (+ `pages_read_engagement`); Instagram Login: `graph.instagram.com`, `instagram_business_basic` + `instagram_business_manage_insights`. Default host `graph.facebook.com`; set `IG_GRAPH_HOST` for the other |
| Reels metric names | verified | `views`, `reach`, `likes`, `comments`, `shares`, `saved`, `total_interactions`, `ig_reels_avg_watch_time`, `ig_reels_video_view_total_time`, `reels_skip_rate`, plus `reposts`, `crossposted_views`, `facebook_views` (and Facebook-Login-only `total_*`). Several are marked "in development" (`views`, `total_interactions`, `ig_reels_video_view_total_time`, `reels_skip_rate`). We request ten of them one at a time and keep what returns |
| Not Reels metrics | verified | `plays`, `ig_reels_aggregated_all_plays_count`, `clips_replays_count` are not listed for Reels; `impressions` is deprecated for media created after 2024-07-02. We do not request them |
| Response shape `data[].values[0].value` or `data[].total_value.value` | assumed | both shapes are read |
| `ig_reels_avg_watch_time` and `ig_reels_video_view_total_time` in **milliseconds** | assumed | stored raw under `raw.insights`; `avg_view_s = ms / 1000`, `watch_time_min = ms / 60000`. If the first real values look like seconds, fix `instagram.to_row` |
| `reels_skip_rate` is a percentage 0-100 | assumed | `viewed_vs_swiped_pct = 100 - reels_skip_rate`; raw value kept |
| `/{IG_USER_ID}/media?fields=id,permalink,timestamp,caption,media_product_type,media_type` with cursor paging | partly verified | the media object reference lists `permalink`, `timestamp` (ISO 8601, UTC) and `media_product_type` (AD/FEED/STORY/REELS); the `/media` edge page returned 404 today, so `limit=50` and `paging.cursors.after` are assumed |
| Access token sent as `Authorization: Bearer` header | assumed | Graph API accepts it; keeps the token out of URLs and logs |
| No retention curve | verified by omission | the insights page lists no per-second retention metric for Reels, so Instagram rows have `retention: null` |

## yt-dlp "Most replayed" heatmap

| Item | Status | Notes |
|---|---|---|
| `yt-dlp -J --skip-download` gives `heatmap: [{start_time, end_time, value}]` | verified on the Spark | yt-dlp 2026.10.26: a control video (dQw4w9WgXcQ) returned 100 points with `value` normalised to max 1.0 |
| Depth Theory sperm whale (fGcgWaswMns) | observed | first fetch (19:32 UTC) returned the full watch-page info (duration 599, 7 chapters, likes and comments) with `heatmap: null`, so status `none`. Later fetches in the same hour got HTTP 429 plus "Sign in to confirm you're not a bot" and a partial info dict |
| Partial answers under `--ignore-no-formats-error` | observed | a refused watch page still prints JSON (no duration, no heatmap). The puller keeps warnings on and marks that `blocked` (no retry for 7 days), not `none` |
| When YouTube shows Most replayed | assumed | only once enough viewers rewatch. `none` is retried after 2 days |

## TikTok

No TikTok API is used in this design (not checked today whether any TikTok API returns a creator's own
retention curve). Numbers come from the human via CSV or screenshots, see `TIKTOK_IMPORT.md`.
