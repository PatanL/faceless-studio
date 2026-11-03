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

**v2 (round 2, Kurzgesagt Shorts and Epic Mountain soundtracks, `KURZ_MUSIC.md` sections 8–10).**

- The music is full from frame 0.
- Cues are 6–17 s (4–7 per Short), with flatter dynamics.
- Each Short gets at most 3 stings, 2 drop-outs and 2 risers.
- Harmony holds two bars per chord, with modal progressions per mood and a tonic pedal under colour chords.
- One motif is stated in the hook, developed in the second half and restated at the loop.
- Instruments are synth pads and soft plucks (piano, harp, celesta in a long room, doubled by a pad), not marimba,
  kalimba or glockenspiel.
- Pulse and percussion enter in bar 2.

**Fewer SFX (R14).** Set `sfx_mode: musical` in config, a script's front matter, or `--sfx-mode musical`. Each cut
then loses its whoosh, storyboard SFX thin to markers, impacts and a few tonal blips (6/min or fewer), and the score
plays an in-chord harp and celesta figure at each setting change. The default stays `full` until the owner picks.

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

## Qwen3-TTS backend (`tts: qwen3`, opt-in; Kokoro stays the default)

Built by the voice track (research/music/VOICE_CADENCE.md) to reach RicksClips / Zack D. cadence on an **original**
voice. It is in the pipeline but no episode uses it until the owner has heard `out/rnd-voice/voice_AB.m4a`.

```yaml
# script front matter
tts: qwen3            # or --engine qwen3
qwen3_voice: ember    # config.QWEN3_VOICES: ember (default) | nova | spark | iris (--qwen3-voice)
emphasis: off         # rule-marked word stress in capitals, default off (--emphasis on|off); see the caveat below
stress: brush, thirteen   # optional: force these words stressed
unstress: navy            # optional: never stress these
audio_profile: story_ricks  # recommended: cuts pauses to 0.10 s (voicefx.tighten) and sets the story mix
```

- **Voices.** Each voice was designed once from a text description with Qwen3-TTS VoiceDesign. The designed clip
  (`pipeline/audio/voices/<id>_ref.flac`, our own audio) is then the voice prompt for the Base model, so the voice is
  identical in every chunk and episode. The descriptions, seeds and reference texts are in `config.QWEN3_VOICES`.
  To add a voice, design it with `qwen3_worker.py` (a job with `instruct` and no `ref_audio`, VoiceDesign model) and
  register its clip. A voice prompt is never a real person's or a reference narrator's audio.
- **Emphasis.** `emphasis.py` marks about a quarter of the words from the measured rules: the hook's act verb and
  the object after it, numbers, contrast and negation words, "so" + adjective, superlatives, names, SEE in "You
  see", and the last word of a short punch line or of the hook. Those words go to the TTS in capitals (the pilot
  measured this as the most reliable control on the Base model). Captions keep the script's own text.
  **Caveat, so it is off by default:** capitals raise the marked words (+3.4 to +3.9 st over the rest, against
  +1.0 to +1.6 plain) but sometimes make the model spell or bend a word. Examples: WROTE read as letters, LAUGHING
  heard as "lacking", and JAPAN'S, YI and VASA bent. `*asterisks*` were worse (a doubled "-ing"). Turn it on per
  script and veto any bent word with `unstress:`.
  `python -m pipeline.audio.emphasis file.txt` prints the marks.
- **Timings.** The worker force-aligns each chunk's script words (torchaudio MMS_FA, a CTC aligner). synthesize()
  gets `(audio, sr, [(word, start, end)])` exactly as it does from Kokoro, so captions, `[sfx:]` markers, cut cues
  and the mix work unchanged (coverage 1.0, `timing_source: ["qwen3"]`). If alignment ever covers under 60 % of the
  words, the existing faster-whisper fallback runs.
- **Where it runs.** It runs in its own venv through `qwen3_worker.py`, with every chunk of a script in one worker
  call (the model loads once). It uses MPS on the Mac or the CPU, and refuses CUDA. On an M1 Pro (bf16, MPS) it runs
  at about 2.1–2.4× real time, so a 62 s Short takes ~2.5 min. The Spark has no Qwen venv yet: running it there on
  CPU needs the same install (below) and is untested.
- **Install (Mac, done 2026-11-02):**
  ```bash
  git clone https://github.com/QwenLM/Qwen3-TTS ~/faceless-work/src/Qwen3-TTS   # read at 022e286
  /opt/homebrew/bin/python3.13 -m venv ~/faceless-work/venvs/qwen3tts
  ~/faceless-work/venvs/qwen3tts/bin/pip install ~/faceless-work/src/Qwen3-TTS   # transformers 4.57.3, torch 2.15
  cd ~/faceless-work/models
  ~/faceless-work/venvs/qwen3tts/bin/hf download Qwen/Qwen3-TTS-12Hz-1.7B-Base --revision fd4b254389122332181a7c3db7f27e918eec64e3 --local-dir Qwen3-TTS-12Hz-1.7B-Base
  ~/faceless-work/venvs/qwen3tts/bin/hf download Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign --revision 5ecdb67327fd37bb2e042aab12ff7391903235d3 --local-dir Qwen3-TTS-12Hz-1.7B-VoiceDesign
  ```
  Each model is 4.5 GB, and peak memory is about 5.8 GB. Paths come from `config.QWEN3`, or from the
  `QWEN3_TTS_PYTHON` and `QWEN3_TTS_MODELS` environment variables.

### Hosted engine: `qwen_api` (designed for, not wired)

`tts: qwen_api` is the slot for Alibaba Cloud Model Studio (DashScope) TTS, e.g. the Qwen-Audio TTS Plus model that
leads the Artificial Analysis arena (about $19 per 1M characters, roughly 2–3 cents per Short). It already plugs into
the same `render_many()` interface as `qwen3`. Today it stops with a clear message, because there is no key and
spending is the owner's decision. To finish it:

- **Key:** `DASHSCOPE_API_KEY` in the environment, or in `~/studio/.env` on the Spark (the engine already reads both).
- **Endpoint:** `POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`
  (Singapore; Beijing is `dashscope.aliyuncs.com`), `Authorization: Bearer <key>`. Body:
  `{"model": <model id>, "input": {"text", "voice", "language_type": "English", "instructions"}}`. The reply carries
  a URL to the audio. The documented SDK call is `dashscope.MultiModalConversation.call`.
- **Style and emphasis:** on the instruct models (`qwen3-tts-instruct-flash` in the docs), `instructions` takes the
  same text as `emphasis.instruct_for(marks, description)`. Send the capitalised text from `plan_texts()` either way.
  Requests are limited to about 600 characters, so send one paragraph chunk per request.
- **Voice:** the API has its own preset voices (e.g. "Cherry", "Ethan"). Ours can only be used if the API offers
  voice design from a text description; never upload anyone else's audio.
- **Word timings:** the API returns none, so align the downloaded audio with `qwen3_worker.align()` (the same MMS_FA
  forced alignment, run in the qwen3 venv), or let the faster-whisper fallback handle it.
- Check the exact model id and parameter names against the current Model Studio reference before wiring it. These
  were taken from the docs page and are not yet tested. Once a key exists, the engine joins the voice A/B.

## Audio profiles (`config.PROFILES`, opt-in per episode)

A profile overlays a niche's settings when the script's front matter says `audio_profile: <name>`, or when make is run
with `--profile <name>`. Front-matter keys such as `speed:` still win over the profile. Episodes without a profile mix
exactly as before.

**`story_ricks`** is the story lane, matched to the 8 RicksClips3000 references (`research/music/RICKS_SOUND.md`; A/B
in `out/rnd-sound/`). It sets the following:

- **Music.** `score.compose_story`: a continuous, plucky, mostly minor track at 100–116 BPM, in pizz, harp, celesta and
  finger bass with no drums. It has its own 4-bar sections and no stings or drop-outs. It sits about 21 LU under the
  voice (`music_db −13`, `duck −2.5`).
- **Voice.** `voicefx.tighten` cuts pauses to 0.10 s at TTS time, before caching. `voicefx.process` runs at mix time:
  HPF 90 Hz, EQ, parallel compression, a limiter and an air exciter.
- **SFX.** Storyboard action cues are on (`action_sfx`). Whooshes are shorter (`sfx_rate`) and per-cue levels sit
  15–21 LU under the voice (`sfx_db`).

`report.json` records `audio_profile`. The score's provenance keeps `generator: pipeline.audio.score` and adds
`arrangement: story_ricks`.

## Proof (2026-11-01)

`samples/b5_horror_30s.md` produced 52 words and 6 cues (4 from markers, 2 automatic) in a 33.2 s file: 30.2 s of voice plus a 3 s stinger tail. Results:

- Loudness: **-14.0 LUFS, -1.6 dBTP** on mix.wav, on Remotion's own render and on the muxed MP4.
- Ducking: the music sits 7.0 dB lower under the voice than in the gaps.
- Timing coverage: 100 % from Kokoro.

`studio/storyboards/b5-audio-demo.json` (built by `demo_storyboard.py`) renders the sample with B2. The captions and the SFX labels and shakes line up with the audio (see `out/B5/`).
