"""Audio proxies for sound design. usage: audio_sync.py <ffmpeg> <video> <motion.json> <out.json>
- 50 ms frames, mono 22.05 kHz. Bands: low <250 Hz, mid 250-4k, high >4k (dB).
- For visual events (cuts/transitions from motion.json, loose detector), compare high-band energy rise
  (max in [-0.15,+0.35] s minus median of preceding 1 s) vs the same statistic at random times."""
import sys, subprocess, json
import numpy as np
ff, vid, mj, out = sys.argv[1:5]
SR = 22050
raw = subprocess.run([ff, "-v", "error", "-threads", "2", "-i", vid, "-vn", "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True).stdout
x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
N = int(0.05 * SR); nf = len(x) // N
fr = x[: nf * N].reshape(nf, N) * np.hanning(N)
S = np.abs(np.fft.rfft(fr, axis=1)) ** 2
f = np.fft.rfftfreq(N, 1 / SR)
def band(lo, hi): return 10 * np.log10(S[:, (f >= lo) & (f < hi)].sum(1) + 1e-9)
low, mid, high = band(20, 250), band(250, 4000), band(4000, 11000)
m = json.load(open(mj)); d = m["diff_series"]; fps = m["fps"]
ev = []
for i in range(len(d)):
    lo, hi = max(0, i - 15), min(len(d), i + 16)
    nb = sorted(d[lo:i] + d[i + 1:hi]); med = nb[len(nb) // 2]
    if d[i] > max(5, 5 * med):
        t = (i + 1) / fps
        if not ev or t - ev[-1] > 0.5: ev.append(t)
def rise(sig, t):
    k = int(t / 0.05); a = sig[max(0, k - 20):k]; b = sig[max(0, k - 3):k + 7]
    return float(b.max() - np.median(a)) if len(a) and len(b) else 0.0
rng = np.random.default_rng(1)
rand = rng.uniform(2, nf * 0.05 - 2, 400)
res = {}
for name, sig in [("high", high), ("mid", mid), ("low", low)]:
    e = np.array([rise(sig, t) for t in ev]); r = np.array([rise(sig, t) for t in rand])
    res[name] = dict(event_median_rise_db=round(float(np.median(e)), 2), random_median_rise_db=round(float(np.median(r)), 2),
                     event_frac_rise_gt6db=round(float((e > 6).mean()), 3), random_frac_rise_gt6db=round(float((r > 6).mean()), 3))
res["n_events"] = len(ev)
res["band_db_pct"] = {k: [round(float(v), 1) for v in np.percentile(s, [10, 50, 90])] for k, s in [("low", low), ("mid", mid), ("high", high)]}
# high-band transient rate: onsets where high band jumps > 8 dB over previous 0.5 s median
on = 0; last = -9
for k in range(10, nf):
    if high[k] - np.median(high[k - 10:k]) > 8 and (k - last) * 0.05 > 0.3: on += 1; last = k
res["hf_onsets_per_min"] = round(on / (nf * 0.05 / 60), 1)
json.dump(res, open(out, "w"), indent=1); print(json.dumps(res))
