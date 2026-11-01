# Status at the weekly reset (observed 14:07 UTC, Nov 1)

Weekly usage went 35% → 85% between 08:40 and 13:52 UTC, then reset to 0% (next reset Nov 8, 14:00 UTC). From here on: video parity for the Awaken recreation only, lean usage (see `~/Documents/Codex/2026-10-30/i-wa/work/POST_RESET.md`).

## Goal checklist

| # | Item | State |
|---|---|---|
| 1 | One-command pipeline (topic → script → storyboard → voice → captions → render → MP4) | **Done.** `./studio-make --niche explainer --topic "…"` / `--niche horror --premise "…"`; script via `claude -p`, everything heavy on the Spark CPU. Proven on 3 new episodes with no hand-edited TSX (`research/repeatability.md`). |
| 2 | Two 2D kits (Depth Theory explainer, phone-chat horror) | **Done.** `studio/src/kits/explainer/`, `studio/src/kits/horror/`, plus audio (Kokoro TTS, -14 LUFS mix) and thumbnails. |
| 3 | Research library, 50+ analyzed videos | **Done.** 63 videos (21 per niche, outliers + controls) with outlier score, title, thumbnail, beats, shot list, transcript: `research/library/INDEX.md`. Plus viral-script corpora of 24-25 annotated outliers per niche with PLAYBOOKs (`research/corpus/*/PLAYBOOK.md`). |
| 4 | 3 pilots pass side-by-side review vs reference frames | **Passed** (`out/pilots/QA.md`): horror-pinned-rules 80/84 (md5 14376d5d…); explainer-orca 9:16 78/80 (8702a89c…), 16:9 76 (797d23d5…); explainer-blue-whale 9:16 visual 79 (1a294416…), 16:9 77 (505c27a3…). Blue whale 9:16's final viewer review and the QA.md update were still running at the reset (allowed to finish). |
| 5 | Codex recreation v13, every section reworked | **In progress.** All 12 sections reworked and reviewed (accepted scenes per section in the workflow journal). Integrated into the phase43 master: S1, S2, S8, S10, S12. Integrating now, one at a time: S3, S4, S5, S6, S7, S9, S11 (a 13:20 deadline in the integrator prompt had made them skip; removed and resumed). A partial cut exists as `outputs/recreation/recreated-full-494s-v13-partial-5of12.mp4`. Full v13 + comparison are encoded when the chain finishes. |

## Also produced before the reset

- `backlog/`: 30 original scripts (10 per niche) grounded in the viral corpora (cited references + beat alignment tables), 4-lens critiqued, all with storyboards; `backlog/INDEX.md` has the production order.
- `backlog/longform/sinking-to-the-bottom/`: full 10-min explainer package (script, shot list, assets, titles, thumbnail, description).
- `backlog/series/`: 5-part series bibles + finished part-2 scripts for 3 horror premises.
- `research/R1`-`R5` reports (R5 = platform policy from official sources: animated content with a generic TTS voice needs no altered-content disclosure; the main monetization risk is low-variation templated output).
- `research/CODE_REVIEW_FINDINGS.md`: 29 confirmed bugs with tests in `tests/`; F22-F24 (originality checker) fixed, and the fixed gate re-checked all 47 scripts: 47/47 PASS. The other 26 are queued with a fix order.
- Recreation extras: `work/sections/BLENDER_COOKBOOK.md`, `work/sections/ALT_CANDIDATES.md` (4 gated alternate fixes ready to integrate: S4 23, S7 55, S5 37, S11 104), the Blender job queue (`work/render-queue/`) and its perf log.

## Cut off / not done

- Kit gap fill (menu item 5) was never started (it would have collided with the explainer fixer).
- The 26 remaining code-review bugs (start with the sync/delete ones F25, F26, F07, F06: they can destroy Spark output).
- Series parts 3-5 are outlines; long-form timings after 0:53 are estimates until TTS re-measures.
