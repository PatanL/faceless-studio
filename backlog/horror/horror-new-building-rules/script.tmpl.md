---
id: horror-new-building-rules
niche: horror
series: 2 parts. Post Part 2 first, then Part 1 a few seconds later so Part 1 sits on top of the grid (PLAYBOOK §5). Each part hooks cold viewers on its own.
title_p1: Never Give Anyone Your Unit Number (Part 1/2)
title_p2: Someone Else Lives In My Apartment (Part 2/2)
alt_titles: The Building Office Wanted Our Unit Numbers. We Don't Have One. | If Someone You Know Asks Your Unit, It Isn't Them | 7C Was In Our Building Chat Twice
format: 9:16
template: pipeline/templates/horror.md (T1 Locked-Door Siege + rules-note modifier); PLAYBOOK §1D engines "Locked-door siege" x "Two rival authorities" x "Rules note"
target_runtime_s: {p1: {R1}, p2: {R2}}
target_words: {p1: {W1}, p2: {W2}}
wpm_spoken_measured: {p1: {WPM1}, p2: {WPM2}}   # PLAYBOOK §7 narrated band 230-270
wpm_overall_measured: {p1: {WPMO1}, p2: {WPMO2}}
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

- Rule one, never give your unit (P1 {t:a03}), is the whole story; the office breaks it in the hook and June keeps it to the end (P2 {t:b24}).
- Rule two, no stairs (P1 {t:a06}), plus Dale's on-screen "taking the stairs" (P1 {t:a10}) and the office's "the stairs are fine" (P1 {t:a12}); paid by Dale's floor-six photos (P2 {t:b10}).
- Rule three, if your hall light goes out stay inside until sunrise (P1 {t:a07}); the lights go out in reply order (P1 {t:a20}-{e:a22}); the one that comes back at sunrise is Mrs. Kowal's (P2 {t:b26}).
- Rule four, someone you know who asks isn't them (P1 {t:a08}); paid by Odette's voice asking "Which unit is this?" (P2 {t:b02}).
- The torn-off end (P1 {t:a09}); paid as the twist at sunrise (P2 {t:b27}).
- The note's header "For whoever lives in 7C next. - D. Rowe" (on screen, P1 {t:a02}); paid by 7C twice in the member list (P2 {t:b14}).
- Four amber lamps (P1 {t:a14}); paid as the cost ladder, four replies, four lights out (P1 {e:a22}), and the dark doors through the peephole (P2 {t:b07}).
- The spare-room light (P1 {t:a30}); paid by the slip under that door and the knocks from inside (P2 {t:b27}, {t:b29}).

**Loops open at the P1 cut (5):** who runs the Building Office; what the torn-off end says; what happened to the four dark units (7A's door is open); who is in the locked spare room; what knocks at June's door. **Open at the P2 cut (3, by design for a 2-part story):** who or what knocks inside the spare room; whether D. Rowe is the protector or a liar; 7B, 7D and 7E still dark (Mrs. Kowal's light came back). Closed in P2: who wrote the note, what the torn rule says, is the voice Odette, did Dale get down, does June survive the night.

## Beat alignment

| # | Our beat | Our time | Reference id + timestamp | Device borrowed | How we adapt it |
|---|---|---|---|---|---|
| P1-1 | B1 hook: an official channel asks for the one thing a rule forbids | P1 {t:a01}-{e:a03} | 7654526047005723937 0:00-0:07 (official chat line, then a contradicting source by 7 s); 7659677578365537569 0:06-0:08 (group-chat authority line that will be undercut) | Place everyone lives + an official instruction + a contradicting source, all in the first 10 s; threat visible in frame 0 | The instruction is on the phone in frame 0 with a feet shadow under the blurred door; the contradiction is a paper note, not an overlay |
| P1-2 | B4 second channel: the authority does not exist | P1 {t:a04}-{e:a05} | 7659677578365537569 0:55-0:59 (counter-voices: real neighbours doubt the authority) | A neighbour in the same chat undercuts the official account | One line from Odette plus a 3-word viewer-proxy question |
| P1-3 | B2 rules note, read fast | P1 {t:a06}-{e:a09} | cVUJmsVkUW4 0:10-0:46 (ordinal imperatives on cards), 0:35 (first if/then branch), 2:01-2:04 (a withheld next part of the document as the series hook) | Numbered rules, one if/then with a strange condition, one part withheld | Rules 2-4 in under 7 s as paper close-ups; rule 4 is the if/then; the bottom is torn off |
| P1-4 | Minor rule broken in public | P1 {t:a10} | 7702661541224566049 0:16-0:17 (the companion proposes breaking the rule), 0:31 (a minor rule broken before the major one) | The joker says he will break a rule on screen | Dale announces the stairs, so rule two pays honestly in Part 2 |
| P1-5 | Authority knows too much, and contradicts a rule | P1 {t:a11}-{e:a13} | 7659677578365537569 1:43-1:49 (top authority tags the hero, leaked private data); cVUJmsVkUW4 1:13 (a later line contradicts an earlier rule) | Leaked data as a rung; a contradiction the viewer can catch | Lease date from an office that doesn't exist, and "the stairs are fine" against rule two |
| P1-6 | Countable plant | P1 {t:a14} | 7702661541224566049 0:47 (hyper-specific plant: a plate number) | Plant a count that pays as a cost later | Four amber lamps on four doors; the far pair is EXIT and TRASH so the count reads |
| P1-7 | B8 midpoint: the authority quotes what it should not know | P1 {t:a15}-{e:a18} | 7670495663624408352 1:34 (the rival knows the supervisor's private words); T42u5xhrq-0 0:31-0:33 (the threat crosses into "my" space at ~50%) | Private knowledge as the turn, aimed at the hero | "The note under the sink is out of date"; nobody else has a note |
| P1-8 | B5 roll-call ladder + proximity ladder | P1 {t:a19}-{e:a23} | 7659677578365537569 0:39-0:52 (instant replies with unit labels); T42u5xhrq-0 0:44-0:47 (distance shrinks rung by rung) | Replies as a tell; a second ladder that moves the threat closer | Each reply = one lamp out, on the spoken unit; the knocking moves one door closer per reply |
| P1-9 | B6 voice swap + casualty proof + peer pressure | P1 {t:a24}-{e:a26} | T42u5xhrq-0 0:51 then 0:56 (lowercase panic, then calm third-person register from the victim's account); 7659677578365537569 1:35-1:51 (@-tags and shill pressure), 1:54-1:58 (dead accounts used) | The trusted account speaks in the wrong register and pushes the hero | Mrs. Kowal (who typed "sorry i like rules") now writes in capitals and full stops: "June, please reply." 7B repeats it word for word |
| P1-10 | B9 peak image, held | P1 {t:a27}-{e:h1} | 7702661541224566049 2:37-2:46 (one horror image, held) | One scariest image, held ~4 s at ~75% | 7A's door open a crack, black inside; every lamp dark |
| P1-11 | B11 target by elimination, then the inside threat | P1 {t:a28}-{e:a30} | 7659677578365537569 1:20-1:33 (hero's unit named as the target); T42u5xhrq-0 0:31-0:33 (something in my room) | The unit as a target label; the threat on both sides of the barrier | "Every unit on seven has replied except one"; then the spare-room light behind her |
| P1-12 | B12 cliff on three knocks, bookend card | P1 {t:a31}-end | 7659677578365537569 4:05-4:08 (cut at peak need, an imperative from the authority); 7702661541224566049 3:16-3:21.9 (bookend shot, part label) | Hard cut, no spoken CTA, part card | Cut on the third knock; the end card repeats frame 0's request ("Reply with your unit number.") with PART 2 |
| P2-1 | Cold open: trusted voice + forbidden question by 3 s | P2 {t:b01}-{e:b02} | 7702661471641128224 0:00-0:20 (cold open, hard hook only at 0:20: the weakness we fix); BciSW_2VMZg (PLAYBOOK §5: the urgent-hook Pt3 got 11x, the mid-list Pt2 1.0x) | Continue mid-scene, but hook cold viewers in 3 s | Knock on frame 0, "my neighbor Odette", then "Which unit is this?" |
| P2-2 | Outside check falsifies the voice, mechanic stated | P2 {t:b04}-{e:b06} | 7702661471641128224 1:36-1:47 (a short question to an outside party falsifies the companion's story); 7659677578365537569 3:41-3:42 (real authority gives the rule, contradicting the lie) | Outside check kills the impostor; the real source states the rule | A text to the real Odette, answered in 2 lines; the second is the 7-word mechanic |
| P2-3 | Premise restated for cold viewers | P2 {t:b07}-{e:b03} | PLAYBOOK §5 (each part must stand alone); cVUJmsVkUW4 1:11-1:12 (a rule repeated as a callback) | Restate the rule the viewer needs | The four dark doors through the peephole + rule four on the note |
| P2-4 | Fast physical ladder, Part 1 plant paid | P2 {t:b08}-{e:b11} | 7702661471641128224 0:20-0:45 (fast ladder), 1:29 (the Part 1 plate number pays) | Escalate at the barrier; pay a planted specific by ~45% | Dale's voice; his three floor-six photos; rule two |
| P2-5 | B7 lull + plant | P2 {t:b12}-{e:b13} | 7702661541224566049 1:31-1:41 (lull, the companion's face hidden) | Short quiet stretch with one odd detail | The lit gap under the locked spare room |
| P2-6 | B8 turn: planted identifier pays | P2 {t:b14}-{e:b16} | 7670495663624408352 2:16 (the dead girl's room number is "our" room) | A repeated number makes the threat personal | 7C twice in the member list; D. Rowe, online |
| P2-7 | B10 clock + reactor-closeness ladder + lifeline | P2 {t:b19}-{e:b22} | 7659677578365537569 3:17-3:41 (countdown; the real party on a thin line gives the imperative); 7694996216505060641 0:27-2:41 (reactors grow closer: strangers to mother); Qz-TrB6W2SM 1:25-1:41 (door ladder: polite, silence, command) | Visible clock; voices climb from neighbour to family; a lifeline that answers | Sunrise as the clock; Kowal, the super, her mother; D. Rowe answers instantly: don't answer it |
| P2-8 | B9 peak image, held | P2 {t:b17}-{e:h2} | 7702661541224566049 2:37-2:46 (one horror image, held); cVUJmsVkUW4 1:43-1:45 (peek through a gap, the strongest effect) | One image, held ~4 s, silence, at 60-80% | A head pressed ear-first to the door, low in the lens; 2 s with heartbeat only |
| P2-9 | Last rung, then false relief at sunrise | P2 {t:b23}-{e:b26} | Qz-TrB6W2SM 1:25-1:41 (the volume ladder ends on the bare command); 7702661471641128224 1:02-1:07 (false calm, then doubt) | The demand stripped to one word; relief that is only partial | Just "7C?" twice; at 6:04 the knocking stops and only 7A's light returns |
| P2-10 | B11 truth twist after safety | P2 {t:b27}-{e:b28} | Qz-TrB6W2SM 2:28-2:39 (retro-reveal after safety); 7659677578365537569 4:00-4:01 (identity reversal of the authority) | Relief, then worse than we knew; an authority reframed | The torn-off end slides out under the spare-room door at 6:04: the note's writer never left |
| P2-11 | B12 bookend cliff | P2 {t:b29}-end | 7702661541224566049 3:16-3:21.9 (bookend shot); 7659677578365537569 4:05-4:08 (last-second message, no resolution) | Motif returns one step worse; hard cut | Three knocks, now from inside her own apartment; end card with D. Rowe's line |

## Script: Part 1

**Hook.** Line 1 (13 words): "At 5:12, the building office asked everyone to reply with their unit number." Frame 0 (also the cover): HandPhone full frame on the residents' chat, a red Building Office alert bubble "Night check. Please reply with your unit number so we know you're home." Behind the phone, the blurred front door with the hall light under it and **a feet shadow breaking the light** (the threat is literally in the cover). The note contradicts the office by {t:a02@9} ("never"), Odette by {t:a04@4}.

Captions: pilot style (top band y 0.12, sentence case, a dark backing pill, up to 6 words a page, red on the emphasis words). Phone text appears word for word as it is read. Spoken numbers are spelled out for Kokoro (TTS column); the captions and the phone keep digits.

<!--P1_SCRIPT-->

<!--P1_NARR-->

## Script: Part 2

**Hook.** Line 1: "Three knocks. Then my neighbor Odette's voice through the door." Frame 0 (cover): the front door on the tail of the third knock, impact marks still settling, hall light on under it, a feet shadow. "Which unit is this?" lands at {t:b02}; the real Odette's "That's not me." at {t:b05}.

<!--P2_SCRIPT-->

<!--P2_NARR-->

## Shot list: Part 1

Generated from `build.py` (storyboard.json = Part 1, storyboard_p2.json = Part 2). In phone scenes the HandPhone fills the frame (cy 0.61, width 0.68), the set behind it is blurred 5 px and a Vignette sits on top. Shot starts sit 0.1 s before the word that names them. Every scene carries a slow push with keyframes so no hold exceeds 2.8 s without a visual event (check_storyboards rule); the two held peak images keep that push imperceptible.

<!--P1_SHOTS-->

## Shot list: Part 2

<!--P2_SHOTS-->

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

<!--P1_PACING-->

**Part 2**

<!--P2_PACING-->

- Silences: P1 0.9 s after the knocking walks closer, 1.3 s on the open door, 0.75 s before the knocks, then the knock gaps; P2 2.0 s on the peak image and 0.7 s before the spare-room knocks.
- Combined runtime is about 2:50, inside the PLAYBOOK story sweet spot (165-250 s). If the posting plan allows, also cut a single combined version to A/B against the two-part post (retention lens, nice-to-have); build.py can emit it by concatenating the two timelines.

## Policy notes (R5)

- research/R5/report.md and research/R5/horror-pinned-rules-DISCLOSURE.md cover the platform rules (checked 2026-11-01). Each part is over 1 minute (TikTok Creator Rewards) and under 3 minutes (YouTube Shorts).
- Inauthentic / repetitive content: this rewrite removes every beat shared with the pilot (see `distinct_from`), and the originality gate is run against episodes/ and backlog/ as well as the corpus. Keep the two parts distinct from the pilot's thumbnail too (thumbnail.md).
- AI voice: set YouTube "AI use / altered content" = yes and TikTok "AI-generated content" on, and reuse the standard caption disclosure line from research/R5/horror-pinned-rules-DISCLOSURE.md.
- Fenwick & Rowe is gone; "Harrow Court" and "D. Rowe" are generic and no real property company is named. No dates are hard-coded on screen (the lock screen says "Sunday").
