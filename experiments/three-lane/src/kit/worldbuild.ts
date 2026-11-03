// World building (our own code; visual track round 3, owner: "theirs has far more detail, on the objects viewers look at
// and in the background"). Reusable dressing pieces, painted backdrops, per-place dressing presets and background life.
//   Pieces:     tapestry(w, h, o)  shelf(o)  pottery(o)  plant(o)  lantern(o)  flagPole(o)  windowView(w, h, view)
//   Backdrops:  townCard(w, h, o)  (a painted town and skyline: hundreds of houses, towers, roofs, windows, smoke)
//               mountainCard(w, h, o)  (painted ridges with rock strata, snow, aerial perspective)
//   Presets:    dressPlace(root, kind, area, o)  kind: hall | deck | harbour | street | workshop | camp
//   Life:       walkers(id, routes, o) (servants walking loops), shifters(id, spots, o) (guards shifting weight),
//               birds(o), smokeColumns(points), flickers(points)  - background extras with small idle loops
// The detail-density gate that checks the result per region is scripts/detail_gate.py.
import * as THREE from "three";
import { lambert, basic, box } from "./sets";
import { model } from "./models";
import { glaze, metal } from "./materials";
import { candelabra, banner } from "./interior";
import { crate } from "./dressing";
import { Flame, Rising } from "./fx";
import { NOINK } from "../ink";
import { rng } from "../paint";
import type { PersonSpec, Rig, V3 } from "./Stage";

const canvas = (w: number, h: number) => { const c = document.createElement("canvas"); c.width = w; c.height = h; return [c, c.getContext("2d")!] as const; };
const ctex = (c: HTMLCanvasElement) => { const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t; };
const shadowed = <T extends THREE.Object3D>(g: T) => { g.traverse((o) => { if ((o as THREE.Mesh).isMesh) { o.castShadow = true; o.receiveShadow = true; } }); return g; };

// ---------------------------------------------------------------- pieces
/** a wall tapestry (faces +z): a painted scene panel (hills, a tree, a beast, a border of knots), fringe, a gold rod */
export function tapestry(w = 2.2, h = 3.0, o: { field?: string; border?: string; seed?: number } = {}): THREE.Group {
  const [c, g] = canvas(256, 352), r = rng(o.seed ?? 3), field = o.field ?? "#7a2a3a", border = o.border ?? "#d9a441";
  g.fillStyle = field; g.fillRect(0, 0, 256, 352);
  g.fillStyle = border; g.fillRect(0, 0, 256, 18); g.fillRect(0, 316, 256, 18); g.fillRect(0, 0, 18, 334); g.fillRect(238, 0, 18, 334);
  for (let x = 6; x < 256; x += 14) { g.fillStyle = field; g.beginPath(); g.arc(x, 9, 3, 0, 7); g.arc(x, 325, 3, 0, 7); g.fill(); }
  // the scene: layered hills, a tree, a stylised beast, stars
  const hills = ["#3f6a4a", "#557a52", "#6f8f5a"];
  hills.forEach((col, k) => { g.fillStyle = col; g.beginPath(); g.moveTo(18, 316); for (let x = 18; x <= 238; x += 10) g.lineTo(x, 230 + k * 22 + Math.sin(x * 0.05 + k * 2 + r()) * 14); g.lineTo(238, 316); g.closePath(); g.fill(); });
  g.fillStyle = "#4a2e1e"; g.fillRect(170, 170, 10, 70); g.fillStyle = "#2f5a3a"; g.beginPath(); g.arc(175, 160, 30, 0, 7); g.fill();
  g.fillStyle = border; g.beginPath(); g.ellipse(95, 205, 40, 18, 0, 0, 7); g.fill(); g.beginPath(); g.arc(130, 190, 14, 0, 7); g.fill();
  for (const [x, y] of [[60, 180], [80, 182], [100, 182], [120, 180]]) g.fillRect(x, y + 18, 5, 20);
  for (let k = 0; k < 18; k++) { g.fillStyle = "rgba(255,230,160,0.8)"; g.beginPath(); g.arc(30 + r() * 196, 30 + r() * 110, 2 + r() * 2, 0, 7); g.fill(); }
  for (let k = 0; k < 200; k++) { g.fillStyle = `rgba(0,0,0,${0.04 + r() * 0.05})`; g.fillRect(r() * 256, r() * 352, 1, 6); }       // weave
  const grp = new THREE.Group();
  const geo = new THREE.PlaneGeometry(w, h, 6, 8), p = geo.getAttribute("position") as THREE.BufferAttribute;
  for (let i = 0; i < p.count; i++) p.setZ(i, 0.03 * Math.sin((p.getX(i) / w) * Math.PI * 4));
  geo.computeVertexNormals();
  const cloth = new THREE.Mesh(geo, lambert({ map: ctex(c), side: THREE.DoubleSide })); cloth.position.y = -h / 2; grp.add(cloth);
  const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, w + 0.3, 10), metal("gold", { grain: true })); rod.rotation.z = Math.PI / 2; grp.add(rod);
  return shadowed(grp);
}

/** glazed pottery: a lathed jar or vase with painted bands (or a library vase) */
export function pottery(o: { seed?: number; h?: number } = {}): THREE.Object3D {
  const r = rng(o.seed ?? 1), h = o.h ?? 0.6 + r() * 0.5, k = Math.floor(r() * 4);
  if (k === 0) return model(["ceramic_vase_01", "ceramic_vase_03", "ceramic_pot", "planter_pot_clay"][Math.floor(r() * 4)], { scale: h / 0.6, seed: o.seed });
  const prof: [number, number][] = k === 1 ? [[0, 0], [0.16, 0], [0.24, 0.25], [0.2, 0.62], [0.09, 0.82], [0.11, 1], [0, 1]] : k === 2 ? [[0, 0], [0.2, 0], [0.26, 0.4], [0.16, 0.85], [0.18, 1], [0, 1]] : [[0, 0], [0.12, 0], [0.3, 0.3], [0.26, 0.55], [0.08, 0.75], [0.07, 1], [0, 1]];
  const cols = ["#2f5a8a", "#a8402a", "#3f7a5a", "#e3c27a", "#6a3a6a"];
  const [c, g] = canvas(128, 128); g.fillStyle = cols[Math.floor(r() * 5)]; g.fillRect(0, 0, 128, 128);
  g.fillStyle = "#f2e6c8"; g.fillRect(0, 40, 128, 10); g.fillRect(0, 86, 128, 6);
  for (let x = 0; x < 128; x += 16) { g.beginPath(); g.arc(x + 8, 66, 5, 0, 7); g.fill(); }
  const m = new THREE.MeshPhysicalMaterial({ map: ctex(c), roughness: 0.4, clearcoat: 1, clearcoatRoughness: 0.15 }); m.userData.env = true;
  const v = new THREE.Mesh(new THREE.LatheGeometry(prof.map(([x, y]) => new THREE.Vector2(x * h, y * h)), 32), m);
  return shadowed(v);
}

/** a wooden shelf unit stocked with pottery, boxes and books */
export function shelf(o: { w?: number; h?: number; seed?: number } = {}): THREE.Group {
  const g = new THREE.Group(), w = o.w ?? 1.8, h = o.h ?? 2.2, r = rng(o.seed ?? 7);
  const wood = lambert({ color: "#6a4228" });
  for (const x of [-w / 2, w / 2]) box(g, wood, 0.06, h, 0.45, x, h / 2, 0);
  box(g, wood, w, h, 0.03, 0, h / 2, -0.21);
  for (let k = 0; k < 4; k++) {
    const y = 0.1 + k * (h - 0.2) / 3.2; box(g, wood, w, 0.05, 0.45, 0, y, 0);
    let x = -w / 2 + 0.12;
    while (x < w / 2 - 0.15) {
      const kind = r();
      if (kind < 0.45) { const p = pottery({ seed: Math.floor(r() * 999), h: 0.22 + r() * 0.15 }); p.position.set(x + 0.1, y + 0.025, 0); g.add(p); x += 0.26; }
      else if (kind < 0.75) { for (let b = 0; b < 5; b++) { const bk = new THREE.Mesh(new THREE.BoxGeometry(0.045, 0.22 + r() * 0.06, 0.18), lambert({ color: ["#7a2a2a", "#2a4a7a", "#3f6a3f", "#8a6a2a"][b % 4] })); bk.position.set(x + b * 0.05, y + 0.14, 0); bk.rotation.z = (r() - 0.5) * 0.1; g.add(bk); } x += 0.3; }
      else { const cr = crate(0.2); cr.position.set(x + 0.1, y + 0.025, 0); g.add(cr); x += 0.26; }
    }
  }
  return shadowed(g);
}

/** a potted plant: a library fern / nettle, or a painted urn with a leafy shrub */
export function plant(o: { seed?: number; h?: number } = {}): THREE.Object3D {
  const r = rng(o.seed ?? 5), h = o.h ?? 1.2;
  const g = new THREE.Group();
  const urn = model("planter_pot_clay", { scale: h * 0.6, seed: o.seed }); g.add(urn);
  const leaf = lambert({ color: ["#4f7f40", "#5f8f4a", "#3f6f3a"][Math.floor(r() * 3)] });
  for (let k = 0; k < 14; k++) { const s = new THREE.Mesh(new THREE.IcosahedronGeometry(0.14 * h + r() * 0.08 * h, 0), leaf); s.position.set((r() - 0.5) * 0.45 * h, 0.45 * h + r() * 0.6 * h, (r() - 0.5) * 0.45 * h); g.add(s); }
  return shadowed(g);
}

/** a lantern (library model) with a warm glow inside (blooms) */
export function lantern(o: { scale?: number } = {}): THREE.Group & { light: V3 } {
  const g = new THREE.Group() as THREE.Group & { light: V3 }, s = o.scale ?? 1;
  g.add(model("wooden_lantern_01", { scale: s, contact: false }));
  const fl = new THREE.Mesh(new THREE.SphereGeometry(0.05 * s, 10, 8), basic({ color: "#ffcf80" })); (fl.material as THREE.MeshBasicMaterial).color.multiplyScalar(2.5);
  fl.position.y = 0.2 * s; fl.layers.set(NOINK); fl.userData.bloom = true; g.add(fl); g.light = [0, 0.2 * s, 0];
  return g;
}

/** a flag on a pole: a waving cloth (animated by flagsRig) */
export function flagPole(o: { h?: number; color?: string; seed?: number } = {}): THREE.Group {
  const g = new THREE.Group(), h = o.h ?? 4;
  const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.045, h, 8), lambert({ color: "#5a3a22" })); pole.position.y = h / 2; g.add(pole);
  const knob = new THREE.Mesh(new THREE.SphereGeometry(0.07, 10, 8), metal("gold")); knob.position.y = h; g.add(knob);
  const cloth = new THREE.Mesh(new THREE.PlaneGeometry(1.2, 0.8, 10, 4), lambert({ color: o.color ?? "#b8302f", side: THREE.DoubleSide }));
  cloth.position.set(0.62, h - 0.45, 0); cloth.userData.flag = { seed: o.seed ?? 1 }; g.add(cloth);
  return shadowed(g);
}

// ---------------------------------------------------------------- painted backdrops
/** a painted town and skyline (faces +z): rows of houses with roofs and windows receding, towers, domes, smoke */
export function townCard(w = 200, h = 60, o: { seed?: number; wall?: string; roof?: string[]; haze?: string } = {}): THREE.Mesh {
  const W = 2048, Hh = Math.round((W * h) / w), [c, g] = canvas(W, Hh), r = rng(o.seed ?? 9);
  const roofs = o.roof ?? ["#b8483a", "#4a5a9a", "#a86a3a", "#6a7a8a"], haze = o.haze ?? "#cfd8e8";
  for (let row = 0; row < 7; row++) {
    const base = Hh * (0.55 + row * 0.07), s = 0.5 + row * 0.12, fade = 0.55 - row * 0.08;
    for (let x = -20; x < W; x += (40 + r() * 30) * s) {
      const bw = (34 + r() * 30) * s, bh = (30 + r() * 50) * s;
      g.fillStyle = o.wall ?? ["#f4efe6", "#ece2d2", "#f7f2ea", "#e6dccb"][Math.floor(r() * 4)]; g.fillRect(x, base - bh, bw, bh + Hh);
      g.fillStyle = roofs[Math.floor(r() * roofs.length)]; g.beginPath(); g.moveTo(x - 3, base - bh); g.lineTo(x + bw / 2, base - bh - bw * 0.45); g.lineTo(x + bw + 3, base - bh); g.fill();
      g.fillStyle = "#3a3448"; for (let wy = base - bh + 8 * s; wy < base - 6 * s; wy += 14 * s) for (let wx = x + 5 * s; wx < x + bw - 6 * s; wx += 11 * s) if (r() < 0.6) g.fillRect(wx, wy, 4 * s, 6 * s);
      g.strokeStyle = "rgba(30,24,40,0.6)"; g.lineWidth = 1.2; g.strokeRect(x, base - bh, bw, bh);
    }
    g.fillStyle = haze; g.globalAlpha = Math.max(0, fade); g.fillRect(0, 0, W, base); g.globalAlpha = 1;
  }
  for (let k = 0; k < 9; k++) {                                   // towers and domes above the roofs
    const x = r() * W, bh = 90 + r() * 120, bw = 26 + r() * 16, base = Hh * (0.62 + r() * 0.1);
    g.fillStyle = "#efe8dc"; g.fillRect(x, base - bh, bw, bh); g.strokeStyle = "rgba(30,24,40,0.7)"; g.strokeRect(x, base - bh, bw, bh);
    g.fillStyle = r() < 0.5 ? "#4a5a9a" : "#c9a23a";
    if (r() < 0.5) { g.beginPath(); g.moveTo(x - 4, base - bh); g.lineTo(x + bw / 2, base - bh - bw * 1.6); g.lineTo(x + bw + 4, base - bh); g.fill(); }
    else { g.beginPath(); g.arc(x + bw / 2, base - bh, bw * 0.7, Math.PI, 0); g.fill(); }
    g.fillStyle = "#b8302f"; g.fillRect(x + bw / 2, base - bh - bw * 1.9, 2, 20); g.fillRect(x + bw / 2 + 2, base - bh - bw * 1.9, 14, 8);
  }
  for (let k = 0; k < 6; k++) { const x = r() * W, y = Hh * (0.5 + r() * 0.1); for (let q = 0; q < 6; q++) { g.fillStyle = `rgba(230,230,235,${0.35 - q * 0.05})`; g.beginPath(); g.arc(x + q * 6, y - q * 16, 8 + q * 4, 0, 7); g.fill(); } }
  const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), basic({ map: ctex(c), transparent: true, fog: false }));
  m.layers.set(NOINK); return m;
}
/** painted mountains (faces +z): several ridges with rock strata, snowcaps, aerial perspective toward the sky */
export function mountainCard(w = 600, h = 160, o: { seed?: number; rock?: string; sky?: string } = {}): THREE.Mesh {
  const W = 2048, Hh = Math.round((W * h) / w), [c, g] = canvas(W, Hh), r = rng(o.seed ?? 11);
  const sky = new THREE.Color(o.sky ?? "#cfe0f4"), rock = new THREE.Color(o.rock ?? "#6f7a96");
  for (let ridge = 0; ridge < 4; ridge++) {
    const t = 1 - ridge / 4, col = rock.clone().lerp(sky, 0.15 + 0.6 * (1 - ridge / 3) * 0.6 + (3 - ridge) * 0.08);
    const pts: [number, number][] = []; let y = Hh * (0.25 + ridge * 0.12);
    for (let x = 0; x <= W; x += 24) { y += (r() - 0.5) * 60 * t + (Hh * (0.25 + ridge * 0.12) - y) * 0.08; pts.push([x, Math.max(10, y)]); }
    g.fillStyle = `#${col.getHexString()}`; g.beginPath(); g.moveTo(0, Hh); pts.forEach(([x, yy]) => g.lineTo(x, yy)); g.lineTo(W, Hh); g.closePath(); g.fill();
    g.save(); g.clip();
    for (let k = 0; k < 220; k++) { g.strokeStyle = `rgba(30,30,50,${0.06 + r() * 0.08})`; g.lineWidth = 2; const x = r() * W, yy = r() * Hh; g.beginPath(); g.moveTo(x, yy); g.lineTo(x + 20 + r() * 40, yy + 30 + r() * 30); g.stroke(); }
    pts.forEach(([x, yy], i) => { if (i % 2 === 0 && yy < Hh * (0.32 + ridge * 0.1)) { g.fillStyle = "rgba(250,252,255,0.95)"; g.beginPath(); g.moveTo(x - 30, yy + 34); g.lineTo(x, yy); g.lineTo(x + 30, yy + 30); g.lineTo(x + 10, yy + 22); g.lineTo(x - 6, yy + 36); g.fill(); } });
    g.restore();
    g.strokeStyle = "rgba(30,30,50,0.45)"; g.lineWidth = 2.5; g.beginPath(); pts.forEach(([x, yy], i) => (i ? g.lineTo(x, yy) : g.moveTo(x, yy))); g.stroke();
  }
  const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), basic({ map: ctex(c), transparent: true, fog: false }));
  m.layers.set(NOINK); return m;
}
/** a window with a view out: a stone frame over a painted landscape (town or mountains), glowing a little */
export function windowView(w = 1.4, h = 2.4, view: "town" | "mountains" = "mountains", seed = 3): THREE.Group {
  const g = new THREE.Group();
  const card = view === "town" ? townCard(w, h, { seed }) : mountainCard(w, h, { seed });
  (card.material as THREE.MeshBasicMaterial).color.setScalar(1.15); g.add(card);
  const frame = lambert({ color: "#cdbfa8" });
  box(g, frame, w + 0.24, 0.16, 0.2, 0, h / 2 + 0.08, 0.05); box(g, frame, w + 0.24, 0.2, 0.3, 0, -h / 2 - 0.1, 0.08);
  for (const x of [-w / 2 - 0.06, w / 2 + 0.06]) box(g, frame, 0.12, h, 0.2, x, 0, 0.05);
  box(g, lambert({ color: "#3a3040" }), 0.04, h, 0.04, 0, 0, 0.06); box(g, lambert({ color: "#3a3040" }), w, 0.04, 0.04, 0, h * 0.15, 0.06);
  return g;
}

// ---------------------------------------------------------------- dressing presets per place type
export type PlaceKind = "hall" | "deck" | "harbour" | "street" | "workshop" | "camp";
/** dress a wall-lined area [x0, z0, x1, z1] of a place: returns the light points (candles, lanterns) for bokeh */
export function dressPlace(root: THREE.Object3D, kind: PlaceKind, area: [number, number, number, number], o: { seed?: number; n?: number; wall?: "left" | "right" | "back"; keep?: [number, number, number, number][] } = {}): V3[] {
  const r = rng(o.seed ?? 21), lights: V3[] = [], [x0, z0, x1, z1] = area, n = o.n ?? 8;
  const free = (x: number, z: number) => !(o.keep ?? []).some(([a, b, c, d]) => x > a && x < c && z > b && z < d);
  const place = (obj: THREE.Object3D, x: number, z: number, ry = 0) => { obj.position.set(x, 0, z); obj.rotation.y = ry; root.add(obj); };
  const pick = (items: (() => THREE.Object3D)[]) => items[Math.floor(r() * items.length)]();
  const lantern1 = () => { const l = lantern({ scale: 1.2 }); return l; };
  const catalog: Record<PlaceKind, (() => THREE.Object3D)[]> = {
    hall: [() => shelf({ seed: Math.floor(r() * 99) }), () => plant({ seed: Math.floor(r() * 99) }), () => pottery({ seed: Math.floor(r() * 99), h: 0.9 }), () => candelabra({ n: 5 }), () => model("painted_wooden_bench", { seed: 2 })],
    deck: [() => model("barrel_03"), () => model("wooden_crate_01"), lantern1, () => model("wicker_basket_01"), () => model("wooden_bucket_01")],
    harbour: [() => model("wooden_barrels_01", { scale: 0.8 }), () => model("wooden_crate_02"), lantern1, () => flagPole({ color: ["#b8302f", "#2f5aa8"][Math.floor(r() * 2)] }), () => model("wicker_basket_02")],
    street: [() => plant({ seed: Math.floor(r() * 99) }), () => pottery({ seed: Math.floor(r() * 99), h: 0.8 }), lantern1, () => model("wooden_stool_01"), () => model("wine_barrel_01", { scale: 0.9 })],
    workshop: [() => shelf({ seed: Math.floor(r() * 99), h: 1.8 }), () => model("painted_wooden_table"), () => model("wooden_bucket_01"), () => model("tree_stump_01", { scale: 0.7 }), lantern1],
    camp: [() => flagPole({ h: 5, color: ["#b8302f", "#e0b04a", "#2f5aa8"][Math.floor(r() * 3)] }), () => model("stone_fire_pit"), () => model("wooden_crate_01"), () => model("wicker_basket_01"), lantern1],
  };
  const along = o.wall ?? "left";
  for (let i = 0; i < n; i++) {
    const u = (i + 0.5 + (r() - 0.5) * 0.4) / n;
    const x = along === "back" ? x0 + (x1 - x0) * u : along === "left" ? x0 + r() * 0.3 : x1 - r() * 0.3;
    const z = along === "back" ? z0 + r() * 0.3 : z0 + (z1 - z0) * u;
    if (!free(x, z)) continue;
    const obj = pick(catalog[kind]);
    place(obj, x, z, along === "left" ? Math.PI / 2 : along === "right" ? -Math.PI / 2 : 0);
    const c = obj as THREE.Object3D & { flames?: V3[]; light?: V3 };
    for (const f of c.flames ?? (c.light ? [c.light] : [])) { const p = new THREE.Vector3(...f).applyEuler(obj.rotation).add(obj.position); lights.push([p.x, p.y, p.z]); }
  }
  return lights;
}

// ---------------------------------------------------------------- background life
/** servants walking loops between waypoints (Actors with the walk cycle), each with its own phase */
export function walkers(id: string, routes: V3[][], o: { costumes?: string[]; speed?: number; seed?: number } = {}): PersonSpec[] {
  const r = rng(o.seed ?? 31), sp = o.speed ?? 0.9;
  return routes.map((route, k) => {
    const segs = route.map((p, i) => new THREE.Vector3(...p).distanceTo(new THREE.Vector3(...route[(i + 1) % route.length])));
    const L = segs.reduce((a, b) => a + b, 0), phase = r() * L, costume = (o.costumes ?? ["courtOfficial", "courtOfficial2", "scholar"])[k % (o.costumes?.length ?? 3)];
    const posAt = (t: number): [V3, V3] => {
      let d = (phase + t * sp) % L;
      for (let i = 0; i < route.length; i++) {
        if (d <= segs[i]) { const a = new THREE.Vector3(...route[i]), b = new THREE.Vector3(...route[(i + 1) % route.length]); const p = a.clone().lerp(b, d / segs[i]); return [[p.x, p.y, p.z], [b.x, b.y, b.z]]; }
        d -= segs[i];
      }
      return [route[0], route[1]];
    };
    return { id: `${id}${k}`, extra: true, at: (t: number) => posAt(t)[0], faceTo: (t: number) => posAt(t)[1], props: () => ({ costume, seed: 40 + k, face: "neutral", pose: "stand", walk: 1, blinks: [] }) };
  });
}
/** guards / courtiers standing at spots, shifting pose every few seconds (each on its own clock) */
export function shifters(id: string, spots: V3[], o: { costumes?: string[]; poses?: string[]; every?: number; face?: V3; seed?: number } = {}): PersonSpec[] {
  const r = rng(o.seed ?? 41), poses = o.poses ?? ["stand", "hips", "hold", "stand"];
  return spots.map((p, k) => {
    const every = (o.every ?? 3) * (0.7 + r() * 0.6), off = r() * every, costume = (o.costumes ?? ["hanGuard"])[k % (o.costumes?.length ?? 1)];
    const track = Array.from({ length: 12 }, (_, i) => ({ t: off + i * every, v: poses[(i + k) % poses.length] }));
    return { id: `${id}${k}`, extra: true, at: () => p, faceTo: o.face ? () => o.face! : undefined, props: () => ({ costume, seed: 60 + k, face: "neutral", pose: [{ t: 0, v: poses[k % poses.length] }, ...track], blinks: [] }) };
  });
}
/** a flock of birds crossing the sky: flapping V sprites on a slow drift */
export const birds = (o: { n?: number; from: V3; to: V3; period?: number; size?: number; seed?: number }): Rig => (ctx) => {
  const r = rng(o.seed ?? 3), n = o.n ?? 7, mat = new THREE.MeshBasicMaterial({ color: "#2a2a38", side: THREE.DoubleSide, fog: false });
  const mk = () => { const s = new THREE.Shape(); s.moveTo(-1, 0.3); s.quadraticCurveTo(-0.5, 0.4, 0, 0); s.quadraticCurveTo(0.5, 0.4, 1, 0.3); s.quadraticCurveTo(0.5, 0.15, 0, -0.1); s.quadraticCurveTo(-0.5, 0.15, -1, 0.3); return new THREE.ShapeGeometry(s); };
  const bs = Array.from({ length: n }, (_, k) => { const m = new THREE.Mesh(mk(), mat); m.layers.set(NOINK); m.userData.off = [(r() - 0.5) * 8, (r() - 0.5) * 3, (r() - 0.5) * 4, r() * 6]; ctx.root.add(m); return m; });
  const A = new THREE.Vector3(...o.from), B = new THREE.Vector3(...o.to), sz = o.size ?? 0.8;
  return (t, cam) => bs.forEach((m) => {
    const [dx, dy, dz, ph] = m.userData.off as number[], u = ((t + ph) / (o.period ?? 14)) % 1;
    m.position.copy(A).lerp(B, u).add(new THREE.Vector3(dx, dy + Math.sin(t * 1.3 + ph) * 0.4, dz));
    m.quaternion.copy(cam.quaternion); const flap = 0.4 + 0.6 * Math.abs(Math.sin(t * 9 + ph * 3)); m.scale.set(sz, sz * flap, 1);
  });
};
/** smoke columns rising from points (chimneys, braziers, distant fires) */
export const smokeColumns = (points: V3[], o: { scale?: number; tint?: number } = {}): Rig => (ctx) => {
  const sm = points.map((p, i) => { const s = new Rising(10, "smoke", 2.6 * (o.scale ?? 1), 70 + i); s.group.position.set(...p); ctx.root.add(s.group); return s; });
  return (t) => sm.forEach((s) => s.update(t, 1, o.tint ?? 1.0, 0.8, 14));
};
/** flickering flames at points (torches, braziers, hearths) */
export const flickers = (points: V3[], size = 0.6): Rig => (ctx) => {
  const fl = points.map(([x, y, z], i) => { const f = new Flame(size, x + z + i); f.mesh.position.set(x, y, z); ctx.root.add(f.mesh); return f; });
  return (t, cam) => fl.forEach((f) => f.update(t, 1, cam));
};
/** wave the cloth of every flagPole under the rig's root */
export const flagsRig = (): Rig => (ctx) => {
  const cloths: THREE.Mesh[] = []; ctx.root.traverse((o) => { if ((o as THREE.Mesh).userData?.flag) cloths.push(o as THREE.Mesh); });
  const base = cloths.map((c) => Float32Array.from((c.geometry.getAttribute("position") as THREE.BufferAttribute).array as Float32Array));
  return (t) => cloths.forEach((c, i) => { const p = c.geometry.getAttribute("position") as THREE.BufferAttribute, b = base[i], s = (c.userData.flag as { seed: number }).seed;
    for (let k = 0; k < p.count; k++) { const x = b[k * 3] + 0.6; p.setZ(k, 0.12 * x * Math.sin(t * 5 + x * 4 + s)); } p.needsUpdate = true; c.geometry.computeVertexNormals(); });
};
