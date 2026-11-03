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

## 2026-11-02 · story lane · story-chess-turk v6 (v5 open items) + the blind panel

**Video:** `out/story-chess-turk/story-chess-turk_v6.mp4` (58.9 s, sha256 `944a2e6b…`), phone copy
`out/story-chess-turk/story-chess-turk_v6_phone.mp4` (16.7 MB). Same voice and mix as v5 (−14.0 LUFS, TP −2.1 dBTP).

### What changed from v5

- **One hall, no same-room dissolves.**
  - p02 (interior) to p06 now share one layout: the same Turk, inventor and court in the same places.
  - Each scene starts where the last camera ended (`cont`). `story_camera.py` now joins `cont` scenes seamlessly
    (no crossfade), so 10.3 s and 23.7 s read as camera moves.
  - The cutaway scenes p10 to p12 are joined the same way.
  - Poses, faces, props, the dimmed room and the candle glow are carried across every join.
  - The p03 court laughs at the Turk in the same shot. The p06 count is the man from the court, seated.
  - The p02 push-in past the Empress is gone.
- **Hands on the doors.**
  - He walks along the cabinet and his free hand is on each door as it swings.
  - In the hook only the left door opens, by hand.
  - In the cutaway the gear-side door opens first; he slides on "slid", and only then do his doors open.
- **Candle:** it stands on the cabinet top. He reaches up and takes it on "candle", holds it into the open left bay
  (the light now pools in that bay), and sets it back before winding the key.
- **Chess hands:** they enter over 13 frames, decelerating, and leave over 21 frames with a slow start. Napoleon's arm
  comes from his side. The next hand starts only after the last piece has landed.
- **Fire, smoke, labels:**
  - The museum fire builds over about 1.1 s.
  - No flame sits over the Turk's face.
  - The smoke trail goes up his back to the neck, and puffs leave the turban.
  - Labels leave with a 0.3 s fade.
  - The master's hand blends onto the lever.
  - The room stays dark under the newspaper.

### Measured (same tools; v6 = the bold column)

| Check | refs range | v4 | v5 | v6 |
|---|---|---|---|---|
| words/s · pauses ≥ 0.8 s | 3.33-3.89 · 0-1 | 3.13 · 5 | 3.79 · 0 | **3.79 · 0** |
| hard cuts · one-frame jumps | 0-3 · 0-12 | 20 · 54 | 2 · 3 | **2 · 3** |
| camera moving % · median px/f | 96-100 · 5.76-11.09 | 70 · 0.58 | 99 · 5.87 | **100 · 5.46** |
| moves/10 s · quiet-frame zoom % | 5.1-9.6 · 69-88 | 2.1 · 29 | 11.0 · 75 | **10.9 · 74** |
| saturation · colourfulness | 0.41-0.61 · 23-34 | 0.73 · 61 | 0.45 · 30 | **0.45 · 30** |
| luma p50 · non-ink p5 | 0.31-0.58 · 0.09-0.23 | 0.24 · 0.14 | 0.39 · 0.22 | **0.41 · 0.22** |
| shadow chroma · hue | 9-35 · violet-blue | 83 · 306 | 29 · 292 | **29 · 292** |
| ink edge · soft edge % · acutance | 0.54-0.66 · 3.8-14.6 · 0.32-0.42 | 0.17 · 1.5 · 0.47 | 0.59 · 5.4 · 0.39 | **0.60 · 5.3 · 0.39** |

Everything is inside the references' range except moves per 10 s (10.9 against a maximum of 9.6).

### Frame review

There were four every-frame rounds on v6 (3 reviewers each, frames30 sheets), plus still checks of the last fixes.

**Fixed:**
- the ghosted joins;
- doors opening without a hand;
- the candle popping in;
- the candle-to-key pop;
- the glow lighting the wrong bay;
- fast hand exits;
- the fire flare;
- smoke over the face;
- the label blink;
- the lever snap;
- the backdrop swap under the newspaper;
- captions over the inventor's face;
- his face cut at the left edge (he now stands at x 16 %).

**Still open:**
- In the Turk close-ups (11.6-13.6 s) the inventor sits right above the caption band.
- The board inserts in p01, p06 and p08 are still dissolves: a different framing of the same room.
- The sweep reads small.
- The map shows two pins and no route.
- The Turk only darkens; he does not visibly turn to ash.
- The newspaper picture is unreadable.
- The hidden master is not visibly "folded".
- The magnets are small.
- Gear angles jump a few degrees at two joins.

**Caption pages that break mid-phrase** (shared paging in `phrases.py`; left alone while the kurz lane renders with it):

| Now | Would be |
|---|---|
| "THAT BEAT NEARLY / EVERY PLAYER," | "THAT BEAT / NEARLY EVERY PLAYER," |
| "HE OPENED / IT UP" | "HE OPENED IT UP" |
| "INTO THE EMPRESS'S / PALACE IN VIENNA." | "INTO THE EMPRESS'S PALACE / IN VIENNA." |
| "SITS A LIFE-SIZE / WOODEN MAN" | "A LIFE-SIZE WOODEN MAN" |
| "AT A CHESS / BOARD." | "AT A CHESS BOARD." |
| "THE WHOLE / COURT LAUGHS." | "THE WHOLE COURT LAUGHS." |
| "ONE BY ONE AND HOLDS / A CANDLE / BEHIND THEM." | "ONE BY ONE / AND HOLDS A CANDLE BEHIND THEM." |
| "HE WINDS / A KEY." | "HE WINDS A KEY." |
| "BRAVE ENOUGH / TO PLAY / IT GETS CRUSHED." ("play it" split) | "BRAVE ENOUGH TO PLAY IT / GETS CRUSHED." |
| "NO ONE / IS LAUGHING NOW." | "NO ONE IS LAUGHING NOW." |
| "THEN A MUSEUM / FIRE BURNS" ("museum fire" split) | "THEN A MUSEUM FIRE / BURNS THE TURK TO ASH," |
| "THERE WAS A MAN / INSIDE." | "THERE WAS A MAN INSIDE." |
| "WHEN EACH DOOR / OPENED, HE SLID / HIS SEAT" | "WHEN EACH DOOR OPENED, / HE SLID HIS SEAT" |
| "MAGNETS UNDER / THE BOARD SHOWED / HIM EVERY MOVE," | "MAGNETS UNDER THE BOARD / SHOWED HIM EVERY MOVE," |
| "AND A LEVER MOVED / THE TURK'S HAND." | "AND A LEVER / MOVED THE TURK'S HAND." |
| "IN A BOX, PLAYING / BY CANDLELIGHT." | "IN A BOX, / PLAYING BY CANDLELIGHT." |

**The rule I'd add:**
- Never end a page on an article, preposition, auxiliary or conjunction (a, the, at, to, into, and, was).
- Never split a noun phrase ("museum fire", "chess board") or a verb from its object ("play it", "showed him").

### Blind side-by-side panel (PARITY.md §2)

**Setup:**
- Eight pairs: v6 against each of the 8 references.
- Each video is a sheet of 16 matched-moment frames: 0, 0.5, 1, 2 and 3 s, then 10-90 % of the runtime, then the last
  1.5 s and 0.2 s.
- Judges also got both narration transcripts.
- A/B order came from a coin: `sha256(sha256(v6) + sha256(ref)) mod 2`.
- Three independent judge agents rated every FEEDBACK.md principle per pair and listed concrete flaws.
- Ratings and the key are in `research/references/data/story_lane_v6_panel.json`. The frame sheets hold reference
  screenshots, so they are not in the repo.

**Per principle:**

| Principle | J1 | J2 | J3 | Judges with ours ≥ same tier (in ≥ 5 of 8 pairs) | Concrete flaw named in ours | Verdict |
|---|---|---|---|---|---|---|
| 1 Hook first | 8/8 | 7/8 | 8/8 | 3/3 | none | **pass** |
| 2 World makes sense | 8/8 | 8/8 | 8/8 | 3/3 | (edge-cut courtiers at 23.6 s; counted under 5) | **pass** |
| 3 Show what's said | 3/8 | 1/8 | 5/8 | 1/3 | one hall for 0-27 s, cutaway held 47-59 s; "museum fire" shows the newspaper | **fail** |
| 4 Consistent and smooth | 8/8 | 8/8 | 8/8 | 3/3 | none | **pass** |
| 5 Readable on a phone | 8/8 | 8/8 | 8/8 (ours better in 7-8/8) | 3/3 | mid-phrase caption pages; NEW YORK/PARIS labels collide (29.5 s); court figures cut by the right edge (23.6 s); caption on the cabinet art | **fail** (flaw rule) |
| 6 Natural sound (transcript only) | 8/8 | 8/8 | 7/8 | 3/3 | none | **pass** (voice itself not judged) |
| 7 Quality over novelty (craft) | 0/8 | 0/8 | 0/8 | 0/3 | flat 2D vector sets against lit 3D/painterly sets | **fail** |
| 8 Pay off the promise | 8/8 | 8/8 | 8/8 | 3/3 | none | **pass** |

- **Overall per judge (ours same tier or better):** J1 2/8, J2 2/8, J3 4/8. Ours was never rated better overall
  except by J3 in 2 pairs, the ones with the references' world errors.
- **Blindness:** all three judges named the two pipelines at once ("flat 2D vector" against "stick figures in lit 3D
  or painterly sets").

**Verdict: FAIL (principles 3, 5 and 7).**

**Why each failed:**
- **7 (craft).** This is gap 2 from the check: the references are lit 3D/painterly worlds with depth. The grade, ink and
  blur numbers now match, but flat layered SVG sets do not. Fix: plan step 4 (one 3D set, end to end), which the cost
  test says is affordable.
- **3 (show what's said).** The v6 one-hall staging, done to kill the dissolve ghosts, means 0-27 s is one room and
  47-59 s one cutaway. The references move through 5-8 settings a minute. Fix: more places and angles per beat (court
  balcony, a workshop, the road, Paris and Vienna rooms, the board underside), each a real set.
- **5 (readable).** Ours actually wins this on ratings in nearly every pair. It fails on named flaws, all cheap except
  the caption paging: the map label collision, the edge-cropped court at 23.6 s, and captions over the cabinet art.

**Not run:** the owner's phone check (§3), which waits for a version that passes §2.

## 2026-11-02 · story lane · story-chess-turk v7: the 3D pipeline check (no review, no panel)

The owner had already posted the Chess Turk, so v7 is only used to check the 3D story pipeline
(`experiments/three-lane/src/turk`, composition `Turk3D`). There was no frame review, no panel and no further rounds.

- **Render.** 1768 frames at 1080×1920 took 3123 s on the Spark CPU (SwiftShader, concurrency 4, niced), about 1.8 s per frame.
- **Output.** `out/story-chess-turk/story-chess-turk_v7.mp4` (sha 1d5077c8…).
- **Shots.** 10 shot groups: hall, courtyard, the hall from 14 solved angles, map, Paris, Napoleon at night, museum fire, gallery burn, workshop cutaway, hall at night. They join with 7-frame dissolves between places, with 2 hard cuts (fire, reveal).

| Metric (refs' range) | v6 (2D) | v7 (3D) | |
|---|---|---|---|
| moving % · median px/f (≥95 · ≥5) | 99.5 · 5.46 | 99.1 · **11.38** | in |
| quiet-frame zoom (≥70 %) | 74 % | 70 % | in, at the edge |
| hard cuts · one-frame jumps (≤3 · ≤12) | 2 · 3 | 3 · 6 | in |
| moves / 10 s (5.1-9.6) | 10.9 | **8.3** | now in |
| saturation p50 (0.41-0.61) | 0.448 | 0.585 | in |
| colourfulness (23-34) | 30.1 | **22.1** | just low |
| luma p50 (0.31-0.58) | 0.408 | **0.292** | just low |
| non-ink p5 (0.09-0.23) | 0.22 | **0.045** | low: crushed darks, 6 % black area |
| shadow chroma (≤35) | 29 (violet) | 20 (hue drifts warm) | in, but not violet |
| ink edge · soft edge · acutance (0.54-0.66 · 4-15 % · 0.32-0.42) | 0.60 · 5.3 % · 0.39 | 0.66 · 5.2 % · 0.36 | in (ink at the top edge) |

- **What the 3D pipeline gets right.** Camera motion and pace now land inside every reference range: moves per 10 s fell from 10.9 to 8.3 because the 3D glides are longer and smoother. Ink and blur also match.
- **What to fix in the kit.** The night and fire presets crush the darks. The next episode lifts the black point in the grade (shadow floor) and keeps the shadows violet, to bring non-ink p5, luma and colourfulness back into range.
- **Also noted.** `camera_motion.py` cannot fit a 2D similarity to 3D parallax on 152 frames ("unfit"). This is expected for real 3D and is not a fault.

## 2026-11-02 · story lane · story-vasa v1-v14: the first episode built on the 3D kit, with three blind panel rounds

- **Topic.** The Vasa (Stockholm, 1628).
- **Script.** The adopted narration from `research/library/STORY_SCRIPT_REVIEWS.md`: 62 s at 3.8 words/s, with "You see" at 43.8 s (70 %). The script judge scores it 95.3.
- **Build.** `experiments/three-lane/src/vasa` on the kit, rendered on the Mac (`RENDER_SLOT=mac`, `--gl=angle`, concurrency 4). Each render passes through `scripts/repair_frames.py` to remove the GPU's tiled "mosaic" frames.
- **Final.** `out/story-vasa/story-vasa_v14.mp4` (sha 6afb1cc7…). The phone copy, `story-vasa_v14_phone.mp4`, is 25.9 MB.

### Measured (same tools and flags as above, every frame; v14 is the final)

| Metric (refs' range) | v9 | v10 | v11 | **v14** |
|---|---|---|---|---|
| words/s · pauses ≥ 0.8 s (3.33-3.89 · 0-1) | 3.8 · 0 | 3.8 · 0 | 3.8 · 0 | **3.8 · 0** |
| hard cuts · one-frame jumps (0-3 · 0-12) | 2 · 12 | 2 · 13 | 2 · **15** | **1 · 6** |
| moving % · median px/f (96-100 · 5.8-11.1) | — | — | 99 · 6.6 | **100 · 6.3** |
| moves / 10 s (5.1-9.6) | **10.96** | — | 9.67 | **9.34** |
| quiet-frame zoom (69-88 %) | — | — | 78 | **79** |
| saturation · colourfulness (0.41-0.61 · 23-34) | — | — | 0.557 · 29 | **0.563 · 29** |
| luma p50 · non-ink p5 (0.31-0.58 · 0.09-0.23) | — | 0.321 · — | 0.364 · 0.146 | **0.350 · 0.144** |
| shadow chroma · hue (9-35 · 36-306) | — | — | 21 · 56 | **21 · 56** |
| ink edge · soft edge · acutance (0.54-0.66 · 3.8-14.6 % · 0.32-0.42) | — | 0.517 (low) | 0.597 · 5.7 · 0.374 | **0.584 · 6.5 · 0.367** |

v14 is inside every reference range. Two changes brought the last two rows in:
- **Jumps (15 → 6).** Whips now overlap 3 frames under a 16 px smear, instead of 2 frames under 13 px.
- **Moves.** The ending runs four slower rolls instead of six quick ones.

Checks from `research/library/RICKSCLIPS_RULEBOOK.md` §4 that the existing outputs already cover (v14):

| Check | v14 | Reference range |
|---|---|---|
| shot length, median · max | 3.3 · 8.0 s | 1.67-3.6 · 4.7-14.9 s |
| transitions per minute | 16.4 | 9.2-24.8 |
| first transition | 3.37 s | 0.7-12.4 s |
| move attack · release (median) | 11 · 11.5 f | 4.5-20.5 · 4.5-34 f |
| snap moves | 4 | 0-14 |
| hold | 0 % | 0-4.7 % |
| jump flags per minute | 5.8 | — |
| shot groups (17 joins) | 18 in 62 s | — |
| distinct places | 7: harbour/deck, camp, quay, gun deck, hall, explanation room, ballast quay | 5-17 |

**Still open from the rulebook** (not built in this episode):
- caption pages of 1-3 words in mixed case (an owner decision, because FEEDBACK.md principle 5 asks for whole-phrase captions);
- match transitions (0);
- face swaps anchored to caption words;
- glints and an fx library;
- ambient movers;
- tweened relights.

### Every-frame review
Each render was reviewed on 30 fps sheets, along with a camera-replay framing check (`scripts/framing.ts`). Fixes, by version:

- **v11**
  - The ending is filmed over open water with no sheds.
  - The wobble crew stays whole beside the rocking hull, then the masts swing on "wobbles".
  - The hearing room has no throne.
  - The guns run out before "two".
  - The sails are fuller and the ink is wider.
- **v14**
  - The gun decks are framed a few ports at a time, so the bronze guns read.
  - The launch is split into two whip-joined shots, so the camera no longer flies through the rigging or sits inside a shed.
  - The camp and letters close-ups keep every figure whole.
  - The hearing captions are moved clear of the king's portrait.
  - `repair_frames` now also catches two mosaic frames in a row.
- **Kit additions**
  - `CamKey.drift`;
  - `hallSet({throne})`;
  - `harbourSet({sheds})`.

### Blind side-by-side panel (PARITY.md §2): three rounds, 3 judges, 8 pairs each
Each cell is the number of pairs, out of 8, in which a judge rated ours same-or-better.

| Principle | Round 1 (v9) | Round 2 (v10) | **Round 3 (v14)** |
|---|---|---|---|
| 1 Hook | pass | 8 · 8 · 7 | **8 · 8 · 8** |
| 2 World | pass | 8 · 8 · 8 | **8 · 8 · 8** |
| 3 Show what's said | fail (flaws) | 8 · 8 · 4 | **8 · 8 · 8** |
| 4 Smooth | pass | 8 · 8 · 8 | **8 · 8 · 8** |
| 5 Readable | fail (flaws) | 8 · 8 · 8 | **8 · 8 · 8** |
| 6 Sound | pass | 8 · 8 · 8 | **8 · 8 · 8** |
| 7 Craft | fail (flaws) | 4 · 8 · 0 | **8 · 0 · 8** |
| 8 Payoff | pass | 8 · 8 · 3 | **8 · 8 · 8** |

**Verdict after the last allowed round: FAIL by the flaw rule on principles 1, 2, 3, 4, 5 and 7. Principles 6 and 8 pass outright.**
- **On ratings, it passes.** All 8 principles pass at ≥ 5/8 for ≥ 2 of 3 judges; craft is 2 of 3.
- **Why judges preferred ours.** Whole-phrase captions, a world that stays in one place and era, a progress gauge, and a payoff that lands. The references lost on one-word captions over faces, edge cuts, ghosted dissolves and world slips.
- **What fails it.** The flaw rule fails a principle whenever any judge names a concrete defect in ours, and every judge named some. Full data: `research/references/data/story_lane_vasa_panel.json`.

The named defects, by principle:
- **1 Hook.** The thirty sailors are tiny on the far rail at 0-3 s. All 3 judges named this.
- **2 World.** The heel gauge peaks at 9° in the opening dock test but at 19-20° when the ending replays the same test, and it climbs while the visible tilt barely changes.
- **3 Show what's said.**
  - At 12.4 s the ports are still closed on "mightiest warship".
  - At 18.6 s the wobble does not read in a still.
  - At 49.6 s "built upside down" plays over the bottle tank.
- **4 Smooth.** The opening holds one side-on framing for about 5 s.
- **5 Readable.**
  - Captions over the rigging (18.6 s), the gun-port row (2-3 s) and legs (37.2 s).
  - Small HUD labels.
- **7 Craft.**
  - Edge cuts: the stern banner (60.6 s), a sailor (61.9 s), the bow (18.6 s) and the crowd (24.8 s).
  - A glow over the cross-section at 55.9 s.
  - A flat, low-detail look, named by judge 2.

**Next fixes (cheap ones first):**
1. One heel scale for the dock test (the opening and the callback must match).
2. Hook framed on the runners at mid-deck.
3. Ports open from 12.0 s.
4. A caption gate that keeps captions off rigging and gun-port rows (the rulebook's `caption_on_face_frames`, extended to the busy bands).
5. The solver keeps the stern inside the frame in the last shot.
6. The rulebook's build order for craft: faces on the word, an fx library, insert sets, match transitions.

**Not run:** the owner's phone check (§3), which waits for a version that passes §2.

### story-vasa v15 and panel round 4 (the last on Vasa)

The coordinator asked for a v15 with only the cheap fixes for the flaws round 3 named, then one more panel round.
The output is `out/story-vasa/story-vasa_v15.mp4` (sha a5c8af61…), with a 25.9 MB phone copy, `story-vasa_v15_phone.mp4`. Captions are unchanged: their style is waiting on the owner.

**Fixes (by round-3 flaw):**
1. **Heel scale.** The opening test and the ending callback now share one heel scale (`RUN_DUR`, `RUN_GAIN`). Both peaks read 18°, where before they read 9° and 19°.
2. **Hook.** It is framed on the crew as one column up the deck, from two angles joined by one glide, with every runner in frame and the captions on open deck.
3. **Gun ports.** They are open from 12.0 s.
4. **Wobble.** It is filmed bow-on with the whole ship. A slower roll of ±11° lands on "wobbles", and the gauge shows it.
5. **"Built upside down".** The line now plays over the Vasa's own section. It drops in on "The Vasa", reads HEAVY on top and LIGHT below, and rocks in its tank.
6. **The 5 s side-on hold.** It is gone. The hook and the ending each use the column shots, and the ending whips to the stern quarter on "at the dock".
7. **Captions and HUD.**
   - New kit hooks: `GroupSpec.busy(t, cam)` marks the rigging and the camera-side port rows; `Episode3D` takes `screenAvoid` for HUD panels.
   - Caption placement weights busy bands 3× and faces and panels 8×.
   - A caption gate in `scripts/framing.ts` exits 1 when any page sits more than 12 % over a face, a busy band or a panel. It still flags two hook pages at 13-14 %, which the stills show over plain deck.
   - The gauge is now labelled HEEL and is bigger, the DISTANCE panel is bigger, and the distance panel now appears from the first gust.
8. **Framing.** The stern banner and every sailor stay in frame (the replay framing check is clean in every Vasa group).

**Also fixed:** `repair_frames.py` now scans every tile period. A mosaic with a 59/160 period slipped through at 59.4 s.

**Measured (v15).** All 17 checks are inside the reference ranges:

| Check | v15 |
|---|---|
| words/s | 3.8 |
| pauses ≥ 0.8 s | 0 |
| cuts · jumps | 1 · 7 |
| moving | 100 % at 6.0 px/f |
| moves / 10 s | 8.86 |
| quiet zoom | 81 % |
| saturation · colourfulness | 0.566 · 29 |
| luma p50 | 0.314 (the floor) |
| non-ink p5 | 0.137 |
| shadow chroma · hue | 20 · 54 |
| ink · soft edge · acutance | 0.59 · 6.6 % · 0.373 |

The rulebook checks are also in range:

| Check | v15 |
|---|---|
| shot length, median · max | 3.33 · 8.0 s |
| transitions per minute | 16.4 |
| first transition | 3.4 s |
| move attack · release (median) | 9 · 9 f |
| snap moves | 3 |
| hold | 0.2 % |

**Every-frame review (30 fps sheets).** Clean apart from one transient: the stern banner touches the left edge for about 0.2 s during the glide at 60.7 s.

**Panel round 4 (v15).** Each cell is the number of pairs, out of 8, in which a judge rated ours same-or-better (judges 1 · 2 · 3).

| Principle | Round 3 (v14) | **Round 4 (v15)** | Flaw rule (round 4) |
|---|---|---|---|
| 1 Hook | 8 · 8 · 8 | **8 · 8 · 8** | fail: masts cut at the top, sailors still small in the overhead deck shot |
| 2 World | 8 · 8 · 8 | **8 · 8 · 8** | fail: the gauge swings 6°, 2°, 10° as the crew runs back and forth, which reads as jumping backwards |
| 3 Show what's said | 8 · 8 · 8 | **8 · 8 · 8** | fail: a bare-masted hull at 18.6 s; DISTANCE never named in the narration; the sinking is not clear at 31 s |
| 4 Smooth | 8 · 8 · 8 | **8 · 8 · 8** | **pass** (was a fail) |
| 5 Readable | 8 · 8 · 8 | **8 · 8 · 8** | fail: gauge over the mast top at 18.6 s; HEAVY/LIGHT labels small; captions over legs (37 s) and the diagram bottom (56 s) |
| 6 Sound | 8 · 8 · 8 | **8 · 8 · 8** | pass |
| 7 Craft | 8 · 0 · 8 | **5 · 5 · 8** (3 of 3) | fail: crowd cut at 24.8 s, banner at the edge at 60.6 s, flat sparse water and sky |
| 8 Payoff | 8 · 8 · 8 | **8 · 8 · 8** | pass |

**Verdict after the last allowed round: FAIL by the flaw rule on principles 1, 2, 3, 5 and 7.** Principles 4, 6 and 8 pass outright.
- **On ratings, it passes.** All 8 principles pass with all 3 judges, and craft goes from 2 of 3 judges to 3 of 3.
- **Which flaws are new.** None of the round-3 flaws that v15 targeted (the 9°/19° gauge mismatch, ports closed at 12.4 s, "upside down" over the bottles, the 5 s hold, captions over the rigging and port row) was named again. The flaws named now are new ones, or ones v15 did not touch: the overhead hook still reads small, the oscillating gauge, label size, and the flat look.

Full data: `research/references/data/story_lane_vasa_panel.json` (rounds 3 and 4).

## 2026-11-02 · story lane · story-barca-shield v1-v14: the first episode on the integrated kit, three blind panel rounds

- **Topic.** Barca, c. 515 BC: the bronze-smith whose shield rang over the Persian mines. It is rank 1 in STORY_TOPIC_QUEUE.md.
- **Script.** The script track's draft, fact-checked against Herodotus 4.200, Aeneas Tacticus 37.6-7 and the Wikipedia article on Barca.
  - **Two fixes.** The attacks never stopped; the mines were dug while the walls were assaulted. Barca was inland, not "on the coast".
  - **Judge.** 100 on estimated timings, 98.1 on the voiced timings.
- **Audio.** Profile `story_ricks` at speed 1.18: 3.74 words/s, no gap above 0.08 s, last word at 57.35 s.
- **Captions.** The hybrid: the reference look with one-line phrase pages (`caption_rule: phrase1`, `captions="ricks-phrase"`).
- **Build.** `experiments/three-lane/src/barca` on the integrated kit, gates set to fail. Every rendered version passed the hold, cast, edge and caption gates.
- **Final.** `out/story-barca-shield/story-barca-shield_v14.mp4` (sha 15d6d0ad…). The phone copy is 24.4 MB.

### Measured (v14, every frame)

All 17 checks are inside the reference ranges:

| Check | v14 |
|---|---|
| words/s | 3.74 |
| pauses ≥ 0.8 s | 0 |
| cuts · jumps | 2 · 7 |
| moving | 99 % at 6.39 px/f |
| moves / 10 s | 9.17 |
| quiet zoom | 81 % |
| saturation · colourfulness | 0.503 · 24 |
| luma p50 · non-ink p5 | 0.518 · 0.224 |
| shadow chroma · hue | 16 · 300 |
| ink · soft edge · acutance | 0.605 · 5.9 % · 0.334 |

The rulebook checks are also in range:

| Check | v14 |
|---|---|
| shot length, median · max | 3.43 · 7.4 s |
| transitions per minute | 15.6 |
| first transition | 0.77 s |
| move attack · release | 9 · 9 f |
| plan | 20.8 place changes/min, 11 places |
| cast | median head 0.114, 63 % ≥ 0.07 |

How v1 got into range:
- **Jumps (56 → 7).** The whips were lengthened from 0.4 to 0.6 s.
- **Luma (0.60 → 0.52).** Darker ground and walls, with day and golden light leaned toward night.
- **Acutance.** Less lens blur on the world shots.
- **Motion.** Fewer camera keys plus slow orbits.

### Blind panel (PARITY.md §2): 3 rounds, 3 judges, 8 pairs

Each cell is the number of pairs, out of 8, in which a judge rated ours same-or-better (judges 1 · 2 · 3).

| Principle | Round 1 (v7) | Round 2 (v12) | **Round 3 (v14)** |
|---|---|---|---|
| 1 Hook | 0 · 0 · 0 | 0 · 0 · 0 | **0 · 0 · 0** |
| 2 World | 8 · 8 · 4 | 4 · 2 · 7 | **8 · 8 · 8** |
| 3 Show what's said | 0 · 0 · 5 | 0 · 0 · 0 | **0 · 1 · 0** |
| 4 Smooth | 0 · 8 · 8 | 8 · 2 · 8 | **8 · 8 · 3** |
| 5 Readable | 8 · 8 · 8 | 8 · 8 · 8 | **8 · 8 · 8** |
| 6 Sound | 8 · 8 · 8 | 8 · 8 · 8 | **8 · 8 · 8** |
| 7 Craft | 0 · 0 · 0 | 0 · 0 · 0 | **0 · 0 · 0** |
| 8 Payoff | 4 · 8 · 7 | 5 · 2 · 8 | **8 · 8 · 3** |

**Verdict after the last allowed round: FAIL on the ratings for hook, show what's said and craft (0 of 3 judges each).**
- World, smooth, readable, sound and payoff pass on ratings.
- Every principle also fails the flaw rule.

Unlike Vasa, this is a ratings failure, not just named flaws. The judges preferred the references' richer, finished sets.

**What the judges said:**
- **Hook.** Frame 0 never shows the odd act (the shield laid in the dirt) together with the army.
  - Round 1: a static smith at a wall.
  - Round 3: a shouting Persian at the wall, with the smith only from 1.8 s.
- **Show what's said.**
  - The siege and the hammering are barely shown.
  - "Kneels, listens" plays with the smith standing (the Actor's crouch is shallow).
  - The map doesn't read as Libya.
- **Craft.**
  - Flat, low-detail sets.
  - One tunnel cut held about 17 s from 40 s to the end.
  - Near-identical end frames.
  - Shields and figures cut at the edges in single frames.
  - The Actor's arms read as detached.
- **Wins.** All three judges credited the whole-phrase captions (readable 8/8 every round) and the coherent world. The references' recurring losses were one-word captions, edge cuts, ghosted dissolves and era mismatches.

**Kit findings for the visual track:**
- The Actor's head highlight was drawn as an ink arc from ear to mouth that read as a headset microphone (round 1, all 3 judges). Fixed in f91c214.
- The Actor's `crouch` reads as standing at phone size; a real kneel pose is needed.
- The arm-to-hand joint reads as detached.
- The gates pass shots that judges still call static or empty (a held cross-section, a void around a table): the hold gate counts view changes, not visual change.

Full data: `research/references/data/story_lane_barca_panel.json`.
