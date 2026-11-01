"""Voice + music bed (sidechain-style ducking with lookahead) + SFX -> -14 LUFS stereo mix.

All in numpy at 48 kHz. Loudness is measured with pyloudnorm (BS.1770) and re-checked with
ffmpeg's ebur128 scanner (independent implementation, true peak).
"""
from __future__ import annotations

import os
import re
import subprocess

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy.ndimage import minimum_filter1d, uniform_filter1d
from scipy.signal import resample_poly

from .config import SFX_DB, SR, TARGET_LUFS, TRUE_PEAK_DB

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PUBLIC = os.path.join(ROOT, "studio", "public")
FRAME = 0.01  # 10 ms analysis frames for the ducking envelope

_meter = pyln.Meter(SR)


def db2lin(db):
    return 10 ** (db / 20)


def lufs(x: np.ndarray) -> float:
    if len(x) < int(0.5 * SR):
        x = np.pad(x, [(0, int(0.5 * SR) - len(x))] + [(0, 0)] * (x.ndim - 1))
    v = _meter.integrated_loudness(x)
    return float(v) if np.isfinite(v) else -70.0


def active_rms_db(x: np.ndarray) -> float:
    """RMS over the part of a sound within 30 dB of its peak (for short SFX)."""
    m = np.abs(x if x.ndim == 1 else x.mean(1))
    if m.max() == 0:
        return -120.0
    sel = m > m.max() * db2lin(-30)
    return 20 * np.log10(np.sqrt(np.mean((x if x.ndim == 1 else x.mean(1))[sel] ** 2)) + 1e-12)


def load(path: str) -> np.ndarray:
    """Load any audio file as float32 (n, ch) at 48 kHz (decodes non-wav with ffmpeg)."""
    if not path.lower().endswith((".wav", ".flac")):
        out = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-f", "f32le", "-ac", "2",
                              "-ar", str(SR), "-"], check=True, capture_output=True).stdout
        return np.frombuffer(out, np.float32).reshape(-1, 2).copy()
    x, sr = sf.read(path, dtype="float32", always_2d=True)
    if sr != SR:
        from math import gcd
        g = gcd(SR, sr)
        x = resample_poly(x, SR // g, sr // g, axis=0).astype(np.float32)
    return x


def find_asset(kind: str, name: str) -> str:
    """kind = music | sfx. A name, a path under studio/public, or an absolute path."""
    if os.path.isabs(name) and os.path.exists(name):
        return name
    for cand in (os.path.join(PUBLIC, name), *(os.path.join(PUBLIC, kind, name + ext) for ext in (".wav", ".m4a", ".ogg", ".mp3"))):
        if os.path.exists(cand):
            return cand
    raise FileNotFoundError(f"{kind} '{name}' not found under {PUBLIC}/{kind}/")


def speech_mask(voice: np.ndarray, hold=0.25):
    """Frame-level speech activity from the voice itself (the 'sidechain' signal)."""
    hop = int(FRAME * SR)
    n = len(voice) // hop + 1
    v = np.pad(voice, (0, n * hop - len(voice)))
    rms = np.sqrt(np.mean(v.reshape(n, hop) ** 2, axis=1) + 1e-12)
    db = 20 * np.log10(rms)
    active = (db > max(db.max() - 38, -55))
    # close short gaps between words so the bed doesn't pump inside a sentence
    k = int(hold / FRAME)
    act = active.copy()
    idx = np.nonzero(active)[0]
    for a, b in zip(idx[:-1], idx[1:]):
        if 1 < b - a <= k:
            act[a:b] = True
    return act


def duck_envelope(mask: np.ndarray, attack: float, release: float, lookahead: float) -> np.ndarray:
    """0..1 frame envelope: rises over `attack` starting `lookahead` before speech, falls over `release`."""
    la = int(lookahead / FRAME)
    m = mask.copy()
    if la:
        m[:-la] |= mask[la:]  # start ducking before the first syllable
    env = np.zeros(len(m))
    up = FRAME / max(attack, FRAME)
    down = FRAME / max(release, FRAME)
    e = 0.0
    for i, on in enumerate(m):
        e = min(1.0, e + up) if on else max(0.0, e - down)
        env[i] = e
    # smooth the linear ramps into S-curves
    return 0.5 - 0.5 * np.cos(np.pi * env)


def frames_to_samples(env: np.ndarray, n: int) -> np.ndarray:
    x = (np.arange(len(env)) + 0.5) * FRAME * SR
    return np.interp(np.arange(n), x, env).astype(np.float32)


def true_peak_db(x: np.ndarray) -> float:
    up = resample_poly(x, 4, 1, axis=0)
    return 20 * np.log10(np.abs(up).max() + 1e-12)


def limiter(x: np.ndarray, ceiling_db: float, look=0.005) -> np.ndarray:
    """Lookahead brickwall: min-filtered gain then a box smoother of half the window, so the
    smoothed gain never exceeds the gain each sample needs."""
    peak = np.abs(x).max(axis=1) if x.ndim == 2 else np.abs(x)
    need = np.minimum(1.0, db2lin(ceiling_db) / np.maximum(peak, 1e-9))
    w = max(2, int(look * SR))
    g = minimum_filter1d(need, size=2 * w + 1, mode="nearest")
    g = uniform_filter1d(g, size=w + 1 if w % 2 == 0 else w, mode="nearest")
    g = np.minimum(g, minimum_filter1d(need, size=3, mode="nearest"))
    return x * (g[:, None] if x.ndim == 2 else g)


def ffmpeg_loudness(path: str) -> dict:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    tail = r.stderr[r.stderr.rfind("Summary:"):]
    get = lambda k: float(re.search(rf"{k}:\s+(-?[\d.]+|-inf)", tail).group(1).replace("-inf", "-120"))
    return {"I_lufs": get("I"), "LRA_lu": get("LRA"), "true_peak_dbtp": get("Peak")}


def _sfx_bus(cues, total, log):
    """Unscaled mono sum of the SFX (only used as a sidechain key)."""
    if not cues:
        return None
    bus = np.zeros(total, np.float32)
    for c in cues:
        try:
            x = load(find_asset("sfx", c["cue"])).mean(1)
        except FileNotFoundError:
            continue
        i = int(round(c["at"] * SR))
        j = min(total, i + len(x))
        if j > i:
            bus[i:j] += x[: j - i]
    return bus


def mix(voice: np.ndarray, cues: list[dict], cfg: dict, music: str | None, out_dir: str, log=print) -> dict:
    n_voice = len(voice)
    fade_out = cfg.get("music_fade_out", 2.0)
    # length: voice + 0.4 s, extended so SFX tails (e.g. a final stinger) ring out, capped at max_tail
    cue_end = 0
    for c in cues:
        try:
            cue_end = max(cue_end, int((c["at"] + sf.info(find_asset("sfx", c["cue"])).duration) * SR))
        except Exception:
            pass
    total = min(max(n_voice + int(0.4 * SR), cue_end), n_voice + int(cfg.get("max_tail", 3.0) * SR))
    # --- voice: reference level -20 LUFS during the mix (headroom), stereo centre
    v_lufs = lufs(voice)
    vg = db2lin(-20.0 - v_lufs)
    v = np.zeros((total, 2), np.float32)
    v[:n_voice] = (voice * vg)[:, None]
    ref = -20.0
    # --- music bed, ducked under the voice
    m = np.zeros((total, 2), np.float32)
    duck_stats = {}
    env_s = None
    if music:
        bed = load(find_asset("music", music))
        reps = int(np.ceil(total / len(bed)))
        bed = np.tile(bed, (reps, 1))[:total]
        bed *= db2lin(ref + cfg["music_db"] - lufs(bed[: min(len(bed), 30 * SR)]))
        mask = speech_mask(voice)
        env = duck_envelope(mask, cfg["attack"], cfg["release"], cfg["lookahead"])
        env_s = frames_to_samples(env, n_voice)
        env_s = np.pad(env_s, (0, total - n_voice))
        gain_db = cfg["duck_db"] * env_s
        # SFX are a second, lighter sidechain so knocks/stingers punch through the bed
        sfx_bus = _sfx_bus(cues, total, log)
        if sfx_bus is not None and cfg.get("sfx_duck_db", 0):
            env_x = frames_to_samples(duck_envelope(speech_mask(sfx_bus, hold=0.1), 0.02, 0.35, 0.03), total)
            gain_db = gain_db + cfg["sfx_duck_db"] * env_x * (1 - env_s)
        else:
            env_x = np.zeros(total, np.float32)
        gain = db2lin(gain_db)
        t = np.arange(total) / SR
        fi = np.clip(t / max(cfg.get("music_fade_in", 1.0), 1e-3), 0, 1)
        fo = np.clip((total / SR - t) / max(fade_out, 1e-3), 0, 1)
        m = bed * (gain * fi * fo)[:, None]
        # measured duck depth: bed level in speech frames vs gap frames (for the report)
        sp = env_s > 0.95
        gp = (env_s < 0.05) & (env_x < 0.05)  # gaps with no voice and no SFX
        rms = lambda a: 20 * np.log10(np.sqrt(np.mean(a ** 2)) + 1e-12)
        if sp.any() and gp.any():
            duck_stats = {"music_rms_db_under_voice": round(rms(m[sp]), 2), "music_rms_db_in_gaps": round(rms(m[gp]), 2)}
            duck_stats["measured_duck_db"] = round(duck_stats["music_rms_db_under_voice"] - duck_stats["music_rms_db_in_gaps"], 2)
    # --- SFX
    s = np.zeros((total, 2), np.float32)
    placed = []
    for c in cues:
        try:
            x = load(find_asset("sfx", c["cue"])).mean(1)
        except FileNotFoundError as e:
            log(f"[mix] WARNING {e}")
            continue
        level = ref + SFX_DB.get(c["cue"], -6.0) + c.get("db", 0.0)
        x = x * db2lin(level - active_rms_db(x))
        i = int(round(c["at"] * SR))
        j = min(total, i + len(x))
        if j <= i:
            continue
        s[i:j] += x[: j - i, None]
        placed.append({**c, "dur": round(len(x) / SR, 3), "level_db": round(level - ref, 1)})
    # --- gentle 0.8 s fade on music + sfx at the very end (voice has finished by then)
    fl = min(total, int(0.8 * SR))
    s[total - fl:] *= np.linspace(1, 0, fl)[:, None] ** 2
    m[total - fl:] *= np.linspace(1, 0, fl)[:, None] ** 2
    # --- sum, normalise to target, limit, iterate
    pre = v + m + s
    g = db2lin(TARGET_LUFS - lufs(pre))
    ceiling = TRUE_PEAK_DB - 0.6
    for _ in range(6):
        out = limiter(pre * g, ceiling)
        err = TARGET_LUFS - lufs(out)
        tp = true_peak_db(out)
        if abs(err) < 0.2 and tp <= TRUE_PEAK_DB:
            break
        if tp > TRUE_PEAK_DB:
            ceiling -= tp - TRUE_PEAK_DB + 0.1
        g *= db2lin(err)
    os.makedirs(out_dir, exist_ok=True)
    paths = {k: os.path.join(out_dir, f"{k}.wav") for k in ("mix", "voice", "music", "sfx")}
    sf.write(paths["mix"], out, SR, subtype="PCM_24")
    sf.write(paths["voice"], v[:, 0] * g, SR, subtype="PCM_24")
    sf.write(paths["music"], m * g, SR, subtype="PCM_24")
    sf.write(paths["sfx"], s * g, SR, subtype="PCM_24")
    if env_s is not None:
        np.save(os.path.join(out_dir, "duck_env.npy"), env_s[:: int(FRAME * SR)])
    meas = ffmpeg_loudness(paths["mix"])
    rep = {
        "target_lufs": TARGET_LUFS, "pyloudnorm_lufs": round(lufs(out), 2), "true_peak_dbtp_4x": round(true_peak_db(out), 2),
        "ffmpeg_ebur128": meas, "duration_s": round(total / SR, 3), "music": music, "sfx_placed": placed, **duck_stats,
    }
    log(f"[mix] {meas['I_lufs']} LUFS (ffmpeg), TP {meas['true_peak_dbtp']} dBTP, LRA {meas['LRA_lu']}, "
        f"duck {duck_stats.get('measured_duck_db')} dB, {len(placed)} sfx")
    return {"paths": paths, "report": rep}
