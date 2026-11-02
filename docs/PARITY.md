# Goal 1: production quality parity with the reference channels

Owner (2026-11-02): the first goal is matching the reference channels' production quality, because it's definable and
verifiable. Views come after.

A Short **passes parity** for its lane when all three checks pass.

## 1. Measured checks (scripts, every frame)

Measure ours and 3+ reference Shorts of the lane with the same tools (`pipeline/qa/frames30.py`,
`research/frame-analysis/tools/`, `pipeline/qa/gate.py`, `research/music/tools/`). Ours must sit inside the
references' range (min–max) or beat it on:

| Check | Tool | Notes |
|---|---|---|
| Visual change interval (median s between changes) | frames30 / every_frame.py | Zack D. ~1.4 s cuts; Kurzgesagt 1.6–2.4 s |
| Setting changes per minute, longest hold | every_frame.py + settings | refs 5–8/min; no hold > 40 s |
| Frozen holds, one-frame pops/snaps | frames30 flags | none unintended |
| Detail density (D1–D5) and colour families | experiments/kurz-style tools | within range for the lane's look |
| Captions: phrase pages, safe area, no collisions | gate.py + staging | zero violations |
| Loudness, voice-over-music gap, true peak | gate.py, measure tools | −14 LUFS; voice ~17 LU over the score |
| Hook: subject on screen at frame 0, premise landed by 3 s | transcript + frame 0 | as the refs do |

## 2. Blind side-by-side panel

Three judges each see unlabeled pairs (ours vs a reference Short of the same lane, order decided by a coin derived
from the file hashes, never by the judge) as matched-moment frame sheets plus the two audio tracks' transcripts. For
each principle in FEEDBACK.md they answer "A better / same tier / B better". **Pass:** across judges, ours is
"same tier or better" on every principle in at least 2 of 3 judges, and nobody can tell ours apart by a production
flaw they can point to (a judge naming a concrete defect in ours = fail that principle).

## 3. Owner check

The owner watches ours next to one reference on a phone and agrees they're the same tier.

## Order of work

Parity first, per lane, with the specialist workflow (`scripts/workflows/video_pipeline.js`). Record each attempt's
check results in `docs/PARITY_LOG.md`. Posting and view experiments (docs/EXPERIMENTS.md) run alongside but don't
replace this goal.
