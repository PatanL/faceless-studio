"""Summarize yt-dlp flat-playlist jsonl files: count, median/max views, median duration, top videos.
python -I summarize_lists.py file1.jsonl ... -> prints JSON lines per file"""
import json, sys, statistics as st
for p in sys.argv[1:]:
    rows = [json.loads(l) for l in open(p) if l.strip()]
    if not rows:
        continue
    v = [r.get("view_count") or 0 for r in rows]
    d = [r.get("duration") or 0 for r in rows]
    top = sorted(rows, key=lambda r: -(r.get("view_count") or 0))[:5]
    print(json.dumps({
        "file": p, "n": len(rows), "median_views": st.median(v), "max_views": max(v),
        "mean_views": int(st.mean(v)), "median_dur": st.median(d),
        "top": [{"id": r["id"], "views": r.get("view_count"), "likes": r.get("like_count"), "dur": r.get("duration"),
                  "title": (r.get("title") or r.get("description") or "")[:100],
                  "url": r.get("url") or r.get("webpage_url")} for r in top]}, ensure_ascii=False))
