#!/usr/bin/env python3
"""Pacing stats for whatif corpus (raw/*.txt) and R3 control transcripts."""
import json, re, statistics as st, sys, pathlib, html

ROOT = pathlib.Path('/Users/patrickliu/Documents/faceless-studio/research')
CORP = ROOT / 'corpus/whatif/raw'
R3T = ROOT / 'R3/transcripts'

NUMWORDS = set('two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred thousand million billion trillion half twice double triple percent dozen quarter'.split())
YOU = set("you your you're yours yourself you'd you'll you've".split())
PIVOT_RE = re.compile(r"\b(but|except|until|however|instead|and then|here's|turns out|problem|wait|or so)\b", re.I)


def clean(t):
    t = html.unescape(t)
    t = re.sub(r"\[(music|laughter|snorts|applause|clears throat|[a-z ]+)\]", " ", t, flags=re.I)
    t = t.replace('>>', ' ').replace('—', ' ')
    return re.sub(r"\s+", " ", t).strip()


def ts(s):
    p = [int(x) for x in s.split(':')]
    return p[0] * 60 + p[1] if len(p) == 2 else p[0] * 3600 + p[1] * 60 + p[2]


def parse(path):
    lines = path.read_text(errors='ignore').splitlines()
    segs = []
    for ln in lines:
        m = re.match(r"\[(\d+:\d+(?::\d+)?)\]\s*(.*)", ln.strip())
        if m:
            segs.append((ts(m.group(1)), clean(m.group(2))))
    return segs


def metrics(segs, dur):
    text = ' '.join(s for _, s in segs)
    words = re.findall(r"[A-Za-z0-9][A-Za-z0-9',.%$]*", text)
    toks = [w.lower().strip(".,") for w in words]
    n = len(toks)
    mins = dur / 60
    sents = [s.strip() for s in re.split(r"(?<=[.?!])\s+", text) if re.search(r"[A-Za-z]", s)]
    slen = [len(re.findall(r"[A-Za-z0-9']+", s)) for s in sents]
    you_s = sum(1 for s in sents if YOU & set(re.findall(r"[a-z']+", s.lower())))
    you_w = sum(1 for t in toks if t in YOU)
    nums = sum(1 for t in toks if re.search(r"\d", t) or t in NUMWORDS)
    qs = sum(1 for s in sents if s.endswith('?'))
    piv = len(PIVOT_RE.findall(text))
    short = sum(1 for l in slen if l <= 3)
    # first 30 s
    f30 = ' '.join(s for t, s in segs if t < 30)
    f30w = re.findall(r"[A-Za-z0-9']+", f30.lower())
    return dict(words=n, wpm=round(n / mins, 1), sent_n=len(sents),
                sent_mean=round(st.mean(slen), 1) if slen else 0,
                sent_median=st.median(slen) if slen else 0,
                pct_you_sent=round(100 * you_s / max(1, len(sents)), 1),
                you_per100w=round(100 * you_w / max(1, n), 1),
                nums_per_min=round(nums / mins, 1), q_per_min=round(qs / mins, 2),
                pivots_per_min=round(piv / mins, 2), punch_pct=round(100 * short / max(1, len(sents)), 1),
                f30_you=sum(1 for w in f30w if w in YOU), f30_nums=sum(1 for w in f30w if re.search(r'\d', w) or w in NUMWORDS))


def main():
    out = {}
    # corpus long-form
    for p in sorted(CORP.glob('*.txt')):
        head = p.read_text(errors='ignore').splitlines()[0]
        parts = [x.strip() for x in head.lstrip('# ').split('|')]
        dur = int(parts[5].rstrip('s'))
        segs = parse(p)
        if 'tiktok' in parts[0]:
            caps = [(t, re.sub(r'^(CAPTION|TITLE|END|END fact|HUD|HUD subline):\s*', '', s)) for t, s in segs if re.match(r'(CAPTION):', s)]
            alltext = [(t, re.sub(r'\(.*?\)', '', re.sub(r'^[A-Z ]+?:\s*', '', s))) for t, s in segs if re.match(r'(CAPTION|TITLE|END|END fact|HUD|HUD subline):', s)]
            cw = [len(re.findall(r"[A-Za-z0-9π']+", s)) for _, s in caps]
            times = [t for t, _ in caps]
            gaps = [b - a for a, b in zip(times, times[1:])]
            elem_times = sorted(set(t for t, s in segs))
            m = metrics(alltext, dur)
            capm = metrics(caps, dur)
            m.update(dict(captions=len(caps), caption_words=sum(cw), caption_wpm=round(sum(cw) / (dur / 60), 1),
                          caption_len_mean=round(st.mean(cw), 1), caption_len_max=max(cw),
                          caption_gap_mean=round(st.mean(gaps), 1), caption_gap_median=st.median(gaps),
                          new_element_every_s=round(dur / len(elem_times), 1),
                          caption_you_pct=capm['pct_you_sent'], caption_nums=sum(1 for _, s in caps if re.search(r"\d", s))))
            m['format'] = 'short'
        else:
            m = metrics(segs, dur)
            m['format'] = 'long'
        m.update(id=p.stem, views=int(parts[3]), outlier=float(parts[4]), dur=dur, title=parts[1])
        out[p.stem] = m
    # controls (R3 transcripts)
    vids = {v['id']: v for v in json.load(open(ROOT / 'R3/raw/r3_videos.json'))}
    med = {'IFOLOGY': 103529, 'Awaken': 292226}
    ctrl = {}
    for p in sorted(R3T.glob('*.txt')):
        v = vids.get(p.stem)
        if not v or v['channel'] not in med or v['duration'] < 240:
            continue
        segs = parse(p)
        if not segs:
            continue
        m = metrics(segs, v['duration'])
        m.update(id=p.stem, views=v['views'], outlier=round(v['views'] / med[v['channel']], 2), dur=v['duration'], title=v['title'], channel=v['channel'])
        ctrl[p.stem] = m
    json.dump({'corpus': out, 'controls': ctrl}, open(sys.argv[1], 'w'), indent=1)
    keys = ['wpm', 'sent_mean', 'sent_median', 'pct_you_sent', 'you_per100w', 'nums_per_min', 'q_per_min', 'pivots_per_min', 'punch_pct', 'f30_you', 'f30_nums']
    print('CORPUS')
    for k, m in out.items():
        extra = '' if m['format'] == 'long' else ' caps=%d cw=%d capwpm=%.1f capmean=%.1f max=%d gap=%.1f/%s elem=%.1f capyou=%.0f capnums=%d' % (m['captions'], m['caption_words'], m['caption_wpm'], m['caption_len_mean'], m['caption_len_max'], m['caption_gap_mean'], m['caption_gap_median'], m['new_element_every_s'], m['caption_you_pct'], m['caption_nums'])
        print(k, m['format'], m['outlier'], m['dur'], m['words'], ' '.join('%s=%s' % (x, m[x]) for x in keys), extra)
    print('CONTROLS')
    for k, m in sorted(ctrl.items(), key=lambda kv: -kv[1]['outlier']):
        print(k, m['channel'], m['outlier'], m['dur'], m['words'], ' '.join('%s=%s' % (x, m[x]) for x in keys), m['title'][:45])


main()
