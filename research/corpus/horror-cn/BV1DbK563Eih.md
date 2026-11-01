# BV1DbK563Eih: 诡夜红床 ("Red Bed on a Strange Night"): my roommate's red bed curtain, and the dorm supervisor says she isn't human

Internal research only. This file studies structure so we can write original, transposed stories. Do not translate, retell or remix this story for publication. See `SOURCES.md` for the rules.

## 1. Header

| Field | Value |
|---|---|
| URL | https://www.bilibili.com/video/BV1DbK563Eih |
| Title | 一口气看完《诡夜红床》：室友买了个红床帘，宿管看见后告诉我，我的室友不是人 ("All at once: [Red Bed on a Strange Night]: my roommate bought a red bed curtain, the dorm supervisor saw it and told me my roommate isn't human") |
| Channel | 夏哭有点怂 (Bilibili mid 3546890610150077). The first-person narrator is named 夏哭 (Xia Ku), the same as the channel, so the narrator is the channel's mascot. Upcoming-series trailers on the channel say "夏哭带你求生" ("Xia Ku takes you through survival"). |
| Uploaded | 2026-07-16. Tag: 悬疑 (suspense). |
| Views | 53,582 Bilibili plays (2026-11-01). 445 likes, 20 comments, 81 danmaku. |
| Duration | 13:35 (814.6 s). |
| Series structure | This upload compiles a 3-part series. Part 3 is [BV19CNX6nEWT](https://www.bilibili.com/video/BV19CNX6nEWT): 5:40, uploaded 2026-07-14, **2,081 views**. The compilation went up 2 days later and has **about 25x** Part 3's views. Part 3's length puts its start at about 7:55 here, right after the "should I go out?" cliffhanger. The 1/2 split is not confirmed; it is probably at about 3:45, the point where the English repost stops. The same channel repeats the pattern with 吓吓打墙: Part 1 got 2,843 views, while the "一口气看完" compilation got 54,361. **The single-sitting compilation is the format that performs.** |
| English reposts | mraevq TikTok [7670495663624408352](https://www.tiktok.com/@mraevq/video/7670495663624408352): **194K views**, 14K likes, 2:55, uploaded 2026-08-05, an 18x outlier for the channel. That is about 3.6x the Bilibili compilation's views. Annotated in `research/corpus/horror/7670495663624408352.md`. |
| Match evidence | Confirmed. The mraevq English transcript (`research/corpus/horror/raw/7670495663624408352.txt`) follows this video line by line from the hook ("My roommate bought bright red bed curtains") to the lightning-wood rule at 3:45, then stops. **The repost is Part 1 only**: 225 s of source in 175 s, so the TTS runs about 1.29x faster. Names are localized: Xiaoru becomes "Lily", Xia Ku becomes "Emma", and the pun-campus 吓大 becomes "Xiamen University" in the caption. Nothing in Part 1 is cut. The underlying text story also exists as several other Chinese readings. |

**How the data was gathered** (Spark CPU only, `nice -n 10`, `CUDA_VISIBLE_DEVICES=""`):
- **Video.** The 480p AVC stream (852x480, format 30032) is at `dgx-spark:~/studio/refs/horror-cn/BV1DbK563Eih/v30032.mp4`.
  - Video came through yt-dlp. Audio (30232) got HTTP 567 from the `mirrorcosov` CDN.
  - The fix was the known workaround: take the URL from `yt-dlp -g` and fetch it with curl, a Bilibili Referer header and the host swapped to `upos-sz-mirrorhw.bilivideo.com`.
- **Subtitles.** There are no auto-subs. The danmaku XML (81 comments) is saved as `a.danmaku.xml`.
- **Narration text.** It comes from **OCR of the burned-in captions**, at 3 fps on a 70 px crop of the bottom band (rapidocr, `~/studio/venvs/r2`, 2 threads).
  - Deduplicated, that gives **420 timed caption lines** (`captions_ocr.txt`). About 6 are OCR noise ("T", "Z", "H", "43").
  - The captions are the narration word for word. faster-whisper small (zh, CPU, 4 threads, `whisper_small.txt`, 587 segments) matches them throughout, apart from homophone errors such as 果实不 for 裹尸布 and 苏管 for 宿管.
- **On-screen text.** A full-frame OCR pass at 1 fps (`ocr_full.jsonl`) caught these:
  - The phone news screen (2:46 and 9:06).
  - The "lightning wood wards off evil" encyclopedia page (4:23).
  - The compass dial (8:46, 10:19).
  - A one-second compliance card at 0:21.
  - The "GIRLS DORMITORY" sign (9:09).
- **Images.** The contact sheets `sheet_0..3.jpg` (one frame every 6 s) and a UI grid `ui.jpg` are on the Spark.
- **Translation.** The English below is my own paraphrase. The mraevq transcript is a near-literal English rendering of 0:00–3:45.

## 2. Story outline (my summary)

**Part 1 (0:00–3:45).**
- **The setup.**
  - The narrator, Xia Ku, shares dorm 7-404 with Xiaoru. Xiaoru has hung a bright red curtain around her bunk.
  - The dorm supervisor (宿管阿姨, "the Aunt") goes white when she sees it. She says it is made from a burial shroud and the roommate is not a living person.
  - Rule 1: set your shoes by the bed, one facing forward and one backward, and ghosts can't get onto your bed.
- **The rule backfires.** Xia Ku does it and then can't find her own bed. She runs back to the Aunt and asks, half-joking, whether that means *she* isn't human. The Aunt says the ghost overheard them and cast an illusion. She hands over a packet of incense ash "offered before the Bodhisattva". Rule 2: tonight, whatever you hear, don't open your eyes.
- **The night.** Back in the room, the bed is there again.
  - At 11 pm Xiaoru gets out from behind her curtain, knocks three times on Xia Ku's bed frame and whispers that she knows Xia Ku is awake. Something has climbed onto her bed, Xiaoru says: open your eyes.
  - Xia Ku scoffs: dorm beds are singles, she'd notice. Then something wet and sticky licks her face.
  - Xiaoru explains that ghosts fear open eyes, because the gaze blocks them from stealing life force. Then she repeats the Aunt's private words back to her.
  - Xiaoru says the Aunt gave *her* "incense ash" two days ago too, and it was really the Aunt's dead daughter's cremated ashes. The Aunt is hunting for a **替身**, a replacement victim for her daughter. "Feel inside the packet for unburned bone."
  - Xia Ku opens her eyes and finds bone fragments. The licking stops.
- **The evidence and the new rule.**
  - Xiaoru shows a phone news story: a fire in dorm building 7, room 404, caused by a banned high-power appliance, killed a female student. The photo shows the Aunt kneeling and weeping.
  - The school gave the grieving mother the supervisor job, and she wants a replacement for her daughter.
  - Xiaoru's family are exorcists. Her red curtain is soaked in black-dog blood and repels evil. She meant to hide Xia Ku behind it tonight, but it's too late: half of Xia Ku's life force is gone.
  - Rule 3: break a branch from a lightning-struck tree on the campus back hill and put it under your pillow. The ghost will then go after someone else.

**Part 2 (3:45–7:54).**
- **The Aunt's counter-rule.**
  - Xia Ku brings back the branch. The Aunt is waiting at the door: "Did you open your eyes last night?"
  - Xia Ku accuses her of wanting a replacement for her daughter and threatens to call the police.
  - The Aunt shrugs ("life and death are fate"). Because Xia Ku is her daughter's age, she offers one hint: the five elements generate each other, so put a basin of water by the bed tonight.
  - Xia Ku checks online that lightning wood really does repel ghosts, and sets out the water anyway "as double insurance".
- **The fire.**
  - She wakes up burning: the bed is on fire. Xiaoru doesn't stir, "as if sleeping like the dead". The basin puts the fire out.
  - Xiaoru emerges and asks innocently what happened. Xia Ku concludes she was faking sleep and wanted her burned.
  - Then Xia Ku catches herself: why would a bed catch fire at all?
- **The Aunt's version.** Next morning the Aunt weeps: "again, again".
  - Her daughter did die in that room, but not from an appliance. The room's feng shui offends a fire ghost, and it catches fire every year. Nobody died until her daughter, who had a "light" birth chart, became the fire ghost's replacement and made the news.
  - She asked the school to close the room, and they agreed, but... Xia Ku cuts her off before she can finish.
  - Wood under the pillow feeds fire. And the back hill is too low to attract lightning, so the branch isn't lightning wood but **coffin wood**, heavy with yin.
  - Xia Ku now wonders how Xiaoru even knew about "lightning wood" on the back hill.
- **The verdict and Rule 4.**
  - The water only treated the symptom. The fire ghost has succeeded two nights running, so tonight Xia Ku dies.
  - She sobs and offers to become the Aunt's daughter and look after her in old age.
  - The Aunt relents. Rule 4: hide inside the red curtain tonight. The shroud masks a living person's scent. The ghost will try everything to lure her out, so whatever she sees or hears, she must not leave.
- **The night of the fire.**
  - Back in 404, Xiaoru is gone. At midnight Xia Ku climbs into Xiaoru's curtained bunk.
  - Footsteps and shouts of "Fire!" fill the hall. The Aunt bangs on the door: "Open up, run!"
  - The Aunt doesn't wait or plead; she moves on to the next door. Xia Ku reasons that a lure would try harder... unless the ghost understands psychology.
  - Smoke thickens. **Cliffhanger: should I go out?**

**Part 3 (7:54–13:35).**
- **The escape.**
  - Xia Ku decides being tricked to death beats burning in place, and runs.
  - Her phone buzzes with a text from an unknown number, two characters: "Go left." She follows it and gets out of the building.
- **The Taoist.**
  - An old Taoist with a compass is waiting outside: "Just in time." He sent the text to break the ghost's illusion. "The fire was fake, but the death trap is real."
  - He shows the same fire news story, but this photo has **one more person** next to the weeping Aunt: Xiaoru. **Xiaoru is the Aunt's dead daughter.** They do look alike.
  - Xia Ku re-reads everything: the Aunt sent her into Xiaoru's curtain and Xiaoru vanished. Mother and daughter were working as a team.
- **The identity twist.**
  - Xia Ku was also in the room during the real fire and escaped. The mother couldn't bear that her own daughter died and this girl didn't. She trapped Xia Ku's living soul (生魂) in an illusion of the dorm and hid part of her memories, so that Xiaoru could be reborn in Xia Ku's body.
  - Xia Ku can't remember her old life. She has to get back to her body before Xiaoru takes it.
  - The compass needle will stop at the "life gate".
- **Xiaoru's version.**
  - The spinning compass leads her straight back to room 404. Xiaoru leans out of the red curtain: "you came back after all."
  - Xia Ku assumes the Taoist and Xiaoru are allies, braces for death and dares them to finish it.
  - Xiaoru breaks down instead. Yes, her mother wants to trade Xia Ku's life for hers, but Xiaoru refuses: stealing a replacement defies heaven, and her mother would die violently and never be reborn. "I want to live, but I want my mom to live more."
  - The Taoist is a fraud, she says. The real exit is the "lightning wood" spot she sent Xia Ku to: kowtow there three times, last until dawn, and you'll wake.
- **The Aunt's version again.**
  - Xia Ku goes to the Aunt. Xiaoru *was* her daughter, the Aunt says, but she's a fire ghost now, and that spot is her coffin wood. Kowtowing there means volunteering as prey.
  - If Xia Ku had stayed in the curtain she would have survived to the "soul-return hour". Now both the curtain and the hill mean death.
- **The deduction.** If the Aunt is a living person, she must also be a living soul in this space. So how does *she* get out?
  - The Aunt fetches a Bodhisattva statue: "this is our life gate". At midnight a door will appear; wait here and don't let anyone destroy it.
  - She'll go and "finish it" with her daughter.
- **The ending.**
  - At midnight the statue turns red-hot and Xia Ku drops it. A door appears; the Aunt didn't lie.
  - As Xia Ku opens it, the Aunt calls from the end of the corridor, "Wait for me!" Xiaoru is right behind her.
  - Afraid Xiaoru will stop her, Xia Ku says "Aunt, I'm sorry" and **shuts the door on both of them**. End. Nothing resolves who was telling the truth.

## 3. Beat table

Timestamps are from the Bilibili video. "Mechanic" uses the corpus device names where they fit. "Authority" marks whom the narrator currently trusts. The authority carousel is the engine of this story.

| t | Beat | Mechanic | What the viewer believes now | Open loops |
|---|---|---|---|---|
| 0:00 | Roommate hung a bright red bed curtain; the Aunt goes pale | Cold-open object + authority reaction (2 captions) | Something is wrong with the curtain | What's wrong with red? |
| 0:04 | "That curtain is a burial shroud. Your roommate isn't alive" | **Fake authority** names the monster (title payoff at 4 s) | The roommate is a ghost | Is she? |
| 0:08 | Rule 1: shoes one forward, one backward, by the bed | **Rule list**, item 1 | Following the rule = safe | |
| 0:19 | Narrator can't find her own bed | Rule backfires on the rule-follower | Something is off | Why her? |
| 0:25 | "Why am *I* the one who can't find the bed? Am I not human?" | Joke-line that is actually the **biggest planted clue** | A throwaway gag | (Answered at 9:52) |
| 0:31 | Aunt: the ghost overheard us and blinded you first | Authority explains away the anomaly (**wrong detail covered**) | The Aunt is still credible | |
| 0:40 | Paper packet of incense ash "offered before the Bodhisattva" | Protective object handed over | The ash is protection | |
| 0:47 | Rule 2: whatever you hear tonight, don't open your eyes | Rule list, item 2 + withheld info ("you'll find out") | Eyes shut = safe | **What will I hear?** (restated 3x) |
| 0:57 | Bed is back: "the ash works" | False relief | The Aunt was right | |
| 1:09 | 11 pm, curtain rustles, Xiaoru gets up, footsteps, **three knocks on the bed frame** | Night ritual; sound-only scare | The roommate-ghost is coming | |
| 1:24 | "Xia Ku, are you asleep?"; narrator keeps eyes shut | Name-calling in the dark (a lure) | Xiaoru is the ghost | |
| 1:34 | "I know you're awake. Open your eyes, something's on your bed" | **Contradictory order** (open vs. keep shut) | Classic lure; ignore it | |
| 1:39 | Narrator: "beds are singles, I'd notice" | Rational pushback (comic) | | |
| 1:45 | Wet, sticky licking on her face | Physical sensation scare | Something IS on the bed | Who's lying? |
| 1:54 | Xiaoru: "ghosts fear open eyes; your gaze stops them stealing your yang" | **Rule inversion**: same rule, opposite meaning | | |
| 2:01 | Narrator: how does Xiaoru know what the Aunt told me in private? | Knowledge leak as a red flag | Xiaoru is sinister | |
| 2:05 | Xiaoru: the Aunt gave me the same ash; it's her daughter's ashes; she wants a replacement | **Trusted source contradicted** (authority handoff #1: Aunt to Xiaoru) | The Aunt is the villain | |
| 2:18 | "Feel inside, there's unburned bone" | **Touch test**: a physical check the viewer can follow | | |
| 2:23 | Eyes open, bone found, the licking stops | Proof + rule confirmed in the new direction | Xiaoru is the ally | |
| 2:42 | Phone news: building 7, room 404 fire killed a female student; photo of the Aunt weeping | **Phone evidence screen** + **room-number match** | We live in the death room | |
| 3:03 | Motive: grieving mother given the job; wants a replacement | Villain motive explained | | |
| 3:11 | Xiaoru's family are exorcists; curtain soaked in black-dog blood | Re-reads the hook object as protective | The red curtain is good | |
| 3:24 | "Can I have a curtain too?" "Too late: half your yang is gone" | **Stakes timer** (resource half-drained) | Clock is ticking | |
| 3:33 | Rule 3: lightning-struck branch from the back hill under the pillow; "it will go find someone else" | New rule from the new authority (mirrors Rule 1's cadence) | Branch = safe | Is Xiaoru the next fake authority? **[Probable Part 1 end; the repost stops here]** |
| 3:45 | Narrator fetches the branch; the Aunt blocks the door: "Did you open your eyes last night?" | Authority knows too much | The Aunt is guilty | |
| 4:00 | Narrator accuses her; threatens police | Confrontation | | |
| 4:08 | Aunt: "life and death are fate"; one hint: five elements, basin of water by the bed | **Cryptic counter-rule** from the discredited authority | Possibly a trick | Why water? |
| 4:22 | Online search confirms lightning wood repels ghosts (encyclopedia page on screen) | Outside verification (seems to settle it) | Xiaoru is honest | |
| 4:28 | "Is she playing hard to get?" Puts the water out anyway as double insurance | Hedging (the viewer agrees) | | |
| 4:39 | Wakes burning; bed on fire | Escalation: physical danger | | |
| 4:46 | Xiaoru won't wake, "sleeping like the dead" | Wordplay clue (literally dead) | Xiaoru wants her dead | |
| 4:51 | Water puts it out; Xiaoru emerges innocently | The Aunt's rule saves her | **Doubt swings back to the Aunt** | |
| 5:13 | "Wait: why would my bed catch fire?" | Self-question re-hook | | Cause of fire? |
| 5:18 | Morning; "you knew there'd be a fire"; the Aunt cries "again, again" | Authority handoff #2 (Xiaoru to Aunt) | | |
| 5:34 | Real story: fire ghost, bad feng shui, a fire every year, the daughter became its replacement | Re-explains the news article (same evidence, new reading) | The Aunt is a victim | |
| 5:59 | "I told the school this room can't be lived in... they agreed, but..." **cut off by the narrator** | Interrupted line (**withheld clue**) | | Why is it still open? (Answered at 9:55: it's an illusion) |
| 6:10 | Wood under the pillow feeds fire (five elements) | Rule logic paid off | | |
| 6:20 | "Did you get it from the back hill? It's too low for lightning, so it's **coffin wood**" | **Logic clue** (wrong detail exposed: height) | Xiaoru lied | |
| 6:37 | "How did Xiaoru know there was lightning wood there?" | Knowledge-leak red flag, mirroring 2:01 | | |
| 6:45 | "Tonight is your death date" | Deadline | | Will she live? |
| 6:53 | Narrator begs, offers to be her daughter | Emotional low point; ironic, since the Aunt wants exactly that | | |
| 7:01 | Rule 4: hide in the red curtain; the shroud hides your living scent; don't come out whatever you see or hear | Rule list, item 4. **The hook object flips meaning again.** | The curtain is safety | |
| 7:26 | Back in 404: Xiaoru has vanished | Absence clue | | Where is she? |
| 7:31 | Midnight, climbs into Xiaoru's curtain; first half of the night quiet | False calm | | |
| 7:37 | Footsteps; "Run! Fire!"; the Aunt knocks: "Open the door!" | **Trusted voice at the door** + emergency (real or lure?) | | |
| 7:56 | The Aunt doesn't plead, moves to the next door | **Behaviour test**: a lure would focus on her | Probably real... | |
| 8:11 | "Unless the ghost understands psychology" | Double-think | | |
| 8:16 | Smoke thickens; "better tricked to death than burned lying still" | Forced choice; she **breaks the rule** | **[Part 3 starts about here]** | |
| 8:28 | Phone: text from an unknown number, two characters: "Go left" | **Anonymous text / burner instruction** | Someone is helping | Who? |
| 8:43 | Old Taoist with a compass at the entrance: "just in time" | New authority (#3) | Rescue | |
| 9:02 | "The fire was fake, but the death trap is real" | Reversal line (re-hook) | | |
| 9:04 | Same news article, but **one extra person** in the photo: Xiaoru | **Count clue** in a doubled artifact | | |
| 9:15 | Xiaoru is the Aunt's daughter; they look alike | Identity reveal | Both are villains | |
| 9:22 | Re-reads: the Aunt said to hide in the curtain, then Xiaoru vanished; a double act | Replay of earlier beats | | |
| 9:36 | You were in the fire too and escaped; envy: "why my daughter?" | Motive deepens | | |
| 9:48 | Your living soul is trapped in an illusion; memories hidden; Xiaoru wants your body | **"You are the ghost" twist** (pays off 0:25 and 5:59) | The narrator isn't fully alive | How to get out? |
| 10:18 | The compass needle will stop at the life gate | New rule from the new authority | | |
| 10:25 | The compass leads her back to 404; Xiaoru in the red curtain: "you came back" | Betrayal fake-out | The Taoist is in league | |
| 10:42 | Narrator defiant: "do your worst" | Resignation beat (comic bravado) | | |
| 10:53 | Xiaoru cries: "if I wanted to hurt you I'd have done it; I stopped my mom" | Authority handoff #4 (Taoist to Xiaoru); **sympathetic-ghost reversal** | Xiaoru is good | |
| 11:14 | "I want to live, but I want my mom to live more"; heavenly punishment if the mother succeeds | Moral stakes | | |
| 11:31 | "The Taoist is a liar"; exit = kowtow 3 times at the lightning-wood spot, last until dawn | Competing exit #2 | | Which exit? |
| 11:45 | Narrator doubts; goes to the Aunt | The narrator becomes the investigator | | |
| 11:57 | Aunt: Xiaoru *is* a fire ghost now; kowtowing there = volunteering as prey; now both options mean death | Authority handoff #5 (Xiaoru to Aunt); **no-win board** | | |
| 12:23 | Deduction: the Aunt is alive too, so she's also a soul here; how does SHE leave? | **Narrator outthinks the authorities** | | |
| 12:42 | The Aunt brings a Bodhisattva statue: "our life gate", appears at midnight; she'll "finish it" with her daughter | Competing exit #3; callback to the "Bodhisattva" ash | The Aunt is the honest one? | Is it a trap? |
| 13:01 | Midnight: the statue turns red-hot; a door appears | Rule paid off (the Aunt didn't lie) | Escape is real | |
| 13:14 | The Aunt shouts "wait for me"; Xiaoru right behind her | **Pursuer + ally ambiguity** in one shot | | Is the Aunt fleeing Xiaoru or bringing her? |
| 13:21 | "I can't die. Aunt, I'm sorry." **Shuts the door.** | **Selfish-survival ending** | The narrator saved herself at someone's cost | Who lied? Was the door real? What happens to the Aunt? |

## 4. Clue chain

| Clue (planted) | Where | Surface reading | Payoff |
|---|---|---|---|
| The rule meant to stop ghosts reaching the bed stops *her* | 0:19–0:28 ("am I not human?") | Ghost illusion, a gag | She is a disembodied living soul (9:48). The best-planted clue in the video. |
| The Aunt's private words repeated by Xiaoru | 2:01 | Xiaoru is spying | Xiaoru got the same treatment; later, mother and daughter are a team (9:22) |
| Incense ash from "before the Bodhisattva" | 0:43 | Protection | Bone fragments = the daughter's ashes (2:26). The Bodhisattva returns as the statue/door (12:42). |
| The red curtain as shroud | 0:04 | Evil object | Re-read three times: protective (3:16), a scent-mask hiding place (7:03), Xiaoru's lair (10:30) |
| News article, building 7 room 404 | 2:46 | A dead girl and a grieving mother | Same article with an extra face, Xiaoru (9:08) |
| Visual-only: Xiaoru's black nails, pure-black eyes, chalk-white skin, face cut off above the lips | 2:45 onward | Style | She's dead (9:15). Danmaku at 171–193 s spotted all three. |
| Xiaoru and the Aunt look alike | Never pointed out until 9:19 | Same art style | Mother and daughter (9:19); a fair-play visual clue |
| "Five elements generate each other" | 4:16 | Cryptic folk wisdom | Wood feeds fire (6:13); water saves her (4:54) |
| Online search confirms lightning wood works | 4:22 | Settles Xiaoru's honesty | Misdirection: the object was never lightning wood (6:20) |
| Back hill too low for lightning | 6:26 | Logic | Exposes Xiaoru's object as coffin wood |
| Xiaoru "sleeps like the dead" during the fire | 4:46 | Faking sleep | Literally dead |
| The Aunt's interrupted "the school agreed to close the room, but..." | 5:59–6:05 | Rambling | The room shouldn't be in use, so it's an illusion (9:55) |
| A fire every year in this room | 5:46 | Feng-shui lore | Sets up the fire night (7:39), which is "fake fire, real trap" (9:02) |
| Xiaoru vanishes right after the Aunt sends Xia Ku to her curtain | 7:26 | Odd | Read as a double act (9:22), then re-read as Xiaoru protecting her (10:57) |
| The Aunt moves on to other doors instead of pleading | 7:56 | Real-emergency tell | Ambiguous; the fire turns out to be an illusion |
| Midnight | 7:29, 12:48 | Ritual hour | The door appears at 13:01 |
| The narrator offers to "be your daughter" | 6:55 | Desperation | Dramatic irony: the Aunt literally wants her body for her daughter (9:57) |
| The narrator's memory gaps | Implied: she never mentions her own past | Not noticed | "Part of your memory was hidden" (9:50) |

**Unpaid or contradictory threads.** The comment section argues about these, and some are probably deliberate.
- Who licked her face on night 1, if Xiaoru was by the bed talking?
- Why did the Aunt's water save her if the Aunt is the villain?
- Why does the Aunt's Bodhisattva door work, if the Aunt trapped her?
- Is the Taoist honest? His compass led her back to Xiaoru.

Danmaku at 703 s asks "so who's actually telling the truth?" and at 739 s "so many reversals, layer inside layer". The final reading is left to the viewer.

## 5. Twist inventory

| # | t | Twist | Type | Setup |
|---|---|---|---|---|
| 1 | 0:04 | The roommate isn't alive | Premise reveal by an authority | Hook object (red curtain) |
| 2 | 0:19 | The protective rule makes *her* lose her bed | Rule backfire / identity hint | Rule 1 at 0:10 |
| 3 | 1:45 | Something IS on the bed | Sensation scare confirming the "lie" | Narrator's "beds are singles" scoff |
| 4 | 2:05 | The authority's talisman is her dead daughter's ashes | **Fake authority + wrong detail** (protective object is the opposite) | Ash packet at 0:43; knowledge leak at 2:01 |
| 5 | 2:42 | We live in the room where the girl died | Location match via phone news | Room number given only now |
| 6 | 3:11 | The red curtain is protection | Hook-object inversion | Shroud claim at 0:04 |
| 7 | 4:39 | Following the ally's rule sets her bed on fire | Rule backfire #2 | Lightning wood at 3:36; five-elements hint at 4:16 |
| 8 | 5:34 | The death was a fire ghost, not an appliance | Same evidence, new reading | Article at 2:46 |
| 9 | 6:20 | The "lightning wood" is coffin wood | **Wrong detail exposed by logic** (hill height) | Back hill named at 3:34 |
| 10 | 7:01 | Hide in the curtain the Aunt called a shroud | Authority reverses her own rule | Twists 1 and 6 |
| 11 | 9:02 | The fire was an illusion | Reality reversal | Fire every year (5:46); smoke but no flames shown on the escape |
| 12 | 9:08 | The photo has an extra person: Xiaoru | **Count clue** / doubled artifact | Same article at 2:46 with only the Aunt |
| 13 | 9:15 | Xiaoru is the Aunt's daughter | Identity reveal; two "rival" authorities were family | Resemblance; vanishing at 7:26 |
| 14 | 9:48 | The narrator is a trapped living soul | **"You're the ghost"** (unreliable-self) | Lost bed at 0:25; interrupted closure line at 5:59 |
| 15 | 10:53 | The ghost daughter is protecting her | Sympathetic-monster reversal | "If I wanted to hurt you..." |
| 16 | 11:31 | The Taoist is a liar (per Xiaoru) | Trusted source contradicted (third time) | The compass led her back to 404 |
| 17 | 12:23 | The Aunt is a living soul too, so she knows the way out | **Narrator's own deduction** | "You're a soul" logic applied to the Aunt |
| 18 | 13:01 | The Bodhisattva door is real | Payoff of the Aunt's rule | Bodhisattva callback |
| 19 | 13:21 | The narrator shuts the door on the Aunt | **Selfish-survival reversal** (anti-hero) | Begging and fear of death at 6:53; "I want to live" |

Nineteen twists in 815 s is about one every 43 s. Twists 4–14 are tightly linked. Twists 15–19 pile reversal on reversal without one replay clue that settles the truth, and that ambiguity is what the comments run on.

## 6. GENERIC vs SPECIFIC

**GENERIC (genre conventions; free to use in our originals):**
- A building supervisor or caretaker as the rule-giver; the shared-room setting (dorm, bunkhouse, hostel, ward).
- A roommate flagged as "not human" by an authority in the first 5 seconds.
- **Rules that backfire on the rule-follower**, where each backfire seeds the identity twist.
- **The authority carousel**: two or three rival advisers, each discrediting the last with one piece of evidence. The narrator's trust swings about every 2 minutes.
- A protective object that is secretly the opposite (talisman = remains, blessing = curse), checked by touch.
- The same rule given with opposite meanings by rival advisers (eyes shut vs. eyes open).
- A knowledge leak ("how do you know what she told me?") as a red flag.
- Phone news article as outside evidence with a room-number match, re-read later; a **second copy of the evidence with one extra detail** (extra person, extra line).
- Folk-cosmology logic as a rule system (five elements, yin/yang, midnight) to make rules feel deducible.
- A "fact" exposed by physical logic (height, distance, weight, timing).
- An interrupted sentence that hides a key fact.
- A night emergency with a trusted voice at the door, plus a **behaviour test** ("a lure would try harder").
- An anonymous text with a one-word instruction.
- A third authority with a ritual instrument who explains "it's all an illusion".
- **"You are the ghost / you're the one trapped"**, set up by an early anomaly played as a joke.
- The replacement (替身) motive: someone must die in your place.
- A sympathetic monster who protects you against her own family.
- Several competing exits from several advisers, then the narrator deduces which adviser shares her situation.
- A selfish last act (shutting the door, leaving someone behind) with an unresolved who-lied ending.
- A cliffhanger at a door decision for the part break.

**SPECIFIC (this author's expression; a transposed story must NOT reuse):**
- Names and world: Xia Ku (the channel's mascot narrator) and Xiaoru; the dorm supervisor and her dead daughter; the old Taoist. The pun-world 吓大 / 吓哭市 / 吓哭新闻社 ("Scare University / Scare-Cry City / Scare-Cry News"). Building 7, room 404; the date "2024-07-01, midnight".
- The **red bed curtain** made of burial shroud and soaked in black-dog blood as the central object, flipping evil → protective → hiding place → lair.
- The exact rules: shoes one forward, one backward; ash "offered before the Bodhisattva" that is the daughter's cremated ash, with unburned bone; eyes shut vs. eyes open as gaze protecting yang; lightning wood from the back hill that is really coffin wood because the hill is too low; a basin of water via the five elements; kowtow three times and last until dawn; the compass whose needle stops at the life gate; the Bodhisattva statue turning red-hot into a door at midnight.
- The licking sensation on the face while a roommate whispers "open your eyes".
- The fire-ghost feng-shui backstory (fires every year; the daughter's "light" birth chart).
- The two-character text "Go left" from the Taoist.
- The news photo gaining the daughter's face.
- The survivor-envy motive: the mother traps the survivor of *the same fire* to give her body to the dead daughter.
- The daughter refusing out of love for her mother (heavenly punishment).
- The closing beat: the narrator shuts the door on the Aunt and her daughter.
- Distinctive lines to avoid echoing in any language:
  - "骗人也要讲基本法" (even liars need basic rules)
  - "火是假的，但死局却是真的" (the fire was fake, the death trap real)
  - "杀人不过头点地" (killing is just a nod of the head)
  - "阿姨，我以后给你当女儿" (I'll be your daughter)
  - "我想活，可我更想要我妈活下去"
  - "阿姨对不起"

**Safe transposition moves** (for our writers):
- Keep the **carousel engine**: three advisers, each with one rule, one piece of evidence and one discrediting detail about the last. Change the setting (night-shift hospital ward, cruise-ship crew cabin, summer-camp cabin, remote research station).
- Replace the protective-object reversal with a different object and test (a scent, a key card, a recording) and a different physical check.
- Keep "the first rule backfires on *you*" as the identity seed, but make the identity twist something other than a trapped living soul (for example: you're the replacement, you're the one already counted, you're the one on the old roster).
- Use a doubled artifact with a different change (a timestamp that moves, a headcount in a group photo, a name missing from a list) and a different outside channel than a news app.
- Give the ending a **single replay clue** that settles who lied. This source's ambiguity costs it clarity; the dinosaur study (`BV1fR7szYEDq.md`) reached the same conclusion from the other direction.
- Keep the selfish-door ending only if the motive differs. Avoid closing on a shut door after an "I'm sorry".

## 7. Pacing

| Metric | Value |
|---|---|
| Caption lines | 414 real lines over 13:35, so **30.5 lines/min**, about 2.0 s per caption, about 10.7 characters per line |
| Chinese characters | 4,445 Han characters, so **about 327 chars/min**. That is slower than the 杰出影视 dinosaur study (370). The read is calmer and more anime-drama than 沙雕. |
| English equivalent | The mraevq dub of Part 1 runs about 207 wpm (604 words over 2:55, covering 3:45 of source). That is 1.29x compression with nothing cut, so the Chinese reading time is longer than a literal English translation. **The full 13:35 would land at about 10.5 min, about 2,200 English words.** |
| Hook | Object (0:00), authority reaction (0:02), "it's a shroud" (0:04), "your roommate isn't alive" (0:06), rule 1 (0:08), the rule backfires (0:19). **Four hooks inside 8 s** and a backfire by 20 s. |
| Cuts | About 147 scene changes (ffmpeg scene > 0.3), so about **10.8 cuts/min**, about 5.5 s average shot. Many more visual changes are expression swaps on a held shot. |
| Re-hook interval | The beat table has 69 rows; about 45 are genuine turns (a new threat, reveal, rule or reversal), so **one every 18 s** on average. Twists alone (19) come every 43 s. The longest stretch without a new turn is 9:36–10:18 (42 s of the Taoist's exposition), which still contains the "you're a trapped soul" reveal. |
| Authority handoffs | Aunt (0:02) → Xiaoru (2:05) → Aunt (5:18) → Taoist (8:43) → Xiaoru (10:53) → Aunt (11:57) → narrator's own deduction (12:23). That is **6 handoffs, about every 2 min**. Each handoff carries one piece of evidence that discredits the previous adviser. |
| Act shape | **Part 1 (0:00–3:45, 28%)**: rules → night ordeal → ally reversal → new rule. **Part 2 (3:45–7:54, 31%)**: counter-rule → fire → re-reversal (coffin wood) → curtain rule → door dilemma. **Part 3 (7:54–13:35, 42%)**: SMS escape → Taoist → identity twist → ghost's plea → counter-plea → deduction → door. |
| Cliffhanger / part-2 mechanics | Each part ends on a decision or rule, not a death. Part 1 ends on the new ally issuing a rule ("it will go find someone else"), so the question is whether she's the next fake authority. Part 2 ends on "should I go out?", with fire alarm vs. the rule. Part 3 ends on the door shutting, with no resolution. The episodic parts got about 2–3K views each; the compilation got 53.6K and the Part-1-only English repost got 194K. **For us: publish the self-contained 2:30–3:00 "Part 1" unit, ending on a new-rule cliffhanger, as the primary short.** |
| Danmaku density (per 30 s) | 81 total, so sparse. Peak **11 at 210–240 s** (Xiaoru's exorcist reveal, with viewers flagging her black eyes, white skin and black nails: "can you trust a roommate who looks like that?"). Then 8 at 180–210 s, 7 at 150–180 s ("an actual reversal"), and 7 at 390–420 s ("why not just change dorms?"). Late comments are few but on-topic: "reversal" (570 s), "surely the Taoist isn't bad too?" (638 s), "I guessed right" (695 s), "who's telling the truth?" (703 s), "layer inside layer" (739 s). |
| Engagement bait | Plausibility gaps viewers argue about: why not change dorms or report it; why is the narrator still in the room; who to trust. The "who lied?" ending is the main comment driver. Likes are low (0.8% of views). |

## 8. Visual vocabulary

- **Art style.**
  - Semi-realistic anime / webtoon 2D: slim proportions, clean lines, muted cel shading. This is **not** the big-head 沙雕 style.
  - Desaturated blue-grey and teal palette. **Red is reserved for the curtain**, the only saturated colour, apart from the fire's orange.
  - Heavy corner vignettes in nearly every shot, a peephole-like dark ring.
  - Gore: none. The fire is an orange flame overlay on the bed shot. The "death" is never shown.
- **Expressions** (a small swap set):
  - Wide eyes with pinprick pupils and a dark band of shadow across the eyes (dread). This is the narrator's default.
  - Sweat drops.
  - Gritted-teeth anger.
  - Open-mouth sobbing.
  - A rotated 90° sideways face close-up for "lying in bed with eyes shut".
  - Xiaoru: chalk-white skin, pure-black eyes or a face cropped above the lips, black nails. These are visual-only tells the comments pick up.
  - The Aunt: sunken eyes and teary close-ups.
  - Characters barely move. Emotion comes from swapping faces and from push-ins.
- **Costume coding** (one outfit per character):
  - Narrator: grey T-shirt with a cat print, ponytail.
  - Xiaoru: cream sweater, long dark hair.
  - The Aunt: dark-green cardigan, grey shirt, staff ID on a lanyard.
  - Taoist: yellow robe with a bagua trigram on the chest, a striped hat, a wooden sword with red tassels, and a compass.
- **Sets** (about 6, reused heavily):
  - Dorm 404 with bunk beds, desks, a bookshelf and the red curtain. This is the dominant set.
  - Dorm doorway or corridor with the Aunt framed by the door and a barred window.
  - Night exterior at the building entrance under a street lamp, for the Taoist.
  - A burned "GIRLS DORMITORY" entrance with a sheet-covered body and the kneeling Aunt, as the news photo.
  - A long dark corridor with a glowing door for the ending.
- **Phone language.**
  - **The phone screen is held up to camera** in a hand: a news-app article ("吓哭新闻" masthead, headline, date line, photo, outlet credit).
  - The narrator's own lookup appears as a white encyclopedia card ("雷击木可以辟邪" with an entry body).
  - The SMS beat is the narrator gripping a phone over a **purple background with manga radial speed lines**, the shock frame held for about 10 s across the SMS beat.
  - No chat bubbles, no group chat, no call screens.
  - Our horror kit's chat and SMS UI would be an upgrade over the source here, not a copy of it.
- **Overlays.**
  - Burned-in single-line white captions with a black outline, bottom centre, about 11 characters each.
  - A persistent top-left watermark "纯属虚构，请勿模仿" ("pure fiction, do not imitate").
  - A **one-second compliance card at 0:21** (观前提醒): "contains horror elements … the whole film follows scientific values, involves no ghosts or superstition; fear comes from the contest between human nature and crime … all fictional". This is the platform-safety boilerplate that lets Chinese uploaders publish ghost content.
  - A full-frame compass-dial insert (8:46, 10:19), described as "spinning like an eyeball".
  - Flame overlays. A Bodhisattva statue glowing red.
  - No timers, counters or rule cards. Every rule and deadline is spoken, never shown.
- **Camera.**
  - Static medium shots and over-the-shoulder two-shots, with the listener as a blurred dark shoulder in the right foreground. That shoulder framing is used for nearly every dialogue scene.
  - Slow push-ins on reveals.
  - Silhouette shots of Xiaoru behind the red curtain for menace.
