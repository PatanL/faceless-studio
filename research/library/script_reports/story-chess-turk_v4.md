# Script judge: research/library/script_reports/story-chess-turk_v4.narration.md

Spec: `research/library/STORY_SCRIPT_SPEC.md`. Timing: measured (word coverage 0.986).
**Score: 83.4 / 100** (out of 104 checkable points; rubric items included).

## Outside the spec (biggest point losses first)

- **wps** = 3.11 (target 3.4-3.9; -3.6 pts).   
  _all 24: 3.36-4.09 words/s, top median 3.67_
- **pauses_ge400** = 6 (target 0-1; -3.0 pts). 0 >= 0.8 s, 9.42 s total  
  _8 audio refs: 0-1 gaps >= 0.4 s, none >= 0.8 s_
- **dialogue** = 0 (target 1-5; -3.0 pts). sentences []  
  _character lines: top median 2 (0-5), >= 2 in 5/8 top vs 5/16 rest_
- **jokes** = 1.0 (target 2-6; -2.0 pts). only the deadpan 'Twice.'; 'The whole court laughs' and 'Nobody's laughing now' report laughter, they don't make any  
  _jokes: top median 2 (1-4), >= 2 in 6/8 top vs 6/16 rest_
- **hook_s** = 6.62 (target 2.5-5.5; -1.8 pts).   
  _hook spoken in 3.0-5.4 s (top 8)_
- **facts** = 9.0 (target 4-7; -1.7 pts). Vienna palace 1770; turbaned wooden figure; doors opened with a candle to show gears; toured ~80 years; beat Franklin; Napoleon's illegal moves and the swept board; 1854 fire; hidden master on a sliding seat; magnets under the board + lever to the hand  
  _distinct real-world claims: top median 5 (2-7), >= 4 in 7/8 top vs 5/16 rest_
- **numbers** = 6 (target 1-5; -0.8 pts). 1770, one, one, eighty, Twice, 1854  
  _number tokens: top 1-5 (median 3), rest median 5.5 (up to 15)_
- **runtime_s** = 66.77 (target 55-65.5; -0.7 pts).   
  _top 8: 39-65 s, median 62; the two shortest refs (31, 35 s) are the two lowest_
- **hook_words** = 22 (target 8-21; -0.4 pts).   
  _hook (sentence 1, or 1-2 when 2 completes the paradox): top 9-21 words, median 14_
- **mech_slower** = 0.16 (target -1.0-0.1; -0.2 pts). mechanism 3.29 w/s, last line 3.24 w/s vs 3.11 overall  
  _top 8 slow down after the pivot (mechanism 3.58, last line 3.51 vs 3.67 overall); the rest speed up (3.84 / 4.17)_

## All checks

| check | value | target | points |
|---|---|---|---|
| runtime_s | 66.77 | 55-65.5 | 4.33/5 |
| words | 207 | 200-245 | 3.0/3 |
| wps | 3.11 | 3.4-3.9 | 1.37/5 |
| pauses_per_10s | 4.81 | 2.3-5.5 | 2.0/2 |
| pauses_ge400 | 6 | 0-1 | 0.0/3 |
| mech_slower | 0.16 | -1.0-0.1 | 1.76/2 |
| hook_words | 22 | 8-21 | 3.56/4 |
| hook_s | 6.62 | 2.5-5.5 | 2.21/4 |
| hook_form | declarative, concrete subject |  | 5.0/5 |
| setup_end_pct | 29.3 | 12-36 | 6.0/6 |
| esc_steps | 5 | 3-6 | 8.0/8 |
| pivot_pct | 73.6 | 55-82 | 8.0/8 |
| you_see | [9.9] |  | 3.0/3 |
| mech_words | 42 | 28-55 | 5.0/5 |
| last_line | The robot that beat Napoleon was a man in a box, playing by candlelight. |  | 5.0/5 |
| numbers | 6 | 1-5 | 3.2/4 |
| dialogue | 0 | 1-5 | 0.0/3 |
| sentence_len | {"median": 10.5, "max": 22, "share_le6": 0.3, "share_ge20": 0.05} |  | 4.0/4 |
| facts | 9.0 | 4-7 | 4.29/6 |
| jokes | 1.0 | 2-6 | 2.0/4 |
| reversal | 2.0 | 1-3 | 2.0/2 |
| ridicule | 1.0 | 1-9 | 2.0/2 |
| mechanism_visible | 1.0 | 1-1 | 4.0/4 |
| shootable_share | 1.0 | 0.9-1.0 | 4.0/4 |
| hook_act_on_screen | 1.0 | 1-1 | 3.0/3 |

## Beat map (as detected; override with --beats)

| # | beat | start s | words | sentence |
|---|---|---|---|---|
| 1 | HOOK | 0.0 | 22 | He built a chess robot that could beat anyone, and before every game, he opened it up to prove it was empty. |
| 2 | setup | 6.62 | 19 | You see, it's 1770, and an inventor has just rolled a wooden cabinet into the Empress's palace in Vienna. |
| 3 | setup | 13.82 | 14 | On top sits a life-size wooden man in a turban, staring at a chessboard. |
| 4 | setup | 18.24 | 4 | The whole court laughs. |
| 5 | E1 | 19.56 | 14 | So he opens the doors one by one and holds a candle behind them. |
| 6 | E1 | 24.0 | 3 | Nothing but gears. |
| 7 | E2 | 25.3 | 13 | He winds a key, the gears tick, and the Turk lifts its arm. |
| 8 | E2 | 28.6 | 9 | The first count brave enough to play it loses. |
| 9 | E2 | 31.38 | 3 | Nobody's laughing now. |
| 10 | E3 | 32.68 | 8 | For eighty years the Turk tours the world. |
| 11 | E3 | 34.7 | 4 | It beats Benjamin Franklin. |
| 12 | E4 | 36.46 | 11 | And when Napoleon tries to cheat, it puts his piece back. |
| 13 | E4 | 39.8 | 1 | Twice. |
| 14 | E4 | 40.64 | 10 | The third time, it sweeps every piece off the board. |
| 15 | E5 | 43.44 | 16 | Then in 1854, a fire burns the Turk to ash, and its secret finally comes out. |
| 16 | PIVOT | 49.14 | 5 | There was a man inside. |
| 17 | mechanism | 50.58 | 7 | A chess master, folded into the cabinet. |
| 18 | mechanism | 53.06 | 15 | When each door opened, he slid his seat to the other side, behind fake gears. |
| 19 | mechanism | 57.8 | 15 | Magnets under the board showed him every move, and a lever moved the Turk's hand. |
| 20 | LAST | 62.16 | 14 | The robot that beat Napoleon was a man in a box, playing by candlelight. |

## Pace

- 207 words, 20 sentences, 66.77 s, 3.11 words/s; sentence median 10.5 words, longest 22.
- 'You see' at [9.9] % of runtime; numbers ['1770', 'one', 'one', 'eighty', 'Twice', '1854']; 'you' 0.5 per 100 words.
- Pauses >= 150 ms: 32 (4.81 per 10 s, 9.42 s total); >= 0.4 s: 6; >= 0.8 s: 0. Longest: 0.52 s after 'Twice.' at 40.12 s, 0.48 s after 'loses.' at 30.9 s, 0.46 s after '1854,' at 44.64 s, 0.44 s after 'gears.' at 57.36 s, 0.4 s after 'anyone,' at 2.56 s, 0.4 s after 'gears.' at 24.9 s
- setup: sentences 2-4, 12.64 s, 37 words, 2.93 w/s, starts at 9.9 %.
- mechanism: sentences 16-19, 12.78 s, 42 words, 3.29 w/s, starts at 73.6 %.
- E1: sentences 5-6, 5.34 s, 17 words, 3.18 w/s, starts at 29.3 %.
- E2: sentences 7-9, 7.16 s, 25 words, 3.49 w/s, starts at 37.9 %.
- E3: sentences 10-11, 3.5 s, 12 words, 3.43 w/s, starts at 48.9 %.
- E4: sentences 12-14, 6.76 s, 22 words, 3.25 w/s, starts at 54.6 %.
- E5: sentences 15-15, 5.54 s, 16 words, 2.89 w/s, starts at 65.1 %.
