"""Generate small original test audio (music bed + SFX) with the stdlib only.
usage: python3 scripts/gen_test_audio.py [outdir=public/test]"""
import math, random, struct, sys, wave, os

SR = 22050
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'public', 'test')
os.makedirs(out, exist_ok=True)

def write(name, samples):
    peak = max(1e-9, max(abs(s) for s in samples))
    g = 0.89 / peak
    with wave.open(os.path.join(out, name), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(b''.join(struct.pack('<h', int(max(-1, min(1, s * g)) * 32767)) for s in samples))
    print('wrote', name, len(samples) / SR, 's')

def note(m):  # midi -> Hz
    return 440 * 2 ** ((m - 69) / 12)

# music bed: Am F C G pad, 3 s per chord, soft pulse on every half second
chords = [[57, 60, 64], [53, 57, 60], [48, 55, 64], [55, 59, 62]]
N = SR * 12
music = [0.0] * N
for ci, ch in enumerate(chords):
    s0 = ci * 3 * SR
    for i in range(3 * SR):
        t = i / SR
        env = min(1, t / 0.4) * min(1, (3 - t) / 0.4)
        v = 0
        for m in ch:
            f = note(m)
            v += math.sin(2 * math.pi * f * t) + 0.3 * math.sin(2 * math.pi * 2 * f * t) + 0.12 * math.sin(2 * math.pi * 3 * f * t)
        v += 0.6 * math.sin(2 * math.pi * note(ch[0] - 12) * t)
        music[s0 + i] += v * env * 0.18
for b in range(24):
    s0 = int(b * 0.5 * SR)
    for i in range(int(0.25 * SR)):
        t = i / SR
        f = 55 + 70 * math.exp(-t * 30)
        if s0 + i < N:
            music[s0 + i] += math.sin(2 * math.pi * f * t) * math.exp(-t * 14) * 0.9
write('music-bed.wav', music)

rnd = random.Random(7)
# whoosh: low-passed noise, cutoff sweeps up then down
n = int(0.6 * SR); y = 0; wh = []
for i in range(n):
    p = i / n
    a = math.sin(math.pi * p) ** 2
    cutoff = 0.02 + 0.25 * math.sin(math.pi * p)
    y += cutoff * (rnd.uniform(-1, 1) - y)
    wh.append(y * a)
write('whoosh.wav', wh)

# pop: quick downward sine chirp
n = int(0.16 * SR); ph = 0; pop = []
for i in range(n):
    t = i / SR
    f = 300 + 700 * math.exp(-t * 40)
    ph += 2 * math.pi * f / SR
    pop.append(math.sin(ph) * math.exp(-t * 28))
write('pop.wav', pop)

# impact: sub boom + noise transient
n = int(1.0 * SR); ph = 0; imp = []; y = 0
for i in range(n):
    t = i / SR
    f = 42 + 80 * math.exp(-t * 18)
    ph += 2 * math.pi * f / SR
    y += 0.3 * (rnd.uniform(-1, 1) - y)
    imp.append(math.sin(ph) * math.exp(-t * 4) + y * math.exp(-t * 25) * 0.8)
write('impact.wav', imp)

# glitch: stuttered, bit-crushed square chirps
n = int(0.4 * SR); gl = []
for i in range(n):
    t = i / SR
    seg = int(t * 40)
    f = [220, 880, 440, 1320, 330][seg % 5]
    on = (seg * 7) % 3 != 0
    v = 1 if math.sin(2 * math.pi * f * t) > 0 else -1
    v = round(v * on * 4) / 4 + rnd.uniform(-0.3, 0.3) * on
    gl.append(v * 0.6 * (1 - t / 0.4))
write('glitch.wav', gl)
