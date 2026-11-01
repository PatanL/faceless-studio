#!/usr/bin/env python3
"""VO timeline from vo_lines.json + durations.json (Kokoro, measured on the Spark).

usage: python3 timing.py [--md]   -> prints stats (and with --md the timestamped VO section for script.md)
Writes timeline.json: [{id, beat, start, end, text, screen, words: [[w, abs_start, abs_end]]}]
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
spec = json.load(open(os.path.join(HERE, "vo_lines.json")))
dur = json.load(open(os.path.join(HERE, "durations.json")))
LEAD = 0.2      # silence before the first word (frame 0 is the hook image)
TAIL = 0.6      # after the last line
t = LEAD
tl = []
for ln in spec["lines"]:
    d = dur[ln["id"]]
    s = round(t, 2)
    e = round(t + d["dur"], 2)
    tl.append({**{k: ln[k] for k in ("id", "beat", "text", "screen")}, "start": s, "end": e, "pause": ln["pause"],
               "words": [[w, round(s + a, 3), round(s + b, 3)] for w, a, b in d["words"]]})
    t = e + ln["pause"]
total = round(tl[-1]["end"] + TAIL, 2)
json.dump({"total": total, "lines": tl}, open(os.path.join(HERE, "timeline.json"), "w"), indent=1, ensure_ascii=False)

def mmss(x):
    return f"{int(x // 60)}:{x % 60:04.1f}"

words = [w for ln in tl for w in re.findall(r"[A-Za-z0-9'’,\-]+", ln["text"]) if re.search(r"[A-Za-z0-9]", w)]
nw = len(words)
sents = [s for ln in tl for s in re.split(r"(?<=[.?!])\s+", ln["text"]) if s.strip()]
you_s = sum(1 for s in sents if re.search(r"\byou(r|'re|'d|'ll|rs|rself)?\b", s, re.I))
you_w = sum(1 for w in words if re.fullmatch(r"you(r|'re|'d|'ll|rs|rself)?", w.lower().replace("’", "'")))
nums = sum(1 for w in words if re.search(r"\d", w) or w.lower().strip(",") in {
    "two","three","four","five","six","ten","fifteen","twenty-five","thirty","thirty-five","thirty-eight","forty",
    "forty-five","fifty","sixteen","eighteen","hundred","sixty","million","eighty"})
speech = sum(ln["end"] - ln["start"] for ln in tl)
print(f"lines {len(tl)}  words {nw}  total {total:.1f}s ({mmss(total)})  overall wpm {nw / total * 60:.0f}  speech-only wpm {nw / speech * 60:.0f}")
print(f"sentences {len(sents)}  avg {nw / len(sents):.1f} words  you-sentences {you_s / len(sents) * 100:.0f}%  you-words {you_w / nw * 100:.1f}%  numbers/min {nums / total * 60:.1f}")
for key in ("B1", "R5", "W11", "K11", "X1", "U1", "G1", "S1", "S13", "V1", "V3", "E1", "C1"):
    ln = next(l for l in tl if l["id"] == key)
    print(f"  {key:4} {mmss(ln['start'])}  {ln['start'] / total * 100:4.1f}%")
hook = [l for l in tl if l["id"] in ("H1", "H2")]
hw = sum(len(l["text"].split()) for l in hook)
print(f"hook {hw} words, ends {hook[-1]['end']:.1f}s")
if "--md" in sys.argv:
    cur = None
    for ln in tl:
        if ln["beat"] != cur:
            cur = ln["beat"]
            print(f"\n#### [{cur}] {mmss(ln['start'])}\n")
        print(f"- **{ln['id']} · {mmss(ln['start'])}–{mmss(ln['end'])}** {ln['text']}" + ("  " if ln["screen"] else ""))
        if ln["screen"]:
            print(f"  ON SCREEN: `{ln['screen']}`")
