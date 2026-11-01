"""Metrics collection (OPERATOR_DESIGN 9.1-9.3, row shape 5.11).

  python -m pipeline.analytics.collect --due [--list] [--dry-run]
  python -m pipeline.analytics.collect --post-key <slug>:<platform> --window 48h|7d [--dry-run]

`--due` reads `data/posts.jsonl` (latest row per post_key, status `published`, not dry-run) and the windows in
`data/operator/config.json` (`metrics_windows_h`, default [48, 168]). A (post, window) is due once the post is that
old and has no real metrics row for the window yet. A YouTube row whose Analytics part was still empty
(`pending`) is retried every 12 h until window + 48 h (Analytics lags 1-3 days). TikTok has no API here: due
TikTok windows are listed as "manual" (the human drops a CSV/screenshot, see TIKTOK_IMPORT.md).

Credentials missing -> `DRY-RUN: missing <NAMES> in ~/studio/.env`, exit 0. With `--post-key` a dry run appends a
synthetic row (`dry_run: true`, `source: synthetic`, the API requests it would make) so the downstream chain can be
exercised; with `--due` a dry run only lists (no rows, so nothing fires twice). Synthetic rows never count for
experiments, learning or the kill rule.
"""
from __future__ import annotations

import argparse
import json
import sys

from . import beatmap as bmap
from . import instagram, synthetic, youtube
from ._common import (DependencyError, EXIT_DEP, EXIT_FAIL, EXIT_OK, EXIT_USAGE, config, dpath, iso, is_real,
                      jsonl_append, jsonl_latest, jsonl_read, load_env, now_utc, parse, window_hours, window_label)
from .align import interp

RETRY_PENDING_H = 12
PENDING_GRACE_H = 48


def derive(retention: dict | None, duration_s: float | None) -> dict | None:
    """hold_3s = watch ratio at 3 s; hold_50pct at x = 0.5; completion at x = 0.97 (before the loop end spike)."""
    if not retention or not duration_s:
        return None
    xs, ys = retention["x"], retention["watch_ratio"]
    return {"hold_3s": round(interp(xs, ys, 3.0 / duration_s), 4), "hold_50pct": round(interp(xs, ys, 0.5), 4),
            "completion": round(interp(xs, ys, 0.97), 4)}


def published_posts() -> list[dict]:
    posts = jsonl_latest(dpath("posts.jsonl"), "post_key").values()
    return [p for p in posts if p.get("status") == "published" and p.get("published_at") and is_real(p)]


def due(now=None, windows_h: list[int] | None = None) -> list[dict]:
    now = now or now_utc()
    windows_h = windows_h or config().get("metrics_windows_h", [48, 168])
    rows = [r for r in jsonl_read(dpath("metrics.jsonl")) if is_real(r)]
    out = []
    for p in published_posts():
        age_h = (now - parse(p["published_at"])).total_seconds() / 3600
        for w in windows_h:
            if age_h < w:
                continue
            label = window_label(w)
            have = [r for r in rows if r.get("post_key") == p["post_key"] and r.get("window") == label]
            last = have[-1] if have else None
            if last and not last.get("pending"):
                continue
            if last and last.get("pending"):
                since = (now - parse(last["at"])).total_seconds() / 3600
                if age_h > w + PENDING_GRACE_H or since < RETRY_PENDING_H:
                    continue
            out.append({"post_key": p["post_key"], "platform": p["platform"], "window": label,
                        "age_h": round(age_h, 1), "manual": p["platform"] == "tiktok", "retry": bool(last)})
    return out


def _duration(post: dict) -> float:
    if post.get("duration_s"):
        return float(post["duration_s"])
    try:
        return float(bmap.load(post["slug"])["duration_s"])
    except Exception:
        return 75.0


def build_row(post: dict, window: str, part: dict, dry: bool, now=None) -> dict:
    now = now or now_utc()
    age_h = (now - parse(post["published_at"])).total_seconds() / 3600 if post.get("published_at") else None
    D = part.pop("duration_s", None) or _duration(post)
    row = {"v": 1, "at": iso(now), "post_key": post["post_key"], "slug": post.get("slug"),
           "platform": post.get("platform"), "external_id": part.pop("external_id", None) or post.get("external_id"),
           "window": window, "age_h": None if age_h is None else round(age_h, 1), "duration_s": D}
    keys = ["source", "views", "engaged_views", "likes", "comments", "shares", "saves", "subs_gained", "avg_view_s",
            "avg_view_pct", "watch_time_min", "reach", "viewed_vs_swiped_pct", "retention"]
    for k in keys:
        row[k] = part.pop(k, None)
    row["derived"] = derive(row["retention"], D)
    row.update({k: v for k, v in part.items() if v is not None})
    if dry:
        row["dry_run"] = True
        row["status"] = "dry_run"
    return row


def synthetic_part(post: dict, window: str) -> dict:
    D = _duration(post)
    part = {"source": "synthetic", **synthetic.totals(post["post_key"], window, D), "duration_s": D}
    if post.get("platform") == "youtube":
        seed = synthetic.seed_of(post["post_key"], window)
        part["retention"] = synthetic.retention_curve(D, [(D * 0.3, 0.05), (D * 0.62, 0.04)], seed % 1000, noise=0.004)
    return part


def collect_one(post: dict, window: str, env: dict, force_dry: bool = False) -> tuple[dict | None, str | None]:
    """-> (row, dry-run reason). TikTok is never fetched here."""
    plat = post.get("platform")
    if plat == "tiktok":
        return None, "tiktok is manual (TIKTOK_IMPORT.md)"
    miss = youtube.missing(env) if plat == "youtube" else instagram.missing(env)
    if force_dry or miss:
        reqs = (youtube.requests_for(post.get("external_id") or "<external_id>", post.get("published_at") or iso(now_utc()))
                if plat == "youtube" else instagram.requests_for(post, env))
        part = synthetic_part(post, window)
        part["requests"] = reqs
        reason = f"DRY-RUN: missing {', '.join(miss)} in ~/studio/.env" if miss else "DRY-RUN: forced"
        return build_row(post, window, part, True), reason
    if plat == "youtube":
        if not post.get("external_id"):
            return build_row(post, window, {"source": "yt_data", "error": "no external_id yet", "pending": ["external_id"]},
                             False), None
        part = youtube.fetch(post["external_id"], post["published_at"], env)
    else:
        part = instagram.fetch(post, env)
    return build_row(post, window, part, False), None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.analytics.collect")
    ap.add_argument("--due", action="store_true")
    ap.add_argument("--list", action="store_true", help="with --due: list only")
    ap.add_argument("--post-key")
    ap.add_argument("--window", default="48h")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    if bool(a.due) == bool(a.post_key):
        ap.print_usage(sys.stderr)
        return EXIT_USAGE
    window_hours(a.window)
    env = load_env()
    if a.due:
        items = due()
        miss = sorted(set(youtube.missing(env) + instagram.missing(env)))
        dry = a.dry_run or bool(miss)
        if dry and miss:
            print(f"DRY-RUN: missing {', '.join(miss)} in ~/studio/.env")
        print(f"{len(items)} due")
        for it in items:
            print(f"  {it['post_key']} {it['window']} age {it['age_h']} h" + (" MANUAL (tiktok)" if it["manual"] else "")
                  + (" retry" if it["retry"] else ""))
        if a.list or dry:
            if dry and items:
                print("dry-run: would fetch the above; nothing written")
            return EXIT_OK
        posts = jsonl_latest(dpath("posts.jsonl"), "post_key")
        rc = EXIT_OK
        for it in items:
            if it["manual"]:
                continue
            try:
                row, _ = collect_one(posts[it["post_key"]], it["window"], env)
            except DependencyError as e:
                print(f"dependency: {e}", file=sys.stderr)
                return EXIT_DEP
            except Exception as e:  # one bad post never blocks the rest
                print(f"error {it['post_key']} {it['window']}: {e}", file=sys.stderr)
                rc = EXIT_FAIL
                continue
            if row:
                jsonl_append(dpath("metrics.jsonl"), row)
                print(f"wrote {row['post_key']} {row['window']} views={row['views']} pending={row.get('pending')}")
        return rc
    posts = jsonl_latest(dpath("posts.jsonl"), "post_key")
    post = posts.get(a.post_key)
    if post is None:
        slug, _, plat = a.post_key.rpartition(":")
        post = {"post_key": a.post_key, "slug": slug, "platform": plat, "published_at": iso(now_utc()), "dry_run": True}
        a.dry_run = True
        print(f"note: {a.post_key} not in data/posts.jsonl; synthetic dry run")
    try:
        row, reason = collect_one(post, a.window, env, a.dry_run)
    except DependencyError as e:
        print(f"dependency: {e}", file=sys.stderr)
        return EXIT_DEP
    if reason:
        print(reason)
    if row is None:
        print("nothing to fetch")
        return EXIT_OK
    jsonl_append(dpath("metrics.jsonl"), row)
    shown = {k: v for k, v in row.items() if k not in ("retention", "requests", "raw")}
    print(json.dumps(shown, ensure_ascii=False))
    if row.get("retention"):
        print(f"retention: {len(row['retention']['x'])} points")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
