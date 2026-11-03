# VS1Z decode: "The Ancient Jar That Warned an Empire" (RicksClips3000, 30.7M views)

Internal replication study only. Never published. Frame numbers are at 30 fps (F0 = 0.000 s). Narration is quoted
only as short fragments or referred to as "narration line N" (21 lines, `ricks24_beats.json`). Word onsets are
whisper timings converted to frames; caption page starts were measured from the burnt-in captions
(`experiments/three-lane/src/study/VS1Z/tools/caption_pages.py`) and agree with whisper within 2 frames.

Measured context (`ricks24_metrics.json`):
- 1945 frames, 235 words, 3.62 words/s, no dead air.
- One hard cut (F92). 15 gradual transitions. Shot length median 2.8 s (0.4 to 13 s).
- Camera moving in 99.3 % of frames. 41 moves (6.3 per 10 s). Median attack 15 f, release 12 f.
- 3 snaps (attack 3 f or less at 25 px/f or more): F146, F1515, F1794.
- Quiet-frame zoom active 86 %; push-in share 48 %. This video pulls out almost as often as it pushes.

How framing is given: **head** = head height ÷ frame height; **at (x, y)** = the head or subject centre in frame
fractions (x from the left, y from the top). Moves give type, direction, rough distance, ease and frames.

---

## 1. Shot list, F0-F599 (the replicated 20 s: hook through setup)

### Shot 1: F0-F91, one continuous take (narration line 1, "He put ... the emperor")

**What and why.** The subject is the inventor at the jar, already mid-act at F0, with his arm in the dragon's mouth.
The first noun phrase ("a bronze ball in a dragon's mouth") gets the close-up; the third (the emperor) gets the
crane reveal. Every noun is shown on the frame it is said.

| Frames | Words | Picture | Framing | Camera |
|---|---|---|---|---|
| F0-F20 | He, put a, bronze | The inventor, left, with his arm out to a dragon head on the jar. Jar right, a frog at its foot. Throne, drapes and rose window behind, warm candle bowls at left. | Head 0.17 at (0.27, 0.48). Jar 0.75 of the frame height on the right. | Slow drift right and in (about 3 % over 20 f). |
| F21-F33 | ball in | The push into the dragon: the inventor slides off frame left by F27. | — | Fast push-in plus truck right, ~3x magnification in 12 f. Peak at F25 (frame-diff jumps flagged F21-F29). Ease-in about 4 f, then the travel, then a 4 f settle. |
| F33-F58 | a dragon's, mouth | Close-up of the dragon head: open jaws, the ball, the stick arm. At F36-F43 the arm withdraws, leaving the ball in the jaw. Candle-bowl bokeh glows bottom left. | Dragon head 0.6 at (0.45, 0.4). | Slow push (measured move F52: peak 7.8, attack 14). |
| F52-F57 | mouth | A 4-point glint on the ball. | — | — |
| F59-F72 | and | Crane up and over the dragon and the jar's shoulder, then the lid, revealing the throne. | — | Crane up plus tilt down onto the dais, about 14 f with ease-in and ease-out. The jar lid wipes the frame (in-world wipe). |
| F72-F91 | told, the emperor, | The emperor on his throne, frowning, between two helmeted guards. The jar lid is a dark foreground mass across the bottom 25 %. | Emperor head 0.06 at (0.5, 0.42). Lid fills y 0.72-1.0. | Slow push. |

- **Poses and faces (the inventor).** Smug half-lid eyes F0-F13; ring eyes (surprise) at F14, on "bronze", held
  through the push. The emperor and guards frown throughout.
- **Props and graphics.** The bronze ball; the stick arm; a glint on "mouth". There are no labels.
- **Lighting.** A warm interior: candle bowls and practicals with bloom, cool lavender stone, the red and gold throne.
  The light does not change.
- **Join out.** The only hard cut of the video, at F92: a reverse back to the inventor, two frames before the word
  "emperor" ends (F94).

### Shot 2: F92-F224, one take plus a travel (narration line 1, from "if"; line 2)

| Frames | Words | Picture | Framing | Camera |
|---|---|---|---|---|
| F92-F142 | if, this ever, falls, out, | The inventor, left, faces the camera beside the jar; the dragon and ball are at his shoulder. | Head 0.17 at (0.27, 0.48). | Slow push (about 5 % over 50 f). |
| F121-F131 | falls | The ball drops out of the dragon's mouth into the frog below. | — | — |
| F143-F158 | run. | The inventor turns to camera, terrified, arm up. Speed lines radiate. | Head 0.22 at (0.5, 0.55). | **Snap punch-in** at F143-F146: measured peak 55.7 px/f, attack 0, so effectively a 2-3 f zoom of about 25 % recentring on his face. It then holds and creeps. |
| F158-F167 | (the start of line 2) | The travel: the inventor slides out of frame left and the camera flies past the jar down the aisle to the throne. The foreground jar crosses the frame as a wipe at F160-F163. | — | Fast truck and dolly, about 10 f, motion-blurred (measured move F190 region). |
| F168-F192 | The whole court, burst | The emperor, chest-up on his throne, guards at both frame edges. | Head 0.21 at (0.48, 0.38). | Slow push. |
| F193-F224 | out, laughing., You see, | The court bursts out laughing. | Emperor head 0.08 at (0.5, 0.4). The guards flank him; the carpet runs to the bottom of frame. | Pull-back crane: up and back, F193-F210, ease-in and ease-out (measured move F190: peak 32, attack 9, release 18). Then a slow drift. |

- **Faces (the inventor).** Neutral F92; a smirk at F101 ("this"); ring eyes at F109 ("ever"); a 1-frame blink at
  F117; worried/angry at F120 ("falls"); squint at F126 ("out,"); ring eyes at F131; ring eyes plus a grid-teeth
  grimace at F136 ("run."); sweat drop at F143; terrified with an open mouth at F144-F158.
- **Faces (the emperor).** A frown holds through F179. On "burst" (F180-F183) the emperor's face snaps to a grimace,
  then a wide laugh. The guards follow 3-6 f later (staggered), then lean in as cackles, with bodies tilted, from F193.
- **Props and graphics.** The falling ball (F121-F131, gravity, lands in the frog's mouth); speed lines F142-F160;
  the sweat drop.
- **Lighting.** Unchanged.
- **Join out.** A 4-6 f dissolve (F222-F227) to the jar from a new angle. The place is the same; it is a new idea.

### Shot 3: F225-F404, one long move (narration line 3, "You see ... open mouth.")

**Why.** "You see" opens the explanation, so the camera turns from people to the object. The orbit counts the
dragons for "eight dragons coiled around". The push lands on one dragon for "each holding a ball", and the tilt
down lands on the frog for "a frog's open mouth". The picture walks the sentence clause by clause, top to bottom of
the object.

| Frames | Words | Picture | Framing | Camera |
|---|---|---|---|---|
| F225-F300 | there were, eight, dragons, coiled around, a giant | The jar from a high three-quarter on its right; four or five dragons read as a ring; frogs at its foot. | Jar centre at (0.3, 0.42), jar height 0.45. | Orbit left and descend, slowly (measured moves F229-F294: a train of 10-18 px/f peaks, long). |
| F300-F345 | bronze, jar, each, holding | The jar more frontal; the front dragon is centred. | Jar 0.5 → 0.65. | The orbit continues and pushes in. |
| F345-F362 | a ball | Push to the front dragon. The lid leaves the top of frame. | Dragon head 0.12 at (0.5, 0.25). | Push-in, ease-in-out (measured F345: peak 24, attack 34, release 19). |
| F362-F404 | over, a frog's, open, mouth., But | Tilt down the jar's belly to the frog with its open mouth, bottom centre. | Frog 0.18 at (0.35, 0.78). | Tilt down plus push (measured F380: peak 24). Ends nearly still. |

- **Faces.** No characters are in the shot.
- **Props and graphics.** No labels or glints; the jar alone carries the explanation.
- **Lighting.** Unchanged; the jar's blue-grey bronze against warm bokeh.
- **Join out.** A 6 f dissolve (F402-F407) to a new place: the balcony in daylight.

### Shot 4: F405-F535, a crane out and back (narration line 4, "But the emperor ... from a jar.")

**Why.** The line contrasts the emperor's power with the jar. The camera shows that power literally: it cranes up off
the emperor to reveal the army ("biggest army in the world"), then comes back down to his face for "from a jar."

| Frames | Words | Picture | Framing | Camera |
|---|---|---|---|---|
| F405-F426 | the emperor, had the | The emperor on a palace balcony: balustrade, a stone urn, a banner left, red carpet. Day sky with clouds; the city behind. | Head 0.13 at (0.55, 0.40). | Slow push. |
| F427-F445 | biggest, army | The emperor sinks out of the bottom of frame; the parade ground comes into view below, packed with soldiers either side of a red runner up to the city gate. | — | Crane up and tilt down: fast ease-in, slower ease-out (measured F420: peak 15). |
| F445-F497 | in the world, and, he wasn't | The army fills the frame. The emperor is a tiny head at the bottom centre. | Head 0.05 at (0.5, 0.93). | A slow drift. |
| F497-F512 | about, to run | The camera comes back down to the emperor. | — | Crane down; measured moves F481-F507, with a 1 f attack at F507. |
| F512-F535 | from, a jar. | The emperor again, frowning. | Head 0.13 at (0.55, 0.4). | Slow push. |

- **Faces.** A deadpan frown throughout, with one blink.
- **Lighting.** The first light change of the video: interior warm becomes exterior blue-sky day.
- **Join out.** A 5 f dissolve (F533-F538) back to the hall.

### Shot 5: F536-F599, then on into F600 (narration line 5, "Weeks later, a ball fell, but nothing happened.")

| Frames | Words | Picture | Framing | Camera |
|---|---|---|---|---|
| F536-F565 | Weeks, later, a ball | The hall, now with a long table of courtiers behind. The inventor, small, bottom left, asleep standing. Jar centre-left; dragons and frogs ring it. | Head 0.1 at (0.25, 0.6). | Slow push (measured F569: peak 8.8, attack 49). |
| F566-F575 | fell, | A ball drops into a frog with an impact star. The inventor jolts awake: ring eyes, a hair-shock tuft. | — | — |
| F576-F593 | but, nothing | The inventor looks around. | — | — |
| F594-F610 | happened. | The camera rushes right and in past the jar to the frog that caught the ball. The ball sits in its mouth at F600. | — | A fast truck and push, about 15 f, ease-in. It continues into shot 6, so there is no transition. |

---

## 2. Shot list, F600-F1944 (decoded for the thought process, not replicated)

| # | Frames | Narration | Picture and move | Join out |
|---|---|---|---|---|
| 6 | F600-F640 | line 6 | The frog with the ball → top-down on the emperor's wine cup (no ripple) → crane up to the emperor holding the cup. | Travel (one move). |
| 7 | F640-F665 | line 6 end | The emperor on his throne, close; a deadpan push. | 6 f dissolve. |
| 8 | F668-F715 | line 7 | A banquet table: courtiers laughing harder, one falling off the bench. Slow truck. | 6 f dissolve. |
| 9 | F720-F800 | line 8 to "toy" | The emperor on his throne, mid shot. Expression swaps on "called" and "expensive". Push-in. | 5 f dissolve. |
| 10 | F805-F875 | line 8, "threw the inventor out of the city, jar and all." | The city gate: the inventor and the jar on a cart pushed out; guards and market stalls. A push through the arch. | 25 f dissolve (F868-F894; measured 0.87 s). |
| 11 | F880-F955 | line 9, "dragged it up a hill" | Silhouette at sunset: he drags the cart up the slope; the sun flares. A slow truck up the slope. | 24 f dissolve (F935-F959). |
| 12 | F960-F988 | line 9, "lived there alone." | Golden dusk: a camp on the hill, the jar, a fire, the city far behind. | 6 f dissolve. |
| 13 | F990-F1115 | lines 10-12, "Then, one night ... all eight at once." | Moonlit night, blue: he sleeps by the jar ("Z"). On "a ball" the camera snaps to the jar (measured F1022: peak 38.7). Balls drop; on "another" a second; for "all eight" a wide shot as all fall, then an orbit. Hair-shock wake-up F1056-F1083. | Dissolve to a new place. |
| 14 | F1116-F1212 | line 13 | The city gates' iron bars at night with torches: he screams through the bars. Push-in through the bars to his face. | 6 f dissolve. |
| 15 | F1213-F1307 | lines 14-15 | A guard on the wall walk at night, quoted line with mouth flaps; a whip (F1245: peak 36.6) to a second guard. | 6 f dissolve. |
| 16 | F1308-F1380 | line 16 | He walks back with a lantern; the guards laugh behind. A cheap bobbing walk; the lantern swings. | 12 f dissolve to sunrise. |
| 17 | F1381-F1450 | line 17 | Dawn relight: from behind him, the palace far off; on "pile" the palace collapses into a smoke column; birds. A crane-up (F1405, F1434). | Smoke wipe into the jar (F1451-F1460). |
| 18 | F1451-F1650 | lines 18-19 | Inside the jar: a pendulum with eight rods. Push down the shaft; a snap at F1515 (80 px/f); a swing hits a rod. | Travel along the rod. |
| 19 | F1650-F1750 | line 19, "snapped the dragon's jaw open" | The dragon's jaw opens; the ball drops into the frog. A tilt down follows the ball (measured F1717). | 6 f dissolve. |
| 20 | F1750-F1800 | line 20 | A mountain far away gets a puff ("a nudge"); pull back across the landscape (F1794: 102 px/f, the fastest move). | Travel. |
| 21 | F1800-F1855 | line 21 to "biggest" | The jar at sunset; all eight balls drop; push-in. | Dissolve into a cut-away. |
| 22 | F1855-F1944 | line 21 end | A cross-section of the earth: the fault glows under the city ("right underneath them"). Holds to the end. | End. |

Shot-level counts:
- 22 shots in 65 s.
- Places: hall, balcony, gate, hill, camp, city wall, ruins, jar interior, landscape, cross-section.
- The place changes about every 6.5 s, but the hall is revisited 4 times in the first 20 s.

---

## 3. The hook, beat by beat (for the voice and script tracks)

Narration line 1 is one 4.96 s sentence: a hook built as an odd act followed by a warning.

The voice:
- Speaks at 3.8 words/s with no breath until after "emperor" (a 0.18 s pause, F94-F99).
- Pauses again (0.26 s) after "out,".
- Delivers the payoff word "run." alone, loudest: speech energy peaks at F142-F144, about -10.7 dBFS against -12 to
  -18 for the rest of the line.

How the image meets the voice:

| Frame | Voice | Image |
|---|---|---|
| F0 | "He" (onset at F0, no lead-in) | Already mid-act: the arm is in the dragon's mouth, the face smug. There is no title card and no establishing shot. Every element of the story's premise is in frame 0: the inventor, the jar, a dragon, a frog. The emperor is in the background. |
| F14 | (before "bronze", F23) | The face snaps to ring eyes. |
| F21-F33 | "bronze ball in" | The camera rushes to the object being named. |
| F44-F58 | "dragon's mouth" | The close-up on the mouth, the arm withdraws (F36-F43), and a glint on the ball at F52 lands on "mouth" (F58 ±6). |
| F59-F72 | "and told" | The crane up and over to the emperor, arriving as "the emperor" starts (F79-F85). |
| F92 | the end of "emperor" (the pause) | Hard cut back to the inventor: the only cut, used as the "now listen" beat. |
| F99-F117 | "if this ever" | Small face swaps on "this" and "ever". |
| F118-F131 | "falls" | The ball physically falls out (F121-F131), the action illustrating the hypothetical. |
| F126 | "out," | Squint. |
| F136 | (into "run.") | A grimace. |
| F143-F146 | "run." (the loudest word) | A sweat drop, the snap punch-in (55.7 px/f, the hardest camera hit of the opening) and speed lines. The face goes terrified. |

The 0.3 s silence after "run." (F149-F157) plays over the held terrified close-up. The next line ("The whole court")
starts on the travel to the emperor.

The rule: the loudest word gets the hardest camera hit and the biggest face, on the same frame. The pauses are where
the cuts or travels go.

---

## 4. The director's thought process: rules of thumb

1. **One line, one camera thought.** Each narration line is one shot or one continuous move; clauses inside the line
   are beats of that move, not new shots. Line 1 is two takes (split at the only cut); line 3 is one 6 s orbit that
   walks the sentence's clauses down the object.
2. **Show each noun on the frame it is said.** The camera arrives at the thing within about 0-10 frames of its word:
   "bronze ball" → the dragon close-up; "the emperor" → the crane lands on him; "biggest army" → the crane reveals it;
   "frog's open mouth" → the tilt lands on the frog. The shot is chosen by the nouns, the move by the order of the nouns.
3. **Frame 0 is the premise, mid-act.** The protagonist, the object and the stakes (the throne behind) are all in
   frame 0. The character is already doing the odd act, and the face is already a reaction (smug). There is no
   establishing shot: the "establish" comes later as a crane.
4. **The payoff word gets the hardest hit.** Loudest word = a snap zoom (2-3 f) + the biggest face + a mark (sweat) +
   a graphic (speed lines), all on the same frame. The rest of the line runs on slow pushes, so the hit reads.
5. **Cut only once, at the turn.** The one hard cut sits in the pause between the act and the warning. Everything
   else is a short dissolve (4-6 f) or a camera travel: dissolves for a new idea or place, travels when the next
   subject is in the same space (the jar to the emperor, the frog to the wine cup).
6. **Reveal scale by craning, not by cutting.** Power and size are shown by moving the camera off the character to
   the big thing and back: up from the emperor to the army, up from the jar to the throne. The character sinks out
   of frame; the return lands on their face for the line's end.
7. **Explain an object by touring it top to bottom.** "You see" turns the camera from people to the object. An orbit
   counts parts ("eight dragons"); a push isolates one ("each holding a ball"); a tilt follows the logic downward
   ("over a frog's open mouth"). There are no labels or diagrams until the mechanism, which gets an inside view.
8. **Show the abstract with a physical stand-in.** "Nothing happened" is shown by a calm wine cup with no ripple;
   "the biggest army" by a packed parade ground; "a nudge from far away" by a puff on a distant mountain; "underneath
   them" by a cross-section. Every abstract claim becomes one prop in one frame.
9. **Reactions are staged in depth, with stagger.** The emperor reacts first, then the guards 3-6 f later; the
   crowd's laugh is a pull-back so the whole court reads at once. Faces swap on the word, held 6-40 f.
10. **Places change for story time, not variety.** The first 20 s stay mostly in one hall (4 visits) with one
    excursion (the balcony) that the line demands. New places come with new story time ("Weeks later", "one night",
    "next morning"), each with a new light: warm hall, blue day, sunset, moonlight, dawn, then the cross-section.
11. **The camera is never still and alternates push and pull.** Slow pushes carry the lines; pulls and cranes open
    the space on reveals; 3 snaps in 65 s mark the 3 shocks (run, the pendulum hits the rod, the far-away nudge).
    About 6 moves per 10 s, each eased (attack about 15 f).
12. **Depth on every frame.** A foreground mass (the jar lid, the jar's shoulder, the balustrade, the bars), the
    subject in the mid-ground, a lit background with bokeh practicals. Lens blur separates the layers, and transitions
    often use the foreground mass as a wipe (the jar lid, the passing jar, smoke).

Shorter observations:
- Captions carry 1-3 words, swap hard on the word, sit at y 0.71, and run from frame 0.
- No screen shake, even for the earthquake.
- The emperor never changes expression on his own line; he only reacts.
- Two characters carry the whole video, and the main one is on screen about 60 % of the time.
