# pipeline/audio: script to voice, captions and mix (lane B5)

Runs on the Spark, on CPU only (`CUDA_VISIBLE_DEVICES=""` is forced). The Mac only syncs code.

```bash
# from the Mac: push code (no npm needed), then work on the Spark
SKIP_NPM=1 scripts/spark_sync.sh
ssh dgx-spark
source ~/studio/app/scripts/spark_env.sh && cd ~/studio/app
python -m pipeline.audio.synth                       # (re)build SFX + beds once (15 s)
python -m pipeline.audio.make stories/x/script.md --niche horror --id ep-x --meta-out episodes/ep-x/audio
# render the storyboard (captions.src + audio from audio.storyboard.json), then optionally:
python -m pipeline.audio.mux studio/out/ep-x.mp4 studio/public/episodes/ep-x/mix.wav studio/out/ep-x-final.mp4
```

A 30 s script takes about 10 s of wall time: Kokoro runs at roughly 0.3–0.7× real time on 6 threads, and the mix takes under 1 s.

## Voices (picked from B1's samples)

| Niche | Voice | Speed | Chain |
|---|---|---|---|
| explainer | Kokoro `am_michael`, a calm US documentary male | 0.96 | HPF 70 Hz, 2.5:1 compression, +1.5 dB presence at 3.2 kHz |
| horror | Kokoro `bm_george`, a tense first-person UK male | 1.02 | HPF 80 Hz, 3:1 compression, +1.5 dB at 250 Hz (close-mic), short room echo |

To override a voice, use `--voice/--speed/--engine piper`, or set `voice:`/`speed:` in the script's front matter. All settings are in `config.py`.

## Script format (`script.py`)

The narration is read from a fenced ```` ```narration ```` block. If there isn't one, the parser falls back to a `## Narration` / `## Script` / `## VO` section, then to `VO:` lines, then to the whole body. Front matter, headings and tables are ignored. Paragraphs are separated by a pause (0.38 s explainer, 0.55 s horror). Inline markers:

- `[sfx: knock3]` fires at the next spoken word.
- `[sfx: stinger @0.15 vol=-2]` adds an offset in seconds and a level change in dB.
- `[sfx: knock3_slow wait]` plays the sound and holds the narration until it ends.
- `[pause: 0.8]` inserts silence.
- `[music: dread]` or `[music: none]` sets the music bed.

Auto SFX: keywords trigger cues ("knocks" → `knock3`, "buzzed" → `phone_buzz`, "text" → `notify`, "sonar" → `sonar_ping` and others, listed per niche in `config.py`). An auto cue never fires within 1.5 s of another cue. Turn them off with `--no-auto-sfx`.

## Timing → captions

Kokoro token timestamps are merged into words (punctuation and contractions attach to their word), then aligned to the script's own words with difflib, so captions show the script text exactly. If coverage drops below 60 % (or with `--whisper` / Piper), faster-whisper `base.en` int8 aligns instead. `captions.json` is `{"words":[{"text","start","end"}]}`, which is B2's `Word` schema, so use it as `captions.src`.

## Mix (`mix.py`)

- The voice is set to a reference level of -20 LUFS.
- The bed sits `music_db` below the voice (-15 dB explainer, -12 dB horror).
- **Sidechain-style ducking**: the voice's own activity (10 ms RMS, 0.25 s hold) drives the music down by `duck_db` (-9 / -7 dB). Attack is 0.10–0.12 s, release is 0.55–0.8 s, and there is **80–100 ms of lookahead**, so the bed starts dipping before the first syllable. SFX act as a second, lighter key (-4 / -5 dB) so knocks and stingers punch through.
- Each SFX is placed at its cue time and leveled by its active RMS relative to the voice (`SFX_DB`).
- The final stage gains to **-14 LUFS integrated** and runs a lookahead brickwall limiter with a true-peak check (4× oversampled), iterating until the result is within 0.2 LU and at or below -1 dBTP. ffmpeg `ebur128` then checks it independently (see `report.json`).
- Outputs: `mix.wav`, stems (`voice`/`music`/`sfx`.wav at mix gain), `cues.json` (global times for visual sync, e.g. camera shake on impacts), `audio.storyboard.json`, `report.json` and `waveform.png`.

## Library (`synth.py`, all original, CC0, see LICENSES.md)

SFX in `studio/public/sfx/<cue>.wav` (B2 `cue` names): boom, breath, bubbles, click, clock_ticking, ding, door_creak, drone, footsteps, glitch, heartbeat, heartbeat_fast, heartbeat_slow, impact, knock, knock3, knock3_slow, message_pop, message_send, notify, phone_buzz, phone_buzz_long, pop, riser, sonar_ping, static, stinger, tick, typing, underwater_rumble, whoosh, whoosh_long.

Seamlessly looping beds in `studio/public/music/`: `deep_ocean` and `documentary_pulse` (explainer; `deep_ocean` is
the fallback for the score), `dread` and `tension_pulse` (horror).

`python -m pipeline.audio.synth --sheet sfx.png` draws every SFX (waveform over spectrogram) for a visual check.

## Scored soundtrack (`score.py`, music `score`, the explainer default)

The research behind it is in `research/music/KURZ_MUSIC.md`. The music is composed per episode from the storyboard's
per-scene `setting` timeline, the word timings and the script's SFX markers:

- **Moods.** A mood per setting run, from the place, its light and the words spoken there: curious, board, tense,
  cold, warm, question or deep.
- **Cues.** Cues last 4–16 s (longer runs split at sentence starts). A cue boundary moves onto a pivot or answer word
  up to 1.2 s before a setting change. Inside a cue, every setting change adds colour.
- **Reveals.** Stings land on reveal words, at most 3 drop-outs come before the strongest reveals, and risers lead into
  cues whose intensity rises.
- **Hook and loop.** The hook is sparse and lands with a hit on the first setting change. For `ending: loop`, a bookend
  cue resolves into bar 1 and the tail is wrapped onto the start.
- **Rendering.** Notes are rendered with FluidSynth from GeneralUser GS (`sf2.py`, licence-pinned by sha256). The sub
  bass and booms are synthesized in numpy. Effects (reverb, EQ, compression) come from pedalboard.

```bash
bash scripts/spark_music_setup.sh          # once: FluidSynth (user space), the SoundFont, pretty_midi/mido/pedalboard
# after the storyboard exists (studio-make does this itself: Make.remix_score after the storyboard step)
python -m pipeline.audio.make episodes/<slug>/script.md --id <slug> --reuse-tts --music score \
    [--extra-cues episodes/<slug>/audio/sfx_events.json]
python -m pipeline.audio.score episodes/<slug>/storyboard.json --out /tmp/s --loop   # score only
```

**Mix and fallback.**

- Levels for the score (`config.score_mix`): about 10 LU under the voice while it talks, a 3.5 dB duck, and an extra
  −6 dB band duck at 1–4 kHz under the voice (`duck_band`), with a true-peak ceiling of −2 dBTP so the AAC encode stays
  under −1.
- Without a storyboard (the first TTS pass), or if FluidSynth or the SoundFont is missing, the mix uses `deep_ocean`
  and records `music_fallback_reason` in `report.json`.

**QA.**

- `report.json` carries `music_provenance` (generator, SoundFont, sha256). The gate passes `score` only when the
  SoundFont is one of the cleared ones.
- `score_plan.json` and `score.mid` are copied to `episodes/<slug>/audio/`.
- `research/music/tools/measure_ab.py` measures an old-vs-new pair: loudness, voice gap on a phone model, the
  1–4 kHz SNR, cue timing, drop-out depth and the loop seam.

## Proof (2026-11-01)

`samples/b5_horror_30s.md` produced 52 words and 6 cues (4 from markers, 2 automatic) in a 33.2 s file: 30.2 s of voice plus a 3 s stinger tail. Results:

- Loudness: **-14.0 LUFS, -1.6 dBTP** on mix.wav, on Remotion's own render and on the muxed MP4.
- Ducking: the music sits 7.0 dB lower under the voice than in the gaps.
- Timing coverage: 100 % from Kokoro.

`studio/storyboards/b5-audio-demo.json` (built by `demo_storyboard.py`) renders the sample with B2. The captions and the SFX labels and shakes line up with the audio (see `out/B5/`).
