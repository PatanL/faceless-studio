---
id: horror-group-chat-extra-member
niche: horror
part: 1 of 2
title: We Have No Night Security. Our Building Chat Does. (Part 1)
alt_titles: One Member Of Our Building Chat Isn't A Neighbour (Part 1) | Someone In Our Building Chat Always Knows Who's In The Hallway (Part 1)
format: 9:16 vertical, 2-part series, Part 1 ends on a cliffhanger, "PT 1" corner tag + 0.8 s "PART 2" card
target_runtime_s: 81 (measured 80.8 s mix from the Kokoro run of this file; window 76-86; never under 61 for Creator Rewards)
target_words: 307 spoken (measured by pipeline/audio/script.parse, beat headers are HTML comments and are not read)
target_wpm: 228 = 307 words / 80.8 s full runtime, measured the PLAYBOOK way (tools/pacing_stats.py, words / duration)
hook: core hook 28 words / 0:00-0:05.95 (contradiction "We have no night security" lands 0:01.95-0:03.1)
voice: af_heart
speed: 1.45
paragraph_pause: 0.05
music: dread
template: pipeline/templates/horror.md (T1 Locked-Door Siege, chat-thread variant), Shorts skeleton S1-S10 with B10/B11 from the story skeleton
engine: Locked-door siege with a compromised channel, two ladders (proximity + channel removal), headcount ritual as the signature
evidence: mraevq group-chat seed 7654526047005723937 717K (66.7x); udhwkz group-chat seed 7659677578365537569 376K (10.8x); Textify chat Short T42u5xhrq-0 869K (25.5x)
references:
  - id: 7659677578365537569
    url: https://www.tiktok.com/@udhwkz/video/7659677578365537569
    views: 376200
    outlier_score: 10.79
    why: SIEGE-CHAT, the closest structure (residents' chat as the weapon, a door the hero must not open, three channels). Borrowed the 22-words-in-6-s core hook shape (threat, signature rule, short texture line), the one odd checkable detail at the peephole (0:18-0:21), the visitor sensing the hero behind the door (1:11-1:15), the normal-sounding chorus plus one doubter with outside evidence (0:39-1:09), the authority silencing that doubter (2:21), peers then piling on the hero with imperatives (1:35-1:51), the isolation beat where only the enemy's channel still works (2:03-2:11), the lifeline asked the opening question under a countdown (3:17-3:41), and the outside source that falsifies the authority itself (3:58-4:01). No killer, no cop, no stickers, no burner phone, no muting, no unit 802.
  - id: T42u5xhrq-0
    url: https://www.youtube.com/shorts/T42u5xhrq-0
    views: 868500
    outlier_score: 25.54
    why: TEXT-FIGURE, the 60 s chat-Short timing reference and the source of the Shorts skeleton. Borrowed the named source by 5% (0:03), the warning stated then broken at once (0:15-0:17), the explicit foreshadow line just before the turn (0:29), the turn where the threat leaves the screen for my space at ~50% (0:31-0:33), the short distance rungs (0:44-0:47), the typography split (entity in calm sentence case, humans in lowercase, 0:56), and the last line turned on the phone owner (0:56-0:58). Different medium, characters, threat and wording.
  - id: 7654526047005723937
    url: https://www.tiktok.com/@mraevq/video/7654526047005723937
    views: 716900
    outlier_score: 66.69
    why: SIEGE-OVERLAY, the corpus's top outlier and the exact phone-chat format the kit is built for. Borrowed only its first 12 s: the building chat brought in at once, the trusted-looking authority contradicted inside the hook (0:07-0:10), and a casualty count that makes the threat a pattern by 0:12. Its omniscient overlay chorus, game frame, phone-under-the-bed, ambush plan and villain-eavesdrop ending are NOT used.
---

# We Have No Night Security. Our Building Chat Does. (Part 1)

**Premise.** Larkspur Court's residents' chat has a member called Night Security. The building has no night security.
Ask the chat "who's in the hallway?" and Night Security answers in one second with a headcount and a name, and it is
never wrong. Its bio holds two rules: ask me, and never use your peephole. Two C used hers in March and that flat has
been empty since. At 1:12 a.m. footsteps stop outside Nora's door (5B, she lives alone). Night Security says "One. Mr.
Okafor, next door." She breaks rule two: it is Mr. Okafor, facing her door, not blinking. Then a private message: "You
looked, 5B. So did 2C." The admin brings outside evidence (the account joined two days before the chat existed) and
Night Security removes her from the group. Then it answers a question nobody asked: "One. Floor 8, by the stairs. Me."
Floor 7, 6, 5. The footsteps stop at her door, 911 has no signal, only the chat sends. The peephole is covered, and the
black blinks. Night Security posts a 20-second door check; the neighbours she trusted tell her to open. Mr. Okafor
answers her DM: he has been asleep since nine, there is no Night Security in his chat, nobody has posted since Friday.
She asks the only question it answers, about her own flat: "Who's in 5B?" It answers: "Two."

**Why this is not a second "member 41".** `episodes/horror-member-41` (built) owns the 40-flats/41-members count, the
"keeps coming back" admin and the "please open, for your safety" door ending. This script drops all three:
- **Title formula:** a contradiction stated as the title (no member count anywhere in the title, hook or VO).
- **Admin beat:** the admin is the viewer-proxy doubter with outside evidence, and the entity removes *her*. Nobody tries to remove the entity.
- **Ending:** the door never opens and nobody asks her to open it as the last line. The ritual is turned on her own flat ("Who's in 5B?" "Two."). The threat moves past the door, into the room.
- Also not `horror-pinned-rules` (no pinned rules post, no "only one person out there" peephole ending) and not
  `horror-new-building-rules` (no rules list from a dissolved management company).

**Ownable signature.** The headcount ritual: ask "who's in the hallway?", get "a number, a name, in one second".
The viewer can track it, and the last line pays it with the one count the viewer can check (she lives alone).

**Plants.**
1. "A number, a name" (0:04) + "home alone" (0:11) -> "Who's in five B?" "Two." (1:18.4). Paid (count-match, inverted).
2. Bio rule 2 "Never use your peephole" (0:07) -> broken at 0:18 and 0:53. Paid twice.
3. "Two C used hers in March... empty since" (0:08-0:10) -> "You looked, five B. So did two C." (0:24-0:25). Paid as the first threat to her.
4. Profile "Unit: — · Joined Mar 1" (0:06, on screen) -> Mrs. Petrov: it joined two days before this chat existed (0:29-0:32). Paid.
5. "Not once had it said where it was" (0:38) -> "Floor eight, by the stairs. Me." (0:43-0:44). Paid.
6. "Not blinking" (0:21) -> the covered lens blinks (0:56.2 picture, 0:57.4 VO). Paid as a contrast: the one that did not blink is the one that does.
7. **Unpaid for Part 2:** what happened to 2C and to Mrs. Petrov after the removal; 214 answers since March; why Okafor's
   chat has been silent since Friday (so whose chat is Nora in?); the door-check chip still running at the cut (0:02
   left); who the second one in 5B is.

**Loops.** L1 who is Night Security (0:01, open); L2 what happens if you look (0:08, closed 0:10 "empty since", re-armed
0:24); L3 who is at my door (0:13 -> 0:15 "Okafor" -> re-opened 1:12, open); L4 can anyone stop it (0:29, closed 0:34:
no, it removed the admin); L5 where is it (0:38 -> 0:43 -> 0:50, closed: at my door); L6 will help come (0:50.6,
closed 0:51.5: no signal); L7 is my chat even real (1:14, open); L8 who is the second one in 5B (1:18.4, open). Eight
opened (5.9/min, inside the 60 s Shorts 6-8 band), **four open at the cut** (L1, L3, L7, L8). Every loop opened before 50% is
closed or re-armed before 50%.

## Pacing vs PLAYBOOK (measured, Kokoro af_heart, speed 1.45 narrator / 1.3 Night Security / 1.38 Okafor)

Every number below comes from the TTS word stamps of this exact narration block (Spark CPU run, ~12:30 UTC, saved in
`audio/captions.json` and `audio/report.json`), not from a words-per-second assumption. The hook paragraph runs at
1.5, the narrator at 1.45.

| Metric | PLAYBOOK target | This script (measured) |
|---|---|---|
| Runtime | Shorts 50-100 s / Part 1 60-90 s | 80.8 s (last word at 78.4 s, held breath, black, then the PART 2 card) |
| Words / wpm | narrated 230-270 (words / full duration) | 307 / 80.8 s = **228 wpm**, 2 wpm under the band floor and above the controls' median of 213 (240 wpm with the 4.3 s of planned silence removed, stated only for comparison; the PLAYBOOK metric is the first number) |
| Line 1 | <=12 words, place/object + danger | 9 words: "Our building chat has a member called Night Security." |
| Core hook | <=30 words, <=6 s | **28 words, 0:00-0:05.95** (to "Never wrong.") |
| Trusted source contradicted | <=11 s | "We have no night security" at **0:01.95-0:03.1** |
| Casualty / stakes | H11: casualty proof by ~8 s | "Two C used hers in March" 0:08.4, "has been empty since" 0:09.6-0:10.6 |
| Jolt interval | Shorts median 2.5-3.5 s, never >8 s | 34 jolts in 81 s, median ~2.3 s, longest gap 3.3 s (the held peephole, which carries the blink) |
| Re-hook / bubble rate | chat ~1.1 s per bubble, panel reset 6-9 s | 26 bubbles + 3 system lines + 2 banners + 1 call screen; picture change median ~2.6 s |
| Named threat / premise paid | S2 by ~12% | named at 0:01 (1%), premise paid by 0:05.95 (7%) |
| Rule broken | S4 23-38% | 0:18.4 (23%) |
| Exit closed | S5 38-50% | the admin is removed at 0:34.3 (42%) |
| Midpoint turn | S6 43-55% | it posts unasked and names itself, 0:39.8-0:44.2 (**49-55%**), the only full-frame colour flash on "Me." (0:43.9) |
| Proximity ladder | S7 50-78% | Floor 8, 7, 6, 5, my door, 0:43-0:50 (53-62%), then past the door at 1:18.4 |
| Channel-removal ladder | two ladders together (§8) | admin removed (42%) -> nobody replies (58%) -> no signal, only the chat sends (63-65%) -> it is inside the Okafor DM (84%) -> the real chat has been silent since Friday (92%) |
| Scariest image | once, 60-80%, held ~4 s | covered peephole 0:53.9-0:57.9 (**67-72%**), fully still for 3.5 s, heartbeat from the first frame of the hold (0:55.0), the black lens blinks at 0:56.2 |
| Lifeline under a clock | 70-90% | 20-second door check + DM to Okafor, 1:00.2-1:11.1 (74-88%) |
| Truth twist | 85-95% | Okafor: asleep since nine, no Night Security in his chat, nobody posted since Friday, 1:11.9-1:15.6 (**89-93%**) |
| Ending | cut at greatest need, bookend frame 0, part label | "Who's in five B?" "Two." at 1:18.4 (97%), framed exactly like frame 0, the hall light under the door goes out; PT 1 corner tag all video + 0.8 s PART 2 card |
| Numbers / min | narrated 3-5, chat 0-1 | ~19/min. Over target, on purpose: unit labels are the building map (SIEGE-CHAT's "[name] from [unit]" device) and the count is the signature. "Five A" is never spoken (it is "Mr. Okafor, next door") so 5A/5B can't be confused by ear |
| Sentence median | 6-9 words, 3-5-word punches at spikes | median 6; punches: "Never wrong." "Not blinking." "So did two C." "Nobody typed." "Me." "No signal." "Covered." "It blinked." "Two." |
| "You" share | first-person narrated 3-13% | 3.8% (3 of 79 sentences, all inside messages: "your peephole", "You looked", "Was that you"); classified as first-person narrated, not dialogue-heavy |
| Timed silences | 1-3, with SFX | 0.3 s between floors, 2.2 s inside the peephole hold (heartbeat + the blink click), 0.5 s on "Okafor was typing", 0.9 s held breath before the card |
| Open loops | 3-6 open at the cut for a series | 8 opened, 4 open at the cut |

## Beat alignment

One skeleton: the Shorts beats S1-S10 (PLAYBOOK §1B) for an 81 s chat Short, plus B6/B10/B11 from the story skeleton
(§1A), which the Shorts table has no slot for. Reference timestamps re-checked against `research/corpus/horror/<id>.md`.

| Our beat | Our time (% of 81 s) | Reference id + timestamp (% of its runtime) | Device borrowed | How we adapt it |
|---|---|---|---|---|
| S1 Hook: trusted thing contradicted | 0:00-0:03.1 (0-4%) | 7654526047005723937 0:00-0:10 (0-3%); 7659677578365537569 0:00-0:06 | Threat in "our" building in line 1 with the chat brought in at once; a trusted-looking authority contradicted inside the hook; core hook ~22-30 words in 6 s | The authority *is* a chat member, and the narrator kills it in 5 words at 0:02 |
| S2 Named threat + signature | 0:03.2-0:05.95 (4-7%) | T42u5xhrq-0 0:03 (5%); 7659677578365537569 0:02-0:04 | Name the source of the danger by ~5%; give it a signature, then a short texture line | The signature is a ritual the viewer can track: a number, a name, in one second. Texture line "Never wrong." |
| S3 Setup + plant (rules + casualty) | 0:06.2-0:10.6 (8-13%) | 7654526047005723937 0:12 (3%); T42u5xhrq-0 0:15-0:17 (25-28%) | A casualty count that turns the threat into a pattern; a warning the viewer will see broken | Two rules in its bio (no pinned post, no numbered list), and one countable casualty: 2C looked, 2C is empty |
| S3 Intrusion at the barrier | 0:10.9-0:18.0 (13-22%) | 7659677578365537569 0:11-0:16 (4-6%) | The threat arrives at my door right after the set-up; the hero turns to the channel | Footsteps stop at 5B; she asks the ritual question; the answer comes in one second and names her neighbour |
| S4 Rule broken + one odd detail | 0:18.4-0:22.6 (23-28%) | 7659677578365537569 0:18-0:21 (7-8%); T42u5xhrq-0 0:17 (28%) | Peephole look with one odd, checkable detail; the warning broken right after it is given | It is Okafor, as promised, facing her door, not blinking. Nothing else is wrong with him, so the oddity stays small and unexplained until 1:12 |
| S4 Rung: it knows (identifier match) | 0:22.8-0:25.6 (28-32%) | 7659677578365537569 1:11-1:15 (28-30%) | The visitor senses the hero behind the door | Private message: "You looked, five B. So did two C." The viewer matches the planted 2C (T7) and knows what happened to the last one who looked, at 31% |
| S5 Chorus, doubter, exit closed | 0:25.8-0:36.4 (32-45%) | 7659677578365537569 0:39-1:09 (16-28%) and 2:21 (56%) | Normal-sounding neighbours; one doubter with outside evidence; the authority silences the dissent | 9D defends it (it found her cat); Mrs. Petrov, the admin, brings the landlord's join date and tries to remove it; it removes her. The viewer-proxy speaks the objection and is shut down |
| S5 Foreshadow line | 0:36.7-0:39.5 (45-49%) | T42u5xhrq-0 0:29 (48%) | One explicit foreshadow right before the turn (no lull: the 60 s chat hit has none) | "Two hundred fourteen answers since March. Not once had it said where it was." |
| S6 Turn at ~50% | 0:39.8-0:44.2 (49-55%) | T42u5xhrq-0 0:31-0:33 (52-55%) | The threat leaves the screen for my space; the video's one full-frame colour flash | It answers a question nobody asked, and for the first time the answer is where it is: "One. Floor eight, by the stairs. Me." |
| S7 Proximity ladder | 0:44.4-0:50.4 (55-62%) | T42u5xhrq-0 0:44-0:47 (73-78%) | Distance shrinks in short rungs, ~1.5 s apart | Floor 7, Floor 6, Floor 5, then the footsteps stop at my door. Ours runs earlier in the band (S7 is 50-78%) so the image, clock and twist all fit after it |
| S7 Silence rung | 0:46.7-0:47.9 (58-59%) | 7659677578365537569 1:04-1:09 (26-28%) | The unanswered post shows the room is controlled | "Everyone saw it. Nobody replied." Header reads "Seen by 36"; no typing dots anywhere |
| B6 Isolation | 0:50.6-0:53.0 (63-66%) | 7659677578365537569 2:03-2:11 (49-53%) | No signal; only the enemy's channel still works | "I called nine one one. No signal. Only the chat would send." Later than the story band (40-55%) because a Short has no room before its turn |
| S9/B9 Scariest image, held | 0:53.3-0:57.9 (66-72%) | PLAYBOOK B9 (one image, 60-80%, held ~4 s; SIEGE-OVERLAY's peak at ~72%) | One image, late, held still | Rule 2 broken again: the lens is covered. 3.5 s still hold with heartbeat; inside it the black goes slightly lighter and back (a blink) with a wet glint, then "It blinked." |
| B10 Lifeline under a clock + peer pressure | 1:00.2-1:11.1 (74-88%) | 7659677578365537569 3:17-3:41 (79-89%) and 1:35-1:51 (38-44%) | A countdown starts; the hero asks the opening question to the one outside source; peers pile on with imperatives | A 20-second door check; 9D, 7C and 3D tell her to open (the people who defended it, T9); she DMs Okafor and Night Security is already in that DM |
| B11 Truth twist (outside check) | 1:11.9-1:15.6 (89-93%) | 7659677578365537569 3:58-4:01 (96%) | A concrete detail from an outside source falsifies the authority itself, not just the visitor | Okafor: asleep since nine (so the "correct" 1:12 answer was a lie), no Night Security in his chat, nobody has posted since Friday (so the whole thread she has been reading may not be the building's) |
| S10 Twist on "you" + bookend | 1:15.8-1:20.8 (94-100%) | T42u5xhrq-0 0:56-0:58 (93-97%); 7659677578365537569 4:05-4:08 | The last line turns the threat on the phone owner; a last-second message; last shot = first shot | Her own question, the ritual pointed at her flat: "Who's in five B?" "Two." Same phone framing as frame 0, the hall light under the door goes out, held breath, PART 2 card |

## Script

**Hook.**
- First line (VO + caption, 0:00): "Our building chat has a member called Night Security."
- First visual (frame 0, also the cover): a hand holding the phone in front of her own front door, seen from inside,
  the hall light a bright line under it. The chat "Larkspur Court Residents" is open; the newest bubble is the grey
  shield avatar, Night Security: "Nobody. Go back to bed, 3D." (3D never said she was in bed.) A red scrawl beside the
  avatar: "we have no night security". The threat (an account that sees the hallway) and the barrier (the door) are
  both in frame 0.

**Voices.** One narrator voice (af_heart) reads everything, so Night Security must never sound like Nora:
- **Required:** every Night Security line is its own paragraph at `[speed: 1.3] [vox: -3]` (slower, quieter, flat),
  and every one is announced by the line before it ("One second later:", "Then a private message.", "Then it posted",
  "Then, to the whole group:", "So I asked it..."). "Me." at 0:44 is therefore heard as the entity, not as Nora.
- Okafor's reply is a third light variation: `[speed: 1.38] [vox: -1]`, attributed by "Okafor was typing."
- When `pipeline/audio/script.py` gets a per-paragraph `[voice: ...]` marker (owned by the horror closeout lane while
  `pipeline/audio/` is locked), put Night Security on `am_puck` and keep the speed and gain marks.

Markup: `[pause: n]` = n s of silence; `[sfx: name @+s]` fires s seconds after the next spoken word (or the end of the
paragraph). Unit labels are spoken as "five B"; the phone shows "5B". Beat headers are HTML comments, which the parser
strips, so nothing in them is read aloud.

```narration
<!-- S1 HOOK -->
[music: dread] [speed: 1.5] Our building chat has a member called Night Security. We have no night security. [sfx: drone] Ask who's in the hallway. [sfx: message_pop] A number, a name, in one second. [sfx: message_pop] Never wrong.

<!-- S3 RULES + CASUALTY -->
[speed: 1.45] Its bio says: [sfx: pop] Ask me. Never use your peephole. Two C used hers in March. Two C has been empty since. [sfx: stinger vol=-10]

<!-- S3 INTRUSION -->
Tonight at one twelve, home alone, I heard footsteps stop outside my door. Five B. I asked. [sfx: message_send] One second later:

[speed: 1.3] [vox: -3] [sfx: message_pop] One. Mr. Okafor, next door. Taking out recycling.

<!-- S4 RULE BROKEN -->
[speed: 1.45] I broke the rule. [sfx: breath vol=-6] Through the peephole, it was Mr. Okafor. Facing my door. [sfx: heartbeat_slow vol=-14] Not blinking. Then he was gone. [sfx: phone_buzz] Then a private message.

[speed: 1.3] [vox: -3] You looked, five B. So did two C. [sfx: stinger]

<!-- S5 CHORUS + ADMIN -->
[speed: 1.45] [sfx: message_send] I asked the group who runs it. [sfx: message_pop] Nine D: leave it alone, it found my cat. [sfx: message_pop] Mrs. Petrov, our admin: the landlord says that account joined two days before this chat existed. Removing it.

A grey line. [sfx: pop] [sfx: glitch vol=-8] Night Security removed Mrs. Petrov. Nobody typed. Two hundred fourteen answers since March. Not once had it said where it was.

<!-- S6 TURN -->
Then it posted, [sfx: notify] and nobody had asked.

[speed: 1.3] [vox: -3] Who's in the hallway? One. Floor eight, by the stairs. [sfx: glitch] Me. [sfx: drone]

<!-- S7 LADDER -->
[vox: -3] [sfx: pop] [sfx: footsteps vol=-12] Floor seven. [pause: 0.3] [sfx: pop] Floor six.

[speed: 1.45] Everyone saw it. Nobody replied.

[speed: 1.3] [vox: -3] [sfx: pop] [sfx: footsteps vol=-4] Floor five.

[speed: 1.45] The footsteps stopped outside my door. [sfx: impact vol=-12] I called nine one one. No signal. Only the chat would send.

<!-- S9 SCARIEST IMAGE -->
I looked again. The peephole was black. Covered. [sfx: heartbeat_slow] [sfx: click @+1.2 vol=-6] [pause: 2.2] It blinked. [sfx: stinger]

[speed: 1.3] [vox: -3] [sfx: message_pop] Step back from the peephole, five B.

<!-- B10 LIFELINE UNDER A CLOCK -->
[speed: 1.45] Then, to the whole group: [sfx: notify]

[speed: 1.3] [vox: -3] Door check. Five B. Twenty seconds. [sfx: clock_ticking]

[speed: 1.45] [sfx: message_pop] Nine D: just open it, five B. It's never wrong. [sfx: message_pop] Then seven C. [sfx: message_pop] Then three D. [sfx: clock_ticking vol=-4] I texted Mr. Okafor. [sfx: glitch vol=-12] Night Security was in that chat too. [sfx: message_send] Was that you at my door? [sfx: typing] Okafor was typing. [sfx: clock_ticking vol=-4] [pause: 0.5]

<!-- B11 TWIST -->
[speed: 1.38] [vox: -1] [sfx: message_pop] I've been asleep since nine. What Night Security? Nobody's posted in our chat since Friday. [sfx: stinger @+0.2]

<!-- S10 CLIFF -->
[speed: 1.45] So I asked it the only thing it answers. [sfx: message_send] Who's in five B?

[speed: 1.3] [vox: -3] [sfx: message_pop] Two. [sfx: breath @+0.4 vol=-2] [pause: 0.9]
```

### Line-by-line timing and on-screen text

Times are the measured Kokoro word stamps of the final run (`audio/captions.json`, first word of each line). On-screen chat typography: humans type in
lowercase, Night Security always answers in calm sentence case (TEXT-FIGURE's register split); Nora's own messages go
from "who's in the hallway?" to "was that you at my door??" as the ladder climbs.

| t | VO / caption line | Beat | On-screen text (phone UI, RedText, callouts) |
|---|---|---|---|
| 0:00.1 | Our building chat has a member called Night Security. | S1 | Chat "Larkspur Court Residents · 38 members"; newest bubble Night Security: "Nobody. Go back to bed, 3D." under "Ama · 3D: someone's in the hall??"; RedText scrawl "we have no night security" (frame 0, the episode's one RedText) |
| 0:01.95 | We have no night security. | S1 | — (scrawl stays) |
| 0:03.2 | Ask who's in the hallway. | S2 | "Leo · 7C: who's in the hallway?" (3.3) |
| 0:04.2 | A number, a name, in one second. | S2 | Night Security: "One. Delivery for 7A. Leaving now." (4.2, no typing dots, same minute as 7C's question) |
| 0:05.5 | Never wrong. | S2 | Punch-in on the grey shield avatar |
| 0:06.2 | Its bio says: Ask me. Never use your peephole. | S3 | Header swaps to "Night Security · Unit: — · Joined Mar 1"; bio bar (kit `pinned`, label BIO): "Ask me. / Never use your peephole." |
| 0:08.4 | Two C used hers in March. Two C has been empty since. | S3 | Hallway, door plate "2C", no light under it |
| 0:10.9 | Tonight at one twelve, home alone, I heard footsteps stop outside my door. Five B. | S3 | Phone clock "1:12"; label "5B" on the door; feet shadow under the door from 0:12.2 |
| 0:13.9 | I asked. One second later: | S3 | Me (Nora · 5B): "who's in the hallway?" (14.0) |
| 0:15.6 | One. Mr. Okafor, next door. Taking out recycling. | S3 | Night Security: "One. Mr. Okafor, next door. Taking out recycling." (15.6, no typing dots) |
| 0:18.4 | I broke the rule. | S4 | — |
| 0:19.1 | Through the peephole, it was Mr. Okafor. Facing my door. Not blinking. | S4 | — (peephole POV, Okafor, eyes fixed on the lens) |
| 0:22.0 | Then he was gone. Then a private message. | S4 | Empty peephole; lock-screen notification "Night Security · private message" (23.3) |
| 0:24.0 | You looked, five B. So did two C. | S4 | DM: "You looked, 5B." (24.0) / "So did 2C." (24.8) |
| 0:25.8 | I asked the group who runs it. | S5 | Me: "who actually runs night security??" (25.9) |
| 0:27.1 | Nine D: leave it alone, it found my cat. | S5 | "Dana · 9D: leave it alone it found my cat 🐈" (27.1) |
| 0:29.3 | Mrs. Petrov, our admin: the landlord says that account joined two days before this chat existed. Removing it. | S5 | "Mrs. Petrov · 1A · admin: Landlord says that account joined 2 days before this chat existed. Removing it." (29.3) |
| 0:33.6 | A grey line. Night Security removed Mrs. Petrov. Nobody typed. | S5 | System line "Night Security removed Mrs. Petrov (1A)" (34.3) |
| 0:36.7 | Two hundred fourteen answers since March. Not once had it said where it was. | S5 | Search view "Night Security · 214 results", day chip "Mar 3", old answers scroll by |
| 0:39.8 | Then it posted, and nobody had asked. | S6 | Back in the group; unread badge +1 (40.0); no question above it |
| 0:41.6 | Who's in the hallway? One. Floor eight, by the stairs. Me. | S6 | Night Security: "Who's in the hallway? One. Floor 8, by the stairs. Me." (41.6); full-frame glitch on "Me." (43.9) |
| 0:44.4 | Floor seven. Floor six. | S7 | Stair sign "7", then "6"; bubbles "Floor 7." (44.4) "Floor 6." (45.8) |
| 0:46.7 | Everyone saw it. Nobody replied. | S7 | Header "Seen by 36"; no typing dots anywhere |
| 0:48.3 | Floor five. | S7 | Stair sign "5"; banner "Night Security: Floor 5." |
| 0:49.3 | The footsteps stopped outside my door. | S7 | — (the shadow under the door returns) |
| 0:50.6 | I called nine one one. No signal. Only the chat would send. | B6 | Call screen "911 · No signal · Call failed"; then the chat input bar, the only thing that works |
| 0:53.3 | I looked again. The peephole was black. Covered. | S9 | — (held black lens, faint rim; the black lightens and goes back at 56.2, a wet glint on the rim) |
| 0:57.4 | It blinked. | S9 | — |
| 0:58.2 | Step back from the peephole, five B. | S9 | DM: "Step back from the peephole, 5B." |
| 1:00.2 | Then, to the whole group: | B10 | Banner "Larkspur Court Residents" |
| 1:01.3 | Door check. Five B. Twenty seconds. | B10 | Night Security: "Door check. 5B. 20 seconds."; countdown chip "0:20" starts at 1:02.5 and ticks every second to the cut |
| 1:03.3 | Nine D: just open it, five B. It's never wrong. Then seven C. Then three D. | B10 | "Dana · 9D: just open it 5B its never wrong" / "Leo · 7C: open it" / "Ama · 3D: open it 5B" |
| 1:06.5 | I texted Mr. Okafor. Night Security was in that chat too. | B10 | New DM "Mr. Okafor · 5A · last seen 9:02 PM"; system line "Night Security is in this chat" (67.8) |
| 1:09.3 | Was that you at my door? Okafor was typing. | B10 | Me: "was that you at my door??" (69.3); "Mr. Okafor is typing…" (70.4) |
| 1:11.9 | I've been asleep since nine. What Night Security? Nobody's posted in our chat since Friday. | B11 | Okafor: "ive been asleep since 9. what night security?? nobodys posted in our chat since friday" (71.9) |
| 1:15.8 | So I asked it the only thing it answers. Who's in five B? | S10 | Whip back to the group chat, framed exactly like frame 0; me: "who's in 5B?" (77.3) |
| 1:18.4 | Two. | S10 | Night Security: "Two." (78.4); the light line under the door goes out (78.6); chip reads 0:05, then 0:04; cut to black 79.6; PART 2 card 79.8-80.8 |

## Shot list

Global episode times below; `storyboard.json` (written alongside by `gen_storyboard.py` from `audio/captions.json`,
valid against `studio/src/core/schema.ts`, 28 scenes, 80.87 s) converts every prop time to **scene-local seconds**
(kit rule: "Times in props are scene seconds"). Stills checked on the Spark: `out/stills/horror-group-chat-extra-member_storyboard.jpg`,
`_fix.jpg`, `_blink.jpg`. The audio (mix.wav etc.) is in `dgx-spark:~/studio/app/studio/public/episodes/horror-group-chat-extra-member/`. Members map for every chat: Night Security {color "#4b5563",
initials "🛡️"} (Noto Color Emoji is installed on the Spark), Nora · 5B (me), Mr. Okafor · 5A, Leo · 7C, Ama · 3D,
Dana · 9D, Mrs. Petrov · 1A · admin. Mr. Okafor = `horror/Neighbour` recoloured (`colors {hair "#1b1716", skin
"#7a4e33", top "#3e5872", topShade "#2c3f52", shirt "#d9d2c3"}`, `blink` false); he keeps the Neighbour's face shape,
so reuse the same recolour in Part 2. A `PT 1` pill (core text layer, depth 0) sits bottom-left (x 120, y 1440) in
every scene.

| t_start | t_end | Shot | Visual (kit vocabulary, no new code) | Camera | SFX (placed by the mix, report.json) |
|---|---|---|---|---|---|
| 0.0 | 6.15 | Phone over the front door (cover) | `horror/HandPhone` (cx 0.53, cy 0.61, phoneWidth 0.68, tilt -3) over a `horror/FrontDoor` layer (blur 8, opacity 0.75, chain on, hallLight 0.9). Chat as in the timing table; Night Security bubbles never show typing dots. `horror/RedText` scrawl from -0.3. | slow push 1.00 -> 1.04, step punch-in on the avatar at 5.5 | drone 3.1, message_pop 4.2 and 5.5 |
| 6.15 | 8.35 | Phone, profile + bio | Same phone: `title` "Night Security", `subtitle` "Unit: — · Joined Mar 1", `pinned {label "BIO", text "Ask me.\nNever use your peephole.", lines 2, at 0.3}` | static | pop 6.8 |
| 8.35 | 10.87 | Set, the empty flat | `horror/Hallway` lights 1, figure 0, runner true, `horror/Flicker` 0.1; core rect + text plate "2C" on the near-left door | slow dolly 1.0 -> 1.06 | stinger 10.7 |
| 10.87 | 13.85 | Set, barrier | `horror/FrontDoor` chain on, hallLight 1, `feet [1.3, 3.0]` (shadow arrives with "footsteps"); callout label "5B" at 2.55; `horror/Darkness` | slow push | footsteps (auto) 12.2 |
| 13.85 | 18.4 | Phone, the ritual | HandPhone chat, `clock` "1:12", me bubble 14.0, Night Security bubble 15.6 (no dots) | push 1.0 -> 1.05 | message_send 14.5, message_pop 15.6 |
| 18.4 | 19.12 | Character | `horror/Protagonist` expr suspicious, pose idle, lookX 0.5, over `horror/FrontDoor` (blur 4) | push-in 1.0 -> 1.08 | breath 19.1 |
| 19.12 | 22.0 | Peephole POV | `horror/Peephole` figure neighbour (Okafor colours), expr blank, `blink` false, lookX 0, lookY 0, lean 0.45, flicker 0.1 | slow push 1.0 -> 1.04 (fisheye hold) | heartbeat_slow 21.2 |
| 22.0 | 22.82 | Peephole, empty | `horror/Peephole` figure none, flicker 0.2 | static | — |
| 22.82 | 25.8 | Phone, DM | HandPhone `screens` lock -> chat at 0.9; lock `notifications` at 0.45; chat `dm` "Night Security", bubbles 24.0 and 24.8; `vibrate` at 0.45; `horror/Glitch` 0.2 s at 25.3 | shake 0.2 s, amplitude 12 at 25.3 | phone_buzz 22.8, stinger 25.6 |
| 25.8 | 33.63 | Phone, chorus + admin | Group chat over `horror/LivingRoom` (blur 8): me 25.9, 9D 27.1, typing Petrov 28.6-29.3, Petrov 29.3 | static, slow push from 29.3 | message_send 25.8, message_pop 27.1, 29.3 |
| 33.63 | 36.7 | Phone, removal | Same chat, system line 34.3; HandPhone `glitch` 0.2 s at 34.3 | static, tremble 0 | pop + glitch 34.3 |
| 36.7 | 39.84 | Phone, search | Chat `title` "Search: Night Security", `subtitle` "214 results", `dayLabel` "Mar 3", 8 old Night Security answers at negative times plus 2 arriving inside the shot so the list moves | slow drift | cut whoosh |
| 39.84 | 44.44 | Phone, turn | Group chat; `unread` badge +1 at 0.2; Night Security bubble 41.6; full-frame `horror/Glitch` 0.25 s amount 0.9 at 43.9 (the one colour flash) | shake 0.25 s, amplitude 16 at 43.9 | notify 40.5, glitch 43.9, drone 44.2 |
| 44.44 | 45.77 | Set, ladder | `horror/Stairwell` floor "7", exit true, flicker 0.3, `horror/Darkness` radius 0.4 | quick push | pop + footsteps 44.4 |
| 45.77 | 46.66 | Set, ladder | `horror/Stairwell` floor "6" | quick push | pop 45.8 |
| 46.66 | 48.34 | Phone, silence | Group chat: "Floor 7." "Floor 6." posted; `subtitle` "Seen by 36"; no typing | static, no tremble | — (room tone) |
| 48.34 | 49.25 | Set, ladder | `horror/Stairwell` floor "5", flicker 0.4; core callout banner "Night Security: Floor 5." | static | pop + footsteps 48.3 |
| 49.25 | 50.61 | Set, barrier | `horror/FrontDoor` chain on, hallLight 1, `flicker` 0.3, `feet` from 0.1 | slow push | footsteps (auto) 49.3, impact 50.6 |
| 50.61 | 53.34 | Phone, isolation | HandPhone `screens` call -> chat at 1.55: `call {name "911", sub "No signal", label "Call failed"}`; then the group chat input | static | — |
| 53.34 | 53.93 | Character | `horror/Protagonist` expr terrified, pose idle, light none, lookX 0.6 | push-in 1.0 -> 1.1 | — |
| 53.93 | 58.24 | **Scariest image, held still** | `horror/Peephole {figure 'none', exposure 0.03, flicker 0, surround '#26272d'}` (the grey door around the lens makes the black read as a covered lens, not a dropped frame); a second identical Peephole layer at exposure 0.6 whose opacity keyframes go 0 -> 0.85 -> 0 over 56.05-56.45 (the blink); core `circle` glint r 9 px on the rim, opacity flash 56.15-56.5; `horror/Heartbeat` bpm 70 -> 90 from 1.0; `horror/Vignette` 0.6 | **no move** (the only fully still shot) | heartbeat_slow 55.0, click 56.2, stinger 57.9 |
| 58.24 | 60.17 | Phone, DM | Night Security DM, bubble at 58.24; `vibrate` | static, tremble 4 | message_pop 58.2 |
| 60.17 | 63.31 | Phone, door check | Group chat; `banners` at 0.55; Night Security bubble 61.3; countdown chip starts 62.5 (core text layers, one per second, at x 50% y 29% above the phone header) | slow push | notify 61.0, clock_ticking 63.0 |
| 63.31 | 66.47 | Phone, the neighbours turn | Group chat: 9D 63.3, 7C 65.4, 3D 66.0; chip continues | static, tremble 3 | message_pop 63.3, 65.4, 66.0 |
| 66.47 | 71.89 | Phone, lifeline | DM `dm` "Mr. Okafor", `subtitle` "5A · last seen 9:02 PM"; system line 67.8; me 69.3; typing Okafor 70.4-71.9; chip continues | slow push | clock_ticking 66.5, glitch 67.8, message_send 69.3, typing 70.4, clock_ticking 71.2 |
| 71.89 | 75.78 | Phone, twist | Okafor bubble 71.9; `horror/Glitch` 0.2 s at 73.2 on "what night security??" | push-in 1.0 -> 1.12 | message_pop 71.9, stinger 75.8 |
| 75.78 | 79.6 | **Bookend** | Core `whip` into the group chat framed exactly like 0.0 (same HandPhone and FrontDoor layer); me 77.3, Night Security "Two." 78.4; a second FrontDoor layer with hallLight 0 fades in over 78.6-78.9 (the light under the door goes out); chip reads 0:05 -> 0:04 | slow push 1.00 -> 1.04 (same move as 0:00) | message_send 77.3, message_pop 78.4, breath 79.3 |
| 79.6 | 80.8 | Card | Black, then `horror/EndCard {rule "Who's in 5B?", from "Night Security", sub "is typing…", label "PART 2", at 0.2}` | — | — (bed out) |

## Kit needs

None are blocking; every row above renders with today's kit (checked against `studio/src/kits/horror/README.md`,
`Phone.tsx` and `backgrounds.tsx`). Optional polish, each under ~20 lines:
- `chat.countdown {from, at}` header chip in `Phone.tsx` (replaces the per-second text layers).
- A `horror/Hallway` `walk {from, to, at, dur}` prop (not needed in this version: the visitor never walks on screen).
- A door number plate prop on `horror/FrontDoor`/`horror/Hallway` (the core rect + text layers do it today).
- A `[voice: am_puck]` paragraph marker in `pipeline/audio/script.py` (locked to the horror closeout lane for now).

## Part 2 hand-off

- **Cold open, hook in <=3 s, no recap:** start on the chip at 0:05 and the word "Two." in the chat; the first spoken
  line restates the stakes for cold viewers in fresh words; title findable alone ("...(Part 2)").
- **Pay by ~45% of Part 2:** whose chat Nora has been reading (Okafor's has been silent since Friday), or what
  happened to 2C. Then open a bigger loop. Upload order per PLAYBOOK §5: Part 2 goes up first so Part 1 tops the grid.
  Do not post this Part 1 until a Part 2 script and render exist.
- Keep the headcount ritual as the series signature; the "second one in 5B" belongs to Part 2's midpoint, not its hook.

## Originality and policy notes

- No corpus premise reused: no killer in the complex, no fake police officer, no stickers, no admin muting the chat, no
  burner phone or battery call, no unit 802, no overlay chorus, no livestream, no death game. The headcount ritual, the
  two-line bio, 2C's empty flat, the removed admin, the floor-by-floor self-report, the blinking covered lens, the
  silent-since-Friday chat and "Two." are ours.
- Devices borrowed (structure only) are listed in the beat table. Wording is original; `scripts/originality_check.py`
  prints PASS (see `review.json`).
- Catalog variety: this is now the only horror script whose climax is not a door being opened, a peephole figure or
  "open up" (the 10 siblings flagged by the originality review). "For your safety" is not used.
- Policy (research/R5/report.md): fiction in flat 2D cartoon with a generic TTS narrator needs no altered-content
  disclosure on YouTube or TikTok; the risk R5 names is templated, low-variation series, which is why the title
  formula, admin beat and ending were changed rather than reskinned. 81 s clears TikTok's over-one-minute Creator
  Rewards rule. Set "made for kids" to No.
