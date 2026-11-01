"""Collect judge_metrics.sh outputs into JUDGE_METRICS.json and print them against the
STYLE_BIBLE.md section 13 targets (the automatic checks of JUDGE_RUBRIC.md).
usage: python -I judge_summary.py <outdir> [label]
"""
import sys, os, re, json, glob
import numpy as np, cv2

d = sys.argv[1]; label = sys.argv[2] if len(sys.argv) > 2 else os.path.basename(d.rstrip("/"))
J = lambda f: json.load(open(os.path.join(d, f)))
med = lambda xs: float(np.median(xs)) if len(xs) else float("nan")
m = {"label": label}

pc = J("palette.json")
for k in ("conform", "vm_share", "sat_chroma", "grey", "near_white", "pure_white", "black", "hue_fam"):
    m["pal_" + k] = round(med([r[k] for r in pc]), 4)
fm = J("fm.json").values()
for k in ("edge_den", "outline", "blur_frac", "grad_frac", "n_colours"):
    m["fm_" + k] = round(med([r[k] for r in fm]), 4)
m["fm_val_p50"] = round(med([r["val"][1] for r in fm]), 3)

rows = [l.split() for l in open(os.path.join(d, "density.txt")) if l.strip() and not l.startswith("frame")]
m["density_shapes"] = med([int(r[1]) for r in rows]); m["density_micro"] = med([int(r[2]) for r in rows])

# small specks: connected components brighter than the local background (kurz-bio/particles.py, cv2 port)
sp = []
for f in sorted(glob.glob(os.path.join(d, "grid", "*.jpg"))):
    a = cv2.imread(f).astype(np.float32); L = a @ np.array([.0722, .7152, .2126], np.float32)
    L = cv2.resize(L, (1920, 1080), interpolation=cv2.INTER_AREA) if L.shape[1] != 1920 else L
    small = cv2.resize(L, (L.shape[1] // 4, L.shape[0] // 4), interpolation=cv2.INTER_AREA)
    bg = cv2.resize(cv2.medianBlur(np.clip(small, 0, 255).astype(np.uint8), 15).astype(np.float32), (L.shape[1], L.shape[0]))
    n, lab, st, _ = cv2.connectedComponentsWithStats(((L - bg) > 12).astype(np.uint8), connectivity=8)
    a_ = st[1:, cv2.CC_STAT_AREA]; sp.append(int(((a_ >= 6) & (a_ <= 400)).sum()))
m["specks_small"] = med(sp)

g = open(os.path.join(d, "gridchange.txt")).read()
x = re.search(r"seconds per NEW picture ([\d.]+); seconds per visible change \(evolved\|new\) ([\d.]+); longest hold (\d+)", g)
if x: m["sec_per_new"], m["sec_per_change"], m["longest_hold_s"] = float(x[1]), float(x[2]), int(x[3])

ms = J("motion_summary.json"); z = np.load(os.path.join(d, "motion.npz")); chg = z["chg"][1:]
m["duration_s"] = ms["duration"]; m["hard_cuts"] = ms["n_cuts"]
m["hard_cuts_per_min"] = round(ms["n_cuts"] / max(ms["duration"] / 60, 1e-6), 2)
m["frozen_pct"] = round(float((chg == 0).mean() * 100), 2)          # no pixel changes > 6 levels (256x144)
m["alive_pct"] = round(100 - m["frozen_pct"], 2)
m["quiet_pct"] = ms["pct_static_frames"]; m["longest_quiet_s"] = ms["longest_static_s"]
m["big_change_interval_s"] = ms.get("big_change_interval_s_median")
m["pan_pct"] = ms["pct_frames_global_pan"]
ce = J("scores_events.json")["stats"] if os.path.exists(os.path.join(d, "scores_events.json")) else {}
m["anim_transitions"] = ce.get("animated_transitions"); m["shot_len_median_s"] = (ce.get("shot_len_s") or {}).get("median")

lt = open(os.path.join(d, "loud.txt")).read()
x = re.search(r"Integrated loudness:\s+I:\s+([-\d.]+) LUFS", lt); m["lufs_i"] = float(x[1]) if x else None
x = re.search(r"Loudness range:\s+LRA:\s+([-\d.]+) LU", lt); m["lra"] = float(x[1]) if x else None
sl = open(os.path.join(d, "silence.txt")).read()
m["silences_045"] = len(re.findall(r"silence_end", sl))
json.dump(m, open(os.path.join(d, "JUDGE_METRICS.json"), "w"), indent=1)

# id, key, test, target text (keep in sync with STYLE_BIBLE.md section 13)
T = [("P1", "pal_conform", lambda v: v >= 0.85, ">= 0.85"),
     ("P2", "pal_vm_share", lambda v: v <= 0.08, "<= 0.08"),
     ("P3", "pal_sat_chroma", lambda v: 0.66 <= v <= 0.88, "0.66-0.88"),
     ("P4", "pal_grey", lambda v: v <= 0.04, "<= 0.04"),
     ("P5", "pal_hue_fam", lambda v: v >= 3, ">= 3"),
     ("P6", "pal_near_white", lambda v: v <= 0.015, "<= 0.015"),
     ("P7", "pal_pure_white", lambda v: v <= 0.003, "<= 0.003"),
     ("P8", "pal_black", lambda v: v <= 0.005, "<= 0.005"),
     ("D1", "density_shapes", lambda v: v >= 110, ">= 110"),
     ("D2", "density_micro", lambda v: v >= 600, ">= 600"),
     ("D3", "specks_small", lambda v: v >= 120, ">= 120"),
     ("D4", "fm_edge_den", lambda v: 0.040 <= v <= 0.08, "0.040-0.08"),
     ("D5", "fm_outline", lambda v: v <= 0.05, "<= 0.05"),
     ("M1", "alive_pct", lambda v: v >= 95, ">= 95 (pass >= 80)"),
     ("M2", "longest_quiet_s", lambda v: v <= 2.5, "<= 2.5"),
     ("M3", "sec_per_new", lambda v: v <= 3.5, "<= 3.5 (long-form <= 5)"),
     ("M4", "sec_per_change", lambda v: 2.0 <= v <= 4.5, "2.0-4.5"),
     ("M5", "hard_cuts_per_min", lambda v: v <= 2, "<= 2"),
     ("A1", "lufs_i", lambda v: v is not None and -15 <= v <= -13, "-14 +/- 1"),
     ("A2", "lra", lambda v: v is not None and v <= 4, "<= 4"),
     ("A3", "silences_045", lambda v: v == 0, "0")]
print(f"== {label}  ({m.get('duration_s')} s)")
npass = 0
for i, k, t, txt in T:
    v = m.get(k)
    ok = (v is not None and not (isinstance(v, float) and np.isnan(v)) and t(v))
    npass += ok
    print(f"{i:3s} {k:20s} {str(v):>10s}  target {txt:18s} {'PASS' if ok else 'FAIL'}")
print(f"automatic checks passed: {npass}/{len(T)}")
