"""YouTube "Most replayed" heatmap puller (OPERATOR_DESIGN 9.5, file shape 5.12).

  python -m pipeline.analytics.heatmap <video_id|url> [--force] [--align]
  python -m pipeline.analytics.heatmap --from-daily 20 [--align]      # weekly: top explainer outliers

Runs `yt-dlp -J --skip-download` (metadata only, never media) on the Spark, one process at a time under
flock("ytdlp"), `nice -n 10`, with `--cookies $YTDLP_COOKIES_FILE` if that is set in ~/studio/.env. On the Mac
(no STUDIO_LOCAL, SPARK_HOST != local) the same command runs on the Spark over `ssh $SPARK_HOST` (BRIEF: yt-dlp
only on the Spark).

Status values: ok (heatmap points present) | none (the video has no Most-replayed graph yet: YouTube shows it only
once enough viewers rewatched; retried after 2 days) | blocked (bot check: no retry for 7 days) | error.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shlex
import subprocess
import sys
from datetime import timedelta

from ._common import (EXIT_FAIL, EXIT_OK, EXIT_USAGE, dpath, env_or_default, flock, iso, jsonl_read, load_env,
                      now_utc, parse, read_json, redact, rpath, write_json_atomic)

RETRY_AFTER = {"blocked": timedelta(days=7), "none": timedelta(days=2), "error": timedelta(hours=12),
               "ok": timedelta(days=7)}
BLOCK_PAT = re.compile(r"confirm you.?re not a bot|Sign in to confirm|HTTP Error 429|This helps protect our community", re.I)


def video_id_of(s: str) -> str:
    m = re.search(r"(?:v=|youtu\.be/|shorts/)([\w-]{11})", s)
    return m.group(1) if m else s.strip()


def _local_mode() -> bool:
    return (os.environ.get("STUDIO_LOCAL") == "1" or os.environ.get("SPARK_HOST") == "local"
            or platform.system() != "Darwin")


def ytdlp_args(video_id: str, env: dict) -> tuple[str, list[str], str | None]:
    """(yt-dlp binary as configured, args, cookies path as configured). Paths may start with ~ (expanded where run)."""
    ytdlp = env_or_default(env, "YTDLP_BIN", "~/.local/bin/yt-dlp")
    # no --no-warnings: the bot-check / 429 warnings are how a partial (heatmap-less) answer is told apart from a
    # video that really has no Most-replayed graph
    args = ["-J", "--skip-download", "--ignore-no-formats-error", "--no-playlist"]
    return ytdlp, args + [f"https://www.youtube.com/watch?v={video_id}"], env.get("YTDLP_COOKIES_FILE") or None


def _remote_path(p: str) -> str:
    # ~ must expand on the Spark, so quote everything after it
    return '"$HOME"' + shlex.quote(p[1:]) if p.startswith("~") else shlex.quote(p)


def run_ytdlp(video_id: str, env: dict, timeout_s: int = 180) -> tuple[int, str, str]:
    ytdlp, args, cookies = ytdlp_args(video_id, env)
    if _local_mode():
        cmd = [os.path.expanduser(ytdlp)] + (["--cookies", os.path.expanduser(cookies)] if cookies else []) + args
        with flock("ytdlp", timeout_s=900):
            p = subprocess.run(["nice", "-n", "10", *cmd], capture_output=True, text=True, timeout=timeout_s)
        return p.returncode, p.stdout, p.stderr
    # Mac: run on the Spark. Cookies (if any) are a Spark-side path from the Spark's ~/studio/.env, so the Mac never
    # passes one; the Spark copy of this module reads its own env when run there.
    host = os.environ.get("SPARK_HOST", "dgx-spark")
    remote = ("mkdir -p ~/studio/locks && flock -w 900 ~/studio/locks/ytdlp.lock nice -n 10 "
              + _remote_path(ytdlp) + " " + " ".join(shlex.quote(x) for x in args))
    p = subprocess.run(["ssh", host, remote], capture_output=True, text=True, timeout=timeout_s + 60)
    return p.returncode, p.stdout, p.stderr


def parse_info(video_id: str, rc: int, out: str, err: str) -> dict:
    row = {"v": 1, "video_id": video_id, "fetched_at": iso(now_utc()), "duration_s": None, "status": "error",
           "points": [], "error": None}
    info = None
    if out.strip():
        try:
            info = json.loads(out)
        except json.JSONDecodeError:
            info = None
    if info is None:
        tail = redact((err or "").strip().splitlines()[-1] if (err or "").strip() else f"yt-dlp exit {rc}")
        row["status"] = "blocked" if BLOCK_PAT.search(err or "") else "error"
        row["error"] = tail[:300]
        return row
    row["duration_s"] = info.get("duration")
    row["title"] = info.get("title")
    row["channel"] = info.get("channel")
    row["view_count"] = info.get("view_count")
    row["chapters"] = [{"t": c.get("start_time"), "title": c.get("title")} for c in (info.get("chapters") or [])]
    hm = info.get("heatmap") or []
    row["points"] = [{"start": round(float(p["start_time"]), 3), "end": round(float(p["end_time"]), 3),
                      "value": round(float(p["value"]), 5)} for p in hm if "start_time" in p]
    block = BLOCK_PAT.search(err or "")
    if row["points"]:
        row["status"] = "ok"
    elif block or row["duration_s"] is None:
        # --ignore-no-formats-error lets yt-dlp print a partial info dict when the watch page was refused (429 /
        # bot check): no heatmap there means nothing, so this is "blocked", not "none"
        row["status"] = "blocked" if block else "error"
        line = next((l for l in (err or "").splitlines() if BLOCK_PAT.search(l)), "partial info (no duration)")
        row["error"] = redact(line.strip())[:300]
    else:
        row["status"] = "none"
        row["error"] = "no heatmap in yt-dlp info (YouTube shows Most replayed only once enough viewers rewatch)"
    return row


def fetch(video: str, force: bool = False, env: dict | None = None) -> dict:
    vid = video_id_of(video)
    path = dpath("heatmaps", f"{vid}.json")
    old = read_json(path)
    if old and not force:
        age = now_utc() - parse(old["fetched_at"])
        if age < RETRY_AFTER.get(old.get("status"), timedelta(0)):
            old["_cached"] = True
            return old
    env = env if env is not None else load_env()
    try:
        rc, out, err = run_ytdlp(vid, env)
    except subprocess.TimeoutExpired:
        rc, out, err = 124, "", "yt-dlp timed out"
    row = parse_info(vid, rc, out, err)
    if old and old.get("status") == "ok" and row["status"] != "ok":
        row["previous_ok_at"] = old["fetched_at"]
        row["points"] = old["points"]  # keep the last good curve, but report the new status
        row["status_points"] = "previous"
    write_json_atomic(path, row)
    return row


def daily_top(n: int) -> list[str]:
    """Top-n explainer YouTube outliers from research/library.jsonl (Spark-owned research pull)."""
    rows = [r for r in jsonl_read(rpath("research", "library.jsonl"))
            if r.get("type") == "video" and r.get("niche") == "explainer" and r.get("platform", "youtube") == "youtube"]
    best: dict[str, dict] = {}
    for r in rows:
        vid = r.get("id") or r.get("video_id")
        if vid:
            best[vid] = r
    ranked = sorted(best.values(), key=lambda r: (-(r.get("outlier_score") or 0), str(r.get("id"))))
    return [r.get("id") or r.get("video_id") for r in ranked[:n]]


def summary_line(row: dict) -> str:
    pts = row.get("points") or []
    s = f"{row['video_id']}: status={row['status']} duration={row.get('duration_s')} points={len(pts)}"
    if pts:
        top = max(pts, key=lambda p: p["value"])
        s += f" peak={top['value']:.2f}@{top['start']:.0f}-{top['end']:.0f}s"
    if row.get("_cached"):
        s += " (cached)"
    if row.get("error") and row["status"] != "ok":
        s += f" note={row['error']}"
    return s


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.analytics.heatmap")
    ap.add_argument("video", nargs="?")
    ap.add_argument("--from-daily", type=int, metavar="N")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--align", action="store_true", help="also run align --source when points exist")
    a = ap.parse_args(argv)
    if bool(a.video) == bool(a.from_daily):
        ap.print_usage(sys.stderr)
        return EXIT_USAGE
    vids = [a.video] if a.video else daily_top(a.from_daily)
    rc = EXIT_OK
    for v in vids:
        row = fetch(v, a.force)
        print(summary_line(row))
        if row["status"] == "error":
            rc = EXIT_FAIL
        if a.align and row.get("points"):
            from . import align

            try:
                align.main(["--source", row["video_id"]])
            except FileNotFoundError as e:
                print(f"  align skipped: {e}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
