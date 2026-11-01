"""Sameness check: is this episode too close to one of the last N published ones? (design 7.2)

usage: python -m pipeline.qa.sameness <slug> [--root DIR] [--last-n 10] [--against slug,slug]

History = the last N distinct slugs in data/posts.jsonl whose latest row per post_key has status
published / scheduled / draft / sending (manual posts included), newest first, excluding <slug>;
or the explicit --against list. Their fingerprints come from out/<s>/qa/fingerprint.json (built if missing).

FAIL (any one): title char-trigram cosine >= 0.6; hook (first sentence) cosine >= 0.6; same topic
(aliases: orca = killer whale); thumbnail dHash Hamming <= 8; narration 5-gram containment >= 0.15
(the same script re-voiced); median frame dHash Hamming <= 10 at 10 fixed positions (the same cut re-uploaded).
WARN: beat sequence normalised edit distance <= 0.1 vs 3+ of the history (templated storyline);
shot-mix cosine >= 0.95; cover dHash Hamming <= 8; same main kit subject; same source video.
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys

from . import fingerprint as fpmod
from . import textsim
from .util import find_mp4, last_n_default, read_jsonl, root

THRESH = {
    "title": 0.6, "hook": 0.6, "thumb_hamming": 8, "script": 0.15, "frames_hamming": 10,
    "beats_ned": 0.1, "beats_min_count": 3, "shot_mix": 0.95, "cover_hamming": 8,
}
LIVE = {"published", "scheduled", "draft", "sending"}


def history_slugs(r, slug: str, last_n: int) -> list[str]:
    latest: dict[str, dict] = {}
    for row in read_jsonl(r / "data" / "posts.jsonl"):
        if row.get("post_key"):
            latest[row["post_key"]] = row
    when: dict[str, str] = {}
    for row in latest.values():
        s = row.get("slug")
        if not s or s == slug or row.get("status") not in LIVE:
            continue
        t = row.get("published_at") or row.get("scheduled_at") or row.get("at") or ""
        when[s] = max(when.get(s, ""), t)
    return [s for s, _ in sorted(when.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)][:last_n]


def load_history(r, slugs: list[str]) -> list[dict]:
    out = []
    for s in slugs:
        fp = fpmod.load(r, s)
        if fp is None and ((r / "episodes" / s / "script.md").is_file() or find_mp4(r, s)):
            fp = fpmod.build(s, r, video=find_mp4(r, s) is not None)
            fpmod.save(r, fp)
        if fp is not None:
            out.append(fp)
    return out


def _frames_hamming(a: list, b: list) -> int | None:
    ds = [textsim.hamming_hex(x, y) for x, y in zip(a or [], b or [])]
    ds = [d for d in ds if d is not None]
    return int(statistics.median(ds)) if len(ds) >= 5 else None


def pair(fp: dict, old: dict) -> dict:
    """All measures between this fingerprint and one past fingerprint."""
    ned = (textsim.norm_edit_distance(fp.get("beat_seq") or [], old.get("beat_seq") or [])
           if fp.get("beat_seq") and old.get("beat_seq") else None)
    return {
        "slug": old.get("slug"),
        "title": round(textsim.trigram_cosine(fp.get("title", ""), old.get("title", "")), 3),
        "hook": round(textsim.trigram_cosine(fp.get("hook", ""), old.get("hook", "")), 3),
        "topic": textsim.same_topic(fp.get("topic", ""), old.get("topic", "")),
        "thumb_hamming": textsim.hamming_hex(fp.get("thumb_dhash"), old.get("thumb_dhash")),
        "cover_hamming": textsim.hamming_hex(fp.get("cover_dhash"), old.get("cover_dhash")),
        "frames_hamming": _frames_hamming(fp.get("frame_dhashes"), old.get("frame_dhashes")),
        "script": round(textsim.containment(fp.get("narration_shingles") or [], old.get("narration_shingles") or []), 3),
        "beats_ned": None if ned is None else round(ned, 3),
        "shot_mix": round(textsim.cosine(fp.get("shot_mix") or {}, old.get("shot_mix") or {}), 3),
        "subject": bool(fp.get("subject")) and fp.get("subject") == old.get("subject"),
        "source": bool(fp.get("source_id")) and fp.get("source_id") == old.get("source_id"),
    }


def check(fp: dict, hist: list[dict]) -> dict:
    """The gate's `sameness` entry: {status, value, threshold, detail}."""
    if not hist:
        return {"status": "PASS", "value": {"vs": [], "max": {}}, "threshold": _thr_text(),
                "detail": "no published history to compare against"}
    pairs = [pair(fp, h) for h in hist]
    hits = []
    for p in pairs:
        s = p["slug"]
        if p["title"] >= THRESH["title"]:
            hits.append(("FAIL", s, "title", p["title"], f">= {THRESH['title']}"))
        if p["hook"] >= THRESH["hook"]:
            hits.append(("FAIL", s, "hook", p["hook"], f">= {THRESH['hook']}"))
        if p["topic"]:
            hits.append(("FAIL", s, "topic", f"{fp.get('topic')!r} ~ {next(h for h in hist if h.get('slug') == s).get('topic')!r}", "same topic"))
        if p["thumb_hamming"] is not None and p["thumb_hamming"] <= THRESH["thumb_hamming"]:
            hits.append(("FAIL", s, "thumb_hamming", p["thumb_hamming"], f"<= {THRESH['thumb_hamming']}"))
        if p["script"] >= THRESH["script"]:
            hits.append(("FAIL", s, "script", p["script"], f">= {THRESH['script']} of 5-grams shared"))
        if p["frames_hamming"] is not None and p["frames_hamming"] <= THRESH["frames_hamming"]:
            hits.append(("FAIL", s, "frames_hamming", p["frames_hamming"], f"median <= {THRESH['frames_hamming']}"))
        if p["shot_mix"] >= THRESH["shot_mix"]:
            hits.append(("WARN", s, "shot_mix", p["shot_mix"], f">= {THRESH['shot_mix']}"))
        if p["cover_hamming"] is not None and p["cover_hamming"] <= THRESH["cover_hamming"]:
            hits.append(("WARN", s, "cover_hamming", p["cover_hamming"], f"<= {THRESH['cover_hamming']}"))
        if p["subject"]:
            hits.append(("WARN", s, "subject", fp.get("subject"), "same main subject"))
        if p["source"]:
            hits.append(("WARN", s, "source", fp.get("source_id"), "same source video"))
    close_beats = [p["slug"] for p in pairs if p["beats_ned"] is not None and p["beats_ned"] <= THRESH["beats_ned"]]
    if len(close_beats) >= THRESH["beats_min_count"]:
        hits.append(("WARN", ",".join(close_beats), "beats_ned", len(close_beats),
                     f"beat sequence within {THRESH['beats_ned']} of {THRESH['beats_min_count']}+ recent videos"))
    status = "FAIL" if any(h[0] == "FAIL" for h in hits) else "WARN" if hits else "PASS"
    return {
        "status": status,
        "value": {"vs": [p["slug"] for p in pairs], "max": _maxes(pairs), "pairs": pairs},
        "threshold": _thr_text(),
        "hits": [{"level": l, "vs": s, "metric": m, "value": v, "threshold": t} for l, s, m, v, t in hits],
        "detail": "; ".join(f"{l} {m}={v} vs {s} ({t})" for l, s, m, v, t in hits) or f"vs {len(pairs)} recent videos",
    }


def _maxes(pairs: list[dict]) -> dict:
    def mx(k):
        vals = [p[k] for p in pairs if p[k] is not None]
        return max(vals) if vals else None

    def mn(k):
        vals = [p[k] for p in pairs if p[k] is not None]
        return min(vals) if vals else None
    beats = [1 - p["beats_ned"] for p in pairs if p["beats_ned"] is not None]
    return {"title": mx("title"), "hook": mx("hook"), "script": mx("script"), "shot_mix": mx("shot_mix"),
            "beats": round(max(beats), 3) if beats else None, "thumb_hamming": mn("thumb_hamming"),
            "cover_hamming": mn("cover_hamming"), "frames_hamming": mn("frames_hamming"),
            "same_topic": [p["slug"] for p in pairs if p["topic"]]}


def _thr_text() -> str:
    t = THRESH
    return (f"FAIL: title>={t['title']}, hook>={t['hook']}, same topic, thumb_hamming<={t['thumb_hamming']}, "
            f"script>={t['script']}, frames_hamming<={t['frames_hamming']}; WARN: beats_ned<={t['beats_ned']} "
            f"vs {t['beats_min_count']}+, shot_mix>={t['shot_mix']}, cover_hamming<={t['cover_hamming']}, same subject/source")


def run(r, slug: str, fp: dict, last_n: int | None = None, against: list[str] | None = None) -> dict:
    slugs = [s for s in against if s != slug] if against is not None else history_slugs(r, slug, last_n or last_n_default(r))
    return check(fp, load_history(r, slugs))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.qa.sameness")
    ap.add_argument("slug")
    ap.add_argument("--root")
    ap.add_argument("--last-n", type=int)
    ap.add_argument("--against", help="comma-separated slugs instead of data/posts.jsonl history")
    a = ap.parse_args(argv)
    r = root(a.root)
    fp = fpmod.load(r, a.slug) or fpmod.build(a.slug, r)
    res = run(r, a.slug, fp, a.last_n, a.against.split(",") if a.against else None)
    print(json.dumps(res, indent=1))
    return 6 if res["status"] == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
