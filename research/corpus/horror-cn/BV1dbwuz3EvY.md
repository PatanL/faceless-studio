# 迷雾疑凶 ("Mist: The Suspect"): a dumpling note warns "the killer is coming"

> Internal research for learning the genre. **Do not translate, retell or adapt this story for publication.** Use it to study mechanics, pacing and twist construction only. Anything we publish must be an original, transposed story that passes `scripts/originality_check.py`.

## 1. Header

| Field | Value |
|---|---|
| URL | https://www.bilibili.com/video/BV1dbwuz3EvY |
| Title | 一口气看完【迷雾疑凶】我吃饺子吃出一张纸条，上面写着杀人凶手要来了 ("Watch it all in one go: [Mist: The Suspect] I bit into a dumpling and found a note: the killer is coming") |
| Channel | 杰出影视本人 (Bilibili mid 75872737). Same 【迷雾 X】 anthology as BV1oPbFzDEX6; the hero is again "Chen Jie" (陈杰, called 小杰 by his father). |
| Uploaded | 2026-03-15 |
| Views | 524,623 Bilibili plays (info.json, 2026-11-01). This is the channel's biggest hit in our corpus. |
| Duration | 18:59 (1,139 s). A single complete story. |
| English reposts | **Confirmed but weak.** ChenJie Horror YouTube [vrk6RQ11W6M](https://www.youtube.com/watch?v=vrk6RQ11W6M), "A Note Said 'The Killer Is Coming' — Then the Door Opened": **12,002 views**, uploaded 2026-09-17, six months after the source. It is a 78:37 compilation. This story is the opener and runs 0:00–26:41 (34% of the runtime); the next story (tally marks carved on an arm) starts at 26:41. The repost reuses the original animation with burned-in English captions, an English voice-over and a "ChenJie Horror" corner tag. Its English is a close line-by-line translation of the Chinese captions, which I checked against the OCR for 0:00–7:49. I found no TikTok repost. A Bilibili short cut of the same story, BV1dbwXzcEAM, has 146.7K more views. |
| Text source | **Bilibili served only the first 7:50 to a logged-out client.** Every `playurl` variant returned one `durl` segment with `length` 469,967 ms against a `timelength` of 1,139,072 ms. That held for 360p, 480p and 720p, with DASH and wbi-signed requests, and with html5 and `try_look`. I did not log in. For **0:00–7:49** I OCR'd the burned-in captions (rapidocr, 1 fps, 470 frames), which gave 237 de-duplicated caption lines. The captions are the narration. For **7:50–18:59** I used the English auto-captions of the ChenJie repost and mapped their timestamps back to the source as CN ≈ EN × 0.712. I calibrated that at two points: the cliffhanger line (CN 7:45 = EN 10:53) and the end (CN 18:59 = EN 26:41). The danmaku timestamps agree with the mapping: DNA comments at 17:06–17:08, and "huh? another mastermind?" at 18:55. **Every timestamp after 7:49 is approximate (±10 s) and marked "~".** I did not run Whisper: the captions cover the narration, and Bilibili gave us no audio after 7:50. |
| Files on Spark | `~/studio/refs/horror-cn/BV1dbwuz3EvY/` holds `src.mp4` (480p, first 7:50 only), `src.info.json`, `src.danmaku.xml`, `frames/`, `ocr.jsonl`, `ocr_collated.txt` (Chinese, timestamped), `onscreen_ocr.txt`, `translation_en.txt` (full working translation with CN≈ and EN timestamps, internal only), `sheet.jpg` and `sheet_key.jpg`. `en_repost/` holds `vrk.mp4` (360p), the VTT captions, `vrk_clean.txt` and `sheet_rest.jpg` (the second half, from the repost). |

## 2. Story outline (my summary)

1. **The note in the dumpling.** On New Year's Eve, the narrator (a young man) is eating dumplings with his mother and younger sister when he bites into a slip of paper: observe carefully, the killer is coming. He bins it as a prank. The front door swings open. His mother goes to look, assuming it's the lonely neighbour, and screams. The narrator drags his sister under the sofa. A man in a cap and face mask walks in with a hammer. There are three bowls on the table, so he knows people are hiding. He finds them, and the sister dies, then the narrator.
2. **The loop.** He jolts awake at the table. The note is back, and only he can see it. He reasons that leaving would mean meeting the killer halfway, so he hides his mother and sister in the wardrobe, locks the bedroom, hides behind the curtain and texts the police. The killer flips the sofa, pries the door, stands an arm's length from the curtain, and leaves. Then the family is found anyway, and he dies running.
3. **The frame reveal.** He wakes in a hospital bed with his father and a "Professor Han". Han explains that the narrator is under hypnosis. The murders were real, the cameras were broken, he is the only survivor, and he once saw the killer's face. The hospital is dream layer 1 and the crime scene is layer 2, a dream within a dream that keeps the loop stable. His mother and sister are already dead.
4. **The note was the hypnotist's.** Back in the loop, the note now reads "don't be afraid, it's all your dream; look at the killer's face." He barricades the door; the killer smashes through. The killer is methodical, chose this family, and anticipates every move the narrator makes. He fails through 99 loops. His father begs Han to stop; Han says the police need this.
5. **The faceless face.** He spots a ceiling vent, hides in it, drops on the killer and rips off the mask, and finds a **black shadow where the face should be**. Han offers a pop-psychology rule: dreams can't invent a face you've never seen, so unseen faces stay shadowed. That suggests the narrator never truly saw the killer. His father asks to end it.
6. **First accusation: the father.** Using that same rule, the narrator reasons that the killer knew the flat's layout, their body sizes, the wardrobe's capacity, and that only three people were home. He asks his father where he really was that night. The father was on an unusual New Year's Eve business trip. The narrator accuses him outright, and asks about another woman.
7. **The false solution collapses.** The father swears, offers his business partner, CCTV and dash-cam footage as an alibi, and weeps. The narrator doubts himself; the danmaku at this point starts guessing that the narrator himself did it. He goes back in, loops up to 999 times, still sees only shadow, and gives up.
8. **The pocket watch.** As Han swings a pocket watch to wake him, the narrator realises he had never met Han before the hypnosis, yet Han's face is fully visible in the dream. By Han's own rule, he must have seen it before.
9. **Reality.** He wakes in a lab, bandaged and convulsing. Police are present, and Han wears a surgical mask; in the waking world the narrator has only ever seen his eyes. So Han is the killer. Han is warm and jokey with the police and oddly close with the father.
10. **Two killers.** The killer knew the house too well to be a stranger, so there must have been an insider. Han is the narrator's age and a man, so he isn't the father's lover; he could be the father's **secret son**. The narrator asks Han to take off his mask "out of curiosity", and the face matches. In the formal statement he points at Han, then at his father as accomplice.
11. **Proof and confession.** The father refuses to give blood; the police take a DNA test anyway: father and son. Han confesses. The father filmed the flat's layout and set up the business-trip alibi. Han, a wealthy medical professor with no visible link to the family, had no apparent motive. He volunteered to hypnotise the survivor so that reliving the murders would traumatise him into suppressing the face. The father's motive is gambling debts to loan sharks. Han offered to clear them on condition the father acknowledge him and marry his mother, and Han wanted the family dead.
12. **The coda sting.** The narrator, alone at home on what is still New Year, watches the case go public. Han's mother kneels before reporters. The loan sharks come for the father's debts, and he sends them to the prison. The last beat: he takes the mother's and sister's accident-insurance policies, which *he* bought for them last month with himself as beneficiary, and collects 5 million. The danmaku reacts with "huh? there's another mastermind?" The ending implies that the survivor was a schemer too.

Short lines worth noting for analysis (no more than these): the note 注意观察，杀人凶手要来了 ("observe carefully, the killer is coming"), and the cliffhanger 但在我说出答案之前 ("but before I say the answer…").

## 3. Beat table

The CN text exists up to 7:49. Rows marked ~ come from the English repost, with timestamps mapped to the source.

| Time | Beat | Mechanic | What the viewer believes now | Open loops |
|---|---|---|---|---|
| 0:00 | Bites a note out of a dumpling: observe carefully, the killer is coming | **Found warning** (a rule-card substitute inside a festive object); the title premise lands in 2 s | A prank | Who wrote it? Why "observe" not "run"? (pays off 3:53 / 12:45) |
| 0:04–0:07 | Bins it; the door swings open by itself | Dismissal, then an instant **prank-turns-real** | Something is coming | Who opened it? |
| 0:09–0:22 | Mum goes to check: probably the lonely neighbour whose kid isn't home for New Year | **Trusted adult dismisses danger**; the neighbour line is a red herring and holiday texture | The mother is walking into danger | — |
| 0:24–0:35 | Hero drags sister under the sofa; Mum screams outside | Hiding place #1; the scream is off-screen | Home invasion | Will they be found? |
| 0:37–0:45 | Masked, capped man with a hammer; **three sets of bowls** on the table | **Count clue** (the killer reads the room); antagonist look established | The killer is smart | How many does he think are here? |
| 0:46–0:58 | Hero shoves sister out to run; she's killed; the sofa is flipped and he's killed | First deaths; the killer "already knew" the hiding spot | Hopeless | How did he know? (pays off ~8:54) |
| 1:00–1:10 | Wakes at the table, touches his head: no wound. "Dream or rebirth?" | **Death-loop reset** at the 1-minute mark | It's a time loop | Loop rules? |
| 1:11–1:35 | The same note; he waves it in their faces and they can't see it | **Only-I-can-see message** | Supernatural warning meant for him | Who is it from? (pays off 3:58) |
| 1:36–1:50 | Can't leave, because the killer is already halfway; footsteps arrive | Hero reasoning aloud; timer (the killer's walk) | A survival puzzle | — |
| 1:51–2:12 | Stops Mum, hides her and the sister in the wardrobe, locks the bedroom, hides behind the curtain | Hiding places #2–#3; the wardrobe "only fits two" | A smarter plan | — |
| 2:02–2:06 | "How did he know only three of us were home, on **New Year's Eve** of all nights?" | **Hero flags the anomaly**, then has no time to think it through | Odd, but the story moves on | **The core open loop** (pays off ~8:54, ~16:05) |
| 2:14–2:32 | Sofa flipped, door pried; he stands at the curtain, then leaves. Hero has sent an SMS to the police | Near-miss suspense; the police SMS as false hope | He might survive | — |
| 2:33–2:43 | Sister screams; both dead; hero killed running | Loop death #2 | The loop can't be beaten by hiding | — |
| 2:45–3:01 | Wakes in a **hospital bed**; Dad: "Dad's here." "Where are Mum and my sister?" Dad cries | **Location shift / frame break** | He was rescued? | Where's the family? |
| 3:02–3:25 | Professor Han: you're not awake, I'm hypnotising you; the killer escaped, cameras broken, you're the sole survivor and saw his face | **Trusted source** (doctor, police-sanctioned) **re-frames everything**; the mission is stated | The loop is therapy; the family is really dead | Whose face? |
| 3:28–3:43 | Two-layer dream (hospital = layer 1, crime = layer 2) | Pseudo-technical rule exposition | The frame is rational | Is the hospital real? (pays off ~12:56) |
| 3:51–4:08 | The note now says "don't be afraid, this is your dream; look at the face." The family are already dead | **Changed note** (source revealed); grief beat | Han is the guide | — |
| 4:11–4:30 | Barricade with table and sofa; the door is smashed. "Methodical, targeted: we were chosen prey" | Escalation; a **targeted-victim** deduction | A planned murder | Why this family? (pays off ~17:52) |
| 4:32–4:47 | Kitchen knife fight; the killer is strong and "knows my next move"; dozens of deaths | **Planted tell** (familiarity with the hero's habits); montage compression | Unbeatable killer | How does he know me? (pays off ~11:06) |
| 4:49–5:25 | **Loop 99**: back in the ward. Dad: too cruel, stop. Han insists; "you're not alone" | **Count clue** (99); the helper insists on continuing, a wrong detail in hindsight | Han is devoted | Why so keen? (pays off ~17:34) |
| 5:27–5:44 | Notices a ceiling vent after dozens more loops; hides Mum and sister in the bathroom; climbs in | New tool; the payoff of the "observe carefully" instruction | A plan finally | — |
| 5:46–6:05 | Drops on the killer and rips off the cap and mask | Ambush; unmasking | The answer is coming | — |
| 6:06–6:10 | **The face is a black shadow**; killed | **Unmasking reveals nothing** (blank face) | Blocked | Why no face? |
| 6:12–6:49 | The pain is real. Han: you probably never saw his face; a dream can't invent a face you've never seen | **Fake authority states a rule** that will convict him | The hero never saw the killer | — |
| 6:51–7:06 | Dad: end it. Hero agrees, exhausted | False ending | It's over | — |
| 7:07–7:32 | "Wait… Han said I can't dream a face I've never seen." "I know who the killer is." Killer knew sofa fit, wardrobe fits two, only three home | **Hero re-reads a rule as evidence** | The hero has cracked it | Who? |
| 7:33–7:49 | "Must be close to our family… who else?" Eyes red. "But before I say the answer, one question" | **Cliffhanger withholding the name** (the Bilibili guest preview happens to end here) | It's someone in the room | **Who?** |
| ~7:50–8:26 | Inner monologue: only Dad knows the flat; montage of Dad's love | Suspicion of the beloved parent; sentimental counterweight | Dad?! | — |
| ~8:26–9:19 | "Where were you? A New Year's Eve business trip?" "Did you kill Mum and Lily?" Evidence: layout, hiding spots, the three-at-home, the odd trip | **Accusation of a trusted figure** | Dad is the killer | — |
| ~9:19–10:20 | Dad: you're traumatised, get him therapy. "Another woman?" Dad swears; partner, CCTV and dash-cam alibi; he weeps | **Alibi defence**; the grief seems genuine | Dad is innocent? | — |
| ~10:20–11:20 | Hero doubts himself: skating injury memory; "Dad taught me to fight" (explains the killer knowing his moves) | **False solution collapses** (but the clue is re-stated) | The hero was wrong | Who else knows him? |
| ~11:20–12:30 | Back in; the vent again; shadow face again; gives up and lets himself die; **loop 999**; quits | Despair montage; count escalation 99 → 999 | No answer exists | — |
| ~12:38–12:52 | Han swings a **pocket watch** to wake him. The hero realises he'd never met Han, yet sees his face in the dream | **The rule turns on its author**; the realisation comes during the exit | **Han is the killer** | Proof? |
| ~12:56–13:20 | Wakes in a **lab**; real pain; police present; Han in a surgical mask, so only eyes ever seen | **Real-world layer reveal** confirms the clue | Han is the killer | How to prove it? |
| ~13:28–14:14 | Han is warm and jokey with the police ("you middle-aged guys wouldn't get it") | Villain's charm in plain sight; dramatic irony | Hero knows, room doesn't | Motive? |
| ~14:14–15:04 | "Why us?" Han and Dad share a silent rapport. An insider must exist: two killers. Han is the hero's age and a man, so not a lover; he's a **secret son**. His brows look like young Dad's | **Second deduction** re-convicts the cleared suspect | Dad + Han | Can he prove it? |
| ~15:04–15:30 | "It's stuffy, take your mask off? I'm curious." The face matches the dream | **Test the suspect** (trap via a casual request) | Confirmed | — |
| ~15:36–16:19 | In the formal statement he points at Han, then at Dad. Han realises his own rule was the flaw. Hero lays out the motive: decades as the hidden son | **Summation scene** in front of authority | Case closed? | Proof |
| ~16:37–17:05 | Dad refuses blood: "my son is delirious." DNA test: father and son | **Objective proof** device | Proven | Why? |
| ~17:05–17:50 | Han confesses: Dad filmed the layout; trip alibi; no motive, rich, so unsuspected; hypnosis designed to traumatise the survivor into erasing the face | **Villain monologue** re-explaining the helper role | Han's "help" was the second attack | — |
| ~17:52–18:16 | Dad: gambling debts, loan sharks; Han's condition was to acknowledge him and marry his mother; Han wanted the family dead. "Lighter sentence?" | Motive stack; a pathetic accomplice | Closure | — |
| ~18:16–18:51 | Alone at home, still New Year; public exposure; Han's mother kneels to reporters; loan sharks sent to the prison | Aftermath montage | Bittersweet end | — |
| ~18:51–18:59 | Collects 5 million on the accident insurance **he bought them last month**, himself the beneficiary | **Final sting reversal** (survivor as schemer), unexplained | Was the hero in on it? | Deliberately left open |

## 4. Clue chain

| Clue planted (time) | Where it pays off | Notes |
|---|---|---|
| Note says "observe carefully", not "run" (0:02, 1:13, 1:17 hero questions it) | 3:53 the note is the hypnotist's prompt ("look at the face"); the real task is observation | The hero flags the odd wording himself. The wording is the clue. |
| Note visible only to the hero (1:20–1:35) | 3:58 it's an implant from Han | Converts a supernatural device into a rational one. |
| Three sets of bowls (0:43) | ~8:54 "only you knew only three of us were home" | Count clue; it reads as killer cunning, then as insider knowledge. |
| Killer finds the sofa hiding spot instantly (0:56) | 7:23 "he knew we could fit under the sofa" | — |
| "How did he know only three were home on New Year's Eve?" (2:03) | 7:29, ~8:54 (Dad), ~16:05 (Dad + Han) | **The central fair-play clue.** Raised at 11% of runtime, then buried under action. |
| The wardrobe "only fits two" (2:11) | 7:27 "he knew the wardrobe holds two" | A domestic-knowledge clue. |
| Dad absent from New Year's Eve dinner (the three bowls, 0:43; Dad first seen at 2:53) | ~8:26 the odd business trip; ~17:05 the alibi was planned | Absence as a clue. Never commented on until the accusation. |
| Killer is methodical, chose this family (4:27–4:30) | ~17:52 the motive: the family's existence | — |
| Killer anticipates the hero's moves (4:38) | ~10:50 "Dad taught me to fight" (insider coaching) | Re-stated during the false-solution collapse, so it survives the father's alibi. |
| Han insists on continuing when Dad asks to stop (5:07) | ~17:34 the hypnosis was meant to cause trauma, not recovery | **The wrong detail from the fake authority.** It reads as professionalism. |
| Han and Dad standing side by side at every ward scene (2:53 onward) | ~14:36 their rapport; ~16:05 father and son; DNA ~17:05 | A visual staging clue. They're always paired in frame. |
| The black shadow face (6:06) | 6:42 explained by Han's rule; ~12:45 Han's own face is *not* shadowed | The failure becomes the key. |
| Han's rule: dreams can't invent unseen faces (6:42–6:49) | 7:11 misapplied to Dad; ~12:45 correctly applied to Han | **One rule, two deductions.** The author's own authority figure supplies the logic that convicts him. Danmaku at 6:45 ("the hero never met Han before either") and 7:01–7:02 ("it's that doctor, same eyes") show viewers caught it early. |
| Han's surgical mask in reality (~13:10) | ~13:28 "I'd only ever seen his eyes" | The mask motif mirrors the killer's mask. |
| Han's age, "about my age" (~14:14) | ~14:54 not a lover, so a son | A demographic deduction. |
| Han's eyes and brows look like young Dad (~14:58) | DNA ~17:05 | — |
| Dad refuses a blood sample (~16:40) | DNA match | Refusal as a tell. |
| Insurance bought "last month" (~18:51) | **No payoff.** It is the final sting itself | An unplanted sting. Viewers' earlier "the hero did it" guesses (danmaku 10:42–11:19) make it feel half-earned. |
| Neighbour "Lao Wang" lonely at New Year (0:17–0:22) | Never | Red herring and festive texture; never returns. |
| Police SMS (2:21) | Never; nobody comes | A false-hope device. In the frame, police are only present in the reality layer. |

## 5. Twist inventory

| # | Twist | Type | Setup |
|---|---|---|---|
| 1 | The prank note is real; the door opens (0:07) | Prank-turns-real | The note in the first 2 s; the casual dismissal. |
| 2 | Death resets to dinner (1:00) | Death-loop reveal | The note returns verbatim (1:13). |
| 3 | Only the hero can see the note (1:22) | Private-message anomaly | Waving it in their faces. |
| 4 | It's a hypnosis-induced dream within a dream; the family is already dead; he's the sole survivor (2:45–3:43) | **Frame break / "it's all a reconstruction"** | Note wording "observe"; the impossible loop. |
| 5 | The note was the hypnotist's prompt (3:53) | Re-attribution of a mystery device | Twist 3. |
| 6 | The murder was targeted, not random (4:27) | Motive escalation | The door smashed even through the barricade; the three bowls. |
| 7 | The unmasked face is a void (6:06) | Blank-reveal (anti-twist) | 99 failed loops building expectation. |
| 8 | The mind can't invent faces, so the hero never saw him (6:42) | Authority's rule (a false lead *and* the key) | The shadow face. |
| 9 | "I know who it is", then it's **Dad** (7:19 → ~8:46) | Beloved-parent accusation | Three bowls; the hiding spots; the wardrobe; the absence. |
| 10 | Dad has an alibi; the hero was wrong (~10:00–10:41) | **False solution** | The genuine grief; the CCTV and dash-cam. |
| 11 | Han's face is visible in the dream, so Han is the killer (~12:45) | **Helper-is-the-killer**, convicted by his own rule | Han's rule at 6:42; the reality-layer mask; never having met him. |
| 12 | Han's "therapy" was a second attack meant to erase his face (~17:34) | Help-as-sabotage | Han insisting at 5:07; "you're not alone". |
| 13 | Dad *was* involved: Han is his secret son (~15:00, DNA ~17:05) | **Cleared suspect re-convicted** / double killers | Twist 9's evidence was never refuted, only the alibi. |
| 14 | Dad's motive: gambling debts plus a deal to marry Han's mother (~17:52) | Mundane-greed motive behind the horror | None before; told, not shown. |
| 15 | The hero insured them last month and collects 5 million (~18:51) | **Final sting / unreliable survivor** | Not set up; the danmaku shows viewers half-expected the hero to be guilty after twist 10. |

Structure note: the twists alternate between **external frame** twists (loop → hypnosis → reality lab) and **suspect** twists (Dad → Han → Dad + Han → the hero?). This is the same "helper is the villain" spine as BV1oPbFzDEX6 (the analyst Wang), so it is clearly this anthology's house move. This time it is wrapped in a crime procedural instead of the supernatural.

## 6. GENERIC vs SPECIFIC

**GENERIC: genre conventions anyone can use**

- A warning message found in an everyday object at an ordinary meal; the hero dismisses it; it comes true within seconds.
- A death-loop that resets to the same moment, with the hero touching the fatal wound and finding nothing.
- A message only the hero can see.
- Home-invasion survival puzzles: hiding spots, barricades, a near miss with the killer's breathing inches away, a police call that never helps.
- A frame break revealing that the loop is a reconstruction: a simulation, therapy, VR or interrogation, with the family already dead and the hero the sole witness.
- A mission inside the loop (see the face, find the name), with a counter of failed attempts that escalates (dozens → hundreds).
- Unmasking that reveals nothing (blank, blurred or shadowed).
- A pseudo-scientific rule from an expert (about memory, dreams or perception) that later becomes the key clue.
- "The killer knew our home too well" → insider deduction.
- Accusing a beloved family member; an alibi; self-doubt; the false solution.
- **Helper-is-the-villain**: the expert guiding the hero is the culprit, and his own rule convicts him.
- A cleared suspect re-convicted as an accomplice (two killers).
- Testing a suspect with an innocent-seeming request; a summation in front of the police; a DNA or blood test as objective proof; a confession monologue explaining the "help".
- A last-line sting that recasts the survivor (insurance, inheritance, a secret).
- A festive setting (New Year, a birthday, a wedding) for contrast with violence.
- First-person past tense, a hero who reasons aloud, a caption line roughly every 2 s.

**SPECIFIC: this author's expression; a transposed story must NOT reuse any of these**

- Names and roles: Chen Jie / 小杰, sister Lili (丽丽), Professor Han (韩教授), Officer Wang, the neighbour Lao Wang; the mother, sister and absent father on **New Year's Eve with dumplings**.
- The **note baked into a dumpling** with that exact wording, and its later changed text.
- The masked, capped hammer killer; the specific hiding sequence (under the sofa → wardrobe for two plus the curtain → barricade with table and sofa → ceiling vent ambush).
- The **two-layer hypnosis dream** (hospital = layer 1, crime = layer 2) and its "hypnosis tech isn't advanced enough" rationale.
- The **99 / 999** loop counts.
- The **black-shadow face** combined with the "can't dream a face you've never seen" (Freud-attributed) rule, used first against the father and then against the hypnotist whose face is visible. This exact clue mechanism is the story's signature; do not reuse it in any costume.
- The pocket-watch wake-up as the moment of realisation; the surgical mask in the waking lab.
- The secret son, the father's accomplice role (filming the layout, the business-trip alibi), the gambling and loan-shark debt, and the condition to marry the son's mother.
- The "therapy designed to induce PTSD so the witness forgets the face" motive.
- The coda details: the kneeling mother before reporters, the loan sharks sent to the prison, the **5 million accident insurance bought last month**.
- The exact twist order (note → loop → hypnosis frame → targeted → shadow face → face rule → accuse Dad → alibi → 999 → helper's face → reality lab → secret son → DNA → confession → insurance sting). Even with new names, reusing this chain counts as retelling.
- The quoted lines above, and any phrasing from `translation_en.txt`.

**How to transpose (direction, not a script):** keep the *shape*: a found warning → a loop → a frame break to an expert-guided reconstruction → a blank-reveal → an expert rule → wrong family suspect → the expert's rule turns on the expert → two culprits → objective proof → a sting. Replace every concrete part: a different setting and occasion, a different reconstruction tech (for example, a voice-message archive or a smart-home log replay), a different "can't fake X" rule (sound, handwriting, a habit), a different culprit relationship and motive, and a different sting. The originality gate applies.

## 7. Pacing

- **Density (0:00–7:49, OCR).** 237 de-duplicated caption lines in 470 s, about **30 lines/min** (28–32 in every minute, very flat). About 2,900 Chinese characters, about **370 chars/min (~6.2/s)**. A new caption arrives every **2.0 s** on average. This matches BV1oPbFzDEX6 (368 chars/min), so it's the house tempo.
- **English equivalent.** The repost needs about 5,070 English words for the 19-minute story: about **267 words per source minute**. The repost doesn't speed up; it narrates at about 190 wpm and stretches the story 1.4× (19:00 → 26:41). For our Shorts or long-form, either compress (cut about 30% of lines) or accept the stretch.
- **Line length.** 8–16 characters per caption line, one breath per line. Dialogue and narration share the same caption style.
- **Hook.** Premise at **0:02** (the note); door opens at **0:07**; first scream at **0:30**; first death and loop at **0:58–1:00**. All of the premise, proof and the loop mechanic land inside the first minute.
- **Re-hook interval.** In 0:00–7:49 I count about 40 distinct turns: a **mean of about 12 s**, and never more than 25 s without a new event or deduction. The second half (from the repost) is slower, with about 25 turns in about 11 minutes (mean about 27 s). The slowest stretch is the father's alibi (~9:19–10:41, ~80 s of dialogue and memory), the same "deduction sag" at about 50% seen in BV1oPbFzDEX6.
- **Re-hook phrases (generic):** "the next second…" (下一秒), "before I could…" (还没等我…), "suddenly I realised…" (突然意识到), "wait…" (等等), "a chilling answer surfaced" (毛骨悚然的答案). Loop deaths are compressed into one-line montage beats ("in the following loops I never once…").
- **Act structure (as % of runtime):**

  | Share | Act |
  |---|---|
  | 0–5% | Warning, invasion, first death |
  | 5–14% | Loop and hiding puzzle |
  | 14–20% | Hypnosis frame break |
  | 20–33% | Failed loops and the vent |
  | 33–37% | Shadow face plus the face rule |
  | 37–56% | Accuse the father, then the false solution |
  | 56–66% | Despair, loop 999 |
  | 66–68% | Helper's-face realisation |
  | 68–89% | Reality lab, test, summation, DNA |
  | 89–97% | Confessions |
  | 97–100% | Aftermath and sting |

  The main twist (Han) lands at **67%**, earlier than in BV1oPbFzDEX6 (85%). The last third is a procedural proof sequence, so this story trades shock for satisfaction. It is the channel's biggest hit, which suggests that audiences like a fair-play detective payoff.
- **Cliffhanger / part-2 mechanics.** On Bilibili it's a single "一口气看完" compilation; the 146.7K short cut BV1dbwXzcEAM exists. Natural Part-cut points with a built-in question:
  - 0:58 (killed, then wakes);
  - 2:45 (hospital: "where are Mum and my sister?");
  - 6:06 (the face is a shadow);
  - **7:45 "I know who the killer is, but before I say it…"** (a textbook part-1 ender at 41%);
  - ~12:45 (Han's face is visible);
  - ~16:05 ("Han is your son, isn't he?").
  
  The name-withholding cliffhanger at 7:45 is the strongest generic device here: the hero knows, the viewer doesn't, and a question is posed first.

## 8. Visual vocabulary

- **Art style.** The same flat 2D 沙雕 puppet animation as the rest of the anthology: big heads, thick outlines, stock eyes. The hero's "shock" face has white eyes with tiny or concentric pupils. Squinting, furrowed brows mean suspicion; there are tears for grief. The hero's bandaged head appears in the reality-layer scenes.
- **Characters by costume** (one outfit each):
  - Hero: neon-yellow jacket with a lightning patch, white tee.
  - Mother: purple dress, black bob.
  - Sister: red hair, denim jacket, black skirt.
  - Killer: red cap, black face mask, black jacket, white hoodie, hammer.
  - Father: black T-shirt.
  - Professor Han: long brown hair, green scrubs under a white coat, stethoscope; a blue surgical mask in the reality layer.
  - Police: hi-vis yellow vests marked POLICE, blue shirts.
  - Han's mother: a red suit (kneeling before reporters).
- **Phone UI: almost none.** The only phone is a handheld prop for the police SMS (2:21) — no chat screen, no notes app. The "message" device is a **paper note prop** shown in close-up, with tiny printed text and a large caption overlay; later it's held up to the camera with changed text. This is notably different from the chat-driven stories, and shows that the genre's warning device doesn't have to be phone UI.
- **Rooms and locations:**
  - Dining room (round wooden table, dumpling platter, rice bowls and chopsticks, wooden cabinet).
  - Living room (white sofa, flipped over in kills).
  - Front door (dark frame, the killer silhouetted).
  - Bedroom with wardrobe and curtain.
  - Bathroom.
  - Kitchen (knife).
  - Ceiling vent (close-up grille).
  - Hospital ward (bed, white blanket, blue privacy curtain, grey-blue walls).
  - Reality-layer "lab" (grey walls, police crowd).
  - DNA lab (staff in white with sample tubes).
  - Street with reporters and microphones.
  - Home balcony; insurance office (hero with a folder).
- **Overlays and effects:**
  - Burned-in white captions with a black outline, bottom centre, one line at a time; a small channel watermark top right.
  - A **translucent curtain overlay** over the hero to show hiding (2:27–2:30).
  - A **black radial blur "shadow face"** (6:06).
  - A cartoon dust-cloud fight puff.
  - A **pocket-watch pendulum** swinging in from frame edge.
  - Death cuts straight to the wake-up (no gore; the hammer swing cuts away).
  - The repost adds a "ChenJie Horror" green corner tag and its own English captions.
- **Shot grammar.** Static medium shots; the ward is staged as a fixed three-shot (hero in bed left, Dad centre, Han right) that repeats every return. Unmasking and realisation beats cut to an extreme close-up of the hero's face. The hiding scenes use point-of-view framing (looking down through the vent grille, through the curtain). Cuts come about once per caption line (every 2 s).
