"""Measure an A/B pair of mixes (old bed vs new score) built by pipeline.audio.make from the same voice and SFX.

Checks what can be verified without listening: loudness and true peak, clipping, the voice-to-music gap under speech
(full range and through a phone-speaker model), masking in the voice's 1-4 kHz band, music dynamics, silence gaps,
cue timing against setting changes and reveal words (planned vs measured onsets in the music stem), drop-out depth,
and the loop seam.

usage (Spark, ~/studio/.venv): python research/music/tools/measure_ab.py A_dir B_dir storyboard.json out.json [out.png]
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy.signal import butter, sosfilt, stft

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from pipeline.episodes import settings as S  # noqa: E402

SR = 48000
HOP = 0.1


def rd(p):
    x, sr = sf.read(p, dtype="float64", always_2d=True)
    assert sr == SR, (p, sr)
    return x


def kw(x):
    m = pyln.Meter(SR)
    y = x.copy()
    for f in m._filters.values():
        y = f.apply_filter(y)
    return y


def lane(x, win=0.4):
    """momentary-style loudness every HOP s (centred window `win`)"""
    p = (kw(x) ** 2).sum(1)
    h = int(HOP * SR)
    n = len(p) // h
    e = p[: n * h].reshape(n, h).mean(1)
    k = max(1, int(win / HOP))
    from scipy.ndimage import uniform_filter1d
    return -0.691 + 10 * np.log10(uniform_filter1d(e, k, mode="nearest") + 1e-12)


def phone(x):
    """small phone speaker: nothing under ~350 Hz (2nd-order), soft top above 9 kHz, a 2-4 kHz bump"""
    sos = np.vstack([butter(2, 350, "highpass", fs=SR, output="sos"), butter(2, 9000, "lowpass", fs=SR, output="sos")])
    y = sosfilt(sos, x, axis=0)
    b = butter(2, [2000, 4000], "bandpass", fs=SR, output="sos")
    return y + 0.4 * sosfilt(b, y, axis=0)


def band_db(x, lo, hi):
    f, _, Z = stft(x.mean(1), fs=SR, nperseg=2048, noverlap=2048 - int(HOP * SR))
    P = (np.abs(Z) ** 2)[(f >= lo) & (f < hi)].sum(0)
    return 10 * np.log10(P + 1e-12)


def speech_mask(v):
    l = lane(v, 0.1)
    ref = np.percentile(l, 95)
    return (l > ref - 25) & (l > -60)


def measure(d, sb, plan=None):
    v, m, s, mx = (rd(os.path.join(d, f"{k}.wav")) for k in ("voice", "music", "sfx", "mix"))
    v = np.repeat(v, 2, axis=1) if v.shape[1] == 1 else v
    n = min(len(v), len(m), len(mx))
    v, m, s, mx = v[:n], m[:n], s[:n], mx[:n]
    T = n / SR
    sp = speech_mask(v)
    vl, ml = lane(v), lane(m)
    k = min(len(sp), len(vl), len(ml))
    sp, vl, ml = sp[:k], vl[:k], ml[:k]
    t = (np.arange(k) + 0.5) * HOP
    meter = pyln.Meter(SR)
    out = {"dir": d, "duration_s": round(T, 2)}
    out["mix_integrated_lufs"] = round(meter.integrated_loudness(mx), 2)
    up = np.abs(np.concatenate([mx[:, 0], mx[:, 1]]))
    out["mix_sample_peak_dbfs"] = round(20 * np.log10(up.max()), 2)
    out["clipped_samples"] = int((up >= 0.999).sum())
    out["nan"] = int(np.isnan(mx).sum())
    gap = vl[sp] - ml[sp]
    out["voice_minus_music_under_speech_lu"] = {"p10": round(float(np.percentile(gap, 10)), 1),
                                                 "median": round(float(np.median(gap)), 1),
                                                 "p90": round(float(np.percentile(gap, 90)), 1)}
    pv, pm = lane(phone(v))[:k], lane(phone(m))[:k]
    pg = pv[sp] - pm[sp]
    out["phone_voice_minus_music_under_speech_lu"] = {"p10": round(float(np.percentile(pg, 10)), 1),
                                                       "median": round(float(np.median(pg)), 1),
                                                       "p90": round(float(np.percentile(pg, 90)), 1)}
    out["phone_music_audible_share"] = round(float(np.mean(pm[sp] > pv[sp] - 20)), 3)  # within 20 LU of the voice
    vb, mb = band_db(v, 1000, 4000), band_db(m, 1000, 4000)
    kk = min(len(vb), len(mb), k)
    out["voice_band_1_4k_snr_db_median"] = round(float(np.median((vb[:kk] - mb[:kk])[sp[:kk]])), 1)
    st = lane(m, 3.0)[:k]
    out["music_short_term_p10_p95"] = [round(float(np.percentile(st, 10)), 1), round(float(np.percentile(st, 95)), 1)]
    out["music_short_term_range_db"] = round(out["music_short_term_p10_p95"][1] - out["music_short_term_p10_p95"][0], 1)
    # silence: 200 ms mix windows under -45 LUFS (dead air), music-stem windows under -60 (outside planned drop-outs)
    ml2 = lane(mx, 0.2)[:k]
    out["mix_dead_air_windows"] = [round(float(x), 1) for x in t[ml2 < -45]]
    drops = (plan or {}).get("drops", [])
    in_drop = np.zeros(k, bool)
    for dd in drops:
        in_drop |= (t >= dd["t0"] - 0.1) & (t <= dd["t1"] + 0.3)
    mq = lane(m, 0.2)[:k]
    quiet = (mq < -60) & ~in_drop & (t > 0.3) & (t < T - 0.3)
    out["music_silent_windows_outside_dropouts"] = [round(float(x), 1) for x in t[quiet]]
    # transitions: music level in +-0.6 s of each setting change vs median under speech
    tl = S.timeline(sb)
    changes = [r["t0"] for r in tl[1:] if r["t0"] < T - 0.5]
    near = np.zeros(k, bool)
    for c in changes:
        near |= np.abs(t - c) <= 0.6
    out["music_at_setting_changes_minus_under_speech_db"] = round(float(np.median(ml[near]) - np.median(ml[sp & ~near])), 1)
    # loop seam: music and mix RMS of the last vs first 200 ms, and the sample step across the seam
    w = int(0.2 * SR)
    r = lambda a: 20 * np.log10(np.sqrt(np.mean(a ** 2)) + 1e-12)
    out["seam"] = {"music_last_200ms_db": round(r(m[-w:]), 1), "music_first_200ms_db": round(r(m[:w]), 1),
                   "mix_last_200ms_db": round(r(mx[-w:]), 1), "mix_first_200ms_db": round(r(mx[:w]), 1),
                   "mix_sample_step": round(float(np.abs(mx[-1] - mx[0]).max()), 4),
                   "mix_typical_sample_step": round(float(np.median(np.abs(np.diff(mx[:, 0])))), 4)}
    return out, {"t": t, "vl": vl, "ml": ml, "sp": sp, "m": m, "changes": changes}


def timing(plan, m, sb, words):
    """planned score events vs the audio: low-band onsets in the music stem near cue starts and stings"""
    f, tt, Z = stft(m.mean(1), fs=SR, nperseg=1024, noverlap=1024 - 240)  # 5 ms hop
    low = 10 * np.log10((np.abs(Z) ** 2)[(f >= 30) & (f < 250)].sum(0) + 1e-12)
    flux = np.maximum(0, np.diff(low, prepend=low[0]))

    def onset_near(t0, win=0.15):
        sel = (tt >= t0 - win) & (tt <= t0 + win)
        if not sel.any():
            return None
        i = np.argmax(flux[sel])
        return round(float(tt[sel][i] - t0), 3), round(float(flux[sel][i]), 1)

    tl = S.timeline(sb)
    changes = [r["t0"] for r in tl[1:]]
    res = {"cues": [], "stings": [], "drops": [], "risers": []}
    for c in plan["cues"][1:]:
        dch = min(changes, key=lambda x: abs(x - c["t0"])) if changes else None
        res["cues"].append({"t0": round(c["t0"], 3), "mood": c["mood"], "to_setting_change_s": round(c["t0"] - dch, 3),
                            "onset": onset_near(c["t0"])})
    starts = np.array([w["start"] for w in words])
    for s in plan["stings"]:
        i = int(np.argmin(np.abs(starts - s["t"])))
        res["stings"].append({"t": s["t"], "why": s["why"], "word": words[i]["text"],
                              "to_word_start_s": round(s["t"] - 0.03 - starts[i], 3), "onset": onset_near(s["t"] - 0.03)})
    ml = lane(m, 0.2)
    for dd in plan["drops"]:
        i0, i1 = int(dd["t0"] / HOP), int(dd["t1"] / HOP)
        before = np.median(ml[max(0, i0 - 15):i0 - 1])
        res["drops"].append({**dd, "depth_db": round(float(before - np.min(ml[i0:i1 + 1])), 1)})
    for rz in plan["risers"]:
        i0, i1 = int(rz["t0"] / HOP), int(rz["t1"] / HOP)
        res["risers"].append({**rz, "rise_db": round(float(np.max(lane(m, 0.4)[i1 - 3:i1 + 1]) - lane(m, 0.4)[i0]), 1)})
    return res


def main():
    A, B, sbp, outp = sys.argv[1:5]
    png = sys.argv[5] if len(sys.argv) > 5 else None
    sb = json.load(open(sbp))
    plan = json.load(open(os.path.join(B, "score_plan.json")))
    words = json.load(open(os.path.join(B, "captions.json")))["words"]
    ra, la = measure(A, sb)
    rb, lb = measure(B, sb, plan)
    res = {"A_bed": ra, "B_score": rb, "B_timing": timing(plan, lb["m"], sb, words)}
    json.dump(res, open(outp, "w"), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != "B_timing"}, indent=1))
    print(json.dumps(res["B_timing"], indent=1))
    if png:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(3, 1, figsize=(22, 10), sharex=True)
        labs = (os.environ.get("AB_LABEL_A", "A: deep_ocean bed"), os.environ.get("AB_LABEL_B", "B: score"))
        for a_, (lab, l) in zip(ax[:2], ((labs[0], la), (labs[1], lb))):
            a_.plot(l["t"], l["vl"], color="#58a6ff", lw=0.6, label="voice M")
            a_.plot(l["t"], l["ml"], color="#f0883e", lw=0.9, label="music M")
            for c in l["changes"]:
                a_.axvline(c, color="#2ea043", lw=1)
            a_.set_ylim(-60, -5)
            a_.set_title(lab + " (green = setting change)")
            a_.legend(loc="lower left", fontsize=7)
            a_.grid(alpha=0.2)
        for c in plan["cues"]:
            ax[1].axvline(c["t0"], color="#a371f7", ls="--", lw=1)
            ax[1].text(c["t0"] + 0.2, -8, f"{c['mood']}{c['intensity']}", fontsize=8, color="#a371f7")
        for s in plan["stings"]:
            ax[1].plot([s["t"]], [-12], "v", color="#f85149")
        for d in plan["drops"]:
            ax[1].axvspan(d["t0"], d["t1"], color="#f85149", alpha=0.3)
        for r in plan["risers"]:
            ax[1].annotate("", xy=(r["t1"], -15), xytext=(r["t0"], -15), arrowprops=dict(arrowstyle="->", color="#d29922"))
        m = lb["m"].mean(1)
        f, tt, Z = stft(m, fs=SR, nperseg=4096, noverlap=4096 - 2400)
        sel = (f > 25) & (f < 8000)
        ax[2].pcolormesh(tt, f[sel], 20 * np.log10(np.abs(Z[sel]) + 1e-9), shading="auto", vmin=-110, vmax=-30, cmap="magma")
        ax[2].set_yscale("log")
        ax[2].set_ylim(30, 8000)
        ax[2].set_title("B score music stem, spectrogram 30 Hz - 8 kHz")
        ax[2].set_xticks(np.arange(0, lb["t"][-1] + 1, 2))
        fig.tight_layout()
        fig.savefig(png, dpi=60)


if __name__ == "__main__":
    main()
