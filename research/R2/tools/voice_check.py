"""Detect spoken language + transcribe first 40 s of each wav (CPU only).
CUDA_VISIBLE_DEVICES="" python -I voice_check.py a.wav b.wav ..."""
import sys, wave
import numpy as np
from faster_whisper import WhisperModel
m = WhisperModel("base", device="cpu", compute_type="int8", cpu_threads=8)
for p in sys.argv[1:]:
    w = wave.open(p); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    segs, info = m.transcribe(a, vad_filter=True)
    txt = " ".join(s.text.strip() for s in segs)
    print(f"== {p.split('/')[-1]} lang={info.language} p={info.language_probability:.2f} speech_s={info.duration_after_vad:.1f}/{info.duration:.1f}")
    print("   ", txt[:400])
