#!/usr/bin/env python3
"""Build research/library/library.json (+ stats.json) from research/library/videos/*.json.

The per-video analyses were written by several agents with slightly different key names,
so everything here is defensive: it normalises the fields the index needs and records
paths to transcripts, contact sheets, thumbnails, corpus annotations and review-ref frames.

Usage: python3 research/library/build_library.py   (run from anywhere; Mac-safe, pure stdlib)
"""
import glob
import json
import os
import re
import statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))


def rel(p):
    return os.path.relpath(p, ROOT)


def sget(obj, *keys, default=None):
    """Get the first present key from a dict; tolerate strings/None."""
    if not isinstance(obj, dict):
        return default
    for k in keys:
        if k in obj and obj[k] not in (None, "", [], {}):
            return obj[k]
    return default


def text(x, n=None):
    if x is None:
        return ""
    s = x if isinstance(x, str) else json.dumps(x, ensure_ascii=False)
    s = re.sub(r"\s+", " ", s).strip()
    return s[:n] if n else s


def num(x):
    if isinstance(x, (int, float)):
        return float(x)
    if isinstance(x, str):
        m = re.search(r"(\d+(?:\.\d+)?)", x)
        if m:
            return float(m.group(1))
    return None


def find_pacing(p, patterns):
    if not isinstance(p, dict):
        return None
    for k, v in p.items():
        if any(re.search(pt, k) for pt in patterns):
            n = num(v)
            if n is not None:
                return n
    return None


EXPLAINER_CATS = [
    ("presenter", r"presenter|greenscreen|green_screen|talking|host|creator|face"),
    ("title_card", r"title|chapter|card_gate|list item|end card|question_card|text_card|kinetic"),
    ("scale_comparison", r"scale|size|comparison|vs_|versus|silhouette_line"),
    ("map", r"map|globe"),
    ("diagram_infographic", r"diagram|infographic|anatomy|chart|timeline|graph|stat|counter|meter|isotype|cutaway|cross.?section"),
    ("stock_footage", r"stock|broll|b-roll|footage|real|wildlife|photo|clip_in_frame|document"),
    ("cgi_illustration", r"cgi|render|illustration|paleoart|vector|animation|animated|cartoon|character|pov|arena|action|scene"),
]
HORROR_CATS = [
    ("phone_ui", r"phone|chat|imessage|message|text_ui|screen|ui|notification|call|danmaku"),
    ("text_card", r"black|text_card|prose|title|card|typewriter"),
    ("close_up", r"close|cu\b|mcu|insert|reaction|ecu|detail"),
    ("two_shot_group", r"two|three|group|ots|over_the_shoulder|shot_reverse"),
    ("wide_establishing", r"wide|establishing|exterior|ws\b|silhouette|monster"),
    ("character_medium", r"medium|ms\b|character|single|full"),
    ("pov", r"pov"),
]
WHATIF_CATS = [
    ("title_card", r"title|card|text|chapter"),
    ("diagram_infographic", r"diagram|infographic|map|chart|graph|stat|counter|globe|space"),
    ("wide_establishing", r"wide|establishing|aerial|city|landscape"),
    ("close_up", r"close|cu\b|insert|reaction|detail"),
    ("character_medium", r"medium|character|two|group|ms\b"),
]
CATS = {"explainer": EXPLAINER_CATS, "horror": HORROR_CATS, "whatif": WHATIF_CATS}


def shot_cat(niche, shot_type):
    s = (shot_type or "").lower()
    for name, pat in CATS.get(niche, []):
        if re.search(pat, s):
            return name
    return "other"


def title_features(title):
    t = title or ""
    words = re.findall(r"[A-Za-z0-9']+", t)
    caps = [w for w in words if len(w) > 2 and w.isupper()]
    return {
        "title_words": len(words),
        "title_has_you": bool(re.search(r"\byou(r|'d|'re)?\b", t, re.I)),
        "title_question": "?" in t or bool(re.match(r"\s*(what|why|how|can|could|would|is|do)\b", t, re.I)),
        "title_number": bool(re.search(r"\d", t)),
        "title_caps_word": bool(caps),
        "title_emoji_or_ellipsis": bool(re.search(r"\.\.\.|…|[\U0001F300-\U0001FAFF]", t)),
        "title_is_hashtags": t.strip().startswith("#"),
    }


def load():
    rows = []
    for f in sorted(glob.glob(os.path.join(HERE, "videos", "*.json"))):
        try:
            d = json.load(open(f))
        except Exception as e:  # noqa
            print("skip (bad json)", f, e)
            continue
        if not isinstance(d, dict) or not d.get("niche"):
            print("skip (empty/failed)", f)
            continue
        d["id"] = d.get("id") or d.get("video_id") or os.path.basename(f)[:-5]
        d["_path"] = f
        rows.append(d)
    return rows


def row_for(d):
    vid = d["id"]
    niche = d["niche"]
    hook = d.get("hook") if isinstance(d.get("hook"), dict) else {"device": d.get("hook")}
    tp = d.get("title_pattern") if isinstance(d.get("title_pattern"), dict) else {"template": d.get("title_pattern")}
    th = d.get("thumbnail") if isinstance(d.get("thumbnail"), dict) else {"text": d.get("thumbnail")}
    pacing = d.get("pacing") if isinstance(d.get("pacing"), dict) else {}
    shots = d.get("shot_list") or []
    beats = d.get("beats") or []
    dur = num(d.get("duration")) or 0.0

    wpm = find_pacing(pacing, [r"words_per_min", r"^wpm$", r"wpm"])
    if wpm is None:
        words = find_pacing(pacing, [r"^words(_total)?(_approx)?$"])
        if words and dur:
            wpm = round(words / dur * 60, 1)
    avg_shot = find_pacing(pacing, [r"avg_shot", r"avg_hard_cut", r"mean_shot", r"avg_cut"])
    if avg_shot is None and shots and dur:
        avg_shot = round(dur / len(shots), 2)
    cap_int = find_pacing(pacing, [r"caption.*(interval|card_s|change_interval|hold)", r"avg_cue_length", r"avg_seconds_per_bubble"])
    vis_change = find_pacing(pacing, [r"visual_change", r"element_build"])
    rehook = find_pacing(pacing, [r"rehook", r"re_hook", r"open_loop"])
    hook_len = num(sget(hook, "hook_length_s", "length_s", "duration_s"))

    cats = {}
    for s in shots:
        a, b = num(s.get("t_start")), num(s.get("t_end"))
        span = (b - a) if (a is not None and b is not None and b > a) else 1.0
        c = shot_cat(niche, s.get("shot_type"))
        cats[c] = cats.get(c, 0) + span
    tot = sum(cats.values()) or 1.0
    shot_mix = {k: round(v / tot, 3) for k, v in sorted(cats.items(), key=lambda kv: -kv[1])}

    def exists(p):
        return rel(p) if os.path.exists(p) else None

    sheets = sorted(rel(p) for p in glob.glob(os.path.join(HERE, "sheets", f"{vid}*.jpg")))
    corpus = exists(os.path.join(ROOT, "research", "corpus", niche, f"{vid}.md"))
    refs = sorted(rel(p) for p in glob.glob(os.path.join(HERE, "review-refs", niche, vid, "*.jpg")))

    r = {
        "id": vid,
        "niche": niche,
        "role": d.get("role"),
        "platform": d.get("platform"),
        "format": "9:16" if (d.get("platform") in ("tiktok", "youtube_shorts") or (dur and dur <= 62)) else "16:9",
        "url": d.get("url"),
        "channel": d.get("channel"),
        "title": d.get("title"),
        "upload_date": d.get("upload_date"),
        "duration_s": dur,
        "views": d.get("views"),
        "likes": d.get("likes"),
        "comments": d.get("comments"),
        "subs": d.get("subs"),
        "channel_median_views": d.get("channel_median_views"),
        "outlier_score": d.get("outlier_score"),
        "title_template": text(sget(tp, "template", "pattern", "formula"), 200),
        "thumbnail_text": text(sget(th, "text", "text_overlay"), 200),
        "thumbnail_why": text(sget(th, "why_it_works", "notes"), 300),
        "hook_device": text(sget(hook, "device", "devices", "visual_device", "type", "technique"), 300),
        "hook_verbatim": text(sget(hook, "verbatim_0_5s", "verbatim", "line", "text"), 300),
        "hook_length_s": hook_len,
        "beats_n": len(beats),
        "beat_sequence": [text(b.get("beat_type") or b.get("type") or b.get("name"), 60) for b in beats if isinstance(b, dict)],
        "shots_n": len(shots),
        "shot_mix": shot_mix,
        "words_per_min": wpm,
        "avg_shot_s": avg_shot,
        "caption_interval_s": cap_int,
        "visual_change_s": vis_change,
        "rehook_interval_s": rehook,
        "techniques": [text(x, 400) for x in (d.get("techniques_worth_copying") or [])],
        **title_features(d.get("title")),
        "paths": {
            "analysis": rel(d["_path"]),
            "transcript": exists(os.path.join(HERE, "transcripts", f"{vid}.txt")),
            "thumbnail": exists(os.path.join(HERE, "thumbs", f"{vid}.jpg")),
            "sheets": sheets,
            "corpus_annotation": corpus,
            "review_ref_frames": refs,
        },
    }
    return r


def agg(rows):
    out = {"n": len(rows)}
    def med(key):
        vals = [r[key] for r in rows if isinstance(r.get(key), (int, float))]
        return round(st.median(vals), 2) if vals else None
    for k in ["duration_s", "hook_length_s", "words_per_min", "avg_shot_s", "visual_change_s", "caption_interval_s", "beats_n", "shots_n", "title_words", "outlier_score", "views"]:
        out["median_" + k] = med(k)
    for k in ["title_has_you", "title_question", "title_number", "title_caps_word", "title_emoji_or_ellipsis", "title_is_hashtags"]:
        out["pct_" + k] = round(100 * sum(1 for r in rows if r.get(k)) / max(1, len(rows)))
    out["pct_thumb_text"] = round(100 * sum(1 for r in rows if r["thumbnail_text"] and not re.match(r"(?i)none|no text|n/a", r["thumbnail_text"])) / max(1, len(rows)))
    mix = {}
    for r in rows:
        for k, v in r["shot_mix"].items():
            mix[k] = mix.get(k, 0) + v
    out["shot_mix_mean"] = {k: round(v / max(1, len(rows)), 3) for k, v in sorted(mix.items(), key=lambda kv: -kv[1])}
    return out


def main():
    rows = [row_for(d) for d in load()]
    rows.sort(key=lambda r: (r["niche"], -(r["outlier_score"] or 0)))
    lib = {
        "generated_by": "research/library/build_library.py",
        "count": len(rows),
        "counts": {},
        "fields": "one row per analysed video; paths are relative to the repo root",
        "videos": rows,
    }
    stats = {}
    for n in sorted({r["niche"] for r in rows}):
        nr = [r for r in rows if r["niche"] == n]
        lib["counts"][n] = {"total": len(nr), "outlier": sum(r["role"] == "outlier" for r in nr), "control": sum(r["role"] == "control" for r in nr)}
        stats[n] = {}
        for role in ["outlier", "control"]:
            stats[n][role] = agg([r for r in nr if r["role"] == role])
        for fmt in ["9:16", "16:9"]:
            for role in ["outlier", "control"]:
                sub = [r for r in nr if r["role"] == role and r["format"] == fmt]
                if sub:
                    stats[n][f"{role}_{fmt}"] = agg(sub)
    json.dump(lib, open(os.path.join(HERE, "library.json"), "w"), indent=1, ensure_ascii=False)
    json.dump(stats, open(os.path.join(HERE, "stats.json"), "w"), indent=1, ensure_ascii=False)
    write_index(lib, stats)
    print("library.json:", len(rows), "rows", lib["counts"])
    print("INDEX.md written")


def _lnk(path_from_root, label):
    if not path_from_root:
        return ""
    return f"[{label}]({os.path.relpath(os.path.join(ROOT, path_from_root), HERE)})"


def _md(x):
    return (x or "").replace("|", "/").replace("\n", " ")


def _fmt(v, nd=0):
    if v is None:
        return "-"
    if isinstance(v, float):
        return f"{v:.{nd}f}" if nd else f"{v:.0f}"
    return str(v)


def _views(v):
    if not v:
        return "-"
    return f"{v/1e6:.1f}M" if v >= 1e6 else f"{v/1e3:.0f}K"


NICHE_TITLES = {
    "explainer": "Explainer: ocean/animal \"you vs X\"",
    "horror": "Horror: phone-chat and animated story",
    "whatif": "What-if",
}


def write_index(lib, stats):
    rows = lib["videos"]
    L = []
    L.append("# Research library index")
    L.append("")
    L.append(f"{lib['count']} analysed videos: " + ", ".join(
        f"{n} {c['total']} ({c['outlier']} outliers / {c['control']} controls)" for n, c in lib["counts"].items()) + ".")
    L.append("")
    L.append("Generated by `research/library/build_library.py` from `videos/*.json`. The cross-video notes come from `index_notes/<niche>.md`. "
             "Machine-readable versions are `library.json` (one row per video with key fields and paths) and `stats.json` (medians by niche, role and format). "
             "**Outlier score** = views / channel median views. Controls are ordinary uploads (about 1x) from the same or similar channels. "
             "Pilot QA reference frames are in `review-refs/` (see `review-refs/<niche>/README.md` and `scripts/side_by_side.sh`).")
    L.append("")
    L.append("Columns: **analysis** = full JSON (hook, beats, shot list, pacing, techniques); **tx** = timestamped transcript; "
             "**sheet** = contact sheet; **corpus** = line-by-line annotated script in `research/corpus/`; **refs** = QA frames.")
    L.append("")
    L.append("Contents: " + " · ".join(f"[{NICHE_TITLES.get(n, n)}](#{n})" for n in lib["counts"]))
    L.append("")
    for n in lib["counts"]:
        nr = [r for r in rows if r["niche"] == n]
        L.append(f'<a id="{n}"></a>')
        L.append(f"## {NICHE_TITLES.get(n, n)}")
        L.append("")
        L.append("| # | Score | Role | Views | Fmt | Dur | Channel | Title | Hook device | Files |")
        L.append("|---|---|---|---|---|---|---|---|---|---|")
        for i, r in enumerate(sorted(nr, key=lambda r: -(r["outlier_score"] or 0)), 1):
            p = r["paths"]
            files = " ".join(x for x in [
                _lnk(p["analysis"], "analysis"), _lnk(p["transcript"], "tx"),
                _lnk(p["sheets"][0] if p["sheets"] else None, "sheet"), _lnk(p["corpus_annotation"], "corpus"),
                _lnk(os.path.dirname(p["review_ref_frames"][0]) if p["review_ref_frames"] else None, "refs")] if x)
            d = r["duration_s"] or 0
            dur = f"{int(d//60)}:{int(d%60):02d}"
            hook = _md(r["hook_device"])[:110] + ("…" if len(r["hook_device"] or "") > 110 else "")
            L.append(f"| {i} | **{r['outlier_score']}** | {r['role']} | {_views(r['views'])} | {r['format']} | {dur} | {_md(r['channel'])} | "
                     f"[{_md(r['title'])[:70]}]({r['url']}) | {hook} | {files} |")
        L.append("")
        L.append("**Measured medians** (from `stats.json`; wpm for caption-only Shorts counts on-screen words):")
        L.append("")
        keys = [k for k in ["outlier_9:16", "control_9:16", "outlier_16:9", "control_16:9"] if k in stats[n]]
        L.append("| Metric | " + " | ".join(k.replace("_", " ") + f" (n={stats[n][k]['n']})" for k in keys) + " |")
        L.append("|---|" + "---|" * len(keys))
        metrics = [("Duration s", "median_duration_s", 0), ("Words/min", "median_words_per_min", 0),
                   ("Avg shot / hard-cut s", "median_avg_shot_s", 1), ("Caption card s", "median_caption_interval_s", 1),
                   ("Beats", "median_beats_n", 0), ("Views", "median_views", None),
                   ("Title has 'you' %", "pct_title_has_you", 0), ("Title question %", "pct_title_question", 0),
                   ("Title has number %", "pct_title_number", 0), ("Title hashtag-only %", "pct_title_is_hashtags", 0),
                   ("Thumbnail has text %", "pct_thumb_text", 0)]
        for lab, k, nd in metrics:
            vals = []
            for kk in keys:
                v = stats[n][kk].get(k)
                vals.append(_views(v) if nd is None else _fmt(v, nd))
            L.append(f"| {lab} | " + " | ".join(vals) + " |")
        mixrow = []
        for kk in keys:
            m = stats[n][kk]["shot_mix_mean"]
            mixrow.append(", ".join(f"{a} {round(b*100)}%" for a, b in [kv for kv in m.items() if kv[0] != "other"][:5]))
        L.append("| Shot mix (screen time) | " + " | ".join(mixrow) + " |")
        L.append("")
        notes = os.path.join(HERE, "index_notes", f"{n}.md")
        if os.path.exists(notes):
            L.append(open(notes).read().strip())
            L.append("")
    open(os.path.join(HERE, "INDEX.md"), "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
