"""Aggregate voice_cadence.py measurements of a reference group into the numbers VOICE_CADENCE.md cites.
Numbers only: no transcripts or lines are written (reference words stay in ~/faceless-work).

usage: python voice_cadence_summary.py out.json group=dir_of_jsons [group2=dir2 ...]
"""
import glob
import json
import re
import sys

import numpy as np


def q(v, d=2):
    v = [x for x in v if x is not None]
    if not v:
        return None
    return {"median": round(float(np.median(v)), d), "p25": round(float(np.percentile(v, 25)), d),
            "p75": round(float(np.percentile(v, 75)), d), "n": len(v)}


def group(files):
    R = {k: [] for k in ("f0_median_hz", "f0_range_p5_p95_st", "f0_1s_median_spread_st_p10_p90", "phrase_range_st",
                         "words_per_s", "articulation_syl_per_s", "stressed_share", "stress_pitch_vs_unstressed_st",
                         "stress_pitch_prominence_st", "stress_loud_vs_unstressed_db", "stress_len_vs_unstressed",
                         "sentence_start_st", "sentence_end_st", "sentence_peak_pos", "gaps_ge_120ms_per_min",
                         "gaps_ge_80ms_per_min", "hook_sentence_s")}
    cls, rate_len, pauses = {}, {"1-6": [], "6-10": [], "10-16": [], "16+": []}, {"sentence": [], "comma": [], "inside": []}
    hook = {"act_verb_is_pitch_peak": 0, "hooks": 0, "act_verb_pitch_st": [], "hook_end_len": [], "hook_end_stressed": 0}
    for f in files:
        d = json.load(open(f))
        s, W = d["summary"], d["words"]
        for k in ("f0_median_hz", "f0_range_p5_p95_st", "f0_1s_median_spread_st_p10_p90", "words_per_s",
                  "stressed_share", "gaps_ge_120ms_per_min", "gaps_ge_80ms_per_min"):
            R[k].append(s[k])
        R["phrase_range_st"].append(s["phrase_range_st_median"])
        c = s["stress_contrast"]
        R["stress_pitch_vs_unstressed_st"].append(c["pitch_peak_st"])
        R["stress_pitch_prominence_st"].append(c["pitch_prom_st"])
        R["stress_loud_vs_unstressed_db"].append(c["loud_db"])
        R["stress_len_vs_unstressed"].append(c["len_ratio"])
        gaps = [max(0.0, b["start"] - a["end"]) for a, b in zip(W, W[1:])]
        R["articulation_syl_per_s"].append(sum(w["syl"] for w in W) / (W[-1]["end"] - W[0]["start"] - sum(g for g in gaps if g >= 0.03)))
        se = s["sentences"]
        med = np.median([x["syl_ps"] for x in se if x["syl_ps"]])
        i = 0
        for k, x in enumerate(se):
            ws = W[i:i + x["n"]]
            i += x["n"]
            R["sentence_start_st"].append(x["start_st"])
            R["sentence_end_st"].append(x["end_st"])
            R["sentence_peak_pos"].append(x["peak_pos"])
            if x["syl_ps"] and x["n"] >= 2:
                key = "1-6" if x["n"] < 6 else "6-10" if x["n"] < 10 else "10-16" if x["n"] < 16 else "16+"
                rate_len[key].append(x["syl_ps"] / med)
            if k == 0:
                R["hook_sentence_s"].append(ws[-1]["end"] - ws[0]["start"])
                hook["hooks"] += 1
                verbs = [w for w in ws if w["cls"] == "verb"]
                pk = max(ws, key=lambda w: w["pitch_re_med_st"] if w["pitch_re_med_st"] is not None else -99)
                if verbs and verbs[0] is pk:
                    hook["act_verb_is_pitch_peak"] += 1
                if verbs and verbs[0]["pitch_re_med_st"] is not None:
                    hook["act_verb_pitch_st"].append(verbs[0]["pitch_re_med_st"])
                hook["hook_end_len"].append(ws[-1]["len_ratio"])
                hook["hook_end_stressed"] += int(ws[-1]["stressed"])
        for a, b in zip(W, W[1:]):
            g = max(0.0, b["start"] - a["end"])
            k = "sentence" if re.search(r"[.!?][\"”’]*$", a["text"]) else "comma" if re.search(r"[,;:—–-]$", a["text"]) else "inside"
            pauses[k].append(g)
        for k, v in s["by_class"].items():
            cls.setdefault(k, {"n": 0, "stressed_rate": [], "pitch_re_med_st": [], "len_ratio": []})
            cls[k]["n"] += v["n"]
            for m in ("stressed_rate", "pitch_re_med_st", "len_ratio"):
                cls[k][m].append(v[m])
    out = {k: q(v) for k, v in R.items()}
    out["n_shorts"] = len(files)
    out["by_class"] = {k: {"words": v["n"], **{m: q(v[m]) for m in ("stressed_rate", "pitch_re_med_st", "len_ratio")}}
                       for k, v in cls.items()}
    out["pace_by_sentence_words"] = {k: q(v) for k, v in rate_len.items()}
    out["pauses"] = {k: {"boundaries": len(v), "share_ge_30ms": round(float(np.mean(np.array(v) >= 0.03)), 2),
                         "share_ge_80ms": round(float(np.mean(np.array(v) >= 0.08)), 2),
                         "median_s_when_present": round(float(np.median([g for g in v if g >= 0.03])), 3) if any(g >= 0.03 for g in v) else None}
                     for k, v in pauses.items()}
    out["hook"] = {"hooks": hook["hooks"], "first_verb_is_pitch_peak": hook["act_verb_is_pitch_peak"],
                   "first_verb_pitch_st": q(hook["act_verb_pitch_st"]), "hook_end_len_ratio": q(hook["hook_end_len"]),
                   "hook_end_stressed": hook["hook_end_stressed"]}
    return out


if __name__ == "__main__":
    res = {}
    for a in sys.argv[2:]:
        name, d = a.split("=", 1)
        res[name] = group([f for f in sorted(glob.glob(d.rstrip("/") + "/*.json"))])
    json.dump(res, open(sys.argv[1], "w"), indent=1)
    print(json.dumps(res, indent=1)[:6000])
