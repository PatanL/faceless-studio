"""One-variable experiments (OPERATOR_DESIGN 5.14, 5.15, 9.7).

  python -m pipeline.analytics.experiments assign --date YYYY-MM-DD --slot a|b [--slug S]
  python -m pipeline.analytics.experiments open --dimension hook|structure|visual [--variable K --treatment V] [--confirm]
  python -m pipeline.analytics.experiments decide [--dry-run]
  python -m pipeline.analytics.experiments status

Rules: one running experiment at a time; every other variable comes from data/learned/rules.json. Arms alternate
by slot and day: on an even local day (by date ordinal, so consecutive days always alternate) slot A = control,
B = treatment; odd days swap. Decision at min_n_per_arm (extend up to max_n_per_arm while inconclusive):
adopt if the treatment median of the primary metric beats control by >= 10 % relative AND the treatment wins >= 2/3
of the same-day pairs AND no secondary metric is worse by > 15 %; reject if control wins by the same rule; else
inconclusive at max n (control kept). Synthetic / dry-run metrics never count.
"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import sys
from datetime import date

from ._common import (EXIT_NOTHING, EXIT_OK, EXIT_USAGE, ROOT, config, dpath, iso, is_real, jsonl_append, jsonl_read,
                      median, now_utc, read_json, rpath, write_json_atomic)

VARIABLES = {
    "hook.type": ["source"] + [f"H{i}" for i in range(1, 22)],
    "hook.max_words": list(range(5, 15)),
    "hook.visual": ["subject_full", "subject_eye", "you_vs_subject", "headline_only"],
    "structure.skeleton": ["source", "playbook_list", "playbook_ladder"],
    "structure.turnstile_pct": list(range(40, 71)),
    "structure.ending": ["loop_callback", "stinger_fact", "twist_question"],
    "pace.wpm": list(range(170, 216)),
    "pace.rehook_s": "float 6-12",
    "visual.max_hold_s": "float 1.5-3.0",
    "visual.cover": ["scale", "eye", "abyss", "headline"],
    "visual.shot_mix": ["creature_heavy", "infographic_heavy", "balanced"],
    "visual.caption_style": ["pill", "page"],
}
FLOAT_RANGES = {"pace.rehook_s": (6.0, 12.0), "visual.max_hold_s": (1.5, 3.0)}
DEFAULTS = {"hook.type": "source", "hook.max_words": 12, "structure.skeleton": "source", "pace.rehook_s": 9,
            "visual.max_hold_s": 3.0, "visual.cover": "scale", "visual.shot_mix": "balanced"}
# control values for variables the 5.15 defaults leave out (what the current kit/prompts already do)
BASELINE = {"hook.visual": "subject_full", "structure.turnstile_pct": 60, "structure.ending": "loop_callback",
            "pace.wpm": 195, "visual.caption_style": "page"}


def baseline(var: str, rules: dict | None = None):
    rules = rules if rules is not None else load_rules()["defaults"]
    return rules.get(var, DEFAULTS.get(var, BASELINE.get(var)))

# Ordered backlog per dimension: (variable, treatment, hypothesis, primary). The first one not yet run is proposed.
CANDIDATES = {
    "hook": [
        ("hook.max_words", 8, "A shorter first line (<= 8 words) lands the premise before the 1-2 s swipe", "youtube.derived.hold_3s"),
        ("hook.visual", "you_vs_subject", "Showing YOU next to the subject in frame 0 makes the stakes readable at a glance", "youtube.derived.hold_3s"),
        ("hook.type", "H6", "The unnamed-predator paradox hook beats copying the source's hook shape", "youtube.derived.hold_3s"),
    ],
    "structure": [
        ("pace.rehook_s", 7.0, "A re-hook every 7 s (vs 9) flattens the mid-video decline", "youtube.avg_view_pct"),
        ("structure.ending", "stinger_fact", "A stinger fact ending lifts end hold vs the loop callback", "youtube.derived.completion"),
        ("structure.skeleton", "playbook_ladder", "The PLAYBOOK escalation ladder holds better than the source order", "youtube.avg_view_pct"),
    ],
    "visual": [
        ("visual.max_hold_s", 2.0, "No visual hold over 2.0 s (vs 3.0) reduces mid-scene drops", "youtube.avg_view_pct"),
        ("visual.cover", "eye", "An eye close-up cover/frame 0 beats the scale cover", "youtube.derived.hold_3s"),
        ("visual.shot_mix", "creature_heavy", "More creature shots, fewer infographics, holds attention", "youtube.avg_view_pct"),
    ],
}
SECONDARY = ["youtube.avg_view_pct", "youtube.views@7d"]
PROPOSAL_TARGET = {"hook": "research/corpus/explainer/PLAYBOOK.md", "structure": "research/corpus/explainer/PLAYBOOK.md",
                   "pace": "research/corpus/explainer/PLAYBOOK.md", "visual": "pipeline/prompts/shots_explainer.md"}

LEDGER = lambda: dpath("experiments.jsonl")
RULES = lambda: dpath("learned", "rules.json")


def validate(var: str, val) -> object:
    if var not in VARIABLES:
        raise ValueError(f"unknown variable {var!r}; allowed: {', '.join(VARIABLES)}")
    if var in FLOAT_RANGES:
        lo, hi = FLOAT_RANGES[var]
        v = float(val)
        if not lo <= v <= hi:
            raise ValueError(f"{var} must be {lo}-{hi}")
        return v
    allowed = VARIABLES[var]
    if isinstance(allowed[0], int) and not isinstance(allowed[0], bool):
        v = int(val)
    else:
        v = str(val)
    if v not in allowed:
        raise ValueError(f"{var}={val!r} not in {allowed}")
    return v


# ---------------------------------------------------------------- ledger views
def rows() -> list[dict]:
    return jsonl_read(LEDGER())


def experiments() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for r in rows():
        if r.get("type") == "experiment":
            out[r["experiment_id"]] = r
    return out


def running() -> dict | None:
    run = [e for e in experiments().values() if e.get("status") == "running"]
    return sorted(run, key=lambda e: e["experiment_id"])[-1] if run else None


def next_id() -> str:
    ids = [int(m.group(1)) for e in experiments() if (m := re.match(r"EXP-(\d+)", e))]
    return f"EXP-{(max(ids) + 1 if ids else 1):03d}"


def load_rules() -> dict:
    r = read_json(RULES())
    if r:
        return r
    base = (read_json(rpath("pipeline", "ops", "config.default.json"), {}) or {}).get("rules_defaults") or DEFAULTS
    return {"v": 1, "updated_at": None, "defaults": dict(base), "notes": [], "history": []}


# ---------------------------------------------------------------- assign
def arm_for(day: str, slot: str) -> str:
    even = date.fromisoformat(day).toordinal() % 2 == 0
    a_is_control = even
    return "control" if (slot == "a") == a_is_control else "treatment"


def assign(day: str, slot: str, slug: str | None = None, write: bool = True) -> dict:
    exp = running()
    if not exp:
        return {}
    for r in rows():
        if (r.get("type") == "assignment" and r.get("experiment_id") == exp["experiment_id"]
                and r.get("date") == day and r.get("slot") == slot):
            if slug and r.get("slug") != slug and write:
                jsonl_append(LEDGER(), {**r, "at": iso(now_utc()), "slug": slug})
            return {"experiment_id": exp["experiment_id"], "arm": r["arm"],
                    "variables": {exp["variable"]: exp[r["arm"]]}}
    arm = arm_for(day, slot)
    if write:
        jsonl_append(LEDGER(), {"v": 1, "type": "assignment", "experiment_id": exp["experiment_id"], "slug": slug,
                                "date": day, "slot": slot, "arm": arm})
    return {"experiment_id": exp["experiment_id"], "arm": arm, "variables": {exp["variable"]: exp[arm]}}


# ---------------------------------------------------------------- open
def propose(dimension: str) -> dict | None:
    done = {(e["variable"], str(e["treatment"])) for e in experiments().values()}
    rules = load_rules()["defaults"]
    for var, val, hyp, primary in CANDIDATES[dimension]:
        if (var, str(val)) in done or rules.get(var) == val:
            continue
        return {"dimension": dimension, "variable": var, "control": baseline(var, rules),
                "treatment": val, "hypothesis": hyp, "primary_metric": primary}
    return None


def open_experiment(spec: dict, min_n: int = 6, max_n: int = 10) -> dict:
    if running():
        raise RuntimeError(f"{running()['experiment_id']} is still running (one experiment at a time)")
    spec = dict(spec)
    spec["treatment"] = validate(spec["variable"], spec["treatment"])
    spec["control"] = validate(spec["variable"], spec["control"])
    if spec["treatment"] == spec["control"]:
        raise ValueError("treatment equals control")
    row = {"v": 1, "type": "experiment", "experiment_id": next_id(), **spec,
           "secondary": [s for s in SECONDARY if s != spec["primary_metric"]], "window": "7d",
           "min_n_per_arm": min_n, "max_n_per_arm": max_n, "status": "running", "opened_at": iso(now_utc())}
    jsonl_append(LEDGER(), row)
    return row


# ---------------------------------------------------------------- decide
def metric_value(rows_by_key: dict, slug: str, spec: str, default_window: str):
    """'youtube.derived.hold_3s' or 'youtube.views@7d' -> value from the latest real metrics row."""
    spec, _, win = spec.partition("@")
    plat, *path = spec.split(".")
    r = rows_by_key.get((f"{slug}:{plat}", win or default_window))
    if not r:
        return None
    v = r
    for p in path:
        v = v.get(p) if isinstance(v, dict) else None
    return v


def samples(exp: dict) -> list[dict]:
    """[{slug, arm, date}] from assignments with a slug, posts rows tagged with the experiment, and variant.json."""
    eid = exp["experiment_id"]
    out: dict[str, dict] = {}
    for r in rows():
        if r.get("type") == "assignment" and r.get("experiment_id") == eid and r.get("slug"):
            out[r["slug"]] = {"slug": r["slug"], "arm": r["arm"], "date": r["date"]}
    for p in jsonl_read(dpath("posts.jsonl")):
        if p.get("experiment_id") == eid and p.get("arm") and p.get("slug") and is_real(p):
            out.setdefault(p["slug"], {"slug": p["slug"], "arm": p["arm"], "date": _slug_date(p["slug"])})
    epi = rpath("episodes")
    if os.path.isdir(epi):
        for d in os.listdir(epi):
            if d.startswith("op-"):
                v = read_json(os.path.join(epi, d, "variant.json")) or {}
                if v.get("experiment_id") == eid and v.get("arm"):
                    out.setdefault(d, {"slug": d, "arm": v["arm"], "date": _slug_date(d)})
    return list(out.values())


def _slug_date(slug: str) -> str | None:
    m = re.match(r"op-(\d{4})(\d{2})(\d{2})-", slug)
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else None


def rule(ctrl: list[float], treat: list[float], pairs: list[tuple[float, float]],
         sec: dict[str, tuple[list[float], list[float]]], min_n: int, max_n: int,
         gain: float = 0.10, pair_share: float = 2 / 3, sec_loss: float = 0.15) -> dict:
    """Pure decision rule (5.14). sec: name -> (control values, treatment values). Thresholds default to 5.14 and
    come from config `experiments.adopt_rel_gain / pair_win_share / secondary_max_rel_loss` when set."""
    n = {"control": len(ctrl), "treatment": len(treat)}
    mc, mt = median(ctrl), median(treat)
    res = {"n": n, "medians": {"control": mc, "treatment": mt}, "effect": None, "paired_wins": None}
    if min(n.values()) < min_n or mc is None or mt is None:
        res["decision"] = "pending"
        return res
    res["effect"] = round((mt - mc) / abs(mc), 4) if mc else None
    tw = sum(1 for c, t in pairs if t > c)
    cw = sum(1 for c, t in pairs if c > t)
    res["paired_wins"] = f"{tw}/{len(pairs)}"
    sec_med = {k: (median(c), median(t)) for k, (c, t) in sec.items()}
    res["secondary_medians"] = {k: {"control": c, "treatment": t} for k, (c, t) in sec_med.items()}

    def wins(a_med, b_med, a_pairs, side):  # does side "a" win against "b"?
        if b_med is None or a_med is None or b_med == 0:
            return False
        if (a_med - b_med) / abs(b_med) < gain - 1e-9:
            return False
        if not pairs or a_pairs < pair_share * len(pairs) - 1e-9:
            return False
        for c, t in sec_med.values():
            a, b = (t, c) if side == "treatment" else (c, t)
            if a is not None and b not in (None, 0) and (a - b) / abs(b) < -sec_loss:
                return False
        return True

    if wins(mt, mc, tw, "treatment"):
        res["decision"] = "adopt"
    elif wins(mc, mt, cw, "control"):
        res["decision"] = "reject"
    elif min(n.values()) >= max_n:
        res["decision"] = "inconclusive"
    else:
        res["decision"] = "extend"
    return res


def evaluate(exp: dict) -> dict:
    mrows = {}
    for r in jsonl_read(dpath("metrics.jsonl")):
        if is_real(r):
            mrows[(r.get("post_key"), r.get("window"))] = r
    win = exp.get("window", "7d")
    ss = samples(exp)
    val = lambda s, spec: metric_value(mrows, s["slug"], spec, win)
    data = [dict(s, primary=val(s, exp["primary_metric"])) for s in ss]
    data = [d for d in data if d["primary"] is not None]
    ctrl = [d["primary"] for d in data if d["arm"] == "control"]
    treat = [d["primary"] for d in data if d["arm"] == "treatment"]
    by_day: dict[str, dict] = {}
    for d in data:
        by_day.setdefault(d["date"], {})[d["arm"]] = d["primary"]
    pairs = [(v["control"], v["treatment"]) for v in by_day.values() if "control" in v and "treatment" in v]
    sec = {}
    for spec in exp.get("secondary", []):
        c = [val(s, spec) for s in ss if s["arm"] == "control"]
        t = [val(s, spec) for s in ss if s["arm"] == "treatment"]
        sec[spec] = ([x for x in c if x is not None], [x for x in t if x is not None])
    cfg = config().get("experiments", {}) or {}
    res = rule(ctrl, treat, pairs, sec, exp.get("min_n_per_arm", 6), exp.get("max_n_per_arm", 10),
               float(cfg.get("adopt_rel_gain", 0.10)), float(cfg.get("pair_win_share", 2 / 3)),
               float(cfg.get("secondary_max_rel_loss", 0.15)))
    res["samples"] = [{k: d[k] for k in ("slug", "arm", "date", "primary")} for d in data]
    return res


def proposal_patch(exp: dict, day: str) -> str | None:
    target = PROPOSAL_TARGET.get(exp["variable"].split(".")[0])
    if not target or not os.path.exists(os.path.join(ROOT, target)):
        return None
    with open(os.path.join(ROOT, target), encoding="utf-8") as f:
        old = f.read().splitlines(keepends=True)
    new = list(old)
    if not new or not new[-1].endswith("\n"):
        new.append("\n")
    head = "## Learned from experiments (operator)\n"
    if head not in new:
        new += ["\n", head, "\n"]
    new.append(f"- {day} {exp['experiment_id']}: `{exp['variable']}` = `{exp['treatment']}` "
               f"(was `{exp['control']}`). {exp.get('hypothesis', '').rstrip('.')}. Evidence: data/experiments.jsonl "
               f"result row for {exp['experiment_id']}.\n")
    diff = difflib.unified_diff(old, new, fromfile=f"a/{target}", tofile=f"b/{target}")
    path = dpath("proposals", f"{day}-{exp['experiment_id']}.patch")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(diff)
    return os.path.relpath(path, ROOT) if path.startswith(ROOT) else path


def apply_decision(exp: dict, res: dict) -> None:
    now = iso(now_utc())
    day = now[:10]
    jsonl_append(LEDGER(), {"v": 1, "type": "result", "experiment_id": exp["experiment_id"],
                            **{k: res[k] for k in ("n", "medians", "paired_wins", "effect", "decision")},
                            "notes": f"secondary {json.dumps(res.get('secondary_medians'))}"})
    if res["decision"] in ("extend", "pending"):
        return
    if res["decision"] == "adopt":
        rules = load_rules()
        old = rules["defaults"].get(exp["variable"])
        rules["defaults"][exp["variable"]] = exp["treatment"]
        rules["history"].append({"experiment_id": exp["experiment_id"], "key": exp["variable"], "old": old,
                                 "new": exp["treatment"], "at": now})
        note = (f"{exp['variable']}={exp['treatment']} beat {old} on {exp['primary_metric']} "
                f"({res['medians']['treatment']:.3g} vs {res['medians']['control']:.3g}, pairs {res['paired_wins']}) "
                f"[{exp['experiment_id']}]")
        rules["notes"] = (rules.get("notes", []) + [note])[-12:]
        rules["updated_at"] = now
        write_json_atomic(RULES(), rules)
        jsonl_append(LEDGER(), {"v": 1, "type": "promotion", "experiment_id": exp["experiment_id"], "target": "rules",
                                "key": exp["variable"], "value": exp["treatment"], "proposal": None,
                                "status": "overlay_applied"})
        patch = proposal_patch(exp, day)
        if patch:
            jsonl_append(LEDGER(), {"v": 1, "type": "promotion", "experiment_id": exp["experiment_id"],
                                    "target": "playbook" if "PLAYBOOK" in patch else "prompt", "key": exp["variable"],
                                    "value": exp["treatment"], "proposal": patch, "status": "proposed"})
    jsonl_append(LEDGER(), {**exp, "at": now, "status": "decided", "decision": res["decision"], "decided_at": now})


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.analytics.experiments")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("assign")
    s.add_argument("--date", required=True)
    s.add_argument("--slot", required=True, choices=["a", "b"])
    s.add_argument("--slug")
    s.add_argument("--dry-run", action="store_true")
    o = sub.add_parser("open")
    o.add_argument("--dimension", required=True, choices=list(CANDIDATES))
    o.add_argument("--variable")
    o.add_argument("--treatment")
    o.add_argument("--control")
    o.add_argument("--hypothesis", default="")
    o.add_argument("--primary", default="youtube.derived.hold_3s")
    o.add_argument("--min-n", type=int, default=6)
    o.add_argument("--max-n", type=int, default=10)
    o.add_argument("--confirm", action="store_true", help="write the experiment row (operator confirms)")
    d = sub.add_parser("decide")
    d.add_argument("--dry-run", action="store_true")
    sub.add_parser("status")
    a = ap.parse_args(argv)
    if a.cmd == "assign":
        print(json.dumps(assign(a.date, a.slot, a.slug, write=not a.dry_run)))
        return EXIT_OK
    if a.cmd == "open":
        if a.variable:
            if a.treatment is None:
                print("--treatment is required with --variable", file=sys.stderr)
                return EXIT_USAGE
            spec = {"dimension": a.dimension, "variable": a.variable, "treatment": a.treatment,
                    "control": a.control if a.control is not None else baseline(a.variable),
                    "hypothesis": a.hypothesis, "primary_metric": a.primary}
        else:
            spec = propose(a.dimension)
            if not spec:
                print(f"no untested candidate left for {a.dimension}", file=sys.stderr)
                return EXIT_NOTHING
        if not a.confirm:
            print(json.dumps({"proposal": spec, "note": "rerun with --confirm to open it"}, indent=1))
            return EXIT_OK
        try:
            print(json.dumps(open_experiment(spec, a.min_n, a.max_n), indent=1))
        except (RuntimeError, ValueError) as e:
            print(f"error: {e}", file=sys.stderr)
            return EXIT_USAGE
        return EXIT_OK
    if a.cmd == "status":
        for e in experiments().values():
            print(f"{e['experiment_id']} {e['status']:<8} {e['variable']}: {e['control']} vs {e['treatment']}"
                  + (f" -> {e.get('decision')}" if e.get("decision") else ""))
        return EXIT_OK
    exp = running()
    if not exp:
        print("no running experiment")
        return EXIT_NOTHING
    res = evaluate(exp)
    print(json.dumps({"experiment_id": exp["experiment_id"], **{k: v for k, v in res.items() if k != "samples"}}, indent=1))
    if not a.dry_run:
        apply_decision(exp, res)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
