# Episodes

Each folder holds `script.md` (front matter with references, beat alignment, facts to verify, the
```` ```narration ```` block, shot notes), `audio/` (Kokoro word timings and mix report from
`pipeline.audio.make --meta-out`), and `storyboard.json` (B2 schema, built by `pipeline/episodes/build.py`).
Rule: **one narration paragraph = one scene**; layers are anchored to spoken words.

| Slug | Niche | Title | Length | Notes |
|---|---|---|---|---|
| **explainer-orca** | explainer | Why You'd Never Want To Meet An Orca | 75.1 s | **Explainer pilot (P1)** |
| explainer-blue-whale | explainer | You Could Fit In Its Mouth. You'd Never Fit Down Its Throat. | 70.1 s | scale paradox |
| explainer-pressure-ladder | explainer | What The Ocean Does To Your Body, Depth By Depth | 88.8 s | depth ladder |
| explainer-saltwater-croc | explainer | Why You'd Never Want To Swim With A Saltwater Crocodile | 85.0 s | myth-busting options |
| explainer-anglerfish | explainer | Never Swim Toward A Light In The Deep | 83.9 s | scale-up + biology twist |
| **horror-pinned-rules** | horror | Someone Pinned New Rules In Our Building Chat (Part 1) | 65.2 s | **Horror pilot (P2)** |
| horror-mom-two-chats | horror | Mom Texted Two Different Things At Once (Part 1) | 75.0 s | family chat vs DM |
| horror-member-41 | horror | Our Building Has 40 Apartments. The Chat Has 41 Members. (Part 1) | 81.8 s | unknown account |
| horror-elevator-maintenance | horror | I Texted Elevator Maintenance At 1 A.M. (Part 1) | 79.2 s | help-line ritual |
| horror-roommate-two-rooms | horror | My Roommate Was In Two Rooms At Once (Part 1) | 71.1 s | doppelganger |

## One command (`studio-make`, lane H1)

```bash
./studio-make --niche explainer --topic "orca"                 # writes episodes/explainer-orca-v2/ (never touches a pilot)
./studio-make --niche horror --premise "the chat has one member more than the building has flats"
./studio-make --script backlog/explainer/<slug>/script.md       # start from a finished script (slug = its id:)
./studio-make --slug <slug> --from storyboard                   # rerun from a step (script tts shots storyboard review render package thumbs collect)
```

No per-episode code: the storyboard comes from `episodes/<slug>/shots.json` (word-anchored scene specs, written by
`claude -p` on the Spark from `pipeline/prompts/shots_<niche>.md`) and is built by `pipeline/episodes/auto.py`
(anchors -> times, kit-name/hold/layout checks, zod). Outputs: `out/<slug>/` (MP4, contact sheets, thumbs, titles,
description, MANIFEST.md); step log in `episodes/<slug>/make.log`. Findings: `research/repeatability.md`.

## Rebuild

```bash
# Spark (CPU only): voice, captions, mix -> studio/public/episodes/<slug>/ and episodes/<slug>/audio/
SKIP_NPM=1 scripts/spark_sync.sh
ssh dgx-spark 'source ~/studio/app/scripts/spark_env.sh && cd ~/studio/app && TTS_THREADS=4 nice -n 10 \
  python -m pipeline.audio.make episodes/<slug>/script.md --id <slug> --meta-out episodes/<slug>/audio'
rsync -a dgx-spark:~/studio/app/episodes/<slug>/audio/ episodes/<slug>/audio/
# Mac (light): storyboard from script + timings, then validate + render on the Spark
python3 -m pipeline.episodes.build <slug>
CONC=4 PROPS=episodes/<slug>/storyboard.json scripts/spark_render.sh Storyboard <slug>.mp4
# look-dev without an MP4 render (niced stills, no render lock): one contact sheet of chosen seconds
scripts/spark_stills.sh episodes/<slug>/storyboard.json 0.5,3,8 out/stills/<slug>.jpg
# first 10 s only: add --frames=0-299 to spark_render.sh
# 16:9 cut (same audio/captions; uniform remap of the 9:16 picture zone, captions to a bottom band)
python3 -m pipeline.episodes.reformat <slug>
CONC=4 PROPS=episodes/<slug>/storyboard_16x9.json scripts/spark_render.sh Storyboard <slug>_16x9.mp4
# thumbnails (B6): episodes/<slug>/thumbs.json, kit art via "art"/"humanArt" (see explainer-blue-whale)
OUT=pilots/<slug>/thumbs scripts/thumbs_render.sh episodes/<slug>/thumbs.json
```

The storyboard plays `episodes/<slug>/mix.wav` from `studio/public` (Spark only, gitignored); rerun
`pipeline.audio.make` if it is missing. Scene builders live in `pipeline/episodes/{explainer,horror}_eps.py`.
Templates: `pipeline/templates/explainer.md`, `pipeline/templates/horror.md`.
Every script passed `scripts/originality_check.py` against `research/corpus` and `research/library/transcripts`.
