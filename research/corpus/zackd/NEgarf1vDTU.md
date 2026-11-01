# NEgarf1vDTU: Maggots Started Falling From Her Ceiling (Zack D. Films)

> Internal research only, to learn the format. The verbatim lines below are for structure study. Do not reuse the wording, premise, characters, footage, audio or visuals in anything we publish (BRIEF hard rule 5). Run `scripts/originality_check.py` on any script that cites this file.

## Header stats

| Field | Value |
|---|---|
| URL | https://www.youtube.com/shorts/NEgarf1vDTU |
| Title | Maggots Started Falling From Her Ceiling (ends with one 😱 emoji) |
| Channel | Zack D. Films (about 29.5M subs) |
| Role in sample | **Outlier**, top of the "gross" cluster (cluster median 12.5M). Outlier score **2.64** = 29M / rolling median 11M (`channel.json`). |
| Views | 29,889,609 (yt-dlp on the Spark, 2026-11-01). Uploaded 2026-09-30, so about 32 days old. |
| Likes / comments | 506,868 likes (**1.7%**, half the channel median of 3.5%) / about 2,500 comments (**0.008%**, under a third of the 0.028% median). A passive, replayed watch: the reach did not come from engagement. |
| Format | YouTube Short, 9:16 (608x1080, 30 fps), semi-photoreal 3D CG animation, one male narrator voice-over, burned-in captions, a music bed under the whole thing |
| Duration | 33.06 s. Speech runs 0:00.0 to 0:32.4, then a 0.6 s tail on the last shot. |
| Words | **92** (91 heard by faster-whisper small and medium.en, plus "Now" at about 0:16.8, which the on-screen caption shows and a primed re-run picks up faintly) |
| Words/min | **170 wpm** over the speech span (92 / 32.4 s), 167 wpm over the full runtime. The pace dips in the middle and slows down for the ending (table below). |
| Sentences | 7 sentences, 6 to 20 words each (18 / 8 / 10 / 11 / 17 / 8 / 20). Plain declarative past tense, third person ("she", "her"), no "you", no question, no number. |
| Audio | No silence anywhere above -35 dB (the music never drops out). Integrated loudness -12 LUFS, LRA 2.2 LU, so it is heavily compressed. Pauses between sentences are 0.32 to 0.46 s. The **longest pause (0.62 s at 0:16.5)** sits right before the midpoint turn. |
| Transcript | faster-whisper small and medium.en (CPU, int8, 4 threads) on the Spark: `~/studio/refs/zackd/NEgarf1vDTU/NEgarf1vDTU.words.json` and `.words.medium.json` (word timings). The YouTube subtitles returned HTTP 429, so this transcript comes from whisper only. |
| Frames | `sheets/NEgarf1vDTU.jpg`: 9 x 4 grid, 1 tile per second, row-major, tile 1 = 0 s, with the caption visible in each tile. Shot timings were refined from a 2 fps sheet and a 4 fps sheet of 0:06.5-0:10 and 0:16.5-0:26 on the Spark (`sheet2.jpg`, `sheet4.jpg`), plus ffmpeg scene detection (threshold 0.08). Cuts at 1.13, 2.04, 3.74, 4.94, 6.81, 9.54, 14.15, 19.45, 19.99 and 25.73 s. Accuracy is about ±0.25 s. |

### Pacing by section

| Section | Time | Words | wpm |
|---|---|---|---|
| Hook sentence (to "light bulb") | 0:00.0-0:03.7 | 13 | **~210** |
| Multiplication + spread | 0:03.7-0:09.2 | 13 | ~142 |
| Landlord appeal | 0:09.3-0:13.0 | 10 | ~154 |
| Smell / neighbours | 0:13.2-0:16.5 | 11 | ~174 |
| Turn + the woman upstairs | 0:16.5-0:22.2 | 17 | ~178 |
| Police + door | 0:22.5-0:26.5 | 13 | ~190 |
| Follow the smell + reveal | 0:26.5-0:32.4 | 15 | **~136** |

The hook is the fastest stretch, so the premise lands before the thumb moves. The reveal is the slowest, about 0.3-0.7 s per word on "skeleton / curled / up". The ending is said slowly on purpose.

## 1. Line-by-line annotation (verbatim, internal only)

Beat key: HOOK, MULTIPLY, SPREAD, ACT (protagonist acts), CORROB (corroborating second symptom from an independent source), TURN (the point of view moves to the source), PORTRAIT (the hidden subject, alive), STING (social isolation line), AUTH (authority arrives), THRESH (threshold crossing), REVEAL, LOOP.
Device key: ANOM = one small wrong thing inside an everyday action; QTY = counting up without numbers ("one → more → everywhere"); DIR = a spatial pointer (above, upstairs, inside) that aims the viewer's suspicion; SENSE = a second sense (smell) brought in to corroborate; WITNESS = independent witnesses; ISO = a loneliness or invisibility detail; DELAY = a time-lapse word ("eventually"); FOLLOW = the camera or characters literally follow the symptom; NOUN-DROP = the reveal is one concrete noun; POSTURE = a body-position detail added after the reveal noun; SPATIAL-LOOP = the last word mirrors the first location (floor ↔ ceiling); IMPLIED = the cause is never stated, the viewer infers it.

| # | Time | Line | Beat | Device | Purpose |
|---|---|---|---|---|---|
| 1 | 0:00.0 | A maggot dropped from her ceiling | HOOK | ANOM, DIR (ceiling = "from above"), title restated | Says the title back inside 2 s. A single larva (the smallest unit of the anomaly) aims the viewer upward. The first frame already shows the maggot on the bulb, so the visual hook comes before the words. |
| 2 | 0:02.0 | as she was changing her light bulb, | HOOK (context) | ANOM (mundane chore), relatability | Puts the horror inside a chore everyone does. It also explains why her hand is right at the opening in the ceiling, which is the camera's reason to be at ceiling level. |
| 3 | 0:04.1 | followed by more and more. | MULTIPLY | QTY (one → more → more), repetition | The first rung of escalation is pure quantity. The doubled word works like a drumroll and the visual turns into a downpour. |
| 4 | 0:06.2 | They covered her furniture, | SPREAD | QTY (surface coverage) | Moves from the ceiling to every surface. Each surface gets its own macro shot (sofa, cabinet). |
| 5 | 0:07.7 | filling her entire apartment. | SPREAD (peak of rung 1) | QTY ("entire"), totalising word | Ends the invasion rung on an absolute word. The bathroom-counter shot shows them reached even a room she was not in. |
| 6 | 0:09.6 | She begged her landlord | ACT | Emotional verb ("begged"), appeal to an owner | Makes her a sympathetic victim and starts the institutional track (landlord → police) that carries the second half. |
| 7 | 0:11.1 | to investigate the room above her. | ACT / LOOP-OPEN (what is upstairs?) | DIR ("above") | **The key open loop.** The script now names the suspect location without saying what is in it. The camera orbits to the hole in her ceiling as the line is said. |
| 8 | 0:13.3 | At the same time, | CORROB (bridge) | Parallel-timeline connector | Brings in a second storyline without a cut in the narration. It tells the viewer this is a separate clue. |
| 9 | 0:14.2 | the other residents complained about the smell. | CORROB | SENSE (smell), WITNESS (other residents) | A second symptom, of a different sense, from people who don't know the protagonist. Two independent clues now point at one room. "The smell" uses the definite article, as if the viewer already knows which one. |
| 10 | 0:16.8 | [Now] the room belonged to a woman | TURN (at 51% of runtime) | Pivot word after the longest pause (0.62 s) | The point of view leaves the protagonist for good. She is never seen again. The real subject appears at exactly the midpoint. |
| 11 | 0:18.7 | who lived alone, | PORTRAIT | ISO | Shows her alive, eating alone, which humanises the coming reveal. "Alone" is the first hint of why nobody noticed. |
| 12 | 0:20.1 | and the other residents barely knew her. | STING | ISO, WITNESS (callback to line 9) | The same neighbours who smelled her had walked past her without speaking. This is the emotional sting and the hidden explanation of the timeline. The visual shows them passing in the hallway without eye contact. |
| 13 | 0:22.5 | The police were eventually called | AUTH | DELAY ("eventually") | "Eventually" quietly says a lot of time went by. Uniforms raise the stakes from a nuisance to an incident. |
| 14 | 0:24.2 | to check inside. | AUTH / LOOP-OPEN (what is inside?) | DIR ("inside") | Second spatial pointer. The loop has moved from "above" to "inside". |
| 15 | 0:25.4 | When they opened the door, | THRESH | Threshold beat, subordinate clause (no full stop) | The door is the last barrier. The clause stays open, so there is no exit point until the reveal. |
| 16 | 0:26.5 | they followed the smell inside | THRESH | FOLLOW, SENSE (callback to line 9) | The smell clue from 0:14 now guides the reveal. The camera follows the green vapour. |
| 17 | 0:28.8 | where they found her skeleton | REVEAL (at 90% of runtime) | NOUN-DROP ("skeleton", not "body") | One noun answers both clues and implies months, not days, which pays off "barely knew her" and "eventually". The script never says the maggots came from her (IMPLIED). |
| 18 | 0:30.7 | curled up on the floor. | REVEAL coda / LOOP | POSTURE, SPATIAL-LOOP ("floor" → line 1 "ceiling") | The posture detail turns the reveal from a fact into an image. The last word "floor" is the other side of the first location, "ceiling". On replay, "A maggot dropped from her ceiling" now explains itself, so the loop works as a payoff. |

## 2. Escalation ladder

Each rung adds a new **kind** of evidence instead of more of the same. Every rung also narrows where the source is.

| Rung | Time | % | What escalates | Where it points |
|---|---|---|---|---|
| 1. One unit | 0:00-0:03.7 | 0-11 | a single maggot, curiosity and disgust | the ceiling |
| 2. Quantity | 0:03.7-0:06 | 11-18 | "more and more", a downpour | still the ceiling |
| 3. Coverage | 0:06-0:09.2 | 18-28 | every surface, even other rooms | the whole apartment (worst point of the "nuisance" story) |
| 4. Agency | 0:09.6-0:13 | 29-39 | the victim asks someone in charge | **the room above** (named) |
| 5. Second sense | 0:13.3-0:16.5 | 40-50 | smell, from independent witnesses | the same room, from a second direction |
| 6. Identity | 0:16.8-0:19.8 | 51-60 | the room has a person, shown alive | a person, not a place |
| 7. Isolation | 0:20.1-0:22.2 | 61-67 | nobody knew her, which explains the delay | the dread now has a cause |
| 8. Authority | 0:22.5-0:25 | 68-76 | police, "eventually" | inside the door |
| 9. Threshold | 0:25.4-0:28.8 | 77-87 | the door opens, the smell gets worse | the floor of her room |
| 10. Reveal | 0:28.8-0:32.4 | 87-98 | skeleton, curled up | the floor, which is the ceiling from rung 1 |

The story changes genre at 50%: it starts as a gross-out nuisance and ends as a sad, macabre case of a lonely death. The gross-out half gets the click. The second half gives the replay and the share.

## 3. Punchline / twist mechanics

1. **Two clues, one source, no stated link.** Clue A (larvae through the ceiling) and clue B (smell in the hallway) come from different people and different senses. The script never says "the maggots came from her body". The viewer works it out at the word "skeleton", and inferring it yourself hits harder than being told.
2. **The noun does the work of three sentences.** "Skeleton" rather than "body" says that a lot of time passed. That ties back to "barely knew her" and "eventually", so the punchline is also a judgement on the neighbours without any moral spelled out.
3. **Show her alive before the reveal.** The 0:17-0:22 portrait (eating alone, ignored in the hallway) makes the reveal sad as well as gross. That is the second emotion stacked on the first, which is why a "gross" video behaves like a story hit.
4. **The protagonist is only a way in.** The woman downstairs carries the hook and then disappears at 0:16. The camera changes subject at the midpoint, after the longest pause. A Zack D. "news story" introduces the real subject late.
5. **Costume as the ID.** The skeleton wears the same yellow top and dark skirt as the woman at the table. The identification happens visually, so the narration does not need a "that woman" line.
6. **Spatial loop.** The script ends on "floor" and starts on "ceiling". The last shot looks straight down at the floor of the upper flat, the first looks straight up at the ceiling of the lower one. On a replay the opening line means something new, so the loop is a reward, not just a seamless join.
7. **No CTA, no comment on the story.** The narration stops on the reveal image. The last 0.6 s is a slow overhead drift with music only.
8. Fact note for our own scripts: fly larvae do leave a food source to pupate and can crawl long distances through gaps, which is the real basis for this kind of news story. "Skeleton" alongside live maggots is a compressed timeline, though: heavy maggot activity usually comes before full skeletonisation. Our scripts must keep their biology consistent even when the format compresses time.

## 4. Hook

- **Visual hook: frame 0.** Close-up looking up at a hand on a light bulb, with a larva already on the bulb base. It is readable without sound.
- **Spoken hook:** the first sentence clause, **13 words in 3.7 s (~210 wpm)**. Extended through the first escalation ("...more and more") it is 18 words in 5.9 s (~183 wpm).
- The title and the first line say the same thing, so the title's promise is paid in under 2 s and the body runs on "why?".
- Overall **170 wpm**. That is about the same as the channel's mechanism explainers (the horsefly video was 177), but the shape is different: fast hook, mid-tempo middle, slow reveal.

## 5. Shot list

17 shots in 33.06 s, an **average of about 1.9 s per shot**. That is slower than the channel's mechanism explainers (about 1.15 s) because the story runs on long continuous camera moves. The longest takes are the 4.6 s orbit (shot 10) and the 7.3 s final reveal move (shot 17).

| # | Time | Shot type | What's on screen | Camera move | How the visual literalizes the line |
|---|---|---|---|---|---|
| 1 | 0:00.0-0:01.1 | ECU, low angle (looking straight up) | Hand turning a white bulb in a white ceiling fixture. A cream-orange larva sits on the metal base. | Slow push up | "A maggot … ceiling": the single larva is the first thing shown. |
| 2 | 0:01.1-0:02.0 | CU, low angle | Bulb pulled down from the socket, larva on the threads, a second hand reaching | Tilt / slight arc | "from her ceiling": shows the hole the larva came out of. |
| 3 | 0:02.0-0:03.7 | MS, eye level | Woman (short brown hair, white tee with the channel logo, jeans) holding the bulb, recoiling. A larva is on her shirt. Saturated blue walls. | Static then a jolt (shake at about 3.5 s as she flinches) | "as she was changing her light bulb": the chore plus her disgust. |
| 4 | 0:03.7-0:04.9 | CU, low angle | Empty socket in the fixture, larvae crawling out of it, one dropping toward the lens | Slow push | "followed by more": the source opening produces more. |
| 5 | 0:04.9-0:06.8 | Wide, high-ish angle | Larvae pour out of the fixture like rain. She jumps off a chair, the chair tips, she lands. Larvae on the rug and floor. | Slight drop / follow | "more and more": the quantity becomes a downpour, plus slapstick physical comedy (the jump). |
| 6 | 0:06.8-0:07.0 | Macro | Ribbed grey upholstery thick with larvae | Push in, about 0.2 s, then a whip | "They covered": the texture of coverage. |
| 7 | 0:07.0-0:07.6 | Macro, moving | Dark rug and wood cabinet edge streaked with larvae | **Whip pan** (motion blur) | "her furniture": the whip makes it feel like they are everywhere at once. |
| 8 | 0:07.6-0:09.0 | Medium CU | Bathroom vanity, chrome tap, larvae across the counter | Slow dolly along the counter | "filling her entire apartment": even a room away from the source. |
| 9 | 0:09.0-0:09.5 | MS | Bathroom doorway, pull back into the blue living room | Pull back / whip | Transition, the spread reads as wall to wall. |
| 10 | 0:09.5-0:14.1 | MCU → OTS → Wide (one take) | Woman on the phone, hand on chest, distressed. The camera orbits behind her and the hole in the ceiling appears above. Pull back to a wide of the room, larvae on the floor. | **Orbit + pull back**, continuous 4.6 s | "begged her landlord" (MCU on the phone) → "the room above her" (the camera rises to show the ceiling hole as the word lands) → "At the same time" (the wide closes her scene). |
| 11 | 0:14.1-0:17.2 | MS, hallway | Pale blue-grey corridor with an elevator behind. One man kneels at the base of a door, sniffing. Another covers his nose. **Green translucent vapour** leaks from under the door. | Slow push, ends in a **whip pan** | "residents complained about the smell": smell drawn as a visible green glow. |
| 12 | 0:17.3-0:19.4 | MCU | Older woman (grey bun, yellow top) eating soup alone at a table. **Olive / khaki walls** (a new colour = a new apartment). | Slow push / slight orbit | "the room belonged to a woman": shows her alive, doing an everyday routine. |
| 13 | 0:19.4-0:19.8 | Wide, from behind | Her small figure alone at the table in a dim room | Static, then a **flash to white** | "who lived alone": the composition shows her alone. The white flash marks a time jump. |
| 14 | 0:20.0-0:21.4 | MS → Wide, hallway | She walks past the same male neighbour from shot 11. Neither looks at the other. | Tracking with them | "barely knew her": the indifference is acted out. |
| 15 | 0:21.4-0:24.0 | Wide → MCU → MS (one move) | Empty corridor → push into the elevator doors → the doors part on two uniformed police officers (MCU) → they walk out toward camera | **Push in**, then truck back as they walk | "The police were eventually called": the empty corridor before the doors stands in for the wait ("eventually"). The doors opening reveal the authority. |
| 16 | 0:24.0-0:25.7 | MS, hallway | Officers at her door. One pushes and shoulders it. | Static / slight push | "to check inside": a physical effort at the threshold. |
| 17 | 0:25.7-0:33.1 | Interior MS → CU → Wide → **top-down** (one continuous move) | The door swings in, the officers enter and gag. CU of one burying his nose in his elbow, green vapour around him. Pull back and down: in the foreground on a round rug, a **skeleton in the yellow top and dark skirt**, curled on its side, with larvae scattered around and green vapour. The camera cranes up to directly overhead and drifts. | **Continuous**: push → pull back → crane to overhead, slow rotation | "they followed the smell inside" (the camera moves along the vapour) → "found her skeleton" (the pull back puts the body in the foreground as the noun lands) → "curled up on the floor" (the overhead shows the posture and the floor, mirroring shot 1's straight-up view). |

## 6. Visual grammar notes

- **Character design:** stock-looking, semi-photoreal 3D people (a Daz / Character Creator look). The faces are realistic but a little stiff, and the expressions are big and readable from a distance (open-mouth shock, hand on chest, elbow over the nose). Everyone wears simple flat-colour clothes that work as identity tags: white tee for the protagonist, **yellow top for the woman upstairs** (it carries the reveal), blue tee for the neighbour, navy uniforms for the police. Channel branding appears inside the world: the logo on the protagonist's shirt and on framed wall art in both apartments.
- **Palette:** each location has its own colour. Ground floor = **saturated cyan-blue** walls with grey sofa and dark floor. Hallway = **pale blue-grey**. Upstairs flat = **olive / khaki**. The accents are the cream-orange larvae and the **acid-green smell vapour**, and the yellow top stands out on purpose against the olive walls. Overall saturation is medium, the image is clean, and there is no grime or film grain.
- **Lighting:** bright, soft, even, high-key global illumination with no horror shadows. Even the body is lit like a furniture catalogue. The bright, clean light is what lets very morbid content stay watchable and ad-friendly. The only lighting cue is a slight dimming for the "alone" wide (shot 13).
- **Materials:** glossy, slightly translucent larvae with a segmented body, instanced in the hundreds. Fabric shows ribbed upholstery detail in macro, ceramic and chrome have clean reflections, and the floors are pale wood with visible grain. The skeleton is clean ivory, not gory, and still clothed. Smell is a **cartoon convention inside a photoreal world**: a green, semi-transparent volumetric glow.
- **Camera language:** the camera hardly ever sits still. It pushes in, orbits, cranes, and whip-pans as a transition. Low-angle ECUs looking straight up open the video, and a straight-down overhead closes it. Long continuous takes carry two to three lines each (shots 10, 15, 17). The camera reframes to show each new noun as it is spoken (the ceiling hole on "above", the body on "skeleton"). Shallow depth of field is used on the macros. A small camera shake comes with sudden physical action (the flinch, the jump).
- **Cut rhythm:** fast in the gross-out setup (about 1 cut/s, 0:00-0:09.5, with whip pans), then long takes for the story half (4.6 s, 3 s, 2.6 s, 7.3 s). The edit slows down as the dread builds, which is the opposite of the usual "faster toward the climax" rule. Transitions are hard cuts, whip pans, and one flash to white (a time jump).
- **Captions:** white, bold, rounded sans-serif in sentence case with a soft dark drop shadow, no box. One line of **2-3 words** at a time, centred horizontally at about **78% of frame height**, in the lower third over the action. Captions change every 0.4-1 s and follow the speech exactly. There is no highlight word, no emoji and no colour change. The caption text includes "Now" at 0:16.8 even though it is barely audible.
- **Sound:** a constant music bed, compressed to -12 LUFS, so it never goes quiet. Narration is calm, even and news-reader-like, with no performed fear. The flat delivery over gruesome images is part of the tone.

## 7. Transferable skeleton (no original wording)

"Domestic anomaly → hidden source" story Short, 30-34 s, about 90 words, about 170 wpm. Third person, past tense, 7 plain sentences.

| Slot | % of runtime | Job | Rules |
|---|---|---|---|
| S1 Intrusion | 0-11 | One small wrong thing shows up during an ordinary chore. Name the location it came from. | It is in the first frame. Use the title's noun inside 2 s. Say it fast (≥200 wpm). Use a direction word (up, down, behind, inside). |
| S2 Multiply | 11-18 | The single unit becomes many. | Repetition or a counting word, no numbers. One wide "downpour" shot with physical comedy. |
| S3 Coverage | 18-28 | It reaches every surface, even a room away. | 2-3 macro shots of different textures, linked with whip pans. End on an absolute word. |
| S4 Appeal | 29-39 | The victim asks whoever is in charge to check the suspected source. | Name the place, not what is in it (the open loop). The camera shows the place as it is named. |
| S5 Second clue | 40-50 | Independent witnesses notice a different-sense symptom (sound, smell, temperature, light) from the same place. | Use a parallel-time connector. Show the symptom as a stylised visual (glow, ripple, haze). |
| S6 Pause + turn | 50-52 | About a 0.6 s pause, then the point of view moves to the source. The first protagonist leaves. | A one-word pivot. New location, new wall colour. |
| S7 Portrait | 52-60 | Show the hidden subject alive, doing a lonely routine. | Give them one signature costume colour that will be the ID later. |
| S8 Sting | 61-67 | One line of social invisibility that also explains the delay. | Reuse the S5 witnesses on screen, ignoring the subject. |
| S9 Authority | 68-76 | Officials arrive "after a while". | A time-lapse word. An empty space before a reveal (doors, corridor). |
| S10 Threshold | 77-87 | The barrier opens. They follow the S5 symptom inside. | A subordinate clause with no full stop. The camera literally follows the symptom. |
| S11 Reveal | 87-98 | One concrete noun that answers S1 and S5 together and implies how much time passed, plus one posture detail. | Never state the causal link. The costume colour confirms who it is. Say it slowly (~135 wpm). The last word is a place that mirrors S1's location, so the replay explains the hook. |
| S12 Tail | 98-100 | About 0.5 s, music only, slow overhead drift. | No CTA, no moral. |

Visual rules to carry over: bright, even, non-horror lighting on dark subject matter; a colour code for each location; stylised visible symptoms inside a realistic world; long continuous camera moves in the story half that reframe to each new noun; first and last shots as opposite camera angles (straight up / straight down).
