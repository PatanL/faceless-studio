# Mom's Note, Day 1, WrONG Rules (annotated)

| Field | Value |
|---|---|
| URL | https://www.youtube.com/watch?v=cVUJmsVkUW4 |
| Title | "Horror Stories \| Mom's Note Day 1 \| Scary Animation" |
| Channel | WrONG Rules (channel median 9,400 views over the 30 most recent uploads) |
| Views | 290,919 |
| Outlier score | **30.95x** |
| Duration | 135 s (2:15) |
| Upload date | 2023-08-14 |
| Format | 16:9 YouTube animated "rules note". The whole script is a note from a mother to her daughter, read aloud by a calm female voice. The note is a list of survival rules for one night alone at home. The art is soft, painted anime-style stills of one girl (red sweater, red headband) in a small apartment, with slow pushes and crossfades. Hand-lettered captions run along the bottom; key words are coloured (red for danger or safety items, blue for "blue"). Full-screen black title cards carry the most important rules. Glitch effects (RGB split, black-and-white, neon colour inversion) mark the threat moments. |
| Total words | **323 spoken** (42 transcript lines), plus 2 caption-only lines seen on the frames (0:23, 1:30; 9 words, possibly spoken but dropped by whisper) = **332** |
| Words/min | **~144 wpm** over the full runtime (323 / 2.25 min); ~151 wpm over the spoken span 0:00–2:12 including the caption-only lines. That is slow and deliberate, about half the speed of the TikTok horror reposts (~280 wpm). Average line is 7.7 words, about 3.1 s. |

Sources:
- Transcript: `raw/cVUJmsVkUW4.txt` (faster-whisper small on the Spark CPU plus auto-subs; 0:29–1:12 rebuilt from the burned-in captions).
- Frames: `sheets/cVUJmsVkUW4.jpg` (about one frame every 4 s) and the 1 fps sheets on the Spark at `~/studio/refs/corpus_horror/sheets/cVUJmsVkUW4/s_001..012.jpg` (sheet k covers seconds 12(k-1) to 12k-1).

Lines are quoted verbatim for internal research only. Never reuse the wording, the mother's-note premise details, the colour rules, the doll or the closet.

**Key mechanic, the rules list *is* the story:** there is no narrator action, dialogue or plot beyond the rules. Every line is a second-person imperative from a trusted parent, and the picture shows the girl obeying it. Horror comes from three things:
1. **Implied threats.** Each rule implies a danger that is never named ("creature", "dark shape", "blue eyes").
2. **If/then branches.** The rules fork ("if you spot... / if they are... / if not..."), so the viewer simulates the danger.
3. **Hidden contradictions.** The note says to throw out everything blue or white, then later says to bring the blue and white things back in, that a *white* closet is safe, and that *blue* eyes may be inside it. It also says the lights must stay on, and then one must go off. The viewer starts to suspect the note, or whoever wrote it, can't be trusted. That drives comments and the Day 2 click.

The parents' absence is never explained. It is the master loop for the series.

## 1. Line-by-line

| Time | Line (verbatim, internal only) | Beat | Device | Purpose | Visual |
|---|---|---|---|---|---|
| 0:00 | My sweetie, you're back home safe. | Hook (frame) | Second-person "you", warm direct address, false safety | Sets the frame: a parent speaking to a child who is alone. "Safe" is said so it can be taken away | Close-up of the sad girl holding a folded note, green wall, dresser |
| 0:02 | But you've got to follow every single word to stay alive. | Hook (stakes) | "But" reversal, life-or-death stakes, rule/warning | Flips safety to mortal danger in 4 s; tells the viewer every following line matters | Same close-up; captions "every single word to stay alive" |
| 0:06 | This note is your lifeline. Got it? | Hook (contract) | Fake authority (the note itself), rhetorical question, emphasis word (LIFELINE) | Makes the note the rulebook, so the viewer listens like the girl does. "Got it?" is a beat for the viewer too | Girl from behind at the table, note on the table; 0:09 ghosted double-exposure of her face with big "GOT IT" caption (pattern interrupt) |
| 0:10 | First thing, lock the big door and the bathroom door so no creature can get in. | Rule 1 / setup | Countdown/ordinal ("First thing", big red caption), rule, unnamed threat ("creature", in red) | Starts the checklist; "creature" is the first spoken hint of a monster, and it is never explained | Red "FIRST THING" caption over the ghosted face, then the girl turning a door lock in profile |
| 0:16 | Use newspapers to cover all the windows. | Rule 2 | Rule, oddly specific instruction | Specific, physical, easy to picture; the viewer wonders what is outside | Girl from behind taping newspapers over a window |
| 0:19 | Block that light, like your life depends on it. | Rule 2 (stakes) | Life-or-death idiom | Reasserts the stakes; light becomes a motif (it matters in the bathroom later) | Same newspaper window |
| 0:23 | (caption only) Because it does | Re-hook | Literalised idiom, punch line (3 words, large green caption) | Turns the idiom into a literal threat; small shock at the 17% mark | Large bold green caption over the newspaper shot |
| 0:24 | I have left a red doll for you. | Talisman (setup) | Object plant, colour coding ("RED" in red) | Introduces a protective item and the colour rule system; a Chekhov's gun used at 0:52 | Painted doll in a red dress on a white floor; 0:25 black-and-white triple-doll stutter frame |
| 0:26 | Keep it close. Don't let it wander away from you. | Talisman (open loop) | Rule/warning, implied agency ("wander" means the doll can move) | One word makes the protector itself uncanny; opens "what is the doll?" | 0:26 blurred dark ghost figure flash (jump frame), doll again, then an inverted dark doll and a dark red frame |
| 0:29 | Remember to look around for anything blue or white. | Rule 3 / color hunt | Colour rule ("BLUE" in blue), "remember" | A new, arbitrary rule; the viewer starts tracking colours (sets up the later contradictions) | Dark vignette, slow push on a blue stool in an empty room |
| 0:33 | Trash them now. | Rule 3 | Short imperative, urgency ("now") | Punch line; no reason given, which is the scary part | Same stool |
| 0:35 | If they're big, get them in the bathroom. | Rule 3 (branch) | If/then branch | First conditional; ties the colour rule to the bathroom set piece | Girl dragging the blue stool toward a frosted-glass door |
| 0:38 | You have to remember to knock on the bathroom door before you open it. | Rule 4 / escalation | Ritual rule, "you have to" | Knocking on your own bathroom implies something lives in there; key escalation | Girl from behind at the frosted bathroom door, hand on the light switch |
| 0:42 | [title card] Only then... | Re-hook | Title card on black, ellipsis, sequence word | Pattern interrupt; the pause makes the viewer lean in for the next step | Black screen, large hand-lettered "ONLY THEN" |
| 0:43 | [title card] Turn on the light. | Rule 4 | Title card, colour keyword ("LIGHT" in yellow) | The light motif returns; this is a step in the ritual | Black screen, "TURN ON THE LIGHT" |
| 0:46 | [title card] Don't open the door right away. | Rule 4 (warning) | Rule/warning, delay instruction | Builds dread through waiting; the viewer expects something behind the glass | Blue-lit frosted door with a hazy silhouette behind it; door edge in the foreground |
| 0:50 | If you spot a dark shape, | Escalation / first threat image | If/then branch, vague threat noun | First time the threat is *shown*: the shape is on screen as the line is said | 0:48–0:51 tall black silhouette behind the frosted glass, then a dark figure with faint pale eyes |
| 0:52 | kill the light, grab the doll | Escalation (action) | Rapid imperative chain, callback (doll) | Pays off the doll plant; the pace speeds up (two commands in two seconds) | Girl in blue darkness pressing the door shut |
| 0:54 | and run back to Mom and Dad's room. | Escalation (flight) | Location callback ("Mom and Dad's room"), flight | Sends her to the parents' room, which reminds the viewer the parents are gone | Warm-lit shot, girl from behind closing a wooden bedroom door |
| 0:57 | [red title card] Now. | Peak / pattern interrupt | One-word title card, red, hard cut | The loudest beat so far (42% of runtime); a jolt of urgency | Black screen, glowing red "NOW" |
| 0:58 | Close that bedroom door too. | Escalation | Imperative | Seals her in; the camera now shares her hiding POV | Over-shoulder of the girl facing the closed bedroom door, low angle |
| 1:00 | After that, peek under the door to see if the lights in the living room are flickering. | Escalation (surveillance) | Ritual check, sign to watch for (flicker) | Makes the viewer watch the strip under the door with her; flicker means the presence is near | 1:02 RGB-split glitch frame; then the girl staring at the door gap; 1:05 a small light flickers under the door |
| 1:05 | If they are, stay put. | Escalation (branch A) | If/then branch, short imperative | Freeze response; tension through stillness | 1:06 black-and-white glitch frame; 1:07 colour glitch bar |
| 1:08 | If not, check the bathroom again. | Escalation (branch B) | If/then branch | Sends her back toward the threat, which raises dread instead of relief | Same over-shoulder door shot |
| 1:11 | [red title card] Remember, | Re-hook | Title card, red, "remember" | Pattern interrupt; signals that the next line is a repeated, critical rule | Black screen, red hand-lettered "REMEMBER" |
| 1:12 | don't open the door right away. | Re-hook (callback) | Repeated rule (callback to 0:46) | Repetition makes it feel like a ritual and reminds the viewer of the shadow | Black title card with the same white lettering as 0:46 |
| 1:13 | If the shadow disappears, bring in the blue and white things ASAP. | Twist (contradiction 1) | If/then, contradiction (she was told to trash them at 0:33) | The viewer notices the rule reverses itself: are the blue and white things bait, or an offering? Big comment driver | Girl at the open bathroom: tiled room, bucket, wet blue-green stains on the floor |
| 1:19 | Remember, only turn off the light in the bathroom. | Rule 5 (contradiction 2) | "Remember", light rule | Reverses the earlier "turn on the light" with no reason; deepens the bathroom mystery | Close-up from behind: hand on the light switch |
| 1:22 | Keep all the other room lights on. | Rule 5 | Rule | Light means safety everywhere except the bathroom; implies the bathroom thing wants the dark | Same switch shot |
| 1:25 | Foods in the fridge. | Lull (domestic) | Mundane care, tonal contrast | A breath; the mother's warmth makes the horror rules feel worse by contrast | Girl from behind reaching into a bright, stocked fridge |
| 1:27 | Warm it up before eating. | Lull | Mundane rule | Keeps the "rule" rhythm going inside the lull; viewers may read menace into it | Same fridge shot |
| 1:30 | (caption only) But don't eat it all up | Lull (micro hook) | Caption-only aside, mild warning | Small open question (rationing implies a long absence); keeps the lull from going dead | Front shot of the girl, hand on her cheek, tired |
| 1:32 | If you're tired at night, go to our room. | Setup (night) | If/then, location callback | Moves the story to night and to the parents' room again | Girl front-on, sleepy, against a green wall |
| 1:35 | In there, you'll see a white closet. | Setup (contradiction 3 planted) | Colour callback (white) | The careful viewer notices a white object she was told to trash; plants the final scare | Wide doorway shot: small girl, tall white closet on the right; crossfade |
| 1:37 | It's safe, don't worry. | False safety | Reassurance (fake authority), dramatic irony | The reassurance itself is the warning sign; the viewer doesn't believe it | Girl in the doorway, hand on cheek |
| 1:40 | Before you go to bed, check on the closet. | Escalation | Ritual check, contradiction (why check a "safe" closet?) | Undercuts "safe" three seconds after saying it | Profile of the girl at the closet's gap, light grey closet doors |
| 1:43 | Carefully peek through the gap. | Escalation | POV instruction, slow-down word ("carefully") | Puts the viewer's eye at the gap; maximum suspense | Big-eyed close-up of the girl's face, trembling |
| 1:45 | If you see blue eyes watching from inside, shine your flashlight till they vanish. | Peak / reveal | If/then, colour callback (blue), threat image, counter-ritual | Horror peak at about 79% of runtime: the "safe" place has a watcher, and it is blue | 1:46–1:51 the girl's face distorted with neon pink and blue colour inversion and glowing eyes (the strongest visual in the video) |
| 1:51 | One last thing before bed, hang a bag on the outside doorknob. | Ritual / wind-down | Countdown ("one last thing"), title card, offering ritual | Signals the end of the list; the unexplained bag (for whom?) opens a quiet loop | Black title card "ONE LAST THING BEFORE BED", then hands hanging a white plastic bag on a door handle |
| 1:57 | Lock the door and then you go rest. | Resolution (Day 1) | Imperative, comfort | Releases tension; the girl survives the night | "Lock the door" over the bag shot; black card "AND THEN YOU GO REST" |
| 2:01 | Next morning you'll find the second note inside the bedside drawer. | Series hook | Sequel plant, specific location | Turns the episode into Day 1 of a series; the viewer wants note 2 | Girl asleep in bed by a white bedside table |
| 2:04 | But don't read it early. | Cliffhanger (prohibition) | Rule/warning, forbidden knowledge | A prohibition the viewer wants to break; implies note 2 is dangerous or time-locked | Crossfade: the girl awake, reading a sheet of paper in bed |
| 2:07 | Your dad and I trust that you can make it. | Emotional payoff | Parent voice, trust, implied absence | Warm close that reminds the viewer the parents are gone and she is alone | Girl reading, worried |
| 2:10 | You have to make it to the second day, my love. | Cliffhanger / CTA (implicit) | Survival framing, red keyword ("THE SECOND DAY"), episode countdown | Doubles as a "watch the next part" line without saying subscribe | Black screen with "you have to make it to THE SECOND DAY my love" (red highlight), then "To be Continue..." card 2:13–2:15 |

## 2. Structure summary

### Beat sequence (135 s)

| # | Beat | Time | Seconds | % runtime |
|---|---|---|---|---|
| 1 | Hook: warm address, "but" reversal to life-or-death, the note as lifeline | 0:00–0:10 | 10 | 7% |
| 2 | Fortify the home: lock doors (creature), cover windows, block light, "because it does" | 0:10–0:24 | 14 | 10% |
| 3 | Talisman: red doll, "don't let it wander" (ghost flash) | 0:24–0:29 | 5 | 4% |
| 4 | Colour hunt: find blue/white things, trash them, big ones to the bathroom, knock first | 0:29–0:42 | 13 | 10% |
| 5 | Bathroom protocol set piece: title cards, shadow behind glass, kill the light, grab the doll, run, NOW, peek under the door, flicker branch, REMEMBER, bring the blue/white things back (contradiction) | 0:42–1:19 | 37 | 27% |
| 6 | Light rule reversal and domestic lull (fridge, food) | 1:19–1:32 | 13 | 10% |
| 7 | Night closet: "our room", white closet "safe", peek through the gap, blue eyes (horror peak) | 1:32–1:51 | 19 | 14% |
| 8 | Bedtime ritual: bag on the outside doorknob, lock, rest | 1:51–2:01 | 10 | 7% |
| 9 | Series cliffhanger: second note, don't read it early, trust, "make it to the second day", "To be Continue..." | 2:01–2:15 | 14 | 10% |

### Hook

- Lines 1–3 (0:00–0:10): **24 words in about 9–10 s**, about 150 wpm, the same calm pace as the body. The hook relies on contrast, not speed.
- Structure: warm safety line, then a "but" with life-or-death stakes, then the note named as the rulebook plus a check question ("Got it?").
- No threat is named in the hook. The first concrete threat word ("creature") arrives at 0:13.
- Visual: a sad close-up holding the note, then the girl from behind with the note on the table, then a ghosted double-exposure on "Got it?" as the first pattern interrupt.

### Re-hooks

There is a new rule, threat, branch or title card at these times:

0:02, 0:06, 0:10, 0:13, 0:19, 0:23, 0:24, 0:26, 0:29, 0:33, 0:38, 0:42, 0:46, 0:50, 0:54, 0:57, 1:00, 1:05, 1:11, 1:13, 1:19, 1:30, 1:35, 1:37, 1:43, 1:45, 1:51, 2:01, 2:04, 2:10

- **Median interval: about 3–4 s; mean about 4.3 s.** The rules-list format re-hooks almost by definition, since every line is a new instruction.
- The biggest gap is **1:19 to 1:30 (about 11 s)**, the fridge lull. It is deliberate and carried by tonal contrast.
- **Title cards on black** (0:42, 0:43, 0:46, 0:57, 1:11, 1:12, 1:51, 1:57, 2:10, 2:13) work as a pause-and-punch device about every 10–15 s in the middle of the video.
- **Picture cadence:** a new still or effect about every 3–4 s, slower than TikTok horror (about 2 s). Slow pushes and crossfades fill the time.

### Open loops

| Loop | Opens | Development | Closes? |
|---|---|---|---|
| L1 Where are Mom and Dad, and why a note? | 0:00 (implicit) | "Mom and Dad's room" 0:54, "our room" 1:32, "your dad and I" 2:07 | Open: the series master loop |
| L2 What is the "creature"? | 0:13 | Shown as a shadow behind glass (0:46–0:51), and as blue eyes in the closet (1:45) | Open; never named, two possible forms |
| L3 What does the red doll do? | 0:24–0:26 ("don't let it wander") | Used at 0:52 ("grab the doll") | Half closed (it's the escape talisman); why it might wander stays open |
| L4 Why blue and white? | 0:29 | Reversed at 1:13 (bring them back in); white closet is "safe" (1:35); blue eyes (1:45) | Open; contradictions point to bait or an offering, the main comment driver |
| L5 What's behind the bathroom door? | 0:38 (knock first) | Shadow 0:46–0:50; flicker check 1:00; "if the shadow disappears" 1:13; only the bathroom light goes off 1:19 | Conditional close (the shadow can leave); its nature stays open |
| L6 Why a bag on the outside doorknob? | 1:51 | (none) | Open |
| L7 What's in note 2, and why not read it early? | 2:01–2:04 | (none) | Open; this is the click to Day 2 |
| L8 Can the note be trusted? | Builds from 1:13 (contradiction 1), 1:19, 1:35–1:45 | Never stated, only implied | Open; lets the viewer feel smarter than the character |

Only L3 and L5 close, and only partially. The episode ends calm, with every big loop still open.

### Escalation ladder

1. Passive defence (locks, newspapers).
2. A talisman that might move on its own.
3. An active hunt for dangerous objects.
4. A ritual at a door in your own home (knock, light, wait).
5. The threat is seen (shadow, dark figure behind the glass).
6. Flight ("NOW", a one-word red card).
7. Hiding and surveillance (peek under the door, flicker branch).
8. The rules reverse themselves (bring the blue/white things back, the light goes off).
9. Lull (food).
10. The "safe" place is not safe (a watcher in the white closet), the visual horror peak at about 79%.
11. A strange offering ritual (bag outside), then sleep.
12. A series cliff (the forbidden next note).

The ladder rises twice:
- First peak: the bathroom shadow and "NOW" at 0:46–0:57 (34–42% of runtime).
- Main peak: the closet eyes at 1:43–1:51 (76–82%).

Each peak is followed by a short wind-down: the conditional branches after the first, and the bedtime ritual after the second.

### How it ends

- A **soft landing plus a series cliffhanger**, not a hard cut. Day 1 is survived (the girl sleeps), then the narration plants note 2 with a prohibition ("don't read it early"). The last line restates survival stakes as an episode count ("the second day"), with that phrase in red, then a "To be Continue..." card.
- There is no spoken subscribe CTA. The sequel itself is the CTA, and the title's "Day 1" pre-sells the series.
- The emotional state at the end is warm unease: love from the parent, plus the suspicion that the rules contradict themselves.

### Pacing stats

- About 144–151 wpm: slow, calm and maternal. The horror comes from the content, not speed.
- Average line is 7.7 words, about 3.1 s.
- Punch lines of 5 words or fewer appear at 0:23, 0:33, 0:42–0:43, 0:57, 1:05, 1:11, 1:25–1:27, 1:37, 2:04. That is about every 15 s, usually as a caption or title card.
- About 75% of lines are imperatives; 8 lines are if/then branches.
- About 95% of lines contain "you", explicitly or implied. There is no first-person narrator action at all.

### Visual notes

- **One character, many stills.** One girl (red sweater and red headband, so she always carries the "safe" colour), about 25 distinct painted stills. The sets are: living/dining room with the note, front door lock, newspaper window, doll on a white floor, blue stool, frosted-glass bathroom door (blue light), bedroom door low angle, light switch close-up, fridge, front tired portrait, doorway with white closet, closet gap profile, eye close-up, doorknob with bag, bed.
- **Threat visuals are mostly effects, not new art:** ghost double-exposure, a black-and-white triple stutter, a blurred dark figure flash, a silhouette behind frosted glass, RGB-split and colour-bar glitches, and the neon colour-inverted face for the peak. All of these are easy to make in code (filters, blend modes, offsets).
- **Typography carries the beats:** hand-lettered font. Colour keywords match the rule system (CREATURE, RED, NOW, REMEMBER and THE SECOND DAY in red; BLUE in blue; LIGHT in yellow; "BECAUSE IT DOES" in green). Full-screen black title cards are used for the most important rules.
- **Code-only fit: very high.** A note or paper prop, a captions-with-colour-keywords component, black title cards, a few backgrounds and one puppet character with 4–5 expressions. Glitch and inversion filters add the scares. This is cheaper than the chat-phone format.

## 3. Transferable skeleton (no original wording)

Use this for a 2:00–2:30 "instructions left for you" horror Part 1 (16:9 or 9:16), at 140–160 wpm, about 300–360 words, 35–45 lines. The narrator is an absent guardian; the protagonist is alone, silent and obeys on screen.

1. **Hook, 0–7% (20–30 words, about 10 s):**
   - A warm, personal address telling the protagonist they are safe for now.
   - A "but" line that turns this into life-or-death if any instruction is skipped.
   - The document is named as the only thing keeping them alive, then a one- or two-word check question.
   - Visual: the protagonist holding the document, then a ghosted or stuttered frame on the check question.
2. **Fortify, 7–17%:**
   - An ordinal opener ("first..."), then 2–3 defensive rules about entrances and sight lines. One rule names an unexplained threat in a single word.
   - End with an idiom about survival that is then taken literally as a 3-word punch caption.
3. **Talisman, 17–21%:**
   - The guardian has left a protective object in a signature colour.
   - One rule about keeping it close contains a word implying the object can move on its own.
   - Flash a 1-frame dark-figure or stutter effect.
4. **Arbitrary hunt, 21–31%:**
   - A rule to find and remove everything of one or two specific colours or types, with no reason given.
   - A size-based branch sends the big ones to one specific room.
   - A ritual instruction about that room's door (a signal before entering).
5. **The room protocol set piece, 31–58% (the longest beat):**
   - A sequence of title cards (sequence word, then action, then a delay).
   - The threat appears as a shape behind a barrier.
   - Then a rapid chain of 2–3 commands (darkness, the talisman, flee to a named room) and a one-word red title card.
   - Then hiding plus a surveillance check with two if/then branches (stay or go back).
   - A "remember" card that repeats the delay rule.
   - Close the beat with a conditional all-clear that **reverses an earlier rule** (contradiction 1).
6. **Reversal and lull, 58–68%:**
   - One more rule that quietly contradicts an earlier one (on/off, open/closed).
   - Then 2–3 mundane care instructions (food, warmth). One has a small odd edge suggesting a long absence.
   - Keep it under 12 s.
7. **The "safe" place, 68–82%:**
   - Send the protagonist to the guardian's own space and describe a hiding place in a colour the viewer was told is dangerous (contradiction 2).
   - Reassure that it is safe, then immediately ask for a check of it ("carefully look through...").
   - Peak: if a specific coloured sign of a watcher appears inside, use a counter-ritual to make it go away.
   - Visual: the strongest effect in the video (colour inversion, glow, distortion) on the protagonist's face.
8. **Bedtime ritual, 82–90%:**
   - "One last thing" title card, an unexplained offering or signal left outside a door, lock, rest.
   - Release the tension.
9. **Series hook, 90–100%:**
   - Morning: the next document is waiting in a specific place, with a prohibition against reading it early.
   - The guardian says they trust the protagonist to survive.
   - End on survival stakes framed as the next episode number, with that phrase coloured, then a "to be continued" card. No spoken subscribe.

**Devices to reuse:**
- The whole script as second-person imperatives from a trusted, absent authority.
- Unnamed threat nouns.
- If/then branches that make the viewer simulate the danger.
- Colour-coded rules echoed in caption colours.
- A talisman with a hint of agency.
- Title cards on black for key rules and one-word urgency.
- A repeated "remember" rule.
- At least two planted contradictions that make the rules suspect.
- A "safe" location revealed as watched.
- An unexplained offering ritual.
- A forbidden next document.
- Episode-count stakes as the CTA.

**Pacing targets:**
- A new instruction every 3–5 s; never let a gap run past 12 s.
- A title card about every 10–15 s through the middle.
- Slow, calm voice (140–160 wpm).
- A new picture every 3–4 s, with pushes and crossfades.
- Two peaks: a first sighting at 35–42% and the main horror image at 75–82%.
- Each peak is followed by a branch or ritual wind-down.
