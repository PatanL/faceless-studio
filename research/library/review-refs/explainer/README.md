# Explainer review refs (pilot QA)

These are three outlier references with 12 frames each, all 1080 px wide (`NN_<qa_class>.jpg`). Every reference uses the same 12 shot classes in the same order, so `scripts/side_by_side.sh <pilot.mp4> explainer` can put the pilot's frame for each class next to them. Timestamps and descriptions are in `../frames_spec.json`; a frame marked `substitute` there means that reference has no shot of that class, so the closest shot was used.

| Ref | Score | Why it's here | Format |
|---|---|---|---|
| [fGcgWaswMns](https://www.youtube.com/watch?v=fGcgWaswMns), Depth Theory, *Why You'd Never Want To Meet A Sperm Whale* | 14.57x (2.3M views on about 6K subs) | **The style target**: flat 2D vector ocean, "you" diver, scale cards, counters, options menu. Most of the pilot's kit is modelled on it. | 16:9, 10 min |
| [mzeN0BXR4e0](https://www.youtube.com/watch?v=mzeN0BXR4e0), Mr. Science, *Why Deep Sea Creatures Get Creepier the Deeper You Go* | 12.86x (17.2M) | Descent-as-structure: the depth-zone diagram lights up a new band each chapter. The thumbnail creature appears as frame 1 (real footage). | 16:9, 18 min |
| [6mRR91AbxjQ](https://www.youtube.com/shorts/6mRR91AbxjQ), Zack D. Films, *How Horseflies Bite You* | 1.87x (13.7M) | The strongest **9:16** explainer outlier, which matches the pilot format: second-person line 1, 2-4 word captions, a surface-to-cutaway morph, a highlight glow, and a loop ending. It's 3D CG; copy the pacing and captions, not the render style. | 9:16, 28 s |

## Frames (row = shot class)

| # | Class | fGcgWaswMns | mzeN0BXR4e0 | 6mRR91AbxjQ |
|---|---|---|---|---|
| 01 | thumbnail | "IT HEARS YOU.." + tiny diver, red arrow | "WE REALLY CAN'T EXPLAIN" + creature vs diver | Shorts auto-cover (crop) |
| 02 | hook_0s | vector diver, god rays (3 s) | real ROV footage "Real footage..." (1.5 s) | macro fly + "When a horse fly" |
| 03 | hook_caption | false-safety checklist chip with tick | stakes cutaway (space) | wide scale reveal "bites you" |
| 04 | hero_creature | SPERM WHALE reveal, centred caps label | anglerfish | ECU six needle tools |
| 05 | you_scale | silhouette over ruler "~16 M" | comparison composite | macro-as-landscape |
| 06 | diagram_anatomy | cutaway "A BIOLOGICAL SPEAKER" | depth-zone cross-section | surface-to-cutaway morph |
| 07 | stat_counter | meter "236 dB", red underlined header | zone diagram, new band lit | cutaway (substitute) |
| 08 | title_question_card | "WHAT DOES IT EAT?" | sonar echogram (substitute) | metaphor swap (substitute) |
| 09 | map_or_depth | depth counter "1,190 m" + ruler | Google Earth trench | (substitute) |
| 10 | options_or_list | YOU vs SPERM WHALE speed bars (options menu beat) | montage (substitute) | (substitute) |
| 11 | stock_proof | short real clip as proof | reef B-roll | glow highlight (substitute) |
| 12 | ending_verdict | "IF IT DECIDED YOU WERE A PROBLEM..." over struck options | recap montage | wide loop bookend |

## What a pilot must match (pass/fail at review)

**Frame and colour**
- The ocean is a deep navy-to-teal vertical gradient with god rays and slow particles. Never flat black, and never a bright cyan "pool". The darkest band is near-black navy (about `#06121c`) and the lightest about `#2a6a8a`.
- **One accent colour for danger**: red (about `#e5383b`) only on the threat word, the header underline or the arrow. Everything else is white or grey on navy.
- Creatures are flat vector with a slight texture, side-on, filling at least 40% of the frame width in hero shots. The human ("you" or the diver) is drawn small next to them; the scale contrast *is* the shot.

**Type and captions**
- Labels and cards are heavy sans in caps with slight tracking: centred lower third for names ("SPERM WHALE"), and centred at the top, red and underlined, for questions and headers.
- 9:16 burned captions: 2-4 words per card, bold white with a soft shadow, inside the safe area (`SAFE_AREA` in `studio/src/core/schema.ts`, about y 230-1480). A new card every 1-3 s, never covering the creature's face or the number being explained.
- Numbers are always **drawn and animated** (a filling meter, a counting counter, a ruler label) and placed next to a familiar object.

**Hook and pacing**
- **Frame 0 must not be black.** The cover of a Short is frame 0, and the test render faded in from black. By 0.5 s the creature or the "you" figure is on screen with a caption that puts the viewer in the scene (second person).
- Something new appears every 2-4 s (a label, tick, counter or cut). For Shorts, aim for a hard cut or a new layer every 1-3 s; a hold longer than 4 s fails.
- The last frame bookends the hook (the same creature or the same line), not an end card.

**Thumbnail (separate PNG)**
- 2-4 words that add a claim the title doesn't make, in white with one red word, heavy condensed caps, on a near-black background. A tiny human with a red arrow and the creature at a much larger scale.

**What may differ:** creature species, the exact layout of cards, music. Don't copy any reference's text, characters or footage (BRIEF rule 5).

## How to review

```bash
# needs research/library/review-refs (in git) and the pilot MP4 (+ its storyboard if found automatically)
scripts/side_by_side.sh out/explainer-orca.mp4 explainer                  # -> out/qa/explainer-orca_vs_explainer.jpg
scripts/side_by_side.sh out/explainer-orca.mp4 explainer --thumb out/thumbs/explainer-orca.png --refs fGcgWaswMns,6mRR91AbxjQ
```
Read the JPG. Each row shows the references on the left and the pilot (red frame) on the right. Fail the pilot if a row breaks one of the rules above.
