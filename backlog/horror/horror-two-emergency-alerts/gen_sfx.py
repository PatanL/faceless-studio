"""Synthesize the 3 original SFX this episode needs (numpy only; run on the Spark CPU).

usage: OMP_NUM_THREADS=2 nice -n 10 ~/studio/.venv/bin/python gen_sfx.py <out_dir>
writes alert_tone.wav, alert_tone_wall.wav, chain_strain.wav (24 kHz mono 16-bit).

alert_tone is deliberately NOT the EAS Attention Signal (853 + 960 Hz two-tone), not the WEA cadence and not a
SAME header burst: it is 4 pulses of a gliding minor-third pair (560->700 Hz and 672->840 Hz, both below 853 Hz)
with a soft 3rd harmonic and a sub thump, so it reads as "a phone screaming" without imitating a real alert.
"""
import os
import sys
import wave

import numpy as np

SR = 24000
out = sys.argv[1]
os.makedirs(out, exist_ok=True)
rng = np.random.default_rng(7)


def write(name, x):
    x = x / (np.max(np.abs(x)) + 1e-9) * 0.89
    with wave.open(os.path.join(out, name), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32767).astype("<i2").tobytes())


def onepole_lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.zeros_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc = (1 - a) * v + a * acc
        y[i] = acc
    return y


def pulse(dur, f0, f1):
    t = np.arange(int(dur * SR)) / SR
    f = f0 + (f1 - f0) * (t / dur) ** 0.7
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) + 0.8 * np.sin(1.2 * ph) + 0.18 * np.sin(3 * ph)
    s = np.tanh(1.8 * s)  # a little grit, like a phone speaker pushed to max
    env = np.minimum(1, t / 0.008) * np.minimum(1, (dur - t) / 0.03)
    return s * env


# ---- alert_tone: 4 pulses, 0.26 s on / 0.1 s off, ~1.45 s total, plus a sub thump on pulse 1
parts = []
for k in range(4):
    parts.append(pulse(0.26, 560, 700))
    parts.append(np.zeros(int(0.1 * SR)))
tone = np.concatenate(parts)
tt = np.arange(len(tone)) / SR
tone += 0.5 * np.sin(2 * np.pi * 70 * tt) * np.exp(-tt / 0.08)
write("alert_tone.wav", tone)

# ---- alert_tone_wall: the same tone heard through a wall (two one-pole LPs at 700 Hz, short room smear)
wall = onepole_lp(onepole_lp(tone, 700), 700)
smear = np.zeros(len(wall) + int(0.25 * SR))
for d, g in ((0.0, 1.0), (0.023, 0.45), (0.051, 0.3), (0.089, 0.18), (0.14, 0.1)):
    i = int(d * SR)
    smear[i:i + len(wall)] += g * wall
write("alert_tone_wall.wav", smear)

# ---- chain_strain: a door chain snapping taut and rattling in its track (~0.9 s)
n = int(0.9 * SR)
x = np.zeros(n)
t = np.arange(n) / SR
for k, t0 in enumerate([0.0, 0.07, 0.16, 0.31, 0.44, 0.6]):
    i0 = int(t0 * SR)
    m = n - i0
    tl = np.arange(m) / SR
    amp = 1.0 if k == 0 else 0.55 * (0.8 ** k)
    ring = sum(np.sin(2 * np.pi * f * tl + rng.uniform(0, 6.28)) * np.exp(-tl / dcy)
               for f, dcy in ((2310, 0.05), (3720, 0.035), (5130, 0.025), (1480, 0.07)))
    click = rng.normal(0, 1, m) * np.exp(-tl / 0.004)
    x[i0:] += amp * (0.6 * ring + click)
x += 0.6 * np.sin(2 * np.pi * 95 * t) * np.exp(-t / 0.05)  # the door hitting the chain
write("chain_strain.wav", x)
print("ok", os.listdir(out))
