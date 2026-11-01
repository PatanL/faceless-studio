# BV14EiCBdEUh: 迷雾伪行 ("Mist: Impostor Walk"). On his 20th birthday the hero gets texts saying he is not human

> Internal research only. Do not translate, retell or remix this story for publication. We study its mechanics so we can write original, transposed stories that pass `scripts/originality_check.py`.

## 1. Header

| Field | Value |
|---|---|
| URL | https://www.bilibili.com/video/BV14EiCBdEUh |
| Title | 一口气看完【迷雾伪行】20岁生日那天，我突然收到短信，请注意，你不是人类 ("Binge it in one go: [Mist: Impostor Walk]. On my 20th birthday I suddenly got a text: attention, you are not human") |
| Channel | 杰出影视本人 (Bilibili mid 75872737), from the 【迷雾 X】 series that the English "Chenjie" repost ecosystem draws on |
| Uploaded | 2026-01-07 |
| Views | 49,607 plays as of 2026-11-01. 2,476 likes, 883 favs, 8 danmaku, 11 replies |
| Duration | 945 s (15:45) |
| Tags | 充电动画短剧孵化 (paid "charge" animated-drama incubator), 细思极恐, 烧脑, 悬疑, 恐怖, 一口气看完 |
| English repost evidence | **Confirmed.** lehwh7 TikTok [7651280297169816865](https://www.tiktok.com/@lehwh7/video/7651280297169816865), "I Got A Message Saying 'You Are A Weirn' On My 20th Birthday": **528.7K views**, 33.1K likes, 609 comments, 938 s, posted 2026-06-14. lehwh7 YouTube [BCjSTd7cJxw](https://www.youtube.com/watch?v=BCjSTd7cJxw): 23K, 937 s. The repost has **10.7× the source's views** and went up 5 months after the source. The match is shot for shot: it is mirrored footage with the same birthday, unknown-number texts and starch-sausage test. |

**How this was studied.** All processing ran on the Spark CPU with `nice -n 10` and `CUDA_VISIBLE_DEVICES=""`. Files are in `dgx-spark:~/studio/refs/horror-cn/BV14EiCBdEUh/`.
- **Free preview only.** The video is 充电 (paid "charge") content. Logged out, Bilibili serves only the first **505 s (to 08:25)** at every resolution, even though the API reports 945 s. yt-dlp got HTTP 567 from the CDN, so `src.mp4` (480p, 505 s) was fetched through the html5 playurl API.
- **First half (00:00–08:25), Chinese.** RapidOCR at 1 fps read the hard-coded Chinese captions and phone screens (`ocr_zh.jsonl`, condensed in `ocr_zh_condensed.txt`). faster-whisper small, zh, int8, 4 threads, gave narration timing (`zh_whisper.txt`). Bilibili has no auto-subs without a login.
- **Second half (08:25–15:45), English.** It comes from the lehwh7 YouTube repost: `en_repost.mp4` (480×854), its English auto-subs (`en_repost_clean.txt`), and RapidOCR on horizontally flipped frames for the Chinese phone screens (`ocr_en_flip.jsonl`). The repost's Chinese captions are cropped out, so second-half beats rest on the English TTS translation. That translation renders 伪人 inconsistently as "Weiran", "Weirn" and "mutant".
- **Timestamps.** "src" times are source times. In the second half, times are estimated from the repost clock (≈ src 08:25 + (repost − 07:42) × 0.93) and marked "≈".

Glossary: **伪人** (wěirén) means "fake person / impostor". It is the monster class in this story. A 伪人 replaces a human and is undetectable until age 20.

## 2. Story outline (my summary)

- **The texts.** On his 20th birthday at a family dinner, Chen Jie (陈杰, "小杰") gets texts from an unknown number. They say he is not human: he is a 伪人 and must hide.
- **The six rules.** A second text gives a six-point "how humans detect 伪人 / how we counter-disguise" list:
  1. Before 20 you can't be told apart.
  2. Humans never have powers, but 伪人 awaken one at 20.
  3. Humans pricing starch sausages follow "3 yuan for one, 5 for two."
  4. Humans far outnumber you.
  5. If suspected, clear the suspicion or die.
  6. Not every human knows 伪人 exist.
- **The vanishing texts.** He dismisses it all as a prank. Then his dad grabs the phone, and the texts have vanished, replaced by a message from the school beauty, Lili (丽丽), inviting him to the swimming pool.
- **The cousin dies.** His cousin Xiaoqiang (小强) gets the same texts. The uncle (大舅, mother's brother) asks the cousin the starch-sausage question. The cousin gives the text's answer ("5 or 6 for two"), and the uncle beats him to death with a baseball bat. The body melts into black liquid.
- **Dad explains, then asks.** The parents explain that 伪人 exist, are undetectable before 20, and that only 伪人 receive these texts. Then they turn the sausage question on Chen Jie.
- **The trap answer.** He works out that the text's "rule" is the trap. A real human answers from lived experience: they're 2.5 yuan each. That answer clears him. The uncle still looks at him with malice.
- **His power?** Alone, he realises his "power" is making the texts invisible to humans. He texts the unknown sender a "correction" to the manual. The "system" thanks him and offers a reward: a 伪人-scent suppressor in swimming-pool locker 35, code 1234.
- **The knife feint.** The uncle drops by and claims 伪人 blood changes colour after 20. He feints with a knife to grab the phone. Mom walks in with fruit at the right moment, and the hidden texts stay hidden.
- **Lili's note.** At the pool, Lili says she is a 伪人 too. She gives him a note of 4 "replacement rules":
  1. Once inside a family, bring at least one companion into it.
  2. Raise your ally without telling them anything before 20.
  3. Never reveal yourself, since you can't know who your ally is.
  4. A 伪人 can host only one companion, and 伪人 cannot kill 伪人.

  He guesses Mom is his ally.
- **The locker.** The uncle catches him at the lockers and says human genes instinctively sense replacement. Chen Jie grabs the locker item and runs. The uncle just smiles. *(The free preview cuts here at 08:25. lehwh7's "Part 2" badge starts at the same point.)*
- **"Your prop is marked."** A new text says locker 35 has been triggered, every concealment prop is void, and his item is marked. He concludes the texts were sent by humans all along. He flees on foot to a forest.
- **Mom or Dad?** Mom finds him and carries him. Dad texts: "run, your mom isn't one of us, she'll hurt you." Dad arrives and the parents square off. Mom lifts a huge rock, a sign of a 伪人 power.
- **Which parent is the ally?** Lili and her father wave him across a road. He tests them: did my mom send you? Lili's odd reaction tells him it was Dad. He re-reads the past: the text-hiding power was Dad's, and the fruit plate was Dad's idea. So Dad is his secret 伪人 ally.
- **Lili dies; the hero says "I'm human."** Lili's father kills her, and she melts. Chen Jie objects that 伪人 can't kill 伪人. The father says he is human, and that Chen Jie is human too: Chen Jie sent him the anonymous tip about Lili. Chen Jie admits it. He says he is human and staged everything to flush out the 伪人 around him.
- **Lore dump.** 伪人 reproduce once, by dissolving a piece of heart flesh in water for a human to drink. Dad made him that way. The 伪人 inside him lost a fight for his body at 18. Mom and he subdue Dad, who is executed by the 伪人管理局 (Impostor Management Bureau). Chen Jie joins the Bureau.
- **Back at school.** The cover story says Lili and her mother died in a car crash. He reasons that Lili's mother was the replaced one. By elimination he concludes Mom replaced his cousin:
  - The uncle killed a 伪人, so he is human.
  - The aunt died in childbirth.
  - Dad had already used his one replacement on him.

  He kills Mom in her sleep.
- **Who sends the texts.** On the sofa, the uncle mass-sends texts. They were first sent by a turned 伪人 informant and are now sent by government agents. Dad's last words had been "I know what you are; live on, for our kind."
- **Mirror twist.** The narrator is the 伪人. His power is **symbiosis**: the real Chen Jie lives sealed inside him. 伪人 can't kill 伪人, but the human inside can, so he used the human half to kill Mom. He has fooled the uncle and the whole Bureau.
- **Coda.** He dissolves a piece of his heart in a bottle of mineral water and hands it to the uncle. THE END.

## 3. Beat table

Times are source time. "≈" marks second-half times estimated from the English repost.

| Time | Beat | Mechanic | What the viewer believes now | Open loops |
|---|---|---|---|---|
| 00:00 | Birthday + unknown-number SMS: "you are not human, don't expose yourself" | Cold-open hook in line 1. Burner/unknown-number warning. Milestone-age trigger (20th birthday) | Hero is a normal kid being pranked, or secretly a monster | Who sent it? Is he human? |
| 00:08 | Dad leans in and the screen goes black by itself | Phone glitch / anomaly. Lie to family ("just spam") | Something supernatural is shielding him | Why did the screen die? |
| 00:24 | Second SMS: 6-point detection/counter-disguise rule list | **Rule list** on full-screen phone UI. **Fake authority + wrong detail** (the sausage price, rule 3) | Rules are an insider's survival guide | Which rule matters? Rule 3 is oddly specific |
| 00:51 | Hero mocks the rules: no powers, so he's "100% human" | Skeptic beat. Narrator "corrects" rule 3 with his own price knowledge, a hidden plant | Rules are nonsense | — |
| 01:12 | Dad grabs the phone; the texts are gone, replaced by the school beauty's pool invite | **Mute/recall**: messages vanish. Romance decoy | Someone deleted them? | Who erased them? Why the pool? |
| 01:43 | Cousin gets the same texts; the uncle snatches the phone: "are you human?" | **Group pressure** (family dinner as a tribunal). Contagion: it's not just me | The texts are real | What will the uncle do? |
| 02:10 | Sausage question → cousin gives the rule's answer → bat kill → black puddle | **Shibboleth test.** Shock death of a minor character. Body-melt "proof" | The rule answer is fatal; the family are hunters | Why did the "right" answer kill him? |
| 02:49 | Dad's exposition: 伪人 replace people, undetectable before 20, **only 伪人 get these texts** | Trusted source (parent) gives world rules. The key rule is planted | Hero is a 伪人 by definition | Will they test him? |
| 03:13 | Dad's gaze goes cold: "can you answer it?" | Everyone stares. Ticking interrogation. Cornered | He's about to die | — |
| 03:28 | He fakes outrage to stall; the uncle presses: "even a wrong answer doesn't make you one" | Pressure from the group. A false safety net | — | — |
| 04:01 | Deduction: the trap is the sausage, not the price → "2.5 yuan each" | **Trusted source contradicted** (the text was wrong on purpose). Lived-experience shibboleth | He's safe, and smart | Uncle's lingering malice |
| 04:34 | Bedroom: his power = hiding texts from humans | Rule 2 pays off (powers at 20). A false ability attribution, planted | His power explains the vanishing | Who's helping him? |
| 04:56 | He texts the sender; no answer; a "correction" gets a reply: system update + reward, locker 35, code 1234 | **Fake authority** ("survival manual system", gamified reward). Bait | An ally network exists | Is the reward real? |
| 05:31 | Uncle visits, claims blood changes colour, knife feint, steals the phone | **Wrong detail** (the blood claim is a bluff). Misdirection | Uncle is hunting him | Will the uncle see the texts? |
| 06:02 | Mom walks in with fruit; he wills the texts hidden; the uncle sees nothing | Rescue by a parent (planted to be re-attributed later) | Mom is his ally | Did Mom do it on purpose? |
| 06:29 | Pool: Lili says "I'm one too; every family with one 伪人 has another" | Ally reveal. **Count clue** (at least two per family) | He has allies | Who's the other one at home? |
| 06:53 | Note: 4 replacement rules (bring a companion; raise them silently; never self-reveal; host only one; **伪人 can't kill 伪人**) | Second rule list on paper. **Count clue** (only one). Kill-restriction rule | Mom = companion (the uncle killed, so he's ruled out) | Can he trust Lili? |
| 07:30 | Two metres from locker 35, the uncle grabs his shoulder: "you're a deep-cover 伪人" | Gut-instinct-genes lore. Knife again. Identity accusation | Uncle knows | — |
| 08:14 | Keypad, grab, run; the uncle doesn't chase, eerie smile | **Paywall cliffhanger**: the free preview ends at 08:25 on the smile. The English "Part 2" starts here | The pickup worked, or it's a trap | Why didn't he chase? |
| ≈08:32 | SMS: "locker 35 triggered, all props void, your prop is marked" | **Trusted source contradicted**: the sender is human. Timer/marked-item pressure | He's been tracked the whole time | Who's safe? |
| ≈09:00 | Flees on foot (no public transport, someone might shout "impostor") | Paranoia monologue. Location change (forest) | He's alone | — |
| ≈09:23 | Mom finds and carries him; Dad texts "run, Mom isn't one of us" | **Two trusted sources contradict each other** (Mom in person vs Dad by text). Narrator: "the message is at least half suspect" | Mom or Dad: one is the ally, one the hunter | Which parent? |
| ≈09:56 | Parents square off; Mom lifts a huge rock (power) | Visual "proof" pointing at Mom (a misdirect) | Mom is a 伪人 | — |
| ≈10:33 | Lili and her father wave him over; he tests: "did my mom send you?" Lili looks odd | Test question to an ally. Interrogating a helper | Not Mom: it's Dad | — |
| ≈11:01 | Re-read: the hiding power was Dad's; the fruit was Dad's idea | **Reversal by re-attribution**: earlier beats replayed with new meaning | Dad = secret ally | Then who's the threat? |
| ≈11:24 | Lili melts; her father did it; "伪人 can't kill 伪人" → "I'm human" | Kill rule pays off (it proves the father is human) | Lili's dad is a hunter | Is the hero next? |
| ≈11:33 | Lili's father: "you're human too, you tipped me off about Lili"; hero: "yes, I staged it all" | **Reversal 1: hero claims to be a human hunter.** Recontextualises everything | Hero is human; Dad is a 伪人 | But he got the 伪人-only texts… |
| ≈11:50 | Lore: heart-flesh water, reproduce once, a body fight at 18 | Exposition beat (biology rules). Plants the age-18 struggle | Dad tried to replace him and failed | — |
| ≈12:30 | Hero + Mom subdue Dad; Bureau executes him; hero joins the Bureau | Institution reveal (伪人管理局) | Case closed | Mom? |
| ≈13:15 | School gossip: Lili and her mother "died in a car crash"; the father survived | Cover-story beat. Deduction: Lili's mother was the replaced one | — | Who replaced the cousin? |
| ≈13:29 | Elimination: the uncle killed a 伪人 (so human); the aunt died in childbirth; Dad used his one → Mom | **Count clue pays off** (only one each). Kill-rule pays off | Mom is a 伪人 | — |
| ≈13:57 | Night: he kills Mom in her sleep | Cold escalation | Hero is a ruthless human hunter | — |
| ≈14:06 | Sofa: the uncle batch-sends texts; the sender was a turned informant, now agents | Sender reveal (the texts are a government honeypot) | World explained | Dad's last words? |
| ≈14:29 | Dad's last words: "Son, I know your identity, live on, for our kind" | Planted line, paid off immediately | Odd… | — |
| ≈14:34 | Mirror: "the real Chen Jie is sealed inside me." Power = symbiosis; the human half did the killing | **Final reversal: unreliable narrator.** Mirror reveal. Loophole in the kill rule | Narrator is the monster and fooled everyone | What will he do now? |
| ≈15:10 | Heart flesh into mineral water, handed to the uncle (an agent) | **Last-line escalation** (the monster infiltrates the hunters) | The uncle will be replaced | Sequel hook |

## 4. Clue chain

| # | Clue planted (src time) | Payoff |
|---|---|---|
| 1 | Rule 3: "3 yuan for one, 5 for two" (00:24); the narrator muses that haggling saves a yuan (01:05) | The cousin dies on the rule answer (02:23). The hero's lived-experience price, 2.5 each, saves him (04:16). The planted rule was a human-made trap (≈14:06). |
| 2 | The screen dies by itself when Dad leans in (00:12); the texts vanish when Dad holds the phone (01:27) | First read as the hero's power (04:50). Re-attributed as Dad's power (≈11:01). Finally the hero's real power is something else, symbiosis (≈14:34). |
| 3 | "Only 伪人 receive 伪人 texts" (03:06) | The hero received them, so his ≈11:33 "I'm human" claim contradicts a stated rule. That is the fair-play tell for the mirror twist. |
| 4 | Rule 2: powers awaken at 20 (00:31) | Drives the "what's my power" beat (04:34), Mom's rock (≈10:19), and the 20th-birthday framing. The hero turning 20 is when his symbiosis ability matters. |
| 5 | "Not all humans know 伪人 exist" (00:47) | The car-crash cover story (≈13:15) and the secret Bureau (≈12:47). |
| 6 | The uncle's lingering malice (04:29, 06:25) and "gut feeling from genes" (07:59) | The uncle was right all along. He is a human agent. He becomes the final victim (≈15:10). |
| 7 | Mom arrives with fruit at the critical moment (06:02) | First read as Mom = ally (07:23). Re-read: the fruit was Dad's idea (≈11:01). |
| 8 | Lili: "where there's one 伪人 in a family, there's another" (06:43) | Sets up the "who's my companion" hunt (07:18). The home holds two 伪人, Dad and Mom. |
| 9 | Replacement rule 4a: "can host only one companion" (07:12) | Elimination logic: Dad's one was the hero, so Mom replaced the cousin (≈13:29). |
| 10 | Replacement rule 4b: "伪人 cannot kill 伪人" (07:15) | Clears the uncle (07:20). Clears Lili's father (≈11:24). Mom and Dad fight but can't kill each other (≈12:30). Final loophole: the human half kills Mom (≈14:40). |
| 11 | The "system" reward: locker 35, code 1234 (05:16) | A human honeypot. The prop gets marked (≈08:32). Explains why the uncle didn't chase (08:24). |
| 12 | The uncle's knife and blood-colour claim (05:44) | A bluff. The real goal was the phone. It teaches the viewer that hunters lie with wrong details, which primes the sausage-rule logic. |
| 13 | Lore: replacement via heart flesh dissolved in water (≈11:40) | The coda, mineral water handed to the uncle (≈15:10). |
| 14 | The body struggle "at 18" (≈12:40) | Inverted by the mirror twist: the 伪人 won, or rather coexists (≈14:34). |
| 15 | Dad's last words: "I know your identity… for our kind" (≈14:15) | The mirror twist (≈14:20). Dad knew the narrator was his 伪人 offspring. |

## 5. Twist inventory

| # | Twist (≈src time) | Type | Setup |
|---|---|---|---|
| 1 | The rule-list answer is the death answer (02:23) | **Trusted source contradicted** / poisoned rule | Rule 3's suspiciously exact price, plus the narrator's own aside that real prices vary |
| 2 | The family are hunters, not victims (02:10–02:49) | Ally → threat | The uncle's anger at "are you human" and the parents' faces "changing" |
| 3 | Correct answer = lived experience, 2.5 yuan (04:16) | Shibboleth inversion (book knowledge vs street knowledge) | The 01:05 haggling aside |
| 4 | The knife is a feint; the target is the phone (05:52) | Misdirection | The blood-colour claim |
| 5 | The school beauty is a 伪人 (06:37) | Romance → ally reveal | Her suspicious text arriving exactly as the others vanished |
| 6 | The reward locker is a human trap (≈08:32) | **Fake authority** exposed | The gamified "system" tone; the uncle not chasing |
| 7 | Dad, not Mom, is the ally (≈11:01) | Re-attribution reversal | The fruit plate and the vanishing texts happening near Dad |
| 8 | Lili's father kills her, so he's human (≈11:24) | Kill-rule proof | Replacement rule 4b |
| 9 | The hero is a human double agent who tipped off the hunters (≈11:33) | Protagonist allegiance flip | Few clues: this is the deliberate false bottom |
| 10 | Mom is the second 伪人; the hero kills her (≈13:57) | Deduction by elimination | Rule "only one companion" + the aunt's death in childbirth + the uncle's kill |
| 11 | The texts are a government honeypot (≈14:06) | Sender reveal | Twists 1 and 6 |
| 12 | **The narrator is the 伪人 (symbiosis); the human half did the killing** (≈14:34) | Unreliable narrator / mirror reveal | Clue 3 (only 伪人 get texts), Dad's last words, the age-18 struggle, the kill-rule loophole |
| 13 | He seeds the uncle via heart-flesh water (≈15:10) | Final escalation / sequel hook | The reproduction lore |

The chain runs about 13 twists in 15:45, roughly one per 73 s. In the second half it speeds up to about one per 40 s.

## 6. GENERIC vs SPECIFIC

**GENERIC (genre conventions anyone can use)**
- An unknown-number or system text announcing "you are not human / you are the monster" at a milestone (birthday, first day, move-in).
- A numbered rule list delivered as a full-screen phone message, with one rule deliberately wrong (fake authority + wrong detail).
- Shibboleth tests: an everyday-knowledge question where book knowledge kills and lived experience saves.
- A family dinner that turns into a tribunal. A minor relative killed early as proof of stakes. Monster corpses dissolve (proof without gore).
- Messages that vanish when others look. A "what's my power?" beat after a coming-of-age awakening.
- A gamified "system" voice (reward, update, user) as bait. A honeypot location: locker, mailbox, drop point.
- Two trusted sources contradict each other (in person vs by text), and the hero tests a helper with a question only the true sender could answer.
- Rules with countable limits ("only one", "can't kill own kind") that later drive deduction by elimination and then become loopholes.
- A reveal that a secret agency runs the warnings. A cover-story news beat.
- An unreliable first-person narrator flipped in the last minute: a mirror reveal. The monster wins and spreads in the final line.
- A paywall or Part-2 cut on a silent menacing look rather than an action.

**SPECIFIC (this author's expression: a transposed story must NOT reuse it)**
- The 伪人 creature and its exact lore:
  - Undetectable until 20, power at 20.
  - Heart flesh dissolved in water as the means of reproduction, once per life, six months after awakening.
  - Black-liquid melt.
  - A "symbiosis" power with the real self sealed inside.
- The starch-sausage (淀粉肠) price shibboleth, the "3 for one / 5 for two" rule, and the "2.5 yuan" answer.
- The named cast and roles:
  - 陈杰/小杰, the hero.
  - 小强, the cousin killed by his own father.
  - 大舅, the uncle-agent.
  - 丽丽, the school-beauty 伪人 killed by her father, with the car-crash cover.
  - Mom and Dad as the two 伪人.
  - The aunt dead in childbirth.
- The exact props and tricks: locker 35, code 1234, the "scent suppressor" watch, the blood-colour knife feint, the fruit-plate rescue, the giant-rock tell.
- Both rule lists as written: the 6-point detection list and the 4-point 替换守则 replacement rules.
- The 伪人管理局 bureau, and its history of a turned informant who once sent the texts.
- The exact twist chain: the hero claims to be a human double agent → kills Mom → mirror symbiosis reveal → heart-water to the uncle.
- Distinctive lines: "在人类横行的世界里活下去吧" (survive in a world overrun by humans); Dad's dying "for our kind"; the mirror monologue.

**Transposition notes (structure only).** Keep the shape: milestone text → rule list with one poisoned rule → relative dies on the "correct" answer → hero survives by lived knowledge → bait reward → contradicting sources → count-rule elimination → allegiance flip → mirror reveal. Swap the creature, the shibboleth (it must be culturally native to the English audience), the cast, the props, the agency and the final mechanism. The lived-knowledge shibboleth is the most portable device. It needs a question that every real local answers "wrong" by the book.

## 7. Pacing

**Chinese source (first 505 s, from OCR captions plus whisper)**
- Caption lines: 326 in 505 s, which is **38.7 lines/min**. Each line holds one caption of about 9.8 Chinese characters on screen for about 1.5 s.
- Characters: **≈379 chars/min**. The whisper speech rate is 375 chars/min. That is fast, flat TTS-style narration, steady across the video:
  - 0–1 min: 412 chars/min.
  - 1–3 min: 370.
  - 3–5 min: 381.
  - 5–7 min: 377.
  - 7–8.4 min: 372.
- In English terms, that is roughly 230–250 words/min. The lehwh7 English TTS runs about **250 wpm** (about 3,900 words in 15:37).

**Hook**
- Hook length is about 7 s: the first 3 caption lines carry the whole premise, with no intro and no title card.
- The first escalation, the rule list, lands at 00:24. The first death lands at 02:23, 15% in.

**Re-hook interval.** First-half turns land at:

00:08, 00:24, 01:12, 01:43, 02:10, 02:49, 03:13, 04:01, 04:29, 04:49, 05:16, 05:33, 05:47, 06:02, 06:37, 06:53, 07:32, 08:09, 08:24

That is **19 turns in 8:25, one every ≈27 s**. Second-half reversals come about every 20–40 s, and the final minute stacks two twists.

**Cliffhanger and part-2 mechanics**
- Bilibili free-preview cut. The 充电 paywall cut sits at **08:25 (53%)** on a silent beat: the uncle doesn't chase and just smiles.
- lehwh7's "Part 2" break. lehwh7 reuses exactly that point. A "Part 2" badge appears from about 07:42 of the repost, the captions switch to bold impact style, and the whole thing posts as one 15:38 video.
- Lesson: put the part break at the midpoint, on an unexplained calm reaction from the antagonist. Don't put it on an action.

**Structure ratios (of 945 s)**

| Section | Range | Share |
|---|---|---|
| Hook and rules | 0–5% | 5% |
| First death | 15% | — |
| Survival test | 18–29% | 11% |
| Bait and investigation | 30–53% | 23% |
| Chase and contradicting sources | 54–75% | 21% |
| Allegiance flips | 72–90% | 18% |
| Mirror reveal | 92% | — |
| Coda | last 4% | 4% |

**Exposition**
- 3 lore dumps: Dad at 02:49, the uncle at 07:51, the hero at ≈11:40.
- Each is under 40 s and sits right after a shock, so the viewer is still hooked.

**Narration stance.** First-person past tense, with constant inner-monologue deductions ("不对…", "no wait…") that turn reasoning itself into a beat.

## 8. Visual vocabulary

**Style**
- 2D flat-shaded "沙雕" big-head chibi animation.
- Thick outlines, minimal limb animation, mostly static poses with camera push-ins and zooms.
- Frame 852×480, 16:9, 30 fps.

**Characters**
- Hero: spiky black hair, **neon yellow-green zip jacket with a lightning bolt**, white tee. Always holds a black phone with a cartoon pineapple on the case.
- Dad: black tee, short hair.
- Mom: purple top, black bob with bangs, thin arched brows.
- Uncle: bald, **pink V-neck sweater**, permanent sneer. Reaches for a baseball bat or knife.
- Cousin: white hoodie.
- Lili: denim jacket and dark skirt.
- Lili's father: black suit.
- Classmates: orange cap.

**Expressions**
- Narrowed side-eye squint for suspicion; it is the hero's default "thinking" face.
- Wide round shocked eyes with tiny pupils.
- Uncle's half-lidded malicious smile.
- Mom's flat stare.
- Close-up face zooms with black vignette for menace.
- A sweat-drop pose for panic.

**Phone UI**
- Full-screen SMS overlay: grey title bar with a "<" chevron and the contact name (未知号码 "unknown number", 校花-丽丽, 老爸).
- **Green incoming bubbles** on the left, **blue outgoing** on the right.
- Long rule lists are crammed into a single green bubble, readable on pause.
- System notices ("检测到35号储物柜…") come as stacked green bubbles.
- The phone is often shown in-hand at the frame edge while the character reacts.

**Paper props.** A handwritten-style note titled 伪人替换守则 ("impostor replacement rules"), held up full frame.

**Rooms and places**
- Living/dining room: wooden display shelves with bowls, a birthday cake with one candle. This is the tribunal set.
- Hero's bedroom: grey bed, dim.
- Swimming-pool entrance and grey locker corridor: numbered blue circle plates 34/35, a keypad close-up.
- Night forest: green trees on a purple-black sky.
- Roadside, a classroom with a green board, Mom's bedroom at night, the sofa, a mirror.

**Overlays and effects**
- Hard-coded white captions with black stroke, bottom centre, one line.
- Watermark "杰出影视本人 bilibili" at top right.
- Purple radial burst for shock or flashback.
- A grey smoke puff for fights.
- The black-liquid puddle for monster death.
- Hard cuts. No danmaku-style on-screen chat.

**The English repost's adaptations (lehwh7)**
- Mirrored footage, which defeats Content ID.
- 9:16 frame with the video band in the middle, small English caption line above it, cyan "@lehwh7" watermark.
- Part 2 uses bold white/yellow impact captions, then a "THE END" card.
- The Chinese captions are cropped out. The phone screens stay in Chinese, unreadable to English viewers, and still worked: the 529K views came without translated UI.
