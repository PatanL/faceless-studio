"""Per-niche voice and mix settings. Voices were picked from B1's samples (out/voices/)."""

NICHES = {
    "explainer": {
        # calm US documentary male; slightly slower than default for gravitas
        "engine": "kokoro", "voice": "am_michael", "lang": "a", "speed": 0.96,
        # Shorts pace: chunks are tail-trimmed to <=0.12 s, so ~0.4 s between paragraphs (no dead air)
        "paragraph_pause": 0.28,
        "trim_tail": True,
        "voice_chain": "highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=1,"
                       "equalizer=f=3200:t=q:w=1.2:g=1.5",
        "music": "deep_ocean",
        "music_db": -5.0,    # bed loudness relative to the voice, between lines (-15 left deep_ocean ~28 dB under)
        "duck_db": -9.0,     # extra attenuation while the voice talks
        "sfx_duck_db": -4.0, # lighter duck while an SFX plays (outside speech)
        "attack": 0.10, "release": 0.55, "lookahead": 0.08,
        "music_fade_in": 1.0, "music_fade_out": 2.0,
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
        "music_db": -12.0,
        "duck_db": -7.0,
        "sfx_duck_db": -5.0,
        "attack": 0.12, "release": 0.8, "lookahead": 0.10,
        "music_fade_in": 1.5, "music_fade_out": 2.5,
        "auto_sfx": {
            r"\bknock(s|ed|ing)?\b": "knock3", r"\bbuzz(ed|es|ing)?\b|\bvibrat": "phone_buzz",
            r"\bheart(beat)?\b": "heartbeat_slow", r"\bcreak": "door_creak", r"\bding\b": "ding",
            r"\bfootsteps?\b": "footsteps", r"\btext(ed)?\b|\bmessage\b": "notify",
        },
        # auto cues fire on the spoken word, i.e. inside speech: keep them under the key words
        "auto_sfx_db": {"knock3": -6.0},
        "trim_tail": True,
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
