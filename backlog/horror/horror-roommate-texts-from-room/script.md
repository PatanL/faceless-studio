---
id: horror-roommate-texts-from-room
niche: horror
title: My Roommate Texted Me: Don't Come Out
alt_titles: Three Plates. Two Of Us. | She Can't Open A Door You're Holding
format: 9:16 Short, standalone (no part label; 2 loops open at the cut)
runtime_s: 81.8 measured (Kokoro on the Spark CPU, audio/report.json). Hard cut 0.55 s after the last word. Over 61 s for TikTok Creator Rewards; keep any re-cut above 61 s.
words: 295 spoken (audio/lines.json)
wpm: 270 running speech (65.7 s of voice), 217 over the full runtime including the timed silences. Measured, not assumed. PLAYBOOK §7 chat target 250-275 read speed.
hook: 21 words / 5.2 s core hook; the threat is on screen at frame 0 (banner) and read as line 1; the trusted channel is contradicted at 3.5 s; 40 words in the first 10 s
voices: NARR/ME = Maya, first person (Kokoro af_heart, speed 1.40, horror voice chain). Both Danis use ONE voice (af_sky) so the ear cannot tell them apart; only the room changes. TXT (the Dani thread) dry and close at 1.32; KITCHEN through a wall (high-pass 220 Hz, low-pass 1.8 kHz, short echo, -4.5 dB); DOOR right behind the door (dry, chest boost, compressed, 1.04); CALM (the last two bubbles) at 1.00. MOM = Dani's mom's thread (af_nicole, 1.35).
audio_build: gen_audio.py in this folder (Spark only). pipeline/audio reads one voice per script and is locked by the horror closeout lane, so gen_audio.py imports its Kokoro wrapper, aligner, trims, voice chain and mix read-only and adds per-line voice + FX on top. Output: studio/public/episodes/horror-roommate-texts-from-room/mix.wav (-14.0 LUFS, -1.3 dBTP) and audio/*.json here. Whisper base.en check of the mix reads every kitchen and door line back correctly.
music: tension_pulse, ducked; hushed to near silence for the 3.4 s silence beat (63.7-68.6 s)
template: pipeline/templates/horror.md (chat thread + narrator, doppelganger variant, "two rival authorities" engine)
sibling_check: >-
  episodes/horror-roommate-two-rooms (already built: audio + storyboard) uses the same TOPICS #5 premise, and the first
  draft of this script copied its spine. What is STILL shared: a roommate texts from her bedroom that the one in the
  flat is not her; a warm dinner call in her voice; an outside person, reached by text, proves the roommate is not in
  the flat. What changed so the two do not read as the same video: the hero is Maya (the sibling's hero is Nora); the
  outside check is Dani's MOM with a fact the hero could not know (Dani went home to her family on Sunday while Maya
  was away all week), not a landlord saying "moved out yesterday / keys this morning"; the turn line is "Is she texting
  you, Maya?" (the voice knows about the texter), not "Who are you texting?"; no knock test, no secret-question test, no
  "which one will you let in" ending. New devices: frame-0 banner read as line 1, the door that clicks twice, three
  plates for two people, a door that does not lock and a "hold it up" handle rule, the 911 call stopped by the
  texter (her tell), the voice inverting rule two, a napkin with an in-joke, the handle dipping the instant Maya lets
  go to type, a photo of Maya's own door from inside Dani's room, six counted steps, and "Rule three" from the texter.
  Channel advice: post only one of the two roommate episodes, or space them at least 4 weeks apart.
  Originality gate against episodes/ and the other backlog scripts: see the Originality section at the end.
references:
  - id: 7670495663624408352
    url: https://www.tiktok.com/@mraevq/video/7670495663624408352
    views: 193600
    outlier_score: 18.01
    why: DORM-RULES, the "two rival authorities" engine. Borrowed - the close-person-is-not-themselves verdict in the hook (0:06), numbered rules with a stated protective effect (0:08-0:12), a rule acted on that costs something within seconds (0:14 -> 0:16), the narrator voicing the viewer's question (0:42), a rationalisation broken by the next event (1:14 -> 1:19), the suspect giving an order that contradicts the first authority (1:12) and inverting its rule (1:29-1:31), and the ending where a new rule comes from the wrong mouth (2:43-2:53). Not used - dorm, supervisor, curtains, ash, ghost, lore, the three knocks.
  - id: T42u5xhrq-0
    url: https://www.youtube.com/shorts/T42u5xhrq-0
    views: 868500
    outlier_score: 25.54
    why: TEXT-FIGURE, the 60 s chat-Short timing reference (PLAYBOOK §9.3). Borrowed - several bubbles in the first 3 s (0:00-0:03), the stand-in asking the viewer's question (0:09, 0:19), the denial / prank theory that the next beat breaks (0:34-0:35, 0:41), the turn at about 50% (0:31), the ALL CAPS ladder (0:37), two unanswered checks as the silence beat (0:53), the only image held back to about 88% (0:54), and the calm sentence-case voice swap aimed at "you" (0:56-0:58). Stretched from 60 s to 82 s. Our unanswered checks are "where are you" / "WHO ARE YOU", not a repeated name, so the device is not a template copy.
  - id: 7659677578365537569
    url: https://www.tiktok.com/@udhwkz/video/7659677578365537569
    views: 376200
    outlier_score: 10.79
    why: SIEGE-CHAT, the barrier-plus-channel siege. Borrowed - the trusted channel contradicted inside the hook (0:08 -> 0:11), the threat at the door that senses the hero (1:11-1:15), the barrier about to be bypassed (1:47-1:49), the call for help that never connects while only the enemy's channel still works (2:03-2:11), the one real outside fact that erases the fake story (3:58-4:01), and ending on an imperative (4:05-4:08). Not used - the killer, fake cop, building chat, stickers, burner phone, battery countdown.
device_citations:
  - "7702661471641128224 (@udhwkz HEARSE-P2, 343,100 views, 9.85x, https://www.tiktok.com/@udhwkz/video/7702661471641128224): the outside check by family (PLAYBOOK §4B T5). The narrator contacts the companion's parent (1:36), a pause (1:43), and a family fact falsifies the companion (1:45-1:46). We use it as a text to Dani's mom and her reply."
originality: "python3 scripts/originality_check.py on this file prints PASS against research/corpus + research/library/transcripts, and separately against episodes/ and the other backlog/horror scripts (results at the end of this file)."
status: final script; audio built (gen_audio.py, Spark); storyboard.json validates (npm run validate, Spark) and renders stills (out/stills/roommate_v2.jpg, roommate_v3.jpg)
---

# My Roommate Texted Me: Don't Come Out

**Premise.** 11:40 p.m. Maya has just got back from a week away. Her roommate Dani's door was already shut when she
got home. A text from Dani: *don't come out of your room.* At the same moment, Dani's voice calls from the kitchen:
dinner's ready. The texter says the kitchen girl has her face and gives two rules. Maya's door doesn't lock: rule two
says hold the handle up, *she can't open a door you're holding.* The voice reaches the door, asks "Is she texting
you, Maya?", forces the handle, swears the texter is the copy, and says the rules are there to keep Maya from leaving.
A napkin with an in-joke only Dani knew slides under the door. Maya lets go of the handle to text Dani's mom (it
dips the instant she does): Dani has been home with her family since Sunday. Neither Dani is Dani. Then a photo
arrives from inside Dani's room, of Maya's own door with someone standing at it. Dani's door clicks twice. Six steps.
The handle turns under Maya's hand and stops halfway. The thread, calm for the first time: *Rule three, Maya. Dinner
is for three. Come out.*

**Truth (writers only, never stated).** There are two of them and they work together. The kitchen one plays the warm
roommate; the texter plays the protective roommate and keeps Maya in her room, off the phone, with her hands on the
door, until both are ready. The three plates were for them and her. They can open the door. They want her to open it.

**Ownable signature:** Dani's door clicks twice when it opens. Planted with the actual sound at 14.7 s ("It hadn't
clicked once tonight"), paid with the same sample, into silence and without narration, at 72.4 s (89%).
**Countable plant:** "I set three plates!" (17.6 s) / "Three plates. There's two of us." (20.7 s), paid by "Dinner is
for three." (79.4 s, 97%).
**Rules:** rule one, don't answer her (kept: Maya never speaks); rule two, hold the handle up, she can't open a door
you're holding (tested at 40.2 s, inverted by the voice at 47.3 s, broken at 55.3 s with an instant cost, then
defeated at 76.0 s when the handle turns under Maya's hand anyway); rule three arrives from the texter in the last line.

**Why Maya could not know (the twist's plant):** "I'd been away all week. Her door was shut when I got home." (10.2 s).

**The texter's tells (so "which Dani is real?" is a live question):** it stops the 911 call; it says "she's outside
your door" before Maya hears anything (the creak comes a second later); its rules keep Maya inside, which the voice
says out loud at 47.3 s. The voice's tells: three plates, forcing the handle, knowing about the texter.

### Loops

| Loop | Opens | Closes |
|---|---|---|
| Master: which Dani is real? | 3.5 s (the voice contradicts the text) | 58.7-63.3 s: neither (Dani is at her family's). Restated at 51.2 s ("Only Dani knew that.") |
| Is it a prank? | 16.5 s | 18.6 s: the texter types while the kitchen voice is mid-sentence |
| Can I call for help? | 33.6 s (dialing 911) | 34.8 s: the texter stops it (and gives itself away) |
| Will rule two hold? | 24.4 s | tested 40.2, broken 55.3 (instant dip), defeated 76.0 |
| Why hasn't her door clicked? | 15.3 s | 72.4 s: it clicks, the same sound |
| Who is the third plate for? | 20.7 s | 79.4 s: "Dinner is for three." |
| Who took the photo from an empty room? | 68.6 s | 72.4-75.8 s: whoever was in there just walked out (clicks, six steps) |
| Open at the cut (2) | | What are they? What happens if she comes out? |

Two loops open at the cut: inside the PLAYBOOK §4D standalone band (0-2), so the title carries no part label.

## Pacing vs PLAYBOOK (measured from audio/lines.json, total 81.76 s)

| Metric | PLAYBOOK target | This script |
|---|---|---|
| Runtime | Shorts 50-100 s; chat horror near 60 s; over 61 s for Creator Rewards | 81.8 s (was 91.3 s) |
| Words / wpm | chat 250-275 read speed; narrated 230-270 | 295 words; 270 wpm running speech, 217 overall |
| Line 1 | ≤12 words, place or object + danger or rule | "don't come out of your room." (6 words, a rule) read at 0.1 s, then "My roommate sent that from her bedroom at 11:40." |
| Frame 0 = cover | shows the threat | lock screen 11:40 with the banner "Dani: don't come out of your room" already on screen at frame 0; my door with the warm strip under it behind the phone |
| Hook | core ≤30 words / ≤6 s; trusted source contradicted ≤11 s | core hook 21 words / 5.2 s; contradiction (her voice from the kitchen) at 3.5 s; 40 words in the first 10 s |
| Jolt interval | Shorts 2.5-3.5 s median, never >8 s | 1.6 s median over 47 events; longest gaps 3.8 s (24.4 -> 28.2, rule two being read) and 3.8 s (the held photo) |
| Proximity ladder | physical rungs ~3 s apart, two ladders at once | kitchen (3.5) -> sizzle stops, plate in the hall (31.6) -> "outside your door" (34.8) -> floor creaks at my door (36.7) -> voice through the door (38.0) -> handle tips (40.2) -> forced against my palms (43.8, 44.2) -> napkin through the gap (50.3) -> a second one crosses the flat, six steps (73.6-75.8) -> handle turns under my hand (76.0). Channel ladder in parallel: voice, texts, 911 stopped, rules, mom's thread, the photo |
| Turn | 43-55% | "Is she texting you, Maya?" at 38.0 s (46%) with the only full-frame red flash |
| CAPS ladder | first caps ~60% | "HOLD IT UP" at 41.1 s (50%); calm sentence case from the entity at 78.0 s |
| Skeptic beat | a rationalisation the next event breaks | "I figured it was a prank." (16.5) broken at 18.6 by the texter's bubble landing while the voice is mid-sentence |
| Outside-check twist | PLAYBOOK biggest twist ~89% (55-98) | mom at 58.7-63.3 s (72-77%); the reframe of the texter (rule three, the plates) at 78.0-81.2 s (95-99%) |
| Scariest image | once, 60-80%, held ~4 s | the photo 68.6-72.4 s (84-89%), held still 3.9 s (TEXT-FIGURE's one image is at 90%) |
| Lifeline under a clock | 70-90% | 53.3-57.9 s (65-71%): the clock is physical, Maya's own grip. The handle dips the instant she lets go and she types one-handed. No battery (seven other horror scripts already use one) |
| Silences | 1-3 timed, 3-8 s with SFX | 3.4 s (63.7-68.6: two sends and typing dots, music hushed); 3.6 s (71.6-75.2: the two clicks into silence, then six steps); 0.95 s after "outside your door" before the creak |
| Numbers / min | narrated 3-5, chat 0-1 | 16 (11:40, nine, six, twice, once, three, two, rule one, rule two, 911, once, twice, Sunday, six, rule three, three) = 11.7/min. Above target on purpose: every number is a count the payoff uses |
| Sentence median | chat 4-5 words per bubble, punch lines 49-55% | 4 words; 58% of sentences are ≤4 words |
| "You" share | dialogue-heavy 16-28% | 10 of 42 voiced lines (24%), all inside texts or her voice |
| Ending | hard cut on a new rule from the wrong authority / a threat on "you"; last shot bookends the first | "Rule three, Maya. Dinner is for three. Come out." on the lock screen (11:52), mirroring frame 0 (11:40); behind it four foot shadows now under the door. Hard cut, no CTA |

## Beat alignment (reference timestamps rechecked against research/corpus/horror/<id>.md)

| Our beat | Our time | Reference id + timestamp | Device borrowed | How we adapt it |
|---|---|---|---|---|
| S1 Hook | 0:00.0-0:05.2 | T42u5xhrq-0 0:00-0:03; 7659677578365537569 0:08-0:11 | several messages in the first 3 s; the trusted channel's word contradicted at once | The banner is on screen at frame 0 and read as line 1; the contradiction is her own voice from the kitchen at 3.5 s, not a knock |
| S2 Named threat | 0:05.3-0:10.0 | 7670495663624408352 0:06 | verdict that a close person is not who she seems | The verdict comes from the roommate about her double, with an alibi time ("since nine") |
| S3 Setup + plants | 0:10.2-0:16.4 | T42u5xhrq-0 0:13 plant -> 0:42 payoff; 7670495663624408352 0:57 sound before sight | one odd detail planted to return as the threat; a sound signature | "Away all week" (the twist's plant), six steps, and the door that clicks twice, played once so the viewer learns the sound |
| Skeptic beat | 0:16.5-0:20.6 | T42u5xhrq-0 0:34-0:35, 0:41; 7670495663624408352 1:14 -> 1:19 | a rationalisation (prank) broken by the very next event | The texter's bubble lands while the kitchen voice is mid-sentence: two of them, proved in 2 s with no new props |
| Countable plant | 0:17.6-0:21.9 | 7659677578365537569 0:19 -> 0:28 (count match) | a hyper-specific count that a later count matches | Three plates for two people, paid by "Dinner is for three." |
| S4 Rules | 0:22.0-0:28.0 | 7670495663624408352 0:08-0:12 | numbered rules with a stated protective effect the viewer can check | Rule one (don't answer) and rule two (hold the handle up; she can't open a door you're holding), with "My door doesn't lock." between them |
| Viewer proxy | 0:28.2-0:31.4 | 7670495663624408352 0:42; T42u5xhrq-0 0:09, 0:19 | the narrator voices the viewer's question | "how do I know you're the real one?" gets an unsettling reassurance (PLAYBOOK S5) instead of proof |
| S5 Exit closed | 0:31.6-0:37.9 | 7659677578365537569 2:03-2:11 | the call for help fails and only the enemy's channel still works | The texter itself stops the 911 call ("don't. she's outside your door.") before any sound from the hall; the floor creaks a second later, so the texter knew something it could not hear |
| S6 Turn | 0:38.0-0:40.0 | T42u5xhrq-0 0:31; 7659677578365537569 1:11-1:15 | the threat crosses into my space and senses the hero's channel | "Is she texting you, Maya?" through the door at 46%, the only full-frame red flash |
| S7 Panic ladder | 0:40.1-0:44.8 | T42u5xhrq-0 0:37-0:47; 7670495663624408352 0:14 -> 0:16 | CAPS as volume; the rule tested at once | The handle tips, "HOLD IT UP", both hands, forced down "Once. Twice." |
| B8 Rival claim + rule inversion | 0:44.9-0:49.7 | 7670495663624408352 1:12 and 1:29-1:31 | the suspect contradicts the first authority and inverts its rule | "The one in my room is the copy. She wants you holding that door so you can't leave." |
| Barrier rung + restated loop | 0:49.9-0:53.2 | 7659677578365537569 1:47-1:49; 7670495663624408352 1:47-1:53 | the threat reaches through the barrier; a check-it-yourself proof | A napkin under the door with an in-joke ("still sorry about your cactus") that only Dani knew, which makes the voice look real |
| B10 Lifeline under a clock | 0:53.3-0:57.9 | 7659677578365537569 3:17-3:37; 7670495663624408352 0:14 -> 0:16 | the one real outside contact, reached under pressure; a broken rule punished at once | Maya lets go to text Dani's mom; the handle dips that instant; she types one-handed |
| B11 Outside check | 0:58.7-1:03.3 | 7702661471641128224 1:36-1:46; 7659677578365537569 3:58-4:01 | a family member's concrete fact falsifies the companion | "Dani's been home with us since Sunday. She's asleep down the hall. I just checked." Neither Dani is Dani |
| S8 Silence beat | 1:03.5-1:08.6 | T42u5xhrq-0 0:53 | unanswered checks; the gap is the scare | The handle goes slack; 3.4 s with no voice: "where are you", "WHO ARE YOU", typing dots |
| S9 Proof | 1:08.6-1:12.4 | T42u5xhrq-0 0:54 | the only image, held back to ~90% | A greyscale photo from inside Dani's room of Maya's own door, someone standing at it; held still 3.9 s |
| S10 Plant payoff, voice swap, cut | 1:12.4-1:21.8 | T42u5xhrq-0 0:56-0:58; 7670495663624408352 2:43-2:53; 7659677578365537569 4:05-4:08 | plant pays off; calm sentence case from the entity; new rule from the wrong authority; final imperative | The two clicks into silence, six steps, the handle turns under her hand and stops; "Rule three, Maya. Dinner is for three. Come out." on the lock screen, bookending frame 0 |

## Script

Speaker key: NARR = Maya narrating; ME = Maya's own blue bubble (read by Maya); TXT = a bubble in the "Dani" thread, read
in Dani's voice; KITCHEN = Dani's voice through the wall; DOOR = Dani's voice right behind my door; MOM = a bubble in
the "Dani's Mom" thread; BUBBLE = on screen only. Times are measured starts (audio/lines.json).
Captions: core caption track at the top (`y` 0.12, backing pill, red only on marked words). NARR, KITCHEN and DOOR
lines are captioned; every texted line is shown as its bubble or banner instead, so nothing is on screen twice.

#### S1 Hook (0:00.0-0:05.2)
- `0:00.0` **Frame 0 / cover:** lock screen 11:40, banner "Dani: don't come out of your room" already showing; my door blurred behind the phone, warm light under it.
- `0:00.1` TXT: don't come out of your room.
- `0:01.4` NARR: My roommate sent that from her bedroom at 11:40.
- `0:03.5` KITCHEN: Maya! Dinner's ready, come eat!
#### S2 Named threat (0:05.3-0:10.0)
- `0:05.3` NARR: Dani's voice. From the kitchen.
- `0:06.8` TXT: that one isn't me.
- `0:07.9` TXT: i've been in bed since nine. she has my face.
#### S3 Setup and plants (0:10.2-0:16.4)
- `0:10.2` NARR: I'd been away all week. Her door was shut when I got home.
- `0:12.5` NARR: It's six steps from mine. It clicks twice when it opens.
  - Audio: the latch sample, two clicks 0.38 s apart, at 14.7 s (the signature, heard once).
- `0:15.3` NARR: It hadn't clicked once tonight.
#### Skeptic beat and countable plant (0:16.5-0:21.9)
- `0:16.5` NARR: I figured it was a prank.
- `0:17.6` KITCHEN: I set three plates! Hurry up!
  - On screen: Dani's typing dots run while the voice talks; "she's lying to you" pops on "Hurry" (18.6 s).
- `0:19.3` NARR: She was mid-sentence when that landed.
- `0:20.7` NARR: Three plates. There's two of us.
#### S4 Rules (0:22.0-0:28.0)
- `0:22.0` TXT: rule one. don't answer her.
- `0:23.4` NARR: My door doesn't lock.
- `0:24.4` TXT: rule two. if she tries your handle, hold it up. she can't open a door you're holding.
#### Viewer proxy (0:28.2-0:31.4)
- `0:28.2` ME: how do I know you're the real one?
- `0:29.4` TXT: because she wants you out there. i want you alive.
#### S5 Exit closed, and the texter's tell (0:31.6-0:37.9)
- `0:31.6` NARR: The sizzling stopped. A plate clinked in the hall.
  - Audio: the muffled sizzle (running since 1.1 s) cuts dead; plate clink at 32.8 s.
- `0:33.6` NARR: I started dialing 911.
- `0:34.8` TXT: don't. she's outside your door.
  - `[0.95 s]` nothing; floor creak at 36.7 s.
- `0:37.1` NARR: Then the floor creaked.
#### S6 Turn (0:38.0-0:40.0)
- `0:38.0` DOOR: Is she texting you, Maya?
  - The only full-frame red flash; impact; shake.
#### S7 Panic ladder (0:40.1-0:44.8)
- `0:40.1` NARR: My handle tipped down.
- `0:41.1` TXT: HOLD IT UP
  - On screen: a second CAPS bubble "MAYA HOLD IT" (silent); phone vibrates.
- `0:42.2` NARR: I grabbed it with both hands. It pushed down. Once. Twice.
  - The lever is forced down against both hands exactly on "Once." (43.8) and "Twice." (44.2).
#### B8 Rival claim and rule inversion (0:44.9-0:49.7)
- `0:44.9` DOOR: It's me. The one in my room is the copy.
- `0:47.3` DOOR: She wants you holding that door so you can't leave.
#### Barrier rung (0:49.9-0:53.2)
- `0:49.9` NARR: A napkin slid under my door.
- `0:51.2` NARR: Still sorry about your cactus. Only Dani knew that.
  - On screen: the napkin, her handwriting "still sorry about your cactus".
#### B10 Lifeline under a clock (0:53.3-0:57.9)
- `0:53.3` NARR: Her mom would know.
- `0:54.1` NARR: I let go to text her, and the handle dipped. I shoved it back up, one-handed.
  - Insert: the lever dips on "dipped" (55.3 s), one hand shoves it back.
- `0:57.2` ME: is Dani with you?
  - `[0.85 s]` typing dots from Dani's Mom.
#### B11 Outside check (0:58.7-1:03.3)
- `0:58.7` MOM: Maya? Dani's been home with us since Sunday.
- `1:00.9` MOM: She's asleep down the hall. I just checked.
  - Glitch and stinger on the last bubble.
#### S8 Silence beat (1:03.5-1:08.6)
- `1:03.5` NARR: The handle went slack. Outside, nothing.
- `[3.4 s, no voice, music hushed]` BUBBLE (me): where are you (1:06.4) / BUBBLE (me): WHO ARE YOU (1:07.2) / Dani typing dots (1:08.0)
#### S9 Proof (1:08.6-1:12.4)
- `1:08.6` NARR: She sent a photo. From her room, of my door.
- `1:10.6` NARR: Someone was standing outside it.
  - The only image, held still 3.9 s.
#### S10 Plant payoff, voice swap, cut (1:12.4-1:21.8)
- `[1:12.4]` the two latch clicks, the exact sample from 14.7 s, into 1.2 s of silence. No narration.
- `[1:13.6]` six footsteps crossing the flat, closer each time.
- `1:15.2` NARR: Six steps.
- `1:16.1` NARR: Under my hand, it began to turn.
  - The lever turns slowly down under her hand, then stops dead halfway.
- `1:18.0` CALM: Rule three, Maya.
- `1:19.4` CALM: Dinner is for three. Come out.
  - Lock-screen banners (11:52), mirroring frame 0. Hard cut to black at 1:21.8. No CTA.

## TTS source (multi-voice)

gen_audio.py reads this block. It is the source of truth for every spoken word and SFX cue above.

```cast
# One utterance per line: ID SPEAKER: text
# Speakers: NARR = Maya narrating (af_heart); ME = Maya reading her own blue bubble (af_heart); TXT = the Dani thread (af_sky);
#   CALM = the Dani thread's last two bubbles, slower (af_sky); KITCHEN = Dani's voice through the wall, low-passed (af_sky);
#   DOOR = Dani's voice right behind my door, dry and close (af_sky); MOM = Dani's mom's thread (af_nicole);
#   BUBBLE / BUBBLE_ME / BUBBLE_TXT = on screen only, not voiced.
# Markers: [sfx: name @offset vol=dB hush=s] fires at the next word (line end if last); [gap: s] silence after the line;
#   [hold: s] length of a silent beat; {display|spoken} shows the first form and speaks the second.
L01 TXT: [sfx: notify @-0.12 vol=-2] don't come out of your room.
L02 NARR: [sfx: sizzle @-0.3 vol=-13] My roommate sent that from her bedroom at {11:40|eleven forty}.
L03 KITCHEN: Maya! Dinner's ready, come eat!
L04 NARR: Dani's voice. From the kitchen. [gap: 0.18]
L05 TXT: [sfx: message_pop] that one isn't me.
L06 TXT: [sfx: message_pop] i've been in bed since nine. she has my face. [gap: 0.22]
L07 NARR: I'd been away all week. Her door was shut when I got home.
L08 NARR: It's six steps from mine. It clicks twice when it opens. [sfx: latch2 @0.08] [gap: 0.68]
L09 NARR: It hadn't clicked once tonight. [gap: 0.18]
L10 NARR: I figured it was a prank.
L11 KITCHEN: I set three plates! [sfx: message_pop @0.05] Hurry up!
L12 NARR: She was mid-sentence when that landed.
L13 NARR: Three plates. There's two of us. [gap: 0.18]
L14 TXT: [sfx: message_pop] rule one. don't answer her.
L15 NARR: My door doesn't lock.
L16 TXT: [sfx: message_pop] rule two. if she tries your handle, hold it up. she can't open a door you're holding. [gap: 0.18]
L17 ME: how do I know you're the real one? [sfx: message_send]
L18 TXT: [sfx: message_pop] because she wants you out there. i want you alive. [gap: 0.2]
L19 NARR: [sfx: sizzle_stop @-0.2] The sizzling stopped. A plate [sfx: plate @0.1] clinked in the hall.
L20 NARR: I started dialing {911|nine one one}.
L21 TXT: [sfx: message_pop] don't. she's outside your door. [sfx: floor_creak @0.5] [gap: 0.95]
L22 NARR: Then the floor creaked.
L23 DOOR: [sfx: impact @-0.05 vol=-4] Is she texting you, Maya? [gap: 0.5]
L24 NARR: [sfx: jolt_a @0.05] My handle tipped down.
L25 TXT: [sfx: phone_buzz] {HOLD IT UP|hold it up!}
L26 NARR: I grabbed it with both hands. It pushed down. [sfx: jolt_b] Once. [sfx: jolt_c] Twice.
L27 DOOR: It's me. The one in my room is the copy.
L28 DOOR: She wants you holding that door so you can't leave. [gap: 0.22]
L29 NARR: A napkin [sfx: whoosh vol=-8] slid under my door.
L30 NARR: Still sorry about your cactus. Only Dani knew that.
L31 NARR: Her mom would know.
L32 NARR: I let go to text her, and the handle [sfx: jolt_a] dipped. I shoved it back up, one-handed.
L33 ME: is Dani with you? [sfx: message_send] [gap: 0.85]
L34 MOM: [sfx: message_pop] Maya? Dani's been home with us since Sunday.
L35 MOM: [sfx: message_pop] She's asleep down the hall. I just checked. [sfx: stinger @0.0 vol=-3] [gap: 0.25]
L36 NARR: The handle went slack. Outside, nothing. [sfx: hush4 @0.3 hush=0.3]
B01 BUBBLE: [hold: 1.0]
B02 BUBBLE_ME: [sfx: message_send vol=-4] where are you [hold: 0.85]
B03 BUBBLE_ME: [sfx: message_send vol=-4] WHO ARE YOU [hold: 0.8]
B04 BUBBLE_TXT: typing [hold: 0.6]
L37 NARR: [sfx: message_pop] She sent a photo. From her room, of my door.
L38 NARR: Someone was standing outside it. [gap: 0.8]
B05 BUBBLE: [sfx: latch2] [hold: 1.2]
B06 BUBBLE: [sfx: steps6] [hold: 1.6]
L39 NARR: Six steps. [gap: 0.25]
L40 NARR: [sfx: handle_turn @-0.1] Under my hand, it began to turn. [gap: 0.5]
L41 CALM: [sfx: notify vol=-4] Rule three, Maya.
L42 CALM: [sfx: notify vol=-4] Dinner is for three. Come out. [gap: 0.2]
```

## Single-voice fallback (pipeline/audio/make.py)

`pipeline/episodes/build.py` and `pipeline.audio.make` read the first fenced narration block and one voice. Use this
only if gen_audio.py cannot run: af_heart reads every line, and the texted and voiced Dani lines drop 3 dB so they
sit apart. It loses the identical-Dani-voice effect, so it is a fallback, not the episode.

```narration
[music: tension_pulse] [vox: -3] don't come out of your room.

My roommate sent that from her bedroom at eleven forty.

[vox: -3] Maya! Dinner's ready, come eat!

Dani's voice. From the kitchen.

[vox: -3] that one isn't me.

[vox: -3] i've been in bed since nine. she has my face.

I'd been away all week. Her door was shut when I got home.

It's six steps from mine. It clicks twice when it opens.

It hadn't clicked once tonight.

I figured it was a prank.

[vox: -3] I set three plates! Hurry up!

She was mid-sentence when that landed.

Three plates. There's two of us.

[vox: -3] rule one. don't answer her.

My door doesn't lock.

[vox: -3] rule two. if she tries your handle, hold it up. she can't open a door you're holding.

how do I know you're the real one?

[vox: -3] because she wants you out there. i want you alive.

The sizzling stopped. A plate clinked in the hall.

I started dialing nine one one.

[vox: -3] don't. she's outside your door.

Then the floor creaked.

[vox: -3] Is she texting you, Maya?

My handle tipped down.

[vox: -3] hold it up!

I grabbed it with both hands. It pushed down. Once. Twice.

[vox: -3] It's me. The one in my room is the copy.

[vox: -3] She wants you holding that door so you can't leave.

A napkin slid under my door.

Still sorry about your cactus. Only Dani knew that.

Her mom would know.

I let go to text her, and the handle dipped. I shoved it back up, one-handed.

is Dani with you?

[vox: -3] Maya? Dani's been home with us since Sunday.

[vox: -3] She's asleep down the hall. I just checked.

The handle went slack. Outside, nothing.

She sent a photo. From her room, of my door.

Someone was standing outside it.

Six steps.

Under my hand, it began to turn.

[vox: -3] Rule three, Maya.

[vox: -3] Dinner is for three. Come out.
```

## Shot list (generated by gen_storyboard.py --table from the measured timings; 32 shots, mean 2.55 s)

Component names follow the horror kit README. Maya is drawn as `horror/Protagonist` in its default colours. Dani is never shown
except as the faceless silhouette in the photo. HandPhone at `cy` 0.61 so the captions fit above it. Inline SVG
layers (drawn in gen_storyboard.py) cover the kit gaps: an interior bedroom door with no peephole, chain or deadbolt;
a lever on its own layer that turns, dips and springs back with rotate keyframes; hands on the lever; three plates;
the gap under the door; the napkin; the photo.

| # | t_start | t_end | Shot type | Visual description (kit vocabulary) | SFX |
|---|---|---|---|---|---|
| 1 | 0:00.0 | 0:03.5 | Phone POV, lock screen (cover) | HandPhone lock 11:40, banner "Dani: don't come out of your room" already on screen at frame 0; behind it, my bedroom door blurred with the warm strip under it | notify at 0.0 (banner already present); muffled sizzle fades in under L02 |
| 2 | 0:03.5 | 0:06.7 | Medium, Maya in bed | Bedroom lamp 0.15; Maya pose phone, light phone, looks toward the door (frame right); neutral -> scared on "Dani's voice" | KITCHEN voice through the wall (1.8 kHz low-pass), sizzle under |
| 3 | 0:06.7 | 0:10.1 | Phone POV, DM "Dani" | chat dm "Dani": the warning, then "that one isn't me" and "i've been in bed since nine. she has my face"; typing dots first | message_pop x2 |
| 4 | 0:10.1 | 0:13.4 | Wide, the flat's corridor | Hallway (lights 1, endDoor) as the flat's corridor; label "HOME 10 PM" on "home", then "6 STEPS" between the two bedroom doors | sizzle (muffled) under |
| 5 | 0:13.4 | 0:16.4 | Close, Dani's door | her door (cooler colours), its lever dips twice exactly on the two latch clicks; "CLICK" "CLICK" labels; then still and dark on "hadn't clicked once" | latch2 (the signature sample) after "opens" |
| 6 | 0:16.4 | 0:17.6 | Close, Maya | Bedroom lamp 0.15; Maya suspicious, half a smirk: "I figured it was a prank." | - |
| 7 | 0:17.6 | 0:20.7 | Phone POV, DM "Dani" | Dani typing dots run WHILE the kitchen voice is mid-sentence; "she's lying to you" pops on "Hurry" | message_pop under the kitchen voice |
| 8 | 0:20.7 | 0:21.9 | Top-down insert, the table | three plates set out under warm kitchen light; "3 PLATES" then "2 OF US" in red | - |
| 9 | 0:21.9 | 0:23.4 | Phone POV, rule one | bubble "rule one. don't answer her." + neon card "RULE 1" | - |
| 10 | 0:23.4 | 0:24.3 | Medium, my door | my bedroom door from inside: a plain lever, no lock of any kind; label "NO LOCK" | - |
| 11 | 0:24.3 | 0:31.5 | Phone POV, rule two + my question | bubble rule two + "RULE 2" card; 0.85 s insert of my lever with a white UP arrow on "hold it up"; my blue bubble "how do I know you're the real one?"; Dani: "because she wants you out there. i want you alive." | message_pop, message_send |
| 12 | 0:31.5 | 0:33.5 | Medium, my door | my door from inside, the warm strip under it; the kitchen sound cuts dead; a small "clink" label on the plate sound | sizzle stops dead on "stopped"; plate clink in the hall |
| 13 | 0:33.5 | 0:34.7 | Close, Maya dialing | Maya, phone lit under her face, thumb on the keypad; big red "911" label (no call screen: the kit only draws an incoming call) | - |
| 14 | 0:34.7 | 0:36.6 | Phone POV, DM "Dani" | Dani was already typing as I dialed; "don't. she's outside your door." lands BEFORE any sound from the hall | - |
| 15 | 0:36.6 | 0:38.0 | Medium, my door | the floor creaks; two foot shadows step into the strip under my door and stop | floor_creak |
| 16 | 0:38.0 | 0:40.0 | Close, my door (the turn) | "Is she texting you, Maya?" right behind the door: the only full-frame red flash (Glitch + red Vignette 0.4 s), shake on the impact | impact; DOOR voice dry and close |
| 17 | 0:40.0 | 0:41.0 | Extreme close, my lever | my lever tips down on its own (the handle test) | jolt |
| 18 | 0:41.0 | 0:42.2 | Phone POV, CAPS | CAPS bubbles "HOLD IT UP", "MAYA HOLD IT"; phone vibrates and trembles; heartbeat edges start | phone_buzz |
| 19 | 0:42.2 | 0:44.8 | Extreme close, both hands on the lever | both my hands hold the lever up; it is forced down against them on "Once." and "Twice." | jolt x2 on the words |
| 20 | 0:44.8 | 0:47.2 | Low medium, my door | the door, feet in the strip; her voice pleads: "It's me. The one in my room is the copy." | - |
| 21 | 0:47.2 | 0:49.8 | Close, Maya against the door | Maya (pose idle, holding on, frame-edge hands implied) terrified -> suspicious on "so you can't leave" (the rule inverted) | - |
| 22 | 0:49.8 | 0:51.1 | Low close, the gap under my door | a white napkin slides out from under the door between her two foot shadows | whoosh at -8 dB (paper slide) |
| 23 | 0:51.1 | 0:53.2 | Insert, the napkin | the napkin up close; her handwriting appears: "still sorry about your cactus" | - |
| 24 | 0:53.2 | 0:57.1 | Phone POV, "Dani's Mom" thread | the thread with Dani's mom (one old, harmless message from her); a 0.7 s insert of my lever dipping the instant I let go, then my left hand shoving it back up | jolt on "dipped" |
| 25 | 0:57.1 | 1:03.4 | Phone POV, the outside check | my bubble "is Dani with you?" sends; typing; Mom: "Maya? Dani's been home with us since Sunday." / "She's asleep down the hall. I just checked."; glitch on the last bubble | message_send, typing, message_pop x2, stinger -3 dB |
| 26 | 1:03.4 | 1:05.3 | Close, Maya | Maya pose cover, terrified, no blinking; "The handle went slack. Outside, nothing." | music hushes to near silence |
| 27 | 1:05.3 | 1:08.6 | Phone POV, DM "Dani" (silence) | 3.3 s with no voice: my bubbles "where are you", then "WHO ARE YOU", then Dani's typing dots | message_send x2 at -4 dB, nothing else |
| 28 | 1:08.6 | 1:12.4 | Photo insert (the only image), held still | greyscale photo card (white border, 2 deg tilt) over the blurred thread: taken from inside Dani's dark room, through her doorway, across the flat to MY door; someone stands at it, backlit by the strip | message_pop; held still 3.9 s |
| 29 | 1:12.4 | 1:13.6 | Close, Maya | no narration: the two latch clicks (the plant's exact sample) into silence; Maya's eyes snap toward the sound | latch2 (same file as s05) |
| 30 | 1:13.6 | 1:16.0 | Medium, my door (six steps) | six footsteps cross the flat; a second pair of foot shadows joins the first in the strip on the last step; "Six steps." | steps6 (getting closer) |
| 31 | 1:16.0 | 1:17.9 | Extreme close, my hand on the lever | my one hand holding it up; the lever turns slowly down under it anyway, then stops dead halfway | handle_turn (slow squeak + ratchet), cut dead |
| 32 | 1:17.9 | 1:21.8 | Phone POV, lock screen (bookend of s01) | lock screen again, 11:52; calm banners "Rule three, Maya." / "Dinner is for three. Come out."; behind the phone my door, now with FOUR foot shadows in the strip; hard cut to black | notify x2 at -4 dB; audio and picture cut together |

Stills checked: `out/stills/roommate_v2.jpg` (29 frames across the whole cut) and `out/stills/roommate_v3.jpg` (fixes:
DM header reads "iMessage" not "48 members", the 911 beat is Maya dialing, not the kit's incoming-call screen, and the
napkin line fits).

## Kit and pipeline gaps (none block this episode; each is solved in this folder)

| Gap | Where | Solved here by |
|---|---|---|
| pipeline/audio has one voice per script and no low-pass FX | all Dani lines | gen_audio.py: per-line Kokoro voice + ffmpeg chain, then the pipeline's own mix (read-only import) |
| No sizzle loop, sticky-latch double click, plate clink, handle jolt, slow handle turn, six counted steps, floor creak | S1-S10 | procedural SFX written by gen_audio.py to studio/public/episodes/<id>/sfx/ (original, CC0) |
| `horror/FrontDoor` always draws a peephole, chain, deadbolt and doormat (it is a front door) | every bedroom-door shot | inline SVG `door_svg()` (an interior door with a lever and no lock) |
| `FrontDoor.handle` is only a fast jiggle; no slow turn, no spring-back | s17, s19, s24, s31 | lever as its own SVG layer with eased `rotate` keyframes about its pivot |
| `horror/Bedroom` has no door; no kitchen set | s01, s08 | blurred `door_svg()` behind the phone; the kitchen is only heard, plus an SVG table-top with three plates |
| `horror/Phone` has no photo message kind | s28 | SVG photo card over the blurred thread |
| `horror/Phone` call mode is an incoming-call screen | s13 | Maya dialing (pose phone) + a red "9 1 1" callout |
| `Protagonist` has no back view | - | Dani is never shown in person; only the photo silhouette |

Worth upstreaming once `studio/src/kits/horror` and `pipeline/audio` unlock: an `interior` FrontDoor, a `handle`
turn mode, a Phone `photo` message, and `[voice: x]` / `[fx: lowpass=f]` paragraph markers in pipeline/audio/script.py.

## Posting and policy notes (research/R5 has no general policy file yet; see its horror disclosure block)

- TikTok: switch on the AI-generated content label (Kokoro TTS voices and code-drawn animation). YouTube: the
  altered/synthetic disclosure targets realistic content; this is cartoon fiction, so it is generally not required.
  Write the decision down in the episode's description.md when it is packaged.
- Runtime 81.8 s: over the TikTok Creator Rewards 1-minute floor; any re-cut must stay above 61 s.
- Template fatigue: this episode drops the low-battery lifeline (used in seven other horror scripts) and the
  repeated-name silence checks, and its hero is Maya, not the kit's default Nora. Keep varying the bookend and the
  "one image at ~88%" device across uploads.
- Sibling: do not post this and episodes/horror-roommate-two-rooms close together (see sibling_check).

## Originality (run 2026-11-01 ~12:10 UTC)

| Check | Command | Result |
|---|---|---|
| Corpus + library | `python3 scripts/originality_check.py <this> research/corpus research/library/transcripts` | PASS |
| Built episodes (incl. the sibling) | `python3 scripts/originality_check.py <this> episodes` | PASS |
| Other backlog horror scripts | same, against a copy of `backlog/horror/*/script.md` without this one | PASS (the first run failed on a 9-word run of shot-list boilerplate shared with horror-elevator-maintenance-chat; reworded) |
| Spoken lines only (audio/lines.json) | 5-gram share and longest run against every corpus, library, episode and backlog file | max 0.66% 5-grams (horror-group-chat-extra-member), longest run 6 words; corpus/library max run 4 words; the sibling episodes/horror-roommate-two-rooms 0.00% 5-grams, longest run 3 words ("don't come out") |
