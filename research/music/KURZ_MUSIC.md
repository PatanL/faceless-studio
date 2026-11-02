# How Kurzgesagt's music serves the story, measured, and what we take for 60–90 s Shorts

Internal research for the explainer channel. We study how the music is used and copy none of it: no melody, recording, sample or stem from the references goes into our videos. All our notes are composed by `pipeline/audio/score.py`.

**Goal (owner's clarification, 2026-11-01).** We want the music that works best for our format, not music that sounds most like Kurzgesagt. Our format is a 60–90 s vertical Short, heard on phone speakers. A calm male narrator talks almost the whole time, the picture changes every 2–4 s, the hook lands in the first 3 s and the ending loops. The look is house style A: flat, bold, saturated, playful and curious. Every rule below is judged by four questions:

- Does the voice stay clear on a phone?
- Does it help the hook and retention?
- Does it follow the setting changes?
- Does it stay fresh when the Short loops?

§6 lists what does not transfer.

## 1. Sources and method

| Key | Video | Analysed | Excluded |
|---|---|---|---|
| **D** | "The Deep Sea" (`PaErPyEnDvk`) | 0:00–10:04 (604 s) | intro jingle 0:26.4–0:36.4; sponsor read after 10:04 |
| **W** | "Why Blue Whales Don't Get Cancer" (`1AElONvi9WQ`) | 0:00–7:06 (426 s) | intro jingle 0:26.4–0:32.9 |
| **A** | our orca Short v3/v4 with the `deep_ocean` bed (84.6 s) | all | none |
| **B** | the same orca Short with the new score (84.6 s) | all | none |

All of this ran on the Spark, CPU only, at `nice 10`.

1. **Separation.** Demucs `htdemucs` 4.0.1, CPU, 8 threads (`tools/separate.py`) split each video into vocals, drums, bass and other. D took 204 s and W took 148 s. "Music" means drums + bass + other.
2. **Narration timing.** faster-whisper `small.en` gives word timestamps from the vocals stem (`tools/words.py`): 1,586 words for D and 1,097 for W. A speech mask comes from the vocals stem (50 ms frames within 30 dB of its 95th percentile, holding through gaps under 0.3 s).
3. **Measurement.** `tools/analyze.py` produced everything below. Setting changes come from the hand-made every-frame catalogue (`research/frame-analysis/data/{D,W}_settings.csv`: 48 changes in D, 45 in W). Every "aligned" claim is tested against a circular-shift null: the music events are shifted together by a random offset 2,000 times, and *p* is the share of shifts that match at least as often as the real timing.
4. **Outputs.**
   - Numbers: `data/{D,W,ORCA_*}_music.json`.
   - Every event with the words around it: `data/*_timeline.csv`.
   - Loudness lanes with setting changes, section boundaries, risers, hits and drop-outs: `data/*_music.png`.

**Caveats.**

- Demucs leaves sound effects in the music stem, because it has no separate SFX stem. "Hits" are therefore low-frequency onsets of 8 dB or more in 200 ms, and they include impacts as well as bass and timpani entries.
- Key estimates are Krumhansl profiles per section (r = 0.3–0.8). Treat them as major or minor colour, not exact keys.
- The setting catalogue is accurate to about ±0.5 s.
- Two videos are a small sample. The numbers agree closely between them, which suggests they reflect a house practice.

## 2. What the reference does, with numbers

### 2.1 Level under the voice: steady, about 10 LU down, and it swells in the pauses

| | D | W | A (our old bed) | B (new score) |
|---|---|---|---|---|
| Voice minus music while the narrator talks (momentary LU), median (p10–p90) | **11.1** (1.9–18.8) | **10.0** (3.1–16.0) | 10.4 (6.9–14.0) | **10.2** (5.6–16.3) |
| Music in pauses of 0.5 s or more vs under speech | **+5.0 dB** (paired +3.5) | **+4.9 dB** (paired +4.4) | no pauses | no pauses |
| Speech share of runtime | 84 % | 88 % | 87 % | 87 % |
| Pauses of 0.5 s or more | 83 (median 0.9 s) | 47 (median 0.7 s) | **0** | **0** |
| Music short-term loudness, p10 → p95 | −28.6 → −16.7 (**11.9 dB**) | −26.1 → −17.2 (**8.9 dB**) | −25.2 → −23.6 (**1.6 dB**) | −27.1 → −20.7 (**6.4 dB**) |
| Integrated: voice / music (LUFS) | −17.5 / −26.1 | −16.3 / −26.0 | −16.7 / −28.6 | −16.3 / −27.2 |

- Kurzgesagt keeps the music about 10–11 LU under the talking voice.
- They let the music come up about 5 dB whenever the narrator pauses. The long-form mix sits at about −16 to −17 LUFS integrated.
- The score's loudness breathes over a range of 9–12 dB.
- Our old bed had the same average gap under the voice as the references, but it was flat: a 1.6 dB range against their 9–12 dB.

### 2.2 Sections, texture and setting changes

| | D | W |
|---|---|---|
| Setting changes / min | 4.8 | 6.3 |
| Music section boundaries / min (novelty, ~6 s kernel) | 3.9 (median section 16 s) | 3.3 (median 15.5 s) |
| Setting changes with a section boundary within ±1.5 s | 21 % (chance 20 %, *p* 0.50) | 18 % (chance 16 %, *p* 0.44) |
| Texture change across a setting change (feature distance) vs random moments | 0.40 vs 0.35 | 0.50 vs 0.32 |
| Level step across a setting change, median | 3.0 dB | 1.8 dB |
| **Low hit within ±0.6 s of a setting change** | **33 %** (chance 19 %, *p* 0.019), median −0.1 s | **36 %** (chance 16 %, *p* 0.0005), median −0.3 s |
| Setting changes within ±0.5 s of a sentence start | 40 % (chance 16 %) | 53 % (chance 19 %) |

- A music cue does not restart at every new picture. Cues last about 15 s and span 1–3 settings.
- What follows the picture is the **texture** (an instrument enters or drops out, the level steps 2–3 dB) and, about a third of the time, a **low hit** placed 0.1–0.3 s before the new image settles.
- Setting changes themselves sit on sentence starts, so the music, the picture and the sentence turn together.

### 2.3 Tempo, pulse and instrumentation (spectrum-based)

| | D | W |
|---|---|---|
| Tempo | **117.5 BPM** (windows 112–123) | **123 BPM** (windows 89–123) |
| Pulse clarity (onset autocorrelation), median; share of 15 s windows with a clear pulse | 0.20; 19 % | 0.27; 42 % |
| Harmonic share of the music (HPSS), median | 0.93 | 0.93 |
| Runtime where the drums stem is within 10 dB of the music | **12 %** | **10 %** |
| Runtime with a bass instrument (bass stem within 10 dB) | 32 % | 40 % |
| High-register note spacing, median | 0.41 s (8ths in places: 0.255 s at 2:05–2:14) | 0.48 s |
| Spectral centroid, median | 903 Hz | 1,088 Hz |
| A-weighted 0.8–2.5 kHz / 2.5–6 kHz relative to total | −4.7 / −17.8 dB | −7.1 / −13.7 dB |
| C6 "bell" octave relative to the loudest octave | −31 dB | −33 dB |
| Sections in minor | 69 % | 59 % |

- **Instrumentation.** The music is almost entirely pitched: pads, strings and keys. The pulse comes from arpeggios at about 8th-note spacing, not from drums. Percussion sits in about a tenth of the runtime: the intros (D 0:00–0:36, W 0:00–0:33) and a few driving passages (W 4:16–4:25).
- **Sub and bass.** The C1–C2 octaves hold the most energy in almost every section. A bass instrument plays in about a third of the runtime, in blocks of 30–90 s.
- **Mode follows the light of the place.** D's surface sections (0:00–2:05: coral reef, shelf) read major (E, A, D). From the twilight zone on (2:13) they read minor (A, B, D, F♯, C♯ minor) for the rest of the descent. W opens minor on "cancer is a creepy and mysterious thing", explains in major (B♭ and B major, 0:40–1:53), and turns minor for the threat sections.
- **Our old bed.** It sat almost entirely below 400 Hz (centroid 335 Hz; 2.5–6 kHz at −37 dB relative to total), so a phone speaker plays almost none of it (§4).

### 2.4 Risers, hits, drop-outs

| | D | W |
|---|---|---|
| Risers (rise of 6 dB or more over at least 1.5 s, monotonic) / min | 2.7 | 2.8 |
| Riser length, median; rise, median | 2.2 s; 12 dB | 2.8 s; 10 dB |
| **Riser peaks within 0.5 s of a sentence start** | **52 %** (chance 16 %, *p* < 0.001) | **50 %** (chance 19 %, *p* 0.0015) |
| Riser peaks within 1 s of a setting change | 21 % (chance 9 %, *p* 0.004) | 16 % (chance 9 %, *p* 0.10) |
| Low hits / min | 9.9 | 8.3 |
| Hits within −0.4…+0.3 s of a sentence start | 17 % (chance 11 %, *p* 0.03) | 10 % (chance 13 %) |
| **Drop-outs** (music falls 12 dB or more below its 10 s median for at least 0.3 s) / min | **1.6** | **1.6** |
| Drop-out length; depth (medians) | 0.4 s; 13.6 dB | 0.5 s; 14.4 dB |
| Drop-outs during speech (not in a pause) | 100 % | ~95 % |
| Drop-outs followed by a hit within 1.5 s | 10 of 16 | 6 of 11 |

Examples (video time, words before | after):

- **W 1:03.0–1:04.3**: drop-out (15 dB) under "…and yet they function **perfectly.** | Until they don't." The music then rebuilds with a +28 dB riser from 1:03.7 to 1:07.8. This is the clearest drop-before-the-punchline device.
- **D 0:49.7–0:50.4**: drop-out under "close to the surface | in the first 200 metres". It is followed by a +27 dB riser (0:50.0 → 0:53.2) into "This is where we begin our journey" and a setting change at 0:52.9.
- **D 8:33.4–8:35.5**: two drop-outs under "The deepest point. The Challenger Deep. | 11,000 metres", followed by a +24 dB riser that peaks at 8:36.5.
- **D 0:08.1–0:11.4**: four short stop-time drop-outs under "conquered the Arctic, and penetrated the deepest jungles". They are stabs that land on the triptych's setting changes at 7.4, 9.9 and 12.9 s.
- **W 5:56.4**: drop-out, then a hit on "Cancer is killing cancer. | This process can repeat…"

- Risers build toward the **start of a sentence**, not toward a picture change.
- Drop-outs come **under the last words of a set-up line**, 0.3–1.3 s before the line that turns, and the music comes back with a hit or riser. They are not silences between sentences.

### 2.5 How the music starts and ends

- **W.** The hook line is spoken over near-silence: the music sits at −58 to −47 LUFS for the first 3 s. The music then enters with a +40 dB swell (0.1 → 3.8 s) and lands with a low hit at 3.35 s, right after "…creepy and mysterious thing."
- **D.** The music starts quietly at 0.35 s (−38 LUFS) and swells +28 dB from 2.2 to 4.9 s. It lands a hit on the punch word "boring." at 3.75 s, at the first setting change (3.9 s).
- In both, the full texture **arrives on the hook's punch, 3–4 s in**.
- **Endings.** D's loudest music of the whole video is the ascent montage (short-term −12.8 LUFS around 9:34–9:40, about 12 dB above its typical level). It then resolves to −25 and fades to −50 over about 4 s. W swells on "Cancer has always been a challenge" (+16.5 dB riser, 6:54–6:56) and then settles about 8 dB lower by the end. Both build the biggest moment shortly before the end, then resolve.

### 2.6 Sound design and music

- Noise-like whoosh transients are rare: 0.6/min in D and 3.1/min in W. They line up only weakly with the visual transitions (*p* 0.07–0.09).
- Most transitions are carried musically, by the low hits of §2.2 (33–36 % of setting changes).
- Kurzgesagt's sound effects are mostly tonal, small and close to the mix level. Demucs cannot pull them apart from the score, which itself shows how well they blend.
- Our v3 orca is the opposite. It places **81 SFX cues in 84.6 s (57/min)**, including a whoosh or bubbles on every cut.

## 3. Rules (implemented in `pipeline/audio/score.py` unless marked)

| # | Rule | Reference evidence | Implementation |
|---|---|---|---|
| R1 | Voice about 10–11 LU over the music while talking. Duck about 3.5 dB, plus a further −6 dB of the music's 1–4 kHz while the voice talks, so the consonants stay clear. | §2.1: 10.0 / 11.1 LU | `config.NICHES.explainer.score_mix`: `music_db −7`, `duck_db −3.5`, `duck_band` −6 dB at 1–4 kHz (dynamic EQ in `mix.py`). Measured on B: 10.2 LU median. |
| R2 | The music breathes: about 6–9 dB of short-term range from cue intensity, risers and drop-outs, never a flat bed. | §2.1: 9–12 dB | Intensity 0–3 per cue (−3.5 / −1.5 / 0 / +1.5 dB plus layers). B: 6.4 dB. |
| R3 | One cue per mood, about 4–16 s. Runs over 18 s split into roughly 12 s sections at sentence starts. A cue spans 1–3 settings. | §2.2: sections every 15–16 s | `plan()` steps 2 and 2b |
| R4 | Every setting change changes texture: a new cue, or a new layer and a bell inside the cue. About a third of the changes, the cue starts, get a low hit 0–30 ms before the picture. | §2.2: texture 0.40–0.50 vs 0.32–0.35; hits 33–36 % | `arrange()`: internal-setting colour, `booms` and timpani at cue starts |
| R5 | The music turns on the word. A strong reveal (pivot, answer or marker) up to 1.2 s before a setting change moves the cue boundary to that word. | §2.2: changes on sentence starts 40–53 %; §2.4: risers peak on sentence starts 50–52 % | `plan()` step 3 |
| R6 | Mood follows the place and its light (major for day and surface, minor for dark, deep and hunts), plus the words: hunt words make it tense, mother or calf words make it warm, a question on a board makes it suspended. | §2.3: D major until 2:05, minor after the twilight zone | `mood_of()` with `MOODS` (curious, board, tense, cold, warm, question, deep) |
| R7 | The pulse comes from arpeggios and ostinati around 108 BPM. Drums only in the most intense cues (about 10 % of runtime). | §2.3: 117–123 BPM, drums within 10 dB in 10–12 % | Arp 8ths at intensity ≥ 1, pulse at ≥ 2, timpani and taiko only at tense ≥ 2/3 |
| R8 | Risers (reverse cymbal, pad swell, arps at double time) into cues whose intensity rises, ½–1 bar long. | §2.4: 2.7–2.8/min, 2.2–2.8 s | `plan()` step 7. B: 6 risers in 84.6 s (4.3/min) |
| R9 | Stings: a low hit (timpani, low-strings stab, sub boom) plus one bell, placed 30 ms before the reveal word. Strong reveals at least 4 s apart, punch lines at least 8 s apart. | §2.4: 8–10 low hits/min; drop-out then hit 55–63 % | `find_reveals()`, `plan()` step 6 |
| R10 | Drop-outs: 0.6 s, at least 20 dB, under the end of the set-up line before the strongest reveals. At least 14 s apart, never in the hook. | §2.4: 1.6/min, 0.4–0.5 s, 13–14 dB, under speech | `plan()` step 6. B: 3 drop-outs, 22–29 dB |
| R11 | The hook plays sparse (pad, sub, motif) about 9 dB under the later cues. A riser lands the full texture with a hit on the first setting change (≈ 3 s). | §2.5: W lands at 3.2–3.4 s, D at 3.75 s | Hook role, intensity 0, a 1-bar riser |
| R12 | Loop ending: the last cue returns to the hook's mood, texture and harmony and ends on the chord that leads into bar 1. The rendered tail is wrapped onto the start, with no fade at the seam. | (does not transfer, see §6; our replacement) | `role="bookend"` plus tail wrap. `mix.py` uses a 10 ms anti-click only. |
| R13 | Phone-first spectrum: a sub with 2nd and 3rd harmonics, bass and pads in 150 Hz–1 kHz, sparkle above 4 kHz, a pocket at 2.5–3 kHz. | §2.3 and §4: the old bed vanished on phones | Per-stem EQ and bus EQ in `fx_chain()` |
| R14 | Fewer, musical transition sounds: tonal hits instead of a whoosh on every cut. **Not implemented yet.** It needs a change to `make.cut_cues`/`sfx_events` (owner decision: the SFX density is a separate lane). | §2.6: whooshes 0.6–3.1/min vs our 57 SFX/min | Recommended next step |

## 4. Proof on the orca Short (A = v4 with the old bed, B = v4 with the score)

Same voice, same 81 SFX cues and the same video stream; only the music differs. B was built by `pipeline.audio.make --reuse-tts --extra-cues … --music score`. Measured by `tools/measure_ab.py` (`data/orca_ab/ab_measure.json`, `.png`) and `tools/analyze.py`.

| Check | A (old bed) | B (score) | Target |
|---|---|---|---|
| Integrated loudness, mix.wav | −14.1 LUFS | −14.1 LUFS | −14 |
| True peak: mix.wav / muxed MP4 | −1.3 / −1.3 dBTP | −2.0 / −2.0 dBTP | ≤ −1 |
| Clipped samples, NaN | 0, 0 | 0, 0 | 0 |
| Voice minus music under speech, median (p10–p90) (analyzer mask) | 10.4 (6.9–14.0) | **10.2** (5.6–16.3) | 10–11 (Kurz) |
| … with the stricter `measure_ab` mask | 13.2 (9.7–16.7) | 13.1 (8.5–19.2) | — |
| … through a phone-speaker model (HPF 350 Hz, LPF 9 kHz, 2–4 kHz bump) | 16.5 | **14.8** | music audible but under |
| Speech frames with the music within 20 LU of the voice on a phone | 80 % | **83 %** | higher |
| Voice-to-music SNR at 1–4 kHz, median | 25.5 dB (bed has no top) | **16.0 dB** | ≥ 12 dB |
| Music short-term range | 1.6 dB | **6.4 dB** | 6–12 |
| Texture distance at setting changes vs random | 0.33 vs 0.15 | **0.93 vs 0.46** | ≫ random |
| Cue starts vs setting changes | (no cues) | 10 of 10 on a change, one moved to the answer word "culture" (−0.18 s) | R4, R5 |
| Low-band onset at each cue start (measured in the music stem) | — | within −20…+24 ms at 7 of 10. Tense at 19.35 s: +129 ms. Bookend at 80.07 s: none (intended). Twist at 70.39 s: +72 ms, where the sting on "Except" 0.1 s later carries it. | ≤ 30 ms |
| Stings vs reveal words | — | "The" (liver) / "culture." / "Except" / "About" (sunk): all at −30 ms, onsets measured at +1…+3 ms | R9 |
| Drop-outs | — | 35.29–35.87 (before "The liver."), 62.34–62.92 (before "culture."), 76.64–77.22 (before "About seven boats have sunk"): 23.9 / 29.4 / 22.3 dB deep | R10 |
| Riser rise (in the ducked music stem) | — | 10.1, 4.9, 2.4, 3.3, 2.9, 4.5 dB | audible swell |
| Silence: 200 ms mix windows under −45 LUFS; music under −60 outside drop-outs | none; none | none; none | none |
| Loop seam: music last vs first 200 ms; sample step | −32.4 / −35.6 dB; 0 | −37.7 / −33.7 dB; 0 | ≤ 4 dB, no click |

The plan for the orca (`data/orca_ab/score_plan.json`), as cue start time, mood and intensity:

| Time | Cue |
|---|---|
| 0:00 | tense 0 (hook) |
| 3.3 | board 1 |
| 10.7 | board 2 |
| 19.3 | tense 2 (pod) |
| 24.0 | cold 2 (Antarctica) |
| 30.9 | tense 2 (South Africa map, then Gansbaai) |
| 42.7 | tense 3 (Western Australia, blue whale) |
| 51.4 | question 1 |
| 62.9 | warm 1 ("culture", mother and calf) |
| 70.4 | tense 3 (Iberia twist) |
| 80.1 | tense 0 (bookend) |

- Moods move relative to D: board in D major, warm in F major, question on suspended IV and V chords.
- The last two chords are B♭ and C, which lead back into the D-minor bar 1.

**What could not be verified.** Nobody has listened to it. Musicality (voicings, motif, how the SoundFont presets sound together), whether the stings read as "musical" rather than "SFX", and whether the busier B under the voice tires a listener over several loops all need the owner's ears. The phone figures come from a filter model, not a real handset. The A/B comparison file (`orca_music_ab.mp4`) is a re-encode and peaks at −0.9 dBTP. The deliverable B file is −2.0 dBTP.

## 5. Where the reference is right for us and why

- **Voice first.** About 10 LU is enough for a calm narrator. On a phone our score sits about 15 LU under the voice and is audible 83 % of the time, against 80 % for the old bed. The 1–4 kHz band duck keeps a 16 dB SNR where intelligibility lives.
- **Following the picture.** Our settings change 9.2 times a minute, against their 4.8–6.3. So we do what they do at the texture level and keep cue changes for mood changes and reveals. Restarting the music every 3 s would sound like channel-surfing.
- **The hook.** The music "arrives" on the hook's punch at about 3 s with a hit and the first setting change. That matches both references, and it gives the viewer a second lift exactly where Shorts lose people (the 3 s swipe point).

## 6. What does not transfer from long-form to Shorts

1. **Swells in pauses.** Kurzgesagt's +5 dB "the music fills the pause" depends on 47–83 pauses of 0.5 s or more. Our narration has **zero** (paragraph gaps are about 0.27 s by design). The swell moves to cue boundaries and risers instead: B is +1.8 dB at setting changes against under speech.
2. **Silence under the hook.** W speaks its first line over near-silence (−55 LUFS). On a muted-autoplay feed, with a loop seam, total silence reads as dead air. Our hook plays a quiet pad, motif and sub at about −9 dB relative to the body, and keeps the "arrival at 3 s" idea.
3. **The 10 s intro jingle and the fade-out ending.** Neither fits a looping Short. We use the bookend cue that resolves into bar 1 (R12).
4. **Long cues and big arcs.** Their cues last about 15 s and build over 10 minutes to a climax near the end. We build within 85 s: escalate repeated moods, climax on the last big reveal (blue whale, then the Iberia twist at intensity 3), and return to the hook texture for the loop.
5. **Mix level.** They deliver about −16 to −17 LUFS integrated (long-form YouTube). Shorts need −14. Only the relative numbers transfer.
6. **Sub-bass weight.** Their sub carries real weight on headphones and TVs. On a phone speaker it is gone, so we add harmonics to the sub and keep body in 150 Hz–1 kHz.
7. **Drop-out rate.** 1.6/min suits a 10-minute film. In an 85 s loop we cap it at one per 14 s or more (three in the orca), so the device does not wear out on the second loop.

## 7. Files

- `tools/separate.py`: Demucs separation.
- `tools/words.py`: whisper word times.
- `tools/analyze.py`: all reference measurements.
- `tools/measure_ab.py`: the A/B checks.
- `data/`: JSON, CSV and PNG per video, and `data/orca_ab/` for the proof (plan, MIDI, report, measurements).
- Videos and stems stay on the Spark under `~/studio/work/kurz-music/`. They are never copied to the Mac or committed.
