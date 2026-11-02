"""Demucs (htdemucs, CPU) 4-stem separation of a reference video's audio, for study only (never reused).

usage (Spark, music venv):  CUDA_VISIBLE_DEVICES="" OMP_NUM_THREADS=8 nice -n 10 \
    ~/studio/venvs/music/bin/python research/music/tools/separate.py in.mp4 out_dir
Writes out_dir/{vocals,drums,bass,other,music}.flac at 44.1 kHz stereo (music = drums+bass+other).
Audio I/O is ffmpeg + soundfile (no torchaudio backends).
"""
import os
import subprocess
import sys
import time

os.environ["CUDA_VISIBLE_DEVICES"] = ""
import numpy as np
import soundfile as sf
import torch
from demucs.apply import apply_model
from demucs.pretrained import get_model

torch.set_num_threads(int(os.environ.get("OMP_NUM_THREADS", "8")))
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
SR = 44100
raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", src, "-vn", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                     check=True, capture_output=True).stdout
x = np.frombuffer(raw, np.float32).reshape(-1, 2).T.copy()
model = get_model("htdemucs")
assert model.samplerate == SR
wav = torch.from_numpy(x)
ref = wav.mean(0)
wav = (wav - ref.mean()) / (ref.std() + 1e-8)
t0 = time.time()
with torch.no_grad():
    stems = apply_model(model, wav[None], device="cpu", shifts=1, split=True, overlap=0.25, progress=False)[0]
stems = stems * (ref.std() + 1e-8) + ref.mean()
res = {}
for name, s in zip(model.sources, stems):
    res[name] = s.numpy().T
    sf.write(os.path.join(out, f"{name}.flac"), res[name], SR)
sf.write(os.path.join(out, "music.flac"), res["drums"] + res["bass"] + res["other"], SR)
print(f"done {src}: {x.shape[1] / SR:.1f}s audio in {time.time() - t0:.0f}s")
