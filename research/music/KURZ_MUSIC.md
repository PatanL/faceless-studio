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

> **Level (owner, 2026-11-01).** The owner kept the score as the default but found it too loud: "music should be background". The coordinator set `score_mix` to `music_db −12`, `duck_db −4.5` (b338acb), so the voice sits about 17 LU over the score on the orca instead of ~10–11 (Kurzgesagt's long-form level). The owner confirmed that level, and round 2 keeps it. Round 2's Shorts data supports the choice: Kurzgesagt's own Shorts sit at a median of **13.6 LU** (§8.2).

---

# Round 2 (2026-11-02): Kurzgesagt's Shorts, the soundtracks, and a deeper score

Same method and rules as round 1. Everything ran on the Spark, CPU only, at `nice 10`. Reference audio stays on the Spark (`~/studio/refs/kurz-shorts`, `~/studio/refs/kurz-ost`) and is never committed. Everything we ship is still generated by our code.

New tools:

- `tools/cuts.py`: visual-change timeline for the Shorts.
- `tools/shorts_summary.py`: how the music lands, sits in sections and ends.
- `tools/harmony.py`: chord and key HMM, roman numerals.
- `tools/structure.py`: layers and recurring themes.
- `tools/palette.py`: preset matching and our comparison clips in `palette/`.
- `tools/sfx_residual.py`: isolates SFX by explaining the video's music with the released soundtrack.

## 8.1 Sources

**Kurzgesagt Shorts (10).** These are the top viewed of the latest 60 on @kurzgesagt/shorts, 1.4M–5.4M views, 60–84 s:

| ID | Title |
|---|---|
| `2cK8l5Yg5w8` | Deadliest Thing in Your Kitchen |
| `UC5Mpc-GQCg` | Moon's Invisible Threat |
| `KTu2V65Iiho` | Why Does Cocaine Feel So Good? |
| `tZ8i1RxGSYM` | Can Earth Run Out of Water? |
| `VYhUa3WC4nU` | Why Being Poor Is Expensive |
| `Gn-KqiRv0XI` | Most Average Person |
| `6Dj5ufzrZ78` | Could Humans Evolve Flight? |
| `YqAI0oqtt7w` | Dust Is Not What You Think |
| `OxOx6--oN8I` | Most Dangerous Animal |
| `sravy3Vjdlw` | Nature's Ultimate Impostor |

Each Short went through Demucs and whisper as in round 1. Its setting changes come from `cuts.py`, a colour-histogram change detector run at 10 fps. That detector is a stand-in for the hand catalogue and over-counts camera moves somewhat.

**Epic Mountain soundtracks (6)**, clean music with no voice. Epic Mountain's official YouTube channel publishes one "– Soundtrack (year)" upload per video. Bandcamp (`epicmountain.bandcamp.com`) sells only two unrelated live songs, so YouTube is the clean source:

| ID | Soundtrack | Year |
|---|---|---|
| `TeRxsGUPXb8` | Deep Sea (the D video's own score) | 2019 |
| `6Yo8x9BAgRw` | Peto's Paradox (the W video's own score) | 2020 |
| `nB0snrTDS2o` | You vs Cancer | 2023 |
| `y4Qmn4WzZxI` | Autoimmune | 2025 |
| `xFX0mEnkNQ4` | Friends | 2022 |
| `Bw6KsPiYuO8` | Optimistic Nihilism | 2017 |

## 8.2 Shorts vs long-form (the biggest corrections)

Medians across the 10 Shorts, with the range in brackets. The long-form columns repeat round 1.

| | **Shorts** (10) | Long-form D / W |
|---|---|---|
| Narration speed | 177 wpm (161–187) | — |
| Picture changes / min | 14 (10–20) | 4.8 / 6.3 (settings) |
| **Music at its level from frame 0** (1 s level within 6 dB of its median) | **0.05 s in 8 of 10**. The two others: 1.65 s and 3.85 s | lands at 3.2–3.75 s over a near-silent hook |
| Music level in the first second vs its median | −2.1 dB (−10.3…+6.0) | −20 to −40 dB |
| Hook: first sentence ends / first picture change | 2.0 s / 2.15 s | 4–5 s |
| **Voice minus music while talking** | **13.6 LU** (2.5–23.6) | 10.0 / 11.1 |
| Music short-term range | **3.9 dB** (1.7–11.9) | 8.9 / 11.9 |
| Pauses of 0.5 s or more | 0 (0–3) | 47 / 83 |
| **Music sections / min; sections per Short** | **3.5** (2.3–4.5); **5.5** (4–7), about 12–17 s each | 3.3 / 3.9 per min |
| Music texture change at picture changes vs random moments | 0.47 vs 0.47 (no relation) | 0.40 vs 0.35, 0.50 vs 0.32 |
| Risers / min | **0** (0–0.8) | 2.7 / 2.8 |
| Drop-outs / min | 0.75 (0–3.0) | 1.6 / 1.6 |
| Low hits / min | 0.8 (0–18) | 9.9 / 8.3 |
| Sections with drums within 10 dB of the music | 25 % (5 of 10 Shorts have drums in at least half their sections) | 10–12 % |
| Minor sections | 74 % | 59–69 % |
| Last word to the end of the video | 0.5 s (0.37–1.57) | — (end card, outro) |
| Music level over the last second vs its median | −0.8 dB. 7 of 10 end at full level; 3 fade (−10 to −20 dB) | fade over ~4 s |
| Harmony at the end vs the start (chroma cosine) | 0.88 (0.54–0.98) | — |

- **The music is there at frame 0.** It is already at its working level, with no near-silent hook and no "arrival" at 3 s. The hook line is about 2 s long and the picture changes once in it.
- **It is quieter.** The voice sits about 13.6 LU over the music. That supports the owner's "background" level.
- **It is flatter.** The music varies about 4 dB rather than 9–12.
- **It uses fewer devices.** No risers, under one drop-out a minute, few hits.
- **It is organised in 4–7 sections of 12–17 s**, not around the 14/min picture changes.
- **It runs to the end at level and loops harmonically** (end chroma close to the start), even though Kurzgesagt's Shorts don't loop their narration.
- **Beats are more common than in long form.**

## 8.3 Harmony (clean soundtracks)

| Soundtrack | BPM | Chord length, median (beats) | sus2 + sus4 | maj7 | dom7 | Pedal or inversion | Minor-key share | Modulations |
|---|---|---|---|---|---|---|---|---|
| Deep Sea | 117.5 | **10** | 38 % | 18 % | 0 % | 13 % | 29 % | A → Dm → C♯ → F♯m (3) |
| Peto's Paradox | 123 | 9.5 | 22 % | 32 % | 0.4 % | 19 % | 59 % | Bm → F♯ → B → G → E♭m (4) |
| You vs Cancer | 103 | 7 | 4 % | **52 %** | 1.7 % | 5 % | 24 % | E → A → Am → E → Am (4) |
| Autoimmune | 117.5 | 4 | 21 % | 13 % | 1.4 % | 11 % | 72 % | Am → Cm → E → F♯ (3) |
| Friends | 117.5 | 6 | 12 % | 24 % | 0 % | 19 % | 43 % | A ↔ Em … → G (5) |
| Optimistic Nihilism | 117.5 | 8 | 9 % | 15 % | 0 % | 13 % | 100 % | Dm (0) |

- **Slow harmonic rhythm.** A median of 4–10 beats a chord, about 2–5 s at 117.5 BPM. Deep Sea sits on one A-sus2 chord for 88 beats (0:99–2:25). The movement comes from arpeggios over a held chord, not from chord changes. Our round-1 score changed chord every bar (2.2 s).
- **Tonic-centred and modal.**
  - The tonic chord in some colour (I, i, Isus2, Imaj7) covers 40–60 % of the time.
  - Dominant-seventh cadences are almost absent (0–1.7 %).
  - The recurring moves are borrowed or modal chords around the tonic.
- **Recurring moves:**

  | Move | Character | Found in |
  |---|---|---|
  | I–bVImaj7–bVII–I(sus2) | wonder | Deep Sea; Friends `bVImaj7-bVIImaj7` |
  | i–bIII–v and iv–bIII | reflective | Optimistic Nihilism |
  | i–bvi and V–i | tension | Autoimmune `i-bvi` ×16, `V-i` ×11 |
  | Imaj7–#IVmaj7 | Lydian float | Peto's Paradox |
  | i–bIImaj7 | Phrygian, dark depths | Deep Sea 4:09–4:17; You vs Cancer |
  | I–v7–bVIImaj7–Isus4 | bright, playful | Friends `I-v7` ×12, `v7-bVIImaj7` ×9 |

- **Mood.** Sus2/sus4 and maj7 carry the "open, curious" sound. Minor triads with bVI and bII carry danger and depth.
- **Modulations** come every 2–3 minutes (0–0.6/min), mostly by a 4th or 5th (10 of 19). In an 85 s Short that means **at most one key change**.

## 8.4 Melody and motifs

`structure.py` matches 8-beat windows of the top register (C5–C8), allowing transposition. Pure ostinato is excluded.

- **A theme returns 60 s or more later in 5 of 6 soundtracks.** Deep Sea is the exception: its one return is two statements 127 s apart.
- **Optimistic Nihilism** states a theme at 1:37 and brings it back at 5:25 and 5:51, the last minute of a 6:12 track: a recapitulation near the end.
- **You vs Cancer** has themes returning up to 192 s later (4:07 → 7:18).
- **Friends** develops one theme 13 times over 138 s at different pitches (C5, G5, D5, F♯5) and brings it back at 7:56.
- **Peto's Paradox** returns its theme 5 times over 88 s, and each return is louder (−23 → −17 dB) and brighter (spectral centroid 860 → 1,250 Hz).
- **Within a section,** themes repeat every 8 beats (Autoimmune, Friends), as a cell over the slow chords.

**For an 85 s Short:** state a short motif in the hook, develop it once or twice in the second half (louder, higher, a new instrument, or stretched), and restate it in the loop bookend.

## 8.5 Sound palette (our comparison clips: `research/music/palette/*.mp3`)

**Reference note events.** 900 isolated note onsets above 1 kHz from the soundtracks' "other" stems fall into three groups, and all three are soft:

- attack 77–88 ms;
- decay only 11.5–13.6 dB/s;
- a steeply falling, dark-topped spectrum.

They are "soft synth" plucks and keys in a big room.

**Raw GeneralUser GS presets** are much harder and shorter: 5–30 ms attack and 33–90 dB/s decay.

Distance to the nearest reference group (lower is closer, in standardised units):

| Treatment | Candidates (distance) |
|---|---|
| **Closest** | `piano` + room treatment (**1.06**), `harp` + room (**1.10**), piano + celesta an octave up + warm pad doubling (1.11), harp + warm pad (1.17) |
| Raw | piano (1.15), harp (1.18), celesta (1.34) |
| **Far** | glockenspiel 1.70, kalimba 1.92, vibraphone 2.09, marimba 2.14, crystal 2.31, tinker bell 3.03 |

- "Room treatment" means LPF 6.5 kHz, light chorus, a dotted-8th echo and a long bright reverb.
- Round 1 used glockenspiel, marimba and kalimba in several moods. They are among the furthest from Kurzgesagt's sound.
- Doubling a pluck with a quiet pad note (`harp+warmpad`) brings the attack to 75 ms. Its decay then stays too slow (27 dB/s), so the doubling goes on alternate notes only.

**Pads.** Synth pads are closest:

| Pad | Distance |
|---|---|
| Warm Pad | **0.50** |
| Halo Pad | **0.51** |
| Soundtrack | 0.64 |
| Fantasia | 0.66 |
| Atmosphere | 0.67 |
| Synth Strings | 0.81 |
| **Orchestral Slow Strings** | 1.57 |
| **Concert Choir** | 1.85 |

Round 1 used orchestral strings as the main pad for the tense and warm moods.

## 8.6 Layering

`structure.py` uses the soundtrack stems: sub, bass, sustained pad, keys and arps, lead line, percussion.

| | Median over the 6 soundtracks (range) |
|---|---|
| Section length | 13 s (12–14) |
| Layers present in a section's first 2 s | **4** (3–5) |
| Layers at the section's fullest | 5 (4–6) |
| Sections that add a layer after their start | 85 % (77–97) |
| Time from section start to the full layer count | **2.8 s** (1.0–4.5) |
| Layer that enters first | sub (19–30 sections per track), else pad |
| Runtime with the pad on | **98 %** |
| Runtime with keys or arps on | 68–94 % |
| Runtime with percussion on | 29–62 % |
| Runtime with a lead line standing out | ~25 % |

**A cue starts nearly full and adds the last layer or two within about one bar. It does not grow slowly from one instrument.**

- The pad never stops. Arps run most of the time.
- Percussion comes and goes with the energy.
- In the Shorts, the music "lands" in the first 0.05 s and keeps 4–7 sections. That is the same "start full, vary one layer" pattern, packed tighter.

## 8.7 Sound effects (The Deep Sea, isolated with its own soundtrack)

`sfx_residual.py` aligns the video's music stem to the released score with 20 s chunks.

- The edit offsets come out as −34.5, −33.4, −29.1 and −19.8 s; the video inserts material that the soundtrack doesn't have.
- 73 % of the runtime aligns, and the soundtrack explains 63 % of the music stem's power.
- What remains, where it is at least as loud as the music and jumps 8 dB, is the sound design.

| | |
|---|---|
| Events | **43, about 5.2/min** |
| Tonal (spectral flatness 0.3 or less) | **98 %**. Almost no noise whooshes |
| In key with the surrounding music (chroma cosine above 0.8) | **63 %** |
| Level vs the music | −0.5 dB (about the same) |
| Level vs the voice | −15 dB |
| Length | median 0.14 s |
| Visual transitions with an SFX within 0.5 s | **3 of 47** |

Kurzgesagt's sound design is a few short, tonal, mostly in-key blips at the music's level. Transitions are carried by the music, not by whooshes. Our v3/v4 orca has 81 SFX in 84.6 s (57/min), with a whoosh or bubbles on every cut.

**Caveats.** The residual also holds edit and mix differences, and only 73 % of the runtime aligned. Treat 5/min as an order of magnitude.

## 9. What changed (pipeline/audio/score.py v2, make.py, config.py)

| Rule (round 2) | Evidence | Change |
|---|---|---|
| R15 Start full: the hook cue plays at about −1 dB, with pad, arp, bass and sub from frame 0 (no pulse or percussion) | §8.2: 8 of 10 Shorts at level in 0.05 s | Replaces R11's sparse −9 dB hook and its riser |
| R16 Fewer, longer cues: same mood merges up to 17 s; cues under 6 s join a neighbour; runs over 18 s split at sentence starts (building before 60 %, breathing after) | §8.2: 4–7 sections of 12–17 s | `MIN_CUE`, `MAX_CUE`. Orca: 11 → 9 cues |
| R17 Flatter dynamics: intensity −2.5 / −1 / 0 / +1 dB | §8.2: 3.9 dB range | `INTENSITY_DB`. Orca range 6.4 → 3.3 dB |
| R18 Devices capped per Short: 3 or fewer stings (6 s or more apart), 2 or fewer drop-outs (20 s or more apart), 2 or fewer risers (the biggest jumps only) | §8.2: risers 0/min, drop-outs 0.75/min | `MAX_STINGS/DROPS/RISERS`. Orca: 4 / 3 / 6 → 3 / 2 / 2 |
| R19 Harmony from the soundtracks: two bars a chord, tonic-centred modal moves per mood (table below), tonic pedal under bII, bIII and #IV, tempo 117.5 | §8.3 | `MOODS`, `BPM`, chord grouping |
| R20 One motif, developed: stated in the hook, developed in the warm or resolution cue (piano, stretched 1.5×) and the climax (an octave up, celesta over piano, +10 velocity), restated in the bookend | §8.4 | `motif_cues` |
| R21 Kurzgesagt palette: synth pads (warm, halo, soundtrack, atmosphere) instead of orchestral strings; soft plucks (piano, harp, celesta) with the room treatment and pad doubling; no marimba, kalimba or glockenspiel | §8.5 | `MOODS` instruments, the `keys` FX chain, `double` |
| R22 Layering: cues start with 4 layers; pulse and percussion enter in bar 2; percussion rests for the last 2 beats before a new cue | §8.6 | `late`, `tail_cut` |
| R14 (now implemented) `sfx_mode: musical`: no whoosh or bubbles per cut; storyboard SFX thin to markers, impacts and a few tonal UI sounds (2.5 s or more apart, 6/min or fewer); the score plays a short in-chord harp and celesta figure plus a soft low thump at each setting change that isn't a cue start or a sting | §8.7 | `config.sfx_mode` (default `full`) and `sfx_musical`; `make.py --sfx-mode`, `musical_sfx()`; `score.plan(transitions=True)`. Orca: 81 → 8 SFX (5.7/min) + 5 tonal transition hits |

**Progressions per mood.** Each chord lasts two bars.

| Mood | Progression | Source |
|---|---|---|
| curious | Isus2 · Imaj7 · bVImaj7 · bVII(add9); alt Imaj7 · #IVmaj7 · Imaj7 · Vsus4 | Deep Sea; Peto's Paradox |
| board | I(add9) · v7 · bVIImaj7 · Isus4 | Friends |
| tense | i · bVI · Vsus4 · V; alt i · bIII · v · iv | Autoimmune; Optimistic Nihilism |
| cold | Isus2 · bIIImaj7 · Isus2 · v | Deep Sea |
| warm | Imaj7 · bVImaj7 · IVmaj7 · Imaj7, in the relative major | You vs Cancer |
| question | Imaj7 · #IVmaj7 · Imaj7 · Vsus4 | Peto's Paradox, Lydian |
| deep | i(add9) · bIImaj7 · i · bVImaj7 | Phrygian |

**Superseded long-form rules, now that Shorts data exists:**

- R11, the sparse hook, is replaced by R15.
- R8, risers at 2.7–2.8/min, is cut to at most 2 per Short.
- R2, the 6–9 dB range, is now about 4 dB.
- R4, texture at every setting change: Kurzgesagt's Shorts don't follow their 14/min picture changes. We keep a light colour change at our settings, and in `musical` mode the tonal transition hits take that job.

## 10. Proof: orca v4, three versions at the approved level (music_db −12, duck −4.5)

Same voice, same storyboard SFX in A and B, same v4 picture. Built with `pipeline.audio.make --reuse-tts --extra-cues … --music score [--sfx-mode musical]`. Measured with `tools/measure_ab.py` (`data/orca_ab_r2/`) and `tools/analyze.py` (`data/ORCA_r2_*`).

| Check | A: current score | B: new score | C: new score + fewer SFX |
|---|---|---|---|
| Phone MP4 `out/lantern/` (720×1280, 1.7 Mb/s, AAC 192k) | `orca_v4_score_A_current.mp4`, 19.2 MB | `orca_v4_score_B_new.mp4`, 19.1 MB | `orca_v4_score_C_new_fewer_sfx.mp4`, 19.1 MB |
| Loudness / true peak (MP4) | −14.1 LUFS / −2.0 dBTP | −14.1 / −2.1 | −14.1 / −2.2 |
| Clipped samples, NaN, dead air, silent music outside drop-outs | 0, 0, 0, 2 windows | 0, 0, 0, 0 | 0, 0, 0, 0 |
| Voice minus music while talking, median (`analyze.py` mask, as for the references) | 16.2 LU | 15.7 LU | 16.0 LU |
| … with the `measure_ab` mask | 19.1 LU | 18.5 LU | 18.7 LU |
| Voice-to-music SNR at 1–4 kHz | 21.9 dB | 21.8 dB | 22.5 dB |
| Speech frames with the music within 20 LU of the voice on the phone model | 44 % | **50 %** | **51 %** |
| Music short-term range | 6.4 dB | **3.3 dB** | 4.2 dB |
| Cues / stings / drop-outs / risers | 11 / 4 / 3 / 6 | **9 / 3 / 2 / 2** | 9 / 3 / 2 / 2 |
| Music sections / min (novelty) | 3.6 | 4.3 | 4.3 (Kurz Shorts 3.5) |
| SFX in the mix | 81 (57/min) | 81 | **8 (5.7/min)** + 5 tonal transition hits in the score |
| Cue starts vs setting changes | on a change | all 8 within 0.18 s of a setting change (one moved to "culture", one split section on a sentence start 0.15 s after a change). Measured low onsets −41…+122 ms | same; −18…+87 ms |
| Stings vs words ("The" liver / "Except" / "About" sunk) | — | −30 ms each. Measured onsets +1, +147, +2 ms | +1, +2, +2 ms |
| Drop-out depth | round 1: 22–29 dB | 17.3 / 18.2 dB | 15.3 / 10.7 dB |
| Loop seam: music last vs first 200 ms; sample step | −43.3 / −39.0 dB; 0 | −33.8 / −31.3 dB; 0.0001 | −32.7 / −30.6 dB; 0.0002 |

- **Seam.** B's bookend sits 2.5 dB above its cue level. At first the hook's bar 1, which also carries the wrapped tail, was 6.5 dB louder than the bookend's last bar. Now the step is the bar-1 downbeat only (+2.5 dB for 200 ms).
- **True peak.** The C mix measured +0.3 dBTP after an AAC encode at 160 kb/s: a codec overshoot at 67.4 s on a mix that is −2.1 dBTP. At 192 kb/s it measured −2.2. The phone files use 192k. `pipeline.audio.mux` already encodes at 256k.

**What can't be verified without ears:**

- whether the slower harmony and synth pads read as "Kurzgesagt-like" rather than static;
- whether the soft doubled plucks smear under the voice on a phone;
- whether the motif's return on the Iberia twist feels earned;
- whether the tonal transition hits in C read as music or as sound effects;
- whether C's thinner sound design loses impact at the liver and boat moments, where the impacts and markers remain;
- whether the bar-1 downbeat at the loop seam is noticeable.

Key estimates of our own score are rough: the board mood, D-mixolydian, reads as "G major".

## 11. Files (round 2)

- **Tools:** `tools/cuts.py`, `shorts_summary.py`, `harmony.py`, `structure.py`, `palette.py`, `sfx_residual.py`.
- **Data:**
  - `data/shorts/*` (per-Short analysis and `summary.json`);
  - `data/round2/*` (harmony and structure per soundtrack, `palette.json`, `D_sfx.json`);
  - `data/orca_ab_r2/*` (A/B/C measurements, plans and MIDI);
  - `data/ORCA_r2_*` (analyzer output).
- **Clips:** `palette/*.mp3`. These are our renders only: the closest preset treatments playing the same phrase over a warm pad.
