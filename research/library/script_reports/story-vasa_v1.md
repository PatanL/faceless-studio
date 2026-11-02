# Script judge: episodes/story-vasa/script.md

Spec: `research/library/STORY_SCRIPT_SPEC.md`. Timing: measured (word coverage 0.922).
**Score: 80.1 / 100** (out of 104 checkable points; rubric items included).

## Outside the spec (biggest point losses first)

- **last_line** = It sits in Stockholm today, never sailing again. (target see why; -4.0 pts). 8 words (11-24); 1.0 s of video after the last word  
  _last line 11-24 words (top median 16.5), not a question (0/8 top), the video ends <= 0.5 s after it_
- **numbers** = 15 (target 1-5; -4.0 pts). Thirty, 1628, seventy-two, two, four, thirteen, hundred, thirty, one, one, two, 120, twice, thirty, 1961  
  _number tokens: top 1-5 (median 3), rest median 5.5 (up to 15)_
- **jokes** = 0.0 (target 2-6; -4.0 pts). no line is written for a laugh; 'Only God knows, one builder says' and 'The admiral wishes the king were home' are wry at most  
  _jokes: top median 2 (1-4), >= 2 in 6/8 top vs 6/16 rest_
- **facts** = 10.0 (target 4-7; -2.6 pts). counted at the grain used for the references: the 30-man test stopped after three runs; the king at war orders 72 guns; two gun decks + carvings; the launch crowd and sails; gust/rights/second gust/ports under, sinks 1,300 m out, ~30 dead; the inquiry blames no one ('Only God knows'); the weighted-toy principle; bronze guns over 120 t of stone; twice the ballast would sink the ports; raised 1961, in Stockholm today. Top-8 maximum is 7: it reads as a fact list  
  _distinct real-world claims: top median 5 (2-7), >= 4 in 7/8 top vs 5/16 rest_
- **ridicule** = 0.0 (target 1-9; -2.0 pts). nobody mocks the test or the admiral on the page; the king's letters overrule him but no one laughs or jeers  
  _someone mocks the odd act (S6): Jar, Storm Oil, Railroads, Mirror_
- **hook_words** = 24 (target 8-21; -1.3 pts).   
  _hook (sentence 1, or 1-2 when 2 completes the paradox): top 9-21 words, median 14_
- **wps** = 4.0 (target 3.4-3.9; -1.2 pts).   
  _all 24: 3.36-4.09 words/s, top median 3.67_
- **pauses_ge400** = 2 (target 0-1; -0.8 pts). 0 >= 0.8 s, 7.72 s total  
  _8 audio refs: 0-1 gaps >= 0.4 s, none >= 0.8 s_
- **hook_s** = 5.94 (target 2.5-5.5; -0.7 pts).   
  _hook spoken in 3.0-5.4 s (top 8)_
- **mech_words** = 56 (target 28-55; -0.1 pts). 12.86 s, 0.24 of the words  
  _mechanism: top 32-49 words, 9-15 s, 15-32 % of the words_

## All checks

| check | value | target | points |
|---|---|---|---|
| runtime_s | 59.0 | 55-65.5 | 5.0/5 |
| words | 231 | 200-245 | 3.0/3 |
| wps | 4.0 | 3.4-3.9 | 3.75/5 |
| pauses_per_10s | 5.03 | 2.3-5.5 | 2.0/2 |
| pauses_ge400 | 2 | 0-1 | 2.25/3 |
| mech_slower | 0.06 | -1.0-0.1 | 2.0/2 |
| hook_words | 24 | 8-21 | 2.67/4 |
| hook_s | 5.94 | 2.5-5.5 | 3.3/4 |
| hook_form | declarative, concrete subject |  | 5.0/5 |
| setup_end_pct | 27.2 | 12-36 | 6.0/6 |
| esc_steps | 4 | 3-6 | 8.0/8 |
| pivot_pct | 62.3 | 55-82 | 8.0/8 |
| you_see | [62.3] |  | 3.0/3 |
| mech_words | 56 | 28-55 | 4.86/5 |
| last_line | It sits in Stockholm today, never sailing again. |  | 1.0/5 |
| numbers | 15 | 1-5 | 0.0/4 |
| dialogue | 2 | 1-5 | 3.0/3 |
| sentence_len | {"median": 10, "max": 19, "share_le6": 0.35, "share_ge20": 0.0} |  | 4.0/4 |
| facts | 10.0 | 4-7 | 3.43/6 |
| jokes | 0.0 | 2-6 | 0.0/4 |
| reversal | 1.0 | 1-3 | 2.0/2 |
| ridicule | 0.0 | 1-9 | 0.0/2 |
| mechanism_visible | 1.0 | 1-1 | 4.0/4 |
| shootable_share | 0.96 | 0.9-1.0 | 4.0/4 |
| hook_act_on_screen | 1.0 | 1-1 | 3.0/3 |

## Beat map (as detected; override with --beats)

| # | beat | start s | words | sentence |
|---|---|---|---|---|
| 1 | HOOK | 0.32 | 10 | Thirty sailors ran back and forth across a brand-new warship. |
| 2 | HOOK | 3.2 | 14 | After the third run, the admiral stopped the test, and the ship sailed anyway. |
| 3 | setup | 6.26 | 4 | It's 1628 in Stockholm. |
| 4 | setup | 7.8 | 15 | The king, away at war, orders seventy-two heavy cannons for his new warship, the Vasa. |
| 5 | setup | 12.42 | 16 | So it gets two decks of guns, stacked high above the water, and hundreds of carvings. |
| 6 | E1 | 16.02 | 6 | But every run rocks it harder. |
| 7 | E1 | 17.56 | 7 | The admiral wishes the king were home. |
| 8 | E1 | 19.2 | 8 | The king's letters say: get her to sea. |
| 9 | E2 | 20.9 | 11 | On August tenth, a huge crowd watches four sails go up. |
| 10 | E2 | 23.6 | 6 | A gust tips the Vasa over. |
| 11 | E2 | 24.96 | 3 | It rights itself. |
| 12 | E3 | 25.68 | 12 | Then a second gust pushes the lower gun ports under the water. |
| 13 | E3 | 28.34 | 16 | The gun deck floods, and thirteen hundred meters out, in front of everyone, the Vasa sinks. |
| 14 | E3 | 32.7 | 4 | About thirty people die. |
| 15 | E4 | 33.78 | 5 | The inquiry punishes no one. |
| 16 | E4 | 35.16 | 6 | Only God knows, one builder says. |
| 17 | PIVOT | 36.76 | 18 | You see, a ship stays upright like a weighted toy: heavy at the bottom, light at the top. |
| 18 | mechanism | 40.42 | 5 | The Vasa was the opposite. |
| 19 | mechanism | 41.8 | 14 | Its bronze cannons sat high on two decks, over just 120 tons of stone. |
| 20 | mechanism | 45.66 | 19 | It needed about twice as much, but more weight would push the lower gun ports down to the waterline. |
| 21 |  | 49.72 | 14 | So when thirty men ran across the deck, the ship was already warning them. |
| 22 |  | 52.96 | 10 | In 1961, they raised it from the mud, almost whole. |
| 23 | LAST | 55.88 | 8 | It sits in Stockholm today, never sailing again. |

## Pace

- 231 words, 23 sentences, 59.0 s, 4.0 words/s; sentence median 10 words, longest 19.
- 'You see' at [62.3] % of runtime; numbers ['Thirty', '1628', 'seventy-two', 'two', 'four', 'thirteen', 'hundred', 'thirty', 'one', 'one', 'two', '120', 'twice', 'thirty', '1961']; 'you' 0.4 per 100 words.
- Pauses >= 150 ms: 29 (5.03 per 10 s, 7.72 s total); >= 0.4 s: 2; >= 0.8 s: 0. Longest: 0.42 s after 'sinks.' at 32.28 s, 0.4 s after '1961,' at 53.58 s, 0.36 s after 'floods,' at 29.3 s, 0.34 s after 'war,' at 9.12 s, 0.34 s after 'harder.' at 17.22 s, 0.34 s after 'opposite.' at 41.46 s
- setup: sentences 3-5, 9.32 s, 35 words, 3.76 w/s, starts at 10.6 %.
- mechanism: sentences 17-20, 12.86 s, 56 words, 4.35 w/s, starts at 62.3 %.
- E1: sentences 6-8, 4.72 s, 21 words, 4.45 w/s, starts at 27.2 %.
- E2: sentences 9-11, 4.78 s, 20 words, 4.18 w/s, starts at 35.4 %.
- E3: sentences 12-14, 7.94 s, 32 words, 4.03 w/s, starts at 43.5 %.
- E4: sentences 15-16, 2.8 s, 11 words, 3.93 w/s, starts at 57.3 %.
