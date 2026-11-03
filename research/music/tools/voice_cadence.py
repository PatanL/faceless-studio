"""Per-word prosody of a narration: which words carry stress, phrase pitch shape, pace and pauses.

Built for research/music/VOICE_CADENCE.md. It measures delivery only (where stress falls, pitch movement, pace and
pauses) and never models a speaker's timbre. Reference audio stays outside the repo (~/faceless-work/).

usage (Mac, the voicelab venv outside the repo: faster-whisper, librosa, spaCy en_core_web_sm):
  ~/faceless-work/venvs/voicelab/bin/python -I research/music/tools/voice_cadence.py measure in.flac out.json \
      [--text script.txt] [--label name]
  ... voice_cadence.py summary out1.json out2.json ... > summary.json

Per word: start/end (transcript from faster-whisper medium.en, or the known script with --text; times from torchaudio's
MMS_FA CTC forced aligner, then re-cut at real silences),
syllables, f0 peak and median in semitones re the speaker's median f0, local pitch prominence (peak minus the mean
of the neighbouring words' peaks), peak loudness re the speaker's median word peak, per-syllable duration re the
speaker's median, a composite stress score (sum of the three z-scores), POS / word class.
Per phrase (split at punctuation or a gap >= 150 ms): f0 range p10-p90 (st), start and end pitch, pace.
Whole file: the same voice numbers RICKS_SOUND.md uses (f0 median, p5-p95 st, 1 s-median spread p10-p90), plus
stress contrast (mean prominence of stressed minus unstressed words), pauses and their places.
"""
from __future__ import annotations

import difflib
import json
import os
import re
import sys

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ["CUDA_VISIBLE_DEVICES"] = ""

import numpy as np

SR = 22050
HOP = 110  # 5 ms
STRESS_Z = 1.0  # composite z-score at or above which a word counts as stressed
GAP_PHRASE = 0.15
CONTRAST = {"but", "only", "just", "even", "actually", "never", "still", "yet", "instead", "nothing", "no", "not",
            "all", "every", "ever", "entire", "whole", "nobody", "none", "already", "until", "except", "except",
            "turns", "real", "really", "so", "too", "most", "first", "last", "single", "himself", "herself"}
NUMWORDS = {"one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
            "twenty", "thirty", "forty", "fifty", "hundred", "hundreds", "thousand", "thousands", "million",
            "millions", "billion", "half", "dozen", "dozens", "once", "twice", "first", "second", "third"}


def _norm(w):
    return re.sub(r"[^a-z0-9']", "", w.lower())


def syllables(word):
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return max(1, len(re.sub(r"\D", "", word)))  # digits: about one syllable each
    groups = re.findall(r"[aeiouy]+", w)
    n = len(groups)
    if w.endswith("e") and not w.endswith(("le", "ee", "ye")) and n > 1:
        n -= 1
    if w.endswith("ed") and not w.endswith(("ted", "ded")) and n > 1:
        n -= 1
    return max(1, n)


_WHISPER = None


def transcribe(path):
    global _WHISPER
    from faster_whisper import WhisperModel
    if _WHISPER is None:
        _WHISPER = WhisperModel(os.environ.get("WHISPER_MODEL", "medium.en"), device="cpu", compute_type="int8",
                                cpu_threads=int(os.environ.get("THREADS", "6")))
    import subprocess
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-vn", "-ac", "1", "-ar", "16000", "-f", "f32le",
                          "-"], check=True, capture_output=True).stdout
    a16 = np.frombuffer(raw, np.float32).copy()
    segs, _ = _WHISPER.transcribe(a16, word_timestamps=True, beam_size=5, language="en",
                                  condition_on_previous_text=True, vad_filter=False)
    return [{"text": w.word.strip(), "start": float(w.start), "end": float(w.end)} for s in segs for w in s.words]


def align_to_text(words, text):
    """Give the known script words the whisper times (difflib on normalised words; gaps interpolated)."""
    sw = text.split()
    a, b = [_norm(w) for w in sw], [_norm(w["text"]) for w in words]
    times = [None] * len(sw)
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                times[i1 + k] = (words[j1 + k]["start"], words[j1 + k]["end"])
        elif tag == "replace" and j2 > j1:
            s0, e0, n = words[j1]["start"], words[j2 - 1]["end"], i2 - i1
            for k in range(n):
                times[i1 + k] = (s0 + (e0 - s0) * k / n, s0 + (e0 - s0) * (k + 1) / n)
    matched = sum(t is not None for t in times) / max(1, len(times))
    for i in range(len(times)):
        if times[i] is None:
            lo = times[i - 1][1] if i and times[i - 1] else 0.0
            j = i
            while j < len(times) and times[j] is None:
                j += 1
            hi = times[j][0] if j < len(times) else lo + 0.3 * (j - i)
            n = j - i
            for k in range(n):
                times[i + k] = (lo + (hi - lo) * k / n, lo + (hi - lo) * (k + 1) / n)
    return [{"text": w, "start": s, "end": e} for w, (s, e) in zip(sw, times)], matched


_ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen " \
        "seventeen eighteen nineteen".split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def num_words(n):
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + ("" if n % 10 == 0 else " " + _ONES[n % 10])
    if n < 1000:
        return _ONES[n // 100] + " hundred" + ("" if n % 100 == 0 else " " + num_words(n % 100))
    if n < 1000000:
        return num_words(n // 1000) + " thousand" + ("" if n % 1000 == 0 else " " + num_words(n % 1000))
    return " ".join(_ONES[int(c)] for c in str(n))


def spoken_chars(word):
    """Word -> list of letter-only tokens the MMS aligner can use ('39' -> 'thirty nine', 'brand-new' -> 2)."""
    w = word.lower().replace("’", "'")
    w = re.sub(r"\d+", lambda m: " " + num_words(int(m.group())) + " ", w.replace(",", "") if re.search(r"\d", w) else w)
    toks = [re.sub(r"[^a-z']", "", t) for t in re.split(r"[\s\-–—]+", w)]
    return [t.strip("'") for t in toks if t.strip("'")]


_FA = None


def force_align(path, words):
    """CTC forced alignment (torchaudio MMS_FA) of the transcript words: start/end per word to ~20 ms.
    Whisper's own word times collapse some words to zero length and widen gaps at punctuation."""
    global _FA
    import subprocess
    import torch
    import torchaudio
    if _FA is None:
        b = torchaudio.pipelines.MMS_FA
        _FA = (b, b.get_model(with_star=False).eval(), b.get_tokenizer(), b.get_aligner())
    b, model, tok, aligner = _FA
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(b.sample_rate),
                          "-f", "f32le", "-"], check=True, capture_output=True).stdout
    wav = torch.from_numpy(np.frombuffer(raw, np.float32).copy())[None]
    with torch.inference_mode():
        em, _ = model(wav)
    ratio = wav.shape[1] / em.shape[1] / b.sample_rate
    pieces, owner = [], []
    for i, w in enumerate(words):
        for t in spoken_chars(w["text"]):
            pieces.append(t)
            owner.append(i)
    spans = aligner(em[0], tok(pieces))
    got = {}
    for k, sp in enumerate(spans):
        s, e = sp[0].start * ratio, sp[-1].end * ratio
        i = owner[k]
        got[i] = (min(s, got[i][0]), max(e, got[i][1])) if i in got else (s, e)
    out = []
    for i, w in enumerate(words):
        if i in got:
            out.append({**w, "start": float(got[i][0]), "end": float(got[i][1])})
        else:  # no letters (e.g. "%"): squeeze between neighbours
            prev = out[-1]["end"] if out else 0.0
            out.append({**w, "start": prev, "end": prev})
    return out


_NLP = None


def tag(words):
    global _NLP
    import spacy
    if _NLP is None:
        _NLP = spacy.load("en_core_web_sm")
    text = " ".join(w["text"] for w in words)
    doc = _NLP(text)
    # map tokens back to words by character offsets
    offs, pos = [], 0
    for w in words:
        offs.append((pos, pos + len(w["text"])))
        pos += len(w["text"]) + 1
    for w, (s, e) in zip(words, offs):
        toks = [t for t in doc if t.idx >= s and t.idx < e and not t.is_punct]
        t = toks[0] if toks else None
        w["pos"] = t.pos_ if t else "X"
        w["dep"] = t.dep_ if t else ""
        w["cls"] = word_class(w["text"], t)
    return words


def word_class(text, t):
    n = _norm(text).strip("'")
    if n in CONTRAST:
        return "contrast"
    if re.search(r"\d", n) or n in NUMWORDS or (t is not None and t.pos_ == "NUM"):
        return "number"
    if t is None:
        return "other"
    if t.pos_ == "PROPN":
        return "name"
    if t.pos_ == "VERB":
        return "verb"
    if t.pos_ == "NOUN":
        return "object" if t.dep_ in ("dobj", "pobj", "attr", "oprd") else "noun"
    if t.pos_ in ("ADJ", "ADV"):
        return "modifier"
    if t.pos_ in ("PRON",) and n in ("he", "she", "they", "i", "we"):
        return "subject_pron"
    return "function"


def features(path, words):
    import librosa
    y, _ = librosa.load(path, sr=SR, mono=True)
    f0, vflag, _ = librosa.pyin(y, fmin=65, fmax=520, sr=SR, frame_length=1024, hop_length=HOP)
    t = librosa.frames_to_time(np.arange(len(f0)), sr=SR, hop_length=HOP)
    ok = vflag & np.isfinite(f0)
    med = float(np.median(f0[ok]))
    st = np.full_like(f0, np.nan)
    st[ok] = 12 * np.log2(f0[ok] / med)
    # 30 ms RMS on the same 5 ms grid
    rms = librosa.feature.rms(y=y, frame_length=662, hop_length=HOP, center=True)[0]
    db = 20 * np.log10(np.maximum(rms[: len(t)], 1e-6))
    # Word boundaries from the signal. Whisper widens the gap at every punctuation mark (0.12-0.36 s), while the real
    # silence there is usually 0.01-0.10 s (VS1Z check). So each boundary is re-cut at the longest run of frames
    # 25 dB under the speech median between the two words; with no such run (>= 30 ms) the words touch.
    sp = (t >= words[0]["start"]) & (t <= words[-1]["end"]) if words else np.ones_like(t, bool)
    sp_med = float(np.median(db[sp]))
    quiet = db < sp_med - 25.0
    for a, b in zip(words, words[1:]):
        lo, hi = max(a["start"] + 0.04, a["end"] - 0.15), min(b["end"] - 0.04, b["start"] + 0.15)
        idx = np.nonzero((t >= lo) & (t <= hi))[0]
        best, cur, best_end = 0, 0, None
        for k in idx:
            cur = cur + 1 if quiet[k] else 0
            if cur > best:
                best, best_end = cur, k
        if best * HOP / SR >= 0.03:
            s0 = t[best_end - best + 1]
            a["end"], b["start"] = float(s0), float(t[best_end] + HOP / SR)
        elif b["start"] > a["end"]:
            a["end"] = b["start"]
    out = {"f0_median_hz": round(med, 1)}
    fv = f0[ok]
    s_all = st[ok]
    out["f0_p5_p95_hz"] = [round(float(np.percentile(fv, 5)), 1), round(float(np.percentile(fv, 95)), 1)]
    out["f0_range_p5_p95_st"] = round(float(np.percentile(s_all, 95) - np.percentile(s_all, 5)), 2)
    meds = []
    for w0 in np.arange(0, t[-1], 1.0):
        m = (t >= w0) & (t < w0 + 1) & ok
        if m.sum() > 20:
            meds.append(float(np.median(st[m])))
    out["f0_1s_median_spread_st_p10_p90"] = round(float(np.percentile(meds, 90) - np.percentile(meds, 10)), 2) if meds else None
    for w in words:
        m = (t >= w["start"]) & (t < max(w["end"], w["start"] + 0.04))
        vm = m & ok
        w["syl"] = syllables(w["text"])
        w["dur"] = round(w["end"] - w["start"], 3)
        if vm.sum() >= 3:
            w["f0_peak_st"] = round(float(np.percentile(st[vm], 90)), 2)
            w["f0_med_st"] = round(float(np.median(st[vm])), 2)
            w["f0_first_st"] = round(float(np.median(st[vm][: max(3, vm.sum() // 4)])), 2)
            w["f0_last_st"] = round(float(np.median(st[vm][-max(3, vm.sum() // 4):])), 2)
        else:
            w["f0_peak_st"] = w["f0_med_st"] = w["f0_first_st"] = w["f0_last_st"] = None
        w["loud_db"] = round(float(np.max(db[m])), 2) if m.any() else None
    return out, (t, st, ok, db)


def phrases(words):
    out, cur = [], []
    for i, w in enumerate(words):
        cur.append(i)
        nxt_gap = words[i + 1]["start"] - w["end"] if i + 1 < len(words) else 9
        if re.search(r"[.!?,;:—–-]$", w["text"]) or nxt_gap >= GAP_PHRASE:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def sentences(words):
    out, cur = [], []
    for i, w in enumerate(words):
        cur.append(i)
        if re.search(r"[.!?]['\"”’)]*$", w["text"]):
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def score(words):
    """Local prominence and the composite stress score."""
    peaks = [w["f0_peak_st"] for w in words]
    louds = [w["loud_db"] for w in words]
    ph_of = {}
    for pi, ph in enumerate(phrases(words)):
        for i in ph:
            ph_of[i] = pi
    for i, w in enumerate(words):
        nb = [peaks[j] for j in (i - 1, i + 1) if 0 <= j < len(words) and peaks[j] is not None]
        w["pitch_prom_st"] = round(peaks[i] - float(np.mean(nb)), 2) if peaks[i] is not None and nb else None
        nl = [louds[j] for j in (i - 1, i + 1) if 0 <= j < len(words) and louds[j] is not None]
        w["loud_prom_db"] = round(louds[i] - float(np.mean(nl)), 2) if louds[i] is not None and nl else None
        w["phrase"] = ph_of[i]
    psd = [w["dur"] / w["syl"] for w in words if w["cls"] != "function"]
    med_psd = float(np.median(psd)) if psd else 0.2
    for w in words:
        w["len_ratio"] = round((w["dur"] / w["syl"]) / med_psd, 3)
    meds = {}
    for k in ("f0_peak_st", "loud_db"):
        v = [w[k] for w in words if w[k] is not None]
        meds[k] = float(np.median(v)) if v else 0.0
    for w in words:
        w["pitch_re_med_st"] = None if w["f0_peak_st"] is None else round(w["f0_peak_st"] - meds["f0_peak_st"], 2)
        w["loud_re_med_db"] = None if w["loud_db"] is None else round(w["loud_db"] - meds["loud_db"], 2)

    def z(key, transform=lambda x: x):
        v = np.array([transform(w[key]) for w in words if w[key] is not None], float)
        mu, sd = (float(np.mean(v)), float(np.std(v)) or 1.0) if len(v) else (0.0, 1.0)
        return {id(w): (transform(w[key]) - mu) / sd for w in words if w[key] is not None}

    zp = z("pitch_re_med_st")
    zpp = z("pitch_prom_st")
    zl = z("loud_re_med_db")
    zd = z("len_ratio", lambda x: float(np.log(max(x, 1e-3))))
    for w in words:
        parts = [0.5 * zp.get(id(w), 0.0) + 0.5 * zpp.get(id(w), 0.0), zl.get(id(w), 0.0), zd.get(id(w), 0.0)]
        w["stress_z"] = round(float(sum(parts)) / np.sqrt(2.0), 2)
        w["stressed"] = bool(w["stress_z"] >= STRESS_Z)
    return words


def summarise(words, voice, dur):
    sw = [w for w in words if w["stressed"]]
    uw = [w for w in words if not w["stressed"]]

    def mean(v):
        v = [x for x in v if x is not None]
        return round(float(np.mean(v)), 2) if v else None

    s = dict(voice)
    s["words"] = len(words)
    span = words[-1]["end"] - words[0]["start"] if words else 0
    s["speech_span_s"] = round(span, 2)
    s["words_per_s"] = round(len(words) / span, 2) if span else None
    s["syl_per_s"] = round(sum(w["syl"] for w in words) / span, 2) if span else None
    s["stressed_share"] = round(len(sw) / max(1, len(words)), 3)
    s["stress_contrast"] = {
        "pitch_peak_st": None if not sw or not uw else round(mean([w["pitch_re_med_st"] for w in sw]) - mean([w["pitch_re_med_st"] for w in uw]), 2),
        "pitch_prom_st": mean([w["pitch_prom_st"] for w in sw]),
        "loud_db": None if not sw or not uw else round(mean([w["loud_re_med_db"] for w in sw]) - mean([w["loud_re_med_db"] for w in uw]), 2),
        "len_ratio": None if not sw or not uw else round(mean([w["len_ratio"] for w in sw]) / mean([w["len_ratio"] for w in uw]), 3),
    }
    by = {}
    for w in words:
        by.setdefault(w["cls"], []).append(w)
    s["by_class"] = {c: {"n": len(v), "stressed_rate": round(sum(x["stressed"] for x in v) / len(v), 3),
                         "stress_z": mean([x["stress_z"] for x in v]),
                         "pitch_re_med_st": mean([x["pitch_re_med_st"] for x in v]),
                         "len_ratio": mean([x["len_ratio"] for x in v])} for c, v in sorted(by.items())}
    # where stress lands among the stressed words
    s["stressed_class_share"] = {c: round(sum(1 for w in sw if w["cls"] == c) / max(1, len(sw)), 3) for c in by}
    # phrases
    ph = []
    for idx in phrases(words):
        ws = [words[i] for i in idx]
        pk = [w["f0_peak_st"] for w in ws if w["f0_peak_st"] is not None]
        md = [w["f0_med_st"] for w in ws if w["f0_med_st"] is not None]
        d = ws[-1]["end"] - ws[0]["start"]
        ph.append({"n": len(ws), "range_st": round(max(pk) - min(md), 2) if pk and md else None,
                   "start_st": ws[0]["f0_first_st"] if ws[0]["f0_first_st"] is not None else (md[0] if md else None),
                   "end_st": ws[-1]["f0_last_st"], "max_at": int(np.argmax([w["f0_peak_st"] if w["f0_peak_st"] is not None else -99 for w in ws])) / max(1, len(ws) - 1),
                   "wps": round(len(ws) / d, 2) if d > 0 else None, "text": " ".join(w["text"] for w in ws)})
    s["phrases"] = ph
    multi = [p for p in ph if p["n"] >= 3 and p["range_st"] is not None]
    s["phrase_range_st_median"] = round(float(np.median([p["range_st"] for p in multi])), 2) if multi else None
    # sentences: start / end pitch, pace
    se = []
    for idx in sentences(words):
        ws = [words[i] for i in idx]
        d = ws[-1]["end"] - ws[0]["start"]
        first = [w["f0_med_st"] for w in ws[:2] if w["f0_med_st"] is not None]
        se.append({"n": len(ws), "start_st": mean(first), "end_st": ws[-1]["f0_last_st"],
                   "peak_st": max([w["f0_peak_st"] for w in ws if w["f0_peak_st"] is not None] or [None]) if any(w["f0_peak_st"] is not None for w in ws) else None,
                   "peak_pos": round(int(np.argmax([w["f0_peak_st"] if w["f0_peak_st"] is not None else -99 for w in ws])) / max(1, len(ws) - 1), 2),
                   "wps": round(len(ws) / d, 2) if d > 0 else None,
                   "syl_ps": round(sum(w["syl"] for w in ws) / d, 2) if d > 0 else None,
                   "stressed": [w["text"] for w in ws if w["stressed"]],
                   "text": " ".join(w["text"] for w in ws)})
    s["sentences"] = se
    # pauses
    gaps = []
    for a, b in zip(words, words[1:]):
        g = b["start"] - a["end"]
        if g >= 0.08:
            gaps.append({"after": a["text"], "before": b["text"], "gap_s": round(g, 3),
                         "at_punct": bool(re.search(r"[.!?,;:—–-]$", a["text"])),
                         "before_stressed": b["stressed"]})
    s["pauses"] = gaps
    s["gaps_ge_120ms_per_min"] = round(sum(g["gap_s"] >= 0.12 for g in gaps) / (span / 60), 2) if span else None
    s["gaps_ge_80ms_per_min"] = round(len(gaps) / (span / 60), 2) if span else None
    return s


def measure(path, text=None, label=None):
    words = transcribe(path)
    matched = None
    heard = " ".join(w["text"] for w in words)
    if text:  # whisper checks the content (share of script words heard); the aligner times the script words
        words, matched = align_to_text(words, text)
    words = [w for w in words if _norm(w["text"])]
    words = force_align(path, words)
    tag(words)
    voice, _ = features(path, words)
    score(words)
    dur = words[-1]["end"] if words else 0
    s = summarise(words, voice, dur)
    s["label"] = label or os.path.basename(path)
    s["align_matched"] = matched
    s["heard"] = heard if text else None  # whisper's transcript of a render (refs: not stored, it is their text)
    return {"summary": s, "words": words}


def main(argv):
    if argv[0] == "measure":
        path, out = argv[1], argv[2]
        text = None
        label = None
        if "--text" in argv:
            text = open(argv[argv.index("--text") + 1], encoding="utf-8").read()
        if "--label" in argv:
            label = argv[argv.index("--label") + 1]
        r = measure(path, text, label)
        json.dump(r, open(out, "w"), indent=1)
        s = r["summary"]
        print(f"{s['label']}: f0 {s['f0_median_hz']} Hz, p5-p95 {s['f0_range_p5_p95_st']} st, 1s-spread "
              f"{s['f0_1s_median_spread_st_p10_p90']} st, {s['words_per_s']} w/s, stressed {s['stressed_share']}, "
              f"contrast {s['stress_contrast']}")
    elif argv[0] == "batch":  # batch jobs.json: [{"in", "out", "label", "text"?}] (one whisper load for all)
        for j in json.load(open(argv[1])):
            if os.path.exists(j["out"]) and "--force" not in argv:
                continue
            text = open(j["text"], encoding="utf-8").read() if j.get("text") else None
            r = measure(j["in"], text, j.get("label"))
            json.dump(r, open(j["out"], "w"), indent=1)
            s = r["summary"]
            print(f"{s['label']}: f0 {s['f0_median_hz']} Hz, p5-p95 {s['f0_range_p5_p95_st']} st, 1s-spread "
                  f"{s['f0_1s_median_spread_st_p10_p90']} st, {s['words_per_s']} w/s, stressed {s['stressed_share']}, "
                  f"contrast {s['stress_contrast']}", flush=True)
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
