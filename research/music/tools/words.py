"""Word timings of a reference narration (Demucs vocals stem) with faster-whisper, CPU, 4 threads.

usage (Spark, ~/studio/.venv): CUDA_VISIBLE_DEVICES="" nice -n 10 python research/music/tools/words.py vocals.flac words.json
"""
import json
import os
import sys

os.environ["CUDA_VISIBLE_DEVICES"] = ""
import soundfile as sf
from faster_whisper import WhisperModel
from scipy.signal import resample_poly

m = WhisperModel(os.environ.get("WHISPER_MODEL", "small.en"), device="cpu", compute_type="int8", cpu_threads=4)
x, sr = sf.read(sys.argv[1], dtype="float32", always_2d=True)
x = resample_poly(x.mean(1), 16000, sr).astype("float32")  # decoded here (PyAV API mismatch in this venv)
segs, _ = m.transcribe(x, word_timestamps=True, vad_filter=False, beam_size=5, condition_on_previous_text=False)
words = [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)} for s in segs for w in (s.words or [])]
json.dump({"words": words}, open(sys.argv[2], "w"), indent=0)
print(len(words), "words")
