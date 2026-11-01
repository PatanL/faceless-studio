---
id: horror-night-doorman-rules
niche: horror
series: 2 parts (upload Part 2 first, then Part 1 a few seconds later so Part 1 sits on top of the grid; PLAYBOOK §5)
title_p1: I Broke Rule 3 of My Night Desk. The Owner Told Me To. (Part 1/2)
title_p2: The Desk Phone Rang From the Empty Apartment (Part 2/2)
alt_titles: see titles.md (8 ranked options)
format: 9:16
template: pipeline/templates/horror.md (T2 Unspoken Rule Broken + T1 fake authority in the phone)
engine: Taboo rule broken (job rules) x Two rival authorities (PLAYBOOK §1D)
cast: Lena (narrator, first night shift), Gus Brandt (night concierge 31 years, exists only as a chat), "Mr. Pell" (a contact saved as the owner), Marcus (day shift). Names are unique to this episode in backlog/ and episodes/.
runtime_s: {part1: {P1_RT}, part2: {P2_RT}}   # MEASURED: Kokoro-82M on the Spark CPU, per line (tts_durations.json)
words: {part1: {P1_W}, part2: {P2_W}}
wpm_overall: {part1: {P1_WPM}, part2: {P2_WPM}}   # words / runtime; PLAYBOOK §7 narrated band 230-270
wpm_speaking: {part1: {P1_WPMS}, part2: {P2_WPMS}}   # words / speech time (pauses and holds excluded)
voice: af_heart speed 1.35 (Lena reads her narration and every chat bubble aloud, "Gus: ..."); bm_george speed 1.05 for THE VOICE only (the 1903 line and the man in the blazer, Part 2)
music: dread bed, ducked under VO; the bed drops out for each held image (two music entries per part)
sfx_new: desk_ring (two-tone 440/480 Hz with a 20 Hz trill, synthesized on the Spark with ffmpeg aevalsrc; studio/public/sfx/desk_ring.wav)
source_of_truth: lines.py (spoken lines) -> tts_measure.py (Spark) -> build.py (timeline.json, storyboard.json = Part 1, storyboard_p2.json = Part 2, and the tables below)
references:
  - id: 7692268145888873760
    url: https://www.tiktok.com/@udhwkz/video/7692268145888873760
    views: 694900
    outlier_score: 19.94
    short: TRUCKER-RULES
    why: Closest engine. A mentor's job rules in the hook, the "tonight I broke them" confession (0:07), and rules broken on screen one at a time (0:20 rule 1, 0:25 the hubris rule). Also the sound-before-visual cue (1:45-1:51) and one grotesque image held about 4 s (2:09-2:12).
  - id: 7702661541224566049
    url: https://www.tiktok.com/@udhwkz/video/7702661541224566049
    views: 2200000
    outlier_score: 63.13
    short: HEARSE-P1
    why: The cleanest Part-1 skeleton (PLAYBOOK §9). A rule in the first second; a minor rule broken BEFORE it is stated (0:31 window spit, rule stated 0:36, "another rule" 0:41); a planted number paid in the sequel (plate, 0:47); a trap number for distance to help (47 km, 0:23); the held peak (2:37-2:46); a bookended cut (3:16-3:21).
  - id: 7702661471641128224
    url: https://www.tiktok.com/@udhwkz/video/7702661471641128224
    views: 343100
    outlier_score: 9.85
    short: HEARSE-P2
    why: The sequel of HEARSE-P1 (same series, counted with it as one reference pair). Used for Part 2's mechanics only: cold open with no recap (0:00-0:11), the Part-1 number plant paid at ~45% (plate, 1:28-1:29), the outside check that falsifies the companion's story (call, "What uncle?", 1:36-1:47), and the reframe "it wasn't him who lied" (1:59-2:00). Its hook comes late (0:20) and it got 16% of Part 1's views, so our Part 2 puts the jolt in line 1 instead.
  - id: 7659677578365537569
    url: https://www.tiktok.com/@udhwkz/video/7659677578365537569
    views: 376200
    outlier_score: 10.79
    short: SIEGE-CHAT
    why: Our main visual is a held phone with a chat. Borrowed devices: the official all-clear undercut within 5 s (0:06-0:11), clue questions (0:18-0:19), the `[Name]: [message]` read-out rhythm (0:31-0:55), the admin's command (1:43-1:51), the deduction that an authority account is fake (1:54-1:58), only one channel still working (2:03-2:11), the dying lifeline (3:17-3:33), the identity twist (3:58-4:01) and the cliff on an imperative message (4:05-4:08).
---

# Night Desk Rules (2 parts)

**Premise (original).** Lena works her first night on the front desk of the Calloway, a residential tower. The night concierge, Gus, had the desk for 31 years; last night was his last shift, and they never met. He adds her to a two-person chat, "Desk Handover", with six rules. Rule 3: *if 1903 calls, send nobody up. 1903 is empty.* At 1 a.m. she breaks rule 1 without having read it, and the building answers at once: the empty elevator comes down from 19 by itself, waits with 19 already lit, and climbs back. At 2:41 a contact saved as the owner, Mr. Pell, orders her up to 1903, and rule 5 says to obey the owner's texts. Gus says the number was never Pell's. The camera monitor shows 1903 open a crack and a man in a concierge blazer facing the wall beside it. Part 1 ends as line 1903 lights up red under old tape and Gus sends a new order: *Let it ring.*

Part 2 (cold open, works alone): she picks up anyway. A voice using Gus's name calls her "kid" and says the chat isn't him. Chat-Gus says he's home in bed. A paper staff sheet shows Pell's real number is not the one texting her, and dialing Gus's cell lights line 1903: his phone is up there. The 96th key (tag 1903), the empty elevator and the visitor log ("2:41, 1903 called, going up myself, back in five") all point up. She reads rule 3 the other way round: send nobody up is why Gus went himself and why nobody ever followed. Pell was right about one thing: somebody had to go up. She breaks rules 4, 2, 6 and, last, 3 ("I sent somebody up. Me."). On 19 a man in a concierge blazer faces the wall outside 1903. 911 fails at 4%. Without turning, in Gus's voice: *"Thanks, kid. Your shift now."* The light goes out. The chat: *"I'm sorry. I lied so you wouldn't come."* The cut: the handover chat adds Marcus (day shift) and sends the six rules **from Lena**, with rule 3 rewritten: *"Even if it sounds like me."*

**One identity model, and the props agree.**
- The **chat Gus** is the real Gus, and he is in 1903 (his cell rings there, P2 0:29). Every order he gives protects her: shut the door, don't go up, let it ring, don't pick up, put the key back, "if I'm standing up there, it isn't me". "I'm home in bed" is a protective lie, and he says so (P2 1:46, "I lied so you wouldn't come"). That also explains P1's question "How did he know? He wasn't even in the building": he was.
- **The voice** (desk line, then the man in the blazer) is the lure. It has Gus's voice and blazer and is the only speaker who says "kid" (re-watch clue, never stated).
- **"Mr. Pell"** texts from a number that is not the owner's (paper sheet 555-0178 vs texting 555-0143). Rule 5 is a real rule; the contact was swapped, so in Part 1 "neither rule was wrong; the number was" (P1 1:14).
- There is no pocket glow (the earlier draft had the blazer holding the chat's phone). The only device in 1903 is Gus's cell.

**What changed in this rewrite (critique must-fix list).**
- Rule 5 is now an obey order ("If Mr. Pell, the owner, texts you, do what he says"), so the midpoint clash is real, and it is resolved in one line by the swapped number. The "never calls" half is gone (no dead gun).
- The hook is honest: "A text from the owner ordered me to." The ascent is tied to the order in Part 2 ("Pell lied about everything else, but he was right about one thing. Somebody had to go up."), and rule 3 is the last and biggest stamp of the break ladder ("I sent somebody up. Me. Rule three." + a red **3 ✕** with the loudest hit).
- Rules 1, 2, 4 and 6 are prohibitions that can be broken ("Never open...", "don't get in", "if there's a 96th, don't touch it", "Never leave the desk before 7").
- A minor rule is broken in Part 1 at 0:15 (13%), before it is read (HEARSE-P1 0:31), and something answers at 0:17.5 (16%). Rules 1, 2, 4, 5 are read just in time; all six are on screen at 0:40.
- "Let it ring." is a fresh imperative at the cut (Gus never said it before; at 1:18 he only says "Don't go up. Don't send anyone." and ignores "and if 1903 calls?").
- Peak images: Part 1 holds 3.8 s on the CCTV tile, now with a figure and one change during the hold (1903's dark gap widens); Part 2 holds 4.0 s.
- All timing is MEASURED from Kokoro word timestamps on the Spark CPU; there is no assumed wpm anywhere in this file.
- Part 2 restates rules 3, 4 and 6 with their content for cold viewers; each ✕ stamp carries the rule text.
- Numbers cut: 24 floors (spoken), 11-to-7, 1102 pizza, 1:40. Fragments merged into 6-12-word lines; punch lines kept for spikes.
- Cast renamed (Lena, Gus Brandt) so the channel does not reuse "Nora" or "Varga".

**Distinct from existing episodes.** Not the seed plot (killer, fake cop, admin mute, burner phone), not horror-pinned-rules (knock rules, a fake neighbour at the door), not horror-member-41 (extra account, door-to-door knocks), not horror-elevator-maintenance (the floor counter climb here is under 3 s and uses its own events). The villain is a job handover; the barrier is a desk phone line and an elevator; the ending is the rules list re-sent in the narrator's name.

## Pacing check (measured)

| Metric | PLAYBOOK target | Part 1 | Part 2 |
|---|---|---|---|
| Runtime | 165-250 s story, or 2 x ~120 s; each part >= 61 s (Creator Rewards) | {P1_RT} s | {P2_RT} s |
| Words / wpm overall | 230-270 narrated | {P1_W} / {P1_WPM} | {P2_W} / {P2_WPM} |
| wpm while speaking | (refs 262-366) | {P1_WPMS} | {P2_WPMS} |
| Core hook | <= 30 words, <= 6-7 s | {P1_HOOKW} words / {P1_HOOKS} s (lines 1-2) | 24 words / 5.8 s (q1-q2) + the voice line (10 words) ends at 9.1 s |
| Trusted source contradicted | <= 11 s | {P1_CONTRA} s (owner's text ordered the rule broken; banner on screen) | {P2_CONTRA} s (the voice: "it isn't me") |
| Words in the first 10 s | median 43.5 | {P1_W10} | {P2_W10} |
| Jolt interval | median 6 s, never > 25 s dry | median {P1_JMED} s, longest gap {P1_JMAX} s ({P1_JN} jolts) | median {P2_JMED} s, longest gap {P2_JMAX} s ({P2_JN} jolts) |
| Intrusion at the barrier (B3) | ~6% | 0:15 = 13% (rule 1 broken), the building answers 0:17.5 = 16% (the owner's banner is on screen at 0:05 = 5%) | 0:05 = 4% (picks up the 1903 line) |
| First proof (B4) | 8-20% | 0:17.5 = 16% (elevator comes down by itself) | 0:24 = 20% (paper vs the texting number) |
| Midpoint turn | 45-60% | 0:53.9-0:59.8 = 48-53% (the owner's order + rule 5) | 1:00.4 = 50% (rule 3 inverted) |
| Scariest image, held | once, 60-82%, ~4 s still | 1:20.3-1:30.5 = 71-80%, hold 3.8 s at 77-80% with one change (the door gap widens) | 1:28.7-1:36.7 = 74-81%, hold 4.0 s at 77-81% |
| Lifeline under a clock | 70-90% | 1:36.6 = 86% (security: next patrol 6 AM) | 1:36.7 = 81% (4% battery, 911 fails) |
| Truth twist | 85-95% | 1:13.6 = 65% (number "never his": early variant) | 1:43.0 = 86% ("Thanks, kid. Your shift now."), resolved 1:46 = 88% |
| Plants for next part | >= 2 unpaid | 96 hooks / 95 keys, 1903's empty hook, 19, 2:41, yellow tape, "how did he know?" | pays tape + line at 0:29 (24%), 96th key at 0:42 (35%), 2:41 at 0:57 (47%) |
| Loops open at the cut | 3-6 (series) | 5 (who is the man in the blazer, who is Pell, why 2:41, where is Gus, will she pick up) | 3 (is Lena the new thing in 1903, will Marcus obey, who/what texts as Pell) |
| Numbers per minute | 3-5 (narrated 2.2-5.8) | {P1_NPM} (distinct: {P1_NUMS}) | {P2_NPM} (distinct: {P2_NUMS}) |
| Sentence median / punch share | 6-9 words / 13-22% | {P1_SMED} / {P1_PUNCH}% (chat bubbles such as "Go up now." count) | {P2_SMED} / {P2_PUNCH}% |
| Questions | 3.3/min median | {P1_Q} ({P1_QPM}/min) | {P2_Q} ({P2_QPM}/min): "So which Gus was in my chat?" (0:18), "How?" (1:24) |
| Timed silences | 1-3 | 1.1 s typing, 3.8 s CCTV hold, 1.4 s ring, 1.3 s end | 0.6 s before "ninety-six", 4.0 s figure hold, 1.2 s end |

Notes: numbers per minute counts distinct load-bearing numbers (rule labels not counted); P2 runs a little high because the count ladder (93-94-95-96) and the floor ladder (5-9-13-16) are spoken on purpose. B6 isolation in Part 1 is late (89%); Part 1 has an earlier channel-loss rung only in the sense that the security line is a recording.

## Beat alignment

Timestamps on our side are measured (timeline.json). Reference timestamps were re-checked against `research/corpus/horror/<id>.md`.

| # | Our beat | Our time | Reference id + timestamp | Device borrowed | How we adapt it |
|---|---|---|---|---|---|
| P1-1 | B1 hook: rule 3 + confession + cause | 0:00-0:06.6 | 7692268145888873760 0:00-0:10 (rules, then "tonight I broke them" 0:07); 7702661541224566049 0:00 (rule in the first second) | Rule in line 1, confession, threat in frame 0 | Only rule 3 is spoken. The confession names the cause honestly ("A text from the owner ordered me to"), paid at 0:58 (the order) and in Part 2 (1:09 "Somebody had to go up", 1:16 "Rule three."). Frame 0 is the red light through the tape. |
| P1-2 | Trusted rule contradicted by an official voice | 0:05.4 | 7659677578365537569 0:06-0:11 (management's all-clear undercut by a knock 3 s later); PLAYBOOK §2 combination rule | Contradiction inside 11 s | The owner's banner ("Go up now.") flashes over the rule. Note: the earlier draft cited SIEGE-CHAT as a flash-forward; it has none. The flash-forward device is FARM-FLASHFWD's H10 (gzXY52lcAcI 0:00) and we do not use it. |
| P1-3 | B2 setup + authority | 0:06.7-0:13.8 | 7692268145888873760 0:07 (mentor + "over a decade"); 7702661541224566049 0:05 ("Tonight" entry) | The authority's years as a number | 31 years, never met, a chat is the only contact. 7 s. |
| P1-4 | B3 intrusion: a minor rule broken before it is read | 0:13.8-0:23.6 (break 0:15 = 13%; answer 0:17.5 = 16%) | 7702661541224566049 0:31-0:41 (spits out of the window, "Roll that back up", rule stated after, "another rule" 0:41); 7692268145888873760 0:20 (rule 1 broken on screen, 12%) | Break first, rule stated after the damage | She props the glass door at 1 a.m.; the empty elevator starts down from 19 by itself; Gus states rule 1 only after (0:20). |
| P1-5 | Clue question | 0:23.6 | 7659677578365537569 0:18-0:19 (rhetorical clue questions) | Rhetorical question as a plant | "How did he know? He wasn't even in the building." Paid in Part 2: his phone is in 1903. |
| P1-6 | B4 first proof: the rules are real | 0:25.4-0:39.6 (23-35%) | 7702661541224566049 1:08 (the ritual works: the hearse door opens, so the rules are real) | The world answers the rule | The empty car opens; 19 is already lit inside; the doors wait until she looks away, then it climbs back to 19. Rule 2 is read just in time (0:29). |
| P1-7 | Verdict | 0:39.6 | 7659677578365537569 0:55 ("This was way too coincidental."); 7692268145888873760 1:52 (3-word punch) | Short verdict at the spike | "One small rule broken, and the building answered in seconds." All six rules on screen. |
| P1-8 | B7 lull + plants | 0:43.7-0:53.9 (10 s) | 7702661541224566049 0:47 (plate "1574", paid in the sequel 1:29); 1:31-1:41 (lull) | Hyper-specific plant in a short lull | Rule 4 (95 keys, 96 hooks, 1903's hook empty) and the yellow tape. Both paid in Part 2. |
| P1-9 | B8 midpoint: the owner orders the break | 0:53.9-1:07.2 (48-60%) | 7659677578365537569 1:43-1:51 (the admin tags the hero: open the door now); 7702661541224566049 0:36-0:41 (rule stated just in time); PLAYBOOK §1D two rival authorities (DORM-RULES) | The authority's command read word for word; a rule revealed when it is needed | Rule 5 (obey the owner's texts) is read at 0:59.8, right after the order, and collides with rule 3. |
| P1-10 | Typing silence | 1:07.2-1:11.4 | 7659677578365537569 1:04-1:09 (nobody replies; held breath) | Silence as a re-hook | "Gus is typing…" on, off, on; 1.1 s with no VO. |
| P1-11 | The authority account is fake | 1:11.5-1:16.3 (65%) | 7659677578365537569 1:54-1:58 (deduction: the four accounts are fake, the killer has their phones) | Fake-authority reveal | "That number was never his." Resolves the clash in one line: "So neither rule was wrong. The number was." |
| P1-12 | B9 held image | 1:20.3-1:30.5 (hold 1:26.7-1:30.5 = 77-80%) | 7692268145888873760 2:09-2:12 (head out over the windshield, held ~4 s); 7702661541224566049 2:37-2:46 | One scariest image, held still | CCTV tile CAM 19-E: 1903 open a crack, a back-view man in a concierge blazer facing the wall beside it. During the 3.8 s hold the dark gap of the door widens. |
| P1-13 | Taunt + time match | 1:30.5-1:36.6 | 7659677578365537569 0:28 ("exactly 4": a count the viewer can check) | Number match | 2:41 tonight = 2:41 last night. |
| P1-14 | B10 lifeline + trap number | 1:36.6 (86%) | 7659677578365537569 2:03 (calls 911, no signal); 7702661541224566049 0:23 (47 km to the next exit) | Outside help removed, with a number for how far it is | Security line is a recording; next patrol 6 a.m. |
| P1-15 | B6 isolation | 1:39.7 (89%) | 7659677578365537569 2:21-2:30 (admin mutes everyone; the ally goes silent) | The ally goes silent | Gus's presence line goes "online" -> "last seen 2:38". |
| P1-16 | B12 cliff + bookend | 1:42.6-1:52.4 | 7692268145888873760 1:45-1:51 (engine sound before the car); 7659677578365537569 4:05-4:08 (imperative message at the cut); 7702661541224566049 3:16-3:21 (cut, bookend) | Sound before visual, fresh imperative, the last shot repeats the first | A ring she has never heard, then the red light under the tape, then "Let it ring." (new), then the frame-0 framing + PART 1/2. |
| P2-1 | Cold open: rule + threat + defiance | 0:00-0:05.8 | 7702661471641128224 0:00-0:11 (cold open, no recap); PLAYBOOK §5 (each part hooks cold in <= 3 s) | No recap; the situation is readable alone | Unlike HEARSE-P2 (hard hook only at 0:20), line 1 is the threat: the phone ringing from the empty apartment. She defies "Let it ring." |
| P2-2 | Contradiction on the line | 0:05.9-0:10.8 (7.1 s) | 7659677578365537569 2:13-2:18 (a lone message: "that's not the police"); 7702661471641128224 0:12 (jolt by 6%) | A lone voice discredits the trusted channel | The voice says the chat isn't him. Only this voice says "kid" (clue). |
| P2-3 | Rival authorities, read-out rhythm | 0:10.8-0:20.9 | 7659677578365537569 0:31-0:55 (`[Name] from [unit]: [message]`) and 2:11 ("why is the chat still working?") | Read-out chorus + a rhetorical restatement of the master question | Chat-Gus, Pell, the voice. "So which Gus was in my chat?" |
| P2-4 | B4 outside check on paper | 0:20.9-0:36.0 (17-30%) | 7702661471641128224 1:36-1:47 (calls the companion's dad: "What uncle?"); 7702661541224566049 3:07 (a private fact contradicts the story) | An outside fact falsifies a story | The laminated sheet: Pell's real number is not the texting one (pays rule 5); Gus's cell rings in 1903. |
| P2-5 | Count ladder, Part-1 plant paid | 0:36.0-0:45.0 (30-38%) | 7702661471641128224 1:28-1:29 (1 s tease, then the Part-1 plate paid); 7702661541224566049 2:32 ("Once, twice, three times": spoken count) | Spoken count with a beat before the wrong number | Rule 4 restated in full for cold viewers; 93, 94, 95, 0.6 s black, 96; tag 1903 on the hook that was empty in Part 1. |
| P2-6 | Sound before reveal | 0:45.0-0:52.5 | 7692268145888873760 1:45-1:51 | Sound first | The chime, then the empty car from 19 holding its doors. "Everything in this building was pointing up." |
| P2-7 | B7 lull + paper plant paid | 0:52.5-1:00.4 | 7702661471641128224 1:13-1:15 (quiet observation, then new physical evidence) | Evidence in a lull | Gus's log line at 2:41 last night pays Part 1's time match; "He never signed back in." |
| P2-8 | B8 midpoint reframe | 1:00.4-1:10.2 (50-58%) | 7702661471641128224 1:59-2:00 ("it wasn't him who lied"); PLAYBOOK T3 rule inversion (DORM-RULES, 50-63%) | The protective rule read the other way | Send nobody up is why Gus went himself and why nobody followed. Then the hook's promise: "he was right about one thing. Somebody had to go up." No undefined "they". |
| P2-9 | Rule-break ladder | 1:10.2-1:20.0 (58-67%) | 7692268145888873760 0:20, 0:25, 2:35 (each rule broken on screen); 7702661471641128224 0:20-0:45 (fast physical ladder) | One rule per beat, each named | 4 ✕ the 96th key, 2 ✕ rode it empty, 6 ✕ left the desk, then the biggest: **3 ✕ sent somebody up: me**. Chat-Gus: "Nobody means you too." |
| P2-10 | Channel removal; only the chat works | 1:20.0-1:26.2 | 7659677578365537569 2:03-2:11 (no signal, only the group chat works) | Only one channel still works | Lights dip at 13, signal dies at 16, the chat still delivers. "How?" Then: "If I'm standing up there, it isn't me." |
| P2-11 | B9 held image | 1:28.7-1:36.7 (hold 1:32.7-1:36.7 = 77-81%) | 7702661541224566049 2:37-2:46; 7692268145888873760 2:09-2:12 | One scariest image, held still | Part 1's CCTV composition in person, in colour, closer. |
| P2-12 | B10 lifeline under a clock | 1:36.7 (81%) | 7659677578365537569 3:17-3:33 (one bar of battery, a 30 s countdown) | A handicapped last lifeline | 4% battery, no signal, 911 fails: the last outside channel is gone. |
| P2-13 | B11 twist | 1:40.2-1:49.2 (84-91%) | 7659677578365537569 3:58-4:01 (the authority's identity collapses); 7702661541224566049 3:01-3:07 (a planted inconsistency for re-watchers) | Identity twist | The man in the blazer speaks in the line voice ("Thanks, kid. Your shift now."). Chat-Gus: "I lied so you wouldn't come." |
| P2-14 | B12 cliff + bookend | 1:49.2-2:00.0 | PLAYBOOK §4C ending #2 (new rule from a new authority, DORM-RULES); 7702661471641128224 3:09 (hard cut on a named threat, no remedy); 7702661541224566049 3:16-3:21 (bookend) | New rule mirroring the old rule's wording; last shot repeats the first | Marcus is added; the six rules go out from Lena; rule 3 now ends "Even if it sounds like me." Same bubble framing as Part 1 frame 0. |

---

## Part 1/2: "I Broke Rule 3 of My Night Desk. The Owner Told Me To."

**Hook.** First line (VO, 0:00): "Rule three of my night desk. If nineteen-oh-three calls, send nobody up." First visual (frame 0, also the cover): the desk-phone close-up with the 1903 button under yellow tape, a red light glowing **bright** through it (brighter than the story has it, so it reads at grid size), LCD "LINE 1903", and the rule-3 bubble as a red card. Cover text: **RULE 3: 1903 IS EMPTY.** (see thumbnail.md)

### Narration (one paragraph = one measured TTS line; VOICE = bm_george)

```narration
{P1_NARR}
```

### Timed script (measured)

| t | dur | VO / caption | Beat | On screen |
|---|---|---|---|---|
{P1_LINES}

### Scene list (storyboard.json)

| scene | start | end | notes |
|---|---|---|---|
{P1_SCENES}

---

## Part 2/2: "The Desk Phone Rang From the Empty Apartment"

**Hook.** First line (VO, 0:00): "Our front desk phone was ringing from nineteen-oh-three." First visual (frame 0, also the cover): the desk phone ringing, the red light pulsing through the tape, LCD "LINE 1903 · CALLING". Cover text: **1903 IS EMPTY. IT'S CALLING.**

### Narration (VOICE = bm_george)

```narration
{P2_NARR}
```

### Timed script (measured)

| t | dur | VO / caption | Beat | On screen |
|---|---|---|---|---|
{P2_LINES}

### Scene list (storyboard_p2.json)

| scene | start | end | notes |
|---|---|---|---|
{P2_SCENES}

## Production notes

- **Build:** `python3 build.py` (stdlib, Mac-safe) rebuilds timeline.json, storyboard.json (Part 1) and storyboard_p2.json (Part 2) from lines.py + tts_durations.json. After any wording change: rsync this folder to the Spark and run `CUDA_VISIBLE_DEVICES="" OMP_NUM_THREADS=4 nice -n 10 ~/studio/.venv/bin/python tts_measure.py tts_durations.json ~/studio/tts/horror-night-doorman-rules`, then copy the wavs to `studio/public/episodes/horror-night-doorman-rules/{p1,p2}/vo/` (done for this version).
- **Validation (this version):** `npm run validate` equivalent on the Spark: both storyboards ok (9:16, 30 fps, 34 + 37 scenes). `scripts/check_storyboards.py` on the Spark: all components registered, all audio present; the only flag is the deliberate held images (3.8 s and 4.0 s; the pilot's 3 s hold rule is overridden by PLAYBOOK §1A B9 "held still ~4 s"). Stills sheets were rendered on the Spark and checked: `out/stills/horror-night-doorman-rules_storyboard.jpg`, `out/stills/horror-night-doorman-rules_storyboard_p2.jpg`, plus the fix pass `out/stills/doorman_p1_fix.jpg`, `out/stills/doorman_p2_fix.jpg`.
- **Kit (locked until horror PASS, BRIEF 11:27):** no kit file was touched. The lobby, desk phone (taped 1903 button, red light, LCD), 96-hook key board, elevator doors and car, CCTV grid, staff sheet, visitor log and the back-view blazer figure are inline SVG / core layers in build.py (`lobby()`, `desk_phone()`, `keyboard()`, `elevator_view()`, `cctv_grid()`, `paper()`, `FIGURE`, `hallway_1903()`). When the kit unlocks they map 1:1 onto the producibility critique's proposed `horror/LobbyDesk` (views wide | deskphone | keys | monitor | elevator), `horror/Paper`, and Hallway props `endDoorAjar`, `endDoorLabel`, `figureFacing:'away'`, `figureX`. The CCTV look is the scene grade (saturate 0) plus a low Glitch, not a per-layer filter. Presence uses the chat subtitle swap ("Gus · online" -> "Gus · last seen 2:38"). The floor counter uses ElevatorPanel `from 5 to 16` with `perFloor` fitted to the spoken "five ... sixteen" and `floors: 20` (so a 19 button exists and the camera frames the display).
- **SFX:** `desk_ring` is a real file now (synthesized offline on the Spark: `ffmpeg -f lavfi aevalsrc` two sines 440/480 Hz x a 20 Hz trill, band-passed 300-3400 Hz, 2.0 s ring + 0.4 s tail, `-threads 2`, nice 10), so nothing is pitch-shifted at runtime.
- **Posting:** upload Part 2, then Part 1 within a minute. Part 2's title stands alone.
- **Policy / disclosure:** non-graphic; the figure is a back view and nobody is hurt on screen. Invented building, owner, phone numbers (555-01xx fiction range) and company. The messenger UI is the generic kit UI. Each part is >= 61 s (Creator Rewards) and < 3 min (Shorts). Description line: "Original fiction · synthetic narration (Kokoro TTS) · code-animated". Set TikTok's AI-generated content toggle conservatively for the synthetic voice; YouTube's altered/synthetic label targets realistic content, so it is likely not required for this stylized animation (see research R5 disclosure block). "The Calloway" names no city or address.
- **Narration contract:** every chat message read aloud appears in a bubble with the same words (digits shown as digits: "Rule 1" for "Rule one"). Part 2's closing bubbles repeat `lines.RULES` exactly, except rule 3 (`lines.RULE3_NEW`).
- **TTS:** "nineteen-oh-three", "two forty-one" and "nine-one-one" are spelled out; captions show 1903 / 2:41 / 911 through the `cap` maps. "Mr." is sent to Kokoro as "Mister", "a.m." as "A M".
