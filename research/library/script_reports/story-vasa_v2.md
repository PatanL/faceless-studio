# Script judge: episodes/story-vasa/script.md

Spec: `research/library/STORY_SCRIPT_SPEC.md`. Timing: measured (word coverage 0.926).
**Score: 80.8 / 100** (out of 104 checkable points; rubric items included).

## Outside the spec (biggest point losses first)

- **last_line** = It sits in Stockholm today, never sailing again. (target see why; -4.0 pts). 8 words (11-24); 1.06 s of video after the last word  
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
- **hook_s** = 6.24 (target 2.5-5.5; -1.2 pts).   
  _hook spoken in 3.0-5.4 s (top 8)_
- **pauses_ge400** = 2 (target 0-1; -0.8 pts). 0 >= 0.8 s, 7.28 s total  
  _8 audio refs: 0-1 gaps >= 0.4 s, none >= 0.8 s_
- **mech_words** = 56 (target 28-55; -0.1 pts). 13.96 s, 0.24 of the words  
  _mechanism: top 32-49 words, 9-15 s, 15-32 % of the words_

## All checks

| check | value | target | points |
|---|---|---|---|
| runtime_s | 63.42 | 55-65.5 | 5.0/5 |
| words | 231 | 200-245 | 3.0/3 |
| wps | 3.72 | 3.4-3.9 | 5.0/5 |
| pauses_per_10s | 4.19 | 2.3-5.5 | 2.0/2 |
| pauses_ge400 | 2 | 0-1 | 2.25/3 |
| mech_slower | 0.08 | -1.0-0.1 | 2.0/2 |
| hook_words | 24 | 8-21 | 2.67/4 |
| hook_s | 6.24 | 2.5-5.5 | 2.82/4 |
| hook_form | declarative, concrete subject |  | 5.0/5 |
| setup_end_pct | 26.7 | 12-36 | 6.0/6 |
| esc_steps | 4 | 3-6 | 8.0/8 |
| pivot_pct | 62.1 | 55-82 | 8.0/8 |
| you_see | [62.1] |  | 3.0/3 |
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
| 2 | HOOK | 3.26 | 14 | After the third run, the admiral stopped the test, and the ship sailed anyway. |
| 3 | setup | 6.56 | 4 | It's 1628 in Stockholm. |
| 4 | setup | 8.14 | 15 | The king, away at war, orders seventy-two heavy cannons for his new warship, the Vasa. |
| 5 | setup | 12.76 | 16 | So it gets two decks of guns, stacked high above the water, and hundreds of carvings. |
| 6 | E1 | 16.94 | 6 | But every run rocks it harder. |
| 7 | E1 | 18.62 | 7 | The admiral wishes the king were home. |
| 8 | E1 | 20.34 | 8 | The king's letters say: get her to sea. |
| 9 | E2 | 22.08 | 11 | On August tenth, a huge crowd watches four sails go up. |
| 10 | E2 | 25.06 | 6 | A gust tips the Vasa over. |
| 11 | E2 | 26.24 | 3 | It rights itself. |
| 12 | E3 | 27.32 | 12 | Then a second gust pushes the lower gun ports under the water. |
| 13 | E3 | 30.22 | 16 | The gun deck floods, and thirteen hundred meters out, in front of everyone, the Vasa sinks. |
| 14 | E3 | 34.8 | 4 | About thirty people die. |
| 15 | E4 | 36.02 | 5 | The inquiry punishes no one. |
| 16 | E4 | 37.54 | 6 | Only God knows, one builder says. |
| 17 | PIVOT | 39.36 | 18 | You see, a ship stays upright like a weighted toy: heavy at the bottom, light at the top. |
| 18 | mechanism | 43.3 | 5 | The Vasa was the opposite. |
| 19 | mechanism | 44.7 | 14 | Its bronze cannons sat high on two decks, over just 120 tons of stone. |
| 20 | mechanism | 48.84 | 19 | It needed about twice as much, but more weight would push the lower gun ports down to the waterline. |
| 21 |  | 53.4 | 14 | So when thirty men ran across the deck, the ship was already warning them. |
| 22 |  | 56.78 | 10 | In 1961, they raised it from the mud, almost whole. |
| 23 | LAST | 60.14 | 8 | It sits in Stockholm today, never sailing again. |

## Pace

- 231 words, 23 sentences, 63.42 s, 3.72 words/s; sentence median 10 words, longest 19.
- 'You see' at [62.1] % of runtime; numbers ['Thirty', '1628', 'seventy-two', 'two', 'four', 'thirteen', 'hundred', 'thirty', 'one', 'one', 'two', '120', 'twice', 'thirty', '1961']; 'you' 0.4 per 100 words.
- Pauses >= 150 ms: 26 (4.19 per 10 s, 7.28 s total); >= 0.4 s: 2; >= 0.8 s: 0. Longest: 0.5 s after '1961,' at 57.54 s, 0.44 s after 'sinks.' at 34.36 s, 0.38 s after 'today,' at 61.28 s, 0.36 s after 'floods,' at 31.18 s, 0.36 s after 'decks,' at 46.64 s, 0.36 s after 'deck,' at 55.1 s
- setup: sentences 3-5, 9.94 s, 35 words, 3.52 w/s, starts at 10.3 %.
- mechanism: sentences 17-20, 13.96 s, 56 words, 4.01 w/s, starts at 62.1 %.
- E1: sentences 6-8, 5.0 s, 21 words, 4.2 w/s, starts at 26.7 %.
- E2: sentences 9-11, 5.24 s, 20 words, 3.82 w/s, starts at 34.8 %.
- E3: sentences 12-14, 8.54 s, 32 words, 3.75 w/s, starts at 43.1 %.
- E4: sentences 15-16, 3.14 s, 11 words, 3.5 w/s, starts at 56.8 %.
