"""Prosody-transplant gap test: put a reference read's delivery onto OUR voice saying the same words.

What is copied, as numbers only: each word's duration and the pause lengths (time warp at word boundaries), the
pitch contour in semitones relative to the reference speaker's median (re-centred on our voice's own median, so our
register stays ours), and each word's loudness relative to the read's median. Our voice's own audio is what gets
modified (Praat PSOLA overlap-add through parselmouth); no reference audio is mixed in and its timbre is never
modelled.

usage (voicelab venv):
  python -I prosody_transplant.py ref_audio ref_words.json our_audio our_words.json out.wav
    ref_words / our_words: voice_cadence.py measure output for the same text (word lists must match)
"""
import difflib
import json
import re
import sys

import numpy as np
import parselmouth
from parselmouth.praat import call

STEP = 0.005


def _n(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def pitch_track(snd, floor=65, ceil=520):
    p = snd.to_pitch_ac(time_step=STEP, pitch_floor=floor, pitch_ceiling=ceil)
    t = p.xs()
    f = p.selected_array["frequency"].astype(float)
    f[f <= 0] = np.nan
    # drop octave jumps: frames > 6 st away from a 7-frame running median
    med = np.array([np.nanmedian(f[max(0, i - 3): i + 4]) if np.isfinite(f[max(0, i - 3): i + 4]).any() else np.nan
                    for i in range(len(f))])
    bad = np.isfinite(f) & np.isfinite(med) & (np.abs(12 * np.log2(f / med)) > 6)
    f[bad] = np.nan
    return t, f


def knots(ref_w, our_w, ref_end, our_end):
    a, b = [_n(w["text"]) for w in ref_w], [_n(w["text"]) for w in our_w]
    pairs = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                r, o = ref_w[i1 + k], our_w[j1 + k]
                pairs += [(o["start"], r["start"]), (o["end"], r["end"])]
    pts = [(0.0, 0.0)] + sorted(pairs) + [(our_end, ref_end)]
    out = [pts[0]]
    for o, r in pts[1:]:  # strictly increasing on both axes; a pause of ours where the ref has none -> ~5 ms
        if o - out[-1][0] < 0.01:
            continue
        r = max(r, out[-1][1] + 0.005)
        out.append((o, r))
    return out


def transplant(ref_audio, ref_words, our_audio, our_words, out_path, loud_clip=9.0):
    ref = parselmouth.Sound(ref_audio)
    ours = parselmouth.Sound(our_audio)
    if ours.n_channels > 1:
        ours = ours.convert_to_mono()
    if ref.n_channels > 1:
        ref = ref.convert_to_mono()
    rw, ow = json.load(open(ref_words))["words"], json.load(open(our_words))["words"]
    K = knots(rw, ow, ref.duration, ours.duration)
    ko, kr = np.array([k[0] for k in K]), np.array([k[1] for k in K])
    # durations: a step DurationTier, one factor per interval of our timeline (words and the gaps between them)
    dt = call("Create DurationTier", "dur", 0.0, ours.duration)
    for (o0, r0), (o1, r1) in zip(K, K[1:]):
        fac = float(np.clip((r1 - r0) / (o1 - o0), 0.02, 4.0))
        call(dt, "Add point", o0 + 1e-4, fac)
        call(dt, "Add point", o1 - 1e-4, fac)
    # pitch: the reference's contour in st re its median, re-centred on our median, sampled on our own time axis
    rt, rf = pitch_track(ref)
    ot, of = pitch_track(ours)
    r_med, o_med = np.nanmedian(rf), np.nanmedian(of)
    pt = call("Create PitchTier", "pitch", 0.0, ours.duration)
    n_pts = 0
    for t in np.arange(0.0, ours.duration, STEP):
        tau = float(np.interp(t, ko, kr))
        i = int(round((tau - rt[0]) / STEP))
        if 0 <= i < len(rf) and np.isfinite(rf[i]):
            call(pt, "Add point", float(t), float(o_med * (rf[i] / r_med)))
            n_pts += 1
    man = call(ours, "To Manipulation", STEP, 60, 600)
    call([pt, man], "Replace pitch tier")
    call([dt, man], "Replace duration tier")
    res = call(man, "Get resynthesis (overlap-add)")
    y = res.values[0].astype(np.float64)
    sr = res.sampling_frequency
    # loudness: word by word, the reference's word peak (re its median) replaces ours, 30 ms ramps
    def word_db(snd, words, tmap=None):
        x = snd.values[0]
        s = snd.sampling_frequency
        out = []
        for w in words:
            a, b = (w["start"], w["end"]) if tmap is None else (tmap(w["start"]), tmap(w["end"]))
            seg = x[int(a * s): max(int(a * s) + 1, int(b * s))]
            win = max(1, int(0.03 * s))
            if len(seg) < win:
                out.append(None)
                continue
            r = np.sqrt(np.convolve(seg ** 2, np.ones(win) / win, mode="valid"))
            out.append(20 * np.log10(max(r.max(), 1e-6)))
        v = np.array([x for x in out if x is not None])
        med = np.median(v) if len(v) else 0.0
        return [None if x is None else x - med for x in out]
    a_, b_ = [_n(w["text"]) for w in rw], [_n(w["text"]) for w in ow]
    pairs = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a_, b=b_, autojunk=False).get_opcodes():
        if tag == "equal":
            pairs += [(rw[i1 + k], ow[j1 + k]) for k in range(i2 - i1)]
    ref_db = word_db(ref, [p[0] for p in pairs])
    # our words now sit on the reference timeline (that is what the duration tier did)
    new_words = [{"start": p[0]["start"], "end": p[0]["end"]} for p in pairs]
    res_snd = parselmouth.Sound(y[None], sampling_frequency=sr)
    our_db = word_db(res_snd, new_words)
    g_t, g_v = [], []
    for (r, _), w, rd, od in zip(pairs, new_words, ref_db, our_db):
        g = 0.0 if rd is None or od is None else float(np.clip(rd - od, -loud_clip, loud_clip))
        g_t += [w["start"] + 0.015, w["end"] - 0.015]
        g_v += [g, g]
    if g_t:
        t = np.arange(len(y)) / sr
        gain = 10 ** (np.interp(t, g_t, g_v) / 20)
        y = y * gain
    y = y / max(1e-6, np.abs(y).max()) * 0.89
    import soundfile as sf
    sf.write(out_path, y.astype(np.float32), int(sr))
    return {"knots": len(K), "pitch_points": n_pts, "ref_median_hz": round(float(r_med), 1),
            "our_median_hz": round(float(o_med), 1), "duration_s": round(len(y) / sr, 2),
            "word_gain_db": [round(x, 1) for x in g_v[::2]]}


if __name__ == "__main__":
    print(json.dumps(transplant(*sys.argv[1:6])))
