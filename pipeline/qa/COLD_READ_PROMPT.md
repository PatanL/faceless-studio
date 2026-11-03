# Cold-reader "makes sense" test (story lane, required before voicing)

`script_judge.py` checks structure. This checks whether a viewer who knows nothing **understands** the story and is
**hooked**. A fresh agent with zero context reads only the narration (pass A), then the narration plus the shot list
(pass B), and answers in JSON. `pipeline/qa/cold_read.py` builds both prompts and scores the answers against an
answer key written by the script's author.

**Pass rule (owner, 2026-11-02):** a script is voiced only when pass A retells every key beat (coverage 1.0 on
who, what happened, why and twist), has **no reread line the reader marks `lost`**, and no logic jump marked
`blocks_understanding`. Every `slowed` line, unexplained term and "sounds wrong" flag is fixed or answered in a note.
The reader is told to be picky, so a few `slowed` flags are normal: on 2026-11-02 the three story scripts drew 7-11
reread flags each while their readers still retold every beat.

## How to run it (agent-run; the CLI only builds prompts and scores)

1. Write the key: `episodes/<slug>/cold_key.json` or next to a draft (`research/library/drafts/<slug>.cold_key.json`).
   Format in `cold_read.py --help`. Write it before reading any answer.
2. `python3 -m pipeline.qa.cold_read prompt <script.md>` -> paste into a **fresh** agent (no repo access, no title,
   no other context). Save its JSON reply as `<slug>.cold_A.json`.
3. Send the same agent `python3 -m pipeline.qa.cold_read prompt <script.md> --shots <shot list> --pass B`.
   Save as `<slug>.cold_B.json`. (B tells you what the pictures fix and what they can't.)
4. `python3 -m pipeline.qa.cold_read score <slug>.cold_A.json --key <key> [--b <slug>.cold_B.json] [--out report.md]`.
5. Fix every reread line and real jump, then repeat with a **new** agent (a reader who has seen the old version is
   no longer cold).

## The prompt (cold_read.py fills {NARRATION} and, for pass B, {SHOTS})

You are a viewer who has never heard of this story. Below is the narration of a 60-second animated Short, exactly as
it is spoken, one paragraph per line. You hear it once at normal speed; you cannot pause or look anything up. Don't
use outside knowledge to fill gaps: if the narration doesn't say it, it's a gap.

NARRATION:
{NARRATION}

{SHOTS}

Answer in JSON only, with these keys:

- `hook`: after hearing only the first line, `{"keep_watching": 1-5, "question_in_my_head": "...", "why": "..."}`.
- `who`: every character or group and what they want, in your own words.
- `what_happened`: the events in order, one short sentence each.
- `why`: the reason the story turns out the way it does (the mechanism), in your own words, as you would explain
  it to a friend.
- `twist`: what the ending reveals or flips, in one sentence.
- `reread_lines`: every line you'd have to hear twice to follow, as `{"line": "<quote>", "why": "...", "level": "lost" | "slowed"}`.
  Include lines where a pronoun is unclear, two numbers collide, a term arrives before it's explained, or a sentence
  is too long to hold. `lost` = after hearing it once you could not say what just happened (you'd lose the thread);
  `slowed` = you followed it, but it cost effort.
- `unexplained_terms`: words or names a typical 16-year-old wouldn't know and the narration never explains.
- `logic_jumps`: places where the story skips a step, as `{"between": "<line> -> <line>", "missing": "...", "blocks_understanding": true | false}`
  (true only if the gap stops you understanding the story, not for nice-to-know details).
- `sounds_wrong`: claims that sound false, contradictory or confusing, with why.
- `confidence`: 1-5, how sure you are you understood the whole story.

Be picky. A flag costs nothing; a viewer who swipes away costs everything.
