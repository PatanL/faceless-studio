"""Review sheets: out/<slug>/qa/sbs.jpg (ours over the source, one column per beat), stills.jpg (12 frames) and
timeline.jpg (one frame per second, for orientation), plus the every-frame sheets in qa/f30/ (frames30.py).

usage: python -m pipeline.qa.sheet <slug> [--root DIR] [--source-frames auto|none]

Labels use a built-in 5x7 bitmap font, so this needs only numpy + ffmpeg (the Spark's static ffmpeg has no
drawtext and its venv has no Pillow). Source frames come from $STUDIO_REFS/<niche>/<source_id>.mp4
(default ~/studio/refs); when the source video is not on disk the source row shows the beat label only.
"""
from __future__ import annotations

import argparse
import sys

import numpy as np

from . import frames
from .util import be_nice, find_mp4, front_matter, probe_duration, qa_dir, read_json, refs_dir, root

CW, CH = 216, 384          # cell = one 9:16 frame at 1/5 scale
LAB = 22                   # label strip height
BG = (16, 18, 22)
FG = (235, 235, 235)
ACC = (255, 90, 74)

_F = {  # 5x7 glyphs, rows top to bottom, '#' = on
    "A": ".###.#...##...#######...##...##...#", "B": "####.#...##...#####.#...##...#####.",
    "C": ".###.#...##....#....#....#...#.###.", "D": "####.#...##...##...##...##...#####.",
    "E": "######....#....####.#....#....#####", "F": "######....#....####.#....#....#....",
    "G": ".###.#...##....#.####...##...#.###.", "H": "#...##...##...#######...##...##...#",
    "I": ".###...#....#....#....#....#...###.", "J": "..###...#....#....#.#..#.#..#..##..",
    "K": "#...##..#.#.#..##...#.#..#..#.#...#", "L": "#....#....#....#....#....#....#####",
    "M": "#...###.###.#.##.#.##...##...##...#", "N": "#...###..##.#.##..###...##...##...#",
    "O": ".###.#...##...##...##...##...#.###.", "P": "####.#...##...#####.#....#....#....",
    "Q": ".###.#...##...##...##.#.##..#..##.#", "R": "####.#...##...#####.#.#..#..#.#...#",
    "S": ".#####....#.....###.....#....#####.", "T": "#####..#....#....#....#....#....#..",
    "U": "#...##...##...##...##...##...#.###.", "V": "#...##...##...##...##...#.#.#...#..",
    "W": "#...##...##...##.#.##.#.##.#.#.#.#.", "X": "#...##...#.#.#...#...#.#.#...##...#",
    "Y": "#...##...#.#.#...#....#....#....#..", "Z": "#####....#...#...#...#...#....#####",
    "0": ".###.#...##..###.#.###..##...#.###.", "1": "..#...##....#....#....#....#...###.",
    "2": ".###.#...#....#...#...#...#...#####", "3": "#####...#...#.....#.....##...#.###.",
    "4": "...#...##..#.#.#..#.#####...#....#.", "5": "######....####.....#....##...#.###.",
    "6": "..##..#...#....####.#...##...#.###.", "7": "#####....#...#...#...#....#....#...",
    "8": ".###.#...##...#.###.#...##...#.###.", "9": ".###.#...##...#.####....#...#..##..",
    ":": "......##...##........##...##.......", ".": "..........................##...##..",
    "-": "...............#####...............", "%": "##...##..#...#...#...#...#..##...##",
    "/": "....#....#...#...#...#...#....#....", "#": ".#.#..#.#.#####.#.#.#####.#.#..#.#.",
    "+": ".......#....#..#####..#....#.......", "(": "...#...#...#....#....#.....#.....#.",
    ")": ".#.....#.....#....#....#...#...#...", "?": ".###.#...#....#...#...#.........#..",
    "'": "..#....#...#.......................", ",": ".....................##....#...#...",
    "_": "..............................#####", "=": "..........#####.....#####..........",
    " ": "." * 35,
}


def _glyph(ch: str) -> np.ndarray:
    s = _F.get(ch.upper(), _F["?"])
    s = (s + "." * 35)[:35]
    return np.array([[c == "#" for c in s[r * 5:(r + 1) * 5]] for r in range(7)])


def text(img: np.ndarray, x: int, y: int, s: str, color=FG, scale: int = 2) -> None:
    """Draw s at (x, y) in place, clipped to the image."""
    H, W, _ = img.shape
    for ch in s:
        g = np.kron(_glyph(ch), np.ones((scale, scale), dtype=bool))
        h, w = g.shape
        if x + w > W:
            break
        if y + h <= H and x >= 0 and y >= 0:
            region = img[y:y + h, x:x + w]
            region[g] = color
        x += 6 * scale


def cell(img: np.ndarray | None, label: str, color=FG, note: str = "") -> np.ndarray:
    c = np.full((CH + LAB, CW, 3), BG, dtype=np.uint8)
    if img is not None:
        c[LAB:] = img
    else:
        text(c, 8, LAB + CH // 2 - 20, note or "NO SOURCE FRAME", (150, 150, 150))
    text(c, 4, 4, label[:17], color)
    return c


def grid(cells: list[np.ndarray], cols: int, pad: int = 4) -> np.ndarray:
    rows = (len(cells) + cols - 1) // cols
    h, w, _ = cells[0].shape
    out = np.full((rows * (h + pad) + pad, cols * (w + pad) + pad, 3), BG, dtype=np.uint8)
    for i, c in enumerate(cells):
        r, k = divmod(i, cols)
        out[pad + r * (h + pad):pad + r * (h + pad) + h, pad + k * (w + pad):pad + k * (w + pad) + w] = c
    return out


def mmss(t: float) -> str:
    return f"{int(t // 60)}:{t % 60:04.1f}"


def stills(mp4, samples: np.ndarray, dur: float) -> np.ndarray:
    """12 frames: frame 0 (the cover), 10 evenly spaced, the last frame (loop check)."""
    n = len(samples)
    cells = [cell(samples[0], "0:00.0 COVER", ACC)]
    for k in range(1, 11):
        t = dur * k / 11
        cells.append(cell(samples[min(n - 1, int(t))], mmss(int(t))))
    cells.append(cell(frames.grab(mp4, None, CW, CH, last=True), f"{mmss(dur)} LAST", ACC))
    return grid(cells, 6)


def timeline(samples: np.ndarray) -> np.ndarray:
    """Every 1 fps sample in order, 10 per row: shows what each second puts on screen and how often the setting changes."""
    return grid([cell(f, mmss(i)) for i, f in enumerate(samples)], 10)


def source_video(niche: str, ids: list[str]):
    for sid in ids:
        if not sid:
            continue
        p = refs_dir() / niche / f"{sid}.mp4"
        if p.is_file():
            return sid, p
    return (ids[0] if ids else None), None


def beat_plan(dur: float, bm: dict | None, src: dict, src_dur: float | None) -> list[tuple[str, float, float | None]]:
    """[(label, our t, source t)] one per skeleton beat (beatmap + source.json), else 8 evenly spaced points."""
    plan = []
    sk = src.get("skeleton") or []
    beats = {b.get("i"): b for b in src.get("beats") or []}
    if bm and bm.get("scenes") and sk:
        for k in sk:
            sc = [s for s in bm["scenes"] if s.get("skeleton_i") == k.get("i")]
            if not sc:
                continue
            ours = (min(s["t0"] for s in sc) + max(s["t1"] for s in sc)) / 2
            sb_ = [beats[i] for i in k.get("from_beats", []) if i in beats]
            st = (min(b["t0"] for b in sb_) + max(b["t1"] for b in sb_)) / 2 if sb_ else None
            plan.append((str(k.get("label", k.get("i"))), ours, st))
        if plan:
            return plan
    for k in range(8):
        f = (k + 0.5) / 8
        plan.append((f"{int(f * 100)}%", f * dur, f * src_dur if src_dur else None))
    return plan


def sbs(mp4, dur: float, bm, src: dict, fm: dict, niche: str, source_frames: str = "auto") -> np.ndarray:
    # Only the episode's own source: its beat times (source.json) mean nothing on another video, so a corpus
    # neighbour is never substituted when the source MP4 is missing (that showed a jellyfish TikTok under an orca
    # episode). Episodes without source.json (no beat times) may still fall back to their front-matter references.
    ids = [src["source_id"]] if src.get("source_id") else list(fm.get("_references") or [])
    sid, svid = source_video(niche, [i for i in ids if i]) if source_frames == "auto" else (src.get("source_id"), None)
    sdur = probe_duration(svid) if svid else None
    plan = beat_plan(dur, bm, src, sdur)
    top, bottom = [], []
    for label, t, st in plan:
        top.append(cell(frames.grab(mp4, t, CW, CH), f"{label} {mmss(t)}", ACC))
        img = frames.grab(svid, st, CW, CH) if svid and st is not None else None
        bottom.append(cell(img, f"SRC {mmss(st)}" if st is not None else "SRC", FG,
                           note=f"{(sid or 'NO SOURCE')[:14]}" + ("" if svid else " NOT ON DISK")))
    sheet = grid(top + bottom, len(plan))
    head = np.full((30, sheet.shape[1], 3), BG, dtype=np.uint8)
    text(head, 6, 8, f"OURS (TOP) VS SOURCE {sid or '-'} (BOTTOM)"[:max(10, sheet.shape[1] // 12)], FG)
    return np.concatenate([head, sheet])


def make_all(r, slug: str, mp4, samples, dur: float, sb, bm, src, fm, niche: str, source_frames="auto") -> dict:
    qd = qa_dir(r, slug)
    out = {"sbs": qd / "sbs.jpg", "stills": qd / "stills.jpg", "timeline": qd / "timeline.jpg"}
    frames.to_jpg(sbs(mp4, dur, bm, src, fm, niche, source_frames), out["sbs"])
    frames.to_jpg(stills(mp4, samples, dur), out["stills"])
    frames.to_jpg(timeline(samples), out["timeline"])
    from . import frames30
    out["frames30"] = qd / "frames30.json"
    frames30.make(r, slug, mp4, sb)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.qa.sheet")
    ap.add_argument("slug")
    ap.add_argument("--root")
    ap.add_argument("--source-frames", choices=["auto", "none"], default="auto")
    a = ap.parse_args(argv)
    be_nice()
    r = root(a.root)
    ep = r / "episodes" / a.slug
    mp4 = find_mp4(r, a.slug)
    if not mp4:
        print(f"no MP4 for {a.slug}", file=sys.stderr)
        return 1
    dur = probe_duration(mp4)
    script = ep / "script.md"
    fm = front_matter(script.read_text(encoding="utf-8")) if script.is_file() else {}
    out = make_all(r, a.slug, mp4, frames.sample_video(mp4), dur, read_json(ep / "storyboard.json") or {},
                   read_json(ep / "beatmap.json"), read_json(ep / "source.json") or {}, fm,
                   fm.get("niche") or "explainer", a.source_frames)
    for k, v in out.items():
        print(f"{k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
