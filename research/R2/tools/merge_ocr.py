"""Merge sharded OCR json -> deduped caption timeline + panel text.
python -I merge_ocr.py prefix out_captions.txt out_panel.txt"""
import json, sys, glob, difflib
prefix, out_c, out_p = sys.argv[1:4]
rows = []
for f in sorted(glob.glob(prefix + "_*.json")):
    rows += json.load(open(f))
rows.sort(key=lambda r: r["t"])
caps, last = [], ""
for r in rows:
    c = r["caption"].strip()
    if not c:
        continue
    if difflib.SequenceMatcher(None, c.lower(), last.lower()).ratio() > 0.8:
        if len(c) > len(caps[-1][1]):
            caps[-1] = (caps[-1][0], c)
        last = c
        continue
    caps.append((r["t"], c)); last = c
with open(out_c, "w") as f:
    for t, c in caps:
        f.write(f"[{int(t//60)}:{t%60:04.1f}] {c}\n")
pan, lastp = [], ""
for r in rows:
    p = r.get("panel", "").strip()
    if p and difflib.SequenceMatcher(None, p, lastp).ratio() < 0.7:
        pan.append((r["t"], p)); lastp = p
with open(out_p, "w") as f:
    for t, p in pan:
        f.write(f"[{int(t//60)}:{t%60:04.1f}] {p}\n")
print(len(caps), len(pan))
