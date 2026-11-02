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

from .config import MUSIC_BEDS, SCORE, SFX_DB, SR, TARGET_LUFS, TRUE_PEAK_DB

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


def music_name(name: str) -> str:
    """'deep_ocean', 'music/deep_ocean.m4a' -> 'deep_ocean' (the bed's allowlist key)."""
    return os.path.splitext(os.path.basename(str(name).strip()))[0]


def find_asset(kind: str, name: str) -> str:
    """kind = music | sfx. sfx: a name, a path under studio/public, or an absolute path. music: only an in-house
    bed from config.MUSIC_BEDS (by name), looked up under studio/public/music/."""
    if kind == "music":
        bed = music_name(name)
        if bed == SCORE:
            raise FileNotFoundError("music 'score' is composed per episode (pipeline.audio.score via mix(score_fn=...)), "
                                    "not a file")
        if bed not in MUSIC_BEDS or os.path.isabs(str(name)) or ".." in str(name):
            raise FileNotFoundError(f"music {name!r} is not an in-house bed {MUSIC_BEDS} (no third-party or absolute-path "
                                    f"music: it can be Content ID claimed on Shorts over 60 s)")
        for ext in (".wav", ".m4a", ".ogg", ".mp3"):
            cand = os.path.join(PUBLIC, "music", bed + ext)
            if os.path.exists(cand):
                return cand
        raise FileNotFoundError(f"music '{bed}' not found under {PUBLIC}/music/ (run python -m pipeline.audio.synth)")
    if os.path.isabs(name) and os.path.exists(name):
        return name
    for cand in (os.path.join(PUBLIC, name), *(os.path.join(PUBLIC, kind, name + ext) for ext in (".wav", ".m4a", ".ogg", ".mp3"))):
        if os.path.exists(cand):
            return cand
    raise FileNotFoundError(f"{kind} '{name}' not found under {PUBLIC}/{kind}/")


def last_voiced(voice: np.ndarray, floor_db=-40.0) -> int:
    """Sample index just after the last 10 ms frame within floor_db of the voice's loudest frame."""
    hop = int(FRAME * SR)
    n = len(voice) // hop
    if n == 0:
        return len(voice)
    rms = np.sqrt(np.mean(voice[: n * hop].reshape(n, hop) ** 2, axis=1) + 1e-12)
    db = 20 * np.log10(rms)
    idx = np.nonzero(db > db.max() + floor_db)[0]
    return int((idx[-1] + 1) * hop) if len(idx) else len(voice)


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


def max_momentary(x: np.ndarray) -> float:
    """Loudest 400 ms window (BS.1770 momentary loudness, 100 ms hop) of a short sound."""
    w, hop = int(0.4 * SR), int(0.1 * SR)
    if len(x) <= w:
        return lufs(x)
    vals = [lufs(x[i:i + w]) for i in range(0, len(x) - w, hop)]
    return max(vals) if vals else -70.0


def hush_gain(cues, total, cfg):
    """Music gain (linear, per sample) that drops the bed to near silence for `hush` s before featured cues
    (cue["hush"] from the script marker, else cfg["hush"][cue]), holds it through the hit and recovers after."""
    g = np.ones(total, np.float32)
    floor = db2lin(cfg.get("hush_db", -32.0))
    for c in cues:
        h = float(c.get("hush", cfg.get("hush", {}).get(c["cue"], 0.0)))
        if h <= 0:
            continue
        try:
            dur = sf.info(find_asset("sfx", c["cue"])).duration
        except Exception:
            dur = 1.0
        t = np.arange(total) / SR
        a0, a1 = c["at"] - h - 0.12, c["at"] - h       # fade down
        b0, b1 = c["at"] + 0.6 * dur, c["at"] + 0.6 * dur + 1.2  # hold through the hit, then recover
        env = np.ones(total, np.float32)
        env = np.where(t >= a0, 1 - (1 - floor) * np.clip((t - a0) / (a1 - a0), 0, 1), env)
        env = np.where(t >= b0, floor + (1 - floor) * np.clip((t - b0) / (b1 - b0), 0, 1), env)
        g = np.minimum(g, env.astype(np.float32))
    return g


def _rate(x: np.ndarray, rate) -> np.ndarray:
    """pitch/speed variant of a cue (tape-style resample; rate 1 = unchanged), so repeated hits never sound stamped"""
    r = float(rate or 1.0)
    if abs(r - 1.0) < 1e-3 or len(x) < 2:
        return x
    n = max(2, int(len(x) / r))
    return np.interp(np.arange(n) * r, np.arange(len(x)), x).astype(np.float32)


def _sfx_bus(cues, total, log):
    """Unscaled mono sum of the SFX (only used as a sidechain key)."""
    if not cues:
        return None
    bus = np.zeros(total, np.float32)
    for c in cues:
        try:
            x = _rate(load(find_asset("sfx", c["cue"])).mean(1), c.get("rate", 1.0))
        except FileNotFoundError:
            continue
        i = int(round(c["at"] * SR))
        j = min(total, i + len(x))
        if j > i:
            bus[i:j] += x[: j - i]
    return bus


def mix(voice: np.ndarray, cues: list[dict], cfg: dict, music: str | None, out_dir: str, log=print,
        score_fn=None) -> dict:
    """score_fn(seconds, loop) -> {"audio": (n, 2) float32, "provenance": {...}, "plan": {...}} composes the bed when
    music is config.SCORE (pipeline.audio.make builds it from the storyboard)."""
    if cfg.get("voice_fx"):  # profile voice chain (pipeline/audio/voicefx.py); niches without one are unchanged
        from .voicefx import process
        voice = process(voice, cfg["voice_fx"])
    sfx_db = {**SFX_DB, **cfg.get("sfx_db", {})}
    sfx_rate = cfg.get("sfx_rate", {})
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
    if cfg.get("loop_tail") is not None:  # loop ending: last voiced sample + loop_tail (ignores the padded TTS tail)
        total = min(n_voice, last_voiced(voice) + int(float(cfg["loop_tail"]) * SR))
        voice = voice[:total]
        n_voice = total
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
    provenance, score_plan = None, None
    is_score = bool(music) and music_name(music) == SCORE
    loop = cfg.get("loop_tail") is not None
    if music:
        if is_score:
            if score_fn is None:
                raise ValueError("music 'score' needs score_fn (pipeline.audio.make passes one when a storyboard exists)")
            sc = score_fn(total / SR, loop)
            bed = sc["audio"][:total]
            bed = np.pad(bed, ((0, total - len(bed)), (0, 0)))
            provenance, score_plan = sc["provenance"], sc["plan"]
            bed_lufs = lufs(bed)  # the whole score: its cues have their own dynamics
        else:
            bed = load(find_asset("music", music))
            reps = int(np.ceil(total / len(bed)))
            bed = np.tile(bed, (reps, 1))[:total]
            bed_lufs = lufs(bed[: min(len(bed), 30 * SR)])
        bed *= db2lin(ref + cfg["music_db"] - bed_lufs)
        mask = speech_mask(voice)
        env = duck_envelope(mask, cfg["attack"], cfg["release"], cfg["lookahead"])
        env_s = frames_to_samples(env, n_voice)
        env_s = np.pad(env_s, (0, total - n_voice))
        gain_db = cfg["duck_db"] * env_s
        # SFX are a second, lighter sidechain so knocks/stingers punch through the bed
        sfx_bus = _sfx_bus([{**c, "rate": float(c.get("rate") or 1.0) * float(sfx_rate.get(c["cue"], 1.0))} for c in cues],
                           total, log)
        if sfx_bus is not None and cfg.get("sfx_duck_db", 0):
            env_x = frames_to_samples(duck_envelope(speech_mask(sfx_bus, hold=0.1), 0.02, 0.35, 0.03), total)
            gain_db = gain_db + cfg["sfx_duck_db"] * env_x * (1 - env_s)
        else:
            env_x = np.zeros(total, np.float32)
        gain = db2lin(gain_db)
        t = np.arange(total) / SR
        # a looping score is continuous across the replay seam (its tail is wrapped onto bar 1): only 10 ms anti-click
        fi = np.clip(t / max(0.01 if (is_score and loop) else cfg.get("music_fade_in", 1.0), 1e-3), 0, 1)
        fo = np.clip((total / SR - t) / max(0.01 if (is_score and loop) else fade_out, 1e-3), 0, 1)
        m = bed * (gain * fi * fo * hush_gain(cues, total, cfg))[:, None]
        bd = cfg.get("duck_band")
        if bd:  # band duck (dynamic EQ): the voice's 1-4 kHz pocket opens further in the music while it talks
            from scipy.signal import butter, sosfiltfilt
            sos = butter(2, [bd.get("lo", 1000), bd.get("hi", 4000)], "bandpass", fs=SR, output="sos")
            band = sosfiltfilt(sos, m, axis=0).astype(np.float32)
            m = m + band * (db2lin(float(bd["db"]) * env_s) - 1.0)[:, None]
        # measured duck depth: bed level in speech frames vs gap frames (for the report)
        sp = env_s > 0.95
        gp = (env_s < 0.05) & (env_x < 0.05)  # gaps with no voice and no SFX
        rms = lambda a: 20 * np.log10(np.sqrt(np.mean(a ** 2)) + 1e-12)
        if sp.any() and gp.any():
            duck_stats = {"music_rms_db_under_voice": round(rms(m[sp]), 2), "music_rms_db_in_gaps": round(rms(m[gp]), 2)}
            duck_stats["measured_duck_db"] = round(duck_stats["music_rms_db_under_voice"] - duck_stats["music_rms_db_in_gaps"], 2)
            # how far the bed sits under the narration while it talks (voice RMS vs bed RMS, same speech frames)
            duck_stats["bed_below_voice_db"] = round(rms(v[:, 0][sp]) - duck_stats["music_rms_db_under_voice"], 2)
    # --- SFX
    s = np.zeros((total, 2), np.float32)
    placed = []
    for c in cues:
        try:
            x = load(find_asset("sfx", c["cue"])).mean(1)
        except FileNotFoundError as e:
            log(f"[mix] WARNING {e}")
            continue
        x = _rate(x, float(c.get("rate") or 1.0) * float(sfx_rate.get(c["cue"], 1.0)))
        sq = cfg.get("sfx_squash", {}).get(c["cue"], 0)
        if sq:  # pre-limit the transients (dB) so a featured hit can be loud without slamming the true-peak ceiling
            x = limiter((x / (np.abs(x).max() + 1e-9))[:, None], -float(sq))[:, 0]
        loud = cfg.get("sfx_momentary", {})
        if c["cue"] in loud:  # featured hit: set by its loudest 400 ms (momentary LUFS) relative to the voice
            level = ref + loud[c["cue"]] + c.get("db", 0.0)
            x = x * db2lin(level - max_momentary(x))
        else:
            level = ref + sfx_db.get(c["cue"], -6.0) + c.get("db", 0.0)
            x = x * db2lin(level - active_rms_db(x))
        i = int(round(c["at"] * SR))
        j = min(total, i + len(x))
        if j <= i:
            continue
        s[i:j] += x[: j - i, None]
        placed.append({**c, "dur": round(len(x) / SR, 3), "level_db": round(level - ref, 1)})
    # --- gentle 0.8 s fade on music + sfx at the very end (voice has finished by then); loop endings: end_fade
    fl = min(total, max(1, int(float(cfg.get("end_fade", 0.8)) * SR)))
    s[total - fl:] *= np.linspace(1, 0, fl)[:, None] ** 2
    if not (is_score and loop):
        m[total - fl:] *= np.linspace(1, 0, fl)[:, None] ** 2
    # --- sum, normalise to target, limit, iterate
    pre = v + m + s
    g = db2lin(TARGET_LUFS - lufs(pre))
    # cfg true_peak_db: a lower ceiling for mixes whose transients overshoot in the AAC encode (score timpani/booms:
    # -1.2 dBTP in the wav measured -0.5 dBTP in the muxed MP4 on the orca A/B)
    tp_max = float(cfg.get("true_peak_db", TRUE_PEAK_DB))
    ceiling = tp_max - 0.6
    for _ in range(6):
        out = limiter(pre * g, ceiling)
        err = TARGET_LUFS - lufs(out)
        tp = true_peak_db(out)
        if abs(err) < 0.2 and tp <= tp_max:
            break
        if tp > tp_max:
            ceiling -= tp - tp_max + 0.1
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
    for c in placed:  # how loud each hit lands in the final mix (vs the narration's integrated level)
        i, j = int(c["at"] * SR), min(total, int((c["at"] + c["dur"]) * SR))
        if j - i > int(0.4 * SR):
            c["mix_momentary_max"] = round(max_momentary(out[i:j]), 1)
    rep = {
        "target_lufs": TARGET_LUFS, "pyloudnorm_lufs": round(lufs(out), 2), "true_peak_dbtp_4x": round(true_peak_db(out), 2),
        "ffmpeg_ebur128": meas, "duration_s": round(total / SR, 3), "music": music, "sfx_placed": placed, **duck_stats,
    }
    if provenance:
        rep["music_provenance"] = provenance
        rep["score"] = {"cues": [{k: c[k] for k in ("t0", "t1", "mood", "intensity", "role")} for c in score_plan["cues"]],
                        "stings": score_plan["stings"], "drops": score_plan["drops"], "risers": score_plan["risers"]}
    log(f"[mix] {meas['I_lufs']} LUFS (ffmpeg), TP {meas['true_peak_dbtp']} dBTP, LRA {meas['LRA_lu']}, "
        f"duck {duck_stats.get('measured_duck_db')} dB, {len(placed)} sfx")
    return {"paths": paths, "report": rep}
