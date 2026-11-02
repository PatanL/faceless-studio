// story-chess-turk v7: who is where, what moves and where the camera goes, for every beat (our own code).
// Word-anchored on the Kokoro timings (timing.ts). Places: the palace hall (several real angles, the board close-up
// and the gear bay are camera moves inside it), Schönbrunn's courtyard, a touring map, a Paris salon, the hall at
// night (1809), the museum fire (street and gallery), a night workshop for the explanation, the hall at night again.
import * as THREE from "three";
import type { GroupSpec, PersonSpec, V3 } from "./Stage";
import type { CamKey } from "./campath";
import { Timing } from "./timing";
import { exteriorSet, hallSet, salonSet, mapTableSet, museumSet, galleryInteriorSet, workshopSet, glowSprite, lambert } from "./sets";
import { parchment } from "./paint2";
import { Flame, Rising, ashHeap } from "./fx";
import { NOINK } from "../ink";
import { LAND } from "../../../../studio/src/kits/explainer/mapdata";

// ------------------------------------------------------------------------------------------------ small helpers
const clamp01 = (u: number) => Math.min(1, Math.max(0, u));
const sm = (u: number) => { u = clamp01(u); return u * u * (3 - 2 * u); };
/** eased ramp from v0 at t0 to v1 at t1 */
const ramp = (t: number, t0: number, t1: number, v0: number, v1: number) => v0 + (v1 - v0) * sm((t - t0) / Math.max(1e-6, t1 - t0));
/** piecewise eased track [[t, v], ...] */
const track = (t: number, keys: [number, number][]) => {
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 1; i < keys.length; i++) if (t < keys[i][0]) return ramp(t, keys[i - 1][0], keys[i][0], keys[i - 1][1], keys[i][1]);
  return keys[keys.length - 1][1];
};
/** discrete value held from each key time */
const step = <T,>(t: number, keys: [number, T][]): T => { let v = keys[0][1]; for (const [k, x] of keys) if (t >= k) v = x; return v; };
/** poses as a stick-kit track (the Person blends pose changes over 0.22 s itself): pass absolute times */
const poses = (keys: [number, string][]) => keys.map(([t, v]) => ({ t, v }));
const K = (t: number, pos: V3, look: V3, fov = 40): CamKey => ({ t, pos, look, fov });
/** move along keyframes [[t, x, z], ...] (eased), y = 0 */
const walk = (t: number, keys: [number, number, number][]): V3 => {
  if (t <= keys[0][0]) return [keys[0][1], 0, keys[0][2]];
  for (let i = 1; i < keys.length; i++) if (t < keys[i][0]) {
    const u = sm((t - keys[i - 1][0]) / (keys[i][0] - keys[i - 1][0]));
    return [keys[i - 1][1] + (keys[i][1] - keys[i - 1][1]) * u, 0, keys[i - 1][2] + (keys[i][2] - keys[i - 1][2]) * u];
  }
  const l = keys[keys.length - 1]; return [l[1], 0, l[2]];
};
const walking = (t: number, keys: [number, number, number][]) => {
  for (let i = 1; i < keys.length; i++) if (t >= keys[i - 1][0] && t < keys[i][0] && (keys[i][1] !== keys[i - 1][1] || keys[i][2] !== keys[i - 1][2])) return 1;
  return 0;
};

// ------------------------------------------------------------------------------------------------ framing
/** an axis-aligned box [x0, y0, z0, x1, y1, z1] (world metres) that a shot must hold */
export type Box = [number, number, number, number, number, number];
const personBox = (p: V3, seated = false, upper = false): Box =>
  [p[0] - 0.32, upper ? (seated ? 0.75 : 0.95) : 0, p[2] - 0.12, p[0] + 0.32, seated ? 1.45 : 1.7, p[2] + 0.12];
const cabBox = (c: V3, withTurk = true): Box => [c[0] - 0.62, 0, c[2] - 0.4, c[0] + 0.62, withTurk ? 1.9 : 0.95, c[2] + 0.4];
const boardBox = (c: V3): Box => [c[0] - 0.12, 0.9, c[2] - 0.26, c[0] + 0.44, 1.02, c[2] + 0.3];
const turkBox = (c: V3): Box => [c[0] - 0.4, 0.95, c[2] - 0.4, c[0] + 0.4, 1.9, c[2]];
const bayBox = (c: V3): Box => [c[0] - 0.6, 0.12, c[2] + 0.25, c[0] - 0.14, 0.92, c[2] + 0.42];
const rightBays = (c: V3): Box => [c[0] - 0.14, 0.12, c[2] + 0.25, c[0] + 0.6, 0.92, c[2] + 0.42];
const FIT_CAM = new THREE.PerspectiveCamera(40, 1080 / 1920, 0.05, 200);
type Pad = { x?: number; t?: number; b?: number };
const corners = (boxes: Box[]) => {
  const pts: THREE.Vector3[] = [];
  for (const b of boxes) for (const x of [b[0], b[3]]) for (const y of [b[1], b[4]]) for (const z of [b[2], b[5]]) pts.push(new THREE.Vector3(x, y, z));
  return pts;
};
function solve(boxes: Box[], az: number, el: number, fov: number, pad: Pad) {
  const px = pad.x ?? 0.12, pt = pad.t ?? 0.14, pb = pad.b ?? 0.3;
  const pts = corners(boxes);
  const bb = new THREE.Box3().setFromPoints(pts);
  const look = bb.getCenter(new THREE.Vector3());
  const a = (az * Math.PI) / 180, e = (el * Math.PI) / 180;
  const dir = new THREE.Vector3(Math.sin(a) * Math.cos(e), Math.sin(e), Math.cos(a) * Math.cos(e));
  let d = bb.getSize(new THREE.Vector3()).length() * 1.5 + 0.5;
  const cam = FIT_CAM; cam.fov = fov; cam.updateProjectionMatrix();
  const right = new THREE.Vector3(), up = new THREE.Vector3();
  for (let i = 0; i < 40; i++) {
    cam.position.copy(look).addScaledVector(dir, d); cam.lookAt(look); cam.updateMatrixWorld();
    let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity, behind = false;
    for (const p of pts) {
      const v = p.clone().applyMatrix4(cam.matrixWorldInverse);
      if (v.z > -0.1) { behind = true; break; }
      const q = p.clone().project(cam);
      x0 = Math.min(x0, q.x); x1 = Math.max(x1, q.x); y0 = Math.min(y0, q.y); y1 = Math.max(y1, q.y);
    }
    if (behind) { d *= 1.4; continue; }
    const tx0 = -1 + px, tx1 = 1 - px, ty0 = -1 + pb, ty1 = 1 - pt;
    const s = Math.max((x1 - x0) / (tx1 - tx0), (y1 - y0) / (ty1 - ty0));
    const halfH = d * Math.tan((fov * Math.PI) / 360), halfW = halfH * (1080 / 1920);
    right.setFromMatrixColumn(cam.matrixWorld, 0); up.setFromMatrixColumn(cam.matrixWorld, 1);
    look.addScaledVector(right, (((x0 + x1) / 2 - (tx0 + tx1) / 2) * halfW) * 0.8).addScaledVector(up, (((y0 + y1) / 2 - (ty0 + ty1) / 2) * halfH) * 0.8);
    d *= 1 + (s - 1) * 0.7;
  }
  cam.position.copy(look).addScaledVector(dir, d); cam.lookAt(look); cam.updateMatrixWorld();
  return { pos: cam.position.clone(), look };
}
/** fraction of a box's screen rectangle inside the frame for the last solved camera (0 when behind the lens) */
function inside(b: Box) {
  const cam = FIT_CAM;
  let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
  for (const p of corners([b])) {
    const v = p.clone().applyMatrix4(cam.matrixWorldInverse);
    if (v.z > -0.05) return 0.5;          // straddles the lens: treat as cut
    const q = p.clone().project(cam);
    x0 = Math.min(x0, q.x); x1 = Math.max(x1, q.x); y0 = Math.min(y0, q.y); y1 = Math.max(y1, q.y);
  }
  const ix = Math.max(0, Math.min(1, x1) - Math.max(-1, x0)), iy = Math.max(0, Math.min(1, y1) - Math.max(-1, y0));
  return (ix * iy) / Math.max(1e-6, (x1 - x0) * (y1 - y0));
}
/** a checked framing: the camera looks along (az, el) degrees (az 0 = from the front, +z; az 90 = from +x; el > 0 =
 * from above) and stands where every box fits inside the 9:16 frame with the given margins (NDC units; the bottom
 * margin keeps the subjects above the caption band). others: the other figures in the place - a figure that would be
 * cut by the frame edge is taken into the shot when it is mostly in, and the angle is nudged when only a sliver of it
 * shows, so no held framing cuts a figure */
/** the room the camera must stay inside for the fits that follow (null = open air) */
let ROOM: Box | null = null;
const inRoom = (p: THREE.Vector3) => !ROOM || (p.x > ROOM[0] && p.y > ROOM[1] && p.z > ROOM[2] && p.x < ROOM[3] && p.y < ROOM[4] && p.z < ROOM[5]);
function fit(t: number, boxes: Box[], az: number, el: number, fov = 40, pad: Pad = {}, others: Box[] = []): CamKey {
  // inside a room: widen the lens, then swing toward the front, until the camera stands inside it
  for (const [dz, df] of [[0, 0], [0, 8], [0, 16], [Math.sign(az) * -15, 8], [Math.sign(az) * -30, 8], [Math.sign(az) * -45, 8]]) {
    const k = fitFree(t, boxes, az + dz, el, fov + df, pad, others);
    if (inRoom(new THREE.Vector3(...k.pos))) return k;
  }
  return fitFree(t, boxes, 0, el, fov + 16, pad, others);
}
function fitFree(t: number, boxes: Box[], az: number, el: number, fov = 40, pad: Pad = {}, others: Box[] = []): CamKey {
  let subj = [...boxes];
  let best: { pos: THREE.Vector3; look: THREE.Vector3; bad: number } | null = null;
  for (const daz of [0, 6, -6, 12, -12, 18, -18]) {
    subj = [...boxes];
    let r = solve(subj, az + daz, el, fov, pad);
    for (let k = 0; k < 4; k++) {
      const grow = others.filter((b) => { const f = inside(b); return f > 0.3 && f < 0.995 && !subj.includes(b); });
      if (!grow.length) break;
      subj.push(...grow); r = solve(subj, az + daz, el, fov, pad);
    }
    const bad = others.filter((b) => !subj.includes(b)).reduce((n, b) => { const f = inside(b); return n + (f > 0.002 && f < 0.995 ? 1 : 0); }, 0);
    if (!best || bad < best.bad) best = { ...r, bad };
    if (bad === 0) break;
  }
  const { pos, look } = best!;
  return { t, pos: [pos.x, pos.y, pos.z], look: [look.x, look.y, look.z], fov };
}
/** shift a box by a cabinet position */
const at = (c: V3, b: Box): Box => [b[0] + c[0], b[1] + c[1], b[2] + c[2], b[3] + c[0], b[4] + c[1], b[5] + c[2]];
void at;

/** a 3D text tag (lantern-tag look: dark pill, cream Anton text) that lives in the world (moves with the camera) */
export function tagSprite(text: string, h = 0.07) {
  const c = document.createElement("canvas");
  const g = c.getContext("2d")!;
  g.font = '64px "Anton", Impact, sans-serif';
  const w = Math.ceil(g.measureText(text).width) + 90;
  c.width = w; c.height = 110;
  g.fillStyle = "rgba(27, 18, 64, 0.92)"; g.beginPath(); g.roundRect(4, 4, w - 8, 102, 51); g.fill();
  g.strokeStyle = "#f2d8a0"; g.lineWidth = 5; g.stroke();
  g.fillStyle = "#fff2c0"; g.font = '64px "Anton", Impact, sans-serif'; g.textBaseline = "middle"; g.textAlign = "center";
  (g as CanvasRenderingContext2D & { letterSpacing?: string }).letterSpacing = "3px";
  g.fillText(text, w / 2, 58);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: t, depthTest: false, fog: false, transparent: true }));
  s.scale.set(h * (w / 110), h, 1); s.layers.set(NOINK); s.renderOrder = 10;
  return s;
}
/** a candle standing on a surface: wax, brass dish, flame + glow; visible() decides when it is there */
function candleProp(root: THREE.Object3D) {
  const g = new THREE.Group();
  const dish = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.05, 0.012, 16), lambert({ color: "#d9a43a" })); dish.position.y = 0.006;
  const wax = new THREE.Mesh(new THREE.CylinderGeometry(0.016, 0.016, 0.12, 12), lambert({ color: "#f4eee1" })); wax.position.y = 0.072;
  const flame = new THREE.Mesh(new THREE.SphereGeometry(0.012, 10, 8), new THREE.MeshBasicMaterial({ color: "#ffcf6a", fog: false }));
  flame.scale.set(1, 1.8, 1); flame.position.y = 0.15; flame.layers.set(NOINK);
  for (const m of [dish, wax]) { m.castShadow = true; m.receiveShadow = true; }
  g.add(dish, wax, flame);
  glowSprite(g, [255, 196, 120], 0.35, 0, 0.16, 0);
  root.add(g);
  return g;
}

// ------------------------------------------------------------------------------------------------ the story
export function buildStory(T: Timing): { groups: GroupSpec[]; tags: Tag[]; paperAt: number; paperOut: number; headlineOut: number } {
  const w = T.w.bind(T), S = T.S.bind(T);
  const groups: GroupSpec[] = [];
  const CAB: V3 = [0, 0, -6];
  const cabAt = () => CAB;
  // the player's chair (the count, then Napoleon) at the cabinet's right, reaching the board
  const CHAIR: V3 = [1.0, 0, -5.95];
  // the inventor's marks: beside the left door, in front of the left bay (reaching the right doors), at the left side
  const KL: V3 = [-1.0, 0, -5.42], KR: V3 = [-0.33, 0, -5.28], KS: V3 = [-1.05, 0, -6.05];
  const COURT = { empress: [2.3, 0, -7.6] as V3, courtier: [3.05, 0, -6.9] as V3, courtier2: [-2.1, 0, -7.7] as V3 };

  // ---------------- people of the hall (the same people in the same places in every hall beat)
  const count = (withScene5: boolean): PersonSpec => ({
    id: "count", flip: true, at: () => CHAIR,
    props: (t) => ({ costume: "count", seated: true, seed: 13, pose: "reach",
      face: step(t, [[0, "smug"], [w(0, "player"), "shock"], [w(0, "game"), "frown"],
        ...(withScene5 ? [[w(5, "brave"), "worried"] as [number, string], [w(5, "crushed"), "shock"] as [number, string]] : [])]) }),
  });
  const court = (laughAt: number | null, quietAt: number | null, shockAt: number | null): PersonSpec[] => {
    const face = (t: number) => step(t, [[0, "smug"], ...(laughAt !== null ? [[laughAt, "laugh"] as [number, string]] : []),
      ...(quietAt !== null ? [[quietAt, "smug"] as [number, string]] : []), ...(shockAt !== null ? [[shockAt, "shock"] as [number, string]] : [])]);
    const pose = (t: number, rest: string) => (laughAt !== null && t >= laughAt && (quietAt === null || t < quietAt) ? "laugh" : rest);
    return [
      { id: "empress", flip: true, at: () => COURT.empress, props: (t) => ({ costume: "empress", seed: 4, face: face(t), pose: pose(t, "hips") }) },
      { id: "courtier2", at: () => COURT.courtier2, props: (t) => ({ costume: "courtier2", seed: 12, face: face(t), pose: pose(t, "stand") }) },
      { id: "courtier", flip: true, at: () => COURT.courtier, props: (t) => ({ costume: "courtier", seed: 11, face: face(t), pose: pose(t, "point") }) },
    ];
  };
  const everyone = (k: V3): Box[] => [cabBox(CAB), personBox(CHAIR, true), personBox(COURT.empress), personBox(COURT.courtier),
    personBox(COURT.courtier2), personBox(k)];

  const hallOthers = (t: number, k: (t: number) => V3): Box[] => [personBox(CHAIR, true), personBox(COURT.empress), personBox(COURT.courtier),
    personBox(COURT.courtier2), personBox(k(t))];

  const HALL: Box = [-5.6, 0.2, -19.6, 5.6, 6, 7.6];
  // ================= G1 hook: the hall, the robot beats a player, he opens the left door
  {
    ROOM = HALL;
    const t0 = 0, t1 = S(1);
    const opened = w(0, "opened");
    groups.push({
      id: "hook", t0, t1, xfade: 0, set: () => hallSet(false), light: "day",
      cam: [
        fit(0, [cabBox(CAB), personBox(CHAIR, true)], 18, 10, 40, {}, hallOthers(0, () => KL)),                       // the robot and its opponent
        fit(w(0, "beat") - 0.15, [boardBox(CAB)], 30, 42, 38, { b: 0.4 }, hallOthers(w(0, "beat") - 0.15, () => KL)),               // the board: the robot wins
        fit(w(0, "and"), everyone(KL), 8, 14, 42, {}, hallOthers(w(0, "and"), () => KL)),                                         // the whole court
        fit(opened, [personBox(KL), cabBox(CAB, false)], -18, 6, 40, {}, hallOthers(opened, () => KL)),                     // he opens the left door
        fit(w(0, "empty"), [bayBox(CAB)], 6, 4, 36, { x: 0.18, b: 0.42, t: 0.25 }, hallOthers(w(0, "empty"), () => KL)),        // empty: gears only
      ],
      cabinet: {
        at: cabAt,
        state: (t) => ({ t, doorL: ramp(t, opened + 0.1, opened + 0.6, 0, 1), bayGlow: ramp(t, w(0, "prove"), w(0, "prove") + 0.4, 0, 0.8), spin: t * 0.6 }),
        chess: () => ({ moves: [{ t: w(0, "beat") - 0.1, from: "d8", to: "e2", hand: "turk", dur: 0.45 }],
          topple: { t: w(0, "beat") + 0.38, sq: "e1" }, glow: { t: w(0, "beat") + 0.38, sq: "e1" } }),
        turk: (t) => ({ arm: track(t, [[0, 0.6], [w(0, "beat") - 0.3, 1]]), reach: track(t, [[0, 0.3], [w(0, "beat") - 0.3, 0.8], [w(0, "and"), 0.4]]), look: 0.6 }),
      },
      people: [
        { id: "kempelen", at: () => KL,
          props: () => ({ costume: "kempelen", seed: 2, face: [{ t: 0, v: "smug" }, { t: w(0, "empty"), v: "grin" }],
            pose: poses([[0, "point"], [opened - 0.15, "reach"]]) }) },
        count(false),
        ...court(null, null, null),
      ],
    });
  }

  // ================= G2 Schönbrunn courtyard: he rolls the cabinet up to the palace
  {
    ROOM = null;
    const t0 = S(1), t1 = w(1, "empress's");
    const arrive = w(1, "cabinet", 1, 0, true);
    const roll = (t: number): V3 => walk(t, [[t0, 3.4, -0.6], [arrive, 0.6, -6.2]]);
    const kemp = (t: number): V3 => { const [x, , z] = roll(t); return [x + 0.95, 0, z + 0.35]; };
    const both = (t: number): Box[] => [cabBox(roll(t)), personBox(kemp(t))];
    groups.push({
      id: "courtyard", t0, t1, xfade: 0.233, set: exteriorSet, light: "day",
      cam: [
        fit(t0, [...both(t0), [-4, 0, -19, 4, 7.5, -18]], 20, 6, 42, { b: 0.2 }, [personBox(kemp(t0))]),          // the palace, the cabinet arriving
        fit(w(1, "inventor"), both(w(1, "inventor")), 35, 8, 40, {}, [personBox(kemp(w(1, "inventor")))]),                          // the inventor pushing it
        fit((w(1, "inventor") + arrive) / 2, both((w(1, "inventor") + arrive) / 2), 50, 8, 40, {}, [personBox(kemp((w(1, "inventor") + arrive) / 2))]),
        fit(arrive, both(arrive), 40, 8, 40, {}, [personBox(kemp(arrive))]),
        fit(t1, [...both(t1), [-3, 2, -19, 3, 8, -18]], 25, 4, 44, { b: 0.15 }, [personBox(kemp(t1))]),           // up at the palace
      ],
      cabinet: { at: roll, rotY: 0.35, state: (t) => ({ t, spin: 0 }), chess: () => ({ moves: [] }), turk: () => ({ look: 0.4 }) },
      people: [{ id: "kempelen", flip: true, at: kemp,
        props: (t) => ({ costume: "kempelen", seed: 2, face: "smile", pose: "push", walk: t < arrive ? 1 : 0 }) }],
    });
  }

  // ================= G3 the hall from many angles: the court, the doors, the gears, the key, the count's game
  {
    ROOM = HALL;
    const t0 = w(1, "empress's"), t1 = S(6);
    const opens = w(3, "opens"), one = w(3, "one"), one2 = w(3, "one", 2), and3 = w(3, "and"), candleW = w(3, "candle"), behind = w(3, "behind");
    const s4 = S(4), winds = w(4, "winds"), lifts = w(4, "lifts");
    // the inventor: at the left door, in front of the left bay for the right doors, back beside the left bay with the
    // candle, then round to the cabinet's left side to wind the key
    const nothing = w(3, "nothing"), down = nothing + 0.15;
    const kk: [number, number, number][] = [[t0, KL[0], KL[2]], [opens + 0.35, KL[0], KL[2]], [one - 0.1, KR[0], KR[2]],
      [and3 - 0.05, KR[0], KR[2]], [candleW - 0.32, KL[0], KL[2]], [down + 0.1, KL[0], KL[2]], [winds - 0.12, KS[0], KS[2]], [t1, KS[0], KS[2]]];
    const kAt = (t: number) => walk(t, kk);
    const laugh = w(2, "laughs") - 0.25, quiet = S(3) + 0.6, shock = w(5, "no") - 0.1;
    groups.push({
      id: "hall", t0, t1, xfade: 0.233, set: () => hallSet(false), light: "day",
      cam: [
        fit(t0, [...everyone(kAt(t0)), [-2, 0.5, -18.5, 2, 3.2, -17.5]], 12, 12, 44, { b: 0.2 }, hallOthers(t0, kAt)),   // the hall: throne, court, cabinet
        fit(w(2, "wooden"), [turkBox(CAB)], 12, -10, 38, {}, hallOthers(w(2, "wooden"), kAt)),                                // low on the wooden man
        fit(w(2, "staring"), [boardBox(CAB), [-0.3, 1.3, -6.3, 0.3, 1.85, -6.0]], 28, 34, 38, { b: 0.35 }, hallOthers(w(2, "staring"), kAt)),   // his stare down at the board
        fit(w(2, "whole"), [personBox(COURT.empress), personBox(COURT.courtier), personBox(CHAIR, true)], 34, 8, 40, {}, hallOthers(w(2, "whole"), kAt)),   // the court laughing
        fit(opens, [personBox(kAt(opens)), cabBox(CAB, false)], 18, 6, 40, {}, hallOthers(opens, kAt)),              // the left door
        fit(one, [personBox(kAt(one)), cabBox(CAB, false)], 34, 6, 40, {}, hallOthers(one, kAt)),                  // the right doors, one by one
        fit(candleW, [personBox(kAt(candleW), false, true), bayBox(CAB)], 22, 6, 38, {}, hallOthers(candleW, kAt)),    // the candle into the left bay
        fit(w(3, "nothing"), [bayBox(CAB)], 24, 4, 34, { x: 0.18, b: 0.42, t: 0.25 }, hallOthers(w(3, "nothing"), kAt)),   // nothing but gears
        fit(winds, [personBox(KS), cabBox(CAB)], -58, 8, 40, {}, hallOthers(winds, kAt)),                            // he winds the key at the side
        fit(w(4, "gears"), [bayBox(CAB)], -12, 4, 34, { x: 0.18, b: 0.42, t: 0.25 }, hallOthers(w(4, "gears"), kAt)),    // the gears ticking
        fit(lifts, [turkBox(CAB)], 22, -12, 40, {}, hallOthers(lifts, kAt)),                                          // low: the arm lifts
        fit(w(5, "count"), [personBox(CHAIR, true), boardBox(CAB)], 58, 12, 40, {}, hallOthers(w(5, "count"), kAt)),          // the count sits down to play
        fit(w(5, "play"), [boardBox(CAB)], 32, 44, 38, { b: 0.4 }, hallOthers(w(5, "play"), kAt)),                       // the board: crushed
        fit(w(5, "no"), [personBox(COURT.empress), personBox(COURT.courtier), personBox(CHAIR, true)], 30, 8, 40, {}, hallOthers(w(5, "no"), kAt)),   // nobody laughs
      ],
      cabinet: {
        at: cabAt,
        state: (t) => ({ t,
          doorL: ramp(t, opens + 0.12, opens + 0.6, 0, 1), doorR: ramp(t, one + 0.12, one + 0.55, 0, 1), doorR2: ramp(t, one2 + 0.12, one2 + 0.55, 0, 1),
          bayGlow: track(t, [[candleW, 0], [behind, 1], [down, 1], [down + 0.5, 0.35]]),
          spin: t < winds ? 0 : (t - winds) * 2.2 }),
        chess: () => ({ moves: [{ t: w(5, "play"), from: "d8", to: "e2", hand: "turk", dur: 0.5 }],
          topple: { t: w(5, "crushed"), sq: "e1" }, glow: { t: w(5, "crushed"), sq: "e1" } }),
        turk: (t) => ({ look: track(t, [[0, 0.8], [w(2, "staring"), 0.9]]),
          arm: track(t, [[0, 0], [w(2, "wooden"), 0.2], [lifts, 0.2], [lifts + 0.7, 1]]),
          reach: track(t, [[0, 0], [w(2, "wooden"), 0.3], [s4, 0], [w(5, "enough"), 0], [w(5, "play"), 0.6]]) }),
      },
      people: [
        { id: "kempelen", at: kAt,
          props: (t) => ({ costume: "kempelen", seed: 2,
            face: step(t, [[0, "grin"], [w(2, "wooden"), "smug"], [winds, "focus"], [w(5, "no"), "smug"]]),
            pose: poses([[0, "point"], [opens - 0.15, "reach"], [opens + 0.3, "stand"], [one - 0.1, "reach"], [and3, "stand"],
              [candleW - 0.32, "holdHigh"], [behind, "reach"], [down, "stand"], [winds - 0.1, "wind"], [S(5) + 0.3, "stand"]]),
            item: step(t, [[0, "none"], [candleW, "candle"], [down, "none"], [winds - 0.1, "key"], [S(5) + 0.3, "none"]]),
            walk: walking(t, kk) }) },
        count(true),
        ...court(laugh, quiet, shock),
      ],
      extras: (ctx) => {
        // the candle stands on the cabinet top until he takes it, and again after he sets it down
        const cp = candleProp(ctx.root); cp.position.set(-0.45, 0.9, -5.72);
        return (t) => { cp.visible = t < candleW || t >= down; };
      },
    });
  }

  // ================= G4 the touring map: Vienna, Paris, London, then across the Atlantic to New York
  {
    ROOM = null;
    const t0 = S(6), t1 = w(6, "it");
    // name, lon, lat, label offset on the map (m): every label sits on its own side of its pin, clear of the others
    const cities: [string, number, number, number, number][] = [
      ["VIENNA", 16.37, 48.21, 0.05, 0.1], ["PARIS", 2.35, 48.86, -0.2, 0.06], ["LONDON", -0.13, 51.5, -0.12, -0.09],
      ["NEW YORK", -74.0, 40.7, 0.26, 0.06]];
    const arrive = [t0 + 0.1, w(6, "europe") - 0.2, w(6, "europe") + 0.25, w(6, "america")];
    const LON0 = -88, LON1 = 24, LAT0 = 19, LAT1 = 64, MW = 3.4, MH = 2.4;
    const merc = (lat: number) => Math.log(Math.tan(Math.PI / 4 + (lat * Math.PI) / 360));
    const toMap = (lon: number, lat: number): [number, number] => [((lon - LON0) / (LON1 - LON0) - 0.5) * MW,
      (0.5 - (merc(lat) - merc(LAT0)) / (merc(LAT1) - merc(LAT0))) * MH];
    const mapCanvas = () => {
      const c = parchment();
      const g = c.getContext("2d")!;
      const px = (lon: number, lat: number): [number, number] => { const [x, z] = toMap(lon, lat); return [(x / MW + 0.5) * 1024, (z / MH + 0.5) * 1024]; };
      g.fillStyle = "rgba(70, 130, 160, 0.42)"; g.fillRect(0, 0, 1024, 1024);
      g.strokeStyle = "rgba(40, 70, 100, 0.25)"; g.lineWidth = 1.5;
      for (let lo = -80; lo <= 20; lo += 20) { const [a] = px(lo, LAT0); g.beginPath(); g.moveTo(a, 0); g.lineTo(a, 1024); g.stroke(); }
      for (let la = 25; la <= 60; la += 10) { const [, b] = px(0, la); g.beginPath(); g.moveTo(0, b); g.lineTo(1024, b); g.stroke(); }
      for (const rings of Object.values(LAND)) for (const ring of rings) {
        g.beginPath(); ring.forEach(([lo, la], i) => { const [x, y] = px(lo, la); if (i) g.lineTo(x, y); else g.moveTo(x, y); }); g.closePath();
        g.fillStyle = "#ead7a0"; g.fill(); g.strokeStyle = "#4a3320"; g.lineWidth = 3; g.stroke();
      }
      return c;
    };
    const pts = cities.map(([, lo, la]) => toMap(lo, la));
    const area = (i0: number, i1: number): Box => {
      const xs = pts.slice(i0, i1 + 1).map((p, k) => [p[0], p[0] + cities[i0 + k][3] * 1.6]).flat();
      const zs = pts.slice(i0, i1 + 1).map((p, k) => [p[1], p[1] + cities[i0 + k][4] * 1.6]).flat();
      return [Math.min(...xs) - 0.08, 0.8, Math.min(...zs) - 0.08, Math.max(...xs) + 0.08, 0.9, Math.max(...zs) + 0.08];
    };
    groups.push({
      id: "map", t0, t1, xfade: 0.233, set: () => mapTableSet(mapCanvas()), light: "golden",
      cam: [
        fit(t0, [area(0, 1)], 0, 58, 40, { b: 0.25 }),
        fit(w(6, "europe"), [area(0, 2)], 0, 58, 40, { b: 0.25 }),
        fit(w(6, "america"), [area(3, 3)], 0, 60, 40, { b: 0.25 }),
      ],
      people: [],
      extras: (ctx) => {
        // the route: dots appear as the token passes; the Atlantic leg is an arc
        const legs: THREE.Vector3[][] = [];
        for (let i = 1; i < pts.length; i++) {
          const a = new THREE.Vector3(pts[i - 1][0], 0.81, pts[i - 1][1]), b = new THREE.Vector3(pts[i][0], 0.81, pts[i][1]);
          const mid = a.clone().lerp(b, 0.5); if (i === 3) mid.z -= 0.25;
          const curve = new THREE.QuadraticBezierCurve3(a, mid, b);
          legs.push(curve.getPoints(Math.max(6, Math.round(a.distanceTo(b) / 0.04))));
        }
        const dotMat = new THREE.MeshBasicMaterial({ color: "#8c2a1e", fog: false });
        const dots: { m: THREE.Mesh; t: number }[] = [];
        legs.forEach((leg, i) => leg.forEach((p, j) => {
          if (j % 2) return;
          const m = new THREE.Mesh(new THREE.CircleGeometry(0.012, 10), dotMat); m.rotation.x = -Math.PI / 2; m.position.copy(p).setY(0.8115);
          m.layers.set(NOINK); ctx.root.add(m); dots.push({ m, t: arrive[i] + (arrive[i + 1] - arrive[i]) * (j / leg.length) });
        }));
        const pin = (x: number, z: number) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(0.022, 0.022, 0.014, 14), lambert({ color: "#c0392b" })); m.position.set(x, 0.816, z); m.castShadow = true; ctx.root.add(m); return m; };
        const pins = pts.map(([x, z]) => pin(x, z));
        const labels = cities.map(([name, , , dx, dz], i) => { const s = tagSprite(name, 0.085); s.position.set(pts[i][0] + dx, 0.84, pts[i][1] + dz); ctx.root.add(s); return s; });
        // the touring token: a little cabinet with a turban
        const token = new THREE.Group();
        const tb = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.05, 0.05), lambert({ color: "#b47a3a" })); tb.position.y = 0.025;
        const tt = new THREE.Mesh(new THREE.SphereGeometry(0.022, 12, 10), lambert({ color: "#f4eee1" })); tt.position.set(-0.015, 0.075, -0.01);
        for (const m of [tb, tt]) { m.castShadow = true; token.add(m); }
        ctx.root.add(token);
        return (t) => {
          dots.forEach((d) => (d.m.visible = t >= d.t));
          pins.forEach((p, i) => { p.visible = t >= arrive[i] - 0.05; p.scale.setScalar(Math.max(0.001, sm((t - arrive[i] + 0.05) / 0.2))); });
          labels.forEach((s, i) => { (s.material as THREE.SpriteMaterial).opacity = sm((t - arrive[i]) / 0.25); s.visible = t >= arrive[i]; });
          let li = 0; while (li < arrive.length - 2 && t >= arrive[li + 1]) li++;
          const u = clamp01((t - arrive[li]) / (arrive[li + 1] - arrive[li]));
          const leg = legs[Math.min(li, legs.length - 1)];
          const p = leg[Math.min(leg.length - 1, Math.round(u * (leg.length - 1)))];
          token.position.set(p.x, 0.8115, p.z);
        };
      },
    });
  }

  // ================= G5 Paris, 1783: Benjamin Franklin
  {
    const t0 = w(6, "it"), t1 = S(7);
    const PC: V3 = [-0.35, 0, -3.9], FR: V3 = [0.65, 0, -3.85];
    groups.push({
      id: "paris", t0, t1, xfade: 0.233, set: salonSet, light: "golden",
      cam: [
        fit(t0, [cabBox(PC), personBox(FR, true)], 16, 10, 40, {}, [personBox(FR, true)]),                           // the Turk and Franklin at the board
        fit(w(6, "franklin"), [personBox(FR, true, true), boardBox(PC)], -24, 14, 38, {}, [personBox(FR, true)]),    // Franklin loses
      ],
      cabinet: { at: () => PC, state: (t) => ({ t }), chess: () => ({ moves: [], topple: { t: w(6, "beats") + 0.2, sq: "e1" } }),
        turk: (t) => ({ arm: 1, reach: track(t, [[0, 0.2], [w(6, "beats"), 1]]), look: 0.8 }) },
      people: [{ id: "franklin", flip: true, at: () => FR,
        props: (t) => ({ costume: "franklin", seated: true, seed: 21, pose: "reach", face: step(t, [[0, "focus"], [w(6, "franklin"), "shock"]]) }) }],
    });
  }

  // ================= G6 Vienna 1809 at night: Napoleon cheats, the robot puts it back, then sweeps the board
  {
    ROOM = HALL;
    const t0 = S(7), t1 = S(8);
    const tries = w(7, "tries"), third = w(7, "third"), sweeps = w(7, "sweeps");
    groups.push({
      id: "napoleon", t0, t1, xfade: 0.233, set: () => hallSet(true), light: "night",
      cam: [
        fit(t0, [cabBox(CAB), personBox(CHAIR, true)], 24, 10, 40, {}, [personBox(CHAIR, true)]),                       // the Turk and Napoleon
        fit(tries, [boardBox(CAB)], 32, 44, 38, { b: 0.4 }, [personBox(CHAIR, true)]),                              // he cheats; it puts the piece back
        fit(w(7, "twice"), [boardBox(CAB)], 6, 50, 38, { b: 0.4 }, [personBox(CHAIR, true)]),
        fit(third, [personBox(CHAIR, true, true), turkBox(CAB)], 40, 6, 40, {}, [personBox(CHAIR, true)]),              // the third time
        fit(sweeps, [cabBox(CAB), personBox(CHAIR, true)], 26, 12, 40, {}, [personBox(CHAIR, true)]),                   // the sweep
        fit(w(7, "board"), [cabBox(CAB, false), personBox(CHAIR, true), [0.6, 0, -6.3, 1.9, 0.3, -5.0]], 40, 14, 40, {}, [personBox(CHAIR, true)]),   // pieces on the floor
      ],
      cabinet: {
        at: cabAt, setup: "napoleon",
        state: (t) => ({ t }),
        chess: () => ({ moves: [
          { t: tries + 0.06, from: "d1", to: "f5", hand: "human", dur: 0.4, illegal: true },
          { t: tries + 1.06, from: "f5", to: "d1", hand: "turk", dur: 0.4 },
          { t: tries + 2.06, from: "d1", to: "f5", hand: "human", dur: 0.4, illegal: true },
          { t: tries + 3.06, from: "f5", to: "d1", hand: "turk", dur: 0.4 }], sweepAt: sweeps }),
        turk: (t) => ({ look: 0.8, sweep: t >= sweeps ? [{ t: sweeps, v: 1 }] : [], arm: t >= third ? 0 : 0.3, reach: 0.4 }),
      },
      people: [{ id: "napoleon", flip: true, at: () => CHAIR,
        props: (t) => ({ costume: "napoleon", seated: true, seed: 31, pose: t < third ? "handIn" : "reach",
          face: step(t, [[0, "smug"], [tries, "smug"], [w(7, "twice"), "angry"], [sweeps + 0.25, "shock"]]) }) }],
    });
  }

  // ================= G7 Philadelphia 1854: the museum burns
  {
    const t0 = S(8), t1 = w(8, "turk");
    const fireT = w(8, "fire");
    groups.push({
      id: "museum", t0, t1, xfade: 0, set: museumSet, light: "fire",
      cam: [K(t0, [3.2, 2.0, 9.0], [0.0, 5.0, -9.0], 44), K(fireT, [2.0, 2.8, 4.5], [0.0, 6.2, -9.0], 42)],
      people: [],
      extras: (ctx) => {
        const flames: { f: Flame; d: number }[] = [];
        [[-6, 9.8], [-3, 10.2], [0, 11.8], [3, 10.2], [6, 9.8], [-6, 4.7], [0, 4.7], [3, 4.7], [-3, 1.3], [3, 1.3], [6, 1.3]].forEach(([x, y], i) => {
          const f = new Flame(3.2 + (i % 3) * 0.8, i); f.mesh.position.set(x, y, -7.7); ctx.root.add(f.mesh); flames.push({ f, d: i * 0.07 });
        });
        const smoke = new Rising(14, "smoke", 2.4, 3); smoke.group.position.set(0, 10, -9); ctx.root.add(smoke.group);
        const embers = new Rising(40, "ember", 0.12, 4); embers.group.position.set(0, 4, -8); ctx.root.add(embers.group);
        const wins = Object.values(ctx.set.extra) as THREE.Mesh[];
        return (t, cam) => {
          const grow = (k: number) => ramp(t, fireT - 0.5 + k, fireT + 0.2 + k, 0.45, 1);
          flames.forEach(({ f, d }) => f.update(t, grow(d), cam));
          smoke.update(t, grow(0.2), 9, 3.2, 10); embers.update(t, grow(0.1), 8, 2.0, 12);
          wins.forEach((m, i) => (m.material as THREE.MeshBasicMaterial).color.set("#232846").lerp(new THREE.Color("#ff9a3a"), grow(0.06 * (i % 5))));
        };
      },
    });
  }

  // ================= G8 the gallery: the Turk burns to ash
  {
    const t0 = w(8, "turk"), t1 = S(9);
    const ash = w(8, "ash");
    groups.push({
      id: "gallery", t0, t1, xfade: 0.233, set: galleryInteriorSet, light: "fire",
      cam: [K(t0, [1.3, 1.45, -0.9], [0.0, 1.25, -4.2], 40), K(ash, [0.9, 1.25, -1.6], [0.0, 1.0, -4.0], 40)],
      cabinet: { at: () => [0, 0, -4], state: (t) => ({ t, char: ramp(t, t0, ash + 0.6, 0.2, 1) }), chess: () => ({ moves: [] }),
        turk: () => ({ look: 0.2 }), turkChar: (t) => ramp(t, t0, ash, 0.15, 0.85), turkBurn: (t) => ramp(t, ash - 0.15, w(8, "secret"), 0, 1) },
      people: [],
      extras: (ctx) => {
        const flames: Flame[] = [];
        [[-0.78, -3.75, 0], [0.8, -3.8, 0], [-0.5, -4.45, 0.9], [0.55, -4.4, 0.9], [-1.25, -4.6, 0], [1.3, -4.3, 0]].forEach(([x, z, y], i) => {
          const f = new Flame(1.2 + (i % 3) * 0.3, i + 3); f.mesh.position.set(x, y, z); ctx.root.add(f.mesh); flames.push(f);
        });
        const embers = new Rising(30, "ember", 0.06, 7); embers.group.position.set(0, 0.6, -4); ctx.root.add(embers.group);
        const heap = ashHeap(); heap.position.set(0, 0, -4.05); ctx.root.add(heap);
        glowSprite(ctx.root, [255, 140, 60], 5.0, 0, 1.2, -4.6);
        return (t, cam) => {
          flames.forEach((f, i) => f.update(t, ramp(t, t0 - 0.2, t0 + 0.5 + i * 0.05, 0.4, 1) * ramp(t, w(8, "secret"), t1, 1, 0.5), cam));
          embers.update(t, 1, 2.5, 1.8, 2.5);
          const hk = ramp(t, ash, w(8, "secret") + 0.3, 0.001, 1); heap.scale.set(hk, hk, hk); heap.visible = hk > 0.01;
        };
      },
    });
  }

  // ================= G9 the explanation: a night workshop, the cabinet opened up
  {
    const t0 = S(9), t1 = S(12);
    const man = w(9, "man"), door10 = w(10, "door"), opened10 = w(10, "opened"), slid = w(10, "slid"), side = w(10, "side", 1, 0, true), behindW = w(10, "behind");
    const magnetsW = w(11, "magnets"), boardW = w(11, "board"), lever = w(11, "lever"), moved = w(11, "moved"), handW = w(11, "hand"), candle11 = w(11, "candle"), smokeW = w(11, "smoke");
    groups.push({
      id: "explain", t0, t1, xfade: 0, set: workshopSet, light: "explain",
      cam: [
        K(t0, [0.35, 1.25, 0.9], [0.0, 0.85, -2.5], 42),
        K(w(9, "inside"), [0.5, 0.92, -0.95], [0.22, 0.6, -2.5], 38),
        K(w(10, "cabinet"), [-0.15, 1.05, -0.5], [-0.05, 0.72, -2.5], 40),
        K(w(10, "when"), [0.35, 0.9, -1.05], [0.05, 0.6, -2.5], 38),
        K(slid, [-0.05, 0.86, -1.15], [-0.08, 0.6, -2.5], 38),
        K(behindW, [-0.6, 0.82, -1.25], [-0.37, 0.6, -2.6], 38),
        K(magnetsW, [0.24, 0.62, -1.82], [0.14, 0.83, -2.48], 48),             // up under the board: the magnets
        K(w(11, "every"), [0.55, 0.95, -1.2], [0.2, 0.7, -2.5], 38),
        K(lever, [0.95, 1.38, -0.55], [0.0, 1.0, -2.6], 42),
        K(candle11, [0.25, 1.5, -0.45], [-0.08, 1.2, -2.6], 40),
        K(smokeW, [-0.1, 2.05, -0.85], [-0.27, 1.85, -2.7], 38),
      ],
      cabinet: {
        at: () => [0, 0, -2.5],
        state: (t) => ({ t, cut: 1, master: true,
          doorL: track(t, [[door10, 0], [opened10 + 0.2, 1], [slid - 0.2, 1], [slid + 0.15, 0]]),
          doorR: track(t, [[side, 0], [behindW + 0.2, 1]]), doorR2: track(t, [[side, 0], [behindW + 0.2, 1]]),
          seat: track(t, [[slid, 1], [side, 0], [magnetsW + 0.15, 0], [boardW, 1]]),
          masterCandle: ramp(t, man - 0.05, man + 0.3, 0.15, 1),
          lever: ramp(t, lever - 0.1, lever + 0.4, 0, 1),
          magnets: [{ t: boardW, i: 2 }, { t: w(11, "showed"), i: 5 }, { t: w(11, "every"), i: 3 }, { t: w(11, "move"), i: 6 }],
          spin: 0 }),
        chess: () => ({ moves: [] }),
        turk: (t) => ({ look: 0.5, arm: track(t, [[moved, 0], [handW, 1]]), reach: track(t, [[moved, 0], [handW, 0.6]]),
          smoke: track(t, [[candle11, 0], [smokeW, 1]]) }),
        master: (t) => ({ costume: "master", seated: true, crouch: 1, seed: 7, item: "candle",
          pose: poses([[0, "holdHigh"], [lever - 0.2, "hold"], [candle11, "holdHigh"]]),
          face: step(t, [[0, "shock"], [w(10, "master"), "focus"], [opened10, "worried"], [behindW, "smug"], [magnetsW, "focus"], [candle11, "smug"]]) }),
        masterDark: (t) => ramp(t, man - 0.05, man + 0.3, 0.92, 0),
      },
      people: [],
      extras: (ctx) => {
        const cab = ctx.cabinet!;
        const fp = tagSprite("FALSE PANEL", 0.085); fp.position.set(-0.37, 0.92, 0.25); cab.group.add(fp);
        const mg = tagSprite("MAGNETS", 0.085); mg.position.set(0.5, 0.78, 0.3); cab.group.add(mg);
        const lv = tagSprite("LEVER", 0.085); lv.position.set(0.42, 1.12, 0.1); cab.group.add(lv);
        // the candle smoke: dotted trail up the Turk's back to the neck (the puffs leave the turban in the card)
        const trail: THREE.Sprite[] = [];
        for (let i = 0; i < 14; i++) {
          const s = new THREE.Sprite(new THREE.SpriteMaterial({ color: "#e6e2f0", fog: false, transparent: true, depthWrite: false }));
          s.scale.setScalar(0.022); s.layers.set(NOINK); cab.group.add(s); trail.push(s);
        }
        const fade = (s: THREE.Sprite, a: number, b: number, t: number) => {
          const o = sm((t - a) / 0.3) * (1 - sm((t - b) / 0.3)); s.visible = o > 0.01; (s.material as THREE.SpriteMaterial).opacity = o;
        };
        return (t) => {
          fade(fp, behindW, S(11) - 0.1, t); fade(mg, boardW, w(11, "move", 1, 0.4), t); fade(lv, lever + 0.25, w(11, "hand", 1, 0.3, true), t);
          const on = sm((t - candle11) / 0.4) * (1 - sm((t - (t1 - 0.2)) / 0.2));
          trail.forEach((s, i) => {
            const u = ((i / trail.length + t * 0.35) % 1);
            const a = new THREE.Vector3(0.12, 0.82, -0.05), b = new THREE.Vector3(0.0, 1.3, -0.26), c = new THREE.Vector3(-0.14, 1.52, -0.26);
            const p = u < 0.5 ? a.clone().lerp(b, u * 2) : b.clone().lerp(c, (u - 0.5) * 2);
            s.position.copy(p); s.visible = on > 0.02; (s.material as THREE.SpriteMaterial).opacity = on * 0.9;
          });
        };
      },
    });
  }

  // ================= G10 the hall at night: the robot that beat Napoleon was a man in a box
  {
    const t0 = S(12), t1 = T.total;
    groups.push({
      id: "end", t0, t1, xfade: 0.233, set: () => hallSet(true), light: "night",
      cam: [
        fit(t0, [cabBox(CAB), personBox(CHAIR, true)], 20, 10, 42, {}, [personBox(CHAIR, true)]),                       // the robot and Napoleon
        fit(w(12, "napoleon"), [personBox(CHAIR, true, true), turkBox(CAB)], 38, 6, 40, {}, [personBox(CHAIR, true)]),
        fit(w(12, "man"), [rightBays(CAB)], 12, 4, 38, { x: 0.15, b: 0.4, t: 0.2 }, [personBox(CHAIR, true)]),       // the man in the box
        fit(w(12, "playing"), [rightBays(CAB)], 2, 2, 34, { x: 0.22, b: 0.45, t: 0.3 }, [personBox(CHAIR, true)]),   // playing by candlelight
      ],
      cabinet: {
        at: cabAt, setup: "napoleon",
        state: (t) => ({ t, cut: 1, master: true, seat: 1, masterCandle: 1, lever: 1 }),
        chess: () => ({ moves: [] }),
        turk: (t) => ({ arm: 1, look: 0.8, reach: track(t, [[0, 0.3], [w(12, "playing"), 0.3], [w(12, "candlelight"), 0.8]]) }),
        master: () => ({ costume: "master", seated: true, crouch: 1, seed: 7, item: "candle", pose: "hold", face: "smug" }),
      },
      people: [{ id: "napoleon", flip: true, at: () => CHAIR,
        props: (t) => ({ costume: "napoleon", seated: true, seed: 31, pose: "reach", face: step(t, [[0, "focus"], [w(12, "napoleon"), "frown"]]) }) }],
    });
  }

  const tags: Tag[] = [
    { text: "VIENNA, 1770", at: w(1, "see"), out: w(1, "empress's") - 0.3 },
    { text: "80 YEARS ON TOUR", at: w(6, "eighty"), out: w(6, "it") - 0.3 },
    { text: "PARIS, 1783", at: w(6, "it") + 0.15, out: S(7) - 0.1 },
    { text: "VIENNA, 1809", at: w(7, "napoleon"), out: w(7, "cheat") - 0.2 },
    { text: "PHILADELPHIA, 1854", at: w(8, "museum"), out: w(8, "turk") - 0.1 },
  ];
  return { groups, tags, paperAt: w(8, "secret") - 0.1, paperOut: S(9) + 0.85, headlineOut: w(0, "before") };
}

export type Tag = { text: string; at: number; out: number };
