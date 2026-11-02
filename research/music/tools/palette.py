"""Sound palette: which of our SoundFont presets (alone, layered, processed) sit closest to the reference timbres.

Reference events come from the Demucs "other" stem of the clean soundtracks (no voice): isolated note onsets above
1 kHz (bells / plucks / mallets) and sustained harmonic stretches (pads). Each event is described by a 40-band log-mel
envelope (level-normalised), attack time, decay rate and spectral flatness. Reference note events are clustered (k=3);
every candidate (GeneralUser GS preset, a layered pair, or a pedalboard-processed variant) plays the same register and
is described the same way; the report ranks candidates per cluster and for pads. The reference audio never leaves the
Spark; the comparison clips rendered here are ours (research/music/palette/).

usage (music venv, from ~/studio/app): python research/music/tools/palette.py out.json clipdir stemdir [stemdir ...]
"""
import json
import os
import sys

import numpy as np
import soundfile as sf
from scipy.signal import resample_poly

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
SR = 48000
NM = 40


def mel_fb(sr, n_fft):
    import librosa
    return librosa.filters.mel(sr=sr, n_fft=n_fft, n_mels=NM, fmin=200, fmax=12000)


FB = None


def describe(x, sr=SR):
    """x: mono note event starting at its onset (>= 0.6 s)"""
    global FB
    import librosa
    if FB is None:
        FB = mel_fb(SR, 2048)
    S = np.abs(librosa.stft(x, n_fft=2048, hop_length=240)) ** 2
    M = FB @ S
    e = M.sum(0)
    edb = 10 * np.log10(e + 1e-12)
    pk = int(np.argmax(edb[:40]))
    # attack: 10 % -> 90 % of the peak energy (in ms)
    lin = e[: pk + 1]
    a10 = np.argmax(lin >= 0.1 * e[pk]) if pk else 0
    attack = (pk - a10) * 240 / sr * 1000
    # decay: dB drop from the peak to +300 ms (per second)
    j = min(len(edb) - 1, pk + int(0.3 * sr / 240))
    decay = (edb[pk] - edb[j]) / 0.3
    env = 10 * np.log10(M[:, pk:pk + int(0.25 * sr / 240)].mean(1) + 1e-12)
    env -= env.max()
    flat = float(np.exp(np.mean(np.log(M[10:, pk] + 1e-12))) / (np.mean(M[10:, pk]) + 1e-12))
    return np.concatenate([env / 10.0, [attack / 50.0, decay / 40.0, flat * 5]])


def ref_events(stem_dirs, max_per=150):
    import librosa
    notes, pads = [], []
    for d in stem_dirs:
        x, sr = sf.read(os.path.join(d, "other.flac"), dtype="float32", always_2d=True)
        y = resample_poly(x.mean(1), SR, sr).astype(np.float32)
        yh = librosa.effects.harmonic(y, margin=2.0)
        mel = librosa.feature.melspectrogram(y=yh, sr=SR, n_fft=2048, hop_length=480, n_mels=48, fmin=1000, fmax=10000)
        on = librosa.onset.onset_strength(S=librosa.power_to_db(mel), sr=SR, hop_length=480)
        pk = librosa.util.peak_pick(on, pre_max=3, post_max=3, pre_avg=10, post_avg=10, delta=np.std(on) * 2.0, wait=10)
        t = pk * 480
        iso = [s for i, s in enumerate(t) if (i == 0 or s - t[i - 1] > 0.15 * SR) and s + int(0.6 * SR) < len(y)]
        rng = np.random.default_rng(0)
        if len(iso) > max_per:
            iso = sorted(rng.choice(iso, max_per, replace=False))
        for s in iso:
            notes.append(describe(yh[s - int(0.01 * SR): s + int(0.6 * SR)]))
        # pads: 1 s stretches of low onset strength with harmonic energy
        frames = np.arange(0, len(y) - SR, SR)
        rms = np.array([np.sqrt(np.mean(yh[f:f + SR] ** 2)) for f in frames])
        onr = np.array([on[int(f / 480):int((f + SR) / 480)].mean() for f in frames])
        good = frames[(rms > np.percentile(rms, 60)) & (onr < np.percentile(onr, 30))]
        for f in good[:: max(1, len(good) // 40)]:
            pads.append(pad_desc(yh[f:f + SR]))
    return np.array(notes), np.array(pads)


def pad_desc(x):
    global FB
    import librosa
    if FB is None:
        FB = mel_fb(SR, 2048)
    M = FB @ (np.abs(librosa.stft(x, n_fft=2048, hop_length=480)) ** 2)
    env = 10 * np.log10(M.mean(1) + 1e-12)
    env -= env.max()
    am = 20 * np.log10(np.std(M.sum(0)) / (np.mean(M.sum(0)) + 1e-12) + 1e-6)
    return np.concatenate([env / 10.0, [am / 20.0]])


def kmeans(X, k, it=50, seed=0):
    rng = np.random.default_rng(seed)
    C = X[rng.choice(len(X), k, replace=False)]
    for _ in range(it):
        lab = np.argmin(((X[:, None] - C[None]) ** 2).sum(-1), 1)
        C = np.stack([X[lab == j].mean(0) if (lab == j).any() else C[j] for j in range(k)])
    return C, lab


def candidates():
    """name -> (list of (preset, octave shift, gain dB), fx variant)"""
    one = ["celesta", "glock", "musicbox", "vibes", "marimba", "kalimba", "harp", "pizz", "piano", "crystal",
           "tinkerbell", "fmpiano", "nylon", "steeldrum", "harpsichord", "dulcimer"]
    c = {p: ([(p, 0, 0)], "dry") for p in one}
    c.update({f"{p}+soft": ([(p, 0, 0)], "soft") for p in ("celesta", "musicbox", "vibes", "marimba", "kalimba", "harp",
                                                         "piano", "fmpiano")})
    c.update({
        "celesta+musicbox": ([("celesta", 0, 0), ("musicbox", 0, -6)], "dry"),
        "celesta+vibes": ([("celesta", 0, 0), ("vibes", 0, -6)], "dry"),
        "kalimba+celesta": ([("kalimba", 0, 0), ("celesta", 12, -9)], "dry"),
        "harp+marimba": ([("harp", 0, 0), ("marimba", 0, -6)], "dry"),
        "piano+celesta8va": ([("piano", 0, 0), ("celesta", 12, -8)], "dry"),
        "marimba+kalimba": ([("marimba", 0, 0), ("kalimba", 0, -4)], "dry"),
        "fmpiano+celesta": ([("fmpiano", 0, 0), ("celesta", 0, -6)], "soft"),
        "pizz+harp": ([("pizz", 0, 0), ("harp", 0, -4)], "dry"),
        # soft synth plucks: a pluck doubled by a pad on the same notes (slow attack + long tail), big room
        "piano+warmpad": ([("piano", 0, 0), ("warmpad", 0, -4)], "room"),
        "harp+warmpad": ([("harp", 0, 0), ("warmpad", 0, -4)], "room"),
        "celesta+warmpad": ([("celesta", 0, 0), ("warmpad", 0, -4)], "room"),
        "harp+halopad": ([("harp", 0, 0), ("halopad", 0, -4)], "room"),
        "musicbox+halopad": ([("musicbox", 0, -2), ("halopad", 0, -4)], "room"),
        "piano+celesta8va+warmpad": ([("piano", 0, 0), ("celesta", 12, -8), ("warmpad", 0, -5)], "room"),
        "harp+fantasia": ([("harp", 0, 0), ("newage", 0, -6)], "room"),
        "piano+room": ([("piano", 0, 0)], "room"),
        "harp+room": ([("harp", 0, 0)], "room"),
        "celesta+room": ([("celesta", 0, 0)], "room"),
    })
    return c


EXTRA_P = {"tinkerbell": (0, 112), "fmpiano": (0, 5), "nylon": (0, 24), "steeldrum": (0, 114), "harpsichord": (0, 6),
           "dulcimer": (0, 15), "polysynth": (0, 90), "spacevoice": (0, 91), "sweeppad": (0, 95), "newage": (0, 88),
           "icerain": (0, 96), "soundtrack": (0, 97), "echodrops": (0, 102), "startheme": (0, 103)}
PADS = ["warmpad", "halopad", "fantasia", "slowstrings", "synthstrings", "bowedglass", "atmosphere", "choir",
        "polysynth", "spacevoice", "sweeppad", "soundtrack", "strings"]


def render(parts, keys, dur, fx, held=False):
    import pedalboard as pb
    from pipeline.audio.score import P
    from pipeline.audio.sf2 import Renderer
    r = Renderer()
    out = None
    for name, octv, gdb in parts:
        bank, prog = P.get(name) or EXTRA_P[name]
        ch = 9 if bank == 128 else 0
        ev = []
        for i, k in enumerate(keys):
            t = 0.0 if held else i * dur
            hold = len(keys) * dur if held else dur * (1.8 if fx == "room" else 0.9)
            ev += [(t, "on", ch, k + octv, 96), (t + hold, "off", ch, k + octv)]
        a = r.render(ev, len(keys) * dur if not held else dur, {ch: (bank, prog)}, tail=1.0)
        a *= 10 ** (gdb / 20)
        out = a if out is None else out[: len(a)] + a[: len(out)]
    chain = [pb.HighpassFilter(200)]
    if fx == "soft":
        chain += [pb.LowpassFilter(5500), pb.Chorus(rate_hz=0.4, depth=0.15, mix=0.25)]
    if fx == "room":  # long tail, softened top, a little chorus: the "soft synth" treatment
        chain += [pb.LowpassFilter(6500), pb.Chorus(rate_hz=0.3, depth=0.12, mix=0.2),
                  pb.Delay(delay_seconds=0.383, feedback=0.25, mix=0.15),
                  pb.Reverb(room_size=0.88, damping=0.5, wet_level=0.36, dry_level=0.8, width=1.0)]
    else:
        chain += [pb.Reverb(room_size=0.65, damping=0.45, wet_level=0.22, dry_level=0.85, width=1.0)]
    return pb.Pedalboard(chain)(out.T.astype(np.float32), SR).T


def main():
    out, clipdir = sys.argv[1], sys.argv[2]
    stems = sys.argv[3:]
    os.makedirs(clipdir, exist_ok=True)
    cache = out + ".refcache.npz"
    if os.path.exists(cache):
        z = np.load(cache)
        notes, pads = z["notes"], z["pads"]
    else:
        notes, pads = ref_events(stems)
        np.savez(cache, notes=notes, pads=pads)
    mu, sd = notes.mean(0), notes.std(0) + 1e-6
    C, lab = kmeans((notes - mu) / sd, 3)
    Craw = C * sd + mu
    clusters = []
    for j in range(3):
        c = Craw[j]
        clusters.append({"n": int((lab == j).sum()), "attack_ms": round(float(c[NM] * 50), 1),
                         "decay_db_per_s": round(float(c[NM + 1] * 40), 1), "flatness": round(float(c[NM + 2] / 5), 3),
                         "env_db_by_mel_band": [round(float(v * 10), 1) for v in c[:NM:4]]})
    keys = [84, 88, 91, 86]  # C6 E6 G6 D6: the median register of the reference note events
    res = {"n_note_events": int(len(notes)), "clusters": clusters, "notes": {}, "pads": {}}
    for name, (parts, fx) in candidates().items():
        a = render(parts, keys, 0.6, fx)
        ds = [describe(a[int(i * 0.6 * SR):int((i * 0.6 + 0.61) * SR)].mean(1)) for i in range(len(keys))]
        d = np.mean(ds, 0)
        dist = [round(float(np.sqrt((((d - Craw[j]) / sd) ** 2).mean())), 3) for j in range(3)]
        res["notes"][name] = {"dist_to_clusters": dist, "attack_ms": round(float(d[NM] * 50), 1),
                              "decay_db_per_s": round(float(d[NM + 1] * 40), 1)}
    pmu = pads.mean(0)
    psd = pads.std(0) + 1e-6
    for p in PADS:
        a = render([(p, 0, 0)], [50, 57, 62, 65], 2.5, "dry", held=True)
        dd = np.mean([pad_desc(a[int(s * SR):int((s + 1) * SR)].mean(1)) for s in (0.8, 1.4)], 0)
        res["pads"][p] = round(float(np.sqrt((((dd - pmu) / psd) ** 2).mean())), 3)
    for j in range(3):
        rank = sorted(res["notes"], key=lambda n: res["notes"][n]["dist_to_clusters"][j])
        res["clusters"][j]["closest"] = rank[:6]
    res["pads_ranked"] = sorted(res["pads"], key=res["pads"].get)
    # comparison clips: one phrase (arpeggio over a held pad) per top candidate
    phrase = [74, 81, 86, 88, 86, 81, 79, 83]
    for j in range(3):
        for name in res["clusters"][j]["closest"][:3]:
            parts, fx = candidates()[name]
            a = render(parts, phrase, 0.26, fx)
            pad = render([(res["pads_ranked"][0], 0, -10)], [50, 57, 62, 66], 2.4, "dry", held=True)
            n = min(len(a), len(pad))
            mix = a[:n] + pad[:n]
            mix /= np.abs(mix).max() + 1e-9
            sf.write(os.path.join(clipdir, f"c{j}_{name.replace('+', '_')}.wav"), (mix * 0.7).astype(np.float32), SR)
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps({"clusters": res["clusters"], "pads_ranked": res["pads_ranked"][:6]}, indent=1))


if __name__ == "__main__":
    main()
