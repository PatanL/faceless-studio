"""House-style ("Lantern & Ink") frame metrics for one MP4: the automatic half of
experiments/kurz-style/JUDGE_RUBRIC.md (STYLE_BIBLE.md section 13.1), lean enough for the QA gate.

usage: <python with numpy + opencv + Pillow> -I pipeline/qa/house_metrics.py <video.mp4> <outdir>
       -> <outdir>/house_metrics.json (also printed)

Same definitions as tools/house/judge_metrics.sh + judge_summary.py, so the numbers match the judge's
JUDGE_METRICS.json (checked on orca_full_v2 and the old-kit orca, see pipeline/qa/README.md):
  P*  palette (tools/house/palette_check.py, house/palette.json) on the 2 s grid, medians
  D1/D2 shapes / micro-details (tools/tis/density.py)   D3 small specks (judge_summary.py)
  D4/D5 edge density / outline response (tools/tis/frame_metrics.metrics, imported)
  M1/M2 alive / longest near-still run, M5 hard cuts (tools/kurz-bio/motion.py + motion_summary.py, 30 fps 256x144)
  M3/M4 seconds per new composition / per visible change (tools/tis/gridchange.py)
What is left out on purpose: audio (the gate's loudness check covers A1/A2) and the scdet transition stats.

Standalone on purpose (run with -I; no `pipeline` import): the gate runs it in a python that has opencv (on the Spark
~/studio/venvs/r2), because the gate's own venv has numpy only. Budget: nice 10, one ffmpeg at a time with 2 threads,
OMP/cv2 2 threads, CPU only. About 1-2 min for an 85 s 1080x1920 Short.
"""
import glob
import json
import os
import subprocess
import sys

os.environ["CUDA_VISIBLE_DEVICES"] = ""
for _k in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ.setdefault(_k, "2")
try:
    if os.getpriority(os.PRIO_PROCESS, 0) < 10:
        os.setpriority(os.PRIO_PROCESS, 0, 10)
except (AttributeError, OSError):
    pass

import numpy as np  # noqa: E402
import cv2  # noqa: E402
from PIL import Image  # noqa: E402

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
KS = os.path.join(REPO, "experiments", "kurz-style")
sys.path.insert(0, os.path.join(KS, "tools", "house"))
sys.path.insert(0, os.path.join(KS, "tools", "tis"))
from oklab import hex_to_rgb01, rgb_to_oklab  # noqa: E402
from frame_metrics import metrics as frame_metrics  # noqa: E402

cv2.setNumThreads(2)
GRID_SPF = 2.0   # one frame every 2 s (judge grid)
MOTION_FPS = 30
MW, MH = 256, 144


def ffmpeg() -> str:
    env = os.environ.get("FFMPEG")
    if env:
        return env
    local = os.path.expanduser("~/studio/bin/ffmpeg")
    return local if os.path.isfile(local) else "ffmpeg"


# ------------------------------------------------------------------ palette (tools/house/palette_check.py)

def _palette_segments(path: str):
    pal = json.load(open(path))["ramps"]
    tok = {t["token"]: rgb_to_oklab(hex_to_rgb01(t["hex"])) for r in pal.values() for t in r}
    segs = set()
    for r in pal.values():
        for a, b in zip(r[:-1], r[1:]):
            segs.add((a["token"], b["token"]))
    darks = [t["token"] for t in pal["ink"] + pal["dusk"]]
    lights = ["amber-4", "amber-5", "bone-2", "tide-5"]
    for t in tok:
        for d in darks + lights:
            if d != t:
                segs.add(tuple(sorted((t, d))))
    segs = sorted(segs)
    A = np.array([tok[a] for a, b in segs])
    B = np.array([tok[b] for a, b in segs])
    D = B - A
    return A, D, (D * D).sum(1) + 1e-12


def _seg_dist(P, A, D, DD):
    best = np.full(len(P), np.inf)
    for k in range(0, len(A), 64):
        a, d, dd = A[k:k + 64], D[k:k + 64], DD[k:k + 64]
        t = np.clip(((P[:, None, :] - a[None]) * d[None]).sum(2) / dd[None], 0, 1)
        q = a[None] + t[..., None] * d[None]
        best = np.minimum(best, np.sqrt(((P[:, None, :] - q) ** 2).sum(2)).min(1))
    return best


def palette_row(f: str, segs, tol: float = 0.04) -> dict:
    im = Image.open(f).convert("RGB")
    w, h = im.size
    s = 320 / max(w, h)
    sm = np.asarray(im.resize((max(1, int(w * s)), max(1, int(h * s))), Image.BILINEAR)).reshape(-1, 3)
    rgb = sm.astype(np.float64) / 255
    dist = _seg_dist(rgb_to_oklab(rgb), *segs)
    mx, mn = rgb.max(1), rgb.min(1)
    S = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-9), 0)
    V = mx
    r, g, b = rgb.T
    d = np.maximum(mx - mn, 1e-9)
    H = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    ch = (S > 0.25) & (V > 0.2)
    hb = np.bincount((H[ch] // 30).astype(int) % 12, minlength=12) / max(1, ch.sum())
    return dict(conform=round(float((dist <= tol).mean()), 3), vm_share=round(float(hb[8:11].sum()), 3),
                sat_chroma=round(float(np.median(S[ch])) if ch.any() else 0, 2),
                near_white=round(float(((V > 0.92) & (S < 0.15)).mean()), 4),
                pure_white=round(float((sm.min(1) >= 250).mean()), 4), black=round(float((V < 0.05).mean()), 4),
                grey=round(float(((S < 0.20) & (V > 0.20) & (V <= 0.92)).mean()), 3), hue_fam=int((hb >= 0.03).sum()))


# ------------------------------------------------------------------ density (tools/tis/density.py) + specks (judge_summary.py)

def density_row(f: str) -> tuple[int, int]:
    im = cv2.resize(cv2.imread(f), (960, 540), interpolation=cv2.INTER_AREA)
    im = cv2.bilateralFilter(im, 5, 20, 5)
    lab = cv2.cvtColor(im, cv2.COLOR_BGR2LAB).reshape(-1, 3).astype(np.float32)
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    _, lbl, _ = cv2.kmeans(lab, 16, None, crit, 2, cv2.KMEANS_PP_CENTERS)
    lbl = lbl.reshape(540, 960)
    shapes = micro = 0
    for k in range(16):
        _, _, stats, _ = cv2.connectedComponentsWithStats((lbl == k).astype(np.uint8), connectivity=8)
        a = stats[1:, cv2.CC_STAT_AREA]
        shapes += int((a >= 150).sum())
        micro += int(((a >= 4) & (a < 150)).sum())
    return shapes, micro


def specks_row(f: str) -> int:
    a = cv2.imread(f).astype(np.float32)
    L = a @ np.array([.0722, .7152, .2126], np.float32)
    L = cv2.resize(L, (1920, 1080), interpolation=cv2.INTER_AREA) if L.shape[1] != 1920 else L
    small = cv2.resize(L, (L.shape[1] // 4, L.shape[0] // 4), interpolation=cv2.INTER_AREA)
    bg = cv2.resize(cv2.medianBlur(np.clip(small, 0, 255).astype(np.uint8), 15).astype(np.float32), (L.shape[1], L.shape[0]))
    _, _, st, _ = cv2.connectedComponentsWithStats(((L - bg) > 12).astype(np.uint8), connectivity=8)
    a_ = st[1:, cv2.CC_STAT_AREA]
    return int(((a_ >= 6) & (a_ <= 400)).sum())


# ------------------------------------------------------------------ cadence (tools/tis/gridchange.py)

def gridchange(files: list[str]) -> dict:
    th = [np.asarray(Image.open(f).convert("L").resize((96, 54), Image.BILINEAR), dtype=np.float32) for f in files]
    D = np.array([np.abs(a - b).mean() for a, b in zip(th, th[1:])])
    if not len(D):
        return {}
    same, new = D < 6, D >= 25
    run = best = 0
    for x in same:
        run = run + 1 if x else 0
        best = max(best, run)
    n = len(D)
    # judge_summary.py parses these from gridchange.txt printed with one decimal
    return {"sec_per_new": round(n * GRID_SPF / max(1, new.sum()), 1),
            "sec_per_change": round(n * GRID_SPF / max(1, (~same).sum()), 1), "longest_hold_s": int(round(best * GRID_SPF))}


# ------------------------------------------------------------------ motion (tools/kurz-bio/motion.py + motion_summary.py)

def motion(mp4: str) -> dict:
    cmd = [ffmpeg(), "-nostdin", "-loglevel", "error", "-threads", "2", "-i", mp4, "-an",
           "-vf", f"fps={MOTION_FPS},scale={MW}:{MH},format=gray", "-f", "rawvideo", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    prev = None
    mad, chg, hist = [], [], []
    while True:
        buf = p.stdout.read(MW * MH)
        if len(buf) < MW * MH:
            break
        a = np.frombuffer(buf, np.uint8).reshape(MH, MW).astype(np.float32)
        hist.append(np.histogram(a, 32, (0, 256))[0])
        if prev is not None:
            d = np.abs(a - prev)
            mad.append(d.mean())
            chg.append((d > 6).mean())
        else:
            mad.append(0.0)
            chg.append(0.0)
        prev = a
    p.wait()
    mad, chg = np.array(mad, np.float32), np.array(chg, np.float32)
    n = len(mad)
    if n < 3:
        return {}
    hist = np.array(hist, np.float32)
    h = hist / hist.sum(1, keepdims=True)
    hd = np.r_[0, 0.5 * np.abs(h[1:] - h[:-1]).sum(1)]
    cuts = []
    for i in range(2, n - 2):
        loc = np.r_[mad[max(1, i - 8):i - 1], mad[i + 2:i + 9]]
        base = np.median(loc) if len(loc) else 0
        if mad[i] > 10 and mad[i] > 4 * base + 3 and hd[i] > 0.12:
            if not cuts or i - cuts[-1] > MOTION_FPS * 0.3:
                cuts.append(i)
    static = mad < 0.25
    runs, cur = [], 0
    for s in static:
        if s:
            cur += 1
        else:
            runs.append(cur)
            cur = 0
    runs.append(cur)
    dur = round(n / MOTION_FPS, 1)
    frozen = round(float((chg[1:] == 0).mean() * 100), 2)
    return {"duration_s": dur, "hard_cuts": len(cuts), "cut_times": [round(i / MOTION_FPS, 2) for i in cuts],
            "hard_cuts_per_min": round(len(cuts) / max(dur / 60, 1e-6), 2), "frozen_pct": frozen,
            "alive_pct": round(100 - frozen, 2), "quiet_pct": round(float(static.mean() * 100), 2),
            "longest_quiet_s": round(float(max(runs) / MOTION_FPS), 2)}


# ------------------------------------------------------------------ main

def measure(mp4: str, out: str) -> dict:
    grid = os.path.join(out, "grid")
    os.makedirs(grid, exist_ok=True)
    for f in glob.glob(os.path.join(grid, "g_*.jpg")):
        os.remove(f)
    r = subprocess.run([ffmpeg(), "-nostdin", "-hide_banner", "-loglevel", "error", "-threads", "2", "-i", mp4, "-an",
                        "-vf", f"fps={1 / GRID_SPF}", "-q:v", "3", os.path.join(grid, "g_%05d.jpg")],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"ffmpeg grid failed: {r.stderr[-300:]}")
    files = sorted(glob.glob(os.path.join(grid, "g_*.jpg")))
    if not files:
        raise RuntimeError("no grid frames")
    med = lambda xs: float(np.median(xs)) if len(xs) else float("nan")
    m = {"v": 1, "mp4": mp4, "frames": len(files), "grid_spf": GRID_SPF}
    segs = _palette_segments(os.path.join(KS, "house", "palette.json"))
    pc = [palette_row(f, segs) for f in files]
    for k in ("conform", "vm_share", "sat_chroma", "grey", "near_white", "pure_white", "black", "hue_fam"):
        m["pal_" + k] = round(med([r[k] for r in pc]), 4)
    fm = [x for x in (frame_metrics(f) for f in files) if x]
    for k in ("edge_den", "outline", "blur_frac", "grad_frac", "n_colours"):
        m["fm_" + k] = round(med([r[k] for r in fm]), 4)
    dens = [density_row(f) for f in files]
    m["density_shapes"] = med([d[0] for d in dens])
    m["density_micro"] = med([d[1] for d in dens])
    m["specks_small"] = med([specks_row(f) for f in files])
    m.update(gridchange(files))
    m.update(motion(mp4))
    m["per_frame"] = [{"t": round(i * GRID_SPF, 1), "hue_fam": p["hue_fam"], "sat": p["sat_chroma"],
                       "outline": round(f.get("outline", 0), 3), "edge": round(f.get("edge_den", 0), 4)}
                      for i, (p, f) in enumerate(zip(pc, fm))]
    return m


def main(argv) -> int:
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    mp4, out = argv
    os.makedirs(out, exist_ok=True)
    m = measure(mp4, out)
    with open(os.path.join(out, "house_metrics.json"), "w") as f:
        json.dump(m, f, indent=1)
    print(json.dumps({k: v for k, v in m.items() if k not in ("per_frame", "cut_times")}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
