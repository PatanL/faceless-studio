---
id: horror-new-building-rules
niche: horror
series: 2 parts. Post Part 2 first, then Part 1 a few seconds later so Part 1 sits on top of the grid (PLAYBOOK §5). Each part hooks cold viewers on its own.
title_p1: Never Give Anyone Your Unit Number (Part 1/2)
title_p2: Someone Else Lives In My Apartment (Part 2/2)
alt_titles: The Building Office Wanted Our Unit Numbers. We Don't Have One. | If Someone You Know Asks Your Unit, It Isn't Them | 7C Was In Our Building Chat Twice
format: 9:16
template: pipeline/templates/horror.md (T1 Locked-Door Siege + rules-note modifier); PLAYBOOK §1D engines "Locked-door siege" x "Two rival authorities" x "Rules note"
target_runtime_s: {p1: 78.8, p2: 82.7}
target_words: {p1: 274, p2: 287}
wpm_spoken_measured: {p1: 247, p2: 244}   # PLAYBOOK §7 narrated band 230-270
wpm_overall_measured: {p1: 209, p2: 208}
timing_source: Kokoro-82M af_heart on the Spark CPU (tts_durations.json); every time below is measured, and build.py regenerates this file, both storyboards and the pacing numbers from it
voice: af_heart (June narrates every chat line and the voice at the door)
speed: 1.3 (pilot speed); 1.0-1.2 on the knock and whisper lines, with vox -3 to -6 dB in place of a whisper (Kokoro has none)
music: dread, out before the knocks in both parts
cast: June (narrator, 7C, moved in recently); Odette (3B, downstairs neighbor); Dale (8A, the joker); Mrs. Kowal (7A); Priya (7B), Sam (7D), Tess (7E); D. Rowe (the last tenant of 7C, wrote the note); the "Building Office" chat account
building: Harrow Court. Floor 7 = 7A, 7B, 7C (June, end of the corridor), 7D, 7E, plus the stairwell door and a trash room. The super lives in 1A; there is no building office.
mechanic: "Typing it marks you. Saying it opens." Giving your unit number in the chat puts out the light over your door; saying it aloud from inside lets the thing in. Only the resident of a unit can give it.
references:
  - id: 7659677578365537569
    url: https://www.tiktok.com/@udhwkz/video/7659677578365537569
    views: 376200
    outlier_score: 10.79
    short: SIEGE-CHAT
    why: Closest engine. A residents' chat run by a fake authority, `[Name] from [unit]` read-outs, instant compliant replies as a tell, leaked private data, the hero's unit as the target label, dead neighbours' accounts pressuring the hero, a lifeline under a clock and a cut on a new imperative. We borrow the chat engine, the casualty-proof-plus-peer-pressure rung and the clock lifeline. No killer, no fake cop, no muting, no burner phone, no box.
  - id: cVUJmsVkUW4
    url: https://www.youtube.com/watch?v=cVUJmsVkUW4
    views: 290919
    outlier_score: 30.95
    short: MOM-NOTE
    why: The rules-note format. An absent guardian's written list is the rulebook; numbered imperatives, one if/then branch with a strange condition, a rule that the plot later contradicts, and a forbidden or withheld piece of the document as the series hook. Our note is the last tenant's, taped under the sink; its torn-off end is the twist. We do not reuse its doll, closet, colour rules or parent voice.
  - id: 7670495663624408352
    url: https://www.tiktok.com/@mraevq/video/7670495663624408352
    views: 193600
    outlier_score: 18.01
    short: DORM-RULES
    why: Two rival authorities. One authority's rule (the office: reply with your unit) and another's (the note: never give it) cannot both be safe; the midpoint jolt is an authority quoting words it should not know; the turn is a repeated unit number that turns out to be "our" room. We borrow the rival-authority spine, the "how did it know what I was told" midpoint and the number-callback turn.
secondary_devices:
  - 7702661471641128224 (HEARSE-P2, 343K, 9.9x) sequel mechanics for Part 2: cold open, a Part 1 plant paid early, an outside check that falsifies a companion. We fix its known weakness (hard hook only at 0:20) with a frame-0 knock and the forbidden question at ~3 s.
  - T42u5xhrq-0 (TEXT-FIGURE, 869K, 25.5x) typography voice swap: a lowercase account answers in calm sentence case (P1 Mrs. Kowal).
  - 7702661541224566049 (HEARSE-P1, 2.2M, 63.1x) one held horror image late; the last shot bookends the first.
  - 7654526047005723937 (SIEGE-OVERLAY, 717K, 66.7x) the contradiction inside the first 7 s.
  - 7694996216505060641 (FLOOR-PHRASE, 613K, 17.6x) reactor-closeness ladder (neighbour, neighbour, super, mother) for the borrowed voices.
  - Qz-TrB6W2SM (HOTEL-DOOR, 1.52M, 9.0x) retro-reveal after safety: relief at sunrise, then worse than we knew.
demand_evidence: WrONG Rules "New Household Rules (Pt3?)" BciSW_2VMZg 104K (11.0x); Mr. Creeps "The Apartment Complex I Live In Has Scary Rules The Tenants Must Follow" 33J0uRRRu_8 873K; Lighthouse Horror "The Apartment Building I live in has 5 SCARY Rules" bwLuZt6qvC8 340K; Textify "Don't Answer Your Mom's Voice" 2k3w_XHRd1s 2.74M (borrowed-voice demand)
distinct_from: |
  episodes/horror-pinned-rules (pilot): this rewrite drops every beat it shared with the pilot. No "Management" pinning 7 rules, no "knocks three times, you are not home" rule, no dissolved company, no "Management will never..." rule, no back-against-the-door line, no one-person peephole sting. Here the authority asks for unit numbers in the hook and a paper note from the last tenant forbids it (two rival authorities, not one fake one); the debunk is "we don't have a building office"; the cost is countable (lamps out in reply order); the hidden space is a locked spare room, not a closet.
  episodes/horror-member-41 (extra chat member) and episodes/horror-building-intercom-buzzes-3-m (voice at the intercom): no extra member count, no intercom, no cat-name test.
  backlog/horror/horror-babysitter-parent-rules (fridge note, 5 rules, password): our note has 4 readable rules and a torn-off end; no password, no call.
  The gate below was also run against episodes/ and backlog/ (originality lens, must-fix 1).
---

# Never Give Anyone Your Unit Number (2 parts)

**Premise.** At 5:12 a.m. the "Building Office" asks the Harrow Court residents' chat to reply with their unit numbers. June has a note from the last tenant of 7C, taped under her sink: rule one says never give anyone your unit number, not even the building. Odette, downstairs, says the building has no office. Dale goes to look for it by the stairs, which rule two forbids, and the office tells him the stairs are fine. Then it says the note under the sink is out of date, and nobody else has a note. Four neighbours on floor seven reply anyway; each reply puts out the light over that door, and the knocking walks one door closer each time. Their accounts start posting in tidy sentence case, asking June to reply. Then a private message: every unit has replied except one. Behind her, under the locked spare room door, a light comes on. Three knocks.

Part 2: the voice at her door is Odette's, asking which unit this is. Rule four says someone you know who asks is not them, and the real Odette texts from her bathtub on floor three: typing it marks you, saying it opens. Dale's voice, then his stair photos: floor six, three times. The member list shows 7C twice: June, and D. Rowe, the name on the note, online. Something crouches against the door, listening. Sunrise is nine minutes away. The voices climb from neighbours to her mother, then just her unit, as a question. D. Rowe answers her DM instantly: don't answer it, not even to me. At 6:04 the knocking stops, Mrs. Kowal's light comes back, the other three stay dark, and the torn-off end of the note slides out under the spare room door: I never left 7C. Whatever knocks, it isn't me. Then three knocks from inside the spare room.

**Mechanic (one line the viewer can track).** Typing it marks you. Saying it opens. Only the resident of a unit can give its number: the thing has to make June say "7C" herself, so it borrows voices she trusts.

**Two authorities, told apart.** The note (D. Rowe, the last tenant, the protector) and the "Building Office" chat account (the thing). Every message that asks for a unit, threatens Dale's lease or pushes him to the stairs is the Building Office. The note's rules keep June alive until sunrise. The final knocks are the open question the line "Whatever knocks, it isn't me" sets up: either he is lying, or something else is in the spare room with him.

**Plants and payoffs.**

- Rule one, never give your unit (P1 0:06.6), is the whole story; the office breaks it in the hook and June keeps it to the end (P2 1:01.6).
- Rule two, no stairs (P1 0:13.5), plus Dale's on-screen "taking the stairs" (P1 0:21.4) and the office's "the stairs are fine" (P1 0:25.9); paid by Dale's floor-six photos (P2 0:21.3).
- Rule three, if your hall light goes out stay inside until sunrise (P1 0:14.9); the lights go out in reply order (P1 0:45.3-0:50.7); the one that comes back at sunrise is Mrs. Kowal's (P2 1:05.7).
- Rule four, someone you know who asks isn't them (P1 0:17.9); paid by Odette's voice asking "Which unit is this?" (P2 0:02.5).
- The torn-off end (P1 0:20.2); paid as the twist at sunrise (P2 1:09.6).
- The note's header "For whoever lives in 7C next. - D. Rowe" (on screen, P1 0:03.9); paid by 7C twice in the member list (P2 0:32.6).
- Four amber lamps (P1 0:31.8); paid as the cost ladder, four replies, four lights out (P1 0:50.7), and the dark doors through the peephole (P2 0:08.8).
- The spare-room light (P1 1:08.3); paid by the slip under that door and the knocks from inside (P2 1:09.6, 1:16.7).

**Loops open at the P1 cut (5):** who runs the Building Office; what the torn-off end says; what happened to the four dark units (7A's door is open); who is in the locked spare room; what knocks at June's door. **Open at the P2 cut (3, by design for a 2-part story):** who or what knocks inside the spare room; whether D. Rowe is the protector or a liar; 7B, 7D and 7E still dark (Mrs. Kowal's light came back). Closed in P2: who wrote the note, what the torn rule says, is the voice Odette, did Dale get down, does June survive the night.

## Beat alignment

| # | Our beat | Our time | Reference id + timestamp | Device borrowed | How we adapt it |
|---|---|---|---|---|---|
| P1-1 | B1 hook: an official channel asks for the one thing a rule forbids | P1 0:00.1-0:09.6 | 7654526047005723937 0:00-0:07 (official chat line, then a contradicting source by 7 s); 7659677578365537569 0:06-0:08 (group-chat authority line that will be undercut) | Place everyone lives + an official instruction + a contradicting source, all in the first 10 s; threat visible in frame 0 | The instruction is on the phone in frame 0 with a feet shadow under the blurred door; the contradiction is a paper note, not an overlay |
| P1-2 | B4 second channel: the authority does not exist | P1 0:09.8-0:13.2 | 7659677578365537569 0:55-0:59 (counter-voices: real neighbours doubt the authority) | A neighbour in the same chat undercuts the official account | One line from Odette plus a 3-word viewer-proxy question |
| P1-3 | B2 rules note, read fast | P1 0:13.5-0:21.1 | cVUJmsVkUW4 0:10-0:46 (ordinal imperatives on cards), 0:35 (first if/then branch), 2:01-2:04 (a withheld next part of the document as the series hook) | Numbered rules, one if/then with a strange condition, one part withheld | Rules 2-4 in under 7 s as paper close-ups; rule 4 is the if/then; the bottom is torn off |
| P1-4 | Minor rule broken in public | P1 0:21.4 | 7702661541224566049 0:16-0:17 (the companion proposes breaking the rule), 0:31 (a minor rule broken before the major one) | The joker says he will break a rule on screen | Dale announces the stairs, so rule two pays honestly in Part 2 |
| P1-5 | Authority knows too much, and contradicts a rule | P1 0:24.2-0:31.6 | 7659677578365537569 1:43-1:49 (top authority tags the hero, leaked private data); cVUJmsVkUW4 1:13 (a later line contradicts an earlier rule) | Leaked data as a rung; a contradiction the viewer can catch | Lease date from an office that doesn't exist, and "the stairs are fine" against rule two |
| P1-6 | Countable plant | P1 0:31.8 | 7702661541224566049 0:47 (hyper-specific plant: a plate number) | Plant a count that pays as a cost later | Four amber lamps on four doors; the far pair is EXIT and TRASH so the count reads |
| P1-7 | B8 midpoint: the authority quotes what it should not know | P1 0:35.0-0:42.1 | 7670495663624408352 1:34 (the rival knows the supervisor's private words); T42u5xhrq-0 0:31-0:33 (the threat crosses into "my" space at ~50%) | Private knowledge as the turn, aimed at the hero | "The note under the sink is out of date"; nobody else has a note |
| P1-8 | B5 roll-call ladder + proximity ladder | P1 0:42.3-0:52.7 | 7659677578365537569 0:39-0:52 (instant replies with unit labels); T42u5xhrq-0 0:44-0:47 (distance shrinks rung by rung) | Replies as a tell; a second ladder that moves the threat closer | Each reply = one lamp out, on the spoken unit; the knocking moves one door closer per reply |
| P1-9 | B6 voice swap + casualty proof + peer pressure | P1 0:53.6-0:59.4 | T42u5xhrq-0 0:51 then 0:56 (lowercase panic, then calm third-person register from the victim's account); 7659677578365537569 1:35-1:51 (@-tags and shill pressure), 1:54-1:58 (dead accounts used) | The trusted account speaks in the wrong register and pushes the hero | Mrs. Kowal (who typed "sorry i like rules") now writes in capitals and full stops: "June, please reply." 7B repeats it word for word |
| P1-10 | B9 peak image, held | P1 0:59.7-1:03.6 | 7702661541224566049 2:37-2:46 (one horror image, held) | One scariest image, held ~4 s at ~75% | 7A's door open a crack, black inside; every lamp dark |
| P1-11 | B11 target by elimination, then the inside threat | P1 1:03.6-1:10.9 | 7659677578365537569 1:20-1:33 (hero's unit named as the target); T42u5xhrq-0 0:31-0:33 (something in my room) | The unit as a target label; the threat on both sides of the barrier | "Every unit on seven has replied except one"; then the spare-room light behind her |
| P1-12 | B12 cliff on three knocks, bookend card | P1 1:11.2-end | 7659677578365537569 4:05-4:08 (cut at peak need, an imperative from the authority); 7702661541224566049 3:16-3:21.9 (bookend shot, part label) | Hard cut, no spoken CTA, part card | Cut on the third knock; the end card repeats frame 0's request ("Reply with your unit number.") with PART 2 |
| P2-1 | Cold open: trusted voice + forbidden question by 3 s | P2 0:00.1-0:03.8 | 7702661471641128224 0:00-0:20 (cold open, hard hook only at 0:20: the weakness we fix); BciSW_2VMZg (PLAYBOOK §5: the urgent-hook Pt3 got 11x, the mid-list Pt2 1.0x) | Continue mid-scene, but hook cold viewers in 3 s | Knock on frame 0, "my neighbor Odette", then "Which unit is this?" |
| P2-2 | Outside check falsifies the voice, mechanic stated | P2 0:04.0-0:08.6 | 7702661471641128224 1:36-1:47 (a short question to an outside party falsifies the companion's story); 7659677578365537569 3:41-3:42 (real authority gives the rule, contradicting the lie) | Outside check kills the impostor; the real source states the rule | A text to the real Odette, answered in 2 lines; the second is the 7-word mechanic |
| P2-3 | Premise restated for cold viewers | P2 0:08.8-0:16.1 | PLAYBOOK §5 (each part must stand alone); cVUJmsVkUW4 1:11-1:12 (a rule repeated as a callback) | Restate the rule the viewer needs | The four dark doors through the peephole + rule four on the note |
| P2-4 | Fast physical ladder, Part 1 plant paid | P2 0:16.3-0:26.6 | 7702661471641128224 0:20-0:45 (fast ladder), 1:29 (the Part 1 plate number pays) | Escalate at the barrier; pay a planted specific by ~45% | Dale's voice; his three floor-six photos; rule two |
| P2-5 | B7 lull + plant | P2 0:26.9-0:32.4 | 7702661541224566049 1:31-1:41 (lull, the companion's face hidden) | Short quiet stretch with one odd detail | The lit gap under the locked spare room |
| P2-6 | B8 turn: planted identifier pays | P2 0:32.6-0:39.2 | 7670495663624408352 2:16 (the dead girl's room number is "our" room) | A repeated number makes the threat personal | 7C twice in the member list; D. Rowe, online |
| P2-7 | B10 clock + reactor-closeness ladder + lifeline | P2 0:39.5-0:50.5 | 7659677578365537569 3:17-3:41 (countdown; the real party on a thin line gives the imperative); 7694996216505060641 0:27-2:41 (reactors grow closer: strangers to mother); Qz-TrB6W2SM 1:25-1:41 (door ladder: polite, silence, command) | Visible clock; voices climb from neighbour to family; a lifeline that answers | Sunrise as the clock; Kowal, the super, her mother; D. Rowe answers instantly: don't answer it |
| P2-8 | B9 peak image, held | P2 0:50.7-0:57.7 | 7702661541224566049 2:37-2:46 (one horror image, held); cVUJmsVkUW4 1:43-1:45 (peek through a gap, the strongest effect) | One image, held ~4 s, silence, at 60-80% | A head pressed ear-first to the door, low in the lens; 2 s with heartbeat only |
| P2-9 | Last rung, then false relief at sunrise | P2 0:57.7-1:09.3 | Qz-TrB6W2SM 1:25-1:41 (the volume ladder ends on the bare command); 7702661471641128224 1:02-1:07 (false calm, then doubt) | The demand stripped to one word; relief that is only partial | Just "7C?" twice; at 6:04 the knocking stops and only 7A's light returns |
| P2-10 | B11 truth twist after safety | P2 1:09.6-1:15.9 | Qz-TrB6W2SM 2:28-2:39 (retro-reveal after safety); 7659677578365537569 4:00-4:01 (identity reversal of the authority) | Relief, then worse than we knew; an authority reframed | The torn-off end slides out under the spare-room door at 6:04: the note's writer never left |
| P2-11 | B12 bookend cliff | P2 1:16.7-end | 7702661541224566049 3:16-3:21.9 (bookend shot); 7659677578365537569 4:05-4:08 (last-second message, no resolution) | Motif returns one step worse; hard cut | Three knocks, now from inside her own apartment; end card with D. Rowe's line |

## Script: Part 1

**Hook.** Line 1 (13 words): "At 5:12, the building office asked everyone to reply with their unit number." Frame 0 (also the cover): HandPhone full frame on the residents' chat, a red Building Office alert bubble "Night check. Please reply with your unit number so we know you're home." Behind the phone, the blurred front door with the hall light under it and **a feet shadow breaking the light** (the threat is literally in the cover). The note contradicts the office by 0:05.9 ("never"), Odette by 0:11.2.

Captions: pilot style (top band y 0.12, sentence case, a dark backing pill, up to 6 words a page, red on the emphasis words). Phone text appears word for word as it is read. Spoken numbers are spelled out for Kokoro (TTS column); the captions and the phone keep digits.


**[B1 HOOK: the authority asks, the note forbids]**

- `0:00.1-0:03.8` VO: At 5:12, the building office asked everyone to reply with their unit number. (TTS: "At five twelve, the building office asked everyone to reply with their unit number.")
- `0:03.9-0:06.5` VO: The last tenant's note, taped under my sink, said never do that.
- `0:06.6-0:09.6` VO: Rule one. Never give anyone your unit number. Not even the building.

**[B4 SECOND CHANNEL: there is no office]**

- `0:09.8-0:12.3` VO: My neighbor Odette, 3B: we don't have a building office. (TTS: "My neighbor Odette, three-B: we don't have a building office.")
- `0:12.5-0:13.2` VO: So who's asking?

**[B2 THE NOTE: three more rules, the bottom torn off]**

- `0:13.5-0:14.8` VO: Two. No stairs after midnight.
- `0:14.9-0:17.8` VO: Three. If your hall light goes out, stay inside until sunrise.
- `0:17.9-0:20.1` VO: Four. If someone you know asks your unit, it isn't them.
- `0:20.2-0:21.1` VO: The rest was torn off.

**[CHORUS + LEAK: the joker heads for the stairs]**

- `0:21.4-0:24.1` VO: Dale from 8A said he'd take the stairs and find this office. (TTS: "Dale from eight-A said he'd take the stairs and find this office.")
- `0:24.2-0:25.7` VO: The office answered in four seconds.
- `0:25.9-0:28.6` VO: Dale. Your lease renews in eleven days. The stairs are fine.
- `0:28.7-0:31.6` VO: An office we don't have knew his lease date. And wanted him on the stairs.

**[COUNTABLE PLANT: four lamps]**

- `0:31.8-0:34.8` VO: Through my peephole, four doors down the hall. Four little amber lights.

**[B8 MIDPOINT: it knows about the note]**

- `0:35.0-0:37.1` VO: At 5:25, the office posted again. (TTS: "At five twenty-five, the office posted again.")
- `0:37.2-0:39.3` VO: Reminder. The note under the sink is out of date.
- `0:39.4-0:40.8` VO: Nobody else had a note. It meant me.
- `0:41.0-0:42.1` VO: Odette: nobody answer it.

**[B5 ROLL-CALL LADDER: each reply costs a light, the knocking walks closer]**

- `0:42.3-0:45.2` VO: Mrs. Kowal answered anyway. 7A. Sorry. I like rules. (TTS: "Mrs. Kowal answered anyway. Seven-A. Sorry. I like rules.")
- `0:45.3-0:47.0` VO: In the hall, the light over her door went out.
- `0:47.3-0:49.3` VO: Then 7B. 7D. 7E. Like a roll call. (TTS: "Then seven-B. Seven-D. Seven-E. Like a roll call.")
- `0:49.5-0:50.7` VO: Four replies. Four lights out.
- `0:50.9-0:52.7` VO: Each time, the knocking moved one door closer.

**[B6 VOICE SWAP + CASUALTY PROOF: the dark units post calmly]**

- `0:53.6-0:56.6` VO: Then Mrs. Kowal posted again. Capital letters. Full stops.
- `0:56.8-0:58.1` VO: June, please reply. It's fine.
- `0:58.3-0:59.4` VO: 7B, word for word. (TTS: "Seven-B, word for word.")

**[B9 PEAK IMAGE (P1): the open door]**

- `0:59.7-1:02.2` VO: Mrs. Kowal's door stood open a crack. Dark inside.
- `1:02.3-1:03.6` silence (1.30 s): heartbeat_slow.

**[B11 TARGET BY ELIMINATION + THE INSIDE THREAT]**

- `1:03.6-1:05.8` VO: My phone buzzed. A private message from the office.
- `1:05.9-1:08.0` VO: Every unit on seven has replied except one.
- `1:08.3-1:10.9` VO: Behind me, under the locked spare room door, a light came on.

**[B12 CLIFF: three knocks, cut on the third]**

- `1:11.2-1:13.3` VO: I put my phone face down and held the chain.
- `1:13.4-1:14.1` silence (0.75 s): room tone. Music out.
- `1:14.1-1:14.6` silence (0.45 s): knock.
- `1:14.6-1:14.9` VO: One.
- `1:15.0-1:15.5` silence (0.45 s): knock.
- `1:15.5-1:15.9` VO: Two.
- `1:15.9-1:16.5` silence (0.62 s): knock. HARD CUT at the end.

```narration
[music: dread] [sfx: notify vol=-4] At five twelve, the building office asked everyone to reply with their unit number. The last tenant's note, taped under my sink, said never do that. [sfx: stinger @0.05 vol=-10] Rule one. Never give anyone your unit number. Not even the building.

[sfx: message_pop @0.2 vol=-2] My neighbor Odette, three-B: we don't have a building office. [sfx: glitch vol=-6] So who's asking?

[sfx: tick vol=-6] Two. No stairs after midnight. [sfx: tick vol=-6] Three. If your hall light goes out, stay inside until sunrise. [sfx: tick vol=-6] Four. If someone you know asks your unit, it isn't them. [sfx: click vol=-8] The rest was torn off.

[sfx: message_pop vol=-2] Dale from eight-A said he'd take the stairs and find this office. [sfx: typing vol=-8] The office answered in four seconds. [sfx: message_pop] [sfx: stinger @0.1 vol=-8] Dale. Your lease renews in eleven days. The stairs are fine. An office we don't have knew his lease date. And wanted him on the stairs.

Through my peephole, four doors down the hall. Four little amber lights.

[sfx: notify vol=-4] At five twenty-five, the office posted again. [sfx: message_pop vol=-2] Reminder. The note under the sink is out of date. Nobody else had a note. It meant me. [sfx: stinger vol=-6]

[sfx: message_pop vol=-2] Odette: nobody answer it. [sfx: message_pop @0.9 vol=-2] Mrs. Kowal answered anyway. Seven-A. Sorry. I like rules. In the hall, the light over her door went out. [sfx: click]

Then seven-B. Seven-D. Seven-E. Like a roll call. Four replies. Four lights out. Each time, the knocking moved one door closer. [sfx: knock3_slow vol=-10]

[sfx: message_pop vol=-2] Then Mrs. Kowal posted again. Capital letters. Full stops.

[vox: -2] June, please reply. It's fine.

[sfx: message_pop vol=-2] Seven-B, word for word.

[sfx: door_creak @0.2 vol=-10] Mrs. Kowal's door stood open a crack. Dark inside. [sfx: heartbeat_slow vol=-8] [pause: 1.30] [sfx: phone_buzz] My phone buzzed. A private message from the office. Every unit on seven has replied except one.

Behind me, under the locked spare room door, a light came on. [sfx: click vol=-6]

[speed: 1.15] [vox: -4] I put my phone face down and held the chain.

[music: stop] [pause: 0.75] [sfx: knock wait]

[speed: 1.0] [vox: -6] One.

[sfx: knock wait]

[vox: -6] Two.

[sfx: knock vol=2 wait] [cut]
```

## Script: Part 2

**Hook.** Line 1: "Three knocks. Then my neighbor Odette's voice through the door." Frame 0 (cover): the front door on the tail of the third knock, impact marks still settling, hall light on under it, a feet shadow. "Which unit is this?" lands at 0:02.5; the real Odette's "That's not me." at 0:05.2.


**[P2 COLD HOOK: a trusted voice asks the forbidden question]**

- `0:00.1-0:02.4` VO: Three knocks. Then my neighbor Odette's voice through the door.
- `0:02.5-0:03.8` VO: June? Which unit is this?
- `0:04.0-0:04.7` VO: I texted her.
- `0:05.2-0:06.8` VO: Bathtub. Floor 3. That's not me. (TTS: "Bathtub. Floor three. That's not me.")
- `0:06.9-0:08.6` VO: Typing it marks you. Saying it opens.

**[PREMISE FOR COLD VIEWERS: the mechanic and rule four]**

- `0:08.8-0:12.5` VO: Four neighbors gave the building office their unit tonight. All four hall lights went out.
- `0:12.7-0:16.1` VO: And the note under my sink says, if someone you know asks for your unit, it isn't them.

**[FAST LADDER + PART 1 PLANT PAID: Dale and the stairs]**

- `0:16.3-0:18.0` VO: Then the voice changed. Dale, from 8A. (TTS: "Then the voice changed. Dale, from eight-A.")
- `0:18.1-0:21.1` VO: June, it's Dale. The stairs don't go down anymore. Let me in.
- `0:21.3-0:24.8` VO: Dale had posted from the stairwell. Floor six. Floor six. Floor six.
- `0:25.0-0:26.6` VO: Rule two. No stairs after midnight.

**[B7 LULL + PLANT: the locked spare room]**

- `0:26.9-0:29.8` VO: Then the hall went quiet. Behind me, the spare room light was on.
- `0:29.9-0:32.4` VO: The agent said that room stays locked. Owner's storage.

**[B8 TURN: the planted unit number pays off]**

- `0:32.6-0:35.3` VO: I opened our chat's member list. 7C was in it twice. (TTS: "I opened our chat's member list. Seven-C was in it twice.")
- `0:35.5-0:37.5` VO: Me. And D. Rowe, the name on the note. Online. (TTS: "Me. And Dee Rowe, the name on the note. Online.")
- `0:37.7-0:39.2` VO: Someone else still lives in my apartment.

**[B10 CLOCK + LIFELINE: sunrise, the voices, the man in the spare room]**

- `0:39.5-0:43.1` VO: Sunrise was 6:04. My phone said 5:55. Nine minutes. (TTS: "Sunrise was six oh four. My phone said five fifty-five. Nine minutes.")
- `0:43.2-0:45.8` VO: It tried Mrs. Kowal's voice. The super's. My mother's.
- `0:46.0-0:47.9` VO: I messaged D. Rowe. Are you in my spare room? (TTS: "I messaged Dee Rowe. Are you in my spare room?")
- `0:48.1-0:50.5` VO: He answered instantly. Don't answer it. Not even to me.

**[B9 PEAK IMAGE, HELD (after the lifeline, ~63%)]**

- `0:50.7-0:52.7` VO: I looked through the peephole. Nobody at eye level.
- `0:52.9-0:55.6` VO: Lower down, something was crouched against my door. Ear to the wood.
- `0:55.7-0:57.7` silence (2.00 s): heartbeat_slow.

**[B10 CLOCK, LAST RUNG: just the unit, as a question]**

- `0:57.7-1:01.4` VO: At 6:01, the voices stopped. It just said my unit. 7C? 7C? (TTS: "At six oh one, the voices stopped. It just said my unit. Seven-C? Seven-C?")
- `1:01.6-1:02.8` VO: I bit my sleeve and said nothing.
- `1:03.0-1:05.6` VO: Three minutes. Then two. Then my phone said 6:04. (TTS: "Three minutes. Then two. Then my phone said six oh four.")
- `1:05.7-1:09.3` VO: The knocking stopped. Mrs. Kowal's light came back on. The other three stayed dark.

**[B11 TWIST: the torn-off end of the note, at sunrise]**

- `1:09.6-1:13.3` VO: Then a slip of paper slid out under the spare room door. The torn-off end of the note.
- `1:13.5-1:15.9` VO: I never left 7C. Whatever knocks, it isn't me. (TTS: "I never left Seven-C. Whatever knocks, it isn't me.")
- `1:16.0-1:16.7` silence (0.70 s): room tone. Music out.

**[B12 BOOKEND CLIFF: knocks from the inside]**

- `1:16.7-1:19.0` VO: Then, from inside the spare room. Three knocks.
- `1:19.1-1:20.4` silence (1.35 s): knock, knock, knock. HARD CUT at the end.

```narration
[music: dread] [sfx: knock] Three knocks. Then my neighbor Odette's voice through the door.

[speed: 1.15] June? Which unit is this?

[speed: 1.3] I texted her. [sfx: message_send vol=-2]

[sfx: message_pop] Bathtub. Floor three. That's not me. Typing it marks you. Saying it opens.

Four neighbors gave the building office their unit tonight. All four hall lights went out. And the note under my sink says, if someone you know asks for your unit, it isn't them.

[sfx: knock3 vol=-2] Then the voice changed. Dale, from eight-A.

[speed: 1.2] June, it's Dale. The stairs don't go down anymore. Let me in.

[speed: 1.3] [sfx: message_pop vol=-4] Dale had posted from the stairwell. Floor six. Floor six. Floor six. [sfx: tick vol=-6] Rule two. No stairs after midnight.

Then the hall went quiet. Behind me, the spare room light was on. The agent said that room stays locked. Owner's storage.

I opened our chat's member list. Seven-C was in it twice. Me. And Dee Rowe, the name on the note. Online. [sfx: stinger @0.05 vol=-6] Someone else still lives in my apartment.

[sfx: clock_ticking vol=-14] Sunrise was six oh four. My phone said five fifty-five. Nine minutes. [sfx: knock3 vol=-6] It tried Mrs. Kowal's voice. [sfx: knock3 vol=-4] The super's. [sfx: knock3 vol=-2] My mother's. I messaged Dee Rowe. Are you in my spare room? [sfx: message_send vol=-2] [sfx: message_pop] He answered instantly. Don't answer it. Not even to me.

I looked through the peephole. Nobody at eye level.

[vox: -3] Lower down, something was crouched against my door. Ear to the wood.

[sfx: heartbeat_slow vol=-6] [pause: 2.00] At six oh one, the voices stopped. It just said my unit. Seven-C? Seven-C?

[vox: -3] I bit my sleeve and said nothing.

[sfx: tick vol=-6] Three minutes. Then two. Then my phone said six oh four. The knocking stopped. Mrs. Kowal's light came back on. The other three stayed dark.

[sfx: whoosh @0.4 vol=-10] Then a slip of paper slid out under the spare room door. The torn-off end of the note.

[speed: 1.15] I never left Seven-C. Whatever knocks, it isn't me. [sfx: stinger vol=-4]

[music: stop] [pause: 0.70]

[vox: -3] Then, from inside the spare room. Three knocks.

[sfx: knock] [sfx: knock @0.45 vol=1] [sfx: knock @0.9 vol=3] [pause: 1.35] [cut]
```

## Shot list: Part 1

Generated from `build.py` (storyboard.json = Part 1, storyboard_p2.json = Part 2). In phone scenes the HandPhone fills the frame (cy 0.61, width 0.68), the set behind it is blurred 5 px and a Vignette sits on top. Shot starts sit 0.1 s before the word that names them. Every scene carries a slow push with keyframes so no hold exceeds 2.8 s without a visual event (check_storyboards rule); the two held peak images keep that push imperceptible.

| # | t_start | t_end | shot | visual (kit vocabulary) | camera | SFX in window |
|---|---|---|---|---|---|---|
| 1 | 0.00 | 3.80 | chat (jolt) | COVER. Residents chat, red Building Office alert 'Night check. Please reply with your unit number...'; blurred front door with a feet shadow under it [HandPhone chat over a blurred set] | zoom 1.00->1.05 | notify 0.1 |
| 2 | 3.80 | 6.50 | note (jolt) | The last tenant's note taped under the sink in the phone torch: header 'For whoever lives in 7C next. - D. Rowe', rules 1-4, torn bottom; rule 1 in red [inline SVG note (kit gap) under a torch pool] | zoom 1.00->1.03 | - |
| 3 | 6.50 | 9.72 | rule (jolt) | Close-up strip: '1. Never give anyone your unit number. Not even the building.' [note close-up strip (inline SVG)] | zoom 1.08->1.05 | stinger 6.7 |
| 4 | 9.72 | 12.40 | chat (jolt) | Odette 3B: 'We don't have a building office. The super lives in 1A.' Glitch on the line end [HandPhone chat over a blurred set] | zoom 1.00->1.03 | message_pop 10.0, glitch 12.3 |
| 5 | 12.40 | 13.36 | char (jolt) | June on the sofa, phone light, suspicious [Protagonist (June) over a set] | zoom 1.00->1.01 | - |
| 6 | 13.36 | 14.79 | rule (jolt) | Strip: '2. No stairs after midnight.' (stairwell ghosted behind) [note close-up strip (inline SVG)] | zoom 1.08->1.02 | tick 13.5 |
| 7 | 14.79 | 17.77 | rule (jolt) | Strip: '3. If your hall light goes out, stay inside until sunrise.' [note close-up strip (inline SVG)] | zoom 1.08->1.04 | tick 14.9 |
| 8 | 17.77 | 20.11 | rule (jolt) | Strip: '4. If someone you know asks your unit, it isn't them.' [note close-up strip (inline SVG)] | zoom 1.08->1.04 | tick 17.9 |
| 9 | 20.11 | 21.26 | rule (jolt) | Strip: the ragged torn bottom edge, the top of a '5. If' just visible [note close-up strip (inline SVG)] | zoom 1.08->1.02 | click 20.2 |
| 10 | 21.26 | 24.12 | chat (jolt) | Dale 8A: 'taking the stairs down to find this "office" lol', then 3 quick reactions (😂 / prank?? / who even is this) [HandPhone chat over a blurred set] | zoom 1.00->1.03 | message_pop 21.4 |
| 11 | 24.12 | 25.77 | chat | Header: 'Building Office is typing…' [HandPhone chat over a blurred set] | zoom 1.00->1.02 | typing 24.2 |
| 12 | 25.77 | 28.63 | chat (jolt) | Building Office: 'Dale. Your lease renews in 11 days. The stairs are fine.' [HandPhone chat over a blurred set] | zoom 1.00->1.03 | message_pop 25.9, stinger 26.0 |
| 13 | 28.63 | 31.73 | char (jolt) | June, worried, eyes toward the door [Protagonist (June) over a set] | zoom 1.00->1.04 | - |
| 14 | 31.73 | 34.93 | peep (jolt) | Peephole: corridor, four apartment doors (7A 7B 7D 7E) each with a lit amber lamp; far pair = EXIT stairwell + TRASH, no lamps [fake peephole: kit Hallway + inline lamp overlays + ring mask] | zoom 1.00->1.04 | - |
| 15 | 34.93 | 37.14 | lock (jolt) | Lock screen 5:25, banner 'Building Office · New message' [HandPhone lock screen] | zoom 1.00->1.03 | notify 35.0 |
| 16 | 37.14 | 39.34 | chat (jolt) | Building Office alert: 'Reminder: the note under the sink is out of date. Please reply.' [HandPhone chat over a blurred set] | zoom 1.00->1.03 | message_pop 37.2 |
| 17 | 39.34 | 40.92 | char (jolt) | June: scared, then shocked on 'me' (glitch) [Protagonist (June) over a set] | zoom 1.00->1.02 | stinger 40.8 |
| 18 | 40.92 | 42.19 | chat (jolt) | Odette 3B: 'Nobody answer it.' [HandPhone chat over a blurred set] | zoom 1.00->1.02 | message_pop 41.0 |
| 19 | 42.19 | 45.22 | chat (jolt) | Mrs. Kowal 7A: '7A. sorry i like rules' (lowercase) [HandPhone chat over a blurred set] | zoom 1.00->1.04 | message_pop 43.2 |
| 20 | 45.22 | 47.17 | peep (jolt) | Peephole: the lamp over 7A (nearest left) clicks out on 'out' [fake peephole: kit Hallway + inline lamp overlays + ring mask] | zoom 1.00->1.02 | click 47.0 |
| 21 | 47.17 | 50.78 | peep (jolt) | Peephole: lamps 7B, 7D, 7E die on each spoken unit; a reply chip pops for each [fake peephole: kit Hallway + inline lamp overlays + ring mask] | zoom 1.00->1.04 | - |
| 22 | 50.78 | 53.51 | hall_dark (jolt) | Dark hall, one flickering ceiling light; knocking (three at a time) from the far end [Hallway, lights 1, Darkness] | zoom 1.00->1.03 | knock3_slow 52.7 |
| 23 | 53.51 | 58.16 | chat (jolt) | Mrs. Kowal 7A, now in sentence case: 'June, please reply. It's fine.' [HandPhone chat over a blurred set] | zoom 1.00->1.06 | message_pop 53.6 |
| 24 | 58.16 | 59.56 | chat (jolt) | Priya 7B: 'June, please reply. It's fine.' word for word [HandPhone chat over a blurred set] | zoom 1.00->1.02 | message_pop 58.3 |
| 25 | 59.56 | 63.48 | peep (jolt) | P1 PEAK (held ~4 s, slow push into the lens): every lamp dark; 7A's door stands open a crack, black inside [fake peephole: kit Hallway + inline lamp overlays + ring mask] | zoom 1.00->1.63 | door_creak 59.9, heartbeat_slow 62.3 |
| 26 | 63.48 | 65.81 | lock (jolt) | Lock screen 5:38, private message banner, buzz [HandPhone lock screen] | zoom 1.00->1.03 | phone_buzz 63.6 |
| 27 | 65.81 | 68.24 | chat (jolt) | DM from Building Office: 'Every unit on floor 7 has replied except one.' [HandPhone chat over a blurred set] | zoom 1.00->1.03 | - |
| 28 | 68.24 | 71.08 | spare (jolt) | Behind her: the locked spare-room door; the gap under it lights up on 'light' [spare-room door (inline SVG, kit gap)] | zoom 1.00->1.03 | click 70.9 |
| 29 | 71.08 | 74.01 | door (jolt) | June on the floor at the front door, chain on, hands on the chain [FrontDoor] | zoom 1.00->1.04 | - |
| 30 | 74.01 | 74.95 | door (jolt) | Close door: knock 1, feet shadow, rattle [FrontDoor] | shake x1, zoom 1.00->1.01 | knock 74.1 |
| 31 | 74.95 | 75.76 | char (jolt) | June, hands over mouth [Protagonist (June) over a set] | zoom 1.00->1.01 | knock 75.0 |
| 32 | 75.76 | 76.48 | door (jolt) | Knock 3, handle jiggle; HARD CUT on the knock [FrontDoor] | shake x1, zoom 1.00->1.01 | knock 75.9 |
| 33 | 76.48 | 78.78 | end (jolt) | End card (bookend of frame 0): Building Office bubble 'REPLY.' + 'is typing…', stamp PART 2 [EndCard (bookend)] | zoom 1.00->1.03 | - |

## Shot list: Part 2

| # | t_start | t_end | shot | visual (kit vocabulary) | camera | SFX in window |
|---|---|---|---|---|---|---|
| 1 | 0.00 | 2.36 | door (jolt) | COVER. Front door, hall light on, a feet shadow, impact marks of the third knock still settling [FrontDoor] | shake x1, zoom 1.00->1.03 | knock 0.1 |
| 2 | 2.36 | 3.89 | door (jolt) | Closer on the door; the lever jiggles on 'Which unit' [FrontDoor] | zoom 1.00->1.02 | - |
| 3 | 3.89 | 5.08 | chat (jolt) | Texts to Odette (not the chat): 'Are you outside my door?' then typing dots 0.5 s [HandPhone chat over a blurred set] | zoom 1.00->1.01 | message_send 4.7 |
| 4 | 5.08 | 8.71 | chat (jolt) | Odette: 'Bathtub. Floor 3. That's not me.' then 'Typing it marks you. Saying it opens.' [HandPhone chat over a blurred set] | zoom 1.00->1.04 | message_pop 5.2 |
| 5 | 8.71 | 12.56 | peep (jolt) | Peephole: the four dark lamps (7A 7B 7D 7E) [fake peephole: kit Hallway + inline lamp overlays + ring mask] | zoom 1.00->1.05 | - |
| 6 | 12.56 | 16.23 | rule (jolt) | Strip: '4. If someone you know asks your unit, it isn't them.' [note close-up strip (inline SVG)] | zoom 1.08->1.05 | - |
| 7 | 16.23 | 18.04 | door (jolt) | Three knocks, the voice changes [FrontDoor] | shake x3, zoom 1.00->1.02 | knock3 16.3 |
| 8 | 18.04 | 21.21 | char (jolt) | June on the floor, staring at the door [Protagonist (June) over a set] | zoom 1.00->1.04 | - |
| 9 | 21.21 | 23.45 | stairs (jolt) | Dale's photo 1: stairwell landing '6' [Stairwell floor 6 inside a photo frame] | zoom 1.00->1.03 | message_pop 21.3 |
| 10 | 23.45 | 24.15 | stairs (jolt) | Photo 2: the same landing '6' [Stairwell floor 6 inside a photo frame] | zoom 1.00->1.01 | - |
| 11 | 24.15 | 24.91 | stairs (jolt) | Photo 3: the same landing '6' [Stairwell floor 6 inside a photo frame] | zoom 1.00->1.01 | - |
| 12 | 24.91 | 26.81 | rule (jolt) | Strip: '2. No stairs after midnight.' [note close-up strip (inline SVG)] | zoom 1.08->1.03 | tick 25.0 |
| 13 | 26.81 | 29.83 | spare (jolt) | The spare-room door behind her, light on underneath; slow push [spare-room door (inline SVG, kit gap)] | zoom 1.00->1.04 | - |
| 14 | 29.83 | 32.51 | spare | Closer on the keyed knob: locked, owner's storage [spare-room door (inline SVG, kit gap)] | zoom 1.00->1.35 | - |
| 15 | 32.51 | 37.60 | members (jolt) | Chat member list: two rows read 7C, both ringed red: 'June (you)' and 'D. Rowe · online' [member list (inline SVG panel)] | zoom 1.00->1.06 | - |
| 16 | 37.60 | 39.41 | char (jolt) | June, shocked [Protagonist (June) over a set] | zoom 1.00->1.02 | stinger 37.7 |
| 17 | 39.41 | 43.11 | lock (jolt) | Lock screen 5:55, no notifications [HandPhone lock screen] | zoom 1.00->1.04 | clock_ticking 39.5 |
| 18 | 43.11 | 45.90 | door (jolt) | Three bursts of three knocks: Kowal's voice, the super's, my mother's [FrontDoor] | shake x9, zoom 1.00->1.03 | knock3 43.2, knock3 44.7, knock3 45.2 |
| 19 | 45.90 | 47.95 | chat (jolt) | DM to D. Rowe: 'Are you in my spare room?' [HandPhone chat over a blurred set] | zoom 1.00->1.02 | message_send 47.9 |
| 20 | 47.95 | 50.59 | chat (jolt) | D. Rowe, instantly: 'Don't answer it. Not even to me.' [HandPhone chat over a blurred set] | zoom 1.00->1.03 | message_pop 48.1 |
| 21 | 50.59 | 52.81 | peep (jolt) | Peephole: the dark hall, nobody standing [fake peephole: kit Hallway + inline lamp overlays + ring mask] | zoom 1.00->1.03 | - |
| 22 | 52.81 | 57.64 | peep (jolt) | P2 PEAK (held ~4.8 s): low in the lens, a head pressed ear-first to the door; heartbeat, no VO for 2 s [fake peephole: kit Hallway + inline lamp overlays + ring mask] | zoom 1.00->1.06 | heartbeat_slow 55.7 |
| 23 | 57.64 | 61.51 | door (jolt) | Front door, handle still, feet shadow; captions '7C? 7C?' [FrontDoor] | zoom 1.00->1.05 | - |
| 24 | 61.51 | 62.95 | char (jolt) | June biting her sleeve, hands over mouth [Protagonist (June) over a set] | zoom 1.00->1.02 | - |
| 25 | 62.95 | 63.64 | lock (jolt) | Lock 6:01 [HandPhone lock screen] | zoom 1.00->1.01 | tick 63.0 |
| 26 | 63.64 | 64.87 | lock | Lock 6:02 [HandPhone lock screen] | zoom 1.00->1.01 | - |
| 27 | 64.87 | 65.65 | lock (jolt) | Lock 6:04 [HandPhone lock screen] | zoom 1.00->1.01 | - |
| 28 | 65.65 | 66.57 | door (jolt) | Front door: warm light under it, the shadow gone [FrontDoor] | zoom 1.00->1.01 | - |
| 29 | 66.57 | 69.47 | peep (jolt) | Peephole: 7A's lamp back on (door still ajar), 7B 7D 7E dark [fake peephole: kit Hallway + inline lamp overlays + ring mask] | zoom 1.00->1.43 | - |
| 30 | 69.47 | 73.35 | spare (jolt) | Spare-room door: a slip of paper slides out from the lit gap on 'slid' [spare-room door (inline SVG, kit gap)] | zoom 1.00->1.05 | whoosh 70.0 |
| 31 | 73.35 | 75.89 | slip (jolt) | The slip: 'I never left 7C.' / 'Whatever knocks, it isn't me.' typed on; RedText 'IT ISN'T ME' (the episode's one red scrawl) [slip close-up (inline SVG + text typewriter) + RedText] | zoom 1.08->1.04 | - |
| 32 | 75.89 | 76.59 | black | Black, 0.7 s silence [black] | zoom 1.00->1.01 | stinger 75.9 |
| 33 | 76.59 | 80.43 | spare (jolt) | Spare-room door from her side: three knocks from inside, the gap goes dark on the third; HARD CUT [spare-room door (inline SVG, kit gap)] | shake x3, zoom 1.00->1.05 | knock 79.1, knock 79.5, knock 80.0 |
| 34 | 80.43 | 82.73 | end (jolt) | End card (bookend of the cold open's question): Building Office bubble '7C?' + 'is typing…', stamp 2/2 [EndCard (bookend)] | zoom 1.00->1.03 | - |

## Kit notes (the horror kit is locked until the closeout lane passes QA)

Everything in both storyboards (storyboard.json, storyboard_p2.json) uses registered kit components or core layers. Three critique-flagged gaps are handled in the storyboard itself (inline SVG, tier S), so nothing waits on a kit edit:

- **Door lamps that go out in reply order.** The kit Peephole hardcodes its hall (`HallArt lights={2}`), so the peephole shots are a fake peephole: kit `horror/Hallway` at scale 1.28, inline SVG lamps drawn on the kit's own door geometry (copied from `HallArt`) at the same scale, a ring mask on top. The kit hall has three pairs of side doors; the near pair falls outside the lens ring, so the four visible doors are 7A/7D (middle pair) and 7B/7E (far pair), and the end door carries a green EXIT sign (the stairwell). Four lamps = four apartment doors on screen. Each lamp is an on layer and an off layer swapped at the measured word. After the lock lifts, the clean version is `doorLamps [{door, side, offAt, onAt}]` on HallArt, passed through Peephole.
- **The note, rule strips and the slip.** Paper SVG with Montserrat ink (no hand-lettered font is installed). The slip's two lines use the core text layer's `typewriter`.
- **The spare-room door.** An interior-door SVG (no peephole, chain or deadbolt) with a light gap that switches at the measured word, and core camera shakes on the knocks. After the lock lifts: a `variant: 'interior'` on FrontDoor with `glowColor`, so the knocks also get its rattle and impact marks.
- **No image bubbles.** The registry screenshot and filing card are gone with the rewrite. Dale's photos are three hard 1.1-1.5 s full-frame Stairwell (floor 6) shots inside a white photo border with a timestamp.
- **Clocks.** `lock.time` and `chat.clock` are fixed strings, so the 6:01 / 6:02 / 6:04 lock screens are three scenes cut on the words "Three", "two." and "6:04"; chat scenes carry their own clock (5:12 ... 5:38, 5:45, 5:57).
- **End cards.** Kit `horror/EndCard` (bubble + stamp), repeating each part's frame-0 sender. pipeline/templates/horror.md row 7 says "no part 2 card, exactly one open question"; that row is for standalones. This is a 2-part series, so it follows PLAYBOOK §5 (part label, 3-6 loops open at the P1 cut). Flagged for the template owner, not changed here.
- **Voice track.** `build.py --voice` (Spark) lays the measured line wavs on this timeline into `studio/public/episodes/horror-new-building-rules/p{1,2}_voice.wav`; music and SFX are storyboard audio tracks (dread bed out before the knocks, every SFX cue on a measured word). For the house mix with ducking and loudness, feed `narration_p1.md` / `narration_p2.md` to pipeline/audio instead (it reads one narration block per file).

## Pacing check (measured)

**Part 1**

- 274 words; 66.5 s of speech -> 247 wpm spoken (PLAYBOOK narrated band 230-270); 209 wpm over the full 78.8 s including timed silences and the 2.3 s end card. Kokoro af_heart speed 1.3 (1.0-1.2 on the knock lines), measured on the Spark CPU, not estimated.
- Runtime 78.8 s (cut at 76.5 s): above the 61 s Creator Rewards floor and inside the PLAYBOOK Shorts band (50-100 s).
- Hook: line 1 is 13 words / 3.6 s with the threat in frame 0 (Building Office alert + feet shadow under the door). The trusted source is contradicted by the note at 5.9 s ('never') and again by Odette at 11.2 s (PLAYBOOK cap 11 s).
- Words in the first 10 s: 39 (PLAYBOOK median 43.5).
- Rules list: 13.5-21.1 s = 7.7 s (10% of runtime; target <= 10 s). Rule 1 is already stated in the hook.
- Midpoint turn ('It meant me.') at 39.4 s (50%). Peak image (7A ajar, held 3.9 s) at 59.7 s (76%). Target narrowed at 65.9 s (84%); the inside threat (spare-room light) at 68.3 s; hard cut at 76.5 s (97%).
- Jolts (shot changes that carry a new anomaly, rule, number or notification): 32; median gap 2.7 s, longest 4.6 s (Shorts target 2.5-3.5 s, never > 8 s). 33 shots.
- Numbers per minute: 6.9 (clock times and unit codes; above the 3-5 target, which the unit-number mechanic needs; spoken times are spelled out for Kokoro).

**Part 2**

- 287 words; 70.7 s of speech -> 244 wpm spoken (PLAYBOOK narrated band 230-270); 208 wpm over the full 82.7 s including timed silences and the 2.3 s end card. Kokoro af_heart speed 1.3 (1.0-1.2 on the knock lines), measured on the Spark CPU, not estimated.
- Runtime 82.7 s (cut at 80.4 s): above the 61 s Creator Rewards floor and inside the PLAYBOOK Shorts band (50-100 s).
- Cold hook: a knock on frame 0, Odette's voice by 1.3 s, the forbidden question 'Which unit is this?' at 2.5 s. Her own text falsifies the voice at 5.2 s ('Bathtub. Floor 3. That's not me.'). The mechanic is stated in 7 words by 8.6 s, and the premise for cold viewers (four units gave the number, four lights out; rule four) by 16.1 s.
- Words in the first 10 s: 37.
- Part 1 plant paid (Dale on the stairs, rule two) at 21.3 s (26%). Turn (7C twice in the member list) at 32.6 s (39%). Peak image held 4.8 s from 52.9 s (64%). Clock 39.5-65.6 s. Twist (the torn-off end slides out at sunrise) at 69.6 s (84%); cut at 80.4 s (97%).
- Jolts (shot changes that carry a new anomaly, rule, number or notification): 31; median gap 2.5 s, longest 5.7 s (Shorts target 2.5-3.5 s, never > 8 s). 34 shots.
- Numbers per minute: 7.3 (clock times and unit codes; above the 3-5 target, which the unit-number mechanic needs; spoken times are spelled out for Kokoro).

- Silences: P1 0.9 s after the knocking walks closer, 1.3 s on the open door, 0.75 s before the knocks, then the knock gaps; P2 2.0 s on the peak image and 0.7 s before the spare-room knocks.
- Combined runtime is about 2:50, inside the PLAYBOOK story sweet spot (165-250 s). If the posting plan allows, also cut a single combined version to A/B against the two-part post (retention lens, nice-to-have); build.py can emit it by concatenating the two timelines.

## Policy notes (R5)

- research/R5/report.md and research/R5/horror-pinned-rules-DISCLOSURE.md cover the platform rules (checked 2026-11-01). Each part is over 1 minute (TikTok Creator Rewards) and under 3 minutes (YouTube Shorts).
- Inauthentic / repetitive content: this rewrite removes every beat shared with the pilot (see `distinct_from`), and the originality gate is run against episodes/ and backlog/ as well as the corpus. Keep the two parts distinct from the pilot's thumbnail too (thumbnail.md).
- AI voice: set YouTube "AI use / altered content" = yes and TikTok "AI-generated content" on, and reuse the standard caption disclosure line from research/R5/horror-pinned-rules-DISCLOSURE.md.
- Fenwick & Rowe is gone; "Harrow Court" and "D. Rowe" are generic and no real property company is named. No dates are hard-coded on screen (the lock screen says "Sunday").
