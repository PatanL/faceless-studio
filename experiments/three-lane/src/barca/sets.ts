// story-barca-shield sets (our own code): Barca's wall, the strip of dirt and the street inside it, the plain and the
// Persian camp outside (one world, different places by camera), the shield macro (macroSet with a dirt ground), and
// the cross-section under the wall (crossSectionSet with the tunnel, the wall above, the countershaft).
import * as THREE from "three";
import type { SetBuild } from "../kit/sets";
import { box, cyl, plane, skyDome, glowSprite, lambert, makeKey } from "../kit/sets";
import { stoneCourses, grainPlanks, dress, clouds } from "../kit/dressing";
import { macroSet, crossSectionSet, type Band } from "../kit/cutaways";
import { NOINK } from "../ink";

const rng = (seed: number) => () => { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; };
const canvas = (w: number, h: number) => { const c = document.createElement("canvas"); c.width = w; c.height = h; return [c, c.getContext("2d")!] as const; };
const ctex = (c: HTMLCanvasElement, rep: [number, number] = [1, 1]) => {
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(...rep); t.anisotropy = 8; return t;
};
const INK = "#1b1240";

/** packed earth: tan with darker clods, pebbles with an ink rim, scuffs (never a flat fill) */
export function dirtTex(rep: [number, number] = [1, 1], seed = 9, base = "#c9a06a") {
  const [c, g] = canvas(512, 512); const r = rng(seed);
  g.fillStyle = base; g.fillRect(0, 0, 512, 512);
  for (let k = 0; k < 90; k++) { g.fillStyle = `rgba(120, 78, 40, ${0.08 + r() * 0.12})`; g.beginPath(); g.ellipse(r() * 512, r() * 512, 20 + r() * 60, 10 + r() * 30, r() * 3, 0, Math.PI * 2); g.fill(); }
  for (let k = 0; k < 160; k++) {
    const x = r() * 512, y = r() * 512, rr = 2 + r() * 6;
    g.fillStyle = ["#a98257", "#8e6a45", "#d9bd8c"][k % 3]; g.beginPath(); g.ellipse(x, y, rr, rr * 0.7, r() * 3, 0, Math.PI * 2); g.fill();
    if (rr > 5) { g.strokeStyle = INK; g.lineWidth = 1.5; g.stroke(); }
  }
  g.strokeStyle = "rgba(90, 60, 30, 0.35)"; g.lineWidth = 2;
  for (let k = 0; k < 40; k++) { const x = r() * 512, y = r() * 512; g.beginPath(); g.moveTo(x, y); g.lineTo(x + (r() - 0.5) * 40, y + (r() - 0.5) * 12); g.stroke(); }
  return ctex(c, rep);
}

/** a round bronze shield (hero prop): a lathe dish with a rim, a boss and inked rings, lying face up */
export function shieldMesh(R = 0.45) {
  const g = new THREE.Group();
  const prof = [[0, 0.06], [R * 0.2, 0.058], [R * 0.85, 0.035], [R, 0.02], [R * 1.02, 0.0], [R * 0.9, 0.0], [0, 0.0]].map(([x, y]) => new THREE.Vector2(x, y));
  const bronze = lambert({ color: "#d9a43a" });
  const dish = new THREE.Mesh(new THREE.LatheGeometry(prof, 40), bronze); dish.castShadow = true; g.add(dish);
  const rim = new THREE.Mesh(new THREE.TorusGeometry(R * 0.96, R * 0.05, 8, 40), lambert({ color: "#a8742a" })); rim.rotation.x = Math.PI / 2; rim.position.y = 0.02; g.add(rim);
  const boss = new THREE.Mesh(new THREE.SphereGeometry(R * 0.16, 16, 10, 0, Math.PI * 2, 0, Math.PI / 2), lambert({ color: "#f2c45a" })); boss.position.y = 0.05; g.add(boss);
  for (const k of [0.45, 0.7]) { const ring = new THREE.Mesh(new THREE.TorusGeometry(R * k, R * 0.012, 6, 40), lambert({ color: "#8a5a22" })); ring.rotation.x = Math.PI / 2; ring.position.y = 0.06 - k * 0.04; g.add(ring); }
  return g;
}

// world layout (metres): the wall runs along x at z = 0 (3 m thick, 7 m high, walk at y 7); inside is z < -1.5
export const WALL = { z0: -1.5, z1: 1.5, h: 7, gateX: 12, towerX: -10 };
export const INNER_Z = -3.2;                                         // the dirt strip where the smith walks
export const CAMP = { lord: [-14, 0, 46] as [number, number, number] };

/** Barca: wall, tower, gate, the dirt strip and the street inside, the plain and the Persian camp outside */
export function barcaSet(o: { ram?: boolean; ladders?: boolean; night?: boolean } = {}): SetBuild {
  const root = new THREE.Group(), glows: THREE.Object3D[] = [];
  const r = rng(17);
  const stone = lambert({ map: stoneCourses([6, 2], { hue: 34, light: 54, seed: 3 }) });
  const stoneDark = lambert({ map: stoneCourses([2, 2], { hue: 30, light: 50, seed: 5 }) });
  // ground: the plain (sun-baked earth) and the packed dirt inside
  plane(root, lambert({ map: dirtTex([60, 60], 4, "#bf9560") }), 600, 600, 0, 0, 0, -Math.PI / 2);
  // the wall, in segments round the gate (opening 3.4 m wide, 4.6 m high)
  const segs: [number, number][] = [[-40, WALL.gateX - 1.7], [WALL.gateX + 1.7, 44]];
  for (const [a, b] of segs) box(root, stone, b - a, WALL.h, WALL.z1 - WALL.z0, (a + b) / 2, WALL.h / 2, 0);
  box(root, stone, 3.4, WALL.h - 4.6, WALL.z1 - WALL.z0, WALL.gateX, 4.6 + (WALL.h - 4.6) / 2, 0);
  // gate doors (planks) and the merlons along the outer edge of the walk
  const planks = lambert({ map: grainPlanks([2, 1], { hue: 26, light: 40, vertical: true }) });
  box(root, planks, 3.4, 4.6, 0.3, WALL.gateX, 2.3, 0.9);
  for (let x = -39; x < 44; x += 1.6) if (Math.abs(x - WALL.gateX) > 0.2 || true) box(root, stone, 0.9, 1.1, 0.5, x, WALL.h + 0.55, 1.25);
  // a low inner parapet so the guards lean on something
  box(root, stoneDark, 84, 0.5, 0.3, 2, WALL.h + 0.25, -1.35);
  // the tower at the corner
  box(root, stoneDark, 5.5, 11, 5.5, WALL.towerX, 5.5, 0);
  for (let i = 0; i < 4; i++) for (const [dx, dz] of [[-2.2, 0], [2.2, 0], [0, -2.2], [0, 2.2]]) box(root, stoneDark, dx ? 0.5 : 1.0, 1.0, dz ? 0.5 : 1.0, WALL.towerX + dx + (dz ? (i - 1.5) * 1.2 : 0), 11.5, dz + (dx ? (i - 1.5) * 1.2 : 0));
  // inside: the dirt strip, then the street (paving) and a row of houses with flat roofs, doors and windows
  plane(root, lambert({ map: dirtTex([10, 2], 8, "#b88c58") }), 84, 4, 2, 0.01, -3.5, -Math.PI / 2);
  plane(root, lambert({ map: stoneCourses([20, 2], { hue: 30, light: 60, seed: 9 }) }), 84, 5, 2, 0.012, -8, -Math.PI / 2);
  const walls = ["#e7d3ad", "#dcc29a", "#efdcb8", "#d8b98d"];
  for (let x = -36; x < 40; x += 6.5) {
    const h = 4.5 + r() * 2.5, w = 5.6 + r() * 0.6;
    box(root, lambert({ color: walls[Math.floor(r() * 4)] }), w, h, 5, x, h / 2, -13.2);
    box(root, lambert({ color: "#8a5a3a" }), w + 0.3, 0.3, 5.3, x, h + 0.15, -13.2);
    box(root, lambert({ map: grainPlanks([1, 1], { hue: 22, light: 34, vertical: true }) }), 1.1, 2.1, 0.1, x - 1, 1.05, -10.66);
    box(root, lambert({ color: "#3a2a3e" }), 0.9, 0.8, 0.1, x + 1.5, 2.6, -10.66);
  }
  // street life: sacks, barrels, buckets, crates along the house fronts (kept off the dirt strip and the walk)
  dress(root, { area: [-34, -10.3, 38, -9.6], y: 0, n: 22, kit: ["sack", "barrel", "bucket", "crate"], seed: 12 });
  // outside: ladders and the ram at the gate (the assault), the plain and the Persian camp
  if (o.ladders !== false) for (const x of [-2, 3, 20]) {
    const lad = new THREE.Group(); const pole = lambert({ color: "#7a4a26" });
    box(lad, pole, 0.12, 8.2, 0.12, -0.35, 4.1, 0); box(lad, pole, 0.12, 8.2, 0.12, 0.35, 4.1, 0);
    for (let y = 0.6; y < 8; y += 0.6) box(lad, pole, 0.7, 0.08, 0.08, 0, y, 0);
    lad.position.set(x, 0, 3.6); lad.rotation.x = -0.32; root.add(lad);
  }
  const ram = new THREE.Group();
  if (o.ram !== false) {
    box(ram, planks, 2.6, 2.2, 5, 0, 2.6, 0);
    const roof = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 2.2, 1.4, 4), lambert({ color: "#7a3b2c" })); roof.rotation.y = Math.PI / 4; roof.scale.set(1, 1, 1.9); roof.position.y = 4.4; ram.add(roof);
    const log = new THREE.Mesh(new THREE.CylinderGeometry(0.28, 0.32, 6, 12), lambert({ color: "#6b4426" })); log.rotation.x = Math.PI / 2; log.position.set(0, 1.6, -0.6); log.castShadow = true; ram.add(log);
    for (const [x, z] of [[-1.1, -2], [1.1, -2], [-1.1, 2], [1.1, 2]]) { const wh = new THREE.Mesh(new THREE.CylinderGeometry(0.55, 0.55, 0.25, 16), lambert({ color: "#4b2e1a" })); wh.rotation.z = Math.PI / 2; wh.position.set(x, 0.55, z); ram.add(wh); }
    ram.position.set(WALL.gateX, 0, 5.4); root.add(ram);
  }
  // the camp: rings of tents, banners on tall poles (they show over the wall from inside), cook fires and smoke
  const tentCols = ["#e9dcc0", "#d8c49c", "#c94b3a", "#e0b04a", "#5f7fbf"];
  const tents: [number, number, number][] = [];
  for (let ring = 0; ring < 3; ring++) for (let k = 0; k < 18 + ring * 6; k++) {
    const a = -1.25 + (2.5 * k) / (17 + ring * 6), R = 34 + ring * 16;
    tents.push([Math.sin(a) * R * 1.4, Math.cos(a) * R, 1 + r() * 0.6]);
  }
  for (const [x, z, s] of tents) {
    const t = new THREE.Mesh(new THREE.ConeGeometry(2.2 * s, 3 * s, 6), lambert({ color: tentCols[Math.floor(r() * tentCols.length)] }));
    t.position.set(x, 1.5 * s, z); t.castShadow = true; root.add(t);
  }
  // the commander's tent: striped, bigger, with an awning
  const lt = new THREE.Group();
  const big = new THREE.Mesh(new THREE.CylinderGeometry(3.6, 4.2, 3.2, 12), lambert({ map: stripes() })); big.position.y = 1.6; lt.add(big);
  const top = new THREE.Mesh(new THREE.ConeGeometry(4.6, 2.6, 12), lambert({ color: "#7a2a4a" })); top.position.y = 4.5; lt.add(top);
  lt.position.set(CAMP.lord[0], 0, CAMP.lord[2] + 5); root.add(lt);
  for (const [x, z, col] of [[-6, 9, "#c94b3a"], [6, 10, "#e0b04a"], [22, 9, "#5f7fbf"], [-22, 11, "#c94b3a"], [CAMP.lord[0] + 4, CAMP.lord[2] + 3, "#7a2a4a"]] as [number, number, string][]) {
    cyl(root, lambert({ color: "#5b3a22" }), 0.12, 16, x, 8, z, 6);
    const flag = new THREE.Mesh(new THREE.PlaneGeometry(3, 1.8), lambert({ color: col, side: THREE.DoubleSide })); flag.position.set(x + 1.5, 15, z); root.add(flag);
  }
  for (const [x, z] of [[-8, 30], [10, 34], [26, 40], [-26, 44], [4, 60]]) {
    box(root, lambert({ color: "#4b3a2a" }), 1.2, 0.3, 1.2, x, 0.15, z);
    glows.push(glowSprite(root, [255, 170, 90], o.night ? 6 : 2.5, x, 1.0, z));
  }
  // painted hills on the horizon, sky and inked clouds
  for (let k = 0; k < 9; k++) { const hill = new THREE.Mesh(new THREE.SphereGeometry(40 + r() * 40, 16, 8, 0, Math.PI * 2, 0, Math.PI / 2), lambert({ color: ["#b9a27a", "#a8936e", "#c4ad84"][k % 3] })); hill.scale.y = 0.25; hill.position.set(-200 + k * 50, 0, 220 + r() * 40); root.add(hill); }
  skyDome(root, o.night ? "#1a1840" : "#6f9be0", o.night ? "#3a3470" : "#a9c6ee", o.night ? "#6a5a8a" : "#f3dcae", 400, o.night ? 120 : 0);
  clouds(root, { n: 10, x: [-160, 160], y: [50, 90], z: [120, 260], size: 46, seed: 4 });
  clouds(root, { n: 6, x: [-160, 160], y: [50, 90], z: [-260, -140], size: 46, seed: 6 });
  const key = makeKey(root, [-30, 60, -40], [0, 0, 0], 80);
  return { root, key, glows, extra: { ram }, fogScale: 6 };
}
function stripes() {
  const [c, g] = canvas(256, 64);
  for (let k = 0; k < 16; k++) { g.fillStyle = k % 2 ? "#e9dcc0" : "#7a2a4a"; g.fillRect(k * 16, 0, 16, 64); }
  return ctex(c, [2, 1]);
}

/** the shield macro: macroSet's tabletop and bokeh wall, with a dirt ground laid over the boards (the macro has no
 * dirt surface) and the shield at the origin */
export function shieldMacroSet(o: { night?: boolean } = {}): SetBuild {
  const s = macroSet({ surface: "wood", bokeh: o.night ? [[120, 140, 255], [255, 190, 120]] : [[255, 196, 120], [255, 150, 90], [250, 220, 160]], wall: o.night ? "#1c1838" : "#6a4a3a", seed: 11 });
  // a wide dirt ground (a 6 m plane showed its edge in the last shot) and a darker earth at night
  const dirt = plane(s.root, lambert({ map: dirtTex([12, 12], 21, o.night ? "#7a6a72" : "#c9a06a") }), 24, 24, 0, 0.004, -6, -Math.PI / 2);
  dirt.receiveShadow = true;
  // pebbles and a few clods around the shield, inked
  const r = rng(5);
  for (let k = 0; k < 26; k++) {
    const m = new THREE.Mesh(new THREE.DodecahedronGeometry(0.012 + r() * 0.03, 0), lambert({ color: ["#a98257", "#8e6a45", "#d9bd8c"][k % 3] }));
    const a = r() * Math.PI * 2, d = 0.42 + r() * 0.6; m.position.set(Math.cos(a) * d, 0.015, Math.sin(a) * d - 0.1); m.castShadow = true; s.root.add(m);
  }
  const sh = shieldMesh(0.36); s.root.add(sh);
  return { ...s, extra: { ...s.extra, shield: sh } };
}

/** the cut under the wall: soil bands, the Persian tunnel (cavity), the wall standing on top, the shield on the
 * surface (over solid soil on the left, over the tunnel on the right), and a dark countershaft that grows down */
export const SEC = { W: 12, cav: { x: 2.2, y: -2.6, w: 6.0, h: 2.0 }, shieldSolid: -3.6, shieldHollow: 2.2 };
export function sectionSet(): SetBuild {
  const bands: Band[] = [{ h: 0.6, color: "#b98a52", speck: "#8e6a45" }, { h: 1.6, color: "#c8692f", speck: "#a24f22" }, { h: 1.6, color: "#9b8a7a", speck: "#6f6258" }, { h: 1.6, color: "#6a5a7a", speck: "#4a3e5a" }];
  const s = crossSectionSet({ bands, width: SEC.W, depth: 4, cavity: { ...SEC.cav, d: 1.6, color: "#3a2a26" }, grass: false, frame: true, sky: ["#1e2a5a", "#3a3a7a", "#7a6a9a"], seed: 8 });
  // the surface: packed dirt on top of the block
  box(s.root, lambert({ map: dirtTex([4, 1], 13) }), SEC.W, 0.12, 4, 0, 0.06, -2);
  // a slice of Barca's wall standing on it (right end, over the tunnel's far end) and the gate's ram beyond
  box(s.root, lambert({ map: stoneCourses([2, 2], { hue: 34, light: 60, seed: 3 }) }), 2.2, 4.2, 3.6, 4.6, 2.1, -1.9);
  const sh1 = shieldMesh(0.42), sh2 = shieldMesh(0.42);
  sh1.position.set(SEC.shieldSolid, 0.12, -0.6); sh2.position.set(SEC.shieldHollow, 0.12, -0.6); s.root.add(sh1, sh2);
  // tunnel timbers and a lamp on the back wall
  const wood = lambert({ map: grainPlanks([1, 1], { hue: 26, light: 38 }) });
  for (const x of [-0.4, 2.2, 4.8]) { box(s.root, wood, 0.16, SEC.cav.h, 0.16, x, SEC.cav.y - SEC.cav.h / 2, -1.4); box(s.root, wood, 0.9, 0.14, 1.5, x, SEC.cav.y - 0.07, -0.8); }
  const lamp = new THREE.Mesh(new THREE.SphereGeometry(0.07, 10, 8), new THREE.MeshBasicMaterial({ color: "#ffd27a", fog: false })); lamp.layers.set(NOINK);
  lamp.position.set(1.0, SEC.cav.y - 0.5, -1.45); s.root.add(lamp);
  s.glows.push(glowSprite(s.root, [255, 190, 110], 2.6, 1.0, SEC.cav.y - 0.5, -1.3));
  // the countershaft (grown by the story rig): a dark slot in front of the face, from the surface down
  const shaft = new THREE.Mesh(new THREE.PlaneGeometry(1.0, 1), lambert({ color: "#2a1d1a" }));
  shaft.position.set(SEC.shieldHollow, 0, 0.02); shaft.visible = false; s.root.add(shaft);
  return { ...s, extra: { ...s.extra, shieldSolid: sh1, shieldHollow: sh2, shaft, lamp } };
}
