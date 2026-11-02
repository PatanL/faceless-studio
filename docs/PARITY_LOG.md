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
