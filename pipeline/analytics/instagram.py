"""Instagram Reels collector (Instagram Graph API, "Instagram API with Facebook Login" host by default).
See API_NOTES.md for verified vs assumed metric names.

  python -m pipeline.analytics.instagram fetch --post-key K [--dry-run]

Env (`~/studio/.env`): IG_USER_ID, IG_ACCESS_TOKEN (long-lived; instagram_basic + instagram_manage_insights),
META_GRAPH_VERSION (default v26.0, the version the docs showed on 2026-11-01), IG_GRAPH_HOST (default
graph.facebook.com; graph.instagram.com for an "Instagram Login" token). The token goes in the Authorization
header, never in a URL.

Insights metric names change between Graph versions, so each metric is requested on its own: what returns is kept,
what errors is recorded under raw.errors and never fails the row (if every metric errors, the row is an error row
with `pending`, so it is retried).

posts.jsonl `external_id` for Instagram is the permalink shortcode (Buffer's externalLink, record-manual), not a Graph
media id. Only an all-digit external_id is used as a media id; anything else is resolved through /{ig-user-id}/media
(shortcode or permalink match) and the numeric id is stored on the metrics row (`external_id`, with
`external_shortcode`).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import timedelta

from . import http
from ._common import DependencyError, EXIT_DEP, EXIT_OK, env_or_default, load_env, parse

REQUIRED_ENV = ["IG_USER_ID", "IG_ACCESS_TOKEN"]
# Reels metrics listed on the IG Media Insights reference (2026-11-01, v26.0)
REELS_METRICS = ["views", "reach", "likes", "comments", "shares", "saved", "total_interactions",
                 "ig_reels_avg_watch_time", "ig_reels_video_view_total_time", "reels_skip_rate"]
MEDIA_FIELDS = "id,shortcode,permalink,timestamp,caption,media_product_type,media_type"
SHORTCODE_RX = re.compile(r"instagram\.com/(?:reel|reels|p)/([\w-]+)")


def is_media_id(x) -> bool:
    return bool(x) and str(x).isdigit()


def shortcode_of(post: dict) -> str | None:
    x = post.get("external_id")
    if x and not is_media_id(x):
        return str(x)
    m = SHORTCODE_RX.search(post.get("external_url") or "")
    return m.group(1) if m else None


def missing(env: dict) -> list[str]:
    return [n for n in REQUIRED_ENV if not env.get(n)]


class Client:
    def __init__(self, env: dict):
        self.env = env
        self.base = f"https://{env_or_default(env, 'IG_GRAPH_HOST', 'graph.facebook.com')}/" \
                    f"{env_or_default(env, 'META_GRAPH_VERSION', 'v26.0')}"
        self.hdr = {"Authorization": f"Bearer {env['IG_ACCESS_TOKEN']}"}

    def get(self, path: str, params: dict) -> dict:
        return http.request("GET", f"{self.base}/{path}", params=params, headers=self.hdr)

    def recent_media(self, pages: int = 2) -> list[dict]:
        out, after = [], None
        for _ in range(pages):
            p = {"fields": MEDIA_FIELDS, "limit": 50}
            if after:
                p["after"] = after
            r = self.get(f"{self.env['IG_USER_ID']}/media", p)
            out += r.get("data", [])
            after = (r.get("paging") or {}).get("cursors", {}).get("after")
            if not after or not (r.get("paging") or {}).get("next"):
                break
        return out

    def insight(self, media_id: str, metric: str):
        r = self.get(f"{media_id}/insights", {"metric": metric})
        return insight_value(r, metric)


def insight_value(r: dict, metric: str):
    for d in r.get("data", []):
        if d.get("name") != metric:
            continue
        if d.get("values"):
            return d["values"][0].get("value")
        if d.get("total_value"):
            return d["total_value"].get("value")
    return None


def _norm(s: str) -> str:
    return re.sub(r"\W+", " ", (s or "").lower()).strip()


def match_media(media: list[dict], post: dict) -> dict | None:
    """Find our Reel: permalink == external_url, else timestamp within +-15 min of published_at and the same caption
    start (first 20 normalised chars, at least 10)."""
    url = (post.get("external_url") or "").rstrip("/")
    code = shortcode_of(post)
    for m in media:
        if url and (m.get("permalink") or "").rstrip("/") == url:
            return m
        if code and (m.get("shortcode") == code or f"/{code}/" in (m.get("permalink") or "") + "/"):
            return m
    if not post.get("published_at"):
        return None
    pub = parse(post["published_at"])
    want = _norm(post.get("caption") or post.get("title") or "")
    best = None
    for m in media:
        if m.get("media_product_type") not in (None, "REELS"):
            continue
        try:
            dt = abs(parse(m["timestamp"].replace("+0000", "+00:00")) - pub)
        except (KeyError, ValueError):
            continue
        got = _norm(m.get("caption", ""))
        k = min(20, len(want), len(got))
        if dt <= timedelta(minutes=15) and (not want or (k >= 10 and got[:k] == want[:k])):
            if best is None or dt < best[0]:
                best = (dt, m)
    return best and best[1]


def to_row(vals: dict) -> dict:
    skip = vals.get("reels_skip_rate")
    avg_ms = vals.get("ig_reels_avg_watch_time")
    tot_ms = vals.get("ig_reels_video_view_total_time")
    return {"source": "ig_graph", "views": vals.get("views"), "engaged_views": None, "likes": vals.get("likes"),
            "comments": vals.get("comments"), "shares": vals.get("shares"), "saves": vals.get("saved"),
            "subs_gained": None,
            # ASSUMED unit: milliseconds (see API_NOTES.md)
            "avg_view_s": round(avg_ms / 1000, 2) if isinstance(avg_ms, (int, float)) else None,
            "avg_view_pct": None,
            "watch_time_min": round(tot_ms / 60000, 2) if isinstance(tot_ms, (int, float)) else None,
            "reach": vals.get("reach"),
            "viewed_vs_swiped_pct": round(100 - float(skip), 2) if isinstance(skip, (int, float)) else None,
            "retention": None}


def requests_for(post: dict, env: dict) -> list[dict]:
    base = f"https://{env_or_default(env, 'IG_GRAPH_HOST', 'graph.facebook.com')}/" \
           f"{env_or_default(env, 'META_GRAPH_VERSION', 'v26.0')}"
    mid = post.get("external_id") if is_media_id(post.get("external_id")) else "<resolved media id>"
    out = [] if is_media_id(post.get("external_id")) else [{"GET": f"{base}/{env.get('IG_USER_ID', '<IG_USER_ID>')}/media",
                                                            "fields": MEDIA_FIELDS, "limit": 50}]
    return out + [{"GET": f"{base}/{mid}/insights", "metric": m} for m in REELS_METRICS]


def fetch(post: dict, env: dict) -> dict:
    c = Client(env)
    mid = post.get("external_id")
    media = None
    if not is_media_id(mid):  # a shortcode (or nothing): resolve to the Graph media id
        media = match_media(c.recent_media(), post)
        if not media:
            return {"source": "ig_graph", "error": "media not found (no shortcode/permalink match, no timestamp+caption "
                    "match)", "retention": None, "pending": ["media_id"]}
        mid = media["id"]
    vals, errs = {}, {}
    for m in REELS_METRICS:
        try:
            vals[m] = c.insight(mid, m)
        except http.ApiError as e:
            errs[m] = str(e)[:200]
    row = to_row(vals)
    row["external_id"] = mid
    if media:
        row["external_url"] = media.get("permalink")
        row["external_shortcode"] = media.get("shortcode") or shortcode_of(post)
    row["raw"] = {"insights": vals, "errors": errs or None}
    if errs and all(vals.get(m) is None for m in REELS_METRICS):
        row["error"] = f"every insights metric failed for media {mid}"
        row["pending"] = ["insights"]
    return row


def main(argv=None) -> int:
    from ._common import dpath, jsonl_latest

    ap = argparse.ArgumentParser(prog="python -m pipeline.analytics.instagram")
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fetch")
    f.add_argument("--post-key", required=True)
    f.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    env = load_env()
    post = jsonl_latest(dpath("posts.jsonl"), "post_key").get(a.post_key, {"post_key": a.post_key})
    miss = missing(env)
    if a.dry_run or miss:
        if miss:
            print(f"DRY-RUN: missing {', '.join(miss)} in ~/studio/.env")
        print(json.dumps(requests_for(post, env), indent=1))
        return EXIT_OK
    try:
        print(json.dumps(fetch(post, env), indent=1))
    except DependencyError as e:
        print(f"dependency: {e}", file=sys.stderr)
        return EXIT_DEP
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
