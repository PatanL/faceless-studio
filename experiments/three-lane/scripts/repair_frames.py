"""Find and repair one-frame render glitches in a three-lane render (our own code).

Chrome's GPU screenshot on the Mac (--gl=angle) now and then returns a frame tiled into a mosaic (story-vasa v1/v2:
about 7 in 1,900 frames). A glitch frame differs strongly from both neighbours while the neighbours match each other.
This finds them, re-renders exactly those frames as stills, and overlays the stills onto the video (one x264 re-encode).

usage: python3 repair_frames.py <video.mp4> <out.mp4> --bundle DIR --props storyboard.json --comp Vasa3D [--gl angle]
"""
import argparse, json, os, subprocess, sys, tempfile
import cv2
import numpy as np

def glitch_frames(path, ratio=2.5, floor=3.0):
    cap = cv2.VideoCapture(path)
    small = []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        small.append(cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (90, 160)).astype(np.float32))
    out = []
    if len(small) > 2:   # frame 0 has no left neighbour: compare it with frames 1 and 2
        a0 = np.abs(small[0] - small[1]).mean(); c0 = np.abs(small[1] - small[2]).mean()
        if a0 > floor and a0 > ratio * max(c0, 1.0):
            out.append(0)
    for i in range(1, len(small) - 1):
        a = np.abs(small[i] - small[i - 1]).mean(); b = np.abs(small[i] - small[i + 1]).mean()
        c = np.abs(small[i - 1] - small[i + 1]).mean()
        if min(a, b) > floor and min(a, b) > ratio * max(c, 1.0):
            out.append(i)
    return out, len(small)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("out")
    ap.add_argument("--bundle", required=True); ap.add_argument("--props", required=True); ap.add_argument("--comp", required=True)
    ap.add_argument("--gl", default="angle"); ap.add_argument("--ffmpeg", default="ffmpeg")
    a = ap.parse_args()
    bad, n = glitch_frames(a.video)
    print(json.dumps({"frames": n, "glitch": bad}))
    if not bad:
        subprocess.run(["cp", a.video, a.out], check=True); return
    here = os.path.dirname(os.path.abspath(__file__))
    tmp = tempfile.mkdtemp(prefix="repair_")
    subprocess.run(["nice", "-n", "15", "node", os.path.join(here, "stills.mjs"), os.path.abspath(a.bundle), os.path.abspath(a.props), tmp, a.comp, a.gl, *map(str, bad)],
                   check=True, cwd=os.path.dirname(here))
    inputs, chain, last = ["-i", a.video], [], "0:v"
    for k, f in enumerate(bad, 1):
        inputs += ["-i", os.path.join(tmp, f"f{f:05d}.png")]
        tag = f"v{k}"
        chain.append(f"[{last}][{k}:v]overlay=enable='eq(n\\,{f})'[{tag}]"); last = tag
    cmd = [a.ffmpeg, "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(chain), "-map", f"[{last}]", "-map", "0:a?",
           "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "copy", a.out]
    subprocess.run(["nice", "-n", "10", *cmd], check=True)
    again, _ = glitch_frames(a.out)
    print(json.dumps({"repaired": bad, "left": again}))

if __name__ == "__main__":
    sys.exit(main())
