# Script judge: research/library/drafts/story-myeongnyang.md

Spec: `research/library/STORY_SCRIPT_SPEC.md`. Timing: estimated at 3.67 words/s.
**Score: 97.0 / 100** (out of 92 checkable points; rubric items included).

## Outside the spec (biggest point losses first)

- **jokes** = 1.0 (target 2-6; -2.0 pts). 'His captains hang back, happy to let the admiral go first' (the 'His captains thought he was mad' line is doubt, not a joke). v1 had 2; the second went in the length trim  
  _jokes: top median 2 (1-4), >= 2 in 6/8 top vs 6/16 rest_
- **mech_words** = 58 (target 28-55; -0.4 pts). 15.8 s, 0.25 of the words  
  _mechanism: top 32-49 words, 9-15 s, 15-32 % of the words_
- **hook_s** = 5.72 (target 2.5-5.5; -0.4 pts). estimated  
  _hook spoken in 3.0-5.4 s (top 8)_

## All checks

| check | value | target | points |
|---|---|---|---|
| runtime_s | 64.56 | 55-65.5 | 5.0/5 |
| words | 236 | 200-245 | 3.0/3 |
| hook_words | 21 | 8-21 | 4.0/4 |
| hook_s | 5.72 | 2.5-5.5 | 3.65/4 |
| hook_form | declarative, concrete subject |  | 5.0/5 |
| setup_end_pct | 18.6 | 12-36 | 6.0/6 |
| esc_steps | 4 | 3-6 | 8.0/8 |
| pivot_pct | 60.8 | 55-82 | 8.0/8 |
| you_see | [11.4, 60.8] |  | 3.0/3 |
| mech_words | 58 | 28-55 | 4.57/5 |
| last_line | Yi had a narrow strait, and that day the sea switched sides. |  | 5.0/5 |
| numbers | 5 | 1-5 | 4.0/4 |
| dialogue | 2 | 1-5 | 3.0/3 |
| sentence_len | {"median": 11, "max": 21, "share_le6": 0.19, "share_ge20": 0.14} |  | 4.0/4 |
| facts | 7.0 | 4-7 | 6.0/6 |
| jokes | 1.0 | 2-6 | 2.0/4 |
| reversal | 2.0 | 1-3 | 2.0/2 |
| ridicule | 1.0 | 1-9 | 2.0/2 |
| mechanism_visible | 1.0 | 1-1 | 4.0/4 |
| shootable_share | 1.0 | 0.9-1.0 | 4.0/4 |
| hook_act_on_screen | 1.0 | 1-1 | 3.0/3 |

## Beat map (as detected; override with --beats)

| # | beat | start s | words | sentence |
|---|---|---|---|---|
| 1 | HOOK | 0.0 | 21 | Told to give up the navy, Admiral Yi wrote back four words and sailed thirteen ships at a hundred and thirty-three. |
| 2 | setup | 5.72 | 6 | His captains thought he was mad. |
| 3 | setup | 7.36 | 11 | You see, Japan's invasion fleet has just wiped out Korea's navy. |
| 4 | setup | 10.35 | 6 | Yi's ships are all that's left. |
| 5 | E1 | 11.99 | 18 | So when the king tells him to give up the navy, Yi writes back: "I still have ships." |
| 6 | E1 | 16.89 | 7 | But the Japanese fleet fills the horizon. |
| 7 | E2 | 18.8 | 17 | So Yi picks his spot: a strait so narrow the huge fleet has to squeeze through it. |
| 8 | E2 | 23.43 | 12 | Locals call it the crying strait, for the sound of its water. |
| 9 | E3 | 26.7 | 9 | The Japanese pour in, carried by that rushing water. |
| 10 | E3 | 29.16 | 5 | Ship after ship after ship. |
| 11 | E4 | 30.52 | 11 | His captains hang back, happy to let the admiral go first. |
| 12 | E4 | 33.51 | 21 | The strait is so tight only a few Japanese ships can reach Yi at once, and his cannons hold them off. |
| 13 | PIVOT | 39.24 | 8 | You see, that rushing water is the tide. |
| 14 | mechanism | 41.42 | 10 | Every few hours, it stops and runs the other way. |
| 15 | mechanism | 44.14 | 11 | Historians who rebuilt that day's tides think the tide turned mid-battle. |
| 16 | mechanism | 47.14 | 8 | Now the water runs back out to sea. |
| 17 | mechanism | 49.32 | 21 | The front Japanese ships get shoved back into their own ships, and the tangle is stuck in front of Yi's cannons. |
| 18 |  | 55.04 | 11 | Korean records count thirty-one Japanese ships lost, and none of Yi's. |
| 19 |  | 58.04 | 4 | The rest turn back. |
| 20 |  | 59.13 | 7 | The king thought Yi had nothing left. |
| 21 | LAST | 61.04 | 12 | Yi had a narrow strait, and that day the sea switched sides. |

## Pace

- 236 words, 21 sentences, 64.56 s, 3.67 words/s; sentence median 11 words, longest 21.
- 'You see' at [11.4, 60.8] % of runtime; numbers ['four', 'thirteen', 'hundred', 'thirty-three', 'thirty-one']; 'you' 0.8 per 100 words.
- setup: sentences 2-4, 6.27 s, 23 words, 3.67 w/s, starts at 8.9 %.
- mechanism: sentences 13-17, 15.8 s, 58 words, 3.67 w/s, starts at 60.8 %.
- E1: sentences 5-6, 6.81 s, 25 words, 3.67 w/s, starts at 18.6 %.
- E2: sentences 7-8, 7.9 s, 29 words, 3.67 w/s, starts at 29.1 %.
- E3: sentences 9-10, 3.82 s, 14 words, 3.66 w/s, starts at 41.4 %.
- E4: sentences 11-12, 8.72 s, 32 words, 3.67 w/s, starts at 47.3 %.
