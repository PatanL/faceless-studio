---
id: horror-elevator-maintenance-chat
niche: horror
title: The Elevator Stopped and Maintenance Texted First (Part 1)
alt_titles: see titles.md (8 ranked)
format: 9:16 Short, Part 1 of 2 (title label + a "PART 2" card on the last frame; PLAYBOOK §4C warns that an unlabelled cliff underperforms, udhwkz control 0.77x)
runtime_s: 123.0 (measured, Kokoro-82M on the Spark CPU; window 115-125; over 61 s for TikTok Creator Rewards)
words: 472
wpm: 230 overall (words / full runtime, the way the corpus counts it), 268 while speaking. PLAYBOOK §7 narrated target 230-270; the translated narrated TikTok median is 281.
hook: line 1 = 10 words / 2.0 s ("At 1 a.m., my elevator stopped between six and seven."). The impossibility is spoken by 3.9 s (18 words): "Before I touched a thing, Maintenance texted me." The trusted helper is distrusted at 6.6 s ("I never saved that contact. Who is Maintenance?").
voices: NARR = Nora, af_heart 1.35 (also reads her own ME bubbles and her one live intercom line). MAINT = bm_george 1.15, calm, flat, always sentence case on screen. OMAR = am_michael 1.25 (texts). OMAR-V = am_michael 1.2 with an intercom chain (band-pass 300-3400 Hz, crackle). Last line from Omar's number = am_michael 1.0, pitch -1 st, dry (the voice swap). Every voice is already cached on the Spark. Per-line voices are measured and rendered by this folder's tts_measure.py, because pipeline/audio/tts.py (locked) does one voice per episode.
music: no score. A fan + fluorescent buzz bed, then fan only after the turn (0:57.6), silence from the lights going out (1:06.8), motor whine + sub drone for the climb (1:47.3), hallway tube buzz only after the doors open. Bed segments are in storyboard.json `_bed`.
template: pipeline/templates/horror.md (chat thread + narrator, fake-authority variant)
build: lines.py (every spoken line) -> tts_measure.py (Spark CPU) -> tts_durations.json -> gen_storyboard.py -> storyboard.json + timing.json + script_timed.md (pasted below). Every shot boundary sits 0.10 s before the word it belongs to; nothing is hand-timed.
sibling_check: TOPICS #13 (no-fourth-floor, rejected) shared the elevator; nothing here uses a banned number, a key fob or a "welcome home" line. TOPICS #9's draft "4, then 2" is dropped (it opens like the public Elevator Game). Our button order 2, 11, 5 is owned by the story: it is the controller's reset code. No passenger ever enters the car. Fake-authority voice bm_george is shared with horror-text-from-tomorrow's office, so don't post the two in the same week.
references:
  - id: 7659677578365537569
    url: https://www.tiktok.com/@udhwkz/video/7659677578365537569
    views: 376200
    outlier_score: 10.79
    why: The closest engine (PLAYBOOK §1D "locked-door siege, fake authority"). An official-sounding channel offers safety and is the threat; a count proves it has inside knowledge; the hero's channels die while the enemy's still works, and the fake authority deletes the real warning; a last lifeline to the real authority under a clock gets the opening question answered with one concrete, checkable fact; then a last notification gives an imperative. None of its plot (killer, fake cop, owners' chat, stickers, burner phone, crew) is used.
  - id: T42u5xhrq-0
    url: https://www.youtube.com/shorts/T42u5xhrq-0
    views: 868500
    outlier_score: 25.54
    why: The chat-Short timing reference (PLAYBOOK §9.3) and our format: the viewer holds the phone and the horror arrives as text. Borrowed: several lines plus a banner in the first 3 s, the stand-in asking the viewer's question and getting an unsettling reassurance, the "I can't" exit-closed beat, the turn into the hero's space near 50% with the only colour flash, the two unanswered name checks (calm, then CAPS), the single held image as proof, and the voice swap (the trusted person's own channel speaks calmly as the entity, with the threat on "you"). Stretched from 60 s to 123 s with narration.
  - id: 7694996216505060641
    url: https://www.tiktok.com/@udhwkz/video/7694996216505060641
    views: 613300
    outlier_score: 17.6
    why: The corpus's only elevator story (same set, same narrated 9:16 format) and the best model of a mundane routine that turns wrong inside 4 s. Borrowed: the in-motion elevator hook with one wrong detail, the rational decoy offered early (a jammed car), the home-floor number used as a forcing detail, rhetorical questions that restate the master question, the dead air before the kicker, and the hard cut with the master question unanswered. Its forbidden-phrase engine, floor question, strangers and family ending are not used (its own §3 do-not-use list).
---

# The Elevator Stopped and Maintenance Texted First (Part 1)

**Premise.** At 1 a.m. Nora's elevator, car 2, stops between six and seven. Before she touches anything, a contact called
"Maintenance", one she never saved, texts her by name: don't look at the mirror. It says it is watching her on the car's
camera, whose light is off, and gives four numbered rules: press 2, 11, 5; hold Close until the lights dim; never press
the alarm; don't step out until you see your number (hers is a red nine painted on the landing wall). Each button brings
something closer: a drop, a weight settling on the roof, one tap on the mirror behind her. Nora texts the after-hours
number on the inspection card. Omar, the only maintenance man on call, says 2-11-5 is the car's reset code that only his
office has, and that car 2's camera has been dead since Tuesday: who is she talking to? Maintenance answers inside his
thread. When the lights die, her texts stop being delivered, his promise of the door key is deleted, and Maintenance's
messages still arrive. In the steel doors she sees the mirror behind her holding her own face, calm, where the back of
her head should be. One bar comes back with one text: press the alarm, and the intercom opens for ten seconds. She
breaks the rule. Omar is on nine, right in front of car 2: doors open, lights on, nobody inside. The line dies.
Maintenance: "You shouldn't have done that." The car climbs, the doors open on a wall with no number, the mirror is tapped
twice, and a text arrives from Omar's number: "Don't turn around, Nora. Step out." She never told Omar her name.

**Ownable signature:** a "Maintenance" contact that knows the car better than the building does: its button order is the
controller's reset code, and it can delete the real maintenance man's messages. The mirror on the back wall of car 2 (the
thing she must not look at) taps once at 0:37.1 and twice at 1:57.0.

**Countable plants (all paid):**
- the button order 2, 11, 5 (rule one, 0:17.0; pressed 0:31.7-0:36.1; paid at 0:51.3: "That's the reset code for car 2. Only my office has it." That is the SIEGE-CHAT count-match register: the false authority's instructions prove inside knowledge);
- my floor, a red nine painted across from the doors (0:27.4; paid twice: Omar is on nine at an empty car 2 at 1:39.7, and the landing at 1:50.6 has no number);
- rule four, "Don't step out until you see your number" (0:24.8; broken promise at 1:50.6, and the last order at 1:59.0 tells her to step out anyway);
- the camera with its light off (0:15.2; confirmed dead since Tuesday at 0:54.3);
- the after-hours number on the inspection card (on screen from 0:17.0 in the rules close-up; used by Nora at 0:41.2);
- the two red dashes on the counter (visible in every panel shot from frame 0; paid at 1:46.8, "The display stayed on two dashes.");
- "One of them knew my name" (1:04.3; paid by the last line, "I never told Omar my name.").

**Rules (from the wrong authority), numbered so viewers can count violations:**
- don't look at the mirror (the first text, 0:04.1): broken by accident through the door reflection at 1:14.2, punished at 1:23.6 ("I told you not to look.");
- One, press 2, then 11, then 5: kept;
- Two, hold Close until the lights dim: kept (the light steps down three times from 0:40.8);
- Three, never press the alarm: broken on purpose at 1:34.1. The punishment comes from Maintenance's side, "You shouldn't have done that." at 1:45.3, then the climb. The entity acts; the real authority's advice was right but too late;
- Four, don't step out until you see your number: it can't be kept (there is no number), and the final order contradicts it.

**Loops.** Master loop, who is Maintenance: opened at 2.4 s and 6.6 s ("Who is Maintenance?"), restated at 11.2 s (how do you know my name), 56.8 s (who are you talking to), 1:04.3 (one knew my name), 1:12.9 (why do its texts still come through), and asked out loud on the lifeline at 1:37.1 ("Omar, who's been texting me?"). Partly answered (not anyone in the building, knows the reset code, controls the channel, now speaks from Omar's number), left open.
Micro loops: the camera (0:12.5 -> 0:15.2, closed; reconfirmed 0:54.3); will Omar get here (1:01.1 -> deleted 1:09.2 -> he is on nine 1:38.2, then the line dies; closed: no); the thing on the roof (0:33.5 -> it rides up at 1:47.3; open); the mirror tap (0:37.1 -> my face 1:18.4 -> twice 1:57.0); where am I if car 2 is empty on nine (1:42.4 -> open).
Open at the cut (4, series band 3-6): who or what Maintenance is; what floor this is; what is in the mirror behind me; whether Omar is still Omar. Unpaid specifics for Part 2 (≥2, PLAYBOOK §5): who outside Omar's office has the reset code; the weight that rode up on the roof; Omar's deleted message and his number now used by the entity.

## Pacing vs PLAYBOOK (all measured from timing.json)

| Metric | PLAYBOOK target | This script |
|---|---|---|
| Runtime | Shorts 50-100 s, stories 150-360 s; TOPICS asks ~120 s | 123.0 s |
| Words / wpm | narrated 230-270 (words ÷ full runtime) | 472 words, 230 wpm overall, 268 speaking |
| Hook | line 1 ≤12 words; core ≤30 words / ≤6 s; trusted source contradicted ≤11 s; threat in frame 0 | line 1 10 words / 2.0 s; impossibility spoken by 3.9 s (18 words); "Who is Maintenance?" at 7.8 s; frame 0 = the lock-screen rule banner over the stalled panel (two red dashes) with a face-height highlight in the mirror strip |
| Viewer proxy | early, unsettling reassurance | 0:11.2 "how do you know my name?" -> "I'm watching you on the camera." -> light off (0:15.2) |
| Jolt interval | median 6 s; never >8 s; tighter in the last third | median ~2.4 s (nearly every line is a rule, a number, a sound or a reply). The longest gaps are the two deliberate holds: the held image (5.2 s, 1:18.4-1:23.6) and the dead air after "No number." (3.0 s) |
| Rules | ≥2 stated, ≥1 broken, one "remember this" plant | 1 + 4 numbered rules, 2 broken (one by accident, one on purpose), 1 unkeepable; the red nine pays twice |
| Ladders | two at once | proximity/sensory (drop -> roof -> mirror tap -> my face in the mirror -> two taps behind me) and channel removal (lights -> my texts undelivered -> no service -> his text deleted -> one bar -> intercom dies -> his number taken) |
| Midpoint turn | B8 45-60% (S6 43-55%) | "Who are you talking to?" at 56.8 s (46%), with the only full-frame red flash and 1.0 s of fan-only hold |
| Isolation | B6 40-55%, only the enemy's channel works | 1:06.8-1:12.9 (54-59%): "Not delivered", "No service", his text deleted, Maintenance's banner still lands, "So why did its texts still come through?" |
| Scariest image | once, 60-80%, held ~4 s | my calm face in the mirror where the back of my head should be, 1:18.4 (64%), held 5.2 s (3.0 s of it heartbeat-only silence) |
| Name checks | S8 two unanswered, CAPS | 1:25.3 (69%): "Omar?" then "OMAR??", both "(!) Not delivered" |
| Lifeline under a clock | 70-90%, ask the opening question | 1:27.3-1:44.0 (71-85%): one bar, one text, the alarm; an INTERCOM 0:10 clock that starts on the press and reaches 0:00 exactly as the line cuts; Nora asks the master question out loud at 1:37.1 |
| Truth twist | ~89% (85-95) | the concrete fact "Doors open. Lights on. Nobody's inside." at 1:42.4 (83%, 2 points early). The voice-swap twist "Don't turn around, Nora." from Omar's number lands at 1:59.0 (97%) and is sealed by "I never told Omar my name." (98%) |
| Cliff | last ~5%, imperative, bookend | 1:57.4-2:03.0: lock-screen bookend of frame 0 (1:04 -> 1:11), an imperative with a threat on "you" from the wrong sender, a "PART 2" card, hard cut, no CTA |
| Silences | 1-3 timed, 3-8 s with SFX | two real ones of 3.0 s (the held image: heartbeat only; after "No number.": hallway buzz only) plus four beats: 1.0 s fan-only after the turn, 0.7 s bell + crackle, 0.5 s crackle dies, 0.6 s final hold |
| Numbers / min | narrated 3-5 | 11.2/min (23 spoken: 1 a.m., six, seven, car 2 x6, 2/11/5 x3, nine x2, Tuesday, five minutes, ten seconds). High on purpose: the button count is the story's evidence (count-match engine). Off-band, noted |
| Questions / min | median 3.3 | 4.4/min (9 lines with "?"), with the master question restated 6 times |
| Sentence median | narrated 6-9; chat 4-5 | 4 words, 54% punches (chat-heavy: half the lines are bubbles) |
| "You" share | first-person narrated 3-13%, dialogue-heavy 16-28% | 12% of sentences, all inside MAINT/OMAR lines |
| Phone share | pilot grammar ≤ ~40% | 39% (reaction cuts at 0:45.9, 0:53.0 and the alarm-button insert at 1:30.0) |

## Beat alignment (reference timestamps re-checked against research/corpus/horror/raw/*.txt)

| Our beat | Ours (s, %) | Reference id + timestamp | Device borrowed | How we adapt it |
|---|---|---|---|---|
| B1 hook, in motion | 0:00-0:04 (0-3%) | 7694996216505060641 0:00-0:04; T42u5xhrq-0 0:00-0:03 | a mundane elevator ride with one wrong detail in sentence 1; several lines plus the phone channel inside 3 s | the stop between floors, then the impossibility spoken by 3.9 s (help arrives first); the banner is on screen from frame 0 |
| B1 trusted source distrusted | 0:06.6 (5%) | 7659677578365537569 0:06-0:11 (official all-clear) and 0:39 (the "replied almost instantly" tell) | an official channel's reassurance the viewer distrusts at once; a timing tell | "I never saved that contact. Who is Maintenance?" The tells are speed and her name |
| B2 rational decoy | 0:08.7 (7%) | 7694996216505060641 0:15 (is the elevator breaking down) | a rational cause offered early so the real one lands harder | "Car 2 is jammed. I can get you moving." |
| Viewer proxy | 0:11.2-0:15.2 (9-12%) | T42u5xhrq-0 0:09 and 0:14-0:15; 7659677578365537569 0:18-0:19 | the stand-in asks the viewer's question and gets an unsettling reassurance; a clue that breaks a common-knowledge rule | moved up from 0:31: "how do you know my name?" -> "watching you on the camera" -> the red light is off |
| B2 numbered rules | 0:17.0-0:27.2 (14-22%) | 7659677578365537569 0:35-0:37 (pretext: please cooperate) and 1:46-1:49 (imperative + veiled consequence); PLAYBOOK B2 (numbered list, viewers count violations) | numbered imperatives from the false authority, one with a technical-sounding reason | One-Four as neon cards; "It resets the car" is the pretext; rule four turns the floor plant into a rule |
| Plants | 0:27.4-0:31.5 (22-26%) | PLAYBOOK T7 (planted identifier); 7694996216505060641 1:12 (the home floor as a forcing detail) | a hyper-specific identifier tied to the hero's home that later forces a choice | the red nine is what rule four tells her to wait for; at the cut it is missing and she is ordered out anyway. The mirror is introduced flatly (glare only, never a reflection) |
| B5 pressure ladder | 0:31.7-0:41.1 (26-33%) | 7659677578365537569 1:15-1:24 (physical rungs about 3 s apart); T42u5xhrq-0 0:31-0:33 (a sound inside my space) | rungs about 3 s apart, each closer | one rung per button: drop, roof, one tap on the mirror; "Don't look. Hold Close."; the light steps down |
| B8 hero reaches the real authority | 0:41.2-0:50.3 (34-41%) | 7659677578365537569 3:12-3:20 (the hero finds a way to reach the real authority herself) | agency: the hero makes the call | Nora texts the after-hours number on the inspection card planted on screen at 0:17 |
| B4/T2 count match | 0:51.3 (42%) | 7659677578365537569 0:19-0:28 (four stickers -> exactly four confirmers) and 1:53-1:58 (the four accounts) | a count that proves the false authority has inside knowledge | 2-11-5 is the controller's reset code; only Omar's office has it |
| B8 turn | 0:54.3-0:58.6 (44-48%) | 7659677578365537569 3:41-3:45 (the real authority contradicts the fake one); T42u5xhrq-0 0:31 (turn at ~52%) | a second, trustworthy channel says the first cannot exist | dead camera since Tuesday + "Who are you talking to?" with the only red flash |
| Rival claims + verdict | 0:58.6-1:05.9 (48-54%) | 7659677578365537569 1:43-1:51 (the admin pressures the hero by name); 0:55 (verdict line) | the false authority moves to discredit the real voice; a short verdict closes the rung | Maintenance banners inside Omar's thread: "He isn't in the building." Omar counters with a key and five minutes. Verdict: one knew my name, the other had a key |
| B6 isolation + channel control | 1:06.0-1:14.1 (54-60%) | 7659677578365537569 2:03-2:11 (no signal, red exclamation marks, "why is the chat still working?") and 2:21-2:30 (the admin deletes the warning and mutes everyone) | strip the safe channels; only the enemy's still works; the fake authority acts on the channel | lights out; "Not delivered", "No service"; Omar's door-key text becomes "This message was deleted"; Maintenance's banner still lands; "So why did its texts still come through?" |
| B9 peak contact | 1:14.2-1:25.2 (60-68%) | T42u5xhrq-0 0:54 (the one image, held, as proof); PLAYBOOK §3 silence beat | one still image after 60% that proves the threat is real, then silence | in the steel doors: my terrified reflection close, and in the mirror behind it my own face, calm, staring. 3.0 s heartbeat only. "I told you not to look." |
| S8 name checks | 1:25.3 (69%) | T42u5xhrq-0 0:53 ("Ava?" / "AVA??") | two unanswered name checks, the second in caps | "Omar?" / "OMAR??", both not delivered (the CAPS rung of the typography ladder) |
| B10 lifeline under a clock | 1:27.3-1:44.0 (71-85%) | 7659677578365537569 3:17 (one bar left), 3:24-3:37 (the hero asks the opening questions out loud), 3:33 (the 30 s battery clock) | one costly lifeline, a concrete limit, the master question asked out loud | one bar, one text; the alarm (rule three) is the only route left; the intercom stays open ten seconds and the INTERCOM clock runs in real time from the press; "Omar, who's been texting me?" |
| B11 truth twist (fact) | 1:42.4 (83%) | 7659677578365537569 3:58-4:01 (one concrete, checkable fact erases the fake story); 4:02 (the line dies at peak need) | a single checkable fact from the real authority; the lifeline cuts right after | "I'm on nine, right in front of car 2. Doors open. Lights on. Nobody's inside. So where are—" cut at 0:00 |
| B11 the entity acts | 1:45.3-1:49.2 (86-89%) | 7659677578365537569 2:21-2:30 (the false authority punishes the warning) | the punishment comes from the false authority's side, so the dilemma stays "who is Maintenance", not "who is lying" | "You shouldn't have done that." -> the car climbs; the display stays on two dashes |
| B12 dead air + plant paid | 1:50.6-1:55.7 (90-94%) | 7694996216505060641 2:20-2:25 (dead air while the trusted voice stays silent) | an unanswered silence before the kicker | the blank wall (same framing as the red-nine insert), then 3.0 s of hallway buzz |
| B12 cliff, voice swap | 1:55.7-2:03.0 (94-100%) | T42u5xhrq-0 0:56-0:58 (the trusted person's own channel speaks calmly as the entity, threat on "you"); 7659677578365537569 4:05-4:08 (last notification, imperative); 7694996216505060641 2:39-2:46 (hard cut, master question open) | voice swap + a last-notification imperative + a hard cut | two taps on the mirror; a banner from Omar's number in Omar's voice, slowed, in Maintenance's calm register: "Don't turn around, Nora. Step out."; "I never told Omar my name."; PART 2 card; lock-screen bookend of frame 0 |

## Script (timed from the Kokoro measurement)


#### B1 HOOK: stalled car, and help arrives before anyone asked (0:00.2, 0%)
- `0:00.2` NARR: At 1 a.m., my elevator stopped between six and seven.
  - On screen: Lock screen 1:04, banner 'Maintenance: Stay calm, Nora. Don't look at the mirror.' already up; blurred panel, counter on two red dashes; a pale face-height highlight in the mirror strip at the right edge
- `0:02.4` NARR: Before I touched a thing, Maintenance texted me.
  - On screen: Banner pulses once
- `0:04.1` MAINT (text): Stay calm, Nora. Don't look at the mirror.
  - On screen: Banner text, 'mirror' red in the caption
- `0:06.6` NARR: I never saved that contact. Who is Maintenance?
  - On screen: Banner opens into the 'Maintenance' thread; header 'Maintenance'

#### B2 DECOY + VIEWER PROXY (the 0:03 question asked by 0:13) (0:08.7, 7%)
- `0:08.7` MAINT (text): Car 2 is jammed. I can get you moving.
  - On screen: MAINT bubble
- `0:11.2` NARR: I typed: how do you know my name?
  - On screen: keyboard ticks; ME bubble 'how do you know my name?' pops on 'name'
- `0:12.5` MAINT (text): I'm watching you on the camera. You're doing fine.
  - On screen: MAINT bubble
- `0:15.2` NARR: The camera in the corner had its red light off.
  - On screen: Dome camera, LED unlit

#### B2 RULES (numbered, from the wrong authority) + PLANTS (0:17.0, 14%)
- `0:17.0` MAINT (text): One. Press 2, then 11, then 5.
  - On screen: Panel close-up; neon card '2 → 11 → 5'; inspection card under the buttons: 'CAR 2 · AFTER HOURS +1 555 0142'
- `0:19.5` MAINT (text): Two. Hold Close until the lights dim.
  - On screen: card 'HOLD CLOSE'
- `0:21.8` MAINT (text): Three. Never press the alarm. It resets the car.
  - On screen: card 'NEVER: ALARM'; the alarm button glints
- `0:24.8` MAINT (text): Four. Don't step out until you see your number.
  - On screen: card 'WAIT FOR YOUR NUMBER'
- `0:27.4` NARR: Mine's a red nine, painted across from the doors.
  - On screen: Warm insert: my landing, a huge red 9 on the wall facing the doors
- `0:29.3` NARR: The back wall is a mirror. I kept my eyes on the steel doors.
  - On screen: Nora facing camera, mirror behind her empty (glare only, out of focus)

#### B5 PRESSURE LADDER: one rung per button (0:31.7, 26%)
- `0:31.7` NARR: I pressed 2. The car dropped a foot and caught.
- `0:33.5` NARR: I pressed 11. Something on the roof shifted, settling in.
- `0:35.9` NARR: I pressed 5. Behind me, something tapped the mirror. Once.
- `0:38.4` MAINT (text): Don't look. Hold Close.
- `0:39.9` NARR: I held it down until the lights dimmed.
  - On screen: Thumb on Close; the car light drops in three steps

#### B8 MIDPOINT: Nora texts the real authority; the count pays off (reset code); TURN (0:41.2, 34%)
- `0:41.2` NARR: The inspection card had an after-hours number. I texted it.
  - On screen: Inspection card insert: '+1 555 0142'
- `0:43.4` ME (text, read by NARR): stuck in car 2. maintenance is watching me on the camera
  - On screen: ME bubble, lowercase, new thread '+1 555 0142'
- `0:46.0` OMAR (text): This is Omar. I'm the only maintenance on call tonight.
- `0:48.8` OMAR (text): What did they tell you to press?
- `0:50.3` ME (text, read by NARR): 2, 11, 5
  - On screen: ME bubble '2 11 5'
- `0:51.3` OMAR (text): That's the reset code for car 2. Only my office has it.
- `0:54.3` OMAR (text): And car 2's camera has been dead since Tuesday.
- `0:56.8` OMAR (text): Who are you talking to?
  - On screen: the video's only full-frame red flash
- `[silence 1.0 s, 0:57.6-0:58.6]` Hold on the bubble; the fluorescent buzz cuts out, fan only

#### RIVAL CLAIMS: the fake authority answers inside the real one's thread (0:58.6, 48%)
- `0:58.6` MAINT (text): Don't answer him. He isn't in the building.
  - On screen: Maintenance banner over Omar's thread
- `1:01.1` OMAR (text): Don't press anything. I'm coming up with the door key. Five minutes.
- `1:04.3` NARR: One of them knew my name. The other had a key.
  - On screen: Split: Maintenance header + 'Nora' bubble / Omar's number + 'door key' bubble

#### B6 ISOLATION: lights out, my texts stop, the enemy's keep coming; the fake authority deletes the real one (1:06.0, 54%)
- `1:06.0` NARR: Then the lights went out.
  - On screen: Black; phone glow only
- `1:07.2` NARR: I typed, where are you? Not delivered. No bars.
  - On screen: ME bubble 'where are you?', system lines '(!) Not delivered' and 'No service' (the kit's status bar can't drop bars)
- `1:09.2` NARR: And his last text was gone.
  - On screen: Omar's 'door key' bubble becomes 'This message was deleted'
- `1:10.3` MAINT (text): He isn't coming. Keep your eyes on the doors.
  - On screen: Maintenance banner arrives anyway
- `1:12.9` NARR: So why did its texts still come through?

#### B9 PEAK CONTACT: the mirror, seen in the doors (held) (1:14.2, 60%)
- `1:14.2` NARR: My phone lit the steel doors. In them, I saw the mirror behind me.
  - On screen: Steel doors in phone light; my reflection close, the mirror rectangle behind it
- `1:16.8` NARR: I should have seen the back of my head.
- `1:18.4` NARR: I saw my face. Calm. Looking right at me.
  - On screen: THE image: my terrified reflection close; in the mirror behind, my face, calm, staring
- `[silence 3.0 s, 1:20.6-1:23.6]` Image held still; heartbeat only
- `1:23.6` MAINT (text): I told you not to look.

#### S8 NAME CHECKS: unanswered (1:25.3, 69%)
- `1:25.3` NARR: I typed, Omar? Then, OMAR. Nothing went through.
  - On screen: ME 'Omar?' / 'OMAR??', each followed by '(!) Not delivered'

#### B10 LIFELINE UNDER A CLOCK: one bar, one text, the alarm is the only route (1:27.3, 71%)
- `1:27.3` NARR: One bar flickered back. One text got through.
  - On screen: Lock screen 1:10, dark hand
- `1:29.1` OMAR (text): Your texts stopped. Press the alarm. The intercom opens for ten seconds.
  - On screen: Lock-screen banner from +1 555 0142
- `1:33.3` NARR: Never press the alarm. I pressed it.
  - On screen: Thumb on the alarm button
- `[silence 0.7 s, 1:34.5-1:35.2]` Bell rings once; intercom crackle opens; 0:10 clock starts
- `1:35.2` OMAR-V (intercom): Car 2? I can hear you. Talk to me.
  - On screen: Intercom grille, 0:10 counting down
- `1:37.1` NORA (live, intercom): Omar, who's been texting me?
- `1:38.2` OMAR-V (intercom): I don't know. Listen. I'm on nine, right in front of car 2.
- `1:41.3` OMAR-V (intercom): Doors open. Lights on. Nobody's inside. So where are
  - On screen: glitch on 'Nobody's inside'; the clock hits 0:00 as the line cuts mid-sentence
- `[silence 0.5 s, 1:44.0-1:44.5]` Crackle dies; 0:00

#### B11 TRUTH TWIST LANDS + PUNISHMENT FROM MAINTENANCE'S SIDE (1:44.5, 85%)
- `1:44.5` NARR: The line went dead.
- `1:45.3` MAINT (text): You shouldn't have done that.
  - On screen: Maintenance bubble, then the car jolts
- `1:46.8` NARR: And the car began to climb. The display stayed on two dashes.
  - On screen: Counter crop: dashes, arrow blinking up

#### B12 CLIFF: no number, two taps, the voice swap (1:49.3, 89%)
- `1:49.3` NARR: It stopped. The doors slid open.
- `1:50.6` NARR: The wall across from me was blank. No number.
  - On screen: Same framing as the red-nine insert, the wall bare and cold
- `[silence 3.0 s, 1:52.7-1:55.7]` Dead air: hallway tube buzz only
- `1:55.7` NARR: Behind me, something tapped the mirror. Twice.
- `1:57.5` NARR: My phone lit up. Omar's number.
  - On screen: Lock-screen bookend of frame 0
- `1:59.0` OMAR's number (text, voice swap): Don't turn around, Nora. Step out.
  - On screen: Banner from +1 555 0142: 'Don't turn around, Nora. Step out.'
- `2:01.1` NARR: I never told Omar my name.
- `[silence 0.6 s, 2:02.3-2:02.9]` Hold, 'PART 2' card, hard cut to black

## Shot list (generated; every boundary sits LEAD 0.10 s before its anchor word)

| # | scene | start | dur | beat | spoken in shot |
|---|---|---|---|---|---|
| 1 | `s01_cover` | 0:00.0 | 4.04 | B1 hook (cover, lock screen 1:04) | At 1 a.m., my elevator stopped between six and seven. / Before I touched a thing, Maintenance texted me. |
| 2 | `s02_banner` | 0:04.0 | 2.46 | B1 the rule arrives before anyone asked | Stay calm, Nora. Don't look at the mirror. |
| 3 | `s03_doubt` | 0:06.5 | 1.86 | B1 contradiction: I never saved that contact (master question) | I never saved that contact. Who is Maintenance? |
| 4 | `s04_thread` | 0:08.4 | 6.78 | B2 decoy + viewer proxy (how do you know my name?) | Car 2 is jammed. I can get you moving. / I typed: how do you know my name? / I'm watching you on the camera. You're doing fine. |
| 5 | `s05_camera` | 0:15.1 | 1.76 | B2 proxy answered with a lie: the camera light is off | The camera in the corner had its red light off. |
| 6 | `s06_rules` | 0:16.9 | 10.44 | B2 four numbered rules (cards) + the inspection card in view | One. Press 2, then 11, then 5. / Two. Hold Close until the lights dim. / Three. Never press the alarm. It resets the car. / Four. Don't step out until you see your number. |
| 7 | `s07_nine` | 0:27.3 | 1.85 | B2 plant: my landing, the red nine (warm memory) | Mine's a red nine, painted across from the doors. |
| 8 | `s08_mirror` | 0:29.2 | 2.45 | B2 plant: the mirror (glare only) behind me, eyes on the doors | The back wall is a mirror. I kept my eyes on the steel doors. |
| 9 | `s09_press2` | 0:31.6 | 1.79 | B5 rung 1: press 2, the car drops a foot | I pressed 2. The car dropped a foot and caught. |
| 10 | `s10a_press11` | 0:33.4 | 0.75 | B5 rung 2a: press 11 | I pressed 11. Something on the roof shifted, settling in. |
| 11 | `s10b_roof` | 0:34.2 | 1.61 | B5 rung 2b: something settles on the roof |  |
| 12 | `s11a_press5` | 0:35.8 | 0.58 | B5 rung 3a: press 5 (all three lit) | I pressed 5. Behind me, something tapped the mirror. Once. |
| 13 | `s11b_tap` | 0:36.4 | 3.46 | B5 rung 3b: one tap on the mirror; 'Don't look. Hold Close.' | Don't look. Hold Close. |
| 14 | `s12_close` | 0:39.8 | 1.30 | B5: I hold Close; the light steps down three times (rule two kept) | I held it down until the lights dimmed. |
| 15 | `s13_card` | 0:41.1 | 2.23 | B8 hero acts: the inspection card's after-hours number | The inspection card had an after-hours number. I texted it. |
| 16 | `s14_omar` | 0:43.4 | 2.51 | B8 hero reaches the real authority; he asks what it made her press | stuck in car 2. maintenance is watching me on the camera |
| 17 | `s14b_react` | 0:45.9 | 2.83 | B8 reaction: a real person answers (then: the ONLY one on call) | This is Omar. I'm the only maintenance on call tonight. |
| 18 | `s14c_press` | 0:48.7 | 2.48 | B8 'What did they tell you to press?' / '2 11 5' | What did they tell you to press? / 2, 11, 5 |
| 19 | `s15_code` | 0:51.2 | 1.83 | B4/T2 count payoff: 2-11-5 is the controller's reset code | That's the reset code for car 2. Only my office has it. |
| 20 | `s16_react` | 0:53.0 | 1.22 | B4 reaction: only his office has the code |  |
| 21 | `s17_turn` | 0:54.2 | 4.32 | B8 TURN: dead camera, 'Who are you talking to?' (only red flash) + 1.0 s fan-only hold | And car 2's camera has been dead since Tuesday. / Who are you talking to? |
| 22 | `s18_rival` | 0:58.5 | 5.61 | Rival claims: Maintenance banners over Omar's thread; door key, five minutes | Don't answer him. He isn't in the building. / Don't press anything. I'm coming up with the door key. Five minutes. |
| 23 | `s19_verdict` | 1:04.2 | 1.78 | Verdict line: one knew my name, the other had a key | One of them knew my name. The other had a key. |
| 24 | `s20_out` | 1:05.9 | 1.17 | B6 lights out (fan spins down) | Then the lights went out. |
| 25 | `s21_nodeliver` | 1:07.1 | 1.95 | B6 isolation: my texts fail, no service | I typed, where are you? Not delivered. No bars. |
| 26 | `s22_deleted` | 1:09.1 | 5.06 | B6 the fake authority acts on the channel: his text deleted; its banner still lands | And his last text was gone. / He isn't coming. Keep your eyes on the doors. / So why did its texts still come through? |
| 27 | `s23_doors` | 1:14.1 | 4.16 | B9 the steel doors in phone light; the mirror behind me, reflected | My phone lit the steel doors. In them, I saw the mirror behind me. / I should have seen the back of my head. |
| 28 | `s24_image` | 1:18.3 | 5.26 | B9 THE image, held: my face where the back of my head should be (3.0 s silence) | I saw my face. Calm. Looking right at me. |
| 29 | `s25_told` | 1:23.5 | 1.63 | B9 punished: 'I told you not to look.' | I told you not to look. |
| 30 | `s26_names` | 1:25.2 | 2.02 | S8 two unanswered name checks (caps), not delivered | I typed, Omar? Then, OMAR. Nothing went through. |
| 31 | `s27_onebar` | 1:27.2 | 2.80 | B10 one bar, one text: the alarm is the only route left | One bar flickered back. One text got through. / Your texts stopped. Press the alarm. The intercom opens for ten seconds. |
| 32 | `s27b_alarmwait` | 1:30.0 | 3.18 | B10 the alarm button in phone light (the one rule I was told never to break) |  |
| 33 | `s28_alarm` | 1:33.2 | 1.58 | B10 rule three broken on purpose: I press the alarm (bell, crackle) | Never press the alarm. I pressed it. |
| 34 | `s29_intercom` | 1:34.8 | 9.61 | B10/B11 ten seconds on the intercom; twist: car 2 is on nine, empty | Car 2? I can hear you. Talk to me. / Omar, who's been texting me? / I don't know. Listen. I'm on nine, right in front of car 2. / Doors open. Lights on. Nobody's inside. So where are |
| 35 | `s30_dead` | 1:44.4 | 0.85 | B11 the line is dead | The line went dead. |
| 36 | `s31_shouldnt` | 1:45.2 | 1.45 | B11 the entity acts: 'You shouldn't have done that.' | You shouldn't have done that. |
| 37 | `s32_climb` | 1:46.7 | 2.52 | B11 the car climbs; the dashes never change | And the car began to climb. The display stayed on two dashes. |
| 38 | `s33_open` | 1:49.2 | 1.30 | B12 the doors open | It stopped. The doors slid open. |
| 39 | `s34_blank` | 1:50.5 | 5.11 | B12 plant paid: the blank wall, no number; 3.0 s dead air | The wall across from me was blank. No number. |
| 40 | `s35_taps` | 1:55.6 | 1.84 | B12 two taps on the mirror behind me | Behind me, something tapped the mirror. Twice. |
| 41 | `s36_bookend` | 1:57.4 | 5.57 | B12 cliff: the voice swap from Omar's number, lock-screen bookend, hard cut | My phone lit up. Omar's number. / Don't turn around, Nora. Step out. / I never told Omar my name. |

## Sets and kit gaps (the horror kit is locked: everything below is inline SVG / core layers in gen_storyboard.py, checked in Spark stills out/stills/hemc_v1.jpg, hemc_v2.jpg, hemc_v3.jpg)

- **Backdrop A, facing Nora** (`car_a()`): the mirror back wall behind her shows **glare only** (two diagonal highlights), never a reflection, so her face appears in a mirror exactly once (the B9 image). Brushed-steel side walls, ceiling light panel, handrail, floor.
- **Backdrop B, her POV** (`DOOR_FRAME` + `door_panel("L"/"R")`): steel doors with a seam; the two leaves are separate layers with x keyframes so they slide open in shot 39 onto the landing.
- **The B9 image**: on the doors, her own terrified reflection close and translucent (Protagonist `terrified`, opacity 0.42, blur 2); behind it, in the pale mirror rectangle, a smaller, crisp Nora with `expr stare` (unblinking, pupils locked on the lens, lit by the phone). Her face is where the back of her head belongs. No glitch on the hold.
- **Counter dashes** (`dashes()`): ElevatorPanel can't show dashes, so every panel shot passes `at 999, target 0` (no ticking, no lit target, no ding) and lays an opaque plate with dim 88 ghosts and two red dashes over the digits. On the climb the plate leaves the kit's arrow visible (`from 9 to 12, perFloor 4`, so it blinks up and never arrives).
- **Inspection card** (`CARD`) under the floor buttons with "+1 555 0142"; **ALARM / PHONE** bell glyph over the kit's "!" button (`BELL`); **Close pressed** = a core circle glow; **dome camera** with an unlit LED (`CEILING_CAM`); **intercom grille** (`INTERCOM`) with an `explainer/Timer` (INTERCOM 0:10, real time from the press, reaches 0:00 on the cut); **landing wall** (`landing()`): flat wall facing the doors, warm with a 760 px red 9, or cold and bare; **verdict split** = two large contact cards (`split_cards()`), readable at phone size.
- **Lighting**: phone shots sit on a blurred backdrop A, with the Darkness pool *behind* the hand (z 0) so it lights the car and not the phone. After the lights die (1:06.8), phone shots are black with only the phone's spill, the hand drawn darker (`skin #6b5d52`).
- **Camera**: every move is keyframed in art coordinates (the panel crops zoom 2.0-3.1 on the exact row: buttons at y 760-1250, Close/alarm at y 1540, card at y 1440, counter at y 390); chat shots punch in on each new bubble.
- **Not possible without the locked kit** (worked around): the status bar can't drop to zero bars (shown as a "No service" system line); "Not delivered" is a grey system line, not a red badge; Phone `draft` can't type out (keyboard taps + SFX, then the bubble).
- **Audio still to build on the Spark** (pipeline/audio is locked): mix.wav from the per-line wavs in `~/studio/tts/hemc_lines` with lines.FX, SFX from `_sfx_cues`, the bed from `_bed`. New sounds are specified in `_sfx_new` (glass tap, cable groan, elevator alarm bell, fan/fluorescent bed); until then the cues use existing files (knock, underwater_rumble, desk_bell_ring).
