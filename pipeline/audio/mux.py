"""Put the pipeline's finished mix onto a rendered video (video stream copied), then verify loudness.

Remotion re-mixes and re-encodes audio; muxing mix.wav after the render guarantees the
delivered file keeps -14 LUFS / -1 dBTP exactly as mixed.

usage: python -m pipeline.audio.mux render.mp4 studio/public/episodes/<id>/mix.wav out.mp4
       python -m pipeline.audio.mux --check any.mp4      # just measure
"""
from __future__ import annotations

import argparse
import json
import subprocess

from .mix import ffmpeg_loudness


def mux(video: str, audio: str, out: str):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-i", audio, "-map", "0:v:0", "-map", "1:a:0",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-shortest", "-movflags", "+faststart", out],
                   check=True)
    return ffmpeg_loudness(out)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("files", nargs="+")
    a = ap.parse_args(argv)
    if a.check:
        for f in a.files:
            print(f, json.dumps(ffmpeg_loudness(f)))
        return
    video, audio, out = a.files
    print(out, json.dumps(mux(video, audio, out)))


if __name__ == "__main__":
    main()
