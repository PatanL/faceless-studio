# V15wrmD5VFs: What Happens When You Are Shot (The Infographics Show)

> Internal research use only. The verbatim lines below are for structure study. Do not reuse their wording, footage or audio in our scripts (BRIEF hard rule 5; run `scripts/originality_check.py` on any script that cites this file).

| Field | Value |
|---|---|
| URL | https://www.youtube.com/watch?v=V15wrmD5VFs (Shorts URL: https://www.youtube.com/shorts/V15wrmD5VFs) |
| Title | What Happens When You Are Shot |
| Channel | The Infographics Show (about 15.5M subs) |
| Format | YouTube Short, 9:16 (240x426 stream checked, 24 fps), clean medical-anatomy 3D CG (anonymous mannequin in a white T-shirt, translucent skin/muscle/organ/skeleton layers), yellow bold captions with a thin dark outline in the **upper** sixth of the frame, one calm narrator, uploaded 2024-11-28. This is not the channel's usual 2D cartoon style. Description: one line saying what a bullet does to your body. |
| Views | 2,975,684 (104K likes, 1.5K comments at fetch time) |
| Outlier score | 11.34 (views / channel median of 262.5K across the 60 most recent Shorts). A low-baseline Shorts feed for a big long-form channel; this Short did about 11x its neighbours. |
| Duration | 0:29 (29.02 s audio, 28.96 s video). **The first 1.1 s has no voice** (title card only); speech runs 0:01.1 to about 0:28.9, so the last word lands right on the final frame. No outro, no music-only tail. |
| Total words | 76 (the raw whisper file shows 77 because it mishears "aside" as "a sign"; the burned-in caption reads "pushing aside") |
| Words/min | 164 wpm over the speech span (76 words / 27.8 s), 157 wpm over the full runtime. Sentence 1 (hook + entry mechanism) is 19 words in 6.6 s, about 173 wpm. Sentence 2 (the ricochet fork) is 26 words in 8.7 s, about 180 wpm, the fastest stretch. Sentence 3 (fragment fork + cascade) is 31 words in 11.4 s, about 164 wpm, slowing into the last words ("intense bleeding" is stretched over about 1 s). |
| Sentences | 3, and each is longer than the one before (19, 26, 31 words). Sentence 3 runs 11.4 s with no full stop. 13 clause lines (avg 5.8 words). Shortest: "When you're shot" (3 words). |
| Pronouns, numbers, questions | "you" only twice (you're, your: 2.6% of words), both in the first 10 s. Zero numbers. Zero questions. Hedge words carry the structure: "sometimes" x3, "often" x2, "especially if" x1. A 3-word escalation refrain appears twice verbatim (0:13.8 and 0:24.5). |
| Transcript | `raw/V15wrmD5VFs.txt` (YouTube subs returned HTTP 429; audio fetched on the Spark and transcribed with faster-whisper small, CPU int8, 4 threads, VAD). Word-start times below are from a second faster-whisper small pass on the Spark CPU with `word_timestamps=True` (audio: `dgx-spark:~/studio/refs/explainer/corpus/exp2/audio/V15wrmD5VFs.wav`), cross-checked against the burned-in captions on the 2 fps sheet. |
| Frames | Contact sheets on the Spark (not copied into `research/library/sheets/`): `dgx-spark:~/studio/refs/explainer/corpus/exp2/vid/V15wrmD5VFs_sheet.jpg` (6 x 5, 1 tile per second, row-major, tile n = second n-1, 29 tiles) and `V15wrmD5VFs_half.jpg` (10 x 6, 2 fps, tile n = (n-1) x 0.5 s). Source video (240p, video only): `dgx-spark:~/studio/refs/explainer/corpus/exp2/vid/V15wrmD5VFs.395.mp4`. Hard cuts (ffmpeg scene > 0.25): 4.25, 10.79, 19.46, 27.33 s; every other change is a continuous camera move or a layer peel. |

Visual style seen on the sheet: a clean, bright "medical textbook" world on a pale blue-white gradient. 0:00-0:01.5 a black pistol enters from the right, aimed across the frame, under a large 3-line yellow title card of the premise phrase (bigger than all later captions). 0:01.5-0:03 the gun fires and the camera follows the bullet alone across empty space. 0:03-0:04 a faceless mannequin in a white T-shirt; a small hole appears in the shirt, then a push-in to the hole glowing faint red. 0:04.3 hard cut: the skin is peeled to a muscle layer (abs) with the hole, 0:06.5 the muscle is peeled to an organ cutaway (liver, stomach, intestines) with the bullet passing through, 0:08.5 the camera orbits to the side, 0:09.5 the back of the body with the bullet leaving through an exit hole. 0:10.8 hard cut on the "but": skeleton + organs from the front, the bullet visibly bouncing around inside the ribcage. 0:15.5-0:16.5 the camera swings to a side view of the spine as the bullet hits a vertebra. 0:17-0:19 pelvis and kidneys with an intact bullet. 0:19.5 hard cut on the second "but": a wide shot of a floating organ set (lungs to intestines) on a darker blue gradient, the bullet entering from the right; 0:21.5-0:22 it bursts into fragments with a red glow. 0:22.5-0:27 a macro close-up of the gut with red vessels lit up and fragments lodged in them. 0:27.3 hard cut back to the opening mannequin, full body; on the final word (0:28.5) a dark-red stain spreads from the small hole. Captions are 1-3 words, change every 0.5-1 s, and sit above the subject. 12-14 distinct shots/layers in 29 s (about one every 2.2 s), but only 4 hard cuts: most motion is camera travel and layer peeling, so the body feels like one continuous object being explored.

Restraint note: no shooter, no face, no scream, no blood until the last 1.5 s. The violent premise is told entirely as anatomy, which is likely what keeps a gunshot Short watchable (and ad-friendly) for a general audience. The one blood image is held for the final word as the stinger.

Fact note: the mechanism is pop-science simplified. Real wound ballistics talk about a permanent cavity (tissue crushed in the bullet's path) plus a temporary stretch cavity; the script merges these into "creates a cavity, pushing aside tissue". Bullets mostly deflect off bone rather than bouncing around "like a pinball". The size claim is shaky: fragmentation depends mainly on velocity and bullet construction (fast, small-calibre rifle rounds are the classic fragmenters; big slow handgun rounds usually stay whole), not on the bullet being "larger". Unverified and partly backwards; check every mechanism before reusing anything like it.

## 1. Line-by-line annotation

Beat key: TITLE (silent title card), HOOK, MECH-n (mechanism step n), FORK (binary "sometimes A / but sometimes B" split), ESC-n (escalation rung n), REFRAIN, CONSEQ (consequence), STINGER (final image/word), LOOP.
Device key: 2P = second-person "you/your"; COND = "when you..." conditional premise; LIST3 = three-item list; LAYERS = outside-to-inside body layers (skin, muscle, organs, bone, vessels); HEDGE = "sometimes/often" frequency word that makes a fork; BUT = contrast pivot with a hard cut; REF = repeated verbatim escalation refrain; WORST = "especially if" worst-case condition; SIZE = size-variable fork (small vs large); CHAIN = participle or relative clause that keeps the sentence open ("causing", "sending", "that cause", "leading to"); PEEL = visual layer peel; BLOOM = visual consequence spreading on the body.

The transcript is split at clause level so each row is one idea. Times are word-start times.

| # | Time | Line (verbatim, internal research use only) | Words | Beat | Device | Purpose (why it keeps viewers) | Visual (sheet tile / shot list) |
|---|---|---|---|---|---|---|---|
| 1 | 0:00.0 | (no voice; on-screen title card "WHEN YOU'RE SHOT") | 0 | TITLE | Silent title card over the threat object | The premise is read before it is heard: 1.1 s of a big yellow 3-line card over a pistol. A scroller gets the whole promise from the thumbnail-like first frame, and the gun gives an instant threat image without showing a person. | 0:00-0:01.5 pistol enters from the right on a pale gradient; large yellow title card top-left |
| 2 | 0:01.1 | When you're shot, | 3 | HOOK | 2P, COND, title restated | Puts the viewer's own body in the premise in 3 words, then stops. The voice repeats the card exactly, so there is zero ambiguity about what the next 28 s are. The title phrase is the whole hook: no question, no number, no "did you know". | 0:01.5-0:03 gun fires; camera tracks the bullet alone across empty space |
| 3 | 0:02.4 | the bullet first creates a cavity, | 6 | MECH-1 (entry) | "first" (promises a sequence), technical noun ("cavity") | "First" tells the viewer there are steps, which opens a step-by-step loop. One technical word makes it feel like real anatomy, not gore. | 0:03 mannequin in a white T-shirt, small hole appears; 0:04 push-in to the hole with a faint red glow |
| 4 | 0:04.2 | pushing aside tissue and tearing through skin, muscle and organs. | 10 | MECH-2 (penetration) | LIST3, LAYERS, PEEL | The three-item list walks outside-in, and each layer gets its own caption card and its own peeled visual layer. The viewer watches the body open in order, which is the satisfying "see inside" payoff the title promised. Ends the first sentence at 26% with the bullet already deep inside. | 0:04.3 hard cut: skin peeled to the muscle layer (abs) with the hole; 0:06.5 peeled to organ cutaway, bullet passing through |
| 5 | 0:08.2 | Sometimes the bullet travels cleanly through your body, | 8 | FORK-1 setup (mild branch) | HEDGE, 2P (last "you" word) | Offers the least-bad outcome first, so the viewer expects a "but". The "sometimes" is a promise of a worse case, which is a 2.7 s micro loop. "Cleanly" sets a low bar the next line breaks. | 0:08.5 camera orbits to the side; 0:09.5-0:10.5 back of the body, bullet exits through a small hole |
| 6 | 0:10.9 | but sometimes it can ricochet around inside, | 7 | FORK-1 turn + ESC-1 | BUT, HEDGE, hard cut on the pivot | Closes the micro loop with the worse branch. The hard cut lands on "but" (0:10.8), so the ear and eye turn together at 38%. "Inside" keeps the threat in the body, not passing through. | 0:10.8 hard cut: skeleton + organs from the front, the bullet visibly bouncing inside the ribcage |
| 7 | 0:13.5 | causing even more damage, | 4 | REFRAIN-1 | REF, CHAIN | A short, vague escalation phrase that says "worse" without a new fact. It keeps the sentence open (participle), so there is no stopping point, and it plants a phrase that will return. | Same shot; bullet lodges against the stomach |
| 8 | 0:15.1 | especially if it hits something like bone. | 7 | ESC-2 (worst case) | WORST, LAYERS (next layer: bone) | Adds the worst-case condition and introduces the hardest layer. The camera swings to the spine exactly as "bone" is said, a visual reward for a very short wait. | 0:15.5-0:16.5 camera swings to a side view of the spine; bullet hits a vertebra |
| 9 | 0:17.5 | Smaller bullets will often stay intact, | 6 | FORK-2 setup (mild branch) | SIZE, HEDGE | Second fork, same pattern as line 5: the mild branch first. The viewer has now learned the rhythm and is waiting for the "but", so this line holds them on pattern alone. Shift from what the bullet does to what kind of bullet it is: a new variable mid-video (60%). | 0:17-0:19 pelvis and kidneys, intact bullet near the spine |
| 10 | 0:19.7 | but larger ones will sometimes break apart, | 7 | FORK-2 turn + ESC-3 | BUT, SIZE, HEDGE, hard cut on the pivot | The second "but" lands with the second hard cut (0:19.5) at 68%. The camera pulls back to a wide floating-organ view, a scale change that resets attention for the final third. "Break apart" promises a burst the viewer then sees. | 0:19.5 hard cut: wide shot of a floating organ set on a darker blue gradient; bullet enters from the right; 0:21.5 it bursts |
| 11 | 0:21.9 | sending fragments in multiple directions | 5 | ESC-4 (fragmentation) | CHAIN, visual burst | One threat becomes many. The only "explosion" frame in the video lands here, with a red glow, at 75%. The participle keeps the sentence running. | 0:21.5-0:22.5 red glow burst; camera pushes into the gut |
| 12 | 0:23.9 | that cause even more damage, | 5 | REFRAIN-2 | REF (repeat of line 7), CHAIN | The refrain returns verbatim, which marks this as the second, bigger wave of the same pattern. Repetition is easy to process at speed and signals "we are near the end". | 0:22.5-0:25 macro close-up of the gut, red vessels lit up, fragments lodged |
| 13 | 0:25.8 | often rupturing blood vessels | 4 | CONSEQ-1 | HEDGE, LAYERS (last layer: vessels) | The deepest, most vital layer is named last. The vessels are already glowing red on screen, so the line confirms what the eye sees. | Same macro shot, vessels highlighted |
| 14 | 0:27.2 | leading to intense bleeding. | 4 | CONSEQ-2 + STINGER | CHAIN, BLOOM, bookend cut | The first and only blood. Cuts back to the opening mannequin (0:27.3) so the small entry hole from 0:03 now blooms into a stain on the last word. Bookend shape: outside view, inside journey, outside view with the consequence. Stops at the bleeding with no survival verdict, so the obvious next question ("do you live?") is left to the comments. | 0:27.3 hard cut to the full-body mannequin; 0:28.5 dark-red stain spreads from the hole; video ends 0:29.0 |

## 2. Structure summary

### Beat sequence with share of runtime (29.0 s, 76 words)

| Beat | Time | Seconds | % of runtime | Words |
|---|---|---|---|---|
| Silent title card over the threat object | 0:00-0:01.1 | 1.1 | 4% | 0 |
| Hook + entry mechanism (premise, cavity, three layers) | 0:01.1-0:08.2 | 7.1 | 24% | 19 |
| Fork 1: clean pass-through vs ricochet, refrain, worst case (bone) | 0:08.2-0:17.5 | 9.3 | 32% | 26 |
| Fork 2: small stays whole vs large breaks apart | 0:17.5-0:21.9 | 4.4 | 15% | 13 |
| Cascade: fragments, refrain, vessels, bleeding + bookend stinger | 0:21.9-0:29.0 | 7.1 | 25% | 18 |

Shape: a "process walkthrough" Short. One continuous journey through the body (outside, skin, muscle, organs, bone, vessels, back outside), carried by two parallel forks that each pick the worse branch. The script never resolves anything: every turn makes it worse, and it stops at the worst point. The middle 47% (two forks) is the bulk; the hook mechanism and the cascade are equal bookends of about a quarter each.

### Hook

- Length: 3 words spoken (0:01.1-0:01.8), preceded by 1.1 s of the same words as a silent title card. With the first mechanism step it is 19 words in 6.6 s (one sentence, ending at 26%).
- Type: second-person conditional that restates the title word for word. No question, no number, no claim of surprise. The premise itself is the hook: the topic is so visceral that just naming it is enough.
- Hooks inside the hook: a threat object on screen from frame 1 (the gun), "first" promising a sequence, and the layer peel that starts at 0:04.3 (the "see inside" payoff begins inside the first 15%).

### Re-hook interval

- Turn points (each is a new, worse fact or a pivot): 0:01.1 premise, 0:08.2 fork 1 opens, 0:10.9 "but" (38%), 0:13.5 refrain (47%), 0:15.1 worst case (52%), 0:17.5 fork 2 opens (60%), 0:19.7 "but" (68%), 0:21.9 fragments (75%), 0:24.5 refrain (84%), 0:27.2 bleeding (94%). After the 7 s opening sentence, a turn lands about **every 2.5-3 s** (mean about 3.0 s from 0:08 to 0:27).
- The two "but" pivots are the big re-hooks, about 9 s apart (0:10.9, 0:19.7), and each is paired with a hard cut. The other two hard cuts sit at 0:04.3 (into the body) and 0:27.3 (back out). So hard cuts come every 6-9 s, and a layer peel or camera move fills the gaps every 1-2 s.
- The verbatim refrain at 47% and 84% works as a rhythmic re-hook: same words, bigger context.

### Open loops

| Loop | Opens | Closes | Notes |
|---|---|---|---|
| A: What happens to my body, step by step? | 0:00 title card, 0:02.4 "first" | 0:28.4 "bleeding" | The spine. Paid off continuously by the layer peel; "first" promises steps that never get numbered. |
| B: Mild branch, then what? | 0:08.2 "Sometimes..." | 0:10.9 "but sometimes..." | 2.7 s micro loop |
| C: What makes it worst? | 0:13.5 "even more damage" | 0:15.1 "especially if... bone" | 1.6 s micro loop |
| D: Mild branch, then what? (same pattern) | 0:17.5 "Smaller bullets..." | 0:19.7 "but larger ones..." | 2.2 s micro loop; the viewer now predicts the "but", which makes it satisfying |
| E: Do you survive? | Implied by 0:01.1 "when you're shot" | Never | Deliberately left open: the video stops at peak damage. Comment bait and a rewatch reason. |

Pattern: one long walkthrough loop, two identical fork loops (mild then worse), and one survival question that the video refuses to answer.

### Escalation ladder

1. Threat object, no victim (gun, bullet in empty space).
2. Entry: a small hole in a shirt (mild, almost clean).
3. Penetration through three soft layers (skin, muscle, organs), shown by peeling.
4. Fork 1 mild: it passes straight through (exit hole).
5. Fork 1 worse: it bounces inside.
6. Worst-case condition: it hits bone.
7. Fork 2 mild: the bullet stays whole.
8. Fork 2 worse: it breaks into fragments (one threat becomes many).
9. Fragments damage the deepest vital layer (vessels).
10. Visible consequence on the outside: the stain spreads.

The ladder climbs on two axes: depth (shirt, skin, muscle, organs, bone, vessels, then back to the surface with the result) and multiplicity (one clean path, one bouncing path, many fragment paths). Each fork deliberately "spends" its mild branch first so the worse branch feels like a fall.

### How it ends

On the consequence itself, with a two-word final clause. No survival verdict, no lesson, no CTA, no logo card. The visual bookend (back to the mannequin from 0:03, now with a blooming stain) gives closure for the eye while the story is left open for the mind. The last word lands within 0.5 s of the final frame, so the Short loops straight into the gun and the title card, and the gun now reads as "here it comes again".

### Pacing and device notes for the PLAYBOOK

- About 164 wpm, even and calm, a clinical narrator voice over a violent premise. The contrast (calm voice, clean anatomy, horrible subject) is the tone.
- Two "you" words only, both early; after 0:10 it is all "the bullet" / "it". The viewer is put in the body by the opening conditional and by the anonymous mannequin, not by repeated pronouns. Compare 6mRR91AbxjQ (horsefly bite), which keeps "you/your" throughout.
- Zero numbers. The escalation is carried by hedge words (sometimes / often / especially if) and contrast pivots, not by figures. This is the opposite of the depth-number ladder in fmZfphacPPQ.
- Sentences get longer as the video goes on (19, 26, 31 words) and the last one never stops for 11 s: the rhythm speeds up in feel even though wpm drops slightly.
- One verbatim refrain repeated twice is enough to make a 29 s script feel structured.
- Layer peeling as the visual spine: each body layer is named exactly when it appears. Caption cards sit above the subject so the anatomy in the lower two-thirds stays clear.
- Restraint on gore: the only red is at 75% (glow) and 94% (stain). Holding the one blood image for the last word makes it the stinger.

## 3. Transferable skeleton (no original wording)

Template for a 25-32 s vertical "what happens to your body when [sudden injury or event]" Short: one agent (object, force, animal, substance) travels through one body, with two worse-branch forks and an unresolved ending. At about 160 wpm, 29 s is about 75 words.

1. **Silent title card, 0-4% (0 words, about 1 s).** The premise phrase as a large 3-line caption over the threat object on its own, aimed into the frame. No voice yet. Visual: object enters from one side on a clean pale gradient.
2. **Conditional hook + first mechanism, 4-28% (17-20 words, one sentence).** Say the title phrase as a short second-person conditional (3-4 words), then the agent's first physical action with a "first" sequence word and one technical noun, then a three-item list of body layers ordered outside to inside. Visual: follow the object alone through empty space, then a plain anonymous body with a small entry mark, then peel one layer per list item, each on its own caption.
3. **Fork 1, 28-52% (24-28 words).** A hedge word plus the mild outcome (it passes or ends cleanly), then a contrast pivot plus the worse outcome (it stays and spreads inside). Then a short 3-4 word escalation refrain, then a worst-case condition introduced by an "especially when" style phrase that names the next, harder layer. Visual: hard cut exactly on the pivot word; show the mild branch from behind/outside, the worse branch from inside; swing the camera to the hard layer as it is named.
4. **Fork 2, 52-75% (12-14 words).** Same mild-then-worse pattern on a new variable (size, speed, amount, type): one version stays whole, the other splits or multiplies. Visual: hard cut on the pivot to a wide scale shot (floating organ set or full system), then the split happens on screen with the only bright colour burst so far.
5. **Cascade + bookend stinger, 75-100% (16-20 words, one unbroken clause chain).** The many pieces cause the refrain again, word for word, then damage the deepest vital layer, then a two-word visible consequence. Visual: macro close-up of the vital layer lit up, then a hard cut back to the plain body from step 2 and let the consequence bloom from the entry mark on the final word. End within 0.5 s. No survival verdict, no CTA.

Pacing constants: about 160-165 wpm with a calm, clinical narrator; 3 sentences that each get longer; second person only in the first third; zero numbers; a turn every 2.5-3 s after the opening sentence; two contrast pivots about 9 s apart, each on a hard cut (about 38% and 68%); one 3-4 word refrain used twice (about 47% and 84%); 4 hard cuts total with continuous camera moves or layer peels in between; captions 1-3 words, changing every 0.5-1 s, placed in the top sixth; colour restraint (no red until 75%, the one strong consequence image held for the last word).

For our code-only kit: the anatomy layers map cleanly to stacked SVG groups (outline/skin, muscle, organs, skeleton, vessels) revealed with opacity or clip-path peels on the caption beat; the agent is a small sprite on a motion path (straight for the mild branch, zig-zag inside the ribcage for the worse branch); the split is a particle burst with a radial red glow; vessels are red stroke paths with an animated dash; the bloom is a radial-gradient blob scaling from the entry mark on a white garment shape. Keep the injury agent generic or non-violent in our own topics (venom, cold, pressure, a fall) if the gun framing is a monetisation risk for us.
