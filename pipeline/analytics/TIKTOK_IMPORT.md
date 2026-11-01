# TikTok metrics import

TikTok has no analytics API in this design, so the human supplies TikTok numbers and the operator imports them.

## What the human drops

Into `~/studio/app/data/inbox/tiktok/` on the Spark, any time (the operator's 21:00 job picks them up):

- a CSV in the format below, **or**
- TikTok Studio screenshots (`*.png` / `*.jpg`) of a video's Overview and Viewers/Retention panels.

## CSV format (header required)

```
tiktok_url_or_id,captured_at,views,likes,comments,shares,saves,avg_watch_s,full_watch_pct,new_followers,retention
https://www.tiktok.com/@ourchannel/video/7432100000000000001,2026-11-04T18:00:00Z,12.3K,840,21,57,130,31.4,18.2,44,0:100;3:71;10:48;30:22;60:12
```

- `tiktok_url_or_id`: the video URL or its numeric id. It must match a `tiktok` row in `data/posts.jsonl`
  (`external_id` or `external_url`). For a video posted by hand, record it first with
  `python -m pipeline.publish.post --record-manual <slug> tiktok <url>` (L3), or pass `--post-key`.
- `captured_at`: UTC ISO time the numbers were read. It sets the window: under 96 h after publishing -> `48h`,
  under 20 days -> `7d`, else `28d`.
- Counts may use TikTok's `12.3K` / `1.2M` form. Percentages may carry a `%`.
- `retention` (optional): `seconds:percent` pairs separated by `;`, read off the retention graph (percent of
  viewers still watching at that second). Five to ten points are enough; include `0:100`.

## Screenshots (operator procedure)

1. Read each image (at most 6 images per run).
2. Write one CSV next to them named `<date>-<n>.screenshot.csv` with the columns above. Take the numbers exactly as
   shown; leave a cell empty if it is not visible. Read 5-10 retention points from the graph if it is shown.
3. Run `python -m pipeline.analytics.tiktok_import --inbox`. Rows from `*.screenshot.csv` get
   `source: tiktok_screenshot`; plain CSVs get `tiktok_csv`.
4. Nothing to move by hand: the operator's `tiktok_inbox` job runs `tiktok_import --inbox` (CSVs go to `done/`,
   a CSV that fails goes to `failed/`) and then moves every image not newer than an imported `*.screenshot.csv` to
   `done/`. Re-importing a file never duplicates rows (dedupe on post_key, window, source, captured_at, file name).

TikTok rows feed the scoreboard in LEARNING.md. Experiments and the kill rule use YouTube rows only.
