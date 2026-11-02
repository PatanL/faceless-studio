# Quality principles (read by every builder and reviewer)

Keep this file short and general. Reviewers apply these the way a sharp viewer would and compare against reference videos frame by frame; they should catch specific problems (a jellyfish beside a polar hunt, a label on a face) from the principles, not from a checklist of past incidents. Dated notes and decisions live in `docs/FEEDBACK_LOG.md`.

**Ship bar:** a reviewer watching our video next to the references would call it the same tier, every principle scores ≥ 7/10, and the hook ≥ 8/10. Report defects with timestamps and frames.

## For every video

1. **Hook first.** Within ~3 s the viewer has a reason to keep watching. Frame 0 is the cover: never black or a bare title card. For explainers, the hook sells a specific question, ideally with "you" in it (`research/corpus/*/PLAYBOOK.md` has the formulas that work), and the first proof (a number, a scale comparison, a visible consequence) arrives by ~5–8 s.
2. **The world makes sense.** Everything on screen belongs there: right place, depth, climate, era, scale and lighting, and motivated by the story at that moment. Nothing is decoration for its own sake.
3. **Show what's said.** Every line is literalized on screen; the visuals change at least every ~2.5–4.5 s, and the setting changes as the story moves (a new place, a new depth, a map or diagram), as often as the references do.
4. **Consistent and smooth.** Characters, objects and style stay consistent between shots; motion is plausible and never frozen or snapping.
5. **Readable on a phone.** Whole-phrase captions, no text collisions, inside the safe area; the subject reads at a glance.
6. **Natural sound.** A natural, non-robotic voice; seamless audio; music under the voice; sound effects on the action.
7. **Quality over novelty.** Use whatever technique looks best (standard craft is fine). Only characters, assets, compositions and branding must be our own.
8. **Pay off the promise.** The viewer can feel progress toward the payoff (a depth meter, a counter, a countdown); the payoff is clear and on time; no bait.

## Process

- Before building: study the references frame by frame (native frame rate) for this format.
- After building: review every frame at the native frame rate (`pipeline/qa/frames30.py`, REVIEW_PROMPT §3), compare with the references side by side as a viewer would, then fix what a viewer would notice most.
- Separate formats have separate references (the owner's cinematic "Caught"/Malfoid edits are a different format: motion-and-feeling hooks, continuous POV; don't apply explainer rules there or vice versa).
