# Someone Broke Into Our Hotel Room: Wansee Entertainment (annotated)

| Field | Value |
|---|---|
| URL | https://www.youtube.com/watch?v=Qz-TrB6W2SM |
| Title | Someone Broke Into Our Hotel Room (Horror Animated) |
| Channel | Wansee Entertainment (median of the 60 most recent uploads on the Videos tab: 169,000 views) |
| Views | 1,521,857 |
| Outlier score | **9.01** |
| Duration | 168 s (2:48). Speech runs 0:00 to about 2:44, and the last ~4 s are a silent visual sting |
| Uploaded | 2018-11-09 |
| Format | 16:9 YouTube animated "true story" (also cut vertically as a Short). A first-person child narrator (the blonde girl) with separately acted voices for the kids and the intruder. Flat 2D vector cartoon in the Jaiden/Wansee style: static rooms, mouth flaps and expression swaps, a new shot every 3 to 6 s, no burned-in captions |
| Total words | **447** (faster-whisper small). Whisper dropped a few words at about 1:57 (the line starts mid-sentence with "him,") |
| Words/min | **160 wpm** over 168 s, or **164 wpm** over the 164 s of speech. Per 30 s window: 206 · 126 · 132 · 172 · 162 · ~200 (last 18 s, 48 words in ~14 s of speech). This is less than half the pace of the translated TikTok horror in this corpus (~360 wpm). The slow middle is deliberate: the dialogue scenes leave **dead air for the knocks and silences** (about 8 s at 0:45–0:53, about 4 s at 1:29–1:33) |

Sources: `raw/Qz-TrB6W2SM.txt` (whisper segment starts; names are phonetic: "Team" = Tim). Overview sheet `sheets/Qz-TrB6W2SM.jpg` (a tile about every 5 s). 1 fps sheets: `dgx-spark:~/studio/refs/corpus_horror/sheets/Qz-TrB6W2SM/s_001..014.jpg`. Sheet k covers seconds 12(k−1) to 12k−1, and I checked all 14. Lines are quoted verbatim **for internal research only**. Never reuse the wording, names or story.

Whisper errors worth knowing about (the meaning is clear from context and the visuals):
- "very good as a hotel": roughly "a very good hotel".
- "still makes me half-chill": "still gives me chills".
- "I knew he was on room service": the intended meaning is that he was **not** room service.
- "in a fake ID card": he was using a fake key card.
- "come back until 11 p.m.": "be back by 11 p.m.".
- Dialogue attributions are partly scrambled. From the visuals, the **narrator is the blonde girl**, the orange-shirt boy is Tim (the oldest, the "it's just room service" voice) and the blue-shirt boy is Phil (at the window, wants to keep the door shut).

**Key mechanic:** this is a *true-story confession*. The title is the whole hook (someone got in), so the script can spend 18% of its runtime on cozy setup. The threat then escalates **entirely through a closed door**: a knock, an innocent explanation, a polite voice, a silence, a shouted order, a tell that he's fake (wrong language), and then the key card. He gets in, they lock themselves in a smaller room, and a lucky object rescues them. The ending is an **after-the-fact reveal that the real danger was worse than they knew** (he had been watching them, plus a criminal label). The visuals carry a second, silent layer: a dark figure at the pool in the opening seconds and in a lit window mid-story, paid off by CCTV footage of him watching their table, and a final callback to the pool.

## 1. Line-by-line

Timestamps are whisper segment starts. The visual column comes from the 1 fps sheets.

| Time | Line (verbatim, internal research only) | Beat | Device | Purpose | Visual |
|---|---|---|---|---|---|
| 0:00 | I was around 10 years old when this happened. | **Hook (frame)** | True-story frame, age as a vulnerability number | "This really happened, to a child." Credibility plus protectiveness in 9 words. The title already promised the break-in | Fade up on a grand hotel exterior with a fountain |
| 0:03 | Me and my two best friends and our parents were on a long vacation in Turkey in a very good as a hotel. | Setup | Exotic or specific setting | A foreign country plants "we don't speak the language" (paid off at 1:42), and a "very good hotel" plants false safety | Pool: kids swimming, two mothers in front, **dark silhouettes on loungers behind (one alone, watching)** |
| 0:09 | One night, me and my two best friends who I'll call team at Phil for this video, | Setup | Anonymized names ("I'll call them...") | Signals a real story with privacy protection, which adds authenticity | Dad waves at a hotel-room door, the kids peek out, the door shuts |
| 0:14 | were staying at Team's room in the hotel while our parents were in the hotel restaurant. | Setup / stakes plant | Separation of protector and child | Adults removed: the kids are alone. Classic precondition | Restaurant: waiter with wine glasses, parents at a table (dark windows) |
| 0:18 | The room wasn't bad, actually all of our rooms seemed safe, at least we thought it was. | Foreshadow (soft open loop) | "We thought it was safe" retroactive irony | First crack of dread, and it promises that safety will fail | Kids on armchairs with soda and snacks |
| 0:24 | We were having a lot of fun watching Simpsons and playing Monopoly, | Setup (cozy baseline) | Specific relatable detail (TV show, board game) | Warm normality to contrast against, and it makes the kids likable | Kids laugh at the TV, **Monopoly dice macro** |
| 0:28 | But what happened that night still makes me half-chill. | **Re-hook / open loop** | "But" pivot + lasting-trauma foreshadow | Converts cozy into suspense at 17% runtime. Promises the event is real and bad | Kids cheering over the game, then a slow push on the curtains/window (night) |
| 0:32 | So it was around 1 a.m. and our parents were late. | Stakes | Clock time (number), broken promise | Late night + missing adults = vulnerability rises | Night window/curtains |
| 0:35 | Phil looked at them through the window and said, | Setup | Dialogue lead-in | Shifts into scene mode with acted voices | Blue-shirt boy peeks through the curtain |
| 0:39 | They're still in that stupid restaurant. | Stakes | Kid-voiced dialogue, mild annoyance | Keeps it naturalistic. The kids aren't scared yet, so the viewer is ahead of them | Blue boy close-up, eye roll |
| 0:41 | Yeah, they told us they'll come back until 11 p.m. | Stakes | Number contrast (11 p.m. vs 1 a.m.) | Measurable "2 hours overdue": the adults are unreliable | Blonde girl (narrator) talking, smiling |
| 0:45 | I answered, Guys, someone is knocking on the door. | **Inciting incident** | Knock (sound event), pattern interrupt | The threat arrives at 27% runtime. Then **~8 s of no speech** for knock SFX and reaction | Orange boy in front of the TV turns, then gestures. The blue boy at the dark window looks worried |
| 0:53 | Tim said, It's probably just room service. | Escalation (false reassurance) | Rationalization by the oldest kid | An innocent explanation the viewer doesn't buy creates dramatic irony | Orange boy (Tim) at the TV, explaining |
| 0:57 | Phil said, | (lead-in) | n/a | n/a | Blue boy at the night window |
| 0:58 | Um, can we... can we not open the door? | Escalation | Hesitant plea (stammer), rule-like instinct: "don't open" | Voices what the audience is shouting at the screen | Girl points toward the door |
| 1:05 | I said, I was pretty scared in that situation. | Stakes | Narrator aside, emotion named | Breaks scene to re-anchor first-person fear | Girl pointing, then a wide over-the-shoulder shot toward **the closed door** |
| 1:10 | I was only 10 and my friends were only 2 and 3 years older than me. | Stakes | Number/scale (ages) | Quantifies helplessness: there is no adult in the room | Wide room, the door in center frame |
| 1:14 | So we were all pretty much defenseless children in a room. | Stakes | Explicit stakes summary | Says the vulnerability out loud and primes protective dread | **Exterior: the hotel at night, lit windows, a figure silhouetted in one window** |
| 1:19 | Team who was the oldest answered, oh come on it's just room service. | Escalation (overruled) | Authority-by-age vs instinct | The "leader" makes the wrong call, and the tension rises because he may open the door | Orange boy at the TV, pointing dismissively |
| 1:25 | The guy on the other side of the door said, | **Escalation 1 (voice)** | Unseen speaker | The threat gets a voice but no face | **Intruder at the door, cropped at the jaw: grimy green-gray light, one hand knocking, the other holding a card at the lock reader** |
| 1:28 | Hello? | Escalation | Polite, normal word | Mundane politeness from an unknown man is creepier than a scream | Same crop, mouth moving |
| 1:29 | Can you please open the door? | Escalation | Polite request (a "fake normal" stranger) | Tests whether the kids will comply. ~4 s of silence follows | Same, then a cut to the kids frozen at the Monopoly table |
| 1:33 | When he said that we were all scared. | Reaction | Group fear beat | Gives the viewer permission to be scared too | Wide room, kids frozen |
| 1:35 | In a couple of minutes of silence he said in a louder voice, | **Escalation 2 (silence)** | Time-stretch ("minutes of silence"), volume ramp | Silence as threat, and it sets up the loud sting | Wide room, kids frozen |
| 1:39 | Open the door! | **Escalation 3 (shout)** | Volume spike / pattern interrupt, command | Jump-scare moment: politeness drops away | Intruder crop, mouth wide, shouting |
| 1:42 | I started crying because I knew he was on room service because if he was, he would have | **Reveal 1 (tell)** | Logical tell (wrong language), callback to the "Turkey" plant | The viewer gets proof he's fake, and the 0:03 plant pays off | Girl close-up, tears welling |
| 1:47 | talked in Turkish. | Reveal 1 | Specific clue | Concrete, checkable detail makes it feel true | Orange boy close-up, teeth clenched, crying |
| 1:50 | I was in shock as in that moment I realized that this strange guy is in a fake ID card | **Reveal 2 / stakes spike** | Prop reveal (key card), the "safe room" premise breaks | Closes the 0:18 "seemed safe" loop: the door doesn't protect them | Orange boy crying, then the blue boy shocked → crying |
| 1:55 | to open the door. | Stakes spike | n/a | The door is about to open | Blue boy sobbing |
| 1:57 | him, grabbed both of us and we ran to the bathroom and locked the door. Luckily, the | **Climax (flight)** | Action burst, retreat to a smaller room | Physical action after a long static build. The second locked door = a new, smaller "safe zone" | **Hand grabs an arm**, the kids run past the bed. The room empties, then **the intruder enters, face shown for the first time** |
| 2:02 | guy wasn't fast to get us. He was screaming to open the door. I said, | Climax (siege) | Near-miss ("wasn't fast enough"), repeated command | The threat is now inside and pounding. The repetition of "open the door" is the refrain | Intruder at the bathroom door pounding, then the three kids in the bathroom by the mirror |
| 2:07 | Look! A phone! Luckily, Team's mom left her phone so we could call her if we needed anything. | **Turn (lifeline)** | Exclamation, Chekhov-style convenient object explained by a backstory line | Hope beat, and the explanation keeps it believable | Orange boy, sweating, finds a **flip phone (macro)** |
| 2:15 | So Phil grabbed the phone and called his dad and told them the situation. And they | Resolution (rescue) | Phone UI beat | Fast de-escalation | **Green phone-call icon screen**, then split-screen: dad on the phone in the restaurant / boy in the bathroom |
| 2:20 | came up to find the guy nowhere. They thought we were lying to them until the | **Re-hook (disbelief)** | Vanished threat + adults don't believe the kids | Mini-loop: was it real? New frustration keeps viewers through the denouement | Parents at the room door, then the mother arguing with the kids |
| 2:25 | the hotel manager showed them the footage. | Proof | Fake authority → **real authority/evidence** (CCTV) | Closes the disbelief loop with hard evidence | **Security room: monitors show the man at the door, a guard pointing** |
| 2:28 | We found out that the man was stalking us | **Reveal 3 (retro-horror)** | Reframe: it wasn't random | Recasts the whole video: he had been watching them all along. Pays off the visual silhouettes | **Intruder eating in the restaurant, staring at the families' table** |
| 2:30 | and a couple other children. | Reveal 3 (scale) | Scale-up (it's not just us) | Widens the stakes beyond the narrator | Same |
| 2:32 | In a couple of days, police had finally caught him. | Resolution | Time skip | Safety restored, closing the threat loop | **Police pin him in a night alley, squad car lights** |
| 2:34 | He was a serial rapist and a pedophile. | **Final reveal (worst case)** | Shock label (identity reveal) | The real stakes, revealed only after the danger is over. The "what could have happened" chill | **Mugshot with height chart and number board** |
| 2:37 | We were just lucky he wasn't fast to get us. | Payoff / reflection | Callback to the "wasn't fast" line | Near-miss restated so the viewer replays the climax in their head | Pool callback: the kids swimming again with their mothers |
| 2:40 | I will never forget that night, | **Ending (sign-off)** | Lasting-trauma callback (closes 0:28) | Bookend: the promise "still gives me chills" is now earned | **Pool lounger where the dark silhouette sat at 0:05: a man hidden behind a newspaper** |
| 2:42 | as that was the worst day of my life. | Ending | Superlative | Emotional full stop. No CTA in the audio | Hold on the newspaper man, slow fade to black (≈2:44–2:48 silent) |

## 2. Structure summary

### Beat sequence (% of 168 s)

| Range | Beat | Words | % runtime |
|---|---|---|---|
| 0:00–0:08 | Hook frame: true story, age 10, foreign hotel | 32 | 5% |
| 0:09–0:31 | Setup: kids alone, adults away, false safety, cozy fun, **"but" foreshadow at 0:28** | 71 | 14% |
| 0:32–0:44 | Stakes: 1 a.m., parents 2 h overdue | 36 | 8% |
| 0:45–1:04 | Inciting knock + 8 s silence + "room service" rationalization + plea not to open | 27 | 12% |
| 1:05–1:24 | Vulnerability aside (ages, "defenseless") + the oldest overrules | 49 | 12% |
| 1:25–1:41 | Door ladder: polite voice → silence → shouted command | 41 | 10% |
| 1:42–1:56 | Reveals: wrong language (fake staff) → he has a key card | 45 | 9% |
| 1:57–2:14 | Climax: he gets in, flight to the bathroom, siege, phone found | 50 | 11% |
| 2:15–2:27 | Rescue call → he's gone → adults disbelieve → CCTV proof | 39 | 8% |
| 2:28–2:39 | Aftermath reveals: he was stalking us (and others) → arrested → criminal label → "lucky" | 42 | 7% |
| 2:40–2:48 | Sign-off ("never forget") + silent visual sting at the pool | 15 | 5% |

Four acts:
- **Calm (0:00–0:44, 27%)**
- **Door siege (0:45–1:56, 43%)**
- **Breach and escape (1:57–2:27, 18%)**
- **Retro-reveal and sign-off (2:28–2:48, 12%)**

The siege behind the closed door is the longest act and the core of the video. The actual break-in lasts only ~10 s.

### Hook

- **The title is the hook.** The audio opener is 9 words / 3 s ("this happened when I was 10"). The first block (true story + age + exotic hotel) is 32 words / 9 s. There is no danger in the audio until the knock.
- First explicit tension line: **0:28** (~85 words, 17% runtime), a "but what happened that night..." foreshadow. A soft "we thought it was safe" comes earlier, at 0:18.
- Threat onset (the knock): **0:45–0:47** (~145 words, 27% runtime).
- This only works because the title has already told viewers that someone breaks in, so the cozy setup reads as dramatic irony instead of filler. **For our pilots:** if the title or thumbnail can't carry the promise, we need an audio hook in the first 3 s instead.

### Re-hook interval

Jolts at 0:18, 0:28, 0:32, 0:45, 0:58, 1:10, 1:25, 1:35, 1:39, 1:42, 1:50, 1:57, 2:02, 2:07, 2:20, 2:25, 2:28, 2:34, 2:40.

- Gaps: 10, 4, 13, 13, 12, 15, 10, 4, 3, 8, 7, 5, 5, 13, 5, 3, 6, 6.
- **Median ≈ 6.5 s, mean ≈ 7.9 s.**
- In the setup they come every 10–13 s. From 1:35 to 2:07 they come every 3–8 s: the jolts speed up as the threat closes in.
- The longest dry stretch is 0:00–0:18, carried by the title promise and the cozy specifics.
- Visual cuts come every 3–6 s. **Silence is used as a re-hook**: after the knock (≈8 s) and after "please open the door" (≈4 s). Our TTS pipeline must support timed pauses with SFX for this.

### Open loops (open → close)

| Loop | Opens | Closes |
|---|---|---|
| Title: someone broke into our room | Title / 0:00 | 1:57–2:02 (he's inside) |
| "Seemed safe, at least we thought" | 0:18 | 1:50 (the key card: the room was never safe) |
| "What happened that night still gives me chills" | 0:28 | 2:34–2:42 (the label + "never forget") |
| Parents late, where are they? | 0:32 | 2:15–2:20 (the phone call brings them) |
| Who is knocking? | 0:45 | 1:42 (not staff) → 2:28 (stalker) → 2:34 (who he really is). Closed in three stages |
| Will they open the door? | 0:58 | 1:50 (he doesn't need them to) |
| Will he get them? | 1:57 | 2:07–2:15 (phone) / 2:37 ("lucky") |
| Do the adults believe them? | 2:20 | 2:25 (footage) |
| **Visual only:** the dark figure at the pool (0:05) and the figure in the lit window (1:15) | 0:05 / 1:15 | 2:28 (CCTV: him watching their table). The 2:40 pool callback re-opens it as a lingering unease |

There are 2–3 loops open at once. The "who is it" loop is **closed in three escalating stages**, and each answer is worse than the last: fake staff, then a stalker, then a predator.

### Escalation ladder

- **At the door (each rung ~5–10 s):** parents overdue → knock → "probably room service" → a kid begs not to open → "we're defenseless children" → polite "hello, please open" → minutes of silence → shouted "open the door!" → wrong language (fake) → he has a key card.
- **Breach (~3 s per rung):** he's inside → retreat to the bathroom, lock → he's pounding and screaming → a phone found.
- **Retro (after safety):** vanished → not believed → footage → he was stalking us → and other kids → caught → worst-case identity.
- The **sound/volume ladder** (knock → polite → silence → shout → screaming) does as much work as the plot. The **barrier ladder** (room door → key card defeats it → bathroom door) gives the story its spatial logic.

### How it ends

- Safety is restored first (rescue, proof, arrest). **Then** the darkest information drops (what he was), so the scare lands after the tension has released. That is the "it could have been so much worse" chill.
- The 0:28 foreshadow closes with a first-person sign-off ("never forget / worst day").
- The last ~4 s are a **silent visual sting**: the opening pool shot comes back with a man on the watcher's lounger behind a newspaper, then a fade to black. The visual ending is ambiguous while the audio is fully closed.
- No CTA in the audio. The video is standalone, not a series.

## 3. Transferable skeleton (no original wording)

For a **standalone first-person "it really happened to me" home-invasion or stranger-at-the-door short**, 150–180 s, at about 160–200 wpm with acted dialogue and deliberate silences, a cut every 3–6 s. The title or thumbnail must state the incident outright.

1. **0–5% · Credibility frame.** One line of age/time + "this happened" + a specific, slightly foreign or unfamiliar location. The setting plants one detail that will later expose the threat (language, uniform, schedule, local rule).
2. **5–18% · Cozy baseline with protectors removed.** Establish who is alone and why the guardians are elsewhere. Add one "we thought it was safe" ironic line, two concrete comfort details (a show, a game, snacks), and close with a **"but"-pivot promise of lasting fear**.
3. **18–27% · Clock stakes.** A specific late time + a broken promise from the guardians (expected at X, now it's Y). Dialogue in character voices, still light.
4. **27–40% · Inciting sound + rationalization.** A knock or other sound, then **real dead air**. The most confident character offers an innocent explanation, and the most nervous one voices the "don't open it" instinct. The narrator steps out to quantify helplessness (ages, size, nobody nearby).
5. **40–55% · Barrier ladder at the door.** The unseen stranger escalates in steps: polite request → long silence → loud command. Show the threat only in a tight crop (hands, jaw, a prop at the lock) under a color shift away from the warm room palette.
6. **55–68% · Two tells.** First, a logical clue that the stranger is not who he claims (it pays off the step-1 plant). Second, proof that the barrier won't hold (he has the means to get in). The narrator breaks down here.
7. **68–80% · Breach and retreat.** He gets in, so this is the first full reveal of his face. The group retreats to a smaller locked space, and he besieges it. A pre-planted lifeline object is found and its presence explained in one line.
8. **80–88% · Rescue with a sting.** The guardians arrive, the threat has vanished, and the adults don't believe the kids → an objective record (camera, log, witness) proves it.
9. **88–95% · Retro-reveal ladder.** Only after safety: it was targeted (he'd been watching) → it wasn't only us → he was caught → what he really was (worst plausible label). Each line is darker than the one before.
10. **95–100% · Bookend sign-off + silent sting.** A first-person "never forgot it" line closes the step-2 promise. Then a wordless shot returns to the opening location with an ambiguous figure, and the picture fades. No CTA.

**Visual rules borrowed:**
- Plant the threat **silently in the background** of the opening shots (a lone figure at the edge of frame) and once mid-story (a figure in a window), then pay it off with "footage" late.
- Withhold the antagonist's face until the breach.
- Use macro inserts for props that change the plot: game pieces for the baseline, the key card at the lock, the phone, the call screen, the CCTV monitor, the mugshot board.
- Palette shift: warm interior for safety, desaturated green-gray for the threat.

**Pacing targets:**
- ~450 words over ~165 s.
- About 2–3 deliberate silent beats of 3–8 s, each covered by SFX.
- Jolt gaps around 10–13 s in the setup, tightening to 3–8 s from the 50% mark.
