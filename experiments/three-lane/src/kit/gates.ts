// Build gates for 3D story episodes (our own code). Episode3D runs them when it builds the story and fails the
// render on a failure (an episode can ask for warnings instead); scripts/framing.ts runs them and exits 1.
//   hold   no view held longer than 4 s without a change of place, angle, subject or size (planner.ts; rule book P1-P3)
//   cast   no group whose figures are specks (median head < 0.05 of the frame height) unless it is marked
//          establishing or insert, and heads >= 0.07 in at least 25 % of the frames with figures (refs: median head
//          0.08, 47 % >= 0.07; castframe.ts)
//   edge   no figure's head cut and no body cut by the left or right edge (bottom crops are allowed), and nothing in
//          a group's keepInFrame cut by any edge, for 8+ frames outside a join
//   still  nothing on screen visibly changes for more than 2 s: the camera moves < 2.5 px/frame (screen motion of a grid
//          of points at the subject's distance) and no figure changes pose, face, item or place; a group's
//          `alive` windows (rigs animating: fire, smoke, a dropping weight) count as change (coordinator round 2:
//          "the hold gate passes shots the judges call static"). scripts/visible_change.py checks the render itself.
//   hud    a progress readout never goes backwards and a gauge never reverses direction (by more than its tolerance)
//          outside the windows the story allows (Vasa panel round 4: the heel gauge swinging 6, 2, 10 degrees)
import * as THREE from "three";
import type { GroupSpec, V3 } from "./Stage";
import { planReport } from "./planner";
import { castCheck, peopleCast } from "./castframe";
import { camAt, project, W, H } from "./match";
import { personBox, type Box } from "./framing";

export type HudTrack = { name: string; kind: "progress" | "gauge"; value: (t: number) => number | null; tol?: number; allowBack?: [number, number][] };
export type GateOpts = { fps?: number; maxStill?: number; minCamPx?: number; maxHold?: number; minHead?: number; minShare07?: number; edgeMinF?: number; hud?: HudTrack[]; joins?: "ricks" };
export type GateResult = { failures: string[]; notes: string[] };

/** frames inside a join (whip smear, dissolve, push): nothing is judged there */
const inJoin = (groups: GroupSpec[], t: number) => groups.some((g, i) => i > 0 && Math.abs(t - g.t0) < Math.max(g.xfade / 2, 0.3, (g.join as { frames?: number } | undefined)?.frames ? ((g.join as { frames: number }).frames / 60) : 0));

/** the join mix (story-myeongnyang, owner 2026-11-02: match the RicksClips counts, RICKSCLIPS_RULEBOOK C3-C7, T2-T4).
 * Every join is classified: travel (the camera continues through one world: same world name on both sides and the
 * camera pose continuous across the seam, else it counts as a cut), dissolve (5-8 f; "match" dissolves counted too),
 * whip, push / into / outOf / match (push-throughs), cut. */
export function joinMix(groups: GroupSpec[], fps = 30) {
  const counts: Record<string, number> = { travel: 0, dissolve: 0, matchDissolve: 0, whip: 0, push: 0, cut: 0 };
  const bad: string[] = [];
  groups.forEach((g, i) => {
    if (i === 0) return;
    const j = (g.join ?? (g.xfade > 0 ? { kind: "whip" } : { kind: "cut" })) as { kind: string; frames?: number; match?: boolean; world?: string };
    if (j.kind === "travel") {
      const p = groups[i - 1], a = camAt(p, g.t0 - 1e-4, new THREE.PerspectiveCamera()), b = camAt(g, g.t0, new THREE.PerspectiveCamera());
      const dp = a.position.distanceTo(b.position), dq = a.quaternion.angleTo(b.quaternion) * 180 / Math.PI;
      const pj = p.join as { world?: string } | undefined;
      const sameWorld = (p as GroupSpec & { world?: string }).world === j.world || pj?.world === j.world || (g as GroupSpec & { world?: string }).world === j.world;
      if (dp < 0.05 * Math.max(1, a.position.length() * 0.01) + 0.05 && dq < 0.5 && sameWorld) counts.travel++;
      else { counts.cut++; bad.push(`join into ${g.id} at ${g.t0.toFixed(2)} s is declared travel but the camera jumps ${dp.toFixed(2)} m / ${dq.toFixed(1)} deg`); }
    } else if (j.kind === "dissolve") {
      counts[j.match ? "matchDissolve" : "dissolve"]++;
      if ((j.frames ?? 6) > 8 || (j.frames ?? 6) < 3) bad.push(`dissolve into ${g.id} is ${j.frames} f (3-8)`);
    } else if (j.kind === "whip") counts.whip++;
    else if (j.kind === "cut") counts.cut++;
    else counts.push++;
  });
  return { counts, bad };
}

function boxOnScreen(cam: THREE.PerspectiveCamera, b: Box) {
  let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity, behind = false;
  for (const x of [b[0], b[3]]) for (const y of [b[1], b[4]]) for (const z of [b[2], b[5]]) {
    const q = project(cam, [x, y, z]);
    if (q.behind) { behind = true; continue; }
    x0 = Math.min(x0, q.x); x1 = Math.max(x1, q.x); y0 = Math.min(y0, q.y); y1 = Math.max(y1, q.y);
  }
  const area = Math.max(1, (x1 - x0) * (y1 - y0));
  const ix = Math.max(0, Math.min(W, x1) - Math.max(0, x0)), iy = Math.max(0, Math.min(H, y1) - Math.max(0, y0));
  return { inside: behind ? -1 : (ix * iy) / area, hFrac: (y1 - y0) / H, sides: x0 < 0 || x1 > W, x0, x1 };
}

export function runGates(groups: GroupSpec[], words: { text: string; start: number }[], o: GateOpts = {}): GateResult {
  const fps = o.fps ?? 30, failures: string[] = [], notes: string[] = [];
  // hold
  const plan = planReport(groups, words, o.maxHold ?? 4);
  for (const h of plan.flagged) failures.push(`hold: ${h.t0}-${h.t1} s (${h.len} s) in ${h.group}; change the view at ${h.splitAt.join(", ")} s`);
  notes.push(`plan: ${plan.placeChangesPerMin} place changes/min, ${plan.distinctPlaces} places, longest hold ${plan.longestHold} s`);
  // joins (opt-in): cuts <= 1, whips <= 8, dissolves 4-20 (match dissolves included), at least one match dissolve,
  // each dissolve <= 8 f, the first transition no earlier than 0.7 s
  if (o.joins === "ricks") {
    const { counts, bad } = joinMix(groups, fps);
    const diss = counts.dissolve + counts.matchDissolve;
    if (counts.cut > 1) failures.push(`joins: ${counts.cut} hard cuts (refs 0-1)`);
    if (counts.whip > 8) failures.push(`joins: ${counts.whip} whips (refs median 5, at most 8)`);
    if (diss < 4 || diss > 20) failures.push(`joins: ${diss} dissolves (refs 4-20, about 12)`);
    if (counts.matchDissolve < 1) failures.push(`joins: no match dissolve (refs: an object keeps its spot)`);
    if (groups.length > 1 && groups[1].t0 < 0.7) failures.push(`joins: first transition at ${groups[1].t0.toFixed(2)} s (refs >= 0.7 s)`);
    failures.push(...bad.map((b) => `joins: ${b}`));
    notes.push(`joins: ${Object.entries(counts).map(([k, v]) => `${k} ${v}`).join(", ")}`);
  }
  // cast
  const cast = castCheck(groups, peopleCast, fps, o.minHead ?? 0.05);
  for (const r of cast.rows) {
    const g = groups.find((q) => q.id === r.group);
    if (r.small && !g?.establishing && !g?.insert) failures.push(`cast: ${r.group} figures are specks (median head ${r.median} of the frame height, target >= ${o.minHead ?? 0.05}); use castKey "medium"/"close" or mark it establishing`);
  }
  if (cast.rows.length && cast.shareGe007 < (o.minShare07 ?? 0.25)) failures.push(`cast: heads >= 0.07 in only ${Math.round(100 * cast.shareGe007)} % of the frames with figures (target >= ${Math.round(100 * (o.minShare07 ?? 0.25))} %)`);
  notes.push(`cast: median head ${cast.median}, ${Math.round(100 * cast.shareGe007)} % >= 0.07`);
  // edge
  const runs = new Map<string, number[]>();
  for (const g of groups) for (let f = Math.round(g.t0 * fps); f < Math.round(g.t1 * fps); f++) {
    const t = f / fps;
    if (inJoin(groups, t)) continue;
    const cam = camAt(g, t);
    const cut = (k: string) => { if (!runs.has(k)) runs.set(k, []); runs.get(k)!.push(f); };
    // figures: the head must be whole and the body must not cross the left or right edge; a body cropped by the
    // bottom edge is a framing choice (the refs' figures fill the lower half), not a cut
    for (const p of g.people) {
      if (p.visible && !p.visible(t)) continue;
      const b = personBox(p.at(t), (p.props(t) as { seated?: boolean }).seated === true), s = p.scale ?? 1;
      const body: Box = s === 1 ? b : [b[0], b[1], b[2], b[0] + (b[3] - b[0]) * s, b[1] + (b[4] - b[1]) * s, b[5]];
      const head: Box = [body[0], body[4] - 0.3 * (body[4] - body[1]), body[2], body[3], body[4], body[5]];
      const rh = boxOnScreen(cam, head), rb = boxOnScreen(cam, body);
      // a figure looming in front of the lens (closer than 1 m) blocks the shot
      const pc = new THREE.Vector3((body[0] + body[3]) / 2, (body[1] + body[4]) / 2, (body[2] + body[5]) / 2);
      if (rb.inside > 0 && pc.distanceTo(cam.position) < 1.0 && !(g.people.length === 1)) cut(`${g.id}:${p.id}:lens`);
      if (rb.hFrac > 1.2 || rh.hFrac > 0.3 || rb.inside <= 0.02) continue;   // a face close-up (head > 30 % of the frame), or out of the shot
      if ((rh.inside > 0.02 && rh.inside < 0.95) || (rb.sides && rb.inside < 0.95)) cut(`${g.id}:${p.id}`);
    }
    // keepInFrame boxes: any edge
    (g.keepInFrame ? g.keepInFrame(t) : []).forEach((b, i) => { const r = boxOnScreen(cam, b); if (r.inside > 0.02 && r.inside < 0.95 && r.hFrac < 1.2) cut(`${g.id}:keep${i}`); });
  }
  for (const [k, fs] of runs) {
    let s = fs[0], prev = fs[0];
    for (const f of [...fs.slice(1), -1]) {
      if (f !== prev + 1) { if (prev - s + 1 >= (o.edgeMinF ?? 8)) failures.push(`edge: ${k} cut by the frame edge ${(s / fps).toFixed(2)}-${(prev / fps).toFixed(2)} s`); s = f; }
      prev = f;
    }
  }
  // still: per frame, does anything visibly change?
  {
    const maxStill = Math.round((o.maxStill ?? 2) * fps), minPx = o.minCamPx ?? 2.5;
    const cam2 = new THREE.PerspectiveCamera();
    for (const g of groups) {
      let run = 0, runStart = 0;
      const alive = (g as GroupSpec & { alive?: [number, number][] }).alive ?? [];
      const f0 = Math.round(g.t0 * fps), f1 = Math.round(g.t1 * fps);
      let prevProps: string[] | null = null;
      for (let f = f0; f < f1; f++) {
        const t = f / fps;
        const a = camAt(g, t), look = new THREE.Vector3(); a.getWorldDirection(look);
        // the grid sits at the subject's depth (median distance to the visible figures, else 4 m): a 4 m grid overstated
        // a slow drift on a distant subject (Barca r2: the section at 45.6-48.7 s passed the gate, then read as still)
        const vis = g.people.filter((q) => !q.visible || q.visible(t)).map((q) => { const [x, y, z] = q.at(t); return a.position.distanceTo(new THREE.Vector3(x, y + 0.8, z)); }).sort((u, v) => u - v);
        const d = vis.length ? Math.max(2, vis[Math.floor(vis.length / 2)]) : 4, centre = a.position.clone().addScaledVector(look, d);
        const right = new THREE.Vector3().setFromMatrixColumn(a.matrixWorld, 0), up = new THREE.Vector3().setFromMatrixColumn(a.matrixWorld, 1);
        const pts: V3[] = [];
        for (const i of [-1, 0, 1]) for (const j of [-1, 0, 1]) { const p = centre.clone().addScaledVector(right, i * 0.3 * d).addScaledVector(up, j * 0.5 * d); pts.push([p.x, p.y, p.z]); }
        const p0 = pts.map((p) => project(a, p));
        cam2.copy(camAt(g, t + 1 / fps));
        const p1 = pts.map((p) => project(cam2, p));
        const camPx = p0.reduce((n, q, i) => n + Math.hypot(q.x - p1[i].x, q.y - p1[i].y), 0) / pts.length;
        // a figure's change counts only if the figure is big enough on screen for it to show (>= 0.2 of the frame
        // height): small miners swinging picks read as still in the render (Barca r2, visible_change.py)
        const shown = g.people.filter((q) => !q.visible || q.visible(t));
        const props = shown.map((q) => JSON.stringify([q.at(t).map((x) => Math.round((x ?? 0) * 100)), q.props(t)]));
        const tall = shown.map((q) => { const [x, y, z] = q.at(t), lo = project(a, [x, y, z]), hi = project(a, [x, y + 1.9 * (q.scale ?? 1), z]); return Math.abs(lo.y - hi.y) / H; });
        const figure = prevProps !== null && (props.length !== prevProps.length || props.some((x, i) => x !== prevProps![i] && tall[i] >= 0.2));
        prevProps = props;
        const changing = camPx >= minPx || figure || alive.some(([x, y]) => t >= x && t <= y) || inJoin(groups, t);
        if (changing) { if (run > maxStill) failures.push(`still: ${g.id} shows nothing changing ${(runStart / fps).toFixed(2)}-${((runStart + run) / fps).toFixed(2)} s (${(run / fps).toFixed(1)} s; camera < ${minPx} px/f, figures still); move the camera, act, or mark rig motion in alive`); run = 0; }
        else { if (run === 0) runStart = f; run++; }
      }
      if (run > maxStill) failures.push(`still: ${g.id} shows nothing changing ${(runStart / fps).toFixed(2)}-${((runStart + run) / fps).toFixed(2)} s (${(run / fps).toFixed(1)} s)`);
    }
  }
  // hud
  for (const h of o.hud ?? []) {
    const tol = h.tol ?? (h.kind === "progress" ? 1e-6 : 2);
    const allowed = (t: number) => (h.allowBack ?? []).some(([a, b]) => t >= a && t <= b);
    let last: number | null = null, dir = 0, ext: number | null = null;
    const turns: number[] = [];
    for (let f = 0; f < Math.round(groups[groups.length - 1].t1 * fps); f++) {
      const t = f / fps, v = h.value(t);
      if (v === null) { last = null; dir = 0; ext = null; continue; }
      if (h.kind === "progress") {
        if (last !== null && v < last - tol && !allowed(t)) turns.push(t);
        last = v; continue;
      }
      // gauge, with hysteresis: a turn back by more than tol from the furthest reading so far is a reversal
      if (ext === null) { ext = v; dir = 0; continue; }
      if (dir === 0) { if (Math.abs(v - ext) > tol) { dir = Math.sign(v - ext); ext = v; } continue; }
      if ((v - ext) * dir > 0) ext = v;
      else if (Math.abs(v - ext) > tol) { if (!allowed(t)) turns.push(t); dir = -dir; ext = v; }
    }
    if (turns.length) failures.push(`hud: ${h.name} ${h.kind === "progress" ? "goes backwards" : "reverses"} ${turns.length}x (first at ${turns.slice(0, 4).map((x) => x.toFixed(2)).join(", ")} s)`);
  }
  return { failures, notes };
}
