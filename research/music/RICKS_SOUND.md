# RicksClips3000 story Shorts: how they sound, measured, and how ours compare

Goal 1 asks for parity with RicksClips3000 (docs/PARITY.md) on voice, music and sound effects (FEEDBACK principle 6:
"natural sound"). This note sets the rules with measured ranges and shows where our story audio sits on each one. It
also describes the `story_ricks` audio profile built to close the gaps, and the A/B that tests it.

All numbers are in `research/references/data/ricks24_audio.json`: per reference, the groups, our episodes and the A/B
sides. The A/B against the reference ranges is in `out/rnd-sound/ab_numbers.json`.

## 1. Sample and method

**n = 8, not 24.** The 24 files in `~/studio/refs/lanes/ricks/vid/` are video-only downloads. Only the 8 PARITY
references have an audio track (`~/studio/refs/ig/ricks720_*.webm`). Nothing new was downloaded. The "top vs rest" split
uses the views ranks across all 24 Shorts:

- **Top (5):** VS1Z (rank 1), 0m6G (2), GM9U (5), Mz72 (6) and 7xS8 (7).
- **Rest (3):** 5WMQ (17), ZDy3 (19) and jpFJ (20).

With 5 against 3, treat every group difference below as a lead to test, not a finding. Measuring the 16 Shorts without
audio would need a new download, which the coordinator has to approve first.

**Where the work ran.** Everything ran on the Mac. The Spark was used only to copy files (its hottest zone read
72–79 °C, below the 80 °C limit). The reference audio, stems and words stay outside the repo in
`~/faceless-work/ricks-sound/`.

**Separation.** Demucs 4.1.0 `htdemucs_ft` (MIT) on MPS, installed in the venv `~/faceless-work/venvs/sound`, not
system-wide. Its weights come from the author's HF repository `adefossez/HTDemucs-ft` as safetensors. The tool is
`tools/separate_mac.py`. FluidSynth 2.6.2 for the A/B renders comes from a conda-forge environment in
`~/faceless-work/envs/fluidsynth`. The SoundFont was copied from the Spark and its sha256 matches `config.SOUNDFONTS`.

**Measurement tools.**

- `tools/story_sound.py` (new) measures loudness, the voice-over-music gap, the music bed, SFX events, room tone and
  the voice.
- `tools/analyze.py` (existing) measures music sections, tempo, swells, hits and drop-outs.
- `tools/motion_spikes.py` (new) finds on-screen motion onsets.
- `tools/palette.py` (existing) matches the reference timbres to our SoundFont presets.
- `tools/story_sound_summary.py` (new) collects the results into the JSON.

**Like for like.** Our mixes went through the same Demucs and the same detectors as the references. Our own true stems
are also measured, so each tool's bias shows: Demucs reads our voice-over-music gap about 1.4–2.5 LU *larger* than the
true stems do.

**SFX detector.** It finds events in the Demucs drums stem that rise out of their own rolling median spectrum. I checked
it against Turk's 14 known cues:

- On our true SFX stem it finds all 7 whooshes, the impact and the stinger. It misses ticks, clicks and the slow door
  creak.
- On our Demucs drums stem it finds only about half.

So the reference counts are lower bounds. The references' SFX are crisp, broadband transients that Demucs puts in the
drums stem, which suits the detector. Ours are soft swells and narrow ticks, which it mostly misses.

## 2. The rules (reference median, range over the 8) and where ours stand

In the tables, "ours" is the Demucs-measured Turk v4 / v6 / v7 (current) and Vasa v1. Our true stems are in brackets.

### Loudness

| Rule | Refs | Turk v4 / v6 / v7 | Vasa v1 |
|---|---|---|---|
| Integrated loudness | **−14.0 LUFS** (−15.0 to −14.0) | −14.2 / −14.0 / −14.1 | −14.0 |
| True peak | **−2.0 dBTP** (−2.9 to −1.6) | −2.1 / −2.2 / −2.3 | −2.1 |
| LRA | **2.4 LU** (1.7 to 3.2) | 1.9 / 1.6 / 1.6 | 1.5 (low) |

Loudness is already at parity. Our LRA sits at or under the bottom of the range because the bed is flat and the voice is
continuous.

### Voice over music

| Rule | Refs | Turk v4 / v6 / v7 | Vasa v1 |
|---|---|---|---|
| Voice minus music bed, momentary, under speech: p50 | **20.7 LU** (19.5 to 22.4) | 19.5 / 19.5 / 19.8 (true 18.4) | 20.3 (true 18.8) |
| Same, p10 | **14.9** (11.9 to 16.9) | 13.4 / 11.7 / 11.6 | 10.7 (too close) |
| Same, p90 | **26.0** (24.0 to 27.9) | 24.6 / 24.9 / 24.9 | 25.6 |
| Voice minus all non-voice (music + SFX), integrated | **19.4 LU** (14.7 to 21.0) | 18.9 / 17.1 / 16.8 | 16.9 |

- The music sits about **20–21 LU** under the talking voice, roughly 3 LU further down than docs/PARITY.md's working
  figure of "~17 LU".
- Our median gap is close, but our loud moments (p10) come 3–4 LU nearer the voice than theirs.
- Our non-voice layer as a whole is 2.5 LU too hot, and the SFX are what push it up (see SFX below).

### Music presence over time

| Rule | Refs | Ours |
|---|---|---|
| Music enters | **at 0.05 s, at full level**, in 8/8 | same (0.05 s) |
| Music plays throughout | **100 %** of the runtime, no digital silence | same |
| Drop-outs | **0** (0 to 2; a 0.3 s dip in 2 refs) | Turk 1 (the stinger hush), Vasa 4 |
| Bed range, short-term p10→p95 | **7.4 dB** (5.3 to 12.8) | 7.2 / 9.0 / 9.1, Vasa 10.8 (true 5.5–6.5) |
| Music section boundaries vs visual changes | chance in 6/8; above chance in 2/8 (7xS8 p = 0.013, Mz72 p = 0.039) | score cues follow the settings |
| Music at the "You see" turn | no drop-out in 7/7; level step −5.6 to +5.0 dB, centred near 0 | no "You see" handling (fine) |
| Same track shared across Shorts | **no**: pairwise chroma r ≤ 0.48, against ≥ 0.8 for a shared track | each score is unique (fine) |

The music is a continuous library-style track that runs on its own clock. It has 4–6 sections of about 11 s and no
stings. It does not mark the cuts or the "You see" reveal. Our score does more than that (stings, a drop-out, cue
changes at settings), and none of it is needed for this lane.

### Music style (ear-equivalent spectral cues)

| Cue | Refs | Turk v7 (current score) | Vasa v1 |
|---|---|---|---|
| Tempo | **~113 BPM** (96 to 152; 103 top vs 118 rest) | 112–118 | 99 |
| Pulse clarity | **0.18** (0.11 to 0.27): soft, no kit | 0.10 | 0.12 |
| Drums stem re music | **−33 dB** (−36 to −22): no drum kit | −34 | −33 |
| Bass stem re music | **−8.5 dB** (−38 to −6.6; 6 of 8 between −10 and −6.6) | −8.6 | −27 |
| "Other" stem re music | **−1.3 dB**: plucked and keyed melody carries the track | — | — |
| Minor share of sections | **0.81** (D minor in 4/8; also E min, A min/maj, D maj) | 0.75 | 0.25 |
| Spectral centroid | **1415 Hz** (1071 to 1790): bright | **939 (dark)** | 1046 |
| Note onsets per second | **1.8** (1.3 to 2.0) | 1.4 | 0.9 |
| Section length | **10.9 s** (8.0 to 15.7) | 12.5 | 14.4 |
| Band balance, dBA re total | 2.5–6 kHz **−9**, 6–11 kHz **−19** | −5 / −32 | −9 / −30 |

Timbre (palette.py, 682 isolated note events from the 8 "other" stems) falls into three clusters, all closest to
**pizzicato + harp, nylon guitar or music box**, **harp in a room**, and **piano or celesta**. The pads rank halopad,
then synthstrings.

Read by ear-equivalents, the reference music is a light, plucky, slightly mischievous storybook cue: pizzicato strings,
harp and piano/celesta, a plucked bass, no drums, mostly minor, about one note per beat. Ours is darker and slower
(warm pads, a low-passed top, sparse notes).

### Sound effects

| Rule | Refs | Turk v7 | Vasa v1 |
|---|---|---|---|
| Detected SFX per minute (Demucs, lower bound) | **11.6** (2.8 to 32.5); top 12.1, rest 11.0 | 8.1 (placed: 14.3) | 8.1 (placed: ~20) |
| Kinds per minute | whoosh **5.1** (0 to 14.9), pop/click **4.3** (1.9 to 6.5), impact **0.9** (0 to 10.3), foley **0.9**, tonal 0.5, riser 0, ambience 0 | whoosh 5–7, pop 1–2, tonal stingers 2, door creak and clock (long, ambience-like) | impacts 9, foley 3, whoosh 4, tonal 3 |
| Duration | whoosh **0.13 s** (p90 0.31), impact 0.09, pop 0.06 | whoosh **0.7–1.2 s** | similar |
| Level vs the voice (peak 100 ms re voice momentary median) | whoosh **−15.5 LU** (−17.2 to −12.9), impact **−16.8** (−22 to −11.9), pop **−21** (−26 to −14.5) | whoosh −7.3, stinger and impact **+0.3 to +1.5**, pops −16 (true stems) | whoosh −7.3, impacts −5.6, foley −4.4, stingers +1.5 |
| Sync to scene transitions / cuts (±0.3 s) | **chance** in 8/8 (share 0.17, null 0.19) | cut whoosh 0.3 s before each paragraph | same |
| Sync to on-screen motion onsets (±0.2 s) | top 5: share 0.24, null 0.12; VS1Z p = 0.035, 0m6G p = 0.05; rest: chance | chance | 0.32 vs 0.16 (p = 0.055) |
| SFX inside speech | **100 %**: under the narration, never in pauses | same | same |

- RicksClips SFX are frequent, tiny and quiet: short swishes and pops 15–21 LU under the voice. They land on on-screen
  motion (a thing appearing or moving) more than on the cuts.
- **Ours are 7–9 LU too loud** (stingers 15+ LU too loud) and 5–10 times too long.
- Ours lean on long ambience-like cues (door creak 3.0 s, clock 3.3 s) that the references never use.

### Room tone and silence

| Rule | Refs | Ours |
|---|---|---|
| Speech gaps ≥ 120 ms | **1.0 per minute** (0 to 6), median 0.14 s | **25–37 per minute**, 0.24–0.32 s each |
| Vocals stem in gaps re speech | **−42 dB** (−45 to −34): clean, gated or edited | −39 (true −40): fine |
| Mix in gaps re speech | **−21 dB** (the music fills it) | −18: fine |
| Breaths | **0 per minute** in 8/8 | 0: fine |

There is no audible room tone or noise floor, and the narration runs on with almost no pauses. Our sentence gaps are the
largest rhythm difference between the two.

### The voice

| Rule | Refs | Ours (Turk v7, Vasa v1) |
|---|---|---|
| f0 median | **194 Hz** (174 to 205), p5–p95 about 110–330 Hz | **115 Hz** (`am_michael`) |
| f0 range p5–p95 | **16.3 st** (14.8 to 16.9) | 14.1 / 17.1 (true 9.7) |
| Phrase-level pitch movement (1 s medians, p10–p90) | **8.8 st** (7.6 to 10.3) | **5.8 / 4.7** |
| Pace, words per second | **3.8** (3.4 to 3.97) | 3.81 / 4.01 |
| Pace variation, 3 s CV | **0.15** (0.12 to 0.18) | 0.10 / 0.14 |
| Loudness spread, momentary p10–p90 | **5.6 LU** (5.2 to 6.5) | 7.3 / 7.6 (true 8.4): under-compressed |
| Crest factor, p50 | **12.2 dB** (11.4 to 12.5) | 14.5 / 14.3 (true 14.8–15.1): under-compressed |
| Brightness (4–8 kHz minus 300 Hz–1 kHz) | **−8.5 dB** (−10 to −7.2) | −9.0 / −8.1 |
| Presence (1–4 kHz minus 300 Hz–1 kHz) | **−7.0 dB** (−7.1 to −6.8) | −7.1 / −7.0 |
| Air, 8–16 kHz re total | **−14.3 dB** (−15.4 to −12.5) | **−25** (Kokoro renders at 24 kHz, so nothing above 12 kHz) |
| Under 100 Hz re total | **−22.6 dB** (−27.6 to −18.7) | −11 (our f0 sits near 100 Hz) |

The references' voice is a higher, animated read with about twice our phrase-level pitch movement. It is compressed to a
tight ~12 dB crest, bright, with full air, and has no breaths or pauses. Pace and presence already match. The rest is
processing, except pitch and intonation, which come from casting.

### Top by views vs the rest (n = 5 vs 3, leads only)

Same in both groups:

- loudness;
- the voice-over-music gap (20.8 vs 20.6 LU);
- the voice (f0, crest, pace);
- the SFX count (12.1 vs 11.0 per minute).

Different, tentatively:

- **The top group's SFX come more regularly** (median interval 1.8 vs 5.2 s), with more whooshes (7.1 vs 4.4 per minute).
- **The top group's SFX land on motion more often** (0.24 vs 0.08; null 0.12–0.14).
- **The top group's music is busier and moves more:** 1.9 vs 1.5 onsets per second; bed range 8.4 vs 6.1 dB; 8 vs 5
  level steps.
- **The top group's music is more often minor and slower** (0.83 vs 0.5; 103 vs 118 BPM).

## 3. Gaps in ours, by size

1. **SFX too loud and too long.** Whooshes sit 7–9 LU over the references and stingers about 15 LU over. Ours last 0.7–1.2 s against their 0.1–0.3 s. There are too few pops, and the long ambience cues have no counterpart.
2. **Music is the wrong colour.** Ours is dark and pad-led (centroid 940 Hz, 2.5–6 kHz at −33 dB in the true stem); theirs is bright and plucky (1415 Hz). Our score also has stings, drop-outs and cues tied to the settings, which the references don't.
3. **Sentence pauses.** We have 25–37 gaps per minute against their 1 per minute.
4. **Voice under-compressed and missing its air.** Crest is 14.5–15 against 12.2, momentary spread 7.3–8.4 against 5.6, and the 8–16 kHz band sits 11 dB low.
5. **Voice casting.** f0 is 115 Hz against 194 Hz, with half the intonation movement. Processing can't fix this without sounding artificial.
6. Smaller ones: the non-voice layer is 2.5 LU hot, the music's loud moments (p10) come too near the voice, and LRA is
   low.

## 4. The `story_ricks` profile (pipeline/audio)

An episode opts in with `audio_profile: story_ricks` in its script front matter, or with
`python -m pipeline.audio.make ... --profile story_ricks`. Without that line, nothing changes:

- The explainer and horror niches and their defaults are untouched.
- The Turk A side re-rendered on the Mac after the change is bit-identical to the Spark's mix.wav (max difference
  1e-6).

The profile is `config.PROFILES["story_ricks"]`.

**Music.** `score.compose_story` composes a new arrangement of our own scored music. Every note is generated in code, the
instruments are presets from the cleared GeneralUser GS bank, and provenance keeps
`generator: pipeline.audio.score`, so the gate's music check still applies.

- The key, tempo (100–116 BPM), mode (80 % minor) and melody are seeded per episode, so each Short gets its own track.
- Pizzicato and harp carry the melody at about one note per beat, with a celesta octave double, a harp arpeggio and a
  quiet halo pad in some sections, and a plucked finger bass. There is no drum kit.
- The top is bright (no low-pass).
- The 4-bar sections (A A2 B A3 C …) add or drop a layer for 2–4 dB level steps, with one pad swell.
- There are no stings and no drop-outs.
- The music plays from frame 0 and, with `ending: loop`, wraps its tail onto the start.
- Mix: `music_db −13`, `duck −2.5`, a light 1.5–5 kHz band duck of −2 dB.

**Voice.** `voicefx.process` runs at mix time:

- high-pass at 90 Hz (24 dB/oct);
- −2.5 dB at 2.5 kHz and −3 dB at 5.5 kHz;
- 4:1 parallel compression (35 % wet);
- a limiter at −7.5 dB re −20 LUFS;
- an exciter that adds harmonics above 8 kHz.

At TTS time, `voicefx.tighten` cuts silent runs to 0.10 s before the timings are cached, so captions and the storyboard
follow. `sentence_gap 0.04` and `paragraph_pause 0`.

**SFX.**

- Storyboard action cues (pops and ticks on appearances and labels) are on by default (`action_sfx`).
- Whooshes play at rate 2.0–2.6, which makes them shorter and brighter.
- The cut whoosh comes 0.12 s before the line.
- Per-cue levels are pulled down: whoosh −16, impact −20, stinger −18, pop −15, tick and click −16 dB re the voice
  reference.
- The SFX duck is −1 dB.

## 5. Proof: the 20 s A/B on Chess Turk (out/rnd-sound/)

The files:

- `turk_A_current_story_mix_0-20s.wav`: the current story mix (explainer niche, score v2, −12 / −4.5, SFX full).
- `turk_B_story_ricks_0-20s.wav`: the same cached voice and storyboard through `story_ricks`.
- `turk_B_story_ricks_tightened_voice_0-20s.wav`: B with the pause tightening applied to the cached voice.
- `turk_AB_A-then-B_0-20s.m4a`: A, then 1 s of silence, then B, for a phone check.
- `ab_numbers.json`: the numbers.

The clips measure −14.3, −14.1 and −14.1 LUFS, with peaks at −2.1, −2.8 and −3.2 dBFS. Full-length measures follow,
on Demucs stems like the references unless marked.

| Rule | Refs | A (current) | B | B tightened |
|---|---|---|---|---|
| Voice minus bed p50 / p10 / p90 | 20.7 / 14.9 / 26.0 | 19.8 / **11.6** / 24.9 | **21.3 / 15.3 / 26.3** | 21.6 / 17.3 / 25.8 |
| Voice minus non-voice, integrated | 19.4 (14.7 to 21.0) | 16.8 | **21.0** | 21.2 (0.2 over) |
| Music centroid | 1415 (1071 to 1790) | **939** | **1533** | 1620 |
| Music onsets per second | 1.83 (1.28 to 1.98) | 1.41 | **1.82** | 2.2 (over) |
| Pulse clarity | 0.18 (0.11 to 0.27) | **0.10** | **0.26** | 0.17 |
| Bed range | 7.4 (5.3 to 12.8) | 9.1 | **7.2** | 7.1 |
| Music drop-outs | 0 (0 to 2) | 1 | **0** | 1 |
| Section length | 10.9 s (8.0 to 15.7) | 12.5 | **8.8** | 9.3 |
| Whoosh level vs voice (true stems) | −15.5 (−17.2 to −12.9) | **−7.3** | **−14.1** | −14.1 |
| Stinger / impact level (true stems) | −16.8 (−22 to −11.9) | **+0.9** | **−17.5** | −15.7 |
| Voice crest p50 | 12.2 (11.4 to 12.5) | **14.5** | **11.9** | 11.7 |
| Voice momentary spread | 5.6 (5.2 to 6.5) | **7.3** | **6.5** | 4.5 (under) |
| Air 8–16 kHz | −14.3 | **−25** | **−14.2** | −14.2 |
| Brightness | −8.5 (−10 to −7.2) | −9.0 | **−7.5** | −7.6 |
| Speech gaps ≥ 120 ms per minute | 1.0 (0 to 6) | **25.5** | 20.4 (cached voice) | **1.1** |
| Words per second | 3.8 (3.4 to 3.97) | 3.81 | 3.81 | 4.1 (over) |
| True peak / LRA | −2.0 / 2.4 | −2.3 / 1.6 | −3.0 / 1.2 (both low) | −3.4 / 1.1 |

B moves into the reference range on the gap, the music colour, the pulse, note density and drop-outs, the SFX levels, and
the voice crest, spread, air and brightness.

**Still open:**

- **Pace after tightening.** Tightening removes 4.1 s, so words per second rises to 4.1. The production path needs a TTS
  pass with Kokoro speed about 1.20 instead of 1.28. The episode's front matter `speed:` overrides the profile, so the
  script owner sets it. Tightened voices also come out over-compressed (spread 4.5).
- **SFX character.** On the like-for-like Demucs detector, B's SFX barely register (1–3 per minute against the
  references' 11.6). Our library's whooshes and ticks are soft and narrowband, so the levels and density are right but
  the timbre is not. Next step: add short broadband swish and pop sounds to `synth.py`.
- **Bass.** Demucs reads the story bass at −24 dB re the music. Our own stems put it at −6, which suggests the
  references' bass is a different, more bass-like timbre.
- **LRA** is 1.1–1.2 against 1.7–3.2, and **true peak** 0.1–0.5 dB under the range.
- **Voice casting** (f0 and intonation): this is the owner's call. `am_michael` won the explainer blind test. A story-lane
  voice test with higher, more animated voices is the next step for that rule.

Nobody has listened to these yet: every check above is measured. The clips need the owner's ear (phone, A then B).

## 6. Re-running

```bash
# Mac, outside the repo: ~/faceless-work/ricks-sound/{ig,stems,meas,an,vis}
P=~/faceless-work/venvs/sound/bin/python; T=research/music/tools
$P -I $T/separate_mac.py in.webm stems/<id>
$P -I $T/story_sound.py --stems stems/<id> --key <id> --out meas/<id>.json --words words/<id>.json \
   --frames research/references/data/ricks24_metrics.json:<id> --you-see 7.2
$P -I $T/analyze.py --stems stems/<id> --words words/<id>.json --settings-json vis/<id>.json --key <id> --out an
$P -I $T/motion_spikes.py video vis/<id>_motion.json
$P -I $T/story_sound_summary.py ~/faceless-work/ricks-sound research/references/data/ricks24_metrics.json \
   research/references/data/ricks24_audio.json
# a story mix with the profile (FluidSynth: STUDIO_FLUIDSYNTH_LIB / STUDIO_SOUNDFONTS on the Mac)
python -m pipeline.audio.make episodes/<slug>/script.md --id <slug> --profile story_ricks --reuse-tts --out <dir>
```
