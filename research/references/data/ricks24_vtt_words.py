"""YouTube en-orig .vtt -> {id: [{text, start, cue_end}]} for ricks24_beats_build.py. usage: python3 -I ricks24_vtt_words.py SUBS_DIR OUT.json"""
import json, re, sys, glob, os
ts = lambda s: sum(float(x) * m for x, m in zip(s.split(":")[::-1], (1, 60, 3600)))
def parse(path):
    words, cue_t, cue_e = [], None, None
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        m = re.match(r"([\d:.]+) --> ([\d:.]+)", line)
        if m:
            cue_t, cue_e = ts(m.group(1)), ts(m.group(2)); continue
        if cue_t is None or "<c>" not in line: continue
        parts = re.split(r"<(\d+:\d+:\d+\.\d+)>", line)
        t = cue_t
        for k, p in enumerate(parts):
            if k % 2 == 1: t = ts(p); continue
            txt = re.sub(r"</?c[^>]*>", "", p).strip()
            for j, w in enumerate(txt.split()):
                words.append({"text": w, "start": round(t + 0.01 * j, 3), "cue_end": round(cue_e, 3)})
    return words
if __name__ == "__main__":
    out = {}
    for f in sorted(glob.glob(sys.argv[1] + "/*.en-orig.vtt")):
        vid = os.path.basename(f).split(".")[0]
        out[vid] = parse(f)
    json.dump(out, open(sys.argv[2], "w"))
    print({k: len(v) for k, v in out.items()})
