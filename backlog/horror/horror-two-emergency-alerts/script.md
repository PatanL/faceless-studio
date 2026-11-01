---
slug: horror-two-emergency-alerts
niche: horror
format: single            # standalone: 2 loops open at the cut (PLAYBOOK §4D standalone 0-2). No part label.
aspect: "9:16"
title: "Every Phone On My Floor Got An Emergency Alert"
alt_titles: see titles.md (8 ranked options)
template: pipeline/templates/horror.md T1 Locked-Door Siege, re-skinned onto the alert channel, + broadcast-PSA register for the alert text
engine: "The alert channel is the weapon: a real alert, a sloppy fake, then the real sender hijacked; each door's phone screams before its knock"
build: backlog/horror/horror-two-emergency-alerts/build.py   # lines.py -> Kokoro (tts_measure.py, Spark CPU) -> timeline.json + storyboard.json
voice: af_heart           # narrator. Plain values only (pipeline/audio/make.py reads these keys verbatim)
speed: 1.36
paragraph_pause: 0.06
voices_per_line: "lines.py VOICES: N af_heart 1.36 (narrator), T af_heart 1.12 + whisper fx (Tess speaking), A bf_emma 1.12 (alert text), D am_michael 1.08 (the man: door voice AND 'dispatcher', same voice on purpose)"
music: "music/dread.m4a, hard-muted (track segments end) for silences q1 (3.0 s), q2 (4.0 s) and q3 (0.9 s, the final hold)"
runtime_s: 124.7
words: 503
wpm_overall: 242        # Kokoro-measured over the full runtime incl. silences (PLAYBOOK narrated band 230-270)
hook: "Frame 0 = the lock screen at 2:47 with a red EMERGENCY ALERT card. 18 words in 4.8 s; the rule word lands at 1.6 s; the same channel contradicts itself at 6.2 s"
references:
  - id: "7654526047005723937"
    short: SIEGE-OVERLAY
    url: https://www.tiktok.com/@mraevq/video/7654526047005723937
    views: 716900
    outlier_score: 66.69
    why_chosen: "Highest outlier in the corpus and the closest hook shape (H3): an official all-clear with a number, a threat at the door, a contradiction by 7 s. We borrow the hand-at-the-door near-miss (0:07, 3:06-3:29), the barrier-under-a-clock (0:42-0:44 key; 3:45-3:59 'under a minute'), the lull where the knocking stops (2:38-2:44) and the lifeline Q&A. Not borrowed: killer, fake cop, overlay chorus, burner phone, gang, radio, '802'."
  - id: "7659677578365537569"
    short: SIEGE-CHAT
    url: https://www.tiktok.com/@udhwkz/video/7659677578365537569
    views: 376200
    outlier_score: 10.79
    why_chosen: "Same engine at a tighter cadence. We borrow the [Name, place]: [message] read-out, the countable proof, 'why is only the enemy's channel still working?' (2:11), the lone ally silenced (2:13-2:21), the rapid questions under a clock and the identity twist hidden behind a question the viewer expects a safe answer to (3:52-4:01), then the cut on an imperative from a channel that should be safe (4:05-4:08). Not borrowed: hallway song, stickers, muting admin, sublease, malware, jammer."
  - id: omuJBFs2L6c
    short: CLASSMATE-PSA
    url: https://www.youtube.com/watch?v=omuJBFs2L6c
    views: 762944
    outlier_score: 18.61
    why_chosen: "The only official-broadcast voice in the corpus and a ~97 s short. We borrow the deadpan institutional register for the alert text, the turn that moves the threat into YOUR place at ~43% with the video's single full-frame colour flash (0:41-0:45), and the sign-off-as-cut with the last shot bookending the first (1:32-1:37). Not borrowed: extra-classmate premise, rules list, ritual phrase, brand ident, pictograms."
secondary_device_sources:
  - "Qz-TrB6W2SM (HOTEL-DOOR, 1.52M, 9.0x): silence as a re-hook after the knock (0:45-0:53 dead air) and the barrier ladder (door -> it has a key card). Device-level only."
---

# Every Phone On My Floor Got An Emergency Alert

**Premise.** At 2:47 a.m. every phone on the eleventh floor of Ashby Tower screams: shelter in place, open your door for no one, not even emergency services. Nine minutes later a second alert retracts it and asks residents to let county staff in. Tess Avila, 11F, checks the sender: *Countv*, one letter off. So the open-up alert is fake. But before every knock, the phone behind that door screams first, door by door down the hall, and each neighbour who opens posts the same words: *All done. Painless. Open up when they knock.* Ines, next door, starts to warn her and is cut off mid-word. Then Tess works out that the alerts are choosing doors, and hers hasn't screamed yet. It does. Alert three comes from the correctly spelled sender and says to admit county staff. The voice at her door knows her sister's name, though Tess's call to her never went through. Through the peephole a man presses her own lock screen to the glass. A key opens her door to the chain. She calls the number in alert three, the only call all night that rings. The calm dispatcher confirms the v alert was fake ("good catch"), says the new one is real, and asks for her name, her unit and whether anyone is with her. "Just me." *Thank you, Tess*, in her ear and through the gap in her door at once. Then alert four: her name, one occupant, open the door.

**Why it should work (evidence).**
- **Topic demand (long-form, not Shorts):** in `backlog/horror/evidence/emergency_alert_horror_story.jsonl`, alert-premise narrations pull 230K-492K: Mr. Creeps' curfew alert (ep3H0HvoGgo, 492K, 61 min), "Every Screen: HIDE" (ycSq5xSF_oQ, 310K, 40 min), Lighthouse Horror's Brynhorn alert rules (nZrs5_rmstI, 394K, 27 min) and "Stay Inside and Lock Your Doors" (cF6p1IKtVJk, 268K, 24 min). GregBroDudeMan's 2.48M (hgjc2Zp6jMc) is a 41-min reaction compilation, so it shows audience appetite for alert horror, not a story format. None of these is a Short. The evidence file has no short-form alert-horror outlier, so this is a format bet.
- **Format proof:** the short-form proof is the corpus, not the topic. CLASSMATE-PSA (763K, 18.6x, 97 s) shows the official-broadcast register working in a ~100 s video, and SIEGE-OVERLAY / SIEGE-CHAT show the fake-authority siege on a phone UI.
- **Cheap to build:** the alerts, chat, call and lock screens are pure UI drawn in code, and the storyboard validates with no kit edits.

**Ownable signature.** The phone screams before the knock. Every door they choose gets an alert first, so the viewer learns the rule by watching it three times, and at 49% Tess says it out loud: *mine hadn't screamed yet.* The second signature is the letter v. It is visible from 0:06, glints once at 9.9 s with no VO, gets spelled out at 0:27, and is turned inside out at 1:58: *The v was never a mistake.*

**Plants and payoffs.**

| Plant | Planted | Paid |
|---|---|---|
| "Further instructions by alert only." (alert 1 footer, on screen) | 0:00 (cover frame) | Alerts 3 and 4 are exactly those further instructions, from the hijacked sender (1:04, 2:00) |
| "Countv" in alert 2's sender line | 0:06 on screen, glint 9.9 s | Spelled out 0:27; the "dispatcher" says "Good catch" 1:41; reframed "The v was never a mistake" 1:58 |
| Raf: "They asked how many live here." | 0:17 | The dispatcher: "is anyone with you?" 1:50 → "Just me" → alert 4 "One occupant" 2:00 |
| A phone screams down the hall before each knock | 0:11, 0:29, 0:34, 0:47 | 0:56-1:00 the pattern is named; 1:02 her own phone screams; 1:07 her door gets the knock |
| Her call to her sister Josie fails | 0:40 | 1:10 the voice at the door says Josie called them; 1:16 the tell: that call never went through |
| Only the chat and the alerts still work | 0:42 | 1:31 the number from an alert is the only call that rings; it is them |
| "All done. Painless. Open up when they knock." | 0:31 Raf, 0:36 Lorna, 0:49 Ines (the ally) | 1:25 every door on the floor stands open, dark: the neighbours' fate, shown |

**Loops at the cut (standalone, 2 open):** (1) does Tess open, and what happens to the one occupant; (2) who "they" are and how they took the county's alert system. **Closed in the video:** which alert is real (only the first), whether the dispatcher is real (no, it is the man at the door), what happened to the neighbours who opened (every door open and dark), and why the fake was spelled wrong (bait). Early loops close before 50% (the sender check at 22%, the pattern at 45-49%), per PLAYBOOK §5.

**Changes from the reviewed draft.** Protagonist renamed (Nora → Tess Avila), the fourth floor and 401-409 door-number ladder are gone (eleventh floor, phone-before-knock ladder, names not unit numbers), the "X:12 a.m." opening and the "___ Court" building are gone (Ashby Tower, no spoken clock time), the hold queue and the second "One, ma'am" answer are gone (the lifeline is now the trap), and there is a near-miss, a key-and-chain clock and a silenced ally.

## Pacing vs PLAYBOOK (Kokoro-measured on the Spark CPU, `tts_durations.json`)

| Metric | Ours | PLAYBOOK target |
|---|---|---|
| Runtime | 124.7 s | Story 150-360 / Shorts 50-100: we sit between them on purpose (see below) |
| Words, wpm over the full runtime | 503 words, **242 wpm** (spoken 280) | narrated 230-270 over the full runtime |
| Alert lines (bf_emma 1.12, flat) | 189 wpm | broadcast 145-180 |
| Core hook | 18 words, 4.8 s ("Every phone on my floor screamed at once." + alert 1) | ≤30 words, ≤6 s |
| Rule word / first contradiction | 1.6 s / 6.2 s ("Previous alert sent in error") | line 1 ≤12 words; contradiction ≤11 s |
| Jolt interval | median 1.9 s, max 6.0 s (59 jolts) | median 6, ≤8, nothing dry >25 s |
| Timed silences | 3.0 s (0:52.9, knocking stops: breath + one creak) and 4.0 s (1:21.2, the scariest image: one heartbeat), plus a 0.9 s final hold | 1-3 silences of 3-8 s with SFX |
| Numbers spoken | 3.9 per min (nine minutes, three doors, alert three, three knocks, four inches, eleven-F ×2, one occupant) | narrated 2.2-5.8 |
| Second-person sentences | 6% (alerts, door voice, dispatcher) | narrated 5-15% |
| Sentence median | 4 words (narrator 5); the bubbles and alerts count as sentences, so 51% are ≤4-word punch lines | 6-9, punch lines at spikes |
| Midpoint turn | 0:55.9-1:01.0 (45-49%), amber flash on "yet" at 1:00.5 | 45-60% |
| Peak contact | her phone screams 1:02.7 (50%) → door knocks 1:07.6 (54%) | starts ~67% (47-80) |
| Scariest image, held | 1:18.7-1:28.7 (63-71%), held still 4.0 s at 1:21.2 | 60-80%, ~4 s |
| Lifeline under a clock | 1:29.7-1:55.1 (72-92%); the clock is the door open on its chain, straining every ~2.3 s | 70-90% |
| Truth twist | 1:55.1 (92%) "Thank you, Tess." in two places | 85-95% |
| Cliff + bookend | 1:59.5-2:04.7 (96-100%), same framing as frame 0 | last ~5% |

**Runtime choice.** 124.7 s sits between the corpus' Shorts (50-100 s) and its stories (150-360 s), which a reviewer flagged. We kept it rather than padding to 150 s or cutting to 95 s. At 95 s the ladder loses rungs (the ally, the near-miss and the clock), and those beats are what the critiques asked for. At 150 s we would drop below 230 wpm or need filler. YouTube Shorts allow up to 3 min, and TikTok's Creator Rewards need more than 1 min, so 125 s works on both. If the A/B test shows retention falling off after 100 s, the cheapest cut is s04's Lorna line + n11 + s10 (about 6 s).

## Beat alignment (ours vs the reference, both as % of runtime)

| Our beat | Ours (time, %) | Reference id @ timestamp (%) | Device borrowed | How we adapt it |
|---|---|---|---|---|
| B1 Hook: threat + official order | 0:00-0:04.8 (0-4%) | 7654526047005723937 @0:00-0:05 (0-1%); 7659677578365537569 @0:00-0:08 (0-3%) | H3: danger in my building in line 1, an official channel speaks in 3 s | Line 1 is 8 words and the official order starts at 1.6 s. The alert itself is the threat, and it is on screen in frame 0 |
| B2/B4 False safety + contradiction | 0:05.0-0:10.9 (4-9%) | 7654526047005723937 @0:03 (1%) "N minutes later" all-clear; 7659677578365537569 @0:08 (3%) | An all-clear with a number, contradicted inside 11 s | The contradiction comes from the same channel: two alerts cancel each other |
| B3 Intrusion | 0:10.9-0:14.0 (9-11%) | 7659677578365537569 @0:11 (4%) | The knock that follows the false all-clear | A phone screams at the far end of the hall, then that door gets the knock: rung 1 of our own ladder |
| B5 Chorus + ignored proxy | 0:14.0-0:25.7 (11-21%) | 7659677578365537569 @0:31-0:55 (12-22%) read-out, @0:55-1:11 (22-28%) "no one replied" | `[Name, place]: [message]` every 2-3 s; doubts nobody answers | Raf plants "how many live here", Ines asks the viewer's question, Lorna defends the fake, Tess's question gets typing dots and then nothing |
| B4 Countable proof | 0:25.7-0:29.5 (21-24%) | 7659677578365537569 @0:19-0:28 (8-11%); 7654526047005723937 @0:15 (4%) | A detail the viewer can verify proves the trusted channel is lying | One letter in a sender line, spelled out with a tick per letter. A 3-word verdict, not an explanation |
| B5 Ladder + count match | 0:29.5-0:39.8 (24-32%) | 7659677578365537569 @1:26-1:53 (35-45%) channel keeps pushing; 7654526047005723937 @0:22-0:46 (6-13%) pressure stack | Physical rungs ~3 s apart between chat beats; matched messages | Phone screams → knock → identical post. "Word for word. Even the full stop." |
| B6 Isolation | 0:39.8-0:44.7 (32-36%) | 7659677578365537569 @2:03-2:13 (49-53%) "why is the chat still working?"; 7654526047005723937 @1:18-1:20 (22%) | Outside lines fail; only the enemy's channel works | Calls and texts fail; "the floor chat, and the alerts" still work. That seeds the trap at 1:31 |
| B5 Lone ally silenced | 0:44.7-0:52.1 (36-42%) | 7659677578365537569 @2:13-2:21 (53-57%); 7654526047005723937 @1:22-1:35 (23-27%) | One neighbour breaks ranks and is cut off | Ines's warning stops mid-word, her phone screams through Tess's wall, and a minute later she posts the line herself |
| B7 Lull + timed silence | 0:52.1-0:55.9 (42-45%) | 7654526047005723937 @2:38-2:44 (44-46%) knocking stops; Qz-TrB6W2SM @0:45-0:53 (27-32%) dead air | Silence as the jolt | 3.0 s, music muted, a breath and one creak |
| B8 Midpoint turn | 0:55.9-1:01.0 (45-49%) | omuJBFs2L6c @0:41-0:45 (42-46%) "in your [place]" + only colour flash; 7659677578365537569 @1:54-1:58 (46-47%) deduction | The frame flips onto the hero's own space; the single full-frame flash | The alerts were never warnings, they were choosing doors. "And mine hadn't screamed yet." Amber flash on "yet" |
| B9 Peak contact | 1:02.7-1:10.3 (50-56%) | 7654526047005723937 @4:22-4:25 (73-74%) hammering stops, handle rattles, a phone rings inside | The threat reaches the barrier with one sensory hit | Her phone screams (the rule pays), alert 3 is spelled right and says admit them, then three slow knocks. Earlier than the reference's 73%, inside the PLAYBOOK's 47-80% |
| B3/B9 Near-miss + dilemma | 1:08.6-1:17.8 (55-62%) | 7654526047005723937 @3:06-3:29 (52-59%) moves to open for a pleading voice, @0:24-0:26 polite command + consequence; 7659677578365537569 @0:16 (6%) "about to unlock" | The hero nearly complies, then catches a tell | The real sender says open; the voice is warm and names her sister; her hand slides the chain; the tell is that her call never went through |
| B9 Scariest image, held | 1:17.8-1:28.7 (63-71%); still 1:21.2-1:25.2 | 7654526047005723937 @4:22-4:25 (73%); device: omuJBFs2L6c @0:23-0:27 (24%) the entity knows your house | Proof the threat is inside your private space, held still | Her own lock screen pressed to the peephole: same wallpaper, same three alerts, 4 s of silence. Behind him every door is open |
| B10 Lifeline under a clock | 1:29.7-1:55.1 (72-92%) | 7659677578365537569 @3:17-3:44 (80-90%) one bar, 30 s, rapid questions; 7654526047005723937 @0:42-0:44 key coming, @3:45-3:59 (63-67%) "under a minute" | A real-looking authority on the one working line, with a clock; answers in rising order | The clock is a key in her lock and a chain whose screws are coming out. The answers rise: the v is fake → the new one is ours → name, unit, anyone with you? |
| B11 Truth twist | 1:55.1-1:59.5 (92-96%) | 7659677578365537569 @3:52-4:01 (93-97%) the safe-answer question hides the identity twist; PLAYBOOK T6 voice swap, T10 the authority never existed | The trusted authority is the threat | "Thank you, Tess." arrives on the phone and through the door gap at once. "The v was never a mistake" turns the midpoint proof into bait |
| B12 Cliff + bookend | 1:59.5-2:04.7 (96-100%) | 7659677578365537569 @4:05-4:08 (98-100%) cut on an imperative from a channel that should be safe; omuJBFs2L6c @1:32-1:37 (95-100%) sign-off as the cut, last shot = first | Hard cut on a new imperative; bookend | Alert 4 in frame 0's framing: her name, "One occupant. Open the door." Hard cut, no card |

## Script

Narrator Tess Avila, first person, past tense. Voices per line are in `lines.py` (the single source; `build.py` reads it and so does the Kokoro pass). Chat messages are read by the narrator in the `[Name], [place]: [message]` rhythm. Tess's own spoken words on the call are a separate whisper take. The alert text is a flat read of the banner. The man at the door and the "dispatcher" are **one voice** (am_michael 1.08): door fx (lowpass 1.3 kHz) at the door, phone fx (band-pass 300-3400 Hz) on the call, and both at once for the twist.

### Line-by-line (Kokoro-measured start times; speaker; on-screen)

| Start | Dur | Spk | Line | On screen |
|---|---|---|---|---|
| 0:00.1 | 1.41 | N | Every phone on my floor screamed at once. | COVER FRAME. Lock screen 2:47, alert 1 card: EMERGENCY ALERT · Lindhurst County Emergency Management · SHELTER IN PLACE. Do not open your door for anyone, including emergency services. Further instructions by alert only. |
| 0:01.6 | 3.13 | A | Open your door for no one. Not even emergency services. | Push in on the alert 1 body; caption card NOT EVEN EMERGENCY SERVICES |
| 0:05.0 | 1.16 | N | Nine minutes later, a second one. | Lock clock 2:56; alert 2 drops on top of alert 1 |
| 0:06.2 | 4.46 | A | Previous alert sent in error. County staff are visiting every unit. Please let them in. | Alert 2: sender 'Lindhurst Countv Emergency Management'. A 0.3 s hairline glint runs over the v (no VO) |
| 0:10.9 | 2.20 | N | At the far end of my hall, one phone went off. Alone. | Hallway, far end door lit; a faint red pulse under it |
| 0:13.2 | 0.46 | N | Then a knock. | Same hallway, tiny figure at the far door |
| 0:14.0 | 0.69 | N | The floor chat lit up. | Chat 'Ashby Tower · Floor 11', 12 members |
| 0:14.8 | 3.14 | N | Raf, end of the hall: County jackets. Super polite. They asked how many live here. | Raf: 'county jackets. super polite. they asked how many live here' |
| 0:18.0 | 1.58 | N | Ines, next door: So which one is real? | Ines: 'so which one is real??' |
| 0:19.7 | 2.06 | N | Lorna: The second, obviously. The first was a glitch. | Lorna: 'the second obviously. first was a glitch' |
| 0:21.9 | 2.84 | N | I typed: Then why did the first one say not even emergency services? | Me: 'then why did the first one say not even emergency services?' |
| 0:24.8 | 0.61 | N | Nobody answered. | Typing dots start under Lorna, then stop |
| 0:25.7 | 1.23 | N | So I checked who sent the second one. | Alert 2 details |
| 0:27.1 | 1.22 | N | Not County. C, O, U, N, T, V. | Full-frame header card: 'Lindhurst Countv'; letters light C·O·U·N·T·V on each tick; the v gets a red ring |
| 0:28.4 | 0.91 | N | The open-up alert was fake. | Card: 'PLEASE LET THEM IN' stamped FAKE |
| 0:29.5 | 1.72 | N | Then another phone went off, closer. Knock. | Hallway, figure nearer; pulse under door 2 |
| 0:31.3 | 2.54 | N | Raf posted again. All done. Painless. Open up when they knock. | Raf: 'All done. Painless. Open up when they knock.' |
| 0:33.9 | 1.88 | N | Lorna's phone was next, three doors down. Knock. | Hallway, figure at door 3 |
| 0:35.9 | 2.19 | N | Then Lorna. All done. Painless. Open up when they knock. | Lorna: identical bubble, stacked under Raf's |
| 0:38.2 | 1.34 | N | Word for word. Even the full stop. | ECU: the two bubbles aligned, both full stops ringed red |
| 0:39.8 | 2.59 | N | I called my sister, Josie. Call failed. My texts sat on sending. | Outgoing call 'Josie' -> 'Call Failed'; SMS 'pick up pls' with grey 'Sending...' |
| 0:42.5 | 2.15 | N | Only two things still worked. The floor chat, and the alerts. | Home screen: everything greyed except the chat icon and the red alert icon |
| 0:44.7 | 1.52 | N | Then Ines posted: Don't open. They're not | Ines: 'don't open. they're not'  (bubble ends mid-line) |
| 0:46.3 | 0.85 | N | That was the whole message. | Hold on the cut-off bubble |
| 0:47.4 | 1.54 | N | Then her phone screamed, right through my wall. | Living-room wall; the framed print rattles on the knock next door |
| 0:49.0 | 3.04 | N | A minute later, Ines posted. All done. Painless. Open up when they knock. | Third identical bubble, from Ines |
| 0:52.1 | 0.75 | N | Then the knocking stopped. |  |
| 0:52.9 | 3.00 | — | *[timed silence 3.0 s]* | Silence 3 s: Tess on the floor, back to the door, phone glow; music hard-muted |
| 0:55.9 | 1.87 | N | Every door they knocked, the phone behind it screamed first. | Floor plan diagram: doors light red in order 1, 2, 3, then the knock icon follows each |
| 0:57.9 | 1.78 | N | They weren't warning the building. They were picking doors. |  |
| 0:59.7 | 1.00 | N | And mine hadn't screamed yet. | THE ONLY FULL-FRAME COLOUR FLASH: amber on 'yet', then her door lights red on the plan |
| 1:01.0 | 1.57 | N | I held the power button. It wouldn't turn off. | Power-off slider glitches back to the lock screen |
| 1:02.7 | 0.64 | N | Then mine screamed. | Lock screen, alert 3 lands, phone shakes |
| 1:03.5 | 0.99 | N | Alert three. Spelled right. | Sender line 'Lindhurst County' gets a green underline under the y |
| 1:04.5 | 2.81 | A | Previous alerts sent in error. Admit county staff. | Alert 3 body + footer 'Questions? Call 555-0148' |
| 1:07.6 | 0.95 | N | Three slow knocks. My door. | FrontDoor, three knocks, feet shadow |
| 1:08.6 | 1.47 | N | Now the real sender was telling me to open. |  |
| 1:10.3 | 3.76 | D | Ms. Avila? County. Your sister Josie called us. She's worried sick. | FrontDoor, handle still; warm voice through the wood |
| 1:14.3 | 1.38 | N | My hand was already sliding the chain off. | ECU: her hand slides the chain halfway along the track |
| 1:15.8 | 1.94 | N | Then I remembered. My call to Josie never went through. | Insert: the 'Call Failed' screen again (1 s) |
| 1:17.8 | 0.77 | N | I looked through the peephole. |  |
| 1:18.7 | 2.47 | N | He was pressing a phone flat to the glass. On it was my lock screen. | Peephole POV: a man in a cap, backlit; a phone pressed to the lens |
| 1:21.2 | 4.00 | — | *[timed silence 4.0 s]* | SCARIEST IMAGE, held 4 s, no VO: her own lock screen inside the lens. Same wallpaper, the three red alerts, 3:09 ticking with hers |
| 1:25.2 | 3.46 | N | My wallpaper. My three alerts. Behind him, every door on my floor stood open. Dark. | Pull back inside the lens: behind him the hall, every door open, black inside |
| 1:28.7 | 0.84 | N | I put the chain back on. |  |
| 1:29.7 | 1.90 | N | Alert three had a number at the bottom. I called it. | Footer '555-0148' tapped; outgoing call screen |
| 1:31.7 | 1.74 | N | All night, nothing had connected. This one rang. |  |
| 1:33.5 | 3.17 | N | Then a key turned in my lock. The door swung in, four inches, and hit the chain. | FrontDoor from inside: door open to the chain, a strip of hall light; the chain shudders |
| 1:36.9 | 1.84 | D | Lindhurst County. Is your door shut? | Call screen 'Lindhurst County EM · 00:01' running |
| 1:39.0 | 1.49 | T | Did you send the alert with the v? | Tess MCU, pose ear, whisper |
| 1:40.7 | 2.03 | D | No, ma'am. That one's fake. Good catch. |  |
| 1:42.9 | 1.47 | T | And the one telling me to let them in? |  |
| 1:44.6 | 2.64 | D | That one's ours. Our staff are outside your door. |  |
| 1:47.5 | 1.99 | N | The chain jumped. The screws were coming out of the frame. | ECU: chain plate, screws backing out |
| 1:49.7 | 3.05 | D | Quickly now. Your name, your unit, and is anyone with you? |  |
| 1:52.9 | 1.93 | T | Tess Avila. Eleven F. Just me. |  |
| 1:55.1 | 0.84 | D | Thank you, Tess. | Split: the call screen and the four-inch gap; the same words arrive in both |
| 1:56.1 | 2.09 | N | In my ear, and through the gap in my door. The same voice. |  |
| 1:58.3 | 0.93 | N | The v was never a mistake. |  |
| 1:59.5 | 1.02 | N | My phone lit up in my hand. | BOOKEND of the cover frame: same lock screen framing |
| 2:00.8 | 2.93 | A | Tess Avila, eleven F. One occupant. Open the door. | Alert 4 card: TESS AVILA · 11F · ONE OCCUPANT. Open the door. Sender spelled right |
| 2:03.8 | 0.90 | — | *[timed silence 0.9 s]* | Hold on alert 4, then hard cut to black (no card, no tail) |

### Spoken text, plain (what the originality gate checks: it skips tables)

```spoken
Narrator: Every phone on my floor screamed at once.
Alert voice: Open your door for no one. Not even emergency services.
Narrator: Nine minutes later, a second one.
Alert voice: Previous alert sent in error. County staff are visiting every unit. Please let them in.
Narrator: At the far end of my hall, one phone went off. Alone.
Narrator: Then a knock.
Narrator: The floor chat lit up.
Narrator: Raf, end of the hall: County jackets. Super polite. They asked how many live here.
Narrator: Ines, next door: So which one is real?
Narrator: Lorna: The second, obviously. The first was a glitch.
Narrator: I typed: Then why did the first one say not even emergency services?
Narrator: Nobody answered.
Narrator: So I checked who sent the second one.
Narrator: Not County. C, O, U, N, T, V.
Narrator: The open-up alert was fake.
Narrator: Then another phone went off, closer. Knock.
Narrator: Raf posted again. All done. Painless. Open up when they knock.
Narrator: Lorna's phone was next, three doors down. Knock.
Narrator: Then Lorna. All done. Painless. Open up when they knock.
Narrator: Word for word. Even the full stop.
Narrator: I called my sister, Josie. Call failed. My texts sat on sending.
Narrator: Only two things still worked. The floor chat, and the alerts.
Narrator: Then Ines posted: Don't open. They're not
Narrator: That was the whole message.
Narrator: Then her phone screamed, right through my wall.
Narrator: A minute later, Ines posted. All done. Painless. Open up when they knock.
Narrator: Then the knocking stopped.
[timed silence 3.0 s]
Narrator: Every door they knocked, the phone behind it screamed first.
Narrator: They weren't warning the building. They were picking doors.
Narrator: And mine hadn't screamed yet.
Narrator: I held the power button. It wouldn't turn off.
Narrator: Then mine screamed.
Narrator: Alert three. Spelled right.
Alert voice: Previous alerts sent in error. Admit county staff.
Narrator: Three slow knocks. My door.
Narrator: Now the real sender was telling me to open.
The man: Ms. Avila? County. Your sister Josie called us. She's worried sick.
Narrator: My hand was already sliding the chain off.
Narrator: Then I remembered. My call to Josie never went through.
Narrator: I looked through the peephole.
Narrator: He was pressing a phone flat to the glass. On it was my lock screen.
[timed silence 4.0 s]
Narrator: My wallpaper. My three alerts. Behind him, every door on my floor stood open. Dark.
Narrator: I put the chain back on.
Narrator: Alert three had a number at the bottom. I called it.
Narrator: All night, nothing had connected. This one rang.
Narrator: Then a key turned in my lock. The door swung in, four inches, and hit the chain.
The man: Lindhurst County. Is your door shut?
Tess: Did you send the alert with the v?
The man: No, ma'am. That one's fake. Good catch.
Tess: And the one telling me to let them in?
The man: That one's ours. Our staff are outside your door.
Narrator: The chain jumped. The screws were coming out of the frame.
The man: Quickly now. Your name, your unit, and is anyone with you?
Tess: Tess Avila. Eleven F. Just me.
The man: Thank you, Tess.
Narrator: In my ear, and through the gap in my door. The same voice.
Narrator: The v was never a mistake.
Narrator: My phone lit up in my hand.
Alert voice: Tess Avila, eleven F. One occupant. Open the door.
[timed silence 0.9 s]
```

## Shot list (storyboard.json: 37 scenes, validates with `studio/src/cli/validate.ts`)

Every visual uses registered horror-kit components (HandPhone chat, Hallway, FrontDoor, LivingRoom, Protagonist recoloured auburn/mustard so she doesn't read as the kit's default "Nora", Vignette, Glitch, Flicker, Darkness) plus core layers. Where the kit can't do something yet, the shot is drawn from core layers instead, so **no kit file was edited**:
- The red emergency-alert card. It is stylised: a dark card with a red strip, a custom triangle and an in-world sender line, not a pixel copy of the iOS/Android WEA banner. "Lindhurst County" stays readable.
- The lock, outgoing-call and home screens, on a static phone frame.
- The peephole with a phone pressed to the lens, as one svg with its own clipPath. The man wears a cap, so he is not the recurring Mr. Hale puppet.
- The C-O-U-N-T-V header card, the bubble ECU, the floor plan, the chain and the 4-inch door gap.

Stills checked: `out/stills/horror-two-emergency-alerts_storyboard.jpg` and `_fix.jpg`.

| # | Scene | Start | End | What it shows |
|---|---|---|---|---|
| 1 | s01_cover_alert1 | 0:00.0 | 0:05.0 | COVER FRAME = frame 0: lock screen 2:47 with the red alert card already up; phone glow on a dark bedroom. During a1 the camera pushes onto the body so 'including emergency services' and 'Further instructions by alert only' read; caption card NOT EVEN EMERGENCY SERVICES sits in the top band ~3-5 s. |
| 2 | s02_alert2_stacks | 0:05.0 | 0:10.9 | Alert 2 stacks over alert 1 (clock 2:56). Sender line reads 'Lindhurst Countv Emergency Management'. A 0.3 s hairline glint on the v (fair-play plant, no VO). |
| 3 | s03_hall_far_phone | 0:10.9 | 0:14.0 | The far door glows red for a beat (its phone screaming through the hall), then a tiny figure knocks there. Rung 1 of the ladder: phone first, then the knock. (Check the red pulse sits on Hallway's end door on a still.) |
| 4 | s04_floor_chat | 0:14.0 | 0:25.7 | Chat 'Ashby Tower · Floor 11' (12 members). Raf's plant ('they asked how many live here'), Ines's viewer-proxy question, Lorna defends the fake alert, my question sends, typing dots under Lorna start and stop. |
| 5 | s05_countv_card | 0:25.7 | 0:29.5 | Zoomed sender header built from core text layers (kit has no per-glyph highlight): each letter lights on its tick (word-anchored to the Kokoro letter times), the V lights red and gets a ring, FAKE stamps on n13. |
| 6 | s06_hall_rung2 | 0:29.5 | 0:31.3 | Rung 2: a closer door glows red, then the knock. |
| 7 | s07_chat_raf_painless | 0:31.3 | 0:33.9 | Raf's second post: 'All done. Painless. Open up when they knock.' |
| 8 | s08_hall_rung3_lorna | 0:33.9 | 0:35.9 | Rung 3: Lorna's door, three doors down, glows red; knock. |
| 9 | s09_chat_lorna_painless | 0:35.9 | 0:38.2 | Lorna's identical post stacks under Raf's. |
| 10 | s10_bubbles_ecu | 0:38.2 | 0:39.8 | Bubble replicas as core layers (positions are ours, so the rings land): both full stops ringed red. Verify the ring x (806) against Montserrat 800 46 px on a still. |
| 11 | s11_isolation | 0:39.8 | 0:44.7 | Outgoing-call screen drawn from core layers (kit CallScreen is incoming-only): 'Calling…' -> 'Call Failed', then the SMS stuck on 'Sending…', then the home screen greyed except two icons: Floor chat and Alerts. |
| 12 | s12_ines_cut_off | 0:44.7 | 0:47.4 | The lone ally: Ines (next door) posts 'don't open. they're not' and the bubble ends mid-line. Hold on it. |
| 13 | s13_shared_wall | 0:47.4 | 0:49.0 | Her shared wall: red glow bleeds through on Ines's alert, the framed print rattles on the knock next door. |
| 14 | s14_ines_painless | 0:49.0 | 0:52.1 | Third identical post, from the ally who warned her. Pull out so all three identical bubbles show. |
| 15 | s15_silence | 0:52.1 | 0:55.9 | TIMED SILENCE 3.0 s after 'Then the knocking stopped.' Music hard-muted (music track ends here), room tone, one breath, one floor creak at +1.7 s. Tess low on the floor, back to her chained door, phone glow only. |
| 16 | s16_midpoint_plan | 0:55.9 | 1:01.0 | MIDPOINT TURN (B8 / S6 'in your place'): top-down floor plan; Raf, Lorna, Ines light red in order with a phone glyph, then KNOCK. The pattern says the alerts were choosing doors. THE ONLY FULL-FRAME COLOUR FLASH: amber 0.3 s on 'yet', then her door ('ME') pulses red. Camera pushes onto her door. |
| 17 | s17_power_button | 1:01.0 | 1:02.7 | Power-off slider: the knob slides, glitches and snaps back to the lock screen. They're inside the phone. |
| 18 | s18_my_phone_screams | 1:02.7 | 1:07.6 | PEAK CONTACT (the pattern pays): her own phone screams. Alert 3 lands from the correctly spelled sender (green underline under the y): 'Previous alerts sent in error. Admit county staff.' Footer: 'Questions? Call 555-0148' (fictional 555-01xx range). |
| 19 | s19_my_door_knocks | 1:07.6 | 1:10.3 | Three slow knocks timed to the transients inside knock3_slow.wav (0.01/0.96/1.91 s); feet shadow under the door. |
| 20 | s20_door_voice | 1:10.3 | 1:14.3 | Door voice (am_michael, door fx: lowpass 1.3 kHz): warm, specific, names her sister Josie. Tess in the lower left, turns shocked on 'Josie'. |
| 21 | s21_chain_slide | 1:14.3 | 1:15.8 | NEAR-MISS: ECU on the chain track; her hand slides the chain knob halfway toward the open end. |
| 22 | s22_call_never_went_through | 1:15.8 | 1:17.8 | The tell: a flash insert of the 'Call Failed' screen from s11. Josie never heard from her, so how do they know Josie? |
| 23 | s23_peephole_held_phone | 1:17.8 | 1:28.7 | Peephole as ONE svg with its own clipPath (the kit Peephole can't hold a prop): a backlit man in a cap (not the recurring Mr. Hale puppet), every hall door open and black behind him. He presses a phone flat to the lens: HER lock screen (same wallpaper as frame 0, three red cards, 3:09). SCARIEST IMAGE: the 4.0 s timed silence holds ~1.45x on the phone (one heartbeat at +0.8 s, faint flicker, no VO, music muted), then pulls back on n38 to show the open doors. Clock 3:09 matches her own phone. |
| 24 | s24_chain_back | 1:28.7 | 1:29.7 | Chain slammed back to the locked end (click). |
| 25 | s25_call_the_number | 1:29.7 | 1:33.5 | Push onto alert 3's footer, tap '555-0148', outgoing call. Everything else failed all night; this rings. |
| 26 | s26_key_door_hits_chain | 1:33.5 | 1:36.9 | A key turns (they have keys), the door swings in four inches and slams against the chain. DOOR_GAP svg: a 4-inch strip of hall light, the chain taut across it. From here the chain strains every ~2.3 s (the clock). |
| 27 | s27_dispatch_door_shut | 1:36.9 | 1:39.0 | 'Lindhurst County. Is your door shut?' (phone fx band-pass) |
| 28 | s28_tess_v_question | 1:39.0 | 1:40.7 | Whisper: 'Did you send the alert with the v?' Looking away from the door. |
| 29 | s29_dispatch_good_catch | 1:40.7 | 1:42.9 | 'No, ma'am. That one's fake. Good catch.' (sells trust; reframed at n45) |
| 30 | s30_tess_let_them_in | 1:42.9 | 1:44.6 | Whisper: 'And the one telling me to let them in?' Looking at the door. |
| 31 | s31_dispatch_ours | 1:44.6 | 1:47.5 | 'That one's ours. Our staff are outside your door.' |
| 32 | s32_chain_screws | 1:47.5 | 1:49.7 | ECU: the chain plate, screws backing out of the frame (clock rung). |
| 33 | s33_dispatch_anyone | 1:49.7 | 1:52.9 | 'Quickly now. Your name, your unit, and is anyone with you?' (= Raf's 'how many live here') |
| 34 | s34_tess_just_me | 1:52.9 | 1:55.1 | Whisper: 'Tess Avila. Eleven F. Just me.' |
| 35 | s35_twist_same_voice | 1:55.1 | 1:58.3 | TRUTH TWIST: d6 'Thank you, Tess.' plays twice, d6_phone (band-pass) and d6_door (lowpass) 0.06 s apart: the 'dispatcher' is the man at the door. Call card top, the 4-inch gap right, Tess bottom-left turning to it. |
| 36 | s36_v_never_a_mistake | 1:58.3 | 1:59.5 | Reframe of the midpoint proof: the Countv card returns with 'Good catch.' typed under it. The typo was bait so she'd trust the alerts that were spelled right. |
| 37 | s37_bookend_alert4 | 1:59.5 | 2:04.7 | BOOKEND of s01 (same framing, push and blur). Alert 4 drops on top of the stack: 'TESS AVILA · 11F · ONE OCCUPANT. Open the door.' Hold 0.9 s, then HARD CUT to black (no card, no music tail). |

## Audio

- **VO:** 60 per-line Kokoro clips on the Spark (`~/studio/tts/horror-two-emergency-alerts/`). They come from `tts_measure.py` and then `vo_fx.sh` (door / phone / whisper fx; d6 is rendered as d6_phone + d6_door, with the door copy 0.06 s later). Copy them to `studio/public/episodes/horror-two-emergency-alerts/vo/` before rendering.
- **New SFX (3, original, `gen_sfx.py`, in `sfx/` here; copy to `studio/public/sfx/` at promotion):**
  - `alert_tone`: four pulses of a gliding minor-third pair, 560→700 Hz and 672→840 Hz, all below 853 Hz.
  - `alert_tone_wall`: the same tone heard through a wall.
  - `chain_strain`: the chain snapping taut and rattling.
- **Alert-tone safety:** `alert_tone` is **not** the EAS Attention Signal (853 + 960 Hz two-tone), not the WEA cadence and not a SAME header. 47 CFR 11.45 forbids simulated EAS tones (FCC actions against Fox, CBS and ESPN promos), and real tones panic viewers whose phones use them. Never swap in a recorded real alert.
- **Existing SFX:** knock, knock3_slow (FrontDoor knocks sit on its transients at 0.01/0.96/1.91 s), message_pop, message_send, stinger, glitch, impact, click, door_creak, breath, heartbeat, tick, phone_buzz.
- **Explicit cues only.** There is no auto-SFX, because storyboard.json carries every cue. If this script is ever pushed through `pipeline.audio.make` instead, run it with `--no-auto-sfx`, or "knock" will double every knock.
- **Music:** dread bed in three segments. It cuts dead at 0:52.9 (q1), 1:21.2 (q2) and 2:03.8 (the final hold), and returns after each silence.

## Kit gaps (logged, not edited; the storyboard already has a core-layer equivalent for each)

1. A `kind: 'emergency'` NotifCard variant in horror/Phone, so lock notifications can be red alert cards inside HandPhone (the hand-held look). This shot uses a static phone frame for now.
2. A Peephole `held` slot (a prop phone inside the clipped fisheye).
3. `call.outgoing` in CallScreen (no Accept button or rings).
4. Per-entry `screens[]` prop merge.

Once 1-3 land, `build.py` can swap the core-layer screens for kit ones without retiming anything.

## Originality notes

- **Our own story:** Ashby Tower, Lindhurst County, the phone-before-knock rule, Tess, Raf, Ines, Lorna, Josie, the Countv bait, the hijacked sender, the lock screen at the peephole, the 4-inch chain clock and the two-place voice are all original. There is no killer, police officer, stickers, muting admin, burner phone, battery countdown, radio or room "802".
- **Distinct from our catalogue:** episodes/horror-member-41 has single knocks walking a fourth-floor door-number list; this script has no door numbers and no fourth floor, and the ladder is phones screaming. backlog horror-mom-two-chats is about two family messages and its protagonist is Nora; this one has no family authority and Tess is new. horror-new-building-rules has "X:12 a.m.", "Harrow Court" and pinned rules; here no clock time is spoken, the building is a Tower and nothing is a rules post.
- **Possible premise collisions** (checked on the Spark with yt-dlp metadata):
  - cF6p1IKtVJk (Lighthouse Horror, "Stay Inside and Lock Your Doors") narrates r/nosleep "The Smile of Your Shadow" by u/DustyBronco, a shadow premise.
  - bvggYlFsvD8 (Mr. Creeps) is a Boris Bacic stay-inside story.
  - We found no retraction-alert or phone-before-knock beat in either description, but the full transcripts were not checked.
- **Fictional details:** Lindhurst County is fictional (the nearest real name is a Nottinghamshire parish). 555-0148 is in the reserved fictional 555-0100..0199 range.
- **Gate:** `python3 scripts/originality_check.py backlog/horror/horror-two-emergency-alerts/script.md research/corpus research/library/transcripts` → PASS (2026-11-01, ~12:25 UTC). Both the whole script.md and a VO-only extract pass. VO 5-gram overlap with our own horror catalogue is ≤0.2% (pinned-rules, night-doorman-rules, new-building-rules).
- **Disclosure:** this is fiction told in first person. Never call it true. Turn on TikTok's AI-generated content label (synthetic voices). Put this in the YouTube description: "Fictional story. Synthetic voices. All animation is original and drawn in code." `research/R5` still has no policy file, so this follows the working guidance in `out/pilots/QA.md`.
