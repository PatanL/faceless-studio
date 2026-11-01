# Episodes

Each folder holds `script.md` (front matter with references, beat alignment, facts to verify, the
```` ```narration ```` block, shot notes), `audio/` (Kokoro word timings and mix report from
`pipeline.audio.make --meta-out`), and `storyboard.json` (B2 schema, built by `pipeline/episodes/build.py`).
Rule: **one narration paragraph = one scene**; layers are anchored to spoken words.

| Slug | Niche | Title | Length | Notes |
|---|---|---|---|---|
| **explainer-orca** | explainer | Why You'd Never Want To Meet An Orca | 89.4 s | **Explainer pilot (P1)** |
| explainer-blue-whale | explainer | You Could Fit In Its Mouth. You'd Never Fit Down Its Throat. | 86.6 s | scale paradox |
| explainer-pressure-ladder | explainer | What The Ocean Does To Your Body, Depth By Depth | 88.8 s | depth ladder |
| explainer-saltwater-croc | explainer | Why You'd Never Want To Swim With A Saltwater Crocodile | 85.0 s | myth-busting options |
| explainer-anglerfish | explainer | Never Swim Toward A Light In The Deep | 83.9 s | scale-up + biology twist |
| **horror-pinned-rules** | horror | Someone Pinned New Rules In Our Building Chat (Part 1) | 88.3 s | **Horror pilot (P2)** |
| horror-mom-two-chats | horror | Mom Texted Two Different Things At Once (Part 1) | 75.0 s | family chat vs DM |
| horror-member-41 | horror | Our Building Has 40 Apartments. The Chat Has 41 Members. (Part 1) | 81.8 s | unknown account |
| horror-elevator-maintenance | horror | I Texted Elevator Maintenance At 1 A.M. (Part 1) | 79.2 s | help-line ritual |
| horror-roommate-two-rooms | horror | My Roommate Was In Two Rooms At Once (Part 1) | 71.1 s | doppelganger |

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
```

The storyboard plays `episodes/<slug>/mix.wav` from `studio/public` (Spark only, gitignored); rerun
`pipeline.audio.make` if it is missing. Scene builders live in `pipeline/episodes/{explainer,horror}_eps.py`.
Templates: `pipeline/templates/explainer.md`, `pipeline/templates/horror.md`.
Every script passed `scripts/originality_check.py` against `research/corpus` and `research/library/transcripts`.
