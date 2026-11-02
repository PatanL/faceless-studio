// Shot planner checks (our own code; RICKSCLIPS_RULEBOOK P1-P3, S8, C1/C4 and section 4's place_changes_per_min,
// shot_len_*, first_transition_s, match_transitions). Pure math over a story's groups (no rendering), so it runs in
// the story build, in KitLab, or from a node script (scripts in next/tools).
//   viewChanges(groups)  every change of place (group boundary) or of view (a camera key whose framing differs
//                        enough from the last one: a new angle, a new subject or a big size change)
//   planReport(...)      holds between changes, the holds longer than 4 s (flagged), place changes per minute,
//                        distinct places, inserts, first transition; and for each flagged hold the caption-word
//                        starts where a cutaway / angle change could go (every ~3 s inside it)
import * as THREE from "three";
import type { GroupSpec } from "../kit/Stage";
import type { CamKey } from "../kit/campath";

export type PlanGroup = GroupSpec & { place?: string; insert?: boolean; join?: { kind: string } };
export type Change = { t: number; kind: "place" | "view"; group: string; why: string };
export type Hold = { t0: number; t1: number; len: number; group: string; flag: boolean; splitAt: number[] };

const v = (a: [number, number, number]) => new THREE.Vector3(...a);
/** does key b frame something different from key a? (angle >= 20 deg about the subject, the subject moved >= 35 % of
 * the viewing distance, or the shot size changed >= 1.6x) */
export function differs(a: CamKey, b: CamKey): string | null {
  const la = v(a.look), lb = v(b.look), da = v(a.pos).sub(la), db = v(b.pos).sub(lb);
  const ang = (da.angleTo(db) * 180) / Math.PI;
  if (ang >= 20) return `angle ${ang.toFixed(0)} deg`;
  const dist = Math.max(da.length(), db.length());
  if (la.distanceTo(lb) >= 0.35 * dist) return `subject moved ${(la.distanceTo(lb) / dist * 100).toFixed(0)} %`;
  const size = (da.length() * Math.tan(((a.fov ?? 40) * Math.PI) / 360)) / (db.length() * Math.tan(((b.fov ?? 40) * Math.PI) / 360));
  if (size >= 1.6 || size <= 1 / 1.6) return `size x${size.toFixed(2)}`;
  return null;
}

export function viewChanges(groups: PlanGroup[]): Change[] {
  const out: Change[] = [];
  groups.forEach((g, i) => {
    if (i > 0) out.push({ t: g.t0, kind: "place", group: g.id, why: `${(groups[i - 1].place ?? groups[i - 1].id)} -> ${g.place ?? g.id} (${g.join?.kind ?? (g.xfade > 0 ? "whip" : "cut")})` });
    const ks = [...g.cam].sort((a, b) => a.t - b.t);
    let ref = ks[0];
    for (const k of ks.slice(1)) {
      if (k.t <= g.t0 + 1e-3 || k.t >= g.t1) { ref = k; continue; }
      const why = differs(ref, k);
      // a glide lands ~0.27 s after its key time starts the move; count the change at the key time
      if (why) { out.push({ t: k.t, kind: "view", group: g.id, why }); ref = k; }
    }
  });
  return out.sort((a, b) => a.t - b.t);
}

export type Report = {
  duration: number; changes: Change[]; holds: Hold[]; flagged: Hold[];
  medianHold: number; longestHold: number; placeChangesPerMin: number; viewChangesPerMin: number;
  distinctPlaces: number; inserts: number; firstTransition: number | null; matchJoins: number;
};
/** the plan report. words: caption words (for split suggestions); maxHold: the rule (4 s) */
export function planReport(groups: PlanGroup[], words: { text: string; start: number }[] = [], maxHold = 4): Report {
  const t0 = groups[0].t0, t1 = groups[groups.length - 1].t1, dur = t1 - t0;
  const changes = viewChanges(groups);
  const marks = [t0, ...changes.map((c) => c.t), t1];
  const holds: Hold[] = [];
  for (let i = 0; i + 1 < marks.length; i++) {
    const a = marks[i], b = marks[i + 1];
    if (b - a < 1e-3) continue;
    const g = [...groups].reverse().find((q) => a >= q.t0 - 1e-6) ?? groups[0];
    const flag = b - a > maxHold;
    // suggest word starts every ~3 s inside a long hold (a new angle, insert or place must land on a word)
    const splitAt: number[] = [];
    if (flag) for (let s = a + 3; s < b - 1; s += 3) {
      const w = words.filter((x) => x.start > s - 0.8 && x.start < s + 0.8).sort((x, y) => Math.abs(x.start - s) - Math.abs(y.start - s))[0];
      splitAt.push(+(w ? w.start : s).toFixed(2));
    }
    holds.push({ t0: +a.toFixed(3), t1: +b.toFixed(3), len: +(b - a).toFixed(2), group: g.id, flag, splitAt });
  }
  const lens = holds.map((h) => h.len).sort((x, y) => x - y);
  const places = new Set(groups.map((g) => g.place ?? g.id));
  const placeChanges = changes.filter((c) => c.kind === "place").length;
  return {
    duration: +dur.toFixed(2), changes, holds, flagged: holds.filter((h) => h.flag),
    medianHold: lens[Math.floor(lens.length / 2)], longestHold: lens[lens.length - 1],
    placeChangesPerMin: +((placeChanges / dur) * 60).toFixed(1), viewChangesPerMin: +((changes.length / dur) * 60).toFixed(1),
    distinctPlaces: places.size, inserts: groups.filter((g) => g.insert).length,
    firstTransition: groups.length > 1 ? +groups[1].t0.toFixed(2) : null,
    matchJoins: groups.filter((g) => g.join && g.join.kind !== "whip" && g.join.kind !== "cut").length,
  };
}

/** human-readable report lines */
export function planText(r: Report): string {
  const L = [
    `duration ${r.duration} s; ${r.changes.length} changes (${r.viewChangesPerMin}/min), place changes ${r.placeChangesPerMin}/min, ${r.distinctPlaces} places, ${r.inserts} inserts`,
    `holds: median ${r.medianHold} s, longest ${r.longestHold} s; first transition ${r.firstTransition} s; match/push/frame joins ${r.matchJoins}`,
    ...r.flagged.map((h) => `FLAG hold ${h.t0}-${h.t1} s (${h.len} s) in ${h.group}: put a cutaway or new angle at ${h.splitAt.join(", ")} s`),
  ];
  return L.join("\n");
}
