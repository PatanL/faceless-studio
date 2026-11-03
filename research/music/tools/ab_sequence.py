"""Join clips into one listening file for the owner: each clip loudness-matched (-16 LUFS), 1.0 s of silence
between clips, 48 kHz mono AAC. Writes a sidecar .txt with the order and each clip's start time.

usage (voicelab venv): python -I ab_sequence.py out.m4a "label 1=path1.wav" "label 2=path2.wav" ...
"""
import os
import subprocess
import sys
import tempfile

import numpy as np
import pyloudnorm as pyln
import soundfile as sf

SR = 48000
GAP = 1.0


def load(path):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le",
                          "-"], check=True, capture_output=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)


def main(out, items, title=None):
    meter = pyln.Meter(SR)
    parts, lines, t = [], [], 0.0
    for k, item in enumerate(items, 1):
        label, path = item.split("=", 1)
        y = load(path)
        lufs = meter.integrated_loudness(y)
        y = y * 10 ** ((-16.0 - lufs) / 20)
        pk = np.abs(y).max()
        if pk > 0.95:
            y *= 0.95 / pk
        lines.append(f"{k:2d}. {t:6.2f} s  {label}  ({len(y) / SR:.1f} s)")
        parts += [y, np.zeros(int(GAP * SR))]
        t += len(y) / SR + GAP
    a = np.concatenate(parts[:-1]).astype(np.float32)
    with tempfile.TemporaryDirectory() as d:
        wav = os.path.join(d, "a.wav")
        sf.write(wav, a, SR)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", wav, "-c:a", "aac", "-b:a", "160k", out], check=True)
    txt = os.path.splitext(out)[0] + ".txt"
    with open(txt, "w") as f:
        if title:
            f.write(title.rstrip() + "\n\n")
        f.write(f"Order (each clip at -16 LUFS, {GAP:.1f} s of silence between clips, {t - GAP:.1f} s total):\n")
        f.write("\n".join(lines) + "\n")
    print(open(txt).read())


if __name__ == "__main__":
    args = sys.argv[1:]
    title = None
    if args and args[0] == "--title":
        title, args = args[1], args[2:]
    main(args[0], args[1:], title)
