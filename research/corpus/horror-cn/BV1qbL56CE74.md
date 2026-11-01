# 磨牙怪 (the teeth-grinding monster): source study

Internal research only. This is a structural teardown of one Chinese source story so we can learn the genre. **Do not translate, retell or remix this story for publication.** Section 6 lists what we may borrow (genre conventions) and what we must not (this author's specific expression).

## 1. Header

| Field | Value |
|---|---|
| Listed source | https://www.bilibili.com/video/BV1qbL56CE74, 【怪物悬疑七部曲】 ("Monster suspense, seven parts"), compilation uploaded 2026-05-16 |
| Channel | 杰出影视本人 (Bilibili mid 75872737), the studio behind the 迷雾 / "Chen Jie" repost ecosystem (see `SOURCES.md`) |
| Views | 41,782 Bilibili plays for the whole 68-min compilation (4,083 s). There is no standalone count: the single episode is still missing from the space listing and from Bilibili search ("磨牙怪" returns only this compilation). |
| Chapter in the Bilibili compilation | 磨牙怪 runs 40:39 to 48:26 (2439 to 2906 s, 467 s). Chapters in order: 吸血鬼, 智尸, 伪人, 人尸, **磨牙怪**, 寄生虫, 高温虫. |
| Copy actually analysed | Bilibili gives logged-out users only a 605 s preview of this compilation (playurl `timelength` 4083242, but `durl` length 604992, with or without `try_look`, dash or html5 parameters). So the text comes from the same studio's footage re-uploaded to YouTube: **沸點漫研社 `72uYkNKfjXo`**, 【MULTI SUB】末日动画《末日十部曲》. That upload is 2025-08-19, 7,649 s long, with 26.0K views, and its description says it is licensed. Its title is this story's hook line. The story runs **19:26 to 27:35 (1166 to 1655 s, 489 s)**. It has the same yellow-jacket hero ("小杰") and the same art. It is 22 s longer than the Bilibili chapter, probably a slightly different cut. |
| Story duration | 8:09 from the first line to 全剧终 ("the end") |
| First known date | The standalone 杰出影视 episode predates 2025-08-19, the date of the 沸點漫研社 re-upload. |
| English repost evidence | **Confirmed** (previously "probable"). The lehwh7 YouTube copy [tP5JPBvdMzg](https://www.youtube.com/watch?v=tP5JPBvdMzg), "TEETH GRINDING MONSTER #chenjie", 2026-07-12, 586 s, has 21.8K views. Its English auto-transcript follows the Chinese beat for beat: same helper handle ("Time Hunter"), phone in a potted plant, silver needle, braised rabbit, jade pendant vs brooch, Uncle Wang in 503. The lehwh7 TikTok post 7659482056656735521 has **1.9M** views and 143K likes (2026-07-06, 9:45 per R2). A copy by StoriesDaily, `piVAsr5G32M` (586 s), has 27 views. The English TTS version runs about 20% longer than the Chinese (586 s vs 489 s) at about 255 words per minute. |
| Files on the Spark | `~/studio/refs/horror-cn/BV1qbL56CE74/`. **Chinese text:** `captions_ocr.txt` (raw burned-in captions OCR'd at 1 fps), `captions_clean.txt` (353 deduped lines), `whisper_zh_small.tsv` (faster-whisper small, zh, CPU, 4 threads; matches the captions). **Phone chat screens:** `ui_ocr.txt` (OCR of the chat UI). **English repost:** `en_repost.txt`. **Video:** `yt72.mp4` (480p source), `seg.mp4` and `seg.wav` (the story only, from 1160 s), `frames/` (1 fps). **Bilibili extras:** `full.danmaku.xml` (only 6 danmaku in the chapter). |

Timestamps below are **story clock** (0:00 is the first line). To convert: YouTube `72uYkNKfjXo` = story clock + 19:26. The Bilibili compilation is roughly story clock + 40:39, but it drifts by up to about 20 s.

## 2. Story outline (own summary)

A teenage boy is spending the summer at his grandfather's flat, a month after his grandmother died. For three nights, at 2 a.m., something grinds its teeth outside his bedroom door, and the sound stops whenever he opens the door. He asks for help online. A stranger with a hunter-style handle DMs him. The stranger says it is a teeth-grinding monster: it sharpens its teeth for seven days, then eats its victim inside a dream, then moves on to the rest of humanity. The stranger tells him to film it secretly. The boy hides his phone in a plant pot, but falls into a sudden deep sleep and the footage shows an empty room. The helper says the monster dodged the camera and is disguised as someone close to him.

That leaves two suspects. His father, who hates the heat and never visits the un-air-conditioned flat, suddenly announces he is coming. The grandfather pulls the boy aside: "your father has no shadow". He sends the boy to a neighbour, Uncle Wang, who gives him a protective jade pendant and agrees the father is "no longer human". The helper supplies a test: prick the neck with a silver needle, red blood means human, black means monster. Then the father privately accuses the grandfather. The old man never eats rabbit, but today he finished the braised rabbit. The father dreamed of the boy being chased by the grandfather. He gives the boy a brooch to keep on him. The boy trusts no one and throws the brooch on the floor.

The needle test fails: the grandfather wakes up, and the father is still awake on his phone. The boy plants the phone again and instantly falls asleep. He "wakes" to a black head emerging from his father's room, the grandfather sees nothing, and the head whispers from the ceiling. He wakes again: it was a dream. This time the footage shows the monster. The helper says to look for a distinguishing mark. The monster has a scar on the back of its hand. So does the father, who says he cut himself five days ago, the night the grinding began. The father insists they must leave and says he heard the grandfather making clacking noises at night. Then the grandfather finishes the rabbit again, though his beloved pet was a rabbit.

Nights blur into nested dreams. The jade pendant heats up and repels the monster once, then fails. The clock reads 4 a.m., then "2 a.m." on the next waking, which is impossible. The boy sees his father eating the neighbour's dog. He punches himself and still cannot tell if he is awake. His father tackles him at Uncle Wang's door. Each time he wakes, the jade has cracked further and is finally split in two. The discarded brooch is cracked too. The helper finally replies: throw away the brooch (a "soul lock"), keep Wang's jade, bury the brooch. The narration says the boy buries it and goes to sleep as told. In the dream the monster lunges, bounces off, and is told it was fooled. The boy buried the jade, not the brooch, because the helper knew who gave him the jade, and he never said. The helper was the monster. So the brooch is real, the father is innocent, and the grandfather is the monster.

He wakes for real. The grandfather-monster is pinned in a glowing circle. The father reveals he works for a supernatural-incident agency, has been tracking these creatures for a month, and came to protect his son. The thrown brooch burns the monster to charcoal. Coda: they go next door and kill Uncle Wang, who was also a monster, and set off to save the world.

Short analysis quotes (at most 15 words each):
- The rule/timer line: "这个过程大概持续七天，等七天后它会在梦境里吃掉你" ("the process takes about seven days; after seven days it eats you in your dream").
- The deduction line: "我从没告诉他玉佩是谁给的" ("I never told him who gave me the jade").

## 3. Beat table

| Story clock | Beat | Mechanic | What the viewer believes now | Open loops |
|---|---|---|---|---|
| 0:00 | Cold open: 2 a.m. grinding outside the door, gone whenever he opens it, 3 nights running | Fixed-hour phenomenon; "only when you don't look" rule | Something is stalking him | What is it? Why does it vanish? |
| 0:06 | Online stranger "猎人" DMs: it's a teeth-grinding monster, humanity is doomed | **Fake authority** (anonymous online expert); phone chat UI | A knowledgeable ally has appeared | Is the stranger credible? |
| 0:18 | Rule set: grinds for 7 days, then eats you in a dream, then everyone | **Rule list + countdown timer** (day 3 of 7) | Hard deadline, about 4 days left | Can it be stopped? |
| 0:36 | "Film it secretly": phone hidden in a plant pot; at 2 a.m. he blacks out; footage empty | Proof attempt fails; unnatural sleep | Maybe the helper is a liar ("你这个骗子" / "you liar") | Why the sudden sleep? |
| 0:57 | Helper: it saw the camera, and **it is disguised as someone close to you** | Escalation from external to internal threat | Someone in the house is the monster | Who? |
| 1:05 | Setup: summer at grandpa's, grandma died a month ago; grandpa's door was ajar last night | Suspect 1 planted with circumstantial clue | Grandpa is suspicious | Grandma's death? |
| 1:15 | Dad calls: arriving today, though he hates the heat and never visits | Suspect 2 planted with behaviour-break clue | Dad is suspicious too | Why is Dad coming now? |
| 1:25 | Grandpa privately: "your dad has no shadow"; go to Uncle Wang, 503 | **Accusation from suspect 1**; secondary authority | Dad is the monster? | Shadow never verified on screen |
| 1:40 | Wang gives jade pendant, agrees Dad "is no longer human" | **Corroborating authority** + protective token #1 | Two adults say Dad is the monster | Wang's role |
| 1:53 | Helper: silver-needle test (red = human, black = monster); do it while they sleep; real Dad probably eaten | Test procedure (a rule the hero can execute) | Tension: Dad may already be dead | Will the test happen? |
| 2:18 | Dad privately: grandpa never eats rabbit but ate all of it; Dad dreamed grandpa chasing the son; gives brooch | **Mirror accusation**; protective token #2 | Now both suspects accuse each other | Which token is real? |
| 2:42 | Hero throws the brooch on the floor; "trust no one"; plans the needle test before 2 a.m. | Hero agency + self-imposed deadline | Hero is paranoid and neutral | Brooch left on the floor (planted) |
| 2:53 | Needle at grandpa's neck; grandpa wakes; flimsy excuse; Dad still awake | Near-miss suspense; test denied | Grandpa may be onto him | Test still unresolved |
| 3:10 | Plant pot again; instant sleep; "dinner!"; black head from Dad's room; grandpa sees nothing; head on the ceiling: "looking for me?" | **Jump scare + dream reveal #1** | Dad's room is the source → Dad is the monster | Was it a dream or a warning? |
| 3:47 | Footage now shows the monster grinding, identical to the dream | **Reversal**: the "liar" was right | Helper is trustworthy | — |
| 3:57 | Helper asks for his address and the needle result, then suggests matching a "special mark" | Trusted source steers the investigation | Helper is a guide | Why does he want the address? (planted) |
| 4:16 | Monster has a scar on the back of its hand; Dad has the same scar, "cut 5 days ago", the day the grinding began | **Count clue / date match** (misdirection) | Dad is almost certainly the monster | Grandpa's hands? |
| 4:33 | Dad: "we must leave"; he heard grandpa clacking at night | Counter-accusation 2 | Viewer split | Who is lying? |
| 4:42 | Grandpa has no scar; but eats all the rabbit again, though his dead pet was a rabbit | Contradictory evidence stack | Scar says Dad, rabbit says grandpa | Viewer must weigh clues |
| 5:00 | Dream: jade heats up and repels the monster; wakes at 4 a.m.; jade cracked | Token "proven" | Jade (Wang) is protective → trust the Wang/helper side | Why cracked? |
| 5:18 | Jade fails; wakes at "2 a.m." (but it was 4); monster at the door; wakes: dream within a dream; day 7; helper silent | **Clock-contradiction clue**; nested dream; timer expires tonight | He is trapped; time is up | Is he awake now? |
| 5:45 | Grandpa: "Dad's in the kitchen"; Dad eating the neighbour's dog: "found out" → lunge → wakes (dream^3) | Gross-out image; suspect-2 framing | Dad is the monster (third time shown) | Viewer distrusts every scene |
| 6:05 | Sunlight unreal; punches himself, but pain could be dreamt; runs to Wang; Dad tackles him; wakes at 4 a.m. | Reality-check failure (loop) | No escape | — |
| 6:21 | Jade split in two; the discarded brooch is cracked too | Token damage as clue (both "fought") | Both tokens absorbed attacks | Which one protected him? |
| 6:27 | Helper finally replies: brooch = soul lock, throw it away; jade = protection; bury the brooch | **Trusted source issues a fatal instruction** | Relief: rescue instructions | — |
| 6:40 | Narration: he buries the brooch and reports "done"; helper: "go to sleep, leave the rest to me" | **Narrator withholds** (states the opposite of the true action) | Hero complied | "Leave the rest to me" is ominous |
| 6:49 | Dream: "mealtime" lunge, monster repelled; "look what this is": he buried the jade, not the brooch | **Reversal via a switched object** | Hero outplayed the monster | Why did he suspect? |
| 7:01 | Deduction: never told the helper who gave the jade, yet the helper named Wang → helper = monster; brooch real → Dad innocent → **grandpa is the monster** | **Knowledge-leak tell**; trusted source contradicted; double identity reversal | Everything re-sorts | Who is Dad really? |
| 7:18 | Wakes for real; grandpa-monster pinned in a magic circle; Dad: supernatural-incident agency, tracking them for a month, came to protect him | Hidden-protector reveal | Dad is a hero | Grandma's death (month) = implied first victim |
| 7:43 | Brooch thrown, fire, 10 min later charcoal | Token pays off as a weapon | Threat ended | Invasion is "large scale" |
| 7:53 | "Uncle Wang must be one too (he gave the jade)"; kill him "for practice"; set off to save the world; 全剧终 | **Coda kill + franchise tag** | Satisfying cleanup | Sequel hook (more of them) |

## 4. Clue chain

| Clue (planted at) | Points to (surface reading) | Pays off at | True meaning |
|---|---|---|---|
| Sound vanishes when he opens the door (0:00) | Something shy outside | 0:44 helper explanation | It hides when watched; motivates the hidden camera |
| Helper's 7-day / eaten-in-a-dream rule (0:18) | Helper is an expert | 5:47 "day 7, tonight it eats me"; 6:05 "trapping me in dreams" | Truthful lore used to buy credibility (the liar tells mostly truth) |
| Sudden blackout at 2 a.m. (0:53, 3:20) | Monster's power | 3:47 dream; 5:18 nested dreams | The dream-eating mechanism is already running |
| Grandma died a month ago (1:08) | Background grief | 7:36 Dad: agency found the monsters "a month ago" | Implies grandpa was replaced or grandma eaten (never stated) |
| Grandpa's door ajar the night of filming (1:12) | Grandpa was up | Never verbally paid; consistent with 7:01 | Genuine clue toward grandpa |
| Dad never visits, hates heat (1:15) | Dad acting out of character | 7:38 | He came on a mission, not as an impostor |
| "Dad has no shadow" (1:32) | Dad is inhuman | Never shown; dissolved by 7:01 | A lie by the real monster (unverified-claim device) |
| Wang: "your dad is no longer human" + jade (1:40) | Corroboration | 7:01 helper knew it was Wang's jade; 7:53 Wang is a monster | Coordinated lie from a second monster |
| Silver-needle test (1:53) | A fair test | 2:53 denied | Never completed; keeps suspicion open; in hindsight a ploy to make the boy attack a sleeping relative |
| Rabbit meat: grandpa "never eats rabbit" (2:23) | Grandpa is off | 4:42 again; dead pet rabbit (4:55) | Genuine clue (from the innocent party) |
| Dad's dream of grandpa chasing the son (2:31) | Dad's motive | 7:38 | True premonition / agent intel |
| Brooch thrown on the floor (2:42) | Hero rejects Dad's gift | 6:21 cracked; 6:49 repels monster; 7:43 weapon | Real protection worked even from the floor. This is the key plant. |
| Helper asks for his address (3:57) | Help is coming | Not explicitly paid off | Monster probing (dangling, ominous) |
| Helper's "special mark" method (4:00) | Investigation tool | 4:16 scar on Dad | Misdirection engineered by the helper |
| Scar on Dad, 5 days old = grinding start (4:16) | Dad is the monster | **Never explained** | Red herring (a coincidence the story leaves hanging) |
| Dad: grandpa clacks his teeth at night (4:33) | Counter-accusation | 7:01 | True |
| Jade heats and repels the monster (5:00) | Jade protects | 6:21 split; 6:49 inverted | Staged or false (left unexplained) |
| Clock reads 2 a.m. after waking at 4 a.m. (5:18) | Something is wrong | 5:24 "dream within a dream" | Fair-play tell for the nested dream |
| Helper silent on day 7 (5:40) | Helper busy | 6:27 replies at the critical moment | The monster times its instruction |
| Helper names "Wang's jade" (6:33) | Helpful detail | **7:01 deduction** | Knowledge leak: the helper is the monster |
| Narration "I buried the brooch" (6:40) | Compliance | 6:49 | Unreliable narration (switched object) |

## 5. Twist inventory

| # | Twist | Type | Setup |
|---|---|---|---|
| 1 | The camera footage is empty | Proof-denied reversal | The "only when unobserved" rule at 0:00 |
| 2 | The monster is disguised as someone close | Threat moves indoors | Grandma's death, two relatives in the house |
| 3 | Each suspect privately accuses the other, each with a gift-token | Mirror-accusation whodunit | Two invitations to trust (grandpa → Wang → jade; Dad → brooch) |
| 4 | The black head in Dad's room was a dream | False awakening, jump-scare variety | The unnatural sleep rule |
| 5 | The second footage shows the monster: the "liar" was right | Credibility reversal (raises trust in the helper right before he betrays) | Twist 1 |
| 6 | Dad has the monster's scar, dated to day one | Misdirection via count/date match | The helper's "mark" method |
| 7 | Dream within a dream within a dream | Nested-reality escalation | Clock contradiction (4 a.m. → 2 a.m.), the dream-eating rule |
| 8 | The online helper is the monster | Trusted source contradicted (knowledge-leak tell) | The helper "knows" who gave the jade; the boy never said |
| 9 | He buried the other token | Withheld action / unreliable narration | The brooch left on the floor; both tokens cracked |
| 10 | Grandpa is the monster; Dad is a supernatural agent | Double identity reversal (accused ↔ accuser) | Rabbit clue, the night clacking, the month timeline, the out-of-character visit |
| 11 | The helpful neighbour is also a monster | Coda twist / franchise tag | He supplied the jade and endorsed the lie |

## 6. GENERIC vs SPECIFIC

**GENERIC (genre conventions, free to use in a transposed original):**
- A night phenomenon at a fixed hour that stops when observed.
- An anonymous online helper who explains the rules (forum, DM, group chat). Later revealed as the antagonist, exposed by knowing something they could not know.
- A countdown in days before the creature "completes" and kills.
- Secretly recording with a hidden phone; footage that is empty, then later shows the thing.
- "It's disguised as someone close to you" → two-suspect household whodunit. Each suspect privately accuses the other.
- Two protective objects from the two sides; one is real, one is a trap. The hero must choose.
- A physical test to tell human from monster (blood, reflection, mark, question).
- A distinguishing mark seen on the creature and matched on a person, as a red herring.
- False awakenings and nested dreams, exposed by an impossible clock time. Pain is no proof of waking.
- The narrator hides a switched action until the reveal.
- The "innocent suspect is secretly a hunter/agent" reveal. A coda where the hero and ally take out the second impostor and go on to fight more.
- Fear-spike interjection lines ("my heart stopped") roughly every 20 to 30 s.

**SPECIFIC (this author's expression, must NOT reuse):**
- The monster concept itself: a creature that grinds/sharpens its teeth outside the door for 7 days, then eats you in a dream. That means no teeth-grinding monster in any form.
- The helper's handle 时空猎人 / "Time Hunter".
- The cast trio: grandfather + father + Uncle Wang in flat 503, with a grandmother dead a month, at a summer stay at grandpa's flat without air-conditioning.
- The paired tokens **jade pendant (neighbour) vs brooch (father)**, and the buried-the-other-one switch.
- The silver needle with red vs black blood.
- The scar on the back of the hand, "cut 5 days ago".
- Braised rabbit + grandpa's dead pet rabbit; "no shadow".
- Father eating the neighbour's dog in the kitchen.
- Phone hidden in a plant pot.
- The 2 a.m. / 4 a.m. clock pair.
- The "supernatural incident bureau" father; the brooch that sets the monster on fire for 10 minutes until it is charcoal.
- The exact twist chain: helper betrays → buried-token switch → accuser is the monster → neighbour coda.
- Distinctive lines: the ceiling whisper "你是在找我吗", the "mealtime" line "用餐时间到了", "蠢货 / 你看这是什么", "正好给你练练手".

A transposed story should keep at most two or three generic mechanics from this list. It should change the creature, the warning channel's identity and the token logic, so that no clue in it is the same clue in new clothes.

## 7. Pacing

- **Density:** 353 deduped caption lines in 8:09 = **43 caption lines/min**, about one line every 1.4 s. About 3,200 Chinese characters = **about 393 chars/min** (6.5 per second). That is 9.1 characters per line on average, all single-line captions.
- **Narration:** whisper finds speech covering essentially the whole runtime, wall to wall, with no silent beats. Dialogue and narration come in one VO register. Chat messages are read aloud in full while the chat screen is on screen.
- **English repost pacing:** about 2,500 words in 9:46 = **about 255 wpm** TTS. The English version is about 20% longer than the Chinese.
- **Re-hook interval:** the beat table has 31 beats in 489 s = **one turn every about 16 s**. From 3:10 on, the interval shrinks to about 12 to 15 s: a dream-wake every 20 to 30 s from 5:00 to 6:21. Explicit fear interjections (心脏骤停 / 心脏狂跳 / 毛骨悚然 / 心凉了半截) recur about every 45 to 60 s.
- **Structure by percentage:**
  - Hook and rules: 0 to 8%.
  - First proof fails, threat goes indoors: 8 to 14%.
  - Suspects, accusations and tokens: 14 to 37%.
  - Test denied, dream 1, footage proof: 37 to 52%.
  - Misdirection (scar) and counter-evidence: 52 to 61%.
  - Nested-dream gauntlet: 61 to 79%.
  - Betrayal instruction and switch reveal: 79 to 90%.
  - Real wake-up, identity reveal, kill, coda: 90 to 100%.
- **Hook:** the 6-second cold open is the premise in one sentence: hour, sound, "vanishes when I look", 3 days. The YouTube compilation uses it as the title.
- **Cliffhanger / part 2:** none. It is a closed one-part story with a franchise tag ("embark on saving the world"). In compilations, the next story starts within 1 s of 全剧终 (danmaku: "无缝衔接", "seamless"). Repost channels like udhwkz would split it at the 3:47 footage-proof beat or at 5:24, after "day 7".

## 8. Visual vocabulary

- **Phone UI:** a full-height WeChat-style chat panel on the left half of the frame, with the hero holding a black phone on the right.
  - Contact title "时空猎人" at the top. The helper has a black square avatar with "猎"; the hero has an orange avatar with "杰".
  - The hero's messages are green bubbles on the right; the helper's are white bubbles on the left.
  - Messages append one by one in sync with the VO, and the panel stays up for about 15 to 50 s per exchange (about 0:10 to 1:00, 1:54 to 2:16, 3:57 to 4:12, 6:27 to 6:47).
  - There is no timer UI; the countdown lives only in narration.
  - Phone video playback is shown as a cut to a "footage" shot of the hallway or living room.
- **Rooms:**
  - The boy's bedroom: grey bed, door, side cabinet with a pink potted flower. This is the "home base" shot, reused all story.
  - Grandpa's bedroom at night.
  - A dining table with braised rabbit dishes (red food is a recurring prop).
  - A living room with a white sofa and wooden shelving; Uncle Wang's grey-blue sofa room.
  - A kitchen with green cabinets.
  - The flat block exterior / ground (burying), and a sunlit window (the "is it real?" shot).
- **Characters:**
  - Hero: a chibi teen in a neon-yellow jacket over a white tee, spiky dark hair. He is the studio's recurring "小杰 / Chen Jie" model.
  - Grandpa: white-haired, black blazer.
  - Dad: a suit.
  - Uncle Wang: a green-grey tracksuit.
  - Expressions are limited and meme-like: wide-eyed shock with tiny pupils, sweat-drop fear, smug squint at the reveal, cold stare for suspects. Mouths flap only.
- **Monster:** a muscular, fully black horned humanoid with glowing red/purple eyes and clawed hands. It appears first as a silhouette head poking from a door and hanging from the ceiling, then in full body. It is never shown actually grinding with detail; the sound carries it.
- **Overlays and FX:**
  - Burned-in single-line white captions with a dark outline at the bottom centre, on every frame.
  - A red/orange glowing magic circle with smoke under the trapped monster.
  - Cartoon fire filling the frame for the kill.
  - A glowing golden brooch held at arm's length like a talisman.
  - A white flash or a hard cut on each false awakening (wake shot = the hero bolting upright in bed).
  - No on-screen timers or countdown numerals in this story. The neighbouring stories in the compilation use floating lifespan numbers, which is a distinct overlay style worth noting for other episodes.
