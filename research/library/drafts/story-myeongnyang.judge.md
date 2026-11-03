# Script judge: research/library/drafts/story-myeongnyang.md

Spec: `research/library/STORY_SCRIPT_SPEC.md`. Timing: estimated at 3.9 words/s.
**Score: 98.4 / 100** (out of 92 checkable points; rubric items included).

## Outside the spec (biggest point losses first)

- **facts** = 3.0 (target 4-7; -1.5 pts). stated as true: some narrow straits' tide runs like a river and stops and reverses every few hours; that current is stronger than oars; only a few ships fit through narrows at once. Everything else is invented story (by design in this form, so the spec's 4-7 facts doesn't apply as-is)  
  _distinct real-world claims: top median 5 (2-7), >= 4 in 7/8 top vs 5/16 rest_

## All checks

| check | value | target | points |
|---|---|---|---|
| runtime_s | 63.07 | 55-65.5 | 5.0/5 |
| words | 245 | 200-245 | 3.0/3 |
| hook_words | 20 | 8-21 | 4.0/4 |
| hook_s | 5.13 | 2.5-5.5 | 4.0/4 |
| hook_form | declarative, concrete subject |  | 5.0/5 |
| setup_end_pct | 25.2 | 12-36 | 6.0/6 |
| esc_steps | 4 | 3-6 | 8.0/8 |
| pivot_pct | 57.7 | 55-82 | 8.0/8 |
| you_see | [57.7] |  | 3.0/3 |
| mech_words | 45 | 28-55 | 5.0/5 |
| last_line | And the cork drifts right back past him, going the other way. |  | 5.0/5 |
| numbers | 2 | 1-5 | 4.0/4 |
| dialogue | 4 | 1-5 | 3.0/3 |
| sentence_len | {"median": 12, "max": 20, "share_le6": 0.35, "share_ge20": 0.09} |  | 4.0/4 |
| facts | 3.0 | 4-7 | 4.5/6 |
| jokes | 6.0 | 2-6 | 4.0/4 |
| reversal | 2.0 | 1-3 | 2.0/2 |
| ridicule | 3.0 | 1-9 | 2.0/2 |
| mechanism_visible | 1.0 | 1-1 | 4.0/4 |
| shootable_share | 1.0 | 0.9-1.0 | 4.0/4 |
| hook_act_on_screen | 1.0 | 1-1 | 3.0/3 |

## Beat map (as detected; override with --beats)

| # | beat | start s | words | sentence |
|---|---|---|---|---|
| 1 | HOOK | 0.0 | 20 | He anchored his last ships in a roaring strait, with an enemy fleet so close he could hear them laughing. |
| 2 | setup | 5.13 | 5 | His captain grabs his collar. |
| 3 | setup | 6.41 | 12 | "They've got ten ships for every one of ours, and you're parking?" |
| 4 | setup | 9.49 | 4 | He doesn't look up. |
| 5 | setup | 10.51 | 12 | He just drops a cork over the side and watches it drift. |
| 6 | setup | 13.59 | 6 | "Wait for the water," he says. |
| 7 | setup | 15.13 | 3 | "Watch the cork." |
| 8 | E1 | 15.9 | 15 | Then the enemy charges into the strait, the current carrying them in like a river. |
| 9 | E1 | 19.74 | 4 | Their admiral is thrilled. |
| 10 | E1 | 20.77 | 7 | The sea is doing all the rowing. |
| 11 | E2 | 22.56 | 14 | His own captains anchor well behind him, politely letting him face the enemy first. |
| 12 | E3 | 26.15 | 19 | But the strait is so narrow only a few ships fit at once, and his cannons keep those busy. |
| 13 | E4 | 31.03 | 6 | Meanwhile, the cork is slowing down. |
| 14 | E4 | 32.56 | 15 | Then it stops dead, just as the enemy flagship pulls close enough to spit on. |
| 15 | PIVOT | 36.41 | 8 | You see, some narrow straits really do this. |
| 16 | mechanism | 38.46 | 16 | The tide runs through like a river, and every few hours it stops and turns around. |
| 17 | mechanism | 42.56 | 15 | Now the water that rushed them in shoves them back, harder than they can row. |
| 18 | mechanism | 46.41 | 4 | His ships are anchored. |
| 19 | mechanism | 47.44 | 2 | Theirs aren't. |
| 20 |  | 47.95 | 14 | Their front ships pile into the ones behind, and his cannons pound the jam. |
| 21 |  | 51.54 | 20 | By sunset, the whole enemy fleet is drifting backwards out of the strait, their admiral close enough to wave goodbye. |
| 22 |  | 56.67 | 12 | His captain, who called it parking, now says it was his idea. |
| 23 | LAST | 59.74 | 12 | And the cork drifts right back past him, going the other way. |

## Pace

- 245 words, 23 sentences, 63.07 s, 3.9 words/s; sentence median 12 words, longest 20.
- 'You see' at [57.7] % of runtime; numbers ['ten', 'one']; 'you' 0.8 per 100 words.
- setup: sentences 2-7, 10.77 s, 42 words, 3.9 w/s, starts at 8.1 %.
- mechanism: sentences 15-19, 11.54 s, 45 words, 3.9 w/s, starts at 57.7 %.
- E1: sentences 8-10, 6.66 s, 26 words, 3.9 w/s, starts at 25.2 %.
- E2: sentences 11-11, 3.59 s, 14 words, 3.9 w/s, starts at 35.8 %.
- E3: sentences 12-12, 4.88 s, 19 words, 3.89 w/s, starts at 41.5 %.
- E4: sentences 13-14, 5.38 s, 21 words, 3.9 w/s, starts at 49.2 %.
