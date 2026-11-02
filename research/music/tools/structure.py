"""Layering and recurring themes in a clean soundtrack (Epic Mountain OSTs). Study only.

Layers (0.5 s frames): sub (20-60 Hz), bass (harmonic 60-200 Hz), pad (sustained harmonic 200-2000 Hz), keys/arp (note
onsets in the harmonic part above 1.2 kHz), lead (one salient pitch above C5 standing out of the chord), perc (HPSS
percussive part). A layer is "on" when within 18 dB of its own 95th percentile (onset layers: >= 1 onset/s). Sections
come from a chroma + band-energy novelty curve; per section: layers at the start, when the count peaks, entry order.

Themes: beat-synchronous chroma of the top register (C5-C8, harmonic part) in 8-beat windows; two windows match when
their transposition-invariant correlation >= 0.8 and they lie >= 24 beats apart; matches with < 0.15 beat-to-beat
change are ostinato (an arpeggio over one chord), not a theme. Each theme reports its occurrences, transpositions and
the register / level of each return (development).

usage (music venv): python research/music/tools/structure.py ost.flac out.json
"""
import json
import sys
from collections import Counter

import numpy as np
import soundfile as sf
from scipy.ndimage import maximum_filter1d, uniform_filter1d
from scipy.signal import resample_poly

SR = 22050
HOP = 512


def main():
    import librosa
    src, out = sys.argv[1], sys.argv[2]
    x, sr = sf.read(src, dtype="float32", always_2d=True)
    y = resample_poly(x.mean(1), SR, sr).astype(np.float32)
    S = np.abs(librosa.stft(y, n_fft=2048, hop_length=HOP)) ** 2
    f = librosa.fft_frequencies(sr=SR, n_fft=2048)
    H, P = librosa.decompose.hpss(S, margin=2.0)
    ft = librosa.frames_to_time(np.arange(S.shape[1]), sr=SR, hop_length=HOP)
    G = 0.5
    ng = int(ft[-1] / G) + 1
    gi = np.minimum((ft / G).astype(int), ng - 1)
    agg = lambda v: np.bincount(gi, weights=v, minlength=ng) / (np.bincount(gi, minlength=ng) + 1e-9)
    db = lambda v: 10 * np.log10(v + 1e-12)
    band = lambda M, lo, hi: M[(f >= lo) & (f < hi)].sum(0)
    lay = {
        "sub": db(agg(band(S, 20, 60))),
        "bass": db(agg(band(H, 60, 200))),
        "pad": None, "keys": None, "lead": None,
        "perc": db(agg(P[(f >= 60)].sum(0))),
    }
    if len(sys.argv) > 3:  # Demucs stems of the soundtrack: drums = percussion, bass stem = bass
        def stem_db(name):
            z, r = sf.read(f"{sys.argv[3]}/{name}.flac", dtype="float32", always_2d=True)
            z = resample_poly(z.mean(1), SR, r).astype(np.float32)[: len(y)]
            e = librosa.feature.rms(y=z, frame_length=2048, hop_length=HOP)[0] ** 2
            e = np.pad(e, (0, max(0, len(ft) - len(e))))[: len(ft)]
            return db(agg(e))
        lay["perc"] = stem_db("drums")
        lay["bass"] = stem_db("bass")
    # pad: sustained harmonic 200-2000 Hz = harmonic energy minus its onset (flux) part
    hm = band(H, 200, 2000)
    flux = np.maximum(0, np.diff(db(hm), prepend=db(hm)[0]))
    lay["pad"] = db(agg(hm)) - 0.0 * agg(flux)
    melH = librosa.feature.melspectrogram(S=H, sr=SR, n_mels=48, fmin=1200, fmax=9000)
    on_hi = librosa.onset.onset_strength(S=librosa.power_to_db(melH), sr=SR, hop_length=HOP)
    pk = librosa.util.peak_pick(on_hi, pre_max=3, post_max=3, pre_avg=10, post_avg=10, delta=np.std(on_hi) * 1.2, wait=3)
    rate = np.bincount(gi[pk], minlength=ng) / G
    lay["keys"] = uniform_filter1d(rate, 4)  # onsets/s
    # lead: salient top pitch above C5 (CQT peak prominence over the median of the C5-C8 bins)
    yh = librosa.istft(np.sqrt(H) * np.exp(1j * np.angle(librosa.stft(y, n_fft=2048, hop_length=HOP))), hop_length=HOP,
                       length=len(y))
    C = np.abs(librosa.cqt(yh, sr=SR, hop_length=HOP, fmin=librosa.note_to_hz("C5"), n_bins=36, bins_per_octave=12))
    Cd = librosa.amplitude_to_db(C, ref=np.max)
    prom = Cd.max(0) - np.median(Cd, 0)
    lay["lead"] = agg(prom)
    # --- activity
    act = {}
    for k, v in lay.items():
        if k == "keys":
            act[k] = v >= 1.0
        elif k == "lead":
            act[k] = v >= np.percentile(v, 75) + 0  # top quartile prominence = a line stands out
            act[k] &= lay["keys"] < 6
        else:
            act[k] = v >= np.percentile(v, 95) - 18
    total = db(agg(S.sum(0)))
    loud = total >= np.percentile(total, 95) - 30
    for k in act:
        act[k] &= loud
    n_on = sum(act[k].astype(int) for k in act)
    # --- sections (novelty on chroma + band levels)
    ch = librosa.feature.chroma_stft(S=H, sr=SR, hop_length=HOP)
    feats = np.vstack([np.stack([agg(c) for c in ch]) * 2, np.stack([lay[k] for k in ("sub", "bass", "pad", "perc")]) / 10,
                       lay["keys"][None] / 4])
    Z = (feats - feats.mean(1, keepdims=True)) / (feats.std(1, keepdims=True) + 1e-9)
    Zn = Z / (np.linalg.norm(Z, axis=0, keepdims=True) + 1e-9)
    SSM = Zn.T @ Zn
    k = 12
    ii = np.arange(-k, k)
    g = np.exp(-0.5 * ((ii + 0.5) / (0.5 * k)) ** 2)
    ker = np.outer(g, g) * np.outer(np.sign(ii + 0.5), np.sign(ii + 0.5))
    nov = np.array([np.sum(SSM[c - k:c + k, c - k:c + k] * ker) if k <= c < ng - k else 0 for c in range(ng)])
    mx = maximum_filter1d(nov, size=2 * 12 + 1)
    bidx = [i for i in np.nonzero((nov == mx) & (nov > np.median(nov) + 0.8 * nov.std()))[0]]
    edges = [0] + bidx + [ng]
    names = list(act)
    sections = []
    for a, b in zip(edges[:-1], edges[1:]):
        if b - a < 8:
            continue
        cnt = n_on[a:b]
        first = {nm: next((round((i - a) * G, 1) for i in range(a, b) if act[nm][i]), None) for nm in names}
        order = [nm for nm, t in sorted(((nm, t) for nm, t in first.items() if t is not None), key=lambda z: z[1])]
        start_layers = [nm for nm in names if act[nm][a:a + 4].mean() > 0.5]
        drops = [nm for nm in names if act[nm][a:b].any() and (act[nm][a:b].mean() < 0.8) and
                 any(act[nm][i] and not act[nm][i + 1] for i in range(a, b - 1))]
        sections.append({"t0": round(a * G, 1), "t1": round(b * G, 1), "dur": round((b - a) * G, 1),
                         "layers_at_start": start_layers, "n_start": int(np.median(cnt[:4])),
                         "n_max": int(cnt.max()), "t_to_max_s": round(float(np.argmax(cnt >= cnt.max())) * G, 1),
                         "entry_order": order, "entry_times_s": {nm: first[nm] for nm in order},
                         "share_on": {nm: round(float(act[nm][a:b].mean()), 2) for nm in names},
                         "layers_dropping_mid_section": drops})
    # build pattern summary
    builds = [s for s in sections if s["n_max"] > s["n_start"]]
    summ = {
        "sections": len(sections), "section_len_median_s": float(np.median([s["dur"] for s in sections])) if sections else None,
        "layers_at_section_start_median": float(np.median([s["n_start"] for s in sections])) if sections else None,
        "layers_max_median": float(np.median([s["n_max"] for s in sections])) if sections else None,
        "share_sections_that_build": round(len(builds) / max(1, len(sections)), 2),
        "time_to_full_median_s": float(np.median([s["t_to_max_s"] for s in builds])) if builds else None,
        "first_layer_counts": Counter(s["entry_order"][0] for s in sections if s["entry_order"]).most_common(),
        "share_on_overall": {nm: round(float(act[nm][loud].mean()), 2) for nm in names},
        "layer_count_hist": {int(c): round(float((n_on[loud] == c).mean()), 2) for c in range(7)},
    }
    # --- themes
    tempo, beats = librosa.beat.beat_track(y=y, sr=SR, hop_length=HOP)
    Chi = librosa.feature.chroma_cqt(y=yh, sr=SR, hop_length=HOP, fmin=librosa.note_to_hz("C5"), n_octaves=3)
    Cb = librosa.util.sync(Chi, beats, aggregate=np.max)
    Cb = Cb / (Cb.max(0, keepdims=True) + 1e-9)
    bt = librosa.frames_to_time(np.concatenate([[0], beats]), sr=SR, hop_length=HOP)
    W = 8
    wins = []
    for i in range(0, Cb.shape[1] - W, 2):
        w = Cb[:, i:i + W]
        change = float(np.mean(np.abs(np.diff(w, axis=1))))
        wins.append((i, w, change))
    matches = []
    for a in range(len(wins)):
        ia, wa, ca = wins[a]
        if ca < 0.15:
            continue
        va = (wa - wa.mean()).ravel()
        for b in range(a + 1, len(wins)):
            ib, wb, cb = wins[b]
            if ib - ia < 24 or cb < 0.15:
                continue
            best, sh = -1, 0
            for s in range(12):
                vb = (np.roll(wb, s, axis=0) - wb.mean()).ravel()
                r = float(va @ vb / (np.linalg.norm(va) * np.linalg.norm(vb) + 1e-9))
                if r > best:
                    best, sh = r, s
            if best >= 0.8:
                matches.append((ia, ib, round(best, 2), sh))
    # cluster windows into themes (union-find)
    par = {}

    def fnd(u):
        par.setdefault(u, u)
        while par[u] != u:
            par[u] = par[par[u]]
            u = par[u]
        return u
    for ia, ib, _, _ in matches:
        par[fnd(ia)] = fnd(ib)
    groups = {}
    for ia, ib, r, sh in matches:
        groups.setdefault(fnd(ia), set()).update([ia, ib])
    cent = librosa.feature.spectral_centroid(S=np.sqrt(H), sr=SR)[0]
    rms = librosa.feature.rms(S=np.sqrt(S))[0]
    themes = []
    for g_, members in groups.items():
        ms = sorted(members)
        # merge overlapping windows into occurrences
        occ = []
        for i in ms:
            if occ and i - occ[-1][1] <= 2:
                occ[-1][1] = i + W
            else:
                occ.append([i, i + W])
        if len(occ) < 2:
            continue
        times = [(round(float(bt[min(a, len(bt) - 1)]), 1), round(float(bt[min(b, len(bt) - 1)]), 1)) for a, b in occ]
        span = times[-1][0] - times[0][0]
        fr = lambda t0, t1: (ft >= t0) & (ft < t1)
        regs = [int(np.median(cent[fr(*tt)])) if fr(*tt).any() else None for tt in times]
        lv = [round(float(20 * np.log10(np.mean(rms[fr(*tt)]) + 1e-9)), 1) if fr(*tt).any() else None for tt in times]
        top = [librosa.midi_to_note(int(librosa.hz_to_midi(librosa.note_to_hz("C5")) + np.argmax(C[:, fr(*tt)].mean(1))))
               if fr(*tt).any() else None for tt in times]
        themes.append({"occurrences": times, "n": len(times), "span_s": round(span, 1), "centroid_hz": regs,
                       "level_db": lv, "top_note": top})
    themes.sort(key=lambda t: (-t["n"], -t["span_s"]))
    T = len(y) / SR
    summ["themes_returning_after_60s"] = sum(1 for t in themes if t["span_s"] >= 60)
    summ["largest_theme"] = themes[0] if themes else None
    json.dump({"src": src, "duration_s": round(T, 1), "summary": summ, "sections": sections, "themes": themes[:12]},
              open(out, "w"), indent=0)
    print(json.dumps(summ, indent=0)[:2500])


if __name__ == "__main__":
    main()
