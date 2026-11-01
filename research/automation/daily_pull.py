#!/usr/bin/env python3
"""Daily research pull: channel listings -> outlier scores -> research/library.jsonl.

Runs on the DGX Spark from cron (scripts/research_daily.sh, 06:00 America/Chicago).
Metadata only: `yt-dlp --flat-playlist -J` per channel tab. Never downloads media,
never calls an LLM, never touches the GPU. Python stdlib only.

Per run it appends to research/library.jsonl (relative to the repo root):
  {"type": "video", ...}    one row per notable upload (first seen, score >= 1.5, or top 3 of its tab;
                            --rows all = every listed upload; the first run on 2026-11-01 wrote all)
  {"type": "channel", ...}  one summary row per channel tab (median, top outlier, errors)
  {"type": "run", ...}      one row at the end (counts, duration, errors)
and writes research/daily/<YYYY-MM-DD>.md + research/daily/latest.md (top outliers, new ones flagged).
State for first_seen / view deltas lives in research/library.state.json.

outlier_score = views / median(views of the same channel + same format), the same
definition as research/library (INDEX.md). The median pool excludes uploads younger
than --min-age-days (by TikTok timestamp, or by our own first_seen for YouTube, whose flat
listings carry no dates) unless that leaves fewer than 5 uploads.

usage: python3 research/automation/daily_pull.py [--limit 30] [--only NAME] [--dry-run]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import statistics
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
YTDLP = os.environ.get("YTDLP", str(Path.home() / ".local/bin/yt-dlp"))


def utcnow() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def run_ytdlp(url: str, limit: int, timeout: int) -> tuple[dict | None, str | None]:
    cmd = [YTDLP, "--flat-playlist", "-J", "--playlist-end", str(limit), "--no-warnings",
           "--socket-timeout", "30", "--ignore-no-formats-error", url]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, f"timeout after {timeout}s"
    except FileNotFoundError:
        return None, f"yt-dlp not found at {YTDLP}"
    if p.returncode != 0 or not p.stdout.strip():
        err = (p.stderr or "").strip().splitlines()
        return None, (err[-1] if err else f"exit {p.returncode}")[:300]
    try:
        return json.loads(p.stdout), None
    except json.JSONDecodeError as e:
        return None, f"bad json: {e}"


def tab_url(ch: dict, tab: str) -> str:
    if ch["platform"] == "youtube":
        return ch["url"].rstrip("/") + "/" + tab
    return ch["url"]


def video_url(ch: dict, vid: str, tab: str) -> str:
    if ch["platform"] == "tiktok":
        return f"{ch['url']}/video/{vid}"
    return f"https://www.youtube.com/shorts/{vid}" if tab == "shorts" else f"https://www.youtube.com/watch?v={vid}"


def fmt_views(n) -> str:
    if n is None:
        return "-"
    n = float(n)
    for unit, d in (("B", 1e9), ("M", 1e6), ("K", 1e3)):
        if n >= d:
            return f"{n / d:.1f}{unit}"
    return str(int(n))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--channels", default=str(ROOT / "research/automation/channels.json"))
    ap.add_argument("--out", default=str(ROOT / "research/library.jsonl"))
    ap.add_argument("--state", default=str(ROOT / "research/library.state.json"))
    ap.add_argument("--report-dir", default=str(ROOT / "research/daily"))
    ap.add_argument("--limit", type=int, default=30, help="newest uploads per channel tab")
    ap.add_argument("--min-age-days", type=float, default=3.0)
    ap.add_argument("--sleep", type=float, default=2.0, help="pause between yt-dlp calls")
    ap.add_argument("--timeout", type=int, default=240)
    ap.add_argument("--report-min-score", type=float, default=2.0)
    ap.add_argument("--rows", choices=("notable", "all"), default="notable",
                    help="video rows to append: notable = first seen, score >= --notable-score, or top 3 of its tab")
    ap.add_argument("--notable-score", type=float, default=1.5)
    ap.add_argument("--only", help="poll only channels whose name contains this (case-insensitive)")
    ap.add_argument("--dry-run", action="store_true", help="print rows, write nothing")
    a = ap.parse_args()

    t0 = time.time()
    now = utcnow()
    run_id = now.strftime("%Y-%m-%dT%H:%MZ")
    today = now.date().isoformat()
    channels = [c for c in json.load(open(a.channels))["channels"] if c.get("enabled", True)]
    if a.only:
        channels = [c for c in channels if a.only.lower() in c["name"].lower()]

    state_path = Path(a.state)
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    rows: list[dict] = []
    errors: list[str] = []
    n_calls = 0

    for ch in channels:
        for tab in ch["tabs"]:
            if n_calls:
                time.sleep(a.sleep)
            n_calls += 1
            data, err = run_ytdlp(tab_url(ch, tab), a.limit, a.timeout)
            fmt = {"videos": "long", "shorts": "short", "posts": "tiktok"}.get(tab, tab)
            base = {"run": run_id, "date": today, "niche": ch["niche"], "channel": ch["name"],
                    "channel_role": ch["role"], "platform": ch["platform"], "format": fmt}
            if err:
                # A channel without a Shorts tab is normal; record it but don't count it as a failure.
                benign = tab == "shorts" and ("does not have a shorts tab" in err.lower() or "not exist" in err.lower())
                if not benign:
                    errors.append(f"{ch['name']}/{tab}: {err}")
                rows.append({"type": "channel", **base, "url": tab_url(ch, tab), "n": 0, "error": err, "benign": benign})
                print(f"[pull] {ch['name']}/{tab}: {'no tab' if benign else 'ERROR ' + err}", file=sys.stderr)
                continue
            subs = data.get("channel_follower_count")
            # Has this channel tab been polled before? Then an unseen upload really is new (age ~0).
            tab_known = any(s.get("channel") == ch["name"] and s.get("format") == fmt for s in state.values())
            vids = []
            for e in data.get("entries") or []:
                if not e or not e.get("id"):
                    continue
                vid = str(e["id"])
                key = f"{ch['platform']}:{vid}"
                st = state.get(key, {})
                first_seen = st.get("first_seen", run_id)
                ts = e.get("timestamp") or e.get("release_timestamp")
                if ts:
                    age = (now.timestamp() - float(ts)) / 86400
                else:
                    age = None
                seen_age = (now - dt.datetime.strptime(first_seen, "%Y-%m-%dT%H:%MZ").replace(tzinfo=dt.timezone.utc)).total_seconds() / 86400
                views = e.get("view_count")
                vids.append({
                    "type": "video", **base, "id": vid, "url": video_url(ch, vid, tab),
                    "title": (e.get("title") or "").strip()[:300], "duration_s": e.get("duration"),
                    "views": views, "likes": e.get("like_count"), "comments": e.get("comment_count"),
                    "upload_ts": int(ts) if ts else None,
                    "upload_date": dt.datetime.fromtimestamp(float(ts), dt.timezone.utc).date().isoformat() if ts else None,
                    "age_days": round(age, 2) if age is not None else None,
                    "first_seen": first_seen, "new": key not in state,
                    "views_prev": st.get("views"),
                    "views_delta": (views - st["views"]) if (views is not None and st.get("views") is not None) else None,
                    "subs": subs,
                    "_pool_age": age if age is not None else (seen_age if (key in state or tab_known) else None),
                })
            with_views = [v for v in vids if v["views"] is not None]
            # Median pool: uploads at least min-age old. Unknown age (first poll of a YouTube tab) counts as old.
            pool = [v["views"] for v in with_views if v["_pool_age"] is None or v["_pool_age"] >= a.min_age_days]
            pool_note = "aged"
            if len(pool) < 5:
                pool = [v["views"] for v in with_views]
                pool_note = "all"
            med = statistics.median(pool) if pool else None
            for v in vids:
                v.pop("_pool_age")
                v["channel_median_views"] = med
                v["median_pool_n"] = len(pool)
                v["outlier_score"] = round(v["views"] / med, 2) if (med and v["views"] is not None) else None
            ranked = sorted([v for v in vids if v["outlier_score"] is not None], key=lambda v: -v["outlier_score"])
            for i, v in enumerate(ranked, 1):
                v["rank"] = i
            rows.extend(vids)
            top = ranked[0] if ranked else None
            rows.append({"type": "channel", **base, "url": tab_url(ch, tab), "subs": subs, "n": len(vids),
                         "median_views": med, "median_pool": pool_note, "median_pool_n": len(pool),
                         "top_id": top["id"] if top else None, "top_score": top["outlier_score"] if top else None,
                         "n_new": sum(v["new"] for v in vids), "error": None})
            print(f"[pull] {ch['name']}/{tab}: {len(vids)} uploads, median {fmt_views(med)}, "
                  f"top {top['outlier_score'] if top else '-'}x, new {sum(v['new'] for v in vids)}", file=sys.stderr)

    videos = [r for r in rows if r["type"] == "video"]
    run_row = {"type": "run", "run": run_id, "date": today, "channels": len(channels), "calls": n_calls,
               "videos": len(videos), "new": sum(v["new"] for v in videos), "errors": errors,
               "seconds": round(time.time() - t0, 1), "limit": a.limit}
    rows.append(run_row)

    if a.dry_run:
        for r in rows:
            print(json.dumps(r, ensure_ascii=False))
        return 0

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    def keep(r: dict) -> bool:  # keeps the file small: ~100-200 video rows/day instead of ~1,000
        if r["type"] != "video" or a.rows == "all":
            return True
        return r["new"] or (r.get("outlier_score") or 0) >= a.notable_score or (r.get("rank") or 99) <= 3

    with out.open("a", encoding="utf-8") as f:
        for r in rows:
            if keep(r):
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

    for v in videos:
        key = f"{v['platform']}:{v['id']}"
        s = state.setdefault(key, {"first_seen": v["first_seen"]})
        s.update({"views": v["views"], "last_seen": run_id, "channel": v["channel"], "niche": v["niche"],
                  "format": v["format"]})
    tmp = state_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False))
    tmp.replace(state_path)

    write_report(Path(a.report_dir), today, run_row, rows, a.report_min_score)
    print(f"[pull] done: {len(videos)} video rows, {run_row['new']} new, {len(errors)} errors, "
          f"{run_row['seconds']} s -> {out}", file=sys.stderr)
    return 0 if len(errors) < max(3, n_calls // 2) else 1


def write_report(d: Path, today: str, run_row: dict, rows: list[dict], min_score: float) -> None:
    d.mkdir(parents=True, exist_ok=True)
    vids = [r for r in rows if r["type"] == "video" and r.get("outlier_score") is not None]
    L = [f"# Daily outliers {today}", "",
         f"Run {run_row['run']}: {run_row['channels']} channels, {run_row['videos']} uploads listed, "
         f"{run_row['new']} first seen today, {len(run_row['errors'])} errors, {run_row['seconds']} s. "
         f"Score = views / channel median for the same format. Metadata only (yt-dlp --flat-playlist).", ""]
    for niche in ("explainer", "horror", "whatif"):
        top = sorted([v for v in vids if v["niche"] == niche and v["outlier_score"] >= min_score],
                     key=lambda v: -v["outlier_score"])[:15]
        L += [f"## {niche} (score >= {min_score})", ""]
        if not top:
            L += ["None today.", ""]
            continue
        L += ["| Score | Views | +views | Fmt | Channel | Title | New |", "|---|---|---|---|---|---|---|"]
        for v in top:
            title = (v["title"] or v["id"]).replace("|", "/")[:80]
            L.append(f"| **{v['outlier_score']}** | {fmt_views(v['views'])} | {fmt_views(v['views_delta']) if v['views_delta'] else '-'} "
                     f"| {v['format']} | {v['channel']} | [{title}]({v['url']}) | {'NEW' if v['new'] else ''} |")
        L.append("")
    if run_row["errors"]:
        L += ["## Errors", ""] + [f"- {e}" for e in run_row["errors"]] + [""]
    text = "\n".join(L)
    (d / f"{today}.md").write_text(text)
    (d / "latest.md").write_text(text)


if __name__ == "__main__":
    sys.exit(main())
