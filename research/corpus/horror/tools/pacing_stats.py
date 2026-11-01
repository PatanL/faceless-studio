#!/usr/bin/env python3
"""Pacing stats for the horror corpus (raw/*.txt, raw/_alt/*.txt) and library controls.

Usage: python3 -I pacing_stats.py <out.json>
Reads only local text files. Prints a table and writes JSON.
"""
import html
import json
import pathlib
import re
import statistics as st
import sys

ROOT = pathlib.Path('/Users/patrickliu/Documents/faceless-studio/research')
CORP = ROOT / 'corpus/horror/raw'
LIB_T = ROOT / 'library/transcripts'
LIB_V = ROOT / 'library/videos'

# library horror transcripts used as same-channel / same-format comparisons
CONTROLS = ['7696062340852190496', '7665304797242821921', 'xKgepVHATm4', 'epzTfKxp16E',
            'KJfJKo400b0', 'dqEIz_8bP-8', '0xzpKw7To98']
# extra library outliers (not in the 12) for a bigger "hit" pool
CHAT_IDS = {'T42u5xhrq-0', 'gzXY52lcAcI', '0xzpKw7To98', 'Xv32FAAUI-0', 'wh9ESTS69Dk'}  # one bubble = one sentence
# expansion (12:08 UTC): corpus files that are controls, and the ids that came with the expansion
CORPUS_CONTROLS = {'FDLk6TlVTq0'}
EXPANSION = {'wh9ESTS69Dk', '8bo9yZvedUM', '7650872317119057168', 'gDNMSoGSZgQ', 'kJCVK8xTkPk', '7659482056656735521',
             'x--ui6_mAxE', 'shTJ7_kRNJ8', '02nCBx8WqW0', '6WfCF7KsLaQ', 'hPWu7UAovxk', 'cWgSgd-QcOY', 'FDLk6TlVTq0'}
EXTRA_HITS = ['7664930759395888416', '7666044652910316833', 'Xv32FAAUI-0', 'tB9Ln4eINus', 'CQKPC9MlciE']

NUMWORDS = set('one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen '
               'seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred thousand '
               'million billion half twice dozen dozens first second third fourth fifth midnight'.split())
YOU = set("you your you're yours yourself you'd you'll you've ya".split())
ME = set("i i'm i'd i'll i've me my mine myself we we're our us".split())
RULE_RE = re.compile(r"\b(never|don't|do not|must|rule|rules|always|no matter|whatever you do|remember)\b", re.I)
TURN_RE = re.compile(r"\b(but|suddenly|just then|right then|until|then i|that's when|turns out|wait)\b", re.I)


def ts(s):
    s = s.split('-')[0]
    p = s.split(':')
    p = [float(x) for x in p]
    if len(p) == 2:
        return p[0] * 60 + p[1]
    return p[0] * 3600 + p[1] * 60 + p[2]


def clean(t):
    t = html.unescape(t)
    t = re.sub(r"^\d\d:\d\d:\d\d\.\d+\s*-->\s*\d\d:\d\d:\d\d\.\d+\s*", "", t)
    t = re.sub(r"\[[^\]]*\]", " ", t)          # [music], [title card], [LOCK SCREEN ...]
    t = re.sub(r"\([^)]*\)", " ", t)            # (auto-sub notes)
    t = t.replace('>>', ' ').replace('—', ' ')
    t = re.sub(r"^\s*[A-Z][A-Za-z .'\-]{0,24}:\s+", "", t)   # speaker labels in chat transcripts
    return re.sub(r"\s+", " ", t).strip()


def parse(path):
    chat = path.stem in CHAT_IDS
    segs, prev = [], None
    for ln in path.read_text(errors='ignore').splitlines():
        m = re.match(r"\s*\[(\d+:\d+(?::\d+)?(?:\.\d+)?(?:-\d+:\d+(?:\.\d+)?)?)\]\s*(.*)", ln)
        if not m:
            continue
        txt = clean(m.group(2))
        if not txt or txt == prev:
            continue
        prev = txt
        if chat and not re.search(r"[.?!…]$", txt):
            txt += '.'
        segs.append((ts(m.group(1)), txt))
    return segs


def metrics(segs, dur):
    text = ' '.join(s for _, s in segs)
    toks = [w.lower().strip(".,!?\"'") for w in re.findall(r"[A-Za-z0-9][A-Za-z0-9',.%$:]*", text)]
    toks = [t for t in toks if t]
    n = len(toks)
    mins = dur / 60
    sents = [s.strip() for s in re.split(r"(?<=[.?!])\s+", text) if re.search(r"[A-Za-z]", s)]
    slen = [len(re.findall(r"[A-Za-z0-9']+", s)) for s in sents]
    you_s = sum(1 for s in sents if YOU & set(re.findall(r"[a-z']+", s.lower())))
    you_w = sum(1 for t in toks if t in YOU)
    me_w = sum(1 for t in toks if t in ME)
    nums = sum(1 for t in toks if re.search(r"\d", t) or t in NUMWORDS)
    qs = sum(1 for s in sents if s.endswith('?'))
    rules = len(RULE_RE.findall(text))
    turns = len(TURN_RE.findall(text))
    short = sum(1 for l in slen if l <= 4)
    first10 = ' '.join(s for t, s in segs if t < 10)
    f10 = len(re.findall(r"[A-Za-z0-9']+", first10))
    return dict(words=n, wpm=round(n / mins, 1), sent_n=len(sents),
                sent_mean=round(st.mean(slen), 1) if slen else 0,
                sent_median=st.median(slen) if slen else 0,
                pct_you_sent=round(100 * you_s / max(1, len(sents)), 1),
                you_per100w=round(100 * you_w / max(1, n), 1),
                me_per100w=round(100 * me_w / max(1, n), 1),
                nums_per_min=round(nums / mins, 1), q_per_min=round(qs / mins, 1),
                rule_words_per_min=round(rules / mins, 1), turn_words_per_min=round(turns / mins, 1),
                punch_pct=round(100 * short / max(1, len(sents)), 1), words_first10s=f10)


def corpus_entry(p):
    head = p.read_text(errors='ignore').splitlines()[0]
    parts = [x.strip() for x in head.lstrip('# ').split('|')]
    mm, ss = parts[-1].split(':')
    dur = int(mm) * 60 + int(ss)
    m = metrics(parse(p), dur)
    m.update(id=p.stem, views=int(parts[-3]), outlier=float(parts[-2]), dur=dur, channel=parts[-4])
    return m


def lib_entry(vid):
    v = json.load(open(LIB_V / f'{vid}.json'))
    p = LIB_T / f'{vid}.txt'
    m = metrics(parse(p), float(v['duration']))
    m.update(id=vid, views=v['views'], outlier=v['outlier_score'], dur=v['duration'], channel=v['channel'])
    return m


def main():
    out = {'corpus': {}, 'alt': {}, 'extra_hits': {}, 'controls': {}}
    for p in sorted(CORP.glob('*.txt')):
        if p.stem in CORPUS_CONTROLS:
            out['controls'][p.stem] = corpus_entry(p)
        else:
            out['corpus'][p.stem] = corpus_entry(p)
    for p in sorted((CORP / '_alt').glob('*.txt')):
        out['alt'][p.stem] = corpus_entry(p)
    for vid in EXTRA_HITS:
        out['extra_hits'][vid] = lib_entry(vid)
    for vid in CONTROLS:
        out['controls'][vid] = lib_entry(vid)
    keys = ['wpm', 'sent_mean', 'sent_median', 'pct_you_sent', 'you_per100w', 'me_per100w', 'nums_per_min',
            'q_per_min', 'rule_words_per_min', 'turn_words_per_min', 'punch_pct', 'words_first10s']
    # medians per group
    summary = {}
    for g, d in out.items():
        if not d:
            continue
        summary[g] = {k: {'median': st.median([m[k] for m in d.values()]),
                          'min': min(m[k] for m in d.values()), 'max': max(m[k] for m in d.values())} for k in keys}
    # sub-groups of the corpus hits: the first 12 vs the expansion
    for g, sel in [('corpus_orig12', lambda k: k not in EXPANSION), ('corpus_expansion', lambda k: k in EXPANSION)]:
        d = {k: v for k, v in out['corpus'].items() if sel(k)}
        summary[g] = {k: {'median': st.median([m[k] for m in d.values()]),
                          'min': min(m[k] for m in d.values()), 'max': max(m[k] for m in d.values())} for k in keys}
    out['summary'] = summary
    json.dump(out, open(sys.argv[1], 'w'), indent=1)
    for g in ['corpus', 'alt', 'extra_hits', 'controls']:
        print(g.upper())
        for k, m in sorted(out[g].items(), key=lambda kv: -kv[1]['outlier']):
            print(f"{k:20s} {m['channel'][:14]:14s} x{m['outlier']:<6} {int(m['dur']):4d}s {m['words']:5d}w "
                  + ' '.join(f"{x}={m[x]}" for x in keys))
    print('SUMMARY (median [min-max])')
    for g, s in summary.items():
        print(g, ' '.join(f"{k}={v['median']}[{v['min']}-{v['max']}]" for k, v in s.items()))


main()
