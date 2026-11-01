# I Gave Her a Ride: Wansee Short (annotated)

| Field | Value |
|---|---|
| URL | https://www.youtube.com/shorts/x--ui6_mAxE |
| Title | I gave her a ride, but she was..... |
| Channel | Wansee Entertainment, Shorts tab (median of the 25 most recent Shorts: 15,000 views) |
| Views | 141,758 (4,413 likes, 75 comments at collection) |
| Outlier score | **9.45** (views divided by the Shorts median) |
| Duration | 15 s (0:15) |
| Uploaded | 2023-05-05 |
| Format | YouTube Short, 600×800 (3:4) at 25 fps. Flat 2D cartoon animation (Wansee house style: thick outlines, desaturated greens and greys, limited motion made of expression swaps and slow pushes). A top black bar carries a **burned-in title caption for the whole 15 s** ("I gave her a ride / But she was....", white sans). A bottom black bar carries the red WANSEE ENTERTAINMENT logo. No word-by-word captions. Single first-person narrator. Description is only "#shorts / Horror Story Animated by Wansee Entertainment". The "again" in line 2 and the named character suggest it is cut from a longer Wansee story, but that is not verified |
| Total words | **35** spoken in 5 lines (yt-dlp auto-subs, en-orig VTT with word timings) |
| Words/min | **140 wpm** over the full 15 s; about **167 wpm** while actually speaking (35 words in about 12.6 s of speech). By line: L1 about 180, L2 about 120 (the name is drawn out), L3 about 235 (fastest, on the reveal), L4 about 175, L5 about 190 |
| Person | First person: 4 uses of "I/me/my" (11% of words). The entity is "she/her" (3) and named once. No "you" |
| Silence | One deliberate gap of **1.3 s (0:05.8 to 0:07.1, 9% of runtime)** with no narration, exactly while the entity is first fully visible. Two micro-gaps of 0.3 s and 0.7 s |

Sources: `raw/x--ui6_mAxE.txt` (timestamped lines), refined here with the VTT word timings (`dgx-spark:~/studio/refs/corpus_horror/x2/subs/x--ui6_mAxE.en-orig.vtt`). Video `dgx-spark:~/studio/refs/corpus_horror/x2/vid/x--ui6_mAxE.mp4`. 2 fps frames `dgx-spark:~/studio/refs/corpus_horror/x2/frames/x--ui6_mAxE/f_0001..0030.jpg` and one overview sheet `dgx-spark:~/studio/refs/corpus_horror/x2/sheets/x--ui6_mAxE/overview.jpg` (8×4 tiles, tile n = second (n-1)/2; all 30 checked visually). Download and frames ran on the Spark CPU (`nice -n 10`, ffmpeg `-threads 2`). Lines are quoted verbatim **for internal research only**. Never reuse the wording, the character, the car-ride premise or the creature design. "Mary talish" is the auto-sub spelling of the name and is probably a mishearing.

**Key mechanic:** this is the **minimum viable horror Short**: one location, two characters, five lines, one transformation. The title caption ("I gave her a ride, but she was....") stays on screen the whole time, so the open loop is literally visible in every frame and the narration only has to close it. The picture runs **about 2 s ahead of the words**: the driver's eyes slide sideways at 0:03.5, the woman is in the back seat by 0:05, her tongue drops at 0:07.5, and only then does the narrator say she is "not human". The viewer gets the scare first and the confirmation second (show, then tell), and the 1.3 s silence sits on the first full reveal. The threat closes distance in every beat, from the back seat to the driver's cheek, and the video cuts on a "smile" line with no resolution.

## 1. Line-by-line

Timestamps are VTT word starts (the raw file merges L1 and L2 under 0:00; the VTT puts L2 in its own cue at 0:03.3). The visual column comes from the 2 fps frames.

| Time | Line (verbatim, internal research only) | Beat | Device | Purpose | Visual |
|---|---|---|---|---|---|
| 0:00 | *(caption, on screen 0:00–0:15)* I gave her a ride / But she was.... | Hook: persistent title | Trailing-ellipsis cliffhanger caption, kind act + "but" | Opens the only loop that matters before a word is spoken, and keeps it open on screen for the entire runtime, so a viewer joining mid-scroll still gets the premise | Top black bar, white text, every frame |
| 0:00.7 | just as I got into my car | Hook: mundane setup | First person, ordinary action, "just as" (timing word implies interruption) | Places us in a small enclosed space in 7 words. "Just as" tells the viewer something is about to happen | 0:00 empty driver headrest seen from the back seat (POV of whoever sits behind), a pale shape enters at 0:00.5; 0:01 cut to frontal shot of the driver, neutral face, dark back seat behind him |
| 0:03.3 | I saw Mary talish again | Recognition / re-hook | Named character + **"again"** (implied history, a sequel feeling) | Tells us he knows her and has met her before, so the viewer assumes a backstory and a pattern. Raises "why is she here?" without explaining | 0:03 driver blinks; **0:03.5 his eyes slide sideways** before anything is visible; 0:04.5 a figure appears at the left edge of the back seat; 0:05 woman fully visible: blonde hair, black hollow eye sockets |
| 0:05.8–0:07.1 | *(silence, 1.3 s)* | **Silent reveal** | Held beat, no narration, dramatic irony (viewer sees her, the words have not said what she is) | The biggest scare lands with no voice over it, which makes it feel real-time. The viewer's own reaction fills the gap | Two-shot held: rotting woman behind, driver staring sideways; his mouth starts to open at 0:07 |
| 0:07.1 | this time she was not looking like a human | Transformation / escalation | "This time" (callback to "again"), negation ("not ... human") | Confirms in words what the viewer already saw, and the callback implies she looked normal before, so the change is new and worse | **0:07.5 her tongue drops out to her chest**, driver's mouth opens in a scream; **0:09 cut to a side-profile close-up** of the driver, sweating, screaming toward the back |
| 0:09.5 | but rather a ghost or a zombie | Escalation: naming | Two monster categories joined by "or" (the narrator can't classify it) | Not knowing *which* monster is scarier than knowing; it also gives commenters something to argue about | 0:09.5 the back seat is dark, then from 0:10 she leans forward out of the dark behind the headrest, long tongue reaching toward him (about 0:10–0:12) |
| 0:12.7 | and she gave me a creepy smile | **Ending sting** | Human gesture made wrong (a "smile" from a monster), "and" (flat, final) | A normal social signal becomes the threat. Ending on it, with no escape or explanation, leaves the viewer in the car | 0:12–0:15 her face is beside his, tongue at his cheek/neck, held to the last frame |

## 2. Structure summary

### Beat sequence (15 s)

| Beat | Time | Seconds | % of runtime | Words | wpm |
|---|---|---|---|---|---|
| Caption hook + mundane setup | 0:00–0:03.3 | 3.3 | 22% | 7 | about 180 (while speaking) |
| Recognition ("again") + first sighting | 0:03.3–0:05.8 | 2.5 | 17% | 5 | about 120 |
| Silent reveal | 0:05.8–0:07.1 | 1.3 | 9% | 0 | 0 |
| Transformation + naming (she moves closer) | 0:07.1–0:12.7 | 5.6 | 37% | 16 | about 205 (while speaking) |
| Smile sting, cut | 0:12.7–0:15 | 2.3 | 15% | 7 | about 190 |

Setup takes **22%**, recognition and the silent reveal take **26%**, and the transformation plus sting take **52%**. The monster is on screen for **two thirds** of the runtime (from 0:05 on).

### Hook

- **Length:** the caption hook is 9 words, on screen from frame 1 to the end. The spoken hook is 7 words in 2.3 s (0:00.7–0:03.0). The first visual threat (a figure in the back seat) arrives at **0:04.5–0:05 (30%)**.
- **Shape:** a kind act + "but she was…" (caption), then an ordinary first-person action with a "just as" interruption cue.
- The first second is an empty seat seen from behind, which already reads as "someone is sitting behind you".

### Re-hook interval

- **Jolts** (new information or a visual shock): 0:00.5 (shape enters), 0:03.3 (name + "again"), 0:03.5 (eyes slide), 0:05 (she's in the back seat), 0:07.1 ("not human"), 0:07.5 (tongue), 0:09 (cut to close-up), 0:10 (she leans forward), 0:12.7 (smile + face at his cheek). That is **about one every 1.7 s** (9 in 15 s). Big jolts (sighting, tongue, lean-in, smile) come **about every 2.5 s**.
- **Shots:** only **3 shots** (from behind the headrest 0:00–0:01, frontal two-shot 0:01–0:09, side-profile close-up 0:09–0:15), so a cut every 5 s. The motion inside each shot (eyes, mouth, entity entering, tongue, lean) changes about every 1.5 s, which carries the pacing instead of cuts.
- **Pattern interrupt:** the 1.3 s silence at 0:05.8, then the camera change to a tighter, side-on angle at 0:09 (the only real cut after the first second).

### Open loops

| Loop | Opens | Closes |
|---|---|---|
| "But she was…" (what was she?) | 0:00 (caption) | Visually at 0:05, verbally at 0:07–0:12 |
| "Again" (who is she, what happened before?) | 0:03.3 | **Never** (implies a prior story, drives "part 2?" comments) |
| What will she do to him? | 0:10 (she leans in) | **Never**; the video cuts on the smile |

### Escalation ladder (the threat gets closer)

1. Empty seat seen from behind (0:00)
2. A familiar person, "again" (0:03)
3. In the back seat, eyes hollow (0:05)
4. Not human (0:07)
5. Grotesque body detail: the tongue (0:07.5)
6. Unclassifiable: one monster or another (0:09.5)
7. Out of the back seat, leaning forward (0:10)
8. Face at his face, smiling (0:12.7)

Every beat shrinks the distance; the last frame has zero distance.

### Ending

No resolution, no escape, no explanation, no CTA. It cuts on the smile while her face touches his. The persistent caption still reads "But she was....", so the last frame and the first frame show the same unanswered question. At 15 s the Short loops cleanly back to the empty seat, which reads as a fresh "someone is behind you" shot (rewatch-friendly).

## 3. Transferable skeleton (no original wording)

Format: a 13–16 s first-person micro-story in one enclosed space, two characters, one transformation. About 30–40 words, about 140 wpm overall (about 170–190 while speaking), 3 shots, one silent beat.

1. **Persistent caption (0–100%).** A one-line title burned into a top bar for the whole video: a small favour or ordinary act, then "but they were…" cut off with an ellipsis. It is the hook and the open loop at once.
2. **Empty-space opener (0–7%).** The first second shows the space where the threat will be (an empty seat, doorway or bed edge) from an odd angle, then cuts to the protagonist.
3. **Mundane setup line (5–22%).** 6–8 first-person words: an everyday action plus a timing cue that implies interruption.
4. **Recognition line (22–39%).** The protagonist sees someone they know, with a word that implies a previous encounter. The protagonist's eyes move toward the threat **before** the threat is visible; the threat then appears at the edge of frame.
5. **Silent reveal (39–48%).** 1–1.5 s with no narration while the entity is fully visible. The viewer gets the scare before the words.
6. **"Not human" line (48–63%).** A negation that confirms what the viewer saw, with a callback to the earlier encounter. One grotesque body detail appears on screen as it is said; cut to a tighter, side-on close-up of the protagonist.
7. **Can't-classify line (63–80%).** The narrator names two different monster types joined by "or". The entity moves out of its position toward the protagonist.
8. **Wrong-gesture sting (80–100%).** The entity does an ordinary friendly gesture (smile, wave, greeting) at zero distance. Cut on it. No escape, no explanation.

**Pacing rules:** a new jolt about every 1.5–2 s; visuals lead narration by about 2 s (show, then tell); only 3 shots, with motion inside the shot doing the work; the monster on screen for the last two thirds; the fastest speech on the transformation line; the only silence on the first full reveal. Keep the caption static and readable in the top bar and leave the bottom bar for the brand mark.
