"""Rule-based melody shaper (`melody: rules`): the prosody transplant of the gap test, but with no reference read.

research/music/VOICE_CADENCE.md found the gap to RicksClips is melody. Putting their measured contour on our voice
lifted the Jar match from 71 to 94. This builds that kind of contour from the measured RULES instead, then applies
it to our own TTS audio with Praat PSOLA (parselmouth). Nothing from any reference recording is used.

Target, per sentence (semitones re the voice's own median):
- a declining line from +1.0 at the first word to -4.0 at the last (refs: onset +1.8, end -5.6, peak in the first
  fifth); function words and pronouns sit 1.5 st under the line;
- stressed words (emphasis.mark: hook act verb, numbers, contrast, names, the twist...) sit +5 st over the line, the
  hook's act verb +7 (refs: +5.2 over unstressed, a 4.5 st jump, act verb +7.1); contrast words get a +2.6 reset;
- the last word falls to -5.6;
- blended with the TTS's own word-level melody (keep_own; it already agrees with real reads at r ~0.75) plus its
  micro-melody, then the whole melody is scaled to the measured 17.2 st p5-p95 range.
Timing: stressed words x1.25 longer, function words x0.85; sentences of 5 words or fewer x1.25 (refs 0.76x pace);
pauses set to 90 ms at full stops, 60 ms at commas, none elsewhere; then a global factor (0.85-1.15) brings the pace
toward 3.75 words/s.

Python API: shape(audio, sr, words, text, spec) -> (audio, time_map) with words [(text, start, end)] in text order.
CLI (any venv with parselmouth, e.g. the qwen3 one; the pipeline calls it as a subprocess):
  python -I melody.py in.wav words.json text.txt out.wav [spec.json]   -> out.wav + out.map.json
"""
from __future__ import annotations

import json
import os
import re
import sys

import numpy as np

DEFAULT = {"line_on": 1.0, "line_off": -4.0, "end_st": -5.6, "func_st": -1.5, "stress_st": 5.0, "act_st": 7.0,
           "contrast_st": 2.6, "alpha": 1.0, "keep_own": 0.6, "target_range_st": 17.2, "range_clip": [0.8, 2.0],
           "len_stress": 1.25, "len_func": 0.85, "short_sentence": 5, "short_slow": 1.25, "gap_stop": 0.09,
           "gap_comma": 0.06, "target_wps": 3.75, "pace_clip": [0.85, 1.15],
           "density": 0.35}  # pass 3 (VOICE_CADENCE.md section 8); pass 1's rules-only contour flattened the read


def _plan(words, text, p):
    """Per word: (kind, pitch offset re the sentence line, duration factor, sentence id, position in sentence)."""
    try:
        from . import emphasis as E
    except ImportError:
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        from pipeline.audio import emphasis as E
    toks = text.split()
    def _ls(v):  # front matter "stress: a, b" or a list
        return [x.strip() for x in v.split(",") if x.strip()] if isinstance(v, str) else list(v or [])
    marks = {m.index: m.reason for m in E.mark(text, force=_ls(p.get("stress")), veto=_ls(p.get("unstress")),
                                               density=p["density"])} if len(toks) == len(words) else {}
    sents, cur = [], []
    for i, (w, _, _) in enumerate(words):
        cur.append(i)
        if re.search(r"[.!?][\"'”’)]*$", w):
            sents.append(cur)
            cur = []
    if cur:
        sents.append(cur)
    plan = [None] * len(words)
    for si, sent in enumerate(sents):
        short = len(sent) <= p["short_sentence"]
        for k, i in enumerate(sent):
            n = E._norm(words[i][0])
            r = marks.get(i)
            if r == "act verb":
                kind, off, lf = "act", p["act_st"], p["len_stress"]
            elif r == "contrast":
                kind, off, lf = "contrast", p["contrast_st"], 1.0
            elif r:
                kind, off, lf = "stress", p["stress_st"], p["len_stress"]
            elif n in E.FUNCTION or n in E.SUBJECT:
                kind, off, lf = "func", p["func_st"], p["len_func"]
            else:
                kind, off, lf = "plain", 0.0, 1.0
            if short:
                lf *= p["short_slow"]
            plan[i] = (kind, off, lf, si, k / max(1, len(sent) - 1), k == len(sent) - 1)
    return plan, sents


def shape(audio, sr, words, text, spec=None):
    import parselmouth
    from parselmouth.praat import call
    p = {**DEFAULT, **(spec or {})}
    words = [(w, float(s), float(e)) for w, s, e in words]
    snd = parselmouth.Sound(np.asarray(audio, np.float64)[None], sampling_frequency=sr)
    dur = snd.duration
    plan, sents = _plan(words, text, p)
    man = call(snd, "To Manipulation", 0.005, 60, 600)
    pt = call(man, "Extract pitch tier")
    n = call(pt, "Get number of points")
    ts = np.array([call(pt, "Get time from index", i + 1) for i in range(n)])
    fs = np.array([call(pt, "Get value at index", i + 1) for i in range(n)])
    if n < 10 or not words:
        return np.asarray(audio, np.float32), [[0.0, 0.0], [dur, dur]]
    med = float(np.median(fs))
    st = 12 * np.log2(fs / med)
    # the voice's own per-word median: what is left over is its micro-melody
    wid = np.full(len(ts), -1)
    for i, (_, s, e) in enumerate(words):
        wid[(ts >= s) & (ts < max(e, s + 0.02))] = i
    resid = np.zeros_like(st)
    for i in range(len(words)):
        m = wid == i
        if m.any():
            resid[m] = st[m] - np.median(st[m])
    # anchors of the target contour: (time, st)
    anchors = []
    for sent in sents:
        s0, s1 = words[sent[0]][1], words[sent[-1]][2]
        span = max(1e-3, s1 - s0)
        for i in sent:
            kind, off, _, _, _, last = plan[i]
            w, s, e = words[i]
            mid = 0.5 * (s + e)
            line = p["line_on"] + (p["line_off"] - p["line_on"]) * (mid - s0) / span
            v = line + off
            if kind in ("stress", "act"):
                anchors += [(s + 0.15 * (e - s), line + 0.3 * off), (s + 0.4 * (e - s), v), (s + 0.75 * (e - s), v)]
            else:
                anchors += [(s + 0.3 * (e - s), v), (s + 0.7 * (e - s), v)]
            if last:
                anchors.append((e - 0.02, min(v, p["end_st"]) if kind != "act" else v))
    anchors.sort()
    at, av = np.array([a[0] for a in anchors]), np.array([a[1] for a in anchors])
    rule = np.interp(ts, at, av)
    # keep the TTS's own word-level melody too (it already agrees with real reads at r ~0.75): its per-word medians
    own = np.zeros_like(st)
    for i in range(len(words)):
        m = wid == i
        if m.any():
            own[m] = np.median(st[m])
    target = (1 - p["keep_own"]) * rule + p["keep_own"] * own + p["alpha"] * resid
    # then widen or narrow the whole melody to the measured range (refs p5-p95 17.2 st)
    c = float(np.median(target))
    cur = float(np.percentile(target, 95) - np.percentile(target, 5))
    k = float(np.clip(p["target_range_st"] / max(cur, 1e-3), *p["range_clip"]))
    target = np.clip(c + (target - c) * k, -12.0, 14.0)
    new = call("Create PitchTier", "melody", 0.0, dur)
    for t, v in zip(ts, target):
        call(new, "Add point", float(t), float(med * 2 ** (v / 12)))
    call([new, man], "Replace pitch tier")
    # durations: intervals = lead, word, gap, word, ..., tail; one factor each
    iv = []
    if words[0][1] > 0:
        iv.append((0.0, words[0][1], 1.0, "lead"))
    for i, (w, s, e) in enumerate(words):
        iv.append((s, e, plan[i][2], "word"))
        if i + 1 < len(words):
            g0, g1 = e, words[i + 1][1]
            if g1 - g0 > 0.005:
                want = p["gap_stop"] if re.search(r"[.!?][\"'”’)]*$", w) else p["gap_comma"] if re.search(r"[,;:—–]$", w) else 0.0
                iv.append((g0, g1, max(0.02, min(1.0, want / (g1 - g0))) if want < g1 - g0 else 1.0, "gap"))
    if words[-1][2] < dur:
        iv.append((words[-1][2], dur, 1.0, "tail"))
    # pace toward target words/s (speech span only)
    span_new = sum((b - a) * f for a, b, f, k in iv if k in ("word", "gap"))
    want_span = len(words) / p["target_wps"]
    word_t = sum((b - a) * f for a, b, f, k in iv if k == "word")
    g = float(np.clip((want_span - (span_new - word_t)) / max(1e-3, word_t), *p["pace_clip"]))
    iv = [(a, b, f * g if k == "word" else f, k) for a, b, f, k in iv]
    dt = call("Create DurationTier", "dur", 0.0, dur)
    for a, b, f, _ in iv:
        if b - a < 0.004:
            continue
        call(dt, "Add point", a + 0.001, f)
        call(dt, "Add point", b - 0.001, f)
    call([dt, man], "Replace duration tier")
    out = call(man, "Get resynthesis (overlap-add)").values[0]
    pk = np.abs(out).max()
    if pk > 0.98:
        out = out * 0.98 / pk
    # time map: original -> new, at every interval edge
    tmap, t_new = [[0.0, 0.0]], 0.0
    for a, b, f, _ in iv:
        t_new += (b - a) * f
        tmap.append([round(b, 4), round(t_new, 4)])
    return out.astype(np.float32), tmap


def remap(t, tmap):
    a = np.array(tmap)
    return float(np.interp(t, a[:, 0], a[:, 1]))


if __name__ == "__main__":
    import soundfile as sf
    a, sr = sf.read(sys.argv[1], dtype="float32")
    if a.ndim > 1:
        a = a.mean(1)
    raw = json.load(open(sys.argv[2]))
    if isinstance(raw, dict):
        raw = raw["words"]
    words = [(w["text"], w["start"], w["end"]) if isinstance(w, dict) else tuple(w) for w in raw]
    text = open(sys.argv[3], encoding="utf-8").read()
    spec = json.load(open(sys.argv[5])) if len(sys.argv) > 5 else None
    y, tmap = shape(a, sr, words, text, spec)
    sf.write(sys.argv[4], y, sr)
    json.dump(tmap, open(sys.argv[4][:-4] + ".map.json", "w"))


def apply_external(audio48, words, cfg, sr=48000, log=print):
    """Pipeline hook (`melody: rules`): run shape() in a venv that has parselmouth (cfg melody_python, default the
    qwen3 venv), on the whole voice track. -> (audio, words, time_map) with the word times remapped."""
    import subprocess
    import tempfile
    import soundfile as sf
    from .config import QWEN3
    py = os.path.expanduser(cfg.get("melody_python") or os.environ.get("QWEN3_TTS_PYTHON", QWEN3["python"]))
    with tempfile.TemporaryDirectory() as d:
        sf.write(os.path.join(d, "in.wav"), audio48, sr)
        json.dump([[w["text"], w["start"], w["end"]] for w in words], open(os.path.join(d, "w.json"), "w"))
        open(os.path.join(d, "t.txt"), "w").write(" ".join(w["text"] for w in words))
        spec = os.path.join(d, "spec.json")
        json.dump(cfg.get("melody_spec") or {}, open(spec, "w"))
        subprocess.run([py, "-I", os.path.abspath(__file__), os.path.join(d, "in.wav"), os.path.join(d, "w.json"),
                        os.path.join(d, "t.txt"), os.path.join(d, "out.wav"), spec], check=True)
        y, _ = sf.read(os.path.join(d, "out.wav"), dtype="float32")
        tmap = json.load(open(os.path.join(d, "out.map.json")))
    new = [{**w, "start": round(remap(w["start"], tmap), 3), "end": round(remap(w["end"], tmap), 3)} for w in words]
    log(f"[tts] melody: rules ({len(audio48) / sr:.2f}s -> {len(y) / sr:.2f}s)")
    return y, new, tmap
