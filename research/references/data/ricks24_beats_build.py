"""Beat-map the 24 RicksClips3000 story Shorts -> research/references/data/ricks24_beats.json (text + timings only).

usage: python3 -I ricks24_beats_build.py WORKDIR REFDIR OUT.json
  WORKDIR: vttwords.json (ricks24_vtt_words.py), wt/<id>.json (faster-whisper medium.en int8 word timestamps, run on the Mac),
           pause_model.json = {"coef": [0.02383, 0.05276]} (word duration = a + b * chars, fit on the 8 whisper refs)
  REFDIR:  copy of dgx-spark:~/studio/refs/lanes/ricks/{meta,cuts.jsonl}
Manual coding (beats, jokes, reversals, facts, on-screen naming, dialogue) lives in ricks24_beats_ann.py."""
import json, re, os, sys, glob, difflib, statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ricks24_beats_ann import A, DIALOGUE
W, R, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
vtt = json.load(open(f"{W}/vttwords.json"))
PM = json.load(open(f"{W}/pause_model.json"))
dur = {json.loads(l)["file"].split(".")[0]: json.loads(l)["dur"] for l in open(f"{R}/cuts.jsonl")}
meta = {}
for f in glob.glob(f"{R}/meta/*.info.json"):
    d = json.load(open(f)); meta[d["id"]] = dict(title=d["title"], views=d["view_count"], upload_date=d["upload_date"], likes=d.get("like_count"))
order = sorted(meta, key=lambda k: -meta[k]["views"])
tier = {v: ("top" if i < 8 else "mid" if i < 16 else "bottom") for i, v in enumerate(order)}
norm = lambda s: re.sub(r"[^a-z0-9']", "", s.lower())
NUMW = set("one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred thousand million billion half twice dozen".split())

def words_for(vid):
    """Return words [{text,start,end,src}] and sentence boundaries (list of word-index lists)."""
    vw = [w for w in vtt[vid] if w["text"] != "[music]"]
    # VTT sentence split
    sents, cur = [], []
    for i, w in enumerate(vw):
        cur.append(i)
        if re.search(r'[.!?]["\']?$', w["text"]): sents.append(cur); cur = []
    if cur: sents.append(cur)
    wp = f"{W}/wt/{vid}.json"
    if not os.path.exists(wp):
        out = []
        for i, w in enumerate(vw):
            nxt = vw[i + 1]["start"] if i + 1 < len(vw) else w["start"] + 0.35
            out.append(dict(text=w["text"], start=w["start"], end=None, onset_next=round(nxt, 3)))
        return out, sents, "youtube_en_orig_vtt", None
    ww = json.load(open(wp))["words"]
    a = [norm(w["text"]) for w in vw]; b = [norm(w["text"]) for w in ww]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    m = {}
    for blk in sm.get_matching_blocks():
        for k in range(blk.size): m[blk.a + k] = blk.b + k
    errs = [abs(vw[i]["start"] - ww[j]["start"]) for i, j in m.items()]
    # sentence boundaries in whisper index space: each whisper word goes to the sentence of the last matched VTT word at or before it
    w2s = {}
    for si, s in enumerate(sents):
        for i in s:
            if i in m: w2s[m[i]] = si
    sid, sents_w = 0, [[] for _ in sents]
    for j in range(len(ww)):
        if j in w2s: sid = w2s[j]
        sents_w[sid].append(j)
    # sentence-final whisper words that belong to the next sentence's first matched word: fine as is
    # text from the VTT (keeps punctuation and quotes), timings from whisper; unmatched whisper words keep whisper text
    inv = {j: i for i, j in m.items()}
    out = [dict(text=(vw[inv[j]]["text"] if j in inv else w["text"]), start=w["start"], end=w["end"]) for j, w in enumerate(ww)]
    acc = dict(matched=len(m), vtt_words=len(vw), whisper_words=len(ww), onset_err_med=round(st.median(errs), 3),
               onset_err_p90=round(sorted(errs)[int(0.9 * len(errs))], 3), share_within_100ms=round(sum(e <= 0.1 for e in errs) / len(errs), 3),
               trailing_words_missing_from_vtt=len(ww) - 1 - max(m.values()))
    return out, [s for s in sents_w if s], "faster-whisper medium.en word timestamps (Mac), sentence breaks from the en-orig vtt", acc

def numbers(text):
    toks = re.findall(r"[\$]?\d[\d,.:]*%?|[A-Za-z]+", text)
    return [t for t in toks if re.match(r"[\$]?\d", t) or t.lower() in NUMW]

res = {}
for vid in order:
    ws, sents, src, acc = words_for(vid)
    D = dur[vid]; ann = A[vid]
    timed = "end" in ws[0] and ws[0]["end"] is not None
    S = []
    for k, idx in enumerate(sents):
        st_ = ws[idx[0]]["start"]
        en = ws[idx[-1]]["end"] if timed else (ws[sents[k + 1][0]]["start"] if k + 1 < len(sents) else ws[idx[-1]]["start"] + 0.35)
        txt = " ".join(ws[i]["text"] for i in idx)
        S.append(dict(i=k + 1, start=round(st_, 2), end=round(en, 2), words=len(idx), text=txt))
    nW = sum(s["words"] for s in S)
    span0, span1 = S[0]["start"], S[-1]["end"]
    # pauses
    pauses = []
    kind = lambda t: "sentence_end" if re.search(r'[.!?]["\']?$', t) else ("comma" if re.search(r'[,;:]["\']?$', t) else "mid_phrase")
    if timed:
        for a_, b_ in zip(ws, ws[1:]):
            g = b_["start"] - a_["end"]
            if g >= 0.15: pauses.append(dict(at=round(a_["end"], 2), pct=round(100 * a_["end"] / D, 1), len=round(g, 2), after=a_["text"], where=kind(a_["text"])))
    else:  # estimated from vtt onsets: interval minus predicted word duration (fit on the 8 whisper refs, per-video counts within ~25 %)
        c0, c1 = PM["coef"]
        for a_, b_ in zip(ws, ws[1:]):
            g = b_["start"] - a_["start"] - (c0 + c1 * len(norm(a_["text"])))
            if g >= 0.2: pauses.append(dict(at=round(a_["start"], 2), pct=round(100 * a_["start"] / D, 1), len_est=round(g, 2), after=a_["text"], where=kind(a_["text"])))
    beats_lab = {}
    def lab(i):
        for key in ("H", "S", "Y", "M"):
            if i in (ann.get(key) or []): return key
        for n, e in enumerate(ann["E"]):
            if i in e: return f"E{n+1}"
        if i == ann.get("L"): return "L"
        return "?"
    for s in S:
        s["beat"] = lab(s["i"])
        if s["i"] == ann["P"]: s["pivot"] = True
        if s["i"] == ann["L"]: s["last_line"] = True
        if s["i"] in ann["J"]: s["joke"] = True
        if s["i"] in ann["R"]: s["reversal"] = True
        if s["i"] in DIALOGUE[vid]: s["dialogue"] = True
        s["wps"] = round(s["words"] / max(0.3, s["end"] - s["start"]), 2) if timed else None
        s["numbers"] = numbers(s["text"])
    def beat_span(idxs):
        idxs = [i for i in idxs if 1 <= i <= len(S)]
        if not idxs: return None
        a_, b_ = S[min(idxs) - 1], S[max(idxs) - 1]
        n = sum(S[i - 1]["words"] for i in idxs)
        end = b_["end"]
        return dict(sentences=sorted(idxs), start=a_["start"], end=end, dur=round(end - a_["start"], 2), words=n,
                    wps=round(n / max(0.3, end - a_["start"]), 2), pct_start=round(100 * a_["start"] / D, 1))
    beats = dict(hook=beat_span(ann["H"]), setup=beat_span(ann["S"]),
                 escalation=[beat_span(e) for e in ann["E"]],
                 pivot=(dict(sentence=ann["P"], kind=ann["pivot_kind"], start=S[ann["P"] - 1]["start"], pct=round(100 * S[ann["P"] - 1]["start"] / D, 1),
                             text=S[ann["P"] - 1]["text"]) if ann["P"] else dict(kind="none")),
                 mechanism=beat_span(ann["M"]), payoff=beat_span(ann.get("Y", [])),
                 last_line=dict(sentence=ann["L"], text=S[ann["L"] - 1]["text"], words=S[ann["L"] - 1]["words"], end=S[ann["L"] - 1]["end"],
                                tail_after_s=round(D - S[ann["L"] - 1]["end"], 2)))
    ys = [dict(t=ws[i]["start"], pct=round(100 * ws[i]["start"] / D, 1)) for i in range(len(ws) - 1)
          if norm(ws[i]["text"]) == "you" and norm(ws[i + 1]["text"]).startswith("see")]
    lens = [s["words"] for s in S]
    allnum = [n for s in S for n in s["numbers"]]
    you = sum(1 for w in ws if norm(w["text"]) in ("you", "your", "you're", "yourself", "you'd", "you'll", "you've"))
    quotes = sum(1 for s in S if '"' in s["text"] or "“" in s["text"])
    res[vid] = dict(
        title=meta[vid]["title"], views=meta[vid]["views"], tier=tier[vid], rank=order.index(vid) + 1, duration_s=D,
        timing_source=src, timing_check_vs_vtt=acc,
        n_words=nW, n_sentences=len(S), speech_start=span0, speech_end=round(span1, 2),
        wps=round(nW / (span1 - span0), 2),
        sentence_words=dict(list=lens, median=st.median(lens), mean=round(st.mean(lens), 1), max=max(lens), min=min(lens),
                            share_le6=round(sum(l <= 6 for l in lens) / len(lens), 2), share_ge20=round(sum(l >= 20 for l in lens) / len(lens), 2)),
        pauses_ge150ms=(dict(method="whisper word gaps", n=len(pauses), per_10s=round(10 * len(pauses) / (span1 - span0), 2), total_s=round(sum(p["len"] for p in pauses), 2),
                             n_ge_400ms=sum(p["len"] >= 0.4 for p in pauses), n_ge_800ms=sum(p["len"] >= 0.8 for p in pauses),
                             where={k: sum(p["where"] == k for p in pauses) for k in ("sentence_end", "comma", "mid_phrase")}, list=pauses) if timed else
                        dict(method="ESTIMATED from vtt onsets (count within ~25 %, single pauses ~60 % precise)", n=len(pauses), per_10s=round(10 * len(pauses) / (span1 - span0), 2),
                             where={k: sum(p["where"] == k for p in pauses) for k in ("sentence_end", "comma", "mid_phrase")}, list=pauses)),
        you_see=ys, beats=beats,
        n_escalation_steps=len(ann["E"]), n_jokes=len(ann["J"]), n_reversals=len(ann["R"]), n_facts=ann["facts"],
        numbers=dict(tokens=allnum, n=len(allnum), distinct=len(set(n.lower() for n in allnum))),
        you_per_100w=round(100 * you / nW, 1), dialogue_sentences=len(DIALOGUE[vid]),
        names_on_screen=dict(literal=ann["lit"], of=len(S), share=round(ann["lit"] / len(S), 2)),
        hook_form=ann["form"], hook_on_screen=ann["hook_screen"],
        sentences=S, words=[[w["text"], w["start"], w.get("end")] for w in ws])
hdr = dict(
  built="2026-11-02", what="RicksClips3000, the 24 story-style Shorts (2026-10-07..11-01): words with timings, sentences, hand-coded beats, tiers by views (top/mid/bottom 8). Text and timings only, no media.",
  timing_sources={"whisper": "8 refs with audio (the 720p webm on the Spark, ~/studio/refs/ig/ricks720_*.webm): faster-whisper medium.en int8 word timestamps on the Mac, text and sentence breaks from the YouTube en-orig vtt",
                  "vtt": "16 refs (the lanes/ricks webm copies are video-only): YouTube en-orig vtt word onsets; end=null"},
  vtt_accuracy="vtt onsets vs whisper on the 8 audio refs: median |error| 0.04-0.10 s, p90 0.12-0.20 s, 51-80 % within 100 ms; the vtt drops 0-2 trailing words (whisper restores them)",
  pauses="gaps >= 150 ms between whisper word end and next start (8 refs, exact to whisper's ~50 ms). For the 16 vtt refs: ESTIMATED as onset interval minus predicted word duration (0.024 + 0.053 s/char, fit on the 8), threshold 0.2 s: per-video counts within ~25 %, single pauses ~60 % precise",
  beats="H hook, S setup, E1..En escalation steps, P pivot (the turn into the reason; kind you_see/other_phrase/shown/none), M mechanism, Y payoff, L last line; coded by hand from the transcripts and per-sentence midpoint frames (240p)",
  names_on_screen="share of sentences whose named concrete noun or action is visible in the frame at the sentence midpoint (240p sheets, coded by eye)",
  words="[text, start, end] per spoken word ([music] tags dropped)",
  facts="distinct real-world claims (history or mechanism), hand count; numbers = number tokens (digits and number words) in the text")
txt = json.dumps(dict(header=hdr, videos=res), indent=1)
txt = re.sub(r'\[\n\s+("(?:[^"\\\\]|\\\\.)*"),\n\s+([-\d.]+|null),\n\s+([-\d.]+|null)\n\s+\]', r"[\1, \2, \3]", txt)
txt = re.sub(r"\[\n\s+(\d+(?:,\n\s+\d+)*)\n\s+\]", lambda m: "[" + re.sub(r",\n\s+", ", ", m.group(1)) + "]", txt)
open(OUT, "w").write(txt)
print("ok", len(res))
