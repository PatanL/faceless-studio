# LEARNING 2026-W44

Generated 2026-11-01 21:19 UTC by `python -m pipeline.analytics.learning`. 0 videos with posts, 0 real metrics rows, 0 own and 1 source alignments. Synthetic and dry-run rows are excluded.

## 1. Scoreboard

| Video | Published (local) | Source | Arm | YT 48h | YT 7d | TT 48h | TT 7d | IG 48h | IG 7d | hold 3s | avg view % |
|---|---|---|---|---|---|---|---|---|---|---|---|
| (no published videos with real metrics yet) | | | | | | | | | | | |

## 2. Where viewers leave (beat level)

z > 0 means that beat loses viewers faster than the rest of its own video (first 2 % and last 3 % excluded).

| Beat | Scenes | Median z (drop/s vs own video) | Median drop/s |
|---|---|---|---|
| (no retention alignments yet) | | | |

| Component | Scenes | Median z | Median drop/s |
|---|---|---|---|
| (fewer than 2 scenes per component so far) | | | |

## 3. Source vs ours

| Video | Source | Source's most replayed beat | Our scenes on it | Their z | Kept? |
|---|---|---|---|---|---|
| (no own alignments yet) | | | | | |

## 4. Experiments

- No experiment running.
- Rules overlay (`data/learned/rules.json`): hook.max_words=12, hook.type=source, pace.rehook_s=9, structure.skeleton=source, visual.cover=scale, visual.max_hold_s=3.0, visual.shot_mix=balanced.

## 5. Kill rule

- Verdict **insufficient**: 0 of 30 YouTube videos have 7-day numbers.
- n = 0, median 7-day views - (target 10000), first-10 -, last-10 -, Theil-Sen slope -/video.

## 6. Candidate next experiments (ranked by beat-level loss)

1. `hook.max_words`: `12` -> `8` (hook; no beat data yet). A shorter first line (<= 8 words) lands the premise before the 1-2 s swipe. Primary `youtube.derived.hold_3s`. Open with `python -m pipeline.analytics.experiments open --dimension hook --confirm`.
2. `pace.rehook_s`: `9` -> `7.0` (structure; no beat data yet). A re-hook every 7 s (vs 9) flattens the mid-video decline. Primary `youtube.avg_view_pct`. Open with `python -m pipeline.analytics.experiments open --dimension structure --confirm`.
3. `visual.max_hold_s`: `3.0` -> `2.0` (visual; no beat data yet). No visual hold over 2.0 s (vs 3.0) reduces mid-scene drops. Primary `youtube.avg_view_pct`. Open with `python -m pipeline.analytics.experiments open --dimension visual --confirm`.

## 7. Operator notes

- **DRY RUN 2026-11-01 (synthetic numbers, not evidence).** One cycle: `op-20261101-b-ocean`, modelled on VtrcKTkhDHU
  (OctoLab, 8.29M views, x318.8, a 34-min long-form). Review r1 FIX (72; gate FAIL: a 0.9 s black "WHY?" card), r2 PASS (76).
  Buffer drafts were built for YouTube, TikTok and Instagram (dry run, nothing sent). Runtime 93.5 s, outside the 61-90 s
  window that experiments compare.
- Synthetic 7-d YouTube curve, aligned: hold_3s 0.74, avg view 58.6 %. The steepest drops were p05 RUNG1 at 27.6 s
  ("It scales up." caption over the blue-whale line, z +2.37), p09 PEAK at 57.5 s (boats rammed) and p01 HOOK at 2.3 s.
  The drops are placed by the generator; this only proves that align names scene, beat, line and caption.
- Source heatmap (real, VtrcKTkhDHU): the most replayed moment is the cold-open hook (10 s). The steepest fall-offs are at 8:05
  (sharks abandon territory), 30:20 (captivity payoff) and 31:41 (toxins). Our cut keeps the shark beat at 18-26 s
  and the captivity reversal at 72-82 s.
- **Proposed next experiment (not opened; it opens on the first Monday with data):** `hook.max_words` 12 -> 8, primary
  `youtube.derived.hold_3s`, arms alternating by slot and day, 6-10 counted videos per arm. Why first: dimension order
  is hook, then structure, then visual, and the hook is the cheapest one-variable change; this video's hook was 10 words.
