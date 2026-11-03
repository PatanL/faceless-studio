"""Story-lane script judge: scores a narration against research/library/STORY_SCRIPT_SPEC.md.

usage:
  python3 -m pipeline.qa.script_judge <slug | path/to/script.md> [--timings PATH] [--beats SPEC] [--rubric PATH]
                                      [--out report.md] [--json report.json]
  python3 -m pipeline.qa.script_judge --ref VS1Z_Q-Klt8          # judge one RicksClips reference (calibration)
  python3 -m pipeline.qa.script_judge --calibrate                # all 24 references, scores by tier

Input: the ```narration block of episodes/<slug>/script.md (or any .md with that block; [sfx: ...] tags dropped,
parsed exactly as TTS reads it). Timings, when available, make the pace, pause and position checks exact:
  --timings PATH   {"words": [{"text","start","end"}]} (captions.json from Kokoro, or a faster-whisper dump).
                   Default for a slug: episodes/<slug>/audio/captions.json when it covers >= 80 % of the words.
Without timings every time is estimated from word position at the references' pace (3.67 words/s incl. pauses).

Beats are found by phrase heuristics (calibrated on the 24 references, see --calibrate). Override when wrong:
  --beats "H=1-2;E=4-5,6,7-8;P=9;M=9-11;L=13"   sentence numbers (1-based) as printed in the report; E steps
                   comma-separated; M = the mechanism span (default: pivot to the sentence before the last line).

--rubric PATH merges judgment items a reviewer answers with pipeline/qa/SCRIPT_JUDGE_PROMPT.md (facts, jokes,
reversal, ridicule, visible mechanism, shootable lines, hook act on screen). Without it those items are left out
and the score is out of the checkable points only (reported as such).

Deterministic, stdlib only, no network. Exit 0 always (it is a report, not a gate).
"""
from __future__ import annotations

import argparse
import difflib
import json
import pathlib
import re
import statistics as st
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
REFS = REPO / "research" / "references" / "data" / "ricks24_beats.json"
SPEC_DOC = "research/library/STORY_SCRIPT_SPEC.md"

# --------------------------------------------------------------------------- the spec (numbers from ricks24_beats.json)
# Each rule: (lo, hi) is full marks, (lo2, hi2) is where the score reaches 0 (linear in between).
REF_WPS = 3.67  # top-8 median words/s over the speech span, pauses included
SPEC = {
    "runtime_s":        dict(rng=(55, 65.5), zero=(45, 75), w=5, why="top 8: 39-65 s, median 62; the two shortest refs (31, 35 s) are the two lowest"),
    "words":            dict(rng=(200, 245), zero=(150, 290), w=3, why="top 8: 145-247 words, median 219"),
    "wps":              dict(rng=(3.4, 3.9), zero=(3.0, 4.3), w=5, why="all 24: 3.36-4.09 words/s, top median 3.67"),
    "pauses_per_10s":   dict(rng=(2.3, 5.5), zero=(1.0, 8.0), w=2, why="gaps >= 150 ms: 2.3-5.5 per 10 s in all 24 (median ~3.7), mean gap ~0.22 s"),
    "pauses_ge400":     dict(rng=(0, 1), zero=(0, 5), w=3, why="8 audio refs: 0-1 gaps >= 0.4 s, none >= 0.8 s"),
    "mech_slower":      dict(rng=(-1.0, 0.1), zero=(-1.0, 0.6), w=2, why="top 8 slow down after the pivot (mechanism 3.58, last line 3.51 vs 3.67 overall); the rest speed up (3.84 / 4.17)"),
    "hook_words":       dict(rng=(8, 21), zero=(4, 30), w=4, why="hook (sentence 1, or 1-2 when 2 completes the paradox): top 9-21 words, median 14"),
    "hook_s":           dict(rng=(2.5, 5.5), zero=(1.5, 8.0), w=4, why="hook spoken in 3.0-5.4 s (top 8)"),
    "hook_form":        dict(w=5, why="23/24 open on a declarative concrete line at 0.0 s; the one question hook is #23; no date/place opener in any"),
    "setup_end_pct":    dict(rng=(12, 36), zero=(5, 55), w=6, why="first escalation starts at 17-34 % in the top 8 (median 30), 38 % in the rest"),
    "esc_steps":        dict(rng=(3, 6), zero=(1, 9), w=8, why="escalation steps: top median 4 (2-6), >= 4 in 6/8 top vs 4/16 rest"),
    "pivot_pct":        dict(rng=(55, 82), zero=(35, 95), w=8, why="the turn into the reason: top 55-81 % of runtime, median 66; 7/8 top have one"),
    "you_see":          dict(w=3, why="'You see' is either the backstory bridge (<= 12 %, 4/8 top) or the pivot (60-81 %); never in between, at most 2"),
    "mech_words":       dict(rng=(28, 55), zero=(12, 90), w=5, why="mechanism: top 32-49 words, 9-15 s, 15-32 % of the words"),
    "last_line":        dict(w=5, why="last line 11-24 words (top median 16.5), not a question (0/8 top), the video ends <= 0.5 s after it"),
    "numbers":          dict(rng=(1, 5), zero=(0, 10), w=4, why="number tokens: top 1-5 (median 3), rest median 5.5 (up to 15)"),
    "dialogue":         dict(rng=(1, 5), zero=(0, 8), w=3, why="character lines: top median 2 (0-5), >= 2 in 5/8 top vs 5/16 rest"),
    "sentence_len":     dict(w=4, why="sentence median 10-15 words (top 12.5), longest <= 30, short punch lines (<= 6 words) in 10-35 %"),
}
RUBRIC = {  # judgment items, answered with SCRIPT_JUDGE_PROMPT.md; points if within range
    "facts":            dict(rng=(4, 7), w=6, why="distinct real-world claims: top median 5 (2-7), >= 4 in 7/8 top vs 5/16 rest"),
    "jokes":            dict(rng=(2, 6), w=4, why="jokes: top median 2 (1-4), >= 2 in 6/8 top vs 6/16 rest"),
    "reversal":         dict(rng=(1, 3), w=2, why="at least one reversal (the mockers proved wrong, the trap springs)"),
    "ridicule":         dict(rng=(1, 9), w=2, why="someone mocks the odd act (S6): Jar, Storm Oil, Railroads, Mirror"),
    "mechanism_visible":dict(rng=(1, 1), w=4, why="the cause is a physical thing the camera can watch (S3): 6/8 top"),
    "shootable_share":  dict(rng=(0.9, 1.0), w=4, why="each sentence names something on screen: top median 0.97, all >= 0.68"),
    "hook_act_on_screen": dict(rng=(1, 1), w=3, why="frame 0 shows the protagonist doing the odd act (all 24)"),
}

# --------------------------------------------------------------------------- text helpers
NUMW = set("one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen "
           "eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred thousand million billion "
           "half twice dozen".split())
PIVOT_RE = re.compile(r"^(you see\b|see,|that's because|that is because|here's (the|how|why|what)|the (secret|trick|reason|catch|truth|answer)\b|"
                      r"(it )?turns out|in real life|back then|there was a man|inside (the|it|was|that)|wait, \w+\?|well, he|"
                      r"because the|the real reason|what (nobody|no one) knew)", re.I)
ESC_RE = re.compile(r"^(then\b|and then|but then|now,? (they|he|she|the|nobody|no one)|meanwhile|eventually|deeper|until\b|soon\b|"
                    r"\w+ later|(a|one|two|three) (few )?(days?|weeks?|months?|years?|hours?|minutes?) (later|go by|pass)|"
                    r"the (next|first|second|third|following|last) (night|day|morning|week|time|race|year)|"
                    r"one (night|day|morning|monday|week|winter|summer)|by (the end|midnight|july|may|morning|the fifth|then)|"
                    r"in (may|june|july|the last|\d{3,4})|on (august|the hottest|the \w+ day)|at (first|this point|\d)|"
                    r"for (\w+ )?(years|decades|weeks|months)|every (friday|trip|night|morning)|within\b|after (the|that|\w+ weeks)|"
                    r"so,? (he|she|they|the (captain|dad|knight|king)|you|if|when) |but (by|the (first|next))|still,|instead,|except when|at night)", re.I)
YOU = {"you", "your", "you're", "yourself", "you'd", "you'll", "you've"}
norm = lambda s: re.sub(r"[^a-z0-9']", "", s.lower().replace("’", "'"))


def split_sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text.strip())
    parts = re.split(r'(?:(?<=[.!?])|(?<=[.!?]["”]))\s+(?=["“]?[A-Z0-9])', text)
    out = []
    for p in parts:  # re-attach a closing quote the split left on the next piece
        p = p.strip()
        if out and p.startswith(('"', "”")) and len(p) == 1:
            out[-1] += p
            continue
        if p:
            out.append(p)
    return out


def numbers(text: str) -> list[str]:
    toks = re.findall(r"\$?\d(?:[\d,.:]*\d)?%?|[A-Za-z-]+", text)
    out = []
    for t in toks:
        if re.match(r"\$?\d", t):
            out.append(t)
        elif any(p in NUMW for p in t.lower().split("-")):
            out.append(t)
    return out


def ramp(x, rng, zero):
    lo, hi = rng
    zl, zh = zero
    if lo <= x <= hi:
        return 1.0
    if x < lo:
        return max(0.0, (x - zl) / (lo - zl)) if lo > zl else 0.0
    return max(0.0, (zh - x) / (zh - hi)) if zh > hi else 0.0


# --------------------------------------------------------------------------- inputs
def read_narration(path: pathlib.Path) -> tuple[list[str], dict]:
    if str(REPO) not in sys.path:
        sys.path.insert(0, str(REPO))
    from pipeline.qa.util import front_matter, narration_paragraphs
    txt = path.read_text(encoding="utf-8")
    return narration_paragraphs(path), front_matter(txt)


def load_words(path) -> list[dict] | None:
    if not path or not pathlib.Path(path).is_file():
        return None
    d = json.loads(pathlib.Path(path).read_text())
    ws = d.get("words") if isinstance(d, dict) else d
    out = []
    for w in ws or []:
        if isinstance(w, (list, tuple)):
            w = dict(text=w[0], start=w[1], end=w[2])
        if w.get("text", "").strip() and w.get("text") != "[music]":
            out.append(dict(text=w["text"].strip(), start=float(w["start"]), end=(None if w.get("end") is None else float(w["end"]))))
    return out


def align(script_words: list[str], timed: list[dict]) -> tuple[list[dict | None], float]:
    a = [norm(w) for w in script_words]
    b = [norm(w["text"]) for w in timed]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    m = {}
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            m[blk.a + k] = blk.b + k
    out = [timed[m[i]] if i in m else None for i in range(len(a))]
    # fill gaps by interpolation between matched neighbours
    for i in range(len(out)):
        if out[i] is None:
            prev = next((out[j] for j in range(i - 1, -1, -1) if out[j]), None)
            nxt = next((out[j] for j in range(i + 1, len(out)) if out[j]), None)
            t = (prev["end"] or prev["start"]) if prev else (nxt["start"] if nxt else 0.0)
            out[i] = dict(text=script_words[i], start=t, end=t, interp=True)
    return out, (len(m) / max(1, len(a)))


# --------------------------------------------------------------------------- analysis
def build(sentences: list[str], timed: list[dict] | None, duration: float | None, beats_override: str | None):
    words, sid = [], []
    for k, s in enumerate(sentences):
        for w in s.split():
            words.append(w)
            sid.append(k)
    nW = len(words)
    coverage = None
    if timed:
        tw, coverage = align(words, timed)
        if coverage < 0.8:
            tw = None
    else:
        tw = None
    if tw:
        starts = [w["start"] for w in tw]
        ends = [w["end"] if w.get("end") is not None else None for w in tw]
        # vtt-only refs: end = next onset
        for i in range(nW):
            if ends[i] is None:
                ends[i] = starts[i + 1] if i + 1 < nW else starts[i] + 0.35
        span0, span1 = starts[0], ends[-1]
        dur = duration or (span1 + 0.25)
        timing = "measured"
    else:
        starts = [i / REF_WPS for i in range(nW)]
        ends = [(i + 1) / REF_WPS for i in range(nW)]
        span0, span1 = 0.0, nW / REF_WPS
        dur = duration or (span1 + 0.25)
        timing = f"estimated at {REF_WPS} words/s"
    S = []
    i = 0
    for k, s in enumerate(sentences):
        n = len(s.split())
        S.append(dict(i=k + 1, text=s, words=n, start=round(starts[i], 2), end=round(ends[i + n - 1], 2)))
        i += n
    pct = lambda t: round(100 * t / dur, 1)

    # ---- beats
    # the hook is sentence 1, plus sentence 2 when it completes the paradox ("Gambling is illegal in Japan. Yet ...")
    hook = [1]
    if len(S) > 2 and S[0]["words"] <= 12 and S[0]["words"] + S[1]["words"] <= 26 and \
            re.match(r"^(yet|but|and|after|still|except|then|so|one's|now)\b", S[1]["text"].lstrip('"“'), re.I):
        hook = [1, 2]
    ov = {}
    if beats_override:
        for part in beats_override.split(";"):
            if "=" in part:
                k, v = part.split("=", 1)
                ov[k.strip().upper()] = v.strip()

    def rng_list(spec):  # noqa: E306
        out = []
        for p in spec.split(","):
            if "-" in p:
                a, b = p.split("-")
                out.extend(range(int(a), int(b) + 1))
            elif p.strip():
                out.append(int(p))
        return out

    if "H" in ov:
        hook = rng_list(ov["H"])
    B = dict(hook=hook)
    if "P" in ov:
        piv = int(ov["P"]) if ov["P"].lower() != "none" else None
    else:
        piv = None
        cum = 0
        for s in S:
            if cum / nW >= 0.40 and s["i"] > 2 and PIVOT_RE.search(s["text"].lstrip('"“')):
                piv = s["i"]
                break
            cum += s["words"]
    last = int(ov.get("L", len(S)))
    if "E" in ov:
        esc = [rng_list(x) for x in ov["E"].split(",") if x.strip()]
    else:
        zone_end = (piv - 1) if piv else last - 1
        marks = [s["i"] for s in S if len(hook) + 1 <= s["i"] <= zone_end and ESC_RE.search(s["text"].lstrip('"“'))]
        # each marker sentence opens a step, except a short one (<= 6 words: "Then another.") which continues it
        starts_ = [m for j, m in enumerate(marks) if j == 0 or S[m - 1]["words"] > 6]
        esc = []
        for j, a in enumerate(starts_):
            b = (starts_[j + 1] - 1) if j + 1 < len(starts_) else zone_end
            esc.append(list(range(a, b + 1)))
    first_esc = esc[0][0] if esc else (piv or last)
    setup = list(range(len(hook) + 1, first_esc))
    mech = list(range(piv, last)) if piv else []
    if piv and piv == last:
        mech = [piv]
    if "M" in ov:
        mech = rng_list(ov["M"])
    B.update(setup=setup, esc=esc, pivot=piv, mech=mech, last=last)

    def span(idx):
        idx = [x for x in idx if 1 <= x <= len(S)]
        if not idx:
            return None
        a, b = S[min(idx) - 1], S[max(idx) - 1]
        n = sum(S[x - 1]["words"] for x in idx)
        return dict(sentences=f"{min(idx)}-{max(idx)}", start=a["start"], end=b["end"], dur=round(b["end"] - a["start"], 2),
                    words=n, wps=round(n / max(0.3, b["end"] - a["start"]), 2), pct_start=pct(a["start"]))

    # ---- pauses
    pauses = []
    has_ends = bool(tw) and sum(1 for w in tw if w.get("end") is not None and not w.get("interp")) > 0.8 * nW
    if has_ends:
        for a, b in zip(range(nW - 1), range(1, nW)):
            g = starts[b] - ends[a]
            if g >= 0.15 and not tw[a].get("interp") and not tw[b].get("interp"):
                pauses.append(dict(at=round(ends[a], 2), len=round(g, 2), after=words[a]))
    lens = [s["words"] for s in S]
    allnum = [x for s in S for x in numbers(s["text"])]
    dia = [s["i"] for s in S if re.search(r'["“”]', s["text"]) or re.search(r"\b(says?|said|yells?|asks?|goes|screams?|whispers?):?\s", s["text"])
           or re.search(r":\s+[A-Za-z]", s["text"])]
    ys = []
    for j in range(nW - 1):
        if norm(words[j]) == "you" and norm(words[j + 1]).startswith("see"):
            ys.append(pct(starts[j]))
    you = sum(1 for w in words if norm(w) in YOU)
    M = dict(
        timing=timing, timing_coverage=None if coverage is None else round(coverage, 3), duration_s=round(dur, 2),
        n_words=nW, n_sentences=len(S), wps=round(nW / max(1e-6, span1 - span0), 2),
        sentence_words=dict(median=st.median(lens), max=max(lens), share_le6=round(sum(l <= 6 for l in lens) / len(lens), 2),
                            share_ge20=round(sum(l >= 20 for l in lens) / len(lens), 2)),
        pauses=(dict(n=len(pauses), per_10s=round(10 * len(pauses) / max(1e-6, span1 - span0), 2), total_s=round(sum(p["len"] for p in pauses), 2),
                     n_ge_400ms=sum(p["len"] >= 0.4 for p in pauses), n_ge_800ms=sum(p["len"] >= 0.8 for p in pauses),
                     longest=sorted(pauses, key=lambda p: -p["len"])[:6]) if has_ends else None),
        hook=dict(text=" ".join(S[i - 1]["text"] for i in hook), words=sum(S[i - 1]["words"] for i in hook), sentences=len(hook),
                  dur=round((S[len(hook)]["start"] if len(S) > len(hook) else S[-1]["end"]) - S[0]["start"], 2)),
        setup=span(setup), esc=[span(e) for e in esc], pivot=(dict(i=piv, pct=pct(S[piv - 1]["start"]), text=S[piv - 1]["text"]) if piv else None),
        mechanism=span(mech), last=dict(i=last, text=S[last - 1]["text"], words=S[last - 1]["words"], tail_s=round(dur - S[last - 1]["end"], 2),
                                         wps=round(S[last - 1]["words"] / max(0.3, S[last - 1]["end"] - S[last - 1]["start"]), 2)),
        you_see_pct=ys, numbers=allnum, dialogue=dia, you_per_100w=round(100 * you / nW, 1),
        setup_end_pct=pct(S[first_esc - 1]["start"]) if first_esc <= len(S) else None,
    )
    return S, B, M


def judge(S, B, M, rubric: dict | None):
    R = []

    def add(key, val, score, note=""):
        spec = SPEC.get(key) or RUBRIC.get(key)
        R.append(dict(check=key, value=val, score=round(score, 2), points=round(score * spec["w"], 2), of=spec["w"],
                      target=(f"{spec['rng'][0]}-{spec['rng'][1]}" if "rng" in spec else ""), why=spec["why"], note=note))

    def rng(key, x, note=""):
        s = SPEC[key]
        add(key, x, ramp(x, s["rng"], s["zero"]), note)

    measured = M["timing"] == "measured"
    rng("runtime_s", M["duration_s"], "" if measured else "estimated from word count")
    rng("words", M["n_words"])
    if measured:
        rng("wps", M["wps"])
        if M["pauses"]:
            rng("pauses_per_10s", M["pauses"]["per_10s"], "timings look gapless (Kokoro captions.json words abut): measure the rendered audio "
                "with whisper and pass --timings" if M["pauses"]["per_10s"] < 1.0 else "")
            rng("pauses_ge400", M["pauses"]["n_ge_400ms"], f"{M['pauses']['n_ge_800ms']} >= 0.8 s, {M['pauses']['total_s']} s total")
        if M["mechanism"]:
            d = round(((M["mechanism"]["wps"] + M["last"]["wps"]) / 2) - M["wps"], 2)
            rng("mech_slower", d, f"mechanism {M['mechanism']['wps']} w/s, last line {M['last']['wps']} w/s vs {M['wps']} overall")
    rng("hook_words", M["hook"]["words"])
    rng("hook_s", M["hook"]["dur"], "" if measured else "estimated")
    h = S[0]["text"]
    bad = []
    if h.rstrip('"”').endswith("?"):
        bad.append("question")
    if re.match(r"^(in \d|it's \d|it was \d|once|long ago|in the year|this is|meet |have you|did you know|imagine|in this video)", h, re.I):
        bad.append("opens on setup/date/intro, not the act")
    if not re.match(r"^(he|she|they|a |an |the |his |her |their |if you|there's|thirty|\w+ (sailors|men|people|soldiers))|^[A-Z][a-z]+ ", h):
        bad.append("no concrete subject up front")
    add("hook_form", "; ".join(bad) or "declarative, concrete subject", 1.0 if not bad else (0.4 if len(bad) == 1 else 0.0))
    if M["setup_end_pct"] is not None:
        rng("setup_end_pct", M["setup_end_pct"], f"first escalation at sentence {B['esc'][0][0] if B['esc'] else '-'}")
    rng("esc_steps", len(B["esc"]), "auto-detected (about +-1); override with --beats E=..." if True else "")
    if M["pivot"]:
        rng("pivot_pct", M["pivot"]["pct"], f"sentence {M['pivot']['i']}: {M['pivot']['text'][:60]}")
    else:
        add("pivot_pct", None, 0.0, "no turn into the reason found after 40 % (override with --beats P=n)")
    ys = M["you_see_pct"]
    ok = len(ys) <= 2 and all(p <= 12 or 55 <= p <= 85 for p in ys)
    add("you_see", ys, 1.0 if ok else (0.5 if len(ys) <= 2 else 0.0),
        "" if ok else "a 'You see' between 12 % and 55 % reads as a mid-story explainer")
    if M["mechanism"]:
        rng("mech_words", M["mechanism"]["words"], f"{M['mechanism']['dur']} s, {round(M['mechanism']['words'] / M['n_words'], 2)} of the words")
    else:
        add("mech_words", 0, 0.0, "no mechanism span (no pivot)")
    L = M["last"]
    pen = []
    if not (11 <= L["words"] <= 24):
        pen.append(f"{L['words']} words (11-24)")
    if L["text"].rstrip('"”').endswith("?"):
        pen.append("ends on a question")
    if measured and L["tail_s"] > 0.6:
        pen.append(f"{L['tail_s']} s of video after the last word")
    add("last_line", L["text"], max(0.0, 1 - 0.4 * len(pen)), "; ".join(pen))
    rng("numbers", len(M["numbers"]), ", ".join(M["numbers"]))
    rng("dialogue", len(M["dialogue"]), f"sentences {M['dialogue']}")
    sw = M["sentence_words"]
    sc = 1.0
    notes = []
    if not 9 <= sw["median"] <= 15:
        sc -= 0.4
        notes.append(f"median {sw['median']}")
    if sw["max"] > 30:
        sc -= 0.3
        notes.append(f"longest {sw['max']}")
    if not 0.10 <= sw["share_le6"] <= 0.35:
        sc -= 0.3
        notes.append(f"short lines {sw['share_le6']}")
    add("sentence_len", sw, max(0.0, sc), "; ".join(notes))
    if rubric:
        for k, spec in RUBRIC.items():
            if k in rubric and rubric[k] is not None:
                v = rubric[k]
                x = float(v["value"] if isinstance(v, dict) else v)
                lo, hi = spec["rng"]
                s = 1.0 if lo <= x <= hi else (max(0.0, x / lo) if x < lo else max(0.0, 1 - (x - hi) / max(1, hi)))
                add(k, x, s, (v.get("note", "") if isinstance(v, dict) else ""))
    got = sum(r["points"] for r in R)
    of = sum(r["of"] for r in R)
    return R, round(100 * got / of, 1), of


# --------------------------------------------------------------------------- report
def render(name, S, B, M, R, score, of, meta=None) -> str:
    out = [f"# Script judge: {name}", "",
           f"Spec: `{SPEC_DOC}`. Timing: {M['timing']}" + (f" (word coverage {M['timing_coverage']})" if M["timing_coverage"] else "") + ".",
           f"**Score: {score} / 100** (out of {of} checkable points; rubric items " + ("included" if any(r["check"] in RUBRIC for r in R) else "not answered") + ").", "",
           "## Outside the spec (biggest point losses first)", ""]
    lost = sorted([r for r in R if r["score"] < 1], key=lambda r: -(r["of"] - r["points"]))
    if not lost:
        out.append("- nothing")
    for r in lost:
        out.append(f"- **{r['check']}** = {json.dumps(r['value']) if not isinstance(r['value'], str) else r['value']}"
                   f" (target {r['target'] or 'see why'}; -{round(r['of'] - r['points'], 1)} pts). {r['note']}  \n  _{r['why']}_")
    out += ["", "## All checks", "", "| check | value | target | points |", "|---|---|---|---|"]
    for r in R:
        v = r["value"] if isinstance(r["value"], (int, float, str)) or r["value"] is None else json.dumps(r["value"])
        v = str(v).replace("|", "/")
        out.append(f"| {r['check']} | {v[:80]} | {r['target']} | {r['points']}/{r['of']} |")
    out += ["", "## Beat map (as detected; override with --beats)", "",
            "| # | beat | start s | words | sentence |", "|---|---|---|---|---|"]
    lab = {i: "HOOK" for i in B["hook"]}
    for x in B["setup"]:
        lab[x] = "setup"
    for n, e in enumerate(B["esc"]):
        for x in e:
            lab[x] = f"E{n + 1}"
    for x in B["mech"]:
        lab[x] = "mechanism"
    if B["pivot"]:
        lab[B["pivot"]] = "PIVOT"
    lab[B["last"]] = "LAST"
    for s in S:
        out.append(f"| {s['i']} | {lab.get(s['i'], '')} | {s['start']} | {s['words']} | {s['text'].replace('|', '/')} |")
    p = M["pauses"]
    out += ["", "## Pace", "",
            f"- {M['n_words']} words, {M['n_sentences']} sentences, {M['duration_s']} s, {M['wps']} words/s; sentence median "
            f"{M['sentence_words']['median']} words, longest {M['sentence_words']['max']}.",
            f"- 'You see' at {M['you_see_pct']} % of runtime; numbers {M['numbers']}; 'you' {M['you_per_100w']} per 100 words."]
    if p:
        out.append(f"- Pauses >= 150 ms: {p['n']} ({p['per_10s']} per 10 s, {p['total_s']} s total); >= 0.4 s: {p['n_ge_400ms']}; >= 0.8 s: {p['n_ge_800ms']}. "
                   "Longest: " + ", ".join(f"{q['len']} s after '{q['after']}' at {q['at']} s" for q in p["longest"]))
    for k in ("setup", "mechanism"):
        if M[k]:
            out.append(f"- {k}: sentences {M[k]['sentences']}, {M[k]['dur']} s, {M[k]['words']} words, {M[k]['wps']} w/s, starts at {M[k]['pct_start']} %.")
    for n, e in enumerate(M["esc"]):
        out.append(f"- E{n + 1}: sentences {e['sentences']}, {e['dur']} s, {e['words']} words, {e['wps']} w/s, starts at {e['pct_start']} %.")
    return "\n".join(out) + "\n"


def run_one(name, sentences, timed, duration, beats, rubric):
    S, B, M = build(sentences, timed, duration, beats)
    R, score, of = judge(S, B, M, rubric)
    return dict(name=name, score=score, of=of, checks=R, metrics=M, beats=B, sentences=S)


def ref_input(vid: str):
    d = json.loads(REFS.read_text())["videos"][vid]
    sents = [s["text"] for s in d["sentences"]]
    timed = [dict(text=w[0], start=w[1], end=w[2]) for w in d["words"]]
    return d, sents, timed


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", nargs="?")
    ap.add_argument("--timings")
    ap.add_argument("--duration", type=float, help="video length in s (default: last word end + 0.25)")
    ap.add_argument("--wps", type=float, help="words/s for estimated timings when there is no audio (default 3.67)")
    ap.add_argument("--beats")
    ap.add_argument("--rubric")
    ap.add_argument("--out")
    ap.add_argument("--json")
    ap.add_argument("--ref")
    ap.add_argument("--calibrate", action="store_true")
    a = ap.parse_args(argv)
    if a.wps:
        globals()["REF_WPS"] = a.wps
    rubric = json.loads(pathlib.Path(a.rubric).read_text()) if a.rubric else None
    if a.calibrate:
        refs = json.loads(REFS.read_text())["videos"]
        rows = []
        for vid, d in refs.items():
            _, sents, timed = ref_input(vid)
            r = run_one(vid, sents, timed, d["duration_s"], None, None)
            coded = dict(facts=d["n_facts"], jokes=d["n_jokes"], reversal=d["n_reversals"], shootable_share=d["names_on_screen"]["share"])
            r2 = run_one(vid, sents, timed, d["duration_s"], None, coded)
            man_p = d["beats"]["pivot"].get("sentence")
            rows.append(dict(id=vid, tier=d["tier"], title=d["title"], score=r["score"], score_coded=r2["score"], esc_auto=len(r["beats"]["esc"]),
                             esc_manual=d["n_escalation_steps"], pivot_auto=r["beats"]["pivot"], pivot_manual=man_p))
        print("deterministic score | with the 4 hand-coded rubric items (facts, jokes, reversal, shootable share)")
        for t in ("top", "mid", "bottom"):
            xs = [r["score"] for r in rows if r["tier"] == t]
            ys = [r["score_coded"] for r in rows if r["tier"] == t]
            print(f"{t:6s} median {st.median(xs):5.1f}  min {min(xs):5.1f}  max {max(xs):5.1f}   |  median {st.median(ys):5.1f}  min {min(ys):5.1f}  max {max(ys):5.1f}")
        mae = st.mean(abs(r["esc_auto"] - r["esc_manual"]) for r in rows)
        pv = sum(1 for r in rows if r["pivot_auto"] == r["pivot_manual"])
        print(f"escalation steps auto vs hand: mean |error| {mae:.2f}; pivot sentence auto == hand in {pv}/24")
        for r in rows:
            print(f"  {r['tier']:6s} {r['score']:5.1f} {r['score_coded']:5.1f}  esc {r['esc_auto']}/{r['esc_manual']}  pivot {r['pivot_auto']}/{r['pivot_manual']}  {r['title']}")
        if a.json:
            pathlib.Path(a.json).write_text(json.dumps(rows, indent=1))
        return 0
    if a.ref:
        d, sents, timed = ref_input(a.ref)
        name, duration = f"{a.ref} ({d['title']}, reference)", d["duration_s"]
    else:
        t = pathlib.Path(a.target)
        if not t.suffix:
            slug = a.target
            t = REPO / "episodes" / slug / "script.md"
            if not a.timings and (REPO / "episodes" / slug / "audio" / "captions.json").is_file():
                a.timings = str(REPO / "episodes" / slug / "audio" / "captions.json")
        paras, fm = read_narration(t)
        sents = [s for p in paras for s in split_sentences(p)]
        timed = load_words(a.timings)
        name, duration = f"{t.relative_to(REPO) if t.is_absolute() and REPO in t.parents else t}", a.duration
    r = run_one(name, sents, timed, duration, a.beats, rubric)
    md = render(name, r["sentences"], r["beats"], r["metrics"], r["checks"], r["score"], r["of"])
    if a.out:
        pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        pathlib.Path(a.out).write_text(md)
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(r, indent=1, default=str))
    print(md if not a.out else f"{name}: {r['score']} / 100 -> {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
