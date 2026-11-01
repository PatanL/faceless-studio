"""Refresh open Buffer posts and append status rows to data/posts.jsonl (OPERATOR_DESIGN 8.1, 5.10).

    python -m pipeline.publish.status [--all-open] [--slug S] [--dry-run]

Open = latest row per post_key with a buffer_post_id and status draft | scheduled | sending | missed, plus a
`published` row whose external_url/external_id is still null (Buffer fills externalLink after the platform has
processed the upload) for up to LINK_GRACE_H after it was sent. One GraphQL
request per 25 posts (aliased `post(input: {id})`). A row is appended only when something changed. Drafts still
unapproved `drafts_missed_h` after their slot become `missed` (Buffer keeps them; approving later still works and
the next refresh records it). Exit 4 when nothing is open, 5 when Buffer rejects the key.
"""
from __future__ import annotations

import argparse
import sys

from pipeline.common import env as cenv
from pipeline.common import jsonl, timeutil

from . import buffer as B
from . import host as H
from . import paths
from .post import _map_status, external_id

OPEN = {"draft", "scheduled", "sending", "missed"}
TERMINAL = {"published", "failed", "deleted"}
TRACKED = ("status", "buffer_status", "published_at", "external_url", "external_id", "error", "scheduled_at")
CHUNK = 25
LINK_GRACE_H = 48


def needs_link(r: dict, now=None) -> bool:
    """A published row without its platform link yet, sent less than LINK_GRACE_H ago."""
    if r.get("status") != "published" or (r.get("external_url") and r.get("external_id")):
        return False
    sent = r.get("published_at")
    if not sent:
        return True
    now = now or timeutil.now_utc()
    return (now - timeutil.parse(sent)).total_seconds() < LINK_GRACE_H * 3600


def open_rows(ledger, slug: str | None = None, now=None) -> list[dict]:
    rows = jsonl.latest(str(ledger), "post_key").values()
    return [r for r in rows if r.get("buffer_post_id") and not r.get("dry_run")
            and (r.get("status") in OPEN or needs_link(r, now)) and (not slug or r.get("slug") == slug)]


def updated_row(prev: dict, post: dict | None, now, missed_h: float) -> dict | None:
    new = {k: v for k, v in prev.items() if k not in ("at", "payload")}
    if post is None:
        new.update(status="deleted", buffer_status=None)
    else:
        st = _map_status(post.get("status"))
        if st == "draft" and prev.get("scheduled_at"):
            if now.timestamp() > timeutil.parse(prev["scheduled_at"]).timestamp() + missed_h * 3600:
                st = "missed"
        url = post.get("externalLink")
        new.update(status=st, buffer_status=post.get("status"),
                   published_at=post.get("sentAt") or prev.get("published_at"),
                   external_url=url or prev.get("external_url"),
                   external_id=external_id(prev["platform"], url) or prev.get("external_id"),
                   error=(post.get("error") or {}).get("message"),
                   scheduled_at=(post.get("dueAt") or prev.get("scheduled_at") or "").replace(".000Z", "Z") or None)
    if all(new.get(k) == prev.get(k) for k in TRACKED):
        return None
    return new


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.publish.status")
    ap.add_argument("--all-open", action="store_true", help="refresh every open post (the default)")
    ap.add_argument("--slug")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    ledger = paths.posts_ledger()
    rows = open_rows(ledger, a.slug)
    if not rows:
        print("no open posts")
        return B.EXIT_NOTHING
    client, _, _ = B.client_from_env(a.dry_run)
    cfg = paths.load_config()
    missed_h = float(cfg.get("drafts_missed_h", 6))
    now = timeutil.now_utc()
    changed = 0
    try:
        for i in range(0, len(rows), CHUNK):
            chunk = rows[i:i + CHUNK]
            cur = client.posts_by_ids([r["buffer_post_id"] for r in chunk])
            if cur is None:  # dry-run printed the request
                continue
            for r in chunk:
                new = updated_row(r, cur.get(r["buffer_post_id"]), now, missed_h)
                if new:
                    jsonl.append(str(ledger), new)
                    changed += 1
                    print(f"{r['post_key']}: {r.get('status')} -> {new['status']}"
                          f"{' ' + new['external_url'] if new.get('external_url') else ''}"
                          f"{' error: ' + new['error'] if new.get('error') else ''}")
    except B.BufferError as e:
        print(f"ERROR: {cenv.redact(str(e))}", file=sys.stderr)
        return e.exit_code
    if not client.dry_run:
        _prune(ledger)
        print(f"{len(rows)} open, {changed} changed")
    return B.EXIT_OK


def _prune(ledger):
    """Static mode: drop hosted copies once every post of that slug is terminal."""
    if (cenv.load_env().get("PUBLIC_HOST_MODE") or "").lower() != "static":
        return
    by_slug: dict[str, list[dict]] = {}
    for r in jsonl.latest(str(ledger), "post_key").values():
        if not r.get("dry_run") and (r.get("host") or {}).get("mode") == "static":
            by_slug.setdefault(r["slug"], []).append(r)
    for slug, rs in by_slug.items():
        if all(r.get("status") in TERMINAL for r in rs):
            gone = H.prune_static(f"{slug}.mp4")
            if gone:
                print(f"pruned hosted media for {slug} ({len(gone)})")


if __name__ == "__main__":
    sys.exit(main())
