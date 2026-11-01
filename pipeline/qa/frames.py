"""Frame sampling and per-frame measures (ffmpeg rawvideo -> numpy).

All ffmpeg calls use 2 threads; callers run them one at a time (design 1.5: <= 2 ffmpeg at once).
"""
from __future__ import annotations

import pathlib

import numpy as np

from .util import run, tool

SAMPLE_W, SAMPLE_H = 216, 384  # 1/5 of 1080x1920; 16:9 sources are letterboxed into it
THREADS = ["-threads", "2", "-filter_threads", "2"]


def _fit(w: int, h: int) -> str:
    return (f"scale={w}:{h}:force_original_aspect_ratio=decrease:flags=area,"
            f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=black,format=rgb24")


def sample_video(mp4, fps: float = 1.0, w: int = SAMPLE_W, h: int = SAMPLE_H) -> np.ndarray:
    """Frames at t = 0, 1/fps, 2/fps ... as uint8 (N, h, w, 3). Frame 0 is the cover."""
    cmd = [tool("ffmpeg"), "-nostdin", "-hide_banner", "-loglevel", "error", *THREADS, "-i", str(mp4),
           "-an", "-vf", f"fps={fps}:round=down,{_fit(w, h)}", "-f", "rawvideo", "pipe:1"]
    p = run(cmd, binary=True)
    if p.returncode != 0:
        raise RuntimeError(f"ffmpeg sample failed: {p.stderr.decode(errors='ignore')[-300:]}")
    buf = np.frombuffer(p.stdout, dtype=np.uint8)
    n = buf.size // (w * h * 3)
    return buf[: n * w * h * 3].reshape(n, h, w, 3)


def grab(mp4, t: float | None, w: int = SAMPLE_W, h: int = SAMPLE_H, last: bool = False) -> np.ndarray | None:
    """One frame at t seconds (or the last frame with last=True) as (h, w, 3)."""
    # no -ss at 0: the image2 demuxer (thumbnails) returns no frame after an input seek
    pre = ["-sseof", "-0.25"] if last else ["-ss", f"{t:.3f}"] if t and t > 0 else []
    post = [] if last else ["-frames:v", "1"]
    cmd = [tool("ffmpeg"), "-nostdin", "-hide_banner", "-loglevel", "error", *THREADS, *pre, "-i", str(mp4),
           "-an", "-vf", _fit(w, h), *post, "-f", "rawvideo", "pipe:1"]
    p = run(cmd, binary=True)
    need = w * h * 3
    if p.returncode != 0 or len(p.stdout) < need:
        return None
    buf = np.frombuffer(p.stdout[-need:], dtype=np.uint8)  # last=True decodes the final 0.25 s: keep the last frame
    return buf.reshape(h, w, 3)


def load_image(path, w: int, h: int) -> np.ndarray | None:
    if not path or not pathlib.Path(path).is_file():
        return None
    return grab(path, 0.0, w, h)


def gray(img: np.ndarray) -> np.ndarray:
    return img[..., 0] * 0.299 + img[..., 1] * 0.587 + img[..., 2] * 0.114


def _resize_mean(a: np.ndarray, oh: int, ow: int) -> np.ndarray:
    h, w = a.shape
    ys = np.linspace(0, h, oh + 1).astype(int)
    xs = np.linspace(0, w, ow + 1).astype(int)
    out = np.empty((oh, ow))
    for i in range(oh):
        for j in range(ow):
            out[i, j] = a[ys[i]:max(ys[i + 1], ys[i] + 1), xs[j]:max(xs[j + 1], xs[j] + 1)].mean()
    return out


def dhash(img: np.ndarray | None, size: int = 8) -> str | None:
    """Difference hash (size x size bits, hex). Robust to re-encodes, small brightness and colour changes."""
    if img is None:
        return None
    g = _resize_mean(gray(img.astype(np.float64)), size, size + 1)
    bits = (g[:, 1:] > g[:, :-1]).flatten()
    v = 0
    for b in bits:
        v = (v << 1) | int(b)
    return f"{v:0{size * size // 4}x}"


def magenta_share(img: np.ndarray, tol: int = 8) -> float:
    """Share of pixels within +-tol of #FF00FF (the kit's 'missing: name' box)."""
    r, g, b = (img[..., i].astype(np.int16) for i in range(3))
    m = (r >= 255 - tol) & (g <= tol) & (b >= 255 - tol)
    return float(m.mean())


def is_blank(img: np.ndarray, std_max: float = 2.0) -> bool:
    """Near-uniform frame that is not black (e.g. a flat colour where a scene failed to draw)."""
    g = gray(img.astype(np.float64))
    return float(g.std()) < std_max and float(g.mean()) > 20


def to_jpg(img: np.ndarray, path, q: int = 3) -> None:
    h, w, _ = img.shape
    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    cmd = [tool("ffmpeg"), "-nostdin", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo",
           "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-i", "pipe:0", "-frames:v", "1", "-q:v", str(q), str(path)]
    import subprocess
    p = subprocess.run(cmd, input=np.ascontiguousarray(img, dtype=np.uint8).tobytes(), capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(f"ffmpeg jpg write failed: {p.stderr.decode(errors='ignore')[-300:]}")
