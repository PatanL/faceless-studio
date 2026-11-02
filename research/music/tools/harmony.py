"""Chords, keys and progressions of a music track (clean soundtrack or a Demucs music stem). Study only.

Beat-synchronous chroma of the harmonic part (HPSS, CQT 36 bins/oct) -> chord HMM (12 roots x 7 qualities + N, Viterbi
with a self-transition bias) and a key HMM (24 keys on 8-beat windows, Krumhansl profiles, strong self-transition).
Bass pitch class per beat from a low-band CQT shows pedals and inversions. Chords are converted to roman numerals in
the local key, so progressions from different keys can be counted together.

usage (music venv): python research/music/tools/harmony.py audio.flac out.json [--start s] [--end s]
"""
from __future__ import annotations

import json
import sys
from collections import Counter

import numpy as np
import soundfile as sf
from scipy.signal import resample_poly

NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
QUALS = {"maj": [0, 4, 7], "min": [0, 3, 7], "maj7": [0, 4, 7, 11], "min7": [0, 3, 7, 10], "7": [0, 4, 7, 10],
         "sus2": [0, 2, 7], "sus4": [0, 5, 7]}
MAJ = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
MIN = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
ROMAN = ["I", "bII", "II", "bIII", "III", "IV", "#IV", "V", "bVI", "VI", "bVII", "VII"]


def viterbi(logp, stay):
    """logp (T, S) emission log-probs; uniform switching with self-transition prob `stay`"""
    T, S = logp.shape
    ls, lm = np.log(stay), np.log((1 - stay) / (S - 1))
    d = logp[0].copy()
    bp = np.zeros((T, S), int)
    for t in range(1, T):
        best = d.max()
        arg = d.argmax()
        cand_stay = d + ls
        cand_move = best + lm
        bp[t] = np.where(cand_stay >= cand_move, np.arange(S), arg)
        d = np.maximum(cand_stay, cand_move) + logp[t]
    path = [int(d.argmax())]
    for t in range(T - 1, 0, -1):
        path.append(int(bp[t][path[-1]]))
    return path[::-1]


def analyse(y, sr):
    import librosa
    yh = librosa.effects.harmonic(y, margin=3.0)
    _, beats = librosa.beat.beat_track(y=y, sr=sr, hop_length=512, units="frames")
    tempo = float(np.atleast_1d(librosa.feature.tempo(y=y, sr=sr, hop_length=512))[0])
    C = librosa.feature.chroma_cqt(y=yh, sr=sr, hop_length=512, bins_per_octave=36, n_octaves=6,
                                   fmin=librosa.note_to_hz("C2"))
    B = np.abs(librosa.cqt(yh, sr=sr, hop_length=512, fmin=librosa.note_to_hz("C1"), n_bins=36, bins_per_octave=12))
    bass_pc = (B.reshape(3, 12, -1).sum(0))
    if len(beats) < 8:  # no beat grid (rubato / ambient): 0.5 s frames
        beats = np.arange(0, C.shape[1], int(0.5 * sr / 512))
    Cb = librosa.util.sync(C, beats, aggregate=np.median)
    Bb = librosa.util.sync(bass_pc, beats, aggregate=np.median)
    bt = librosa.frames_to_time(np.concatenate([[0], beats]), sr=sr, hop_length=512)
    energy = librosa.util.sync(librosa.feature.rms(y=yh, hop_length=512), beats)[0]
    # --- chords
    labels, tmpl = [], []
    for r in range(12):
        for q, iv in QUALS.items():
            v = np.zeros(12)
            v[[(r + i) % 12 for i in iv]] = 1
            v[r] += 0.5  # root weight
            labels.append((r, q))
            tmpl.append(v / np.linalg.norm(v))
    tmpl = np.array(tmpl)
    X = Cb / (np.linalg.norm(Cb, axis=0, keepdims=True) + 1e-9)
    sim = tmpl @ X  # (S, T)
    quiet = energy < np.percentile(energy, 10) * 0.5
    logp = (12 * sim).T
    logp -= logp.max(1, keepdims=True)
    logp = logp - np.log(np.exp(logp).sum(1, keepdims=True))
    path = viterbi(logp, 0.85)
    # --- keys on 8-beat windows
    K = []
    for r in range(12):
        K.append(np.roll(MAJ, r) / np.linalg.norm(MAJ))
        K.append(np.roll(MIN, r) / np.linalg.norm(MIN))
    K = np.array(K)
    win = 8
    Cw = np.stack([Cb[:, max(0, i - win // 2):i + win // 2].mean(1) for i in range(Cb.shape[1])], 1)
    Cw = (Cw - Cw.mean(0)) / (Cw.std(0) + 1e-9)
    ksim = (K - K.mean(1, keepdims=True)) @ Cw / 12
    klog = (8 * ksim).T
    klog -= klog.max(1, keepdims=True)
    kpath = viterbi(klog - np.log(np.exp(klog).sum(1, keepdims=True)), 0.995)
    keyname = lambda k: f"{NAMES[k // 2]} {'maj' if k % 2 == 0 else 'min'}"
    # --- segments
    n = len(path)
    times = bt[:n + 1] if len(bt) > n else np.append(bt, bt[-1] + 0.5)
    chords = []
    for i in range(n):
        r, q = labels[path[i]]
        kk = kpath[i]
        tonic = kk // 2
        rn = ROMAN[(r - tonic) % 12]
        rn = rn.lower() if q in ("min", "min7") else rn
        lab = f"{NAMES[r]}{'' if q == 'maj' else q}"
        bass = int(Bb[:, i].argmax())
        if chords and chords[-1]["label"] == lab and chords[-1]["key"] == keyname(kk):
            chords[-1]["t1"] = float(times[i + 1])
            chords[-1]["beats"] += 1
            chords[-1]["bass_votes"].append(bass)
            continue
        chords.append({"t0": float(times[i]), "t1": float(times[i + 1]), "label": lab, "root": r, "q": q,
                       "key": keyname(kk), "roman": rn + ("" if q in ("maj", "min") else q.replace("min", "")),
                       "beats": 1, "bass_votes": [bass], "fit": round(float(sim[path[i], i]), 2),
                       "quiet": bool(quiet[i])})
    for c in chords:
        bv = Counter(c.pop("bass_votes")).most_common(1)[0][0]
        c["bass"] = NAMES[bv]
        c["bass_rel"] = (bv - c["root"]) % 12  # 0 root position, 3/4 third, 7 fifth, else other (pedal / slash)
        c["t0"], c["t1"] = round(c["t0"], 2), round(c["t1"], 2)
    keys = []
    for i, kk in enumerate(kpath):
        if keys and keys[-1]["key"] == keyname(kk):
            keys[-1]["t1"] = round(float(times[i + 1]), 2)
        else:
            keys.append({"t0": round(float(times[i]), 2), "t1": round(float(times[i + 1]), 2), "key": keyname(kk)})
    return tempo, chords, keys


def stats(chords, keys, tempo):
    sol = [c for c in chords if not c["quiet"] and c["beats"] >= 2]
    tot = sum(c["beats"] for c in sol) or 1
    qual = Counter()
    for c in sol:
        qual[c["q"]] += c["beats"]
    rn_b = Counter()
    rn_4 = Counter()
    seq = [c["roman"] for c in sol]
    for a, b in zip(seq, seq[1:]):
        rn_b[f"{a}-{b}"] += 1
    for i in range(len(seq) - 3):
        rn_4["-".join(seq[i:i + 4])] += 1
    deg = Counter()
    for c in sol:
        deg[c["roman"]] += c["beats"]
    km = [k for k in keys if k["t1"] - k["t0"] >= 6]
    mods = []
    for a, b in zip(km, km[1:]):
        ta = NAMES.index(a["key"].split()[0])
        tb = NAMES.index(b["key"].split()[0])
        mods.append({"t": b["t0"], "from": a["key"], "to": b["key"], "semitones": (tb - ta) % 12})
    return {"tempo": round(tempo, 1), "n_chords": len(sol),
            "chord_len_beats_median": float(np.median([c["beats"] for c in sol])) if sol else None,
            "quality_share": {q: round(v / tot, 3) for q, v in qual.most_common()},
            "degree_share": {d: round(v / tot, 3) for d, v in deg.most_common(12)},
            "top_bigrams": rn_b.most_common(12), "top_4grams": rn_4.most_common(10),
            "inversion_or_pedal_share": round(sum(c["beats"] for c in sol if c["bass_rel"] not in (0,)) / tot, 3),
            "keys": km, "modulations": mods,
            "minor_key_share": round(sum(k["t1"] - k["t0"] for k in km if k["key"].endswith("min")) /
                                     max(1e-9, sum(k["t1"] - k["t0"] for k in km)), 3)}


def main():
    src, out = sys.argv[1], sys.argv[2]
    start = float(sys.argv[sys.argv.index("--start") + 1]) if "--start" in sys.argv else 0.0
    end = float(sys.argv[sys.argv.index("--end") + 1]) if "--end" in sys.argv else None
    x, sr = sf.read(src, dtype="float32", always_2d=True)
    y = x.mean(1)[int(start * sr): int(end * sr) if end else None]
    y = resample_poly(y, 22050, sr).astype(np.float32)
    tempo, chords, keys = analyse(y, 22050)
    for c in chords:
        c["t0"] = round(c["t0"] + start, 2)
        c["t1"] = round(c["t1"] + start, 2)
    for k in keys:
        k["t0"] = round(k["t0"] + start, 2)
        k["t1"] = round(k["t1"] + start, 2)
    st = stats(chords, keys, tempo)
    json.dump({"src": src, "stats": st, "chords": chords, "keys": keys}, open(out, "w"), indent=0)
    print(json.dumps({k: v for k, v in st.items() if k not in ("keys",)}, indent=0)[:3000])


if __name__ == "__main__":
    main()
