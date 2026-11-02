"""House-style ("Lantern & Ink") checks for the QA gate: explainer episodes only.

  staging      pipeline/episodes/staging.py on the built storyboard (collisions: a prop through the hero, a label on the
               caption band or on a figure, a number clipped, a label outside the safe area, a headline repeating the
               caption, freeze-then-abrupt-push, no colour shift), plus "was this storyboard built in the house style at
               all" (scene light on every scene, no `look: "legacy"` background). Violations FAIL, [echo] warnings WARN.
  house_style  the automatic metrics of experiments/kurz-style/JUDGE_RUBRIC.md (STYLE_BIBLE.md 13.1) measured on the MP4
               by pipeline/qa/house_metrics.py, against the thresholds below.

Calibration (2026-11-01, Spark, pipeline/qa/house_metrics.py; the numbers match tools/house/judge_metrics.sh):

  metric                      new orca (orca_full_v2,  old-kit orca (out/pilots  old-kit op episode   blue whale (house
                              59/100, the live look)   9x16, ~24/100)            (op-...-sperm-whale)  v2d)
  P5 hue families                 3                        1                         1                    2
  D3 small specks               192                       63.5                      45.5                231
  D4 edge density             0.058                    0.029                     0.020                0.058
  D5 outline response         0.091                    0.130                     0.150                0.094
  M5 hard cuts / min           0.71                     7.99                      1.97                 4.29
  D2 micro-details             1512                      714                       508                 1438
  M3 s per new composition      8.2                     10.6                      15.0                  5.2

FAIL lines sit between the two looks: the new orca passes every FAIL line, the old-kit orca fails five (P5, D3, D4, D5,
M5) and the old-kit operator episode four (P5, D3, D4, D5). The bible targets themselves (e.g. D5 <= 0.05, M3 <= 3.5 s)
are WARN lines: the live look does not reach them all yet (orca_full_v2: D5 0.091, M3 8.2 s), so they tell the
reviewer where it is short of the target without blocking the video. D5's FAIL margin is the narrowest (0.12 vs
0.091 / 0.13): re-calibrate it when the look changes (rerun house_metrics.py on the new and old orca).
"""
from __future__ import annotations

import json
import os
import pathlib
import shutil
import subprocess

from .util import REPO, read_json, rel

# id: (metric key, FAIL test, WARN test, text). A test returns True when the value is BAD.
THRESHOLDS = {
    "P3": ("pal_sat_chroma", lambda v: not 0.55 <= v <= 0.95, lambda v: not 0.66 <= v <= 0.88,
           "chromatic saturation: FAIL outside 0.55-0.95, WARN outside 0.66-0.88"),
    "P4": ("pal_grey", lambda v: v > 0.08, lambda v: v > 0.04, "grey mid-tone share: FAIL > 0.08, WARN > 0.04"),
    "P5": ("pal_hue_fam", lambda v: v < 2, lambda v: v < 3, "hue families per frame: FAIL < 2, WARN < 3"),
    "P7": ("pal_pure_white", None, lambda v: v > 0.003, "pure-white share: WARN > 0.003"),
    "D1": ("density_shapes", None, lambda v: v < 110, "shapes per frame: WARN < 110"),
    "D2": ("density_micro", lambda v: v < 400, lambda v: v < 600, "micro-details per frame: FAIL < 400, WARN < 600"),
    "D3": ("specks_small", lambda v: v < 100, lambda v: v < 120, "small specks per frame: FAIL < 100, WARN < 120"),
    "D4": ("fm_edge_den", lambda v: v < 0.035, lambda v: not 0.040 <= v <= 0.08,
           "edge density: FAIL < 0.035, WARN outside 0.040-0.08"),
    "D5": ("fm_outline", lambda v: v > 0.12, lambda v: v > 0.05, "outline response: FAIL > 0.12, WARN > 0.05"),
    "M1": ("alive_pct", lambda v: v < 80, lambda v: v < 95, "frames with any change %: FAIL < 80, WARN < 95"),
    "M2": ("longest_quiet_s", lambda v: v > 6, lambda v: v > 2.5, "longest near-still run s: FAIL > 6, WARN > 2.5"),
    "M3": ("sec_per_new", None, lambda v: v > 3.5, "s per new composition: WARN > 3.5 (Shorts target)"),
    "M4": ("sec_per_change", None, lambda v: not 2.0 <= v <= 4.5, "s per visible change: WARN outside 2.0-4.5"),
    "M5": ("hard_cuts_per_min", lambda v: v > 6, lambda v: v > 2, "hard cuts per minute: FAIL > 6, WARN > 2"),
}
METRICS_SCRIPT = REPO / "pipeline" / "qa" / "house_metrics.py"


def is_explainer(niche: str | None, sb: dict | None) -> bool:
    if niche and "horror" in niche:
        return False
    if niche and "explainer" in niche:
        return True
    bgs = [((s.get("background") or {}).get("name") or "") for s in (sb or {}).get("scenes", [])]
    return any(b.startswith("explainer/") for b in bgs)


def on_spark(r: pathlib.Path) -> bool:
    if os.environ.get("STUDIO_LOCAL") == "1":
        return True
    return os.path.realpath(r) == os.path.realpath(os.path.expanduser("~/studio/app"))


def chk(status, value=None, threshold=None, detail=""):
    d = {"status": status, "value": value}
    if threshold is not None:
        d["threshold"] = threshold
    if detail:
        d["detail"] = detail
    return d


# ------------------------------------------------------------------ storyboard: built in the house style + staging

def house_built(sb: dict) -> list[str]:
    """reasons the storyboard is not a house-style (Lantern & Ink) build; [] = it is"""
    out = []
    scenes = sb.get("scenes") or []
    unlit = [s.get("id") for s in scenes if not s.get("light")]
    if unlit:
        out.append(f"{len(unlit)}/{len(scenes)} scenes have no scene light ({', '.join(map(str, unlit[:5]))}): "
                   f"the house pass (pipeline/episodes/house.py) did not run")
    legacy = [s.get("id") for s in scenes if ((s.get("background") or {}).get("props") or {}).get("look") == "legacy"]
    if legacy:
        out.append(f"legacy background look in {', '.join(map(str, legacy[:5]))}")
    return out


def check_staging(sb: dict | None, niche: str | None) -> dict:
    if not is_explainer(niche, sb):
        return chk("PASS", None, detail="not an explainer: the house style does not apply")
    if not sb or not sb.get("scenes"):
        return chk("WARN", None, detail="no storyboard.json: staging not checked")
    from pipeline.episodes import staging
    not_house = house_built(sb)
    try:
        msgs = staging.check(sb)
    except Exception as e:  # noqa: BLE001 - a storyboard the checker cannot read is a FAIL, not a crash
        return chk("FAIL", None, "pipeline/episodes/staging.py", f"staging checker error: {e}")
    fails = not_house + [m for m in msgs if not staging.is_warning(m)]
    warns = [m for m in msgs if staging.is_warning(m)]
    st = "FAIL" if fails else "WARN" if warns else "PASS"
    return chk(st, {"fail": fails[:20], "warn": warns[:10]},
               "house-built storyboard and no staging violation (pipeline/episodes/staging.py; [echo] = WARN)",
               f"{len(fails)} violation(s), {len(warns)} warning(s)")


# ------------------------------------------------------------------ video: JUDGE_RUBRIC automatic metrics

def metrics_python() -> str | None:
    """a python with numpy + opencv + Pillow: $STUDIO_HOUSE_PY, the Spark's r2 venv, then this interpreter"""
    import sys
    cands = [os.environ.get("STUDIO_HOUSE_PY"), os.path.expanduser("~/studio/venvs/r2/bin/python"), sys.executable,
             shutil.which("python3")]
    for c in cands:
        if not c or not os.path.isfile(c):
            continue
        p = subprocess.run([c, "-I", "-c", "import cv2, PIL, numpy"], capture_output=True)
        if p.returncode == 0:
            return c
    return None


def measure(r: pathlib.Path, mp4, qd: pathlib.Path, log=print) -> dict:
    py = metrics_python()
    if not py:
        raise FileNotFoundError("no python with opencv + Pillow (set STUDIO_HOUSE_PY)")
    out = qd / "house"
    out.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "CUDA_VISIBLE_DEVICES": "", "OMP_NUM_THREADS": "2", "MKL_NUM_THREADS": "2",
           "OPENBLAS_NUM_THREADS": "2"}
    script = r / "pipeline" / "qa" / "house_metrics.py"
    script = script if script.is_file() else METRICS_SCRIPT
    log(f"house metrics: {py} {rel(r, script)}")
    p = subprocess.run(["nice", "-n", "10", py, "-I", str(script), str(mp4), str(out)], capture_output=True, text=True,
                       env=env, timeout=1800)
    if p.returncode != 0:
        raise RuntimeError(f"house_metrics.py failed: {(p.stderr or p.stdout)[-400:]}")
    shutil.rmtree(out / "grid", ignore_errors=True)   # 40+ full-res JPGs; the gate keeps only the numbers
    return read_json(out / "house_metrics.json") or {}


def evaluate(m: dict) -> tuple[str, dict, list[str], list[str]]:
    rows, fails, warns = {}, [], []
    for i, (key, ft, wt, txt) in THRESHOLDS.items():
        v = m.get(key)
        if v is None or (isinstance(v, float) and v != v):
            rows[i] = {"key": key, "value": None, "status": "WARN"}
            warns.append(f"{i} {key} not measured")
            continue
        st = "FAIL" if ft and ft(v) else "WARN" if wt and wt(v) else "PASS"
        rows[i] = {"key": key, "value": v, "status": st}
        if st == "FAIL":
            fails.append(f"{i} {key} {v} ({txt})")
        elif st == "WARN":
            warns.append(f"{i} {key} {v} ({txt})")
    st = "FAIL" if fails else "WARN" if warns else "PASS"
    return st, rows, fails, warns


def check_house_style(r: pathlib.Path, mp4, qd: pathlib.Path, niche: str | None, sb: dict | None, log=print) -> dict:
    if not is_explainer(niche, sb):
        return chk("PASS", None, detail="not an explainer: the house style does not apply")
    thr = "JUDGE_RUBRIC automatic metrics, thresholds in pipeline/qa/house_style.py THRESHOLDS"
    if not on_spark(r) and not os.environ.get("STUDIO_HOUSE_PY"):
        # the Mac is reserved for other work (BRIEF): measure only on the Spark, or when asked to
        return chk("WARN", None, thr, "not measured off the Spark (set STUDIO_HOUSE_PY to a python with opencv)")
    try:
        m = measure(r, mp4, qd, log)
    except FileNotFoundError as e:
        # the Spark must measure it (the gate there is the ship gate); elsewhere (Mac tests) it is a warning
        return chk("FAIL" if on_spark(r) else "WARN", None, thr, f"not measured: {e}")
    except (RuntimeError, subprocess.TimeoutExpired, OSError, ValueError) as e:
        return chk("FAIL", None, thr, f"not measured: {e}")
    st, rows, fails, warns = evaluate(m)
    val = {i: x["value"] for i, x in rows.items()}
    val["status"] = {i: x["status"] for i, x in rows.items() if x["status"] != "PASS"}
    val["metrics_file"] = rel(r, qd / "house" / "house_metrics.json")
    detail = "; ".join(["FAIL " + f for f in fails] + ["WARN " + w for w in warns]) or "every metric on target"
    return chk(st, val, thr, detail)


def main(argv=None) -> int:
    """python -m pipeline.qa.house_style <metrics.json>: re-evaluate a house_metrics.json / JUDGE_METRICS.json"""
    import sys
    argv = sys.argv[1:] if argv is None else argv
    for p in argv:
        m = json.load(open(p))
        st, rows, fails, warns = evaluate(m)
        print(f"{p}: {st}")
        for i, x in rows.items():
            print(f"  {x['status']:4} {i} {x['key']:18} {x['value']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
