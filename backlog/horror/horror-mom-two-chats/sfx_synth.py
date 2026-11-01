"""Synthesise the 4 SFX this episode needs that studio/public/sfx does not have yet (numpy only, CPU, seeded).

usage (Spark): OMP_NUM_THREADS=2 nice -n 10 ~/studio/.venv/bin/python sfx_synth.py <out_dir>
writes desk_bell_ring.wav, key_scrape.wav, siren.wav, relay_click.wav (48 kHz mono 16-bit, like studio/public/sfx).
All original synthesis (CC0 like pipeline/audio/synth.py); nothing sampled or downloaded.
"""
import os
import sys
import wave

import numpy as np

SR = 48000
rng = np.random.default_rng(412)


def write(path, x, peak=0.89):
    x = np.asarray(x, dtype=np.float64)
    x = x / (np.max(np.abs(x)) + 1e-9) * peak
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


def t(sec):
    return np.arange(int(sec * SR)) / SR


def onepole_lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc = (1 - a) * v + a * acc
        y[i] = acc
    return y


def room(x, decay=0.35, mix=0.25):
    """Tiny seeded-noise convolution reverb (a hallway closet: short, dark)."""
    n = int(decay * SR)
    ir = rng.standard_normal(n) * np.exp(-np.linspace(0, 7, n))
    ir = onepole_lp(ir, 2500)
    wet = np.convolve(x, ir)[: len(x) + n]
    dry = np.concatenate([x, np.zeros(n)])[: len(wet)]
    return (1 - mix) * dry + mix * wet / (np.max(np.abs(wet)) + 1e-9) * np.max(np.abs(x))


def desk_bell_ring():
    """Old desk-phone bell: two 0.4 s bursts (striker at 20 Hz on a 2-partial bell) and a pause; 2 cycles = 4.0 s.
    Muffled (low-passed) because it rings inside a coat in a closet."""
    cyc = np.zeros(int(2.0 * SR))
    for start in (0.0, 0.6):
        tt = t(0.4)
        striker = (np.sin(2 * np.pi * 20 * tt) > 0).astype(float)
        striker = onepole_lp(striker, 120)
        bell = (np.sin(2 * np.pi * 1180 * tt) + 0.6 * np.sin(2 * np.pi * 1520 * tt) + 0.25 * np.sin(2 * np.pi * 2410 * tt))
        env = np.minimum(1, tt / 0.01) * np.minimum(1, (0.4 - tt) / 0.05)
        i0 = int(start * SR)
        cyc[i0:i0 + len(tt)] += bell * (0.35 + 0.65 * striker) * env
    x = np.concatenate([cyc, cyc])
    x = onepole_lp(x, 1900)
    return room(x, 0.3, 0.3)


def key_scrape():
    """A key sliding into a pin-tumbler lock: 5 ridged clicks over a filtered metal scrape, then a seat thunk (0.9 s)."""
    n = int(0.9 * SR)
    x = np.zeros(n)
    tt = t(0.9)
    scrape = rng.standard_normal(n)
    scrape = scrape - onepole_lp(scrape, 1800)  # high-pass
    env = np.clip((tt - 0.05) / 0.05, 0, 1) * np.clip((0.62 - tt) / 0.08, 0, 1)
    x += 0.25 * scrape * env * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * tt))
    for k, c in enumerate(np.linspace(0.12, 0.55, 5)):
        i = int(c * SR)
        m = int(0.012 * SR)
        click = rng.standard_normal(m) * np.exp(-np.linspace(0, 6, m))
        ring = np.sin(2 * np.pi * (3200 + 300 * k) * np.arange(m) / SR) * np.exp(-np.linspace(0, 5, m))
        x[i:i + m] += 0.8 * click + 0.5 * ring
    i = int(0.66 * SR)
    m = int(0.18 * SR)
    th = np.sin(2 * np.pi * 180 * np.arange(m) / SR) * np.exp(-np.linspace(0, 9, m))
    x[i:i + m] += 0.9 * th + 0.3 * rng.standard_normal(m) * np.exp(-np.linspace(0, 12, m))
    return room(x, 0.25, 0.2)


def siren():
    """Two-tone US-style wail through walls: distant to near over 4.5 s (low-pass opens, level rises)."""
    tt = t(4.5)
    f = 900 + 450 * (0.5 + 0.5 * np.sin(2 * np.pi * 0.45 * tt - np.pi / 2))
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sign(np.sin(ph)) * 0.4 + np.sin(ph) * 0.6
    near = np.clip(tt / 4.0, 0, 1) ** 1.5
    lo = onepole_lp(x, 500)
    hi = onepole_lp(x, 2600)
    x = (1 - near) * lo + near * hi
    x *= 0.15 + 0.85 * near
    x *= np.minimum(1, (4.5 - tt) / 0.3)
    return room(x, 0.4, 0.35)


def relay_click():
    """The hall motion light switching on: a relay clack + a short mains buzz (0.35 s)."""
    n = int(0.35 * SR)
    x = np.zeros(n)
    m = int(0.01 * SR)
    x[:m] += rng.standard_normal(m) * np.exp(-np.linspace(0, 5, m))
    tt = t(0.35)
    hum = (np.sin(2 * np.pi * 120 * tt) + 0.5 * np.sin(2 * np.pi * 240 * tt)) * np.exp(-tt * 9) * 0.25
    return x + hum


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out, exist_ok=True)
    for name, fn in [("desk_bell_ring", desk_bell_ring), ("key_scrape", key_scrape), ("siren", siren), ("relay_click", relay_click)]:
        write(os.path.join(out, f"{name}.wav"), fn())
        print(name, "ok")
