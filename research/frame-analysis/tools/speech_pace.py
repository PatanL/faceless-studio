"""Narration pace from word timings: words per second, pauses, the "You see," pivot and the first sentence.

usage: python -I speech_pace.py <words> [<words> ...] [--json out.json]
  <words> = a YouTube json3 caption track (word start times from tOffsetMs) or one of our captions.json files
            ({"words": [{"text", "start", "end"}]}).
Measures (start-to-start, so both sources are treated the same way):
  wps        words / (last word start - first word start + 0.3 s)
  gaps       start-to-start intervals >= 0.8 s (a pause after a word; median interval at ~4 wps is ~0.25 s)
  dead_air   sum over those gaps of (interval - 0.4 s)
  you_see    times of "you see" (case-insensitive), also as % of the narration
  first      the first sentence (up to the first . ! or ?)
"""
import argparse
import json
import os
import re


def load(path):
    d = json.load(open(path))
    if "words" in d:
        return [(w["text"], float(w["start"])) for w in d["words"]]
    out = []
    for ev in d.get("events", []):
        t0 = ev.get("tStartMs", 0)
        for s in ev.get("segs", []) or []:
            txt = s.get("utf8", "").strip()
            if txt and txt != "\n":
                for k, piece in enumerate(txt.split()):
                    out.append((piece, (t0 + s.get("tOffsetMs", 0)) / 1000.0 + 0.01 * k))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+"); ap.add_argument("--json", default=None)
    a = ap.parse_args()
    res = []
    for f in a.files:
        w = [x for x in load(f) if not re.fullmatch(r"\[.*\]", x[0])]
        t = [x[1] for x in w]
        span = t[-1] - t[0] + 0.3
        iv = [b - a_ for a_, b in zip(t[:-1], t[1:])]
        gaps = [(round(t[i], 2), round(g, 2)) for i, g in enumerate(iv) if g >= 0.8]
        text = " ".join(x[0] for x in w)
        low = [re.sub(r"[^a-z']", "", x[0].lower()) for x in w]
        ys = [round(w[i][1], 2) for i in range(len(w) - 1) if low[i] == "you" and low[i + 1] == "see"]
        m = re.search(r"^(.*?[.!?])(\s|$)", text)
        res.append(dict(file=os.path.basename(f), words=len(w), span_s=round(span, 2), wps=round(len(w) / span, 2),
                        median_interval=round(sorted(iv)[len(iv) // 2], 3), n_gaps_0_8=len(gaps),
                        dead_air_s=round(sum(g - 0.4 for _, g in gaps), 2), gaps=gaps,
                        you_see_t=ys, you_see_pct=[round(100 * (y - t[0]) / span, 1) for y in ys],
                        first=(m.group(1) if m else text[:160])))
    for r in res:
        print(json.dumps({k: v for k, v in r.items() if k != "gaps"}))
    if a.json:
        json.dump(res, open(a.json, "w"), indent=1)


if __name__ == "__main__":
    main()
