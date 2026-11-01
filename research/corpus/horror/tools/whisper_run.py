"""CPU whisper: python -I whisper_run.py out_dir model a.wav b.wav ...  -> out_dir/<id>.json (segments) """
import sys, json, os, time
from faster_whisper import WhisperModel
out, model = sys.argv[1], sys.argv[2]
m = WhisperModel(model, device="cpu", compute_type="int8", cpu_threads=4)
for p in sys.argv[3:]:
    i = os.path.basename(p)[:-4]
    dst = os.path.join(out, i + ".json")
    if os.path.exists(dst): continue
    t0 = time.time()
    segs, info = m.transcribe(p, vad_filter=True, language="en", beam_size=1, condition_on_previous_text=False)
    rows = [{"s": round(s.start, 2), "e": round(s.end, 2), "t": s.text.strip()} for s in segs]
    json.dump({"id": i, "lang": info.language, "dur": info.duration, "speech": info.duration_after_vad, "segments": rows}, open(dst, "w"), ensure_ascii=False, indent=0)
    print(i, len(rows), round(time.time() - t0), "s", flush=True)
