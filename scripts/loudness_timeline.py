#!/usr/bin/env python3
"""Momentary-loudness check of a mix (ffmpeg ebur128): is the scare the loudest moment?

usage: python3 scripts/loudness_timeline.py <mix.wav|mp4> [cues.json] [--speech A-B]
Prints integrated / LRA / true peak, the narration's momentary median and p90 (speech window, default the
middle 50 % of the file), and the max momentary of every cue window in cues.json ([{cue, at, dur}]).
"""
import json
import re
import statistics as st
import subprocess
import sys


def timeline(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    rows = [(float(a), float(b), float(c)) for a, b, c in
            re.findall(r"t:\s*([\d.]+)\s+TARGET:\S+\s+LUFS\s+M:\s*(-?[\d.]+)\s+S:\s*(-?[\d.]+)", r.stderr)]
    tail = r.stderr[r.stderr.rfind("Summary:"):]
    get = lambda k: float(re.search(rf"{k}:\s+(-?[\d.]+)", tail).group(1))
    return rows, {"I": get("I"), "LRA": get("LRA"), "TP": get("Peak")}


def main():
    args = sys.argv[1:]
    path = args[0]
    cues = json.load(open(args[1])) if len(args) > 1 and args[1].endswith(".json") else []
    rows, summ = timeline(path)
    dur = rows[-1][0] if rows else 0
    a, b = dur * 0.25, dur * 0.75
    if "--speech" in args:
        a, b = map(float, args[args.index("--speech") + 1].split("-"))
    sp = sorted(m for t, m, _ in rows if a <= t <= b and m > -40)
    print(f"I {summ['I']} LUFS  LRA {summ['LRA']} LU  TP {summ['TP']} dBTP")
    if sp:
        print(f"speech {a:.0f}-{b:.0f}s momentary median {st.median(sp):.1f}  p90 {sp[int(0.9 * len(sp))]:.1f}")
    for c in cues:
        w = [m for t, m, _ in rows if c["at"] + 0.3 <= t <= c["at"] + c.get("dur", 1.0) + 0.3]
        if w:
            print(f"  {c['cue']:<14} @{c['at']:6.2f}s  max M {max(w):6.1f}")


if __name__ == "__main__":
    main()
