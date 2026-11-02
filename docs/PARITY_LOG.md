# Parity log

One entry per parity attempt (docs/PARITY.md): which Short, what changed, the measured checks next to the lane's
references, what the frame review found, and what is still open. Newest at the bottom.

## 2026-11-02 · story lane · story-chess-turk v5 (plan steps 1-3 of research/references/STORY_LANE_TUTORIAL_CHECK.md)

**Video:** `out/story-chess-turk/story-chess-turk_v5.mp4` (58.9 s, 1080x1920, sha256 `c2315454…`), phone copy
`out/story-chess-turk/story-chess-turk_v5_phone.mp4` (17 MB). Rendered through `scripts/render.sh` on the Spark
(CPU, nice, concurrency 2): 1767 frames in ~93 s.

### What changed from v4

- **Camera grammar.** `pipeline/episodes/story_camera.py` (new) runs after the house pass when `shots.json` has
  `"story_camera"`; `auto.py` calls it (a 3-line hook).
  - Each authored camera key is a checked framing. Instant jumps become ~0.9 s sine-eased glides.
  - Every hold pushes in (≥ 0.18 %/frame) and drifts toward the next framing. In `drift_mode: "toward"` the drift saturates
    before it gets there, so the camera never leaves the span between two checked framings.
  - No shake and no house float.
  - The set moves at depth 0.9, not 0.3.
  - Hard cuts: three are authored, into the court → cabinet beat, the fire and the reveal. The cut detector finds 2.
  - Every other scene or shot change is a 7-frame crossfade. Same-set changes either start where the last camera ended
    (`cont`) or are matched so the Turk dissolves into himself.
- **Colour, ink, blur** (stick kit only):
  - `storybook()` OKLab remap in `stick/common.ts`: lifts the mid-tones, cuts chroma hardest in the darks and warms the
    highlights a little.
  - `ink` prop: deep-violet outlines on filled shapes. Decorative paint (planks, tiles, grid, chess squares) has none.
  - Lens blur: 3 px on the set layer; characters and props stay sharp.
- **Narration:**
  - Rewritten tighter and re-voiced: 221 words, Kokoro speed 1.28, paragraph pause 0.08.
  - Spoken years are gone from the narration (the tags still show them), because a long numeral token reads as a pause.
  - Two lines were changed after a whisper check misheard them: "No one is laughing now" and "travels Europe".
  - Originality check: PASS.
- **Staging fixes from the frame review:**
  - The chess hands enter, carry the piece and leave as separate phases; hands can overlap between moves.
  - The queen lands beside the king as he falls.
  - Inventor framing: he holds the candle from the start and pushes the cabinet into the shot.
  - The seat slide is eased and his own doors open only after he is hidden.
  - Labels ride with the set.
  - The map is reframed and has no unlabelled pin.
  - New candle-smoke line: a smoke trail and puffs from the turban.

### Measured checks (same tools and flags as the check; every frame)

| Check | 7xS8 | VS1Z | Mz72 | 5WMQ | ZDy3 | GM9U | jpFJ | 0m6G | refs range | v4 | v5 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| words/s | 3.33 | 3.62 | 3.84 | 3.84 | 3.76 | 3.71 | 3.89 | 3.74 | 3.33-3.89 | 3.13 | **3.79** |
| pauses ≥ 0.8 s | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0-1 | 5 | **0** |
| hard cuts | 1 | 1 | 3 | 0 | 0 | 1 | 0 | 0 | 0-3 | 20 | **2** |
| 1-frame jumps (frames30) | 0 | 12 | 10 | 4 | 0 | 0 | 3 | 2 | 0-12 | 54 | **3** |
| camera moving % (≥ 0.3 px/f) | 99 | 99 | 100 | 98 | 96 | 100 | 96 | 99 | 96-100 | 70 | **99** |
| median camera speed px/f | 9.69 | 6.07 | 9.63 | 6.68 | 5.9 | 7.18 | 5.76 | 11.09 | 5.76-11.09 | 0.58 | **5.87** |
| moves / 10 s | 7.37 | 5.09 | 9.6 | 7.02 | 5.95 | 5.88 | 5.17 | 6.94 | 5.09-9.6 | 2.1 | **11.03** |
| quiet frames zooming % | 81 | 81 | 88 | 79 | 73 | 84 | 69 | 87 | 69-88 | 29 | **75** |
| saturation (HSV S median) | 0.50 | 0.42 | 0.61 | 0.41 | 0.46 | 0.54 | 0.49 | 0.42 | 0.41-0.61 | 0.73 | **0.45** |
| colourfulness | 34 | 23 | 33 | 27 | 28 | 29 | 32 | 30 | 23-34 | 61 | **30** |
| luma p50 | 0.46 | 0.37 | 0.31 | 0.43 | 0.54 | 0.34 | 0.53 | 0.58 | 0.31-0.58 | 0.24 | **0.39** |
| non-ink p5 (black level) | 0.15 | 0.16 | 0.09 | 0.13 | 0.19 | 0.12 | 0.23 | 0.18 | 0.09-0.23 | 0.14 | **0.22** |
| shadow chroma | 21 | 13 | 29 | 9 | 16 | 25 | 21 | 35 | 9-35 | 83 | **29** |
| shadow hue ° (Lab) | 36 | 296 | 300 | 274 | 294 | 306 | 48 | 299 | violet-blue in 6/8 | 306 | **292** |
| ink on strong edges | 0.54 | 0.62 | 0.65 | 0.58 | 0.56 | 0.61 | 0.66 | 0.64 | 0.54-0.66 | 0.17 | **0.59** |
| soft (lens-blurred) edges % | 13.6 | 14.6 | 9.4 | 10.0 | 11.5 | 7.2 | 9.4 | 3.8 | 3.8-14.6 | 1.5 | **5.4** |
| edge acutance | 0.32 | 0.32 | 0.37 | 0.35 | 0.37 | 0.38 | 0.37 | 0.42 | 0.32-0.42 | 0.47 | **0.39** |

**Other checks:**
- Loudness is −14.0 LUFS with true peak −2.1 dBTP.
- The staging and caption gate (auto.py) passes.
- Runtime is 58.9 s (references 40-65 s).

**Result:**
- Every measured check is inside the references' range except moves per 10 s (11.0 against a maximum of 9.6), which is slightly busier.
- Plan step 1 targets are met: moving ≥ 95 %, median ≥ 5 px/f, quiet-frame zoom ≥ 70 %, ≤ 3 hard cuts, ≤ 12 jumps.
- Plan step 2 targets are met: 3.6-3.9 words/s and at most one gap of 0.8 s or more.

**Data and tools:**
- `research/references/data/story_lane_v5_data.json`
- `run_one.sh`, `parity_table.py` and `summ_keys.py` in the same folder. They are the Spark working copies, using the paths in `~/studio/scratch/storylane/`.

### Frame review (pipeline/qa/REVIEW_PROMPT.md §3, frames30 sheets, reviewers per 10-20 s)

There were seven rounds (one per fix render), each with 3-6 frame-reviewer agents reading every sheet. They found and
fixed:
- faces cut at the eyes by push-ins, and subjects drifting out of frame. The fix was the "toward" drift mode and
  per-framing push caps;
- hands popping in and out of the board close-ups;
- a king toppling with nothing touching it;
- captions over the board and over the hidden man;
- the candle popping in unlit;
- Paris dropping off the map;
- the museum's empty bottom third;
- the seat slide snapping, with the man visible through his open door;
- same-set double images;
- floating labels;
- the smoke trail playing while the turban was off-screen;
- a cramped ending.

**Still open:** the last round still found these, and in any round some of them are borderline calls:
- Two crossfades between framings of the same hall (10.3 s, 23.7 s) are matched on the Turk. The other figures still
  ghost slightly for about 4 frames.
- The push-in that ends p02 slides the Empress and the inventor off the frame edges at 9.8-10.3 s. This is a push past
  them, not a hold.
- Some caption pages break mid-phrase ("HE OPENED" / "IT UP"). Paging is shared code (`phrases.py`) and was not changed here.
- Doors open with no hand on them, and the candle is held in front of the doors rather than behind them.
- Chess hands leave in 3-4 frames.
- The museum flares up in about 4 frames, and one flame sits over the burning Turk's face.
- The smoke trail crosses the Turk's face.
- The MAGNETS and LEVER chips sit at the board's edge, and the magnets are small.
- The court shot leaves the Turk out.
- Sets are still flat layered 2D. Characters are not lit by the scene light and there is no parallax beyond depth 0.9
  against 1.0 (gap 2 in the check). See the 3D cost test in docs/RND_LOG.md.

**Not done yet:** the blind side-by-side panel (PARITY.md §2) and the owner's phone check (§3).
