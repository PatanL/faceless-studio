"""Rule-driven prosody boost: widen OUR render's own melody and push the rule-marked stresses toward the measured
RicksClips / Zack D. delivery (research/music/VOICE_CADENCE.md section 3). The target is the measured statistics,
not any recording: nothing from a reference read is used.

On the TTS output (Praat PSOLA through parselmouth):
- pitch: every f0 point's distance from the voice's median (in semitones) is scaled so the render's p5-p95 range
  reaches `target_range_st` (refs 17.2 st; never compressed, at most `max_expand`), and each stressed
  word gets a smooth `bump_st` rise (a raised cosine over the word). The aim is the refs' ~17 st p5-p95 and ~9 st
  phrase movement, with stressed words ~5 st over the rest;
- length: stressed words are stretched by `lengthen`; the other words are shortened so the total length is unchanged.

Words are [(text, start, end)] (forced-aligned); `stressed` holds the indices of the stressed words
(pipeline/audio/emphasis.py). Experimental, not in the pipeline: on the Jar it lifted a plain Qwen take from 71 to 80
(voice_compare match) but gave an emphasised take only +0.3, inside the take-to-take noise (VOICE_CADENCE.md section 4).
Runs in any venv with parselmouth (qwen3tts, voicelab).

usage: python -I prosody_boost.py in.wav words.json out.wav "<the script text>"   (marks computed here)
"""
import json
import sys

import numpy as np

DEFAULT = {"target_range_st": 17.2, "max_expand": 1.8, "bump_st": 2.5, "lengthen": 1.2, "max_up_st": 14.0,
           "max_down_st": -12.0}


def boost(audio, sr, words, stressed, spec=None):
    import parselmouth
    from parselmouth.praat import call
    p = {**DEFAULT, **(spec or {})}
    snd = parselmouth.Sound(np.asarray(audio, np.float64)[None], sampling_frequency=sr)
    man = call(snd, "To Manipulation", 0.005, 60, 600)
    pt = call(man, "Extract pitch tier")
    n = call(pt, "Get number of points")
    ts = np.array([call(pt, "Get time from index", i + 1) for i in range(n)])
    fs = np.array([call(pt, "Get value at index", i + 1) for i in range(n)])
    if n < 10:
        return np.asarray(audio, np.float32)
    med = float(np.median(fs))
    st0 = 12 * np.log2(fs / med)
    cur = float(np.percentile(st0, 95) - np.percentile(st0, 5))
    expand = float(np.clip(p["target_range_st"] / max(cur, 1e-3), 1.0, p["max_expand"]))
    st = st0 * expand
    for i in stressed:
        if i >= len(words):
            continue
        _, s, e = words[i]
        if e - s < 0.04:
            continue
        m = (ts >= s) & (ts <= e)
        ph = (ts[m] - s) / (e - s)
        st[m] += p["bump_st"] * np.sin(np.pi * np.clip(ph * 1.2, 0, 1)) ** 2 + 0.0
    st = np.clip(st, p["max_down_st"], p["max_up_st"])
    new = call("Create PitchTier", "boost", 0.0, snd.duration)
    for t, v in zip(ts, st):
        call(new, "Add point", float(t), float(med * 2 ** (v / 12)))
    call([new, man], "Replace pitch tier")
    # duration: stressed words longer, the rest shorter, same total
    marked = [(words[i][1], words[i][2]) for i in sorted(set(stressed)) if i < len(words) and words[i][2] - words[i][1] >= 0.04]
    if marked and p["lengthen"] != 1.0:
        tm = sum(e - s for s, e in marked)
        rest = snd.duration - tm
        other = max(0.6, (snd.duration - p["lengthen"] * tm) / rest) if rest > 0.2 else 1.0
        dt = call("Create DurationTier", "len", 0.0, snd.duration)
        call(dt, "Add point", 0.0, other)
        for s, e in marked:
            call(dt, "Add point", s - 0.002, other)
            call(dt, "Add point", s + 0.002, p["lengthen"])
            call(dt, "Add point", e - 0.002, p["lengthen"])
            call(dt, "Add point", e + 0.002, other)
        call([dt, man], "Replace duration tier")
    out = call(man, "Get resynthesis (overlap-add)").values[0]
    pk = np.abs(out).max()
    if pk > 0.98:
        out = out * 0.98 / pk
    return out.astype(np.float32)


def remap_words(words, stressed, spec=None):
    """Word times after boost's duration change (same piecewise factors), so captions stay in sync."""
    p = {**DEFAULT, **(spec or {})}
    marked = sorted(set(i for i in stressed if i < len(words) and words[i][2] - words[i][1] >= 0.04))
    if not marked or p["lengthen"] == 1.0:
        return words
    total = max(w[2] for w in words) + 0.5
    tm = sum(words[i][2] - words[i][1] for i in marked)
    rest = total - tm
    other = max(0.6, (total - p["lengthen"] * tm) / rest) if rest > 0.2 else 1.0
    spans = [(words[i][1], words[i][2]) for i in marked]

    def f(t):
        out, last = 0.0, 0.0
        for s, e in spans:
            if t <= s:
                break
            out += (s - last) * other
            out += (min(t, e) - s) * p["lengthen"]
            last = e
            if t <= e:
                return out
        return out + (t - last) * other
    return [(w, round(f(s), 3), round(f(e), 3)) for w, s, e in words]


if __name__ == "__main__":
    import os
    import soundfile as sf
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from pipeline.audio import emphasis as E
    a, sr = sf.read(sys.argv[1], dtype="float32")
    if a.ndim > 1:
        a = a.mean(1)
    raw = json.load(open(sys.argv[2]))
    words = [(w["text"], w["start"], w["end"]) for w in raw["words"]] if isinstance(raw, dict) else [tuple(w) for w in raw]
    marks = [m.index for m in E.mark(sys.argv[4])]
    spec = json.loads(sys.argv[5]) if len(sys.argv) > 5 else None
    sf.write(sys.argv[3], boost(a, sr, words, marks, spec), sr)
