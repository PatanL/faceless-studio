"""Deterministic synthetic data for --dry-run, tests and proofs. Rows built from it carry `dry_run: true` and
`source: "synthetic"`, and every reader that learns from data (experiments, learning, killrule) skips them.

  python -m pipeline.analytics.synthetic retention --duration 75.13 --drop 13.0:0.08 --drop 30.5:0.07 > curve.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import sys


def seed_of(*parts) -> int:
    return int(hashlib.sha256("|".join(map(str, parts)).encode()).hexdigest()[:12], 16)


def retention_curve(duration_s: float, drops: list[tuple[float, float]] = (), seed: int = 0,
                    start: float = 1.05, hook_loss: float = 0.30, decay_per_s: float = 0.006,
                    end_spike: float = 0.05, noise: float = 0.0) -> dict:
    """YouTube-shaped audience retention: 100 points at elapsedVideoTimeRatio 0.01..1.00.
    Hook swipe-off in the first ~1.5 s, slow exponential decay, a cliff of `size` (absolute watch-ratio, spread over
    ~0.6 s) at each (t, size) in `drops`, and a small loop spike in the last 3 %."""
    rnd = random.Random(seed)
    xs = [round(0.01 * k, 2) for k in range(1, 101)]
    out, rel = [], []
    for x in xs:
        t = x * duration_s
        r = start - hook_loss * (1 - math.exp(-t / 0.6))
        r *= math.exp(-decay_per_s * t)
        for (td, size) in drops:
            r -= size / (1 + math.exp(-(t - td) / 0.15))
        if x > 0.97:
            r += end_spike * (x - 0.97) / 0.03
        if noise:
            r += rnd.uniform(-noise, noise)
        out.append(round(max(r, 0.0), 4))
        rel.append(round(min(max(0.5 + (r - 0.55), 0.0), 1.0), 4))
    return {"x": xs, "watch_ratio": out, "relative": rel}


def heatmap(duration_s: float, bumps: list[tuple[float, float]] = (), base: float = 0.25, seed: int = 0,
            noise: float = 0.0) -> dict:
    """yt-dlp-shaped Most-replayed heatmap: 100 equal segments, value normalised so the max is 1.0. A high start
    (rewatched intro), slow decay, and a Gaussian bump of `height` at each (t, height) in `bumps` (width 4 % of D)."""
    rnd = random.Random(seed)
    n, w = 100, 0.04 * duration_s
    raw = []
    for k in range(n):
        t = (k + 0.5) * duration_s / n
        v = base + 0.5 * math.exp(-t / (0.03 * duration_s)) + 0.1 * math.exp(-t / duration_s)
        v += sum(h * math.exp(-((t - tb) / w) ** 2) for tb, h in bumps)
        v += rnd.uniform(-noise, noise) if noise else 0.0
        raw.append(max(v, 0.0))
    top = max(raw) or 1.0
    seg = duration_s / n
    pts = [{"start": round(k * seg, 3), "end": round((k + 1) * seg, 3), "value": round(v / top, 5)} for k, v in enumerate(raw)]
    return {"duration_s": duration_s, "status": "ok", "synthetic": True, "points": pts}


def totals(post_key: str, window: str, duration_s: float) -> dict:
    rnd = random.Random(seed_of(post_key, window))
    views = int(rnd.lognormvariate(8.0 if window == "48h" else 8.6, 1.0))
    avg_pct = round(rnd.uniform(55, 95), 1)
    return {"views": views, "engaged_views": int(views * rnd.uniform(0.55, 0.8)),
            "likes": int(views * rnd.uniform(0.01, 0.05)), "comments": int(views * rnd.uniform(0.0005, 0.003)),
            "shares": int(views * rnd.uniform(0.001, 0.01)), "saves": None,
            "subs_gained": int(views * rnd.uniform(0.0005, 0.004)),
            "avg_view_pct": avg_pct, "avg_view_s": round(duration_s * avg_pct / 100, 1),
            "watch_time_min": round(views * duration_s * avg_pct / 100 / 60, 1)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.analytics.synthetic")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("retention")
    r.add_argument("--duration", type=float, required=True)
    r.add_argument("--drop", action="append", default=[], help="T:SIZE, e.g. 13.0:0.08")
    r.add_argument("--seed", type=int, default=0)
    r.add_argument("--noise", type=float, default=0.0)
    h = sub.add_parser("heatmap")
    h.add_argument("--duration", type=float, required=True)
    h.add_argument("--bump", action="append", default=[], help="T:HEIGHT, e.g. 320:0.6")
    h.add_argument("--seed", type=int, default=0)
    h.add_argument("--noise", type=float, default=0.0)
    a = ap.parse_args(argv)
    if a.cmd == "heatmap":
        bumps = [(float(t), float(v)) for t, v in (b.split(":") for b in a.bump)]
        json.dump({**heatmap(a.duration, bumps, seed=a.seed, noise=a.noise), "planted_bumps": bumps}, sys.stdout)
        print()
        return 0
    drops = [(float(t), float(s)) for t, s in (d.split(":") for d in a.drop)]
    ret = retention_curve(a.duration, drops, a.seed, noise=a.noise)
    json.dump({"duration_s": a.duration, "synthetic": True, "planted_drops": drops, "retention": ret}, sys.stdout)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
