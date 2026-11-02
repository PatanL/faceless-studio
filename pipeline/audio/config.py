"""Per-niche voice and mix settings. Voices were picked from B1's samples (out/voices/)."""

# Music beds a video may use: only the in-house beds that pipeline/audio/synth.py generates (CC0, LICENSES.md), so
# nothing can draw a Content ID claim on a Short over 60 s. mix.find_asset("music", ...) refuses anything else and the
# QA gate FAILs a mix whose report.json names another bed. Keep in sync with synth.BEDS.
# "score" is the per-episode soundtrack composed in code by pipeline/audio/score.py (every note generated here, rendered
# from a licence-cleared SoundFont listed in SOUNDFONTS below); the gate also checks its provenance in report.json.
SCORE = "score"
MUSIC_BEDS = ("deep_ocean", "documentary_pulse", "dread", "tension_pulse", SCORE)

# SoundFonts the score may render with, pinned by sha256 (licence text and source in pipeline/audio/LICENSES.md).
# sf2.soundfont() refuses any other file, so a swapped or unvetted bank can never reach a mix.
SOUNDFONTS = {
    "GeneralUser-GS": {
        "file": "GeneralUser-GS/GeneralUser-GS.sf2",
        "sha256": "9575028c7a1f589f5770fccc8cff2734566af40cd26ed836944e9a5152688cfe",
        "licence": "GeneralUser GS License v2.0 (v2.0.3): use without restriction for music creation, private or "
                   "commercial, including profit from recordings made with it",
        "source": "https://github.com/mrbumpy409/GeneralUser-GS @684543d5 (S. Christian Collins)",
    },
}

NICHES = {
    "explainer": {
        # calm US documentary male. Owner's blind test (2026-11-01, out/voices/lab/matched-male #7): am_michael read one
        # sentence at a time at speed 1.1 with no EQ/compressor chain sounded least robotic. Paragraph-at-once synthesis
        # plus the chain was the robotic part, not the voice.
        "engine": "kokoro", "voice": "am_michael", "lang": "a", "speed": 1.1,
        "sentence_mode": True, "sentence_gap": 0.26,  # gap between sentences, divided by speed
        # Shorts pace: chunks are tail-trimmed to <=0.12 s, so ~0.27 s between paragraphs (no dead air)
        "paragraph_pause": 0.15,
        "trim_tail": True,
        "lead_in": 0.1, "trim_head": 0.03,  # first word by ~0.15 s (frame 0 is the cover; no dead air)
        "trim_head_every": 0.05,  # Kokoro's ~0.2-0.3 s lead silence on every later chunk too (paragraph gaps ~0.3 s)
        # no EQ/compressor chain: it cost ~0.1 UTMOS and the owner preferred the clean read (lab INDEX.md)
        "voice_chain": "",
        # the scored soundtrack composed from the storyboard (pipeline/audio/score.py, research/music/KURZ_MUSIC.md);
        # before a storyboard exists (first TTS pass) or without FluidSynth/the SoundFont it falls back to deep_ocean
        "music": "score",
        "score_fallback": "deep_ocean",
        # score levels (override the bed-tuned music_db/duck_db, also those in a script's front matter; a script may set
        # score_music_db / score_duck_db): voice ~11 LU over the music while it talks (Kurz: 10-11 median)
        # duck_band: while the voice talks the score's 1-4 kHz (consonants, intelligibility) dips a further 6 dB
        "score_mix": {"music_db": -7.0, "duck_db": -3.5, "duck_band": {"lo": 1000, "hi": 4000, "db": -6.0},
                      "true_peak_db": -2.0},
        # bed loudness (LUFS) relative to the voice, between lines. Orca review: -15 / -9 duck put the bed ~24 LU
        # (~26 dB RMS) under the talking voice, inaudible on a phone. -13.5 / -5 = ~18.5 LU, ~20 dB RMS under the voice
        # while it talks (report.json mix.bed_below_voice_db), and it swells back up in the gaps.
        "music_db": -13.5,
        "duck_db": -5.0,     # gentle duck while the voice talks (was -9)
        # whoosh/swell on every scene cut (pipeline.audio.make.cut_cues); cuts with a marker cue keep only that cue
        "cut_sfx": {"cues": ["whoosh", "bubbles", "whoosh", "whoosh_long"], "lead": 0.3, "db": -5.0},
        "sfx_duck_db": -4.0, # lighter duck while an SFX plays (outside speech)
        "attack": 0.10, "release": 0.55, "lookahead": 0.08,
        "music_fade_in": 1.0, "music_fade_out": 2.0,
        # script front matter `ending: loop` (Shorts whose last line feeds frame 0): the mix ends `loop_tail` s after the
        # last voiced sample (not the padded TTS tail or SFX tails) and the bed plays through the seam (no 2 s fade to
        # silence, orca review: 1.4 s of dead air at the replay seam)
        "loop_ending": {"loop_tail": 0.3, "music_fade_out": 0.05, "music_fade_in": 0.15, "end_fade": 0.05},
        "auto_sfx": {
            r"\bsonar\b": "sonar_ping", r"\bbubbl": "bubbles", r"\bcrush(ed|es|ing)?\b": "impact",
            r"\bboom\b|\bexplod": "boom", r"\bsuddenly\b": "whoosh",
        },
    },
    "horror": {
        # tense first-person narrator (UK male, B1 horror sample), a touch faster for unease
        "engine": "kokoro", "voice": "bm_george", "lang": "b", "speed": 1.02,
        "paragraph_pause": 0.15,  # chunks are tail-trimmed to <=0.12 s, so ~0.27 s between paragraphs
        # close-mic'd and slightly roomy
        "voice_chain": "highpass=f=80,acompressor=threshold=-22dB:ratio=3:attack=5:release=100:makeup=1,"
                       "equalizer=f=250:t=q:w=1:g=1.5,aecho=0.9:0.9:23|41:0.10|0.06",
        "music": "dread",
        "music_db": -7.5,    # was -12: the bed sat ~38 dB under the voice and vanished in the knock silences
        "lead_in": 0.1, "trim_head": 0.03,  # voice starts by ~0.15 s (frame 0 is the cover; no dead air)
        "duck_db": -7.0,
        "sfx_duck_db": -5.0,
        "attack": 0.12, "release": 0.8, "lookahead": 0.10,
        "music_fade_in": 0.3, "music_fade_out": 2.5,
        "auto_sfx": {
            r"\bknock(s|ed|ing)?\b": "knock3", r"\bbuzz(ed|es|ing)?\b|\bvibrat": "phone_buzz",
            r"\bheart(beat)?\b": "heartbeat_slow", r"\bcreak": "door_creak", r"\bding\b": "ding",
            r"\bfootsteps?\b": "footsteps", r"\btext(ed)?\b|\bmessage\b": "notify",
        },
        # auto cues fire on the spoken word, i.e. inside speech: keep them under the key words
        "auto_sfx_db": {"knock3": -6.0},
        "trim_tail": True,
        # the scare must be the loudest event: featured hits are levelled by their loudest 400 ms (momentary LUFS)
        # relative to the voice (voice ~ -14 LUFS in the final mix -> knocks ~ -11, end stinger ~ -12)
        "sfx_momentary": {"knock3_slow": 5.5, "stinger": 3.0},
        "sfx_squash": {"knock3_slow": 6.0, "stinger": 3.0},  # transient pre-limit (crest 13 -> 9.5 dB on the knocks)
        # music bed drops to near silence this long before a featured hit (a held breath), then recovers
        "hush": {"knock3_slow": 0.6},
        "hush_db": -32.0,
    },
}

# Default level of each SFX relative to the voice loudness (dB). Unknown cues use -6.
SFX_DB = {
    "knock": -3, "knock3": -3, "knock3_slow": -3, "phone_buzz": -7, "phone_buzz_long": -7,
    "notify": -10, "message_send": -12, "message_pop": -12, "pop": -12, "click": -14, "typing": -14,
    "heartbeat": -4, "heartbeat_slow": -4, "heartbeat_fast": -4, "whoosh": -10, "whoosh_long": -10,
    "riser": -9, "impact": -4, "boom": -4, "stinger": -5, "ding": -10, "door_creak": -8,
    "static": -12, "glitch": -10, "tick": -14, "clock_ticking": -12, "sonar_ping": -10,
    "bubbles": -12, "underwater_rumble": -8, "footsteps": -8, "breath": -10, "drone": -10,
}

TARGET_LUFS = -14.0
TRUE_PEAK_DB = -1.0     # ceiling for the final mix (dBTP)
SR = 48000
