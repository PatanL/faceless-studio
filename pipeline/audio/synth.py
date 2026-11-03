"""Procedural SFX and music beds (numpy/scipy only, no samples, no downloads).

Everything here is generated from math and seeded noise, so the output is original work
owned by this project (see pipeline/audio/LICENSES.md).

usage (Spark):
  python -m pipeline.audio.synth                       # all SFX -> studio/public/sfx, beds -> studio/public/music
  python -m pipeline.audio.synth --only knock3,notify  # a subset
  python -m pipeline.audio.synth --list
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

import numpy as np
from scipy import signal

SR = 48000
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SFX_DIR = os.path.join(ROOT, "studio", "public", "sfx")
MUSIC_DIR = os.path.join(ROOT, "studio", "public", "music")


# ----------------------------------------------------------------------------- helpers

def t_axis(dur: float) -> np.ndarray:
    return np.arange(int(dur * SR)) / SR


def rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


def env_exp(n: int, decay: float, attack: float = 0.002) -> np.ndarray:
    t = np.arange(n) / SR
    a = np.clip(t / max(attack, 1e-4), 0, 1)
    return a * np.exp(-t / max(decay, 1e-4))


def env_ad(n: int, attack: float, release: float) -> np.ndarray:
    """Raised-cosine attack then raised-cosine release over the whole length."""
    t = np.arange(n) / SR
    dur = n / SR
    a = np.where(t < attack, 0.5 - 0.5 * np.cos(np.pi * np.clip(t / max(attack, 1e-4), 0, 1)), 1.0)
    r = np.where(t > dur - release, 0.5 - 0.5 * np.cos(np.pi * np.clip((dur - t) / max(release, 1e-4), 0, 1)), 1.0)
    return a * r


def sweep_sine(f0, f1, dur, curve="exp") -> np.ndarray:
    t = t_axis(dur)
    if curve == "exp":
        f = f0 * (f1 / f0) ** (t / dur)
    else:
        f = f0 + (f1 - f0) * t / dur
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


def freq_sine(f: np.ndarray) -> np.ndarray:
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


def bp(x, lo, hi, order=2):
    sos = signal.butter(order, [lo, hi], btype="band", fs=SR, output="sos")
    return signal.sosfilt(sos, x)


def lp(x, f, order=2):
    sos = signal.butter(order, f, btype="low", fs=SR, output="sos")
    return signal.sosfilt(sos, x)


def hp(x, f, order=2):
    sos = signal.butter(order, f, btype="high", fs=SR, output="sos")
    return signal.sosfilt(sos, x)


def resonator(x, f, q):
    b, a = signal.iirpeak(f, q, fs=SR)
    return signal.lfilter(b, a, x)


def brown(n, seed):
    w = rng(seed).standard_normal(n)
    b = np.cumsum(w)
    b = hp(b, 20)
    return b / (np.abs(b).max() + 1e-9)


def shaped_noise(dur, center, width, amp, seed=1):
    """White noise whose spectrum is a moving Gaussian bump. center/width/amp are
    callables of normalised time u in [0,1] (Hz, Hz, linear)."""
    n = int(round(dur * SR))
    x = rng(seed).standard_normal(n)
    nper = 1024
    f, tt, Z = signal.stft(x, fs=SR, nperseg=nper)
    u = np.clip(tt / dur, 0, 1)
    c = np.array([center(v) for v in u])
    w = np.array([width(v) for v in u])
    a = np.array([amp(v) for v in u])
    mask = np.exp(-0.5 * ((f[:, None] - c[None, :]) / w[None, :]) ** 2) * a[None, :]
    _, y = signal.istft(Z * mask, fs=SR, nperseg=nper)
    return y[:n]


def reverb(x, seconds=1.2, wet=0.3, seed=7, predelay=0.012, damp=4000, stereo=False):
    """Convolution with exponentially decaying filtered noise."""
    n = int(seconds * SR)
    outs = []
    for ch in range(2 if stereo else 1):
        ir = rng(seed + ch).standard_normal(n) * np.exp(-np.arange(n) / SR * (6.9 / seconds))
        ir = lp(ir, damp)
        ir = np.concatenate([np.zeros(int(predelay * SR)), ir])
        ir /= np.sqrt(np.sum(ir ** 2)) + 1e-9
        y = signal.fftconvolve(x, ir)[: len(x) + len(ir) - 1]
        dry = np.concatenate([x, np.zeros(len(y) - len(x))])
        outs.append((1 - wet) * dry + wet * y)
    return np.stack(outs, 1) if stereo else outs[0]


def place(dst, src, at):
    i = int(round(at * SR))
    if i < 0:
        src, i = src[-i:], 0
    j = min(len(dst), i + len(src))
    if j > i:
        dst[i:j] += src[: j - i]
    return dst


def norm_peak(x, db=-1.0):
    p = np.abs(x).max()
    return x if p == 0 else x * (10 ** (db / 20) / p)


def trim_tail(x, thresh_db=-60):
    """Drop trailing near-silence (keeps reverb tails above threshold)."""
    a = np.abs(x if x.ndim == 1 else x.max(1))
    th = a.max() * 10 ** (thresh_db / 20)
    idx = np.nonzero(a > th)[0]
    end = idx[-1] + int(0.02 * SR) if len(idx) else len(x)
    y = x[: min(len(x), end)].copy()
    fade = min(len(y), int(0.01 * SR))
    if fade:
        ramp = np.linspace(1, 0, fade)
        y[-fade:] *= ramp if y.ndim == 1 else ramp[:, None]
    return y


def write_wav(path, x, sr=SR):
    import soundfile as sf
    os.makedirs(os.path.dirname(path), exist_ok=True)
    sf.write(path, np.clip(x, -1, 1).astype(np.float32), sr, subtype="PCM_16")


# ----------------------------------------------------------------------------- SFX

def sfx_whoosh(dur=0.9, seed=11, lo=250, hi=3200):
    y = shaped_noise(dur, lambda u: lo * (hi / lo) ** np.sin(np.pi * u) ** 1.5,
                     lambda u: 300 + 900 * np.sin(np.pi * u), lambda u: np.sin(np.pi * u) ** 2, seed)
    return reverb(y, 0.6, 0.15)


def _swish(dur, f0, f1, attack, tau, seed, width=1.0, lp_hz=7000):
    """A short, dry, mono noise swish (the RicksClips3000 kind, research/music/RICKS_SOUND.md section 7): a band of
    noise ~1 octave wide gliding f0 -> f1, a fast power-curve attack and an exponential release (tau s)."""
    y = shaped_noise(dur, lambda u: f0 * (f1 / f0) ** u, lambda u: width * f0 * (f1 / f0) ** u, lambda u: 1.0, seed)
    t = t_axis(dur)[: len(y)]
    env = np.where(t < attack, (t / attack) ** 1.5, np.exp(-(t - attack) / tau))
    return lp(y * env, lp_hz, 2)


def sfx_swish():
    # flat, the common one: centroid ~2 kHz, ~0.12 s at -20 dB, attack 0.04 s, release ~0.08 s
    return _swish(0.24, 1900, 1700, 0.04, 0.035, 61)


def sfx_swish_fall():
    # the falling variant (about a quarter of theirs): ~2.6 -> 1.8 kHz over its -20 dB span, a little longer
    return _swish(0.3, 3200, 1200, 0.035, 0.06, 62)


def sfx_whoosh_long():
    return sfx_whoosh(1.6, 12, 180, 2600)


def sfx_riser(dur=2.6):
    n = int(dur * SR)
    t = t_axis(dur)
    noise = shaped_noise(dur, lambda u: 200 * 30 ** u, lambda u: 150 + 1500 * u, lambda u: u ** 2.2, 13)
    tone = sweep_sine(110, 880, dur) * (t / dur) ** 3 * 0.35
    tone += sweep_sine(116, 930, dur) * (t / dur) ** 3 * 0.25  # detuned, beating
    y = noise / (np.abs(noise).max() + 1e-9) + tone
    y[-int(0.01 * SR):] *= np.linspace(1, 0, int(0.01 * SR))
    return y[:n]


def sfx_impact(dur=1.9, seed=14):
    n = int(dur * SR)
    t = t_axis(dur)
    f = 32 + 45 * np.exp(-t / 0.08)
    sub = freq_sine(f) * env_exp(n, 0.55)
    click = lp(rng(seed).standard_normal(n), 1800) * env_exp(n, 0.025) * 0.8
    body = lp(rng(seed + 1).standard_normal(n), 400) * env_exp(n, 0.25) * 0.6
    return reverb(sub + click + body, 1.4, 0.25)


def sfx_boom():
    n = int(3.5 * SR)
    y = sfx_impact(3.5, 15)
    rumble = lp(brown(n, 16), 120) * env_ad(n, 0.05, 2.5) * 0.5
    return y[:n] + rumble


def _lubdub(n, f=48, decay=0.08, seed=0):
    t = np.arange(n) / SR
    tone = freq_sine(f + 25 * np.exp(-t / 0.02)) * env_exp(n, decay, 0.004)
    thump = lp(rng(seed).standard_normal(n), 140) * env_exp(n, decay * 0.6, 0.002) * 0.8
    return tone + thump


def _heartbeats(bpm, beats, seed=20):
    period = 60 / bpm
    dur = period * beats + 0.5
    y = np.zeros(int(dur * SR))
    for i in range(beats):
        jit = rng(seed + i).uniform(-0.01, 0.01)
        place(y, _lubdub(int(0.35 * SR), 46, 0.09, seed + i), i * period + jit)
        place(y, 0.65 * _lubdub(int(0.3 * SR), 58, 0.07, seed + 50 + i), i * period + 0.2 + jit)
    return lp(y, 300)


def sfx_heartbeat():
    return _heartbeats(70, 1)


def sfx_heartbeat_slow():
    return _heartbeats(62, 5)


def sfx_heartbeat_fast():
    return _heartbeats(120, 8)


def _buzz(dur, seed):
    n = int(dur * SR)
    t = t_axis(dur)
    f = 172 + 4 * np.sin(2 * np.pi * 7 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    motor = np.tanh(3 * np.sin(ph)) * 0.6 + 0.25 * np.sin(2 * ph)
    rattle = bp(rng(seed).standard_normal(n), 1800, 4200) * (0.5 + 0.5 * np.sin(ph)) ** 4 * 0.5
    return (lp(motor, 1200) + rattle) * env_ad(n, 0.02, 0.03)


def sfx_phone_buzz():
    y = np.zeros(int(1.3 * SR))
    place(y, _buzz(0.42, 21), 0.0)
    place(y, _buzz(0.42, 22), 0.62)
    return reverb(y, 0.25, 0.12)  # small table resonance


def sfx_phone_buzz_long():
    y = np.zeros(int(3.0 * SR))
    for i in range(3):
        place(y, _buzz(0.6, 23 + i), i * 0.95)
    return reverb(y, 0.25, 0.12)


def _bell(n, f, partials=((1, 1, 1.0), (2.0, 0.4, 0.5), (3.01, 0.25, 0.3)), decay=0.25):
    t = np.arange(n) / SR
    y = np.zeros(n)
    for mult, amp, dmul in partials:
        y += amp * np.sin(2 * np.pi * f * mult * t) * np.exp(-t / (decay * dmul))
    return y * np.clip(t / 0.003, 0, 1)


def sfx_notify():
    y = np.zeros(int(0.9 * SR))
    place(y, _bell(int(0.5 * SR), 1568), 0)
    place(y, _bell(int(0.6 * SR), 2093), 0.11)
    return reverb(y, 0.5, 0.18)


def sfx_message_send():
    n = int(0.22 * SR)
    t = t_axis(0.22)
    y = freq_sine(500 + 900 * (t / 0.22) ** 0.6) * env_ad(n, 0.01, 0.12)
    return reverb(y, 0.3, 0.12)


def sfx_message_pop():
    n = int(0.16 * SR)
    t = t_axis(0.16)
    y = freq_sine(1000 * np.exp(-t / 0.08) + 520) * env_exp(n, 0.05, 0.003)
    return y


def sfx_pop():
    n = int(0.12 * SR)
    t = t_axis(0.12)
    return freq_sine(300 + 900 * np.exp(-t / 0.015)) * env_exp(n, 0.03, 0.001)


def sfx_click():
    n = int(0.04 * SR)
    return bp(rng(30).standard_normal(n), 2000, 6000) * env_exp(n, 0.004, 0.0005)


def sfx_typing(dur=2.2, seed=31):
    r = rng(seed)
    y = np.zeros(int(dur * SR))
    at = 0.05
    while at < dur - 0.1:
        n = int(0.03 * SR)
        k = bp(r.standard_normal(n), 1500, 7000) * env_exp(n, 0.003, 0.0004) * r.uniform(0.5, 1)
        k += lp(r.standard_normal(n), 500) * env_exp(n, 0.008) * 0.4
        place(y, k, at)
        at += r.uniform(0.06, 0.19) + (0.25 if r.random() < 0.12 else 0)
    return reverb(y, 0.2, 0.1)


def _knock(seed, strength=1.0):
    n = int(0.45 * SR)
    r = rng(seed)
    hit = lp(r.standard_normal(n), 1600) * env_exp(n, 0.006, 0.0005)
    body = np.zeros(n)
    for f, d in ((105, 0.09), (178, 0.07), (262, 0.05), (410, 0.03)):
        body += np.sin(2 * np.pi * f * r.uniform(0.97, 1.03) * np.arange(n) / SR) * env_exp(n, d, 0.001)
    return strength * (0.8 * hit + 0.6 * body)


def _knocks(times, seed=40, room=0.7):
    y = np.zeros(int((times[-1] + 0.6) * SR))
    for i, at in enumerate(times):
        place(y, _knock(seed + i, 1.0 - 0.08 * (i % 2)), at)
    return reverb(y, room, 0.22)


def sfx_knock():
    return _knocks([0.0])


def sfx_knock3():
    return _knocks([0.0, 0.32, 0.64])


def _heavy_knock(seed, strength=1.0):
    """A fist on a solid door, close to the listener: knuckle crack + low door-panel thump + rattle in the frame."""
    n = int(0.7 * SR)
    t = np.arange(n) / SR
    r = rng(seed)
    crack = lp(r.standard_normal(n), 2400) * env_exp(n, 0.008, 0.0005)
    f = 62 + 38 * np.exp(-t / 0.03)
    thump = np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(n, 0.16, 0.002)
    panel = np.zeros(n)
    for fr, d in ((96, 0.14), (151, 0.10), (233, 0.07), (372, 0.04)):
        panel += np.sin(2 * np.pi * fr * r.uniform(0.98, 1.02) * t) * env_exp(n, d, 0.001)
    rattle = bp(r.standard_normal(n), 1800, 4200) * env_exp(n, 0.05, 0.004) * (0.5 + 0.5 * np.sin(2 * np.pi * 37 * t))
    y = 0.7 * crack + 1.1 * thump + 0.55 * panel + 0.12 * rattle
    y = np.tanh(2.2 * y) / np.tanh(2.2)  # soften the crest so the hit can sit loud under the true-peak ceiling
    return strength * y


def sfx_knock3_slow():
    """The climactic three knocks (0 / 0.95 / 1.9 s): heavy door thumps in a small hallway."""
    times = [0.0, 0.95, 1.9]
    y = np.zeros(int((times[-1] + 1.0) * SR))
    for i, at in enumerate(times):
        place(y, _heavy_knock(60 + i, 1.0 if i != 1 else 0.94), at)
    return reverb(y, 0.9, 0.3, predelay=0.008, damp=3000)


def sfx_door_creak(dur=2.4, seed=50):
    n = int(dur * SR)
    t = t_axis(dur)
    rate = 22 + 45 * np.sin(np.pi * t / dur) ** 2 + 8 * np.sin(2 * np.pi * 1.3 * t)
    phase = np.cumsum(rate) / SR
    pulses = np.diff(np.floor(phase), prepend=0) > 0
    exc = pulses.astype(float) * rng(seed).uniform(0.6, 1.0, n)
    exc = lp(exc + 0.02 * rng(seed + 1).standard_normal(n), 6000)
    y = resonator(exc, 640, 18) + 0.7 * resonator(exc, 1150, 22) + 0.4 * resonator(exc, 1980, 25)
    y *= env_ad(n, 0.15, 0.3)
    return reverb(y, 0.9, 0.25)


def sfx_ding():
    n = int(2.6 * SR)
    y = _bell(n, 1046.5, ((1, 1, 1.0), (2.0, 0.35, 0.6), (2.76, 0.25, 0.4), (5.4, 0.08, 0.2)), decay=0.9)
    y2 = _bell(n, 830.6, ((1, 1, 1.0), (2.0, 0.3, 0.6), (2.76, 0.2, 0.4)), decay=1.0)
    out = np.zeros(int(3.0 * SR))
    place(out, y, 0)
    place(out, 0.9 * y2, 0.42)
    return reverb(out, 1.0, 0.2)


def sfx_stinger(dur=3.2):
    n = int(dur * SR)
    t = t_axis(dur)
    y = np.zeros(n)
    for f in (220, 233.1, 329.6, 349.2):  # A3, Bb3, E4, F4: minor-second clusters
        for d in (-0.6, 0.6):
            ph = 2 * np.pi * np.cumsum(np.full(n, f + d)) / SR
            y += signal.sawtooth(ph) * 0.12
    y = lp(y, 2500)
    y *= np.clip(t / 0.08, 0, 1) * np.exp(-t / 1.1)
    hit = sfx_impact(dur, 52)[:n] * 0.7
    return reverb(y + hit, 2.0, 0.35)


def sfx_static(dur=1.2, seed=60):
    n = int(dur * SR)
    r = rng(seed)
    x = r.standard_normal(n)
    x = np.round(x * 6) / 6  # bitcrush
    gate = np.repeat(r.random(int(dur * 40) + 1) > 0.35, SR // 40)[:n]
    return hp(x * np.convolve(gate.astype(float), np.ones(200) / 200, "same"), 300) * env_ad(n, 0.01, 0.08) * 0.6


def sfx_glitch():
    n = int(0.42 * SR)
    r = rng(61)
    y = np.zeros(n)
    i = 0
    while i < n:
        seg = int(r.uniform(0.01, 0.05) * SR)
        f = r.choice([180, 440, 1200, 2400, 90])
        piece = (signal.square(2 * np.pi * f * np.arange(seg) / SR) * 0.4 if r.random() < 0.5
                 else r.standard_normal(seg) * 0.5)
        y[i:i + seg] = piece[: max(0, min(seg, n - i))]
        i += seg + int(r.uniform(0, 0.02) * SR)
    return y * env_ad(n, 0.002, 0.03)


def sfx_tick():
    n = int(0.06 * SR)
    return bp(rng(70).standard_normal(n), 2500, 6000) * env_exp(n, 0.006, 0.0005) + \
        0.3 * np.sin(2 * np.pi * 3100 * np.arange(n) / SR) * env_exp(n, 0.01)


def sfx_clock_ticking():
    y = np.zeros(int(4.2 * SR))
    for i in range(4):
        place(y, sfx_tick() * (1.0 if i % 2 == 0 else 0.75), i * 1.0)
    return reverb(y, 0.5, 0.15)


def sfx_sonar_ping():
    n = int(1.6 * SR)
    t = np.arange(n) / SR
    ping = np.sin(2 * np.pi * 1180 * t) * np.exp(-t / 0.45) * np.clip(t / 0.004, 0, 1)
    ping += 0.25 * np.sin(2 * np.pi * 2360 * t) * np.exp(-t / 0.2)
    y = np.zeros(int(3.4 * SR))
    place(y, ping, 0)
    place(y, 0.28 * lp(ping, 2500), 1.15)  # echo off the "target"
    return reverb(y, 2.2, 0.4)


def sfx_bubbles(dur=2.2, seed=80):
    r = rng(seed)
    y = np.zeros(int(dur * SR))
    for _ in range(int(dur * 9)):
        d = r.uniform(0.02, 0.07)
        n = int(d * SR)
        f0 = r.uniform(350, 900)
        b = sweep_sine(f0, f0 * r.uniform(1.6, 2.6), d) * env_ad(n, 0.004, d * 0.6)
        place(y, b * r.uniform(0.3, 1), r.uniform(0, dur - d))
    return reverb(lp(y, 3000), 0.7, 0.3)


def sfx_underwater_rumble(dur=5.0):
    n = int(dur * SR)
    t = t_axis(dur)
    y = lp(brown(n, 81), 180, 4) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.25 * t))
    return y * env_ad(n, 1.0, 1.5)


def sfx_footsteps(steps=4, interval=0.62, seed=90):
    y = np.zeros(int((steps * interval + 0.6) * SR))
    for i in range(steps):
        n = int(0.3 * SR)
        r = rng(seed + i)
        thud = lp(r.standard_normal(n), 220) * env_exp(n, 0.04, 0.003)
        scuff = bp(r.standard_normal(n), 800, 3000) * env_exp(n, 0.03, 0.01) * 0.25
        place(y, thud + scuff, i * interval + r.uniform(-0.02, 0.02))
    return reverb(y, 1.1, 0.3)


def sfx_breath():
    dur = 1.6
    return shaped_noise(dur, lambda u: 1100 + 500 * u, lambda u: 600, lambda u: np.sin(np.pi * min(1, u * 1.15)) ** 1.5, 95)


def sfx_drone(dur=8.0):
    n = int(dur * SR)
    t = t_axis(dur)
    y = np.zeros(n)
    for f, a in ((55, 1), (55.4, 0.8), (77.8, 0.35), (110.3, 0.25)):
        y += a * np.sin(2 * np.pi * f * t + rng(int(f)).uniform(0, 6.28))
    y += 0.3 * lp(brown(n, 99), 300)
    return y * env_ad(n, 1.5, 2.0)


SFX = {name[4:]: fn for name, fn in sorted(globals().items()) if name.startswith("sfx_") and callable(fn)}


# ----------------------------------------------------------------------------- music beds

def _note(f, n, seed, detune_cents=(-7, -2, 3, 8), harmonics=8, bright=2.6):
    """Soft additive saw-ish pad note, stereo (n, 2)."""
    t = np.arange(n) / SR
    r = rng(seed)
    out = np.zeros((n, 2))
    for k, c in enumerate(detune_cents):
        fd = f * 2 ** (c / 1200)
        ch = k % 2
        ph0 = r.uniform(0, 2 * np.pi)
        for h in range(1, harmonics + 1):
            amp = (1 / h) * np.exp(-(h - 1) / bright)
            out[:, ch] += amp * np.sin(2 * np.pi * fd * h * t + ph0 * h)
    return out / len(detune_cents)


def _loopify(x, loop_len, xfade):
    """x has loop_len + xfade samples: crossfade the tail into the head so it loops cleanly."""
    head = x[:xfade].copy()
    tail = x[loop_len:loop_len + xfade]
    w = np.linspace(0, 1, xfade)[:, None] if x.ndim == 2 else np.linspace(0, 1, xfade)
    y = x[:loop_len].copy()
    y[:xfade] = head * np.sqrt(w) + tail * np.sqrt(1 - w)
    return y


def _pad_progression(chords, chord_len, total, seed, bright=2.6, gain=1.0):
    n = int(total * SR)
    out = np.zeros((n, 2))
    over = 3.0  # chords overlap (crossfade) this many seconds
    for i, notes in enumerate(chords):
        start = i * chord_len - over / 2
        ln = chord_len + over
        a, b = int(max(0, start) * SR), int(min(total, start + ln) * SR)
        m = b - a
        if m <= 0:
            continue
        e = env_ad(m, over, over)[:, None]
        for j, f in enumerate(notes):
            out[a:b] += _note(f, m, seed + 10 * i + j, bright=bright) * e * gain
    return out


def bed_deep_ocean(loop=48.0, seed=200):
    """Explainer: slow, cold, curious minor pad + sub + filtered 'pressure' noise + far bells."""
    xf = 4.0
    total = loop + xf
    n = int(total * SR)
    # D minor-ish: Dm9, Bbmaj7, Gm9, A7sus — 4 chords of 12 s, cycle repeats in the crossfade tail
    chords = [[73.42, 146.8, 220.0, 329.6, 349.2],
              [58.27, 116.5, 174.6, 220.0, 293.7],
              [49.0, 98.0, 233.1, 293.7, 349.2],
              [55.0, 110.0, 196.0, 293.7, 329.6]]
    chords = chords + chords[:1]
    pad = _pad_progression(chords, loop / 4, total, seed, bright=2.2)
    pad = np.stack([lp(pad[:, 0], 1400), lp(pad[:, 1], 1400)], 1)
    t = np.arange(n) / SR
    noise = lp(brown(n, seed + 1), 260, 4) * (0.5 + 0.5 * np.sin(2 * np.pi * t / (loop / 3))) * 0.5
    y = pad + noise[:, None] * np.array([[1.0, 0.85]])
    bells = np.zeros(n)
    r = rng(seed + 2)
    pent = [587.3, 659.3, 880.0, 987.8, 1174.7]
    for at in np.arange(3.0, total - 3, 6.0):
        place(bells, _bell(int(2.5 * SR), r.choice(pent), decay=0.8) * 0.12, at + r.uniform(-0.6, 0.6))
    bells = reverb(bells, 3.0, 0.6, stereo=True)[:n]
    y = y + bells
    return _loopify(y, int(loop * SR), int(xf * SR))


def bed_documentary_pulse(loop=45.7, seed=300):
    """Explainer (lighter): pad + soft 8th-note pluck arpeggio at 84 bpm (16 bars)."""
    bpm = 84
    eighth = 60 / bpm / 2
    xf = 4.0
    total = loop + xf
    n = int(total * SR)
    chords = [[65.41, 130.8, 196.0, 261.6, 329.6],  # C(add9)-ish
              [55.0, 110.0, 164.8, 261.6, 329.6],   # Am7
              [43.65, 87.31, 174.6, 220.0, 261.6],  # Fmaj7
              [49.0, 98.0, 146.8, 246.9, 293.7]]    # G
    chords = chords + chords[:1]
    clen = loop / 4
    pad = _pad_progression(chords, clen, total, seed, bright=1.8, gain=0.7)
    pad = np.stack([lp(pad[:, 0], 1100), lp(pad[:, 1], 1100)], 1)
    pl = np.zeros((n, 2))
    k = 0
    for at in np.arange(0, total - 0.5, eighth):
        ci = min(int(at // clen), len(chords) - 1)
        notes = chords[ci][2:]
        f = notes[[0, 1, 2, 1][k % 4]] * 2
        m = int(0.6 * SR)
        tt = np.arange(m) / SR
        p = (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt)) * np.exp(-tt / 0.18) * np.clip(tt / 0.004, 0, 1)
        pan = 0.5 + 0.3 * np.sin(k * 0.7)
        acc = 1.0 if k % 2 == 0 else 0.7
        place(pl[:, 0], p * (1 - pan) * 0.22 * acc, at)
        place(pl[:, 1], p * pan * 0.22 * acc, at)
        k += 1
    pl = reverb(lp(pl.mean(1), 3000), 1.4, 0.35, stereo=True)[:n] * 0.9 + pl * 0.3
    y = pad + pl
    return _loopify(y, int(loop * SR), int(xf * SR))


def bed_dread(loop=48.0, seed=400):
    """Horror: beating low drone with a tritone, moving wind noise, far low hits, a thin high whine."""
    xf = 5.0
    total = loop + xf
    n = int(total * SR)
    t = np.arange(n) / SR
    y = np.zeros((n, 2))
    for f, a, beat in ((55.0, 1.0, 0.13), (82.4, 0.35, 0.21), (77.8, 0.3, 0.08), (110.0, 0.22, 0.17)):
        for ch, sgn in ((0, -1), (1, 1)):
            fd = f + sgn * beat
            y[:, ch] += a * np.sin(2 * np.pi * fd * t + seed * 0.1 * ch)
    y = np.stack([lp(np.tanh(1.4 * y[:, c]), 700) for c in range(2)], 1) * 0.55
    wind = np.zeros((n, 2))
    for c in range(2):
        w = shaped_noise(total, lambda u, c=c: 500 + 320 * np.sin(2 * np.pi * u * total / (loop / 2) + c),
                         lambda u: 220, lambda u: 1.0, seed + 5 + c)[:n]
        wind[:, c] = w * (0.5 + 0.5 * np.sin(2 * np.pi * t / (loop / 4) + 2 * c)) ** 2
    wind /= np.abs(wind).max() + 1e-9
    y += wind * 0.18
    hits = np.zeros(n)
    for at in (9.0, 31.0):
        place(hits, lp(sfx_impact(2.5, seed + int(at)), 200) * 0.35, at)
    y += reverb(hits, 3.0, 0.6, stereo=True)[:n]
    whine = freq_sine(1760 + 25 * np.sin(2 * np.pi * 0.07 * t)) * (np.clip(np.sin(2 * np.pi * t / loop - 1.2), 0, 1) ** 3) * 0.02
    y += np.stack([whine, np.roll(whine, 400)], 1)
    return _loopify(y, int(loop * SR), int(xf * SR))


def bed_tension_pulse(loop=48.0, seed=500):
    """Horror (active): dread drone under a soft 60 bpm sub pulse and a quiet ticking."""
    xf = 2.0
    total = loop + xf
    n = int(total * SR)
    base = bed_dread(loop + xf + 5.0, seed)[:n] * 0.7
    pulse = np.zeros(n)
    for i in range(int(total)):
        place(pulse, _lubdub(int(0.4 * SR), 44, 0.12, seed + i) * 0.5, i * 1.0)
        place(pulse, _lubdub(int(0.3 * SR), 52, 0.08, seed + 99 + i) * 0.3, i * 1.0 + 0.22)
    tick = np.zeros(n)
    for i in range(int(total * 2)):
        place(tick, sfx_tick() * 0.06, i * 0.5 + 0.25)
    y = base + lp(pulse, 200)[:, None] + reverb(tick, 0.6, 0.3, stereo=True)[:n]
    return _loopify(y, int(loop * SR), int(xf * SR))


BEDS = {"deep_ocean": bed_deep_ocean, "documentary_pulse": bed_documentary_pulse,
        "dread": bed_dread, "tension_pulse": bed_tension_pulse}


def encode_m4a(wav_path, m4a_path, kbps=192):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav_path, "-c:a", "aac", "-b:a", f"{kbps}k", m4a_path], check=True)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="", help="comma list of sfx/bed names")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--sfx-dir", default=SFX_DIR)
    ap.add_argument("--music-dir", default=MUSIC_DIR)
    ap.add_argument("--sheet", help="write a PNG (waveform over spectrogram) of every SFX in order, then exit")
    a = ap.parse_args(argv)
    if a.sheet:
        import soundfile as sf
        names = sorted(f[:-4] for f in os.listdir(a.sfx_dir) if f.endswith(".wav"))
        gap = np.zeros(int(0.35 * SR), np.float32)
        parts = []
        for nm in names:
            x, _ = sf.read(os.path.join(a.sfx_dir, nm + ".wav"), dtype="float32")
            parts += [x if x.ndim == 1 else x.mean(1), gap]
        tmp = a.sheet + ".wav"
        write_wav(tmp, np.concatenate(parts))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-filter_complex",
                        "[0:a]asplit[a][b];[a]showwavespic=s=2400x160:colors=0xff5c7a[w];"
                        "[b]showspectrumpic=s=2400x400:legend=0:scale=log:color=intensity[s];[w][s]vstack[o]",
                        "-map", "[o]", "-frames:v", "1", a.sheet], check=True)
        os.remove(tmp)
        print("order:", ", ".join(names))
        return
    if a.list:
        print("sfx:", ", ".join(SFX))
        print("beds:", ", ".join(BEDS))
        return
    only = {s for s in a.only.split(",") if s}
    for name, fn in SFX.items():
        if only and name not in only:
            continue
        x = trim_tail(norm_peak(fn(), -1.0))
        write_wav(os.path.join(a.sfx_dir, f"{name}.wav"), x)
        print(f"sfx  {name:20s} {len(x) / SR:5.2f}s", flush=True)
    for name, fn in BEDS.items():
        if only and name not in only:
            continue
        x = norm_peak(fn(), -3.0)
        wav = os.path.join(a.music_dir, f"{name}.wav")
        write_wav(wav, x)
        encode_m4a(wav, os.path.join(a.music_dir, f"{name}.m4a"))
        print(f"bed  {name:20s} {len(x) / SR:5.2f}s", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
