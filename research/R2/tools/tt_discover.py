"""Fetch TikTok /discover/<slug> pages (server-rendered) and pull video/author stats.
Run on Spark: python -I tt_discover.py slug1 slug2 ... > out.jsonl
"""
import json, re, sys
from curl_cffi import requests

for slug in sys.argv[1:]:
    url = f"https://www.tiktok.com/discover/{slug}"
    try:
        r = requests.get(url, impersonate="chrome", timeout=30)
    except Exception as e:
        print(json.dumps({"slug": slug, "error": str(e)})); continue
    m = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>', r.text, re.S)
    if not m:
        print(json.dumps({"slug": slug, "status": r.status_code, "error": "no data"})); continue
    data = json.loads(m.group(1))
    found = []
    def walk(o):
        if isinstance(o, dict):
            if "stats" in o and "author" in o and "id" in o:
                a = o["author"] if isinstance(o["author"], dict) else {"uniqueId": o["author"]}
                st = o.get("stats") or {}
                found.append({"id": o["id"], "author": a.get("uniqueId"), "desc": o.get("desc", "")[:150],
                              "views": st.get("playCount"), "likes": st.get("diggCount"),
                              "duration": (o.get("video") or {}).get("duration"), "createTime": o.get("createTime")})
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(data)
    print(json.dumps({"slug": slug, "status": r.status_code, "n": len(found), "videos": found}, ensure_ascii=False))
