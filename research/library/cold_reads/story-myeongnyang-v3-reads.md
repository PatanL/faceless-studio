# Myeongnyang v3 (Storm Oil form): cold reads, 3 readers per round (2026-11-02)

Fresh readers (Claude Sonnet, no tools, no context), narration only, prompt per `pipeline/qa/COLD_READ_PROMPT.md`,
plus an `ending` question: which lines are jokes, did you take any joke as fact, is this a real historical event. Key:
`story-myeongnyang-v3.cold_key.json` (written before any answer). **Pass = every beat retold, no `lost` line, no
blocking jump. A round passes when 2 of 3 readers pass.**

| Round | Text | Reader | Beats retold | lost | slowed | blocking | Funny | Pass |
|---|---|---|---|---|---|---|---|---|
| A | first v3 draft (no anchored line; ending "drifts backwards past him") | 1 | all | 1 | 11 | 2 | 3 | no |
| A | | 2 | all | 0 | 7 | 2 | 3 | no |
| A | | 3 | all | 0 | 10 | 1 | 3 | no |
| **B** | **v3 as in the draft, before the last edit** | 1 | all | 1 ("captains back their ships away" vs anchored) | 8 | 1 | 4 | no |
| **B** | | 2 | all | 0 | 9 | 0 | 3 | **yes** |
| **B** | | 3 | all | 0 | 8 | 0 | 3 | **yes** |

| **C (final)** | **v3 with "anchor well behind him" and "channel" for "strait" (2026-11-03)** | 1 | all | 0 | 5 | 0 | 3 | **yes** |
| **C** | | 2 | all | 0 | 9 | 0 | 3 | **yes** |
| **C** | | 3 | all | 0 | 8 | 1 (how he knows the tide will turn) | 3 | no |

**Round B: PASS (2 of 3).**

**Round C (final text): PASS (2 of 3).**
- No `lost` line from any reader; the anchored-captains fix held.
- The one block: nothing says how he knows when the tide will turn. If it's wanted, a fix is one line before the turn,
  "Fishermen call it the slack: the water stops before it turns."
- All three readers again read the battle as a tale and only the tide as the fact.

**Round A blockers, fixed for B:**
- who won: "drifts backwards past him" read as an escape. Now: "his cannons pound the jam" and "the whole enemy fleet
  is drifting backwards out of the strait";
- why his ships don't move: added "His ships are anchored. Theirs aren't.";
- "pours in" against "only a few fit": now "But the strait is so narrow only a few ships fit at once";
- "politely letting him go first" ("go first where?").

**Round B, one reader's fail:** the captains "back their ships away" although everyone is anchored. The line now reads
"anchor well behind him" (edited after the round).

**What all six readers said about truth:**
- No names, place or date, so the battle reads as a tale or legend.
- The only claim presented as fact is the tide ("some narrow straits really do this").
- No reader took a joke as a historical fact. Two weren't sure whether "ten ships for every one of ours" is exact;
  it's a character's line, roughly the real 13 vs 133.

**Recurring slowed lines (not blocking):**
- "Watch the cork" pays off only at the "You see";
- "the jam" needs a beat to picture;
- the cork's return direction in the last line.
