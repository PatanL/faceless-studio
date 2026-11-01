---
id: horror-mom-two-chats
niche: horror
format: 9:16 (1080x1920), ONE narrated first-person story (single cut, no Part 2), horror kit phone-chat UI + core layers
parts: 1
title: "My Mom Texted Me Twice. Only One Said Don't Open The Door."
alt_titles: see titles.md (8 ranked options)
template: pipeline/templates/horror.md (T1 Locked-Door Siege, family-chat variant, crossed with the "two rival authorities" engine from PLAYBOOK §1D)
runtime_s: 193.3 (measured: Kokoro-82M per line on the Spark CPU, tts_durations.json; timeline.json from build.py)
words: 633 (Nora 466, family-chat Mom 45, private-chat Mom 43, Dad 48, real Mom 23, voice-swap line 8)
wpm: "236.9 speaking / 196.5 overall (PLAYBOOK §7 narrated target 230-270 speaking). The overall rate includes 18.6 s of PLANNED silence (silent bubbles, a 4.0 s ring beat, a 4.0 s peak hold) and 14.4 s of breaths between lines. All measured, nothing extrapolated."
format_decision: "Both the retention and the reference critiques flagged the old 2 x 105 s split: it sat between the chat-Short length and the story sweet spot (PLAYBOOK §1, 165-250 s), and PLAYBOOK §5 measures Part 2 at 16% of Part 1's views. This final version is one 193 s story, the length of the two closest references (7670495663624408352 at 175 s, 7659677578365537569 at 249 s). If a TikTok split is ever forced, the only clean cut is 1:28.5 (after the closet ring, Dad is typing); it is not built."
voices: "Kokoro, all cached on the Spark (lines.VOICES): Nora af_heart 1.30 (narrator); both 'Mom' chats af_nicole (group 1.15 warm, private 1.02 colder: same contact, same voice); Dad on the hotel landline am_michael 1.12; the real Mom in person af_sky 1.18; the last bubble of the private 'Mom' thread is read in Dad's landline voice (am_michael 1.00): the voice swap. Dad's family-chat bubbles land SILENT on screen, so the first time we hear Dad is the landline."
music: "dread bed in segments (storyboard audio.music): out for the closet ring silence beat (1:24.5-1:28.5), out from the battery death through the peak (2:23.6-2:37.4), tension_pulse back in for the rescue. Multiple segments are supported by core/audio.tsx; no mix change needed."
references:
  - id: "7659677578365537569"
    url: https://www.tiktok.com/@udhwkz/video/7659677578365537569
    title: Hallway-song killer, fake cop, owners' group chat (@udhwkz, SIEGE-CHAT)
    views: 376200
    outlier_score: 10.79
    why_chosen: "Same engine (a locked-door siege where the trusted chat is the weapon) and the same narrated-first-person + held-phone visual. Borrowed devices: danger in our home contradicted by 0:11 (0:00-0:11), the near-open at the barrier (0:16), a common-knowledge rule the viewer can count against (0:18), the too-fast reply tell (0:39 'replied almost instantly'), the threat sensing the hero through the door (1:11-1:15), the top authority who never speaks naming the hero (1:35-1:51), the threat to bypass the lock with keys (1:47-1:49), isolation where only the enemy's channel still works (2:03-2:11), the battery-clock lifeline (3:17-3:42) and the last-second notification with an imperative (4:05). Not reused: no killer, no fake cop, no stickers, no admin muting, no burner phone, no unit numbers."
  - id: "7670495663624408352"
    url: https://www.tiktok.com/@mraevq/video/7670495663624408352
    title: Dorm red curtains and the supervisor's rules (@mraevq, DORM-RULES)
    views: 193600
    outlier_score: 18.01
    why_chosen: "The two-rival-authorities engine: two voices with equal claim to trust give opposite orders, and the protective one turns out to serve the threat. Borrowed: the 'remember this' protective rule from an absent authority (0:08-0:14), a protective 'no matter what' order that would blind the hero (0:38-0:47), the counter-authority explaining why the protective order was the trap and stating its opposite (1:28-1:37, T3) and the ending in which the trusted ally's voice is made suspect (2:38-2:55). Not reused: no dorm, curtains, ash, ghost or life-force lore."
  - id: gzXY52lcAcI
    url: https://www.youtube.com/shorts/gzXY52lcAcI
    title: The Creepiest Farmer Text Chat Ever!! - PART 1 (Textify, FARM-FLASHFWD)
    views: 352848
    outlier_score: 10.38
    why_chosen: "Closest cast and chat grammar: a family group thread plus a 1:1 thread with a parent, with a hard switch between thread headers (0:13), and the 'family member pushes the risky choice, the kid objects, the parent overrules' rung (0:39-0:52, done here as 'Rule. Use your key.' answered by 'Forgot them this morning. Check the hook.'). Its farm, trucks and 'things' are not used."
device_citations:
  - "T42u5xhrq-0 (Textify TEXT-FIGURE, 868,500 views, 25.54x, https://www.youtube.com/shorts/T42u5xhrq-0): the ~1.1 s bubble rhythm used for Dad's silent bubbles; the CAPS typography rung (0:46-0:47); distance going to zero (0:47); the silence beat (0:53); one held image as proof (0:54); the victim's thread speaking calmly as the entity and turning on 'you' (0:56-0:58)."
  - "7702661471641128224 (@udhwkz HEARSE-P2, 343,100 views, 9.85x): the outside call that falsifies the companion (1:36-1:58), including the long pause before the answer (1:43) and the 2-word falsifier (1:45, pattern T5)."
  - "7666044652910316833 (@mraevq, 325,900 views, 30.32x, library transcript): 'I called him, and his ringtone came from [nearby]' (3:47, 56% of 6:43). Our B8 turn uses the same device at 43%: Nora calls Dad and his ringtone answers from the hall closet behind her. Wording and setting are ours."
  - "Qz-TrB6W2SM (Wansee HOTEL-DOOR, 1.52M, 9.01x): the retro-reveal after safety (2:28-2:34, T8) and the closing return to the opening place (2:40-2:48)."
demand_evidence: "Textify 'Don't Answer Your Mom's Voice' 2.74M and 'Do Not Answer Your Family's Voice' 2.46M (~140x a 17.5K median); The Rule Files 'FaceTime Mom' 66K (5.7x). See backlog/horror/TOPICS.md row 2 and backlog/horror/evidence/s2_do_not_trust_your_mom_horror_shorts.jsonl, mom_texted_me_horror_story.jsonl, family_group_chat_horror_story.jsonl."
files: "lines.py (single source of the spoken lines) -> tts_measure.py (Kokoro on the Spark) -> tts_durations.json -> build.py -> timeline.json + storyboard.json. sfx_synth.py made studio/public/sfx/{desk_bell_ring,key_scrape,siren,relay_click}.wav. titles.md, thumbnail.md, review.json."
originality: "python3 scripts/originality_check.py backlog/horror/horror-mom-two-chats/script.md research/corpus research/library/transcripts -> PASS (section 9)"
status: "final script; storyboard.json validates (zod, Spark) and is render-ready (check_storyboards: 0 missing components, 0 missing audio, only the planned 4.0 s peak hold). 80 Spark stills reviewed (out/stills/horror-mom-two-chats_v1a/_v1b/_v1c.jpg). Not done: a full MP4 render."
supersedes: "the 2-part backlog draft of this file and episodes/horror-mom-two-chats/script.md (S1 75 s draft). Premise kept; story, setting (now an apartment), logic, ending and production all rewritten."
---

# My Mom Texted Me Twice. Only One Said Don't Open The Door.

**Premise.** 11:40 p.m. Nora, 17, is home alone in apartment 6C. Mom's family-chat account texts *I'm outside. Unlock the door.* Nine seconds later the same contact, in their private thread, texts *Don't open it. I'm still at work.* Each Mom passes one test and fails another. Dad, in Columbus, never posts, but now he posts to vouch for the one outside. Nora calls him, and his ringtone goes off in the hall closet behind her.

**Truth (writers only, never stated).** Neither chat is Mom: her phone died at nine on her ICU shift. One thing speaks through every family phone it can reach, including Dad's cell, forgotten in his winter coat in the hall closet. It plays the warm Mom outside who wants in, and the strict Mom inside who keeps Nora locked in next to that closet and, when it counts, orders her *into* it. It is learning whose voice she obeys. It knows Marigold because it was in the kitchen when the word was picked. The hall motion light never sees it. At the end she trusted the landline, so that is the voice it will use next time.

**Master question.** Which Mom is real? It becomes "neither", then "what voice will it use next".

**Ownable rule (PLAYBOOK §8).** Mom's fridge note: *AFTER 10 THE DOOR STAYS LOCKED. EVEN FOR ME. I HAVE MY KEY.* Stated at 0:09; used as a weapon at 0:19 ("Rule. Use your key."); its loophole becomes the attack at 1:59-2:03 (a key from outside, the rule spoken back as the deadbolt turns); broken by Nora at 2:48 only after the planted light test passes.

**Second signature (fair-play tell).** The hall light outside is on a motion sensor: "It clicks on for anyone, even the neighbor's cat. It never clicked on." (0:56-1:01). Paid at 2:45: it clicks on for the police. No on-screen flicker anywhere (real PIR lights hold 30 s or more; originality critique).

### Plants and loops

| Plant / loop | Planted | Paid / status |
|---|---|---|
| Rule: door locked after ten, even for Mom, she has her own key | 0:09 (fridge note) | 0:19 used as a test; 1:59-2:03 a key turns the lock and the rule is spoken back; 2:48 Nora breaks it on purpose |
| Room 412, Lakeview Suites (second line of the fridge note, in Dad's hand) | 0:09 (on screen only) | 1:36 the landline lifeline; 3:09 the last line turns it into the threat |
| Keys on the hook, red lanyard (backs the group Mom: "check the hook") | 0:23 | 1:56 the hook is empty, "nobody had come in". Who took them stays **open** |
| Private Mom: "They're in my pocket" (clean catchable lie, no typing dots) | 0:31 | 2:54 Mom's phone died at nine: the private chat was never her |
| Group Mom: "phone's on three percent" (a second catchable lie) | 0:15 | 2:54 the same reveal: her phone was dead, not at 3% |
| No typing dots in the private thread (the tell) | 0:34 | 3:06 typing dots appear for the first time, on the final threat |
| Code word Marigold, "we never typed it anywhere" | 0:37-0:49 | 2:58 "We only ever said it out loud, in our kitchen" -> 3:02 it was inside our home |
| Hall motion light stays dark for her | 0:56-1:01 | 2:45 it clicks on for the officers: "It had never come on for her" |
| Dad "never posts", "never lied", in Columbus | 1:01-1:09 | 1:42 his cell is in his coat in our hall closet |
| Dad's old desk-phone ringtone | 1:19 | 1:24 the 4 s ring beat; the closet phone at 2:29 |
| Nora's battery (status bar from frame 0, 6% -> 2%) | 0:00 (on screen) | 1:50 "two percent" = the lifeline clock; 2:22 it dies; 3:04 the dead phone lights up anyway |
| "Now I know whose voice you trust" / Room 412 in Dad's voice | 3:07-3:11 | **Open**: the next call from the trusted line |

Early loops (which Mom lies about the keys, the code word, what the doorbell is) close before 50%. At the cut 3 stay open: the keys, the thing in the house, the next call from Room 412. That is the PLAYBOOK §4D standalone range (0-2, +1 re-opened by the final sting).

---

## 1. Beat alignment (our % vs the reference's %)

| Our beat | Our time (%) | Reference id + timestamp (%) | Device borrowed | How we adapt it |
|---|---|---|---|---|
| B1 Hook: two texts, same contact, opposite orders | 0:00-0:07 (0-4%) | 7659677578365537569 0:00-0:11 (0-4%): danger in our home, the official all-clear, contradicted at 0:11; gzXY52lcAcI 0:13 (22%): hard switch between thread headers | A trusted source contradicted inside 11 s; two thread modes | Line 1 is 7 words ("Mom texted: I'm outside. Unlock the door."). The contradiction ("Don't open it") lands at **4.3 s**; core hook 17 words / 6.8 s. Frame 0 shows both banners fully readable over the door with the feet in the red EXIT glow |
| B3 Intrusion at the barrier | 0:07 (4%) | 7659677578365537569 0:11 (4%): "someone knocked" | Threat at *my* door | "And one of them was right outside our door." Whip to the feet under the door |
| B2 Rule laid down (+2 plants on one prop) | 0:09-0:14 (5-7%) | 7670495663624408352 0:08-0:14 (5-8%): "remember this" protective rule | Ownable rule from an absent guardian | Fridge note with a hidden loophole ("I have my key") and Dad's hotel line (Rm 412) |
| B3 Pressure: objection overruled, near-open | 0:14-0:27 (7-14%) | gzXY52lcAcI 0:39-0:52 (66-88%): the parent pushes the risky choice, the kid objects, the parent overrules; 7659677578365537569 0:16 (6%): "about to unlock" | Overrule rung; the near-open | Nora objects with the rule itself ("Rule. Use your key."); the group Mom overrules by pointing at the hook, the hook checks out, and her hand goes to the deadbolt. Ours sits earlier than FARM's because the overrule is the B3 set-up, not the Short's climax |
| B4 Counter-voice + catchable lie | 0:27-0:37 (14-19%) | 7659677578365537569 0:39 (16%): "3 people replied almost instantly" | A reply too fast to be human is the tell | The private Mom sees her hand on the lock (re-hook question "How did she know?"), then lies in one second with no typing dots |
| S4 Test: the code word micro loop | 0:37-0:51 (19-27%) | T42u5xhrq-0 0:09-0:11 (15-18%): micro loop opened and closed; 7670495663624408352 0:38-0:47 (22-27%): a protective "no matter what" order | Test question; protective order | Group dodges, private answers the never-typed word and adds an order (chain on). The viewer tilts to the private chat |
| B5 Rung: doorbell, peephole, the light rule | 0:51-1:02 (27-32%) | 7659677578365537569 1:09-1:15 (28-30%): held breath at the peephole; 0:18 (7%): a common-knowledge rule broken ("cops work in pairs") | Peephole hold; a real-world rule the viewer can count against | Blue scrubs too close to the lens, no face; "It clicks on for anyone, even the neighbor's cat. It never clicked on." |
| B5 Top authority who never speaks | 1:02-1:10 (32-36%) | 7659677578365537569 1:35-1:51 (38-44%): the admin names the hero, "open the door now" | The highest-trust voice pushes compliance | Dad "never posts" posts 3 SILENT bubbles (T42 bubble rhythm); "never lied" raises the cost of doubt |
| S7 Proximity + typography ladder | 1:10-1:16 (36-40%) | T42u5xhrq-0 0:44-0:47 (73-78%): distance shrinks, caps; 7659677578365537569 1:11-1:15 (28-30%): the threat senses the hero, pounding | It can see her; the mask slips | "I can see your shadow under the door, Nora." -> lever tilts slowly -> silent CAPS bubble + knocks |
| B8 Turn: the voucher is in the house | 1:16-1:28 (40-46%) | 7666044652910316833 3:47 (56%): "his ringtone came from next door"; PLAYBOOK B8 (45-60%) "a personal link to the threat"; T42u5xhrq-0 0:53 (88%): silence beat | Ringtone gives away where the authority's phone really is | Ringtone behind her, in our hall closet (43%). The 4.0 s silence beat (two ring cycles, under-door glow pulsing, music out) meets the 3-8 s spec |
| B6 Isolation: only the enemy's channel answers | 1:28-1:33 (46-48%) | 7659677578365537569 2:03-2:11 (49-53%) | Only the enemy's channel works | "Dad is typing", then silent calm bubbles: "Don't turn around, kiddo." / "Just open the front door." |
| B10 Lifeline outside the compromised channels, battery clock | 1:33-1:53 (48-59%) | 7702661471641128224 1:36-1:58 (50-62%): the outside call falsifies the companion, long pause at 1:43; 7659677578365537569 3:17 (79%): one bar of battery | Outside check + a short lethal number | Hotel landline from the fridge note. Real Dad: his cell is in his coat in our closet, so who is typing? Police 8 min; her battery 2% |
| B5 Barrier ladder + the rule spoken back | 1:53-2:08 (59-67%) | 7659677578365537569 1:47-1:49 (43-44%): "they're bringing the keys"; Qz-TrB6W2SM barrier ladder ("it has a key", PLAYBOOK §4A) | Lock bypassed; last barrier left | Hook empty ("nobody had come in"), a key from outside, "Even for her, the door stays locked. She has her own key." (PLAYBOOK §1C: the rule returns at the climax as a spoken line), the deadbolt turns, the door slams to the chain |
| T3 Rule inversion | 2:08-2:24 (67-75%) | 7670495663624408352 1:28-1:37 (50-55%): the counter-authority explains the protective rule was the trap and states its opposite | The helper's safe place IS the threat | Private Mom: "Get in the hall closet. Shut the door. Don't make a sound." Real Dad: "That's where my phone is ... Lock yourself in the bathroom." She obeys him. Ours lands later than DORM's because our midpoint slot is the ringtone turn |
| B9 Peak contact, one held image | 2:24-2:37 (75-81%) | T42u5xhrq-0 0:54 (90%): the only image, held as proof; 0:56-0:58: the thread turns on "you"; PLAYBOOK B9 (60-80%, hold ~4 s) | One still image, held; threat addressed to the hero | The closet opens itself; the sleeve still swinging (physical wrongness); the phone in the pocket types a draft that addresses her, "turn around nora", held 4.0 s with no music |
| B10 Rescue decided by the planted rule | 2:37-2:54 (81-90%) | 7659677578365537569 0:28 (11%): the hero checks a planted detail (count match); Qz-TrB6W2SM 2:25 (86%): hard evidence closes the disbelief loop | The planted identifier decides who is real | "Voices lie. So I watched the light under the door." Red EXIT strip -> warm motion light, two pairs of feet. She breaks the rule: chain off |
| B11 Truth twist after safety (T8 + T5) | 2:54-3:04 (90-95%) | Qz-TrB6W2SM 2:28-2:34 (88-91%): relief, then worse than you knew; 7702661471641128224 1:45 (55%): a 2-word falsifier | New information at the twist, not a recap | Mom: "my phone died at nine. I never texted you." Then Marigold: "We only ever said it out loud, in our kitchen" -> it was in our home |
| B12 Voice swap, verifier made suspect, bookend | 3:04-3:13 (95-100%) | T42u5xhrq-0 0:56-0:58 (93-97%): voice swap; 7670495663624408352 2:38-2:55 (91-100%): the trusted ally's role is taken over; 7659677578365537569 4:05 (98%): last-second notification; Qz-TrB6W2SM 2:40-2:48: return to the opening place | Threat aimed at what the hero actually trusted | Her dead phone lights up; typing dots for the first time; "Now I know whose voice you trust." then, in Dad's landline voice, "Next time, I'll call from Room 412." Last frame = frame 0's composition. Hard cut, no CTA |

---

## 2. Script (measured timeline)

Times are measured (Kokoro per line + the breaths and silences in lines.py). Speakers: N Nora (narrator), M family-chat "Mom", P private-chat "Mom", D Dad (landline), R Mom in person, X the private thread in Dad's voice. "—" rows are timed silences (no VO; the picture keeps moving). Text is the spoken form; captions show digits ("412", "2%", "8").

| Start | Dur | Spk | Line | Beat | On screen |
|---|---|---|---|---|---|
| 0:00.1 | 0.68 | N | Mom texted: | B1 | FRAME 0 = COVER. Lock screen 11:40, two banners already stacked and fully readable: "Family · Mom: I'm outside. Unlock the door." over "Mom: Don't open it. I'm still at work." Behind the phone, sharp: our front door, the red EXIT-sign strip under it broken by two feet |
| 0:00.9 | 2.05 | M | I'm outside. Unlock the door. | B1 | Punch-in on banner 1 (Family · Mom) |
| 0:03.3 | 0.88 | N | Nine seconds later: | B1 | Punch-in on banner 2 (Mom, the private thread), timestamps 11:40 / 11:40 |
| 0:04.3 | 2.50 | P | Don't open it. I'm still at work. | B1 | Banner 2 held, red edge pulse |
| 0:07.1 | 1.67 | N | And one of them was right outside our door. | B1 | Whip to the front door from inside: hall side dark, only the red EXIT glow under the door, two feet breaking it |
| 0:08.9 | 4.74 | N | Mom's rule is on our fridge. After ten, the door stays locked. Even for her. She has her own key. | B2 | Yellow sticky note on the fridge: "AFTER 10 THE DOOR STAYS LOCKED. EVEN FOR ME. I HAVE MY KEY. —M"; smaller second line in Dad's hand: "Dad: Lakeview Suites, Rm 412 (back Sun)". "EVEN FOR ME" underlines itself in red |
| 0:14.0 | 4.20 | M | Hands full, honey. Phone's on three percent. Please. | B3 | Family thread (Mom, Dad, Nora). Mom: "hands full honey" / "phone's on 3%" / "please" |
| 0:18.5 | 1.50 | N | So I sent her the rule. Use your key. | B3 | Me (blue): "Rule. Use your key." |
| 0:20.3 | 2.71 | M | Forgot them this morning. Check the hook. | B3 | Mom: "forgot them this morning" / "check the hook" |
| 0:23.3 | 3.90 | N | Her keys were on the hook, on the red hospital lanyard. My hand went to the deadbolt. | B3 | Key hook by the door: Mom's key ring on a plain red lanyard. Then the deadbolt thumb-turn, close; Nora's hand reaching in (near-open) |
| 0:27.5 | 1.38 | P | Don't touch that lock. | B4 | Buzz. Private thread "Mom": "Don't touch that lock." arrives with NO typing dots |
| 0:29.2 | 2.08 | N | How did she know? I typed, your keys are right here. | B4 | Me: "ur keys are right here on the hook??" |
| 0:31.5 | 2.56 | P | No they're not. They're in my pocket. | B4 | Instant, no dots: "No they're not." / "They're in my pocket." |
| 0:34.4 | 2.92 | N | No typing dots. One second. And I was staring at her keys. | B4 | Punch-in on the empty space where typing dots should be; cut to the keys on the hook |
| 0:37.5 | 4.92 | N | So I asked both of them for our code word. Mom and I picked it at the kitchen table. We never typed it anywhere. | S4 | Me, in both threads: "what's our word?" (two whips). Nora close-up on "kitchen table" |
| 0:42.7 | 3.67 | M | Nora, I'm not doing this in the hallway. Open up. | S4 | Family · Mom: "Nora I'm not doing this in the hallway" / "open up" |
| 0:46.7 | 2.56 | P | Marigold. Now put the chain on. | S4 | Private · Mom: "Marigold." / "Now put the chain on." |
| 0:49.6 | 1.67 | N | Only Mom knew that. I slid the chain on. | S4 | Insert: the door chain sliding into its track |
| 0:51.4 | 0.91 | N | Then the doorbell rang. | B5a | Front door, shake on the bell |
| 0:52.4 | 3.84 | N | Through the peephole, blue scrubs. Head down. Too close to the lens to see a face. | B5a | Peephole POV: the corridor dark except the red EXIT sign; a blue-scrubs shoulder and a bowed head fill the bottom of the lens |
| 0:56.5 | 5.04 | N | Our hall light is on a motion sensor. It clicks on for anyone, even the neighbor's cat. It never clicked on. | B5a | Hold the dark peephole; cut on "never" to the strip under the door: still only red |
| 1:01.7 | 2.60 | N | Then Dad posted in the family chat. Dad never posts. | B5b | Family thread: Dad's avatar (D, slate) with typing dots; his last message above it, from Sep 14: "ok" |
| 1:04.4 | 2.60 | — | *[silence 2.6 s]* | B5b | SILENT bubbles (no VO), big punch-in: Dad: "It's really her, kiddo." / "I just talked to her." / "Let your mother in." |
| 1:07.0 | 2.70 | N | Dad was in Columbus till Sunday. And he has never lied to me. | B5b | Nora close-up, worried. Behind her, out of focus: the hall closet door |
| 1:10.0 | 2.72 | M | I can see your shadow under the door, Nora. | S7 | Family · Mom: "I can see your shadow under the door, Nora." Cut to floor level: Nora's shadow strip inside, the feet outside |
| 1:13.1 | 1.88 | N | The handle tilted down. Slowly. Then up. | S7 | Macro: the lever handle tilts down slowly, then back up |
| 1:15.0 | 1.50 | — | *[silence 1.5 s]* | S7 | SILENT CAPS bubble (red alert style), phone vibrates, door knocks: "NORA. OPEN. THE DOOR." |
| 1:16.5 | 1.66 | N | I didn't text Dad back. I called him. | B8 | Outgoing call screen: "Dad · mobile · calling…" with one red End button |
| 1:18.3 | 1.00 | — | *[silence 1.0 s]* | B8 | Ringback, faint, in the earpiece only |
| 1:19.3 | 5.12 | N | Two rings and a pause. Dad's old desk-phone ringtone. Not in my ear. Behind me. In our hall closet. | B8 | Nora's eyes go wide (no blink). On "Behind me": over-the-shoulder, past her back-view silhouette, to the hall closet door; phone glow pulses under it with each ring |
| 1:24.5 | 4.00 | — | *[silence 4.0 s]* | B8 | SILENCE BEAT 4.0 s: two more full ring cycles from the closet, no VO, music out. The glow pulses, then goes dark |
| 1:28.5 | 2.55 | N | The ringing stopped. And in the family chat, Dad was typing. | B6 | Family thread header: "Dad is typing…" |
| 1:31.2 | 2.00 | — | *[silence 2.0 s]* | B6 | SILENT calm bubbles: Dad: "Don't turn around, kiddo." / "Just open the front door." |
| 1:33.2 | 4.09 | N | I backed away from the closet and called the hotel number on the fridge. Room four twelve. | B10 | Walk-back: Nora toward camera, the closet behind her. Insert: the fridge note's "Rm 412" line. Outgoing call "Lakeview Suites · Room 412" |
| 1:37.6 | 1.72 | D | Hello? Nora? What's wrong, kiddo? | B10 | Call connects; timer starts 00:00 |
| 1:39.6 | 2.13 | N | His real voice. Half asleep. Where's your phone, Dad? | B10 | Nora close-up, phone to her ear, whispering |
| 1:42.0 | 3.32 | D | My cell? It's in my winter coat. In the hall closet. I forgot it. | B10 | Call screen; cut on "closet" to the closet door, dark |
| 1:45.6 | 0.94 | N | Then who's typing on it? | B10 | Nora close-up, scared |
| 1:46.7 | 0.80 | — | *[silence 0.8 s]* | B10 | Call timer runs; silence on the line |
| 1:47.5 | 3.19 | D | Stay on the line. I'm having the front desk call your police. | B10 | Call screen, timer running |
| 1:50.9 | 2.17 | N | Eight minutes, they said. My battery said two percent. | B10 | Battery glyph in the status bar flips red: 2%; chip "police · 8 min" |
| 1:53.4 | 1.62 | M | Who are you whispering to, honey? | B5c | Banner over the call: "Family · Mom: who are you whispering to, honey?" |
| 1:55.3 | 3.47 | N | I looked at the hook. Empty. Nobody had come in. I'd been standing right here. | B5c | Same framing as the key-hook insert: the hook is empty. Then Nora, looking around her own hallway |
| 1:59.0 | 1.72 | N | Then a key slid into our lock, from outside. | B5c | Macro on the lock cylinder, the key sound only |
| 2:00.9 | 2.54 | N | Even for her, the door stays locked. She has her own key. | B5c | Flash insert of the fridge note: "I HAVE MY KEY" turns red |
| 2:03.7 | 4.76 | N | The deadbolt turned. The door slammed open against the chain. Three inches of black. Nothing came in. | B5c | The thumb-turn rotates by itself; the door jerks open to the chain; the gap is pure black; cold air drifts in; nothing is ever visible in the gap |
| 2:08.7 | 4.58 | P | Get in the hall closet. Shut the door. Don't make a sound. | T3 | Banners from the private "Mom": "Get in the hall closet." / "Shut the door." / "Don't make a sound." |
| 2:13.6 | 1.16 | N | Mom says hide in the closet. | T3 | Nora whispering into the phone |
| 2:15.1 | 5.04 | D | Nora, no. That's where my phone is. Whatever's typing is in there. Lock yourself in the bathroom. | T3 | Call screen; on "in there" a fast cut to the closet door |
| 2:20.4 | 3.04 | N | I ran for the bathroom. Halfway there, my screen went black. Dead. | T3 | Hall, running; the phone in her hand goes black (battery dead): the landline is gone |
| 2:23.6 | 1.20 | — | *[silence 1.2 s]* | T3 | Dark hallway; her breath; the closet door beside her |
| 2:24.8 | 1.79 | N | And the closet door swung open by itself. | B9 | The hall closet door swings open on its own |
| 2:26.7 | 2.53 | N | Dad's coat. Nobody in it. But the sleeve was still swinging. | B9 | Inside: coats on hangers; Dad's grey winter coat in the middle; its empty sleeve still swinging, slowing |
| 2:29.5 | 2.04 | N | His phone was lit in the pocket, and it was typing. | B9 | Push in on the coat pocket: a phone screen glowing through the fabric |
| 2:31.6 | 4.00 | — | *[silence 4.0 s]* | B9 | THE scariest image, held ~4 s, no music: macro on the phone half out of the pocket, Family thread, draft field typing one letter at a time: "turn around nora" |
| 2:35.6 | 1.62 | N | It typed, turn around, Nora. I didn't. | B9 | Nora's face, eyes locked forward; behind her (out of focus) the front door, open to the chain, black gap |
| 2:37.4 | 3.58 | N | Then red and blue light slid under the front door. The gap eased shut by itself. | B10b | Red/blue wash pulses under the door and across the wall; the black gap narrows to nothing; the latch clicks |
| 2:41.2 | 2.16 | N | A man's voice. Police. Your dad called us. | B10b | Front door, three knocks, red/blue light |
| 2:43.6 | 1.95 | N | Voices lie. So I watched the light under the door. | B10b | Floor level: the strip under the door, red/blue only |
| 2:45.7 | 2.69 | N | Click. The hall light came on for them. It had never come on for her. | B10b | On "Click" the strip turns warm white: the motion light. Peephole: two officers, lit |
| 2:48.6 | 1.61 | N | So I broke Mom's rule. Chain off. | B10b | Insert: chain off |
| 2:50.4 | 3.42 | N | Two officers. And Mom, running out of the elevator in her blue scrubs. | B10b | Elevator panel arrives at 6; the lit corridor, a figure running toward us |
| 2:54.2 | 2.50 | R | Baby, my phone died at nine. I never texted you. | B11 | Insert: Mom's hand holding her phone, black, dead; it reflects the hall light |
| 2:57.0 | 1.39 | N | But the private chat knew Marigold. | B11 | Nora close-up, relief turning to fear |
| 2:58.6 | 3.48 | R | Nobody knows Marigold. We only ever said it out loud, in our kitchen. | B11 | Slow push into our dark kitchen behind them, the fridge note just visible |
| 3:02.4 | 1.71 | N | So whatever answered had been in our kitchen. | B11 | Nora looking back into the apartment, terrified |
| 3:04.3 | 2.34 | N | Then my dead phone lit up. The private chat. Mom. | B12 | Her black phone wakes by itself: lock screen, banner "Mom" (same avatar as frame 0) |
| 3:07.0 | 2.26 | P | Now I know whose voice you trust. | B12 | Private thread: typing dots for the FIRST time (the tell breaks), then "Now I know whose voice you trust." |
| 3:09.5 | 2.18 | X | Next time, I'll call from Room four twelve. | B12 | Second bubble, read in DAD's landline voice: "Next time, I'll call from Room 412." Bookend: phone over the front door, as in frame 0 |
| 3:11.8 | 1.50 | — | *[silence 1.5 s]* | B12 | Hold on the bookend frame; hard cut to black. No CTA, no part card |

## 2b. Narration (plain text, every spoken line in order)

The originality gate skips markdown tables, so the spoken lines are repeated here as prose so the gate checks them. (The storyboard plays per-line Kokoro wavs; this block is not used for TTS.)

```narration
Mom texted:

I'm outside. Unlock the door.

Nine seconds later:

Don't open it. I'm still at work.

And one of them was right outside our door.

Mom's rule is on our fridge. After ten, the door stays locked. Even for her. She has her own key.

Hands full, honey. Phone's on three percent. Please.

So I sent her the rule. Use your key.

Forgot them this morning. Check the hook.

Her keys were on the hook, on the red hospital lanyard. My hand went to the deadbolt.

Don't touch that lock.

How did she know? I typed, your keys are right here.

No they're not. They're in my pocket.

No typing dots. One second. And I was staring at her keys.

So I asked both of them for our code word. Mom and I picked it at the kitchen table. We never typed it anywhere.

Nora, I'm not doing this in the hallway. Open up.

Marigold. Now put the chain on.

Only Mom knew that. I slid the chain on.

Then the doorbell rang.

Through the peephole, blue scrubs. Head down. Too close to the lens to see a face.

Our hall light is on a motion sensor. It clicks on for anyone, even the neighbor's cat. It never clicked on.

Then Dad posted in the family chat. Dad never posts.

Dad was in Columbus till Sunday. And he has never lied to me.

I can see your shadow under the door, Nora.

The handle tilted down. Slowly. Then up.

I didn't text Dad back. I called him.

Two rings and a pause. Dad's old desk-phone ringtone. Not in my ear. Behind me. In our hall closet.

The ringing stopped. And in the family chat, Dad was typing.

I backed away from the closet and called the hotel number on the fridge. Room four twelve.

Hello? Nora? What's wrong, kiddo?

His real voice. Half asleep. Where's your phone, Dad?

My cell? It's in my winter coat. In the hall closet. I forgot it.

Then who's typing on it?

Stay on the line. I'm having the front desk call your police.

Eight minutes, they said. My battery said two percent.

Who are you whispering to, honey?

I looked at the hook. Empty. Nobody had come in. I'd been standing right here.

Then a key slid into our lock, from outside.

Even for her, the door stays locked. She has her own key.

The deadbolt turned. The door slammed open against the chain. Three inches of black. Nothing came in.

Get in the hall closet. Shut the door. Don't make a sound.

Mom says hide in the closet.

Nora, no. That's where my phone is. Whatever's typing is in there. Lock yourself in the bathroom.

I ran for the bathroom. Halfway there, my screen went black. Dead.

And the closet door swung open by itself.

Dad's coat. Nobody in it. But the sleeve was still swinging.

His phone was lit in the pocket, and it was typing.

It typed, turn around, Nora. I didn't.

Then red and blue light slid under the front door. The gap eased shut by itself.

A man's voice. Police. Your dad called us.

Voices lie. So I watched the light under the door.

Click. The hall light came on for them. It had never come on for her.

So I broke Mom's rule. Chain off.

Two officers. And Mom, running out of the elevator in her blue scrubs.

Baby, my phone died at nine. I never texted you.

But the private chat knew Marigold.

Nobody knows Marigold. We only ever said it out loud, in our kitchen.

So whatever answered had been in our kitchen.

Then my dead phone lit up. The private chat. Mom.

Now I know whose voice you trust.

Next time, I'll call from Room four twelve.
```

---

## 3. Shot list (storyboard.json scenes)

Built by build.py from the measured word times; every in-scene cut is anchored to a word. Kit components used: `horror/FrontDoor`, `horror/Peephole`, `horror/HandPhone`, `horror/Phone`, `horror/Protagonist`, `horror/LivingRoom`, `horror/Hallway`, `horror/ElevatorPanel`, `horror/Darkness`, `horror/Vignette`, `horror/Heartbeat`, `horror/Glitch`. Everything else is core layers or inline SVG drawn in build.py (the kit is locked, BRIEF 11:27).

| Scene | Start | End | Intent |
|---|---|---|---|
| s01_hook | 0:00.0 | 0:07.1 | FRAME 0 = COVER: both Mom banners fully readable on the lock screen (11:40), the front door sharp behind the phone with the red EXIT strip under it broken by two feet. Punch-ins: banner 1 on 'I'm outside', banner 2 on 'Nine seconds later'. |
| s02_door | 0:07.1 | 0:08.9 | Premise paid: the feet in the red EXIT glow. Hall light OFF (the motion sensor never fires for her). |
| s03_rule | 0:08.9 | 0:14.0 | Ownable rule + loophole on one prop. The small second line plants Lakeview Suites Rm 412 (paid at 1:35 and in the last line). |
| s04_group | 0:14.0 | 0:23.3 | Warm Mom: plausible details. Nora turns the rule into a test ('Rule. Use your key.'); the group Mom overrules it by pointing at the hook. |
| s05_hook_near_open | 0:23.3 | 0:27.5 | The hook confirms the group Mom (keys on a plain red lanyard). Then the near-open: the deadbolt thumb-turn, close. |
| s06_private_lie | 0:27.5 | 0:37.5 | The private Mom knows her hand is on the lock, then lies instantly (no typing dots): the clean catchable lie. |
| s07_codeword | 0:37.5 | 0:51.4 | Micro loop: the group dodges, the private chat answers the never-typed word and adds an order (chain on). |
| s08_bell_peephole | 0:51.4 | 1:01.7 | Peephole: dark corridor, red EXIT sign, blue scrubs pressed too close to the lens. The motion light rule is stated as history (it clicks on for anyone); it never fires. No on-screen flicker (real PIR lights hold 30 s+). |
| s09_dad_vouches | 1:01.7 | 1:10.0 | Dad's three bubbles land SILENT (no VO): the TEXT-FIGURE bubble rhythm, so his first heard voice is the landline. Behind Nora: the hall closet door. |
| s10_shadow_handle | 1:10.0 | 1:16.5 | Proximity: it sees her shadow; the lever tilts down slowly and back up (drawn insert, not the kit's fast jiggle). Typography ladder: the group Mom breaks into CAPS (silent alert bubble) with knocks. |
| s11_ring_in_closet | 1:16.5 | 1:28.5 | TURN (personal link): the voucher's phone rings in OUR hall closet. 4.0 s silence beat: two full ring cycles, the under-door glow pulses with each ring, music out. |
| s12_dad_typing | 1:28.5 | 1:33.2 | Isolation: the only channel answering is the enemy's. Dad's calm sentence-case bubbles land silent. |
| s13_hotel_landline | 1:33.2 | 1:53.4 | Lifeline: the hotel landline from the fridge note (Room 412). Real Dad: his cell is in his coat in the closet. Clock: police 8 min, her battery 2%. Call screen = one red End button (outgoing, then connected). |
| s14_barrier | 1:53.4 | 2:08.7 | Barrier ladder: hook empty (nobody came in) -> a key from outside -> the rule spoken back as dread (the fridge note's 'I HAVE MY KEY' turns red) -> the deadbolt turns -> the door slams to the chain; three inches of black. |
| s15_inversion | 2:08.7 | 2:24.8 | T3 rule inversion: the helper's protective order (hide in the closet) is the trap; the real authority names it ('that's where my phone is') and gives the opposite. She obeys him. Then the battery dies: the landline is gone. |
| s16_peak_closet | 2:24.8 | 2:37.4 | THE scariest image, once (~71%): the closet opens itself; Dad's coat, nobody in it, the sleeve still swinging; the phone in the pocket types a draft that addresses her ('turn around nora'), held still ~4 s with no music (the one intended hold over 3 s). Then her face, eyes forward; behind her the door's black gap. |
| s17_rescue_light | 2:37.4 | 2:48.6 | Rescue under red/blue. The gap closes by itself (latch click). The planted rule decides: on 'Click' the strip under the door turns from EXIT red to warm motion light, with two pairs of feet; peephole: two lit officers. |
| s18_chain_off | 2:48.6 | 2:54.2 | She breaks Mom's rule because the light test passed. Two officers in the lit corridor; the elevator reaches 6: Mom. |
| s19_twist | 2:54.2 | 3:04.3 | T8 after safety, NEW information: Mom's phone died at nine, so neither chat was ever her; and Marigold was only ever said out loud in our kitchen, so whatever answered had been inside our home. |
| s20_voice_swap | 3:04.3 | 3:13.3 | Her dead phone wakes. The private thread shows typing dots for the first time (the tell breaks), then the threat aimed at what she actually trusted: the Room 412 landline, read in Dad's voice. Last frame = frame 0's composition (phone over the front door). Hard cut, no CTA. |

---

## 4. Pacing check (PLAYBOOK §3, §7, §8), all measured

| Check | Target | Ours |
|---|---|---|
| Runtime | story sweet spot 165-250 s | **193.3 s** |
| Line 1 | ≤12 words, a place or object + danger | 7 words, "Mom texted: I'm outside. Unlock the door." (the door; the danger lands 3.4 s later) |
| Core hook | ≤30 words / ≤6 s; contradiction ≤11 s | 17 words; contradiction at **4.3 s**; danger at our door at 8.4 s; 32 words in the first 10 s |
| Frame 0 | the threat visible | both banners readable + the door with feet in the red EXIT strip (s01, Spark still checked) |
| Words per minute | 230-270 speaking (narrated) | **236.9 speaking**, 196.5 overall (18.6 s of planned silence + 14.4 s of breaths) |
| Jolt interval | median 6 s, none over 8 s | 76 jolts, **median 2.5 s, max 7.0 s** (2:08.7 helper order -> 2:15.7 Dad's answer) |
| Longest dry stretch | ≤25 s | 7.0 s |
| Picture change | every 2-3 s | every scene passes the 3.0 s hold rule except the planned 4.0 s peak hold (s16) |
| Turn | 45-60% (B8) | ringtone in the closet at 43% ("Behind me"), confirmed by real Dad at 54% |
| Scariest image | once, 60-80%, held ~4 s | the closet phone typing "turn around nora", 79-81%, held 4.0 s, music out |
| Lifeline under a clock | 70-90% | landline 48-74%, battery 2% from 57%, dies at 74%; police arrive at 81% |
| Truth twist | 85-95% | 90% (Mom's phone dead since nine; Marigold only ever spoken in our kitchen) |
| Rules / warnings | ≥2, ≥1 broken, one "remember this" plant | the fridge rule (used, attacked, broken), "put the chain on", "don't turn around", "hide in the closet" (disobeyed), "lock yourself in the bathroom" (obeyed) |
| Two ladders | proximity + channel removal | proximity: outside the door, near-open, chain, doorbell, peephole, shadow, handle, behind me, key in the lock, the gap, the closet opens. Channel removal: both Mom chats, Dad's account, the landline, her battery, then the dead phone wakes |
| Typography ladder | normal -> CAPS -> calm entity | group Mom calm -> "NORA. OPEN. THE DOOR." (caps, 1:15) -> Dad's calm sentence case (1:31) -> calm final threat (3:07) |
| Silences | 1-3 timed, 3-8 s with SFX | 4.0 s ring beat (1:24.5, two desk-bell cycles), 4.0 s peak hold (2:31.6, typing ticks); plus 2.6 s and 2.0 s silent-bubble beats, 1.5 s caps + knocks, 1.2 s after the battery dies |
| Numbers per minute | 3-5 (narrated) | 12 distinct (11:40, nine seconds, ten, 3%, Sunday, Room 412, 8 minutes, 2%, three inches, nine, two officers, 412 again): 3.7/min |
| Second person | narrated 5-15% | 6.8% of sentences (all inside messages or dialogue) |
| Sentence length | median 6-9, punch lines at spikes | median 4 overall / 5 narrator (chat-heavy format; chat punch share 49-55% in PLAYBOOK §7, ours 53%). Accepted: bubbles and verdict lines are short by design |
| Questions | 3.3/min | 8 (2.5/min): "How did she know?", "what's our word?", "Who are you whispering to?", "Then who's typing on it?"... |
| Loops open at the end | standalone 0-2 (+1) | 3 (keys, the thing in the house, the next call from Room 412) |
| Spoken subscribe / app funnel | none | none; hard cut on the bookend frame |

---

## 5. Production notes

- **Setting is an apartment** (producibility must-fix): corridor outside, red EXIT sign as the one fixed light source (it is what lights the strip and the feet under the door), the hall motion light that never fires, an elevator for Mom. No porch, snow, driveway or exterior set.
- **Drawn here, not in the kit** (build.py): the red EXIT strip + feet over `horror/FrontDoor` (hallLight 0), the warm strip that replaces it on "Click"; the peephole overlay (dark corridor, EXIT glow, blue-scrubs shoulders and a bowed head too close to the lens, no face; later two lit officers); the fridge note (Anton caps on a sticky, red underline keyframe, "I HAVE MY KEY" turning red on the callback); the key hook with and without keys; the deadbolt macro with a thumb-turn that rotates by keyframe; the lever macro that tilts slowly (the kit's lever only jiggles fast); the black door gap (a scaleX-keyframed slit at the latch edge) with cold-air dust particles; the inner-hall wall with a louvered closet door that swings open (scaleX hinge) and a phone glow under it that pulses with each ring; the closet interior (coats, Dad's grey coat, a separate sleeve layer swinging and decaying); the closet-phone macro with a core-text typewriter draft (cps 5); outgoing/connected call screens with one red End button and a per-second timer; the battery chip.
- **Cast.** Nora = `horror/Protagonist`. The figure at the door is never a face. The real Mom stays off-face (her hand + dead phone insert, the elevator, the corridor figure), so she is never read as Nora's rig recoloured. Dad is never seen.
- **The tell.** The private "Mom" never shows typing dots until the final threat (3:06). The group Mom always does.
- **SFX.** All cues exist in `studio/public/sfx/`. New, synthesised on the Spark CPU by sfx_synth.py (numpy, seeded, CC0 like pipeline/audio): `desk_bell_ring` (two 0.4 s bell bursts + pause, x2 cycles, muffled as if inside a coat), `key_scrape`, `siren` (distant to near), `relay_click` (the motion light).
- **Audio assembly.** pipeline/audio/make.py is single-voice, so the storyboard plays the per-line Kokoro wavs directly (`audio.voice`, `duckOn: voice`), as horror-delivery-photo-inside does. On the Spark they are in `studio/public/episodes/horror-mom-two-chats/vo/`.
- **Non-graphic.** No injury, no gore words, nothing visible in the door gap. The first 7 s and the cover are clean.
- **Generic UI only.** Thread titles "Family" and "Mom"; no messenger branding; "Lakeview Suites" is invented.
- **Disclosure (R5 + originality critique).** Description line: "Fictional story. Synthetic voices. All animation is original and drawn in code." Turn on TikTok's AI-generated label (realistic Kokoro voices); YouTube: not made for kids; the altered-content toggle is not required for clearly animated content with no real person's voice, but the description line covers the first-person framing.

---

## 6. How each critique was applied

**Retention (6).**
1. Dead phone held back: Dad never says it; it arrives only at the hug (2:54, 90%) as Mom's own line, and the twist adds new information (Marigold was only spoken aloud in our kitchen -> it was inside).
2. Marigold paid (2:58-3:02), with the "we never typed it anywhere" plant at 0:41.
3. Key logic: the group Mom says "Forgot them this morning. Check the hook." and the hook confirms it; "They're in my pocket" is the one clean lie.
4. Hook: attribution tags cut ("Mom texted:" / "Nine seconds later:"); both banners fully readable in frame 0; the contradiction lands at 4.3 s.
5. The private Mom's malice is on screen: "Get in the hall closet. Shut the door. Don't make a sound." (2:08), named as the trap by Dad.
6. The rule is a weapon ("Rule. Use your key." 0:19) and returns as a spoken line as the key turns (2:01).
7. Tags and recap cut; pace measured at 237 wpm speaking.
8. The peak is a physical hit: the sleeve still swinging, and a draft that addresses her ("turn around nora"), voiced as "It typed, turn around, Nora. I didn't."
Nice-to-haves: single ~3:13 story; physical rungs every few seconds (near-open 0:26, chain 0:50, doorbell 0:51); a short lethal clock (2% battery); no "all night"; distinct voices and silent fake-Dad bubbles; "Nobody had come in. I'd been standing right here."; no "same number, same photo".

**Reference (6).** Hook compressed (contradiction 4.3 s); Marigold paid with the never-typed suspicion; B8 re-cited (ringtone turn = 7666044652910316833 3:47) and a real T3 inversion added at 67-75% with DORM 1:28-1:37 cited at its true %; jolt max 7.0 s; silences of 4.0 s x2; wpm measured; alignment re-cited (instant reply = SIEGE 0:39; the overrule = FARM 0:39-0:52 with Nora's objection; no FARM rescue-clock claim); near-open at the deadbolt (0:26); the ending makes the trusted landline suspect, in Dad's voice, and bookends frame 0. Motion light planted as a countable rule before it pays; battery clock; one prop carries the rule + Room 412; caps ladder; sharp feet in the cover.

**Originality (7).** Keys fixed; no moth flicker; Marigold paid; ringtone device cited (7666044652910316833 3:47); hook within limits; deadbolt continuity: the key unlocks the deadbolt, the door slams to the chain, the gap "eased shut by itself" (latch click), then "Chain off" opens it. Nice-to-haves: "3%" is now labelled a second lie; "your police" covers Columbus 911; plain red lanyard, no badge; disclosure in section 5; typing dots break at the payoff.

**Producibility (5).** Apartment setting; peephole figure, EXIT light, draft typewriter, closet door + interior, slow lever, deadbolt turn, door gap, outgoing call screen, battery chip all built from core layers/SVG with no kit edit; shots that needed rig poses (running Mom, hug, hand on knob, back-of-head with glints) replaced (elevator + corridor figure, dead-phone hand insert, swinging closet door, SVG back silhouette with no eyes); 4 SFX synthesised and cued by name; music drops done as music segments; the shot list is keyed to measured words, not paragraphs (no build.py paragraph coupling); holds ≤3 s except the planned peak; no PART 2 card (single cut, hard cut).

---

## 7. Spark proof

- `storyboard.json` validates with `npm run validate` (zod) on the Spark: 20 scenes, 193.30 s, 629 caption words, 11 kit components.
- `scripts/check_storyboards.py` on the Spark: 0 missing components, 0 missing audio, max hold 4.0 s (the planned peak only).
- Stills: `out/stills/horror-mom-two-chats_v1a.jpg`, `_v1b.jpg`, `_v1c.jpg` (80 frames). Fixed after review: the cover phone moved off the door so the feet strip reads; the fridge note text resized to fit; call timers no longer leak across cuts; the closet interior lit enough to read the coat and sleeve; the draft field lifted clear of the pocket.

---

## 8. Jolt map (measured)

0:00.0 two Mom banners (frame 0), 0:00.9 unlock the door, 0:03.3 nine seconds later, 0:04.3 don't open it (contradiction), 0:07.9 one of them is outside our door, 0:10.3 rule: door locked after ten, 0:12.8 loophole: she has her own key, 0:15.5 3% battery plea, 0:19.4 rule as a test: use your key, 0:22.2 check the hook, 0:23.3 keys on the hook, 0:26.1 hand on the deadbolt, 0:27.5 private: don't touch that lock, 0:29.2 how did she know?, 0:31.8 they're in my pocket (lie), 0:34.4 no typing dots, 0:37.5 code word asked, 0:41.5 never typed it, 0:42.7 group dodges, 0:46.7 Marigold, 0:50.5 chain on, 0:51.6 doorbell, 0:53.1 peephole: scrubs too close, 0:56.5 motion light rule, 1:00.8 it never clicked on, 1:03.5 Dad never posts, 1:04.4 silent Dad bubbles, 1:09.0 never lied, 1:10.0 I can see your shadow, 1:13.1 handle tilts, 1:15.0 CAPS + knocks, 1:17.7 calls Dad, 1:18.3 ringback, 1:19.3 ringtone, 1:22.9 behind me, in the closet, 1:24.5 4 s ring silence, 1:30.3 Dad is typing, 1:31.2 don't turn around, 1:36.4 Room 412, 1:37.6 real Dad answers, 1:44.1 cell in the closet, 1:45.6 who's typing?, 1:49.1 police called, 1:52.1 8 minutes / 2%, 1:53.4 it hears her, 1:56.2 hook empty, 1:56.8 nobody came in, 1:59.1 key in the lock, 2:00.9 rule spoken back, 2:05.1 deadbolt turns / chain, 2:08.7 helper: hide in the closet, 2:15.7 Dad: that's where my phone is, 2:19.6 bathroom, 2:22.6 battery dies, 2:25.5 closet opens itself, 2:28.3 sleeve still swinging, 2:31.1 phone typing, 2:32.2 draft: turn around nora, 2:37.0 I didn't, 2:37.4 red/blue light, 2:39.7 gap closes, 2:42.0 police, 2:44.5 light test, 2:45.7 light clicks on, 2:47.6 never for her, 2:49.7 breaks the rule: chain off, 2:51.5 Mom from the elevator, 2:54.9 Mom: phone died at nine, 2:55.8 I never texted you, 2:57.0 it knew Marigold, 3:01.7 only said in our kitchen, 3:02.4 it was in our kitchen, 3:05.0 dead phone lights up, 3:06.1 first typing dots, 3:07.0 whose voice you trust, 3:09.5 Room 412, in Dad's voice

Median gap 2.52 s, max 7.01 s (76 jolts).

---

## 9. Originality gate

Command (repo root): `python3 scripts/originality_check.py backlog/horror/horror-mom-two-chats/script.md research/corpus research/library/transcripts`

Result (2026-11-01 ~12:35 UTC, final text): **PASS** (210 source files scanned).
- Highest single-source 5-gram share: 0.14% (the three PLAYBOOK.md files, from the gate command quoted in this section). Limit 2%.
- Longest shared run: 7 words, again only the quoted gate command line. For the spoken lines alone (section 2b) the longest run against any source is 5 words, the generic "door, don't make a sound" (library control dqEIz_8bP-8). Limit 8.
- The gate skips markdown tables, so section 2b repeats every spoken line as prose; the PASS covers it.
