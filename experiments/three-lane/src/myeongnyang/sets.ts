// The places of story-myeongnyang as 3D sets (our own code, on the kit's set helpers): the Myeongnyang (Uldolmok)
// strait between Jindo island (-z) and the mainland (+z), its narrow gap at x 30-110, Yi's thirteen panokseon and
// the Japanese fleet of 133; the current is a band of painted streaks over the water that the story scrolls (and stops,
// and turns); whirlpools spin in the gap. Ships are built once per type, merged per material, and cloned.
import * as THREE from "three";
import { mergeGeometries } from "three/examples/jsm/utils/BufferGeometryUtils.js";
import { NOINK } from "../ink";
import { SetBuild, lambert, basic, box, glowSprite, skyDome, makeKey } from "../kit/sets";
import { richWater, grainPlanks } from "../kit/dressing";
import { rng } from "../paint";
import type { V3, Rig } from "../kit/Stage";
import { Flame, Rising } from "../kit/fx";

const canvas = (w: number, h: number) => { const c = document.createElement("canvas"); c.width = w; c.height = h; return [c, c.getContext("2d")!] as const; };
const tex = (c: HTMLCanvasElement, repeat: [number, number] = [1, 1]) => { const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(...repeat); t.anisotropy = 8; return t; };
const sm = (a: number, b: number, x: number) => { const u = Math.min(1, Math.max(0, (x - a) / (b - a))); return u * u * (3 - 2 * u); };

// ------------------------------------------------------------------------------------------------ the strait
/** half-width of open water at x: the gap (80 m) at x 30-110, wider toward Yi's side (x < 0) and the bay (x > 200) */
export const halfW = (x: number) => 40 + 95 * sm(110, 230, x) + 75 * sm(30, -60, x);
const n2 = (x: number, z: number) => 0.5 + 0.25 * Math.sin(x * 0.031 + z * 0.017) + 0.15 * Math.sin(x * 0.083 - z * 0.061 + 1.3) + 0.1 * Math.sin(x * 0.19 + z * 0.23);
/** land height at (x, z) (y 0 = the sea; below the shore line the terrain dips under the water) */
export function landH(x: number, z: number) {
  const d = Math.abs(z) - halfW(x);
  if (d < 0) return -4;
  return 1.2 + 34 * (1 - Math.exp(-d / 38)) * (0.55 + 0.8 * n2(x, z)) + (d < 6 ? -1.2 * (1 - d / 6) : 0);
}
export const DECK_K = 3.4, DECK_J = 3.2;    // deck heights (panokseon upper deck, Japanese deck)

function terrain(root: THREE.Object3D, night: boolean) {
  const W = 1000, D = 760, nx = 200, nz = 152, cx = 110;
  const g = new THREE.PlaneGeometry(W, D, nx, nz); g.rotateX(-Math.PI / 2);
  const p = g.getAttribute("position") as THREE.BufferAttribute;
  const col = new Float32Array(p.count * 3);
  const grass = new THREE.Color(night ? "#3f5a4a" : "#6e9a4c"), dark = new THREE.Color(night ? "#2c4038" : "#4d7a3c"),
    rock = new THREE.Color(night ? "#585868" : "#8c8478"), sand = new THREE.Color(night ? "#7a7468" : "#d8c49a");
  const c = new THREE.Color();
  for (let i = 0; i < p.count; i++) {
    const x = p.getX(i) + cx, z = p.getZ(i), h = landH(x, z);
    p.setX(i, x); p.setY(i, h);
    const d = Math.abs(z) - halfW(x);
    if (d < 5) c.copy(rock).lerp(sand, Math.max(0, d) / 5 * 0.4);
    else c.copy(grass).lerp(dark, Math.min(1, Math.max(0, n2(x * 2.1, z * 1.7) - 0.3) * 1.6)).lerp(rock, Math.max(0, 1 - (d - 5) / 12) * 0.7);
    col.set([c.r, c.g, c.b], i * 3);
  }
  g.setAttribute("color", new THREE.BufferAttribute(col, 3)); g.computeVertexNormals();
  const m = new THREE.Mesh(g, lambert({ vertexColors: true })); m.receiveShadow = true; root.add(m);
  // pines: merged cones on the slopes, rocks along the shore
  const r = rng(31), cones: THREE.BufferGeometry[] = [], rocks: THREE.BufferGeometry[] = [];
  for (let k = 0; k < 900; k++) {
    const x = cx - W / 2 + r() * W, z = (r() < 0.5 ? -1 : 1) * (halfW(x) + 8 + r() * 200), h = landH(x, z);
    if (h < 4 || n2(x * 3, z * 3) < 0.42) continue;
    const s = 2.2 + r() * 2.6, cg = new THREE.ConeGeometry(s * 0.45, s * 1.6, 6); cg.translate(x, h + s * 0.8, z); cones.push(cg);
  }
  for (let k = 0; k < 160; k++) {
    const x = cx - W / 2 + r() * W, side = r() < 0.5 ? -1 : 1, z = side * (halfW(x) + r() * 4), s = 1.2 + r() * 2.8;
    const rg = new THREE.DodecahedronGeometry(s, 0); rg.scale(1.3, 0.7, 1); rg.translate(x, 0.2 + s * 0.2, z); rocks.push(rg);
  }
  const pine = new THREE.Mesh(mergeGeometries(cones), lambert({ color: night ? "#22382e" : "#356040" })); pine.castShadow = true; root.add(pine);
  const rk = new THREE.Mesh(mergeGeometries(rocks), lambert({ color: night ? "#4c4c5a" : "#7c766e" })); rk.castShadow = true; root.add(rk);
}

/** a streak texture: white dashes along +u (the current), transparent between */
let streakT: THREE.CanvasTexture | null = null;
function streaks() {
  if (streakT) return streakT;
  const S = 512, [c, g] = canvas(S, S), r = rng(77);
  g.lineCap = "round";
  for (let i = 0; i < 150; i++) {
    const x = r() * S, y = r() * S, w = 30 + r() * 110;
    g.strokeStyle = `rgba(245,252,255,${0.35 + r() * 0.45})`; g.lineWidth = 2 + r() * 4;
    g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + w / 2, y + (r() - 0.5) * 10, x + w, y); g.stroke();
    if (x + w > S) { g.beginPath(); g.moveTo(x - S, y); g.quadraticCurveTo(x - S + w / 2, y, x - S + w, y); g.stroke(); }
  }
  streakT = tex(c, [10, 6]); return streakT;
}
/** a whirlpool texture: spiral foam arms */
let whirlT: THREE.CanvasTexture | null = null;
function whirl() {
  if (whirlT) return whirlT;
  const S = 256, [c, g] = canvas(S, S);
  g.translate(S / 2, S / 2); g.lineCap = "round";
  for (let arm = 0; arm < 4; arm++) {
    g.beginPath();
    for (let k = 0; k <= 60; k++) { const u = k / 60, a = arm * Math.PI / 2 + u * 5.2, rr = 12 + u * 110; const x = Math.cos(a) * rr, y = Math.sin(a) * rr; k ? g.lineTo(x, y) : g.moveTo(x, y); }
    g.strokeStyle = "rgba(245,252,255,0.75)"; g.lineWidth = 7; g.stroke();
  }
  g.fillStyle = "rgba(20,60,80,0.45)"; g.beginPath(); g.arc(0, 0, 14, 0, 7); g.fill();
  whirlT = tex(c); return whirlT;
}

export type StraitOpts = { night?: boolean; dusk?: boolean; explain?: boolean; fog?: number };
/** the strait: water, the two shores, the sky; extra.water (kit wave life), extra.current (the streak band) */
export function straitSet(o: StraitOpts = {}): SetBuild {
  const root = new THREE.Group(), glows: THREE.Object3D[] = [];
  const water = new THREE.Mesh(new THREE.PlaneGeometry(1600, 1600), lambert({ map: richWater([90, 90], { deep: !!(o.night || o.explain) }) }));
  water.rotation.x = -Math.PI / 2; water.position.set(100, 0, 0); water.receiveShadow = true; root.add(water);
  terrain(root, !!(o.night || o.explain));
  const sky = o.night || o.explain ? skyDome(root, "#0b0f33", "#1f2a66", "#3a4a86", 1500, 160)
    : o.dusk ? skyDome(root, "#3d4688", "#d8785c", "#f3b47c", 1500)
    : skyDome(root, "#3f7fd0", "#9cc4e8", "#f3d8ae", 1500);
  // the current: a band of streaks over the strait's water (scrolled by currentRig); never inked
  // The streak and pool planes sit a few cm over the water; from a high camera (the explainer map, 200 m up, near 0.05)
  // that is under one depth step, so they z-fought the water and dropped out on single frames. A polygon offset pulls
  // them toward the camera by a fixed number of depth steps at any distance, and the explainer (no ships) also lifts them.
  const lift = o.explain ? 0.5 : 0;
  const zfix = { polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -8 };
  const cur = new THREE.Mesh(new THREE.PlaneGeometry(700, 300), new THREE.MeshBasicMaterial({ map: streaks().clone(), transparent: true, depthWrite: false, opacity: 0.0, fog: true, ...zfix }));
  (cur.material as THREE.MeshBasicMaterial).map!.needsUpdate = true;
  cur.rotation.x = -Math.PI / 2; cur.position.set(110, 0.05 + lift, 0); cur.layers.set(NOINK); cur.renderOrder = 2; root.add(cur);
  // whirlpools in the gap
  const pools = new THREE.Group(); root.add(pools);
  for (const [x, z, s] of [[52, -20, 16], [84, 16, 20], [70, -2, 12], [104, -14, 14], [40, 22, 11]] as [number, number, number][]) {
    const m = new THREE.Mesh(new THREE.PlaneGeometry(s, s), new THREE.MeshBasicMaterial({ map: whirl(), transparent: true, depthWrite: false, fog: true, ...zfix }));
    m.rotation.x = -Math.PI / 2; m.position.set(x, 0.07 + lift, z); m.layers.set(NOINK); m.renderOrder = 3; pools.add(m);
  }
  const key = o.night || o.explain ? makeKey(root, [-60, 80, -40], [40, 0, 0], 90) : o.dusk ? makeKey(root, [-160, 50, 60], [40, 0, 0], 90) : makeKey(root, [-90, 110, 70], [40, 0, 0], 90);
  key.shadow.camera.far = 400;
  return { root, key, glows, sky, extra: { water, current: cur, pools }, fogScale: o.fog ?? 10 };
}

/** current streaks and whirlpools: phase(t) = how far the water has moved (m, +x positive), amp(t) 0..1 = how much white
 * water shows (0 at slack). The streaks drift with the phase; the pools spin with it. */
export const currentRig = (phase: (t: number) => number, amp: (t: number) => number): Rig => (ctx) => {
  const cur = ctx.set.extra.current as THREE.Mesh, pools = ctx.set.extra.pools as THREE.Group;
  const mat = cur.material as THREE.MeshBasicMaterial;
  return (t) => {
    const a = amp(t), ph = phase(t);
    mat.opacity = 0.9 * a; cur.visible = a > 0.01;
    mat.map!.offset.set(-ph / 70, 0);
    pools.children.forEach((m, i) => { const mm = m as THREE.Mesh; mm.rotation.z = (i % 2 ? 1 : 1.2) * ph * 0.05; (mm.material as THREE.MeshBasicMaterial).opacity = a; mm.visible = a > 0.02; mm.scale.setScalar(0.6 + 0.4 * a); });
  };
};

// ------------------------------------------------------------------------------------------------ ships
function shieldWall(base: string, trim: string, rows = 1, cols = 14, emblem = false) {
  const [c, g] = canvas(512, 96 * rows);
  g.fillStyle = base; g.fillRect(0, 0, 512, 96 * rows);
  const w = 512 / cols;
  for (let r = 0; r < rows; r++) for (let k = 0; k < cols; k++) {
    g.fillStyle = trim; g.fillRect(k * w + 3, r * 96 + 6, w - 6, 84);
    g.strokeStyle = "rgba(20,10,10,0.6)"; g.lineWidth = 3; g.strokeRect(k * w + 3, r * 96 + 6, w - 6, 84);
    if (emblem) { g.fillStyle = "rgba(240,230,200,0.85)"; g.beginPath(); g.arc(k * w + w / 2, r * 96 + 48, w * 0.22, 0, 7); g.fill(); }
    else { g.fillStyle = "rgba(20,10,10,0.75)"; g.fillRect(k * w + w / 2 - 3, r * 96 + 30, 6, 30); }   // the gun / bow port
  }
  return tex(c);
}
function sailTex(base: string, batten: string, n: number, mon = false) {
  const [c, g] = canvas(256, 320);
  g.fillStyle = base; g.fillRect(0, 0, 256, 320);
  g.strokeStyle = batten; g.lineWidth = 7;
  for (let k = 1; k < n; k++) { g.beginPath(); g.moveTo(0, (k * 320) / n); g.lineTo(256, (k * 320) / n); g.stroke(); }
  if (mon) { g.strokeStyle = "#1a1a24"; g.lineWidth = 16; g.beginPath(); g.arc(128, 150, 62, 0, 7); g.stroke(); g.fillStyle = "#1a1a24"; g.fillRect(118, 92, 20, 118); }
  g.strokeStyle = "rgba(0,0,0,0.25)"; g.lineWidth = 6; g.strokeRect(3, 3, 250, 314);
  return tex(c);
}
function flagTex(a: string, b: string) {
  const [c, g] = canvas(64, 256);
  g.fillStyle = a; g.fillRect(0, 0, 64, 256); g.fillStyle = b; g.fillRect(0, 0, 64, 40); g.fillRect(0, 216, 64, 40);
  return tex(c);
}
/** merge a group's meshes by material into one mesh per material (cheap to clone and draw) */
function mergeByMat(g: THREE.Group): THREE.Group {
  g.updateMatrixWorld(true);
  const by = new Map<THREE.Material, THREE.BufferGeometry[]>();
  g.traverse((o) => {
    const m = o as THREE.Mesh; if (!m.isMesh) return;
    const geo = m.geometry.clone().applyMatrix4(m.matrixWorld);
    const ng = geo.index ? geo : geo; for (const k of Object.keys(ng.attributes)) if (!["position", "normal", "uv"].includes(k)) ng.deleteAttribute(k);
    const mat = m.material as THREE.Material; (by.get(mat) ?? by.set(mat, []).get(mat)!).push(ng.index ? ng.toNonIndexed() : ng);
  });
  const out = new THREE.Group();
  for (const [mat, geos] of by) {
    const mm = new THREE.Mesh(mergeGeometries(geos), mat); mm.castShadow = true; mm.receiveShadow = true;
    if ((mat as THREE.Material & { userData: Record<string, unknown> }).userData.noink) mm.layers.set(NOINK);
    out.add(mm);
  }
  return out;
}
const M: Record<string, THREE.Material> = {};
const mat = (k: string, f: () => THREE.Material) => (M[k] ??= f());

/** a Korean panokseon (our own model): a broad flat-bottomed hull, the upper deck enclosed by red shield walls with gun
 * ports, a command pavilion on top, two masts with battened sails, oars; deck top at DECK_K. Bow toward +x. */
export function panokseon(o: { flagship?: boolean; sails?: number } = {}): THREE.Group {
  const g = new THREE.Group();
  const hull = mat("kHull", () => lambert({ map: grainPlanks([3, 1], { hue: 26, light: 34, boards: 5, seed: 4 }) }));
  const wall = mat("kWall", () => lambert({ map: shieldWall("#7a1f1a", "#c8402e", 1, 16) }));
  const deck = mat("kDeck", () => lambert({ map: grainPlanks([4, 2], { hue: 28, light: 40, boards: 8, seed: 6 }) }));
  const red = mat("kRed", () => lambert({ color: "#a8342a" })), roof = mat("kRoof", () => lambert({ color: "#3a3040" }));
  const wood = mat("kWood", () => lambert({ color: "#5a3a24" }));
  const sail = mat("kSail", () => lambert({ map: sailTex("#c9a878", "#6a4a2c", 7), side: THREE.DoubleSide }));
  // hull: a broad box, a raked flat bow and a squared stern
  box(g, hull, 14, 2.0, 6.0, 0, 0.6, 0);
  const bow = new THREE.Mesh(new THREE.BoxGeometry(3, 2.0, 5.4), hull); bow.position.set(8.1, 0.9, 0); bow.rotation.z = 0.35; g.add(bow);
  box(g, wall, 15, 1.6, 6.8, 0.4, 2.5, 0);                       // the shield wall round the upper deck
  for (const z of [-3.45, 3.45]) box(g, red, 15.2, 0.5, 0.25, 0.4, DECK_K + 0.25, z);   // red rails (read from above)
  box(g, red, 0.25, 0.5, 7.0, 7.95, DECK_K + 0.25, 0); box(g, red, 0.25, 0.5, 7.0, -7.15, DECK_K + 0.25, 0);
  box(g, deck, 15.2, 0.2, 7.0, 0.4, DECK_K - 0.1, 0);              // the upper deck floor
  // the command pavilion (jangdae) at the stern
  for (const [x, z] of [[-5.8, -1.2], [-3.4, -1.2], [-5.8, 1.2], [-3.4, 1.2]]) box(g, red, 0.22, 2.0, 0.22, x, DECK_K + 1.0, z);
  box(g, deck, 3.0, 0.16, 3.0, -4.6, DECK_K + 2.0, 0);
  const rf = new THREE.Mesh(new THREE.ConeGeometry(2.6, 1.2, 4), roof); rf.rotation.y = Math.PI / 4; rf.position.set(-4.6, DECK_K + 2.7, 0); g.add(rf);
  // masts and sails
  const sails = o.sails ?? 1;
  for (const x of [2.6, -1.0]) {
    if (sails >= 0) box(g, wood, 0.3, 11, 0.3, x, DECK_K + 5.5, 0);
    if (sails > 0) { const s = new THREE.Mesh(new THREE.PlaneGeometry(4.8, 6.2 * sails), sail); s.rotation.y = Math.PI / 2; s.position.set(x + 0.2, DECK_K + 7.6 - 3.1 * (1 - sails), 0); g.add(s); }
    else if (sails === 0) { const roll = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.35, 5.0, 8), mat("kRoll", () => lambert({ color: "#b8956a" }))); roll.rotation.x = Math.PI / 2; roll.position.set(x + 0.3, DECK_K + 1.6, 0); g.add(roll); }
  }
  // oars, eight a side, into the water
  for (const side of [-1, 1]) for (let k = 0; k < 8; k++) {
    const oar = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.14, 4.2), wood);
    oar.position.set(-5 + k * 1.4, 0.9, side * 4.4); oar.rotation.x = side * 0.55; g.add(oar);
  }
  const merged = mergeByMat(g);
  // flags (kept separate: they wave)
  const flagM = mat(o.flagship ? "kFlagF" : "kFlag", () => lambert({ map: flagTex(o.flagship ? "#d23a2a" : "#2f5f9e", o.flagship ? "#f0c040" : "#e8e0c8"), side: THREE.DoubleSide }));
  const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 5, 6), wood); pole.position.set(-6.2, DECK_K + 4.5, 0); merged.add(pole);
  const fl = new THREE.Mesh(new THREE.PlaneGeometry(o.flagship ? 2.6 : 1.6, o.flagship ? 3.4 : 2.2), flagM);
  fl.position.set(-6.2 - (o.flagship ? 1.3 : 0.8), DECK_K + 5.6 + (o.flagship ? 0.2 : 0.5), 0); fl.name = "flag"; merged.add(fl);
  return merged;
}

/** a Japanese sekibune / atakebune (our own model): a narrower hull with a raked bow, a boxed deckhouse with shield
 * walls, one mast with a white square sail and a black ring crest, tall nobori banners; deck top at DECK_J; bow +x */
export function atake(o: { banners?: number; seed?: number } = {}): THREE.Group {
  const g = new THREE.Group(), r = rng(o.seed ?? 3);
  const hull = mat("jHull", () => lambert({ map: grainPlanks([3, 1], { hue: 34, light: 46, boards: 5, seed: 8 }) }));
  const wall = mat("jWall", () => lambert({ map: shieldWall("#2a2a36", "#b89a6a", 1, 14, false) }));
  const deck = mat("jDeck", () => lambert({ map: grainPlanks([4, 2], { hue: 36, light: 58, boards: 8, seed: 9 }) }));
  const dark = mat("jDark", () => lambert({ color: "#2a2a36" })), wood = mat("jWood", () => lambert({ color: "#6a4a2c" }));
  const sail = mat("jSail", () => lambert({ map: sailTex("#ece6d8", "#b9b1a0", 6, true), side: THREE.DoubleSide }));
  box(g, hull, 12, 1.8, 4.4, 0, 0.6, 0);
  const bow = new THREE.Mesh(new THREE.BoxGeometry(3.4, 1.4, 3.6), hull); bow.position.set(7.2, 1.2, 0); bow.rotation.z = 0.5; g.add(bow);
  box(g, wall, 11, 1.5, 4.8, -0.4, 2.3, 0);
  box(g, deck, 11.2, 0.2, 5.0, -0.4, DECK_J - 0.1, 0);
  box(g, dark, 3.2, 1.6, 3.0, -4.0, DECK_J + 0.8, 0);                // the stern cabin
  box(g, wood, 0.28, 10, 0.28, 0.8, DECK_J + 5, 0);
  const s = new THREE.Mesh(new THREE.PlaneGeometry(4.4, 5.4), sail); s.rotation.y = Math.PI / 2; s.position.set(1.0, DECK_J + 6.4, 0); g.add(s);
  for (const side of [-1, 1]) for (let k = 0; k < 6; k++) {
    const oar = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.12, 3.4), wood); oar.position.set(-4 + k * 1.5, 0.9, side * 3.2); oar.rotation.x = side * 0.6; g.add(oar);
  }
  const merged = mergeByMat(g);
  // nobori banners along the rails (tall, thin, coloured)
  const cols = [["#f2efe6", "#1a1a24"], ["#b8342c", "#f2efe6"], ["#1a1a24", "#e2b33c"], ["#f2efe6", "#b8342c"]];
  const nb = o.banners ?? 4;
  for (let k = 0; k < nb; k++) {
    const [a, b] = cols[Math.floor(r() * cols.length)];
    const fm = mat(`nob${a}${b}`, () => lambert({ map: flagTex(a, b), side: THREE.DoubleSide }));
    const x = -4.5 + (k / Math.max(1, nb - 1)) * 9, z = (k % 2 ? 1 : -1) * 2.2;
    const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 4.6, 5), wood); pole.position.set(x, DECK_J + 2.3, z); merged.add(pole);
    const f = new THREE.Mesh(new THREE.PlaneGeometry(0.7, 2.8), fm); f.position.set(x - 0.38, DECK_J + 3.2, z); f.name = "flag"; merged.add(f);
  }
  return merged;
}

// ------------------------------------------------------------------------------------------------ fleets
export type Berth = { x: number; z: number; yaw: number; k: number };
/** Yi's thirteen at the west mouth: the flagship (k 0) at the back, his twelve in two columns ahead of it */
export function koreanLine(x0 = 16): Berth[] {
  const out: Berth[] = [{ x: x0, z: 0, yaw: 0, k: 0 }];
  for (let k = 1; k <= 12; k++) { const p = Math.ceil(k / 2); out.push({ x: x0 + 10 + 7.5 * p, z: (k % 2 ? 1 : -1) * (11 + 0.5 * p), yaw: 0, k }); }
  return out;
}
/** the 133: rows through the gap and back into the bay, as many abreast as the water allows */
export function japaneseFleet(x0 = 64, n = 133): Berth[] {
  const r = rng(11), out: Berth[] = [];
  for (let x = x0; out.length < n; x += 15 + r() * 3) {
    const hw = halfW(x) - 11, per = Math.max(2, Math.floor((2 * hw) / 16));
    for (let k = 0; k < per && out.length < n; k++) {
      const z = -hw + (k + 0.5) * ((2 * hw) / per) + (r() - 0.5) * 5;
      out.push({ x: x + (r() - 0.5) * 6, z, yaw: Math.PI + (r() - 0.5) * 0.25, k: out.length });
    }
  }
  return out;
}
/** place cloned ships at berths, moved by move(t, b) each frame; returns the groups (index = berth k) */
export const fleetRig = (make: (b: Berth) => THREE.Group, berths: Berth[], move?: (t: number, b: Berth) => { dx?: number; dz?: number; dyaw?: number; heel?: number }, onMake?: (gs: THREE.Group[]) => void): Rig => (ctx) => {
  const gs = berths.map((b) => { const s = make(b); s.position.set(b.x, 0, b.z); s.rotation.y = b.yaw; ctx.root.add(s); return s; });
  onMake?.(gs);
  return (t) => berths.forEach((b, i) => {
    const m = move ? move(t, b) : {};
    const s = gs[i];
    s.position.set(b.x + (m.dx ?? 0), 0.06 * Math.sin(t * 1.3 + b.k), b.z + (m.dz ?? 0));
    s.rotation.set(0, b.yaw + (m.dyaw ?? 0), (m.heel ?? 0) + 0.012 * Math.sin(t * 1.1 + b.k * 0.7));
    s.traverse((o) => { if (o.name === "flag") o.rotation.y = 0.25 * Math.sin(t * 3 + b.k + o.position.x); });
  });
};
// shared prototypes (geometry built once per type; clones share it)
const PKs = new Map<string, THREE.Group>(); const PJ: THREE.Group[] = [];
/** furled: sails down (at anchor); the flagship at anchor also has its masts lowered */
export const korean = (flagship = false, furled = false) => { const k = `${flagship}${furled}`; if (!PKs.has(k)) PKs.set(k, panokseon({ flagship, sails: furled ? (flagship ? -1 : 0) : 1 })); return PKs.get(k)!.clone(); };
export const japanese = (k: number) => { if (!PJ.length) for (let s = 0; s < 4; s++) PJ.push(atake({ seed: 3 + s, banners: 3 + s })); return PJ[k % 4].clone(); };

/** world position of a point on a berth's deck (local x along the bow, z to port) */
export const onDeck = (b: { x: number; z: number; yaw: number }, lx: number, lz: number, y: number): V3 =>
  [b.x + Math.cos(b.yaw) * lx + Math.sin(b.yaw) * lz, y, b.z - Math.sin(b.yaw) * lx + Math.cos(b.yaw) * lz];

/** a lantern glow at p (night scenes) */
export const lanternGlows = (ps: V3[], size = 3): Rig => (ctx) => {
  for (const p of ps) { const s = glowSprite(ctx.root, [255, 190, 110], size, ...p); (s as THREE.Object3D).userData.bloom = true; ctx.set.glows.push(s);
    const l = new THREE.Mesh(new THREE.SphereGeometry(0.22, 8, 6), basic({ color: "#ffd890" })); l.position.set(...p); l.layers.set(NOINK); ctx.root.add(l); }
  return () => {};
};
export { NOINK };

// ------------------------------------------------------------------------------------------------ wrecks
/** burning wrecks: broken, listing hulls with fire and smoke ([x, z, list]); panokseon by default, or make(i) (e.g. an
 * enemy atake: japanese) */
export const wreckRig = (at: [number, number, number][], make: (i: number) => THREE.Group = () => korean(false)): Rig => (ctx) => {
  const items = at.map(([x, z, list], i) => {
    const g = make(i); g.position.set(x, -1.4, z); g.rotation.set(list * 0.5, i * 1.3, list); ctx.root.add(g);
    g.traverse((o) => { if (o.name === "flag") o.visible = false; });
    const fl = [0, 1, 2].map((k) => { const f = new Flame(4 + k, i * 3 + k); f.mesh.position.set(x - 3 + k * 3, 1.5, z + (k - 1)); ctx.root.add(f.mesh); return f; });
    const sm = new Rising(12, "smoke", 6, 40 + i); sm.group.position.set(x, 3, z); ctx.root.add(sm.group);
    const gl = glowSprite(ctx.root, [255, 150, 70], 14, x, 3, z); (gl as THREE.Object3D).userData.bloom = true; ctx.set.glows.push(gl);
    return { fl, sm };
  });
  return (t, cam) => items.forEach((it) => { it.fl.forEach((f) => f.update(t, 1, cam)); it.sm.update(t, 1, 16, 3, 8); });
};

// ------------------------------------------------------------------------------------------------ the throne hall
/** the Joseon throne hall at night (our own set): red pillars, a painted beam frieze, paper lattice doors, the
 * sun-moon-five-peaks screen behind a raised throne, lamps */
export function courtSet(): SetBuild {
  const root = new THREE.Group(), glows: THREE.Object3D[] = [];
  const floor = lambert({ map: grainPlanks([6, 6], { hue: 30, light: 36, boards: 10, seed: 21 }) });
  box(root, floor, 16, 0.2, 16, 0, -0.1, 1);
  const lattice = (() => { const [c, g] = canvas(256, 256); g.fillStyle = "#e9dcb8"; g.fillRect(0, 0, 256, 256); g.strokeStyle = "#7a4a2c"; g.lineWidth = 6;
    for (let k = 0; k <= 8; k++) { g.beginPath(); g.moveTo(k * 32, 0); g.lineTo(k * 32, 256); g.stroke(); g.beginPath(); g.moveTo(0, k * 32); g.lineTo(256, k * 32); g.stroke(); } return tex(c, [3, 2]); })();
  const doors = lambert({ map: lattice }), red = lambert({ color: "#a8322a" }), green = lambert({ color: "#2f7a5e" });
  box(root, doors, 0.3, 6, 16, -8, 3, 1); box(root, doors, 0.3, 6, 16, 8, 3, 1); box(root, doors, 16, 6, 0.3, 0, 3, 9);
  box(root, lambert({ color: "#5a2a22" }), 16, 6, 0.3, 0, 3, -6.6);
  // the screen: red sun, white moon, five blue-green peaks, waterfalls, waves, pines
  const [c, g] = canvas(1024, 512);
  g.fillStyle = "#1d3a5c"; g.fillRect(0, 0, 1024, 512);
  for (const [x, h] of [[120, 300], [300, 380], [512, 440], [724, 380], [904, 300]]) { g.fillStyle = "#2f8a6e"; g.beginPath(); g.moveTo(x - 150, 420); g.quadraticCurveTo(x, 420 - h * 1.4, x + 150, 420); g.fill(); g.strokeStyle = "#e8d8a8"; g.lineWidth = 6; g.stroke(); }
  g.fillStyle = "#d8392b"; g.beginPath(); g.arc(200, 110, 52, 0, 7); g.fill();
  g.fillStyle = "#f2efe6"; g.beginPath(); g.arc(824, 110, 52, 0, 7); g.fill();
  g.fillStyle = "#2a6fa0"; g.fillRect(0, 420, 1024, 92);
  g.strokeStyle = "#e8f0f8"; g.lineWidth = 5; for (let x = 0; x < 1024; x += 48) { g.beginPath(); g.arc(x + 24, 470, 22, Math.PI, 0); g.stroke(); }
  g.strokeStyle = "#c9a24a"; g.lineWidth = 18; g.strokeRect(9, 9, 1006, 494);
  const screen = new THREE.Mesh(new THREE.PlaneGeometry(9, 4.5), lambert({ map: tex(c) })); screen.position.set(0, 3.2, -6.3); root.add(screen);
  // dais, throne, pillars, beams
  box(root, red, 7, 0.4, 3.6, 0, 0.2, -4.6); box(root, red, 5, 0.35, 2.6, 0, 0.55, -4.9);
  box(root, lambert({ color: "#c9a24a" }), 1.6, 1.2, 0.3, 0, 1.4, -5.4);
  for (const x of [-5.5, 5.5]) for (const z of [-5, -0.5, 4]) box(root, red, 0.5, 6, 0.5, x, 3, z);
  for (const z of [-5, -0.5, 4]) box(root, green, 12, 0.5, 0.5, 0, 5.8, z);
  for (const [x, z] of [[-4, -3.5], [4, -3.5], [-4, 2.5], [4, 2.5]]) { const s = glowSprite(root, [255, 190, 110], 3.4, x, 2.6, z); (s as THREE.Object3D).userData.bloom = true; glows.push(s);
    box(root, lambert({ color: "#e9dcb8" }), 0.5, 0.7, 0.5, x, 2.6, z); box(root, lambert({ color: "#5a3a24" }), 0.12, 2.3, 0.12, x, 1.15, z); }
  const key = makeKey(root, [3, 9, 8], [0, 1, -3], 12);
  return { root, key, glows, extra: {}, fogScale: 1.4 };
}
