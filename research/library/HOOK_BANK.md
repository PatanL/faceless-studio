# Hook bank (story lane): what the top openings do, measured

Built 2026-11-02 for the owner's priority: hooks, and scripts that make sense. Internal research. Reference lines
appear only as short paraphrased fragments; every full example line here is ours.

**Data**
- RicksClips3000: the 24 story Shorts, tiers top/mid/bottom 8 by views. Word timings in
  `research/references/data/ricks24_beats.json`; frames at 0, 1, 2, 3 s and each sentence midpoint (240p sheets).
- Zack D. Films, two sets: (a) the 16 hypothetical Shorts in LANE_PRINCIPLES.md (top 8 vs ordinary 8), with captions
  and 0-3 s strips copied from `dgx-spark:~/studio/refs/lanes/zackd/` (no new fetch); (b) the 10 annotated Shorts in
  `research/corpus/zackd/` (7 outliers vs 3 controls; hook analysis in its PLAYBOOK.md).
- "Lands" = the time the hook's twist or question is complete (the stinger word), from the word timings.

## 1. Measured: top vs ordinary

| Feature | Ricks top 8 | Ricks mid 8 | Ricks bottom 8 | Zack what-if top 8 | Zack what-if ordinary 8 | Lever? |
|---|---|---|---|---|---|---|
| **Frame 0: one character mid-act, close, with the key prop** (S-hook) | **5/8** | 2/8 | 2/8 | 4/8 | 5/8 | **Ricks: yes** (5/8 vs 4/16) |
| ...and the first line names that act | 5/5 | 2/2 | 2/2 | - | - | where frame 0 is the act, always |
| The impossible change is on screen by 3 s | - | - | - | **7/8** | 1/8 | **Zack: yes** |
| Line and image say the same thing in 0-3 s | 8/8 | 7/8 | 8/8 | 7/8 | 8/8 | floor |
| Words until the hook lands | 13.5 (9-20) | 18.5 (12-24) | 11.5 (8-15) | 22.5 (15-34) | 21 (11-35) | no split; Ricks lands faster than Zack |
| Seconds until it lands | 3.6 (2.6-4.8) | 4.9 (3.0-6.2) | 2.9 (1.8-4.1) | 8.6 (6.2-11.0) | 7.1 (3.9-11.8) | top Ricks: always <= 4.8 s |
| Opens a question only the video closes | 8/8 | 8/8 | 7/8 | 8/8 | 6/8 (one answers itself in line 1, one has no claim) | floor; missing it is fatal |
| A person and an object in line 1 | 6/8 | 7/8 | 6/8 | 7/8 | 6/8 | floor |
| A number in line 1 | 2/8 | 5/8 | 1/8 | 2/8 | 0/8 | no; top Ricks use few |
| "You"/your body in line 1 | 2/8 | 2/8 | 3/8 | 7/8 | 6/8 | no (S7, W4) |
| "You might think / most people assume" opener | 0/8 | 0/8 | 0/8 | **0/8** | **3/8** | avoid |
| Direct question in line 1 | 0/8 | 0/8 | 1/8 (the #23 video) | 2/8 (a challenge to you) | 3/8 (about an object) | avoid, unless it dares the viewer |
| Opens on a date, place card or "imagine" | 0/8 | 0/8 | 0/8 | 1/8 | 0/8 | avoid |

Zack D. corpus (b): frame 0 shows the most unusual thing available in 10/10. The hook states the action already in
progress in 7/7 outliers. Hedges: 0/7 outliers, 1/3 controls. The weakest control gives its reframe away at 14 %.

**What the numbers say**
1. **The picture hooks first, the line names it.** Ricks: in the top tier, frame 0 is one person in the middle of the
   strange act, close, holding the prop that matters. The line says that act, and the wider context (court, army,
   fleet) arrives at 2-4 s. Zack: the impossible change itself is on screen by 3 s.
2. **Land it by about 4.5 s.** No top Ricks hook needs more than 4.8 s or 20 words. The middle tier's slower hooks
   (up to 6.2 s) are where the long ones live.
3. **One open question the viewer can say in their own words** ("why would a ball falling mean run?"). Nothing in
   line 1 answers it.
4. **What hurts:** debunk openers, questions about objects, date or place openers, hedges, and two numbers in a
   row (Barca's context opener scored 0/8 on the hook panel in four rounds; Myeongnyang v1's two-number hook ranked
   14 of 19 in the blind test below).

## 2. Patterns (counts are line-1 forms; the frame column says what frame 0 shows)

| # | Pattern | Ricks top / mid / bottom | Zack top / ord | Frame 0 |
|---|---|---|---|---|
| H1 | **Odd act, one person, past tense**: "[He/They] [did a strange concrete thing] [with a named object]" | 4 / 4 / 3 | - | the act, close |
| H2 | **Odd act + the warning or threat it implies** (a subset of H1): the act, then an order or danger that makes it urgent | 2 / 0 / 0 | - | the act, then the threat at 2-3 s |
| H3 | **Rule vs reality**: "[X] is forbidden or impossible, yet [X is everywhere / something worse happens]" | 2 / 1 / 0 | - | the thing that shouldn't exist |
| H4 | **Counterintuitive outcome**: "If you [do X], you'd [the opposite of what you expect]" | 2 / 0 / 1 | 5 / 0 (commit to the premise, one concrete consequence) | the outcome on the body or object |
| H5 | **Debunk setup** ("you might think...") | 0 / 0 / 0 | 0 / 3 | - (avoid) |
| H6 | **Question** | 0 / 0 / 1 | 2 / 3 | - (avoid) |

H1 and H2 are the same family: the top tier's H1 lines usually carry a second half that sharpens the question.

**Paraphrased fragments (references) and our own lines**

- **H1 Odd act.** Refs: someone buried with a bell tied to a finger; a cook tipping oil over the side; an engineer
  cutting gaps into new track.
  - Ours: "A shogun paid his carpenters to build a floor that squeaks."
  - Ours: "Every morning the smith pressed his ear to a shield lying in the dirt."
  - Ours: "Told to give up the navy, Admiral Yi wrote back four words and sailed thirteen ships at a hundred and thirty-three." (won the blind test below)
- **H2 Odd act + warning.** Refs: a ball set in a dragon's mouth, with "if it falls, run"; oil poured out while the
  pirates close in.
  - Ours: "He tied a bell to the city gate and told the guards that if it ever rang on a still night, they should flee."
  - Ours: "She buried her best silver in the garden and told her son never to dig there, whatever happened."
- **H3 Rule vs reality.** Refs: a country where gambling is banned but there's a hall on every street; a country where
  firing is near impossible, so bosses found something worse.
  - Ours: "Building dams on the river was forbidden, yet one governor tamed it with baskets of stones."
  - Ours: "Ships were banned from the harbour at night, and every night one sailed in anyway."
- **H4 Counterintuitive outcome.** Refs: being hit by a plain cannonball as the lucky case; your hair weighing as much
  as a bowling ball if it could move.
  - Ours: "If your ship got hit at Myeongnyang, the water was the thing to fear, not the cannon."
  - Ours: "If you flooded your own country on purpose, you might just save it."

## 3. Hook rubric (score before the blind test; 10 points)

| Points | Check |
|---|---|
| 3 | **Frame 0 is the act**: one character in the middle of the strange act, close, with the key prop, and line 1 names that act. Context comes at 2-4 s. |
| 2 | **Lands by <= 4.5 s and <= 21 words** (one sentence, or two short ones where the second completes the paradox). |
| 2 | **One open question** a viewer could say back ("why would he...?"), not answered in line 1. |
| 1 | **Concrete**: a person and an object; at most one number pair. |
| 1 | **No banned openers**: no question about an object, no "you might think", no date or place card, no "imagine", no hedge. |
| 1 | **Line = image** for the first 3 s (say nothing the frame can't show). |

Then the **blind test**: 10+ variants plus 6 real top hooks (as text, shuffled differently for each of 3 fresh
judges, "would you keep watching past 3 s?"). Ship a hook only if its mean rank is at least as good as the
median real hook.

## 4. Worked example: the Jar (VS1Z_Q-Klt8, 30.7M), line by line

Paraphrased fragments only. Times are word timings from ricks24_beats.json.

| s | Job | What the line does (paraphrase) | Why these words | Question it leaves |
|---|---|---|---|---|
| 0.0 | **Hook (H2)** | an inventor sets a ball in a bronze dragon's mouth and warns the emperor to run if it ever falls | three hard nouns (ball, dragon, emperor), plain verbs (put, told, falls, run); the last word is one syllable, a command | why would a falling ball mean run? |
| 5.2 | **Doubt** | the whole court laughs | 6 words, one sound; the vindication setup | will they be sorry? |
| 7.2 | **Setup ("You see" bridge, 11 %)** | the device described as a picture: eight dragons around a jar, each holding a ball over a frog's open mouth | one image per clause, one number (eight), no function given | what is it for? |
| 13.4 | **Stakes / doubt from power** | the emperor has the biggest army and won't run from a jar | echoes "run"; shrinks the device ("a jar") in the doubter's mouth | will pride cost him? |
| 17.6 | **E1** | weeks later a ball falls, and nothing happens | time jump + trigger + anticlimax, 8 words | was it fake? |
| 20.3 | **Joke** | not even a ripple, a dig at the emperor | the doubt turned into a gag | - |
| 22.2 | **Doubt escalates** | they laugh even harder | callback to 5.2 s, now worse | - |
| 24.1 | **E2** | the emperor mocks it as a costly toy and throws the inventor out, jar and all | stakes move to the hero: exile | what happens to him? |
| 29.5 | E2 | he drags it up a hill and lives alone | a picture of loneliness, no comment | - |
| 32.8 | **E3 (rule of three)** | one night a ball drops; then another; then all eight | sentences shrink (5, 2, 5 words): the rhythm is the escalation | what does all eight mean? |
| 37.0 | **E4** | he runs to the gates to warn the city, and the guards jeer | two short jeers as dialogue; the third round of laughter | will anyone listen? |
| 45.8 | **Payoff (before the mechanism)** | the next morning the palace is rubble | one image; nobody explains yet | how did the jar know? |
| 48.5 | **Turn into the mechanism (75 %)** | inside hangs a pendulum with a rod toward each dragon | "inside" is the turn word, not "You see" | how does it work? |
| 52.4 | Mechanism | a nudge, the pendulum swings, the rod opens a jaw, the ball drops | a chain of 4 verbs, each drawable | what did one ball mean? |
| 58.2 | Mechanism | one ball means a faraway tremor | the number answers the setup's "eight" | and all eight? |
| 60.3 | **Last line** | all eight meant the biggest quake was right under them | returns to "all eight" and to the palace; ends on the place | - (closed) |

**The architecture**
1. Odd act plus a warning.
2. Doubt (6 words).
3. "You see" picture of the device.
4. The powerful doubter's "but".
5. The first trigger fizzles.
6. Doubt grows.
7. The stakes move onto the hero.
8. A rule-of-three acceleration.
9. The jeers.
10. The payoff image.
11. The mechanism as a chain of drawable verbs.
12. The last line closes the first question.

Every line leaves one question, and the next line answers the previous one while opening another.

## 5. Myeongnyang: hook test and the first 20 s on the Jar architecture

**Blind ranking** (`research/library/cold_reads/myeongnyang_hook_ranking.json`)
- **Set:** 13 of our variants (all naming an act Yi does) and 6 real top hooks (4 Ricks, 2 Zack D.), shown as text.
  Three fresh judges each saw a different shuffle.

| Mean rank (of 19) | Hook | Source |
|---|---|---|
| 1.0 | buried with a bell on his finger (paraphrase) | Ricks, 10.9M |
| 3.3 | a ball in the dragon's mouth, "run" (paraphrase) | Ricks, 30.7M |
| **3.7** | **Told to give up the navy, Admiral Yi wrote back four words and sailed thirteen ships at a hundred and thirty-three.** | ours (winner) |
| 4.7 | oil poured into the sea with pirates close behind (paraphrase) | Ricks, 10.8M |
| 5.7 | sawing gaps into a railroad (paraphrase) | Ricks, 9.0M |
| 6.3 | Admiral Yi sailed out to fight a hundred and thirty-three warships, and his own captains hid behind him. | ours |
| 7.3 | Admiral Yi anchored his last thirteen ships in a strait so loud the locals called it crying... | ours |
| 13.3 | the absolute-zero body premise (paraphrase) | Zack D., 17.2M |
| **14.0** | Ordered to give up the navy, Admiral Yi took his last thirteen ships to fight a hundred and thirty-three. | **our v1** |
| 19.0 | the moving-hair premise (paraphrase) | Zack D., 20.5M |

- **Why it won (judges' notes):** a withheld detail ("four words") on top of the odds. Like the Jar's warning, it
  is something the protagonist said that the viewer wants to hear.
- **What separated the rest:** the fleet-count-only hooks ranked 11-17; those that end on an act or a slight ranked
  better.

**First 20 s, mapped line by line to the Jar** (full v2 in `research/library/drafts/story-myeongnyang.md`)

| s | Jar job | Myeongnyang v2 line |
|---|---|---|
| 0.0 | Hook: odd act + something said to the ruler | Told to give up the navy, Admiral Yi wrote back four words and sailed thirteen ships at a hundred and thirty-three. |
| 5.7 | Doubt (6 words) | His captains thought he was mad. |
| 7.4 | "You see" bridge (11 %) | You see, Japan's invasion fleet has just wiped out Korea's navy. Yi's ships are all that's left. |
| 12.0 | The ruler's word, answered (the open question closed) | So when the king tells him to give up the navy, Yi writes back: "I still have ships." |
| 16.9 | The powerful side's "but" | But the Japanese fleet fills the horizon. |
| 18.8 | E1: the odd choice | So Yi picks his spot: a strait so narrow the huge fleet has to squeeze through it. |

**Frame 0 for this hook.** Yi close, at his desk by lamplight on his ship, brush on the reply (the key prop). The
thirteen ships facing the 133 come in at 2-4 s, on "sailed thirteen ships". The integrator's 13-vs-133 wide is the
right second image, not the first.
