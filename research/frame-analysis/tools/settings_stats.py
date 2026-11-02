"""Setting-vs-shot statistics from a hand-made settings catalogue plus frame_metrics events.

usage: python3 -I settings_stats.py <settings.csv> <events.json> [--t0 S --t1 S] [--json out.json]

settings.csv columns: start,end,setting,place,kind,motivation
  setting = the backdrop rig as seen (e.g. dark-board, open-blue, sub-porthole)
  place   = where in the world it is ("-" for abstract boards); a new place with the same rig
            counts as a place change but not a backdrop change
  kind    = world | board | analogy | stock | intro
Rows with kind=intro and anything outside [t0, t1] are dropped (runtime = t1 - t0 minus intro).
Each boundary is snapped to the nearest cut/transition within 0.6 s and classified as
cut / transition (with its measured duration) / continuous (no cut or transition nearby:
a camera move, morph, pan or element change carried it).
"""
import csv, json, argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("csv"); ap.add_argument("events")
ap.add_argument("--t0", type=float, default=0.0); ap.add_argument("--t1", type=float, default=0.0)
ap.add_argument("--json", default="")
a = ap.parse_args()
ev = json.load(open(a.events))
t1 = a.t1 or ev["duration"]
rows = [r for r in csv.DictReader(open(a.csv))]
for r in rows: r["start"] = float(r["start"]); r["end"] = float(r["end"])
intro = sum(min(r["end"], t1) - max(r["start"], a.t0) for r in rows if r["kind"] == "intro")
intro_rows = [r for r in rows if r["kind"] == "intro"]
rows = [r for r in rows if r["kind"] != "intro" and r["end"] > a.t0 and r["start"] < t1]
runtime = t1 - a.t0 - intro
mins = runtime / 60

cuts = ev["cuts"]; trans = ev["transitions"]
def boundary_type(t):
    c = [x for x in cuts if abs(x - t) <= 0.6]
    if c: return "cut", 0.0
    tr = [x for x in trans if x["start"] - 0.6 <= t <= x["end"] + 0.6]
    if tr: return "transition", tr[0]["dur"]
    return "continuous", None

def merge(rows, key):
    out = []
    for r in rows:
        if out and out[-1][key] == r[key] and abs(out[-1]["end"] - r["start"]) < 0.05:
            out[-1] = dict(out[-1], end=r["end"])
        else:
            out.append(dict(r))
    return out

def holds(segs):
    d = np.array([s["end"] - s["start"] for s in segs])
    return dict(n=len(d), median=round(float(np.median(d)), 1), p25=round(float(np.percentile(d, 25)), 1),
                p75=round(float(np.percentile(d, 75)), 1), max=round(float(d.max()), 1))

back = merge(rows, "setting")
rows_pk = [dict(r, pk=r["setting"] + "|" + r["place"]) for r in rows]
place = merge(rows_pk, "pk")
world = [s for s in place if s["kind"] in ("world", "stock")]

def shots_in(s):
    evs = [c for c in cuts if s["start"] + 0.3 < c < s["end"] - 0.3] + \
          [x["end"] for x in trans if s["start"] + 0.3 < x["end"] < s["end"] - 0.3]
    return len(evs) + 1

def comps_in(s):
    return sum(1 for c in ev["comp_events"] if s["start"] < c["t"] < s["end"])

# content-only shot statistics (cuts + gradual transitions, intro rows removed)
in_content = lambda t: a.t0 <= t <= t1 and not any(r0["start"] <= t < r0["end"] for r0 in intro_rows)
bnds = sorted([c for c in cuts if in_content(c)] + [x["end"] for x in trans if in_content(x["end"])])
edges = [a.t0] + bnds + [t1]
sl = np.diff(edges); sl = sl[sl > 0.05]
trn = [x for x in trans if in_content(x["end"])]
evts = sorted(bnds + [c["t"] for c in ev["comp_events"] if in_content(c["t"])])
gaps = np.diff([a.t0] + evts)
d_tr = np.array([x["dur"] for x in trn]) if trn else np.array([0.0])
shot_stats = dict(hard_cuts_per_min=round(sum(1 for c in cuts if in_content(c)) / mins, 2),
                  transitions_per_min=round(len(trn) / mins, 2),
                  transition_dur_s=dict(median=round(float(np.median(d_tr)), 2), p25=round(float(np.percentile(d_tr, 25)), 2),
                                        p75=round(float(np.percentile(d_tr, 75)), 2),
                                        share_le_0p35s=round(float((d_tr <= 0.35).mean()), 2)),
                  shot_len_s=dict(median=round(float(np.median(sl)), 2), p25=round(float(np.percentile(sl, 25)), 2),
                                  p75=round(float(np.percentile(sl, 75)), 2), p90=round(float(np.percentile(sl, 90)), 2)),
                  comp_events_per_min=round(sum(1 for c in ev["comp_events"] if in_content(c["t"])) / mins, 2),
                  visual_event_gap_s=dict(median=round(float(np.median(gaps)), 2), p75=round(float(np.percentile(gaps, 75)), 2),
                                          p90=round(float(np.percentile(gaps, 90)), 2)))

btypes = [boundary_type(s["start"]) for s in back[1:]]
ptypes = [boundary_type(s["start"]) for s in place[1:]]
kinds = {}
for r in rows: kinds[r["kind"]] = kinds.get(r["kind"], 0) + r["end"] - r["start"]
shots_per_backdrop = [shots_in(s) for s in back]
res = dict(
    runtime_s=round(runtime, 1),
    distinct_backdrops=len({r["setting"] for r in rows}),
    distinct_places=len({r["place"] for r in rows if r["place"] != "-"}),
    backdrop_changes=len(back) - 1, backdrop_changes_per_min=round((len(back) - 1) / mins, 2),
    place_or_backdrop_changes=len(place) - 1, place_changes_per_min=round((len(place) - 1) / mins, 2),
    backdrop_hold_s=holds(back), place_hold_s=holds(place), world_place_hold_s=holds(world) if world else None,
    shots=shot_stats,
    shots_per_backdrop_hold=dict(median=float(np.median(shots_per_backdrop)), mean=round(float(np.mean(shots_per_backdrop)), 2)),
    boundary_types_backdrop={k: sum(1 for t, _ in btypes if t == k) for k in ("cut", "transition", "continuous")},
    boundary_types_place={k: sum(1 for t, _ in ptypes if t == k) for k in ("cut", "transition", "continuous")},
    runtime_share_by_kind={k: round(v / runtime, 3) for k, v in sorted(kinds.items())},
    distinct_backdrops_by_kind={k: len({r["setting"] for r in rows if r["kind"] == k}) for k in sorted({r["kind"] for r in rows})},
    shot_boundaries_that_change_backdrop=round(sum(1 for b in bnds if any(abs(b - s["start"]) <= 0.6 for s in back[1:])) / max(1, len(bnds)), 2),
    returns_to_backdrop=sum(1 for i, s in enumerate(back) if any(b["setting"] == s["setting"] for b in back[:i])),
    top_backdrops=sorted(((s, round(sum(r["end"] - r["start"] for r in rows if r["setting"] == s) / runtime, 3))
                          for s in {r["setting"] for r in rows}), key=lambda x: -x[1])[:8],
)
print(json.dumps(res, indent=1))
if a.json: json.dump(dict(res, backdrop_segments=back, place_segments=place), open(a.json, "w"), indent=1)
