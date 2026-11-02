"""Isolate a video's sound effects by explaining its Demucs music stem with the released soundtrack (study only).

1. Align: 20 s chunks of the video's music stem against the OST (FFT cross-correlation of the onset envelope plus
   12 chroma rows at 20 ms), offsets median-filtered; chunks without a confident match are left unexplained.
2. Explain: per 46 ms frame and mel band, the aligned OST times a smooth per-band gain (least squares over 4 s).
3. Residual = video music minus explained (power, floored at 0) -> SFX candidates where the residual is within 6 dB of
   the music (or louder) for >= 60 ms. Each event: time, length, level vs music and voice, flatness (noise vs tone),
   whether it is "in key" (chroma of the event vs the OST chroma around it), and its distance to the nearest visual
   transition / setting change.

usage (music venv): python sfx_residual.py video_stems_dir ost.flac settings.csv events.json out.json [--exclude a-b,..]
"""
import csv
import json
import sys

import numpy as np
import soundfile as sf
from scipy.ndimage import median_filter, uniform_filter1d
from scipy.signal import resample_poly

SR = 22050
HOP = 1024


def load(p):
    x, r = sf.read(p, dtype="float32", always_2d=True)
    return resample_poly(x.mean(1), SR, r).astype(np.float32)


def feats(y):
    import librosa
    on = librosa.onset.onset_strength(y=y, sr=SR, hop_length=441)
    ch = librosa.feature.chroma_stft(y=y, sr=SR, hop_length=441)
    F = np.vstack([(on - on.mean()) / (on.std() + 1e-9), (ch - ch.mean(1, keepdims=True)) / (ch.std(1, keepdims=True) + 1e-9)])
    return F


def xcorr(a, b):
    """best lag of a (short) inside b, summed over rows, normalised"""
    n = len(b[0]) + len(a[0])
    nfft = 1 << int(np.ceil(np.log2(n)))
    acc = np.zeros(nfft)
    for ra, rb in zip(a, b):
        acc += np.fft.irfft(np.fft.rfft(rb, nfft) * np.conj(np.fft.rfft(ra, nfft)), nfft)
    acc = acc[: len(b[0]) - len(a[0]) + 1]
    i = int(np.argmax(acc))
    return i, float(acc[i] / (len(a[0]) * len(a)))


def main():
    import librosa
    vdir, ost, setp, evp, out = sys.argv[1:6]
    excl = []
    if "--exclude" in sys.argv:
        excl = [tuple(map(float, r.split("-"))) for r in sys.argv[sys.argv.index("--exclude") + 1].split(",")]
    vm = load(f"{vdir}/music.flac")
    vv = load(f"{vdir}/vocals.flac")
    o = load(ost)
    Fv, Fo = feats(vm), feats(o)
    fps = SR / 441
    chunk, step = int(20 * fps), int(5 * fps)
    offs = []
    for s in range(0, Fv.shape[1] - chunk, step):
        lag, sc = xcorr(Fv[:, s:s + chunk], Fo)
        offs.append((s / fps, (lag - s) / fps, sc))
    offs = np.array(offs)
    good = offs[:, 2] > np.percentile(offs[:, 2], 25)
    med = median_filter(offs[:, 1], size=5)
    # frame-level mapping video t -> ost t (piecewise by chunk centre)
    S_v = np.abs(librosa.stft(vm, n_fft=2048, hop_length=HOP)) ** 2
    S_o = np.abs(librosa.stft(o, n_fft=2048, hop_length=HOP)) ** 2
    fb = librosa.filters.mel(sr=SR, n_fft=2048, n_mels=48, fmin=40, fmax=10000)
    Mv, Mo = fb @ S_v, fb @ S_o
    tv = librosa.frames_to_time(np.arange(Mv.shape[1]), sr=SR, hop_length=HOP)
    cen = offs[:, 0] + 10
    off_t = np.interp(tv, cen, med)
    ok_t = np.interp(tv, cen, (good & (np.abs(offs[:, 1] - med) < 0.2)).astype(float)) > 0.5
    io = np.clip(np.round((tv + off_t) * SR / HOP).astype(int), 0, Mo.shape[1] - 1)
    Mo_al = Mo[:, io]
    # per-band gain, smoothed over ~4 s
    w = int(4 * SR / HOP)
    num = uniform_filter1d(Mv * Mo_al, w, axis=1)
    den = uniform_filter1d(Mo_al ** 2, w, axis=1) + 1e-12
    g = np.clip(num / den, 0, 10)
    expl = g * Mo_al
    resid = np.maximum(Mv - expl, 0)
    # bands above ~300 Hz only (the bass misfits of a 46 ms grid are not SFX)
    rdb = 10 * np.log10(resid[8:].sum(0) + 1e-12)
    mdb = 10 * np.log10(Mv[8:].sum(0) + 1e-12)
    jump = rdb - median_filter(rdb, size=int(1.0 * SR / HOP), origin=int(0.5 * SR / HOP) - 1)
    S_vv = np.abs(librosa.stft(vv, n_fft=2048, hop_length=HOP)) ** 2
    vdb = 10 * np.log10((fb @ S_vv).sum(0) + 1e-12)
    explained_share = float(1 - resid.sum() / (Mv.sum() + 1e-12))
    excl_m = np.zeros(len(tv), bool)
    for a, b in excl:
        excl_m |= (tv >= a) & (tv < b)
    # an SFX: the unexplained part is at least as loud as the music there and jumps >= 8 dB over the second before
    onset = ok_t & ~excl_m & (rdb >= mdb - 1) & (jump >= 8) & (mdb > np.percentile(mdb, 20))
    cand = np.zeros(len(onset), bool)
    for k in np.nonzero(onset)[0]:  # extend each onset while the residual stays dominant
        e = k
        while e < len(rdb) and rdb[e] >= mdb[e] - 3 and e - k < int(2.0 * SR / HOP):
            e += 1
        cand[k:max(e, k + 2)] = True
    ch_v = librosa.feature.chroma_stft(S=resid, sr=SR) if False else None  # noqa
    # events
    ev = []
    i = 0
    trans = [x["start"] for x in json.load(open(evp)).get("transitions", [])]
    sets = [float(r["start"]) for r in csv.DictReader(open(setp))]
    while i < len(cand):
        if cand[i]:
            j = i
            while j < len(cand) and cand[j]:
                j += 1
            if (j - i) * HOP / SR >= 0.06:
                seg = resid[:, i:j]
                lin = seg.mean(1)
                flat = float(np.exp(np.mean(np.log(lin[8:] + 1e-12))) / (np.mean(lin[8:]) + 1e-12))
                # chroma of the residual vs the OST around it (+-2 s): in key?
                f_ = librosa.fft_frequencies(sr=SR, n_fft=2048)
                cr = librosa.feature.chroma_stft(S=np.maximum(S_v[:, i:j] - (g[:, i:j].mean() * S_o[:, io[i:j]]), 0),
                                                 sr=SR).mean(1)
                a0, a1 = max(0, i - int(2 * SR / HOP)), min(len(io), j + int(2 * SR / HOP))
                co = librosa.feature.chroma_stft(S=S_o[:, io[a0:a1]], sr=SR).mean(1)
                inkey = float(cr @ co / (np.linalg.norm(cr) * np.linalg.norm(co) + 1e-9))
                t = float(tv[i])
                cent = float((f_[:, None] * np.maximum(S_v[:, i:j] - S_o[:, io[i:j]] * g[:, i:j].mean(), 0)).sum() /
                             (np.maximum(S_v[:, i:j] - S_o[:, io[i:j]] * g[:, i:j].mean(), 0).sum() + 1e-12))
                ev.append({"t": round(t, 2), "dur": round((j - i) * HOP / SR, 2),
                           "resid_minus_music_db": round(float(np.max(rdb[i:j] - mdb[i:j])), 1),
                           "resid_minus_voice_db": round(float(np.max(rdb[i:j]) - np.median(vdb[max(0, i - 40):j + 40])), 1),
                           "flatness": round(flat, 3), "centroid_hz": int(cent), "chroma_vs_music": round(inkey, 2),
                           "to_transition_s": round(min((tt - t for tt in trans), key=abs), 2) if trans else None,
                           "to_setting_s": round(min((tt - t for tt in sets), key=abs), 2) if sets else None})
            i = j
        else:
            i += 1
    T_eff = float((ok_t & ~excl_m).sum() * HOP / SR)
    near_tr = [e for e in ev if e["to_transition_s"] is not None and abs(e["to_transition_s"]) <= 0.5]
    tr_used = [tt for tt in trans if not any(a <= tt < b for a, b in excl)]
    tr_with = sum(1 for tt in tr_used if any(abs(e["t"] - tt) <= 0.5 for e in ev))
    summ = {"aligned_share": round(float(ok_t.mean()), 2), "explained_power_share": round(explained_share, 3),
            "events": len(ev), "events_per_min": round(len(ev) / (T_eff / 60), 2),
            "transitions_with_an_sfx_within_0p5s": f"{tr_with}/{len(tr_used)}",
            "noise_like_share (flatness>0.3)": round(np.mean([e["flatness"] > 0.3 for e in ev]), 2) if ev else None,
            "in_key_share (chroma cos>0.8)": round(np.mean([e["chroma_vs_music"] > 0.8 for e in ev]), 2) if ev else None,
            "level_vs_music_db_median": float(np.median([e["resid_minus_music_db"] for e in ev])) if ev else None,
            "level_vs_voice_db_median": float(np.median([e["resid_minus_voice_db"] for e in ev])) if ev else None,
            "dur_median_s": float(np.median([e["dur"] for e in ev])) if ev else None,
            "centroid_median_hz": float(np.median([e["centroid_hz"] for e in ev])) if ev else None,
            "near_transition_events": len(near_tr)}
    json.dump({"summary": summ, "offsets": offs.tolist(), "events": ev}, open(out, "w"), indent=0)
    print(json.dumps(summ, indent=1))


if __name__ == "__main__":
    main()
