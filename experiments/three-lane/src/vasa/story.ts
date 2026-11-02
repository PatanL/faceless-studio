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
  const h = s.heel ?? 0, yaw = s.yaw ?? 0, pi = s.pitch ?? 0;
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
const heelFromRuns = (runs: (t: number) => number, t0: number, dur: number, gain: number) => (t: number) => {
  const lagged = runs(t - 0.35);
  const n = clamp01((t - t0) / (dur * 3));
  return lagged * (0.03 + gain * n);
};

// ------------------------------------------------------------------------------------------------ props
/** a weighted toy (roly-poly): a hemisphere base and a light body; heavy: where the iron sits ("bottom" | "top") */
function toy(heavy: "bottom" | "top") {
  const g = new THREE.Group();                 // pivot = base sphere centre
  const iron = lambert({ color: "#2b2b3a" }), cream = lambert({ color: "#efe4c8" }), red = lambert({ color: "#c0392b" });
  const base = new THREE.Mesh(new THREE.SphereGeometry(0.32, 24, 16, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2), heavy === "bottom" ? iron : cream);
  base.castShadow = true; g.add(base);
  const body = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.32, 0.5, 20), cream); body.position.y = 0.25; body.castShadow = true; g.add(body);
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.2, 18, 14), cream); head.position.y = 0.62; head.castShadow = true; g.add(head);
  const hat = new THREE.Mesh(new THREE.ConeGeometry(0.16, 0.26, 16), heavy === "top" ? iron : red); hat.position.y = 0.88; g.add(hat);
  if (heavy === "top") { const w = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 0.16, 16), iron); w.position.y = 0.78; g.add(w); }
  for (const dx of [-0.07, 0.07]) { const e = new THREE.Mesh(new THREE.SphereGeometry(0.025, 8, 6), iron); e.position.set(dx, 0.66, 0.18); g.add(e); }
  const outer = new THREE.Group(); outer.add(g); g.position.y = 0.32;
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
  const back = new THREE.Mesh(new THREE.ShapeGeometry(sh), lambert({ color: "#6a4630" })); back.position.z = -0.27; body.add(back);
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
    const p = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.7 * k, 0.52), portMat.clone()); p.position.set(side * halfW(u, y) * k, y * k, 0); body.add(p);
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

  // ---- the running test (hook and scene 4): the ship moored at the quay, eight runners for the thirty
  const runners: { id: string; costume: string; x: number; dz: number }[] = [
    { id: "s1", costume: "sailor", x: -6, dz: 0 }, { id: "s2", costume: "sailor2", x: -4, dz: 0.6 }, { id: "s3", costume: "sailor", x: -2, dz: -0.4 },
    { id: "s4", costume: "sailor2", x: 3.6, dz: 0.3 }, { id: "s5", costume: "sailor", x: 5.6, dz: -0.6 }, { id: "s6", costume: "sailor2", x: 7.6, dz: 0.2 },
    { id: "s7", costume: "sailor", x: 9.6, dz: -0.2 }, { id: "s8", costume: "sailor2", x: 11.3, dz: 0.5 }];
  const deckGroup = (id: string, t0: number, t1: number, xfade: number, runT0: number, runDur: number, nRuns: number, gain: number,
    stopAt: number, cams: (st: (t: number) => ShipState, at: (r: typeof runners[0], t: number) => V3, oth: (t: number) => Box[]) => GroupSpec["cam"], admiral: Partial<PersonSpec> = {}): GroupSpec => {
    const runs = RUNS(runT0, runDur, nRuns);
    const heel = heelFromRuns(runs, runT0, runDur, gain);
    const st = (t: number): ShipState => ({ heel: heel(t), lids: 0, sails: 0 });
    const at = (r: typeof runners[0], t: number): V3 => {
      const zz = runs(t) * (halfW(uOf(r.x), deckY(r.x)) - 1.3) + r.dz;
      return shipPt(st(t), [r.x, deckY(r.x), zz]);
    };
    const hold: { ship?: Ship } = {};
    const ADM: V3 = [-9.6, 0, 1.4], CAPT: V3 = [-9.6, 0, -1.6];
    const oth = (t: number): Box[] => [...runners.map((r) => personBox(at(r, t))), personBox(shipPt(st(t), [ADM[0], deckY(ADM[0]), ADM[2]])), personBox(shipPt(st(t), [CAPT[0], deckY(CAPT[0]), CAPT[2]]))];
    return {
      id, t0, t1, xfade, set: () => harbourSet(), light: "day",
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

  // ================= G1 hook: thirty sailors run across the new warship; the admiral stops the test
  {
    const t0 = 0, t1 = w(0, "and", 2) - 0.05;
    const stopAt = w(0, "stopped");
    groups.push(deckGroup("test", t0, t1, 0, 0.0, 1.05, 3, 0.07, stopAt, (st, at, oth) => {
      const run = (t: number) => runners.slice(2, 6).map((r) => personBox(at(r, t)));
      return [
        fit(0, [...run(0.6)], 25, 42, 42, { b: 0.25 }, oth(0)),                                   // across the deck: the runners
        fit(w(0, "third"), [...run(w(0, "third")), personBox(shipPt(st(3.3), [-9.6, deckY(-9.6), 1.4]))], -35, 38, 42, { b: 0.25 }, oth(w(0, "third"))),
        fit(stopAt, [personBox(shipPt(st(stopAt), [-9.6, deckY(-9.6), 1.4]), false, true)], 60, 8, 38, {}, oth(stopAt)),   // the admiral: stop
      ];
    }));
  }

  // ================= G2 ... and the ship sailed anyway (a glimpse ahead: sails set, leaving the quay)
  const sailing = (t: number, tStart: number): ShipState => ({ x: 6 + Math.max(0, t - tStart) * 2.2, sails: 1, lids: 1, guns: 0.6 });
  {
    const t0 = w(0, "and", 2) - 0.05, t1 = S(1);
    const hold: { ship?: Ship } = {};
    const st = (t: number) => sailing(t, t0 - 2);
    groups.push({ id: "anyway", t0, t1, xfade: 0.233, set: () => harbourSet(), light: "golden",
      cam: [fit(t0, [hullBox(st(t0), true)], 140, 6, 40, { b: 0.2 }), fit(t1, [hullBox(st(t1), true)], 125, 3, 42, { b: 0.2 })],
      people: [], rigs: [shipRig(st, hold), waterRig()], avoid: (t) => [hullBox(st(t))] });
  }

  // ================= G3 Stockholm, 1628: the harbour from above, the Vasa at the shipyard quay
  const moored: ShipState = { sails: 0, lids: 0 };
  {
    const t0 = S(1), t1 = w(1, "the", 1) - 0.1;
    groups.push({ id: "harbour", t0, t1, xfade: 0.233, set: () => harbourSet(), light: "day",
      cam: [fit(t0, [hullBox(moored, true), [-40, 0, -25, 60, 8, 30]], 30, 34, 44, { b: 0.2 }), fit(t1, [hullBox(moored, true)], 40, 22, 42, { b: 0.2 })],
      people: [], rigs: [shipRig(() => moored, {}), waterRig()], avoid: () => [hullBox(moored, true)] });
  }

  // ================= G4 the king at war in Poland, ordering the guns
  {
    const t0 = w(1, "the", 1) - 0.1, t1 = w(1, "orders") - 0.05;
    const KING: V3 = [-0.4, 0, -1.3];
    groups.push({ id: "camp", t0, t1, xfade: 0.233, set: campSet, light: "day",
      cam: [fit(t0, [personBox(KING, true), [-0.2, 0, -1.9, 1.4, 1.0, -0.9]], 24, 10, 40, {}, [personBox([1.5, 0, -2.2])]), fit(t1, [personBox(KING, true, true), [0, 0.7, -1.8, 1.3, 0.9, -1.0]], 36, 16, 36, {}, [personBox([1.5, 0, -2.2])])],
      people: [{ id: "king", at: () => KING, props: (t) => ({ costume: "king", seated: true, seed: 3, pose: "hold", item: "letter", face: step(t, [[0, "focus"], [w(1, "war") - 0.1, "smug"]]) }) },
        { id: "aide", flip: true, at: () => [1.5, 0, -2.2], props: () => ({ costume: "citizen2", seed: 9, pose: "stand", face: "neutral" }) }],
      avoid: () => [[-0.8, 0, -2, 1.6, 1.4, -0.8]] });
  }

  // ================= G5 the quay: heavy cannons swung aboard, two decks of guns, the gilded stern
  {
    const t0 = w(1, "orders") - 0.05, t1 = S(3);
    const two = w(2, "two"), stacked = w(2, "stacked"), hundreds = w(2, "hundreds");
    const st = (t: number): ShipState => ({ lids: ramp(t, two, two + 0.6, 0, 1), guns: ramp(t, two + 0.2, two + 0.9, 0, 1), sails: 0 });
    const WR: V3 = [10.5, 1.8, -11.4];
    groups.push({ id: "guns", t0, t1, xfade: 0.233, set: () => harbourSet(), light: "day",
      cam: [
        fit(t0, [[4, 1.8, -14, 13, 17, -3], personBox(WR)], 128, 8, 40),                         // the derrick swings a gun aboard
        fit(w(1, "vasa"), [hullBox(st(w(1, "vasa")))], 30, 10, 42, { b: 0.25 }),                    // the Vasa
        fit(two, [[-14, 0.6, 3, 10, 4.6, 7]], 18, 4, 40, { b: 0.3 }),                              // two rows of ports open, guns run out
        fit(stacked, [[-6, -0.2, 4, 6, 4.6, 7]], 12, -2, 34, { b: 0.3 }),                          // low at the waterline: stacked high
        fit(hundreds, [[-24.5, 0, -6, -22.5, 10.2, 6]], -88, 6, 38, { b: 0.25, t: 0.1 }),           // the gilded stern
      ],
      people: [{ id: "wright", flip: true, at: () => WR, props: () => ({ costume: "shipwright", seed: 4, pose: "point", face: "smug" }) },
        { id: "wright2", at: () => [5.5, 1.8, -12.5], props: () => ({ costume: "sailor2", seed: 6, pose: "push", face: "focus" }) }],
      rigs: [shipRig(st, {}), waterRig(), (ctx) => {
        const hang = ctx.set.extra.hanging as THREE.Mesh, line = ctx.set.extra.line as THREE.Mesh;
        return (t) => {
          const u = clamp01((t - t0) / 2.4);
          const p = new THREE.Vector3(8, 15 - 10 * sm(u), -6 + 2.5 * sm(u));
          hang.position.copy(p); hang.visible = u < 1;
          const a = new THREE.Vector3(8, 17.1, -0.5 + 0), b = p.clone().add(new THREE.Vector3(0, 0.3, 0));
          line.position.copy(a).lerp(b, 0.5); line.scale.set(1, a.distanceTo(b), 1); line.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), b.clone().sub(a).normalize()); line.visible = u < 1;
        };
      }],
      avoid: (t) => (t > hundreds - 0.3 ? [[-24.5, 0, -6, -22.5, 10.2, 6]] : []) });
  }

  // ================= G6 the test again: every run rocks her harder; the admiral wishes the king were home
  {
    const t0 = S(3), t1 = w(3, "the", 3) - 0.05;
    const adm = w(3, "admiral");
    groups.push(deckGroup("test2", t0, t1, 0.233, t0 - 0.2, 0.95, 4, 0.11, adm - 0.1, (st, at, oth) => {
      const run = (t: number) => runners.slice(0, 5).map((r) => personBox(at(r, t)));
      const admAt = (t: number) => shipPt(st(t), [-9.6, deckY(-9.6), 1.4]);
      return [
        fit(t0, run(t0 + 0.4), -25, 30, 42, { b: 0.28 }, oth(t0)),                                       // low at the rail: the horizon tips
        fit(w(3, "harder"), run(w(3, "harder")), 25, 32, 40, { b: 0.28 }, oth(w(3, "harder"))),
        fit(adm, [personBox(admAt(adm), false, true)], 50, 6, 36, {}, oth(adm)),                               // the admiral close
        fit(t1, [personBox(admAt(t1), false, true), personBox(shipPt(st(t1), [-9.6, deckY(-9.6), -1.6]), false, true)], 75, 8, 38, {}, oth(t1)),
      ];
    }, { props: (t: number) => ({ costume: "admiral", seed: 5, pose: t >= adm ? "handIn" : "hips", face: t >= adm ? "worried" : "frown" }) }));
  }

  // ================= G7 the king's letters: get her to sea
  {
    const t0 = w(3, "the", 3) - 0.05, t1 = S(4);
    const KING: V3 = [-0.4, 0, -1.3];
    groups.push({ id: "letters", t0, t1, xfade: 0.233, set: campSet, light: "golden",
      cam: [fit(t0, [personBox(KING, true, true), [0, 0.7, -1.8, 1.3, 0.9, -1.0]], -30, 12, 36), fit(t1, [personBox(KING, true, true)], -18, 6, 34)],
      people: [{ id: "king", at: () => KING, props: () => ({ costume: "king", seated: true, seed: 3, pose: "point", item: "letter", face: "angry" }) },
        { id: "courier", flip: true, at: () => [1.7, 0, -0.9], props: () => ({ costume: "citizen2", seed: 9, pose: "reach", face: "worried" }) }],
      avoid: () => [[-0.8, 0, -2, 1.6, 1.4, -0.8]] });
  }

  // ================= G8 10 August: the crowd, four sails, the two gusts (one continuous sail across the harbour)
  const tSail = w(4, "four") - 0.6;
  const gust1 = w(5, "gust"), rights = w(5, "rights"), gust2 = w(5, "gust", 2), under = w(5, "under");
  const voyageHeel = (t: number) => track(t, [[gust1 - 0.15, 0], [gust1 + 0.45, 0.24], [rights - 0.1, 0.18], [rights + 0.5, 0.06], [gust2 - 0.05, 0.05], [gust2 + 0.7, 0.3], [under + 0.3, 0.42], [S(6) + 1.0, 0.55]]);
  const voyage = (t: number): ShipState => ({ x: 30 + Math.max(0, t - tSail) * 2.4, sails: ramp(t, tSail, tSail + 0.9, 0, 1), lids: 1, guns: 0.7, heel: voyageHeel(t) });
  const crowd: { id: string; costume: string; x: number; z: number }[] = [
    { id: "c1", costume: "citizen", x: -6, z: -10.6 }, { id: "c2", costume: "citizen2", x: -4.6, z: -11.4 }, { id: "c3", costume: "sailor", x: -3, z: -10.4 },
    { id: "c4", costume: "citizen", x: -1.4, z: -11.6 }, { id: "c5", costume: "citizen2", x: 0.2, z: -10.6 }, { id: "c6", costume: "shipwright", x: 1.8, z: -11.2 }];
  const crowdPeople = (react: number): PersonSpec[] => crowd.map((c, i) => ({ id: c.id, flip: false, at: () => [c.x, 1.8, c.z],
    props: (t) => ({ costume: c.costume, seed: i * 3 + 1, pose: t >= react ? (i % 2 ? "armsUp" : "shrug") : (i % 3 === 0 ? "point" : "stand"), face: t >= react ? "shock" : (i % 2 ? "smile" : "grin") }) }));
  const crowdBox = (): Box => [-6.4, 1.8, -12, 2.2, 3.5, -10];
  {
    const t0 = S(4), t1 = S(6);
    const four = w(4, "four"), tips = w(5, "tips");
    groups.push({ id: "launch", t0, t1, xfade: 0.233, set: () => harbourSet({ cannonsOnQuay: false }), light: "golden",
      cam: [
        fit(t0, [crowdBox(), hullBox(voyage(t0), true)], -150, 8, 42, { b: 0.2 }),               // behind the crowd: the Vasa ready
        fit(w(4, "crowd"), [crowdBox()], 15, 6, 38),                                               // the crowd on the quay
        fit(four, [[voyage(four).x! - 14, 12, -6, voyage(four).x! + 16, 50, 6]], 40, -8, 44, { b: 0.15 }),   // four sails go up
        fit(tips, [hullBox(voyage(tips), true)], 90, 4, 42, { b: 0.18 }),                         // from the water: she heels
        fit(gust2, [hullBox(voyage(gust2))], 70, 2, 40, { b: 0.25 }),
        fit(under, [[voyage(under).x! - 16, -0.5, 3, voyage(under).x! + 14, 5, 7]], 20, 0.5, 34, { b: 0.3 }),   // the ports go under
      ],
      people: crowdPeople(tips),
      rigs: [shipRig(voyage, {}), waterRig(), gustRig([gust1 - 0.2, gust2 - 0.2], (t) => voyage(t).x!)],
      avoid: (t) => [hullBox(voyage(t))] });
  }

  // ================= G9 the gun deck floods (inside, heeling)
  {
    const t0 = S(6), t1 = w(6, "and", 1) + 0.1;
    groups.push({ id: "gundeck", t0, t1, xfade: 0.233, set: gundeckSet, light: "golden",
      cam: [{ t: t0, pos: [-1.2, 1.25, 9], look: [1.2, 0.7, -6], fov: 50 }, { t: t1, pos: [-1.4, 1.35, 6.5], look: [1.6, 0.6, -8], fov: 50 }],
      people: [{ id: "gunner", at: (t) => [-1.2 + Math.max(0, t - t0) * 0.5, 0, -2.5], props: () => ({ costume: "sailor2", seed: 2, pose: "armsUp", walk: 1, face: "shock" }) }],
      rigs: [(ctx) => {
        const room = ctx.set.extra.room as THREE.Group, flood = ctx.set.extra.flood as THREE.Mesh;
        const pours: THREE.Mesh[] = [];
        for (let k = 0; k < 11; k++) {
          const m = new THREE.Mesh(new THREE.PlaneGeometry(0.75, 1.0), new THREE.MeshBasicMaterial({ color: "#7fc4d6", transparent: true, opacity: 0.85, fog: false, side: THREE.DoubleSide }));
          m.position.set(4.3, 0.55, -16 + k * 3.2); m.rotation.y = Math.PI / 2; m.layers.set(NOINK); room.add(m); pours.push(m);
        }
        const spray = new Rising(30, "puff", 0.12, 4); spray.group.position.set(4.2, 0.6, 0); room.add(spray.group);
        return (t) => {
          room.rotation.z = 0.32 + 0.05 * sm((t - t0) / 1.4);
          flood.position.y = ramp(t, t0, t1 + 0.4, 0.02, 0.6);
          pours.forEach((m, i) => { m.scale.set(1, 0.8 + 0.25 * Math.sin(t * 13 + i), 1); m.position.y = 0.5 - 0.05 * Math.sin(t * 9 + i); });
          spray.update(t, 1, 1.0, 0.8, 16);
        };
      }],
      avoid: () => [] });
  }

  // ================= G10 1,300 metres out, in front of everyone, she sinks
  {
    const t0 = w(6, "and", 1) + 0.1, t1 = S(7);
    const sinks = w(6, "sinks");
    const st = (t: number): ShipState => ({ ...voyage(Math.min(t, sinks - 0.6)), heel: track(t, [[t0, 0.6], [sinks, 1.05], [t1, 1.25]]), sink: ramp(t, t0, t1 + 0.6, 1.0, 26), sails: 1 });
    groups.push({ id: "sinking", t0, t1, xfade: 0.233, set: () => harbourSet({ cannonsOnQuay: false }), light: "golden",
      cam: [
        fit(t0, [crowdBox(), hullBox(st(t0), true)], -150, 6, 40, { b: 0.2 }),                   // from the quay, behind the crowd
        fit(w(6, "everyone"), [crowdBox()], 20, 6, 38),                                           // everyone watching
        fit(sinks, [hullBox(st(sinks), true)], 100, 3, 40, { b: 0.2 }),                           // she goes down
        fit(w(6, "die"), [[st(t1).x! - 20, -1, -10, st(t1).x! + 20, 8, 10]], 80, 10, 40, { b: 0.2 }),
      ],
      people: crowdPeople(t0),
      rigs: [shipRig(st, {}), waterRig(), (ctx) => {
        const bub = new Rising(40, "puff", 1.2, 6); ctx.root.add(bub.group);
        const debris: THREE.Mesh[] = [];
        for (let i = 0; i < 14; i++) { const d = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.3, 0.5), lambert({ color: "#6b4a2b" })); ctx.root.add(d); debris.push(d); }
        const boats: THREE.Mesh[] = [];
        for (let i = 0; i < 3; i++) { const b = new THREE.Mesh(new THREE.BoxGeometry(4, 0.8, 1.6), lambert({ color: "#7a5532" })); b.castShadow = true; ctx.root.add(b); boats.push(b); }
        return (t) => {
          const x = st(t).x!;
          bub.group.position.set(x, 0, 2); bub.update(t, ramp(t, sinks - 0.5, sinks + 0.3, 0, 1), 3, 1.2, 14);
          debris.forEach((d, i) => { const a = i * 2.4; d.position.set(x + Math.cos(a) * (3 + i * 0.6), 0.15 + 0.05 * Math.sin(t * 3 + i), Math.sin(a) * (3 + i * 0.5)); d.rotation.y = a + t * 0.2; d.visible = t > sinks - 0.2; });
          boats.forEach((b, i) => { b.position.set(x - 30 + i * 6 + (t - t0) * 3.5, 0.3, -14 + i * 9); b.rotation.y = 0.2; });
        };
      }],
      avoid: (t) => [hullBox(st(t))] });
  }

  // ================= G11 the inquiry: no one is punished; "Only God knows"
  {
    const t0 = S(7), t1 = S(8);
    setRoom([-5.6, 0.2, -19.6, 5.6, 6, 7.6]);
    const J1: V3 = [-1.4, 0, -9], J2: V3 = [0, 0, -9.2], J3: V3 = [1.4, 0, -9], B: V3 = [0.2, 0, -6.6], A: V3 = [-2.2, 0, -6.8];
    const judges = [J1, J2, J3];
    const only = w(7, "only");
    groups.push({ id: "inquiry", t0, t1, xfade: 0.233, set: () => hallSet(false), light: "day",
      cam: [
        fit(t0, [...judges.map((j) => personBox(j, true)), personBox(B), personBox(A)], 0, 10, 42, {}, [personBox(B), personBox(A)]),
        fit(only, [personBox(B, false, true)], 20, 2, 36, {}, [personBox(A), ...judges.map((j) => personBox(j, true))]),
      ],
      people: [
        ...judges.map((j, i): PersonSpec => ({ id: `j${i}`, flip: i === 2, at: () => j, props: () => ({ costume: i === 1 ? "admiral" : "citizen2", seated: true, seed: 11 + i, pose: i === 1 ? "point" : "hold", face: "frown" }) })),
        { id: "builder", flip: true, at: () => B, props: (t) => ({ costume: "shipwright", seed: 4, pose: t >= only - 0.2 ? "shrug" : "stand", face: t >= only - 0.2 ? "worried" : "neutral" }) },
        { id: "accused", at: () => A, props: () => ({ costume: "captain", seed: 8, pose: "stand", face: "worried" }) },
      ],
      rigs: [(ctx) => { const tab = new THREE.Mesh(new THREE.BoxGeometry(4.6, 0.8, 1.0), lambert({ color: "#4a2e1c" })); tab.position.set(0, 0.4, -8.3); tab.castShadow = true; ctx.root.add(tab); return () => undefined; }],
      avoid: () => [personBox(B), ...judges.map((j) => personBox(j, true))] });
    setRoom(null);
  }

  // ================= G12 the explanation (night blue): weighted toys, the hull cross-section, the ballast, the warning
  const SEC_K = 0.4, SEC: V3 = [2.0, 0, -6.2];
  const pivot = w(8, "you") - 0.05, toyW = w(8, "weighted"), heavyW = w(8, "heavy"), opp = w(9, "opposite"), cannons = w(9, "cannons"), stoneW = w(9, "stone");
  const needed = w(10, "needed"), push = w(10, "push"), waterline = w(10, "waterline"), menW = w(11, "men"), warning = w(11, "warning");
  {
    const t0 = S(8), t1 = menW + 0.9;
    const secW = halfW(0.5, 0) * SEC_K;
    const secBox: Box = [SEC[0] - secW - 0.6, 0, SEC[2] - 0.5, SEC[0] + secW + 0.6, (deckTop(0.5) + DRAFT) * SEC_K + 0.6, SEC[2] + 0.5];
    const toysBox: Box = [-3.6, 0, -6.6, -1.8, 1.3, -5.6];
    const tankTop = DRAFT * SEC_K + 0.05;
    groups.push({ id: "explain", t0, t1, xfade: 0, set: explainSet, light: "explain",
      cam: [
        fit(t0, [toysBox], 8, 14, 38, { b: 0.35 }),                               // the weighted toy rocks back up
        fit(heavyW, [toysBox], 4, 8, 36, { b: 0.35 }),
        fit(opp, [toysBox, secBox], 6, 14, 42, { b: 0.3 }),                      // the top-heavy toy falls; the Vasa's section
        fit(cannons, [secBox], 10, 8, 38, { b: 0.3, x: 0.06 }),                   // guns high on two decks
        fit(stoneW, [[SEC[0] - secW, 0.3, SEC[2] - 0.4, SEC[0] + secW, 0.9, SEC[2] + 0.4]], 6, 18, 36, { b: 0.35 }),   // only stones below
        fit(push, [secBox], -8, 6, 38, { b: 0.3, x: 0.06 }),                      // more stone: the ports reach the water
        fit(menW, [secBox], 12, 10, 40, { b: 0.3, x: 0.06 }),
      ],
      people: [0, 1, 2].map((i): PersonSpec => ({ id: `m${i}`, scale: 0.22, at: (t) => {
        const runs = RUNS(menW - 0.9, 0.55, 6)(t);
        const heel = secHeel(t);
        const loc: V3 = [runs * 0.12 * (i + 1) * 0.9, (deckTop(0.5) - 0.25) * SEC_K + tankTop, (i - 1) * 0.12];
        const [x, y] = [loc[0] * Math.cos(heel) - (loc[1] - tankTop) * Math.sin(heel), loc[0] * Math.sin(heel) + (loc[1] - tankTop) * Math.cos(heel) + tankTop];
        return [SEC[0] + x, y, SEC[2] + loc[2]];
      }, visible: (t) => t >= menW - 1.0, props: (t) => ({ costume: i % 2 ? "sailor2" : "sailor", seed: i, pose: "sweep", walk: t < t1 ? 1 : 0, face: "focus" }) })),
      rigs: [(ctx) => {
        const good = toy("bottom"), bad = toy("top");
        good.outer.position.set(-3.2, 0, -6.1); bad.outer.position.set(-2.2, 0, -6.1); ctx.root.add(good.outer, bad.outer);
        const sec = sectionModel(SEC_K); sec.root.position.set(SEC[0], tankTop, SEC[2]); ctx.root.add(sec.root);
        glowSprite(ctx.root, [255, 200, 140], 6.5, SEC[0], 2.2, SEC[2] - 1.2);
        // the water: a blue backdrop behind the section, a faint front glass and a bright waterline, so the hull below
        // the water (and the stones in it) stays readable
        const tank = new THREE.Mesh(new THREE.PlaneGeometry(secW * 2 + 1.6, tankTop), new THREE.MeshBasicMaterial({ color: "#3f8fb0", fog: false }));
        tank.position.set(SEC[0], tankTop / 2, SEC[2] - 0.45); tank.layers.set(NOINK); ctx.root.add(tank);
        const glass = new THREE.Mesh(new THREE.PlaneGeometry(secW * 2 + 1.6, tankTop), new THREE.MeshBasicMaterial({ color: "#8fd8ec", transparent: true, opacity: 0.14, depthWrite: false, fog: false }));
        glass.position.set(SEC[0], tankTop / 2, SEC[2] + 0.45); glass.layers.set(NOINK); ctx.root.add(glass);
        const wl = new THREE.Mesh(new THREE.BoxGeometry(secW * 2 + 1.6, 0.035, 0.02), new THREE.MeshBasicMaterial({ color: "#e8fbff", fog: false }));
        wl.position.set(SEC[0], tankTop, SEC[2] + 0.46); wl.layers.set(NOINK); ctx.root.add(wl);
        const tankEdge = new THREE.Mesh(new THREE.BoxGeometry(secW * 2 + 1.7, 0.06, 0.95), lambert({ color: "#5b3a22" })); tankEdge.position.set(SEC[0], 0.03, SEC[2]); ctx.root.add(tankEdge);
        const guns = tagSprite("GUNS", 0.3), stones = tagSprite("BALLAST", 0.3), low = tagSprite("LOWER GUN PORTS", 0.26);
        for (const s of [guns, stones, low]) ctx.root.add(s);
        const fade = (s: THREE.Sprite, a: number, b: number, t: number) => { const o = sm((t - a) / 0.25) * (1 - sm((t - b) / 0.25)); s.visible = o > 0.01; (s.material as THREE.SpriteMaterial).opacity = o; };
        return (t) => {
          // toys: the good one is knocked at "weighted" and rocks back; the bad one tips over at "opposite"
          const dg = t - toyW;
          good.g.rotation.z = dg > 0 ? 0.55 * Math.exp(-dg * 1.4) * Math.cos(dg * 6.5) : 0;
          const db = t - opp;
          const fall = db > 0 ? Math.min(1.35, 0.15 * Math.exp(db * 3.2) - 0.15 + 0.12 * db) : 0;
          bad.g.rotation.z = -fall; bad.g.position.x = -fall * 0.32 * 0.5;
          // the section: appears at "opposite", guns rise into place on "cannons", stones on "stone", doubled on "needed"
          sec.root.visible = t >= opp - 0.3;
          const ap = sm((t - (opp - 0.3)) / 0.5); sec.root.scale.setScalar(Math.max(0.001, ap));
          sec.guns.forEach((g, i) => { const k = sm((t - cannons - i * 0.12) / 0.35); g.visible = k > 0.01; g.scale.setScalar(Math.max(0.001, k)); });
          sec.stones.forEach((s, i) => { s.visible = t >= stoneW - 0.2 + i * 0.01; });
          sec.more.forEach((s, i) => { s.visible = t >= needed + i * 0.03 && t < menW - 1.0; (s.material as THREE.MeshLambertMaterial).emissive?.set?.("#000000"); });
          // sink deeper with the extra ballast: the lower ports reach the waterline
          const extra = ramp(t, push - 0.2, waterline + 0.1, 0, 1) * (t < menW - 1.0 ? 1 : 0);
          sec.root.position.y = tankTop - extra * 1.25 * SEC_K;
          sec.lowPorts.forEach((p) => (p.material as THREE.MeshBasicMaterial).color.set(extra > 0.85 ? "#e0442e" : "#1a1424"));
          sec.root.rotation.z = secHeel(t);
          // centre of gravity: low (hull alone), high once the guns are in, a little lower with the stones
          sec.cg.position.y = (ramp(t, cannons, cannons + 0.6, -1.2, 2.2) - ramp(t, stoneW, stoneW + 0.4, 0, 0.5)) * SEC_K;
          sec.cg.visible = t >= cannons;
          guns.position.set(SEC[0] + 0.0, (DRAFT + 5.0) * SEC_K + 0.3, SEC[2] + 0.5); fade(guns, cannons + 0.2, needed, t);
          stones.position.set(SEC[0], 0.2 * SEC_K * 4 + 0.15, SEC[2] + 0.6); fade(stones, stoneW - 0.1, push, t);
          low.position.set(SEC[0] + secW * 0.2, tankTop + 0.75, SEC[2] + 0.6); fade(low, push + 0.2, menW - 0.9, t);
        };
      }],
      avoid: (t) => (t < opp ? [toysBox] : [secBox]) });
  }
  function secHeel(t: number) {
    const rock = RUNS(menW - 0.9, 0.55, 6)(t - 0.15);
    const k = clamp01((t - (menW - 0.9)) / 2.2);
    return t >= menW - 0.9 ? rock * (0.05 + 0.3 * k) : 0;
  }

  // ================= G13 the warning: back on the real deck, rolling harder with every run
  {
    const t0 = menW + 0.9, t1 = S(12);
    groups.push(deckGroup("warning", t0, t1, 0.233, t0 - 1.0, 0.8, 6, 0.16, t1 + 1, (st, at, oth) => {
      const run = (t: number) => runners.slice(1, 6).map((r) => personBox(at(r, t)));
      return [fit(t0, run(t0), 25, 40, 42, { b: 0.28 }, oth(t0)), fit(warning, run(warning), -30, 36, 40, { b: 0.28 }, oth(warning))];
    }));
  }

  // ================= G14 1961: raised from the mud
  {
    const t0 = S(12), t1 = w(12, "it", 2) - 0.1;
    const st = (t: number): ShipState => ({ x: 0, sink: ramp(t, w(12, "raised"), t1 + 0.5, 28, 17), heel: ramp(t, t0, t1, 0.12, 0.04), masts: false, sails: 0, lids: 0 });
    groups.push({ id: "seabed", t0, t1, xfade: 0.233, set: seabedSet, light: "underwater",
      cam: [fit(t0, [sternBox(st(t0))], 50, -4, 44, { b: 0.2 }), fit(t1, [sternBox(st(t1))], 30, -12, 44, { b: 0.2 })],
      people: [],
      rigs: [shipRig(st, {}, { carvings: true }), (ctx) => {
        const cables: THREE.Mesh[] = [];
        for (const x of [-12, -4, 4, 12]) { const c = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 1, 6), lambert({ color: "#2a2a30" })); ctx.root.add(c); cables.push(c); c.userData.x = x; }
        const bub = new Rising(30, "puff", 0.5, 9); ctx.root.add(bub.group);
        return (t) => {
          const s = st(t); const top = -(s.sink ?? 0) + 4;
          cables.forEach((c) => { c.position.set(c.userData.x, top / 2, 0); c.scale.set(1, Math.abs(top), 1); });
          bub.group.position.set(0, -(s.sink ?? 0), 0); bub.update(t, 0.8, 14, 3, 30);
        };
      }],
      avoid: (t) => [hullBox(st(t))] });
  }

  // ================= G15 the museum: almost whole, never sailing again
  {
    const t0 = w(12, "it", 2) - 0.1, t1 = T.total;
    const st: ShipState = { x: 0, sink: 0, heel: 0, masts: true, sails: 0, lids: 1, guns: 0.6 };
    const visitors: { id: string; costume: string; x: number; z: number }[] = [
      { id: "v1", costume: "plain", x: -8, z: 12 }, { id: "v2", costume: "master", x: -5.5, z: 13 }, { id: "v3", costume: "plain", x: 6, z: 12.5 }, { id: "v4", costume: "sailor", x: 9, z: 13.4 }];
    setRoom([-58, -5, -38, 58, 60, 60]);
    groups.push({ id: "museum", t0, t1, xfade: 0.233, set: museumHallSet, light: "museum",
      cam: [
        fit(t0, [sternBox(st), ...visitors.map((v) => personBox([v.x, -5.2, v.z]))], 30, 6, 46, { b: 0.2 }),
        fit(w(12, "never"), [[-25, -2, -7, -21, 11, 7]], -40, 4, 40, { b: 0.25 }),
      ],
      people: visitors.map((v, i): PersonSpec => ({ id: v.id, flip: i % 2 === 1, at: () => [v.x, -5.2, v.z], props: () => ({ costume: v.costume, seed: i * 5, pose: i % 2 ? "point" : "stand", face: i % 2 ? "smile" : "neutral" }) })),
      rigs: [shipRig(() => st, {})],
      avoid: () => [hullBox(st)] });
    setRoom(null);
  }

  const tags: Tag[] = [
    { text: "STOCKHOLM, 1628", at: w(1, "it's") + 0.1, out: w(1, "the", 1) - 0.4 },
    { text: "POLAND", at: w(1, "the", 1), out: w(1, "orders") - 0.25 },
    { text: "STOCKHOLM HARBOUR", at: w(4, "on") + 0.05, out: w(4, "four") - 0.2 },
    { text: "THE VASA MUSEUM", at: w(12, "sits"), out: T.total - 0.3 },
  ];
  // the roll gauge and the distance counter (progress toward the payoff)
  const testHeel = (t: number) => { const runs = RUNS(0, 1.05, 3); return heelFromRuns(runs, 0, 1.05, 0.07)(t); };
  const test2Heel = (t: number) => { const t0 = S(3); const runs = RUNS(t0 - 0.2, 0.95, 4); return heelFromRuns(runs, t0 - 0.2, 0.95, 0.11)(t); };
  const heel = (t: number): number | null => {
    if (t < w(0, "stopped") + 0.4) return testHeel(t);
    if (t >= S(3) && t < w(3, "the", 3)) return test2Heel(t);
    if (t >= gust1 - 0.4 && t < S(6)) return voyageHeel(t);
    return null;
  };
  const dist = (t: number): number | null => (t >= tSail && t < S(7) - 0.2 ? Math.min(1300, Math.max(0, (t - tSail) / (w(6, "sinks") - tSail)) * 1300) : null);
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
