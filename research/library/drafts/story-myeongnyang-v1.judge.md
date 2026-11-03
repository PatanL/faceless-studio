# Script judge: research/library/drafts/story-myeongnyang.md

Spec: `research/library/STORY_SCRIPT_SPEC.md`. Timing: estimated at 3.67 words/s.
**Score: 98.7 / 100** (out of 92 checkable points; rubric items included).

## Outside the spec (biggest point losses first)

- **sentence_len** = {"median": 14.0, "max": 19, "share_le6": 0.06, "share_ge20": 0.0} (target see why; -1.2 pts). short lines 0.06  
  _sentence median 10-15 words (top 12.5), longest <= 30, short punch lines (<= 6 words) in 10-35 %_

## All checks

| check | value | target | points |
|---|---|---|---|
| runtime_s | 58.83 | 55-65.5 | 5.0/5 |
| words | 215 | 200-245 | 3.0/3 |
| hook_words | 19 | 8-21 | 4.0/4 |
| hook_s | 5.18 | 2.5-5.5 | 4.0/4 |
| hook_form | declarative, concrete subject |  | 5.0/5 |
| setup_end_pct | 28.7 | 12-36 | 6.0/6 |
| esc_steps | 4 | 3-6 | 8.0/8 |
| pivot_pct | 61.1 | 55-82 | 8.0/8 |
| you_see | [61.1] |  | 3.0/3 |
| mech_words | 53 | 28-55 | 5.0/5 |
| last_line | The king thought Yi had no navy left, but he had a sea that changes sides. |  | 5.0/5 |
| numbers | 5 | 1-5 | 4.0/4 |
| dialogue | 1 | 1-5 | 3.0/3 |
| sentence_len | {"median": 14.0, "max": 19, "share_le6": 0.06, "share_ge20": 0.0} |  | 2.8/4 |
| facts | 6.0 | 4-7 | 6.0/6 |
| jokes | 2.0 | 2-6 | 4.0/4 |
| reversal | 2.0 | 1-3 | 2.0/2 |
| ridicule | 1.0 | 1-9 | 2.0/2 |
| mechanism_visible | 1.0 | 1-1 | 4.0/4 |
| shootable_share | 1.0 | 0.9-1.0 | 4.0/4 |
| hook_act_on_screen | 1.0 | 1-1 | 3.0/3 |

## Beat map (as detected; override with --beats)

| # | beat | start s | words | sentence |
|---|---|---|---|---|
| 1 | HOOK | 0.0 | 19 | Ordered to give up the navy, Admiral Yi took his last thirteen ships to fight a hundred and thirty-three. |
| 2 | setup | 5.18 | 10 | Even his own captains think he has lost his mind. |
| 3 | setup | 7.9 | 14 | Korea's fleet has just been burned to the waterline by a Japanese invasion fleet. |
| 4 | setup | 11.72 | 12 | So the king tells Yi to come ashore and fight on land. |
| 5 | setup | 14.99 | 7 | Yi writes back, "I still have ships." |
| 6 | E1 | 16.89 | 14 | Then he anchors them at the mouth of the narrowest, loudest strait in Korea. |
| 7 | E1 | 20.71 | 13 | The locals call it the crying strait, for the roar of its water. |
| 8 | E2 | 24.25 | 19 | The Japanese fleet pours in with the current behind it, ship after ship, faster than any oar could row. |
| 9 | E3 | 29.43 | 11 | His captains hang back and politely let the admiral go first. |
| 10 | E3 | 32.43 | 9 | For hours, his flagship holds the front almost alone. |
| 11 | E4 | 34.88 | 4 | Then the roaring stops. |
| 12 | PIVOT | 35.97 | 19 | You see, the water in that strait runs like a river, and it turns around four times a day. |
| 13 | mechanism | 41.14 | 18 | The Japanese had ridden the current into a gap so narrow only a few ships could reach him. |
| 14 | mechanism | 46.05 | 16 | When the tide turned, historians reckon, that same current shoved their ships backwards into each other. |
| 15 |  | 50.41 | 14 | Korean records count ship after ship lost that day, and not one of his. |
| 16 | LAST | 54.22 | 16 | The king thought Yi had no navy left, but he had a sea that changes sides. |

## Pace

- 215 words, 16 sentences, 58.83 s, 3.67 words/s; sentence median 14.0 words, longest 19.
- 'You see' at [61.1] % of runtime; numbers ['thirteen', 'hundred', 'thirty-three', 'four', 'one']; 'you' 0.5 per 100 words.
- setup: sentences 2-5, 11.71 s, 43 words, 3.67 w/s, starts at 8.8 %.
- mechanism: sentences 12-14, 14.44 s, 53 words, 3.67 w/s, starts at 61.1 %.
- E1: sentences 6-7, 7.36 s, 27 words, 3.67 w/s, starts at 28.7 %.
- E2: sentences 8-8, 5.18 s, 19 words, 3.67 w/s, starts at 41.2 %.
- E3: sentences 9-10, 5.45 s, 20 words, 3.67 w/s, starts at 50.0 %.
- E4: sentences 11-11, 1.09 s, 4 words, 3.67 w/s, starts at 59.3 %.
