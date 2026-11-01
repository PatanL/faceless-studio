# explainer-orca: title options

Each option maps to a viral title pattern from `research/corpus/explainer` (INDEX.json, PLAYBOOK hook shapes).
Thumbnail text is listed next to each title so the two never repeat the same words.

| # | Title | Pattern (reference, views, outlier score) | Pair with thumbnail |
|---|---|---|---|
| 1 | **Why You'd Never Want To Meet An Orca** | Depth Theory series formula "Why You'd Never Want To Meet [X]" (fGcgWaswMns, 2.31M, 14.65x); same series name as explainer-blue-whale #2 | scale: 0 HUMAN KILLS |
| 2 | **The Killer Whale Has Never Killed You. Here's Why.** | Paradox stated first, then a promised answer (VtrcKTkhDHU "Why The Ocean's Deadliest Predator Refuses To Kill Us", 8.29M, 318.82x) | eye: IT CHOSE NOT TO |
| 3 | **Orcas Could Hunt You. They Choose Not To.** | Predator-refuses paradox as two short sentences (VtrcKTkhDHU, 8.29M, 318.82x) | scale-b: WHY NOT YOU? |
| 4 | **Why Orcas Are Much Scarier Than You Think** | "Much worse than you think" escalation (jw6bS-WL4F4 "Why This Tiny Jellyfish Is Much Worse Than You Think", 6.72M, 1.43x) | scale: 0 HUMAN KILLS |
| 5 | **Why Has An Orca Never Eaten A Human?** | Question title with the answer held back for the payoff (fmZfphacPPQ "Could You Survive Extreme Ocean Pressure?", 14.71M, 1.84x) | eye: IT CHOSE NOT TO |

**Pick:** #2 on Shorts and TikTok: it is the hook line, and the paradox earns the curiosity click. Use #1 on the 16:9 cut so it
sits in the "never want to meet" series next to explainer-blue-whale.

Thumbnails (`thumbs/`, 1280x720 + 1080x1920 each, spec `episodes/explainer-orca/thumbs.json`):
- `explainer-orca_explainer-scale_*`: whole orca on an 8 m ruler, tiny diver YOU, "0 HUMAN KILLS"
- `explainer-orca_explainer-eye_*`: orca head fills the frame, diver at its chin, "IT CHOSE NOT TO"
- `explainer-orca-b_explainer-scale_*`: teal scale variant, "WHY NOT YOU?"
