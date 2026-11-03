# Comedy and invention: how RicksClips and Zack D. play it

Built 2026-11-02 from data already on hand, with no new downloads:
- the 24 RicksClips story Shorts (`research/references/data/ricks24_beats.json`: transcripts, word timings, my joke,
  dialogue and reversal coding, and the per-sentence frames);
- the 16 Zack D. what-if Shorts (captions and 0-3 s / last-2 s strips from the Spark lanes copy);
- the 10 annotated Zack D. Shorts in `research/corpus/zackd/`.

Reference moves are paraphrased; every full example line is ours. Tiers: Ricks top / mid / bottom 8 by views;
Zack what-if top 8 / ordinary 8; Zack corpus 7 outliers / 3 controls.

## 1. The moves, counted

| # | Move | Where it sits | Ricks top / mid / bottom | Zack top / ord | Tracks views? |
|---|---|---|---|---|---|
| C1 | **Comeuppance ending**: the mocker or villain gets the disaster, exaggerated (the wave drops exactly on the pirates; the "perfect" railroad kicks sideways; the palace that laughed is rubble) | payoff / final line, 4-5.5 s | 3 / 1 / 2 | - | **yes (3/8 vs 3/16)** |
| C2 | **Ironic one-liner last line**: a dry summary that flips the frame (on paper nobody gambled; holding the idea instead of the balls; the debt buried with him) | final line, 2.5-5.3 s, 11-21 words | 4 / 2 / 1 | - | yes |
| C1+C2 | **Final line is comic, ironic or a comeuppance** | final line | **6 / 2 / 3** | - | **6/8 vs 5/16** |
| C3 | **Absurd-consequence punchline** (your face meets the track; a haircut feels like losing fingers; you melt into goop; the bank sends you to a coin machine that keeps 16 %) | final line | - | **6 / 3** | **yes** |
| C4 | **Running gag / callback of the mockers**: the laugh line returns 2-3 times, then flips ("nobody's laughing now") | setup -> escalation -> final | 4 / 1 / 2 | - | **yes (4/8 vs 3/16)** |
| C5 | **Fake dialogue**: invented quotes, often in a modern voice | setup and escalation | 5 / 5 / 4 | (Zack rarely uses dialogue) | no (floor) |
| C5a | ...in modern slang inside a period setting (the "toy guy", "you go check", "you're making soup?") | escalation | 4 / 1 / 1 | - | weak yes |
| C6 | **Hyperbole gag mid-story** (the world's priciest toy; a horse that lost to the milk cart while pulling it; a rival who'd lose a race carrying two beers) | escalation, median 37 % of runtime | 4 / 2 / 2 | - | weak |
| C7 | **Invented twist ending on a fictional plot** (the buyer is the burglar; the customer was an agent; the town founder is his mom) | final 10-20 % | 1 / 3 / 3 | - | **no (1/8 vs 6/16)** |
| C8 | **"The moral" ending** (joke or sincere) | final line | 0 / 0 / 1 (the tree video) | 0 / 1 (the bird-and-fish rhyme, 3.6M) | **no, avoid** |
| C9 | **Debunk or doom ending** ("it wouldn't work", "everyone dies") | final line | 0 / 0 / 0 | **0 / 4** | **no, avoid** |
| C10 | **Whole-video fiction gag on a real-sounding title** (a wordless outlet gag; a fake patent product) | whole video | - | corpus: 2/7 outliers, 0/3 controls | small n |
| C11 | **Anachronism played for laughs** (an object out of its era) | - | 0 / 0 / 0 | 0 / 0 | not used; they use modern *voice* (C5a) instead |

**Timing**
- **Mid-story jokes:**
  - median position 37 % of runtime (escalation);
  - 0.9-7.6 s long (median 3.2 s);
  - top-tier jokes are shorter: median 2.5 s, 12 words.
- **Final comic lines:**
  - 2.5-5.5 s and 11-21 words;
  - the video ends about 0.2 s after the last word, with no tail to "let it land".
- **No pause before the punchline:** the gap before joke and last lines is 0.18 s (median), against 0.16 s before
  other sentences (whisper timings of the 8 refs with audio). The signal is in the words and the picture, not the
  timing.

**How they signal "this is a joke, not a fact"**
1. **It's a character talking.** Jeers and boasts are put in mouths, in modern slang, so they read as dialogue, not
   narration.
2. **Hyperbole past plausibility.** Nobody believes the horse was pulling the milk cart.
3. **The callback structure.** The third laugh, then "nobody's laughing", tells you the story is being told for
   effect.
4. **The face on screen.** On joke lines the frame cuts to the speaker's exaggerated face: a guard cackling and
   pointing, two smug bettors, a captain grabbing a collar.
5. **A fence between story and fact** where it matters. Hedge words mark the real-but-unsure: "rumoured", "apparently",
   "in real life". One mid-tier video turns from its invented sting story to the facts with "in real life" at its
   pivot.

## 2. What they keep true, what they invent, and where they cross

- **Kept true.** In every real-mechanism video the mechanism is right, and so are the checkable numbers stated as
  fact:
  - the pendulum, storm oil flattening ripples, thermal expansion and the standard rail length, shot types and the
    Rodman ball's weight;
  - the prize-exchange shop, the expulsion rooms, Benford's first digits, lottery stings and the fall-time study.
- **Invented:**
  - the plot around it (an exile on a hill, a rival railroad, a pirate chase in a storm);
  - minor characters and every line of dialogue;
  - the comeuppance staging (the wave lands on the pirates "50 yards behind"; the rival train jumps "right as" a train
    rolls on);
  - whole anecdotes (the bell-coffin murder plot is fiction wrapped around the real safety coffin).
- **Where the line gets crossed** (our check against common sources):
  - the Jar's last-line meaning of "all eight balls" (the device indicated a direction; it never read eight balls as
    "right underneath");
  - the "impossible to get fired" hook (the body later says "almost impossible");
  - "sink it in one shot";
  - a reaction-time claim stated as settled science.
  - That's 3/8 top, 1/8 mid, 0/8 bottom. Crossing hasn't hurt them, but each one is an embellishment of degree on a
    true base, never a reversed mechanism. **For us the line holds** (rule below).
- **Do funny endings track views?**
  - Ricks: yes, when the joke is the consequence of a true mechanism landing on the doubters (a comic or comeuppance
    final line in 6/8 top, 5/16 rest).
  - Zack D.: yes. Absurd-consequence punchlines are in 6/8 top against 3/8 ordinary; debunk, doom and moral endings
    in 0/8 top against 4/8 ordinary.
  - No, when the invention replaces the mechanism: invented twist endings on fictional plots are in 1/8 top against
    6/16 rest.

## 3. Patterns to use, with our own example endings

**P1. Comeuppance callback (C1 + C4).**
- Plant a doubter's line early.
- Repeat it once.
- End with the true mechanism's consequence landing on that doubter, plus one exaggerated image.
- Refs (paraphrased):
  - the room that mocked the bettor goes quiet as the wire spells his horse;
  - the emperor's laughing court wakes to rubble;
  - the pirates who laughed at the soup get the wave.
- Ours:
  - **Vasa type:** "The king got the mightiest warship afloat. For less than a mile." (true: she sank about 1,300 m
    out)
  - **Barca type:** "The guard who laughed at him spent the rest of the siege on his knees, ear to a shield."
    (invented fate, plainly a joke)
  - **Myeongnyang type:** "Suddenly, his captains can't wait to follow him." (used in v2)

**P2. Ironic one-liner (C2).** Close the hook's question in one dry sentence that reframes the whole story. No
moral, no "and that's why".
- Refs (paraphrased): nobody, on paper, ever gambled; you wake up holding the idea instead of the balls; every debt
  went into the ground with him.
- Ours:
  - **Vasa type:** "The thirty sailors had run the test perfectly. Nobody wanted the answer."
  - **Barca type:** "The Persians had picks, tunnels and months of work. The city had one man who listened to the
    floor."
  - **Myeongnyang type:** "The king thought Yi had nothing left, but he had one line and a sea that switched sides."
    (used in v2)

**P3. Absurd consequence (C3; for what-if and mechanism Shorts).** Commit to the premise and end on the one physical
consequence the viewer can feel. No debunk.
- Refs (paraphrased): the faceplant; the haircut that feels like amputation; the coin machine's 16 % cut.
- Ours: "Fill the Vasa's ballast to the top, and she floats perfectly level, with her gun ports exactly at sea level."

**Avoid:**
- **C7:** a twist that replaces the true mechanism.
- **C8:** moral endings.
- **C9:** debunk or doom endings.
- Any joke that states a false number or a wrong mechanism.

## 4. The rule for us

1. **Invented plot, characters, dialogue and punchlines are fine when they read as story or as a joke:** a
   character's line, obvious hyperbole, a callback, an exaggerated face on screen. They need no source.
2. **Every stated fact stays sourced:** numbers, dates, names, places, the mechanism and real outcomes (deaths,
   losses, who won). If a fact is contested, hedge it on air ("historians think", "by one count", "Korean records
   count").
3. **The joke rides on the true mechanism, never replaces it.** The comeuppance is the real consequence, staged for
   laughs; the cause stays exactly right.
4. **Don't put invented words in a named real person's mouth as if quoted from history.**
   - Paraphrase a documented line (Yi's reply), or give the invented line to an unnamed character (a guard, the
     captains).
   - When it isn't obvious, mark the dramatisation in the script's fact notes.
5. **Check with the cold reader.** Ask "did you take any joke as a real fact?"; the answer must be no. (Myeongnyang v2:
   no, 3/5 funny.)
