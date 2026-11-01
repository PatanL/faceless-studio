import re, json, statistics as st, sys
R = '/Users/patrickliu/Documents/faceless-studio/research/'
C = R + 'corpus/explainer/'

def tsec(s):
    p = [float(x) for x in s.split(':')]
    return p[0]*60+p[1] if len(p) == 2 else p[0]*3600+p[1]*60+p[2]

def load(path, skip_hash=True, first_header=False):
    lines = open(path).read().splitlines()
    if first_header: lines = lines[1:]
    out = []; last = 0
    for ln in lines:
        if ln.startswith('#'): continue
        m = re.match(r'^\[(\d+:\d+(?::\d+)?(?:\.\d+)?)\]\s*(.*)$', ln)
        if m:
            last = tsec(m.group(1)); out.append((last, m.group(2)))
        elif ln.strip():
            out.append((last, ln))
    return out

NUMW = set('one two three four five six seven eight nine ten eleven twelve twenty thirty forty fifty hundred hundreds thousand thousands million millions billion billions dozen dozens half quarter percent'.split())
YOU = set("you your you're youre yourself you'd you'll you've yours ya".split())

def stats(id, path, dur, header=False, speech_end=None):
    rows = load(path, first_header=header)
    text = ' '.join(t for _, t in rows)
    text = re.sub(r'\[[^\]]*\]', ' ', text)
    words = re.findall(r"[A-Za-z0-9][A-Za-z0-9'’,.\-]*", text)
    wl = [w.lower().strip(".,'’").replace('’', "'") for w in words]
    n = len(wl)
    end = speech_end or (rows[-1][0] + 2.5 if rows else dur)
    end = min(end, dur)
    start = rows[0][0] if rows else 0
    span = max(end - start, 1)
    you = sum(1 for w in wl if w in YOU)
    nums = sum(1 for w in wl if re.match(r'^\d', w) or w in NUMW)
    sents = [s for s in re.split(r'[.!?]+', text) if len(s.split()) > 0]
    sl = [len(s.split()) for s in sents]
    # sentences with "you"
    sy = sum(1 for s in sents if any(w.lower().strip(".,'’").replace('’', "'") in YOU for w in s.split()))
    return dict(id=id, dur=dur, words=n, wpm=round(n / span * 60), you_pct=round(100 * you / n, 1),
                you_per_min=round(you / span * 60, 1), nums_per_min=round(nums / span * 60, 1),
                sent_avg=round(st.mean(sl), 1) if sl else None, sent_med=st.median(sl) if sl else None,
                n_sent=len(sl), you_sent_pct=round(100 * sy / len(sl)) if sl else None)

corpus = {
 'fGcgWaswMns': 599, 'nAWpLtG-kNs': 970, 'VtrcKTkhDHU': 2022, 'mzeN0BXR4e0': 1077, 'JkAcCdqYJN0': 551,
 'QxM2Hu70tVk': 529, 'XFFjxTllpoA': 59, 'jw6bS-WL4F4': 58, 'Ky0XPonYDcc': 40, '4QGQhaRv4Dw': 37.5,
 'fmZfphacPPQ': 33, '6mRR91AbxjQ': 27.6}
out = {}
for k, d in corpus.items():
    out[k] = stats(k, C + 'raw/' + k + '.txt', d)
controls = {
 'U35yA-9nVEA': (R + 'library/transcripts/U35yA-9nVEA.txt', 57, True),
 'XffxtLGdXUQ': (R + 'library/transcripts/XffxtLGdXUQ.txt', 25.4, True),
 '2819-mQEA9M': (R + 'R1/subs/2819-mQEA9M.transcript.txt', 596, False),
 '4Mmo_dlsArE': (R + 'R1/subs/4Mmo_dlsArE.transcript.txt', 652, False),
 'mg2YJ04Hl9k': (R + 'R1/subs/mg2YJ04Hl9k.transcript.txt', 1181, False),
 'JavhxLs3Cs8': (R + 'library/transcripts/JavhxLs3Cs8.txt', 600, True),
 'uH-hucq-dmA': (R + 'library/transcripts/uH-hucq-dmA.txt', 1920, True),
}
for k, (p, d, h) in controls.items():
    out[k] = stats(k, p, d, header=h)

# open loops counted from annotation tables
def loops(id):
    s = open(C + id + '.md').read()
    m = re.search(r'###? Open loops[^\n]*\n(.*?)(\n###|\n## )', s, re.S)
    if not m:
        m2 = re.search(r'\*\*Open loops:\*\*(.*?)\n- \*\*', s, re.S)
        return None
    rows = [l for l in m.group(1).splitlines() if l.startswith('|') and not re.match(r'^\|\s*-', l)]
    return max(len(rows) - 1, 0)
for k in corpus:
    L = loops(k); out[k]['loops'] = L
    if L: out[k]['loops_per_min'] = round(L / (corpus[k] / 60), 2)
json.dump(out, open(sys.argv[1], 'w'), indent=1)
for k, v in out.items(): print(v)
