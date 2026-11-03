"""Every swish (short noise whoosh) of a video, measured one by one. Study only.

For each event (an onset time from story_sound.py's whoosh class, or our own cue list) on a stem that holds the SFX
(Demucs drums for the references, our own sfx.wav when we have it):

  level      peak 100 ms loudness of the swish minus the voice's median momentary loudness in the speech within +-2 s
  shape      duration, attack and release from the 5 ms envelope (onset/end at peak - 20 dB)
  pitch      centroid at the start / peak / end third, movement in octaves -> rising | falling | arch | flat
  colour     brightness (energy share above 4 kHz), flatness (noise ~0.1+ vs tone ~0.01)
  width      side/mid energy (dB) and the L/R correlation
  landing    cut | dissolve | camera whip | motion (prop moves or appears) | nothing, within 0.25 s; and which cuts,
             dissolves and whips carry no swish

usage: python -I swish.py --stem drums.flac --voice vocals.flac --events meas.json|cues.json --key K --out out.json
       [--frames ricks24_metrics.json:ID] [--cuts cuts.json] [--motion motion.json] [--kinds whoosh] [--cues whoosh,...]
"""
import argparse
import json
import os
import sys

import numpy as np
import soundfile as sf
from scipy.signal import resample_poly

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze import close_gaps, loudness_track  # noqa: E402

SR = 44100


def load(p):
    x, r = sf.read(p, dtype="float32", always_2d=True)
    if r != SR:
        from math import gcd
        g = gcd(SR, r)
        x = resample_poly(x, SR // g, r // g, axis=0).astype(np.float32)
    return np.repeat(x, 2, 1) if x.shape[1] == 1 else x


def features(x, t, vM, speech, hop_v=0.1):
    """x stereo stem; t onset guess"""
    import librosa
    i0 = max(0, int((t - 0.15) * SR))
    i1 = min(len(x), int((t + 1.2) * SR))
    from scipy.signal import butter, sosfiltfilt
    # 150 Hz high-pass: the drums stem carries bass/kick bleed under the swishes
    seg = sosfiltfilt(butter(4, 150, "highpass", fs=SR, output="sos"), x[i0:i1], axis=0).astype(np.float32)
    m = seg.mean(1)
    h = int(0.005 * SR)
    n = len(m) // h
    if n < 10:
        return None
    env = 10 * np.log10(np.mean(m[: n * h].reshape(n, h) ** 2, 1) + 1e-12)
    # the peak inside 0.6 s after the onset guess
    lo, hi = int(0.1 / 0.005), min(n, int(0.75 / 0.005))
    pk = lo + int(np.argmax(env[lo:hi]))
    thr = env[pk] - 20
    a = pk
    while a > 0 and env[a - 1] > thr and pk - a < int(0.4 / 0.005):
        a -= 1
    b = pk
    while b < n - 1 and env[b + 1] > thr:
        b += 1
    on_t, pk_t, end_t = (i0 + a * h) / SR, (i0 + pk * h) / SR, (i0 + (b + 1) * h) / SR
    s0, s1 = a * h, (b + 1) * h
    y = m[s0:s1]
    if len(y) < 512:
        y = np.pad(y, (0, 512 - len(y)))
    S = np.abs(librosa.stft(y, n_fft=512, hop_length=128)) ** 2
    f = librosa.fft_frequencies(sr=SR, n_fft=512)
    e = S.sum(0)
    cen = (f[:, None] * S).sum(0) / (e + 1e-12)
    k = len(cen)
    third = max(1, k // 3)
    w = e + 1e-12
    c_start = float(np.average(cen[:third], weights=w[:third]))
    c_end = float(np.average(cen[-third:], weights=w[-third:]))
    c_peak = float(cen[int(np.argmax(e))])
    c_all = float(np.average(cen, weights=w))
    mv = np.log2(c_end / max(c_start, 1))
    up, down = np.log2(c_peak / max(c_start, 1)), np.log2(c_peak / max(c_end, 1))
    if up > 0.25 and down > 0.25:
        shape = "arch"
    elif mv > 0.25:
        shape = "rising"
    elif mv < -0.25:
        shape = "falling"
    else:
        shape = "flat"
    bright = float(S[f >= 4000].sum() / (S.sum() + 1e-12))
    band = (f >= 300) & (f <= 12000)  # flatness in the swish band: noise ~0.2-0.5, tone < 0.05
    flat = float(np.median(np.exp(np.mean(np.log(S[band] + 1e-14), 0)) / (np.mean(S[band], 0) + 1e-14)))
    L, R = seg[a * h:(b + 1) * h, 0], seg[a * h:(b + 1) * h, 1]
    mid, side = (L + R) / 2, (L - R) / 2
    width_db = float(10 * np.log10((side ** 2).sum() / ((mid ** 2).sum() + 1e-12) + 1e-12))
    corr = float(np.corrcoef(L, R)[0, 1]) if L.std() > 0 and R.std() > 0 else 1.0
    # level: peak 100 ms loudness vs the voice's speech median within +-2 s
    Lf = loudness_track(x[max(0, s0 + i0 - int(0.05 * SR)): i0 + s1 + int(0.05 * SR)], 0.1, hop=0.01)
    j0, j1 = max(0, int((on_t - 2) / hop_v)), min(len(vM), int((end_t + 2) / hop_v))
    sp = speech[j0:j1]
    vref = float(np.median(vM[j0:j1][sp])) if sp.any() else float(np.median(vM[speech]))
    return {"t": round(on_t, 3), "peak_t": round(pk_t, 3), "dur_s": round(end_t - on_t, 3),
            "attack_s": round(pk_t - on_t, 3), "release_s": round(end_t - pk_t, 3),
            "level_vs_voice_lu": round(float(Lf.max()) - vref, 1),
            "centroid_hz": int(c_all), "centroid_start_hz": int(c_start), "centroid_peak_hz": int(c_peak),
            "centroid_end_hz": int(c_end), "pitch_move_oct": round(float(mv), 2), "pitch_shape": shape,
            "brightness_gt4k": round(bright, 3), "flatness": round(flat, 3),
            "width_side_minus_mid_db": round(width_db, 1), "lr_corr": round(corr, 2)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stem", required=True)
    ap.add_argument("--voice", required=True)
    ap.add_argument("--events", required=True)
    ap.add_argument("--key", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--frames")
    ap.add_argument("--cuts")
    ap.add_argument("--motion")
    ap.add_argument("--kinds", default="whoosh")
    ap.add_argument("--cues", default="whoosh,whoosh_long,swish")
    ap.add_argument("--offset", type=float, default=0.0, help="shift event times (s), e.g. a clip start")
    a = ap.parse_args()
    x = load(a.stem)
    v = load(a.voice)
    n = min(len(x), len(v))
    x, v = x[:n], v[:n]
    T = n / SR
    v50 = loudness_track(v, 0.05)
    speech = close_gaps((v50 > np.percentile(v50, 95) - 30) & (v50 > -60), 3)
    vM = loudness_track(v, 0.4)[: len(speech)]
    ev = json.load(open(a.events))
    if isinstance(ev, dict):  # story_sound.py output
        times = [(e["t"], e["kind"]) for e in ev["sfx"]["events"] if e["kind"] in a.kinds.split(",")]
    else:  # our cues.json / sfx_placed
        times = [(c["at"], c["cue"] + ":" + str(c.get("source", ""))) for c in ev if c["cue"] in a.cues.split(",")]
    times = [(t + a.offset, k) for t, k in times if 0 <= t + a.offset < T - 0.2]
    # visual events
    cuts, dissolves, whips, motion = [], [], [], []
    if a.frames:
        p, vid = a.frames.rsplit(":", 1)
        d = json.load(open(p))["videos"][vid]["measured_240p"]
        cuts = list(d["frame_metrics"]["cuts"])
        dissolves = [(x_["start"], x_["end"]) for x_ in d["frame_metrics"]["transitions"]]
        mv = d["camera"]["moves"]
        # a whip: a fast, short camera move (peak speed in the top quarter of this video's moves, FWHM <= 6 frames)
        thr = np.percentile([m_["peak"] for m_ in mv], 75) if mv else 1e9
        whips = [m_["t"] for m_ in mv if m_["peak"] >= thr and m_["fwhm"] <= 6]
    if a.cuts:
        cuts = [r["t0"] for r in json.load(open(a.cuts))][1:]
    if a.motion:
        motion = [s["t"] for s in json.load(open(a.motion))["spikes"]]
    out = []
    for t, kind in times:
        f = features(x, t, vM, speech)
        if f is None:
            continue
        f["src"] = kind
        if f["centroid_hz"] < 500:  # a low thump the detector filed as a whoosh, not a swish
            continue
        tt = f["t"]
        land = "nothing"
        if any(abs(c - tt) <= 0.25 for c in cuts):
            land = "cut"
        elif any(s0 - 0.25 <= tt <= s1 + 0.1 for s0, s1 in dissolves):
            land = "dissolve"
        elif any(abs(w - tt) <= 0.25 for w in whips):
            land = "camera_whip"
        elif any(abs(m_ - tt) <= 0.25 for m_ in motion):
            land = "motion"
        f["lands_on"] = land
        out.append(f)
    st = [o["t"] for o in out]
    near = lambda tt, w=0.3: any(abs(s - tt) <= w for s in st)
    unsw = {"cuts": len(cuts), "cuts_without_swish": sum(not near(c) for c in cuts),
            "dissolves": len(dissolves), "dissolves_without_swish": sum(not any(s0 - 0.25 <= s <= s1 + 0.1 for s in st)
                                                                       for s0, s1 in dissolves),
            "camera_whips": len(whips), "whips_without_swish": sum(not near(w) for w in whips),
            "motion_onsets": len(motion), "motion_onsets_without_swish": sum(not near(m_, 0.25) for m_ in motion)}

    def med(k):
        vals = [o[k] for o in out]
        return [round(float(np.percentile(vals, p)), 3) for p in (10, 50, 90)] if vals else None
    summ = {"n": len(out), "per_min": round(len(out) / (T / 60), 2),
            "interval_s_p50": round(float(np.median(np.diff(st))), 2) if len(st) > 2 else None}
    for k in ("level_vs_voice_lu", "dur_s", "attack_s", "release_s", "centroid_hz", "centroid_start_hz",
              "centroid_peak_hz", "centroid_end_hz", "pitch_move_oct", "brightness_gt4k", "flatness",
              "width_side_minus_mid_db", "lr_corr"):
        summ[k + "_p10_p50_p90"] = med(k)
    for k in ("pitch_shape", "lands_on"):
        c = {}
        for o in out:
            c[o[k]] = c.get(o[k], 0) + 1
        summ[k] = c
    res = {"key": a.key, "duration_s": round(T, 2), "summary": summ, "unswished": unsw, "swishes": out}
    json.dump(res, open(a.out, "w"), indent=1)
    print(a.key, json.dumps(summ))


if __name__ == "__main__":
    main()
