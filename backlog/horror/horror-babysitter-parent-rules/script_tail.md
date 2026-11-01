

## Kit needs (for the builder)

Nothing below blocks the storyboard: every item already has an inline-SVG or core-layer stand-in in `gen_storyboard.py` that validates and renders (stills checked). These are upgrades for after the horror lock lifts.

- **Handwriting fonts.** Only Montserrat and Anton are bundled (`studio/src/core/fonts.ts`). The two hands on the note are now Montserrat 800 upright navy/red (marker) against Montserrat 500 italic, skewed, grey (pencil), which reads as two writers in the stills. Better: bundle two OFL fonts on the Spark into `studio/public/fonts` (Caveat for Mrs. Doyle's marker, Patrick Hand or Gochi Hand for the pencil) with a targeted `fonts.ts` edit, then swap the `font-family` in `fridge_note()`.
- **`horror/FridgeNote` component** (when the kit unlocks): promote `fridge_note()`, `highlight()` and `pencil_rings()` into a kit card with `rules [{num, hand, text}]`, per-rule highlight cues and a `variant` card/child.
- **`horror/Child` puppet**: promote `monitor_room()` + the mouth layers into a component with `pose` wall/profile and `talk` windows.
- **SFX**: synthesize `landline_ring` and `chain_slide` (recipes in `storyboard.json` `_sfx_new`).
- **Multi-voice mix**: `mix.wav` is not built. Same recipe as the siblings: Kokoro line wavs written by `tts_measure.py ... <wav_dir>` (already on the Spark at `~/studio/tmp/babysitter_wavs`), the `lines.FX` filters with ffmpeg on the Spark (`highpass/lowpass`, `rubberband` or `asetrate` for ±st, `adelay`+`amix` for the 45 ms slap), placed at the `timing.json` starts, SFX from `_sfx_cues`, dread bed with the hush windows.

## Pacing check (measured)

- **Runtime 100.5 s**: 317 words, 230 wpm while speaking (Kokoro on the Spark CPU), 189 wpm overall with 6.5 s of timed silence. At the edge of the 50-100 s Shorts band, down from 117 s planned in the previous draft (which was really ~123 s at the measured rate).
- **Hook**: line 1 is 7 words (babysitting + 34th floor). Rule five by 2.4 s, the call at 5.3 s, "What password" at **6.4 s**. 34 words spoken in the first 10 s (PLAYBOOK median 43.5).
- **Jolts**: 44 scenes in 100.5 s (median ~2.3 s per shot). Every scene changes something the viewer can name (a readout, a rule, a count, a bubble). The longest still stretch is the peak: the arm settles at 76.7 s and the frame holds to 80.0 s, 3.0 s of it silent (`check_storyboards.py` max hold 4.3 s).
- **Shape**: hook 0-6%; plant 8%; compliance 12-20%; proof 20-27%; rules lull 27-39% (cards every ~3 s, MOM-NOTE style); proximity 39-45%; **turn 45-52%** (the password at the door, rule five now admits the visitor); near-miss 53%; lifeline under the count 55-69%; **peak image 71-80%**; temptation 80-84%; **twist 84-90%**; voice swap 98%; end card 98.9-100.5.
- **Rules**: 5 stated; rule 3 broken by the knock; rule 5 inverted at the door; rule 4 obeyed as an action; two contradictions planted (rule 5 vs rule 3; rule 4 vs the mother); the twist forges rules 1 and 4.
- **Ladders**: proximity (lobby, elevator 12/20/31/34, door, Theo's bed, the handset in Ivy's hand, Ivy's own voice) and channel removal (house phone → monitor → texts unread → the door goes quiet → the house phone belongs to it). Volume at the door: polite password, count, silence.
- **Numbers**: 7:40, 7:12, 9:40, 34th, 12, 20, 31, 34, rules 1-5, the count 1-5, Extension 2. 30 spoken number words (17.9 per minute; the rule ordinals and the count inflate it; clock times and floors alone are ~5 per minute).
- **Viewer proxy**: "So why buzz?" (the keys tell), "What does rule four mean?" (Ivy asks the viewer's question to the real authority, and it gets answered).
- **Silences**: 0.7 s on the empty hall, 1.25 s of clear air for the knocks, 3.0 s on the peak image, 1.2 s breath on the line before the last word.
- **Sentences**: median 3 words, 71% punch lines; this script is built from fragments read as cards and readouts. Lines that carry the story (n1, n7, n12, n16, n23, n27) are 8-14 words.
- **Non-graphic**: no injury, no gore words; the arm holds the receiver and never touches the child's skin on screen. The cover shows a note, a ringing phone and a text, never the child (mark the upload "not made for kids"; keep Theo off every thumbnail).
- **No spoken subscribe**, no part card. Standalone.
