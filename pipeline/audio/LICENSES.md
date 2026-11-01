# Audio licences (lane B5)

Every sound the pipeline ships with is **generated from code in this repo**. No samples,
loops, presets or recordings were downloaded, and nothing came from the reference videos.

| Asset | Path | Source | Licence |
|---|---|---|---|
| 32 SFX (`boom`, `breath`, `bubbles`, `click`, `clock_ticking`, `ding`, `door_creak`, `drone`, `footsteps`, `glitch`, `heartbeat`, `heartbeat_fast`, `heartbeat_slow`, `impact`, `knock`, `knock3`, `knock3_slow`, `message_pop`, `message_send`, `notify`, `phone_buzz`, `phone_buzz_long`, `pop`, `riser`, `sonar_ping`, `static`, `stinger`, `tick`, `typing`, `underwater_rumble`, `whoosh`, `whoosh_long`) | `studio/public/sfx/*.wav` | `pipeline/audio/synth.py`: numpy/scipy synthesis from sine/saw oscillators, seeded noise, filters, and a convolution reverb whose impulse response is seeded noise | Original work of this project. Released as CC0-1.0. |
| 4 music beds (`deep_ocean`, `documentary_pulse`, `dread`, `tension_pulse`) | `studio/public/music/*.m4a` (the `.wav` masters are rebuilt on the Spark and not committed) | `pipeline/audio/synth.py` (additive pads, plucks, drones; the chord progressions are generic and not taken from any song) | Original work of this project. Released as CC0-1.0. |
| Narration voices | made at run time and not committed | Kokoro-82M (hexgrad, **Apache-2.0** weights and code), voices `am_michael` and `bm_george`, CPU inference | Generated speech can be used commercially under Apache-2.0. Disclose the use of a synthetic voice wherever the platform asks for it (see research/R5). |
| Fallback voice | `~/studio/models/piper/en_US-ryan-high.onnx` (Spark) | Piper (rhasspy). Check the voice's MODEL_CARD before using it commercially. ryan-high is trained on a dataset with its own terms. | Fallback only. Not used by default. |
| Word alignment | | faster-whisper `base.en` (MIT, OpenAI Whisper weights MIT) | Used only for timing, not for content. |

Rebuild everything with `python -m pipeline.audio.synth` (the output is deterministic because the seeds are fixed).

## Adding third-party audio later

Use only CC0 or similarly unrestricted sources, such as freesound.org filtered to CC0, Pixabay audio under the Pixabay Content License, or the YouTube Audio Library under "no attribution required". For each file, add a row here with the exact URL, author, licence, licence URL and download date, and keep the file in `studio/public/sfx/ext/` or `studio/public/music/ext/`. Do not use CC-BY-NC or "free for personal use" files, and do not rip audio from any video.
