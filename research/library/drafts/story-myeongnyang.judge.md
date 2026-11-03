# Script judge: research/library/drafts/story-myeongnyang.md

Spec: `research/library/STORY_SCRIPT_SPEC.md`. Timing: estimated at 3.67 words/s.
**Score: 98.5 / 100** (out of 92 checkable points; rubric items included).

## Outside the spec (biggest point losses first)

- **numbers** = 6 (target 1-5; -0.8 pts). one, thirteen, hundred, thirty-three, thirty-one, one  
  _number tokens: top 1-5 (median 3), rest median 5.5 (up to 15)_
- **hook_s** = 5.72 (target 2.5-5.5; -0.4 pts). estimated  
  _hook spoken in 3.0-5.4 s (top 8)_
- **mech_words** = 56 (target 28-55; -0.1 pts). 15.26 s, 0.23 of the words  
  _mechanism: top 32-49 words, 9-15 s, 15-32 % of the words_
- **runtime_s** = 65.65 (target 55-65.5; -0.1 pts). estimated from word count  
  _top 8: 39-65 s, median 62; the two shortest refs (31, 35 s) are the two lowest_

## All checks

| check | value | target | points |
|---|---|---|---|
| runtime_s | 65.65 | 55-65.5 | 4.92/5 |
| words | 240 | 200-245 | 3.0/3 |
| hook_words | 21 | 8-21 | 4.0/4 |
| hook_s | 5.72 | 2.5-5.5 | 3.65/4 |
| hook_form | declarative, concrete subject |  | 5.0/5 |
| setup_end_pct | 18.3 | 12-36 | 6.0/6 |
| esc_steps | 4 | 3-6 | 8.0/8 |
| pivot_pct | 59.3 | 55-82 | 8.0/8 |
| you_see | [11.2, 59.4] |  | 3.0/3 |
| mech_words | 56 | 28-55 | 4.86/5 |
| last_line | The king thought Yi had nothing left, but he had one line and a sea that switche |  | 5.0/5 |
| numbers | 6 | 1-5 | 3.2/4 |
| dialogue | 2 | 1-5 | 3.0/3 |
| sentence_len | {"median": 11, "max": 21, "share_le6": 0.24, "share_ge20": 0.14} |  | 4.0/4 |
| facts | 7.0 | 4-7 | 6.0/6 |
| jokes | 2.0 | 2-6 | 4.0/4 |
| reversal | 2.0 | 1-3 | 2.0/2 |
| ridicule | 1.0 | 1-9 | 2.0/2 |
| mechanism_visible | 1.0 | 1-1 | 4.0/4 |
| shootable_share | 1.0 | 0.9-1.0 | 4.0/4 |
| hook_act_on_screen | 1.0 | 1-1 | 3.0/3 |

## Beat map (as detected; override with --beats)

| # | beat | start s | words | sentence |
|---|---|---|---|---|
| 1 | HOOK | 0.0 | 21 | Told to give up the navy, Admiral Yi answered with one line and sailed thirteen ships at a hundred and thirty-three. |
| 2 | setup | 5.72 | 6 | His captains thought he was mad. |
| 3 | setup | 7.36 | 11 | You see, Japan's invasion fleet has just wiped out Korea's navy. |
| 4 | setup | 10.35 | 6 | Yi's ships are all that's left. |
| 5 | E1 | 11.99 | 17 | So when the king tells him to give up the navy, Yi answers: "I still have ships." |
| 6 | E1 | 16.62 | 7 | But the Japanese fleet fills the horizon. |
| 7 | E2 | 18.53 | 17 | So Yi picks his spot: a strait so narrow the huge fleet has to squeeze through it. |
| 8 | E2 | 23.16 | 12 | Locals call it the crying strait, for the sound of its water. |
| 9 | E3 | 26.43 | 9 | The Japanese pour in, carried by that rushing water. |
| 10 | E3 | 28.88 | 5 | Ship after ship after ship. |
| 11 | E4 | 30.25 | 11 | His captains hang back, happy to let the admiral go first. |
| 12 | E4 | 33.24 | 21 | The strait is so tight only a few Japanese ships can reach Yi at once, and his cannons hold them off. |
| 13 | PIVOT | 38.96 | 8 | You see, that rushing water is the tide. |
| 14 | mechanism | 41.14 | 10 | Every few hours, it stops and runs the other way. |
| 15 | mechanism | 43.87 | 11 | Historians who rebuilt that day's tides think the tide turned mid-battle. |
| 16 | mechanism | 46.87 | 6 | Now the water runs back out. |
| 17 | mechanism | 48.5 | 21 | The front Japanese ships get shoved back into their own ships, and the tangle is stuck in front of Yi's cannons. |
| 18 |  | 54.22 | 11 | Korean records count thirty-one Japanese ships lost, and none of Yi's. |
| 19 |  | 57.22 | 4 | The rest turn back. |
| 20 |  | 58.31 | 8 | Suddenly, his captains can't wait to follow him. |
| 21 | LAST | 60.49 | 18 | The king thought Yi had nothing left, but he had one line and a sea that switched sides. |

## Pace

- 240 words, 21 sentences, 65.65 s, 3.67 words/s; sentence median 11 words, longest 21.
- 'You see' at [11.2, 59.4] % of runtime; numbers ['one', 'thirteen', 'hundred', 'thirty-three', 'thirty-one', 'one']; 'you' 0.8 per 100 words.
- setup: sentences 2-4, 6.27 s, 23 words, 3.67 w/s, starts at 8.7 %.
- mechanism: sentences 13-17, 15.26 s, 56 words, 3.67 w/s, starts at 59.3 %.
- E1: sentences 5-6, 6.54 s, 24 words, 3.67 w/s, starts at 18.3 %.
- E2: sentences 7-8, 7.9 s, 29 words, 3.67 w/s, starts at 28.2 %.
- E3: sentences 9-10, 3.82 s, 14 words, 3.66 w/s, starts at 40.3 %.
- E4: sentences 11-12, 8.71 s, 32 words, 3.67 w/s, starts at 46.1 %.
