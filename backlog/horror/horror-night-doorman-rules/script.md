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
runtime_s: {part1: 112.4, part2: 120.0}   # MEASURED: Kokoro-82M on the Spark CPU, per line (tts_durations.json)
words: {part1: 473, part2: 508}
wpm_overall: {part1: 252.6, part2: 254.0}   # words / runtime; PLAYBOOK §7 narrated band 230-270
wpm_speaking: {part1: 284.9, part2: 282.9}   # words / speech time (pauses and holds excluded)
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
| Runtime | 165-250 s story, or 2 x ~120 s; each part >= 61 s (Creator Rewards) | 112.4 s | 120.0 s |
| Words / wpm overall | 230-270 narrated | 473 / 252.6 | 508 / 254.0 |
| wpm while speaking | (refs 262-366) | 284.9 | 282.9 |
| Core hook | <= 30 words, <= 6-7 s | 28 words / 6.58 s (lines 1-2) | 24 words / 5.8 s (q1-q2) + the voice line (10 words) ends at 9.1 s |
| Trusted source contradicted | <= 11 s | 5.4 s (owner's text ordered the rule broken; banner on screen) | 7.1 s (the voice: "it isn't me") |
| Words in the first 10 s | median 43.5 | 43 | 39 |
| Jolt interval | median 6 s, never > 25 s dry | median 2.72 s, longest gap 6.96 s (40 jolts) | median 2.48 s, longest gap 5.15 s (45 jolts) |
| Intrusion at the barrier (B3) | ~6% | 0:15 = 13% (rule 1 broken), the building answers 0:17.5 = 16% (the owner's banner is on screen at 0:05 = 5%) | 0:05 = 4% (picks up the 1903 line) |
| First proof (B4) | 8-20% | 0:17.5 = 16% (elevator comes down by itself) | 0:24 = 20% (paper vs the texting number) |
| Midpoint turn | 45-60% | 0:53.9-0:59.8 = 48-53% (the owner's order + rule 5) | 1:00.4 = 50% (rule 3 inverted) |
| Scariest image, held | once, 60-82%, ~4 s still | 1:20.3-1:30.5 = 71-80%, hold 3.8 s at 77-80% with one change (the door gap widens) | 1:28.7-1:36.7 = 74-81%, hold 4.0 s at 77-81% |
| Lifeline under a clock | 70-90% | 1:36.6 = 86% (security: next patrol 6 AM) | 1:36.7 = 81% (4% battery, 911 fails) |
| Truth twist | 85-95% | 1:13.6 = 65% (number "never his": early variant) | 1:43.0 = 86% ("Thanks, kid. Your shift now."), resolved 1:46 = 88% |
| Plants for next part | >= 2 unpaid | 96 hooks / 95 keys, 1903's empty hook, 19, 2:41, yellow tape, "how did he know?" | pays tape + line at 0:29 (24%), 96th key at 0:42 (35%), 2:41 at 0:57 (47%) |
| Loops open at the cut | 3-6 (series) | 5 (who is the man in the blazer, who is Pell, why 2:41, where is Gus, will she pick up) | 3 (is Lena the new thing in 1903, will Marcus obey, who/what texts as Pell) |
| Numbers per minute | 3-5 (narrated 2.2-5.8) | 5.3 (distinct: 1903, 31 years, six rules, 1 AM, 19, 95, 96th, 2:41, 24 hours, 6 AM) | 6.0 (distinct: 1903, 3 AM, 95, 96th, 93-94-95 count, 19, 2:41, five (minutes), 5-9-13-16 floors, 4%, 911, seven) |
| Sentence median / punch share | 6-9 words / 13-22% | 6.0 / 27% (chat bubbles such as "Go up now." count) | 7 / 25% |
| Questions | 3.3/min median | 4 (2.1/min) | 2 (1.0/min): "So which Gus was in my chat?" (0:18), "How?" (1:24) |
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
Rule three of my night desk. If nineteen-oh-three calls, send nobody up. Nineteen-oh-three is empty.

Tonight I broke rule three. A text from the owner ordered me to.

The concierge before me, Gus, had that desk for thirty-one years. Last night was his last shift.

We never met, but he added me to a chat called Desk Handover, with six rules.

I only read rule three. So at one, when the lobby got stuffy, I propped the glass door open.

Behind me, the elevator started coming down by itself, from nineteen.

Gus texted: Shut the door. Rule one, never open the glass doors after one.

How did he know? He wasn't even in the building.

I kicked the door shut, but the elevator kept coming, and it opened on the lobby with nobody inside.

Gus: Rule two. If the elevator comes down empty, don't get in.

So I stayed in my chair. Inside the car, the button for nineteen was already lit.

And the doors stayed open, waiting, until I looked away. Then it climbed straight back to nineteen.

One small rule broken, and the building answered in seconds. After that, I read every rule twice.

Rule four was about the key board behind me. At three, count the keys: ninety-five, and if there's a ninety-sixth, don't touch it.

And on the desk phone, the button for nineteen-oh-three had a strip of yellow tape over it. Old tape, curling at one corner.

At two forty-one, the work phone buzzed. A text from a contact already saved as Mr. Pell, owner.

Nineteen-oh-three needs help. Go up now.

Rule five. If Mr. Pell, the owner, texts you, do what he says.

So rule five said go up, and rule three said nobody goes up. The same man wrote both. One of them had to be wrong.

I asked Gus which rule wins. He started typing. Stopped. Started again.

[pause: 1.1]

Gus: What number texted you?

I sent him a screenshot.

That number was never his.

So neither rule was wrong. The number was.

Gus: Don't go up. Don't send anyone.

I typed, and if nineteen-oh-three calls? And he didn't answer.

I checked the camera monitor. On nineteen, the door to nineteen-oh-three was open a crack, and a man in a concierge blazer stood beside it, facing the wall.

[pause: 3.8]

Then Pell again. Gus doesn't work here anymore. Ask him why he left at two forty-one last night.

Two forty-one, the exact same minute, twenty-four hours ago.

I called building security and got a recording. Next patrol, six a.m.

I typed to Gus, why did you leave? And his little green dot went grey.

Then the desk phone made a sound I'd never heard it make. Under the yellow tape, a light was glowing red.

[pause: 1.4]

It was line nineteen-oh-three, and Gus's dot flicked back to green.

Let it ring.

[pause: 1.3]
```

### Timed script (measured)

| t | dur | VO / caption | Beat | On screen |
|---|---|---|---|---|
| 0:00.1 | 4.00 | Rule three of my night desk. If nineteen-oh-three calls, send nobody up. Nineteen-oh-three is empty. | B1 | FRAME 0 = COVER: desk-phone close-up, the 1903 button under yellow tape glowing bright red through it; the propped work phone shows the Desk Handover chat with the rule-3 bubble enlarged ("1903" in an alert bubble) |
| 0:04.3 | 2.29 | Tonight I broke rule three. A text from the owner ordered me to. | B1 | Lock-screen banner flash: "Mr. Pell (Owner) · Go up now." (snap zoom, glitch) |
| 0:06.7 | 3.79 | The concierge before me, Gus, had that desk for thirty-one years. Last night was his last shift. | B2 | Lobby wide: glass doors, marble desk, elevator behind; Lena small at the desk. Chat header "Desk Handover · 2 members", system line "Gus Brandt · Night Desk · 31 yrs" |
| 0:10.7 | 2.96 | We never met, but he added me to a chat called Desk Handover, with six rules. | B2 | Banner "Gus added you to Desk Handover"; Gus: "6 rules. Read them twice." then the six rule bubbles stack in fast |
| 0:13.8 | 3.57 | I only read rule three. So at one, when the lobby got stuffy, I propped the glass door open. | B3 | Desk clock 1:04; the glass door swings open onto the dark street, wastebasket as a wedge |
| 0:17.5 | 2.54 | Behind me, the elevator started coming down by itself, from nineteen. | B3 | Elevator floor display counting down 19 > 18 > 17 (nobody pressed it) |
| 0:20.2 | 3.22 | Gus texted: Shut the door. Rule one, never open the glass doors after one. | B3 | Gus: "Shut the door. Rule 1, never open the glass doors after 1." (rule-1 pinned bar highlighted) |
| 0:23.6 | 1.60 | How did he know? He wasn't even in the building. | B3 | Lena CU, suspicious, looking up at the ceiling |
| 0:25.4 | 3.91 | I kicked the door shut, but the elevator kept coming, and it opened on the lobby with nobody inside. | B4 | Door bolt flash; elevator doors slide open on an empty lit car |
| 0:29.4 | 2.49 | Gus: Rule two. If the elevator comes down empty, don't get in. | B4 | Rule-2 bubble pops: "2. If the elevator comes down empty, don't get in." |
| 0:32.1 | 3.43 | So I stayed in my chair. Inside the car, the button for nineteen was already lit. | B4 | Car panel insert: button 19 glowing orange, nobody inside |
| 0:35.7 | 3.77 | And the doors stayed open, waiting, until I looked away. Then it climbed straight back to nineteen. | B4 | Doors hold open (no timer runs out); the moment the camera cuts to Lena looking down, the doors close; display climbs to 19 |
| 0:39.6 | 3.89 | One small rule broken, and the building answered in seconds. After that, I read every rule twice. | B4 | Chat pulls out to show all six rule bubbles; ticks appear beside 1 and 2 |
| 0:43.7 | 5.24 | Rule four was about the key board behind me. At three, count the keys: ninety-five, and if there's a ninety-sixth, don't touch it. | B7 | Key board: 96 numbered hooks, 95 keys, one empty hook; rule-4 bubble "4. At 3, count the keys. 95. If there's a 96th, don't touch it." |
| 0:49.1 | 4.66 | And on the desk phone, the button for nineteen-oh-three had a strip of yellow tape over it. Old tape, curling at one corner. | B7 | Desk-phone close-up: rows of unit buttons "1901 1902 [tape] 1904"; the tape's curled corner |
| 0:53.9 | 4.17 | At two forty-one, the work phone buzzed. A text from a contact already saved as Mr. Pell, owner. | B8 | Desk clock 2:41; new thread "Mr. Pell (Owner)" with a saved-contact card |
| 0:58.2 | 1.44 | Nineteen-oh-three needs help. Go up now. | B8 | Pell: "1903 needs help. Go up now." |
| 0:59.8 | 2.52 | Rule five. If Mr. Pell, the owner, texts you, do what he says. | B8 | Rule-5 bubble highlighted: "5. If Mr. Pell, the owner, texts you, do what he says." |
| 1:02.5 | 4.57 | So rule five said go up, and rule three said nobody goes up. The same man wrote both. One of them had to be wrong. | B8 | Whip between the rule-5 and rule-3 bubbles, both highlighted |
| 1:07.2 | 3.01 | I asked Gus which rule wins. He started typing. Stopped. Started again. | B8 | Me: "The owner says go up. Which rule wins?"; header "Gus is typing…" on, off, on |
| 1:10.3 | 1.10 | *[silence 1.1 s]* | B8 | Typing dots, no VO |
| 1:11.5 | 1.01 | Gus: What number texted you? | B8 | Gus: "What number texted you?" |
| 1:12.6 | 0.85 | I sent him a screenshot. | B8 | My screenshot bubble: the Pell contact card, number visible (it will not match the staff sheet in Part 2) |
| 1:13.6 | 0.92 | That number was never his. | B8 | Gus: "That number was never his." (glitch, shake) |
| 1:14.6 | 1.51 | So neither rule was wrong. The number was. | B8 | Lena CU, shocked |
| 1:16.3 | 1.36 | Gus: Don't go up. Don't send anyone. | B8 | Gus: "Don't go up. Don't send anyone." |
| 1:17.8 | 2.28 | I typed, and if nineteen-oh-three calls? And he didn't answer. | B8 | Me: "and if 1903 calls?" (delivered, no reply) |
| 1:20.3 | 6.28 | I checked the camera monitor. On nineteen, the door to nineteen-oh-three was open a crack, and a man in a concierge blazer stood beside it, facing the wall. | B9 | Monitor: 2x3 CCTV grid, zoom into "CAM 19-E"; grey hallway, 1903's door ajar, a back-view man in a navy blazer facing the wall beside it |
| 1:26.7 | 3.80 | *[silence 3.8 s]* | B9 | HELD 3.8 s, music out: the dark gap of 1903's door widens slowly while the man does not move |
| 1:30.5 | 3.62 | Then Pell again. Gus doesn't work here anymore. Ask him why he left at two forty-one last night. | B9 | Pell: "Gus doesn't work here anymore. Ask him why he left at 2:41 last night." |
| 1:34.2 | 2.21 | Two forty-one, the exact same minute, twenty-four hours ago. | B9 | Desk clock 2:41 in red, then "-24 h" |
| 1:36.6 | 2.91 | I called building security and got a recording. Next patrol, six a.m. | B10 | Call screen "Calloway Security · recording"; "Next patrol 6:00 AM" |
| 1:39.7 | 2.74 | I typed to Gus, why did you leave? And his little green dot went grey. | B10 | Me: "why did you leave?"; Gus's header goes from "online" to "last seen 2:38" |
| 1:42.6 | 3.96 | Then the desk phone made a sound I'd never heard it make. Under the yellow tape, a light was glowing red. | B12 | Lobby wide, lights dip; then the desk-phone ECU, red light through the tape |
| 1:46.6 | 1.40 | *[silence 1.4 s]* | B12 | Ring; LCD "LINE 1903"; no VO |
| 1:48.0 | 2.47 | It was line nineteen-oh-three, and Gus's dot flicked back to green. | B12 | Gus's header: "online"; typing dots |
| 1:50.7 | 0.42 | Let it ring. | B12 | Gus: "Let it ring." Push past it to the rule-3 bubble over the red-lit button (frame-0 framing); card "PART 1/2" |
| 1:51.1 | 1.30 | *[silence 1.3 s]* | B12 | Hold the bookend; hard cut to black |

### Scene list (storyboard.json)

| scene | start | end | notes |
|---|---|---|---|
| s01_cover | 0.00 | 5.40 | FRAME 0 = COVER: the red light glows bright through the yellow tape on 1903's button (brighter than the story has it, for the grid); the rule-3 bubble as a red card. Punch-in on the tape on 'Nineteen-oh-three is empty'. |
| s02_order | 5.40 | 6.74 | Flash-forward contradiction by 6 s: the owner's text orders rule 3 broken. |
| s03_setup | 6.74 | 10.68 | The Calloway lobby (glass doors, desk, elevator, key board); then the only contact: a system card for Gus. |
| s04_rules | 10.68 | 13.81 | Six bubbles stack in fast on 'six rules' (one pop each); rule 3 is the red alert bubble. |
| s05_break | 13.81 | 17.54 | B3 at ~13%: a minor rule broken before she has read it (HEARSE-P1 0:31). The glass door swings open on 'propped'. |
| s06_answer | 17.54 | 20.24 | Something visibly answers: the display counts down from 19 with nobody pressing it. |
| s07_gus_knows | 20.24 | 23.62 |  |
| s08_how | 23.62 | 25.38 | Plant: Gus knew. He is in the building (Part 2: his phone is in 1903). |
| s09_empty | 25.38 | 29.45 |  |
| s10_rule2 | 29.45 | 32.10 |  |
| s11_lit | 32.10 | 35.69 | Rule 2 earns 'true': the car's panel already has 19 lit (wrong detail). |
| s12_waits | 35.69 | 39.62 | The doors hold open until she looks down; the cut back finds them closed and the display climbing to 19. |
| s13_twice | 39.62 | 43.67 | Verdict line; the pull-out shows all six rules on screen (rules 4-6 are read just in time later). |
| s14_keys | 43.67 | 49.08 | Plant: 96 hooks (24 floors x 4), 95 keys; the empty hook is 1903's. The push ends on it. |
| s15_tape | 49.08 | 53.89 | Plant: the yellow tape, old, curling at one corner. No light yet. |
| s16_pell | 53.89 | 58.22 | MIDPOINT ~49%: a contact already saved as the owner. |
| s17_goup | 58.22 | 59.82 |  |
| s18_rule5 | 59.82 | 62.50 |  |
| s19_collide | 62.50 | 67.24 | Two rival authorities in one list (DORM-RULES engine): obey the owner vs send nobody. |
| s20_typing | 67.24 | 71.45 |  |
| s21_number | 71.45 | 73.56 |  |
| s22_never | 73.56 | 74.63 |  |
| s23_numberwas | 74.63 | 76.31 |  |
| s24_dontgo | 76.31 | 80.27 |  |
| s25_monitor | 80.27 | 81.51 | Monitor: 2x3 CCTV grid; digital zoom into CAM 19-E. |
| s26_peak | 81.51 | 90.45 | B9 HELD IMAGE (3.8 s still, music out): 1903 open a crack, a back-view man in a concierge blazer facing the wall beside it. During the hold the dark gap of the door widens (the one change in frame). |
| s27_taunt | 90.45 | 94.23 |  |
| s28_match | 94.23 | 96.60 |  |
| s29_security | 96.60 | 99.67 |  |
| s30_grey | 99.67 | 102.56 | B6 isolation: the presence line goes from 'online' to 'last seen 2:38'. |
| s31_sound | 102.56 | 104.68 | Sound before visual (TRUCKER 1:45): one distorted ring; lights dip. |
| s32_redlight | 104.68 | 109.19 | The red light through the tape (pays the P1-7 plant), ring on the silence. |
| s33_green | 109.19 | 110.65 |  |
| s34_cliff | 110.65 | 112.37 | B12: a fresh imperative ('Let it ring.' was never said before), then the frame-0 framing as the bookend + PART 1/2. |

---

## Part 2/2: "The Desk Phone Rang From the Empty Apartment"

**Hook.** First line (VO, 0:00): "Our front desk phone was ringing from nineteen-oh-three." First visual (frame 0, also the cover): the desk phone ringing, the red light pulsing through the tape, LCD "LINE 1903 · CALLING". Cover text: **1903 IS EMPTY. IT'S CALLING.**

### Narration (VOICE = bm_george)

```narration
Our front desk phone was ringing from nineteen-oh-three. My handover rules swore nineteen-oh-three was empty.

Gus said let it ring, and I picked up.

VOICE: Kid, it's Gus. Whatever's in that chat, it isn't me.

Then a click, and the line went dead.

Then the handover chat buzzed. Gus: That wasn't me on the phone. I'm home in bed. Don't pick up again.

Then the owner, Pell: Gus never came home last night. Go up.

Two Guses and one owner. So which Gus was in my chat? Somebody was lying to me.

Under the desk there's a laminated staff sheet. It's paper, and nobody can edit paper.

Mr. Pell's real number was on it. It wasn't the number that had been texting me.

Gus's cell was on it too, so I dialed it.

It rang, and at the exact same second, under the yellow tape, line nineteen-oh-three lit up.

His phone was up there, so the Gus in my chat lied too. He wasn't home in bed.

At three a.m., rule four: count the keys. Ninety-five, and if there's a ninety-sixth, don't touch it.

Ninety-three. Ninety-four. Ninety-five.

[pause: 0.6]

Ninety-six.

The extra key had a brass tag that said nineteen-oh-three.

Behind me, the elevator chimed. It had come down from nineteen, empty, and it held its doors open for me.

The key, the elevator, the owner. Everything in this building was pointing up.

I opened the visitor log so my hands had something to do. Gus's last entry was from last night.

Two forty-one, nineteen-oh-three called, going up myself, back in five.

He never signed back in.

That's when I got it. Rule three says send nobody up, so Gus didn't send anybody. He went himself.

And rule three is why nobody ever went up after him.

Pell lied about everything else, but he was right about one thing. Somebody had to go up.

I took the ninety-sixth key, rule four. I got into the empty elevator, rule two.

I left the desk before seven, rule six. And I sent somebody up. Me. Rule three.

The chat lit up. Gus: Put the key back, please. Nobody means you too.

Five, nine, and at thirteen the lights dipped. At sixteen my signal died, but the chat kept working. How?

Gus: If I'm standing up there, it isn't me.

At nineteen, the doors opened on a hallway with one light on.

At the far end, outside nineteen-oh-three, a man in a concierge blazer stood with his face to the wall.

[pause: 4.0]

Four percent battery and no signal. I dialed nine-one-one anyway, and the call failed.

He didn't turn around. He just said, softly, in Gus's voice:

VOICE: Thanks, kid. Your shift now.

Then the hallway light went out.

The chat buzzed one last time. Gus: I'm sorry. I lied so you wouldn't come.

Then the handover chat added a new member, Marcus from the day shift. And a message started sending, from me.

The same six rules, word for word, except rule three. If nineteen-oh-three calls, send nobody up. Even if it sounds like me.

[pause: 1.2]
```

### Timed script (measured)

| t | dur | VO / caption | Beat | On screen |
|---|---|---|---|---|
| 0:00.1 | 4.03 | Our front desk phone was ringing from nineteen-oh-three. My handover rules swore nineteen-oh-three was empty. | B1 | FRAME 0 = COVER: desk-phone ECU, red light through the yellow tape, LCD "LINE 1903 · CALLING"; behind it the work phone with the rule-3 bubble |
| 0:04.3 | 1.28 | Gus said let it ring, and I picked up. | B1 | Gus's bubble "Let it ring." on the propped phone; Lena lifts the receiver |
| 0:05.9 | 3.21 | **VOICE:** Kid, it's Gus. Whatever's in that chat, it isn't me. | B1 | Lena CU, receiver to her ear; LCD "1903 · 00:04" (line hiss) |
| 0:09.4 | 1.22 | Then a click, and the line went dead. | B1 | LCD "LINE DROPPED"; the red light snaps off |
| 0:10.8 | 4.07 | Then the handover chat buzzed. Gus: That wasn't me on the phone. I'm home in bed. Don't pick up again. | B5 | Gus: "That wasn't me on the phone. I'm home in bed. Don't pick up again." |
| 0:15.0 | 2.25 | Then the owner, Pell: Gus never came home last night. Go up. | B5 | Thread "Mr. Pell (Owner)": "Gus never came home last night. Go up." |
| 0:17.4 | 3.34 | Two Guses and one owner. So which Gus was in my chat? Somebody was lying to me. | B5 | Lena CU, eyes left / right |
| 0:20.9 | 3.34 | Under the desk there's a laminated staff sheet. It's paper, and nobody can edit paper. | B4 | Tilt down under the desk: a laminated sheet "CALLOWAY STAFF · EMERGENCY CONTACTS" in phone-torch light |
| 0:24.4 | 2.90 | Mr. Pell's real number was on it. It wasn't the number that had been texting me. | B4 | Sheet row "R. Pell (Owner)" with a number; side by side with the Pell contact card: the numbers differ (red strike on the contact) |
| 0:27.5 | 1.56 | Gus's cell was on it too, so I dialed it. | B4 | Row "G. Brandt (Night) · cell" highlighted; call screen "Gus Brandt · calling…" |
| 0:29.2 | 3.58 | It rang, and at the exact same second, under the yellow tape, line nineteen-oh-three lit up. | B4 | Split screen: work phone "calling…" / desk-phone 1903 light, pulsing together |
| 0:32.9 | 2.93 | His phone was up there, so the Gus in my chat lied too. He wasn't home in bed. | B4 | Gus's bubble "I'm home in bed." edited to red: "I'm home in bed. ✕" |
| 0:36.0 | 3.99 | At three a.m., rule four: count the keys. Ninety-five, and if there's a ninety-sixth, don't touch it. | B5b | Desk clock 3:00; rule-4 bubble "4. At 3, count the keys. 95. If there's a 96th, don't touch it."; key board |
| 0:40.2 | 1.43 | Ninety-three. Ninety-four. Ninety-five. | B5b | Count overlay 93 · 94 · 95, one hook lighting per count |
| 0:41.6 | 0.60 | *[silence 0.6 s]* | B5b | Near-black beat, one brass glint |
| 0:42.2 | 0.53 | Ninety-six. | B5b | "96" in red; the extra key swings on hook 96 |
| 0:42.9 | 1.98 | The extra key had a brass tag that said nineteen-oh-three. | B5b | Brass tag "1903" ECU |
| 0:45.0 | 4.34 | Behind me, the elevator chimed. It had come down from nineteen, empty, and it held its doors open for me. | B5b | Lena turns; the elevator doors open on an empty lit car; button 19 lit inside |
| 0:49.6 | 2.74 | The key, the elevator, the owner. Everything in this building was pointing up. | B5b | Triptych: brass tag / open car / Pell bubble, each pops on its word; arrows up |
| 0:52.5 | 3.94 | I opened the visitor log so my hands had something to do. Gus's last entry was from last night. | B7 | Visitor log, pages turning back to yesterday |
| 0:56.6 | 2.71 | Two forty-one, nineteen-oh-three called, going up myself, back in five. | B7 | Handwriting writes on: "2:41 – 1903 called. Going up myself. Back in five. –G" |
| 0:59.4 | 0.79 | He never signed back in. | B7 | The empty TIME IN cell |
| 1:00.4 | 4.10 | That's when I got it. Rule three says send nobody up, so Gus didn't send anybody. He went himself. | B8 | Lena CU, shocked to angry; rule-3 bubble over her |
| 1:04.6 | 2.07 | And rule three is why nobody ever went up after him. | B8 | Rule-3 bubble: "send nobody up" glows red |
| 1:06.9 | 3.15 | Pell lied about everything else, but he was right about one thing. Somebody had to go up. | B8 | Pell's "Go up now." bubble; Lena stands |
| 1:10.2 | 3.24 | I took the ninety-sixth key, rule four. I got into the empty elevator, rule two. | B5c | Hook 96 empties; stamp "4 ✕ the 96th key"; elevator doors; stamp "2 ✕ rode it empty" |
| 1:13.6 | 3.32 | I left the desk before seven, rule six. And I sent somebody up. Me. Rule three. | B5c | Empty desk, chair turning; stamp "6 ✕ left the desk"; then the big red stamp "3 ✕ sent somebody up: me" |
| 1:17.1 | 2.72 | The chat lit up. Gus: Put the key back, please. Nobody means you too. | B5c | Gus: "Put the key back, please. Nobody means you too." |
| 1:19.9 | 4.40 | Five, nine, and at thirteen the lights dipped. At sixteen my signal died, but the chat kept working. How? | B5c | Floor display 5 > 9 > 13 (light dip) > 16 (status bar "No Service"); the chat still delivers |
| 1:24.5 | 1.53 | Gus: If I'm standing up there, it isn't me. | B5c | Gus: "If I'm standing up there, it isn't me." |
| 1:26.2 | 2.38 | At nineteen, the doors opened on a hallway with one light on. | B9 | Display 19; doors part on the hallway |
| 1:28.7 | 3.88 | At the far end, outside nineteen-oh-three, a man in a concierge blazer stood with his face to the wall. | B9 | Hallway, one light; door plate 1903 ajar; the back-view blazer man beside it, facing the wall |
| 1:32.7 | 4.00 | *[silence 4.0 s]* | B9 | HELD 4.0 s, music out, heartbeat only; slow push 1.00 > 1.04 |
| 1:36.7 | 3.40 | Four percent battery and no signal. I dialed nine-one-one anyway, and the call failed. | B10 | Battery 4% red; call "911 · Call failed" |
| 1:40.2 | 2.46 | He didn't turn around. He just said, softly, in Gus's voice: | B11 | Hallway, very slow push; no lip flap |
| 1:43.0 | 1.71 | **VOICE:** Thanks, kid. Your shift now. | B11 | Caption only; the man stays facing the wall |
| 1:45.0 | 0.99 | Then the hallway light went out. | B11 | Black; phone glow from below on Lena |
| 1:46.2 | 2.91 | The chat buzzed one last time. Gus: I'm sorry. I lied so you wouldn't come. | B11 | Gus: "I'm sorry. I lied so you wouldn't come." |
| 1:49.2 | 4.24 | Then the handover chat added a new member, Marcus from the day shift. And a message started sending, from me. | B12 | Banner "Marcus (Day Desk) joined Desk Handover"; header "3 members"; my outgoing bubble with a sending spinner |
| 1:53.6 | 5.07 | The same six rules, word for word, except rule three. If nineteen-oh-three calls, send nobody up. Even if it sounds like me. | B12 | Rules 1, 2, 4, 5, 6 stack in exactly as in Part 1, sent by Lena; last bubble: "3. If 1903 calls, send nobody up. Even if it sounds like me."; card "END · PART 2/2" |
| 1:58.8 | 1.20 | *[silence 1.2 s]* | B12 | Faint ring of line 1903 under the bookend; hard cut |

### Scene list (storyboard_p2.json)

| scene | start | end | notes |
|---|---|---|---|
| t01_cover | 0.00 | 2.21 | FRAME 0 = COVER: the desk phone ringing from 1903, red light through the yellow tape, LCD 'LINE 1903 · CALLING'. |
| t02_rule | 2.21 | 4.31 |  |
| t03_pickup | 4.31 | 5.89 | She defies Gus's last order: 'Let it ring.' -> picked up. |
| t04_voice | 5.89 | 9.40 | Contradiction at ~8 s: the voice (bm_george) says the chat isn't him. Re-watch clue: only this voice says 'kid'. |
| t05_dead | 9.40 | 10.78 |  |
| t06_chat | 10.78 | 15.01 |  |
| t07_pell | 15.01 | 17.42 |  |
| t08_which | 17.42 | 20.92 |  |
| t09_sheet | 20.92 | 24.42 | B4 outside check (HEARSE-P2 1:36): paper nobody can edit. |
| t10_mismatch | 24.42 | 27.48 | Pays rule 5: the rule was real, the contact was swapped (555-0178 on paper vs 555-0143 texting). |
| t11_dial | 27.48 | 29.20 |  |
| t12_sync | 29.20 | 32.95 | Two lights flash together: Gus's cell rings in 1903. |
| t13_lied | 32.95 | 36.04 |  |
| t14_rule4 | 36.04 | 40.19 |  |
| t15_count | 40.19 | 42.23 |  |
| t16_96 | 42.23 | 45.05 | Part-1 plant paid at ~33% (key 96 on the empty hook, tag 1903). |
| t17_elevator | 45.05 | 49.55 |  |
| t18_up | 49.55 | 52.45 |  |
| t19_log | 52.45 | 56.55 |  |
| t20_entry | 56.55 | 59.43 | B7 paper plant: Gus went up at 2:41 (pays the Part-1 2:41 match). |
| t21_timein | 59.43 | 60.38 |  |
| t22_reframe | 60.38 | 64.64 | B8 MIDPOINT ~51%: rule 3 inverted. 'Send nobody up' is why Gus went himself, and why nobody followed. |
| t23_nobody | 64.64 | 66.87 |  |
| t24_somebody | 66.87 | 70.18 | Ties the ascent to the owner's order (the hook's promise). |
| t25_breaks | 70.18 | 73.58 | Rule-break ladder: each rule named with its content as it breaks. |
| t26_rule3 | 73.58 | 77.06 | The title rule is named as it breaks, biggest stamp of the ladder (the loudest hit). |
| t27_putback | 77.06 | 79.94 |  |
| t28_floors | 79.94 | 84.49 | Channel removal: lights dip at 13, signal dies at 16, only the chat still works (SIEGE-CHAT 2:03-2:11). |
| t29_notme | 84.49 | 86.18 |  |
| t30_nineteen | 86.18 | 88.72 |  |
| t31_peak | 88.72 | 96.69 | B9 HELD IMAGE (4.0 s, music out): the same composition as Part 1's CCTV peak, now in colour, in person, closer. |
| t32_911 | 96.69 | 100.25 | B10: the outside lifeline, 4% battery, fails. |
| t33_kid | 100.25 | 105.02 | B11 TWIST ~86%: 'Thanks, kid. Your shift now.' in the line voice (bm_george); he never turns, no lip flap. |
| t34_out | 105.02 | 106.16 |  |
| t35_sorry | 106.16 | 109.24 | Resolves the identity knot: the chat was the real Gus, lying to keep her away. |
| t36_marcus | 109.24 | 113.64 |  |
| t37_bookend | 113.64 | 120.01 | B12 new rule from a new authority: the same six rules, sent from Lena; rule 3 rewritten. Bookends Part 1's frame-0 rule. |

## Production notes

- **Build:** `python3 build.py` (stdlib, Mac-safe) rebuilds timeline.json, storyboard.json (Part 1) and storyboard_p2.json (Part 2) from lines.py + tts_durations.json. After any wording change: rsync this folder to the Spark and run `CUDA_VISIBLE_DEVICES="" OMP_NUM_THREADS=4 nice -n 10 ~/studio/.venv/bin/python tts_measure.py tts_durations.json ~/studio/tts/horror-night-doorman-rules`, then copy the wavs to `studio/public/episodes/horror-night-doorman-rules/{p1,p2}/vo/` (done for this version).
- **Validation (this version):** `npm run validate` equivalent on the Spark: both storyboards ok (9:16, 30 fps, 34 + 37 scenes). `scripts/check_storyboards.py` on the Spark: all components registered, all audio present; the only flag is the deliberate held images (3.8 s and 4.0 s; the pilot's 3 s hold rule is overridden by PLAYBOOK §1A B9 "held still ~4 s"). Stills sheets were rendered on the Spark and checked: `out/stills/horror-night-doorman-rules_storyboard.jpg`, `out/stills/horror-night-doorman-rules_storyboard_p2.jpg`, plus the fix pass `out/stills/doorman_p1_fix.jpg`, `out/stills/doorman_p2_fix.jpg`.
- **Kit (locked until horror PASS, BRIEF 11:27):** no kit file was touched. The lobby, desk phone (taped 1903 button, red light, LCD), 96-hook key board, elevator doors and car, CCTV grid, staff sheet, visitor log and the back-view blazer figure are inline SVG / core layers in build.py (`lobby()`, `desk_phone()`, `keyboard()`, `elevator_view()`, `cctv_grid()`, `paper()`, `FIGURE`, `hallway_1903()`). When the kit unlocks they map 1:1 onto the producibility critique's proposed `horror/LobbyDesk` (views wide | deskphone | keys | monitor | elevator), `horror/Paper`, and Hallway props `endDoorAjar`, `endDoorLabel`, `figureFacing:'away'`, `figureX`. The CCTV look is the scene grade (saturate 0) plus a low Glitch, not a per-layer filter. Presence uses the chat subtitle swap ("Gus · online" -> "Gus · last seen 2:38"). The floor counter uses ElevatorPanel `from 5 to 16` with `perFloor` fitted to the spoken "five ... sixteen" and `floors: 20` (so a 19 button exists and the camera frames the display).
- **SFX:** `desk_ring` is a real file now (synthesized offline on the Spark: `ffmpeg -f lavfi aevalsrc` two sines 440/480 Hz x a 20 Hz trill, band-passed 300-3400 Hz, 2.0 s ring + 0.4 s tail, `-threads 2`, nice 10), so nothing is pitch-shifted at runtime.
- **Posting:** upload Part 2, then Part 1 within a minute. Part 2's title stands alone.
- **Policy / disclosure:** non-graphic; the figure is a back view and nobody is hurt on screen. Invented building, owner, phone numbers (555-01xx fiction range) and company. The messenger UI is the generic kit UI. Each part is >= 61 s (Creator Rewards) and < 3 min (Shorts). Description line: "Original fiction · synthetic narration (Kokoro TTS) · code-animated". Set TikTok's AI-generated content toggle conservatively for the synthetic voice; YouTube's altered/synthetic label targets realistic content, so it is likely not required for this stylized animation (see research R5 disclosure block). "The Calloway" names no city or address.
- **Narration contract:** every chat message read aloud appears in a bubble with the same words (digits shown as digits: "Rule 1" for "Rule one"). Part 2's closing bubbles repeat `lines.RULES` exactly, except rule 3 (`lines.RULE3_NEW`).
- **TTS:** "nineteen-oh-three", "two forty-one" and "nine-one-one" are spelled out; captions show 1903 / 2:41 / 911 through the `cap` maps. "Mr." is sent to Kokoro as "Mister", "a.m." as "A M".
