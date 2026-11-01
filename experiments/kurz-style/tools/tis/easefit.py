"""Fit a camera move from motion.py output to standard easing curves.
usage: python -I easefit.py <motion.csv> <t0> <t1> <zoom|pan> [<t0> <t1> <zoom|pan> ...]
Progress p(t) = cumulative log-scale (zoom) or cumulative |pan| path length (pan),
normalised to 0..1 over [t0, t1]. Reports RMSE vs linear, ease-out sine/quad/cubic/quart/expo,
ease-in-out sine/cubic, and the time to reach 50 % / 90 % of the move.
"""
import sys, csv, math
import numpy as np

curves = {
    "linear": lambda x: x,
    "out-sine": lambda x: np.sin(x * math.pi / 2),
    "out-quad": lambda x: 1 - (1 - x) ** 2,
    "out-cubic": lambda x: 1 - (1 - x) ** 3,
    "out-quart": lambda x: 1 - (1 - x) ** 4,
    "out-expo": lambda x: np.where(x >= 1, 1, 1 - 2 ** (-10 * x)),
    "inout-sine": lambda x: -(np.cos(math.pi * x) - 1) / 2,
    "inout-cubic": lambda x: np.where(x < 0.5, 4 * x ** 3, 1 - (-2 * x + 2) ** 3 / 2),
}
rows = list(csv.DictReader(open(sys.argv[1])))
t = np.array([float(r["t"]) for r in rows])
ls = np.log(np.array([float(r["s"]) for r in rows]))
pan = np.hypot(np.array([float(r["tx"]) for r in rows]), np.array([float(r["ty"]) for r in rows]))
a = sys.argv[2:]
for i in range(0, len(a), 3):
    t0, t1, kind = float(a[i]), float(a[i + 1]), a[i + 2]
    m = (t >= t0) & (t <= t1)
    inc = np.abs(ls[m]) if kind == "zoom" else pan[m]
    cum = np.cumsum(inc); p = cum / cum[-1]
    x = (t[m] - t[m][0]) / (t[m][-1] - t[m][0])
    fits = sorted(((float(np.sqrt(np.mean((f(x) - p) ** 2))), n) for n, f in curves.items()))
    tot = (math.exp(np.sum(ls[m])) - 1) * 100 if kind == "zoom" else cum[-1]
    t50 = t[m][np.searchsorted(p, 0.5)] - t[m][0]; t90 = t[m][np.searchsorted(p, 0.9)] - t[m][0]
    print(f"{sys.argv[1].split('/')[-1]} {t0}-{t1}s {kind}: total {tot:+.1f}{'%' if kind=='zoom' else ' px'}  "
          f"50% at {t50:.2f}s, 90% at {t90:.2f}s of {t1-t0:.2f}s  best: " + ", ".join(f"{n} {e:.3f}" for e, n in fits[:3]))
