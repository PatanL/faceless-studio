"""Stills for a setting / logic audit: every `step` seconds plus both sides of every boundary, and labelled contact sheets.

usage: python -I sample_frames.py <video> <out_dir> [--step 0.5] [--events X_events.json] [--storyboard sb.json]
                                  [--width 360] [--cols 6] [--threads 6]

Writes <out_dir>/f_<frame>.jpg (frame index at the native rate, width --width), and contact sheets
<out_dir>/sheet_<n>.jpg with the timestamp, frame number and storyboard scene id burned under each tile.
Boundaries = scene starts from the storyboard, hard cuts and transition spans from every_frame.py's events.json; each
boundary gets frames at -3 and +3 (and the transition's start/end) so a setting change is seen on both sides.
"""
import argparse
import json
import os

import cv2
import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("out_dir")
    ap.add_argument("--step", type=float, default=0.5)
    ap.add_argument("--events")
    ap.add_argument("--storyboard")
    ap.add_argument("--width", type=int, default=360)
    ap.add_argument("--cols", type=int, default=6)
    ap.add_argument("--threads", type=int, default=6)
    a = ap.parse_args()
    cv2.setNumThreads(a.threads)
    os.makedirs(a.out_dir, exist_ok=True)
    cap = cv2.VideoCapture(a.video)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    want = {int(round(k * a.step * fps)) for k in range(int(n / fps / a.step) + 1)}
    scenes = []
    if a.storyboard:
        t = 0.0
        for s in json.load(open(a.storyboard))["scenes"]:
            scenes.append((t, s["id"]))
            k = int(round(t * fps))
            want |= {k - 3, k + 3}
            t += s["duration"]
    if a.events:
        ev = json.load(open(a.events))
        for c in ev["cuts"]:
            k = int(round(c * fps))
            want |= {k - 3, k + 3}
        for tr in ev["transitions"]:
            want |= {int(round(tr["start"] * fps)), int(round(tr["t"] * fps)), int(round(tr["end"] * fps))}
    want = sorted(k for k in want if 0 <= k < n)
    sid = lambda t: next((i for st, i in reversed(scenes) if t >= st - 1e-6), "")
    tiles = []
    k = 0
    wi = 0
    while wi < len(want):
        ok, fr = cap.read()
        if not ok:
            break
        if k == want[wi]:
            h = int(fr.shape[0] * a.width / fr.shape[1])
            im = cv2.resize(fr, (a.width, h), interpolation=cv2.INTER_AREA)
            cv2.imwrite(os.path.join(a.out_dir, f"f_{k:05d}.jpg"), im, [cv2.IMWRITE_JPEG_QUALITY, 88])
            t = k / fps
            lab = np.full((34, a.width, 3), 20, np.uint8)
            cv2.putText(lab, f"{int(t // 60)}:{t % 60:05.2f}  f{k}  {sid(t)}", (6, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.62,
                        (240, 240, 240), 1, cv2.LINE_AA)
            tiles.append(np.vstack([im, lab]))
            wi += 1
        k += 1
    per = a.cols * 3
    for s in range(0, len(tiles), per):
        grp = tiles[s:s + per]
        while len(grp) % a.cols:
            grp.append(np.zeros_like(tiles[0]))
        rows = [np.hstack(grp[r:r + a.cols]) for r in range(0, len(grp), a.cols)]
        cv2.imwrite(os.path.join(a.out_dir, f"sheet_{s // per:02d}.jpg"), np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 84])
    print(len(tiles), "frames,", (len(tiles) + per - 1) // per, "sheets ->", a.out_dir)


if __name__ == "__main__":
    main()
