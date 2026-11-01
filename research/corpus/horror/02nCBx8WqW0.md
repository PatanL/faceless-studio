# Gym kid turns Snapchat stalker: Llama Arts (annotated)

| Field | Value |
|---|---|
| URL | https://www.youtube.com/watch?v=02nCBx8WqW0 |
| Title | Disturbing True Snapchat Stories Animated |
| Channel | Llama Arts (median of the 60 most recent uploads on the Videos tab: 1,850,000 views) |
| Views | 11,900,854 |
| Outlier score | **6.43** (views divided by the channel median) |
| Duration | 286 s (4:46). About 7 s of black and a title card before the first word, speech from 0:07 to about 4:28, then ~15 s of fade to black with music |
| Upload date | 2017-10-12 |
| Format | 16:9 YouTube 2D animated **first-person "true story" read-out** (Family-Guy-style flat vector cartoon). One male narrator, no acted voices, no burned-in captions except the text on the stalker's snaps ("heyy", "why did you remove me?", "answer me bitch!") and one gag caption at the gym. A music bed runs under the whole video. Shots change every 3–6 s: wide room shots, narrator reaction close-ups, and full-screen phone POV inserts for each snap |
| Total words | **743** (creator captions, 49 cues) |
| Words/min | **171 wpm** over the ~261 s of speech, **156 wpm** over the full 286 s. Per 60 s window: 176 · 159 · 166 · 151 · 91 (last 46 s, of which ~18 s is speech). Per 30 s: 85 · 91 · 91 · 68 · 84 · 82 · 73 · 78 · 91. The dip at 1:30–2:00 (68) is the first snap, where two full-screen photo inserts are held with little speech; the 3:30–4:00 window (78) holds the window taps with ~1–1.5 s audio gaps around them (silencedetect at -35 dB: 3:38.5–3:39.8 and 3:41.7–3:42.8) |

Sources: `raw/02nCBx8WqW0.txt` (creator-uploaded English captions, en VTT via yt-dlp on the Spark, one line per cue at its start time). Overview sheet `sheets/02nCBx8WqW0.jpg` (a tile every 5 s). 1 fps sheets: `dgx-spark:~/studio/refs/corpus_horror/sheets/02nCBx8WqW0/s_001..024.jpg` (sheet k covers seconds 12(k−1) to 12k−1); a 3 s overview at `dgx-spark:~/studio/refs/corpus_horror/x2/02n/o_01..02.jpg`, which is what the Visual column is read from, so visual timings are ±2 s. Video (480p) at `dgx-spark:~/studio/refs/corpus_horror/vid/02nCBx8WqW0.mp4`. Lines are quoted verbatim **for internal research only. Never reuse the wording, names, places or plot.**

Caption quirks worth knowing about (creator captions, so there are no recognition errors, only loose grammar):
- "Up until a few days ago. I went to..." (0:09): one sentence, "Up until a few days ago I went to a small local gym in my now previous town". The word "previous" is the plant that 4:11 pays off.
- "a snap on my phone saying from Shaun" (1:29): the notification text "Snapchat from Shaun".
- "The text the picture was hey with two y's" (1:52): "The text on the picture was 'hey' with two y's" (the insert at ~1:54 shows "heyy").
- "I'm sure not even a minute later" (2:20): probably "I swear"; the meaning is "less than a minute later".
- "(Window Taps)" (3:39) is a sound cue in the captions, not narration.

**Key mechanic:** a **true-story stalker escalation told through one app's notification sound**. The title and thumbnail carry the promise ("disturbing", "true", "Snapchat"), so the narration can open with a flat "this happened a week ago" and a slow, comic gym encounter (31% of runtime before the first snap). The horror is a **contact-channel ladder**: in person → he asks for my handles → a creepy selfie snap at night → I remove him → instant angrier snap → I block him → he makes a new account → a photo of **my front lawn** → taps on **my window**. Each rung is a safety action by the narrator that fails within minutes, and each failure is shown as a full-screen phone insert with a few words of on-image text. The climax is a **power reversal**: the narrator is a grown man (stated mid-story as a reframe), so instead of hiding he yanks the stalker in through the window and knocks him out. The ending closes the legal loop (police witness a death threat), pays off the "previous town" plant (he moved away), then reopens the story through the medium itself: any new friend request could be the same person.

## 1. Line-by-line

N = narrator (the only voice). Snap text = on-image text in a phone insert. Timestamps are caption-cue starts.

| Time | Line (verbatim, internal only) | Beat | Device | Purpose | Visual |
|---|---|---|---|---|---|
| 0:00 | (no speech, music in) | Pre-roll | Title card | Series branding; the title promises "true" and the app | Black, then a dark card with a yellow ghost-style app badge and the series title (0:06), fade out |
| 0:07 | This happened a week ago | **Hook (frame)** | Recency claim, 5 words | "True and fresh": the event is still live for the narrator, which licenses everything that follows as testimony | Title card fading out |
| 0:09 | Up until a few days ago. I went to a small local gym in my now previous, New Jersey town called Black Bear Fitness | Setup (credibility) | Specific real-sounding place (state + named business); "now previous" | Concreteness reads as truth. "Now previous town" is a quiet plant: why did he leave? (closed 4:11) | Street exterior: a small gym storefront |
| 0:16 | One day I had the misfortune of running into some skinny awkward Yet creepy looking kid probably 18 years old | **Villain intro** | Three-adjective sketch ending on "creepy" + an age number | The antagonist arrives at 6% of runtime, first as a social nuisance with one creepy word | Gym interior: thin dark-clothed kid standing by the treadmills, a joke poster on the wall |
| 0:24 | he didn't look like he belonged in a gym at all | Setup | Out-of-place detail | "He doesn't belong here" is the first wrongness cue | Same, the kid hovering among regulars |
| 0:28 | I had headphones in and I was doing my set when I heard him saying something to me, but it was muffled by the music | **Inciting (contact)** | Boundary violation, sensory detail (muffled voice) | First unwanted contact: he breaches a personal space the narrator signalled as closed | Narrator (blond, tank top, earbuds) curling a dumbbell on a bench; the kid steps in from the right |
| 0:34 | I was already annoyed with this kid given that he was breaking an unwritten rule of the gym | Setup | Narrator's attitude stated | Sets the tone as irritated, not scared, so the later fear has room to grow | Narrator close-up, earbud cable visible |
| 0:39 | "Don't try to talk to somebody when they're doing their sets." | Setup | Quoted social rule (on screen as a caption box) | A comic rule the viewer recognizes; first sign the kid ignores social rules, which predicts he will ignore bigger ones | Two-shot, the rule written in a box at top of frame |
| 0:43 | I took my time finishing my set and then took my headphones out to ask if he needed something | Setup | Small passive-aggressive action | Relatable gym-etiquette humor; makes the narrator likable | Narrator close-up, side-eye |
| 0:48 | Then he started acting like I looked familiar but right away I knew this kid was just trying some pathetic attempt at making friends | Escalation (social) | Fake-familiarity pretext | The stranger invents a connection, a classic grooming/stalker opener; played as pathetic, not dangerous | Two-shot: narrator on the bench, kid talking |
| 0:56 | I assured him I didn't but the kid wouldn't stop talking to me | Escalation | Refusal ignored | Second ignored "no" | Same two-shot, held |
| 0:59 | I'll skip most of the conversation | Transition | Narrator ellipsis | Signals pace control: the storyteller cuts boredom, which builds trust | Same; the kid scratches his head |
| 1:01 | But eventually he actually asked me for my Instagram and Snapchat. weirdly enough and for whatever reason I gave them to him | **Fatal mistake** | Self-blame confession ("for whatever reason") | The narrator hands over the channel the whole horror will come through; the viewer shouts "why?" | Two-shot, then a comic smoke-puff gag (~1:09) |
| 1:08 | Instead of just saying something like buddy I'm trying to work out or I don't have social media | Aside | Hindsight alternative | Turns the mistake into a lesson the viewer can apply; first "it could have been avoided" note | A washed-out, sepia "what I should have done" cutaway (~1:12) |
| 1:15 | After I gave him my snapchat and Instagram however, I did kind of urge him to let me resume my workout | Setup | Polite brush-off | Third boundary statement | Two-shot |
| 1:20 | He finally seemed to get the message and walked away not without saying bye like three times though | Release (comic) + plant | Numbered quirk ("bye like three times") | Laugh line that is also a tell: he can't take a hint and repeats himself (repeated contact is the whole plot) | The kid walks off to the right, the narrator alone on the bench |
| 1:29 | That night I got a snap on my phone saying from Shaun | **Escalation 1 (channel)** | Time cut + notification | The threat moves from the gym into the home, through the phone; 31% of runtime | Night: narrator on a couch in a dark living room, red T-shirt |
| 1:33 | I Immediately sigh and said "Oh no" just wondering why the hell the kid would snap me | Reaction | Annoyed sigh, not fear | Keeps the register comic; dread stays with the viewer | Couch wide shot |
| 1:40 | I opened the snap and the kid was in a creepy weird pose | **Reveal (image 1)** | Phone-POV insert | First full-screen look at the stalker as he chooses to present himself | Full-screen selfie: huge white eyes, face pushed at the lens, head on hand, phone edges framing it (held ~6 s) |
| 1:44 | Face way too close to the camera with his head resting in his hand and a half smile on his face | Description | Precise physical description of a photo | Lets the viewer picture the image while it's on screen; "way too close" is the distance motif in miniature | Same insert |
| 1:52 | The text the picture was hey with two y's I muttered the words " What the Fuck" | Escalation | Tiny text detail ("two y's") + profanity punchline | A trivial detail made creepy by its eagerness; the curse is the comic release | Insert with "heyy" at the bottom (~1:54), then the narrator's flat, unimpressed close-up |
| 2:00 | For the record I'm a guy, which made this even more weird | **Reframe** | Narrator identity reveal mid-story | Recasts the contact as obsessive rather than romantic; also plants that the narrator is physically capable (paid off 3:48) | Deadpan close-up |
| 2:04 | My thought process was I've had enough of this loser already. I'm gonna remove him and make it clear | Decision | Stated plan | Opens the loop "will removing him work?" | Couch wide, then close-up |
| 2:10 | I don't want to talk if I see him at the gym again and | Decision | Plan continued | | Close-up |
| 2:13 | So I did I removed him minutes after he sent that snap | **Safety action 1** | Countermeasure | First defense; the viewer expects it to fail | Over-the-shoulder: the narrator watching a cartoon on TV, as if it's over |
| 2:20 | I'm sure not even a minute later again the message popped up on my phone saying snapchat from Shaun | **Escalation 2 (instant reply)** | Time compression ("not even a minute") | The defense fails at once; speed itself is the threat | Narrator on the couch, reaching for the phone |
| 2:28 | I waited a few minutes before opening it | Delay | Held breath | Small suspense pause before the reveal | Same |
| 2:31 | This one was even creepier | Re-hook | Comparative promise | Tells the viewer the ladder is climbing before showing it | Same |
| 2:33 | Now the kid was sitting up on his bed. No smile more of a surprised angry expression | **Reveal (image 2)** | Second photo, contrast with the first (smile → anger; hand → bed) | The mask slips: the friendly pose becomes rage, and we see into his bedroom | Full-screen selfie: wide eyes, flat mouth, dark bedroom behind |
| 2:39 | The text over the image said why did you remove me? | **Escalation 2 (text)** | Accusation as a question | He knows what the narrator did seconds ago; the "he's watching" feeling | Insert with "why did you remove me?" (held ~6 s) |
| 2:43 | Now I went as far as to block him meaning he couldn't snap me anymore | **Safety action 2** | Stronger countermeasure, explained in-world | Closes the channel "for good"; the explanation tells the viewer the rules of the app so the next breach reads as clever and determined | Narrator standing up from the couch |
| 2:48 | That was that I threw my phone on the desk sigh out of relief | **False relief** | Relief beat | The lull before the worst rung (PLAYBOOK B7, ~8 s) | Wide dark room; the phone tossed on the desk |
| 2:56 | Half an hour later my phone goes off saying Shaun added you as a friend and then snapchat from Shaun | **Escalation 3 (workaround)** | Time stamp + double notification | The block is beaten; repeated notification text is now a sting of its own | Dark room, the phone lighting up on the desk |
| 3:03 | he actually made a new account | Escalation | Plain statement of effort | Effort is what makes him frightening: he will spend any cost to reach me | Narrator standing over the desk |
| 3:07 | I opened the snap and felt my heart drop | Re-hook | Body-fear line | The narrator's first stated fear (everything before this was annoyance); a one-line promise of the worst image | Shocked close-up, mouth open |
| 3:10 | It was a picture of my front lawn the text over it "Answer me Bitch" | **Peak reveal (image 3)** | The stalker's photo of the hero's own house + insult | The threat is physically outside, right now. The hook's "disturbing" is paid at 66% of runtime | Full-screen insert: the narrator's house at night, lit windows, "answer me bitch!" at the top |
| 3:16 | The first thing I could think of was how did he find my address? | Open loop | The viewer's question asked out loud | Voices the audience's thought so they stay with the narrator | Narrator lit by phone glow |
| 3:21 | Then I realized snapchat made that new map feature that lets you see where your friends are | **Explanation (real-world hook)** | Real app feature as the mechanism | Grounds the horror in a feature viewers have on their own phones (topical in 2017); makes the story shareable as a warning | Same, phone glow |
| 3:27 | Somehow, I had the balls to open the window to see outside | Escalation (action) | Hero investigates | Reverses the usual hide response; tension through a window | From behind: the narrator at the window, night street outside; he slides it open |
| 3:31 | It was clear out there. I shut the window and the blinds and started considering calling 911 | **False all-clear** | Empty view + barrier closed + help considered | Classic "nothing there" beat; closing the blinds removes our view, so the next sound has to carry the scare | Exterior: the house at night, the narrator's silhouette in a lit window (the stalker's angle); then the blinds shut |
| 3:39 | (Window Taps) | **Peak contact (sound)** | Sound cue in a ~1.4 s gap in the speech | The threat is at the glass; the silence around the taps is the scare | Narrator standing in front of closed blinds, still |
| 3:42 | It was the sound of taps on the window | Reaction | Narrator names the sound | Confirms what the viewer heard; ~1 s gap after it | Same, held stare |
| 3:45 | I took a deep breath and with one swift motion | **Turn (reversal set-up)** | Wind-up line | The breath tells the viewer the narrator is about to act, not hide | Same |
| 3:48 | I pulled up the blind and the window at the same time and pulled the kid into my room by his neck | **Climax (power reversal)** | Victim becomes aggressor; physical contact initiated by the hero | Releases all the built tension as catharsis; pays off "I'm a guy" (2:00) | The stalker's face outside the window, then the narrator hauling him in by the neck |
| 3:54 | I punched him in the face a few times before he was out cold now I called 911 | Climax | Violence + help called | Revenge fantasy closed; authority finally summoned | Narrator with fists up, then on the phone |
| 4:01 | By the time they arrived he was awake cursing me out promising he'd be back and kill me | **Aftermath threat** | Spoken death threat | Keeps danger alive past the knockout; plants the final loop | Stalker on the couch in a black T-shirt, sneering |
| 4:06 | The cops heard it all I didn't even have to make a case the kid was an idiot | Resolution (legal) | Witnessed threat | Justice without paperwork; the comic "idiot" verdict | Two police officers, the stalker, the narrator in the living room |
| 4:11 | Luckily the timing of this worked out well because I just moved a couple days ago out of state | **Callback (plant paid)** | Pays off "now previous town" (0:09) | Physical distance as safety; explains the opening phrasing | Narrator in an airplane seat by a round window, green hoodie |
| 4:17 | Only thing that worries me I don't want to have to make a new snapchat account | Coda | Mundane worry | Lowers the register before the final sting | Same, phone in hand |
| 4:21 | But any time somebody new adds me on the app. I'll never know if it's secretly that Shaun kid again. | **Ending (open loop)** | Lingering paranoia tied to the medium | Leaves the viewer with the same fear about their own friend requests; the threat could return through the same channel | Close-up of a phone with a yellow notification badge, then his face lit by the screen, eyes closing; fade to black (~4:35) |

## 2. Structure summary

### Beat sequence (% of 286 s)

| Range | Beat | Words | % runtime |
|---|---|---|---|
| 0:00–0:06 | Black + series title card, music only | 0 | 2% |
| 0:07–0:15 | Hook frame: "a week ago", "now previous" town, named gym | 29 | 3% |
| 0:16–0:27 | Villain intro: skinny, awkward, creepy, 18, doesn't belong | 31 | 4% |
| 0:28–0:58 | Gym encounter: talks mid-set, the unwritten rule, fake familiarity, won't stop | 110 | 11% |
| 0:59–1:28 | The mistake: asks for handles → narrator gives them → hindsight brush-off line → "bye" three times | 85 | 10% |
| 1:29–2:19 | **Snap 1** at night: creepy close selfie, "heyy", "I'm a guy" reframe, remove him | 137 | 18% |
| 2:20–2:55 | **Snap 2** within a minute: angry bedroom selfie, "why did you remove me?" → block → relief | 89 | 12.5% |
| 2:56–3:26 | **Snap 3** from a new account: photo of my front lawn + insult → how did he find me → the map feature | 81 | 11% |
| 3:27–3:44 | Window check: open, nothing, blinds shut, 911 considered → **taps on the glass** | 40 | 6% |
| 3:45–4:00 | Reversal: yank him in by the neck, knock him out, call 911 | 50 | 5.5% |
| 4:01–4:10 | Aftermath: death threat, cops hear it | 36 | 3.5% |
| 4:11–4:30 | Coda: moved out of state; any new friend request could be him | 55 | 7% |
| 4:31–4:46 | Fade to black, music out | 0 | 5.5% |

Four acts:
- **Social comedy (0:00–1:28, 31%)**: no danger, just an awkward kid and the narrator's one mistake (giving his handles). The register is annoyed and jokey.
- **Notification ladder (1:29–3:26, 41%)**: three snaps, two countermeasures, each beaten within minutes. Each snap gets a full-screen phone insert with a few words of on-image text.
- **Window and reversal (3:27–4:00, 12%)**: the threat moves from the screen to the glass; the hero attacks instead of hiding.
- **Aftermath and lingering hook (4:01–4:46, 16%)**: the law, the move, the paranoia, a long black tail.

The first real menace (the night snap) lands at **31%** and the scariest image (my own house) at **66%**. That is late by PLAYBOOK standards, but the title has already promised a "disturbing" app story and the gym scene has its own comic engine (an etiquette rule, a pathetic stranger, a self-blamed mistake).

### Hook

- **The title and thumbnail are the hook** ("disturbing", "true", the app name). There are ~7 s of black and a title card before any speech, which no current Short could afford.
- The audio opener is **5 words / ~2 s** ("happened a week ago": a recency truth claim). The first block (truth + "now previous" town + a named business) is **29 words / 9 s**.
- First creepy word: 0:16 ("creepy looking kid", ~word 30, 6% runtime). First unwanted contact: 0:28 (10%). First menace inside the story: 1:29 (the night snap, 31%).
- **For our pilots:** the "this happened recently, in a place I've since left" frame is cheap and plants a payoff. But our horror Shorts need a threat in the first 3 s, so the gym-style comic setup would have to be cut to ≤ 15% or opened with a flash-forward to the front-lawn photo.

### Re-hook interval

32 jolts tagged (new information, a new snap, a countermeasure, a reversal, a sound): 0:07, 0:16, 0:28, 0:39, 0:48, 1:01, 1:20, 1:29, 1:40, 1:52, 2:00, 2:13, 2:20, 2:31, 2:39, 2:43, 2:48, 2:56, 3:07, 3:10, 3:16, 3:21, 3:27, 3:31, 3:39, 3:45, 3:48, 3:54, 4:01, 4:06, 4:11, 4:21.

- Gaps (s): 9, 12, 11, 9, 13, 19, 9, 11, 12, 8, 13, 7, 11, 8, 4, 5, 8, 11, 3, 6, 5, 6, 4, 8, 6, 3, 6, 7, 5, 5, 10.
- **Median 8 s, mean 8.2 s.** Before the second snap (to 2:13): median 11 s, mean 11.5 s. From 2:20 on: median 6 s, mean 6.4 s. From the block (2:43) to the knockout (3:54) the jolts come every **3–8 s**.
- The longest dry stretch is **1:01–1:20 (19 s)**: the mistake, the hindsight aside and the brush-off. It survives because it's the self-blame confession viewers argue about.
- **Visual cuts every 3–6 s** throughout; each snap gets a held full-screen insert (~6 s), which is where the per-30 s word rate drops to 68.
- **The notification line is a re-hook device of its own**: "snap from [name]" is repeated three times (1:29, 2:20, 2:56), each time with a shorter delay before it ("that night" → "not even a minute later" → "half an hour later" after a block that should have been permanent).

### Open loops (open → close)

| Loop | Opens | Closes |
|---|---|---|
| Title: what's disturbing about it? | Title / 0:07 | 3:10 (the front-lawn photo) |
| Why is the town "now previous"? | 0:09 | 4:11 (he moved out of state) |
| What does this creepy kid want? | 0:16 | 0:48 (to be friends) → 1:40 (fixation) → 3:10 (he's dangerous). Answered in three worsening stages |
| Why did he hand over his handles? | 1:01 | Never answered ("for whatever reason"); left as the confessional mistake |
| What's in the snap? | 1:29 / 2:20 / 2:56 | 1:40 / 2:33 / 3:10 |
| Will removing him work? | 2:04 | 2:20 (no) |
| Will blocking him work? | 2:43 | 2:56 (no, a new account) |
| How did he find my address? | 3:16 | 3:21 (the map feature) |
| Is he outside? | 3:27 | 3:31 (looks clear) → 3:39 (taps) → 3:48 (yes) |
| "He'll be back to kill me" | 4:01 | 4:11 (I moved) → 4:21 reopened: any new add could be him. **Open at the end** |

One to three loops are open at once. The comedy loops (what he wants) fold into the horror loops; only one loop stays open at the end, and it's tied to the viewer's own app.

### Escalation ladder

- **Channel ladder (the core):** in person at the gym → asks for handles → a snap at night → removed → instant snap → blocked → new account + friend request → a photo of my house → taps on my window → inside my room (pulled in by the hero).
- **Distance ladder:** across the gym → at my bench → in my phone → (his own bedroom, shown) → my front lawn → my window glass → my room.
- **Image ladder (what each snap shows):** a smiling too-close face → an angry face in his bedroom → no face at all, just **my house**. The scariest picture is the one without him in it.
- **Text ladder (on-image words):** a friendly greeting → an accusing question → an insulting command.
- **Countermeasure ladder (the hero's):** polite hint → remove → block → look outside → shut the blinds → consider calling for help → physical attack → call for help. Each step is stronger than the last and the first four fail.
- **Time ladder:** "one day" → "that night" → "minutes after" → "not even a minute later" → "half an hour later" → now (the taps). The intervals shrink as the stalker gets closer.
- **Register ladder:** annoyed (gym) → exasperated cursing (snap 1) → relieved (block) → "heart drop" (house) → calm resolve (the deep breath) → wry ("the kid was an idiot") → uneasy (final line).

### How it ends

- A **power-reversal climax** instead of a hide-and-survive one: the narrator grabs the stalker through the window and knocks him out. The "I'm a guy" reframe at 2:00 is the plant.
- Safety is then stacked three ways: police, a witnessed death threat, and a move out of state that pays off the "now previous town" phrase from the opening.
- The last line reopens the threat through the medium itself (any new friend request could be him), so the viewer leaves with a small paranoia about their own phone. No CTA in the audio; the video fades to black for ~15 s.

### Pacing and device notes for the PLAYBOOK

- **171 wpm** in a single calm first-person voice, slower than the translated TikTok horror (~360 wpm) and close to the other YouTube true-story cartoon (HOTEL-DOOR, 160 wpm).
- **One app, one notification phrase, repeated as a sting.** Each repetition comes faster and after a stronger countermeasure. This is the true-story confession engine with a **channel ladder** in place of a door ladder.
- **Full-screen "phone POV" inserts** with 2–5 words of on-image text are the scare images. Hold each ~6 s with little narration.
- **The scariest image has no monster in it**: a photo of the hero's own house sent by the stalker.
- **A real-world mechanism** (a location-sharing feature) turns the story into a warning viewers share. Our version should use a generic, plausible feature, not a named app.
- **Mid-story identity reframe** ("I'm a guy") recasts the threat and plants the reversal.
- **Silence around a sound cue** (the taps) is the only dead air in the video, ~1–1.5 s on each side.
- **Opening phrasing that plants the ending** ("my now previous town").
- Weak spots to avoid copying: a 7 s title-card pre-roll, a 31% comedy setup, and the 19 s mistake/aside stretch at 1:01–1:20.

## 3. Transferable skeleton (no original wording)

For a **first-person "this really happened to me" stalker-through-a-phone story**, 4–5 min, one calm narrator at ~170 wpm, a cut every 3–6 s, full-screen phone inserts for each message, and a music bed. The title or thumbnail must name the platform type and promise something "disturbing", since the audio opens flat.

| % of runtime | Beat | What happens (abstract) | Device |
|---|---|---|---|
| 0–3% | Credibility frame | One line saying it happened recently, then a specific everyday place in a town the narrator calls their *former* home | Recency truth claim; a plant for the ending |
| 3–7% | The odd stranger | A short sketch of someone who doesn't fit the place, ending on one creepy adjective and an age | Out-of-place detail |
| 7–21% | Boundary ignored | The stranger interrupts the narrator during a private routine, breaks an unspoken etiquette rule (shown as an on-screen caption), invents a reason they've met, and keeps talking after a no | Comic irritation, ignored refusals |
| 21–31% | The mistake | The narrator hands over a way to be contacted and admits they don't know why; a short hindsight aside on what they should have said; the stranger leaves with a small repetitive quirk | Self-blame confession; quirk as a tell |
| 31–49% | Message 1 | That night the first message arrives; a too-close, too-friendly image with one eager word; the narrator curses; a mid-story fact about the narrator that reframes the contact; the narrator cuts the stranger off | Phone-POV insert; identity reframe that plants the climax |
| 49–61% | Message 2 | Less than a minute later another arrives; the face is now angry, the setting is the stranger's private room, and the text accuses the narrator of what they just did; the narrator uses the strongest block available and relaxes | Instant reply; comparative "even worse" promise; false relief |
| 61–72% | Message 3 | After a short lull the block is beaten (a new identity); the image is the narrator's own home from outside, with an insult; the narrator asks how, then works out an everyday feature that leaked their location | Scariest image without the villain in it; real-world mechanism |
| 72–78% | The glass | The narrator looks outside, sees nothing, shuts the window and covers it, thinks about calling for help; then a small sound at the glass, framed by short silences | False all-clear; sound cue as peak contact |
| 78–84% | Reversal | A breath, one fast motion, and the narrator drags the stalker inside and overpowers them, then calls for help | Victim becomes aggressor; pays off the reframe |
| 84–88% | Aftermath | The stalker wakes and threatens to come back; the authorities hear it, so it's settled | Witnessed threat |
| 88–95% | Coda | The narrator has since moved far away (pays off "former home"); a mundane worry about rejoining the platform; the last line: any new contact request could be the same person | Bookend + lingering open loop tied to the viewer's own phone |
| 95–100% | Out | Hold on the narrator's screen-lit face, fade to black under music | Visual sting, no CTA |

Production notes:
- Each message needs its own **full-screen phone insert**: the image, a few words of on-image text, and the notification sound. Repeat the same notification phrase in the narration every time; it becomes the sting.
- Make the three images escalate in **intimacy of place**: their face, their room, *your* house.
- Shrink the time between messages each round and say the interval aloud.
- Leave 1–1.5 s of dead air on both sides of the one sound cue at the window.
- For our Shorts kit, cut the first 31% to ≤ 15% or open on a flash-forward to the house photo; keep the channel ladder, the reframe plant and the "former home" bookend.
- Don't use a real app name, real place names or a real-looking business in our versions.
