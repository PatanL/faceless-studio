"""B1 TTS smoke test: Kokoro-82M on CPU -> WAV + word timings (Kokoro tokens and faster-whisper).

usage (on the Spark):  CUDA_VISIBLE_DEVICES="" ~/studio/.venv/bin/python pipeline/tts_sample.py OUT_DIR
"""
import json, os, sys, time
os.environ["CUDA_VISIBLE_DEVICES"] = ""
import numpy as np, soundfile as sf, torch
torch.set_num_threads(int(os.environ.get("TTS_THREADS", "6")))
from kokoro import KPipeline

OUT = sys.argv[1] if len(sys.argv) > 1 else "out/voices"
os.makedirs(OUT, exist_ok=True)

EXPLAINER = (
    "Two thousand meters below you, there is no sunlight at all. The water is close to freezing, "
    "and the pressure would crush a submarine like a soda can. But something down here is watching. "
    "Its eyes are as wide as dinner plates, and it can see the faint glow of a sperm whale coming from "
    "a hundred meters away. Now imagine you are the thing it is looking at."
)
HORROR = (
    "At two in the morning, my neighbor texted the building group chat. Do not open your door tonight, "
    "no matter who knocks. I laughed and put my phone down. Then someone knocked. Three slow knocks. "
    "I checked the chat again. My neighbor had sent one more message. It said, that is not me. "
    "And the knocking started again, louder this time."
)
VOICES = [
    ("am_michael", EXPLAINER, "explainer"),
    ("af_heart", EXPLAINER, "explainer"),
    ("bm_george", HORROR, "horror"),
]

pipe = KPipeline(lang_code="a", device="cpu")   # American English G2P; British voices still work
pipe_b = KPipeline(lang_code="b", device="cpu")
report = []
if os.environ.get("WHISPER_ONLY"):
    report = json.load(open(f"{OUT}/report.json"))["samples"]
for voice, text, niche in ([] if os.environ.get("WHISPER_ONLY") else VOICES):
    p = pipe_b if voice.startswith("b") else pipe
    t0 = time.time()
    chunks, words, offset = [], [], 0.0
    for r in p(text, voice=voice, speed=1.0):
        audio = r.audio.numpy() if hasattr(r.audio, "numpy") else np.asarray(r.audio)
        for tok in (r.tokens or []):
            if tok.start_ts is not None and tok.end_ts is not None and tok.text.strip():
                words.append({"w": tok.text, "s": round(offset + tok.start_ts, 3), "e": round(offset + tok.end_ts, 3)})
        chunks.append(audio)
        offset += len(audio) / 24000
    wav = np.concatenate(chunks)
    synth = time.time() - t0
    base = f"{OUT}/{niche}_{voice}"
    sf.write(base + ".wav", wav, 24000)
    json.dump({"voice": voice, "text": text, "duration_s": round(len(wav) / 24000, 2), "words": words},
              open(base + ".kokoro_words.json", "w"), indent=1)
    report.append({"voice": voice, "niche": niche, "duration_s": round(len(wav) / 24000, 2),
                   "synth_s": round(synth, 2), "rtf": round(synth / (len(wav) / 24000), 3),
                   "kokoro_word_count": len(words)})
    print(report[-1], flush=True)

json.dump({"samples": report}, open(f"{OUT}/report.json", "w"), indent=1)

def load16k(path):
    """Decode via soundfile + linear resample to 16 kHz (avoids PyAV API drift)."""
    a, sr = sf.read(path, dtype="float32")
    if a.ndim > 1: a = a.mean(axis=1)
    n = int(len(a) * 16000 / sr)
    return np.interp(np.linspace(0, len(a) - 1, n), np.arange(len(a)), a).astype(np.float32)

# faster-whisper word alignment check (CPU, int8)
from faster_whisper import WhisperModel
t0 = time.time()
wm = WhisperModel("base.en", device="cpu", compute_type="int8", cpu_threads=6)
load = time.time() - t0
for r in report:
    base = f"{OUT}/{r['niche']}_{r['voice']}"
    t0 = time.time()
    audio16 = load16k(base + ".wav")
    segs, _ = wm.transcribe(audio16, word_timestamps=True, beam_size=1)
    ws = [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)} for s in segs for w in s.words]
    r["whisper_s"] = round(time.time() - t0, 2)
    r["whisper_word_count"] = len(ws)
    json.dump({"model": "faster-whisper base.en int8", "words": ws}, open(base + ".whisper_words.json", "w"), indent=1)
    print(r, flush=True)
json.dump({"whisper_load_s": round(load, 2), "samples": report}, open(f"{OUT}/report.json", "w"), indent=1)
