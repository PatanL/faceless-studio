# Repeatability test (lane H1, P3) — 2026-11-01, 11:05-11:50 UTC

**Question:** can `./studio-make` produce a new episode with zero hand-edited TSX (and zero per-episode code)?
**Answer:** yes, in both niches. Three episodes went from script or topic to a rendered MP4, thumbnails, titles and
description, without a hand edit to any storyboard, shots file, TSX or episode Python. The manual interventions were
all one-off kit or pipeline fixes, and each one is now in the repo (table below). Quality is "solid first cut". It is
not "pilot after two review rounds" yet. The remaining defects are listed at the end.

## What one command does now

`./studio-make --niche explainer --topic "..."` (or `--niche horror --premise "..."`, or `--script <path>`) runs the
pipeline in `pipeline/make.py`. The Mac only orchestrates; every heavy step runs on the Spark (CPU, niced):

| step | how | time (cookiecutter v1 / v2) |
|---|---|---|
| script | `claude -p` + `pipeline/prompts/script_<niche>.md` (template, PLAYBOOK, corpus refs, kit inventory); runs `originality_check.py` until it passes, then we re-check it | 4.1 min (octopus), 1.7 min (horror) |
| tts | `pipeline.audio.make` (Kokoro, word timings, mix) | 39-65 s, **in parallel with shots** |
| shots | `claude -p` + `pipeline/prompts/shots_<niche>.md` writes `shots.json`: storyboard scenes whose times are **word anchors** (`"@bus+0.2"`). It loops on `pipeline.episodes.auto --check` | 5-8 min |
| storyboard | `pipeline/episodes/auto.py`: anchors become times; checks kit names and species, 3 s holds, text below 66 %, scale partners sharing `pxPerM`; then zod | 5 s |
| review | contact sheet (2 stills per scene); `claude -p` reads the image and fixes `shots.json`; rebuild | 1-1.5 min |
| render | `spark_render.sh` (render lock, concurrency 4) plus a 12-frame contact sheet | 102-146 s for ~87 s of video |
| package | `claude -p` + `pipeline/prompts/package.md` writes `titles.md`, `description.md`, `thumbs.json` | ~2 min |
| thumbs | `thumbs_render.sh` | 15-20 s |
| collect | copies the outputs to `out/<slug>/` and writes `MANIFEST.md` | — |

Wall clock: **13-15 min per episode** with no human in the loop. Most of that is the `claude -p` calls.

## Episodes produced

| slug | start | result | per-episode hand edits |
|---|---|---|---|
| `explainer-short-cookiecutter-shark` (**the test episode**) | backlog script (`--script`) | 87.2 s 9:16 MP4, 6 thumbs, titles, description. v1 at 11:24, v2 at 11:41 (v2 = rerun of `--reshot --from shots` after the kit fix) | **0** |
| `explainer-giant-pacific-octopus` | `--topic "giant pacific octopus"` (script written by `claude -p`, originality PASS) | 86.5 s MP4, thumbs, titles, description | **0** |
| `horror-building-intercom-buzzes-3-m` | `--premise "the building intercom buzzes at 3 a.m. ..."` | 72.7 s MP4 with chat, call, lock screen, elevator, peephole and EndCard, plus thumbs, titles, description | **0** |

Why a backlog script: every episode in `episodes/` had already been rendered by S1 (`out/S1/*.mp4`), and pilot 3 was taken
by blue-whale (BRIEF 09:47). The explainer niche is the more mature one (two explainer pilots), so the test took the
unrendered backlog Short `explainer-short-cookiecutter-shark`. Its script was corpus-grounded and had already passed originality.

## Manual interventions (all of them) and what was fixed

| # | what happened | intervention | fixed in |
|---|---|---|---|
| 1 | The hand-built storyboards need ~100-400 lines of per-episode Python each (`explainer_eps.py`, `orca_pilot.py`, `horror_eps.py`). A new episode had no builder. | Wrote the generic word-anchored builder, so no episode needs code any more | `pipeline/episodes/auto.py`, `pipeline/prompts/shots_*.md` |
| 2 | The kit had no cookiecutter shark. v1 faked it with an inline-SVG brown cigar, and the **thumbnails could not show the subject at all** (blue whale and great white stood in) | New kit figure `explainer/Cookiecutter` (0.5 m, `glow` track, `collar`, `mouth`), then `--reshot --from shots`. The v2 video and thumbs use it | `studio/src/kits/explainer/smallsharks.tsx` (+ creature.tsx, index.tsx, README) |
| 3 | DepthMeter showed "120 M m". The LLM read `suffix` as the unit. | A unit-like suffix now replaces the unit; README says what `suffix` is | `ocean.tsx`, kit README |
| 4 | Map zoomed to a Hawaii pin and showed open ocean (no Pacific islands in the land data) | Added Hawaiian island rings; README warns that a pin with no coastline shows open ocean at high zoom | `mapdata.ts`, kit README |
| 5 | The v1 hole-saw prop (inline SVG) read as a blank slab and appeared after the sampled still | The reviewer prompt now flags props that don't read as what is spoken; 2 stills per scene instead of 1 (round 2 fixed timing + drawing) | `pipeline/prompts/review.md`, `pipeline/make.py` |
| 6 | The scale beat (pencil on a bus) is easy to fake with box-fit sizes | Checker warns when figures in one scene do not share `pxPerM` | `auto.py` (`layout_warnings`) |
| 7 | The packaging agent could not see the pilot titles/description examples (`out/` is not synced to the Spark) | The examples go into the prompt inline | `pipeline/make.py`, `pipeline/prompts/package.md` |
| 8 | The octopus run crashed in `package` with `KeyError: titles_example`. The prompt file had been edited while that run was in flight (my edit, fix #7) | Resumed with `--from package`. This only happens when code changes mid-run | — |
| 9 | Topic-derived slugs: "3 a.m." became `-3-m`, and `--topic orca` would have collided with the pilot | Slugs drop 1-letter tokens. A derived slug never reuses a hand-built episode folder (`-v2` suffix), and `--slug` of an episode with a hand builder needs `--force` | `pipeline/make.py` |

Nothing in this test needed a TSX edit inside an episode, a hand-edited `storyboard.json`, or a hand-edited `shots.json`.

## Remaining defects (seen in the renders, not fixed)

Cookiecutter v2 (`out/explainer-short-cookiecutter-shark/dense_v2.jpg`):
- ~37 s "like a hole saw": the wide whale-skin cross-section reads as a beige slab. Inline-SVG props stay the weakest
  part. The fix is more kit props (hole saw, ice-cream scoop, pencil, submarine), not prompts.
- The mouth close-up (inline SVG) is reused in 4 scenes. The 2009 map is a boxed panel and is not full-bleed. The "below you"
  depth scene is very dark with a small subject.
- Thumbs `scale` template: a diver stands next to a 0.5 m animal. The template assumes the subject is bigger than the human, and that is
  false for small creatures (kit fix: flip it to a hand or fingertip for scale under ~1 m).

Octopus (`out/explainer-giant-pacific-octopus/explainer-giant-pacific-octopus_sheet.jpg`):
- The camouflage beat shows no colour change (`Octopus` has no colour/camouflage track). One "still not the strangest" frame
  has only a headline.

Horror (`out/horror-building-intercom-buzzes-3-m/horror-building-intercom-buzzes-3-m_sheet.jpg`):
- ~70 s: a caption sits over a chat bubble (the reviewer saw it and left it). The EndCard title "YOUR KEY NEVER LEFT" collides
  with the PART 2 stamp (EndCard should auto-fit long titles). The peephole shot is an empty fisheye.

Process:
- The review agent fixes `shots.json` without seeing the result. Its own reply says it never re-rendered the stills.
  `--review-rounds 2` (one extra minute each) closes that loop. Consider making 2 the default.
- None of the three new episodes has had the side-by-side QA review against `research/library/review-refs/` that the pilots got.
  Treat them as backlog drafts, not ready-to-post.
- Facts in `claude -p`-written scripts (octopus, horror) are listed under "Facts to verify". A human must check them before posting.

## How to reproduce

```bash
./studio-make --script backlog/explainer/explainer-short-cookiecutter-shark/script.md     # ~14 min
./studio-make --niche explainer --topic "giant pacific octopus"
./studio-make --niche horror --premise "the building intercom buzzes at 3 a.m. ..."
./studio-make --slug <slug> --from review --review-rounds 2                                   # another automatic polish pass
```
