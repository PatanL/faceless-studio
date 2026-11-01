"""Sameness check: is this episode too close to one of the last N published ones? (design 7.2)

usage: python -m pipeline.qa.sameness <slug> [--root DIR] [--last-n 10] [--against slug,slug]

History = the last N distinct slugs in data/posts.jsonl whose latest row per post_key has status
published / scheduled / draft / sending (manual posts included), newest first, excluding <slug>, plus every
operator episode (episodes/op-*) whose out/<s>/qa/gate.json says PASS and was written in the last 48 h and whose
review is not REJECT (the other slot of the same day, or one waiting for review/publish); or the explicit --against
list. Their fingerprints come from out/<s>/qa/fingerprint.json (built if missing). The result records which history
was used (`history_mode` default | against | last_n, and `history`): pipeline.publish.post refuses a gate.json made
with a non-default history and re-runs this check from fingerprint.json at post time.

FAIL (any one): title char-trigram cosine >= 0.6 on the subject words too (textsim.title_compare: the same title
template on a different subject is only a WARN); hook (first sentence) cosine >= 0.6; same topic
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
import time

from . import fingerprint as fpmod
from . import textsim
from .util import find_mp4, last_n_default, read_json, read_jsonl, root

THRESH = {
    "title": 0.6, "hook": 0.6, "thumb_hamming": 8, "script": 0.15, "frames_hamming": 10,
    "beats_ned": 0.1, "beats_min_count": 3, "shot_mix": 0.95, "cover_hamming": 8,
}
LIVE = {"published", "scheduled", "draft", "sending"}
RECENT_GATED_H = 48


def recent_gated(r, slug: str, hours: float = RECENT_GATED_H, now: float | None = None) -> list[str]:
    """op-* episodes with a gate PASS written in the last `hours` and no REJECT review, newest first (not <slug>)."""
    now = now or time.time()
    out = []
    for g in (r / "out").glob("op-*/qa/gate.json"):
        s = g.parent.parent.name
        if s == slug:
            continue
        try:
            age_h = (now - g.stat().st_mtime) / 3600
        except OSError:
            continue
        if age_h > hours:
            continue
        gate = read_json(g) or {}
        review = read_json(g.parent / "review.json") or {}
        if gate.get("verdict") == "PASS" and review.get("verdict") != "REJECT":
            out.append((g.stat().st_mtime, s))
    return [s for _, s in sorted(out, reverse=True)]


def history_slugs(r, slug: str, last_n: int, posts_path=None, gated: bool = True) -> list[str]:
    latest: dict[str, dict] = {}
    for row in read_jsonl(posts_path or (r / "data" / "posts.jsonl")):
        if row.get("post_key"):
            latest[row["post_key"]] = row
    when: dict[str, str] = {}
    for row in latest.values():
        s = row.get("slug")
        if not s or s == slug or row.get("status") not in LIVE:
            continue
        t = row.get("published_at") or row.get("scheduled_at") or row.get("at") or ""
        when[s] = max(when.get(s, ""), t)
    out = [s for s, _ in sorted(when.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)][:last_n]
    if gated:
        out += [s for s in recent_gated(r, slug) if s not in out]
    return out


def load_history(r, slugs: list[str], build_missing: bool = True) -> list[dict]:
    out = []
    for s in slugs:
        fp = fpmod.load(r, s)
        if fp is None and build_missing and ((r / "episodes" / s / "script.md").is_file() or find_mp4(r, s)):
            fp = fpmod.build(s, r, video=find_mp4(r, s) is not None)
            fpmod.save(r, fp)
        if fp is not None:
            out.append(fp)
    return out


def _frames_hamming(a: list, b: list) -> int | None:
    ds = [textsim.hamming_hex(x, y) for x, y in zip(a or [], b or [])]
    ds = [d for d in ds if d is not None]
    return int(statistics.median(ds)) if len(ds) >= 5 else None


def titles_of(fp: dict) -> list[str]:
    """The posted title plus the other title strings the fingerprint carries (title_alt)."""
    return [t for t in dict.fromkeys([fp.get("title") or "", *(fp.get("title_alt") or [])]) if t] or [""]


def title_pair(a: dict, b: dict) -> dict:
    """Worst textsim.title_compare over every title string of a and b."""
    order = {"FAIL": 2, "WARN": 1, "PASS": 0}
    best = None
    for x in titles_of(a):
        for y in titles_of(b):
            c = textsim.title_compare(x, y, THRESH["title"])
            if best is None or (order[c["level"]], c["full"]) > (order[best["level"]], best["full"]):
                best = c
    return best


def pair(fp: dict, old: dict) -> dict:
    """All measures between this fingerprint and one past fingerprint."""
    ned = (textsim.norm_edit_distance(fp.get("beat_seq") or [], old.get("beat_seq") or [])
           if fp.get("beat_seq") and old.get("beat_seq") else None)
    tp = title_pair(fp, old)
    return {
        "slug": old.get("slug"),
        "title": tp["full"], "title_content": tp["content"], "title_level": tp["level"],
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
        if p["title_level"] == "FAIL":
            hits.append(("FAIL", s, "title", p["title"], f">= {THRESH['title']} (subject words {p['title_content']})"))
        elif p["title_level"] == "WARN":
            hits.append(("WARN", s, "title_template", p["title"],
                         f">= {THRESH['title']} but a different subject (subject words {p['title_content']})"))
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
    return (f"FAIL: title>={t['title']} (and subject words >={t['title']}; template only = WARN), hook>={t['hook']}, same topic, thumb_hamming<={t['thumb_hamming']}, "
            f"script>={t['script']}, frames_hamming<={t['frames_hamming']}; WARN: beats_ned<={t['beats_ned']} "
            f"vs {t['beats_min_count']}+, shot_mix>={t['shot_mix']}, cover_hamming<={t['cover_hamming']}, same subject/source")


def history_mode(last_n: int | None, against: list[str] | None, r=None) -> str:
    if against is not None:
        return "against"
    if last_n is not None and r is not None and last_n != last_n_default(r):
        return "last_n"
    return "default"


def run(r, slug: str, fp: dict, last_n: int | None = None, against: list[str] | None = None,
        posts_path=None, build_missing: bool = True) -> dict:
    slugs = ([s for s in against if s and s != slug] if against is not None
             else history_slugs(r, slug, last_n or last_n_default(r), posts_path))
    res = check(fp, load_history(r, slugs, build_missing))
    res["history_mode"] = history_mode(last_n, against, r)
    res["history"] = slugs
    return res


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
