# Story script reviews (script and pacing track)

Proposals only: nothing here edits an episode. The owner routes them. Every number is from
`research/library/STORY_SCRIPT_SPEC.md` and `pipeline/qa/script_judge.py`; full reports in
`research/library/script_reports/` and `research/library/drafts/*.judge.md`.

How the scores were made: the deterministic checks use whisper word timings of the rendered audio (the same method as
the references); the 7 rubric items were answered by the script-track agent with `pipeline/qa/SCRIPT_JUDGE_PROMPT.md`
(`*.rubric.json`). Beat boundaries were set by hand with `--beats` where the heuristics missed them (noted in each
report). On the 24 references the judge gives top 90.6, middle 70.0, bottom 63.9.

## story-vasa (v2 render, 2026-11-02 10:55): 80.8 / 100 with the rubric (85.6 measured checks only)

Reads well and is already on the spec for runtime (63.4 s), words (231), pace (3.72 w/s), pivot ("You see" at 62 %),
setup end (27 %), escalation (4 steps by hand) and sentence length. The gaps, biggest first:

1. **It's a fact list.** About 10 distinct facts at the grain used for the references (top 8: 2-7, median 5) and
   15 number tokens (top 8: 1-5): Thirty, 1628, seventy-two, two, four, thirteen hundred, thirty, 120, twice, thirty,
   1961. The viewer can't hold them, and none is the hero number. Keep "thirty sailors" (it carries the hook and the
   last line); make the rest pictures (two gun decks stacked high; "in her own harbour"; "too little stone").
2. **The ending is an epilogue.** "It sits in Stockholm today, never sailing again." is 8 words, and the video runs
   1.1 s past it. The top 8 end on the payoff (11-24 words) and stop within 0.5 s. The real payoff line is already
   in the script ("So when thirty men ran across the deck, the ship was already warning them."): end there, or on a
   stronger version of it, and drop the 1961 raising (save it for the description or a pinned comment).
3. **No laughs and no doubter's voice.** 0 jokes (top median 2), 0 jeers, and the admiral's line is reported, not
   heard. The facts give us two dry laughs we can use without inventing anything about real people: nobody dares tell
   the king, and the inquiry blames no one because the man who ordered the guns was the king. Quote the admiral and
   the letters as short lines (paraphrases of the testimony and the letters).
4. **Hook too long.** Sentences 1-2 together are 24 words / 6.2 s; the paradox ("and the ship sailed anyway") lands
   after the top 8's hook has already ended (3.0-5.4 s). Fold it into one sentence of about 20 words.
5. **Two gaps >= 0.4 s** (0.50 s after "1961," and 0.44 s after "sinks."); the references have at most one. Minor;
   cutting the epilogue removes the first.
6. **Mechanism slightly long** (56 words in 14 s vs 32-49 in the top 8): "The Vasa was the opposite." and the 120-ton
   detail can go; the comparison carries it.

**Proposed narration:** `research/library/drafts/story-vasa-proposed.md` (judge 97.8 on estimated timing, rubric
included; originality PASS against the 24 Ricks transcripts). 234 words, about 64 s at 3.67 w/s (trim to ~225 if the voice runs slow), 5 number tokens,
about 6 facts, 3 dry jokes, 2 quoted lines, 5 escalation steps, "You see" at about 69 %, mechanism 50 words, last line
= the opening test as the warning. Line-by-line against v2:

| v2 | Proposed | Why |
|---|---|---|
| S1-2: "Thirty sailors ran back and forth ... After the third run, the admiral stopped the test, and the ship sailed anyway." | "Thirty sailors ran across a brand-new warship until she nearly rolled over, and the navy sent her to sea anyway." | one 20-word hook, paradox inside 5.5 s |
| S3-4: "It's 1628 in Stockholm. The king, away at war, orders seventy-two heavy cannons ..." | "The admiral stops the test and mutters, 'If only the king were here.' But the king is off at war, and he wants the mightiest warship afloat." | the doubter gets a voice; two numbers gone |
| S5: "two decks of guns ... and hundreds of carvings" | "two decks of heavy bronze cannons, stacked high above the water" | the mechanism's cause, planted early; carvings cut |
| S6-8: rocks harder / admiral wishes / letters | "Nobody wants to tell the king his masterpiece wobbles. His letters keep arriving: 'Get her to sea.'" | joke 1 + the king's line |
| S9-14: launch, gusts, 1,300 m, about thirty die | launch crowd; "One light gust leans her over. She shakes it off, and the crowd keeps waving."; second gust, ports under; "the Vasa sinks inside her own harbour" | escalation in pictures; distance and toll go to on-screen text if wanted |
| S15-16: "The inquiry punishes no one. Only God knows, one builder says." | "At the hearing, one builder's best explanation is, 'Only God knows.' Nobody is punished. The man who ordered the cannons was the king." | the reversal and joke 2 |
| S17-21: weighted toy, opposite, 120 tons, twice, thirty men warning | bottle with sand; "built upside down, with tons of bronze up high and too little stone below"; more stone sinks the ports | 50 words, one comparison |
| S22-23: raised in 1961; sits in Stockholm | "So when thirty sailors nearly rolled her over at the dock, the Vasa was showing them exactly how she would sink." | the payoff is the last line; callback to frame 0 |

Facts to re-check before voicing: "inside her own harbour" (she sank about 1,300 m out, in Stockholm harbour) and
"The man who ordered the cannons was the king" (the 1626 armament order; the inquiry found no one guilty). The
admiral's and the king's lines are paraphrases, as the v1 script already notes. Voice at about speed 1.30 and measure:
the target is 3.6-3.8 w/s with no gap >= 0.4 s.

## story-chess-turk (posted v4, 67 s): 83.4 / 100 with the rubric (82.8 measured checks only)

Posted, so this is for the next story script, not a re-edit. Structure is on spec: setup ends at 29 %, five
escalation steps, the pivot ("There was a man inside.") at 74 %, 42 words of mechanism, a payoff last line that ends
on the word. The losses are delivery and voice:

1. **Too slow and too pausy:** 3.11 w/s (refs 3.36-4.09) and 6 gaps >= 0.4 s, 9.4 s of gaps in total (refs: at most
   one, 3.9-7.1 s in total). That's most of why it ran 67 s. The current script.md at speed 1.28 already reads
   3.78 w/s.
2. **No character lines and one joke.** The court "laughs" but never says anything; Napoleon never speaks. A single
   jeer ("A wooden man? Does it eat, too?") and one dry aside would put it at the top-8 median.
3. **Hook 22 words / 6.6 s** (refs 3.0-5.4 s): "He built a chess robot that could beat anyone" is a claim; the odd act is the
   second half. Leading with the act ("Before every game, he opened his chess robot to prove it was empty.") is
   14 words.
4. **Six numbers** (1770, one by one, eighty, Twice, 1854): one over the range; the years add nothing a viewer keeps.
5. **Nine facts**, at the top of the range: fine for a ~60 s cut, crowded at 67 s.

## Topic queue drafts (STORY_TOPIC_QUEUE.md ranks 1-2)

Both on estimated timing (not voiced yet); rubric answered by this track, so treat the rubric half as a self-check,
not an independent review. Originality PASS against the 24 Ricks transcripts. They share some phrasing with the
queue's own notes (our text).

| Draft | Score | Words / est. s | Hook | Pivot | Numbers | Facts | Jokes | Notes |
|---|---|---|---|---|---|---|---|---|
| `drafts/story-barca-shield.md` | 100.0 | 218 / 60 | 19 words, the smith laying his shield in the dirt | "You see" at 67 % | 2 | 6 | 2 | trench-and-oath ending left out (a second mechanism); sequel material |
| `drafts/story-myeongnyang.md` | 98.7 | 215 / 59 | 19 words, 13 ships vs 133 | "You see" at 61 % | 5 | 6 | 2 | tide-turn hedged ("historians reckon"); "I still have ships" paraphrases the traditional quotation |

Before voicing either: run `python3 -m pipeline.qa.script_judge <slug>` again on the voiced episode (it picks up
`audio/captions.json`), and for the gap checks run whisper on the render and pass `--timings`.

## Reproduce the scores

```bash
R=research/library/script_reports; D=research/library/drafts
python3 -m pipeline.qa.script_judge $R/story-chess-turk_v4.narration.md --timings $R/story-chess-turk_v4.whisper.json \
  --duration 66.77 --beats "E=5-6,7-9,10-11,12-14,15;P=16;M=16-19;L=20" --rubric $R/story-chess-turk_v4.rubric.json
python3 -m pipeline.qa.script_judge story-vasa --timings $R/story-vasa_v2.whisper.json --duration 63.42 \
  --beats "H=1-2;E=6-8,9-11,12-14,15-16;P=17;M=17-20;L=23" --rubric $R/story-vasa_v2.rubric.json
python3 -m pipeline.qa.script_judge $D/story-vasa-proposed.md --beats "E=5-6,7,8-9,10-11,12-14;P=15;L=18" --rubric $D/story-vasa-proposed.rubric.json
python3 -m pipeline.qa.script_judge $D/story-barca-shield.md --beats "E=5,6-9,10-11,12;P=13;L=17" --rubric $D/story-barca-shield.rubric.json
python3 -m pipeline.qa.script_judge $D/story-myeongnyang.md --beats "E=6-7,8,9-10,11;P=12;M=12-14;L=16" --rubric $D/story-myeongnyang.rubric.json
python3 -m pipeline.qa.script_judge --calibrate
```

The `*.whisper.json` files are faster-whisper medium.en word timings of the rendered audio (Mac, int8):
`story-chess-turk_v4.mp4` (posted) and `out/story-vasa/story-vasa_v{1,2}.mp4`. The Vasa v2 report is a snapshot of
`episodes/story-vasa/script.md` as of 2026-11-02 ~11:00; re-run after any script change.

## Cold-reader "makes sense" test (2026-11-02)

- **Method:** one fresh reader per script (Claude Sonnet, no tools, no context). Pass A: the narration only. Pass B:
  the same reader with the shot list.
- **Scoring:** keys and scores in `research/library/cold_reads/`; method in `pipeline/qa/COLD_READ_PROMPT.md`.
- **All three readers retold every key beat** (who, what, why, twist).
- **None passed the "no lost line, no blocking jump" bar.**

| Script | Score (A) | Hook (keep watching) | Lost lines | Blocking jumps | Friction |
|---|---|---|---|---|---|
| story-vasa (posted text) | 50.0 | 3/5 | 3 | 6 | 0 |
| story-barca-shield v15 | 72.5 | 4/5 | 1 | 2 | 45 |
| story-myeongnyang (episode text = lightly edited draft v1) | 73.5 | 4/5 | 0 | 2 | 47 |

### What confused each reader

**story-vasa**
- **Lost lines (narration only):**
  - "If only the king were here" (why does the admiral want him there?);
  - the hearing beat (three ideas; never says the king can't be blamed);
  - "more stone would only have pushed those gun ports down" (the ballast trade-off is never said; it sounds like it
    contradicts the bottle-with-sand line).
- **Still confusing with the pictures:**
  - the guns "stacked high above the water" against "lower gun ports dip under", which is the most serious;
  - the more-stone line;
  - the admiral's meaning;
  - "sent her to sea" against sinking inside the harbour.
- **Unexplained terms:** Vasa, gun ports, ballast, waterline, hearing.

**story-barca-shield v15**
- **Lost line:** "So wherever it rang, the defenders dug straight down": no beat where anyone believes the smith.
- **Blocking jumps:**
  - the smith's motive (why would he suspect a tunnel?);
  - how the mocking guards came to act;
  - no outcome: did the city survive, did the siege fail?
- **Fixed by the pictures:** the map, the cross-section labels and the ringing macro fixed setting, tunnel and
  mechanism.
- **Not fixed by the pictures:** the motive and the missing ending.
- **Also flagged:** "Barca" heard as Barcelona or Barça; months of hammering against months of digging; tense shifts.

**story-myeongnyang (episode text)**
- **Slowed lines:** 8; no lost lines.
- **Blocking jumps:**
  - did Yi plan for the current or get lucky?
  - how the collisions became 31 losses, and what the other ships did.
- **Fixed by the pictures:** the 13/133 tags, the "after you" gestures, the arrows swinging and the JAPAN 31 / YI 0
  board fixed most of the slowed lines.
- **Not fixed by the pictures:** "Then, historians think, the roaring stops" (the stop arrives before the
  explanation, and the hedge makes the mechanism sound unproven).

### What to change

**Vasa** (posted, so for the next ship story):
- Say "gun ports, the holes the cannons fire through".
- Say "more stone makes her sit lower".
- Say "nobody can punish the king".
- Keep "high" and "low" consistent with the picture.

**Barca:**
- Give the smith one line of reason ("the attacks had stopped, and he wondered why").
- Add one line where a guard grabs a shovel.
- End on the outcome before the quip.

**Myeongnyang:** see the v2 rewrite and its rounds in `research/library/drafts/story-myeongnyang.md`.
