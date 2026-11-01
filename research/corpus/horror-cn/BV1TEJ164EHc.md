# 拦车孝: "never overtake a hearse" (BV1TEJ164EHc), source study

> **Internal research only.** This file studies how the story is built so we can write *original, transposed* stories. Never translate, retell or remix this story (or its underlying web-fiction text) for publication. Short Chinese lines are quoted only to analyse devices. BRIEF rule 5 and the originality gate both apply.

## 1. Header

| Field | Value |
|---|---|
| URL | https://www.bilibili.com/video/BV1TEJ164EHc |
| Title | 你们知道拦车孝吗？遇到灵车千万别超车！ ("Do you know 'blocking the hearse for filial respect'? If you meet a hearse, never overtake it!") |
| Channel | 异常收录档案 (Bilibili mid 3461575153289625) |
| Published | 2026-10-15 |
| Views | 740,655 plays, 42,935 likes (2026-11-01) |
| Duration | 1,293 s (21:33), single part, 16:9, 1080p master |
| English repost evidence | **Confirmed.** udhwkz TikTok Part 1 [7702661541224566049](https://www.tiktok.com/@udhwkz/video/7702661541224566049): 2.2M views, 164K likes. Part 2 [7702661471641128224](https://www.tiktok.com/@udhwkz/video/7702661471641128224): 343K. Both posted 2026-10-31, 16 days after the source, at about 3.0× the source's views. Part 1 covers source 0:00–4:28 (ends when the companion asks to drive). Part 2 covers 4:28–8:44 (ends on the expert naming the entity). Annotated in `research/corpus/horror/7702661541224566049.md` and `…471641128224.md`. No Part 3 was seen. |
| Underlying text | The animation adapts a web-fiction text, 路游魂 ("road-wandering soul"). A plain TTS reading of the same text, 肉肉讲故事 [JnjiZiM8gjk](https://www.youtube.com/watch?v=JnjiZiM8gjk) (29:38, 766 views, 2026-05-24), predates the animation by almost 5 months, and its lines match the animation's captions nearly word for word. This is the "one text, several studios" pattern again (see `SOURCES.md` finding 4). The premise is not the studio's own either. |
| Genre / register | 异常收录档案 folk-taboo register: a "你们知道X吗？" (did you know X?) title, a trade rule ("开大车的都知道", "every trucker knows"), rural funeral customs, a folk-religion expert. It is **not** a group-chat / phone-UI story. The single phone screen is one call. |

### How this was studied (Spark CPU, `nice -n 10`, `CUDA_VISIBLE_DEVICES=""`)

- **Video.** Bilibili gives a logged-out viewer only a **trial stream of the first 525 s (0:00–8:45)**. Every quality and API variant (`durl` length 524,980 ms, `timelength` 1,293,235) behaves this way, and yt-dlp got HTTP 567 on a full GET. I downloaded the 480p trial stream with 1 MB range requests. It matches the server md5. Saved to `dgx-spark:~/studio/refs/horror-cn/BV1TEJ164EHc/BV1TEJ164EHc.mp4`.
  - **The udhwkz repost ends at exactly 8:44 too.** The English reposter very likely cut its two parts from the same logged-out trial stream.
- **Subtitles.** There are no auto-subs without a login. The video has **burned-in captions**, so those are the text:
  - rapidocr (venv r2, 2 threads) on 1 frame per 2 s gave 263 frames: `ocr.jsonl`.
  - A partial 2 fps pass on the caption band gave the card timing: `ocr_cap.jsonl`.
  - faster-whisper small (zh, CPU, 4 threads) is a cross-check: `BV1TEJ164EHc.zh.txt`. It was still running at write time because the box load was about 50.
- **8:45–21:33.** The rest of the plot comes from the 肉肉讲故事 reading's uploaded zh subtitles (`rourou_JnjiZiM8gjk.zh.vtt` → `rourou_text.txt`, 970 lines). The two versions align at a steady rate: animation time ≈ reading time × 0.72–0.74. This is checked at 0:34, 4:20 and 8:44, and the end-to-end durations agree (1,293 s ≈ 1,778 s × 0.727).
  - I mapped the times as `anim = 525 + (reading − 735) × 0.736`. Then I checked them against 14 time-stamped danmaku anchors from the full 21:33 (178 danmaku in `BV1TEJ164EHc.danmaku.xml`). They agree within about ±15 s.
  - Times after 8:45 are marked **~** (estimated).
- **Merged text.** The merged Chinese text (OCR captions, then the mapped reading) is `BV1TEJ164EHc.merged_zh.tsv`: 807 lines. A contact sheet (1 tile per 10 s, 0:00–8:45) is `sheet.jpg`.
- **Differences found.** The animation drops a few aside lines that are in the text:
  - "he's new and doesn't know the rules yet"
  - "his jaw dropped; I smiled and stretched"

  Otherwise it keeps the text in order. The narrator is 冬哥 "Dong-ge" in the animation and 远哥 in the reading. Danmaku give his full name as 张东东.

## 2. Story outline (my English summary)

**Act 1: the rules and the mirror (0:00–5:58).** A veteran trucker, Dong, drives at night with his young co-driver Xiao Wu.
- **The rules.** A funeral convoy merges in ahead of them: a lead sedan with a white flower bow, and a hearse with 奠 ("mourning") on the rear glass. Dong states the trade rule: you never overtake a hearse. The next exit is 47 km away, but this stretch kills a dozen people a year, so crawling behind the convoy is "safe".
- **Rule two is broken.** Xiao Wu grumbles, rolls down the window and spits ("bad luck"). Dong snaps out rule two: never open a window at night. Xiao Wu goes quiet with an odd face.
- **The stranger's ritual.** A big truck, plate J1574, overtakes the convoy and stops across its front. Its driver walks back stiff-legged, kneels, and kowtows three times hard enough to hear from tens of metres. Then he raises both hands. The hearse's rear door opens, a corner is torn from the white cloth over the coffin, and he receives it and drives off.
- **The explanation.** Dong explains the local custom of 拦车孝, "blocking the hearse to pay filial respect". A distant relative, or someone who owed the dead a favour, who missed the last goodbye stops the convoy, kowtows three times, and asks for a scrap of mourning cloth to enshrine.
- **Xiao Wu repeats it.** Xiao Wu says the portrait on the coffin looked like his maternal uncle. His seatbelt clicks off. He opens the door while the truck is moving, jumps out, rolls without pain, and walks stiff-kneed to the hearse. The convoy has stopped as if it were waiting for him. He performs the same ritual, lying flat on the third bow. This time a thin, dry hand passes the cloth out of the hearse's *window*.
- **Wrong return.** He comes back too neat: cloth folded into his pocket, hands on his knees, face bluish-white in the dash light. He insists it was his uncle and that he saw the portrait "when we passed the hearse". Dong knows Xiao Wu is an only child but not whether his mother has siblings.
- **The drive.** Xiao Wu offers to drive, and Dong lets him because the convoy is slow. Dong dozes off. He wakes to find the convoy gone and the speedometer at 120 on a mountain road. Xiao Wu's shoulder is hard and bony, his hands are "welded" to the wheel, and he grins at the approaching cliff.
- **The save.** Dong sees the five-emperor coin charm (五帝钱) swinging on the mirror, bought at a temple the day he bought the truck. He rips it off and presses it to Xiao Wu's brow. Xiao Wu goes slack, and the truck skids to a stop at the edge. "Sorry, I fell asleep." Dong knows it isn't that simple.

**Act 2: verification and the expert (5:58–8:45).**
- **Dawn evidence.** At dawn Xiao Wu is truly asleep, and a blue-black mark has appeared on his wrist. Two km on, a truck has gone through the guardrail and its driver is dead. The official cause is "fatigue driving", and the plate is J1574.
- **The phone check.** At the service area Dong phones Xiao Wu's father on the pretext of visiting the uncle's grave. The father says his wife is an only daughter: there is no uncle. Dong covers ("I must have misheard") and realises it wasn't Xiao Wu who lied. It was the thing inside him.
- **The mentor call.** He calls Old Qiu, the trucker who taught him the custom. Qiu pulls over and says this is not a normal 拦车孝. Go now, in daylight, to Ge's funeral-goods shop at the east end of Black Stone town, and say Qiu sent you.
- **The shop.** The shop is dusty, full of paper houses, incense and gold-paper ingots, and an old man of 70+ is folding ingots. He stops at Qiu's name.
- **The examination.** Xiao Wu is carried in. He is heavier than one person, rigid, and his breath is cold. The mark has grown around the wrist "like a slowly crawling snake". Grandpa Ge names it: the fingerprint of a 路游魂, a road-wandering soul. *(The guest stream and the English repost both end here.)*

**Act 3: lore, a refused remedy, a failed remedy (~8:45–~14:10).**
- **The lore.** The 47 km stretch of national road 107 was a post road before 1949, and many people are buried under the roadbed. New crash deaths add more every year. Unburied and unmourned, these souls cannot leave, and each needs a substitute.
- **How the custom is hijacked.** 拦车孝 is real, but sometimes the one blocking the hearse is not alive. A road soul has no body, so it borrows a living one, and it got into the truck when the window was opened. The cloth carries the dead's "last journey" and works as a pass (路引). With it the soul can follow the dead off the road to be reborn, and the borrowed body stays behind to guard the road, which means dying on it. When the mark closes around the wrist, he dies.
- **Remedy 1 (refused).** Another funeral leaves 李家坳 tomorrow on road 107. Block it, return the cloth, and the curse passes to someone else. Dong refuses: Xiao Wu is under 20 and drives to pay for his sick mother's treatment, and he would never accept that. Ge throws Dong out.
- **Remedy 2.** Dong can't get Xiao Wu to swallow congee, weeps, and decides to drive him home so his parents can see him one last time. Ge relents: "you're not a bad man." The second remedy is to become the dead man's godson (认亲), which makes Xiao Wu family of that funeral, so the soul can't touch him.
- **The rite at the bereaved house.** They find the family. The son first thinks they've come to extort money, then agrees ("just burn paper for him at Qingming"). Ge says the son's consent is not enough; the dead man must consent.
  - Xiao Wu's knees won't bend. A slap from a peach-wood sword makes him slump.
  - The incense smoke rises straight.
  - Two copper coins land both-tails three times. On the fourth try the incense stick snaps.
  - Ge bows an apology and leaves.
- **Why it failed.** The spit out of the window offended them: "the dead don't know what's in your heart". The mark is almost closed, and he won't live past tomorrow unless the soul gives up of its own accord, which it never would.

**Act 4: the soul speaks (~14:10–~16:30).**
- **The night drive.** That night Xiao Wu is gone, and so are the keys. He sits at the wheel of the running truck with the doors locked. Dong smashes the window with a brick and climbs in. The coin works for two seconds, then Xiao Wu throttles him one-handed as another cliff approaches.
- **The voice.** A *woman's* voice comes from Xiao Wu's throat: truck drivers all deserve to die.
- **The line that stops her.** Dong croaks: Xiao Wu, your mother is waiting for you to earn her treatment money, so what happens to her if you die? The grip loosens, and Dong crashes the truck into the rock wall instead of the drop.
- **The dream.** Xiao Wu wakes from a dream: a woman flagging down vehicles on the mountain road was hit off the cliff by a big truck, at the very bend where they nearly went over. She carried a green cloth bag.
- **Ge reverses himself.** It never wanted rebirth. It wanted the pass so it could leave its stretch of road and kill truck drivers.

**Act 5: the victim behind the ghost (~16:30–21:33).**
- **The remains.** Below the 100 m drop (an hour's climb through crow-filled woods) lie a skeleton and the green bag: 5,000 yuan in small, long-saved notes, plus an ID card for Zhao Zhi. Twenty km away, her village says she vanished 5 years ago. Her son works far away, came back once, and is missing a hand.
- **The son.** Dong phones the son, Zhou Xiong, who hangs up ("scammer, get lost"). Dong texts a photo of the ID, and Zhou calls back and comes that night.
  - At 20 his right hand was torn off in a factory. In hospital he kept calling for his mother. The hospital said family had been notified, but she never came and never answered.
  - He decided she had run off and abandoned him.
  - Dong hands him the bag and points up at the road where she was hit.
- **The rite.** Ge burns incense, yellow paper and the pass, then rings a bell. Xiao Wu stands, sees Zhou, and the mother speaks through him.
  - She got the hospital's call, took all her savings, got lost in the mountains at night, and was hit while hitchhiking.
  - Mother and son apologise to each other. He bought the red padded coat she once wanted. She asks if the hand still hurts and grips his empty sleeve.
  - Second bell: she says goodbye, and Xiao Wu collapses. Zhou chases the drifting ash, calling "Mom".
- **Coda.** Zhou reburies her on a south-facing slope that looks over the road out of the mountains. He carved the headstone one-handed in three days and burns the red coat at the grave. Xiao Wu wakes with a clean wrist, borrows the phone, and calls his own mother: "it's me, I'm fine, I just missed you."

## 3. Beat table

Times to 8:44 come from the video and its OCR captions. Times marked **~** are estimated (see method). In the mechanic column, the **bold** tag names the genre device.

| Time | Beat | Mechanic | What the viewer believes now | Open loops |
|---|---|---|---|---|
| 0:00–0:07 | Trade taboo in line 1: never overtake a funeral convoy. "Respect" is the official reason, fear of contamination the real one | **Rule list** (rule 1, stated as insider knowledge), official vs real reason | This world has rules; someone will break this one | What happens if you overtake? |
| 0:07–0:25 | Convoy merges ahead; omen inventory (white-flower sedan, hazards, hearse with 奠, coffin glimpsed) | Concrete omen props; something half seen | Atmosphere, no threat yet | Who is in the coffin? |
| 0:25–0:33 | Xiao Wu: "just pass them"; Dong: 亡人上路，生人让道 ("the dead on the road, the living step aside") | Temptation voiced by the viewer proxy; maxim plus **fake authority** (trade lore) | The rule is serious, and Dong is the reliable insider | |
| 0:33–0:41 | 47 km to the next exit; the stretch kills 10+ a year; "following slowly is actually safe" | **Count clue** (47 km, dozen deaths); false safety | Trapped but safe if they obey | Why is this road deadly? |
| 0:42–0:56 | Xiao Wu opens the window, spits, "bad luck"; Dong: never open a window at night; odd face | **Rule broken before it is stated** (rule 2); reaction shot | A minor slip, now scolded | A: did something get in? |
| 0:58–1:10 | A truck overtakes; plate J1574 shown; it stops across the convoy | Rule 1 broken by a stranger; **plant** (plate insert) | Punishment incoming for the stranger | B: what will he do? Plate J1574 |
| 1:12–1:40 | Stiff-legged walk, kneel, three thudding bows, hands raised; hearse opens; cloth corner given | **Ritual template** (step-by-step choreography, a count of three) | The convoy answers rituals, so the supernatural is real | Why stiff? Why the cloth? |
| 1:42–1:58 | Dong names 拦车孝: who may do it (distant kin, someone who owed a favour), the steps, the purpose | **Fake authority + wrong detail.** The explanation is true but incomplete; the missing detail is that the blocker may not be alive. Q&A exposition | False relief: a rational custom, nothing evil | B closed (falsely) |
| 2:00–2:22 | Driving on; Xiao Wu faces away; "did you see the portrait? He looks like my uncle"; "how could you see that far?" | Hidden face; personal-link claim; narrator's logic check | Odd coincidence, probably grief | C: is it really his uncle? |
| 2:24–2:44 | Soft click: seatbelt off, blank face, hand on handle, door pops, red **车门未关** (door open) warning on the dash | Sound cue paid off in 5 s; macro dashboard insert | He is not himself | A reopened |
| 2:46–3:02 | Brake, tyre scream; he jumps, rolls, feels no pain, ignores his name | Wrong-body proof; repetition of non-response | Possessed | |
| 3:04–3:38 | Convoy stops "as if waiting"; same stiff walk, kneel, bows counted "一下两下三下" ("once, twice, three times"), lies flat; **a thin hand gives the cloth from the hearse window** | **Mirror** of the 1:12 template, plus **a deviation** (the dead hand) as the escalation | The ritual is happening to *us* now | D: who handed it over? |
| 3:40–3:52 | Too-neat return: folds cloth, hands on knees, bluish-white face | Uncanny calm; underlit face | Something is wearing Xiao Wu | |
| 3:54–4:12 | "Yes, my mother's cousin… saw the portrait when we *passed* the hearse"; Dong: only child, unsure about the mother's side | **Wrong detail** (they never passed it); false close of C | Plausible but off | C reopened as E: does the uncle exist? |
| 4:18–4:44 | "Let me drive"; Dong agrees ("slow as a snail behind the hearse"); swap; Dong dozes | Dramatic irony; the possessed asks for control. *(udhwkz Part 1 cuts here, ~4:28)* | The viewer screams "don't" | F: what will he do at the wheel? |
| 4:46–5:28 | Convoy gone; speedometer **120** on a mountain road; "oh" without slowing; hard bony shoulder; welded hands; grin; cliff bend; "I'm done for" | **Burner/timer** (speed and distance to the cliff as the countdown); escalation ladder of failed interventions | Death in seconds | |
| 5:30–5:48 | Coin charm swinging on the mirror (temple, the day he bought the truck); rips the string, presses it to the brow; slack hands; skid stop at the edge | **Planted object save.** The coin has hung visibly in POV shots since 1:20 | Saved, and the charm works | Is it over? |
| 5:50–5:56 | "Sorry, I fell asleep" / "I knew it wasn't that simple" | False calm plus narrator doubt | Not over | |
| 5:58–6:10 | Rooster, dawn; truly asleep; a **blue-black mark** on his wrist | Act break; **timer** planted (the mark) | Contaminated | G: what is the mark? |
| 6:12–6:32 | Crash 2 km on: guardrail gone, driver dead, "fatigue driving"; plate **J1574** | **Count/plate clue payoff**; the rule-breaker's fate mirrors Xiao Wu's | Kowtow = death. Xiao Wu kowtowed too | |
| 6:34–6:56 | Calls the father; "his mother is an only daughter, where would an uncle come from?" Dong lies to calm him | **Trusted source contradicted** (outside phone check); narrator conceals | The "uncle" was bait; something lied through him | E closed: no uncle |
| 6:58–7:08 | Warm sunny service area, cold back; "not Xiao Wu: the thing on Xiao Wu lied" | Reframe line; mood contrast | Possession confirmed | H: what is it? |
| 7:10–7:36 | Phone UI "邱哥 通话中" (Brother Qiu, on call); Qiu taught him the custom; engine noise drops as Qiu pulls over; "not a normal 拦车孝"; daylight deadline; address and referral | **Mentor call**; the authority's alarm escalates; **trusted source contradicted** (the custom has a dark variant) | The expert chain is real | |
| 7:38–8:14 | Funeral shop between a hardware and a grain store; paper houses, incense, gold ingots; old man stops folding at Qiu's name | Mundane-wrapped occult threshold; password | Help exists | |
| 8:16–8:44 | Carried in: heavier than one person, rigid, cold breath; mark longer, "like a slowly crawling snake"; 这是路游魂的指印 ("this is the fingerprint of a road-wandering soul") | Examination ladder (each item compared to the morning); **named entity cliffhanger**. *(Guest stream and udhwkz Part 2 end here)* | It has a name; it is serious | H named; G: how long left? |
| ~8:47–9:20 | Lore: road 107, the 47 km stretch, a pre-1949 post road over buried bodies, yearly crashes; unmourned souls need substitutes; the blocker may not be alive; got in through the open window | **Rule-system lore** that pays off three plants (47 km, a dozen deaths, the window) | Xiao Wu was chosen because he broke rule 2 | |
| ~9:21–10:05 | The cloth is a pass (路引) for leaving the road to be reborn; the borrowed body stays to "guard the road" = dies; when the mark circles the wrist, he dies | **Timer** defined (the mark closing) | A clock is running, and the soul just wants out | I: can they break it? |
| ~10:05–11:00 | Remedy 1: block tomorrow's funeral and pass the cloth on. Dong refuses (Xiao Wu is under 20 and funds his sick mother's treatment) | **Moral choice**; the mother motif is planted (it later saves him); danmaku argue Dong chose for Xiao Wu | Dong chose decency over survival | |
| ~11:00–11:40 | Thrown out; congee won't go down; tears; "take him home to see his parents"; Ge relents: remedy 2, 认亲 (become the dead man's godson) | **Reward for virtue** (mentor softens); new hope | There's a clean way out | |
| ~11:40–12:50 | Road back; bereaved village; the son suspects extortion, then agrees; Ge: "the son's yes is useless, the dead must agree" | Social friction beat; a rule inside the rule | The dead man holds the key | J: will the dead man accept? |
| ~12:50–13:35 | Knees won't bend; peach-wood sword; smoke rises straight; coins tails-tails ×3; the incense snaps; Ge bows out | **Count clue** (three refusals, the rule of three); omen escalation | Refused, and they don't know why | K: why refused? |
| ~13:40–14:15 | Dong recalls the spit; "the dead don't know your heart"; the mark nearly closed: "won't live past tomorrow"; only if the soul gives up willingly | Callback to 0:44 (cause found); deadline tightened | Doomed by a careless spit | |
| ~14:20–15:00 | Night: Xiao Wu and the keys gone; at the wheel, doors locked; brick through the window; coin works for only 2 s; choked one-handed; cliff again | **Reversal** of the coin save (the plant now fails); the act-1 set piece repeated at higher stakes | The charm no longer works | |
| ~15:00–15:30 | A woman's voice: "truck drivers all deserve to die"; Dong: "your mother is waiting for you…"; the grip loosens; crash into the rock | **Voice reveal** (gender flip); emotional key turns the lock | The ghost is a woman with a grudge, and the mother line moved her | L: who is she? Why that line? |
| ~15:30–16:20 | Ge: "what did you say to it?"; Xiao Wu wakes: dream of a woman flagging vehicles, hit off the cliff by a big truck at the same bend; Ge: it wanted the pass to roam and kill drivers, not to be reborn | **Trusted source contradicted** (the expert corrects his own lore); dream exposition | Revenge spirit, and a victim | M: find her |
| ~16:25–17:20 | 100 m drop; descent through woods and crows; skeleton; green bag, 5,000 yuan in mixed small notes; ID: Zhao Zhi; village 20 km away: vanished 5 years ago, son missing a hand | Dream detail (green bag) paid in ~30 s; **count** clues (5,000 yuan, 5 years, 20 km) | She was saving money for someone | N: the son |
| ~17:20–17:50 | Calls the son: "scammer, get lost"; photo of the ID; he calls back; silence, sobbing | Comic-real friction; phone-as-proof | The son has lived without knowing | |
| ~17:50–18:30 | His backstory: hand torn off at 20, called for Mom in hospital, she never came, he thought she abandoned him; he gets the bag and the place | **Reversal** (the "abandoning" mother died coming to him); mirror of Xiao Wu (also about 20, also a mother) | The villain is a victim | |
| ~18:30–20:35 | Rite: the pass burned, a bell; the mother speaks through Xiao Wu; the hitchhike explained; mutual apologies; red coat; "does the hand still hurt?" grips the empty sleeve; second bell, farewell, ash chased | Tear-jerk dialogue scene; **mute/recall** inverted (the dead speak once, then go silent) | Grief, not fear | |
| ~20:35–21:33 | Reburial facing the road out; headstone carved one-handed in 3 days; the coat burned; Xiao Wu's wrist clean; he calls his own mother | Bookend; the motif closes on the companion | Resolved, warm ending | None |

## 4. Clue chain (plant → payoff)

| # | Plant (time) | Payoff (time) | Notes |
|---|---|---|---|
| 1 | Rule 1: never overtake a hearse (0:00) | J1574 overtakes (0:58) → dead in a crash, "fatigue driving" (6:14–6:28) | The stranger previews Xiao Wu's fate. The plate is shown twice so the viewer can match it. |
| 2 | Rule 2: never open a window at night (0:52), broken *before* it is stated (0:44) | Ge: the soul can't get into a closed cab, so it entered through the window (~9:15). The spit also explains the failed 认亲 (~13:45) | One careless act pays off twice, as both the mechanism and the motive. |
| 3 | "This stretch kills a dozen a year" (0:38) | The road-107 lore: buried post road, yearly crashes, souls needing substitutes (~8:50) | A throwaway statistic becomes the world's rule. |
| 4 | 47 km to the next exit (0:34) | The cursed stretch is 47 km, from 李家坳 to 王家屯 (~8:52); the soul's range limit (~16:15) | The number marks the boundary of the curse. |
| 5 | Stiff walk, knees don't bend (1:16, 3:12) | Xiao Wu's knees won't bend at the shrine; a peach-wood sword fixes it (~13:00) | Body tell used three times. |
| 6 | Three bows (1:22, 3:24) | Coin toss three times, three refusals (~13:20); the second bell is the farewell (~20:00) | Rule of three: a count the viewer can follow. |
| 7 | 拦车孝 eligibility: distant kin or someone who owed a favour (1:46) | The "uncle" claim (2:16) is the possession's cover story, falsified by the father (6:48); the 认亲 remedy uses the same kinship logic (~11:40) | The custom's own rules are both the trap and the cure. |
| 8 | "Saw the portrait when we *passed* the hearse" (4:02); "how could you see that far?" (2:20) | They never passed it; the information came from elsewhere | A rewarded close watch. |
| 9 | Five-emperor coin swinging in POV shots (visible from about 1:20, again at 4:20) | Save at the cliff (5:30–5:42) → fails after 2 s in the act-4 repeat (~14:51) | Planted visually, cashed in once, then reversed to raise the stakes. |
| 10 | Blue-black mark (6:06) | Longer, "like a snake" (8:36) → nearly closed, "won't live past tomorrow" (~14:04) → clean (~21:08) | A visible timer drawn on the body. |
| 11 | Thin, dry hand passes the cloth from the hearse window (3:30) | Never explained. Ambient dread: the dead themselves endorse the transfer | Deliberately unpaid image. |
| 12 | Old Qiu "taught me the custom" (7:12) | Qiu sends him to Ge (7:30) | Mentor chain, giving the expert legitimacy. |
| 13 | Xiao Wu: under 20, driving to fund his sick mother's treatment (~10:50, the refusal speech) | Dong's choked line about his mother stops the ghost (~15:19); Zhou Xiong was also 20 and also lost his mother (~17:55); Xiao Wu's closing call to his mother (~21:20) | **The thematic spine.** Planted inside a moral choice, so it reads as character, not as a clue. |
| 14 | "Truck drivers all deserve to die" in a woman's voice (~15:12) | She was hit by a big truck while hitchhiking (~16:05, ~19:10) | Explains why the ghost targets truckers and why it hijacks 拦车, "blocking vehicles", the act that killed her. |
| 15 | Green cloth bag in Xiao Wu's dream (~16:20) | Found under a rock with 5,000 yuan (~16:57) | Short-range plant (~30 s). |
| 16 | Son "missing a hand" (~17:15) | "Does that hand still hurt?"; she grips the empty sleeve (~20:12) | The emotional peak hangs on a physical detail. |
| 17 | Official cause "fatigue driving" (6:22) and Xiao Wu's "I fell asleep" (5:54) | Mirrored excuses; the truth is possession | A mundane explanation hides the supernatural one. |

## 5. Twist inventory

| # | Time | Twist | Type | Setup |
|---|---|---|---|---|
| 1 | 3:04–3:38 | The companion performs the stranger's ritual | **Mirror** (the template happens to an insider) | The 1:12 ritual is shown in full and then explained, so the repeat is legible beat for beat. |
| 2 | 3:28–3:32 | The cloth comes from a *hand in the window*, not from a living driver at the door | **Template deviation** | The viewer has memorised the template; changing one step is the escalation. |
| 3 | 6:28 | The man who overtook the hearse is dead | **Rule-breaker punished / foreshadow mirror** | Plate shown twice at 1:04–1:06. "Fatigue driving" mirrors "I fell asleep". |
| 4 | 6:48 | There is no uncle | **Trusted source contradicted** (family phone check) | Only-child doubt at 4:10; the "passed the hearse" slip at 4:02. |
| 5 | 8:44 → ~9:00 | 拦车孝 is real, but the blocker can be a borrowed body | **Fake authority + wrong detail** (Dong's explanation was right but incomplete) | Dong hedged "it's my first time seeing it" (1:44). Qiu: "not a normal one". |
| 6 | ~13:30 | The kinship rite fails: the dead refuse | **Remedy reversal** (hope crushed by an omen count) | The rule that the dead must agree is stated just before. |
| 7 | ~13:45 | The cause was the spit | **Small sin, big consequence** | Shown at 0:44 and scolded at 0:52. |
| 8 | ~14:51 | The coin no longer works | **Tool reversal** | The same object saved them at 5:40. |
| 9 | ~15:10 | The ghost is a woman who hates truck drivers | **Voice/identity reveal** | The road-death lore and the trucker frame. |
| 10 | ~16:12 | It never wanted rebirth; it wanted to roam and kill | **Motive reversal**, the expert correcting himself | The "pass" lore at ~9:30 gave the benign reading first. |
| 11 | ~17:50–19:20 | The killer-ghost is a mother who died rushing to her injured son, who believed she abandoned him | **Villain-to-victim reversal** (horror → tearjerker) | The money bag, "missing a hand", and the mother line that loosened her grip. |
| 12 | ~15:19 (paid ~19:00) | What saved Dong was empathy, not an exorcism tool | **Resolution by recognition** | Planted in the refusal speech (~10:50). Danmaku at 18:05 spell the connection out. |

The twist chain's shape: **mechanical horror (acts 1–2) → expert lore and failed remedies (act 3) → identity reveal (act 4) → melodrama (act 5).** The opening danmaku warn repeat viewers: 省流：好结局 / 结尾有刀 ("TL;DR: happy ending" / "the ending stabs you"). The Chinese audience treats the tearjerker turn as the payoff, and danmaku density peaks again at 18:24–20:32 (泪目, "tears"). The English repost never reached that half.

## 6. GENERIC vs SPECIFIC

### Generic: genre conventions anyone can use

- **Frame.** An insider trade rule in line 1 ("every [trade] knows you never…"), with an official reason and then the real, fearful one.
- **A second rule broken before it is stated.** The viewer sees the slip, then learns it was one.
- **A stranger breaks the big rule first** and later dies. Their fate previews the protagonist's.
- **The ritual template, then its mirror.** Show a stranger's uncanny ritual in full, explain it rationally, then make a trusted companion perform it beat for beat with one step changed.
- **Possession tells:**
  - stiff gait
  - non-response to their name
  - no pain
  - too-neat posture
  - underlit pale face
  - grin at danger
  - wrong voice
- **Companion's backstory falsified by an outside phone call** to a family member, while the narrator hides his fear.
- **Body-mark timer** that grows between scenes until it "closes".
- **Mentor chain.** A colleague refers the narrator to an old folk expert in a mundane-looking shop, with a daylight deadline and a referral password.
- **Two remedies.** A selfish one (pass the curse on) that the hero refuses, and a clean one that fails because of the earlier small sin.
- **Planted protective object.** It saves the hero once and fails the second time.
- **Revenge ghost turned sympathetic victim**, laid to rest by reuniting it with family and returning its belongings.
- **Bookend.** The companion survives and makes a small gesture that echoes the theme.
- **Number clues** (distance, death toll, count of three) that later turn out to be the rules of the world.

### Specific: this author's expression, which a transposed story must NOT reuse

- **Premise core.** The 拦车孝 custom itself as the hook: kowtowing to a hearse for a strip of coffin cloth, and the cloth as a 路引 (pass) out of the road. Don't use a funeral-convoy/hearse taboo + cloth-token story at all. This is the studio's (and the web-fiction text's) signature.
- **Names and places:** 冬哥/张东东 (Dong), 小武 (Xiao Wu), 老邱 (Old Qiu), 葛爷 (Grandpa Ge) and 葛记殡葬铺子 (Ge's funeral shop), 黑石镇 (Black Stone town), 107国道 with the 47 km stretch from 李家坳 to 王家屯, 赵芷 (Zhao Zhi), 周雄 (Zhou Xiong).
- **Exact clue combination:**
  - plate J1574
  - 47 km and a dozen deaths a year
  - a window spit as the entry point
  - "saw the portrait when we passed the hearse"
  - only child plus "mother is an only daughter"
  - the five-emperor coin on the mirror pressed to the brow
  - the 120 speedometer at the cliff bend
  - a blue-black wrist mark circling like a snake
- **Exact twist chain:** stranger's ritual → companion mirrors it → stranger dead by plate → no uncle → road soul → refused transfer remedy → failed godson rite (coins tails ×3, incense snaps) → woman's voice hating truck drivers → dream of a hitchhiker hit by a truck → skeleton with a green bag of 5,000 yuan → one-handed son who thought he was abandoned → red padded coat → empty sleeve → one-handed headstone.
- **Distinctive lines** (do not echo them in translation either):
  - 亡人上路，生人让道 ("the dead on the road, the living step aside")
  - "like a devout believer"
  - "like a slowly crawling snake"
  - "not Xiao Wu: the thing on Xiao Wu lied"
  - "truck drivers all deserve to die"
  - "does that hand still hurt?"
  - "I just missed you"
- **Set-piece choreography.** The kneel, three thuds, hands-raised begging pose, the cloth corner torn and handed over, the cloth folded twice into the pocket, hands placed on the knees.

**Transposition guidance (mechanics only).** Keep the "insider rule → stranger breaks it → companion mirrors it → outside check falsifies → expert names it → timer → remedy reversal" skeleton. Invent a new trade, a new custom or protocol, a new token, new tells and a new victim backstory, and run the originality gate against `research/corpus/`. Our lane's strength would be English-native settings: long-haul or rideshare night shifts, hospital transport, ferry crossings, a cemetery groundskeeper. None of them should use a hearse or a cloth token.

## 7. Pacing

- **Text density.**
  - About **356 Chinese characters per minute** over the whole 21:33 (7,664 Han characters in the full text). It is about 366 in the first 8:45.
  - The plain reading of the same text runs at about 259/min, so the animation is **~1.37× faster** and drops some aside lines.
  - The udhwkz English dub runs at about 364 wpm and compresses the source by about 0.75× on top of that (4:28 of source → 3:22 of repost).
- **Caption cards.** One short line per card, typically 4–15 characters, white, bottom centre. From the 2 fps OCR of 0:00–0:40: **~45 cards/min, mean 1.5 s per card** (range 0.5–3 s). Dialogue fragments get 0.5–1 s cards (冬哥, 超过去啊, 亡人上路 / 生人让道). Lines are split at the clause so the captions keep pace with cuts every 2–3 s.
- **Re-hook interval.**
  - In 0:00–8:44, a new threat, reveal or question lands about every **8–10 s**: median 8 s on the matching English cut, longest gap about 24 s during the 1:42–2:12 explanation and lull.
  - In the second half, the gaps stretch to 20–40 s in the expert-lore stretch (~8:47–10:05) and in the shop/village dialogue. Each stretch still ends on a hook (the death clock, "a remedy, but it's vicious", "the dead must agree", "won't live past tomorrow").
- **Act lengths (share of 21:33).**

  | Act | Range | Share |
  |---|---|---|
  | Rules + mirror + cliff | 0:00–5:58 | 28% |
  | Evidence + expert | 5:58–8:45 | 13% |
  | Lore + two remedies | ~8:45–~14:15 | 25% |
  | Night attack + voice + dream | ~14:15–~16:25 | 10% |
  | Victim + reunion + coda | ~16:25–21:33 | 24% |

  The horror is front-loaded. The back quarter is melodrama.
- **Set-piece rhythm.** The cliff-car set piece happens twice (4:46–5:48 and ~14:20–15:30). Each runs about 60–70 s with a near-death count and a last-second save.
- **Part breaks / cliffhangers.**
  - The source is one long part with no part-2 card, but it has natural cut points that close one loop and open a bigger one:
    - 4:28 "let him drive"
    - 5:56 "not that simple"
    - 6:28 the J1574 plate
    - 8:44 the entity named
    - ~13:35 the incense snaps
    - ~15:12 the woman's voice
    - ~16:12 the motive reversal
  - The reposter used the first two big ones (4:28 and 8:44) as Part 1 and Part 2 endings and posted Part 2 nine seconds before Part 1 (see the repost files).
  - The 8:44 cut also coincides with Bilibili's logged-out trial length, so the repost likely stopped there because that was all it had.
- **Danmaku heat map** (178 comments, as a proxy for engagement):
  - Clusters at 0:00–0:35 (repeat viewers posting "good ending / the ending stabs").
  - 5:02–5:57 (the cliff save, about 30 comments: "pull the handbrake", "summon the soul-whip from the other channel", "what truck stops from 120?").
  - 8:46–8:59 (the entity named; locals: "road 107 is outside my house").
  - ~11:00–11:10 (arguing about the refusal).
  - 18:24–20:32 (tears).
  - Many comments cross-reference another studio's trucker horror (老D悬疑, its hero 龙长栋 and his 打魂鞭 "soul-striking whip"), so the trucker-taboo sub-genre is shared and competitive in China.

## 8. Visual vocabulary

From `sheet.jpg` (0:00–8:45) and the frame OCR. Details of the second half are inferred from the text and danmaku.

- **Format.** 16:9, 1080p master. Static or slow-pan 2D shots with frequent punch-ins, a cut every ~2–3 s. Burned white captions, single line, bottom centre. No on-screen title card or branding at the open.
- **Characters.** White round-faced stick figures with thick black outlines and dark tufted hair. Simple coloured shirts carry identity: Dong in blue, Xiao Wu in brown/khaki. Grandpa Ge is grey-haired in a beige robe. Qiu is seen in a red tractor or truck cab on the phone.
- **Expressions:**
  - neutral dot eyes
  - **dread shading** (a grey gradient over the upper face)
  - blank stare
  - creepy grin with teeth
  - red-faced strain with red anger marks
  - pale apology
  - eyes closed, sleeping, head tilted, mouth open
  - old man's frown
- **Backgrounds.** Painterly semi-realistic photobash, desaturated blue-grey night. The scenes are:
  - truck cab interior, as a two-shot from outside the windshield, a POV over the dash, or a passenger close-up
  - misty mountain highway and guardrail
  - black sedan with a white chrysanthemum bow
  - small hearse with **奠** on the rear glass
  - coffin under a white cloth
  - J1574 truck rear
  - crash scene with an ambulance and broken guardrail
  - dawn service area with parked trucks
  - rural courtyard (the father's phone cutaway)
  - rural shop street; the funeral-goods shop interior (paper houses, paper horses, incense bundles, gold ingots)
- **Inserts and overlays** (macro "evidence" cards):
  - plate **J1574** (twice)
  - red dashboard pictogram **车门未关** ("door not closed")
  - speedometer needle at **120** with red warning lights
  - five-emperor coin with a red tassel swinging from the mirror (a recurring foreground element in POV shots)
  - wrist mark close-ups
  - circular insets (EXIT 47 km sign; mirror or rear-view memory)
  - red motion marks; camera shake on impacts; tyre-smoke skid
- **Phone UI.** Minimal. One call screen at 7:10: contact **邱哥**, label **通话中** ("on call"), battery 100%. The father call is shown as a split cutaway, not a UI. The later calls to Zhou Xiong (a hang-up, a photo of the ID sent) are probably similar.
  - **No group chat, SMS thread, danmaku overlay or rule-list card.** The rules are spoken in narration.
  - This is the folk-taboo register, unlike the group-chat stories in the corpus. For our kit it means a "rules-horror" episode can work with zero chat UI, provided the rules are stated in line 1 and recur as counted callbacks.
