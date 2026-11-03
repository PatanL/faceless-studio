---
id: story-myeongnyang
lane: story (RicksClips3000 parity)
status: v2 draft from the script track (research/library/STORY_TOPIC_QUEUE.md rank 2); proposal only, episodes/story-myeongnyang is not touched
title: The Korean Strait That Changed Sides
target_runtime_s: 63-65 at 3.7-3.8 words/s (239 words)
facts_source: STORY_TOPIC_QUEUE.md section 2 (Encykorea, JoongAng Daily, PNNL, Kim 2015)
---

# The Korean Strait That Changed Sides: v2

> **Fact flag (operator, 2026-11-02): "wrote back four words" is not supported.** Yi's reply to the king was a longer
> letter, usually rendered as "I still have twelve ships" (a translation of a classical Chinese sentence), so "four
> words" counts our English paraphrase, not what he wrote. Before voicing, change it to something true that keeps the
> hook's shape, e.g. "wrote back one line" or "answered with a single sentence", and re-run the hook ranking only if
> the meaning changes.
>
> **Resolved (script track, 2026-11-02):** the hook now reads "answered with one line". The meaning is unchanged, so it
> was not re-ranked. Line 4 says "Yi answers", not "writes back".


## What changed from v1, and why

- **Hook**
  - v1's hook ranked 14 of 19 in a blind test against 6 real top hooks.
  - v2's hook ranked 3.7 of 19, between the Jar and Storm Oil (details below and in HOOK_BANK.md section 5).
  - It names an act one character does: Yi writing back.
  - It withholds what he said, which line 4 pays off.
  - **Accuracy fix (2026-11-02):** "wrote back four words" is now "answered with one line". His reply was a longer
    letter, and the famous line comes from it. This wording change was not re-ranked.
- **First 20 s:** rebuilt on the Jar's line-by-line architecture (hook, doubt, "You see" bridge, the ruler's word
  answered, the powerful side's "but", the odd choice).
- **Cold-reader fixes:**
  - The plan is now stated: the narrow strait, so only a few ships reach him at once.
  - The reversal is named as the tide.
  - "Historians think" now attaches to the tide's timing only.
  - The outcome is spelled out (the jam in front of his cannons, 31 lost, the rest turn back).
  - The last line credits both the plan (the strait) and the luck (the sea).
- **Ending (COMEDY_ENDINGS.md P1 + P2):**
  - comeuppance callback on the doubting captains ("Suddenly, his captains can't wait to follow him");
  - then the ironic one-liner that closes the hook's "one line" ("...but he had one line and a sea that switched sides").
  - The last ~10 s, from "Korean records count", run 40 words; the captains' line is invented and plainly a joke.
- **Removed:**
  - "four times a day" (now "every few hours", keeping the numbers at 5 tokens);
  - the "roaring stops" line that confused two readers.

## Narration

```narration
[sfx: brush] Told to give up the navy, Admiral Yi answered with one line and sailed thirteen ships at a hundred and thirty-three.

[sfx: knock] His captains thought he was mad.

[sfx: whoosh] You see, Japan's invasion fleet has just wiped out Korea's navy. Yi's ships are all that's left.

[sfx: knock] So when the king tells him to give up the navy, Yi answers: "I still have ships."

[sfx: whoosh_long] But the Japanese fleet fills the horizon.

[sfx: whoosh] So Yi picks his spot: a strait so narrow the huge fleet has to squeeze through it.

[sfx: whoosh] Locals call it the crying strait, for the sound of its water.

[sfx: impact] The Japanese pour in, carried by that rushing water. Ship after ship after ship.

[sfx: knock] His captains hang back, happy to let the admiral go first.

[sfx: impact] The strait is so tight only a few Japanese ships can reach Yi at once, and his cannons hold them off.

[sfx: stinger] You see, that rushing water is the tide. Every few hours, it stops and runs the other way.

[sfx: tick] Historians who rebuilt that day's tides think the tide turned mid-battle.

[sfx: whoosh_long] Now the water runs back out. The front Japanese ships get shoved back into their own ships, and the tangle is stuck in front of Yi's cannons.

[sfx: impact] Korean records count thirty-one Japanese ships lost, and none of Yi's. The rest turn back.

[sfx: knock] Suddenly, his captains can't wait to follow him.

[sfx: stinger] The king thought Yi had nothing left, but he had one line and a sea that switched sides.
```

## Frame 0 and the opening (for the integrator)

- **0.0-2.0 s (the hook's act):** Yi close, by lamplight on his ship, brushing his reply onto paper (the key prop),
  on "Told to give up the navy, Admiral Yi answered with one line".
- **2.0-4.0 s (context):** pull out or cut to his thirteen ships facing the 133, on "and sailed thirteen ships at a
  hundred and thirty-three". The planned 13-vs-133 image belongs here, not at frame 0 (LANE_PRINCIPLES S-hook:
  Barca's context-first opening scored 0/8 on the hook panel).
- **12 s:** "I still have ships": the letter seen from the king's side (pays off "one line").
- Keep the 13 and 133 numbers on screen as tags. Readers lose them by ear, and 31 later collides with 13.

## Facts and hedges

- Every fact is from the queue's verified list:
  - the navy destroyed (Chilcheollyang);
  - the king's order;
  - Yi's reply (a paraphrase of the traditional quotation, which has "twelve" warships);
  - 13 against about 133;
  - the crying strait;
  - the current that reverses;
  - the tide turning mid-battle;
  - Korean records' 31 and none of Yi's.
- **Hedged on air:** the tide turning mid-battle ("historians who rebuilt that day's tides think", queue fact 5,
  CONTESTED) and the losses ("Korean records count", queue fact 3).
- **Re-check before voicing:**
  - "The rest turn back": the Japanese fleet withdrew from the strait; check against Encykorea.
  - "Yi picks his spot" (choosing the narrows): consistent with the queue's story notes and Kim 2015.

## Scores

- **script_judge** (estimated timing, rubric by this track):
  - **98.5** with the comedy ending; measured checks only: 98.0 (`story-myeongnyang.judge.md`).
  - Lost points: 6 number tokens, where the spec allows 5 ("one line" is counted twice); a mechanism slightly over
    range; a hook 0.2 s long.
  - 240 words: 65.6 s at the reference pace of 3.67 w/s, 64 s at 3.75. Trim a word or two if the voice runs slow.
- **Hook, blind ranking:** mean rank 3.7 of 19 (3 judges: 5, 3, 3), mean score 7.3/10. v1's hook: 14.0, 5.7/10
  (`research/library/cold_reads/myeongnyang_hook_ranking.json`).
- **Cold reader**, one fresh reader per round, narration only (`research/library/cold_reads/`).

| Round | Version | Beats retold | lost lines | slowed | blocking jumps | Friction (0-100) | Main new confusion |
|---|---|---|---|---|---|---|---|
| 0 | episode v1 text | all | 0 | 8 | 2 | 47 | did Yi plan the tide or get lucky; how 31 ships were lost |
| 1 | first rewrite | all | 0 | 10 | 2 | 40 | same two, plus why a turning current moves oared ships |
| 2 | + plan/luck line | all | 1 | 8 | 2 | 37 | the hedge line itself ("nobody knows if he counted on the turn") |
| 3 | + tide named | all | 1 | 8 | 2 | 35 | "shoved backwards ... right under Yi's cannons" read as moving away |
| 4 | + jam rewrite | all | 1 | 8 | 2 | 40 | one 33-word paragraph; plan vs luck again |
| 5 | v2 minus final edits | all | 2 | 6 | 1 | 38 | the "plan was only the strait" line; picturing the jam |
| 6 | **v2 (this file)**, with the comedy ending and "one line" | all | **0** | 5 | **0** | 69 | **PASS** (one reader; confidence 4/5; ending 3/5 funny; took no joke as fact) |

**Result: round 6 passed. That is one reader; confirm with 3 before voicing.**
- Every reader retold every beat (who, what, why, twist), and every reader rated the hook 4/5.
- Rounds 0-5 never reached "no lost line and no blocking jump". Round 6 did: 0 lost, 0 blocking, 5 slowed; report in
  `research/library/cold_reads/story-myeongnyang-v2b.cold_report.md`.
- Each fix removed the flagged problem, but the next fresh reader found a different one.
- Friction stayed in a 35-47 band with no trend. One picky reader per round can't separate versions that close, so
  the pass rule should use 3 readers and a majority.
- What did hold across rounds: the mechanism paragraph is where readers stumble. Pictures fixed most of it in pass B
  for v1 (the arrows swinging, the tally board). So the shot list should carry the jam, and the narration should
  stay as short as above.

---

## v1 (2026-11-02, kept for reference; the episode copy in episodes/story-myeongnyang/ is a lightly edited v1)

**Beat plan (spec template, 62 s):** hook = the paradox act (ordered to quit, fights ten to one); doubt line (his own
captains); setup: the burned fleet, the king's order, his reply (a character line); escalations: he anchors at the
crying strait, the Japanese pour in on the current, his captains hang back, the roar stops (slack water); pivot at ~62 %;
mechanism in ~40 words (a river-like current that reverses, a gap only a few ships wide, the turn shoves them back);
payoff (Korean records: their losses, none of his) and the last line.

**Numbers kept to five tokens:** thirteen / a hundred and thirty-three (the hero contrast), four (times a day), one.
Left out: 330 at Eoranpo, 293 m, 11.5 knots, 31 ships, the tidal power station (good on-screen labels instead).

## Narration

```text
[sfx: whoosh] Ordered to give up the navy, Admiral Yi took his last thirteen ships to fight a hundred and thirty-three.

[sfx: knock] Even his own captains think he has lost his mind.

[sfx: whoosh_long] Korea's fleet has just been burned to the waterline by a Japanese invasion fleet.

[sfx: knock] So the king tells Yi to come ashore and fight on land. Yi writes back, "I still have ships."

[sfx: whoosh] Then he anchors them at the mouth of the narrowest, loudest strait in Korea. The locals call it the crying strait, for the roar of its water.

[sfx: impact] The Japanese fleet pours in with the current behind it, ship after ship, faster than any oar could row.

[sfx: impact] His captains hang back and politely let the admiral go first. For hours, his flagship holds the front almost alone.

[sfx: tick] Then the roaring stops.

[sfx: stinger] You see, the water in that strait runs like a river, and it turns around four times a day.

[sfx: whoosh] The Japanese had ridden the current into a gap so narrow only a few ships could reach him.

[sfx: whoosh_long] When the tide turned, historians reckon, that same current shoved their ships backwards into each other.

[sfx: impact] Korean records count ship after ship lost that day, and not one of his.

[sfx: stinger] The king thought Yi had no navy left, but he had a sea that changes sides.
```

## Facts used (all from the queue's verified list)

- Korea's fleet destroyed at Chilcheollyang (1597); the king ordered Yi to give up the navy and fight on land; Yi
  refused ("I still have ships" paraphrases the traditional quotation "your servant still has twelve warships").
- Yi had 13 ships; about 133 Japanese ships entered the strait (Encykorea; JoongAng Daily).
- Myeongnyang / Uldolmok, "the crying strait", for the roar of its water; very narrow; the current runs like a river and
  reverses about four times a day (Encykorea; PNNL).
- His captains hung back at first (queue story notes).
- The tide turning mid-battle is a modern reconstruction: hedged on air as "historians reckon" (CONTESTED, queue fact 5).
- Losses: "Korean records count" (CONTESTED on the Japanese side, queue fact 3); none of Yi's ships lost.
- Left out: the iron chains (probably legend).

## Shot notes (S-env)

The burning wreck after Chilcheollyang; the royal court and the messenger; Yi writing at night; the strait from the
Jindo cliffs with whirlpools; the Japanese fleet streaming in on the current (arrows of water); the flagship alone at the
front; the current reversing (the same arrows flipping), ships shoved back into each other; end on the empty strait
running the other way.
