# Script judge: research/library/drafts/story-vasa-proposed.md

Spec: `research/library/STORY_SCRIPT_SPEC.md`. Timing: estimated at 3.67 words/s.
**Score: 97.8 / 100** (out of 92 checkable points; rubric items included).

## Outside the spec (biggest point losses first)

- **ridicule** = 0.0 (target 1-9; -2.0 pts). no one mocks the test: the doubter (the admiral) is overruled, not laughed at. S6 is low confidence and we don't invent jeers for real people  
  _someone mocks the odd act (S6): Jar, Storm Oil, Railroads, Mirror_

## All checks

| check | value | target | points |
|---|---|---|---|
| runtime_s | 64.01 | 55-65.5 | 5.0/5 |
| words | 234 | 200-245 | 3.0/3 |
| hook_words | 20 | 8-21 | 4.0/4 |
| hook_s | 5.45 | 2.5-5.5 | 4.0/4 |
| hook_form | declarative, concrete subject |  | 5.0/5 |
| setup_end_pct | 26.4 | 12-36 | 6.0/6 |
| esc_steps | 5 | 3-6 | 8.0/8 |
| pivot_pct | 69.4 | 55-82 | 8.0/8 |
| you_see | [69.4] |  | 3.0/3 |
| mech_words | 50 | 28-55 | 5.0/5 |
| last_line | So when thirty sailors nearly rolled her over at the dock, the Vasa was showing  |  | 5.0/5 |
| numbers | 5 | 1-5 | 4.0/4 |
| dialogue | 4 | 1-5 | 3.0/3 |
| sentence_len | {"median": 13.5, "max": 21, "share_le6": 0.11, "share_ge20": 0.11} |  | 4.0/4 |
| facts | 6.0 | 4-7 | 6.0/6 |
| jokes | 3.0 | 2-6 | 4.0/4 |
| reversal | 2.0 | 1-3 | 2.0/2 |
| ridicule | 0.0 | 1-9 | 0.0/2 |
| mechanism_visible | 1.0 | 1-1 | 4.0/4 |
| shootable_share | 1.0 | 0.9-1.0 | 4.0/4 |
| hook_act_on_screen | 1.0 | 1-1 | 3.0/3 |

## Beat map (as detected; override with --beats)

| # | beat | start s | words | sentence |
|---|---|---|---|---|
| 1 | HOOK | 0.0 | 20 | Thirty sailors ran across a brand-new warship until she nearly rolled over, and the navy sent her to sea anyway. |
| 2 | setup | 5.45 | 13 | The admiral stops the test and mutters, "If only the king were here." |
| 3 | setup | 8.99 | 14 | But the king is off at war, and he wants the mightiest warship afloat. |
| 4 | setup | 12.81 | 15 | So the Vasa gets two decks of heavy bronze cannons, stacked high above the water. |
| 5 | E1 | 16.89 | 9 | Nobody wants to tell the king his masterpiece wobbles. |
| 6 | E1 | 19.35 | 8 | His letters keep arriving: "Get her to sea." |
| 7 | E2 | 21.53 | 11 | On launch day, a huge crowd watches her sails go up. |
| 8 | E3 | 24.52 | 6 | One light gust leans her over. |
| 9 | E3 | 26.16 | 9 | She shakes it off, and the crowd keeps waving. |
| 10 | E4 | 28.61 | 17 | Then a second gust tips her further, and her open lower gun ports dip under the water. |
| 11 | E4 | 33.24 | 18 | The sea pours in, and in front of the whole city, the Vasa sinks inside her own harbour. |
| 12 | E5 | 38.15 | 11 | At the hearing, one builder's best explanation is, "Only God knows." |
| 13 | E5 | 41.14 | 3 | Nobody is punished. |
| 14 | E5 | 41.96 | 9 | The man who ordered the cannons was the king. |
| 15 | PIVOT | 44.41 | 19 | You see, a ship stays upright like a bottle with sand in the bottom: heavy low, light on top. |
| 16 | mechanism | 49.59 | 17 | The Vasa was built upside down, with tons of bronze up high and too little stone below. |
| 17 | mechanism | 54.22 | 14 | And more stone would only have pushed those gun ports down to the waterline. |
| 18 | LAST | 58.04 | 21 | So when thirty sailors nearly rolled her over at the dock, the Vasa was showing them exactly how she would sink. |

## Pace

- 234 words, 18 sentences, 64.01 s, 3.67 words/s; sentence median 13.5 words, longest 21.
- 'You see' at [69.4] % of runtime; numbers ['Thirty', 'two', 'One', 'one', 'thirty']; 'you' 0.4 per 100 words.
- setup: sentences 2-4, 11.44 s, 42 words, 3.67 w/s, starts at 8.5 %.
- mechanism: sentences 15-17, 13.63 s, 50 words, 3.67 w/s, starts at 69.4 %.
- E1: sentences 5-6, 4.64 s, 17 words, 3.66 w/s, starts at 26.4 %.
- E2: sentences 7-7, 2.99 s, 11 words, 3.68 w/s, starts at 33.6 %.
- E3: sentences 8-9, 4.09 s, 15 words, 3.67 w/s, starts at 38.3 %.
- E4: sentences 10-11, 9.54 s, 35 words, 3.67 w/s, starts at 44.7 %.
- E5: sentences 12-14, 6.26 s, 23 words, 3.67 w/s, starts at 59.6 %.
