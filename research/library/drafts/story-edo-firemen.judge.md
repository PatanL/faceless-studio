# Script judge: research/library/drafts/story-edo-firemen.md

Spec: `research/library/STORY_SCRIPT_SPEC.md`. Timing: estimated at 3.9 words/s.
**Score: 100.0 / 100** (out of 67 checkable points; rubric items not answered).

## Outside the spec (biggest point losses first)

- nothing

## All checks

| check | value | target | points |
|---|---|---|---|
| runtime_s | 62.3 | 55-65.5 | 5.0/5 |
| words | 242 | 200-245 | 3.0/3 |
| hook_words | 20 | 8-21 | 4.0/4 |
| hook_s | 5.13 | 2.5-5.5 | 4.0/4 |
| hook_form | declarative, concrete subject |  | 5.0/5 |
| setup_end_pct | 35.8 | 12-36 | 6.0/6 |
| esc_steps | 3 | 3-6 | 8.0/8 |
| pivot_pct | 67.1 | 55-82 | 8.0/8 |
| you_see | [67.1] |  | 3.0/3 |
| mech_words | 55 | 28-55 | 5.0/5 |
| last_line | A week later, the owner finishes his new house, the house next door catches fire |  | 5.0/5 |
| numbers | 1 | 1-5 | 4.0/4 |
| dialogue | 5 | 1-5 | 3.0/3 |
| sentence_len | {"median": 12.5, "max": 24, "share_le6": 0.25, "share_ge20": 0.15} |  | 4.0/4 |

## Beat map (as detected; override with --beats)

| # | beat | start s | words | sentence |
|---|---|---|---|---|
| 1 | HOOK | 0.0 | 20 | He smashed a man's house during breakfast, with a fire so close the man's tea was boiling in his cup. |
| 2 | setup | 5.13 | 9 | The owner jumps up, still holding his rice bowl. |
| 3 | setup | 7.44 | 9 | "The fire's next door, you've got the wrong house!" |
| 4 | setup | 9.74 | 16 | He licks a finger, checks the wind, then hooks a pole into the roof and pulls. |
| 5 | setup | 13.85 | 17 | The owner grabs a broom and chases him around the house, rice bowl in the other hand. |
| 6 | setup | 18.21 | 8 | Half the street comes out with buckets, laughing. |
| 7 | setup | 20.26 | 2 | "Some fireman! |
| 8 | setup | 20.77 | 6 | He can't even find the fire!" |
| 9 | E1 | 22.31 | 13 | Then he pulls down the last wall, just as the wind picks up. |
| 10 | E1 | 25.64 | 2 | "Wrong house!" |
| 11 | E2 | 26.15 | 16 | Soon a gust drives the fire straight toward the gap, and the laughing street behind it. |
| 12 | E3 | 30.26 | 18 | Seconds later, the flames leap over and land on the bare dirt where the house used to be. |
| 13 | E3 | 34.87 | 4 | And there they stop. |
| 14 | E3 | 35.9 | 12 | They flicker, they shrink, and they die, right at the owner's feet. |
| 15 | E3 | 38.97 | 11 | The street goes quiet, and somebody slowly puts down his bucket. |
| 16 | PIVOT | 41.79 | 21 | You see, firemen in old Edo really did this, because their hand pumps could barely throw water past the next roof. |
| 17 | mechanism | 47.18 | 13 | In a wooden city, in a strong wind, that won't drown a fire. |
| 18 | mechanism | 50.51 | 5 | But you can starve it. |
| 19 | mechanism | 51.79 | 16 | Tear down the houses in its path, and when it arrives, there's nothing left to burn. |
| 20 | LAST | 55.9 | 24 | A week later, the owner finishes his new house, the house next door catches fire, and the same fireman knocks politely, holding his pole. |

## Pace

- 242 words, 20 sentences, 62.3 s, 3.9 words/s; sentence median 12.5 words, longest 24.
- 'You see' at [67.1] % of runtime; numbers ['Half']; 'you' 1.2 per 100 words.
- setup: sentences 2-8, 17.18 s, 67 words, 3.9 w/s, starts at 8.2 %.
- mechanism: sentences 16-19, 14.11 s, 55 words, 3.9 w/s, starts at 67.1 %.
- E1: sentences 9-10, 3.84 s, 15 words, 3.91 w/s, starts at 35.8 %.
- E2: sentences 11-11, 4.11 s, 16 words, 3.89 w/s, starts at 42.0 %.
- E3: sentences 12-15, 11.53 s, 45 words, 3.9 w/s, starts at 48.6 %.
