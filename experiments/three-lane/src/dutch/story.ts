// story-dutch-waterline v1 (our own code): the anonymous Storm Oil form. A farmer cranks his own floodgate open with an
// invading army on the road behind him, wades in and checks the water against his knee; his neighbour pumps it back
// out; the general laughs at the "puddles", loses two riders and a hat to the hidden ditches, runs his troop boats
// aground and wades home carrying one. The only stated fact is the "You see" line (1672: the Dutch flooded their own
// land about knee-deep on purpose, too deep to march through, too shallow for boats, the ditches hidden).
// One polder world (sets.ts) plus the explainer's cut-away slice. Groups are anchored on the Kokoro (am_eric) word
// timings; the joins follow the RicksClips mix (dissolves 5-8 f, six whips, one cut, one match dissolve on the hat),
// and the gates stay failing.
import * as THREE from "three";
import type { GroupSpec, PersonSpec, V3, Rig } from "../kit/Stage";
import type { Timing } from "../kit/timing";
import { fit, tagSprite, sm, personBox, frameKey, track } from "../kit/framing";
import { castKey } from "../kit/castframe";
import type { CamKey } from "../kit/campath";
import { faceTrack, poseTrack, wordT, markAt, type Word } from "../kit/acting";
import { glints, debris } from "../kit/fx2";
import { mixKey } from "../kit/lightarc";
import { NOINK } from "../ink";
import { polderSet, sectionSet, floodRig, sectionWater, propRig, crowdRig, rider, soldier, horse, gallop, troopBoat, cannon, floatingHat,
  DIKE_Z, DIKE_H, GATE_Z, FAR, ROAD_Z, RISE, RISE_X, KNEE, SEC } from "./sets";

export type DutchStory = { groups: GroupSpec[] };

const clamp01 = (u: number) => Math.min(1, Math.max(0, u));
const cK = (t: number, feet: V3[], preset: "close" | "medium" | "wide", az: number, el: number, fov: number, s = 1): CamKey =>
  ({ ...castKey(t, feet, preset, az, el, fov, s), drift: preset === "wide" ? 0.3 : preset === "close" ? 0.5 : 0.4 });
const pair = (t: number, ps: V3[], az: number, el: number, fov = 40, drift = 0.3, seated = false): CamKey => ({ ...fit(t, ps.map((p) => personBox(p, seated)), az, el, fov, { b: 0.34, t: 0.16, x: 0.14 }), drift });
const D = (frames = 6) => ({ kind: "dissolve" as const, frames });
const WHIP = { kind: "whip" as const };
/** a world label that pops in at t0 and out at t1 */
const label = (text: string, at: V3, t0: number, t1: number, h = 1.2): Rig => (ctx) => {
  const s = tagSprite(text, h); ctx.root.add(s);
  const mat = (s as THREE.Sprite).material as THREE.SpriteMaterial;
  return (t) => { s.position.set(...at); const o = sm((t - t0) / 0.12) * (1 - sm((t - t1) / 0.12)); s.visible = o > 0.01; mat.opacity = o; };
};
/** water splashes: droplets thrown up in arcs (white-blue balls on the frame grid), a foam ring on the surface */
type Splash = { at: V3; t: number; size?: number; n?: number };
const splash = (cues: Splash[]): Rig => (ctx) => {
  const dm = new THREE.MeshBasicMaterial({ color: "#eaf6ff", fog: true }), rm = new THREE.MeshBasicMaterial({ color: "#f4fbff", transparent: true, depthWrite: false, fog: true, side: THREE.DoubleSide });
  const parts = cues.map((c, ci) => {
    let s = 17 + ci * 31; const r = () => ((s = (s * 16807) % 2147483647) / 2147483647);
    const drops = Array.from({ length: c.n ?? 14 }, () => { const m = new THREE.Mesh(new THREE.SphereGeometry(1, 6, 5), dm); m.layers.set(NOINK); ctx.root.add(m); const a = r() * Math.PI * 2, v = 0.5 + r() * 0.8; return { m, vx: Math.cos(a) * v, vz: Math.sin(a) * v, vy: 1.8 + r() * 1.8, k: 0.5 + r() * 0.6 }; });
    const ring = new THREE.Mesh(new THREE.RingGeometry(0.7, 1, 28), rm.clone()); ring.rotation.x = -Math.PI / 2; ring.layers.set(NOINK); ring.renderOrder = 4; ctx.root.add(ring);
    return { drops, ring };
  });
  return (t) => cues.forEach((c, i) => {
    const u = Math.round((t - c.t) * 30) / 30, sz = c.size ?? 1, { drops, ring } = parts[i];
    const on = u >= 0 && u < 0.7;
    for (const d of drops) { d.m.visible = on; if (!on) continue; d.m.position.set(c.at[0] + d.vx * u * 2 * sz, c.at[1] + (d.vy * u - 4.9 * u * u) * sz, c.at[2] + d.vz * u * 2 * sz); d.m.scale.setScalar(0.07 * sz * d.k * (1 - u)); }
    ring.visible = u >= 0 && u < 0.9; if (ring.visible) { ring.position.set(c.at[0], c.at[1] + 0.02, c.at[2]); ring.scale.setScalar(sz * (0.3 + 1.2 * Math.sqrt(u / 0.9))); (ring.material as THREE.MeshBasicMaterial).opacity = 0.9 * (1 - u / 0.9); }
  });
};

export function buildStory(T: Timing): DutchStory {
  const words = T.words as Word[];
  const w = (word: string, after = -1, n = 1) => wordT(words, word, n, after);
  const END = words[words.length - 1].end + 0.4;
  const groups: GroupSpec[] = [];
  const add = (g: GroupSpec) => groups.push({ sun: "auto", ...g } as GroupSpec);
  const DUSK = mixKey("golden", "fire", 0.45);

  // ---- the farm's timeline: the gate, the water, the windmill
  const tSlam = w("slams") + 0.3, tKnee = w("knee,", 19), tPump = w("pumping"), tStop = w("stops", 44);
  const level = (t: number) => track(t, [[0, -0.2], [10.4, -0.2], [10.5, 0.02], [12.6, 0.07], [13.2, 0.08], [15.0, 0.17], [15.3, 0.22], [19.6, 0.22], [tKnee + 0.05, KNEE]]);
  const open = (t: number) => (t < tSlam ? sm((t + 1.2) / 3.0) : 1 - clamp01((t - tSlam) / 0.12));
  const crank = (t: number) => -2.4 * Math.min(t + 1.2, 3.4);
  const sails = (t: number) => (t < tPump - 0.6 ? 0 : t < tStop ? 1.3 * (t - tPump + 0.6) : 1.3 * (tStop - tPump + 0.6) + 1.3 * 1.2 * (1 - Math.exp(-(t - tStop) / 1.2)));
  const pool = (t: number) => (t < -1 ? 0 : 0.6 + 2.2 * Math.sqrt(Math.max(0, t + 1)) + (t > 4.3 ? 2.5 * (t - 4.3) : 0));
  const farm = floodRig(level, open, crank, sails, pool);
  // pumping: the mill's outflow throws water over the dike while the sails turn
  const MILL: V3 = [-30, 0, -2.5];
  const pumpSplash = (t0: number, t1: number) => splash(Array.from({ length: Math.max(0, Math.floor((Math.min(t1, tStop) - Math.max(t0, tPump)) / 0.35)) }, (_, k) => ({ at: [MILL[0] + 1.5, DIKE_H + 0.2, DIKE_Z - 2.4] as V3, t: Math.max(t0, tPump) + k * 0.35, size: 1.4, n: 10 })));

  // ---- the cast
  const F_GATE: V3 = [-2.7, 0, GATE_Z + 0.6];
  const farmerP = (face: unknown, pose: unknown, extra: Record<string, unknown> = {}) => ({ costume: "farmer", seed: 11, face, pose, ...extra });
  const neighP = (face: unknown, pose: unknown, extra: Record<string, unknown> = {}) => ({ costume: "neighbour", seed: 23, face, pose, ...extra });
  const genP = (face: unknown, pose: unknown, extra: Record<string, unknown> = {}) => ({ costume: "general", seed: 37, face, pose, ...extra });
  const WHEEL: V3 = [-1.85, 1.15, GATE_Z + 0.45];
  // the hook's crank: his arms go round with the wheel (push / wind / reach in turn, 5 frames each)
  const crankPose = (t0: number, t1: number) => { const ks: { t: number; v: string }[] = []; for (let t = t0, k = 0; t < t1; t += 5 / 30, k++) ks.push({ t, v: ["push", "wind", "reach", "wind"][k % 4] }); return ks; };

  // ---- the army: a column on the far bank road, the general on the dike
  const column = (t: number, x0: number, n: number, v: number): V3[] => Array.from({ length: n }, (_, i) => [x0 - v * t + (i >> 1) * 2.6, FAR, ROAD_Z + (i % 2 ? 1.1 : -1.1)] as V3);
  const armyRig = (x0: number, n = 24, v = 1.6) => crowdRig((i) => (i % 3 === 2 ? soldier({ pike: true }) : rider({ horseCoat: ["#8a5a34", "#5a3a26", "#c8a070"][i % 3] })), (t) => column(t, x0, n, v), () => Math.PI,
    (o, t, i) => { const h = o.userData.horse as THREE.Group | undefined; if (h) gallop(h, t * 1.1 + i * 0.37, 0.35); else o.position.y += 0.06 * Math.abs(Math.sin(t * 6 + i)); });
  const HOOK_GX = -7.4;
  const genSeat = (h: V3, k = 1): V3 => [h[0], h[1] + (1.4 - 0.575) * k, h[2] + 0.05];
  // the hook's general rides in east along the dike crown just west of the gate and reins in behind the farmer, his
  // column on the crown behind him and more on the far bank road (drawn 1.15x: a cartoon cheat so his laugh reads on a
  // phone; the camera swings round to the farmer's front so the general stands over his shoulder, as in the key frame)
  const GK = 1.15, HOOK_GEN = (t: number): V3 => [HOOK_GX - 6.5 * (1 - sm(t / 2.4)), DIKE_H, DIKE_Z + 0.35];
  const crownColumn = (t: number, n: number): V3[] => Array.from({ length: n }, (_, i) => [HOOK_GEN(t)[0] - 3.4 - (i >> 1) * 2.4 - (i % 2) * 0.9, DIKE_H, DIKE_Z + (i % 2 ? -0.75 : 0.55)] as V3);
  const crownRig = crowdRig((i) => (i % 3 === 2 ? soldier({ pike: true }) : rider({ horseCoat: ["#8a5a34", "#5a3a26", "#c8a070"][i % 3] })), (t) => crownColumn(t, 14), () => 0,
    (o, t, i) => { const h = o.userData.horse as THREE.Group | undefined; const go = 0.08 + 0.3 * (1 - sm((t - 1.6) / 1.2)); if (h) gallop(h, t * 1.1 + i * 0.37, go); else o.position.y += 0.06 * go * Math.abs(Math.sin(t * 6 + i)); });

  // ================= 1 the hook: he cranks his own floodgate open, the army on the road behind, the general laughing
  {
    const t0 = 0, t1 = w("His", 4);
    const HEAD: V3 = [F_GATE[0], 1.375, F_GATE[2]];
        // one smooth orbit (sampled every 0.3 s so the farmer stays framed on the arc): from his close at the wheel round to
    // his front, pulling back until the general on the crown stands over his shoulder (by 2.5 s), then a slow drift
    const tSwing = 3.0;
    const hk = (t: number): CamKey => { const u = sm(t / tSwing), v = clamp01((t - tSwing) / (t1 - tSwing));
      return frameKey(t, HEAD, 0.3 - 0.02 * u, 0.33 + 0.18 * u + 0.01 * v, 0.59, 0.2 - 0.09 * u - 0.006 * v, -12 + 58 * u + 2 * v, 3 + 3 * u + 0.5 * v, 40, "lin"); };
    const cam: CamKey[] = [...Array.from({ length: 11 }, (_, k) => hk(k * 0.3)), hk(t1)];
    add({ id: "hook", place: "gate", t0, t1, xfade: 0, set: () => polderSet(), light: "golden", lens: { cInf: 4 }, cam, alive: [[t0, t1]],
      people: [{ id: "farmer", at: () => F_GATE, faceTo: () => WHEEL, props: () => farmerP(faceTrack(words, "angry", [{ word: "snorting.", face: "focus" }], t0), crankPose(t0 - 1, t1 + 1)) },
        { id: "gen", extra: true, scale: GK, at: (t) => genSeat(HOOK_GEN(t), GK), faceTo: () => F_GATE, props: () => genP(faceTrack(words, "grin", [{ word: "close", face: "cackle", react: [{ face: "squeeze", frames: 3 }] }], t0), poseTrack(words, "hold", [["close", "point"]], t0), { seated: true, chair: false }) }],
      rigs: [farm, armyRig(-52, 28), crownRig, propRig(() => { const h = horse({ coat: "#f2ece0", mane: "#c8b8a0" }); h.scale.setScalar(GK); return h; }, HOOK_GEN, () => 0, (o, t) => gallop(o as THREE.Group, t * 1.1, 0.06 + 0.3 * (1 - sm((t - 1.6) / 1.2)))),
        splash(Array.from({ length: 16 }, (_, k) => ({ at: [(k % 3 - 1) * 0.6, 0.08, GATE_Z + 1.2] as V3, t: k * 0.28, size: 1.1, n: 10 })))] });
  }
  // ================= 2 his neighbour drops his pitchfork (in the cabbages, the water spreading behind)
  const N_FIELD: V3 = [3.8, 0, 1.6];
  const fork = (from: () => V3 | null, drop: number) => propRig(() => { const g = new THREE.Group(); const wd = new THREE.MeshLambertMaterial({ color: "#8a6a3a" }), st = new THREE.MeshLambertMaterial({ color: "#9aa2b4" });
    const sh = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 1.6, 6), wd); sh.position.y = 0.8; g.add(sh);
    for (const x of [-0.1, 0, 0.1]) { const p = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.32, 5), st); p.position.set(x, 1.72, 0); g.add(p); }
    const cr = new THREE.Mesh(new THREE.BoxGeometry(0.26, 0.03, 0.03), st); cr.position.y = 1.58; g.add(cr); return g; }, from, () => 0.3,
    (o, t) => { const u = clamp01((t - drop) / 0.35); o.rotation.z = -1.45 * u * u; o.position.x += 0.9 * u * u; });
  {
    const t0 = w("His", 4), t1 = w('"The');
    const tDrop = w("drops") + 0.15;
    add({ id: "fork", place: "field", t0, t1, xfade: 0.2, join: WHIP, set: () => polderSet(), light: "golden", lens: { cInf: 6 },
      cam: [cK(t0, [N_FIELD], "medium", 36, 6, 40), { ...cK(t1, [N_FIELD], "medium", 28, 5, 36), glide: 1 }], alive: [[t0, t1]],
      people: [{ id: "neigh", at: () => N_FIELD, faceTo: () => F_GATE, props: () => neighP(faceTrack(words, "neutral", [{ word: "drops", face: "stunned", react: [{ face: "blank", frames: 2 }] }], t0), poseTrack(words, "hold", [["drops", "stand"], ["pitchfork.", "cheeks"]], t0)) }],
      rigs: [farm, fork(() => [N_FIELD[0] + 0.45, 0, N_FIELD[2] + 0.15], tDrop)] });
  }
  // ================= 3 "The enemy's coming, and you're watering the cabbages?" (the two of them; he keeps cranking)
  {
    const t0 = w('"The'), t1 = w("He", w('"The'));
    const N: V3 = [0.6, 0, GATE_Z + 3.2];
    add({ id: "cabbages", place: "gate", t0, t1, xfade: 0.2, join: D(6), set: () => polderSet(), light: "golden", lens: { cInf: 5 },
      cam: [pair(t0, [F_GATE, N], 24, 7, 42, 0), { ...pair(t1, [F_GATE, N], 14, 7, 38, 0), glide: 1 }], alive: [[t0, t1]],
      people: [{ id: "neigh", at: () => N, faceTo: () => F_GATE, props: () => neighP(faceTrack(words, "angry", [{ word: 'cabbages?"', face: "scream", react: [{ face: "squeeze", frames: 2 }] }], t0), poseTrack(words, "point", [["watering", "shrug"], ['cabbages?"', "armsUp"]], t0), { quote: [[t0, w('cabbages?"') + 0.5]] }) },
        { id: "farmer", at: () => F_GATE, faceTo: () => WHEEL, props: () => farmerP(faceTrack(words, "deadpan", [{ word: 'cabbages?"', face: "blank" }], t0), crankPose(t0, t1 + 1)) }],
      rigs: [farm, splash(Array.from({ length: 9 }, (_, k) => ({ at: [(k % 3 - 1) * 0.6, 0.08, GATE_Z + 1.2] as V3, t: t0 + k * 0.3, size: 1.1, n: 10 })))] });
  }
  // ================= 4 he props the floodgate open (an insert: a pole jammed under the raised board)
  {
    const t0 = w("He", w('"The')), t1 = w("rolls");
    const tProp = w("props") + 0.1;
    add({ id: "prop", place: "gate", insert: true, t0, t1, xfade: 0.2, join: D(5), set: () => polderSet(), light: "golden", lens: { cInf: 7 },
      cam: [{ t: t0, pos: [2.6, 1.0, GATE_Z + 4.2], look: [0.1, 1.2, GATE_Z], fov: 44, drift: 0 }, { t: t1, pos: [2.3, 0.9, GATE_Z + 3.6], look: [0.1, 1.1, GATE_Z], fov: 42, glide: 1 }], alive: [[t0, t1]],
      people: [],
      rigs: [farm, propRig(() => { const m = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.08, 1.7, 7), new THREE.MeshLambertMaterial({ color: "#7a5a32" })); return m; },
        (t) => (t < tProp - 0.3 ? null : [0.75, 0.75 + 0.6 * (1 - sm((t - tProp + 0.3) / 0.3)), GATE_Z + 0.25] as V3), () => 0, (o) => { o.rotation.x = 0.12; }),
        splash(Array.from({ length: 6 }, (_, k) => ({ at: [(k % 3 - 1) * 0.6, 0.08, GATE_Z + 1.2] as V3, t: t0 + k * 0.28, size: 1.2, n: 10 }))), glints([{ at: [0.75, 1.4, GATE_Z + 0.3], t: tProp, size: 0.8 }])] });
  }
  // ================= 5 rolls his trousers to the knee and wades in
  const wadeP = (t: number, t0: number, t1: number): V3 => { const u = sm((t - t0) / (t1 - t0)); return [-2.0 + 2.6 * u, 0, GATE_Z + 2.0 + 2.2 * u]; };
  const tWade0 = w("wades"), tWade1 = w('"Not') + 0.1;
  const F_IN: V3 = wadeP(99, tWade0, tWade1);
  {
    const t0 = w("rolls"), t1 = w('"Not');
    add({ id: "rolls", place: "field", t0, t1, xfade: 0.2, join: D(6), set: () => polderSet(), light: "golden", lens: { cInf: 6 },
      cam: [{ ...cK(t0, [wadeP(t0, tWade0, tWade1)], "medium", -40, 6, 40), drift: 0 }, { ...cK(tWade0, [wadeP(tWade0, tWade0, tWade1)], "medium", -36, 6, 40), glide: 1 }, { ...cK(t1, [F_IN], "medium", -30, 5, 38), glide: 1 }], alive: [[t0, t1]],
      people: [{ id: "farmer", at: (t) => wadeP(t, tWade0, tWade1), faceTo: () => [6, 0, 6], props: (t) => farmerP(faceTrack(words, "focus", [{ word: "wades", face: "deadpan" }], t0),
        poseTrack(words, "reach", [["knee,", "hips"], ["wades", "stand"]], t0), { crouch: [{ t: t0, v: 0.55 }, { t: w("knee,", t0) - 0.1, v: 0 }], walk: t > tWade0 && t < tWade1 ? 1 : 0 }) }],
      rigs: [farm, splash([0, 1, 2, 3].map((k) => { const tt = tWade0 + 0.1 + k * 0.15; const p = wadeP(tt, tWade0, tWade1); return { at: [p[0], 0.07, p[2]] as V3, t: tt, size: 0.6, n: 8 }; }))] });
  }
  // ================= 6 "Not yet," as the water creeps up his shin (the gauge, low at the water line)
  const knee = (t0: number, t1: number, id: string, cues: Parameters<typeof faceTrack>[2], pose: Parameters<typeof poseTrack>[2], extra: Record<string, unknown>, light: string, az0: number, az1: number, at: V3 = F_IN, opts: { dawn?: boolean } = {}, join: GroupSpec["join"] = WHIP) =>
    add({ id, place: "gauge", t0, t1, xfade: 0.2, join, set: () => polderSet(opts), light, lens: { cInf: 6 },
      cam: [{ ...fit(t0, [personBox(at)], az0, 2, 36, { b: 0.24, t: 0.12, x: 0.2 }), drift: 0 }, { ...fit(t1, [personBox(at)], az1, 1, 32, { b: 0.24, t: 0.12, x: 0.2 }), glide: 1 }], alive: [[t0, t1]],
      people: [{ id: "farmer", at: () => at, faceTo: () => [at[0] + 4, 0, at[2] + 1], props: () => farmerP(faceTrack(words, "focus", cues, t0), poseTrack(words, "hips", pose, t0), extra) }],
      rigs: [farm] });
  knee(w('"Not'), w("By"), "notyet", [{ word: '"Not', face: "deadpan" }, { word: "shin.", face: "puzzled" }], [['"Not', "hold"]], { quote: [[w('"Not'), w("says,") + 0.3]] }, "golden", -30, -22, F_IN, {}, WHIP);
  // ================= 7 by morning the whole village is furious (on the dike over the flooded fields)
  {
    const t0 = w("By"), t1 = w("and", w("furious,"));
    const V = [[-6.5, -8.6], [-8.0, -7.4], [-9.6, -8.4]].map(([x, z]): V3 => [x, DIKE_H, z]);
    const cos = ["citizen2", "villager3", "neighbour"];
    add({ id: "village", place: "dike", t0, t1, xfade: 0.2, join: D(8), set: () => polderSet({ dawn: true }), light: "golden", lens: { cInf: 5 },
      cam: [pair(t0, V, 18, 6, 44, 0), { ...pair(t1, V, 8, 5, 40, 0), glide: 1 }], alive: [[t0, t1]],
      people: V.map((p, i): PersonSpec => ({ id: `v${i}`, at: () => p, faceTo: () => [2, 0, 6], props: () => ({ costume: i === 2 ? "citizen" : cos[i], seed: 50 + i, face: faceTrack(words, "angry", [{ word: "furious,", face: i === 1 ? "scream" : "furious", react: [{ face: "squeeze", frames: 2 }] }], t0 + i * 0.1), pose: poseTrack(words, i === 1 ? "armsUp" : "point", [["furious,", i === 0 ? "strikeUp" : "armsUp"]], t0), marks: [markAt(words, "furious,", "vein")] }) })),
      rigs: [farm] });
  }
  // ================= 8 his neighbour pumping it back out with a windmill (the sails turn, water over the dike)
  const N_MILL: V3 = [-27.6, 0, 1.4];
  {
    const t0 = w("and", w("furious,")), t1 = w("Then", w("windmill."));
    add({ id: "mill", place: "mill", establishing: true, t0, t1, xfade: 0.2, join: D(6), set: () => polderSet({ dawn: true }), light: "golden", lens: { cInf: 4 },
      cam: [{ t: t0, pos: [-24, 6, 26], look: [-29.5, 5, -2], fov: 44, drift: 0.3 }, { ...cK(w("pumping") + 0.3, [N_MILL], "medium", 16, 16, 50), glide: 1 }, { ...cK(t1, [N_MILL], "medium", 12, 16, 48), glide: 1 }],
      alive: [[t0, t1]],
      people: [{ id: "neigh", at: () => N_MILL, faceTo: () => [-32, 0, 0], props: () => neighP(faceTrack(words, "angry", [{ word: "pumping", face: "grimace" }], t0), [{ t: t0, v: "push" }, ...Array.from({ length: 12 }, (_, k) => ({ t: tPump + k * 0.3, v: k % 2 ? "push" : "reach" }))], { marks: [markAt(words, "windmill.", "sweat")] }) }],
      rigs: [farm, pumpSplash(t0, t1)] });
  }
  // ================= 9 then the water touches his knee (the gauge again, the line right at his knee)
  knee(w("Then", w("windmill.")), w("and", tKnee), "knee", [{ word: "knee,", face: "stunned", react: [{ face: "blank", frames: 2 }] }], [["knee,", "point"]], { marks: [markAt(words, "knee,", "sweat")] }, "day", 26, 18, F_IN, {}, WHIP);
  // ================= 10 he slams the floodgate shut: "That'll do."
  {
    const t0 = w("and", tKnee), t1 = w("Soon");
    const F: V3 = [-1.4, 0, GATE_Z + 1.2];
    add({ id: "slam", place: "gate", t0, t1, xfade: 0.2, join: D(6), set: () => polderSet(), light: "day", lens: { cInf: 5 },
      cam: [{ ...fit(t0, [personBox(F), [-1.3, 0, GATE_Z - 0.3, 1.5, 3.5, GATE_Z + 0.3]], -34, 6, 42, { b: 0.3, t: 0.12, x: 0.1 }), drift: 0 }, { ...cK(w('"That\'ll'), [F], "close", -24, 4, 38), glide: 0.6 }, { ...cK(t1, [F], "close", -20, 4, 36), glide: 1 }],
      alive: [[t0, t1]],
      people: [{ id: "farmer", at: () => F, faceTo: () => [3, 0, GATE_Z + 3], props: () => farmerP(faceTrack(words, "focus", [{ word: "slams", face: "angry" }, { word: '"That\'ll', face: "smug" }], t0), poseTrack(words, "reach", [["slams", "strike"], ['"That\'ll', "hips"]], t0), { quote: [[w('"That\'ll'), w('do."') + 0.4]] }) }],
      rigs: [farm, splash([{ at: [0, 0.4, GATE_Z + 0.2], t: tSlam + 0.1, size: 2.2, n: 20 }]), glints([{ at: [0, 2.0, GATE_Z + 0.2], t: tSlam + 0.1, size: 1.6 }])] });
  }
  // ---- the east: the army's rise, the general on his white horse at the edge of the water
  const G_HORSE: V3 = [RISE_X + 3.5, RISE, 17.2];
  const G_SEAT = genSeat(G_HORSE);
  const genHorse = (jig = 0) => propRig(() => horse({ coat: "#f2ece0", mane: "#c8b8a0" }), () => G_HORSE, () => Math.PI, (o, t) => gallop(o as THREE.Group, t * 0.6, jig));
  const camp = (t: number): V3[] => Array.from({ length: 22 }, (_, i) => [RISE_X + 8 + (i >> 1) * 2.6, RISE, 20 + (i % 2 ? 1.2 : -1.2)] as V3);
  const campRig = crowdRig((i) => (i % 3 === 2 ? soldier({ pike: true }) : rider({ horseCoat: ["#8a5a34", "#5a3a26", "#c8a070"][i % 3] })), camp, () => Math.PI,
    (o, t, i) => { const h = o.userData.horse as THREE.Group | undefined; if (h) gallop(h, t * 0.5 + i * 0.3, 0.12); });
  const day = () => polderSet();
  // ================= 11 soon the army reaches the flood (high, behind the column: the shiny water to the horizon)
  {
    const t0 = w("Soon"), t1 = w("and", w("flood,"));
    const arrive = (t: number): V3[] => camp(t).map((p) => [p[0] + 14 - 14 * sm((t - t0 + 0.4) / 1.8), p[1], p[2]] as V3);
    add({ id: "reach", place: "rise", establishing: true, t0, t1, xfade: 0.2, join: D(6), set: day, light: "day", lens: { cInf: 3 },
      cam: [{ t: t0, pos: [RISE_X + 52, 16, 40], look: [RISE_X - 30, 0, 12], fov: 46, drift: 0 }, { t: t1, pos: [RISE_X + 46, 14, 37], look: [RISE_X - 32, 0, 12], fov: 46, glide: 1 }],
      people: [], alive: [[t0, t1]],
      rigs: [farm, crowdRig((i) => (i % 3 === 2 ? soldier({ pike: true }) : rider({ horseCoat: ["#8a5a34", "#5a3a26", "#c8a070"][i % 3] })), arrive, () => Math.PI, (o, t, i) => { const h = o.userData.horse as THREE.Group | undefined; if (h) gallop(h, t * 1.1 + i * 0.3, 0.35 * (1 - sm((t - t0 - 1.2) / 0.6))); }),
        propRig(() => horse({ coat: "#f2ece0", mane: "#c8b8a0" }), (t) => [G_HORSE[0] + 14 - 14 * sm((t - t0 + 0.4) / 1.8), G_HORSE[1], G_HORSE[2]], () => Math.PI, (o, t) => gallop(o as THREE.Group, t * 1.1, 0.35 * (1 - sm((t - t0 - 1.2) / 0.6))))] });
  }
  // ================= 12 their general laughs so hard he nearly falls off his horse
  {
    const t0 = w("and", w("flood,")), t1 = w('"They\'re');
    const tFall = w("falls");
    const at = (t: number): V3 => { const u = sm((t - tFall + 0.1) / 0.25) * (1 - sm((t - tFall - 0.55) / 0.3)); return [G_SEAT[0] + 0.28 * u, G_SEAT[1] - 0.22 * u, G_SEAT[2]]; };
    add({ id: "laugh", place: "rise", t0, t1, xfade: 0.2, join: D(6), set: day, light: "day", lens: { cInf: 6 },
      cam: [{ ...fit(t0, [personBox(G_SEAT, true), [G_HORSE[0] - 1.2, RISE, G_HORSE[2] - 0.4, G_HORSE[0] + 1.0, RISE + 1.4, G_HORSE[2] + 0.4]], -64, 6, 40, { b: 0.3, t: 0.14, x: 0.1 }), drift: 0 }, { ...cK(tFall, [G_SEAT], "medium", -54, 6, 38), glide: 1 }, { ...cK(t1, [G_SEAT], "medium", -50, 6, 36), glide: 1 }],
      alive: [[t0, t1]],
      people: [{ id: "gen", at, faceTo: () => [0, 0, 10], props: () => genP(faceTrack(words, "grin", [{ word: "laughs", face: "cackle", react: [{ face: "squeeze", frames: 3 }] }, { word: "falls", face: "terrified" }, { word: "horse.", face: "cackle" }], t0), poseTrack(words, "laugh", [["falls", "armsUp"], ["horse.", "laugh"]], t0), { seated: true, chair: false, hatPop: [tFall] }) }],
      rigs: [farm, genHorse(0.05), campRig] });
  }
  // ================= 13 "They're defending their country with puddles!" (close, pointing at the water)
  {
    const t0 = w('"They\'re'), t1 = w("The", t0);
    add({ id: "puddles", place: "rise", t0, t1, xfade: 0, join: { kind: "cut" }, set: day, light: "day", lens: { cInf: 7 },
      cam: [cK(t0, [G_SEAT], "close", -30, 4, 40), { ...cK(t1, [G_SEAT], "close", -24, 3, 36), glide: 1 }], alive: [[t0, t1]],
      people: [{ id: "gen", at: () => G_SEAT, faceTo: () => [RISE_X - 20, 0, 17], props: () => genP(faceTrack(words, "smug", [{ word: 'puddles!"', face: "cackle", react: [{ face: "squeeze", frames: 2 }] }], t0), poseTrack(words, "point", [['puddles!"', "laugh"]], t0), { seated: true, chair: false, quote: [[t0, w('puddles!"') + 0.5]] }) }],
      rigs: [farm, genHorse(0), campRig] });
  }
  // ---- the cavalry charge: ten riders down the ramp and west across the water
  // lane 13 is the first plunge's alone and the rest ride 4+ m north of it (the hat shots look past the hat from beside
  // it): v1 had riders in lanes 13-16 galloping right past the lens at 35.5-36.9 s; they now ride in a pack at 17-21
  const LANE = (i: number) => [13, 18, 17.6, 19, 19.8, 20, 17, 21, 18.3, 20.6][i];
  const tGo = w("sends", w("general", 29)) + 0.2;
  const charge = (t: number, i: number): V3 => { const u = Math.max(0, t - tGo - (i % 5) * 0.12 - Math.floor(i / 5) * 0.5); const x = RISE_X + 6 + (i % 5) * 1.4 + Math.floor(i / 5) * 3 - 6.5 * u; return [x, x > RISE_X ? RISE : Math.max(0, RISE - (RISE_X - x) * 0.12), LANE(i)]; };
  const tV1 = w("vanishes,"), tV2 = w("another.") - 0.1;
  const plunge = (t: number, tv: number, p: V3): V3 | null => { const u = (t - tv) / 0.3; return u < 0 ? p : u > 1 ? null : [p[0] - 0.8 * u, p[1] - 2.6 * u * u, p[2]]; };
  const V1 = 0, V2 = 6;     // the riders the ditches take
  const cav = (frozenAfter = 1e9) => crowdRig((i) => rider({ horseCoat: ["#8a5a34", "#5a3a26", "#c8a070", "#3a2a22"][i % 4] }),
    (t) => Array.from({ length: 10 }, (_, i) => { const p = charge(Math.min(t, frozenAfter), i); return i === V1 ? plunge(t, tV1, charge(Math.min(t, tV1), i)) : i === V2 ? plunge(t, tV2, charge(Math.min(t, tV2), i)) : p; }),
    () => Math.PI, (o, t, i) => { const h = o.userData.horse as THREE.Group; if (h) gallop(h, t * 2.2 + i * 0.27, 0.75); o.position.y += 0.08 * Math.abs(Math.sin(t * 7 + i)); });
  const cavSplash = (t0: number, t1: number) => splash(Array.from({ length: 10 }, (_, i) => i).flatMap((i) => Array.from({ length: Math.ceil((t1 - t0) / 0.4) }, (_, k) => { const tt = t0 + k * 0.4 + (i % 4) * 0.1; const p = charge(tt, i); return p[0] < RISE_X - 1 && !(i === V1 && tt > tV1) && !(i === V2 && tt > tV2) ? [{ at: [p[0] - 0.3, KNEE + 0.02, p[2]] as V3, t: tt, size: 1.0, n: 8 }] : []; })));
  const HAT1: V3 = [charge(tV1, V1)[0] - 0.9, KNEE, LANE(V1)], HAT2: V3 = [charge(tV2, V2)[0] - 0.9, KNEE, LANE(V2) + 0.4];
  const hatRig = (p: V3, tIn: number) => propRig(floatingHat, (t) => (t < tIn ? null : [p[0] - 0.08 * (t - tIn), p[1] + 0.025 * Math.sin(t * 3.4) + (t - tIn < 0.25 ? 0.6 * (1 - (t - tIn) / 0.25) : 0), p[2]] as V3), (t) => 0.4 * t, (o, t) => { o.rotation.z = 0.12 * Math.sin(t * 2.7); });
  // ================= 14 he sends his cavalry galloping across the shiny water (low, beside the charge)
  {
    const t0 = w("The", w('"They\'re')), t1 = w("Seconds");
    add({ id: "charge", place: "polder", establishing: true, t0, t1, xfade: 0.2, join: D(6), set: day, light: "day", lens: { cInf: 4 },
      cam: [{ t: t0, pos: [RISE_X - 5, 1.7, 26], look: [RISE_X + 4, 1.4, 17], fov: 46, drift: 0 }, { t: t1, pos: [RISE_X - 14, 1.5, 26.5], look: [RISE_X - 9, 1.1, 17], fov: 46, glide: 1 }],
      people: [], alive: [[t0, t1]],
      rigs: [farm, cav(), cavSplash(t0, t1), genHorse(0), campRig, label("SHINY WATER", [RISE_X - 26, 3.2, 17], w("shiny") - 0.1, t1 + 1, 1.2)] });
  }
  // ================= 15 seconds later the first horse vanishes, rider and all, leaving one hat floating
  const hatKey = (t: number, d: number, az: number, el: number): CamKey => { const a = (az * Math.PI) / 180, e = (el * Math.PI) / 180; return { t, pos: [HAT1[0] + Math.sin(a) * Math.cos(e) * d, HAT1[1] + Math.sin(e) * d, HAT1[2] + Math.cos(a) * Math.cos(e) * d], look: [HAT1[0], HAT1[1] + 0.3, HAT1[2]], fov: 42 }; };
  {
    const t0 = w("Seconds"), t1 = w("Then", tV1);
    const cv = (t: number) => charge(Math.min(t, tV1), V1);
    add({ id: "vanish", place: "polder", establishing: true, t0, t1, xfade: 0.2, join: D(6), set: day, light: "day", lens: { cInf: 6 },
      cam: [{ t: t0, pos: [cv(t0)[0] - 12, 2.2, LANE(V1) - 9], look: [cv(t0)[0] - 3, 1.2, LANE(V1)], fov: 42, drift: 0 }, { t: tV1, pos: [cv(tV1)[0] - 9, 2.0, LANE(V1) - 7.5], look: [cv(tV1)[0] - 1, 1.0, LANE(V1)], fov: 42, glide: 1 },
        { ...hatKey(w("hat"), 4.4, 130, 14), glide: 1 }, { ...hatKey(t1, 3.8, 105, 13), glide: 1 }],
      people: [], alive: [[t0, t1]],
      rigs: [farm, cav(), cavSplash(t0, t1), splash([{ at: [cv(tV1)[0] - 0.6, KNEE, LANE(V1)], t: tV1 + 0.05, size: 2.6, n: 24 }]), hatRig(HAT1, tV1 + 0.3), label("ONE HAT", [HAT1[0], 1.6, HAT1[2]], w("hat") - 0.05, t1 + 1, 0.55)] });
  }
  // ================= 16 "Then another." - a match dissolve on the floating hat; the next rider goes down behind it
  {
    const t0 = w("Then", tV1), t1 = w("The", w("another."));
    const c2 = charge(tV2, V2);
    add({ id: "another", place: "polder", establishing: true, t0, t1, xfade: 0.2, join: { kind: "dissolve", frames: 6, match: true }, set: day, light: "day", lens: { cInf: 6 },
      cam: [{ ...hatKey(t0, 3.8, 105, 13), drift: 0 }, { ...hatKey(t1, 5.2, 104, 9), glide: 1 }],
      people: [], alive: [[t0, t1]],
      rigs: [farm, cav(), cavSplash(t0, t1), splash([{ at: [c2[0] - 0.6, KNEE, LANE(V2)], t: tV2 + 0.05, size: 2.6, n: 24 }]), hatRig(HAT1, tV1 + 0.3), hatRig(HAT2, tV2 + 0.3)] });
  }
  // ================= 17 the general sends boats to fish them out (soldiers shove two loaded boats down the ramp)
  const tBoat = w("sends", w("general", 38)) + 0.3, tScrape = w("scrape"), tStopB = w("stop", tScrape) + 0.25;
  const boatX = (t: number, k: number) => { const u = Math.max(0, t - tBoat - k * 0.4); const free = RISE_X - 4 - 3.2 * u; const stopAt = RISE_X - 4 - 3.2 * (tStopB - tBoat - k * 0.4) + 1.2; return t < tStopB ? free : stopAt + Math.min(0, free - stopAt); };
  const BZ = (k: number) => 11 - k * 3.4;
  const boatPos = (t: number, k: number): V3 => { const x = boatX(t, k); return [x, x > RISE_X - 6 ? Math.max(0, RISE - (RISE_X - x) * 0.12) : 0, BZ(k)]; };
  const boatRig = (k: number) => propRig(() => troopBoat({ crew: 6 }), (t) => boatPos(t, k), () => Math.PI, (o, t) => { const v = clamp01((t - tScrape) / 0.25) * (1 - clamp01((t - tStopB - 0.2) / 0.5)); o.rotation.z = -0.1 * v; o.rotation.x = 0.04 * Math.sin(t * 9) * v; });
  {
    const t0 = w("The", w("another.")), t1 = w("and", w("out,", t0));
    add({ id: "boats", place: "rise", t0, t1, xfade: 0.2, join: D(6), set: day, light: "day", lens: { cInf: 5 },
      cam: [{ ...fit(t0, [personBox(G_SEAT, true), [RISE_X - 3, RISE, 8, RISE_X - 1, RISE + 1.2, 11]], 24, 8, 40, { b: 0.3, t: 0.14, x: 0.06 }), drift: 0 }, { ...fit(t1, [personBox(G_SEAT, true), [RISE_X - 4, 0.4, 8, RISE_X - 2, 1.6, 11]], 18, 8, 38, { b: 0.3, t: 0.14, x: 0.06 }), glide: 1 }],
      alive: [[t0, t1]],
      people: [{ id: "gen", at: () => G_SEAT, faceTo: () => [RISE_X - 20, 0, 17], props: () => genP(faceTrack(words, "angry", [{ word: "boats", face: "furious" }], t0), poseTrack(words, "point", [["fish", "sweep"]], t0), { seated: true, chair: false, quote: [[w("sends", t0), w("out,", t0)]] }) }],
      rigs: [farm, genHorse(0), boatRig(0), boatRig(1), splash([0, 1].map((k) => ({ at: [RISE_X - 6, KNEE, BZ(k)] as V3, t: tBoat + 0.6 + k * 0.4, size: 2.4, n: 18 })))] });
  }
  // ================= 18 and the boats scrape to a stop in the mud (low beside the lead boat, mud flying)
  {
    const t0 = w("and", w("out,", w("The", w("another.")))), t1 = w("Back", 41);
    const b0 = (t: number) => boatPos(t, 0);
    add({ id: "scrape", place: "polder", insert: true, t0, t1, xfade: 0.2, join: WHIP, set: day, light: "day", lens: { cInf: 6 },
      cam: [{ t: t0, pos: [b0(t0)[0] - 6, 1.0, BZ(0) + 5.5], look: [b0(t0)[0] - 0.5, 0.7, BZ(0)], fov: 44, drift: 0 }, { t: tStopB, pos: [b0(tStopB)[0] - 5.2, 0.9, BZ(0) + 4.9], look: [b0(tStopB)[0] - 0.3, 0.7, BZ(0)], fov: 42, glide: 1 }, { t: t1, pos: [b0(tStopB)[0] - 5.0, 0.9, BZ(0) + 4.7], look: [b0(tStopB)[0] - 0.3, 0.7, BZ(0)], fov: 40, glide: 1 }],
      people: [], alive: [[t0, t1]],
      rigs: [farm, boatRig(0), boatRig(1), debris([0, 1, 2].map((k) => ({ at: (t: number) => { const p = boatPos(t, 0); return [p[0] - 2.6, 0.35, p[2]] as V3; }, t: tScrape + k * 0.22, n: 26, kind: "shard" as const, size: 0.18, floorY: KNEE, up: 1.4, speed: 2.4 }))),
        splash([{ at: [boatPos(tScrape, 0)[0] - 2.4, KNEE, BZ(0)], t: tScrape, size: 1.8, n: 16 }, { at: [boatPos(tStopB, 0)[0] - 2.6, KNEE, BZ(0)], t: tStopB - 0.1, size: 2.2, n: 18 }]), label("STUCK", [boatPos(tStopB, 0)[0], 2.6, BZ(0)], tStopB, t1 + 1, 0.7)] });
  }
  // ================= 19 back at the gate, the farmer checks the water against his knee (the gauge, third time: a nod)
  knee(w("Back", 41), w("and", w("knee,", 41)), "check", [{ word: "checks", face: "focus" }, { word: "knee,", face: "smug" }], [["checks", "reach"], ["knee,", "hips"]], { crouch: [{ t: w("checks"), v: 0.35 }, { t: w("knee,", 41) - 0.1, v: 0 }] }, "day", -18, -10, [-0.9, 0, GATE_Z + 2.6], {}, D(6));
  // ================= 20 and his neighbour quietly stops pumping (at the mill door, the sails slow to a stop)
  {
    const t0 = w("and", w("knee,", 41)), t1 = w("You");
    add({ id: "quiet", place: "mill", t0, t1, xfade: 0.2, join: D(6), set: () => polderSet(), light: "day", lens: { cInf: 5 },
      cam: [{ ...cK(t0, [N_MILL], "medium", 34, 8, 44), drift: 0 }, { ...cK(t1, [N_MILL], "medium", 26, 8, 40), glide: 1 }], alive: [[t0, t1]],
      people: [{ id: "neigh", at: (t) => [N_MILL[0] + 0.5 * sm((t - tStop) / 0.6), 0, N_MILL[2] + 0.3 * sm((t - tStop) / 0.6)], faceTo: () => [-20, 0, 8], props: () => neighP(faceTrack(words, "worried", [{ word: "stops", face: "sly" }], t0), [{ t: t0, v: "push" }, ...Array.from({ length: Math.max(0, Math.floor((tStop - t0) / 0.3)) }, (_, k) => ({ t: t0 + 0.3 * (k + 1), v: k % 2 ? "push" : "reach" })), { t: tStop, v: "handIn" }], { look: [{ t: t0, v: 0 }, { t: tStop + 0.3, v: -1 }] }) }],
      rigs: [farm, pumpSplash(t0, t1)] });
  }
  // ================= 21 you see: the Dutch really did this in 1672 to stop a French invasion (high over the polder)
  const arrowRig = (from: V3, to: V3, t0: number, t1: number, color = "#2f4f9e"): Rig => (ctx) => {
    const len = Math.hypot(to[0] - from[0], to[2] - from[2]), sh = new THREE.Shape();
    sh.moveTo(0, -3); sh.lineTo(len - 12, -3); sh.lineTo(len - 12, -8); sh.lineTo(len, 0); sh.lineTo(len - 12, 8); sh.lineTo(len - 12, 3); sh.lineTo(0, 3); sh.lineTo(0, -3);
    const m = new THREE.Mesh(new THREE.ShapeGeometry(sh), new THREE.MeshBasicMaterial({ color, transparent: true, depthWrite: false, fog: false })); m.rotation.x = -Math.PI / 2; m.rotation.z = Math.atan2(-(to[2] - from[2]), to[0] - from[0]); m.position.set(from[0], 3, from[2]); m.layers.set(NOINK); m.renderOrder = 6; ctx.root.add(m);
    return (t) => { const u = sm((t - t0) / (t1 - t0)); m.scale.set(Math.max(0.02, u), 1, 1); m.visible = t > t0; };
  };
  {
    const t0 = w("You"), t1 = w("keeping");
    add({ id: "map", place: "map", insert: true, t0, t1, xfade: 0.2, join: WHIP, set: () => polderSet({ high: true }), light: "day", lens: { cInf: 1 },
      cam: [{ t: t0, pos: [RISE_X + 70, 120, 20], look: [10, 0, 14], fov: 44, drift: 0 }, { t: w("stop", t0), pos: [RISE_X + 24, 62, 19], look: [28, 0, 15], fov: 44, glide: 1, drift: 0.2 }, { t: t1, pos: [RISE_X + 20, 58, 19], look: [26, 0, 15], fov: 44, glide: 1, drift: 0.2 }],
      people: [], alive: [[t0, t1]],
      rigs: [farm, campRig, label("1672", [10, 24, 14], w("1672") - 0.1, t1 + 1, 11), label("HOLLAND", [-10, 5.5, 14], w("Dutch") - 0.1, t1 + 1, 7),
        label("FRENCH ARMY", [RISE_X + 22, 8, 14], w("French") - 0.1, t1 + 1, 5), arrowRig([RISE_X + 70, 0, 20], [RISE_X - 2, 0, 20], w("stop", t0) - 0.2, w("stop", t0) + 0.6, "#c8382c"),
        label("WATER LINE", [50, 5, 14], w("invasion,") - 0.1, t1 + 1, 5)] });
  }
  // ---- the explainer slice: he stands in it to show the depth; a horse, a cannon, a boat, a ditch
  const SX = (x: number): V3 => [x, 0, 0.3];
  const secCam = (t: number, x: number, w0: number, el = 8, lookY = 0.8): CamKey => ({ t, pos: [x, lookY + Math.tan((el * Math.PI) / 180) * w0, w0], look: [x, lookY, 0], fov: 40 });
  const water = sectionWater(() => KNEE);
  {
    const t0 = w("keeping"), t1 = w("That's");
    const F = SX(-8.4);
    add({ id: "kneedeep", place: "section", insert: true, t0, t1, xfade: 0.2, join: D(6), set: sectionSet, light: "explain", lens: { cInf: 2 },
      cam: [{ ...secCam(t0, -8.2, 6.4, 6, 0.9), drift: 0 }, { ...secCam(t1, -8.0, 5.8, 6, 0.85), glide: 1 }], alive: [[t0, t1]],
      people: [{ id: "farmer", at: () => F, faceTo: () => [0, 0, 6], props: () => farmerP(faceTrack(words, "smug", [{ word: "knee-deep", face: "bliss" }], t0), poseTrack(words, "hips", [["knee-deep", "point"]], t0)) }],
      rigs: [water, label("KNEE-DEEP", [-8.2, -0.45, 1.7], w("knee-deep") - 0.1, t1 + 1, 0.24), label("ON PURPOSE", [-8.2, 2.25, 0.4], w("purpose.") - 0.1, t1 + 1, 0.34)] });
  }
  {
    const t0 = w("That's"), t1 = w("but", t0);
    add({ id: "toodeep", place: "section", insert: true, t0, t1, xfade: 0.2, join: D(5), set: sectionSet, light: "explain", lens: { cInf: 2 },
      cam: [{ ...secCam(t0, -0.9, 8.6, 8, 1.0), drift: 0 }, { ...secCam(t1, -0.4, 8.0, 8, 1.0), glide: 1 }], alive: [[t0, t1]],
      people: [],
      rigs: [water, propRig(() => rider(), () => [-1.9, -0.05, 0.2], () => 0, (o, t) => { const h = o.userData.horse as THREE.Group; gallop(h, t * 1.6, 0.5); o.rotation.z = 0.05 * Math.sin(t * 5); }),
        propRig(cannon, (t) => [0.0 + 0.04 * Math.sin(t * 9), -0.12, 0.3], () => 0), propRig(() => soldier({}), (t) => [1.15, 0, 0.3 + 0.03 * Math.sin(t * 8)], () => Math.PI, (o, t) => { o.rotation.z = 0.35 + 0.05 * Math.sin(t * 8); }),
        splash([0, 1, 2, 3, 4].map((k) => ({ at: [-1.6 + (k % 2) * 0.5, KNEE, 0.6] as V3, t: t0 + k * 0.42, size: 0.9, n: 8 }))),
        label("TOO DEEP TO MARCH", [-0.6, 2.7, 0.5], w("deep", t0) - 0.1, t1 + 1, 0.42)] });
  }
  {
    const t0 = w("but", w("That's")), t1 = w("And", t0);
    add({ id: "tooshallow", place: "section", insert: true, t0, t1, xfade: 0.2, join: D(5), set: sectionSet, light: "explain", lens: { cInf: 2 },
      cam: [{ ...secCam(t0, 8.4, 8.4, 8, 0.8), drift: 0 }, { ...secCam(t1, 8.6, 7.6, 8, 0.8), glide: 1 }], alive: [[t0, t1]],
      people: [],
      rigs: [water, propRig(() => troopBoat({ crew: 4 }), (t) => [8.6 - 0.25 * (1 - sm((t - t0) / 0.5)), 0.0, 0.2], () => 0, (o, t) => { o.rotation.z = 0.06 * (1 - sm((t - t0) / 0.6)); }),
        splash([{ at: [11.2, KNEE, 0.6], t: t0 + 0.15, size: 1.4, n: 14 }]), label("TOO SHALLOW TO FLOAT", [8.4, 2.4, 0.5], w("shallow") - 0.1, t1 + 1, 0.42)] });
  }
  {
    const t0 = w("And", w("but", w("That's"))), t1 = w("By", t0);
    const tPl = w("plunge."), D2 = SEC.ditches[1];
    const sx = (t: number): V3 => { const u = clamp01((t - w("so", t0)) / (tPl - w("so", t0))); const fall = clamp01((t - tPl) / 0.28); const x = D2 - 2.4 + 1.5 * u + 0.75 * fall; return [x, -1.5 * fall * fall, 0.3]; };
    add({ id: "ditch", place: "section", insert: true, t0, t1, xfade: 0.2, join: D(6), set: sectionSet, light: "explain", lens: { cInf: 2 },
      cam: [{ t: t0, pos: [D2 - 1.3, 8.5, 8.0], look: [D2 - 1.3, 0.2, 0], fov: 40, drift: 0 }, { ...secCam(w("every", t0) + 0.6, D2 - 1.35, 9.6, 6, 0.3), glide: 1 }, { ...secCam(t1, D2 - 1.25, 9.2, 5, 0.2), glide: 1 }],
      alive: [[t0, t1]],
      people: [{ id: "sol", at: sx, faceTo: () => [D2 + 4, 0, 0], props: (t) => ({ costume: "fsoldier", seed: 61, face: faceTrack(words, "smug", [{ word: "step", face: "worried" }, { word: "plunge.", face: "terrified", react: [{ face: "scream", frames: 3 }] }], t0), pose: poseTrack(words, "stand", [["plunge.", "armsUp"]], t0), walk: t > w("so", t0) && t < tPl ? 1 : 0 }) }],
      rigs: [sectionWater((t) => KNEE), splash([{ at: [D2, KNEE, 0.6], t: tPl + 0.2, size: 1.8, n: 20 }]), label("HIDDEN DITCH", [D2 - 0.9, -1.1, 1.75], w("ditch") - 0.1, t1 + 1, 0.3),
        (ctx) => { const top = ctx.set.extra.top as THREE.Mesh, m = top.material as THREE.MeshLambertMaterial, ws = ctx.set.extra.ditchW as unknown as THREE.Mesh[];
          return (t) => { const reveal = sm((t - w("every", t0) - 0.2) / 0.6); m.opacity = 0.98 - 0.45 * reveal; ws.forEach((d) => { (d.material as THREE.MeshLambertMaterial).opacity = 0.8; }); }; }] });
  }
  // ================= 26 by sunset the general who laughed at puddles wades home, soaked to the knee, carrying his own boat
  {
    const t0 = w("By", w("plunge.")), t1 = END;
    const g = (t: number): V3 => [40 + 0.9 * (t - t0), 0, 30];
    const tSoak = w("soaked");
    // he holds it up right side up (v1 carried it hull-up over his head): the keel on his raised hands, the hull just
    // behind his head, tipped toward the camera so the seats show
    const BOAT_Y = 1.47;
    const boatBox = (p: V3): [number, number, number, number, number, number] => [p[0] - 1.25, BOAT_Y, p[2] - 0.95, p[0] + 1.25, BOAT_Y + 0.4, p[2] - 0.15];
    add({ id: "home", place: "polder-dusk", t0, t1, xfade: 0.2, join: D(8), set: () => polderSet({ dusk: true }), light: DUSK, lens: { cInf: 5 },
      cam: [{ ...fit(t0, [personBox(g(t0)), personBox(g(tSoak)), boatBox(g(t0)), boatBox(g(tSoak))], -20, 7, 44, { b: 0.3, t: 0.12, x: 0.1 }), drift: 0 }, { ...fit(tSoak, [personBox(g(tSoak)), boatBox(g(tSoak))], -12, 4, 40, { b: 0.24, t: 0.1, x: 0.1 }), glide: 1 }, { ...fit(t1, [personBox(g(t1)), boatBox(g(t1))], -8, 3, 36, { b: 0.24, t: 0.1, x: 0.1 }), glide: 1 }],
      alive: [[t0, t1]],
      people: [{ id: "gen", at: g, faceTo: (t) => [g(t)[0] + 10, 0, g(t)[2]], props: () => genP(faceTrack(words, "sob", [{ word: "soaked", face: "grimace" }, { word: "boat.", face: "sob" }], t0), "armsUp", { walk: 1, stepF: 9, marks: [markAt(words, "soaked", "tears")] }) }],
      rigs: [floodRig(() => KNEE, () => 0), propRig(() => { const b = troopBoat({}); b.scale.setScalar(0.42); return b; }, (t) => { const p = g(t); return [p[0] + 0.1, BOAT_Y + 0.025 * Math.abs(Math.sin(t * 6.6)), p[2] - 0.55]; }, () => 0.45, (o, t) => { o.rotation.x = 0.28; o.rotation.z = 0.04 * Math.sin(t * 3.3); }),
        splash(Array.from({ length: Math.ceil((t1 - t0) / 0.6) }, (_, k) => { const tt = t0 + k * 0.6; const p = g(tt); return { at: [p[0] + 0.2, KNEE + 0.01, p[2] + 0.1] as V3, t: tt, size: 0.7, n: 8 }; }))] });
  }
  return { groups };
}
