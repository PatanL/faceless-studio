// The places of story-dutch-waterline as 3D sets (our own code, on the kit's set helpers): one Dutch polder world.
// The farm sits south of a grass dike (z -8) with a wooden floodgate in a gap at x 0; behind the dike a canal (water
// y CANAL) and a high far bank (y FAR) carry the army's road (z -34). The polder fields (y 0) are cut into parcels by
// ditches; the flood is one water plane whose height the story sets per frame (FLOOD.y). The neighbour's windmill
// stands at the dike foot west of the gate, the village further west, and the army's camp on a rise to the east
// (x > 90, y RISE) where its road runs down into the polder. Horses, soldiers, boats and the cannon are code models
// with round white heads (the house character design); the named cast are Actor cards (story.ts).
import * as THREE from "three";
import { mergeGeometries } from "three/examples/jsm/utils/BufferGeometryUtils.js";
import { NOINK } from "../ink";
import { SetBuild, lambert, box, skyDome, makeKey } from "../kit/sets";
import { richWater, grainPlanks } from "../kit/dressing";
import { tent } from "../kit/architecture";
import { rng } from "../paint";
import type { V3, Rig } from "../kit/Stage";

const canvas = (w: number, h: number) => { const c = document.createElement("canvas"); c.width = w; c.height = h; return [c, c.getContext("2d")!] as const; };
const tex = (c: HTMLCanvasElement, repeat: [number, number] = [1, 1]) => { const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(...repeat); t.anisotropy = 8; return t; };
const clamp01 = (u: number) => Math.min(1, Math.max(0, u));

export const DIKE_Z = -8, GATE_Z = -3.6, DIKE_H = 1.3, CANAL = 0.9, FAR = 2.2, ROAD_Z = -34, RISE = 0.8, RISE_X = 90;
/** the knee: where the water stands on an Actor card (the knee of the 1.75 m drawing is 0.31 m up) */
export const KNEE = 0.31;
/** the flood: one plane over the whole polder; the story writes FLOOD.y before each frame (the floodRig) */
export const FLOOD = { y: -0.2 };

// ------------------------------------------------------------------------------------------------ textures
let fieldT: THREE.CanvasTexture | null = null;
/** one 20 m polder parcel: green crop rows, a ditch along two edges (it tiles into a grid of parcels) */
function fieldTex() {
  if (fieldT) return fieldT;
  const S = 512, [c, g] = canvas(S, S), r = rng(5);
  g.fillStyle = "#7aa84e"; g.fillRect(0, 0, S, S);
  for (let y = 0; y < S; y += 16) { g.fillStyle = y % 32 ? "#6c9a44" : "#86b456"; g.fillRect(0, y, S, 8); }
  for (let k = 0; k < 500; k++) { g.fillStyle = `rgba(${r() < 0.5 ? "60,90,40" : "150,190,90"},0.25)`; g.fillRect(r() * S, r() * S, 3 + r() * 6, 2 + r() * 3); }
  g.fillStyle = "#3d6a8a"; g.fillRect(0, 0, S, 14); g.fillRect(0, 0, 14, S);           // the ditches
  g.fillStyle = "#4f8a3c"; g.fillRect(0, 14, S, 5); g.fillRect(14, 0, 5, S);
  fieldT = tex(c, [40, 40]); return fieldT;
}
function grassTex(rep: [number, number], seed = 3) {
  const S = 256, [c, g] = canvas(S, S), r = rng(seed);
  g.fillStyle = "#6f9e46"; g.fillRect(0, 0, S, S);
  for (let k = 0; k < 900; k++) { g.strokeStyle = r() < 0.5 ? "rgba(70,110,40,0.5)" : "rgba(160,200,100,0.5)"; g.lineWidth = 2; const x = r() * S, y = r() * S; g.beginPath(); g.moveTo(x, y); g.lineTo(x + (r() - 0.5) * 4, y - 6 - r() * 6); g.stroke(); }
  return tex(c, rep);
}
let streakT: THREE.CanvasTexture | null = null;
/** white foam streaks along +v (a gushing sheet of water) */
function streaks() {
  if (streakT) return streakT;
  const S = 256, [c, g] = canvas(S, S), r = rng(9);
  g.fillStyle = "rgba(90,170,220,0.95)"; g.fillRect(0, 0, S, S);
  g.lineCap = "round";
  for (let i = 0; i < 70; i++) { const x = r() * S, y = r() * S, h = 30 + r() * 80; g.strokeStyle = `rgba(245,252,255,${0.5 + r() * 0.5})`; g.lineWidth = 3 + r() * 6; g.beginPath(); g.moveTo(x, y); g.lineTo(x + (r() - 0.5) * 6, y + h); g.stroke(); }
  streakT = tex(c, [2, 1]); return streakT;
}

// ------------------------------------------------------------------------------------------------ props (code models)
const M: Record<string, THREE.Material> = {};
const mat = (k: string, f: () => THREE.Material) => (M[k] ??= f());
const HEAD_M = () => mat("head", () => lambert({ color: "#f6f1e6" }));

/** a horse (our own model), ~1.15 m at the withers, facing +x; legs are pivot groups (userData.legs) for the gallop;
 * userData.saddle = the saddle top (local) */
export function horse(o: { coat?: string; mane?: string; seed?: number } = {}): THREE.Group {
  const g = new THREE.Group();
  const coat = mat(`h${o.coat}`, () => lambert({ color: o.coat ?? "#8a5a34" })), mane = mat(`m${o.mane}`, () => lambert({ color: o.mane ?? "#3a2618" }));
  const body = new THREE.Mesh(new THREE.SphereGeometry(0.5, 16, 12), coat); body.scale.set(1.25, 0.62, 0.55); body.position.set(0, 1.05, 0); body.castShadow = true; g.add(body);
  const neck = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.22, 0.75, 10), coat); neck.position.set(0.55, 1.42, 0); neck.rotation.z = -0.75; neck.castShadow = true; g.add(neck);
  const head = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.24, 0.22), coat); head.position.set(0.86, 1.66, 0); head.rotation.z = -0.55; head.castShadow = true; g.add(head);
  const muzzle = new THREE.Mesh(new THREE.SphereGeometry(0.13, 10, 8), mat("muzzle", () => lambert({ color: "#e8d8c4" }))); muzzle.position.set(1.06, 1.54, 0); g.add(muzzle);
  for (const s of [-1, 1]) { const ear = new THREE.Mesh(new THREE.ConeGeometry(0.05, 0.16, 6), coat); ear.position.set(0.74, 1.86, s * 0.07); g.add(ear);
    const eye = new THREE.Mesh(new THREE.SphereGeometry(0.035, 8, 6), mat("eye", () => lambert({ color: "#1a1420" }))); eye.position.set(0.86, 1.72, s * 0.11); g.add(eye); }
  const m1 = new THREE.Mesh(new THREE.BoxGeometry(0.62, 0.12, 0.06), mane); m1.position.set(0.48, 1.62, 0); m1.rotation.z = -0.75; g.add(m1);
  const tail = new THREE.Mesh(new THREE.ConeGeometry(0.1, 0.7, 8), mane); tail.position.set(-0.7, 0.92, 0); tail.rotation.z = -0.5; g.add(tail);
  const saddle = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.08, 0.6), mat("saddle", () => lambert({ color: "#5a2a1e" }))); saddle.position.set(0.02, 1.36, 0); g.add(saddle);
  const cloth = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.34, 0.62), mat("cloth", () => lambert({ color: "#2f4f9e" }))); cloth.position.set(0.02, 1.2, 0); g.add(cloth);
  const legs: THREE.Group[] = [];
  for (const [x, z] of [[0.38, 0.16], [0.38, -0.16], [-0.38, 0.16], [-0.38, -0.16]]) {
    const pv = new THREE.Group(); pv.position.set(x, 0.95, z); g.add(pv);
    const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.06, 0.92, 8), coat); leg.position.y = -0.46; leg.castShadow = true; pv.add(leg);
    const hoof = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.09, 0.08, 8), mane); hoof.position.y = -0.92; pv.add(hoof);
    legs.push(pv);
  }
  g.userData.legs = legs; g.userData.saddle = 1.4;
  return g;
}
/** swing the legs: gallop (u = phase in cycles) or 0 to stand */
export function gallop(h: THREE.Group, u: number, amp = 0.7) {
  (h.userData.legs as THREE.Group[]).forEach((l, i) => { l.rotation.z = amp * Math.sin(2 * Math.PI * u + [0, 0.5, 2.6, 3.1][i]); });
}
/** a round-head soldier (our own model): white head, blue coat, steel morion; seated = the rider (no legs); facing +x */
export function soldier(o: { seated?: boolean; coat?: string; pike?: boolean; hat?: "morion" | "none" | "tricorn" } = {}): THREE.Group {
  const g = new THREE.Group();
  const coat = mat(`c${o.coat}`, () => lambert({ color: o.coat ?? "#2f4f9e" })), steel = mat("steel", () => lambert({ color: "#9aa2b4" })), ink = mat("ink", () => lambert({ color: "#1d1a2e" }));
  const y0 = o.seated ? 0 : 0.5;
  if (!o.seated) for (const s of [-1, 1]) { const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.5, 6), mat("legs", () => lambert({ color: "#e8e0cc" }))); leg.position.set(0, 0.25, s * 0.09); g.add(leg); }
  const body = new THREE.Mesh(new THREE.CylinderGeometry(0.17, 0.23, 0.62, 10), coat); body.position.y = y0 + 0.31; body.castShadow = true; g.add(body);
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.25, 16, 12), HEAD_M()); head.position.y = y0 + 0.86; head.castShadow = true; g.add(head);
  for (const s of [-1, 1]) { const e = new THREE.Mesh(new THREE.SphereGeometry(0.03, 6, 5), ink); e.position.set(0.22, y0 + 0.88, s * 0.08); g.add(e); }
  if ((o.hat ?? "morion") === "morion") {
    const cap = new THREE.Mesh(new THREE.SphereGeometry(0.26, 14, 8, 0, Math.PI * 2, 0, Math.PI / 2), steel); cap.position.y = y0 + 0.93; g.add(cap);
    const brim = new THREE.Mesh(new THREE.TorusGeometry(0.27, 0.03, 6, 18), steel); brim.rotation.x = Math.PI / 2; brim.position.y = y0 + 0.93; g.add(brim);
    const crest = new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.1, 0.03), steel); crest.position.y = y0 + 1.2; g.add(crest);
  } else if (o.hat === "tricorn") {
    const tri = new THREE.Mesh(new THREE.ConeGeometry(0.34, 0.2, 3), ink); tri.position.y = y0 + 1.08; g.add(tri);
  }
  if (o.pike) { const p = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 3.0, 5), mat("pole", () => lambert({ color: "#6a4a2a" }))); p.position.set(0.22, y0 + 1.2, 0.18); g.add(p);
    const tip = new THREE.Mesh(new THREE.ConeGeometry(0.06, 0.24, 6), steel); tip.position.set(0.22, y0 + 2.8, 0.18); g.add(tip); }
  return g;
}
/** a rider on a horse: the soldier sits on the saddle; userData.horse for the gallop */
export function rider(o: { coat?: string; horseCoat?: string } = {}): THREE.Group {
  const g = new THREE.Group(), h = horse({ coat: o.horseCoat }); g.add(h);
  const s = soldier({ seated: true, coat: o.coat }); s.position.set(-0.02, 1.38, 0); g.add(s);
  for (const z of [-0.2, 0.2]) { const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.5, 6), mat("legs", () => lambert({ color: "#e8e0cc" }))); leg.position.set(0.05, 1.2, z * 1.4); leg.rotation.z = 0.25; s.parent!.add(leg); }
  g.userData.horse = h; return g;
}
/** a heavy troop boat (our own model): a flat-bottomed wooden hull, 5.4 m, bow +x, gunwale 0.75 m up; userData.seats */
export function troopBoat(o: { crew?: number } = {}): THREE.Group {
  const g = new THREE.Group();
  const sh = new THREE.Shape(); sh.moveTo(-2.6, -0.9); sh.lineTo(1.6, -0.9); sh.quadraticCurveTo(2.7, -0.5, 2.9, 0); sh.quadraticCurveTo(2.7, 0.5, 1.6, 0.9); sh.lineTo(-2.6, 0.9); sh.lineTo(-2.6, -0.9);
  const hole = new THREE.Path(); hole.moveTo(-2.45, -0.75); hole.lineTo(1.5, -0.75); hole.quadraticCurveTo(2.45, -0.4, 2.6, 0); hole.quadraticCurveTo(2.45, 0.4, 1.5, 0.75); hole.lineTo(-2.45, 0.75); hole.lineTo(-2.45, -0.75); sh.holes.push(hole);
  const wood = mat("boat", () => lambert({ map: grainPlanks([2, 1], { hue: 26, light: 40, boards: 5, seed: 4 }) })), dark = mat("boatd", () => lambert({ color: "#5a3a22" }));
  const wall = new THREE.Mesh(new THREE.ExtrudeGeometry(sh, { depth: 0.6, bevelEnabled: false }), wood); wall.rotation.x = -Math.PI / 2; wall.position.y = 0.15; wall.castShadow = true; g.add(wall);
  const floor = new THREE.Shape(sh.getPoints(16));
  const bottom = new THREE.Mesh(new THREE.ExtrudeGeometry(floor, { depth: 0.16, bevelEnabled: false }), dark); bottom.rotation.x = -Math.PI / 2; bottom.position.y = 0.0; g.add(bottom);
  const rim = new THREE.Mesh(new THREE.BoxGeometry(5.3, 0.06, 0.06), mat("trim", () => lambert({ color: "#c8382c" })));
  for (const z of [-0.88, 0.88]) { const r2 = rim.clone(); r2.position.set(-0.4, 0.76, z); g.add(r2); }
  for (const x of [-1.6, -0.2, 1.1]) box(g, dark, 0.22, 0.06, 1.6, x, 0.45, 0);
  const crew = o.crew ?? 0, seats: V3[] = [];
  for (let k = 0; k < crew; k++) { const x = -2.0 + (k >> 1) * 1.3, z = (k % 2 ? 0.38 : -0.38); seats.push([x, 0.16, z]);
    const s = soldier({ seated: true, pike: k % 3 === 0 }); s.position.set(x, 0.42, z); g.add(s); }
  for (const z of [-1, 1]) { const oar = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 2.4, 5), mat("pole", () => lambert({ color: "#6a4a2a" }))); oar.position.set(-0.4, 0.75, z * 1.3); oar.rotation.x = z * 1.2; g.add(oar); }
  g.userData.seats = seats; return g;
}
/** a field cannon on a two-wheeled carriage, barrel +x */
export function cannon(): THREE.Group {
  const g = new THREE.Group(), wood = mat("cwood", () => lambert({ color: "#7a4e2a" })), iron = mat("iron", () => lambert({ color: "#2c2e3a" }));
  const b = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.18, 1.8, 12), iron); b.rotation.z = -Math.PI / 2 + 0.12; b.position.set(0.3, 0.75, 0); b.castShadow = true; g.add(b);
  box(g, wood, 1.6, 0.18, 0.4, -0.3, 0.5, 0);
  for (const z of [-0.4, 0.4]) { const w = new THREE.Mesh(new THREE.TorusGeometry(0.45, 0.06, 6, 18), wood); w.position.set(0, 0.48, z); g.add(w);
    for (let k = 0; k < 6; k++) { const sp = new THREE.Mesh(new THREE.BoxGeometry(0.85, 0.04, 0.04), wood); sp.rotation.z = (k * Math.PI) / 6; sp.position.set(0, 0.48, z); g.add(sp); } }
  return g;
}
/** a cabbage (flattened green ball with leaf rings) */
function cabbageGeo(x: number, z: number, s: number) {
  const a = new THREE.SphereGeometry(0.2 * s, 9, 7); a.scale(1, 0.8, 1); a.translate(x, 0.13 * s, z);
  const b = new THREE.SphereGeometry(0.26 * s, 9, 5, 0, Math.PI * 2, Math.PI * 0.45, Math.PI * 0.4); b.translate(x, 0.2 * s, z);
  return [a, b];
}
/** a Dutch gabled house: brick body, a stepped gable to the street (+z), a steep tiled roof */
function dutchHouse(root: THREE.Object3D, x: number, z: number, w: number, h: number, d: number, seed: number) {
  const r = rng(seed), brick = mat(`br${seed % 3}`, () => lambert({ color: ["#b85a3c", "#a04a34", "#c46a44"][seed % 3] })), roof = mat("roof", () => lambert({ color: "#4a3a3a" })), white = mat("white", () => lambert({ color: "#f2ead8" })), win = mat("win", () => lambert({ color: "#2f4a6a" }));
  box(root, brick, w, h, d, x, h / 2, z);
  const sh = new THREE.Shape(); sh.moveTo(-w / 2, 0); sh.lineTo(w / 2, 0); sh.lineTo(0, w * 0.75); sh.lineTo(-w / 2, 0);
  const gable = new THREE.Mesh(new THREE.ExtrudeGeometry(sh, { depth: d, bevelEnabled: false }), roof); gable.position.set(x, h, z - d / 2); gable.castShadow = true; root.add(gable);
  for (const s of [-1, 1]) box(root, white, 0.5, 0.7, 0.06, x + s * w * 0.22, h * 0.62, z + d / 2 + 0.02, false);
  box(root, white, 0.6, 1.1, 0.06, x + (r() - 0.5) * 0.4, 0.55, z + d / 2 + 0.02, false);
  box(root, win, 0.36, 0.5, 0.08, x - w * 0.22, h * 0.62, z + d / 2 + 0.03, false); box(root, win, 0.36, 0.5, 0.08, x + w * 0.22, h * 0.62, z + d / 2 + 0.03, false);
}
/** a windmill (polder mill): a tapered octagonal thatched tower, a cap, four lattice sails facing +z (extra.sails) */
function windmill(root: THREE.Object3D, x: number, z: number): THREE.Group {
  const thatch = mat("thatch", () => lambert({ color: "#6a5a44" })), cap = mat("cap", () => lambert({ color: "#3a3030" })), sailM = mat("sail", () => lambert({ color: "#efe6d2", side: THREE.DoubleSide })), frame = mat("sframe", () => lambert({ color: "#5a3a2a" }));
  const tw = new THREE.Mesh(new THREE.CylinderGeometry(1.5, 2.6, 7.5, 8), thatch); tw.position.set(x, 3.75, z); tw.castShadow = true; root.add(tw);
  box(root, mat("base", () => lambert({ color: "#9a4a34" })), 5.6, 1.2, 5.6, x, 0.6, z);
  const c = new THREE.Mesh(new THREE.SphereGeometry(1.7, 12, 8, 0, Math.PI * 2, 0, Math.PI / 2), cap); c.scale.set(1, 0.8, 1.2); c.position.set(x, 7.5, z); root.add(c);
  box(root, mat("door", () => lambert({ color: "#3a2a20" })), 0.9, 1.6, 0.1, x, 1.9, z + 2.35, false);
  const hub = new THREE.Group(); hub.position.set(x, 7.6, z + 2.0); root.add(hub);
  for (let k = 0; k < 4; k++) { const arm = new THREE.Group(); arm.rotation.z = (k * Math.PI) / 2; hub.add(arm);
    const spar = new THREE.Mesh(new THREE.BoxGeometry(0.14, 6.4, 0.14), frame); spar.position.y = 3.2; arm.add(spar);
    const sail = new THREE.Mesh(new THREE.PlaneGeometry(1.2, 5.0), sailM); sail.position.set(0.68, 3.6, 0.02); arm.add(sail);
    for (let j = 0; j < 6; j++) { const bar = new THREE.Mesh(new THREE.BoxGeometry(1.3, 0.05, 0.05), frame); bar.position.set(0.68, 1.4 + j * 0.85, 0.06); arm.add(bar); } }
  // the outflow: a wooden trough over the dike to the canal, with a sheet of water in it (extra.spout)
  return hub;
}
/** a poplar */
function poplar(root: THREE.Object3D, x: number, z: number, h: number, y = 0) {
  const leaf = mat("leaf", () => lambert({ color: "#3f7a3c" })), trunk = mat("trunk", () => lambert({ color: "#6b4a2b" }));
  const tr = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.2, h * 0.4, 6), trunk); tr.position.set(x, y + h * 0.2, z); root.add(tr);
  const cr = new THREE.Mesh(new THREE.SphereGeometry(1, 10, 8), leaf); cr.scale.set(h * 0.17, h * 0.42, h * 0.17); cr.position.set(x, y + h * 0.58, z); cr.castShadow = true; root.add(cr);
}
/** the dike's cross-section (z, y) swept along x from x0 to x1 */
function dike(root: THREE.Object3D, x0: number, x1: number, zc: number, h: number, top = 3, base = 9, m?: THREE.Material) {
  const sh = new THREE.Shape(); sh.moveTo(-base / 2, -0.05); sh.lineTo(base / 2, -0.05); sh.lineTo(top / 2, h); sh.lineTo(-top / 2, h); sh.lineTo(-base / 2, -0.05);
  const g = new THREE.ExtrudeGeometry(sh, { depth: x1 - x0, bevelEnabled: false }); g.rotateY(Math.PI / 2); g.translate(x0, 0, zc);
  const d = new THREE.Mesh(g, m ?? lambert({ map: grassTex([0.4, 0.4]) })); d.castShadow = true; d.receiveShadow = true; root.add(d);
  const path = new THREE.Mesh(new THREE.PlaneGeometry(x1 - x0, top * 0.5), mat("path", () => lambert({ color: "#c8a878" }))); path.rotation.x = -Math.PI / 2; path.position.set((x0 + x1) / 2, h + 0.01, zc); path.receiveShadow = true; root.add(path);
  return d;
}

export type PolderOpts = { dusk?: boolean; dawn?: boolean; high?: boolean };
/** the polder world. extra: flood (the water plane), gate (the sliding gate board), wheel, gush (the sheet of water
 * through the gate), pool (the spreading disc of water in front of it), sails (the windmill's hub), cabbages */
export function polderSet(o: PolderOpts = {}): SetBuild {
  const root = new THREE.Group();
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(800, 800), lambert({ map: fieldTex() })); ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; root.add(ground);
  // the flood (the story moves it), and the canal behind the dike
  const flood = new THREE.Mesh(new THREE.PlaneGeometry(800, 800), lambert({ map: richWater([160, 160]), transparent: true, opacity: 0.93 }));
  flood.rotation.x = -Math.PI / 2; flood.position.y = FLOOD.y; flood.receiveShadow = true; flood.userData.noWaves = true; flood.renderOrder = 1; root.add(flood);
  const canal = new THREE.Mesh(new THREE.PlaneGeometry(800, 24), lambert({ map: richWater([160, 5]) })); canal.rotation.x = -Math.PI / 2; canal.position.set(0, CANAL, -20); root.add(canal);
  // the dike, broken at the gate (x -1.2..1.2), and the high far bank with the road
  const grass = lambert({ map: grassTex([8, 1]) });
  dike(root, -300, -1.2, DIKE_Z, DIKE_H, 3, 9, grass); dike(root, 1.2, 300, DIKE_Z, DIKE_H, 3, 9, grass);
  box(root, grass, 600, FAR, 40, 0, FAR / 2, -52); box(root, mat("bank", () => lambert({ color: "#7a6a4a" })), 600, FAR - CANAL + 0.4, 1.0, 0, CANAL + (FAR - CANAL) / 2 - 0.2, -32.1, false);
  const road = new THREE.Mesh(new THREE.PlaneGeometry(600, 4), mat("road", () => lambert({ color: "#c8a878" }))); road.rotation.x = -Math.PI / 2; road.position.set(0, FAR + 0.01, ROAD_Z - 2); road.receiveShadow = true; root.add(road);
  // the gap's floor and the floodgate: two posts, a beam, the board (slides up), a crank wheel on the west post
  const wood = mat("gwood", () => lambert({ map: grainPlanks([1, 1], { hue: 28, light: 40, boards: 4, seed: 6 }) })), dark = mat("gdark", () => lambert({ color: "#5a3a22" })), iron = mat("giron", () => lambert({ color: "#3a3a44" }));
  box(root, mat("sill", () => lambert({ color: "#7a6a5a" })), 2.4, 0.04, 9, 0, 0.02, DIKE_Z);
  for (const s of [-1, 1]) { box(root, wood, 0.4, 3.4, 0.4, s * 1.35, 1.7, GATE_Z); box(root, mat("chan", () => lambert({ color: "#8a7a5a" })), 0.3, DIKE_H, 9, s * 1.35, DIKE_H / 2, DIKE_Z); }
  box(root, wood, 3.3, 0.4, 0.45, 0, 3.3, GATE_Z);
  const gate = new THREE.Group(); root.add(gate);
  box(gate, wood, 2.4, 1.5, 0.2, 0, 0.75, GATE_Z - 0.15); for (const y of [0.3, 0.75, 1.2]) box(gate, dark, 2.45, 0.08, 0.06, 0, y, GATE_Z - 0.03, false);
  const rope = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 1.8, 5), mat("rope", () => lambert({ color: "#d8b878" }))); rope.position.set(0, 2.4, GATE_Z - 0.05); root.add(rope);
  const pulley = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.25, 0.2, 14), iron); pulley.rotation.x = Math.PI / 2; pulley.position.set(0, 3.3, GATE_Z + 0.3); root.add(pulley);
  const wheel = new THREE.Group(); wheel.position.set(-1.85, 1.15, GATE_Z + 0.45); root.add(wheel);
  const rim = new THREE.Mesh(new THREE.TorusGeometry(0.62, 0.07, 8, 26), wood); wheel.add(rim);
  for (let k = 0; k < 4; k++) { const sp = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.07, 0.07), wood); sp.rotation.z = (k * Math.PI) / 4; wheel.add(sp); }
  const handle = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 0.4, 6), dark); handle.rotation.x = Math.PI / 2; handle.position.set(0.55, 0, 0.2); wheel.add(handle);
  const axle = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 0.6, 10), iron); axle.rotation.x = Math.PI / 2; axle.position.set(-1.85, 1.15, GATE_Z + 0.2); root.add(axle);
  box(root, wood, 0.3, 1.2, 0.3, -1.85, 0.6, GATE_Z + 0.25);
  // the gush: a sheet of streaked water from the canal lip down through the gap onto the field
  const gushG = new THREE.PlaneGeometry(2.3, 11, 1, 24); const gp = gushG.getAttribute("position") as THREE.BufferAttribute;
  for (let i = 0; i < gp.count; i++) { const v = (gp.getY(i) + 5.5) / 11; const zz = -13 + (1 - v) * 11.5, k = clamp01((zz - GATE_Z + 0.3) / 1.6), yy = 0.06 + (CANAL - 0.06) * (1 - k * k * (3 - 2 * k)); gp.setXYZ(i, gp.getX(i), yy, zz); }
  gushG.computeVertexNormals();
  const gush = new THREE.Mesh(gushG, new THREE.MeshBasicMaterial({ map: streaks().clone(), transparent: true, depthWrite: false, side: THREE.DoubleSide, fog: true }));
  (gush.material as THREE.MeshBasicMaterial).map!.needsUpdate = true; gush.layers.set(NOINK); gush.renderOrder = 3; root.add(gush);
  const pool = new THREE.Mesh(new THREE.CircleGeometry(1, 40), new THREE.MeshBasicMaterial({ map: richWater([4, 4]), transparent: true, opacity: 0.95, fog: true, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -4 }));
  pool.rotation.x = -Math.PI / 2; pool.position.set(0, 0.03, GATE_Z + 2.4); pool.scale.set(1, 0.6, 1); pool.renderOrder = 2; root.add(pool);
  // cabbages in rows on the farm's field (x -12..14, z -4..16)
  const cg: THREE.BufferGeometry[] = [], r = rng(13);
  for (let x = -12; x <= 14; x += 1.1) for (let z = -3.4; z <= 16; z += 1.0) { if (x > -3.6 && x < 2 && z < 0.6) continue; cg.push(...cabbageGeo(x + (r() - 0.5) * 0.2, z + (r() - 0.5) * 0.2, 0.9 + r() * 0.35)); }
  const cabbages = new THREE.Mesh(mergeGeometries(cg.map((g) => g.toNonIndexed())), lambert({ color: "#7ec05a" })); cabbages.castShadow = true; cabbages.receiveShadow = true; root.add(cabbages);
  // the farmhouse on its mound, the neighbour's windmill at the dike foot, the village, poplars along the dike
  box(root, grass, 14, 0.5, 12, -18, 0.25, 8); dutchHouse(root, -18, 8, 6, 3.4, 7, 1); box(root, mat("barn", () => lambert({ color: "#6a4a3a" })), 5, 2.6, 5, -24, 1.55, 6);
  const sails = windmill(root, -30, -2.5);
  for (let k = 0; k < 9; k++) { box(root, grass, 9, 0.5, 9, -56 - k * 7, 0.25, 6 + (k % 3) * 6); dutchHouse(root, -56 - k * 7, 6 + (k % 3) * 6, 4.5 + (k % 2), 3 + (k % 3) * 0.6, 5, k + 2); }
  const church = new THREE.Mesh(new THREE.ConeGeometry(1.4, 9, 8), mat("spire", () => lambert({ color: "#3a4a5a" }))); church.position.set(-80, 12, 2); root.add(church); box(root, mat("chb", () => lambert({ color: "#a04a34" })), 4, 8, 4, -80, 4, 2);
  for (let k = 0; k < 26; k++) { const x = -150 + k * 12 + (k % 3) * 2; if (Math.abs(x) < 8 || Math.abs(x + 30) < 6) continue; poplar(root, x, DIKE_Z - 2.8, 7 + (k % 4), DIKE_H * 0.6); }
  for (let k = 0; k < 14; k++) poplar(root, -140 + k * 21, -46, 8 + (k % 3) * 2, FAR);
  // the army's rise to the east: a raised plateau with its road running down into the polder at RISE_X
  box(root, grass, 200, RISE, 120, RISE_X + 100, RISE / 2, 20);
  const ramp = new THREE.Mesh(new THREE.BoxGeometry(10, 0.3, 6), mat("road", () => lambert({ color: "#c8a878" }))); ramp.position.set(RISE_X - 3, RISE / 2 - 0.1, 20); ramp.rotation.z = Math.atan2(RISE, 10) * 0.9; root.add(ramp);
  const road2 = new THREE.Mesh(new THREE.PlaneGeometry(100, 5), mat("road", () => lambert({ color: "#c8a878" }))); road2.rotation.x = -Math.PI / 2; road2.position.set(RISE_X + 50, RISE + 0.01, 20); road2.receiveShadow = true; root.add(road2);
  // the camp on the rise: tents, banners
  for (let k = 0; k < 9; k++) { const tn = tent({ r: 2.2 + (k % 3) * 0.4, h: 3 + (k % 2), a: "#f0ead8", b: k % 2 ? "#2f4f9e" : "#c8382c", seed: k }); tn.position.set(RISE_X + 14 + (k % 3) * 8, RISE, 4 + Math.floor(k / 3) * 7 - (k % 2) * 2); root.add(tn); }
  for (const [x, z, c] of [[RISE_X + 8, 14, "#2f4f9e"], [RISE_X + 8, 26, "#f2ead8"], [RISE_X + 30, 12, "#2f4f9e"]] as [number, number, string][]) {
    const p = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 6, 6), mat("pole", () => lambert({ color: "#6a4a2a" }))); p.position.set(x, RISE + 3, z); root.add(p);
    const f = new THREE.Mesh(new THREE.PlaneGeometry(2.4, 1.5), lambert({ color: c, side: THREE.DoubleSide })); f.position.set(x + 1.2, RISE + 5.1, z); root.add(f); }
  // far trees and a horizon line of mills
  for (let k = 0; k < 12; k++) poplar(root, RISE_X + 10 + k * 9, 52, 7 + (k % 3), RISE);
  const sky = o.dusk ? skyDome(root, "#3d4688", "#e0806a", "#f6c088", 1500) : o.dawn ? skyDome(root, "#5a7ac0", "#e8b0a0", "#f8dcb4", 1500) : skyDome(root, "#3f7fd0", "#9cc4e8", "#f3e0b8", 1500);
  const key = o.dusk ? makeKey(root, [-120, 40, 80], [0, 0, 0], 80) : o.dawn ? makeKey(root, [100, 40, 90], [0, 0, 0], 80) : makeKey(root, [-60, 90, 70], [0, 0, 0], 80);
  key.shadow.camera.far = 400;
  return { root, key, glows: [], sky, extra: { flood, gate, wheel, gush, pool, sails, cabbages, canal }, fogScale: o.high ? 14 : 8 };
}

/** flood(t) = the water height over the polder; the gate opening (0 shut .. 1 open); the wheel turn (radians); the
 * windmill's sail turn; the gush and pool follow the opening */
export const floodRig = (level: (t: number) => number, open: (t: number) => number, crank: (t: number) => number = () => 0, sails: (t: number) => number = () => 0, pool: (t: number) => number = () => 0): Rig => (ctx) => {
  const e = ctx.set.extra, fl = e.flood as THREE.Mesh, gm = (e.gush as THREE.Mesh).material as THREE.MeshBasicMaterial, pm = e.pool as THREE.Mesh;
  const fm = (fl.material as THREE.MeshLambertMaterial).map!, cm = ((e.canal as THREE.Mesh).material as THREE.MeshLambertMaterial).map!;
  return (t) => {
    FLOOD.y = level(t); fl.position.y = FLOOD.y; fl.visible = FLOOD.y > -0.05;
    fm.offset.set(-t * 0.004, t * 0.003); cm.offset.set(-t * 0.01, 0);
    const u = clamp01(open(t)); (e.gate as THREE.Group).position.y = 1.45 * u;
    (e.wheel as THREE.Group).rotation.z = crank(t);
    gm.opacity = u; (e.gush as THREE.Mesh).visible = u > 0.02; gm.map!.offset.set(0, t * 1.6);
    const pr = pool(t); pm.visible = pr > 0.05 && FLOOD.y < 0.03; pm.scale.set(pr, pr * 0.8, 1); (pm.material as THREE.MeshBasicMaterial).map!.offset.set(t * 0.05, 0);
    (e.sails as THREE.Group).rotation.z = sails(t);
  };
};

/** the explainer: a cut-away slice of the polder (x -12..12): soil layers, two ditches, the water over it all (the
 * story sets its height), a plain sky card behind. extra.water (the water slab), extra.ditchWater */
export const SEC = { x0: -12, x1: 12, ditches: [-4.5, 5.5], dw: 1.8, dd: 1.6, z: 1.6 };
export function sectionSet(): SetBuild {
  const root = new THREE.Group();
  const soil = (top: string, layers: string[]) => { const [c, g] = canvas(64, 256); const n = layers.length; layers.forEach((col, i) => { g.fillStyle = col; g.fillRect(0, (i * 256) / n, 64, 256 / n + 1); }); g.fillStyle = top; g.fillRect(0, 0, 64, 20); return tex(c); };
  const earth = lambert({ map: soil("#5f9a3c", ["#7a5a3a", "#6a4a30", "#5a3e28", "#4a3220"]) });
  const D = 3.2;   // soil depth shown
  // soil blocks between the ditches
  const xs = [SEC.x0, ...SEC.ditches.flatMap((x) => [x - SEC.dw / 2, x + SEC.dw / 2]), SEC.x1];
  for (let i = 0; i < xs.length; i += 2) box(root, earth, xs[i + 1] - xs[i], D, 2 * SEC.z, (xs[i] + xs[i + 1]) / 2, -D / 2, 0);
  for (const x of SEC.ditches) box(root, earth, SEC.dw, D - SEC.dd, 2 * SEC.z, x, -SEC.dd - (D - SEC.dd) / 2, 0);
  // grass tufts on the field tops (under the water)
  const tuft = lambert({ color: "#4f8a3c" });
  for (let x = SEC.x0 + 0.4; x < SEC.x1; x += 0.7) { if (SEC.ditches.some((d) => Math.abs(x - d) < SEC.dw / 2 + 0.1)) continue; const m = new THREE.Mesh(new THREE.ConeGeometry(0.07, 0.18, 5), tuft); m.position.set(x, 0.09, SEC.z - 0.1); root.add(m); }
  const water = new THREE.Mesh(new THREE.BoxGeometry(SEC.x1 - SEC.x0, 1, 2 * SEC.z + 0.02), new THREE.MeshLambertMaterial({ color: "#3a8ac8", transparent: true, opacity: 0.5, depthWrite: false }));
  water.position.set(0, 0.5, 0); water.renderOrder = 2; root.add(water);
  const top = new THREE.Mesh(new THREE.PlaneGeometry(SEC.x1 - SEC.x0, 2 * SEC.z), new THREE.MeshLambertMaterial({ map: richWater([6, 1]), transparent: true, opacity: 0.85, depthWrite: false })); top.rotation.x = -Math.PI / 2; top.renderOrder = 3; root.add(top);
  const ditchW: THREE.Mesh[] = SEC.ditches.map((x) => { const m = new THREE.Mesh(new THREE.BoxGeometry(SEC.dw, SEC.dd, 2 * SEC.z + 0.02), new THREE.MeshLambertMaterial({ color: "#2a6aa8", transparent: true, opacity: 0.6, depthWrite: false })); m.position.set(x, -SEC.dd / 2, 0); m.renderOrder = 2; root.add(m); return m; });
  // the back: a pale sky card and a strip of flooded polder behind the slice
  const [c, g] = canvas(16, 256); const gr = g.createLinearGradient(0, 0, 0, 256); gr.addColorStop(0, "#9cc8ec"); gr.addColorStop(1, "#e8f2f8"); g.fillStyle = gr; g.fillRect(0, 0, 16, 256);
  const sky = new THREE.Mesh(new THREE.PlaneGeometry(200, 80), new THREE.MeshBasicMaterial({ map: tex(c), fog: false })); sky.position.set(0, 20, -60); root.add(sky);
  const back = new THREE.Mesh(new THREE.PlaneGeometry(200, 60), lambert({ map: richWater([30, 10]) })); back.rotation.x = -Math.PI / 2; back.position.set(0, 0.0, -32); root.add(back);
  const key = makeKey(root, [-8, 16, 14], [0, 0, 0], 20);
  return { root, key, glows: [], extra: { water, top, ditchW } as unknown as Record<string, THREE.Object3D>, fogScale: 6 };
}
/** the section's water height (m above the field tops) */
export const sectionWater = (h: (t: number) => number): Rig => (ctx) => {
  const w = ctx.set.extra.water as THREE.Mesh, top = ctx.set.extra.top as THREE.Mesh;
  return (t) => { const y = Math.max(0.01, h(t)); w.scale.y = y; w.position.y = y / 2; top.position.y = y + 0.005; ((top.material as THREE.MeshLambertMaterial).map!).offset.set(-t * 0.02, 0); };
};

/** models placed by a function of time (pos, yaw, and an optional per-frame update with the object) */
export const propRig = (make: () => THREE.Object3D, at: (t: number) => V3 | null, yaw: (t: number) => number = () => 0, upd?: (o: THREE.Object3D, t: number) => void): Rig => (ctx) => {
  const o = make(); ctx.root.add(o);
  return (t) => { const p = at(t); o.visible = !!p; if (!p) return; o.position.set(...p); o.rotation.y = yaw(t); upd?.(o, t); };
};
/** a crowd of models: n copies at spots(t)[i] */
export const crowdRig = (make: (i: number) => THREE.Object3D, spots: (t: number) => (V3 | null)[], yaw: (t: number, i: number) => number = () => 0, upd?: (o: THREE.Object3D, t: number, i: number) => void): Rig => (ctx) => {
  const os: THREE.Object3D[] = [];
  return (t) => {
    const ps = spots(t);
    while (os.length < ps.length) { const o = make(os.length); ctx.root.add(o); os.push(o); }
    os.forEach((o, i) => { const p = ps[i]; o.visible = !!p; if (!p) return; o.position.set(...p); o.rotation.y = yaw(t, i); upd?.(o, t, i); });
  };
};
/** a hat floating on the water (the rider's morion, upside down, bobbing) */
export function floatingHat(): THREE.Group {
  const g = new THREE.Group(), steel = mat("steel", () => lambert({ color: "#9aa2b4" }));
  const cap = new THREE.Mesh(new THREE.SphereGeometry(0.3, 14, 8, 0, Math.PI * 2, 0, Math.PI / 2), steel); cap.rotation.x = Math.PI; cap.position.y = 0.12; g.add(cap);
  const brim = new THREE.Mesh(new THREE.TorusGeometry(0.32, 0.04, 6, 18), steel); brim.rotation.x = Math.PI / 2; brim.position.y = 0.12; g.add(brim);
  const plume = new THREE.Mesh(new THREE.SphereGeometry(0.1, 8, 6), mat("plume", () => lambert({ color: "#c8382c" }))); plume.position.set(0, 0.16, 0.18); g.add(plume);
  return g;
}
export { NOINK };
