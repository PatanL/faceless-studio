# Pilot QA: side-by-side review against the references

Written 2026-11-01 ~11:35 UTC from the review-round results of the QA workflow; closeout added ~12:20 UTC (see "Closeout (11:35-13:40 UTC)"). Each round had two reviewers:
a **visual parity** reviewer (does it look like the `research/library/review-refs/<niche>/` references in a feed?) and a
**viewer / retention** reviewer (would a viewer watch to the end?). Sheets come from `scripts/side_by_side.sh`
(rows = shot classes, reference columns + pilot in the last column) and live in `out/qa/`.

Scores are given as each reviewer reported them. Most used /100; three used /10 (horror r1 visual 3/10, horror r2
visual 6/10, blue-whale r3 viewer 7/10). Where a round's two sheet files are byte-identical, the sheet is shown once.

Final verdicts at closeout (md5 = the exact file each verdict is for):

| Pilot | Cut | Cleared file (md5) | Last review (visual / viewer) | Final verdict |
|---|---|---|---|---|
| horror-pinned-rules | 9:16, 65.2 s | `horror-pinned-rules_9x16.mp4` (`14376d5d76a453b9fcbf22c542915e87`) | closeout c1: 80 PASS / 84 PASS | **PASS**, cleared to post |
| explainer-orca | 9:16, 75.1 s | none. Last reviewed `explainer-orca_9x16-prev.mp4` (`55793987a7dbd227e216683c22d5e0af`) | closeout regression: 72 FAIL | **FAIL**; `explainer-orca_9x16.mp4` (`8702a89c1e5e44ca4b4d9bf7ba737d2c`, fix pass 2) not reviewed |
| explainer-orca | 16:9, 75.1 s | none. Last reviewed `explainer-orca_16x9-prev.mp4` (`355d0d72cdebf46ec19837e359f08d52`) | closeout 16:9: 68 FAIL | **FAIL**; `explainer-orca_16x9.mp4` (`3ac1cbad7f12d78c521b05c9f6a0e258`) not reviewed |
| explainer-blue-whale | 9:16, 70.1 s | `explainer-blue-whale_9x16-prev.mp4` (`c1c5647ab05231848d86df6ce30f6cab`) | closeout regression: 77 PASS | **PASS** for that file; `explainer-blue-whale_9x16.mp4` (`491cdd4c60b0ee8ddf7030de8ff2c036`, fix pass 2) not reviewed |
| explainer-blue-whale | 16:9, 70.1 s | none. Last reviewed `explainer-blue-whale_16x9-prev.mp4` (`6847ebcab12637f867c5c078ab24eff0`) | closeout 16:9: 66 FAIL | **FAIL**; `explainer-blue-whale_16x9.mp4` (`08093d1acb11c6b415da5130eb5be240`) not reviewed |

Pre-closeout rounds: orca 2 rounds (round 2 74 / 80, recorded PASS, withdrawn in closeout as under the 75 bar), horror 3 rounds
(round 3 72 FAIL / 82 PASS), blue whale 3 rounds (round 3 80 / 7 of 10 PASS, on `d859720c…`, now `-prev2.mp4`).

Each pilot folder holds the posting package: the 9:16 MP4 (+ 16:9 for the explainers), `thumbs/` (3 thumbnails in
9:16 and 16:9, plus `sheet_*.jpg`), `titles.md`, `description.md` (with AI-voice / altered-content disclosure steps), and
`references.md` (the cited viral references and the beat alignment table). See "Package" under each pilot.

---

## 1. explainer-orca (P-explainer): round 2 PASS, closeout FAIL (see Closeout)

**Round 2 cut:** 75.115 s, 1080x1920, md5 55793987…, commit 10b036c; now `explainer-orca_9x16-prev.mp4` (the current
`explainer-orca_9x16.mp4` is the unreviewed fix-pass-2 cut, md5 8702a89c…). The 76.6 s round 1 cut (md5 79ef71a5…) is no
longer in the folder.

| Round | MP4 reviewed | Visual parity | Viewer / retention | Round result |
|---|---|---|---|---|
| 1 | 76.6 s cut (now `-prev`) | 60/100 FAIL (close) | PASS (no score given; reported 78) | FAIL |
| 2 | 75.1 s cut, commit 10b036c (final) | 74/100 PASS | 80 PASS | **PASS** |

### Round 1 (60 / 78): FAIL

![explainer-orca round 1, visual parity sheet](../qa/explainer-orca_r1_visual.jpg)
![explainer-orca round 1, viewer sheet](../qa/explainer-orca_r1_viewer.jpg)

<details><summary>Visual parity, 60/100, FAIL (close)</summary>

What already works: the flat-vector look of the kit is in the same family as fGcgWaswMns (Depth Theory). The navy-to-teal
gradient with god rays is on spec (#0a1b23 top, #2c6070 mid, #0c1f28 bottom). Red is mostly kept for accents (BIGGEST, SUNK,
the struck option, the counter underline). Captions are 2-4 word heavy white caps with a shadow at y≈1380 (inside SAFE_AREA).
The ~8 M ruler with the cars and 6 TONNES (6-9 s), the Gansbaai map, the sailboat with the snapped rudder and the
KILLER WHALE? loop bookend at 76 s hold up next to the references. The thumbnails are strong and on brief.

Why it would still look amateur in a feed:
1. Frame 0 (the Shorts cover) is a quiet mid-shot: white KILLER WHALE? header, orca at ~30% scale, a ~60 px diver, no claim, no red.
2. Several holds are 60-80% empty water: 10-16 s (speed bars, orca a sliver, tiny YOU), 50-56 s (options list alone), 72-74 s, 24 s (empty iceberg).
3. Two "you" art styles: the white stick figure (8 s, 54 s) clashes with the vector diver.
4. The diver is 60-110 px long at 1080 wide, smaller than its own YOU tag.
5. Collisions: the 0 WILD HUMAN KILLS card covers the diver at 2.5 s; three stacked orcas in Antarctica (24-28 s); a YOU tag with no body at 28 s.
6. Five different header treatments; the refs use one rule (centred, red underline).
7. Caption cards end on dangling words (YOU'RE SCARED OF / MAYBE THEY / AND THIS SMART / WHAT CHANCE).

Camera and motion are adequate (zoom keyframes in every scene, something new every 2-3 s). Storyboard start times run 1-2 s
ahead of the 2 s scrub; a few frames don't match the storyboard order (sailboat at 62.5 s vs p11 at 62.0 s; the p09 harbour
seal not visible at 52/54 s). episodes/README.md listed the orca at 89.4 s; it was a 76.6 s cut.
</details>

<details><summary>Viewer / retention, PASS (78)</summary>

Checked 1 s frames for 0-5 s and 2 s after, ebur128 / silencedetect / scene detection on the Spark CPU (nice, 2-4 threads).
The Spark's own `studio/out/pilots/explainer-orca/explainer-orca_9x16.mp4` was a stale 89.4 s render; don't QA against it.

Verdict PASS. Hook lands: frame 0 shows the orca at ~74% width, a YOU diver and KILLER WHALE?; the 10-word paradox ends at
2.9 s; 0 WILD HUMAN KILLS arrives at ~2.0 s. Scene/layer changes at least every ~1.5 s, caption cards every 0.5-1.5 s, no hold
over 4 s. Escalation reads well; red only on threat words; last frame = frame 0 (loop bookend, no CTA, PLAYBOOK S7).
Captions word-synced (31 onsets checked, lead 10-130 ms, median ~70 ms). Audio -14.1 LUFS, TP -1.1 dBFS, LRA 1.7, no
clipping; bed ~19-20 dB under the voice (barely audible on phone speakers). 205 wpm (band 180-230); hook 10 words / 2.9 s;
re-hooks at 48%, 61%, 81%; "you" ~11/min (target 12-20). At 76 s it is longer than any corpus outlier (max 59 s).
Script cites 3 references with a beat table; originality_check PASS.

Weak spots: (1) ~1.4 s dead air at the loop seam; (2) p09 options beat (49.4-54.3 s) is ~5 s of a small list on empty navy at
the highest drop-off point; (3) header styling, p01 car over the scale label, unreadable Iberia map, caption split
"THEY CAN'T.", two sheet rows unmatched. Sheet committed (a0c196d).
</details>

### Round 2 (74 / 80): PASS

![explainer-orca round 2, side-by-side sheet (visual and viewer sheets are identical)](../qa/explainer-orca_r2_visual.jpg)

<details><summary>Visual parity, 74/100, PASS</summary>

Next to fGcgWaswMns (style target) the pilot holds up: same flat-vector navy-to-teal ocean with god rays, clean orca, great
white and blue whale art, heavy caps headers with a red underline, red as the only accent (the 0, LIVER, BIGGEST, RAMMING,
SUNK). Captions ~75 px bold white caps with outline at y≈1330-1460, as readable as Zack D's 6mRR91AbxjQ. Frame 0 is the cover
"0 HUMAN KILLS" (one red word) over a large orca and a small YOU diver; last frame bookends it; the thumbnails match the
reference thumbnail grammar. A new layer or cut every 1-3 s, camera punches throughout, no hold over 4 s.

Five localized defects keep it below the references:
1. p04 Antarctica (21.7-27.6 s): the seal is never drawn, so "WASHES THE SEAL" plays over an empty floe. Cause: in
   `pipeline/episodes/orca_pilot.py` ~l.230 the seal sets opacity only on its last keyframe, and `studio/src/core/anim.ts`
   `sample()` returns the first defined keyframe value (0) for all earlier t.
2. The dark "menace" orca silhouettes in p06 (36-38 s) and p08 (45.9-49 s), #0a2531/#08202b on #06121c-#0b1a22, are invisible: an empty dark screen with a tiny diver.
3. p11 Iberia map (64.6-65.5 s): "IBERIAN ORCAS" label collides with orca icons and rings; PORTUGAL chip overlaps a ring; peninsula hard to recognise at zoom 15.
4. p12: the "~7 BOATS SUNK SINCE 2020" card touches the caption.
5. p01: the four cars at 8-9 s are clipped by both frame edges after the 1.19x punch.

Minor: "IN THE WILD" is low-contrast grey-teal on teal; surface-split scenes have a band (~#60a1b4) lighter than the README's
#2a6a8a cap; the filled white YOU figure looks plainer than the diver art.
</details>

<details><summary>Viewer / retention, 80, PASS</summary>

75.1 s, commit 10b036c. Hook passes (frame 0 cover, 10 words in 2.9 s, red COULD KILL at 1 s; PLAYBOOK S1 and H6). Visual
change passes (10 fps frame-diff: no 2 s stretch without change). Caption sync passes (onsets +0.05 to +0.14 s, one +0.29 s at
9.8 s; captions match speech at 11 spot checks). Audio -14.0 LUFS, LRA 1.6, TP -1.2 dBTP, no clipping, bed 13.8 dB under the
voice, ducked 11 dB. 204 wpm; 12 "you" per minute (edge of 12-20); turnstile at 49% with a hard cut. Loop bookend, no CTA.
Script cites VtrcKTkhDHU, fGcgWaswMns, jw6bS-WL4F4 with a beat table; originality_check PASS. Matches fGcgWaswMns on the
review-ref rules.

Problems: headline/tag swaps crossfade into garbled double text at 43.1-43.4 s and 56.8-57.1 s (lighter at 59.0 s); the orca
shadow is invisible in the turnstile beat (36-38 s is YOU alone); the "3 SECONDS TO REACH YOU" card touches the caption at
17 s; an orphan "OF" on caption line 3 at 29 s. Risks: average sentence 7.7 words with many full stops (PLAYBOOK wants chained
clauses); 75 s is longer than any Short outlier in the corpus (28-59 s). Sheet committed (b1cdfea).
</details>

### What still falls short of the references (orca)

- **Missing seal in p04 (21.7-27.6 s)**: the caption says the wave washes the seal off, but no seal is drawn (keyframe opacity bug in `orca_pilot.py` / `anim.ts sample()`). This is the one story/visual mismatch.
- **Invisible "menace" orcas at 36-38 s and 45.9-49 s**: near-black on near-black; those beats read as an empty screen at the turnstile, the likeliest swipe point.
- **Text collisions**: the 3 SECONDS card (17 s) and the ~7 BOATS SUNK card (p12) touch the caption; the Iberia map labels collide (64.6-65.5 s).
- **Crossfade double text** at 43.1-43.4 s and 56.8-57.1 s; an orphan "OF" caption line at 29 s.
- **Framing**: the cars clip both edges at 8-9 s; the plain filled YOU figure next to the diver art.
- **Structure**: 75 s is longer than every corpus Short outlier (28-59 s); "you" density sits at the bottom of the band.
- **16:9 cut (new, rendered ~11:31 UTC on the Spark CPU, 72 s at concurrency 4 from the current storyboard)**: the frame-0 "0 HUMAN KILLS" header is cropped at the top edge by the cover push-in (the last frame is fine). Long-form uses the custom thumbnail, so this is cosmetic, but `pipeline/episodes/reformat.py` should clamp the push-in so headers stay in frame.

### Package (`out/pilots/explainer-orca/`)

| File | Status |
|---|---|
| `explainer-orca_9x16.mp4` | re-rendered 2026-11-01 ~12:11 UTC on the Spark CPU (commit f7031ad), 75.1 s, 1080x1920, md5 8702a89c…: 2nd explainer fix pass (seal on the floe 21.7-25.5 s and washed off, lit menace silhouettes p06/p08, sequential header/tag swaps at 43 s and 57 s, ~7 BOATS card at y 50 %, cleaner Iberia map, diver-style YOU, short low impact flash, least-cost caption pages with number/unit joins). The round 2 PASS cut is `-prev.mp4`. |
| `explainer-orca_16x9.mp4` | re-rendered 2026-11-01 ~12:12 UTC on the Spark CPU (commit f7031ad), 75.1 s, 1920x1080, md5 3ac1cbad…: same fixes as the 9:16 plus text 40 px clear of the caption band, Map registered with its rings/chips, 1.15x zoom on p02/p03/p06/p08, YOU · 1.75 M chip in p09, longer one-line caption pages. The 11:45 cut is `-prev.mp4`. |
| `thumbs/` | 3 thumbnails x 2 ratios: `explainer-orca_explainer-scale_*` (0 HUMAN KILLS), `explainer-orca_explainer-eye_*` (IT CHOSE NOT TO), `explainer-orca-b_explainer-scale_*` (WHY NOT YOU?) |
| `titles.md` | 5 titles mapped to reference patterns; pick #2 for Shorts/TikTok, #1 for 16:9 |
| `description.md` | Shorts + 16:9 copy, chapters re-timed to the 75.1 s cut, fact re-check list, disclosure steps |
| `references.md` | VtrcKTkhDHU (318.8x), fGcgWaswMns (14.65x), jw6bS-WL4F4 (1.43x) + beat alignment |

---

## 2. horror-pinned-rules (P-horror): PASS (closeout round 1)

**Final MP4 (closeout):** `/Users/patrickliu/Documents/faceless-studio/out/pilots/horror-pinned-rules/horror-pinned-rules_9x16.mp4`
(65.216 s, 1080x1920, md5 14376d5d76a453b9fcbf22c542915e87, fix round 3, commits 9d44c51 + 44d8661), PASS in closeout round 1.
Before the closeout (the rest of this paragraph): round 3 reviewed the 65.2 s cut from commit 2be1192 (md5 ca79bba8…); the
folder then held md5 cbe798ad… (now `horror-pinned-rules_9x16-prev.mp4`), the later re-render from commit 6d050b5 (11:03 UTC), which only changed caption colour (red on emphasis words
only) and re-timed the storyboard to the shipped mix by ~20 ms. It was not re-reviewed; a 4-frame check at 0 / 8.5 / 61.5 /
65.1 s shows the same picture as round 3, with "ONLY ONE" still on the grin and the end card still faded.
The render itself was done by the parallel agent a0dbf06d2d06b5c22 (audio mix, kit, final render) on the Spark CPU.
A 65.75 s `-prev.mp4` (believed to be the round 2 cut) was copied back from `~/studio/archive/horror-pinned-rules-retired/` at
the time; it has since been replaced in the folder by the cbe798ad… file. The 88.3 s S1 cut reviewed in round 1 is retired (archived on the Spark).

| Round | MP4 reviewed | Visual parity | Viewer / retention | Round result |
|---|---|---|---|---|
| 1 | 88.3 s S1 cut (`~/studio/app/studio/out/S1/horror-pinned-rules.mp4`, retired) | 3/10 FAIL | 48 FAIL | FAIL |
| 2 | 64.94 s fix-1 cut | 6/10 FAIL | 74 PASS | FAIL |
| 3 | 65.216 s fix-2 cut, commit 2be1192 | 72/100 FAIL | 82 PASS | **FAIL** |

The workflow's MP4 field for round 1 held a placeholder ("Waiting for monitor events.") and round 3's held the fixer's
report text; both reviewers resolved the real file themselves as described above.

### Round 1 (3/10 / 48): FAIL

![horror-pinned-rules round 1, side-by-side sheet (visual and viewer sheets are identical)](../qa/horror-pinned-rules_r1_visual.jpg)

<details><summary>Visual parity, 3/10, FAIL</summary>

Reviewed the 88.3 s render finished 09:48 UTC (pulled at the time to `out/pilots/horror-pinned-rules/horror-pinned-rules.mp4`, since retired).

Works: clean, readable phone-chat UI (bubble text larger than the refs, red alert bubbles read well); the peephole fisheye
ending, knock-shake and glitch beats are good ideas; the protagonist art is comparable to the stick-figure ref (7659677578365537569).

Fails: (1) frame 0 is fully black, and the 0.5 s hook frame is an empty dark chat; (2) one shot for 34 s: the same HandPhone over
blurred bedroom from 0 to 34 s and in 9 of 14 scenes, while the refs alternate phone insert, reaction, set and prop insert every
few seconds; (3) far too dark: mean luma 24-38 vs the refs' 50-150 (median ~90); (4) Nora is a small head cut off in the corner
under an empty door (p09/p10); (5) the camera push-in moves the phone into the caption (p04, p07); (6) "ONLY ONE" covers the
neighbour's eyes and mouth at the payoff; (7) the peephole face reads neutral and friendly; (8) crude sausage-finger hand;
(9) no establishing shot, two-shot or prop insert. Full-bleed 9:16 with bold 3-word chunks is an acceptable house style only if subjects fill the frame.
</details>

<details><summary>Viewer / retention, 48, FAIL</summary>

88.34 s, 30 fps; frames, ebur128, silencedetect and scene detection on the Spark CPU (nice, 2 threads).

Passes: spoken hook "Rule four said..." runs 0.53-3.6 s with a knock at 1.95 s; captions within ±66 ms of 15 voice onsets;
-14.0 LUFS, TP -1.5 dBTP, LRA 3.5, music 6.5 dB ducked under the voice; 3 references with a beat table, originality PASS;
the scariest image (peephole, 68 s, 77%) and twist ("only one", 84 s, 95%) sit where the PLAYBOOK wants them.

Fails: black cover frame (0.2 s fade-in) and an empty phone to 0.57 s; one composition for 34 s with the top ~60% empty, a
new bubble only every 3-7 s and the thumb covering the newest bubble; the trusted source is contradicted at 27-31 s (35%)
instead of by 11 s; 163 wpm against 230-270, with 13 paragraph gaps of ~1.3 s (~17 s of low-energy air); static stretches
over 3 s (6-12, 61-68, 73-80, 84.4-88.3 s); no Part 2 card or bookend; Nora on screen only ~16 s and no two-shot.
Most viewers would leave in the 10-30 s phone stretch.
</details>

### Round 2 (6/10 / 74): FAIL

![horror-pinned-rules round 2, side-by-side sheet (visual and viewer sheets are identical)](../qa/horror-pinned-rules_r2_visual.jpg)

<details><summary>Visual parity, 6/10, FAIL</summary>

Clearly better than round 1: clean flat art with thick outlines, desaturated blue-grey night with one red accent, readable chat
(40-55 px bubbles). The door silhouette (~28 s) and peephole grin (~62 s) hold up next to the refs; RULE 6: typing + PART 2
works as a cliffhanger.

Still amateur: (1) every 2-3 word caption page wraps into a stacked 2-line pill (a `captions.tsx` layout bug), and captions at
y≈0.16 sit on top of white chat bubbles in ~8 of 33 samples, as mute-illegible fragments ("on and break", "There was only",
"C checked."); the refs use one clean 6-9 word line in a dark band. (2) The phone dominates: chat fills the frame in ~55% of
samples (cap 45%), punch-ins crop bubbles at the edges, and the cover is a text-only chat close-up under a translucent neon
banner, while all three refs open on a threat figure. Smaller: grey bone-like hand; four near-identical medium shots 40-48 s;
stray "ONLY ONE" on the peephole. Side note: voice 65.754 s vs video 64.95 s (last word ends 62.15 s, probably harmless).
</details>

<details><summary>Viewer / retention, 74, PASS</summary>

64.94 s. Hook lands by 1-3 s (red RULE 4 bubble at frame 0, line spoken by 3.3 s, knock + shake on "knocks" at 1.76 s);
longest hold 0-3.3 s (with a zoom), others ≤2.2 s (123 cuts/punches); a new jolt at least every ~6 s; turn at ~50% (grey dot
32.5 s); ending per PLAYBOOK §4C type 2 (RULE 6 from a new authority + PART 2, bookends the phone shot, no CTA). Captions
offset a constant ~+0.06 s. -14.0 LUFS, TP -1.5 dBTP, LRA 2.2, ~4.8 dB ducking. 3 references + beat table, originality PASS.

Holding it back: caption pills over chat text in ~8 places; the "terrified" face reads as a laughing grin at 4 beats; authority
contradicted at 12.4 s on screen / 14.8 s in speech (targets ≤11-12 s); 31 words in the first 10 s (median 43.5), ~193 wpm vs
230-270; 3-word caption fragments that split names and the payoff line; no physical threat on the cover; phone ~53% of screen
time (guidance 10-45%); the scariest image held only ~1.9 s.
</details>

### Round 3 (72 / 82): FAIL (visual parity)

![horror-pinned-rules round 3, visual parity sheet](../qa/horror-pinned-rules_r3_visual.jpg)
![horror-pinned-rules round 3, viewer sheet](../qa/horror-pinned-rules_r3_viewer.jpg)

Fix round 2 (what went in): one-line captions that shrink type to ≤76% instead of wrapping, per-scene caption height
(`captionY` / `captionYAt`), page breaks never before a unit letter or number or after "only" (commit 3dda10c); frame 0 =
silhouette at the door with RULE 4 on an opaque plate; chat punch-ins at zoom 1.22 with the whole bubble in frame and the
caption dropped to y≈0.75; reaction cuts, the Ben-at-5A hallway plant, the light-switch insert, the ECU / door / terrified
sequence; grin held longer, 0.2 s glitch (builder, b5c44fb); new terrified mouth, skin-tone rounded hand, opaque neon plate
(kit); tightened script, voice from 0.1 s, louder dread bed, contradiction at ~10-11 s (audio). The fixer flagged two leftovers
in the other agent's lane: the "inside. Dev in Six-C checked." page at ~9.5 s and "ONLY ONE" on the grin.

<details><summary>Visual parity, 72/100, FAIL</summary>

65.216 s, md5 ca79bba8, commit 2be1192; scrubbed every 2 s plus every 0.5 s over 35-64 s.

At parity: frame 0 is a real cover (silhouette under an opaque red RULE 4 plate, no black frame); desaturated blue-grey with
red as the only danger accent; flat outlined cast with expression swaps, cleaner than the mraevq/udhwkz panels; "Hartwell
Property Group. DISSOLVED." on screen at 10 s; ~50 px chat in punch-ins, high-contrast dark theme, chat ~40% of runtime;
real shot variety (ECU 40.5 s, 5A hallway plant 18 s, peephole 46-59 s, red-lit grin 60.5 s); one-line captions ~3% of frame
height on a dark pill in the top band, like the refs.

Why it still fails:
1. "ONLY ONE" is still burned onto the grin's chin from 60.5 to 63.5 s, though the reviewer asked to drop it.
2. The caption page "inside. Dev in Six-C checked." runs across a sentence and scene break at 8-9.5 s (core paginate bug).
3. About a dozen pages end on a dangling function word ("Rule four said if", "Rule five: Management will", "So who'd been answering our", "Management may", "hallway light and sat", "We just need to come", "A calm voice said", "I looked through", "His little green").
4. Every chat punch-in (6, 8, 10, 28, 32, 52-56 s) slices a half-visible text row across the top edge; it reads as a cropping error.
5. The light-switch insert (35-37 s) is three flat rects on a grey wall, no hand, no light change: a placeholder.
6. The last frame (65.1 s) is the RULE 6 / PART 2 card faded to ~40%: an outro fade, not a hard cliffhanger cut.

Smaller: the thumb overlaps the low-band caption (6, 10, 28 s); caption + RULE 4 plate stack two text blocks in the top 25% at
0.5 s; 41.4-44.3 s is a static door with no caption or visible knock shake; the same couch medium shot repeats 5 times (4, 12,
14, 16, 34 s); no two-shot. All six main fixes are targeted edits; only the switch insert needs new kit art.
</details>

<details><summary>Viewer / retention, 82, PASS</summary>

65.216 s, md5 ca79bba8. Sheet built on the Mac with `side_by_side.sh <mp4> horror --storyboard ...`; all other ffmpeg niced on
the Spark CPU. Heads-up: the Spark copy at `~/studio/app/studio/out/pilots/horror-pinned-rules/horror-pinned-rules_9x16.mp4`
is an older 64.94 s file.

Hook passes: frame 0 cover (silhouette + "RULE 4: DON'T ANSWER THE DOOR"), no fade; voice at 0.10 s, knock at 0.99 s, rule
line spoken by 2.2 s, first cut at 1.83 s; contradiction "Management shut down two years ago" at 9.6-10.8 s (inside 11 s).
Visual change passes: cuts/punches never more than ~2.6 s apart (longest holds 5.6-8.07, 16.3-18.8, 41.43-44.07 s with no
voice or caption, and the end card from 63.2 s). Captions word-synced at 6 spot checks, one line, change every ~1.4-2 s.
Audio: I -14.0 LUFS, LRA 6.0, TP -1.3, no clipping, bed 14 dB under the voice; silence only in the last 0.86 s. Something new
goes wrong about every 5 s; the grin is held ~3.5 s (target 4). ~194 wpm vs 230-270 (not a blocker at 65 s). Ending RULE 6 +
PART 2, no spoken CTA. 3 references (63.1x, 10.8x, 31x) with a beat table; originality PASS. No two-shot; the dark chat theme
differs from the README's light-UI note but was a deliberate call in b5c44fb.

Both flagged leftovers confirmed: the "inside. Dev in Six-C checked." page (7.40-~9.6 s) comes from the core caption code
(`studio/src/core/captions.tsx:104`, 3dda10c), not the other agent's builder; "ONLY ONE" (≈60-63 s) comes from
`pipeline/episodes/horror_eps.py:525-526` (b5c44fb).
</details>

### What still falls short of the references (horror)

- **"ONLY ONE" burned onto the grin (≈60-63.5 s)**: still present in the current file (checked at 61.5 s). Remove the RedText at `pipeline/episodes/horror_eps.py:525-526`; the refs never put text over the scare face.
- **Caption pagination**: a page that runs across a sentence and scene break ("inside. Dev in Six-C checked.", `captions.tsx:104`) and ~12 pages that end on a dangling function word. The refs show whole one-line subtitles.
- **Punch-in cropping**: every chat punch-in slices a half row of text at the top edge.
- **Placeholder light-switch insert (35-37 s)** with no hand or light change; a static, captionless door at 41.4-44.3 s; the same couch medium shot five times; no two-shot.
- **Ending**: the RULE 6 / PART 2 card fades to ~40% (still the case at 65.1 s in the current file); the refs hard-cut on the cliffhanger.
- **Pace**: ~194 wpm against the PLAYBOOK's 230-270 for narrated stories.
- **Review gap**: the current file (6d050b5 re-render) was not re-reviewed; only the caption colour changed.

Status before the closeout: the viewer reviewer would let it run (82, PASS), but visual parity failed three times, so it was
not cleared to post until fixes 1-6 of round 3 landed and another round passed. **Update (closeout):** all six fixes landed in
9d44c51 / 44d8661 and closeout round 1 passed (80 / 84 on md5 14376d5d…); it is cleared to post.

### Package (`out/pilots/horror-pinned-rules/`)

| File | Status |
|---|---|
| `horror-pinned-rules_9x16.mp4` | **final**, 65.216 s, 1080x1920, md5 14376d5d76a453b9fcbf22c542915e87 (fix round 3, 9d44c51, rendered 11:54 UTC on the Spark CPU), PASS in closeout round 1. `-prev.mp4` (md5 cbe798ad…) is the 6d050b5 re-render of the round 3 cut. Horror is 9:16 only. |
| `thumbs/` | 3 thumbnails x 2 ratios: `_horror-chat_*` (RULE 4: DON'T ANSWER THE DOOR), `_horror-door_*` (THREE KNOCKS), `_horror-hallway_*` (WHO PINNED THIS?); spare `horror-pinned-rules-door_horror-door_*` (WHO WROTE RULE 4?) |
| `titles.md` | 5 titles; pick #2 for TikTok/Shorts, #1 as the YouTube series title. Thumbnail pairings corrected to the rendered thumbnail text. |
| `description.md` | TikTok/Shorts copy, fiction + synthetic-voice line, R5 disclosure block merged at closeout (official sources) |
| `references.md` | 7702661541224566049 (63.13x), 7659677578365537569 (10.79x), cVUJmsVkUW4 (30.95x) + beat alignment |

---

## 3. explainer-blue-whale (pilot 3): 9:16 PASS (closeout regression, md5 c1c5647a…), 16:9 FAIL

**Round 3 cut:** 70.08 s, 1080x1920, md5 d859720c…, now `explainer-blue-whale_9x16-prev2.mp4`. The cleared 9:16 at closeout is
`explainer-blue-whale_9x16-prev.mp4` (md5 c1c5647a…, regression 77 PASS); the current `explainer-blue-whale_9x16.mp4` (md5
491cdd4c…) is the unreviewed fix-pass-2 cut. The 72.9 s round 2 cut is no longer in the folder.

| Round | MP4 reviewed | Visual parity | Viewer / retention | Round result |
|---|---|---|---|---|
| 1 | 86.6 s cut | 58/100 FAIL | 58 FAIL | FAIL |
| 2 | 72.9 s cut (now `-prev`) | 74/100 FAIL | 68 FAIL | FAIL |
| 3 | 70.08 s cut (final) | 80/100 PASS | 7/10 PASS | **PASS** |

### Round 1 (58 / 58): FAIL

![explainer-blue-whale round 1, side-by-side sheet (visual and viewer sheets are identical)](../qa/explainer-blue-whale_r1_visual.jpg)

<details><summary>Visual parity, 58/100, FAIL</summary>

Good parts close to fGcgWaswMns: ocean gradient on spec (#28697c → #06202c, god rays, particles), clean flat whale and diver,
captions inside the safe area (y 0.72, size 84), hook and ending share the whale + YOU shot, strong thumbnails.

Amateur in a feed: (1) red everywhere: karaoke red on function words (AND, THAT'S, JUST, MUCH), red stats, an emoji heart, red X,
red sub-headlines; (2) caption pages end mid-phrase ("THAT'S TWO AND", "MUCH AS AN", "PARKED NOSE TO"); (3) clip-art beats: an
emoji heart with no golf cart (p04), an elephant floating with no tongue (p03), a white stick figure next to a beach ball with no
throat (p08); (4) poor use of 9:16: the whale a ~5%-tall sliver in p01/p02/p05/p06, bottom 30-40% empty, a featureless band
in p09; (5) low motion: no camera move in p03/p05/p06/p08, holds over 4 s (30.7-35.2, 41.2-45.4, 50.0-54.1, 78.4-82.6 s),
cuts every 5-10 s vs ~1.5 s on the 9:16 ref; (6) frame 0 has no text or YOU, and the last frame fades to black; (7) tags too
small for a phone (32-38 px), headers echo the caption. Sheet rows: thumbnail/cover fail; hook weak; anatomy and title card fail
(elephant, no tongue); stat and hero borderline; options and stock_proof fail; ending passes on content but ends black.
</details>

<details><summary>Viewer / retention, 58, FAIL</summary>

86.6 s, 47 frames. Style matches fGcgWaswMns; frame 0 not black; captions word-synced at 6 points; 2-4 word cards at y≈1280;
-14.1 LUFS, TP -1.1; originality PASS with 3 references.

Fails: a 19-word hook with the paradox at 5.8 s (target ≤12 words in ~3 s); ~157 wpm at TTS speed 0.96 with ~1 s dead pauses;
holds over 4 s (heart 31-37 s with no golf cart, throat gauge 66.5-70.5, bookend 78.4-82.5, weight 21-24.6); only 0.3 s
fades, no hard cuts; turnstile at 63% (target 45-55%); the throat scene swaps the diver for a stick figure and the red X sits on
the beach ball; a spoken comment CTA and a 0.5 s fade-out that breaks the loop; red on every caption; music inaudible
(-45.6 dBFS under the voice).
</details>

### Round 2 (74 / 68): FAIL

![explainer-blue-whale round 2, visual parity sheet](../qa/explainer-blue-whale_r2_visual.jpg)
![explainer-blue-whale round 2, viewer sheet](../qa/explainer-blue-whale_r2_viewer.jpg)

<details><summary>Visual parity, 74/100, FAIL</summary>

72.9 s. Matches the Depth Theory style: flat whale, navy-to-teal with god rays, red on threat words, drawn animated numbers
(≈190 t balance, 188 dB vs a jet, 40,000,000 krill counter, 2 BPM ECG); frame 0 not black with YOU in the mouth; last frame =
frame 0; punch-ins every ~1.5-2.5 s; captions at y≈1382.

Fails: (1) caption paging: 86 cards in 73 s (~0.85 s each), many orphan words or split numbers ("CART.", "close to two | hundred
tonnes", "as a beach | ball."); the 6mRR ref always shows phrase-complete cards; (2) under-filled or broken compositions:
near-black frame with a tiny heart (25-28 s), a flat black whale slab (42-44 s), the throat close-up with a slate band, diver
off-frame and the ball above the ring (51-57 s), a whale sliver (58-60 s), a thin vertical whale alone (4-7 s); (3) a weak cover:
78 px "FITS IN ITS MOUTH", no red word, restates the title; (4) the chosen thumbnail "YOU FIT INSIDE" repeats the title (ROOM
TO SPARE is the strongest). Minor: the 30 M chip over the ruler's own "30"; caption on the ruler's 0 tick; an all-red header.
</details>

<details><summary>Viewer / retention, 68, FAIL</summary>

72.9 s. Passes: word sync (28 onsets within ±0.17 s), mix (-14.0 LUFS, TP -1.1, music ~13 LU under the voice), loop ending
with no CTA, 3 references + originality PASS, frame 0 cover, no 3 s window without a visual change (hard cuts at 4.6 ... 66.6 s).

Fails: dead air (first word at 0.575 s, ten 0.6-0.74 s paragraph gaps ≈4.5 s; paradox lands at 4.13 s vs ≤3 s); a "tongue /
heart / call" fact list with zero "you" from 4.8 to 41 s (4.2 you/min vs 12-20), the likely swipe zone; turnstile at 56%, peak
at 79%, a redundant second re-hook, stinger ending on "there"; weak frames (half-drawn ECG and tiny heart at 26 s; krill with
no whale at 34.8-36.5 s; throat set not full-bleed with seams at 51-57 s; diver alone at 57.3-59.3 s; a fish-like vertical tail
at ~65.5 s); split number/compound pages ("CLOSE TO TWO | HUNDRED TONNES", "AS A BEACH | BALL.").
</details>

### Round 3 (80 / 7 of 10): PASS

![explainer-blue-whale round 3, side-by-side sheet (visual and viewer sheets are identical)](../qa/explainer-blue-whale_r3_visual.jpg)

<details><summary>Visual parity, 80/100, PASS</summary>

At least as good as the Depth Theory target (fGcgWaswMns) and a better use of 9:16 than either 16:9 ref. Frame 0 is a cover
(heavy-caps headline with red EAT, red arrow, open-mouthed whale, tiny YOU inside), repeated exactly at 69.3 s. Navy-to-teal
with god rays, never black; red only on the threat word, arrow and stat underlines. Every number drawn next to a familiar
object (buses on a ruler, balance with a sauropod and an elephant, heart vs golf cart, ECG, jet, krill counter, throat vs beach
ball). 84 px heavy white captions at y≈0.72, 2-4 words. Something new every 1-3 s, no hold over 4 s; full-bleed changes keep
the energy up. Strong thumbnails.

Still unpolished: (1) text blocks collide in the lower-middle band (tags/stats at y 60-64% sit on the y 72% caption; the 12 s
headline runs into the bus); (2) two tails on screen in p09 at 63 s; (3) the p03 "forty of you" crowd and the p01 diver are too
small to read on a phone; (4) in p04 the heart and golf cart are pushed to the edges and the diver/YOU overlap the cart.
None would look amateur in a feed; 1-3 are cheap scene-builder edits.
</details>

<details><summary>Viewer / retention, 7/10, PASS</summary>

70.08 s. Hook: frame 0 cover (YOU'RE TOO BIG TO EAT, red EAT, YOU in a gape ~75% of width); narration from 0.10 s; both halves of
the 12-word paradox done by 3.63 s. Picture change every 0.5-2.5 s (quieter but moving 27.4-35.3 s). Captions match speech at
36 sampled times; sentence-gap dips within 0.0-0.2 s of the storyboard except 30.44 s (heartbeat SFX) and 49.08 s (0.28 s
early). I -14.1 LUFS, LRA 1.5, TP -1.1, no clipping, music ~18 dB under the voice. 225 words in 69.7 s = 194 wpm; gaps 0.12-0.19 s.
Stinger ends at 69.39 s, last frame = frame 0, no CTA (PLAYBOOK S7). References jw6bS-WL4F4, JkAcCdqYJN0, fGcgWaswMns with
a beat table; originality PASS. Matches the review-refs README rules.

Defects: (1) both SFX land a sentence late: the heartbeat (30.49 s, 4.39 s) plays over the CALL scene, the whoosh (63.89 s)
over the bookend line; (2) a separate FLUKE svg overlaps the whale's own tail at ~62.5-63.8 s (two tails); (3) in p05 the far YOU
chip and a ~2 px diver are jammed against the 188 dB card; (4) p03 opens on an empty tilted balance for ~0.3 s (19.0 s); (5) some
pages run 5-6 words; (6) script: turnstile at 59% (target 45-55%), only 39% of sentences contain "you" (target ≥60%), and rungs
2-6 are sideways size facts, so 15-40 s is the likeliest swipe zone.
</details>

### What still falls short of the references (blue whale)

- **Mid-video sag (15-40 s)**: length / weight / tongue / heart / call are sideways size facts with little "you" (39% of sentences vs ≥60%); the turnstile sits at 59%.
- **SFX one sentence late**: heartbeat over the call scene (30.5 s), whoosh over the bookend line (63.9 s).
- **Two tails at the climax (≈62.5-63.8 s)**: the separate FLUKE svg overlaps the whale's own tail.
- **Lower-middle text collisions**: tags/stats at y 60-64% on the y 72% caption; the 12 s headline into the bus; the p05 YOU chip and ~2 px diver jammed on the 188 dB card.
- **Too small for a phone**: the "forty of you" crowd (p03) and the p01 diver; the heart and golf cart pushed to the frame edges (p04); an empty tilted balance for 0.3 s at 19.0 s.
- **Caption pages of 5-6 words** in places, against the refs' 2-4.
- **16:9 cut** (6-frame check): at ~8 s the "30 M" chip runs into the "HOW BIG IS IT?" header and the vertical ruler leaves both sides of the 16:9 frame empty; the two-tails defect is visible at 63 s too. It was re-rendered today from the current kit code; the 9:16 was rendered at ~10:49 UTC, before the caption-pager commit 1360749, so 16:9 caption pages can differ slightly from the 9:16.

### Package (`out/pilots/explainer-blue-whale/`)

| File | Status |
|---|---|
| `explainer-blue-whale_9x16.mp4` | re-rendered 2026-11-01 ~12:15 UTC on the Spark CPU (commit f7031ad), 70.08 s, 1080x1920, md5 491cdd4c…: 2nd fix pass (NO WAY DOWN 2 s header, crowd at y 30-46 %, 188 dB card leaves before the far YOU, fluke sweeps mid-frame 62.5-63.9 s with the body fading over 0.6 s, YOU chip clear of the header chip, caption joins). The 11:45 cut is `-prev.mp4`, the round 3 PASS cut `-prev2.mp4`. |
| `explainer-blue-whale_16x9.mp4` | re-rendered 2026-11-01 ~12:14 UTC on the Spark CPU (commit f7031ad), 70.08 s, 1920x1080, md5 08093d1a…: full-bleed throat set (49-54.5 s, no portrait panel), landscape-native p01/p02/p04 (ruler; head close-up + frame-wide balance; heart and golf cart side by side, full-bleed deep set), crowd in frame at 22-23.5 s, text 40 px clear of the caption band, TOP_SAFE 5 %, 16:9-only caption joins. The 11:45 cut is `-prev.mp4`. |
| `thumbs/` | 3 thumbnails x 2 ratios: `explainer-blue-whale_explainer-eye_*` (ROOM TO SPARE, primary), `explainer-blue-whale-b_explainer-eye_*` (IT CAN'T SWALLOW YOU), `explainer-blue-whale_explainer-scale_*` (TOO BIG TO EAT) |
| `titles.md` | 7 titles mapped to reference patterns; pick #1 for Shorts/TikTok, #2 for 16:9 |
| `description.md` | Shorts + 16:9 copy, chapters re-timed to the 70.1 s cut, sources, pinned-comment CTA, disclosure steps |
| `references.md` | jw6bS-WL4F4 (1.43x), JkAcCdqYJN0 (15.82x), fGcgWaswMns (14.65x) + beat alignment |

---

## Closeout (11:35-13:40 UTC)

Written ~12:20 UTC. Each review below names the md5 of the exact file the reviewer opened. All renders, scrubs, ebur128 and
scene detection ran niced on the Spark CPU (no GPU). Sheets were built with `scripts/side_by_side.sh` before commit edd3007, so
`_9x16` / `_16x9` file names did not resolve a storyboard (rows filled by relative position) and 16:9 frames sat in 9:16 cells;
every reviewer made up for it with full-resolution scrubs.

### Horror (horror-pinned-rules): PASS in closeout round 1

**Fixer output (fix round 3, the input to closeout round 1):**
`out/pilots/horror-pinned-rules/horror-pinned-rules_9x16.mp4`, md5 `14376d5d76a453b9fcbf22c542915e87`, 65.216 s, 1080x1920,
30 fps, rendered 11:54 UTC from commit 9d44c51 (storyboard + `pipeline/episodes/horror_eps.py`) on top of kit commit 44d8661
(`studio/src/kits/horror/`: LightSwitch insert with a hand, a flick and the light dying; TopFade for chat punch-ins; chat list
fades under the header). The Spark copy has the same md5. What went in: no text on the grin; a hard cut to the RULE 6 / PART 2
card; a real switch insert; punch-ins under a top fade with the caption in the top band (thumb clear); a low caption under the
cover plate; KNOCK beats and camera jolts at 41-44 s; varied reaction framings; a hallway two-shot; phrase-complete caption
paging (glue).

| Closeout round | MP4 reviewed (md5) | Visual parity | Viewer / retention | Round result |
|---|---|---|---|---|
| c1 | `14376d5d76a453b9fcbf22c542915e87` (both reviewers) | 80/100 PASS | 84/100 PASS | **PASS** |

![horror-pinned-rules closeout round 1, side-by-side sheet (visual and viewer sheets are identical)](../qa/horror-pinned-rules_c1_visual.jpg)

<details><summary>Visual parity, 80/100, PASS (md5 14376d5d…)</summary>

Scrubbed every 2 s over 0-65.1 s, every 0.5 s over 36-65 s, every 0.25 s over 2.25-4.5 s and 40.5-42.75 s; no files edited.
The sheet's two_shot row grabbed the empty door at 43.2 s (relative position); the real hallway two-shot is at 18 s.

All six round-3 failures are fixed: (1) no text on the grin (60.5-63 s is a clean red-lit grin, "person out there." sits above
the head); (2) "Dev in Six-C checked." is its own page at 9 s; (3) caption pages are mostly whole phrases ("Rule five:", "ask to
come inside.", "A calm voice said my name.", "It's Management.", "There was only one" / "person out there."), cleaner than the
refs' own mid-sentence subtitles; (4) chat punch-ins sit under a top fade with the caption in the top band, thumb clear;
(5) the light-switch insert at 36 s has a hand and a flick, and the light dies; (6) hard cut at 63.5 s to the RULE 6 / PART 2
card at full brightness through 65.1 s, no fade. Also new: KNOCK beats and camera jolts at 41-44.5 s, varied reaction framings
(against the door, ECU, terrified medium) and a Ben (5A) + Nora hallway two-shot at 18 s.

Against the refs: the cover (silhouette, white dot eyes, opaque red RULE 4 plate) is as strong as the mraevq axe and udhwkz
grin covers; desaturated blue-grey with red as the only danger accent, at parity; flat outlined art with expression swaps,
cleaner but simpler (no texture or dread shading); ~50 px dark-theme chat bubbles, chat in ~41% of 2 s samples (guidance
10-45%); one-line captions on a dark pill, ~3% of frame height, changing every 1-2 s; the climax cuts or punches at least every
~1.5 s, the longest hold is the intended captionless grin at 61-63 s.

Below 85 because: a one-row top slice and the caption on the "Dev (6C)" label at the 2.75 s punch-in; "KNOCK" flashed across
the ECU's forehead at 41.25-41.75 s; captions over still-readable ghosted rows (3.0, 6.0, 55.5 s); a crude grey mitten hand on
the switch; the couch medium is still the default reaction (0.5-4, 12, 14, 16, 34 s); a few split phrases ("Management shut" /
"down", "I'm standing right" / "behind them.", "So who'd been answering").
</details>

<details><summary>Viewer / retention, 84/100, PASS (md5 14376d5d…)</summary>

Also read 1 fps contact sheets of the whole cut and a 20-frame spot-check sheet; no files edited.

- **Hook:** frame 0 is the silhouette at the door under the opaque "RULE 4: DON'T ANSWER THE DOOR" plate with the caption "Rule
  four said if someone"; voice at 0.10 s, knock at 0.99 s, rule spoken by 2.2 s, first cut at 1.83 s; no black frame, no fade-in.
- **Visual change:** the longest gaps between detected changes are ~2.6 s (5.43-8.07 chat scroll with caption changes,
  16.3-18.8 two-shot, 41.43-44.07 door with KNOCK flash and jolt, 63.17-65.2 end card); nothing past ~2.65 s.
- **Captions:** six page onsets (Dev 8.215, Ben 16.322, Someone's 22.93, Rule 31.093, Right 38.685, There 59.361) flip within
  ~0.1 s; every page is one line on a dark pill in the top band; the old merged page is gone and no text sits on the grin.
- **Audio:** -14.0 LUFS, LRA 6.0 LU, TP -1.3 dBTP, no clipping; silence below -40 dB only in the last 0.76 s; bed 14 dB under
  the voice, ducking ~7.9 dB.
- **Story beats:** contradiction "Management shut down two years ago" at 9.6-10.8 s; 5A two-shot ~16 s, Ben's knocks 23 s, green
  dot to grey 28 s, glitch and rule-5 edit 29-34 s (midpoint ~48%), switch insert 35-37 s, knocks at my door 40.5 s (62%),
  peephole voice 45 s, "standing right behind them" 54 s, "only one" reveal 59.4 s, red grin 60-63.2 s.
- **Ending:** hard cut to RULE 6 "Management is typing..." + PART 2, full brightness to the last frame (64.0, 64.6, 65.15 s), no
  spoken CTA, loops to the RULE 4 cover (PLAYBOOK §4C types 1 and 2).
- **References / originality:** 3 references (63.13x, 10.79x, 30.95x) with a beat table; `scripts/originality_check.py` PASS.

Below ~90 because: caption pages still split clauses (`maxChars` 20), including the payoff line; ~194 wpm (196 words / ~60.6 s)
against 230-270, ~33 words in the first 10 s against a median of 43, contradiction at 9.6 s where top outliers land it by 5-7 s;
55.5-57.7 s is a 2.2 s stretch with no voice and no caption on a static chat right before the payoff; the grin is held ~3.2 s
with glitch jitter (PLAYBOOK: hold still ~4 s); faded chat rows show behind the top-band caption at ~4 s and 26-27 s.
A viewer would likely watch to the end: high jolt rate, a new threat about every 5 s, a clean PART 2 cliffhanger.
</details>

**Final verdict: PASS** (80 / 84, both on md5 `14376d5d76a453b9fcbf22c542915e87`). Cleared to post; the 11:27 horror lock is
lifted. The R5 disclosure block (`research/R5/horror-pinned-rules-DISCLOSURE.md`) is merged into
`out/pilots/horror-pinned-rules/description.md`. Non-blocking polish for Part 2 / the kit (horror paths, now unlocked): the 2.75 s
punch-in top slice, KNOCK over the ECU face, ghosted rows behind captions, the mitten hand, the couch-medium default, split
clauses, pace (~194 wpm, contradiction by ~6 s), the 55.5-57.7 s dead stretch and a still ~4 s grin hold.

### Explainers: 16:9 fixes, 16:9 review, 9:16 regression checks

**16:9 fix pass 1 (commits 200bc5e code + storyboards, d1c72da QA rows):** `pipeline/episodes/reformat.py` (top-edge clamp for
every episode + per-scene landscape hook) and `pipeline/episodes/explainer_eps.py` (blue-whale 16:9 p01, p09 whale fade);
storyboards `episodes/explainer-orca/storyboard_16x9.json`, `episodes/explainer-blue-whale/storyboard.json` and
`storyboard_16x9.json` rebuilt. Rendered on the Spark CPU (nice -n 10, concurrency 4, render lock) in a separate tree
`~/studio/ex16` built from 200bc5e with the committed `studio/src/core/Episode.tsx` and `captions.tsx` (the shared tree had another
agent's uncommitted pager edits; those are not in these MP4s). No horror paths touched.

| Output | md5 | Length / size | Replaced | Fix |
|---|---|---|---|---|
| `explainer-orca_16x9.mp4` | `355d0d72cdebf46ec19837e359f08d52` | 75.115 s, 1920x1080 | `ebd0a409…` (11:31 cut) | 0 HUMAN KILLS header fully inside the frame on frame 0 and the last frame. Cause: the reformat placed screen-fixed text too high (not the push-in). 9:16 unchanged. |
| `explainer-blue-whale_16x9.mp4` | `6847ebcab12637f867c5c078ab24eff0` | 70.08 s, 1920x1080 | `da6d25f4…` | p01 landscape-native: whale along a horizontal 0-30 m ruler, 2.5 buses nose to tail, YOU and YOU ≈ 1/16 at the 0 end, 30 M chip at the ruler end; two tails fixed; cover headline and DEEP DIVE tag off the top edge. |
| `explainer-blue-whale_9x16.mp4` | `c1c5647ab05231848d86df6ce30f6cab` | 70.08 s, 1080x1920 | `d859720c…` (round 3 PASS) | Two tails also fixed in the 9:16 (whale body fades into the water before the tail close-up enters at ~62.5 s). Captions from the committed pager 1360749, so a few pages differ from round 3. |

Fixer's open items (not changed): 9:16 blue whale ~8 s 30 M chip beside the HOW BIG IS IT? header and the tail crossing the
caption for ~0.2 s at 62.6 s; orca 16:9 cover, dorsal fin tip touching IN THE WILD.

| Review | MP4 reviewed (md5) | Score | Result |
|---|---|---|---|
| orca 16:9 visual | `355d0d72cdebf46ec19837e359f08d52` | 68/100 | **FAIL** |
| blue whale 16:9 visual | `6847ebcab12637f867c5c078ab24eff0` | 66/100 | **FAIL** |
| blue whale 9:16 regression | `c1c5647ab05231848d86df6ce30f6cab` | 77/100 | **PASS** |
| orca 9:16 regression | `55793987a7dbd227e216683c22d5e0af` (byte-identical to the round 2 cut, 10b036c) | 72/100 | **FAIL** |

All four reviewed cuts predate the caption-pager commit 7b7e0eb (11:46 UTC), so they still carry the older page breaks.

![explainer-orca 16:9 visual review sheet](../qa/explainer-orca_16x9_visual.jpg)

<details><summary>explainer-orca 16:9, 68/100, FAIL (md5 355d0d72…)</summary>

Sheet built with `--storyboard episodes/explainer-orca/storyboard_16x9.json`; also a 2 s scrub of the whole cut, 0.5 s scrubs of
45.5-75 s (p08-p13) and 22-27.5 s, and full-resolution frames.

Holds up against fGcgWaswMns: same flat-vector navy-to-teal ocean with god rays and clean orca / great white / blue whale /
sailboat art; red only on 0, LIVER, BIGGEST, RAMMING, SUNK, MENU and header underlines; strong cover (0 HUMAN KILLS, red 0 and
underline, now fully in frame; orca ~54% of the width; diver with YOU), repeated at 75.0 s so the loop closes; something new every
0.5-2 s, a whip at 61.5 s, the sailboat tipping at 70.5-71 s, the ~7 counter; longest still ~1.5 s (empty map 63-64.5 s);
~54 px heavy white caps in a bottom band near 85% height, title-safe.

Amateur next to the refs: three round-2 defects remain (no seal in p04; invisible dark orca silhouettes, so 36.5-38 s and 46-49 s
are a tiny diver on a dark screen; label/card collisions); new: garbled double-text crossfades at 57.0 and 59.0 s, many pages
ending mid-clause ("SO WHY HAS SOMETHING", "YOU'RE ABOUT THE SIZE", "AND YOU'D NEVER MEET", "IT HITS FIFTY-SIX", "THE BEST
ANSWER"), and poor use of 16:9 (`reformat.py` maps the whole 9:16 picture into the centre column, outer thirds empty water).

Blocking: "HAVE SUNK." caption inside the "~7 BOATS SUNK SINCE 2020" card at 69-71 s (text on text); "WASHES THE SEAL" with no seal drawn.
</details>

![explainer-blue-whale 16:9 visual review sheet](../qa/explainer-blue-whale_16x9_visual.jpg)

<details><summary>explainer-blue-whale 16:9, 66/100, FAIL (md5 6847ebca…)</summary>

File mtime 11:44:45 UTC, rendered from 200bc5e; sheet md5 0045166c…. Also scrubbed full-width frames every 2 s, every 0.5 s over
44-64 s and 62-70 s, and 15-23 s.

Matches fGcgWaswMns: flat vector art at the same polish; navy-to-teal with god rays, never black; red only on EAT, THROAT, TURN,
the arrow and underlines; heavy caps headers with a red underline; numbers drawn next to familiar objects (2.5 buses on a 0-30 m
ruler, counter to 190 t, elephant on a balance, 188 dB next to a jet, krill counter to 40,000,000); something new every 1-2 s.
The landscape-native ruler in p01 (4-14 s) is the best shot. Frame 0 is a usable cover and the last frame (69.3-70 s) loops.

Row by row: cover borderline (left third empty, ~70 px diver, frame-0 page "YOU'D FIT INSIDE A BLUE" dangles); hook pass (2 s
header CAN'T SWALLOW YOU repeats the caption); p01 pass (strongest); stat_counter 14-19 s borderline (whale ~20% of width, grey
ghost sauropod, BIGGER THAN ANY DINOSAUR tag touches the caption, empty balance ~0.3 s at 18.5-19 s); anatomy 19-30 s fail (the
forty-of-you crowd pushed off the top edge at 22-23 s, ~2.7 TONNES EACH on the caption, heart + golf cart a small cluster with
~55% of the frame empty at 24-27 s, DEEP DIVE a hard-edged portrait column and the 2-BPM box outline through the caption at
28-30 s); call 30-35 s fail (YOU chip half-hidden behind the 188 dB card, DECIBELS line on the caption at 34 s); krill 44-49 s pass
on motion, mostly empty frame.

Blocking: (1) the throat set (49.0-54.5 s) renders as a narrow portrait rectangle ~35-45% of the width with ocean both sides, its
bottom edge visible and the diver's legs hanging outside; cause `_full_frame()` in `reformat.py` resizing the 2376x3072
MOUTH_BG_WIDE svg into 1920x1080 while `studio/src/core/layers.tsx:169` forces `preserveAspectRatio="xMidYMid meet"`;
(2) the two-tails fix overcorrected: the whale fades to a ghost at ~62 s, a lone fluke crosses for <1 s (62.5-63.2 s) and leaves
through the top, and 63.5-64 s is "7 M TAIL" with a tiny YOU in empty water under "WIDE SWEEPS PAST." Also NOT THE MOUTH (55-59 s)
YOU chip covers the diver, WRONG PLACE, WRONG TIME (59.5-62 s) chip over the YOU chip; ending 64-70 s passes (headline tops
~40-45 px from the top, just outside 5% title-safe). Captions are pre-7b7e0eb and full of split pages ("THAT'S TWO AND A HALF |
CITY BUSES", "IT EATS UP TO FORTY MILLION | KRILL A DAY", "AND A TAIL SEVEN METRES | WIDE SWEEPS PAST", …).
</details>

![explainer-blue-whale 9:16 regression sheet](../qa/explainer-blue-whale_regress_visual.jpg)

<details><summary>explainer-blue-whale 9:16 regression, 77/100, PASS (md5 c1c5647a…)</summary>

Scrubbed every 2 s, every 0.5 s over 49-66 s, every 0.2 s over 62.1-62.9 s and 24.3-25.7 s; compared with the round-3 cut
(d859720c) at 10 timestamps. No blocking defect; everything that passed round 3 holds (frame-0 cover YOU'RE TOO BIG TO EAT with
red EAT and arrow, matching last frame at 69.3 s; navy-to-teal never black; red only on threat words; every number next to a
familiar object; the full-bleed throat set 49.5-55 s is the strongest frame; climax changes every 0.5-1 s, no hold over ~2.5 s;
art polish equal to fGcgWaswMns). Regression: the two-tails fix holds (no double tail 62.1-63.5 s), caption pages are the same as
round 3; one new weak spot, a nearly empty frame for ~0.5 s (62.2-62.7 s) under "AND A TAIL SEVEN METRES" before the fluke rises
through the caption band. Below ~85: dangling/split pages from the older pager 1360749 (e.g. "YOU'D FIT INSIDE A BLUE" at
0.5-1.4 s, "IT EATS UP TO FORTY" | "MILLION KRILL A DAY," splitting a glued number); lower-middle text collisions unchanged; golf
cart clipped by the right edge 24.3-25.7 s; the forty-of-you crowd too small for a phone; whale or fluke under the caption at
4 s, 43-44 s and 62.7 s.
</details>

![explainer-orca 9:16 regression sheet](../qa/explainer-orca_regress_visual.jpg)

<details><summary>explainer-orca 9:16 regression, 72/100, FAIL (md5 55793987…)</summary>

Byte-identical to the round 2 cut (commit 10b036c): none of the round-2 defects was fixed in the 9:16 and 7b7e0eb came after it.
Scrubs every 2 s and every 0.5 s over 60-75 s, 34-49 s and 21.5-28 s, plus detail frames (Spark CPU, nice, 2 threads).

Matches the refs: the fGcgWaswMns ocean and art, red as accent only, heavy caps headers with red underline, a strong frame-0
cover (0 HUMAN KILLS, orca ~75% of the width, YOU diver) bookended by the last frame, bold white captions at y ~1230-1480, real
camera energy in the climax (map push, rudder snap with shake, boat listing and sinking).

Falls short: no seal in p04 ("WASHES THE SEAL STRAIGHT OFF" over an empty floe); menace orca invisible at 36-38 s and 46-49 s;
garbled crossfade text at 43.0 s ("2019·WA" / "ADULT BLUE WHALE") and 56.9 s ("WHY NOT YOU?" / "MOTHER + CALF"); collisions (3
SECONDS card on the caption ~16 s, ~7 BOATS SUNK card on the caption 67.5-69.5 s, YOU chip touching "A THOUSAND" 44-45 s,
IBERIAN ORCAS / PORTUGAL chips over rings and icon 64.5-65.5 s); edge crops (4 cars 8-9 s, lower Antarctica orcas 22-23 s, orca
nose off the left edge 66.5-67 s and 70-71 s); dangling pages (IT HITS FIFTY-SIX / IS AS TALL / WHAT CHANCE / THIS FAST / ORCAS
EAT / HAS EVER TAUGHT / AND NO ORCA MOTHER) and an orphan "OF" at 28-29 s; a near-white flash at ~41.5 s; two "you" art styles.
No single blocker, but 72 is under the reviewer's 75 bar. The reviewer notes round 2's 74 was recorded as PASS although it
was also under that bar, so the round-2 PASS for this same file is withdrawn.
</details>

**Explainer fix pass 2 (after the reviews, ~12:10-12:16 UTC, not yet reviewed):** commits 1b92552 (kit: diver-style YOU,
Headline sub colour, Ocean glow), d8ade18 (`reformat.py` + `build.py`: full-frame svgs cover the 16:9 frame, so the throat set /
DEEP DIVE are no longer portrait columns; Map registered with its overlays; text 40 px clear of the caption band; TOP_SAFE 5%;
CAPTION_JOIN tokens), c4ac3ca (orca + blue whale storyboards and `orca_pilot.py` / `explainer_eps.py`: seal visible on the floe,
lit menace silhouettes, sequential header swaps, p12 counter at y 50%, cleaner p11 map, crowd inside the frame, 188 dB card out
before the far YOU, fluke mid-frame with the body fading over 0.6 s), edd3007 (side_by_side resolves `_16x9`/`_9x16` storyboards
and sizes cells to the aspect), 79ebfd2 and f7031ad (blue-whale 16:9 landscape-native p04 and p02), 92094e1 (package rows). These
renders come from f7031ad, after 7b7e0eb, so they use the new pager. They target every blocking defect above, but **no reviewer
has seen them**, so they carry no verdict:

| File now in the folder | md5 | Rendered (UTC) | Review status |
|---|---|---|---|
| `explainer-orca/explainer-orca_9x16.mp4` | `8702a89c1e5e44ca4b4d9bf7ba737d2c` | ~12:11 | not reviewed |
| `explainer-orca/explainer-orca_16x9.mp4` | `3ac1cbad7f12d78c521b05c9f6a0e258` | ~12:12 | not reviewed |
| `explainer-blue-whale/explainer-blue-whale_9x16.mp4` | `491cdd4c60b0ee8ddf7030de8ff2c036` | ~12:15 | not reviewed |
| `explainer-blue-whale/explainer-blue-whale_16x9.mp4` | `08093d1acb11c6b415da5130eb5be240` | ~12:14 | not reviewed |

**Explainer verdicts at closeout:**
- **explainer-orca: FAIL, not cleared to post.** Last reviewed 9:16 = 72 FAIL (`55793987…`, now `explainer-orca_9x16-prev.mp4`);
  last reviewed 16:9 = 68 FAIL (`355d0d72…`, now `explainer-orca_16x9-prev.mp4`). The fix-pass-2 cuts need one review.
- **explainer-blue-whale 9:16: PASS** for `c1c5647ab05231848d86df6ce30f6cab` (77, now `explainer-blue-whale_9x16-prev.mp4`). Post
  that file unless the fix-pass-2 cut (`491cdd4c…`, the current `_9x16.mp4`) passes its own review.
- **explainer-blue-whale 16:9: FAIL, not cleared.** Last reviewed = 66 FAIL (`6847ebca…`, now `explainer-blue-whale_16x9-prev.mp4`).

### Policy outcome (lane R5)

- **Committed:** c56c3ed (disclosure sections in both explainer `description.md` files, checked against official YouTube / TikTok /
  Meta pages ~11:40 UTC, with source links; horror block in `research/R5/horror-pinned-rules-DISCLOSURE.md`, now merged into the
  horror description) and cc5d003 (`research/R5/report.md`, saved by the orchestrator from the lane's returned text). So the
  `research/R5/report.md` links in the descriptions resolve.
- **Set on upload, every pilot:** YouTube "AI use" = **Yes** (older Studio: "Altered content"); TikTok "AI-generated content"
  **on**; Instagram / Facebook **AI label** on; the plain-text synthetic-voice line in every caption; Made for kids = **No**.
  YouTube says disclosing alone doesn't limit reach or earnings, while not disclosing realistic synthetic audio risks Partner
  Program action.
- **Monetisation:** keep our own synthesized music beds (Shorts over 60 s with claimed content are blocked); TikTok Creator Rewards'
  1-minute minimum is met (65.2 / 70.1 / 75.1 s; keep re-cuts above ~62 s); post 9:16 + 16:9 as one Short plus one long-form video;
  every episode needs distinct script and set pieces (YouTube "inauthentic content", 15 Jul 2025); horror stays non-graphic in the
  thumbnail and first seconds; Kokoro-82M (Apache-2.0) is the only voice to ship (Piper voices have non-commercial / research licences).
- **Open:** `report.md` item 3 and pipeline rule 5 say disclosure is not required (animated, generic TTS) and suggest "Altered
  content = No"; the later, source-checked description sections say disclose (Yes). Disclosing is the safe, cost-free side, so the
  descriptions win; reconcile `report.md` rule 5. The later lane's full report ("Platform policy and monetization (official
  sources only)") reached the closeout cut off after its title, so it is not saved; two TikTok Help Center pages and the Instagram
  AI-label steps load only with JavaScript, so their wording comes from TikTok's and Meta's pages as shown in search results.

### MP4s in the pilot folders at closeout (md5 checked ~12:20 UTC)

| File | md5 | Length | What it is |
|---|---|---|---|
| `horror-pinned-rules/horror-pinned-rules_9x16.mp4` | `14376d5d76a453b9fcbf22c542915e87` | 65.216 s | **final, PASS (closeout c1)** |
| `horror-pinned-rules/horror-pinned-rules_9x16-prev.mp4` | `cbe798adc19a9bf5c680d71be4c0e167` | 65.216 s | 6d050b5 re-render of the round 3 cut (not reviewed) |
| `explainer-orca/explainer-orca_9x16.mp4` | `8702a89c1e5e44ca4b4d9bf7ba737d2c` | 75.115 s | fix pass 2, not reviewed |
| `explainer-orca/explainer-orca_9x16-prev.mp4` | `55793987a7dbd227e216683c22d5e0af` | 75.115 s | round 2 cut; closeout regression 72 FAIL |
| `explainer-orca/explainer-orca_16x9.mp4` | `3ac1cbad7f12d78c521b05c9f6a0e258` | 75.115 s | fix pass 2, not reviewed |
| `explainer-orca/explainer-orca_16x9-prev.mp4` | `355d0d72cdebf46ec19837e359f08d52` | 75.115 s | 16:9 fix pass 1; 68 FAIL |
| `explainer-blue-whale/explainer-blue-whale_9x16.mp4` | `491cdd4c60b0ee8ddf7030de8ff2c036` | 70.08 s | fix pass 2, not reviewed |
| `explainer-blue-whale/explainer-blue-whale_9x16-prev.mp4` | `c1c5647ab05231848d86df6ce30f6cab` | 70.08 s | **9:16 PASS (regression 77)** |
| `explainer-blue-whale/explainer-blue-whale_9x16-prev2.mp4` | `d859720c289d1cc5047622d5da44f4d1` | 70.08 s | round 3 PASS cut (80 / 7 of 10) |
| `explainer-blue-whale/explainer-blue-whale_16x9.mp4` | `08093d1acb11c6b415da5130eb5be240` | 70.08 s | fix pass 2, not reviewed |
| `explainer-blue-whale/explainer-blue-whale_16x9-prev.mp4` | `6847ebcab12637f867c5c078ab24eff0` | 70.08 s | 16:9 fix pass 1; 66 FAIL |
| `explainer-orca/first10_v1.mp4`, `first10_v2.mp4`; `explainer-blue-whale/first10_v1.mp4`, `first10_v2.mp4` | `8edb4dce…`, `ffe5be11…`; `f509f705…`, `0828fd54…` | 10.0 s | early first-10 s tests, not for posting |

Older cuts named earlier in this file (orca `79ef71a5…`, horror `ca79bba8…` and the 65.75 s round 2 copy, blue whale 72.9 s
round 2 and `cc0959b6…`, the 16:9 cuts `ebd0a409…` / `da6d25f4…`) are no longer in the folders.

---

## Notes for whoever posts

- **Disclosure:** every `description.md` now carries the R5 section checked against official pages (YouTube "AI use" = Yes,
  TikTok "AI-generated content" on, Meta AI label on, Made for kids = No, synthetic-voice caption line); see "Policy outcome"
  under Closeout and `research/R5/report.md`. Re-check the platform pages on publish day.
- **What to post:** horror `horror-pinned-rules_9x16.mp4` and blue whale `explainer-blue-whale_9x16-prev.mp4` are cleared; the
  orca cuts and both 16:9 cuts are not (see the summary table).
- **MP4s are not in git** (25-40 MB each, local only under `out/pilots/<slug>/`). Text files, thumbnails and QA sheets are committed.
- **Fact checks before publishing:** `episodes/explainer-orca/script.md` (the "~7 boats sunk" count) and `episodes/explainer-blue-whale/script.md` "Facts to verify".
- `episodes/README.md` lengths updated to the shipped cuts (orca 75.1 s, blue whale 70.1 s, horror 65.2 s).
