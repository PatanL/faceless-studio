# BV1nEoYBBEXE: killer in the complex, a danmaku overlay, a livestream show (R2 seed)

> Internal research only. This is a study of structure and mechanics. **Never translate, retell or remix this story for publication.** Section 6 lists what a transposed story must not reuse.

## 1. Header

| Field | Value |
|---|---|
| Title | 小区闯入了杀人犯，我却能看见弹幕，原来这是一场直播秀 ("A killer got into my complex, but I can see danmaku: it turns out this is a livestream show") |
| URL | https://www.bilibili.com/video/BV1nEoYBBEXE |
| Channel | 杰出影视本人 (Bilibili mid 75872737), tags 悬疑 / 原创动画 |
| Published | 2026-04-23 |
| Views | 151,701 plays, 4,075 likes (2026-11-01). That is about 2.5x the channel median of 61K for the 38 uploads within ±60 days |
| Duration | 7:21 (441 s), single episode, no part 2 found in 421 of the channel's 471 uploads. The final viewer danmaku asks 后续在哪 ("where's the sequel?") |
| Studio's own precedent | 【迷雾弹幕】 BV1EKG9zwEYi (2025-04-30, 150K, 8:58): an earlier dorm-killer episode built on the same danmaku device. The studio reuses the device about once a year at roughly the same view level |
| English reposts | **Confirmed.** mraevq TikTok 7654526047005723937: **717K**, 2026-06-23. It is a near line-by-line translation, cut to 5:58 at about 265 English wpm, with names swapped (张伯 to "Jake", 红霞 to "Ruby"). Its transcript is in `research/library/transcripts/7654526047005723937.txt`, so the originality check already covers its English wording. It ends with "Tap the story below to watch the full ending" even though the source has no sequel. udhwkz TikTok 7659677578365537569: 376K, 2026-07-07. That one comes from the sister animation by 橘里漫剧 (BV1f9TF6DEEz, 18.4K, the hallway-song version of the same web-fiction premise). 胡说漫's Qx_l91Oz7YI (98 views, 2026-06-17) is a later re-adaptation. The best repost has about 4.7x the source's views |
| Premise origin | Probably a web-fiction short story (知乎/番茄 type), because three studios animated it within 10 weeks. 杰出影视's danmaku and livestream layer seems to be its own addition: the other two versions use a hallway song instead |
| Extraction | Spark CPU: 480p video and audio in `~/studio/refs/horror-cn/BV1nEoYBBEXE/`. Bilibili CC subs need a login, so none were downloaded. Viewer danmaku XML (110 comments) was saved. Full narration came from OCR (rapidocr, 1 fps) of the burned-in captions (`captions_ocr.txt`, 294 lines). Chat, SMS and overlay text came from frame OCR (`onscreen_ocr.txt`). faster-whisper medium (zh, int8, 4 threads, `whisper_zh.txt`) agrees with the caption OCR line for line wherever I compared them (first 3:30); it was still running on a loaded box when this was written. English working translation: `translation_en.txt` (Spark only, never in the repo) |

**Caption self-censorship (a genre habit worth knowing).** The voice says 杀人犯 (killer), 杀掉 (kill), 死 (death) and 尸体 (corpse). The burned-in captions write 虾人犯 ("shrimp-person criminal"), 虾掉, 三 and 户体. Viewers turn this into a running joke: the first danmaku lines are 《虾人犯》. The English equivalent is TikTok algospeak ("unalive"). Our captions should avoid trigger words the same way, without making a joke of it.

## 2. Story outline (my summary)

Night. In the residents' group chat of a big housing complex, the property admin ("Uncle Zhang") warns that a killer has got in. Two minutes later several neighbours post that he has been caught. A policeman knocks on the narrator's door (Chen Jie, block 13, flat 802). As he reaches for the handle, glowing text appears in front of his eyes: the "cop" is the killer in a fake uniform, and this is his seventh flat. He counts the neighbours who posted the all-clear: exactly six. They are probably dead, and the killer is posting from their phones.

The cop gets aggressive and radios in that 13-802 is refusing. The group chat reacts at once: neighbours @mention Chen Jie to cooperate, and the admin says the landlord is bringing a key. Chen Jie reasons that the admin posted the first alert, so the admin is probably dead too, and he trusts nobody. The floating text speaks again. It calls him "streamer", says the chat is all the killer's alt accounts, and says a phone call would settle it. He has no signal and his messages won't send. A neighbour, "Li Ping" from 601, posts that there are bloody footprints in the lift and that he must not open, because it isn't the police. Then the admin mutes the whole group. The overlay concludes that he is the unwitting star of a staged survival livestream, that "no round is unwinnable" and that a clue exists.

He remembers a black phone that the previous tenant left under the bed. With one bar of battery he reaches the real police. They tell him the complex is jammed, the target is a murder gang rather than a lone killer, and the real property manager is a middle-aged woman standing with them at the perimeter. So the admin account is an impostor. The phone dies. In its last seconds he sees an SMS on it: "Don't let them find you."

The knocking stops and he hears a crash below. A middle-aged woman rings frantically, says she is Li Ping from 601 and that the cop smashed her lock while she hid on the landing above. The overlay argues about whether she is a planted "hook wolf". He checks that her hands are empty and lets her in, but he hides the phone call and the gang detail from her. He asks how long the lock-smash took ("under a minute"). The fake cop returns with a hammer. The door opens outward, so it can't be braced. Chen Jie proposes an ambush: lights off, she hides in the bedroom and makes a noise, and he waits in the kitchen by the door with a knife. The door gives, a phone rings inside, and the cop rushes past the kitchen. "Li Ping" runs out shouting "he's in the kitchen!" But he is already gone.

Reveal: he never trusted her. Everyone knew the killer walked down from 8 to 6, so anyone hiding on the 7th-floor landing would have been caught. In the lift he presses every floor from 1 to 5 and gets off at 6. The overlay celebrates, with jokes about wetting themselves. Flat 601 is ajar, because the gang really did smash it to stage the act. A body lies on the sofa. On the table is a walkie-talkie, and through it he hears the gang argue about which floor he left the lift on. A leader assigns the sweep: one member takes a lift down, the fake cop takes the other lift up, and they will search down from the roof and "collect the radio when you reach 6", which is the floor he is on. The other blocks are already "processing the goods". The last line threatens to make the "little loach" beg for death. It ends there.

Short quotes used for analysis (3):
- Overlay hook, 0:10: 这已经是他骗的第七户了 ("this is already the seventh flat he's tricked").
- Count clue, 0:19: 不多不少正好六个 ("no more, no less: exactly six").
- Game-rule promise, 2:05: 每场直播都没有必死的局 ("no round of the stream is a certain death").

## 3. Beat table

| Time | Beat | Mechanic | What the viewer believes now | Open loops |
|---|---|---|---|---|
| 0:00–0:08 | Admin alert, then the all-clear, then a knock | **Fake authority + all-clear**; cold open with no intro | There was a killer, he's caught, the cop is routine | Why so fast? |
| 0:09–0:14 | Glowing text: the cop is the killer, this is the 7th flat | **Supernatural overlay contradicts the authority** (the hook at 9 s) | The person at the door is the killer | What is the text? Who writes it? |
| 0:15–0:22 | Exactly six people posted the all-clear | **Count clue** (6 posters plus the hero = 7th) | The six are dead; their phones are being used | Is the whole chat fake? |
| 0:23–0:35 | Cop pounds and radios "13-802 refusing" | **Escalation + door threat** | He's being cornered | Who's on the radio? |
| 0:36–0:57 | Chat answers the radio call in real time; @mentions; landlord key threat | **Group-chat pressure + fake authority with wrong detail** (the chat knows something only audible at the door; the "polite 20-year-old cop" corroboration) + **timer** (the key is coming) | The chat is coordinated with the door | Is Uncle Zhang dead? |
| 0:58–1:11 | Hero's deduction: the first poster is a suspect; trust no one; looks for a weapon | **Hero voices the viewer's deduction** | Everyone online is hostile | — |
| 1:12–1:24 | Overlay: "the streamer has brains", "he has a gun", "just call" | **Overlay as a chorus**: praise, dread and a hint in one beat | The overlay is an audience | Why "streamer"? |
| 1:25–1:38 | No signal, messages won't send | **Isolation / comms cut** | Truly alone | — |
| 1:39–1:55 | 601 posts bloody footprints, "don't open, not police"; admin mutes everyone | **Trusted contrarian voice** (later contradicted) + **mute** | 601 is an ally; the admin is the killer | What are the "stolen goods"? |
| 1:56–2:16 | "Wait to die?" Overlay: dead end, but "no round is unwinnable"; title reveal: a livestream show | **Game-rule promise** (a clue exists) + **premise reveal at 30%** | It's a rigged death-game stream with an audience | Who runs the stream? |
| 2:17–2:26 | The previous tenant's phone under the bed, 1 bar | **Burner phone / timer** | A lifeline exists | Why did the tenant leave it? |
| 2:27–3:03 | Police: jammed zone, a gang not one killer, real manager = middle-aged woman Du Mei; 30 s battery; call drops | **Trusted source (real police) contradicts the chat**, a **scale escalation** (gang) and an **identity check** (admin is fake) | The admin is fake; it's many people | Why no police inside? |
| 3:04–3:11 | Overlay: "dumb, read the texts first"; SMS: "Don't let them find you" | **Missed-clue sting** (the overlay scolds) | Someone warned before | Who sent it? |
| 3:12–3:24 | Knocking stops, the cop leaves, a crash, frantic doorbell | **Breather, then a new knock** | The danger moved | Where did he go? |
| 3:25–3:45 | "Li Ping from 601": he smashed my lock, I hid one floor up | **Second visitor / ally-at-the-door** | Probably the ally from the chat | Is she real? |
| 3:46–4:03 | Overlay debates: "hook wolf planted in the chat?" "I'll eat poop if he survives" | **Audience as a split jury**: it states the suspicion aloud, then muddies it | 50/50 | — |
| 4:04–4:37 | Checks her empty hands, opens; hides the phone and the gang info; asks how long the smash took ("under a minute") | **Information asymmetry** + **timer elicitation** | The hero might be fooled; viewer tension rises | What is he planning? |
| 4:38–5:12 | Cop returns with a hammer; the door opens outward; ambush plan | **Plan stated aloud** (it reads as a bait plan) | Ambush with Li Ping | Will she betray him? |
| 5:13–5:37 | Breaker off, darkness, knife; the door gives; a phone rings; Li Ping shouts "he's in the kitchen"; he's gone | **Betrayal reveal + vanish** | She was the gang's plant; where is he? | How did he get out? |
| 5:38–5:51 | Elevator; explains the 7th-floor logic; presses 1–5, exits at 6 | **Reversal: the hero was ahead all along** + a **floor-logic clue** pays off | The hero is smart; he faked his floor | — |
| 5:52–6:10 | Overlay celebrates, diaper jokes, "he can't escape death in the end" | **Comic relief + doom reset** | A breather | — |
| 6:11–6:32 | 601 ajar; real body on the sofa; overlay: "the killers' stream ended long ago" | **Scene of the real victim**; **second stream exists** | The gang is also streamed / a cult? | Two streams? |
| 6:33–7:20 | Radio on the table: the gang argues lift logic, the leader orders a sweep down to 6 and "collect the radio"; "other blocks processing goods"; final threat | **Overheard plan (dramatic irony) + countdown aimed at the hero's floor**; hard cliffhanger | They're coming to exactly where he is | Everything: goods, cult, police, tenant, Hongxia = Li Ping? |

## 4. Clue chain

| Clue (planted) | Where | Payoff |
|---|---|---|
| "Seventh flat" (overlay) | 0:10 | Combined with **exactly six** all-clear posters (0:19), the hero is #7. The chat is dead people's phones |
| The chat replies to a radio call only audible at the door ("13-802 has a situation") | 0:33–0:42 | Proves the chat and the door are one operation (implicit; the hero states "they all push me to open") |
| "Polite 20-year-old cop came by and left" (fake corroborating detail) | 0:03 chat | Fake detail builds false trust. Not paid off explicitly. Viewers instead flagged **a lone cop** (police come in pairs) as the tell: 8 danmaku say so |
| The admin posted the first alert | 1:00 | Police at 2:55: the real manager is Du Mei, a middle-aged woman at the perimeter. The admin account is an impostor |
| "Stolen goods are no small matter" (admin, mute pretext) | 1:48 | 7:14 "other blocks are processing the goods". Never explained (open loop: trafficking implied) |
| Previous tenant's black phone, "he said he didn't want it back" | 2:17 | Works in a jammed zone. SMS "Don't let them find you" (3:08) means the previous tenant knew. Unresolved |
| Battery 1 bar / 30 s | 2:23, 2:40 | Forces the call to drop before full info; sets up the "read the SMS first" sting |
| Overlay "no round is unwinnable, there's a clue" | 2:05 | Licenses the reader to hunt; paid by the 7th-floor deduction |
| The 601 chat message warning "not police" (trust deposit) | 1:39 | 601 "Li Ping" shows up in person (3:25) and betrays him at 5:31. The warning was the setup |
| Li Ping's alibi: hid on the landing one floor up | 3:38 | 5:41: the killer walked 8 to 6 and would have passed her, so she lied |
| Real police say the manager is a **middle-aged woman** | 2:57 | Li Ping is also a middle-aged woman. Viewer danmaku at 3:51 suspects her. Never confirmed (an open loop for a sequel) |
| "How long did the smash take?" "Under a minute" | 4:30 | Times the ambush and escape window (implicit) |
| The door opens **outward**, can't be braced | 4:45 | Lets him slip out past the cop who charges inward (5:28) |
| He hides the phone call and the gang info from Li Ping | 4:20 | She still thinks it's one man, so the gang doesn't learn what he knows |
| Lift: presses 1–5, exits at 6 | 5:48 | 6:40 the gang argues which floor; 601 (on 6) is the last place they'd look, until "collect the radio at 6" |
| Overlay: "anyone still watching the killers' stream?" | 6:25 | Sets up two streams / a cult. Open loop |
| Walkie-talkie left on the 601 table | 6:33 | The overheard sweep plan targets floor 6. Cliffhanger |

## 5. Twist inventory

| # | Twist | Type | Setup |
|---|---|---|---|
| 1 | The cop at the door is the killer | **Trusted authority is the threat** | Cold-open all-clear, then a supernatural overlay at 9 s. Told rather than deduced: the twist is the hook |
| 2 | The all-clear posters are dead; their phones are being used | **Count deduction** | "Seventh flat" + "exactly six" |
| 3 | He is the unwitting star of a staged death-game livestream; the overlay is the audience | **Genre/frame reveal** (system / 弹幕 / 无限流 trope) | The overlay calls him "streamer" at 1:15, then the explicit line at 2:16 |
| 4 | The admin is an impostor; the real manager is elsewhere | **Identity contradiction from a trusted outside source** | The admin posted first; police name the real manager |
| 5 | It's a gang, not a lone killer | **Scale escalation** | A lone-cop oddity; six phones at once (viewers questioned it) |
| 6 | The friendly neighbour is a plant ("hook wolf") | **Ally betrayal** | Her warning in the chat (trust deposit), the mute (excuse for not going home), the overlay naming the suspicion and then doubting it |
| 7 | The hero was never fooled and escaped during his own ambush | **Competence reversal** (智斗) | The withheld info, the "under a minute" timer, the outward door, then the floor logic explained after the escape |
| 8 | The killers have their own stream / a cult | **World expansion** | Two lines of overlay at 6:25 |
| 9 | The gang's sweep converges on his floor; more members are in other blocks | **Cliffhanger countdown** | Walkie-talkie dramatic irony |

## 6. GENERIC vs SPECIFIC

**GENERIC (genre conventions anyone can use):**
- A resident or tenant alone at night; a building-wide threat announced in a group chat.
- An all-clear that comes too fast; an authority figure at the door; the peephole POV.
- An information overlay only the hero can see. The broad family is "system / bullet comments / hidden audience / annotated reality". The device is a genre staple (无限流, 系统文); this studio already used it in 2025.
- Counting clues (N messages vs N victims), a chat that knows what it shouldn't, impostor admin accounts.
- Comms cut / jamming, a muted chat, a dying battery as a timer, an old phone left by a previous occupant.
- A neighbour who asks to be let in; testing a visitor with a factual question; the hero withholding info from an ally.
- An ambush plan that is secretly an escape; an alibi broken by spatial logic.
- Overheard enemy comms; an open-ended gang cliffhanger; an audience that jokes to vent tension.
- Caption self-censorship of death words.

**SPECIFIC (this author's or this web novel's expression; a transposed story must NOT reuse):**
- The combination: **killer in a fake police uniform + "seventh flat" + exactly six all-clear posters**.
- **Danmaku livestream show** as the frame for a **killer-in-the-complex** story, i.e. the hero being an unwitting streamer of a murder show with viewers who joke about diapers.
- The **601 bloody-footprints-in-the-lift** warning, then the **group mute** under a "stolen goods" pretext.
- The **previous tenant's phone under the bed**, the SMS "Don't let them find you", and real police describing the real manager as a middle-aged woman at the perimeter.
- The **"hid on the landing one floor up / the killer walked 8 to 6"** alibi break.
- The **lights-off kitchen ambush with an outward-opening door** and the escape during the ambush.
- **Press floors 1–5, exit at 6**, then hide in the victim's flat and find the gang's **walkie-talkie** with the sweep plan.
- Names and places: Chen Jie, 13-802, Anxinyuan (安心苑), Uncle Zhang, Li Ping/601, Du Mei, Hongxia, Qian Ren, Mao Gui. The "little loach" (小泥鳅) epithet; "processing the goods"; the "hook wolf" line; the diaper and handstand-eat-poop jokes; the wording of the three quoted lines above.
- The twist order 1 to 9 as a chain. A transposition may reuse at most two or three generic mechanics, in a different order, with a different frame, a different threat and a different escape logic.

**Transposition notes (for our writers):** what travels is (a) an overlay that contradicts authority within 10 s, (b) a numeric deduction by 20 s, (c) a trusted voice that turns out to be the trap, and (d) a hero who out-thinks the trap, with the explanation **after** the escape. Build a new frame for the overlay. Change the threat, the location and the clue math. Keep the cadence.

## 7. Pacing

- **Density:** 294 caption lines and about 2,736 hanzi in 441 s, which is **about 373 hanzi/min and 40 caption lines/min (one line per about 1.5 s)**. Per minute it is very flat: 389 / 385 / 380 / 350 / 377 / 389 / 374 hanzi. No slow sections; tension comes from content, not tempo changes. The English repost runs about 1,590 words in 5:58, **about 265 wpm**: TTS reposts compress about 20% in time by speeding up.
- **Narration mode:** first-person past tense with all dialogue read by the narrator voice. Chat messages are read aloud in full while the chat UI is on screen.
- **Hook:** premise plus reversal in 9 s: alert, all-clear, knock, then the overlay. The count clue lands at 19 s. There is no title card or intro.
- **Re-hook interval:** a new reveal, contradiction or escalation every **about 15–25 s** (beats at 0:09, 0:19, 0:33, 0:44, 1:12, 1:25, 1:39, 1:48, 2:05, 2:17, 2:30, 2:55, 3:08, 3:25, 3:46, 4:30, 4:38, 5:24, 5:38, 6:11, 6:33). **Overlay interjections** (the chorus) come at 0:09, 1:12, 2:02, 3:04, 3:46, 5:52 and 6:22, about every 50–60 s. Each one re-states stakes, hints, or doubts the hero.
- **Structure by %:** hook 0–2%, isolation build to 27%, premise reveal at 30%, lifeline call 33–41%, second visitor 46–58%, ambush and betrayal 68–76%, explanation 77–80%, aftermath and enemy plan 84–100%. The **trap (the ally at the door) sits in the middle**; the **reversal at about 77%**; and the **last 15% re-opens the danger**.
- **Cliffhanger mechanics:** no resolution. It ends on the villain's threat while the sweep converges on the hero's floor, with 5+ open loops (goods, cult stream, missing police, previous tenant, Hongxia/Li Ping identity). Viewers ask for the sequel. Reposters add a "watch the full ending" CTA and split it into parts (udhwkz posts Part 2 first).
- **Comment bait:** deliberate or tolerated logic gaps (a lone cop, six phones at once, an outward door, "emergency calls work without signal") produced most of the 110 danmaku. Nitpicks drive engagement.

## 8. Visual vocabulary

- **Style:** flat 2D 沙雕-style cutout animation; limited motion (pose swaps, small shakes, smoke puffs); 16:9 landscape at 852x480 (reposts crop to 9:16 or letterbox). Watermark top right.
- **Hero:** one recurring design: a neon yellow-green jacket with a lightning-bolt patch, a white T-shirt and a pale face. Expressions are the main acting: **saucer-eyed shock** (white rings), squint suspicion, sweat, a hand-on-chin "I figured it out" pose for the reveal.
- **Phone UI types:**
  - (1) A WeChat-style group chat, "安心苑物业群(156)", shown as a big phone mock beside the hero. Avatars, display names in the 栋-室-name format (`7栋1801刘顺`), @mentions, the moon-avatar admin. Messages fill progressively.
  - (2) A full-screen **battery 1%** icon on black.
  - (3) A phone-to-ear call with a lightning "ringing" spark.
  - (4) An SMS screen with a yellow header, "手机短信", and one line of text.
  - (5) A "no signal" moment shown by the hero's face plus the caption only.
- **Overlay:** the danmaku is not drawn as scrolling bullet comments. It is a **glowing electric-blue framed panel with red/pink 3–4-line text** that pops beside the hero's head, a "system window" look. Our transposition should invent its own overlay look.
- **Rooms and shots:**
  - The front door from inside (black door, lever handle, peephole), a peephole/corridor cutaway of the visitor.
  - Bedroom (grey bed, books), kitchen (dark), a "lights off" grey tint over the same layout.
  - An **elevator button panel close-up** with a finger pressing (10…1, -1, -2).
  - A pink living room with a bookshelf and a sofa body (stylized, bloodless).
  - A **walkie-talkie on a round table** with a lightning spark for the voices.
- **Antagonists:** the fake cop in a blue shirt and a hi-vis "POLICE" vest, with a hammer and a radio; his face is half-shadowed by hair. The "POLICE" text is often mirrored (a flipped asset). The female plant: middle-aged, purple top, pink blush, a smile that turns sinister when she shouts.
- **Captions:** bottom centre, white with a black outline, one short clause each (6–12 hanzi), always on. Death words are spelled with substitutes (see Header).
