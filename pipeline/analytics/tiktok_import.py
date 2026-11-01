"""TikTok metrics import (manual; there is no TikTok analytics API in this design). See TIKTOK_IMPORT.md.

  python -m pipeline.analytics.tiktok_import <file.csv> [--post-key K] [--source tiktok_csv|tiktok_screenshot]
  python -m pipeline.analytics.tiktok_import --inbox          # every *.csv in data/inbox/tiktok/, then move to done/
                                                              # (a CSV that fails to import goes to failed/)

Rows already in data/metrics.jsonl (same post_key, window, source, captured_at and raw file name) are skipped, so a
re-import never duplicates metrics.

CSV header (required): tiktok_url_or_id,captured_at,views,likes,comments,shares,saves,avg_watch_s,full_watch_pct,
new_followers,retention   (retention optional: "s:pct;s:pct;...", e.g. "0:100;3:71;10:48;30:22").
"""
from __future__ import annotations

import argparse
import csv
import os
import re
import shutil
import sys

from ._common import (EXIT_FAIL, EXIT_OK, EXIT_USAGE, dpath, iso, jsonl_append, jsonl_latest, jsonl_read, now_utc,
                      parse)
from .collect import derive

COLUMNS = ["tiktok_url_or_id", "captured_at", "views", "likes", "comments", "shares", "saves", "avg_watch_s",
           "full_watch_pct", "new_followers", "retention"]


def tiktok_id(s: str) -> str:
    m = re.search(r"/video/(\d+)", s or "")
    return m.group(1) if m else (s or "").strip()


def _num(v, cast=float):
    v = (v or "").strip().replace(",", "")
    if not v:
        return None
    mult = 1
    if v[-1] in "kKmM":  # TikTok Studio shows 12.3K
        mult = 1000 if v[-1] in "kK" else 1_000_000
        v = v[:-1]
    return cast(float(v.rstrip("%")) * mult)


def parse_retention(s: str, duration_s: float | None) -> dict | None:
    if not s or not s.strip() or not duration_s:
        return None
    pts = []
    for part in s.split(";"):
        if ":" in part:
            t, p = part.split(":", 1)
            pts.append((float(t), float(p.rstrip("%")) / 100))
    pts.sort()
    if len(pts) < 2:
        return None
    return {"x": [round(min(t / duration_s, 1.0), 4) for t, _ in pts], "watch_ratio": [round(p, 4) for _, p in pts]}


def window_for(age_h: float) -> str:
    if age_h < 96:
        return "48h"
    if age_h < 20 * 24:
        return "7d"
    return "28d"


def find_post(posts: dict, ident: str) -> dict | None:
    tid = tiktok_id(ident)
    for p in posts.values():
        if p.get("platform") != "tiktok":
            continue
        if tid and (p.get("external_id") == tid or tid in (p.get("external_url") or "")):
            return p
    return None


def dedupe_key(row: dict) -> tuple:
    return (row.get("post_key"), row.get("window"), row.get("source"), row.get("captured_at"),
            os.path.basename(row.get("raw_file") or ""))


def import_csv(path: str, post_key: str | None = None, source: str = "tiktok_csv") -> list[dict]:
    posts = jsonl_latest(dpath("posts.jsonl"), "post_key")
    rows = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        rd = csv.DictReader(f)
        hdr = [h.strip() for h in (rd.fieldnames or [])]
        miss = [c for c in COLUMNS[:-1] if c not in hdr]
        if miss:
            raise ValueError(f"{path}: missing CSV columns {miss} (header is required, see TIKTOK_IMPORT.md)")
        for n, r in enumerate(rd, 2):
            r = {k.strip(): (v or "") for k, v in r.items() if k}
            post = posts.get(post_key) if post_key else find_post(posts, r["tiktok_url_or_id"])
            if not post:
                raise ValueError(f"{path}:{n}: no tiktok post in data/posts.jsonl for {r['tiktok_url_or_id']!r} "
                                 f"(pass --post-key, or record it with pipeline.publish.post --record-manual)")
            cap = parse(r["captured_at"]) if r.get("captured_at") else now_utc()
            age_h = (cap - parse(post["published_at"])).total_seconds() / 3600 if post.get("published_at") else None
            D = float(post.get("duration_s") or 0) or None
            ret = parse_retention(r.get("retention", ""), D)
            avg = _num(r.get("avg_watch_s"))
            row = {"v": 1, "at": iso(now_utc()), "post_key": post["post_key"], "slug": post.get("slug"),
                   "platform": "tiktok", "external_id": tiktok_id(r["tiktok_url_or_id"]) or post.get("external_id"),
                   "window": window_for(age_h) if age_h is not None else "7d",
                   "age_h": None if age_h is None else round(age_h, 1), "captured_at": iso(cap), "duration_s": D,
                   "source": source, "views": _num(r.get("views"), int), "engaged_views": None,
                   "likes": _num(r.get("likes"), int), "comments": _num(r.get("comments"), int),
                   "shares": _num(r.get("shares"), int), "saves": _num(r.get("saves"), int),
                   "subs_gained": _num(r.get("new_followers"), int), "avg_view_s": avg,
                   "avg_view_pct": round(100 * avg / D, 1) if (avg is not None and D) else None,
                   "watch_time_min": None, "reach": None, "viewed_vs_swiped_pct": None,
                   "full_watch_pct": _num(r.get("full_watch_pct")), "retention": ret,
                   "derived": derive(ret, D), "raw_file": os.path.relpath(path, dpath(".."))}
            rows.append(row)
    have = {dedupe_key(m) for m in jsonl_read(dpath("metrics.jsonl")) if str(m.get("source", "")).startswith("tiktok")}
    new = []
    for row in rows:
        k = dedupe_key(row)
        if k in have:
            continue
        have.add(k)
        jsonl_append(dpath("metrics.jsonl"), row)
        new.append(row)
    return new


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.analytics.tiktok_import")
    ap.add_argument("file", nargs="?")
    ap.add_argument("--inbox", action="store_true")
    ap.add_argument("--post-key")
    ap.add_argument("--source", default=None, choices=["tiktok_csv", "tiktok_screenshot"])
    a = ap.parse_args(argv)
    if bool(a.file) == bool(a.inbox):
        ap.print_usage(sys.stderr)
        return EXIT_USAGE
    inbox = dpath("inbox", "tiktok")
    files = [a.file] if a.file else sorted(os.path.join(inbox, f) for f in os.listdir(inbox) if f.endswith(".csv")) \
        if os.path.isdir(inbox) else []
    rc = EXIT_OK
    for f in files:
        src = a.source or ("tiktok_screenshot" if ".screenshot." in os.path.basename(f) else "tiktok_csv")
        try:
            rows = import_csv(f, a.post_key, src)
        except (ValueError, KeyError) as e:
            print(f"error: {e}", file=sys.stderr)
            rc = EXIT_FAIL
            if a.inbox:  # never re-tried daily: the human fixes it and drops it again
                bad = os.path.join(inbox, "failed")
                os.makedirs(bad, exist_ok=True)
                shutil.move(f, os.path.join(bad, os.path.basename(f)))
            continue
        print(f"{f}: {len(rows)} new rows -> data/metrics.jsonl")
        if a.inbox:
            done = os.path.join(inbox, "done")
            os.makedirs(done, exist_ok=True)
            shutil.move(f, os.path.join(done, os.path.basename(f)))
    if a.inbox and not files:
        print("inbox empty")
    return rc


if __name__ == "__main__":
    sys.exit(main())
