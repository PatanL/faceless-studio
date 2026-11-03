# Voice cadence: how RicksClips3000 and Zack D. Films deliver a line, measured word by word

Owner priority (FEEDBACK_LOG, 2026-11-02): our narration needs the RicksClips / Zack D. cadence, especially the
"He did X" hook where the stress lands on the key words. This note measures that delivery and turns it into rules a
TTS can be driven by. **Cadence transfers, identity does not:** their audio is measured for prosody only (where
stress falls, pitch movement, pace, pauses). It is never a voice-clone prompt, reference speaker or training data.
Our voice is designed from a text description (Qwen3-TTS VoiceDesign, section 5).

Numbers: `research/references/data/voice_cadence_refs.json` (aggregates only). Per-word measurements and the
reference audio stay outside the repo in `~/faceless-work/voice-cadence/`.

## 1. Sample and method

- **RicksClips3000, n = 8:** the 8 PARITY Shorts with audio (`ricks720_*.webm`, already on the Mac from the sound
  track), vocals from the existing Demucs `htdemucs_ft` stems. 1,813 words.
- **Zack D. Films, n = 9:** the narrated Shorts from `research/corpus/zackd` whose audio was already on the Spark
  (copied, nothing downloaded), separated the same way. 0BZ1C83I2R4 is left out: it has no narrator, only one shouted
  line. 905 words.
- **Words and times:** transcript from faster-whisper `medium.en`, times from torchaudio's MMS_FA CTC forced aligner,
  and each boundary re-cut at the real silence (frames 25 dB under the speech median). Whisper's own word times were
  unusable for pauses: it widens every punctuation gap to 0.12–0.36 s where the signal has 0.01–0.10 s.
- **Per word** (`research/music/tools/voice_cadence.py`): f0 peak (pYIN, 90th percentile inside the word) in semitones
  relative to the speaker's median; local pitch prominence (peak minus the mean of the neighbours' peaks); peak
  loudness re the median word; per-syllable duration re the speaker's median (lengthening); POS class (spaCy). A word
  is **stressed** when the sum of its pitch, loudness and length z-scores (divided by √2) is ≥ 1.0.
- **Cross-check with RICKS_SOUND.md:** the same RicksClips files give f0 196 Hz, p5–p95 17.2 st, 1 s-median movement
  8.9 st, 3.75 words/s and 0.97 gaps ≥ 120 ms per minute. The sound track measured 194 Hz, 16.3 st, 8.8 st, 3.8 w/s and
  1.0 per minute, so the two pipelines agree.

## 2. The delivery, in numbers (median, IQR in brackets)

| | RicksClips (n = 8) | Zack D. (n = 9) |
|---|---|---|
| f0 median | 196 Hz (184–203) | 159 Hz (148–175) |
| f0 range p5–p95 | 17.2 st (16.4–17.4) | 18.4 st (18.1–18.8) |
| Phrase-level movement (1 s medians, p10–p90) | 8.9 st (7.9–10.0) | 11.0 st (10.3–11.4) |
| Pitch range inside a phrase (peak to low) | 13.9 st | 16.5 st |
| Words stressed | 25 % (about one word in four) | 26 % |
| Stressed vs unstressed words: pitch | **+5.2 st** (4.9–5.4) | **+7.1 st** (6.2–7.3) |
| Stressed words' local jump over their neighbours | **4.5 st** (4.4–4.9) | 5.5 st (4.5–6.2) |
| Stressed vs unstressed: loudness | +1.7 dB | +1.9 dB |
| Stressed vs unstressed: length per syllable | **×1.78** (1.72–1.87) | ×1.73 |
| Sentence onset (first two words) | +1.8 st over the median | +3.2 st |
| Sentence end (last word) | −5.6 st (a fall of ~7 st) | −4.9 st |
| Where the sentence's pitch peak falls | at 20 % of the sentence | at 36 % |
| Pace | **3.75 words/s**, 4.9 syllables/s articulated | 2.8 words/s, 4.0 syll/s |
| Pauses ≥ 120 ms | **1.0 per minute** | 13.5 per minute |
| Pause at a full stop | 79 % have one, **median 70 ms** | 94 %, median 170 ms |
| Pause at a comma | 55 %, median 55 ms | 65 %, median 145 ms |
| Pause inside a phrase | 4 % | 5 % |
| Hook sentence | 3.3 s | 6.2 s |

Loudness does little work (under 2 dB). **Stress is pitch plus length:** a stressed word sits about 5 st over the
unstressed ones and lasts about 1.8 times as long per syllable. Zack D. is the same shape, slower and wider.

### Which words carry the stress (share of each class that is stressed; RicksClips / Zack D.)

| Class | RicksClips | Zack D. | How it is stressed |
|---|---|---|---|
| Names | 83 % | 100 % (n = 4) | pitch (+2.5 st), not length |
| Nouns (subjects, the strange thing) | 59 % | 33 % | pitch (+2.1 st) and a little length |
| Numbers | 50 % (33–71) | 100 % (n = 3) | pitch +2.3 st, length ×1.2 |
| Objects of the verb | 45 % | 46 % | **length** (×1.24 / ×1.36); pitch near the median because objects end phrases |
| Adjectives and adverbs | 35 % | 33 % | pitch |
| Main verbs | 30 % | 43 % | pitch; the hook's act verb gets the sentence's peak |
| Contrast and negation words (but, only, never, nobody, not/n't, even, every, whole) | 24 % | 16 % | **a pitch reset** (+2.6 st) without length: they restart the melody high |
| Function words | 7 % | 3 % | low (−2.4 st) and short (×0.6) |
| Subject pronouns (he, they) | 0 % | 0 % | short (×0.6) but often at the high sentence onset |

### The "He did X" hook

Five of the eight RicksClips hooks open with a subject and a past-tense act ("He [verb]…" or "They [verb]…"). In four of those five **the act verb is the highest-pitched word of the whole
sentence**, and in the fifth it is within 0.1 st of the peak. It sits +6.8 to +9.0 st over the speaker's median
(median of all 8 hooks' first verb: +7.1 st), right after a short, low "He". The verb is raised more than lengthened
(×0.6–1.6). Then the melody steps down through the strange object, which is lengthened (×1.5–1.75). The hook's last
word is long (×1.4 median, up to ×2.3). Examples, paraphrased:

- The railroad hook (a man cuts gaps into the track at fixed spacing): the act verb +7.5 st ×1.6, then "gaps" ×1.6,
  the spacing number +5.6 st, and the last word ×1.6.
- The coffin-bell hook (a burial with a bell attached): the burial verb +9.0 st ×1.3, then "bell" +5.9 st.
- The horse-race hook (a man stakes everything on the worst horse): the betting verb +6.8 st, "life" +4.6 ×1.5, the
  superlative +6.9 st (the sentence peak), and the last word ×1.75.
- The Jar hook: the act verb +7.5 st (the sentence peak), the object's adjective +5.4 st ×1.75, then a drop to
  −10 st just before the one-word punch, which is long and low (×2.1).
- Contrast: HASN'T +7.4 st, NOBODY'S +6.9 to +7.7 st (and short, ×0.55–0.67): a pitch reset, not a stretch.
- "So + adjective": SO carries the jump (+5.9 to +7.1 st); the adjective is lengthened (*tall* ×1.8, *deep* ×1.3).
- The turn: in *You see,* the word SEE is raised (+3.6 to +6.9 st), lengthened a little (×0.9–1.4), and followed by
  only a micro-pause.

Zack D.'s hooks open with the subject noun or an imperative (*Imagine…*, *If you…*), so the peak sits on the first
content word, not always a verb (2 of 9 on the verb). The rest of the pattern is the same: high start, a stressed word
every three or four words, a long last word (×1.5).

### Pace

- RicksClips' pace is flat across the Short (the hook, middle and end all within 3 % of the median sentence rate).
  "Slower on the reveal" is real but is carried by **sentence length**:
  - sentences of 1–5 words (the punch lines, e.g. a two-word death reveal) run at **0.76×** the median rate;
  - 6–9 words at 0.92×;
  - 10–15 words at 1.01×;
  - 16+ words (the escalation, long run-on chains) at **1.05×**.
- Inside a sentence, the stressed words take the time (×1.8) and the function words give it back (×0.6). The overall
  rate stays at 3.75 words/s.
- Zack D. reads slower overall (2.8 w/s) with the same short-line slowdown (0.86×, n = 2) and an even rate otherwise.

### Pauses

- RicksClips has almost no pauses: 70 ms at a full stop, 55 ms at a comma when there is one at all, and almost never
  a pause before the twist word. Of the 64 pauses ≥ 80 ms, 52 % come before a function word (a new clause) and 16 %
  before a contrast word ("But…"). There are 0 breaths.
- The emphasis comes from the pitch jump and the lengthening, not from a dramatic pause.
- Zack D. leaves ~170 ms at full stops and ~145 ms at commas, which is still short.

## 3. The rules for our narration

1. **Register and range:** a voice whose own median sits around 160–200 Hz, with a p5–p95 range of about 17 st and
   1 s-median movement of 8–11 st (Kokoro am_michael: 108 Hz, 9.6 st, 5.4 st).
2. **One stress every three to four words (25 %)**, each about **+5 st over the unstressed words** (a 4.5 st jump
   over its neighbours) and **×1.8 longer per syllable**. Loudness can stay within 2 dB.
3. **What to stress, in priority order:**
   - the hook's act verb (the sentence's pitch peak, about +7 st);
   - numbers;
   - the strange object (lengthened);
   - contrast and negation words (a pitch reset, not lengthened);
   - "so"/"too" + adjective, and superlatives;
   - names;
   - SEE in "You see";
   - the last content word of a short punch line, and the hook's last word (lengthened ×1.5–2).
   Never stress function words or a subject pronoun.
4. **Melody:** each sentence starts about 2 st over the median, peaks in its first fifth, and falls about 7 st to its
   last word. Contrast words restart it high.
5. **Pace by sentence length:** 3.75 words/s overall. Punch lines of 5 words or fewer at about 0.75×, long chains
   at about 1.05×.
6. **Pauses:** at most ~70 ms at full stops and ~55 ms at commas; none inside phrases; no pause before the twist (the
   pitch jump does that job). At most about one gap ≥ 120 ms per minute.

`pipeline/audio/emphasis.py` applies rule 3 from the text alone (no POS tagger, so it runs anywhere). Words can be
forced or vetoed in a script's front matter. Rules 1, 2, 4 and 5 come from casting and the TTS. Rule 6 comes from the
TTS plus `voicefx.tighten` (pauses cut to 0.10 s, as in the `story_ricks` profile).

## 4. The gap test: is it the voice or the delivery?

`out/rnd-voice/gap_test.m4a`, with its order and numbers in `gap_test.txt`. It plays the Jar's first three lines:
RicksClips' original, then for each of our voices the plain render, the same render with RicksClips' prosody
transplanted onto it, and our best native take.

The transplant (`research/music/tools/prosody_transplant.py`, Praat PSOLA through parselmouth) works on our audio
with their numbers only:
- each word's duration and each pause (a time warp at the word boundaries);
- the f0 contour in semitones relative to their median, re-centred on our voice's median so our register stays ours;
- each word's loudness relative to the median.

No reference audio is mixed in or used as a prompt. The match score comes from `voice_compare.py`: a 0–100 blend of
stress-pattern r, pitch-contour r, length r, stressed-word overlap, the jump size on their stressed words, f0 range
and movement, pace and pauses.

| Clip | Match | Stress r | Pitch r | Stressed-word overlap | Jump on their stressed words (theirs 3.9 st) | Range ratio | Movement ratio | Pace (theirs 3.48 w/s) | Pauses ≥ 80 ms (theirs 2, 0.19 s) |
|---|---|---|---|---|---|---|---|---|---|
| Kokoro am_michael, plain | 67 | 0.84 | 0.85 | 0.71 | 2.4 st | 0.60 | 0.61 | 3.74 | 5, 1.32 s |
| Kokoro + transplant | 89 | 0.85 | 0.88 | 0.88 | 3.5 st | 1.01 | 0.88 | 3.50 | 3, 0.30 s |
| Kokoro best native (pauses tightened) | 74 | 0.85 | 0.85 | 0.71 | 2.7 st | 0.59 | 0.83 | 4.01 | 3, 0.35 s |
| Qwen3 "nova", plain | 71 | 0.83 | 0.80 | 0.88 | 2.6 st | 0.87 | 0.64 | 3.15 | 6, 1.66 s |
| nova + transplant | **94** | 0.94 | 0.95 | 0.88 | 3.6 st | 1.05 | 0.82 | 3.48 | 2, 0.19 s |
| nova best native (emphasis, tightened; best of 3 takes) | 82 | 0.81 | 0.74 | 0.88 | 3.5 st | 1.00 | 0.67 | 3.34 | 4, 0.35 s |

What it shows:
- **Kokoro already stresses the right words.** Its stress and pitch patterns correlate 0.84–0.85 with RicksClips'
  read. What it lacks is size: about 60 % of their pitch range and phrase movement, a 2.4 st jump against 3.9 st,
  1.3 s of pauses against 0.19 s, and a register of ~107 Hz against their 168 Hz on these lines. With the transplant
  the numbers reach their level (89), but the register stays at 107 Hz, so it is still a low, documentary voice.
- **The gap is prosody plus register.** On a voice in the right register (nova, ~185 Hz), the transplanted delivery
  measures 94. Whether it *sounds* RicksClips-level is the owner's listen. If it does, the voice itself is not the
  limit.
- **Native, Qwen3 gets most of the way.** Rule-marked emphasis brings the jump to 3.5 st and the range to 1.0×. The
  phrase-level movement (0.67×) and stray pauses are still short of theirs, so those are the remaining targets.
- A rule-driven boost (`research/music/tools/prosody_boost.py`) widens our own melody to the measured 17 st and adds
  a bump on the marked words. It lifted plain nova from 71 to 80 but the emphasised take only from 81.8 to 82.1,
  within take-to-take noise, so it is not in the pipeline.
- **Drama 3 could not be tested.** The Spark was unreachable during this test. Its official inference code
  (`resolve_drama3_devices`) also accepts only CUDA devices. On CPU its FP8 experts would be dequantized to bf16,
  about 70 GB for 35B parameters, against the ~49 GB the Spark had free. For speed, the owner's Nov 1 CPU test of the
  smaller S2-Pro took 6 min for 4.3 s of audio. Running Drama 3 on the GPU is the owner's call.

## 5. Our voices: Qwen3-TTS, designed and then reused

**Install** (Mac only; the Spark's GPU was never used):
- The official code (github.com/QwenLM/Qwen3-TTS @022e286) was read before running. Model loading only pulls the
  named repo and its `speech_tokenizer/`. Reference-audio URLs are fetched only on the clone path, which we feed with
  local files. The one `eval` is a constant string.
- Installed from that clone into `~/faceless-work/venvs/qwen3tts` (Python 3.13, torch 2.15, transformers 4.57.3).
- Weights come from the official Qwen HF repos, pinned to their revisions: 1.7B-VoiceDesign and 1.7B-Base, 4.5 GB
  each, in `~/faceless-work/models`.
- It runs bf16 on MPS at 1.8–2.4× real time (M1 Pro). Peak memory is 5.8 GB, and disk stayed above 20 GB free.

**Design, then reuse.** VoiceDesign makes a new voice on every call: one description gave clips from 167 to
335 Hz across seeds and instructions. A long delivery instruction also pulls the voice itself around. So each
voice is designed **once** from its text description, on our own reference text, and three seeds were scored
against the section 3 numbers. The chosen clip is then the voice prompt for the Base model (the official "voice
design then clone" workflow). Within a voice, the register then holds steady across texts and takes: nova stays at
180–200 Hz.

| Voice | Description (abridged) | Designed clip f0 |
|---|---|---|
| nova | energetic, warm young male storyteller, bright clear tenor, a smile in the voice, playful | ~185 Hz |
| spark | upbeat male narrator, light bright voice with a slight rasp, fast and punchy, "telling a friend" | 190 Hz |
| ember | confident, warm male storyteller, resonant mid-range, animated, lands twists with relish | 158 Hz |
| iris | energetic young female storyteller, bright, warm, playful, big rises and falls | 385 Hz |

**Emphasis controls tried** (pilot: nova, the Jar lines, 3 takes each, pauses tightened, match vs RicksClips' read):

| Control | Match (3 takes) | Note |
|---|---|---|
| VoiceDesign, plain | 62–75 | voice drifts between takes (167–208 Hz) |
| VoiceDesign + instruction naming the words to hit | 54–77 | the instruction moves the voice (183–251 Hz) |
| VoiceDesign + stressed words in CAPITALS | 60–69 | |
| Designed voice reused (Base), plain | 74–82 | stable voice |
| **Designed voice reused (Base) + CAPITALS** | **75–81** | stable; the best stressed-word overlap (0.76–0.88) and jump |

The Base model has no instruction input, so on the reused voice the emphasis control is the capitalised text from
`emphasis.py`. The instruction route (`emphasis.instruct_for`) stays for VoiceDesign and for a hosted instruct model.

## 6. The test: 4 voices × plain / emphasis × 3 texts × 2 takes, against Kokoro

The texts are the Myeongnyang hook plus its first ~15 s (62 words, using the operator's "one line" fact fix), the
posted Vasa hook plus ~15 s (62 words), and the Jar's first three lines. Kokoro uses the current settings (am_michael,
speed 1.30, sentence mode). Qwen takes are the reused designed voice, with pauses cut to 0.10 s as `story_ricks`
does. Numbers are the means of 6 clips (Kokoro: 3).

| Condition | f0 | Range (17.2) | Movement (8.9) | Stressed vs rest (5.24) | Jump (4.51) | Lengthening (1.78) | w/s (3.75) | Pauses ≥ 80 ms/min (7.8) | Closeness | Jar match | Blind judge |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ember plain | 147 Hz | 14.7 | **7.0** | 4.83 | 2.96 | 1.62 | 3.60 | 13.3 | 83.9 | 77.2 | **1** |
| nova emphasis | 189 Hz | **15.3** | 6.4 | **5.10** | **3.25** | 1.67 | 3.44 | 13.7 | **85.0** | **78.0** | 2 |
| ember emphasis | 147 Hz | 14.0 | 6.6 | 4.32 | 2.66 | 1.71 | 3.52 | 11.7 | 81.6 | 72.7 | 3 |
| nova plain | 182 Hz | 14.6 | 5.0 | 4.35 | 2.99 | 1.76 | 3.59 | 13.5 | 79.9 | 75.7 | 4 |
| spark plain | 189 Hz | 12.9 | 6.1 | 4.21 | 2.97 | 1.77 | 3.38 | 14.1 | 78.5 | 67.0 | 5 |
| spark emphasis | 182 Hz | 13.1 | 5.0 | 4.34 | 3.04 | 1.67 | 3.37 | 12.5 | 78.0 | 68.4 | 6 |
| **Kokoro am_michael (current)** | 113 Hz | 10.0 | 5.1 | 4.45 | 3.23 | 1.77 | 3.80 | 26.6 | 72.1 | 67.4 | 7 |
| iris plain | 355 Hz | 12.1 | 4.9 | 2.77 | 2.18 | 1.64 | 3.57 | 6.4 | 71.3 | 66.3 | 8 |
| iris emphasis | 369 Hz | 13.0 | 3.9 | 2.61 | 2.25 | 1.67 | 3.56 | 2.9 | 71.0 | 63.8 | 9 |

- **Closeness** is a 0–100 score for nearness to the RicksClips medians, across the eight delivery numbers in the
  table.
- **Jar match** is the word-by-word `voice_compare.py` score against RicksClips' own read of the same lines (mean of
  2 takes).
- **The blind judge** was a fresh agent. It ranked anonymised ids from the measurements, the measured stressed words
  and the ASR transcripts; it cannot hear. Its reasons:
  - **#1 ember plain:** the best phrase movement and consistent takes.
  - **#2 nova emphasis:** the biggest pitch numbers and the best Jar match, but it was marked down for ASR errors and
    for stressed function words.
  - **Kokoro, 7th:** the narrowest range and three times the reference pauses.
  - **iris, last:** an implausibly high median, possibly pYIN octave errors, and weak contrast.
- **Confidence.** The judge put the top three (ember plain, nova emphasis, ember emphasis) as "moderately
  confident". Takes of the same condition swing 1–2 st in jump, so differences under ~0.5 st are noise.

**Emphasis in capitals works, but it costs clarity.** On the Myeongnyang hook, capitals raised the marked words
+3.4 to +3.9 st over the rest (plain: +1.0 to +1.6). But in every emphasised condition the model at times spelled or
bent a capitalised word:
- WROTE as letters;
- LAUGHING heard as "lacking" in 6 of 8 emphasised Jar takes (0 of 8 plain);
- JAPAN'S, YI and VASA bent.

Plain takes had none of these errors. On a 2-take check, skipping capitals on names and short words didn't fix it, and `*asterisks*`
doubled syllables.

**Verdict.**
- Every Qwen male voice beats Kokoro on closeness, range and pauses; Kokoro ranks 7th of 9.
- **ember plain** is the safest winner (judge #1, clean ASR, closest phrase movement at 7.0 st).
- **nova with emphasis** is the closest to RicksClips on the numbers, but it needs a bend-free emphasis control
  first.
- No condition yet reaches the reference phrase movement (8.9 st) or the jump (4.5 st). The gap test (section 4)
  shows that this missing melody, not the voice, is what remains.

## 7. Backend and next steps

`tts: qwen3` is wired as an opt-in engine (pipeline/audio/README.md, "Qwen3-TTS backend"):
- default voice `ember`, `emphasis: off`;
- the same word timings as Kokoro (forced alignment, coverage 1.0 in the end-to-end test);
- one worker call per script, on MPS.

Kokoro stays the default until the owner has listened to `out/rnd-voice/voice_AB.m4a` (order in `voice_AB.txt`).
`tts: qwen_api` is the slot for the hosted Qwen model, documented but off until there is a key.

Next, in order of measured payoff:
1. **A bend-free emphasis control.** Candidates:
   - capitals only on words the ASR check passes (render, run whisper, re-render the bent chunk with that word
     plain);
   - a per-word prosody edit after synthesis on the marked words (`prosody_boost.py`; the gap test shows PSOLA edits
     at RicksClips' size sound intact on our voice).
2. **Pauses.** Set `tighten_gaps.max_gap` to 0.07 s for qwen3, matching the refs' 70 ms at full stops. At 0.10 s we
   measure 12–14 gaps ≥ 80 ms per minute against their 7.8.
3. **Phrase movement 7 → 9 st.** Try designing ember again with "big rises and falls" in the description and
   scoring 3 seeds again.
4. **Drama 3**, if the owner puts it on the GPU, and **qwen_api**, if a key is added: both join this same A/B and
   the same measurements.


## 8. The rule-based melody shaper (`melody: rules`) and Ming-3.0-tts

**The shaper** (`pipeline/audio/melody.py`) is the gap-test transplant, but with no reference. It marks stress with
the section 3 rules (`emphasis.mark`, 35 % density) and builds a target melody:
- a declining line through each sentence;
- stressed words +5 st over it, the hook's act verb +7, and contrast words +2.6 as a reset;
- the last word falling to −5.6.

It blends that target 40/60 with the TTS's own word-level melody (that melody already correlates ~0.75 with real
reads), keeps the TTS's micro-melody, and scales the result to the measured 17.2 st range. Timing changes too:
stressed words ×1.25, function words ×0.85, punch lines of 5 words or fewer ×1.25, pauses of 90 ms at full stops and
60 ms at commas, and pace pulled toward 3.75 w/s. PSOLA applies all of it to our own take.

Three passes, one each, no judge:
1. Pass 1 used the rules-only contour. It **flattened** the read (range ~10 st, Jar match 57–64).
2. Pass 2 added the blend and range scaling.
3. Pass 3 changed density and timing. Its numbers, the means over 3 texts × 2 takes, are below.

| Voice | Closeness, plain → shaped | Jar match, plain → shaped (per take) | Range | Movement | Stressed vs rest | w/s | New misreads | Spectral change (MCD-DTW) |
|---|---|---|---|---|---|---|---|---|
| ember | 83.9 → **90.8** | 73.6 / 80.8 → 74.0 / 75.7 | 17.5 | 8.2 | 6.1 | 3.75 | 0 | 30 |
| nova | 79.9 → 86.4 | 79.0 / 72.3 → 76.9 / 71.1 | 16.4 | 6.0 | 5.6 | 3.75 | 0 | 35 |
| Kokoro | 72.1 → 89.1 | 67.4 → **84.3** | 16.2 | 9.0 | 7.5 | 3.76 | 1 (sea/see) | 28 |

- **Spectral change, for scale:** the gap-test transplant, which kept the words intact, measures 31–45. Two takes of
  the same text measure 51. So the shaper's 26–39 is a smaller spectral change than either.
- **The shaper reaches the RicksClips numbers.** On range, movement, stress size, pace and pauses it takes ember to
  90.8 closeness, the highest of any condition, with no misread words.
- **It does not reach the 88 Jar-match target.** Ember and nova land at 71–77, about where their plain takes were,
  because the rules put stress on different words than RicksClips chose for these exact lines (stressed-word overlap
  0.65–0.77). Kokoro gains the most (67 → 84) because its own placement already matched theirs (r 0.85), but its
  register stays at 113 Hz.
- **What 88 needs is the word choice, not the size.** The transplant scored 94 by copying their exact word choices.
- **One intelligibility risk:** in the end-to-end test, the shaped ember take had "one line" heard as "online".

**Ming-3.0-tts-0.5b** (inclusionAI; official repo @a39b806, HF weights rev 7247f4c, own venv, CPU bf16):
- **Setup.** Its MPS path fails on mixed bf16/f32 operations written for CUDA autocast, so it runs on CPU under bf16
  autocast at about 5–6× real time. The voice is our own, designed once (VOICE_DESIGN, from a text description of a
  young male storyteller) and reused from that clip.

| Ming condition | Jar match | Closeness | f0 | Range | Movement | Misreads |
|---|---|---|---|---|---|---|
| plain (designed voice reused) | 59.4 | 74.3 / 74.5 | ~253 Hz | 13.3 / 10.8 | 3.3 / 3.0 | 0 |
| emotion `惊讶` (surprised) | 58.6 | 73.0 / 68.2 | 381–403 Hz | 12.4 / 9.9 | 6.2 / 4.4 | 0 |
| freeform instruction naming the words to hit | 37.8 | 63.5 / 75.4 | 236 / 156 Hz | — | — | dropped 2 of 3 Jar sentences; the voice changed |
| plain + shaper | 69.6 | 70.6 / 77.7 | ~250 Hz | 10.6 / 12.9 | 2.5 / 3.6 | 0 |

(Where two values are given, they are Jar / Myeongnyang.)

- **Ming does not beat ember or nova natively.** Its closeness of 73–75 compares with 80–85, and its Jar match of 59
  with 76–78. Its melody is the flattest of the candidates (3 st movement). The emotion control mostly raises the
  register, and the freeform control is unreliable on long text.

**Wiring.** `melody: rules` (front matter, or `--melody rules`) runs after any engine (`tts: qwen3` and Kokoro):
- it is **off by default**;
- it runs in the qwen3 venv, which has parselmouth;
- word times and SFX cues are remapped; caption starts land within 14 ms (median) of a fresh forced alignment.

Listen: `out/rnd-voice/melody_AB.m4a` (order in `melody_AB.txt`).
