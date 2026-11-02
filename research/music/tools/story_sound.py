"""Story-lane sound measures (voice, music bed, SFX, room tone) of one video from its Demucs stems. Study only.

Complements analyze.py (music sections, tempo, risers, hits, drop-outs). Everything is measured from the stems and
the narration; nothing is reused.

  loudness   mix integrated LUFS, LRA and true peak (ffmpeg ebur128), voice / non-voice / music-bed integrated
  gap        voice minus non-voice and voice minus music bed (SFX frames removed), momentary 0.4 s, under speech
  bed        music-bed lane (non-voice stem with SFX events masked): entry, level steps, drop-outs, behaviour at the
             "You see" turn and at the end
  sfx        events in the non-voice stem that stand out of its own rolling median spectrum (>= 6 dB over >= 25 % of
             64 mel bands, >= 35 ms): count/min, kind by shape (impact, whoosh, riser, pop/click, tonal hit, foley),
             sync to visual transitions / cuts / camera moves (circular-shift null), level vs the voice
  ambience   1 s windows of the non-voice stem that are noise-like (flatness, low harmonic share) without a pulse
  room tone  the mix and the vocals stem in speech gaps (>= 120 ms) relative to speech; digital-silence share
  voice      f0 (pYIN) median / p5-p95 range in semitones, loudness spread (momentary p10-p90), crest factor, pace
             (words/s in 3 s windows, CV), breaths per minute, spectral balance (low cut, presence, brightness)

usage (Mac sound venv): python -I story_sound.py --stems DIR --key K --out out.json
       [--words words.json] [--frames ricks24_metrics.json:VIDEO_ID | --cuts cuts.json] [--you-see 7.2,...]
       [--voice voice.wav --music music.wav --sfx sfx.wav]   # our own true stems instead of Demucs
"""
import argparse
import json
import os
import re
import subprocess
import sys

import numpy as np
import soundfile as sf
from scipy.ndimage import median_filter, uniform_filter1d
from scipy.signal import resample_poly

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze import align, close_gaps, loudness_track, runs  # noqa: E402

SR = 44100
HOP = 0.1


def load(p, sr=SR):
    x, r = sf.read(p, dtype="float32", always_2d=True)
    if r != sr:
        from math import gcd
        g = gcd(sr, r)
        x = resample_poly(x, sr // g, r // g, axis=0).astype(np.float32)
    if x.shape[1] == 1:
        x = np.repeat(x, 2, axis=1)
    return x


def smask(mask, n, hop=HOP):
    """frame mask on a hop grid -> sample mask of length n (padded with False)"""
    m = np.repeat(mask, int(round(hop * SR)))[:n]
    return np.pad(m, (0, n - len(m)))


def integ(x):
    import pyloudnorm as pyln
    v = pyln.Meter(SR).integrated_loudness(x.astype(np.float64))
    return round(float(v), 1) if np.isfinite(v) else -70.0


def ffmpeg_loud(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    tail = r.stderr[r.stderr.rfind("Summary:"):]
    get = lambda k: float(re.search(rf"{k}:\s+(-?[\d.]+|-inf)", tail).group(1).replace("-inf", "-120"))
    return {"I_lufs": get("I"), "LRA_lu": get("LRA"), "true_peak_dbtp": get("Peak")}


def q(a, ps=(10, 50, 90), nd=1):
    a = np.asarray(a, float)
    a = a[np.isfinite(a)]
    if len(a) == 0:
        return None
    return [round(float(np.percentile(a, p)), nd) for p in ps]


def read_words(p):
    if not p or not os.path.exists(p):
        return []
    d = json.load(open(p))
    ws = d.get("words", d)
    out = []
    for w in ws:
        s = w.get("start", w.get("s"))
        if s is None:
            continue
        out.append({"w": str(w.get("text", w.get("w", ""))), "s": float(s), "e": w.get("end", w.get("e"))})
    return out


# ----------------------------------------------------------------------------- SFX events

def mel_db(x):
    import librosa
    y = resample_poly(x.mean(1), 1, 2).astype(np.float32)
    S = np.abs(librosa.stft(y, n_fft=1024, hop_length=256)) ** 2
    mel = librosa.feature.melspectrogram(S=S, sr=SR // 2, n_mels=64, fmin=40, fmax=11000)
    return S, 10 * np.log10(mel + 1e-10)


def sfx_events(det, speech, abs_floor_db):
    """Events of the detection stem (Demucs drums: whooshes, impacts, foley; or our true SFX stem) that rise out of its
    own rolling median spectrum by >= 6 dB over >= 25 % of the audible mel bands for >= 35 ms. A band is audible when it
    is within 50 dB of the voice's loudest bands (abs_floor_db), so bleed and noise floor never count."""
    import librosa
    sr, hop = SR // 2, 256
    S, X = mel_db(det)
    fps = sr / hop
    bed = median_filter(X, size=(1, int(2.5 * fps)), mode="nearest")
    ex = np.clip(X - bed, 0, None)
    live = X > abs_floor_db
    frac = ((ex >= 6) & live).mean(0)
    lowb = freqs_m = None
    import librosa as _l
    freqs_m = _l.mel_frequencies(n_mels=64, fmin=40, fmax=11000)
    lowb = freqs_m < 300
    # low thumps (impacts, booms) only light the low bands: >= 8 dB over >= 50 % of the audible bands under 300 Hz
    low_on = (((ex[lowb] >= 8) & live[lowb]).mean(0) >= 0.5)
    on = close_gaps((uniform_filter1d(frac, 3) >= 0.25) | low_on, 3)
    ft = librosa.frames_to_time(np.arange(X.shape[1]), sr=sr, hop_length=hop)
    freqs = librosa.mel_frequencies(n_mels=64, fmin=40, fmax=11000)
    flat_all = librosa.feature.spectral_flatness(S=np.sqrt(S))[0]
    H, P = librosa.decompose.hpss(S, margin=1.0)
    hshare = H.sum(0) / (H.sum(0) + P.sum(0) + 1e-12)
    evs = []
    mask = np.zeros(len(ft), bool)
    for i0, i1 in runs(on):
        if (i1 - i0) / fps < 0.035:
            continue
        # extend over the decay while the excess stays >= 3 dB over 15 % of the audible bands (<= 2.5 s more)
        j = i1
        while j < len(ft) - 1 and ((ex[:, j] >= 3) & live[:, j]).mean() >= 0.15 and (j - i1) / fps < 2.5:
            j += 1
        i1 = j
        if evs and ft[i0] - (evs[-1]["t"] + evs[-1]["dur"]) < 0.08:  # a re-trigger inside the previous event's tail
            mask[i0:i1] = True
            continue
        dur = (i1 - i0) / fps
        seg = ex[:, i0:i1]
        e_lin = (10 ** (X[:, i0:i1] / 10)).sum(0)
        pk = int(np.argmax(e_lin))
        attack = pk / fps
        spec = (10 ** (seg / 10) - 1).clip(0).mean(1) + 1e-12
        cent = float((freqs * spec).sum() / spec.sum())
        low_share = float(spec[freqs < 200].sum() / spec.sum())
        flat = float(np.median(flat_all[i0:i1]))
        hs = float(np.median(hshare[i0:i1]))

        def cen(a, b):
            s_ = (10 ** (X[:, a:b] / 10)).mean(1)
            return float((freqs * s_).sum() / (s_.sum() + 1e-12))
        n3 = max(1, (i1 - i0) // 3)
        sweep = cen(i1 - n3, i1) / max(cen(i0, i0 + n3), 1.0)
        rise = float(10 * np.log10(e_lin[pk] / (e_lin[0] + 1e-12)))
        n_trans = int((np.diff((frac[i0:i1] >= 0.25).astype(int)) == 1).sum() + 1)
        if dur >= 1.0 and pk >= 0.6 * (i1 - i0) and rise >= 6:
            kind = "riser"
        elif dur < 0.15:  # short: a click/pop (instant attack, or a blip), a swish (noise swelling in), or a thud
            kind = "impact" if cent < 600 else ("pop_click" if dur < 0.08 or attack < 0.02 else "whoosh")
        elif attack <= 0.035 and dur >= 0.25 and n_trans <= 2:
            kind = "impact"          # a hit with a decay (low boom, tonal stinger or thud)
        elif hs >= 0.7:
            kind = "tonal"           # ding / chime / musical blip without a sharp hit
        elif attack >= 0.03 and cent >= 600 and n_trans <= 2:
            kind = "whoosh"
        else:
            kind = "foley"           # several transients or a short irregular texture (steps, creak, cloth, paper)
        t0 = float(ft[i0])
        k = min(len(speech) - 1, int(t0 / HOP))
        evs.append({"t": round(t0, 3), "dur": round(dur, 3), "kind": kind, "attack_s": round(attack, 3),
                    "centroid_hz": int(cent), "low_share": round(low_share, 2), "flatness": round(flat, 3),
                    "harmonic_share": round(hs, 2), "sweep": round(sweep, 2), "rise_db": round(rise, 1),
                    "n_transients": n_trans, "in_speech": bool(speech[k])})
        mask[i0:i1] = True
    return evs, mask, ft


def event_levels(evs, nv, voice_speech_M):
    """peak 100 ms loudness of the non-voice stem in each event, relative to the voice's speech median (momentary)"""
    L = loudness_track(nv, 0.1, hop=0.02)
    for e in evs:
        i0, i1 = int(e["t"] / 0.02), int((e["t"] + max(e["dur"], 0.1)) / 0.02) + 1
        e["level_vs_voice_lu"] = round(float(L[i0:i1].max() - voice_speech_M), 1) if i1 > i0 else None
    return evs


# ----------------------------------------------------------------------------- voice

def voice_measures(v, speech, words, T):
    import librosa
    y = resample_poly(v.mean(1), 1, 2).astype(np.float32)
    sr = SR // 2
    f0, vflag, _ = librosa.pyin(y, fmin=60, fmax=400, sr=sr, frame_length=2048, hop_length=256)
    f = f0[vflag & np.isfinite(f0)]
    out = {}
    if len(f) > 50:
        st = 12 * np.log2(f / np.median(f))
        out["f0_median_hz"] = round(float(np.median(f)), 1)
        out["f0_p5_p95_hz"] = [round(float(np.percentile(f, 5)), 1), round(float(np.percentile(f, 95)), 1)]
        out["f0_range_p5_p95_st"] = round(float(np.percentile(st, 95) - np.percentile(st, 5)), 1)
        out["f0_std_st"] = round(float(np.std(st)), 2)
        # phrase-level pitch movement: median f0 per 1 s voiced window, spread across windows
        ft = librosa.frames_to_time(np.arange(len(f0)), sr=sr, hop_length=256)
        meds = []
        for w0 in np.arange(0, T - 1, 1.0):
            m = (ft >= w0) & (ft < w0 + 1) & vflag & np.isfinite(f0)
            if m.sum() > 20:
                meds.append(12 * np.log2(np.median(f0[m]) / np.median(f)))
        out["f0_1s_median_spread_st_p10_p90"] = round(float(np.percentile(meds, 90) - np.percentile(meds, 10)), 1) if meds else None
    vM = loudness_track(v, 0.4)[: len(speech)]
    out["voice_M_speech_p10_p50_p90"] = q(vM[speech])
    out["voice_M_spread_p10_p90_lu"] = round(float(np.percentile(vM[speech], 90) - np.percentile(vM[speech], 10)), 1)
    vS = loudness_track(v, 3.0)[: len(speech)]
    out["voice_S_spread_p10_p95_lu"] = round(float(np.percentile(vS[speech], 95) - np.percentile(vS[speech], 10)), 1)
    # crest factor (peak / RMS) per 0.5 s speech window: compression shows as a low, tight crest
    mono = v.mean(1)
    h = int(0.5 * SR)
    crest = []
    for i in range(0, len(mono) - h, h):
        k = int((i + h / 2) / SR / HOP)
        if k < len(speech) and speech[k]:
            seg = mono[i:i + h]
            r = np.sqrt(np.mean(seg ** 2))
            if r > 1e-4:
                crest.append(20 * np.log10(np.abs(seg).max() / r))
    out["crest_db_p10_p50_p90"] = q(crest)
    # spectral balance of the speech (long-term average spectrum, 1/3-ish bands, dB re the total)
    sp_idx = np.repeat(speech, int(HOP * SR))[: len(mono)]
    ys = mono[: len(sp_idx)][sp_idx]
    if len(ys) > SR:
        import scipy.signal as ss
        fr, P = ss.welch(ys, SR, nperseg=4096)
        tot = P[(fr >= 50) & (fr <= 16000)].sum()
        band = lambda lo, hi: round(float(10 * np.log10(P[(fr >= lo) & (fr < hi)].sum() / tot + 1e-12)), 1)
        out["ltas_db_rel_total"] = {"lt100": band(20, 100), "100_300": band(100, 300), "300_1k": band(300, 1000),
                                    "1k_4k": band(1000, 4000), "4k_8k": band(4000, 8000), "8k_16k": band(8000, 16000)}
        out["brightness_db_4k_8k_minus_300_1k"] = round(out["ltas_db_rel_total"]["4k_8k"] - out["ltas_db_rel_total"]["300_1k"], 1)
        out["presence_db_1k_4k_minus_300_1k"] = round(out["ltas_db_rel_total"]["1k_4k"] - out["ltas_db_rel_total"]["300_1k"], 1)
        out["spectral_centroid_hz"] = int((fr * P).sum() / P.sum())
    # pace
    if words:
        st_ = np.array([w["s"] for w in words])
        span = st_[-1] - st_[0]
        out["words"] = len(words)
        out["wps"] = round(len(words) / max(span, 1e-3), 2)
        rates = [((st_ >= w0) & (st_ < w0 + 3)).sum() / 3 for w0 in np.arange(st_[0], st_[-1] - 3, 1.0)]
        out["wps_3s_p10_p50_p90"] = q(rates, nd=2)
        out["wps_3s_cv"] = round(float(np.std(rates) / np.mean(rates)), 3) if rates else None
    return out


def breaths_and_gaps(v, mix, nv, speech_fine, fine_hop, speech_ref_db):
    """speech gaps (>= 120 ms, from the 20 ms speech mask) -> room tone of the mix / vocals stem and breaths"""
    import librosa
    gaps = [(a * fine_hop, b * fine_hop) for a, b in runs(~speech_fine) if (b - a) * fine_hop >= 0.12]
    vm, mm = v.mean(1), mix.mean(1)
    rms = lambda s: 20 * np.log10(np.sqrt(np.mean(s ** 2)) + 1e-9)
    vg, mg, breaths = [], [], []
    for g0, g1 in gaps:
        i0, i1 = int((g0 + 0.02) * SR), int((g1 - 0.02) * SR)
        if i1 - i0 < int(0.06 * SR):
            continue
        vs, ms = vm[i0:i1], mm[i0:i1]
        vg.append(rms(vs) - speech_ref_db)
        mg.append(rms(ms) - speech_ref_db)
        # breath: noise-like voice-stem energy 10-40 dB under speech for 100-700 ms inside the gap, centroid 700-5k
        if 0.1 <= g1 - g0 <= 1.2:
            fl = librosa.feature.spectral_flatness(y=vs, n_fft=1024, hop_length=256)[0]
            ce = librosa.feature.spectral_centroid(y=vs, sr=SR, n_fft=1024, hop_length=256)[0]
            fr = 20 * np.log10(np.sqrt(np.mean(vs[: len(vs) // 256 * 256].reshape(-1, 256) ** 2, 1)) + 1e-9) - speech_ref_db
            m = (fr > -40) & (fr < -10) & (fl[: len(fr)] > 0.05) & (ce[: len(fr)] > 700) & (ce[: len(fr)] < 6000)
            if m.sum() * 256 / SR >= 0.1:
                breaths.append(round(g0, 2))
    T = len(mm) / SR
    fr = 20 * np.log10(np.sqrt(np.mean(mm[: len(mm) // 2205 * 2205].reshape(-1, 2205) ** 2, 1)) + 1e-9)
    return {
        "speech_gaps_ge_0p12s": len(gaps),
        "gap_len_s_p50_p90": q([b - a for a, b in gaps], (50, 90), 2) if gaps else None,
        "vocals_stem_in_gaps_db_rel_speech_p10_p50_p90": q(vg),
        "mix_in_gaps_db_rel_speech_p10_p50_p90": q(mg),
        "mix_digital_silence_share_50ms_below_-60dbfs": round(float((fr < -60).mean()), 3),
        "mix_min_50ms_dbfs": round(float(fr.min()), 1),
        "breaths": len(breaths), "breaths_per_min": round(len(breaths) / (T / 60), 1), "breath_t": breaths[:40],
    }


# ----------------------------------------------------------------------------- music bed

def bed_measures(nv, music_only, sfx_mask_ft, ft, speech, vM_med, T, you_see, trans):
    """music-bed lane: non-voice momentary with SFX frames removed (or a true music stem)"""
    src = music_only if music_only is not None else nv
    mM = loudness_track(src, 0.4)[: len(speech)]
    t = (np.arange(len(mM)) + 0.5) * HOP
    bedM = mM.copy()
    if music_only is None and sfx_mask_ft is not None:
        m = np.interp(t, ft, sfx_mask_ft.astype(float)) > 0.1
        m = close_gaps(m, 2)
        # masked frames: interpolate from the clean neighbours
        good = ~m
        if good.sum() > 10:
            bedM[m] = np.interp(t[m], t[good], mM[good])
    bedS = uniform_filter1d(bedM, 10)  # ~1 s
    present = bedS > max(vM_med - 35, -60)
    entry = next((float(t[i]) for i in range(len(t)) if present[i:i + 5].all()), None)
    run_med = median_filter(bedS, size=int(8 / HOP), mode="nearest")
    low = (bedS <= run_med - 10) | ~present
    drops = []
    for i0, i1 in runs(low):
        if (i1 - i0) * HOP >= 0.4 and i0 * HOP > 1.0 and i1 * HOP < T - 1.0:
            drops.append({"t0": round(i0 * HOP, 1), "t1": round(i1 * HOP, 1),
                          "depth_db": round(float(np.median(run_med[i0:i1] - bedS[i0:i1])), 1)})
    # level steps: 2 s after vs 2 s before each second; big steps = section changes in level
    steps = []
    for i in range(20, len(t) - 20):
        steps.append(np.median(bedM[i:i + 20]) - np.median(bedM[i - 20:i]))
    steps = np.array(steps)
    out = {"bed_integrated_lufs": None, "bed_M_speech_median": round(float(np.median(bedM[speech])), 1),
           "bed_M_gaps_median": round(float(np.median(bedM[~speech])), 1) if (~speech).sum() > 5 else None,
           "bed_entry_s": entry, "bed_present_share": round(float(present.mean()), 3),
           "bed_S_p10_p95": q(bedS, (10, 95)), "bed_S_range_p10_p95_db": round(float(np.percentile(bedS, 95) - np.percentile(bedS, 10)), 1),
           "bed_dropouts": drops, "bed_level_steps_ge_4db": int((np.abs(steps) >= 4).sum() // 10) if len(steps) else 0,
           "bed_first_5s_every_1s": [round(float(x), 1) for x in bedS[:50:10]],
           "bed_last_5s_every_1s": [round(float(x), 1) for x in bedS[-50::10]]}
    if you_see:
        ys = []
        for y in you_see:
            i = int(y / HOP)
            if 20 <= i < len(t) - 20:
                ys.append({"t": y, "bed_step_db": round(float(np.median(bedM[i:i + 20]) - np.median(bedM[i - 20:i])), 1),
                           "drop_within_1s": any(abs(d["t0"] - y) <= 1.0 or abs(d["t1"] - y) <= 1.0 for d in drops)})
        out["you_see"] = ys
    return out, bedM


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stems")
    ap.add_argument("--key", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--words")
    ap.add_argument("--frames", help="ricks24_metrics.json:VIDEO_ID (transitions, cuts, camera moves at 240p)")
    ap.add_argument("--cuts", help="cuts.py output (our videos)")
    ap.add_argument("--you-see", default="")
    ap.add_argument("--mixfile")
    ap.add_argument("--voice")
    ap.add_argument("--music")
    ap.add_argument("--sfx")
    a = ap.parse_args()

    st = a.stems
    mixp = a.mixfile or os.path.join(st, "mix.flac")
    mix = load(mixp)
    v = load(a.voice) if a.voice else load(os.path.join(st, "vocals.flac"))
    true_stems = bool(a.voice)
    if true_stems:
        mus = load(a.music)
        sfx = load(a.sfx) if a.sfx else np.zeros_like(mus)
        n = min(len(mix), len(v), len(mus), len(sfx))
        mix, v, mus, sfx = mix[:n], v[:n], mus[:n], sfx[:n]
        nv = mus + sfx
    else:
        nv = load(os.path.join(st, "music.flac"))
        n = min(len(mix), len(v), len(nv))
        mix, v, nv = mix[:n], v[:n], nv[:n]
        mus = None
    T = n / SR
    words = read_words(a.words)
    you_see = [float(x) for x in a.you_see.split(",") if x]

    # speech mask (analyze.py convention: 50 ms loudness within 30 dB of its 95th pct, 0.3 s gaps closed) on 0.1 s grid
    v50 = loudness_track(v, 0.05)
    nt = len(v50)
    ref = np.percentile(v50, 95)
    speech = close_gaps((v50 > ref - 30) & (v50 > -60), 3)
    # fine 20 ms mask for gaps / breaths (no gap closing)
    v20 = loudness_track(v, 0.03, hop=0.02)
    speech_fine = (v20 > np.percentile(v20, 95) - 30) & (v20 > -60)
    speech_fine = close_gaps(speech_fine, 2)
    vM = loudness_track(v, 0.4)[:nt]
    nM = loudness_track(nv, 0.4)[:nt]
    vM_med = float(np.median(vM[speech]))

    res = {"key": a.key, "duration_s": round(T, 2), "stems": "true" if true_stems else "demucs"}
    if a.mixfile is None and st and os.path.exists(os.path.join(st, "mix.flac")):
        res["mix"] = ffmpeg_loud(os.path.join(st, "mix.flac"))
    else:
        res["mix"] = ffmpeg_loud(mixp)
    res["integrated"] = {"voice_lufs": integ(v), "nonvoice_lufs": integ(nv)}
    if mus is not None:
        res["integrated"]["music_lufs"] = integ(mus)
        res["integrated"]["sfx_lufs"] = integ(sfx) if np.abs(sfx).max() > 0 else None

    # SFX
    sp_rms_db = 20 * np.log10(np.sqrt(np.mean(v.mean(1)[smask(speech, n)] ** 2)) + 1e-9)
    # detection stem: our true SFX stem, else the Demucs drums stem (where noise-like SFX land); audible floor from
    # the voice: 50 dB under the 95th percentile of its loudest mel band per frame
    _, Xv = mel_db(v)
    floor = float(np.percentile(Xv.max(0), 95) - 50)
    det = sfx if (true_stems and a.sfx) else load(os.path.join(st, "drums.flac"))[:n]
    evs, mask_ft, ft = sfx_events(det, speech, floor)
    evs = event_levels(evs, det, vM_med)
    kinds = {}
    for e in evs:
        kinds[e["kind"]] = kinds.get(e["kind"], 0) + 1
    res["sfx"] = {"n": len(evs), "per_min": round(len(evs) / (T / 60), 1), "kinds": kinds,
                  "kinds_per_min": {k: round(c / (T / 60), 1) for k, c in kinds.items()},
                  "level_vs_voice_lu_p10_p50_p90": q([e["level_vs_voice_lu"] for e in evs if e["level_vs_voice_lu"] is not None]),
                  "level_by_kind_median": {k: round(float(np.median([e["level_vs_voice_lu"] for e in evs if e["kind"] == k])), 1) for k in kinds},
                  "share_in_speech": round(float(np.mean([e["in_speech"] for e in evs])), 2) if evs else None,
                  "interval_s_p50": round(float(np.median(np.diff([e["t"] for e in evs]))), 2) if len(evs) > 2 else None,
                  "events": evs}

    # visual sync
    trans, cuts, moves = [], [], []
    if a.frames:
        p, vid = a.frames.rsplit(":", 1)
        d = json.load(open(p))["videos"][vid]["measured_240p"]
        trans = [x["start"] for x in d["frame_metrics"]["transitions"]]
        cuts = d["frame_metrics"]["cuts"]
        mv = d["camera"]["moves"]
        pk_thr = np.percentile([m["peak"] for m in mv], 50) if mv else 0
        moves = [m["t"] for m in mv if m["peak"] >= pk_thr]
    elif a.cuts:
        cj = json.load(open(a.cuts))
        trans = [x["t0"] for x in cj][1:]
    vis = sorted(set([round(x, 2) for x in trans + cuts]))
    on = [e["t"] for e in evs]
    sync = {}
    if vis and on:
        sync["visual_changes_with_sfx_within_0p3s"] = align(vis, on, 0.3, T, [])
        sync["sfx_on_a_visual_change_within_0p3s"] = align(on, vis, 0.3, T, [])
        for k in kinds:
            ok = [e["t"] for e in evs if e["kind"] == k]
            if len(ok) >= 2:
                sync[f"{k}_on_visual_change"] = align(ok, vis, 0.3, T, [])
    if moves and on:
        sync["sfx_on_camera_move_peak_within_0p3s"] = align(on, moves, 0.3, T, [])
    sync["n_visual_changes"] = len(vis)
    res["sfx"]["sync"] = sync

    # ambience: 1 s windows of the non-voice stem, noise-like and unpitched
    import librosa
    y = resample_poly(nv.mean(1), 1, 2).astype(np.float32)
    Sx = np.abs(librosa.stft(y, n_fft=2048, hop_length=512))
    H, P = librosa.decompose.hpss(Sx ** 2, margin=1.0)
    hs = H.sum(0) / (H.sum(0) + P.sum(0) + 1e-12)
    fl = librosa.feature.spectral_flatness(S=Sx)[0]
    e = (Sx ** 2).sum(0)
    fps = (SR // 2) / 512
    amb = []
    for w in range(int(T)):
        sl = slice(int(w * fps), int((w + 1) * fps))
        if e[sl].mean() <= 0:
            continue
        amb.append((float(np.median(hs[sl])), float(np.median(fl[sl]))))
    amb = np.array(amb)
    res["nonvoice_texture"] = {"harmonic_share_p10_p50_p90": q(amb[:, 0], nd=2), "flatness_p50": round(float(np.median(amb[:, 1])), 3),
                               "ambience_like_windows_share": round(float(((amb[:, 0] < 0.5) & (amb[:, 1] > 0.05)).mean()), 3)}

    # gap and bed
    bed, bedM = bed_measures(nv, mus, mask_ft, ft, speech, vM_med, T, you_see, trans)
    bed["bed_integrated_lufs"] = integ(mus) if mus is not None else None
    res["bed"] = bed
    res["gap"] = {"voice_minus_nonvoice_M_under_speech_p10_p50_p90": q((vM - nM)[speech]),
                  "voice_minus_bed_M_under_speech_p10_p50_p90": q((vM - bedM)[speech]),
                  "voice_minus_nonvoice_integrated_lu": round(res["integrated"]["voice_lufs"] - res["integrated"]["nonvoice_lufs"], 1),
                  "bed_gap_minus_speech_db": round(bed["bed_M_gaps_median"] - bed["bed_M_speech_median"], 1) if bed["bed_M_gaps_median"] is not None else None,
                  "speech_share": round(float(speech.mean()), 3)}
    res["room"] = breaths_and_gaps(v, mix, nv, speech_fine, 0.02, sp_rms_db)
    res["voice"] = voice_measures(v, speech, words, T)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(res, open(a.out, "w"), indent=1)
    s = {k: res[k] for k in ("mix", "integrated", "gap")}
    s["sfx"] = {k: res["sfx"][k] for k in ("per_min", "kinds", "level_vs_voice_lu_p10_p50_p90")}
    print(a.key, json.dumps(s))


if __name__ == "__main__":
    main()
