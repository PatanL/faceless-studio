---
template: horror
niche: first-person phone / group-chat apartment horror, 2D cartoon (mraevq / udhwkz format, original stories only)
sources: research/R2 (beat_templates.json T1-T4, premises.json), research/corpus/horror (12 annotated outliers), research/R5 (policy), backlog/horror/TOPICS.md
voice: Kokoro af_heart at speed 1.12 for "Nora" (the kit's protagonist is a young woman); bm_george 1.02 is the B5 default if a male lead is used
---

# Horror template

Format: a 60-90 s **Part 1** (9:16) that works on its own, ends on a cliffhanger, and can grow into a
2.5-3.5 min TikTok part or an 8-12 min YouTube compilation later (R2 §7). One first-person narrator reads
narration and every chat message.

Files: `episodes/<slug>/script.md` -> `episodes/<slug>/storyboard.json` via `python3 pipeline/episodes/build.py <slug>`.

## Hard contract between script and storyboard

1. **One narration paragraph = one scene** (cut at its first word). 1-3 sentences, 3-8 s each.
2. Chat bubbles, knocks and expression swaps are anchored to the word that mentions them, so the bubble
   pops in exactly when the narrator reads it.
3. Messages the narrator reads aloud appear on the phone **word for word** (R2: chat text lives inside the phone UI, captions sit above it).
4. A phone insert at least every ~25 s (R2 global rule); alternate phone, door/peephole and face shots ~every 6 s.

## Part-1 beat structure (60-90 s, ~240-290 words at ~230 wpm)

| # | Beat | % runtime | What it does | Device (corpus) | Default kit shot |
|---|---|---|---|---|---|
| 1 | **Rule / threat hook** | 0-8 | Line 1 <= 14 words, first person, past tense, names a concrete object (a rule, a chat, a door). The rule or warning is literally on screen. | spoken rule in first 5 s (7702661541224566049 0:00, 7692268145888873760 0:00), threat-at-home + omen rule (7659677578365537569 0:00) | `HandPhone` lock/chat with the rule as a bubble |
| 2 | **Channel + authority** | 8-20 | Where the warning came from and who "owns" the channel (Management, Mom, Night Desk, Maintenance). | official all-clear (7659677578365537569 0:08), authority account in chat | `HandPhone` chat, members with unit labels |
| 3 | **Chorus / test** | 20-35 | 2-4 quick replies in a burst (`[Name] from [unit]: [message]`), or the hero tests the channel with a question only the real person knows. One doubter. | chat read-out rhythm (7659677578365537569 0:28-0:55), password test (gzXY52lcAcI) | chat burst with typing dots |
| 4 | **Contradiction** | 30-45 | A second, more trustworthy channel says the authority is false (landlord, real maintenance, a records search, a private message). | second channel disproves (7702661471641128224 "What uncle?"), count-match reveal (7659677578365537569 0:24) | new chat thread, `kind: alert` bubble, `Glitch` |
| 5 | **Physical arrival** | 45-70 | The threat reaches the barrier: knocks, doorbell, footsteps, elevator counter. One wrong countable detail. | knock at the barrier (7654526047005723937 0:08), fake authority with one wrong detail (R2 §4) | `FrontDoor` knocks + shake, `Peephole`, `ElevatorPanel`, `Hallway` |
| 6 | **Reframe** | 70-90 | The channel the hero trusted is compromised or the authority never existed. Short verdict lines (3-6 words). | identity twist (7659677578365537569 4:00), "you're not imagining it" (omuJBFs2L6c 1:15) | face close-up (`Protagonist` terrified), `Heartbeat`, `RedText` |
| 7 | **Cliffhanger** | 90-100 | A new message/imperative or a reveal that reframes an authority; exactly **one** open question; last line is a full sentence. No "part 2" card. | hard cut on unresolved imperative (7659677578365537569 4:05, 7702661541224566049 end) | `HandPhone` final bubble or typing dots, `Glitch`, stinger |

Pacing (corpus): core hook <= 25 words / <= 6 s; a re-hook every ~6-8 s, tightening to 3-5 s in the final third;
alternate 10-14 word lines with 3-6 word verdict lines; a 0.3-0.6 s pause before the reveal (`[pause: 0.4]`).

Templates by premise type (R2 beat_templates.json): T1 Locked-Door Siege (group chat + fake authority),
T2 Unspoken Rule Broken, T3 2 A.M. Sound + Online Stranger, T4 Observer-Overlay (modifier). Each episode names one.

## Visual grammar (kit: `studio/src/kits/horror`)

- Phone scenes: `horror/HandPhone` full frame, `cy` 0.585, `phoneWidth` ~0.68, a blurred set behind (`blur` 10, `opacity` 0.6),
  `horror/Vignette` on top. Chat threads keep their history across scenes (older bubbles at negative `at`).
- Captions: top band, `y` 0.15, `fontSize` 76, sentence case, red highlight `#ff4b55`, `maxWords` 3.
- Sets: FrontDoor (knocks, feet shadow, handle jiggle), Peephole (Neighbour/silhouette), Hallway, ElevatorPanel, Bedroom, LivingRoom, Stairwell.
- Cast: `horror/Protagonist` ("Nora", our narrator) with expression swaps; `horror/Neighbour` / `Stranger` (Mr. Hale) as the face of any fake authority; silhouettes for anyone unseen.
- FX: Flicker, Vignette, Heartbeat (rising bpm into the reveal), Glitch (on reframes), RedText (one per episode max), Darkness.
- Night grade: blue-teal, low saturation; red only for the threat.

## Policy and originality gates (R5)

- Wholly original stories, characters, units and endings. Never reuse the seed plots (killer in the complex, fake cop with stickers,
  admin mutes the chat, burner phone, "802") or any line from the Chinese series.
- Non-graphic: no injury on screen, no gore words; thumbnail and first 7 s clean.
- Generic messenger UI only (the kit's), no WhatsApp/iMessage/WeChat branding; invented company names.
- Endings must differ episode to episode (sameness review): vary the channel (group chat, family chat, SMS, elevator support, landlord) and the final reveal.
- Front matter `references:` (2-3 corpus ids) + beat alignment table; `scripts/originality_check.py` must PASS.
- Not made for kids. Vertical parts >= 61 s for Creator Rewards.
