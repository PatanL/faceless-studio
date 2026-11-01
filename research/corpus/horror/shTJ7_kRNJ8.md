# If Everyone On The Night Bus Stands Up At Your Stop... STAY SEATED: NightProtocol (annotated)

| Field | Value |
|---|---|
| URL | https://www.youtube.com/watch?v=shTJ7_kRNJ8 |
| Title | If Everyone On The Night Bus Stands Up At Your Stop... STAY SEATED |
| Channel | NightProtocol (229 subscribers; median of all 15 uploads on the Videos tab: 422 views) |
| Views | 3,201 at collection, **1 day after upload** (22 likes), so the count is still rising |
| Outlier score | **7.59** (views divided by the channel median) |
| Duration | 633 s (10:33). Speech runs 0:00 to about 10:31 |
| Uploaded | 2026-10-31 |
| Format | 16:9 1920×1080 YouTube long-form "If X... STAY Y" **second-person rules story**. One synthetic narrator over AI-style stills (per the collection note; there is no contact sheet for this video, so the visuals are not verified here). YouTube chapters: The last bus home 0:00 · File 015 1:36 · Rule 1 1:41 · Rule 2 2:56 · Rule 3 4:04 · Rule 4 5:21 · Rule 5 6:23 · Rule 6 7:26 · Rule 7 8:39 · The next morning 9:52. A numbered-series brand ("Night Protocol file 015") |
| Total words | **1,861** (yt-dlp en-orig auto-subs, cleaned with `tools/vtt2lines.py`; not cross-checked with whisper) |
| Words/min | **176 wpm** over 633 s. Per 60 s window: 186 · 152 · 183 · 168 · 172 · 174 · 183 · 187 · 179 · 183 · 94 (last 33 s ≈ 171 wpm). Very flat: the only slow stretch is 1:00–2:00 (152), where the stand-up scene and the title card leave short pauses. Each rule chapter runs 168–189 wpm |
| Sentences | 211, **median 7 words**. Lots of 2–5-word fragments ("Look at the floor." "Keep counting.") |
| Second person | 116 uses of you/your/you'll etc. (**6.2%** of words, from the very first word). The viewer is the protagonist throughout, and a named friend (Sammy) is the stake |
| Prohibitions | 25 uses of "don't / do not / never". **7 numbered rules**, each a YouTube chapter |
| Numbers | 51 numbers or number words (≈4.8/min): stop counts, seconds, years, file number, floor, closing time, "41 times / 12 stops" |

Sources: `raw/shTJ7_kRNJ8.txt` (VTT cue starts, rolling duplicates removed), metadata `dgx-spark:~/studio/refs/corpus_horror/x2/meta/shTJ7_kRNJ8.json` (chapters, tags, description). No video was downloaded and no sheets were made, so this file has **no Visual column**. Lines are quoted verbatim **for internal research only**. Never reuse the wording, the night-bus premise, the rules, the "Sammy" friend or the channel's "protocol file" identity.

Auto-sub errors worth knowing about (the meaning is clear from context):
- The friend is spelled both "Sammy" (9×) and "Sami" (2×). Same character.
- 5:54 "and they'll smile. A man reported this in 2022." The cue boundary splits the sting from the next anecdote. Two sentences.
- 6:21 "Come on, stay in your seat." The two mouthed words are "Come on"; "stay in your seat" is the narrator's order.
- 7:05 "away herself / standing at the empty stop waving" = "as the bus pulled away: herself, standing at the empty stop, waving".
- 8:45 "the lights will flicker on all of them for the first time" most likely means the aisle lights all come on at once for the first time (closing the 0:49 flickering-light plant).

**Key mechanic:** a **survival manual in the second person, wrapped around a one-night story**. The cold open states the premise as a rule list in 15 s, then a 70 s scene puts "you" and a friend on the bus and triggers the event, and then **seven numbered rules** walk through the rest of the ride in chronological order. Each rule is a ~63–75 s chapter with the same anatomy: header → why your instinct is wrong → a sensory anomaly → "if X, do Y" sub-rules → what happens if you break it → a **dated case-file testimony** whose last line is a sting. The plot moves *inside* the rules: the friend is lost at rule 4 (pre-announced at 1:31 as "the one almost everyone breaks"), returns as an impostor at rule 6 and calls you back at rule 7. After the escape, a lore dump explains the bus, then a **next-morning tech epilogue** (transit-app receipt, texts and a call from the friend) re-opens the threat, and the last line rewrites the title's rule ("it only needs you to stand up").

## 1. Line-by-line

Timestamps are VTT cue starts. Cues that split one sentence are merged into one row under the first timestamp.

| Time | Line (verbatim, internal research only) | Beat | Device | Purpose |
|---|---|---|---|---|
| 0:00 | If you're ever on the last bus home and every passenger stands up at the same stop, | **Hook (premise)** | Conditional "If you..." opener that repeats the title; universal setting (last bus home) | The title is spoken as the first line, so the click is paid immediately and the viewer is cast as the protagonist |
| 0:05 | stay seated. | Hook (rule 0) | Two-word imperative after a pause | The core rule as a punchline. Sets the "obey to survive" contract |
| 0:07 | Don't ask where they're going. | Hook | Prohibition list (rule of three, 1/3) | Plants "where are they going?" as an open loop |
| 0:08 | Don't look at the driver in his mirror. | Hook | Prohibition 2/3, a specific odd object | Plants the driver/mirror (paid off by rule 2 at 2:55) |
| 0:10 | And whatever you do, don't get off with them, even if your friend does. | **Hook (stake)** | "Whatever you do" escalator + "even if your friend does" | The biggest loop of the video: the friend will go. Paid at 5:33, with a callback at 10:09 |
| 0:15 | I'm not talking about a busy stop where a lot of people happen to get off. | Clarifier | Pre-empting the skeptic ("I'm not talking about...") | Removes the ordinary explanation before the viewer can think it |
| 0:19 | I'm talking about every single passenger standing up at the exact same second at a stop you've never seen before. | Clarifier (sharpened) | Absolutes ("every single", "exact same second") + unknown place | Makes the anomaly precise and visual. Ends the 27 s extended hook |
| 0:27 | It's late. You and your friend Sammy just caught the last bus home. | Setup | Present tense, second person, named friend | Starts the scene. Naming the friend makes him the emotional stake |
| 0:31 | It's raining. Both your phones are almost dead. | Setup | Isolation set (weather + dead phones) | Removes the easy exits (calling for help). Rain is a sensory motif reused at 7:42 and 10:12 |
| 0:34 | And you're just happy to be out of the cold. | Setup (false safety) | Comfort beat | The bus starts as a refuge, so the inversion hurts more. "Cold" returns at 2:02 |
| 0:36 | The bus is almost full, which is strange for this hour. | Setup / first crack | "Which is strange" understatement | The first wrong detail, delivered calmly |
| 0:40 | Nobody is talking. Nobody is on their phone. Nobody is asleep. | Escalation | Anaphora ("Nobody is...") ×3 | Rhythm of three that removes every normal passenger behavior |
| 0:45 | They're all sitting perfectly straight looking at the back of the seat in front of them. | Escalation | Uniform posture (hive-mind image) | A concrete still image for the visual track; establishes they act as one |
| 0:49 | One of the lights above the aisle keeps flickering. | Escalation | Flicker motif | Classic horror lighting cue. Closes at 8:45 when the lights finally all come on |
| 0:53 | And every time it does, you could swear the passengers are a little closer to you than before. | **Re-hook** | Weeping-angels movement (only moves when unseen) | The first sign of threat toward "you". Never confirmed, so it stays as dread |
| 0:58 | The screen above the driver says, "Next stop." | Escalation | Mundane tech (stop display) | Sets up an announcement the viewer expects to be completed |
| 1:02 | And then nothing. | Escalation | Broken pattern, 3-word sentence | The missing stop name is the jolt. Paid at 3:38 (blank screen) and 10:01 (stop with no name) |
| 1:04 | The bus slows down. The doors open onto an empty road. | Escalation | Short declaratives, slow build | Puts the viewer at the doors of the unknown stop |
| 1:08 | No shelter, no sign, no lights. | Escalation | Triple negation | Defines "the empty road", a recurring location (4:29, 8:18, 9:16, 10:01) |
| 1:11 | And every passenger stands up at once. | **Inciting incident** | Title event delivered | Pays the title at 11% runtime |
| 1:14 | They don't push. They don't hold the handrails. They just stand in the aisle facing the doors waiting. | Escalation | Negations of normal crowd behavior | Wrongness through what they *don't* do. "Waiting" plants 9:45–9:50 |
| 1:20 | Sami leans over and whispers, "Is this our stop?" It isn't. | Escalation | Friend's question + 2-word answer | The friend is already tempted. Opens the "is this our stop" thread |
| 1:25 | Your stop is four stops away. | Stakes | Number (distance countdown) | A countdown frame for the whole ride; rule 3 builds on it |
| 1:27 | If this ever happens to you, follow these seven rules. | **Structure promise** | Explicit list length | Tells the viewer the video's length in units, so they can track progress |
| 1:31 | And remember rule number four. It's the one almost everyone breaks. | **Open loop (forward tease)** | Pre-announced failure point | A 3 min 50 s loop that carries the first half (paid at 5:20–5:25) |
| 1:36 | Night protocol file 015, the night bus. | Title card | Series ident with file number | Brand + "official dossier" frame. The number implies a back catalogue (bingeability) |
| 1:40 | Rule number one, stay seated. | **Rule 1 header** | Numbered imperative | Chapter re-hook, and it repeats the hook rule |
| 1:43 | Your body will want to stand up with them. That's normal. It's how crowds work. | Rule 1: mechanism | Pseudo-science normalizing ("that's normal") | Makes the rule feel grounded and makes the viewer complicit (your body betrays you) |
| 1:48 | When everyone around you moves, your legs move, too, before you even decide to. | Rule 1: mechanism | Loss of bodily control | Moves the threat inside the viewer's own body |
| 1:52 | Keep your hands on your knees and your feet flat on the floor. | Rule 1: procedure | Precise physical instruction | Concrete, imitable, procedural. The "manual" voice |
| 1:56 | The doors will stay open longer than they should. 10 seconds, 30, a full minute. | Rule 1: escalation | Number ladder (10 → 30 → 60) | Stretches time. Plants "why do the doors stay open?" (paid 9:45) |
| 2:02 | Cold air will fill the bus, and you'll notice something. | Rule 1: escalation | "You'll notice something" withhold | A micro-loop of 3 s |
| 2:05 | Your breath is fogging. Sami's breath is fogging. | Rule 1: anomaly | Parallel lines, sensory detail | Sets up a test for who is alive |
| 2:08 | Nobody else's is. Don't point it out. | **Re-hook (reveal)** | Living/dead tell + prohibition | The passengers are not alive. The fog test is reused at 5:41 when the friend turns |
| 2:12 | After a while, the doors will close and everyone will sit back down at exactly the same time as if nothing happened. | Rule 1: false relief | Reset to normal | A breather. "Exactly the same time" keeps the hive-mind image |
| 2:19 | If you already stood up by accident, sit down before the doors close, quietly, like you only stood to fix your jacket. | Rule 1: sub-rule | "If you already broke it" recovery clause | Assumes the viewer may fail, which keeps tension up. A cover story makes it practical |
| 2:27 | If one of them bends down to look at your face, keep breathing normally. | Rule 1: sub-rule / escalation | Closest-yet proximity | The threat comes to face distance |
| 2:31 | They're checking if you're one of them. | **Re-hook** | Explanation that is worse | Implies people can become "one of them". Paid at 9:08–9:12 |
| 2:33 | A student reported this on a night bus outside the city in 2019. | **Case file 1** | Dated testimony (role + place + year) | Proof format: makes a rule video feel like a real dossier |
| 2:38 | She said the passengers stood up three times on the same ride. | Case file 1 | Repetition with count | Raises the stakes from one event to a pattern |
| 2:41 | Each time the stop outside was the same empty road, and each time there was one more person standing on it. | Case file 1 | Growing count ("one more") | The crowd outside grows, so someone is being added |
| 2:49 | The third time she recognized the person. It was the girl who had been sitting next to her when she got on. | **Sting** | Rule-of-three payoff, familiar person | The anecdote ends on a sting. The girl returns at 8:32 |
| 2:55 | Rule number two, don't look at the driver in the mirror. | **Rule 2 header** | Callback to hook prohibition 2 | Pays the 0:08 plant. Follows the sting with no pause |
| 2:59 | Every bus has a big mirror above the driver so he can watch the passengers. | Rule 2: mechanism | Real-world fact | Grounding before the inversion |
| 3:04 | Tonight, he's watching you. You'll feel it before you see it. | Rule 2: escalation | Second-person target | Makes the gaze personal |
| 3:08 | A pressure on the side of your face, like someone standing too close. | Rule 2: anomaly | Bodily simile | A felt sensation the viewer can imagine on their own cheek |
| 3:13 | If you look up, you'll see his eyes in the glass, wide open, not blinking. And under them, a smile that's much too wide for a man who's been driving all night. | **Re-hook (image)** | Uncanny face (unblinking, too-wide smile) | The video's monster image. "Smile" and "never blinked" return at 4:00 and 6:07 |
| 3:24 | Look at the floor. Look at your hands. | Rule 2: procedure | Two-word commands | Pace drop and safe behavior |
| 3:26 | If he speaks to you, it will be through the speaker above your seat. He'll ask if you're getting off here. | Rule 2: sub-rule | Mundane tech turned personal | The bus's own systems speak to you |
| 3:32 | Don't answer. Just shake your head. | Rule 2: procedure | Prohibition + allowed action | Gives a survivable response |
| 3:34 | If you meet his eyes, the bus will stop announcing the stops. The screen will go blank. | **Consequence** | Penalty for breaking the rule | Pays 0:58–1:02 ("next stop... nothing") |
| 3:39 | The bell won't ring when you press it, and without the announcements, you won't know when yours has passed. | Consequence | Loss of control over the exit | Ties rule 2 to the "four stops" countdown and sets up rule 3 |
| 3:46 | One bus company reviewed the camera footage from a night route after a passenger went missing. | **Case file 2** | Institutional source (company + CCTV) + disappearance | Escalates the testimony source from a person to a company and from scary to missing |
| 3:50 | The driver's mirror was visible in every frame. For 40 minutes, the reflection never moved. Not when the bus turned, not when it stopped. | Case file 2 | Number (40 min) + impossible physics | A precise impossible detail |
| 4:00 | It just kept smiling at the same seat. | **Sting** | Callback (smile) + "the same seat" | Implies the missing passenger was the one in that seat. Hard cut to rule 3 |
| 4:04 | Rule number three, count the stops yourself. | **Rule 3 header** | Procedural rule | Turns the 1:25 "four stops" into a viewer task |
| 4:07 | Your stop is the fourth one, so count under your breath if you have to. | Rule 3: procedure | Countdown frame | The viewer counts along: built-in progress tracking |
| 4:11 | One, a gas station with every light switched off and one car parked at the pump with its doors open. | Rule 3: stop 1 | Numbered vignette, abandoned-scene image | Each stop is a micro-scene with one wrong detail (open doors = people who left) |
| 4:19 | Two, a bus shelter with a man inside standing with his face against the wall. He doesn't turn around when the bus stops, but his shoulders are shaking. | Rule 3: stop 2 | Faceless figure, ambiguous emotion (crying or laughing) | Plants the shelter man (returns at 8:32) |
| 4:29 | Three. The empty road again. Same road, same missing sign. | **Re-hook** | Callback location | The empty road returns: a loop, not a route |
| 4:34 | That's what the road is for. Every time you see it, you'll feel like the count has started over. Your head will tell you that you must have counted wrong. | Rule 3: mechanism | Gaslighting (your own mind doubts you) | The threat attacks the viewer's counting/memory |
| 4:42 | It hasn't started over. Keep counting. | Rule 3: procedure | Contradiction + command | Reassurance as order |
| 4:45 | Four will look exactly like your stop. The same corner, the same pharmacy sign, the same tree outside your building. | Rule 3: escalation (false target) | Triple "same" + home details | A fake version of home: the most tempting trap |
| 4:53 | But look closer. The pharmacy sign will be lit even though it closes at 9:00. and your bedroom window up on the third floor will be open. | **Re-hook (tells)** | Spot-the-difference clues with numbers (9:00, third floor) | Lets the viewer play detective; the clues are checkable |
| 5:01 | You closed it this morning. | **Sting** | 5-word personal fact | Implies something is in your home. Never closed |
| 5:03 | That isn't your stop. Stay seated and count it as 3 and 1/2. | Rule 3: procedure | Absurd precise number ("3 and 1/2") | A memorable, quotable rule detail (comment bait) |
| 5:08 | If you lose count, don't ask the other passengers. They'll all tell you the same number, and it will always be one. | Rule 3: sub-rule / sting | Hive answer + "always one" | The count resets if you trust them. Ends the rule on a chill |
| 5:15 | Have you ever missed your stop and had no idea where you were? Tell us in the comments where you were going. | **Mid-roll CTA** | Personal question in-premise | Comment prompt placed at 49%, **just before the rule-4 payoff**, so nobody leaves during it |
| 5:20 | Rule number four, if your friend stands up with them, let them go. This is the one almost everyone breaks. | **Rule 4 header (loop paid)** | Pays the 1:31 tease and the 0:10 "even if your friend does" | The emotional midpoint: the rule asks the viewer to abandon a friend |
| 5:28 | At the next empty stop, the doors will open and the passengers will stand. And this time, Sammy will stand with them. | **Midpoint turn** | Prediction in future tense ("will") | The friend is lost in the plot, foretold as fact |
| 5:36 | He won't look at you. His face will be calm, relaxed, almost happy. | Rule 4: anomaly | Wrong emotion (calm, happy) | Peaceful is scarier than panicked |
| 5:41 | His breath won't be fogging anymore. | **Re-hook (callback)** | Fog test from 2:05 | The viewer already knows what this means: he is one of them |
| 5:43 | You'll grab his sleeve. Everyone does. | Rule 4: temptation | Predicting the viewer's action ("everyone does") | Says why "almost everyone breaks" it |
| 5:46 | Don't. The moment you touch him, every passenger on the bus will turn and look at you. Not their bodies, just their heads. | **Consequence** | Body-horror detail (heads only) | Mass attention as the threat |
| 5:54 | and they'll smile. | Sting | "Smile" motif | The smile spreads from the driver to everyone |
| 5:54 | A man reported this in 2022. He grabbed his brother's arm and pulled him back into his seat. | **Case file 3** | Dated testimony, sibling stake | Shows what breaking the rule costs, with a family member |
| 6:01 | His brother sat down. He thanked him. They rode home together. They ate breakfast together the next morning. | Case file 3 (false relief) | Short-sentence calm sequence | Lulls the viewer: maybe saving him worked |
| 6:07 | But his brother never blinked again, and he never stopped smiling. | **Sting** | "But" turn + callback to the 3:13 driver face | The saved person came back wrong. Justifies the cruel rule |
| 6:11 | If you let Sammy go, he'll walk down the steps with the others. At the bottom, he'll turn around and look at you one last time. | Rule 4: obey path | Farewell beat | Emotional cost of obeying |
| 6:18 | He'll mouth two words. | Rule 4: withhold | Counted withhold ("two words") | A 3 s micro-loop |
| 6:21 | Come on, stay in your seat. | **Re-hook** | Lure ("come on") + immediate counter-order | The friend invites you; the narrator overrides |
| 6:23 | Rule number five. If you get off at your stop and you're still on the bus, sit back down. | **Rule 5 header** | Paradox rule (you got off, yet you're on the bus) | The rule itself is a mystery, so the viewer must listen to understand it |
| 6:29 | When the screen finally shows your stop, you'll press the bell, and this time it will ring. You'll walk to the doors. You'll step down onto the wet sidewalk. You'll feel the cold. You'll hear the doors close behind you. | Rule 5: false escape | "You'll..." anaphora, sensory ladder | A step-by-step escape that feels complete |
| 6:42 | Then you'll blink and you'll be standing in the aisle. Same bus, same passengers, same empty seat next to yours. | **Re-hook (time loop)** | Reset + triple "same" | The escape was false. "Empty seat" marks Sammy's absence |
| 6:50 | Everyone will be looking at you. Sit back down. Don't run for the doors again. | Rule 5: procedure | Mass gaze + prohibition | Keeps the gaze motif |
| 6:55 | A night shift nurse reported trying to get off six times. Each time she was back in the aisle before the bus started moving. | **Case file 4** | Dated-style testimony (role) + count (six) | Repetition makes the loop concrete |
| 7:02 | On the sixth try, she saw something in the window as the bus pulled away herself standing at the empty stop waving. | **Sting** | Doppelganger | The loop leaves a copy of you outside |
| 7:10 | She stayed on until the end of the line. She made it home, but her husband told her she had already come home an hour earlier and that she had gone straight to bed. | **Sting 2 (double)** | Survival + "but" + the double is in her home | Makes "survived" unsettling. Echoes the open window at 4:57 |
| 7:19 | The bus only lets you off when it decides it's your stop. If you keep trying, it lets something else off instead. | Rule 5: lore | Rule-explaining maxim | Gives the bus agency; "something else" stays open |
| 7:26 | Rule number six. If someone sits next to you on an empty bus, don't look at the window. | **Rule 6 header** | Conditional rule with a new setting (empty bus) | Announces the impostor scene before it happens |
| 7:32 | Eventually, the bus will be empty. Just you and the driver. | Rule 6: isolation | Total isolation | Removes the crowd; now it's one-on-one |
| 7:36 | Then you'll hear footsteps in the aisle and someone will sit down in Sammy's seat. | Rule 6: escalation | Sound-only approach | The threat is heard, not seen |
| 7:39 | It will sound like Sammy. It will smell like Sammy's jacket wet from the rain. It might even say your name. | Rule 6: escalation | Sensory ladder (sound → smell → your name) + rain callback | The impostor uses intimate details |
| 7:47 | It might ask why you didn't stop him. | **Re-hook (guilt)** | Guilt hook | Turns the rule-4 obedience into blame. Mirrors 10:09 |
| 7:49 | Don't turn your head and don't look at the dark window. | Rule 6: procedure | Double prohibition | Reinforces the rule |
| 7:52 | In the reflection, the seat next to you is still empty or worse, it isn't. | **Re-hook** | "Or worse" pivot | Two horrors in one line; the second is left to imagination |
| 7:57 | You might feel a head resting on your shoulder, heavy, cold. Don't move it. Don't move at all. | Rule 6: contact | Touch (the closest proximity in the video) | The threat touches you. Short commands |
| 8:06 | Keep your eyes on the floor until the weight beside you goes away. | Rule 6: procedure | Endurance instruction | Survival by waiting |
| 8:10 | When it finally lifts, the seat will still be warm, and there will be a wet handprint on the window on the outside of the glass. | **Sting** | Physical evidence + impossible location (outside) | Proof it was real and not human |
| 8:18 | Before the end of the line, the bus will pass the empty road one last time. It won't slow down. | Escalation (last pass) | "One last time" | Signals the finale |
| 8:24 | Through the window, you'll see all of them standing on the side of the road. Every passenger, the girl, the man from the shelter, and Sammy right at the front. | **Callback roll-call** | Gathers earlier plants (2:52 girl, 4:19 shelter man, Sammy) | Rewards attentive viewers; shows where they all went |
| 8:32 | They won't wave. They'll just turn their heads to follow the bus as it passes. Don't wave back. | Sting + prohibition | Head-turning motif (from 5:46) | Ends on an order that sounds like a joke and isn't |
| 8:37 | Rule number seven. When the driver says last stop, get off and don't look back. | **Rule 7 header** | Exit rule, "don't look back" (Orpheus) | The final rule is the way out |
| 8:45 | At the end of the line, the lights will flicker on all of them for the first time. | Rule 7: change | Closes the flicker motif from 0:49 | A visual signal that this stop is different |
| 8:50 | The driver will say it in a normal tired voice. Last stop. This one is real. | Rule 7: relief | Normal voice as the tell | Release after 7 min of tension |
| 8:56 | Walk to the doors. Step down. Keep walking. | Rule 7: procedure | Two-word commands | Pace for the escape |
| 8:59 | Behind you, you'll hear the engine idle. You'll hear the doors stay open, waiting. You'll hear Sammy call your name from inside. | **Re-hook (temptation)** | "You'll hear" ladder ending on the friend's voice | The last test: the friend's voice behind you |
| 9:08 | Don't turn around because the passengers on that bus were never commuters. They were people who took the last bus home and stood up at the wrong stop. | **Reveal (lore)** | Answer to "where are they going / who are they" | Closes the 0:07 and 2:31 loops: they are past victims |
| 9:16 | The road with no sign isn't on any map. The route number on the front of the bus doesn't exist. | Reveal | Impossible-place facts | Closes the empty-road loop with officialdom |
| 9:22 | The city retired that route years ago after a bus was found parked at the end of the line with its engine still running. The doors were open. Every seat was empty. | **Case file 5 (origin)** | Origin legend, official record | The bus's backstory, told like a news report |
| 9:32 | The driver's log said the bus had stopped 41 times that night. The route only had 12 stops. | **Sting** | Number contrast (41 vs 12) | The video's most quotable impossible statistic |
| 9:39 | Every night, the bus picks up one more. And every night, it needs someone to stand up with them. | Reveal (rule) | "Every night" repetition | Turns a one-time story into an ongoing threat |
| 9:45 | That's why the doors stay open so long. They're not waiting for the passengers to get on. They're waiting for you. | **Reveal (personal)** | Closes the 1:56 / 1:14 "waiting" plants; "for you" | Moves the target from everyone to the viewer |
| 9:51 | The next morning, your phone buzzes. It's your transit app. Trip complete. Thank you for riding. | **Epilogue** | Time skip + mundane tech message | False normality. The phones that were "almost dead" are back |
| 9:57 | You open it. The map shows last night's route and a stop you've never seen on an empty road with no name. | Epilogue (evidence) | Callback (stop with no name) | The bus followed you into your phone |
| 10:04 | Two passengers boarded. one got off. | **Sting** | Number receipt ("two boarded, one got off") | A cold data line that says Sammy didn't come back |
| 10:07 | Then a text from Sammy. Why didn't you get off with me? | **Twist (inversion)** | Inverts the hook rule ("don't get off with them") + 7:47 guilt line | The friend is on the other side and blames you |
| 10:10 | You try calling him. It rings once and you hear rain and an engine and a crowd of people breathing. | Escalation | Sound collage (rain + engine + breathing) | The bus is still out there with him on it |
| 10:16 | Then the call ends and one more text arrives. Same bus tonight. I told them you're coming. | **Cliff / threat re-opened** | Invitation as a threat, tonight | Re-opens the threat for the viewer's own night |
| 10:23 | So if everyone on the night bus ever stands up at your stop, stay seated because the bus doesn't need you to get off. | **Bookend** | Title restated as the close | Ring structure: the first line returns |
| 10:30 | It only needs you to stand up. | **Final twist line** | Reframe of rule 1 (standing is the real danger) | Changes the meaning of the title in the last 3 s, which invites a rewatch and comments |

## 2. Structure summary

### Beat sequence (% of 633 s)

| Range | Beat | Seconds | Words | % runtime | wpm |
|---|---|---|---|---|---|
| 0:00–0:14 | Hook: the title as a rule + 3 prohibitions + "even if your friend does" | 15 | 46 | 2.4% | 184 |
| 0:15–0:26 | Clarifier: not a busy stop, every passenger at the same second | 12 | 36 | 1.9% | 180 |
| 0:27–1:10 | Scene: you + Sammy, rain, dead phones, silent full bus, flicker, "next stop... nothing", empty road | 44 | 124 | 7.0% | 169 |
| 1:11–1:26 | Inciting: everyone stands; "is this our stop?"; four stops away | 16 | 42 | 2.5% | 158 |
| 1:27–1:35 | Promise: seven rules, remember rule four | 9 | 21 | 1.4% | 140 |
| 1:36–1:39 | Title card: protocol file number | 4 | 7 | 0.6% | 105 |
| 1:40–2:54 | Rule 1 (stay seated) + case file (student 2019) | 75 | 219 | 11.8% | 175 |
| 2:55–4:03 | Rule 2 (mirror) + case file (company CCTV, missing passenger) | 69 | 202 | 10.7% | 178 |
| 4:04–5:14 | Rule 3 (count the stops): four stop vignettes, fake home stop | 71 | 205 | 11.4% | 171 |
| 5:15–5:19 | Mid-roll comment CTA | 5 | 22 | 0.8% | 264 |
| 5:20–6:22 | Rule 4 (let the friend go) + case file (brother 2022) | 63 | 176 | 10.0% | 168 |
| 6:23–7:25 | Rule 5 (false exit time loop) + case file (nurse, doppelganger) | 63 | 196 | 10.0% | 187 |
| 7:26–8:36 | Rule 6 (impostor in the friend's seat) + last pass of the empty road | 71 | 227 | 11.4% | 189 |
| 8:37–9:50 | Rule 7 (last stop, don't look back) + lore reveal + origin case | 74 | 220 | 11.7% | 178 |
| 9:51–10:33 | Next-morning epilogue (app, texts, call) + bookend twist line | 43 | 118 | 6.5% | 173 |

Four acts:
- **Cold open and setup (0:00–1:39, 16%).** Premise as rules, scene, inciting event, rule-count promise, title card.
- **Survive the ride: rules 1–3 (1:40–5:19, 35%).** The threat is the passengers, the driver and the route. The friend is still with you.
- **Lose the friend: rules 4–6 (5:20–8:36, 31%).** The friend goes, saving people fails, escape fails, the friend's impostor sits beside you.
- **Escape, lore and the morning after: rule 7 + epilogue (8:37–10:33, 18%).**

The rule chapters are **very even (63–75 s each, 176–227 words)**. The midpoint turn (the friend stands, 5:28) lands at 52% runtime, right after the mid-roll CTA at 49%.

### Rule anatomy (repeated 7 times)

1. **Header** (2–4 s): "Rule number N" + imperative. Rules 1 and 2 repeat the hook's prohibitions; rule 4 pays the pre-announced tease.
2. **Mechanism** (5–15 s): why your instinct or a normal fact leads you wrong ("that's normal", "every bus has a mirror").
3. **Anomaly** (5–15 s): one sensory detail (fogging breath, pressure on the face, a lit sign).
4. **Sub-rules** (5–15 s): "If X happens, do Y", often a recovery clause for when you already broke it.
5. **Consequence** (5–10 s): what breaking it does.
6. **Case file** (15–25 s) in rules 1, 2, 4, 5 and 7: who reported it (student, bus company, a man, a nurse, the city), sometimes a year, a short sequence, and a **one-line sting** at the end. Rules 3 and 6 replace it with an in-scene sting (the window you closed; the handprint outside).
7. **Hard cut** from the sting into the next header, often in the same cue ("...when she got on. Rule number two").

### Hook

- **Length:** 46 words / 15 s (0:00–0:14) for the core hook. With the "I'm not talking about..." clarifier it is 82 words / 27 s (4% runtime).
- **Shape:** the title spoken as line 1 → a two-word rule → three escalating prohibitions → the friend stake. The whole premise and the main loop (the friend will go) are stated before 0:15.
- The title event (everyone stands) happens on screen at **1:11 (11%)**. The scene build in between is carried by the hook's promise.
- The rule-count promise and the "rule four" tease at 1:27–1:33 work as a **second hook** before the long body.

### Re-hook interval

- **Minor jolts** (a new uncanny detail, rule, number or prohibition): 91 in 630 s. **Median gap 6.5 s, mean 7.0 s.** The longest gaps are 16–19 s (0:19–0:36 scene setup, rule 1 mechanism 1:40–1:56, 2:08–2:27, the rule-5 false-escape walkthrough 6:23–6:42, rule-7 header to 8:53).
- **Major jolts** (a sting, a reveal or a rule twist): 33. **Median gap 17 s, mean 19 s.** The longest is 61 s (0:10 → 1:11), the scene build before the inciting event.
- **Chapter re-hooks:** a numbered rule every **63–75 s** (YouTube chapters make it visible on the scrub bar).
- Each case file ends on a sting, and the next rule header comes within 0–4 s of it: there is never a lull after a scare.

### Open loops (open → close)

| Loop | Opens | Closes |
|---|---|---|
| Where are they going / who are they? | 0:07, 2:31 ("checking if you're one of them") | 9:08–9:12 (past riders who stood up) |
| Don't look at the driver's mirror | 0:08 | 2:55 rule 2 |
| Even if your friend does | 0:10 | 5:28 (Sammy stands) → 6:11 (he goes) → 10:07 (he texts) |
| Passengers get closer with each flicker | 0:53 | Never confirmed; the flicker closes at 8:45 |
| "Next stop" ... nothing | 0:58 | 3:34 (the screen goes blank) → 10:01 (the app shows a stop with no name) |
| The empty road | 1:05 | 4:29 → 8:18–8:32 → 9:16 (not on any map) |
| Is this our stop? Four stops away | 1:20–1:25 | 4:04–5:03 (count; the fake fourth stop) → 6:29 (the real stop, a false exit) → 8:50 (last stop is real) |
| Seven rules; remember rule four | 1:27–1:33 | 5:20–5:25 |
| Why do the doors stay open so long? | 1:56 | 9:45–9:50 ("waiting for you") |
| Breath fogging test | 2:05–2:08 | 5:41 (Sammy's breath stops) |
| The girl next to her / one more person | 2:41–2:52 | 8:24–8:32 (roll-call outside) |
| The shelter man | 4:19 | 8:32 |
| Your bedroom window is open | 4:57–5:01 | **Never** (echoed by the nurse's double at 7:12) |
| It lets something else off instead | 7:22 | **Never** |
| Why didn't you stop him? | 7:47 | 10:09 (inverted: "why didn't you get off with me?") |
| 41 stops on a 12-stop route | 9:32 | 9:39 (it picks up one more every night) |
| Same bus tonight | 10:20 | **Never** (the ending loop) |

Two to four loops are open at any time. Planted details come back in **callback roll-calls** (8:24–8:32) and in the epilogue (no-name stop, rain, engine). About four loops stay open at the end (the window, "something else", the friend's fate, tonight's bus), which suits a numbered series.

### Escalation ladder

- **Proximity to you:** strangers in their seats → they seem closer at each flicker → one bends to your face → the driver's gaze presses on your cheek → the bus speaker addresses you → your own home appears as a fake stop → every head turns to you → the bus traps you in a loop → something sits in your friend's seat and rests its head on you → it follows you home through your phone → it invites you back tonight.
- **The friend:** whispers "is this our stop?" → still fogging (alive) → stands, breath gone → mouths a lure → his impostor sits beside you → he calls your name as you leave → texts blaming you → "I told them you're coming".
- **Case-file costs:** a stranger recognized → a passenger missing → a brother returns wrong → a nurse replaced by her double → a whole bus empty with 41 stops on a 12-stop route. Each source is more official (a student → a company → a man → a nurse → the city) and each cost is worse.
- **The rules themselves get stranger:** a simple posture rule → a gaze rule → a counting rule with "3 and 1/2" → an abandon-your-friend rule → a paradox rule (you got off but you're still on) → an impostor rule → an exit rule with "don't look back".

### How it ends

- Rule 7 is survivable: you get off. Then the lore reveal explains the passengers, the road and the route, with an official-record origin and a number sting (41 vs 12).
- The **epilogue** brings the threat into daylight and into the viewer's phone (app receipt, text, call). The friend's text **inverts the hook rule**, and the last text re-opens the threat for tonight.
- The final two lines restate the title (ring structure) and then **re-read rule 1**: the danger was standing up, not getting off. That last-3-seconds reframe is the comment and rewatch driver.
- CTA: one mid-roll comment question at 5:15, in-premise. No spoken subscribe CTA at the end; the "file 015" brand does the series work.

### Pacing and device notes for the PLAYBOOK

- **Long-form rules format:** 10.5 min at ~176 wpm with a median sentence of 7 words. Even, metronomic pacing; tension comes from content, not speed.
- **Seven equal chapters** (~65–75 s each) make a long video skimmable and give a re-hook every minute via the scrub bar.
- **Pre-announced failure point** ("remember rule four, almost everyone breaks it") carries the first half, and the **mid-roll CTA sits right before the payoff**.
- **Case files with dated, role-labelled sources** (student 2019, bus company CCTV, a man 2022, a night-shift nurse, a city route log) end every other rule on a sting.
- **Future-tense second person** ("you'll grab his sleeve; everyone does") predicts the viewer's actions, which feels like the manual has seen this before.
- **Test devices** the viewer can apply (fogging breath, sign lit after closing time, a window you closed) let the audience play detective.
- **Motif chain** (flicker, smile, never blinking, heads turning, rain, the empty road, "waiting") ties all seven chapters together and is cashed in at the roll-call and the lore reveal.
- **Ring structure + final reframe**: the title returns as the last line with one added clause that changes its meaning.
- The 1-day-old view count is small in absolute terms (3,201) on a 422-median channel. Treat the structure as a strong signal for the long-form rules format, not as proof at scale.

## 3. Transferable skeleton (no original wording)

For a **standalone second-person "If X happens... DO Y" rules story**, 8–11 min (scale down to 3–5 min by keeping 4–5 rules and dropping the case files from every other rule), ~175 wpm, median sentence 6–8 words. The title states the trigger and the core rule.

1. **0–3% · Rule-shaped hook.** Speak the title as the first sentence (if [ordinary place + uncanny trigger], [core rule]). Follow with three escalating prohibitions, the last one naming a companion who will break it.
2. **3–5% · Skeptic pre-empt.** One "this isn't the normal version" line, then a sharpened, absolute description of the anomaly (everyone, the same instant, a place you don't know).
3. **5–12% · Scene in present-tense second person.** You + one named companion, late, cut off from help (weather, dead battery). Three or four wrongness details in parallel lines (nobody does A, B or C). Plant 3–4 motifs that will return: a light, a display or sign, a location, a sound.
4. **12–14% · Inciting event + distance countdown.** The title event happens. The companion is tempted. Give a numeric distance to safety.
5. **14–16% · Structure promise + series ident.** State the number of rules and single out one as "the one people break". Show a numbered file/episode card.
6. **16–50% · Rules 1–3, survive the place.** Each ~10–12% of runtime with the anatomy: header → why instinct misleads → one sensory test → if/then sub-rules (including a recovery clause) → consequence → a sourced case file (role, place, year) ending on a one-line sting → hard cut to the next header. Make one rule a counting or spotting task the viewer can do along (fake version of a familiar place with checkable clues).
7. **~49% · In-premise comment CTA,** placed immediately before the pre-announced rule.
8. **50–82% · Rules 4–6, lose the companion.** The teased rule asks the viewer to abandon the companion. Use the earlier sensory test to show the companion has turned. A case file shows that saving someone makes them return wrong. Then a paradox rule (a false escape that resets), then an impostor rule (something takes the companion's place, uses their voice and smell, touches you). End with a last pass of the recurring location and a roll-call of every planted figure.
9. **82–94% · Final rule = the exit, then lore.** A survivable exit with a "don't look back" test using the companion's voice. Then reveal what the threat is (past victims), an official-record origin, and one impossible number contrast. Move the target to "you".
10. **94–100% · Morning-after epilogue + ring close.** A mundane tech message proves the night happened (receipt-style data line). The companion contacts you from the other side, inverting the hook's rule and inviting you back. Close by restating the title with one added clause that reframes the core rule.

**Pacing targets:**
- ~1,850 words over ~10.5 min (or ~550–900 words for 3–5 min).
- A minor jolt every ~6–7 s, a sting every ~15–20 s, a rule header every ~60–75 s.
- Never more than ~20 s without a new uncanny detail; never a pause after a sting.
- 3–4 loops open at any time; leave 3–4 open at the end for the series.
