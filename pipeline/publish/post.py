"""Post one gated episode to YouTube Shorts, TikTok and Instagram Reels through Buffer (OPERATOR_DESIGN 8.1-8.5).

    python -m pipeline.publish.post <slug> --slot-at <ISO> [--platforms youtube,tiktok,instagram]
                                    [--mode draft|auto] [--dry-run] [--ignore-gates] [--mp4 PATH]
    python -m pipeline.publish.post --record-manual <slug> <platform> <url> [--published-at ISO]

Preconditions (exit 6 otherwise): gate.json PASS, review.json PASS, gate.mp4_sha256 == sha256(mp4),
review.gate_sha == sha256(gate.json), no live row for the post_key, config.paused false.
Credentials: BUFFER_API_KEY and BUFFER_CHANNEL_<PLATFORM> from ~/studio/.env; any missing -> dry-run, which prints
the exact GraphQL request per platform and appends `dry_run` rows (with the payload) to data/posts.jsonl.
--ignore-gates is accepted only with --dry-run (for previewing payloads of an episode that has no gate yet).
Mode: config.mode.<platform> unless --mode; "auto" needs config.disclosure_ok_auto.<platform>, else it drops to draft.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

from pipeline.common import env as cenv
from pipeline.common import jsonl, timeutil

from . import buffer as B
from . import captions as C
from . import host as H
from . import paths

PLATFORMS = ("youtube", "tiktok", "instagram")
CHANNEL_VAR = {p: f"BUFFER_CHANNEL_{p.upper()}" for p in PLATFORMS}
LIVE_STATUSES = {"draft", "scheduled", "sending", "published", "missed", "manual"}
DEFAULT_YT_CATEGORY = "28"   # Science & Technology (YoutubePostMetadataInput.categoryId list)
DEFAULT_COVER_OFFSET_MS = 1500
HOLD_POLL_S = 900   # 15 min: Free plan allows ~100 requests/day averaged over 30 days (3 channels)


# ---------------------------------------------------------------------------------------------------------------
# preconditions

def preconditions(slug: str, mp4: Path | None, platforms, cfg: dict, ledger: Path) -> dict:
    qa = paths.qa_dir(slug)
    gate_p, review_p = qa / "gate.json", qa / "review.json"
    gate, review = paths.read_json(gate_p), paths.read_json(review_p)
    mp4_sha = paths.sha256_file(mp4) if mp4 else None
    gate_sha = paths.sha256_file(gate_p) if gate_p.exists() else None
    chk = {}
    chk["mp4"] = {"ok": bool(mp4), "detail": str(mp4) if mp4 else "no MP4 found"}
    chk["gate_pass"] = {"ok": bool(gate) and gate.get("verdict") == "PASS",
                        "detail": f"{gate_p.relative_to(paths.ROOT)}: " +
                                  (gate.get("verdict", "?") if gate else "missing")}
    chk["review_pass"] = {"ok": bool(review) and review.get("verdict") == "PASS",
                          "detail": f"{review_p.relative_to(paths.ROOT)}: " +
                                    (review.get("verdict", "?") if review else "missing")}
    chk["gate_mp4_sha"] = {"ok": bool(gate and mp4_sha) and gate.get("mp4_sha256") == mp4_sha,
                           "detail": "gate.mp4_sha256 == sha256(mp4)" if gate else "no gate.json"}
    chk["review_gate_sha"] = {"ok": bool(review and gate_sha) and review.get("gate_sha") == gate_sha,
                              "detail": "review.gate_sha == sha256(gate.json)" if review else "no review.json"}
    live = {k: r.get("status") for k, r in jsonl.latest(str(ledger), "post_key").items()
            if k in {f"{slug}:{p}" for p in platforms} and _blocking(r)}
    chk["idempotent"] = {"ok": not live, "detail": f"live rows: {live}" if live else "no live row"}
    chk["not_paused"] = {"ok": not cfg.get("paused"), "detail": f"config.paused={cfg.get('paused')}"}
    return chk


def _blocking(row: dict) -> bool:
    st = row.get("status")
    if row.get("dry_run") or st == "dry_run":
        return False
    if st == "failed":
        return bool(row.get("ambiguous"))  # might exist in Buffer: reconcile before posting again
    return st in LIVE_STATUSES


# ---------------------------------------------------------------------------------------------------------------
# payloads

def effective_mode(platform: str, cfg: dict, cli_mode: str | None) -> tuple[str, str | None]:
    want = cli_mode or (cfg.get("mode") or {}).get(platform, "draft")
    if want == "auto" and not (cfg.get("disclosure_ok_auto") or {}).get(platform):
        return "draft", f"{platform}: auto needs config.disclosure_ok_auto.{platform}=true; using draft"
    return want, None


def build_input(platform: str, channel_id: str, cap: dict, video_url: str, slot_at: str, mode: str,
                cover_offset_ms: int | None, yt_category: str) -> dict:
    """CreatePostInput for one platform (field names per developers.buffer.com/reference.md, 2026-11-01)."""
    video: dict = {"url": video_url}
    if platform in ("instagram", "tiktok") and cover_offset_ms is not None:
        video["metadata"] = {"thumbnailOffset": int(cover_offset_ms)}
    inp: dict = {
        "channelId": channel_id,
        "schedulingType": "automatic",
        "mode": "customScheduled",
        "dueAt": slot_at,
        "assets": [{"video": video}],
        "aiAssisted": True,  # captions are LLM-drafted (Buffer tracking flag)
    }
    if mode == "draft":
        inp["saveToDraft"] = True
    if platform == "youtube":
        inp["text"] = cap["youtube"]["description"]
        inp["metadata"] = {"youtube": {
            "title": cap["youtube"]["title"], "categoryId": yt_category, "privacy": "public",
            "madeForKids": False, "isAiGenerated": True, "notifySubscribers": True, "embeddable": True}}
    elif platform == "tiktok":
        inp["text"] = cap["tiktok"]["text"]
        inp["metadata"] = {"tiktok": {"isAiGenerated": True}}
    elif platform == "instagram":
        inp["text"] = cap["instagram"]["text"]
        inp["metadata"] = {"instagram": {"type": "reel", "shouldShareToFeed": True, "isAiGenerated": True}}
    else:
        raise ValueError(platform)
    return inp


def caption_sha(platform: str, inp: dict) -> str:
    title = ((inp.get("metadata") or {}).get("youtube") or {}).get("title", "")
    return paths.sha256_text(title + "\n" + inp.get("text", ""))


def video_duration(slug: str, mp4: Path) -> float | None:
    st = paths.read_json(paths.episode_dir(slug) / "make_status.json") or {}
    d = (st.get("outputs") or {}).get("duration_s")
    if d:
        return float(d)
    if shutil.which("ffprobe"):
        try:
            r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                "default=nw=1:nk=1", str(mp4)], capture_output=True, text=True, timeout=30)
            return round(float(r.stdout.strip()), 2)
        except (ValueError, subprocess.SubprocessError, OSError):
            return None
    return None


def external_id(platform: str, url: str | None) -> str | None:
    if not url:
        return None
    pats = {"youtube": [r"youtube\.com/shorts/([\w-]{11})", r"[?&]v=([\w-]{11})", r"youtu\.be/([\w-]{11})"],
            "tiktok": [r"/video/(\d+)"],
            "instagram": [r"instagram\.com/(?:reel|reels|p)/([\w-]+)"]}  # IG gives the shortcode, not media id
    for p in pats.get(platform, []):
        m = re.search(p, url)
        if m:
            return m.group(1)
    return None


# ---------------------------------------------------------------------------------------------------------------
# commands

def cmd_record_manual(a) -> int:
    slug, platform, url = a.record_manual
    if platform not in PLATFORMS:
        print(f"platform must be one of {PLATFORMS}", file=sys.stderr)
        return B.EXIT_USAGE
    ledger = paths.posts_ledger()
    key = f"{slug}:{platform}"
    prev = jsonl.latest(str(ledger), "post_key").get(key)
    if prev and _blocking(prev) and prev.get("external_url") == url:
        print(f"{key}: already recorded ({prev.get('status')})")
        return B.EXIT_NOTHING
    mp4 = paths.find_mp4(slug)
    row = {"post_key": key, "slug": slug, "platform": platform, "source_id": _source_id(slug),
           "experiment_id": None, "arm": None, "mode": "manual", "dry_run": False, "status": "published",
           "buffer_channel_id": None, "buffer_post_id": None, "scheduled_at": None,
           "published_at": a.published_at or timeutil.iso(), "external_id": external_id(platform, url),
           "external_url": url, "title": None, "caption_sha256": None,
           "video_sha256": paths.sha256_file(mp4) if mp4 else None,
           "duration_s": video_duration(slug, mp4) if mp4 else None, "error": None}
    jsonl.append(str(ledger), row)
    print(f"{key}: recorded manual post {row['external_id'] or url}")
    return B.EXIT_OK


def _source_id(slug: str) -> str | None:
    return (paths.read_json(paths.episode_dir(slug) / "source.json") or {}).get("source_id")


def _variant(slug: str) -> dict:
    return paths.read_json(paths.episode_dir(slug) / "variant.json") or {}


def cmd_post(a) -> int:
    slug = a.slug
    platforms = [p.strip() for p in a.platforms.split(",") if p.strip()]
    bad = [p for p in platforms if p not in PLATFORMS]
    if bad or not platforms:
        print(f"unknown platform(s) {bad}; choose from {PLATFORMS}", file=sys.stderr)
        return B.EXIT_USAGE
    try:
        slot_dt = timeutil.parse(a.slot_at)
    except ValueError:
        print(f"--slot-at must be ISO-8601, got {a.slot_at!r}", file=sys.stderr)
        return B.EXIT_USAGE
    slot_at = slot_dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    if a.ignore_gates and not a.dry_run:
        print("--ignore-gates is only allowed with --dry-run", file=sys.stderr)
        return B.EXIT_USAGE

    allenv = cenv.load_env()
    needed = ["BUFFER_API_KEY"] + [CHANNEL_VAR[p] for p in platforms]
    missing = [n for n in needed if not allenv.get(n)]
    dry = a.dry_run or bool(missing)
    if missing:
        print(cenv.dry_run_notice(missing))
    if not dry and slot_dt.timestamp() < time.time() + 300:
        print(f"--slot-at {slot_at} is less than 5 min away or in the past", file=sys.stderr)
        return B.EXIT_USAGE

    cfg = paths.load_config()
    ledger = paths.posts_ledger()
    mp4 = Path(a.mp4) if a.mp4 else paths.find_mp4(slug)
    if mp4 and not mp4.is_file():
        print(f"--mp4 {mp4} not found", file=sys.stderr)
        return B.EXIT_USAGE
    pre = preconditions(slug, mp4, platforms, cfg, ledger)
    failed = [k for k, v in pre.items() if not v["ok"]]
    print(f"preconditions for {slug}:")
    for k, v in pre.items():
        print(f"  {'ok  ' if v['ok'] else 'FAIL'} {k}: {v['detail']}")
    if not mp4:
        return B.EXIT_GATE
    hard_fail = [k for k in failed if not (a.ignore_gates and k in
                                           ("gate_pass", "review_pass", "gate_mp4_sha", "review_gate_sha"))]
    if hard_fail and not dry:
        print(f"BLOCKED: {', '.join(hard_fail)}")
        return B.EXIT_GATE
    if hard_fail and dry:
        print(f"BLOCKED (a real run exits 6): {', '.join(hard_fail)}; payloads below are a preview only, "
              f"no ledger rows written")

    cap = C.build(slug)
    cap_path = C.write(slug, cap) if not hard_fail else None
    if cap_path:
        print(f"captions: {cap_path.relative_to(paths.ROOT) if cap_path.is_relative_to(paths.ROOT) else cap_path}")
    cover = cap.get("cover_offset_ms")
    cover = DEFAULT_COVER_OFFSET_MS if cover is None else cover
    yt_cat = allenv.get("BUFFER_YT_CATEGORY_ID") or DEFAULT_YT_CATEGORY
    vsha = paths.sha256_file(mp4)
    dur = video_duration(slug, mp4)
    var = _variant(slug)
    client = B.BufferClient(allenv.get("BUFFER_API_KEY"), allenv.get("BUFFER_API_URL"), dry_run=dry)

    modes = {}
    for p in platforms:
        m, note = effective_mode(p, cfg, a.mode)
        modes[p] = m
        if note:
            print("NOTE:", note)

    channels: dict[str, dict] = {}
    org_id = allenv.get("BUFFER_ORG_ID")
    if not dry:
        try:
            org_id = client.resolve_org(org_id)
            channels = {c["id"]: c for c in client.channels(org_id) or []}
        except B.BufferError as e:
            print(f"ERROR: {cenv.redact(str(e))}", file=sys.stderr)
            return e.exit_code
        for p in platforms:
            ch = channels.get(allenv[CHANNEL_VAR[p]])
            if not ch:
                print(f"ERROR: {CHANNEL_VAR[p]} is not a channel of organization {org_id}", file=sys.stderr)
                return B.EXIT_USAGE
            if ch.get("service") != B.PLATFORM_SERVICE[p]:
                print(f"ERROR: {CHANNEL_VAR[p]} is a {ch.get('service')} channel, not {p}", file=sys.stderr)
                return B.EXIT_USAGE
            if ch.get("isDisconnected") or ch.get("isLocked"):
                print(f"ERROR: {p} channel is disconnected or locked in Buffer", file=sys.stderr)
                return B.EXIT_DEP
            if ch.get("isQueuePaused"):
                print(f"WARN: {p} channel queue is paused in Buffer: scheduled posts will not go out")

    rows_written, created, exit_code = 0, [], B.EXIT_OK
    with H.hosted(mp4, ttl_s=a.hold_max_h * 3600, dry_run=dry, name=f"{slug}.mp4") as hosted:
        for p in platforms:
            ch_id = allenv.get(CHANNEL_VAR[p]) or f"<{CHANNEL_VAR[p]}>"
            inp = build_input(p, ch_id, cap, hosted.url, slot_at, modes[p], cover, yt_cat)
            base = {"post_key": f"{slug}:{p}", "slug": slug, "platform": p, "source_id": _source_id(slug),
                    "experiment_id": var.get("experiment_id"), "arm": var.get("arm"), "mode": modes[p],
                    "buffer_channel_id": allenv.get(CHANNEL_VAR[p]), "scheduled_at": slot_at.replace(".000Z", "Z"), "published_at": None,
                    "external_id": None, "external_url": None, "title": cap["youtube"]["title"],
                    "caption_sha256": caption_sha(p, inp), "video_sha256": vsha, "duration_s": dur,
                    "host": {"mode": hosted.mode}}
            if dry:
                print(f"\n=== {p} ({modes[p]}) ===")
                client.create_post(inp, label=f"CreatePost {p}")
                if not hard_fail:
                    row = dict(base, dry_run=True, status="dry_run", buffer_post_id=None, error=None,
                               gates_ignored=bool(a.ignore_gates and failed),
                               preconditions={k: v["ok"] for k, v in pre.items()},
                               payload=client.build(B.load_op("CreatePost"), {"input": inp}, "CreatePost")["body"])
                    jsonl.append(str(ledger), row)
                    rows_written += 1
                continue
            t0 = timeutil.iso()
            try:
                post = client.create_post(inp)
                err, amb = None, False
            except B.Ambiguous as e:
                post, err, amb = _reconcile(client, org_id, ch_id, t0, inp), cenv.redact(str(e)), True
            except B.MutationFailed as e:
                post, err, amb = None, cenv.redact(str(e)), False
            except B.BufferError as e:
                print(f"ERROR {p}: {cenv.redact(str(e))}", file=sys.stderr)
                jsonl.append(str(ledger), dict(base, dry_run=False, status="failed", buffer_post_id=None,
                                               error=cenv.redact(str(e))))
                exit_code = e.exit_code
                break  # stop creating, but still hold the URL for posts already created
            if post:
                status = _map_status(post.get("status"))
                row = dict(base, dry_run=False, status=status, buffer_post_id=post["id"], error=None,
                           buffer_status=post.get("status"), reconciled=amb or None)
                created.append((p, post))
                print(f"{p}: Buffer post {post['id']} {post.get('status')} due {post.get('dueAt')}")
            else:
                row = dict(base, dry_run=False, status="failed", buffer_post_id=None, error=err,
                           ambiguous=amb or None)
                exit_code = B.EXIT_FAIL
                print(f"{p}: FAILED {err}", file=sys.stderr)
            jsonl.append(str(ledger), row)
            rows_written += 1
        if not dry and created and hosted.mode == "cloudflared":
            _hold(client, hosted, created, slot_dt, modes, cfg, a.hold_max_h)
    if dry:
        print(f"\nDRY-RUN done: {rows_written} dry_run row(s) -> "
              f"{ledger if rows_written else '(none: blocked preview)'}")
        return B.EXIT_GATE if hard_fail else B.EXIT_OK
    return exit_code


def _map_status(s: str | None) -> str:
    return {"draft": "draft", "needs_approval": "draft", "scheduled": "scheduled", "sending": "sending",
            "sent": "published", "error": "failed"}.get(s or "", s or "failed")


def _reconcile(client, org_id, ch_id, since_iso, inp) -> dict | None:
    """After an ambiguous createPost, look for a post on that channel created since t0 with the same text."""
    try:
        for p in client.recent_channel_posts(org_id, ch_id, since_iso) or []:
            if (p.get("text") or "").strip() == (inp.get("text") or "").strip():
                return p
    except B.BufferError:
        return None
    return None


def _hold(client, hosted, created, slot_dt, modes, cfg, hold_max_h):
    """Keep the quick tunnel up until Buffer no longer needs our URL.

    Buffer's docs say it fetches the media again when the post goes out. If the created post's asset `source` is
    already a Buffer-hosted URL (it copied the file), close at once. Otherwise poll until every post is sent/error
    or gone, or until slot + drafts_missed_h (draft) / slot + 1 h (auto), capped at hold_max_h from now.
    """
    host = hosted.url.split("/")[2]
    needs = [(p, post) for p, post in created
             if any(host in (a.get("source") or "") for a in post.get("assets") or [])]
    if not needs:
        print("media: Buffer reports its own asset URLs; closing the tunnel")
        return
    grace_h = max(float(cfg.get("drafts_missed_h", 6)) if any(modes[p] == "draft" for p, _ in needs) else 1.0, 0)
    deadline = min(slot_dt.timestamp() + grace_h * 3600, time.time() + hold_max_h * 3600)
    print(f"media: Buffer still points at the tunnel for {[p for p, _ in needs]}; holding until "
          f"{timeutil.iso(dt.datetime.fromtimestamp(deadline, timeutil.UTC))}")
    ids = [post["id"] for _, post in needs]
    while time.time() < deadline:
        time.sleep(HOLD_POLL_S)
        try:
            cur = client.posts_by_ids(ids) or {}
        except B.BufferError as e:
            print(f"hold: status check failed: {cenv.redact(str(e))}")
            continue
        open_ = [i for i in ids if cur.get(i) and cur[i].get("status") not in ("sent", "error")
                 and any(host in (a.get("source") or "") for a in cur[i].get("assets") or [])]
        if not open_:
            print("hold: every post is sent, failed, deleted or re-hosted; closing the tunnel")
            return
    print("hold: deadline reached; closing the tunnel (unsent posts will fail to fetch media; see HUMAN.md)")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.publish.post")
    ap.add_argument("slug", nargs="?")
    ap.add_argument("--slot-at")
    ap.add_argument("--platforms", default=",".join(PLATFORMS))
    ap.add_argument("--mode", choices=["draft", "auto"])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--ignore-gates", action="store_true", help="dry-run only: preview without gate/review PASS")
    ap.add_argument("--mp4")
    ap.add_argument("--hold-max-h", type=float, default=12.0, help="cloudflared mode: max hours to keep the URL up")
    ap.add_argument("--record-manual", nargs=3, metavar=("SLUG", "PLATFORM", "URL"))
    ap.add_argument("--published-at")
    a = ap.parse_args(argv)
    if a.record_manual:
        return cmd_record_manual(a)
    if not a.slug or not a.slot_at:
        ap.error("<slug> and --slot-at are required (or use --record-manual)")
    try:
        return cmd_post(a)
    except (FileNotFoundError, ValueError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return B.EXIT_FAIL
    except H.HostError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return e.exit_code
    except B.BufferError as e:
        print(f"ERROR: {cenv.redact(str(e))}", file=sys.stderr)
        return e.exit_code


if __name__ == "__main__":
    sys.exit(main())
