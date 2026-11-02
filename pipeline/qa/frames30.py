"""Every-frame review material: out/<slug>/qa/f30/ (every frame at the native rate, 2 s per sheet) and
out/<slug>/qa/frames30.json (per-frame flags a script can find, for the reviewers to look at first).

usage: python -m pipeline.qa.frames30 <slug> [--root DIR] [--mp4 PATH (a video outside the episode layout)]

Nothing is skipped or resampled: sheet NN holds frames [NN*2s, NN*2s+2s) in order, 10 per row, each labelled with
its time and frame number. REVIEW_PROMPT.md section 3 splits the sheets across frame reviewers.

Flags (diff = mean |RGB(t) - RGB(t-1)| on the cell-sized proxy, 0-255):
  flash   a frame unlike both neighbours while the neighbours match each other (a one-frame pop or glitch)
  jump    diff > max(12, 5 x the median of the surrounding 1 s): something moved or changed in one frame instead of
          easing. `transition: true` when it is within 0.5 s of a scene start (check it looks intended)
  frozen  >= 0.5 s of identical frames (diff < 0.05) outside the first and last 0.5 s
"""
from __future__ import annotations

import argparse
import subprocess
import sys

import numpy as np

from . import frames
from .sheet import BG, FG, ACC, grid, mmss, text
from .util import be_nice, find_mp4, qa_dir, read_json, root, tool, write_json

FW, FH = 162, 288          # one 9:16 frame at 0.15 scale
LAB = 18
COLS = 10
SECONDS_PER_SHEET = 2


def probe_fps(mp4) -> float:
    p = subprocess.run([tool("ffprobe"), "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=avg_frame_rate", "-of", "csv=p=0", str(mp4)], capture_output=True, text=True)
    num, _, den = (p.stdout.strip() or "30/1").partition("/")
    return float(num) / float(den or 1)


def iter_frames(mp4, w: int = FW, h: int = FH):
    """Every decoded frame in order as (h, w, 3) uint8, streamed (no resampling: -vsync passthrough)."""
    cmd = [tool("ffmpeg"), "-nostdin", "-hide_banner", "-loglevel", "error", *frames.THREADS, "-i", str(mp4),
           "-an", "-fps_mode", "passthrough", "-vf", frames._fit(w, h), "-f", "rawvideo", "pipe:1"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    need = w * h * 3
    try:
        while True:
            buf = p.stdout.read(need)
            if len(buf) < need:
                break
            yield np.frombuffer(buf, dtype=np.uint8).reshape(h, w, 3)
    finally:
        p.stdout.close()
        p.wait()


def fcell(img: np.ndarray, i: int, fps: float, mark: bool) -> np.ndarray:
    c = np.full((FH + LAB, FW, 3), BG, dtype=np.uint8)
    c[LAB:] = img
    text(c, 3, 3, f"{i / fps:.2f} F{i}"[:13], ACC if mark else FG, scale=1)
    return c


def boundaries(sb: dict, fps: float) -> set[int]:
    """frame numbers of scene starts, from storyboard.json (empty when it has no timings)"""
    out, t = set(), 0.0
    for s in (sb or {}).get("scenes", []):
        d = s.get("duration") or s.get("dur")
        if not isinstance(d, (int, float)):
            return set()
        out.add(round(t * fps))
        t += d
    return out


def flags(diff: np.ndarray, skip: np.ndarray, fps: float, cuts: set[int]) -> list[dict]:
    """diff[i]: frame i vs i-1; skip[i]: frame i-1 vs i+1 (frame i's neighbours compared with each other)"""
    n, out = len(diff), []
    near_cut = lambda i: any(abs(i - c) <= fps / 2 for c in cuts)
    for i in range(1, n - 1):
        if min(diff[i], diff[i + 1]) > 6 and skip[i] < 0.35 * min(diff[i], diff[i + 1]):
            out.append({"kind": "flash", "frame": i, "t": round(i / fps, 3), "diff": round(float(diff[i]), 1)})
    r = int(fps // 2)
    for i in range(1, n):
        med = float(np.median(diff[max(1, i - r):i + r + 1]))
        if diff[i] > max(12.0, 5 * med):
            out.append({"kind": "jump", "frame": i, "t": round(i / fps, 3), "diff": round(float(diff[i]), 1),
                        "transition": near_cut(i)})
    run_start = None
    for i in range(1, n + 1):
        still = i < n and diff[i] < 0.05
        if still and run_start is None:
            run_start = i
        elif not still and run_start is not None:
            if (i - run_start) / fps >= 0.5 and run_start / fps > 0.5 and i / fps < n / fps - 0.5:
                out.append({"kind": "frozen", "frame": run_start, "t": round(run_start / fps, 3),
                            "len_s": round((i - run_start) / fps, 2)})
            run_start = None
    return sorted(out, key=lambda f: f["frame"])


def make(r, slug: str, mp4, sb: dict | None = None) -> dict:
    qd = qa_dir(r, slug)
    od = qd / "f30"
    od.mkdir(parents=True, exist_ok=True)
    for old in od.glob("*.jpg"):
        old.unlink()
    fps = probe_fps(mp4)
    per = int(round(fps * SECONDS_PER_SHEET))
    cuts = boundaries(sb or {}, fps)
    diffs, skips, chunk, sheets = [0.0], [0.0], [], []
    prev = prev2 = None
    for i, f in enumerate(iter_frames(mp4)):
        g = f.astype(np.int16)
        if prev is not None:
            diffs.append(float(np.abs(g - prev).mean()))
        if prev2 is not None:
            skips.append(float(np.abs(g - prev2).mean()))
        prev2, prev = prev, g
        chunk.append(fcell(f, i, fps, i in cuts))
        if len(chunk) == per:
            sheets.append(_write(od, len(sheets), chunk, per, fps))
            chunk = []
    if chunk:
        sheets.append(_write(od, len(sheets), chunk, per, fps))
    diff = np.array(diffs)
    fl = flags(diff, np.array(skips + [0.0]), fps, cuts)
    rep = {"v": 1, "slug": slug, "fps": round(fps, 3), "frames": len(diff), "seconds_per_sheet": SECONDS_PER_SHEET,
           "sheets": [str(p.relative_to(r)) for p in sheets], "scene_starts": sorted(cuts), "flags": fl,
           "counts": {k: sum(f["kind"] == k for f in fl) for k in ("flash", "jump", "frozen")}}
    write_json(qd / "frames30.json", rep)
    return rep


def _write(od, k: int, chunk: list[np.ndarray], per: int, fps: float):
    p = od / f"{k:02d}_{mmss(k * per / fps).replace(':', 'm').replace('.', 's')}.jpg"
    frames.to_jpg(grid(chunk, COLS, pad=2), p)
    return p


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.qa.frames30")
    ap.add_argument("slug")
    ap.add_argument("--root")
    ap.add_argument("--mp4")
    a = ap.parse_args(argv)
    be_nice()
    r = root(a.root)
    mp4 = a.mp4 or find_mp4(r, a.slug)
    if not mp4:
        print(f"no MP4 for {a.slug}", file=sys.stderr)
        return 1
    rep = make(r, a.slug, mp4, read_json(r / "episodes" / a.slug / "storyboard.json"))
    print(f"{rep['frames']} frames at {rep['fps']} fps -> {len(rep['sheets'])} sheets in out/{a.slug}/qa/f30/; "
          f"flags {rep['counts']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
