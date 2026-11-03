"""Word-by-word delivery match of a render against a reference read of the same words (voice_cadence.py output).

Measures prosody only: where stress falls, the pitch jump and lengthening on each word, pace and pauses. The
reference is a measurement target, never a voice prompt.

usage: python voice_compare.py ref.json cand.json [cand2.json ...] [--ref-words N] > table.json
  --ref-words N   use only the first N words of the reference (e.g. the Jar's first three lines = 46 words)

Scores, per candidate:
  stress_r        Pearson r of the per-word composite stress score (z of pitch, loudness, length), ref vs cand
  pitch_r         Pearson r of the per-word pitch peak (st re the speaker's median): the shape of the melody
  len_r           Pearson r of the per-word per-syllable length ratio
  stress_f1       overlap of the stressed-word sets (ref top-z words vs cand top-z words, same count)
  jump_ratio      mean pitch jump (local prominence, st) on the ref's stressed words, cand / ref
  len_ratio       mean lengthening on the ref's stressed words, cand / ref
  pace_ratio      words per second, cand / ref
  pause_*         pauses >= 80 ms: count and total seconds, cand and ref
  range_ratio     f0 p5-p95 range (st), cand / ref;  spread_ratio: 1 s-median pitch movement, cand / ref
  match           0-100: 20 stress_r + 15 pitch_r + 5 len_r + 15 stress_f1 + 15 jump + 10 range/spread + 10 pace
                  + 10 pauses (placement and size of the stress both count; register is reported, not scored)
"""
import difflib
import json
import re
import sys

import numpy as np


def _n(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def pair(ref, cand):
    a, b = [_n(w["text"]) for w in ref], [_n(w["text"]) for w in cand]
    out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
        if tag == "equal":
            out += [(ref[i1 + k], cand[j1 + k]) for k in range(i2 - i1)]
    return out


def r(x, y):
    m = [(p, q) for p, q in zip(x, y) if p is not None and q is not None]
    if len(m) < 4:
        return None
    p, q = np.array(m, float).T
    if p.std() == 0 or q.std() == 0:
        return 0.0
    return round(float(np.corrcoef(p, q)[0, 1]), 3)


def pauses(words):
    g = [b["start"] - a["end"] for a, b in zip(words, words[1:])]
    g = [x for x in g if x >= 0.08]
    return len(g), round(float(sum(g)), 2)


def compare(ref, cand, rs_sum=None, cs_sum=None):
    P = pair(ref, cand)
    rw, cw = [p[0] for p in P], [p[1] for p in P]
    k = max(1, sum(w["stressed"] for w in rw))
    rs = {id(w) for w in sorted(rw, key=lambda w: -w["stress_z"])[:k]}
    cs_idx = {i for i, _ in sorted(enumerate(cw), key=lambda t: -t[1]["stress_z"])[:k]}
    rs_idx = {i for i, w in enumerate(rw) if id(w) in rs}
    f1 = round(len(rs_idx & cs_idx) / k, 3)

    def mean(v):
        v = [x for x in v if x is not None]
        return float(np.mean(v)) if v else None

    jr, jc = mean([w["pitch_prom_st"] for w in rw if id(w) in rs]), mean([cw[i]["pitch_prom_st"] for i in rs_idx])
    lr, lc = mean([w["len_ratio"] for w in rw if id(w) in rs]), mean([cw[i]["len_ratio"] for i in rs_idx])
    span = lambda ws: ws[-1]["end"] - ws[0]["start"]
    pr, pc = len(rw) / span(rw), len(cw) / span(cw)
    np_r, tp_r = pauses(rw)
    np_c, tp_c = pauses(cw)
    out = {
        "words_paired": len(P), "stress_r": r([w["stress_z"] for w in rw], [w["stress_z"] for w in cw]),
        "pitch_r": r([w["pitch_re_med_st"] for w in rw], [w["pitch_re_med_st"] for w in cw]),
        "len_r": r([w["len_ratio"] for w in rw], [w["len_ratio"] for w in cw]),
        "stress_f1": f1,
        "jump_ref_st": None if jr is None else round(jr, 2), "jump_cand_st": None if jc is None else round(jc, 2),
        "jump_ratio": None if not jr or jc is None else round(jc / jr, 3),
        "len_ref": None if lr is None else round(lr, 2), "len_cand": None if lc is None else round(lc, 2),
        "len_ratio": None if not lr or lc is None else round(lc / lr, 3),
        "pace_ref_wps": round(pr, 2), "pace_cand_wps": round(pc, 2), "pace_ratio": round(pc / pr, 3),
        "pauses_ref": [np_r, tp_r], "pauses_cand": [np_c, tp_c],
        "ref_stressed": [w["text"] for w in rw if id(w) in rs],
        "cand_stressed": [cw[i]["text"] for i in sorted(cs_idx)],
    }
    clip = lambda x: max(0.0, min(1.0, x))
    jump = clip(1 - abs(1 - (out["jump_ratio"] or 0)))
    pace = clip(1 - abs(1 - out["pace_ratio"]) * 3)
    pz = clip(1 - abs(tp_c - tp_r) / max(0.3, tp_r + 0.3))
    rng = 0.5
    if rs_sum and cs_sum:
        out["f0_median_hz"] = [rs_sum["f0_median_hz"], cs_sum["f0_median_hz"]]
        out["range_ratio"] = round(cs_sum["f0_range_p5_p95_st"] / rs_sum["f0_range_p5_p95_st"], 3)
        out["spread_ratio"] = round(cs_sum["f0_1s_median_spread_st_p10_p90"] / rs_sum["f0_1s_median_spread_st_p10_p90"], 3)
        rng = 0.5 * clip(1 - abs(1 - out["range_ratio"])) + 0.5 * clip(1 - abs(1 - out["spread_ratio"]))
    out["match"] = round(20 * clip(out["stress_r"] or 0) + 15 * clip(out["pitch_r"] or 0) + 5 * clip(out["len_r"] or 0)
                         + 15 * f1 + 15 * jump + 10 * rng + 10 * pace + 10 * pz, 1)
    return out


def main(argv):
    n = None
    if "--ref-words" in argv:
        n = int(argv[argv.index("--ref-words") + 1])
        del argv[argv.index("--ref-words"): argv.index("--ref-words") + 2]
    rd = json.load(open(argv[0]))
    ref = rd["words"][:n] if n else rd["words"]
    res = {}
    for p in argv[1:]:
        d = json.load(open(p))
        res[d["summary"]["label"]] = compare(ref, d["words"], None if n else rd["summary"], d["summary"])
    json.dump(res, sys.stdout, indent=1)


if __name__ == "__main__":
    main(sys.argv[1:])
