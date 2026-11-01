# BV1fR7szYEDq: 迷雾恐龙 ("Mist Dinosaur"): a zoo dinosaur knocks on my door at night

Internal research only. This file studies structure so we can write original, transposed stories. Do not translate, retell or remix this story for publication. See `SOURCES.md` for the rules and for the wider channel map.

## 1. Header

| Field | Value |
|---|---|
| URL | https://www.bilibili.com/video/BV1fR7szYEDq |
| Title | 一口气看完【迷雾恐龙】晚上一只恐龙突然敲响我家的门 ("All at once: [Mist Dinosaur] a dinosaur suddenly knocks on my door at night") |
| Channel | 杰出影视本人 (Bilibili mid 75872737), the source studio behind the English "Chen Jie" repost ecosystem |
| Uploaded | 2025-05-31 |
| Views | 230,514 Bilibili plays (2026-11-01), 10.3K likes, 638 danmaku |
| Duration | 7:47 (467 s), a single episode with no part 2 |
| English reposts | mraevq TikTok [7666044652910316833](https://www.tiktok.com/@mraevq/video/7666044652910316833): **326K** (2026-07-24). lehwh7 TikTok [7649861675100753185](https://www.tiktok.com/@lehwh7/video/7649861675100753185): **305K** (2026-06-10). lehwh7 YouTube [FiNl_v_Eswg](https://www.youtube.com/watch?v=FiNl_v_Eswg): 16.7K. That is **631K on TikTok** across two reposts, 2.7x the Bilibili count. |
| Match evidence | Confirmed. The mraevq English transcript (`research/library/transcripts/7666044652910316833.txt`) follows this video line by line, from the "our zoo bred a dinosaur" opener through to the closing "the zoo belongs to us" call. The repost runs 6:41 against 7:47 here, so its TTS is about 1.16x faster. It translates literally and cuts nothing. |

**How the data was gathered** (Spark CPU only, `nice -n 10`, `CUDA_VISIBLE_DEVICES=""`):
- **Video.** The 480p AV1 stream (852x480) is at `dgx-spark:~/studio/refs/horror-cn/BV1fR7szYEDq/`.
  - yt-dlp returned HTTP 567 from the `mirrorcosov` CDN host for every video format, but audio downloaded fine.
  - The fix: take the URL from `yt-dlp -g` and fetch it with curl, a Bilibili Referer header and the host swapped to `upos-sz-mirrorhw.bilivideo.com`.
- **Subtitles.** There are no auto-subs; Bilibili subtitles need a login. The danmaku XML was saved.
- **Narration text.** It comes from **OCR of the burned-in captions** at 1 fps (rapidocr, `~/studio/venvs/r2`): 311 deduplicated caption lines and 2,867 characters, in `captions_ocr.txt` and `ocr.json`.
  - The captions are the narration word for word.
  - faster-whisper medium (zh, 4 threads) matched the OCR on the 0–26 s it finished, apart from homophone errors. I stopped it there because the box load average was 56 and the run would have taken more than an hour. The partial output is in `whisper_medium_partial_0-26s.txt`.
- **Images.** The contact sheets (`sheet_0..2.jpg`, one frame every 4 s) and a UI grid (`ui.jpg`) are on the Spark.
- **Translation.** The English below is my own paraphrase. The mraevq transcript above is a near-literal English rendering of the full script, if anyone needs line-level detail.

## 2. Story outline (my summary)

The narrator, Chen Jie, works at a zoo whose director has made a fortune exhibiting a small dinosaur the zoo bred. One night, six months later, the dinosaur knocks on Chen's apartment door, speaks in a human voice and calls him "Dad". His coworker Wang Qiang phones to say the animal has escaped. When Chen presses him, Wang admits the director had Chen's DNA spliced in so the animal would be smart enough to perform. Chen hangs up angry.

The director begs Chen not to call the police because the animal hasn't paid for itself yet. Chen remembers the director refusing to let anyone shoot it when a visitor fell into its pen, so he calls the police anyway.

The knocking wakes the next-door neighbour, Sister Wang. She comes out to complain and the dinosaur pins her. She begs Chen for help, and he reaches out and *locks his own door*. Through the peephole he watches the dinosaur use her hand to open her fingerprint lock and drag her inside. It then carries her onto the balcony and eats her where he can see it. She wakes mid-meal, curses him and dies. After eating, the dinosaur visibly grows, from about 1.8 m to 2.5 m.

The director arrives with a tranquilizer gun and a net and refuses Chen's demand to bring a rifle. Off-screen there is a fight, then silence. The director knocks alone and asks to come in "for a drink of water". Wang Qiang phones to warn Chen: the director only brought two keepers. Chen reasons that two men could not carry a 400 kg animal down eight floors. He rings one of the keepers, and the ringtone sounds from the flat next door. The director confesses that the keepers are dead and the dinosaur is sedated but waking, and begs to be let in. Chen deduces that the director could simply run downstairs, so the dinosaur must be standing behind him, forcing him to lure Chen out. He refuses, telling the director this is his own fault. The dinosaur kills the director, eats all three men and grows past 3 m.

The police say snow has blocked the roads, so they are 30 minutes out. Chen warns the residents' group chat. They mock him ("dinosaurs are extinct"). The dead neighbour's husband, Brother Liu, is away on a business trip. He thinks Chen and his wife are pranking him after a fight, and offers 2,000 yuan to anyone who will check flat 804. A gym-type neighbour, Gao Xiang, who calls himself a wilderness-survival expert, takes the job. Chen DMs him not to go.

Gao livestreams the flat to the group: there is no dinosaur, only the wife's bloody clothes on the balcony. The group turns on Chen ("did you kill her and blame a dinosaur?"). Chen spots something behind Gao, and the dinosaur swats Gao away. Minutes later Gao's phone rings Chen, and the dinosaur's voice says "Dad, I'm coming to you." It has grown again and learned to climb, and it crawls along the balconies toward Chen's flat. Chen runs out, meets the arriving police and sends them up, and they shoot it.

**Twist ending.** Wang Qiang calls: *did the police suspect you?* Chen says no. The CCTV proves the dinosaur did everything, the director is dead, the zoo is now "ours", and they will breed more dinosaurs and rule the world. The narrator was a co-conspirator all along.

## 3. Beat table

Timestamps are from the Bilibili video. "Mechanic" uses the corpus device names where they fit.

| t | Beat | Mechanic | What the viewer believes now | Open loops |
|---|---|---|---|---|
| 0:00 | Zoo bred a dinosaur; the director gets rich from it | Cold-open premise in 2 captions; money motive planted | Mundane setup: the director is the profiteer | Why tell us about the money? |
| 0:05 | Half a year later the dinosaur knocks on my door at night | Knock at the door (title payoff in 5 s) | A creature-siege story | How did it find him? |
| 0:07 | Through the door it begs "Dad, open up, I'm hungry, I want meat" | Creature speaks + wrong familiar name | Absurd horror: it talks and calls him Dad | Why "Dad"? |
| 0:15 | Coworker Wang Qiang calls: it escaped, come help search. "No need, it's at my door" | Phone call cross-cut (zoo/home); helper character | Wang is a worried ally | |
| 0:26 | Wang: your door is custom-made, it can't break through; wait for the director | Reassurance from a trusted source (an odd detail: why does he know about the door?) | Chen is safe behind the door | **Why does Wang know the door is special?** (a danmaku viewer asked this at 0:39) |
| 0:31 | Chen demands the truth; Wang admits the director had Chen's genes added so it would be smart enough to perform | Confession/explainer; answers "Dad" | It's literally his offspring; the director is reckless | What else did they add? |
| 0:49 | "You bastard, I'll settle this tomorrow"; hangs up; Wang tells the director | Performed anger (reads as sincere the first time) | Chen is a victim of his workplace | |
| 0:55 | Director: don't call the police, it cost me a fortune and hasn't paid off | Authority with a greedy motive; prohibition ("don't call police") | The director is the villain | Will Chen obey? |
| 1:02 | Flashback: a visitor fell into its pen; the director wouldn't allow shooting; the leg was crushed | Backstory proof of the director's greed | The director values money over lives | |
| 1:11 | Chen calls the police anyway | Hero defies the authority | Chen is the decent one | When will police arrive? |
| 1:13 | Knocking resumes; neighbour Sister Wang comes out to complain | Bystander enters danger | She will be hurt | |
| 1:21 | Chen shouts at her to get inside; the dinosaur pins her instantly | Speed escalation | | |
| 1:29 | She begs Chen to save her; he reaches out and **locks his door**; "I'm no saint" | Reversal of expected heroism (a dark-comic beat) | Chen is selfish but understandable | How far will he go to survive? |
| 1:38 | Silence; through the peephole the dinosaur uses her hand on her fingerprint lock | Peephole reveal; creature intelligence | It's as smart as a human | |
| 1:49 | It drags her into her flat; Chen is "relieved", just has to wait for police | False calm | Threat has moved next door | |
| 1:55 | Screams from the next balcony; it eats her in front of him, on purpose | Deliberate display / taunt | It's targeting Chen personally | What does it want from him? |
| 2:09 | She wakes mid-meal: "why didn't you save me … it should have been you … you'll end up like me"; Chen tells her to endure, it'll stop hurting soon; she dies | Fake death + dying curse; cold response from the hero | Chen is chilling; the curse predicts his death | Will the curse come true? |
| 2:25 | Finished eating, it roars and grows to about 2.5 m (was bred to 1.8 m max) | Feeding-growth rule (count: size goes up) | It gets stronger with every kill, so the clock is ticking | What makes it grow? |
| 2:38 | Director calls: we're in your complex; Chen: building 8, unit 804, next door | Location lock-in | Help has arrived | |
| 2:47 | Chen: bring a rifle. Director: a tranquilizer and net are enough, "treat it like a child". Chen insists | Authority makes the wrong call; Chen puts his warning **on record** | The director will get people killed | Will the tranquilizer work? |
| 3:04 | Director admits adding "a bit of T-rex DNA" | Second confession (explains growth) | | |
| 3:13 | Director at 804: "careful, don't kill it, it's my money tree"; sounds of a fight | Off-screen fight (cheap to animate) | | Who won? |
| 3:22 | Wang Qiang calls: are you OK, have they got there? | Ally check-in (reads as concern; on rewatch it's a status check) | Wang cares | |
| 3:31 | Silence, then a knock: the director says it's sedated, "let me in for some water"; peephole shows him alone | **Trusted source at the door** + peephole | Maybe it's over | Where are the others? |
| 3:44 | Wang: "Don't open! He only brought two keepers. Could they handle it?" | Outside voice contradicts the authority | The director may be lying | Why lie? |
| 3:55 | Chen asks to see it; "my men carried it downstairs"; Chen notes it's 400 kg and they're on the 8th floor | **Count/logistics clue** (2 men, 400 kg, 8 floors) | The director's story is impossible | |
| 4:10 | Director pivots: "you were right, I'll put it down; let me in and I'll explain" | Authority changes story (tell) | | |
| 4:18 | Chen calls keeper Xiao Zhang; the **ringtone sounds from next door** | **Burner-phone/ringtone proof** | The keepers are inside 804, so they're dead | |
| 4:26 | Director confesses: the keepers are dead, he sedated it but it will wake soon, please open | Confession #3 | He's desperate and probably telling the truth | Open or not? |
| 4:38 | Chen: "it's a residential complex, not a prison — you could run downstairs. It's behind you, making you lure me" | **Deduction reversal** (he wouldn't need *my* door) | The dinosaur is using the director as bait | |
| 4:48 | Director weeps "you guessed it, so open the door!"; Chen: "you deserve this, I told you to bring a rifle" | Hero refuses; cites his on-record warning | Chen is ruthless but logically right | |
| 5:02 | The dinosaur appears behind the director and kills him; eats all three on the balcony; now over 3 m | Payoff of the deduction; growth again | The director's arc is closed | What stops it now? |
| 5:12 | Police: roads snowed in, 30 more minutes | **Isolation timer** (weather delay) | Help is far away | Can he last 30 minutes? |
| 5:26 | It has vanished from the balcony; Chen fears for other residents | Threat goes off-screen | It's hunting others | |
| 5:31 | Chen @'s everyone in the **owners' group chat**: dinosaur in 804, four dead, lock up | **Group-chat warning** | Neighbours will be saved | Will they believe him? |
| 5:39 | "Dinosaurs are extinct, what are you on about?" | **Group-chat disbelief** | | |
| 5:45 | Brother Liu: "804 is MY flat … how's my wife?" Chen: she's dead. Liu: you're lying, you two are acting because we fought yesterday | Victim's relative in denial; prank theory | | Who will check? |
| 6:01 | Liu is out of town; he offers 2,000 yuan to anyone who will check 804 | **Money bounty** pulls a volunteer into danger | Someone greedy will die | |
| 6:05 | Gao Xiang takes it ("send the money"); Chen DMs him not to go; Gao: "I'm a wilderness-survival expert" | Private DM vs public chat; overconfident volunteer | Gao is doomed | |
| 6:19 | Gao in the group: "there's no dinosaur here"; then a **livestream** in the chat: empty flat | Live video that shows nothing | Maybe it left the complex | Where is it? |
| 6:31 | Liu: knew it was a prank. Gao: "let me finish — her bloody clothes are on the balcony" | Delayed bad news | | |
| 6:39 | Group turns: "is there a killer in the complex? Chen, did YOU kill her and blame a dinosaur?" | **Suspicion flips onto the narrator** | The group is unfair; Chen is innocent | (On rewatch: almost right) |
| 6:48 | Chen: "Gao, is something behind you?" The dinosaur is behind him and swats him away | "Behind you" on livestream | "Now do you believe me?" | |
| 6:58 | Chen: police are 10 minutes out; stay inside, you'll be fine | Countdown update + new rule ("don't go out") | Safe if you stay in | |
| 7:03 | Gao (dead) calls Chen; the dinosaur's voice: "Dad, I'm coming to find you" | **Dead person's phone calls you**; mimic voice | It's coming for him specifically | |
| 7:13 | It has grown again and learned to climb; crawls along the balconies toward him | Ability escalation | The door is no longer a defence | |
| 7:21 | Chen runs out; police arrive; he sends them up; they shoot it | Fast resolution (one line) | It's over; Chen survived | Why so fast? (the twist is coming) |
| 7:32 | Wang Qiang: "did the police suspect you?" Chen: all smooth, CCTV proved the dinosaur did it, nothing to do with me. The director's dead, the zoo is ours; we breed more and rule the world | **Unreliable narrator / hidden conspirator reveal** | Chen and Wang engineered the night to kill the director and seize the zoo | Sequel hook: more dinosaurs |

## 4. Clue chain

| Clue (planted) | Where | Surface reading | Payoff |
|---|---|---|---|
| The director profits from the dinosaur | 0:01 | Background | Motive for the takeover; "the zoo is ours" (7:41) |
| Wang knows Chen's door is custom-made and can't be broken | 0:26 | Reassurance | They prepared the door in advance (a danmaku viewer spotted this at 0:39) |
| The dinosaur carries Chen's genes and calls him "Dad" | 0:07 / 0:46 | Absurd horror, explained by lab misconduct | It literally is his creature, so the "Dad" calls are sincere. A danmaku viewer at 464 s put it like this: "no wonder it calls him Dad, it was all an act" |
| Chen's performed anger and "settle it tomorrow" | 0:49 | Sincere fury | Staged; Wang is his partner (7:32) |
| The director refused to shoot when a visitor fell in | 1:02 | Shows the director's greed | Justifies blaming the director's choices later (4:54–5:01) |
| Chen locks his door on the neighbour; "I'm no saint"; tells the dying woman to "endure" | 1:33 / 2:19 | Selfish survival | First sign of the narrator's cruelty; makes the conspiracy believable |
| The neighbour's curse "you'll end up like me" | 2:22 | Prophecy of Chen's death | **Red herring.** Chen survives; the curse misdirects us into fearing for him |
| It grows after each meal (1.8 → 2.5 → 3+ m) | 2:28, 5:08, 7:16 | Escalating threat | Turns the kills into a ticking clock and justifies the police kill |
| Chen insists the director bring a rifle | 2:47–2:57 | Sensible advice | He uses it as the record of blame: "I warned you" (4:55). Makes the director's death look self-inflicted |
| Director: "treat it like a child … my money tree" | 2:52 / 3:19 | Greed | Paid off by "you deserve this" (4:54) |
| Wang calls: "have the director's people arrived?" | 3:24 | Concern | A timeline check by the co-conspirator |
| Wang knows the director brought only two keepers | 3:48 | Helpful tip | Insider info that steers Chen into refusing the door |
| 2 men + 400 kg + 8th floor = impossible | 4:05 | Logic puzzle | Proves the director lied |
| Xiao Zhang's ringtone sounds from next door | 4:20 | Proof of lie | The keepers are dead inside 804 |
| "You could just run downstairs" | 4:42 | Deduction that it's behind him | Confirmed when it kills him (5:03) |
| Snow blocks the roads | 5:18 | Isolation | Keeps police away until the director is dead and the dinosaur has done its damage |
| Group accuses Chen of killing the wife and framing the dinosaur | 6:41 | Unfair suspicion | **Dramatic irony.** He is guilty of something close to it |
| The dinosaur is shot by police, with CCTV as alibi | 7:30 / 7:37 | Resolution | Chen's alibi is clean; the "child" was disposable |

## 5. Twist inventory

| # | t | Twist | Type | Setup |
|---|---|---|---|---|
| 1 | 0:07 | The dinosaur talks and calls him Dad | Absurd premise hook | Title + knock; explained at 0:46 |
| 2 | 0:46 | His DNA is in it | Explanation reveal / complicity seed | Wang "confesses" under pressure |
| 3 | 1:33 | The hero locks the door on the begging neighbour | Expectation reversal (anti-hero) | Ordinary "save her" setup subverted |
| 4 | 1:41 | It opens a fingerprint lock with her hand | Creature-intelligence escalation | Genes reveal (smart like him) |
| 5 | 2:09 | The "dead" neighbour wakes and curses him | Fake death + false prophecy | Silence + "relieved" beat |
| 6 | 2:28 | It grows when it eats | Rule reveal (feeding = growth) | Explained at 3:07 (T-rex genes) |
| 7 | 3:44–4:27 | The director at the door is lying | **Trusted source contradicted** | Outside call + count clue + ringtone |
| 8 | 4:44–5:04 | The dinosaur is behind the director, coercing him | Deduction confirmed by death | "You could run downstairs" logic |
| 9 | 6:21–6:44 | Livestream shows no dinosaur, then blood; the group blames Chen | Suspicion flip | Group-chat disbelief at 5:39 |
| 10 | 6:52 | It's right behind the streamer | Jump-scare reveal | Empty-room livestream |
| 11 | 7:03 | A dead man's phone calls with the creature's voice | Mimic/phone escalation | It can talk + it took Gao |
| 12 | 7:18 | It can climb now | Ability escalation (the door is useless) | Growth rule |
| 13 | 7:32 | The narrator and Wang planned it to kill the director and take the zoo | **Unreliable narrator / hidden villain** | Clues at 0:26, 0:49, 1:33, 2:19, 2:47, 3:24, 3:48; motive at 0:01 |

The final twist is asserted more than earned: we never learn whether the escape itself was engineered or only exploited. Danmaku at 450–466 s mixes "I knew there'd be a twist" with confused "???". That is enough for a reaction spike. A tighter transposition should plant one clue that only the conspiracy explains.

## 6. GENERIC vs SPECIFIC

**GENERIC (genre conventions; free to use in our originals):**
- Night knock by something non-human that uses a familiar form of address or voice.
- Peephole checks rendered as a circular vignette insert.
- A neighbour who ignores the warning and is taken first.
- The narrator choosing self-preservation over a neighbour (dark-comic 沙雕 ethics).
- A threat that escalates by feeding, shown through a visible stat (size, count, speed).
- An authority figure (boss, landlord, officer) arrives, gives the wrong order, then turns up at the door alone asking to be let in.
- A third party phones to contradict the person at the door.
- A logistics or count clue that makes the visitor's story impossible.
- A phone ringing on the other side of a wall exposes a lie.
- "If you were free, you'd just leave, so something is holding you": deducing coercion.
- Police delayed by weather or blocked roads.
- Warning the residents' group chat, then disbelief ("X doesn't exist"), then a relative in denial.
- A cash bounty draws a cocky volunteer, who livestreams an empty room before "behind you".
- A dead person's phone calls you.
- The creature gains a new ability that defeats the safe room.
- Fast external resolution, then a last phone call revealing the narrator's true role (unreliable narrator).
- A greedy owner as the obvious antagonist and decoy.

**SPECIFIC (this author's expression; a transposed story must NOT reuse):**
- The premise combination: a **zoo-bred dinosaur with the narrator's spliced DNA that calls him "Dad"**.
- The cast and roles: Chen Jie; coworker Wang Qiang as secret partner; the zoo director with his "money tree" and "treat it like a child"; Sister Wang next door; her husband Brother Liu, away on a business trip, who thinks it's a prank after a marital fight; Gao Xiang the gold-chain "wilderness-survival expert"; keeper Xiao Zhang.
- Building 8, unit 804; the 800-yuan ticket sign; the 2,000-yuan bounty.
- The corpse's finger opening a fingerprint smart lock.
- Eating the neighbour on the balcony "so I would see", with the victim waking mid-meal to curse him.
- The size ladder (1.8 m → 2.5 m → 3 m+) and the T-rex-DNA explanation.
- The exact chain *rifle vs tranquilizer → director alone at door → only two keepers → 400 kg down 8 floors → keeper's ringtone next door → "it's a complex, not a prison" → "you deserve it"*.
- The dinosaur phoning from the dead streamer's phone with "Dad, I'm coming".
- The closing call "did the police suspect you / the zoo is ours / breed more and rule the world".
- Distinctive lines to avoid echoing in any language: "I'm no saint", "treat it like a child", "my money tree", "this is a housing complex, not a prison", "rule the world is within reach".

**Template note.** Danmaku at 78 s and 221 s say this is the studio's earlier black-bear/brown-bear door story re-skinned ("same plot again, just swapped a few things"). So 杰出影视 itself recycles a **siege skeleton**: creature at door → neighbour victim → authority at door lying → group chat → volunteer dies on stream → police → twist call. The skeleton is generic and reusable. The creature, the reason it targets the hero, the clue objects and the twist motive are what make each episode distinct, and those are the parts we must invent ourselves.

**Safe transposition moves** (for our writers):
- Replace the creature and its link to the narrator with a different bond.
- Swap the count clue for a different impossibility, such as timing, sound or weight.
- Use a different exposure device than a ringtone through a wall.
- Give the hidden-villain twist a motive that one planted clue alone explains.
- Keep the knock, the peephole, the lying authority, the group-chat disbelief and the livestream-behind-you mechanics.

## 7. Pacing

| Metric | Value |
|---|---|
| Caption lines | 311 over 7:47, so **40 lines/min**, about 1.5 s per caption, about 9.2 characters per line |
| Chinese characters | 2,867, so **about 370 chars/min** of narration plus dialogue |
| English equivalent | The mraevq dub covers the full script in 6:41 with 1,496 words, so **about 225 wpm**. That is just under the PLAYBOOK target of 230–270 wpm for narrated translated TikTok, which means the literal translation is shorter than the Chinese reading time. |
| Hook | Premise in 2 captions (0:00–0:02), knock at 0:05, creature speech at 0:07, "calls me Dad" at 0:14, phone call at 0:15. Four hooks inside 15 s. |
| Cuts | 96 scene changes (ffmpeg scene > 0.3), so about 12 cuts/min, about 4.9 s average shot. Many more "cuts" are the same set with a new caption. |
| Re-hook interval | I counted about 33 distinct turns (new threat, reveal or reversal) in 467 s, so **one every 14 s on average**. The longest stretch without a new threat is 2:38–3:13 (35 s of director-phone dialogue), and it still drops a reveal at 3:07 (T-rex genes). |
| Act shape | **Act 1 (0:00–1:11)**: premise, the "why Dad" loop, the greedy-boss setup. **Act 2a (1:13–2:37)**: neighbour victim, peephole, balcony kill, growth. **Act 2b (2:38–5:11)**: the authority arc, director at door, count clue, ringtone, coercion deduction, death. **Act 3 (5:12–7:31)**: isolation timer, group chat, bounty, livestream, phone call, climb, police. **Twist (7:32–7:47)**: a 15 s epilogue call. |
| Danmaku density (per 30 s) | 134 at 0–30 s (the hook, plus "省流" spoiler summaries of the twist posted at t=0 by returning viewers); 58 at 90–120 s (locking the neighbour out); 52 at 300–330 s (the director's death and the snow, plus plausibility arguments about jumping off the balcony); 44 at 450–467 s (the twist). The lowest is 10 at 240–270 s (the confession dialogue). |
| Cliffhanger / part-2 mechanics | No part 2; the ending is a sequel-bait villain win ("breed more"). There are natural split points for reposters who cut parts (udhwkz style): 2:24 (curse "you'll end up like me"), 3:46 ("Chen Jie, don't open the door!"), 5:04 (the director killed at the door) and 6:52 ("is something behind you?"). Each ends on a line, not on silence. |
| Engagement bait | Plausibility gaps viewers argue about: why not jump from the balcony, why didn't neighbours hear the roars, dinosaur DNA can't survive. These drive comment volume. |

## 8. Visual vocabulary

- **Art style.**
  - Flat 2D 沙雕 cartoon humans: oversized heads, thick outlines, cel shading.
  - The monster is a semi-realistic painted dark-brown theropod with red eyes and a pink mouth. Putting a realistic monster among cartoon people is part of the joke and the scare.
  - Gore is implied: the victim lies under the beast, and eating is screened behind balcony railings with a smudge or cloud.
- **Expressions** (a small reusable set, swapped per line):
  - Neutral wide eyes.
  - Pinprick pupils with white sclera (fear or shock).
  - Squint with a sneer (suspicion or contempt, used for Chen's cold lines).
  - Crying.
  - Open-mouth shout.
  - Characters barely move. Emotion comes from swapping the face, not from animation.
- **Costume coding.** Every character keeps one loud outfit so viewers can read who is speaking without names on screen:
  - Hero: neon-yellow jacket.
  - Coworker: red hair, white hoodie.
  - Director: black suit.
  - Husband: blond, red jacket.
  - Volunteer: tank top, gold chain, baton.
  - Neighbour: purple top.
  - Police: hi-vis "POLICE" vests.
- **Sets** (about 7, reused heavily):
  - Hero's entry hall: a door with a lever handle and peephole, and a red flower pot on a cabinet. This is the dominant set, roughly half the frames.
  - Zoo exterior: green mesh fence and a chalkboard "门票价 800元" sign. This is the "caller is at the zoo" location tag, in 41 of 467 frames.
  - Corridor with door plates 803/804.
  - Balcony with ornate railings and a giant full moon.
  - Bedroom.
  - The volunteer's living room: grey sofa with yellow and navy cushions.
  - Stairwell for the ending.
- **Phone language.**
  - **No phone-screen UI at all**: no chat bubbles, no call screens, no message overlays.
  - Calls are a character holding a phone to their ear in their own set, intercut with the listener.
  - The "owners' group chat" and the DM are characters holding phones up in their own rooms while narration says "@everyone" or "DM'd".
  - The livestream is the volunteer holding his phone out in the target flat.
  - Our horror kit's chat UI would be an *upgrade* over the source, not a copy of it.
- **Overlays.**
  - Circular peephole insert: grey vignette and a diagonal glass-glare streak.
  - Burned-in single-line white captions with a black outline, bottom centre, about 9 characters each.
  - Channel watermark top-right ("杰出影视本人 bilibili").
  - No timers, counters, rule cards or title cards on screen. Every number (size, weight, minutes, money) is spoken, never shown.
- **Camera.** Mostly static medium shots and two-shots; a cut every 4–5 s; occasional full-figure reveals of the monster behind or beside a character for "behind you" beats.
