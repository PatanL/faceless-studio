# Myeongnyang cold-read rounds (2026-11-02)

Each round is a **fresh** reader (Claude Sonnet, no tools, no context), narration only, with the prompt in
`pipeline/qa/COLD_READ_PROMPT.md`. Rounds 1-5 used the version of the prompt that asks for `lost`/`slowed` and
`blocks_understanding`; round 0 (the episode's v1 text) got those labels from the same reader in its second pass.
Prompts for rounds 1-2 are saved here (`story-myeongnyang-v2/v3.prompt_A.txt`); rounds 3-5 used the same template
on the texts quoted in `research/library/drafts/story-myeongnyang.md` history (this file lists what each reader flagged).

Every reader retold every key beat (who, what, why, twist) and rated the hook 4/5.

| Round | `lost` lines (the reader's words, condensed) | Blocking jumps |
|---|---|---|
| 0 (episode v1) | none | why Yi chose the strait / whether he knew the current would turn; how collisions became 31 losses |
| 1 | none | planned or lucky (the opening calls it his choice, "historians think" calls it luck); why a reversed current pushes ships that have oars |
| 2 | "Nobody knows if he counted on the turn, but historians think it came mid-battle" (hedge-heavy; undercuts "Yi had the sea") | how one ship survives the first wave; planned or lucky |
| 3 | "shoves their ships backwards into the ones behind, right under Yi's cannons" (backwards should mean away from Yi) | why a huge fleet enters a narrow strait / "ship after ship" vs "only a few"; planned or lucky |
| 4 | the 33-word captains + flagship paragraph (too long, "him" ambiguous) | planned or lucky; why the reversal jams ships instead of moving them |
| 5 | "Yi's plan was only the narrow strait. But historians ... think it turned mid-battle" ("it" ambiguous); "the water runs back out, shoving the front ships into the ones still pushing in" (hard to picture by ear) | how the jam became 31 losses |

What held across rounds:
- **The mechanism paragraph is where everyone stumbles.** "Current reverses → front ships pushed back into the rest"
  is hard to picture by ear. In round 0's pass B, the shot list (arrows swinging, ships colliding, the tally board)
  fixed it.
- **Plan vs luck needs one plain sentence**, and the hedge must attach only to the timing. Every reader who saw
  "historians think" near the climax read the whole win as uncertain.
- **13 / 133 / 31 collide by ear.** Put them on screen as tags.
