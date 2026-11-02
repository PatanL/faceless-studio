// story-vasa v1 (our own code): who is where, what moves and where the camera goes, for every beat, word-anchored on
// the Kokoro timings. Places: the Vasa's deck at the shipyard quay (the running test), the harbour, the king's camp in
// Poland, the quay with the guns going aboard, the launch and the two gusts, the flooding gun deck, the sinking seen
// from the shore, the inquiry, a night explanation room (weighted toys, the hull cross-section), the sea bed in 1961
// and the museum hall. Every angle is a solved framing (kit/framing fit).
import * as THREE from "three";
import type { GroupSpec, PersonSpec, Rig, V3 } from "../kit/Stage";
import { Timing } from "../kit/timing";
import { hallSet, glowSprite, lambert } from "../kit/sets";
import { Rising } from "../kit/fx";
import { NOINK } from "../ink";
import { clamp01, sm, ramp, track, step, poses, personBox, fit, setRoom, tagSprite, type Box } from "../kit/framing";
import { Ship, ShipState, deckY, halfW, uOf, HALF_B, DRAFT, deckTop } from "./ship";
import { harbourSet, campSet, gundeckSet, explainSet, seabedSet, museumHallSet } from "./sets";

export type Tag = { text: string; at: number; out: number };
export type VasaStory = { groups: GroupSpec[]; tags: Tag[]; heel: (t: number) => number | null; dist: (t: number) => number | null };

// ------------------------------------------------------------------------------------------------ ship helpers
/** world position of a ship-space point for a ship state (same transform as Ship.update) */
export function shipPt(s: ShipState, p: V3): V3 {
  const h = -(s.heel ?? 0), yaw = s.yaw ?? 0, pi = s.pitch ?? 0;
  let [x, y, z] = p;
  // pitch about z, then heel about x (Euler XYZ order applies x first in the matrix: R = Rx * Ry * Rz)
  [x, y] = [x * Math.cos(pi) - y * Math.sin(pi), x * Math.sin(pi) + y * Math.cos(pi)];
  [y, z] = [y * Math.cos(h) - z * Math.sin(h), y * Math.sin(h) + z * Math.cos(h)];
  [x, z] = [x * Math.cos(yaw) + z * Math.sin(yaw), -x * Math.sin(yaw) + z * Math.cos(yaw)];
  return [x + (s.x ?? 0), y - (s.sink ?? 0), z + (s.z ?? 0)];
}
const sternBox = (s: ShipState): Box => {
  const c = shipPt(s, [0, 0, 0]);
  return [c[0] - 26, c[1] - 2, c[2] - HALF_B - 1, c[0] + 2, c[1] + 10, c[2] + HALF_B + 1];
};
const hullBox = (s: ShipState, withMasts = false): Box => {
  const c = shipPt(s, [0, 0, 0]);
  return [c[0] - 26, Math.max(c[1], -2) - 2, c[2] - HALF_B - 1, c[0] + 29, c[1] + (withMasts ? 50 : 10), c[2] + HALF_B + 1];
};
function shipRig(state: (t: number) => ShipState, hold: { ship?: Ship }, opts: { carvings?: boolean } = {}): Rig {
  return (ctx) => {
    const ship = new Ship(opts); hold.ship = ship; ctx.root.add(ship.group);
    return (t) => ship.update(state(t));
  };
}
const waterRig = (speed = 0.01): Rig => (ctx) => {
  const w = ctx.set.extra.water as THREE.Mesh | undefined;
  const map = w ? ((w.material as THREE.MeshLambertMaterial).map as THREE.Texture) : null;
  return (t) => { if (map) { map.offset.set(t * speed, t * speed * 0.4); } };
};
/** sailors running across the deck (z from starboard to port and back); returns their mean z (-1..1) */
const RUNS = (t0: number, dur: number, n: number) => (t: number) => {
  const k = (t - t0) / dur;
  if (k <= 0) return -1;
  if (k >= n) return n % 2 ? 1 : -1;
  const i = Math.floor(k), f = sm(k - i);
  return i % 2 === 0 ? -1 + 2 * f : 1 - 2 * f;
};
/** the ship answers the crowd with a lag, each run rocking her harder */
const heelFromRuns = (runs: (t: number) => number, t0: number, dur: number, gain: number, tPeak?: number) => (t: number) => {
  const lagged = runs(t - 0.35);
  const n = clamp01((t - t0) / ((tPeak ?? t0 + dur * 3) - t0));
  return lagged * (0.03 + gain * n);
};

// ------------------------------------------------------------------------------------------------ props
/** a floating bottle with sand in it (our comparison for ballast): the pivot is the waterline; sand: where the sand
 * sits ("bottom" floats upright, "top" = built upside down, rolls over) */
function bottle(sand: "bottom" | "top") {
  const g = new THREE.Group();
  const prof = [[0, -0.42], [0.16, -0.42], [0.18, -0.38], [0.18, 0.1], [0.07, 0.24], [0.06, 0.4], [0, 0.4]].map(([r, y]) => new THREE.Vector2(r, y));
  const glass = new THREE.Mesh(new THREE.LatheGeometry(prof, 24), new THREE.MeshLambertMaterial({ color: "#b8e6d8", transparent: true, opacity: 0.45, depthWrite: false }));
  g.add(glass);
  const cork = new THREE.Mesh(new THREE.CylinderGeometry(0.055, 0.05, 0.08, 12), lambert({ color: "#9a6b3c" })); cork.position.y = 0.42; g.add(cork);
  const sandM = lambert({ color: "#e2bf6e" });
  const sandG = new THREE.Mesh(new THREE.CylinderGeometry(0.165, 0.165, 0.2, 20), sandM);
  sandG.position.y = sand === "bottom" ? -0.31 : 0.0; if (sand === "top") sandG.scale.set(1, 1, 1); g.add(sandG);
  const outer = new THREE.Group(); outer.add(g);
  return { outer, g };
}

/** the hull cross-section (amidships) at scale k, with two gun decks of guns, the stone ballast and a water tank */
function sectionModel(k: number) {
  const root = new THREE.Group();          // pivot at the waterline centre
  const body = new THREE.Group(); root.add(body);
  const u = 0.5, top = deckTop(u);
  const sh = new THREE.Shape();
  const N = 24;
  for (let i = 0; i <= N; i++) { const y = -DRAFT + (i / N) * (top + DRAFT); const w = halfW(u, y); if (i === 0) sh.moveTo(-w * k, y * k); else sh.lineTo(-w * k, y * k); }
  for (let i = N; i >= 0; i--) { const y = -DRAFT + (i / N) * (top + DRAFT); sh.lineTo(halfW(u, y) * k, y * k); }
  const inner = new THREE.Path();
  for (let i = 0; i <= N; i++) { const y = -DRAFT + 0.4 + (i / N) * (top - 0.3 + DRAFT - 0.4); const w = Math.max(0.05, halfW(u, y) - 0.4); if (i === 0) inner.moveTo(-w * k, y * k); else inner.lineTo(-w * k, y * k); }
  for (let i = N; i >= 0; i--) { const y = -DRAFT + 0.4 + (i / N) * (top - 0.3 + DRAFT - 0.4); inner.lineTo(Math.max(0.05, halfW(u, y) - 0.4) * k, y * k); }
  sh.holes.push(inner);
  // the planked wall as thick segments along the outline (no shape triangulation), and a dark back panel
  const wallMat = lambert({ color: "#c98a4e" });
  for (const side of [-1, 1]) for (let i = 0; i < N; i++) {
    const y0 = -DRAFT + (i / N) * (top + DRAFT), y1 = -DRAFT + ((i + 1) / N) * (top + DRAFT);
    const a = new THREE.Vector2(side * halfW(u, y0) * k, y0 * k), b2 = new THREE.Vector2(side * halfW(u, y1) * k, y1 * k);
    const len = a.distanceTo(b2), mid = a.clone().add(b2).multiplyScalar(0.5);
    const seg = new THREE.Mesh(new THREE.BoxGeometry(0.45 * k, len + 0.02, 0.55), wallMat);
    seg.position.set(mid.x, mid.y, 0); seg.rotation.z = Math.atan2(b2.y - a.y, b2.x - a.x) - Math.PI / 2; seg.castShadow = true; body.add(seg);
  }
  const keel = new THREE.Mesh(new THREE.BoxGeometry(0.7 * k, 0.5 * k, 0.6), wallMat); keel.position.set(0, -DRAFT * k, 0); body.add(keel);
  void inner;
  // the dry inside: a filled outline (counter-clockwise, no hole) behind the walls, in front of the water backdrop
  const fill = new THREE.Shape();
  for (let i = 0; i <= N; i++) { const y = -DRAFT + (i / N) * (top + DRAFT); const x = halfW(u, y) * k; if (i === 0) fill.moveTo(x, y * k); else fill.lineTo(x, y * k); }
  for (let i = N; i >= 0; i--) { const y = -DRAFT + (i / N) * (top + DRAFT); fill.lineTo(-halfW(u, y) * k, y * k); }
  const back = new THREE.Mesh(new THREE.ShapeGeometry(fill, 4), new THREE.MeshLambertMaterial({ color: "#5a3a26", side: THREE.DoubleSide })); back.position.z = -0.28; body.add(back);
  // decks
  const plank = lambert({ color: "#8a5a32" });
  for (const y of [1.0, 3.3, top - 0.3]) { const w = halfW(u, y) - 0.4; const d = new THREE.Mesh(new THREE.BoxGeometry(w * 2 * k, 0.12 * k, 0.5), plank); d.position.set(0, y * k, 0); body.add(d); }
  // guns: two each side on each gun deck
  const bronze = lambert({ color: "#c08a3a" }), red = lambert({ color: "#b8352a" });
  const guns: THREE.Object3D[] = [];
  for (const y of [1.45, 3.75]) for (const side of [-1, 1]) {
    const gg = new THREE.Group();
    const car = new THREE.Mesh(new THREE.BoxGeometry(1.4 * k, 0.4 * k, 0.4), red); car.position.y = -0.2 * k; gg.add(car);
    const gun = new THREE.Mesh(new THREE.CylinderGeometry(0.22 * k, 0.3 * k, 2.6 * k, 12), bronze); gun.rotation.z = Math.PI / 2; gun.position.y = 0.1 * k; gg.add(gun);
    gg.position.set(side * (halfW(u, y) - 1.4) * k, (y - 0.15) * k, 0); body.add(gg); guns.push(gg);
  }
  // ports (lower row glows red when it reaches the water)
  const portMat = new THREE.MeshBasicMaterial({ color: "#1a1424", fog: false });
  const lowPorts: THREE.Mesh[] = [];
  for (const y of [1.45, 3.75]) for (const side of [-1, 1]) {
    const p = new THREE.Mesh(new THREE.BoxGeometry(0.75 * k, 0.8 * k, 0.1), portMat.clone()); p.position.set(side * (halfW(u, y) - 0.05) * k, y * k, 0.3); body.add(p);
    if (y < 2) lowPorts.push(p);
  }
  // stones: the ballast, and a second (ghost) load
  const stone = lambert({ color: "#c4c4cc" });
  const stones: THREE.Mesh[] = [], more: THREE.Mesh[] = [];
  const r = (i: number) => ((Math.sin(i * 91.7) * 43758.5) % 1 + 1) % 1;
  for (let i = 0; i < 36; i++) {
    const rows = i < 18 ? 0 : 1;
    const x = (-1.6 + (i % 18) * 0.19 + r(i) * 0.1) * k * 2, y = (-DRAFT + 0.55 + rows * 0.42 + r(i + 5) * 0.12) * k;
    const s = new THREE.Mesh(new THREE.DodecahedronGeometry(0.42 * k * (0.8 + r(i + 9) * 0.5)), stone); s.position.set(x * 0.85, y, (r(i + 3) - 0.5) * 0.2);
    if (Math.abs(s.position.x) < (halfW(u, -DRAFT + 0.6 + rows * 0.4) - 0.5) * k) { body.add(s); (rows ? more : stones).push(s); }
  }
  // the centre of gravity marker (a quartered disc)
  const cg = new THREE.Group();
  const q = (a: number, col: string) => { const m = new THREE.Mesh(new THREE.CircleGeometry(0.16, 16, a, Math.PI / 2), new THREE.MeshBasicMaterial({ color: col, fog: false })); m.layers.set(NOINK); cg.add(m); };
  q(0, "#f4eee1"); q(Math.PI / 2, "#1b1240"); q(Math.PI, "#f4eee1"); q(Math.PI * 1.5, "#1b1240");
  cg.position.z = 0.3; body.add(cg);
  return { root, body, guns, stones, more, lowPorts, cg, k, top };
}

// ------------------------------------------------------------------------------------------------ the story
export function buildStory(T: Timing): VasaStory {
  const w = T.w.bind(T), S = T.S.bind(T);
  const groups: GroupSpec[] = [];
  // out on the harbour the camera stays above the water plane (v1: a dive under it showed the void beneath)
  const OPEN: Box = [-1e5, 1.0, -1e5, 1e5, 1e5, 1e5];
  setRoom(OPEN);

  // ---- the running test (hook and scene 4): the ship moored at the quay, eight runners for the thirty
  const runners: { id: string; costume: string; x: number; dz: number }[] =
    [-6.8, -5.6, -4.4, -3.2, -2.0, -0.6, 3.4, 4.6, 5.8, 7.0, 8.2, 9.4, 10.6, 11.8].map((x, i) => ({ id: `s${i + 1}`, costume: i % 2 ? "sailor2" : "sailor", x, dz: ((i * 37) % 7) / 7 - 0.5 }));
  const deckGroup = (id: string, t0: number, t1: number, xfade: number, runT0: number, runDur: number, nRuns: number, gain: number,
    stopAt: number, tPeak: number | undefined, cams: (st: (t: number) => ShipState, at: (r: typeof runners[0], t: number) => V3, oth: (t: number) => Box[]) => GroupSpec["cam"], admiral: Partial<PersonSpec> = {}): GroupSpec => {
    const runs = RUNS(runT0, runDur, nRuns);
    const heel = heelFromRuns(runs, runT0, runDur, gain, tPeak);
    const st = (t: number): ShipState => ({ heel: heel(t), lids: 0, sails: 0 });
    const at = (r: typeof runners[0], t: number): V3 => {
      const zz = runs(t) * (halfW(uOf(r.x), deckY(r.x)) - 1.3) + r.dz;
      return shipPt(st(t), [r.x, deckY(r.x), zz]);
    };
    const hold: { ship?: Ship } = {};
    const ADM: V3 = [-9.6, 0, 1.4], CAPT: V3 = [-11.4, 0, -2.4];
    const oth = (t: number): Box[] => [...runners.map((r) => personBox(at(r, t))), personBox(shipPt(st(t), [ADM[0], deckY(ADM[0]), ADM[2]])), personBox(shipPt(st(t), [CAPT[0], deckY(CAPT[0]), CAPT[2]]))];
    return {
      id, t0, t1, xfade, set: () => harbourSet({ sheds: id !== "warning" }), light: "day",
      cam: cams(st, at, oth),
      people: [
        ...runners.map((r): PersonSpec => ({ id: r.id, flip: false, at: (t) => at(r, t),
          props: (t) => { const k = (t - runT0) / runDur; const moving = k > 0 && k < nRuns && t < stopAt; const dir = Math.floor(Math.max(0, k)) % 2 === 0;
            return { costume: r.costume, seed: r.x * 3, pose: moving ? "sweep" : "stand", walk: moving ? 1 : 0, face: moving ? "focus" : "worried", look: dir ? 1 : -1 }; } })),
        { id: "admiral", flip: false, at: (t) => shipPt(st(t), [ADM[0], deckY(ADM[0]), ADM[2]]),
          props: (t) => ({ costume: "admiral", seed: 5, pose: t >= stopAt - 0.1 ? "armsUp" : "hips", face: t >= stopAt - 0.3 ? "shock" : "frown" }), ...admiral },
        { id: "captain", flip: false, at: (t) => shipPt(st(t), [CAPT[0], deckY(CAPT[0]), CAPT[2]]),
          props: (t) => ({ costume: "captain", seed: 8, pose: "point", face: t >= stopAt ? "worried" : "smug" }) },
      ],
      rigs: [shipRig(st, hold), waterRig()],
      avoid: () => [],
    };
  };
  // runner flip so they face the way they run: done in props via look; the card faces right (toward +z on screen
  // depends on camera) - acceptable for a crowd running both ways.

  // Beats (scene index = narration paragraph): 0 the test and "sent her to sea anyway", 1 the admiral, 2 the king at war,
  // 3 two decks of guns, 4 nobody tells the king / his letters, 5 launch day, 6 the first gust, 7 the second gust,
  // 8 the sea pours in / she sinks, 9 the hearing / the king, 10 the bottle, 11 built upside down / too little stone,
  // 12 more stone, 13 the test was the warning (the last line; the video ends on it).
  const ADM = (st: ShipState) => shipPt(st, [-9.6, deckY(-9.6), 1.4]);

  // ================= G1 the test: thirty sailors run across her until she nearly rolls over
  const navy = w(0, "navy") - 0.25;
  const over = w(0, "over");
  const HOOK_T0 = over - 4.3;                                     // the crossings land so the biggest roll falls on "rolled over"
  {
    groups.push(deckGroup("test", 0, navy, 0, HOOK_T0, 1.0, 5, 0.3, navy + 1, over + 0.1, (st, at, oth) => {
      const run = (t: number) => runners.slice(3, 8).map((r) => personBox(at(r, t)));
      return [
        fit(0, runners.map((r) => personBox(at(r, 0))), 25, 36, 40, { b: 0.38, x: 0.08 }, oth(0)),     // all the runners, already rolling
        fit(over, run(over), -15, 26, 42, { b: 0.35 }, oth(over)),                                // she nearly rolls over
      ];
    }));
  }
  // ================= G2 ... and the navy sent her to sea anyway
  const sailing = (t: number, tStart: number): ShipState => ({ x: 70 + Math.max(0, t - tStart) * 6, z: 30, sails: 1, lids: 1, guns: 0.6, heel: 0.04 });
  {
    const t0 = navy, t1 = S(1);
    const st = (t: number) => sailing(t, t0 - 2);
    groups.push({ id: "anyway", t0, t1, xfade: 0.4, set: () => harbourSet(), light: "golden",
      cam: [fit(t0, [hullBox(st(t0), true)], 70, 4, 40, { b: 0.25 }), fit(t1, [hullBox(st(t1), true)], 55, 3, 42, { b: 0.25 })],
      people: [], rigs: [shipRig(st, {}), waterRig()], avoid: (t) => [hullBox(st(t), true)] });
  }
  // ================= G3 the admiral stops the test and mutters
  {
    const t0 = S(1), t1 = S(2), mut = w(1, "mutters");
    groups.push(deckGroup("admiral", t0, t1, 0.4, t0 - 3.0, 1.0, 3, 0.2, t0 + 0.2, undefined, (st, at, oth) => [
      fit(t0, [personBox(ADM(st(t0)), false, true)], -20, 22, 40, { b: 0.55, t: 0.28 }, oth(t0)),
      fit(mut, [personBox(ADM(st(mut)), false, true)], -12, 18, 34, { b: 0.55, t: 0.28 }, oth(mut)),            // "If only the king were here."
    ], { props: (t: number) => ({ costume: "admiral", seed: 5, pose: t < mut - 0.2 ? "armsUp" : "handIn", face: t < mut - 0.2 ? "shock" : "worried", talk: [[mut + 0.4, t1 - 0.1]] }) }));
  }
  // ================= G4 the king is off at war and wants the mightiest warship afloat
  const KING: V3 = [-0.4, 0, -1.3];
  const kingPeople = (letter: boolean): PersonSpec[] => [
    { id: "king", at: () => KING, props: (t) => ({ costume: "king", seated: true, seed: 3, pose: letter ? "point" : "hold", item: "letter", face: letter ? "angry" : step(t, [[0, "focus"], [w(2, "wants"), "grin"]]) }) },
    { id: "aide", flip: true, at: () => [1.5, 0, -2.2], props: () => ({ costume: "sailor2", seed: 9, pose: letter ? "reach" : "stand", face: "worried" }) },
    { id: "sold1", at: () => [-5.8, 0, -8.5], props: () => ({ costume: "sailor", seed: 2, pose: "point", face: "focus" }) },
    { id: "sold2", flip: true, at: () => [4.2, 0, -9.5], props: () => ({ costume: "sailor2", seed: 6, pose: "hold", face: "frown" }) }];
  {
    const t0 = S(2), t1 = S(3) - 0.35;
    groups.push({ id: "camp", t0, t1, xfade: 0.4, set: campSet, light: "day",
      cam: [fit(t0, [personBox(KING, true), [-0.2, 0, -1.9, 1.4, 1.0, -0.9], personBox([-5.8, 0, -8.5]), personBox([4.2, 0, -9.5]), [-8, 0, -14, 8, 5, -10]], 14, 8, 42, { b: 0.4 }, [personBox([1.5, 0, -2.2])]),
        fit(w(2, "mightiest"), [personBox(KING, true, true), [0.0, 0.8, -1.7, 1.3, 1.5, -1.1]], 34, 14, 34, { b: 0.55, t: 0.3 }, [personBox([1.5, 0, -2.2]), personBox([-5.8, 0, -8.5]), personBox([4.2, 0, -9.5])])],   // the king and his model warship
      people: kingPeople(false), rigs: [(ctx) => {
        // the war on the horizon: smoke from the guns; and the model of the warship he wants, on his table
        const smoke = [-9, 7, 12].map((x, i) => { const r = new Rising(10, "smoke", 2.6, 20 + i); r.group.position.set(x, 1, -14 + i * 2); ctx.root.add(r.group); return r; });
        const model = new THREE.Group(); model.position.set(0.75, 0.82, -1.4); model.rotation.y = 0.5; ctx.root.add(model);
        const hullM = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.14, 0.2), lambert({ color: "#7a4a26" })); hullM.position.y = 0.07; model.add(hullM);
        const stern = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.12, 0.2), lambert({ color: "#d9a43a" })); stern.position.set(-0.3, 0.2, 0); model.add(stern);
        for (const [x, h] of [[-0.18, 0.5], [0.05, 0.62], [0.24, 0.48]] as [number, number][]) {
          const m = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 0.012, h, 6), lambert({ color: "#4a2e1c" })); m.position.set(x, 0.14 + h / 2, 0); model.add(m);
          const sl = new THREE.Mesh(new THREE.PlaneGeometry(0.2, h * 0.5), lambert({ color: "#efe4c8", side: THREE.DoubleSide })); sl.position.set(x + 0.01, 0.14 + h * 0.55, 0); sl.rotation.y = Math.PI / 2; model.add(sl);
        }
        for (let k = 0; k < 6; k++) for (const row of [0.06, 0.11]) { const port = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.025, 0.21), lambert({ color: "#b8352a" })); port.position.set(-0.22 + k * 0.09, row, 0); model.add(port); }
        return (t) => { smoke.forEach((r) => r.update(t, 0.8, 9, 4, 4)); };
      }], avoid: () => [[-0.8, 0, -2, 1.6, 1.4, -0.8]] });
  }
  // ================= G5 two decks of heavy bronze cannons, stacked high above the water
  {
    const t0 = S(3) - 0.35, t1 = S(4);
    const two = w(3, "two"), stacked = w(3, "stacked");
    const st = (t: number): ShipState => ({ lids: ramp(t, two - 0.6, two, 0, 1), guns: ramp(t, two - 0.4, two + 0.3, 0, 1), sails: 0 });
    const WR: V3 = [10.5, 1.8, -11.4];
    groups.push({ id: "guns", t0, t1, xfade: 0.4, set: () => harbourSet(), light: "day",
      cam: [
        fit(t0, [[-14, 0.6, 3, 10, 9, 7]], 30, 8, 40, { b: 0.5 }),                                // from the water: the gun decks open
        fit(two, [[-14, 0.6, 3, 10, 4.6, 7]], 18, 4, 40, { b: 0.35 }),                            // two rows of ports open, guns run out
        fit(stacked, [[-10, -0.6, 4, 8, 4.8, 7]], 24, 1.5, 38, { b: 0.35 }),                      // at the waterline: stacked high
      ],
      people: [{ id: "wright", flip: true, at: () => WR, props: () => ({ costume: "shipwright", seed: 4, pose: "point", face: "smug" }) },
        { id: "wright2", at: () => [5.5, 1.8, -12.5], props: () => ({ costume: "sailor2", seed: 6, pose: "push", face: "focus" }) }],
      rigs: [shipRig(st, {}), waterRig(), (ctx) => {
        const hang = ctx.set.extra.hanging as THREE.Object3D, line = ctx.set.extra.line as THREE.Mesh;
        return (t) => {
          const u = clamp01((t - (t0 - 0.3)) / 1.8);
          const p = new THREE.Vector3(8, 15 - 10 * sm(u), -6 + 2.5 * sm(u));
          hang.position.copy(p); hang.visible = false;
          const a = new THREE.Vector3(8, 17.1, -0.5), b = p.clone().add(new THREE.Vector3(0, 0.3, 0));
          line.position.copy(a).lerp(b, 0.5); line.scale.set(1, a.distanceTo(b), 1); line.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), b.clone().sub(a).normalize()); line.visible = false;
        };
      }],
      avoid: () => [] });
  }
  // ================= G6 nobody wants to tell the king his masterpiece wobbles
  const letters = w(4, "his", 2) - 0.1;
  {
    const t0 = S(4), t1 = letters;
    const st = (t: number): ShipState => ({ sails: 0, lids: 0, guns: 0, heel: 0.15 * Math.sin((t - t0) * 2.6) });
    const Q: V3[] = [[27.6, 1.8, -9.9], [28.9, 1.8, -11.0], [28.2, 1.8, -12.1]];
    groups.push({ id: "wobble", t0, t1, xfade: 0.4, set: () => harbourSet({ cannonsOnQuay: false, sheds: false }), light: "day",
      // crew in front, the rocking hull behind them; wide x pad so the hold's push-in and orbit never crop the crew
      cam: [{ ...fit(t0, Q.map((q) => personBox(q)), 112, 10, 40, { b: 0.45, x: 0.3, t: 0.4 }), drift: 0.3 }, 
        // on "wobbles": low and wide, the crew small in front of the bow and the foremast swinging against the sky
        { ...fit(w(4, "masterpiece") - 0.1, [...Q.map((q) => personBox(q)), [8, 2, -4, 16, 34, 4]], 118, 2, 44, { b: 0.42, x: 0.12 }), glide: 1.1, drift: 0.3 }],
      people: Q.map((q, i): PersonSpec => ({ id: `q${i}`, at: () => q, faceTo: () => Q[i === 2 ? 1 : i + 1], props: (t) => ({ costume: ["shipwright", "captain", "citizen2"][i], seed: i * 4, pose: i === 1 ? "shrug" : "hips",
        face: step(t, [[0, "worried"], [w(4, "wobbles") - 0.1, i === 0 ? "frown" : "worried"]]), look: i === 0 ? 1 : -1 }) })),
      rigs: [shipRig(st, {}), waterRig()], avoid: () => Q.map((q) => personBox(q)) });
  }
  // ================= G7 his letters keep arriving: a courier hands the admiral the king's letter on the quay
  {
    const t0 = letters, t1 = S(5);
    const AD: V3 = [-1.0, 1.8, -10.9], CR: V3 = [0.05, 1.8, -11.0];
    groups.push({ id: "letters", t0, t1, xfade: 0.4, set: () => harbourSet({ cannonsOnQuay: false }), light: "day",
      cam: [fit(t0, [personBox(AD), personBox(CR)], -160, 8, 40, { b: 0.45 }), fit(t1, [personBox(AD, false, true), personBox(CR, false, true)], -170, 4, 34, { b: 0.5 })],
      people: [{ id: "adm", at: () => AD, faceTo: () => CR, props: (t) => ({ costume: "admiral", seed: 5, pose: t > w(4, "get") + 0.3 ? "hold" : t > w(4, "get") - 0.6 ? "reach" : "stand", item: t > w(4, "get") - 0.2 ? "letter" : "none", face: "worried" }) },
        { id: "courier", at: (t) => [CR[0] + 2.2 * (1 - sm((t - t0) / 0.9)), CR[1], CR[2]], faceTo: () => AD, props: (t) => ({ costume: "sailor2", seed: 9, pose: t < t0 + 0.7 ? "stand" : "reach", item: t < w(4, "get") - 0.2 ? "letter" : "none", walk: [{ t: 0, v: 1 }, { t: t0 + 0.6, v: 1 }, { t: t0 + 0.95, v: 0 }], face: "focus" }) }],
      rigs: [shipRig(() => ({ sails: 0, lids: 0 }), {}), waterRig()], avoid: () => [personBox(AD), personBox(CR)] });
  }

  // ================= G8 launch day: the crowd, the sails, the two gusts
  const tSail = w(5, "sails") - 0.5;
  const gust1 = w(6, "gust"), shakes = w(6, "shakes"), gust2 = w(7, "gust"), dip = w(7, "dip");
  const voyageHeel = (t: number) => track(t, [[gust1 - 0.15, 0], [gust1 + 0.5, 0.36], [shakes - 0.1, 0.3], [shakes + 0.55, 0.04], [gust2 - 0.05, 0.04], [gust2 + 0.6, 0.38], [dip + 0.3, 0.5], [S(8) + 1.0, 0.62]]);
  const voyage = (t: number): ShipState => { const d = Math.max(0, t - tSail); return { x: 30 + d * 8, z: d * 3.2, sails: ramp(t, tSail, tSail + 0.9, 0, 1), lids: 1, guns: 0.7, heel: voyageHeel(t) }; };
  const CC = ["citizen", "citizen2", "sailor", "citizen", "citizen2", "shipwright", "sailor2", "citizen", "citizen2", "citizen", "sailor", "citizen2"];
  const crowd = [...CC, ...CC].map((c, i) => ({ id: `c${i + 1}`, costume: c, x: -8.5 + (i % 8) * 1.3 + (Math.floor(i / 8) % 2) * 0.65, z: -10.5 - Math.floor(i / 8) * 1.1 }));
  const crowdPeople = (wave: (t: number) => boolean, shock: number, ship: (t: number) => V3 = () => [60, 0, 10]): PersonSpec[] => crowd.map((c, i) => ({ id: c.id, at: () => [c.x, 1.8, c.z], faceTo: ship,
    props: (t) => ({ costume: c.costume, seed: i * 3 + 1, pose: t >= shock ? (i % 2 ? "armsUp" : "shrug") : wave(t) ? (i % 2 ? "armsUp" : "point") : (i % 3 === 0 ? "point" : "stand"),
      face: t >= shock ? "shock" : (i % 2 ? "smile" : "grin") }) }));
  const crowdBox = (): Box => [-8.9, 1.8, -13.0, 1.5, 3.5, -10.2];
  {
    const t0 = S(5), t1 = S(8);
    const waving = w(6, "waving");
    groups.push({ id: "launch", t0, t1, xfade: 0.4, set: () => harbourSet({ cannonsOnQuay: false }), light: "golden",
      cam: [
        fit(t0, [crowdBox()], 15, 8, 42, { b: 0.45 }),                                            // a huge crowd on the quay
        fit(w(5, "watches"), [crowdBox()], 22, 10, 40, { b: 0.45 }),
        fit(w(5, "sails") + 0.3, [[voyage(w(5, "sails")).x! - 14, 12, -6, voyage(w(5, "sails")).x! + 16, 50, 6]], 40, -8, 44, { b: 0.45 }),   // her sails go up
        fit(gust1 + 0.2, [hullBox(voyage(gust1 + 0.2), true)], -118, 8, 42, { b: 0.42, t: 0.38 }),        // the first gust leans her over (seen from the quay)
        fit(waving, [crowdBox(), hullBox(voyage(waving), true)], -150, 8, 40, { b: 0.4 }),       // she shakes it off over the waving crowd
        fit(gust2 + 0.2, [[voyage(gust2 + 0.2).x! - 22, -1, voyage(gust2 + 0.2).z! - 7, voyage(gust2 + 0.2).x! + 20, 8, voyage(gust2 + 0.2).z! - 3]], -125, 4, 38, { b: 0.42, t: 0.42 }),   // low on the port quarter
        fit(dip, [[voyage(dip).x! - 12, -1, voyage(dip).z! - 7, voyage(dip).x! + 10, 6, voyage(dip).z! - 3]], -130, 3, 34, { b: 0.42, t: 0.42 }),   // the port gun ports dip under
      ],
      people: crowdPeople((t) => t >= waving - 0.6, S(8) + 9, (t) => { const v = voyage(t); return [v.x!, 0, v.z!]; }),
      rigs: [shipRig(voyage, {}), waterRig()],
      avoid: (t) => [hullBox(voyage(t), true)] });
  }
  // ================= G9 the sea pours in (the lower gun deck)
  const front = w(8, "in", 2) - 0.1;
  {
    const t0 = S(8), t1 = front;
    groups.push({ id: "gundeck", t0, t1, xfade: 0.4, set: gundeckSet, light: "day",
      cam: [{ t: t0, pos: [-1.2, 1.25, 9], look: [1.2, 0.7, -6], fov: 50 }, { t: t1, pos: [-1.4, 1.35, 6.5], look: [1.6, 0.6, -8], fov: 50 }],
      people: [{ id: "gunner", at: (t) => [-1.2 + Math.max(0, t - t0) * 0.5, 0, -2.5], props: () => ({ costume: "sailor2", seed: 2, pose: "armsUp", walk: 1, face: "shock" }) }],
      rigs: [(ctx) => {
        const room = ctx.set.extra.room as THREE.Group, flood = ctx.set.extra.flood as THREE.Mesh;
        const pours: THREE.Mesh[] = [];
        for (let k = 0; k < 11; k++) {
          const m = new THREE.Mesh(new THREE.PlaneGeometry(1.8, 0.7), new THREE.MeshBasicMaterial({ color: "#bfeaf4", transparent: true, opacity: 0.9, fog: false, side: THREE.DoubleSide }));
          m.geometry.translate(-0.9, 0, 0); m.position.set(4.75, 0.95, -16 + k * 3.2); m.rotation.z = -0.5; m.layers.set(NOINK); room.add(m); pours.push(m);
        }
        const spray = new Rising(30, "puff", 0.12, 4); spray.group.position.set(4.2, 0.6, 0); room.add(spray.group);
        return (t) => {
          room.rotation.z = -(0.34 + 0.06 * sm((t - t0) / 1.4));
          flood.position.y = ramp(t, t0 - 0.2, t1 + 0.4, -1.2, 0.2);
          pours.forEach((m, i) => { m.scale.set(0.9 + 0.12 * Math.sin(t * 5 + i), 1, 1); });
          spray.update(t, 1, 1.0, 0.8, 16);
        };
      }],
      avoid: () => [] });
  }
  // ================= G10 in front of the whole city, the Vasa sinks inside her own harbour
  {
    const t0 = front, t1 = S(9);
    const sinks = w(8, "sinks"), stop = voyage(t0 - 0.2);
    // she lies over, then goes down ON "sinks" (v4: the hull was gone before the word)
    const st = (t: number): ShipState => ({ ...stop, heel: track(t, [[t0, 0.62], [sinks - 0.3, 0.95], [t1, 1.15]]), sink: track(t, [[t0, 1.0], [sinks - 0.35, 2.0], [sinks + 0.7, 13], [t1 + 0.6, 20]]), sails: 1 });
    const sx = stop.x!, sz = stop.z!;
    groups.push({ id: "sinking", t0, t1, xfade: 0.4, set: () => harbourSet({ cannonsOnQuay: false }), light: "golden",
      cam: [
        fit(t0, [hullBox(st(t0), true)], -165, 6, 38, { b: 0.35 }),                              // from the quay side, the town beyond: she is going over
        fit(sinks, [hullBox(st(sinks), true)], -158, 4, 34, { b: 0.42 }),                        // closer: she sinks, in frame
      ],
      people: crowdPeople(() => false, t0, () => [sx, 0, sz]),
      rigs: [shipRig(st, {}), waterRig(), (ctx) => {
        const bub = new Rising(40, "puff", 1.2, 6); ctx.root.add(bub.group);
        const debris: THREE.Mesh[] = [];
        for (let i = 0; i < 14; i++) { const d = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.3, 0.5), lambert({ color: "#6b4a2b" })); ctx.root.add(d); debris.push(d); }
        return (t) => {
          bub.group.position.set(sx, 0, sz); bub.update(t, ramp(t, sinks - 0.3, sinks + 0.4, 0, 1), 3, 1.2, 14);
          debris.forEach((d, i) => { const a = i * 2.4; d.position.set(sx + Math.cos(a) * (4 + i * 0.6), 0.15 + 0.05 * Math.sin(t * 3 + i), sz + Math.sin(a) * (4 + i * 0.5)); d.rotation.y = a + t * 0.2; d.visible = t > sinks; });
        };
      }],
      avoid: (t) => [hullBox(st(t), true)] });
  }
  // ================= G11 the hearing: "Only God knows." Nobody is punished. The man who ordered the cannons was the king.
  {
    const t0 = S(9), t1 = S(10);
    setRoom([-5.6, 0.2, -19.6, 5.6, 6, 7.6]);
    const J1: V3 = [-1.2, 0, -10.4], J2: V3 = [0, 0, -10.6], J3: V3 = [1.2, 0, -10.4], B: V3 = [0.6, 0, -5.8], A: V3 = [-0.9, 0, -6.4];
    const PORT: V3 = [0, 2.7, -11.9];                              // the king's portrait hung high behind the bench, over the judges' heads
    const judges = [J1, J2, J3];
    const only = w(9, "only"), nobody = w(9, "nobody"), man = w(9, "man");
    const hearing: GroupSpec = { id: "hearing", t0, t1, xfade: 0.4, set: () => hallSet(false, { throne: false }), light: "day",
      cam: [
        { ...fit(t0, [...judges.map((j) => personBox(j, true)), personBox(B), personBox(A), [PORT[0] - 1.1, PORT[1] - 0.4, PORT[2] - 0.1, PORT[0] + 1.1, PORT[1] + 2.6, PORT[2] + 0.1]], 6, 8, 46, { b: 0.55, x: 0.3 }), drift: 0.3 },
        fit(only, [personBox(B, false, true)], 22, 4, 36, { b: 0.55 }, [personBox(A), ...judges.map((j) => personBox(j, true))]),
        fit(nobody, [...judges.map((j) => personBox(j, true)), personBox(B)], 0, 8, 42, { b: 0.45 }, [personBox(A), [PORT[0] - 1.1, PORT[1] - 0.4, PORT[2] - 0.1, PORT[0] + 1.1, PORT[1] + 2.6, PORT[2] + 0.1]]),
        fit(man, [[PORT[0] - 1.3, PORT[1] - 0.5, PORT[2] - 0.1, PORT[0] + 1.3, PORT[1] + 2.9, PORT[2] + 0.4]], 0, 6, 30, { b: 0.5, t: 0.14 },   // the king, and the cannons he ordered
          [...judges.map((j) => personBox(j, true)), personBox(B), personBox(A)]),
      ],
      people: [
        ...judges.map((j, i): PersonSpec => ({ id: `j${i}`, at: () => j, faceTo: () => B, props: (t) => ({ costume: "judge", seated: true, seed: 11 + i, pose: t >= nobody - 0.1 ? "shrug" : (i === 1 ? "point" : "hold"), face: t >= nobody - 0.1 ? "neutral" : "frown" }) })),
        { id: "builder", at: () => B, faceTo: () => J2, props: (t) => ({ costume: "shipwright", seed: 4, pose: t >= only - 0.2 ? "shrug" : "stand", face: t >= only - 0.2 ? "worried" : "neutral", talk: [[only, only + 0.9]] }) },
        { id: "accused", at: () => A, faceTo: () => J2, props: () => ({ costume: "captain", seed: 8, pose: "stand", face: "worried" }) },
        { id: "portrait", billboard: false, scale: 1.25, at: () => [PORT[0], PORT[1] + 0.12, PORT[2] + 0.06], props: (t) => ({ costume: "king", seed: 3, pose: t >= man + 0.6 ? "point" : "hips", face: "smug" }) },
      ],
      rigs: [(ctx) => {
        const tab = new THREE.Mesh(new THREE.BoxGeometry(4.6, 0.8, 1.0), lambert({ color: "#4a2e1c" })); tab.position.set(0, 0.4, -9.6); tab.castShadow = true; ctx.root.add(tab);
        const frame = new THREE.Mesh(new THREE.BoxGeometry(2.2, 2.6, 0.08), lambert({ color: "#d9a43a" })); frame.position.set(PORT[0], PORT[1] + 1.2, PORT[2] - 0.02); ctx.root.add(frame);
        const canvasM = new THREE.Mesh(new THREE.PlaneGeometry(1.9, 2.3), lambert({ color: "#3a2f5a" })); canvasM.position.set(PORT[0], PORT[1] + 1.2, PORT[2] + 0.03); ctx.root.add(canvasM);
        const shelf = new THREE.Mesh(new THREE.BoxGeometry(2.6, 0.08, 0.5), lambert({ color: "#5b3a22" })); shelf.position.set(PORT[0], PORT[1] - 0.25, PORT[2] + 0.2); ctx.root.add(shelf);
        // the cannons he ordered, lined up under his portrait
        const bronzeM = lambert({ color: "#b07a34" });
        for (let k = 0; k < 3; k++) {
          const prof = [[0, 0], [0.18, 0.04], [0.17, 0.3], [0.14, 1.4], [0.17, 1.48], [0.12, 1.6], [0, 1.6]].map(([r, y]) => new THREE.Vector2(r, y));
          const c = new THREE.Mesh(new THREE.LatheGeometry(prof, 14), bronzeM); c.scale.setScalar(0.32); c.rotation.x = Math.PI / 2; c.position.set(PORT[0] - 0.8 + k * 0.8, PORT[1] - 0.1, PORT[2] + 0.1); c.castShadow = true; ctx.root.add(c);
          const car = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.08, 0.36), lambert({ color: "#b8352a" })); car.position.set(PORT[0] - 0.8 + k * 0.8, PORT[1] - 0.17, PORT[2] + 0.25); ctx.root.add(car);
        }
        return () => undefined;
      }],
      avoid: () => [personBox(B), ...judges.map((j) => personBox(j, true))] };
    // the king's portrait is its own shot (a whip in from the bench), so its caption can sit under it
    const pt0 = man - 0.25;
    groups.push({ ...hearing, t1: pt0, cam: hearing.cam.slice(0, 3) });
    groups.push({ ...hearing, id: "portrait", t0: pt0, people: hearing.people.filter((p) => p.id === "portrait"), cam: hearing.cam.slice(3).map((k) => ({ ...k, t: Math.max(k.t, pt0) })), avoid: () => [[PORT[0] - 1.3, PORT[1], PORT[2] - 0.1, PORT[0] + 1.3, PORT[1] + 2.4, PORT[2] + 0.4]] });
    setRoom(OPEN);
  }

  // ================= G12 the explanation (night blue): the bottle with sand, the hull built upside down, more stone
  const SEC_K = 0.4, SEC: V3 = [2.0, 0, -6.2];
  const bottleW = w(10, "bottle"), heavyW = w(10, "heavy"), lightW = w(10, "light"), upside = w(11, "upside"), bronze = w(11, "bronze"), stoneW = w(11, "stone");
  const tooLittle = w(11, "and") - 0.1;
  const more = w(12, "more"), pushed = w(12, "pushed"), waterline = w(12, "waterline"), lastT = S(13);
  const secW = halfW(0.5, 0) * SEC_K;
  const tankTop = (DRAFT + 1.6) * SEC_K;
  const secBox: Box = [SEC[0] - secW - 0.7, 0, SEC[2] - 0.5, SEC[0] + secW + 1.2, tankTop + (deckTop(0.5) + 0.5) * SEC_K, SEC[2] + 0.5];
  const BT: V3 = [-2.7, 0, -6.1];                                  // the small bottle tank
  const bottleBox: Box = [BT[0] - 1.0, 0, BT[2] - 0.4, BT[0] + 1.0, 1.5, BT[2] + 0.4];
  const explainRig: Rig = (ctx) => {
    // the bottle tank (left): two bottles floating; the one with sand in the bottom stands up, the upside-down one rolls over
    const bTank = new THREE.Mesh(new THREE.PlaneGeometry(2.0, 0.9), new THREE.MeshBasicMaterial({ color: "#3f8fb0", fog: false })); bTank.position.set(BT[0], 0.45, BT[2] - 0.3); bTank.layers.set(NOINK); ctx.root.add(bTank);
    const bGlass = new THREE.Mesh(new THREE.PlaneGeometry(2.0, 0.9), new THREE.MeshBasicMaterial({ color: "#8fd8ec", transparent: true, opacity: 0.16, depthWrite: false, fog: false })); bGlass.position.set(BT[0], 0.45, BT[2] + 0.3); bGlass.layers.set(NOINK); ctx.root.add(bGlass);
    const bWl = new THREE.Mesh(new THREE.BoxGeometry(2.0, 0.03, 0.02), new THREE.MeshBasicMaterial({ color: "#e8fbff", fog: false })); bWl.position.set(BT[0], 0.9, BT[2] + 0.31); bWl.layers.set(NOINK); ctx.root.add(bWl);
    const bEdge = new THREE.Mesh(new THREE.BoxGeometry(2.1, 0.06, 0.65), lambert({ color: "#5b3a22" })); bEdge.position.set(BT[0], 0.03, BT[2]); ctx.root.add(bEdge);
    const good = bottle("bottom"), bad = bottle("top");
    good.outer.position.set(BT[0] - 0.45, 0.9, BT[2]); bad.outer.position.set(BT[0] + 0.45, 0.9, BT[2]); ctx.root.add(good.outer, bad.outer);
    const sec = sectionModel(SEC_K); ctx.root.add(sec.root);
    const lamp = new THREE.Group(); lamp.position.set(SEC[0] - 1.6, 4.0, SEC[2] - 1.4); ctx.root.add(lamp);
    const chain = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, 2.0, 4), lambert({ color: "#2a2a30" })); chain.position.y = 1.0; lamp.add(chain);
    lamp.add(new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.2, 0.36, 6), lambert({ color: "#c08a3a" })));
    const flame = new THREE.Mesh(new THREE.SphereGeometry(0.08, 10, 8), new THREE.MeshBasicMaterial({ color: "#ffd27a", fog: false })); flame.layers.set(NOINK); lamp.add(flame);
    glowSprite(ctx.root, [255, 200, 140], 4.5, SEC[0] - 1.6, 3.4, SEC[2] - 1.6);
    const tankParts: THREE.Object3D[] = [];
    const tank = new THREE.Mesh(new THREE.PlaneGeometry(secW * 2 + 1.6, tankTop), new THREE.MeshBasicMaterial({ color: "#3f8fb0", fog: false }));
    tank.position.set(SEC[0], tankTop / 2, SEC[2] - 0.45); tank.layers.set(NOINK); tankParts.push(tank);
    const glass = new THREE.Mesh(new THREE.PlaneGeometry(secW * 2 + 1.6, tankTop), new THREE.MeshBasicMaterial({ color: "#8fd8ec", transparent: true, opacity: 0.14, depthWrite: false, fog: false }));
    glass.position.set(SEC[0], tankTop / 2, SEC[2] + 0.45); glass.layers.set(NOINK); tankParts.push(glass);
    const wl = new THREE.Mesh(new THREE.BoxGeometry(secW * 2 + 1.6, 0.035, 0.02), new THREE.MeshBasicMaterial({ color: "#e8fbff", fog: false }));
    wl.position.set(SEC[0], tankTop, SEC[2] + 0.46); wl.layers.set(NOINK); tankParts.push(wl);
    const tankEdge = new THREE.Mesh(new THREE.BoxGeometry(secW * 2 + 1.7, 0.06, 0.95), lambert({ color: "#5b3a22" })); tankEdge.position.set(SEC[0], 0.03, SEC[2]); tankParts.push(tankEdge);
    for (const p of tankParts) ctx.root.add(p);
    // labels sit inside the frame, on or right beside what they name (v4: clipped at the edges, too small)
    const guns = tagSprite("BRONZE GUNS", 0.5), stones = tagSprite("STONE", 0.5), low = tagSprite("LOWER GUN PORTS", 0.56), cgTag = tagSprite("CENTRE OF GRAVITY", 0.4);
    const heavy = tagSprite("HEAVY", 0.2), light = tagSprite("LIGHT", 0.2), sHeavy = tagSprite("HEAVY", 0.36), sLight = tagSprite("LIGHT", 0.36);
    for (const s2 of [guns, stones, low, cgTag, heavy, light, sHeavy, sLight]) ctx.root.add(s2);
    const fade = (s2: THREE.Object3D, a: number, b: number, t: number) => { const o = sm((t - a) / 0.25) * (1 - sm((t - b) / 0.25)); s2.visible = o > 0.01; ((s2 as THREE.Sprite).material as THREE.SpriteMaterial).opacity = o; };
    return (t) => {
      // the good bottle floats upright and bobs; the upside-down one is dropped in on "upside" and rolls over
      good.g.rotation.z = 0.25 * Math.exp(-(t - S(10)) * 0.8) * Math.cos((t - S(10)) * 4.5);
      good.g.position.y = 0.03 * Math.sin(t * 3);
      const roll = sm((t - upside) / 0.9) * Math.PI * 0.94;
      bad.outer.visible = t >= upside - 0.6;
      bad.g.rotation.z = -(roll + 0.06 * Math.sin(Math.max(0, t - upside) * 6) * (1 - sm((t - upside) / 0.6)));
      bad.g.position.y = 2.2 * (1 - sm((t - (upside - 0.6)) / 0.55)) + 0.03 * Math.sin(t * 3 + 1);
      heavy.position.set(BT[0] - 0.45 + 0.42, 0.62, BT[2] + 0.4); fade(heavy, heavyW - 0.05, upside - 0.1, t);
      light.position.set(BT[0] - 0.45 + 0.42, 1.22, BT[2] + 0.4); fade(light, lightW - 0.05, upside - 0.1, t);
      // the section: dropped into the tank on "upside", guns pop in on "bronze", a thin layer of stone on "stone",
      // more stone on "more", which pushes the ports down to the waterline
      const on = t >= upside - 0.2;
      sec.root.visible = on;                                   // the tank is there from the start; the hull drops into it
      const drop = 1 - sm((t - (upside - 0.2)) / 0.5);
      sec.guns.forEach((g, i) => { const k = sm((t - (bronze - 0.15) - i * 0.08) / 0.3); g.visible = k > 0.01; g.scale.setScalar(Math.max(0.001, k)); });
      sec.stones.forEach((s2, i) => { s2.visible = t >= stoneW - 0.4 + i * 0.012; });
      sec.more.forEach((s2, i) => { s2.visible = t >= more + i * 0.03; });
      const extra = ramp(t, pushed - 0.2, waterline + 0.1, 0, 1);
      sec.root.position.set(SEC[0], tankTop - extra * 1.25 * SEC_K + drop * 1.6, SEC[2]);
      sec.lowPorts.forEach((p) => (p.material as THREE.MeshBasicMaterial).color.set(extra > 0.85 ? "#e0442e" : "#1a1424"));
      sec.cg.position.y = (ramp(t, bronze, bronze + 0.6, -1.2, 2.2) - ramp(t, more, more + 0.5, 0, 0.6)) * SEC_K;
      sec.cg.visible = t >= bronze;
      const y0 = sec.root.position.y;
      sHeavy.position.set(SEC[0], y0 + 2.6 * SEC_K, SEC[2] + 0.7); fade(sHeavy, upside + 0.3, bronze, t);
      sLight.position.set(SEC[0], y0 - 2.6 * SEC_K, SEC[2] + 0.7); fade(sLight, upside + 0.3, stoneW - 0.4, t);
      guns.position.set(SEC[0], y0 + (deckTop(0.5) + 1.1) * SEC_K, SEC[2] + 0.7); fade(guns, bronze, more, t);
      cgTag.position.set(SEC[0] + 0.9, y0 + sec.cg.position.y + 0.25, SEC[2] + 0.7); fade(cgTag, bronze + 0.5, pushed - 0.3, t);
      stones.position.set(SEC[0], y0 + (-DRAFT + 1.9) * SEC_K, SEC[2] + 0.7); fade(stones, stoneW - 0.3, pushed, t);
      low.position.set(SEC[0], tankTop + 0.32, SEC[2] + 0.7); fade(low, pushed, lastT, t);
    };
  };
  {
    groups.push({ id: "explain", t0: S(10), t1: tooLittle, xfade: 0, set: explainSet, light: "explain",
      cam: [
        fit(S(10), [bottleBox], 8, 10, 38, { b: 0.42 }),                         // the bottle with sand floats upright
        fit(heavyW, [[BT[0] - 0.95, 0, BT[2] - 0.4, BT[0] + 0.1, 1.5, BT[2] + 0.4]], 4, 6, 34, { b: 0.42 }),   // heavy low, light on top
        fit(upside, [bottleBox], 6, 8, 38, { b: 0.42 }),                         // built upside down: the other bottle rolls over
        fit(bronze, [secBox], 10, 8, 38, { b: 0.38, x: 0.08 }),                  // the Vasa's section: tons of bronze up high
      ],
      people: [], rigs: [explainRig], avoid: (t) => (t < upside ? [bottleBox] : [secBox]) });
  }
  // ================= G12b ... and too little stone below (the ballast going aboard at the quay)
  {
    const t0 = tooLittle, t1 = S(12);
    const loaders: V3[] = [[-3.2, 1.8, -10.8], [-1.6, 1.8, -11.6], [0.2, 1.8, -10.6], [1.8, 1.8, -11.4]];
    groups.push({ id: "ballast", t0, t1, xfade: 0.4, set: () => harbourSet(), light: "day",
      cam: [fit(t0, [[-6, 1.8, -12.5, 6, 6.5, -5]], -170, 10, 42, { b: 0.32 }, loaders.map((l) => personBox(l))), fit(t1, [[-5, 1.8, -12.5, 5, 6, -5]], -160, 6, 40, { b: 0.32 }, loaders.map((l) => personBox(l)))],
      people: loaders.map((l, i): PersonSpec => ({ id: `l${i}`, flip: i % 2 === 1, at: (t) => [l[0] + 0.3 * Math.sin(t * 2 + i), l[1], l[2]],
        props: () => ({ costume: i % 2 ? "sailor2" : "sailor", seed: i * 3, pose: "hold", walk: 1, face: "focus" }) })),
      rigs: [shipRig(() => ({ sails: 0, lids: 0 }), {}), waterRig(), (ctx) => {
        const stone = lambert({ color: "#a8a8b2" });
        for (let k = 0; k < 14; k++) { const r = new THREE.Mesh(new THREE.DodecahedronGeometry(0.28 + (k % 3) * 0.08), stone); r.position.set(-5 + (k % 7) * 0.45, 2.0 + Math.floor(k / 7) * 0.35, -13.2 + (k % 2) * 0.4); r.castShadow = true; ctx.root.add(r); }
        const plank = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.12, 6), lambert({ color: "#7a5532" })); plank.position.set(0.5, 3.3, -7.6); plank.rotation.x = -0.45; plank.castShadow = true; ctx.root.add(plank);
        return () => undefined;
      }],
      avoid: () => [[-6, 1.8, -12.5, 6, 6.5, -5]] });
  }
  {
    groups.push({ id: "explain2", t0: S(12), t1: lastT, xfade: 0.4, set: explainSet, light: "explain",
      cam: [
        fit(S(12), [secBox], 6, 10, 38, { b: 0.38, x: 0.08 }),                   // more stone
        fit(pushed, [secBox], -8, 6, 38, { b: 0.38, x: 0.08 }),                  // pushes the ports down to the waterline
      ],
      people: [], rigs: [explainRig], avoid: () => [secBox] });
  }
  // ================= G13 the last line: the test at the dock was the warning (rolls her hard; the ports near the water)
  {
    const t0 = lastT, t1 = T.total;
    const showing = w(13, "showing");
    const sinkW = w(13, "sink");
    const W_T0 = sinkW - 0.05 + 0.35 - 6 * 0.8;                      // the biggest roll lands on "sink"
    groups.push(deckGroup("warning", t0, t1, 0.4, W_T0, 0.8, 6, 0.32, t1 + 1, sinkW, (st, at, oth) => {
      const run = (t: number) => runners.slice(3, 8).map((r) => personBox(at(r, t)));
      return [
        fit(t0, run(t0), -15, 26, 42, { b: 0.35 }, oth(t0)),                                     // thirty sailors, rolling her at the dock
        fit(showing, [[-24, -0.5, -8, 12, 12, 8]], -112, 20, 40, { b: 0.42, t: 0.3 }),      // over the sheds: the roll at the dock                    // from the quay: the deck rolling over the port row
        fit(sinkW, [[-16, -1, -8, 4, 6, -4]], -122, 16, 34, { b: 0.42, t: 0.3 }),                          // the ports at the water: how she would sink
      ];
    }));
  }

  const tags: Tag[] = [
    { text: "STOCKHOLM, 1628", at: navy + 0.1, out: S(1) - 0.3 },
    { text: "POLAND", at: S(2) + 0.1, out: S(3) - 0.3 },
    { text: "10 AUGUST 1628", at: S(5) + 0.1, out: tSail - 0.1 },
  ];
  // the roll gauge (the test, the gusts, the last line) and the distance counter (cast off to the sinking)
  const hookHeel = (t: number) => heelFromRuns(RUNS(HOOK_T0, 1.0, 5), HOOK_T0, 1.0, 0.3, over + 0.1)(t);
  const sinkW = w(13, "sink"), W_T0 = sinkW - 0.05 + 0.35 - 6 * 0.8;
  const lastHeel = (t: number) => heelFromRuns(RUNS(W_T0, 0.8, 6), W_T0, 0.8, 0.32, sinkW)(t);
  const heel = (t: number): number | null => {
    if (t < navy) return hookHeel(t);
    if (t >= gust1 - 0.4 && t < S(8)) return voyageHeel(t);
    if (t >= lastT + 0.2) return lastHeel(t);
    return null;
  };
  const dist = (t: number): number | null => (t >= tSail + 0.2 && t < S(9) - 0.2 ? Math.min(1300, Math.max(0, (t - tSail) / (w(8, "sinks") - tSail)) * 1300) : null);
  return { groups, tags, heel, dist };
}

/** wind gusts: white streaks that sweep across the sails */
function gustRig(at: number[], shipX: (t: number) => number): Rig {
  return (ctx) => {
    const streaks: THREE.Mesh[] = [];
    for (let i = 0; i < 16; i++) {
      const m = new THREE.Mesh(new THREE.PlaneGeometry(9, 0.25), new THREE.MeshBasicMaterial({ color: "#ffffff", transparent: true, opacity: 0.7, fog: false, side: THREE.DoubleSide, depthWrite: false }));
      m.layers.set(NOINK); ctx.root.add(m); streaks.push(m);
    }
    void glowSprite;
    return (t) => {
      let k = -1;
      for (const a of at) if (t >= a && t < a + 1.1) k = (t - a) / 1.1;
      streaks.forEach((m, i) => {
        m.visible = k >= 0;
        if (k < 0) return;
        const x = shipX(t);
        m.position.set(x + (-6 + i * 0.9), 6 + (i % 5) * 7, -30 + k * 60 + (i % 3) * 3);
        m.rotation.y = Math.PI / 2;
        (m.material as THREE.MeshBasicMaterial).opacity = 0.75 * Math.sin(k * Math.PI);
      });
    };
  };
}
