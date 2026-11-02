"""Voice processing for an audio profile (config.PROFILES): pause tightening at TTS time and a mix-time voice chain.

Both are opt-in: nothing here runs unless the episode's profile sets `tighten_gaps` / `voice_fx` (the explainer and
horror niches never do). Targets for the story lane come from research/music/RICKS_SOUND.md (RicksClips3000 voices:
speech gaps >= 120 ms about once a minute, crest ~12 dB, momentary spread ~5.5 LU, little energy under 100 Hz, air
above 8 kHz about 14 dB under the total).

  tighten(audio, words, cues, spec)   shortens silent runs between words to spec["max_gap"] s (default 0.10) with
                                      10 ms cross-fades and moves every later word and cue by the time removed; runs
                                      right after TTS, before the timings are cached, so captions and the storyboard
                                      are built on the tightened voice
  process(audio, spec)                mono float32 at config.SR -> same length: high-pass, EQ, two-stage compression
                                      (fast peak control + slow levelling), an "air" exciter that adds harmonics
                                      above 8 kHz (Kokoro renders at 24 kHz, so there is nothing above 12 kHz to lift)
"""
from __future__ import annotations

import numpy as np

from .config import SR


def _frames_db(x: np.ndarray, hop: int) -> np.ndarray:
    n = len(x) // hop
    r = np.sqrt(np.mean(x[: n * hop].reshape(n, hop) ** 2, axis=1) + 1e-12)
    return 20 * np.log10(r)


def tighten(audio: np.ndarray, words: list[dict], cues: list[dict], spec: dict) -> tuple[np.ndarray, list, list, dict]:
    """Silent runs (10 ms frames > `floor_db` under the 95th-percentile frame, longer than max_gap) are cut down to
    max_gap, keeping half of it on each side. Returns (audio, words, cues, stats)."""
    max_gap = float(spec.get("max_gap", 0.10))
    floor = float(spec.get("floor_db", 35.0))
    hop = int(0.01 * SR)
    db = _frames_db(audio, hop)
    if len(db) == 0:
        return audio, words, cues, {"removed_s": 0.0, "gaps": 0}
    quiet = db < np.percentile(db, 95) - floor
    # runs of quiet frames
    m = np.concatenate([[False], quiet, [False]]).astype(int)
    d = np.diff(m)
    runs = list(zip(np.nonzero(d == 1)[0], np.nonzero(d == -1)[0]))
    keep_half = max_gap / 2
    cuts = []  # (start sample, end sample) removed
    for a, b in runs:
        t0, t1 = a * hop / SR, b * hop / SR
        if t1 - t0 <= max_gap or a == 0 or b >= len(db) - 1:   # leave the head and the tail alone
            continue
        cuts.append((int((t0 + keep_half) * SR), int((t1 - keep_half) * SR)))
    if not cuts:
        return audio, words, cues, {"removed_s": 0.0, "gaps": 0}
    xf = int(0.01 * SR)
    out, pos = [], 0
    for c0, c1 in cuts:
        seg = audio[pos:c0].copy()
        if out and len(seg) > xf:  # cross-fade into the previous piece
            prev = out[-1]
            ramp = np.linspace(0, 1, xf, dtype=np.float32)
            prev[-xf:] = prev[-xf:] * (1 - ramp) + seg[:xf] * ramp
            seg = seg[xf:]
        out.append(seg)
        pos = c1
    tail = audio[pos:].copy()
    if out and len(tail) > xf:
        ramp = np.linspace(0, 1, xf, dtype=np.float32)
        out[-1][-xf:] = out[-1][-xf:] * (1 - ramp) + tail[:xf] * ramp
        tail = tail[xf:]
    out.append(tail)
    new = np.concatenate(out).astype(np.float32)
    # time map: removed seconds before t (each cut also loses one cross-fade)
    starts = np.array([c0 / SR for c0, _ in cuts])
    lens = np.array([(c1 - c0 + xf) / SR for c0, c1 in cuts])

    def remap(t):
        if t is None:
            return None
        k = np.searchsorted(starts, t, side="right")
        shift = lens[:k].sum()
        # a time inside a removed span lands on the cut point
        if k and t < starts[k - 1] + lens[k - 1]:
            return round(float(starts[k - 1] - lens[: k - 1].sum()), 3)
        return round(float(max(0.0, t - shift)), 3)

    words = [{**w, "start": remap(w["start"]), "end": remap(w.get("end"))} for w in words]
    cues = [{**c, "at": remap(c["at"])} for c in cues]
    return new, words, cues, {"removed_s": round(float(lens.sum()), 3), "gaps": len(cuts),
                              "duration_before_s": round(len(audio) / SR, 3), "duration_after_s": round(len(new) / SR, 3)}


def exciter(x: np.ndarray, spec: dict) -> np.ndarray:
    """harmonics from the 4-8 kHz band folded above `hp_out` Hz, added at `db` relative to the input"""
    from scipy.signal import butter, sosfilt
    lo = sosfilt(butter(2, float(spec.get("hp_in", 3500)), "highpass", fs=SR, output="sos"), x)
    drive = float(spec.get("drive", 6.0))
    sat = np.tanh(drive * lo / (np.abs(lo).max() + 1e-9)) * (np.abs(lo).max() + 1e-9) / drive
    hi = sosfilt(butter(4, float(spec.get("hp_out", 8500)), "highpass", fs=SR, output="sos"), sat)
    return (x + hi * 10 ** (float(spec.get("db", 0.0)) / 20)).astype(np.float32)


def process(audio: np.ndarray, spec: dict) -> np.ndarray:
    """spec: {"hpf": Hz, "hpf_order": 2|4, "eq": [[Hz, dB, Q], ...], "high_shelf": [Hz, dB],
              "comp": {threshold_db, ratio, attack_ms, release_ms, mix}, "level": {...same keys...},
              "limit": {threshold_db, release_ms}, "air": {hp_in, drive, hp_out, db}}
    dB values assume the voice at -20 LUFS (it is levelled there first)."""
    if not spec:
        return audio
    import pedalboard as pb
    from scipy.signal import butter, sosfilt
    n = len(audio)
    x = audio.astype(np.float32)
    # thresholds are set for a voice at -20 LUFS (the level mix.py puts it at); the mix re-levels afterwards
    import pyloudnorm as pyln
    lv = pyln.Meter(SR).integrated_loudness(x.astype(np.float64))
    if np.isfinite(lv):
        x = x * np.float32(10 ** ((-20.0 - lv) / 20))
    if spec.get("hpf"):
        x = sosfilt(butter(int(spec.get("hpf_order", 2)), float(spec["hpf"]), "highpass", fs=SR, output="sos"), x)
    eq = [pb.PeakFilter(float(f), float(g), float(q)) for f, g, q in spec.get("eq", [])]
    if spec.get("high_shelf"):
        eq.append(pb.HighShelfFilter(float(spec["high_shelf"][0]), float(spec["high_shelf"][1]), 0.7))
    if eq:
        x = pb.Pedalboard(eq)(x[None, :].astype(np.float32), SR)[0]
    for k in ("comp", "level"):
        c = spec.get(k)
        if c:  # "mix" < 1: parallel compression (keeps some of the phrase-level dynamics)
            y = pb.Pedalboard([pb.Compressor(threshold_db=float(c["threshold_db"]), ratio=float(c["ratio"]),
                                             attack_ms=float(c["attack_ms"]), release_ms=float(c["release_ms"]))])(
                x[None, :].astype(np.float32), SR)[0]
            mix = float(c.get("mix", 1.0))
            if mix < 1.0:  # match the compressed path's level to the dry one before blending
                y = y * np.float32(np.sqrt(np.mean(x ** 2) / (np.mean(y ** 2) + 1e-12)))
            x = (mix * y + (1 - mix) * x).astype(np.float32)
    if spec.get("limit"):  # peak limiter for consonant transients (crest factor), on the voice re-levelled to -20 LUFS
        lv = pyln.Meter(SR).integrated_loudness(x.astype(np.float64))
        if np.isfinite(lv):
            x = x * np.float32(10 ** ((-20.0 - lv) / 20))
        x = pb.Pedalboard([pb.Limiter(threshold_db=float(spec["limit"]["threshold_db"]),
                                      release_ms=float(spec["limit"].get("release_ms", 40)))])(
            x[None, :].astype(np.float32), SR)[0]
    if spec.get("air"):
        x = exciter(x, spec["air"])
    x = np.asarray(x, np.float32)[:n]
    return np.pad(x, (0, n - len(x)))
