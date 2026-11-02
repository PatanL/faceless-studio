"""Measure how a video's music serves its narration and its setting changes (study only; nothing is reused).

Inputs are a voice stem and a music stem (Demucs for the references, our own stems for our videos), optional
Demucs drums/bass/other stems, word timings and the hand-made setting catalogue. Everything is measured against
the narration: speech mask from the voice stem, word starts from whisper/Kokoro, setting changes from the catalogue.

usage (Spark, music venv, CPU):
  OMP_NUM_THREADS=4 nice -n 10 ~/studio/venvs/music/bin/python research/music/tools/analyze.py \
      --stems work/kurz-music/PaErPyEnDvk --words work/kurz-music/PaErPyEnDvk/words.json \
      --settings research/frame-analysis/data/D_settings.csv --events research/frame-analysis/data/D_events.json \
      --exclude 26.4-36.4 --end 604 --key D --out research/music/data
  ... --voice voice.wav --music music.wav --words captions.json --settings-json timeline.json --key ORCA

Writes <out>/<key>_music.json (all numbers), <key>_timeline.csv (every detected event with context) and
<key>_music.png (loudness lanes + events, for a visual check).
"""
from __future__ import annotations

import argparse
import csv
import json
import os

import numpy as np
import soundfile as sf
from scipy.ndimage import maximum_filter1d, median_filter, uniform_filter1d
from scipy.signal import resample_poly

SR = 44100
HOP = 0.1  # s, loudness / event grid


# ----------------------------------------------------------------------------- io

def load(path, sr=SR):
    x, r = sf.read(path, dtype="float32", always_2d=True)
    if r != sr:
        from math import gcd
        g = gcd(sr, r)
        x = resample_poly(x, sr // g, r // g, axis=0).astype(np.float32)
    return x


def kweight(x, sr=SR):
    import pyloudnorm as pyln
    m = pyln.Meter(sr)
    y = x.astype(np.float64)
    for f in m._filters.values():
        y = f.apply_filter(y)
    return y


def loudness_track(x, win, sr=SR, hop=HOP):
    """BS.1770 loudness (LUFS, ungated) of `win`-second windows every `hop` s, centred; x (n, ch)."""
    y = kweight(x, sr)
    p = (y ** 2).sum(axis=1)  # channel sum (both weights 1)
    h = int(hop * sr)
    n = len(p) // h
    e = p[: n * h].reshape(n, h).mean(1)
    k = max(1, int(round(win / hop)))
    ms = uniform_filter1d(e, size=k, mode="nearest")
    return -0.691 + 10 * np.log10(ms + 1e-12)


def integrated(x, sr=SR):
    import pyloudnorm as pyln
    v = pyln.Meter(sr).integrated_loudness(x)
    return float(v) if np.isfinite(v) else -70.0


def read_words(path):
    if not path or not os.path.exists(path):
        return []
    d = json.load(open(path))
    ws = d.get("words", d)
    out = []
    for w in ws:
        t = w.get("w", w.get("text", ""))
        s = w.get("s", w.get("start"))
        e = w.get("e", w.get("end"))
        if s is not None:
            out.append({"w": str(t).strip(), "s": float(s), "e": float(e if e is not None else s)})
    return out


def read_settings(args):
    rows = []
    if args.settings:
        for r in csv.DictReader(open(args.settings)):
            rows.append({"t": float(r["start"]), "end": float(r["end"]), "setting": r.get("setting", ""),
                         "place": r.get("place", ""), "kind": r.get("kind", ""), "why": r.get("motivation", "")})
    elif args.settings_json:
        for r in json.load(open(args.settings_json)):
            rows.append({"t": float(r["t0"]), "end": float(r["t1"]), "setting": r.get("label", ""),
                         "place": r.get("place", ""), "kind": r.get("kind", ""), "why": r.get("why", "")})
    return rows


# ----------------------------------------------------------------------------- helpers

def runs(mask):
    """[(i0, i1)) runs of True"""
    m = np.concatenate([[False], mask, [False]]).astype(int)
    d = np.diff(m)
    return list(zip(np.nonzero(d == 1)[0], np.nonzero(d == -1)[0]))


def close_gaps(mask, k):
    out = mask.copy()
    idx = np.nonzero(mask)[0]
    for a, b in zip(idx[:-1], idx[1:]):
        if 1 < b - a <= k:
            out[a:b] = True
    return out


def nearest(t, arr):
    if len(arr) == 0:
        return None
    arr = np.asarray(arr)
    i = int(np.argmin(np.abs(arr - t)))
    return float(arr[i] - t)


def words_around(words, t, before=4, after=6):
    if not words:
        return ""
    starts = np.array([w["s"] for w in words])
    i = int(np.searchsorted(starts, t))
    pre = " ".join(w["w"] for w in words[max(0, i - before):i])
    post = " ".join(w["w"] for w in words[i:i + after])
    return f"{pre} | {post}"


def word_at(words, t, tol=0.2):
    best = None
    for w in words:
        d = w["s"] - t
        if abs(d) <= tol and (best is None or abs(d) < abs(best[1])):
            best = (w["w"], round(d, 3))
    return best


def align(changes, events, tol, T, excl, rng_seed=0, n_perm=2000):
    """share of `changes` with an event within tol s, plus a circular-shift null (events shifted together)"""
    changes, events = np.asarray(changes, float), np.asarray(events, float)
    if len(changes) == 0 or len(events) == 0:
        return {}

    def share(ev):
        return float(np.mean([np.min(np.abs(ev - c)) <= tol for c in changes]))

    obs = share(events)
    rng = np.random.default_rng(rng_seed)
    null = []
    for _ in range(n_perm):
        sh = (events + rng.uniform(10, T - 10)) % T
        null.append(share(sh))
    null = np.array(null)
    signed = [float(events[np.argmin(np.abs(events - c))] - c) for c in changes]
    matched = [s for s in signed if abs(s) <= tol]
    return {"tol_s": tol, "share": round(obs, 3), "null_mean": round(float(null.mean()), 3),
            "p_value": round(float((null >= obs).mean()), 4), "n_changes": int(len(changes)),
            "n_events": int(len(events)),
            "matched_offset_median_s": round(float(np.median(matched)), 2) if matched else None}


def krumhansl(chroma_mean):
    maj = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
    mnr = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
    names = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
    best = (-2, "")
    for k in range(12):
        for prof, mode in ((maj, "maj"), (mnr, "min")):
            r = np.corrcoef(chroma_mean, np.roll(prof, k))[0, 1]
            if r > best[0]:
                best = (r, f"{names[k]} {mode}")
    return best[1], round(float(best[0]), 2)


# ----------------------------------------------------------------------------- main analysis

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stems")
    ap.add_argument("--voice")
    ap.add_argument("--music")
    ap.add_argument("--words")
    ap.add_argument("--settings")
    ap.add_argument("--settings-json")
    ap.add_argument("--events")
    ap.add_argument("--exclude", default="", help="a-b,c-d seconds excluded (intro jingle, sponsor)")
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--end", type=float)
    ap.add_argument("--key", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    import librosa

    os.makedirs(a.out, exist_ok=True)
    st = a.stems
    voice = load(a.voice or os.path.join(st, "vocals.flac"))
    music = load(a.music or os.path.join(st, "music.flac"))
    n = min(len(voice), len(music))
    voice, music = voice[:n], music[:n]
    extra = {}
    if st:
        for k in ("drums", "bass", "other"):
            p = os.path.join(st, f"{k}.flac")
            if os.path.exists(p):
                extra[k] = load(p)[:n]
    T = n / SR
    end = min(a.end or T, T)
    excl = [tuple(map(float, r.split("-"))) for r in a.exclude.split(",") if r]
    words = read_words(a.words)
    sets = read_settings(a)
    t = (np.arange(int(T / HOP)) + 0.5) * HOP
    valid = (t >= a.start) & (t < end)
    for x0, x1 in excl:
        valid &= ~((t >= x0) & (t < x1))
    in_excl = lambda tt: any(x0 <= tt < x1 for x0, x1 in excl) or tt >= end or tt < a.start

    # ---- loudness lanes
    vM = loudness_track(voice, 0.4)[: len(t)]
    mM = loudness_track(music, 0.4)[: len(t)]
    mS = loudness_track(music, 3.0)[: len(t)]
    mF = loudness_track(music, 0.2)[: len(t)]  # fast lane for drop-outs and hits
    lanes = {"voice_M": vM, "music_M": mM}
    for k, x in extra.items():
        lanes[f"{k}_M"] = loudness_track(x, 0.4)[: len(t)]

    # ---- speech mask from the voice stem (50 ms frames -> HOP grid)
    v50 = loudness_track(voice, 0.05)[: len(t)]
    ref = np.percentile(v50[valid], 95)
    speech = (v50 > ref - 30) & (v50 > -60)
    speech = close_gaps(speech, int(0.3 / HOP))
    gaps = [(i0 * HOP, i1 * HOP) for i0, i1 in runs(~speech & valid) if (i1 - i0) * HOP >= 0.5]
    gap_mask = np.zeros(len(t), bool)
    for g0, g1 in gaps:
        gap_mask[int(g0 / HOP) + 2: int(g1 / HOP) - 1] = True  # away from the word edges
    sp = speech & valid
    gp = gap_mask & valid

    sel = lambda x: x[int(a.start * SR): int(end * SR)]
    loud = {
        "mix_integrated_lufs": round(integrated(sel(voice + music)), 1),
        "voice_integrated_lufs": round(integrated(sel(voice)), 1),
        "music_integrated_lufs": round(integrated(sel(music)), 1),
        "music_M_under_speech_median": round(float(np.median(mM[sp])), 1),
        "music_M_in_gaps_median": round(float(np.median(mM[gp])), 1) if gp.any() else None,
        "voice_M_speech_median": round(float(np.median(vM[sp])), 1),
        "voice_minus_music_under_speech_db": {
            "p10": round(float(np.percentile(vM[sp] - mM[sp], 10)), 1),
            "median": round(float(np.median(vM[sp] - mM[sp])), 1),
            "p90": round(float(np.percentile(vM[sp] - mM[sp], 90)), 1)},
        "speech_share": round(float(sp.sum() / valid.sum()), 3),
        "gaps_ge_0p5s": len(gaps),
        "gap_len_s": {"median": round(float(np.median([g1 - g0 for g0, g1 in gaps])), 2) if gaps else None,
                      "p90": round(float(np.percentile([g1 - g0 for g0, g1 in gaps], 90)), 2) if gaps else None},
        "music_LRA_like_p10_p95_short_term": [round(float(np.percentile(mS[valid], 10)), 1),
                                              round(float(np.percentile(mS[valid], 95)), 1)],
    }
    if gp.any():
        loud["music_gap_minus_speech_db"] = round(loud["music_M_in_gaps_median"] - loud["music_M_under_speech_median"], 1)
        # paired: each gap vs the 2 s of speech before it (local duck / swell behaviour)
        pairs = []
        for g0, g1 in gaps:
            i0, i1 = int(g0 / HOP) + 2, int(g1 / HOP) - 1
            j0 = max(0, int((g0 - 2.0) / HOP))
            pre = sp[j0:int(g0 / HOP)]
            if i1 > i0 and pre.any():
                pairs.append(float(np.median(mM[i0:i1]) - np.median(mM[j0:int(g0 / HOP)][pre])))
        if pairs:
            loud["gap_vs_preceding_speech_db"] = {"median": round(float(np.median(pairs)), 1),
                                                  "p25": round(float(np.percentile(pairs, 25)), 1),
                                                  "p75": round(float(np.percentile(pairs, 75)), 1), "n": len(pairs)}

    # ---- features on a 0.5 s grid for section / texture novelty
    y = music.mean(1)
    y22 = resample_poly(y, 1, 2).astype(np.float32)
    sr22 = SR // 2
    hop = 512
    S = np.abs(librosa.stft(y22, n_fft=2048, hop_length=hop)) ** 2
    freqs = librosa.fft_frequencies(sr=sr22, n_fft=2048)
    bands = {"sub_20_60": (20, 60), "bass_60_200": (60, 200), "lowmid_200_800": (200, 800),
             "mid_800_2500": (800, 2500), "pres_2500_6000": (2500, 6000), "air_6000_11000": (6000, 11000)}
    B = np.stack([S[(freqs >= lo) & (freqs < hi)].sum(0) for lo, hi in bands.values()])
    aw = librosa.db_to_power(librosa.A_weighting(np.maximum(freqs, 10)))[:, None]
    BA = np.stack([(S * aw)[(freqs >= lo) & (freqs < hi)].sum(0) for lo, hi in bands.values()])
    H, P = librosa.decompose.hpss(S, margin=2.0)
    # register: harmonic-only CQT energy per octave C1..C8 (what octaves the pitched parts live in)
    yh = librosa.istft(np.sqrt(H) * np.exp(1j * np.angle(librosa.stft(y22, n_fft=2048, hop_length=hop))), hop_length=hop,
                       length=len(y22))
    C = np.abs(librosa.cqt(yh, sr=sr22, hop_length=hop, fmin=librosa.note_to_hz("C1"), n_bins=84, bins_per_octave=12)) ** 2
    C = C[:, : S.shape[1]]
    octs = ["C1-B1 sub", "C2-B2 bass", "C3-B3 low", "C4-B4 mid", "C5-B5 high", "C6-B6 bell", "C7-B7 sparkle"]
    chroma = librosa.feature.chroma_stft(S=H, sr=sr22, n_fft=2048, hop_length=hop)
    mel = librosa.feature.melspectrogram(S=S, sr=sr22, n_mels=64)
    mfcc = librosa.feature.mfcc(S=librosa.power_to_db(mel), n_mfcc=14)[1:]
    cent = librosa.feature.spectral_centroid(S=np.sqrt(S), sr=sr22)[0]
    flat = librosa.feature.spectral_flatness(S=np.sqrt(S))[0]
    onset_env = librosa.onset.onset_strength(S=librosa.power_to_db(mel), sr=sr22, hop_length=hop)
    melH = librosa.feature.melspectrogram(S=H, sr=sr22, n_mels=64, fmin=1200, fmax=9000)
    onset_hi = librosa.onset.onset_strength(S=librosa.power_to_db(melH), sr=sr22, hop_length=hop)
    fr_t = librosa.frames_to_time(np.arange(S.shape[1]), sr=sr22, hop_length=hop)
    G = 0.5
    ng = int(T / G)
    gi = np.minimum((fr_t / G).astype(int), ng - 1)

    def agg(F):
        F = np.atleast_2d(F)
        out = np.zeros((F.shape[0], ng))
        cnt = np.bincount(gi, minlength=ng) + 1e-9
        for r in range(F.shape[0]):
            out[r] = np.bincount(gi, weights=F[r], minlength=ng) / cnt
        return out

    logB = np.log10(agg(B) + 1e-10)
    feats = np.vstack([agg(chroma) * 2.0, agg(mfcc) / 10.0, logB, np.log10(agg(onset_env) + 1e-3)])
    tg = (np.arange(ng) + 0.5) * G
    gvalid = np.array([not in_excl(x) for x in tg])
    Z = (feats - feats[:, gvalid].mean(1, keepdims=True)) / (feats[:, gvalid].std(1, keepdims=True) + 1e-9)
    Z = uniform_filter1d(Z, size=3, axis=1)
    Zn = Z / (np.linalg.norm(Z, axis=0, keepdims=True) + 1e-9)
    SSM = Zn.T @ Zn

    def novelty(half):
        k = int(half / G)
        ii = np.arange(-k, k)
        g = np.exp(-0.5 * ((ii + 0.5) / (0.5 * k)) ** 2)
        ker = np.outer(g, g) * np.outer(np.sign(ii + 0.5), np.sign(ii + 0.5))
        nov = np.zeros(ng)
        for c in range(k, ng - k):
            nov[c] = np.sum(SSM[c - k:c + k, c - k:c + k] * ker)
        nov[~gvalid] = 0
        return nov

    def peaks(nov, mindist, z=1.0):
        thr = np.median(nov[gvalid]) + z * np.std(nov[gvalid])
        mx = maximum_filter1d(nov, size=int(2 * mindist / G) + 1)
        idx = np.nonzero((nov == mx) & (nov > thr) & gvalid)[0]
        return [float(tg[i]) for i in idx]

    nov_coarse = novelty(6.0)
    nov_fine = novelty(2.5)
    bounds_coarse = peaks(nov_coarse, 6.0, 0.8)
    bounds_fine = peaks(nov_fine, 2.5, 0.8)

    # ---- tempo and pulse
    tempo_all = float(np.atleast_1d(librosa.feature.tempo(onset_envelope=onset_env, sr=sr22, hop_length=hop))[0])
    win, step = 15.0, 5.0
    tempi = []
    fps = sr22 / hop
    for w0 in np.arange(a.start, end - win, step):
        if any(x0 < w0 + win and w0 < x1 for x0, x1 in excl):
            continue
        i0, i1 = int(w0 * fps), int((w0 + win) * fps)
        oe = onset_env[i0:i1]
        if oe.std() < 1e-6:
            continue
        oe = (oe - oe.mean()) / oe.std()
        ac = np.correlate(oe, oe, "full")[len(oe) - 1:] / len(oe)
        lags = np.arange(len(ac)) / fps
        rng_ = (lags >= 0.25) & (lags <= 1.5)
        j = np.argmax(ac[rng_])
        lag = lags[rng_][j]
        bpm = 60 / lag
        while bpm < 70:
            bpm *= 2
        while bpm > 160:
            bpm /= 2
        tempi.append({"t": round(float(w0), 1), "bpm": round(float(bpm), 1), "clarity": round(float(ac[rng_][j]), 2)})
    clar = np.array([x["clarity"] for x in tempi]) if tempi else np.array([0])
    bpms = np.array([x["bpm"] for x in tempi]) if tempi else np.array([0])
    tempo = {"global_bpm_librosa": round(tempo_all, 1),
             "window_bpm_median": round(float(np.median(bpms[clar > 0.25])) if (clar > 0.25).any() else float("nan"), 1),
             "window_bpm_p25_p75": [round(float(np.percentile(bpms, 25)), 1), round(float(np.percentile(bpms, 75)), 1)],
             "pulse_clarity_median": round(float(np.median(clar)), 2),
             "share_windows_clear_pulse_gt_0p3": round(float((clar > 0.3).mean()), 2),
             "windows": tempi}

    # ---- sections (between coarse boundaries) with instrumentation by spectrum
    edges = [a.start] + [b for b in bounds_coarse] + [end]
    sections = []
    hi_peaks = librosa.util.peak_pick(onset_hi, pre_max=3, post_max=3, pre_avg=10, post_avg=10,
                                      delta=np.std(onset_hi) * 1.5, wait=4)
    hi_t = fr_t[hi_peaks]
    all_peaks = librosa.util.peak_pick(onset_env, pre_max=3, post_max=3, pre_avg=10, post_avg=10,
                                       delta=np.std(onset_env) * 1.5, wait=4)
    on_t = fr_t[all_peaks]
    for s0, s1 in zip(edges[:-1], edges[1:]):
        if s1 - s0 < 2.0:
            continue
        m = (fr_t >= s0) & (fr_t < s1) & np.array([not in_excl(x) for x in fr_t])
        if m.sum() < 20:
            continue
        band_e = BA[:, m].sum(1)
        band_db = 10 * np.log10(band_e / band_e.sum() + 1e-12)
        oc = C[:, m[: C.shape[1]]].reshape(7, 12, -1).sum(axis=(1, 2))
        oct_db = 10 * np.log10(oc / oc.max() + 1e-12)
        # hi-band note rate with a fixed (global) threshold and its interval in beats of the window's tempo
        hm = (hi_t >= s0) & (hi_t < s1)
        ioi = np.diff(hi_t[hm])
        ioi_med = float(np.median(ioi)) if len(ioi) > 3 else None
        harm = H[:, m].sum() / (H[:, m].sum() + P[:, m].sum())
        ch = chroma[:, m].mean(1)
        key, kr = krumhansl(ch)
        ti = (t >= s0) & (t < s1) & valid
        sec = {"t0": round(s0, 1), "t1": round(s1, 1), "dur": round(s1 - s0, 1),
               "music_M_median": round(float(np.median(mM[ti])), 1),
               "band_dBA_rel_total": {k: round(float(v), 1) for k, v in zip(bands, band_db)},
               "octave_db_rel_max": {k: round(float(v), 1) for k, v in zip(octs, oct_db)},
               "hi_note_ioi_median_s": round(ioi_med, 3) if ioi_med else None,
               "harmonic_share": round(float(harm), 2), "centroid_hz": int(np.median(cent[m])),
               "flatness_median": round(float(np.median(flat[m])), 3),
               "onsets_per_s": round(float(((on_t >= s0) & (on_t < s1)).sum() / (s1 - s0)), 2),
               "hi_tonal_onsets_per_s": round(float(((hi_t >= s0) & (hi_t < s1)).sum() / (s1 - s0)), 2),
               "key": key, "key_r": kr}
        for k in ("drums", "bass", "other"):
            if f"{k}_M" in lanes:
                sec[f"{k}_minus_music_db"] = round(float(np.median(lanes[f"{k}_M"][ti] - mM[ti])), 1)
        sections.append(sec)

    # ---- risers / swells (3 s short-term loudness smoothed; >= 5 dB rise in <= 8 s ending at a local peak)
    Ls = uniform_filter1d(median_filter(loudness_track(music, 1.0)[: len(t)], size=5), size=5)
    risers = []
    rmed = median_filter(Ls, size=int(10 / HOP))
    pk = np.nonzero((Ls == maximum_filter1d(Ls, size=int(4 / HOP))) & valid)[0]
    for i in pk:
        j0 = max(0, i - int(8 / HOP))
        jmin = j0 + int(np.argmin(Ls[j0:i + 1]))
        rise = Ls[i] - Ls[jmin]
        dur = (i - jmin) * HOP
        if rise >= 6.0 and dur >= 1.5 and Ls[i] >= rmed[i] + 2.0 and not in_excl(t[jmin]):
            seg = Ls[jmin:i + 1]
            mono = float(np.mean(np.diff(seg) >= -0.02))
            if mono < 0.8:
                continue
            tp = float(t[i])
            # centroid rising? (filter-sweep risers)
            c0 = np.median(cent[(fr_t >= t[jmin]) & (fr_t < t[jmin] + 0.5)]) if True else 0
            c1 = np.median(cent[(fr_t >= tp - 0.5) & (fr_t < tp)])
            risers.append({"t_start": round(float(t[jmin]), 1), "t_peak": round(tp, 1), "rise_db": round(float(rise), 1),
                           "dur_s": round(dur, 1), "centroid_ratio": round(float(c1 / max(c0, 1)), 2),
                           "to_setting_change_s": nearest(tp, [s["t"] for s in sets]),
                           "peak_in_speech": bool(speech[i]), "peak_in_gap": bool(gap_mask[max(0, i - 3):i + 4].any()),
                           "words": words_around(words, tp)})

    # ---- hits / stings: fast lane (200 ms) jumps >= 8 dB over the previous 0.6 s median, near the music's top level
    hits = []
    top = np.percentile(mM[valid], 90)
    for i in range(int(0.6 / HOP), len(t) - 1):
        if not valid[i]:
            continue
        prev = np.median(mF[i - int(0.6 / HOP):i])
        if mF[i] - prev >= 8.0 and mF[i] >= top - 8 and mF[i] >= mF[i - 1] + 3:
            if hits and t[i] - hits[-1]["t"] < 1.0:
                continue
            tt = float(t[i])
            band = "low" if np.mean(B[0:2, (fr_t >= tt - 0.1) & (fr_t < tt + 0.2)]) > np.mean(B[3:6, (fr_t >= tt - 0.1) & (fr_t < tt + 0.2)]) else "high"
            fl = float(np.median(flat[(fr_t >= tt - 0.05) & (fr_t < tt + 0.2)]))
            hits.append({"t": round(tt, 2), "jump_db": round(float(mF[i] - prev), 1), "band": band,
                         "flatness": round(fl, 3), "in_speech": bool(speech[i]),
                         "word": word_at(words, tt, 0.25), "to_setting_change_s": nearest(tt, [s["t"] for s in sets]),
                         "words": words_around(words, tt)})

    # ---- drop-outs: fast lane <= running 10 s median - 12 dB (or < -55 LUFS) for >= 0.3 s
    run_med = median_filter(mM, size=int(10 / HOP))
    low = ((mF <= run_med - 12) | (mF < -55)) & valid
    drops = []
    for i0, i1 in runs(low):
        d = (i1 - i0) * HOP
        if d < 0.3:
            continue
        t0, t1 = float(i0 * HOP), float(i1 * HOP)
        after = [h for h in hits if t1 - 0.3 <= h["t"] <= t1 + 1.5]
        drops.append({"t0": round(t0, 1), "t1": round(t1, 1), "dur": round(d, 1),
                      "depth_db": round(float(np.median(run_med[i0:i1] - mF[i0:i1])), 1),
                      "speech_during_share": round(float(speech[i0:i1].mean()), 2),
                      "hit_after": bool(after), "to_setting_change_s": nearest(t1, [s["t"] for s in sets]),
                      "words_at_end": words_around(words, t1, 6, 8)})

    # ---- noise-like transients (whooshes / swishes) vs visual transitions
    sfx = []
    fl_g = agg(flat)[0]
    e_g = 10 * np.log10(agg(S[(freqs > 1000)].sum(0)) + 1e-12)[0]
    for i in range(2, ng - 1):
        if gvalid[i] and fl_g[i] > np.percentile(fl_g[gvalid], 93) and e_g[i] > np.median(e_g[gvalid]) + 3 \
                and fl_g[i] >= fl_g[i - 1] and fl_g[i] >= fl_g[i + 1]:
            sfx.append(float(tg[i]))
    trans = []
    if a.events and os.path.exists(a.events):
        ev = json.load(open(a.events))
        trans = [x["start"] for x in ev.get("transitions", []) if not in_excl(x["start"])]

    # ---- alignment of music events with setting changes (and visual transitions)
    changes = [s["t"] for s in sets if s["t"] > a.start + 1 and not in_excl(s["t"])]
    T_eff = end
    al = {
        "coarse_boundaries_vs_setting_changes": align(changes, bounds_coarse, 1.5, T_eff, excl),
        "fine_boundaries_vs_setting_changes": align(changes, bounds_fine, 1.0, T_eff, excl),
        "setting_changes_vs_coarse_boundaries(precision)": align(bounds_coarse, changes, 1.5, T_eff, excl),
        "hits_vs_setting_changes": align(changes, [h["t"] for h in hits], 0.6, T_eff, excl),
        "riser_peaks_vs_setting_changes": align(changes, [r["t_peak"] for r in risers], 1.0, T_eff, excl),
        "dropout_ends_vs_setting_changes": align(changes, [d["t1"] for d in drops], 1.0, T_eff, excl),
        "noise_transients_vs_visual_transitions": align(trans, sfx, 0.5, T_eff, excl) if trans else {},
        "noise_transients_vs_setting_changes": align(changes, sfx, 0.6, T_eff, excl),
    }
    # sentence starts (word after . ? !) and sentence ends: are hits / riser peaks / drop-outs phrased to the narration?
    sent_starts = [w["s"] for prev, w in zip(words[:-1], words[1:]) if prev["w"].rstrip('"\'').endswith((".", "?", "!"))
                   and not in_excl(w["s"])]
    sent_ends = [prev["e"] for prev, w in zip(words[:-1], words[1:]) if prev["w"].rstrip('"\'').endswith((".", "?", "!"))
                 and not in_excl(prev["e"])]
    if sent_starts:
        al["hits_near_sentence_starts(-0.4..+0.3)"] = align([h["t"] + 0.05 for h in hits], sent_starts, 0.35, T_eff, excl)
        al["riser_peaks_near_sentence_starts"] = align([r["t_peak"] for r in risers], sent_starts, 0.5, T_eff, excl)
        al["dropout_ends_near_sentence_starts"] = align([d["t1"] for d in drops], sent_starts, 0.5, T_eff, excl)
        al["dropout_starts_near_sentence_ends"] = align([d["t0"] for d in drops], sent_ends, 0.5, T_eff, excl)
        al["setting_changes_near_sentence_starts"] = align(changes, sent_starts, 0.5, T_eff, excl)
    # music level step at setting changes (3 s after vs 3 s before, short-term) and spectral jump (feature distance)
    steps = []
    for c in changes:
        i = int(c / HOP)
        b0, b1 = max(0, i - 30), min(len(t), i + 30)
        if b1 - i < 10 or i - b0 < 10:
            continue
        gi0, gi1 = int(c / G), min(ng - 1, int(c / G) + 6)
        dist = 1 - float(Zn[:, max(0, gi0 - 6):gi0].mean(1) @ Zn[:, gi0:gi1].mean(1) /
                         (np.linalg.norm(Zn[:, max(0, gi0 - 6):gi0].mean(1)) * np.linalg.norm(Zn[:, gi0:gi1].mean(1)) + 1e-9))
        steps.append({"t": c, "level_step_db": round(float(np.median(mM[i:b1]) - np.median(mM[b0:i])), 1),
                      "texture_dist": round(dist, 3)})
    # baseline texture distance at random non-change times
    rng = np.random.default_rng(1)
    base = []
    for _ in range(400):
        c = rng.uniform(a.start + 4, end - 4)
        if in_excl(c) or (changes and min(abs(np.array(changes) - c)) < 3):
            continue
        gi0, gi1 = int(c / G), min(ng - 1, int(c / G) + 6)
        u, v = Zn[:, max(0, gi0 - 6):gi0].mean(1), Zn[:, gi0:gi1].mean(1)
        base.append(1 - float(u @ v / (np.linalg.norm(u) * np.linalg.norm(v) + 1e-9)))

    # ---- starts and ends
    first_music = next((float(t[i]) for i in range(len(t)) if mM[i] > -45), None)
    first_voice = next((float(t[i]) for i in range(len(t)) if speech[i]), None)
    endi = int(end / HOP) - 1
    tail = mS[max(0, endi - 300):endi + 1]
    ends = {"first_music_above_-45_lufs_s": first_music, "first_speech_s": first_voice,
            "music_M_first_5s": [round(float(x), 1) for x in mM[: int(5 / HOP): 5]],
            "music_S_last_30s_every_2s": [round(float(x), 1) for x in tail[::20]],
            "last_speech_s": float(t[np.nonzero(speech & (t < end))[0][-1]]) if (speech & (t < end)).any() else None}

    res = {"key": a.key, "duration_s": round(T, 1), "analysed": [a.start, end], "excluded": excl,
           "loudness": loud, "tempo": {k: v for k, v in tempo.items() if k != "windows"},
           "n_setting_changes": len(changes),
           "boundaries": {"coarse_per_min": round(len(bounds_coarse) / ((valid.sum() * HOP) / 60), 2),
                          "fine_per_min": round(len(bounds_fine) / ((valid.sum() * HOP) / 60), 2),
                          "coarse": bounds_coarse, "fine": bounds_fine},
           "alignment": al,
           "setting_change_steps": {
               "level_step_abs_median_db": round(float(np.median([abs(s["level_step_db"]) for s in steps])), 1) if steps else None,
               "texture_dist_median_at_changes": round(float(np.median([s["texture_dist"] for s in steps])), 3) if steps else None,
               "texture_dist_median_random": round(float(np.median(base)), 3) if base else None,
               "steps": steps},
           "sections": sections, "risers": risers, "hits": hits, "dropouts": drops,
           "noise_transients_per_min": round(len(sfx) / ((valid.sum() * HOP) / 60), 2),
           "starts_ends": ends, "tempo_windows": tempo["windows"]}
    json.dump(res, open(os.path.join(a.out, f"{a.key}_music.json"), "w"), indent=1)

    with open(os.path.join(a.out, f"{a.key}_timeline.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["t", "type", "detail", "words (before | after)"])
        rows = [(s["t"], "setting", f"{s['setting']} / {s['place']} ({s['kind']}): {s['why']}", words_around(words, s["t"]))
                for s in sets]
        rows += [(b, "music_boundary", "coarse", words_around(words, b)) for b in bounds_coarse]
        rows += [(r["t_peak"], "riser_peak", f"+{r['rise_db']} dB over {r['dur_s']} s", r["words"]) for r in risers]
        rows += [(h["t"], "hit", f"+{h['jump_db']} dB {h['band']} flat={h['flatness']} word={h['word']}", h["words"]) for h in hits]
        rows += [(d["t0"], "dropout", f"{d['dur']} s, -{d['depth_db']} dB, speech {d['speech_during_share']}", d["words_at_end"]) for d in drops]
        for r in sorted(rows, key=lambda r: r[0]):
            w.writerow([round(r[0], 2), *r[1:]])

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        mins = max(1, int(np.ceil(end / 120)))
        fig, axs = plt.subplots(mins, 1, figsize=(22, 3.2 * mins), squeeze=False)
        for k in range(mins):
            ax = axs[k, 0]
            lo, hi = k * 120, min(end, (k + 1) * 120)
            m_ = (t >= lo) & (t < hi)
            ax.plot(t[m_], vM[m_], color="#58a6ff", lw=0.6, label="voice M")
            ax.plot(t[m_], mM[m_], color="#f0883e", lw=0.8, label="music M")
            if "drums_M" in lanes:
                ax.plot(t[m_], lanes["drums_M"][m_], color="#8b949e", lw=0.5, label="drums M")
            for s in sets:
                if lo <= s["t"] < hi:
                    ax.axvline(s["t"], color="#2ea043", lw=1.2)
            for b in bounds_coarse:
                if lo <= b < hi:
                    ax.axvline(b, color="#a371f7", lw=1.0, ls="--")
            for r in risers:
                if lo <= r["t_peak"] < hi:
                    ax.annotate("", xy=(r["t_peak"], -18), xytext=(r["t_start"], -18),
                                arrowprops=dict(arrowstyle="->", color="#d29922"))
            for h in hits:
                if lo <= h["t"] < hi:
                    ax.plot([h["t"]], [-15], "v", color="#f85149")
            for d in drops:
                if lo <= d["t0"] < hi:
                    ax.axvspan(d["t0"], d["t1"], color="#f85149", alpha=0.25)
            for x0, x1 in excl:
                ax.axvspan(max(lo, x0), min(hi, x1), color="#444", alpha=0.3)
            ax.set_xlim(lo, lo + 120)
            ax.set_ylim(-70, -10)
            ax.set_xticks(np.arange(lo, lo + 121, 5))
            ax.grid(alpha=0.2)
            if k == 0:
                ax.legend(loc="lower left", fontsize=7)
                ax.set_title(f"{a.key}: green = setting change, purple dashed = music section boundary, "
                             f"orange arrow = riser, red v = hit, red band = drop-out")
        fig.tight_layout()
        fig.savefig(os.path.join(a.out, f"{a.key}_music.png"), dpi=70)
    except ImportError:
        pass
    print(json.dumps({k: res[k] for k in ("loudness", "tempo", "boundaries", "alignment")}, indent=1)[:6000])
    print("sections", len(sections), "risers", len(risers), "hits", len(hits), "drops", len(drops))


if __name__ == "__main__":
    main()
