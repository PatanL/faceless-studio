"""Clean YouTube auto-sub VTT -> '[mm:ss] line' with rolling-caption dedupe.
Uses word-level <timestamp> tags when present: each new word gets its own time; lines are
built by grouping words into sentences/phrases (break on gap > 0.9s or 14 words)."""
import re, sys
def ts(s):
    h, m, r = s.split(':'); return int(h)*3600 + int(m)*60 + float(r)
def words_from_vtt(path):
    txt = open(path, encoding='utf-8').read()
    blocks = re.split(r'\n\n+', txt)
    words = []
    for b in blocks:
        m = re.match(r'(\d\d:\d\d:\d\d\.\d+) --> (\d\d:\d\d:\d\d\.\d+)', b)
        if not m: continue
        start = ts(m.group(1))
        lines = b.split('\n')[1:]
        for ln in lines:
            if '<c>' not in ln and not re.search(r'<\d\d:', ln): continue
            # first word before first tag has block start time
            parts = re.split(r'(<\d\d:\d\d:\d\d\.\d+>)', ln)
            t = start
            for p in parts:
                mm = re.match(r'<(\d\d:\d\d:\d\d\.\d+)>', p)
                if mm: t = ts(mm.group(1)); continue
                w = re.sub(r'</?c[^>]*>', '', p).strip()
                for ww in w.split():
                    words.append((t, ww))
    if not words:  # no word timing: fall back to cue text, drop repeated lines
        last = None
        for b in blocks:
            m = re.match(r'(\d\d:\d\d:\d\d\.\d+) -->', b)
            if not m: continue
            for ln in b.split('\n')[1:]:
                ln = re.sub(r'<[^>]+>', '', ln).strip()
                if ln and ln != last:
                    for ww in ln.split(): words.append((ts(m.group(1)), ww))
                    last = ln
    return words
def group(words):
    out, cur, t0, lt = [], [], None, None
    for t, w in words:
        if cur and (t - lt > 0.9 or len(cur) >= 14):
            out.append((t0, ' '.join(cur))); cur = []
        if not cur: t0 = t
        cur.append(w); lt = t
        if re.search(r'[.?!]$', w) and len(cur) > 3:
            out.append((t0, ' '.join(cur))); cur = []
    if cur: out.append((t0, ' '.join(cur)))
    return out
if __name__ == '__main__':
    for t, line in group(words_from_vtt(sys.argv[1])):
        print(f"[{int(t//60):02d}:{int(t%60):02d}] {line}")
