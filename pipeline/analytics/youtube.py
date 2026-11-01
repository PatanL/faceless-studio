"""YouTube collector: Data API v3 (statistics) + YouTube Analytics API v2 (totals, audience retention).
See API_NOTES.md for what is verified against the official docs and what is assumed.

  python -m pipeline.analytics.youtube auth                 # HUMAN ONLY, one time (installed-app loopback OAuth)
  python -m pipeline.analytics.youtube fetch <video_id> --published-at ISO [--window 48h] [--dry-run]

Credentials (never in code, never printed): `~/studio/.env` names the files
  YT_CLIENT_SECRETS_FILE  default ~/studio/secrets/yt_client_secret.json  (the user's own "Desktop app" OAuth client)
  YT_TOKEN_FILE           default ~/studio/secrets/yt_token.json          (written by `auth`, mode 600)
  YT_CHANNEL_ID           our channel id (UC...), used to check the token belongs to the right channel
Agents never run `auth`: it needs the human's Google consent in their own browser.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import secrets
import sys
import time
from datetime import timedelta

from . import http
from ._common import (DependencyError, EXIT_DEP, EXIT_OK, env_or_default, iso, load_env, now_utc, parse)

SCOPES = ["https://www.googleapis.com/auth/yt-analytics.readonly", "https://www.googleapis.com/auth/youtube.readonly"]
DATA_API = "https://www.googleapis.com/youtube/v3"
ANALYTICS_API = "https://youtubeanalytics.googleapis.com/v2/reports"
TOKEN_URI = "https://oauth2.googleapis.com/token"
AUTH_URI = "https://accounts.google.com/o/oauth2/v2/auth"
TOTAL_METRICS = ["views", "engagedViews", "estimatedMinutesWatched", "averageViewDuration", "averageViewPercentage",
                 "likes", "comments", "shares", "subscribersGained"]
RETENTION_METRICS = ["audienceWatchRatio", "relativeRetentionPerformance"]
REQUIRED_ENV = ["YT_CHANNEL_ID"]


def paths(env: dict) -> tuple[str, str]:
    cs = os.path.expanduser(env_or_default(env, "YT_CLIENT_SECRETS_FILE", "~/studio/secrets/yt_client_secret.json"))
    tok = os.path.expanduser(env_or_default(env, "YT_TOKEN_FILE", "~/studio/secrets/yt_token.json"))
    return cs, tok


def missing(env: dict) -> list[str]:
    cs, tok = paths(env)
    out = [n for n in REQUIRED_ENV if not env.get(n)]
    if not os.path.exists(cs):
        out.append("YT_CLIENT_SECRETS_FILE (file)")
    if not os.path.exists(tok):
        out.append("YT_TOKEN_FILE (file; run `python -m pipeline.analytics.youtube auth` as the human)")
    return out


def _client(cs_path: str) -> dict:
    with open(cs_path, encoding="utf-8") as f:
        cs = json.load(f)
    c = cs.get("installed") or cs.get("web") or cs
    return {"client_id": c["client_id"], "client_secret": c.get("client_secret", ""), "token_uri": c.get("token_uri", TOKEN_URI)}


def _save_token(path: str, tok: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd = os.open(path + ".tmp", os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump(tok, f)
    os.replace(path + ".tmp", path)
    os.chmod(path, 0o600)


class Client:
    def __init__(self, env: dict):
        self.env = env
        self.cs_path, self.tok_path = paths(env)
        self.client = _client(self.cs_path)
        with open(self.tok_path, encoding="utf-8") as f:
            self.tok = json.load(f)

    def token(self) -> str:
        exp = self.tok.get("expires_at", 0)
        if self.tok.get("access_token") and exp - 60 > time.time():
            return self.tok["access_token"]
        if not self.tok.get("refresh_token"):
            raise DependencyError("YouTube token file has no refresh_token: the human reruns `youtube auth`")
        try:
            r = http.request("POST", self.client["token_uri"], form=True, data={
                "client_id": self.client["client_id"], "client_secret": self.client["client_secret"],
                "refresh_token": self.tok["refresh_token"], "grant_type": "refresh_token"})
        except http.ApiError as e:  # invalid_grant = revoked/expired consent (400/401); 5xx is just an outage
            if e.status >= 500 or e.status == 429:
                raise
            raise DependencyError(f"token refresh failed ({e.status}): the human reruns `youtube auth`")
        self.tok["access_token"] = r["access_token"]
        self.tok["expires_at"] = int(time.time()) + int(r.get("expires_in", 3600))
        _save_token(self.tok_path, self.tok)
        return self.tok["access_token"]

    def get(self, url: str, params: dict) -> dict:
        return http.request("GET", url, params=params, headers={"Authorization": f"Bearer {self.token()}"})

    # -- Data API
    def video(self, video_id: str) -> dict:
        r = self.get(f"{DATA_API}/videos", {"part": "statistics,contentDetails,snippet", "id": video_id})
        items = r.get("items") or []
        if not items:
            return {}
        it = items[0]
        st = it.get("statistics", {})
        return {"views": _int(st.get("viewCount")), "likes": _int(st.get("likeCount")),
                "comments": _int(st.get("commentCount")),
                "duration_s": iso8601_duration(it.get("contentDetails", {}).get("duration", "")),
                "channel_id": it.get("snippet", {}).get("channelId"),
                "published_at": it.get("snippet", {}).get("publishedAt")}

    # -- Analytics API
    def report(self, video_id: str, start: str, end: str, metrics: list[str], dimensions: str | None = None) -> dict:
        p = {"ids": "channel==MINE", "startDate": start, "endDate": end, "metrics": ",".join(metrics),
             "filters": f"video=={video_id}"}
        if dimensions:
            p["dimensions"] = dimensions
        return self.get(ANALYTICS_API, p)

    def totals(self, video_id: str, start: str, end: str) -> tuple[dict, list[str]]:
        metrics, notes = list(TOTAL_METRICS), []
        try:
            r = self.report(video_id, start, end, metrics)
        except http.ApiError as e:
            if e.status != 400:
                raise
            metrics = [m for m in metrics if m != "engagedViews"]
            notes.append("engagedViews rejected (400); retried without it")
            r = self.report(video_id, start, end, metrics)
        return table_row(r), notes

    def retention(self, video_id: str, start: str, end: str) -> dict | None:
        r = self.report(video_id, start, end, RETENTION_METRICS, "elapsedVideoTimeRatio")
        return retention_from_table(r)


def _int(v):
    return None if v is None else int(v)


def iso8601_duration(s: str) -> float | None:
    m = re.fullmatch(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?", s or "")
    if not m or not s:
        return None
    d, h, mi, se = (float(x) if x else 0.0 for x in m.groups())
    return d * 86400 + h * 3600 + mi * 60 + se


def table_row(r: dict) -> dict:
    """First row of a youtubeAnalytics#resultTable as {column name: value}; {} if no rows."""
    rows = r.get("rows") or []
    if not rows:
        return {}
    names = [h["name"] for h in r.get("columnHeaders", [])]
    return dict(zip(names, rows[0]))


def retention_from_table(r: dict) -> dict | None:
    rows = r.get("rows") or []
    if not rows:
        return None
    names = [h["name"] for h in r.get("columnHeaders", [])]
    ix = {n: i for i, n in enumerate(names)}
    rows = sorted(rows, key=lambda row: float(row[ix["elapsedVideoTimeRatio"]]))
    out = {"x": [round(float(row[ix["elapsedVideoTimeRatio"]]), 4) for row in rows],
           "watch_ratio": [float(row[ix["audienceWatchRatio"]]) for row in rows]}
    if "relativeRetentionPerformance" in ix:
        out["relative"] = [float(row[ix["relativeRetentionPerformance"]]) for row in rows]
    return out


def date_range(published_at: str, now=None) -> tuple[str, str]:
    """Analytics days are reported in Pacific time: start a day before the UTC publish date, end today."""
    pub = parse(published_at)
    now = now or now_utc()
    return (pub - timedelta(days=1)).strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d")


def requests_for(video_id: str, published_at: str) -> list[dict]:
    s, e = date_range(published_at)
    return [{"GET": f"{DATA_API}/videos", "part": "statistics,contentDetails,snippet", "id": video_id},
            {"GET": ANALYTICS_API, "ids": "channel==MINE", "startDate": s, "endDate": e,
             "metrics": ",".join(TOTAL_METRICS), "filters": f"video=={video_id}"},
            {"GET": ANALYTICS_API, "ids": "channel==MINE", "startDate": s, "endDate": e,
             "dimensions": "elapsedVideoTimeRatio", "metrics": ",".join(RETENTION_METRICS),
             "filters": f"video=={video_id}"}]


def fetch(video_id: str, published_at: str, env: dict) -> dict:
    """Live fetch -> partial metrics row (counts, retention, raw). Raises DependencyError on auth problems."""
    c = Client(env)
    v = c.video(video_id)
    if env.get("YT_CHANNEL_ID") and v.get("channel_id") and v["channel_id"] != env["YT_CHANNEL_ID"]:
        raise DependencyError(f"video {video_id} is not on YT_CHANNEL_ID (token or id mismatch)")
    s, e = date_range(published_at)
    tot, notes = c.totals(video_id, s, e)
    ret = c.retention(video_id, s, e)
    pending = [k for k, val in (("analytics", tot), ("retention", ret)) if not val]
    row = {"source": "yt_analytics" if tot else "yt_data",
           # lifetime viewCount from the Data API is near real time; Analytics totals lag 1-3 days, so they would
           # undercount at 48 h / 7 d. `views` (the kill-rule number) is the Data API count.
           "views": v.get("views") if v.get("views") is not None else tot.get("views"),
           "views_analytics": tot.get("views"), "engaged_views": tot.get("engagedViews"),
           "likes": tot.get("likes", v.get("likes")), "comments": tot.get("comments", v.get("comments")),
           "shares": tot.get("shares"), "saves": None, "subs_gained": tot.get("subscribersGained"),
           "avg_view_s": tot.get("averageViewDuration"), "avg_view_pct": tot.get("averageViewPercentage"),
           "watch_time_min": tot.get("estimatedMinutesWatched"), "reach": None, "viewed_vs_swiped_pct": None,
           "duration_s": v.get("duration_s"), "retention": ret, "pending": pending or None,
           "raw": {"data_api": v, "totals": tot, "notes": notes, "date_range": [s, e]}}
    return row


# ---------------------------------------------------------------- one-time human consent (loopback + PKCE)
def auth(env: dict, port: int = 8765) -> int:  # pragma: no cover - interactive, human only
    import http.server
    import urllib.parse

    cs_path, tok_path = paths(env)
    if not os.path.exists(cs_path):
        print(f"missing {cs_path}: download your own Desktop-app OAuth client JSON there (mode 600)", file=sys.stderr)
        return EXIT_DEP
    cl = _client(cs_path)
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(48)).rstrip(b"=").decode()
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    state = secrets.token_urlsafe(16)
    redirect = f"http://127.0.0.1:{port}/"
    url = AUTH_URI + "?" + urllib.parse.urlencode({
        "client_id": cl["client_id"], "redirect_uri": redirect, "response_type": "code", "scope": " ".join(SCOPES),
        "access_type": "offline", "prompt": "consent", "state": state,
        "code_challenge": challenge, "code_challenge_method": "S256"})
    got: dict = {}

    class H(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            q = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(self.path).query))
            if q.get("state") == state and "code" in q:
                got["code"] = q["code"]
                msg = b"Consent received. You can close this tab."
            else:
                msg = b"Unexpected request."
            self.send_response(200)
            self.end_headers()
            self.wfile.write(msg)

        def log_message(self, *a):
            pass

    srv = http.server.HTTPServer(("127.0.0.1", port), H)
    print("1. On the Mac: ssh -L 8765:127.0.0.1:8765 dgx-spark   (keep it open)")
    print("2. Open this URL in your own browser and consent with the channel's Google account:\n")
    print(url + "\n")
    while "code" not in got:
        srv.handle_request()
    r = http.request("POST", cl["token_uri"], form=True, data={
        "client_id": cl["client_id"], "client_secret": cl["client_secret"], "code": got["code"],
        "code_verifier": verifier, "redirect_uri": redirect, "grant_type": "authorization_code"})
    _save_token(tok_path, {"refresh_token": r.get("refresh_token"), "access_token": r.get("access_token"),
                           "expires_at": int(time.time()) + int(r.get("expires_in", 3600)), "scopes": SCOPES,
                           "created_at": iso(now_utc())})
    print(f"token saved to {tok_path} (mode 600)")
    return EXIT_OK


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.analytics.youtube")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("auth")
    f = sub.add_parser("fetch")
    f.add_argument("video_id")
    f.add_argument("--published-at", required=True)
    f.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    env = load_env()
    if a.cmd == "auth":
        return auth(env)
    miss = missing(env)
    if a.dry_run or miss:
        if miss:
            print(f"DRY-RUN: missing {', '.join(miss)} in ~/studio/.env")
        print(json.dumps(requests_for(a.video_id, a.published_at), indent=1))
        return EXIT_OK
    try:
        print(json.dumps(fetch(a.video_id, a.published_at, env), indent=1))
    except DependencyError as e:
        print(f"dependency: {e}", file=sys.stderr)
        return EXIT_DEP
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
