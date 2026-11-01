"""Weekly LEARNING.md generator (OPERATOR_DESIGN 9.7). Deterministic text from the ledgers; the operator may append
a short "Operator notes" section by hand.

  python -m pipeline.analytics.learning [--week 2026-W46] [--stdout]

Writes data/learning/<week>.md and copies it to data/learning/LEARNING.md. Synthetic / dry-run rows are left out.
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
from datetime import date

from . import experiments as X
from . import killrule
from ._common import (EXIT_OK, TZ, dpath, is_real, jsonl_latest, jsonl_read, median, now_utc, parse, read_json,
                      rpath)

DIM_OF_BEAT = {"HOOK": "hook", "TURN": "structure", "TWIST": "structure", "BOOKEND": "structure", "STINGER": "structure",
               "WHY": "structure", "OPTIONS": "structure", "PEAK": "structure"}


def iso_week(d: date) -> str:
    y, w, _ = d.isocalendar()
    return f"{y}-W{w:02d}"


def _f(v, fmt="{:.0f}"):
    return "-" if v is None else fmt.format(v)


def gather():
    posts = [p for p in jsonl_latest(dpath("posts.jsonl"), "post_key").values() if is_real(p)]
    metrics: dict[tuple, dict] = {}
    for r in jsonl_read(dpath("metrics.jsonl")):
        if is_real(r):
            metrics[(r["post_key"], r["window"])] = r
    al_own: dict[str, dict] = {}
    al_src: dict[str, dict] = {}
    for r in jsonl_read(dpath("alignments.jsonl")):
        if r.get("synthetic"):
            continue
        if r.get("kind") == "own":
            k = r["post_key"]
            if k not in al_own or r.get("window") == "7d" or al_own[k].get("window") != "7d":
                al_own[k] = r
        elif r.get("kind") == "source":
            al_src[r["video_id"]] = r
    return posts, metrics, al_own, al_src


def scoreboard(posts, metrics, week: str) -> list[str]:
    by_slug: dict[str, dict] = {}
    for p in posts:
        by_slug.setdefault(p["slug"], {})[p["platform"]] = p
    def pub(s):
        return min((p.get("published_at") or p.get("scheduled_at") or "9") for p in by_slug[s].values())
    slugs = sorted(by_slug, key=pub)[-30:]
    out = ["| Video | Published (local) | Source | Arm | YT 48h | YT 7d | TT 48h | TT 7d | IG 48h | IG 7d | hold 3s | avg view % |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for s in slugs:
        ps = by_slug[s]
        any_p = next(iter(ps.values()))
        pa = pub(s)
        local = parse(pa).astimezone(TZ).date() if pa[0].isdigit() else None
        mark = " **(this week)**" if local and iso_week(local) == week else ""
        v = lambda plat, w: (metrics.get((f"{s}:{plat}", w)) or {}).get("views")
        yt = metrics.get((f"{s}:youtube", "7d")) or metrics.get((f"{s}:youtube", "48h")) or {}
        arm = f"{any_p.get('experiment_id')}:{any_p.get('arm')}" if any_p.get("experiment_id") else "-"
        out.append(f"| {s}{mark} | {local or '-'} | {any_p.get('source_id') or '-'} | {arm} | {_f(v('youtube', '48h'))} | "
                   f"{_f(v('youtube', '7d'))} | {_f(v('tiktok', '48h'))} | {_f(v('tiktok', '7d'))} | "
                   f"{_f(v('instagram', '48h'))} | {_f(v('instagram', '7d'))} | "
                   f"{_f((yt.get('derived') or {}).get('hold_3s'), '{:.2f}')} | {_f(yt.get('avg_view_pct'), '{:.1f}')} |")
    if len(out) == 2:
        out.append("| (no published videos with real metrics yet) | | | | | | | | | | | |")
    return out


def beat_tables(al_own) -> tuple[list[str], list[tuple[str, float]]]:
    by_beat: dict[str, list[float]] = {}
    by_comp: dict[str, list[float]] = {}
    for a in al_own.values():
        for s in a["scenes"]:
            z = s.get("z")
            dps = s.get("drop_ranked_per_s")
            if z is None or dps is None:
                continue
            by_beat.setdefault(s.get("beat") or "?", []).append((z, dps))
            for c in s.get("components", []):
                by_comp.setdefault(c, []).append((z, dps))
    out = ["| Beat | Scenes | Median z (drop/s vs own video) | Median drop/s |", "|---|---|---|---|"]
    ranked = sorted(((b, median([z for z, _ in v]), median([d for _, d in v]), len(v)) for b, v in by_beat.items()),
                    key=lambda t: -(t[1] or 0))
    for b, mz, md, n in ranked:
        out.append(f"| {b} | {n} | {mz:+.2f} | {md:.4f} |")
    if not ranked:
        out.append("| (no retention alignments yet) | | | |")
    out += ["", "| Component | Scenes | Median z | Median drop/s |", "|---|---|---|---|"]
    comps = sorted(((c, median([z for z, _ in v]), median([d for _, d in v]), len(v)) for c, v in by_comp.items() if len(v) >= 2),
                   key=lambda t: -(t[1] or 0))
    for c, mz, md, n in comps[:15]:
        out.append(f"| {c} | {n} | {mz:+.2f} | {md:.4f} |")
    if not comps:
        out.append("| (fewer than 2 scenes per component so far) | | | |")
    return out, [(b, mz) for b, mz, _, _ in ranked]


def source_vs_ours(posts, al_own, al_src) -> list[str]:
    src_of = {p["post_key"]: p.get("source_id") for p in posts}
    out = ["| Video | Source | Source's most replayed beat | Our scenes on it | Their z | Kept? |", "|---|---|---|---|---|---|"]
    for k, a in sorted(al_own.items()):
        sid = src_of.get(k) or (read_json(rpath("episodes", a.get("slug") or "", "source.json")) or {}).get("source_id")
        sa = al_src.get(sid) if sid else None
        if not sa:
            out.append(f"| {a.get('slug')} | {sid or '-'} | (no source heatmap) | | | |")
            continue
        best = max(sa["scenes"], key=lambda s: s.get("heat_mean") or 0)
        bi = (best.get("source_beat_i") or [None])[0]
        ours = [s for s in a["scenes"] if bi is not None and bi in (s.get("source_beat_i") or [])]
        zs = [s["z"] for s in ours if s.get("z") is not None]
        kept = "-" if not zs else ("yes" if median(zs) <= 0 else "no (worse than our average)")
        out.append(f"| {a.get('slug')} | {sid} | {best['beat']} ({best['t0']:.0f}-{best['t1']:.0f} s, heat "
                   f"{best.get('heat_mean', 0):.2f}) | {', '.join(s['scene_id'] for s in ours) or '(not mapped)'} | "
                   f"{', '.join(f'{z:+.2f}' for z in zs) or '-'} | {kept} |")
    if len(out) == 2:
        out.append("| (no own alignments yet) | | | | | |")
    return out


def experiment_status() -> list[str]:
    out = []
    run = X.running()
    if run:
        res = X.evaluate(run)
        out.append(f"- **Running {run['experiment_id']}** ({run['dimension']}): `{run['variable']}` "
                   f"`{run['control']}` (control) vs `{run['treatment']}` (treatment). Primary `{run['primary_metric']}`.")
        out.append(f"  - n = {res['n']['control']} / {res['n']['treatment']} (min {run['min_n_per_arm']}, max "
                   f"{run['max_n_per_arm']}); medians {res['medians']}; pairs {res.get('paired_wins')}; "
                   f"rule says **{res['decision']}**.")
    else:
        out.append("- No experiment running.")
    for r in X.rows():
        if r.get("type") == "result" and r.get("decision") not in ("pending", "extend"):
            out.append(f"- {r['experiment_id']} decided **{r['decision']}** at {r['at'][:10]}: medians {r['medians']}, "
                       f"pairs {r.get('paired_wins')}.")
    rules = X.load_rules()
    out.append(f"- Rules overlay (`data/learned/rules.json`): {', '.join(f'{k}={v}' for k, v in sorted(rules['defaults'].items()))}.")
    for n in rules.get("notes", [])[-5:]:
        out.append(f"  - {n}")
    return out


def killrule_status() -> list[str]:
    kr = read_json(dpath("killrule.json"))
    if not kr:
        rows = killrule.series()
        kr = killrule.evaluate([float(r["views"]) for r in rows])
    return [f"- Verdict **{kr['verdict']}**: {kr['explanation']}.",
            f"- n = {kr['n_videos']}, median 7-day views {_f(kr['median_views_7d'])} (target {kr['target_views_7d']:.0f}), "
            f"first-10 {_f(kr['first10_median'])}, last-10 {_f(kr['last10_median'])}, Theil-Sen slope "
            f"{_f(kr['theil_sen_slope_per_video'], '{:+.1f}')}/video."]


def candidates(beat_rank: list[tuple[str, float]]) -> list[str]:
    dims = []
    for b, _ in beat_rank:
        d = DIM_OF_BEAT.get(b.upper(), "visual")
        if d not in dims:
            dims.append(d)
    for d in ("hook", "structure", "visual"):
        if d not in dims:
            dims.append(d)
    loss = dict(beat_rank)
    out = []
    for d in dims:
        p = X.propose(d)
        if not p:
            continue
        why = next((f"largest loss at beat {b} (median z {z:+.2f})" for b, z in beat_rank if DIM_OF_BEAT.get(b.upper(), "visual") == d), "no beat data yet")
        out.append(f"{len(out) + 1}. `{p['variable']}`: `{p['control']}` -> `{p['treatment']}` ({d}; {why}). "
                   f"{p['hypothesis']}. Primary `{p['primary_metric']}`. Open with "
                   f"`python -m pipeline.analytics.experiments open --dimension {d} --confirm`.")
        if len(out) == 3:
            break
    return out or ["(every candidate in the backlog has been tested; add new ones to experiments.CANDIDATES)"]


def build(week: str) -> str:
    posts, metrics, al_own, al_src = gather()
    beat_lines, beat_rank = beat_tables(al_own)
    L = [f"# LEARNING {week}", "",
         f"Generated {now_utc().strftime('%Y-%m-%d %H:%M')} UTC by `python -m pipeline.analytics.learning`. "
         f"{len({p['slug'] for p in posts})} videos with posts, {len(metrics)} real metrics rows, "
         f"{len(al_own)} own and {len(al_src)} source alignments. Synthetic and dry-run rows are excluded.", "",
         "## 1. Scoreboard", ""] + scoreboard(posts, metrics, week) + [
         "", "## 2. Where viewers leave (beat level)", "",
         "z > 0 means that beat loses viewers faster than the rest of its own video (first 2 % and last 3 % excluded).", ""
         ] + beat_lines + ["", "## 3. Source vs ours", ""] + source_vs_ours(posts, al_own, al_src) + [
         "", "## 4. Experiments", ""] + experiment_status() + ["", "## 5. Kill rule", ""] + killrule_status() + [
         "", "## 6. Candidate next experiments (ranked by beat-level loss)", ""] + candidates(beat_rank) + [
         "", "## 7. Operator notes", "", "(operator: 3-5 lines at most)", ""]
    return "\n".join(L)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.analytics.learning")
    ap.add_argument("--week", default=None)
    ap.add_argument("--stdout", action="store_true")
    a = ap.parse_args(argv)
    week = a.week or iso_week(now_utc().astimezone(TZ).date())
    text = build(week)
    if a.stdout:
        print(text)
        return EXIT_OK
    d = dpath("learning")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, f"{week}.md")
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)
    shutil.copyfile(p, os.path.join(d, "LEARNING.md"))
    print(f"wrote {p} and LEARNING.md")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
