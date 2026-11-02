"""Flatten a YouTube .vtt (manual or rolling auto-captions) into timestamped narration lines.

usage: python3 -I vtt_lines.py <file.vtt> [--every 5]   -> prints "m:ss.s  text" chunks of ~N seconds
Rolling auto-captions repeat each line; only words not already printed are kept.
"""
import re, sys, argparse
ap = argparse.ArgumentParser(); ap.add_argument("vtt"); ap.add_argument("--every", type=float, default=5.0)
a = ap.parse_args()
ts = lambda s: sum(float(x) * m for x, m in zip(s.replace(",", ".").split(":")[::-1], (1, 60, 3600)))
cues = []; cur = None
for line in open(a.vtt, encoding="utf-8"):
    line = line.strip()
    m = re.match(r"([\d:.]+) --> ([\d:.]+)", line)
    if m: cur = [ts(m.group(1)), []]; cues.append(cur); continue
    if cur is not None and line and not line.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")):
        cur[1].append(re.sub(r"<[^>]+>", "", line))
words = []; seen_tail = ""
for t, lines in cues:
    txt = " ".join(lines).strip()
    if not txt: continue
    if seen_tail and txt.startswith(seen_tail):        # rolling duplicate
        new = txt[len(seen_tail):].strip()
    elif txt in seen_tail:
        new = ""
    else:
        new = txt
    if new: words.append((t, new))
    seen_tail = lines[-1].strip() if lines else ""
    if len(lines) > 1 and txt.startswith(" ".join(lines[:-1])): seen_tail = lines[-1].strip()
out = []; t0 = None; buf = []
for t, w in words:
    if t0 is None: t0 = t
    buf.append(w)
    if t - t0 >= a.every:
        out.append((t0, " ".join(buf))); t0 = None; buf = []
if buf: out.append((t0, " ".join(buf)))
for t, s in out: print(f"{int(t // 60)}:{t % 60:04.1f}  {s}")
