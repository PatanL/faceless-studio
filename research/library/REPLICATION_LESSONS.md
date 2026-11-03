# Replication lessons (study 1: VS1Z, "The Ancient Jar That Warned an Empire")

Built 2026-11-02 from a shot-for-shot copy of the first 20 s (F0-F599) of RicksClips3000's top Short (30.7M views).

- **Study only.** This was internal and is never published. The decode is `out/study/VS1Z/DECODE.md`, the replica
  is `experiments/three-lane/src/study/VS1Z/`, and the frame-by-frame sheets and match scores are in
  `out/study/VS1Z/compare/` and `out/study/VS1Z/match.json`.
- **What we copied.** The characters, sets and props are our own kit. We copied only the timing, staging, framing,
  camera paths, poses and joins.
- **Ranking.** The gaps are ranked by how much they change the look in a side-by-side, judged on the sheets and the
  per-shot numbers.
- **Status column.**
  - *fixed*: a small kit change, done in this study.
  - *study only*: done inside the study code; promote it if we want it.
  - *visual track*: too big for this study; handed on.

## What matched

- **Timing.** With measured keys, every camera move, face swap, pose snap, prop event and join landed within 1-2
  frames of the reference.
- **Motion curves.** Motion-energy correlation was 0.74-0.82 on the two hook shots, at a lag of 1 frame.
- **Our kit could stage every shot.** The shots were:
  - the push into the dragon's mouth;
  - the crane over the jar lid;
  - the hard cut;
  - the snap punch-in with speed lines;
  - the travel past the jar to the throne;
  - the laugh pull-back;
  - the orbit-push-tilt down the jar;
  - the balcony crane over the army;
  - the dissolves.
- **Where the gap really is.** It was never in *what* the reference does with the camera. It is in how the frame
  *looks* (rows 1-4 of the table) and in how we *author* shots by default (rows 5-9).

## The gaps, ranked

| # | Gap | What the reference does | What we did by default | Effect on the look | Status |
|---|---|---|---|---|---|
| 1 | **Hero props are primitives** | The jar's dragons are sculpted: scales, horns, a crest and a lit gold metal with specular highlights and texture. The frogs have skin detail. The close-up on "a dragon's mouth" is a hero shot of a detailed model. | Our dragon and frogs are built from spheres, cones and tubes with flat two-tone Lambert gold. At mid distance the dragons read as insects (orbit shot, F300-F400). | The largest single difference. Every close-up of the story's key object looks cheap. | **visual track.** We need a hero-prop path: a sculpted or CC0 model per story's key object, with a real metal material (specular and env reflection) kept inside the ink and grade chain. `models.ts` has no dragon or vessel, and the twoTone shader has no specular. |
| 2 | **Interiors are flat, purple and empty** | The throne hall is dense: carved arches, stained glass, dozens of candles and bokeh points, columns with capitals, warm beige stone, a moody falloff into dark corners. | Our hall (plain boxes and cylinders with stoneCourses) read lavender and saturated: the golden preset's violet shade plus blue-heavy carpets. | Mean colour difference (Lab dE on 8 px blocks) was 29-37 in v1. It stayed the largest per-frame error after 3 iterations, even with the palette moved warm. | **visual track.** Interiors need an architecture kit (arches, capitals, vaulting, window tracery) and a "candle interior" light preset: warm key, neutral shade, deep falloff. The presets' violet shade is right for exteriors and wrong for candle-lit rooms. |
| 3 | **Weak depth separation** | Close and medium shots blur the background hard, and the practicals become big round bokeh discs (F30-F59 candle bowls). Foreground masses (the jar lid, the jar's shoulder, the balustrade) sit in every frame. | The lens blur maxes out soft (cInf 18 is the most we used), with no bokeh shape. Glow sprites stay small. | The frames read flatter and busier: everything is equally sharp. | **visual track:** a bokeh pass for emissive points (shape and size from circle of confusion). **Story rule (free):** put a foreground mass in every shot. |
| 4 | **Character silhouettes and costume detail** | Hats with ornaments and pins, coloured robes with gold trim, sashes. Heads are a little larger relative to bodies. Thick even ink. | Our costumes are flatter blocks of colour. The master/official costumes read as modern. | Moderate. The face-swap timing matched, so the acting reads; the figures look plainer. | **visual track:** a costume detail pass (trim, sashes, hat ornaments) for period courts. |
| 5 | **The camera could not be authored exactly** | Every move is placed: a 12 f push, a 3 f snap, a 14 f crane, a 6 s orbit. The ease differs per move (snap-out, ease-in-out, ease-in into a cut). | `CamPath` lands every move about 0.27 s after its key, on a fixed 0.9 s cosine glide, and adds drift, push-in and orbit on every hold. A 3 f snap, a 12 f push or a linear orbit were impossible, and keys were never reached exactly. | Without exact moves, the timing and framing match is unreachable. With them, the timing matched within 1-2 f. | **fixed:** `kit/campath.ts` exact mode. When any key sets `ease`, the path passes every key at its time. `ease` ∈ lin, io, in, out, io5, snap shapes each segment; `curve` uses Catmull-Rom through the neighbours for orbits and cranes. Paths without `ease` are unchanged. |
| 6 | **Framing is authored by cast size, not by screen position** | Shots are composed as "the subject at (x, y), this size, seen from here": inventor head 0.17 at (0.27, 0.48), emperor 0.13 at (0.55, 0.40). | `castKey` / `fit` centre the cast and size it to presets (0.20 / 0.11 / 0.06), so everything drifts toward the centre. | Off-centre thirds framing with a foreground mass is the reference look; our presets centre. | **study only:** `frameKey(f, S, sx, sy, h, frac, az, el, fov)` in `study/VS1Z/story.ts`. Promote it into `kit/framing.ts` next to `fit`. |
| 7 | **Our gates would fail the master** | The emperor's close-up crops both flanking guards at the frame edges on purpose (F168-F192). In the jar orbit, the court figures far behind the jar are specks (head 0.04). | The `edge` gate flags any body cut by the frame edge; the `cast` gate flags a group whose median head is under 0.05. 7 failures on the reference's own staging. | The gates push us away from the reference's composition: we keep flank figures whole and keep inserts populated. | **visual track / kit:** the edge gate should only count the *subject* (or figures with a head ≥ 0.07). The cast gate should only count the group's named cast. Background extras should be exempt. Small, but it touches the gate semantics every episode uses, so it was not changed here. |
| 8 | **No speed lines and no physical object drop** | Speed lines radiate on the snap at "run." (F142-F160). The ball physically drops from the mouth to the frog on "falls" (F121-F131) and on "fell," (F555-F569), landing with an impact star. | Rule E7 lists speed lines; there was no kit piece. There was no "drop this prop into that target with gravity on this word" helper. | Small in the frame, but these are the beats that illustrate the hook's words. | **study only:** `SpeedLines` overlay (`study/VS1Z/VS1Z.tsx`), the `fall()` path and `ballRig` (`study/VS1Z/story.ts`, `sets.ts`). Promote both to `fx2.ts`. |
| 9 | **Travel past a foreground object as the join** | Inside one place, the camera changes subject by flying past a big object, which crosses the frame like a wipe: the passing jar at F160-F163, the jar lid at F60-F70. | Our travel join exists for groups in one world, but our shot plans never route the path *behind* an object. | It hides the change of subject without a dissolve. | **Story rule (free):** route travels behind a foreground mass. |
| 10 | **Light is constant within a place** | The hall never relights in the first 20 s. The first light change is the cut to the balcony (interior warm to exterior day). | — | No gap: rule L2's arc is carried by place changes here, not by relights. | **Note:** don't add relights inside a hook just to tick L4. |

## Process lessons (how we work by default vs how the master works)

1. **We plan places; he plans nouns.** Our shot plans list places and then cast framings. His shot is picked by the
   nouns of the line in order: the camera arrives at each named thing within about 0-10 frames of its word. Our
   script-to-shot step should list each line's nouns with their word frames and give each one an arrival.
2. **One line, one move.** We cut or dissolve at sentence boundaries *and* inside lines. He keeps a line in one
   camera thought (line 3 is one 6 s orbit-push-tilt) and changes the shot at the pause between lines.
3. **The hook's loudest word gets the hardest hit.** "run." is the loudest syllable (energy peak at F142-F144). It
   gets the snap punch-in (55.7 px/f), the terrified face, the sweat drop and speed lines on the same 3 frames. Our
   hooks spread the emphasis across the line. The voice track should mark one payoff word per hook line; the camera
   then snaps on its onset frame.
4. **Measure, then author.** Copying from measured keys (the reference frame, the screen position, the size) took 3
   iterations to get timing within 2 f. Our usual "describe the shot, then tune" loop cannot reach that.
   `frameKey` plus the exact camera path make it possible for originals too: write the framing you want at the frame
   you want it.

## Measured match (per shot, final iteration)

The scores and their notes are in `out/study/VS1Z/match.json`.

- **Structure.** SSIM on blurred luma, caption band masked: 0.22-0.36. It stays low because the sets and props
  differ by design.
- **Motion.** Correlation of the motion-energy curves after the best lag: 0.4-0.8.
- **Judgement.** Timing and joins are good to close. Framing is good after the fixes. The flatter look comes from the
  props and sets (rows 1-4).

## Round 3 (visual track, 2026-11-03): what the kit now does about rows 1-8

- **Rows 1-4** are now kit pieces (`kit/materials.ts`, `kit/heroprops.ts`, `kit/interior.ts`, the `candle` preset,
  `kit/depth.ts`, the court costumes). The replica uses them in v4-v10 (`renders/ours_v10r.mp4`).
- **Rows 6 and 8** are promoted: `frameKey` is in `kit/framing.ts`, `SpeedLines` in `kit/speedlines.tsx`, `fall` and
  `drop` in `kit/fx2.ts`.
- **Row 7** is done: `PersonSpec.extra` and `GroupSpec.cropOK`.
- **Camera smoothness** (owner):
  - `scripts/cam_smooth.py` measures it.
  - Paths are filtered in time (`kit/campath.ts`), with camera motion blur.
  - The `smooth` gate fails unintended velocity steps.

Per-shot scores before and after are in `out/study/VS1Z/match.json` (`match_score_v3_blind`, `match_score_v10`). No
shot reaches 8: the measured term (SSIM ~0.2 with our own sets, by design) caps it near 7.5 even at a judgement of 8.5,
and the blind judge still puts props and look at 4-6 (dragons read dark against the master's polished gold, the
balcony has no painted town, and the throne room is plainer).
