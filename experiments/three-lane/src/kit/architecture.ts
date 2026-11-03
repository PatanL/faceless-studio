// Period-neutral architecture and big props built in code with painted textures (our own code). The CC0 libraries
// we can fetch officially (Poly Haven) have no walls, towers, tents, carts or market stalls, so these are modelled
// here: bevel-free boxes and lathes, but with painted courses, plank grain, striped cloth, and enough parts (ropes,
// poles, trim, goods) that they read as built things, not primitives. All feet on y = 0, facing +z.
import * as THREE from "three";
import { lambert, box, cyl } from "./sets";
import { grainPlanks, stoneCourses } from "./dressing";
import { model } from "./models";
import { rng } from "../paint";

const canvas = (w: number, h: number) => { const c = document.createElement("canvas"); c.width = w; c.height = h; return [c, c.getContext("2d")!] as const; };
const tex = (c: HTMLCanvasElement, rep: [number, number] = [1, 1]) => { const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(...rep); t.anisotropy = 4; return t; };
/** striped canvas cloth with folds (tents, awnings) */
export function cloth(a: string, b: string, stripes = 8, rep: [number, number] = [1, 1]) {
  const [c, g] = canvas(256, 256);
  for (let k = 0; k < stripes; k++) { g.fillStyle = k % 2 ? b : a; g.fillRect((k * 256) / stripes, 0, 256 / stripes + 1, 256); }
  for (let k = 0; k < 10; k++) { g.fillStyle = `rgba(40,25,50,${0.05 + (k % 3) * 0.03})`; g.fillRect(k * 26 + 6, 0, 6, 256); }      // folds
  const grd = g.createLinearGradient(0, 0, 0, 256); grd.addColorStop(0, "rgba(255,245,220,0.18)"); grd.addColorStop(1, "rgba(30,20,60,0.22)");
  g.fillStyle = grd; g.fillRect(0, 0, 256, 256);
  g.fillStyle = "rgba(30,20,40,0.5)"; g.fillRect(0, 244, 256, 12);                                                     // a hem
  return tex(c, rep);
}
/** sun-dried mud brick (houses, low walls) */
export function mudBrick(rep: [number, number] = [1, 1], seed = 3, base = "#d9b98a") {
  const [c, g] = canvas(256, 256), r = rng(seed);
  g.fillStyle = base; g.fillRect(0, 0, 256, 256);
  for (let y = 0, k = 0; y < 256; y += 32, k++) for (let x = (k % 2) * -24; x < 256; x += 48) {
    g.fillStyle = `rgba(${150 + r() * 40},${110 + r() * 30},${70 + r() * 20},0.35)`; g.fillRect(x + 2, y + 2, 44, 28);
    g.strokeStyle = "rgba(90,60,40,0.45)"; g.lineWidth = 2; g.strokeRect(x + 2, y + 2, 44, 28);
  }
  for (let k = 0; k < 40; k++) { g.fillStyle = "rgba(255,240,210,0.15)"; g.beginPath(); g.arc(r() * 256, r() * 256, 4 + r() * 14, 0, 7); g.fill(); }
  return tex(c, rep);
}
const ropeM = () => lambert({ color: "#c2a06a" });
function rope(root: THREE.Object3D, a: THREE.Vector3, b: THREE.Vector3, r = 0.02) {
  const d = b.clone().sub(a), m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, d.length(), 5), ropeM());
  m.position.copy(a).add(b).multiplyScalar(0.5); m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.normalize()); root.add(m); return m;
}

/** a bell tent: canvas walls, a cone roof, a door flap, a centre pole, guy ropes and pegs */
export function tent(o: { r?: number; h?: number; a?: string; b?: string; seed?: number } = {}) {
  const g = new THREE.Group(), R = o.r ?? 2.2, H = o.h ?? 3.2;
  const m = lambert({ map: cloth(o.a ?? "#e9dcc0", o.b ?? "#d8c49c", 12, [3, 1]) });
  const wall = new THREE.Mesh(new THREE.CylinderGeometry(R, R * 1.04, H * 0.35, 18, 1, true), m); wall.position.y = H * 0.175; wall.castShadow = wall.receiveShadow = true; g.add(wall);
  const roof = new THREE.Mesh(new THREE.ConeGeometry(R * 1.12, H * 0.7, 18), m); roof.position.y = H * 0.35 + H * 0.35; roof.castShadow = roof.receiveShadow = true; g.add(roof);
  const door = new THREE.Mesh(new THREE.PlaneGeometry(R * 0.55, H * 0.42), lambert({ color: "#3a2a3e" })); door.position.set(0, H * 0.2, R * 1.02); g.add(door);
  cyl(g, lambert({ color: "#6b4426" }), 0.05, 0.6, 0, H + 0.25, 0, 6);
  const top = new THREE.Vector3(0, H * 0.62, 0);
  for (let k = 0; k < 6; k++) { const a = (k / 6) * Math.PI * 2 + 0.3; const p = new THREE.Vector3(Math.sin(a) * R * 1.9, 0.05, Math.cos(a) * R * 1.9); rope(g, top.clone().add(new THREE.Vector3(Math.sin(a) * R * 0.7, 0, Math.cos(a) * R * 0.7)), p, 0.015); cyl(g, lambert({ color: "#5b3a22" }), 0.03, 0.25, p.x, 0.12, p.z, 5); }
  return g;
}
/** a two-wheeled cart: plank bed, side boards, spoked wheels, shafts, a load (sacks, a barrel) */
export function cart(o: { load?: boolean; seed?: number } = {}) {
  const g = new THREE.Group(), wood = lambert({ map: grainPlanks([1, 1], { hue: 26, light: 40, boards: 4, seed: 41 }) }), dark = lambert({ color: "#4b2e1a" });
  box(g, wood, 1.4, 0.1, 2.2, 0, 0.75, 0); for (const s of [-1, 1]) box(g, wood, 0.08, 0.45, 2.2, s * 0.7, 1.0, 0); box(g, wood, 1.4, 0.45, 0.08, 0, 1.0, -1.1);
  for (const s of [-1, 1]) {
    const w = new THREE.Group(); w.position.set(s * 0.82, 0.55, 0.1);
    const rim = new THREE.Mesh(new THREE.TorusGeometry(0.52, 0.05, 6, 20), dark); rim.rotation.y = Math.PI / 2; w.add(rim);
    for (let k = 0; k < 6; k++) { const sp = new THREE.Mesh(new THREE.BoxGeometry(0.04, 1.0, 0.04), dark); sp.rotation.x = (k / 6) * Math.PI; w.add(sp); }
    const hub = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.09, 0.16, 10), dark); hub.rotation.z = Math.PI / 2; w.add(hub);
    w.traverse((m: THREE.Object3D) => { (m as THREE.Mesh).castShadow = true; }); g.add(w);
    const shaft = box(g, dark, 0.07, 0.07, 2.4, s * 0.45, 0.62, 2.1); shaft.rotation.x = 0.18;
  }
  box(g, dark, 1.8, 0.08, 0.08, 0, 0.55, 0.1);
  if (o.load !== false) { const b = model("barrel_03", { scale: 0.7, seed: 1, contact: false }); b.position.set(-0.3, 0.8, -0.4); g.add(b); const k = model("wicker_basket_01", { scale: 0.9, contact: false }); k.position.set(0.35, 0.8, 0.4); g.add(k); }
  return g;
}
/** a market stall: four posts, a striped awning, a counter, goods (pots, baskets, a scale of jars) */
export function stall(o: { a?: string; b?: string; seed?: number } = {}) {
  const g = new THREE.Group(), r = rng(o.seed ?? 5), wood = lambert({ map: grainPlanks([1, 1], { hue: 28, light: 44, boards: 3, seed: 51 + (o.seed ?? 0) }) });
  for (const [x, z] of [[-1.3, -0.8], [1.3, -0.8], [-1.3, 0.8], [1.3, 0.8]]) box(g, wood, 0.1, 2.4, 0.1, x, 1.2, z);
  const aw = new THREE.Mesh(new THREE.BoxGeometry(3.0, 0.06, 2.0), lambert({ map: cloth(o.a ?? "#c94b3a", o.b ?? "#efe3c8", 10) })); aw.position.y = 2.45; aw.rotation.x = -0.12; aw.castShadow = true; g.add(aw);
  for (let k = 0; k < 10; k++) { const v = new THREE.Mesh(new THREE.ConeGeometry(0.15, 0.25, 3), lambert({ color: k % 2 ? (o.a ?? "#c94b3a") : (o.b ?? "#efe3c8") })); v.rotation.x = Math.PI; v.position.set(-1.35 + k * 0.3, 2.28, 1.02); g.add(v); }
  box(g, wood, 2.6, 0.9, 0.7, 0, 0.45, 0.45); box(g, lambert({ color: "#8a5a3a" }), 2.7, 0.06, 0.8, 0, 0.92, 0.45);
  const goods = ["ceramic_pot", "wicker_basket_02", "ceramic_vase_03", "wooden_bowl_02", "planter_pot_clay"];
  for (let k = 0; k < 5; k++) { const m = model(goods[Math.floor(r() * goods.length)], { scale: 0.55 + r() * 0.2, seed: k, contact: false }); m.position.set(-1.0 + k * 0.5, 0.95, 0.45 + (r() - 0.5) * 0.2); g.add(m); }
  return g;
}
/** a stretch of city wall (len x h x thick) with coursed stone, merlons and a walk; feet on y = 0, outer face +z */
export function wallRun(len: number, h = 7, thick = 3, seed = 3) {
  const g = new THREE.Group(), st = lambert({ map: stoneCourses([Math.max(1, Math.round(len / 4)), Math.round(h / 3)], { hue: 34, light: 54, seed }) });
  box(g, st, len, h, thick, 0, h / 2, 0);
  box(g, lambert({ map: stoneCourses([Math.round(len / 3), 1], { hue: 30, light: 62, seed: seed + 1, moss: false }) }), len + 0.2, 0.35, thick + 0.25, 0, h + 0.17, 0);   // the coping
  for (let x = -len / 2 + 0.6; x < len / 2; x += 1.6) box(g, st, 0.9, 1.1, 0.5, x, h + 0.9, thick / 2 - 0.25);
  for (let x = -len / 2 + 2; x < len / 2; x += 6) box(g, lambert({ color: "#2a2238" }), 0.25, 0.8, 0.1, x, h * 0.6, thick / 2 + 0.03);   // arrow slits
  return g;
}
/** a round tower with a crenellated top and a door */
export function roundTower(r = 2.8, h = 12, seed = 5) {
  const g = new THREE.Group(), st = lambert({ map: stoneCourses([4, Math.round(h / 3)], { hue: 32, light: 52, seed }) });
  const body = new THREE.Mesh(new THREE.CylinderGeometry(r, r * 1.08, h, 24), st); body.position.y = h / 2; body.castShadow = body.receiveShadow = true; g.add(body);
  const lip = new THREE.Mesh(new THREE.CylinderGeometry(r * 1.12, r * 1.12, 0.5, 24), st); lip.position.y = h + 0.25; g.add(lip);
  for (let k = 0; k < 12; k++) { const a = (k / 12) * Math.PI * 2; box(g, st, 0.8, 1.0, 0.5, Math.sin(a) * r * 1.05, h + 1.0, Math.cos(a) * r * 1.05).rotation.y = a; }
  box(g, lambert({ map: grainPlanks([1, 1], { hue: 22, light: 34, vertical: true }) }), 1.1, 2.2, 0.2, 0, 1.1, r * 1.04);
  return g;
}
/** a flat-roofed mud-brick house with a door, window, roof beams sticking out and an awning */
export function house(o: { w?: number; h?: number; d?: number; seed?: number; base?: string } = {}) {
  const g = new THREE.Group(), w = o.w ?? 5.6, h = o.h ?? 4.6, d = o.d ?? 5;
  box(g, lambert({ map: mudBrick([2, 2], o.seed ?? 3, o.base) }), w, h, d, 0, h / 2, 0);
  box(g, lambert({ color: "#8a5a3a" }), w + 0.3, 0.3, d + 0.3, 0, h + 0.15, 0);
  for (let x = -w / 2 + 0.5; x < w / 2; x += 0.9) cyl(g, lambert({ color: "#6b4426" }), 0.07, 0.6, x, h - 0.3, d / 2 + 0.25, 6).rotation.x = Math.PI / 2;
  box(g, lambert({ map: grainPlanks([1, 1], { hue: 22, light: 34, vertical: true }) }), 1.1, 2.1, 0.1, -w * 0.18, 1.05, d / 2 + 0.06);
  box(g, lambert({ color: "#3a2a3e" }), 0.9, 0.8, 0.1, w * 0.25, 2.6, d / 2 + 0.06);
  const aw = new THREE.Mesh(new THREE.BoxGeometry(w * 0.45, 0.05, 1.2), lambert({ map: cloth("#c94b3a", "#e9dcc0", 6) })); aw.position.set(w * 0.25, 3.3, d / 2 + 0.6); aw.rotation.x = 0.25; aw.castShadow = true; g.add(aw);
  return g;
}
/** a stylised date palm: segmented trunk and painted frond cards */
export function palm(h = 6, seed = 7) {
  const g = new THREE.Group(), r = rng(seed), bark = lambert({ color: "#7a5a3a" });
  let y = 0, x = 0;
  for (let k = 0; k < 9; k++) { const s = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.2, h / 9, 8), bark); x += (r() - 0.3) * 0.08; s.position.set(x, y + h / 18, 0); s.castShadow = true; g.add(s); y += h / 9; }
  const leaf = lambert({ color: "#5f8f4a", side: THREE.DoubleSide });
  for (let k = 0; k < 9; k++) {
    const a = (k / 9) * Math.PI * 2, f = new THREE.Mesh(new THREE.PlaneGeometry(0.5, 2.6, 1, 4), leaf);
    const pos = f.geometry.attributes.position; for (let i = 0; i < pos.count; i++) pos.setZ(i, -Math.pow((pos.getY(i) + 1.3) / 2.6, 2) * 0.9);
    f.position.set(x + Math.sin(a) * 1.0, y, Math.cos(a) * 1.0); f.rotation.set(-1.0, a, 0, "YXZ"); f.castShadow = true; g.add(f);
  }
  return g;
}
/** a stone well with a timber frame and a bucket */
export function well() {
  const g = new THREE.Group(), st = lambert({ map: stoneCourses([3, 1], { hue: 32, light: 56, seed: 9 }) });
  const ring = new THREE.Mesh(new THREE.CylinderGeometry(0.9, 0.95, 0.9, 20, 1, true), st); ring.position.y = 0.45; ring.castShadow = true; g.add(ring);
  const dark = lambert({ color: "#4b2e1a" });
  for (const s of [-1, 1]) box(g, dark, 0.12, 1.9, 0.12, s * 0.85, 0.95, 0); box(g, dark, 1.9, 0.12, 0.12, 0, 1.9, 0);
  const b = model("wooden_bucket_01", { scale: 0.8, contact: false }); b.position.set(0.2, 1.1, 0); g.add(b);
  return g;
}
/** a standard: a pole and a cloth banner */
export function standard(col: string, h = 5) {
  const g = new THREE.Group(); cyl(g, lambert({ color: "#5b3a22" }), 0.06, h, 0, h / 2, 0, 6);
  const f = new THREE.Mesh(new THREE.PlaneGeometry(1.2, 0.8), lambert({ color: col, side: THREE.DoubleSide })); f.position.set(0.6, h - 0.5, 0); f.castShadow = true; g.add(f);
  return g;
}
