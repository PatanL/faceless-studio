"""Re-host a scheduled post's video after its quick tunnel died (e.g. the host rebooted).

Starts a new tunnel for the MP4, edits each still-scheduled Buffer post to point at it (text, metadata, due time and
cover offset kept), then holds the tunnel exactly like post.py until every post is sent, failed or gone.

usage: python -m pipeline.publish.rehost <slug> --mp4 PATH --post-ids ID[,ID...] [--hold-max-h 24] [--dry-run]
"""
from __future__ import annotations

import argparse
import sys

from pipeline.common import timeutil

from . import buffer as B
from . import host as H
from . import paths
from .post import _hold

EDIT = """mutation EditPost($input: EditPostInput!) { editPost(input: $input) { __typename
  ... on PostActionSuccess { post { id status dueAt assets { source } } }
  ... on MutationError { message } } }"""

YT_CATEGORY = "28"


def edit_input(post: dict, url: str, yt_category: str = YT_CATEGORY) -> dict:
    """EditPostInput that swaps only the video URL; Buffer rejects edits without text, assets and metadata."""
    a = (post.get("assets") or [{}])[0]
    video: dict = {"url": url}
    off = (a.get("video") or {}).get("thumbnailOffset")
    if off is not None:
        video["metadata"] = {"thumbnailOffset": off}
    md = post.get("metadata") or {}
    kind = md.get("__typename")
    if kind == "YoutubePostMetadata":
        meta = {"youtube": {"title": md.get("title"), "categoryId": yt_category, "privacy": md.get("privacy") or "public",
                            "madeForKids": bool(md.get("madeForKids")), "isAiGenerated": bool(md.get("isAiGenerated")),
                            "notifySubscribers": True, "embeddable": True}}
    elif kind == "InstagramPostMetadata":
        meta = {"instagram": {"type": md.get("type") or "reel", "shouldShareToFeed": md.get("shouldShareToFeed", True),
                              "isAiGenerated": bool(md.get("isAiGenerated"))}}
    elif kind == "TiktokPostMetadata":
        meta = {"tiktok": {"isAiGenerated": bool(md.get("isAiGenerated"))}}
    else:
        raise ValueError(f"post {post.get('id')}: unknown metadata {kind}")
    return {"id": post["id"], "text": post.get("text") or "", "assets": [{"video": video}], "metadata": meta,
            "dueAt": post.get("dueAt"), "mode": "customScheduled", "schedulingType": "automatic"}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("slug")
    ap.add_argument("--mp4", required=True)
    ap.add_argument("--post-ids", required=True)
    ap.add_argument("--hold-max-h", type=float, default=24)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    client, vals, _ = B.client_from_env(a.dry_run)
    ids = [i.strip() for i in a.post_ids.split(",") if i.strip()]
    posts = [] if client.dry_run else [client.post(i) for i in ids]
    live = [p for p in posts if p and p.get("status") not in ("sent", "error")]
    if not client.dry_run and not live:
        print("nothing to re-host: every post is sent, failed or gone")
        return 0
    mp4 = paths.ROOT / a.mp4 if not a.mp4.startswith("/") else a.mp4
    with H.hosted(mp4, ttl_s=a.hold_max_h * 3600, dry_run=client.dry_run, name=f"{a.slug}.mp4") as hosted:
        created, modes = [], {}
        for p in live:
            r = client.request(EDIT, {"input": edit_input(p, hosted.url)}, "EditPost", mutation=True,
                               label=f"EditPost {p['id']}")
            e = (r or {}).get("editPost") or {}
            if e.get("__typename") != "PostActionSuccess":
                print(f"{p['id']}: edit failed: {e.get('message') or e}", file=sys.stderr)
                continue
            post = e["post"]
            plat = p.get("channelService") or "?"
            print(f"{plat}: post {post['id']} now points at the new tunnel, due {post['dueAt']}")
            created.append((plat, post))
            modes[plat] = "auto"
        if client.dry_run or not created:
            return 0 if client.dry_run else 1
        slot_dt = max(timeutil.parse(post["dueAt"].replace(".000Z", "Z")) for _, post in created)
        _hold(client, hosted, created, slot_dt, modes, paths.load_config(), a.hold_max_h)
    return 0


if __name__ == "__main__":
    sys.exit(main())
