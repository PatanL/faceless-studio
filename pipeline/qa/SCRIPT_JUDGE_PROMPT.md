# Script judge: rubric items (story lane)

`pipeline/qa/script_judge.py` measures everything it can count (length, pace, pauses, hook size, beat positions,
numbers, dialogue). Seven items need a reader. Answer them with this prompt (any LLM or a person), save the JSON,
and pass it with `--rubric path.json`. The ranges come from the 24 RicksClips3000 story Shorts
(`research/references/data/ricks24_beats.json`, `research/library/STORY_SCRIPT_SPEC.md`).

## Prompt

You are reviewing a narration script for a ~60 s animated story Short (stick figures in a 3D world, one narrator).
Read only the narration. For each item give a number and a one-line reason that quotes the script's own words.
Be strict: count only what a viewer would actually hear.

1. `facts`: how many distinct real-world claims does the script teach (history or mechanism the viewer could look
   up)? Count "the guns were bronze" and "a gust heeled the ship" as two; don't count invented dialogue or mood.
   Reference: hits teach 4-7 (median 5); fiction teaches 0.
2. `jokes`: how many lines are written to get a laugh or a smirk (a deadpan aside, a mocking line, an absurd
   comparison, a punchline)? Reference: hits have 1-4 (median 2), e.g. a jeering crowd line or an ironic aside.
3. `reversal`: how many times does the situation flip against expectation (the mocked person is proven right,
   the trap springs on the trapper, the safe choice is the deadly one)? 0, 1, 2...
4. `ridicule`: how many lines show someone doubting or mocking the strange act before it is vindicated?
5. `mechanism_visible`: 1 if the reason the story turns is a physical cause the camera can watch happen (a weight,
   a wave, heat, a pendulum, water through a port); 0 if it is only a rule, a law, a feeling or a statistic.
6. `shootable_share`: the share of sentences (0-1) that name a concrete thing or action an animator can put on
   screen at that moment. Abstract lines ("It was a mistake", "Nobody knew why") don't count unless they name a
   thing.
7. `hook_act_on_screen`: 1 if the first sentence describes a person doing a strange, concrete thing that can be
   frame 0 (not a date, a place card, a question or a narrator's claim); 0 otherwise.

Return only JSON:

```json
{"facts": {"value": 5, "note": "..."}, "jokes": {"value": 2, "note": "..."}, "reversal": {"value": 1, "note": "..."},
 "ridicule": {"value": 1, "note": "..."}, "mechanism_visible": {"value": 1, "note": "..."},
 "shootable_share": {"value": 0.95, "note": "..."}, "hook_act_on_screen": {"value": 1, "note": "..."},
 "reviewer": "who answered", "date": "YYYY-MM-DD"}
```
