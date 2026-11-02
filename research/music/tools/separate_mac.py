"""Demucs 4-stem separation on the Mac (MPS when available, else CPU), for study only (never reused in a mix).

Same output layout as separate.py (the Spark/CPU version): out_dir/{vocals,drums,bass,other,music}.flac at 44.1 kHz
stereo, music = drums + bass + other. Default model htdemucs_ft (fine-tuned bag: cleaner vocals, less voice bleed into
the music stem, which matters for the voice-over-music gap); DEMUCS_MODEL=htdemucs for the faster single model.

usage (Mac, sound venv outside the repo):
  ~/faceless-work/venvs/sound/bin/python -I research/music/tools/separate_mac.py in.webm out_dir [in2 out_dir2 ...]
"""
import os
import subprocess
import sys
import time

import numpy as np
import soundfile as sf
import torch
from demucs.apply import apply_model
from demucs.pretrained import get_model

SR = 44100


def main(argv):
    pairs = list(zip(argv[0::2], argv[1::2]))
    dev = "mps" if torch.backends.mps.is_available() and os.environ.get("DEMUCS_DEVICE", "mps") == "mps" else "cpu"
    torch.set_num_threads(int(os.environ.get("OMP_NUM_THREADS", "6")))
    model = get_model(os.environ.get("DEMUCS_MODEL", "htdemucs_ft"))
    assert model.samplerate == SR
    for src, out in pairs:
        if os.path.exists(os.path.join(out, "music.flac")):
            print("skip", out)
            continue
        os.makedirs(out, exist_ok=True)
        raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", src, "-vn", "-f", "f32le", "-ac", "2", "-ar", str(SR),
                              "-"], check=True, capture_output=True).stdout
        x = np.frombuffer(raw, np.float32).reshape(-1, 2).T.copy()
        sf.write(os.path.join(out, "mix.flac"), x.T, SR)
        wav = torch.from_numpy(x)
        ref = wav.mean(0)
        wav = (wav - ref.mean()) / (ref.std() + 1e-8)
        t0 = time.time()
        with torch.no_grad():
            stems = apply_model(model, wav[None], device=dev, shifts=1, split=True, overlap=0.25, progress=False)[0]
        stems = (stems * (ref.std() + 1e-8) + ref.mean()).cpu()
        res = {}
        for name, s in zip(model.sources, stems):
            res[name] = s.numpy().T
            sf.write(os.path.join(out, f"{name}.flac"), res[name], SR)
        sf.write(os.path.join(out, "music.flac"), res["drums"] + res["bass"] + res["other"], SR)
        print(f"done {src}: {x.shape[1] / SR:.1f}s audio in {time.time() - t0:.0f}s on {dev}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
