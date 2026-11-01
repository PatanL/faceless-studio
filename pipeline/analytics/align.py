"""Align a retention curve (own video) or a Most-replayed heatmap (source video) to storyboard scenes, beats and
lines (OPERATOR_DESIGN 9.6, row shape 5.13).

  python -m pipeline.analytics.align <slug> [--window 7d] [--platform youtube] [--curve FILE] [--no-write]
  python -m pipeline.analytics.align --source <video_id> [--curve FILE] [--no-write]

Method: x -> seconds (`x * duration_s`), 3-point median smoothing, per-scene ret0/ret1/drop/drop_per_s, z-score of
drop_per_s against the episode's own scenes, rel_mean from relativeRetentionPerformance, and the top 3 local drops
(steepest smoothed fall between two curve points, at least max(2 s, 3 %) apart) with the scene, beat, narration
sentence and caption page on screen at that moment. The first 2 % (hook settling) and last 3 % (loop end spike)
are excluded from ranking and from z, but reported under `head` / `tail`.

For a heatmap (relative replay intensity, not a survival curve) the same fall-off ranking is used, plus
`heat_mean` per scene and `top_peaks` (most replayed moments).

`--curve FILE` (tests, proofs, manual imports): {"duration_s": D, "retention": {"x": [...], "watch_ratio": [...],
"relative": [...]}} or {"duration_s": D, "points": [{"start", "end", "value"}]}.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys

from . import beatmap as bmap
from ._common import (EXIT_NOTHING, EXIT_OK, EXIT_USAGE, dpath, iso, is_real, jsonl_append, jsonl_read, median,
                      now_utc, read_json, rpath, write_json_atomic)

HEAD, TAIL = 0.02, 0.03


def median3(ys: list[float]) -> list[float]:
    if len(ys) < 3:
        return list(ys)
    return [ys[0]] + [sorted(ys[i - 1:i + 2])[1] for i in range(1, len(ys) - 1)] + [ys[-1]]


def interp(ts: list[float], ys: list[float], t: float) -> float:
    if t <= ts[0]:
        return ys[0]
    if t >= ts[-1]:
        return ys[-1]
    lo, hi = 0, len(ts) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if ts[mid] <= t:
            lo = mid
        else:
            hi = mid
    f = (t - ts[lo]) / (ts[hi] - ts[lo]) if ts[hi] > ts[lo] else 0.0
    return ys[lo] + f * (ys[hi] - ys[lo])


def curve_from_retention(ret: dict, duration_s: float) -> tuple[list[float], list[float], list[float] | None]:
    xs, ys = ret["x"], ret["watch_ratio"]
    rel = ret.get("relative")
    ts = [float(x) * duration_s for x in xs]
    return ts, [float(y) for y in ys], ([float(v) for v in rel] if rel else None)


def curve_from_heatmap(points: list[dict]) -> tuple[list[float], list[float]]:
    pts = sorted(points, key=lambda p: p["start"])
    return [(p["start"] + p["end"]) / 2 for p in pts], [float(p["value"]) for p in pts]


def _z(vals: list[float | None]) -> list[float | None]:
    xs = [v for v in vals if v is not None]
    if len(xs) < 2:
        return [0.0 if v is not None else None for v in vals]
    m = sum(xs) / len(xs)
    sd = math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1)) or 1e-9
    return [None if v is None else round((v - m) / sd, 2) for v in vals]


def align(bm: dict, ts: list[float], ys: list[float], rel: list[float] | None = None, curve: str = "retention",
          duration_s: float | None = None, top_k: int = 3) -> dict:
    D = float(duration_s or bm.get("duration_s") or ts[-1])
    sm = median3(ys)
    lo_t, hi_t = HEAD * D, (1 - TAIL) * D
    R = lambda t: interp(ts, sm, t)

    scenes, ranked = [], []
    for s in bm["scenes"]:
        t0, t1 = float(s["t0"]), min(float(s["t1"]), D)
        r0, r1 = R(t0), R(t1)
        a, b = max(t0, lo_t), min(t1, hi_t)
        rk = (R(a) - R(b)) / (b - a) if b - a > 0.25 else None
        ranked.append(rk)
        row = {"scene_id": s["scene_id"], "beat": s.get("beat"), "skeleton_i": s.get("skeleton_i"),
               "source_beat_i": s.get("source_beat_i", []), "t0": round(t0, 3), "t1": round(t1, 3),
               "ret0": round(r0, 4), "ret1": round(r1, 4), "drop": round(r0 - r1, 4),
               "drop_per_s": round((r0 - r1) / (t1 - t0), 5) if t1 > t0 else 0.0,
               "drop_ranked_per_s": None if rk is None else round(rk, 5),
               "components": s.get("components", []), "line": s.get("text", "")}
        if rel:
            rs = [v for t, v in zip(ts, rel) if t0 <= t < t1]
            row["rel_mean"] = round(sum(rs) / len(rs), 4) if rs else None
        if curve == "heatmap":
            hs = [v for t, v in zip(ts, sm) if t0 <= t < t1]
            row["heat_mean"] = round(sum(hs) / len(hs), 4) if hs else round(R((t0 + t1) / 2), 4)
        scenes.append(row)
    for row, z in zip(scenes, _z(ranked)):
        row["z"] = z

    # local drops between consecutive curve points
    cands = []
    for k in range(1, len(ts)):
        ta, tb = ts[k - 1], ts[k]
        if tb <= ta or ta < lo_t or tb > hi_t:
            continue
        d = (sm[k - 1] - sm[k]) / (tb - ta)
        if d > 0:
            cands.append((d, (ta + tb) / 2, sm[k - 1] - sm[k]))
    cands.sort(key=lambda c: (-c[0], c[1]))
    sep = max(2.0, 0.03 * D)
    picked = []
    for d, t, dd in cands:
        if all(abs(t - p[1]) >= sep for p in picked):
            picked.append((d, t, dd))
        if len(picked) >= top_k:
            break
    top = []
    for d, t, dd in picked:
        sc, sent, prev, page = bmap.at(bm, t)
        top.append({"t": round(t, 2), "scene_id": sc and sc["scene_id"], "beat": sc and sc.get("beat"),
                    "drop": round(dd, 4), "drop_per_s": round(d, 5),
                    "line": sent and sent["text"], "prev_line": prev and prev["text"],
                    "caption": page and page["text"]})
    out = {"curve": curve, "duration_s": round(D, 3), "scenes": scenes, "top_drops": top,
           "head": {"t1": round(lo_t, 2), "ret0": round(sm[0], 4), "ret1": round(R(lo_t), 4)},
           "tail": {"t0": round(hi_t, 2), "ret0": round(R(hi_t), 4), "ret1": round(sm[-1], 4),
                    "end_spike": round(sm[-1] - R(hi_t), 4)}}
    if curve == "heatmap":
        peaks = []
        order = sorted(range(len(ts)), key=lambda k: (-sm[k], ts[k]))
        for k in order:
            if all(abs(ts[k] - p["t"]) >= sep for p in peaks):
                sc, sent, _, _ = bmap.at(bm, ts[k])
                peaks.append({"t": round(ts[k], 2), "value": round(sm[k], 4), "scene_id": sc and sc["scene_id"],
                              "beat": sc and sc.get("beat"), "line": sent and sent["text"]})
            if len(peaks) >= top_k:
                break
        out["top_peaks"] = peaks
    # summary per beat label
    by_beat: dict[str, list[float]] = {}
    for row in scenes:
        key = "heat_mean" if curve == "heatmap" else "z"
        if row.get(key) is not None:
            by_beat.setdefault(row["beat"] or "?", []).append(row[key])
    med = {b: median(v) for b, v in by_beat.items()}
    summ = {}
    if med:
        if curve == "heatmap":
            summ = {"best_beat": max(med, key=med.get), "worst_beat": min(med, key=med.get)}
        else:
            summ = {"worst_beat": max(med, key=med.get), "best_beat": min(med, key=med.get)}
    if curve == "retention":
        summ["hold_3s"] = round(R(3.0), 4)
    out["summary"] = summ
    return out


# ---------------------------------------------------------------- CLI helpers
def load_curve_file(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def latest_metrics(post_key: str, window: str) -> dict | None:
    rows = [r for r in jsonl_read(dpath("metrics.jsonl")) if r.get("post_key") == post_key and r.get("window") == window]
    real = [r for r in rows if is_real(r) and r.get("retention")]
    return (real or [r for r in rows if r.get("retention")] or [None])[-1]


def print_table(row: dict, stream=None) -> None:
    w = (stream or sys.stdout).write
    who = row.get("slug") or row.get("video_id")
    w(f"alignment {row['kind']} {who} curve={row['curve']} duration={row['duration_s']}s "
      f"beatmap={'derived' if row.get('beatmap_derived') else 'beatmap.json'}\n")
    heat = row["curve"] == "heatmap"
    w(f"{'scene':<6}{'beat':<26}{'t0':>7}{'t1':>7}{'ret0':>7}{'ret1':>7}{'drop/s':>9}{'z':>6}{'heat' if heat else '':>6}\n")
    for s in row["scenes"]:
        w(f"{s['scene_id']:<6}{str(s['beat'])[:25]:<26}{s['t0']:>7.2f}{s['t1']:>7.2f}{s['ret0']:>7.3f}{s['ret1']:>7.3f}"
          f"{s['drop_per_s']:>9.4f}{(s['z'] if s['z'] is not None else float('nan')):>6.2f}"
          f"{(s.get('heat_mean') or 0):>6.2f}\n" if heat else
          f"{s['scene_id']:<6}{str(s['beat'])[:25]:<26}{s['t0']:>7.2f}{s['t1']:>7.2f}{s['ret0']:>7.3f}{s['ret1']:>7.3f}"
          f"{s['drop_per_s']:>9.4f}{(s['z'] if s['z'] is not None else float('nan')):>6.2f}\n")
    w(f"head (0-{row['head']['t1']}s, not ranked): {row['head']['ret0']:.3f} -> {row['head']['ret1']:.3f}; "
      f"tail end spike {row['tail']['end_spike']:+.3f}\n")
    for i, d in enumerate(row["top_drops"], 1):
        w(f"DROP {i}: t={d['t']:.2f}s scene {d['scene_id']} [{d['beat']}] fall {d['drop']:.3f} ({d['drop_per_s']:.4f}/s)\n"
          f"   line: {d['line']!r}\n   caption on screen: {d['caption']!r}\n")
    for i, p in enumerate(row.get("top_peaks", []), 1):
        w(f"PEAK {i}: t={p['t']:.2f}s scene {p['scene_id']} [{p['beat']}] value {p['value']:.3f}\n")
    w(f"summary: {json.dumps(row['summary'])}\n")


def run_own(slug: str, window: str, platform: str, curve_file: str | None, episode_dir: str | None) -> dict | None:
    bm = bmap.load(slug, episode_dir)
    post_key = f"{slug}:{platform}"
    if curve_file:
        c = load_curve_file(curve_file)
        m = {"retention": c.get("retention"), "duration_s": c.get("duration_s"), "external_id": c.get("video_id"),
             "dry_run": c.get("synthetic", False)}
    else:
        m = latest_metrics(post_key, window)
        if not m:
            return None
    D = float(m.get("duration_s") or bm["duration_s"])
    ts, ys, rel = curve_from_retention(m["retention"], D)
    res = align(bm, ts, ys, rel, "retention", D)
    return {"v": 1, "at": iso(now_utc()), "kind": "own", "post_key": post_key, "video_id": m.get("external_id"),
            "slug": slug, "window": window, "beatmap_derived": bm.get("derived", False),
            "synthetic": bool(m.get("dry_run")), **res}


def run_source(video_id: str, curve_file: str | None) -> dict | None:
    if curve_file:
        hm = load_curve_file(curve_file)
    else:
        hm = read_json(dpath("heatmaps", f"{video_id}.json"))
    if not hm or not hm.get("points"):
        return None
    bm = bmap.source_beatmap(video_id, hm.get("duration_s"))
    ts, ys = curve_from_heatmap(hm["points"])
    res = align(bm, ts, ys, None, "heatmap", hm.get("duration_s") or bm["duration_s"])
    return {"v": 1, "at": iso(now_utc()), "kind": "source", "post_key": None, "video_id": video_id, "slug": None,
            "window": None, "beatmap_derived": True, "beats_from": bm["derived_from"], "lines_from": bm["lines_from"],
            "synthetic": bool(hm.get("synthetic")), **res}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.analytics.align", description=__doc__.split("\n\n")[0])
    ap.add_argument("slug", nargs="?")
    ap.add_argument("--source", metavar="VIDEO_ID")
    ap.add_argument("--window", default="7d")
    ap.add_argument("--platform", default="youtube")
    ap.add_argument("--curve", metavar="FILE", help="curve JSON instead of the ledgers (tests/proofs)")
    ap.add_argument("--episode-dir")
    ap.add_argument("--no-write", action="store_true", help="print only; do not append data/alignments.jsonl")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if bool(a.slug) == bool(a.source):
        ap.print_usage(sys.stderr)
        return EXIT_USAGE
    row = run_source(a.source, a.curve) if a.source else run_own(a.slug, a.window, a.platform, a.curve, a.episode_dir)
    if row is None:
        print(f"nothing to align: no {'heatmap' if a.source else 'retention curve'} yet", file=sys.stderr)
        return EXIT_NOTHING
    if a.json:
        print(json.dumps(row, indent=1, ensure_ascii=False))
    else:
        print_table(row)
    if not a.no_write and not row.get("synthetic"):
        jsonl_append(dpath("alignments.jsonl"), row)
        if row["kind"] == "own":
            write_json_atomic(rpath("out", row["slug"], "analytics", f"align-{row['window']}-{a.platform}.json"), row)
        print(f"wrote data/alignments.jsonl ({row['kind']})", file=sys.stderr)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
